# VIP 74.1 - HỆ THỐNG GIA SƯ AI THPT 2026 (CHUẨN GDPT 2018 - BẢN VÁ HOÀN THIỆN ĐA MÔN & ĐA KHỐI LỚP)
"""
BỘ KIỂM THỬ HỆ THỐNG TOÀN DIỆN (SYSTEM INTEGRITY TEST SUITE) - GSAI THPT 2026
Tự động kích hoạt trên GitHub Actions CI/CD và Local Pre-flight Verification.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestGSAISystemIntegrity(unittest.TestCase):
    
    def test_01_core_modules_compilation(self):
        """Kiểm tra 100% các file lõi biên dịch sạch sẽ không có lỗi cú pháp."""
        import py_compile
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        core_files = [
            "precision_visual_engine.py",
            "real_exam_engine.py",
            "database.py",
            "lesson_infographic_engine.py"
        ]
        for cf in core_files:
            file_path = os.path.join(root_dir, cf)
            if os.path.exists(file_path):
                py_compile.compile(file_path, doraise=True)

    def test_02_shape_theory_guard_no_spurious_graph(self):
        """Kiểm tra chốt chặn câu hỏi lý thuyết chữ N không bị gán đồ thị rác."""
        import precision_visual_engine as pve
        q_theory = {
            "q": "Đồ thị của hàm số nào dưới đây có dạng giống như chữ N hoặc chữ N ngược?",
            "opt": [
                "y = x^3 - 3x + 1",
                "y = \\frac{x+1}{x-1}",
                "y = x^2 - 2x",
                "y = -x^2 + 2x"
            ],
            "ans": "A"
        }
        healed = pve.enrich_question_visual_precision(dict(q_theory), "Toán học", 12)
        self.assertIsNone(healed.get("f"), "Câu hỏi lý thuyết chữ N tuyệt đối không được có đồ thị f rác!")

    def test_03_genuine_graph_question_preserved(self):
        """Kiểm tra câu hỏi đồ thị thực tế vẫn giữ nguyên đồ thị chuẩn."""
        import precision_visual_engine as pve
        q_genuine = {
            "q": "Đường cong trong hình vẽ bên là đồ thị của hàm số nào dưới đây?",
            "opt": [
                "y = \\frac{2x-1}{x-1}",
                "y = \\frac{x+1}{x-1}",
                "y = x^3 - 3x",
                "y = x^2 - 2"
            ],
            "ans": "A"
        }
        healed = pve.enrich_question_visual_precision(dict(q_genuine), "Toán học", 12)
        self.assertIsNotNone(healed.get("f"), "Câu hỏi có 'hình vẽ bên' phải được gán đồ thị hợp lệ!")

    def test_04_pure_vector_algebra_no_3d_geom(self):
        """Kiểm tra câu hỏi vectơ đại số Oxyz thuần túy không bị gán mô hình 3D vu vơ."""
        import precision_visual_engine as pve
        q_vec = {
            "q": "Trong không gian Oxyz, cho vectơ u = 2i - 3j + k. Tìm tọa độ của vectơ u.",
            "opt": ["(2; -3; 1)", "(2; 3; 1)", "(-2; 3; 1)", "(2; -3; -1)"],
            "ans": "A"
        }
        healed = pve.audit_and_heal_visual_context_gdpt2018(dict(q_vec), "Toán học", 12)
        self.assertIsNone(healed.get("geom_3d"), "Câu hỏi tọa độ vectơ thuần túy không được gán mô hình 3D!")

    def test_05_p2_scoring_ladder_compliance(self):
        """Kiểm tra thang điểm lũy tiến Phần II Đúng/Sai chuẩn QĐ 764 Bộ GD&ĐT (0.1 - 0.25 - 0.5 - 1.0)."""
        from services.scoring_service import calculate_part2_statement_score
        self.assertEqual(calculate_part2_statement_score(0), 0.0)
        self.assertEqual(calculate_part2_statement_score(1), 0.1)
        self.assertEqual(calculate_part2_statement_score(2), 0.25)
        self.assertEqual(calculate_part2_statement_score(3), 0.5)
        self.assertEqual(calculate_part2_statement_score(4), 1.0)

    def test_06_station1_bbt_and_regex_safety(self):
        """Kiểm tra Station 1 không crash bad escape \\m và nhận diện đúng BBT f'(x)."""
        from app import station1_master_sovereign_brain_gate, render_pedagogical_lesson_visuals
        raw_text = "Hàm số có tập xác định D = R và \\R. Bảng biến thiên:\n| x | -∞ | 1 | +∞ |\n| f'(x) | + | 0 | - |\n| y | -∞ ↗ 2 | ↘ -∞ |"
        # 1. Không crash khi chuẩn hóa D = R
        gated = station1_master_sovereign_brain_gate(raw_text, subject="Toán học", grade=12)
        self.assertIn(r"D = \mathbb{R}", gated)
        # 2. Nhận diện và chuyển hóa BBT thành đồ họa chuẩn
        vis = render_pedagogical_lesson_visuals(gated, subject="Toán học", grade=12)
        self.assertTrue("data:image/webp" in vis or "<div style" in vis)

    def test_07_self_distilled_infographic_pipeline(self):
        """Kiểm tra động cơ Infographic tự thân trích xuất chuẩn 4 khối từ AI prompt."""
        import lesson_infographic_engine as lie
        sample_md = """
### TÓM TẮT CẨM NANG INFOGRAPHIC:
Khối 1 (Khái niệm cốt lõi):
- Khái niệm hàm số: Quan hệ một - một giữa tập X và Y. Định nghĩa nền tảng giải tích.
- Tập xác định: Tập giá trị x để biểu thức có nghĩa. D = ℝ với đa thức.
- Tính đơn điệu: Đạo hàm dương hàm đồng biến. Đạo hàm âm hàm nghịch biến.
- Cực trị hàm số: Điểm đạo hàm đổi dấu. Gồm cực đại và cực tiểu.

Khối 2 (Công thức & Quy luật):
- Đạo hàm đa thức: (x^n)' = n*x^(n-1). Quy tắc đạo hàm cơ bản.
- Đạo hàm phân thức: ((ax+b)/(cx+d))' = (ad-bc)/(cx+d)^2. Công thức giải nhanh.
- Điều kiện cực trị: y' = 0 và y'' != 0. Tiêu chuẩn Fermat.
- Phương trình tiếp tuyến: y = f'(x0)(x - x0) + y0. Tiếp tuyến tại một điểm.

Khối 3 (Tiến trình tư duy 4 bước Polya):
- Ví dụ: Khảo sát hàm số y = x^3 - 3x.
- Bước 1 (Tìm hiểu đề): Xác định TXĐ và tính y'.
- Bước 2 (Lập kế hoạch): Giải y' = 0 tìm nghiệm.
- Bước 3 (Thực hiện giải): Lập bảng biến thiên.
- Bước 4 (Nhìn lại & Đúc kết): Kết luận tính đơn điệu.

Khối 4 (Cạm bẫy thực tế & Mẹo thi):
- Bẫy 1: Quên điều kiện mẫu số: Bỏ sót điểm gián đoạn làm sai TXĐ. Bí quyết: Đặt điều kiện trước khi đạo hàm!
- Bẫy 2: Nhầm điểm cực trị và giá trị cực trị: Điểm là x, giá trị là y. Bí quyết: Đọc kỹ từ khóa đề bài!
"""
        extracted = lie.distill_markdown_to_infographic_blocks("Toán", 12, "Hàm số", sample_md)
        self.assertIsNotNone(extracted)
        self.assertEqual(len(extracted["box1"]), 4)
        self.assertEqual(len(extracted["box2"]), 4)
        self.assertEqual(len(extracted["box4"]), 2)
        self.assertEqual(len(extracted["example"]["steps"]), 4)

        svg = lie.build_a4_infographic_svg("Toán", 12, "Hàm số", "TOAN_12", "SGK KNTT", "Kênh GD", "", sample_md)
        self.assertTrue(len(svg) > 5000)
        self.assertIn("<svg", svg)

if __name__ == '__main__':
    unittest.main()

