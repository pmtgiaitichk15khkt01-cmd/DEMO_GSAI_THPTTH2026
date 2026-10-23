# VIP 74.1 - HỆ THỐNG GIA SƯ AI THPT 2026 (CHUẨN GDPT 2018 - BẢN VÁ HOÀN THIỆN ĐA MÔN & ĐA KHỐI LỚP)
"""
SERVICE QUẢN LÝ TRẠNG THÁI TẬP TRUNG (CENTRALIZED STATE SERVICE) - GSAI THPT 2026
Ngăn chặn 100% lỗi KeyError, AttributeError khi Streamlit reload hoặc đổi phiên.
"""
from typing import Any, Dict

DEFAULT_SESSION_STATE: Dict[str, Any] = {
    "selected_station": "📖 Trạm 1: Học Tập & Phòng Lab",
    "sb_station_radio_selector": "📖 Trạm 1: Học Tập & Phòng Lab",
    "exam_state": "config",
    "exam_data": None,
    "exam_answers": {},
    "exam_results": {},
    "exam_score": 0.0,
    "current_subject": "Toán học",
    "current_grade": 12,
    "student_name": "Học sinh Thiện Nhân",
    "student_id": "HS_2026_01",
    "tram3_chat_messages": [],
    "socratic_chat_history": []
}

def init_centralized_session_state(st_module: Any) -> None:
    """Khởi tạo giá trị mặc định cho toàn bộ các key trong st.session_state một cách an toàn."""
    for key, default_val in DEFAULT_SESSION_STATE.items():
        if key not in st_module.session_state:
            st_module.session_state[key] = default_val

def reset_exam_session(st_module: Any) -> None:
    """Đặt lại trạng thái thi sạch sẽ về màn hình cấu hình ban đầu."""
    st_module.session_state["exam_state"] = "config"
    st_module.session_state["exam_data"] = None
    st_module.session_state["exam_answers"] = {}
    st_module.session_state["exam_results"] = {}
    st_module.session_state["tram3_chat_messages"] = []

def safe_get_state(st_module: Any, key: str, fallback: Any = None) -> Any:
    """Truy xuất an toàn một key trong session_state mà không bao giờ bung lỗi KeyError."""
    try:
        return st_module.session_state.get(key, fallback)
    except Exception:
        return fallback