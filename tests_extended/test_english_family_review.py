import unittest

from services.curriculum_policy import correct_reviewed_english_family_guidance as repair


class ReviewedEnglishFamilyTests(unittest.TestCase):
    def test_reviewed_item_context_preserves_internal_key(self):
        source = (
            'In my family, my father usually __________ the heavy lifting, but today he __________ a rest.\n'
            'A. does / is taking\nD. does / takes\nCORRECT: A\n'
            'go to the market / visit her grandmother'
        )
        result = repair(source, 'Tiếng Anh', 10, 'Unit 1 Family life')
        self.assertIn('Right now', result)
        self.assertIn('visit her own mother', result)
        self.assertIn('A. does / is taking\nD. does / takes\nCORRECT: A', result)
        self.assertEqual(result, repair(result, 'Tiếng Anh', 10, 'Unit 1 Family life'))

    def test_time_words_do_not_substitute_for_explicit_example_context(self):
        source = (
            "Today, my mother (not/go) __________ to work; she (stay) __________ at home to celebrate my sister's birthday.\n"
            'I (take) __________ out the rubbish every night, but tonight my brother (do) __________ it for me.\n'
            '**Dấu hiệu nhận biết**'
        )
        result = repair(source, 'Tiếng Anh', 10, 'Unit 1 Family life')
        self.assertIn('My mother usually goes to work in the morning. Right now', result)
        self.assertIn('every night. Right now, my brother', result)
        self.assertNotIn('**Dấu hiệu nhận biết**', result)
        self.assertEqual(source, repair(source, 'Tiếng Anh', 11, 'Family life'))
        self.assertEqual(result, repair(result, 'Tiếng Anh', 10, 'Family life'))

    def test_replacement_context_and_adjective_review_preserve_keys(self):
        source = (
            'In my family, my father ________ the heavy lifting, and my mother does the cooking.\n'
            'A. is doing\nB. does\nC. do\nD. are doing\nCORRECT: B\n'
            '\"Where is your mother?\" - \"She ________ the garden. She loves plants.\"\n'
            'CORRECT: B\n'
            'My brother usually (wash) ________ the dishes, but today I (do) ________ it for him.\n'
            'Vế sau có \"today\" ám chỉ một sự thay đổi tạm thời so với thói quen\n'
            'Nam / usually / take out the rubbish / but / tonight / he / help / his sister / with her homework.\n'
            'lỗi dùng động từ trạng thái (tired)\n'
            'cách dùng thì và động từ trạng thái (stative verbs)\n'
        )
        fixed = repair(source, 'Tiếng Anh', 10, 'Unit 1 Family life')
        self.assertIn("In our family's usual household routine", fixed)
        self.assertIn('garden right now', fixed)
        self.assertIn('Right now, I (do)', fixed)
        self.assertIn('but / right now / he', fixed)
        self.assertNotIn('động từ trạng thái (tired)', fixed)
        self.assertIn('be + tính từ', fixed)
        self.assertEqual(fixed.count('CORRECT: B'), 2)
        self.assertIn('A. is doing\nB. does\nC. do\nD. are doing', fixed)
        self.assertEqual(fixed, repair(fixed, 'Tiếng Anh', 10, 'Unit 1 Family life'))
        self.assertEqual(source, repair(source, 'Tiếng Anh', 11, 'Unit 1 Family life'))
        fenced = '```text\n' + source + '\n```'
        self.assertEqual(fenced, repair(fenced, 'Tiếng Anh', 10, 'Unit 1 Family life'))
        unrelated = 'cách dùng thì và động từ trạng thái (stative verbs): know, believe'
        self.assertEqual(unrelated, repair(unrelated, 'Tiếng Anh', 10, 'Unit 1 Family life'))

    def test_quoted_code_and_other_contexts_stay_unchanged(self):
        source = '```text\nMy sister is cleaning her room every Sunday morning.\n```'
        self.assertEqual(source, repair(source, 'Tiếng Anh', 10, 'Family life'))
        for subject, grade, topic in [('Tiếng Anh', 11, 'Family life'),
                                      ('Ngữ văn', 10, 'Family life'),
                                      ('Tiếng Anh', 10, 'Ecotourism')]:
            prose = 'My sister is cleaning her room every Sunday morning.'
            self.assertEqual(prose, repair(prose, subject, grade, topic))


class ParsedEnglishFamilyTests(unittest.TestCase):
    def test_where_question_evidence_uses_explicit_time_without_approving_level(self):
        from copy import deepcopy
        from services.curriculum_policy import repair_reviewed_english_family_question
        original = {'question': '"Where is your mother right now?"',
                    'correct': 'B', 'level': 'TH',
                    'cognitive_evidence': {
                        'cognitive_rationale': 'Học sinh cần hiểu tình huống "đang ở đâu" để suy luận ra hành động đang diễn ra.',
                        'solution_steps': ["Phân tích câu hỏi 'Where is...?' để xác định thời điểm hành động"],
                        'review': 'pending'}}
        before = deepcopy(original)
        fixed = repair_reviewed_english_family_question(original, 'Tiếng Anh', 10, 'Family life')
        self.assertEqual(original, before)
        self.assertIn('right now', fixed['cognitive_evidence']['cognitive_rationale'])
        self.assertIn('right now', fixed['cognitive_evidence']['solution_steps'][0])
        self.assertEqual(fixed['cognitive_evidence']['review'], 'pending')
        self.assertEqual((fixed['correct'], fixed['level']), ('B', 'TH'))
        self.assertEqual(fixed, repair_reviewed_english_family_question(fixed, 'Tiếng Anh', 10, 'Family life'))
        self.assertEqual(original, repair_reviewed_english_family_question(original, 'Tiếng Anh', 11, 'Family life'))
        self.assertIn('right now', repair(before['cognitive_evidence']['cognitive_rationale'], 'Tiếng Anh', 10, 'Family life'))

    def test_existing_parsed_quiz_is_repaired_without_mutating_key_or_source(self):
        from copy import deepcopy
        from services.curriculum_policy import repair_reviewed_english_family_question
        original = {'question': 'Which sentence describes a household routine?',
                    'options': ['A. My sister clean her room.',
                                'B. My sister is cleaning her room every Sunday morning.',
                                'C. My sister are cleaning her room.',
                                'D. My sister cleans her room every Sunday morning.'],
                    'correct': 'D', 'level': 'VD', 'cognitive_evidence': {'review': 'pending'}}
        before = deepcopy(original)
        fixed = repair_reviewed_english_family_question(original, 'Tiếng Anh', 10, 'Family life')
        self.assertEqual(original, before)
        self.assertEqual(fixed['options'][1], 'B. My sister is clean her room every Sunday morning.')
        self.assertEqual(fixed['correct'], 'D')
        self.assertEqual(fixed['level'], 'VD')  # Never self-certify cognitive level.
        self.assertEqual(fixed['cognitive_evidence'], original['cognitive_evidence'])
        self.assertEqual(fixed, repair_reviewed_english_family_question(fixed, 'Tiếng Anh', 10, 'Family life'))
        self.assertEqual(original, repair_reviewed_english_family_question(original, 'Ngữ văn', 10, 'Family life'))


if __name__ == '__main__':
    unittest.main()
