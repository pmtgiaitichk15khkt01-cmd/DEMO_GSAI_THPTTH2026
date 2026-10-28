"""Streamlit UI regressions without a live Gemini call or production database."""
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from streamlit.testing.v1 import AppTest


class TestStationUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import database
        cls.temp = tempfile.TemporaryDirectory()
        cls.db = database.DatabaseManager(Path(cls.temp.name) / "ui.db")
        cls.db_patch = patch.object(database, "db_manager", cls.db)
        cls.db_patch.start()

    @classmethod
    def tearDownClass(cls):
        cls.db_patch.stop()
        # AppTest creates worker-thread-local connections. Keep test cleanup independent
        # of Windows handle lifetime; TemporaryDirectory cleanup waits for process exit.
        cls.temp._ignore_cleanup_errors = True
        cls.temp.cleanup()

    def app(self):
        at = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py"), default_timeout=45)
        at.secrets["ADMIN_PASS"] = "qa-private-password"
        at.run()
        self.assertEqual([e.message for e in at.exception], [])
        return at

    def test_station1_preset_lab_and_grade_context_reset(self):
        at = self.app()
        next(b for b in at.button if b.label == "Mở mô phỏng có sẵn").click().run()
        self.assertEqual([e.message for e in at.exception], [])
        at.session_state["t3_p3_0"] = "old-answer"
        at.session_state["tram1_chat_history"] = [{"role": "user", "content": "old context"}]
        next(s for s in at.selectbox if s.label == "🎯 Chọn khối lớp:").select("Lớp 6").run()
        self.assertEqual([e.message for e in at.exception], [])
        self.assertNotIn("t3_p3_0", at.session_state)
        self.assertEqual(at.session_state["tram1_chat_history"], [])
        subjects = next(s for s in at.selectbox if s.label == "📚 Môn học cần hỗ trợ:").options
        self.assertIn("Khoa học tự nhiên", subjects)
        self.assertNotIn("Vật lý", subjects)

    def test_station2_empty_session_has_no_fake_mastery(self):
        at = self.app()
        at.session_state["selected_station"] = "✍️ Trạm 2: Gia Sư Socratic & Nộp Bài"
        at.run()
        self.assertEqual([e.message for e in at.exception], [])
        self.assertEqual(at.session_state["tram2_count"], 0)
        self.assertFalse(any("85.4%" in m.value for m in at.markdown))

    def test_station3_wrong_decimal_gets_zero_and_saves_one_event(self):
        at = self.app()
        at.session_state["selected_station"] = "📝 Trạm 3: Luyện Tập & Khảo Thí"
        at.session_state["exam_state"] = "testing"
        at.session_state["exam_data"] = {"code": "QA01", "p1": [], "p2": [], "p3": [{"q": "Tìm giá trị cực đại của $y=-x^3+3x+1$.", "ans": "3"}]}
        at.session_state["exam_context"] = {"name": "QA UI", "grade": "Lớp 12", "subject": "Toán học", "student_id": "qa-ui"}
        at.session_state["exam_deadline"] = time.time() + 90
        at.session_state["attempt_id"] = "qa-ui-decimal"
        at.run()
        next(t for t in at.text_input if t.label == "Nhập đáp số câu 1:").set_value("3.4").run()
        next(b for b in at.button if b.label == "🏁 Nộp bài & Chấm điểm tức thì").click().run()
        self.assertEqual([e.message for e in at.exception], [])
        events = [e for e in at.session_state["analytics_logs"] if e.get("event_id") == "qa-ui-decimal"]
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["score"], 0)
        self.assertFalse(events[0]["answers"]["_item_results"]["p3_0"])
        at.run()
        self.assertEqual(len([e for e in at.session_state["analytics_logs"] if e.get("event_id") == "qa-ui-decimal"]), 1)

    def test_station4_auth_demo_statistics_and_monte_carlo(self):
        at = self.app()
        at.session_state["selected_station"] = "📊 Trạm 4: Dữ Liệu & Nghiên Cứu"
        at.run()
        next(t for t in at.text_input if t.label == "Mật khẩu quản trị:").set_value("GiaoVienKHKT@2026")
        next(b for b in at.button if b.label == "🔓 Mở khóa").click().run()
        self.assertFalse(at.session_state.get("tab4_authenticated", False) if hasattr(at.session_state, "get") else "tab4_authenticated" in at.session_state and at.session_state["tab4_authenticated"])
        next(t for t in at.text_input if t.label == "Mật khẩu quản trị:").set_value("qa-private-password")
        next(b for b in at.button if b.label == "🔓 Mở khóa").click().run()
        self.assertTrue(at.session_state["tab4_authenticated"])
        next(r for r in at.radio if r.label == "Nguồn dữ liệu").set_value("Mô phỏng minh họa").run()
        next(b for b in at.button if b.label == "Phân tích các cặp điểm").click().run()
        self.assertEqual([e.message for e in at.exception], [])
        self.assertTrue(at.session_state["research_result"]["demo"])
        next(b for b in at.button if "Kích hoạt Mô phỏng Monte Carlo" in b.label).click().run()
        self.assertEqual([e.message for e in at.exception], [])
        self.assertFalse(any("Gaussian" in m.value and "p < 0.001" in m.value for m in at.success))


if __name__ == "__main__":
    unittest.main()
