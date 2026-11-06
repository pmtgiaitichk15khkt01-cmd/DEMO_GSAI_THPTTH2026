import copy
import unittest
from unittest.mock import Mock

from services.context_recovery import recover_visual, repair_exam_context
from services.math_conditions import math_condition_conflict


TABLE = "x | -inf | -1 | 1 | +inf\ny' | + | 0 | - | 0 | +\ny | -inf | 3 | -1 | +inf"


class TestInlineBbtRecovery(unittest.TestCase):
    def question(self, ambiguous=False):
        return {"q": "Cho hàm số có bảng biến thiên như sau:\n\n" + TABLE +
                "\n\nHàm số đã cho đồng biến trên khoảng nào dưới đây?",
                "opt": ['A. $(-1;1)$', 'B. $(1;3)$' if ambiguous else 'B. $(-2;0)$',
                        r'C. $(-\infty;-1)$', 'D. $(0;1)$'], "ans": "C"}

    def test_complete_inline_table_moves_to_existing_visual_field_without_data_loss(self):
        q = self.question()
        before = copy.deepcopy(q)
        result = recover_visual(q, "Toán", 12)
        self.assertEqual(result.get("bbt"), TABLE)
        self.assertNotIn(TABLE, result["q"])
        self.assertIn("Hàm số đã cho đồng biến", result["q"])
        self.assertEqual(result["opt"], before["opt"])
        self.assertEqual(result["ans"], before["ans"])
        self.assertEqual(q, before)

    def test_complete_valid_inline_table_does_not_call_ai(self):
        generator = Mock(side_effect=AssertionError("must not call AI"))
        result = repair_exam_context({"p1": [self.question()]}, "Toán", 12, ai_generator=generator)
        generator.assert_not_called()
        self.assertEqual(result["context_recovery"]["unresolved"], 0)

    def test_observed_subinterval_and_full_interval_are_both_counted(self):
        q = recover_visual(self.question(True), "Toán", 12)
        self.assertEqual(math_condition_conflict(q), "bbt_interval_choice_not_unique")
        q["opt"][1] = 'B. $(-2;0)$'
        self.assertEqual(math_condition_conflict(q), '')
        q["ans"] = 'A'
        self.assertEqual(math_condition_conflict(q), "bbt_interval_key_mismatch")

    def test_missing_or_two_tables_are_not_guessed_and_other_subject_is_unchanged(self):
        for text in (TABLE.split("\ny |")[0], TABLE + "\n\n" + TABLE):
            q = {"q": "Cho bảng biến thiên sau:\n" + text}
            self.assertNotIn("bbt", recover_visual(q, "Toán", 12))
        q = self.question()
        self.assertEqual(recover_visual(q, "Vật lí", 12), q)

    def test_unknown_option_format_is_not_a_false_rejection(self):
        q = {**self.question(), "bbt": TABLE}
        q["opt"][0] = "A. Không có khoảng nào"
        self.assertEqual(math_condition_conflict(q), '')

    def test_same_sign_intervals_can_cross_stationary_point_but_not_a_pole(self):
        q = {"q": "Hàm số đồng biến trên khoảng nào dưới đây?",
             "bbt": "x | -inf | 0 | +inf\ny' | + | 0 | +\ny | -inf | 0 | +inf",
             "opt": [r'A. $(-\infty;+\infty)$', 'B. $(-2;0)$', 'C. $(0;2)$', 'D. $(-1;1)$'], "ans": "A"}
        self.assertEqual(math_condition_conflict(q), "bbt_interval_choice_not_unique")
        q["bbt"] = "x | -inf | 0 | +inf\ny' | + | || | +\ny | 0 | +inf || -inf | 0"
        q["opt"] = [r'A. $(-\infty;+\infty)$', 'B. $(-2;0)$', 'C. $(-1;1)$', 'D. $(-3;2)$']
        q["ans"] = 'B'
        self.assertEqual(math_condition_conflict(q), '')

    def test_ambiguous_table_enters_existing_replacement_path_without_key_rewrite(self):
        q = self.question(True)
        original = copy.deepcopy(q)
        result = repair_exam_context({"p1": [q]}, "Toán", 12)
        self.assertEqual(result["context_recovery"]["unresolved"], 1)
        self.assertEqual(result["p1"][0]["ans"], "C")
        self.assertEqual(q, original)
        self.assertEqual(result["context_recovery"]["events"][0]["reason"],
                         "independently_detected_answer_mismatch")

    def test_partial_domain_and_non_monotonic_tasks_are_not_rejected(self):
        q = {"q": "Hàm số đồng biến trên khoảng nào dưới đây?",
             "bbt": "x | -2 | 0 | 2\ny' | + | 0 | -\ny | 0 | 1 | 0",
             "opt": ['A. $(-3;0)$', 'B. $(-2;0)$', 'C. $(0;1)$', 'D. $(0;2)$'], "ans": "A"}
        self.assertEqual(math_condition_conflict(q), '')
        q = recover_visual(self.question(True), "Toán", 12)
        q['q'] = 'Hàm số không đồng biến trên khoảng nào dưới đây?'
        self.assertEqual(math_condition_conflict(q), '')

    def test_decreasing_task_and_duplicate_correct_intervals(self):
        q = recover_visual(self.question(), "Toán", 12)
        q['q'] = 'Hàm số nghịch biến trên khoảng nào dưới đây?'
        q['opt'] = ['A. $(-1;1)$', 'B. $(-2;0)$', r'C. $(-\\infty;-1)$', 'D. $(1;2)$']
        q['ans'] = 'A'
        self.assertEqual(math_condition_conflict(q), '')
        q['opt'][3] = 'D. $(0;1)$'
        self.assertEqual(math_condition_conflict(q), 'bbt_interval_choice_not_unique')
