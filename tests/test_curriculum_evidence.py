import copy
import unittest

from services.academic_context import subjects_for_grade
from services.curriculum_evidence import (
    DIMENSIONS, audit_evidence_readiness, content_fingerprint,
    outcome_reference,
)


class TestCurriculumEvidence(unittest.TestCase):
    def test_amendment_reference_does_not_cross_subject_grade_context(self):
        matches = []
        for grade in range(6, 13):
            for subject in subjects_for_grade(grade):
                result = outcome_reference("tt17-2025-annex-iv-item-5", subject, grade,
                                           on_date="2026-10-30")
                if result:
                    matches.append((subject, grade))
                    self.assertEqual(result["operation"], "remove_content_and_outcome")
                    self.assertFalse(result["blocks_delivery"])
                    self.assertFalse(result["academic_verified"])
        self.assertEqual(matches, [("Địa lý", 12)])

    def test_source_lookup_alias_date_and_unknown_are_conservative(self):
        key = "tt17-2025-annex-iv-item-3"
        self.assertIsNone(outcome_reference(key, "Địa lí", 12, on_date="2025-09-11"))
        row = outcome_reference(key, "Địa lí", 12, on_date="2025-09-12")
        self.assertIn("Phụ lục IV, mục 3", row["locator"])
        self.assertFalse(row["textbook_alignment_verified"])
        row["summary"] = "changed"
        self.assertNotEqual(outcome_reference(key, "Địa lí", 12, on_date="2026-10-30")["summary"], "changed")
        self.assertIsNone(outcome_reference("unknown", "Địa lý", 12, on_date="2026-10-30"))

    def record(self, payload):
        result = {"subject": "Toán học", "grade": 12,
                  "content_sha256": content_fingerprint(payload)}
        for dimension in DIMENSIONS:
            result[dimension] = dict(source_id="fixture-only", source_version="v1",
                locator="appendix/page", rationale="test only", reviewer="fixture",
                checked_at="2026-10-30")
        result["legal"].update(effective_from="2020-01-01", effective_until=None,
            applicability="fixture scope", amendment_review="fixture chain")
        return result

    def audit(self, payload, evidence=None, day="2026-10-30"):
        return audit_evidence_readiness(payload, "Toán", 12, on_date=day, evidence=evidence)

    def test_all_supported_contexts_and_stations_do_not_self_certify(self):
        cells = 0
        for grade in range(6, 13):
            for subject in subjects_for_grade(grade):
                for station in (1, 3):
                    with self.subTest(subject=subject, grade=grade, station=station):
                        payload = {"station": station, "q": "Theory without numbers",
                                   "academic_verified": True, "level": "NB"}
                        before = copy.deepcopy(payload)
                        result = audit_evidence_readiness(payload, subject, grade,
                                                         on_date="2026-10-30")
                        self.assertEqual(result["status"], "insufficient_evidence")
                        self.assertFalse(result["academic_verified"])
                        self.assertFalse(result["blocks_delivery"])
                        self.assertEqual(payload, before)
                        cells += 1
        self.assertEqual(cells, 130)

    def test_complete_fixture_is_only_ready_for_review(self):
        payload = {"q": "Given graph", "f": "x**3", "ans": "A"}
        record = self.record(payload)
        before = copy.deepcopy(record)
        result = self.audit(payload, record)
        self.assertEqual(result["status"], "ready_for_source_review")
        self.assertFalse(result["academic_verified"])
        self.assertEqual(record, before)

    def test_answer_visual_or_question_change_invalidates_binding(self):
        payload = {"q": "Given graph", "f": "x**3", "ans": "A"}
        record = self.record(payload)
        for field in payload:
            with self.subTest(field=field):
                changed = dict(payload, **{field: "different"})
                self.assertIn("missing_or_changed_content_binding",
                              self.audit(changed, record)["issues"])

    def test_wrong_context_is_not_accepted(self):
        record = self.record({})
        record["grade"] = 11
        self.assertIn("missing_or_conflicting_context", self.audit({}, record)["issues"])

    def test_invalid_future_and_expired_dates(self):
        for updates, expected in (
            ({"checked_at": "2026-10-31"}, "checked_at_in_future"),
            ({"checked_at": "bad"}, "checked_at"),
            ({"effective_from": "2027-01-01"}, "outside_recorded_validity"),
            ({"effective_until": "2026-10-30"}, "outside_recorded_validity"),
        ):
            record = self.record({})
            record["legal"].update(updates)
            self.assertIn(expected, self.audit({}, record)["dimensions"]["legal"]["missing"])

    def test_names_without_locators_and_amendment_review_are_insufficient(self):
        record = self.record({})
        record["textbook"].pop("locator")
        record["legal"].pop("amendment_review")
        result = self.audit({}, record)
        self.assertEqual(result["status"], "insufficient_evidence")

    def test_bad_payload_or_date_is_not_silently_rewritten(self):
        with self.assertRaises(ValueError):
            self.audit({}, day="invalid")
        with self.assertRaises(ValueError):
            content_fingerprint({"x": float("nan")})


if __name__ == "__main__":
    unittest.main()
