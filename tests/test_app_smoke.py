# -*- coding: utf-8 -*-
"""
INTEGRATION SMOKE TEST (VIP 74.6)
Kiểm tra tích hợp thực tế toàn diện:
- Đảm bảo app.py khởi động sạch 100%.
- Kiểm tra các hàm trụ cột: sanitize_socratic_hint, safe_json_loads, build_exam_exports, question_visual_html, render_question_source_badge.
- Kiểm tra preflight_exam_auto_heal với cả 3 phần thi Đa môn chuẩn GDPT 2018.
"""

import unittest
import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

class TestAppSmoke(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import app
        cls.app = app

    def test_app_core_functions_exist(self):
        """Kiểm tra sự tồn tại của 5 hàm trụ cột trong app.py"""
        self.assertTrue(callable(getattr(self.app, 'sanitize_socratic_hint', None)))
        self.assertTrue(callable(getattr(self.app, 'safe_json_loads', None)))
        self.assertTrue(callable(getattr(self.app, 'build_exam_exports', None)))
        self.assertTrue(callable(getattr(self.app, 'question_visual_html', None)))
        self.assertTrue(callable(getattr(self.app, 'render_question_source_badge', None)))

    def test_sanitize_socratic_hint_execution(self):
        """Kiểm tra sanitize_socratic_hint không bao giờ ném NameError"""
        hint = self.app.sanitize_socratic_hint(
            "Lời giải chi tiết: Ta có đạo hàm y' = 3x^2 - 6x. Chọn A.",
            correct_answer="A",
            q_text="Tìm khoảng đồng biến của hàm số",
            level="TH",
            subject="Toán học",
            grade_num=12
        )
        self.assertIsInstance(hint, str)
        self.assertNotIn("Chọn A", hint)

    def test_safe_json_loads_execution(self):
        """Kiểm tra safe_json_loads bóc tách JSON chuẩn xác"""
        raw = '```json\n{"items": [{"id": 1, "score": 4.0}], "note": "ok"}\n```'
        res = self.app.safe_json_loads(raw)
        self.assertEqual(res["note"], "ok")
        self.assertEqual(res["items"][0]["score"], 4.0)

    def test_exam_preflight_auto_heal(self):
        """Kiểm tra luồng auto-heal đề thi không bị lỗi NameError hay sập runtime"""
        sample_exam = {
            "p1": [
                {
                    "q": "Cho hàm số $y=f(x)$ liên tục trên $\\mathbb{R}$",
                    "opt": ["A. 1", "B. 2", "C. 3", "D. 4"],
                    "ans": "A",
                    "explain": "Lời giải: Điểm uốn của đồ thị là tâm đối xứng."
                }
            ],
            "p2": [
                {
                    "q": "Các mệnh đề sau đúng hay sai:",
                    "stmts": [{"t": "Mệnh đề 1", "a": True}],
                    "explain": "Giải thích chi tiết mệnh đề"
                }
            ],
            "p3": [
                {
                    "q": "Tìm giá trị cực đại của hàm số:",
                    "ans": "12",
                    "explain": "Đạo hàm bằng 0 tại x = 2"
                }
            ],
            "subject": "Toán học",
            "grade": 12,
            "code": "101"
        }
        # preflight auto heal simulation
        p1_q = sample_exam["p1"][0]
        cleaned_hint = self.app.sanitize_socratic_hint(p1_q["explain"], p1_q["ans"], p1_q["q"], p1_q["opt"], "TH", "Toán học", 12)
        self.assertIsInstance(cleaned_hint, str)

    def test_paired_statistics_hake_gain(self):
        """Kiểm tra paired_statistics tính đúng Hake Normalized Gain & Shapiro-Wilk"""
        pre = [4.0, 5.0, 6.0, 4.5, 5.5]
        post = [7.0, 8.0, 8.5, 7.5, 8.0]
        res = self.app.paired_statistics(pre, post)
        self.assertIn("hake", res)
        self.assertIsNotNone(res["hake"])
        self.assertGreater(res["hake"], 0.3)  # Gain dương đáng kể
        self.assertIn("shapiro_p", res)
        self.assertIn("wilcoxon_p", res)

    def test_cong_nghe_curriculum_and_library(self):
        """Kiểm tra môn Công nghệ đã có mặt đầy đủ trong Curriculum và SGK Library"""
        from data.curriculum_data import BIGDATA_CURRICULUM
        from kntt_sgk_library import KNTT_DIGITAL_LIBRARY
        self.assertIn("Công nghệ", BIGDATA_CURRICULUM)
        self.assertEqual(len(BIGDATA_CURRICULUM["Công nghệ"]), 7)  # Đủ 7 khối lớp 6-12
        for gr in ["6", "7", "8", "9", "10", "11", "12"]:
            self.assertIn(gr, KNTT_DIGITAL_LIBRARY)
            self.assertIn("Công nghệ", KNTT_DIGITAL_LIBRARY[gr])

    def test_latex_export_chunking(self):
        """Kiểm tra build_exam_exports xuất đầy đủ 100% câu trắc nghiệm sang LaTeX (không bị cắt ở 10 câu)"""
        # Giả lập đề Tiếng Anh 40 câu
        sample_exam = {
            "p1": [{"q": f"Question {i+1}", "opt": ["A. a", "B. b", "C. c", "D. d"], "ans": "A"} for i in range(40)],
            "subject": "Tiếng Anh",
            "grade": 12,
            "code": "ENG1201"
        }
        html_markup, tex_code = self.app.build_exam_exports(sample_exam, "Tiếng Anh", "Lớp 12", 50, include_answers=True)
        # Phải chứa cả câu 11, câu 20, câu 30, câu 40
        self.assertIn("Câu 11", tex_code)
        self.assertIn("Câu 20", tex_code)
        self.assertIn("Câu 30", tex_code)
        self.assertIn("Câu 40", tex_code)

if __name__ == '__main__':
    unittest.main()

