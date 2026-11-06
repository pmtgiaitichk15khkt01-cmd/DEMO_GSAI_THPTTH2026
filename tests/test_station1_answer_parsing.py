import unittest
from unittest.mock import patch
from tests.test_expert_patch_regressions import load_function


class Station1AnswerParsingTests(unittest.TestCase):
    def test_recovery_preserves_live_option_order_and_requires_unambiguous_source(self):
        recover = load_function('recover_missing_quiz_keys')
        old = {'question': 'Chọn theo tiêu chí', 'options': ['A. Một', 'B. Hai', 'C. Ba', 'D. Bốn'], 'correct': ''}
        source = dict(old, options=['A. Bốn', 'B. Ba', 'C. Hai', 'D. Một'], correct='C', hint='Tự đối chiếu?')
        fixed = recover([old], [source])[0]
        self.assertEqual(fixed['correct'], 'B')
        self.assertEqual(fixed['options'], old['options'])
        self.assertEqual(old['correct'], '')
        self.assertEqual(recover([old], [source, source])[0], old)
        self.assertEqual(recover([old], [dict(source, question='Khác')])[0], old)
        self.assertEqual(recover([old], [dict(source, correct='')])[0], old)
        known = dict(old, correct='A')
        self.assertEqual(recover([known], [source])[0], known)

    def parse(self, answer):
        fn = load_function('parse_quiz_questions', sanitize_katex_latex=lambda s:s,
            format_pedagogical_math=None, annotate_question=lambda q:q)
        text = 'Câu 1: Nội dung kiểm thử\nA. Một\nB. Hai\nC. Ba\nD. Bốn\n' + answer
        with patch('random.shuffle', side_effect=lambda items:items.reverse()):
            return fn(text)[0]

    def test_missing_key_is_not_invented_as_a(self):
        self.assertEqual(self.parse('')['correct'], '')

    def test_markdown_reserved_fields_keep_key_and_hint_without_leaking_metadata(self):
        for key in ('**CORRECT:** **B**', '**CORRECT**: B', '__CORRECT:__ B'):
            with self.subTest(key=key):
                q = self.parse(key + '\n**HINT:** Em hãy tự đối chiếu tiêu chí?\n'
                               '**OUTCOME:** Viết theo yêu cầu thể loại.')
                self.assertEqual(q['correct'], 'C')
                self.assertEqual(q['hint'], 'Em hãy tự đối chiếu tiêu chí?')
                self.assertEqual(q['learning_outcome'], 'Viết theo yêu cầu thể loại.')
                self.assertNotIn('OUTCOME', q['explain'])

    def test_vietnamese_choose_prefix_preserves_answer_identity_after_shuffle(self):
        q = self.parse('CORRECT: Chọn B')
        self.assertEqual(q['correct'], 'C')
        self.assertEqual(q['options'][2], 'C. Hai')

    def test_list_formatted_internal_fields_are_read_without_leaking_explanation(self):
        for marker in ('* ', '- ', '+ ', '1. ', '2) '):
            with self.subTest(marker=marker):
                q = self.parse(marker + '**CORRECT:** B\n' + marker + 'HINT: Tự xét tiêu chí?\n'
                               + marker + 'EXPLAIN: Lời giải sau nộp.\n'
                               + marker + 'OUTCOME: Phân loại theo định nghĩa.')
                self.assertEqual(q['correct'], 'C')
                self.assertEqual(q['hint'], 'Tự xét tiêu chí?')
                self.assertEqual(q['explain'], 'Lời giải sau nộp.')
                self.assertEqual(q['learning_outcome'], 'Phân loại theo định nghĩa.')

    def test_unrecognized_key_is_not_taken_from_letters_inside_prose(self):
        self.assertEqual(self.parse('CORRECT: Chưa xác định')['correct'], '')

    def test_only_quiz_section_is_parsed_when_lesson_has_a_worked_example(self):
        fn = load_function('parse_quiz_questions', sanitize_katex_latex=lambda s:s,
            format_pedagogical_math=None, annotate_question=lambda q:q)
        example = 'Câu 1: Ví dụ trong lý thuyết\nA. Một\nB. Hai\nC. Ba\nD. Bốn\nCORRECT: A\n'
        quiz = 'Câu 1: Bài luyện tập\nA. Alpha\nB. Beta\nC. Gamma\nD. Delta\nCORRECT: B\n'
        text = '### PHẦN 1: Lý thuyết\n' + example + '### PHẦN 2: Trắc nghiệm\n' + quiz + '### PHẦN 3: Tự luận\n'
        result = fn(text)
        self.assertEqual(len(result), 1)
        self.assertIn('Bài luyện tập', result[0]['question'])
        self.assertNotIn('Ví dụ trong lý thuyết', result[0]['question'])

    def test_plain_section_titles_keep_worked_examples_out_of_quiz(self):
        fn = load_function('parse_quiz_questions', sanitize_katex_latex=lambda s:s,
            format_pedagogical_math=None, annotate_question=lambda q:q)
        sample = 'Câu 1: Nội dung\nA. Một\nB. Hai\nC. Ba\nD. Bốn\nCORRECT: B\n'
        result = fn('PHẦN 1: Lý thuyết\n' + sample + 'PHẦN 2: Trắc nghiệm\n' + sample + 'PHẦN 3: Tự luận\n' + sample)
        self.assertEqual(len(result), 1)

    def test_bold_question_label_does_not_leave_a_dangling_marker(self):
        fn = load_function('parse_quiz_questions', sanitize_katex_latex=lambda s:s,
            format_pedagogical_math=None, annotate_question=lambda q:q)
        for header in ('**Câu 1:** Cho **hàm số** y=x.', 'Câu 1: Cho **hàm số** y=x.', '**Câu 1. [Mức độ: NB]** Cho **hàm số** y=x.'):
            result=fn(header+'\nA. Một\nB. Hai\nC. Ba\nD. Bốn\nCORRECT: B')[0]
            self.assertEqual(result['question'], 'Cho **hàm số** y=x.')

    def test_standard_key_still_shuffles_correctly(self):
        self.assertEqual(self.parse('CORRECT: A')['correct'], 'D')

    def test_question_reference_inside_stem_is_not_a_new_question(self):
        fn = load_function('parse_quiz_questions', sanitize_katex_latex=lambda s:s,
            format_pedagogical_math=None, annotate_question=lambda q:q)
        stem = 'Đối chiếu dữ kiện ở Câu 2: nhân vật có hành động nào?'
        text = 'Câu 1: ' + stem + '\nA. Một\nB. Hai\nC. Ba\nD. Bốn\nCORRECT: B'
        result = fn(text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['question'], stem)

    def test_parenthesized_option_labels_do_not_leave_a_stray_parenthesis(self):
        fn = load_function('parse_quiz_questions', sanitize_katex_latex=lambda s:s,
            format_pedagogical_math=None, annotate_question=lambda q:q)
        text = 'Câu 1: Select the word.\nA) One\nB) Two\nC) Three\nD) Four\nCORRECT: B'
        with patch('random.shuffle', side_effect=lambda items:items.reverse()):
            result = fn(text)[0]
        self.assertEqual(result['options'], ['A. Four', 'B. Three', 'C. Two', 'D. One'])
        self.assertEqual(result['correct'], 'C')


if __name__ == '__main__':
    unittest.main()
