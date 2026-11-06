import unittest

from services.socratic_context import repair_reviewed_station1_closing
from services.curriculum_policy import correct_reviewed_cubic_prior_knowledge


class ClosingScienceTests(unittest.TestCase):
    def test_contradictory_recap_fixed_without_shortening_moral_lesson(self):
        first = "Thầy ghi nhận em phân tích sự đổi dấu của $y'=3x^2$ tại $x=0$."
        moral = ('Bài học trung thực và cầu thị. Marcus Aurelius, Meditations, '
                 'theo bản dịch của George Long; tham khảo tại classics.mit.edu.')
        reply = first + '\n\n' + moral + '\n\nLắng nghe và sửa sai là cách sống có trách nhiệm.'
        student = "Với y=x^3, y'=3x^2 dương hai phía nên không đổi dấu. Em đã hiểu."
        result = repair_reviewed_station1_closing(reply, student, 'Toán học', 12, True)
        self.assertNotIn('phân tích sự đổi dấu', result)
        self.assertIn('Bài học trung thực và cầu thị.', result)
        self.assertIn('Lắng nghe và sửa sai', result)
        self.assertIn('diễn nghĩa tiếng Việt', result)
        self.assertIn('meditations.6.six.html', result)
        self.assertEqual(repair_reviewed_station1_closing(reply, student, 'Toán học', 12, False), reply)

    def test_unique_root_guidance_does_not_give_solution_regions(self):
        text = ('$y=x^3-3x+1$\nBước 4: Kiểm tra lại các trường hợp $m > 3$, $m < -1$ '
                'và các giá trị biên xem đồ thị cắt đường thẳng $y=m$ tại mấy điểm để kết luận chính xác.')
        result = correct_reviewed_cubic_prior_knowledge(text, 'Toán học', 12, 'Khảo sát hàm số bậc ba')
        self.assertNotIn('$m > 3$', result)
        self.assertNotIn('$m < -1$', result)
        self.assertIn('kiểm tra riêng từng mức biên', result)
        self.assertIn('$y=x^3-3x+1$', result)


if __name__ == '__main__':
    unittest.main()
