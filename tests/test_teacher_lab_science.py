import ast
import math
from pathlib import Path
import unittest

from services.lab_scope import resolve_preset_lab, ideal_ph, ammonia_equilibrium, lesson_context_examples, logarithm_model, preset_lab_label


class TeacherScienceTests(unittest.TestCase):
    def test_function_formula_keeps_exact_coefficients_and_normalizes_signs(self):
        from services.lab_scope import function_formula_latex
        self.assertEqual(function_formula_latex([1, 0, -2, 1]), 'y = x^{3} - 2 x + 1')
        self.assertEqual(function_formula_latex([1, -2, 2], [1, -1]),
                         r'y = \frac{x^{2} - 2 x + 2}{x - 1}')
        self.assertIn(r'\frac{x}{2}', function_formula_latex([0.5, 0]))

    def test_ph_reference_cases_and_water_ion_product(self):
        for log_h, expected in [(-3, 3), (-7, 7), (-11, 11), (-2.5, 2.5)]:
            state = ideal_ph(log_h)
            self.assertEqual(state['ph'], expected)
            self.assertAlmostEqual(state['h']*state['oh']/1e-14, 1)
        for value in (1, -15, math.nan, math.inf):
            with self.assertRaises(ValueError):
                ideal_ph(value)

    def test_ammonia_satisfies_mass_action_and_conservation(self):
        for temp in (100, 226.85, 450, 700):
            for pressure in (10, 200, 300):
                result = ammonia_equilibrium(temp, pressure)
                x = result['extent']
                n2, h2, nh3 = 1-x, 3*(1-x), 2*x
                self.assertAlmostEqual(2*n2+nh3, 2)
                self.assertAlmostEqual(2*h2+3*nh3, 6)
                total = n2+h2+nh3
                quotient = (nh3/total*pressure)**2/((n2/total*pressure)*(h2/total*pressure)**3)
                self.assertAlmostEqual(quotient/result['kp'], 1, places=8)
                self.assertTrue(0 < result['conversion'] < 100)
        self.assertGreater(ammonia_equilibrium(400, 200)['extent'], ammonia_equilibrium(500, 200)['extent'])
        self.assertGreater(ammonia_equilibrium(450, 200)['extent'], ammonia_equilibrium(450, 100)['extent'])
        self.assertEqual(ammonia_equilibrium(450, 100)['kp'], ammonia_equilibrium(450, 200)['kp'])
        # Independent room-temperature reference from tabulated Hf/S values.
        self.assertTrue(4e5 < ammonia_equilibrium(25, 1)['kp'] < 7e5)

    def test_grade_examples_use_selected_topics_or_neutral_fallback(self):
        text = lesson_context_examples('Toán', 6, ['Chuyên đề 1: Phân số', 'Chuyên đề 2: Số thập phân'])
        self.assertIn('Phân số', text)
        self.assertNotIn('Tích phân', text)
        self.assertNotIn('IELTS', lesson_context_examples('Tiếng Anh', 6, []))

    def test_ph_presets_do_not_add_seven_to_the_definition(self):
        for subject, label in [('Hóa học', 'Hàm số Lôgarit & Thang đo pH'),
                               ('Khoa học tự nhiên', 'Thang đo pH & Axit - Bazơ (KHTN)')]:
            payload = {'type': 'func_log', 'base': 10.0, 'k': -1.0, 'c': 7.0}
            actual = resolve_preset_lab(subject, label, payload)
            self.assertEqual(actual['type'], 'chem_ph')
            self.assertEqual(payload['c'], 7.0, 'Do not mutate the existing library')

    def test_logarithm_parameters_are_not_silently_changed(self):
        tree = ast.parse(Path('app.py').read_text(encoding='utf-8'))
        branch = next(node for node in ast.walk(tree) if isinstance(node, ast.If)
                      and ast.unparse(node.test) == "dtype == 'func_log'")
        # Check the actual renderer as well as the helper: no hidden numeric
        # replacement may precede validation of the user's slider values.
        numeric_overrides = [node for node in ast.walk(branch)
                             if isinstance(node, ast.Assign)
                             and isinstance(node.value, ast.Constant)
                             and isinstance(node.value.value, (int, float))
                             and any(isinstance(target, ast.Name) and target.id in ('fa', 'fk')
                                     for target in node.targets)]
        self.assertEqual(numeric_overrides, [])
        with self.assertRaisesRegex(ValueError, 'khác 1'):
            logarithm_model(1, 1, 0)
        self.assertEqual(logarithm_model(2, 0, 3)['behavior'], 'constant')
        self.assertFalse(logarithm_model(2, 0, 3)['has_vertical_asymptote'])
        self.assertEqual(logarithm_model(2, -1, 3)['behavior'], 'decreasing')
        self.assertEqual(logarithm_model(.5, -1, 3)['behavior'], 'increasing')
        self.assertAlmostEqual(logarithm_model(1, 1, 0, natural=True)['base'], math.e)

    def test_presets_do_not_claim_models_they_do_not_render(self):
        source = Path('services/lab_scope.py').read_text(encoding='utf-8')
        self.assertIn('không mô phỏng mã hóa RSA', source)
        self.assertIn('không mô phỏng mạch RLC', source)
        self.assertIn('không phải mô hình mạng tinh thể', source)
        self.assertIn('chỉ khi trội hoàn toàn', Path('app.py').read_text(encoding='utf-8'))
        self.assertIn('không mô phỏng mã hóa RSA', preset_lab_label('Hàm số Mũ & Mã hóa dữ liệu (RSA)', 'Tin học', 10))
        self.assertIn('không phải mô hình mạng tinh thể', preset_lab_label('Không gian Oxyz (Mô hình mạng tinh thể)', 'Hóa học', 11))
        self.assertIn('không mô phỏng mạch RLC', preset_lab_label('Mạch điện xoay chiều RLC & Dao động', 'Công nghệ', 11))
        self.assertIn('chỉ xét trội hoàn toàn', preset_lab_label('Quy luật di truyền Mendel (KHTN)', 'Khoa học tự nhiên', 8))


if __name__ == '__main__':
    unittest.main()
