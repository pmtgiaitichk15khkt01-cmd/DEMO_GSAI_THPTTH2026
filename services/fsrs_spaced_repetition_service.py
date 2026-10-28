# VIP 76.0 - HỆ THỐNG GIA SƯ AI THPT 2026 (CHUẨN GDPT 2018 - EDTECH & PSYCHOMETRICS SOTA)
# -*- coding: utf-8 -*-
"""
FSRS SPACED REPETITION SERVICE (THUẬT TOÁN LẶP NGẮT QUÃNG THÍCH ỨNG)
Cá nhân hóa lộ trình ôn tập dựa trên Đường cong Quên lãng Ebbinghaus & Mô hình FSRS:
- Tính Độ bền trí nhớ S (Memory Stability) và Xác suất nhớ lại R(t) = 0.9^(t / S).
- Định vị chính xác 'Điểm rơi vàng' (Optimal Review Window: R ≈ 85% - 90%)
  để cảnh báo học sinh ôn lại đúng lúc trước khi kiến thức bị trôi mất.
- Tự động quét từ bảng diagnostic_logs (Nhật ký sửa lỗi mực đỏ Trạm 2) và kết quả khảo thí Trạm 3.
"""

import time
import math
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple


# Tham số mặc định FSRS cho các mức độ phức tạp bài học
DIFFICULTY_STABILITY_MAP = {
    "NB": 5.0,     # Nhận biết: Độ bền ban đầu 5 ngày
    "TH": 3.0,     # Thông hiểu: Độ bền ban đầu 3 ngày
    "VD": 1.5,     # Vận dụng: Độ bền ban đầu 1.5 ngày
    "VDC": 1.0     # Vận dụng cao: Độ bền ban đầu 1 ngày
}


def calculate_retrievability(days_elapsed: float, stability: float) -> float:
    """
    Tính xác suất nhớ lại R(t) theo thời gian t (ngày) và độ bền S (ngày):
    R(t) = 0.90 ^ (t / S)
    """
    if stability <= 0.01:
        return 0.10
    if days_elapsed <= 0:
        return 1.0
    r = math.pow(0.90, days_elapsed / stability)
    return float(max(0.0, min(1.0, r)))


def update_stability_after_review(
    current_stability: float,
    performance_rating: int, # 1: Quên hẳn (Again), 2: Khó (Hard), 3: Nhớ tốt (Good), 4: Rất dễ (Easy)
    retrievability_at_review: float
) -> float:
    """
    Cập nhật độ bền trí nhớ S mới sau lượt ôn tập:
    Nếu nhớ tốt, độ bền S tăng lên lũy tiến: S_new = S * (1 + factor)
    Nếu quên hẳn, độ bền S bị reset về mức cơ bản.
    """
    if performance_rating == 1: # Quên
        return max(0.5, current_stability * 0.4)
    elif performance_rating == 2: # Khó
        multiplier = 1.2 + 0.2 * (1.0 - retrievability_at_review)
        return current_stability * multiplier
    elif performance_rating == 3: # Tốt
        multiplier = 2.0 + 0.5 * (1.0 - retrievability_at_review)
        return current_stability * multiplier
    else: # Rất dễ (4)
        multiplier = 2.8 + 0.8 * (1.0 - retrievability_at_review)
        return current_stability * multiplier


def analyze_student_fsrs_review_schedule(
    error_logs: Optional[List[Dict[str, Any]]] = None,
    current_time: Optional[datetime] = None
) -> List[Dict[str, Any]]:
    """
    Phân tích nhật ký học tập và đề xuất các chuyên đề cần ôn tập hôm nay:
    - Sắp xếp theo mức độ cấp thiết (Retrievability thấp nhất lên đầu).
    - Cảnh báo 'Điểm rơi vàng' khi R(t) trong khoảng 80% - 90%.
    """
    if current_time is None:
        current_time = datetime.now()

    # Dữ liệu dự phòng nếu chưa có nhật ký thực tế
    if not error_logs:
        return []
    schedule = []
    for item in error_logs:
        topic = item.get("topic", "Chuyên đề ôn tập")
        subject = item.get("subject", "Toán học")
        level = item.get("level", "TH")
        days_ago = float(item.get("logged_days_ago", 1.0))
        mistake = item.get("mistake_desc", "Cần củng cố phương pháp giải")

        # Xác định độ bền ban đầu
        init_stability = DIFFICULTY_STABILITY_MAP.get(level, 2.5)
        current_r = calculate_retrievability(days_ago, init_stability)

        # Đánh giá trạng thái theo FSRS
        if current_r <= 0.70:
            status = "🔴 Nguy cơ quên cao - Cần ôn tập ngay hôm nay!"
            priority = 1
            urgency_badge = "Cực kỳ cấp thiết"
            badge_color = "#dc2626"
        elif current_r <= 0.88:
            status = "🟡 Điểm rơi vàng ôn tập (Optimal Recall Window) - Hiệu quả nhân đôi!"
            priority = 2
            urgency_badge = "Điểm rơi vàng"
            badge_color = "#d97706"
        else:
            status = "🟢 Trí nhớ còn bền vững - Duy trì phản xạ"
            priority = 3
            urgency_badge = "Bình thường"
            badge_color = "#16a34a"

        # Tính thời điểm ôn tập lý tưởng tiếp theo
        optimal_days = init_stability * (math.log(0.85) / math.log(0.90))
        due_date = current_time - timedelta(days=days_ago) + timedelta(days=optimal_days)

        schedule.append({
            "topic": topic,
            "subject": subject,
            "days_since_mistake": round(days_ago, 1),
            "stability_days": round(init_stability, 1),
            "retrievability_percent": round(current_r * 100, 1),
            "status": status,
            "priority": priority,
            "urgency_badge": urgency_badge,
            "badge_color": badge_color,
            "mistake_desc": mistake,
            "recommended_review_date": due_date.strftime("%d/%m/%Y")
        })

    # Sắp xếp theo độ ưu tiên cấp thiết
    schedule.sort(key=lambda x: x["retrievability_percent"])
    return schedule
