import unittest
from services.curriculum_policy import label_declared_paraphrases, correct_reviewed_myth_guidance, policy_prompt
from services.academic_context import subjects_for_grade


class ParaphraseProvenanceTests(unittest.TestCase):
    def test_provenance_rule_is_in_every_supported_subject_grade_prompt(self):
        count = 0
        for grade in range(6, 13):
            for subject in subjects_for_grade(grade):
                for station in (1, 3):
                    with self.subTest(grade=grade, subject=subject, station=station):
                        self.assertIn('không phải trích dẫn nguyên văn', policy_prompt(subject, grade, station))
                        count += 1
        self.assertEqual(count, 130)

    def test_declared_paraphrase_is_labeled_without_certifying_or_rewriting_it(self):
        text = 'Ngữ liệu tham khảo (trích tinh thần văn bản A trong SGK):\n> "Đoạn minh họa."'
        fixed = label_declared_paraphrases(text)
        self.assertIn('không phải trích dẫn nguyên văn SGK', fixed)
        self.assertIn('> "Đoạn minh họa."', fixed)
        self.assertEqual(label_declared_paraphrases(fixed), fixed)
        self.assertEqual(label_declared_paraphrases('```text\n' + text + '\n```'), '```text\n' + text + '\n```')
        original = 'Trích nguyên văn đã đối chiếu: "Nội dung."'
        self.assertEqual(label_declared_paraphrases(original), original)

    def test_myth_content_repair_is_scoped_and_preserves_other_lessons(self):
        text = ('sau đó thần “ngẩng đầu lên đội trời lên cho khỏi đạp xuống đất” rồi đắp cột đá chống trời; '
                'SGK Ngữ thuật')
        fixed = correct_reviewed_myth_guidance(text, 'Ngữ văn', 10, 'Truyện về các vị thần sáng tạo thế giới')
        self.assertNotIn('“ngẩng đầu', fixed)
        self.assertIn('diễn ý, không trích nguyên văn', fixed)
        self.assertIn('SGK Ngữ văn', fixed)
        straight = text.replace('“', '"').replace('”', '"')
        self.assertNotIn('cho khỏi đạp xuống đất', correct_reviewed_myth_guidance(
            straight, 'Ngữ văn', 10, 'Truyện về các vị thần sáng tạo thế giới'))
        italic = text.replace('“', '*“').replace('”', '”*')
        self.assertNotIn('cho khỏi đạp xuống đất', correct_reviewed_myth_guidance(
            italic, 'Ngữ văn', 10, 'Truyện về các vị thần sáng tạo thế giới'))
        self.assertEqual(correct_reviewed_myth_guidance(text, 'Ngữ văn', 11, 'Truyện về các vị thần sáng tạo thế giới'), text)
        self.assertEqual(correct_reviewed_myth_guidance(text, 'Ngữ văn', 10, 'Chữ người tử tù'), text)
