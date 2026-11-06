import unittest
import precision_visual_engine as pve
from app import format_pedagogical_bbt_html

class TestHarmonizeKshsVisuals(unittest.TestCase):
    def test_heal_bbt_null_sanitization(self):
        self.assertEqual(pve.heal_bbt_mathematics("null"), "")
        self.assertEqual(pve.heal_bbt_mathematics("None"), "")
        self.assertEqual(pve.heal_bbt_mathematics("{}"), "")
        self.assertEqual(pve.heal_bbt_mathematics(""), "")

    def test_format_pedagogical_bbt_html_null_sanitization(self):
        self.assertEqual(format_pedagogical_bbt_html("null"), "")
        self.assertEqual(format_pedagogical_bbt_html("None"), "")
        self.assertEqual(format_pedagogical_bbt_html("{}"), "")
        self.assertEqual(format_pedagogical_bbt_html(""), "")

    def test_harmonize_exam_visual_balance_reading_extrema(self):
        exam = {
            "title": "Đề khảo sát Khảo sát hàm số Toán 12",
            "subject": "Toán học",
            "grade": 12,
            "p1": [
                {
                    "q": "Cho hàm số y=f(x) có đồ thị như hình vẽ bên: Giá trị cực tiểu của hàm số đã cho bằng:",
                    "opt": ["A. -2", "B. 2", "C. 1", "D. -1"],
                    "ans": "A",
                    "f": "null",
                    "bbt": "null"
                },
                {
                    "q": "Hàm số nào dưới đây có đồ thị dạng như đường cong trong hình vẽ bên?",
                    "opt": ["A. y = \\frac{2x-1}{x-1}", "B. y = x^3 - 3x", "C. y = \\frac{x^2-x+1}{x-1}", "D. y = x^4 - 2x^2"],
                    "ans": "A"
                },
                {
                    "q": "Cho hàm số y=f(x) có bảng biến thiên như hình bên. Hàm số đạt cực đại tại điểm nào?",
                    "opt": ["A. x = 0", "B. x = 2", "C. x = -2", "D. x = 1"],
                    "ans": "A",
                    "bbt": "null"
                }
            ]
        }

        harmonized = pve.harmonize_exam_visual_balance(exam, subject="Toán học", grade=12, user_custom_req="3 hàm cơ bản bậc ba, 1/1, 2/1")
        p1 = harmonized["p1"]

        # Câu 1: Phải có f và bbt hợp lệ, không được là null
        self.assertIsNotNone(p1[0].get("f"))
        self.assertIsInstance(p1[0].get("f"), dict)
        self.assertNotEqual(p1[0].get("bbt"), "null")
        self.assertIn("type", p1[0]["f"])

        # Câu 2: Nhận diện 1/1 từ phương án A
        self.assertIsNotNone(p1[1].get("f"))
        self.assertEqual(p1[1]["f"].get("type"), "func_1_1")
        self.assertTrue(bool(p1[1].get("tikz")))

        # Câu 3: Phải có BBT hợp lệ, không được là null
        self.assertIsNotNone(p1[2].get("bbt"))
        self.assertNotEqual(p1[2].get("bbt"), "null")
        self.assertIn("y'", p1[2]["bbt"])

if __name__ == "__main__":
    unittest.main()
