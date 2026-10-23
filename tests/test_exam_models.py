# VIP 74.1 - HỆ THỐNG GIA SƯ AI THPT 2026 (CHUẨN GDPT 2018 - BẢN VÁ HOÀN THIỆN ĐA MÔN & ĐA KHỐI LỚP)
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.exam_models import QuestionModel, StatementModel, normalize_exam_dict

class TestExamModels(unittest.TestCase):
    
    def test_question_model_p1(self):
        raw = {
            "question": "Tìm nghiệm phương trình x^2 - 4 = 0",
            "options": ["A. x = 2", "B. x = -2", "C. x = +-2", "D. Vô nghiệm"],
            "ans": "C",
            "explanation": "Ta có x^2 = 4 nên x = +-2"
        }
        qm = QuestionModel.from_dict(raw)
        self.assertEqual(qm.q, "Tìm nghiệm phương trình x^2 - 4 = 0")
        self.assertEqual(len(qm.opt), 4)
        self.assertEqual(qm.ans, "C")
        self.assertEqual(qm.part, "p1")

    def test_question_model_p2_statements(self):
        raw = {
            "q": "Xét tính đơn điệu hàm số y = f(x)",
            "stmts": [
                {"t": "Hàm số đồng biến trên (0; 2)", "a": True},
                {"t": "Hàm số đạt cực tiểu tại x = 1", "a": False}
            ]
        }
        qm = QuestionModel.from_dict(raw)
        self.assertEqual(qm.part, "p2")
        self.assertEqual(len(qm.stmts), 2)
        self.assertTrue(qm.stmts[0].is_correct)
        self.assertFalse(qm.stmts[1].is_correct)

    def test_normalize_exam_dict(self):
        raw_exam = {
            "title": "Đề Khảo sát Toán 12",
            "p1": [{"q": "Câu 1", "options": ["A", "B"], "ans": "A"}],
            "p2": [{"q": "Câu 2", "stmts": [{"t": "Ý a", "a": True}]}]
        }
        norm = normalize_exam_dict(raw_exam)
        self.assertEqual(norm["p1"][0]["part"], "p1")
        self.assertEqual(norm["p2"][0]["part"], "p2")

if __name__ == '__main__':
    unittest.main()
