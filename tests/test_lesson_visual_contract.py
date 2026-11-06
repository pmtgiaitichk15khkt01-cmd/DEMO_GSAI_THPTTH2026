import unittest
from services.academic_context import subjects_for_grade
from services.curriculum_policy import lesson_generation_request


class LessonVisualContractTests(unittest.TestCase):
    def test_math_bbt_request_uses_existing_renderer_contract_only(self):
        count = 0
        for grade in range(6, 13):
            for subject in subjects_for_grade(grade):
                system, prompt = lesson_generation_request(subject, grade, 'QA topic')
                if subject == 'Toán học':
                    self.assertIn('x, y′, y', prompt)
                    self.assertIn('không thay bảng bằng đoạn văn xét dấu', prompt)
                    self.assertIn('chỉ khi nội dung bài thực sự cần', prompt)
                else:
                    self.assertNotIn('x, y′, y', prompt)
                self.assertIn('CORRECT:', prompt)
                self.assertIn('Bước 4: Kiểm tra và nhìn lại', prompt)
                count += 1
        self.assertEqual(count, 65)


if __name__ == '__main__':
    unittest.main()
