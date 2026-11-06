import json
import unittest

from data.socratic_anchors import safe_json_loads


class TestAIJSON(unittest.TestCase):
    def test_complete_root_with_one_redundant_matching_closer_is_recovered(self):
        payload = {'p1': [{'q': 'Câu đầy đủ', 'ans': 'B'}], 'p2': [], 'p3': []}
        self.assertEqual(safe_json_loads(json.dumps(payload) + '\n}'), payload)
        self.assertEqual(safe_json_loads('[{"q":"x"}]\n]'), [{'q': 'x'}])

    def test_closer_recovery_does_not_discard_content_or_accept_mismatched_tail(self):
        for suffix in ('\n]', '\n}{"ans":"D"}', '\n} explanation', '\n}}}}'):
            with self.subTest(suffix=suffix), self.assertRaises(ValueError):
                safe_json_loads('{"q":"x","ans":"B"}' + suffix)

    def test_complete_json_fence_after_short_preamble_is_recovered(self):
        data = {'p1': [{'q': 'Câu đầy đủ', 'ans': 'B'}], 'p2': [], 'p3': []}
        raw = 'Dữ liệu JSON:\n```json\n' + json.dumps(data, ensure_ascii=False) + '\n```'
        self.assertEqual(safe_json_loads(raw), data)

    def test_preamble_fence_does_not_hide_multiple_roots_or_truncation(self):
        for body in ('{"q":"x"} {"q":"y"}', '{"q":"chưa xong'):
            with self.subTest(body=body), self.assertRaises(ValueError):
                safe_json_loads('Dữ liệu JSON:\n```json\n' + body + '\n```')

    def test_standard_exam_is_unchanged(self):
        data = {'p1': [{'q': 'Tìm x.', 'opt': ['A. 1', 'B. 2', 'C. 3', 'D. 4'], 'ans': 'B'}], 'p2': [], 'p3': []}
        self.assertEqual(safe_json_loads(json.dumps(data, ensure_ascii=False)), data)

    def test_opening_fence_without_closing_fence_does_not_cut_json(self):
        data = {'p1': [{'q': 'Câu hỏi', 'ans': 'D'}], 'p2': [], 'p3': []}
        self.assertEqual(safe_json_loads('```json\n' + json.dumps(data)), data)

    def test_combined_inner_quote_and_trailing_comma_are_repaired_together(self):
        raw = '{"q":"Từ "học tập" được dùng như thế nào?","opt":["A", "B", "C", "D",],"ans":"B",}'
        self.assertEqual(safe_json_loads(raw), {'q': 'Từ "học tập" được dùng như thế nào?', 'opt': ['A', 'B', 'C', 'D'], 'ans': 'B'})

    def test_missing_separator_between_complete_properties(self):
        self.assertEqual(safe_json_loads('{"q":"Câu hỏi" "ans":"B"}'), {'q': 'Câu hỏi', 'ans': 'B'})

    def test_missing_separator_between_complete_question_objects(self):
        self.assertEqual(safe_json_loads('{"p1":[{"q":"Câu 1"}{"q":"Câu 2"}]}'), {'p1': [{'q': 'Câu 1'}, {'q': 'Câu 2'}]})

    def test_string_content_resembling_trailing_comma_is_untouched(self):
        text = 'Kí hiệu ,} và ,] trong đoạn trích.'
        self.assertEqual(safe_json_loads(json.dumps({'q': text}))['q'], text)

    def test_latex_survives_combined_syntax_recovery(self):
        raw = r'{"q":"Cho $\frac{1}{2}$ và "vectơ" $\vec{AB}$.","ans":"B",}'
        self.assertEqual(safe_json_loads(raw)['q'], r'Cho $\frac{1}{2}$ và "vectơ" $\vec{AB}$.')

    def test_valid_newline_and_escaped_quotes_remain_valid(self):
        text = 'Dòng một\nDòng hai "trích dẫn".'
        self.assertEqual(safe_json_loads(json.dumps({'q': text}))['q'], text)

    def test_real_truncation_does_not_invent_closing_content(self):
        for raw in ('{"q":"Câu chưa xong', '{"p1":[{"q":"Câu đầy đủ"}', '{"q":"x","ans":', '{"p1":['):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                safe_json_loads(raw)

    def test_duplicate_key_does_not_silently_drop_questions(self):
        with self.assertRaises(ValueError):
            safe_json_loads('{"p1":[{"q":"Câu 1"}],"p1":[{"q":"Câu 2"}]}')

    def test_arrays_and_utf8_text_are_preserved(self):
        data = [{'q': 'Địa lí Việt Nam', 'a': True}, {'q': 'English reading', 'a': False}]
        self.assertEqual(safe_json_loads(json.dumps(data, ensure_ascii=False)), data)

    def test_repair_limit_does_not_turn_into_an_unbounded_loop(self):
        raw = '{' + ' '.join(f'"key{i}":{{}}' for i in range(12)) + '}'
        with self.assertRaises(ValueError):
            safe_json_loads(raw)

    def test_long_multisubject_payload_does_not_drop_any_question(self):
        for subject in ('Toán học', 'Tiếng Anh', 'Địa lý'):
            data = {'subject': subject, 'grade': 12,
                    'p1': [{'q': f'Câu {i} của {subject}', 'opt': ['A', 'B', 'C', 'D'], 'ans': 'B'} for i in range(50)],
                    'p2': [], 'p3': []}
            raw = json.dumps(data, ensure_ascii=False, indent=2).replace('"p3": []', '"p3": [],')
            # A redundant comma near the end of a long response is recoverable
            # without balancing or discarding the preceding questions.
            result = safe_json_loads(raw)
            self.assertEqual(result, data)
