# VIP 74.1 - HỆ THỐNG GIA SƯ AI THPT 2026 (CHUẨN GDPT 2018 - BẢN VÁ HOÀN THIỆN ĐA MÔN & ĐA KHỐI LỚP)
"""
SERVICE CHẤM ĐIỂM KHẢO THÍ CHUẨN QUỐC GIA (SCORING SERVICE) - GSAI THPT 2026
Tuân thủ 100% Quyết định số 764/QĐ-BGDĐT của Bộ Giáo dục và Đào tạo.
"""
import math
import re
from typing import Dict, Any, List, Tuple

def numeric_answer_matches(user_answer, expected_answer, decimals=None) -> bool:
    """So khớp đáp án số Phần III có tính đến sai số làm tròn thực nghiệm (đồng bộ 100% với app.py)."""
    user = str(user_answer or "").strip().replace(",", ".")
    expected = str(expected_answer or "").strip().replace(",", ".")
    if not user or not expected:
        return False
    try:
        u, e = float(user), float(expected)
        if not math.isfinite(u) or not math.isfinite(e):
            return False
        if decimals is not None:
            digits = int(decimals)
            if 0 <= digits <= 10:
                return round(u, digits) == round(e, digits)
        # Dung sai làm tròn thực nghiệm
        if math.isclose(u, e, rel_tol=1e-4, abs_tol=0.015):
            return True
        exp_dec = len(expected.split(".")[1]) if "." in expected else 0
        user_dec = len(user.split(".")[1]) if "." in user else 0
        if exp_dec > 0 and user_dec < exp_dec:
            return False
        if 0 <= exp_dec <= 2:
            return round(u, exp_dec) == round(e, exp_dec)
        return False
    except ValueError:
        return user.lower() == expected.lower()

def calculate_part2_statement_score(correct_statements: int) -> float:
    """
    Thang điểm bậc thang Phần II (Trắc nghiệm Đúng/Sai) theo Quyết định 764/QĐ-BGDĐT:
    - Đúng 1 ý: 0.1 điểm
    - Đúng 2 ý: 0.25 điểm
    - Đúng 3 ý: 0.5 điểm
    - Đúng 4 ý: 1.0 điểm
    """
    if correct_statements == 1:
        return 0.1
    elif correct_statements == 2:
        return 0.25
    elif correct_statements == 3:
        return 0.5
    elif correct_statements == 4:
        return 1.0
    return 0.0

def grade_part1(questions: List[Dict[str, Any]], user_answers: Dict[str, Any], max_score: float = None, subject: str = "Toán học") -> Tuple[float, int, int]:
    """Chấm điểm Phần I (Trắc nghiệm 4 chọn 1) theo Quyết định 764/QĐ-BGDĐT."""
    if not questions:
        return 0.0, 0, 0
    correct_count = 0
    total = len(questions)
    for idx, q in enumerate(questions):
        user_choice = str(user_answers.get(f"p1_{idx}", "")).strip()
        expected = str(q.get("ans", "")).strip().upper()
        user_letter = re.sub(r'[^A-D]', '', user_choice[:3]).upper()[:1] if user_choice else ""
        if user_letter and expected and user_letter == expected:
            correct_count += 1
        elif user_choice and expected and (user_choice == expected or user_choice.startswith(expected)):
            correct_count += 1
    if max_score is not None:
        target_max = float(max_score)
    elif subject == "Tiếng Anh":
        target_max = 10.0
    elif any(k in str(subject).lower() for k in ["vật lý", "vật lí", "hóa học", "sinh học", "khtn", "khoa học tự nhiên"]):
        target_max = 4.5
    elif any(k in str(subject).lower() for k in ["lịch sử", "địa lý", "địa lí", "gdkt", "công dân", "tin học", "công nghệ"]):
        target_max = 6.0
    else: # Môn Toán học hoặc mặc định
        target_max = 3.0
    score = (correct_count / total) * target_max if total > 0 else 0.0
    return round(score, 2), correct_count, total

def grade_part2(questions: List[Dict[str, Any]], user_answers: Dict[str, Any]) -> Tuple[float, int, int]:
    """Chấm điểm Phần II (Trắc nghiệm Đúng/Sai lũy tiến)."""
    if not questions:
        return 0.0, 0, 0
    total_score = 0.0
    total_stmts = 0
    correct_stmts = 0
    for q_idx, q in enumerate(questions):
        stmts = q.get("stmts", [])
        q_correct = 0
        for s_idx, stmt in enumerate(stmts):
            total_stmts += 1
            user_val = str(user_answers.get(f"p2_{q_idx}_{s_idx}", "Chưa chọn")).strip()
            expected_bool = stmt.get("a") if "a" in stmt else stmt.get("ans", True)
            expected_str = "Đúng" if expected_bool else "Sai"
            if user_val == expected_str:
                q_correct += 1
                correct_stmts += 1
        total_score += calculate_part2_statement_score(q_correct)
    return round(total_score, 2), correct_stmts, total_stmts

def grade_part3(questions: List[Dict[str, Any]], user_answers: Dict[str, Any], max_score: float = None, subject: str = "Toán học") -> Tuple[float, int, int]:
    """Chấm điểm Phần III (Trả lời ngắn) có xét dung sai sai số làm tròn thực nghiệm chuẩn thi KHKT."""
    if not questions:
        return 0.0, 0, 0
    correct_count = 0
    total = len(questions)
    for idx, q in enumerate(questions):
        user_val = str(user_answers.get(f"p3_{idx}", "")).strip()
        expected = str(q.get("ans", "")).strip()
        if numeric_answer_matches(user_val, expected, q.get("rounding_decimals")):
            correct_count += 1
    if max_score is not None:
        score = (correct_count / total) * float(max_score) if total > 0 else 0.0
    elif any(k in str(subject).lower() for k in ["vật lý", "vật lí", "hóa học", "sinh học", "khtn", "khoa học tự nhiên"]):
        score = correct_count * 0.25 # 6 câu x 0.25 = 1.5 điểm
    else:
        score = correct_count * 0.5 # Môn Toán 6 câu x 0.5 = 3.0 điểm
    return round(score, 2), correct_count, total
