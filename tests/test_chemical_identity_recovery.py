import copy
import unittest
from services.context_recovery import _question_issue, repair_exam_context

class TestChemicalIdentityRecovery(unittest.TestCase):
    def question(self, stem):
        return {"q": stem, "opt": ["A. 10", "B. 40", "C. 20", "D. 22"],
                "ans": "C", "subject": "Khoa học tự nhiên", "grade": 7,
                "topic": "Nguyên tử"}

    def test_live_stem_is_routed_to_existing_recovery(self):
        original = self.question("Nguyên tử calcium (vôi sống) có 20 proton. Số electron là bao nhiêu?")
        source = {"p1": [original], "p2": [], "p3": []}
        before = copy.deepcopy(source)
        candidate = self.question("Nguyên tử calcium có 20 proton. Số electron của nguyên tử trung hòa là bao nhiêu?")
        calls = []
        def generate(prompt):
            calls.append(prompt)
            return {"replacement_question": candidate}
        result = repair_exam_context(source, "Khoa học tự nhiên", 7, ai_generator=generate)
        self.assertEqual(source, before)
        self.assertEqual(len(calls), 1)
        self.assertEqual(result["context_recovery"]["unresolved"], 0)
        self.assertEqual(result["p1"][0]["replacement_audit"]["reason"], "chemical_identity_mismatch")
        self.assertTrue(result["p1"][0]["is_ai_generated"])

    def test_correct_compound_and_element_are_not_rejected(self):
        for stem in ("Calcium oxide (vôi sống) có công thức CaO.",
                     "Calcium (canxi) có 20 proton.",
                     "Calcium không phải vôi sống.",
                     "Calcium (vôi sống): nhận định đúng hay sai?"):
            self.assertEqual(_question_issue(self.question(stem), "p1", "Khoa học tự nhiên", 7), "")

    def test_distractors_are_not_mistaken_for_stem_claims(self):
        q = self.question("Chất nào sau đây là vôi sống?")
        q["opt"] = ["A. calcium (vôi sống)", "B. CaO", "C. NaCl", "D. H2O"]
        q["ans"] = "B"
        self.assertEqual(_question_issue(q, "p1", "Khoa học tự nhiên", 7), "")
