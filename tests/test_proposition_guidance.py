import unittest

from services.curriculum_policy import correct_reviewed_proposition_guidance


class PropositionGuidanceTests(unittest.TestCase):
    sample = ('Bước 2: Lập kế hoạch: + Xét từng câu: Câu a là khẳng định toán học '
              'về số $15$; Câu b là câu cầu khiến; Câu c là khẳng định về nghiệm '
              'của phương trình trên tập số thực. + Kiểm tra tính đúng/sai.')

    def test_reproduced_classification_is_left_to_student(self):
        fixed = correct_reviewed_proposition_guidance(self.sample, 'Toán học', 10, 'Mệnh đề')
        self.assertNotIn('Câu b là câu cầu khiến', fixed)
        self.assertIn('Em tự nhận diện', fixed)
        self.assertIn('Bước 2:', fixed)
        self.assertIn('Kiểm tra tính đúng/sai.', fixed)
        self.assertEqual(correct_reviewed_proposition_guidance(fixed, 'Toán học', 10, 'Mệnh đề'), fixed)

    def test_examples_code_and_other_contexts_are_preserved(self):
        example = 'Ví dụ có lời giải: Câu b là câu cầu khiến.'
        code = '```text\n' + self.sample + '\n```'
        for value in (example, code):
            self.assertEqual(correct_reviewed_proposition_guidance(value, 'Toán học', 10, 'Mệnh đề'), value)
        for subject, grade, topic in [('Ngữ văn', 10, 'Mệnh đề'), ('Toán học', 11, 'Mệnh đề'),
                                      ('Toán học', 10, 'Vectơ')]:
            self.assertEqual(correct_reviewed_proposition_guidance(self.sample, subject, grade, topic), self.sample)
