import copy
import json
import unittest

from services.academic_context import subjects_for_grade
from services.context_recovery import repair_exam_context
from services.web_question_contract import replacement_question_object


class TestReplacementEnvelopeContract(unittest.TestCase):
    def candidate(self, subject='Toán học', grade=12):
        return {'subject': subject, 'grade': grade, 'topic': 'QA routing',
                'q': 'Quan sát hình bên. Nhãn nào được in đậm?',
                'opt': ['A. A', 'B. B', 'C. C', 'D. D'], 'ans': 'A',
                'composite_visual': {'svg': '<svg xmlns="http://www.w3.org/2000/svg"><text font-weight="bold">A</text></svg>'}}

    def source(self):
        return {'p1': [{'q': 'Quan sát hình bên. Nhãn nào được in đậm?',
                        'opt': ['A. A', 'B. B', 'C. C', 'D. D'], 'ans': 'A', 'topic': 'QA routing'}]}

    def test_single_question_shapes_preserve_content_in_all_65_contexts(self):
        checked = 0
        for grade in range(6, 13):
            for subject in subjects_for_grade(grade):
                candidate = self.candidate(subject, grade)
                for response in (candidate, {'replacement_question': candidate},
                                 {'output': candidate}, {'output': {'replacement_question': candidate}}):
                    before = copy.deepcopy(response)
                    self.assertEqual(replacement_question_object(response), candidate)
                    self.assertEqual(response, before)
                checked += 1
        self.assertEqual(checked, 65)

    def test_adapter_does_not_bypass_existing_validation_or_add_calls(self):
        for wrong_subject in (False, True):
            candidate = self.candidate('Hóa học' if wrong_subject else 'Toán học')
            source = self.source()
            before = copy.deepcopy(source)
            calls = []
            def generate(prompt):
                calls.append(prompt)
                return json.dumps({'output': candidate}, ensure_ascii=False)
            result = repair_exam_context(source, 'Toán học', 12, ai_generator=generate)
            self.assertEqual(len(calls), 1)
            self.assertEqual(source, before)
            self.assertEqual(result['context_recovery']['unresolved'], int(wrong_subject))
            self.assertIn('root key must be replacement_question', calls[0])
            if not wrong_subject:
                self.assertEqual(result['p1'][0]['q'], candidate['q'])
                self.assertEqual(result['p1'][0]['opt'], candidate['opt'])
                self.assertEqual(result['p1'][0]['ans'], candidate['ans'])
                self.assertEqual(result['p1'][0]['replacement_audit']['origin'], 'ai_replacement')

    def test_multiple_ambiguous_or_unidentified_shapes_are_not_guessed(self):
        q = self.candidate()
        for payload in ([q], {'p1': [q]}, {'questions': [q]},
                        {'replacement_question': q, 'output': q},
                        dict(q, replacement_question=q), {'output': q, 'task': 'data'},
                        {'q': 'Missing identity', 'ans': 'A'}, {'output': {'output': q}}):
            with self.subTest(payload=type(payload).__name__), self.assertRaises(ValueError):
                replacement_question_object(payload)


if __name__ == '__main__':
    unittest.main()
