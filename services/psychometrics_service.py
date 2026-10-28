# VIP 76.0 - HỆ THỐNG GIA SƯ AI THPT 2026 (CHUẨN GDPT 2018 - EDTECH & PSYCHOMETRICS SOTA)
# -*- coding: utf-8 -*-
"""
PSYCHOMETRICS SERVICE (ĐO LƯỜNG & KHẢO THÍ SƯ PHẠM CHUẨN ETS - HOA KỲ)
Tính toán chuyên sâu:
1. Độ tin cậy nội tại Cronbach's Alpha (α).
2. Độ khó của từng câu hỏi (Item Difficulty Index - P_i).
3. Độ phân biệt Point-Biserial Correlation (r_pbis) theo chuẩn ETS.
4. Trích xuất ma trận làm bài thực tế từ SQLite (bảng exam_attempts) kết hợp ma trận mô phỏng chuẩn N học sinh.
"""

import json
import math
from typing import Dict, Any, List, Optional, Tuple
import numpy as np


def compute_cronbach_alpha(item_matrix: np.ndarray) -> Dict[str, Any]:
    """
    Tính hệ số tin cậy nội tại Cronbach's Alpha (α):
    α = [K / (K - 1)] * [1 - (Σ σ_i²) / σ_X²]
    trong đó:
      - K: Số lượng câu hỏi (items)
      - σ_i²: Phương sai điểm của từng câu hỏi
      - σ_X²: Phương sai tổng điểm của bài kiểm tra
    """
    if item_matrix is None or item_matrix.size == 0:
        return {"alpha": None, "interpretation": "Chưa có dữ liệu ma trận", "k_items": 0, "n_students": 0}

    arr = np.array(item_matrix, dtype=float)
    if arr.ndim != 2:
        return {"alpha": None, "interpretation": "Ma trận không đúng 2 chiều", "k_items": 0, "n_students": 0}

    n_students, k_items = arr.shape
    if n_students < 3 or k_items < 2:
        return {
            "alpha": None,
            "interpretation": "Cần tối thiểu 3 học sinh và 2 câu hỏi để tính Cronbach's α",
            "k_items": k_items,
            "n_students": n_students
        }

    # Phương sai từng câu (dùng ddof=1 cho mẫu)
    item_variances = np.var(arr, axis=0, ddof=1)
    sum_item_variances = float(np.sum(item_variances))

    # Tổng điểm của từng học sinh và phương sai tổng
    total_scores = np.sum(arr, axis=1)
    total_variance = float(np.var(total_scores, ddof=1))

    if total_variance <= 1e-9:
        return {
            "alpha": 0.0,
            "interpretation": "Phương sai tổng điểm bằng 0 (tất cả học sinh đạt cùng một mức điểm)",
            "k_items": k_items,
            "n_students": n_students,
            "total_variance": total_variance,
            "sum_item_variances": sum_item_variances
        }

    alpha = (k_items / (k_items - 1)) * (1.0 - (sum_item_variances / total_variance))
    alpha = float(alpha)

    # Đánh giá theo thang đo George & Mallery (2003) & ETS
    if alpha >= 0.90:
        interpretation = "Xuất sắc (Excellent internal consistency - Đề thi chuẩn hóa cấp quốc gia)"
        badge_color = "#16a34a"
    elif alpha >= 0.80:
        interpretation = "Rất tốt (Good - Độ tin cậy cao, phù hợp khảo thí diện rộng)"
        badge_color = "#0284c7"
    elif alpha >= 0.70:
        interpretation = "Chấp nhận được (Acceptable - Đạt chuẩn kiểm tra học kỳ)"
        badge_color = "#d97706"
    elif alpha >= 0.60:
        interpretation = "Độ tin cậy nghi ngờ (Questionable - Cần rà soát lại các câu phân biệt kém)"
        badge_color = "#ea580c"
    else:
        interpretation = "Độ tin cậy kém (Poor/Unacceptable - Đề thi chưa chuẩn hóa)"
        badge_color = "#dc2626"

    return {
        "alpha": round(alpha, 4),
        "interpretation": interpretation,
        "badge_color": badge_color,
        "k_items": k_items,
        "n_students": n_students,
        "total_variance": round(total_variance, 4),
        "sum_item_variances": round(sum_item_variances, 4)
    }


def compute_item_analysis(item_matrix: np.ndarray, item_names: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Phân tích từng câu hỏi (Item Analysis):
    - Độ khó P_i: Tỉ lệ thí sinh trả lời đúng (0 <= P_i <= 1).
    - Độ phân biệt Point-Biserial Correlation (r_pbis):
      r_pbis = [X̄_correct - X̄_incorrect] / s_X * sqrt(P_i * (1 - P_i))
      (Đo lường mức độ câu hỏi phân biệt học sinh giỏi và học sinh trung bình).
    """
    if item_matrix is None or item_matrix.size == 0:
        return []

    arr = np.array(item_matrix, dtype=float)
    if arr.ndim != 2:
        return []

    n_students, k_items = arr.shape
    if n_students < 3:
        return []

    total_scores = np.sum(arr, axis=1)
    s_x = float(np.std(total_scores, ddof=1))

    if not item_names or len(item_names) != k_items:
        item_names = [f"Câu {i+1}" for i in range(k_items)]

    results = []
    for i in range(k_items):
        item_scores = arr[:, i]
        # P_i: Tỉ lệ làm đúng
        p_i = float(np.mean(item_scores))

        # Phân nhóm đúng và sai
        correct_mask = item_scores > 0.5
        incorrect_mask = ~correct_mask

        n_correct = int(np.sum(correct_mask))
        n_incorrect = n_students - n_correct

        if n_correct == 0 or n_incorrect == 0 or s_x <= 1e-9:
            # Tất cả làm đúng hoặc tất cả làm sai: không có độ phân biệt
            r_pbis = 0.0
        else:
            mean_correct = float(np.mean(total_scores[correct_mask]))
            mean_incorrect = float(np.mean(total_scores[incorrect_mask]))
            # Công thức Point-Biserial chuẩn
            r_pbis = ((mean_correct - mean_incorrect) / s_x) * math.sqrt(p_i * (1.0 - p_i))
            r_pbis = float(np.clip(r_pbis, -1.0, 1.0))

        # Đánh giá độ phân biệt theo chuẩn ETS
        if r_pbis >= 0.40:
            discrim_label = "Rất tốt (Phân hóa xuất sắc)"
            discrim_color = "#16a34a"
            recommendation = "Giữ nguyên"
        elif r_pbis >= 0.30:
            discrim_label = "Tốt (Phân biệt chuẩn)"
            discrim_color = "#0284c7"
            recommendation = "Giữ nguyên"
        elif r_pbis >= 0.20:
            discrim_label = "Tạm chấp nhận"
            discrim_color = "#d97706"
            recommendation = "Cân nhắc trau chuốt phương án nhiễu"
        else:
            discrim_label = "Kém (Cần cảnh báo / loại bỏ)"
            discrim_color = "#dc2626"
            recommendation = "Cần biên soạn lại hoặc loại khỏi ngân hàng đề"

        # Đánh giá độ khó
        if p_i > 0.85:
            diff_label = "Rất dễ (Nhận biết cơ bản)"
        elif p_i >= 0.65:
            diff_label = "Dễ (Thông hiểu)"
        elif p_i >= 0.35:
            diff_label = "Trung bình (Vận dụng)"
        elif p_i >= 0.15:
            diff_label = "Khó (Vận dụng cao)"
        else:
            diff_label = "Rất khó (Cực khó)"

        results.append({
            "item_name": item_names[i],
            "difficulty_p": round(p_i, 3),
            "difficulty_label": diff_label,
            "rpbis": round(r_pbis, 3),
            "discrimination_label": discrim_label,
            "discrimination_color": discrim_color,
            "recommendation": recommendation,
            "n_correct": n_correct,
            "n_total": n_students
        })

    return results


def extract_item_matrix_from_attempts(attempts_list: List[Dict[str, Any]]) -> Tuple[np.ndarray, List[str]]:
    """
    Bóc tách answers_json từ danh sách bản ghi bảng exam_attempts trong SQLite
    để tạo thành ma trận nhị phân (N học sinh x K câu hỏi).
    """
    if not attempts_list:
        return np.empty((0, 0)), []

    # Thu thập tất cả các key câu hỏi xuất hiện
    all_q_keys = set()
    parsed_attempts = []
    for att in attempts_list:
        ans_raw = att.get("answers_json") or att.get("answers")
        if isinstance(ans_raw, str):
            try:
                ans_dict = json.loads(ans_raw)
            except Exception:
                ans_dict = {}
        elif isinstance(ans_raw, dict):
            ans_dict = ans_raw
        else:
            ans_dict = {}

        # Lọc các key trắc nghiệm (p1, p2, p3)
        valid_keys = {k: v for k, v in ans_dict.items() if any(k.startswith(p) for p in ["p1_", "p2_", "p3_"])}
        all_q_keys.update(valid_keys.keys())
        parsed_attempts.append(valid_keys)

    sorted_keys = sorted(list(all_q_keys))
    if not sorted_keys or len(parsed_attempts) < 2:
        return np.empty((0, 0)), []

    # Xây dựng ma trận: nếu câu hỏi được trả lời đúng = 1, sai/bỏ qua = 0
    matrix = []
    for att in parsed_attempts:
        row = []
        for k in sorted_keys:
            val = att.get(k)
            # Nếu val là dict hoặc boolean hoặc có cờ is_correct
            if isinstance(val, dict):
                is_correct = 1.0 if val.get("is_correct") or val.get("correct") else 0.0
            elif isinstance(val, bool):
                is_correct = 1.0 if val else 0.0
            elif isinstance(val, (int, float)):
                is_correct = 1.0 if val > 0 else 0.0
            elif isinstance(val, str) and val.strip().lower() in ["đúng", "true", "correct", "1"]:
                is_correct = 1.0
            else:
                is_correct = 0.0
            row.append(is_correct)
        matrix.append(row)

    item_names = [f"Câu {k.replace('p1_', 'I.').replace('p2_', 'II.').replace('p3_', 'III.')}" for k in sorted_keys]
    return np.array(matrix, dtype=float), item_names


def generate_benchmark_psychometric_sample(n_students: int = 35, k_items: int = 22, seed: int = 2026) -> Tuple[np.ndarray, List[str]]:
    """
    Sinh ma trận dữ liệu thực nghiệm mẫu chuẩn hóa GDPT 2018 (N=35 học sinh x K=22 câu hỏi)
    dựa trên mô hình Logistic 2 tham số (2PL IRT) để Hội đồng KHKT thẩm định trực tiếp ngay cả khi chưa thi.
    """
    rng = np.random.RandomState(seed)

    # Năng lực học sinh θ_j phân phối chuẩn N(0, 1)
    thetas = rng.normal(0.0, 1.0, n_students)

    # Tham số câu hỏi: Độ khó b_i (-2 đến +2), Độ phân biệt a_i (0.8 đến 2.2)
    b_params = np.linspace(-1.8, 1.8, k_items)
    a_params = rng.uniform(0.9, 2.1, k_items)
    # Cài đặt cố ý 1-2 câu có độ phân biệt thấp (r_pbis < 0.2) để kiểm thử tính năng cảnh báo câu hỏi kém
    a_params[3] = 0.15 # Câu 4 độ phân biệt kém
    a_params[-2] = 0.12 # Câu kế cuối độ phân biệt kém

    matrix = np.zeros((n_students, k_items), dtype=float)
    for j in range(n_students):
        for i in range(k_items):
            # Xác suất làm đúng theo mô hình Rasch/2PL
            prob = 1.0 / (1.0 + np.exp(-a_params[i] * (thetas[j] - b_params[i])))
            matrix[j, i] = 1.0 if rng.rand() < prob else 0.0

    item_names = [f"Câu {i+1} ({'Phần I' if i < 12 else 'Phần II' if i < 16 else 'Phần III'})" for i in range(k_items)]
    return matrix, item_names
