import copy
import json
import unittest
from unittest.mock import patch

from services.academic_context import subjects_for_grade
from services.context_recovery import needs_visual, _candidate_ok, repair_exam_context
from services.recovery_diagnostics import recovery_failure_summary
from services.web_question_contract import replacement_schema


class TestRestoredRecoveryContract(unittest.TestCase):
    def source(self):
        return {'p1': [{'q': 'Cho đồ thị như hình bên. Hãy đọc tung độ giao điểm.',
                        'opt': ['A. 1', 'B. 2', 'C. 3', 'D. 4'],
                        'ans': 'B', 'topic': 'Hàm số', 'level': 'TH'}]}

    def candidate(self):
        return {'subject': 'Toán học', 'grade': 12, 'topic': 'Hàm số', 'level': 'TH',
                'q': 'Cho hàm số $y=x^3+2$. Tung độ giao điểm với trục tung bằng bao nhiêu?',
                'opt': ['A. 1', 'B. 2', 'C. 3', 'D. 4'], 'ans': 'B'}

    def test_requested_output_table_is_not_missing_input(self):
        for text in ('Cho $y=x^3-3x+1$. Lập bảng biến thiên của hàm số.',
                     'Bảng biến thiên của hàm số được lập theo những bước nào?',
                     'Xét dấu đạo hàm rồi lập bảng xét dấu của hàm số đã cho.'):
            self.assertFalse(needs_visual({'q': text}), text)
        for text in ('Cho hàm số có bảng biến thiên sau đây.',
                     'Dựa vào bảng xét dấu, tìm khoảng đồng biến.',
                     'Lập bảng biến thiên dựa vào hình bên.',
                     'Bảng biến thiên của $y=x^3-3x+1$ như hình bên.'):
            self.assertTrue(needs_visual({'q': text}), text)

    def test_math_candidate_is_audited_once_and_rejection_unchanged(self):
        for wrong in (False, True):
            with patch('services.neuro_symbolic_verifier.audit_ai_generated_question_sympy',
                       return_value={'hallucination_detected': wrong}) as verifier:
                self.assertEqual(_candidate_ok(self.candidate(), 'p1', 'Toán học', 12, ['Hàm số']), not wrong)
                self.assertEqual(verifier.call_count, 1)

    def test_rejection_diagnoses_inherited_visual_requirement_without_weakening_it(self):
        before = self.source()
        preserved = copy.deepcopy(before)
        result = repair_exam_context(before, 'Toán', 12,
                     ai_generator=lambda _: {'replacement_question': self.candidate()})
        self.assertEqual(result['context_recovery']['unresolved'], 1)
        self.assertEqual(before, preserved)
        event = result['context_recovery']['events'][0]
        self.assertEqual(event['reason'], 'missing_source_visual')
        self.assertEqual(event['replacement_rejection'], 'replacement_visual_task_not_preserved')

    def test_replacement_prompt_contains_actual_renderer_contract_and_schema(self):
        prompts = []
        candidate = self.candidate()
        candidate['q'] = 'Cho đồ thị như hình bên của $y=x^3+2$. Tung độ giao điểm với trục tung bằng bao nhiêu?'
        def generate(prompt):
            prompts.append(prompt)
            return {'replacement_question': candidate}
        result = repair_exam_context(self.source(), 'Toán', 12, ai_generator=generate,
                                     custom_request='Chỉ hàm bậc ba')
        self.assertEqual(result['context_recovery']['unresolved'], 0)
        self.assertEqual(len(prompts), 1)
        self.assertIn('HỢP ĐỒNG CÂU HỎI TRÊN WEB', prompts[0])
        self.assertIn('socratic_hint', prompts[0])
        self.assertIn('Chỉ hàm bậc ba', prompts[0])

    def test_schema_preserves_subject_grade_part_contract_for_65_contexts(self):
        contexts = 0
        for grade in range(6, 13):
            for subject in subjects_for_grade(grade):
                for part in ('p1', 'p2', 'p3'):
                    data = replacement_schema(part, subject, grade, ['Chủ đề'], 'TH')['replacement_question']
                    self.assertEqual((data['subject'], data['grade'], data['topic']), (subject, grade, 'Chủ đề'))
                    self.assertNotEqual(data['socratic_hint'], data['explain'])
                    if part == 'p1': self.assertEqual(len(data['opt']), 4)
                    if part == 'p2': self.assertEqual(len(data['stmts']), 4)
                contexts += 1
        self.assertEqual(contexts, 65)

    def test_diagnostics_cannot_log_content_via_replacement_reason(self):
        for value, expected in [('replacement_visual_task_not_preserved', 'replacement_visual_task_not_preserved'),
                                ('PRIVATE KEY ANSWER', 'unknown'), ({'private': 'PRIVATE'}, 'unknown')]:
            summary = recovery_failure_summary('Toán học', 12,
                {'events': [{'replacement_rejection': value}]})
            self.assertEqual(summary['events'][0]['replacement_rejection'], expected)
            self.assertNotIn('PRIVATE', json.dumps(summary))
