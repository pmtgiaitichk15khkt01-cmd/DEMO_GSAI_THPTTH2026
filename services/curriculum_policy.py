"""Versioned references and conservative checks, not an academic certification."""
from copy import deepcopy
from datetime import date, datetime, timedelta, timezone
import hashlib
import html
import json
import re
from pathlib import Path

from services.academic_context import academic_context, canonical_subject, folded, normalize_grade, validate_exam_context
from qa_runtime import normalize_bool

POLICY_DATE = "2026-10-24"
T1_CONTEXT_REVISION = 2026110602
REGISTRY = Path(__file__).resolve().parents[1] / "data/legal_references.json"


def label_declared_paraphrases(text):
    """A self-declared paraphrase is not an authenticated textbook quotation.

    Applies to every subject; never rewrites verified quotations or code.
    It labels provenance only and does not certify the paraphrase's facts.
    """
    from services.text_boundaries import preserve_math_and_code
    return preserve_math_and_code(str(text), lambda prose: re.sub(
        r'Ngữ liệu tham khảo\s*\(trích tinh thần[^\n]*?\)\s*:',
        'Đoạn diễn ý minh họa do AI biên soạn (không phải trích dẫn nguyên văn SGK):',
        prose, flags=re.I))


def correct_reviewed_english_family_guidance(text, subject, grade, topic=""):
    """Apply reviewed prose repairs only to the reproduced Family Life items.

    Preserve answer order/keys and code; this is not general semantic approval.
    """
    if (canonical_subject(subject) != 'Tiếng Anh' or normalize_grade(grade) != 10
            or 'family' not in folded(topic)):
        return text
    from services.text_boundaries import preserve_math_and_code
    def repair(prose):
        prose = prose.replace(
            'In my family, my father usually __________ the heavy lifting, but today he __________ a rest.',
            'My father usually __________ the heavy lifting. Right now, he __________ a rest instead of working.')
        prose = prose.replace(
            'My sister is cleaning her room every Sunday morning.',
            'My sister is clean her room every Sunday morning.')
        prose = prose.replace('go to the market / visit her grandmother',
                              "go to the market / visit her own mother (Lan’s grandmother)")
        prose = prose.replace(
            "Today, my mother (not/go) __________ to work; she (stay) __________ at home to celebrate my sister's birthday.",
            "My mother usually goes to work in the morning. Right now, she (not/go) __________ to work; she (stay) __________ at home to celebrate my sister's birthday.")
        prose = prose.replace(
            'Cụm từ "Today" và ngữ cảnh tổ chức sinh nhật cho thấy đây là một tình huống tạm thời, khác với lịch trình làm việc thông thường, do đó ta dùng thì hiện tại tiếp diễn.',
            'Lịch làm việc thường lệ được nêu rõ, còn "Right now" xác định hành động đang diễn ra trong tình huống ngoại lệ. Vì vậy dùng is not going / is staying; riêng từ today không quyết định thì.')
        prose = prose.replace(
            'I (take) __________ out the rubbish every night, but tonight my brother (do) __________ it for me.',
            'I (take) __________ out the rubbish every night. Right now, my brother (do) __________ it for me.')
        prose = prose.replace(
            'Xác định đúng "mỗi tối" (thói quen) và "tối nay" (tình huống cụ thể) để chia động từ.',
            'Phân biệt thói quen mỗi tối với hành động người anh/em đang làm ngay lúc nói: take / is doing. Trạng từ chỉ là gợi ý; phải xét nghĩa và ngữ cảnh.')
        # Independently reviewed issues in the single authorized replacement.
        # Keep option order/keys; strengthen the intended context, not the answer.
        prose = re.sub(
            r'In my family, my father (_+) the heavy lifting, and my mother does the cooking\.',
            r"In our family's usual household routine, my father \1 the heavy lifting, and my mother does the cooking.", prose)
        prose = re.sub(
            r'"Where is your mother\?" - "She (_+) the garden\. She loves plants\."',
            r'"Where is your mother right now?" - "She \1 the garden right now. She loves plants."', prose)
        prose = re.sub(
            r'My brother usually \(wash\) (_+) the dishes, but today I \(do\) (_+) it for him\.',
            r'My brother usually (wash) \1 the dishes. Right now, I (do) \2 it for him.', prose)
        replacements = {
            'Vế sau có "today" ám chỉ một sự thay đổi tạm thời so với thói quen':
                'Vế sau nêu rõ "Right now" và việc người nói đang làm thay; riêng today không quyết định thì',
            'but / tonight / he / help': 'but / right now / he / help',
            'một hành động khác biệt xảy ra vào tối nay': 'một hành động khác biệt đang diễn ra ngay lúc nói',
            'Xác định vế sau là hành động tạm thời (tonight)': 'Xác định vế sau là hành động đang diễn ra (right now)',
            'Vế có "tonight" (diễn tả sự tạm thời/đang xảy ra)': 'Vế có "right now" (hành động đang diễn ra ngay lúc nói)',
            'mốc thời gian "tonight"': 'mốc thời gian "right now"',
            'cách dùng thì và động từ trạng thái (stative verbs)': 'cách dùng thì và cấu trúc be + tính từ',
            'lỗi dùng động từ trạng thái (tired)': 'lỗi dùng be với tính từ tired trong ngữ cảnh này',
            'tính chất của động từ trạng thái': 'cấu trúc be + tính từ trong ngữ cảnh này',
            'Với tính từ "tired" (mệt mỏi - chỉ trạng thái), chúng ta có dùng thì tiếp diễn để mô tả không?':
                'Trong ngữ cảnh này, hãy phân biệt tính từ tired với động từ và xét cách dùng be để mô tả trạng thái.',
            'Câu hỏi "Where is your mother?" cho thấy người hỏi đang tìm người mẹ ở thời điểm hiện tại. Do đó, câu trả lời phải dùng thì Hiện tại tiếp diễn để chỉ hành động đang diễn ra.':
                'Ngữ cảnh nêu right now và hành động tưới vườn đang diễn ra nên trong tình huống này dùng Hiện tại tiếp diễn. Câu hỏi Where is your mother? đứng riêng không phải quy tắc bắt buộc chọn thì.',
        }
        # Keep the reviewed stem, hint and cognitive rationale consistent.
        # These editorial repairs never grant a level or review approval.
        prose = prose.replace(
            'Học sinh cần hiểu tình huống "đang ở đâu" để suy luận ra hành động đang diễn ra.',
            'Học sinh xác định hành động đang diễn ra từ ngữ cảnh tưới vườn và mốc right now; câu hỏi nơi chốn đứng riêng không xác định thì.')
        prose = prose.replace(
            "Phân tích câu hỏi 'Where is...?' để xác định thời điểm hành động",
            'Xác định mốc right now và hành động tưới vườn đang diễn ra')
        prose = prose.replace(
            'Khi ai đó hỏi "Mẹ bạn đâu rồi?", họ muốn biết về một thói quen hàng ngày hay một hành động đang thực hiện ngay lúc đó?',
            'Trong tình huống tưới vườn có mốc right now, hành động đang diễn ra lúc nói hay là thói quen? Câu hỏi nơi chốn đứng riêng chưa đủ để chọn thì.')
        tired_context = 'my mother is being tired' in prose or 'động từ trạng thái (tired)' in prose
        for old, new in replacements.items():
            if (old.startswith(('cách dùng thì và động từ trạng thái', 'tính chất của động từ trạng thái'))
                    and not tired_context):
                continue
            prose = prose.replace(old, new)
        prose = prose.replace('**Dấu hiệu nhận biết**', '**Trạng từ gợi ý, cần xét ngữ cảnh**')
        prose = prose.replace('Tiêu chí sản phẩm:', 'Tự kiểm tra:')
        return prose
    return preserve_math_and_code(str(text), repair)


def repair_reviewed_english_family_question(question, subject, grade, topic=""):
    """Apply the same reviewed prose repairs to an already parsed live quiz.

    Keep keys, order, review decisions and the caller's original unchanged.
    """
    result = deepcopy(question)
    for field in ('question', 'explain', 'hint'):
        if isinstance(result.get(field), str):
            result[field] = correct_reviewed_english_family_guidance(
                result[field], subject, grade, topic)
    evidence = result.get('cognitive_evidence')
    if isinstance(evidence, dict):
        for field in ('learning_outcome', 'cognitive_rationale'):
            if isinstance(evidence.get(field), str):
                evidence[field] = correct_reviewed_english_family_guidance(
                    evidence[field], subject, grade, topic)
        if isinstance(evidence.get('solution_steps'), list):
            evidence['solution_steps'] = [correct_reviewed_english_family_guidance(
                step, subject, grade, topic) if isinstance(step, str) else step
                for step in evidence['solution_steps']]
    if isinstance(result.get('options'), list):
        result['options'] = [correct_reviewed_english_family_guidance(
            option, subject, grade, topic) if isinstance(option, str) else option
            for option in result['options']]
    return result


def correct_reviewed_myth_guidance(text, subject, grade, topic=""):
    """Source-reviewed corrections for the observed mythology lesson only."""
    if (canonical_subject(subject) != 'Ngữ văn' or normalize_grade(grade) != 10
            or 'than sang tao the gioi' not in folded(topic)):
        return text
    from services.text_boundaries import preserve_math_and_code
    def repair(prose):
        prose = prose.replace('SGK Ngữ thuật', 'SGK Ngữ văn')
        prose = prose.replace('các vị thần quen thuộc như thần Trời, thần Đất, thần Mưa, thần Nắng, thần Sét, thần Gió,...',
                              'ba vị thần trong nhóm văn bản đang học: thần Trụ Trời, thần Sét và thần Gió.')
        prose = re.sub(r'thần\s*\*{0,2}["“]ngẩng đầu lên đội trời lên cho khỏi đạp xuống đất["”]\*{0,2}\s*rồi đắp cột đá chống trời',
                       'thần tách trời và đất, đắp cột chống trời (diễn ý, không trích nguyên văn)', prose)
        prose = prose.replace('đội trời lên để đoạt lại đất trời từ vùng hỗn độn',
                              'tách trời và đất từ vùng hỗn độn')
        prose = prose.replace('Sắp xếp ý: Ý 1: Trân trọng trí tưởng tượng và nỗ lực lí giải thế giới của người xưa; Ý 2: Vai trò chính xác, khách quan của khoa học hiện đại; Ý 3: Kết luận về ý nghĩa của cả hai trong đời sống tinh thần và trí tuệ con người.',
                              'Em tự lựa chọn luận điểm, dẫn chứng và cách sắp xếp ý; phân biệt giá trị văn hóa của tưởng tượng thần thoại với yêu cầu bằng chứng của khoa học, rồi tự rút ra kết luận có căn cứ.')
        return prose
    return preserve_math_and_code(str(text), repair)


def correct_reviewed_proposition_guidance(text, subject, grade, topic=""):
    """Remove a reproduced answer-giving classification plan, not examples.

    Shared lesson preprocessing also supplies exports. This is a scoped content
    repair, not a claim that arbitrary hints in every subject are now verified.
    """
    if (canonical_subject(subject) != 'Toán học' or normalize_grade(grade) != 10
            or 'menh de' not in folded(topic)):
        return text
    chunks = re.split(r'(```[\s\S]*?```|~~~[\s\S]*?~~~)', str(text))
    for i in range(0, len(chunks), 2):
        chunks[i] = re.sub(
            r'(?i)Xét từng câu:\s*Câu a là khẳng định toán học về số\s*\$?15\$?;\s*'
            r'Câu b là câu cầu khiến;\s*Câu c là khẳng định về nghiệm của phương trình trên tập số thực\.',
            'Xét từng câu: Em tự nhận diện mục đích của câu, xác định câu có khẳng định điều gì '
            'và có thể xét đúng hoặc sai hay không; ghi lí do trước khi phân loại.', chunks[i])
    return ''.join(chunks)


def correct_reviewed_cubic_prior_knowledge(text, subject, grade, topic=""):
    """Correct a reproduced grade-placement error without rewriting the lesson."""
    if subject != "Toán học" or int(grade) != 12 or "bac ba" not in folded(topic):
        return text
    text = str(text).replace(
        "Nhớ lại cách tính đạo hàm và tìm cực trị của hàm số đã học ở lớp 11.",
        "Ôn lại cách tính đạo hàm đã học ở lớp 11; vận dụng dấu đạo hàm để xác định cực trị theo kiến thức lớp 12."
    ).replace(
        "phân tích sự tăng trưởng có chu kỳ của một đại lượng kinh tế trong ngắn hạn",
        "mô hình hóa sự biến động của một đại lượng kinh tế trong một khoảng thời gian khảo sát"
    )
    if 'x^3-3x+1' in re.sub(r'[\s${}\\]', '', text):
        text = re.sub(
            r'Kiểm tra lại các trường hợp\s+\$m\s*>\s*3\$\s*,\s*\$m\s*<\s*-1\$ và các giá trị biên[^\n]*?để kết luận chính xác\.',
            'Tự xác định các mức tới hạn từ bảng biến thiên, kiểm tra riêng từng mức biên rồi đối chiếu số giao điểm trên mỗi miền để kết luận chính xác.',
            text)
    return text


def repair_reviewed_cubic_question(question, subject, grade):
    """Repair the independently reviewed x^3-3x+1 maximum question only.

    Preserve option labels and selection state; do not shuffle on reruns.
    Unknown functions or non-numeric alternatives are left for review.
    """
    if subject != "Toán học" or int(grade) != 12:
        return question
    stem = str(question.get("question", ""))
    formula = re.sub(r"[\s${}\\]", "", stem)
    if "x^3-3x+1" not in formula:
        return question
    result = deepcopy(question)
    if "gia tri cuc dai" in folded(stem):
        values = []
        for option in question.get("options", []):
            value = re.sub(r"^[A-D][.):]\s*", "", str(option)).strip()
            value = re.sub(r"[\s${}\\]", "", value).replace("−", "-")
            if not re.fullmatch(r"[+-]?\d+", value):
                return question
            values.append(int(value))
        if len(values) != 4 or 3 not in values:
            return question
        correct_index = values.index(3)  # f(-1)=3, with + to - derivative sign.
        used = set()
        for index, value in enumerate(values):
            if value in used:
                value = next(n for n in (0, 1, -1, 2, -2) if n not in values and n not in used)
                result["options"][index] = f"{chr(65 + index)}. ${value}$"
            used.add(value)
        result["correct"] = chr(65 + correct_index)
    result["question"] = result["question"].replace(
        "đồng biến trên khoảng nào dưới đây", "đồng biến trên các khoảng nào dưới đây")
    if "ba nghiem phan biet" in folded(stem):
        # f has local minimum -1 and maximum 3; horizontal levels strictly
        # between them meet the cubic three times. Require one exact option.
        matches = []
        for index, option in enumerate(question.get("options", [])):
            value = re.sub(r"^[A-D][.):]\s*", "", str(option))
            value = re.sub(r"[\s${}\\]", "", value).replace("−", "-")
            if value == "-1<m<3":
                matches.append(index)
        if len(matches) == 1:
            result["correct"] = chr(65 + matches[0])
    if "dong bien tren" in folded(stem):
        matches = []
        for index, option in enumerate(question.get("options", [])):
            value = re.sub(r"^[A-D][.):]\s*", "", str(option))
            value = re.sub(r"[\s${}\\]", "", value.lower()).replace("−", "-").replace("và", "va")
            value = value.replace("left", "").replace("right", "")
            if value == "(-infty;-1)va(1;+infty)":
                matches.append(index)
        if len(matches) == 1:
            result["correct"] = chr(65 + matches[0])
    return result


def correct_reviewed_cubic_production_context(text, subject, grade, topic=""):
    """Clarify the observed production model without inventing physical units."""
    value = str(text or "")
    if (canonical_subject(subject) != 'Toán học' or normalize_grade(grade) != 12
            or 'bac ba' not in folded(topic) or 'loi nhuan' not in folded(value)):
        return value
    from services.text_boundaries import preserve_math_and_code
    return preserve_math_and_code(value, lambda prose: prose.replace(
        'là đơn vị sản lượng',
        'là lượng sản phẩm; giả sử xét sản lượng không âm trong mô hình liên tục; '
        'đề chưa quy định đơn vị đo sản lượng và lợi nhuận'))


def correct_reviewed_html_guidance(text, subject, grade, topic=""):
    """Repair observed prose only; leave HTML examples and answer keys intact."""
    if (canonical_subject(subject) != 'Tin học' or normalize_grade(grade) != 12
            or not re.search(r'\bhtml\b', folded(topic))):
        return text
    replacements = {
        'trình duyệt sẽ hiển thị tất cả chữ trên cùng một dòng, không có tiêu đề to, không có xuống dòng.':
            'trình duyệt không tự suy ra đâu là tiêu đề hay đoạn văn; cách xuống dòng còn phụ thuộc kiểu tệp và chiều rộng vùng hiển thị.',
        'Có 6 cấp độ từ `<h1>` (lớn nhất) đến `<h6>` (nhỏ nhất).':
            'Có 6 cấp tiêu đề từ `<h1>` đến `<h6>`, thể hiện cấp bậc nội dung. Kích thước chữ phụ thuộc CSS; khi dùng định dạng mặc định, các cấp thường có cỡ chữ khác nhau.',
        'Chọn thẻ `<h1>` cho tên sách, `<h2>` hoặc `<h3>` cho tác giả. Dùng thẻ `<p>` kết hợp `<br>` cho phần tóm tắt. Dùng thẻ `<ul>` cho danh sách chương.':
            'Em xác định vai trò của từng phần nội dung rồi tự chọn phần tử phù hợp; giải thích lựa chọn dựa trên ý nghĩa và yêu cầu trình bày.',
        'lớn và đậm nhất': 'ở cấp tiêu đề 1; kích thước và độ đậm phụ thuộc CSS (thường lớn, đậm khi dùng định dạng mặc định)',
        'Kiểm tra xem các thẻ đã có đủ thẻ đóng chưa?':
            'Kiểm tra cặp thẻ của các phần tử thông thường; phân biệt phần tử rỗng như br không có thẻ đóng.',
        'Hướng dẫn bạn thay thế đoạn mã sai bằng các thẻ đúng: thêm thẻ `<title>`, sửa lại dấu `< >` cho `<h1>`, và bao quanh các thẻ `<li>` bằng thẻ danh sách phù hợp.':
            'Em tự đề xuất từng chỉnh sửa, giải thích quy tắc được áp dụng rồi thử trên trình duyệt; so sánh kết quả trước và sau sửa.',
        'Tìm các quy tắc bị vi phạm: (1) Nội dung tiêu đề trang phải nằm trong thẻ nào bên trong `<head>`? (2) Cú pháp đóng/mở thẻ `<h1>` đúng là gì? (3) Thẻ `<li>` có thể đứng độc lập mà không có thẻ cha (`<ul>` hoặc `<ol>`) không?':
            'Em lập bảng đối chiếu yêu cầu, đoạn mã hiện có và quy tắc HTML liên quan; tự xác định vị trí cần sửa và thứ tự kiểm tra.',
        'Sự khác biệt chính giữa việc sử dụng thẻ `<br>` và thẻ `<p>` khi trình bày văn bản là gì?':
            'Khi trình duyệt dùng định dạng mặc định, chưa tùy chỉnh CSS, sự khác biệt giữa `<br>` và `<p>` khi trình bày văn bản là gì?',
    }
    # Protect fenced code. Inline literals in the reviewed sentences are matched
    # as a whole, never interpreted or rewritten as executable markup.
    chunks = re.split(r'(```[\s\S]*?```|~~~[\s\S]*?~~~)', str(text))
    for i in range(0, len(chunks), 2):
        chunks[i] = re.sub(r'\(Học sinh tự liệt kê các lỗi như:[^\n]*\)',
                          'Em tự tìm lỗi, nêu quy tắc liên quan và đề xuất bản sửa; chưa xem lời giải mẫu.', chunks[i])
        inline = re.split(r'(`+[^\n]*?`+)', chunks[i])
        tag = r'(<\s*/?\s*(?:html|head|body|title|h[1-6]|p|br|ol|ul|li)\s*>|/|<>)'
        for j in range(0, len(inline), 2):
            inline[j] = re.sub(r'(?<!\$)\$(?!\$)\s*' + tag + r'\s*\$(?!\$)',
                               lambda m: '`' + re.sub(r'\s+', '', m[1]) + '`', inline[j], flags=re.I)
            inline[j] = re.sub(r'\\\(\s*' + tag + r'\s*\\\)',
                               lambda m: '`' + re.sub(r'\s+', '', m[1]) + '`', inline[j], flags=re.I)
        chunks[i] = ''.join(inline)
        for before, after in replacements.items():
            if '`' in before:
                chunks[i] = chunks[i].replace(before, after)
            else:
                inline = re.split(r'(`+[^\n]*?`+)', chunks[i])
                for j in range(0, len(inline), 2):
                    inline[j] = inline[j].replace(before, after)
                chunks[i] = ''.join(inline)
    return ''.join(chunks)


def policy_evaluation_date():
    """Vietnam issue day; separate from the last source-review snapshot."""
    return datetime.now(timezone(timedelta(hours=7))).date().isoformat()


def legal_references(on_date=None, include_upcoming=False):
    today = date.fromisoformat(on_date or policy_evaluation_date())
    rows = json.loads(REGISTRY.read_text(encoding="utf-8"))["documents"]
    return [r for r in rows if r.get("status") != "draft"
            and (include_upcoming or date.fromisoformat(r["effective_from"]) <= today)
            and (not r.get("effective_until") or today < date.fromisoformat(r["effective_until"]))]


def upcoming_legal_references(on_date=None):
    """Future effective dates, independent of a stale registry status label."""
    today = on_date or policy_evaluation_date()
    return [r for r in legal_references(today, include_upcoming=True)
            if r["effective_from"] > today]


def assessment_profile(subject, grade):
    subject, grade = academic_context(subject, grade)
    if grade < 12:
        counts = (0, 0, 0) if subject == "Ngữ văn" else (20, 0, 0) if subject == "Tiếng Anh" else (12, 2, 2)
        return {"counts": counts, "minutes": 45, "weights": (4.0, 4.0, 2.0), "scope": "practice",
                "label": "Luyện tập theo lớp; số câu và thời lượng do người dạy chọn, không phải định dạng thi tốt nghiệp",
                "note": "Đánh giá ở trường theo TT 22/2021 và hướng dẫn áp dụng; không có một ma trận tốt nghiệp chung cho lớp 6–11."}
    if subject == "Ngữ văn":
        counts, minutes, weights = (0, 0, 0), 120, (4.0, 6.0, 0.0)
    elif subject == "Tiếng Anh":
        counts, minutes, weights = (40, 0, 0), 50, (10.0, 0.0, 0.0)
    elif subject == "Toán học":
        counts, minutes, weights = (12, 4, 6), 90, (3.0, 4.0, 3.0)
    elif subject in {"Vật lý", "Hóa học", "Sinh học", "Địa lý"}:
        counts, minutes, weights = (18, 4, 6), 50, (4.5, 4.0, 1.5)
    else:
        counts, minutes, weights = (24, 4, 0), 50, (6.0, 4.0, 0.0)
    note = "Chỉ tham chiếu cấu trúc QĐ 764 ngày 08/03/2024; đề tạo trong app là đề luyện tập, chưa được Bộ thẩm định."
    if subject == "Tin học":
        note += " Đề gốc có 6 câu Đ/S: 2 chung, 2 Khoa học máy tính, 2 Tin học ứng dụng; thí sinh làm 4 câu theo định hướng. App tạo 4 câu cho định hướng đã chọn."
    if subject == "Công nghệ":
        note += " Phải chọn định hướng Công nghiệp hoặc Nông nghiệp trước khi ra đề."
    return {"counts": counts, "minutes": minutes, "weights": weights, "scope": "graduation_reference",
            "label": "Luyện tập lớp 12, tham chiếu cấu trúc thi tốt nghiệp", "note": note}


def policy_prompt(subject, grade, station, topic="", pathway=""):
    subject, grade = academic_context(subject, grade)
    from services.lesson_sources import textbook_update_notice
    book_update = textbook_update_notice(subject, grade)
    edition_guidance = (book_update['note'] + ' Nguồn thông báo: ' + book_update['url']
                        + ' Không tuyên bố đã đọc bản chỉnh sửa nếu chưa có nội dung sách trong ngữ cảnh.') if book_update else ''
    evaluation_day = policy_evaluation_date()
    refs = legal_references(evaluation_day)
    codes = "; ".join(r["code"] for r in refs if r["scope"] in {"curriculum", "textbook", "assessment"})
    profile = assessment_profile(subject, grade)
    hint_guidance = ("Tiếng Anh — hint từ vựng: không dịch nghĩa hoặc diễn giải riêng phương án đúng, "
                     "không cho từ đồng nghĩa của đáp án hay loại sẵn phương án. Hỏi học sinh tự nhận diện "
                     "mục đích, quan hệ nghĩa hoặc dấu hiệu trong câu trước khi so sánh các lựa chọn. "
                     "Định nghĩa/dịch nghĩa và kết luận đáp án chỉ đặt trong explain sau nộp bài."
                     if subject == "Tiếng Anh" else "")
    self_study_guidance = (
        "TRẠM 1 — BẢN TÓM TẮT BÀI HỌC CHO HỌC SINH TỰ HỌC: Gia sư trực tiếp giải thích "
        "kiến thức cốt lõi, rõ ràng, cô đọng, vừa sức; giữ khái niệm, quy tắc/công thức và điều kiện "
        "áp dụng khi phù hợp, ví dụ ngắn có hướng dẫn và câu tự kiểm tra. Viết cho học sinh đọc và "
        "tự thực hiện; không viết thành giáo án dành cho giáo viên, không thay kiến thức bằng kế hoạch "
        "GV tổ chức hoạt động, chia nhóm hoặc tiêu chí sản phẩm. Không rút mất điều kiện khoa học "
        "để làm ngắn. Giữ các phần luyện tập, gia sư/Lab và lời chốt nhân sinh theo yêu cầu riêng."
        if str(station) == "1" else "")
    return f"""\n[NGỮ CẢNH CHƯƠNG TRÌNH — ngày áp dụng {evaluation_day}; ngày rà soát nguồn {POLICY_DATE}]
Trạm {station}; môn {subject}; lớp {grade}; chủ đề {topic}; định hướng {pathway or 'chưa khai báo'}.
{hint_guidance}
{self_study_guidance}
Chương trình GDPT 2018 đọc cùng các sửa đổi còn áp dụng: {codes}.
Sử dụng Kết nối tri thức với cuộc sống, đối chiếu đính chính/cập nhật NXBGD; bộ sách thống nhất toàn quốc từ năm học 2026–2027 theo QĐ 3588/2025 và danh mục bổ sung tại QĐ 185/2026. Phải kiểm đúng tên sách/lớp trong phụ lục và bản cập nhật năm 2026; không suy ra nội dung bài đã được thẩm định.
CT2018 là chuẩn yêu cầu cần đạt; KNTT là trục bài học, không phải giới hạn mọi học liệu. Được dùng ngữ liệu bổ sung đã xác minh từ Cánh Diều, Chân trời sáng tạo hoặc tài liệu khác phù hợp môn/lớp, lứa tuổi và mục tiêu bài học. Ghi riêng “Ngữ liệu bổ sung”, tên tác phẩm/tác giả, sách/nguồn và vị trí thực sự đối chiếu; không gán ngữ liệu ngoài sách thành nguyên văn hoặc nội dung của KNTT, không tự đổi bộ sách chính hay chuẩn đầu ra. Tên bộ/tài liệu chưa xác minh thì không tự nhận là SGK đã được phê duyệt.
{edition_guidance}
{profile['label']}. {profile['note']}
Không có nội dung SGK hoặc văn bản gốc trong ngữ cảnh thì KHÔNG tuyên bố đã đọc/đối chiếu từng trang, không bịa số trang, trích dẫn, tác giả, URL hay xác nhận của Bộ.
Đoạn diễn ý hoặc minh họa do AI biên soạn phải ghi rõ không phải trích dẫn nguyên văn. Không dùng nhãn “trích tinh thần” để gán đoạn tự viết cho SGK hoặc tác giả; chỉ đặt trong dấu trích dẫn với tư cách nguyên văn khi đã có nguồn đối chiếu chính xác.
Khi câu hỏi yêu cầu trả lời theo đoạn văn hoặc dữ liệu đã cho, lời giải chỉ dùng chi tiết có trong phần học sinh nhìn thấy. Nếu cần kiến thức hoặc chi tiết từ ngoài đoạn, phải cung cấp thêm ngữ liệu đã đối chiếu hoặc nêu rõ câu hỏi yêu cầu liên hệ; không trình bày chi tiết ngoài đoạn như thể có trong đoạn.
Chỉ dùng nội dung đúng yêu cầu cần đạt của môn/lớp; danh sách chủ đề gợi ý của app không phải mục lục SGK đã kiểm định. Yêu cầu tùy biến không được đổi môn/lớp hoặc tự miễn kiểm tra chương trình.
Ngữ văn: dạy học có thể dùng văn bản KNTT đã học; đánh giá cuối học kì/cuối năm/cuối cấp tránh dùng lại văn bản đã học trong SGK theo CV 3175. Không được bịa tác giả/trích đoạn rồi gán cho tác phẩm có thật. Không áp yêu cầu này thành lệnh cấm mọi ngữ liệu SGK ở Trạm 1.
TT 17/2025 cập nhật Lịch sử và Địa lí, Lịch sử 10, Địa lí và GDCD/GDKT&PL theo phụ lục tương ứng. Số liệu hiện hành phải có mốc năm và nguồn; không trình bày 63/64 tỉnh thành như cơ cấu hiện tại, không tự sửa số liệu lịch sử thành số liệu hiện tại.
Không tự đổi dữ kiện/đáp án hoặc bù bảng/đồ thị bằng mẫu để làm câu hỏi có vẻ hợp lệ. Thiếu bằng chứng thì ghi rõ cần giáo viên đối chiếu.
Phân bố độ khó theo yêu cầu cần đạt và kế hoạch kiểm tra; không gọi một tỷ lệ NB/TH/VD/VDC tự chọn là tỷ lệ bắt buộc của Bộ.
Không dùng dự thảo như văn bản đang hiệu lực. Không có căn cứ để nói mọi hàm bậc bốn bị cấm trong toàn bộ CT 2018.
"""


def check_current_facts(text):
    """Reject a narrow current-geography contradiction, preserving historical data."""
    for sentence in re.split(r"[\n.!?]", str(text)):
        value = folded(sentence)
        old_count = re.search(r"\b(?:63|64)\s+tinh(?:\s+thanh)?\b", value)
        current = any(x in value for x in ("hien nay", "hien tai", "nuoc ta co", "viet nam co"))
        historical = any(x in value for x in ("truoc nam 2025", "truoc sap nhap", "truoc sap xep", "nam 2024", "nam 2023", "nam 2022"))
        if old_count and current and not historical:
            raise ValueError("Số tỉnh/thành đang được mô tả là hiện hành nhưng dùng dữ liệu cũ; cần đối chiếu nguồn và mốc thời gian.")


def validate_lesson_policy(text, subject, grade):
    subject, grade = academic_context(subject, grade)
    for line in str(text).splitlines()[:8]:
        clean = re.sub(r"\*\*|__", "", line.strip()).lstrip("#* ")
        for field in re.split(r"[|;·]", clean):
            field = field.strip()
            declared_book = re.match(r"(?:Bộ sách|Sách giáo khoa|SGK)\s*:\s*(.+)", field, re.I)
            if declared_book and any(name in folded(declared_book[1]) for name in ('canh dieu', 'chan troi sang tao')):
                raise ValueError("Bài học khai báo bộ sách khác KNTT; cần đối chiếu nguồn trước khi sử dụng.")
            declared_subject = re.match(r"Môn(?: học)?\s*:\s*(.+)", field, re.I)
            if declared_subject and canonical_subject(declared_subject[1].strip()) != subject:
                raise ValueError("Bài học tự khai báo khác môn đang chọn; cần đối chiếu nguồn.")
            declared_grade = re.match(r"(?:khối lớp|lớp|khối)\s*:\s*(\d{1,2})\b", field, re.I)
            if declared_grade and normalize_grade(declared_grade[1]) != grade:
                raise ValueError("Tiêu đề bài học khai báo khác lớp đang chọn.")
        if line.lstrip().startswith('#'):
            for declared_grade in re.finditer(r"(?:lớp|khối)\s*:?\s*(\d{1,2})\b", clean, re.I):
                if normalize_grade(declared_grade[1]) != grade:
                    raise ValueError("Tiêu đề bài học khai báo khác lớp đang chọn.")
    check_current_facts(text)
    return text


def question_groups(exam):
    for part in ("p1", "p2", "p3", "part_viet"):
        if isinstance(exam.get(part), list):
            yield part, exam[part]
    reading = exam.get("part_doc_hieu")
    if isinstance(reading, dict) and isinstance(reading.get("questions"), list):
        yield "part_doc_hieu", reading["questions"]


def prepare_exam_for_delivery(exam, subject, grade, duration=45, custom_request=""):
    """Preserve academic payload; do not call heuristic answer/diagram healers."""
    subject, grade = validate_exam_context(exam, subject, grade)
    from services.request_scope import explicit_request_scope, question_scope_issue
    request_scope = explicit_request_scope(subject, custom_request)
    result = deepcopy(exam)
    validate_exam_structure(result, subject)
    declared_book = folded(result.get("textbook") or result.get("textbook_series") or "")
    if "canh dieu" in declared_book or "chan troi sang tao" in declared_book:
        raise ValueError("Đề khai báo bộ sách khác KNTT; cần đối chiếu và chọn lại nguồn.")
    result.update(subject=subject, grade=grade)
    result.setdefault("duration", duration)
    texts = [result.get("title", "")]
    for _, questions in question_groups(result):
        for question in questions:
            if not isinstance(question, dict):
                raise ValueError("Câu hỏi không đúng cấu trúc; cần sửa dữ liệu nguồn.")
            validate_exam_context({"p1": [question]}, subject, grade)
            if question_scope_issue(question, request_scope):
                raise ValueError("Câu hỏi chưa khớp yêu cầu chỉ hàm bậc ba; cần thay đúng phạm vi trước khi xuất đề.")
            texts.extend(str(question.get(k, "")) for k in ("q", "explain"))
    check_current_facts("\n".join(texts))
    payload = {k: result[k] for k in ("p1", "p2", "p3", "part_doc_hieu", "part_viet") if k in result}
    result["curriculum_audit"] = {
        "policy_checked_at": POLICY_DATE, "policy_evaluated_on": policy_evaluation_date(), "textbook": "Kết nối tri thức với cuộc sống",
        "status": "needs_teacher_review", "academic_verified": False,
        "source_sha256": hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode()).hexdigest(),
        "note": "Đã kiểm tra ngữ cảnh khai báo và một số mâu thuẫn xác định; chưa xác minh từng yêu cầu cần đạt/trang SGK/nguồn gốc."}
    from services.cognitive_levels import audit_exam_levels
    from services.cognitive_runtime import independent_exam_audit
    result['independent_cognitive_audit'] = independent_exam_audit(result, subject, grade)
    return audit_exam_levels(result)


def validate_exam_structure(exam, subject, counts=None):
    """Reject missing keys instead of inventing A, True, zero or a statement."""
    if not isinstance(exam, dict):
        raise ValueError("Đề thi phải là JSON object.")
    if subject == "Ngữ văn":
        reading = exam.get("part_doc_hieu") or {}
        if not isinstance(reading, dict) or not reading.get("text") or not reading.get("questions") or not exam.get("part_viet"):
            raise ValueError("Đề Ngữ văn thiếu ngữ liệu, câu hỏi đọc hiểu hoặc đề viết.")
    elif not any(exam.get(p) for p in ("p1", "p2", "p3")):
        raise ValueError("Đề thi không có câu hỏi.")
    if counts is not None:
        for part, expected in zip(("p1", "p2", "p3"), counts):
            if not isinstance(exam.get(part, []), list) or len(exam.get(part, [])) != expected:
                raise ValueError(f"Phần {part} chưa đúng {expected} câu theo cấu hình; không tự cắt hoặc bù câu khác.")
    for part, questions in question_groups(exam):
        for q in questions:
            if not isinstance(q, dict) or not isinstance(q.get("q"), str) or not q["q"].strip():
                raise ValueError("Câu hỏi thiếu nội dung.")
            if part == "p1":
                opts = q.get("opt")
                answer = str(q.get("ans", "")).strip()
                if not isinstance(opts, list) or len(opts) != 4 or not all(str(o).strip() for o in opts):
                    raise ValueError("Câu trắc nghiệm phải có đúng 4 phương án có nội dung.")
                if not answer or (answer.upper() not in {"A", "B", "C", "D"} and answer not in opts):
                    raise ValueError("Thiếu đáp án trắc nghiệm hợp lệ; không tự gán A.")
            elif part == "p2":
                stmts = q.get("stmts")
                if not isinstance(stmts, list) or len(stmts) != 4:
                    raise ValueError("Câu Đúng/Sai phải có đúng 4 mệnh đề.")
                for stmt in stmts:
                    if not isinstance(stmt, dict) or not str(stmt.get("t", "")).strip() or normalize_bool(stmt.get("a", stmt.get("ans"))) is None:
                        raise ValueError("Mệnh đề thiếu nội dung/đáp án xác định; không tự gán Đúng.")
            elif part == "p3" and (q.get("ans") is None or not str(q.get("ans", "")).strip()):
                raise ValueError("Thiếu đáp số trả lời ngắn; không tự gán 0.")
    return exam


def matrix_html(subject, grade):
    profile = assessment_profile(subject, grade)
    counts = profile["counts"]
    return (f"<div><b>{html.escape(subject)} · Lớp {grade}</b><p>{html.escape(profile['label'])}</p>"
            f"<p>Số câu luyện tập mặc định (I / II / III): {counts[0]} / {counts[1]} / {counts[2]}; "
            f"{profile['minutes']} phút. Có thể điều chỉnh.</p><p>{html.escape(profile['note'])}</p>"
            "<p>Yêu cầu cần đạt và tỷ lệ mức độ nhận thức phải được giáo viên duyệt theo nội dung đã dạy.</p></div>")


def correct_khtn8_lime_soil_confusion(text, subject, grade, topic=""):
    """Narrow repair for the observed KHTN 8 CaO/Ca(OH)2 soil exercise.

    It runs only when both formulas and the lime/soil context are present,
    preserving all unrelated lesson content.
    """
    value = str(text or "")
    if canonical_subject(subject) == "Khoa học tự nhiên" and normalize_grade(grade) == 8:
        if 'base' in folded(topic) and 'ph' in folded(topic):
            # Do not present the observed sparingly soluble example as a
            # uniformly highly soluble list. Keep its identity and basic solution.
            def clarify_observed_calcium_line(match):
                line = match.group(0)
                line = line.replace('Base tan (Kiềm):', 'Độ tan của một số base:')
                line = line.replace('Tan tốt trong nước. Ví dụ:',
                                    'NaOH, KOH và Ba(OH)₂ là các ví dụ kiềm trong bài. Cần phân biệt:')
                return line.replace('tan ít nhưng vẫn xếp vào nhóm kiềm',
                                    'ít tan; phần hòa tan tạo dung dịch nước vôi trong có tính base')
            value = re.sub(r'(?m)^.*Base tan \(Kiềm\):.*tan ít nhưng vẫn xếp vào nhóm kiềm[^\n]*',
                           clarify_observed_calcium_line, value)
            # Observed recognition exercise: retain the task, but let the pupil
            # infer each solution's behaviour instead of supplying the mapping.
            value = re.sub(
                r'Đặc điểm hóa học của mỗi dung dịch \((?:\$\\ce\{)?NaOH(?:\}\$)? là base, '
                r'(?:\$\\ce\{)?HCl(?:\}\$)? là acid, '
                r'(?:\$\\ce\{)?NaCl(?:\}\$)? là muối trung tính\) khi gặp quỳ tím sẽ như thế nào\?',
                'Em cần tra lại tính chất nào của chất chỉ thị để dự đoán hiện tượng? '
                'Hãy tự lập bảng dự đoán cho từng mẫu và nêu căn cứ.', value)
            def complete_base_knowledge(match):
                knowledge = match.group(2)
                normalized = folded(knowledge)
                additions = []
                if not all(term in normalized for term in ('quy tim', 'phenolphthalein')):
                    additions.append('**Base và chất chỉ thị:** Quan sát mô phỏng hoặc thí nghiệm do giáo viên tổ chức: '
                                     'dung dịch NaOH làm quỳ tím chuyển xanh và phenolphthalein không màu chuyển hồng. '
                                     'Không nếm hoặc chạm hóa chất để nhận biết.')
                if not ('muoi' in normalized and 'nuoc' in normalized
                        and any(term in normalized for term in ('trung hoa', 'phan ung'))):
                    additions.append('**Base tác dụng với acid:** Phản ứng tạo muối và nước. '
                                     r'Ví dụ: $\ce{NaOH + HCl -> NaCl + H2O}$. '
                                     'Tự kiểm: Hãy đối chiếu loại chất của các chất tham gia, sản phẩm và số nguyên tử mỗi nguyên tố.')
                return match.group(0) if not additions else match.group(1) + knowledge.rstrip() + '\n\n' + '\n\n'.join(additions) + '\n'
            value = re.sub(
                r'(?ms)(^[# \t]*(?:\*\*)?2\.\s*Hình thành kiến thức(?:\*\*)?[^\n]*\n)(.*?)'
                r'(?=\n[# \t]*(?:\*\*)?3\.\s*Ví dụ)', complete_base_knowledge, value)
        if all(term in folded(value) for term in ('nuoc xa phong', 'qua cam', 'nuoc tinh khiet')):
            value = re.sub(
                r'Xác định môi trường của từng mẫu dựa trên kiến thức thực tế\s*\(Ví dụ:[^\n]*Xà phòng có cảm giác nhờn[^\n]*\)\.',
                'Dùng dữ liệu được cung cấp hoặc kết quả thử chỉ thị dưới sự hướng dẫn của giáo viên '
                'để xác định môi trường từng mẫu; không nếm hoặc chạm mẫu để nhận biết.', value,
                flags=re.I)
            value = re.sub(
                r'(?mi)^([ \t]*(?:[-*][ \t]*)?)(Mẫu\s*\([123]\)):[^\n]*Dự đoán màu quỳ[^\n]*dựa vào tính[^\n]*',
                lambda match: match.group(1) + match.group(2) + ': Em hãy tự xác định môi trường từ dữ kiện, '
                'dự đoán màu quỳ và nêu căn cứ cho dự đoán của mình.', value)
        value = re.sub(
            r"(?ms)(^[# \t]*(?:\*\*)?1\.\s*Khởi động(?:\*\*)?)(.*?)(?=\n[# \t]*(?:\*\*)?2\.\s*Hình thành kiến thức)",
            lambda match: (match.group(1) + '\n\nQuan sát dữ liệu do giáo viên cung cấp: '
                           'hai mẫu dung dịch được đo có pH lần lượt là 3 và 10. '
                           'Em sẽ dùng thang pH để phân biệt môi trường của chúng như thế nào? '
                           'Hãy nêu căn cứ, không nếm hoặc chạm dung dịch để nhận biết.\n\n')
            if any(term in folded(match.group(2)) for term in ('nhua mit', 'cam giac', 'khi cham'))
            else match.group(0), value)
        # Observed unsafe application: neutralisation is not a treatment rule.
        # NHS: https://www.nhs.uk/conditions/insect-bites-and-stings/
        lines = value.splitlines(keepends=True)
        for index, line in enumerate(lines):
            normalized = folded(line)
            if ('ong dot' in normalized and 'boi' in normalized
                    and ('nuoc voi' in normalized or 'kem danh rang' in normalized)):
                lines[index] = ('**Vận dụng — đánh giá thông tin:** Vì sao không thể suy từ phản ứng trung hòa '
                                'trong phòng thí nghiệm để kết luận cách xử lý vết côn trùng đốt? '
                                'Không tự bôi nước vôi hoặc kem đánh răng lên vết đốt; cần hỏi người lớn '
                                'và tìm hướng dẫn y tế phù hợp. Hãy chỉ ra dữ kiện và nguồn chuyên môn '
                                'cần kiểm chứng trước khi áp dụng một mẹo đời sống.\n')
        value = ''.join(lines)
    if (canonical_subject(subject) != "Khoa học tự nhiên" or normalize_grade(grade) != 8
            or not re.search(r"base|pH|đất", folded(topic))
            or not re.search(r"Ca\s*O", value, re.I)
            or not re.search(r"Ca\s*\(\s*OH\s*\)\s*(?:\{\s*)?2", value, re.I)
            or not re.search(r"voi|dat", folded(value))):
        return value

    value = re.sub(
        r"tính chất của vôi bột\s*\(\s*Ca\s*\(\s*OH\s*\)\s*(?:\{\s*)?2\s*\}?\s+là\s+base\s*\)",
        "tính chất của Ca(OH)₂ (vôi tôi, là base; khác với CaO ban đầu là oxide base)",
        value, flags=re.I,
    )
    def clarify_khtn_alkali(match):
        line = match.group(2)
        if ("KNTT yêu cầu tra bảng tính tan" in line or "độ tan Ca(OH)₂ có giới hạn" in line
                or not re.search(r"Ca\s*\(\s*OH\s*\)\s*(?:\{\s*)?2", line, re.I)):
            return line
        return (line + " (Lưu ý: độ tan Ca(OH)₂ có giới hạn; khi xác định kiềm, "
                "hãy đối chiếu bảng tính tan và quy ước trong bài KNTT).")
    value = re.sub(r"(?im)(^|\n)([^\n]*Base tan\s*\(kiềm\):[^\n]*)", lambda m: m.group(1) + clarify_khtn_alkali(m), value)
    note = " (Lưu ý: độ tan Ca(OH)₂ có giới hạn; khi xác định kiềm, hãy đối chiếu bảng tính tan và quy ước trong bài KNTT)."
    value = re.sub('(?:' + re.escape(note) + '){2,}', lambda _: note, value)
    value = re.sub(
        r"b\)\s*Để giảm độ chua[^\n.]{0,400}?Hãy giải thích\.",
        "b) Vì sao CaO có thể góp phần giảm độ chua sau khi phản ứng với nước tạo Ca(OH)₂? "
        "Cần biết thêm những thông tin nào về loại đất, cây trồng và khuyến cáo kỹ thuật "
        "trước khi quyết định vật liệu, liều lượng cải tạo?",
        value, flags=re.I,
    )
    polya_anchor = re.compile(r"Em hãy so sánh số 5 với số 7.{0,1600}?phân đạm acid.{0,500}?đất\.", re.I | re.S)
    def repair_polya(match):
        old = match.group(0)
        normalized_old = folded(old)
        if "phan dam" not in normalized_old or "chon phuong an" not in normalized_old:
            return old
        return ("Em hãy so sánh pH = 5 với mốc 7 để nhận biết môi trường. Tự viết phương trình CaO phản ứng "
                "với nước, gọi tên đúng chất tạo thành, rồi nêu dữ kiện về cây trồng, đất và hướng dẫn kỹ thuật "
                "còn cần trước khi đề xuất cải tạo.")
    value = polya_anchor.sub(repair_polya, value)
    value = re.sub(
        r"Việc bón vôi bột có giúp đưa pH của đất về gần mức trung tính\s*\(\s*pH\s*=\s*7\s*\)\s*không\?\s*"
        r"Giải pháp này có phù hợp với thực tế sản xuất nông nghiệp không\?",
        "Đã đủ dữ kiện để kết luận đất cần đạt pH = 7 chưa? Em cần đối chiếu thêm loại cây, "
        "đặc điểm đất và hướng dẫn kỹ thuật nào trước khi đề xuất cải tạo?",
        value, flags=re.I,
    )
    return value


def validate_explicit_survey_coverage(text, subject, grade, topic):
    """Presence check for a narrowly explicit request, not semantic approval.

    Reuse the bounded arithmetic parser; never repair text or request more AI.
    Only Part 1 counts, so exercises cannot stand in for worked examples.
    """
    subject, grade = academic_context(subject, grade)
    context = folded(topic)
    if not (subject == 'Toán học' and grade == 12 and 'khao sat' in context
            and re.search(r'\b(?:ba|3)\s+(?:dang\s+)?ham(?:\s+so)?\s+co\s+ban\b|\b(?:ba|3)\s+dang\s+ham\b', context)):
        return text
    theory = re.split(r'(?im)^\s*#{0,6}\s*\*{0,2}PHẦN\s*[23]\b', str(text), maxsplit=1)[0]
    theory = re.sub(r'```[\s\S]*?```|~~~[\s\S]*?~~~', '', theory)
    from services.function_visuals import parse_function, X
    import sympy as sp
    found = set()
    # Match only explicit numeric definitions, including y=f(x)=... .
    for match in re.finditer(r"(?<![\w'])\b(?:y\s*=\s*)?(?:f\s*\(\s*x\s*\)|y)\s*=\s*([^$\n;]+)", theory):
        source = re.split(r'\\(?:quad|qquad|text)\b|\\[)\]]', match[1])[0].strip().rstrip('.,')
        source = source.translate(str.maketrans({'²': '^2', '³': '^3', '−': '-'}))
        try:
            expression, excluded = parse_function(source, strict=True)
            numerator, denominator = sp.fraction(expression)
            degrees = (sp.degree(numerator, X), sp.degree(denominator, X))
            if degrees in {(3, 0), (1, 1), (2, 1)}:
                found.add(degrees)
        except (ValueError, SyntaxError, TypeError, NotImplementedError):
            continue
    missing = [name for degree, name in (((3, 0), 'bậc ba'), ((1, 1), 'phân thức 1/1'), ((2, 1), 'phân thức 2/1')) if degree not in found]
    if missing:
        raise ValueError('Yêu cầu khảo sát cả ba dạng nhưng Phần 1 chưa có ví dụ số tường minh cho: '
                         + ', '.join(missing) + '. Cần bổ sung và thẩm định lời giải; không dùng bài tự làm thay ví dụ.')
    return text


def lesson_prompt(subject, grade, topic):
    from services.cognitive_levels import LEVEL_GUIDANCE
    visual_guidance = ""
    if canonical_subject(subject) == "Toán học":
        visual_guidance = (
            "\nBảng biến thiên: chỉ khi nội dung bài thực sự cần và có đủ dữ kiện, "
            "trình bày bảng Markdown với các hàng x, y′, y (bậc hai có thể x, y), "
            "đủ mốc, dấu đạo hàm, giá trị hoặc giới hạn và mũi tên theo đúng hàm đang xét; "
            "không thay bảng bằng đoạn văn xét dấu. Giữ các cột tương ứng để công cụ dựng bảng hiện có xử lý. "
            "Không tự bịa giới hạn, điểm gián đoạn hoặc thêm bảng giải tích cho bài không cần.\n"
            "Nếu yêu cầu rõ cả ba dạng hàm, Phần 1 cần ba ví dụ số có hướng dẫn riêng; không chỉ liệt kê tên hoặc chuyển ví dụ sang bài tự làm. "
            "Khi khảo sát ba dạng SGK, phải giữ đúng dạng không suy biến: bậc ba có a≠0; "
            "y=(ax+b)/(cx+d) có c≠0 và ad−bc≠0; "
            "y=(ax²+bx+c)/(dx+e) có a≠0, d≠0 và ae²−bde+cd²≠0. "
            "Nếu hệ số không thỏa, nêu rõ hàm không thuộc dạng đang xét; "
            "không dùng hàm hằng, mẫu hằng hoặc điểm khuyết làm ví dụ đạt của dạng phân thức này.\n"
            "Trước khi lập bảng hoặc đồ thị, kiểm tập xác định, nghiệm đạo hàm, dấu từng khoảng, "
            "cực trị, giới hạn và tiệm cận; thiếu dữ kiện thì nêu rõ, không tự bổ sung số liệu. "
            "Bảng ba hàng x, y′, y dùng cột xen kẽ mốc và khoảng: hàng x để trống ô khoảng; "
            "hàng y′ ghi dấu ở ô khoảng và 0 đúng mốc nghiệm; hàng y ghi giá trị ở mốc, "
            "mũi tên ↗ hoặc ↘ ở khoảng. Không chép các số -2, 0, 4, 1 từ ảnh mẫu. "
            "Khi bài có mục Đồ thị hoặc yêu cầu khảo sát/vẽ đồ thị, phải cung cấp biểu thức số tường minh của đúng hàm trong ví dụ để hệ thống dựng hình thực; không chỉ mô tả bằng chữ hoặc hứa học sinh tự vẽ. "
            "Mỗi ví dụ cần hình phải có đồ thị riêng theo đúng dữ kiện; không dùng một hình chung cho các hàm khác nhau. "
            "Trong infographic, nền đồ thị/hình vẽ/BBT và nền nhãn phải trong suốt để dùng đúng nền infographic hiện tại, không đặt khung nền trắng riêng; giữ đường và chữ đủ tương phản. "
            "Đồ thị cần trục Ox/Oy, gốc O, khung nhìn chứa các đặc điểm quan trọng, "
            "tách nhánh tại điểm không xác định; tiệm cận nét đứt, nhãn không đè đường cong. "
            "Đồ thị và bảng phải cùng hàm số, cùng cực trị và giới hạn; "
            "không dùng hình ví dụ khác thay hình của bài. "
            "Biểu diễn giao Ox/Oy nếu có, cực trị và tâm đối xứng; dóng nét đứt tới hai trục "
            "(điểm nằm trên trục thì hình chiếu trùng điểm). Giữ phân số, căn thức và tọa độ vô tỉ "
            "ở dạng chính xác, không đổi thành số thập phân làm tròn. Nghiệm không có biểu thức "
            "ngắn được ký hiệu và định nghĩa chính xác theo thứ tự nghiệm của phương trình; "
            "không dùng ký hiệu chưa định nghĩa. Nhãn không đè trục, đường cong, nét dóng hoặc "
            "nhãn khác; tọa độ dài dùng chú giải rõ ràng. Áp dụng thống nhất trong bài và infographic.\n"

        )
    if canonical_subject(subject) == "Ngữ văn":
        visual_guidance += (
            "\nPhần 3 Ngữ văn: chọn nhiệm vụ theo mục tiêu đọc, viết, nói và nghe hoặc tiếng Việt "
            "của bài đang học. Với nghị luận, Bước 2 hỏi học sinh tự đề xuất luận điểm, tìm dẫn chứng "
            "và sắp xếp ý; với tự sự, tìm sự việc và trình tự kể; với đọc hiểu, tìm chi tiết trong "
            "ngữ liệu và giải thích cách hiểu. Không áp luận điểm nghị luận cho mọi thể loại, "
            "không nêu sẵn kết luận, không viết hộ hoặc áp đặt một cách cảm nhận duy nhất.\n"
        )
    if canonical_subject(subject) == "Ngữ văn":
        visual_guidance += (
            "\nDạy viết theo đúng thể loại: với kể trải nghiệm, học sinh tự chọn sự việc, tìm ý, "
            "lập dàn ý, viết bài hoàn chỉnh rồi đọc sửa theo tiêu chí ngôi thứ nhất nhất quán "
            "(em hoặc tôi đều được), trình tự hợp lý, chi tiết, cảm xúc, ý nghĩa, liên kết và chính tả. "
            "Trải nghiệm bình dị vẫn có giá trị; không bắt buộc cao trào hoặc biến cố kịch tính. "
            "Nếu mục tiêu bài là viết một bài văn, cần có hoạt động tạo bài viết hoàn chỉnh "
            "và tự sửa theo tiêu chí thể loại, không chỉ dàn ý và đoạn rời. Bài đọc hiểu hoặc "
            "tiếng Việt không bị buộc chuyển thành hai bài tập viết cả bài văn. "
            "Không yêu cầu luận điểm/dẫn chứng nghị luận cho bài kể chuyện.\n"
        )
    if canonical_subject(subject) == "Tin học" and re.search(
            r"\b(?:html|css|web)\b|trang mạng", folded(topic)):
        visual_guidance += (
            "\nHTML: phân biệt ngữ nghĩa tiêu đề cấp 1, đoạn văn và ngắt dòng với cách hiển thị. "
            "Nếu hỏi kích thước chữ hoặc khoảng cách đoạn, phải nêu điều kiện CSS mặc định/chưa tùy chỉnh. "
            "Thẻ rỗng như br không có thẻ đóng; không yêu cầu mọi thẻ đều có thẻ đóng. "
            "Bài sửa lỗi cần hỏi học sinh tự phát hiện và đề xuất cách sửa, không liệt kê sẵn toàn bộ bản sửa.\n"
        )
    visual_guidance += (
        "\nKhông gán VDC chỉ vì bài dài, nhiều bước, viết đoạn văn hoặc sửa cú pháp cơ bản. "
        "Chọn mức độ theo thao tác tư duy và yêu cầu cần đạt; chưa đủ căn cứ thì để trống nhãn.\n"
    )
    if canonical_subject(subject) in ("Khoa học tự nhiên", "Hóa học"):
        visual_guidance += (
            "\nKIỂM SOÁT CHÍNH XÁC KHOA HỌC HÓA HỌC: phân biệt tên chất, công thức và loại hợp chất; "
            "không gọi CaO là Ca(OH)2. Nếu nhắc vôi sống, ghi CaO (oxide base); phản ứng với nước tạo "
            "Ca(OH)2 (base, vôi tôi). Không gọi chung hai chất là một. Khi bàn cải tạo đất, pH=7 không "
            "phải mục tiêu mặc định cho mọi cây/đất; không kết luận liều bón từ một giá trị pH đơn lẻ. "
            "Nêu dữ kiện còn thiếu và khuyến cáo cần đối chiếu. Phân biệt base với kiềm theo độ tan được "
            "nêu trong tài liệu lớp học; không đánh đồng base ít tan với kiềm tan tốt.\n"
        )
    return policy_prompt(subject, grade, 1, topic) + LEVEL_GUIDANCE + visual_guidance + r"""
Soạn bài học với ba tiêu đề chính: '### PHẦN 1: BÀI HỌC', '### PHẦN 2: TRẮC NGHIỆM KHÁCH QUAN SOCRATIC', '### PHẦN 3: BÀI TẬP TỰ LUẬN'.
Phần 1: khởi động, hình thành kiến thức, ví dụ có lời giải phù hợp lớp, luyện tập và vận dụng; đặc trưng thể loại/môn học phải được giữ.
Trình bày rõ năm mục của Phần 1: Khởi động; Hình thành kiến thức; Ví dụ có lời giải; Luyện tập; Vận dụng. Nội dung mỗi mục hướng trực tiếp tới học sinh tự học; Hình thành kiến thức phải tóm tắt rõ kiến thức cốt lõi và cách dùng, không chỉ ghi mục tiêu hay hoạt động. Câu hỏi tự kiểm ngắn giúp học sinh nhận ra phần chưa hiểu; không dùng các khung “Mục tiêu – Hoạt động thực hiện – Tiêu chí sản phẩm” thay cho lời giảng. Khởi động dùng tình huống gần gũi gắn đúng bài; luyện tập kiểm tra kiến thức vừa học; vận dụng cho nhiệm vụ khả thi, phù hợp tuổi, không đòi dữ kiện chưa cung cấp. Ví dụ có lời giải phải giải thích cách làm. Với môn đọc hiểu, ngoại ngữ và xã hội, chọn hoạt động đặc trưng môn, không ép thành bài toán tính số. Với thí nghiệm hoặc hóa chất, ưu tiên dữ liệu/mô phỏng và chỉ quan sát thí nghiệm do giáo viên tổ chức; không giao tự pha trộn hóa chất tại nhà.
Với ngoại ngữ, chọn dạng ngữ pháp theo ý nghĩa và ngữ cảnh đủ rõ; trạng từ thời gian không tự quyết định duy nhất một thì. Khi kiểm tra thói quen, phân biệt rõ thói quen ổn định với hoạt động lặp lại tạm thời để không loại một phương án vẫn đúng ngữ pháp. Giữ đúng quan hệ đại từ, người nói và quan hệ gia đình khi chuyển ngữ; không đổi bà của nhân vật thành bà của mẹ nhân vật. Chỉ nhận diện dạng động từ hoặc hòa hợp chủ vị không tự động là vận dụng. Phân biệt từ loại với chức năng trong câu: tính từ tired không phải động từ trạng thái; giải thích cấu trúc be + tính từ theo đúng ngữ cảnh, không biến quy tắc thường dùng thành khẳng định không có ngoại lệ.
Phần 2: đúng 3 câu trắc nghiệm, mỗi câu có 4 phương án A/B/C/D và duy nhất một đáp án. Ghi CORRECT: cho đáp án nội bộ, EXPLAIN: cho giải thích nội bộ, HINT: cho gợi mở Socratic theo riêng ngữ cảnh câu hỏi. HINT chỉ dẫn dắt học sinh tự nghĩ; không giải hộ hoặc tiết lộ đáp án. Không dùng EXPLAIN thay HINT.
Phần 3: đúng 2 câu tự luận, mỗi câu hướng dẫn đủ bốn bước Pólya bằng tiếng Việt: Bước 1: Tìm hiểu đề; Bước 2: Lập kế hoạch; Bước 3: Thực hiện kế hoạch; Bước 4: Kiểm tra và nhìn lại. Chỉ đặt câu hỏi hoặc hướng dẫn để học sinh tự thực hiện, không giải hộ, không đưa đáp án. Phần 1 vẫn được giải thích lý thuyết và có ví dụ minh họa; không áp quy tắc giấu lời giải của Socratic sang Phần 1.
Mỗi câu Phần 2 và Phần 3 mở đầu 'Câu n. [Mức độ: NB/TH/VD/VDC]' (chọn một nhãn, hoặc để rỗng nếu chưa đủ căn cứ). Tiếp theo là nội dung câu, các dòng OUTCOME: yêu cầu cần đạt; COGNITIVE_REASON: căn cứ phân loại; COGNITIVE_STEPS: ["thao tác tư duy 1", "thao tác tư duy 2"]. Đây là đề xuất cần giáo viên duyệt, không mặc định tất cả câu là vận dụng.
Công thức đặt trong $...$ hoặc $$...$$; hóa học dùng \ce{...}, đơn vị và chỉ số đúng bản chất. Không bọc công thức bằng backtick, không tự thay omega thành vô cực.
Chỉ tạo hình/bảng khi có đủ dữ kiện của bài, không chèn bảng mẫu hoặc số liệu không có căn cứ. Nội dung ngắn gọn, đầy đủ, không tự gắn nhãn đã được Bộ kiểm duyệt.
"""


def lesson_generation_request(subject, grade, topic):
    """Promote existing policy/level instructions without duplicating their text."""
    from services.cognitive_levels import LEVEL_GUIDANCE
    prefix = policy_prompt(subject, grade, 1, topic) + LEVEL_GUIDANCE
    system = policy_prompt(subject, grade, 1) + LEVEL_GUIDANCE
    full = lesson_prompt(subject, grade, topic)
    if not full.startswith(prefix):
        raise ValueError("Lesson instruction boundary changed; review request builder.")
    from services.lesson_sources import reviewed_lesson_sources
    context = {"lesson_topic": str(topic)}
    review = reviewed_lesson_sources(subject, grade, topic)
    if review['status'] == 'reviewed_requirements_source':
        context['reviewed_requirements_source'] = review
    return system, json.dumps(context, ensure_ascii=False) + "\n" + full[len(prefix):]


def exam_generation_request(subject, grade, topics, counts, code, custom="", pathway=""):
    """Keep custom requests/schema in user content; no new API call or retry."""
    from services.cognitive_levels import LEVEL_GUIDANCE
    # Materialize once so callers may supply an iterable without losing topics.
    topics = list(topics)
    prefix = policy_prompt(subject, grade, 3, "; ".join(topics), pathway) + LEVEL_GUIDANCE
    system = policy_prompt(subject, grade, 3) + LEVEL_GUIDANCE
    full = exam_prompt(subject, grade, topics, counts, code, custom, pathway)
    if not full.startswith(prefix):
        raise ValueError("Exam instruction boundary changed; review request builder.")
    context = json.dumps({"selected_topics": topics, "pathway": str(pathway)}, ensure_ascii=False)
    return system, context + "\n" + full[len(prefix):]


def exam_prompt(subject, grade, topics, counts, code, custom="", pathway=""):
    from services.web_question_contract import WEB_QUESTION_INSTRUCTION
    from services.cognitive_levels import LEVEL_GUIDANCE
    subject, grade = academic_context(subject, grade)
    if subject == "Ngữ văn":
        schema = {"code": str(code), "subject": subject, "grade": grade,
                  "part_doc_hieu": {"text": "Ngữ liệu mới có nguồn thật; nếu tự sáng tác ghi rõ tự sáng tác", "author": "", "source": "",
                                     "questions": [{"q": "Câu đọc hiểu", "ans": "Hướng dẫn chấm", "point": 1.0, "explain": "Gợi ý"}]},
                  "part_viet": [{"q": "Đề viết theo lớp", "ans": "Rubric chấm", "point": 6.0, "explain": "Gợi ý"}]}
        structure = "Đọc hiểu và Viết, rubric tổng 10 điểm; ở lớp 12 tham chiếu 4/6. Số câu, độ dài văn bản và yêu cầu viết phải phù hợp lớp, không áp bài viết lớp 12 cho THCS."
    else:
        schema = {"code": str(code), "subject": subject, "grade": grade,
                  "p1": [{"q": "Câu hỏi", "opt": ["A. ...", "B. ...", "C. ...", "D. ..."], "ans": "B", "topic": "Chủ đề", "explain": "Gợi ý phương pháp"}],
                  "p2": [{"q": "Ngữ liệu", "stmts": [{"t": "Mệnh đề", "a": True}], "topic": "Chủ đề", "explain": "Gợi ý"}],
                  "p3": [{"q": "Câu trả lời ngắn", "ans": "2.5", "topic": "Chủ đề", "explain": "Gợi ý"}]}
        structure = f"Sinh đúng số câu p1/p2/p3 = {tuple(counts)}. Phần có 0 câu phải là []. Mỗi câu p2 có đúng 4 mệnh đề boolean. p3 có đáp số, đơn vị và quy tắc làm tròn rõ ràng. Tiếng Anh: câu hỏi, đoạn đọc và phương án bằng tiếng Anh; giải thích có thể bằng tiếng Việt."
    evidence_schema = {"level": "", "learning_outcome": "", "cognitive_rationale": "", "solution_steps": [],
                       "hint": "Câu hỏi gợi mở theo riêng ngữ cảnh câu này; không giải hộ hoặc đưa đáp án"}
    for key in ("p1", "p2", "p3", "part_viet"):
        for question in schema.get(key, []):
            question.update(evidence_schema)
            for stmt in question.get("stmts", []):
                stmt.update(evidence_schema)
    for question in schema.get("part_doc_hieu", {}).get("questions", []):
        question.update(evidence_schema)
    from services.request_scope import explicit_request_scope, request_scope_prompt
    return (policy_prompt(subject, grade, 3, "; ".join(topics), pathway) + LEVEL_GUIDANCE + request_scope_prompt(explicit_request_scope(subject, custom)) + "\n"
            + "\nTrường hint là gợi mở Socratic độc lập; explain và ans dành cho giải thích/chấm bài, không dùng thay hint. Không tiết lộ đáp án hoặc giải hộ trong hint."
            + structure + WEB_QUESTION_INSTRUCTION + "\nYêu cầu tùy biến trong phạm vi môn/lớp đã chọn: " + str(custom)
            + "\nTự giải và đối chiếu đáp án với giả thiết; thiếu hình thì không đặt câu yêu cầu đọc hình đó. Không sao chép nguồn thiếu bằng chứng hoặc tự nhận là đề thật."
            + "\nChỉ xuất JSON hợp lệ theo schema sau (mở rộng số câu theo cấu hình):\n" + json.dumps(schema, ensure_ascii=False))
