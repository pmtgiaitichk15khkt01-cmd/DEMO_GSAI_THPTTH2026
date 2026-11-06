import unittest

from services.lesson_export import lesson_body_html
from services.text_boundaries import polya_display_markdown, student_essay_text


class PolyaDisplayTests(unittest.TestCase):
    source = ('Câu 1. Em hãy kể một trải nghiệm.\n\n'
              'Bước 1: Tìm hiểu đề: Em kể điều gì? Bước 2: Lập kế hoạch: Chọn trình tự. '
              'Bước 3: Thực hiện kế hoạch: Tự viết bài. Bước 4: Kiểm tra và nhìn lại: Tự sửa.')

    def test_collapsed_real_world_layout_becomes_four_separate_paragraphs(self):
        result = student_essay_text(self.source)
        for n in range(1, 5):
            self.assertIn(f'\n\n**Bước {n}:', result)
        self.assertIn('Em kể điều gì?', result)
        self.assertIn('Tự viết bài.', result)
        self.assertEqual(student_essay_text(result), result)
        page = lesson_body_html(self.source)
        for n in range(1, 5):
            self.assertIn(f'<p><strong>Bước {n}:', page)

    def test_bold_list_layout_stays_readable_without_duplicate_markers(self):
        text = ('**Bước 1: Tìm hiểu đề:** Đọc đề.\n'
                '- **Bước 2: Lập kế hoạch:** Tự chọn.\n'
                '- **Bước 3: Thực hiện kế hoạch:** Tự làm.\n'
                '- **Bước 4: Kiểm tra và nhìn lại:** Đối chiếu.')
        result = polya_display_markdown(text)
        self.assertEqual(result.count('**Bước '), 4)
        self.assertNotIn('- **Bước', result)
        self.assertEqual(polya_display_markdown(result), result)

    def test_observed_bold_period_heading_leaves_no_markdown_debris(self):
        text = '*   **Bước 1: Tìm hiểu đề.** Đọc đúng ngữ cảnh.\n*   **Bước 2: Lập kế hoạch.** Giữ nội dung.'
        result = polya_display_markdown(text)
        self.assertNotIn('.**', result)
        self.assertIn('**Bước 1: Tìm hiểu đề:** Đọc đúng ngữ cảnh.', result)
        self.assertIn('\n\n**Bước 2: Lập kế hoạch:** Giữ nội dung.', result)
        self.assertEqual(polya_display_markdown(result), result)
        rendered = lesson_body_html(result)
        self.assertNotIn('.**', rendered)
        self.assertIn('Đọc đúng ngữ cảnh.', rendered)

    def test_code_math_and_mentions_are_not_rewritten(self):
        protected = ('```text\nBước 1: Tìm hiểu đề: sample\n```\n'
                     '`Bước 2: Lập kế hoạch: sample`\n$ x=1 $\n'
                     'Em đối chiếu Bước 3 trong quy trình đã học.')
        self.assertEqual(polya_display_markdown(protected), protected)
