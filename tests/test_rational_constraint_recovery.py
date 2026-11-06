import copy
import unittest
from services.context_recovery import recover_visual, repair_exam_context
from services.math_conditions import math_condition_conflict


class TestRationalConstraintRecovery(unittest.TestCase):
    def question(self):
        return {"q": r"Cho hàm số $y = \frac{ax+b}{cx+d}$ có đồ thị như hình vẽ bên. Biết đồ thị đi qua điểm $(0; 1)$ và có đường tiệm cận đứng $x = 1$, đường tiệm cận ngang $y = 2$.",
                "stmts": [{"t": "Hàm số đã cho nghịch biến trên từng khoảng xác định.", "a": False}]}

    def test_exact_constraints_recover_model_without_revealing_formula(self):
        q = self.question(); before = copy.deepcopy(q)
        r = recover_visual(q, 'Toán', 12)
        self.assertEqual(r.get('f'), {'type': 'func_1_1', 'a': 2.0, 'b': -1.0, 'c': 1.0, 'd': -1.0})
        self.assertEqual(r['q'], q['q'])
        self.assertEqual(q, before)
        self.assertEqual(math_condition_conflict(r), 'rational_monotonic_statement_key_mismatch')
        r['stmts'][0]['a'] = True
        self.assertEqual(math_condition_conflict(r), '')

    def test_missing_duplicate_and_degenerate_constraints_are_not_guessed(self):
        q = self.question()
        for text in (q['q'].replace('$(0; 1)$', '$(0; m)$'),
                     q['q'].replace('$(0; 1)$', '$(1; 1)$'),
                     q['q'].replace('$(0; 1)$', '$(0; 2)$'),
                     q['q'] + ' Tiệm cận đứng $x=3$.'):
            self.assertNotIn('f', recover_visual({'q': text}, 'Toán', 12))
        self.assertEqual(recover_visual(q, 'Vật lí', 12), q)

    def test_unknown_statement_is_not_rejected(self):
        q = recover_visual(self.question(), 'Toán', 12)
        q['stmts'][0]['t'] = 'Hàm số không nghịch biến trên toàn bộ miền xác định.'
        self.assertEqual(math_condition_conflict(q), '')

    def test_translated_point_and_increasing_model(self):
        q = self.question()
        q['q'] = q['q'].replace('$(0; 1)$', '$(3; 1)$')
        q['stmts'][0] = {'t': 'Hàm số đã cho đồng biến trên từng khoảng xác định.', 'a': True}
        r = recover_visual(q, 'Toán', 12)
        self.assertEqual(r['f'], {'type': 'func_1_1', 'a': 2.0, 'b': -4.0, 'c': 1.0, 'd': -1.0})
        self.assertEqual(math_condition_conflict(r), '')
        r['stmts'][0]['a'] = False
        self.assertEqual(math_condition_conflict(r), 'rational_monotonic_statement_key_mismatch')

    def test_existing_visual_and_solution_text_are_not_recovery_sources(self):
        q = self.question()
        q['f'] = {'type': 'func_1_1', 'a': 3, 'b': 4, 'c': 1, 'd': -2}
        self.assertEqual(recover_visual(q, 'Toán', 12), q)
        q = self.question()
        source = q['q']
        q['q'] = r'Cho hàm số $y=\\frac{ax+b}{cx+d}$ có đồ thị như hình bên.'
        q['explain'] = source
        self.assertNotIn('f', recover_visual(q, 'Toán', 12))

    def test_wrong_key_can_be_replaced_by_complete_valid_candidate_with_audit(self):
        from unittest.mock import Mock
        q = self.question()
        q['stmts'].extend([{'t': 'Tiệm cận đứng là x=1.', 'a': True},
                           {'t': 'Tiệm cận ngang là y=2.', 'a': True},
                           {'t': 'Đồ thị đi qua điểm (0;1).', 'a': True}])
        source = {'p2': [q]}
        before = copy.deepcopy(source)
        candidate = copy.deepcopy(q)
        candidate.update(subject='Toán học', grade=12, topic='Hàm số')
        candidate['stmts'][0]['a'] = True
        generator = Mock(return_value={'replacement_question': candidate})
        result = repair_exam_context(source, 'Toán', 12, topics=['Hàm số'], ai_generator=generator)
        self.assertEqual(result['context_recovery']['unresolved'], 0)
        generator.assert_called_once()
        self.assertEqual(source, before)
        self.assertTrue(result['p2'][0]['stmts'][0]['a'])
        self.assertEqual(result['p2'][0]['replacement_audit']['origin'], 'ai_replacement')
        self.assertFalse(result['p2'][0]['replacement_audit']['academic_verified'])
