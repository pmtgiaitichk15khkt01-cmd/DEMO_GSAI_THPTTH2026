import unittest
from services.lesson_export import saved_markdown_html


class SavedLessonExportTests(unittest.TestCase):
    def test_utf8_bom_and_original_math_survive_without_ai(self):
        result = saved_markdown_html('\ufeff# Bài đã lưu\n$x^2+1$'.encode('utf-8'), 'Toán học', 10, 'Hàm số')
        self.assertIn('Bài đã lưu', result)
        self.assertIn('x^2+1', result)
        self.assertNotIn('\ufeff', result)

    def test_invalid_or_oversized_files_and_missing_title_rejected(self):
        for payload, topic in [(b'\xff', 'Bài'), (b'x' * 1_000_001, 'Bài'), (b'', 'Bài'), (b'content', '')]:
            with self.subTest(length=len(payload), topic=topic):
                with self.assertRaises(ValueError):
                    saved_markdown_html(payload, 'Ngữ văn', 10, topic)

    def test_explicit_wrong_grade_or_subject_is_not_relabelled(self):
        for text in ('Lớp: 9\nBài học', 'Môn: Hóa học\nBài học'):
            with self.assertRaises(ValueError):
                saved_markdown_html(text.encode('utf-8'), 'Ngữ văn', 10, 'Bài đang chọn')
