"""One vocabulary for subject identity; keep different curricula separate."""
import re
import unicodedata


def folded(value):
    value = unicodedata.normalize("NFD", str(value or "").casefold()).replace("đ", "d")
    return " ".join(re.sub(r"[^a-z0-9]+", " ", "".join(c for c in value if not unicodedata.combining(c))).split())


_SUBJECTS = {
    "Toán học": ("toán", "toán học", "math", "mathematics"),
    "Vật lý": ("vật lí", "vật lý", "lí", "lý", "physics"),
    "Hóa học": ("hóa học", "hoá học", "hóa", "hoá", "chemistry"),
    "Sinh học": ("sinh học", "sinh", "biology"),
    "Ngữ văn": ("ngữ văn", "văn", "literature"),
    "Tiếng Anh": ("tiếng anh", "anh", "english"),
    "Lịch sử": ("lịch sử", "sử", "history"),
    "Địa lý": ("địa lý", "địa lí", "địa", "geography"),
    "Tin học": ("tin học", "tin", "informatics"),
    "Công nghệ": ("công nghệ", "cn", "technology"),
    "Giáo dục công dân": ("giáo dục công dân", "gdcd"),
    "Giáo dục kinh tế và pháp luật": ("giáo dục kinh tế và pháp luật", "gdkt&pl", "gdktpl", "gdkt pl", "gdkt và pl"),
    "Khoa học tự nhiên": ("khoa học tự nhiên", "khtn"),
    "Lịch sử & Địa lý": ("lịch sử & địa lý", "lịch sử và địa lí", "lịch sử và địa lý", "lịch sử địa lý", "lsđl"),
}
_ALIASES = {folded(alias): subject for subject, aliases in _SUBJECTS.items() for alias in (*aliases, subject)}
_COMMON = ("Toán học", "Ngữ văn", "Tiếng Anh", "Tin học", "Công nghệ")


def canonical_subject(value):
    return _ALIASES.get(folded(value), str(value or "").strip())


def subjects_for_grade(grade):
    grade = normalize_grade(grade)
    return _COMMON + (("Khoa học tự nhiên", "Lịch sử & Địa lý", "Giáo dục công dân") if grade <= 9 else
                      ("Vật lý", "Hóa học", "Sinh học", "Lịch sử", "Địa lý", "Giáo dục kinh tế và pháp luật"))


def normalize_grade(value):
    match = re.fullmatch(r"(?:lớp\s*)?(\d{1,2})", str(value).strip(), re.I)
    if not match or not 6 <= int(match[1]) <= 12:
        raise ValueError("Khối lớp phải từ 6 đến 12.")
    return int(match[1])


def academic_context(subject, grade):
    subject, grade = canonical_subject(subject), normalize_grade(grade)
    if subject not in subjects_for_grade(grade):
        raise ValueError(f"Môn {subject} không thuộc danh mục lớp {grade}; hãy chọn đúng môn tích hợp/cấp học.")
    return subject, grade


def topic_matches(requested, candidate):
    """Do not treat a single generic word as a matching topic."""
    requested, candidate = folded(requested), folded(candidate)
    if not requested or not candidate:
        return False
    if requested in candidate or candidate in requested:
        return True
    ignored = {"chuyen", "de", "chu", "bai", "tap", "lop", "va", "cua", "trong", "mot", "cac"}
    left, right = set(requested.split()) - ignored, set(candidate.split()) - ignored
    common = left & right
    return len(common) >= 2 and len(common) / max(1, min(len(left), len(right))) >= 0.75


def validate_exam_context(exam, subject, grade):
    """Reject explicit conflicting metadata, before normalizers can overwrite it."""
    subject, grade = academic_context(subject, grade)
    if not isinstance(exam, dict):
        raise ValueError("Đề thi phải là dữ liệu có cấu trúc.")
    items = [exam]
    for part in ("p1", "p2", "p3", "part_1", "part_2", "part_3", "part_I", "part_II", "part_III", "part_viet"):
        questions = exam.get(part, [])
        if isinstance(questions, list):
            items.extend(q for q in questions if isinstance(q, dict))
    reading = exam.get("part_doc_hieu")
    if isinstance(reading, dict) and isinstance(reading.get("questions"), list):
        items.extend(q for q in reading["questions"] if isinstance(q, dict))
    title_grade = re.search(r"(?:lớp|khối)\s*(\d{1,2})\b", str(exam.get("title", "")), re.I)
    if title_grade and normalize_grade(title_grade[1]) != grade:
        raise ValueError("Tiêu đề đề thi khai báo khác lớp đang chọn.")
    for item in items:
        declared = item.get("subject")
        if declared and canonical_subject(declared) != subject:
            raise ValueError(f"Đề/câu hỏi mang môn {declared}, không khớp môn {subject} đang chọn.")
        declared_grade = item.get("grade", item.get("grade_level"))
        if declared_grade is not None and normalize_grade(declared_grade) != grade:
            raise ValueError(f"Đề/câu hỏi mang lớp {declared_grade}, không khớp lớp {grade} đang chọn.")
    return subject, grade
