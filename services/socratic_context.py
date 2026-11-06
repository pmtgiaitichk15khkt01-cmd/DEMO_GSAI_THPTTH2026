"""Subject-aware fallback questions, without certifying generated hint content."""
import re

from services.academic_context import canonical_subject, folded

T1_CONTEXT_REVISION = 2026110506


def repair_reviewed_station1_closing(reply, student_message, subject, grade, closing=False):
    """Fix a reproduced contradictory recap; preserve the full moral lesson."""
    text = str(reply or '')
    if not closing:
        return text
    student = re.sub(r'[\s${}\\]', '', str(student_message))
    first = re.split(r'\n\s*\n', text, maxsplit=1)[0]
    if (subject == 'Toán học' and int(grade) == 12
            and '3x^2' in student and 'khong doi dau' in folded(student_message)
            and 'phan tich su doi dau' in folded(first)):
        text = text.replace(first,
            'Thầy ghi nhận em đã tự kiểm tra dấu đạo hàm ở hai phía điểm xét và trình bày lập luận của mình. '
            'Việc đối chiếu kết quả thay vì chỉ nhớ công thức là thói quen học tập đáng khuyến khích.', 1)
    if 'Marcus Aurelius' in text and 'Meditations' in text and 'George Long' in text:
        text = text.replace('theo bản dịch của George Long',
                            'diễn nghĩa tiếng Việt từ bản dịch tiếng Anh của George Long')
        if 'meditations.6.six.html' not in text:
            text = text.replace('tham khảo tại classics.mit.edu',
                'nguồn: [Internet Classics Archive — Book VI](https://classics.mit.edu/Antoninus/meditations.6.six.html)')
    return text


def is_post_closure_thanks(message, closed=False, history=None):
    """Only a social acknowledgement after a successful lesson closing."""
    # Recover only from a clearly completed moral closing in this chat,
    # never from a welcome message or the student's thanks alone.
    recorded_closing = any(
        item.get('role') == 'assistant'
        and 'thay chuc' in folded(item.get('content', ''))
        and 'tram 2' in folded(item.get('content', ''))
        and any(marker in folded(item.get('content', ''))
                for marker in ('internet classics archive', 'classics.mit.edu'))
        for item in (history or []) if isinstance(item, dict))
    if not closed and not recorded_closing:
        return False
    value = folded(str(message or ''))
    words = re.findall(r'[a-z]+', value)
    allowed = set('da vang em con cam on thay co rat nhieu a nhe nha nhe lam xin chan thanh biet tri an thank you thanks teacher so much'.split())
    gratitude = 'cam on' in ' '.join(words) or 'thank' in words or 'thanks' in words
    return gratitude and bool(words) and set(words) <= allowed


def _names_unique_chemical_answer(hint, options, correct_answer, question):
    """Block a named element cue unique to the correct formula, not given data."""
    letter = str(correct_answer).strip().upper()
    if not options or letter not in ('A', 'B', 'C', 'D') or len(options) != 4:
        return False
    index = ord(letter)-ord('A')
    aliases = {'Na': ('natri', 'sodium'), 'K': ('kali', 'potassium'),
               'Ca': ('canxi', 'calcium', 'nước vôi'), 'Ba': ('bari', 'barium'),
               'Al': ('nhôm', 'aluminium', 'aluminum'), 'Mg': ('magnesium', 'magie', 'magiê'),
               'Cu': ('kim loại đồng', 'copper'), 'Fe': ('kim loại sắt', 'iron')}
    def contains_symbol(text, symbol):
        return bool(re.search(r'(?<![A-Za-z])'+symbol+r'(?=$|[A-Z0-9(){}^+\-\s$])', str(text)))
    h, q = folded(hint), folded(question)
    for symbol, names in aliases.items():
        if (not contains_symbol(options[index], symbol) or contains_symbol(question, symbol)
                or any(contains_symbol(o, symbol) for i,o in enumerate(options) if i != index)):
            continue
        for name in names:
            cue = r'\b'+re.escape(folded(name))+r'\b'
            if re.search(cue, h) and not re.search(cue, q):
                return True
    return False


def math_context_question(question):
    """Small context-specific fallback library; no calculation or answer content."""
    text = folded(question)
    if 'truc tung' in text and any(term in text for term in ('cat truc tung', 'giao diem', 'tung do')):
        return ('Một điểm nằm trên trục tung thì hoành độ có đặc điểm gì? '
                'Từ đó, em sẽ dùng hàm số đã cho để xác định tung độ như thế nào?')
    has_parameter = 'tham so' in text
    monotonic = any(term in text for term in ('dong bien', 'nghich bien'))
    real_text = folded(re.sub(r'\\(?:mathbb|mathbf|mathrm)\s*(?:\{[Rr]\}|[Rr])|ℝ', 'R', str(question)))
    real_line = bool(re.search(r'\btren\s+(?:tap\s+)?r\b', real_text)) or 'tren toan bo truc so' in text
    if has_parameter and monotonic and real_line:
        tail = (' Khi đã tìm được miền tham số, em sẽ lọc và đếm các giá trị nguyên như thế nào?'
                if 'nguyen' in text else ' Em sẽ suy ra điều kiện của tham số như thế nào?')
        return ('Em sẽ tính đạo hàm chứa tham số và đặt điều kiện về dấu nào để tính đơn điệu '
                'đúng với mọi giá trị của biến trên toàn bộ trục số?' + tail)
    for kind in ('tieu', 'dai'):
        if 'toa do diem cuc ' + kind in text:
            label = 'cực tiểu' if kind == 'tieu' else 'cực đại'
            return (f'Em cần nhận ra sự đổi dấu nào của đạo hàm để tìm hoành độ điểm {label}? '
                    'Sau đó, em sẽ dùng hàm số ban đầu như thế nào để xác định đủ hai tọa độ?')
    return None


_QUESTIONS = {
    'Ngữ văn': 'Em cần tìm chi tiết, từ ngữ hoặc bằng chứng nào trong ngữ liệu để trả lời đúng yêu cầu?',
    'Tiếng Anh': 'Em nhận thấy dấu hiệu nào về nghĩa, cấu trúc câu hoặc ngữ cảnh trước khi đối chiếu các phương án?',
    'Lịch sử': 'Em cần xác định mốc thời gian, bối cảnh và bằng chứng lịch sử nào liên quan đến yêu cầu?',
    'Địa lý': 'Em cần đọc thông tin nào từ bản đồ, bảng số liệu hoặc ngữ liệu địa lí để đối chiếu yêu cầu?',
    'Lịch sử & Địa lý': 'Em cần xác định bối cảnh thời gian, không gian và bằng chứng nào trong ngữ liệu?',
    'Vật lý': 'Em cần nhận diện hiện tượng, các đại lượng và điều kiện áp dụng mối quan hệ vật lí nào?',
    'Hóa học': 'Em cần xác định chất, điều kiện hoặc bằng chứng phản ứng nào trước khi đối chiếu các phương án?',
    'Sinh học': 'Em cần xác định cấp độ tổ chức, quá trình hoặc bằng chứng sinh học nào trong câu hỏi?',
    'Khoa học tự nhiên': 'Em cần nhận diện hiện tượng, dữ kiện và mối quan hệ khoa học nào trong câu hỏi?',
    'Tin học': 'Em cần xác định đầu vào, đầu ra hoặc quy tắc hoạt động nào trong tình huống được nêu?',
    'Công nghệ': 'Em cần xác định chức năng, điều kiện sử dụng và tiêu chí nào của giải pháp công nghệ?',
    'Giáo dục công dân': 'Em cần đối chiếu hành vi, hoàn cảnh và nguyên tắc ứng xử nào trong tình huống?',
    'Giáo dục kinh tế và pháp luật': 'Em cần xác định chủ thể, quan hệ kinh tế hoặc quyền và nghĩa vụ nào trong tình huống?',
}


def guiding_question(hint, options=None, correct_answer='', question_text=''):
    """Prefer a separate guiding question; never substitute the EXPLAIN field.

    Explicit answer markers and verbatim alternatives are rejected here. This
    is a structural check, not proof that every paraphrase is non-revealing.
    Rejection changes only the hint, never blocks the lesson or calls AI again.
    """
    value = str(hint or '').strip()
    marked_answer = re.search(
        r'(?i)(?:\b(?:chọn|đáp án|đáp số|answer|choose|option)\s*(?:đúng\s*)?(?:là|is|:)?\s*[A-D]\b'
        r'|\b[A-D]\s*(?:là\s*)?(?:đúng|correct)\b)', value)
    alternatives = [re.sub(r'^[A-D][.):]\s*', '', str(o), flags=re.I).strip().casefold()
                    for o in options or []]
    answer = str(correct_answer or '').strip().casefold()
    if len(answer) > 3:
        alternatives.append(answer)
    repeats_answer = any(len(o) > 3 and o in value.casefold() for o in alternatives)
    # A standalone numeric equality can disclose a result. Preserve equations
    # already supplied by the question, and coefficients in symbolic formulas.
    numeric_equality = re.compile(r"\b(?:[a-zA-Z]|[fgh]\s*\(\s*x\s*\))\s*=\s*[+-]?\d+(?:[.,]\d+)?(?:\s*/\s*\d+)?(?![\d.,/])(?=\s*(?:[$,;?)}]|(?:có|co|đúng|dung)\b|$))")
    normalize = lambda text: re.sub(r'[\s${}\\]', '', str(text)).casefold()
    source = normalize(question_text)
    new_result = any(normalize(match[0]) not in source for match in numeric_equality.finditer(value))
    if value and len(value) <= 800 and value.endswith('?') and not marked_answer and not repeats_answer and not new_result:
        return value
    return None


def english_reading_question(question):
    """Guide evidence selection from the final reading task, never quote its answer."""
    text = str(question or '')
    if not re.search(r'(?i)\b(?:read\b.{0,50}\b(?:passage|text)|according to (?:the )?(?:passage|text))\b', text):
        return None
    tasks = re.findall(r'(?i)\b(what|where|when|who|why|how)\b[^?]{0,300}\?', text)
    if not tasks:
        return None
    kind = tasks[-1].lower()
    targets = {'what': 'hoạt động, sự việc hoặc thông tin được hỏi',
               'where': 'địa điểm được hỏi', 'when': 'thời điểm được hỏi',
               'who': 'nhân vật được hỏi', 'why': 'nguyên nhân được hỏi',
               'how': 'cách thức hoặc mức độ được hỏi'}
    return (f'Câu hỏi cuối đoạn đọc yêu cầu em xác định {targets[kind]}. '
            'Em sẽ tìm chi tiết nào trong đoạn và kiểm tra đúng chủ thể, hoàn cảnh '
            'trước khi đối chiếu các phương án?')


def computing_context_question(question):
    """Small task-specific prompts; no numerical result or answer alternative."""
    text = folded(question)
    if ('html' in text and 'noi dung' in text and ('hien thi' in text or 'nhin thay' in text)
            and ('trinh duyet' in text or 'trang' in text)):
        return ('Em sẽ phân biệt phần thông tin về tài liệu với phần nội dung người đọc nhìn thấy '
                'theo tiêu chí nào, rồi đối chiếu vai trò của từng phương án ra sao?')
    if 'danh sach' in text and any(term in text for term in ('thu tu', 'danh so')):
        return ('Danh sách trong yêu cầu cần thể hiện mối quan hệ nào giữa các mục? '
                'Em sẽ phân biệt phần tử bao ngoài với từng mục và đối chiếu vai trò của các thẻ ra sao?')
    if 'cpu' in text:
        return ('Em sẽ phân biệt vai trò của CPU với bộ nhớ và thiết bị vào, ra '
                'theo tiêu chí nào trước khi đối chiếu từng phát biểu?')
    if 'dung luong' in text and any(term in text for term in ('the nho', 'tep', 'buc anh')):
        if re.search(r'bao nhieu\s+(?:the nho|thiet bi|o dia)', text):
            return ('Tổng dung lượng cần lưu và dung lượng mỗi thiết bị đã cùng đơn vị chưa? '
                    'Đề đã nêu điều kiện chia tệp giữa các thiết bị chưa? '
                    'Em sẽ xác định số thiết bị cần dùng và xử lý phần dư như thế nào?')
        return ('Dung lượng lưu trữ và dung lượng mỗi tệp đã cùng đơn vị chưa? '
                'Em sẽ dùng quan hệ nào để tìm số tệp chứa được và xử lý phần dư?')
    if 'thiet bi so' in text and any(term in text for term in ('ket noi', 'cong')):
        return ('Với từng nhận định, em có thể đối chiếu thiết bị và cổng kết nối thực tế nào? '
                'Các từ khẳng định tuyệt đối có đúng trong mọi trường hợp không?')
    return None


def subject_socratic_hint(hint, subject, options=None, correct_answer='', question_text=''):
    subject = canonical_subject(subject)
    if subject in ('Hóa học', 'Khoa học tự nhiên') and _names_unique_chemical_answer(hint, options, correct_answer, question_text):
        if any(term in folded(question_text) for term in ('base tan', 'kiem', 'tinh tan')):
            return 'Em sẽ dùng tiêu chí nào và tra bảng tính tan ra sao để tự phân biệt từng chất trong các phương án?'
        return _QUESTIONS[subject]
    question = guiding_question(hint, options, correct_answer, question_text)
    if subject == 'Tin học':
        contextual = computing_context_question(question_text)
        # Live CPU hint repeated the identifying metaphor from the correct option.
        # Replace only that observed cue, not every valid supplied computing hint.
        cpu_metaphor = 'cpu' in folded(question_text) and 'bo nao' in folded(hint)
        key = str(correct_answer).strip().upper()
        html_name_cue = (
            'danh sach' in folded(question_text) and options and len(options) == 4
            and key in ('A', 'B', 'C', 'D')
            and re.search(r'<\s*ol\b', str(options[ord(key) - ord('A')]), re.I)
            and re.search(r'\border(?:ed)?\b', folded(hint))
            and not re.search(r'\border(?:ed)?\b|\bol\b', folded(question_text))
        )
        generic_computing_hint = folded(hint) == folded(_QUESTIONS.get(subject, ''))
        if contextual and (not question or cpu_metaphor or html_name_cue or generic_computing_hint):
            return contextual
    if question:
        return question
    if subject == 'Tiếng Anh':
        contextual = english_reading_question(question_text)
        if contextual:
            return contextual
    return _QUESTIONS.get(subject, 'Em cần xác định dữ kiện và yêu cầu nào trước khi tự đối chiếu các phương án?')
