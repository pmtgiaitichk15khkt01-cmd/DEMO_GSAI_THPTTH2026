import copy
import unittest
from unittest.mock import Mock

from services.bbt_display_contract import aligned_bbt_rows
from services.context_recovery import has_visual, repair_exam_context


class TestBbtVisualNewlines(unittest.TestCase):
    def question(self, escaped):
        bbt = "x | -inf | -1 | 1 | +inf\ny' | + | 0 | - | 0 | +\ny | -inf | 2 | -2 | +inf"
        return {"q": "Cho bảng biến thiên sau. Xét các nhận định.",
                "bbt": bbt.replace("\n", r"\n") if escaped else bbt,
                "stmts": [{"t": f"Nhận định {i}", "a": True} for i in range(4)]}

    def test_renderer_and_presence_check_agree_for_literal_newlines(self):
        for escaped in (False, True):
            with self.subTest(escaped=escaped):
                q = self.question(escaped)
                self.assertIsNotNone(aligned_bbt_rows(q["bbt"]))
                self.assertTrue(has_visual(q))

    def test_complete_table_does_not_spend_ai_repair_budget(self):
        q = self.question(True)
        original = copy.deepcopy(q)
        generator = Mock(side_effect=AssertionError("Complete BBT must not call AI"))
        result = repair_exam_context({"p2": [q]}, "Toán", 12, ai_generator=generator)
        generator.assert_not_called()
        self.assertEqual(result["context_recovery"]["unresolved"], 0)
        self.assertEqual(result["p2"][0], original)
        self.assertEqual(q, original)

    def test_single_line_pipes_are_not_invented_as_a_table(self):
        self.assertFalse(has_visual({"bbt": "x | -inf | 0 | +inf"}))
