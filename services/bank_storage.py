"""Read large exam shards incrementally; share only immutable strings."""
import gzip
import lzma
import hashlib
import json
from copy import deepcopy
from collections import OrderedDict
from pathlib import Path

import ijson


def mark_ai_exam_provenance(exam):
    """Do not launder a generated exam into an official school paper."""
    result = deepcopy(exam)
    result.update(is_ai_harvested=True, is_real_bank_question=False,
                  provenance_kind='ai_generated', source_verification='not_official_exam')
    for part in ('p1', 'p2', 'p3', 'part_viet'):
        for question in result.get(part, []) or []:
            if isinstance(question, dict):
                question.update(is_ai_generated=True, is_real_bank_question=False,
                    provenance_kind='ai_generated', source_verification='not_official_exam')
    return result


def calibration_eligibility(question, review, *, subject, grade, part):
    """Separate legacy practice material from independently verified anchors.

    Review must come from the maintained source-review registry, not question
    metadata. An ADN, famous school name or is_real flag cannot approve a task.
    """
    reasons = []
    if question.get('is_ai_generated') or question.get('provenance_kind') == 'ai_generated':
        reasons.append('generated_material_not_official_anchor')
    identity = content_identity(question, subject=subject, grade=grade, part=part,
                                shared_context=question.get('shared_context'))
    if not isinstance(review, dict):
        review = {}
    if review.get('content_adn') != identity['content_adn']:
        reasons.append('no_matching_independent_content_review')
    if (review.get('subject'), review.get('grade'), review.get('part')) != (subject, grade, part):
        reasons.append('review_context_mismatch')
    for field in ('paper_source_url', 'paper_sha256', 'answer_source_url', 'answer_sha256',
                  'source_locator', 'reviewer', 'reviewed_on', 'curriculum_outcome_locator'):
        if not isinstance(review.get(field), str) or not review[field].strip():
            reasons.append('missing_' + field)
    for field in ('original_item_match', 'answer_check', 'curriculum_mapping'):
        if review.get(field) != 'passed':
            reasons.append('unverified_' + field)
    if review.get('unresolved_issues'):
        reasons.append('unresolved_source_or_answer_issue')
    return {'eligible': not reasons, 'reasons': reasons,
            'content_adn': identity['content_adn'],
            'scope': 'reference_anchor_eligibility_not_ministry_level_certification'}


def content_identity(question, *, subject, grade, part, shared_context=None):
    """A reproducible content ID is not a certificate of correct knowledge."""
    from dedupe_bank import q_fingerprint
    payload = [str(subject), str(grade), str(part), q_fingerprint(question), shared_context or {}]
    digest = hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True,
        separators=(',', ':')).encode()).hexdigest()
    result = dict(question)
    legacy = list(result.get('legacy_qids') or [])
    old = result.get('qid')
    new = 'ADN1_' + digest
    if old and old != new and old not in legacy:
        legacy.append(old)
    result.update(qid=new, content_adn=digest, identity_revision='sha256-exact-v1', legacy_qids=legacy)
    return result


class BoundedCache(OrderedDict):
    """Small LRU; caller serializes compound cache operations."""
    def __init__(self, max_entries):
        super().__init__()
        self.max_entries = max_entries

    def __getitem__(self, key):
        value = super().__getitem__(key)
        self.move_to_end(key)
        return value

    def get(self, key, default=None):
        return self[key] if key in self else default

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.move_to_end(key)
        while len(self) > self.max_entries:
            self.popitem(last=False)

    def popitem(self, last=True):
        # Python 3.10's OrderedDict.popitem can re-enter our __getitem__ after
        # unlinking the key. Its recency update then raises KeyError. Remove
        # explicitly through base methods so eviction never refreshes recency.
        if not self:
            raise KeyError("dictionary is empty")
        key = next(reversed(self)) if last else next(iter(self))
        value = super().__getitem__(key)
        super().__delitem__(key)
        return key, value


def iter_exam_shard(path, grade=None):
    """Support JSON object/array and XZ/GZ without materializing the JSON text.

    Questions remain independent mutable dictionaries. Repeated question text and
    option strings share storage, without changing their values or provenance.
    """
    path = Path(path)
    opener = lzma.open if path.suffix == ".xz" else gzip.open if path.suffix == ".gz" else open
    strings = {}

    def compact(value):
        if isinstance(value, str):
            # Bound the temporary intern table for unexpected/user-produced banks.
            if value in strings:
                return strings[value]
            if len(strings) < 50000:
                strings[value] = value
            return value
        if isinstance(value, list):
            for i, item in enumerate(value):
                value[i] = compact(item)
        elif isinstance(value, dict):
            return {compact(key): compact(item) for key, item in value.items()}
        return value

    with opener(path, "rb") as stream:
        first = stream.read(1)
        while first and first.isspace():
            first = stream.read(1)
        if first not in (b"{", b"["):
            raise ValueError("Exam bank must be a JSON object or array")
        stream.seek(0)
        prefix = "exams.item" if first == b"{" else "item"
        for exam in ijson.items(stream, prefix, use_float=True):
            if grade is not None and str(exam.get('grade')) != str(grade):
                continue
            yield compact(exam)


def read_exam_shard(path, grade=None):
    """Compatibility list API; streaming consumers should use iter_exam_shard."""
    return list(iter_exam_shard(path, grade=grade))


def save_exam_cache_snapshot(directory, record):
    """Keep distinct payloads even when generated exam codes collide.

    Publish a complete file without replacing an existing cache or source file.
    Timestamps do not affect content identity, so repeated saves are idempotent.
    """
    import os
    import tempfile
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    identity = {key: value for key, value in record.items() if key != 'saved_at'}
    stable = json.dumps(identity, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    digest = hashlib.sha256(stable.encode('utf-8')).hexdigest()
    target = directory / ('exam_' + digest + '.json')
    handle, temporary = tempfile.mkstemp(prefix='.exam-', suffix='.tmp', dir=directory)
    try:
        with os.fdopen(handle, 'w', encoding='utf-8') as stream:
            json.dump(record, stream, ensure_ascii=False, indent=2)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, target)
        except FileExistsError:
            existing = json.loads(target.read_text(encoding='utf-8'))
            if {k: v for k, v in existing.items() if k != 'saved_at'} != identity:
                raise ValueError('Conflicting cache snapshot; no overwrite performed')
        return str(target)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def read_curated_exam_packs(directory, *, subject, grade=None):
    """Load only hash-bound, explicitly released CT2018 Station3 supplements.

    A manifest permits loading source records, not whole-paper semantic approval.
    Source holds remain in the returned dictionaries for the delivery gates.
    """
    directory = Path(directory)
    result = []
    for receipt in sorted(directory.glob('*.manifest.json')):
        manifest = json.loads(receipt.read_text(encoding='utf-8'))
        if manifest.get('subject') != subject or (grade is not None and
                str(manifest.get('grade')) != str(grade)):
            continue
        if (manifest.get('schema_version') != 1 or manifest.get('station') != 3
                or manifest.get('curriculum') != 'CT2018'
                or manifest.get('runtime_import_allowed') is not True):
            continue
        filename = manifest.get('filename', '')
        if not isinstance(filename, str) or Path(filename).name != filename or not filename.endswith('.json.xz'):
            raise ValueError('Invalid curated shard filename')
        path = directory / filename
        digest = hashlib.sha256()
        with path.open('rb') as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                digest.update(chunk)
        if digest.hexdigest() != manifest.get('archive_sha256'):
            raise ValueError('Curated shard checksum mismatch')
        rows = read_exam_shard(path, grade=grade)
        if any(row.get('subject') != subject or row.get('curriculum') != 'CT2018'
               or str(row.get('grade')) != str(manifest.get('grade'))
               or str(row.get('year')) != str(manifest.get('year'))
               or str(row.get('code')) != str(manifest.get('variant')) for row in rows):
            raise ValueError('Curated shard context mismatch')
        result.extend(rows)
    return result


def append_exam_atomic(path, exam):
    """Idempotent exact import; reject conflicting identity and concurrent writes."""
    import os
    import tempfile
    path = Path(path)
    before = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
    rows = list(iter_exam_shard(path)) if path.exists() else []
    fields = ('subject', 'grade', 'year', 'code', 'school', 'exam_type')
    identity = lambda row: tuple(str(row.get(k, '')) for k in fields)
    def payload(row):
        return {k: v for k, v in row.items() if k != 'added_at'}
    for row in rows:
        if identity(row) == identity(exam):
            if payload(row) == payload(exam):
                return False
            raise ValueError('Conflicting existing exam identity; review before replacement')
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(prefix=path.name + '.', suffix='.tmp', dir=path.parent)
    os.close(handle)
    try:
        with lzma.open(temporary, 'wt', encoding='utf-8', preset=6) as stream:
            json.dump({'exams': [exam] + rows, 'total': len(rows) + 1}, stream, ensure_ascii=False)
        current = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
        if current != before:
            raise RuntimeError('Shard changed during import; no overwrite performed')
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return True


def exam_storage_identity(exam):
    """Compare content and source context, never the printed code alone."""
    if isinstance(exam.get('data'), dict):
        exam = {**{k: exam[k] for k in ('subject', 'grade', 'code') if k in exam}, **exam['data']}
    # Keep every scientific/context/source field, including unfamiliar extensions.
    # Only storage timestamps may differ without creating another revision.
    payload = {key: value for key, value in exam.items()
               if key not in ('saved_at', 'uploaded_at', 'added_at')}
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True,
                                    separators=(',', ':')).encode('utf-8')).hexdigest()


def unique_exam_records(exams):
    seen = set()
    result = []
    for exam in exams:
        identity = exam_storage_identity(exam)
        if identity not in seen:
            result.append(exam)
            seen.add(identity)
    return result


def read_exam_cache_records(directory, subject, grade):
    """Read both legacy names and content-addressed snapshots by metadata."""
    from services.academic_context import canonical_subject
    result = []
    for path in sorted(Path(directory).glob('*.json')):
        try:
            record = json.loads(path.read_text(encoding='utf-8'))
            if (isinstance(record, dict) and isinstance(record.get('data'), dict)
                    and canonical_subject(record.get('subject', '')) == canonical_subject(subject)
                    and (grade is None or str(record.get('grade')) == str(grade))):
                result.append(record)
        except (ValueError, OSError):
            continue
    return result
