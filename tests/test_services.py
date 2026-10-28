# VIP 74.6 - HỆ THỐNG GIA SƯ AI THPT 2026 (CHUẨN GDPT 2018 - BẢN VÁ HOÀN THIỆN ĐA MÔN & ĐA KHỐI LỚP)
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.scoring_service import calculate_part2_statement_score, grade_part1, grade_part2, grade_part3
from services.state_service import init_centralized_session_state, safe_get_state

class MockSessionState(dict):
    pass

class MockStreamlit:
    def __init__(self):
        self.session_state = MockSessionState()

class TestServices(unittest.TestCase):
    
    def test_p2_score_ladder(self):
        self.assertEqual(calculate_part2_statement_score(0), 0.0)
        self.assertEqual(calculate_part2_statement_score(1), 0.1)
        self.assertEqual(calculate_part2_statement_score(2), 0.25)
        self.assertEqual(calculate_part2_statement_score(3), 0.5)
        self.assertEqual(calculate_part2_statement_score(4), 1.0)

    def test_grade_part1(self):
        qs = [{"ans": "A"}, {"ans": "B"}, {"ans": "C"}, {"ans": "D"}]
        user_ans = {"p1_0": "A", "p1_1": "B", "p1_2": "A", "p1_3": "D"}
        score, correct, total = grade_part1(qs, user_ans)
        self.assertEqual(correct, 3)
        self.assertEqual(total, 4)
        self.assertEqual(score, 2.25)

    def test_state_service_safe_init(self):
        st = MockStreamlit()
        init_centralized_session_state(st)
        self.assertEqual(safe_get_state(st, "selected_station"), "📖 Trạm 1: Học Tập & Phòng Lab")
        self.assertIn(safe_get_state(st, "student_name"), ["Học sinh THPT Tân Hiệp", "Học sinh Thiện Nhân"])
        self.assertEqual(safe_get_state(st, "non_existent_key", "default_val"), "default_val")

    def test_curriculum_matrix(self):
        from services.curriculum_matrix import render_subject_exam_matrix_spec
        van_html = render_subject_exam_matrix_spec("Ngữ văn", 12)
        self.assertIn("764/QĐ-BGDĐT", van_html)
        toan_html = render_subject_exam_matrix_spec("Toán học", 12)
        self.assertIn("Toán", toan_html)

    def test_mermaid_renderer_callable(self):
        from services.mermaid_renderer import render_mermaid
        self.assertTrue(callable(render_mermaid))

if __name__ == '__main__':
    unittest.main()