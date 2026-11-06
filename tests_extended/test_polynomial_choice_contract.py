import copy
import unittest

from services.math_conditions import math_condition_conflict
from services.context_recovery import repair_exam_context


class TestPolynomialChoiceContract(unittest.TestCase):
    def question(self, **overrides):
        value = {'subject':'Toán học','grade':12,'topic':'Hàm số','level':'TH',
                 'q':r'Hàm số nào dưới đây đồng biến trên khoảng $(-\infty;+\infty)$?',
                 'opt':[r'A. $y=x^3+x-5$',r'B. $y=x^3-3x+1$',r'C. $y=-x^3+3x^2-1$',r'D. $y=x^3-3x^2+3x$'],'ans':'A'}
        value.update(overrides)
        return value

    def unique(self):
        value = self.question()
        value['opt'][-1] = r'D. $y=-x^3-x$'
        return value

    def test_live_two_correct_answers_including_isolated_derivative_zero(self):
        question = self.question(); before = copy.deepcopy(question)
        self.assertEqual(math_condition_conflict(question),'polynomial_choice_not_unique')
        self.assertEqual(question,before)

    def test_single_answer_and_wrong_key_are_distinguished(self):
        question = self.unique()
        self.assertEqual(math_condition_conflict(question),'')
        question['ans'] = 'B'
        self.assertEqual(math_condition_conflict(question),'polynomial_monotonic_choice_key_mismatch')
        question['q'] = 'Hàm số nào sau đây nghịch biến trên $R$?'
        question['ans'] = 'D'
        self.assertEqual(math_condition_conflict(question),'')

    def test_unknown_formulas_additional_conditions_and_other_subjects_are_not_guessed(self):
        for question in (self.question(subject='Tiếng Anh'),
                         self.question(q=self.question()['q'] + ' Và có tung độ gốc bằng -5.'),
                         self.question(q='Cho hàm số. Tìm khoảng đồng biến.'),
                         self.question(opt=['A. y=sin(x)','B. y=x','C. y=-x','D. y=x^2'])):
            self.assertEqual(math_condition_conflict(question),'')

    def test_atomic_replacement_keeps_source_and_uses_existing_recovery(self):
        source = {'p1':[self.question()]}; before=copy.deepcopy(source)
        result=repair_exam_context(source,'Toán',12,topics=['Hàm số'],bank_provider=lambda *_:{'p1':[self.unique()]})
        self.assertEqual(source,before)
        self.assertEqual(result['context_recovery']['unresolved'],0)
        self.assertEqual(result['p1'][0]['opt'],self.unique()['opt'])
