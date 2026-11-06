import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from services import curriculum_policy as policy
from services.academic_context import subjects_for_grade


class PolicyEvaluationDateTests(unittest.TestCase):
    def test_default_uses_issue_day_and_excludes_expired_or_future_references(self):
        docs = [dict(code='old', effective_from='2020-01-01', effective_until='2026-10-31'),
                dict(code='current', effective_from='2026-10-31'),
                dict(code='future', effective_from='2026-11-01')]
        with tempfile.TemporaryDirectory() as folder:
            registry = Path(folder) / 'refs.json'
            registry.write_text(json.dumps({'documents': docs}), encoding='utf-8')
            with patch.object(policy, 'REGISTRY', registry), patch.object(policy, 'policy_evaluation_date', return_value='2026-10-31', create=True):
                self.assertEqual([r['code'] for r in policy.legal_references()], ['current'])
                self.assertEqual([r['code'] for r in policy.legal_references('2026-10-30')], ['old'])

    def test_future_notice_stops_on_effective_day_even_if_status_is_stale(self):
        docs = [dict(code='pending', effective_from='2026-12-01', status='upcoming'),
                dict(code='future_without_label', effective_from='2026-12-02', status='active'),
                dict(code='draft', effective_from='2026-12-03', status='draft')]
        with tempfile.TemporaryDirectory() as folder:
            registry = Path(folder) / 'refs.json'
            registry.write_text(json.dumps({'documents': docs}), encoding='utf-8')
            with patch.object(policy, 'REGISTRY', registry):
                self.assertEqual([r['code'] for r in policy.upcoming_legal_references('2026-11-30')],
                                 ['pending', 'future_without_label'])
                self.assertEqual([r['code'] for r in policy.upcoming_legal_references('2026-12-01')],
                                 ['future_without_label'])
                self.assertEqual(policy.upcoming_legal_references('2026-12-02'), [])
                self.assertIn('pending', [r['code'] for r in policy.legal_references('2026-12-01')])

    def test_generation_contexts_show_application_date_separately_from_source_review(self):
        cells = 0
        with patch.object(policy, 'policy_evaluation_date', return_value='2026-10-31', create=True):
            for grade in range(6, 13):
                for subject in subjects_for_grade(grade):
                    for station in (1, 3):
                        prompt = policy.policy_prompt(subject, grade, station)
                        self.assertIn('ngày áp dụng 2026-10-31', prompt)
                        self.assertIn('ngày rà soát nguồn', prompt)
                        cells += 1
        self.assertEqual(cells, 130)


if __name__ == '__main__':
    unittest.main()
