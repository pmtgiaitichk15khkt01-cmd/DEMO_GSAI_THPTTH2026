import copy
import unittest

from services.context_recovery import model_from_explicit_formula, recover_visual, repair_exam_context
from services.pdf_source_visuals import extract_pdf_question_visuals


class TestContextRecovery(unittest.TestCase):
    def missing(self, suffix=""):
        return {"q": "Quan sát hình vẽ bên để nhận diện hàm số " + suffix,
                "opt": ["A. 1", "B. 2", "C. 3", "D. 4"], "ans": "B", "topic": "Hàm số"}

    def replacement(self, **overrides):
        q = {"subject": "Toán học", "grade": 12, "topic": "Hàm số", "q": "Quan sát đồ thị như hình bên của hàm số $y=x^3+2$. Tung độ giao điểm với Oy bằng bao nhiêu?",
             "opt": ["A. 1", "B. 2", "C. 3", "D. 4"], "ans": "B"}
        q.update(overrides)
        return q

    def test_explicit_cubic_coefficients_are_recovered_without_mutation(self):
        q = self.missing(); q["q"] = "Đồ thị như hình vẽ bên của hàm số $y=2x^3-4x^2+3x-7$."
        before = copy.deepcopy(q)
        result = recover_visual(q, "Toán", 12)
        self.assertEqual(result["f"], {"type": "func_3", "a": 2.0, "b": -4.0, "c": 3.0, "d": -7.0})
        self.assertEqual(q, before)
        self.assertEqual(result["opt"], before["opt"])

    def test_rational_recovery_uses_existing_tikz_builder_with_exact_coefficients(self):
        q = self.missing(); q["q"] = r"Đồ thị như hình bên: $y=\frac{3x-5}{2x+7}$."
        result = recover_visual(q, "Toán học", 12)
        self.assertEqual(result["f"], {"type": "func_1_1", "a": 3.0, "b": -5.0, "c": 2.0, "d": 7.0})
        self.assertIn("tikz", result)

    def test_no_template_for_unsupported_or_incomplete_formula(self):
        for expression in ("y=sin(x)", "y=x^3+", "y=__import__('os')", "y=x^5"):
            self.assertIsNone(model_from_explicit_formula(expression))

    def test_answer_options_do_not_supply_the_missing_original_figure(self):
        q = self.missing(); q["opt"][1] = "B. y=x^3-3x+2"
        self.assertNotIn("f", recover_visual(q, "Toán", 12))

    def test_a_function_is_not_a_missing_variation_table(self):
        q = self.missing(); q["q"] = "Bảng biến thiên của $y=x^3-3x+2$ như hình bên."
        self.assertNotIn("f", recover_visual(q, "Toán", 12))
        self.assertNotIn("bbt", recover_visual(q, "Toán", 12))

    def test_lower_grade_does_not_get_a_cubic_illustration(self):
        q = self.missing(); q["q"] += " $y=x^3-3x+2$"
        self.assertNotIn("f", recover_visual(q, "Toán", 6))

    def test_bank_replacement_checks_subject_grade_and_topic(self):
        pool = [self.replacement(subject="Hóa học"), self.replacement(grade=11), self.replacement(topic="Hình học"), self.replacement()]
        result = repair_exam_context({"p1": [self.missing()]}, "Toán", 12, bank_provider=lambda *_: {"p1": pool})
        self.assertEqual(result["context_recovery"]["unresolved"], 0)
        self.assertEqual(result["p1"][0]["q"], pool[-1]["q"])
        self.assertEqual(result["p1"][0]["replacement_audit"]["origin"], "bank_replacement")

    def test_ai_replaces_the_whole_question_and_is_not_labeled_real_bank(self):
        source = {"p1": [self.missing()]}; before = copy.deepcopy(source)
        candidate = self.replacement(school="Trường do AI tự khai", source_url="https://example.edu.vn/fake", is_real_bank_question=True)
        result = repair_exam_context(source, "Toán", 12, ai_generator=lambda _: {"replacement_question": candidate})
        self.assertEqual(source, before)
        self.assertNotEqual(result["p1"][0]["q"], source["p1"][0]["q"])
        self.assertTrue(result["p1"][0]["is_ai_generated"])
        self.assertFalse(result["p1"][0]["is_real_bank_question"])
        self.assertNotIn("school", result["p1"][0])
        self.assertNotIn("source_url", result["p1"][0])

    def test_mismatched_ai_replacement_is_rejected(self):
        result = repair_exam_context({"p1": [self.missing()]}, "Toán", 12,
            ai_generator=lambda _: {"replacement_question": self.replacement(grade=11)})
        self.assertEqual(result["context_recovery"]["unresolved"], 1)

    def test_independently_wrong_answer_is_not_an_acceptable_replacement(self):
        wrong = self.replacement(q="Hàm số $y=x^3$ có bao nhiêu cực trị?", opt=["A. 0", "B. 1", "C. 2", "D. 3"], ans="B")
        result = repair_exam_context({"p1": [self.missing()]}, "Toán", 12, ai_generator=lambda _: {"replacement_question": wrong})
        self.assertEqual(result["context_recovery"]["unresolved"], 1)

    def test_ai_calls_are_bounded_and_failure_keeps_the_original(self):
        calls = []
        def failed(prompt):
            calls.append(prompt)
            raise TimeoutError("test timeout")
        source = {"p1": [self.missing(str(i)) for i in range(3)]}
        result = repair_exam_context(source, "Toán", 12, ai_generator=failed, max_ai_questions=2)
        self.assertEqual(len(calls), 2)
        self.assertEqual(result["context_recovery"]["unresolved"], 3)
        self.assertEqual(result["p1"][0]["q"], source["p1"][0]["q"])

    def test_same_bank_question_is_not_reused_for_two_repairs(self):
        result = repair_exam_context({"p1": [self.missing("1"), self.missing("2")]}, "Toán", 12,
                                     bank_provider=lambda *_: {"p1": [self.replacement()]})
        self.assertEqual(result["context_recovery"]["unresolved"], 1)


class TestPdfSourceVisuals(unittest.TestCase):
    def pdf(self, duplicate=False):
        import pymupdf
        document = pymupdf.open()
        for index in range(2 if duplicate else 1):
            page = document.new_page()
            page.insert_text((40, 30), "PHAN I")
            page.insert_text((40, 75), "Cau 1: Quan sat hinh ben")
            page.draw_rect((70, 100, 200, 165))
            if not duplicate:
                page.insert_text((40, 240), "PHAN II")
                page.insert_text((40, 280), "Cau 1: Quan sat hinh ben")
                page.draw_circle((150, 360), 35)
        content = document.tobytes(); document.close()
        return content

    def test_same_number_in_two_parts_does_not_overwrite(self):
        result = extract_pdf_question_visuals(self.pdf())
        self.assertIn("p1_q_1", result)
        self.assertIn("p2_q_1", result)
        self.assertNotIn("q_1", result)
        self.assertNotEqual(result["p1_q_1"], result["p2_q_1"])
        self.assertEqual(result["_regions"]["p2_q_1"]["part"], "p2")

    def test_repeated_exam_number_is_marked_ambiguous(self):
        result = extract_pdf_question_visuals(self.pdf(duplicate=True))
        self.assertNotIn("p1_q_1", result)
        self.assertIn("p1_q_1", result["_ambiguous"])

    def test_scanner_limits_are_explicit(self):
        result = extract_pdf_question_visuals(self.pdf(duplicate=True), max_pages=1)
        self.assertTrue(result["_truncated"])
