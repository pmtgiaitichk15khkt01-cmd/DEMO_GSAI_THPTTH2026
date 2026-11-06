"""Initial generation must know the renderer contract, before paid recovery."""
import json
import unittest

from services.academic_context import subjects_for_grade
from services.curriculum_policy import exam_prompt
from services.web_question_contract import WEB_QUESTION_INSTRUCTION


class TestInitialExamWebContract(unittest.TestCase):
    def test_initial_generation_keeps_all_65_context_schemas_and_custom_requests(self):
        checked = 0
        marker = 'Chỉ xuất JSON hợp lệ theo schema sau (mở rộng số câu theo cấu hình):\n'
        for grade in range(6, 13):
            for subject in subjects_for_grade(grade):
                with self.subTest(subject=subject, grade=grade):
                    custom = f'Yêu cầu riêng {subject} lớp {grade}'
                    prompt = exam_prompt(subject, grade, ['Chủ đề đang chọn'], (3, 1, 1), '1234', custom)
                    self.assertEqual(prompt.count(WEB_QUESTION_INSTRUCTION), 1)
                    self.assertIn(custom, prompt)
                    schema = json.loads(prompt.split(marker, 1)[1])
                    self.assertEqual((schema['subject'], schema['grade']), (subject, grade))
                    if subject == 'Ngữ văn':
                        self.assertIn('part_doc_hieu', schema)
                        self.assertIn('part_viet', schema)
                        self.assertNotIn('p1', schema)
                        questions = schema['part_doc_hieu']['questions'] + schema['part_viet']
                    else:
                        self.assertEqual(len(schema['p1'][0]['opt']), 4)
                        self.assertIn('ans', schema['p3'][0])
                        questions = schema['p1'] + schema['p2'] + schema['p3']
                    for question in questions:
                        self.assertIn('hint', question)
                        self.assertIn('explain', question)
                        self.assertNotEqual(question['hint'], question['explain'])
                checked += 1
        self.assertEqual(checked, 65)

    def test_visual_examples_and_uniqueness_are_available_before_replacement(self):
        prompt = exam_prompt('Toán', 12, ['Hàm số'], (3, 1, 1), '1234')
        for term in ('func_3', 'bbt', 'mslgn_data', 'đúng một phương án đúng', 'không chỉ khoảng tối đại'):
            self.assertIn(term, prompt)
        self.assertIn('explain và ans dành cho giải thích/chấm bài', prompt)
