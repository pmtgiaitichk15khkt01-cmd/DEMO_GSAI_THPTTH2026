"""Exercise syntax repair on the actual replacement path; no live AI calls."""
import copy
import json
import unittest

from services.context_recovery import repair_exam_context
from services.academic_context import subjects_for_grade


class TestRecoveryJSONPath(unittest.TestCase):
    def source(self):
        return {"p1": [{"q": "Quan sát hình vẽ bên để nhận diện hàm số.",
                        "opt": ["A. 1", "B. 2", "C. 3", "D. 4"],
                        "ans": "B", "topic": "Hàm số"}]}

    def candidate(self):
        return {"subject": "Toán học", "grade": 12, "topic": "Hàm số",
                "q": "Quan sát đồ thị như hình bên của $y=x^3+2$. Tung độ giao điểm với Oy bằng bao nhiêu?",
                "opt": ["A. 1", "B. 2", "C. 3", "D. 4"], "ans": "B"}

    def test_complete_replacement_with_trailing_comma_and_fence_is_recovered(self):
        source = self.source()
        before = copy.deepcopy(source)
        raw = json.dumps({"replacement_question": self.candidate()}, ensure_ascii=False)
        raw = '```json\n' + raw[:-1] + ',}\n```'
        calls = []
        def generate(prompt):
            calls.append(prompt)
            return raw
        result = repair_exam_context(source, "Toán học", 12, ai_generator=generate)
        self.assertEqual(result["context_recovery"]["unresolved"], 0)
        self.assertEqual(len(calls), 1)
        self.assertEqual(result["p1"][0]["f"], {"type": "func_3", "a": 1.0, "b": 0.0, "c": 0.0, "d": 2.0})
        self.assertEqual(result["p1"][0]["opt"], self.candidate()["opt"])
        self.assertEqual(result["p1"][0]["ans"], "B")
        self.assertEqual(source, before)

    def test_valid_string_and_dictionary_replacement_have_identical_results(self):
        payload = {"replacement_question": self.candidate()}
        direct = repair_exam_context(self.source(), "Toán học", 12, ai_generator=lambda _: payload)
        encoded = repair_exam_context(self.source(), "Toán học", 12, ai_generator=lambda _: json.dumps(payload))
        self.assertEqual(direct, encoded)

    def test_latex_fraction_survives_single_or_escaped_json_backslash(self):
        candidate = self.candidate()
        candidate.update(q=r"Quan sát đồ thị như hình bên của $y=\frac{3x-5}{2x+7}$. Tiệm cận đứng là đường thẳng nào?",
                         opt=["A. x=-3.5", "B. x=3.5", "C. x=-1", "D. x=1"], ans="A")
        encoded = json.dumps({"replacement_question": candidate}, ensure_ascii=False)
        for raw in (encoded, encoded.replace(r"\\frac", r"\frac")):
            with self.subTest(raw=raw):
                result = repair_exam_context(self.source(), "Toán học", 12, ai_generator=lambda _: raw)
                self.assertEqual(result["context_recovery"]["unresolved"], 0)
                self.assertEqual(result["p1"][0]["q"], candidate["q"])
                self.assertEqual(result["p1"][0]["opt"], candidate["opt"])
                self.assertEqual(result["p1"][0]["f"], {"type": "func_1_1", "a": 3.0, "b": -5.0, "c": 2.0, "d": 7.0})

    def test_truncated_or_duplicate_replacement_is_not_invented(self):
        payload = json.dumps({"replacement_question": self.candidate()})
        duplicate = payload[:-1] + ',"replacement_question":{}}'
        for raw in (payload[:-2], '{"replacement_question":{"q":"unfinished', duplicate):
            with self.subTest(raw=raw[:50]):
                calls = []
                def generate(prompt):
                    calls.append(prompt)
                    return raw
                source = self.source()
                result = repair_exam_context(source, "Toán học", 12, ai_generator=generate)
                self.assertEqual(result["context_recovery"]["unresolved"], 1)
                self.assertEqual(result["p1"][0]["q"], source["p1"][0]["q"])
                self.assertEqual(result["p1"][0]["ans"], source["p1"][0]["ans"])
                self.assertEqual(len(calls), 1)

    def test_syntax_repair_does_not_accept_wrong_subject(self):
        candidate = self.candidate()
        candidate["subject"] = "Hóa học"
        raw = json.dumps({"replacement_question": candidate})
        raw = raw[:-1] + ',}'
        result = repair_exam_context(self.source(), "Toán học", 12, ai_generator=lambda _: raw)
        self.assertEqual(result["context_recovery"]["unresolved"], 1)

    def test_replacement_json_routing_across_58_non_literature_contexts(self):
        # Synthetic routing fixture only, not curriculum or scientific validation.
        checked = 0
        for grade in range(6, 13):
            for subject in subjects_for_grade(grade):
                if subject == "Ngữ văn":
                    continue  # Literature uses a passage/questions/rubric contract.
                with self.subTest(subject=subject, grade=grade):
                    original = {"q": "Quan sát hình vẽ bên. Nhãn nào được in đậm?",
                                "opt": ["A. A", "B. B", "C. C", "D. D"], "ans": "A", "topic": "QA routing"}
                    replacement = dict(original, subject=subject, grade=grade,
                        composite_visual={"svg": '<svg xmlns="http://www.w3.org/2000/svg"><text font-weight="bold">A</text></svg>'})
                    raw = json.dumps({"replacement_question": replacement}, ensure_ascii=False)
                    raw = '```json\n' + raw[:-1] + ',}\n```'
                    calls = []
                    def generate(prompt):
                        calls.append(prompt)
                        return raw
                    result = repair_exam_context({"p1": [original]}, subject, grade, ai_generator=generate)
                    self.assertEqual(result["context_recovery"]["unresolved"], 0)
                    self.assertEqual(result["p1"][0]["subject"], subject)
                    self.assertEqual(result["p1"][0]["grade"], grade)
                    self.assertEqual(len(calls), 1)
                    checked += 1
        self.assertEqual(checked, 58)

    def test_seven_literature_contexts_keep_passage_and_rubric_atomic(self):
        for grade in range(6, 13):
            with self.subTest(grade=grade):
                source = {"subject": "Ngữ văn", "grade": grade,
                          "part_doc_hieu": {"text": "Ngữ liệu QA tự biên soạn cho kiểm thử.",
                                            "questions": [{"q": "Câu hỏi QA", "ans": "Rubric QA", "point": 1}]},
                          "part_viet": [{"q": "Đề viết QA", "ans": "Rubric viết QA", "point": 6}]}
                before = copy.deepcopy(source)
                calls = []
                result = repair_exam_context(source, "Ngữ văn", grade, ai_generator=lambda p: calls.append(p))
                self.assertEqual(result.pop("context_recovery"), {"events": [], "ai_calls": 0, "unresolved": 0})
                self.assertEqual(result, before)
                self.assertEqual(source, before)
                self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main()
