"""Independent review sidecars; never feed bank questions into Station1."""
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from services.academic_context import academic_context
from services.cognitive_levels import assessment_content_hash, validate_cognitive_review

REGISTRY = Path(__file__).resolve().parents[1] / 'data/cognitive_reviews.json'


def review_binding(question, shared_context=None):
    clean = {k: v for k, v in question.items() if k not in ('cognitive_audit', 'level_claimed')}
    return {'question': clean, 'shared_context': shared_context or {}}


def _load_reviews(registry_path=None):
    try:
        payload = json.loads(Path(registry_path or REGISTRY).read_text(encoding='utf-8'))
        if payload.get('schema_version') != 1 or not isinstance(payload.get('reviews'), dict):
            return {}
        return payload['reviews']
    except (OSError, ValueError, TypeError, AttributeError):
        return {}


def _source_review_held(question, shared_context):
    contexts = [question]
    shared = shared_context
    while isinstance(shared, dict):
        contexts.append(shared)
        for key in ('question', 'reading'):
            if isinstance(shared.get(key), dict):
                contexts.append(shared[key])
        shared = shared.get('shared_context')
    return any(context.get('source_review_issues') for context in contexts)


def independent_question_audit(question, *, subject, grade, topic, purpose,
                               shared_context=None, as_of=None, registry_path=None, _reviews=None):
    subject, grade = academic_context(subject, grade)
    today = as_of or datetime.now(timezone(timedelta(hours=7))).date().isoformat()
    bound = review_binding(question, shared_context)
    digest = assessment_content_hash(bound)
    reviews = _load_reviews(registry_path) if _reviews is None else _reviews
    review = reviews.get(digest, {})
    if not isinstance(review, dict):
        review = {}
    outcome_grade = review.get('grade')
    mapped = question.get('mapped_outcome_grades')
    if not isinstance(mapped, list) and isinstance(shared_context, dict):
        parent = shared_context.get('question')
        mapped = parent.get('mapped_outcome_grades') if isinstance(parent, dict) else None
    # Preserve the curriculum grade; explicit independent evidence may justify
    # using an earlier-grade prerequisite in a later-grade assessment.
    prerequisite = (type(outcome_grade) is int and outcome_grade < grade
        and review.get('assessment_grade') == grade
        and review.get('outcome_grade') == outcome_grade
        and isinstance(mapped, list) and outcome_grade in mapped
        and isinstance(review.get('prerequisite_use_reason'), str)
        and bool(review['prerequisite_use_reason'].strip())
        and bool(shared_context))
    result = validate_cognitive_review(bound, review, subject=subject,
                                       grade=outcome_grade if prerequisite else grade,
                                       topic=str(topic or ''), as_of=today)
    if 'assessment_grade' in review and review['assessment_grade'] != grade:
        result = dict(result, verified=False, status='blocked', reviewed_level='',
                      issues=sorted(set(result['issues'] + ['assessment_grade_mismatch'])))
    if review.get('assessment_purpose') != purpose:
        result = dict(result, verified=False, status='blocked', reviewed_level='',
                      issues=sorted(set(result['issues'] + ['review_purpose_mismatch'])))
    source_held = _source_review_held(question, shared_context)
    if source_held:
        result = dict(result, verified=False, status='blocked', reviewed_level='',
                      issues=sorted(set(result['issues'] + ['unresolved_source_review_hold'])))
    return dict(result, content_sha256=digest, assessment_grade=grade,
                mapped_outcome_grade=outcome_grade,
                curriculum_relationship='explicit_prerequisite' if prerequisite else 'same_grade_or_unverified',
                approval_scope='Independent record validity only; not Ministry certification',
                delivery_status=('held_source_issue' if source_held else
                    'review_record_valid' if result['verified'] else 'needs_teacher_review'))


def independent_exam_audit(exam, subject, grade, *, as_of=None, registry_path=None):
    rows = []
    reviews = _load_reviews(registry_path)
    # A question reviewed in one assessment context cannot authorize another.
    assessment_context = {key: exam[key] for key in (
        'exam_type', 'assessment_purpose', 'exam_session', 'curriculum',
        'textbook', 'textbook_series') if key in exam}
    groups = [(p, exam.get(p, [])) for p in ('p1', 'p2', 'p3', 'part_viet')]
    reading = exam.get('part_doc_hieu')
    if isinstance(reading, (dict, list)):
        groups.append(('part_doc_hieu', reading.get('questions', []) if isinstance(reading, dict) else reading))
    for part, questions in groups:
        if not isinstance(questions, list):
            continue
        for index, question in enumerate(questions):
            if not isinstance(question, dict):
                continue
            shared = {'assessment_context': assessment_context} if assessment_context else {}
            if part == 'part_doc_hieu':
                shared['reading'] = reading
            kwargs = dict(subject=subject, grade=grade, topic=question.get('topic', exam.get('topic', '')),
                          purpose='station3_assessment', as_of=as_of, _reviews=reviews)
            statements = question.get('stmts', [])
            is_container = (isinstance(statements, list) and bool(statements)
                            and all(isinstance(statement, dict) for statement in statements))
            if is_container:
                rows.append(dict(part=part, question=index + 1, record_role='statement_container',
                    content_sha256=assessment_content_hash(review_binding(question, shared)),
                    status='context_bound_only', verified=False, issues=[],
                    approval_scope='Shared context binding only; no aggregate cognitive level or question approval'))
            else:
                rows.append(dict(part=part, question=index + 1, record_role='response_unit',
                                 **independent_question_audit(question, shared_context=shared, **kwargs)))
            for si, statement in enumerate(statements or []):
                if isinstance(statement, dict):
                    parent = review_binding(question, shared)
                    rows.append(dict(part=part, question=index + 1, statement=si + 1, record_role='response_unit',
                                     **independent_question_audit(statement, shared_context=parent, **kwargs)))
    units = [row for row in rows if row['record_role'] == 'response_unit']
    return {'rows': rows, 'response_units': len(units),
            'context_containers': len(rows) - len(units),
            'verified_records': sum(r['verified'] for r in units),
            'pending_records': sum(not r['verified'] for r in units),
            'held_source_records': sum(r['delivery_status'] == 'held_source_issue' for r in units),
            'needs_review_records': sum(not r['verified'] and r['delivery_status'] != 'held_source_issue' for r in units),
            'scope': 'Per-response-unit review; containers bind context without aggregate approval; no whole-exam semantic approval'}


def independent_lesson_quiz_audit(questions, subject, grade, topic, lesson, *, as_of=None,
                                  registry_path=None):
    reviews = _load_reviews(registry_path)
    return [independent_question_audit(question, subject=subject, grade=grade, topic=topic,
                purpose='station1_self_study', shared_context={'lesson': lesson},
                as_of=as_of, _reviews=reviews)
            for question in questions if isinstance(question, dict)]
