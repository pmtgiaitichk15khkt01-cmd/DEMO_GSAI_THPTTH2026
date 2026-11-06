# -*- coding: utf-8 -*-
"""
Unit tests for BBT/BXD Dark Mode high-contrast rendering and LaTeX TikZ specifications.
"""
import unittest
import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import format_pedagogical_bbt_html, _build_svg_bbt_from_rows, _render_math_html_token
from services.tikz_pedagogical_spec import (
    SYSTEM_PROMPT_TIKZ_BBT_GRAPH_SPEC,
    inject_tikz_spec_into_prompt,
    get_tikz_packages_latex_header
)


class TestBBTDarkModeAndTikZSpec(unittest.TestCase):

    def test_bbt_dark_mode_forced_rendering(self):
        """Kiểm thử BBT khi ép buộc is_dark_mode=True."""
        raw_bbt = (
            "x | -inf | 1 | 3 | +inf\n"
            "y' | + | 0 | - | 0 | +\n"
            "y | -inf | ↗ | 4 | ↘ | 0 | ↗ | +inf"
        )
        html_dark = format_pedagogical_bbt_html(raw_bbt, is_dark_mode=True)
        self.assertTrue(len(html_dark) > 50, "BBT HTML output must not be empty.")
        self.assertIn("bbt-dark-forced", html_dark, "Dark mode container must have bbt-dark-forced class.")
        self.assertIn("#0b1329", html_dark, "Dark mode background must be high-contrast dark (#0b1329).")
        self.assertIn("#38bdf8", html_dark, "Dark mode accent border must be bright cyan (#38bdf8).")
        self.assertIn("#f8fafc", html_dark, "Dark mode values must be high-contrast bright text (#f8fafc).")

    def test_bbt_auto_theme_responsive_css(self):
        """Kiểm thử BBT khi is_dark_mode=False vẫn có CSS tự thích ứng Dark Mode."""
        raw_bbt = (
            "x | -inf | -1 | +inf\n"
            "y' | + | 0 | -\n"
            "y | -inf | ↗ | 2 | ↘ | -inf"
        )
        html_auto = format_pedagogical_bbt_html(raw_bbt, is_dark_mode=False)
        self.assertIn("bbt-mode-auto", html_auto)
        self.assertIn("prefers-color-scheme: dark", html_auto, "Must contain media query for system dark mode.")
        self.assertIn('[data-theme="dark"]', html_auto, "Must contain selector for Streamlit dark theme.")

    def test_sign_table_bxd_dark_mode(self):
        """Kiểm thử Bảng xét dấu 2 hàng (BXD) tương thích Dark Mode."""
        x_cells = ["x", "-inf", "1", "2", "+inf"]
        yp_cells = ["y'", "+", "0", "-", "0", "+"]
        html_bxd = _build_svg_bbt_from_rows(x_cells, yp_cells, [], is_sign_table=True, is_dark_mode=True)
        self.assertIn("BẢNG XÉT DẤU", html_bxd)
        self.assertIn("bbt-dark-forced", html_bxd)
        self.assertIn("#22c55e", html_bxd, "Plus sign must be vibrant green (#22c55e).")
        self.assertIn("#ef4444", html_bxd, "Minus sign must be vibrant red (#ef4444).")

    def test_math_html_token_fraction_current_color(self):
        """Kiểm thử phân số trong BBT dùng currentColor để không bị đen chữ trên nền tối."""
        token = r"\frac{3}{2}"
        rendered = _render_math_html_token(token)
        self.assertIn("currentColor", rendered, "Fraction horizontal line must use currentColor for theme adaptability.")
        self.assertIn("bbt-frac-line", rendered)

    def test_tikz_pedagogical_spec_injection(self):
        """Kiểm thử chỉ dẫn Prompt TikZ chuẩn theo 3 tài liệu Word."""
        base_prompt = "Hãy biên soạn đề thi Toán 12."
        injected = inject_tikz_spec_into_prompt(base_prompt, subject="Toán")
        self.assertIn("tkzTabInit", injected, "Must contain tkzTabInit for BXD/BBT.")
        self.assertIn("tkzTabLine", injected, "Must contain tkzTabLine.")
        self.assertIn("tkzMarkSegments", injected, "Must contain geometric marking rules.")
        self.assertIn("pgfplots", injected, "Must contain pgfplots instruction for rational functions.")

        # Non-math subject must not be injected with TikZ spec
        non_math = inject_tikz_spec_into_prompt("Hãy soạn bài Lịch sử", subject="Lịch sử")
        self.assertEqual(non_math, "Hãy soạn bài Lịch sử")

    def test_tikz_packages_header(self):
        """Kiểm thử danh sách các gói LaTeX cho Overleaf."""
        pkgs = get_tikz_packages_latex_header()
        self.assertTrue(any("tkz-tab" in p for p in pkgs))
        self.assertTrue(any("tkz-euclide" in p for p in pkgs))
        self.assertTrue(any("patterns" in p for p in pkgs))
        self.assertTrue(any("pgfplots" in p for p in pkgs))


if __name__ == '__main__':
    unittest.main()
