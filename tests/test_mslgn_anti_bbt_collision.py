import unittest
import sys
import os
sys.path.insert(0, '.')

from real_exam_engine import sanitize_question_visuals

class TestMslgnAntiBbtCollision(unittest.TestCase):
    def test_mslgn_removes_unwanted_bbt(self):
        """Kiểm thử câu hỏi MSLGN có chứa từ 'khoảng biến thiên' và 'bảng sau' không bị gán BBT giải tích."""
        q_bac_an = {
            "q": "Mỗi ngày bác An đều chạy bộ để rèn luyện sức khỏe. Quãng đường chạy bộ mỗi ngày (đơn vị: km) của bác An trong 30 ngày được thống kê ở bảng sau: (Quãng đường [2.5; 3.0): 7; [3.0; 3.5): 7; [3.5; 4.0): 8; [4.0; 4.5): 5; [4.5; 5.0): 3). Khoảng biến thiên của mẫu số liệu ghép nhóm đó bằng",
            "opt": ["A. 0,5.", "B. 1,5.", "C. 2.", "D. 2,5."],
            "ans": "D",
            "bbt": "x | -\\infty | -1 | 1 | +\\infty\ny' | + | 0 | - | 0 | +\ny | -\\infty | \\nearrow | 2 | \\searrow | -2 | \\nearrow | +\\infty"
        }
        res = sanitize_question_visuals(dict(q_bac_an), subject="Toán học")
        self.assertNotIn("bbt", res, "Câu hỏi MSLGN bác An không được phép chứa BBT giải tích đạo hàm!")

    def test_calculus_retains_bbt(self):
        """Kiểm thử câu hỏi Khảo sát hàm số thực sự được bảo lưu BBT chuẩn xác."""
        q_ham_so = {
            "q": "Cho hàm số $y = f(x)$ liên tục trên $\\mathbb{R}$ và có bảng biến thiên như sau:",
            "opt": ["A. Đồng biến trên (0; 2)", "B. Nghịch biến trên (-1; 1)", "C. Cực đại tại x = 1", "D. Cực tiểu tại x = 0"],
            "ans": "B",
            "bbt": "x | -\\infty | -1 | 1 | +\\infty\ny' | + | 0 | - | 0 | +\ny | -\\infty | \\nearrow | 2 | \\searrow | -2 | \\nearrow | +\\infty"
        }
        res = sanitize_question_visuals(dict(q_ham_so), subject="Toán học")
        self.assertIn("bbt", res, "Câu hỏi Khảo sát hàm số phải có trường bbt!")

    def test_other_subjects_stripped_bbt(self):
        """Kiểm thử các môn khác (Vật lý, Hóa học, Địa lí) triệt tiêu 100% BBT Toán học."""
        subjects = ["Vật lý", "Hóa học", "Địa lí", "Sinh học"]
        for subj in subjects:
            q = {
                "q": f"Khảo sát biến thiên đại lượng theo thời gian trong {subj} thể hiện ở bảng sau:",
                "opt": ["A. 1", "B. 2", "C. 3", "D. 4"],
                "ans": "A",
                "bbt": "x | -\\infty | -1 | 1 | +\\infty\ny' | + | 0 | - | 0 | +\ny | -\\infty | \\nearrow | 2 | \\searrow | -2 | \\nearrow | +\\infty"
            }
            res = sanitize_question_visuals(dict(q), subject=subj)
            self.assertNotIn("bbt", res, f"Môn {subj} không được phép chứa BBT Toán học!")

if __name__ == '__main__':
    unittest.main()
