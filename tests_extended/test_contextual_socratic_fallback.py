import unittest

from data.socratic_anchors import sanitize_socratic_hint
from services.academic_context import subjects_for_grade
from services.socratic_context import math_context_question


AXIS = 'Cho hàm số $y=-x^3+3x^2-4$. Đồ thị hàm số cắt trục tung tại điểm có tung độ bằng:'
MINIMUM = 'Cho hàm số $f(x)=x^3-3x+1$. Tọa độ điểm cực tiểu của đồ thị hàm số là:'


class TestContextualSocraticFallback(unittest.TestCase):
    def test_live_axis_question_gets_coordinate_guidance_without_solution(self):
        result = sanitize_socratic_hint('', 'C', AXIS, ['A. 0','B. 3','C. -4','D. 2'])
        self.assertIn('trục tung', result)
        self.assertIn('hoành độ', result)
        self.assertIn('tung độ', result)
        self.assertTrue(result.endswith('?'))
        for leaked in ('-4', 'x=0', 'x = 0', 'đáp án', 'Bước 1', 'SGK'):
            self.assertNotIn(leaked, result)

    def test_live_minimum_coordinates_not_replaced_by_counting_extrema(self):
        result = sanitize_socratic_hint('', 'A', MINIMUM, ['A. (1;-1)','B. (-1;3)','C. (0;1)','D. (1;1)'])
        self.assertIn('cực tiểu', result)
        self.assertIn('hai tọa độ', result)
        self.assertNotIn('đếm', result)
        self.assertNotIn('1', result)
        self.assertNotIn('Định hướng tư duy Socratic', result)

    def test_parameter_monotonicity_on_real_line_guides_parameter_then_integer_count(self):
        question = 'Có bao nhiêu giá trị nguyên của tham số m để hàm số y=1/3x^3-mx^2+4x+3 đồng biến trên R?'
        result = sanitize_socratic_hint('', 'D', question, ['A. 2','B. 3','C. 4','D. 5'])
        for real_notation in (r'$\mathbb{R}$', r'\mathbb R', 'ℝ', 'tập R'):
            variant = sanitize_socratic_hint('', 'D', question.replace('trên R', 'trên '+real_notation))
            self.assertIn('tham số', variant, real_notation)
        self.assertIn('tham số', result)
        self.assertIn('mọi', result)
        self.assertIn('nguyên', result)
        self.assertTrue(result.endswith('?'))
        for answer in ('m²', 'm^2', '≤4', '5', 'đáp án'):
            self.assertNotIn(answer, result)
        self.assertIsNone(math_context_question('Tìm tham số để hàm số đồng biến trên (1;2).'))

    def test_maximum_uses_requested_kind(self):
        result = math_context_question(MINIMUM.replace('cực tiểu','cực đại'))
        self.assertIn('cực đại', result)
        self.assertNotIn('cực tiểu', result)

    def test_valid_separate_hint_still_has_priority(self):
        supplied = 'Em cần kiểm tra đặc điểm tọa độ nào của một điểm thuộc trục tung trước khi dùng hàm số?'
        self.assertEqual(sanitize_socratic_hint(supplied, 'C', AXIS, ['A. 0','B. 3','C. -4','D. 2']), supplied)

    def test_explicit_answer_leak_is_not_preserved(self):
        result = sanitize_socratic_hint('Đáp án C là -4, em thấy đúng không?', 'C', AXIS, ['A. 0','B. 3','C. -4','D. 2'])
        self.assertIn('trục tung', result)
        self.assertNotIn('-4', result)
        self.assertNotIn('đáp án', result.casefold())

    def test_unrelated_math_keeps_existing_fallback_path(self):
        self.assertIsNone(math_context_question('Hàm số có bao nhiêu điểm cực trị?'))
        existing = sanitize_socratic_hint('', 'A', 'Hàm số có bao nhiêu điểm cực trị?', ['A. 0','B. 1','C. 2','D. 3'])
        self.assertIn('cực trị', existing)

    def test_english_reading_fallback_uses_final_task_without_answer(self):
        question = ('Read the following passage and choose the best answer: '
                    'I catch fish with my grandfather. What does the writer do with their grandfather?')
        for grade in range(6, 13):
            result = sanitize_socratic_hint('Đáp án C là catch fish, đúng không?', 'C', question,
                ['A. Dry rice', 'B. Collect eggs', 'C. Catch fish', 'D. Farm work'],
                subject='Anh', grade_num=grade)
            self.assertIn('hoạt động', result)
            self.assertIn('đúng chủ thể', result)
            self.assertTrue(result.endswith('?'))
            self.assertNotIn('catch fish', result.lower())
            self.assertNotIn('grandfather', result.lower())
        supplied = 'Em cần tìm chi tiết nào gắn với người được hỏi trong đoạn đọc?'
        self.assertEqual(sanitize_socratic_hint(supplied, q_text=question, subject='Tiếng Anh'), supplied)
        grammar = sanitize_socratic_hint('', q_text='What do you enjoy ___?', subject='Tiếng Anh')
        self.assertNotIn('đoạn đọc', grammar)

    def test_all_supported_contexts_keep_valid_hint_and_other_subject_routes(self):
        supplied = 'Em cần đối chiếu dữ kiện nào trong câu hỏi trước khi lập luận?'
        checked = 0
        for grade in range(6,13):
            for subject in subjects_for_grade(grade):
                self.assertEqual(sanitize_socratic_hint(supplied, subject=subject, grade_num=grade), supplied)
                if subject != 'Toán học':
                    value = sanitize_socratic_hint('', q_text=AXIS, subject=subject, grade_num=grade)
                    self.assertNotIn('trục tung', value)
                checked += 1
        self.assertEqual(checked,65)


if __name__ == '__main__':
    unittest.main()
