import copy
import ast
import json
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from services.recovery_diagnostics import recovery_failure_summary, log_recovery_failure


class TestRecoveryDiagnostics(unittest.TestCase):
    def sample(self):
        return {"unresolved": 1, "ai_calls": 2, "events": [{
            "part": "p1", "index": 2, "action": "needs_review",
            "reason": "missing_source_visual", "q": "PRIVATE QUESTION",
            "ans": "PRIVATE ANSWER", "before_sha256": "PRIVATE HASH",
        }], "api_key": "PRIVATE KEY", "student": "PRIVATE NAME"}

    def test_failure_identifies_question_and_reason_without_content(self):
        source = self.sample()
        before = copy.deepcopy(source)
        with self.assertLogs("gsai.exam.recovery", level="WARNING") as captured:
            log_recovery_failure("Toán học", 12, source)
        message = captured.output[0]
        self.assertIn("GSAI_RECOVERY_UNRESOLVED", message)
        payload = json.loads(message.split("GSAI_RECOVERY_UNRESOLVED ", 1)[1])
        self.assertEqual(payload["events"][0]["question"], 3)
        self.assertEqual(payload["events"][0]["reason"], "missing_source_visual")
        self.assertEqual(payload["ai_repair_calls"], 2)
        self.assertNotIn("PRIVATE", message)
        self.assertEqual(source, before)

    def test_unknown_codes_cannot_be_used_to_log_arbitrary_content(self):
        data = {"events": [{"part": "PRIVATE", "index": "PRIVATE",
                            "action": "PRIVATE", "reason": "PRIVATE"}]}
        summary = recovery_failure_summary("PRIVATE", "PRIVATE", data)
        self.assertNotIn("PRIVATE", json.dumps(summary))
        self.assertEqual(summary["events"][0]["reason"], "unknown")

    def test_many_failures_produce_bounded_log(self):
        data = self.sample()
        data["events"] *= 1000
        summary = recovery_failure_summary("Toán học", 12, data)
        self.assertEqual(len(summary["events"]), 32)
        self.assertTrue(summary["events_truncated"])
        self.assertLess(len(json.dumps(summary)), 6500)

    def test_all_supported_subjects_and_grades_keep_safe_context(self):
        low = ["Toán học", "Khoa học tự nhiên", "Ngữ văn", "Tiếng Anh", "Lịch sử & Địa lý", "Tin học", "Giáo dục công dân", "Công nghệ"]
        high = ["Toán học", "Vật lý", "Hóa học", "Sinh học", "Ngữ văn", "Tiếng Anh", "Lịch sử", "Địa lý", "Tin học", "Giáo dục kinh tế và pháp luật", "Công nghệ"]
        checked = 0
        for grade in range(6, 13):
            for subject in low if grade <= 9 else high:
                with self.subTest(subject=subject, grade=grade):
                    summary = recovery_failure_summary(subject, grade, self.sample())
                    self.assertEqual((summary["subject"], summary["grade"]), (subject, grade))
                    checked += 1
        self.assertEqual(checked, 65)

    def test_broken_logging_cannot_change_publication_failure(self):
        with patch("services.recovery_diagnostics._LOGGER.warning", side_effect=RuntimeError("handler failed")):
            self.assertIsNone(log_recovery_failure("Toán học", 12, self.sample()))

    def delivery_function(self, unresolved, subject="Toán học", grade=12):
        # Exercise the actual app delivery boundary without running its UI or AI.
        if not hasattr(self, "_delivery_node"):
            tree = ast.parse((Path(__file__).resolve().parents[1] / "app.py").read_text(encoding="utf-8"))
            self._delivery_node = next(node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name == "enrich_exam_data")
        function = self._delivery_node
        class State(dict):
            __setattr__ = dict.__setitem__
            __getattr__ = dict.__getitem__
        recovery = self.sample()
        recovery["unresolved"] = unresolved
        scope = {
            "subject": subject, "grade_num": grade, "ree": None,
            "st": SimpleNamespace(session_state=State()),
            "validate_exam_context": Mock(),
            "repair_exam_context": Mock(return_value={"context_recovery": recovery}),
            "call_gemini_with_fallback": Mock(),
            "prepare_exam_for_delivery": Mock(return_value={"p1": []}),
        }
        exec(compile(ast.Module(body=[function], type_ignores=[]), "app_delivery_boundary", "exec"), scope)
        return scope

    def test_app_failed_delivery_logs_without_opening_exam_or_calling_more_ai(self):
        scope = self.delivery_function(1)
        with self.assertLogs("gsai.exam.recovery", level="WARNING") as captured:
            with self.assertRaisesRegex(ValueError, "Còn câu chưa đủ dữ liệu"):
                scope["enrich_exam_data"]({"p1": []})
        self.assertNotIn("PRIVATE", " ".join(captured.output))
        scope["prepare_exam_for_delivery"].assert_not_called()
        scope["call_gemini_with_fallback"].assert_not_called()
        self.assertEqual(scope["repair_exam_context"].call_args.kwargs["max_ai_questions"], 2)

    def test_app_successful_delivery_is_unchanged_and_does_not_log_failure(self):
        scope = self.delivery_function(0)
        with patch("services.recovery_diagnostics._LOGGER.warning") as log:
            result = scope["enrich_exam_data"]({"p1": []})
        self.assertEqual(result, {"p1": [], "exam_count": 1})
        log.assert_not_called()
        scope["call_gemini_with_fallback"].assert_not_called()

    def test_actual_delivery_boundary_across_65_contexts(self):
        low = ["Toán học", "Khoa học tự nhiên", "Ngữ văn", "Tiếng Anh", "Lịch sử & Địa lý", "Tin học", "Giáo dục công dân", "Công nghệ"]
        high = ["Toán học", "Vật lý", "Hóa học", "Sinh học", "Ngữ văn", "Tiếng Anh", "Lịch sử", "Địa lý", "Tin học", "Giáo dục kinh tế và pháp luật", "Công nghệ"]
        checked = 0
        for grade in range(6, 13):
            for subject in low if grade <= 9 else high:
                for unresolved in (0, 1):
                    with self.subTest(subject=subject, grade=grade, unresolved=unresolved):
                        scope = self.delivery_function(unresolved, subject, grade)
                        with patch("services.recovery_diagnostics._LOGGER.warning") as log:
                            if unresolved:
                                with self.assertRaisesRegex(ValueError, "Còn câu chưa đủ dữ liệu"):
                                    scope["enrich_exam_data"]({})
                                payload = json.loads(log.call_args.args[1])
                                self.assertEqual((payload["subject"], payload["grade"]), (subject, grade))
                            else:
                                self.assertEqual(scope["enrich_exam_data"]({})["exam_count"], 1)
                                log.assert_not_called()
                        scope["call_gemini_with_fallback"].assert_not_called()
                checked += 1
        self.assertEqual(checked, 65)


if __name__ == "__main__":
    unittest.main()
