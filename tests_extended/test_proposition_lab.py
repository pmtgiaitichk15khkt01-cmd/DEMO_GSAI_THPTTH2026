import unittest
from fractions import Fraction
from services.lab_scope import proposition_lab_request, evaluate_proposition


class PropositionLabTests(unittest.TestCase):
    def test_intent_and_actual_coefficients_control_routing(self):
        command = 'Mệnh đề chứa biến P(x): x^2-3x+2=0'
        data = proposition_lab_request(command, 'Toán học')
        self.assertEqual([data[k] for k in ('a', 'b', 'c')], ['1', '-3', '2'])
        self.assertEqual(proposition_lab_request(command.replace('x^2-3x+2', '2x^2+1x-3'), 'Toán học')['a'], '2')
        self.assertIsNone(proposition_lab_request('Vẽ parabol x^2-3x+2=0', 'Toán học'))
        self.assertIsNone(proposition_lab_request(command, 'Ngữ văn'))
        self.assertIsNone(proposition_lab_request('Mệnh đề sin(x)=0', 'Toán học'))
        # Unsupported syntax must not be truncated into different coefficients.
        for expression in ('1/2x^2-3x+2=0', 'sin(x)^2-3x+2=0', 'a*x^2-3x+2=0'):
            self.assertIsNone(proposition_lab_request('Mệnh đề P(x): ' + expression, 'Toán học'))

    def test_substitution_is_exact_and_input_is_not_executed(self):
        data = proposition_lab_request('Mệnh đề x^2-3x+2=0', 'Toán học')
        for x, truth in [('0', False), ('1', True), ('2', True), ('3', False), ('-1', False)]:
            self.assertEqual(evaluate_proposition(data, x)[1], truth)
        self.assertEqual(evaluate_proposition(data, '1/2')[0], Fraction(3, 4))
        for value in ('__import__("os")', 'nan', '', '1/0'):
            with self.assertRaises((ValueError, ZeroDivisionError)):
                evaluate_proposition(data, value)
