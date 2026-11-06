import copy
import unittest
from unittest.mock import Mock

from services.context_recovery import repair_exam_context
from services.math_conditions import math_condition_conflict


class TestRationalIntervalChoice(unittest.TestCase):
    def source(self):
        return dict(subject='Toán học', grade=12, topic='Khảo sát hàm số', level='TH',
            q=r'Hàm số $y=\frac{x+1}{x-2}$ nghịch biến trên khoảng nào dưới đây?',
            opt=[r'A. $(-\infty;2)$ và $(2;+\infty)$', r'B. $(-\infty;+\infty)$',
                 r'C. $(-\infty;2)$', r'D. $\mathbb{R}\setminus\{2\}$'], ans='C')

    def test_live_overlap_is_proved_without_rewriting_options_or_key(self):
        q = self.source()
        before = copy.deepcopy(q)
        self.assertEqual(math_condition_conflict(q), 'rational_interval_choice_not_unique')
        self.assertEqual(q, before)

    def test_single_answer_and_pole_boundary_are_preserved(self):
        q = self.source()
        q['opt'][0] = r'A. $(1;3)$'
        self.assertEqual(math_condition_conflict(q), '')
        # Both strict subintervals are also correct; maximality is not required.
        q['opt'][0] = r'A. $(3;4)$'
        self.assertEqual(math_condition_conflict(q), 'rational_interval_choice_not_unique')

    def test_unknown_conditions_domains_and_other_subject_are_not_guessed(self):
        q = self.source()
        for candidate in (dict(q, q=q['q']+' Với điều kiện bổ sung.'),
                          dict(q, q=q['q'].replace('x+1', 'm*x+1')),
                          dict(q, subject='Tiếng Anh'),
                          dict(q, opt=q['opt'][:3]+['D. Không xác định'])):
            self.assertEqual(math_condition_conflict(candidate), '')

    def test_factored_linear_terms_and_positive_derivative(self):
        q = self.source()
        q['q'] = q['q'].replace('x+1', '2*(x+1)').replace('x-2', '2*(x-2)')
        self.assertEqual(math_condition_conflict(q), 'rational_interval_choice_not_unique')
        q['q'] = q['q'].replace('2*(x+1)', '-2*(x+1)').replace('nghịch biến', 'đồng biến')
        self.assertEqual(math_condition_conflict(q), 'rational_interval_choice_not_unique')
        q['opt'][0] = r'A. $(1;3)$'
        self.assertEqual(math_condition_conflict(q), '')

    def test_existing_bank_recovery_is_atomic_and_uses_no_ai(self):
        source = self.source()
        before = copy.deepcopy(source)
        candidate = self.source()
        candidate['opt'][0] = r'A. $(1;3)$'
        ai = Mock()
        result = repair_exam_context({'p1': [source]}, 'Toán học', 12,
            topics=['Khảo sát hàm số'], bank_provider=lambda *_: {'p1': [candidate]}, ai_generator=ai)
        self.assertEqual(result['context_recovery']['unresolved'], 0)
        self.assertEqual(result['p1'][0]['opt'], candidate['opt'])
        self.assertEqual(source, before)
        ai.assert_not_called()
