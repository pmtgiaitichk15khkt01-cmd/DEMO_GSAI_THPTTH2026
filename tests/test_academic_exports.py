import ast
import hashlib
import html
import json
import re
import tempfile
import unicodedata
import unittest
from pathlib import Path
from unittest.mock import patch

from services.academic_context import academic_context, canonical_subject, subjects_for_grade, topic_matches, validate_exam_context
from services.lesson_export import build_lesson_html, faithful_infographic_data, handwritten_prompt, lesson_body_html
from services.lesson_sources import books_for, lesson_references, PUBLISHER_PORTAL, PUBLISHER_DIGITAL_LIBRARY, textbook_update_notice


class TestAcademicContext(unittest.TestCase):
    def test_direct_export_rejects_wrong_subject_grade_or_book(self):
        for lesson in ['Môn: Hóa học\nNội dung', 'Lớp: 9\nNội dung',
                       'Bộ sách: Cánh Diều\nNội dung']:
            with self.assertRaises(ValueError):
                build_lesson_html('Toán', 8, 'Bài đang kiểm', lesson)

    def test_publisher_catalog_and_digital_reader_are_distinct_official_routes(self):
        self.assertEqual(PUBLISHER_PORTAL, "https://taphuan.nxbgd.vn/tap-huan?tab=public")
        self.assertEqual(PUBLISHER_DIGITAL_LIBRARY, "https://truonghocsoquocgia.nxbgd.vn/")
        self.assertNotEqual(PUBLISHER_PORTAL, PUBLISHER_DIGITAL_LIBRARY)

    def test_2026_publisher_update_is_scoped_to_seven_supported_pairs(self):
        affected = {(grade, subject) for grade in range(6, 13) for subject in subjects_for_grade(grade)
                    if textbook_update_notice(subject, grade)}
        self.assertEqual(affected, {(g, 'Lịch sử & Địa lý') for g in range(6, 10)}
                         | {(10, 'Lịch sử'), (10, 'Giáo dục kinh tế và pháp luật'), (12, 'Địa lý')})
        for grade, subject in affected:
            refs = lesson_references(subject, grade, 'Chủ đề đang kiểm', {}, lambda _: '')
            self.assertIn('Thông báo cập nhật của NXBGD', refs['badge_html'])
            self.assertIn('chưa xác minh là bản chỉnh sửa 2026', refs['badge_html'])
            rows = books_for(subject, grade)
            self.assertTrue(any(row['kind'] == 'publisher_book_page' for row in rows))
            self.assertTrue(all(row['kind'] in ('publisher_book_page', 'portal') for row in rows))

    def test_aliases_accents_and_case_are_one_identity(self):
        for alias, expected in [("TOÁN", "Toán học"), ("Địa lí", "Địa lý"), ("dia ly", "Địa lý"),
                                ("Vật lí", "Vật lý"), ("Hoá học", "Hóa học"), ("LSĐL", "Lịch sử & Địa lý")]:
            for spelling in (alias, unicodedata.normalize("NFD", alias)):
                self.assertEqual(canonical_subject(spelling), expected)

    def test_civic_education_is_not_economics_and_law(self):
        self.assertEqual(academic_context("GDCD", 8), ("Giáo dục công dân", 8))
        with self.assertRaises(ValueError):
            academic_context("GDCD", 12)
        with self.assertRaises(ValueError):
            academic_context("Địa lí", 6)

    def test_all_65_supported_subject_grade_pairs(self):
        count = 0
        for grade in range(6, 13):
            for subject in subjects_for_grade(grade):
                self.assertEqual(academic_context(subject, f"Lớp {grade}"), (subject, grade))
                rows = books_for(subject, grade)
                self.assertTrue(rows)
                self.assertTrue(all(str(grade) in row["title"] for row in rows if row['kind'] != 'portal'))
                count += 1
        self.assertEqual(count, 65)

    def test_technology_textbook_references_link_to_official_grade_and_pathway_pages(self):
        for grade in range(6, 13):
            rows = [r for r in books_for("Công nghệ", grade) if r['kind'] != 'portal']
            self.assertTrue(rows)
            self.assertTrue(all(row["kind"] == "publisher_book_page" for row in rows), grade)
            self.assertTrue(all("taphuan.nxbgd.vn/tap-huan/chi-tiet-sach/" in row["url"] for row in rows), grade)
            self.assertTrue(all(str(grade) in row["title"] for row in rows), grade)
        self.assertIn("Công nghệ trồng trọt", " ".join(r["title"] for r in books_for("Công nghệ", 10)))
        self.assertIn("Công nghệ cơ khí", " ".join(r["title"] for r in books_for("Công nghệ", 11)))
        self.assertIn("Lâm nghiệp", " ".join(r["title"] for r in books_for("Công nghệ", 12)))

    def test_explicit_wrong_exam_metadata_is_rejected(self):
        for exam in [{"subject": "Hóa học", "grade": 12}, {"subject": "Toán", "grade": 11},
                     {"p1": [{"q": "question", "subject": "Vật lý"}]}, {"p3": [{"q": "question", "grade": 10}]}]:
            with self.assertRaises(ValueError):
                validate_exam_context(exam, "Toán học", 12)
        self.assertEqual(validate_exam_context({"subject": "Địa lí", "grade": 12}, "Địa lý", 12), ("Địa lý", 12))

    def test_single_generic_word_cannot_match_topic(self):
        self.assertFalse(topic_matches("Hàm số lượng giác", "Hàm số bậc hai"))
        self.assertTrue(topic_matches("Thống kê mẫu ghép nhóm", "Mẫu ghép nhóm"))


class TestLessonExport(unittest.TestCase):
    lesson = r"""## Phân số trong bài học
Chỉ có nội dung SENTINEL_GRADE_6 và $\frac{1}{2}$.
Ví dụ: $\frac{\sqrt{x+1}}{x^2+1}$.

```python
value = r"\omega"
print("<script>")
```
"""

    def test_source_math_and_code_are_preserved_and_escaped(self):
        rendered = lesson_body_html(self.lesson)
        self.assertIn(html.escape(r"\frac{\sqrt{x+1}}{x^2+1}", quote=True), rendered)
        self.assertIn(r"\omega", rendered)
        self.assertNotIn("<script>", rendered)
        self.assertIn("&lt;script&gt;", rendered)

    def test_offline_document_has_accurate_context_and_embedded_fonts(self):
        output = build_lesson_html("Toán", 6, "Phân số", self.lesson)
        self.assertIn("Toán học · Lớp 6", output)
        self.assertIn('class="handwritten"', output)
        self.assertIn(hashlib.sha256(self.lesson.encode()).hexdigest(), output)
        self.assertIn("data:font/woff2;base64,", output)
        self.assertNotIn("url(fonts/", output)
        self.assertIn("data:font/ttf;base64,", output)
        self.assertNotRegex(output, r'<script[^>]+src=')
        self.assertNotRegex(output, r'<link[^>]+href=')
        self.assertNotIn("fonts.googleapis.com", output)
        self.assertIn("maxExpand:1000", output)
        self.assertIn("trust:false", output)
        self.assertIn("print.disabled=errors>0", output)

    def test_projection_does_not_inject_grade_12_template(self):
        data = faithful_infographic_data("Toán", 6, "Phân số", self.lesson)
        text = json.dumps(data, ensure_ascii=False)
        self.assertNotIn("tiệm cận", text)
        self.assertNotIn("đạo hàm", text)
        self.assertNotIn("x³", text)
        self.assertIn("SENTINEL_GRADE_6", text)
        self.assertFalse(data["example"]["visual_svg"])

    def test_prompt_contains_exact_source_with_only_style_instructions(self):
        prompt = json.loads(handwritten_prompt("Toán", 6, "Phân số", self.lesson))
        self.assertEqual(prompt["content"], self.lesson)
        self.assertEqual((prompt["subject"], prompt["grade"]), ("Toán học", 6))
        self.assertEqual(prompt["style"]["body_ink"], "#182C73")

    def test_empty_or_incompatible_export_fails_explicitly(self):
        with self.assertRaises(ValueError):
            build_lesson_html("Toán", 6, "topic", "")
        with self.assertRaises(ValueError):
            build_lesson_html("Hóa học", 6, "topic", "body")

    def test_naked_math_is_flagged_without_changing_its_meaning(self):
        value = lesson_body_html(r"Công thức chưa đóng: $\frac{1}{2}")
        self.assertIn('data-source-issue="math-delimiter"', value)
        self.assertIn(r"\frac{1}{2}", value)

    def test_final_gate_preserves_physics_symbols_and_code(self):
        tree = ast.parse(Path(__file__).resolve().parents[1].joinpath("app.py").read_text(encoding="utf-8"))
        functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in {"_legacy_sanitize_katex_latex", "sanitize_katex_latex"}]
        namespace = {"re": re}
        exec(compile(ast.Module(body=functions, type_ignores=[]), "latex-test", "exec"), namespace)
        source = r"Dao động $x=A\cos(\omega t+\varphi)$; điện trở $R=2\,\Omega$." + '\n```python\nprint(r"\\frac{1}{2}")\n```'
        output = namespace["sanitize_katex_latex"](source)
        self.assertIn(r"\omega", output)
        self.assertIn(r"\Omega", output)
        self.assertNotIn(r"\infty", output)
        self.assertIn('```python\nprint(r"\\frac{1}{2}")\n```', output)

    def test_long_content_is_not_cut_or_squeezed_into_fixed_page(self):
        lesson = "\n\n".join(f"Ý kiến thức {i}: giữ nguyên phần nội dung." for i in range(250))
        output = build_lesson_html("Ngữ văn", 9, "Đọc hiểu", lesson)
        self.assertIn("Ý kiến thức 249", output)
        self.assertNotIn("height:1130", output)
        self.assertIn("@page{size:A4", output)


class TestReferencesAndExamSelection(unittest.TestCase):
    def test_civic_bank_does_not_become_grade_12_economics(self):
        import real_exam_engine as engine
        rows = engine.get_baseline_full_exams("GDCD", 6)
        self.assertTrue(rows)
        self.assertTrue(all(canonical_subject(row.get("subject")) == "Giáo dục công dân" and str(row.get("grade")) == "6" for row in rows))
        self.assertEqual(engine.get_baseline_full_exams("GDKT&PL", 12), [])
    def test_reference_code_does_not_invent_textbook_chapter_number(self):
        row = lesson_references("Địa lí", 12, "Chủ đề tùy chọn <test>", {}, lambda url: "qr")
        self.assertTrue(row["index_code"].startswith("GSAI-"))
        self.assertNotIn("Chương 1", row["badge_html"])
        self.assertIn("kết quả tìm kiếm", row["badge_html"])
        self.assertIn("&lt;test&gt;", row["badge_html"])

    def test_broken_book_link_is_replaced_by_labeled_portal(self):
        row = books_for("Sinh học", 10)[0]
        self.assertEqual(row["url"], PUBLISHER_PORTAL)
        self.assertEqual(row["kind"], "portal")
        self.assertTrue(row["title"].startswith("Tra cứu"))

    def test_selected_topic_cannot_be_padded_with_unrelated_bank_questions(self):
        import real_exam_engine as engine
        unrelated = {"q": "Câu hỏi không thuộc bài chọn", "topic": "Hình học không gian", "opt": ["A. 1", "B. 2", "C. 3", "D. 4"], "ans": "A"}
        with patch.object(engine, "get_baseline_questions_pool", return_value={"p1": [unrelated], "p2": [], "p3": []}):
            exam = engine.ensure_full_exam_matrix({"chosen_topics": ["Phân số"], "p1": [], "p2": [], "p3": []}, "Toán", 6, (1, 0, 0))
        self.assertEqual(exam["p1"], [])

    def test_literature_cannot_ignore_explicit_selected_topic(self):
        import real_exam_engine as engine
        row = {"subject": "Ngữ văn", "grade": 9, "title": "Thơ trữ tình", "p1": [], "p2": [], "p3": []}
        with patch.object(engine, "get_baseline_full_exams", return_value=[row]), patch.object(engine, "get_baseline_questions_pool", return_value={"p1": [], "p2": [], "p3": []}):
            exam = engine.generate_blended_real_exam("Ngữ văn", 9, ["Văn bản nghị luận"], (1, 0, 0))
        self.assertFalse(exam and exam.get("title") == "Thơ trữ tình")

    def test_word_header_uses_actual_subject_grade_and_duration(self):
        from docx import Document
        from services.azota_lms_exporter import export_exam_to_azota_docx, export_exam_to_azota_text
        exam = {"subject": "Địa lí", "grade": 11, "duration": 25, "p1": [], "p2": [], "p3": []}
        document = Document(export_exam_to_azota_docx(exam))
        text = "\n".join(p.text for p in document.paragraphs)
        self.assertIn("Địa lý", text)
        self.assertIn("Lớp: 11", text)
        self.assertIn("25 phút", text)
        self.assertNotIn("90 phút", text)
        self.assertIn("Lớp: 11", export_exam_to_azota_text(exam))
