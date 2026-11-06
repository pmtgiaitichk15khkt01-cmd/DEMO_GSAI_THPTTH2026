import unittest
import xml.etree.ElementTree as ET

import sympy as sp

from services.function_visuals import (X, explicit_function_visuals, function_model,
                                      graph_svg, variation_svg, with_function_visuals)
from services.lesson_export import build_lesson_html


class FunctionVisualsTests(unittest.TestCase):
    def test_root_equation_legend_uses_katex_fraction_and_powers(self):
        graph = graph_svg(function_model('x^3-3*x^2-3/2'))
        root = ET.fromstring(graph)
        spans = [e for e in root.iter() if e.attrib.get('class') == 'lesson-math']
        self.assertEqual(len(spans), 1)
        self.assertEqual(spans[0].attrib['data-tex'], r'x^{3} - 3 x^{2} - \frac{3}{2} = 0')
        self.assertIn('nghiệm thực phân biệt', ''.join(root.itertext()))

    def test_irrational_coordinates_are_exact_in_graph_and_all_exports(self):
        for source in ('x^3-2x', '(x*x+2)/x', 'x^3-3x+1'):
            with self.subTest(source=source):
                graph = graph_svg(function_model(source, strict=True))
                self.assertNotIn('≈', graph)
                self.assertNotIn('CRootOf', ''.join(ET.fromstring(graph).itertext()))
                self.assertIn('data-axis-coordinate=', graph)
                self.assertIn('data-graph-label=', graph)
                for style in ('handwritten', 'color', 'monochrome'):
                    page = build_lesson_html('Toán học', 12, 'y='+source+'.', 'Bài học.', style)
                    self.assertIn(graph, page)
        graph = graph_svg(function_model('x^3-3x+1'))
        self.assertIn('α₁', graph)
        self.assertIn('nghiệm thực phân biệt', graph)
        self.assertIn('√', graph_svg(function_model('(x*x+2)/x')))

    def test_cubic_all_derivative_discriminants_and_both_leading_signs(self):
        for source, roots, signs in [('x^3-3x+1', [-1, 1], [1, -1, 1]),
                                    ('x^3+1', [0], [1, 1]),
                                    ('x^3+3x+1', [], [1])]:
            for sign in (1, -1):
                with self.subTest(source=source, sign=sign):
                    model = function_model(f'{sign}*({source})')
                    self.assertEqual(model['stationary'], roots)
                    self.assertEqual(model['signs'], [sign*s for s in signs])
                    self.assertEqual(model['limits'][0], (-sign*sp.oo,)*2)
                    self.assertEqual(model['limits'][-1], (sign*sp.oo,)*2)
                    ET.fromstring(variation_svg(model))
                    ET.fromstring(graph_svg(model))

    def test_rational11_signs_limits_and_cancellation_domain(self):
        for source, signs, limits in [('(2x+1)/(x-1)', [-1, -1], (-sp.oo, sp.oo)),
                                     ('(2x-3)/(x-1)', [1, 1], (sp.oo, -sp.oo)),
                                     ('(2x-2)/(x-1)', [0, 0], (2, 2)),
                                     ('0/(x-1)', [0, 0], (0, 0))]:
            with self.subTest(source=source):
                model = function_model(source)
                self.assertEqual(model['excluded'], (1,))
                self.assertEqual(model['signs'], signs)
                self.assertEqual(model['limits'][1], limits)
                graph = graph_svg(model)
                self.assertEqual(graph.count('<polyline '), 2)
                self.assertEqual('r="4"' in graph, limits[0] == limits[1])

    def test_rational21_all_remainder_cases_and_both_signs(self):
        for source, roots, signs, limits in [
            ('(x^2-2x+2)/(x-1)', [0, 2], [1, -1, -1, 1], (-sp.oo, sp.oo)),
            ('(x^2-2x)/(x-1)', [], [1, 1], (sp.oo, -sp.oo)),
            ('(x^2-2x+1)/(x-1)', [], [1, 1], (0, 0)),
        ]:
            for sign in (1, -1):
                with self.subTest(source=source, sign=sign):
                    model = function_model(f'{sign}*({source})')
                    self.assertEqual(sorted(model['stationary']), roots)
                    self.assertEqual(model['signs'], [sign*s for s in signs])
                    self.assertEqual(model['limits'][model['points'].index(1)], tuple(sign*v for v in limits))
                    self.assertEqual(graph_svg(model).count('<polyline '), 2)
                    self.assertIn('∥' if limits[0] != limits[1] else '×', variation_svg(model))

    def test_exact_fractions_and_degenerate_polynomial_cases(self):
        for source, roots, signs in [('(x*x+1)/2', [0], [-1, 1]),
                                     ('-x*x+1', [0], [1, -1]),
                                     ('2x+1', [], [1]), ('-2x+1', [], [-1]),
                                     ('3', [], [0]), ('0', [], [0])]:
            model = function_model(source)
            self.assertEqual(model['stationary'], roots)
            self.assertEqual(model['signs'], signs)
            ET.fromstring(graph_svg(model))
        self.assertIn('1/2', variation_svg(function_model('(x*x+1)/2')))

    def test_poles_are_not_joined_and_holes_are_not_vertical_asymptotes(self):
        for source in ['(2x+1)/(x-1)', '(x*x+1)/x', '1/x', '-1/x']:
            model = function_model(source)
            self.assertEqual(graph_svg(model).count('<polyline '), 2)
            self.assertIn('∥', variation_svg(model))
        hole = function_model('(x*x-1)/(x-1)')
        self.assertIn('×', variation_svg(hole))
        self.assertNotIn('∥', variation_svg(hole))
        self.assertNotIn('Tiệm cận:', graph_svg(hole))

    def test_reject_ambiguous_unsafe_or_unsupported_input(self):
        for source in ['__import__("os")', 'x**1000', '1/0', '1/(x*x+1)', 'x/(x-1)+1/(x-2)']:
            with self.subTest(source=source), self.assertRaises((ValueError, SyntaxError)):
                function_model(source)
        for topic in ['Hàm bậc ba', 'y=x+1 và y=x-1', 'y=sin(x)', 'y=<script>', 'y=1e-3x', 'y=x sin(x)']:
            self.assertEqual(explicit_function_visuals(topic), '')

    def test_latex_fraction_and_powers_match_ascii_model(self):
        self.assertEqual(explicit_function_visuals(r'y=\frac{x^{2}-2x+2}{x-1}.'),
                         explicit_function_visuals('y=(x^2-2x+2)/(x-1).'))

    def test_generic_topic_requires_one_unambiguous_example_outside_code(self):
        self.assertIn('verified-function-visuals', with_function_visuals('<p>Bài học</p>', 'Khảo sát', r'Ví dụ $y=x^3-3x+1$.'))
        for lesson in [r'$y=x+1$ và $y=x-1$', '```python\ny=x+1\n```']:
            self.assertEqual(with_function_visuals('<p>Bài học</p>', 'Khảo sát', lesson), '<p>Bài học</p>')

    def test_each_supported_worked_function_gets_its_own_graph(self):
        body = '<p>Nội dung nguồn</p>'
        result = with_function_visuals(body, 'Khảo sát',
            r'Ví dụ $y=x^3-3x+1$. Ví dụ $y=(x^2+2)/(x-1)$.')
        self.assertTrue(result.startswith(body))
        self.assertEqual(result.count('class="verified-function-visuals"'), 2)
        self.assertEqual(result.count('aria-label="Đồ thị y='), 2)
        self.assertIn('data-projection="true"', result)

    def test_sgk_graph_shows_extrema_center_intercepts_and_projections(self):
        graph = graph_svg(function_model('x^3-3x+1', strict=True))
        self.assertEqual(graph.count('data-projection="true"'), 3)
        self.assertEqual(graph.count('data-point="Ox"'), 3)
        self.assertIn('data-point="Oy I"', graph)
        self.assertIn('I(0; 1)', graph)
        graph = graph_svg(function_model('(2x+1)/(x-1)', strict=True))
        self.assertIn('I(1; 2)', graph)
        self.assertIn('(−1/2; 0)', graph)
        self.assertIn('(0; −1)', graph)
        self.assertEqual(graph.count('data-projection="true"'), 1)
        graph = graph_svg(function_model('(x*x-2x+2)/(x-1)', strict=True))
        self.assertEqual(graph.count('data-projection="true"'), 3)
        self.assertNotIn('data-point="Ox"', graph)
        self.assertIn('I(1; 0)', graph)
        self.assertIn('data-point="Cực trị Oy"', graph)

    def test_sgk_gate_rejects_degenerate_inputs_instead_of_accepting_them(self):
        for source in ['(2x-2)/(x-1)', '0/(x-1)', '(x*x-1)/(x-1)', '(x*x+1)/2', '2x+1', '3', '0']:
            with self.subTest(source=source):
                self.assertIn('data-function-rejected', explicit_function_visuals('y='+source+'.'))
                self.assertNotIn('<svg', explicit_function_visuals('y='+source+'.'))
        for source in ['x^3+1', '(2x+1)/(x-1)', '1/x', '(x*x-2x+2)/(x-1)']:
            self.assertIn('<svg', explicit_function_visuals('y='+source+'.'))
        self.assertIn('data-function-rejected', explicit_function_visuals('Hàm 2/1 y=(0*x^2+2x+1)/(x-1).'))
        self.assertIn('data-function-rejected', explicit_function_visuals('Hàm 1/1 y=(x^2+1)/(x-1).'))

    def test_exact_root_equation_has_native_typesetting_without_javascript(self):
        graph = graph_svg(function_model('x^3-3x^2-3/2', strict=True))
        self.assertIn('<math xmlns="http://www.w3.org/1998/Math/MathML">', graph)
        self.assertIn('<mfrac>', graph)
        self.assertIn('<msup>', graph)
        self.assertIn('class="lesson-math"', graph)
        self.assertIn('data-tex=', graph)

    def test_variation_extremum_values_are_simplified_before_layout(self):
        from services.function_visuals import variation_svg
        table = variation_svg(function_model('(x^2+2)/(x-1)', strict=True))
        self.assertIn('2 − 2·√(3)', table)
        self.assertIn('2 + 2·√(3)', table)
        self.assertNotIn('(1 − √(3))^2', table)

    def test_svg_numeric_math_labels_have_native_radicals_and_fractions(self):
        from services.function_visuals import _label
        radical = _label(100, 100, 'I(1 − √(3); 2 − 2·√(3))')
        self.assertIn('<msqrt>', radical)
        self.assertIn('data-math-label="true"', radical)
        fraction = _label(100, 100, '−2/3')
        self.assertIn('<mfrac>', fraction)
        self.assertNotIn('<math', _label(100,100,'not a mathematical expression'))

    def test_all_styles_share_bbt_and_graph_and_do_not_change_original_text(self):
        lesson = "Nội dung giữ nguyên.\n\n| x | -∞ | 1 | +∞ |\n|---|---|---|---|\n| y′ | - | || | - |\n| y | 2 | sai | 2 |"
        for style in ('handwritten', 'color', 'monochrome'):
            page = build_lesson_html('Toán học', 12, 'Khảo sát y=(2x+1)/(x-1).', lesson, style)
            self.assertIn('Nội dung giữ nguyên.', page)
            self.assertEqual(page.count('class="verified-function-visuals"'), 1)
            self.assertIn('aria-label="Đồ thị y=', page)
            self.assertIn('aria-label="Bảng biến thiên y=', page)
        self.assertNotIn('<section class="verified-function-visuals"', build_lesson_html('Tin học', 12, 'y=x^3', 'HTML'))
        self.assertEqual(with_function_visuals('<p>Không đổi</p>', 'Chủ đề chung'), '<p>Không đổi</p>')


if __name__ == '__main__':
    unittest.main()
