import copy
import json
import unittest
from unittest.mock import patch

from services.context_recovery import repair_exam_context
from services.recovery_diagnostics import recovery_failure_summary


class TestRecoveryErrorStage(unittest.TestCase):
    def source(self):
        return {'p1': [{'q': 'Cho đồ thị như hình bên.', 'topic': 'Hàm số',
                        'opt': ['A. 1', 'B. 2', 'C. 3', 'D. 4'], 'ans': 'B'}]}

    def test_failures_are_classified_without_logging_text_or_adding_calls(self):
        for stage in ('provider', 'decode', 'recover', 'validate'):
            with self.subTest(stage=stage):
                source = self.source()
                before = copy.deepcopy(source)
                calls = []
                def generate(_):
                    calls.append(1)
                    if stage == 'provider': raise RuntimeError('PRIVATE KEY')
                    if stage == 'decode': return '{"unfinished":"PRIVATE ANSWER'
                    return {'replacement_question': {'subject': 'Toán học', 'grade': 12}}
                if stage == 'recover':
                    context = patch('services.context_recovery.recover_visual',
                                    side_effect=[copy.deepcopy(source['p1'][0]), TypeError('PRIVATE KEY')])
                elif stage == 'validate':
                    context = patch('services.context_recovery._candidate_issue', side_effect=KeyError('PRIVATE ANSWER'))
                else:
                    context = patch('services.context_recovery.has_visual', return_value=False)
                with context:
                    result = repair_exam_context(source, 'Toán', 12, ai_generator=generate)
                self.assertEqual(source, before)
                self.assertEqual(len(calls), 1)
                self.assertEqual(result['context_recovery']['unresolved'], 1)
                event = result['context_recovery']['events'][0]
                self.assertEqual(event['replacement_stage'], stage)
                summary = recovery_failure_summary('Toán học', 12, result['context_recovery'])
                self.assertNotIn('PRIVATE', json.dumps(summary))
                self.assertNotEqual(summary['events'][0]['replacement_error_type'], 'unknown')

    def test_wrong_root_shapes_are_envelope_failures_not_json_syntax_failures(self):
        for payload in ([], None, {'replacement_question': []}, {'p1': []}):
            result = repair_exam_context(self.source(), 'Toán', 12, ai_generator=lambda _: payload)
            event = result['context_recovery']['events'][0]
            self.assertEqual((event['replacement_stage'], event['replacement_error_type']), ('envelope', 'ValueError'))

    def test_parseable_json_wrong_wrapper_is_logged_without_private_content(self):
        calls = []
        raw = json.dumps({'output': {'q': 'PRIVATE QUESTION', 'ans': 'PRIVATE ANSWER'}})
        def generate(_):
            calls.append(1)
            return raw
        source = self.source()
        before = copy.deepcopy(source)
        result = repair_exam_context(source, 'Toán', 12, ai_generator=generate)
        summary = recovery_failure_summary('Toán học', 12, result['context_recovery'])
        self.assertEqual(summary['events'][0]['replacement_stage'], 'envelope')
        self.assertEqual(summary['events'][0]['replacement_error_type'], 'ValueError')
        self.assertNotIn('PRIVATE', json.dumps(summary))
        self.assertEqual(len(calls), 1)
        self.assertEqual(source, before)
        self.assertEqual(result['context_recovery']['unresolved'], 1)

    def test_untrusted_stage_and_error_fields_are_whitelisted(self):
        summary = recovery_failure_summary('Toán học', 12, {'events': [{
            'replacement_stage': 'PRIVATE', 'replacement_error_type': {'key': 'PRIVATE'}}]})
        self.assertNotIn('PRIVATE', json.dumps(summary))
        self.assertEqual(summary['events'][0]['replacement_stage'], 'unknown')
        self.assertEqual(summary['events'][0]['replacement_error_type'], 'unknown')
