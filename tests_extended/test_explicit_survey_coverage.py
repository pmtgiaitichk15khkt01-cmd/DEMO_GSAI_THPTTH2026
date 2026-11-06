import unittest
from services.curriculum_policy import validate_explicit_survey_coverage as check


class ExplicitSurveyCoverage(unittest.TestCase):
    topic = 'Khảo sát cả ba dạng hàm cơ bản'
    examples = r'$y=x^3-3x+1$. $y=\frac{2x-1}{x-1}$. $f(x)=\frac{x^2+1}{x-1}$.'

    def test_three_numeric_examples_preserved(self):
        self.assertEqual(check(self.examples, 'Toán', 12, self.topic), self.examples)
        self.assertEqual(check(self.examples.replace('y=', 'y=f(x)='), 'Toán', 12, self.topic), self.examples.replace('y=', 'y=f(x)='))

    def test_exercises_generic_or_cancelled_forms_do_not_count(self):
        for text in (r'$y=x^3-3x$.', r'$y=ax^3+bx^2+cx+d$',
                     self.examples.replace(r'\frac{x^2+1}{x-1}', r'\frac{x^2-1}{x-1}'),
                     '### PHẦN 1: BÀI HỌC\nBa dạng.\n### PHẦN 2: BÀI TẬP\n'+self.examples):
            with self.subTest(text=text), self.assertRaises(ValueError):
                check(text, 'Toán', 12, self.topic)

    def test_other_subjects_grades_and_single_form_unchanged(self):
        for subject, grade, topic in [('Vật lý',12,self.topic), ('Toán',10,self.topic), ('Toán',12,'Khảo sát hàm bậc ba')]:
            self.assertEqual(check('Bài riêng',subject,grade,topic),'Bài riêng')

    def test_actual_gate_checks_before_publishing(self):
        import ast
        from pathlib import Path
        tree = ast.parse(Path('app.py').read_text(encoding='utf-8'))
        gate = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'station1_master_sovereign_brain_gate')
        calls = [n.func.id for n in ast.walk(gate) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)]
        self.assertIn('validate_explicit_survey_coverage', calls)
