import unittest
from services.socratic_context import guiding_question
from data.socratic_anchors import sanitize_socratic_hint


class NumericHintBoundary(unittest.TestCase):
    def test_new_numeric_results_and_explicit_answer_rejected(self):
        for hint in ('Đáp án đúng: B, em hiểu chưa?', 'Em thấy x=77 có đúng không?',
                     'Em thấy x=77.5 có đúng không?', 'Em thấy x=7/2 có đúng không?'):
            with self.subTest(hint=hint):
                self.assertIsNone(guiding_question(hint))
                self.assertNotEqual(sanitize_socratic_hint(hint, q_text='Tìm nghiệm phương trình.'), hint)

    def test_source_equations_and_symbolic_coefficients_preserved(self):
        for formula in ('y=2x+b', 'y=2.5x+b', 'y=2 x+b', r'C=2\pi R'):
            hint = f'Trong biểu thức ${formula}$, em cần đối chiếu đại lượng nào?'
            self.assertEqual(guiding_question(hint), hint)
        hint = 'Với dữ kiện $x=77$, em cần kiểm tra điều kiện nào?'
        self.assertEqual(guiding_question(hint, question_text='Cho $x = 77$. Xét điều kiện.'), hint)
        for word in ('solution', 'therefore'):
            hint = f'Trong đoạn văn, từ {word} đóng vai trò gì?'
            self.assertEqual(guiding_question(hint), hint)
