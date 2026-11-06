"""Contracts for curated external-source records, not synthetic knowledge approval."""
from copy import deepcopy
from pathlib import Path
import unittest
from services.bank_storage import iter_exam_shard
from services.cognitive_runtime import independent_exam_audit
from services.exam_delivery import exam_delivery_held


class Tin0525CognitiveRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path=Path(__file__).parents[1]/'data/real_exam_bank/exams_Tin_h_c.json.xz'
        cls.exam=next(e for e in iter_exam_shard(path)
            if str(e.get('code'))=='0525' and e.get('year')==2026)

    def test_curated_units_retain_prerequisite_grades_and_paper_hold(self):
        original=deepcopy(self.exam)
        audit=independent_exam_audit(self.exam,self.exam['subject'],12,as_of='2026-11-03')
        self.assertEqual(audit['verified_records'],47)
        self.assertEqual(audit['pending_records'],1)
        self.assertEqual(audit['response_units'],48)
        self.assertEqual(audit['context_containers'],6)
        self.assertEqual(audit['held_source_records'],1)
        self.assertEqual(audit['needs_review_records'],0)
        prerequisites=[r for r in audit['rows'] if r['verified']
            and r['curriculum_relationship']=='explicit_prerequisite']
        self.assertEqual(len(prerequisites),16)
        self.assertTrue(all(r['mapped_outcome_grade'] in (10,11)
            and r['assessment_grade']==12 for r in prerequisites))
        q14=next(r for r in audit['rows'] if r['part']=='p1' and r['question']==14)
        self.assertFalse(q14['verified'])
        self.assertTrue(exam_delivery_held(self.exam))
        self.assertEqual(self.exam,original)

    def test_records_do_not_authorize_changed_use_grade_or_expired_date(self):
        changed=deepcopy(self.exam);changed['exam_type']='periodic_assessment'
        for exam,grade,day in [(changed,12,'2026-11-03'),
                (self.exam,11,'2026-11-03'),(self.exam,12,'2026-12-01')]:
            self.assertEqual(independent_exam_audit(exam,self.exam['subject'],grade,
                as_of=day)['verified_records'],0)
