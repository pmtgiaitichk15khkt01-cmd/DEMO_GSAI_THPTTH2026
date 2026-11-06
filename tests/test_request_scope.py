import ast
import copy
import json
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import Mock

from services.academic_context import subjects_for_grade
from services.context_recovery import repair_exam_context
from services.curriculum_policy import exam_prompt, prepare_exam_for_delivery
from services.request_scope import explicit_request_scope, question_scope_issue


REQUEST = "Toán lớp 12, chỉ khảo sát hàm bậc ba; không dùng hàm bậc bốn."


def question(formula, **extra):
    return dict({"subject": "Toán học", "grade": 12, "topic": "Hàm số", "level": "TH",
                 "q": "Cho hàm số $y=" + formula + "$ có bao nhiêu điểm cực trị?",
                 "opt": ["A. 0", "B. 1", "C. 2", "D. 3"], "ans": "A"}, **extra)


class TestRequestScope(unittest.TestCase):
    def scope(self):
        return explicit_request_scope("Toán", REQUEST)

    def test_recognizes_explicit_only_but_not_negated_or_counted_request(self):
        for text in ("Chỉ hàm bậc ba", "chỉ dùng hàm số bậc 3", REQUEST, "only cubic functions"):
            self.assertTrue(explicit_request_scope("Toán học", text), text)
        for text in ("Không chỉ hàm bậc ba", "không phải chỉ hàm bậc ba", "không chỉ dùng hàm bậc ba", "Hãy chỉ ra hàm số bậc ba trong các công thức", "3 câu hàm bậc ba và 2 câu phân thức", "chỉ 3 câu hàm bậc ba", "Khảo sát hàm bậc ba và phân thức"):
            self.assertEqual(explicit_request_scope("Toán học", text), {}, text)

    def test_monotonicity_does_not_change_polynomial_family(self):
        for formula in ("x^3+x", "-x^3-x", "x^3-3x", r"\frac{1}{3}x^3+x"):
            self.assertEqual(question_scope_issue(question(formula), self.scope()), "", formula)
        for formula in ("x", "-x", "x^2", "x^4", r"\frac{2x-1}{x+1}"):
            self.assertEqual(question_scope_issue(question(formula), self.scope()), "outside_explicit_request", formula)

    def test_live_wording_of_vertical_asymptote_is_recognized(self):
        q = question("x^3")
        q["q"] = r"Đường tiệm cận đứng của đồ thị hàm số $y=\frac{2x-1}{x+1}$ là:"
        self.assertEqual(question_scope_issue(q, self.scope()), "outside_explicit_request")

    def test_tangent_line_and_derivative_are_not_the_original_function(self):
        q = question("x^3+x")
        q["q"] += " Tiếp tuyến tại một điểm có phương trình $y=4x-2$. Đạo hàm $y'=3x^2+1$."
        self.assertEqual(question_scope_issue(q, self.scope()), "")

    def test_cancellation_does_not_erase_domain_hole(self):
        for expression in (r"\frac{x^4}{x}", "(x^4)/(x)", "x^4/x"):
            self.assertEqual(question_scope_issue(question(expression), self.scope()), "outside_explicit_request")

    def test_incorrect_model_label_and_conflicting_expression_are_not_trusted(self):
        zero = question("x^2", f={"type": "func_3", "a": 0, "b": 1, "c": 0, "d": 0})
        conflict = question(r"\frac{2x-1}{x+1}", f={"type": "func_3", "a": 1, "b": 0, "c": 0, "d": 0})
        self.assertEqual(question_scope_issue(zero, self.scope()), "outside_explicit_request")
        self.assertEqual(question_scope_issue(conflict, self.scope()), "outside_explicit_request")

    def test_unknown_expression_is_not_a_blanket_rejection(self):
        q = question("a x^3+b x+c")
        self.assertEqual(question_scope_issue(q, self.scope()), "")

    def test_unrelated_requests_do_not_change_65_contexts(self):
        checked = 0
        for grade in range(6, 13):
            for subject in subjects_for_grade(grade):
                with self.subTest(subject=subject, grade=grade):
                    self.assertEqual(explicit_request_scope(subject, "Câu hỏi ngắn phù hợp lớp đang chọn"), {})
                    if subject != "Toán học":
                        self.assertEqual(explicit_request_scope(subject, REQUEST), {})
                    checked += 1
        self.assertEqual(checked, 65)

    def test_valid_cubic_does_not_call_bank_or_ai(self):
        bank = Mock(); ai = Mock()
        source = {"p1": [question("x^3")]}
        result = repair_exam_context(source, "Toán học", 12, ai_generator=ai, bank_provider=bank, custom_request=REQUEST)
        self.assertEqual(result["context_recovery"]["unresolved"], 0)
        ai.assert_not_called(); bank.assert_not_called()

    def test_bank_replacement_obeys_request_and_teacher_topic(self):
        source = {"p1": [question(r"\frac{2x-1}{x+1}", topic="Tiệm cận")]}
        before = copy.deepcopy(source)
        ai = Mock()
        result = repair_exam_context(source, "Toán học", 12, topics=["Hàm số"],
            bank_provider=lambda *_: {"p1": [question("x"), question("x^3")]}, ai_generator=ai, custom_request=REQUEST)
        self.assertEqual(result["context_recovery"]["unresolved"], 0)
        self.assertEqual(result["p1"][0]["q"], question("x^3")["q"])
        self.assertEqual(source, before)
        ai.assert_not_called()

    def test_ai_replacement_receives_request_and_wrong_family_is_not_accepted(self):
        calls = []
        def ai(prompt):
            calls.append(prompt)
            return {"replacement_question": question("x")}
        source = {"p1": [question(r"\frac{2x-1}{x+1}")]}
        result = repair_exam_context(source, "Toán học", 12, topics=["Hàm số"], ai_generator=ai, custom_request=REQUEST)
        self.assertEqual(len(calls), 1)
        self.assertIn(REQUEST, calls[0])
        self.assertEqual(result["context_recovery"]["unresolved"], 1)
        self.assertEqual(result["context_recovery"]["events"][0]["reason"], "outside_explicit_request")
        self.assertEqual(result["p1"][0]["ans"], source["p1"][0]["ans"])

    def test_out_of_scope_question_is_replaced_then_delivered(self):
        source = {"p1": [question(r"\frac{2x-1}{x+1}")]}
        calls = []
        def ai(prompt):
            calls.append(prompt)
            return {"replacement_question": question("x^3")}
        repaired = repair_exam_context(source, "Toán học", 12, topics=["Hàm số"], ai_generator=ai, custom_request=REQUEST)
        self.assertEqual(repaired["context_recovery"]["unresolved"], 0)
        self.assertEqual(len(calls), 1)
        delivered = prepare_exam_for_delivery(repaired, "Toán học", 12, custom_request=REQUEST)
        self.assertEqual(delivered["p1"][0]["q"], question("x^3")["q"])

    def test_final_delivery_catches_contradiction_but_default_path_stays_open(self):
        exam = {"p1": [question(r"\frac{2x-1}{x+1}")]}
        with self.assertRaisesRegex(ValueError, "chưa khớp yêu cầu"):
            prepare_exam_for_delivery(exam, "Toán học", 12, custom_request=REQUEST)
        self.assertEqual(prepare_exam_for_delivery(exam, "Toán học", 12)["subject"], "Toán học")

    def test_generation_prompt_repeats_only_recognized_scope(self):
        self.assertIn("CHỈ HÀM BẬC BA", exam_prompt("Toán học", 12, ["Hàm số"], (3, 1, 1), "1234", REQUEST))
        self.assertNotIn("CHỈ HÀM BẬC BA", exam_prompt("Tiếng Anh", 6, ["School"], (3, 0, 0), "1234", REQUEST))

    def test_app_passes_explicit_snapshot_not_stale_session_request(self):
        tree = ast.parse((Path(__file__).resolve().parents[1]/"app.py").read_text(encoding="utf-8"))
        function = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "enrich_exam_data")
        class State(dict):
            __setattr__ = dict.__setitem__
            __getattr__ = dict.__getitem__
        scope = {"st": SimpleNamespace(session_state=State(custom_request_text="STALE REQUEST")),
                 "subject": "Toán học", "grade_num": 12, "ree": None,
                 "validate_exam_context": Mock(), "call_gemini_with_fallback": Mock(),
                 "repair_exam_context": Mock(return_value={"context_recovery": {"unresolved": 0}}),
                 "prepare_exam_for_delivery": Mock(return_value={})}
        exec(compile(ast.Module(body=[function], type_ignores=[]), "app_request_boundary", "exec"), scope)
        scope["enrich_exam_data"]({}, custom_request=REQUEST)
        self.assertEqual(scope["repair_exam_context"].call_args.kwargs["custom_request"], REQUEST)
        self.assertEqual(scope["prepare_exam_for_delivery"].call_args.kwargs["custom_request"], REQUEST)
        self.assertEqual(scope["repair_exam_context"].call_args.kwargs["max_ai_questions"], 2)


if __name__ == "__main__":
    unittest.main()
