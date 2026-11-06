"""Deliver a reviewed original paper without mixing, recovery or key rewriting.

Original-paper authorization does not authorize unrestricted question reuse or
certify application-assigned cognitive levels as Ministry classifications.
"""
from copy import deepcopy
import json
from pathlib import Path

from services.bank_storage import read_curated_exam_packs
from services.curriculum_policy import prepare_exam_for_delivery

PACKS = Path(__file__).resolve().parents[1] / 'data/curated_exam_sources'
PATHWAYS = {'CS': 'CS', 'ICT': 'ICT', 'Khoa học máy tính': 'CS', 'Tin học ứng dụng': 'ICT'}
# Exact reviewed source bundle, not a general bypass for arbitrary held items.
TIN0530_SHA = '685700c87d4fcf11e30516e1a0567c6cc56a92c9e6660258eae65f597786bc0e'
REUSE_NOTES = {
    'I.7': {'CSS_display_scope_not_unique_without_taught_subset'},
    'II.3': {'requires_explicit_CS_pathway_routing'},
    'II.4': {'requires_explicit_CS_pathway_routing', 'II.4.a_specialized_study_not_ordinary_core'},
    'II.5': {'requires_explicit_ICT_pathway_routing'},
    'II.6': {'requires_explicit_ICT_pathway_routing'},
}


def original_tin0530(pathway, *, directory=None):
    track = PATHWAYS.get(pathway)
    if track is None:
        raise ValueError('Chọn định hướng Khoa học máy tính hoặc Tin học ứng dụng trước khi mở đề gốc.')
    directory = Path(directory or PACKS)
    manifest = json.loads((directory / 'tin_2025_0530.manifest.json').read_text(encoding='utf8'))
    if manifest.get('archive_sha256') != TIN0530_SHA:
        raise ValueError('Bản nguồn đã thay đổi; cần kiểm lại đề và khóa chính thức.')
    rows = read_curated_exam_packs(directory, subject='Tin học', grade=12)
    matches = [e for e in rows if e.get('year') == 2025 and e.get('code') == '0530']
    if len(matches) != 1:
        raise ValueError('Không xác định duy nhất đề gốc 0530 năm 2025.')
    exam = deepcopy(matches[0])
    if exam.get('source_review_issues') or len(exam['p1']) != 24 or len(exam['p2']) != 6 or exam.get('p3'):
        raise ValueError('Đề gốc không đủ cấu trúc đã đối chiếu.')
    expected_mcq = 'BAADDABCBDAABADDCCDDBDBC'
    expected_tf = ['DDDS', 'DSDS', 'DSSD', 'SDSD', 'SSDD', 'DDSS']
    if ''.join(q.get('ans', '') for q in exam['p1']) != expected_mcq:
        raise ValueError('Khóa trắc nghiệm không khớp bản Bộ đã đối chiếu.')
    for index, question in enumerate(exam['p2']):
        statements = question.get('stmts', [])
        if len(statements) != 4 or any(type(s.get('a')) is not bool for s in statements):
            raise ValueError('Thiếu khóa đúng/sai của đề gốc.')
        if ''.join('D' if s['a'] else 'S' for s in statements) != expected_tf[index]:
            raise ValueError('Khóa đúng/sai không khớp bản Bộ đã đối chiếu.')
    for part in ('p1', 'p2'):
        for question in exam[part]:
            sid = question.get('source_id')
            question.update(is_real_bank_question=True, school=exam['school'],
                            year=2025, portal='tuoitre.vn',
                            exam_session=exam['exam_session'], orig_exam_code='0530',
                            orig_pos=sid, source='Tin học THPT2025 mã0530 — ' + sid
                            + '; ảnh đề Tuổi Trẻ đăng lại; khóa Bộ do Cổng Chính phủ đăng lại')
            issues = set(question.get('source_review_issues', []))
            if issues != REUSE_NOTES.get(sid, set()):
                raise ValueError('Có vấn đề nguồn mới chưa được xử lý cho đề gốc.')
            # Preserve reuse restrictions as notes; only this exact original
            # paper context is authorized. The archive/mixed pool stay held.
            if issues:
                question['app_reuse_review_issues'] = question.pop('source_review_issues')
            if any(s.get('source_review_issues') for s in question.get('stmts', [])):
                raise ValueError('Có ý đúng/sai đang chặn nguồn.')
    selected_ids = {'II.1', 'II.2', 'II.3', 'II.4'} if track == 'CS' else {'II.1', 'II.2', 'II.5', 'II.6'}
    exam['p2'] = [q for q in exam['p2'] if q['source_id'] in selected_ids]
    if len(exam['p2']) != 4:
        raise ValueError('Không đủ phần chung và phần lựa chọn.')
    exam.update(duration=50, pathway=track, delivery_mode='original_official_paper',
                title='Đề Tin học tốt nghiệp THPT 2025 — mã 0530 — ' + track,
                original_source_archive_sha256=TIN0530_SHA,
                original_question_numbers_preserved=True)
    solutions = json.loads((directory / 'tin_2025_0530.solutions.json').read_text(encoding='utf8'))
    from services.reviewed_solutions import apply_reviewed_solutions
    exam = apply_reviewed_solutions(exam, solutions, TIN0530_SHA)
    result = prepare_exam_for_delivery(exam, 'Tin học', 12, duration=50)
    return result


def original_question_number(exam, question, fallback):
    """Retain source numbering while answer widgets keep zero-based positions."""
    if exam.get('delivery_mode') != 'original_official_paper':
        return fallback
    source_id = str(question.get('source_id', ''))
    number = source_id.rsplit('.', 1)[-1]
    return int(number) if number.isdigit() else fallback


def original_print_context(exam):
    if exam.get('delivery_mode') != 'original_official_paper':
        return None
    if (exam.get('original_source_archive_sha256') != TIN0530_SHA
            or exam.get('year') != 2025 or exam.get('code') != '0530'
            or exam.get('pathway') not in ('CS', 'ICT')):
        raise ValueError('Không xác định đúng nguồn đề gốc để xuất bản.')
    track = exam['pathway']
    return {
        'title': 'ĐỀ THI TỐT NGHIỆP THPT NĂM 2025 — MÔN TIN HỌC — MÃ 0530',
        'track': 'Khoa học máy tính (CS)' if track == 'CS' else 'Tin học ứng dụng (ICT)',
        'duration': 50,
        'note': 'Bản chép lại, định dạng cho luyện tập; không phải bản PDF gốc. '
                'Ảnh đề do Tuổi Trẻ đăng lại; khóa đáp án Bộ GDĐT do Cổng Chính phủ đăng lại. '
                'Giữ số câu theo đề nguồn; chỉ gồm phần chung và định hướng đã chọn.'
    }
