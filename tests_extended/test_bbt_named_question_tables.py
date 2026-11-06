import unittest
from services.bbt_display_contract import aligned_bbt_rows


class NamedQuestionTables(unittest.TestCase):
    def test_labels_and_values_preserved_without_function_whitelist(self):
        for variable, function, derivative in (
            ('t', 'V(t)', "V'(t)"),
            ('h', 'Revenue(h)', "Revenue′(h)"),
            (r'$\theta$', r'$\Phi(\theta)$', r'$\Phi^{\prime}(\theta)$'),
        ):
            with self.subTest(function=function):
                rows = aligned_bbt_rows(f"{variable} | 0 | 2 | 6\n{derivative} | + | 0 | -\n{function} | 0 | 128 | 0")
                self.assertIsNotNone(rows)
                self.assertEqual([r[0] for r in rows], [variable, derivative, function])
                self.assertEqual(rows[2][1:], ['0', '↗', '128', '↘', '0'])

    def test_unrelated_labels_and_missing_limits_rejected(self):
        for raw in (
            "t | 0 | 2 | 6\nV'(t) | + | 0 | -\nS(t) | 0 | 128 | 0",
            "2026 | 0 | 2 | 6\nV'(t) | + | 0 | -\nV(t) | 0 | 128 | 0",
            "t | -inf | 2 | +inf\nV'(t) | + | || | -\nV(t) | 0 | || | 0",
        ):
            self.assertIsNone(aligned_bbt_rows(raw))
