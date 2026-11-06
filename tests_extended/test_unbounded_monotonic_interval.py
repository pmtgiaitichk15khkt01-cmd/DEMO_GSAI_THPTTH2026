import copy
import unittest
from unittest.mock import Mock

from services.context_recovery import repair_exam_context
from services.math_conditions import math_condition_conflict


class TestUnboundedMonotonicInterval(unittest.TestCase):
    def source(self):
        return dict(subject='Toán học', grade=12, topic='Khảo sát hàm số', level='VD',
            q=r"Cho hàm số $f(x)$ có đạo hàm $f'(x) = (x-1)(x-2)^2(x-3)^3$. Hỏi hàm số $f(x)$ đồng biến trên khoảng $(a; b)$ tối đại. Tính giá trị $b-a$ của khoảng đó nằm trong vùng $x > 2$.", ans='2')

    def test_live_infinite_interval_is_not_assigned_a_finite_length(self):
        q = self.source()
        before = copy.deepcopy(q)
        self.assertEqual(math_condition_conflict(q), 'requested_interval_length_is_infinite')
        self.assertEqual(q, before)

    def test_finite_interval_and_explicit_infinite_answer_are_preserved(self):
        q = self.source()
        self.assertEqual(math_condition_conflict(dict(q, ans=r'+\infty')), '')
        q['q'] = q['q'].replace('(x-3)^3', '(3-x)^3')
        q['ans'] = '1'
        self.assertEqual(math_condition_conflict(q), '')

    def test_extra_conditions_wrong_direction_subject_and_unknown_roots_are_not_guessed(self):
        q = self.source()
        for candidate in (dict(q, q=q['q']+' Với điều kiện bổ sung.'),
                          dict(q, q=q['q'].replace('x > 2', 'x < 2')),
                          dict(q, subject='Vật lí'),
                          dict(q, q=q['q'].replace('(x-1)', '(x-m)')),
                          dict(q, q=q['q'].replace('(x-1)', '(x^2-2)'))):
            self.assertEqual(math_condition_conflict(candidate), '')

    def test_even_zero_does_not_split_a_maximal_increasing_interval(self):
        q = self.source()
        q['q'] = q['q'].replace('(x-1)(x-2)^2(x-3)^3', '(x-3)^2')
        self.assertEqual(math_condition_conflict(q), 'requested_interval_length_is_infinite')
        q['q'] = q['q'].replace('(x-3)^2', 'x^2+1')
        self.assertEqual(math_condition_conflict(q), 'requested_interval_length_is_infinite')
        q['q'] = q['q'].replace('x^2+1', '-x^2-1')
        self.assertEqual(math_condition_conflict(q), '')

    def test_bank_replacement_preserves_source_without_ai(self):
        q = self.source()
        before = copy.deepcopy(q)
        valid = dict(q, q=q['q'].replace('(x-3)^3', '(3-x)^3'), ans='1')
        ai = Mock()
        result = repair_exam_context({'p3': [q]}, 'Toán học', 12,
            topics=['Khảo sát hàm số'], bank_provider=lambda *_: {'p3': [valid]}, ai_generator=ai)
        self.assertEqual(result['context_recovery']['unresolved'], 0)
        self.assertEqual(result['p3'][0]['q'], valid['q'])
        self.assertEqual(q, before)
        ai.assert_not_called()
