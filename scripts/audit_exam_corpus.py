"""Non-destructive, streaming inventory and conservative dedupe of existing XZ.

Never promotes a school name or a URL to verified provenance. Original shards
stay untouched. SQLite is temporary scratch, not an application DB to publish.
"""
import argparse
from collections import Counter
import hashlib
import json
import lzma
from pathlib import Path
import sqlite3
import tempfile
import unicodedata

import ijson

METADATA = {'qid', 'source', 'school', 'portal', 'exam_code', 'year', 'orig_pos',
            'orig_exam_code', 'audit_id', 'level', 'topic', 'cognitive_audit'}


def canonical(value):
    # Do NOT strip powers, braces, case, whitespace in code, punctuation or
    # diacritics. Conservative exact matches sacrifice recall for correctness.
    if isinstance(value, str):
        return unicodedata.normalize('NFC', value.replace('\r\n', '\n'))
    if isinstance(value, list):
        return [canonical(x) for x in value]
    if isinstance(value, dict):
        return {k: canonical(v) for k, v in value.items()}
    return value


def fingerprint(question, context):
    payload = {'context': context, 'question': {k: v for k, v in question.items() if k not in METADATA}}
    return hashlib.sha256(json.dumps(canonical(payload), ensure_ascii=False,
        sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def questions(exam):
    for part in ('p1', 'p2', 'p3', 'part_viet', 'part_doc_hieu'):
        group = exam.get(part, [])
        shared = {}
        if isinstance(group, dict):
            shared = {k: v for k, v in group.items() if k != 'questions'}
            group = group.get('questions', [])
        if isinstance(group, list):
            for pos, q in enumerate(group, 1):
                if isinstance(q, dict):
                    yield part, pos, q, shared


def audit(paths, report_path):
    totals, coverage, files = Counter(), Counter(), []
    with tempfile.TemporaryDirectory(prefix='gsai-corpus-audit-') as scratch:
        db = sqlite3.connect(str(Path(scratch) / 'index.sqlite'))
        db.execute('CREATE TABLE seen (hash TEXT PRIMARY KEY, first_file TEXT, first_exam TEXT)')
        db.execute('CREATE TABLE identity (qid TEXT, hash TEXT, PRIMARY KEY(qid, hash))')
        for path in paths:
            counts = Counter()
            with lzma.open(path, 'rb') as stream:
                first = stream.read(1)
                stream.seek(0)
                if first not in (b'{', b'['):
                    raise ValueError('Invalid JSON root: ' + str(path))
                for exam in ijson.items(stream, 'exams.item' if first == b'{' else 'item', use_float=True):
                    counts['exams'] += 1
                    subject, grade = str(exam.get('subject', '')), str(exam.get('grade', ''))
                    coverage[(subject, grade, str(exam.get('year', '')))] += 1
                    if exam.get('is_blended_real'):
                        counts['blended_exam_claims_require_review'] += 1
                    if not exam.get('url') and not exam.get('pdf_url'):
                        counts['exams_without_source_url'] += 1
                    for part, pos, q, shared in questions(exam):
                        counts['questions'] += 1
                        key = fingerprint(q, {'subject': subject, 'grade': grade, 'part': part, 'shared': shared})
                        qid = q.get('qid')
                        if qid:
                            db.execute('INSERT OR IGNORE INTO identity VALUES (?,?)', (str(qid), key))
                        else:
                            counts['questions_without_qid'] += 1
                        changed = db.execute('INSERT OR IGNORE INTO seen VALUES (?,?,?)',
                            (key, path.name, str(exam.get('code', '')))).rowcount
                        counts['unique_exact' if changed else 'duplicate_exact_occurrences'] += 1
            db.commit()
            totals.update(counts)
            files.append({'file': path.name, 'compressed_bytes': path.stat().st_size, **counts})
        identity = {'legacy_ids_with_multiple_content_hashes': db.execute(
            'SELECT COUNT(*) FROM (SELECT qid FROM identity GROUP BY qid HAVING COUNT(*)>1)').fetchone()[0],
            'distinct_legacy_ids': db.execute('SELECT COUNT(DISTINCT qid) FROM identity').fetchone()[0]}
        db.close()
    report = {'schema': 1, 'mode': 'non_destructive_inventory_not_knowledge_acceptance',
        'exact_policy': 'NFC only; preserve math/code/options order/answers/visuals/shared passage; cross-grade kept separate',
        'source_status': 'Existing labels and URLs NOT independently verified by this audit',
        'totals': dict(totals), 'identity_audit': identity, 'files': files,
        'coverage': [{'subject': s, 'grade': g, 'year': y, 'exam_occurrences': n}
                     for (s, g, y), n in sorted(coverage.items())]}
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bank-dir', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    result = audit(sorted(args.bank_dir.glob('*.json.xz')), args.report)
    print(json.dumps(result['totals']))
