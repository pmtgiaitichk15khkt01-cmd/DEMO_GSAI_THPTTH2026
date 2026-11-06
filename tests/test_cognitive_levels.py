import ast
from copy import deepcopy
import json
from pathlib import Path
import re
import unittest

from services.cognitive_levels import annotate_question, audit_exam_levels, normalize_level, level_caption
from services.curriculum_policy import exam_prompt, lesson_prompt, prepare_exam_for_delivery
from services.context_recovery import repair_exam_context


class TestCognitiveLevels(unittest.TestCase):
    def test_audit_fingerprint_covers_code_visuals_context_and_rubric(self):
        from services.cognitive_levels import assessment_content_hash
        question = {"q": "Predict output", "ans": "C", "level": "TH",
                    "code": "#heading {color:red}", "element": '<h2 id="heading">X</h2>',
                    "image": "diagram-a.svg", "table": [[1, 2]],
                    "source_locator": "0525/page1/Q1", "solution_steps": ["Resolve priority"],
                    "stmts": [{"t": "statement", "ans": True}]}
        original = deepcopy(question)
        digest = annotate_question(question)["cognitive_audit"]["content_sha256"]
        self.assertEqual(digest, assessment_content_hash(question))
        self.assertEqual(question, original)
        for field in ("code", "element", "image", "table", "source_locator", "solution_steps", "stmts"):
            with self.subTest(field=field):
                changed = deepcopy(question)
                changed[field] = "changed evidence"
                self.assertNotEqual(digest, annotate_question(changed)["cognitive_audit"]["content_sha256"])
        question["cognitive_audit"] = {"verified": True, "content_sha256": "forged"}
        self.assertEqual(digest, annotate_question(question)["cognitive_audit"]["content_sha256"])
        self.assertFalse(annotate_question(question)["cognitive_audit"]["verified"])

    def test_aliases_do_not_collapse_ambiguous_or_empty_claims(self):
        for raw, expected in [("Nhận biết", "NB"), ("Hiểu", "TH"), ("Vận dụng cao", "VDC"),
                              ("NB-TH", ""), ("TH-VD", ""), (None, ""), ("NB/TH/VD/VDC", "")]:
            self.assertEqual(normalize_level(raw), expected)

    def test_self_reported_or_forged_verified_evidence_is_not_approval(self):
        q = {"q": "Chỉ cần nhớ dữ kiện", "level": "VDC", "learning_outcome": "tự khai",
             "cognitive_rationale": "tự khai", "solution_steps": ["tự khai"],
             "cognitive_audit": {"verified": True}}
        result = annotate_question(q)
        self.assertFalse(result["cognitive_audit"]["verified"])
        self.assertTrue(result["cognitive_audit"]["self_reported_evidence_present"])
        self.assertEqual(result["cognitive_audit"]["reference_bucket"], "Vận dụng")
        self.assertIn("chưa duyệt", level_caption(result))

    def test_delivery_does_not_relabel_by_question_format(self):
        exam = {"p1": [{"q": "Tìm cách giải mới", "level": "VDC", "opt": ["1", "2", "3", "4"], "ans": "A"}],
                "p3": [{"q": "Nhớ lại một dữ kiện", "level": "NB", "ans": "2"}]}
        before = deepcopy(exam)
        result = prepare_exam_for_delivery(exam, "Toán", 6)
        self.assertEqual(exam, before)
        self.assertEqual(result["p1"][0]["level"], "VDC")
        self.assertEqual(result["p3"][0]["level"], "NB")
        self.assertNotIn("percentages", result["cognitive_audit"])

    def test_tf_statements_have_separate_claims_and_unknown_parent(self):
        result = audit_exam_levels({"p2": [{"q": "Ngữ liệu", "stmts": [
            {"t": "a", "level": "NB"}, {"t": "b", "level": "TH"},
            {"t": "c", "level": "VD"}, {"t": "d", "level": "VDC"}]}]})
        self.assertEqual(result["cognitive_audit"]["statement_claim_counts"], {"NB": 1, "TH": 1, "VD": 1, "VDC": 1})
        self.assertFalse(result["p2"][0].get("level"))
        self.assertEqual(len(result["cognitive_audit"]["rows"]), 5)

    def test_literature_reading_and_writing_are_both_audited(self):
        result = audit_exam_levels({"part_doc_hieu": {"questions": [{"q": "Đọc", "level": "TH"}]},
                                    "part_viet": [{"q": "Viết", "level": "VD"}]})
        self.assertEqual(result["cognitive_audit"]["question_claim_counts"], {"VD": 1, "TH": 1})

    def test_legacy_pipeline_no_longer_invents_missing_level(self):
        import real_exam_engine as engine
        exam = {"p1": [{"q": "Nêu dữ kiện", "opt": ["1", "2", "3", "4"], "ans": "A"}],
                "p3": [{"q": "Ghi số", "ans": "1"}]}
        result = engine.apply_full_7layer_quality_pipeline(exam, "Toán", 6)
        self.assertEqual(result["p1"][0]["level"], "")
        self.assertEqual(result["p3"][0]["level"], "")

    def test_generation_prompts_require_outcome_and_reason_for_each_unit(self):
        for subject in ("Toán", "Ngữ văn"):
            prompt = exam_prompt(subject, 6, ["Bài học"], (1, 1, 1), "1234")
            self.assertIn('"cognitive_rationale"', prompt)
            self.assertIn('"solution_steps"', prompt)
            self.assertIn("không đồng nhất tỷ lệ số câu", prompt)
        self.assertIn("COGNITIVE_REASON:", lesson_prompt("Toán", 6, "Phân số"))

    def test_station1_parser_no_default_vd_and_keeps_evidence_out_of_question(self):
        path = Path(__file__).resolve().parents[1] / "app.py"
        tree = ast.parse(path.read_text(encoding="utf-8"))
        fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "parse_quiz_questions")
        namespace = {"re": re, "json": json, "annotate_question": annotate_question,
                     "sanitize_katex_latex": lambda x: x, "format_pedagogical_math": None}
        exec(compile(ast.Module(body=[fn], type_ignores=[]), "quiz-parser", "exec"), namespace)
        text = 'Câu 1. Tính một nửa của 4?\nOUTCOME: biểu diễn phân số\nCOGNITIVE_REASON: nhận ra quan hệ\nCOGNITIVE_STEPS: ["nhận ra"]\nA. 1\nB. 2\nC. 3\nD. 4\nCORRECT: B\nEXPLAIN: Một nửa là 2.'
        q = namespace["parse_quiz_questions"](text)[0]
        self.assertEqual(q["level"], "")
        self.assertEqual(q["learning_outcome"], "biểu diễn phân số")
        self.assertNotIn("OUTCOME", q["question"])

    def test_replacement_cannot_silently_change_declared_cognitive_target(self):
        source = {"p1": [{"q": "Quan sát hình bên", "topic": "Hàm số", "level": "VDC",
                          "opt": ["1", "2", "3", "4"], "ans": "A"}]}
        candidate = {"subject": "Toán học", "grade": 12, "topic": "Hàm số", "level": "NB",
            "q": "Nhìn đồ thị hình bên của $y=x^3$. Giá trị tại x=0?", "opt": ["0", "1", "2", "3"], "ans": "A"}
        result = repair_exam_context(source, "Toán", 12, ai_generator=lambda _: {"replacement_question": candidate})
        self.assertEqual(result["context_recovery"]["unresolved"], 1)
        self.assertEqual(result["p1"][0]["level"], "VDC")

    def test_metadata_does_not_count_solution_length_as_cognitive_demand(self):
        q = annotate_question({"q": "Tính toán dài", "solution_steps": ["cộng"] * 20})
        self.assertEqual(q["level"], "")
        self.assertFalse(q["cognitive_audit"]["self_reported_evidence_present"])

    def test_schema_normalization_preserves_each_statement_evidence(self):
        from real_exam_engine import normalize_exam_schema
        for field, statement in [("stmts", {"t": "Đọc dữ kiện", "a": False}),
                                 ("items", {"statement": "Đọc dữ kiện", "ans": False}),
                                 ("statements", {"text": "Đọc dữ kiện", "correct": False})]:
            statement.update(level="NB", learning_outcome="nhận ra dữ kiện", cognitive_rationale="đọc trực tiếp", solution_steps=["đọc"])
            q = normalize_exam_schema({"p2": [{"q": "Ngữ liệu", field: [statement]}]}, "Toán", 6)["p2"][0]["stmts"][0]
            self.assertEqual(q["level"], "NB")
            self.assertEqual(q["solution_steps"], ["đọc"])
            self.assertFalse(q["a"])
            self.assertEqual(q["t"], "Đọc dữ kiện")
