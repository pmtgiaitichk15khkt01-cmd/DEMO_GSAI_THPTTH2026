import sys
import unittest
import os

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import lesson_infographic_engine as engine

test_cases = [
    # (Subject, Grade, Topic, Expected Keyword in SVG/Title, Forbidden Keyword)
    ("Toán học", 10, "Hàm số bậc hai và tam thức", "Parabol", "x³"),
    ("Toán học", 11, "Hàm số lượng giác", "Dao động lượng giác", "x³"),
    ("Toán học", 12, "Các số đặc trưng mẫu số liệu ghép nhóm", "HISTOGRAM", "x³"),
    ("Toán học", 12, "Khảo sát và vẽ đồ thị hàm số", "x³", "HISTOGRAM"),
    ("Ngữ văn", 12, "Vợ nhặt (Kim Lân)", "CẤU TRÚC 4 CHIỀU PHÂN TÍCH TÁC PHẨM", "x³"),
    ("Ngữ văn", 10, "Bình Ngô đại cáo (Nguyễn Trãi)", "Bút pháp", "x³"),
    ("Vật lý", 12, "Dao động điều hòa", "x(cm)", "x³"),
    ("Hóa học", 12, "Ester và Lipid", "Chất phản ứng", "x³"),
    ("Sinh học", 12, "Quy luật phân ly Mendel", "AA × aa", "x³"),
    ("Lịch sử", 12, "Cách mạng tháng Tám 1945", "Tiền đề", "x³"),
    ("Địa lý", 12, "Cơ cấu kinh tế theo ngành", "Nông nghiệp", "x³"),
    ("Tiếng Anh", 12, "Unit 1: Life Stories", "Stress", "x³"),
    ("Tin học", 11, "Thuật toán tìm kiếm nhị phân", "A[mid] == k?", "x³"),
    ("Khoa học tự nhiên", 7, "Tế bào - Đơn vị sự sống", "VÒNG TRÒN KHÁM PHÁ KHTN", "x³"),
    ("Giáo dục kinh tế và pháp luật", 11, "Cung cầu trong kinh tế", "E(P₀, Q₀)", "x³")
]

def run_all_tests():
    all_passed = True
    for subj, grd, top, expected, forbidden in test_cases:
        res = engine.generate_worked_example_and_visual(subj, grd, top)
        title = res.get("title", "")
        steps = res.get("steps", [])
        svg = res.get("visual_svg", "")
        full_content = title + " " + " ".join(s[0] + " " + s[1] for s in steps) + " " + svg
        
        passed_expected = expected.lower() in full_content.lower()
        passed_forbidden = forbidden.lower() not in full_content.lower()
        if not (passed_expected and passed_forbidden):
            all_passed = False
    return all_passed

class TestMultiSubjectGradeIntegrity(unittest.TestCase):
    def test_all_fifteen_subject_grade_cases(self):
        self.assertTrue(run_all_tests(), "Có ca đa môn/đa lớp thất bại")


if __name__ == "__main__":
    passed = run_all_tests()
    if passed:
        print("ALL 15 MULTI-SUBJECT MULTI-GRADE TESTS PASSED!")
    else:
        print("SOME TESTS FAILED!")
        sys.exit(1)
