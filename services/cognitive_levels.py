"""Audit claimed cognitive demand; format/position is never evidence of a level."""
from collections import Counter
from copy import deepcopy
import hashlib
import json
from datetime import date

from services.academic_context import folded

LEVELS = {
    "nb": "NB", "biet": "NB", "nhan biet": "NB",
    "th": "TH", "hieu": "TH", "thong hieu": "TH",
    "vd": "VD", "van dung": "VD",
    "vdc": "VDC", "van dung cao": "VDC",
}
LEVEL_GUIDANCE = """
MỨC ĐỘ NHẬN THỨC — PHẢI CÓ CĂN CỨ:
QUY TRÌNH BẮT BUỘC TRƯỚC KHI TRẢ BÀI HỌC/CÂU HỎI (áp dụng mọi môn, mọi lớp):
1. Khóa phạm vi môn/lớp/chủ đề/yêu cầu cần đạt và nguồn áp dụng trước khi soạn. Kiến thức tiên quyết phải được chỉ rõ; không đưa kiến thức ngoài phạm vi thành yêu cầu bắt buộc. Khi yêu cầu người dùng mâu thuẫn chuẩn hoặc thiếu nguồn, nêu giới hạn trong trường giải thích sẵn có; không bịa căn cứ để hợp thức hóa.
2. Kiểm từng khẳng định, ví dụ, ngữ liệu và dữ kiện: đúng bản chất, phù hợp lứa tuổi; ghi đúng tác giả/tác phẩm/trích dẫn nếu có. Không có hình/bảng/đoạn đọc thì không đặt câu buộc học sinh đọc tài liệu đó. Không lấy số liệu minh họa tự tạo làm dữ kiện thực nghiệm hoặc nguồn chính thức.
3. Kiểm tính giải được và đáp án: giả thiết đủ, không mâu thuẫn; miền xác định, điều kiện, đơn vị, dấu, quy tắc làm tròn nhất quán nếu liên quan. Trắc nghiệm một lựa chọn phải có đúng một đáp án đúng và phương án phân biệt; từng ý Đúng/Sai phải có căn cứ riêng. Tự luận/đọc hiểu phải có rubric và chấp nhận cách giải hoặc diễn giải khác có căn cứ, không ép một đáp án chữ nghĩa duy nhất.
4. Đối chiếu đáp án với chính câu hỏi, sau đó đối chiếu mức độ với yêu cầu cần đạt và nhiệm vụ thực tế. Cung cấp lời giải/rubric ngắn gọn có thể kiểm chứng và các thao tác tư duy chính trong trường quy định; không dùng nhãn mức độ hay lời tự khen làm bằng chứng. Gợi ý phải giúp định hướng, không tiết lộ đáp án.
5. Sửa mâu thuẫn phát hiện được trước khi trả trong cùng lần sinh; không thêm câu lỗi để đủ số lượng hoặc tỷ lệ. Nếu không thể hoàn thiện, giữ đúng định dạng đầu ra, nêu phần chưa đáp ứng trong trường giải thích, để mức chưa đủ căn cứ rỗng; không giả vờ đã hoàn thành. Không tự yêu cầu gọi AI lại hoặc tăng số lần thử. Kết quả chỉ là bản đề xuất chờ bộ thẩm định độc lập.
- Khi sinh câu, bám yêu cầu cần đạt CT2018 của đúng môn/lớp và trục bài KNTT; chỉ dùng căn cứ văn bản/nguồn đã cung cấp và còn áp dụng trong phạm vi đó. Không bịa mã yêu cầu cần đạt, trang sách hoặc tình trạng hiệu lực để lấp chỗ thiếu. Ngữ liệu bổ sung phải ghi rõ vai trò và nguồn, không gán thành nguyên văn KNTT.
- Trước khi trả câu, tự giải, kiểm đáp án và đối chiếu thao tác tư duy với mức đề xuất; nếu chưa đủ căn cứ phải để mức rỗng và nêu phần thiếu. Việc tự kiểm này chỉ hỗ trợ chất lượng đầu vào: mọi câu vẫn phải qua bộ thẩm định độc lập sau sinh, không tự cấp trạng thái đã duyệt hoặc dùng chính nhãn AI làm bằng chứng xác nhận.
- Tham chiếu phụ lục CV 7991: Biết, Hiểu, Vận dụng trong từng dạng câu. Phạm vi kiểm tra định kì thực hiện theo hướng dẫn Sở/nhà trường; không áp cứng cho mọi bài luyện tập hoặc đề tốt nghiệp.
- NB: nhận ra/nhớ lại tri thức, khái niệm, dữ kiện đã học. TH: giải thích, diễn giải, phân loại hoặc liên hệ ý nghĩa trong nội dung đã học. VD: lựa chọn và sử dụng kiến thức/kĩ năng để giải quyết nhiệm vụ. Đối chiếu yêu cầu cần đạt của đúng môn/lớp, không chỉ nhìn động từ.
- VDC là nhãn phân hóa mở rộng trong app; khi đối chiếu khung ba mức có thể xếp trong VD, không tự tuyên bố Bộ bắt buộc một cột VDC riêng.
- Không suy NB từ trắc nghiệm, TH từ Đúng/Sai, VD/VDC từ trả lời ngắn; không suy từ số phép tính, độ dài, số liệu lớn hay thứ tự câu. Một câu Đúng/Sai cần căn cứ riêng cho từng ý.
- Mỗi câu/ý phải khai báo level (NB/TH/VD/VDC), learning_outcome (yêu cầu cần đạt, không bịa mã/trang), cognitive_rationale (vì sao nhiệm vụ cần mức đó), solution_steps (các thao tác tư duy để giải). Nêu rõ điều gì đã cho và điều gì học sinh phải tự chọn/suy luận. Nếu chưa đủ căn cứ thì để level rỗng; không đổi nhãn để đủ tỷ lệ.
- Đây là đề xuất của AI, chưa phải kết quả thẩm định. Tỷ lệ theo điểm phải có ma trận và bản đặc tả được giáo viên duyệt; không đồng nhất tỷ lệ số câu với tỷ lệ điểm. Mức độ nhận thức khác độ khó thống kê đo sau khi học sinh làm bài.
"""


def normalize_level(value):
    return LEVELS.get(folded(str(value or "")).strip(), "")


def assessment_content_hash(question):
    """Bind a review to the entire task, answer, rubric and evidence fields."""
    content = {k: v for k, v in question.items()
               if k not in ('cognitive_audit', 'level_claimed')}
    return hashlib.sha256(json.dumps(content, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def validate_reference_item(item, *, subject, grade, outcome_id):
    """School/department exams are reference evidence, not national law.

    In particular an entrance-to-grade-10 paper is not grade-10 curriculum.
    Use the independently mapped outcome/grade, not the title of the exam.
    """
    issues = []
    if not isinstance(item, dict):
        item = {}
    if item.get('issuer_type') not in ('ministry', 'department', 'school'):
        issues.append('unknown_issuer')
    for field in ('issuer', 'source_url', 'school_year', 'exam_type',
                  'paper_sha256', 'answer_sha256', 'source_locator'):
        if not isinstance(item.get(field), str) or not item[field].strip():
            issues.append('missing_' + field)
    if item.get('curriculum') != 'CT2018':
        issues.append('wrong_or_unverified_curriculum')
    grades = item.get('mapped_grades')
    outcomes = item.get('mapped_outcomes')
    if item.get('subject') != subject or not isinstance(grades, list) or grade not in grades:
        issues.append('context_mismatch')
    if not isinstance(outcomes, list) or outcome_id not in outcomes or not outcome_id:
        issues.append('outcome_not_mapped')
    if item.get('independent_answer_check') != 'passed':
        issues.append('answer_not_independently_checked')
    if item.get('known_error'):
        issues.append('source_has_unresolved_error')
    return {'eligible': not issues, 'issues': sorted(set(issues)),
            'role': 'comparison_reference_not_legal_authority',
            'official_level_claim': item.get('published_level', '')
                if item.get('published_level_locator') else ''}


def validate_cognitive_review(question, review, *, subject, grade, topic, as_of):
    """Validate an independently maintained review, never AI's self approval.

    Caller must obtain review from the local reviewed registry, not the generated
    question. Passing this gate checks provenance/completeness, not all subject
    knowledge. A changed solution/rubric requires a new review.
    """
    issues = []
    try:
        today = date.fromisoformat(as_of)
    except (ValueError, TypeError):
        return {'status': 'blocked', 'verified': False, 'issues': ['invalid_evaluation_date']}
    if not isinstance(review, dict):
        review = {}
    try:
        if date.fromisoformat(review['recheck_after']) < today:
            issues.append('review_due_for_recheck')
    except (KeyError, ValueError, TypeError):
        issues.append('missing_review_recheck_date')
    if (review.get('subject'), review.get('grade'), review.get('topic')) != (subject, grade, topic):
        issues.append('context_mismatch')
    if review.get('content_sha256') != assessment_content_hash(question):
        issues.append('content_changed_or_unreviewed')
    level = normalize_level(review.get('reviewed_level'))
    if not level:
        issues.append('missing_reviewed_level')
    for field in ('reviewer', 'learning_outcome', 'solution_rubric', 'cognitive_reason'):
        if not isinstance(review.get(field), str) or not review[field].strip():
            issues.append('missing_' + field)
    operations = review.get('cognitive_operations')
    if not isinstance(operations, list) or not operations or not all(isinstance(s, str) and s.strip() for s in operations):
        issues.append('missing_cognitive_operations')
    for field in ('curriculum_source', 'textbook_source'):
        source = review.get(field)
        if not isinstance(source, dict) or not all(source.get(k) for k in ('url', 'locator', 'read_on')):
            issues.append('missing_' + field)
        else:
            if source.get('document_status') != 'final':
                issues.append('non_final_or_unverified_' + field)
            # A catalog/contents locator establishes where a lesson is, not
            # that its requirements or actual rule text have been reviewed.
            if source.get('read_scope') != 'relevant_content':
                issues.append('relevant_content_not_read_' + field)
            try:
                if date.fromisoformat(source['read_on']) > today:
                    issues.append('invalid_' + field + '_read_date')
            except (ValueError, TypeError):
                issues.append('invalid_' + field + '_read_date')
    legal = review.get('legal_basis')
    if not isinstance(legal, list) or not legal:
        issues.append('missing_legal_basis')
    else:
        for document in legal:
            try:
                if not all(document.get(k) for k in ('code', 'url', 'locator', 'checked_on')):
                    raise ValueError()
                start = date.fromisoformat(document['effective_from'])
                end = date.fromisoformat(document['effective_until']) if document.get('effective_until') else None
                checked = date.fromisoformat(document['checked_on'])
                if start > today or (end and today >= end) or checked > today:
                    raise ValueError()
                # Review must explicitly state the applicable purpose; periodic
                # assessment guidance is not a universal graduation-exam rule.
                if document.get('applicable_purpose') != review.get('assessment_purpose') or not review.get('assessment_purpose'):
                    raise ValueError()
            except (ValueError, KeyError, TypeError, AttributeError):
                issues.append('invalid_or_inapplicable_legal_basis')
    if level == 'VDC' and not str(review.get('advanced_transfer_reason') or '').strip():
        issues.append('missing_advanced_transfer_reason')
    return {'status': 'review_record_valid' if not issues else 'blocked',
            'verified': not issues, 'issues': sorted(set(issues)),
            'reviewed_level': level if not issues else '',
            'reference_bucket': {'NB': 'Biết', 'TH': 'Hiểu', 'VD': 'Vận dụng', 'VDC': 'Vận dụng'}.get(level, ''),
            'scope': 'independent_review_record_validation_not_ministry_certification'}


def annotate_question(question):
    """Retain the source claim, never grant approval based on self-authored fields."""
    result = dict(question)
    claimed = result.get("level_claimed", result.get("level", ""))
    result["level_claimed"] = claimed
    result["level"] = normalize_level(claimed)
    steps = result.get("solution_steps")
    evidence_present = (bool(str(result.get("learning_outcome") or "").strip())
                        and bool(str(result.get("cognitive_rationale") or "").strip())
                        and isinstance(steps, list) and bool(steps)
                        and all(isinstance(s, str) and s.strip() for s in steps))
    result["cognitive_audit"] = {
        "level": result["level"],
        "reference_bucket": {"NB": "Biết", "TH": "Hiểu", "VD": "Vận dụng", "VDC": "Vận dụng"}.get(result["level"], "Chưa xác định"),
        "status": "needs_teacher_review", "verified": False,
        "self_reported_evidence_present": evidence_present,
        "issue": "missing_or_ambiguous_level" if not result["level"] else "unreviewed_claim",
        "content_sha256": assessment_content_hash(question),
    }
    if isinstance(result.get("stmts"), list):
        result["stmts"] = [annotate_question(s) if isinstance(s, dict) else s for s in result["stmts"]]
    return result


def audit_exam_levels(exam):
    """Separate question/statement counts. No invented score percentages or labels."""
    result = deepcopy(exam)
    rows, question_counts, statement_counts = [], Counter(), Counter()
    groups = [(part, result.get(part, [])) for part in ("p1", "p2", "p3", "part_viet")]
    reading = result.get("part_doc_hieu")
    groups.append(("part_doc_hieu", reading.get("questions", []) if isinstance(reading, dict) else reading or []))
    for part, questions in groups:
        if not isinstance(questions, list):
            continue
        for i, question in enumerate(questions):
            if not isinstance(question, dict):
                continue
            q = annotate_question(question)
            # The delivery audit is sidecar metadata; leave source questions/answers intact.
            question_counts[q["level"] or "UNSPECIFIED"] += 1
            rows.append({"part": part, "question": i + 1, "claim": q["level_claimed"], **q["cognitive_audit"]})
            for j, stmt in enumerate(q.get("stmts", [])):
                if isinstance(stmt, dict):
                    statement_counts[stmt["level"] or "UNSPECIFIED"] += 1
                    rows.append({"part": part, "question": i + 1, "statement": j + 1,
                                 "claim": stmt["level_claimed"], **stmt["cognitive_audit"]})
    result["cognitive_audit"] = {"verified": False, "status": "needs_teacher_review",
        "question_claim_counts": dict(question_counts), "statement_claim_counts": dict(statement_counts),
        "point_matrix_status": "not_computed_without_teacher_point_allocation", "rows": rows,
        "note": "Thống kê nhãn khai báo, không chứng nhận mức độ. VDC là phân hóa mở rộng trong VD khi đối chiếu ba mức. Cần duyệt nội dung, yêu cầu cần đạt, lời giải và phân bổ điểm."}
    return result


def level_caption(question, independent_audit=None):
    audit = independent_audit if isinstance(independent_audit, dict) else {}
    reviewed = normalize_level(audit.get("reviewed_level"))
    if (audit.get("verified") is True and audit.get("delivery_status") == "review_record_valid"
            and reviewed and not audit.get("issues")):
        return f"{reviewed} — đã thẩm định trong hệ thống"
    level = normalize_level(question.get("level"))
    return f"{level} — nhãn đề xuất, chưa duyệt" if level else "Chưa xác định mức độ"
