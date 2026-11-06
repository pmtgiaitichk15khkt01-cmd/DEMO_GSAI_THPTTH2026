import copy
import unittest

from services.math_conditions import math_condition_conflict
from services.neuro_symbolic_verifier import audit_ai_generated_question_sympy


class TestParameterIntervalContract(unittest.TestCase):
    def question(self, **overrides):
        question = {'q': r'Cho hàm số bậc ba $y=x^3-3mx^2+3(m^2-1)x$. Tìm giá trị thực của tham số $m$ để đồ thị hàm số có hai điểm cực trị nằm về hai phía của trục tung. Nếu có nhiều giá trị, hãy tính tổng của chúng, nếu là một khoảng $(a;b)$ thì nhập giá trị 999. Nếu không có giá trị nào thỏa mãn, nhập 0.', 'ans': '0'}
        question.update(overrides)
        return question

    def test_observed_wrong_key_is_proved_without_rewriting(self):
        question = self.question()
        before = copy.deepcopy(question)
        self.assertEqual(math_condition_conflict(question), 'parameter_interval_code_answer_mismatch')
        self.assertTrue(audit_ai_generated_question_sympy(question)['hallucination_detected'])
        self.assertEqual(question, before)

    def test_matching_key_is_not_flagged_by_this_rule(self):
        self.assertEqual(math_condition_conflict(self.question(ans='999')), '')

    def test_actual_live_optional_note_keeps_the_same_proof(self):
        question = self.question()
        question['q'] += r' Biết rằng yêu cầu bài toán tương đương với phương trình $y\prime=0$ có hai nghiệm trái dấu.'
        # The live note uses y' (no spelled-out prime command).
        question['q'] = question['q'].replace(r'\prime', "'")
        self.assertEqual(math_condition_conflict(question), 'parameter_interval_code_answer_mismatch')

    def test_extra_restrictions_and_other_formats_are_not_guessed(self):
        for question in (
            self.question(subject='Tiếng Anh'),
            self.question(opt=['A. 0','B. 999','C. 1','D. 2'],ans='B'),
            self.question(q=self.question()['q'] + ' Với $m>0$.'),
            self.question(q=self.question()['q'] + ' Tham số là bội của hai.'),
            self.question(q=self.question()['q'].replace('Tìm giá trị thực', 'Biết tham số là bội của hai. Tìm giá trị thực')),
            self.question(q=self.question()['q'].replace('giá trị thực', 'giá trị số nguyên')),
            self.question(q=self.question()['q'].replace('3(m^2-1)x', '3(m^2+1)x')),
            self.question(q=self.question()['q'].replace('999', 'đáp số')),
        ):
            self.assertEqual(math_condition_conflict(question), '')
