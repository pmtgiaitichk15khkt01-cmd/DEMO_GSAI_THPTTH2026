import json
import unittest
from html.parser import HTMLParser

from services.lesson_export import lesson_body_html, handwritten_prompt


class Cells(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows = []

    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            self.rows.append([])
        elif tag in ('td', 'th'):
            self.rows[-1].append('')

    def handle_data(self, data):
        if self.rows and self.rows[-1]:
            self.rows[-1][-1] += data


class VariationDiscontinuityTests(unittest.TestCase):
    def test_two_limits_stay_in_one_cell_and_columns_remain_aligned(self):
        source = "| x | -∞ | | 1 | | +∞ |\n|---|---|---|---|---|---|\n| y' | | - | || | - | |\n| y | +∞ | ↘ | -∞ || +∞ | ↘ | -∞ |\n"
        parser = Cells()
        parser.feed(lesson_body_html(source))
        self.assertEqual([len(row) for row in parser.rows], [6, 6, 6])
        self.assertEqual(parser.rows[2][3].strip(), '-∞ || +∞')
        self.assertEqual(parser.rows[1][3].strip(), '||')

    def test_fenced_code_double_pipe_is_not_changed(self):
        source = '```text\n| expression | a || b |\n```'
        self.assertIn('a || b', lesson_body_html(source))
        self.assertNotIn(r'\|\|', lesson_body_html(source))

    def test_downloadable_style_prompt_requires_transparent_variation_panel(self):
        prompt = json.loads(handwritten_prompt('Toán học', 12, 'BBT', 'Nội dung gốc'))
        self.assertEqual(prompt['content'], 'Nội dung gốc')
        self.assertTrue(any('transparent panels' in rule for rule in prompt['rules']))

    def test_inline_teaching_steps_and_bullets_break_without_changing_math(self):
        body = lesson_body_html("**Bước 1: Tập xác định:** $D=R$. **Bước 2: Sự biến thiên:** * Tính $y'$. * Lập bảng.")
        self.assertIn('</p>\n<p><strong>Bước 2:', body)
        self.assertEqual(body.count('<li>'), 2)
        self.assertIn('data-tex="y&#x27;"', body)

    def test_multiple_examples_replace_only_their_scoped_source_table(self):
        from services.function_visuals import with_function_visuals
        lesson = r"$y=\frac{x^2-x+1}{x-1}$." + "\n\n| x | -∞ | 0 | 1 | 2 | +∞ |\n|---|---|---|---|---|---|\n| y' | + | 0 | || - | 0 | + |\n| y | -∞ | -1 | -∞ || +∞ | 3 | +∞ |\n\n" + r"Luyện tập $y=\frac{x^2+2*x+2}{x+1}$."
        result = with_function_visuals(lesson_body_html(lesson), 'Hàm phân thức bậc 2/1', lesson)
        self.assertNotIn('<table', result)
        self.assertEqual(result.count('class="verified-function-visuals"'), 2)
