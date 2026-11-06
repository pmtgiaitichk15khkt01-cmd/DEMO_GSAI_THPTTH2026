"""Regressions from the actual optimization lesson's named V(x) table."""
import html
import unittest

from services.lesson_export import lesson_body_html
from tests.test_expert_patch_regressions import load_function


def actual_renderer():
    scope = {'html': html, 'sanitize_svg_for_markdown': lambda text: text}
    for name in ('_render_math_html_token', '_parse_bbt_cells_safe',
                 '_normalize_moet_bbt_grid', '_build_svg_bbt_from_rows',
                 'render_pedagogical_lesson_visuals'):
        scope[name] = load_function(name, **scope)
    return scope['render_pedagogical_lesson_visuals']


def table(variable='x', function='V', prime="'"):
    return (f"3. **Bảng biến thiên:**\n| ${variable}$ | $0$ | | $2$ | | $6$ |\n"
            "| :--- | :--- | :---: | :---: | :---: | :--- |\n"
            f"| ${function}{prime}({variable})$ | | $+$ | $0$ | $-$ | |\n"
            f"| ${function}({variable})$ | $0$ | ↗ | $128$ | ↘ | $0$ |\n")


class NamedVariationTableTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.render = staticmethod(actual_renderer())

    def test_names_variables_and_prime_notation_do_not_limit_math_tables(self):
        for grade in range(6, 13):
            for variable, function in (('x', 'V'), ('t', 'Revenue'),
                                       ('h', 'S'), ('u', 'P'), ('θ', 'Φ')):
                for prime in ("'", '′', r'\prime', r'^{\prime}'):
                    with self.subTest(grade=grade, variable=variable,
                                      function=function, prime=prime):
                        result = self.render(table(variable, function, prime), 'Toán học', grade)
                        self.assertIn('<table', result)
                        self.assertIn('<svg', result)
                        self.assertIn('128', result)
                        self.assertNotIn('| :---', result)

    def test_nonmath_and_unrelated_derivative_are_not_misclassified(self):
        source = table()
        for subject in ('Ngữ văn', 'Tiếng Anh', 'Hóa học', 'Vật lý'):
            self.assertEqual(source, self.render(source, subject, 12))
        unrelated = source.replace("$V'(x)$", "$R'(x)$")
        self.assertNotIn('<svg', self.render(unrelated, 'Toán học', 12))

    def test_named_sign_and_two_row_variation_tables(self):
        sign = '| h | 0 | | 2 |\n|---|---|---|---|\n| Profit(h) | 0 | + | 0 |\n'
        self.assertIn('<table', self.render(sign, 'Toán học', 10))
        two_rows = '| u | 0 | | 2 |\n|---|---|---|---|\n| Cost(u) | 0 | ↗ | 128 |\n'
        self.assertIn('<svg', self.render(two_rows, 'Toán học', 10))

    def test_export_recovers_table_after_list_without_touching_code(self):
        source = table()
        result = lesson_body_html(source)
        self.assertEqual(result.count('<table>'), 1)
        self.assertIn('128', result)
        self.assertNotIn('<table', lesson_body_html('```markdown\n' + source + '```'))
        ordinary = '| Mẫu | pH |\n|---|---|\n| Chanh | 3 |\n| Nước | 7 |\n'
        self.assertEqual(lesson_body_html(ordinary).count('<tr>'), 3)
