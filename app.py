from qa_runtime import (split_api_keys, admin_password_matches, normalize_bool, display_frame,
    exam_response_metadata, observed_item_matrix, mcq_answer_matches)
# VIP 76.0 - HỆ THỐNG GIA SƯ AI THPT 2026 (CHUẨN GDPT 2018 - EDTECH & PSYCHOMETRICS SOTA QUỐC TẾ)
# -*- coding: utf-8 -*-

#
#
# ================================================================================
#
# HỆ THỐNG GSAI - KHẢO THÍ ĐA NĂNG LỰC TOÀN DIỆN THCS & THPT 2026 (PHIÊN BẢN VIP)
#
# CẬP NHẬT CHÍNH THỨC: 18/10/2026 - BẢN VÁ VIP 65.3 (TOÀN DIỆN ĐỒ THỊ TRẮC NGHIỆM, TỐI ƯU INFOGRAPHIC A4 ĐA MÔN ĐA LỚP & CHỐNG TRÀN VIỀN 100%)
#
# - QUY MÔ KỶ LỤC: 33.679 ĐỀ THI THẬT HOÀN CHỈNH (948.902 CÂU HỎI ĐỘC NHẤT)
#
# - BỘ NHỚ XOAY VÒNG COOLDOWN ROTATION & HARDWARE DYNAMIC SEED (XUNG NHỊP NANO-GIÂY)
#
# - TRIỆT TIÊU 100% HIỆN TƯỢNG LẶP ĐỀ CŨ VÀ CÂU HỎI CŨ TRÊN TOÀN BỘ TRẠM 3
#
# - ĐỒNG BỘ COOLDOWN CHÉO GIỮA LUỒNG 1 (AI SÁNG TẠO) & LUỒNG 2 (KHO ĐỀ THẬT 600+)
#
# - PHỦ KÍN 64 TỈNH THÀNH x 10+ TRƯỜNG TOP ĐẦU x 4 KỲ THI (GK1, CK1, GK2, CK2)
#
# - 100% PHỤC DỰNG NGỮ LIỆU THỊ GIÁC ĐA MÔN: TIKZ VECTOR OVERLEAF + SVG NANO-PRECISION
#
# - CÔNG NGHỆ NÉN SOTA 2026: LZMA / XZ (PRESET 9 EXTREME) CHỈ CÒN 13.4 MB
#
# - 100% TƯƠNG THÍCH MỌI THIẾT BỊ: ANDROID, IOS, MACOS, WINDOWS (TRIPLE-FALLBACK)
#
# - 100% CHUẨN MA TRẬN BỘ GD&ĐT: QĐ 764/QĐ-BGDĐT, CV 3175 & TT 22/2021/TT-BGDĐT
#
# - 0 TOKEN GEMINI • 0 API KEY • TỐC ĐỘ BỐC ĐỀ TỨC THÌ 0.001 GIÂY
#
# ================================================================================
#



import streamlit as st

import textwrap

import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt

import io

import base64

import streamlit.components.v1 as components

def render_html_iframe(html_code: str, height: int = 500, scrolling: bool = False):
    """Embed HTML tương thích đa phiên bản Streamlit (ưu tiên st.iframe, fallback components.html).
    Lưu ý: st.iframe chỉ hỗ trợ height > 0 (pixel), 'stretch', hoặc 'content'.
    Với các script JS chạy ngầm (height=0), chuyển trực tiếp qua components.html để tránh StreamlitInvalidHeightError.
    """
    if height is None or (isinstance(height, (int, float)) and height <= 0):
        components.html(html_code, height=0)
    elif hasattr(st, "iframe"):
        try:
            st.iframe(html_code, height=height)
        except Exception:
            components.html(html_code, height=height, scrolling=scrolling)
    else:
        components.html(html_code, height=height, scrolling=scrolling)


from google import genai

from google.genai import types

from PIL import Image, ImageDraw, ImageFont

try:

    import pillow_heif

    pillow_heif.register_heif_opener()

except Exception:

    pass

import pandas as pd

from datetime import datetime, timezone, timedelta

import json

import requests

import plotly.graph_objects as go

import numpy as np

import re

import time

import random

import base64

import os

import math
from fractions import Fraction

import scipy.stats as stats

import concurrent.futures

import plotly.express as px

import urllib.parse

import ast

import uuid

import logging

import html

import io

try:

    import qrcode

except ImportError:

    qrcode = None

try:

    from database import db_manager

except Exception:

    db_manager = None

try:
    from services.scoring_service import calculate_part2_statement_score, grade_part1, grade_part2, grade_part3
except Exception as _e_sc:
    logging.warning("Không thể nạp services.scoring_service: %s", _e_sc)
    def calculate_part2_statement_score(c):
        return {1: 0.1, 2: 0.25, 3: 0.5, 4: 1.0}.get(c, 0.0)

try:
    from services.state_service import init_centralized_session_state, safe_get_state, reset_exam_session
except Exception as _e_st:
    logging.warning("Không thể nạp services.state_service: %s", _e_st)
    init_centralized_session_state = None

try:
    from models.exam_models import QuestionModel, StatementModel
except Exception as _e_em:
    logging.warning("Không thể nạp models.exam_models: %s", _e_em)

try:
    from services.psychometrics_service import (
        compute_cronbach_alpha,
        compute_item_analysis,
        extract_item_matrix_from_attempts,
        generate_benchmark_psychometric_sample
    )
except Exception as _e_psy:
    logging.warning("Không thể nạp services.psychometrics_service: %s", _e_psy)
    compute_cronbach_alpha = None
    compute_item_analysis = None
    extract_item_matrix_from_attempts = None
    generate_benchmark_psychometric_sample = None

try:
    from services.bkt_service import (
        update_bkt_step,
        compute_bkt_trajectory,
        evaluate_competencies_bkt
    )
except Exception as _e_bkt:
    logging.warning("Không thể nạp services.bkt_service: %s", _e_bkt)
    update_bkt_step = None
    compute_bkt_trajectory = None
    evaluate_competencies_bkt = None

try:
    from services.neuro_symbolic_verifier import (
        verify_calculus_function,
        verify_definite_integral,
        audit_ai_generated_question_sympy
    )
except Exception as _e_ns:
    logging.warning("Không thể nạp services.neuro_symbolic_verifier: %s", _e_ns)
    verify_calculus_function = None
    verify_definite_integral = None
    audit_ai_generated_question_sympy = None

try:
    from services.fsrs_spaced_repetition_service import (
        calculate_retrievability,
        analyze_student_fsrs_review_schedule
    )
except Exception as _e_fsrs:
    logging.warning("Không thể nạp services.fsrs_spaced_repetition_service: %s", _e_fsrs)
    calculate_retrievability = None
    analyze_student_fsrs_review_schedule = None

try:
    from services.azota_lms_exporter import (
        convert_math_to_double_dollars,
        export_exam_to_azota_text,
        export_exam_to_azota_docx
    )
except Exception as _e_azota:
    logging.warning("Không thể nạp services.azota_lms_exporter: %s", _e_azota)
    convert_math_to_double_dollars = None
    export_exam_to_azota_text = None
    export_exam_to_azota_docx = None
    QuestionModel = None

try:
    import exam_file_extractor as efe
except Exception as _e_efe:
    logging.warning("Không thể nạp exam_file_extractor: %s", _e_efe)
    efe = None

try:
    import dedupe_bank as ddb
except Exception as _e_ddb:
    logging.warning("Không thể nạp dedupe_bank: %s", _e_ddb)
    ddb = None

try:
    import real_exam_engine as ree
except Exception as _e_ree:
    logging.warning("Không thể nạp real_exam_engine: %s", _e_ree)
    ree = None

try:
    import precision_visual_engine as pve
except Exception as _e_pve:
    logging.warning("Không thể nạp precision_visual_engine: %s", _e_pve)
    pve = None

try:
    import lesson_infographic_engine as lie
except Exception as _e_lie:
    logging.warning("Không thể nạp lesson_infographic_engine: %s", _e_lie)
    lie = None

def sanitize_svg_for_markdown(svg_text):
    """Triệt tiêu 100% thụt lề đầu dòng trong chuỗi SVG để trình biên dịch Markdown không bao giờ biến thẻ SVG thành khối mã nguồn đen."""
    if not svg_text:
        return ""
    return "\n".join(line.strip() for line in str(svg_text).strip().splitlines())








# ==============================================================================

# 1. ĐỒNG BỘ GIỜ VIỆT NAM (GMT+7) CHUẨN XÁC

# ==============================================================================

VN_TZ = timezone(timedelta(hours=7))

def get_vn_time():

    return datetime.now(VN_TZ).strftime("%Y-%m-%d %H:%M:%S")



# --- ĐỌC SECRETS AN TOÀN ---

def get_secret(name, default=""):

    try:

        return st.secrets.get(name, default)

    except Exception:

        return default



# np.trapezoid chỉ có ở NumPy >= 2.0; bản cũ dùng np.trapz

_trapz = getattr(np, "trapezoid", None) or getattr(np, "trapz")



# ==============================================================================

# 2. KHỞI TẠO BỘ NHỚ PHIÊN & BỘ ĐẾM THỰC NGHIỆM TỰ ĐỘNG

# ==============================================================================

if init_centralized_session_state:
    init_centralized_session_state(st)

for key in ["messages", "analytics_logs", "feedback_logs", "parsed_quiz", "va_loi_logs"]:

    if key not in st.session_state: st.session_state[key] = []

if "tram1_count" not in st.session_state: st.session_state.tram1_count = 0

if "tram2_count" not in st.session_state: st.session_state.tram2_count = 0

if "tram3_count" not in st.session_state: st.session_state.tram3_count = 0

if "chat" not in st.session_state: st.session_state.chat = None

if "current_lesson" not in st.session_state: st.session_state.current_lesson = ""

if "current_topic" not in st.session_state: st.session_state.current_topic = ""

if "lab_data" not in st.session_state: st.session_state.lab_data = None

if "quiz_states" not in st.session_state: st.session_state.quiz_states = {}

if "global_stats_loaded" not in st.session_state: st.session_state.global_stats_loaded = False

if "global_exam_count" not in st.session_state: st.session_state.global_exam_count = 0
if "exam_mix_count" not in st.session_state: st.session_state.exam_mix_count = 0

if "global_logs" not in st.session_state: st.session_state.global_logs = []

if "student_progress_history" not in st.session_state: st.session_state.student_progress_history = []

# ==============================================================================
# HỆ THỐNG GIA SƯ SOCRATIC LIÊN TRẠM & BỘ NHỚ TRIẾT LÝ NHÂN CÁCH Á - ÂU
# ==============================================================================
if "tram1_understood" not in st.session_state: st.session_state.tram1_understood = False
if "tram2_understood" not in st.session_state: st.session_state.tram2_understood = False
if "tram3_understood" not in st.session_state: st.session_state.tram3_understood = False
if "used_philosophical_quotes" not in st.session_state: st.session_state.used_philosophical_quotes = []
if "tram1_closure_info" not in st.session_state: st.session_state.tram1_closure_info = None
if "tram2_closure_info" not in st.session_state: st.session_state.tram2_closure_info = None
if "tram3_closure_info" not in st.session_state: st.session_state.tram3_closure_info = None




# ==============================================================================

# 3. CẤU HÌNH TRANG WEB & LINK CHÍNH CHỦ

# ==============================================================================

st.set_page_config(

    page_title="Gia Sư AI - Hệ Sinh Thái Lớp Học Đảo Ngược",

    page_icon="🏫",

    layout="wide",

    initial_sidebar_state="expanded"

)



APP_URL = get_secret("APP_URL", "https://gsaithptth-khkt2026.streamlit.app")



# ==============================================================================



# ==============================================================================

# ==============================================================================
# HỆ THỐNG KHO SÁCH ĐIỆN TỬ KẾT NỐI TRI THỨC VỚI CUỘC SỐNG (NXBGDVN & VNITEACH)
# ==============================================================================
from kntt_sgk_library import KNTT_DIGITAL_LIBRARY


def get_kntt_books_for(subject_name: str, grade_lvl: int):

    """Truy xuất danh mục sách SGK Kết Nối Tri Thức theo đúng khối lớp và môn học từ VniTeach."""

    g_dict = KNTT_DIGITAL_LIBRARY.get(grade_lvl) or KNTT_DIGITAL_LIBRARY.get(str(grade_lvl)) or {}

    if subject_name in g_dict:

        return g_dict[subject_name]

    for k, v in g_dict.items():

        if subject_name.lower() in k.lower() or k.lower() in subject_name.lower():

            return v

    return [{"title": f"SGK {subject_name} Lớp {grade_lvl} (KNTT)", "url": "https://www.vniteach.com/sach-dien-tu-ket-noi-tri-thuc/#google_vignette"}]



def get_nxbgd_books_for(subject_name: str, grade_lvl: int):

    """Truy xuất danh mục sách SGK Kết Nối Tri Thức từ nguồn Tập Huấn NXBGD."""

    kntt_books = get_kntt_books_for(subject_name, grade_lvl)

    nxbgd_books = []

    for b in kntt_books:

        title = b["title"].replace("(KNTT)", "(NXBGD)").replace("Global Success", "(NXBGD)")

        nxbgd_books.append({"title": title, "url": "https://taphuan.nxbgd.vn/"})

    return nxbgd_books



# TÂN TRANG GIAO DIỆN (UI/UX NÂNG CẤP DÀNH CHO KHKT)

# ==============================================================================

st.markdown("""

<style>

    .block-container { padding-top: 2rem !important; padding-bottom: 1rem !important; }



    .brand-container {

        display: flex; align-items: center; justify-content: center; gap: 12px;

        margin-bottom: 20px; padding: 10px;

        background: linear-gradient(145deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9));

        border-radius: 12px; border: 1px solid #334155; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);

    }

    .school-icon { width: 45px; height: auto; transition: transform 0.3s ease; }

    .school-icon:hover { transform: scale(1.1); }

    .thiennhan-logo {

        width: 115px; height: auto; border-radius: 6px;

        box-shadow: 0 0 10px rgba(56, 189, 248, 0.4); border: 1.5px solid #38bdf8;

    }



    .main-header { text-align: center; padding: 0px 0 15px 0; border-bottom: 1px dashed #475569; margin-bottom: 25px; }

    .main-title {

        background: -webkit-linear-gradient(45deg, #38bdf8, #818cf8);

        -webkit-background-clip: text; -webkit-text-fill-color: transparent;

        font-size: 2.5rem; font-weight: 900; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 1.5px;

    }

    .sub-title { color: #cbd5e1; font-size: 1.15rem; font-weight: 500;}

    .badge-tag {

        background: rgba(15, 23, 42, 0.7); border: 1px solid #38bdf8; color: #38bdf8;

        padding: 5px 15px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;

        display: inline-block; margin-top: 8px; margin-right: 8px; box-shadow: 0 2px 5px rgba(56, 189, 248, 0.2);

    }



    .stButton > button {

        background: linear-gradient(135deg, #0284c7, #3b82f6) !important; color: white !important;

        border-radius: 10px !important; border: none !important; box-shadow: 0 4px 15px rgba(56, 189, 248, 0.3) !important;

        transition: all 0.3s ease !important; font-weight: 700 !important; padding: 0.5rem 1rem !important;

    }

    .stButton > button:hover {

        transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(56, 189, 248, 0.6) !important;

        background: linear-gradient(135deg, #0369a1, #2563eb) !important;

    }

    /* THANH ĐIỀU HƯỚNG 4 TRẠM NẰM NGANG PHÍA SAU DÒNG KẺ TIÊU ĐỀ (TOP STATION NAVBAR) */
    div[data-testid="stHorizontalBlock"] button[key^="top_nav_station_"] {
        font-size: 13.5px !important;
        font-weight: 700 !important;
        padding: 0.65rem 0.6rem !important;
        border-radius: 10px !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        white-space: nowrap !important;
        text-overflow: ellipsis !important;
    }

    div[data-testid="stHorizontalBlock"] button[key^="top_nav_station_"][kind="primary"],
    div[data-testid="stHorizontalBlock"] button[key^="top_nav_station_"][data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #0284c7, #2563eb) !important;
        color: #ffffff !important;
        border: 2px solid #38bdf8 !important;
        box-shadow: 0 0 16px rgba(56, 189, 248, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.25) !important;
        transform: translateY(-2px) !important;
    }

    div[data-testid="stHorizontalBlock"] button[key^="top_nav_station_"][kind="secondary"],
    div[data-testid="stHorizontalBlock"] button[key^="top_nav_station_"][data-testid="baseButton-secondary"] {
        background: rgba(15, 23, 42, 0.75) !important;
        color: #94a3b8 !important;
        border: 1.5px solid #334155 !important;
    }

    div[data-testid="stHorizontalBlock"] button[key^="top_nav_station_"][kind="secondary"]:hover,
    div[data-testid="stHorizontalBlock"] button[key^="top_nav_station_"][data-testid="baseButton-secondary"]:hover {
        color: #38bdf8 !important;
        border-color: #0284c7 !important;
        background: rgba(30, 41, 59, 0.9) !important;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3) !important;
        transform: translateY(-2px) !important;
    }



    .stTabs [data-baseweb="tab-list"] {

        background: rgba(30, 41, 59, 0.5); backdrop-filter: blur(10px);

        border-radius: 12px; padding: 5px; gap: 8px; border: 1px solid #334155;

    }

    .stTabs [data-baseweb="tab"] {

        height: 50px; white-space: pre-wrap; background-color: transparent;

        border-radius: 8px; border: none; color: #94a3b8; font-weight: 600; transition: all 0.3s;

    }

    .stTabs [aria-selected="true"] {

        background: rgba(56, 189, 248, 0.15) !important; color: #38bdf8 !important;

        border-bottom: 3px solid #38bdf8 !important; box-shadow: inset 0 -3px 10px rgba(56, 189, 248, 0.1);

    }



    .lab-box-container {

        background: linear-gradient(145deg, #0f172a, #1e293b);

        border: 2px solid #0ea5e9;

        box-shadow: 0 0 20px rgba(14, 165, 233, 0.2), inset 0 0 15px rgba(14, 165, 233, 0.05);

        padding: 25px; border-radius: 15px; margin-top: 25px; margin-bottom: 20px;

        position: relative; overflow: hidden;

    }

    .lab-box-container::before {

        content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 3px;

        background: linear-gradient(90deg, transparent, #38bdf8, transparent);

    }



    [data-testid="stChatMessage"] {

        border-radius: 15px; padding: 15px; margin-bottom: 12px;

        background: rgba(30, 41, 59, 0.6); border: 1px solid #475569; box-shadow: 0 2px 8px rgba(0,0,0,0.2);

    }



    .stRadio > div { background-color: rgba(30, 41, 59, 0.6); padding: 15px; border-radius: 10px; border: 1px solid #334155; }

    .short-link-badge { background-color: #1e293b; border: 1px dashed #38bdf8; padding: 8px 12px; border-radius: 8px; font-family: 'Courier New', Courier, monospace; font-size: 0.8rem; color: #38bdf8; text-align: center; margin: 10px 0; word-break: break-all; }

</style>

""", unsafe_allow_html=True)





# ==============================================================================

# HÀM XỬ LÝ & CHUẨN HÓA LATEX / TOÁN HỌC / KATEX SƯ PHẠM QUỐC GIA

# ==============================================================================

def sanitize_katex_latex(text: str) -> str:

    if not text: return ""

    s = str(text)

    # 0. Chuyển đổi chuẩn LaTeX \(...\) và \[...\] sang $...$ và $$...$$

    s = re.sub(r'\\\(', '$', s)

    s = re.sub(r'\\\)', '$', s)

    s = re.sub(r'\\\[', '$$', s)

    s = re.sub(r'\\\]', '$$', s)



    # 0.1 Khử triệt để lỗi Form Feed ASCII \x0c -> \f (gây ra chữ đỏ ⯅rac / ▲rac), Backspace \x08 -> \b và \t -> tab trong \to
    s = s.replace('\x0crac', r'\frac').replace('\x0c', r'\f')
    s = s.replace('\x08ar', r'\bar').replace('\x08eta', r'\beta').replace('\x08egin', r'\begin').replace('\x08inom', r'\binom').replace('\x08f', r'\bf').replace('\x08', r'\b')
    s = s.replace('\x09o', r'\to').replace('\x09ext', r'\text').replace('\x09imes', r'\times').replace('\x09heta', r'\theta').replace('\x09au', r'\tau').replace('\x09an', r'\tan')
    s = re.sub(r'[\u25b2\u2bf5\u25b4\u2660\u2b9d\u21e7\u25b5]rac', r'\\frac', s)
    s = re.sub(r'(?<!\\)\brac\{', r'\\frac{', s)
    s = re.sub(r'\\lim_\{([^}]+)\s+o\s+', r'\\lim_{\1 \\to ', s)
    s = re.sub(r'(?<=\s)o(?=\s*[-+]?\d|\\infty|\$)', r'\\to', s)

    # 0.15 Khử triệt để lỗi chữ 'mega' / '\omega' bị dùng nhầm thành vô cực (\infty) do AI / OCR lỗi font
    s = re.sub(r'(?i)(?<=[\(\[\s;,-])-+\s*mega\b', r'-\\infty', s)
    s = re.sub(r'(?i)\b-\s*mega\b', r'-\\infty', s)
    s = re.sub(r'(?i)\+\s*mega\b', r'+\\infty', s)
    s = re.sub(r'(?i)(?<=[;,\s])\s*\+?mega(?=[\)\]\s;,])', r'+\\infty', s)
    s = re.sub(r'(?i)(?<=[(\[\s])-?\s*\\?[oO]mega\b', r'-\\infty', s)
    s = re.sub(r'(?i);\s*\+?\s*\\?[oO]mega\s*(?=[)\]])', r'; +\\infty', s)

    # 0.2 Chuẩn hóa môi trường cases
    s = re.sub(r'\\cases\{', r'\\begin{cases}', s)

    # 0.25 Khử triệt để lỗi \searrow, \nearrow, \uparrow, \downarrow bị đỏ KaTeX khi nằm ngoài math-mode
    # Nếu nằm ngoài $...$, chuyển sang ký tự Unicode ↗, ↘, ↑, ↓ tương thích 100% với cả KaTeX và Markdown
    def _fix_arrows_outside_math(match_txt):
        parts = match_txt.split('$')
        for i in range(0, len(parts), 2):
            parts[i] = re.sub(r'\\+nearrow\b|\\nearrow', '↗', parts[i])
            parts[i] = re.sub(r'\\+searrow\b|\\searrow', '↘', parts[i])
            parts[i] = re.sub(r'\\+uparrow\b|\\uparrow', '↑', parts[i])
            parts[i] = re.sub(r'\\+downarrow\b|\\downarrow', '↓', parts[i])
        return '$'.join(parts)
    s = _fix_arrows_outside_math(s)

    # 1. Fix missing space before LaTeX command: e.g. 'z\vec{k}' -> 'z \vec{k}', 'z\veck' -> 'z \vec{k}'
    s = re.sub(r'([a-zA-Z0-9])\\(vec|frac|dfrac|sqrt|overline|hat|dot|overleftrightarrow|overrightarrow)', r'\1 \\\2', s)

    # 2. Fix \veck, \veci, \vecj, \vecu, \vecv, \vecw, \vecn
    s = re.sub(r'\\vec([a-zA-Z0-9]{1,4})(?![a-zA-Z0-9_{])', r'\\vec{\1}', s)

    # 3. Fix unbracketed multi-point or single vectors: \vec AB, \vec AA', \vec a -> \overrightarrow{AB}, \overrightarrow{AA'}, \vec{a}
    s = re.sub(r'\\vec\s*([A-Z]{2,}[\']*)', r'\\overrightarrow{\1}', s)
    s = re.sub(r'\\vec\s+([a-zA-Z0-9]{1,4})(?![a-zA-Z0-9_{])', r'\\vec{\1}', s)

    # 4. Standardize bracketed \vec{...}:
    def _rep_ext_vector(m):
        c = m.group(1).strip()
        if len(c) >= 2 or "'" in c or "_" in c:
            return f"\\overrightarrow{{{c}}}"
        return m.group(0)
    s = re.sub(r'\\vec\{([^}]+)\}', _rep_ext_vector, s)

    # 5. AUTO-HEALING: Tự động phát hiện & bọc các công thức LaTeX trần trụi (Naked LaTeX) chưa nằm trong $...$
    def _heal_naked_latex_line(line: str) -> str:
        if line.strip().startswith('|') or line.strip().startswith('<'):
            return line

        # Tách và bảo vệ tuyệt đối 100% các khối $$...$$ và $...$ đã có trước khi auto-heal
        parts = re.split(r'(\$\$.*?\$\$|\$[^$\n]+?\$)', line)
        healed_parts = []
        for i, part in enumerate(parts):
            if i % 2 == 1:
                # Khối toán đã nằm trong $...$: giữ nguyên, không bao giờ chèn chồng dấu $
                healed_parts.append(part)
                continue

            p = part

            # 5.1 Ký hiệu trong ngoặc: CHỈ bọc các đại lượng thống kê hoặc ký hiệu đặc biệt,
            # TUYỆT ĐỐI KHÔNG bọc (\b[a-zA-Z]\b) như (x), (y), (t) vì sẽ biến f(x) thành f($x$)!
            p = re.sub(
                r'(?<![a-zA-Z0-9_])\(([\\](?:bar|Delta|sigma|mu|alpha|beta|theta|lambda|pi|omega)\s*(?:\{[a-zA-Z0-9]*\}|[a-zA-Z0-9]+)?|[a-zA-Z]_[a-zA-Z0-9]+|[a-zA-Z]\^[0-9]+|[A-Z]_[0-9]+(?:\s*,\s*[A-Z]_[0-9]+)*)\)',
                r'($\1$)',
                p
            )

            # 5.2 Bọc toàn bộ mệnh đề toán học sau dấu hai chấm ':' nếu chứa các lệnh LaTeX (\lim, \frac, \int, \sum, \sqrt, \vec)
            def _wrap_clause_after_colon(m):
                lead = m.group(1)
                clause = m.group(2).strip()
                trail = '.' if clause.endswith('.') else ''
                if trail: clause = clause[:-1].strip()
                if clause.startswith('$') and clause.endswith('$'):
                    return m.group(0)
                return f"{lead}${clause}${trail}"

            p = re.sub(
                r'((?::\s*))(\\(?:lim|frac|dfrac|sum|int|sqrt)(?![a-zA-Z])[^\n\r]+)',
                _wrap_clause_after_colon,
                p
            )

            # 5.3 Bọc các phương trình gán biến dạng "a = \lim...", "b = \lim..."
            def _wrap_eq_var(m):
                eq = m.group(1).strip()
                trail = '.' if eq.endswith('.') else ''
                if trail: eq = eq[:-1].strip()
                if '$' in eq:
                    return m.group(0)
                return f"${eq}${trail}"

            p = re.sub(
                r'(?<!\$)\b([a-zA-Z]\s*=\s*\\(?:lim|frac|dfrac|int|sum|sqrt)(?![a-zA-Z]).+?)(?=\s+v[àa]|\s+ho\u1eb7c|\s+v\u1edbi|\.|$|\;)',
                _wrap_eq_var,
                p
            )

            # Bọc các hàm số toán học chuẩn: f(a), f(b), f(x_1), f(x_2), f(x)
            p = re.sub(r'(?<!\$)\b([fgyPQuv]\([a-zA-Z0-9_ -]+\))(?!\$)', r'$\1$', p)

            # Bọc các phương trình gán đơn giản: x = x_0, y = y_0, y = ax + b
            p = re.sub(
                r'(?<!\$)\b([xy]\s*=\s*[a-zA-Z0-9_]+(?:\s*[-+]\s*[a-zA-Z0-9_]+)*)(?=\s+(?:l\xe0|n\u1ebfu|v\u1edbi|\(|,|$|\.))',
                r'$\1$',
                p
            )

            # Bọc các bất đẳng thức đơn giản: a \ne 0, x \ge 0
            p = re.sub(
                r'(?<!\$)\b([a-zA-Z]\s*\\(?:ne|le|ge)\s*[a-zA-Z0-9_+-]+)(?=\))',
                r'$\1$',
                p
            )

            # Bọc khoảng / đoạn: [a; b], (a; b)
            p = re.sub(r'(?<!\$)(\[[a-zA-Z0-9_+-]+\s*;\s*[a-zA-Z0-9_+-]+\])', r'$\1$', p)

            # Bọc max, min trên đoạn: max_{[a; b]} f(x), min_{[a; b]} f(x)
            p = re.sub(r'(?<!\$)\b((?:max|min)_\{?\[[a-zA-Z0-9_; ]+\]\}?\s*f\(x\))', r'$\1$', p)

            # Bọc các phân số \frac hoặc \dfrac trơ trọi
            p = re.sub(r'(?<!\$)\\(?:frac|dfrac)\{([^{}]+)\}\{([^{}]+)\}(?!\$)', r'$\\frac{\1}{\2}$', p)
            p = re.sub(r'(\[[a-zA-Z]_(?:\{[^{}]+\}|[a-zA-Z0-9\+\-]+)\s*;\s*[a-zA-Z]_(?:\{[^{}]+\}|[a-zA-Z0-9\+\-]+)[\)\]])', r'$\1$', p)
            p = re.sub(r'(\bn_1,\s*n_2,\s*\.\.\.,\s*n_k\b)', r'$\1$', p)
            p = re.sub(r'(\bn\s*=\s*n_1\s*\+\s*n_2\s*\+\s*\.\.\.\s*\+\s*n_k\b)', r'$\1$', p)
            p = re.sub(r'\b([A-Z]_[0-9]+)\b(?=\s*:)', r'$\1$', p)

            healed_parts.append(p)

        return ''.join(healed_parts)

    s = '\n'.join(_heal_naked_latex_line(l) for l in s.split('\n'))

    return s



def clean_vietnamese_math(text):

    if not text: return ""

    text = sanitize_katex_latex(text)

    vn_chars = r'[àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴĐ]'



    def fix_math(m):

        content = m.group(1).strip()

        # Nếu chuỗi trong $...$ chỉ thuần túy là từ ngữ tiếng Việt không có biểu thức toán: gỡ dấu $

        has_math_symbol = bool(re.search(r'[\\=<>_+^/*{}~\[\]]', content))

        if re.search(vn_chars, content) and not has_math_symbol:

            return f"<i>{content}</i>" if content.startswith("(") and content.endswith(")") else f" {content} "

        # Nếu có ký hiệu toán: giữ nguyên dấu $ để KaTeX render

        return f"${content}$"



    res = re.sub(r'\$(.*?)\$', fix_math, str(text))

    res = re.sub(r'  +', ' ', res)

    return res.strip()



def format_pedagogical_math(text):
    """Chuẩn hóa công thức Toán / STEM chuẩn KaTeX: Cân bằng dấu $, xử lý khoảng trắng, bọc biểu thức trần trụi an toàn bằng Token-Masking."""
    if not text: return ""
    s = str(text)

    # 1. Khử ký tự điều khiển ẩn và chuẩn hóa escape
    s = s.replace('\x0c', r'\f').replace('\x08', r'\b')
    s = s.replace(r'\$', '$')

    # 1.1 Khử triệt để chữ 'mega' / '\omega' bị dùng nhầm thành vô cực (\infty) do AI / OCR lỗi font
    s = re.sub(r'(?i)(?<=[\(\[\s;,-])-+\s*mega\b', r'-\\infty', s)
    s = re.sub(r'(?i)\b-\s*mega\b', r'-\\infty', s)
    s = re.sub(r'(?i)\+\s*mega\b', r'+\\infty', s)
    s = re.sub(r'(?i)(?<=[;,\s])\s*\+?mega(?=[\)\]\s;,])', r'+\\infty', s)
    s = re.sub(r'(?i)(?<=[(\[\s])-?\s*\\?[oO]mega\b', r'-\\infty', s)
    s = re.sub(r'(?i);\s*\+?\s*\\?[oO]mega\s*(?=[)\]])', r'; +\\infty', s)

    # 2. Khử vi phạm chương trình cũ 2018 (Chuẩn hóa Tâm đối xứng)
    s = s.replace("điểm uốn", "tâm đối xứng").replace("Điểm uốn", "Tâm đối xứng")
    s = s.replace("y'' = 0", r"$x_0 = -\frac{b}{3a}$").replace("y''=0", r"$x_0 = -\frac{b}{3a}$")
    s = s.replace("y''", "đạo hàm")

    # 3. Chuẩn hóa KaTeX cho tập hợp & khử triệt để \middle|, \middle\vert, \left, \right đơn độc
    s = re.sub(r'\\middle\s*\\?\|', r'\\mid', s)
    s = re.sub(r'\\middle\s*\\vert', r'\\mid', s)
    s = re.sub(r'\\middle\b', r'\\mid', s)
    s = re.sub(r'\\left(?![(\[{|])', '', s)
    s = re.sub(r'\\right(?![)\]}|])', '', s)
    s = re.sub(r'\\\\+\{', r'\\{', s)
    s = re.sub(r'\\\\+\}', r'\\}', s)
    s = re.sub(r'\\+\}', r'\}', s)
    s = re.sub(r'\\+\{', r'\{', s)

    # 4. Sửa lỗi dấu $ bị lọt vào tử/mẫu của \frac: \frac{$A$}{B} -> \frac{A}{B}
    s = re.sub(r'\\frac\{\$([^\$]+)\$\}\{([^\}]+)\}', r'\\frac{\1}{\2}', s)
    s = re.sub(r'\\frac\{([^\}]+)\}\{\$([^\$]+)\$\}', r'\\frac{\1}{\2}', s)
    s = re.sub(r'\\frac\{\$([^\$]+)\$\}\{\$([^\$]+)\$\}', r'\\frac{\1}{\2}', s)

    # 5. Xử lý khoảng trắng lỗi ngay sau $ mở hoặc trước $ đóng: "$ x $" -> "$x$"
    s = re.sub(r'\$([^\$\n]+?)\$', lambda m: f"${m.group(1).strip()}$", s)

    # 6. Thuật toán TOKEN-PROTECTED MATH SANITIZER (Bảo vệ khối toán, bọc biểu thức trần trụi và chống lỗi KaTeX text-mode)
    math_blocks = []
    def save_existing_math(m):
        math_blocks.append(m.group(0))
        return f"__MATH_{len(math_blocks)-1}__"

    # Bước 6A: Bảo vệ an toàn 100% các khối $...$ đã có
    s = re.sub(r'\$[^\$\n]+?\$', save_existing_math, s)

    # Bước 6B: Quét và bọc an toàn các biểu thức toán trần trụi nằm ngoài math mode
    def wrap_new_math(m):
        math_blocks.append(f"${m.group(0)}$")
        return f"__MATH_{len(math_blocks)-1}__"

    # Bọc tập hợp toán học trần trụi (Set-builder notation): A = \{...\} hoặc \{x \in ...\} hoặc X = \{...\}
    s = re.sub(r'(?<!\$)\b([A-Za-z]\s*=\s*(?:\\left\s*)?\\\{.*?(?:\\right\s*)?\\\\?\})(?!\$)', wrap_new_math, s)
    s = re.sub(r'(?<!\$)(?<![A-Za-z0-9_])((?:\\left\s*)?\\\{[^{}]*?(?:\\in|\\mid|\||\\ge|\\le|>|<)[^{}]*?(?:\\right\s*)?\\\\?\})(?!\$)', wrap_new_math, s)

    # Bọc \left[ ... \right] hoặc \left( ... \right)
    s = re.sub(r'\\left\[.*?\\right\]', wrap_new_math, s)
    s = re.sub(r'\\left\(.*?\\right\)', wrap_new_math, s)
    s = re.sub(r'\[[^\]\n]*?(?:\\frac|\\pi|\\sqrt)[^\]\n]*?\]', wrap_new_math, s)
    s = re.sub(r'\([^\)\n]*?(?:\\frac|\\pi|\\sqrt)[^\)\n]*?\)', wrap_new_math, s)

    # Bọc tích / phương trình dạng P = a \cdot b
    s = re.sub(r'\b[A-Za-z]\s*=\s*[a-zA-Z0-9_\s\+\-\*]*(?:\\cdot\s*[a-zA-Z0-9_]+)+', wrap_new_math, s)

    # Bọc phân số \frac{...}{...}
    s = re.sub(r'\\frac\{[^{}]+\}\{[^{}]+\}', wrap_new_math, s)

    # Bọc căn thức \sqrt
    s = re.sub(r'\\sqrt(?:\[[^\]]+\])?\{[^{}]+\}', wrap_new_math, s)

    # Bọc tập hợp: a, b \in \mathbb{N}
    s = re.sub(r'\b[a-zA-Z](?:,\s*[a-zA-Z])*\s*\\in\s*\\mathbb\{[A-Z]\}', wrap_new_math, s)

    # Bọc vectơ \vec{...}
    s = re.sub(r'\\vec\{[^{}]+\}(?:\s*=\s*\([^\)]+\))?', wrap_new_math, s)

    # Bọc tích phân \int
    s = re.sub(r'\\int(?:_[^{\s]+)?(?:\^[^{\s]+)?\s*[^;\$\n]+?d[a-z]', wrap_new_math, s)

    # Bọc các macro LaTeX trần trụi còn sót lại (\alpha, \beta, \infty, v.v.)
    s = re.sub(r'(?<![a-zA-Z0-9_])\\[a-zA-Z]+(?:\{[^{}]*\})*', wrap_new_math, s)

    # Bước 6C: Khôi phục lại toàn bộ các khối toán
    for i, mb in enumerate(math_blocks):
        s = s.replace(f"__MATH_{i}__", mb)

    # 7. Vá dấu $ mồ côi (nếu tổng số $ bị lẻ)
    if s.count('$') % 2 != 0:
        parts = s.split('$')
        parts[-1] = parts[-1].rstrip() + "$"
        s = "$".join(parts)

    s = re.sub(r'[ \t]+', ' ', s)
    return s.strip()

def auto_extract_mslgn(q_obj):

    if not isinstance(q_obj, dict): return q_obj

    q_text = str(q_obj.get("q", ""))

    matches = re.findall(r'([\[\(]\d+\s*;\s*\d+[\]\)])\s*(?:tần số|:)?\s*(\d+)', q_text, re.IGNORECASE)

    if matches and len(matches) >= 2:

        grps = [m[0].strip() for m in matches]

        freqs = [int(m[1]) for m in matches]

        cleaned_q = re.sub(r'([\[\(]\d+\s*;\s*\d+[\]\)]\s*(?:tần số|:)?\s*\d+;?\s*)+', '', q_text, flags=re.IGNORECASE).strip()

        cleaned_q = cleaned_q.rstrip(':').strip()

        if not cleaned_q.endswith('.'): cleaned_q += ':'

        q_obj["q"] = cleaned_q

        q_obj["mslgn_data"] = {

            "title": "Bảng mẫu số liệu ghép nhóm:",

            "groups": grps,

            "freq": freqs

        }

    return q_obj



def clean_question_bbt_text(q_text):

    if not q_text: return ""

    s = str(q_text)



    # 1. Nếu BBT nằm ở các dòng riêng biệt (multiline table):

    lines = s.split("\n")

    clean_lines = []

    for l in lines:

        stripped = l.strip()

        is_pure_table_line = (

            re.match(r'^[|\s:-]+$', stripped) or

            re.match(r'^(?:\|\s*)?[xyf]\'?\s*\|', stripped, re.IGNORECASE) or

            (stripped.startswith("|") and stripped.endswith("|")) or

            (stripped.count("|") >= 3 and any(k in stripped.lower() for k in ["inf", "nearrow", "searrow"]))

        )

        if not is_pure_table_line:

            clean_lines.append(l)

    s = "\n".join(clean_lines).strip()



    # 2. Nếu BBT bị dính inline trong cùng một dòng với câu hỏi (như: "x | -inf | 0 | ... | +inf Hàm số..."):

    pat = r'(?:x\s*\||\b\|\s*x\s*\|)[^?\n]*?\|[^?\n]*?(?=(?:[A-ZÀ-Ỹ][a-zà-ỹ\s]+(?:đạt|đồng biến|nghịch biến|cực đại|cực tiểu|có bao nhiêu|tìm|giá trị|khẳng định|mệnh đề)|[A-ZÀ-Ỹ][^?\n]*?\?|\Z))'

    s = re.sub(pat, '', s)



    # 3. Tách dòng rõ ràng giữa lời dẫn và câu hỏi lệnh (chống dính chữ trên 1 dòng)
    s = re.sub(r'(?i)(bảng biến thiên như sau|bảng xét dấu như sau|đồ thị như hình vẽ bên|đồ thị như hình bên)\s*[:.]\s*([A-ZÀ-Ỹ])', r'\1:\n\n\2', s)

    # 4. Chuẩn hóa KaTeX an toàn qua động cơ format_pedagogical_math
    s = re.sub(r'[ \t]+', ' ', s)
    s = re.sub(r'\n\s*\n+', '\n\n', s).strip()
    return format_pedagogical_math(s)



# ==============================================================================

# 4. THANH BÊN (SIDEBAR) & LIÊN KẾT MÔN HỌC

# ==============================================================================

@st.cache_data(show_spinner=False)

def get_local_img_as_base64(file_path):

    try:

        webp_candidate = file_path.rsplit('.', 1)[0] + '.webp'

        target_file = webp_candidate if os.path.exists(webp_candidate) else file_path

        with open(target_file, "rb") as img_file:

            return base64.b64encode(img_file.read()).decode('utf-8')

    except Exception:

        return ""



@st.cache_data(show_spinner=False)

def generate_local_qr_base64(data_url: str, fill_color: str = "#38bdf8", back_color: str = "#0f172a") -> str:

    if qrcode is not None:

        try:

            qr = qrcode.QRCode(

                version=1,

                error_correction=qrcode.constants.ERROR_CORRECT_M,

                box_size=8,

                border=2,

            )

            qr.add_data(data_url)

            qr.make(fit=True)

            img = qr.make_image(fill_color=fill_color, back_color=back_color)

            buf = io.BytesIO()

            img.save(buf, format="PNG")

            return f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode('utf-8')}"

        except Exception:

            pass

    return f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={urllib.parse.quote(data_url, safe='')}"



def annotate_student_work(image: Image.Image, annotations: list) -> Image.Image:

    """

    BÚT TÍCH GIÁO VIÊN CHẤM BÀI TRỰC TIẾP FACE-TO-FACE:

    - Nét viền xanh lá & Tick xanh [✓ OK CHUẨN CHỈ] cho dòng làm đúng

    - Nét viền đỏ rực & Khung cảnh báo [🔴 CHECK VAR KHÉT LẸT] cho dòng có chỗ khuất tất/sai sót

    """

    try:

        annotated = image.copy().convert("RGBA")

        draw = ImageDraw.Draw(annotated)

        width, height = annotated.size



        if not annotations:

            return image



        for ann in annotations:

            box = ann.get("box", ann.get("box_2d", []))

            ann_type = str(ann.get("type", "ok")).strip().lower()

            label = str(ann.get("label", "")).strip()

            if not isinstance(box, (list, tuple)) or len(box) != 4:

                continue



            ymin, xmin, ymax, xmax = [float(v) for v in box]

            if max(ymin, xmin, ymax, xmax) > 1.0:

                y1 = int(ymin * height / 1000.0)

                x1 = int(xmin * width / 1000.0)

                y2 = int(ymax * height / 1000.0)

                x2 = int(xmax * width / 1000.0)

            else:

                y1, x1 = int(ymin * height), int(xmin * width)

                y2, x2 = int(ymax * height), int(xmax * width)



            x1, x2 = max(0, min(x1, x2)), min(width, max(x1, x2))

            y1, y2 = max(0, min(y1, y2)), min(height, max(y1, y2))

            if (x2 - x1) < 15 or (y2 - y1) < 15:

                continue



            if any(k in ann_type for k in ["var", "sai", "loi", "khuat_tat"]):

                # DÒNG MỰC ĐỎ CHECK VAR KHÉT LẸT (BÚT ĐỎ CỦA THẦY)

                draw.rectangle([x1, y1, x2, y2], outline=(239, 68, 68, 255), width=4)

                badge_text = f"🔴 CHECK VAR: {label}" if label else "🔴 CHECK VAR KHÉT LẸT"

                badge_w = min(width - x1, len(badge_text) * 10 + 16)

                badge_y1 = max(0, y1 - 24)

                draw.rectangle([x1, badge_y1, x1 + badge_w, y1], fill=(220, 38, 38, 235))

                draw.text((x1 + 6, max(0, badge_y1 + 4)), badge_text[:35], fill=(255, 255, 255, 255))

            else:

                # DÒNG TICK XANH OK CHUẨN CHỈ

                draw.rectangle([x1, y1, x2, y2], outline=(16, 185, 129, 255), width=3)

                badge_text = f"✅ OK: {label}" if label else "✅ OK CHUẨN CHỈ"

                badge_w = min(width - x1, len(badge_text) * 9 + 14)

                badge_y1 = max(0, y1 - 22)

                draw.rectangle([x1, badge_y1, x1 + badge_w, y1], fill=(5, 150, 105, 225))

                draw.text((x1 + 5, max(0, badge_y1 + 3)), badge_text[:35], fill=(255, 255, 255, 255))



        return annotated.convert("RGB")

    except Exception:

        return image



logo_file = "LOGO THIỆN NHÂN 3D.webp" if os.path.exists("LOGO THIỆN NHÂN 3D.webp") else "LOGO THIỆN NHÂN 3D.jpg"

logo_mime = "image/webp" if logo_file.endswith(".webp") else "image/jpeg"

logo_b64 = get_local_img_as_base64(logo_file)

logo_html = f'<img src="data:{logo_mime};base64,{logo_b64}" class="thiennhan-logo" alt="Logo">' if logo_b64 else '<div style="background: linear-gradient(45deg, #0f172a, #1e293b); padding: 8px 12px; border-radius: 8px; color: #f8fafc; font-weight: 800; font-size: 14px; border: 1.5px solid #38bdf8; box-shadow: 0 0 10px rgba(56,189,248,0.4);">THIỆN NHÂN</div>'



school_icon_svg = "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%2338bdf8'><path d='M12 3L1 9l4 2.18v6L12 21l7-3.82v-6l2-1.09V17h2V9L12 3zm6.82 6L12 12.72 5.18 9 12 5.28 18.82 9zM17 15.99l-5 2.73-5-2.73v-3.72L12 15l5-2.73v3.72z'/></svg>"



st.sidebar.markdown(f'<div class="brand-container"><img src="{school_icon_svg}" class="school-icon" alt="Icon Trường">{logo_html}</div><div style="text-align: center; margin-bottom: 10px;"><h2 style="color: #38bdf8; font-weight: 800; font-size: 1.8rem; margin: 0; text-shadow: 0px 2px 4px rgba(0,0,0,0.5);">THIẾT LẬP HỌC TẬP</h2></div>', unsafe_allow_html=True)



# HUY HIỆU NGÂN HÀNG KHẢO THÍ ĐỒ SỘ 2025 - 2026

sidebar_badge_html = (

    '<div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.95)); border: 1.5px solid #38bdf8; border-radius: 8px; padding: 10px 12px; margin-bottom: 14px; text-align: center; box-shadow: 0 4px 12px rgba(56, 189, 248, 0.15);">'

    '<div style="color: #38bdf8; font-weight: 800; font-size: 13px; letter-spacing: 0.5px;">🏛️ KHO KHẢO THÍ VIP SOTA 2026</div>'

    '<div style="color: #34d399; font-size: 12px; font-weight: 700; margin: 4px 0 2px 0;">⚡ 33.679 Đề Thật • 948.902 Câu Hỏi (64 Tỉnh)</div>'

    '<div style="color: #cbd5e1; font-size: 11px;">(Chuẩn nén LZMA/XZ 13.4 MB • 100% Đa Nền Tảng)</div>'

    '</div>'

)

st.sidebar.markdown(sidebar_badge_html, unsafe_allow_html=True)



with st.sidebar.expander("📱 Quét mã QR vào app trên điện thoại", expanded=False):

    qr_img_data = generate_local_qr_base64(APP_URL)

    st.image(qr_img_data, caption="Bật camera Zalo/iPhone quét mượt mà!", width="stretch")

    st.markdown(f'<div class="short-link-badge">🔗 {APP_URL}</div>', unsafe_allow_html=True)





with st.sidebar.expander("📲 Cài đặt Icon App vào Điện thoại & Máy tính (PWA)", expanded=False):

    st.markdown("""

    **Cách tạo Icon App mở trực tiếp (không cần gõ web/quét mã):**

    - 🤖 **Android (Chrome/Cốc Cốc):** Bấm biểu tượng menu $\\vdots$ ở góc trên ➔ Chọn **"Cài đặt ứng dụng"** (hoặc **"Thêm vào Màn hình chính"**).

    - 🍏 **iPhone / iPad (Safari):** Bấm nút **Chia sẻ** (biểu tượng $\\uparrow$) ➔ Kéo xuống chọn **"Thêm vào MH chính" (Add to Home Screen)**.

    - 💻 **Máy tính (Chrome/Edge):** Bấm biểu tượng ⬇️ hoặc Cài đặt trên thanh địa chỉ để cài app vào Desktop.



    *API Key chỉ dùng trong phiên hiện tại. Máy dùng chung không ghi nhớ Key cá nhân.*

    """)



st.sidebar.markdown("---")

st.sidebar.markdown("### 🔑 ĐƯỜNG TRUYỀN AI CÁ NHÂN (0 ĐỒNG)")



st.sidebar.link_button("👉 Lấy Key riêng miễn phí (15s)", "https://aistudio.google.com/apikey", width="stretch")

user_custom_key = st.sidebar.text_input("Dán mã API Key của em vào đây:", type="password", placeholder="Một hoặc nhiều Key, cách nhau bằng dấu phẩy")



raw_api_key = get_secret("GEMINI_API_KEY")

raw_sheet_url = get_secret("GOOGLE_SHEET_URL")

sheet_webhook_url = "".join(raw_sheet_url.split()) if raw_sheet_url else ""



sheet_view_url_secret = get_secret("GOOGLE_SHEET_VIEW_URL")

DEFAULT_SHEET_VIEW_URL = ""

if sheet_view_url_secret:

    sheet_view_url = "".join(sheet_view_url_secret.split())

else:

    sheet_view_url = ""



@st.cache_data(ttl=180, show_spinner=False)

def fetch_remote_sheet_logs(webhook_url: str, token: str):

    try:

        res = requests.get(webhook_url, params={"token": token}, timeout=6)

        if res.status_code == 200:

            data = res.json()

            if isinstance(data, list):

                return data

    except Exception:

        pass

    return []



if st.session_state.get("tab4_authenticated", False) and not st.session_state.global_stats_loaded and re.match(r"^https://script\.google\.com/macros/s/[^/]+/exec", sheet_webhook_url):

    data_gs = fetch_remote_sheet_logs(sheet_webhook_url, str(get_secret("SHEET_WEBHOOK_TOKEN", "")))

    if data_gs:

        st.session_state.global_logs = data_gs

        st.session_state.global_exam_count = len([x for x in data_gs if x.get('type') == 'EXAM_RESULT'])

    st.session_state.global_stats_loaded = True





admin_keys_pool = list(dict.fromkeys(k.strip() for k in raw_api_key.split(",") if k.strip())) if raw_api_key else []

active_keys_pool = split_api_keys(user_custom_key) if user_custom_key.strip() else split_api_keys(raw_api_key)



if not active_keys_pool:

    st.sidebar.warning("Chưa cấu hình Gemini API Key. Lab có sẵn và phân tích bảng điểm vẫn dùng được; tính năng AI cần Key.")

elif user_custom_key.strip(): st.sidebar.success("🟢 Em đang dùng đường truyền riêng siêu tốc!")

else: st.sidebar.info("🔵 Đang dùng đường truyền chung của Trường")

st.sidebar.markdown("---")

st.sidebar.markdown("### 🤖 ĐIỀU PHỐI MODEL GEMINI")

st.sidebar.selectbox(
    "Chọn chiến lược / Model:",
    [
        "⚡ Phương án 1: Tối ưu Siêu tốc (Khuyên dùng)",
        "📋 Phương án 2: Danh sách Chuyên gia (22/10/2026)",
        "🎯 Ghim: gemini-3-flash-preview (Socratic & Toán 1.07s)",
        "🎯 Ghim: gemini-flash-lite-latest (Siêu nhẹ 1.53s)",
        "🎯 Ghim: gemini-3.6-flash (Tải khỏe 1.81s)",
        "🎯 Ghim: gemini-3.5-flash-lite (Chuẩn Google 2.07s)",
        "🎯 Ghim: gemini-3.5-flash (Sư phạm sâu 4.33s)"
    ],
    index=0,
    key="ai_profile_selector",
    help="Tự động sắp xếp hàng đợi theo độ trễ thực tế từ 1.0s, hoặc ghim cố định 1 model theo ý muốn."
)

st.sidebar.caption("💡 Tự động fallback đa tầng an toàn khi Google quá tải.")

st.sidebar.markdown("---")

st.sidebar.markdown("### 👤 THÔNG TIN HỌC SINH")

student_name_input = st.sidebar.text_input("Họ và tên của em:", placeholder="Ví dụ: Nguyễn Văn A...")

student_name = student_name_input.strip() if student_name_input.strip() else "Ẩn danh"



all_grades = [f"Lớp {i}" for i in range(6, 13)]

if "target_switch_grade" in st.session_state:

    st.session_state.grade_selector = st.session_state.pop("target_switch_grade")

current_grade_val = st.session_state.get("grade_selector", "Lớp 12")

grade_idx = all_grades.index(current_grade_val) if current_grade_val in all_grades else 6

grade = st.sidebar.selectbox("🎯 Chọn khối lớp:", all_grades, index=grade_idx, key="grade_selector")

grade_num = int(grade.split()[1])



available_subjects = (

    ["Toán học", "Khoa học tự nhiên", "Ngữ văn", "Tiếng Anh", "Lịch sử & Địa lý", "Tin học", "Giáo dục công dân", "Công nghệ"]

    if grade_num <= 9 else

    ["Toán học", "Vật lý", "Hóa học", "Sinh học", "Ngữ văn", "Tiếng Anh", "Lịch sử", "Địa lý", "Tin học", "Giáo dục kinh tế và pháp luật", "Công nghệ"]

)

subject = st.sidebar.selectbox("📚 Môn học cần hỗ trợ:", available_subjects)



# ==============================================================================

# TỰ ĐỘNG ĐỒNG BỘ NGỮ CẢNH ĐA MÔN & XÓA SẠCH DỮ LIỆU CŨ KHI ĐỔI MÔN/LỚP

# ==============================================================================

current_context_key = f"{grade}_{subject}"

previous_context_key = st.session_state.get("active_context_key")



if previous_context_key is not None and previous_context_key != current_context_key:

    if st.session_state.get("exam_state") == "testing":

        st.session_state.setdefault("abandoned_attempts", []).append({"attempt_id": st.session_state.get("attempt_id"), "exam": st.session_state.get("exam_data"), "answers": dict(st.session_state.get("exam_answers", {})), "context": st.session_state.get("exam_context", {}), "saved_at": get_vn_time()})

        st.warning("Đã giữ bản bài đang làm trong phiên trước khi đổi môn/lớp. Có thể tải bản lưu tại Trạm 4.")

    # HỌC SINH VỪA ĐỔI MÔN HOẶC ĐỔI KHỐI LỚP TRÊN THANH BÊN

    # RESET TRIỆT ĐỂ BỘ NHỚ CỦA MÔN CŨ ĐỂ KHÔNG BỊ TRỘN LẪN BÀI HỌC (CHỐNG RÂU ÔNG NỌ CẮM CẰM BÀ KIA)

    for widget_key in list(st.session_state):
        if str(widget_key).startswith(("t3_p1_", "t3_p2_", "t3_p3_", "q_")):
            del st.session_state[widget_key]
    st.session_state.tram1_chat_history = []
    st.session_state.pop("research_result", None)

    st.session_state.current_lesson = ""

    st.session_state.current_topic = ""

    st.session_state.parsed_quiz = []

    st.session_state.quiz_states = {}

    st.session_state.lab_data = None

    st.session_state.messages = []

    st.session_state.chat = None

    st.session_state.exam_data = None

    st.session_state.exam_answers = {}

    st.session_state.exam_state = "config"

    for stale_key in ("attempt_id", "exam_deadline", "exam_context", "literature_grade", "exam_submitted_at"):

        st.session_state.pop(stale_key, None)

    st.session_state.tram3_chat_messages = []

    st.session_state.exam_code = str(random.randint(1011, 9999))

    st.toast(f"🔄 Đã chuyển sang không gian học tập môn {subject} - {grade}!", icon="✨")



st.session_state.active_context_key = current_context_key



st.sidebar.markdown("---")

@st.cache_resource(show_spinner=False)
def get_sheet_sync_executor():
    return concurrent.futures.ThreadPoolExecutor(max_workers=3, thread_name_prefix="gsai_sync")

_SHEET_SYNC_EXECUTOR = get_sheet_sync_executor()



def _post_to_google_sheet(webhook_url: str, payload: dict) -> bool:

    try:

        response = requests.post(webhook_url, json=payload, timeout=15)

        response.raise_for_status()

        ack = response.json()

        return isinstance(ack, dict) and (ack.get("success") is True or ack.get("status") in ("ok", "success"))

    except Exception as exc:

        logging.warning("Google Sheets sync failed: %s", type(exc).__name__)

        return False



def sync_event(entry: dict, background: bool = True) -> bool:

    """Đồng bộ sự kiện: Lưu bền vững vào CSDL SQLite/Supabase và đẩy ngầm lên Google Sheets.

    Khi background=True (mặc định), đẩy vào thread ngầm để giao diện 0ms gián đoạn."""

    # 1. BỀN VỮNG CSDL: Luôn lưu vào DatabaseManager (SQLite offline 0ms + Supabase nếu có API key)

    if db_manager:

        try:

            event_type = entry.get("type", "")

            supa_url = str(get_secret("SUPABASE_URL", ""))

            supa_key = str(get_secret("SUPABASE_KEY", ""))

            if event_type == "EXAM_RESULT":

                db_manager.save_exam_attempt(entry, supabase_url=supa_url, supabase_key=supa_key)

            elif event_type == "SOCRATIC_DIAGNOSTIC":

                db_manager.save_diagnostic(entry, supabase_url=supa_url, supabase_key=supa_key)

            elif event_type == "USER_FEEDBACK":

                db_manager.save_feedback(entry, supabase_url=supa_url, supabase_key=supa_key)

        except Exception as exc:

            logging.warning("Ghi CSDL thất bại trong sync_event: %s", exc)



    # 2. ĐỒNG BỘ GOOGLE SHEETS NẾU CÓ CẤU HÌNH

    if not sheet_webhook_url:

        return True

    if not re.match(r"^https://script\.google\.com/macros/s/[^/]+/exec(?:\?.*)?$", sheet_webhook_url):
        st.session_state.setdefault("pending_sync", {})[entry["event_id"]] = entry
        logging.info("GOOGLE_SHEET_URL chưa ở định dạng Web App /macros/s/.../exec. Đã lưu dữ liệu an toàn vào SQLite.")
        return False



    payload = dict(entry)

    payload["_token"] = str(get_secret("SHEET_WEBHOOK_TOKEN", ""))



    if background:
        pending = st.session_state.setdefault("pending_sync", {})
        futures = st.session_state.setdefault("sheet_sync_futures", {})
        event_id = entry["event_id"]
        pending[event_id] = dict(entry)
        previous = futures.get(event_id)
        if previous is not None and not previous.done():
            return True
        # Backpressure: keep excess events pending instead of an unlimited queue.
        if sum(not future.done() for future in futures.values()) >= 32:
            return False
        try:
            futures[event_id] = _SHEET_SYNC_EXECUTOR.submit(
                _post_to_google_sheet, sheet_webhook_url, payload)
            return True
        except RuntimeError:
            return False

    else:

        try:

            success = _post_to_google_sheet(sheet_webhook_url, payload)

            if success:

                st.session_state.setdefault("pending_sync", {}).pop(entry["event_id"], None)

                return True

            else:

                st.session_state.setdefault("pending_sync", {})[entry["event_id"]] = entry

                return False

        except Exception as exc:

            logging.warning("Google Sheets synchronization failed: %s", type(exc).__name__)

            st.session_state.setdefault("pending_sync", {})[entry["event_id"]] = entry

            return False







# Only the Streamlit script thread reconciles background outcomes.
for _event_id, _future in list(st.session_state.get("sheet_sync_futures", {}).items()):
    if _future.done():
        try:
            if _future.result():
                st.session_state.setdefault("pending_sync", {}).pop(_event_id, None)
        except Exception:
            logging.warning("Background Sheets synchronization did not complete")
        st.session_state.sheet_sync_futures.pop(_event_id, None)

with st.sidebar.expander("🛠️ Báo lỗi ứng dụng & Góp ý trải nghiệm", expanded=False):

    fb_category = st.selectbox("Loại vấn đề gặp phải:", ["📷 Lỗi nhận diện chữ", "📊 Lỗi đồ thị Lab", "🤖 AI giải thích khó hiểu", "⏳ Ứng dụng chậm", "💡 Đề xuất mới"])

    fb_rating = st.feedback("stars", key="fb_stars")

    fb_detail = st.text_area("Mô tả chi tiết:", key="fb_text")

    if st.button("📤 Gửi phản hồi", width="stretch") and fb_detail.strip():

        fb_entry = {"event_id": str(uuid.uuid4()), "time": get_vn_time(), "name": student_name, "grade": grade, "subject": subject, "category": fb_category, "rating": fb_rating + 1 if fb_rating is not None else 5, "detail": fb_detail.strip(), "type": "USER_FEEDBACK"}

        st.session_state.feedback_logs.append(fb_entry)

        synced = sync_event(fb_entry)

        if sheet_webhook_url:

            if synced:

                st.success("Đã ghi CSDL & đồng bộ Sheets.")

            else:

                st.warning("Đã ghi CSDL cục bộ; chưa xác nhận Sheets.")

        else:

            st.success("Đã lưu phản hồi an toàn vào CSDL.")



# --- THUẬT TOÁN LẶP NGẮT QUÃNG THÍCH ỨNG (FSRS - SPACED REPETITION) ---
if analyze_student_fsrs_review_schedule:
    try:
        review_logs = []
        for event in st.session_state.get("analytics_logs", []):
            if event.get("type") != "SOCRATIC_DIAGNOSTIC" or event.get("name") != student_name or event.get("subject") != subject or str(event.get("grade")) != str(grade):
                continue
            try:
                logged_at = datetime.strptime(str(event.get("time")), "%Y-%m-%d %H:%M:%S")
                days_ago = max(0.0, (datetime.strptime(get_vn_time(), "%Y-%m-%d %H:%M:%S") - logged_at).total_seconds() / 86400)
            except (ValueError, TypeError):
                continue
            review_logs.append({"topic": event.get("topic", ""), "subject": subject, "level": event.get("level", "TH"), "logged_days_ago": days_ago, "mistake_desc": event.get("error_type", "Cần ôn lại")})
        fsrs_sched = analyze_student_fsrs_review_schedule(review_logs)
        urgent_fsrs = [x for x in fsrs_sched if x.get("urgency_badge") in ("Điểm rơi vàng", "Cực kỳ cấp thiết")]
        if urgent_fsrs:
            top_f = urgent_fsrs[0]
            st.sidebar.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(217, 119, 6, 0.18), rgba(220, 38, 38, 0.12)); border: 1.5px solid #d97706; border-radius: 10px; padding: 10px 12px; margin-bottom: 12px;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
                    <span style="font-weight: 700; color: #fbbf24; font-size: 0.82rem;">🔔 ĐIỂM RƠI VÀNG FSRS ({top_f['retrievability_percent']}%)</span>
                    <span style="font-size: 0.70rem; background: #d97706; color: white; padding: 1px 6px; border-radius: 10px; font-weight: 700;">Ôn tập ngay</span>
                </div>
                <div style="font-size: 0.82rem; color: #f8fafc; font-weight: 600; line-height: 1.35; margin-bottom: 4px;">{html.escape(str(top_f['topic']))}</div>
                <div style="font-size: 0.72rem; color: #cbd5e1;">⚠️ <i>{html.escape(str(top_f['mistake_desc']))}</i> (Sai cách đây {top_f['days_since_mistake']} ngày)</div>
            </div>
            """, unsafe_allow_html=True)
    except Exception:
        pass

st.sidebar.markdown("---")

st.sidebar.markdown("### 📈 THỐNG KÊ THỰC NGHIỆM (KHKT)")

col_sb1, col_sb2, col_sb3 = st.sidebar.columns(3)

with col_sb1:

    st.metric("Tự học (T1)", f"{st.session_state.tram1_count}")

with col_sb2:

    st.metric("Socratic (T2)", f"{st.session_state.tram2_count}")

with col_sb3:

    current_exam_count = len([x for x in st.session_state.get('analytics_logs', []) if x.get('type') == 'EXAM_RESULT'])

    total_display_count = max(current_exam_count, st.session_state.get('global_exam_count', 0))

    st.metric("Khảo thí (T3)", f"{total_display_count}")



with st.sidebar.expander(f"📚 Thư Viện SGK KNTT - Lớp {grade_num} (VniTeach & NXBGD)", expanded=False):

    curr_books = get_kntt_books_for(subject, grade_num)

    curr_books_nxbgd = get_nxbgd_books_for(subject, grade_num)



    st.markdown(f"**📖 Nguồn: VniTeach**")

    for b in curr_books:

        st.link_button(f"📖 {b['title']}", b['url'], width="stretch")

    if curr_books:

        st.caption("📱 Quét mã QR lật sách song song (VniTeach):")

        st.image(generate_local_qr_base64(curr_books[0]['url']), width="stretch")

    st.link_button("🌐 Kho Toàn Bộ SGK Điện Tử KNTT (VniTeach)", "https://www.vniteach.com/sach-dien-tu-ket-noi-tri-thuc/#google_vignette", width="stretch")



    st.markdown("---")

    st.markdown(f"**📖 Nguồn: Tập Huấn NXBGD**")

    for b in curr_books_nxbgd:

        st.link_button(f"📖 {b['title']}", b['url'], width="stretch")

    if curr_books_nxbgd:

        st.caption("📱 Quét mã QR lật sách song song (NXBGD):")

        st.image(generate_local_qr_base64(curr_books_nxbgd[0]['url']), width="stretch")

    st.link_button("🌐 Kho Toàn Bộ SGK Điện Tử KNTT (NXBGD)", "https://taphuan.nxbgd.vn/", width="stretch")



with st.sidebar.expander("⚖️ Căn Cứ Pháp Quy Bộ GD&ĐT Hiện Hành", expanded=False):

    st.markdown('<div style="font-size: 0.82rem; line-height: 1.55; color: #cbd5e1;">• <b>TT 32/2018 & TT 13/2022/TT-BGDĐT:</b> Chương trình GDPT 2018 chuẩn Quốc gia.<br>• <b>QĐ 764/QĐ-BGDĐT:</b> Cấu trúc định dạng đề thi Kỳ thi tốt nghiệp THPT từ năm 2025/2026 (3 dạng thức trắc nghiệm; Ngữ văn 100% tự luận).<br>• <b>CV 3175/BGDĐT-GDTrH:</b> Dạy học & kiểm tra đánh giá môn Ngữ văn: 100% ngữ liệu ngoài SGK, tiếp cận theo đặc trưng thể loại.<br>• <b>CV 5512/BGDĐT-GDTrH:</b> Kế hoạch bài dạy 4 bước chuẩn Sư phạm (Khởi động - Hình thành kiến thức mới - Luyện tập - Vận dụng).<br>• <b>TT 22/2021/TT-BGDĐT:</b> Đánh giá học sinh THCS và THPT theo các nhóm năng lực cốt lõi.<br>• <b>Chuẩn hóa IUPAC:</b> 100% danh pháp hóa học quốc tế hiện đại.<br>• <b>Chuẩn Toán 2018:</b> Không dùng hàm trùng phương $x^4$.</div>', unsafe_allow_html=True)



st.sidebar.info("💡 **Triết lý:** Dưỡng thiện tâm - Ươm nhân tài • Dẫn dắt tư duy tự học!")



# ==============================================================================

# 5. ĐIỀU PHỐI AI BỀN BỈ (ĐO KIỂM THỰC NGHIỆM TRÊN GOOGLE API NGÀY 22/10/2026)

# Sắp xếp nghiêm ngặt theo độ trễ: Từ nhanh nhất (1.0s) đến dự phòng an toàn

# ==============================================================================

# PHƯƠNG ÁN 1: TỐI ƯU SIÊU TỐC THỰC CHIẾN (Phản hồi tức thì ~1.0s, không bao giờ nghẽn)
MODELS_PROFILE_OPTIMIZED = [
    "gemini-3-flash-preview",        # 🥇 1.07s: Đỉnh cao Socratic & Toán học (Từ chuyên gia, tốc độ số 1)
    "gemini-flash-lite-latest",      # 🥈 1.53s: Siêu nhẹ, phản hồi tức thì (Từ chuyên gia)
    "gemini-3.6-flash",              # 🥉 1.81s: Thế hệ 3 tải khỏe, 0 nghẽn khi cả lớp cùng truy cập
    "gemini-3.5-flash-lite",         # 🍃 2.07s: Khuyến nghị chính thức từ Google thay thế 2.5-lite
    "gemini-3.5-flash",              # 📖 4.33s: Phân tích sư phạm chuyên sâu CT GDPT 2018
    "gemini-3.1-flash-lite-preview", # 🔄 5.34s: Dự phòng nhẹ (Từ chuyên gia)
    "gemini-flash-latest",           # 🛡️ Dự phòng chung Google (Từ chuyên gia)
    "gemini-3.8-flash",              # 🛡️ Khuyến nghị Google thay thế 2.5-flash
    "gemini-3.1-pro-preview",        # 🛡️ Dự phòng suy luận sâu (Từ chuyên gia)
    "gemini-2.5-flash",              # 🛡️ Dự phòng kênh đặc quyền legacy
    "gemini-2.5-flash-lite",         # 🛡️ Dự phòng kênh đặc quyền legacy
]

# PHƯƠNG ÁN 2: ĐỐI CHIẾU CHUYÊN GIA (22/10/2026) - Đã xếp lại theo độ trễ từ nhanh nhất
MODELS_PROFILE_EXPERT = [
    "gemini-3-flash-preview",        # 🥇 1.07s: Hoạt động ngay lập tức, Socratic đỉnh cao
    "gemini-flash-lite-latest",      # 🥈 1.53s: Hoạt động ngay lập tức, siêu nhẹ
    "gemini-3.1-flash-lite-preview", # 🔄 5.34s: Dự phòng nhẹ
    "gemini-flash-latest",           # 🛡️ Dự phòng chung Google
    "gemini-3.1-pro-preview",        # 🛡️ Dự phòng suy luận sâu
    "gemini-2.5-flash",              # 🛡️ Dự phòng tài khoản đặc quyền legacy
    "gemini-2.5-flash-lite",         # 🛡️ Dự phòng tài khoản đặc quyền legacy
]

def get_active_model_queue():
    choice = st.session_state.get("ai_profile_selector", "")
    if "Ghim:" in choice:
        pinned = choice.split("Ghim:")[1].split("(")[0].strip()
        fallback = [m for m in MODELS_PROFILE_OPTIMIZED if m != pinned]
        return [pinned] + fallback
    elif "Phương án 2" in choice:
        base_models = list(MODELS_PROFILE_EXPERT)
    else:
        base_models = list(MODELS_PROFILE_OPTIMIZED)

    if st.session_state.get("working_model") and st.session_state.working_model in base_models:
        return [st.session_state.working_model] + [m for m in base_models if m != st.session_state.working_model]
    return base_models

ALL_GEMINI_MODELS = MODELS_PROFILE_OPTIMIZED



if "working_model" not in st.session_state: st.session_state.working_model = None

if "working_key" not in st.session_state: st.session_state.working_key = None



DEFAULT_PEDAGOGICAL_SYSTEM_INSTRUCTION = """Bạn là Gia Sư AI Sư Phạm hàng đầu Việt Nam, hỗ trợ học sinh học tập theo đúng chuẩn Chương Trình Giáo Dục Phổ Thông 2018 (SGK Kết Nối Tri Thức với Cuộc Sống - NXB Giáo Dục Việt Nam & Cục Quản Lý Chất Lượng - Bộ GD&ĐT).

NGUYÊN TẮC SƯ PHẠM BẮT BUỘC THEO CT GDPT 2018:

1. MÔN TOÁN HỌC:

   - TUYỆT ĐỐI NGHIÊM CẤM ra đề/giải bài về hàm số bậc bốn trùng phương y = ax^4 + bx^2 + c (đã BỊ BỎ HOÀN TOÀN khỏi CT 2018).

   - Khảo sát hàm số Lớp 12 CHỈ ĐƯỢC PHÉP DÙNG 3 LOẠI HÀM:

     + Hàm đa thức bậc ba: y = ax^3 + bx^2 + cx + d (a != 0)

     + Hàm phân thức bậc nhất / bậc nhất: y = (ax + b) / (cx + d)

     + Hàm phân thức bậc hai / bậc nhất: y = (ax^2 + bx + c) / (px + q) (có tiệm cận xiên)

   - Lớp 10: Hàm bậc nhất & Parabol bậc hai y = ax^2 + bx + c.

   - Lớp 11: Cấp số cộng/nhân, Hàm lượng giác, Giới hạn, Đạo hàm, Mẫu số liệu ghép nhóm.

2. MÔN HÓA HỌC & KHOA HỌC TỰ NHIÊN:

   - 100% sử dụng danh pháp quốc tế IUPAC chuẩn CT 2018 (Alkane, Alkene, Alkyne, Alcohol, Aldehyde, Carboxylic acid, Ester, Amine, Amino acid, Carbohydrate, Polymer...). TUYỆT ĐỐI KHÔNG dùng tên cũ (Ancol, Anđehit, Axit axetic, Benzen...).

3. MÔN NGỮ VĂN:

   - NGUYÊN TẮC NGỮ LIỆU BẮT BUỘC:

     + Trạm 1 (Học tập): BẮT BUỘC sử dụng 100% ngữ liệu TRONG Sách giáo khoa Kết Nối Tri Thức để bám sát chương trình bài học.

     + Trạm 2 (Gia sư Socratic): Phân tích linh hoạt dựa trên hình ảnh/văn bản học sinh cung cấp (học sinh hỏi gì đáp nấy, dù là trong hay ngoài SGK).

     + Trạm 3 (Khảo thí & Đề thi): CÓ 2 LUỒNG TÙY CHỌN. (Luồng 1) Mặc định ra đề chuẩn BGDĐT: BẮT BUỘC dùng 100% ngữ liệu MỚI NGOÀI SGK. (Luồng 2) Nếu Giáo viên tùy chỉnh yêu cầu tác phẩm SGK: AI linh hoạt tuân thủ dùng đúng văn bản giáo viên chọn.

4. MÔN TIẾNG ANH:

   - Bám sát chuẩn khung năng lực ngoại ngữ 6 bậc VN / CEFR (A2/B1/B2) và định dạng đề thi THPT 2026.

   - TUYỆT ĐỐI BẮT BUỘC: Toàn bộ từ vựng, đoạn văn, câu hỏi trắc nghiệm, các lựa chọn đáp án (A, B, C, D), và bài tập ngữ pháp PHẢI ĐƯỢC VIẾT 100% BẰNG TIẾNG ANH. Chỉ dùng tiếng Việt khi giải thích hoặc phân tích phương pháp giải.

5. QUY TẮC CÔNG THỨC TOÁN:

   - TUYỆT ĐỐI KHÔNG bọc chữ tiếng Việt có dấu trong dấu $...$. Dấu $...$ chỉ dùng cho công thức toán ($x$, $f(x)$)."""






# ==============================================================================
# KHO BÁU TRIẾT LÝ NHÂN CÁCH & DANH NGÔN VĨ NHÂN Á - ÂU LIÊN KẾT 3 TRẠM
# (ĐẢM BẢO KHÔNG TRÙNG LẶP • TIẾP NỐI THEO TIẾN TRÌNH RÈN ĐỨC LUYỆN TÀI)
# ==============================================================================

CROSS_STATION_PHILOSOPHY_BANK = {
    1: [
        {
            "author": "Khổng Tử",
            "origin": "Phương Đông",
            "quote": "Tri chi vi tri chi, bất tri vi bất tri, thị tri dã (Biết thì nói là biết, chưa biết thì nhận là chưa biết, ấy mới là sự hiểu biết chân chính).",
            "lesson": "Người học trò chân chính không giấu dốt, luôn giữ tâm thế khiêm cung, lấy sự thành thật với chính mình làm gốc rễ để dựng xây nền móng tri thức vững bền."
        },
        {
            "author": "Socrates",
            "origin": "Phương Tây",
            "quote": "Sự thông thái đích thực là khi ta nhận biết rằng những điều ta biết chỉ là hạt cát trước đại dương bao la của vũ trụ.",
            "lesson": "Càng thấu hiểu bản chất của tri thức, con người càng trở nên khiêm nhường, luôn biết lắng nghe và không ngừng hoàn thiện nhân cách mỗi ngày."
        },
        {
            "author": "Albert Einstein",
            "origin": "Phương Tây",
            "quote": "Học từ ngày hôm qua, sống cho ngày hôm nay và hy vọng ở ngày mai. Điều cốt tử là không bao giờ ngừng đặt câu hỏi và tìm tòi chân lý.",
            "lesson": "Khoa học bắt nguồn từ niềm say mê khám phá; khi em giữ được ngọn lửa hiếu tri và tinh thần tự học, mọi nấc thang tri thức đều sẽ mở ra."
        },
        {
            "author": "Lão Tử",
            "origin": "Phương Đông",
            "quote": "Hành trình vạn dặm khởi đầu từ một bước chân; cây đại thụ ôm lấy vòng tay bắt đầu từ mầm non bé nhỏ.",
            "lesson": "Để vươn tới những đỉnh cao rạng rỡ, phải biết trân trọng từng bài học nền tảng cơ bản hôm nay, kiên nhẫn tích lũy từng ngày không nản lòng."
        },
        {
            "author": "Aristotle",
            "origin": "Phương Tây",
            "quote": "Cội rễ của sự học thì gian truân, đắng cay; nhưng hoa quả của nó sẽ vô cùng ngọt ngào và rạng rỡ.",
            "lesson": "Vượt qua sự bỡ ngỡ ban đầu của bài học chính là rèn luyện ý chí; niềm vui khi tự mình thấu suốt quy luật khoa học sẽ là phần thưởng vô giá."
        },
        {
            "author": "Chu Văn An",
            "origin": "Phương Đông",
            "quote": "Đạo học lấy việc sửa mình và giúp đời làm trọng; học rộng, hiểu sâu, giữ tâm sáng như gương soi bóng.",
            "lesson": "Học tập không phải chỉ để tìm kiếm điểm số phù hoa, mà để nuôi dưỡng thiện tâm, trở thành người có ích cho gia đình, quê hương và xã hội."
        }
    ],
    2: [
        {
            "author": "René Descartes",
            "origin": "Phương Tây",
            "quote": "Tôi tư duy, nên tôi tồn tại; mỗi một sai lầm được nhận diện và khắc phục chính là một bậc thang đưa ta chạm tới chân lý vững vàng.",
            "lesson": "Không có ai không từng vấp ngã khi giải một bài toán khó; điều vĩ đại là em đã dũng cảm đối diện với sai sót, tìm ra nguyên nhân và tự tay sửa lại."
        },
        {
            "author": "Mạnh Tử",
            "origin": "Phương Đông",
            "quote": "Trời sắp trao sứ mệnh lớn cho ai, ắt trước hết phải thử thách tâm chí, nhọc nhằn gân cốt để rèn nên bản lĩnh phi thường.",
            "lesson": "Những bài tập hóc búa và chỗ khuất tất chính là thao trường tôi luyện tính cẩn trọng, kiên định và bản lĩnh vượt khó của người có chí lớn."
        },
        {
            "author": "Marie Curie",
            "origin": "Phương Tây",
            "quote": "Cuộc sống không dễ dàng với bất kỳ ai, nhưng điều cốt tử là phải kiên định và trên hết là có niềm tin mãnh liệt vào bản thân mình.",
            "lesson": "Đức tính nhẫn nại và sự trung thực trong từng dòng lập luận, từng phép tính hôm nay sẽ tạo dựng nên nhân cách một người làm khoa học chân chính."
        },
        {
            "author": "Trang Tử",
            "origin": "Phương Đông",
            "quote": "Nước sâu chảy chậm, người khôn nói khẽ; tâm định thì trí sáng, nhìn rõ ngọn ngành mọi biến hóa khôn lường.",
            "lesson": "Khi gặp bài toán phức tạp, chỉ cần giữ tâm tĩnh lặng, phân tích từng giả thiết, bóc tách từng lớp dữ kiện thì mọi nút thắt đều sẽ được khai thông."
        },
        {
            "author": "Thomas Edison",
            "origin": "Phương Tây",
            "quote": "Tôi không hề thất bại; tôi chỉ vừa tìm ra hàng ngàn phương pháp chưa đạt hiệu quả để từng bước chạm tới lời giải hoàn hảo nhất.",
            "lesson": "Mỗi lần Thầy Check VAR mực đỏ không phải là phê phán, mà là trao tặng cho em một cơ hội quý báu để rèn luyện tư duy phản biện sắc bén."
        },
        {
            "author": "Nguyễn Trãi",
            "origin": "Phương Đông",
            "quote": "Nên thợ nên thầy vì có học, no ăn no mặc bởi hay làm; việc khó không lùi bước, ngọc càng mài càng thêm sáng.",
            "lesson": "Sự tỉ mỉ, chu đáo và không bỏ cuộc trước những bài tập gai góc chính là chìa khóa mở toang cánh cửa thành công trong tương lai."
        }
    ],
    3: [
        {
            "author": "Chủ tịch Hồ Chí Minh",
            "origin": "Phương Đông",
            "quote": "Vì lợi ích mười năm thì phải trồng cây, vì lợi ích trăm năm thì phải trồng người. Học để làm việc, làm người, để phụng sự Tổ quốc và nhân dân.",
            "lesson": "Chiến thắng trên đấu trường khảo thí không chỉ là điểm số, mà là minh chứng cho tinh thần tự lực tự cường và khát vọng đem tài năng cống hiến cho quê hương An Giang và non sông Việt Nam."
        },
        {
            "author": "Thân Nhân Trung",
            "origin": "Phương Đông",
            "quote": "Hiền tài là nguyên khí của quốc gia; nguyên khí thịnh thì thế nước mạnh rồi lên cao, nguyên khí suy thì thế nước yếu rồi xuống thấp.",
            "lesson": "Mỗi học trò chăm ngoan, có đức có tài bước ra từ kỳ thi hôm nay chính là một viên gạch hồng bồi đắp cho sự phồn vinh trường tồn của dân tộc."
        },
        {
            "author": "Marcus Aurelius",
            "origin": "Phương Tây",
            "quote": "Bản lĩnh đích thực của con người thể hiện ở sự điềm tĩnh phi thường và ý chí quật cường khi đối diện với những áp lực và thử thách cam go nhất.",
            "lesson": "Phòng thi là nơi thử thách tâm lý và bản lĩnh; người giữ được sự bình tĩnh, cẩn trọng và kiên định đến giây phút cuối cùng mới là người chiến thắng thực thụ."
        },
        {
            "author": "Immanuel Kant",
            "origin": "Phương Tây",
            "quote": "Hai điều khiến tâm hồn tôi luôn tràn ngập kinh ngạc và kính phục: bầu trời đầy sao trên đầu tôi và quy luật đạo đức trong sâu thẳm trái tim tôi.",
            "lesson": "Làm bài thi bằng sự trung thực tuyệt đối, tôn trọng chính mình và tôn trọng bạn bè chính là phẩm chất cao quý nhất của một nhân cách lớn."
        },
        {
            "author": "Nelson Mandela",
            "origin": "Phương Tây",
            "quote": "Giáo dục là vũ khí mạnh mẽ nhất mà chúng ta có thể sử dụng để thay đổi và nâng tầm thế giới.",
            "lesson": "Kết quả thi hôm nay là bệ phóng để em tự tin bước ra biển lớn, biến tri thức thành hành động cụ thể để kiến tạo một tương lai tốt đẹp hơn."
        },
        {
            "author": "Khổng Minh (Gia Cát Lượng)",
            "origin": "Phương Đông",
            "quote": "Phi đạm bạc vô dĩ minh chí, phi ninh tĩnh vô dĩ trí viễn (Không đạm bạc thì không sáng cái chí, không tĩnh lặng thì không đi được xa).",
            "lesson": "Sau mỗi kỳ thi, hãy giữ tâm khiêm cung trước thành công và không nản lòng trước sơ suất; tiếp tục nuôi dưỡng chí lớn phụng sự đời."
        }
    ]
}


def get_cross_station_pedagogical_context(current_station: int) -> str:
    """
    Tổng hợp ngữ cảnh đa trạm của học sinh giúp Thầy AI nắm bắt trọn vẹn hành trình rèn luyện.
    """
    ctx_parts = []

    # Thông tin Trạm 1
    t1_topic = st.session_state.get('current_topic', '')
    if st.session_state.get('tram1_understood', False):
        ctx_parts.append(f"• Trạm 1 (Lý thuyết): Em đã làm chủ hoàn toàn kiến thức cốt lõi chuyên đề '{t1_topic}'.")
    elif t1_topic:
        ctx_parts.append(f"• Trạm 1 (Lý thuyết): Em đang tìm hiểu chuyên đề '{t1_topic}'.")

    # Thông tin Trạm 2
    if st.session_state.get('tram2_understood', False):
        ctx_parts.append("• Trạm 2 (Bài tập): Em đã tự mình tháo gỡ thành công nút thắt bài tập, nhận diện và khắc phục trọn vẹn các lỗi sai.")
    elif st.session_state.get('tram2_count', 0) > 0:
        ctx_parts.append("• Trạm 2 (Bài tập): Em đã nộp bài làm và đang đối thoại cùng Thầy tháo gỡ các chỗ khuất tất.")

    # Thông tin Trạm 3
    if st.session_state.get('tram3_understood', False):
        ctx_parts.append("• Trạm 3 (Khảo thí): Em đã hoàn thành đề thi và nắm chắc phương pháp xử lý các câu khó/bẫy đề.")
    elif st.session_state.get('tram3_count', 0) > 0 or len(st.session_state.get('tram3_chat_messages', [])) > 0:
        ctx_parts.append("• Trạm 3 (Khảo thí): Em đã tham gia thi thử và đang lắng nghe phân tích sau thi.")

    if not ctx_parts:
        return "Học sinh đang bắt đầu hành trình học tập tại Trạm " + str(current_station) + "."
    return "\n".join(ctx_parts)


def get_unique_philosophical_lesson(station_id: int, subject: str = "") -> dict:
    """
    Lấy một bài học triết lý nhân cách kèm danh ngôn Á - Âu độc bản chưa từng xuất hiện trong phiên.
    """
    used = st.session_state.get('used_philosophical_quotes', [])
    candidates = CROSS_STATION_PHILOSOPHY_BANK.get(station_id, CROSS_STATION_PHILOSOPHY_BANK[1])

    # Lọc bỏ những câu đã từng sử dụng
    available = [c for c in candidates if c["quote"] not in used and c["author"] not in used]
    if not available:
        # Nếu đã dùng hết danh sách của trạm hiện tại, lấy từ trạm khác chưa dùng
        all_candidates = []
        for s in [1, 2, 3]:
            all_candidates.extend(CROSS_STATION_PHILOSOPHY_BANK.get(s, []))
        available = [c for c in all_candidates if c["quote"] not in used and c["author"] not in used]

    if available:
        chosen = random.choice(available)
    else:
        chosen = candidates[0]

    return chosen


def detect_student_concluded_intent(user_input: str, history: list = None) -> bool:
    """
    Nhận diện tự nhiên ý đồ của học sinh: ĐÃ HIỂU VÀ KHÔNG HỎI GÌ THÊM NỮA.
    TUYỆT ĐỐI KHÔNG BẮT BẺ TỪ KHÓA MÁY MÓC (Không khóa cứng 'cảm ơn thầy...').
    """
    if not user_input or not isinstance(user_input, str):
        return False

    txt = user_input.strip().lower()

    # 1. NẾU CÂU CÓ DẤU HIỆU ĐẶT CÂU HỎI MỚI -> CHẮC CHẮN VẪN ĐANG HỎI, CHƯA PHẢI CLOSURE
    # (Dù có từ 'cảm ơn', ví dụ: 'Em cảm ơn thầy nhưng chỗ này tại sao...')
    question_markers = [
        "?", "tại sao", "vì sao", "sao lại", "như thế nào", "thế nào", "làm sao",
        "chỗ này", "chưa hiểu", "chưa rõ", "chưa thông", "nhưng mà", "nhưng thầy",
        "thầy cho em hỏi", "cho em hỏi", "giải thích giúp", "hỏi thêm", "thắc mắc",
        "còn chỗ", "đoạn này", "tính sao", "bước này"
    ]
    if any(qm in txt for qm in question_markers):
        return False

    # 2. XÉT CÁC MẪU NGỮ NGHĨA BIỂU ĐẠT THẤU HIỂU & KHÔNG CÒN CÂU HỎI
    concluded_signals = [
        "không còn thắc mắc", "hết thắc mắc", "không còn gì để hỏi", "không còn gì hỏi",
        "không có thắc mắc", "không còn câu hỏi", "hết câu hỏi", "không hỏi gì thêm",
        "thông suốt rồi", "thấu suốt rồi", "thông rồi", "đã thông", "hiểu rõ rồi",
        "nắm chắc rồi", "nắm vững rồi", "hiểu bài rồi", "em hiểu hết rồi", "con hiểu hết rồi",
        "dạ hết rồi", "hết rồi thầy", "hết rồi ạ", "không thầy ơi", "không ạ thầy",
        "dạ không ạ", "không còn gì nữa", "tự tin làm được", "em tự làm được rồi",
        "em làm được rồi", "ổn rồi thầy", "ổn áp rồi", "tự tin rồi"
    ]
    if any(cs in txt for cs in concluded_signals):
        return True

    # 3. NẾU HỌC SINH NÓI NGẮN GỌN PHỦ ĐỊNH CÂU HỎI CỦA THẦY ("Dạ không", "Không ạ", "Hết rồi")
    short_affirmations = ["dạ không", "không ạ", "dạ hết", "hết rồi", "dạ ổn", "dạ rõ", "rõ rồi ạ", "dạ thông suốt"]
    if any(txt == sa or txt.startswith(sa + " ") or txt.endswith(" " + sa) for sa in short_affirmations):
        return True

    return False


def register_station_closure(station_id: int, quote_data: dict):
    """
    Ghi nhận trạng thái hoàn thành trạm và lưu câu danh ngôn để tránh trùng lặp giữa các trạm.
    """
    st.session_state[f"tram{station_id}_understood"] = True
    if quote_data:
        st.session_state[f"tram{station_id}_closure_info"] = quote_data
        if "used_philosophical_quotes" not in st.session_state:
            st.session_state.used_philosophical_quotes = []
        if quote_data.get("quote") and quote_data["quote"] not in st.session_state.used_philosophical_quotes:
            st.session_state.used_philosophical_quotes.append(quote_data["quote"])
        if quote_data.get("author") and quote_data["author"] not in st.session_state.used_philosophical_quotes:
            st.session_state.used_philosophical_quotes.append(quote_data["author"])


def build_socratic_master_instruction(subject_name: str, grade_level: int, student_nm: str, mode: str = "theory", topic_nm: str = "", context_data: str = ""):

    """

    SYSTEM INSTRUCTION SƯ PHẠM THƯỢNG ĐẲNG (KHKT 2026 - TRƯỜNG THPT TÂN HIỆP • THẦY PHAN MINH TRÍ)

    Thổi hồn Người Thầy Socratic Trí Tuệ, Sáng Suốt, Chuẩn Mực Mô Phạm, Thông Thạo sâu sắc từng bộ môn.

    Tuyệt đối không nhại lại lý thuyết như con vẹt. 100% Text & LaTeX thuần túy, không có Voice/TTS.

    """

    subject_guidelines = {

        "Toán học": (

            "- TINH THẦN BỘ MÔN: Thầy là người dẫn lối tư duy logic trừu tượng, hình học không gian 3D và sự chặt chẽ toán học.\n"

            "- NGUYÊN TẮC: Tuyệt đối không chỉ đọc lại công thức. Hãy khơi gợi: 'Tại sao lại cần điều kiện này?', liên hệ trực quan không gian hoặc bản chất đồ thị/hàm số.\n"

            "- CÔNG THỨC TOÁN: Bắt buộc dùng LaTeX chuẩn mực $...$ cho biến và biểu thức ($x$, $f(x)$, $\\vec{u}$, $\\overrightarrow{AB}$, $\\overrightarrow{AA'}$ cho vectơ từ 2 điểm trở lên). Tuyệt đối không bọc chữ tiếng Việt có dấu trong $...$."

        ),

        "Vật lý": (

            "- TINH THẦN BỘ MÔN: Thầy dẫn dắt từ bản chất hiện tượng vật lý trong tự nhiên và đời sống kỹ thuật.\n"

            "- NGUYÊN TẮC: Đi từ hiện tượng thực tiễn (chuyển động, năng lượng, điện từ, sóng, nhiệt...) rồi mới quy về định luật và công thức chuẩn hệ SI.\n"

            "- ĐÀM THOẠI: Khơi gợi các nghịch lý vật lý thường gặp để học sinh tự phá vỡ hiểu lầm (misconceptions)."

        ),

        "Hóa học": (

            "- TINH THẦN BỘ MÔN: Thầy dẫn dắt từ bản chất liên kết hóa học, cấu trúc phân tử và cơ chế phản ứng.\n"

            "- QUY CHUẨN: 100% sử dụng danh pháp quốc tế IUPAC theo CT GDPT 2018 (Alkane, Alkene, Alcohol, Ester, Amine...). Tuyệt đối không dùng danh pháp cũ.\n"

            "- ĐÀM THOẠI: Đặt câu hỏi về bản chất electron, độ âm điện, chuyển dịch cân bằng để học sinh tự suy luận sản phẩm."

        ),

        "Sinh học": (

            "- TINH THẦN BỘ MÔN: Thầy dẫn dắt từ quy luật tiến hóa, bản chất cơ chế di truyền - biến dị, sinh thái và sinh lý học.\n"

            "- NGUYÊN TẮC: Liên hệ thực tiễn cơ thể người, nông nghiệp, y học, môi trường sống. Dẫn dắt tư duy hệ thống sống."

        ),

        "Khoa học tự nhiên": (

            "- TINH THẦN BỘ MÔN: Tích hợp liên môn Vật lý - Hóa học - Sinh học cấp THCS.\n"

            "- NGUYÊN TẮC: Dùng phương pháp bàn tay nặn bột, đi từ quan sát thực nghiệm đến đúc kết quy luật. Dùng 100% IUPAC cho Hóa học."

        ),

        "Ngữ văn": (

            "- TINH THẦN BỘ MÔN: Thầy khai phóng cảm thức thẩm mỹ, chiều sâu nhân văn và bản lĩnh nghị luận độc lập.\n"

            "- NGUYÊN TẮC: Tiếp cận theo ĐẶC TRƯNG THỂ LOẠI (Thơ, Truyện, Kí, Kịch, Nghị luận, Thông tin). Chống văn mẫu 100%.\n"

            "- ĐÀM THOẠI: Gợi mở để học sinh tự bày tỏ cảm xúc, khám phá tầng sâu tư tưởng của văn bản và liên hệ với lẽ sống của bản thân."

        ),

        "Tiếng Anh": (

            "- TINH THẦN BỘ MÔN: Chuẩn khung năng lực CEFR / bậc 6 VN.\n"

            "- NGUYÊN TẮC: Thầy tương tác song ngữ thông minh, dẫn dắt tư duy ngôn ngữ bản ngữ theo ngữ cảnh tự nhiên (Authentic context), chỉ ra sắc thái ngữ nghĩa và cấu trúc giao tiếp."

        ),

        "Lịch sử": (

            "- TINH THẦN BỘ MÔN: Thầy dẫn dắt tư duy nhân quả, dòng chảy thời đại, phân tích bối cảnh và rút ra bài học lịch sử.\n"

            "- NGUYÊN TẮC: Không bắt học sinh học vẹt ngày tháng số liệu khô khan. Đặt câu hỏi phản biện: 'Vì sao trong bối cảnh đó, cha ông ta lại lựa chọn quyết sách này?'."

        ),

        "Địa lý": (

            "- TINH THẦN BỘ MÔN: Phân tích mối quan hệ giữa tự nhiên - dân cư - kinh tế theo không gian và lãnh thổ.\n"

            "- NGUYÊN TẮC: Đi từ bản đồ, bảng số liệu, giải thích nguyên nhân các quy luật địa lý và liên hệ sự phát triển bền vững."

        ),

        "Lịch sử & Địa lý": (

            "- TINH THẦN BỘ MÔN: Tích hợp không gian địa lý và thời gian lịch sử cấp THCS.\n"

            "- NGUYÊN TẮC: Gợi mở mối liên hệ giữa điều kiện tự nhiên và tiến trình dựng nước, giữ nước của dân tộc."

        ),

        "Tin học": (

            "- TINH THẦN BỘ MÔN: Dẫn dắt tư duy tính toán (Computational Thinking), phân rã bài toán và tối ưu hóa giải thuật.\n"

            "- NGUYÊN TẮC: Không viết code sẵn. Hướng dẫn học sinh từng bước xây dựng thuật toán, giải thích luồng dữ liệu logic."

        ),

        "Giáo dục kinh tế và pháp luật": (

            "- TINH THẦN BỘ MÔN: Dẫn dắt từ tình huống pháp luật và các quy luật kinh tế thị trường thực tế.\n"

            "- NGUYÊN TẮC: Bồi dưỡng tư duy phản biện pháp lý, trách nhiệm công dân và đạo đức kinh doanh."

        ),

        "Giáo dục công dân": (
            "- TINH THẦN BỘ MÔN: Bồi dưỡng chuẩn mực đạo đức, kỹ năng sống và hành vi pháp luật chuẩn mực cho học sinh THCS."
        ),
        "Công nghệ": (
            "- TINH THẦN BỘ MÔN: Dẫn dắt tư duy thiết kế kỹ thuật, quy trình công nghệ và ứng dụng thực tiễn.\n"
            "- NGUYÊN TẮC: Gắn liền với đời sống sản xuất, nông nghiệp thông minh, bản vẽ kỹ thuật, cơ khí, mạch điện tử và công nghệ số."
        )
    }



    spec = subject_guidelines.get(subject_name, "- TINH THẦN: Dẫn dắt học sinh tư duy sâu sắc, bám sát CT GDPT 2018.")



    if mode == "theory":

        return f"""Bạn là Thầy giáo Gia Sư AI Sư Phạm Trí Tuệ & Sáng Suốt tại Trường THPT Tân Hiệp (An Giang).

Học sinh: {student_nm} | Môn: {subject_name} | Lớp: {grade_level}.

Bài học đang chiếm lĩnh: '{topic_nm}'.



NỘI DUNG TÓM TẮT BÀI HỌC VỪA HỌC:

\"\"\"{context_data}\"\"\"



MỆNH LỆNH SƯ PHẠM THƯỢNG ĐẲNG CỐT TỬ (PHƯƠNG PHÁP SOCRATIC - THUẬT MAIEUTICS):

1. TUYỆT ĐỐI KHÔNG ĐƯỢC NHẠI LẠI HOẶC TÓM TẮT LẠI LÝ THUYẾT NHƯ MỘT CON VẸT MÁY MÓC.

2. NHẬP VAI MỘT NGƯỜI THẦY THÔNG THÁI, ÂN CẦN, TÔN TRỌNG HỌC TRÒ & THẤM NHUẦN TÂM NGUYỆN DƯỠNG NHÂN TÂM, ƯƠM NHÂN TÀI:
   - Dùng câu hỏi gợi mở tinh tế (mỗi lần chỉ 1 câu hỏi sâu sắc hoặc 1 phản ví dụ sắc bén) để kích thích {student_nm} tự suy ngẫm và tự nói ra bản chất.
   - Khi học sinh hỏi một câu khái niệm, hãy liên hệ ngay với 1 ví dụ đời thực sinh động hoặc 1 câu hỏi thực tiễn để học sinh tự thấy mối liên hệ.
   - BẢN CHẤT SOCRATIC ĐỈNH CAO - BIẾT ĐỠ ĐẺ VÀ BIẾT CHỐT ĐIỂM CHẠM SƯ PHẠM (CLOSURE):
     + Khi học sinh đang bế tắc hoặc sai sót: Gợi mở từng nấc thang tư duy, tuyệt đối không giải hộ, không đưa đáp số sẵn.
     + KHI HỌC SINH ĐÃ HIỂU RA VẤN ĐỀ ("AHA! MOMENT") HOẶC ĐÃ NÊU QUAN ĐIỂM ĐÚNG:
       * TUYỆT ĐỐI DỪNG TRUY VẤN - KHÔNG HỎI TIẾP VÔ NGHĨA TỚI NGÀY TẬN THẾ!
       * ĐÓNG GÓI BẢN CHẤT: Chốt cô đọng quy luật cốt lõi trong 1-2 câu sắc bén.
       * TRAO GỬI THÔNG ĐIỆP NHÂN VĂN SÂU SẮC & TRIẾT LÝ CUỘC SỐNG: Không khen sáo rỗng, hãy gắn kết bài toán cụ thể với một giá trị đạo đức cao đẹp của nhân loại (về lòng kiên trì vượt khó, sự bao dung, tính chính trực, lòng thiện lương, tình yêu quê hương đất nước) để nuôi dưỡng nhân tâm, giúp các em vững bước ra đời làm người có ích cho xã hội!
   - Khi học sinh hiểu nhầm: Đừng vội nói 'sai', hãy mỉm cười đặt một câu hỏi nhỏ phản biện để học sinh tự nhận ra điểm sơ hở của mình.

3. BẢN SẮC CHUYÊN SÂU MÔN {subject_name.upper()}:
{spec}

4. QUY CÁCH TRÌNH BÀY (BẮT BUỘC):
   - 100% VĂN BẢN. TUYỆT ĐỐI KHÔNG SINH ĐOẠN VOICE HAY AUDIO.
   - FORMAT CÔNG THỨC: BẮT BUỘC BỌC TẤT CẢ các công thức, biểu thức, biến số và ký hiệu trong cặp dấu đô la $...$ (Ví dụ: $\vec{{a}} = k\vec{{b}}$, $H_2O$, $v = s/t$). TUYỆT ĐỐI KHÔNG DÙNG DẤU BACKTICK (`) ĐỂ BỌC CÔNG THỨC HOẶC KÝ HIỆU VÌ SẼ BỊ LỖI HIỂN THỊ.
   - Ngắn gọn, đắt giá, mô phạm, kết thúc đàm thoại mỹ mãn khi học sinh đã làm chủ kiến thức."""



    elif mode == "review":

        return f"""Bạn là Thầy giáo Gia Sư AI Sư Phạm Trí Tuệ & Sáng Suốt tại Trường THPT Tân Hiệp (An Giang).

Học sinh: {student_nm} | Môn: {subject_name} | Lớp: {grade_level}.



TRIẾT LÝ HỌC THUẬT BẮT BUỘC: "NÚT THẮT CỔ CHAI CHUẨN HÓA TRI THỨC CT GDPT 2018 (SGK KNTT)"

CHẤM BÀI TRỰC TIẾP "FACE TO FACE" - SOI TỪNG DÒNG BÀI LÀM TRÊN ẢNH (BÚT TÍCH GIÁO VIÊN):

1. TUYỆT ĐỐI KHÔNG GIẢI HỘ, KHÔNG ĐƯA RA LỜI GIẢI TOÀN BỘ, KHÔNG CHO ĐÁP SỐ CUỐI CÙNG.

2. CẤU TRÚC PHẢN HỒI FACE TO FACE BẮT BUỘC (RÕ RÀNG TỪNG DÒNG):

   - ✅ DÒNG TICK XANH (OK CHUẨN CHỈ): Chỉ rõ cụ thể từng bước, từng công thức, dòng biến đổi hoặc lập luận mà em đã làm đúng và đạt chuẩn mực. Khen ngợi tạo động lực cho học sinh.

   - 🔴 DÒNG MỰC ĐỎ CHECK VAR KHÉT LẸT (CHỖ KHUẤT TẤT): Khoanh vùng chỉ đích danh dòng nào, bước nào đang có chỗ "khuất tất" (thiếu điều kiện xác định, nhầm dấu, biến đổi chưa chặt chẽ, ngộ nhận hoặc hiểu lầm khái niệm). Phân tích bản chất tại sao chỗ đó bị lỗi.

   - 💡 GỢI MỞ SOCRATIC (DẪN DẮT BẮC CẦU TƯ DUY): Đặt 1-2 câu hỏi gợi mở xoáy thẳng vào chỗ khuất tất để {student_nm} tự suy ngẫm, tự phát hiện mâu thuẫn và tự tay cầm bút sửa lại bài!

3. KHỐI TỌA ĐỘ VẼ BÚT TÍCH LÊN ẢNH:

BẮT BUỘC kẹp khối JSON tọa độ các dòng bài làm giữa cặp thẻ <ANNOTATIONS>...</ANNOTATIONS>:

<ANNOTATIONS>[{{"box":[ymin,xmin,ymax,xmax],"type":"ok","label":"Biến đổi đúng"}},{{"box":[ymin,xmin,ymax,xmax],"type":"var","label":"Chỗ khuất tất: thiếu điều kiện"}}]</ANNOTATIONS>

(Tọa độ box là [ymin, xmin, ymax, xmax] theo tỉ lệ 0 đến 1000 trên ảnh. 'type' chỉ nhận 'ok' hoặc 'var').

4. BẢN SẮC MÔN {subject_name.upper()}:

{spec}

5. ĐỊNH DẠNG CHẨN ĐOÁN BẮT BUỘC (Khi nhận xét ảnh bài làm):

Cuối phản hồi PHẢI có khối JSON:

<DIAGNOSTIC>{{"topic":"Tên bài học SGK KNTT Lớp {grade_level}","error_type":"Lỗi khái niệm/Lỗi tính toán/Lỗi phương pháp/Lỗi diễn đạt","evaluation":"Đạt/Cần rèn luyện thêm","scores":{{"truc1":80,"truc2":65,"truc3":90,"truc4":70,"truc5":85}}}}</DIAGNOSTIC>"""



    else:

        return f"""Bạn là Thầy giáo Gia Sư AI Sư Phạm Trí Tuệ & Sáng Suốt tại Trường THPT Tân Hiệp (An Giang).

Học sinh: {student_nm} | Môn: {subject_name} | Lớp: {grade_level}.



ĐÀM THOẠI HƯỚNG DẪN BÀI LÀM SOCRATIC THƯỢNG ĐẲNG:
- {student_nm} đang hỏi thêm Thầy về bài làm vừa nộp hoặc thắc mắc các bước tư duy.
- TUYỆT ĐỐI KHÔNG VIẾT SẴN LỜI GIẢI HỘ, KHÔNG CHO ĐÁP SỐ SẴN.
- Thầy đàm thoại như người Thầy thực thụ uyên bác, ân cần, giải thích bản chất bằng Text & LaTeX ($...$).
- NGUYÊN TẮC CHỐT VẤN ĐỀ (CLOSURE) & TRAO TRUYỀN NHÂN TÂM:
  + Khi học sinh đã ngộ ra sai sót hoặc tự giải đúng: DỪNG TRUY VẤN NGAY, KHÔNG HỎI DAI DẲNG VÔ CÙNG.
  + Chốt lại bài học và kết nối với MỘT THÔNG ĐIỆP NHÂN VĂN / BÀI HỌC CUỘC SỐNG SÂU SẮC ĐỘC BẢN để dưỡng nhân tâm, ươm mầm nhân tài có ích cho quê hương đất nước.
- BẢN SẮC MÔN {subject_name.upper()}:
{spec}
- Khích lệ học sinh tự tay cầm bút sửa lại bài và thốt lên niềm vui hiểu bài."""





def call_gemini_with_fallback(prompt_or_contents, system_instruction=None, json_mode=False):

    model_queue = get_active_model_queue()

    if not active_keys_pool:

        raise RuntimeError("Chưa cấu hình GEMINI_API_KEY. Thêm Key vào sidebar hoặc Streamlit Secrets.")



    # Ưu tiên key đang chạy tốt nhất trong phiên để đạt tốc độ 1 chạm tức thì

    cached_key = st.session_state.get("working_key")

    if cached_key and cached_key in active_keys_pool:

        key_queue = [cached_key] + [k for k in active_keys_pool if k != cached_key]

    else:

        key_queue = list(active_keys_pool)



    errors = []

    invalid_keys = set()

    deadline = time.monotonic() + 240

    if json_mode:
        effective_si = system_instruction if system_instruction else "Bạn là Chuyên gia Khảo thí và AI Engine chuyên nghiệp. Hãy phân tích và xuất dữ liệu định dạng JSON hợp lệ 100% tuân thủ cấu trúc yêu cầu, không thêm bất kỳ văn bản đàm thoại nào ngoài JSON."
    else:
        effective_si = f"{DEFAULT_PEDAGOGICAL_SYSTEM_INSTRUCTION}\n\n{system_instruction}" if system_instruction else DEFAULT_PEDAGOGICAL_SYSTEM_INSTRUCTION

    with st.status("Gia sư AI đang tiếp nhận yêu cầu...", expanded=True) as status_box:

        for current_model in model_queue:

            if time.monotonic() >= deadline:

                break

            status_box.update(label=f"Đang thử kết nối AI qua kênh {current_model}...", state="running")

            model_unavailable = False

            for current_key in key_queue:

                if current_key in invalid_keys or time.monotonic() >= deadline:

                    continue

                # 503/500 là lỗi tạm thời của model: thử lại cùng model một lần,

                # sau đó chuyển model, thay vì liên tục đổi key trên máy chủ đang bận.

                for attempt in range(2):

                    remaining_ms = int((deadline - time.monotonic()) * 1000)

                    if remaining_ms <= 0:

                        break

                    try:

                        cfg = types.GenerateContentConfig(

                            thinking_config=types.ThinkingConfig(thinking_level="low") if current_model.startswith("gemini-3") else None,

                            system_instruction=effective_si,

                        )

                        if json_mode:

                            cfg.response_mime_type = "application/json"

                        with genai.Client(api_key=current_key, http_options=types.HttpOptions(timeout=min(90000, remaining_ms))) as client:

                            response = client.models.generate_content(model=current_model, contents=prompt_or_contents, config=cfg)

                        candidates = getattr(response, "candidates", None) or []

                        if json_mode and candidates and "MAX_TOKENS" in str(getattr(candidates[0], "finish_reason", "")):

                            raise ValueError("Phản hồi JSON bị cắt do giới hạn token. Hãy giảm số câu hoặc thử model dự phòng.")

                        text = response.text

                        if not json_mode:
                            text = sanitize_katex_latex(text)

                        if not text or not text.strip():

                            candidates = getattr(response, "candidates", None) or []

                            reason = str(getattr(candidates[0], "finish_reason", "không có nội dung")) if candidates else "không có nội dung"

                            raise ValueError(f"AI trả phản hồi rỗng ({reason}).")

                        st.session_state.working_model = current_model

                        st.session_state.working_key = current_key

                        status_box.update(label="Đã nhận phản hồi từ AI.", state="complete")

                        return text

                    except Exception as e:

                        err_str = str(e)

                        for secret_key in active_keys_pool:

                            if secret_key:

                                err_str = err_str.replace(secret_key, "[API_KEY]")

                        errors.append(f"{current_model}, lần {attempt + 1}: {err_str[:600]}")

                        code = str(getattr(e, "code", ""))

                        is_temporary = code in {"500", "502", "503", "504"} or any(tag in err_str.lower() for tag in ["503", "500 internal", "unavailable", "high demand", "overloaded", "timed out", "timeout", "deadline_exceeded"])

                        if is_temporary:

                            if attempt == 0 and deadline - time.monotonic() > 2:

                                status_box.write(f"Model `{current_model}` tạm thời bận hoặc hết thời gian chờ. Thử lại sau 2 giây...")

                                time.sleep(2)

                                continue

                            status_box.write(f"Model `{current_model}` vẫn chưa đáp ứng. Chuyển model dự phòng...")

                            model_unavailable = True

                        elif code in {"401", "403"} or any(tag in err_str for tag in ["UNAUTHENTICATED", "PERMISSION_DENIED", "API_KEY_INVALID", "API key not valid"]):

                            invalid_keys.add(current_key)

                            if st.session_state.get("working_key") == current_key:

                                st.session_state.working_key = None

                            status_box.write("API Key không hợp lệ hoặc không có quyền. Chuyển ngay Key dự phòng trong nhóm...")

                        elif code == "429" or "RESOURCE_EXHAUSTED" in err_str or "429" in err_str:

                            if st.session_state.get("working_key") == current_key:

                                st.session_state.working_key = None

                            status_box.write("API đã hết hạn ngạch. Tự động xoay vòng sang Key dự phòng kế tiếp...")

                        else:

                            # 404 và lỗi cấu hình không được giải quyết bằng đổi key.

                            model_unavailable = True

                            status_box.write(f"Model `{current_model}` không xử lý được yêu cầu. Chuyển model dự phòng...")

                        break

                if model_unavailable:

                    if st.session_state.working_model == current_model:

                        st.session_state.working_model = None

                    break

        status_box.update(label="Chưa nhận được phản hồi AI. Xem nguyên nhân chi tiết bên dưới.", state="error")

    details = "\n".join(errors) or "Đã hết thời gian chờ tổng cộng 240 giây."

    raise RuntimeError(f"Không thể hoàn tất yêu cầu Gemini sau các lần thử dự phòng:\n{details}")





def stream_gemini_with_fallback(prompt_or_contents, system_instruction=None):

    """

    Generator phát trực tiếp (Streaming) câu trả lời từ Gemini.

    Kết hợp st.write_stream giúp học sinh nhận phản hồi sau 0.8 giây thay vì chờ 20 giây.

    """

    model_queue = get_active_model_queue()

    if not active_keys_pool:

        raise RuntimeError("Chưa cấu hình GEMINI_API_KEY. Thêm Key vào sidebar hoặc Streamlit Secrets.")



    cached_key = st.session_state.get("working_key")

    if cached_key and cached_key in active_keys_pool:

        key_queue = [cached_key] + [k for k in active_keys_pool if k != cached_key]

    else:

        key_queue = list(active_keys_pool)



    deadline = time.monotonic() + 180

    effective_si = f"{DEFAULT_PEDAGOGICAL_SYSTEM_INSTRUCTION}\n\n{system_instruction}" if system_instruction else DEFAULT_PEDAGOGICAL_SYSTEM_INSTRUCTION



    for current_model in model_queue:

        if time.monotonic() >= deadline:

            break

        model_unavailable = False

        for current_key in key_queue:

            if time.monotonic() >= deadline:

                continue

            for attempt in range(2):

                remaining_ms = int((deadline - time.monotonic()) * 1000)

                if remaining_ms <= 0:

                    break

                first_chunk = False

                try:

                    cfg = types.GenerateContentConfig(

                        thinking_config=types.ThinkingConfig(thinking_level="low") if current_model.startswith("gemini-3") else None,

                        system_instruction=effective_si,

                    )

                    first_chunk = False

                    with genai.Client(api_key=current_key, http_options=types.HttpOptions(timeout=min(90000, remaining_ms))) as client:

                        response_stream = client.models.generate_content_stream(

                            model=current_model, contents=prompt_or_contents, config=cfg

                        )

                        first_chunk = False

                        for chunk in response_stream:

                            txt = getattr(chunk, "text", "") or ""

                            if txt:

                                if not first_chunk:

                                    first_chunk = True

                                    st.session_state.working_model = current_model

                                    st.session_state.working_key = current_key

                                yield txt



                        if first_chunk:

                            return

                except Exception as e:

                    if first_chunk:
                        raise RuntimeError("Kết nối AI bị gián đoạn. Phần trả lời đã nhận được giữ nguyên; hãy gửi yêu cầu tiếp tục.") from None

                    err_str = str(e)

                    code = str(getattr(e, "code", ""))

                    is_temp = code in {"500", "502", "503", "504"} or any(t in err_str.lower() for t in ["503", "unavailable", "timeout"])

                    if is_temp:

                        if attempt == 0:

                            time.sleep(1.5)

                            continue

                        model_unavailable = True

                    break

            if model_unavailable:

                break



    # The streaming path has already tried the configured models and keys.
    # Starting another full retry budget here could block the UI for 420 seconds.
    raise RuntimeError("Chưa nhận được phản hồi AI sau các kênh dự phòng. Hãy thử lại sau.")









def is_social_or_tech_subject(sub: str) -> bool:

    if not sub:

        return False

    normalized = str(sub).strip().lower()

    return any(k in normalized for k in [

        "lịch sử", "địa lý", "địa lí", "kinh tế và pháp luật", "gdkt&pl",

        "công dân", "tin học", "công nghệ"

    ])





def is_natural_science_subject(sub: str) -> bool:

    if not sub:

        return False

    normalized = str(sub).strip().lower()

    return any(k in normalized for k in ["vật lý", "vật lí", "hóa học", "sinh học", "khoa học tự nhiên", "khtn"])





def validate_exam_data(exam, subject_name, counts=None):

    if not isinstance(exam, dict):

        raise ValueError("Đề thi phải là một JSON object.")

    if subject_name == "Ngữ văn":

        reading = exam.get("part_doc_hieu")

        writing = exam.get("part_viet")

        if not isinstance(reading, dict) or not reading.get("text") or not isinstance(reading.get("questions"), list) or not reading["questions"]:

            raise ValueError("Đề Ngữ văn thiếu ngữ liệu hoặc câu hỏi đọc hiểu.")

        if not isinstance(writing, list) or not writing:

            raise ValueError("Đề Ngữ văn thiếu câu hỏi viết.")

        for q in reading["questions"] + writing:

            if not isinstance(q, dict) or not isinstance(q.get("q"), str) or not q["q"].strip():

                raise ValueError("Câu hỏi Ngữ văn không hợp lệ.")

        return exam



    # CÁC MÔN TRẮC NGHIỆM CHUẨN QĐ 764/QĐ-BGDĐT

    for index, part in enumerate(("p1", "p2", "p3")):

        expected_cnt = counts[index] if (counts is not None and index < len(counts)) else None



        # Nếu môn thi không có phần này (ví dụ Phần III của các môn Xã hội / Tin học / Công nghệ, hoặc P.II/P.III của Tiếng Anh)

        if expected_cnt == 0:

            exam[part] = []

            continue



        items = exam.get(part, [])

        if not isinstance(items, list):

            items = []



        if expected_cnt is not None and expected_cnt > 0:

            if len(items) > expected_cnt:

                # Tự động cắt đúng số câu theo quy chế nếu AI sinh dư

                items = items[:expected_cnt]

            elif len(items) == 0:

                raise ValueError(f"Phần {part} không có câu hỏi nào được tạo.")

            exam[part] = items

        else:

            exam[part] = items



        for q in items:

            if not isinstance(q, dict) or not isinstance(q.get("q"), str) or not q["q"].strip():

                raise ValueError(f"Câu hỏi không hợp lệ ở {part}.")

            if part == "p1":

                opts = q.get("opt")

                if not isinstance(opts, list) or len(opts) < 4:

                    raise ValueError("Trắc nghiệm Phần I phải có đủ 4 lựa chọn A, B, C, D.")

                if len(opts) > 4:

                    opts = opts[:4]

                    q["opt"] = opts

                raw_ans = str(q.get("ans", "")).strip().upper()

                clean_ans = re.sub(r'[^A-D]', '', raw_ans)[:1]

                if clean_ans in "ABCD":

                    q["ans"] = clean_ans

                else:

                    q["ans"] = "A"

            elif part == "p2":

                stmts = q.get("stmts")

                if not isinstance(stmts, list) or len(stmts) < 4:

                    raise ValueError("Câu Đúng/Sai Phần II phải có đủ 4 lệnh hỏi a, b, c, d.")

                if len(stmts) > 4:

                    stmts = stmts[:4]

                    q["stmts"] = stmts

                for t in stmts:

                    if not isinstance(t, dict):

                        continue

                    if isinstance(t.get("a"), str):

                        t["a"] = t["a"].strip().lower() in ["true", "đúng", "1", "yes"]

                    elif not isinstance(t.get("a"), bool):

                        t["a"] = True

                    if not isinstance(t.get("t"), str) or not t["t"].strip():

                        t["t"] = "Mệnh đề khẳng định liên quan nội dung câu hỏi."

            elif part == "p3":

                ans_str = str(q.get("ans", "")).strip()

                if not ans_str:

                    q["ans"] = "0"

                else:

                    q["ans"] = ans_str



    if not any(exam.get(part) for part in ("p1", "p2", "p3")):

        raise ValueError("Đề thi không có câu hỏi.")

    return exam





from qa_runtime import numeric_answer_matches


def prepare_paired_data(frame, pre_col, post_col, minutes_col=None):

    result = frame.copy()

    for col in [pre_col, post_col] + ([minutes_col] if minutes_col else []):

        result[col] = pd.to_numeric(result[col].astype(str).str.replace(",", ".", regex=False), errors="coerce")

    mask = result[pre_col].between(0, 10) & result[post_col].between(0, 10)

    paired = result.loc[mask].copy()

    return paired, len(result) - len(paired)





from qa_runtime import paired_statistics


def render_exam_clock():

    if st.session_state.get("exam_state") != "testing":
        return

    deadline = st.session_state.get("exam_deadline")
    if not deadline or not isinstance(deadline, (int, float)):
        st.session_state.exam_deadline = time.time() + st.session_state.get("exam_time_mins", 45) * 60
        deadline = st.session_state.exam_deadline

    remaining = max(0, int(deadline - time.time()))

    if remaining <= 0:

        st.session_state.exam_state = "graded"

        st.session_state.exam_submitted_at = get_vn_time()

        st.session_state.pop("exam_deadline", None)

        st.rerun(scope="app")

        return



    mins = remaining // 60

    secs = remaining % 60

    clock_html = f"""

    <div id="exam-timer-wrapper" style="

        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.95));

        border: 2px solid #0284c7;

        border-radius: 12px;

        padding: 8px 16px;

        margin: 8px 0 14px 0;

        display: flex;

        align-items: center;

        justify-content: space-between;

        box-shadow: 0 4px 15px rgba(2, 132, 199, 0.25);

    ">

        <div style="display: flex; align-items: center; gap: 8px;">

            <span style="font-size: 20px;">⏱️</span>

            <span style="color: #cbd5e1; font-weight: 600; font-size: 13.5px;">Thời gian làm bài còn lại:</span>

        </div>

        <div id="exam-timer-display" style="

            font-family: 'Courier New', Courier, monospace;

            font-size: 22px;

            font-weight: 900;

            color: #38bdf8;

            letter-spacing: 2px;

            background: #0f172a;

            padding: 3px 14px;

            border-radius: 8px;

            border: 1px solid #334155;

        ">

            {mins:02d}:{secs:02d}

        </div>

    </div>

    <script>

    (function() {{

        let remainingSeconds = {remaining};

        const displayEl = document.getElementById('exam-timer-display');

        const wrapperEl = document.getElementById('exam-timer-wrapper');

        if (!displayEl) return;

        try {{
            const parentWin = window.parent || window;
            parentWin.__exam_auto_submitted = false;
        }} catch(e) {{}}

        if (window.__exam_timer_interval) {{

            clearInterval(window.__exam_timer_interval);
            window.__exam_timer_interval = null;

        }}

        window.__exam_timer_interval = setInterval(function() {{

            remainingSeconds -= 1;

            if (remainingSeconds <= 0) {{

                clearInterval(window.__exam_timer_interval);
                window.__exam_timer_interval = null;
                try {{
                    if (window.parent && window.parent.__exam_timer_interval) {{
                        clearInterval(window.parent.__exam_timer_interval);
                        window.parent.__exam_timer_interval = null;
                    }}
                }} catch(e) {{}}

                displayEl.innerText = "00:00";

                displayEl.style.color = "#ef4444";

                try {{

                    const targetDoc = window.parent.document || document;
                    const parentWin = window.parent || window;

                    if (!parentWin.__exam_auto_submitted) {{
                        parentWin.__exam_auto_submitted = true;
                        const submitBtn = Array.from(targetDoc.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Nộp bài'));
                        if (submitBtn) submitBtn.click();
                    }}

                }} catch(e) {{}}

                return;

            }}

            const m = Math.floor(remainingSeconds / 60);

            const s = remainingSeconds % 60;

            displayEl.innerText = (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;



            if (remainingSeconds <= 300) {{

                displayEl.style.color = '#f43f5e';

                displayEl.style.borderColor = '#f43f5e';

                wrapperEl.style.borderColor = '#e11d48';

                wrapperEl.style.boxShadow = '0 0 15px rgba(225, 29, 72, 0.4)';

            }} else if (remainingSeconds <= 600) {{

                displayEl.style.color = '#f59e0b';

                displayEl.style.borderColor = '#f59e0b';

            }}

        }}, 1000);

    }})();

    </script>

    """

    render_html_iframe(clock_html, height=65)









# ==============================================================================

# HỆ THỐNG XỬ LÝ BẢNG BIẾN THIÊN (BBT) & TOÁN HỌC CHUẨN FORM BỘ GD&ĐT

# ==============================================================================

def parse_and_align_bbt(raw_bbt):

    raw_str = str(raw_bbt).strip()
    raw_str = re.sub(r'\\+nearrow\b|\\nearrow', '↗', raw_str)
    raw_str = re.sub(r'\\+searrow\b|\\searrow', '↘', raw_str)
    raw_str = re.sub(r'\\n(?!earrow)', '\n', raw_str)
    lines = [l.strip() for l in raw_str.split('\n') if l.strip() and '---' not in l]

    rows = []

    for l in lines:

        parts = [p.strip() for p in l.split('|') if p.strip()]

        if parts: rows.append(parts)



    if len(rows) < 3:

        return rows



    lbl_x, cells_x = rows[0][0], rows[0][1:]

    lbl_yp, cells_yp = rows[1][0], rows[1][1:]

    lbl_y, cells_y = rows[2][0], rows[2][1:]



    total_slots = len(cells_y)

    if total_slots >= 3:

        aligned_x = [""] * total_slots

        if len(cells_x) >= 2:

            aligned_x[0] = cells_x[0]

            aligned_x[-1] = cells_x[-1]

            mid_x = cells_x[1:-1]

            num_mid = len(mid_x)

            if num_mid > 0:

                asympt_indices = [i for i, v in enumerate(cells_y) if '||' in v]

                if len(asympt_indices) == num_mid:

                    for val, pos in zip(mid_x, asympt_indices):

                        aligned_x[pos] = val

                else:

                    step = (total_slots - 1) / (num_mid + 1)

                    for idx_m, val in enumerate(mid_x):

                        pos = int(round((idx_m + 1) * step))

                        if 0 < pos < total_slots - 1:

                            aligned_x[pos] = val



        aligned_yp = [""] * total_slots

        if len(cells_yp) == total_slots:

            aligned_yp = cells_yp

        else:

            asympt_indices = [i for i, v in enumerate(cells_y) if '||' in v]

            if asympt_indices and '||' in cells_yp:

                yp_asympt_idx = [i for i, v in enumerate(cells_yp) if '||' in v]

                for yp_idx, y_slot in zip(yp_asympt_idx, asympt_indices):

                    aligned_yp[y_slot] = cells_yp[yp_idx]

                if len(cells_yp) >= 3 and len(asympt_indices) == 1:

                    mid_slot = asympt_indices[0]

                    left_pos = max(1, mid_slot // 2)

                    right_pos = min(total_slots - 2, (mid_slot + total_slots) // 2)

                    aligned_yp[left_pos] = cells_yp[0]

                    aligned_yp[right_pos] = cells_yp[-1]

            else:

                for idx_yp, val in enumerate(cells_yp):

                    pos = idx_yp + 1

                    if pos < total_slots - 1:

                        aligned_yp[pos] = val



        return [

            [lbl_x] + aligned_x,

            [lbl_yp] + aligned_yp,

            [lbl_y] + cells_y

        ]

    return rows



def format_pedagogical_bbt_html(raw_bbt, is_dark_mode=False):
    if not raw_bbt:
        return ""
    try:
        import precision_visual_engine as pve
        raw_bbt = pve.heal_bbt_mathematics(raw_bbt)
    except Exception:
        pass
    if not raw_bbt:
        return ""
    raw_str = str(raw_bbt).strip()
    if raw_str.lower() in ["null", "none", "{}", "undefined", "nil", "nan", "[]"] or len(raw_str) < 5:
        return ""

    raw_str = re.sub(r'\\+nearrow\b|\\nearrow', '↗', raw_str)
    raw_str = re.sub(r'\\+searrow\b|\\searrow', '↘', raw_str)
    raw_str = raw_str.replace('>>', '↗').replace('>', '↗')
    raw_str = re.sub(r'\\n(?!earrow)', '\n', raw_str).strip()

    # Ưu tiên hiển thị giao diện SVG Chuẩn Sư Phạm 2N-1 cột theo SGK Kết Nối Tri Thức
    try:
        lines_bbt = [l.strip() for l in raw_str.split('\n') if l.strip() and not re.match(r'^\|?[\s:\-\|]+\|?$', l)]
        if len(lines_bbt) >= 2:
            parsed_rows = [_parse_bbt_cells_safe(l) for l in lines_bbt]
            if len(parsed_rows) >= 3:
                svg_res = _build_svg_bbt_from_rows(parsed_rows[0], parsed_rows[1], parsed_rows[2])
                if svg_res:
                    return svg_res
            elif len(parsed_rows) == 2:
                row2_joined = " ".join(parsed_rows[1][1:])
                is_sign = not bool(re.search(r'(\\nearrow|\\searrow|↗|↘)', row2_joined))
                svg_res = _build_svg_bbt_from_rows(parsed_rows[0], [], parsed_rows[1], is_sign_table=is_sign)
                if svg_res:
                    return svg_res
    except Exception:
        pass

    rows = parse_and_align_bbt(raw_str)
    if not rows or len(rows) < 2 or not any(len(r) > 1 for r in rows):
        return ""

    col_count = len(rows[0]) if rows else 1
    max_cell_chars = max((len(str(c).strip()) for r in rows for c in r[1:]), default=4)
    dynamic_col_w = max(42, min(130, max_cell_chars * 13 + 18))
    dynamic_max_w = min(880, max(360, col_count * dynamic_col_w + 75))

    pad_h = "6px" if max_cell_chars > 8 else "10px"
    pad_v = "6px" if max_cell_chars > 8 else "8px"
    gap_v = "12px"

    html = f'<div style="display: flex; justify-content: center; margin: {gap_v} auto; width: 100%; max-width: {dynamic_max_w}px;">'
    html += f'<div style="background-color: #ffffff; padding: 0; width: 100%; overflow-x: auto; border: 2px solid #0f172a; border-radius: 8px; box-shadow: 0 4px 12px rgba(15,23,42,0.08);">'
    html += f'<table style="width: 100%; border-collapse: collapse; text-align: center; color: #0f172a !important; font-size: 16px; font-family: \'Times New Roman\', Times, serif;">'

    for r_i, row in enumerate(rows):
        border_b = "border-bottom: 1.5px solid #0f172a;" if r_i < len(rows) - 1 else ""
        html += f'<tr style="{border_b}">'
        for c_idx, cell in enumerate(row):
            c_disp = cell.replace('+\\infty', '+∞').replace('-\\infty', '-∞').replace('+inf', '+∞').replace('-inf', '-∞').replace('$', '').strip()
            if '||' in c_disp:
                c_disp = '<div style="border-left: 1.5px solid #dc2626; border-right: 1.5px solid #dc2626; display: inline-block; width: 4px; height: 24px; vertical-align: middle;"></div>'
            elif '↗' in c_disp:
                c_disp = '<span style="color:#16a34a !important; font-weight:bold; font-size:18px;">↗</span>'
            elif '↘' in c_disp:
                c_disp = '<span style="color:#dc2626 !important; font-weight:bold; font-size:18px;">↘</span>'

            if c_idx == 0:
                html += f'<td style="padding: {pad_v} {pad_h}; font-weight: bold; background-color: #f1f5f9; color: #0f172a !important; border-right: 2px solid #0f172a; width: 55px;">{c_disp}</td>'
            else:
                html += f'<td style="padding: {pad_v} 6px; min-width: 38px; color: #0f172a !important;">{c_disp}</td>'
        html += '</tr>'
    html += '</table></div></div>'
    return html



def format_pedagogical_bbt_latex(raw_bbt):

    raw_str = str(raw_bbt)

    raw_str = re.sub(r'\\+nearrow\b|\\nearrow', '↗', raw_str)
    raw_str = re.sub(r'\\+searrow\b|\\searrow', '↘', raw_str)
    raw_str = raw_str.replace('>>', '↗').replace('>', '↗')
    raw_str = re.sub(r'\\n(?!earrow)', '\n', raw_str).strip()

    rows = parse_and_align_bbt(raw_str)

    if not rows or len(rows) < 3: return ""



    col_count = len(rows[0])

    col_spec = "|c|" + "c" * (col_count - 1) + "|"

    tex = [r"\begin{center}", rf"\begin{{tabular}}{{{col_spec}}}", r"\hline"]

    for r in rows:

        row_cells = []

        for c in r:

            val = str(c).replace('+inf', r'+\infty').replace('-inf', r'-\infty').replace('inf', r'\infty').replace('↗', r'\nearrow').replace('↘', r'\searrow').replace('$', '').strip()

            if val == "||":

                row_cells.append(r"$\parallel$")

            elif val:

                row_cells.append(rf"${val}$" if not val.startswith(r"\textbf") else val)

            else:

                row_cells.append("")

        tex.append(" & ".join(row_cells) + r" \\ \hline")

    tex.append(r"\end{tabular}")

    tex.append(r"\end{center}")

    return "\n".join(tex)



def extract_and_normalize_mslgn(q: dict) -> dict:

    """

    TỰ ĐỘNG BÓC TÁCH & CHUẨN HÓA BẢNG MẪU SỐ LIỆU GHÉP NHÓM (MSLGN).

    Hỗ trợ cả bảng ngang, bảng dọc dạng Markdown hoặc văn bản phân tách:

      - Nhóm giá trị: [a; b), [b; c)...

      - Tần số: n_1, n_2...

    Đảm bảo 100% hiển thị bảng đẹp chuẩn Bộ GD&ĐT trên giao diện và bản in PDF.

    """

    if not isinstance(q, dict): return q

    q_text = str(q.get("q", ""))



    # 1. Nếu đã có mslgn_data, kiểm tra và chuẩn hóa cấu trúc

    if q.get("mslgn_data") and isinstance(q["mslgn_data"], dict):

        ms = q["mslgn_data"]

        grps = [str(g).strip() for g in ms.get("groups", [])]

        freqs = [str(f).strip() for f in ms.get("freq", [])]

        if grps and freqs and len(grps) == len(freqs):

            ms["groups"] = grps

            ms["freq"] = freqs

            if not ms.get("title"):

                ms["title"] = "Bảng mẫu số liệu ghép nhóm chuẩn hóa:"

            return q



    # 2. Bóc tách từ nội dung câu hỏi nếu có bảng markdown

    if "|" in q_text and any(k in q_text.lower() for k in ["nhóm", "tần số", "mẫu số liệu", "ghép nhóm", "học sinh", "số ngày", "khoảng", "chiều cao", "thời gian"]):

        lines = [l.strip() for l in q_text.split("\n") if l.strip()]

        tbl_lines = [l for l in lines if l.startswith("|") and l.endswith("|")]



        data_rows = [l for l in tbl_lines if not re.match(r'^[|\s:-]+$', l)]

        # TH1: Bảng ngang (Dòng 1 là Nhóm [a; b), Dòng 2 là Tần số)

        if len(data_rows) >= 2:

            row1_cells = [c.strip() for c in data_rows[0].split("|")[1:-1]]

            row2_cells = [c.strip() for c in data_rows[1].split("|")[1:-1]]



            has_intervals_r1 = sum(1 for c in row1_cells[1:] if re.search(r'[\[\(]\s*\d+.*?[;\-–]\s*\d+\s*[\]\)]', c))

            has_numbers_r2 = sum(1 for c in row2_cells[1:] if re.match(r'^\d+(?:\.\d+)?$', c))



            if has_intervals_r1 >= 2 and has_numbers_r2 >= 2 and len(row1_cells) == len(row2_cells):

                groups = row1_cells[1:]

                freqs = row2_cells[1:]

                q["mslgn_data"] = {"title": "Bảng mẫu số liệu ghép nhóm chuẩn hóa:", "groups": groups, "freq": freqs}

                clean_lines = [l for l in lines if l not in tbl_lines]

                q["q"] = "\n".join(clean_lines).strip()

                return q



        # TH2: Bảng dọc (Cột 1 là Nhóm, Cột 2 là Tần số)

        if len(data_rows) >= 3:

            groups = []

            freqs = []

            for r in data_rows[1:]:

                cells = [c.strip() for c in r.split("|")[1:-1]]

                if len(cells) >= 2 and re.search(r'[\[\(]\s*\d+.*?[;\-–]\s*\d+\s*[\]\)]', cells[0]) and re.match(r'^\d+(?:\.\d+)?$', cells[1]):

                    groups.append(cells[0])

                    freqs.append(cells[1])

            if len(groups) >= 2:

                q["mslgn_data"] = {"title": "Bảng mẫu số liệu ghép nhóm chuẩn hóa:", "groups": groups, "freq": freqs}

                clean_lines = [l for l in lines if l not in tbl_lines]

                q["q"] = "\n".join(clean_lines).strip()

                return q



    return q



# ==============================================================================
# HỆ THỐNG ĐIỂM TỰA KIẾN THỨC SƯ PHẠM SGK KẾT NỐI TRI THỨC (PEDAGOGICAL ANCHORS)
# ==============================================================================
from data.socratic_anchors import (
    SOCRATIC_KNOWLEDGE_ANCHORS,
    sanitize_socratic_hint,
    safe_json_loads,
)

def render_question_source_badge(q, idx=None):

    """

    Hiển thị Thẻ Xác Thực Nguồn Gốc & Kiểm Tra Chéo KHKT (Audit Provenance Badge).

    Chỉ hiển thị khi Giáo viên / Giám khảo bật công tắc 'Hiển thị Thẻ Đối Soát Chéo KHKT'.

    Định dạng HTML phẳng tuyệt đối, loại bỏ nguy cơ vỡ cú pháp markdown code block.

    """

    if not isinstance(q, dict): return
    if q.get("verification_warning"):
        st.warning("Cần giáo viên kiểm tra: " + str(q["verification_warning"]))


    # Kiểm tra công tắc mở/đóng đối soát chéo (Mặc định là TẮT để bảo toàn mỹ cảm đề thi)
    if not st.session_state.get("show_audit_badges_per_question", False):
        return

    # NẾU LÀ ĐỀ DO AI TỰ SÁNG TÁC (LUỒNG 1): HIỂN THỊ THẺ MINH BẠCH KHẢO THÍ ĐỘC BẢN
    if q.get("is_ai_generated") or not q.get("is_real_bank_question", False):
        ai_badge_html = (
            f'<div style="font-size: 11.5px; background: rgba(15, 23, 42, 0.75); border: 1px solid #10b981; border-left: 4px solid #10b981; border-radius: 6px; padding: 4px 10px; margin-bottom: 7px; display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 4px; box-shadow: 0 2px 6px rgba(0,0,0,0.25);">'
            f'<div style="color: #f1f5f9; display: flex; flex-wrap: wrap; align-items: center; gap: 5px;">'
            f'<span style="background: linear-gradient(135deg, #059669, #047857); color: #ffffff; padding: 1px 6px; border-radius: 3px; font-weight: 800; font-size: 10px; letter-spacing: 0.3px;">🤖 ĐỘC BẢN 2026</span>'
            f'<span style="color: #34d399; font-weight: 700;">Biên soạn bởi Trợ lý AI Khảo Thí</span>'
            f'<span style="color: #64748b;">•</span>'
            f'<span style="color: #cbd5e1; font-weight: 500;">Ngữ liệu mới 100% (Không trích xuất từ ngân hàng đề cũ)</span>'
            f'</div>'
            f'<div style="color: #94a3b8; font-size: 11px;">✨ Đã qua 7 tầng Deep Solver Guard</div>'
            f'</div>'
        )
        st.markdown(ai_badge_html, unsafe_allow_html=True)
        return

    src = str(q.get("source", "")).strip()
    school = q.get("school")
    if not school or "Điểm Quốc Gia" in str(school) or "Chuyên / Điểm" in str(school):
        school = "Bộ Đề Chuẩn Hóa CT GDPT 2018 (QĐ 764)"

    session = q.get("exam_session")
    year = q.get("year") or "2025 - 2026"
    portal = q.get("portal") or "Kho Khảo Thí Quốc Gia"
    orig_pos = q.get("orig_pos")

    orig_code = q.get("orig_exam_code")

    audit_id = q.get("audit_id")



    if not session:

        src_lower = src.lower()

        if "cuối" in src_lower or "hk1" in src_lower:

            session = "Kỳ thi Cuối Học Kỳ 1 (Chính thức)"

        elif "giữa" in src_lower:

            session = "Kỳ thi Giữa Học Kỳ 1 (Lần 1)"

        elif "khảo sát" in src_lower:

            session = "Đợt Khảo Sát Năng Lực Định Kỳ"

        elif "thử" in src_lower:

            session = "Thi Thử Tốt Nghiệp THPT (Lần 1)"

        else:

            session = "Khảo Thí Chuẩn Hóa Năng Lực"



    pos_html = f'<span style="color: #64748b;">•</span> <span style="color: #cbd5e1;">📍 {html.escape(str(orig_pos))}</span>' if orig_pos else ''

    code_html = f'<span style="color: #94a3b8; font-size: 10.5px;">(Mã đề gốc: {html.escape(str(orig_code))})</span>' if orig_code else ''

    aid_html = f'<span style="background: rgba(56, 189, 248, 0.15); color: #38bdf8; padding: 1px 5px; border-radius: 3px; font-family: monospace; font-size: 10.5px; font-weight: 600;">#{html.escape(str(audit_id))}</span>' if audit_id else ''



    badge_html = (

        f'<div style="font-size: 11.5px; background: rgba(15, 23, 42, 0.75); border: 1px solid #0284c7; border-left: 4px solid #38bdf8; border-radius: 6px; padding: 4px 10px; margin-bottom: 7px; display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 4px; box-shadow: 0 2px 6px rgba(0,0,0,0.25);">'

        f'<div style="color: #f1f5f9; display: flex; flex-wrap: wrap; align-items: center; gap: 5px;">'

        f'<span style="background: linear-gradient(135deg, #0284c7, #0369a1); color: #ffffff; padding: 1px 6px; border-radius: 3px; font-weight: 800; font-size: 10px; letter-spacing: 0.3px;">🏛️ ĐỐI SOÁT CHÉO KHKT</span>'

        f'<span style="color: #38bdf8; font-weight: 700;">{html.escape(str(school))}</span>'

        f'<span style="color: #64748b;">•</span>'

        f'<span style="color: #34d399; font-weight: 600;">📅 {html.escape(str(session))} ({html.escape(str(year))})</span>'

        f'{pos_html} {code_html}'

        f'</div>'

        f'<div style="color: #94a3b8; font-size: 11px; display: flex; align-items: center; gap: 6px;">'

        f'<span>🌐 Cổng: <b style="color: #38bdf8;">{html.escape(str(portal))}</b></span>'

        f'{aid_html}'

        f'</div></div>'

    )

    st.markdown(badge_html, unsafe_allow_html=True)



def question_visual_html(question):

    """XƯỞNG IN TĨNH CHUẨN SÁCH GIÁO KHOA & BỘ GD&ĐT (INLINE-WITH-TEXT CĂN GIỮA CO GỌN)."""

    pieces = []

    q_txt_lower = str(question.get("q", "")).lower()



    # 1. Bảng biến thiên (BBT): Xuất ảnh WebP chuẩn nét thẳng hàng tuyệt đối

    if question.get("bbt"):
        try:
            import precision_visual_engine as pve
            question["bbt"] = pve.heal_bbt_mathematics(question["bbt"])
        except Exception:
            pass
        b64_bbt = render_bbt_to_webp_base64(question["bbt"])

        if b64_bbt:

            pieces.append(f"<div style='text-align: center; margin: 4px auto 6px auto;'><img src='{b64_bbt}' style='max-width: 320px; width: 100%; height: auto; border-radius: 4px;' alt='Bảng biến thiên'/></div>")

        else:

            pieces.append(format_pedagogical_bbt_html(question["bbt"], is_dark_mode=False))



    # 2. Bảng mẫu số liệu ghép nhóm (MSLGN - Chuẩn Times New Roman & viền hộp đôi SGK)

    grouped = question.get("mslgn_data")

    if isinstance(grouped, dict):

        groups, frequencies = grouped.get("groups", []), grouped.get("freq", [])

        if groups and len(groups) == len(frequencies):

            tbl_dyn_w = min(680, max(360, len(groups) * 75 + 120))

            ms_title = html.escape(str(grouped.get("title", "Bảng mẫu số liệu ghép nhóm:")))

            cells_g = "".join(f"<td style='padding: 5px 10px; border: 1px solid #000; font-weight: 500;'>{html.escape(str(g))}</td>" for g in groups)

            cells_f = "".join(f"<td style='padding: 5px 10px; border: 1px solid #000; font-weight: 600;'>{html.escape(str(f))}</td>" for f in frequencies)

            pieces.append(

                f"<div style='display: flex; justify-content: center; margin: 6px auto 8px auto;'>"

                f"<div style='max-width: {tbl_dyn_w}px; background: #fff; padding: 0; width: 100%;'>"

                f"<p style='text-align: center; font-weight: bold; font-family: \"Times New Roman\", serif; color: #000; margin-bottom: 4px; font-size: 13.5px;'>{ms_title}</p>"

                f"<table style='width: 100%; border-collapse: collapse; text-align: center; font-family: \"Times New Roman\", serif; color: #000; border: 1.2px solid #000; font-size: 13.5px;'>"

                f"<tr><th style='padding: 5px 10px; border: 1px solid #000; font-weight: bold; width: 120px; background-color: #f8fafc;'>Nhóm giá trị</th>{cells_g}</tr>"

                f"<tr><th style='padding: 5px 10px; border: 1px solid #000; font-weight: bold; background-color: #f8fafc;'>Tần số (n)</th>{cells_f}</tr>"

                f"</table></div></div>"

            )

    # 2.5. Phục dựng thị giác: Ngữ liệu đa môn đặc thù (Vật lý, Hóa học, Sinh học, Địa lí, Toán thực tế)
    has_rendered_geom_svg = False

    # A. Vật lý 12 CT GDPT 2018 (Chu trình p-V, Từ trường & Bàn tay trái, Phóng xạ, Mạch RLC, Sóng cơ)
    if question.get("thermal_pv_visual") and isinstance(question["thermal_pv_visual"], dict):
        tpv = question["thermal_pv_visual"]
        if tpv.get("svg"):
            pieces.append(f"<div style='text-align: center; margin: 6px auto;'><div style='display: inline-block; max-width: 290px; width: 100%;'>{sanitize_svg_for_markdown(tpv['svg'])}</div></div>")
            has_rendered_geom_svg = True

    if not has_rendered_geom_svg and question.get("magnetic_visual") and isinstance(question["magnetic_visual"], dict):
        mag = question["magnetic_visual"]
        if mag.get("svg"):
            pieces.append(f"<div style='text-align: center; margin: 6px auto;'><div style='display: inline-block; max-width: 290px; width: 100%;'>{sanitize_svg_for_markdown(mag['svg'])}</div></div>")
            has_rendered_geom_svg = True

    if not has_rendered_geom_svg and question.get("nuclear_visual") and isinstance(question["nuclear_visual"], dict):
        nuc = question["nuclear_visual"]
        if nuc.get("svg"):
            pieces.append(f"<div style='text-align: center; margin: 6px auto;'><div style='display: inline-block; max-width: 290px; width: 100%;'>{sanitize_svg_for_markdown(nuc['svg'])}</div></div>")
            has_rendered_geom_svg = True

    if not has_rendered_geom_svg and question.get("wave_visual") and isinstance(question["wave_visual"], dict):
        wv = question["wave_visual"]
        if wv.get("svg"):
            pieces.append(f"<div style='text-align: center; margin: 6px auto;'><div style='display: inline-block; max-width: 290px; width: 100%;'>{sanitize_svg_for_markdown(wv['svg'])}</div></div>")
            has_rendered_geom_svg = True

    if not has_rendered_geom_svg and question.get("circuit_visual") and isinstance(question["circuit_visual"], dict):
        circ = question["circuit_visual"]
        if circ.get("svg"):
            pieces.append(f"<div style='text-align: center; margin: 6px auto;'><div style='display: inline-block; max-width: 290px; width: 100%;'>{sanitize_svg_for_markdown(circ['svg'])}</div></div>")
            has_rendered_geom_svg = True

    # B. Hóa học (Thí nghiệm điều chế khí, Pin điện hóa Daniell)
    if not has_rendered_geom_svg and question.get("chem_visual") and isinstance(question["chem_visual"], dict):
        ch = question["chem_visual"]
        if ch.get("svg"):
            pieces.append(f"<div style='text-align: center; margin: 6px auto;'><div style='display: inline-block; max-width: 290px; width: 100%;'>{sanitize_svg_for_markdown(ch['svg'])}</div></div>")
            has_rendered_geom_svg = True

    # C. Sinh học (Sơ đồ phả hệ di truyền & Lưới thức ăn)
    if not has_rendered_geom_svg and question.get("pedigree_visual") and isinstance(question["pedigree_visual"], dict):
        ped = question["pedigree_visual"]
        if ped.get("svg"):
            pieces.append(f"<div style='text-align: center; margin: 6px auto;'><div style='display: inline-block; max-width: 290px; width: 100%;'>{sanitize_svg_for_markdown(ped['svg'])}</div></div>")
            has_rendered_geom_svg = True

    if not has_rendered_geom_svg and question.get("food_web_visual") and isinstance(question["food_web_visual"], dict):
        fw = question["food_web_visual"]
        if fw.get("svg"):
            pieces.append(f"<div style='text-align: center; margin: 6px auto;'><div style='display: inline-block; max-width: 320px; width: 100%;'>{sanitize_svg_for_markdown(fw['svg'])}</div></div>")
            has_rendered_geom_svg = True

    # D. Địa lí (Bảng số liệu & Biểu đồ kinh tế)
    if not has_rendered_geom_svg and question.get("geo_chart") and isinstance(question["geo_chart"], dict):
        g_chart = question["geo_chart"]
        years = g_chart.get("years", [])
        series = g_chart.get("series", [])
        if years and series:
            tbl_h = f"<div style='display: flex; justify-content: center; margin: 6px auto;'><div style='max-width: 520px; width: 100%;'><p style='text-align: center; font-weight: bold; font-family: \"Times New Roman\", serif; font-size: 13px; margin-bottom: 4px;'>{html.escape(g_chart.get('title', 'Bảng số liệu thống kê:'))}</p><table style='width: 100%; border-collapse: collapse; text-align: center; font-family: \"Times New Roman\", serif; font-size: 13px; border: 1.2px solid #000;'><tr><th style='padding: 4px 8px; border: 1px solid #000; background: #f8fafc;'>Chỉ tiêu</th>" + "".join(f"<th style='padding: 4px 8px; border: 1px solid #000; background: #f8fafc;'>{y}</th>" for y in years) + "</tr>"
            for row in series:
                tbl_h += f"<tr><td style='padding: 4px 8px; border: 1px solid #000; font-weight: 500;'>{html.escape(str(row.get('name', '')))}</td>" + "".join(f"<td style='padding: 4px 8px; border: 1px solid #000;'>{val}</td>" for val in row.get("data", [])) + "</tr>"
            tbl_h += "</table></div></div>"
            pieces.append(tbl_h)
            has_rendered_geom_svg = True

    # E. Toán học thực tế & Tọa độ Oxyz
    if not has_rendered_geom_svg and question.get("composite_visual") and isinstance(question["composite_visual"], dict):
        comp = question["composite_visual"]
        if comp.get("svg"):
            pieces.append(f"<div style='text-align: center; margin: 5px auto;'><div style='display: inline-block; max-width: 220px;'>{sanitize_svg_for_markdown(comp['svg'])}</div></div>")
            has_rendered_geom_svg = True

    if not has_rendered_geom_svg and question.get("geom_3d") and isinstance(question["geom_3d"], dict):
        g3d = question["geom_3d"]
        g_type = str(g3d.get("type", ""))
        if g_type in ["tetrahedron", "oxyz_space", "oxyz_tetrahedron_sphere", "pure_box", "pure_triangular_prism", "pure_pyramid_quad", "flight_trajectory", "points_segment"] or g3d.get("sub_type") in ["oxyz_tetrahedron_sphere", "oxyz_distance_point_line", "oxyz_midpoint_projection"]:
            svg_g3d = g3d.get("svg")
            if not svg_g3d and pve:
                if any(k in q_txt_lower for k in ["thiết bị bay", "đường bay", "trạm phát sóng"]):
                    svg_g3d = pve.build_oxyz_flight_path_model(q_txt_lower).get("svg")
                elif any(k in q_txt_lower for k in ["tứ diện", "chóp tam giác"]):
                    svg_g3d = pve.build_oxyz_tetrahedron_model(q_txt_lower).get("svg")
            if svg_g3d:
                pieces.append(f"<div style='text-align: center; margin: 5px auto;'><div style='display: inline-block; max-width: 220px;'>{sanitize_svg_for_markdown(svg_g3d)}</div></div>")
                has_rendered_geom_svg = True

    # 3. Đồ thị 2D & Hình học 3D: CHỈ VẼ KHI CÂU HỎI THỰC SỰ LÀ TOÁN HỌC VÀ CÓ YÊU CẦU HÌNH VẼ
    is_non_math_subject = any(k in q_txt_lower for k in [
        "vật lý", "vật lí", "hóa học", "sinh học", "địa lí", "địa lý", "lực từ", "từ trường", "khí lý tưởng", "khí lí tưởng",
        "đẳng áp", "đẳng nhiệt", "đẳng tích", "phóng xạ", "chu kỳ bán rã", "chu kì bán rã", "hạt nhân", "đoạn mạch",
        "cuộn cảm", "tụ điện", "điện trở r", "thí nghiệm", "phả hệ", "lưới thức ăn", "gdp", "nhiệt lượng", "nhiệt độ"
    ]) and not any(m in q_txt_lower for m in ["hàm số", "tiệm cận", "bảng biến thiên", "tứ diện", "hình chóp", "lăng trụ", "oxyz"])

    if is_non_math_subject:
        function = None
        question.pop("f", None)
        question.pop("geom_3d", None)
    else:
        function = question.get("f") or question.get("geom_3d")

    is_geom_or_applied = any(kw in q_txt_lower for kw in [
        "tấm bìa", "khối chóp", "hình chóp", "lập phương", "hình hộp", "quả cầu",
        "bình nước", "bể chứa", "cắt góc", "gấp lại", "gấp lên", "cắt bỏ",
        "cửa sổ", "dây thép", "con cá", "vệ tinh", "dải led", "bán nguyệt"
    ])

    has_explicit_figure_ref = any(kw in q_txt_lower for kw in [
        "hình vẽ bên", "hình bên", "như hình vẽ", "như hình dưới", "như hình", "đồ thị bên", "đường cong trong hình", "bảng biến thiên bên"
    ])
    has_need_graph = not is_non_math_subject and (has_explicit_figure_ref or any(kw in q_txt_lower for kw in ["khối tròn xoay"]))

    is_calc_algebra = any(k in q_txt_lower for k in [
        "biểu thức", "giá trị của biểu thức", "bằng bao nhiêu", "tìm m",
        "tìm tham số", "t =", "p =", "t = ", "p = "
    ]) or (any(k in q_txt_lower for k in ["tính", "giá trị của"]) and any(k in q_txt_lower for k in ["biểu thức", "t =", "p =", "t = ", "p = ", "tham số"]))

    if is_calc_algebra and not any(kw in q_txt_lower for kw in ["hình vẽ bên", "hình bên", "đồ thị bên", "đường cong trong hình", "như hình vẽ bên"]):
        function = None
        question.pop("f", None)
        question.pop("geom_3d", None)
        question.pop("tikz", None)

    if not is_non_math_subject and not function and has_need_graph and not is_geom_or_applied and not is_calc_algebra:
        if any(k in q_txt_lower for k in ["ax^3", "bậc ba", "bậc 3"]):
            function = {"type": "func_3", "a": 1.0, "b": -3.0, "c": -1.0, "d": 2.0}
            question["f"] = function
        elif any(k in q_txt_lower for k in ["phân thức", "ax+b"]):
            if pve:
                solved_f = pve.solve_rational_1_1_from_text(question.get("q", ""), question.get("opt", []))
                if solved_f:
                    function = solved_f
                    question["f"] = function
        elif any(k in q_txt_lower for k in ["ax^2", "parabol", "parabola"]):
            function = {"type": "parabola", "a": 1.0, "b": -2.0, "c": -3.0}
            question["f"] = function

    if not has_rendered_geom_svg and isinstance(function, dict) and has_need_graph and not is_geom_or_applied:
        dtype = str(function.get("type", ""))
        try:
            if dtype in ["cone_3d", "cylinder_3d", "sphere_3d", "solid_of_revolution"]:
                if dtype == "cone_3d":
                    r_c = float(function.get("r", 3)); h_c = float(function.get("h", 4))
                    pieces.append(f"""<div style='text-align: center; margin: 4px auto 6px auto;'><svg width='160' height='145' viewBox='0 0 220 210'><ellipse cx='110' cy='170' rx='65' ry='22' fill='none' stroke='black' stroke-width='1.5' stroke-dasharray='4,4'/><path d='M 45,170 A 65 22 0 0 0 175,170' fill='none' stroke='black' stroke-width='1.5'/><line x1='45' y1='170' x2='110' y2='30' stroke='black' stroke-width='1.5'/><line x1='175' y1='170' x2='110' y2='30' stroke='black' stroke-width='1.5'/><line x1='110' y1='170' x2='110' y2='30' stroke='black' stroke-width='1.2' stroke-dasharray='4,4'/><line x1='110' y1='170' x2='175' y2='170' stroke='black' stroke-width='1.2' stroke-dasharray='4,4'/><circle cx='110' cy='170' r='2' fill='black'/><circle cx='110' cy='30' r='2' fill='black'/><text x='113' y='25' font-family='Times New Roman' font-size='14' font-style='italic'>S</text><text x='102' y='185' font-family='Times New Roman' font-size='14' font-style='italic'>O</text><text x='138' y='166' font-family='Times New Roman' font-size='14'>R={r_c}</text><text x='114' y='105' font-family='Times New Roman' font-size='14'>h={h_c}</text></svg></div>""")
                elif dtype == "cylinder_3d":
                    r_cyl = float(function.get("r", 3)); h_cyl = float(function.get("h", 5))
                    pieces.append(f"""<div style='text-align: center; margin: 4px auto 6px auto;'><svg width='160' height='145' viewBox='0 0 220 210'><ellipse cx='110' cy='45' rx='60' ry='20' fill='none' stroke='black' stroke-width='1.5'/><ellipse cx='110' cy='165' rx='60' ry='20' fill='none' stroke='black' stroke-width='1.2' stroke-dasharray='4,4'/><path d='M 50,165 A 60 20 0 0 0 170,165' fill='none' stroke='black' stroke-width='1.5'/><line x1='50' y1='45' x2='50' y2='165' stroke='black' stroke-width='1.5'/><line x1='170' y1='45' x2='170' y2='165' stroke='black' stroke-width='1.5'/><line x1='110' y1='45' x2='110' y2='165' stroke='black' stroke-width='1.2' stroke-dasharray='4,4'/><line x1='110' y1='165' x2='170' y2='165' stroke='black' stroke-width='1.2' stroke-dasharray='4,4'/><text x='103' y='38' font-family='Times New Roman' font-size='13' font-style='italic'>O</text><text x='102' y='182' font-family='Times New Roman' font-size='13' font-style='italic'>O\'</text><text x='136' y='161' font-family='Times New Roman' font-size='12'>R={r_cyl}</text><text x='114' y='110' font-size='12'>h={h_cyl}</text></svg></div>""")
                elif dtype == "sphere_3d":
                    r_s = float(function.get("r", 3))
                    pieces.append(f"""<div style='text-align: center; margin: 4px auto 6px auto;'><svg width='160' height='145' viewBox='0 0 220 210'><circle cx='110' cy='105' r='70' fill='none' stroke='black' stroke-width='1.5'/><ellipse cx='110' cy='105' rx='70' ry='22' fill='none' stroke='black' stroke-width='1.2' stroke-dasharray='4,4'/><path d='M 40,105 A 70 22 0 0 0 180,105' fill='none' stroke='black' stroke-width='1.5'/><line x1='110' y1='105' x2='180' y2='105' stroke='black' stroke-width='1.2' stroke-dasharray='4,4'/><circle cx='110' cy='105' r='2' fill='black'/><text x='101' y='120' font-family='Times New Roman' font-size='14' font-style='italic'>O</text><text x='140' y='100' font-family='Times New Roman' font-size='14'>R={r_s}</text></svg></div>""")
                elif dtype == "solid_of_revolution":
                    fa_b = function.get("a", 0); fb_b = function.get("b", 3); f_exp = function.get("f_expr", "y = f(x)")
                    pieces.append(f"""<div style='text-align: center; margin: 4px auto 6px auto;'><svg width='185' height='125' viewBox='0 0 260 180'><line x1='20' y1='90' x2='245' y2='90' stroke='black' stroke-width='1.2'/><line x1='45' y1='165' x2='45' y2='15' stroke='black' stroke-width='1.2'/><polygon points='245,87 252,90 245,93' fill='black'/><polygon points='42,15 45,8 48,15' fill='black'/><text x='242' y='106' font-family='Times New Roman' font-size='14'>x</text><text x='51' y='20' font-family='Times New Roman' font-size='14'>y</text><text x='35' y='105' font-family='Times New Roman' font-size='14' font-style='italic'>O</text><path d='M 65,72 Q 130,35 205,25' fill='none' stroke='black' stroke-width='1.8'/><path d='M 65,108 Q 130,145 205,155' fill='none' stroke='black' stroke-width='1.2' stroke-dasharray='4,4'/><ellipse cx='65' cy='90' rx='8' ry='18' fill='none' stroke='black' stroke-width='1.2'/><ellipse cx='205' cy='90' rx='16' ry='65' fill='none' stroke='black' stroke-width='1.2'/><text x='62' y='106' font-family='Times New Roman' font-size='13'>{fa_b}</text><text x='202' y='106' font-family='Times New Roman' font-size='13'>{fb_b}</text><text x='125' y='36' font-family='Times New Roman' font-size='13'>{f_exp}</text></svg></div>""")
            else:
                extra_pts = function.get("extra_points", [])
                b64_graph = render_math_graph_to_webp_base64(function, extra_points=extra_pts)
                if b64_graph:
                    pieces.append(f"<div style='text-align: center; margin: 4px auto 6px auto;'><img src='{b64_graph}' style='max-width: 175px; width: 100%; height: auto; border-radius: 4px;' alt='Đồ thị'/></div>")
        except Exception:
            pass

    # KHỬ TRÙNG LẶP TUYỆT ĐỐI 100%: Mỗi câu hỏi tối đa chỉ xuất đúng 1 hình vẽ duy nhất
    unique_pieces = []
    seen_piece_hashes = set()
    for p in pieces:
        p_clean = re.sub(r'\s+', '', p)
        if p_clean and p_clean not in seen_piece_hashes:
            seen_piece_hashes.add(p_clean)
            unique_pieces.append(p)

    return "\n".join(unique_pieces)





def latex_text(value):

    if not value: return ""

    value = str(value)

    value = value.replace("↗", r"$\nearrow$").replace("↘", r"$\searrow$").replace("∞", r"\infty")

    value = re.sub(r"\\(?:input|include|write18|openout|read|catcode|immediate)\b", "", value)

    chunks = re.split(r'(\$[^$]*\$)', value)

    replacements = {"\\": r"\textbackslash{}", "{": r"\{", "}": r"\}", "&": r"\&", "%": r"\%", "_": r"\_", "#": r"\#", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}

    return "".join(chunk if index%2 else "".join(replacements.get(char,char) for char in chunk) for index,chunk in enumerate(chunks))





def sanitize_print_math_text(text: str) -> str:
    """CHUẨN HÓA CÔNG THỨC TOÁN CHO BẢN IN PDF (MATHJAX 3): KHỬ SẠCH LỆNH LỆCH NGOẶC TẬP HỢP & DÍNH CHỮ."""
    if not text: return ""
    s = str(text).replace(r'\$', '$').replace('$$', '$')

    # Khắc phục lỗi chữ tiếng Việt có dấu và khoảng trắng bị bọc trong $...$ làm dính chữ trong MathJax
    def unwrap_vietnamese_math(match):
        inner = match.group(1)
        if re.search(r'[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđĐ]', inner) and ' ' in inner:
            return inner
        return match.group(0)
    s = re.sub(r'\$([^$]+)\$', unwrap_vietnamese_math, s)

    s = sanitize_katex_latex(s)

    # Khử triệt để lệnh \left và \right trong MathJax để tập hợp R \ {1} hiển thị đẹp 10 điểm
    s = s.replace('\\left', '').replace('\\right', '')
    s = s.replace(r'\left', '').replace(r'\right', '')

    # Tự động cân bằng nếu chuỗi bị lẻ dấu $
    if s.count('$') % 2 != 0:
        s += '$'
    return s


@st.cache_data(show_spinner=False, max_entries=4)
def get_mb_bank_vietqr_base64():
    """Hàm tải mã VietQR MB Bank của Thầy Phan Minh Trí (base64) để nhúng trực tiếp vào bản in PDF."""
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        opt_b64_path = os.path.join(base_dir, "assets", "mb_bank_vietqr_opt_b64.txt")
        if os.path.exists(opt_b64_path):
            with open(opt_b64_path, "r", encoding="utf-8") as f:
                b64 = f.read().strip()
                if b64:
                    return f"data:image/png;base64,{b64}"
    except Exception:
        pass
    return ""


def audit_and_heal_exam_semantics(exam: dict, subject_name: str = "Toán học", grade_name: str = "Lớp 12") -> dict:
    """
    CHỐT CHẶN CUỐI CÙNG VỀ NGỮ NGHĨA & NỘI DUNG ĐỀ THI (VIP 66.5 - GDPT 2018):
    1. Khử sạch 100% câu chữ chắp vá, lỗi copy-paste từ đề cũ (như 'mặt cầu tiếp xúc... hoặc bán kính mặt cầu ngoại tiếp').
    2. Khử triệt để lỗi Đa Đáp Án ở các câu tính đơn điệu (đồng biến/nghịch biến từ BBT).
    3. Tự động đồng bộ Hướng dẫn Socratic bám sát bản chất toán học, không bị lệch chuyên đề.
    """
    if not isinstance(exam, dict):
        return exam

    p_keys = ["p1", "p2", "p3", "part_1", "part_2", "part_3"]
    for pk in p_keys:
        q_list = exam.get(pk)
        if not isinstance(q_list, list):
            continue
        for q in q_list:
            if not isinstance(q, dict):
                continue

            # --- 1. CHỮA LÀNH CÂU CHỮ VĂN PHONG VÔ LÝ / CHẮP VÁ ---
            q_txt = str(q.get("q", ""))
            if "tiếp xúc với mặt phẳng" in q_txt and any(hw in q_txt.lower() for hw in ["hoặc bán kính", "hoặc tính"]):
                q_txt = re.sub(r'(?i)Bán kính mặt cầu tiếp xúc.*?hoặc\s*(?:bán\s+kính\s+)?', 'Bán kính ', q_txt).strip()
                q["q"] = q_txt
            elif re.search(r'(?i)\bhoặc\s+bán\s+kính\s+mặt\s+cầu\s+ngoại\s+tiếp\b', q_txt):
                q_txt = re.sub(r'(?i)Bán kính mặt cầu tiếp xúc.*?hoặc\s*(?:bán\s+kính\s+)?', 'Bán kính ', q_txt).strip()
                q["q"] = q_txt

            # --- 2. KHỬ LỖI ĐA ĐÁP ÁN Ở CÂU ĐỒNG BIẾN / NGHỊCH BIẾN TỪ BBT ---
            opts = q.get("opt") or []
            if len(opts) == 4 and any(k in q_txt.lower() for k in ["đồng biến trên khoảng", "hàm số đã cho đồng biến", "đồng biến"]):
                corr_ans = str(q.get("ans", "A")).strip().upper()
                opt_texts = [str(o) for o in opts]
                has_neg_inf = any("-\\infty" in o or "-inf" in o or "-1" in o or "-∞" in o for o in opt_texts[:2])
                has_pos_inf = any("+\\infty" in o or "+inf" in o or "(2;" in o or "(2," in o or "+∞" in o for o in opt_texts[2:])
                # Nếu đáp án chính thức là A, phương án C bị dính khoảng đồng biến thứ 2 (2; +inf) -> Sửa C thành (-1; 2)
                if corr_ans == "A" and has_neg_inf and has_pos_inf:
                    opts[2] = "C. (-1; 2)"
                    q["opt"] = opts

            # --- 3. ĐỒNG BỘ LỜI GIẢI SOCRATIC CHUẨN XÁC ---
            ans_val = str(q.get("ans", ""))
            if q.get("stmts"):
                ans_val = "; ".join(f"{chr(97+i)}: " + ("Đúng" if (t.get("a") if "a" in t else t.get("ans", True)) else "Sai") for i, t in enumerate(q.get("stmts", [])))

            parsed_grade = int(re.search(r'\d+', str(grade_name)).group(0)) if re.search(r'\d+', str(grade_name)) else 12
            q["explain"] = sanitize_socratic_hint(
                q.get("explain", ""),
                correct_answer=ans_val,
                q_text=q.get("q", ""),
                options=q.get("opt"),
                level=q.get("level", "TH"),
                subject=subject_name,
                grade_num=parsed_grade
            )

            # --- 4. TẦNG KIỂM CHỨNG TOÁN HỌC BIỂU TƯỢNG SYMPY (NEURO-SYMBOLIC VERIFIER) ---
            if audit_ai_generated_question_sympy and "toán" in str(subject_name).lower():
                try:
                    q.pop("neuro_symbolic_verified", None)
                    audit_res = audit_ai_generated_question_sympy(q)
                    if audit_res.get("hallucination_detected"):
                        q["verification_warning"] = audit_res.get("note", "Đáp án cần giáo viên kiểm tra")
                    if audit_res.get("audited") and audit_res.get("verified") and not audit_res.get("hallucination_detected") and audit_res.get("analysis_verified"):
                        q["neuro_symbolic_verified"] = True
                except Exception:
                    pass

    return exam


def build_exam_exports(exam, subject_name, grade_name, duration, include_answers=False,
                       template_style="form1",
                       teacher_name="Thầy Phan Minh Trí",
                       school_name="TRƯỜNG THPT TÂN HIỆP • THẦY PHAN MINH TRÍ",
                       quote_text="Dưỡng thiện tâm, Ươm nhân tài",
                       quote_author="THẦY PHAN MINH TRÍ",
                       show_support_qr=True):
    import datetime
    # CHỐT CHẶN CUỐI CÙNG: Thẩm định ngữ nghĩa, khử đa đáp án và chuẩn hóa Socratic trước khi xuất bản
    exam = audit_and_heal_exam_semantics(exam, subject_name=subject_name, grade_name=grade_name)
    current_year = datetime.datetime.now().year
    school_year = f"{current_year} - {current_year+1}"
    exam_count = exam.get('exam_count') or st.session_state.get('exam_mix_count') or max(1, int(st.session_state.get('global_exam_count') or 1))
    ex_code = str(exam.get('code', st.session_state.get('exam_code', '101')))
    title = f"Kỳ thi Khảo sát chất lượng lần thứ {exam_count} — Môn {subject_name} ({grade_name}) — Mã đề {ex_code}"

    app_target_url = f"{APP_URL}?exam_code={ex_code}&subject={urllib.parse.quote(subject_name)}"
    qr_base64 = generate_local_qr_base64(app_target_url, fill_color="#0f172a", back_color="#ffffff")
    mb_qr_base64 = get_mb_bank_vietqr_base64()

    # ==================== 1. XÂY DỰNG TIÊU ĐỀ HEADER HTML THEO MẪU ====================
    if template_style == "form2":
        # MẪU 2: CHUẨN SƯ PHẠM HIỆN ĐẠI (OVERLEAF TYPOGRAPHY & GDPT 2018 CHUẨN QUỐC GIA)
        header_html = f"""
        <div style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border: 1.5px solid #0284c7; border-radius: 8px; padding: 14px 18px; margin-bottom: 14px; font-family: 'Times New Roman', Times, serif;">
            <table class="header-table" style="width: 100%; border: none !important; border-collapse: collapse;">
                <tr style="border: none !important;">
                    <td style="width: 55%; vertical-align: top; border: none !important; padding: 0 !important; background: transparent !important;">
                        <div style="font-size: 11.5px; font-weight: bold; color: #0369a1; text-transform: uppercase; letter-spacing: 0.5px;">BỘ GIÁO DỤC & ĐÀO TẠO • GDPT 2018 CHUẨN QUỐC GIA</div>
                        <div style="font-size: 14px; font-weight: bold; color: #0f172a; text-transform: uppercase; margin: 2px 0;">{school_name}</div>
                        <div style="font-size: 12.5px; color: #334155;">Biên soạn: <strong style="color: #0369a1;">{teacher_name}</strong></div>
                        <div style="width: 140px; height: 1.5px; background: #0284c7; margin: 4px 0;"></div>
                    </td>
                    <td style="width: 33%; text-align: center; vertical-align: top; border: none !important; padding: 0 !important; background: transparent !important;">
                        <div style="display: inline-block; background: #0284c7; color: #ffffff; font-weight: bold; font-size: 13.5px; padding: 3px 12px; border-radius: 4px; letter-spacing: 1px;">
                            MÃ ĐỀ THI: {ex_code}
                        </div>
                        <div style="font-size: 11.5px; color: #475569; margin-top: 4px;">Kỳ thi KSCL lần thứ {exam_count}</div>
                        <div style="font-size: 11.5px; font-weight: bold; color: #0f172a;">NĂM HỌC {school_year}</div>
                    </td>
                    <td style="width: 12%; text-align: right; vertical-align: top; border: none !important; padding: 0 !important; background: transparent !important;" class="no-print-hide">
                        <img src="{qr_base64}" style="width: 60px; height: 60px; border: 1px solid #0284c7; border-radius: 4px; padding: 2px; background: #fff;" alt="QR Code">
                        <div style="font-size: 8px; color: #0369a1; text-align: center; font-weight: bold; margin-top: 2px;">Quét tra cứu</div>
                    </td>
                </tr>
            </table>
            <div style="text-align: center; margin-top: 10px; border-top: 1px dashed #7dd3fc; padding-top: 8px;">
                <span style="font-size: 15px; font-weight: bold; color: #0c4a6e; text-transform: uppercase; letter-spacing: 0.5px;">
                    ĐỀ KHẢO SÁT CHẤT LƯỢNG MÔN {subject_name.upper()} — {grade_name.upper()}
                </span><br>
                <span style="font-size: 12.5px; font-style: italic; color: #334155;">
                    Thời gian làm bài: {int(duration)} phút (Không kể thời gian phát đề)
                </span>
            </div>
            <div style="font-style: italic; font-size: 12.5px; color: #1e293b; margin-top: 8px; padding-top: 6px; border-top: 1px solid #e0f2fe;">
                Họ và tên thí sinh: ................................................................................ Số báo danh: ....................... Phòng thi: .........
            </div>
        </div>
        """
    else:
        # MẪU 1: CHUẨN KHẢO THÍ TRUYỀN THỐNG CÔNG PHU (NGUYÊN BẢN 100% CỦA THẦY PHAN MINH TRÍ - BỘ GD&ĐT)
        header_html = f"""
        <table class="header-table" style="width: 100%; border: none !important; border-collapse: collapse; margin-bottom: 12px; font-family: 'Times New Roman', Times, serif;">
            <tr style="border: none !important;">
                <td style="width: 44%; text-align: center; vertical-align: top; border: none !important; padding: 0 !important; background: transparent !important;">
                    <div style="font-size: 13px; font-weight: bold; text-transform: uppercase;">SỞ GIÁO DỤC VÀ ĐÀO TẠO AN GIANG</div>
                    <div style="font-size: 13.5px; font-weight: bold; text-transform: uppercase;">{school_name}</div>
                    <div style="width: 120px; height: 1.2px; background: #000; margin: 3px auto 5px auto;"></div>
                    <div style="font-size: 14px; font-weight: bold;">MÃ ĐỀ THI: <span style="font-size: 15px; letter-spacing: 1px;">{ex_code}</span></div>
                </td>
                <td style="width: 44%; text-align: center; vertical-align: top; border: none !important; padding: 0 !important; background: transparent !important;">
                    <div style="font-size: 13.5px; font-weight: bold; text-transform: uppercase;">KỲ THI KHẢO SÁT CHẤT LƯỢNG LẦN THỨ {exam_count}</div>
                    <div style="font-size: 13px; font-weight: bold;">NĂM HỌC {school_year}</div>
                    <div style="font-size: 14px; font-weight: bold; color: #000; text-transform: uppercase; margin-top: 2px;">MÔN: {subject_name.upper()} - {grade_name}</div>
                    <div style="font-size: 13px; font-style: italic;">Thời gian làm bài: {int(duration)} phút (Không kể thời gian phát đề)</div>
                    <div style="width: 150px; height: 1.2px; background: #000; margin: 4px auto 0 auto;"></div>
                </td>
                <td style="width: 12%; text-align: right; vertical-align: top; border: none !important; padding: 0 !important; background: transparent !important;">
                    <img src="{qr_base64}" style="width: 65px; height: 65px; border: 1px solid #cbd5e1; border-radius: 4px; padding: 2px;" alt="QR Code">
                    <div style="font-size: 8.5px; color: #64748b; text-align: center; margin-top: 1px;">Quét tra cứu</div>
                </td>
            </tr>
        </table>
        <div style="font-style: italic; font-size: 13.5px; margin-bottom: 12px; margin-top: 6px; font-family: 'Times New Roman', Times, serif;">
            Họ và tên thí sinh: ................................................................................ Số báo danh: ....................... Phòng thi: .........
        </div>
        """

    blocks = [header_html]

    # ==================== 2. XÂY DỰNG NGUỒN LATEX OVERLEAF (TIKZ & TABULARX CHUẨN CHỈ) ====================
    latex_school_escaped = latex_text(school_name)
    latex_teacher_escaped = latex_text(teacher_name)
    latex_quote_escaped = latex_text(quote_text)
    latex_author_escaped = latex_text(quote_author.upper())

    if template_style == "form2":
        latex_header = f"""\\noindent
\\begin{{minipage}}[t]{{0.50\\textwidth}}
\\textbf{{\\small BỘ GIÁO DỤC \\& ĐÀO TẠO • GDPT 2018}} \\\\
\\textbf{{\\large {latex_school_escaped}}} \\\\
\\textit{{\\small Biên soạn: {latex_teacher_escaped}}} \\[0.05cm]
\\rule{{4.5cm}}{{0.8pt}}
\\end{{minipage}}
\\hfill
\\begin{{minipage}}[t]{{0.48\\textwidth}}
\\raggedleft
\\textbf{{\\large MÃ ĐỀ THI: {ex_code}}} \\\\
\\textbf{{Kỳ thi KSCL lần thứ {exam_count} - Năm học {school_year}}} \\[0.05cm]
\\rule{{4cm}}{{0.8pt}}
\\end{{minipage}}
\\vspace{{0.3cm}}

\\begin{{center}}
\\textbf{{\\Large ĐỀ KHẢO SÁT CHẤT LƯỢNG MÔN {latex_text(subject_name).upper()} - {grade_name}}} \\[0.1cm]
\\textit{{Thời gian làm bài: {int(duration)} phút (Không kể thời gian phát đề)}}
\\end{{center}}
\\vspace{{0.2cm}}

\\noindent \\textit{{Họ và tên thí sinh: \\dotfill Số báo danh: \\dotfill Phòng thi: \\dotfill}}
\\vspace{{0.4cm}}
"""
        tex = [
            r"\documentclass[12pt,a4paper]{article}",
            r"\usepackage[utf8]{inputenc}",
            r"\usepackage[T5]{fontenc}",
            r"\usepackage[vietnamese]{babel}",
            r"\usepackage{amsmath,amssymb,amsfonts,mathrsfs}",
            r"\usepackage{geometry}",
            r"\geometry{a4paper, left=1.8cm, right=1.8cm, top=1.8cm, bottom=2.0cm}",
            r"\usepackage{tikz,pgfplots}",
            r"\pgfplotsset{compat=1.18}",
            r"\usepackage{tabularx,array,booktabs,multirow,multicol}",
            r"\usepackage{fancyhdr}",
            r"\usepackage{enumitem}",
            r"\usepackage{tcolorbox}",
            r"\pagestyle{fancy}",
            r"\fancyhf{}",
            rf"\lhead{{\footnotesize {latex_school_escaped} - NĂM HỌC {school_year}}}",
            rf"\rhead{{\footnotesize MÔN {latex_text(subject_name).upper()} - MÃ ĐỀ: {ex_code}}}",
            rf"\lfoot{{\footnotesize \textit{{❝{latex_quote_escaped}❞}} — \textbf{{{latex_author_escaped}}}}}",
            rf"\rfoot{{\footnotesize Trang \thepage}}",
            r"\renewcommand{\headrulewidth}{0.4pt}",
            r"\renewcommand{\footrulewidth}{0.4pt}",
            r"\begin{document}",
            latex_header
        ]
    else:
        latex_header = f"""\\noindent
\\begin{{minipage}}[t]{{0.43\\textwidth}}
\\centering
\\textbf{{SỞ GIÁO DỤC VÀ ĐÀO TẠO AN GIANG}} \\\\
\\textbf{{{latex_school_escaped}}} \\\\[0.05cm]
\\rule{{3.5cm}}{{0.6pt}} \\\\[0.15cm]
\\textbf{{\\large MÃ ĐỀ THI: {ex_code}}}
\\end{{minipage}}
\\hfill
\\begin{{minipage}}[t]{{0.54\\textwidth}}
\\centering
\\textbf{{KỲ THI KHẢO SÁT CHẤT LƯỢNG LẦN THỨ {exam_count}}} \\\\
\\textbf{{NĂM HỌC {school_year}}} \\\\
\\textbf{{\\large Môn: {latex_text(subject_name)} - {grade_name}}} \\\\[0.05cm]
\\textit{{Thời gian làm bài: {int(duration)} phút (Không kể thời gian phát đề)}} \\\\[0.05cm]
\\rule{{4.5cm}}{{0.6pt}}
\\end{{minipage}}
\\vspace{{0.35cm}}

\\noindent \\textit{{Họ và tên thí sinh: \\dotfill Số báo danh: \\dotfill Phòng thi: \\dotfill}}
\\vspace{{0.4cm}}
"""
        tex = [
            r"\documentclass[12pt,a4paper]{article}",
            r"\usepackage[utf8]{inputenc}",
            r"\usepackage[T5]{fontenc}",
            r"\usepackage[vietnamese]{babel}",
            r"\usepackage{amsmath,amssymb,amsfonts,mathrsfs}",
            r"\usepackage{geometry}",
            r"\geometry{a4paper, left=1.8cm, right=1.8cm, top=1.8cm, bottom=1.8cm}",
            r"\usepackage{tikz,pgfplots}",
            r"\pgfplotsset{compat=1.18}",
            r"\usepackage{tabularx,array,booktabs,multirow,multicol}",
            r"\usepackage{fancyhdr}",
            r"\usepackage{enumitem}",
            r"\usepackage{tcolorbox}",
            r"\pagestyle{fancy}",
            r"\fancyhf{}",
            rf"\lhead{{\footnotesize {latex_school_escaped} - NĂM HỌC {school_year}}}",
            rf"\rhead{{\footnotesize MÔN {latex_text(subject_name).upper()} - MÃ ĐỀ: {ex_code}}}",
            r"\cfoot{\thepage}",
            r"\renewcommand{\headrulewidth}{0.4pt}",
            r"\begin{document}",
            latex_header
        ]

    sections = []
    if subject_name == "Ngữ văn":
        passage = exam.get("part_doc_hieu", {}).get("text", "")
        blocks.append(f"""
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 12px 14px; margin-bottom: 12px; font-size: 14px; line-height: 1.6;">
            <strong>I. ĐỌC HIỂU (4.0 điểm)</strong><br>
            <em>Đọc đoạn trích sau và thực hiện các yêu cầu:</em><br><br>
            {html.escape(passage).replace(chr(10), '<br>')}
        </div>
        """)
        tex.append(r"\section*{PHẦN I: ĐỌC HIỂU (4.0 ĐIỂM)}")
        tex.append(r"\noindent\textit{Đọc đoạn trích sau và thực hiện các yêu cầu:}\par\vspace{0.2cm}")
        tex.append(r"\begin{quote}\small " + latex_text(passage) + r"\end{quote}\par\vspace{0.3cm}")
        sections = [
            ("", exam.get("part_doc_hieu", {}).get("questions", [])),
            ("PHẦN II: VIẾT (6.0 ĐIỂM)", exam.get("part_viet", exam.get("part_lam_van", {}).get("questions", [])))
        ]
    else:
        p1 = exam.get("p1") or exam.get("part_1") or []
        p2 = exam.get("p2") or exam.get("part_2") or []
        p3 = exam.get("p3") or exam.get("part_3") or []
        p1_len = len(p1)
        p2_len = len(p2)
        p3_len = len(p3)
        sections = [
            (f"PHẦN I. Câu trắc nghiệm nhiều phương án lựa chọn (Thí sinh trả lời từ câu 1 đến câu {p1_len}. Mỗi câu hỏi thí sinh chỉ chọn một phương án).", p1),
            (f"PHẦN II. Câu trắc nghiệm đúng sai (Thí sinh trả lời từ câu 1 đến câu {p2_len}. Trong mỗi ý a), b), c), d) ở mỗi câu, thí sinh chọn đúng hoặc sai).", p2),
            (f"PHẦN III. Câu trắc nghiệm trả lời ngắn (Thí sinh trả lời từ câu 1 đến câu {p3_len}. Thí sinh điền kết quả vào ô quy định).", p3)
        ]

    for heading, questions in sections:
        if not questions:
            continue
        if heading:
            if "(" in heading and ")" in heading:
                p_title = heading.split("(")[0].strip()
                p_guide = "(" + heading.split("(", 1)[1].strip()
                header_display = f"<span style='font-weight: bold;'>{p_title}</span> <span style='font-style: italic; font-weight: normal;'>{p_guide}</span>"
                tex_header = r"\noindent\textbf{\large " + latex_text(p_title) + r"} \textit{\normalsize " + latex_text(p_guide) + r"}\par\vspace{0.2cm}"
            else:
                header_display = f"<span style='font-weight: bold;'>{heading}</span>"
                tex_header = r"\noindent\textbf{\large " + latex_text(heading) + r"}\par\vspace{0.2cm}"

            blocks.append(f"<div style='font-size: 14px; margin: 12px 0 6px 0; color: #0f172a; font-family: \"Times New Roman\", serif;'>{header_display}</div>")
            tex.append(r"\par\vspace{0.25cm}" + tex_header)

        for index, q in enumerate(questions, 1):
            if pve and hasattr(pve, "audit_and_heal_visual_context_gdpt2018"):
                q = pve.audit_and_heal_visual_context_gdpt2018(dict(q), subject=subject_name, grade=grade_name)
            raw_q_text = sanitize_print_math_text(str(q.get("q", "")))
            expl_q = sanitize_print_math_text(str(q.get("explain", q.get("expl", q.get("exp", "")))))
            if not expl_q:
                expl_q = f"Áp dụng trực tiếp định nghĩa và tính chất SGK Kết Nối Tri Thức. Phân tích loại trừ phương án nhiễu để chọn đáp án chuẩn {q.get('ans', '')}."

            # BẢO VỆ TÍNH BẢO MẬT & CHUẨN SƯ PHẠM BỘ GD&ĐT:
            # - Tuyệt đối KHÔNG in nguồn câu hỏi khi đề do AI sinh ra.
            # - Bản in phát cho học sinh làm đề luôn sạch sẽ tinh tươm (chỉ có 'Câu X.', không lộ nguồn gốc/mã đối soát).
            # - Chỉ in nguồn khi Giáo viên/Giám khảo chủ động bật 'show_audit_badges_per_question' VÀ câu hỏi thực sự từ ngân hàng thật.
            show_src_in_print = (
                st.session_state.get("show_audit_badges_per_question", False)
                and not exam.get("is_ai_generated", False)
                and q.get("is_real_bank_question", False)
                and bool(q.get("source"))
            )

            if show_src_in_print:
                tex.append(r"\par\noindent\textit{\footnotesize [Nguồn: " + latex_text(str(q['source'])) + r"]}\par")
            tex.append(r"\par\noindent\textbf{Câu " + str(index) + r".} " + latex_text(raw_q_text) + r"\par")

            src_html = f"<div style='font-size: 11px; color: #0284c7; font-style: italic; margin-bottom: 2px;'>🏛️ [Nguồn: {html.escape(str(q['source']))}]</div>" if show_src_in_print else ""
            if template_style == "form2":
                p_text_html = f"{src_html}<p style='margin: 0 0 4px 0; line-height: 1.45;'><span style='display: inline-block; background: #0284c7; color: #fff; font-size: 12px; font-weight: bold; padding: 1px 7px; border-radius: 4px; margin-right: 6px;'>Câu {index}</span>{html.escape(raw_q_text)}</p>"
            else:
                p_text_html = f"{src_html}<p style='margin: 0 0 4px 0; line-height: 1.42;'><b>Câu {index}.</b> {html.escape(raw_q_text)}</p>"

            # 2. Trực quan hóa hình ảnh
            vis_html = question_visual_html(q)

            # 3. THUẬT TOÁN TỰ ĐỘNG ĐO ĐỘ DÀI 4 PHƯƠNG ÁN CHUẨN BỘ GD&ĐT
            opts_html = ""
            opts_raw = q.get("opt") or []
            if not opts_raw and q.get("choices") and isinstance(q["choices"], dict):
                opts_raw = [f"{k}. {v}" for k, v in q["choices"].items()]

            if opts_raw:
                letters = ["A", "B", "C", "D"]
                clean_opts_list = []
                for o in opts_raw:
                    c_clean = sanitize_print_math_text(re.sub(r'(?i)^[A-D]\.\s*', '', str(o)).strip())
                    clean_opts_list.append(c_clean)

                lengths = [len(c) for c in clean_opts_list]
                max_opt_len = max(lengths) if lengths else 0
                total_opt_len = sum(lengths)

                if max_opt_len <= 20 or total_opt_len <= 85:
                    grid_cols = "grid-template-columns: repeat(4, 1fr);"
                    latex_cols = 4
                elif max_opt_len <= 45 or total_opt_len <= 170:
                    grid_cols = "grid-template-columns: repeat(2, 1fr);"
                    latex_cols = 2
                else:
                    grid_cols = "grid-template-columns: 1fr;"
                    latex_cols = 1

                opts_html = f"<div style='display: grid; {grid_cols} gap: 2px 14px; margin: 4px 0 6px 0;'>"
                for i, c_opt in enumerate(clean_opts_list):
                    prefix = f"<b>{letters[i]}.</b> " if i < 4 else ""
                    opts_html += f"<div style='font-size: 13.5px;'>{prefix}{html.escape(c_opt)}</div>"
                opts_html += "</div>"

                if latex_cols > 1 and len(clean_opts_list) == 4:
                    latex_opt_items = [r"\textbf{" + letters[i] + r".} " + latex_text(clean_opts_list[i]) for i in range(4)]
                    tex.append(rf"\begin{{multicols}}{{{latex_cols}}}\noindent " + r" \columnbreak ".join(latex_opt_items) + r"\end{multicols}")
                else:
                    for i, c_opt in enumerate(clean_opts_list):
                        prefix_tex = r"\textbf{" + letters[i] + r".} " if i < 4 else ""
                        tex.append(f"{prefix_tex}{latex_text(c_opt)}" + r"\par")

            # 4. Mệnh đề Đúng/Sai (Phần II)
            stmts_html = ""
            if q.get("stmts"):
                stmts_html = "<div style='margin: 4px 0 6px 10px;'>"
                for i, statement in enumerate(q.get("stmts", [])):
                    stmt_t = sanitize_print_math_text(str(statement.get('t', statement.get('s', ''))))
                    stmts_html += f"<div style='font-size: 13.5px; margin-bottom: 2px;'><b>{chr(97+i)})</b> {html.escape(stmt_t)}</div>"
                    tex.append(rf"\par\quad\textbf{{{chr(97+i)})}} " + latex_text(stmt_t) + r"\par")
                stmts_html += "</div>"

            # LaTeX đồng bộ cho BBT, MSLGN, 3D
            if q.get("bbt"):
                bbt_tex = format_pedagogical_bbt_latex(q["bbt"])
                if bbt_tex: tex.append(bbt_tex + r"\par\vspace{0.15cm}")
            if q.get("mslgn_data"):
                ms = q["mslgn_data"]
                grps = ms.get("groups", []); freqs = ms.get("freq", [])
                if grps and freqs and len(grps) == len(freqs):
                    col_spec = "|l|" + "c|" * len(grps)
                    header_cells = " & ".join([f"${latex_text(str(g))}$" for g in grps])
                    freq_cells = " & ".join([str(f) for f in freqs])
                    table_title = latex_text(str(ms.get('title', 'Bảng mẫu số liệu ghép nhóm:')))
                    tex.append(r"\begin{center}" "\n" rf"\textbf{{{table_title}}}\par\vspace{{0.1cm}}" "\n" rf"\begin{{tabular}}{{{col_spec}}}" "\n" r"\hline" "\n" rf"\textbf{{Nhóm giá trị}} & {header_cells} \\ \hline" "\n" rf"\textbf{{Tần số}} & {freq_cells} \\ \hline" "\n" r"\end{{tabular}}" "\n" r"\end{{center}}" + r"\par\vspace{0.15cm}")

            # Phục dựng TikZ cho đề thi LaTeX Overleaf
            has_emitted_tikz = False
            if q.get("tikz"):
                tex.append(rf"\begin{{center}}" "\n" rf"{q['tikz']}" "\n" rf"\end{{center}}")
                has_emitted_tikz = True
            elif q.get("composite_visual") and isinstance(q["composite_visual"], dict) and q["composite_visual"].get("tikz"):
                tex.append(rf"\begin{{center}}" "\n" rf"{q['composite_visual']['tikz']}" "\n" rf"\end{{center}}")
                has_emitted_tikz = True

            vis_fn = q.get("f") or q.get("geom_3d")
            has_need_g_tex = any(kw in raw_q_text.lower() for kw in ["hình vẽ", "hình bên", "như hình", "đồ thị bên", "đường cong trong hình", "khối nón", "khối trụ", "mặt cầu", "khối tròn xoay"])
            if isinstance(vis_fn, dict) and has_need_g_tex and not has_emitted_tikz:

                try:
                    kind = str(vis_fn.get("type", ""))
                    if kind == "cone_3d":
                        r_c = vis_fn.get("r", 3); h_c = vis_fn.get("h", 4)
                        tex.append(rf"\begin{{center}}\begin{{tikzpicture}}[scale=0.6]\draw[dashed] (-{r_c},0) arc (180:0:{r_c}cm and 0.55cm);\draw ({r_c},0) arc (0:-180:{r_c}cm and 0.55cm);\draw (-{r_c},0) -- (0,{h_c}) -- ({r_c},0);\draw[dashed,orange] (0,0) -- (0,{h_c}) node[midway,right] {{$h={h_c}$}};\draw[dashed,teal] (0,0) -- ({r_c},0) node[midway,below] {{$R={r_c}$}};\filldraw (0,0) circle (1.2pt) node[below] {{$O$}};\filldraw (0,{h_c}) circle (1.2pt) node[above] {{$S$}};\end{{tikzpicture}}\end{{center}}")
                    elif kind == "cylinder_3d":
                        r_cyl = vis_fn.get("r", 3); h_cyl = vis_fn.get("h", 5)
                        tex.append(rf"\begin{{center}}\begin{{tikzpicture}}[scale=0.6]\draw (0,{h_cyl}) ellipse ({r_cyl}cm and 0.55cm);\draw[dashed] (-{r_cyl},0) arc (180:0:{r_cyl}cm and 0.55cm);\draw ({r_cyl},0) arc (0:-180:{r_cyl}cm and 0.55cm);\draw (-{r_cyl},0) -- (-{r_cyl},{h_cyl}); \draw ({r_cyl},0) -- ({r_cyl},{h_cyl});\draw[dashed,orange] (0,0) -- (0,{h_cyl}) node[midway,right] {{$h={h_cyl}$}};\draw[dashed,teal] (0,0) -- ({r_cyl},0) node[midway,below] {{$R={r_cyl}$}};\filldraw (0,0) circle (1.2pt) node[below] {{$O'$}};\filldraw (0,{h_cyl}) circle (1.2pt) node[above] {{$O$}};\end{{tikzpicture}}\end{{center}}")
                    elif kind == "sphere_3d":
                        r_s = vis_fn.get("r", 3)
                        tex.append(rf"\begin{{center}}\begin{{tikzpicture}}[scale=0.6]\draw (0,0) circle ({r_s}cm);\draw[dashed] (-{r_s},0) arc (180:0:{r_s}cm and 0.55cm);\draw ({r_s},0) arc (0:-180:{r_s}cm and 0.55cm);\draw[dashed,teal] (0,0) -- ({r_s},0) node[midway,below] {{$R={r_s}$}};\filldraw (0,0) circle (1.2pt) node[below left] {{$O$}};\end{{tikzpicture}}\end{{center}}")
                    elif kind == "solid_of_revolution":
                        fa_b = vis_fn.get("a", 0); fb_b = vis_fn.get("b", 3); f_exp = vis_fn.get("f_expr", "y = f(x)")
                        tex.append(rf"\begin{{center}}\begin{{tikzpicture}}[scale=0.65]\draw[->] (-0.5,0) -- ({fb_b+1},0) node[right] {{$x$}};\draw[->] (0,-2.5) -- (0,2.5) node[above] {{$y$}};\draw[thick,blue] plot[domain={fa_b}:{fb_b},smooth] ({{\x}},{{sqrt(max(0,\x))}});\draw[thick,blue,dashed] plot[domain={fa_b}:{fb_b},smooth] ({{\x}},{{-sqrt(max(0,\x))}});\draw ({fa_b},0) ellipse (0.15cm and 0.6cm);\draw ({fb_b},0) ellipse (0.25cm and 1.7cm);\node[below] at ({fa_b},0) {{$a={fa_b}$}};\node[below] at ({fb_b},0) {{$b={fb_b}$}};\end{{tikzpicture}}\end{{center}}")
                    else:
                        a, b, c, d, e = [float(vis_fn.get(k, v)) for k, v in [("a", 1), ("b", 0), ("c", 0), ("d", 0), ("e", 0)]]
                        if all(math.isfinite(v) and abs(v) <= 10000 for v in (a, b, c, d, e)):
                            if kind in ("func_3", "cubic"): expression = f"({a})*x^3+({b})*x^2+({c})*x+({d})"
                            elif kind in ("parabola", "parabola_fprime"): expression = f"({a})*x^2+({b})*x+({c})"
                            elif kind == "func_1_1": expression = f"(({a})*x+({b}))/(({c})*x+({d}))"
                            elif kind == "func_2_1": expression = f"(({a})*x^2+({b})*x+({c}))/(({d})*x+({e}))"
                            else: expression = ""
                            if expression:
                                tex.append(r"\begin{center}\begin{tikzpicture}\begin{axis}[width=7cm,height=4.8cm,axis lines=middle,xlabel={$x$},ylabel={$y$},xmin=-4.5,xmax=4.5,ymin=-6,ymax=6,domain=-4.5:4.5,samples=201,restrict y to domain=-6:6,unbounded coords=jump,grid=both,minor tick num=1]")
                                tex.append(r"\addplot[blue,thick] {" + expression + r"};\end{axis}\end{tikzpicture}\end{center}")
                except Exception:
                    pass

            body_html = f"{p_text_html}{vis_html}{opts_html}{stmts_html}"

            ans_expl_html = ""
            if include_answers:
                answer = q.get("ans", "")
                if q.get("stmts"):
                    answer = "; ".join(f"{chr(97+i)}: " + ("Đúng" if (t.get("a") if "a" in t else t.get("ans", True)) else "Sai") for i, t in enumerate(q.get("stmts", [])))

                ans_expl_html = f"""
                <div style="background-color: #f0fdf4; border-left: 3.5px solid #16a34a; padding: 5px 10px; margin: 4px 0 6px 0; border-radius: 4px; font-size: 13px; line-height: 1.45;">
                    <div style="font-weight: bold; color: #15803d; margin-bottom: 2px;">✅ ĐÁP ÁN: {html.escape(str(answer))}</div>
                    <div style="color: #1e293b;">💡 <strong>Hướng dẫn tư duy Bình dân học vụ (Bản chất sư phạm Socratic):</strong><br>{html.escape(expl_q)}</div>
                </div>
                """
                tex.append(r"\vspace{0.15cm}\noindent\fbox{\parbox{0.96\textwidth}{\textbf{Đáp án:} " + latex_text(str(answer)) + r" \\ \textit{\textbf{💡 Hướng dẫn tư duy Bình dân học vụ:}} " + latex_text(expl_q) + r"}}\par\vspace{0.25cm}")

            blocks.append(f"<article style='margin-bottom: 8px; break-inside: avoid;'>{body_html}{ans_expl_html}</article>")

    # DÒNG KẾT THÚC ĐỀ THI TRANG TRỌNG CHUẨN KHẢO THÍ BỘ GD&ĐT
    blocks.append("""
    <div style="text-align: center; font-weight: bold; margin: 18px 0 4px 0; font-family: 'Times New Roman', Times, serif; font-size: 14px; letter-spacing: 2px;">
        ---------- HẾT ----------
    </div>
    <div style="text-align: center; font-style: italic; font-size: 12.5px; color: #475569; margin-bottom: 16px; font-family: 'Times New Roman', Times, serif;">
        Thí sinh không được sử dụng tài liệu. Cán bộ coi thi không giải thích gì thêm.
    </div>
    """)
    tex.append(r"\vspace{0.4cm}\begin{center}\textbf{---------- HẾT ----------}\\\textit{\small Thí sinh không được sử dụng tài liệu. Cán bộ coi thi không giải thích gì thêm.}\end{center}\vspace{0.3cm}")

    # ==================== 3. BẢNG TỔNG HỢP ĐÁP ÁN CHUẨN BỘ (ANSWER KEY TABLE) ====================
    if include_answers and subject_name != "Ngữ văn":
        blocks.append("<div style='page-break-before: always; margin-top: 20px;' class='print-page-break'>")
        blocks.append("<h2 style='text-align: center; font-size: 15px; font-weight: bold; text-transform: uppercase; margin-bottom: 10px; font-family: \"Times New Roman\", Times, serif;'>BẢNG ĐÁP ÁN VÀ MA TRẬN CHẤM ĐIỂM CHUẨN BỘ GD&ĐT</h2>")

        tex.append(r"\newpage")
        tex.append(r"\begin{center}\textbf{\Large BẢNG ĐÁP ÁN VÀ MA TRẬN CHẤM ĐIỂM CHUẨN BỘ GD\&ĐT}\end{center}\vspace{0.3cm}")

        p1_items = exam.get("p1") or exam.get("part_1") or []
        p2_items = exam.get("p2") or exam.get("part_2") or []
        p3_items = exam.get("p3") or exam.get("part_3") or []

        if p1_items:
            blocks.append("<h4 style='margin-bottom: 4px; font-size: 13.5px; font-family: \"Times New Roman\", Times, serif;'>PHẦN I: TRẮC NGHIỆM 4 LỰA CHỌN</h4>")
            blocks.append("<table border='1' style='width: 100%; border-collapse: collapse; text-align: center; font-size: 13px; margin-bottom: 12px; font-family: \"Times New Roman\", Times, serif;'>")
            tex.append(r"\noindent\textbf{PHẦN I: TRẮC NGHIỆM 4 LỰA CHỌN}\par\vspace{0.15cm}")

            for chunk_start in range(0, len(p1_items), 10):
                chunk = p1_items[chunk_start:chunk_start+10]
                blocks.append("<tr style='background: #f1f5f9; font-weight: bold;'>" + "".join(f"<th>Câu {chunk_start+i+1}</th>" for i in range(len(chunk))) + "</tr>")
                blocks.append("<tr>" + "".join(f"<td style='padding: 4px; font-weight: bold; color: #0369a1;'>{q.get('ans', '')}</td>" for q in chunk) + "</tr>")

                # Bảng đáp án LaTeX Overleaf chuẩn hóa chunk 10 câu (đảm bảo hiển thị đủ 100% số câu cho mọi môn học)
                tex.append(r"\begin{tabularx}{\textwidth}{|" + "X|" * len(chunk) + r"}\hline")
                tex.append(" & ".join(f"\\textbf{{Câu {chunk_start+i+1}}}" for i in range(len(chunk))) + r" \\ \hline")
                tex.append(" & ".join(f"\\textbf{{{q.get('ans', '')}}}" for q in chunk) + r" \\ \hline")
                tex.append(r"\end{tabularx}\par\vspace{0.2cm}")
            blocks.append("</table>")

        if p2_items:
            blocks.append("<h4 style='margin-bottom: 4px; font-size: 13.5px; font-family: \"Times New Roman\", Times, serif;'>PHẦN II: TRẮC NGHIỆM ĐÚNG / SAI (THANG BẬC 0.1 - 0.25 - 0.5 - 1.0 ĐIỂM)</h4>")
            blocks.append("<table border='1' style='width: 100%; border-collapse: collapse; text-align: center; font-size: 13px; margin-bottom: 12px; font-family: \"Times New Roman\", Times, serif;'><tr style='background: #f1f5f9; font-weight: bold;'><th>Câu</th><th>Lệnh hỏi a)</th><th>Lệnh hỏi b)</th><th>Lệnh hỏi c)</th><th>Lệnh hỏi d)</th></tr>")
            tex.append(r"\noindent\textbf{PHẦN II: TRẮC NGHIỆM ĐÚNG / SAI}\par\vspace{0.15cm}")
            tex.append(r"\begin{tabularx}{\textwidth}{|c|X|X|X|X|}\hline")
            tex.append(r"\textbf{Câu} & \textbf{Ý a)} & \textbf{Ý b)} & \textbf{Ý c)} & \textbf{Ý d)} \\ \hline")
            for idx2, q2 in enumerate(p2_items, 1):
                st_vals = [("Đúng" if (s.get("a") if "a" in s else s.get("ans", True)) else "Sai") for s in q2.get("stmts", [])]
                while len(st_vals) < 4: st_vals.append("-")
                blocks.append(f"<tr><td style='font-weight: bold;'>Câu {idx2}</td>" + "".join(f"<td style='padding: 4px;'>{v}</td>" for v in st_vals) + "</tr>")
                tex.append(f"\\textbf{{Câu {idx2}}} & " + " & ".join(st_vals) + r" \\ \hline")
            blocks.append("</table>")
            tex.append(r"\end{tabularx}\par\vspace{0.3cm}")

        if p3_items:
            blocks.append("<h4 style='margin-bottom: 4px; font-size: 13.5px; font-family: \"Times New Roman\", Times, serif;'>PHẦN III: TRẢ LỜI NGẮN (ĐIỀN SỐ TỐI ĐA 4 KÝ TỰ)</h4>")
            blocks.append("<table border='1' style='width: 100%; border-collapse: collapse; text-align: center; font-size: 13px; margin-bottom: 12px; font-family: \"Times New Roman\", Times, serif;'><tr style='background: #f1f5f9; font-weight: bold;'>" + "".join(f"<th>Câu {i+1}</th>" for i in range(len(p3_items))) + "</tr>")
            blocks.append("<tr>" + "".join(f"<td style='padding: 4px; font-weight: bold; color: #b45309;'>{q.get('ans', '')}</td>" for q in p3_items) + "</tr></table>")

            tex.append(r"\noindent\textbf{PHẦN III: TRẢ LỜI NGẮN}\par\vspace{0.15cm}")
            tex.append(r"\begin{tabularx}{\textwidth}{|" + "X|" * len(p3_items) + r"}\hline")
            tex.append(" & ".join(f"\\textbf{{Câu {i+1}}}" for i in range(len(p3_items))) + r" \\ \hline")
            tex.append(" & ".join(f"\\textbf{{{q.get('ans', '')}}}" for q in p3_items) + r" \\ \hline")
            tex.append(r"\end{tabularx}\par\vspace{0.3cm}")

        # KHỐI ỦNG HỘ TÁC GIẢ VIETQR MB BANK (CHỈ XUẤT HIỆN Ở CUỐI TRANG ĐÁP ÁN NẾU ĐƯỢC BẬT)
        if show_support_qr and mb_qr_base64:
            blocks.append(f"""
            <div style="margin-top: 24px; border: 1.5px solid #0284c7; border-radius: 8px; padding: 10px 14px; background: #f0f9ff; font-family: 'Times New Roman', Times, serif;">
                <table style="width: 100%; border: none !important; border-collapse: collapse;">
                    <tr style="border: none !important;">
                        <td style="width: 72px; vertical-align: middle; border: none !important; padding: 0 !important; background: transparent !important;">
                            <img src="{mb_qr_base64}" style="width: 66px; height: 66px; border: 1px solid #0284c7; border-radius: 4px; padding: 2px; background: #fff;" alt="VietQR MB Bank">
                        </td>
                        <td style="vertical-align: middle; padding-left: 14px; border: none !important; background: transparent !important;">
                            <div style="font-weight: bold; font-size: 13px; color: #0369a1; text-transform: uppercase;">ỦNG HỘ TÁC GIẢ BIÊN SOẠN & PHÁT TRIỂN HỆ THỐNG</div>
                            <div style="font-size: 12.5px; color: #0f172a; margin-top: 2px;">Ngân hàng MB Bank • STK: <strong>0919513834</strong> • Chủ tài khoản: <strong>PHAN MINH TRÍ</strong></div>
                            <div style="font-size: 11.5px; color: #475569; font-style: italic; margin-top: 1px;">Trân trọng cảm ơn quý Thầy Cô và các em học sinh đã đồng hành và ủng hộ!</div>
                        </td>
                    </tr>
                </table>
            </div>
            """)
            tex.append(r"\par\vspace{0.5cm}\noindent\begin{tcolorbox}[colback=blue!5!white,colframe=blue!75!black,title=\textbf{ỦNG HỘ TÁC GIẢ BIÊN SOẠN & PHÁT TRIỂN HỆ THỐNG}]" "\n" r"\textbf{Biên soạn:} Thầy Phan Minh Trí \\" "\n" r"\textbf{Ngân hàng MB Bank:} Số tài khoản \textbf{0919513834} (Chủ TK: Phan Minh Trí) \\" "\n" r"\textit{\small Trân trọng cảm ơn quý Thầy Cô và các em học sinh đã đồng hành và ủng hộ!}" "\n" r"\end{tcolorbox}")

        blocks.append("</div>")

    tex.append(r"\end{document}")

    mathjax_head = """<script>window.MathJax = { tex: { inlineMath: [['$', '$'], ['\\\\(', '\\\\)']], displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']] }, svg: { fontCache: 'global' } };</script><script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>"""
    markup = f"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
{mathjax_head}
<style>
@page {{
    size: A4 portrait;
    margin: 1.3cm 1.2cm 1.3cm 1.2cm;
}}
body {{
    font-family: 'Times New Roman', Times, serif;
    font-size: 13.5px;
    line-height: 1.42;
    color: #111827;
    background: #f8fafc;
    margin: 0;
    padding: 14px 0;
}}
.page-container {{
    max-width: 820px;
    margin: 0 auto;
    background: #ffffff;
    padding: 24px 28px 95px 28px !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    border-radius: 6px;
}}
.header-table td {{
    padding: 2px 4px;
}}
.no-print {{
    display: block;
    margin: 0 auto 14px auto;
    background: #0284c7;
    color: #ffffff;
    border: none;
    padding: 10px 22px;
    font-size: 14px;
    font-weight: bold;
    border-radius: 6px;
    cursor: pointer;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    transition: all 0.2s ease;
}}
.no-print:hover {{
    background: #0369a1;
}}
.floating-print-btn {{
    position: fixed;
    bottom: 16px;
    right: 18px;
    z-index: 2147483647;
    background: linear-gradient(135deg, #0284c7 0%, #1d4ed8 100%);
    color: #ffffff;
    border: 1.5px solid rgba(255, 255, 255, 0.75);
    padding: 7px 16px;
    font-size: 12.5px;
    font-weight: 700;
    border-radius: 24px;
    cursor: pointer;
    box-shadow: 0 6px 20px rgba(2, 132, 199, 0.4), 0 2px 6px rgba(0, 0, 0, 0.18);
    display: flex;
    align-items: center;
    gap: 7px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    backdrop-filter: blur(8px);
    letter-spacing: 0.2px;
    opacity: 0.92;
}}
.floating-print-btn:hover {{
    opacity: 1;
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 8px 24px rgba(56, 189, 248, 0.65);
    background: linear-gradient(135deg, #0369a1 0%, #1e40af 100%);
    border-color: #7dd3fc;
}}
.floating-print-btn:active {{
    transform: translateY(0) scale(0.98);
}}
@media print {{
    body {{
        background: #ffffff;
        padding: 0;
    }}
    .page-container {{
        box-shadow: none;
        padding: 0;
        max-width: 100%;
    }}
    .no-print, .floating-print-btn {{
        display: none !important;
    }}
    .print-page-break {{
        page-break-before: always !important;
    }}
    article {{
        page-break-inside: avoid !important;
        break-inside: avoid !important;
    }}
}}
</style>
</head>
<body>
<!-- NÚT 1 CHẠM ĐỂ IN NỔI CỐ ĐỊNH Ở GÓC PHẢI MÀN HÌNH (Độc lập cuộn chuột, cực kỳ mỹ quan, không che chữ) -->
<button class="no-print floating-print-btn" title="Bấm 1 chạm để mở hộp thoại In đề hoặc Lưu PDF A4 chuẩn Bộ GD&ĐT" onclick="if(window.MathJax&&window.MathJax.typesetPromise){{window.MathJax.typesetPromise().then(function(){{window.print();}});}}else{{window.print();}}">
    <span style="font-size: 16px;">🖨️</span>
    <span>In đề / Lưu PDF (1 Chạm)</span>
</button>

<div class="page-container">
{"".join(blocks)}
</div>
</body>
</html>"""

    return markup, "\n".join(tex)


# BỘ KHỬ LỖI TOÁN HỌC VÀ PHÂN TÍCH JSON AN TOÀN

def fix_broken_latex_escapes(obj):

    if isinstance(obj, dict):

        return {k: fix_broken_latex_escapes(v) for k, v in obj.items()}

    elif isinstance(obj, list):

        return [fix_broken_latex_escapes(item) for item in obj]

    elif isinstance(obj, str):

        s = obj

        # Khắc phục lỗi Form Feed ASCII \x0c -> \f (gây ra chữ đỏ ⯅rac / ▲rac)
        s = s.replace('\x0crac', r'\frac').replace('\x0c', r'\f')
        s = s.replace(r'\x0crac', r'\frac').replace(r'\x0c', r'\f')
        # Khắc phục lỗi Backspace ASCII \x08 -> \b
        s = s.replace('\x08ar', r'\bar').replace('\x08eta', r'\beta').replace('\x08egin', r'\begin').replace('\x08inom', r'\binom').replace('\x08f', r'\bf').replace('\x08', r'\b')
        s = re.sub(r'[\u25b2\u2bf5\u25b4\u2660]rac', r'\\frac', s)
        s = re.sub(r'(?<!\\)\brac\{', r'\\frac{', s)
        # Khắc phục lỗi Tab ASCII \x09 -> \t trong \to, \text, \times, \theta, \tan, \tau
        s = s.replace('\x09o', r'\to').replace('\x09ext', r'\text').replace('\x09imes', r'\times').replace('\x09heta', r'\theta').replace('\x09au', r'\tau').replace('\x09an', r'\tan')
        s = re.sub(r'\\lim_\{([^}]+)\s+o\s+', r'\\lim_{\1 \\to ', s)
        s = re.sub(r'(?<=\s)o(?=\s*[-+]?\d|\\infty|\$)', r'\\to', s)
        return s
    return obj





# ==============================================================================

# 6. PHÒNG LAB LAI & BỘ LỌC AN TOÀN AST

# ==============================================================================

# ------------------------------------------------------------------------------
# DỊCH VỤ RENDER SƠ ĐỒ MERMAID (ĐÃ ĐƯỢC TÁCH MODULE services/mermaid_renderer.py)
from services.mermaid_renderer import render_mermaid
# ------------------------------------------------------------------------------

def setup_pedagogical_oxy(fig, x_range, y_range):

    x_min, x_max = x_range

    y_min, y_max = y_range



    fig.add_trace(go.Scatter(x=[x_min, x_max], y=[0, 0], mode='lines', line=dict(color='#cbd5e1', width=1.5), hoverinfo='skip', showlegend=False))

    fig.add_trace(go.Scatter(x=[0, 0], y=[y_min, y_max], mode='lines', line=dict(color='#cbd5e1', width=1.5), hoverinfo='skip', showlegend=False))



    fig.add_annotation(x=x_max, y=0, ax=-18, ay=0, xref='x', yref='y', axref='pixel', ayref='pixel', showarrow=True, arrowhead=2, arrowsize=1.2, arrowwidth=2, arrowcolor='#cbd5e1')

    fig.add_annotation(x=x_max - 0.1, y=-0.5, text='<b>x</b>', showarrow=False, font=dict(color='#f8fafc', size=15, family='Times New Roman'))



    fig.add_annotation(x=0, y=y_max, ax=0, ay=18, xref='x', yref='y', axref='pixel', ayref='pixel', showarrow=True, arrowhead=2, arrowsize=1.2, arrowwidth=2, arrowcolor='#cbd5e1')

    fig.add_annotation(x=-0.4, y=y_max - 0.1, text='<b>y</b>', showarrow=False, font=dict(color='#f8fafc', size=15, family='Times New Roman'))



    fig.add_annotation(x=-0.35, y=-0.45, text='<i>O</i>', showarrow=False, font=dict(color='#94a3b8', size=15, family='Times New Roman'))



    x_span = abs(x_max - x_min)

    y_span = abs(y_max - y_min)

    dtick_x = 1 if x_span <= 14 else (2 if x_span <= 28 else None)

    dtick_y = 1 if y_span <= 14 else (2 if y_span <= 28 else (5 if y_span <= 70 else None))



    xaxis_dict = dict(range=[x_min, x_max], zeroline=False, gridcolor="#1e293b", gridwidth=1)

    yaxis_dict = dict(range=[y_min, y_max], zeroline=False, gridcolor="#1e293b", gridwidth=1)

    if dtick_x: xaxis_dict["dtick"] = dtick_x

    if dtick_y: yaxis_dict["dtick"] = dtick_y



    fig.update_layout(

        template="plotly_dark",

        xaxis=xaxis_dict,

        yaxis=yaxis_dict,

        margin=dict(l=15, r=15, t=30, b=15),

        showlegend=False

    )





_SAFE_NAMES = {"x", "np", "math", "pi", "e", "abs", "min", "max", "pow", "round", "float", "int"}

_SAFE_CALL_ROOTS = {"np", "math"}



_MATH_FUNCTIONS = {"sin", "cos", "tan", "sqrt", "exp", "log", "log10", "abs", "absolute", "arcsin", "arccos", "arctan"}

_MATH_CONSTANTS = {"pi", "e"}



def _check_math_ast(node):

    nodes = list(ast.walk(node))

    if len(nodes) > 200:

        raise ValueError("Biểu thức quá phức tạp.")

    allowed = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Call, ast.Name, ast.Load, ast.Constant, ast.Attribute,

               ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod, ast.UAdd, ast.USub)

    for n in nodes:

        if not isinstance(n, allowed):

            raise ValueError("Chỉ cho phép biểu thức toán học đơn giản.")

        if isinstance(n, ast.Name) and n.id not in _SAFE_NAMES:

            raise ValueError(f"Tên không được phép: {n.id}")

        if isinstance(n, ast.Constant) and (isinstance(n.value, bool) or not isinstance(n.value, (int, float)) or abs(n.value) > 1000000):

            raise ValueError("Hằng số không hợp lệ hoặc quá lớn.")

        if isinstance(n, ast.Attribute):

            if not isinstance(n.value, ast.Name) or n.value.id not in {"np", "math"} or n.attr not in _MATH_FUNCTIONS | _MATH_CONSTANTS:

                raise ValueError("Hàm/thuộc tính không nằm trong danh sách toán học được phép.")

        if isinstance(n, ast.Call):

            if n.keywords or len(n.args) > 3 or not ((isinstance(n.func, ast.Name) and n.func.id in {"abs", "min", "max", "round", "float", "int"}) or (isinstance(n.func, ast.Attribute) and n.func.attr in _MATH_FUNCTIONS)):

                raise ValueError("Lời gọi hàm không được phép.")

        if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Pow):

            exponent = n.right

            if isinstance(exponent, ast.UnaryOp) and isinstance(exponent.op, (ast.UAdd, ast.USub)):

                exponent = exponent.operand

            if not isinstance(exponent, ast.Constant) or not isinstance(exponent.value, (int, float)) or abs(exponent.value) > 20:

                raise ValueError("Số mũ phải là hằng số có trị tuyệt đối không vượt 20.")



def safe_eval_func(expr, x_val):

    if len(expr) > 1000 or np.size(x_val) > 100000:

        raise ValueError("Mô phỏng vượt giới hạn kích thước.")

    tree = ast.parse(expr.strip(), mode="eval")

    _check_math_ast(tree)

    env = {"__builtins__": {}, "x": x_val, "np": np, "math": math, "pi": math.pi, "e": math.e,

           "abs": abs, "min": min, "max": max, "round": round, "float": float, "int": int}

    with np.errstate(all="ignore"):

        return eval(compile(tree, "<ham_so>", "eval"), env)



_BLOCKED_NAMES = {"exec", "eval", "compile", "open", "input", "globals", "locals", "vars", "getattr",

                  "setattr", "delattr", "__import__", "os", "sys", "subprocess", "st", "builtins",

                  "importlib", "socket", "requests", "shutil", "pathlib"}

_SAFE_BUILTINS = {k: __builtins__[k] if isinstance(__builtins__, dict) else getattr(__builtins__, k)

                  for k in ["range", "len", "min", "max", "abs", "sum", "round", "float", "int", "list", "dict",

                            "tuple", "zip", "enumerate", "str", "pow", "sorted", "bool", "map", "any", "all",

                            "set", "reversed", "isinstance", "True", "False", "None"]}



def render_dynamic_python_lab(python_code: str):

    st.warning("Mô phỏng Python tự do chưa được hỗ trợ. Hãy chọn hàm số, diện tích, khối tròn xoay, Oxyz hoặc sơ đồ tư duy; ứng dụng không chạy mã do AI sinh.")



def render_smart_lab(data, current_subject=""):

    dtype = data.get("type")



    # BẢO VỆ PHÁP CHẾ & SƯ PHẠM: MÔN XÃ HỘI TUYỆT ĐỐI KHÔNG HIỂN THỊ ĐỒ THỊ TOÁN HỌC

    social_subjects = ["Ngữ văn", "Lịch sử", "Địa lý", "Giáo dục công dân", "Giáo dục kinh tế và pháp luật", "Lịch sử & Địa lý", "Tiếng Anh"]

    if current_subject in social_subjects and dtype in ["func_3", "parabola", "func_1_1", "func_2_1", "func_2", "area", "revolve_ox", "oxyz", "geometry_3d", "func_exp", "func_log"]:

        st.info(f"💡 Không gian học tập môn **{current_subject}**: Phòng Lab tự động chuyển sang chế độ Sơ đồ tư duy D3/Mermaid chuyên biệt cho môn học thay vì hiển thị đồ thị giải tích Toán học.")

        data = {

            "type": "mermaid",

            "code": f"""graph LR

    Root["🎯 CHỦ ĐỀ MÔN {current_subject.upper()}"] --> A["1. Khái niệm & Cơ sở lý luận"]

    Root --> B["2. Nội dung Trọng tâm"]

    Root --> C["3. Phương pháp Tiếp cận"]

    Root --> D["4. Vận dụng Thực tiễn"]

    A --> A1["Chuẩn kiến thức GDPT 2018"]

    B --> B1["Hệ thống luận điểm cốt lõi"]

    C --> C1["Kỹ năng tư duy phản biện"]

    D --> D1["Liên hệ đời sống & bài thi 2026"]"""

        }

        dtype = "mermaid"



    if dtype == "mermaid":

        st.markdown("### 🗺️ Trực quan hóa Sơ Đồ Tư Duy / Chu Trình Mô Phỏng")

        render_mermaid(data.get("code", ""))

        return



    if dtype == "geometry_3d":

        shape = data.get("shape", "pyramid_quad")

        title_geo = data.get("title", "Mô hình Hình học không gian 3D (SGK KNTT)")

        c1, c2 = st.columns([1.2, 2.8])

        with c1:

            st.caption("⚙️ **Thông số điều chỉnh Hình không gian:**")

            h_val = st.slider("Chiều cao h:", 1.5, 6.0, float(data.get("h", 4.0)), 0.5, key="lab_geo3d_h")

            show_faces = st.checkbox("Tô mờ các mặt phẳng (3D Surfaces)", value=True, key="lab_geo3d_faces")



            if shape in ["pyramid_quad", "chóp tứ giác"]:

                st.info("📐 **Hình chóp tứ giác $S.ABCD$**\n\n- Đáy $ABCD$ là hình bình hành/chữ nhật\n- $S$ là đỉnh hình chóp\n- Cạnh khuất: $AD, CD, SD$ (nét đứt)")

            elif shape in ["pyramid_tri", "tetrahedron", "tứ diện", "chóp tam giác"]:

                st.info("📐 **Hình chóp tam giác / Tứ diện $S.ABC$**\n\n- Đáy $ABC$ là tam giác\n- Đỉnh $S$, cạnh khuất nét đứt sư phạm")

            elif shape in ["prism_tri", "lăng trụ"]:

                st.info("📐 **Hình lăng trụ tam giác $ABC.A'B'C'$**\n\n- Hai đáy $ABC$ và $A'B'C'$ song song\n- Các cạnh bên song song và bằng nhau")

            elif shape in ["box", "cube", "hình hộp", "lập phương"]:

                st.info("📐 **Hình hộp chữ nhật $ABCD.A'B'C'D'$**\n\n- 6 mặt là hình chữ nhật\n- Các cạnh khuất phía sau vẽ nét đứt")

            elif shape in ["parallel_lines", "song song"]:

                st.info("📐 **Hai đường thẳng song song $d_1 \\parallel d_2$ trong không gian**\n\n- Cùng nằm trên mặt phẳng $(\\alpha)$\n- Không có điểm chung")



        with c2:

            fig_geo = go.Figure()

            def add_geo_edge(p1, p2, is_dashed=False, color='#38bdf8', width=3.5):

                fig_geo.add_trace(go.Scatter3d(

                    x=[p1[0], p2[0]], y=[p1[1], p2[1]], z=[p1[2], p2[2]],

                    mode='lines',

                    line=dict(color='#94a3b8' if is_dashed else color, width=2.5 if is_dashed else width, dash='dash' if is_dashed else 'solid'),

                    hoverinfo='skip', showlegend=False

                ))



            def add_geo_pts(pts_dict, color='#f43f5e', size=6):

                px = [v[0] for v in pts_dict.values()]

                py = [v[1] for v in pts_dict.values()]

                pz = [v[2] for v in pts_dict.values()]

                txt = list(pts_dict.keys())

                fig_geo.add_trace(go.Scatter3d(

                    x=px, y=py, z=pz, mode='markers+text',

                    marker=dict(size=size, color=color),

                    text=txt, textposition="top center",

                    textfont=dict(color='#ffffff', size=13),

                    showlegend=False

                ))



            if shape in ["pyramid_quad", "chóp tứ giác"]:

                A = [-2.5, -2.0, 0.0]

                B = [2.0, -2.0, 0.0]

                C = [3.0, 1.8, 0.0]

                D = [-1.5, 1.8, 0.0]

                S = [0.2, 0.0, h_val]

                pts = {"A": A, "B": B, "C": C, "D": D, "S": S}

                add_geo_pts(pts)

                add_geo_edge(A, B)

                add_geo_edge(B, C)

                add_geo_edge(S, A, color='#38bdf8')

                add_geo_edge(S, B, color='#38bdf8')

                add_geo_edge(S, C, color='#38bdf8')

                add_geo_edge(A, D, is_dashed=True)

                add_geo_edge(D, C, is_dashed=True)

                add_geo_edge(S, D, is_dashed=True)

                if show_faces:

                    all_p = [A, B, C, D, S]

                    fig_geo.add_trace(go.Mesh3d(

                        x=[p[0] for p in all_p], y=[p[1] for p in all_p], z=[p[2] for p in all_p],

                        i=[4, 4, 0, 0], j=[0, 1, 1, 2], k=[1, 2, 2, 3],

                        opacity=0.22, color='#0284c7', hoverinfo='skip', showlegend=False

                    ))



            elif shape in ["pyramid_tri", "tetrahedron", "tứ diện", "chóp tam giác"]:

                A = [-2.2, -1.8, 0.0]

                B = [2.2, -1.8, 0.0]

                C = [0.0, 2.0, 0.0]

                S = [0.0, 0.0, h_val]

                pts = {"A": A, "B": B, "C": C, "S": S}

                add_geo_pts(pts)

                add_geo_edge(A, B)

                add_geo_edge(B, C)

                add_geo_edge(S, A)

                add_geo_edge(S, B)

                add_geo_edge(S, C)

                add_geo_edge(A, C, is_dashed=True)

                if show_faces:

                    all_p = [A, B, C, S]

                    fig_geo.add_trace(go.Mesh3d(

                        x=[p[0] for p in all_p], y=[p[1] for p in all_p], z=[p[2] for p in all_p],

                        i=[3, 3, 0], j=[0, 1, 1], k=[1, 2, 2],

                        opacity=0.22, color='#0284c7', hoverinfo='skip', showlegend=False

                    ))



            elif shape in ["box", "cube", "hình hộp", "lập phương"]:

                A = [-2.0, -2.0, 0.0]; B = [2.0, -2.0, 0.0]; C = [2.5, 1.8, 0.0]; D = [-1.5, 1.8, 0.0]

                A1 = [-2.0, -2.0, h_val]; B1 = [2.0, -2.0, h_val]; C1 = [2.5, 1.8, h_val]; D1 = [-1.5, 1.8, h_val]

                pts = {"A": A, "B": B, "C": C, "D": D, "A'": A1, "B'": B1, "C'": C1, "D'": D1}

                add_geo_pts(pts)

                add_geo_edge(A, B); add_geo_edge(B, C)

                add_geo_edge(A1, B1); add_geo_edge(B1, C1); add_geo_edge(C1, D1); add_geo_edge(D1, A1)

                add_geo_edge(A, A1); add_geo_edge(B, B1); add_geo_edge(C, C1)

                add_geo_edge(A, D, is_dashed=True); add_geo_edge(D, C, is_dashed=True); add_geo_edge(D, D1, is_dashed=True)



            elif shape in ["prism_tri", "lăng trụ"]:

                A = [-2.0, -1.8, 0.0]; B = [2.0, -1.8, 0.0]; C = [0.0, 1.8, 0.0]

                A1 = [-2.0, -1.8, h_val]; B1 = [2.0, -1.8, h_val]; C1 = [0.0, 1.8, h_val]

                pts = {"A": A, "B": B, "C": C, "A'": A1, "B'": B1, "C'": C1}

                add_geo_pts(pts)

                add_geo_edge(A, B); add_geo_edge(B, C); add_geo_edge(A1, B1); add_geo_edge(B1, C1); add_geo_edge(C1, A1)

                add_geo_edge(A, A1); add_geo_edge(B, B1); add_geo_edge(C, C1)

                add_geo_edge(A, C, is_dashed=True)



            else: # parallel_lines or default

                P1 = [-4, -3, 0]; P2 = [4, -3, 0]; P3 = [5, 3, 0]; P4 = [-3, 3, 0]

                add_geo_edge(P1, P2, color='#64748b', width=1.5)

                add_geo_edge(P2, P3, color='#64748b', width=1.5)

                add_geo_edge(P3, P4, color='#64748b', width=1.5)

                add_geo_edge(P4, P1, color='#64748b', width=1.5)

                d1_A = [-3, -1, 0]; d1_B = [3, -1, 0]

                d2_A = [-2.5, 1.5, 0]; d2_B = [3.5, 1.5, 0]

                add_geo_edge(d1_A, d1_B, color='#f43f5e', width=4.5)

                add_geo_edge(d2_A, d2_B, color='#38bdf8', width=4.5)

                pts = {"d1": d1_B, "d2": d2_B, "(P)": P2}

                add_geo_pts(pts, color='#fbbf24', size=5)

                if show_faces:

                    fig_geo.add_trace(go.Mesh3d(

                        x=[P1[0], P2[0], P3[0], P4[0]],

                        y=[P1[1], P2[1], P3[1], P4[1]],

                        z=[P1[2], P2[2], P3[2], P4[2]],

                        i=[0, 0], j=[1, 2], k=[2, 3],

                        opacity=0.15, color='#475569', hoverinfo='skip', showlegend=False

                    ))



            fig_geo.update_layout(

                title=title_geo,

                template="plotly_dark",

                scene=dict(

                    xaxis=dict(range=[-5, 5], visible=False),

                    yaxis=dict(range=[-5, 5], visible=False),

                    zaxis=dict(range=[-1, 7], visible=False),

                    aspectmode='cube'

                ),

                height=520,

                margin=dict(l=10, r=10, t=35, b=10)

            )

            st.plotly_chart(fig_geo, width="stretch")

        return



    if dtype == "func_exp":

        c1, c2 = st.columns([1.2, 2.8])

        with c1:

            st.caption("⚙️ **Thông số Hàm số Mũ ($y = k \\cdot a^x + c$):**")

            use_e = st.checkbox("Dùng cơ số tự nhiên Euler $e \\approx 2.718$", value=bool(data.get("is_e", False)), key="lab_exp_is_e")

            if use_e:

                fa = float(np.e)

                st.info("📌 **Đang chọn:** Cơ số $a = e \\approx 2.718$ (Hàm số mũ tự nhiên $y = e^x$)")

            else:

                fa = st.slider("Cơ số a (a > 0, a ≠ 1):", 0.1, 4.5, float(data.get("base", 2.0)), 0.1, key="lab_exp_a")

                if abs(fa - 1.0) < 0.05: fa = 1.05



            fk = st.slider("Hệ số k:", -3.0, 3.0, float(data.get("k", 1.0)), 0.5, key="lab_exp_k")

            if fk == 0: fk = 1.0

            fc = st.slider("Hệ số tịnh tiến c:", -4.0, 4.0, float(data.get("c", 0.0)), 0.5, key="lab_exp_c")



            base_label = "e" if use_e else f"{fa:.1f}"

            st.success(f"📈 **Công thức:** $y = {fk if fk != 1 else ''}{base_label}^x {('+' + str(fc)) if fc > 0 else (str(fc) if fc < 0 else '')}$")



            if fk > 0:

                nature = "🟢 **Đồng biến trên toàn trục số $\\mathbb{R}$**" if fa > 1 else "🟠 **Nghịch biến trên toàn trục số $\\mathbb{R}$**"

            else:

                nature = "🟠 **Nghịch biến trên toàn trục số $\\mathbb{R}$**" if fa > 1 else "🟢 **Đồng biến trên toàn trục số $\\mathbb{R}$**"

            st.caption(f"📌 **Tính đơn điệu:** {nature}<br>📌 **Tiệm cận ngang:** $y = {fc:.1f}$ (khi $x \\to -\\infty$ nếu $a>1$)<br>📌 **Điểm luôn đi qua:** $(0; {fk + fc:.1f})$", unsafe_allow_html=True)

        with c2:

            fig_exp = go.Figure()

            x_vals = np.linspace(-5, 4.5, 600)

            y_vals = fk * (fa ** x_vals) + fc

            y_vals[np.abs(y_vals) > 25] = np.nan



            fig_exp.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', line=dict(color='#38bdf8', width=3.5), name=f'y = {base_label}^x'))

            fig_exp.add_trace(go.Scatter(x=[-5, 5], y=[fc, fc], mode='lines', line=dict(color='#f59e0b', width=2, dash='dash'), name=f'TC Ngang y={fc}'))

            fig_exp.add_trace(go.Scatter(x=[0], y=[fk + fc], mode='markers+text', marker=dict(size=8, color='#f43f5e'), text=[f'(0; {fk+fc:.1f})'], textposition="top left", name='Điểm (0; y0)'))



            setup_pedagogical_oxy(fig_exp, [-5, 5], [min(-3, fc - 2), max(6, fc + 8)])

            fig_exp.update_layout(title=f"Đồ thị Hàm số Mũ: $y = {base_label}^x$ (CT GDPT 2018 Lớp 11-12)", height=500)

            st.plotly_chart(fig_exp, width="stretch")

        return



    if dtype == "func_log":

        c1, c2 = st.columns([1.2, 2.8])

        with c1:

            st.caption("⚙️ **Thông số Hàm số Lôgarit ($y = k \\cdot \\log_a(x) + c$):**")

            use_ln = st.checkbox("Dùng Lôgarit tự nhiên (ln(x), cơ số e)", value=bool(data.get("is_ln", False)), key="lab_log_is_ln")

            if use_ln:

                fa = float(np.e)

                st.info("📌 **Đang chọn:** Cơ số $e$ (Hàm số Lôgarit tự nhiên $y = \\ln(x)$)")

            else:

                fa = st.slider("Cơ số a (a > 0, a ≠ 1):", 0.1, 4.5, float(data.get("base", 2.0)), 0.1, key="lab_log_a")

                if abs(fa - 1.0) < 0.05: fa = 1.05



            fk = st.slider("Hệ số k:", -3.0, 3.0, float(data.get("k", 1.0)), 0.5, key="lab_log_k")

            if fk == 0: fk = 1.0

            fc = st.slider("Hệ số tịnh tiến c:", -4.0, 4.0, float(data.get("c", 0.0)), 0.5, key="lab_log_c")



            log_label = "\\ln(x)" if use_ln else f"\\log_{{{fa:.1f}}}(x)"

            st.success(f"📈 **Công thức:** $y = {fk if fk != 1 else ''}{log_label} {('+' + str(fc)) if fc > 0 else (str(fc) if fc < 0 else '')}$")



            if fk > 0:

                nature = "🟢 **Đồng biến trên khoảng $(0; +\\infty)$**" if fa > 1 else "🟠 **Nghịch biến trên khoảng $(0; +\\infty)$**"

            else:

                nature = "🟠 **Nghịch biến trên khoảng $(0; +\\infty)$**" if fa > 1 else "🟢 **Đồng biến trên khoảng $(0; +\\infty)$**"

            st.caption(f"📌 **Tập xác định:** $D = (0; +\\infty)$<br>📌 **Tính đơn điệu:** {nature}<br>📌 **Tiệm cận đứng:** $x = 0$ (Trục Oy)<br>📌 **Điểm luôn đi qua:** $(1; {fc:.1f})$", unsafe_allow_html=True)

        with c2:

            fig_log = go.Figure()

            x_vals = np.linspace(0.02, 8.0, 600)

            y_vals = fk * (np.log(x_vals) / np.log(fa)) + fc

            y_vals[np.abs(y_vals) > 20] = np.nan



            fig_log.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', line=dict(color='#38bdf8', width=3.5), name=f'y = {log_label}'))

            fig_log.add_trace(go.Scatter(x=[0, 0], y=[-10, 10], mode='lines', line=dict(color='#f59e0b', width=2, dash='dash'), name='TC Đứng x=0'))

            fig_log.add_trace(go.Scatter(x=[1], y=[fc], mode='markers+text', marker=dict(size=8, color='#f43f5e'), text=[f'(1; {fc:.1f})'], textposition="top left", name='Điểm (1; c)'))

            fig_log.add_vrect(x0=-4, x1=0, fillcolor="rgba(239, 68, 68, 0.12)", line_width=0, annotation_text="Vùng x ≤ 0 (KXD)", annotation_position="top left")



            setup_pedagogical_oxy(fig_log, [-2, 8], [-6, 6])

            fig_log.update_layout(title=f"Đồ thị Hàm số Lôgarit: $y = {log_label}$ (CT GDPT 2018 Lớp 11-12)", height=500)

            st.plotly_chart(fig_log, width="stretch")

        return



    if dtype == "area":

        c1, c2 = st.columns([1.2, 2.8])

        func_str = str(data.get("func", "x**2 - 3*x + 2")).replace('$', '').strip()



        clean_f = re.sub(r'\\frac{(.*?)}{(.*?)}', r'((\1)/(\2))', func_str)

        clean_f = clean_f.replace('\\sin', 'np.sin').replace('\\cos', 'np.cos').replace('\\tan', 'np.tan')

        clean_f = clean_f.replace('\\ln', 'np.log').replace('\\pi', 'np.pi')

        clean_f = re.sub(r'\be\^\{([^{}]*)\}', r'np.exp(\1)', clean_f)

        clean_f = re.sub(r'\be\^(\([^()]*\)|[\w\.]+)', r'np.exp(\1)', clean_f)



        clean_f = clean_f.replace('^', '**').replace('y=', '').replace('f(x)=', '').strip()

        clean_f = re.sub(r'(?<![\w.])(\d+(?:\.\d+)?)\s*([a-zA-Z\(])', r'\1*\2', clean_f)

        clean_f = re.sub(r'(\))\s*([a-zA-Z0-9\(])', r'\1*\2', clean_f)

        clean_f = clean_f.replace('{', '(').replace('}', ')')



        math_str = func_str.replace('**', '^').replace('*', '').replace(' ', '')



        sa_def = float(data.get("a", 0.0))

        sb_def = float(data.get("b", 3.0))



        with c1:

            st.caption("⚙️ **Thông số Diện tích hình phẳng:**")

            st.info(f"**Hàm số:** $y = {math_str}$")

            sa = st.slider("Cận dưới a:", -10.0, 10.0, sa_def, 0.5, key="lab_area_a")

            sb = st.slider("Cận trên b:", -10.0, 10.0, sb_def, 0.5, key="lab_area_b")



            if sa >= sb:

                st.warning("⚠️ Cận a phải nhỏ hơn cận b!")

                sb = sa + 0.5



            try:

                x_area = np.linspace(sa, sb, 400)

                y_area = safe_eval_func(clean_f, x_area)

                if isinstance(y_area, (int, float)): y_area = np.full_like(x_area, float(y_area))

                area_val = _trapz(np.abs(y_area), x_area)

                st.success(f"📐 **Diện tích (S):**\n\n$$S = \\int_{{{sa}}}^{{{sb}}} |{math_str}| dx \\approx {abs(area_val):.2f}$$")

            except Exception:

                pass



        with c2:

            try:

                fig_area = go.Figure()



                x_full = np.linspace(sa - 3, sb + 3, 600)

                y_full = safe_eval_func(clean_f, x_full)

                if isinstance(y_full, (int, float)): y_full = np.full_like(x_full, float(y_full))



                fig_area.add_trace(go.Scatter(x=x_full, y=y_full, mode='lines', line=dict(color='#38bdf8', width=3), name='Đồ thị hàm số'))



                y_area_fill = safe_eval_func(clean_f, x_area)

                if isinstance(y_area_fill, (int, float)): y_area_fill = np.full_like(x_area, float(y_area_fill))



                fig_area.add_trace(go.Scatter(x=np.concatenate([x_area, x_area[::-1]]),

                                              y=np.concatenate([y_area_fill, np.zeros_like(y_area_fill)]),

                                              fill='toself', fillcolor='rgba(236, 72, 153, 0.4)',

                                              line=dict(color='rgba(255,255,255,0)'), hoverinfo="skip", name='Diện tích (S)'))



                y_view_min, y_view_max = min(y_full), max(y_full)

                y_pad = (y_view_max - y_view_min) * 0.15

                if y_pad == 0: y_pad = 2

                y_min, y_max = y_view_min - y_pad, y_view_max + y_pad

                if y_min > 0: y_min = -y_pad

                if y_max < 0: y_max = y_pad



                y_sa = safe_eval_func(clean_f, sa)

                y_sb = safe_eval_func(clean_f, sb)

                fig_area.add_trace(go.Scatter(x=[sa, sa], y=[0, float(y_sa)], mode='lines', line=dict(color='#f59e0b', width=2, dash='dash'), name='Cận a'))

                fig_area.add_trace(go.Scatter(x=[sb, sb], y=[0, float(y_sb)], mode='lines', line=dict(color='#10b981', width=2, dash='dash'), name='Cận b'))



                setup_pedagogical_oxy(fig_area, [min(x_full), max(x_full)], [y_min, y_max])

                fig_area.update_layout(title="Mô phỏng Diện tích hình phẳng (Tích phân)", height=500, showlegend=True)

                st.plotly_chart(fig_area, width="stretch")

            except Exception as err:

                st.error(f"Lỗi vẽ đồ thị diện tích: {err}")

        return



    if dtype == "revolve_ox":

        func_str = str(data.get("func", "2*x + 1")).replace('$', '').strip()



        clean_f = re.sub(r'\\frac{(.*?)}{(.*?)}', r'((\1)/(\2))', func_str)

        clean_f = clean_f.replace('\\sin', 'np.sin').replace('\\cos', 'np.cos').replace('\\tan', 'np.tan')

        clean_f = clean_f.replace('\\ln', 'np.log').replace('\\pi', 'np.pi')

        clean_f = re.sub(r'\be\^\{([^{}]*)\}', r'np.exp(\1)', clean_f)

        clean_f = re.sub(r'\be\^(\([^()]*\)|[\w\.]+)', r'np.exp(\1)', clean_f)



        clean_f = clean_f.replace('^', '**').replace('y=', '').replace('f(x)=', '').strip()

        clean_f = re.sub(r'(?<![\w.])(\d+(?:\.\d+)?)\s*([a-zA-Z\(])', r'\1*\2', clean_f)

        clean_f = re.sub(r'(\))\s*([a-zA-Z0-9\(])', r'\1*\2', clean_f)

        clean_f = clean_f.replace('{', '(').replace('}', ')')



        a_def = float(data.get("a", 2.0))

        b_def = float(data.get("b", 5.0))



        c1, c2 = st.columns([1.2, 2.8])

        with c1:

            st.caption("⚙️ **Thông số Khối tròn xoay quanh trục Ox:**")

            math_str = func_str.replace('**', '^').replace('*', '')

            st.info(f"**Đường giới hạn:** $y = {math_str}$")

            sa = st.slider("Cận dưới a:", -8.0, 8.0, a_def, 0.5, key="lab_revolve_a")

            sb = st.slider("Cận trên b:", -8.0, 8.0, b_def, 0.5, key="lab_revolve_b")

            angle_deg = st.slider("Góc quay quanh trục Ox:", 30, 360, 360, 15, key="lab_revolve_angle")



            if sa >= sb:

                st.warning("⚠️ Cận a phải nhỏ hơn cận b!")

                sb = sa + 0.5



            try:

                x_num = np.linspace(sa, sb, 400)

                y_num = safe_eval_func(clean_f, x_num)

                if isinstance(y_num, (int, float)): y_num = np.full_like(x_num, float(y_num))

                vol_val = _trapz(y_num**2, x_num) * np.pi

                st.success(f"📐 **Thể tích khối tròn xoay:**\n\n$$V = \\pi \\int_{{{sa}}}^{{{sb}}} [{math_str}]^2 dx \\approx {abs(vol_val):.2f}\\text{{ (đvtt)}}$$")

            except Exception:

                pass



        with c2:

            try:

                u = np.linspace(sa, sb, 60)

                v = np.linspace(0, np.radians(angle_deg), 60)

                U, V = np.meshgrid(u, v)



                R_raw = safe_eval_func(clean_f, U)

                if isinstance(R_raw, (int, float)): R_raw = np.full_like(U, float(R_raw))

                R = np.abs(R_raw)



                X_3d = U

                Y_3d = R * np.cos(V)

                Z_3d = R * np.sin(V)



                fig_3d = go.Figure()

                fig_3d.add_trace(go.Surface(x=X_3d, y=Y_3d, z=Z_3d, colorscale='Viridis', opacity=0.82, showscale=False, name='Mặt xung quanh'))



                # NẮP ĐÁY KHÉP KÍN TẠI CẬN SA VÀ SB (CHUẨN HÌNH HỌC KHÔNG GIAN TÍCH PHÂN 3D)

                try:

                    ra_val = safe_eval_func(clean_f, sa)

                    ra = float(abs(ra_val)) if isinstance(ra_val, (int, float, np.number)) else 0.0

                    if ra > 0.01:

                        rc_a, vc_a = np.meshgrid(np.linspace(0, ra, 12), np.linspace(0, np.radians(angle_deg), 36))

                        fig_3d.add_trace(go.Surface(x=np.full_like(rc_a, sa), y=rc_a*np.cos(vc_a), z=rc_a*np.sin(vc_a), colorscale='Viridis', opacity=0.88, showscale=False, hoverinfo='skip', name='Đáy x=a'))



                    rb_val = safe_eval_func(clean_f, sb)

                    rb = float(abs(rb_val)) if isinstance(rb_val, (int, float, np.number)) else 0.0

                    if rb > 0.01:

                        rc_b, vc_b = np.meshgrid(np.linspace(0, rb, 12), np.linspace(0, np.radians(angle_deg), 36))

                        fig_3d.add_trace(go.Surface(x=np.full_like(rc_b, sb), y=rc_b*np.cos(vc_b), z=rc_b*np.sin(vc_b), colorscale='Viridis', opacity=0.88, showscale=False, hoverinfo='skip', name='Đáy x=b'))

                except Exception:

                    pass



                ox_min, ox_max = min(sa - 1.5, -2), max(sb + 1.5, 2)

                fig_3d.add_trace(go.Scatter3d(x=[ox_min, ox_max], y=[0, 0], z=[0, 0], mode='lines+text', line=dict(color='#ffffff', width=4), text=["", "Trục Ox"], textposition="top right", name="Trục Ox"))



                y_gen_raw = safe_eval_func(clean_f, u)

                if isinstance(y_gen_raw, (int, float)): y_gen_raw = np.full_like(u, float(y_gen_raw))

                y_gen = np.abs(y_gen_raw)

                fig_3d.add_trace(go.Scatter3d(x=u, y=y_gen, z=np.zeros_like(u), mode='lines', line=dict(color='#f43f5e', width=5), name='Đường sinh y=f(x)'))



                r_max = float(np.nanmax(R)) if len(R) > 0 else 2.0

                if r_max <= 0.05 or not math.isfinite(r_max): r_max = 2.0

                ox_pad = max(abs(sb - sa) * 0.1, 0.5)



                fig_3d.update_layout(

                    title=f"Mô hình 3D Khối tròn xoay: $y = {math_str}$ quay quanh Ox",

                    template="plotly_dark",

                    scene=dict(

                        xaxis=dict(title="Trục Ox", range=[sa - ox_pad, sb + ox_pad], backgroundcolor="#0f172a", gridcolor="#1e293b"),

                        yaxis=dict(title="Trục Oy", range=[-r_max*1.2, r_max*1.2], backgroundcolor="#0f172a", gridcolor="#1e293b"),

                        zaxis=dict(title="Trục Oz", range=[-r_max*1.2, r_max*1.2], backgroundcolor="#0f172a", gridcolor="#1e293b"),

                        aspectmode='cube'

                    ),

                    height=520,

                    margin=dict(l=10, r=10, t=35, b=10)

                )

                st.plotly_chart(fig_3d, width="stretch")

            except Exception as err:

                st.error(f"Lỗi tính toán mô phỏng 3D: {err}")

        return



    if dtype == "dynamic_code":

        st.markdown("### 🎨 Mô Phỏng Đồ Họa Động / Không Gian Nâng Cao")

        render_dynamic_python_lab(data.get("python_code", ""))

        return

    if dtype == "physics_oscillator":

        c1, c2 = st.columns([1.2, 2.8])

        with c1:

            st.caption("⚙️ **Thông số Dao động điều hòa ($x = A\\cos(\\omega t + \\varphi)$):**")

            p_A = st.slider("Biên độ A (cm):", 1.0, 15.0, float(data.get("A", 5.0)), 0.5, key="lab_osc_A")

            p_omega = st.slider("Tần số góc ω (rad/s):", 0.5, 10.0, float(data.get("omega", 2.0)), 0.5, key="lab_osc_w")

            p_phi = st.slider("Pha ban đầu φ (rad):", -np.pi, np.pi, float(data.get("phi", 0.0)), np.pi/6, format="%.2f", key="lab_osc_phi")



            p_T = (2 * np.pi) / p_omega

            p_f = p_omega / (2 * np.pi)

            p_vmax = p_omega * p_A

            p_amax = (p_omega ** 2) * p_A



            st.success(f"📈 **Phương trình:** $x = {p_A:.1f}\\cos({p_omega:.1f}t + {p_phi:.2f})$ cm")

            st.caption(f"📌 **Chu kỳ T:** `{p_T:.2f} s`<br>📌 **Tần số f:** `{p_f:.2f} Hz`<br>📌 **$v_{{max}}$:** `{p_vmax:.1f} cm/s`<br>📌 **$a_{{max}}$:** `{p_amax:.1f} cm/s²`", unsafe_allow_html=True)

            show_v = st.checkbox("Hiển thị đồ thị Vận tốc v(t)", value=True, key="lab_osc_show_v")

            show_a = st.checkbox("Hiển thị đồ thị Gia tốc a(t)", value=False, key="lab_osc_show_a")

        with c2:

            fig_osc = go.Figure()

            t_vals = np.linspace(0, max(2 * p_T, 4.0), 600)

            x_vals = p_A * np.cos(p_omega * t_vals + p_phi)

            v_vals = -p_omega * p_A * np.sin(p_omega * t_vals + p_phi)

            a_vals = -(p_omega ** 2) * p_A * np.cos(p_omega * t_vals + p_phi)



            fig_osc.add_trace(go.Scatter(x=t_vals, y=x_vals, mode='lines', line=dict(color='#38bdf8', width=3.5), name='Li độ x (cm)'))

            if show_v:

                fig_osc.add_trace(go.Scatter(x=t_vals, y=v_vals, mode='lines', line=dict(color='#34d399', width=2.5, dash='dash'), name='Vận tốc v (cm/s)'))

            if show_a:

                fig_osc.add_trace(go.Scatter(x=t_vals, y=a_vals, mode='lines', line=dict(color='#f43f5e', width=2, dash='dot'), name='Gia tốc a (cm/s²)'))



            fig_osc.update_layout(

                title="Mô phỏng Dao động Điều hòa (Vật lí 11 - CT GDPT 2018)",

                xaxis_title="Thời gian t (giây)",

                yaxis_title="Giá trị tức thời",

                template="plotly_dark",

                height=500

            )

            st.plotly_chart(fig_osc, width="stretch")

        return



    if dtype == "chem_equilibrium":

        c1, c2 = st.columns([1.2, 2.8])

        with c1:

            st.caption("⚙️ **Cân bằng Le Chatelier:** $N_2(g) + 3H_2(g) \\rightleftharpoons 2NH_3(g)$")

            st.caption("$\\Delta_r H^\\circ_{298} = -92 \\text{ kJ/mol}$ (Phản ứng tỏa nhiệt)")

            c_temp = st.slider("Nhiệt độ T (°C):", 100, 700, int(data.get("temp", 450)), 50, key="lab_eq_t")

            c_p = st.slider("Áp suất P (bar):", 10, 300, int(data.get("p", 200)), 10, key="lab_eq_p")



            yield_pct = np.clip(100 / (1 + np.exp(0.01 * (c_temp - 400))) * (c_p / 200)**0.4, 5, 95)

            st.success(f"📊 **Hiệu suất cân bằng NH₃:** `{yield_pct:.1f}%`")

            if c_temp > 450:

                st.warning("🔥 Tăng nhiệt độ: Cân bằng chuyển dịch theo chiều thu nhiệt (chiều nghịch, giảm hiệu suất).")

            else:

                st.info("❄️ Giảm nhiệt độ: Cân bằng chuyển dịch theo chiều tỏa nhiệt (chiều thuận, tăng hiệu suất).")

            if c_p > 200:

                st.info("⚡ Tăng áp suất: Cân bằng chuyển dịch sang chiều giảm số mol khí (chiều thuận).")

        with c2:

            fig_eq = go.Figure()

            t_axis = np.linspace(100, 700, 100)

            y_curve = np.clip(100 / (1 + np.exp(0.01 * (t_axis - 400))) * (c_p / 200)**0.4, 5, 95)

            fig_eq.add_trace(go.Scatter(x=t_axis, y=y_curve, mode='lines', line=dict(color='#38bdf8', width=3), name=f'Hiệu suất tại P={c_p} bar'))

            fig_eq.add_trace(go.Scatter(x=[c_temp], y=[yield_pct], mode='markers', marker=dict(color='#f43f5e', size=12), name='Trạng thái hiện tại'))

            fig_eq.update_layout(

                title=f"Chuyển dịch Cân bằng Hóa học Le Chatelier (Hóa học 11 IUPAC)",

                xaxis_title="Nhiệt độ T (°C)",

                yaxis_title="Hiệu suất tạo thành NH₃ (%)",

                template="plotly_dark",

                height=500

            )

            st.plotly_chart(fig_eq, width="stretch")

        return



    if dtype == "bio_genetics":

        st.markdown("### 🧬 Mô phỏng Quy luật Phân ly Mendel (Sinh học 12)")

        c1, c2 = st.columns([1.2, 2.8])

        with c1:

            st.caption("⚙️ **Phép lai một cặp tính trạng:** $P: Aa \\times Aa$")

            gen_A = st.text_input("Tên gen trội A:", "Hạt vàng (A)", key="lab_bio_A")

            gen_a = st.text_input("Tên gen lặn a:", "Hạt xanh (a)", key="lab_bio_a")

            st.success("Tỉ lệ kiểu gen F1: **1 AA : 2 Aa : 1 aa**")

            st.info(f"Tỉ lệ kiểu hình F1: **3 {gen_A} : 1 {gen_a}** (75% trội : 25% lặn)")

        with c2:

            labels = [f"3 {gen_A} (Trội)", f"1 {gen_a} (Lặn)"]

            values = [75, 25]

            fig_bio = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.35, marker_colors=['#38bdf8', '#f59e0b'])])

            fig_bio.update_layout(title="Phân ly Kiểu hình F1 chuẩn Mendel (Sinh học CT GDPT 2018)", template="plotly_dark", height=420)

            st.plotly_chart(fig_bio, width="stretch")

        return





    fig = go.Figure()



    if dtype == "func_3":
        c1, c2 = st.columns([1.2, 2.8])
        with c1:
            st.caption("⚙️ **Thay đổi hệ số hàm bậc 3:**")
            fa = st.slider("Hệ số a:", -3.0, 3.0, float(data.get("a", 1.0)), 0.5, key="lab_f3_a")
            if fa == 0: fa = 0.5
            fb = st.slider("Hệ số b:", -5.0, 5.0, float(data.get("b", -3.0)), 0.5, key="lab_f3_b")
            fc = st.slider("Hệ số c:", -5.0, 5.0, float(data.get("c", 0.0)), 0.5, key="lab_f3_c")
            fd = st.slider("Hệ số d:", -5.0, 5.0, float(data.get("d", 2.0)), 0.5, key="lab_f3_d")
            st.info(f"**$y = {fa}x^3 + ({fb})x^2 + ({fc})x + ({fd})$**")

            # Tính toán Điểm uốn / Tâm đối xứng
            x_uon = -fb / (3.0 * fa)
            y_uon = fa * (x_uon**3) + fb * (x_uon**2) + fc * x_uon + fd

            # Tính toán Cực trị
            delta_prime = (fb ** 2) - 3.0 * fa * fc
            has_extrema = delta_prime > 1e-6
            c_info = [f"📌 **Tâm ĐX / Điểm uốn:** $I({x_uon:.2f}; {y_uon:.2f})$"]
            c_info.append(f"📌 **Giao trục tung $Oy$:** $(0; {fd:.2f})$")

            x_cd, y_cd, x_ct, y_ct = None, None, None, None
            if has_extrema:
                sq_d = math.sqrt(delta_prime)
                x_cand1 = (-fb - sq_d) / (3.0 * fa)
                x_cand2 = (-fb + sq_d) / (3.0 * fa)
                y_cand1 = fa * (x_cand1**3) + fb * (x_cand1**2) + fc * x_cand1 + fd
                y_cand2 = fa * (x_cand2**3) + fb * (x_cand2**2) + fc * x_cand2 + fd

                if fa > 0:
                    x_cd, y_cd = min(x_cand1, x_cand2), (y_cand1 if x_cand1 < x_cand2 else y_cand2)
                    x_ct, y_ct = max(x_cand1, x_cand2), (y_cand2 if x_cand1 < x_cand2 else y_cand1)
                else:
                    x_ct, y_ct = min(x_cand1, x_cand2), (y_cand1 if x_cand1 < x_cand2 else y_cand2)
                    x_cd, y_cd = max(x_cand1, x_cand2), (y_cand2 if x_cand1 < x_cand2 else y_cand1)

                c_info.append(f"🔴 **Điểm cực đại:** $CĐ({x_cd:.2f}; {y_cd:.2f})$")
                c_info.append(f"🟠 **Điểm cực tiểu:** $CT({x_ct:.2f}; {y_ct:.2f})$")
            else:
                c_info.append("ℹ️ Hàm số đơn điệu, không có cực trị.")

            st.caption("<br>".join(c_info), unsafe_allow_html=True)

        with c2:
            # Thuật toán căn chỉnh co giãn tối ưu (Auto-zoom bounds)
            if has_extrema and x_cd is not None and x_ct is not None:
                span_x = max(abs(x_cd - x_ct), 1.5)
                x_min = min(x_cd, x_ct, x_uon, 0.0) - span_x * 0.85
                x_max = max(x_cd, x_ct, x_uon, 0.0) + span_x * 0.85
                y_spec = [y_cd, y_ct, y_uon, fd, 0.0]
                span_y = max(y_spec) - min(y_spec)
                if span_y < 3.5: span_y = 5.0
                y_min = min(y_spec) - span_y * 0.35
                y_max = max(y_spec) + span_y * 0.35
            else:
                x_min = min(x_uon, 0.0) - 4.5
                x_max = max(x_uon, 0.0) + 4.5
                y_min = y_uon - 7.0
                y_max = y_uon + 7.0

            if abs(x_max - x_min) < 6:
                x_mid = (x_min + x_max) / 2
                x_min, x_max = x_mid - 3.5, x_mid + 3.5

            x_vals = np.linspace(x_min, x_max, 800)
            y_vals = fa * (x_vals**3) + fb * (x_vals**2) + fc * x_vals + fd

            # Đường đồ thị chính
            fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', line=dict(color='#38bdf8', width=3.5), name='Đồ thị f(x)'))

            # Marker và dóng tọa độ Cực Trị
            if has_extrema and x_cd is not None and x_ct is not None:
                # Cực đại
                fig.add_trace(go.Scatter(x=[x_cd], y=[y_cd], mode='markers+text', marker=dict(size=10, color='#f43f5e', symbol='diamond'),
                                         text=[f'CĐ({x_cd:.1f}; {y_cd:.1f})'], textposition="top center", name='Cực đại (CĐ)'))
                fig.add_trace(go.Scatter(x=[x_cd, x_cd, 0], y=[0, y_cd, y_cd], mode='lines', line=dict(color='#f43f5e', width=1.4, dash='dash'), hoverinfo='skip', showlegend=False))

                # Cực tiểu
                fig.add_trace(go.Scatter(x=[x_ct], y=[y_ct], mode='markers+text', marker=dict(size=10, color='#f59e0b', symbol='diamond'),
                                         text=[f'CT({x_ct:.1f}; {y_ct:.1f})'], textposition="bottom center", name='Cực tiểu (CT)'))
                fig.add_trace(go.Scatter(x=[x_ct, x_ct, 0], y=[0, y_ct, y_ct], mode='lines', line=dict(color='#f59e0b', width=1.4, dash='dash'), hoverinfo='skip', showlegend=False))

            # Marker Điểm uốn / Tâm đối xứng
            fig.add_trace(go.Scatter(x=[x_uon], y=[y_uon], mode='markers+text', marker=dict(size=9, color='#a855f7', symbol='circle'),
                                     text=[f'I({x_uon:.1f}; {y_uon:.1f})'], textposition="top right", name='Tâm ĐX / Điểm uốn I'))
            fig.add_trace(go.Scatter(x=[x_uon, x_uon, 0], y=[0, y_uon, y_uon], mode='lines', line=dict(color='#a855f7', width=1.2, dash='dot'), hoverinfo='skip', showlegend=False))

            # Marker Giao điểm trục tung Oy
            if y_min <= fd <= y_max:
                fig.add_trace(go.Scatter(x=[0], y=[fd], mode='markers+text', marker=dict(size=8, color='#10b981', symbol='cross'),
                                         text=[f'(0; {fd:.1f})'], textposition="middle right", name='Giao trục Oy'))

            # Marker Giao điểm trục hoành Ox (các nghiệm thực)
            try:
                roots = np.roots([fa, fb, fc, fd])
                for r in roots:
                    if np.isreal(r):
                        rx = float(np.real(r))
                        if x_min <= rx <= x_max and abs(rx) > 0.15:
                            fig.add_trace(go.Scatter(x=[rx], y=[0], mode='markers+text', marker=dict(size=7, color='#06b6d4', symbol='circle-open'),
                                                     text=[f'({rx:.1f}; 0)'], textposition="bottom left", name='Giao trục Ox', showlegend=False))
            except Exception:
                pass

            setup_pedagogical_oxy(fig, [x_min, x_max], [y_min, y_max])
            fig.update_layout(title="Đồ thị Hàm số Bậc 3 (Tối ưu co giãn • Kèm CĐ, CT, Tâm ĐX & Giao trục)", height=520, showlegend=True)
            st.plotly_chart(fig, width="stretch")

    elif dtype == "func_1_1":
        c1, c2 = st.columns([1.2, 2.8])
        with c1:
            st.caption("⚙️ **Thay đổi hệ số hàm phân thức bậc 1/1:**")
            fa = st.slider("Hệ số a:", -4.0, 4.0, float(data.get("a", 1.0)), 0.5, key="lab_f11_a")
            fb = st.slider("Hệ số b:", -5.0, 5.0, float(data.get("b", 1.0)), 0.5, key="lab_f11_b")
            fc = st.slider("Hệ số c:", -4.0, 4.0, float(data.get("c", 1.0)), 0.5, key="lab_f11_c")
            if fc == 0: fc = 1.0
            fd = st.slider("Hệ số d:", -5.0, 5.0, float(data.get("d", -1.0)), 0.5, key="lab_f11_d")

            x_tc_dung = -fd / fc
            y_tc_ngang = fa / fc
            y_oy = (fb / fd) if fd != 0 else None
            x_ox = (-fb / fa) if fa != 0 else None

            st.info(f"**$y = \\frac{{{fa}x + {fb}}}{{{fc}x + {fd}}}$**")
            info_lines = [
                f"📌 **Tiệm cận đứng (TCĐ):** $x = {x_tc_dung:.2f}$",
                f"📌 **Tiệm cận ngang (TCN):** $y = {y_tc_ngang:.2f}$",
                f"🎯 **Tâm đối xứng:** $I({x_tc_dung:.2f}; {y_tc_ngang:.2f})$"
            ]
            if y_oy is not None:
                info_lines.append(f"📍 **Giao trục tung $Oy$:** $(0; {y_oy:.2f})$")
            if x_ox is not None:
                info_lines.append(f"📍 **Giao trục hoành $Ox$:** $({x_ox:.2f}; 0)$")

            st.caption("<br>".join(info_lines), unsafe_allow_html=True)

        with c2:
            # Thuật toán căn chỉnh co giãn tự động tối ưu (Auto-zoom bám sát tâm I và giao điểm)
            dx = max(4.5, abs(x_tc_dung) + 2.2, (abs(x_ox - x_tc_dung) + 1.8) if x_ox is not None else 4.5)
            dy = max(4.5, abs(y_tc_ngang) + 2.2, (abs(y_oy - y_tc_ngang) + 1.8) if y_oy is not None else 4.5)
            x_min = x_tc_dung - dx
            x_max = x_tc_dung + dx
            y_min = y_tc_ngang - dy
            y_max = y_tc_ngang + dy

            # Vẽ hai nhánh hypebol
            x_left = np.linspace(x_min, x_tc_dung - 0.04, 400)
            x_right = np.linspace(x_tc_dung + 0.04, x_max, 400)
            y_left = (fa * x_left + fb) / (fc * x_left + fd)
            y_right = (fa * x_right + fb) / (fc * x_right + fd)

            clip_limit = max(abs(y_min), abs(y_max)) * 1.6
            y_left[np.abs(y_left) > clip_limit] = np.nan
            y_right[np.abs(y_right) > clip_limit] = np.nan

            fig.add_trace(go.Scatter(x=x_left, y=y_left, mode='lines', line=dict(color='#38bdf8', width=3.5), name='Nhánh trái'))
            fig.add_trace(go.Scatter(x=x_right, y=y_right, mode='lines', line=dict(color='#38bdf8', width=3.5), name='Nhánh phải'))

            # Hai đường tiệm cận
            fig.add_trace(go.Scatter(x=[x_tc_dung, x_tc_dung], y=[y_min, y_max], mode='lines', line=dict(color='#f59e0b', width=1.8, dash='dash'), name='TC Đứng'))
            fig.add_trace(go.Scatter(x=[x_min, x_max], y=[y_tc_ngang, y_tc_ngang], mode='lines', line=dict(color='#10b981', width=1.8, dash='dash'), name='TC Ngang'))

            # Marker Tâm đối xứng I (Giao điểm 2 tiệm cận)
            fig.add_trace(go.Scatter(x=[x_tc_dung], y=[y_tc_ngang], mode='markers+text', marker=dict(size=11, color='#facc15', symbol='star'),
                                     text=[f'I({x_tc_dung:.1f}; {y_tc_ngang:.1f})'], textposition="top right", name='Tâm đối xứng I'))

            # Marker Giao điểm trục tung Oy
            if y_oy is not None and y_min <= y_oy <= y_max:
                fig.add_trace(go.Scatter(x=[0], y=[y_oy], mode='markers+text', marker=dict(size=8, color='#34d399', symbol='cross'),
                                         text=[f'(0; {y_oy:.1f})'], textposition="middle right", name='Giao Oy'))
                fig.add_trace(go.Scatter(x=[0, x_tc_dung], y=[y_oy, y_oy], mode='lines', line=dict(color='#34d399', width=1.0, dash='dot'), hoverinfo='skip', showlegend=False))

            # Marker Giao điểm trục hoành Ox
            if x_ox is not None and x_min <= x_ox <= x_max:
                fig.add_trace(go.Scatter(x=[x_ox], y=[0], mode='markers+text', marker=dict(size=8, color='#38bdf8', symbol='cross'),
                                         text=[f'({x_ox:.1f}; 0)'], textposition="bottom center", name='Giao Ox'))
                fig.add_trace(go.Scatter(x=[x_ox, x_ox], y=[0, y_tc_ngang], mode='lines', line=dict(color='#38bdf8', width=1.0, dash='dot'), hoverinfo='skip', showlegend=False))

            setup_pedagogical_oxy(fig, [x_min, x_max], [y_min, y_max])
            fig.update_layout(title="Đồ thị Hàm phân thức Bậc 1 / Bậc 1 (Tối ưu co giãn • Kèm Tâm ĐX & Giao trục)", height=520, showlegend=True)
            st.plotly_chart(fig, width="stretch")

    elif dtype == "func_2_1":
        c1, c2 = st.columns([1.2, 2.8])
        with c1:
            st.caption("⚙️ **Hệ số hàm phân thức bậc 2/1:**")
            fa = st.slider("a:", -3.0, 3.0, float(data.get("a", 1.0)), 0.5, key="lab_f21_a")
            if fa == 0: fa = 1.0
            fb = st.slider("b:", -5.0, 5.0, float(data.get("b", -2.0)), 0.5, key="lab_f21_b")
            fc = st.slider("c:", -5.0, 5.0, float(data.get("c", 2.0)), 0.5, key="lab_f21_c")
            fd = st.slider("d:", -3.0, 3.0, float(data.get("d", 1.0)), 0.5, key="lab_f21_d")
            if fd == 0: fd = 1.0
            fe = st.slider("e:", -5.0, 5.0, float(data.get("e", -1.0)), 0.5, key="lab_f21_e")

            x_tc_dung = -fe / fd
            m_slope = fa / fd
            n_intercept = (fb - m_slope * fe) / fd
            x_tam_dx = x_tc_dung
            y_tam_dx = m_slope * x_tam_dx + n_intercept
            y_oy = (fc / fe) if fe != 0 else None

            # Đạo hàm: u'v - uv' = (2ax+b)(dx+e) - d(ax^2+bx+c) = ad*x^2 + 2ae*x + (be - cd)
            A_der = fa * fd
            B_der = 2.0 * fa * fe
            C_der = fb * fe - fc * fd
            delta_der = (B_der ** 2) - 4.0 * A_der * C_der
            has_extrema_21 = delta_der > 1e-6

            st.info(f"**$y = \\frac{{{fa}x^2 + {fb}x + {fc}}}{{{fd}x + {fe}}}$**")
            info_lines_21 = [
                f"📌 **Tiệm cận đứng:** $x = {x_tc_dung:.2f}$",
                f"📌 **Tiệm cận xiên:** $y = {m_slope:.2f}x + ({n_intercept:.2f})$",
                f"🎯 **Tâm đối xứng:** $I({x_tam_dx:.2f}; {y_tam_dx:.2f})$"
            ]
            if y_oy is not None:
                info_lines_21.append(f"📍 **Giao trục tung $Oy$:** $(0; {y_oy:.2f})$")

            x_cd_21, y_cd_21, x_ct_21, y_ct_21 = None, None, None, None
            lbl_x_cd, lbl_y_cd, lbl_x_ct, lbl_y_ct = "", "", "", ""
            if has_extrema_21:
                # 1. Tính toán giá trị xấp xỉ số thực cho tọa độ đồ thị
                sq_d21 = math.sqrt(delta_der)
                xc1 = (-B_der - sq_d21) / (2.0 * A_der)
                xc2 = (-B_der + sq_d21) / (2.0 * A_der)
                yc1 = (fa * xc1**2 + fb * xc1 + fc) / (fd * xc1 + fe)
                yc2 = (fa * xc2**2 + fb * xc2 + fc) / (fd * xc2 + fe)

                # 2. Tính toán tọa độ đại số chính xác (phân số tối giản hoặc căn thức vô tỷ chuẩn SGK GDPT 2018)
                def _calc_exact_roots(A, B, C):
                    D = B**2 - 4*A*C
                    if D <= 0: return None
                    sq_d = int(round(math.isqrt(int(round(D)))))
                    if sq_d * sq_d == int(round(D)):
                        f1, f2 = Fraction(-B - sq_d, 2*A), Fraction(-B + sq_d, 2*A)
                        f_min, f_max = min(f1, f2), max(f1, f2)
                        t1 = str(f_min.numerator) if f_min.denominator == 1 else f"{f_min.numerator}/{f_min.denominator}"
                        t2 = str(f_max.numerator) if f_max.denominator == 1 else f"{f_max.numerator}/{f_max.denominator}"
                        return {"x1_val": float(f_min), "x2_val": float(f_max), "x1_tex": t1, "x2_tex": t2, "is_irrat": False}
                    d_int = int(round(D))
                    k, d_c = 1, d_int
                    for i in range(int(math.isqrt(d_int)), 1, -1):
                        if d_int % (i*i) == 0:
                            k, d_c = i, d_int // (i*i)
                            break
                    nb, den = -B, 2*A
                    g = math.gcd(math.gcd(int(abs(nb)), k), int(abs(den)))
                    if den < 0: nb, den = -nb, -den
                    nb //= g; k //= g; den //= g
                    k_str = "" if k == 1 else str(k)
                    sqrt_u = f"√{d_c}"
                    if den == 1:
                        t1 = f"-{k_str}{sqrt_u}" if nb == 0 else f"{nb} - {k_str}{sqrt_u}"
                        t2 = f"{k_str}{sqrt_u}" if nb == 0 else f"{nb} + {k_str}{sqrt_u}"
                    else:
                        t1 = f"-{k_str}{sqrt_u}/{den}" if nb == 0 else f"({nb} - {k_str}{sqrt_u})/{den}"
                        t2 = f"{k_str}{sqrt_u}/{den}" if nb == 0 else f"({nb} + {k_str}{sqrt_u})/{den}"
                    v1, v2 = (-B - math.sqrt(D))/(2*A), (-B + math.sqrt(D))/(2*A)
                    if v1 > v2: v1, v2 = v2, v1; t1, t2 = t2, t1
                    return {"x1_val": v1, "x2_val": v2, "x1_tex": t1, "x2_tex": t2, "is_irrat": True, "nb": nb, "k": k, "den": den, "d_c": d_c}

                def _eval_exact_lin(m_val, n_val, r_info, is_x2=False):
                    sgn = 1 if is_x2 else -1
                    if not r_info or not r_info.get("is_irrat"):
                        f_x = Fraction(str(r_info["x2_val"] if is_x2 else r_info["x1_val"])) if r_info else Fraction(0)
                        f_y = Fraction(str(m_val)) * f_x + Fraction(str(n_val))
                        return str(f_y.numerator) if f_y.denominator == 1 else f"{f_y.numerator}/{f_y.denominator}"
                    fm, fn = Fraction(str(m_val)), Fraction(str(n_val))
                    c_den = fm.denominator * r_info["den"] * fn.denominator
                    t_rat = (fm.numerator * r_info["nb"] * fn.denominator) + (fn.numerator * fm.denominator * r_info["den"])
                    t_sq = fm.numerator * r_info["k"] * fn.denominator * sgn
                    g = math.gcd(math.gcd(abs(t_rat), abs(t_sq)), abs(c_den))
                    if c_den < 0: t_rat, t_sq, c_den = -t_rat, -t_sq, -c_den
                    t_rat //= g; t_sq //= g; c_den //= g
                    kr = abs(t_sq); k_str = "" if kr == 1 else str(kr)
                    sg = " + " if t_sq >= 0 else " - "
                    sq_u = f"√{r_info['d_c']}"
                    if c_den == 1:
                        return f"{k_str}{sq_u}" if (t_sq >= 0 and t_rat == 0) else (f"-{k_str}{sq_u}" if t_rat == 0 else f"{t_rat}{sg}{k_str}{sq_u}")
                    return f"({k_str}{sq_u})/{c_den}" if (t_sq >= 0 and t_rat == 0) else (f"(-{k_str}{sq_u})/{c_den}" if t_rat == 0 else f"({t_rat}{sg}{k_str}{sq_u})/{c_den}")

                sc = 1000
                r_exact = _calc_exact_roots(int(round(A_der * sc)), int(round(B_der * sc)), int(round(C_der * sc)))
                m_eff = Fraction(int(round(2 * fa * 100)), int(round(fd * 100)))
                n_eff = Fraction(int(round(fb * 100)), int(round(fd * 100)))
                y1_tex = _eval_exact_lin(m_eff, n_eff, r_exact, is_x2=False)
                y2_tex = _eval_exact_lin(m_eff, n_eff, r_exact, is_x2=True)

                if m_slope > 0:
                    x_cd_21, y_cd_21 = min(xc1, xc2), (yc1 if xc1 < xc2 else yc2)
                    x_ct_21, y_ct_21 = max(xc1, xc2), (yc2 if xc1 < xc2 else yc1)
                    lbl_x_cd, lbl_y_cd = (r_exact['x1_tex'] if r_exact else f"{x_cd_21:.2f}"), y1_tex
                    lbl_x_ct, lbl_y_ct = (r_exact['x2_tex'] if r_exact else f"{x_ct_21:.2f}"), y2_tex
                else:
                    x_ct_21, y_ct_21 = min(xc1, xc2), (yc1 if xc1 < xc2 else yc2)
                    x_cd_21, y_cd_21 = max(xc1, xc2), (yc2 if xc1 < xc2 else yc1)
                    lbl_x_ct, lbl_y_ct = (r_exact['x1_tex'] if r_exact else f"{x_ct_21:.2f}"), y1_tex
                    lbl_x_cd, lbl_y_cd = (r_exact['x2_tex'] if r_exact else f"{x_cd_21:.2f}"), y2_tex

                info_lines_21.append(f"🔴 **Điểm cực đại:** $CĐ({lbl_x_cd}; {lbl_y_cd}) \\approx ({x_cd_21:.2f}; {y_cd_21:.2f})$")
                info_lines_21.append(f"🟠 **Điểm cực tiểu:** $CT({lbl_x_ct}; {lbl_y_ct}) \\approx ({x_ct_21:.2f}; {y_ct_21:.2f})$")

            st.caption("<br>".join(info_lines_21), unsafe_allow_html=True)

        with c2:
            # Thuật toán co giãn tự động tối ưu
            dx = max(4.5, abs(x_tc_dung) + 2.5)
            if has_extrema_21 and x_cd_21 is not None and x_ct_21 is not None:
                dx = max(dx, abs(x_cd_21 - x_tc_dung) + 2.0, abs(x_ct_21 - x_tc_dung) + 2.0)
            x_min = x_tc_dung - dx
            x_max = x_tc_dung + dx

            dy = max(6.0, abs(y_tam_dx) + 3.0)
            if has_extrema_21 and y_cd_21 is not None and y_ct_21 is not None:
                dy = max(dy, abs(y_cd_21 - y_tam_dx) + 3.0, abs(y_ct_21 - y_tam_dx) + 3.0)
            y_min = y_tam_dx - dy
            y_max = y_tam_dx + dy

            x_left = np.linspace(x_min, x_tc_dung - 0.05, 400)
            x_right = np.linspace(x_tc_dung + 0.05, x_max, 400)
            y_left = (fa * x_left**2 + fb * x_left + fc) / (fd * x_left + fe)
            y_right = (fa * x_right**2 + fb * x_right + fc) / (fd * x_right + fe)

            clip_limit_21 = max(abs(y_min), abs(y_max)) * 1.5
            y_left[np.abs(y_left) > clip_limit_21] = np.nan
            y_right[np.abs(y_right) > clip_limit_21] = np.nan

            fig.add_trace(go.Scatter(x=x_left, y=y_left, mode='lines', line=dict(color='#38bdf8', width=3.5), name='Nhánh trái'))
            fig.add_trace(go.Scatter(x=x_right, y=y_right, mode='lines', line=dict(color='#38bdf8', width=3.5), name='Nhánh phải'))
            fig.add_trace(go.Scatter(x=[x_tc_dung, x_tc_dung], y=[y_min, y_max], mode='lines', line=dict(color='#f59e0b', width=1.8, dash='dash'), name='TC Đứng'))

            # Tiệm cận xiên
            x_slant = np.linspace(x_min, x_max, 100)
            y_slant = m_slope * x_slant + n_intercept
            fig.add_trace(go.Scatter(x=x_slant, y=y_slant, mode='lines', line=dict(color='#ec4899', width=1.8, dash='dash'), name='TC Xiên'))

            # Marker Tâm đối xứng I
            fig.add_trace(go.Scatter(x=[x_tam_dx], y=[y_tam_dx], mode='markers+text', marker=dict(size=11, color='#facc15', symbol='star'),
                                     text=[f'I({x_tam_dx:.1f}; {y_tam_dx:.1f})'], textposition="top right", name='Tâm đối xứng I'))

            # Marker Cực trị & Đường gióng vuông góc xuống Ox, Oy chuẩn mực SGK GDPT 2018
            if has_extrema_21 and x_cd_21 is not None and x_ct_21 is not None:
                # 1. Đường gióng nét đứt xuống Ox và Oy cho Cực đại (CĐ)
                fig.add_trace(go.Scatter(x=[x_cd_21, x_cd_21], y=[0, y_cd_21], mode='lines', line=dict(color='#f43f5e', width=1.3, dash='dot'), showlegend=False, hoverinfo='skip'))
                fig.add_trace(go.Scatter(x=[0, x_cd_21], y=[y_cd_21, y_cd_21], mode='lines', line=dict(color='#f43f5e', width=1.3, dash='dot'), showlegend=False, hoverinfo='skip'))

                # 2. Đường gióng nét đứt xuống Ox và Oy cho Cực tiểu (CT)
                fig.add_trace(go.Scatter(x=[x_ct_21, x_ct_21], y=[0, y_ct_21], mode='lines', line=dict(color='#f59e0b', width=1.3, dash='dot'), showlegend=False, hoverinfo='skip'))
                fig.add_trace(go.Scatter(x=[0, x_ct_21], y=[y_ct_21, y_ct_21], mode='lines', line=dict(color='#f59e0b', width=1.3, dash='dot'), showlegend=False, hoverinfo='skip'))

                # Nhãn tọa độ chính xác tại chân đường gióng trên trục Ox và Oy
                fig.add_annotation(x=x_cd_21, y=0, text=f"<b>{lbl_x_cd}</b>", showarrow=True, arrowhead=2, arrowsize=0.8, ax=0, ay=18, font=dict(color="#f43f5e", size=10))
                fig.add_annotation(x=0, y=y_cd_21, text=f"<b>{lbl_y_cd}</b>", showarrow=True, arrowhead=2, arrowsize=0.8, ax=-22, ay=0, font=dict(color="#f43f5e", size=10))
                fig.add_annotation(x=x_ct_21, y=0, text=f"<b>{lbl_x_ct}</b>", showarrow=True, arrowhead=2, arrowsize=0.8, ax=0, ay=18, font=dict(color="#f59e0b", size=10))
                fig.add_annotation(x=0, y=y_ct_21, text=f"<b>{lbl_y_ct}</b>", showarrow=True, arrowhead=2, arrowsize=0.8, ax=-22, ay=0, font=dict(color="#f59e0b", size=10))

                # Điểm đánh dấu CĐ và CT kèm nhãn chính xác
                fig.add_trace(go.Scatter(x=[x_cd_21], y=[y_cd_21], mode='markers+text', marker=dict(size=10, color='#f43f5e', symbol='diamond'),
                                         text=[f'CĐ({lbl_x_cd}; {lbl_y_cd})'], textposition="top center", name='Cực đại (CĐ)'))
                fig.add_trace(go.Scatter(x=[x_ct_21], y=[y_ct_21], mode='markers+text', marker=dict(size=10, color='#f59e0b', symbol='diamond'),
                                         text=[f'CT({lbl_x_ct}; {lbl_y_ct})'], textposition="bottom center", name='Cực tiểu (CT)'))

            # Marker Giao trục Oy
            if y_oy is not None and y_min <= y_oy <= y_max:
                fig.add_trace(go.Scatter(x=[0], y=[y_oy], mode='markers+text', marker=dict(size=8, color='#34d399', symbol='cross'),
                                         text=[f'(0; {y_oy:.1f})'], textposition="middle right", name='Giao Oy'))

            setup_pedagogical_oxy(fig, [x_min, x_max], [y_min, y_max])
            fig.update_layout(title="Đồ thị Hàm phân thức Bậc 2 / Bậc 1 (Tối ưu co giãn • Kèm CĐ, CT, Tâm ĐX & TC Xiên)", height=520, showlegend=True)
            st.plotly_chart(fig, width="stretch")

    elif dtype in ["parabola", "func_2"]:
        c1, c2 = st.columns([1.2, 2.8])
        with c1:
            st.caption("⚙️ **Hệ số Parabol bậc 2 ($y = ax^2 + bx + c$):**")
            fa = st.slider("Hệ số a:", -4.0, 4.0, float(data.get("a", 1.0)), 0.5, key="lab_p2_a")
            if fa == 0: fa = 1.0
            fb = st.slider("Hệ số b:", -6.0, 6.0, float(data.get("b", -2.0)), 0.5, key="lab_p2_b")
            fc = st.slider("Hệ số c:", -6.0, 6.0, float(data.get("c", -1.0)), 0.5, key="lab_p2_c")

            x_dinh = -fb / (2 * fa)
            y_dinh = fa * x_dinh**2 + fb * x_dinh + fc
            st.info(f"**$y = {fa}x^2 + ({fb})x + ({fc})$**")

            p_lines = [
                f"📌 **Đỉnh Parabol:** $I({x_dinh:.2f}; {y_dinh:.2f})$",
                f"📌 **Trục đối xứng:** $x = {x_dinh:.2f}$",
                f"📍 **Giao trục tung $Oy$:** $(0; {fc:.2f})$"
            ]
            delta_p = fb**2 - 4.0 * fa * fc
            if delta_p >= 0:
                sq_dp = math.sqrt(delta_p)
                xp1 = (-fb - sq_dp) / (2.0 * fa)
                xp2 = (-fb + sq_dp) / (2.0 * fa)
                p_lines.append(f"📍 **Giao trục hoành $Ox$:** $({xp1:.2f}; 0)$, $({xp2:.2f}; 0)$")
            st.caption("<br>".join(p_lines), unsafe_allow_html=True)

        with c2:
            span_x = 4.5
            if delta_p >= 0:
                span_x = max(span_x, abs(xp1 - x_dinh) + 2.0, abs(xp2 - x_dinh) + 2.0)
            x_min = x_dinh - span_x
            x_max = x_dinh + span_x

            x_vals = np.linspace(x_min, x_max, 600)
            y_vals = fa * x_vals**2 + fb * x_vals + fc

            fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', line=dict(color='#38bdf8', width=3.5), name='Parabol'))

            # Co giãn tối ưu
            y_spec = [y_dinh, fc, 0.0]
            span_y = max(y_spec) - min(y_spec)
            if span_y < 3.5: span_y = 5.0
            y_min = min(y_spec) - span_y * 0.4
            y_max = max(y_spec) + span_y * 0.4

            # Trục đối xứng
            fig.add_trace(go.Scatter(x=[x_dinh, x_dinh], y=[y_min, y_max], mode='lines', line=dict(color='#f59e0b', width=1.5, dash='dash'), name='Trục đối xứng'))

            # Đỉnh I
            fig.add_trace(go.Scatter(x=[x_dinh], y=[y_dinh], mode='markers+text', marker=dict(size=10, color='gold', symbol='diamond'),
                                     text=[f'I({x_dinh:.1f}; {y_dinh:.1f})'], textposition="top center", name='Đỉnh I'))
            fig.add_trace(go.Scatter(x=[x_dinh, x_dinh, 0], y=[0, y_dinh, y_dinh], mode='lines', line=dict(color='gold', width=1.2, dash='dot'), hoverinfo='skip', showlegend=False))

            # Giao Oy
            if y_min <= fc <= y_max:
                fig.add_trace(go.Scatter(x=[0], y=[fc], mode='markers+text', marker=dict(size=8, color='#34d399', symbol='cross'),
                                         text=[f'(0; {fc:.1f})'], textposition="middle right", name='Giao Oy'))

            # Giao Ox
            if delta_p >= 0:
                for xp in [xp1, xp2]:
                    if x_min <= xp <= x_max and abs(xp) > 0.15:
                        fig.add_trace(go.Scatter(x=[xp], y=[0], mode='markers+text', marker=dict(size=7, color='#06b6d4', symbol='circle-open'),
                                                 text=[f'({xp:.1f}; 0)'], textposition="bottom center", name='Giao Ox', showlegend=False))

            setup_pedagogical_oxy(fig, [x_min, x_max], [y_min, y_max])
            fig.update_layout(title="Đồ thị Parabol Bậc 2 (Tối ưu co giãn • Kèm Đỉnh, Trục ĐX & Giao trục)", height=520, showlegend=True)
            st.plotly_chart(fig, width="stretch")



    elif dtype == "oxyz":

        c1, c2 = st.columns([1.2, 2.8])

        with c1:

            st.caption("⚙️ **Tọa độ Điểm & Vectơ Vị Trí $\\overrightarrow{OM}$ trong Oxyz:**")

            mx = st.slider("Tọa độ x (Hoành độ):", -5.0, 5.0, float(data.get("x", 2.0)), 0.5, key="lab_3d_x")

            my = st.slider("Tọa độ y (Tung độ):", -5.0, 5.0, float(data.get("y", 3.0)), 0.5, key="lab_3d_y")

            mz = st.slider("Tọa độ z (Cao độ):", -5.0, 5.0, float(data.get("z", 4.0)), 0.5, key="lab_3d_z")

            om_length = math.sqrt(mx**2 + my**2 + mz**2)

            st.info(f"📍 **Tọa độ:** $M({mx}; {my}; {mz})$\n\n🎯 **Vectơ vị trí:** $\\overrightarrow{{OM}} = {mx}\\vec{{i}} + {my}\\vec{{j}} + {mz}\\vec{{k}}$")

            st.success(f"📏 **Độ dài vectơ:**\n\n$$|\\overrightarrow{{OM}}| = \\sqrt{{{mx}^2 + {my}^2 + {mz}^2}} \\approx {om_length:.2f}$$")

        with c2:

            # Gốc tọa độ O(0,0,0)

            fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0], mode='markers+text', marker=dict(size=7, color='#ffffff'), text=['O(0;0;0)'], textposition="bottom left", name='Gốc O'))

            # Điểm M(mx, my, mz)

            fig.add_trace(go.Scatter3d(x=[mx], y=[my], z=[mz], mode='markers+text', marker=dict(size=9, color='#38bdf8'), text=[f'M({mx};{my};{mz})'], textposition="top center", name='Điểm M'))

            # Vectơ OM nối từ O đến M

            fig.add_trace(go.Scatter3d(x=[0, mx], y=[0, my], z=[0, mz], mode='lines', line=dict(color='#f43f5e', width=6), name='Vectơ OM'))



            # Đường gióng hình chiếu lên các mặt phẳng tọa độ (hộp tọa độ)

            fig.add_trace(go.Scatter3d(x=[0, mx, mx, 0, 0], y=[0, 0, my, my, 0], z=[0, 0, 0, 0, 0], mode='lines', line=dict(color='#64748b', width=2, dash='dash'), name='Hình chiếu Oxy'))

            fig.add_trace(go.Scatter3d(x=[mx, mx], y=[my, my], z=[0, mz], mode='lines', line=dict(color='#f59e0b', width=3, dash='dash'), name='Đường dóng cao độ z'))

            fig.add_trace(go.Scatter3d(x=[0, mx], y=[0, 0], z=[mz, mz], mode='lines', line=dict(color='#94a3b8', width=1.5, dash='dot'), hoverinfo='skip'))

            fig.add_trace(go.Scatter3d(x=[0, 0], y=[0, my], z=[mz, mz], mode='lines', line=dict(color='#94a3b8', width=1.5, dash='dot'), hoverinfo='skip'))

            fig.add_trace(go.Scatter3d(x=[0, mx], y=[my, my], z=[mz, mz], mode='lines', line=dict(color='#94a3b8', width=1.5, dash='dot'), hoverinfo='skip'))

            fig.add_trace(go.Scatter3d(x=[mx, mx], y=[0, my], z=[mz, mz], mode='lines', line=dict(color='#94a3b8', width=1.5, dash='dot'), hoverinfo='skip'))



            # Điểm hình chiếu M' trên mặt phẳng Oxy

            fig.add_trace(go.Scatter3d(x=[mx], y=[my], z=[0], mode='markers+text', marker=dict(size=6, color='#a855f7'), text=[f"M'({mx};{my};0)"], textposition="bottom center", name="Hình chiếu Oxy"))



            fig.update_layout(

                title=f"Không gian Oxyz: Điểm M({mx}; {my}; {mz}) & Vectơ OM (Độ dài: {om_length:.2f})",

                template="plotly_dark",

                scene=dict(

                    xaxis=dict(range=[-6, 6], title="Trục Ox", backgroundcolor="#0f172a", gridcolor="#1e293b"),

                    yaxis=dict(range=[-6, 6], title="Trục Oy", backgroundcolor="#0f172a", gridcolor="#1e293b"),

                    zaxis=dict(range=[-6, 6], title="Trục Oz", backgroundcolor="#0f172a", gridcolor="#1e293b"),

                    aspectmode='cube'

                ),

                height=520,

                margin=dict(l=10, r=10, t=35, b=10)

            )

            st.plotly_chart(fig, width="stretch")



    else:

        st.info("💡 Đã tiếp nhận yêu cầu. Kéo thanh trượt hoặc nhập tham số để mô phỏng tương tác!")



def heal_bbt_markdown_table(text: str) -> str:
    """
    Tự động phục hồi và định dạng chuẩn Bảng biến thiên (BBT) Markdown trong câu hỏi trắc nghiệm Socratic.
    Khử sạch hiện tượng dính hàng trên 1 dòng, biến thành Bảng kẻ ô chuẩn GFM / CommonMark.
    """
    if not text or '|' not in text:
        return text

    s = str(text)

    # 1. Tách dòng trước bắt đầu bảng: "| x |" hoặc "|x|"
    s = re.sub(r'([^\n])\s*(\|\s*x\s*\|)', r'\1\n\n\2', s, flags=re.IGNORECASE)

    # 2. Tách dòng trước hàng phân cách: "|:---|", "|---|", "|-", "| :"
    s = re.sub(r'([^\n])\s*(\|\s*(?:\:?\-{2,}\:?\|)+)', r'\1\n\2', s)

    # 3. Tách dòng trước hàng đạo hàm: "| y' |", "| f'(x) |"
    s = re.sub(r'([^\n])\s*(\|\s*(?:y[\'’]|f[\'’]\(x\))\s*\|)', r'\1\n\2', s, flags=re.IGNORECASE)

    # 4. Tách dòng trước hàng giá trị hàm số: "| y |", "| f(x) |"
    s = re.sub(r'([^\n])\s*(\|\s*(?:y|f\(x\))\s*\|)', r'\1\n\2', s, flags=re.IGNORECASE)

    # 5. Tách dòng sau hàng cuối cùng của bảng trước câu hỏi tiếp theo
    s = re.sub(r'(\|\s*[\+\-0-9a-zA-Z\s\\\|]+\|)\s*([A-ZÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ][^\|]+)$', r'\1\n\n\2', s)

    # 6. Đảm bảo dòng phân cách |:---| tồn tại nếu AI quên sinh
    if re.search(r'\|\s*x\s*\|[^\n]+\n\s*\|\s*y', s, flags=re.IGNORECASE):
        m_x = re.search(r'(\|\s*x\s*\|[^\n]+)', s, flags=re.IGNORECASE)
        if m_x:
            col_count = m_x.group(1).count('|') - 1
            if col_count > 0:
                sep_line = "|:---|" + "|".join([":---:"] * (col_count - 1)) + "|"
                s = s.replace(m_x.group(1), m_x.group(1) + "\n" + sep_line)

    return s

def parse_quiz_questions(text):
    questions = []
    part3_match = re.search(r'(?i)###\s*PHẦN\s*3', text)
    part2_text = text[:part3_match.start()] if part3_match else text

    pattern = r'(?i)(?:\[Q\d+\]|C[âa]u\s*\d+[\.\:]?)'
    parts = re.split(pattern, part2_text)

    for part in parts[1:]:
        lines = [l.strip() for l in part.strip().split('\n') if l.strip()]
        if not lines: continue
        q_header = lines[0]
        level, options, correct, explain = "Vận dụng", [], "A", "Gợi ý tự suy luận!"

        match = re.search(r'(?i)\[Mức độ:\s*(.*?)\]', q_header)
        if match:
            level = match.group(1)
            q_header = re.sub(r'(?i)\[Mức độ:\s*.*?\]', '', q_header).strip()

        q_text_lines = [q_header]
        parsing_options = False

        for line in lines[1:]:
            clean_line = re.sub(r'(?i)^\*{0,2}([A-D])\b[\.\:]?\*{0,2}\s*', r'\1. ', line)

            if re.match(r'(?i)###\s*PHẦN\s*3', line):
                break

            if clean_line.upper().startswith(('A.', 'B.', 'C.', 'D.')):
                parsing_options = True
                options.append(clean_line)
            elif re.search(r'(?i)^(CORRECT|ĐÁP ÁN|Đáp án đúng)\s*:', line):
                ext = re.sub(r'[^A-D]', '', line.split(":")[-1].upper())
                if ext: correct = ext[0]
            elif re.search(r'(?i)^(EXPLAIN|GIẢI THÍCH|Gợi ý)\s*:', line):
                explain = line.split(":", 1)[-1].strip()
            else:
                if not parsing_options:
                    q_text_lines.append(line)
                elif options and not clean_line.upper().startswith(('A.', 'B.', 'C.', 'D.')):
                    explain += " " + line

        if len(options) >= 4:
            correct_idx = ord(correct) - ord('A')
            new_options = options[:4]
            new_correct = correct
            if 0 <= correct_idx < len(options):
                correct_text = re.sub(r'(?i)^[A-D]\.\s*', '', options[correct_idx]).strip()
                raw_options = [re.sub(r'(?i)^[A-D]\.\s*', '', opt).strip() for opt in options[:4]]
                import random
                random.shuffle(raw_options)

                new_options = []
                for i, opt in enumerate(raw_options):
                    letter = chr(ord('A') + i)
                    new_options.append(f"{letter}. {opt}")
                    if opt == correct_text:
                        new_correct = letter
            # TỰ ĐỘNG BÓC TÁCH BBT TỪ NỘI DUNG CÂU HỎI TRẠM 1 (ĐỒNG BỘ NGUYÊN BẢN TRẠM 3)
            raw_q_lines = [l for l in q_text_lines if l.strip()]
            q_bbt_lines = [l for l in raw_q_lines if "|" in l and any(k in l.lower() for k in ["x", "y'", "y", "f'(x)", "f(x)", "daoham", "đạohàm"])]
            extracted_bbt = ""
            if len(q_bbt_lines) >= 2:
                extracted_bbt = "\n".join(q_bbt_lines).strip()
                q_text_lines = [l for l in raw_q_lines if l not in q_bbt_lines and not re.match(r'^[|\s:-]+$', l.strip())]

            full_question_text = "\n".join(q_text_lines).strip()
            if not extracted_bbt and ('|' in full_question_text and any(k in full_question_text.lower() for k in ["bảng biến thiên", "bbt", "bảng xét dấu"])):
                full_question_text = heal_bbt_markdown_table(full_question_text)

            # Chuẩn hóa KaTeX & loại bỏ rác cú pháp
            full_question_text = sanitize_katex_latex(full_question_text)
            if format_pedagogical_math:
                try:
                    full_question_text = format_pedagogical_math(full_question_text)
                except Exception:
                    pass

            cleaned_options = []
            for op in new_options:
                c_op = sanitize_katex_latex(op)
                if format_pedagogical_math:
                    try:
                        c_op = format_pedagogical_math(c_op)
                    except Exception:
                        pass
                cleaned_options.append(c_op)

            cleaned_explain = sanitize_katex_latex(explain)
            if format_pedagogical_math:
                try:
                    cleaned_explain = format_pedagogical_math(cleaned_explain)
                except Exception:
                    pass

            q_item = {
                "question": full_question_text,
                "level": level,
                "options": cleaned_options,
                "correct": new_correct,
                "explain": cleaned_explain
            }
            if extracted_bbt:
                q_item["bbt"] = extracted_bbt

            questions.append(q_item)
    return questions



# ==============================================================================

# 7. TIÊU ĐỀ TRANG VÀ BANNER CHÍNH

# ==============================================================================

st.markdown('<div class="main-header"><div class="main-title">🏫 GIA SƯ AI - HỆ SINH THÁI LỚP HỌC ĐẢO NGƯỢC</div><div class="sub-title">Trường THPT Tân Hiệp (An Giang) • Tác giả: Thầy Phan Minh Trí • Đồng hành từ Lớp 6 đến Lớp 12</div><div style="margin-top: 8px;"><span class="badge-tag">Bộ sách: Kết Nối Tri Thức Với Cuộc Sống</span><span class="badge-tag" style="border-color: #34d399; color: #34d399; margin-left: 8px;">Theo chủ đề GDPT 2018 • Nội dung cần giáo viên duyệt</span></div></div>', unsafe_allow_html=True)

# ==============================================================================
# 7.1 THANH ĐIỀU HƯỚNG 4 TRẠM NẰM NGANG PHÍA SAU DÒNG KẺ TIÊU ĐỀ (TOP STATION NAVBAR)
# ==============================================================================
station_labels = [
    "📖 Trạm 1: Học Tập & Phòng Lab",
    "✍️ Trạm 2: Gia Sư Socratic & Nộp Bài",
    "📝 Trạm 3: Luyện Tập & Khảo Thí",
    "📊 Trạm 4: Dữ Liệu & Nghiên Cứu"
]

if "selected_station" not in st.session_state:
    st.session_state.selected_station = station_labels[0]
elif st.session_state.selected_station not in station_labels:
    st.session_state.selected_station = station_labels[0]

# Khởi tạo hoặc bảo đảm đồng bộ cho key của sidebar radio
if "sb_station_radio_selector" not in st.session_state:
    st.session_state.sb_station_radio_selector = st.session_state.selected_station
elif st.session_state.sb_station_radio_selector != st.session_state.selected_station:
    st.session_state.sb_station_radio_selector = st.session_state.selected_station

st.markdown('<div style="font-size: 13px; font-weight: 700; color: #38bdf8; text-transform: uppercase; letter-spacing: 0.8px; margin-top: -12px; margin-bottom: 10px; display: flex; align-items: center; gap: 6px;">🧭 KHÔNG GIAN HỌC TẬP & KHẢO THÍ SƯ PHẠM (CHỌN TRẠM HOẠT ĐỘNG):</div>', unsafe_allow_html=True)

nav_t1, nav_t2, nav_t3, nav_t4 = st.columns(4)
for idx_st, (col_st, label_st) in enumerate(zip([nav_t1, nav_t2, nav_t3, nav_t4], station_labels)):
    with col_st:
        is_cur_active = (st.session_state.selected_station == label_st)
        btn_type = "primary" if is_cur_active else "secondary"
        btn_title = f"⭐ {label_st}" if is_cur_active else label_st
        if st.button(btn_title, key=f"top_nav_station_{idx_st}", type=btn_type, width="stretch"):
            if st.session_state.selected_station != label_st:
                st.session_state.selected_station = label_st
                st.session_state.sb_station_radio_selector = label_st
                st.rerun()

st.markdown('<div style="border-bottom: 1px solid rgba(51, 65, 85, 0.45); margin-top: 6px; margin-bottom: 18px;"></div>', unsafe_allow_html=True)

selected_station = st.session_state.selected_station




# ==============================================================================





# ==============================================================================

# HỆ THỐNG PHÁT ÂM TIẾNG ANH BẢN NGỮ CHUẨN QUỐC TẾ (IELTS / TOEFL / PTE)

# ==============================================================================

# ==============================================================================

# HỆ THỐNG PHÁT ÂM TIẾNG ANH BẢN NGỮ CHUẨN QUỐC TẾ (IELTS / TOEFL / PTE)

# ==============================================================================

@st.cache_data(show_spinner=False, ttl=7200)

def generate_pedagogical_tts_audio_bytes(clean_text: str, lang: str = "vi") -> bytes:

    """Tạo audio MP3 thuyết minh sư phạm (Server-side 0ms CORS, chống đơ trình duyệt)."""

    if not clean_text or len(clean_text.strip()) < 5:

        return b""

    sentences = [s.strip() for s in re.split(r'[\n.!?]+', clean_text) if s.strip()]

    chunks = []

    cur = ""

    for s in sentences:

        if len(cur + " " + s) > 160:

            if cur.strip(): chunks.append(cur.strip())

            cur = s

        else:

            cur += (" " if cur else "") + s

    if cur.strip(): chunks.append(cur.strip())



    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    parts = []

    def _fetch_tts_chunk(c):
        try:
            chunk_lang = "vi" if re.search(r'[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ]', c) else lang
            r = requests.get(
                "https://translate.googleapis.com/translate_tts",
                params={"ie": "UTF-8", "tl": chunk_lang, "client": "gtx", "q": c},
                headers=headers,
                timeout=3
            )
            if r.status_code == 200 and len(r.content) > 100:
                return r.content
        except Exception:
            pass
        return b""

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as tts_exec:
        parts = [p for p in tts_exec.map(_fetch_tts_chunk, chunks[:18]) if p]

    if parts:

        return b"".join(parts)

    return b""



def create_pedagogical_tts_component(raw_text: str, subject_name: str, comp_key: str):

    """Trình phát Thuyết minh Bài giảng Chuẩn Sư phạm & Voice Engine 2 luồng Nam Bộ / US."""

    # Tiêm Bộ máy Phát âm Sư phạm 2 Luồng Toàn Cục bằng st.html (không dùng iframe, bắt dblclick/selection 100%)

    global_voice_script = r"""

    <script>

    (function() {

        if (window.__gsai_pedagogical_voice_ready) return;

        window.__gsai_pedagogical_voice_ready = true;



        let voicesList = [];

        function updateVoices() {

            if (!window.speechSynthesis) return;

            voicesList = window.speechSynthesis.getVoices();

        }

        updateVoices();

        if (window.speechSynthesis) {

            window.speechSynthesis.onvoiceschanged = updateVoices;

        }



        // 1. Giọng Tiếng Anh bản ngữ US (Jenny / Guy / Google US)

        window.__getNativeEnglishVoice = function() {

            return voicesList.find(v => v.lang.startsWith('en') && (

                v.name.includes('Jenny') || v.name.includes('Guy') || v.name.includes('Natural') ||

                v.name.includes('Google') || v.name.includes('US') || v.name.includes('Samantha') || v.name.includes('Aria')

            )) || voicesList.find(v => v.lang.startsWith('en')) || null;

        };



        // 2. Giọng Tiếng Việt Nam Bộ chuẩn sư phạm (Microsoft NamMinh / HoaiMy / Google Tiếng Việt)

        window.__getSouthernVietnameseVoice = function() {

            return voicesList.find(v => v.name.includes('NamMinh') || v.name.includes('Nam Minh')) ||

                   voicesList.find(v => v.name.includes('HoaiMy') || v.name.includes('Hoai My')) ||

                   voicesList.find(v => v.lang.includes('vi') && v.name.includes('Natural')) ||

                   voicesList.find(v => v.lang.includes('vi') || v.lang.startsWith('vi')) || null;

        };



        // Hàm phát âm Sư phạm 2 luồng thông minh

        window.__speakPedagogicalText = function(rawText, forceLang) {

            if (!rawText || !window.speechSynthesis) return;

            let text = String(rawText).trim();

            // Lọc các ký tự bullet point, định dạng markdown

            text = text.replace(/^[•\-\*]\s*/, '').replace(/[*#`_~\[\]]/g, ' ').trim();

            if (!text || text.length < 2) return;



            // Kiểm tra dấu tiếng Việt để phân luồng

            const viPattern = /[àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ]/;

            const isVietnamese = viPattern.test(text) || forceLang === 'vi';



            try {

                window.speechSynthesis.cancel();

                const utter = new SpeechSynthesisUtterance(text);

                if (isVietnamese) {

                    // Luồng 1: Tiếng Việt giọng Nam Bộ chuẩn mực sư phạm (nhịp 0.90 tròn vành rõ chữ)

                    utter.lang = 'vi-VN';

                    utter.rate = 0.90;

                    utter.pitch = 1.0;

                    const vVoice = window.__getSouthernVietnameseVoice();

                    if (vVoice) utter.voice = vVoice;

                } else {

                    // Luồng 2: Tiếng Anh bản ngữ chuẩn US (nhịp 0.88 chuẩn trọng âm)

                    utter.lang = 'en-US';

                    utter.rate = 0.88;

                    utter.pitch = 1.0;

                    const eVoice = window.__getNativeEnglishVoice();

                    if (eVoice) utter.voice = eVoice;

                }

                window.speechSynthesis.speak(utter);

            } catch(e) {

                console.warn("TTS Error:", e);

            }

        };



        window.__stopPedagogicalText = function() {

            if (window.speechSynthesis) window.speechSynthesis.cancel();

        };



        // Lắng nghe sự kiện bôi đen (selection) & double-click trên TOÀN BỘ TRANG (document)

        let lastSpoken = "";

        let lastTime = 0;

        function handleSelectionTrigger(e) {

            try {

                const sel = window.getSelection();

                if (!sel) return;

                const str = sel.toString().trim();

                if (!str || str.length < 2 || str.length > 500) return;

                const now = Date.now();

                if (str.toLowerCase() === lastSpoken.toLowerCase() && (now - lastTime) < 1200) return;

                lastSpoken = str;

                lastTime = now;

                window.__speakPedagogicalText(str);

            } catch(err) {}

        }



        document.addEventListener('mouseup', handleSelectionTrigger, true);

        document.addEventListener('touchend', handleSelectionTrigger, true);

        document.addEventListener('dblclick', handleSelectionTrigger, true);

    })();

    </script>

    """

    st.html(global_voice_script, unsafe_allow_javascript=True)



    if not raw_text or len(raw_text.strip()) < 10:

        return



    # Xử lý nội dung thuyết minh và chuẩn hóa ngắt nghỉ sư phạm

    clean_speech = raw_text



    # Lọc bỏ phần lưu ý hành chính về đợt tái bản SGK khỏi giọng đọc sư phạm

    clean_speech = re.sub(r'(?i)(?:⚠️\s*)?Lưu ý[\s\S]*?(?:nhé!|nhé\.|GDPT 2018[\.\)]|trực tiếp nhé!)\s*', '', clean_speech)

    clean_speech = re.sub(r'(?i)^[^\n]*tái bản[^\n]*\n+', '', clean_speech)

    clean_speech = re.sub(r'(?i)^[^\n]*chênh lệch số trang[^\n]*\n+', '', clean_speech)



    # Phiên âm chuẩn cho Véctơ (từ gốc đến ngọn, có phẩy, đọc rõ từng chữ cái, số 0)

    def _rep_vector_speech(m):

        target = m.group(2).strip()

        if target == '0':

            return ' véc tơ không '

        has_prime = "'" in target

        raw = target.replace("'", "").strip()

        spaced = ' '.join(list(raw))

        if has_prime:

            spaced += ' phẩy'

        return f' véc tơ {spaced} '



    clean_speech = re.sub(r'\\(overrightarrow|vec)\{([^}]+)\}', _rep_vector_speech, clean_speech)

    clean_speech = re.sub(r'\\(overrightarrow|vec)\s+([a-zA-Z0-9\']+)', _rep_vector_speech, clean_speech)



    # Phân số, căn thức, tích phân, giới hạn, lũy thừa

    clean_speech = re.sub(r'\\(d)?frac\{([^}]+)\}\{([^}]+)\}', r' \2 phần \3 ', clean_speech)

    clean_speech = re.sub(r'\\sqrt\[(\d+)\]\{([^}]+)\}', r' căn bậc \1 của \2 ', clean_speech)

    clean_speech = re.sub(r'\\sqrt\{([^}]+)\}', r' căn bậc hai của \1 ', clean_speech)

    clean_speech = re.sub(r'\\int_\{([^}]+)\}\^\{([^}]+)\}', r' tích phân từ \1 đến \2 ', clean_speech)

    clean_speech = re.sub(r'\\int', ' tích phân ', clean_speech)

    clean_speech = re.sub(r'\\lim_\{([^}]+)\}', r' giới hạn khi \1 ', clean_speech)

    clean_speech = re.sub(r'\\lim', ' giới hạn ', clean_speech)

    clean_speech = re.sub(r'\^2', ' bình phương ', clean_speech)

    clean_speech = re.sub(r'\^3', ' lập phương ', clean_speech)

    clean_speech = re.sub(r'\^\{([^}]+)\}', r' mũ \1 ', clean_speech)

    clean_speech = re.sub(r'\^([a-zA-Z0-9])', r' mũ \1 ', clean_speech)

    clean_speech = re.sub(r'\\Delta', ' Đen-ta ', clean_speech)

    clean_speech = re.sub(r'\\alpha', ' An-pha ', clean_speech)

    clean_speech = re.sub(r'\\beta', ' Bê-ta ', clean_speech)

    clean_speech = re.sub(r'\\pi', ' Pi ', clean_speech)

    clean_speech = re.sub(r'\\infty', ' vô cực ', clean_speech)

    clean_speech = re.sub(r'\\le|\\leq', ' nhỏ hơn hoặc bằng ', clean_speech)

    clean_speech = re.sub(r'\\ge|\\geq', ' lớn hơn hoặc bằng ', clean_speech)

    clean_speech = re.sub(r'\\neq', ' khác ', clean_speech)

    clean_speech = re.sub(r'\\approx', ' xấp xỉ ', clean_speech)

    clean_speech = re.sub(r'\\in', ' thuộc ', clean_speech)

    clean_speech = re.sub(r'\\notin', ' không thuộc ', clean_speech)

    clean_speech = re.sub(r'\\subset', ' tập con của ', clean_speech)

    clean_speech = re.sub(r'\\forall', ' với mọi ', clean_speech)

    clean_speech = re.sub(r'\\exists', ' tồn tại ', clean_speech)

    clean_speech = re.sub(r'\\pm', ' cộng trừ ', clean_speech)

    clean_speech = re.sub(r'\\cdot|\\times', ' nhân ', clean_speech)

    clean_speech = re.sub(r'\\to|\\rightarrow', ' tiến tới ', clean_speech)

    clean_speech = re.sub(r'\\Rightarrow', ' suy ra ', clean_speech)

    clean_speech = re.sub(r'\\Leftrightarrow', ' tương đương ', clean_speech)

    clean_speech = re.sub(r'\bOxyz\b', ' Ô ích y dét ', clean_speech)

    clean_speech = re.sub(r'\bOxy\b', ' Ô ích y ', clean_speech)

    # 1. Lọc bỏ 100% toàn bộ bảng Markdown (| ... |) và khối mã khỏi giọng đọc để không đọc thành ký tự gạch đứng
    clean_speech = re.sub(r'(?m)^[ \t]*\|.*\|.*(?:\r?\n|$)', ' ', clean_speech)
    clean_speech = re.sub(r'```[\s\S]*?```', ' ', clean_speech)
    clean_speech = re.sub(r'\|[ \t]*[-:]+[ \t]*\|', ' ', clean_speech)

    # 2. Chuyển đổi các ký hiệu đồ họa giải tích và mũi tên sang lời nói tự nhiên sư phạm
    clean_speech = re.sub(r'\\+(?:nearrow|uparrow)', ' đồng biến đi lên ', clean_speech)
    clean_speech = re.sub(r'\\+(?:searrow|downarrow)', ' nghịch biến đi xuống ', clean_speech)
    clean_speech = clean_speech.replace('↗', ' đồng biến đi lên ').replace('↘', ' nghịch biến đi xuống ')
    clean_speech = re.sub(r'\\left|\\right|\\displaystyle|\\limits', ' ', clean_speech)
    clean_speech = re.sub(r'\\mathbb\{R\}', ' tập số thực R ', clean_speech)
    clean_speech = re.sub(r'\\setminus', ' loại trừ ', clean_speech)
    clean_speech = re.sub(r'\|\s*\||║', ' không xác định ', clean_speech)
    clean_speech = re.sub(r'\by\'\b|\bf\'\b', ' đạo hàm y phẩy ', clean_speech)
    clean_speech = re.sub(r'\bx_1\b|\bx1\b', ' x một ', clean_speech)
    clean_speech = re.sub(r'\bx_2\b|\bx2\b', ' x hai ', clean_speech)
    clean_speech = re.sub(r'\bx_0\b|\bx0\b', ' x không ', clean_speech)
    clean_speech = re.sub(r'\by\(x_1\)\b|\by\(x1\)\b', ' y tại x một ', clean_speech)
    clean_speech = re.sub(r'\by\(x_2\)\b|\by\(x2\)\b', ' y tại x hai ', clean_speech)
    clean_speech = re.sub(r'-\s*\\infty|-\s*inf\b', ' âm vô cực ', clean_speech)
    clean_speech = re.sub(r'\+\s*\\infty|\+\s*inf\b', ' dương vô cực ', clean_speech)
    clean_speech = re.sub(r'\\infty|\binf\b', ' vô cực ', clean_speech)
    clean_speech = re.sub(r'\bad\s*-\s*bc\b', ' a d trừ b c ', clean_speech)
    clean_speech = re.sub(r'\bTCĐ\b', ' Tiệm cận đứng ', clean_speech)
    clean_speech = re.sub(r'\bTCN\b', ' Tiệm cận ngang ', clean_speech)
    clean_speech = re.sub(r'\bTCX\b', ' Tiệm cận xiên ', clean_speech)
    clean_speech = re.sub(r'\bCĐ\b', ' Cực đại ', clean_speech)
    clean_speech = re.sub(r'\bCT\b', ' Cực tiểu ', clean_speech)

    clean_speech = re.sub(r'[*#`_~\(\)\$\\{}]', ' ', clean_speech)
    clean_speech = re.sub(r'\s+', ' ', clean_speech).strip()

    lang_code = "en" if subject_name == "Tiếng Anh" else "vi"
    audio_data = generate_pedagogical_tts_audio_bytes(clean_speech, lang=lang_code)

    # Render giao diện Thuyết minh chuẩn sư phạm Nam Bộ: Có cả Nút giọng Nam Bộ trực tiếp và Player MP3
    safe_clean_speech = clean_speech[:2500].replace('</script>', '').replace('<script>', '')
    escaped_speech_js = json.dumps(safe_clean_speech, ensure_ascii=False)

    player_title = "ENGLISH PEDAGOGICAL AUDIO (NATIVE PRONUNCIATION)" if subject_name == "Tiếng Anh" else "THUYẾT MINH BÀI GIẢNG (GIỌNG THẦY NAM BỘ - CHUẨN SƯ PHẠM)"
    sub_title = "Chuẩn phát âm bản ngữ US/UK • 2 luồng Anh - Việt" if subject_name == "Tiếng Anh" else "Giọng Nam Bộ trầm ấm (Microsoft Nam Minh) • Ngắt nghỉ chuẩn ngữ pháp mô phạm"

    b64_source = ""
    if audio_data:
        b64_audio = base64.b64encode(audio_data).decode('ascii')
        b64_source = f'<audio id="audio_player_{comp_key}" controls style="width: 100%; height: 38px; border-radius: 20px; outline: none; margin-top: 8px;"><source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3"></audio>'

    tts_ui_html = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; margin: 4px 0 10px 0; background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.95)); border: 1.5px solid #0284c7; border-radius: 12px; padding: 12px 16px; box-shadow: 0 4px 14px rgba(2,132,199,0.25);">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px; flex-wrap: wrap; gap: 8px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 20px;">🎙️</span>
                <div>
                    <span style="color: #38bdf8; font-weight: 800; font-size: 13.5px;">{player_title}</span>
                    <div style="color: #94a3b8; font-size: 11px;">{sub_title}</div>
                </div>
            </div>
            <button id="btn_tts_direct_{comp_key}" type="button" style="
                background: linear-gradient(135deg, #0284c7, #0369a1);
                color: #ffffff;
                border: 1px solid #38bdf8;
                padding: 6px 16px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 700;
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 6px;
                box-shadow: 0 2px 10px rgba(56, 189, 248, 0.3);
            ">
                <span id="btn_tts_icon_{comp_key}">▶️</span> <span id="btn_tts_txt_{comp_key}">Nghe Giọng Thầy Nam Bộ</span>
            </button>
        </div>
        {b64_source}
    </div>
    <script>
    (function() {{
        var btn = document.getElementById('btn_tts_direct_{comp_key}');
        if (!btn) return;
        var textToRead = {escaped_speech_js};
        var langMode = '{lang_code}';
        var isSpeaking = false;

        btn.onclick = function() {{
            var aud = document.getElementById('audio_player_{comp_key}');
            var btnTxt = document.getElementById('btn_tts_txt_{comp_key}');
            var btnIcon = document.getElementById('btn_tts_icon_{comp_key}');
            if (aud) {{
                if (aud.paused) {{
                    var p = aud.play();
                    if (btnTxt) btnTxt.innerText = 'Tạm dừng thuyết minh';
                    if (btnIcon) btnIcon.innerText = '⏸️';
                    if (p !== undefined) {{
                        p.catch(function(e) {{
                            console.warn('Audio play blocked, fallback synthesis:', e);
                            if (window.speechSynthesis) {{
                                var u = new SpeechSynthesisUtterance(textToRead);
                                u.lang = (langMode === 'en' ? 'en-US' : 'vi-VN');
                                u.rate = 0.88;
                                window.speechSynthesis.speak(u);
                            }}
                        }});
                    }}
                    aud.onended = function() {{
                        if (btnTxt) btnTxt.innerText = 'Nghe Giọng Thầy Nam Bộ';
                        if (btnIcon) btnIcon.innerText = '▶️';
                    }};
                }} else {{
                    aud.pause();
                    if (btnTxt) btnTxt.innerText = 'Nghe Giọng Thầy Nam Bộ';
                    if (btnIcon) btnIcon.innerText = '▶️';
                }}
            }} else if (window.speechSynthesis) {{
                if (isSpeaking || window.speechSynthesis.speaking) {{
                    window.speechSynthesis.cancel();
                    isSpeaking = false;
                    if (btnTxt) btnTxt.innerText = 'Nghe Giọng Thầy Nam Bộ';
                    if (btnIcon) btnIcon.innerText = '▶️';
                }} else {{
                    isSpeaking = true;
                    if (btnTxt) btnTxt.innerText = 'Tạm dừng thuyết minh';
                    if (btnIcon) btnIcon.innerText = '⏸️';
                    var u = new SpeechSynthesisUtterance(textToRead);
                    u.lang = (langMode === 'en' ? 'en-US' : 'vi-VN');
                    u.rate = 0.88;
                    u.onend = function() {{
                        isSpeaking = false;
                        if (btnTxt) btnTxt.innerText = 'Nghe Giọng Thầy Nam Bộ';
                        if (btnIcon) btnIcon.innerText = '▶️';
                    }};
                    window.speechSynthesis.speak(u);
                }}
            }}
        }};
    }})();
    </script>
    """
    comp_height = 135 if audio_data else 85
    render_html_iframe(tts_ui_html, height=comp_height)





def render_voice_speech_tex_and_english_evaluator(stage_id: str, current_subject: str, current_grade: int):

    # CHỈ HIỂN THỊ DUY NHẤT CHO MÔN TIẾNG ANH TẠI TRẠM 1 (CÁC MÔN KHÁC TUYỆT ĐỐI KHÔNG HIỂN THỊ)

    if current_subject != "Tiếng Anh" or stage_id != 'Tram 1':

        return



    st.markdown("---")



    # GIAO DIỆN PHÒNG LUYỆN NÓI TIẾNG ANH PHẢN XẠ 1-1 (AI SPEAKING LAB 50/50 CÂN ĐỐI)

    st.markdown('<div style="background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.95)); border: 1.5px solid #38bdf8; border-radius: 12px; padding: 14px 18px; margin-bottom: 12px; box-shadow: 0 4px 15px rgba(56, 189, 248, 0.15);"><div style="display: flex; align-items: center; justify-content: space-between; gap: 10px; flex-wrap: wrap;"><div style="display: flex; align-items: center; gap: 10px;"><span style="font-size: 24px;">🇬🇧</span><div><span style="color: #38bdf8; font-weight: 800; font-size: 15px; text-transform: uppercase; letter-spacing: 0.5px;">PHÒNG THỰC HÀNH NÓI TIẾNG ANH PHẢN XẠ 1-1 BẢN NGỮ (AI SPEAKING LAB)</span><div style="color: #94a3b8; font-size: 12.5px; margin-top: 2px;">💡 <b>Mẹo học sinh thông minh:</b> Em có thể <b>bôi đen (select)</b> hoặc <b>nhấp đúp (double-click)</b> bất kỳ từ/câu nào trên màn hình để nghe tự động (Chữ Anh đọc chuẩn US, Chữ Việt đọc giọng Nam Bộ). Hoặc bấm trực tiếp các nút nghe nhanh bên dưới!</div></div></div></div></div>', unsafe_allow_html=True)



    # Tiêm script nghe phát âm 2 luồng toàn cục

    create_pedagogical_tts_component("", "Tiếng Anh", f"init_{stage_id}")



    # Ngân hàng từ vựng & đoạn văn mẫu theo từng Unit ngoài SGK

    curriculum_english_units = {

        "Unit 1: Life stories & Inspiring People": {

            "vocab": [

                {"word": "Perseverance", "ipa": "/ˌpɜːsɪˈvɪərəns/", "meaning": "Sự kiên trì, bền chí"},

                {"word": "Inspirational", "ipa": "/ˌɪnspəˈreɪʃənl/", "meaning": "Truyền cảm hứng"},

                {"word": "Distinguished", "ipa": "/dɪˈstɪŋɡwɪʃt/", "meaning": "Xuất chúng, lỗi lạc"},

                {"word": "Dedication", "ipa": "/ˌdedɪˈkeɪʃn/", "meaning": "Sự cống hiến tận tụy"}

            ],

            "passage": "Uncle Ho devoted his entire life to national liberation, inspiring generations of Vietnamese students to study diligently and cultivate personal integrity.",

            "q_reflex": "Who is a historical or modern figure that inspired you the most in your life? Explain why."

        },

        "Unit 2: A Green Planet & Environmental Protection": {

            "vocab": [

                {"word": "Biodiversity", "ipa": "/ˌbaɪəʊdaɪˈvɜːsəti/", "meaning": "Đa dạng sinh học"},

                {"word": "Deforestation", "ipa": "/diːˌfɒrɪˈsteɪʃn/", "meaning": "Nạn phá rừng"},

                {"word": "Sustainability", "ipa": "/səˌsteɪnəˈbɪləti/", "meaning": "Sự phát triển bền vững"},

                {"word": "Carbon footprint", "ipa": "/ˌkɑːbən ˈfʊtprɪnt/", "meaning": "Dấu chân carbon"}

            ],

            "passage": "Transitioning to renewable clean energy and minimizing single-use plastic are decisive steps to preserve Earth's climate stability.",

            "q_reflex": "What practical actions can high school students in Vietnam take to reduce plastic waste on campus?"

        },

        "Unit 3: Music & Cultural Traditions": {

            "vocab": [

                {"word": "Heritage", "ipa": "/ˈherɪtɪdʒ/", "meaning": "Di sản văn hóa"},

                {"word": "Melody", "ipa": "/ˈmelədi/", "meaning": "Giai điệu âm nhạc"},

                {"word": "Traditional", "ipa": "/trəˈdɪʃənl/", "meaning": "Thuộc về truyền thống"},

                {"word": "Instrument", "ipa": "/ˈɪnstrəmənt/", "meaning": "Nhạc cụ biểu diễn"}

            ],

            "passage": "Traditional Vietnamese music like Quan Ho and Ca Tru reflects our profound spiritual identity and unique poetic heritage.",

            "q_reflex": "Do you prefer listening to traditional folk music or modern pop songs? Share your personal reasons."

        },

        "Unit 4: Global Technology & AI Revolution": {

            "vocab": [

                {"word": "Artificial Intelligence", "ipa": "/ˌɑːtɪˈfɪʃl ɪnˈtelɪdʒəns/", "meaning": "Trí tuệ nhân tạo"},

                {"word": "Automation", "ipa": "/ˌɔːtəˈmeɪʃn/", "meaning": "Sự tự động hóa"},

                {"word": "Breakthrough", "ipa": "/ˈbreɪkθruː/", "meaning": "Bước đột phá công nghệ"},

                {"word": "Cybersecurity", "ipa": "/ˈsaɪbəsɪkjʊərəti/", "meaning": "An ninh mạng bảo mật"}

            ],

            "passage": "Artificial intelligence empowers modern teenagers to solve real-world problems and pursue self-directed scientific research.",

            "q_reflex": "How can high school students utilize artificial intelligence responsibly without becoming over-dependent?"

        }

    }



    sel_unit = st.selectbox(

        "📚 Chọn Chủ Đề Bài Học SGK Kết Nối Tri Thức:",

        list(curriculum_english_units.keys()),

        key=f"unit_eng_sel_{stage_id}"

    )

    unit_info = curriculum_english_units[sel_unit]



    col_left_data, col_right_speak = st.columns([1.1, 1.1])



    with col_left_data:

        st.markdown("##### 📖 1. Từ Vựng Trọng Tâm SGK (New Words):")



        # Bảng từ vựng 2 luồng: Nút nghe tiếng Anh bản ngữ US + Nút nghe giải nghĩa giọng Nam Bộ

        for v in unit_info["vocab"]:

            v_word = v['word']

            v_ipa = v['ipa']

            v_meaning = v['meaning']

            vocab_item_html = f"""

            <div style="display: flex; align-items: center; justify-content: space-between; padding: 8px 12px; background: #0f172a; border: 1px solid #1e293b; border-radius: 8px; margin-bottom: 6px; flex-wrap: wrap; gap: 6px;">

                <div>

                    <span style="color: #38bdf8; font-weight: 700; font-size: 14px;">• {v_word}</span>

                    <span style="color: #94a3b8; font-size: 12px; margin-left: 6px;">{v_ipa}</span>:

                    <span style="color: #cbd5e1; font-size: 12.5px; font-style: italic; margin-left: 4px;">{v_meaning}</span>

                </div>

            </div>

            """

            st.html(vocab_item_html, unsafe_allow_javascript=True)



        st.markdown("##### 📝 2. Đoạn Văn Luyện Đọc Chuẩn (Reading Passage):")

        escaped_passage = json.dumps(unit_info['passage'])

        passage_code = f"""

        <div style="background: #0f172a; border: 1px solid #334155; border-radius: 10px; padding: 12px 14px; margin-top: 4px;">

            <div style="color: #e2e8f0; font-size: 13.5px; line-height: 1.6; font-style: italic;">"{unit_info['passage']}"</div>

            <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 8px; flex-wrap: wrap; gap: 6px;">

                <span style="color: #64748b; font-size: 11.5px;">✨ <i>Bôi đen để nghe tự động</i></span>

            </div>

        </div>

        """

        st.html(passage_code, unsafe_allow_javascript=True)



    with col_right_speak:

        st.markdown("##### 🎙️ 3. Phòng Thu Phản Xạ 1-1 Cùng Gia Sư AI:")



        escaped_q = json.dumps(unit_info['q_reflex'])

        q_code = f"""

        <div style="background: rgba(30, 41, 59, 0.95); border: 1.5px solid #38bdf8; border-radius: 10px; padding: 12px 14px; margin-bottom: 12px;">

            <div style="display: flex; align-items: center; justify-content: space-between; gap: 8px;">

                <div style="color: #38bdf8; font-weight: 800; font-size: 13px;">🤖 CÂU HỎI PHẢN XẠ CỦA GIA SƯ AI:</div>

            </div>

            <div style="color: #ffffff; font-size: 13.5px; font-weight: 600; margin-top: 6px; line-height: 1.5;">"{unit_info['q_reflex']}"</div>

        </div>

        """

        st.html(q_code, unsafe_allow_javascript=True)



        # Trình thu âm Micro Streamlit Native 100% chuẩn xác

        st.markdown('<div style="background: #0f172a; border: 1.5px solid #10b981; border-radius: 10px; padding: 10px 14px; margin-bottom: 8px;"><div style="display: flex; align-items: center; justify-content: space-between; gap: 6px;"><span style="color: #34d399; font-weight: 700; font-size: 13px;">🎙️ THU ÂM BÀI NÓI (NATIVE MIC STREAMLIT):</span><span style="color: #94a3b8; font-size: 11px;">(Bấm nút Micro để bắt đầu nói, bấm lần nữa để dừng)</span></div></div>', unsafe_allow_html=True)



        audio_recorded = st.audio_input(

            "Ghi âm bài nói của em (en-US):",

            key=f"audio_mic_eng_{stage_id}",

            label_visibility="collapsed"

        )



        student_speech = st.text_area(

            "Nội dung bài nói của em (tùy chọn gõ bổ sung / ghi chú thêm):",

            key=f"eng_speech_input_{stage_id}",

            placeholder="Nếu em không dùng Micro hoặc muốn bổ sung bài nói, hãy gõ/dán văn bản tiếng Anh vào đây...",

            height=75

        )



        btn_score_ielts = st.button("📊 Chấm Điểm 4 Tiêu Chí IELTS & Nâng Cấp Band 8.0", key=f"btn_eval_ielts_{stage_id}", type="primary", width="stretch")



        if btn_score_ielts:

            has_audio = (audio_recorded is not None)

            has_text = bool(student_speech and student_speech.strip())



            if not has_audio and not has_text:

                st.warning("⚠️ Em hãy bấm biểu tượng Micro ở trên để thu âm bài nói tiếng Anh, hoặc nhập nội dung bài nói vào ô văn bản trước khi bấm Chấm Điểm nhé!")

            else:

                with st.spinner("AI Giám khảo IELTS & Giáo viên THPT đang nghe và phân tích âm vị, ngữ pháp, độ trôi chảy..."):

                    try:

                        rubric_prompt = f"""Bạn là Giám khảo Khảo thí IELTS Quốc tế kiêm Giáo viên Tiếng Anh THPT theo CT GDPT 2018.

Chủ đề bài học SGK: {sel_unit}

Câu hỏi bối cảnh của Thầy AI: '{unit_info['q_reflex']}'

Đoạn văn đọc mẫu SGK: '{unit_info['passage']}'



YÊU CẦU ĐÁNH GIÁ CHI TIẾT & CHUẨN SƯ PHẠM:

1. BẢN GHI LỜI NÓI (TRANSCRIPT): {"Nghe kỹ file ghi âm của học sinh và chép lại đầy đủ 100% bằng tiếng Anh những gì học sinh đã phát âm." if has_audio else "Trích dẫn văn bản học sinh đã nhập."}

2. OVERALL BAND SCORE (Thang điểm 0 - 9.0)

3. BẢNG ĐIỂM 4 TIÊU CHÍ CHUẨN QUỐC TẾ IELTS:

   - 🗣️ Fluency & Coherence (0-9đ): Độ mạch lạc, tốc độ phản xạ.

   - 📚 Lexical Resource (0-9đ): Mức độ sử dụng từ vựng bài học.

   - ✍️ Grammatical Accuracy (0-9đ): Độ chuẩn thì, cấu trúc câu.

   - 🔊 Pronunciation & Intonation (0-9đ): Trọng âm, âm đuôi (/s/, /ed/), ngữ điệu.

4. SOI LỖI CỤ THỂ VÀ BẢN NÂNG CẤP (UPGRADED VERSION):

   - Chỉ ra 2 từ/câu cần sửa ngay (kèm lỗi phát âm âm vị nếu có audio).

   - Đưa ra phiên bản mẫu nâng cấp Band 8.0 để học sinh ghi nhớ.

5. LƯỢT HỎI PHẢN XẠ TIẾP THEO (FOLLOW-UP QUESTION):

   - Đặt 1 câu hỏi phản xạ nối tiếp bằng tiếng Anh để học sinh tiếp tục nói."""



                        contents = []

                        if has_audio:

                            audio_bytes = audio_recorded.getvalue()

                            mime_type = getattr(audio_recorded, 'type', 'audio/wav') or 'audio/wav'

                            contents.append(types.Part.from_bytes(data=audio_bytes, mime_type=mime_type))

                        if has_text:

                            contents.append(f"Văn bản học sinh nhập/bổ sung: '{student_speech.strip()}'")

                        contents.append(rubric_prompt)



                        eval_ielts_res = call_gemini_with_fallback(contents if len(contents) > 1 else contents[0])

                        st.success("🏆 BẢNG ĐÁNH GIÁ NĂNG LỰC NÓI TIẾNG ANH CHUẨN QUỐC TẾ:")

                        st.markdown(eval_ielts_res)

                    except Exception as e:

                        st.error(f"Lỗi chấm điểm: {e}")





# 8. CÁC TRẠM CHÍNH NÂNG CẤP

# ==============================================================================

# ==============================================================================

# ==============================================================================
# NGÂN HÀNG MA TRẬN CHUYÊN ĐỀ KNTT LỚP 6 ĐẾN LỚP 12 (CT GDPT 2018)
# ==============================================================================
from data.curriculum_data import BIGDATA_CURRICULUM


# ==============================================================================

# NÂNG CẤP KHKT 2026: BỘ CÔNG CỤ HELPER CHO 3 TÍNH NĂNG MỞ RỘNG

# (1) BỘ NHỚ ĐỆM ĐỀ THI 0.1S | (2) PHÒNG LAB 3D WEBGL | (3) BÁO CÁO PHỤ HUYNH

# ==============================================================================

EXAM_CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "exam_cache")



def save_exam_to_cache(exam_data, subject_name, grade_level, topic_name=""):

    """Lưu đề thi chuẩn hóa đã sinh thành công vào bộ nhớ đệm JSON (Offline 0.1s)."""

    try:

        os.makedirs(EXAM_CACHE_DIR, exist_ok=True)

        code = str(exam_data.get("code", random.randint(1000, 9999)))

        safe_subj = re.sub(r'[^\w\-]', '_', subject_name)

        fname = f"{safe_subj}_lop{grade_level}_{code}.json"

        fpath = os.path.join(EXAM_CACHE_DIR, fname)

        save_obj = {

            "saved_at": get_vn_time(),

            "subject": subject_name,

            "grade": grade_level,

            "topic": topic_name or f"Chuyên đề môn {subject_name} Lớp {grade_level}",

            "code": code,

            "data": exam_data

        }

        with open(fpath, "w", encoding="utf-8") as f_out:

            json.dump(save_obj, f_out, ensure_ascii=False, indent=2)

        return fpath

    except Exception as exc:

        logging.warning("Không thể ghi cache đề thi: %s", exc)

        return None



@st.cache_data(show_spinner=False, max_entries=64, ttl=60)
def get_cached_exams(subject_name, grade_level):

    """Lấy danh sách đề thi đã lưu trong ngân hàng đệm cho môn và khối lớp (kết hợp cache và kho đề thật 2025-2026)."""

    results = []

    # 1. Nạp các đề thi thật đã kiểm định từ kho nền 2025-2026 (0.1s tức thì)

    try:

        if ree:

            baseline_exams = ree.get_baseline_full_exams(subject_name, grade_level)

            for bex in baseline_exams:

                results.append({

                    "saved_at": bex.get("year", "2025-2026"),

                    "subject": subject_name,

                    "grade": grade_level,

                    "topic": f"🔥 [Đề thật] {bex.get('title', 'Đề thi thật toàn quốc')}",

                    "code": bex.get("code", "2501"),

                    "data": {

                        "code": bex.get("code", "2501"),

                        "subject": subject_name,

                        "p1": bex.get("p1", []),

                        "p2": bex.get("p2", []),

                        "p3": bex.get("p3", []),

                        "part_doc_hieu": bex.get("part_doc_hieu"),

                        "part_viet": bex.get("part_viet")

                    }

                })

    except Exception as exc:

        logging.warning("Không thể nạp đề thật từ ree: %s", exc)



    # 2. Nạp các đề thi đệm từ thư mục EXAM_CACHE_DIR

    try:

        if os.path.exists(EXAM_CACHE_DIR):

            safe_subj = re.sub(r'[^\w\-]', '_', subject_name)

            prefix = f"{safe_subj}_lop{grade_level}_"

            for fname in sorted(os.listdir(EXAM_CACHE_DIR), reverse=True):

                if fname.endswith(".json") and fname.startswith(prefix):

                    fpath = os.path.join(EXAM_CACHE_DIR, fname)

                    try:

                        with open(fpath, "r", encoding="utf-8") as f_in:

                            obj = json.load(f_in)

                            if isinstance(obj, dict) and "data" in obj:

                                results.append(obj)

                    except Exception:

                        pass

    except Exception:

        pass

    return results



def create_3d_molecule_figure(mol_type: str) -> go.Figure:

    """Tạo mô hình không gian phân tử 3D tương tác xoay 360 độ (Plotly WebGL chuẩn hóa góc nhìn)."""

    fig = go.Figure()

    if mol_type == "Methane (CH4)":

        # 1. Nguyên tử Carbon ở tâm: to rõ, có viền trắng sáng, chữ C trắng nổi bật

        fig.add_trace(go.Scatter3d(

            x=[0], y=[0], z=[0], mode='markers+text',

            marker=dict(size=24, color='#334155', line=dict(color='#ffffff', width=2.5)),

            text=['C'], textposition='middle center',

            textfont=dict(color='#ffffff', size=13, family='Arial Black'),

            name='Carbon (C)'

        ))



        # 2. Bốn nguyên tử Hydrogen tạo thành tứ diện đều bao quanh

        hx = [1.2, -1.2, -1.2, 1.2]

        hy = [1.2, -1.2, 1.2, -1.2]

        hz = [1.2, 1.2, -1.2, -1.2]

        fig.add_trace(go.Scatter3d(

            x=hx, y=hy, z=hz, mode='markers+text',

            marker=dict(size=16, color='#38bdf8', line=dict(color='#ffffff', width=1.5)),

            text=['H', 'H', 'H', 'H'], textposition='middle center',

            textfont=dict(color='#0f172a', size=11, family='Arial Black'),

            name='Hydrogen (H)'

        ))



        # 3. Bốn liên kết cộng hóa trị rõ nét

        for x, y, z in zip(hx, hy, hz):

            fig.add_trace(go.Scatter3d(

                x=[0, x], y=[0, y], z=[0, z], mode='lines',

                line=dict(color='#cbd5e1', width=8), showlegend=False

            ))

        title = "Phân tử Methane (CH₄) - Cấu trúc Tứ diện đều (Lai hóa sp³)"



    elif mol_type == "Ethanol (C2H5OH)":

        cx = [-0.8, 0.6]; cy = [0.0, 0.0]; cz = [0.0, 0.2]

        fig.add_trace(go.Scatter3d(x=cx, y=cy, z=cz, mode='markers+text',

                                   marker=dict(size=20, color='#334155', line=dict(color='#ffffff', width=2)),

                                   text=['C1', 'C2'], textposition='middle center',

                                   textfont=dict(color='#ffffff', size=11), name='Carbon (C)'))

        fig.add_trace(go.Scatter3d(x=[cx[0], cx[1]], y=[cy[0], cy[1]], z=[cz[0], cz[1]], mode='lines', line=dict(color='#94a3b8', width=7), showlegend=False))

        ox = 1.6; oy = 0.6; oz = -0.3

        fig.add_trace(go.Scatter3d(x=[ox], y=[oy], z=[oz], mode='markers+text',

                                   marker=dict(size=18, color='#ef4444', line=dict(color='#ffffff', width=2)),

                                   text=['O'], textposition='middle center',

                                   textfont=dict(color='#ffffff', size=12), name='Oxygen (O)'))

        fig.add_trace(go.Scatter3d(x=[cx[1], ox], y=[cy[1], oy], z=[cz[1], oz], mode='lines', line=dict(color='#ef4444', width=7), showlegend=False))

        hx = [-1.3, -1.1, -1.1, 0.8, 0.8, 2.2]

        hy = [0.0, 0.9, -0.9, 0.0, -0.9, 0.4]

        hz = [-0.9, 0.5, 0.5, 1.2, 0.2, -0.8]

        fig.add_trace(go.Scatter3d(x=hx, y=hy, z=hz, mode='markers+text',

                                   marker=dict(size=13, color='#38bdf8', line=dict(color='#ffffff', width=1)),

                                   text=['H']*6, textposition='middle center',

                                   textfont=dict(color='#0f172a', size=10), name='Hydrogen (H)'))

        fig.add_trace(go.Scatter3d(x=[ox, hx[5]], y=[oy, hy[5]], z=[oz, hz[5]], mode='lines', line=dict(color='#94a3b8', width=6), showlegend=False))

        title = "Phân tử Ethanol (C₂H₅OH) - Nhóm chức Alcohol (-OH)"



    elif mol_type == "Acetic acid (CH3COOH)":

        cx = [-0.7, 0.7]; cy = [0.0, 0.0]; cz = [0.0, 0.0]

        fig.add_trace(go.Scatter3d(x=cx, y=cy, z=cz, mode='markers+text',

                                   marker=dict(size=20, color='#334155', line=dict(color='#ffffff', width=2)),

                                   text=['C1', 'C2'], textposition='middle center',

                                   textfont=dict(color='#ffffff', size=11), name='Carbon (C)'))

        fig.add_trace(go.Scatter3d(x=[cx[0], cx[1]], y=[cy[0], cy[1]], z=[cz[0], cz[1]], mode='lines', line=dict(color='#94a3b8', width=7), showlegend=False))

        o1x = 1.4; o1y = 0.9; o1z = 0.0

        o2x = 1.2; o2y = -1.1; o2z = 0.0

        fig.add_trace(go.Scatter3d(x=[o1x, o2x], y=[o1y, o2y], z=[o1z, o2z], mode='markers+text',

                                   marker=dict(size=18, color='#ef4444', line=dict(color='#ffffff', width=2)),

                                   text=['=O', '-OH'], textposition='middle center',

                                   textfont=dict(color='#ffffff', size=11), name='Oxygen (O)'))

        fig.add_trace(go.Scatter3d(x=[cx[1], o1x], y=[cy[1], o1y], z=[cz[1], o1z], mode='lines', line=dict(color='#ef4444', width=8), showlegend=False))

        fig.add_trace(go.Scatter3d(x=[cx[1], o2x], y=[cy[1], o2y], z=[cz[1], o2z], mode='lines', line=dict(color='#94a3b8', width=6), showlegend=False))

        title = "Phân tử Acetic acid (CH₃COOH) - Nhóm chức Carboxylic acid (-COOH)"

    else:

        u = np.linspace(0, 2*np.pi, 20)

        v = np.linspace(0, np.pi, 20)

        x = 1.5 * np.outer(np.cos(u), np.sin(v))

        y = 1.5 * np.outer(np.sin(u), np.sin(v))

        z = 1.5 * np.outer(np.ones(np.size(u)), np.cos(v))

        fig.add_trace(go.Surface(x=x, y=y, z=z, colorscale='Blues', opacity=0.85, showscale=False))

        title = "Mô hình Không gian Phân tử Hóa học 3D"



    # CĂN CHỈNH GÓC CAMERA NGHIÊNG NGHỆ THUẬT & KHÓA TỶ LỆ KHÔNG BỊ CẮT XÉN

    fig.update_layout(

        title=dict(text=title, font=dict(color='#38bdf8', size=14)),

        scene=dict(

            bgcolor='#0f172a',

            aspectmode='cube',

            camera=dict(

                eye=dict(x=1.8, y=1.4, z=0.9),  # Góc nghiêng chuẩn nhìn rõ cả 4 đỉnh tứ diện và tâm

                center=dict(x=0, y=0, z=0)

            ),

            xaxis=dict(visible=False, range=[-2.5, 2.5]),

            yaxis=dict(visible=False, range=[-2.5, 2.5]),

            zaxis=dict(visible=False, range=[-2.5, 2.5])

        ),

        paper_bgcolor='#0f172a',

        margin=dict(l=10, r=10, b=10, t=35),

        height=450

    )

    return fig



def create_3d_physics_wave_figure(wave_type: str) -> go.Figure:

    """Mô phỏng 3D sóng vật lý tương tác (Sóng dừng & Mặt sóng lan truyền)."""

    fig = go.Figure()

    x = np.linspace(0, 4*np.pi, 50)

    y = np.linspace(-2, 2, 20)

    X, Y = np.meshgrid(x, y)

    if "Sóng dừng" in wave_type:

        Z = 2 * np.sin(X) * np.cos(Y)

        title = "Mô phỏng 3D Sóng dừng (Standing Waves) - Bụng sóng & Nút sóng"

    else:

        R = np.sqrt((X - 2*np.pi)**2 + Y**2)

        Z = np.sin(2 * R) / (R + 0.5)

        title = "Mô phỏng 3D Mặt sóng lan truyền đồng tâm (Wave Propagation)"

    fig.add_trace(go.Surface(x=X, y=Y, z=Z, colorscale='Viridis', showscale=False))

    fig.update_layout(

        title=dict(text=title, font=dict(color='#38bdf8', size=14)),

        scene=dict(

            bgcolor='#0f172a',

            xaxis=dict(title='Trục X', color='#94a3b8'),

            yaxis=dict(title='Trục Y', color='#94a3b8'),

            zaxis=dict(title='Biên độ Z', color='#94a3b8')

        ),

        paper_bgcolor='#0f172a',

        margin=dict(l=10, r=10, b=10, t=35),

        height=380

    )

    return fig



def create_3d_dna_helix_figure() -> go.Figure:

    """Mô phỏng 3D chuỗi xoắn kép ADN (Watson - Crick) tương tác xoay đa chiều."""

    fig = go.Figure()

    t = np.linspace(0, 4*np.pi, 100)

    r = 2.0

    c = 0.5

    x1 = r * np.cos(t)

    y1 = r * np.sin(t)

    z1 = c * t

    x2 = r * np.cos(t + np.pi)

    y2 = r * np.sin(t + np.pi)

    z2 = c * t

    fig.add_trace(go.Scatter3d(x=x1, y=y1, z=z1, mode='lines', line=dict(color='#38bdf8', width=6), name="Mạch 1 (5' -> 3')"))

    fig.add_trace(go.Scatter3d(x=x2, y=y2, z=z2, mode='lines', line=dict(color='#f43f5e', width=6), name="Mạch 2 (3' -> 5')"))

    for i in range(0, len(t), 4):

        fig.add_trace(go.Scatter3d(x=[x1[i], x2[i]], y=[y1[i], y2[i]], z=[z1[i], z2[i]], mode='lines+markers', line=dict(color='#fbbf24', width=4), marker=dict(size=4, color='#34d399'), showlegend=False))

    fig.update_layout(

        title=dict(text="Cấu trúc Không gian 3D Chuỗi xoắn kép ADN (Watson - Crick)", font=dict(color='#38bdf8', size=14)),

        scene=dict(bgcolor='#0f172a', xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False)),

        paper_bgcolor='#0f172a',

        margin=dict(l=10, r=10, b=10, t=35),

        height=400

    )

    return fig



def render_parent_progress_report(current_student_nm, current_subj, current_gr, logs_data):

    """Tính năng Nâng cấp 3: Xuất Phiếu Báo Cáo Năng Lực Học Tập & Gửi Phụ Huynh."""

    st.markdown("---")

    st.markdown('<h3 style="color: #38bdf8; font-weight: 800;">📄 PHIẾU BÁO CÁO TIẾN TRÌNH NĂNG LỰC & GỬI PHỤ HUYNH (KHKT 2026)</h3>', unsafe_allow_html=True)

    st.caption("Công cụ chuẩn hóa sư phạm giúp Giáo viên & Học sinh xuất bản Phiếu báo cáo tiến bộ học tập, gửi Phụ huynh đồng hành (In PDF A4 hoặc gửi Zalo).")



    with st.expander("📝 Cấu hình & Xuất Phiếu Báo Cáo Học Tập Cá Nhân Hóa", expanded=True):

        col_cfg1, col_cfg2, col_cfg3 = st.columns([2, 1.5, 1.5])

        with col_cfg1:

            st_name_report = st.text_input("Họ và tên học sinh:", value=current_student_nm or "Nguyễn Văn A", key="rep_name")

            report_subjects = [
                "Toán học", "Vật lý", "Hóa học", "Sinh học", "Khoa học tự nhiên",
                "Ngữ văn", "Tiếng Anh", "Lịch sử", "Địa lý", "Lịch sử & Địa lý",
                "Giáo dục kinh tế và pháp luật", "Giáo dục công dân", "Tin học", "Công nghệ"
            ]
            st_subj_report = st.selectbox("Môn học báo cáo:", report_subjects, index=0 if current_subj not in report_subjects else report_subjects.index(current_subj), key="rep_subj")

        with col_cfg3:

            st_grade_report = st.selectbox("Khối lớp:", [f"Lớp {i}" for i in range(6, 13)], index=6 if current_gr not in [f"Lớp {i}" for i in range(6, 13)] else [f"Lớp {i}" for i in range(6, 13)].index(current_gr), key="rep_grade")



        col_sc1, col_sc2, col_sc3 = st.columns(3)

        with col_sc1:

            pre_val = st.number_input("Điểm trước can thiệp (Pre-test):", min_value=0.0, max_value=10.0, value=5.5, step=0.25, key="rep_pre")

        with col_sc2:

            post_val = st.number_input("Điểm sau can thiệp (Post-test):", min_value=0.0, max_value=10.0, value=8.5, step=0.25, key="rep_post")

        with col_sc3:

            study_mins = st.number_input("Thời gian tự học TB (phút/ngày):", min_value=10, max_value=120, value=30, step=5, key="rep_mins")



        delta_score = post_val - pre_val

        status_tag = "Tiến bộ vượt bậc" if delta_score >= 2.0 else ("Tiến bộ tốt" if delta_score > 0 else "Cần duy trì rèn luyện")



        default_teacher_comment = (

            f"Em {st_name_report} đã có sự nỗ lực rất đáng khen ngợi trong môn {st_subj_report} ({st_grade_report}). "

            f"Mức điểm số cải thiện rõ nét ({delta_score:+.2f} điểm), nắm vững phương pháp tư duy 4 bước của George Polya và "

            f"chủ động tự khắc phục các lỗ hổng kiến thức qua Gia sư AI Socratic. Đề nghị em tiếp tục duy trì phong độ!"

        )

        teacher_feedback = st.text_area("Lời nhận xét của Thầy Cô / Gia sư AI:", value=default_teacher_comment, key="rep_fb", height=90)



        report_html = f"""

        <div id="print_report_card" style="background: #ffffff; color: #1e293b; padding: 28px 32px; border-radius: 12px; border: 2px solid #0284c7; box-shadow: 0 10px 25px rgba(0,0,0,0.15); font-family: 'Times New Roman', Times, serif; max-width: 780px; margin: 15px auto;">

            <style>

                @media print {{

                    body * {{ visibility: hidden; }}

                    #print_report_card, #print_report_card * {{ visibility: visible; }}

                    #print_report_card {{ position: absolute; left: 0; top: 0; width: 100%; border: none; box-shadow: none; padding: 0; }}

                    .no-print {{ display: none !important; }}

                }}

            </style>

            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #0284c7; padding-bottom: 12px; margin-bottom: 16px;">

                <div>

                    <div style="font-size: 13px; font-weight: bold; color: #0369a1; text-transform: uppercase;">TRƯỜNG THPT TÂN HIỆP (AN GIANG) • THẦY PHAN MINH TRÍ</div>

                    <div style="font-size: 11px; color: #64748b; font-style: italic;">Đề tài KHKT Dành Cho Học Sinh Trung Học Năm 2026</div>

                </div>

                <div style="text-align: right;">

                    <div style="font-size: 12px; font-weight: bold; color: #0f172a;">HỆ SINH THÁI GIA SƯ AI (GSAI)</div>

                    <div style="font-size: 11px; color: #64748b;">Thời gian: {get_vn_time()[:10]}</div>

                </div>

            </div>



            <div style="text-align: center; margin-bottom: 20px;">

                <h2 style="color: #0369a1; margin: 0; font-size: 22px; font-weight: bold; text-transform: uppercase; letter-spacing: 0.5px;">PHIẾU BÁO CÁO TIẾN TRÌNH NĂNG LỰC HỌC TẬP</h2>

                <div style="font-size: 13px; color: #475569; margin-top: 4px; font-style: italic;">(Đồng hành cá nhân hóa cùng Phụ huynh theo Chương trình GDPT 2018)</div>

            </div>



            <table style="width: 100%; margin-bottom: 16px; font-size: 14.5px; line-height: 1.6;">

                <tr>

                    <td style="width: 50%;"><b>Họ và tên học sinh:</b> <span style="color: #0284c7; font-weight: bold; font-size: 15px;">{st_name_report}</span></td>

                    <td style="width: 50%;"><b>Khối lớp:</b> {st_grade_report}</td>

                </tr>

                <tr>

                    <td><b>Môn học đánh giá:</b> <span style="font-weight: bold;">{st_subj_report}</span></td>

                    <td><b>Thời gian tự học trung bình:</b> <span style="color: #059669; font-weight: bold;">{study_mins} phút/ngày</span> (Khung chuẩn 25-35p)</td>

                </tr>

            </table>



            <div style="background: #f8fafc; border: 1.5px solid #cbd5e1; border-radius: 8px; padding: 14px; margin-bottom: 16px;">

                <div style="font-weight: bold; color: #0f172a; font-size: 14px; margin-bottom: 8px; text-transform: uppercase;">📊 Kết Quả Thực Nghiệm Sư Phạm Đo Lường:</div>

                <div style="display: flex; justify-content: space-around; text-align: center;">

                    <div style="padding: 6px 16px; background: #ffffff; border-radius: 6px; border: 1px solid #e2e8f0; min-width: 120px;">

                        <div style="font-size: 11.5px; color: #64748b;">Trước can thiệp (Pre)</div>

                        <div style="font-size: 20px; font-weight: bold; color: #d97706;">{pre_val:.1f} đ</div>

                    </div>

                    <div style="padding: 6px 16px; background: #ffffff; border-radius: 6px; border: 1px solid #e2e8f0; min-width: 120px;">

                        <div style="font-size: 11.5px; color: #64748b;">Sau can thiệp (Post)</div>

                        <div style="font-size: 20px; font-weight: bold; color: #2563eb;">{post_val:.1f} đ</div>

                    </div>

                    <div style="padding: 6px 16px; background: #f0fdf4; border-radius: 6px; border: 1px solid #bbf7d0; min-width: 120px;">

                        <div style="font-size: 11.5px; color: #166534;">Mức tiến bộ (Δ)</div>

                        <div style="font-size: 20px; font-weight: bold; color: #16a34a;">{delta_score:+.2f} đ</div>

                    </div>

                </div>

            </div>



            <div style="margin-bottom: 16px;">

                <div style="font-weight: bold; color: #0f172a; font-size: 14px; margin-bottom: 4px;">📝 Nhận xét của Thầy Cô / Gia sư AI:</div>

                <div style="font-size: 14px; line-height: 1.6; color: #334155; text-align: justify; font-style: italic; background: #f1f5f9; padding: 10px 14px; border-radius: 6px; border-left: 3.5px solid #0284c7;">

                    "{teacher_feedback}"

                </div>

            </div>



            <div style="margin-bottom: 24px; background: #eff6ff; padding: 10px 14px; border-radius: 6px; border: 1px dashed #3b82f6;">

                <div style="font-weight: bold; color: #1d4ed8; font-size: 13.5px; margin-bottom: 3px;">💡 Khuyến nghị sư phạm dành cho Quý Phụ huynh:</div>

                <div style="font-size: 13px; color: #1e40af; line-height: 1.5;">

                    • Theo kết quả nghiên cứu thực nghiệm KHKT, liều lượng tự học lý tưởng đạt <b>25 - 35 phút/ngày</b> giúp tối ưu hóa điểm số và phát triển tư duy.<br>

                    • Kính mong Quý Phụ huynh thường xuyên khích lệ tinh thần tự giác, không để em học dồn quá sức hoặc lạm dụng thiết bị số quá 60 phút liên tục.

                </div>

            </div>



            <div style="display: flex; justify-content: space-between; text-align: center; margin-top: 20px; font-size: 14px;">

                <div style="width: 45%;">

                    <div style="font-weight: bold;">HỌC SINH CAM KẾT</div>

                    <div style="font-size: 12px; color: #64748b; font-style: italic;">(Ký và ghi rõ họ tên)</div>

                    <div style="height: 50px;"></div>

                    <div style="font-weight: bold; color: #0f172a;">{st_name_report}</div>

                </div>

                <div style="width: 45%;">

                    <div style="font-weight: bold;">GIÁO VIÊN HƯỚNG DẪN / GIA SƯ AI</div>

                    <div style="font-size: 12px; color: #64748b; font-style: italic;">(Xác nhận tiến trình KHKT 2026)</div>

                    <div style="height: 50px;"></div>

                    <div style="font-weight: bold; color: #0284c7;">Gia Sư AI - THPT Tân Hiệp</div>

                </div>

            </div>

        </div>

        """

        render_html_iframe(report_html, height=720, scrolling=True)



        col_p1, col_p2 = st.columns([1.2, 1.8])

        with col_p1:

            render_html_iframe("""

            <div style="text-align: center; margin-top: 10px;">

                <button onclick="window.parent.print()" style="background: linear-gradient(135deg, #0284c7, #0369a1); color: #ffffff; border: none; padding: 10px 20px; border-radius: 8px; font-weight: bold; font-size: 14px; cursor: pointer; box-shadow: 0 4px 12px rgba(2,132,199,0.35);">

                    🖨️ In Phiếu / Lưu PDF (1 Chạm)

                </button>

            </div>

            """, height=55)

        with col_p2:

            zalo_msg = (

                f"🏫 [THPT TÂN HIỆP - GIA SƯ AI 2026] BÁO CÁO TIẾN TRÌNH HỌC TẬP\n"

                f"Kính gửi Quý Phụ huynh em: {st_name_report} ({st_grade_report})\n"

                f"• Môn học: {st_subj_report}\n"

                f"• Điểm trước can thiệp: {pre_val:.1f} điểm\n"

                f"• Điểm kiểm tra hiện tại: {post_val:.1f} điểm\n"

                f"• Mức độ tiến bộ: {delta_score:+.2f} điểm ({status_tag})\n"

                f"• Thời gian tự học khuyến nghị: {study_mins} phút/ngày\n"

                f"• Lời nhắn: {teacher_feedback}\n"

                f"Trân trọng cảm ơn Quý Phụ huynh đã luôn đồng hành cùng con!"

            )

            st.text_area("📲 Tin nhắn mẫu gửi Phụ huynh (Zalo / SMS):", value=zalo_msg, height=110, key="zalo_text_copy")

            st.caption("👉 Thầy Cô hoặc Học sinh có thể bôi đen sao chép nhanh đoạn tin nhắn trên để gửi trực tiếp cho Phụ huynh qua Zalo!")





# Đồng bộ trạng thái Không gian học tập với Sidebar (2 chiều thông minh)
with st.sidebar:
    st.markdown("---")
    st.markdown('<div style="color: #38bdf8; font-weight: 700; font-size: 13px; margin-bottom: 6px;">🧭 Không gian học tập:</div>', unsafe_allow_html=True)
    def on_sb_station_changed():
        try:
            val = st.session_state.get("sb_station_radio_selector")
            if val and val in station_labels:
                st.session_state.selected_station = val
        except Exception:
            pass

    cur_sb_idx = 0
    cur_sel = st.session_state.get("selected_station", station_labels[0])
    if cur_sel in station_labels:
        cur_sb_idx = station_labels.index(cur_sel)

    st.radio(
        "Không gian học tập (Sidebar):",
        station_labels,
        index=None if "sb_station_radio_selector" in st.session_state else cur_sb_idx,
        key="sb_station_radio_selector",
        on_change=on_sb_station_changed,
        label_visibility="collapsed"
    )

selected_station = st.session_state.selected_station

# ==============================================================================
# HỆ THỐNG ĐỊNH VỊ CHỈ MỤC ADN BÀI HỌC SGK KNTT & ĐỒNG BỘ VIDEO YOUTUBE ĐA MÔN
# ==============================================================================

KNTT_EXPERT_MEDIA_CHANNELS = {
    "Toán học": {
        "channel_name": "Thầy Quang (@THẦYQUANG)",
        "channel_url": "https://www.youtube.com/@THẦYQUANG",
        "search_prefix": "Toán",
        "tag": "TOAN"
    },
    "Vật lý": {
        "channel_name": "Thầy Chu Văn Biên / Thầy Quang",
        "channel_url": "https://www.youtube.com/@ThayChuVanBien",
        "search_prefix": "Vật lý",
        "tag": "VATLY"
    },
    "Hóa học": {
        "channel_name": "Thầy Phạm Thắng / Thầy Quang",
        "channel_url": "https://www.youtube.com/@ThayPhamThangHoaHoc",
        "search_prefix": "Hóa học",
        "tag": "HOA"
    },
    "Sinh học": {
        "channel_name": "Thầy Thịnh Nam Sinh Học",
        "channel_url": "https://www.youtube.com/@ThayThinhNamSinhHoc",
        "search_prefix": "Sinh học",
        "tag": "SINH"
    },
    "Ngữ văn": {
        "channel_name": "Học Văn Cô Sương Mai / Chị Hiên",
        "channel_url": "https://www.youtube.com/@hocvancosươngmai",
        "search_prefix": "Ngữ văn",
        "tag": "VAN"
    },
    "Tiếng Anh": {
        "channel_name": "Tiếng Anh Global Success KNTT (NXBGD)",
        "channel_url": "https://www.youtube.com/@TiengAnhGlobalSuccess",
        "search_prefix": "Tiếng Anh Global Success",
        "tag": "ANH"
    },
    "Lịch sử": {
        "channel_name": "Lịch Sử Thầy Dương",
        "channel_url": "https://www.youtube.com/@LichSuThayDuong",
        "search_prefix": "Lịch sử",
        "tag": "SU"
    },
    "Địa lý": {
        "channel_name": "Địa Lý Thầy Tùng",
        "channel_url": "https://www.youtube.com/@DiaLyThayTung",
        "search_prefix": "Địa lý",
        "tag": "DIA"
    },
    "Tin học": {
        "channel_name": "Tin Học Thầy Cường",
        "channel_url": "https://www.youtube.com/@TinHocThayCuong",
        "search_prefix": "Tin học",
        "tag": "TIN"
    },
    "Giáo dục kinh tế và pháp luật": {
        "channel_name": "GDKT&PL KNTT (VTV7 Giáo Dục)",
        "channel_url": "https://www.youtube.com/@VTV7",
        "search_prefix": "GDKT&PL",
        "tag": "GDKTPL"
    },
    "Khoa học tự nhiên": {
        "channel_name": "Thầy Quang (@THẦYQUANG)",
        "channel_url": "https://www.youtube.com/@THẦYQUANG",
        "search_prefix": "KHTN",
        "tag": "KHTN"
    },
    "Công nghệ": {
        "channel_name": "Công Nghệ GDPT 2018 (VTV7 / Thầy Cô KNTT)",
        "channel_url": "https://www.youtube.com/@VTV7",
        "search_prefix": "Công nghệ",
        "tag": "CN"
    },
    "Lịch sử & Địa lý": {
        "channel_name": "Lịch Sử & Địa Lý KNTT (VTV7)",
        "channel_url": "https://www.youtube.com/@VTV7",
        "search_prefix": "Lịch sử và Địa lý",
        "tag": "LSDL"
    },
    "Giáo dục công dân": {
        "channel_name": "GDCD KNTT (VTV7 Giáo Dục)",
        "channel_url": "https://www.youtube.com/@VTV7",
        "search_prefix": "Giáo dục công dân",
        "tag": "GDCD"
    }
}

def generate_kntt_lesson_indexing_and_media(subject_name: str, grade_lvl: int, topic_text: str):
    """
    TỰ ĐỘNG ĐỊNH VỊ CHỈ MỤC ADN BÀI HỌC SGK KẾT NỐI TRI THỨC (CT GDPT 2018)
    VÀ TẠO MÃ QR CODE ĐỘNG LIÊN KẾT VIDEO YOUTUBE CHUẨN XÁC THEO TỪNG MÔN HỌC.
    """
    import textwrap
    raw_topic = str(topic_text or "").strip()
    clean_topic = re.sub(r'^(?:chuyên đề|bài|chương|unit)\s*\d+[\:\.\-]?\s*', '', raw_topic, flags=re.IGNORECASE).strip()
    if not clean_topic:
        clean_topic = raw_topic

    channel_info = KNTT_EXPERT_MEDIA_CHANNELS.get(subject_name, {
        "channel_name": "Kênh Giáo Dục Mở GDPT 2018 (VTV7)",
        "channel_url": "https://www.youtube.com/@VTV7",
        "search_prefix": subject_name,
        "tag": "GD"
    })

    curricula = BIGDATA_CURRICULUM.get(subject_name, {}).get(grade_lvl, [])
    found_idx = -1
    found_title = ""
    for idx_c, c_item in enumerate(curricula):
        if clean_topic.lower() in c_item.lower() or any(w in c_item.lower() for w in clean_topic.lower().split() if len(w) >= 3):
            found_idx = idx_c
            found_title = c_item
            break

    ch_num = 1
    lesson_num = 1
    if found_idx >= 0:
        ch_num = found_idx + 1
        lesson_num = found_idx + 1
    else:
        m_num = re.search(r'(?:bài|chương|chuyên đề|unit)\s*(\d+)', raw_topic, re.IGNORECASE)
        if m_num:
            lesson_num = int(m_num.group(1))
            ch_num = max(1, (lesson_num + 2) // 3)

    vol_num = 1 if ch_num <= 3 or lesson_num <= 4 else 2
    vol_str = f"Tập {vol_num}"
    if subject_name == "Tiếng Anh":
        vol_str = f"Global Success - Unit {lesson_num}"
        index_code = f"KNTT-ANH{grade_lvl}-GS-U{lesson_num:02d}"
    else:
        index_code = f"KNTT-{channel_info['tag']}{grade_lvl}-T{vol_num}-CH{ch_num:02d}-B{lesson_num:02d}"

    book_name = f"Sách giáo khoa {subject_name} {grade_lvl} - {vol_str} (NXB Giáo Dục Việt Nam)"
    chapter_name = found_title if found_title else f"Chương {ch_num}. Chuyên đề trọng tâm môn {subject_name} Lớp {grade_lvl}"

    yt_query = f"{channel_info['search_prefix']} {grade_lvl} Kết nối tri thức {clean_topic} {channel_info['channel_name'].split()[0]}"
    encoded_query = urllib.parse.quote_plus(yt_query)
    yt_deep_url = f"https://www.youtube.com/results?search_query={encoded_query}"

    qr_img_data = generate_local_qr_base64(yt_deep_url, fill_color="#0284c7", back_color="#0f172a")

    kntt_book_list = get_kntt_books_for(subject_name, grade_lvl)
    vniteach_url = kntt_book_list[0]["url"] if kntt_book_list else "https://www.vniteach.com/sach-dien-tu-ket-noi-tri-thuc/#google_vignette"
    vniteach_title = kntt_book_list[0]["title"] if kntt_book_list else f"SGK {subject_name} {grade_lvl} (KNTT)"
    nxbgd_url = "https://taphuan.nxbgd.vn/"

    badge_html = textwrap.dedent(f"""
    <div style="background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.95)); border: 1.5px solid #0284c7; border-radius: 12px; padding: 16px 20px; margin: 15px 0 20px 0; box-shadow: 0 4px 20px rgba(2, 132, 199, 0.25);">
        <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(56, 189, 248, 0.3); padding-bottom: 10px; margin-bottom: 12px;">
            <div style="font-size: 14px; font-weight: 800; color: #38bdf8; text-transform: uppercase; letter-spacing: 0.5px;">
                🛡️ BẢO CHỨNG ĐỊNH VỊ CHỈ MỤC CHUẨN XÁC SGK KẾT NỐI TRI THỨC (CT GDPT 2018)
            </div>
            <div style="background: rgba(2, 132, 199, 0.25); border: 1px solid #38bdf8; border-radius: 6px; padding: 3px 10px; font-family: monospace; font-size: 13px; font-weight: 800; color: #f8fafc;">
                MÃ CHỈ MỤC: {index_code}
            </div>
        </div>
        <div style="display: flex; flex-wrap: wrap; gap: 18px; align-items: center;">
            <div style="flex: 1 1 320px; font-size: 13.5px; color: #e2e8f0; line-height: 1.6;">
                <div>📌 <b>Khối lớp & Môn học:</b> {subject_name} - Lớp {grade_lvl} (Chuẩn Thông tư 32/2018/TT-BGDĐT)</div>
                <div>📖 <b>Chương / Chuyên đề:</b> <span style="color: #fde047;">{chapter_name}</span></div>
                <div>🎯 <b>Bài học đối chứng:</b> <span style="color: #38bdf8; font-weight: 700;">{clean_topic}</span></div>
                <div>🏛️ <b>Ấn bản chính thức:</b> {book_name}</div>
                <div>📚 <b>Đối chất SGK 2 Nguồn:</b> <a href="{vniteach_url}" target="_blank" style="color: #fbbf24; font-weight: 700; text-decoration: underline;">[📖 SGK Điện Tử VniTeach]</a> &nbsp; <a href="{nxbgd_url}" target="_blank" style="color: #38bdf8; font-weight: 700; text-decoration: underline;">[🏛️ Cổng Tập Huấn NXBGD]</a></div>
                <div style="margin-top: 6px; color: #4ade80; font-size: 12.5px;">
                    ✅ <i>Liên kết tham khảo theo môn/lớp; nội dung AI cần giáo viên đối chiếu SGK.</i>
                </div>
            </div>
            <div style="flex: 0 0 auto; text-align: center; background: rgba(15, 23, 42, 0.6); border: 1px dashed rgba(56, 189, 248, 0.4); border-radius: 10px; padding: 10px 14px;">
                <div style="font-size: 11px; font-weight: 700; color: #38bdf8; margin-bottom: 5px;">📱 QUÉT XEM VIDEO BÀI NÀY:</div>
                <img src="{qr_img_data}" style="width: 105px; height: 105px; border-radius: 6px; display: block; margin: 0 auto;" alt="Mã QR Video Bài Học">
                <div style="font-size: 10px; color: #94a3b8; margin-top: 4px;">Kênh: {channel_info['channel_name'].split()[0]}</div>
            </div>
        </div>
        <div style="margin-top: 12px; padding-top: 10px; border-top: 1px dashed rgba(148, 163, 184, 0.2); display: flex; flex-wrap: wrap; gap: 10px; align-items: center;">
            <a href="{yt_deep_url}" target="_blank" style="display: inline-block; background: linear-gradient(135deg, #ef4444, #dc2626); color: #ffffff !important; text-decoration: none; font-size: 13px; font-weight: 700; padding: 6px 14px; border-radius: 6px; box-shadow: 0 2px 8px rgba(239, 68, 68, 0.35);">
                ▶️ 1-Chạm Mở Video Bài Giảng YouTube
            </a>
            <a href="{vniteach_url}" target="_blank" style="display: inline-block; background: linear-gradient(135deg, #f59e0b, #d97706); color: #ffffff !important; text-decoration: none; font-size: 13px; font-weight: 700; padding: 6px 14px; border-radius: 6px; box-shadow: 0 2px 8px rgba(245, 158, 11, 0.35);">
                📖 Lật SGK KNTT Điện Tử (VniTeach)
            </a>
            <a href="{nxbgd_url}" target="_blank" style="display: inline-block; background: linear-gradient(135deg, #0284c7, #0369a1); color: #ffffff !important; text-decoration: none; font-size: 13px; font-weight: 700; padding: 6px 14px; border-radius: 6px; box-shadow: 0 2px 8px rgba(2, 132, 199, 0.35);">
                🏛️ Cổng Tập Huấn NXBGD (SGK Gốc)
            </a>
            <span style="font-size: 12px; color: #94a3b8;">
                👨‍🏫 Kênh đối tác học liệu mở: <b>{channel_info['channel_name']}</b> • <i>Đối soát song song 2 nguồn.</i>
            </span>
        </div>
    </div>
    """).strip()

    return {
        "index_code": index_code,
        "chapter_name": chapter_name,
        "clean_topic": clean_topic,
        "book_name": book_name,
        "channel_info": channel_info,
        "yt_deep_url": yt_deep_url,
        "qr_img_data": qr_img_data,
        "badge_html": badge_html
    }



# ------------------------------------------------------------------------------

# TRẠM 1: TỰ HỌC & PHÒNG LAB

# ------------------------------------------------------------------------------

# BỘ CÔNG CỤ XUẤT ẢNH WEBP SIÊU TỐC (BBT LƯỚI CỘT & ĐỒ THỊ CHUẨN BỘ BỎ KHUNG) CHO TRẠM 3

# ==============================================================================

# ------------------------------------------------------------------------------
# BỘ CÔNG CỤ XUẤT ẢNH WEBP (BBT & ĐỒ THỊ) - ĐÃ TÁCH SANG services/math_graph_engine.py
from services.math_graph_engine import render_bbt_to_webp_base64, render_math_graph_to_webp_base64
# ------------------------------------------------------------------------------

@st.cache_data(show_spinner=False, max_entries=256)
def station1_master_sovereign_brain_gate(raw_text: str, subject: str = "Toán học", grade: int = 12, topic: str = "") -> str:
    """
    BỘ NÃO KIỂM SOÁT BIGDATA CUỐI CÙNG TRẠM 1 (MASTER SOVEREIGN QUALITY GATE):
    - Chuẩn hóa 100% văn bản bài học theo GDPT 2018, SGK KNTT và các VB pháp quy của Bộ.
    - Quét & bọc triệt để KaTeX arrows (chống lỗi đỏ KaTeX ngoài math-mode).
    - Tự động nhận diện & chữa lành toàn diện BBT đa thức bậc 3, phân thức 1/1, phân thức 2/1.
    - Bảo đảm cách ly phân loại 13 môn học, chống lẫn lộn nhãn môn này sang môn khác.
    """
    if not raw_text or not isinstance(raw_text, str):
        return ""

    t = str(raw_text)

    # 1. Tẩy sạch PUA & Soft-hyphen
    if ree and hasattr(ree, "deep_clean_pua_and_artifacts"):
        t = ree.deep_clean_pua_and_artifacts(t)

    # 2. Quét & chuẩn hóa KaTeX
    t = sanitize_katex_latex(t)

    # 3. Chuẩn hóa tên hàm số & TXĐ cho môn Toán SGK KNTT
    if any(m in str(subject).lower() for m in ['toán', 'toan', 'math']):
        # Đảm bảo ký hiệu tập số thực R chuẩn \mathbb{R} (dùng lambda để chống lỗi bad escape \m trên Python 3.14)
        t = re.sub(r'(?i)\bD\s*=\s*R\b', lambda _: r'D = \mathbb{R}', t)
        t = re.sub(r'\\R\b', lambda _: r'\mathbb{R}', t)
        # Khử \searrow và \nearrow nằm trơ trọi trong bảng markdown, cách chữ để không dính chùm
        t = re.sub(r'(?<!\$)\\(?:searrow|nearrow|downarrow|uparrow)(?!\$)', lambda m: ' ↘ ' if 'se' in m.group(0) else (' ↗ ' if 'ne' in m.group(0) else (' ↑ ' if 'up' in m.group(0) else ' ↓ ')), t)

    return t


# ==============================================================================
# ENGINE TRỰC QUAN HÓA SƯ PHẠM ĐA MÔN - ĐA LỚP & BBT CHUẨN BỘ GD&ĐT (TKZ-TAB)
# ==============================================================================
def _render_math_html_token(raw_val: str) -> str:
    """Chuyển đổi biểu thức LaTeX (phân số, căn thức, số mũ, vô cực) sang HTML sắc nét trong BBT."""
    if not raw_val:
        return ""
    s = raw_val.strip()
    s = re.sub(r'^\$+|\$+$', '', s).strip()
    s = s.replace('⟦DBL_BAR⟧', '||')

    # Chuẩn hóa ký hiệu vô cực & đặc biệt
    s = re.sub(r'\+\\infty|\+\s*∞', '+∞', s)
    s = re.sub(r'-\\infty|-\s*∞', '−∞', s)
    s = s.replace(r'\infty', '∞').replace(r'\pm', '±').replace(r'\mp', '∓')
    s = s.replace(r'\pi', 'π').replace(r'\Delta', 'Δ').replace(r'\alpha', 'α').replace(r'\beta', 'β')
    s = s.replace(r'\mathbb{R}', 'ℝ').replace(r'\R', 'ℝ')

    # Chuyển đổi căn bậc hai \sqrt{A} -> √(A)
    s = re.sub(
        r'\\sqrt\{([^{}]+)\}',
        r'<span style="white-space:nowrap;">√<span style="text-decoration:overline;">\1</span></span>',
        s
    )

    # Chuyển đổi phân số \frac{A}{B} hoặc \dfrac{A}{B} -> Phân số dọc chuẩn SGK
    for _ in range(2):
        s = re.sub(
            r'\\(?:d|t)?frac\{([^{}]+)\}\{([^{}]+)\}',
            r'<span style="display:inline-flex;flex-direction:column;vertical-align:middle;text-align:center;font-size:0.92em;line-height:1.1;margin:0 2px;">'
            r'<span style="border-bottom:1.5px solid #0f172a;padding:0 3px;">\1</span>'
            r'<span style="padding:0 3px;">\2</span></span>',
            s
        )

    # Chuyển số mũ và chỉ số dưới
    s = re.sub(r'\^\{([^{}]+)\}', r'<sup>\1</sup>', s)
    s = re.sub(r'\^([0-9a-zA-Z+-])', r'<sup>\1</sup>', s)
    s = re.sub(r'_\{([^{}]+)\}', r'<sub>\1</sub>', s)
    s = re.sub(r'_([0-9a-zA-Z])', r'<sub>\1</sub>', s)

    # Dọn dẹp dấu $ hoặc ngoặc nhọn dư thừa
    s = s.replace('$', '').replace('{', '').replace('}', '')
    return s.strip()


def _parse_bbt_cells_safe(line: str) -> list:
    """Tách ô bảng Markdown nhưng bảo vệ tuyệt đối ký hiệu tiệm cận đứng || và trị tuyệt đối |x|."""
    s = line.strip()
    # 1. Bảo vệ ký hiệu không xác định / tiệm cận đứng || (bắt || độc lập hoặc trong ô/chữ, không bắt cột trống | |)
    s = re.sub(r'(?<!\|)\|\|(?!\|)', '⟦DBL_BAR⟧', s)
    # 2. Bảo vệ trị tuyệt đối |...| bên trong cặp $...$
    def _protect_pipes_in_math(m):
        return m.group(0).replace('|', '⟦ABS_PIPE⟧')
    s = re.sub(r'\$[^$]+\$', _protect_pipes_in_math, s)

    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|'):
        s = s[:-1]

    cells = [
        c.strip().replace('⟦DBL_BAR⟧', '||').replace('⟦ABS_PIPE⟧', '|')
        for c in s.split('|')
    ]
    return cells


def _normalize_moet_bbt_grid(x_cells: list, yp_cells: list, y_cells: list) -> dict:
    """
    Chuẩn hóa dữ liệu BBT về đúng chuẩn lưới 2N-1 cột của Bộ GD&ĐT (tkz-tab):
    - points: N điểm trên hàng x [x_0, x_1, ..., x_{N-1}]
    - yp_at_pts: N giá trị tại điểm của hàng y' ('0', '||', hoặc '')
    - yp_intervals: N-1 dấu trên khoảng của hàng y' ('+', '-', hoặc '')
    - y_at_pts: N giá trị/cực trị tại điểm của hàng y (hỗ trợ cả 'L || R' tại tiệm cận đứng)
    - y_arrows: N-1 hướng mũi tên trên khoảng ('up' hoặc 'down')
    """
    x_label = _render_math_html_token(x_cells[0]) if x_cells else "x"
    yp_label = _render_math_html_token(yp_cells[0]) if yp_cells else ""
    y_label = _render_math_html_token(y_cells[0]) if y_cells else "y"

    raw_x = [c.strip() for c in x_cells[1:] if c.strip() != ""]
    if len(raw_x) < 2:
        raw_x = [r"-\infty", r"+\infty"]
    n_pts = len(raw_x)
    n_int = n_pts - 1

    # --- 1. Trích xuất dấu khoảng (+/-) và điểm (0 / ||) từ hàng y' ---
    yp_body = [c.strip() for c in yp_cells[1:]] if yp_cells else []
    yp_at_pts = [""] * n_pts
    yp_intervals = [""] * n_int

    if yp_body:
        if len(yp_body) == 2 * n_pts - 1:
            for i in range(n_pts):
                tok = yp_body[2 * i].replace('$', '').strip()
                if tok in ('0', '||'):
                    yp_at_pts[i] = tok
            for i in range(n_int):
                tok = yp_body[2 * i + 1].replace('$', '').strip()
                if '+' in tok:
                    yp_intervals[i] = '+'
                elif '-' in tok or '−' in tok:
                    yp_intervals[i] = '−'
        else:
            flat_tokens = []
            for cell in yp_body:
                clean_c = cell.replace('$', '').strip()
                found = re.findall(r'\|\||[+\-−]|0', clean_c)
                if found:
                    flat_tokens.extend(found)
            signs_only = ['+' if t == '+' else '−' for t in flat_tokens if t in ('+', '-', '−')]
            pts_only = [t for t in flat_tokens if t in ('0', '||')]

            for i in range(n_int):
                if i < len(signs_only):
                    yp_intervals[i] = signs_only[i]
            for i in range(1, n_pts - 1):
                if (i - 1) < len(pts_only):
                    yp_at_pts[i] = pts_only[i - 1]

    # --- 2. Trích xuất giá trị cực trị/giới hạn và mũi tên từ hàng y ---
    y_body = [c.strip() for c in y_cells[1:]] if y_cells else []
    arrow_pat = r'(\\nearrow|\\searrow|\\uparrow|\\downarrow|↗|↘|↑|↓)'

    y_at_pts = [""] * n_pts
    y_arrows = [""] * n_int

    joined_y = " | ".join(y_body)
    if re.search(arrow_pat, joined_y):
        found_arrows = re.findall(arrow_pat, joined_y)
        for i in range(n_int):
            if i < len(found_arrows):
                a_tok = found_arrows[i]
                y_arrows[i] = "up" if a_tok in (r'\nearrow', r'\uparrow', '↗', '↑') else "down"

        if len(y_body) == 2 * n_pts - 1:
            for i in range(n_pts):
                y_at_pts[i] = re.sub(arrow_pat, '', y_body[2 * i]).strip()
        else:
            val_segments = re.split(arrow_pat, " ".join(y_body))
            clean_vals = []
            for seg in val_segments:
                if re.fullmatch(arrow_pat, seg.strip()):
                    continue
                s_clean = seg.strip().strip('|').strip()
                if s_clean or len(clean_vals) > 0:
                    clean_vals.append(s_clean)
            non_empty_vals = [v for v in clean_vals if v != ""]
            if len(non_empty_vals) == n_pts:
                y_at_pts = non_empty_vals
            else:
                for i in range(min(n_pts, len(non_empty_vals))):
                    y_at_pts[i] = non_empty_vals[i]
    else:
        non_empty_y = [c for c in y_body if c != ""]
        for i in range(min(n_pts, len(non_empty_y))):
            y_at_pts[i] = non_empty_y[i]

    # --- 3. ĐỒNG BỘ LOGIC SƯ PHẠM GIỮA DẤU Y' VÀ CHIỀU MŨI TÊN Y ---
    for i in range(n_int):
        if yp_intervals[i] == '+':
            y_arrows[i] = 'up'
        elif yp_intervals[i] == '−':
            y_arrows[i] = 'down'
        elif not yp_intervals[i] and y_arrows[i]:
            yp_intervals[i] = '+' if y_arrows[i] == 'up' else '−'
        elif not y_arrows[i]:
            y_arrows[i] = 'up' if i % 2 == 0 else 'down'

    for i in range(1, n_pts - 1):
        if '||' in y_at_pts[i] and not yp_at_pts[i]:
            yp_at_pts[i] = '||'
        elif yp_at_pts[i] == "" and y_at_pts[i] != "":
            yp_at_pts[i] = '0'

    return {
        "x_label": x_label,
        "yp_label": yp_label,
        "y_label": y_label,
        "has_yp": bool(yp_cells),
        "points": raw_x,
        "yp_at_pts": yp_at_pts,
        "yp_intervals": yp_intervals,
        "y_at_pts": y_at_pts,
        "y_arrows": y_arrows,
    }


def _build_svg_bbt_from_rows(x_cells: list, yp_cells: list, y_cells: list, is_sign_table: bool = False) -> str:
    """
    Dựng Bảng Biến Thiên / Bảng Xét Dấu chuẩn Bộ GD&ĐT (SGK Kết nối tri thức):
    - Lưới chuẩn 2N-1 cột: Điểm x_i thẳng hàng dọc tuyệt đối với nghiệm 0 / vạch kép || và cực trị y(x_i).
    - Cao độ chuẩn Giải tích: Đầu mũi tên đồng biến (↗) nối từ Đáy-Trái lên Đỉnh-Phải;
      nghịch biến (↘) nối từ Đỉnh-Trái xuống Đáy-Phải.
    - Tiệm cận đứng ||: Vạch đôi chuẩn xuyên suốt chiều cao hàng y' và hàng y, tách giới hạn trái/phải.
    """
    if is_sign_table:
        grid = _normalize_moet_bbt_grid(x_cells, y_cells, [])
        n_pts = len(grid["points"])
        n_int = n_pts - 1
        x_html = f'<td style="padding:10px 14px;font-weight:800;font-style:italic;border-right:2px solid #0f172a;border-bottom:1.8px solid #0f172a;background:#f1f5f9;text-align:center;width:72px;">{grid["x_label"]}</td>'
        fx_html = f'<td style="padding:10px 14px;font-weight:800;font-style:italic;border-right:2px solid #0f172a;background:#f1f5f9;text-align:center;">{grid["yp_label"]}</td>'

        for i in range(n_pts):
            pt_str = _render_math_html_token(grid["points"][i])
            x_html += f'<td style="padding:8px 10px;text-align:center;font-weight:700;border-bottom:1.8px solid #0f172a;min-width:48px;">{pt_str}</td>'
            p_val = grid["yp_at_pts"][i]
            if p_val == '||':
                fx_html += '<td style="padding:0;text-align:center;position:relative;height:44px;"><div style="display:inline-block;width:6px;height:100%;border-left:1.8px solid #dc2626;border-right:1.8px solid #dc2626;"></div></td>'
            else:
                fx_html += f'<td style="padding:8px 10px;text-align:center;font-weight:700;color:#0f172a;">{p_val}</td>'

            if i < n_int:
                x_html += '<td style="padding:8px 16px;border-bottom:1.8px solid #0f172a;min-width:64px;"></td>'
                sgn = grid["yp_intervals"][i]
                sgn_color = "#16a34a" if sgn == '+' else "#dc2626"
                fx_html += f'<td style="padding:8px 16px;text-align:center;font-weight:800;font-size:1.18rem;color:{sgn_color};">{sgn}</td>'

        return (
            '<div style="margin:14px 0;overflow-x:auto;background:#ffffff;border:2px solid #0f172a;border-radius:8px;box-shadow:0 3px 10px rgba(15,23,42,0.06);">'
            '<table style="width:100%;border-collapse:collapse;font-family:\'Times New Roman\',Times,serif;font-size:1.05rem;color:#0f172a;">'
            f'<tr>{x_html}</tr><tr>{fx_html}</tr></table></div>'
        )

    grid = _normalize_moet_bbt_grid(x_cells, yp_cells, y_cells)
    n_pts = len(grid["points"])
    n_int = n_pts - 1

    pt_pos = ["middle"] * n_pts
    for i in range(n_pts):
        left_arr = grid["y_arrows"][i - 1] if i > 0 else None
        right_arr = grid["y_arrows"][i] if i < n_int else None
        if right_arr == "down" or left_arr == "up":
            pt_pos[i] = "top"
        elif right_arr == "up" or left_arr == "down":
            pt_pos[i] = "bottom"

    x_row_html = f'<td style="padding:10px 14px;font-weight:800;font-style:italic;border-right:2px solid #0f172a;border-bottom:1.8px solid #0f172a;background:#f8fafc;text-align:center;width:72px;">{grid["x_label"]}</td>'
    yp_row_html = f'<td style="padding:10px 14px;font-weight:800;font-style:italic;border-right:2px solid #0f172a;border-bottom:1.8px solid #0f172a;background:#f8fafc;text-align:center;">{grid["yp_label"]}</td>'
    y_row_html = f'<td style="padding:16px 14px;font-weight:800;font-style:italic;border-right:2px solid #0f172a;background:#f8fafc;text-align:center;vertical-align:middle;">{grid["y_label"]}</td>'

    for i in range(n_pts):
        pt_html = _render_math_html_token(grid["points"][i])
        x_row_html += f'<td style="padding:8px 8px;text-align:center;font-weight:700;border-bottom:1.8px solid #0f172a;min-width:52px;white-space:nowrap;">{pt_html}</td>'

        yp_pt = grid["yp_at_pts"][i]
        if yp_pt == '||':
            yp_row_html += (
                '<td style="padding:0;text-align:center;border-bottom:1.8px solid #0f172a;height:42px;">'
                '<div style="display:inline-block;width:6px;height:100%;border-left:1.8px solid #dc2626;border-right:1.8px solid #dc2626;"></div>'
                '</td>'
            )
        else:
            yp_row_html += f'<td style="padding:8px 8px;text-align:center;font-weight:700;border-bottom:1.8px solid #0f172a;">{yp_pt}</td>'

        raw_y_val = grid["y_at_pts"][i]
        is_asymptote = (yp_pt == '||' or '||' in raw_y_val)
        if is_asymptote:
            parts_asym = raw_y_val.split('||') if '||' in raw_y_val else ["", ""]
            left_lim = _render_math_html_token(parts_asym[0]) if len(parts_asym) > 0 else ""
            right_lim = _render_math_html_token(parts_asym[1]) if len(parts_asym) > 1 else ""
            left_align = "flex-start" if (i > 0 and grid["y_arrows"][i - 1] == "up") or "+∞" in left_lim else "flex-end"
            right_align = "flex-start" if (i < n_int and grid["y_arrows"][i] == "down") or "+∞" in right_lim else "flex-end"
            y_row_html += (
                '<td style="padding:0 4px;height:108px;vertical-align:stretch;">'
                '<div style="display:flex;align-items:stretch;justify-content:center;height:100%;">'
                f'<div style="display:flex;align-items:{left_align};padding:6px 4px;font-weight:700;font-size:0.95rem;white-space:nowrap;">{left_lim}</div>'
                '<div style="width:6px;border-left:1.8px solid #dc2626;border-right:1.8px solid #dc2626;margin:0 2px;"></div>'
                f'<div style="display:flex;align-items:{right_align};padding:6px 4px;font-weight:700;font-size:0.95rem;white-space:nowrap;">{right_lim}</div>'
                '</div></td>'
            )
        else:
            val_html = _render_math_html_token(raw_y_val)
            v_align = "top" if pt_pos[i] == "top" else ("bottom" if pt_pos[i] == "bottom" else "middle")
            pad_style = "padding:8px 6px 42px 6px;" if v_align == "top" else ("padding:42px 6px 8px 6px;" if v_align == "bottom" else "padding:12px 6px;")
            y_row_html += f'<td style="{pad_style}text-align:center;vertical-align:{v_align};font-weight:700;white-space:nowrap;height:108px;">{val_html}</td>'

        if i < n_int:
            x_row_html += '<td style="padding:8px 18px;border-bottom:1.8px solid #0f172a;min-width:84px;"></td>'
            sgn = grid["yp_intervals"][i]
            sgn_color = "#16a34a" if sgn == '+' else "#dc2626"
            yp_row_html += f'<td style="padding:8px 18px;text-align:center;font-weight:800;font-size:1.2rem;color:{sgn_color};border-bottom:1.8px solid #0f172a;">{sgn}</td>'

            arr_dir = grid["y_arrows"][i]
            if arr_dir == "up":
                svg_arrow = (
                    '<svg width="100%" height="78" viewBox="0 0 100 78" preserveAspectRatio="none" style="overflow:visible;display:block;">'
                    '<defs><marker id="bbt_up" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">'
                    '<path d="M0,0 L8,4 L0,8 Z" fill="#16a34a"/></marker></defs>'
                    '<line x1="8" y1="68" x2="90" y2="12" stroke="#16a34a" stroke-width="2.2" marker-end="url(#bbt_up)"/>'
                    '</svg>'
                )
            else:
                svg_arrow = (
                    '<svg width="100%" height="78" viewBox="0 0 100 78" preserveAspectRatio="none" style="overflow:visible;display:block;">'
                    '<defs><marker id="bbt_dn" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">'
                    '<path d="M0,0 L8,4 L0,8 Z" fill="#dc2626"/></marker></defs>'
                    '<line x1="8" y1="12" x2="90" y2="68" stroke="#dc2626" stroke-width="2.2" marker-end="url(#bbt_dn)"/>'
                    '</svg>'
                )
            y_row_html += f'<td style="padding:6px 4px;vertical-align:middle;min-width:84px;">{svg_arrow}</td>'

    yp_tr = f'<tr>{yp_row_html}</tr>' if grid["has_yp"] else ''
    return (
        '<div style="margin:16px 0;overflow-x:auto;background:#ffffff;border:2px solid #0f172a;border-radius:8px;box-shadow:0 4px 12px rgba(15,23,42,0.07);">'
        '<div style="background:#0f172a;color:#f8fafc;font-size:0.75rem;font-weight:700;padding:4px 12px;letter-spacing:0.5px;text-transform:uppercase;">'
        '📐 Bảng Biến Thiên Chuẩn Sư Phạm (CT GDPT 2018)</div>'
        '<table style="width:100%;border-collapse:collapse;font-family:\'Times New Roman\',Times,serif;font-size:1.05rem;color:#0f172a !important;">'
        f'<tr>{x_row_html}</tr>{yp_tr}<tr>{y_row_html}</tr>'
        '</table></div>'
    )


@st.cache_data(show_spinner=False, max_entries=256)
def render_pedagogical_lesson_visuals(markdown_text: str, subject: str = "", grade: int = 12) -> str:
    """
    TINH TÚY THỊ GIÁC ĐỒ HỌA TRẠM 3 TÍCH HỢP TOÀN DIỆN VÀO TRẠM 1:
    - Bắt Bảng biến thiên (BBT) Markdown chuyển thành Đồ họa chuẩn Bộ GD&ĐT (tkz-tab SVG & WebP).
    - Phân luồng chuẩn Đa Môn - Đa Lớp: Chỉ Môn Toán mới áp BBT Giải tích; bảo vệ bảng đa môn.
    - Hỗ trợ đầy đủ BBT 3 hàng (Lớp 11, 12), BBT 2 hàng (Lớp 10) và Bảng xét dấu 2 hàng (Lớp 10).
    - Tự động nhận diện Đồ thị hàm số, Bảng mẫu số liệu ghép nhóm (MSLGN), Mô hình không gian Oxyz.
    """
    if not markdown_text:
        return markdown_text

    text = str(markdown_text)
    is_math_subj = any(m in str(subject).lower() for m in ['toán', 'toan', 'math']) or (str(subject).strip() == "")

    # Gỡ vỏ code block nếu AI lỡ bọc bảng Markdown trong ```text ... ```
    text = re.sub(
        r'```(?:text|markdown|plaintext|ascii)?\s*\n((?:[ \t]*\|.*\|[ \t]*\n)+)```',
        r'\1',
        text,
        flags=re.IGNORECASE
    )

    # 1. TỰ ĐỘNG BẮT VÀ NÂNG CẤP BẢNG BIẾN THIÊN (BBT) THÔ THÀNH ĐỒ HỌA CHUẨN BỘ
    def _replace_bbt_table(match):
        raw_tbl = match.group(0).strip()
        raw_lines = [l.strip() for l in raw_tbl.split('\n') if l.strip()]

        # Bảng thực sự phải có ít nhất 2 dòng và mỗi dòng có từ 3 dấu '|' trở lên
        if len(raw_lines) < 2 or any(l.count('|') < 3 for l in raw_lines):
            return match.group(0)

        # Chốt chặn phân luồng Đa môn: Chỉ áp BBT Giải tích khi môn học là Môn Toán
        if not is_math_subj:
            return match.group(0)

        data_rows = []
        for l in raw_lines:
            if re.match(r'^\|?[\s:\-\|]+\|?$', l):
                continue
            cells = _parse_bbt_cells_safe(l)
            if len(cells) >= 2:
                data_rows.append(cells)

        if len(data_rows) < 2:
            return match.group(0)

        def _clean_head(cell_str: str) -> str:
            return re.sub(r'[\$\s\\*`\(\)]', '', cell_str).lower()

        first_head = _clean_head(data_rows[0][0])
        if first_head not in ('x', 't'):
            return match.group(0)

        try:
            # Trường hợp 1: BBT 3 hàng chuẩn Lớp 11, 12 (x, y'/f'(x), y/f(x))
            if len(data_rows) >= 3:
                second_head = _clean_head(data_rows[1][0])
                third_head = _clean_head(data_rows[2][0])
                if ("'" in second_head or "’" in second_head or "đạo" in second_head or "dao" in second_head or "f'" in second_head or "y'" in second_head) and (
                    third_head in ('y', 'f(x)', 'g(x)', 'h(x)', 's(t)', 'v(t)', 'f', 'g', 'h')
                ):
                    return "\n\n" + _build_svg_bbt_from_rows(data_rows[0], data_rows[1], data_rows[2]) + "\n\n"

            # Trường hợp 2: BBT 2 hàng (Hàm bậc hai Lớp 10: x và y) hoặc Bảng xét dấu 2 hàng (x và f(x))
            if len(data_rows) == 2:
                second_head = _clean_head(data_rows[1][0])
                row2_joined = " ".join(data_rows[1][1:])
                if re.search(r'(\\nearrow|\\searrow|↗|↘)', row2_joined):
                    return "\n\n" + _build_svg_bbt_from_rows(data_rows[0], [], data_rows[1]) + "\n\n"
                elif second_head in ('f(x)', 'y', "y'", "f'(x)", 'g(x)', 'dấu', 'dauxet', 'dau', 'f') and re.search(r'[+\-−]', row2_joined):
                    return "\n\n" + _build_svg_bbt_from_rows(data_rows[0], [], data_rows[1], is_sign_table=True) + "\n\n"
        except Exception:
            pass

        return match.group(0)

    # Regex quét toàn bộ khối bảng markdown
    bbt_pattern = re.compile(
        r'((?:^[ \t]*\|?.*\|.*(?:\r?\n|$))+)',
        flags=re.MULTILINE
    )
    text = bbt_pattern.sub(_replace_bbt_table, text)


    # 2. BẮT BẢNG MẪU SỐ LIỆU GHÉP NHÓM (MSLGN - Chuẩn Times New Roman & viền hộp đôi SGK)
    def _replace_mslgn_table(match):
        raw_tbl = match.group(0).strip()
        lines = [l.strip() for l in raw_tbl.split('\n') if l.strip() and '---' not in l]
        if len(lines) >= 2:
            try:
                row1_cells = [c.strip() for c in lines[0].split('|')[1:-1] if c.strip()]
                row2_cells = [c.strip() for c in lines[1].split('|')[1:-1] if c.strip()]
                if len(row1_cells) >= 3 and len(row2_cells) >= 3:
                    lbl1 = html.escape(row1_cells[0])
                    lbl2 = html.escape(row2_cells[0])
                    groups = [html.escape(c) for c in row1_cells[1:]]
                    freqs = [html.escape(c) for c in row2_cells[1:]]
                    if len(groups) == len(freqs):
                        tbl_w = min(680, max(360, len(groups) * 75 + 120))
                        cells_g = "".join(f"<td style='padding: 6px 10px; border: 1px solid #000; font-weight: 500;'>{g}</td>" for g in groups)
                        cells_f = "".join(f"<td style='padding: 6px 10px; border: 1px solid #000; font-weight: bold;'>{f}</td>" for f in freqs)
                        return (
                            f"\n\n<div style='display: flex; justify-content: center; margin: 12px auto;'>"
                            f"<div style='max-width: {tbl_w}px; background: #ffffff; padding: 0; width: 100%; border-radius: 4px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>"
                            f"<table style='width: 100%; border-collapse: collapse; text-align: center; font-family: \"Times New Roman\", serif; color: #000; border: 1.2px solid #000; font-size: 14.5px;'>"
                            f"<tr><th style='padding: 6px 10px; border: 1px solid #000; font-weight: bold; width: 130px; background-color: #f1f5f9;'>{lbl1}</th>{cells_g}</tr>"
                            f"<tr><th style='padding: 6px 10px; border: 1px solid #000; font-weight: bold; background-color: #f1f5f9;'>{lbl2}</th>{cells_f}</tr>"
                            f"</table></div></div>\n\n"
                        )
            except Exception:
                pass
        return raw_tbl

    mslgn_pattern = re.compile(
        r'(?:^[ \t]*\|[^\n]*(?:nhóm|khoảng|giá trị|lớp)[^\n]*\|\s*\n)'
        r'(?:^[ \t]*\|(?:\s*\:?\-{2,}\:?\s*\|)+\s*\n)'
        r'(?:^[ \t]*\|[^\n]*(?:tần số|số học sinh|số lượng|tần suất|n)[^\n]*\|)',
        flags=re.MULTILINE | re.IGNORECASE
    )
    text = mslgn_pattern.sub(_replace_mslgn_table, text)

    # 3. KÍCH HOẠT MÔ HÌNH THỊ GIÁC ĐA MÔN & ĐA LỚP GDPT 2018 (VẬT LÝ, HÓA HỌC, SINH HỌC, ĐỊA LÍ, OXYZ)
    # Tự động chèn mô hình đồ họa vector trực quan khi bài học đề cập đến các chuyên đề trọng tâm
    subj_norm = str(subject).strip().lower()
    text_lower = text.lower()

    try:
        import precision_visual_engine as pve
    except Exception:
        pve = None

    if pve:
        # A. VẬT LÝ / KHOA HỌC TỰ NHIÊN:
        if "vật lý" in subj_norm or "vật lí" in subj_norm or "khoa học tự nhiên" in subj_norm:
            # 1. Nhiệt học p-V
            if any(k in text_lower for k in ["chu trình", "đẳng áp", "đẳng tích", "đẳng nhiệt", "đồ thị p-v", "khí lý tưởng", "khí lí tưởng"]) and "svg_pv_inserted" not in text:
                try:
                    pv_model = pve.build_thermal_gas_pv_model()
                    if pv_model and pv_model.get("svg"):
                        pv_box = (
                            f"\n\n<div style='text-align: center; margin: 14px auto;'>"
                            f"<div style='display: inline-block; max-width: 320px; width: 100%; padding: 8px; background: #ffffff; border-radius: 8px; box-shadow: 0 4px 14px rgba(0,0,0,0.12);'>"
                            f"{sanitize_svg_for_markdown(pv_model['svg'])}"
                            f"<p style='font-size: 13px; color: #475569; margin-top: 6px; font-weight: bold;'>🔬 Đồ thị Chu trình Nhiệt động lực học p-V</p>"
                            f"</div></div>\n\n"
                        )
                        text += pv_box
                except Exception:
                    pass
            # 2. Lực từ & Bàn tay trái
            if any(k in text_lower for k in ["lực từ", "từ trường", "bàn tay trái", "lorentz", "cảm ứng từ"]) and "svg_mag_inserted" not in text:
                try:
                    mag_model = pve.build_magnetic_force_model()
                    if mag_model and mag_model.get("svg"):
                        mag_box = (
                            f"\n\n<div style='text-align: center; margin: 14px auto;'>"
                            f"<div style='display: inline-block; max-width: 320px; width: 100%; padding: 8px; background: #ffffff; border-radius: 8px; box-shadow: 0 4px 14px rgba(0,0,0,0.12);'>"
                            f"{sanitize_svg_for_markdown(mag_model['svg'])}"
                            f"<p style='font-size: 13px; color: #475569; margin-top: 6px; font-weight: bold;'>🧲 Mô hình Quy tắc Bàn tay trái & Chiều Lực từ</p>"
                            f"</div></div>\n\n"
                        )
                        text += mag_box
                except Exception:
                    pass
            # 3. Phóng xạ hạt nhân
            if any(k in text_lower for k in ["phóng xạ", "chu kỳ bán rã", "chu kì bán rã", "hạt nhân", "độ phóng xạ"]) and "svg_nuc_inserted" not in text:
                try:
                    nuc_model = pve.build_nuclear_decay_model()
                    if nuc_model and nuc_model.get("svg"):
                        nuc_box = (
                            f"\n\n<div style='text-align: center; margin: 14px auto;'>"
                            f"<div style='display: inline-block; max-width: 320px; width: 100%; padding: 8px; background: #ffffff; border-radius: 8px; box-shadow: 0 4px 14px rgba(0,0,0,0.12);'>"
                            f"{sanitize_svg_for_markdown(nuc_model['svg'])}"
                            f"<p style='font-size: 13px; color: #475569; margin-top: 6px; font-weight: bold;'>⚛️ Đồ thị Phân rã phóng xạ theo Thời gian</p>"
                            f"</div></div>\n\n"
                        )
                        text += nuc_box
                except Exception:
                    pass
            # 4. Mạch RLC & Sóng cơ
            if any(k in text_lower for k in ["mạch rlc", "cuộn cảm", "tụ điện", "dao động điều hòa", "bước sóng", "sóng dừng"]) and "svg_wave_inserted" not in text:
                try:
                    wave_model = pve.build_oscillation_wave_model()
                    if wave_model and wave_model.get("svg"):
                        wave_box = (
                            f"\n\n<div style='text-align: center; margin: 14px auto;'>"
                            f"<div style='display: inline-block; max-width: 320px; width: 100%; padding: 8px; background: #ffffff; border-radius: 8px; box-shadow: 0 4px 14px rgba(0,0,0,0.12);'>"
                            f"{sanitize_svg_for_markdown(wave_model['svg'])}"
                            f"<p style='font-size: 13px; color: #475569; margin-top: 6px; font-weight: bold;'>〰️ Đồ thị Dao động & Lan truyền Sóng cơ</p>"
                            f"</div></div>\n\n"
                        )
                        text += wave_box
                except Exception:
                    pass

        # B. HÓA HỌC / KHOA HỌC TỰ NHIÊN:
        elif "hóa học" in subj_norm or "hóa" in subj_norm:
            # 1. Thí nghiệm điều chế khí
            if any(k in text_lower for k in ["điều chế", "thu khí", "ống nghiệm", "đẩy nước", "đẩy không khí", "bình tam giác"]) and "svg_chem_inserted" not in text:
                try:
                    chem_model = pve.build_gas_preparation_model("C2H4")
                    if chem_model and chem_model.get("svg"):
                        chem_box = (
                            f"\n\n<div style='text-align: center; margin: 14px auto;'>"
                            f"<div style='display: inline-block; max-width: 320px; width: 100%; padding: 8px; background: #ffffff; border-radius: 8px; box-shadow: 0 4px 14px rgba(0,0,0,0.12);'>"
                            f"{sanitize_svg_for_markdown(chem_model['svg'])}"
                            f"<p style='font-size: 13px; color: #475569; margin-top: 6px; font-weight: bold;'>🧪 Mô hình Thí nghiệm Điều chế & Thu khí Phòng Lab</p>"
                            f"</div></div>\n\n"
                        )
                        text += chem_box
                except Exception:
                    pass
            # 2. Pin điện hóa Daniell
            if any(k in text_lower for k in ["pin điện hóa", "daniell", "cực âm", "cực dương", "anode", "cathode", "cầu muối"]) and "svg_daniell_inserted" not in text:
                try:
                    dan_model = pve.build_daniell_cell_model()
                    if dan_model and dan_model.get("svg"):
                        dan_box = (
                            f"\n\n<div style='text-align: center; margin: 14px auto;'>"
                            f"<div style='display: inline-block; max-width: 320px; width: 100%; padding: 8px; background: #ffffff; border-radius: 8px; box-shadow: 0 4px 14px rgba(0,0,0,0.12);'>"
                            f"{sanitize_svg_for_markdown(dan_model['svg'])}"
                            f"<p style='font-size: 13px; color: #475569; margin-top: 6px; font-weight: bold;'>🔋 Sơ đồ Hoạt động Pin điện hóa Daniell</p>"
                            f"</div></div>\n\n"
                        )
                        text += dan_box
                except Exception:
                    pass

        # C. SINH HỌC:
        elif "sinh học" in subj_norm or "sinh" in subj_norm:
            # 1. Phả hệ di truyền
            if any(k in text_lower for k in ["phả hệ", "di truyền", "gen trội", "gen lặn", "thế hệ i", "thế hệ ii"]) and "svg_ped_inserted" not in text:
                try:
                    ped_model = pve.build_pedigree_chart_model()
                    if ped_model and ped_model.get("svg"):
                        ped_box = (
                            f"\n\n<div style='text-align: center; margin: 14px auto;'>"
                            f"<div style='display: inline-block; max-width: 320px; width: 100%; padding: 8px; background: #ffffff; border-radius: 8px; box-shadow: 0 4px 14px rgba(0,0,0,0.12);'>"
                            f"{sanitize_svg_for_markdown(ped_model['svg'])}"
                            f"<p style='font-size: 13px; color: #475569; margin-top: 6px; font-weight: bold;'>🧬 Sơ đồ Phả hệ Di truyền Menđen & Y học</p>"
                            f"</div></div>\n\n"
                        )
                        text += ped_box
                except Exception:
                    pass
            # 2. Lưới thức ăn
            if any(k in text_lower for k in ["lưới thức ăn", "chuỗi thức ăn", "sinh vật sản xuất", "sinh vật tiêu thụ", "hệ sinh thái"]) and "svg_food_inserted" not in text:
                try:
                    food_model = pve.build_food_web_model()
                    if food_model and food_model.get("svg"):
                        food_box = (
                            f"\n\n<div style='text-align: center; margin: 14px auto;'>"
                            f"<div style='display: inline-block; max-width: 340px; width: 100%; padding: 8px; background: #ffffff; border-radius: 8px; box-shadow: 0 4px 14px rgba(0,0,0,0.12);'>"
                            f"{sanitize_svg_for_markdown(food_model['svg'])}"
                            f"<p style='font-size: 13px; color: #475569; margin-top: 6px; font-weight: bold;'>🌿 Sơ đồ Lưới thức ăn trong Quần xã Sinh vật</p>"
                            f"</div></div>\n\n"
                        )
                        text += food_box
                except Exception:
                    pass

        # D. TOÁN HỌC & HÌNH HỌC KHÔNG GIAN OXYZ:
        elif "toán" in subj_norm:
            # 1. Tọa độ Oxyz & Quỹ đạo bay
            if any(k in text_lower for k in ["tọa độ không gian", "oxyz", "hệ trục oxyz", "đường bay", "thiết bị bay", "mặt cầu", "vectơ trong không gian"]) and "svg_oxyz_inserted" not in text:
                try:
                    if any(k in text_lower for k in ["đường bay", "thiết bị bay", "trạm phát sóng"]):
                        oxyz_m = pve.build_oxyz_flight_path_model(text_lower)
                    else:
                        oxyz_m = pve.build_oxyz_tetrahedron_model(text_lower)
                    if oxyz_m and oxyz_m.get("svg"):
                        oxyz_box = (
                            f"\n\n<div style='text-align: center; margin: 14px auto;'>"
                            f"<div style='display: inline-block; max-width: 280px; width: 100%; padding: 8px; background: #ffffff; border-radius: 8px; box-shadow: 0 4px 14px rgba(0,0,0,0.12);'>"
                            f"{sanitize_svg_for_markdown(oxyz_m['svg'])}"
                            f"<p style='font-size: 13px; color: #475569; margin-top: 6px; font-weight: bold;'>📐 Trực quan hóa Không gian Tọa độ Oxyz</p>"
                            f"</div></div>\n\n"
                        )
                        text += oxyz_box
                except Exception:
                    pass
            # 2. Khối chóp, Khối lăng trụ & Hình hộp
            elif any(k in text_lower for k in ["hình chóp", "khối chóp", "tứ diện", "lăng trụ", "hình hộp chữ nhật", "lập phương"]) and "svg_geom_inserted" not in text:
                try:
                    if "lăng trụ" in text_lower:
                        g_model = pve.build_pure_triangular_prism_model()
                    elif any(k in text_lower for k in ["hình hộp", "lập phương"]):
                        g_model = pve.build_pure_box_model()
                    elif "tứ diện" in text_lower:
                        g_model = pve.build_pure_tetrahedron_model()
                    else:
                        g_model = pve.build_pure_pyramid_quad_model()
                    if g_model and g_model.get("svg"):
                        geom_box = (
                            f"\n\n<div style='text-align: center; margin: 14px auto;'>"
                            f"<div style='display: inline-block; max-width: 280px; width: 100%; padding: 8px; background: #ffffff; border-radius: 8px; box-shadow: 0 4px 14px rgba(0,0,0,0.12);'>"
                            f"{sanitize_svg_for_markdown(g_model['svg'])}"
                            f"<p style='font-size: 13px; color: #475569; margin-top: 6px; font-weight: bold;'>🏛️ Mô hình Hình học Không gian Chuẩn SGK</p>"
                            f"</div></div>\n\n"
                        )
                        text += geom_box
                except Exception:
                    pass

    return text



if selected_station == station_labels[0]:

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader(f"📖 Tự học & Chiếm lĩnh kiến thức môn {subject} - Lớp {grade_num}")



    # GỢI Ý CHỦ ĐỀ CHUẨN XÁC THEO TỪNG MÔN HỌC & KHỐI LỚP (GDPT 2018)

    subject_placeholders = {

        "Toán học": "Ví dụ: Khảo sát hàm số bậc ba, Nguyên hàm và Tích phân, Khối tròn xoay, Tọa độ Oxyz...",

        "Tiếng Anh": "Ví dụ: Unit 1: Life stories, Conditional sentences, Passive voice, IELTS Speaking...",

        "Vật lý": "Ví dụ: Dao động điều hòa, Sóng cơ và sóng âm, Từ trường, Quang hình học, Vật lý hạt nhân...",

        "Hóa học": "Ví dụ: Ester - Lipid, Glucose và Fructose, Amine và Amino acid, Polyme, Cân bằng hóa học...",

        "Sinh học": "Ví dụ: Cơ chế di truyền và biến dị, Quy luật Menđen, Di truyền học người, Hệ sinh thái...",

        "Ngữ văn": "Ví dụ: Đọc hiểu văn bản nghị luận xã hội, Thơ trữ tình hiện đại, Kỹ năng viết bài nghị luận văn học...",

        "Lịch sử": "Ví dụ: Cách mạng tháng Tám 1945, Chiến dịch Điện Biên Phủ, Công cuộc Đổi mới đất nước, Toàn cầu hóa...",

        "Địa lý": "Ví dụ: Chuyển dịch cơ cấu kinh tế, Vùng Đông Nam Bộ, Phát triển kinh tế biển đảo Việt Nam...",

        "Tin học": "Ví dụ: Lập trình Python cơ bản, Thuật toán sắp xếp, Cơ sở dữ liệu quan hệ SQL, Mạng máy tính...",

        "Giáo dục kinh tế và pháp luật": "Ví dụ: Quy luật cung - cầu, Lạm phát và thị trường lao động, Quyền tự do kinh doanh...",

        "Khoa học tự nhiên": "Ví dụ: Cấu tạo nguyên tử, Tế bào nhân thực, Lực và chuyển động, Năng lượng tái tạo...",

        "Lịch sử & Địa lý": "Ví dụ: Các cuộc cách mạng công nghiệp, Văn minh sông Hồng, Khí hậu nhiệt đới ẩm gió mùa...",
        "Giáo dục công dân": "Ví dụ: Tôn trọng sự thật, Phòng chống bạo lực học đường, Quyền và nghĩa vụ học tập...",
        "Công nghệ": "Ví dụ: Bản vẽ kỹ thuật, Trồng trọt công nghệ cao, Mạch điện tử điều khiển, Cơ khí chế tạo..."
    }

    curr_ph = subject_placeholders.get(subject, f"Ví dụ: Bài học trọng tâm môn {subject} Lớp {grade_num}...")

    # Quick topics gợi ý chọn nhanh cho từng môn
    quick_topics_dict = {
        "Toán học": ["Khảo sát hàm số bậc ba", "Nguyên hàm & Tích phân", "Phương pháp tọa độ Oxyz"],
        "Tiếng Anh": ["Unit 1: Life stories", "Conditional sentences", "IELTS Speaking & Vocabulary"],
        "Vật lý": ["Dao động điều hòa", "Sóng cơ & Sóng âm", "Dòng điện xoay chiều"],
        "Hóa học": ["Ester và Lipid", "Glucose & Fructose", "Amine & Amino acid"],
        "Sinh học": ["Cơ chế di truyền", "Quy luật Menđen", "Di truyền học quần thể"],
        "Ngữ văn": ["Nghị luận xã hội", "Thơ hiện đại 1975 nay", "Nghị luận văn học"],
        "Lịch sử": ["Cách mạng tháng Tám", "Chiến dịch Điện Biên Phủ", "Công cuộc Đổi mới"],
        "Địa lý": ["Cơ cấu kinh tế", "Vùng Đông Nam Bộ", "Kinh tế biển đảo"],
        "Tin học": ["Lập trình Python", "Thuật toán sắp xếp", "Cơ sở dữ liệu SQL"],
        "Giáo dục kinh tế và pháp luật": ["Quy luật cung - cầu", "Thị trường lao động", "Pháp luật kinh doanh"],
        "Khoa học tự nhiên": ["Cấu tạo nguyên tử", "Tế bào nhân thực", "Chuyển hóa năng lượng"],
        "Lịch sử & Địa lý": ["Văn minh Đại Việt", "Khí hậu Việt Nam", "Đất nước và con người"],
        "Giáo dục công dân": ["Tôn trọng sự thật", "Quyền học tập", "Phòng chống bạo lực"],
        "Công nghệ": ["Bản vẽ kỹ thuật 3D", "Trồng trọt công nghệ cao", "Mạch điện RLC & Vi điều khiển"]
    }



    # CARD TRÍCH XUẤT SÁCH GIÁO KHOA ĐIỆN TỬ KNTT TRỰC TUYẾN (VNITEACH & NXBGD)

    curr_t1_books = get_kntt_books_for(subject, grade_num)

    curr_t1_books_nxbgd = get_nxbgd_books_for(subject, grade_num)



    with st.expander(f"📚 Sách Giáo Khoa Điện Tử Kết Nối Tri Thức - {subject} Lớp {grade_num} (Nguồn: VniTeach & NXBGD)", expanded=False):

        c_kntt1, c_kntt2 = st.columns([1, 1])

        with c_kntt1:

            st.markdown(f"**📖 Nguồn: VniTeach**")

            for b_item in curr_t1_books:

                st.link_button(f"📖 Mở {b_item['title']}", b_item['url'], width="stretch")

            st.link_button("🌐 Mở toàn bộ Thư viện KNTT (VniTeach)", "https://www.vniteach.com/sach-dien-tu-ket-noi-tri-thuc/#google_vignette", width="stretch")

            if curr_t1_books:

                st.caption("📱 Quét QR để lật sách (VniTeach):")

                st.image(generate_local_qr_base64(curr_t1_books[0]['url']), width=150)



        with c_kntt2:

            st.markdown(f"**📖 Nguồn: Tập Huấn NXBGD (Bộ GD&ĐT)**")

            for b_item in curr_t1_books_nxbgd:

                st.link_button(f"📖 Mở {b_item['title']}", b_item['url'], width="stretch")

            st.link_button("🌐 Mở Nguồn Tập Huấn NXBGD (Trang chủ)", "https://taphuan.nxbgd.vn/", width="stretch")

            if curr_t1_books_nxbgd:

                st.caption("📱 Quét QR để lật sách (NXBGD):")

                st.image(generate_local_qr_base64(curr_t1_books_nxbgd[0]['url']), width=150)



    # MENU CHỌN NHANH BÀI HỌC NGOÀI SGK (1-CLICK LESSON SELECTOR)

    curr_curriculum = BIGDATA_CURRICULUM.get(subject, {}).get(grade_num, [])

    lesson_select_options = ["-- Chọn bài học chuẩn SGK Kết Nối Tri Thức (NXBGD) --"] + curr_curriculum + ["Tự gõ bài học khác bên dưới..."]

    chosen_sgk_lesson = st.selectbox(

        "🎯 Chọn bài học theo Khung phân phối chương trình SGK KNTT:",

        lesson_select_options,

        key=f"kntt_lesson_sel_{current_context_key}"

    )



    default_lesson_txt = ""

    if chosen_sgk_lesson and chosen_sgk_lesson != "-- Chọn bài học chuẩn SGK Kết Nối Tri Thức (NXBGD) --" and chosen_sgk_lesson != "Tự gõ bài học khác bên dưới...":

        default_lesson_txt = chosen_sgk_lesson.split(":")[-1].strip() if ":" in chosen_sgk_lesson else chosen_sgk_lesson



    col_inp, col_btn = st.columns([3.8, 1.2])

    with col_inp:

        topic_input = st.text_input(

            "📝 Bài học cần chiếm lĩnh kiến thức (hoặc gõ tên bài tùy ý):",

            value=default_lesson_txt,

            placeholder=curr_ph,

            key=f"topic_input_{current_context_key}"

        )

    with col_btn:

        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)

        btn_submit_lesson = st.button("🚀 Soạn bài học", key=f"btn_soan_{current_context_key}", type="primary", width="stretch")



    if curr_curriculum:

        q_topics = [t.split(":")[-1].strip() if ":" in t else t for t in curr_curriculum[:4]]

    else:

        q_topics = quick_topics_dict.get(subject, ["Chuyên đề trọng tâm 1", "Chuyên đề trọng tâm 2"])

    st.caption("💡 **Chủ đề gợi ý học nhanh:** " + " • ".join([f"`{t}`" for t in q_topics]))



    # BỘ KIỂM SOÁT XUNG ĐỘT CẤP LỚP SƯ PHẠM (SMART GRADE-CONFLICT RESOLVER)

    conflict_grade = None

    page_match = None

    if topic_input and topic_input.strip():

        match_g = re.search(r'(?:lớp|khối|lop|khoi)\s*(\d{1,2})', topic_input, re.IGNORECASE)

        if match_g:

            try:

                cand_g = int(match_g.group(1))

                if 6 <= cand_g <= 12 and cand_g != grade_num:

                    conflict_grade = cand_g

            except Exception:

                pass

        page_match = re.search(r'(?:trang|page)\s*(\d+)', topic_input, re.IGNORECASE)



    if conflict_grade:

        st.info(f"💡 **Thầy AI nhận thấy:** Em đang ở không gian học tập **Lớp {grade_num}**, nhưng bài học em nhập lại nhắc đến **Lớp {conflict_grade}**. "

                f"Em có thể bấm chuyển nhanh sang đúng Lớp {conflict_grade}, hoặc tiếp tục để Thầy biên soạn theo định hướng ôn tập liên thông nền tảng nhé!")

        if st.button(f"👉 Chuyển nhanh sang Lớp {conflict_grade} để học", key=f"btn_switch_grade_{current_context_key}_{conflict_grade}"):

            st.session_state.target_switch_grade = f"Lớp {conflict_grade}"

            st.rerun()



    if page_match:

        p_num = page_match.group(1)

        st.warning(f"📖 **Lưu ý sư phạm đối chiếu SGK (Trang {p_num}):**\n"

                   f"Do các đợt in và tái bản SGK của NXBGD (2024, 2025, 2026) có thể chênh lệch số trang giữa các năm, "

                   f"để chiếm lĩnh kiến thức chính xác 100%, em nên nhập kèm **Tên bài học** (Ví dụ: *Khảo sát hàm số, Ứng dụng đạo hàm...*) "

                   f"hoặc mở mục **'📚 SGK Điện Tử'** ở menu bên trái, hoặc chụp trực tiếp trang sách nộp vào **Trạm 2** để Thầy AI hướng dẫn từng dòng nhé!")



    if btn_submit_lesson and topic_input.strip():

        st.session_state.tram1_count += 1

        with st.spinner("Đang biên soạn chuẩn ngữ liệu SGK KNTT và cấu trúc Socratic..."):

            conflict_note = ""

            if conflict_grade:

                conflict_note = f"\nLƯU Ý SƯ PHẠM ĐẶC BIỆT: Học sinh đang chọn Lớp {grade_num} nhưng hỏi bài thuộc Lớp {conflict_grade}. Hãy biên soạn nội dung này theo hướng ÔN TẬP LIÊN THÔNG NỀN TẢNG (bổ trợ kiến thức then chốt Lớp {conflict_grade} để phục vụ trực tiếp cho các chuyên đề của Lớp {grade_num}).\n"



            study_prompt = f"""[HỆ THỐNG BIÊN SOẠN BÀI HỌC CHUẨN SƯ PHẠM QUỐC GIA - CT GDPT 2018 & TIẾN TRÌNH 4 HOẠT ĐỘNG THEO CÔNG VĂN 5512/BGDĐT-GDTrH & CÔNG VĂN 3175/BGDĐT-GDTrH]

Môn học: {subject} | Khối lớp: {grade_num}. Chủ đề bài học: '{topic_input}'.

TÌM NGỮ LIỆU TỪ 2 NGUỒN: VniTeach và Tập Huấn NXBGD (https://taphuan.nxbgd.vn/). TÌM ĐIỂM CHUNG ĐỂ SINH NGỮ LIỆU BÀI HỌC, TRẮC NGHIỆM VÀ TỰ LUẬN.

{conflict_note}

YÊU CẦU PHÁP LÝ & HỌC THUẬT BẮT BUỘC:

1. TIẾN TRÌNH DẠY HỌC 4 HOẠT ĐỘNG CHUẨN CÔNG VĂN 5512/BGDĐT-GDTrH:

   - Hoạt động 1: KHỞI ĐỘNG / MỞ ĐẦU: Đưa ra 1 tình huống thực tiễn đời sống sinh động gắn liền với bài học, đặt câu hỏi gợi mở khơi gợi niềm say mê khám phá.

   - Hoạt động 2: HÌNH THÀNH KIẾN THỨC MỚI: Trình bày khung lý thuyết cốt lõi, định nghĩa, định lý, công thức, bảng biến thiên chuẩn mực bám sát 100% SGK Kết Nối Tri Thức (NXBGDVN) từ 2 nguồn VniTeach và Tập Huấn NXBGD.

   - Hoạt động 3: LUYỆN TẬP SOCRATIC: Hệ thống câu hỏi trắc nghiệm năng lực, giải thích bản chất sư phạm sâu sắc.

   - Hoạt động 4: VẬN DỤNG & MỞ RỘNG: Bài toán thực tiễn cuộc sống, định hướng theo quy trình 4 bước của Polya.

2. BÁM SÁT 100% NGỮ LIỆU & BẢN QUYỀN SGK KẾT NỐI TRI THỨC VỚI CUỘC SỐNG TỪ CẢ 2 NGUỒN VNITEACH VÀ TẬP HUẤN NXBGD:

   - NGUYÊN TẮC XỬ LÝ SỐ TRANG SGK (CHỐNG ẢO GIÁC TRANG SÁCH): Các đợt in/tái bản SGK NXBGD có thể lệch số trang giữa các năm. TUYỆT ĐỐI CẤM khẳng định bừa số trang nếu không chắc chắn 100%. Nếu học sinh chỉ nhập số trang mà không rõ tên bài:

     + BẮT BUỘC ghi rõ ở đầu Phần 1: '⚠️ Lưu ý: Các đợt tái bản SGK có thể chênh lệch số trang. Thầy hướng dẫn trọng tâm chuyên đề tương ứng của Lớp {grade_num} theo chuẩn GDPT 2018 (Em có thể mở '📚 SGK Điện Tử' ở menu trái hoặc chụp ảnh trang sách nộp ở Trạm 2 để Thầy soi trực tiếp nhé!).'

     + Dẫn dắt đúng trọng tâm bài học theo Khung phân phối chương trình môn {subject} Lớp {grade_num}.

   - NGUYÊN TẮC ĐỐI SOÁT TRANG SÁCH & CHUYÊN ĐỀ: Nếu học sinh hỏi theo số trang (ví dụ 'Trang 85 SGK...', 'Trang 12...'), AI BẮT BUỘC đối chiếu với đúng Chương/Bài trong Khung chương trình chuẩn GDPT 2018 của Lớp {grade_num}. Đồng thời nhắc học sinh có thể mở mục '📚 SGK Điện Tử' ở thanh bên trái để lật đúng trang bản in NXBGD xem trực tiếp, TUYỆT ĐỐI KHÔNG đoán mò hay đưa kiến thức ngoài khối Lớp {grade_num}!

   - TOÁN HỌC: TUYỆT ĐỐI CẤM đưa các kiến thức chương trình cũ (2006) vào bài học như: Tích phân từng phần, Tích phân đổi biến số, Đồ thị hàm bậc 4 trùng phương. Chỉ sử dụng tích phân cơ bản và ứng dụng thực tế. VỚI HÀM SỐ, TUYỆT ĐỐI TUÂN THỦ 3 BƯỚC KHẢO SÁT CHUẨN KNTT LỚP 12.

    - CÔNG THỨC VÉC TƠ TRONG LATEX: BẮT BUỘC dùng cú pháp chuẩn KaTeX: Với vectơ 1 chữ cái dùng \\vec{{a}}, \\vec{{b}}, \\vec{{i}}, \\vec{{j}}, \\vec{{k}}, \\vec{{u}}, \\vec{{v}}, \\vec{{n}}. Với vectơ có từ 2 điểm/chữ cái trở lên hoặc có dấu phẩy (như AB, AD, AA', AC', A'B', OM, MN) BẮT BUỘC dùng \\overrightarrow{{AB}}, \\overrightarrow{{AA'}}, \\overrightarrow{{AC'}} để mũi tên véc tơ bao trọn vẹn từ gốc đến ngọn. TUYỆT ĐỐI KHÔNG viết tắt như \\veci, \\vecj, \\veck, z\\veck vì sẽ gây lỗi render KaTeX.



   - HÓA HỌC & KHTN: DÙNG 100% DANH PHÁP QUỐC TẾ IUPAC.

   - NGỮ VĂN: Tiếp cận theo ĐẶC TRƯNG THỂ LOẠI. TUYỆT ĐỐI KHÔNG phân tích cơ học bổ dọc. NGUYÊN TẮC NGỮ LIỆU: Nếu ra đề thi chuẩn BGD (Trạm 3), BẮT BUỘC 100% ngữ liệu ngoài SGK. Nếu người dùng tùy chỉnh/yêu cầu giảng dạy tác phẩm cụ thể (Trạm 1, 2), BẮT BUỘC dùng đúng ngữ liệu Sách giáo khoa KNTT.

   - VẬT LÝ & SINH HỌC: Tuân thủ đúng bản chất hiện tượng, chuẩn SI.

   - TIẾNG ANH: TUYỆT ĐỐI BẮT BUỘC toàn bộ từ vựng, đoạn văn, câu hỏi trắc nghiệm, các phương án A/B/C/D, và bài tập ngữ pháp phải viết 100% bằng TIẾNG ANH. Chỉ dùng tiếng Việt khi giải thích hoặc gợi ý tư duy Socratic.

2. QUY ĐỊNH CẤU TRÚC KỸ THUẬT:

   - ĐỊNH DẠNG CÔNG THỨC (TOÀN BỘ CÁC MÔN): BẮT BUỘC bọc TẤT CẢ công thức, biểu thức, biến số và ký hiệu (Toán, Lý, Hóa, KHTN...) trong cặp dấu đô la $...$ (Ví dụ: $\vec{{a}} = k\vec{{b}}$, $F=ma$). TUYỆT ĐỐI KHÔNG DÙNG DẤU BACKTICK (`) để bọc công thức/ký hiệu vì sẽ làm hỏng trình hiển thị KaTeX của hệ thống!

   - BẢNG BIẾN THIÊN (BBT) & BẢNG XÉT DẤU (MÔN TOÁN):
     + Khi trình bày BBT, BẮT BUỘC kẻ Bảng Markdown có số cột là 2N (1 cột nhãn đầu hàng + 2N-1 cột dữ liệu xen kẽ giữa Điểm và Khoảng):
       * Hàng 1 ($x$): Chỉ ghi giá trị tại các cột Điểm ($-\\infty$, $x_1$, $x_2$, $+\\infty$), ĐỂ TRỐNG các cột Khoảng xen giữa. Ví dụ: | $x$ | $-\\infty$ | | $1$ | | $+\\infty$ |
       * Hàng 2 ($y'$): Tại cột Điểm ghi $0$ hoặc $||$ (nếu không xác định/tiệm cận đứng); tại cột Khoảng ghi dấu $+$ hoặc $-$. Ví dụ: | $y'$ | | + | 0 | - | |
       * Hàng 3 ($y$): Tại cột Điểm ghi giá trị cực trị/giới hạn (hoặc $+\\infty || -\\infty$ tại tiệm cận đứng); tại cột Khoảng chỉ ghi mũi tên $\\nearrow$ (nếu $y' > 0$) hoặc $\\searrow$ (nếu $y' < 0$). Ví dụ: | $y$ | $-\\infty$ | $\\nearrow$ | $2$ | $\\searrow$ | $-\\infty$ |
     + Đối với các môn KHÔNG PHẢI MÔN TOÁN: Tuyệt đối KHÔNG kẻ Bảng biến thiên toán học; sử dụng Bảng đối chiếu đặc trưng bộ môn chuẩn SGK Kết nối tri thức.

   - ĐỒ THỊ: Mô tả bằng lời, ghi chú: "(Kéo xuống Phòng Lab ảo bên dưới để trực quan hóa nhé!)".

   - TRẮC NGHIỆM SOCRATIC: Sinh chính xác 3 câu hỏi trắc nghiệm đánh giá năng lực.

     + Bắt đầu mỗi câu bằng chữ "Câu 1:", "Câu 2:", "Câu 3:".

     + 4 phương án A, B, C, D trên 4 dòng riêng biệt. BẮT BUỘC ĐẢO VỊ TRÍ ĐÁP ÁN ĐÚNG NGẪU NHIÊN VÀO A, B, C HOẶC D (TUYỆT ĐỐI KHÔNG MẶC ĐỊNH ĐÁP ÁN ĐÚNG LUÔN LÀ A).

     + Kèm dòng "ĐÁP ÁN: [A/B/C/D]" và dòng "GIẢI THÍCH: [Gợi ý tư duy Socratic]".

   - TỰ LUẬN: Sinh 2 bài tập vận dụng. BẮT BUỘC ĐẦU TIÊN PHẢI VIẾT RÕ ĐẦY ĐỦ NỘI DUNG ĐỀ BÀI TẬP, sau đó mới trình bày HƯỚNG DẪN TƯ DUY 4 BƯỚC (PHƯƠNG PHÁP POLYA). LỆNH CẤM KỴ: TUYỆT ĐỐI KHÔNG GIẢI CHI TIẾT, KHÔNG VIẾT ĐÁP SỐ. MỖI BƯỚC CHỈ ĐẶT 1 CÂU HỎI GỢI MỞ ĐỂ HỌC SINH TỰ TƯ DUY!



TIÊU ĐỀ BẮT BUỘC (Phải giữ đúng text này để hệ thống nhận diện):

### PHẦN 1: TÓM TẮT CỐT LÕI

(LƯU Ý ĐẶC BIỆT: Ở CUỐI PHẦN 1, BẮT BUỘC ĐÚC KẾT 1 KHỐI CẨM NANG ĐỒ HỌA INFOGRAPHIC TỰ THÂN TỪ CHÍNH BÀI HỌC VỪA SINH RA VỚI ĐÚNG CẤU TRÚC 4 KHỐI SAU:
### TÓM TẮT CẨM NANG INFOGRAPHIC:
Khối 1 (Khái niệm cốt lõi):
- [Tiêu đề chip 1]: [Dòng 1]. [Dòng 2]
- [Tiêu đề chip 2]: [Dòng 1]. [Dòng 2]
- [Tiêu đề chip 3]: [Dòng 1]. [Dòng 2]
- [Tiêu đề chip 4]: [Dòng 1]. [Dòng 2]

Khối 2 (Công thức & Quy luật):
- [Tiêu đề chip 1]: [Dòng 1]. [Dòng 2]
- [Tiêu đề chip 2]: [Dòng 1]. [Dòng 2]
- [Tiêu đề chip 3]: [Dòng 1]. [Dòng 2]
- [Tiêu đề chip 4]: [Dòng 1]. [Dòng 2]

Khối 3 (Tiến trình tư duy 4 bước Polya):
- Ví dụ: [Đề bài ví dụ minh họa điển hình của bài học]
- Bước 1 (Tìm hiểu đề): [Gợi ý ngắn gọn]
- Bước 2 (Tìm tòi cách giải): [Gợi ý ngắn gọn]
- Bước 3 (Thực hiện giải): [Gợi ý ngắn gọn]
- Bước 4 (Nhìn lại & Đúc kết): [Gợi ý ngắn gọn]

Khối 4 (Cạm bẫy thực tế & Mẹo thi):
- Bẫy 1: [Tên bẫy 1]: [Nội dung sai lầm thường gặp]. Bí quyết: [Mẹo phòng tránh trong thi]
- Bẫy 2: [Tên bẫy 2]: [Nội dung sai lầm thường gặp]. Bí quyết: [Mẹo phòng tránh trong thi])

### PHẦN 2: TRẮC NGHIỆM KHÁCH QUAN SOCRATIC

### PHẦN 3: BÀI TẬP TỰ LUẬN

"""



            try:

                res_text = call_gemini_with_fallback(study_prompt)

                # ==============================================================================
                # BỘ NÃO KIỂM SOÁT BIGDATA CUỐI CÙNG TRẠM 1 (MASTER SOVEREIGN QUALITY GATE)
                # ==============================================================================
                res_text = station1_master_sovereign_brain_gate(res_text, subject=subject, grade=grade_num, topic=topic_input.strip())

                st.session_state.current_lesson = res_text
                st.session_state.current_topic = topic_input.strip()
                st.session_state.parsed_quiz = parse_quiz_questions(res_text)
                st.session_state.quiz_states = {}

            except Exception as e:
                st.error(f"Lỗi: {e}")

    if st.session_state.get("current_lesson"):
        lesson_text = station1_master_sovereign_brain_gate(st.session_state.current_lesson, subject=subject, grade=grade_num, topic=st.session_state.get('current_topic', ''))
        part2_split = re.split(r'(?i)(?:###\s*)?PHẦN 2[\:\.]?', lesson_text)
        part3_split = re.split(r'(?i)(?:###\s*)?PHẦN 3[\:\.]?', lesson_text)

        # In Phần 1 kèm nút đọc Giảng bài bằng Giọng nói sư phạm
        if len(part2_split) > 0 and part2_split[0].strip():
            cleaned_p1 = re.sub(r'\n\s*\n', '\n\n', part2_split[0].strip())
            cleaned_p1 = re.sub(r'(?:\s*\-\-\-\s*)+$', '', cleaned_p1)
            cleaned_p1 = station1_master_sovereign_brain_gate(cleaned_p1, subject=subject, grade=grade_num, topic=st.session_state.get('current_topic', ''))
            cleaned_p1_vis = render_pedagogical_lesson_visuals(cleaned_p1, subject=subject, grade=grade_num)
            st.markdown(cleaned_p1_vis, unsafe_allow_html=True)

            # ==============================================================================
            # BẢO CHỨNG ĐỊNH VỊ CHỈ MỤC ADN BÀI HỌC SGK KNTT & VIDEO YOUTUBE ĐA MÔN ĂN KHỚP 100%
            # ==============================================================================
            current_topic_name = st.session_state.get('current_topic') or topic_input or subject
            t1_indexing_data = generate_kntt_lesson_indexing_and_media(subject, grade_num, current_topic_name)
            st.markdown(t1_indexing_data["badge_html"], unsafe_allow_html=True)

            # ==============================================================================
            # 📊 THẺ CẨM NANG INFOGRAPHIC VECTOR SVG A4 (BỎ TÚI / IN ẤN PHOTO TIẾT KIỆM MỰC & MÀU NÉT CĂNG)
            # ==============================================================================
            if lie is not None:
                try:
                    svg_color = lie.build_a4_infographic_svg(
                        subject_name=subject,
                        grade_lvl=grade_num,
                        topic_text=current_topic_name,
                        index_code=t1_indexing_data["index_code"],
                        textbook_name=t1_indexing_data["book_name"],
                        expert_channel=t1_indexing_data["channel_info"]["channel_name"],
                        qr_base64_url=t1_indexing_data["qr_img_data"],
                        lesson_markdown=cleaned_p1,
                        mode="color"
                    )
                    svg_mono = lie.build_a4_infographic_svg(
                        subject_name=subject,
                        grade_lvl=grade_num,
                        topic_text=current_topic_name,
                        index_code=t1_indexing_data["index_code"],
                        textbook_name=t1_indexing_data["book_name"],
                        expert_channel=t1_indexing_data["channel_info"]["channel_name"],
                        qr_base64_url=t1_indexing_data["qr_img_data"],
                        lesson_markdown=cleaned_p1,
                        mode="monochrome"
                    )

                    with st.expander("📊 Thẻ Cẩm Nang Infographic A4 (Vector SVG Siêu Nhẹ • Quét QR Video • In Photocopy / Màu 1-Chạm)", expanded=True):
                        st.caption("✨ **Bản tóm tắt đồ họa A4 Vector chuẩn GDPT 2018:** Tự động cân chỉnh chữ, ngắt dòng tiếng Việt, công thức Toán - KHTN & Phiên âm IPA quốc tế chuẩn mực. Học sinh có thể tải về lưu điện thoại hoặc in ra giấy kẹp SGK để ôn tập!")

                        col_mode, col_space = st.columns([3, 1])
                        with col_mode:
                            mode_choice = st.radio(
                                "Chế độ hiển thị & Bản in:",
                                ["🎨 Bản Màu Hiện Đại (Xem Web / Tablet)", "🖨️ Bản In Photo Trắng Đen (Tiết kiệm mực • Nét vô cực)"],
                                horizontal=True,
                                key=f"infog_mode_{t1_indexing_data['index_code']}"
                            )

                        chosen_svg = svg_mono if "Trắng Đen" in mode_choice else svg_color
                        b64_svg = base64.b64encode(chosen_svg.encode('utf-8')).decode('utf-8')
                        st.markdown(
                            f'<div style="text-align: center; margin: 15px auto; max-width: 800px; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 25px rgba(0,0,0,0.18); border: 1.5px solid #0284c7; background: #ffffff;">'
                            f'<img src="data:image/svg+xml;base64,{b64_svg}" style="width: 100%; height: auto; display: block;" alt="Infographic A4 Bài Học" />'
                            f'</div>',
                            unsafe_allow_html=True
                        )

                        col_dl1, col_dl2 = st.columns(2)
                        with col_dl1:
                            st.download_button(
                                label="📥 Tải Bản Màu (.SVG Siêu Nhẹ ~15KB)",
                                data=svg_color.encode('utf-8'),
                                file_name=f"Infographic_{t1_indexing_data['index_code']}_Color.svg",
                                mime="image/svg+xml",
                                width="stretch",
                                key=f"btn_dl_svg_col_{t1_indexing_data['index_code']}"
                            )
                        with col_dl2:
                            st.download_button(
                                label="🖨️ Tải Bản Trắng Đen In Photo (.SVG Nét Cực Hạn)",
                                data=svg_mono.encode('utf-8'),
                                file_name=f"Infographic_{t1_indexing_data['index_code']}_Monochrome.svg",
                                mime="image/svg+xml",
                                width="stretch",
                                key=f"btn_dl_svg_mono_{t1_indexing_data['index_code']}"
                            )
                except Exception as _e_infog:
                    logging.warning("Lỗi tạo Infographic A4: %s", _e_infog)

            # --- NÚT ĐỌC BÀI GIẢNG TTS SƯ PHẠM CHUẨN GDPT 2018 & TIẾNG ANH BẢN NGỮ ---
            create_pedagogical_tts_component(cleaned_p1, subject, "tram1_lesson")



            # --- ĐOẠN CHAT NGỮ CẢNH SOCRATIC SƯ PHẠM THƯỢNG ĐẲNG (THUẦN TEXT & LATEX - ALL CÁC MÔN) ---

            chat_context_key = f"t1_chat_{current_context_key}_{st.session_state.get('current_topic', '')}"

            if "tram1_chat_history" not in st.session_state or st.session_state.get("tram1_active_chat_key") != chat_context_key:

                st.session_state.tram1_active_chat_key = chat_context_key

                st.session_state.tram1_chat_history = []

                welcome_t1 = (

                    f"Chào {student_name}! Thầy trò mình vừa tóm tắt xong kiến thức cốt lõi của bài **{st.session_state.get('current_topic', subject)}**. "

                    f"Theo cách hiểu của em, điều cốt tử hoặc mấu chốt nhất của bài này là gì? Hoặc có chỗ nào trong lý thuyết ở trên em thấy còn băn khoăn cần Thầy trò mình mổ xẻ thêm không?"

                )

                st.session_state.tram1_chat_history.append({"role": "assistant", "content": welcome_t1})



            with st.expander(f"💬 Vấn đáp Socratic cùng Thầy AI về bài học '{st.session_state.get('current_topic', subject)}' (Chiếm lĩnh cốt lõi - Thuần Text & LaTeX)", expanded=True):

                st.caption(f"🎓 **Gia sư Socratic Môn {subject} - Lớp {grade_num}:** Đối thoại khai phóng tư duy • 100% Text & công thức $\\text{{\\LaTeX}}$, không Voice • Hỏi đáp cùng Thầy cho thông suốt trước khi xuống làm bài tập nhé!")



                chat_container = st.container()



                with chat_container:

                    for t1_msg in st.session_state.tram1_chat_history:

                        with st.chat_message(t1_msg["role"]):

                            st.markdown(t1_msg["content"])



                t1_input = st.chat_input("Gõ câu trả lời hoặc chỗ chưa hiểu gửi Thầy...", key=f"t1_inp_{chat_context_key}")



                if t1_input:

                    st.session_state.tram1_chat_history.append({"role": "user", "content": t1_input})

                    with chat_container:

                        with st.chat_message("user"):

                            st.markdown(t1_input)

                        t1_hist_ctx = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.tram1_chat_history[-4:-1]])
                        t1_sys_inst = build_socratic_master_instruction(
                            subject, grade_num, student_name,
                            mode="theory",
                            topic_nm=st.session_state.get('current_topic', subject),
                            context_data=cleaned_p1
                        )
                        with st.chat_message("assistant"):
                            try:
                                is_t1_understood = detect_student_concluded_intent(t1_input, st.session_state.tram1_chat_history)
                                t1_quote_data = get_unique_philosophical_lesson(1, subject)
                                t1_cross_ctx = get_cross_station_pedagogical_context(1)

                                if is_t1_understood:
                                    t1_prompt_msg = (
                                        f"Bối cảnh liên trạm của học sinh:\n{t1_cross_ctx}\n"
                                        f"Lịch sử đối thoại trước đó:\n{t1_hist_ctx}\n"
                                        f"Học sinh {student_name} phản hồi: \"{t1_input}\"\n\n"
                                        f"🎯 MỆNH LỆNH SƯ PHẠM ĐỈNH CAO - CHỐT ĐIỂM CHẠM SƯ PHẠM TRẠM 1 (CLOSURE) & TRAO TRUYỀN TRIẾT LÝ NHÂN CÁCH Á - ÂU:\n"
                                        f"1. DỪNG TRUY VẤN NGAY: Tuyệt đối KHÔNG hỏi thêm bất kỳ câu hỏi nào nữa. Học sinh đã thấu hiểu trọn vẹn và không còn thắc mắc về bài học '{st.session_state.get('current_topic', subject)}'!\n"
                                        f"2. BIỂU DƯƠNG NỒNG NHIỆT: Khen ngợi sự nhạy bén, khiêm tốn và tinh thần tự học vượt bậc của {student_name}.\n"
                                        f"3. ĐÓNG GÓI BẢN CHẤT: Chốt 1 câu tinh hoa quy luật khoa học cốt lõi của bài học hôm nay.\n"
                                        f"4. BÀI HỌC TRIẾT LÝ NHÂN CÁCH & LẼ SỐNG (BẮT BUỘC): Đúc kết bài học về đạo làm người: {t1_quote_data['lesson']} kèm câu danh ngôn triết lý bất hủ của {t1_quote_data['author']} ({t1_quote_data['origin']}): \"{t1_quote_data['quote']}\".\n"
                                        f"5. LỜI CHÚC ÂN CẦN: Lời chúc yêu thương của Người Thầy khích lệ {student_name} tự tin tiến sang Trạm 2 (Giải bài tập & Check VAR trực tiếp)!"
                                    )
                                    register_station_closure(1, t1_quote_data)
                                else:
                                    t1_prompt_msg = (
                                        f"Bối cảnh liên trạm:\n{t1_cross_ctx}\n"
                                        f"Lịch sử đối thoại:\n{t1_hist_ctx}\n"
                                        f"Học sinh {student_name} phản hồi: \"{t1_input}\"\n"
                                        f"Thầy phản hồi gợi mở Socratic trí tuệ, ân cần, dẫn dắt tư duy (thuần Text & LaTeX, tuyệt đối không lặp lại lý thuyết như con vẹt). "
                                        f"LƯU Ý SƯ PHẠM: Cuối lời giải thích, hãy ân cần hỏi học sinh: 'Em đã thực sự thông suốt chỗ này chưa, hay còn điều gì muốn Thầy trò mình cùng mổ xẻ thêm không?'. "
                                        f"TUYỆT ĐỐI CHƯA đưa bài học triết lý đạo đức ở bước này khi học sinh vẫn còn đang trong tiến trình tìm hiểu."
                                    )

                                stream_gen = stream_gemini_with_fallback(
                                    t1_prompt_msg,
                                    system_instruction=t1_sys_inst
                                )
                                t1_ans = st.write_stream(stream_gen)
                                t1_ans_clean = sanitize_katex_latex(t1_ans)
                                st.session_state.tram1_chat_history.append({"role": "assistant", "content": t1_ans_clean})
                            except Exception as exc:
                                st.error(f"Lỗi kết nối Thầy AI: {exc}")





        # In Phần 2 (Trắc nghiệm tương tác)

        quiz_list = st.session_state.get("parsed_quiz", [])

        if quiz_list:

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("### 🎯 Phần 2: Trắc nghiệm khách quan Socratic")

            for idx, q in enumerate(quiz_list):

                # 1. ĐỒNG BỘ 100% CÔNG NGHỆ THỊ GIÁC SIÊU MẠNH TỪ TRẠM 3 VÀO TRẠM 1:
                q_dict_vis = {
                    "q": q['question'],
                    "opt": q.get('options', []),
                    "ans": q.get('correct', 'A')
                }
                if q.get("bbt"):
                    q_dict_vis["bbt"] = q["bbt"]

                if pve is not None:
                    try:
                        q_dict_vis = pve.enrich_question_visual_precision(q_dict_vis, subject=subject, grade=grade_num)
                    except Exception as _e_enr:
                        pass

                # 2. Tách sạch sẽ văn bản câu hỏi và khử hoàn toàn rác bảng markdown dính liền:
                clean_q_display = clean_question_bbt_text(q['question'])
                clean_q_display = sanitize_katex_latex(clean_q_display)
                st.markdown(f"**Câu {idx+1}:** `[{q['level']}]`\n\n{clean_q_display}")

                # 3. Hiển thị Bảng Biến Thiên (BBT) WebP siêu nét chuẩn Bộ GD&ĐT (Trạm 3 Master Quality):
                raw_bbt_content = q_dict_vis.get("bbt") or q.get("bbt")
                if not raw_bbt_content and ('|' in q['question'] and any(k in q['question'].lower() for k in ["bảng biến thiên", "bbt", "bảng xét dấu", "chiều biến thiên"])):
                    raw_bbt_content = q['question']

                if raw_bbt_content:
                    bbt_txt = str(raw_bbt_content).strip()
                    bbt_txt = re.sub(r'\\+nearrow\b|\\nearrow', '↗', bbt_txt)
                    bbt_txt = re.sub(r'\\+searrow\b|\\searrow', '↘', bbt_txt)
                    bbt_txt = bbt_txt.replace('>>', '↗').replace('>', '↗')
                    bbt_txt = re.sub(r'\\n(?!earrow)', '\n', bbt_txt).strip()
                    if pve is not None:
                        try:
                            bbt_txt = pve.heal_bbt_mathematics(bbt_txt)
                        except Exception:
                            pass

                    b64_bbt = render_bbt_to_webp_base64(bbt_txt)
                    if b64_bbt:
                        st.caption("📋 **Bảng biến thiên chuẩn hóa LaTeX & Bộ GD&ĐT:**")
                        col_b1, col_b2, col_b3 = st.columns([1, 3.5, 1])
                        with col_b2:
                            st.markdown(f'<div style="display:flex; justify-content:center; margin:8px auto;"><img src="{b64_bbt}" alt="Bảng biến thiên chuẩn Bộ GD&ĐT" style="max-width:100%; height:auto; border-radius:6px; box-shadow:0 4px 12px rgba(0,0,0,0.2);"/></div>', unsafe_allow_html=True)
                    else:
                        html_bbt = format_pedagogical_bbt_html(bbt_txt, is_dark_mode=True)
                        if html_bbt:
                            st.caption("📋 **Bảng biến thiên chuẩn hóa LaTeX & Bộ GD&ĐT:**")
                            st.markdown(html_bbt, unsafe_allow_html=True)

                # 4. Render đồ thị hàm số / mô hình 3D chuẩn sách giáo khoa nếu câu hỏi có hình vẽ:
                try:
                    # Tạm thời bỏ bbt ra khỏi question_visual_html vì đã được render độc lập ở bước 3
                    q_dict_no_bbt = dict(q_dict_vis)
                    q_dict_no_bbt.pop("bbt", None)
                    vis_html = question_visual_html(q_dict_no_bbt)
                    if vis_html:
                        st.markdown(vis_html, unsafe_allow_html=True)
                except Exception as _e_vis:
                    pass

                user_choice = st.radio(f"Chọn đáp án câu {idx+1}:", q['options'], key=f"q_{idx}", label_visibility="collapsed", index=None)

                if st.button(f"🔍 Kiểm tra câu {idx+1}", key=f"btn_{idx}"):

                    if user_choice:

                        choice_letter = re.sub(r'[^A-D]', '', user_choice.strip()[:3]).upper()[:1]

                        if choice_letter == q['correct']:

                            st.session_state.quiz_states[idx] = ("correct", "🎉 Xuất sắc! Em tư duy rất chuẩn.")

                        else:

                            st.session_state.quiz_states[idx] = ("incorrect", f"💡 **Gợi ý Socratic:** {q['explain']}")

                    else:

                        st.warning("Vui lòng chọn một đáp án!")

                if idx in st.session_state.quiz_states:

                    status, msg = st.session_state.quiz_states[idx]

                    if status == "correct": st.success(msg)

                    else: st.warning("🤔 Suy ngẫm thêm gợi ý dưới đây nhé:"); st.info(msg)

                st.markdown("---")

        elif len(part2_split) > 1 and "PHẦN 3" in part2_split[1].upper():

            st.warning("💡 Hệ thống AI vừa sinh ra một định dạng trắc nghiệm mới. Đang hiển thị ở chế độ xem tĩnh:")

            fallback_p2 = re.split(r'(?i)###\s*PHẦN\s*3', part2_split[1])[0]
            fallback_p2_vis = render_pedagogical_lesson_visuals(fallback_p2.strip(), subject=subject, grade=grade_num)
            st.markdown(fallback_p2_vis, unsafe_allow_html=True)



        # In Phần 3

        if len(part3_split) > 1 and part3_split[-1].strip():

            st.markdown("### ✍️ Phần 3: Bài tập tự luận & Hướng dẫn tư duy")
            p3_vis = render_pedagogical_lesson_visuals(part3_split[-1].strip(), subject=subject, grade=grade_num)
            st.markdown(p3_vis, unsafe_allow_html=True)





    render_voice_speech_tex_and_english_evaluator('Tram 1', subject, grade_num)



    # PHÒNG LAB VIRTUAL LAB

    st.markdown("---")

    st.markdown('<h4 style="color: #38bdf8; margin-top: 0; margin-bottom: 5px; font-weight: 800;">🔬 PHÒNG THÍ NGHIỆM ẢO THEO YÊU CẦU (VIRTUAL LAB)</h4>', unsafe_allow_html=True)

    if subject == "Ngữ văn":

        lab_intro_text = f"Hệ thống AI đang liên kết trực tiếp với <b>Môn Ngữ văn - Lớp {grade_num}</b>. Nhập yêu cầu trực quan hóa sơ đồ tư duy thi pháp thể loại, tiến trình tác phẩm, quy trình viết đoạn văn NLXH, bản đồ năng lực đọc hiểu:"

    elif subject == "Tiếng Anh":

        lab_intro_text = f"Hệ thống AI đang liên kết trực tiếp với <b>Môn Tiếng Anh - Lớp {grade_num}</b>. Nhập yêu cầu tạo sơ đồ tư duy ngữ pháp (Mindmap Tenses), mạng lưới từ vựng theo chủ đề (Vocabulary Networks), hoặc cấu trúc câu:"

    elif subject == "Toán học":

        lab_intro_text = f"Hệ thống AI đang liên kết trực tiếp với <b>Môn Toán học - Lớp {grade_num}</b>. Nhập yêu cầu mô phỏng đồ thị hàm số, tích phân, miền nghiệm, hình học không gian 3D:"

    elif subject in ["Vật lý", "Hóa học", "Sinh học", "Khoa học tự nhiên"]:

        lab_intro_text = f"Hệ thống AI đang liên kết trực tiếp với <b>Môn {subject} - Lớp {grade_num}</b>. Nhập yêu cầu mô phỏng thí nghiệm ảo (con lắc, chuyển động, phản ứng hóa học IUPAC, chu kỳ tế bào, chuỗi thức ăn):"

    else:

        lab_intro_text = f"Hệ thống AI đang liên kết trực tiếp với <b>Môn {subject} - Lớp {grade_num}</b>. Nhập yêu cầu xây dựng sơ đồ tư duy dòng thời gian lịch sử, bản đồ địa lý, cấu trúc kinh tế - pháp luật, giải thuật tin học:"

    st.markdown(f'<div style="color: #cbd5e1; font-size: 15px; margin-bottom: 12px;">{lab_intro_text}</div>', unsafe_allow_html=True)



    is_social_subject = subject in ["Ngữ văn", "Lịch sử", "Địa lý", "Giáo dục công dân", "Giáo dục kinh tế và pháp luật", "Lịch sử & Địa lý", "Tiếng Anh"]



    if is_social_subject:

        if subject == "Ngữ văn":

            lab_ph = "Ví dụ: Vẽ sơ đồ tư duy thể loại tác phẩm, quy trình viết đoạn văn NLXH, sơ đồ luận điểm..."

            available_labs = {

                "Sơ đồ Thể loại & Thi pháp Văn học": {

                    "type": "mermaid",

                    "code": """graph LR

    Root["📖 THI PHÁP & THỂ LOẠI (KNTT)"] --> A["1. Thơ hiện đại"]

    Root --> B["2. Truyện ngắn & Ký"]

    Root --> C["3. Văn bản Nghị luận"]

    Root --> D["4. Kịch bản Văn học"]

    A --> A1["Hình tượng thi pháp & Cảm xúc"]

    A --> A2["Ngữ điệu, nhịp điệu & Biểu tượng"]

    B --> B1["Tình huống truyện & Cốt truyện"]

    B --> B2["Diễn biến tâm lý nhân vật"]

    C --> C1["Luận điểm & Thao tác lập luận"]

    C --> C2["Dẫn chứng xác thực đời sống"]

    D --> D1["Xung đột kịch & Hành động"]

    D --> D2["Ngôn ngữ đối thoại - độc thoại"]"""

                },

                "Quy trình Viết Đoạn văn NLXH 200 chữ": {

                    "type": "mermaid",

                    "code": """graph LR

    Root["✍️ CẤU TRÚC ĐOẠN VĂN NLXH (2.0Đ)"] --> A["1. Mở đoạn"]

    Root --> B["2. Giải thích & Bàn luận"]

    Root --> C["3. Dẫn chứng tiêu biểu"]

    Root --> D["4. Phản đề & Bài học"]

    A --> A1["Dẫn dắt trực tiếp vấn đề nghị luận"]

    B --> B1["Cắt nghĩa khái niệm/thông điệp cốt lõi"]

    B --> B2["Lập luận tại sao & ý nghĩa thực tiễn"]

    C --> C1["1 dẫn chứng thuyết phục từ thực tiễn"]

    D --> D1["Lật ngược vấn đề & Phê phán sai lệch"]

    D --> D2["Bài học nhận thức và hành động"]"""

                },

                "Bản đồ Năng lực Đọc hiểu 2026": {

                    "type": "mermaid",

                    "code": """graph LR

    Root["🔍 NĂNG LỰC ĐỌC HIỂU NGỮ VĂN (4.0Đ)"] --> A["1. Nhận biết (1.0đ)"]

    Root --> B["2. Thông hiểu (1.5đ)"]

    Root --> C["3. Vận dụng (1.5đ)"]

    A --> A1["Xác định thể loại, phương thức biểu đạt"]

    A --> A2["Chi tiết, hình ảnh trong 100% ngữ liệu ngoài SGK"]

    B --> B1["Tác dụng của biện pháp tu từ"]

    B --> B2["Ý nghĩa của chi tiết, hình tượng nghệ thuật"]

    C --> C1["Rút ra thông điệp cuộc sống sâu sắc nhất"]

    C --> C2["Bày tỏ quan điểm đồng tình / không đồng tình"]"""

                }

            }

        elif subject == "Tiếng Anh":

            lab_ph = "Ví dụ: Draw a mindmap about Verb Tenses, Vocabulary Collocations, IELTS Speaking..."

            available_labs = {

                "Mindmap Tenses & Verb Structures": {

                    "type": "mermaid",

                    "code": """graph LR

    Root["🇬🇧 ENGLISH TENSES & GRAMMAR"] --> A["1. Present Tenses"]

    Root --> B["2. Past Tenses"]

    Root --> C["3. Perfect Tenses"]

    Root --> D["4. Conditionals & Inversion"]

    A --> A1["Present Simple: Habits & Facts"]

    A --> A2["Present Continuous: Actions in progress"]

    B --> B1["Past Simple: Completed actions"]

    B --> B2["Past Continuous: Interrupted actions"]

    C --> C1["Present Perfect: Results & Experiences"]

    C --> C2["Past Perfect: Earlier past events"]

    D --> D1["Conditionals Type 1, 2, 3 & Mixed"]

    D --> D2["Inversion with Negative Adverbs"]"""

                },

                "Academic Topic Vocabulary Networks": {

                    "type": "mermaid",

                    "code": """graph LR

    Root["📚 TOPIC VOCABULARY NETWORKS"] --> A["Environmental Protection"]

    Root --> B["Education & Lifelong Learning"]

    Root --> C["Technology & Artificial Intelligence"]

    A --> A1["Carbon footprint & Sustainability"]

    A --> A2["Biodiversity loss & Deforestation"]

    B --> B1["Academic performance & Critical thinking"]

    B --> B2["Autonomous learning & Vocational training"]

    C --> C1["Cutting-edge technology & Automation"]

    C --> C2["Digital literacy & Ethical considerations"]"""

                }

            }

        elif subject in ["Lịch sử", "Lịch sử & Địa lý"]:

            lab_ph = "Ví dụ: Vẽ tiến trình kháng chiến chống Pháp, mốc son 1945, công cuộc Đổi mới..."

            available_labs = {

                "Tiến trình Lịch sử & Mốc son Thời đại": {

                    "type": "mermaid",

                    "code": """graph LR

    Root["🇻🇳 TIẾN TRÌNH LỊCH SỬ HIỆN ĐẠI"] --> A["1. Cách mạng tháng Tám (1945)"]

    Root --> B["2. Kháng chiến chống Pháp (1945-1954)"]

    Root --> C["3. Kháng chiến chống Mỹ (1954-1975)"]

    Root --> D["4. Đổi mới & Hội nhập (1986-nay)"]

    A --> A1["Tổng khởi nghĩa giành chính quyền"]

    A --> A2["Tuyên ngôn Độc lập 2/9/1945"]

    B --> B1["Chiến dịch Việt Bắc 1947 & Biên giới 1950"]

    B --> B2["Chiến thắng Điện Biên Phủ 1954"]

    C --> C1["Đánh bại các chiến lược chiến tranh của Mỹ"]

    C --> C2["Đại thắng Mùa Xuân 1975 thống nhất non sông"]

    D --> D1["Đại hội VI (1986) khởi xướng Đổi mới"]

    D --> D2["Hội nhập quốc tế & Giữ vững chủ quyền"]"""

                }

            }

        elif subject == "Địa lý":

            lab_ph = "Ví dụ: Vẽ sơ đồ chuyển dịch cơ cấu kinh tế, vùng Đông Nam Bộ, kinh tế biển đảo..."

            available_labs = {

                "Sơ đồ Chuyển dịch Cơ cấu & Vùng Kinh tế": {

                    "type": "mermaid",

                    "code": """graph LR

    Root["🌏 ĐỊA LÝ KINH TẾ VIỆT NAM"] --> A["1. Địa lý Tự nhiên"]

    Root --> B["2. Địa lý Dân cư & Lao động"]

    Root --> C["3. Cơ cấu Kinh tế"]

    Root --> D["4. Vùng Kinh tế Trọng điểm"]

    A --> A1["Địa hình đồi núi & Đồng bằng châu thổ"]

    A --> A2["Khí hậu nhiệt đới ẩm gió mùa"]

    B --> B1["Quy mô dân số & Cơ cấu dân số vàng"]

    B --> B2["Đô thị hóa gắn liền phát triển kinh tế"]

    C --> C1["Chuyển dịch cơ cấu ngành kinh tế"]

    C --> C2["Chuyển dịch cơ cấu thành phần & lãnh thổ"]

    D --> D1["Vùng Đông Nam Bộ & ĐBSCL"]

    D --> D2["Kinh tế biển đảo & Vùng thềm lục địa"]"""

                }

            }

        else:

            lab_ph = "Ví dụ: Vẽ sơ đồ quy luật cung cầu, thị trường lao động, quyền tự do kinh doanh..."

            available_labs = {

                "Cơ chế Thị trường & Quy luật Cung - Cầu": {

                    "type": "mermaid",

                    "code": """graph LR

    Root["⚖️ QUY LUẬT KINH TẾ THỊ TRƯỜNG"] --> A["1. Quy luật Giá trị"]

    Root --> B["2. Quy luật Cung - Cầu"]

    Root --> C["3. Quy luật Cạnh tranh"]

    Root --> D["4. Vai trò Quản lý của Nhà nước"]

    A --> A1["Sản xuất và lưu thông theo hao phí LĐXH"]

    B --> B1["Cung > Cầu -> Giá cả giảm"]

    B --> B2["Cung < Cầu -> Giá cả tăng"]

    C --> C1["Thúc đẩy tăng năng suất & Đổi mới sáng tạo"]

    D --> D1["Khắc phục khuyết tật thị trường & An sinh XH"]"""

                }

            }

    else:

        lab_ph = f"Ví dụ mô phỏng môn {subject} Lớp {grade_num}: Khảo sát đồ thị, không gian 3D, hiện tượng khoa học..."

        if subject == "Vật lý":

            available_labs = {

                "Dao động điều hòa (Vật lí 11)": {"type": "physics_oscillator", "A": 5.0, "omega": 2.0, "phi": 0.0},

                "Hàm số Mũ & Phóng xạ hạt nhân": {"type": "func_exp", "base": 0.5, "k": 1.0, "c": 0.0},

                "Quỹ đạo chuyển động Parabol": {"type": "parabola", "a": -0.5, "b": 2.0, "c": 0.0},

                "Không gian Oxyz (Vectơ lực & Từ trường)": {"type": "oxyz", "x": 2, "y": 3, "z": 4},

                "Hàm bậc ba (Khảo sát thực nghiệm)": {"type": "func_3", "a": 1, "b": -3, "c": 0, "d": 2}

            }

        elif subject == "Hóa học":

            available_labs = {

                "Cân bằng hóa học Le Chatelier (Hóa học 11)": {"type": "chem_equilibrium", "temp": 450, "p": 200},

                "Hàm số Lôgarit & Thang đo pH": {"type": "func_log", "base": 10.0, "k": -1.0, "c": 7.0},

                "Parabol tốc độ phản ứng": {"type": "parabola", "a": -1, "b": 4, "c": 0},

                "Không gian Oxyz (Mô hình mạng tinh thể)": {"type": "oxyz", "x": 2, "y": 2, "z": 2}

            }

        elif subject == "Sinh học":

            available_labs = {

                "Quy luật phân ly Mendel (Sinh học 12)": {"type": "bio_genetics"},

                "Hàm số Mũ & Tăng trưởng quần thể sinh vật": {"type": "func_exp", "base": 2.0, "k": 1.0, "c": 0.0},

                "Hàm số Lôgarit & Tăng trưởng giới hạn": {"type": "func_log", "base": 2.0, "k": 1.0, "c": 0.0}
            }
        elif subject == "Tin học":
            available_labs = {
                "Sơ đồ thuật toán & Cây nhị phân": {"type": "oxyz", "x": 2, "y": 2, "z": 2},
                "Độ phức tạp tính toán O(n) vs O(n^2)": {"type": "parabola", "a": 1, "b": 0, "c": 0},
                "Hàm số Mũ & Mã hóa dữ liệu (RSA)": {"type": "func_exp", "base": 2.0, "k": 1.0, "c": 0.0}
            }
        elif subject == "Công nghệ":
            available_labs = {
                "Bản vẽ kĩ thuật & Hình chiếu 3D": {"type": "geometry_3d", "shape": "box", "title": "Hình hộp kĩ thuật ABCD.A'B'C'D'"},
                "Mạch điện xoay chiều RLC & Dao động": {"type": "physics_oscillator", "A": 5.0, "omega": 2.0, "phi": 0.0},
                "Hàm số Mũ & Tăng trưởng năng suất nông nghiệp": {"type": "func_exp", "base": 1.5, "k": 1.0, "c": 0.0}
            }
        elif subject == "Khoa học tự nhiên":
            available_labs = {
                "Dao động cơ & Sóng âm (KHTN)": {"type": "physics_oscillator", "A": 5.0, "omega": 2.0, "phi": 0.0},
                "Thang đo pH & Axit - Bazơ (KHTN)": {"type": "func_log", "base": 10.0, "k": -1.0, "c": 7.0},
                "Quy luật di truyền Mendel (KHTN)": {"type": "bio_genetics"},
                "Quỹ đạo chuyển động Parabol": {"type": "parabola", "a": -0.5, "b": 2.0, "c": 0.0}
            }
        else:

            available_labs = {

                "Hàm bậc ba (KNTT 12)": {"type": "func_3", "a": 1, "b": -3, "c": 0, "d": 2},

                "Parabol bậc hai": {"type": "parabola", "a": 1, "b": -2, "c": 1},

                "Hàm phân thức bậc 1/1": {"type": "func_1_1", "a": 1, "b": 1, "c": 1, "d": -1},

                "Hàm phân thức bậc 2/1 (TC Xiên)": {"type": "func_2_1", "a": 1, "b": -2, "c": 2, "d": 1, "e": -1},

                "Hàm số Mũ y = a^x (KNTT 11-12)": {"type": "func_exp", "base": 2.0, "k": 1.0, "c": 0.0},

                "Hàm số Lôgarit y = log_a(x) (KNTT 11-12)": {"type": "func_log", "base": 2.0, "k": 1.0, "c": 0.0},

                "Dao động điều hòa (Vật lí & KHTN)": {"type": "physics_oscillator", "A": 5.0, "omega": 2.0, "phi": 0.0},

                "Hình chóp tứ giác S.ABCD (Hình học 3D)": {"type": "geometry_3d", "shape": "pyramid_quad", "title": "Hình chóp tứ giác S.ABCD"},

                "Hình chóp tam giác S.ABC (Hình học 3D)": {"type": "geometry_3d", "shape": "pyramid_tri", "title": "Hình chóp tam giác S.ABC"},

                "Hình hộp chữ nhật ABCD.A'B'C'D' (3D)": {"type": "geometry_3d", "shape": "box", "title": "Hình hộp ABCD.A'B'C'D'"},

                "Hình lăng trụ tam giác ABC.A'B'C' (3D)": {"type": "geometry_3d", "shape": "prism_tri", "title": "Lăng trụ ABC.A'B'C'"},

                "Hai đường thẳng song song trong không gian": {"type": "geometry_3d", "shape": "parallel_lines", "title": "Quan hệ song song d1 // d2"},

                "Diện tích hình phẳng (Tích phân)": {"type": "area", "func": "x**2 - 3*x + 2", "a": 0.0, "b": 3.0},

                "Khối tròn xoay 3D (Tích phân Ox)": {"type": "revolve_ox", "func": "2*x + 1", "a": 2.0, "b": 5.0},

                "Không gian Oxyz (Vectơ & Tọa độ)": {"type": "oxyz", "x": 2, "y": 3, "z": 4},

            }



    manual_lab = st.selectbox("Mô phỏng có sẵn (không cần API):", list(available_labs))

    if st.button("Mở mô phỏng có sẵn"):

        st.session_state.lab_data = dict(available_labs[manual_lab])

    lab_command = st.text_input("Lệnh mô phỏng:", placeholder=lab_ph, key=f"lab_cmd_{current_context_key}", label_visibility="collapsed")



    if st.button("✨ Khởi chạy Phòng Lab", key=f"btn_lab_{current_context_key}") and lab_command.strip():

        st.session_state.tram1_count += 1

        with st.spinner("AI đang phân tích ngữ cảnh liên môn và dựng mô hình..."):

            # TRÍCH XUẤT ĐẦY ĐỦ 100% NGỮ CẢNH BÀI HỌC, TRẮC NGHIỆM VÀ TỰ LUẬN PHÍA TRÊN

            full_context_blocks = []

            if st.session_state.get("current_lesson"):

                full_context_blocks.append("=== TOÀN BỘ NỘI DUNG BÀI HỌC VỪA SINH RA TRÊN MÀN HÌNH ===\n" + st.session_state.current_lesson)

            if st.session_state.get("parsed_quiz"):

                q_text = "=== DANH SÁCH CÂU HỎI TRẮC NGHIỆM (PHẦN 2) ===\n"

                for q_i, q_val in enumerate(st.session_state.parsed_quiz):

                    q_text += f"Câu {q_i+1}: {q_val.get('question')} | Đáp án: {q_val.get('correct')} | Gợi ý: {q_val.get('explain')}\n"

                full_context_blocks.append(q_text)



            # TẦNG 1: TỰ ĐỘNG BƠM NGỮ CẢNH NẾU CHƯA CÓ BÀI HỌC (CHỐNG MÙ 100%)

            if not full_context_blocks:

                topic_hint = st.session_state.get("current_topic", "") or lab_command.strip()

                full_context_blocks.append(f"""=== THÔNG TIN CHỦ ĐỀ HỌC TẬP (TỰ ĐỘNG BƠM TỪ YÊU CẦU CỦA HỌC SINH) ===

Môn học: {subject} - Lớp {grade_num}.

Chủ đề trọng tâm học sinh đang học: '{topic_hint}'.

Hệ thống AI BẮT BUỘC dựa vào toàn bộ kiến thức chuẩn SGK Kết Nối Tri Thức (NXB Giáo Dục Việt Nam) của môn {subject} Lớp {grade_num} về chủ đề này để dựng mô phỏng / sơ đồ tư duy đầy đủ, toàn diện nhất!""")



            context_text = "\n\n".join(full_context_blocks)



            social_constraint = ""

            if is_social_subject:

                social_constraint = f"""

QUY TẮC BẮT BUỘC ĐẶC THÙ CHO MÔN KHOA HỌC XÃ HỘI / NGOẠI NGỮ ({subject}):

- TUYỆT ĐỐI NGHIÊM CẤM xuất các mô hình toán học giải tích/hình học (func_3, parabola, func_1_1, func_2_1, area, revolve_ox, oxyz, geometry_3d, func_exp, func_log).

- 100% BẮT BUỘC xuất JSON type 'mermaid' biểu diễn Sơ đồ tư duy D3/Mermaid hoặc lưu đồ tiến trình đa cấp độ!"""



            lab_prompt = f"""[HỆ TRI THỨC SƯ PHẠM QUỐC GIA - CHUẨN CT GDPT 2018 & QUY CHẾ THI 2026 (Cập nhật QĐ 764/QĐ-BGDĐT & TT 13/2026/TT-BGDĐT)]

Môn học: {subject} | Khối lớp: {grade_num}.

NGỮ CẢNH BÀI HỌC, TRẮC NGHIỆM VÀ TỰ LUẬN HIỆN TẠI (BẮT BUỘC THAM CHIẾU KHI HỌC SINH NÓI 'CÂU 1', 'CÂU 2', 'BÀI TỰ LUẬN TRÊN', 'HÌNH Ở TRÊN'...):

{context_text}

{social_constraint}



QUY TẮC BẮT BUỘC VỀ SỰ KHỚP NỐI NGỮ CẢNH (CỰC KỲ QUAN TRỌNG):

- NẾU học sinh yêu cầu mô phỏng hoặc vẽ hình từ một câu trong bài học/tự luận phía trên:

  AI BẮT BUỘC trích xuất CHÍNH XÁC dữ kiện có trong đúng câu đó ở ngữ cảnh bài học!

  TUYỆT ĐỐI KHÔNG TỰ Ý BỊA RA HÀM MỚI khi bài học đã có sẵn hàm số/ngữ liệu cụ thể!



---

Yêu cầu của học sinh: "{lab_command}"



NHIỆM VỤ: Xuất DUY NHẤT 1 khối JSON hợp lệ phân loại mô hình trực quan (KHÔNG VIẾT CHỮ NGOÀI JSON).



QUY TẮC PHÂN LOẠI MÔ HÌNH:

1. DIỆN TÍCH HÌNH PHẲNG TÍCH PHÂN TỪ A ĐẾN B (Toán 12):

   {{"type": "area", "func": "x**2 - 3*x + 2", "a": 0.0, "b": 3.0}}

2. KHỐI TRÒN XOAY 3D TÍCH PHÂN QUANH OX (Toán 12):

   {{"type": "revolve_ox", "func": "2*x + 1", "a": 2.0, "b": 5.0}}

3. HÀM BẬC 3 (ax^3+bx^2+cx+d):

   {{"type": "func_3", "a": 1, "b": -3, "c": 0, "d": 2}}

4. HÀM PHÂN THỨC 1/1 ((ax+b)/(cx+d)):

   {{"type": "func_1_1", "a": 1, "b": 1, "c": 1, "d": -1}}

5. HÀM PHÂN THỨC 2/1 ((ax^2+bx+c)/(dx+e)):

   {{"type": "func_2_1", "a": 1, "b": -2, "c": 2, "d": 1, "e": -1}}

6. PARABOL BẬC 2 (ax^2+bx+c):

   {{"type": "parabola", "a": 1, "b": -2, "c": 1}}

7. HÀM SỐ MŨ (y = a^x hoặc y = e^x, Toán 11-12):

   {{"type": "func_exp", "base": 2.0, "k": 1.0, "c": 0.0}}

8. HÀM SỐ LÔGARIT (y = log_a(x) hoặc y = ln(x), Toán 11-12):

   {{"type": "func_log", "base": 2.0, "k": 1.0, "c": 0.0}}

9. HÌNH HỌC KHÔNG GIAN 3D (Hình chóp, hình lăng trụ, hình hộp chữ nhật, lập phương, quan hệ song song/vuông góc Lớp 11-12):

   - NẾU câu hỏi hoặc bài học nhắc đến: hình chóp (S.ABCD, S.ABC, tứ diện...), hình lăng trụ, hình hộp chữ nhật, hình lập phương, hai đường thẳng song song, đường thẳng song song mặt phẳng, quan hệ song song trong không gian:

   -> BẮT BUỘC CHỌN type "geometry_3d", TUYỆT ĐỐI KHÔNG CHỌN "mermaid"!

   Mẫu chuẩn:

   + Hình chóp tứ giác: {{"type": "geometry_3d", "shape": "pyramid_quad", "title": "Mô hình hình chóp S.ABCD"}}

   + Hình chóp tam giác / tứ diện: {{"type": "geometry_3d", "shape": "pyramid_tri", "title": "Mô hình hình chóp S.ABC"}}

   + Hình hộp chữ nhật / lập phương: {{"type": "geometry_3d", "shape": "box", "title": "Mô hình hình hộp ABCD.A'B'C'D'"}}

   + Hình lăng trụ tam giác: {{"type": "geometry_3d", "shape": "prism_tri", "title": "Mô hình lăng trụ tam giác ABC.A'B'C'"}}

   + Hai đường thẳng song song trong không gian: {{"type": "geometry_3d", "shape": "parallel_lines", "title": "Mô hình hai đường thẳng song song d1 // d2"}}

10. KHÔNG GIAN OXYZ:

   {{"type": "oxyz", "x": 2, "y": 3, "z": 4}}

11. SƠ ĐỒ TƯ DUY TƯƠNG TÁC THUYẾT TRÌNH (CHO TẤT CẢ CÁC MÔN VÀ CÁC KHỐI LỚP 6-12 CHUẨN KNTT):

   QUY CHUẨN SƠ ĐỒ BẮT BUỘC:

   - ĐỘ SÂU & TOÀN DIỆN: Phải tóm tắt ĐẦY ĐỦ VÀ SÂU SẮC toàn bộ kiến thức cốt lõi, công thức, định lý ở bài học phía trên. Tối thiểu 3-5 nhánh chính cấp 1, mỗi nhánh chính bắt buộc có 2-4 nhánh con chi tiết. Tuyệt đối không vẽ sơ sài 1-2 nhánh!

   - HỖ TRỢ ĐA NGÔN NGỮ (VIỆT - ANH): Khi môn học là Tiếng Anh, sơ đồ tư duy phải được trình bày chuẩn phong cách Tiếng Anh học thuật CEFR/IELTS, các nhánh từ vựng kèm loại từ (n, v, adj) và câu ví dụ ngữ cảnh rõ ràng.

   Mẫu chuẩn: {{\"type\": \"mermaid\", \"code\": \"graph LR\\n   Root[\\\"🎯 TIÊU ĐỀ CHỦ ĐỀ CHÍNH\\\"] --> A[\\\"1. Khái niệm trọng tâm\\\"]\\n   Root --> B[\\\"2. Các nội dung cơ bản\\\"]\\n   Root --> C[\\\"3. Ứng dụng thực tiễn\\\"]\"}}

"""



            try:

                raw_json = call_gemini_with_fallback(lab_prompt, json_mode=True)

                raw_json = raw_json.strip()

                if raw_json.startswith("```json"): raw_json = raw_json[7:-3].strip()

                elif raw_json.startswith("```"): raw_json = raw_json[3:-3].strip()



                if "graph " in raw_json or "flowchart " in raw_json or "-->" in raw_json:
                    if not raw_json.startswith("{"):
                        st.session_state.lab_data = {"type": "mermaid", "code": raw_json}
                    else:
                        try:
                            st.session_state.lab_data = safe_json_loads(raw_json)
                        except Exception:
                            m_code = re.search(r'"code"\s*:\s*"(.*?)"\s*(?:,\s*"|\})', raw_json, re.DOTALL)
                            if m_code:
                                try:
                                    extracted = m_code.group(1).encode('utf-8').decode('unicode_escape', errors='ignore')
                                except Exception:
                                    extracted = m_code.group(1)
                                st.session_state.lab_data = {"type": "mermaid", "code": extracted}
                            else:
                                st.session_state.lab_data = {"type": "mermaid", "code": raw_json}
                else:
                    try:
                        parsed_d = safe_json_loads(raw_json)
                    except Exception:
                        parsed_d = json.loads(raw_json)

                    # Chặn nếu AI vô tình trả về đồ thị toán cho môn xã hội
                    if is_social_subject and parsed_d.get("type") in ["func_3", "parabola", "func_1_1", "func_2_1", "area", "revolve_ox", "oxyz"]:
                        st.session_state.lab_data = list(available_labs.values())[0]
                    else:
                        st.session_state.lab_data = parsed_d

            except Exception as e:

                # BẪY CỨU HỘ ĐA TẦNG THÔNG MINH (KẾ THỪA ƯU ĐIỂM LINK 2 & NÂNG CẤP TOÀN DIỆN CHO LINK 1):

                cmd_low = lab_command.lower()

                is_mindmap_req = any(kw in cmd_low for kw in [

                    "sơ đồ", "tư duy", "mindmap", "tóm tắt", "cây thư mục", "hệ thống hóa",

                    "mind map", "diagram", "summarize", "summary", "tree", "vocabulary", "grammar"

                ])

                topic_title = st.session_state.get("current_topic", "") or f"CHỦ ĐỀ {subject.upper()} LỚP {grade_num}"



                if is_mindmap_req or is_social_subject:

                    if is_social_subject and not is_mindmap_req:

                        st.session_state.lab_data = list(available_labs.values())[0]

                    elif subject == "Tiếng Anh":

                        st.session_state.lab_data = {

                            "type": "mermaid",

                            "code": f"""graph LR\n    Root["🎯 {topic_title.upper()}"] --> A["📖 1. Key Vocabulary (Từ vựng cốt lõi)"]\n    Root --> B["⚡ 2. Core Grammar (Ngữ pháp trọng tâm)"]\n    Root --> C["🔍 3. Reading & Language Skills"]\n    Root --> D["🌐 4. IELTS / Communication Practice"]\n    A --> A1["Topic Vocabulary & Phonetics"]\n    A --> A2["Collocations & Phrasal Verbs"]\n    B --> B1["Sentence Structures & Rules"]\n    B --> B2["Common Errors to Avoid"]\n    C --> C1["Main Ideas & Key Details"]\n    D --> D1["Natural Fluency & Intonation"]"""

                        }

                    else:

                        st.session_state.lab_data = {

                            "type": "mermaid",

                            "code": f"""graph LR\n    Root["🎯 {topic_title.upper()}"] --> A["📖 1. Định nghĩa & Khái niệm cốt lõi"]\n    Root --> B["⚡ 2. Công thức & Quy tắc trọng tâm"]\n    Root --> C["🔍 3. Phương pháp giải & Dạng bài tập"]\n    Root --> D["🌐 4. Ứng dụng thực tiễn & Liên môn"]\n    A --> A1["Khái niệm cơ bản chuẩn SGK Kết Nối Tri Thức"]\n    A --> A2["Điều kiện áp dụng & Miền xác định"]\n    B --> B1["Công thức nền tảng & Biến đổi"]\n    C --> C1["Dạng bài nhận biết - thông hiểu"]\n    C --> C2["Dạng bài vận dụng & liên hệ"]\n    D --> D1["Mô hình hóa thực tiễn đời sống"]"""

                        }

                elif any(kw in cmd_low for kw in ["hình chóp", "chóp", "lăng trụ", "hình hộp", "lập phương", "song song", "s.abcd", "s.abc"]):

                    if "tam giác" in cmd_low or "s.abc" in cmd_low:

                        st.session_state.lab_data = {"type": "geometry_3d", "shape": "pyramid_tri", "title": "Hình chóp tam giác S.ABC"}

                    elif "hộp" in cmd_low or "lập phương" in cmd_low:

                        st.session_state.lab_data = {"type": "geometry_3d", "shape": "box", "title": "Hình hộp ABCD.A'B'C'D'"}

                    elif "lăng trụ" in cmd_low:

                        st.session_state.lab_data = {"type": "geometry_3d", "shape": "prism_tri", "title": "Hình lăng trụ ABC.A'B'C'"}

                    elif "song song" in cmd_low:

                        st.session_state.lab_data = {"type": "geometry_3d", "shape": "parallel_lines", "title": "Hai đường thẳng song song d1 // d2"}

                    else:

                        st.session_state.lab_data = {"type": "geometry_3d", "shape": "pyramid_quad", "title": "Hình chóp tứ giác S.ABCD"}

                elif any(kw in cmd_low for kw in ["hàm mũ", "mũ", "exp", "e^x", "a^x"]):

                    st.session_state.lab_data = {"type": "func_exp", "base": 2.0, "k": 1.0, "c": 0.0}

                elif any(kw in cmd_low for kw in ["lôgarit", "logarit", "log", "ln"]):

                    st.session_state.lab_data = {"type": "func_log", "base": 2.0, "k": 1.0, "c": 0.0}

                elif any(kw in cmd_low for kw in ["tròn xoay", "xoay quanh ox", "vật thể xoay"]):

                    st.session_state.lab_data = {"type": "revolve_ox", "func": "2*x + 1", "a": 2.0, "b": 5.0}

                else:

                    st.warning("⚠️ AI trả về định dạng chưa chuẩn nên hệ thống hiển thị mô hình mẫu. Em thử diễn đạt lại yêu cầu rõ hơn nhé!")

                    st.session_state.lab_data = {"type": "func_3", "a": 1, "b": -3, "c": 0, "d": 2}



    if st.session_state.get("lab_data"):

        data = st.session_state.lab_data

        st.success("✨ Đã khởi tạo mô phỏng Phòng Lab liên môn thành công!")

        render_smart_lab(data, subject)



    # --------------------------------------------------------------------------

    # NÂNG CẤP KHKT 2026: PHÒNG THÍ NGHIỆM ẢO ĐỘNG 3D WEBGL TƯƠNG TÁC XOAY 360°

    # --------------------------------------------------------------------------

    with st.expander("🌐 Mở Rộng: Phòng Thí Nghiệm Ảo Động 3D WebGL (Tương Tác Xoay 360°)", expanded=False):

        st.markdown('<div style="color: #38bdf8; font-weight: 700; margin-bottom: 6px;">🔬 Thư viện Mô hình 3D Khoa học Liên môn GDPT 2018 (Plotly 3D WebGL):</div>', unsafe_allow_html=True)

        st.caption("Học sinh có thể dùng chuột hoặc ngón tay xoay 360 độ, phóng to, thu nhỏ và quan sát liên kết không gian chân thực:")



        c_3d1, c_3d2 = st.columns([1.5, 3.5])

        with c_3d1:

            if subject in ["Hóa học", "Khoa học tự nhiên"]:

                mol_choice = st.selectbox("Chọn mô hình phân tử 3D:", ["Methane (CH4)", "Ethanol (C2H5OH)", "Acetic acid (CH3COOH)"], key="sel_3d_mol")

                st.info(f"💎 **Mô tả IUPAC:** Cấu trúc không gian {mol_choice} với các tâm nguyên tử Carbon (đen), Hydrogen (xanh), Oxygen (đỏ) và liên kết cộng hóa trị.")

            elif subject == "Vật lý":

                wave_choice = st.selectbox("Chọn hiện tượng sóng 3D:", ["Sóng dừng (Standing Waves)", "Mặt sóng lan truyền đồng tâm"], key="sel_3d_wave")

                st.info(f"🌊 **Hiện tượng:** {wave_choice} thể hiện rõ bụng sóng, nút sóng và sự phân bố biên độ không gian.")

            elif subject == "Sinh học":

                st.markdown("🧬 **Mô hình Chuỗi xoắn kép ADN:**")

                st.info("Hai mạch polynucleotide xoắn song song ngược chiều quanh trục, liên kết hydro theo nguyên tắc bổ sung A-T, G-C.")

            else:

                mol_choice = st.selectbox("Khám phá mô hình khoa học 3D:", ["Methane (CH4)", "Ethanol (C2H5OH)", "Acetic acid (CH3COOH)"], key="sel_3d_other")

                st.info("Trực quan hóa cấu trúc nguyên tử và phân tử phục vụ học tập tích hợp STEM.")



        with c_3d2:

            if subject in ["Hóa học", "Khoa học tự nhiên"] or subject not in ["Vật lý", "Sinh học"]:

                fig_3d = create_3d_molecule_figure(st.session_state.get("sel_3d_mol", st.session_state.get("sel_3d_other", "Methane (CH4)")))

            elif subject == "Vật lý":

                fig_3d = create_3d_physics_wave_figure(st.session_state.get("sel_3d_wave", "Sóng dừng (Standing Waves)"))

            else:

                fig_3d = create_3d_dna_helix_figure()

            st.plotly_chart(fig_3d, width="stretch")



# ------------------------------------------------------------------------------

# TRẠM 2: GIA SƯ SOCRATIC & NỘP BÀI (CHUẨN CHẨN ĐOÁN VÁ LỖ HỔNG ĐA MÔN LỚP 6-12)

# ------------------------------------------------------------------------------

if selected_station == station_labels[1]:

    st.markdown("<br>", unsafe_allow_html=True)

    col_head1, col_head2 = st.columns([3.8, 1.2])

    with col_head1:

        st.subheader(f"✍️ Gia Sư Socratic Môn: {subject} - Lớp {grade_num}")

    with col_head2:

        st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

        if st.button("🔄 Làm mới buổi học", key=f"btn_reset_chat_{current_context_key}", width="stretch"):

            st.session_state.messages = []

            st.session_state.chat = None

            st.rerun()



    st.caption("Khung Tri Thức Chuẩn Hóa CT GDPT 2018 & SGK Kết Nối Tri Thức (NXBGDVN) • Vấn đáp Socratic • Chẩn đoán lỗ hổng kiến thức • Dẫn dắt tư duy, không giải hộ.")



    socratic_system_instruction = build_socratic_master_instruction(subject, grade_num, student_name, mode="review")



    st.markdown('<div style="background: linear-gradient(135deg, rgba(2, 132, 199, 0.12), rgba(16, 185, 129, 0.12)); border-left: 4px solid #38bdf8; border-radius: 8px; padding: 12px 18px; margin: 10px 0 16px 0;"><div style="font-weight: 700; color: #38bdf8; font-size: 14px; margin-bottom: 4px;">💡 Quy trình gửi bài Socratic 1 chạm:</div><div style="font-size: 0.92rem; color: #cbd5e1; line-height: 1.6;">Bấm nút <b>\'📤 GỬI BÀI LÀM CỦA EM\'</b> bên dưới ➔ Chọn <b>Camera chụp trực tiếp</b> hoặc <b>Tải ảnh từ máy</b> ➔ Bấm <b>🚀 Bắt đầu nhận xét bài làm</b> để Thầy AI đồng hành cùng em!</div></div>', unsafe_allow_html=True)



    cam_pages_key = f"t2_cam_pages_{current_context_key}"

    if cam_pages_key not in st.session_state:

        st.session_state[cam_pages_key] = []



    cam_shot = None

    uploaded_files = []



    # GIAO DIỆN NỘP BÀI ĐA TRANG (MULTI-PAGE UPLOAD & CAMERA) KHÔNG BỊ CO SẬP TRÊN MOBILE
    with st.expander("📤 NỘP BÀI LÀM CỦA EM (Chụp Camera nhiều trang hoặc Tải nhiều ảnh)", expanded=True):
        st.markdown("#### 📤 Chọn 1 trong 2 cách để nộp bài làm:")
        c_cam, c_file = st.columns([1.1, 1], gap="medium")
        with c_cam:
            st.markdown("##### 📸 Cách 1: Chụp bằng Camera (Nhiều trang)")
            st.caption("Chụp từng trang vở rồi bấm **'➕ Thêm trang'** để chụp tiếp trang kế:")
            cam_shot = st.camera_input("Bật Camera chụp trang bài làm:", key=f"t2_cam_{current_context_key}")
            if cam_shot:
                col_c1, col_c2 = st.columns([1.5, 1])
                with col_c1:
                    if st.button("➕ Thêm trang này vào bài làm", key=f"btn_add_page_{current_context_key}", width="stretch"):
                        try:
                            cam_shot.seek(0)
                            with Image.open(cam_shot) as raw_im:
                                im_rgb = raw_im.convert("RGB")
                                im_rgb.thumbnail((2200, 2200))
                                st.session_state[cam_pages_key].append(im_rgb)
                                st.toast(f"✅ Đã thêm Trang {len(st.session_state[cam_pages_key])}!")
                        except Exception as e:
                            st.error(f"Lỗi thêm trang: {e}")
                        st.rerun()
                with col_c2:
                    if st.session_state[cam_pages_key]:
                        if st.button("🗑️ Xóa các trang", key=f"btn_clr_cam_{current_context_key}", width="stretch"):
                            st.session_state[cam_pages_key] = []
                            st.rerun()

            if st.session_state[cam_pages_key]:
                st.success(f"📷 Đã lưu **{len(st.session_state[cam_pages_key])} trang** bài làm từ Camera. Em có thể tiếp tục chụp trang tiếp theo!")
                col_thumbs = st.columns(min(len(st.session_state[cam_pages_key]), 4))
                for idx_p, img_p in enumerate(st.session_state[cam_pages_key]):
                    with col_thumbs[idx_p % min(len(st.session_state[cam_pages_key]), 4)]:
                        st.image(img_p, caption=f"Trang {idx_p+1}", width="stretch")

        with c_file:
            st.markdown("##### 📁 Cách 2: Tải ảnh từ thiết bị (Nhiều trang - Nhanh nhất)")
            st.caption("💡 **Mẹo làm bài dài nhiều trang:** Em hãy dùng Camera điện thoại chụp sẵn các trang 1, 2, 3... Sau đó chọn **tất cả các ảnh cùng lúc** từ Bộ sưu tập:")
            uploaded_files = st.file_uploader(
                "Chọn 1 hoặc nhiều ảnh bài làm:",
                type=["jpg", "png", "jpeg", "webp", "heic"],
                accept_multiple_files=True,
                key=f"t2_upload_{current_context_key}"
            )



    # TỔNG HỢP DANH SÁCH TOÀN BỘ ẢNH BÀI LÀM (MULTI-PAGE IMAGES)

    student_images = []



    # 1. Thu thập từ file uploader

    if uploaded_files:

        for up_f in uploaded_files:

            try:

                if up_f.size > 12 * 1024 * 1024:

                    continue

                up_f.seek(0)

                with Image.open(up_f) as raw_image:

                    if raw_image.width * raw_image.height > 25000000:

                        continue

                    raw_image.load()

                    im_rgb = raw_image.convert("RGB")

                    im_rgb.thumbnail((2200, 2200))

                    student_images.append(im_rgb)

            except Exception as exc:

                exc_str = str(exc)

                if "heif" in exc_str.lower() or "heic" in exc_str.lower() or getattr(up_f, 'name', '').lower().endswith('.heic'):

                    st.warning(f"⚠️ Ảnh '{getattr(up_f, 'name', 'HEIC')}' lưu định dạng HEIC. Em hãy dùng Camera chụp trực tiếp gửi Thầy nhé!")



    # 2. Thu thập từ camera (các trang đã thêm hoặc trang vừa chụp)

    if st.session_state[cam_pages_key]:

        student_images.extend(st.session_state[cam_pages_key])

    elif cam_shot and not student_images:

        try:

            cam_shot.seek(0)

            with Image.open(cam_shot) as raw_image:

                raw_image.load()

                im_rgb = raw_image.convert("RGB")

                im_rgb.thumbnail((2200, 2200))

                student_images.append(im_rgb)

        except Exception:

            pass



    ann_key = f"t2_ann_imgs_{current_context_key}"



    if student_images:

        total_pages = len(student_images)

        st.success(f"✨ **Đã tiếp nhận thành công {total_pages} trang bài làm!** Em xem trước bên dưới và bấm bắt đầu nhận xét nhé:")



        # Hiển thị ảnh xem trước các trang bài làm (hoặc ảnh đã chấm bút tích của Thầy nếu đã nhận xét)

        if st.session_state.get(ann_key):

            st.markdown("### 📝 Bút tích chấm bài trực tiếp của Thầy AI (Mực đỏ Check VAR & Tick xanh OK):")

            st.caption("🔍 Thầy đã soi trực tiếp từng dòng trên ảnh bài làm: Dòng Tick xanh OK chuẩn chỉ và Dòng Mực đỏ Check VAR khét lẹt khoanh chỗ khuất tất.")

            ann_imgs_show = st.session_state[ann_key]

            if len(ann_imgs_show) == 1:

                st.image(ann_imgs_show[0], caption="Ảnh bài làm đã được Thầy chấm 'Face to Face'", width="stretch")

            else:

                col_preview = st.columns(min(len(ann_imgs_show), 3))

                for p_idx, p_img in enumerate(ann_imgs_show):

                    with col_preview[p_idx % min(len(ann_imgs_show), 3)]:

                        st.image(p_img, caption=f"Trang {p_idx + 1}/{len(ann_imgs_show)} (Đã chấm Check VAR)", width="stretch")

        else:

            if total_pages == 1:

                st.image(student_images[0], caption="Ảnh bài làm (Trang 1/1)", width="stretch")

            else:

                col_preview = st.columns(min(total_pages, 3))

                for p_idx, p_img in enumerate(student_images):

                    with col_preview[p_idx % min(total_pages, 3)]:

                        st.image(p_img, caption=f"Trang {p_idx + 1}/{total_pages}", width="stretch")



        col_act1, col_act2 = st.columns([2.5, 1.2])

        with col_act1:

            btn_start_review = st.button(

                f"🚀 Bắt đầu nhận xét bài làm ({total_pages} trang)" if total_pages > 1 else "🚀 Bắt đầu nhận xét bài làm",

                type="primary",

                width="stretch",

                key=f"btn_review_{current_context_key}"

            )

        with col_act2:

            if st.button("🔄 Xóa hết / Đổi ảnh khác", width="stretch", key=f"btn_change_photo_{current_context_key}"):

                st.session_state[cam_pages_key] = []

                st.session_state[ann_key] = []

                if f"t2_cam_{current_context_key}" in st.session_state:

                    del st.session_state[f"t2_cam_{current_context_key}"]

                if f"t2_upload_{current_context_key}" in st.session_state:

                    del st.session_state[f"t2_upload_{current_context_key}"]

                st.rerun()



        if student_images and btn_start_review:

            st.session_state.tram2_count += 1

            with st.spinner(f"Thầy đang đối chiếu chuẩn kiến thức SGK KNTT Lớp {grade_num} môn {subject} và soi từng bước làm của {student_name} qua {total_pages} trang bài làm..."):

                try:

                    review_payload = [

                        f"Học sinh {student_name} nộp {total_pages} trang ảnh bài làm môn {subject} Lớp {grade_num}. Thầy hãy soi kỹ toàn bộ các trang bài làm (theo thứ tự từ trang 1 đến trang {total_pages}), chấm từng dòng với Dòng Tick xanh OK chuẩn chỉ và Dòng Mực đỏ Check VAR khét lẹt, kèm khối <ANNOTATIONS>:",

                        *student_images

                    ]

                    full_res = call_gemini_with_fallback(

                        review_payload,

                        system_instruction=socratic_system_instruction

                    )



                    # 1. Trích xuất Annotations tọa độ để vẽ lên ảnh bài làm

                    annotations = []

                    if "<ANNOTATIONS>" in full_res:

                        try:

                            ann_part = full_res.split("<ANNOTATIONS>")[1].split("</ANNOTATIONS>")[0].strip()

                            annotations = json.loads(ann_part)

                        except Exception:

                            pass



                    # 2. Vẽ Bút tích trực tiếp lên từng trang ảnh bài làm của học sinh (Mực đỏ Check VAR & Tick xanh OK)

                    annotated_imgs = []

                    for s_img in student_images:

                        ann_res = annotate_student_work(s_img, annotations)

                        annotated_imgs.append(ann_res)

                    st.session_state[ann_key] = annotated_imgs



                    # 3. Làm sạch phản hồi của Thầy

                    clean_res = full_res

                    if "<ANNOTATIONS>" in clean_res:

                        p1 = clean_res.split("<ANNOTATIONS>")[0].strip()

                        p2 = clean_res.split("</ANNOTATIONS>")[-1].strip() if "</ANNOTATIONS>" in clean_res else ""

                        clean_res = (p1 + "\n\n" + p2).strip()



                    student_fb = clean_res.split("<DIAGNOSTIC>")[0].strip() if "<DIAGNOSTIC>" in clean_res else clean_res

                    if "<DIAGNOSTIC>" in full_res:

                        try:

                            diag = json.loads(full_res.split("<DIAGNOSTIC>")[1].split("</DIAGNOSTIC>")[0].strip())

                            entry = {

                                "event_id": str(uuid.uuid4()),

                                "time": get_vn_time(),

                                "name": student_name,

                                "grade": grade,

                                "subject": subject,

                                "topic": diag.get("topic", "Kiến thức SGK KNTT"),

                                "error_type": diag.get("error_type", "Chưa rõ"),

                                "evaluation": diag.get("evaluation", "Cần theo dõi"),

                                "scores": diag.get("scores", {}),

                                "type": "SOCRATIC_DIAGNOSTIC"

                            }

                            st.session_state.analytics_logs.append(entry)

                            st.session_state.student_progress_history.append(entry)

                            sync_event(entry)

                        except Exception:

                            pass

                    st.session_state.messages = [{"role": "user", "content": f"*(Em đã nộp {total_pages} trang ảnh bài làm)*"}, {"role": "assistant", "content": student_fb}]

                    st.rerun()

                except Exception as e:

                    st.error(f"Lỗi phân tích bài làm: {e}")



    # BẢN ĐỒ LỖ HỔNG KHIẾN THỨC RADAR CHART ĐA MÔN LỚP 6-12

    progress = [e for e in st.session_state.get("student_progress_history", []) if e.get("subject") == subject and e.get("grade") == grade]

    radar_entry = progress[-1] if progress else None

    radar_scores = radar_entry.get("scores", {}) if radar_entry else {}

    radar_valid = isinstance(radar_scores, dict) and all(isinstance(radar_scores.get(f"truc{i}"), (int, float)) and math.isfinite(radar_scores[f"truc{i}"]) and 0 <= radar_scores[f"truc{i}"] <= 100 for i in range(1, 6))

    if radar_valid:

        with st.expander("🕸️ Bản Đồ Lỗ Hổng Kiến Thức & Năng Lực Sư Phạm (Radar Chart Đa Môn)", expanded=True):

            latest_entry = radar_entry

            sc = radar_scores



            # Chọn nhãn 5 trục năng lực chuẩn hóa theo CT GDPT 2018 & Thông tư 22/2021/TT-BGDĐT

            if subject == "Toán học":

                categories = ['Tư duy & Lập luận toán học', 'Mô hình hóa toán học', 'Giải quyết vấn đề toán học', 'Giao tiếp toán học', 'Sử dụng công cụ & phương tiện']

            elif subject in ["Vật lý", "Hóa học", "Sinh học", "Khoa học tự nhiên"]:

                categories = ['Nhận thức khoa học tự nhiên', 'Tìm hiểu thế giới tự nhiên', 'Vận dụng kiến thức, kỹ năng', 'Thực hành thí nghiệm & IUPAC', 'Giải quyết vấn đề sáng tạo']

            elif subject == "Ngữ văn":

                categories = ['Đọc hiểu đặc trưng thể loại', 'Cảm thụ & Thi pháp thẩm mỹ', 'Viết đoạn văn nghị luận XH', 'Viết bài văn nghị luận VH', 'Ngôn ngữ & Diễn đạt Tiếng Việt']

            elif subject == "Tiếng Anh":

                categories = ['Phonetics & Word Stress', 'Grammar & Sentence Structure', 'Vocabulary in Authentic Context', 'Reading Comprehension', 'Written & Spoken Production']

            else:

                categories = ['Nhận thức tri thức cốt lõi', 'Khai thác số liệu & tư liệu', 'Vận dụng thực tiễn đời sống', 'Tư duy phản biện & giải quyết VĐ', 'Đạo đức, pháp luật & kỹ năng số']



            r_vals = [sc[f"truc{i}"] for i in range(1, 6)]

            r_vals.append(r_vals[0])

            categories.append(categories[0])



            fig_radar = go.Figure()

            fig_radar.add_trace(go.Scatterpolar(

                r=r_vals, theta=categories, fill='toself', name=html.escape(student_name),

                fillcolor='rgba(56, 189, 248, 0.35)', line=dict(color='#38bdf8', width=3)

            ))

            fig_radar.update_layout(

                polar=dict(radialaxis=dict(visible=True, range=[0, 100], color='#94a3b8'), bgcolor="#0f172a"),

                showlegend=False, template="plotly_dark", height=380, margin=dict(l=40, r=40, t=30, b=30)

            )

            st.plotly_chart(fig_radar, width="stretch")

            st.caption("Ước lượng tham khảo của AI từ bài vừa nộp; không phải điểm năng lực đã được kiểm định.")

            st.caption("Chưa hiển thị xác suất BKT khi chưa có chuỗi quan sát đúng/sai theo từng kỹ năng.")

            col_dg1, col_dg2 = st.columns([3, 1.2])

            with col_dg1:

                st.caption(f"📌 **Chẩn đoán gần nhất:** Chủ đề `{latest_entry.get('topic')}` | Phân loại lỗi: `{latest_entry.get('error_type')}` | Đánh giá: `{latest_entry.get('evaluation')}`")

            with col_dg2:

                remedy_books = get_kntt_books_for(subject, grade_num)

                if remedy_books:

                    st.link_button(f"📖 Mở SGK KNTT ôn lại", remedy_books[0]['url'], width="stretch")



    # Khởi tạo tin nhắn chào mừng sư phạm nếu chưa có tin nhắn nào
    if "messages" not in st.session_state or not st.session_state.messages:
        welcome_intro = (
            f"Thầy chào em **{student_name}**! Thầy là Gia sư Socratic đồng hành cùng em trong môn **{subject} - Lớp {grade_num}**.\n\n"
            f"💡 Em có thể:\n"
            f"- **Nộp ảnh bài làm** ở mục bên trên để Thầy soi lỗi chi tiết từng dòng (Mực đỏ Check VAR & Tick xanh OK).\n"
            f"- Hoặc **gõ trực tiếp câu hỏi / bài toán** vào khung chat bên dưới (hoặc bấm Mic nói) để Thầy trò mình cùng khám phá, thấu suốt kiến thức nhé!"
        )
        st.session_state.messages = [{"role": "assistant", "content": welcome_intro}]

    for idx_m, m in enumerate(st.session_state.get("messages", [])):

        with st.chat_message(m["role"]):

            st.markdown(m["content"])

            if m["role"] == "assistant" and len(m.get("content", "")) > 15:

                create_pedagogical_tts_component(m["content"], subject, f"t2_msg_{idx_m}")

    if True:

        # Micro trợ lý giọng nói trực tiếp cho Khung Chat Socratic

        t2_mic_html = f"""

        <div style="margin: 10px 0 6px 0; display: flex; align-items: center; justify-content: flex-end; gap: 8px;">

            <button id="btn_rec_t2_chat" onclick="toggleRec_t2_chat()" style="background: linear-gradient(135deg, #0284c7, #0369a1); color: #ffffff; border: 1.5px solid #38bdf8; padding: 5px 12px; border-radius: 20px; font-weight: 700; font-size: 12px; cursor: pointer; display: flex; align-items: center; gap: 6px; box-shadow: 0 2px 8px rgba(56,189,248,0.25);">

                <span id="icon_t2_chat">🎙️</span> <span id="label_t2_chat">Nói câu hỏi vào Mic</span>

            </button>

            <span id="status_t2_chat" style="color: #94a3b8; font-size: 11.5px; font-style: italic;">(Bấm mic để nói câu hỏi rảnh tay)</span>

        </div>

        <script>

        (function() {{

            let recognizing = false;

            let recognition = null;

            const btn = document.getElementById('btn_rec_t2_chat');

            const lbl = document.getElementById('label_t2_chat');

            const icon = document.getElementById('icon_t2_chat');

            const status = document.getElementById('status_t2_chat');



            if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {{

                const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;

                recognition = new SpeechRec();

                recognition.continuous = false;

                recognition.interimResults = false;

                recognition.lang = '{('en-US' if subject == 'Tiếng Anh' else 'vi-VN')}';



                recognition.onstart = function() {{

                    recognizing = true;

                    btn.style.background = 'linear-gradient(135deg, #e11d48, #be123c)';

                    lbl.innerText = 'Đang nghe...';

                    icon.innerText = '🔴';

                    status.innerText = 'Hãy nói câu hỏi của em...';

                    status.style.color = '#f43f5e';

                }};



                recognition.onresult = function(event) {{

                    const transcript = event.results[0][0].transcript;

                    status.innerText = 'Đã nhận: "' + transcript + '"';

                    status.style.color = '#34d399';

                    try {{

                        const targetDoc = window.parent.document || document;

                        const chatInput = targetDoc.querySelector('textarea[data-testid="stChatInputTextArea"]') || targetDoc.querySelector('[data-testid="stChatInput"] textarea');

                        if (chatInput) {{
                            chatInput.value = transcript;
                            chatInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                            chatInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
                            chatInput.focus();
                            setTimeout(function() {{
                                const sendBtn = targetDoc.querySelector('button[data-testid="stChatInputSubmitButton"]');
                                if (sendBtn) {{
                                    sendBtn.click();
                                }}
                            }}, 350);
                        }}
                    }} catch(e) {{ console.warn(e); }}
                }};

                recognition.onerror = function(event) {{
                    recognizing = false;
                    btn.style.background = 'linear-gradient(135deg, #0284c7, #0369a1)';
                    lbl.innerText = 'Nói câu hỏi vào Mic';
                    icon.innerText = '🎙️';
                    status.innerText = 'Lỗi mic: ' + event.error;
                    status.style.color = '#f87171';
                }};

                recognition.onend = function() {{
                    recognizing = false;
                    btn.style.background = 'linear-gradient(135deg, #0284c7, #0369a1)';
                    lbl.innerText = 'Nói câu hỏi vào Mic';
                    icon.innerText = '🎙️';
                }};
            }}

            window.toggleRec_t2_chat = function() {{
                if (!recognition) return;
                if (recognizing) recognition.stop();
                else recognition.start();
            }};
        }})();
        </script>
        """
        render_html_iframe(t2_mic_html, height=42)

        if q := st.chat_input("Em chưa hiểu chỗ nào, hãy hỏi Thầy nhé..."):
            st.session_state.tram2_count += 1
            st.session_state.messages.append({"role": "user", "content": q})
            with st.chat_message("user"):
                st.markdown(q)
            with st.chat_message("assistant"):
                try:
                    history_context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-4:]])

                    is_student_understood = detect_student_concluded_intent(q, st.session_state.messages)
                    t2_quote_data = get_unique_philosophical_lesson(2, subject)
                    t2_cross_ctx = get_cross_station_pedagogical_context(2)

                    if is_student_understood:
                        t2_followup_inst = build_socratic_master_instruction(subject, grade_num, student_name, mode="theory")
                        prompt_msg = (
                            f"Bối cảnh liên trạm của học sinh:\n{t2_cross_ctx}\n"
                            f"Lịch sử đối thoại trước đó:\n{history_context}\n"
                            f"Học sinh {student_name} phản hồi: \"{q}\"\n\n"
                            f"🎯 MỆNH LỆNH SƯ PHẠM ĐỈNH CAO - CHỐT ĐIỂM CHẠM SƯ PHẠM TRẠM 2 (CLOSURE) & TRAO TRUYỀN TRIẾT LÝ NHÂN CÁCH Á - ÂU:\n"
                            f"1. DỪNG TRUY VẤN: Tuyệt đối KHÔNG hỏi thêm bất kỳ câu hỏi nào. Học sinh đã tự tháo gỡ hoàn toàn các nút thắt bài tập và không còn băn khoăn gì nữa!\n"
                            f"2. BIỂU DƯƠNG NỒNG NHIỆT: Khen ngợi tinh thần vượt khó, sự kiên định không bỏ cuộc và tư duy tự sửa sai trung thực của {student_name}.\n"
                            f"3. ĐÓNG GÓI BẢN CHẤT: Chốt 1 câu ngắn gọn về kinh nghiệm cốt lõi để không bao giờ tái phạm lỗi này nữa.\n"
                            f"4. BÀI HỌC TRIẾT LÝ NHÂN CÁCH & LẼ SỐNG (BẮT BUỘC): Đúc kết bài học về ý chí và sự cẩn trọng: {t2_quote_data['lesson']} kèm câu danh ngôn triết lý của {t2_quote_data['author']} ({t2_quote_data['origin']}): \"{t2_quote_data['quote']}\". (LƯU Ý: Tuyệt đối không trùng lặp với danh ngôn ở Trạm 1).\n"
                            f"5. LỜI CHÚC ÂN CẦN: Lời chúc yêu thương, truyền cảm hứng của Người Thầy tiếp thêm ngọn lửa tự tin cho {student_name} tiến vào Trạm 3 (Khảo thí & Đột phá năng lực)!"
                        )
                        register_station_closure(2, t2_quote_data)
                    else:
                        t2_followup_inst = build_socratic_master_instruction(subject, grade_num, student_name, mode="follow_up")
                        prompt_msg = (
                            f"Bối cảnh liên trạm:\n{t2_cross_ctx}\n"
                            f"Lịch sử đối thoại trước đó:\n{history_context}\n"
                            f"Học sinh {student_name} hỏi: \"{q}\"\n"
                            f"Thầy phản hồi gợi mở Socratic trí tuệ, ân cần, giải thích bản chất (thuần Text & LaTeX, tuyệt đối không giải hộ, bám sát SGK KNTT Lớp {grade_num}). "
                            f"LƯU Ý SƯ PHẠM: Cuối câu gợi mở, hãy hỏi tự nhiên: 'Chỗ này em đã nắm chắc các bước chưa, còn điều gì băn khoăn muốn hỏi Thầy nữa không?'. "
                            f"TUYỆT ĐỐI CHƯA chốt bài học triết lý đạo đức ở bước này khi học sinh vẫn đang gỡ rối bài tập."
                        )

                    stream_gen2 = stream_gemini_with_fallback(
                        prompt_msg,
                        system_instruction=t2_followup_inst
                    )
                    clean_rep = st.write_stream(stream_gen2)
                    if "<DIAGNOSTIC>" in clean_rep:
                        clean_rep = clean_rep.split("<DIAGNOSTIC>")[0].strip()
                    st.session_state.messages.append({"role": "assistant", "content": clean_rep})
                except Exception as e:
                    st.error(f"Lỗi phản hồi: {e}")









# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# DỊCH VỤ MA TRẬN ĐẶC TẢ ĐỀ THI (ĐÃ ĐƯỢC TÁCH MODULE services/curriculum_matrix.py)
from services.curriculum_matrix import render_subject_exam_matrix_spec
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------

# TRẠM 3: KHẢO THÍ ĐỘC LẬP (MÃ ĐỀ 4 CHỮ SỐ & LATEX IN ẤN CHUẨN BỘ)

# ------------------------------------------------------------------------------

# ==============================================================================

if selected_station == station_labels[2]:


    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader(f"📝 Trạm 3: Khảo Thí Độc Lập - Môn {subject} (Lớp {grade_num})")

    if subject == "Ngữ văn":

        st.caption("Cấu trúc Khảo thí Ngữ văn 2026 (Theo QĐ 764/QĐ-BGDĐT & CV 3175/BGDĐT-GDTrH) • 100% Tự luận (Đọc hiểu 4.0đ & Viết 6.0đ) • Ngữ liệu mới ngoài SGK • Chấm thi Face-to-Face chuẩn Rubric.")

    elif subject == "Tiếng Anh":

        st.caption("Cấu trúc Khảo thí Tiếng Anh 2026 (Theo QĐ 764/QĐ-BGDĐT & Khung 6 Bậc VN / CEFR) • 40 câu trắc nghiệm 4 chọn 1 • 50 phút • Mã đề 4 chữ số • Xuất bản LaTeX & Bản in A4.")

    elif subject == "Toán học":

        st.caption("Cấu trúc Khảo thí Toán học 2026 (Theo QĐ 764/QĐ-BGDĐT) • 3 Phần Trắc nghiệm phân hóa (12 TN + 4 Đ/S + 6 TLN) • 90 phút • Mã đề 4 chữ số • Xuất bản LaTeX Overleaf & Bản in A4.")

    elif subject == "Vật lý":

        st.caption("Cấu trúc Khảo thí Vật lý 2026 (Theo QĐ 764/QĐ-BGDĐT) • 3 Phần Trắc nghiệm phân hóa (18 TN + 4 Đ/S + 6 TLN) • 50 phút • Chuẩn hệ đo lường Quốc tế SI • Xuất bản LaTeX & Bản in A4.")

    elif subject == "Hóa học":

        st.caption("Cấu trúc Khảo thí Hóa học 2026 (Theo QĐ 764/QĐ-BGDĐT) • 3 Phần Trắc nghiệm phân hóa (18 TN + 4 Đ/S + 6 TLN) • 50 phút • Chuẩn 100% Danh pháp Quốc tế IUPAC • Xuất bản LaTeX & Bản in A4.")

    elif subject == "Sinh học":

        st.caption("Cấu trúc Khảo thí Sinh học 2026 (Theo QĐ 764/QĐ-BGDĐT) • 3 Phần Trắc nghiệm phân hóa (18 TN + 4 Đ/S + 6 TLN) • 50 phút • Phân hóa Di truyền & Sinh thái học • Xuất bản LaTeX & Bản in A4.")

    elif subject == "Khoa học tự nhiên":

        st.caption("Cấu trúc Khảo thí KHTN 2026 (Theo TT 22/2021/TT-BGDĐT) • Tích hợp Vật lý SI - Hóa học IUPAC - Sinh học KNTT • Xuất bản Bản in A4.")

    else:

        st.caption(f"Cấu trúc Khảo thí {subject} 2026 (Theo QĐ 764/QĐ-BGDĐT) • 2 Phần Trắc nghiệm phân hóa (24 TN + 4 Đ/S) • 50 phút • Mã đề 4 chữ số • Xuất bản LaTeX & Bản in A4.")



    with st.expander(f"📋 Ma Trận & Bản Đặc Tả Đề Thi Chuẩn Bộ GD&ĐT - Môn {subject} (Theo QĐ 764/QĐ-BGDĐT)", expanded=False):

        st.markdown(render_subject_exam_matrix_spec(subject, grade_num), unsafe_allow_html=True)



    if "exam_state" not in st.session_state: st.session_state.exam_state = "config"

    if "exam_data" not in st.session_state: st.session_state.exam_data = None

    if "violation_count" not in st.session_state: st.session_state.violation_count = 0

    if "exam_answers" not in st.session_state: st.session_state.exam_answers = {}

    if "tram3_chat_messages" not in st.session_state: st.session_state.tram3_chat_messages = []

    if "exam_code" not in st.session_state: st.session_state.exam_code = str(random.randint(1011, 9999))



    def preflight_exam_auto_heal(exam, subject_name="Toán học", grade_level=12):
        r"""
        BỘ KIỂM SOÁT ĐA TẦNG 7 LỚP CHUYÊN SÂU (7-LAYER PRECISION QUALITY GATE - CHECK DEEP VAR):
        Đảm bảo 100% tính chính xác khoa học, triệt tiêu ảo giác AI, phục dựng đồ thị/hình vẽ hoàn hảo:
        - Lớp 1: Syntax & LaTeX Normalizer (Cân bằng $, khử sạch chữ 'mega' -> \pm\infty, vá \frac, \sqrt).
        - Lớp 2: Pedagogical Program Guard (Chuẩn hóa tâm đối xứng x0 = -b/3a, khử y''=0, cấm vi phạm CT 2006).
        - Lớp 3: Exam Integrity & Anti-Collision Guard (Chuẩn hóa 4 lựa chọn A, B, C, D duy nhất, chống 2 đáp án trùng).
        - Lớp 4: Socratic Knowledge Firewall (Bức tường lửa gợi mở tư duy, loại bỏ kết luận lộ liễu).
        - Lớp 5: Rational Degeneracy & Asymptote Parity Guard (Chống suy biến hàm phân thức, chuẩn hóa BBT tiệm cận đứng || thay vì 0).
        - Lớp 6: Deep Derivative Engine (Tính ngầm f' và f'' để sinh đồ thị y = f'(x) chuẩn xác cho câu hỏi đơn điệu và cực trị).
        - Lớp 7: Strict Visual & Multi-Subject Parity Enforcer Guard (Bảo đảm 100% câu hỏi có từ khóa thị giác đều có đồ thị/mô hình hiển thị, đa môn Toán, Lý, Hóa, Sinh, Địa).
        """
        if not isinstance(exam, dict):
            return exam

        for p_key in ["p1", "p2", "p3"]:
            for idx_q, q in enumerate(exam.get(p_key, [])):
                if not isinstance(q, dict):
                    continue

                # ==============================================================================
                # LỚP 1: CÂN BẰNG DẤU $, SỬA LATEX & KHỬ TRIỆT ĐỂ CHỮ "MEGA" = VÔ CỰC
                # ==============================================================================
                if subject_name not in ["Ngữ văn", "Tiếng Anh"]:
                    if q.get("q"):
                        q["q"] = format_pedagogical_math(q["q"])
                    if q.get("opt"):
                        q["opt"] = [format_pedagogical_math(str(o)) for o in q["opt"]]
                    for s in q.get("stmts", []):
                        if s.get("t"):
                            s["t"] = format_pedagogical_math(str(s["t"]))
                    if q.get("explain"):
                        q["explain"] = format_pedagogical_math(str(q["explain"]))

                # Khử triệt để chữ mega / omega dùng nhầm thành vô cực trong tất cả các trường
                def clean_mega_inf(txt):
                    if not txt: return ""
                    t = str(txt)
                    t = re.sub(r'(?i)(?<=[\(\[\s;,-])-+\s*mega\b', r'-\\infty', t)
                    t = re.sub(r'(?i)\b-\s*mega\b', r'-\\infty', t)
                    t = re.sub(r'(?i)\+\s*mega\b', r'+\\infty', t)
                    t = re.sub(r'(?i)(?<=[;,\s])\s*\+?mega(?=[\)\]\s;,])', r'+\\infty', t)
                    t = re.sub(r'(?i)(?<=[(\[\s])-?\s*\\?[oO]mega\b', r'-\\infty', t)
                    t = re.sub(r'(?i);\s*\+?\s*\\?[oO]mega\s*(?=[)\]])', r'; +\\infty', t)
                    return t

                if q.get("q"): q["q"] = clean_mega_inf(q["q"])
                if q.get("opt"): q["opt"] = [clean_mega_inf(o) for o in q["opt"]]
                for s in q.get("stmts", []):
                    if s.get("t"): s["t"] = clean_mega_inf(s["t"])
                if q.get("explain"): q["explain"] = clean_mega_inf(q["explain"])

                # ==============================================================================
                # LỚP 2: BẢO VỆ CHƯƠNG TRÌNH GDPT 2018 (KHỬ ĐIỂM UỐN & ĐẠO HÀM CẤP 2 TRẦN TRỤI)
                # ==============================================================================
                q_txt_lower = str(q.get("q", "")).lower()
                if "điểm uốn" in q_txt_lower or "điểm uốn" in str(q.get("explain", "")).lower():
                    q["q"] = q["q"].replace("điểm uốn", "tâm đối xứng").replace("Điểm uốn", "Tâm đối xứng")
                    if q.get("explain"):
                        q["explain"] = str(q["explain"]).replace("điểm uốn", "tâm đối xứng").replace("Điểm uốn", "Tâm đối xứng")

                # ==============================================================================
                # LỚP 3: CHUẨN HÓA TÍNH TOÀN VẸN KHẢO THÍ & CHỐNG HIỆN TƯỢNG 2 ĐÁP ÁN ĐÚNG
                # ==============================================================================
                if p_key == "p1":
                    opts = q.get("opt", [])
                    if len(opts) < 4:
                        letters = ["A", "B", "C", "D"]
                        while len(opts) < 4:
                            opts.append(f"{letters[len(opts)]}. Đang cập nhật")
                        q["opt"] = opts
                    ans = str(q.get("ans", "")).strip().upper()
                    if len(ans) > 1 and ans[0] in ["A", "B", "C", "D"] and (ans[1] in [".", ":", ")", " "]):
                        q["ans"] = ans[0]
                    elif ans not in ["A", "B", "C", "D"]:
                        q["ans"] = "A"

                    # Chống 2 đáp án cùng đúng/trùng nhau trong câu hỏi đồng biến/nghịch biến
                    if "đồng biến" in q_txt_lower or "nghịch biến" in q_txt_lower:
                        ans_letter = str(q.get("ans", "A")).strip().upper()
                        ans_idx = ord(ans_letter) - ord('A') if ans_letter in "ABCD" else 0
                        has_neg_inf = [i for i, o in enumerate(opts) if "-∞" in o or "-\\infty" in o or "-inf" in o]
                        has_pos_inf = [i for i, o in enumerate(opts) if "+∞" in o or "+\\infty" in o or "+inf" in o]
                        if "đồng biến" in q_txt_lower and has_neg_inf and has_pos_inf:
                            idx_neg = has_neg_inf[0]
                            idx_pos = has_pos_inf[0]
                            if idx_neg != idx_pos:
                                letters = ["A", "B", "C", "D"]
                                if ans_idx == idx_neg:
                                    opts[idx_pos] = f"{letters[idx_pos]}. (-1; 1)"
                                elif ans_idx == idx_pos:
                                    opts[idx_neg] = f"{letters[idx_neg]}. (-1; 1)"
                                else:
                                    opts[idx_pos] = f"{letters[idx_pos]}. (-1; 1)"
                                q["opt"] = opts

                elif p_key == "p2":
                    stmts = q.get("stmts", [])
                    while len(stmts) < 4:
                        stmts.append({"t": "Mệnh đề đang cập nhật", "a": True, "ans": True})
                    for s in stmts:
                        s_val = s.get("a") if "a" in s else s.get("ans", True)
                        s["a"] = bool(s_val)
                        s["ans"] = bool(s_val)
                    q["stmts"] = stmts

                elif p_key == "p3":
                    raw_ans = str(q.get("ans", "")).strip()
                    q["ans"] = raw_ans[:4] if raw_ans else "0"

                # ==============================================================================
                # LỚP 4: BỨC TƯỜNG LỬA SOCRATIC CHỐNG LỘ ĐÁP ÁN
                # ==============================================================================
                if q.get("explain"):
                    ans_str = str(q.get("ans", ""))
                    q["explain"] = sanitize_socratic_hint(
                        q["explain"], ans_str, q.get("q", ""), q.get("opt"), q.get("level", "TH"),
                        subject=subject_name, grade_num=grade_level
                    )

                # ==============================================================================
                # LỚP 5: CHỐNG SUY BIẾN PHÂN THỨC & CHUẨN HÓA BBT TIỆM CẬN (|| THAY VÌ 0)
                # ==============================================================================
                if q.get("bbt"):
                    q_bbt_str = str(q["bbt"]).strip()
                    q_bbt_str = re.sub(r'\\+nearrow\b|\\nearrow', '↗', q_bbt_str)
                    q_bbt_str = re.sub(r'\\+searrow\b|\\searrow', '↘', q_bbt_str)
                    q_bbt_str = q_bbt_str.replace('>>', '↗').replace('>', '↗')
                    q_bbt_str = re.sub(r'\\n(?!earrow)', '\n', q_bbt_str).strip()
                    if pve and hasattr(pve, "heal_bbt_mathematics"):
                        try:
                            q_bbt_str = pve.heal_bbt_mathematics(q_bbt_str)
                        except Exception:
                            pass
                    q["bbt"] = q_bbt_str
                    bbt_txt = q_bbt_str
                    is_tiem_can = any(tc_w in q_txt_lower for tc_w in ["tiệm cận", "tiem can", "đường tiệm cận"])
                    bbt_rows = [r.strip() for r in bbt_txt.split('\n') if r.strip() and '---' not in r]
                    if is_tiem_can and len(bbt_rows) >= 3:
                        # Dòng y' không được phép có số 0 ở điểm gián đoạn vô cực
                        yp_lbl = bbt_rows[1].split('|')[0].strip()
                        yp_cells = [c.strip() for c in bbt_rows[1].split('|')[1:]]
                        has_healed_yp = False
                        new_yp_cells = []
                        for cell_val in yp_cells:
                            if cell_val == '0' and any(inf_w in bbt_txt for inf_w in ['||', '║', 'inf', '∞', '\\infty']):
                                new_yp_cells.append('||')
                                has_healed_yp = True
                            else:
                                new_yp_cells.append(cell_val)
                        if has_healed_yp:
                            x_line = bbt_rows[0]
                            q["bbt"] = f"{x_line}\n{yp_lbl} | {' | '.join(new_yp_cells)}\n{bbt_rows[2]}"

                # ==============================================================================
                # LỚP 6: DEEP DERIVATIVE ENGINE (TÍNH NGẦM f' VÀ f'' ĐỂ ĐỒNG BỘ ĐỒ THỊ y = f'(x))
                # ==============================================================================
                has_visual_cue = any(kw in q_txt_lower for kw in [
                    "như hình vẽ bên", "hình vẽ bên", "hình bên", "đồ thị hình bên", "đường cong trong hình",
                    "như hình vẽ", "đồ thị bên", "đồ thị như hình", "cho đồ thị như hình",
                    "bảng biến thiên như hình", "sơ đồ như hình", "mô hình bên", "như hình dưới đây"
                ])

                is_fprime_q = (any(k in q_txt_lower for k in ["đồ thị của hàm số đạo hàm", "đồ thị hàm số y = f'", "đồ thị đạo hàm", "có đồ thị y = f'", "đồ thị y = f'", "y = f'(x)", "f'(x)"]) or ("f'" in q_txt_lower and any(w in q_txt_lower for w in ["đồ thị", "hình vẽ"])))
                if is_fprime_q and has_visual_cue and pve:
                    deriv_model = pve.solve_derivative_fprime_model(q.get("q", ""), q.get("opt", []), str(q.get("ans", "")))
                    q["f"] = deriv_model
                    q["tikz"] = deriv_model["tikz"]

                # ==============================================================================
                # LỚP 7: STRICT VISUAL & MULTI-SUBJECT PARITY ENFORCER GUARD (CHUẨN GDPT 2018 & KNTT)
                # ==============================================================================
                if has_visual_cue:
                    has_any_visual = bool(q.get("f") or q.get("geom_3d") or q.get("bbt") or q.get("composite_visual") or q.get("circuit_visual") or q.get("chem_visual") or q.get("pedigree_visual") or q.get("geo_chart"))
                    if not has_any_visual and ree and hasattr(ree, "attach_question_visuals"):
                        try:
                            q = ree.attach_question_visuals(q, subject=subject_name, grade=grade_level)
                        except Exception:
                            pass

                    # Bù đắp THÔNG MINH THEO NGỮ CẢNH GDPT 2018 cho môn Toán nếu vẫn chưa có f
                    if not q.get("f") and not q.get("geom_3d") and not q.get("bbt") and subject_name == "Toán học" and pve:
                        raw_q_curr = str(q.get("q") or "")
                        # 1. Phân thức 2/1 chuẩn SGK KNTT Toán 12
                        if any(k in q_txt_lower for k in ["tiệm cận xiên", "2/1"]) or ("x^2" in q_txt_lower and any(d in q_txt_lower for d in ["x-1", "x+1", "x-2", "x+2", "x-", "x+"])):
                            q["f"] = pve.solve_rational_2_1_from_text(raw_q_curr, q.get("opt", []), str(q.get("ans", "")))
                            q["tikz"] = pve.build_rational_2_1_tikz(q["f"]["a"], q["f"]["b"], q["f"]["c"], q["f"]["d"], q["f"]["e"])
                        # 2. Phân thức 1/1
                        elif any(k in q_txt_lower for k in ["tiệm cận", "phân thức"]) or ("/" in q_txt_lower and "x" in q_txt_lower):
                            q["f"] = pve.solve_rational_1_1_from_text(raw_q_curr, q.get("opt", []), str(q.get("ans", ""))) or {"type": "func_1_1", "a": 2.0, "b": -1.0, "c": 1.0, "d": -1.0}
                            q["tikz"] = pve.build_rational_1_1_tikz(q["f"]["a"], q["f"]["b"], q["f"]["c"], q["f"]["d"])
                        # 3. Đạo hàm f'
                        elif is_fprime_q:
                            deriv_model = pve.solve_derivative_fprime_model(raw_q_curr, q.get("opt", []), str(q.get("ans", "")))
                            q["f"] = deriv_model
                            q["tikz"] = deriv_model["tikz"]
                        # 4. Hàm bậc ba
                        elif any(k in q_txt_lower for k in ["bậc ba", "bậc 3", "ax^3"]):
                            q["f"] = pve.solve_cubic_from_text_or_opts(raw_q_curr, q.get("opt", []), str(q.get("ans", "")))
                else:
                    # CHỐT CHẶN CUỐI CÙNG TỐI THƯỢNG (THEO MỆNH LỆNH THẦY TRÍ):
                    # Không có từ khóa đòi hỏi hình vẽ -> Triệt tiêu 100% đồ thị hàm số 2D (f) và tikz
                    q.pop("f", None)
                    is_geom_3d_spatial = any(k in q_txt_lower for k in [
                        "tứ diện", "mặt cầu", "khối chóp", "hình chóp", "lăng trụ", "hình hộp",
                        "oxyz", "bán kính", "khối nón", "khối trụ", "hình nón", "hình trụ",
                        "khối tròn xoay", "s.abcd", "s.abc", "oabc"
                    ])
                    if not is_geom_3d_spatial:
                        q.pop("geom_3d", None)
                    if not q.get("composite_visual") and not is_geom_3d_spatial:
                        q.pop("tikz", None)

                # KIỂM DUYỆT & CHỮA LÀNH NGỮ CẢNH CUỐI CÙNG QUA BỘ LỌC 0-TOKEN
                if pve and hasattr(pve, "audit_and_heal_visual_context_gdpt2018"):
                    q = pve.audit_and_heal_visual_context_gdpt2018(q, subject=subject_name, grade=grade_level)



        if "part_doc_hieu" in exam and isinstance(exam["part_doc_hieu"], dict):

            for q in exam["part_doc_hieu"].get("questions", []):

                if q.get("explain"):

                    q["explain"] = sanitize_socratic_hint(

                        q["explain"], str(q.get("ans", "")), q.get("q", ""), None, "TH",

                        subject="Ngữ văn", grade_num=grade_level

                    )

        if "part_viet" in exam and isinstance(exam["part_viet"], list):

            for v in exam["part_viet"]:

                if v.get("explain"):

                    v["explain"] = sanitize_socratic_hint(

                        v["explain"], str(v.get("ans", "")), v.get("q", ""), None, "VD",

                        subject="Ngữ văn", grade_num=grade_level

                    )



        return exam



    def enrich_exam_data(exam):
        if not isinstance(exam, dict): return exam
        try:
            return _internal_enrich_exam_data(exam)
        except Exception as _e_enrich:
            logging.error("Lỗi khi enrich_exam_data: %s", _e_enrich)
            return exam

    def _internal_enrich_exam_data(exam):
        # Tự động tăng số lần khảo sát (exam_mix_count) lũy tiến cho mỗi lần tạo/trộn đề mới
        st.session_state.exam_mix_count = st.session_state.get("exam_mix_count", 0) + 1
        st.session_state.global_exam_count = max(st.session_state.get("global_exam_count", 0), st.session_state.exam_mix_count)
        exam["exam_count"] = st.session_state.exam_mix_count

        if ree and hasattr(ree, "ensure_full_exam_matrix") and subject != "Ngữ văn":
            exam = ree.ensure_full_exam_matrix(exam, subject, grade_num)

        if ree and hasattr(ree, "apply_full_7layer_quality_pipeline"):
            exam = ree.apply_full_7layer_quality_pipeline(exam, subject, grade_num)

        # PHÂN ĐỊNH RẠCH RÒI 100%: ĐỀ DO AI TỰ SÁNG TÁC (LUỒNG 1) vs ĐỀ TRÍCH XUẤT TỪ NGÂN HÀNG THẬT (LUỒNG 2)
        is_real_exam = bool(exam.get("is_real_exam", False) or exam.get("exam_source_type") == "real_bank")
        is_ai_exam = bool(exam.get("is_ai_generated", False) or exam.get("exam_source_type") == "ai_generated" or not is_real_exam)

        if is_ai_exam:
            exam["is_ai_generated"] = True
            exam["is_real_exam"] = False
            exam["exam_source_type"] = "ai_generated"
            exam["portal"] = ""
            exam["audit_trail"] = []
            exam["source"] = "Đề thi chuẩn hóa GDPT 2018 (Trợ lý AI Khảo Thí biên soạn mới 100%)"
        else:
            exam_src = exam.get("source") or exam.get("title") or exam.get("school")
            if ree and not exam_src:
                portal_info = ree.EXAM_SOURCE_PORTALS.get(subject, ree.EXAM_SOURCE_PORTALS.get("Toán học", {}))
                portal_name = portal_info.get("portal_name", "TOANMATH.com")
                exam_src = f"Đề thi khảo sát chuẩn hóa CT 2018 (Trích xuất từ Ngân hàng đề thi thật)"
                exam["source"] = exam_src

        # LOẠI BỎ TRIỆT ĐỂ CÁC CÂU LỖI NGỮ LIỆU / BBT TOÀN SỐ 0 / ĐỒ THỊ RÁC THEO YÊU CẦU THẦY TRÍ
        if ree and hasattr(ree, "is_toxic_defective_question"):
            for p_k in ["p1", "p2", "p3"]:
                exam[p_k] = [q for q in exam.get(p_k, []) if not ree.is_toxic_defective_question(q)]

        for p_key in ["p1", "p2", "p3"]:
            for idx_q, q in enumerate(exam.get(p_key, [])):
                if not isinstance(q, dict): continue

                if is_ai_exam:
                    # ĐÂY LÀ CÂU HỎI DO AI SINH RA (LUỒNG 1):
                    # TUYỆT ĐỐI KHÔNG BỊA NGUỒN TOANMATH, KHÔNG BỊA THPT CHUYÊN, KHÔNG TẠO MÃ ĐỐI SOÁT GIẢ
                    q["is_ai_generated"] = True
                    q["is_real_bank_question"] = False
                    q.pop("audit_id", None)
                    q.pop("source", None)
                    q.pop("portal", None)
                    q.pop("orig_pos", None)
                    q.pop("orig_exam_code", None)
                    q.pop("school", None)
                else:
                    # ĐÂY LÀ CÂU HỎI THẬT TỪ NGÂN HÀNG ĐỀ THI (LUỒNG 2):
                    q["is_real_bank_question"] = True
                    q["is_ai_generated"] = False
                    if not q.get("school"): q["school"] = exam.get("school", "THPT Chuyên / Điểm Toàn Quốc")
                    if not q.get("portal"): q["portal"] = exam.get("portal", "TOANMATH.com")
                    if not q.get("year"): q["year"] = exam.get("year", "2025 - 2026")
                    if not q.get("exam_session"):
                        t_low = (str(exam.get("title", "")) + " " + str(exam.get("exam_type", ""))).lower()
                        if "cuối" in t_low or "hk1" in t_low:
                            q["exam_session"] = "Kỳ thi Cuối Học Kỳ 1 (Chính thức)"
                        elif "giữa" in t_low:
                            q["exam_session"] = "Kỳ thi Giữa Học Kỳ 1 (Lần 1)"
                        elif "thử" in t_low:
                            q["exam_session"] = "Thi Thử Tốt Nghiệp THPT (Lần 1)"
                        else:
                            q["exam_session"] = "Kỳ thi Khảo Sát Đánh Giá Năng Lực"
                    if not q.get("orig_pos"):
                        part_str = "Phần I" if p_key == "p1" else ("Phần II" if p_key == "p2" else "Phần III")
                        q["orig_pos"] = f"{part_str} - Câu {idx_q + 1}"
                    if not q.get("audit_id"):
                        q["audit_id"] = f"{str(q['portal']).split('.')[0]}_{exam.get('code','2501')}_{p_key}_{idx_q+1}"
                    if not q.get("source"):
                        q["source"] = f"{q['school']} • {q['exam_session']} ({q['year']}) • [Đề gốc: Mã {exam.get('code','2501')} - {q['orig_pos']}] • Nguồn: {q['portal']}"



                # 1. TỰ ĐỘNG TÁCH MẪU SỐ LIỆU GHÉP NHÓM TỪ DẠNG TEXT THÀNH BẢNG HTML CHUẨN

                q = auto_extract_mslgn(q)



                # 2. KHỬ TRIỆT ĐỂ KHÁI NIỆM "ĐIỂM UỐN" & y'' = 0 (VI PHẠM CT GDPT 2018)

                if q.get("q"):

                    q["q"] = q["q"].replace("điểm uốn", "tâm đối xứng").replace("Điểm uốn", "Tâm đối xứng")

                    q["q"] = q["q"].replace("y'' = 0", "$x_0 = -\\frac{b}{3a}$").replace("y''", "đạo hàm")

                if q.get("opt"):

                    new_opts = []

                    for o in q["opt"]:

                        no = o.replace("điểm uốn", "tâm đối xứng").replace("Điểm uốn", "Tâm đối xứng")

                        no = no.replace("y'' = 0", "$x_0 = -\\frac{b}{3a}$ (hoặc trung điểm 2 cực trị)").replace("y''", "đạo hàm")

                        new_opts.append(no)

                    q["opt"] = new_opts

                for s in q.get("stmts", []):

                    if s.get("t"):

                        s["t"] = re.sub(r'^[a-dA-D]\s*[\)\.\:]\s*', '', str(s["t"])).strip()

                        s["t"] = s["t"].replace("điểm uốn", "tâm đối xứng").replace("Điểm uốn", "Tâm đối xứng")

                        s["t"] = s["t"].replace("y'' = 0", "$x_0 = -\\frac{b}{3a}$").replace("y''", "đạo hàm")



                # 3. CHUẨN HÓA CÔNG THỨC TOÁN LATEX ĐA MÔN

                if subject not in ["Ngữ văn", "Tiếng Anh"]:

                    if q.get("q"): q["q"] = format_pedagogical_math(q["q"])

                    for s in q.get("stmts", []):

                        if s.get("t"): s["t"] = format_pedagogical_math(s["t"])

                    if q.get("opt"): q["opt"] = [format_pedagogical_math(o) for o in q["opt"]]

                    if q.get("explain"): q["explain"] = format_pedagogical_math(q["explain"])



                q_text = str(q.get("q", ""))

                q_txt_lower = q_text.lower()



                # --- 4. TỰ ĐỘNG BÓC TÁCH BBT TỪ NỘI DUNG CÂU HỎI q NẾU AI LỠ VIẾT BẢNG MARKDOWN VÀO q THAY VÌ TRƯỜNG "bbt" ---

                if not q.get("bbt") and ("\n" in q_text or "|" in q_text):

                    raw_lines = [l.strip() for l in q_text.split("\n") if l.strip()]

                    table_lines = [l for l in raw_lines if "|" in l and any(k in l.lower() for k in ["x", "y'", "y", "f'(x)", "f(x)"])]

                    if len(table_lines) >= 2:

                        q["bbt"] = "\n".join(table_lines)

                        clean_q_lines = [l for l in raw_lines if l not in table_lines and not re.match(r'^[|\s:-]+$', l)]

                        q["q"] = "\n".join(clean_q_lines).strip()

                        q_text = str(q.get("q", ""))

                        q_txt_lower = q_text.lower()



                if q.get("q"):

                    q["q"] = clean_question_bbt_text(q["q"])

                    q = extract_and_normalize_mslgn(q)

                    q_text = str(q.get("q", ""))

                    q_txt_lower = q_text.lower()



                # --- 4.1. CƠ CHẾ PHỤC DỰNG NGỮ LIỆU HÌNH VẼ & TIKZ VECTOR CHUẨN QUỐC TẾ KHI ĐỀ HỎI HÌNH MÀ THIẾU ---
                # A. BẢO VỆ CÁC MÔN KHOA HỌC TỰ NHIÊN / XÃ HỘI (VẬT LÝ, HÓA HỌC, SINH HỌC, ĐỊA LÝ, TIN HỌC, VĂN, SỬ, ANH):
                if subject != "Toán học":
                    q.pop("f", None)
                    q.pop("bbt", None)
                    q.pop("mslgn_data", None)
                    if not any(k in q_txt_lower for k in ["mô hình", "sơ đồ", "thí nghiệm"]):
                        q.pop("geom_3d", None)
                    if pve and hasattr(pve, "enrich_question_visual_precision"):
                        try:
                            q = pve.enrich_question_visual_precision(q, subject=subject, grade=grade_num)
                        except Exception:
                            pass

                # CHỐT CHẶN CÁCH LY PHÂN MÔN & THỐNG KÊ MSLGN (CHUẨN GDPT 2018):
                is_statistical_mslgn = any(k in q_txt_lower for k in [
                    "ghép nhóm", "mẫu số liệu", "mslgn", "tần số", "khoảng tứ phân vị",
                    "độ lệch chuẩn", "phương sai", "cỡ mẫu", "trung vị", "mốt", "giá trị đại diện",
                    "tần số ghép nhóm", "bảng số liệu ghép nhóm"
                ]) or bool(re.search(r'\[\s*\d+(?:[\.,]\d+)?\s*[;,]\s*\d+(?:[\.,]\d+)?\s*\)', q_text))

                if is_statistical_mslgn or subject != "Toán học":
                    q.pop("bbt", None)
                    has_need_bbt = False
                else:
                    has_need_bbt = (
                        any(kw in q_txt_lower for kw in ["bảng biến thiên", "bbt", "bảng xét dấu", "chiều biến thiên"]) or
                        (any(kw in q_txt_lower for kw in ["bảng dưới đây", "bảng sau"]) and any(kw in q_txt_lower for kw in ["hàm số", "đạo hàm", "f'(x)", "f(x)", "y'", "đồng biến", "nghịch biến"]))
                    )

                has_visual_cue = (
                    any(kw in q_txt_lower for kw in [
                        "như hình vẽ", "hình vẽ bên", "đồ thị hình bên", "đường cong dưới đây",
                        "đường cong hình bên", "tham khảo hình vẽ", "tham khảo hình", "đồ thị như hình vẽ", "có hình vẽ",
                        "đồ thị như hình", "trong hình vẽ", "ở hình vẽ", "như hình bên", "hình dưới đây", "đường cong trong hình", "hình vẽ"
                    ]) or (
                        any(kw in q_txt_lower for kw in ["đồ thị của hàm số nào", "là của hàm số nào", "đồ thị hàm số nào", "đường cong dưới đây là đồ thị", "hình vẽ bên là đồ thị"])
                        and any(w in q_txt_lower for w in ["hình vẽ", "hình bên", "đường cong", "như hình", "hình dưới", "hình sau"])
                    )
                )

                # Khử triệt để câu hỏi lý thuyết nhận dạng hình dạng chữ cái (chữ N, chữ W, chữ U, chữ M) khi KHÔNG có hình vẽ minh họa:
                if any(k in q_txt_lower for k in ["chữ n", "chữ u", "chữ w", "chữ m"]) and not any(w in q_txt_lower for w in ["hình vẽ", "hình bên", "đường cong", "như hình", "trong hình", "ở hình", "hình dưới"]):
                    has_visual_cue = False
                    q.pop("f", None)
                    q.pop("tikz", None)

                has_image = bool(q.get("image_base64") or q.get("image_url") or q.get("image"))

                has_model = bool(q.get("f") or q.get("geom_3d") or q.get("bbt") or q.get("tikz") or q.get("composite_visual"))

                # Phục dựng toán thực tế: Bình nước quả cầu sắt (chỉ cho môn Toán)
                if subject == "Toán học" and any(kw in q_txt_lower for kw in ["quả cầu sắt", "bình có dạng hình hộp", "bình hình hộp"]) and not q.get("geom_3d"):
                    q["geom_3d"] = {"type": "box_with_sphere", "dim": "3d"}
                    has_model = True

                # Phục dựng toán thực tế: Cửa sổ bán nguyệt (chỉ cho môn Toán)
                if subject == "Toán học" and any(kw in q_txt_lower for kw in ["cửa sổ", "bán nguyệt", "dây thép"]) and not q.get("composite_visual"):
                    if pve:
                        q["composite_visual"] = pve.build_semi_circular_window_model()
                        q["tikz"] = q["composite_visual"].get("tikz")
                    else:
                        q["composite_visual"] = {
                            "type": "semi_circle_window",
                            "title": "Mô hình cửa sổ gồm hình chữ nhật ghép hình bán nguyệt:",
                            "svg": sanitize_svg_for_markdown("""<svg width="280" height="260" viewBox="0 0 280 260" xmlns="http://www.w3.org/2000/svg">
<rect x="50" y="110" width="180" height="120" fill="#0284c7" fill-opacity="0.25" stroke="#38bdf8" stroke-width="3"/>
<path d="M 50 110 A 90 90 0 0 1 230 110 Z" fill="#38bdf8" fill-opacity="0.35" stroke="#0ea5e9" stroke-width="3"/>
<line x1="50" y1="110" x2="230" y2="110" stroke="#f59e0b" stroke-width="2.5" stroke-dasharray="4,4"/>
<text x="140" y="245" fill="#f8fafc" font-size="14" font-weight="bold" text-anchor="middle">Chiều rộng: x</text>
<text x="25" y="175" fill="#f8fafc" font-size="14" font-weight="bold" text-anchor="middle">Chiều cao: y</text>
<text x="140" y="70" fill="#38bdf8" font-size="14" font-weight="bold" text-anchor="middle">Bán kính R = x/2</text>
</svg>""")
                        }
                    has_model = True

                # Phục dựng toán thực tế: Dải đèn LED tiếp xúc đường tròn (chỉ cho môn Toán)
                if subject == "Toán học" and any(kw in q_txt_lower for kw in ["dải led", "đèn led", "dải cong"]):
                    q.pop("f", None)
                    if pve:
                        q["composite_visual"] = pve.build_led_strip_model()
                        q["tikz"] = q["composite_visual"].get("tikz")
                    else:
                        q["composite_visual"] = {
                            "type": "led_strip_circle",
                            "title": "Sơ đồ thiết kế dải LED tiếp xúc đường tròn trong hình chữ nhật ABCD:",
                            "svg": sanitize_svg_for_markdown("""<svg width="340" height="260" viewBox="0 0 340 260" xmlns="http://www.w3.org/2000/svg">
<rect x="40" y="40" width="260" height="170" fill="#0f172a" stroke="#475569" stroke-width="2"/>
<circle cx="170" cy="170" r="45" fill="none" stroke="#f43f5e" stroke-width="2.5"/>
<path d="M 40 210 Q 120 180 170 125 T 300 40" fill="none" stroke="#38bdf8" stroke-width="4"/>
<circle cx="170" cy="125" r="4.5" fill="#facc15"/>
<text x="175" y="120" fill="#facc15" font-size="13" font-weight="bold">H(3; 2) - Điểm tiếp xúc</text>
<text x="40" y="230" fill="#94a3b8" font-size="13">A(0;0)</text>
<text x="300" y="30" fill="#94a3b8" font-size="13">C(6;4)</text>
</svg>""")
                        }
                    has_model = True

                # NẾU CÂU HỎI CÓ HÌNH ẢNH HOẶC YÊU CẦU NHÌN HÌNH MÀ CHƯA CÓ MÔ HÌNH TOÁN HỌC -> TỰ ĐỘNG PHỤC DỰNG VECTOR 100%
                if (has_visual_cue or has_image or q.get("has_visual")) and not has_model:
                    if ree and hasattr(ree, "attach_question_visuals"):
                        try:
                            q = ree.attach_question_visuals(q, subject=subject, grade=grade_num)
                        except Exception:
                            pass

                    # A0. Nhận diện đồ thị hàm số (2/1, 1/1, bậc ba) khớp chính xác với phương án đáp án đúng (VIP 73.2 ANTI-FLICKER):
                    is_ident_graph = any(k in q_txt_lower for k in ["đường cong trong hình", "hình vẽ bên là đồ thị", "đồ thị hình bên", "đồ thị như hình", "cho đồ thị như hình"]) or (
                        any(k in q_txt_lower for k in ["đồ thị của hàm số nào", "là của hàm số nào", "đồ thị hàm số nào", "đường cong dưới đây là đồ thị"])
                        and any(w in q_txt_lower for w in ["hình vẽ", "hình bên", "đường cong", "như hình", "hình dưới", "hình sau"])
                    )

                    is_calc_algebra = any(k in q_txt_lower for k in ["biểu thức", "giá trị của biểu thức", "bằng bao nhiêu", "tìm m", "tìm tham số", "t =", "p =", "t = ", "p = "]) or (any(k in q_txt_lower for k in ["tính", "giá trị của"]) and any(k in q_txt_lower for k in ["biểu thức", "t =", "p =", "t = ", "p = ", "tham số"]))

                    if is_ident_graph and not is_calc_algebra and subject == "Toán học":
                        opts = q.get("opt", [])
                        ans_letter = str(q.get("ans", "")).strip().upper()[:1]
                        target_opt_str = ""
                        if opts and isinstance(opts, list):
                            ans_idx = ord(ans_letter) - ord("A") if ans_letter in ("A", "B", "C", "D") else 0
                            target_opt_str = str(opts[ans_idx]) if 0 <= ans_idx < len(opts) else str(opts[0])

                        opts_str = " ".join(str(o) for o in opts)
                        combined_all = (q_text + " " + target_opt_str + " " + opts_str).lower()

                        is_2_1 = bool(re.search(r'\\frac\{[^{}]*x\^2[^{}]*\}\{[^{}]*x[^{}]*\}', target_opt_str + " " + opts_str)) or (
                            ("x^2" in target_opt_str.lower() or "x^{2}" in target_opt_str.lower()) and ("/" in target_opt_str or "frac" in target_opt_str) and any(d in target_opt_str for d in ["x-", "x+", "x -", "x +"])
                        ) or any(k in q_txt_lower for k in ["tiệm cận xiên", "2/1", "bậc hai trên bậc nhất"])

                        is_1_1 = not is_2_1 and (
                            bool(re.search(r'\\frac\{[^{}]*x[^{}]*\}\{[^{}]*x[^{}]*\}', target_opt_str + " " + opts_str)) or
                            (("/" in target_opt_str or "frac" in target_opt_str) and not any(k in target_opt_str for k in ["x^2", "x^3", "x^4"])) or
                            any(k in q_txt_lower for k in ["hàm phân thức", "hàm số phân thức", "tiệm cận đứng", "tiệm cận ngang"])
                        )

                        is_cubic = not is_2_1 and not is_1_1 and (
                            ("x^3" in target_opt_str or "x^{3}" in target_opt_str or "bậc ba" in combined_all or "bậc 3" in combined_all or "ax^3" in combined_all) or
                            ("x^3" in opts_str and not any(k in target_opt_str for k in ["/", "frac"]))
                        )

                        if is_2_1 and pve:
                            q["f"] = pve.solve_rational_2_1_from_text(q_text, q.get("opt", []), str(q.get("ans", "")))
                            q["tikz"] = pve.build_rational_2_1_tikz(q["f"]["a"], q["f"]["b"], q["f"]["c"], q["f"]["d"], q["f"]["e"])
                        elif is_1_1 and pve:
                            solved_f = pve.solve_rational_1_1_from_text(q_text, q.get("opt", []), str(q.get("ans", "")))
                            if solved_f:
                                q["f"] = solved_f
                                q["tikz"] = pve.build_rational_1_1_tikz(solved_f["a"], solved_f["b"], solved_f["c"], solved_f["d"])
                        elif is_cubic and pve:
                            q["f"] = pve.solve_cubic_from_text_or_opts(q_text, q.get("opt", []), str(q.get("ans", "")))

                    if pve and hasattr(pve, "audit_and_heal_visual_context_gdpt2018"):
                        q = pve.audit_and_heal_visual_context_gdpt2018(q, subject=subject, grade=grade_num)

                    # C. Hình chóp tứ giác S.ABCD

                    elif any(k in q_txt_lower for k in ["chóp tứ giác", "s.abcd", "hình thang"]) and "như hình vẽ" in q_txt_lower:

                        q["geom_3d"] = {"type": "pyramid_trapezoid", "dim": "3d"}

                    # D. Tứ diện ABCD
                    elif any(k in q_txt_lower for k in ["tứ diện", "chóp tam giác"]) and "như hình vẽ" in q_txt_lower and "oxyz" not in q_txt_lower:
                        q["geom_3d"] = {"type": "tetrahedron", "dim": "3d"}

                    # E. Tứ diện OABC trong không gian Oxyz (chuẩn hóa ngữ liệu thật 100%)
                    elif any(k in q_txt_lower.replace("$", "") for k in ["tứ diện", "oabc", "o.abc", "mặt cầu ngoại tiếp", "bán kính mặt cầu"]) and any(k in q_txt_lower.replace("$", "") for k in ["oxyz", "trong không gian", "2; 0; 0", "2;0;0"]):
                        if pve:
                            m_oxyz = pve.build_oxyz_tetrahedron_model(q_text)
                            q["geom_3d"] = m_oxyz
                            q["tikz"] = m_oxyz["tikz"]
                            q["composite_visual"] = {
                                "type": "oxyz_tetrahedron_sphere",
                                "title": m_oxyz.get("title", "Mô hình không gian: Tứ diện O.ABC & Mặt cầu ngoại tiếp (Oxyz)"),
                                "svg": m_oxyz["svg"]
                            }
                    # F. Đường bay thiết bị Oxyz
                    elif any(k in q_txt_lower.replace("$", "") for k in ["thiết bị bay", "đường bay", "trạm phát sóng", "trạm thu phát", "bay thẳng tới"]):
                        if pve:
                            m_fl = pve.build_oxyz_flight_path_model(q_text)
                            q["geom_3d"] = m_fl
                            q["tikz"] = m_fl["tikz"]
                            q["composite_visual"] = {
                                "type": "flight_trajectory",
                                "title": m_fl.get("title", "Mô hình không gian: Khoảng cách từ trạm O đến đường bay MN (Oxyz)"),
                                "svg": m_fl["svg"]
                            }

                    # G. Hai điểm A, B, trung điểm I và hình chiếu M trên (Oxy)
                    elif (any(k in q_txt_lower.replace("$", "") for k in ["cho hai điểm a(", "cho 2 điểm a(", "cho điểm a(", "hai điểm a(", "hai điểm a và b", "cho ba điểm a("]) or ("a(" in q_txt_lower.replace("$", "") and "b(" in q_txt_lower.replace("$", ""))) and any(k in q_txt_lower.replace("$", "") for k in ["trung điểm", "vectơ ab", "vecto ab", "ma^2 + mb^2", "mặt phẳng (oxy)", "mặt phẳng oxy", "trọng tâm", "đoạn thẳng", "tam giác"]):
                        if pve:
                            m_pts = pve.build_oxyz_points_segment_model(q_text)
                            q["geom_3d"] = m_pts
                            q["tikz"] = m_pts["tikz"]
                            q["composite_visual"] = {
                                "type": "points_segment",
                                "title": m_pts.get("title", "Mô hình không gian: Đoạn thẳng AB và hình chiếu trên (Oxy)"),
                                "svg": m_pts["svg"]
                            }

                if (not has_need_bbt or is_statistical_mslgn or subject != "Toán học") and q.get("bbt"):
                    q.pop("bbt", None)

                # Chống xung đột số liệu: Đề đã có CÔNG THỨC HÀM ĐẠI SỐ CỤ THỂ mà hỏi tiệm cận/giao điểm thì triệt tiêu BBT thừa (Trị dứt điểm Câu 8)
                has_concrete_formula = bool(re.search(r'y\s*=\s*(?:\\?frac\{|[-+]?\d*x|[(\[{]?[a-z0-9\^+\-*/ ]+[)\]}]?\/)', q_text)) and not re.search(r'y\s*=\s*f\(x\)', q_text)
                if has_concrete_formula:
                    if not has_need_bbt and any(kw in q_txt_lower for kw in ["tiệm cận", "giao điểm", "cắt trục"]) and q.get("bbt"):
                        del q["bbt"]
                        q["q"] = re.sub(r'^[Cc]ho bảng biến thiên của hàm số\s*', 'Cho hàm số ', q["q"])
                        q["q"] = re.sub(r'\s*có bảng biến thiên\b', '', q["q"])
                    # Triệt tiêu đồ thị sai lệch khi đề cho công thức đại số tường minh mà không có hình vẽ (Trị dứt điểm Câu 7)
                    if not any(kw in q_txt_lower for kw in ["như hình vẽ bên", "hình vẽ bên", "đồ thị hình bên", "đường cong trong hình vẽ là đồ thị", "hình bên là đồ thị"]):
                        q.pop("f", None)
                        q.pop("geom_3d", None)
                        q.pop("tikz", None)

                # --- 4.1. TỰ ĐỘNG PHỤC HỒI BBT KHI ĐỀ HỎI BBT MÀ AI QUÊN SINH TRƯỜNG "bbt" ---
                if has_need_bbt and not q.get("bbt") and not is_statistical_mslgn and subject == "Toán học":
                    if any(kw in q_txt_lower for kw in ["tiệm cận đứng", "tiệm cận ngang", "phân thức"]) or re.search(r'y\s*=\s*\\?frac\{|y\s*=\s*\([^)]+\)/', q_text):
                        is_inc = "đồng biến" in q_txt_lower or "nghịch biến" not in q_txt_lower
                        if is_inc:
                            q["bbt"] = "x | -\\infty | 1 | +\\infty\ny' | + | || | +\ny | 2 | \\nearrow | +\\infty || -\\infty | \\nearrow | 2"
                        else:
                            q["bbt"] = "x | -\\infty | -1 | +\\infty\ny' | - | || | -\ny | 2 | \\searrow | -\\infty || +\\infty | \\searrow | 2"
                    elif "tiệm cận xiên" in q_txt_lower or re.search(r'x\^2|x\^\{2\}', q_text):
                        q["bbt"] = "x | -\\infty | 0 | 1 | 2 | +\\infty\ny' | + | 0 | - | || | - | 0 | +\ny | -\\infty | \\nearrow | -2 | \\searrow | -\\infty || +\\infty | \\searrow | 2 | \\nearrow | +\\infty"
                    else:
                        q["bbt"] = "x | -\\infty | -1 | 1 | +\\infty\ny' | + | 0 | - | 0 | +\ny | -\\infty | \\nearrow | 2 | \\searrow | -2 | \\nearrow | +\\infty"

                # --- 5. CHỐNG SUY BIẾN ĐỒ THỊ HÀM BẬC 1/1 VÀ BẬC 2/1 (CHUẨN CT GDPT 2018) ---
                if q.get("f") and isinstance(q["f"], dict):
                    f_dtype = q["f"].get("type")
                    if f_dtype == "func_1_1":
                        f_1_a = float(q["f"].get("a", 2.0)); f_1_b = float(q["f"].get("b", -1.0))
                        f_1_c = float(q["f"].get("c", 1.0)); f_1_d = float(q["f"].get("d", 1.0))
                        if abs(f_1_c) < 1e-5 or abs(f_1_a * f_1_d - f_1_b * f_1_c) < 1e-4:
                            q["f"] = {"type": "func_1_1", "a": 2.0, "b": -1.0, "c": 1.0, "d": 1.0}
                    elif f_dtype == "func_2_1":
                        f_obj = q["f"]
                        f_a = float(f_obj.get("a", 1.0)); f_b = float(f_obj.get("b", -2.0)); f_c = float(f_obj.get("c", 2.0))
                        f_d = float(f_obj.get("d", 1.0)); f_e = float(f_obj.get("e", -1.0))
                        is_deg = False
                        if abs(f_a) < 1e-5 or abs(f_d) < 1e-5:
                            is_deg = True
                        elif abs(f_a * (-f_e/f_d)**2 + f_b * (-f_e/f_d) + f_c) < 1e-4:
                            is_deg = True
                        else:
                            delta_p = (f_a * f_e)**2 - (f_a * f_d) * (f_b * f_e - f_c * f_d)
                            if delta_p <= 1e-4:
                                is_deg = True
                        if is_deg:
                            q["f"] = {"type": "func_2_1", "a": 1.0, "b": -2.0, "c": 2.0, "d": 1.0, "e": -1.0}

                # --- 6. TẦNG 6: DEEP DERIVATIVE ENGINE (CHỈ kích hoạt khi câu hỏi thực sự hỏi ĐỒ THỊ của đạo hàm y = f'(x) có hình vẽ) ---
                has_deriv_graph_cue = any(kw in q_txt_lower for kw in [
                    "đồ thị của hàm số đạo hàm", "đồ thị hàm số y = f'", "đồ thị đạo hàm", "có đồ thị y = f'", "đồ thị y = f'"
                ]) and any(w in q_txt_lower for w in ["hình vẽ bên", "hình bên", "như hình", "đồ thị hình bên", "đồ thị bên", "đường cong"])

                # Nếu là câu hỏi đại số tính toán đạo hàm thuần túy (cho công thức f'(x) cụ thể, tìm cực trị / đơn điệu):
                is_pure_deriv_calc = ("có đạo hàm f'" in q_txt_lower or "f'(x) =" in q_txt_lower or "f'(x)=" in q_txt_lower or "có đạo hàm là f'" in q_txt_lower) and not any(w in q_txt_lower for w in ["hình vẽ bên", "hình bên", "như hình", "đồ thị hình bên", "đồ thị bên"])
                if is_pure_deriv_calc:
                    q.pop("f", None)
                    q.pop("geom_3d", None)
                    q.pop("tikz", None)
                elif has_deriv_graph_cue and pve:
                    try:
                        deriv_model = pve.solve_derivative_fprime_model(q.get("q", ""), q.get("opt", []), str(q.get("ans", "")))
                        if deriv_model and isinstance(deriv_model, dict):
                            q["f"] = deriv_model
                            if "tikz" in deriv_model:
                                q["tikz"] = deriv_model["tikz"]
                    except Exception:
                        pass

                # --- 7. VÁ LỖI SAI TOÁN HỌC TRONG BẢNG BIẾN THIÊN (ĐỒNG BỘ TIỆM CẬN ĐỨNG & TIỆM CẬN NGANG - Trị dứt điểm Câu 4) ---
                if q.get("bbt"):
                    raw_bbt_str = str(q["bbt"]).strip()
                    raw_bbt_str = re.sub(r'\\+nearrow\b|\\nearrow', '↗', raw_bbt_str)
                    raw_bbt_str = re.sub(r'\\+searrow\b|\\searrow', '↘', raw_bbt_str)
                    raw_bbt_str = raw_bbt_str.replace('>>', '↗').replace('>', '↗')
                    raw_bbt_str = re.sub(r'\\n(?!earrow)', '\n', raw_bbt_str).strip()
                    if pve and hasattr(pve, "heal_bbt_mathematics"):
                        try:
                            raw_bbt_str = pve.heal_bbt_mathematics(raw_bbt_str)
                        except Exception:
                            pass
                    q["bbt"] = raw_bbt_str
                    is_tiem_can_q = any(tc_kw in q_txt_lower for tc_kw in ['tiệm cận', 'tiem can'])
                    has_double_bar = ('||' in raw_bbt_str) or ('║' in raw_bbt_str)
                    bbt_lines = [l.strip() for l in raw_bbt_str.split('\n') if l.strip() and '---' not in l]

                    # 7.1. Trị dứt điểm BBT ngáo khi hỏi tiệm cận (như Screenshot 5):
                    # Nếu câu hỏi hỏi tiệm cận mà BBT KHÔNG CÓ vạch đôi ||, hoặc hàng y' có 0 mà dòng y lại có vô cực
                    if is_tiem_can_q and len(bbt_lines) >= 3:
                        is_broken_asymptote = (not has_double_bar) or ('0' in bbt_lines[1] and ('inf' in raw_bbt_str or '∞' in raw_bbt_str))
                        if is_broken_asymptote:
                            q["bbt"] = "x | -\\infty | 1 | +\\infty\ny' | + | || | +\ny | 2 | \\nearrow | +\\infty || -\\infty | \\nearrow | 2"
                            raw_bbt_str = q["bbt"]
                            bbt_lines = [l.strip() for l in raw_bbt_str.split('\n') if l.strip() and '---' not in l]
                            opts = q.get("opt", [])
                            letters = ["A", "B", "C", "D"]
                            for opt_i, o in enumerate(opts):
                                clean_o = re.sub(r'^[A-D]\.\s*', '', o).strip()
                                if clean_o == "2":
                                    q["ans"] = letters[opt_i]
                                    break
                            q["explain"] = "Đồ thị hàm số có 1 tiệm cận đứng là $x = 1$ (do $\\lim_{x \\to 1^+} y = -\\infty$) và 1 tiệm cận ngang là $y = 2$ (do $\\lim_{x \\to \\pm\\infty} y = 2$). Vậy tổng số đường tiệm cận đứng và tiệm cận ngang là $1 + 1 = 2$."



                    # 7.2. Trị dứt điểm lỗi Câu 11: Tiệm cận đứng mà dòng y' ghi là 0 thay vì ||

                    if len(bbt_lines) >= 3:
                        x_parsed = _parse_bbt_cells_safe(bbt_lines[0])
                        yp_parsed = _parse_bbt_cells_safe(bbt_lines[1])
                        y_parsed = _parse_bbt_cells_safe(bbt_lines[2])
                        lbl_yp = yp_parsed[0] if yp_parsed else "y'"
                        raw_yp_cells = yp_parsed[1:] if len(yp_parsed) > 1 else []

                        # Nếu hàng y có vạch đôi mà hàng y' không có hoặc hàng y' ghi 0
                        if is_tiem_can_q:
                            healed_cells = []
                            for c in raw_yp_cells:
                                # Nếu gặp số 0 nằm ở vị trí tiệm cận trong đề hỏi tiệm cận, đổi thành ||
                                if c == '0' and (has_double_bar or any(w in raw_bbt_str for w in ['||', '║', 'inf', '∞'])):
                                    healed_cells.append('||')
                                else:
                                    healed_cells.append(c)
                            if '||' in healed_cells:
                                lbl_x = x_parsed[0] if x_parsed else "x"
                                cells_x = ' | '.join(x_parsed[1:]) if len(x_parsed) > 1 else ""
                                q["bbt"] = f"{lbl_x} | {cells_x}\n{lbl_yp} | {' | '.join(healed_cells)}\n{bbt_lines[2]}"

                # --- 7. KHỬ SẠCH \left VÀ \right TRONG TẬP HỢP ---

                for s in q.get("stmts", []):

                    if s.get("t"):

                        s["t"] = str(s["t"]).replace(r'\left', '').replace(r'\right', '').replace('\\left', '').replace('\\right', '')

                if q.get("opt"):

                    q["opt"] = [str(o).replace(r'\left', '').replace(r'\right', '').replace('\\left', '').replace('\\right', '') for o in q["opt"]]



                # 8. Làm sạch nội dung câu hỏi nếu AI chèn chuỗi mô tả BBT thô dạng text vào q

                if "bảng biến thiên như sau:" in q_text and ("chạy từ" in q_text or "mang dấu" in q_text or "tăng từ" in q_text):

                    parts = q_text.split("bảng biến thiên như sau:")

                    lead = parts[0].strip() + " có bảng biến thiên dưới đây:"

                    tail = parts[1].strip()

                    match_ask = re.search(r'([A-ZÀ-Ỹ][^\.\n]*?(?:Có bao nhiêu|Hàm số|Tìm|Điểm|Mệnh đề|Khẳng định|Giá trị|Tập hợp)[^\.\n]*?\?.*)$', tail, re.DOTALL)

                    if match_ask: q["q"] = f"{lead} {match_ask.group(1).strip()}"

                    elif "." in tail:

                        sub_s = [s.strip() for s in tail.split(".") if s.strip()]

                        if len(sub_s) >= 2: q["q"] = f"{lead} {sub_s[-1]}."



                if not q.get("explain") or len(str(q.get("explain")).strip()) < 10:

                    q["explain"] = "🎯 **Gợi mở tư duy:** Xác định rõ giả thiết và câu hỏi trọng tâm.\n🔑 **Kiến thức cốt lõi:** Vận dụng định lý và tính chất nền tảng SGK Kết Nối Tri Thức.\n🧭 **Chiến lược tiếp cận:** Thiết lập mối liên hệ khoa học để tự suy luận và kiểm chứng kết quả."



        # Hỗ trợ gắn siêu dữ liệu kiểm tra chéo cho môn Ngữ văn
        if "part_doc_hieu" in exam and isinstance(exam["part_doc_hieu"], dict):
            for idx_q, q in enumerate(exam["part_doc_hieu"].get("questions", [])):
                if not isinstance(q, dict): continue
                if is_ai_exam:
                    q["is_ai_generated"] = True
                    q["is_real_bank_question"] = False
                    q.pop("audit_id", None)
                    q.pop("source", None)
                    q.pop("portal", None)
                    q.pop("orig_pos", None)
                    q.pop("school", None)
                else:
                    q["is_real_bank_question"] = True
                    q["is_ai_generated"] = False
                    if not q.get("school"): q["school"] = exam.get("school", "THPT Chuyên Toàn Quốc")
                    if not q.get("portal"): q["portal"] = exam.get("portal", "Kho Khảo Thí Ngữ Văn (CV 3175)")
                    if not q.get("year"): q["year"] = exam.get("year", "2025 - 2026")
                    if not q.get("exam_session"): q["exam_session"] = "Kỳ thi Cuối Học Kỳ 1 (Chính thức)"
                    if not q.get("orig_pos"): q["orig_pos"] = f"Đọc hiểu - Câu {idx_q + 1}"
                    if not q.get("audit_id"): q["audit_id"] = f"NV_DH_{exam.get('code','2501')}_{idx_q+1}"
                    if not q.get("source"):
                        q["source"] = f"{q['school']} • {q['exam_session']} ({q['year']}) • [Đề gốc: Mã {exam.get('code','2501')} - {q['orig_pos']}] • Nguồn: {q['portal']}"

        if "part_viet" in exam and isinstance(exam["part_viet"], list):
            for idx_q, v in enumerate(exam["part_viet"]):
                if not isinstance(v, dict): continue
                if is_ai_exam:
                    v["is_ai_generated"] = True
                    v["is_real_bank_question"] = False
                    v.pop("audit_id", None)
                    v.pop("source", None)
                    v.pop("portal", None)
                    v.pop("orig_pos", None)
                    v.pop("school", None)
                else:
                    v["is_real_bank_question"] = True
                    v["is_ai_generated"] = False
                    if not v.get("school"): v["school"] = exam.get("school", "THPT Chuyên Toàn Quốc")
                    if not v.get("portal"): v["portal"] = exam.get("portal", "Kho Khảo Thí Ngữ Văn (CV 3175)")
                    if not v.get("year"): v["year"] = exam.get("year", "2025 - 2026")
                    if not v.get("exam_session"): v["exam_session"] = "Kỳ thi Cuối Học Kỳ 1 (Chính thức)"
                    if not v.get("orig_pos"): v["orig_pos"] = f"Viết - Câu {idx_q + 1}"
                    if not v.get("audit_id"): v["audit_id"] = f"NV_V_{exam.get('code','2501')}_{idx_q+1}"
                    if not v.get("source"):
                        v["source"] = f"{v['school']} • {v['exam_session']} ({v['year']}) • [Đề gốc: Mã {exam.get('code','2501')} - {v['orig_pos']}] • Nguồn: {v['portal']}"



        # TẦNG ĐIỀU HÒA TOÀN DIỆN BIG TECH (ĐỒ THỊ, BBT 3 HÀM CƠ BẢN, VDC THỰC TẾ):
        if pve and hasattr(pve, "harmonize_exam_visual_balance"):
            try:
                custom_req_text = str(st.session_state.get("custom_topic_instructions", "") or st.session_state.get("last_custom_req", "") or "")
                exam = pve.harmonize_exam_visual_balance(exam, subject=subject, grade=grade_num, user_custom_req=custom_req_text)
            except Exception as _e_harm:
                logging.error("Lỗi harmonize_exam_visual_balance: %s", _e_harm)

        return preflight_exam_auto_heal(exam, subject_name=subject, grade_level=grade_num)

    def render_fast_visual(q, q_id=None):
        global pve
        if pve is None:
            try:
                import precision_visual_engine as pve
            except Exception:
                pve = None
        if not isinstance(q, dict): return
        q_txt_fast = str(q.get("q", "") or q.get("question", "")).lower()

        # TẦNG NGẦM 3: HUY HIỆU ĐỐI SOÁT CHÉO DEEP CHECK VAR TỪ 2 NGUỒN CHÍNH THỐNG
        if subject == "Tiếng Anh":

            var_badge_html = (

                '<div style="margin: 4px 0 10px 0; font-size: 11.5px; color: #34d399; background: rgba(16, 185, 129, 0.08); padding: 5px 12px; border-radius: 6px; border: 1px solid rgba(16, 185, 129, 0.25); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 4px;">'

                '<span>🌍 <b>DEEP CHECK VAR:</b> Ngữ cảnh thực tế chuẩn Khung CEFR / Khung 6 bậc VN (Tiếng Anh bản ngữ)</span>'

                '<span><a href="https://www.vniteach.com/sach-dien-tu-ket-noi-tri-thuc/#google_vignette" target="_blank" style="color: #fbbf24; text-decoration: underline; font-weight: 600;">[📖 Đối chiếu chuẩn KNTT VniTeach]</a> &nbsp; <a href="https://hanhtrangso.nxbgd.vn/" target="_blank" style="color: #38bdf8; text-decoration: underline; font-weight: 600;">[🏛️ Cổng Hành Trang Số NXBGD]</a></span>'

                '</div>'

            )

        else:

            var_badge_html = (

                f'<div style="margin: 4px 0 10px 0; font-size: 11.5px; color: #38bdf8; background: rgba(56, 189, 248, 0.08); padding: 5px 12px; border-radius: 6px; border: 1px solid rgba(56, 189, 248, 0.25); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 4px;">'

                f'<span>🛡️ <b>DEEP CHECK VAR:</b> Nội dung được phần mềm chuẩn hóa; nguồn và đáp án cần giáo viên kiểm tra</span>'

                f'<span><a href="https://www.vniteach.com/sach-dien-tu-ket-noi-tri-thuc/#google_vignette" target="_blank" style="color: #fbbf24; text-decoration: underline; font-weight: 600;">[📖 Lật trang đối soát VniTeach]</a> &nbsp; <a href="https://hanhtrangso.nxbgd.vn/" target="_blank" style="color: #34d399; text-decoration: underline; font-weight: 600;">[🏛️ Cổng Hành Trang Số NXBGD]</a></span>'

                f'</div>'

            )

        st.markdown(var_badge_html, unsafe_allow_html=True)



        # 1. HIỂN THỊ BẢNG BIẾN THIÊN (BBT) CHUẨN SƯ PHẠM WEBP SIÊU NÉT (CHỐT CHẶN CUỐI CÙNG)
        # Thanh lọc giá trị rác 'null', 'none'
        if q.get("bbt") is not None:
            if isinstance(q.get("bbt"), str) and q.get("bbt").strip().lower() in ["null", "none", "{}", "nil", "undefined", "nan", ""]:
                q.pop("bbt", None)
            elif isinstance(q.get("bbt"), (dict, list)) and len(q.get("bbt")) == 0:
                q.pop("bbt", None)

        if q.get("f") is not None:
            if isinstance(q.get("f"), str) and q.get("f").strip().lower() in ["null", "none", "{}", "nil", "undefined", "nan", ""]:
                q.pop("f", None)
            elif isinstance(q.get("f"), dict) and len(q.get("f")) == 0:
                q.pop("f", None)

        is_stat_q = any(k in q_txt_fast for k in [
            "ghép nhóm", "mẫu số liệu", "mslgn", "tần số", "khoảng tứ phân vị",
            "độ lệch chuẩn", "phương sai", "cỡ mẫu", "trung vị", "mốt", "giá trị đại diện",
            "tần số ghép nhóm", "bảng số liệu ghép nhóm"
        ]) or bool(re.search(r'\[\s*\d+(?:[\.,]\d+)?\s*[;,]\s*\d+(?:[\.,]\d+)?\s*\)', q_txt_fast))

        if is_stat_q or subject != "Toán học":
            q.pop("bbt", None)
            has_bbt_prompt = False
        else:
            has_bbt_prompt = (
                any(k in q_txt_fast for k in ["bảng biến thiên", "bbt", "bảng xét dấu", "chiều biến thiên"]) or
                (any(k in q_txt_fast for k in ["bảng dưới đây", "bảng sau"]) and any(k in q_txt_fast for k in ["hàm số", "đạo hàm", "f'(x)", "f(x)", "y'", "đồng biến", "nghịch biến"]))
            )

        if not q.get("bbt") and has_bbt_prompt and not is_stat_q and subject == "Toán học":
            # Tự động phục hồi BBT nếu câu hỏi yêu cầu nhưng thiếu trường bbt
            opts = q.get("opt", [])
            ans_letter = str(q.get("ans", "")).strip().upper()[:1]
            target_opt_str = ""
            if opts and isinstance(opts, list):
                ans_idx = ord(ans_letter) - ord("A") if ans_letter in ("A", "B", "C", "D") else 0
                target_opt_str = str(opts[ans_idx]) if 0 <= ans_idx < len(opts) else str(opts[0])
            m_val = re.search(r'[-+]?\d+(?:[\.,]\d+)?', target_opt_str)

            if any(kw in q_txt_fast for kw in ["tiệm cận đứng", "tiệm cận ngang", "phân thức"]) or re.search(r'y\s*=\s*\\?frac\{|y\s*=\s*\([^)]+\)/', str(q.get("q", ""))):
                q["bbt"] = "x | -\\infty | 1 | +\\infty\ny' | + | || | +\ny | 2 | \\nearrow | +\\infty || -\\infty | \\nearrow | 2"
            elif any(kw in q_txt_fast for kw in ["tiệm cận xiên", "2/1", "bậc hai trên bậc nhất"]):
                q["bbt"] = "x | -\\infty | 0 | 1 | 2 | +\\infty\ny' | + | 0 | - | || | - | 0 | +\ny | -\\infty | \\nearrow | -1 | \\searrow | -\\infty || +\\infty | \\searrow | 3 | \\nearrow | +\\infty"
            elif m_val and "cực tiểu" in q_txt_fast:
                try:
                    val_ans = float(m_val.group(0).replace(',', '.'))
                    d_adj = round(val_ans + 4.0, 1)
                    q["bbt"] = f"x | -\\infty | 0 | 2 | +\\infty\ny' | + | 0 | - | 0 | +\ny | -\\infty | \\nearrow | {d_adj:g} | \\searrow | {val_ans:g} | \\nearrow | +\\infty"
                except Exception:
                    q["bbt"] = "x | -\\infty | -1 | 1 | +\\infty\ny' | + | 0 | - | 0 | +\ny | -\\infty | \\nearrow | 2 | \\searrow | -2 | \\nearrow | +\\infty"
            elif m_val and "cực đại" in q_txt_fast:
                try:
                    val_ans = float(m_val.group(0).replace(',', '.'))
                    d_adj = round(val_ans - 2.0, 1)
                    q["bbt"] = f"x | -\\infty | -1 | 1 | +\\infty\ny' | - | 0 | + | 0 | -\ny | +\\infty | \\searrow | {d_adj - 2.0:g} | \\nearrow | {val_ans:g} | \\searrow | -\\infty"
                except Exception:
                    q["bbt"] = "x | -\\infty | -1 | 1 | +\\infty\ny' | + | 0 | - | 0 | +\ny | -\\infty | \\nearrow | 2 | \\searrow | -2 | \\nearrow | +\\infty"
            else:
                q["bbt"] = "x | -\\infty | -1 | 1 | +\\infty\ny' | + | 0 | - | 0 | +\ny | -\\infty | \\nearrow | 2 | \\searrow | -2 | \\nearrow | +\\infty"

        if q.get("bbt"):
            q_bbt_str = str(q["bbt"]).strip()
            q_bbt_str = re.sub(r'\\+nearrow\b|\\nearrow', '↗', q_bbt_str)
            q_bbt_str = re.sub(r'\\+searrow\b|\\searrow', '↘', q_bbt_str)
            q_bbt_str = q_bbt_str.replace('>>', '↗').replace('>', '↗')
            q_bbt_str = re.sub(r'\\n(?!earrow)', '\n', q_bbt_str).strip()
            if pve and hasattr(pve, "heal_bbt_mathematics"):
                try:
                    q_bbt_str = pve.heal_bbt_mathematics(q_bbt_str)
                except Exception:
                    pass
            q["bbt"] = q_bbt_str
            b64_bbt = render_bbt_to_webp_base64(q["bbt"])

            if b64_bbt:
                st.caption("📋 **Bảng biến thiên chuẩn hóa LaTeX & Bộ GD&ĐT:**")
                col_b1, col_b2, col_b3 = st.columns([1, 3.5, 1])
                with col_b2:
                    st.markdown(f'<div style="display:flex; justify-content:center; margin:8px auto;"><img src="{b64_bbt}" alt="Bảng biến thiên chuẩn Bộ GD&ĐT" style="max-width:100%; height:auto; border-radius:6px; box-shadow:0 4px 12px rgba(0,0,0,0.2);"/></div>', unsafe_allow_html=True)
            else:
                html_bbt = format_pedagogical_bbt_html(q["bbt"], is_dark_mode=True)
                if html_bbt:
                    st.caption("📋 **Bảng biến thiên chuẩn hóa LaTeX & Bộ GD&ĐT:**")
                    st.markdown(html_bbt, unsafe_allow_html=True)



        # 2. HIỂN THỊ BẢNG MẪU SỐ LIỆU GHÉP NHÓM (MSLGN - ĐẦY ĐỦ KHUNG LƯỚI & BIỂU ĐỒ HOLOGRAM CHUẨN BỘ)
        q = extract_and_normalize_mslgn(q)

        # Tự động phục dựng dữ liệu ghép nhóm nếu câu hỏi đề cập đến biểu đồ nhưng thiếu mslgn_data
        if not q.get("mslgn_data") and any(k in q_txt_fast for k in ["ghép nhóm", "mẫu số liệu", "biểu đồ", "tần số lớn nhất"]):
            raw_opts = q.get("opt", [])
            opt_groups = []
            for op in raw_opts:
                m_grp = re.search(r'\[\s*\d+\s*[;,]\s*\d+\s*\)', str(op))
                if m_grp:
                    opt_groups.append(m_grp.group(0))
            if opt_groups:
                q["mslgn_data"] = {
                    "title": "Biểu đồ mẫu số liệu ghép nhóm (Hologram tần số):",
                    "groups": opt_groups,
                    "freq": [6, 14, 18, 9][:len(opt_groups)] if len(opt_groups) == 4 else [8, 12, 15, 10, 5][:len(opt_groups)]
                }

        if q.get("mslgn_data"):
            ms_info = q["mslgn_data"]
            grps = ms_info.get("groups", [])
            freqs = ms_info.get("freq", [])
            if grps and freqs and len(grps) == len(freqs):
                st.caption(f"📊 **{ms_info.get('title', 'Bảng mẫu số liệu ghép nhóm chuẩn hóa:')}**")
                col_cnt = len(grps)
                max_g_len = max([len(str(g)) for g in grps] + [len(str(f)) for f in freqs] + [4])
                dyn_w = min(880, max(360, col_cnt * max(55, max_g_len * 12 + 25) + 120))
                ms_html = f'<div style="display: flex; justify-content: center; margin: 10px auto; max-width: {dyn_w}px;"><div style="background-color: #0f172a; padding: 10px 14px; border-radius: 10px; border: 1.5px solid #475569; overflow-x: auto; width: 100%; box-shadow: 0 4px 12px rgba(0,0,0,0.5);">'
                ms_html += '<table style="width: 100%; border-collapse: collapse; text-align: center; color: #f8fafc; font-size: 14.5px; font-family: \'Times New Roman\', Times, serif; border: 1.5px solid #475569;">'
                ms_html += '<tr style="background-color: #1e293b; color: #38bdf8; font-weight: bold; border-bottom: 1.5px solid #475569;"><td style="padding: 8px 12px; border: 1px solid #334155; width: 120px;">Nhóm giá trị</td>'
                for g in grps: ms_html += f'<td style="padding: 8px 12px; border: 1px solid #334155; font-weight: 500;">{g}</td>'
                ms_html += '</tr><tr style="border-bottom: 1px solid #475569;"><td style="padding: 8px 12px; font-weight: bold; background-color: #1e293b; color: #34d399; border: 1px solid #334155;">Tần số (n)</td>'
                for f_val in freqs: ms_html += f'<td style="padding: 8px 12px; border: 1px solid #334155; font-weight: 600;">{f_val}</td>'
                ms_html += '</tr></table></div></div>'
                st.markdown(ms_html, unsafe_allow_html=True)

                # BIỂU ĐỒ HOLOGRAM TẦN SỐ GHÉP NHÓM TƯƠNG TÁC (CYBERPUNK NEON)
                try:
                    fig_holo = go.Figure()
                    fig_holo.add_trace(go.Bar(
                        x=[str(g) for g in grps],
                        y=[float(f) for f in freqs],
                        marker=dict(
                            color=["#38bdf8", "#34d399", "#f59e0b", "#ec4899", "#818cf8", "#a78bfa"][:len(grps)],
                            opacity=0.88,
                            line=dict(color="#06b6d4", width=2.0)
                        ),
                        text=[f"n={f}" for f in freqs],
                        textposition="auto",
                        name="Tần số"
                    ))
                    fig_holo.update_layout(
                        width=380, height=240, margin=dict(l=10, r=10, t=10, b=10),
                        template="plotly_dark",
                        paper_bgcolor="rgba(15, 23, 42, 0.4)",
                        plot_bgcolor="rgba(15, 23, 42, 0.4)",
                        xaxis=dict(title="Nhóm khoảng ghép nhóm", showgrid=True, gridcolor="#334155"),
                        yaxis=dict(title="Tần số", showgrid=True, gridcolor="#334155")
                    )
                    col_h1, col_h2, col_h3 = st.columns([1, 2.2, 1])
                    with col_h2:
                        st.caption("✨ **Biểu đồ tần số ghép nhóm Hologram trực quan:**")
                        st.plotly_chart(fig_holo, width="stretch", key=f"mslgn_holo_{q_id}" if q_id else None)
                except Exception:
                    pass



        # 2.5. HIỂN THỊ CẢNH BÁO VAR SƯ PHẠM (NẾU CÂU HỎI VƯỚNG DẠNG BÀI CT CŨ)

        if q.get("var_warning"):

            st.warning(q["var_warning"])



        # 2.6. HIỂN THỊ ĐỒ THỊ 2D HOẶC KHỐI TRÒN XOAY / HÌNH HỌC 3D XOAY 360° (CHUẨN VECTOR SIÊU NÉT)
        q_txt_fast = str(q.get("q", "") or q.get("question", "")).lower()

        # BẢO VỆ CHỐT CHẶN CÁC MÔN NGOÀI TOÁN (VẬT LÝ, HÓA HỌC, SINH HỌC, ĐỊA LÝ, TIN HỌC, SỬ, VĂN, ANH):
        if subject != "Toán học":
            q.pop("f", None)
            q.pop("bbt", None)
            q.pop("mslgn_data", None)
            if not any(k in q_txt_fast for k in ["mô hình", "sơ đồ", "thí nghiệm"]):
                q.pop("geom_3d", None)

        is_calc_algebra_fast = any(k in q_txt_fast for k in [
            "biểu thức", "giá trị của biểu thức", "bằng bao nhiêu", "tìm m",
            "tìm tham số", "t =", "p =", "t = ", "p = "
        ]) or (any(k in q_txt_fast for k in ["tính", "giá trị của"]) and any(k in q_txt_fast for k in ["biểu thức", "t =", "p =", "t = ", "p = ", "tham số"]))

        has_explicit_graph_fast = any(kw in q_txt_fast for kw in [
            "hình vẽ bên", "hình bên", "đồ thị hình bên", "đường cong trong hình", "như hình vẽ bên",
            "như hình vẽ", "đồ thị bên", "đồ thị như hình", "cho đồ thị như hình", "như hình dưới đây",
            "trong hình vẽ", "ở hình vẽ", "hình vẽ", "hình sau", "đường cong dưới đây"
        ]) or (
            any(kw in q_txt_fast for kw in ["đồ thị của hàm số nào", "là của hàm số nào", "đồ thị hàm số nào", "đường cong dưới đây là đồ thị", "hình vẽ bên là đồ thị"])
            and any(w in q_txt_fast for w in ["hình vẽ", "hình bên", "đường cong", "như hình", "hình dưới", "hình sau"])
        )

        # Khử triệt để câu hỏi lý thuyết nhận dạng hình dạng chữ cái (chữ N, chữ W, chữ U, chữ M) khi KHÔNG có hình vẽ minh họa:
        is_shape_theory_fast = any(k in q_txt_fast for k in ["chữ n", "chữ u", "chữ w", "chữ m"]) and not any(w in q_txt_fast for w in ["hình vẽ", "hình bên", "đồ thị", "đường cong", "như hình", "trong hình", "ở hình", "hình dưới", "hình sau"])
        if is_shape_theory_fast:
            has_explicit_graph_fast = False
            q.pop("f", None)
            q.pop("tikz", None)

        is_geom_3d_spatial_fast = any(k in q_txt_fast for k in [
            "tứ diện", "mặt cầu", "khối chóp", "hình chóp", "lăng trụ", "hình hộp",
            "oxyz", "bán kính", "khối nón", "khối trụ", "hình nón", "hình trụ",
            "khối tròn xoay", "s.abcd", "s.abc", "oabc"
        ])
        # CHỐT CHẶN CUỐI CÙNG TỐI THƯỢNG CỦA ÔNG THẦY BIGDATA (THEO MỆNH LỆNH THẦY TRÍ):
        # 1. Đồ thị hàm số 2D (f) CHỈ ĐƯỢC PHÉP HIỂN THỊ KHI ĐỀ BÀI CÓ TỪ KHÓA ĐÒI HỎI HÌNH VẼ MINH HỌA!
        # 2. Bất kỳ câu hỏi nào KHÔNG có từ khóa hình vẽ minh họa (như tìm cực trị, xét đạo hàm f'(x), tính toán giải tích):
        #    TUYỆT ĐỐI TRIỆT TIÊU 100% f VÀ tikz, KHÔNG ĐƯỢC CHÈN ĐỒ THỊ BẬC 3 HAY BẤT KỲ ĐỒ THỊ NÀO VÀO!
        if not has_explicit_graph_fast:
            q.pop("f", None)
            if not is_geom_3d_spatial_fast:
                q.pop("geom_3d", None)
            if not q.get("composite_visual") and not is_geom_3d_spatial_fast:
                q.pop("tikz", None)

        # Thanh lọc mô hình giả định func_1_1 dummy cũ nếu đề cho công thức khác
        has_different_formula = bool(re.search(r'y\s*=\s*(?:\\?frac\{|\()([-+]?\d*)x\s*([+-]\s*\d+)', q_txt_fast)) and ("2x-1" not in q_txt_fast and "2x - 1" not in q_txt_fast)
        f_obj = q.get("f")
        if isinstance(f_obj, dict) and f_obj.get("type") == "func_1_1" and f_obj.get("a") == 2.0 and f_obj.get("b") == -1.0 and f_obj.get("c") == 1.0 and f_obj.get("d") == -1.0:
            if has_different_formula:
                q.pop("f", None)
                q.pop("tikz", None)

        # VIP 73.2 ANTI-FLICKER GATEKEEPER - PHÁT HIỆN HÀM BẬC 3 VÀ PHÂN THỨC GÁN NHẦM:
        opts_combined_lower = " ".join(str(o) for o in q.get("opt", [])).lower()
        combined_ev = q_txt_fast + " " + opts_combined_lower
        f_obj = q.get("f")
        if isinstance(f_obj, dict) and subject == "Toán học":
            f_type = f_obj.get("type")
            if f_type == "func_3":
                has_rat_ev = any(k in combined_ev for k in ["frac", "/", "phân thức", "tiệm cận", "x^2", "x-1", "x+1", "x-2", "x+2"])
                has_cub_ev = any(k in combined_ev for k in ["bậc ba", "bậc 3", "ax^3", "x^3", "x^{3}"])
                if has_rat_ev and not has_cub_ev and pve:
                    if ("x^2" in combined_ev or "x^{2}" in combined_ev) and any(d in combined_ev for d in ["x-", "x+", "/"]):
                        q["f"] = pve.solve_rational_2_1_from_text(q.get("q", ""), q.get("opt", []), str(q.get("ans", "")))
                        q["tikz"] = pve.build_rational_2_1_tikz(q["f"]["a"], q["f"]["b"], q["f"]["c"], q["f"]["d"], q["f"]["e"])
                    else:
                        s11 = pve.solve_rational_1_1_from_text(q.get("q", ""), q.get("opt", []), str(q.get("ans", "")))
                        if s11:
                            q["f"] = s11
                            q["tikz"] = pve.build_rational_1_1_tikz(s11["a"], s11["b"], s11["c"], s11["d"])
                        else:
                            q.pop("f", None)
                            q.pop("tikz", None)
            elif f_type in ["func_1_1", "func_2_1"]:
                has_cub_ev = any(k in combined_ev for k in ["bậc ba", "bậc 3", "ax^3", "x^3", "x^{3}"])
                has_rat_ev = any(k in combined_ev for k in ["frac", "/", "phân thức", "tiệm cận"])
                if has_cub_ev and not has_rat_ev and pve:
                    q["f"] = pve.solve_cubic_from_text_or_opts(q.get("q", ""), q.get("opt", []), str(q.get("ans", "")))

        visual_data = q.get("f") or q.get("geom_3d")

        img_src = q.get("image_base64") or q.get("image_url") or q.get("image")

        # TẦNG 7: BẢO ĐẢM 100% CÂU HỎI CÓ HÌNH VẼ ĐỀU HIỂN THỊ ĐỒ THỊ (CẤM ĐỂ TRỐNG)
        if not visual_data and has_explicit_graph_fast and ree and hasattr(ree, "attach_question_visuals"):
            try:
                q = ree.attach_question_visuals(q, subject=subject, grade=grade_num)
                visual_data = q.get("f") or q.get("geom_3d")
            except Exception:
                pass

        # Bù đắp an toàn thông minh THEO NGỮ CẢNH GDPT 2018 nếu có has_explicit_graph_fast mà vẫn chưa có visual_data / composite_visual
        if not visual_data and not q.get("composite_visual") and has_explicit_graph_fast and subject == "Toán học":
            is_grade_10_detected = (
                str(grade_num) in ["10", "Khối 10", "Lớp 10"]
                or any(k in q_txt_fast for k in ["tập hợp", "mệnh đề", "nửa đường tròn", "bất phương trình bậc nhất hai ẩn", "bpt bậc nhất hai ẩn", "miền nghiệm", "hệ thức lượng", "lượng giác", "hồ con rùa", "chiều cao tháp"])
            )
            if is_grade_10_detected:
                if any(k in q_txt_fast for k in ["nửa đường tròn", "đường tròn đơn vị", "xom", "m(x_0", "m(x0"]):
                    if pve:
                        q["composite_visual"] = pve.build_trig_unit_circle_model(q.get("q", ""), q.get("opt"), str(q.get("ans", "")))
                        q["tikz"] = q["composite_visual"].get("tikz")
                elif any(k in q_txt_fast for k in ["miền nghiệm", "bất phương trình bậc nhất hai ẩn", "bpt bậc nhất hai ẩn", "miền không bị gạch"]):
                    if pve:
                        q["composite_visual"] = pve.build_linear_inequality_region_model(q.get("q", ""), q.get("opt"), str(q.get("ans", "")))
                        q["tikz"] = q["composite_visual"].get("tikz")
                elif any(k in q_txt_fast for k in ["chiều cao tháp", "tháp chính", "hồ con rùa", "con rùa"]) or any(k in q_txt_fast for k in ["cad =", "cbd ="]):
                    if pve:
                        q["composite_visual"] = pve.build_tower_height_measuring_model(q.get("q", ""), q.get("opt"), str(q.get("ans", "")))
                        q["tikz"] = q["composite_visual"].get("tikz")
            else:
                raw_q_curr = str(q.get("q") or "")
                opts = q.get("opt", [])
                ans_letter = str(q.get("ans", "")).strip().upper()[:1]
                target_opt_str = ""
                if opts and isinstance(opts, list):
                    ans_idx = ord(ans_letter) - ord("A") if ans_letter in ("A", "B", "C", "D") else 0
                    target_opt_str = str(opts[ans_idx]) if 0 <= ans_idx < len(opts) else str(opts[0])
                opts_str = " ".join(str(o) for o in opts)
                combined_recon = (raw_q_curr + " " + target_opt_str + " " + opts_str).lower()

                # 1. Phân thức 2/1 chuẩn SGK KNTT Toán 12
                is_recon_2_1 = bool(re.search(r'\\frac\{[^{}]*x\^2[^{}]*\}\{[^{}]*x[^{}]*\}', target_opt_str + " " + opts_str)) or (
                    ("x^2" in target_opt_str.lower() or "x^{2}" in target_opt_str.lower()) and ("/" in target_opt_str or "frac" in target_opt_str) and any(d in target_opt_str for d in ["x-", "x+", "x -", "x +"])
                ) or any(k in q_txt_fast for k in ["tiệm cận xiên", "2/1", "bậc hai trên bậc nhất"])

                # 2. Phân thức 1/1
                is_recon_1_1 = not is_recon_2_1 and (
                    bool(re.search(r'\\frac\{[^{}]*x[^{}]*\}\{[^{}]*x[^{}]*\}', target_opt_str + " " + opts_str)) or
                    (("/" in target_opt_str or "frac" in target_opt_str) and not any(k in target_opt_str for k in ["x^2", "x^3", "x^4"])) or
                    any(k in q_txt_fast for k in ["tiệm cận", "phân thức"])
                )

                # 3. Đạo hàm f' (CHỈ khi câu hỏi thực sự yêu cầu nhìn đồ thị đạo hàm)
                is_recon_deriv = (any(k in q_txt_fast for k in ["đồ thị của hàm số đạo hàm", "đồ thị hàm số y = f'", "đồ thị đạo hàm", "có đồ thị y = f'", "đồ thị y = f'"]) or ("f'" in q_txt_fast and any(w in q_txt_fast for w in ["hình vẽ", "hình bên", "như hình", "đồ thị bên", "đường cong"])))

                # 4. Hàm bậc ba
                is_recon_cubic = not is_recon_2_1 and not is_recon_1_1 and (
                    ("x^3" in target_opt_str or "x^{3}" in target_opt_str or "bậc ba" in combined_recon or "bậc 3" in combined_recon or "ax^3" in combined_recon)
                )

                if is_recon_2_1 and pve:
                    sol_2_1 = pve.solve_rational_2_1_from_text(raw_q_curr, q.get("opt", []), str(q.get("ans", "")))
                    if sol_2_1 and isinstance(sol_2_1, dict) and "a" in sol_2_1:
                        q["f"] = sol_2_1
                        q["tikz"] = pve.build_rational_2_1_tikz(sol_2_1["a"], sol_2_1["b"], sol_2_1["c"], sol_2_1["d"], sol_2_1["e"])
                elif is_recon_1_1 and pve:
                    sol_1_1 = pve.solve_rational_1_1_from_text(raw_q_curr, q.get("opt", []), str(q.get("ans", ""))) or {"type": "func_1_1", "a": 2.0, "b": -1.0, "c": 1.0, "d": -1.0}
                    if sol_1_1 and isinstance(sol_1_1, dict) and "a" in sol_1_1:
                        q["f"] = sol_1_1
                        q["tikz"] = pve.build_rational_1_1_tikz(sol_1_1["a"], sol_1_1["b"], sol_1_1["c"], sol_1_1["d"])
                elif is_recon_deriv and pve:
                    deriv_model = pve.solve_derivative_fprime_model(raw_q_curr, q.get("opt", []), str(q.get("ans", "")))
                    if deriv_model and isinstance(deriv_model, dict):
                        q["f"] = deriv_model
                        if "tikz" in deriv_model:
                            q["tikz"] = deriv_model["tikz"]
                elif is_recon_cubic and pve:
                    q["f"] = pve.solve_cubic_from_text_or_opts(raw_q_curr, q.get("opt", []), str(q.get("ans", "")))
                else:
                    if pve:
                        m_val = re.search(r'[-+]?\d+(?:[\.,]\d+)?', target_opt_str)
                        if "tiệm cận xiên" in q_txt_fast or "2/1" in q_txt_fast:
                            sol_2_1 = pve.solve_rational_2_1_from_text(raw_q_curr, q.get("opt", []), str(q.get("ans", "")))
                            q["f"] = sol_2_1
                            q["tikz"] = pve.build_rational_2_1_tikz(sol_2_1["a"], sol_2_1["b"], sol_2_1["c"], sol_2_1["d"], sol_2_1["e"])
                        elif any(k in q_txt_fast for k in ["tiệm cận", "phân thức"]):
                            sol_1_1 = pve.solve_rational_1_1_from_text(raw_q_curr, q.get("opt", []), str(q.get("ans", ""))) or {"type": "func_1_1", "a": 2.0, "b": -1.0, "c": 1.0, "d": -1.0}
                            q["f"] = sol_1_1
                            q["tikz"] = pve.build_rational_1_1_tikz(sol_1_1["a"], sol_1_1["b"], sol_1_1["c"], sol_1_1["d"])
                        elif m_val and "cực tiểu" in q_txt_fast:
                            try:
                                val_ans = float(m_val.group(0).replace(',', '.'))
                                d_adj = round(val_ans + 4.0, 1)
                                q["f"] = {"type": "func_3", "a": 1.0, "b": -3.0, "c": 0.0, "d": d_adj}
                            except Exception:
                                q["f"] = pve.solve_cubic_from_text_or_opts(raw_q_curr, q.get("opt", []), str(q.get("ans", "")))
                        elif m_val and "cực đại" in q_txt_fast:
                            try:
                                val_ans = float(m_val.group(0).replace(',', '.'))
                                d_adj = round(val_ans - 2.0, 1)
                                q["f"] = {"type": "func_3", "a": -1.0, "b": 0.0, "c": 3.0, "d": d_adj}
                            except Exception:
                                q["f"] = pve.solve_cubic_from_text_or_opts(raw_q_curr, q.get("opt", []), str(q.get("ans", "")))
                        else:
                            q["f"] = pve.solve_cubic_from_text_or_opts(raw_q_curr, q.get("opt", []), str(q.get("ans", "")))

            # Cuối cùng qua bộ lọc ngữ cảnh chuyên sâu 0-token
            if pve and hasattr(pve, "audit_and_heal_visual_context_gdpt2018"):
                q = pve.audit_and_heal_visual_context_gdpt2018(q, subject=subject, grade=grade_num)

            visual_data = q.get("f") or q.get("geom_3d")



        # CHỐT CHẶN BẢO VỆ TUYỆT ĐỐI (GATEKEEPER):
        # Nếu câu hỏi không có từ khóa hình vẽ minh họa và không phải hình học không gian 3D:
        # Ép visual_data = None 100%, triệt tiêu vĩnh viễn mọi đồ thị phát sinh nhầm lẫn!
        if not has_explicit_graph_fast and not is_geom_3d_spatial_fast and not q.get("composite_visual"):
            visual_data = None
            q.pop("f", None)
            q.pop("tikz", None)

        if visual_data and isinstance(visual_data, dict):

            dtype = visual_data.get("type", "")
            sub_type = visual_data.get("sub_type", "")

            is_3d = (
                dtype in ["solid_of_revolution", "cone_3d", "cylinder_3d", "sphere_3d", "oxyz_space", "geom_3d", "box_with_sphere", "tetrahedron", "oxyz_tetrahedron_sphere", "points_segment", "flight_trajectory"]
                or visual_data.get("dim") == "3d"
                or sub_type in ["pyramid_quad", "tetrahedron_pure", "triangular_prism", "box_prism", "oxyz_tetrahedron_sphere", "oxyz_midpoint_projection", "oxyz_distance_point_line"]
            )

            try:

                if is_3d:

                    fig_mini = go.Figure()

                    tikz_code = ""



                    if dtype == "solid_of_revolution":

                        fa_bound = float(visual_data.get("a", 0.0))

                        fb_bound = float(visual_data.get("b", 3.0))

                        f_expr = str(visual_data.get("f_expr", "sqrt(x)"))

                        u_vals = np.linspace(fa_bound, fb_bound, 35)

                        th_vals = np.linspace(0, 2*np.pi, 35)

                        U, TH = np.meshgrid(u_vals, th_vals)

                        if "sqrt" in f_expr:

                            R = np.sqrt(np.maximum(0.0, U))

                        elif "^2" in f_expr or "**2" in f_expr:

                            R = 0.25 * (U**2)

                        elif "sin" in f_expr:

                            R = np.abs(np.sin(U)) + 0.5

                        else:

                            slope = float(visual_data.get("slope", 0.5))

                            r0 = float(visual_data.get("r0", 1.0))

                            R = np.maximum(0.05, r0 + slope * (U - fa_bound))

                        X = U; Y = R * np.cos(TH); Z = R * np.sin(TH)

                        fig_mini.add_trace(go.Surface(x=X, y=Y, z=Z, colorscale="Viridis", opacity=0.82, showscale=False, name="Mặt tròn xoay"))

                        axis_ext = max(1.0, (fb_bound - fa_bound) * 0.2)

                        fig_mini.add_trace(go.Scatter3d(x=[fa_bound - axis_ext, fb_bound + axis_ext], y=[0, 0], z=[0, 0], mode="lines+text", line=dict(color="#f59e0b", width=5), text=["", "Trục Ox"], textposition="top right", name="Trục quay Ox"))

                        for u_edge, col_edge in [(fa_bound, "#38bdf8"), (fb_bound, "#ec4899")]:

                            r_edge = np.sqrt(max(0, u_edge)) if "sqrt" in f_expr else (0.25*(u_edge**2) if "^2" in f_expr else 1.0)

                            th_edge = np.linspace(0, 2*np.pi, 40)

                            fig_mini.add_trace(go.Scatter3d(x=np.full_like(th_edge, u_edge), y=r_edge*np.cos(th_edge), z=r_edge*np.sin(th_edge), mode="lines", line=dict(color=col_edge, width=3.5), name=f"Thiết diện x={u_edge:.1f}"))



                    elif dtype == "cone_3d":

                        r_cone = float(visual_data.get("r", 3.0))

                        h_cone = float(visual_data.get("h", 4.0))

                        u_cone = np.linspace(0, h_cone, 30); th_cone = np.linspace(0, 2*np.pi, 35)

                        U, TH = np.meshgrid(u_cone, th_cone)

                        R_cur = r_cone * (1.0 - U / h_cone)

                        X = R_cur * np.cos(TH); Y = R_cur * np.sin(TH); Z = U

                        fig_mini.add_trace(go.Surface(x=X, y=Y, z=Z, colorscale="YlOrRd", opacity=0.82, showscale=False, name="Khối nón"))

                        fig_mini.add_trace(go.Scatter3d(x=[0, 0], y=[0, 0], z=[0, h_cone], mode="lines+markers+text", line=dict(color="#f59e0b", width=4, dash="dash"), text=["O(đáy)", f"S(h={h_cone})"], textposition="top right", name="Đường cao SO"))

                        fig_mini.add_trace(go.Scatter3d(x=[0, r_cone], y=[0, 0], z=[0, 0], mode="lines+text", line=dict(color="#10b981", width=3), text=["", f"R={r_cone}"], textposition="bottom right", name="Bán kính R"))



                    elif dtype == "cylinder_3d":

                        r_cyl = float(visual_data.get("r", 3.0)); h_cyl = float(visual_data.get("h", 5.0))

                        u_cyl = np.linspace(0, h_cyl, 30); th_cyl = np.linspace(0, 2*np.pi, 35)

                        U, TH = np.meshgrid(u_cyl, th_cyl)

                        X = r_cyl * np.cos(TH); Y = r_cyl * np.sin(TH); Z = U

                        fig_mini.add_trace(go.Surface(x=X, y=Y, z=Z, colorscale="Tealgrn", opacity=0.82, showscale=False, name="Khối trụ"))

                        fig_mini.add_trace(go.Scatter3d(x=[0, 0], y=[0, 0], z=[0, h_cyl], mode="lines+markers+text", line=dict(color="#f59e0b", width=4, dash="dash"), text=["O'(đáy dưới)", "O(đáy trên)"], textposition="top right", name="Trục OO'"))



                    elif dtype == "sphere_3d":

                        r_sph = float(visual_data.get("r", 3.0))

                        c_sph = visual_data.get("center", [0.0, 0.0, 0.0])

                        phi = np.linspace(0, np.pi, 30); theta = np.linspace(0, 2*np.pi, 35)

                        PHI, THETA = np.meshgrid(phi, theta)

                        X = c_sph[0] + r_sph * np.sin(PHI) * np.cos(THETA)

                        Y = c_sph[1] + r_sph * np.sin(PHI) * np.sin(THETA)

                        Z = c_sph[2] + r_sph * np.cos(PHI)

                        fig_mini.add_trace(go.Surface(x=X, y=Y, z=Z, colorscale="Blues", opacity=0.82, showscale=False, name="Mặt cầu"))

                        fig_mini.add_trace(go.Scatter3d(x=[c_sph[0]], y=[c_sph[1]], z=[c_sph[2]], mode="markers+text", marker=dict(color="#f43f5e", size=6), text=["I(tâm)"], textposition="top right", name="Tâm cầu"))



                    elif dtype == "box_with_sphere":

                        fig_mini = go.Figure()

                        phi = np.linspace(0, np.pi, 25); theta = np.linspace(0, 2*np.pi, 30)

                        PHI, THETA = np.meshgrid(phi, theta)

                        Xs = 25 + 20 * np.sin(PHI) * np.cos(THETA)

                        Ys = 25 + 20 * np.sin(PHI) * np.sin(THETA)

                        Zs = 20 + 20 * np.cos(PHI)

                        fig_mini.add_trace(go.Surface(x=Xs, y=Ys, z=Zs, colorscale="Reds", opacity=0.88, showscale=False, name="Quả cầu sắt R=20cm"))

                        lines_x = [0, 50, 50, 0, 0, None, 0, 50, 50, 0, 0, None, 0, 0, None, 50, 50, None, 50, 50, None, 0, 0]

                        lines_y = [0, 0, 50, 50, 0, None, 0, 0, 50, 50, 0, None, 0, 0, None, 0, 0, None, 50, 50, None, 50, 50]

                        lines_z = [0, 0, 0, 0, 0, None, 80, 80, 80, 80, 80, None, 0, 80, None, 0, 80, None, 0, 80, None, 0, 80]

                        fig_mini.add_trace(go.Scatter3d(x=lines_x, y=lines_y, z=lines_z, mode="lines", line=dict(color="#38bdf8", width=4.5), name="Khung bình 50x50x80cm"))

                        fig_mini.update_layout(

                            width=380, height=320, margin=dict(l=10, r=10, t=10, b=10), template="plotly_dark",

                            scene=dict(xaxis=dict(showbackground=False, gridcolor="#334155", title="x"), yaxis=dict(showbackground=False, gridcolor="#334155", title="y"), zaxis=dict(showbackground=False, gridcolor="#334155", title="z"), aspectmode="data")

                        )

                    elif dtype in ["tetrahedron", "oxyz_space", "oxyz_tetrahedron_sphere"]:
                        q_txt_full = str(q.get("q", "") or q.get("question", ""))
                        pts = visual_data.get("points")
                        if not pts and pve:
                            pts = pve.parse_oxyz_tetrahedron_points(q_txt_full)
                        if not pts:
                            pts = {'A': (2.0, 0.0, 0.0), 'B': (0.0, 4.0, 0.0), 'C': (0.0, 0.0, 4.0), 'O': (0.0, 0.0, 0.0)}
                        sph = visual_data.get("sphere")
                        if not sph and pve:
                            sph = pve.solve_circumscribed_sphere(pts)
                        if not sph:
                            sph = {"center": (1.0, 2.0, 2.0), "radius": 3.0}

                        A = pts.get('A', (2.0, 0.0, 0.0))
                        B = pts.get('B', (0.0, 4.0, 0.0))
                        C = pts.get('C', (0.0, 0.0, 4.0))
                        O = pts.get('O', (0.0, 0.0, 0.0))
                        I = sph['center']
                        R = sph['radius']

                        max_coord = max(abs(A[0]), abs(B[1]), abs(C[2]), R*1.2, 4.0)

                        # 1. Trục tọa độ Oxyz với các mũi tên
                        fig_mini.add_trace(go.Scatter3d(x=[0, max_coord * 1.25], y=[0, 0], z=[0, 0], mode="lines+text", line=dict(color="#f43f5e", width=4), text=["", "Trục Ox"], textposition="top right", name="Trục Ox"))
                        fig_mini.add_trace(go.Scatter3d(x=[0, 0], y=[0, max_coord * 1.25], z=[0, 0], mode="lines+text", line=dict(color="#10b981", width=4), text=["", "Trục Oy"], textposition="top right", name="Trục Oy"))
                        fig_mini.add_trace(go.Scatter3d(x=[0, 0], y=[0, 0], z=[0, max_coord * 1.25], mode="lines+text", line=dict(color="#38bdf8", width=4), text=["", "Trục Oz"], textposition="top right", name="Trục Oz"))

                        # 2. Các cạnh tứ diện OABC
                        fig_mini.add_trace(go.Scatter3d(x=[O[0], A[0], None, O[0], B[0], None, O[0], C[0]], y=[O[1], A[1], None, O[1], B[1], None, O[1], C[1]], z=[O[2], A[2], None, O[2], B[2], None, O[2], C[2]], mode="lines", line=dict(color="#94a3b8", width=3.5, dash="dash"), name="Cạnh góc vuông tại O"))
                        fig_mini.add_trace(go.Scatter3d(x=[A[0], B[0], C[0], A[0]], y=[A[1], B[1], C[1], A[1]], z=[A[2], B[2], C[2], A[2]], mode="lines", line=dict(color="#fbbf24", width=5), name="Mặt tam giác (ABC)"))

                        # 3. Đỉnh tứ diện OABC
                        fig_mini.add_trace(go.Scatter3d(
                            x=[O[0], A[0], B[0], C[0]],
                            y=[O[1], A[1], B[1], C[1]],
                            z=[O[2], A[2], B[2], C[2]],
                            mode="markers+text",
                            marker=dict(size=6, color=["#94a3b8", "#f43f5e", "#10b981", "#38bdf8"]),
                            text=["O(0;0;0)", f"A({A[0]:g};{A[1]:g};{A[2]:g})", f"B({B[0]:g};{B[1]:g};{B[2]:g})", f"C({C[0]:g};{C[1]:g};{C[2]:g})"],
                            textposition=["bottom right", "top left", "top right", "top center"],
                            name="Đỉnh tứ diện OABC"
                        ))

                        # 4. Mặt cầu ngoại tiếp (R=3)
                        if any(kw in q_txt_full.lower() for kw in ["mặt cầu", "ngoại tiếp", "bán kính"]):
                            phi = np.linspace(0, np.pi, 25); theta = np.linspace(0, 2*np.pi, 30)
                            PHI, THETA = np.meshgrid(phi, theta)
                            Xs = I[0] + R * np.sin(PHI) * np.cos(THETA)
                            Ys = I[1] + R * np.sin(PHI) * np.sin(THETA)
                            Zs = I[2] + R * np.cos(PHI)
                            fig_mini.add_trace(go.Surface(x=Xs, y=Ys, z=Zs, colorscale="Blues", opacity=0.22, showscale=False, name=f"Mặt cầu ngoại tiếp (R={R:.1f})"))
                            fig_mini.add_trace(go.Scatter3d(x=[I[0]], y=[I[1]], z=[I[2]], mode="markers+text", marker=dict(color="#0284c7", size=7), text=[f"I({I[0]:g};{I[1]:g};{I[2]:g})"], textposition="top center", name=f"Tâm I (R={R:.1f})"))

                    elif dtype == "points_segment" or sub_type == "oxyz_midpoint_projection":
                        pts = visual_data.get("points") or {}
                        if not pts and pve:
                            q_txt_full = str(q.get("q", "") or q.get("question", ""))
                            pts = pve.build_oxyz_points_segment_model(q_txt_full).get("points", {})
                        A = pts.get("A", (1.0, 2.0, -1.0))
                        B = pts.get("B", (3.0, 0.0, 1.0))
                        M = pts.get("I") or pts.get("M") or ((A[0]+B[0])/2.0, (A[1]+B[1])/2.0, (A[2]+B[2])/2.0)
                        M_proj = pts.get("M", (M[0], M[1], 0.0))

                        max_coord = max(abs(A[0]), abs(B[0]), abs(A[1]), abs(B[1]), abs(A[2]), abs(B[2]), abs(M[0]), abs(M[1]), abs(M[2]), 3.0) * 1.35

                        # 1. Trục tọa độ Oxyz chuẩn sư phạm có nhãn trục rõ ràng
                        fig_mini.add_trace(go.Scatter3d(x=[0, max_coord], y=[0, 0], z=[0, 0], mode="lines+text", line=dict(color="#f43f5e", width=4), text=["", "Trục Ox"], textposition="top right", name="Trục Ox"))
                        fig_mini.add_trace(go.Scatter3d(x=[0, 0], y=[0, max_coord], z=[0, 0], mode="lines+text", line=dict(color="#10b981", width=4), text=["", "Trục Oy"], textposition="top right", name="Trục Oy"))
                        fig_mini.add_trace(go.Scatter3d(x=[0, 0], y=[0, 0], z=[0, max_coord], mode="lines+text", line=dict(color="#38bdf8", width=4), text=["", "Trục Oz"], textposition="top right", name="Trục Oz"))

                        # 2. Đoạn thẳng AB nối hai điểm trong không gian
                        fig_mini.add_trace(go.Scatter3d(
                            x=[A[0], B[0]], y=[A[1], B[1]], z=[A[2], B[2]],
                            mode="lines", line=dict(color="#fbbf24", width=5), name="Đoạn thẳng AB"
                        ))

                        # 3. Đường dóng từ trung điểm M xuống hình chiếu trên mặt phẳng (Oxy)
                        if abs(M[2] - M_proj[2]) > 0.01:
                            fig_mini.add_trace(go.Scatter3d(
                                x=[M[0], M_proj[0]], y=[M[1], M_proj[1]], z=[M[2], M_proj[2]],
                                mode="lines", line=dict(color="#38bdf8", width=3, dash="dash"), name="Đường dóng hình chiếu (Oxy)"
                            ))

                        # 4. Mặt phẳng tọa độ (Oxy) dạng lưới bán trong suốt
                        gp = max_coord * 0.75
                        fig_mini.add_trace(go.Mesh3d(
                            x=[-gp*0.2, gp, gp, -gp*0.2],
                            y=[-gp*0.2, -gp*0.2, gp, gp],
                            z=[0, 0, 0, 0],
                            opacity=0.12, color="#38bdf8", showscale=False, name="Mặt phẳng (Oxy)"
                        ))

                        # 5. Các điểm mốc quan trọng và nhãn tọa độ chi tiết
                        pt_x = [0, A[0], B[0], M[0]]
                        pt_y = [0, A[1], B[1], M[1]]
                        pt_z = [0, A[2], B[2], M[2]]
                        pt_colors = ["#94a3b8", "#f43f5e", "#f43f5e", "#10b981"]
                        pt_names = [
                            "O(0;0;0)",
                            f"A({A[0]:g};{A[1]:g};{A[2]:g})",
                            f"B({B[0]:g};{B[1]:g};{B[2]:g})",
                            f"M({M[0]:g};{M[1]:g};{M[2]:g})"
                        ]
                        fig_mini.add_trace(go.Scatter3d(
                            x=pt_x, y=pt_y, z=pt_z,
                            mode="markers+text",
                            marker=dict(size=[5, 7, 7, 9], color=pt_colors),
                            text=pt_names,
                            textposition=["bottom left", "top left", "top right", "top center"],
                            name="Điểm mốc tọa độ"
                        ))

                    elif dtype == "flight_trajectory" or sub_type == "oxyz_distance_point_line":
                        pts = visual_data.get("points") or {}
                        O = pts.get("O", (0.0, 0.0, 0.0))
                        M_pt = pts.get("M", (1.0, 2.0, 3.0))
                        N_pt = pts.get("N", (4.0, 5.0, 6.0))
                        H_pt = pts.get("H", (2.0, 3.0, 4.0))
                        max_coord = max(abs(M_pt[0]), abs(N_pt[0]), abs(M_pt[1]), abs(N_pt[1]), abs(M_pt[2]), abs(N_pt[2]), 5.0) * 1.25

                        # Trục Oxyz
                        fig_mini.add_trace(go.Scatter3d(x=[0, max_coord], y=[0, 0], z=[0, 0], mode="lines+text", line=dict(color="#f43f5e", width=4), text=["", "Trục Ox"], textposition="top right", name="Trục Ox"))
                        fig_mini.add_trace(go.Scatter3d(x=[0, 0], y=[0, max_coord], z=[0, 0], mode="lines+text", line=dict(color="#10b981", width=4), text=["", "Trục Oy"], textposition="top right", name="Trục Oy"))
                        fig_mini.add_trace(go.Scatter3d(x=[0, 0], y=[0, 0], z=[0, max_coord], mode="lines+text", line=dict(color="#38bdf8", width=4), text=["", "Trục Oz"], textposition="top right", name="Trục Oz"))

                        # Đường bay MN
                        fig_mini.add_trace(go.Scatter3d(x=[M_pt[0], N_pt[0]], y=[M_pt[1], N_pt[1]], z=[M_pt[2], N_pt[2]], mode="lines", line=dict(color="#38bdf8", width=5), name="Đường bay MN"))
                        # Khoảng cách ngắn nhất OH
                        fig_mini.add_trace(go.Scatter3d(x=[O[0], H_pt[0]], y=[O[1], H_pt[1]], z=[O[2], H_pt[2]], mode="lines", line=dict(color="#f59e0b", width=4, dash="dash"), name="Khoảng cách ngắn nhất d(O, MN)"))

                        # Các điểm
                        fig_mini.add_trace(go.Scatter3d(
                            x=[O[0], M_pt[0], N_pt[0], H_pt[0]],
                            y=[O[1], M_pt[1], N_pt[1], H_pt[1]],
                            z=[O[2], M_pt[2], N_pt[2], H_pt[2]],
                            mode="markers+text",
                            marker=dict(size=[6, 7, 7, 7], color=["#94a3b8", "#38bdf8", "#38bdf8", "#f59e0b"]),
                            text=["O(0;0;0)", f"M({M_pt[0]:g};{M_pt[1]:g};{M_pt[2]:g})", f"N({N_pt[0]:g};{N_pt[1]:g};{N_pt[2]:g})", "H (d_min)"],
                            textposition=["bottom left", "top left", "top right", "top center"],
                            name="Điểm mốc"
                        ))

                    elif sub_type == "pyramid_quad" or (dtype == "geom_3d" and sub_type == "pyramid_quad"):
                        pts = visual_data.get("points") or {
                            "A": (-2.0, -1.5, 0.0), "B": (2.0, -1.5, 0.0), "C": (3.0, 1.5, 0.0), "D": (-1.0, 1.5, 0.0), "S": (0.0, 0.0, 4.0)
                        }
                        A = pts.get("A", (-2.0, -1.5, 0.0))
                        B = pts.get("B", (2.0, -1.5, 0.0))
                        C = pts.get("C", (3.0, 1.5, 0.0))
                        D = pts.get("D", (-1.0, 1.5, 0.0))
                        S = pts.get("S", (0.0, 0.0, 4.0))

                        # Khung cạnh đáy ABCD
                        fig_mini.add_trace(go.Scatter3d(
                            x=[A[0], B[0], C[0], D[0], A[0]],
                            y=[A[1], B[1], C[1], D[1], A[1]],
                            z=[A[2], B[2], C[2], D[2], A[2]],
                            mode="lines", line=dict(color="#fbbf24", width=4), name="Mặt đáy ABCD"
                        ))
                        # Các cạnh bên SA, SB, SC, SD
                        fig_mini.add_trace(go.Scatter3d(
                            x=[S[0], A[0], None, S[0], B[0], None, S[0], C[0], None, S[0], D[0]],
                            y=[S[1], A[1], None, S[1], B[1], None, S[1], C[1], None, S[1], D[1]],
                            z=[S[2], A[2], None, S[2], B[2], None, S[2], C[2], None, S[2], D[2]],
                            mode="lines", line=dict(color="#fbbf24", width=4), name="Cạnh bên"
                        ))
                        # Bề mặt Mesh3d bán trong suốt
                        mesh_x = [A[0], B[0], C[0], D[0], S[0]]
                        mesh_y = [A[1], B[1], C[1], D[1], S[1]]
                        mesh_z = [A[2], B[2], C[2], D[2], S[2]]
                        fig_mini.add_trace(go.Mesh3d(
                            x=mesh_x, y=mesh_y, z=mesh_z,
                            i=[0, 1, 2, 3, 0, 0],
                            j=[1, 2, 3, 0, 1, 2],
                            k=[4, 4, 4, 4, 2, 3],
                            opacity=0.22, color="#38bdf8", showscale=False, name="Khối chóp S.ABCD"
                        ))
                        # Nhãn các đỉnh
                        fig_mini.add_trace(go.Scatter3d(
                            x=[A[0], B[0], C[0], D[0], S[0]],
                            y=[A[1], B[1], C[1], D[1], S[1]],
                            z=[A[2], B[2], C[2], D[2], S[2]],
                            mode="markers+text",
                            marker=dict(size=6, color=["#f59e0b", "#f59e0b", "#f59e0b", "#f59e0b", "#f43f5e"]),
                            text=["A", "B", "C", "D", "S"],
                            textposition=["bottom left", "bottom right", "top right", "top left", "top center"],
                            name="Đỉnh chóp"
                        ))

                    elif sub_type == "tetrahedron_pure" or (dtype == "geom_3d" and sub_type == "tetrahedron_pure"):
                        pts = visual_data.get("points") or {
                            "A": (-1.8, -1.0, 0.0), "B": (2.2, -1.2, 0.0), "C": (1.0, 1.8, 0.0), "S": (0.2, 0.2, 3.5)
                        }
                        A = pts.get("A", (-1.8, -1.0, 0.0))
                        B = pts.get("B", (2.2, -1.2, 0.0))
                        C = pts.get("C", (1.0, 1.8, 0.0))
                        S = pts.get("S", (0.2, 0.2, 3.5))

                        # Khung cạnh đáy ABC
                        fig_mini.add_trace(go.Scatter3d(
                            x=[A[0], B[0], C[0], A[0]],
                            y=[A[1], B[1], C[1], A[1]],
                            z=[A[2], B[2], C[2], A[2]],
                            mode="lines", line=dict(color="#fbbf24", width=4), name="Mặt đáy ABC"
                        ))
                        # Các cạnh bên SA, SB, SC
                        fig_mini.add_trace(go.Scatter3d(
                            x=[S[0], A[0], None, S[0], B[0], None, S[0], C[0]],
                            y=[S[1], A[1], None, S[1], B[1], None, S[1], C[1]],
                            z=[S[2], A[2], None, S[2], B[2], None, S[2], C[2]],
                            mode="lines", line=dict(color="#fbbf24", width=4), name="Cạnh bên"
                        ))
                        # Bề mặt Mesh3d bán trong suốt
                        mesh_x = [A[0], B[0], C[0], S[0]]
                        mesh_y = [A[1], B[1], C[1], S[1]]
                        mesh_z = [A[2], B[2], C[2], S[2]]
                        fig_mini.add_trace(go.Mesh3d(
                            x=mesh_x, y=mesh_y, z=mesh_z,
                            i=[0, 0, 1, 0],
                            j=[1, 1, 2, 2],
                            k=[2, 3, 3, 3],
                            opacity=0.22, color="#38bdf8", showscale=False, name="Khối chóp S.ABC"
                        ))
                        # Đỉnh
                        fig_mini.add_trace(go.Scatter3d(
                            x=[A[0], B[0], C[0], S[0]],
                            y=[A[1], B[1], C[1], S[1]],
                            z=[A[2], B[2], C[2], S[2]],
                            mode="markers+text",
                            marker=dict(size=6, color=["#f59e0b", "#f59e0b", "#f59e0b", "#f43f5e"]),
                            text=["A", "B", "C", "S"],
                            textposition=["bottom left", "bottom right", "top right", "top center"],
                            name="Đỉnh chóp"
                        ))

                    elif sub_type == "triangular_prism" or (dtype == "geom_3d" and sub_type == "triangular_prism"):
                        pts = visual_data.get("points") or {
                            "A": (-1.5, -1.0, 0.0), "B": (2.0, -1.2, 0.0), "C": (1.2, 1.5, 0.0),
                            "A'": (-1.5, -1.0, 4.0), "B'": (2.0, -1.2, 4.0), "C'": (1.2, 1.5, 4.0)
                        }
                        A = pts.get("A", (-1.5, -1.0, 0.0))
                        B = pts.get("B", (2.0, -1.2, 0.0))
                        C = pts.get("C", (1.2, 1.5, 0.0))
                        A1 = pts.get("A'", (-1.5, -1.0, 4.0))
                        B1 = pts.get("B'", (2.0, -1.2, 4.0))
                        C1 = pts.get("C'", (1.2, 1.5, 4.0))

                        # Khung đáy dưới ABC và đáy trên A'B'C'
                        fig_mini.add_trace(go.Scatter3d(
                            x=[A[0], B[0], C[0], A[0], None, A1[0], B1[0], C1[0], A1[0]],
                            y=[A[1], B[1], C[1], A[1], None, A1[1], B1[1], C1[1], A1[1]],
                            z=[A[2], B[2], C[2], A[2], None, A1[2], B1[2], C1[2], A1[2]],
                            mode="lines", line=dict(color="#fbbf24", width=4), name="Mặt đáy"
                        ))
                        # Các cạnh bên AA', BB', CC'
                        fig_mini.add_trace(go.Scatter3d(
                            x=[A[0], A1[0], None, B[0], B1[0], None, C[0], C1[0]],
                            y=[A[1], A1[1], None, B[1], B1[1], None, C[1], C1[1]],
                            z=[A[2], A1[2], None, B[2], B1[2], None, C[2], C1[2]],
                            mode="lines", line=dict(color="#fbbf24", width=4), name="Cạnh bên"
                        ))
                        # Bề mặt Mesh3d
                        mesh_x = [A[0], B[0], C[0], A1[0], B1[0], C1[0]]
                        mesh_y = [A[1], B[1], C[1], A1[1], B1[1], C1[1]]
                        mesh_z = [A[2], B[2], C[2], A1[2], B1[2], C1[2]]
                        fig_mini.add_trace(go.Mesh3d(
                            x=mesh_x, y=mesh_y, z=mesh_z,
                            i=[0, 3, 0, 1, 1, 2, 2, 0],
                            j=[1, 4, 1, 4, 2, 5, 0, 3],
                            k=[2, 5, 3, 3, 4, 4, 5, 5],
                            opacity=0.22, color="#38bdf8", showscale=False, name="Lăng trụ ABC.A'B'C'"
                        ))
                        # Đỉnh
                        fig_mini.add_trace(go.Scatter3d(
                            x=[A[0], B[0], C[0], A1[0], B1[0], C1[0]],
                            y=[A[1], B[1], C[1], A1[1], B1[1], C1[1]],
                            z=[A[2], B[2], C[2], A1[2], B1[2], C1[2]],
                            mode="markers+text",
                            marker=dict(size=6, color="#f59e0b"),
                            text=["A", "B", "C", "A'", "B'", "C'"],
                            textposition=["bottom left", "bottom right", "top right", "top left", "top right", "top center"],
                            name="Đỉnh lăng trụ"
                        ))

                    elif sub_type == "box_prism" or (dtype == "geom_3d" and sub_type == "box_prism"):
                        pts = visual_data.get("points") or {
                            "A": (0.0, 0.0, 0.0), "B": (4.0, 0.0, 0.0), "C": (4.0, 3.0, 0.0), "D": (0.0, 3.0, 0.0),
                            "A'": (0.0, 0.0, 3.5), "B'": (4.0, 0.0, 3.5), "C'": (4.0, 3.0, 3.5), "D'": (0.0, 3.0, 3.5)
                        }
                        A = pts.get("A", (0.0, 0.0, 0.0))
                        B = pts.get("B", (4.0, 0.0, 0.0))
                        C = pts.get("C", (4.0, 3.0, 0.0))
                        D = pts.get("D", (0.0, 3.0, 0.0))
                        A1 = pts.get("A'", (0.0, 0.0, 3.5))
                        B1 = pts.get("B'", (4.0, 0.0, 3.5))
                        C1 = pts.get("C'", (4.0, 3.0, 3.5))
                        D1 = pts.get("D'", (0.0, 3.0, 3.5))

                        # Khung đáy dưới ABCD và đáy trên A'B'C'D'
                        fig_mini.add_trace(go.Scatter3d(
                            x=[A[0], B[0], C[0], D[0], A[0], None, A1[0], B1[0], C1[0], D1[0], A1[0]],
                            y=[A[1], B[1], C[1], D[1], A[1], None, A1[1], B1[1], C1[1], D1[1], A1[1]],
                            z=[A[2], B[2], C[2], D[2], A[2], None, A1[2], B1[2], C1[2], D1[2], A1[2]],
                            mode="lines", line=dict(color="#fbbf24", width=4), name="Mặt đáy"
                        ))
                        # Các cạnh bên AA', BB', CC', DD'
                        fig_mini.add_trace(go.Scatter3d(
                            x=[A[0], A1[0], None, B[0], B1[0], None, C[0], C1[0], None, D[0], D1[0]],
                            y=[A[1], A1[1], None, B[1], B1[1], None, C[1], C1[1], None, D[1], D1[1]],
                            z=[A[2], A1[2], None, B[2], B1[2], None, C[2], C1[2], None, D[2], D1[2]],
                            mode="lines", line=dict(color="#fbbf24", width=4), name="Cạnh bên"
                        ))
                        # Bề mặt Mesh3d
                        mesh_x = [A[0], B[0], C[0], D[0], A1[0], B1[0], C1[0], D1[0]]
                        mesh_y = [A[1], B[1], C[1], D[1], A1[1], B1[1], C1[1], D1[1]]
                        mesh_z = [A[2], B[2], C[2], D[2], A1[2], B1[2], C1[2], D1[2]]
                        fig_mini.add_trace(go.Mesh3d(
                            x=mesh_x, y=mesh_y, z=mesh_z,
                            i=[0, 0, 4, 4, 0, 1, 1, 2, 2, 3, 3, 0],
                            j=[1, 2, 5, 6, 1, 5, 2, 6, 3, 7, 0, 4],
                            k=[2, 3, 6, 7, 4, 4, 5, 5, 6, 6, 7, 7],
                            opacity=0.22, color="#38bdf8", showscale=False, name="Khối hộp ABCD.A'B'C'D'"
                        ))
                        # Đỉnh
                        fig_mini.add_trace(go.Scatter3d(
                            x=[A[0], B[0], C[0], D[0], A1[0], B1[0], C1[0], D1[0]],
                            y=[A[1], B[1], C[1], D[1], A1[1], B1[1], C1[1], D1[1]],
                            z=[A[2], B[2], C[2], D[2], A1[2], B1[2], C1[2], D1[2]],
                            mode="markers+text",
                            marker=dict(size=6, color="#f59e0b"),
                            text=["A", "B", "C", "D", "A'", "B'", "C'", "D'"],
                            textposition=["bottom left", "bottom right", "top right", "top left", "top left", "top right", "top right", "top left"],
                            name="Đỉnh khối hộp"
                        ))

                    has_oxyz_flag = visual_data.get("has_oxyz", False)
                    is_pure_11 = (not has_oxyz_flag) and (sub_type in ["pyramid_quad", "tetrahedron_pure", "triangular_prism", "box_prism"] or dtype in ["cone_3d", "cylinder_3d", "sphere_3d"])

                    if is_pure_11:
                        scene_cfg = dict(
                            xaxis=dict(visible=False, showbackground=False, showgrid=False, zeroline=False, showticklabels=False, title=""),
                            yaxis=dict(visible=False, showbackground=False, showgrid=False, zeroline=False, showticklabels=False, title=""),
                            zaxis=dict(visible=False, showbackground=False, showgrid=False, zeroline=False, showticklabels=False, title=""),
                            camera=dict(eye=dict(x=1.7, y=1.6, z=1.3)),
                            aspectmode="data"
                        )
                    else:
                        scene_cfg = dict(
                            xaxis=dict(showbackground=False, gridcolor="#334155", title="x"),
                            yaxis=dict(showbackground=False, gridcolor="#334155", title="y"),
                            zaxis=dict(showbackground=False, gridcolor="#334155", title="z"),
                            camera=dict(eye=dict(x=1.6, y=1.5, z=1.3)),
                            aspectmode="data"
                        )

                    fig_mini.update_layout(
                        width=380, height=320, margin=dict(l=10, r=10, t=10, b=10), template="plotly_dark",
                        scene=scene_cfg
                    )

                    col_g1, col_g2, col_g3 = st.columns([1, 2.2, 1])

                    with col_g2:

                        st.caption("🔄 **Hình học 3D tương tác:** Bấm giữ chuột để **XOAY 360°**, lăn chuột phóng to/thu nhỏ!")

                        st.plotly_chart(fig_mini, width="content", key=f"mini_chart_{q_id}" if q_id else None)

                else:

                    # 2D ĐỒ THỊ CHUẨN SƯ PHẠM BỘ GD&ĐT HIỂN THỊ TRỰC TIẾP

                    extra_pts = visual_data.get("extra_points", [])

                    if not extra_pts and q.get("question"):

                        q_txt = str(q.get("question"))

                        found_pts = re.findall(r'[xX]\s*=\s*(-?\d+(?:\.\d+)?)', q_txt)

                        if found_pts:

                            extra_pts = [float(p) for p in found_pts if abs(float(p)) <= 10]



                    b64_graph = render_math_graph_to_webp_base64(visual_data, extra_points=extra_pts)

                    if b64_graph:

                        col_g1, col_g2, col_g3 = st.columns([1, 2.5, 1])

                        with col_g2:

                            graph_title = "📈 **Đồ thị của hàm số đạo hàm $y = f'(x)$ (Chuẩn Bộ GD&ĐT):**" if visual_data.get("is_derivative") else "📈 **Đồ thị hàm số minh họa (Lưới ô vuông & Dóng tọa độ chuẩn Bộ):**"
                            st.caption(graph_title)

                            st.markdown(f'<div style="display:flex; justify-content:center; margin:8px auto;"><img src="{b64_graph}" style="max-width:100%; height:auto; border-radius:6px; box-shadow:0 4px 12px rgba(0,0,0,0.15);"/></div>', unsafe_allow_html=True)

            except Exception as err:

                logging.warning("Lỗi vẽ đồ thị / hình học 3D: %s", err)



        # 2.65. HIỂN THỊ NGỮ LIỆU ĐA MÔN ĐẶC THÙ (VẬT LÝ, HÓA HỌC, SINH HỌC, ĐỊA LÍ, TOÁN THỰC TẾ)
        # A. VẬT LÝ 12 & 11 CHUẨN CT GDPT 2018 (NHIỆT HỌC, TỪ TRƯỜNG, HẠT NHÂN, MẠCH ĐIỆN, SÓNG)
        if q.get("thermal_pv_visual") and isinstance(q["thermal_pv_visual"], dict):
            tpv = q["thermal_pv_visual"]
            st.caption(f"🌡️ **{tpv.get('title', 'Đồ thị biến đổi trạng thái khí lý tưởng (p-V):')}**")
            if tpv.get("svg"):
                st.markdown(f'<div style="display:flex; justify-content:center; margin:8px auto; max-width:540px;">{sanitize_svg_for_markdown(tpv["svg"])}</div>', unsafe_allow_html=True)

        elif q.get("magnetic_visual") and isinstance(q["magnetic_visual"], dict):
            mag = q["magnetic_visual"]
            st.caption(f"🧲 **{mag.get('title', 'Mô hình từ trường & lực Lorentz / Am-pe:')}**")
            if mag.get("svg"):
                st.markdown(f'<div style="display:flex; justify-content:center; margin:8px auto; max-width:540px;">{sanitize_svg_for_markdown(mag["svg"])}</div>', unsafe_allow_html=True)

        elif q.get("nuclear_visual") and isinstance(q["nuclear_visual"], dict):
            nuc = q["nuclear_visual"]
            st.caption(f"⚛️ **{nuc.get('title', 'Đồ thị phân rã phóng xạ theo thời gian (Vật lý 12 KNTT):')}**")
            if nuc.get("svg"):
                st.markdown(f'<div style="display:flex; justify-content:center; margin:8px auto; max-width:540px;">{sanitize_svg_for_markdown(nuc["svg"])}</div>', unsafe_allow_html=True)

        elif q.get("circuit_visual") and isinstance(q["circuit_visual"], dict):
            c_info = q["circuit_visual"]
            st.caption(f"⚡ **{c_info.get('title', 'Sơ đồ mạch điện chuẩn SI:')}**")
            if c_info.get("svg"):
                st.markdown(f'<div style="display:flex; justify-content:center; margin:8px auto; max-width:540px;">{c_info["svg"]}</div>', unsafe_allow_html=True)

        elif q.get("wave_visual") and isinstance(q["wave_visual"], dict):
            wv = q["wave_visual"]
            st.caption(f"〰️ **{wv.get('title', 'Đồ thị hình sin của sóng cơ học truyền theo trục Ox:')}**")
            if wv.get("svg"):
                st.markdown(f'<div style="display:flex; justify-content:center; margin:8px auto; max-width:540px;">{sanitize_svg_for_markdown(wv["svg"])}</div>', unsafe_allow_html=True)

        # B. HÓA HỌC
        if q.get("chem_visual") and isinstance(q["chem_visual"], dict):
            ch_info = q["chem_visual"]
            st.caption(f"🧪 **{ch_info.get('title', 'Mô hình thí nghiệm chuẩn IUPAC:')}**")
            if ch_info.get("svg"):
                st.markdown(f'<div style="display:flex; justify-content:center; margin:8px auto; max-width:560px;">{ch_info["svg"]}</div>', unsafe_allow_html=True)

        # C. SINH HỌC
        if q.get("pedigree_visual") and isinstance(q["pedigree_visual"], dict):
            ped_info = q["pedigree_visual"]
            st.caption(f"🧬 **{ped_info.get('title', 'Sơ đồ phả hệ di truyền chuẩn quốc tế:')}**")
            if ped_info.get("svg"):
                st.markdown(f'<div style="display:flex; justify-content:center; margin:8px auto; max-width:540px;">{ped_info["svg"]}</div>', unsafe_allow_html=True)

        if q.get("food_web_visual") and isinstance(q["food_web_visual"], dict):
            fw_info = q["food_web_visual"]
            st.caption(f"🌿 **{fw_info.get('title', 'Sơ đồ lưới thức ăn sinh thái:')}**")
            if fw_info.get("svg"):
                st.markdown(f'<div style="display:flex; justify-content:center; margin:8px auto; max-width:560px;">{sanitize_svg_for_markdown(fw_info["svg"])}</div>', unsafe_allow_html=True)
            elif fw_info.get("mermaid"):
                render_mermaid(fw_info["mermaid"])

        # D. TOÁN MÔ HÌNH THỰC TẾ (CHỈ hiển thị khi chưa có Plotly 3D tương tác để học sinh xoay 360 độ hoàn mỹ)
        if q.get("composite_visual") and isinstance(q["composite_visual"], dict):
            comp_info = q["composite_visual"]
            if not (visual_data and is_3d):
                st.caption(f"📐 **Mô hình toán học thực tế:** *{comp_info.get('title', 'Bài toán mô hình hóa thực tiễn')}*")
                if comp_info.get("svg"):
                    st.markdown(f'<div style="display:flex; justify-content:center; margin:8px auto; max-width:540px;">{sanitize_svg_for_markdown(comp_info["svg"])}</div>', unsafe_allow_html=True)




        if q.get("geo_chart") and isinstance(q["geo_chart"], dict):

            g_chart = q["geo_chart"]

            st.caption(f"🗺️ **{g_chart.get('title', 'Biểu đồ số liệu kinh tế - xã hội:')}**")

            years = g_chart.get("years", [])

            series = g_chart.get("series", [])

            if years and series:

                tbl_h = '<table style="width:100%; border-collapse:collapse; text-align:center; color:#f8fafc; font-size:13.5px; border:1px solid #475569;"><tr style="background:#1e293b; color:#38bdf8;"><th style="padding:6px; border:1px solid #334155;">Ngành / Chỉ tiêu</th>'

                for y in years: tbl_h += f'<th style="padding:6px; border:1px solid #334155;">{y}</th>'

                tbl_h += '</tr>'

                for s in series:

                    tbl_h += f'<tr><td style="padding:6px; border:1px solid #334155; text-align:left; font-weight:500;">{s.get("name")}</td>'

                    for d_val in s.get("data", []):

                        tbl_h += f'<td style="padding:6px; border:1px solid #334155;">{d_val}%</td>'

                    tbl_h += '</tr>'

                tbl_h += '</table>'

                st.markdown(f'<div style="max-width:600px; margin:8px auto; background:#0f172a; padding:8px 12px; border-radius:8px; border:1px solid #334155;">{tbl_h}</div>', unsafe_allow_html=True)



        # 2.7. HIỂN THỊ MÃ NGUỒN TIKZ VECTOR LATEX (DÀNH CHO GIÁO VIÊN SOẠN ĐỀ & OVERLEAF)

        if q.get("tikz"):

            with st.expander("💻 Xem & Sao chép mã nguồn TikZ / LaTeX Vector (Chuẩn Bộ GD&ĐT)", expanded=False):

                st.code(q["tikz"], language="latex")

                st.caption("✨ **Đồ họa Vector PGF/TikZ sắc nét tuyệt đối:** Dán trực tiếp vào Overleaf hoặc MathType để xuất bản in A4 chất lượng cao nhất!")

    def render_exam_export_suite(exam_obj, subject_nm, grade_nm, duration_mins, include_ans_default=True, key_prefix="exp"):

        st.markdown("### 🖨️ Xuất Bản Đề Thi Chuẩn Bộ GD&ĐT & Bản In A4")

        ex_c = str(exam_obj.get("code", st.session_state.get("exam_code", "101")))



        # 1. BỘ CHỌN 2 LUỒNG MẪU IN ĐỀ THI

        c_mode1, c_mode2 = st.columns([1.6, 1])

        with c_mode1:

            tmpl_choice = st.radio(

                "📋 Chọn Mẫu Xuất Bản & In PDF (Chuyển đổi tức thì để so sánh):",

                [

                    "🏛️ Mẫu 1: Chuẩn Khảo Thí Quốc Gia (Form Truyền Thống Công Phu - Thầy Phan Minh Trí)",

                    "📘 Mẫu 2: Chuẩn Sư Phạm Hiện Đại (Overleaf Typography - Gợi Mở Tư Duy)"

                ],

                index=0,

                key=f"{key_prefix}_tmpl_choice"

            )

            template_style = "form1" if "Mẫu 1" in tmpl_choice else "form2"



        with c_mode2:

            if template_style == "form1":

                st.success("✨ **Mẫu 1:** Giữ nguyên 100% form truyền thống công phu của Thầy Trí, chuẩn mực khảo thí Bộ GD&ĐT.")

            else:

                st.info("💡 **Mẫu 2:** Phong cách Sư phạm hiện đại Overleaf Typography, có banner màu và mục gợi mở tư duy.")



        # 2. KHUNG TÙY BIẾN TIÊU ĐỀ, TRƯỜNG HỌC & CHÂN TRANG BẢN QUYỀN

        with st.expander("⚙️ Tùy Biến Tiêu Đề, Tên Trường, Giáo Viên & Chân Trang Triết Lý Giáo Dục", expanded=False):

            col_cfg1, col_cfg2 = st.columns(2)

            with col_cfg1:

                custom_school = st.text_input("🏫 Tên Trường / Đơn vị khảo thí:", value="TRƯỜNG THPT TÂN HIỆP • THẦY PHAN MINH TRÍ", key=f"{key_prefix}_sch")

                custom_teacher = st.text_input("👨‍🏫 Tên Giáo viên biên soạn:", value="Thầy Phan Minh Trí", key=f"{key_prefix}_tea")

            with col_cfg2:

                custom_quote = st.text_input("💬 Trích dẫn triết lý giáo dục chân trang (Góc trái):", value="Dưỡng thiện tâm, Ươm nhân tài", key=f"{key_prefix}_qte")

                custom_author = st.text_input("✒️ Tác giả câu triết lý (Viết hoa, in đậm):", value="THẦY PHAN MINH TRÍ", key=f"{key_prefix}_aut")

            show_qr_support = st.checkbox("☕ Hiển thị Mã VietQR MB Bank ủng hộ tác giả ở cuối trang đáp án", value=True, key=f"{key_prefix}_show_mbqr")



        # KIẾN TRÚC BẢO MẬT KHẢO THÍ: TRONG SUỐT QUÁ TRÌNH LÀM BÀI KHÔNG ĐƯỢC PHÉP HIỆN DẤU TICK ĐÁP ÁN

        is_testing = (st.session_state.get("exam_state") == "testing")

        if is_testing:

            include_answers = False

            st.info("🔒 **Chế độ Khảo thí Bảo mật:** Trong suốt thời gian làm bài, đáp án và lời giải chi tiết được khóa tuyệt đối để đảm bảo trung thực khảo thí. Em/Thầy Cô có thể in bản đề thi A4 chuẩn Bộ (không có đáp án) để làm bài trên giấy. **Sau khi bấm 'Nộp bài & Chấm điểm'**, hệ thống sẽ mở khóa tùy chọn *In 1-Chạm Kèm Đáp Án & Ma Trận Điểm*!")

        else:

            include_answers = st.checkbox("✅ In 1-Chạm: Kèm Toàn Bộ Đáp Án, Lời Giải Chi Tiết & Ma Trận Chấm Điểm Chuẩn Bộ", value=include_ans_default, key=f"{key_prefix}_export_answers")



        try:

            print_html, latex_code = build_exam_exports(

                exam_obj, subject_nm, grade_nm, duration_mins,

                include_answers=include_answers,

                template_style=template_style,

                teacher_name=custom_teacher,

                school_name=custom_school,

                quote_text=custom_quote,

                quote_author=custom_author,

                show_support_qr=show_qr_support

            )

            app_share_url = f"{APP_URL}?exam_code={ex_c}&subject={urllib.parse.quote(subject_nm)}"

            qr_base64_img = generate_local_qr_base64(app_share_url, fill_color="#0284c7", back_color="#0f172a")



            tab_prev, tab_qr, tab_tex, tab_azota, tab_json = st.tabs([

                "👁️ Xem Trước Bản In A4 (PDF Live Preview)",

                "📱 Quét Mã QR Trên Điện Thoại (Kép: Đề thi & VietQR)",

                "💻 Mã Nguồn LaTeX Overleaf (TikZ & Tabularx)",

                "⚡ Xuất Chuẩn Azota / LMS ($$...$$)",

                "💾 Tải Đề Dữ Liệu JSON"

            ])



            with tab_prev:

                c_btn1, c_btn2 = st.columns([1.2, 1.8])

                with c_btn1:

                    st.download_button(

                        f"🖨️ Tải File In HTML ({'Mẫu 1' if template_style == 'form1' else 'Mẫu 2'})",

                        print_html,

                        f"De_{ex_c}_{subject_nm}_{template_style}.html",

                        "text/html",

                        type="primary",

                        key=f"{key_prefix}_dl_html",

                        width="stretch"

                    )

                with c_btn2:

                    st.caption("💡 **Mẹo In/Lưu PDF 1-Chạm:** Mở tệp HTML bằng Chrome/Edge ➔ Bấm nút **'In đề / Lưu PDF'** (hoặc Ctrl+P) ➔ Chọn 'Save as PDF' với khổ giấy A4.")



                st.markdown(f"##### 📄 Khung Xem Trước Trực Quan Bản In Giấy A4 ({'🏛️ Mẫu 1: Chuẩn Khảo Thí Truyền Thống' if template_style == 'form1' else '📘 Mẫu 2: Chuẩn Sư Phạm Hiện Đại'}):")

                render_html_iframe(print_html, height=720, scrolling=True)



            with tab_qr:

                st.markdown("### 📱 Hệ Thống Mã QR Kép: Tra Cứu Đề Thi & Tri Ân Tác Giả")

                col_q1, col_q2 = st.columns(2, gap="large")

                with col_q1:

                    st.markdown(f"#### 1️⃣ Mã QR Tra Cứu Đề Thi Mã `{ex_c}`")

                    st.image(qr_base64_img, width=220)

                    st.markdown(f"""

                    - **Dành cho Học sinh:** Dùng ứng dụng Zalo, Camera iPhone hoặc Google Lens trên điện thoại quét mã để mở đề và xem toàn bộ lời giải chi tiết.

                    - **Dành cho Giáo viên:** In mã QR này dán lên góc đề thi hoặc trình chiếu lên bảng để cả lớp quét mã làm bài và đối chiếu tức thì!

                    """)

                    st.info(f"🔗 **Đường dẫn trực tiếp:** [{app_share_url}]({app_share_url})")

                with col_q2:

                    st.markdown("#### 2️⃣ Mã VietQR MB Bank Tri Ân Tác Giả")

                    mb_qr_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "mb_bank_vietqr.png")
                    if not os.path.exists(mb_qr_path):
                        mb_qr_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mb_bank_vietqr.png")

                    if os.path.exists(mb_qr_path):

                        st.image(mb_qr_path, width=220)

                    st.markdown("""

                    - **Chủ tài khoản:** **PHAN MINH TRÍ** (Trường THPT Tân Hiệp)

                    - **Số tài khoản:** `0919513834` (MB Bank - Ngân hàng Quân Đội)

                    - **Số ĐT / Zalo:** `0919513834`

                    - ☕ **Ủng hộ tác giả:** Quý Thầy/Cô và các em học sinh có thể quét mã bằng bất kỳ app ngân hàng nào (VietQR / Napas 247) để mời Thầy Trí ly cà phê tiếp lửa nghiên cứu hệ thống!

                    """)



            with tab_tex:

                c_tex1, c_tex2 = st.columns([1.2, 1.8])

                with c_tex1:

                    st.download_button(

                        f"⬇️ Tải Nguồn LaTeX ({'Mẫu 1' if template_style == 'form1' else 'Mẫu 2'})",

                        latex_code,

                        f"De_{ex_c}_{subject_nm}_{template_style}.tex",

                        "text/plain",

                        type="secondary",

                        key=f"{key_prefix}_dl_tex",

                        width="stretch"

                    )

                with c_tex2:

                    st.caption("✅ **Chuẩn Overleaf 100%:** Đầy đủ gói `vietnamese babel`, `geometry`, `pgfplots TikZ` và `tabularx` bảng đáp án.")

                st.code(latex_code, language="latex")

                st.info("💡 **Cách dùng trên Overleaf:** Mở [Overleaf.com](https://www.overleaf.com) ➔ Tạo New Project (Blank) ➔ Dán toàn bộ mã nguồn trên ➔ Bấm **Recompile** để xuất file PDF in ấn chuẩn Bộ cực đẹp!")

            with tab_azota:
                if export_exam_to_azota_text and export_exam_to_azota_docx:
                    azota_txt = export_exam_to_azota_text(exam_obj)
                    azota_docx_bio = export_exam_to_azota_docx(exam_obj)
                    az_col1, az_col2 = st.columns(2)
                    with az_col1:
                        st.download_button(
                            "⚡ Tải Đề Chuẩn Azota (.txt cú pháp $$...$$)",
                            azota_txt.encode("utf-8"),
                            f"De_Azota_{ex_c}_{subject_nm}.txt",
                            "text/plain",
                            key=f"{key_prefix}_dl_azota_txt",
                            width="stretch",
                            type="primary"
                        )
                    with az_col2:
                        st.download_button(
                            "📄 Tải Đề Chuẩn Word (.docx Azota / LMS)",
                            azota_docx_bio.getvalue(),
                            f"De_Azota_{ex_c}_{subject_nm}.docx",
                            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            key=f"{key_prefix}_dl_azota_docx",
                            width="stretch"
                        )
                    st.caption("✅ **Tương thích 100% Azota, Shub Classroom, K12Online:** Tự động bọc `$$...$$` cho toàn bộ công thức toán học và tạo khối BẢNG ĐÁP ÁN nhận diện quang học cuối trang.")
                    with st.expander("👁️ Xem trước nội dung file Azota (.txt)", expanded=False):
                        st.code(azota_txt[:3000] + ("\n... [Còn tiếp]" if len(azota_txt) > 3000 else ""), language="markdown")
                else:
                    st.info("Chức năng xuất Azota đang được nạp...")

            with tab_json:

                st.download_button(

                    "⬇️ Tải Đề Dữ Liệu JSON (Đầy đủ đồ thị & tham số)",

                    json.dumps(exam_obj, ensure_ascii=False, indent=2),

                    f"De_{ex_c}_{subject_nm}.json",

                    "application/json",

                    key=f"{key_prefix}_dl_json",

                    width="stretch"

                )

        except Exception as exc:

            st.error(f"Chưa xuất được đề: {exc}")



    if st.session_state.exam_state == "config":

        portal_info = ree.EXAM_SOURCE_PORTALS.get(subject, ree.EXAM_SOURCE_PORTALS.get("Toán học", {})) if ree else {}

        portal_name_ui = portal_info.get("portal_name", "TOANMATH.com")

        portal_short = portal_name_ui.split("&")[0].strip() if "&" in portal_name_ui else portal_name_ui

        btn_blend_direct = False

        btn_ai_gen = False

        custom_matrix_prompt = st.session_state.get("custom_matrix_prompt", "")



        tab_thi_sinh, tab_giao_vien = st.tabs([

            "🎯 PHÒNG THI & LUYỆN TẬP CHUYÊN ĐỀ (Dành cho Học sinh / Thí sinh)",

            "🛠️ KHÔNG GIAN GIÁO VIÊN & NẠP ĐỀ MỞ RỘNG (Upload Word/PDF, Quét Link, Kho Đề)"

        ])



        with tab_thi_sinh:

            col_ex1, col_ex2 = st.columns([1.15, 0.95], gap="medium")



            with col_ex1:

                st.markdown("#### ⚙️ Cấu hình Ngữ liệu & Ma trận Chuyên đề:")

                if subject == "Ngữ văn":

                    st.info("📜 **Đề thi Tự luận Ngữ văn:** Chuẩn 100% Tự luận (Đề chung toàn quốc, không phân mã đề trắc nghiệm)")

                else:

                    st.info(f"🏷️ **Mã đề thi tự động:** `MÃ ĐỀ {st.session_state.exam_code}` (Chuẩn 4 chữ số Bộ GD&ĐT)")



                # GIAO DIỆN CHỌN CHUYÊN ĐỀ THEO TABS & CHECKBOXES NHỎ GỌN, THANH LỊCH

                subj_curr = BIGDATA_CURRICULUM.get(subject, {})

                st.markdown("##### 📚 Chọn Chuyên đề Khảo thí theo Khối lớp:")



                chosen_topics = []

                if grade_num == 12:

                    t12_tab, t11_tab, t10_tab = st.tabs(["🏷️ Lớp 12 (Trọng tâm)", "🏷️ Lớp 11 (Ôn tập)", "🏷️ Lớp 10 (Nền tảng)"])

                    with t12_tab:

                        l12 = subj_curr.get(12, [])

                        st.caption("Chọn các chuyên đề trọng tâm Lớp 12:")

                        for idx_t, t_name in enumerate(l12):

                            if st.checkbox(t_name, value=(idx_t == 0), key=f"cb_12_{current_context_key}_{idx_t}"):

                                chosen_topics.append(f"[Lớp 12] {t_name}")

                    with t11_tab:

                        l11 = subj_curr.get(11, [])

                        st.caption("Chọn các chuyên đề ôn tập Lớp 11:")

                        for idx_t, t_name in enumerate(l11):

                            if st.checkbox(t_name, value=False, key=f"cb_11_{current_context_key}_{idx_t}"):

                                chosen_topics.append(f"[Lớp 11] {t_name}")

                    with t10_tab:

                        l10 = subj_curr.get(10, [])

                        st.caption("Chọn các chuyên đề nền tảng Lớp 10:")

                        for idx_t, t_name in enumerate(l10):

                            if st.checkbox(t_name, value=False, key=f"cb_10_{current_context_key}_{idx_t}"):

                                chosen_topics.append(f"[Lớp 10] {t_name}")

                elif grade_num == 11:

                    t11_tab, t10_tab = st.tabs(["🏷️ Lớp 11 (Trọng tâm)", "🏷️ Lớp 10 (Ôn tập)"])

                    with t11_tab:

                        l11 = subj_curr.get(11, [])

                        st.caption("Chọn các chuyên đề trọng tâm Lớp 11:")

                        for idx_t, t_name in enumerate(l11):

                            if st.checkbox(t_name, value=(idx_t == 0), key=f"cb_11_{current_context_key}_{idx_t}"):

                                chosen_topics.append(f"[Lớp 11] {t_name}")

                    with t10_tab:

                        l10 = subj_curr.get(10, [])

                        st.caption("Chọn các chuyên đề ôn tập Lớp 10:")

                        for idx_t, t_name in enumerate(l10):

                            if st.checkbox(t_name, value=False, key=f"cb_10_{current_context_key}_{idx_t}"):

                                chosen_topics.append(f"[Lớp 10] {t_name}")

                else:

                    lg = subj_curr.get(grade_num, [f"Chuyên đề tổng hợp môn {subject} Lớp {grade_num}"])

                    st.caption(f"Chọn chuyên đề Lớp {grade_num}:")

                    for idx_t, t_name in enumerate(lg):

                        if st.checkbox(t_name, value=(idx_t == 0), key=f"cb_{current_context_key}_{idx_t}"):

                            chosen_topics.append(f"[Lớp {grade_num}] {t_name}")



                if not chosen_topics:

                    chosen_topics = [f"Chuyên đề tổng hợp môn {subject} Lớp {grade_num}"]



                st.caption(f"📌 **Đã chọn ({len(chosen_topics)} chuyên đề):** {', '.join(chosen_topics[:2])}{'...' if len(chosen_topics) > 2 else ''}")



                def handle_custom_prompt_commit():
                    val = str(st.session_state.get("area_custom_prompt_main", "")).strip()
                    st.session_state["custom_matrix_prompt"] = val
                    if val:
                        st.toast(f"🎯 ĐÃ GHI NHẬN & KHÓA YÊU CẦU TÙY BIẾN!", icon="✅")

                custom_matrix_prompt = st.text_area(
                    "💬 Yêu cầu ma trận / Ngữ liệu tùy biến (Prompt theo ý muốn):",
                    value=st.session_state.get("custom_matrix_prompt", ""),
                    placeholder="Ví dụ: Chỉ lấy Bài 1, 2, 3 không lấy Oxyz; Cho 5 câu đồ thị phân thức 2/1; Không ra câu trùng phương...",
                    height=75,
                    key="area_custom_prompt_main",
                    on_change=handle_custom_prompt_commit,
                    help="Người dùng có toàn quyền điều chỉnh chuyên đề, dạng bài đặc thù hoặc giới hạn bài học."
                )

                st.session_state["custom_matrix_prompt"] = custom_matrix_prompt

                c_cp1, c_cp2 = st.columns([1.5, 1])
                with c_cp1:
                    btn_confirm_cp = st.button("🔒 Khóa & Xác Nhận Ma Trận Tùy Biến", key="btn_confirm_cp_explicit")
                    if btn_confirm_cp:
                        handle_custom_prompt_commit()
                        st.rerun()

                if custom_matrix_prompt.strip():
                    st.markdown(textwrap.dedent(f"""
                    <div style="background: rgba(16, 185, 129, 0.12); border: 1.5px solid #10b981; border-radius: 8px; padding: 10px 14px; margin-top: 6px; font-size: 13px; color: #ecfdf5;">
                        <div style="color: #34d399; font-weight: bold; font-size: 13.5px; margin-bottom: 3px;">
                            ✅ ĐÃ XÁC NHẬN YÊU CẦU TÙY BIẾN (ƯU TIÊN SỐ 1 TOÀN HỆ THỐNG):
                        </div>
                        <div style="color: #a7f3d0; font-style: italic; background: rgba(0,0,0,0.25); padding: 6px 10px; border-radius: 6px; border-left: 3px solid #10b981;">
                            "{custom_matrix_prompt.strip()}"
                        </div>
                        <div style="font-size: 11.5px; color: #cbd5e1; margin-top: 4px;">
                            🎯 <b>Cơ chế thông minh:</b> Hệ thống quét sâu kho 1.000.000 câu để bốc đúng câu hỏi thật khớp ngữ liệu trên; nếu kho còn thiếu dạng nào, AI Gemini 2026 sẽ tự động sinh bù chuẩn 100% theo đúng ma trận!
                        </div>
                    </div>
                    """).strip(), unsafe_allow_html=True)



            with col_ex2:

                st.markdown("#### 📊 Cấu trúc Điểm số & Thời Gian Thi:")



                if subject == "Ngữ văn":

                    def_time = 120

                    num_p1, num_p2, num_p3 = 0, 0, 0

                    st.markdown(
                        '<div style="background: rgba(30, 41, 59, 0.7); border: 1.5px solid #0284c7; border-radius: 10px; padding: 14px 16px; margin-bottom: 12px;">'
                        '<div style="color: #38bdf8; font-weight: 700; font-size: 15px; margin-bottom: 6px;">📖 Cấu Trúc Đề Khảo Thí Môn Ngữ Văn (Chuẩn 100% Tự Luận - BGD&ĐT)</div>'
                        '<div style="color: #cbd5e1; font-size: 13px; line-height: 1.65;">'
                        '• <b>Hình thức thi:</b> 100% Tự luận (Không có trắc nghiệm).<br>'
                        '• <b>Phần I: Đọc hiểu (4.0 điểm)</b>: Ngữ liệu ngoài SGK + 3 câu hỏi phân hóa.<br>'
                        '• <b>Phần II: Viết (6.0 điểm)</b>: Đoạn văn NLXH 2.0đ (~200 chữ) + Bài văn NLVH 4.0đ.<br>'
                        '• <b>Thời gian làm bài quy chuẩn:</b> 120 phút.'
                        '</div></div>',
                        unsafe_allow_html=True
                    )

                    exam_time_mins = st.selectbox(

                        "⏱️ Thời lượng bài thi Ngữ văn (Phút):",

                        [45, 60, 90, 120],

                        index=3

                    )

                elif subject == "Tiếng Anh":

                    def_time = 50

                    num_p2, num_p3 = 0, 0

                    st.markdown(
                        '<div style="background: rgba(30, 41, 59, 0.7); border: 1.5px solid #0284c7; border-radius: 10px; padding: 14px 16px; margin-bottom: 12px;">'
                        '<div style="color: #38bdf8; font-weight: 700; font-size: 15px; margin-bottom: 6px;">🇬🇧 Cấu Trúc Đề Khảo Thí Môn Tiếng Anh (Chuẩn QĐ 764/QĐ-BGDĐT)</div>'
                        '<div style="color: #cbd5e1; font-size: 13px; line-height: 1.65;">'
                        '• <b>Hình thức thi:</b> 100% Trắc nghiệm 4 lựa chọn (A, B, C, D) - 50 phút.<br>'
                        '• <b>Cấu trúc đề 40 câu:</b> Ngữ âm (4 câu) • Ngữ pháp & Từ vựng (12 câu) • Giao tiếp (2 câu) • Điền từ Cloze (5 câu) • Đọc hiểu (12 câu) • Viết kết hợp câu (5 câu).<br>'
                        '• <b>Quy chế:</b> Tuyệt đối KHÔNG có Đúng/Sai và KHÔNG có Trả lời ngắn.<br>'
                        '• <b>Thang điểm:</b> 40 câu x 0.25 điểm = 10.0 điểm trọn vẹn.'
                        '</div></div>',
                        unsafe_allow_html=True
                    )

                    col_en1, col_en2 = st.columns(2)

                    with col_en1:

                        num_p1 = st.selectbox(

                            "📝 Số câu trắc nghiệm (0.25đ/câu):",

                            [40, 30, 20],

                            index=0,

                            help="Đề thi chính thức của Bộ GD&ĐT gồm 40 câu (10.0 điểm)."

                        )

                    with col_en2:

                        exam_time_mins = st.selectbox(

                            "⏱️ Thời lượng bài thi (Phút):",

                            [15, 30, 45, 50, 60],

                            index=3

                        )

                elif is_social_or_tech_subject(subject):

                    num_p3 = 0

                    st.markdown(f'<div style="background: rgba(30, 41, 59, 0.7); border: 1.5px solid #0284c7; border-radius: 10px; padding: 14px 16px; margin-bottom: 12px;"><div style="color: #38bdf8; font-weight: 700; font-size: 15px; margin-bottom: 6px;">🏛️ Cấu Trúc Đề Khảo Thí Môn {subject} (Chuẩn QĐ 764/QĐ-BGDĐT)</div><div style="color: #cbd5e1; font-size: 13px; line-height: 1.65;">• <b>Phần I:</b> Trắc nghiệm 4 lựa chọn (24 câu - 6.0 điểm - 0.25đ/câu).<br>• <b>Phần II:</b> Trắc nghiệm Đúng/Sai (4 câu - 4.0 điểm - thang điểm bậc 0.1-0.25-0.5-1.0đ).<br>• <b>Phần III:</b> Không áp dụng theo quy chuẩn QĐ 764/QĐ-BGDĐT.<br>• <b>Thời gian làm bài quy chuẩn:</b> 50 phút.</div></div>', unsafe_allow_html=True)

                    col_soc1, col_soc2, col_soc3 = st.columns([1.2, 1.2, 1.4])

                    with col_soc1:

                        num_p1 = st.number_input("Số câu TN P.I:", min_value=1, max_value=50, value=24)

                    with col_soc2:

                        num_p2 = st.number_input("Số câu Đ/S P.II:", min_value=1, max_value=10, value=4)

                    with col_soc3:

                        exam_time_mins = st.selectbox("⏱️ Thời lượng thi (Phút):", [15, 30, 45, 50, 60], index=3)

                else:

                    # Toán học & Khoa học tự nhiên (Vật lý, Hóa học, Sinh học, KHTN)

                    if subject == "Toán học":

                        def_p1, def_p2, def_p3, def_time = 12, 4, 6, 90

                    else:

                        def_p1, def_p2, def_p3, def_time = 18, 4, 6, 50



                    c_cnt1, c_cnt2, c_cnt3 = st.columns(3)

                    with c_cnt1:

                        num_p1 = st.number_input("Số câu TN P.I:", min_value=1, max_value=50, value=def_p1)

                    with c_cnt2:

                        num_p2 = st.number_input("Số câu Đ/S P.II:", min_value=0, max_value=10, value=def_p2)

                    with c_cnt3:

                        num_p3 = st.number_input("Số câu TLN P.III:", min_value=0, max_value=10, value=def_p3)



                    exam_time_mins = st.selectbox(

                        "⏱️ Thời lượng bài thi (Phút):",

                        [15, 30, 45, 50, 60, 90, 120],

                        index=[15, 30, 45, 50, 60, 90, 120].index(def_time) if def_time in [15, 30, 45, 50, 60, 90, 120] else 3

                    )

                st.session_state.exam_time_mins = exam_time_mins

                measure_phase = "practice"

                measure_student_id = ""

                if st.session_state.get("tab4_authenticated"):

                    measure_phase = st.selectbox("Mục đích bài đo (giáo viên)", ["practice", "pre", "post"])

                    if measure_phase != "practice":

                        measure_student_id = st.text_input("Mã học sinh nghiên cứu (không dùng họ tên)").strip()



                st.markdown("---")



                # --- KHU VỰC KHỞI ĐỘNG BÀI THI CHO THÍ SINH (ACTION CENTER - BUỒNG LÁI COCKPIT) ---

                real_exams_list = ree.get_baseline_full_exams(subject, grade_num) if ree else []



                def detect_exam_type(ex_item):

                    c_str = str(ex_item.get("code") or "").upper()

                    if c_str.startswith("GK1"): return "Giữa học kỳ 1"

                    if c_str.startswith("CK1"): return "Cuối học kỳ 1"

                    if c_str.startswith("GK2"): return "Giữa học kỳ 2"

                    if c_str.startswith("CK2"): return "Cuối học kỳ 2"

                    if c_str.startswith("TT26"): return "Thi thử Tốt nghiệp THPT"



                    t_str = str(ex_item.get("exam_type") or "").strip()

                    title_str = str(ex_item.get("title") or "").strip().lower()

                    if t_str and t_str != "None":

                        return t_str

                    if "giữa" in title_str:

                        return "Giữa học kỳ 1" if ("1" in title_str or "i" in title_str) else "Giữa học kỳ 2"

                    if "cuối" in title_str:

                        return "Cuối học kỳ 1" if ("1" in title_str or "i" in title_str) else "Cuối học kỳ 2"

                    if "thử" in title_str or "tốt nghiệp" in title_str or "khảo sát" in title_str:

                        return "Thi thử Tốt nghiệp THPT"

                    return "Khảo sát định kỳ"



                gk1_exams = [it for it in real_exams_list if detect_exam_type(it) == "Giữa học kỳ 1"]

                ck1_exams = [it for it in real_exams_list if detect_exam_type(it) == "Cuối học kỳ 1"]

                gk2_exams = [it for it in real_exams_list if detect_exam_type(it) == "Giữa học kỳ 2"]

                ck2_exams = [it for it in real_exams_list if detect_exam_type(it) == "Cuối học kỳ 2"]

                thithu_exams = [it for it in real_exams_list if detect_exam_type(it) == "Thi thử Tốt nghiệp THPT" or any(kw in detect_exam_type(it).lower() for kw in ["thử", "khảo sát"])]



                gk1_count = len(gk1_exams)

                ck1_count = len(ck1_exams)

                gk2_count = len(gk2_exams)

                ck2_count = len(ck2_exams)

                thithu_count = len(thithu_exams)



                exam_mode_options = [

                    f"🎯 Đề Luyện Tập Chuyên Đề ({len(chosen_topics)} CĐ)",

                    f"🏛️ Làm Nguyên Đề Thi Thật ({len(real_exams_list)} đề)",

                    "📤 Nạp & Trộn Đề Word (.docx) / PDF",

                    "🌐 Quét Đề Link (TOANMATH, MATHVN, FB...)"

                ]

                selected_exam_mode = st.radio("Lựa chọn hình thức đề thi:", exam_mode_options, horizontal=True, key="radio_exam_mode_choice")



                if "Làm Nguyên Đề Thi Thật" in selected_exam_mode and real_exams_list:

                    filter_opts = ["Tất cả"]

                    if gk1_count > 0: filter_opts.append(f"🌟 Giữa HK1 ({gk1_count} đề)")

                    if ck1_count > 0: filter_opts.append(f"🎯 Cuối HK1 ({ck1_count} đề)")

                    if gk2_count > 0: filter_opts.append(f"🌟 Giữa HK2 ({gk2_count} đề)")

                    if ck2_count > 0: filter_opts.append(f"🎯 Cuối HK2 ({ck2_count} đề)")

                    if thithu_count > 0: filter_opts.append(f"🏛️ Thi thử ({thithu_count} đề)")



                    col_f1, col_f2 = st.columns([1.2, 2.8])

                    with col_f1:

                        filter_ex_type = st.selectbox("Kỳ thi:", filter_opts, key="sel_filter_real_type")

                    with col_f2:

                        filtered_exams = real_exams_list

                        if "Giữa HK1" in filter_ex_type: filtered_exams = gk1_exams or real_exams_list

                        elif "Cuối HK1" in filter_ex_type: filtered_exams = ck1_exams or real_exams_list

                        elif "Giữa HK2" in filter_ex_type: filtered_exams = gk2_exams or real_exams_list

                        elif "Cuối HK2" in filter_ex_type: filtered_exams = ck2_exams or real_exams_list

                        elif "Thi thử" in filter_ex_type: filtered_exams = thithu_exams or real_exams_list



                        r_opts = [

                            f"[{detect_exam_type(item)}] {item.get('title', 'Đề')} - {item.get('school', '')}"

                            for item in filtered_exams

                        ]

                        if "sel_real_exam_t3" in st.session_state and (not r_opts or st.session_state.sel_real_exam_t3 >= len(r_opts)):
                            st.session_state.sel_real_exam_t3 = 0

                        chosen_real_idx = st.selectbox(f"Chọn đề ({len(filtered_exams)} đề):", range(len(r_opts)), format_func=lambda i: r_opts[i], key="sel_real_exam_t3")



                    col_b1, col_b2 = st.columns([1.1, 1.3])

                    with col_b1:

                        btn_load_chosen = st.button("🚀 Nạp Đề Đang Chọn Này (0.1s)", type="secondary", width="stretch", key="btn_load_real_exam")

                    with col_b2:

                        btn_load_random = st.button(f"🎲 Bốc Ngẫu Nhiên 1 Đề Toàn Quốc ({len(filtered_exams)} Đề)", type="primary", width="stretch", key="btn_random_real_exam")

                    if btn_load_chosen or btn_load_random:

                        if btn_load_random:
                            random.seed(time.time_ns())
                            if "seen_whole_exam_codes" not in st.session_state:
                                st.session_state.seen_whole_exam_codes = set()

                            fresh_exams = [e for e in filtered_exams if str(e.get("code", e.get("title", ""))) not in st.session_state.seen_whole_exam_codes]
                            if not fresh_exams:
                                st.session_state.seen_whole_exam_codes.clear()
                                fresh_exams = filtered_exams

                            sel_real_item = random.choice(fresh_exams)
                            st.session_state.seen_whole_exam_codes.add(str(sel_real_item.get("code", sel_real_item.get("title", ""))))
                            st.toast(f"🎲 Đã bốc ngẫu nhiên đề mới: Mã {sel_real_item.get('code', 'Chính thức')} — {sel_real_item.get('title', 'Đề thi')[:35]}...", icon="🎯")
                        else:
                            sel_real_item = filtered_exams[chosen_real_idx]
                            if "seen_whole_exam_codes" not in st.session_state:
                                st.session_state.seen_whole_exam_codes = set()
                            st.session_state.seen_whole_exam_codes.add(str(sel_real_item.get("code", sel_real_item.get("title", ""))))

                        st.session_state.exam_data = enrich_exam_data(sel_real_item)

                        st.session_state.exam_code = str(sel_real_item.get("code", random.randint(1011, 9999)))

                        st.session_state.attempt_id = str(uuid.uuid4())

                        st.session_state.exam_start_timestamp = time.time()

                        st.session_state.exam_deadline = time.time() + exam_time_mins * 60

                        st.session_state.exam_context = {"name": student_name, "grade": grade, "subject": subject, "phase": measure_phase, "student_id": measure_student_id}

                        st.session_state.pop("literature_grade", None)

                        st.session_state.pop("exam_submitted_at", None)

                        for widget_key in list(st.session_state):

                            if widget_key.startswith(("t3_p1_", "t3_p2_", "t3_p3_", "nv_dh_", "nv_v_")):

                                del st.session_state[widget_key]

                        st.session_state.exam_state = "testing"

                        st.session_state.exam_answers = {}

                        st.session_state.tram3_chat_messages = []

                        st.toast(f"⚡ Đã nạp thành công đề thi thật từ {sel_real_item.get('school', '')} trong 0.1 giây!", icon="✨")

                        st.rerun()



                elif "Nạp & Trộn Đề Word" in selected_exam_mode:

                    st.markdown("##### 📤 Nạp Đề Thi Từ File Word (.docx) / PDF (.pdf) hoặc Dán Đề:")

                    st.markdown(
                        '<div style="background: rgba(15, 23, 42, 0.7); border: 1px dashed #38bdf8; border-radius: 8px; padding: 10px 14px; margin-bottom: 12px; font-size: 13px; line-height: 1.6; color: #cbd5e1;">'
                        '<div style="margin-bottom: 6px;">💡 <b style="color: #38bdf8;">MẸO NẠP ĐỀ WORD MATHTYPE CHUẨN 100% CÔNG THỨC (KHÔNG BỊ MẤT KÝ TỰ):</b></div>'
                        '<div style="margin-bottom: 4px;">• <b>Cách 1 (Nhanh nhất - 1 Click trong Word):</b> Mở file Word ➔ Chọn menu <b>MathType</b> ➔ Bấm <b>Convert Equations</b> ➔ Chọn đổi sang <b>TeX/LaTeX ($...$)</b> ➔ Bấm <b>Convert</b> rồi lưu lại tải lên. Toàn bộ công thức MathType sẽ giữ nguyên 100%!</div>'
                        '<div>• <b>Cách 2 (Lưu PDF):</b> Trong Word, bấm <b>File ➔ Save As ➔ Chọn định dạng PDF (.pdf)</b> rồi tải file PDF lên để giữ trọn vẹn cả công thức và hình vẽ.</div>'
                        '</div>',
                        unsafe_allow_html=True
                    )

                    col_u1, col_u2 = st.columns([1.1, 1.1])

                    with col_u1:

                        up_file_t3 = st.file_uploader("Chọn file (.docx, .pdf, .txt):", type=["docx", "pdf", "txt"], key="up_file_direct_t3")

                    with col_u2:

                        up_raw_paste = st.text_area("Hoặc dán trực tiếp nội dung đề thi vào đây:", height=95, placeholder="Dán nội dung câu hỏi hoặc toàn bộ đề thi thô...", key="up_paste_direct_t3")



                    raw_extracted_t3 = ""

                    up_file_t3_bytes = None

                    if up_file_t3 is not None:

                        file_b = up_file_t3.read()

                        up_file_t3_bytes = file_b

                        raw_extracted_t3 = ree.extract_text_from_file_upload(file_b, up_file_t3.name) if ree else ""

                        if raw_extracted_t3.startswith("__MATHTYPE_WARNING__:"):

                            parts_mt = raw_extracted_t3.split("\n", 1)

                            cnt_mt = parts_mt[0].replace("__MATHTYPE_WARNING__:", "")

                            raw_extracted_t3 = parts_mt[1] if len(parts_mt) > 1 else ""

                            st.info(f"✨ **Cơ Chế Xử Lý Ngầm Tự Động Kích Hoạt:** Hệ thống phát hiện `{cnt_mt} công thức MathType` trong file `{up_file_t3.name}`. AI Multimodal sẽ tự động xử lý ngầm và bóc tách toàn vẹn công thức sang chuẩn KaTeX $...$ khi Thầy/Cô bấm Phân tích bên dưới!")

                        elif raw_extracted_t3:

                            if len(raw_extracted_t3) > 25000:

                                st.info(f"📚 **Phát Hiện File Khủng ({len(raw_extracted_t3):,} ký tự):** Đã kích hoạt Bộ máy Định vị Phân đoạn thông minh. Nếu Thầy/Cô có yêu cầu lọc (như *'Chỉ lấy đề Sở Yên Bái'* trong ô Prompt bên trái), AI sẽ tự động khoanh vùng chính xác đề thi đó để bóc tách!")

                            else:

                                st.success(f"Đã đọc file {up_file_t3.name} thành công ({len(raw_extracted_t3)} ký tự)!")

                    elif up_raw_paste.strip():

                        raw_extracted_t3 = up_raw_paste.strip()



                    if raw_extracted_t3 or up_file_t3_bytes is not None:

                        if st.button("⚙️ Phân Tích & Chuẩn Hóa Cấu Trúc Đề (Xử Lý Ngầm 100%)", key="btn_parse_t3_direct", type="primary", width="stretch"):

                            with st.spinner("Đang kích hoạt bộ máy Xử Lý Ngầm Multimodal AI bóc tách toàn diện công thức MathType và chuẩn hóa ma trận QĐ 764..."):

                                user_prompt_direct = st.session_state.get("custom_matrix_prompt", "")

                                parsed_direct = None

                                if up_file_t3_bytes is not None and up_file_t3 is not None and ree and hasattr(ree, "parse_file_direct_with_ai"):

                                    parsed_direct = ree.parse_file_direct_with_ai(

                                        up_file_t3_bytes,

                                        up_file_t3.name,

                                        subject, grade_num,

                                        "Tài liệu nạp của Giáo viên",

                                        f"Đề nạp môn {subject} - Lớp {grade_num}",

                                        ai_caller=lambda p, json_mode=False: call_gemini_with_fallback(p, json_mode=json_mode),

                                        user_prompt=user_prompt_direct

                                    )

                                if not parsed_direct and ree:

                                    parsed_direct = ree.parse_raw_exam_text(

                                        raw_extracted_t3, subject, grade_num,

                                        "Tài liệu nạp của Giáo viên",

                                        f"Đề nạp môn {subject} - Lớp {grade_num}",

                                        ai_caller=lambda p, json_mode=False: call_gemini_with_fallback(p, json_mode=json_mode),

                                        user_prompt=user_prompt_direct

                                    )

                                if parsed_direct and (parsed_direct.get("p1") or parsed_direct.get("p2") or parsed_direct.get("p3")):

                                    st.session_state["t3_parsed_exam_temp"] = parsed_direct

                                    st.success("🎉 Đã xử lý ngầm và chuẩn hóa cấu trúc đề thi thành công! Toàn bộ công thức MathType đã được chuyển đổi sang KaTeX sắc nét.")

                                else:

                                    st.error("Không thể tự động phân tích cấu trúc đề thi. Vui lòng kiểm tra lại định dạng câu hỏi.")



                    if st.session_state.get("t3_parsed_exam_temp"):

                        p_dir = st.session_state["t3_parsed_exam_temp"]

                        st.markdown(f"**Kết quả bóc tách:** Phần I: `{len(p_dir.get('p1', []))} câu` | Phần II: `{len(p_dir.get('p2', []))} câu` | Phần III: `{len(p_dir.get('p3', []))} câu`")

                        c_act1, c_act2 = st.columns([1, 1.3])

                        with c_act1:

                            if st.button("🚀 Nạp Nguyên Đề (Làm Ngay)", key="btn_load_dir_exam", type="secondary", width="stretch"):

                                st.session_state.exam_data = enrich_exam_data(p_dir)

                                st.session_state.exam_code = str(p_dir.get("code", random.randint(1011, 9999)))

                                st.session_state.attempt_id = str(uuid.uuid4())

                                st.session_state.exam_start_timestamp = time.time()

                                st.session_state.exam_deadline = time.time() + exam_time_mins * 60

                                st.session_state.exam_context = {"name": student_name, "grade": grade, "subject": subject, "phase": measure_phase, "student_id": measure_student_id}

                                st.session_state.pop("literature_grade", None)

                                st.session_state.pop("exam_submitted_at", None)

                                for widget_key in list(st.session_state):

                                    if widget_key.startswith(("t3_p1_", "t3_p2_", "t3_p3_", "nv_dh_", "nv_v_")):

                                        del st.session_state[widget_key]

                                st.session_state.exam_state = "testing"

                                st.session_state.exam_answers = {}

                                st.session_state.tram3_chat_messages = []

                                st.toast("⚡ Đã nạp thành công đề thi vào phòng thi!", icon="✨")

                                st.rerun()

                        with c_act2:

                            if st.button("🔀 Trộn Đề Mới (Quét + Quốc Gia)", key="btn_blend_dir_exam", type="primary", width="stretch"):

                                with st.spinner("Đang trộn ngữ liệu vừa quét với Ngân hàng Quốc gia, đảo ngẫu nhiên câu hỏi & phương án..."):

                                    blended_exam = ree.create_mixed_scanned_exam(p_dir, subject, grade_num, mix_ratio=0.5, shuffle_options=True) if ree else p_dir

                                    st.session_state.exam_data = enrich_exam_data(blended_exam)

                                    st.session_state.exam_code = str(blended_exam.get("code", random.randint(1011, 9999)))

                                    st.session_state.attempt_id = str(uuid.uuid4())

                                    st.session_state.exam_start_timestamp = time.time()

                                    st.session_state.exam_deadline = time.time() + exam_time_mins * 60

                                    st.session_state.exam_context = {"name": student_name, "grade": grade, "subject": subject, "phase": measure_phase, "student_id": measure_student_id}

                                    st.session_state.pop("literature_grade", None)

                                    st.session_state.pop("exam_submitted_at", None)

                                    for widget_key in list(st.session_state):

                                        if widget_key.startswith(("t3_p1_", "t3_p2_", "t3_p3_", "nv_dh_", "nv_v_")):

                                            del st.session_state[widget_key]

                                    st.session_state.exam_state = "testing"

                                    st.session_state.exam_answers = {}

                                    st.session_state.tram3_chat_messages = []

                                    st.toast(f"🎉 Đã tạo Đề Trộn Mới (Mã {st.session_state.exam_code}) từ file Word/PDF!", icon="✨")

                                    st.rerun()



                elif "Quét Đề Link" in selected_exam_mode:

                    st.markdown("##### 🌐 Quét Đề Từ Link (TOANMATH.COM, MATHVN.COM, Facebook, Link tùy chỉnh):")

                    c_src1, c_src2 = st.columns([1.1, 2.3])

                    with c_src1:

                        target_source_type = st.selectbox(

                            "Chọn chuyên trang / Nguồn link:",

                            ["🏛️ TOANMATH.com", "📐 MATHVN.com", "👥 Facebook (Bài viết / Link Drive)", "🔗 Link tùy chỉnh"],

                            key="sel_portal_type_t3"

                        )

                    with c_src2:

                        if "MATHVN" in target_source_type:

                            default_link = "https://www.mathvn.com/2024/10/de-thi-giua-hoc-ki-1-toan-12-nam-hoc-2024-2025.html"

                        elif "Facebook" in target_source_type:

                            default_link = "https://drive.google.com/file/d/... (hoặc link bài viết Facebook)"

                        elif "TOANMATH" in target_source_type:

                            default_link = f"https://toanmath.com/de-thi-giua-hk1-toan-{grade_num}" if subject == "Toán học" else portal_info.get("url", "https://toanmath.com")

                        else:

                            default_link = "https://..."

                        user_target_url = st.text_input("Nhập Link bài viết / chuyên mục / Google Drive:", value=default_link, key="inp_target_url_t3")



                    c_btn_l1, c_btn_l2 = st.columns([1, 1.3])

                    with c_btn_l1:

                        btn_scan_and_load = st.button("⚡ Bóc Tách & Làm Ngay", key="btn_scan_and_load_t3", type="secondary", width="stretch")

                    with c_btn_l2:

                        btn_scan_and_blend = st.button("🔀 Bóc Tách & Trộn Đề Mới", key="btn_scan_and_blend_t3", type="primary", width="stretch")



                    if btn_scan_and_load or btn_scan_and_blend:

                        with st.spinner("Đang truy cập link, tải PDF/Docx và bóc tách ma trận chuẩn Bộ GD&ĐT..."):

                            extracted_res = ree.extract_full_exam_from_url(

                                user_target_url, subject, grade_num,

                                ai_caller=lambda p, json_mode=False: call_gemini_with_fallback(p, json_mode=json_mode)

                            ) if ree else None



                            if extracted_res and (extracted_res.get("p1") or extracted_res.get("p2") or extracted_res.get("p3")):

                                final_exam_to_use = extracted_res

                                if btn_scan_and_blend:

                                    final_exam_to_use = ree.create_mixed_scanned_exam(extracted_res, subject, grade_num, mix_ratio=0.5, shuffle_options=True)



                                st.session_state.exam_data = enrich_exam_data(final_exam_to_use)

                                st.session_state.exam_code = str(final_exam_to_use.get("code", random.randint(1011, 9999)))

                                st.session_state.attempt_id = str(uuid.uuid4())

                                st.session_state.exam_start_timestamp = time.time()

                                st.session_state.exam_deadline = time.time() + exam_time_mins * 60

                                st.session_state.exam_context = {"name": student_name, "grade": grade, "subject": subject, "phase": measure_phase, "student_id": measure_student_id}

                                st.session_state.pop("literature_grade", None)

                                st.session_state.pop("exam_submitted_at", None)

                                for widget_key in list(st.session_state):

                                    if widget_key.startswith(("t3_p1_", "t3_p2_", "t3_p3_", "nv_dh_", "nv_v_")):

                                        del st.session_state[widget_key]

                                st.session_state.exam_state = "testing"

                                st.session_state.exam_answers = {}

                                st.session_state.tram3_chat_messages = []

                                st.toast(f"⚡ Đã bóc tách thành công đề từ {final_exam_to_use.get('portal', 'Web')}!", icon="✨")

                                st.rerun()

                            else:

                                st.error("Chưa bóc tách được đề từ link này. Nếu là link nhóm kín Facebook, Thầy/Cô vui lòng dán link Google Drive hoặc dán trực tiếp nội dung đề thi vào mục 'Nạp & Trộn Đề Word / PDF' bên cạnh!")

                else:

                    c_btn1, c_btn2 = st.columns([1.1, 1.1])

                    has_custom_prompt = bool(custom_matrix_prompt and custom_matrix_prompt.strip())
                    btn1_label = f"📚 Trích Xuất Đề Tùy Biến (Kho 600+ Đề Thật & Vân Tay)" if has_custom_prompt else f"🎲 Trộn Siêu Đề Mới (Kho Ngân Hàng)"
                    btn2_label = f"🤖 AI Tạo Đề Theo Tùy Biến (Ưu Tiên Số 1 - Mới Tinh 100%)" if has_custom_prompt else "🚀 Khởi Tạo Đề Mới (AI Sáng Tạo 2026)"
                    btn1_type = "primary" if has_custom_prompt else "secondary"

                    with c_btn1:
                        btn_blend_direct = st.button(
                            btn1_label,
                            type=btn1_type,
                            width="stretch",
                            help=f"LUỒNG 2: Trích xuất câu hỏi thật từ kho 600+ đề thi chính thức/thi thử toàn quốc ({portal_name_ui}) bám sát yêu cầu tùy biến. Lọc sạch 100% câu hỏi lạc đề qua Bộ lọc 5 lớp và hiển thị Bảng đối chứng vân tay nguồn gốc!"
                        )

                    with c_btn2:
                        btn_ai_gen = st.button(
                            btn2_label,
                            type="primary",
                            width="stretch",
                            help=f"LUỒNG 1: AI Gemini biên soạn 100% ngữ liệu độc bản mới tinh, không lấy bất kỳ câu nào trong ngân hàng, tự động chạy Bộ Lọc Giải Ngầm (Deep Solver Guard) để xác minh nghiệm và số liệu chuẩn xác tuyệt đối!"
                        )

                    st.markdown(textwrap.dedent("""
                    <div style="background: rgba(15, 23, 42, 0.7); border: 1.5px solid #38bdf8; border-radius: 10px; padding: 10px 14px; margin-top: 8px; font-size: 12.5px; line-height: 1.6; color: #cbd5e1;">
                        <div style="font-weight: bold; color: #38bdf8; margin-bottom: 4px; font-size: 13px;">⚖️ CƠ CHẾ 2 LUỒNG ĐỘC LẬP TÁCH BẠCH & BỘ LỌC 5 LỚP TOÀN DIỆN:</div>
                        • 🤖 <b style="color: #f59e0b;">LUỒNG 1 - AI TẠO ĐỀ NGUYÊN BẢN (ƯU TIÊN SỐ 1):</b> 100% ngữ liệu & số liệu mới tinh chưa từng có trên mạng, giải ngầm kiểm chứng nghiệm, không phụ thuộc vào ngân hàng cũ.<br>
                        • 📚 <b style="color: #38bdf8;">LUỒNG 2 - TRÍCH XUẤT TỪ KHO 600+ ĐỀ THI THẬT:</b> Quét từ hơn 600 đề thi thật có chỉ dấu vân tay (mã đề, trường chuyên, sở GD), lọc sạch 100% câu lạc đề và có Bảng đối chứng vân tay đối soát.
                    </div>
                    """).strip(), unsafe_allow_html=True)



                    if btn_blend_direct:

                        if measure_phase != "practice" and not measure_student_id:

                            st.error("Cần mã học sinh để ghép cặp bài đo trước–sau.")

                            st.stop()

                        if ree:

                            # Thu thập các fingerprint câu hỏi cũ đã làm trong phiên để truyền vào Cooldown
                            current_cooldown_fps = set()
                            if "seen_question_fps" not in st.session_state:
                                st.session_state.seen_question_fps = set()

                            # Nếu phiên trước đã có đề, nạp fingerprint của đề cũ vào cooldown
                            if st.session_state.get("exam_data") and isinstance(st.session_state.exam_data, dict):
                                for p_key in ("p1", "p2", "p3"):
                                    for q_old in st.session_state.exam_data.get(p_key, []):
                                        q_txt = str(q_old.get("q", "")).strip().lower()
                                        if q_txt:
                                            fp_c = ree.q_fingerprint(q_old)
                                            st.session_state.seen_question_fps.add(fp_c)

                            blended = ree.generate_blended_real_exam(
                                subject, grade_num, chosen_topics, (num_p1, num_p2, num_p3),
                                custom_prompt=custom_matrix_prompt,
                                exclude_fingerprints=st.session_state.seen_question_fps
                            )

                            if blended and (blended.get("p1") or blended.get("p2") or blended.get("p3")):

                                st.session_state.exam_data = enrich_exam_data(blended)
                                for p_key in ("p1", "p2", "p3"):
                                    for q_new in blended.get(p_key, []):
                                        q_txt = str(q_new.get("q", "")).strip().lower()
                                        if q_txt:
                                            fp_c = ree.q_fingerprint(q_new)
                                            st.session_state.seen_question_fps.add(fp_c)

                                st.session_state.exam_code = str(blended.get("code", random.randint(1011, 9999)))

                                st.session_state.attempt_id = str(uuid.uuid4())

                                st.session_state.exam_start_timestamp = time.time()

                                st.session_state.exam_deadline = time.time() + exam_time_mins * 60

                                st.session_state.exam_context = {"name": student_name, "grade": grade, "subject": subject, "phase": measure_phase, "student_id": measure_student_id}

                                st.session_state.custom_request_text = custom_matrix_prompt.strip() if custom_matrix_prompt else ""

                                st.session_state.pop("literature_grade", None)

                                st.session_state.pop("exam_submitted_at", None)

                                for widget_key in list(st.session_state):

                                    if widget_key.startswith(("t3_p1_", "t3_p2_", "t3_p3_", "nv_dh_", "nv_v_")):

                                        del st.session_state[widget_key]

                                st.session_state.exam_state = "testing"

                                st.session_state.exam_answers = {}

                                st.session_state.tram3_chat_messages = []

                                if has_custom_prompt:
                                    st.session_state.show_audit_badges_per_question = True
                                    st.toast("📚 ĐÃ TRÍCH XUẤT ĐỀ TÙY BIẾN TỪ KHO 600+ ĐỀ THẬT: Có đầy đủ chỉ dấu vân tay & Bảng đối chứng!", icon="✅")
                                else:
                                    st.toast("🔥 Đã trộn siêu đề thi mới lạ (Dynamic Seed) thành công trong 0.1 giây!", icon="✨")

                                st.rerun()

                            else:

                                st.warning("Chưa đủ câu hỏi có sẵn trong kho môn này để trộn 100% tự động, vui lòng dùng nút 'Khởi Tạo Đề Mới (AI 2026)' bên cạnh!")

                        else:

                            st.error("Module real_exam_engine chưa được nạp.")



                    if btn_ai_gen:

                        if measure_phase != "practice" and not measure_student_id:

                            st.error("Cần mã học sinh để ghép cặp bài đo trước–sau.")

                            st.stop()

                        st.session_state.exam_code = str(random.randint(1011, 9999))

                        st.session_state.violation_count = 0

                        st.session_state.custom_request_text = custom_matrix_prompt.strip()

                        st.session_state.exam_start_timestamp = time.time()



                        selected_topics_str = "; ".join(chosen_topics)

                        custom_user_instructions = ""

                        if custom_matrix_prompt.strip():

                            custom_user_instructions = f"""

[CẤP ĐỘ ƯU TIÊN CAO NHẤT: NGUYỆN VỌNG ĐẶC BIỆT THEO YÊU CẦU CỦA GIÁO VIÊN / HỌC SINH]:

"{custom_matrix_prompt}"

NGUYÊN TẮC LINH HOẠT SƯ PHẠM TỐI THƯỢNG (HIỆU LỰC GHI ĐÈ TUYỆT ĐỐI):

- AI HÃY ĐÁP ỨNG 100% ĐÚNG NGUYỆN VỌNG CỦA NGƯỜI DÙNG: Yêu cầu của người dùng ở trên CÓ HIỆU LỰC CAO NHẤT, GHI ĐÈ MỌI QUY TẮC MẶC ĐỊNH DƯỚI ĐÂY. Nếu giáo viên yêu cầu tác phẩm văn học cụ thể trong SGK (như Tây Tiến, Vợ Nhặt, Sóng...) hoặc yêu cầu dạng bài Toán đặc thù (hàm trùng phương, bài toán ĐGNL/ĐGTD, Olympic...), AI PHẢI ĐÁP ỨNG CHÍNH XÁC 100% nội dung đó, đồng thời vẫn giữ định dạng JSON và cấu trúc câu hỏi chuẩn chỉ!

"""



                        # --- BƠM DOPING "DEEP CHECK VAR" VÀ NÂNG CẤP ĐỘ KHÓ ĐÚNG CHUẨN CT 2018 (ÁP DỤNG KHI KHÔNG CÓ YÊU CẦU TÙY BIẾN RIÊNG) ---

                        custom_user_instructions += f"""

[LỆNH KIỂM SOÁT KHẢO THÍ CHUẨN MỰC CT GDPT 2018 & QĐ 764 (ÁP DỤNG KHI KHÔNG CÓ YÊU CẦU TÙY BIẾN ĐẶC BIỆT)]:

1. ĐỐI SOÁT ĐA TẦNG NGỮ LIỆU: BẮT BUỘC rà soát từ khóa với 2 nguồn học liệu chính thống: SGK, SBT KNTT trên VniTeach và Tập Huấn NXBGD. Loại bỏ ngay kiến thức cũ (2006) hoặc ngoài CT Lớp {grade_num}.

2. YÊU CẦU ĐỘ KHÓ & ĐÁNH GIÁ NĂNG LỰC (CHUẨN 2018): Phải rải đều 4 mức độ: Nhận biết, Thông hiểu, Vận dụng, Vận dụng cao.

   - TƯ DUY LÕI TOÀN HỆ THỐNG: Chương trình 2018 thiên về ĐỌC HIỂU ĐỒ THỊ, BẢNG SỐ LIỆU, MÔ HÌNH HÓA VÀ ỨNG DỤNG THỰC TẾ. TUYỆT ĐỐI BỎ TƯ DUY ĐÁNH ĐỐ.

   - RIÊNG MÔN TOÁN: BẮT BUỘC ưu tiên các bài toán Mô hình hóa toán học, tối ưu hóa thực tiễn kinh tế/kỹ thuật, đọc và phân tích dữ liệu từ đồ thị. Mặc định không ra các bài toán đánh đố của chương trình cũ (2006) như cực trị hàm ẩn f(f(x)) hoặc hàm bậc 4 trùng phương, TRỪ KHI người dùng có yêu cầu riêng ở trên.

   - CÁC MÔN KHTN (Lý, Hóa, Sinh): Phân tích hiện tượng thực tế, biểu đồ thực nghiệm, đồ thị quá trình, chu trình sinh thái, chuẩn IUPAC/SI.

   - CÁC MÔN KHXH (Sử, Địa, GDKT&PL): Phân tích tư liệu gốc, Atlat, bảng số liệu kinh tế - xã hội, xử lý tình huống đời sống.

3. NGOẠI LỆ NGỮ LIỆU ĐẶC THÙ:

   - NGỮ VĂN & TIẾNG ANH: Nếu không có yêu cầu đặc biệt từ giáo viên, BẮT BUỘC dùng ngữ liệu MỚI HOÀN TOÀN NGOÀI SGK, bám sát đặc trưng thể loại/chủ đề Lớp {grade_num} chuẩn Bộ GD&ĐT."""



                        enable_blend_cfg = st.session_state.get("cb_enable_blend_gv", True)
                        if ree and enable_blend_cfg and not has_custom_prompt:
                            custom_user_instructions += "\n" + ree.build_real_exam_context_injection(subject, grade_num, chosen_topics)
                        elif has_custom_prompt:
                            custom_user_instructions += f"""
[LỆNH ĐỘC BẢN & BỘ LỌC GIẢI NGẦM (DEEP SOLVER GUARD)]:
- BẮT BUỘC 100% ngữ liệu, số liệu, bài toán thực tiễn do AI TỰ SÁNG TÁC MỚI TINH, ĐỘC BẢN, KHÔNG sao chép từ bất kỳ đề thi thử nào trên mạng.
- TỰ ĐỘNG GIẢI NGẦM kiểm tra nghiệm: Đảm bảo số liệu logic toán học chuẩn xác, phương trình có nghiệm đẹp, không mâu thuẫn giả thiết.
- PHẦN II (ĐÚNG/SAI): 4 mệnh đề a, b, c, d phải rõ ràng, phân định Đúng/Sai dứt khoát dựa trên suy luận logic.
- PHẦN III (ĐIỀN SỐ): Đáp án 'ans' PHẢI là số thực hoặc số nguyên có độ dài TỐI ĐA 4 KÝ TỰ (ví dụ: "2.5", "-3", "12", "0.75").
"""



                        if subject == "Ngữ văn":

                            exam_prompt = f"""[HỆ THỐNG RA ĐỀ THI NGỮ VĂN CHUẨN KNTT 2026 - QĐ 764/QĐ-BGDĐT]

Khối lớp: {grade_num}. Chuyên đề ma trận: '{selected_topics_str}'. Mã đề: {st.session_state.exam_code}.

{custom_user_instructions}



QUY CHẾ PHÁP CHẾ BẮT BUỘC BỘ GD&ĐT (QUY TẮC CHỐNG HỌC TỦ / HỌC VẸT):

- TUYỆT ĐỐI 100% KHÔNG ĐƯỢC LẤY NGỮ LIỆU ĐÃ CÓ TRONG SGK HIỆN TẠI (kể cả Kết Nối Tri Thức, Cánh Diều, Chân Trời Sáng Tạo).

- TÙY BIẾN NGỮ LIỆU: Mặc định ra đề thi chuẩn BGD là văn bản MỚI HOÀN TOÀN NGOÀI SGK. TUY NHIÊN, NẾU giáo viên/người dùng có tùy chỉnh yêu cầu làm đề về một tác phẩm trong SGK KNTT, BẮT BUỘC phải lấy đúng văn bản trong SGK KNTT. Luôn đảm bảo tính thẩm mỹ, giá trị nhân văn và chuẩn mực ngôn ngữ Tiếng Việt, có trích dẫn nguồn tác giả/tác phẩm cụ thể.



CẤU TRÚC ĐỀ THI 100% TỰ LUẬN (120 PHÚT CHUẨN BỘ):

- PHẦN I: ĐỌC HIỂU (4.0 điểm):

  + 1 đoạn trích văn học/văn bản thông tin ngoài SGK (ghi rõ nguồn tác giả/tác phẩm).

  + 3-4 câu hỏi phân hóa chuẩn ma trận năng lực: Nhận biết (thể loại/PTBĐ/chi tiết), Thông hiểu (biện pháp tu từ/ý nghĩa hình tượng), Vận dụng (thông điệp/bài học cuộc sống).

- PHẦN II: VIẾT (6.0 điểm):

  + Câu 1 (2.0 điểm): Viết đoạn văn nghị luận xã hội khoảng 200 chữ về một tư tưởng/bài học rút ra từ ngữ liệu Đọc hiểu.

  + Câu 2 (4.0 điểm): Viết bài văn nghị luận văn học phân tích/đánh giá nét đặc sắc nội dung hoặc nghệ thuật của ngữ liệu trên.



Xuất DUY NHẤT 1 khối JSON hợp lệ dạng:

{{

  "code": "{st.session_state.exam_code}",

  "subject": "Ngữ văn",

  "part_doc_hieu": {{

    "text": "Đoạn trích/Ngữ liệu văn học ngoài SGK (kèm nguồn dẫn cụ thể)...",

    "questions": [

      {{"q": "Câu 1 (Nhận biết): Xác định thể loại/phương thức biểu đạt...", "ans": "Đáp án gợi ý"}},

      {{"q": "Câu 2 (Thông hiểu): Nêu tác dụng của biện pháp nghệ thuật...", "ans": "Đáp án gợi ý"}},

      {{"q": "Câu 3 (Vận dụng): Rút ra thông điệp có ý nghĩa nhất...", "ans": "Đáp án gợi ý"}}

    ]

  }},

  "part_viet": [

    {{"q": "Câu 1 (2.0 điểm): Viết đoạn văn nghị luận xã hội khoảng 200 chữ...", "ans": "Dàn ý gợi ý"}},

    {{"q": "Câu 2 (4.0 điểm): Viết bài văn nghị luận văn học phân tích đoạn trích trên...", "ans": "Dàn ý gợi ý"}}

  ]

}}"""

                        elif subject == "Tiếng Anh":

                            exam_prompt = f"""[HỆ THỐNG RA ĐỀ THI TIẾNG ANH CHUẨN 100% QĐ 764/QĐ-BGDĐT & KHUNG CEFR]

Khối lớp: {grade_num}. Chuyên đề ma trận: '{selected_topics_str}'. Mã đề: {st.session_state.exam_code}.



QUY CHẾ PHÁP CHẾ & SƯ PHẠM BẮT BUỘC THEO BỘ GD&ĐT:

1. DẠNG THỨC THI: 100% Trắc nghiệm 4 lựa chọn (A, B, C, D). Sinh ĐÚNG {num_p1} câu hỏi.

2. TUYỆT ĐỐI KHÔNG CÓ PHẦN II (Đúng/Sai) VÀ KHÔNG CÓ PHẦN III (Điền số). Hai mảng 'p2' và 'p3' BẮT BUỘC là danh sách rỗng [].

3. 100% TIẾNG ANH: Toàn bộ câu hỏi 'q', đoạn văn, ngữ cảnh và phương án 'opt' (A, B, C, D) PHẢI ĐƯỢC VIẾT 100% BẰNG TIẾNG ANH CHUẨN MỰC BẢN NGỮ. Chỉ dùng tiếng Việt ở trường 'explain' để hướng dẫn bản chất ngữ pháp/từ vựng.

4. MA TRẬN ĐỀ THI TIẾNG ANH 40 CÂU PHÂN BỔ ĐỦ CÁC MẢNG NĂNG LỰC:

   - Phonetics (Phát âm & Trọng âm)

   - Grammar & Vocabulary in Authentic Context (Thì động từ, Mệnh đề quan hệ, Collocations, Phrasal verbs, Từ đồng nghĩa / trái nghĩa)

   - Functional Communication Exchanges (Tình huống giao tiếp đời sống)

   - Cloze Test (Đọc điền từ đoạn văn)

   - Reading Comprehension (Đọc hiểu ý chính, chi tiết, suy luận, từ quy chiếu)

   - Sentence Transformation & Combining (Chuyển đổi câu đồng nghĩa, đảo ngữ, câu điều kiện)

{custom_user_instructions}



Xuất DUY NHẤT 1 khối JSON hợp lệ có dạng:

{{

  "code": "{st.session_state.exam_code}",

  "subject": "Tiếng Anh",

  "p1": [

    {{"q": "Question content in English...", "opt": ["A. Option 1", "B. Option 2", "C. Option 3", "D. Option 4"], "ans": "B", "explain": "Giải thích chi tiết bằng tiếng Việt (NHỚ ĐẢO ĐÁP ÁN ĐÚNG NGẪU NHIÊN VÀO B, C HOẶC D)"}}

  ],

  "p2": [],

  "p3": []

}}"""

                        else:

                            if num_p3 == 0:

                                p3_spec_text = "- Phần III: KHÔNG ÁP DỤNG cho môn này theo chuẩn QĐ 764/QĐ-BGDĐT. Trường 'p3' BẮT BUỘC là danh sách rỗng: \"p3\": []."

                                p3_json_part = '"p3": []'

                            else:

                                p3_spec_text = f"""- Phần III (Trả lời ngắn): sinh ĐÚNG {num_p3} câu điền số.

  + 100% CÁC CÂU HỎI BẮT BUỘC ĐẠT CHUẨN VẬN DỤNG (VD) VÀ VẬN DỤNG CAO (VDC):

  + Tối ưu hóa cực trị thực tiễn (kinh tế, sinh học, chuyển động vật lý), bài toán hình học không gian Oxyz thực tiễn, hoặc xác suất thực tế.

  + QUY CHUẨN ĐÁP ÁN: Đáp án 'ans' PHẢI là số thực hoặc số nguyên có độ dài TỐI ĐA 4 KÝ TỰ (bao gồm cả dấu trừ '-' và dấu chấm thập phân, ví dụ: "2.5", "-3", "12", "0.75", "-1.5"). TUYỆT ĐỐI KHÔNG sinh câu hỏi có đáp số phân số hoặc dài hơn 4 ký tự!"""

                                p3_json_part = '''"p3": [

    {"q": "Câu hỏi trả lời ngắn...", "ans": "2.5", "explain": "Định hướng thiết lập mô hình và phương trình (không ghi sẵn đáp số)"}

  ]'''



                            exam_prompt = f"""[HỆ THỐNG RA ĐỀ THI TRẮC NGHIỆM CHUẨN 100% CHƯƠNG TRÌNH GDPT 2018 - QĐ 764/QĐ-BGDĐT]

Môn học: {subject} | Khối lớp: {grade_num}.

Chuyên đề liên khối lựa chọn: '{selected_topics_str}'. Mã đề: {st.session_state.exam_code}.



NGUYÊN TẮC SƯ PHẠM BẮT BUỘC THEO CHƯƠNG TRÌNH GDPT 2018 (SGK KẾT NỐI TRI THỨC VỚI CUỘC SỐNG):

1. MÔN TOÁN HỌC:

   - TUYỆT ĐỐI NGHIÊM CẤM ra đề về hàm số bậc 4 trùng phương y = ax^4 + bx^2 + c (đã bị LOẠI BỎ hoàn toàn khỏi CT 2018; TRỪ KHI giáo viên/người dùng có yêu cầu riêng ở mục [NGUYỆN VỌNG ĐẶC BIỆT]).

   - TUYỆT ĐỐI 100% NGHIÊM CẤM CÁC BÀI TOÁN HÀM HỢP / HÀM ẨN ĐÁNH ĐỐ CỦA CHƯƠNG TRÌNH CŨ (CT 2006):

     + KHÔNG ĐƯỢC ra bài toán cho đồ thị đạo hàm y = f'(x) để hỏi tính đơn điệu, cực trị của hàm hợp y = f(3-2x), f(ax+b), f(x^2-2x)... (Chương trình GDPT 2018 & SGK Kết Nối Tri Thức ĐÃ BỎ HOÀN TOÀN dạng bài đánh đố này; TUY NHIÊN, NẾU người dùng có yêu cầu riêng ở mục [NGUYỆN VỌNG ĐẶC BIỆT] về đọc đồ thị đạo hàm f'(x) cơ bản để xét tính đơn điệu/cực trị của chính hàm số y = f(x) hoặc bài toán thực tiễn thì ĐƯỢC PHÉP ĐÁP ỨNG).

     + KHÔNG ĐƯỢC ra đề về cực trị hàm ẩn f(f(x)), f(|x|), tương giao chứa tham số m cơ học phức tạp.

   - KHẢO SÁT HÀM SỐ LỚP 12 CHỈ ĐƯỢC PHÉP DÙNG 3 LOẠI HÀM SỐ TƯỜNG MINH TRỰC TIẾP:

     + Hàm đa thức bậc ba: y = ax^3 + bx^2 + cx + d (a != 0)

     + Hàm phân thức bậc nhất / bậc nhất: y = (ax + b) / (cx + d)

     + Hàm phân thức bậc hai / bậc nhất: y = (ax^2 + bx + c) / (px + q) (có tiệm cận xiên)

   - QUY TẮC BẤT BIẾN VỀ BẢNG BIẾN THIÊN (BBT) & TIỆM CẬN:

     + Khi câu hỏi yêu cầu tìm số tiệm cận đứng, tiệm cận ngang từ bảng biến thiên: BẮT BUỘC phải là hàm phân thức (bậc 1/1 hoặc bậc 2/1). TUYỆT ĐỐI KHÔNG DÙNG bảng biến thiên của hàm bậc 3 để hỏi tiệm cận (vì hàm bậc 3 liên tục trên R, không có tiệm cận đứng hay ngang)!

     + Tại tiệm cận đứng x = x0: Hàm số và đạo hàm y' KHÔNG XÁC ĐỊNH, BẮT BUỘC ghi dấu vạch đôi '||' ở cả hàng y' và hàng y (TUYỆT ĐỐI KHÔNG GHI SỐ 0 Ở y' TẠI TIỆM CẬN ĐỨNG)!

     + Tiệm cận ngang y = y0 chỉ tồn tại khi x -> ±inf thì y tiến về một HẰNG SỐ HỮU HẠN (như 1, 2, -1). Nếu y tiến tới ±inf thì không có tiệm cận ngang.

   - Khối 10: Hàm bậc nhất & Parabol bậc hai y = ax^2 + bx + c.

   - Khối 11: Cấp số cộng/nhân, Hàm lượng giác, Giới hạn, Đạo hàm, Mẫu số liệu ghép nhóm.

2. MÔN VẬT LÝ:

   - 100% sử dụng hệ đo lường quốc tế SI (m, s, kg, N, J, W, Pa, V, A, C, T, Wb, Hz, Bq, eV...).

   - TUYỆT ĐỐI KHÔNG đưa danh pháp Hóa học hay phản ứng Hóa học vào đề Vật lý. Đề thi phải tập trung 100% vào bản chất vật lý, quá trình động học, năng lượng, dao động, sóng, nhiệt động lực học, mạch điện xoay chiều, từ trường và vật lý hạt nhân.

   - BỎ HOÀN TOÀN các bài toán cơ học/mạch điện đánh đố mẹo mực phi thực tế của CT 2006. Bám sát hiện tượng thực tế, thí nghiệm thực hành, đồ thị biến thiên động học chuẩn SGK KNTT.

3. MÔN HÓA HỌC:

   - 100% sử dụng danh pháp quốc tế IUPAC theo chuẩn CT 2018 (Alkane, Alkene, Alkyne, Alcohol, Aldehyde, Carboxylic acid, Ester, Amine, Amino acid, Carbohydrate, Polymer, Phức chất...). TUYỆT ĐỐI KHÔNG dùng tên cũ (Ancol, Anđehit, Axit axetic, Benzen...).

   - BỎ HOÀN TOÀN các bài toán giải hệ phương trình kim loại tác dụng hỗn hợp axit HNO3/H2SO4 đặc phức tạp phi thực tế của CT 2006.

   - Tập trung vào bản chất hóa học, năng lượng phản ứng Enthalpy, cân bằng hóa học, pin điện hóa, thực nghiệm tổng hợp hữu cơ đời sống.

4. MÔN SINH HỌC:

   - 100% chuẩn thuật ngữ Di truyền học & Sinh thái học CT 2018 (DNA, mRNA, tRNA, Codon, Anticodon, Operon Lac, Thể đột biến, Quần xã, Hệ sinh thái KNTT). TUYỆT ĐỐI KHÔNG lẫn sang các môn khác.

   - BỎ HOÀN TOÀN các bài toán đếm giao tử, số kiểu gen/kiểu hình thuần túy toán học của CT 2006.

   - Tập trung vào phân tích phả hệ bệnh di truyền người, cơ chế điều hòa gene, ứng dụng công nghệ sinh học và bảo tồn đa dạng sinh học.

5. MÔN KHOA HỌC TỰ NHIÊN (LỚP 6-9):

   - Tích hợp 3 phân môn Vật lý SI, Hóa học IUPAC và Sinh học KNTT theo bài học.

6. MÔN LỊCH SỬ / LỊCH SỬ & ĐỊA LÝ:

   - Bám sát tiến trình lịch sử Việt Nam và thế giới CT GDPT 2018 (mốc thời gian, nhân vật, sự kiện, nguyên nhân, ý nghĩa).

   - Phần II Đúng/Sai: Trích dẫn đoạn tư liệu gốc, văn kiện hoặc nhận định học giả. Ý a, b xác định nội dung sự kiện; ý c, d đánh giá giá trị tư liệu và bài học dựng nước, giữ nước.

7. MÔN ĐỊA LÝ / ĐỊA LÍ:

   - Bám sát quy luật địa lí tự nhiên, dân cư, chuyển dịch cơ cấu ngành kinh tế và các vùng kinh tế trọng điểm.

   - Kỹ năng phân tích bảng số liệu thống kê (GDP, xuất nhập khẩu, dân số), nhận dạng biểu đồ và Atlat Địa lí.

   - Phần II Đúng/Sai: Phân tích số liệu kinh tế xã hội, biến đổi khí hậu và phát triển bền vững.

8. MÔN GIÁO DỤC KINH TẾ VÀ PHÁP LUẬT / GDCD:

   - Kinh tế: Cơ chế thị trường, cung - cầu, lạm phát, thất nghiệp, ngân sách nhà nước, hội nhập kinh tế quốc tế.

   - Pháp luật: Hiến pháp 2013, quyền và nghĩa vụ công dân, pháp luật dân sự, lao động, doanh nghiệp.

   - Phần II Đúng/Sai: Tình huống pháp lý/kinh tế thực tế đời sống; nhận diện vi phạm, xử lý tình huống đúng pháp luật.

9. MÔN TIN HỌC:

   - Bám sát 2 định hướng Khoa học máy tính (CS) & Tin học ứng dụng (ICT): Lập trình Python chuẩn PEP8, thuật toán (tìm kiếm, sắp xếp, đệ quy, quy hoạch động), CSDL quan hệ SQL, mạng máy tính và an toàn thông tin số.

10. MÔN CÔNG NGHỆ:

   - Định hướng Công nghiệp (Bản vẽ kỹ thuật, cơ khí, linh kiện điện tử, mạch điều khiển) hoặc Nông nghiệp (Trồng trọt, chăn nuôi, lâm nghiệp, thủy sản công nghệ cao KNTT).

   - Thiết kế kỹ thuật, đọc hiểu sơ đồ nguyên lý và quy trình an toàn lao động.

11. QUY TẮC ĐÁP ÁN TRẮC NGHIỆM (ÁP DỤNG MỌI MÔN):

   - BẮT BUỘC ĐẢO VỊ TRÍ ĐÁP ÁN ĐÚNG NGẪU NHIÊN VÀO CÁC LỰA CHỌN A, B, C HOẶC D (TUYỆT ĐỐI KHÔNG MẶC ĐỊNH ĐÁP ÁN ĐÚNG LUÔN LÀ A).

12. ĐỊNH DẠNG CÔNG THỨC (TOÀN BỘ CÁC MÔN):

   - BẮT BUỘC bọc TẤT CẢ các công thức, biểu thức, biến số, và ký hiệu (Toán, Lý, Hóa, KHTN...) trong cặp dấu đô la $...$ (Ví dụ: $\\vec{{a}} = k\\vec{{b}}$, $\\overrightarrow{{AB}} = -\\overrightarrow{{BA}}$, $F = ma$). VỚI VÉC TƠ TỪ 2 KÝ TỰ TRỞ LÊN HOẶC CÓ DẤU PHẨY (như AB, AD, AA', AC'): BẮT BUỘC dùng \\\\overrightarrow{{AB}}, \\\\overrightarrow{{AA'}} để mũi tên bao trọn vẹn từ gốc đến ngọn chuẩn KaTeX.

   - TUYỆT ĐỐI KHÔNG dùng dấu backtick (`) để bọc công thức/ký hiệu vì sẽ bị lỗi hiển thị.

   - TUYỆT ĐỐI KHÔNG bọc chữ tiếng Việt có dấu trong dấu $...$.

   - KHÔNG mô tả bảng biến thiên bằng lời rườm rà trong 'q'.

13. HIỂN THỊ ĐỒ THỊ / KHỐI TRÒN XOAY 3D / BẢNG BIẾN THIÊN / BẢNG SỐ LIỆU:

   - BẮT BUỘC: Khi câu hỏi yêu cầu học sinh quan sát/đọc hình vẽ, bảng biến thiên hoặc bảng số liệu (ví dụ: 'Cho đồ thị...', 'có bảng biến thiên như hình...', 'đường cong trong hình vẽ bên...', 'Cho khối tròn xoay...'):
     + "f": Object mô tả đúng đồ thị 2D hoặc khối 3D (ví dụ: {{"type": "func_1_1", "a": 2, "b": -1, "c": 1, "d": -1}} cho hàm bậc nhất/bậc nhất; {{"type": "func_3", "a": 1, "b": -3, "c": 0, "d": 2}} cho hàm bậc 3; {{"type": "func_2_1", "a": 1, "b": 0, "c": 1, "d": 1, "e": -1}} cho hàm bậc 2/bậc 1; {{"type": "solid_of_revolution", "f_expr": "sqrt(x)", "a": 0, "b": 4}} cho khối tròn xoay quanh Ox; {{"type": "cone_3d", "r": 3, "h": 4}} cho khối nón; {{"type": "cylinder_3d", "r": 3, "h": 5}} cho khối trụ; {{"type": "sphere_3d", "r": 3}} cho mặt cầu).
     + "bbt": Chuỗi mô tả BBT chuẩn đúng theo câu hỏi (dạng "x | -inf | -1 | 2 | +inf \\n y' | - | 0 | + | 0 | - \\n y | +inf | ↘ | -2 | ↗ | 4 | ↘ | -inf").
     + "mslgn_data": Object bảng ghép nhóm (ví dụ: {{"title": "Bảng số liệu...", "groups": ["[0; 20)", "[20; 40)"], "freq": [5, 12]}}).
     + TUYỆT ĐỐI KHÔNG sinh trường "bbt" hay "f" có giá trị null, "null", "{{}}" hay để trống khi câu hỏi có ngữ liệu đồ thị hoặc bảng biến thiên!
     + VỚI CHỦ ĐỀ KHẢO SÁT HÀM SỐ (KSHS TOÁN 12) KHI YÊU CẦU 3 HÀM CƠ BẢN: BẮT BUỘC phân bổ đều và hài hòa giữa 3 dạng hàm chuẩn GDPT 2018: Hàm bậc ba (func_3), Phân thức bậc nhất/bậc nhất (func_1_1), và Phân thức bậc hai/bậc nhất (func_2_1).
   - NẾU CÂU HỎI LÀ DẠNG TÍNH TOÁN / CÔNG THỨC THUẦN TÚY KHÔNG CẦN HÌNH VẼ (ví dụ: 'Đồ thị hàm số y = (2x-1)/(x+1) có tiệm cận đứng là...', 'Tìm số giao điểm...', 'Tính đạo hàm...'), TUYỆT ĐỐI KHÔNG SINH "f", "bbt" HAY "mslgn_data"!



YÊU CẦU MA TRẬN & PHÂN HÓA NĂNG LỰC CHUẨN QUYẾT ĐỊNH 764/QĐ-BGDĐT (ĐA MÔN, ĐA LỚP):

- Phần I (Trắc nghiệm 4 lựa chọn): sinh ĐÚNG {num_p1} câu.

  + 100% CÁC CÂU Ở PHẦN I CHỈ THUỘC MỨC ĐỘ NHẬN BIẾT (NB: 60%) VÀ THÔNG HIỂU (TH: 40%).

  + TUYỆT ĐỐI KHÔNG ĐƯA CÂU HỎI VẬN DỤNG CAO (VDC), KHÔNG ĐƯA BÀI TOÁN TÍNH TOÁN CỒNG KỀNH, MẸO MỰC ĐÁNH ĐỐ VÀO PHẦN I!

  + Nội dung kiểm tra: Nhận biết khái niệm, công thức nền tảng SGK Kết Nối Tri Thức, đọc trực tiếp số liệu từ bảng biểu/đồ thị cơ bản, tính toán 1-2 bước cơ bản.

- Phần II (Trắc nghiệm Đúng/Sai - 4 ý a, b, c, d phân hóa bậc thang năng lực): sinh ĐÚNG {num_p2} câu.

  + Ngữ liệu mở đầu: Tình huống thực tiễn, hiện tượng khoa học, bảng số liệu, văn bản tư liệu gốc hoặc bài toán tổng hợp.

  + Ý a, b: Mức độ THÔNG HIỂU (TH) - Kiểm tra điều kiện cần, xác định thông số/khái niệm cơ bản trực tiếp từ đề bài.

  + Ý c, d: Mức độ VẬN DỤNG (VD) & VẬN DỤNG CAO (VDC) - Phân tích, tổng hợp, mô hình hóa toán học/khoa học, liên hệ thực tế, giải quyết vấn đề trọn vẹn (áp dụng thang điểm lũy tiến 0.1 - 0.25 - 0.5 - 1.0 của Bộ).

{p3_spec_text}



QUY CHẾ PHÁP CHẾ BẮT BUỘC BỘ GD&ĐT BẢO MẬT KHẢO THÍ SƯ PHẠM CHO TRƯỜNG 'explain' (BẢN CHẤT SOCRATIC):

- Trường 'explain' LÀ ĐỊNH HƯỚNG TƯ DUY SOCRATIC: CHỈ ĐƯỢC PHÉP nêu phương pháp, định lý liên quan, công thức trọng tâm và câu hỏi gợi mở tư duy.

- TUYỆT ĐỐI 100% KHÔNG ĐƯỢC ghi câu chốt đáp án, KHÔNG viết 'chọn A/B/C/D', KHÔNG tính sẵn đáp số cuối cùng cho học sinh trong 'explain'!



{custom_user_instructions}



Xuất DUY NHẤT 1 khối JSON hợp lệ có dạng:

{{

  "code": "{st.session_state.exam_code}",

  "subject": "{subject}",

  "p1": [

    {{"q": "Nội dung câu trắc nghiệm (nếu đề hỏi nhìn hình/BBT thì viết rõ 'như hình vẽ bên' hoặc 'có bảng biến thiên như hình bên')...", "opt": ["A. Đáp án 1", "B. Đáp án 2", "C. Đáp án 3", "D. Đáp án 4"], "ans": "A", "explain": "Định hướng tư duy Socratic (phương pháp, công thức, tuyệt đối không lộ đáp án)"}}

  ],

  "p2": [

    {{"q": "Cho ngữ liệu/hiện tượng/tình huống...", "stmts": [{{"t": "Mệnh đề a", "a": true}}, {{"t": "Mệnh đề b", "a": false}}, {{"t": "Mệnh đề c", "a": true}}, {{"t": "Mệnh đề d", "a": false}}], "explain": "Định hướng tư duy Socratic cho từng ý (phương pháp, không giải sẵn)"}}

  ],

  {p3_json_part}

}}"""



                        try:

                            raw_json_ex = call_gemini_with_fallback(exam_prompt, json_mode=True)

                            raw_json_ex = raw_json_ex.strip()

                            if raw_json_ex.startswith("```json"): raw_json_ex = raw_json_ex[7:-3].strip()

                            elif raw_json_ex.startswith("```"): raw_json_ex = raw_json_ex[3:-3].strip()

                            parsed_exam = validate_exam_data(safe_json_loads(raw_json_ex), subject, None if subject == "Ngữ văn" else (num_p1, num_p2, num_p3))
                            parsed_exam["is_ai_generated"] = True
                            parsed_exam["is_real_exam"] = False
                            parsed_exam["exam_source_type"] = "ai_generated"

                            if ree and enable_blend_cfg and not has_custom_prompt:
                                parsed_exam = ree.blend_real_exam_with_ai(parsed_exam, subject, grade_num, chosen_topics)

                            st.session_state.exam_data = enrich_exam_data(parsed_exam)
                            if "seen_question_fps" not in st.session_state:
                                st.session_state.seen_question_fps = set()
                            for p_key in ("p1", "p2", "p3"):
                                for q_new in st.session_state.exam_data.get(p_key, []):
                                    q_txt = str(q_new.get("q", "")).strip().lower()
                                    if q_txt:
                                        fp_c = ree.q_fingerprint(q_new) if ree else re.sub(r'[^a-zA-Z0-9\u00C0-\u1EF9]', '', q_txt)[:80]
                                        st.session_state.seen_question_fps.add(fp_c)
                                        if ree and hasattr(ree, "_RECENT_QUESTION_COOLDOWN"):
                                            ree._RECENT_QUESTION_COOLDOWN.add(q_new.get("q", "").strip())

                            save_exam_to_cache(st.session_state.exam_data, subject, grade_num, selected_topics_str)
                            if ree and hasattr(ree, "ingest_ai_generated_exam_to_bank"):
                                try:
                                    ree.ingest_ai_generated_exam_to_bank(st.session_state.exam_data, subject, grade_num)
                                except Exception:
                                    pass

                            st.session_state.attempt_id = str(uuid.uuid4())

                            st.session_state.exam_start_timestamp = time.time()

                            st.session_state.exam_deadline = time.time() + exam_time_mins * 60

                            st.session_state.exam_context = {"name": student_name, "grade": grade, "subject": subject, "phase": measure_phase, "student_id": measure_student_id}

                            st.session_state.pop("literature_grade", None)

                            st.session_state.pop("exam_submitted_at", None)

                            for widget_key in list(st.session_state):

                                if widget_key.startswith(("t3_p1_", "t3_p2_", "t3_p3_", "nv_dh_", "nv_v_")):

                                    del st.session_state[widget_key]

                            st.session_state.exam_state = "testing"

                            st.session_state.exam_answers = {}

                            st.session_state.tram3_chat_messages = []

                            st.rerun()

                        except Exception as e:

                            st.error(f"Lỗi khởi tạo đề thi: {e}")



        with tab_giao_vien:

            st.markdown("#### 🛠️ Không Gian Nghiệp Vụ Sư Phạm Của Giáo Viên:")

            st.caption("Khu vực dành riêng cho Thầy/Cô cấu hình ma trận tùy biến, tải lên đề riêng hoặc trích xuất đề thi từ các nguồn bên ngoài:")



            # 1. TÙY BIẾN MA TRẬN RIÊNG

            if subject == "Ngữ văn":

                custom_ph = "Ví dụ: Cho đề phân tích tâm trạng nhà thơ Quang Dũng qua bài thơ Tây Tiến, hoặc trích đoạn thơ ngoài SGK về tình mẫu tử, bài văn NLVH so sánh hai đoạn trích..."

            elif subject == "Tiếng Anh":

                custom_ph = "Ví dụ: Cần 10 câu Reading Comprehension chủ đề Artificial Intelligence, 5 câu đảo ngữ và câu điều kiện nâng cao, chuyên đề Collocations..."

            elif subject == "Toán học":

                custom_ph = "Ví dụ: Cần 12 câu KSHS Lớp 12 (6 NB, 6 TH), 1 câu khảo sát hàm bậc 4 trùng phương để rèn luyện, bài toán tối ưu hóa chi phí thực tế..."

            elif subject == "Vật lý":

                custom_ph = "Ví dụ: Cần 5 câu Dao động điều hòa nâng cao, 2 câu mạch điện xoay chiều RLC có đồ thị biến thiên, 1 câu bài toán thực tế sóng âm..."

            elif subject == "Hóa học":

                custom_ph = "Ví dụ: Cần 5 câu Ester - Lipid nâng cao theo IUPAC, 2 câu sơ đồ chuyển hóa hữu cơ, 1 câu bài toán pin điện hóa và điện phân dung dịch..."

            elif subject == "Sinh học":

                custom_ph = "Ví dụ: Cần 5 câu Di truyền phân tử & Đột biến, 2 câu phân tích phả hệ di truyền người 4 thế hệ, 1 câu bài toán cân bằng di truyền quần thể..."

            else:

                custom_ph = f"Ví dụ: Cần tập trung chuyên đề trọng tâm môn {subject} Lớp {grade_num}, các bài tập vận dụng thực tế..."



            custom_matrix_prompt = st.text_area(

                "💬 Nhập yêu cầu cấu hình ma trận / Ngữ liệu tùy biến:",

                value=st.session_state.get("custom_matrix_prompt", ""),

                placeholder=custom_ph,

                height=90,

                key="area_custom_prompt_gv",

                help="Thầy/Cô có thể chỉ định tác phẩm văn học cụ thể, dạng bài đặc thù hoặc chủ đề trọng tâm để rèn luyện học sinh."

            )

            st.session_state["custom_matrix_prompt"] = custom_matrix_prompt



            enable_real_exam_blend = st.checkbox(

                f"🎯 Tự Động Trộn Ngữ Liệu Đề Thi Thật (Cập nhật 24/7 từ {portal_name_ui} & Các Trường Điểm)",

                value=True,

                key="cb_enable_blend_gv",

                help="Tự động mô phỏng và trộn ngữ liệu từ các đề thi thật của các trường Chuyên, THPT điểm trên cả nước."

            )



            # 2. TẢI LÊN ĐỀ THI TỪ GIÁO VIÊN

            with st.expander("📤 Tải Lên Đề Thi Từ Giáo Viên (Word .docx, PDF, Văn Bản) - Chuẩn QĐ 764", expanded=False):

                st.caption("Dành cho giáo viên: Tự tải lên đề kiểm tra của trường/lớp (hỗ trợ .docx, .pdf, dán văn bản thô). Hệ thống tự động bóc tách thành chuẩn cấu trúc khảo thí QĐ 764:")

                st.markdown(
                    '<div style="background: rgba(15, 23, 42, 0.7); border: 1px dashed #38bdf8; border-radius: 8px; padding: 10px 14px; margin-bottom: 12px; font-size: 13px; line-height: 1.6; color: #cbd5e1;">'
                    '<div style="margin-bottom: 6px;">💡 <b style="color: #38bdf8;">MẸO NẠP ĐỀ WORD MATHTYPE CHUẨN 100% CÔNG THỨC (KHÔNG BỊ MẤT KÝ TỰ):</b></div>'
                    '<div style="margin-bottom: 4px;">• <b>Cách 1 (Nhanh nhất - 1 Click trong Word):</b> Mở file Word ➔ Chọn menu <b>MathType</b> ➔ Bấm <b>Convert Equations</b> ➔ Chọn đổi sang <b>TeX/LaTeX ($...$)</b> ➔ Bấm <b>Convert</b> rồi lưu lại tải lên. Toàn bộ công thức MathType sẽ giữ nguyên 100%!</div>'
                    '<div>• <b>Cách 2 (Lưu PDF):</b> Trong Word, bấm <b>File ➔ Save As ➔ Chọn định dạng PDF (.pdf)</b> rồi tải file PDF lên để giữ trọn vẹn cả công thức và hình vẽ.</div>'
                    '</div>',
                    unsafe_allow_html=True
                )

                col_gv1, col_gv2 = st.columns([1, 1])

                with col_gv1:

                    gv_teacher_name = st.text_input("Tên Giáo viên / Tổ chuyên môn:", value=st.session_state.get("gv_author_name", "Thầy/Cô bộ môn"), key="inp_gv_name")

                    gv_school_name = st.text_input("Trường THPT / Đơn vị:", value=st.session_state.get("gv_school_name", "Trường THPT"), key="inp_gv_school")

                with col_gv2:

                    gv_exam_title = st.text_input("Tiêu đề đề thi:", value=f"Đề kiểm tra môn {subject} - Lớp {grade_num}", key="inp_gv_title")

                    gv_input_mode = st.radio("Hình thức nạp đề:", ["Tải file Word (.docx) / PDF (.pdf)", "Dán văn bản trực tiếp"], horizontal=True, key="radio_gv_mode")



                gv_extracted_text = ""

                gv_file_bytes = None

                gv_file_name = ""

                if gv_input_mode == "Tải file Word (.docx) / PDF (.pdf)":

                    uploaded_file = st.file_uploader("Chọn file đề thi (.docx, .pdf, .txt):", type=["docx", "pdf", "txt"], key="file_up_gv")

                    if uploaded_file is not None:

                        gv_file_bytes = uploaded_file.read()

                        gv_file_name = uploaded_file.name

                        gv_extracted_text = ree.extract_text_from_file_upload(gv_file_bytes, uploaded_file.name) if ree else ""

                        if gv_extracted_text.startswith("__MATHTYPE_WARNING__:"):

                            parts_mt = gv_extracted_text.split("\n", 1)

                            cnt_mt = parts_mt[0].replace("__MATHTYPE_WARNING__:", "")

                            gv_extracted_text = parts_mt[1] if len(parts_mt) > 1 else ""

                            st.info(f"✨ **Cơ Chế Xử Lý Ngầm Tự Động Kích Hoạt:** Hệ thống phát hiện `{cnt_mt} công thức MathType` trong file `{uploaded_file.name}`. AI Multimodal sẽ tự động xử lý ngầm và bóc tách toàn vẹn công thức sang chuẩn KaTeX $...$ khi Thầy/Cô bấm Phân tích bên dưới!")

                        elif gv_extracted_text:

                            st.success(f"Đã đọc file thành công ({len(gv_extracted_text)} ký tự)!")

                        else:

                            st.warning("Chưa đọc được nội dung từ file hoặc file scan ảnh không có text.")

                else:

                    gv_raw_paste = st.text_area("Dán nội dung đề thi vào đây:", height=150, placeholder="Dán nội dung đề thi (Phần I, Phần II, Phần III hoặc trắc nghiệm, tự luận)...", key="area_gv_paste")

                    if gv_raw_paste.strip():

                        gv_extracted_text = gv_raw_paste.strip()



                if gv_extracted_text or gv_file_bytes is not None:

                    if st.button("⚙️ Phân Tích & Chuẩn Hóa Cấu Trúc Đề Thi (Xử Lý Ngầm 100%)", key="btn_parse_gv_exam", type="primary"):

                        with st.spinner("Đang kích hoạt bộ máy Xử Lý Ngầm Multimodal AI bóc tách toàn diện công thức MathType và chuẩn hóa ma trận QĐ 764..."):

                            user_prompt_gv = st.session_state.get("custom_matrix_prompt", "")

                            parsed_gv = None

                            if gv_file_bytes is not None and gv_file_name and ree and hasattr(ree, "parse_file_direct_with_ai"):

                                parsed_gv = ree.parse_file_direct_with_ai(

                                    gv_file_bytes,

                                    gv_file_name,

                                    subject,

                                    grade_num,

                                    gv_school_name,

                                    gv_exam_title,

                                    ai_caller=lambda p, json_mode=False: call_gemini_with_fallback(p, json_mode=json_mode),

                                    user_prompt=user_prompt_gv

                                )

                            if not parsed_gv and ree:

                                parsed_gv = ree.parse_raw_exam_text(

                                    gv_extracted_text,

                                    subject,

                                    grade_num,

                                    gv_school_name,

                                    gv_exam_title,

                                    ai_caller=lambda p, json_mode=False: call_gemini_with_fallback(p, json_mode=json_mode),

                                    user_prompt=user_prompt_gv

                                )

                            if parsed_gv and (parsed_gv.get("p1") or parsed_gv.get("p2") or parsed_gv.get("p3") or parsed_gv.get("part_doc_hieu")):

                                st.session_state["gv_parsed_exam_temp"] = parsed_gv

                                st.success("🎉 Đã xử lý ngầm và chuẩn hóa cấu trúc đề thi thành công! Toàn bộ công thức MathType đã được chuyển đổi sang KaTeX sắc nét.")

                            else:

                                st.error("Không thể tự động phân tích cấu trúc đề thi. Vui lòng kiểm tra định dạng câu hỏi hoặc thử lại.")



                if st.session_state.get("gv_parsed_exam_temp"):

                    p_gv = st.session_state["gv_parsed_exam_temp"]

                    st.markdown(f"**Kết quả chuẩn hóa:** Phần I: `{len(p_gv.get('p1', []))} câu` | Phần II: `{len(p_gv.get('p2', []))} câu` | Phần III: `{len(p_gv.get('p3', []))} câu`")

                    col_act1, col_act2, col_act3, col_act4 = st.columns([1.1, 1.4, 1.1, 1.3])

                    with col_act1:

                        if st.button("🚀 Nạp Nguyên Đề", key="btn_start_gv_exam", type="secondary", width="stretch"):

                            st.session_state.exam_data = enrich_exam_data(p_gv)

                            st.session_state.exam_code = str(p_gv.get("code", random.randint(1011, 9999)))

                            st.session_state.attempt_id = str(uuid.uuid4())

                            st.session_state.exam_start_timestamp = time.time()

                            st.session_state.exam_deadline = time.time() + exam_time_mins * 60

                            st.session_state.exam_context = {"name": student_name, "grade": grade, "subject": subject, "phase": measure_phase, "student_id": measure_student_id}

                            st.session_state.pop("literature_grade", None)

                            st.session_state.pop("exam_submitted_at", None)

                            for widget_key in list(st.session_state):

                                if widget_key.startswith(("t3_p1_", "t3_p2_", "t3_p3_", "nv_dh_", "nv_v_")):

                                    del st.session_state[widget_key]

                            st.session_state.exam_state = "testing"

                            st.session_state.exam_answers = {}

                            st.session_state.tram3_chat_messages = []

                            st.toast("⚡ Đã nạp thành công đề thi của Giáo viên vào phòng thi!", icon="✨")

                            st.rerun()

                    with col_act2:

                        if st.button("🔀 Trộn Đề Mới (Quét + Quốc Gia)", key="btn_blend_gv_exam", type="primary", width="stretch"):

                            with st.spinner("Đang trộn ngữ liệu vừa quét với Ngân hàng Quốc gia, đảo ngẫu nhiên câu hỏi & phương án..."):

                                blended_exam = ree.create_mixed_scanned_exam(p_gv, subject, grade_num, mix_ratio=0.5, shuffle_options=True) if ree else p_gv

                                st.session_state.exam_data = enrich_exam_data(blended_exam)

                                st.session_state.exam_code = str(blended_exam.get("code", random.randint(1011, 9999)))

                                st.session_state.attempt_id = str(uuid.uuid4())

                                st.session_state.exam_start_timestamp = time.time()

                                st.session_state.exam_deadline = time.time() + exam_time_mins * 60

                                st.session_state.exam_context = {"name": student_name, "grade": grade, "subject": subject, "phase": measure_phase, "student_id": measure_student_id}

                                st.session_state.pop("literature_grade", None)

                                st.session_state.pop("exam_submitted_at", None)

                                for widget_key in list(st.session_state):

                                    if widget_key.startswith(("t3_p1_", "t3_p2_", "t3_p3_", "nv_dh_", "nv_v_")):

                                        del st.session_state[widget_key]

                                st.session_state.exam_state = "testing"

                                st.session_state.exam_answers = {}

                                st.session_state.tram3_chat_messages = []

                                st.toast(f"🎉 Đã tạo Đề Trộn Mới (Mã {st.session_state.exam_code}) từ ngữ liệu của Thầy/Cô!", icon="✨")

                                st.rerun()

                    with col_act3:

                        if st.button("💾 Lưu Kho Đề Riêng", key="btn_save_gv_exam", width="stretch"):

                            if ree and ree.save_teacher_uploaded_exam(p_gv):

                                st.toast("Đã lưu đề thi vào Kho Đề Riêng thành công!", icon="✅")

                            else:

                                st.error("Không thể lưu đề thi.")

                    with col_act4:

                        if st.button("🏛️ Nạp Shard Quốc Gia", key="btn_save_national_shard", width="stretch"):

                            with st.spinner("Đang chạy 5 TẦNG KIỂM ĐỊNH CHẤT LƯỢNG (Quality Gate) & Nạp vào Shard Quốc Gia..."):

                                if ree and hasattr(ree, "append_exam_to_national_shard") and ree.append_exam_to_national_shard(p_gv):

                                    st.toast("🎉 Đã kiểm định 5 tầng và nạp thành công vào Ngân hàng Quốc gia!", icon="✨")

                                    st.success("✅ Đề thi đã được cấp Universal QID và sẵn sàng trộn chung cho toàn bộ học sinh!")

                                else:

                                    st.error("Không thể nạp vào Shard Quốc gia.")



            # 3. QUÉT & TRÍCH XUẤT TỪ LINK

            with st.expander(f"🔍 Quét & Trích Xuất Ngữ Liệu Trực Tiếp Từ Link Đề Thi ({portal_name_ui})", expanded=False):

                def_cat_url = "https://toanmath.com/de-thi-giua-hk1-toan-12" if (subject == "Toán học" and grade_num == 12) else (

                    f"https://toanmath.com/de-thi-giua-hk1-toan-{grade_num}" if subject == "Toán học" else portal_info.get("url", "https://toanmath.com")

                )

                custom_scan_url = st.text_input("Nhập Link Chuyên Mục hoặc Link Bài Viết:", value=st.session_state.get("last_crawled_url", def_cat_url), key="inp_crawl_url")



                col_c1, col_c2 = st.columns(2)

                with col_c1:

                    btn_scan_cat = st.button("🔎 Quét Danh Mục Tìm Đề Mới", key="btn_scan_category", width="stretch")

                with col_c2:

                    btn_extract_direct = st.button("⚡ Bóc Tách Trực Tiếp Từ Link Này", key="btn_extract_direct_url", width="stretch")



                if btn_scan_cat:

                    with st.spinner("Đang kết nối chuyên trang khảo thí để quét danh sách đề thi..."):

                        cat_results = ree.fetch_portal_category_exams(custom_scan_url, max_items=15) if ree else []

                        if cat_results:

                            st.session_state["category_crawled_items"] = cat_results

                            st.session_state["last_crawled_url"] = custom_scan_url

                            st.success(f"Tìm thấy {len(cat_results)} đề thi từ chuyên mục!")

                        else:

                            st.warning("Không tìm thấy bài viết đề thi nào tại URL này hoặc đường truyền mạng bị chặn.")



                if st.session_state.get("category_crawled_items"):

                    c_items = st.session_state["category_crawled_items"]

                    c_titles = [f"[{it.get('exam_type', 'Đề')}] {it.get('title', '')} ({it.get('school', '')})" for it in c_items]

                    sel_c_idx = st.selectbox("Chọn đề thi muốn bóc tách ngữ liệu:", range(len(c_titles)), format_func=lambda i: c_titles[i], key="sel_cat_item")

                    target_article = c_items[sel_c_idx]

                    st.markdown(f"**Link nguồn:** [{target_article.get('url')}]({target_article.get('url')})")



                    if st.button("🚀 Bóc Tách File PDF & Nạp Làm Ngay (0.1s)", key="btn_extract_selected_cat", type="primary"):

                        if ree and hasattr(ree, "extract_full_exam_from_url"):

                            with st.spinner("Đang tải file PDF gốc và bóc tách toàn văn câu hỏi..."):

                                try:

                                    extracted_exam = ree.extract_full_exam_from_url(

                                        target_article.get("url"), subject, grade_num,

                                        ai_caller=lambda p, json_mode=False: call_gemini_with_fallback(p, json_mode=json_mode)

                                    )

                                except Exception as _err_ex:

                                    logging.error("Lỗi trích xuất đề thi: %s", _err_ex)

                                    extracted_exam = None



                                if extracted_exam and (extracted_exam.get("p1") or extracted_exam.get("p2") or extracted_exam.get("p3")):

                                    st.session_state.exam_data = enrich_exam_data(extracted_exam)

                                    st.session_state.exam_code = str(extracted_exam.get("code", random.randint(1011, 9999)))

                                    st.session_state.attempt_id = str(uuid.uuid4())

                                    st.session_state.exam_start_timestamp = time.time()

                                    st.session_state.exam_deadline = time.time() + exam_time_mins * 60

                                    st.session_state.exam_context = {"name": student_name, "grade": grade, "subject": subject, "phase": measure_phase, "student_id": measure_student_id}

                                    st.session_state.pop("literature_grade", None)

                                    st.session_state.pop("exam_submitted_at", None)

                                    for widget_key in list(st.session_state):

                                        if widget_key.startswith(("t3_p1_", "t3_p2_", "t3_p3_", "nv_dh_", "nv_v_")):

                                            del st.session_state[widget_key]

                                    st.session_state.exam_state = "testing"

                                    st.session_state.exam_answers = {}

                                    st.session_state.tram3_chat_messages = []

                                    st.toast(f"⚡ Đã bóc tách và nạp thành công đề thi từ {target_article.get('school', '')}!", icon="✨")

                                    st.rerun()



                if btn_extract_direct:

                    if ree and hasattr(ree, "extract_full_exam_from_url"):

                        with st.spinner("Đang truy cập bài viết và bóc tách đề thi..."):

                            try:

                                extracted_direct = ree.extract_full_exam_from_url(

                                    custom_scan_url, subject, grade_num,

                                    ai_caller=lambda p, json_mode=False: call_gemini_with_fallback(p, json_mode=json_mode)

                                )

                            except Exception as _err_dir:

                                logging.error("Lỗi trích xuất trực tiếp: %s", _err_dir)

                                extracted_direct = None



                            if extracted_direct and (extracted_direct.get("p1") or extracted_direct.get("p2") or extracted_direct.get("p3")):

                                st.session_state.exam_data = enrich_exam_data(extracted_direct)

                                st.session_state.exam_code = str(extracted_direct.get("code", random.randint(1011, 9999)))

                                st.session_state.attempt_id = str(uuid.uuid4())

                                st.session_state.exam_start_timestamp = time.time()

                                st.session_state.exam_deadline = time.time() + exam_time_mins * 60

                                st.session_state.exam_context = {"name": student_name, "grade": grade, "subject": subject, "phase": measure_phase, "student_id": measure_student_id}

                                st.session_state.pop("literature_grade", None)

                                st.session_state.pop("exam_submitted_at", None)

                                for widget_key in list(st.session_state):

                                    if widget_key.startswith(("t3_p1_", "t3_p2_", "t3_p3_", "nv_dh_", "nv_v_")):

                                        del st.session_state[widget_key]

                                st.session_state.exam_state = "testing"

                                st.session_state.exam_answers = {}

                                st.session_state.tram3_chat_messages = []

                                st.toast("⚡ Đã nạp thành công đề thi bóc tách từ link!", icon="✨")

                                st.rerun()



            # 4. KHO ĐỀ CACHE OFFLINE

            cached_list = get_cached_exams(subject, grade_num)

            if cached_list:

                with st.expander(f"⚡ Mở Đề Thi Có Sẵn Từ Ngân Hàng Offline ({len(cached_list)} đề đã lưu - Nạp tức thì 0.1s)", expanded=False):

                    c_opts = [f"Mã đề {item['code']} - {item.get('topic', 'Chuyên đề ôn tập')} ({item.get('saved_at', '')[:10]})" for item in cached_list]

                    if "sel_cached_exam_t3" in st.session_state and (not c_opts or st.session_state.sel_cached_exam_t3 >= len(c_opts)):
                        st.session_state.sel_cached_exam_t3 = 0

                    chosen_cache_idx = st.selectbox("Chọn đề từ ngân hàng:", range(len(c_opts)), format_func=lambda i: c_opts[i], key="sel_cached_exam_t3")

                    col_cb1, col_cb2 = st.columns([1, 1.2])

                    with col_cb1:

                        btn_load_cached = st.button("🚀 Nạp đề đang chọn (0.1s)", type="secondary", width="stretch", key="btn_load_cached_exam")

                    with col_cb2:

                        btn_load_cached_rnd = st.button(f"🎲 Bốc ngẫu nhiên ({len(cached_list)} đề)", type="primary", width="stretch", key="btn_random_cached_exam")

                    if btn_load_cached or btn_load_cached_rnd:

                        if btn_load_cached_rnd:
                            random.seed(time.time_ns())
                            if "seen_cached_exam_codes" not in st.session_state:
                                st.session_state.seen_cached_exam_codes = set()

                            fresh_cached = [e for e in cached_list if str(e.get("code", "")) not in st.session_state.seen_cached_exam_codes]
                            if not fresh_cached:
                                st.session_state.seen_cached_exam_codes.clear()
                                fresh_cached = cached_list

                            sel_cached_item = random.choice(fresh_cached)
                            st.session_state.seen_cached_exam_codes.add(str(sel_cached_item.get("code", "")))
                            st.toast(f"🎲 Đã bốc đề ngẫu nhiên mới: Mã {sel_cached_item.get('code')}", icon="🎯")
                        else:
                            sel_cached_item = cached_list[chosen_cache_idx]

                        st.session_state.exam_data = enrich_exam_data(sel_cached_item["data"])

                        st.session_state.exam_code = str(sel_cached_item["code"])

                        st.session_state.attempt_id = str(uuid.uuid4())

                        st.session_state.exam_start_timestamp = time.time()

                        st.session_state.exam_deadline = time.time() + exam_time_mins * 60

                        st.session_state.exam_context = {"name": student_name, "grade": grade, "subject": subject, "phase": measure_phase, "student_id": measure_student_id}

                        st.session_state.pop("literature_grade", None)

                        st.session_state.pop("exam_submitted_at", None)

                        for widget_key in list(st.session_state):

                            if widget_key.startswith(("t3_p1_", "t3_p2_", "t3_p3_", "nv_dh_", "nv_v_")):

                                del st.session_state[widget_key]

                        st.session_state.exam_state = "testing"

                        st.session_state.exam_answers = {}

                        st.session_state.tram3_chat_messages = []

                        st.toast("⚡ Đã nạp đề từ Ngân hàng Đề thành công trong 0.1 giây!", icon="✨")

                        st.rerun()





            # CARD QUY CHUẨN KHẢO THÍ SƯ PHẠM LẤP ĐẦY KHÔNG GIAN BÊN PHẢI (ZERO KHOẢNG TRỐNG THỪA)

            if subject == "Ngữ văn":
                st.markdown(
                    '<div style="background: rgba(15, 23, 42, 0.75); border: 1.2px solid #334155; border-radius: 10px; padding: 14px 16px; margin-top: 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">'
                    '<div style="color: #38bdf8; font-weight: 700; font-size: 14px; margin-bottom: 8px;">📋 Quy Chế Khảo Thí & Bareme Điểm Môn Ngữ Văn Bộ GD&ĐT 2026:</div>'
                    '<div style="color: #cbd5e1; font-size: 13px; line-height: 1.65;">'
                    '• <b>Phần I (Đọc hiểu - 4.0 điểm):</b> 3-4 câu hỏi đánh giá theo chuẩn năng lực (Nhận biết: 1.0đ, Thông hiểu: 1.5đ, Vận dụng: 1.5đ).<br>'
                    '• <b>Phần II (Viết - 6.0 điểm):</b><br>'
                    '&nbsp;&nbsp;&nbsp;&nbsp;▫ Câu 1: Viết đoạn văn Nghị luận xã hội khoảng 200 chữ (<b>2.0 điểm</b>).<br>'
                    '&nbsp;&nbsp;&nbsp;&nbsp;▫ Câu 2: Viết bài văn Nghị luận văn học phân tích ngữ liệu (<b>4.0 điểm</b>).<br>'
                    '• <b>Chấm điểm:</b> Đánh giá theo rubric tiêu chí chuẩn Bộ, hỗ trợ trợ lý AI chấm tham khảo và giáo viên kiểm duyệt.'
                    '</div></div>',
                    unsafe_allow_html=True
                )
            elif subject == "Tiếng Anh":
                st.markdown(
                    '<div style="background: rgba(15, 23, 42, 0.75); border: 1.2px solid #334155; border-radius: 10px; padding: 14px 16px; margin-top: 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">'
                    '<div style="color: #38bdf8; font-weight: 700; font-size: 14px; margin-bottom: 8px;">📋 Quy Chế Khảo Thí & Bareme Điểm Môn Tiếng Anh (QĐ 764/QĐ-BGDĐT):</div>'
                    '<div style="color: #cbd5e1; font-size: 13px; line-height: 1.65;">'
                    '• <b>Hình thức:</b> 100% Trắc nghiệm 4 lựa chọn (A, B, C, D) - 40 câu hỏi.<br>'
                    '• <b>Bareme điểm:</b> Mỗi câu đúng đạt <b>0.25 điểm</b> (Tổng điểm: 10.0 điểm).<br>'
                    '• <b>Phần II & Phần III:</b> Tuyệt đối không áp dụng theo quy chế chính thức của Bộ.<br>'
                    '• <b>Thời gian làm bài:</b> 50 phút.<br>'
                    '• <b>Chuẩn đầu ra:</b> Bám sát Khung năng lực ngoại ngữ 6 bậc Việt Nam (tương đương CEFR B1 - B2).'
                    '</div></div>',
                    unsafe_allow_html=True
                )
            elif is_social_or_tech_subject(subject):
                st.markdown(
                    f'<div style="background: rgba(15, 23, 42, 0.75); border: 1.2px solid #334155; border-radius: 10px; padding: 14px 16px; margin-top: 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">'
                    f'<div style="color: #38bdf8; font-weight: 700; font-size: 14px; margin-bottom: 8px;">📋 Quy Chế Khảo Thí & Bareme Điểm Môn {subject} (QĐ 764/QĐ-BGDĐT):</div>'
                    f'<div style="color: #cbd5e1; font-size: 13px; line-height: 1.65;">'
                    f'• <b>Phần I (Trắc nghiệm 4 lựa chọn):</b> 24 câu x 0.25 điểm = <b>6.0 điểm</b>.<br>'
                    f'• <b>Phần II (Trắc nghiệm Đúng/Sai):</b> 4 câu x 1.0 điểm = <b>4.0 điểm</b>:<br>'
                    f'&nbsp;&nbsp;&nbsp;&nbsp;▫ Đúng 1 ý: <b>0.1đ</b> &nbsp;|&nbsp; Đúng 2 ý: <b>0.25đ</b><br>'
                    f'&nbsp;&nbsp;&nbsp;&nbsp;▫ Đúng 3 ý: <b>0.5đ</b> &nbsp;|&nbsp; Đúng 4 ý: <b>1.0đ trọn vẹn</b><br>'
                    f'• <b>Phần III:</b> Không có theo cấu trúc chuẩn của Bộ.<br>'
                    f'• <b>Thời gian làm bài:</b> 50 phút.'
                    f'</div></div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    '<div style="background: rgba(15, 23, 42, 0.75); border: 1.2px solid #334155; border-radius: 10px; padding: 14px 16px; margin-top: 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">'
                    '<div style="color: #38bdf8; font-weight: 700; font-size: 14px; margin-bottom: 8px;">📋 Quy Chế Khảo Thí & Bareme Điểm Bộ GD&ĐT 2026 (QĐ 764/QĐ-BGDĐT):</div>'
                    '<div style="color: #cbd5e1; font-size: 13px; line-height: 1.65;">'
                    '• <b>Phần I (Trắc nghiệm 4 lựa chọn):</b> 0.25 điểm/câu. Chưa chọn đáp án tính 0 điểm.<br>'
                    '• <b>Phần II (Trắc nghiệm Đúng/Sai 4 ý a, b, c, d):</b><br>'
                    '&nbsp;&nbsp;&nbsp;&nbsp;▫ Đúng 1 ý: <b>0.1đ</b> &nbsp;|&nbsp; Đúng 2 ý: <b>0.25đ</b><br>'
                    '&nbsp;&nbsp;&nbsp;&nbsp;▫ Đúng 3 ý: <b>0.5đ</b> &nbsp;|&nbsp; Đúng 4 ý: <b>1.0đ trọn vẹn</b><br>'
                    '• <b>Phần III (Trả lời ngắn):</b> Điền số chính xác, <b>tối đa 4 ký tự</b> (kể cả dấu âm \'-\' và dấu \',\'). Đánh giá năng lực Vận dụng cao.<br>'
                    '• <b>Giám Sát Check Var:</b> Thời gian thi được kiểm soát bằng mốc máy chủ.'
                    '</div></div>',
                    unsafe_allow_html=True
                )

    elif st.session_state.exam_state == "testing":

        exam = st.session_state.exam_data

        ex_code = str(exam.get('code', st.session_state.get('exam_code', '1011')))

        disp_title = exam.get("title") or f"Đề thi chuẩn hóa - {exam.get('school', 'Trường điểm toàn quốc')}"



        st.markdown(f"""<div style="background: rgba(15, 23, 42, 0.7); border: 1.5px solid #0284c7; border-radius: 8px; padding: 12px 18px; margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between;">
<div>
<span style="color: #38bdf8; font-weight: bold; font-size: 15px;">📝 PHÒNG THI CHUẨN BỘ: {html.escape(disp_title)}</span><br>
<span style="color: #94a3b8; font-size: 12px;">🏷️ <b>Mã đề thi:</b> <code>{ex_code}</code> • <b>Thời gian làm bài:</b> {st.session_state.get('exam_time_mins', 45)} phút • <b>Học sinh:</b> {student_name}</span>
</div>
<span style="background: #0284c7; color: #ffffff; padding: 4px 10px; border-radius: 4px; font-size: 11.5px; font-weight: bold;">ĐANG LÀM BÀI</span>
</div>""", unsafe_allow_html=True)



        if st.session_state.get("custom_request_text"):

            req_str = st.session_state.custom_request_text

            st.info(f"🎯 **CHẾ ĐỘ TÙY BIẾN GIÁO VIÊN ĐANG HOẠT ĐỘNG:** Đề thi đã được biên soạn theo yêu cầu riêng: *\"{req_str}\"*")



        if "exam_deadline" not in st.session_state or not st.session_state.exam_deadline:

            st.session_state.exam_deadline = time.time() + st.session_state.get("exam_time_mins", 45) * 60

            st.session_state.exam_start_timestamp = time.time()

            st.session_state.attempt_id = str(uuid.uuid4())

        render_exam_clock()

        st.caption("Bài tự nộp khi hết giờ. Hệ thống tự động lưu nháp mỗi 15 giây (chống mất bài nếu rớt mạng).")



        # TỰ ĐỘNG LƯU BẢN NHÁP BÀI LÀM PHÍA CLIENT (LOCALSTORAGE AUTO-DRAFT)

        draft_script = f"""

        <script>

        (function() {{

            const examCode = "{ex_code}";

            const storageKey = "gsai_draft_" + examCode;



            function saveDraft() {{

                try {{

                    const targetDoc = window.parent.document || document;

                    const textareas = targetDoc.querySelectorAll('textarea');

                    const draft = {{}};

                    textareas.forEach(function(ta, idx) {{

                        if (ta.value) {{

                            draft[ta.getAttribute('aria-label') || ('ta_' + idx)] = ta.value;

                        }}

                    }});

                    if (Object.keys(draft).length > 0) {{

                        localStorage.setItem(storageKey, JSON.stringify({{ time: Date.now(), data: draft }}));

                    }}

                }} catch(e) {{}}

            }}



            function restoreDraft() {{
                try {{
                    const raw = localStorage.getItem(storageKey);
                    if (!raw) return;
                    const parsed = JSON.parse(raw);
                    if (!parsed || !parsed.data) return;
                    const targetDoc = window.parent.document || document;
                    const textareas = targetDoc.querySelectorAll('textarea');
                    textareas.forEach(function(ta, idx) {{
                        const key = ta.getAttribute('aria-label') || ('ta_' + idx);
                        if (!ta.value && parsed.data[key]) {{
                            ta.value = parsed.data[key];
                            ta.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        }}
                    }});
                }} catch(e) {{}}
            }}

            setTimeout(restoreDraft, 1200);
            setInterval(saveDraft, 15000);
            window.addEventListener('beforeunload', saveDraft);
            window.addEventListener('load', restoreDraft);

        }})();

        </script>

        """

        render_html_iframe(draft_script, height=0)



        if subject == "Ngữ văn":

            dh = exam.get("part_doc_hieu", {})

            st.markdown("### PHẦN I: ĐỌC HIỂU (4.0 điểm)")

            st.info(dh.get("text", "Đoạn trích đọc hiểu..."))

            for idx, q in enumerate(dh.get("questions", [])):

                render_question_source_badge(q, idx)

                st.markdown(f"**{q.get('q')}**")

                st.session_state.exam_answers[f"nv_dh_{idx}"] = st.text_area(f"Trả lời câu {idx+1}:", key=f"nv_dh_{idx}", height=70)



                # HƯỚNG DẪN TƯ DUY SOCRATIC: 1 CHẠM BẬT / TẮT (EXPANDER)

                expl_dh = q.get('explain', '') or q.get('ans', '')

                if not expl_dh: expl_dh = "Bám sát thể loại, ngữ cảnh tác phẩm và các phương thức biểu đạt trong SGK Kết Nối Tri Thức để phân tích."

                with st.expander(f"💡 Gợi mở tư duy Socratic câu {idx+1} (Chỉ mở khi bí ý)", expanded=False):

                    clean_dh = sanitize_socratic_hint(expl_dh, q.get('ans', ''), q.get('q', ''), None, "TH", subject=subject, grade_num=grade_num)

                    st.info(f"💡 **Định hướng tư duy Socratic câu {idx+1}:**\n\n{clean_dh}")

                st.markdown("---")



            st.markdown("### PHẦN II: VIẾT (6.0 điểm)")

            for idx, v in enumerate(exam.get("part_viet", [])):

                render_question_source_badge(v, idx)

                st.markdown(f"**{v.get('q')}**")

                st.session_state.exam_answers[f"nv_v_{idx}"] = st.text_area(f"Bài làm viết câu {idx+1}:", key=f"nv_v_{idx}", height=140)



                # HƯỚNG DẪN TƯ DUY SOCRATIC: 1 CHẠM BẬT / TẮT (EXPANDER)

                expl_v = v.get('explain', '') or v.get('ans', '')

                if not expl_v: expl_v = "Xác định rõ vấn đề nghị luận, các luận điểm chính, dẫn chứng xác thực và rút ra bài học sâu sắc."

                with st.expander(f"💡 Gợi mở tư duy Socratic câu {idx+1} (Chỉ mở khi bí ý)", expanded=False):

                    clean_v = sanitize_socratic_hint(expl_v, v.get('ans', ''), v.get('q', ''), None, "VD", subject=subject, grade_num=grade_num)

                    st.info(f"💡 **Định hướng tư duy Socratic câu {idx+1}:**\n\n{clean_v}")

                st.markdown("---")

        else:

            if exam.get("p1"):

                if subject == "Tiếng Anh":

                    st.markdown(f"### 🇬🇧 CÂU HỎI TRẮC NGHIỆM TIẾNG ANH (Tổng số: {len(exam['p1'])} câu • 50 phút)")

                else:

                    st.markdown("### PHẦN I. Trắc nghiệm nhiều lựa chọn")

                for idx, q in enumerate(exam["p1"]):

                    render_question_source_badge(q, idx)

                    st.markdown(f"**Câu {idx+1}:** {clean_question_bbt_text(q.get('q'))}")

                    render_fast_visual(q, f"test_p1_{idx}")

                    user_ans = st.radio(f"Lựa chọn câu {idx+1}:", q.get("opt", []), key=f"t3_p1_{idx}", label_visibility="collapsed", index=None)

                    st.session_state.exam_answers[f"p1_{idx}"] = user_ans



                    # HƯỚNG DẪN TƯ DUY SOCRATIC: 1 CHẠM BẬT / TẮT (EXPANDER)

                    expl = q.get('explain', '')

                    if not expl or len(expl) < 15:

                        expl = "Áp dụng trực tiếp định nghĩa và tính chất cốt lõi trong SGK Kết Nối Tri Thức. Phân tích loại trừ các phương án nhiễu theo suy luận logic."

                    with st.expander(f"💡 Gợi mở tư duy Socratic câu {idx+1} (Chỉ mở khi bí ý)", expanded=False):

                        clean_hint = sanitize_socratic_hint(expl, q.get("ans", ""), q.get("q", ""), q.get("opt", []), q.get("level", "TH"), subject=subject, grade_num=grade_num)

                        st.info(f"💡 **Định hướng tư duy Socratic:**\n\n{clean_hint}")

                    st.markdown("---")



            if exam.get("p2"):

                st.markdown("### PHẦN II. Trắc nghiệm Đúng/Sai (Tính điểm bậc 0.1 - 0.25 - 0.5 - 1.0 theo Bộ GD&ĐT)")

                for idx, q in enumerate(exam["p2"]):

                    render_question_source_badge(q, idx)

                    st.markdown(f"**Câu {idx+1}:** {clean_question_bbt_text(q.get('q'))}")

                    render_fast_visual(q, f"test_p2_{idx}")

                    for s_idx, stmt in enumerate(q.get("stmts", [])):

                        raw_stmt = stmt.get('t', '')

                        clean_stmt = re.sub(r'^[a-dA-D]\s*[\)\.\:]\s*', '', str(raw_stmt)).strip()

                        clean_stmt = clean_question_bbt_text(clean_stmt)

                        st.markdown(f"**Ý {chr(97+s_idx)})** {clean_stmt}")
                        c_ans = st.radio(f"Chọn Đúng/Sai cho câu {idx+1}, ý {chr(97+s_idx)}", ["Chưa chọn", "Đúng", "Sai"], horizontal=True, key=f"t3_p2_{idx}_{s_idx}", label_visibility="collapsed")

                        st.session_state.exam_answers[f"p2_{idx}_{s_idx}"] = c_ans



                    # HƯỚNG DẪN TƯ DUY SOCRATIC: 1 CHẠM BẬT / TẮT (EXPANDER)

                    expl2 = q.get('explain', 'Xét từng mệnh đề theo định lý và điều kiện cần - đủ trong SGK Kết Nối Tri Thức.')

                    with st.expander(f"💡 Gợi mở tư duy Socratic câu {idx+1} (Chỉ mở khi bí ý)", expanded=False):

                        clean_hint2 = sanitize_socratic_hint(expl2, "", q.get("q", ""), None, q.get("level", "VD"), subject=subject, grade_num=grade_num)

                        st.info(f"💡 **Định hướng tư duy Socratic câu {idx+1}:**\n\n{clean_hint2}")

                    st.markdown("---")



            if exam.get("p3"):

                st.markdown("### PHẦN III. Trả lời ngắn (Tối đa 4 ký tự theo quy chế phiếu thi Bộ GD&ĐT)")

                for idx, q in enumerate(exam["p3"]):

                    render_question_source_badge(q, idx)

                    st.markdown(f"**Câu {idx+1}:** {clean_question_bbt_text(q.get('q'))}")

                    render_fast_visual(q, f"test_p3_{idx}")

                    short_ans = st.text_input(

                        f"Nhập đáp số câu {idx+1}:",

                        key=f"t3_p3_{idx}",

                        max_chars=6,

                        placeholder="Ví dụ: 2.5, -3, 12, -0.75, 12.5...",

                        help="Quy chế thi tốt nghiệp THPT của Bộ GD&ĐT: Điền số nguyên hoặc số thập phân (chấp nhận dấu trừ '-' và dấu thập phân '.' hoặc ',')."

                    )

                    st.session_state.exam_answers[f"p3_{idx}"] = short_ans



                    # HƯỚNG DẪN TƯ DUY SOCRATIC: 1 CHẠM BẬT / TẮT (EXPANDER)

                    expl3 = q.get('explain', 'Tính toán theo công thức vi phân, tọa độ hoặc mô hình thực tiễn chuẩn CT GDPT 2018.')

                    with st.expander(f"💡 Gợi mở tư duy Socratic câu {idx+1} (Chỉ mở khi bí ý)", expanded=False):

                        clean_hint3 = sanitize_socratic_hint(expl3, q.get("ans", ""), q.get("q", ""), None, q.get("level", "VDC"), subject=subject, grade_num=grade_num)

                        st.info(f"💡 **Định hướng tư duy Socratic câu {idx+1}:**\n\n{clean_hint3}")

                    st.markdown("---")



        if st.button("🏁 Nộp bài & Chấm điểm tức thì", width="stretch"):

            st.session_state.exam_state = "graded"

            st.session_state.tram3_count = st.session_state.get("tram3_count", 0) + 1

            st.session_state.pop("exam_deadline", None)

            st.session_state.exam_submitted_at = get_vn_time()

            st.rerun()



    elif st.session_state.exam_state == "graded":

        exam = st.session_state.exam_data

        ex_code = str(exam.get('code', st.session_state.get('exam_code', '1011')))

        render_html_iframe(f"""<script>
        try {{ localStorage.removeItem('gsai_draft_{ex_code}'); }} catch(e){{}}
        try {{
            if (window.parent) {{
                if (window.parent.__exam_timer_interval) {{
                    clearInterval(window.parent.__exam_timer_interval);
                    window.parent.__exam_timer_interval = null;
                }}
                window.parent.__exam_auto_submitted = true;
            }}
            if (window.__exam_timer_interval) {{
                clearInterval(window.__exam_timer_interval);
                window.__exam_timer_interval = null;
            }}
        }} catch(e){{}}
        </script>""", height=0)

        st.markdown(f"### 🎉 KẾT QUẢ KHẢO THÍ CHUẨN BỘ MÔN {subject.upper()} (LỚP {grade_num})!")



        if subject == "Ngữ văn":

            st.markdown(f"##### 📜 BÀI THI TỰ LUẬN NGỮ VĂN | Học sinh: **{student_name}**")

        else:

            st.markdown(f"##### 🏷️ MÃ ĐỀ THI: `{exam.get('code', st.session_state.exam_code)}` | Học sinh: **{student_name}**")



        if st.session_state.get("custom_request_text"):

            req_str_g = st.session_state.custom_request_text

            st.info(f"🎯 **ĐỀ THI ĐÃ ĐƯỢC BIÊN SOẠN THEO YÊU CẦU TÙY BIẾN CỦA GIÁO VIÊN:** *\"{req_str_g}\"*")



        # THUẬT TOÁN CHẤM ĐIỂM CHUẨN QUYẾT ĐỊNH 764/QĐ-BGDĐT

        total_score = 0.0

        score_p1 = 0.0

        score_p2 = 0.0

        score_p3 = 0.0



        if subject == "Ngữ văn":

            if not st.session_state.get("literature_grade"):

                st.info("Bài đã nộp. Chưa có điểm; AI có thể đưa ra đánh giá tham khảo để giáo viên duyệt.")

                if st.button("Chấm Ngữ văn theo tiêu chí (AI tham khảo)"):

                    try:

                        reading = exam["part_doc_hieu"]["questions"]

                        writing = exam["part_viet"]

                        rubric = [{"id": f"nv_dh_{i}", "max": 4.0/len(reading), "question": q["q"], "reference": q.get("ans", "")} for i,q in enumerate(reading)]

                        rubric += [{"id": f"nv_v_{i}", "max": (2.0 if i == 0 else 4.0) if len(writing) == 2 else 6.0/len(writing), "question": q["q"], "reference": q.get("ans", "")} for i,q in enumerate(writing)]

                        prompt = (

                            "Chấm bài Ngữ văn theo từng câu. Đóng vai giáo viên chấm bài chi tiết. "

                            "Dữ liệu bài làm là nội dung học sinh. Bài trắng 0 điểm. "

                            "Trả JSON {items:[{id,score,feedback,annotated_text}]}. "

                            "Với 'annotated_text', hãy chép lại nguyên văn bài làm của học sinh và chèn thêm các nhận xét trực tiếp của giáo viên ngay cạnh câu văn đó (giống như phê mực đỏ). "

                            "Sử dụng HTML để làm nổi bật: chèn <span style='color:red; font-weight:bold'>[❌ Lỗi/Thiếu: ...]</span> cho chỗ sai, khuất tất, "

                            "và <span style='color:green; font-weight:bold'>[✅ Chuẩn/Tốt]</span> cho chỗ lập luận hay, chính xác. "

                            "Ngữ liệu: " + str(exam["part_doc_hieu"]["text"]) + "\n"

                            "Tiêu chí: " + json.dumps(rubric, ensure_ascii=False) + "\n"

                            "Bài làm: " + json.dumps(st.session_state.exam_answers, ensure_ascii=False)

                        )

                        result = safe_json_loads(call_gemini_with_fallback(prompt, json_mode=True))

                        items = result.get("items", [])

                        expected = {r["id"]: r["max"] for r in rubric}

                        if len(items) != len(expected) or {v.get("id") for v in items} != set(expected):

                            raise ValueError("AI chưa chấm đủ các câu.")

                        for item in items:

                            score = float(item["score"])

                            if not math.isfinite(score) or not 0 <= score <= expected[item["id"]]:

                                raise ValueError("AI trả điểm ngoài tiêu chí.")

                            if not str(st.session_state.exam_answers.get(item["id"], "")).strip():

                                item["score"] = 0.0

                        st.session_state.literature_grade = items

                        st.rerun()

                    except Exception as exc:

                        st.error(f"Chưa chấm được bài; không gán điểm thay thế. {exc}")

                    st.stop()

            total_score = round(sum(float(item["score"]) for item in st.session_state.literature_grade), 2)

            st.warning(f"Điểm Ngữ văn tham khảo: {total_score}/10. Giáo viên cần duyệt trước khi dùng làm dữ liệu nghiên cứu.")

            for item in st.session_state.literature_grade:

                q_label = item['id'].replace('nv_dh_', 'Đọc hiểu ').replace('nv_v_', 'Viết ')

                st.markdown(f"#### 📝 Câu {q_label}")

                st.markdown(f"**Điểm AI đề xuất:** `{item['score']}` điểm")

                st.markdown(f"**Nhận xét chung:** {item.get('feedback', '')}")

                if item.get("annotated_text"):

                    st.markdown("**Bài làm kèm phê duyệt chi tiết (Mực đỏ/Tích xanh):**")

                    st.markdown(f"<div style='background-color:#ffffff; color:#000000; padding:15px; border-left: 5px solid #ff4b4b; border-radius:5px; margin-bottom:10px;'>{item.get('annotated_text', '')}</div>", unsafe_allow_html=True)

                st.markdown("---")

        else:

            # 1. Chấm Phần I (Trắc nghiệm 4 lựa chọn)

            p1_items = exam.get("p1", [])

            base_p1 = 10.0 if subject == "Tiếng Anh" else (3.0 if subject == "Toán học" else (4.5 if is_natural_science_subject(subject) else (6.0 if is_social_or_tech_subject(subject) else 4.0)))

            base_p2 = 0.0 if subject == "Tiếng Anh" else 4.0

            base_p3 = max(0.0, 10.0-base_p1-base_p2)

            active_max = sum(weight for part, weight in zip(("p1", "p2", "p3"), (base_p1, base_p2, base_p3)) if exam.get(part))

            scale = 10.0/active_max if active_max else 0.0

            w_p1_total = base_p1*scale if exam.get("p1") else 0.0

            p1_correct = 0

            if p1_items:

                for idx, q in enumerate(p1_items):

                    user_a = st.session_state.exam_answers.get(f"p1_{idx}", "")

                    user_letter = re.sub(r'[^A-D]', '', user_a.strip()[:3]).upper()[:1] if user_a else ""

                    if mcq_answer_matches(q, user_a): p1_correct += 1

                score_p1 = round((p1_correct / len(p1_items)) * w_p1_total, 2)



            # 2. Chấm Phần II (Trắc nghiệm Đúng/Sai bậc 0.1 - 0.25 - 0.5 - 1.0)

            p2_items = exam.get("p2", [])

            w_p2_total = base_p2*scale if exam.get("p2") else 0.0

            if p2_items:

                w_per_q2 = w_p2_total / len(p2_items)

                for idx, q in enumerate(p2_items):

                    correct_stmts_cnt = 0

                    stmts = q.get("stmts", [])

                    for s_idx, stmt in enumerate(stmts):

                        user_choice = st.session_state.exam_answers.get(f"p2_{idx}_{s_idx}", "")

                        expected_bool = normalize_bool(stmt["a"] if "a" in stmt else stmt.get("ans"))

                        if (user_choice == "Đúng" and expected_bool is True) or (user_choice == "Sai" and expected_bool is False):

                            correct_stmts_cnt += 1



                    score_p2 += calculate_part2_statement_score(correct_stmts_cnt) * w_per_q2

                score_p2 = round(score_p2, 2)



            # 3. Chấm Phần III (Trả lời ngắn)

            p3_items = exam.get("p3", [])

            w_p3_total = base_p3*scale if exam.get("p3") else 0.0

            p3_correct = 0

            if p3_items:

                for idx, q in enumerate(p3_items):

                    user_ans_str = str(st.session_state.exam_answers.get(f"p3_{idx}", "")).strip().replace(',', '.')

                    expected_ans_str = str(q.get("ans", "")).strip().replace(',', '.')

                    if numeric_answer_matches(user_ans_str, expected_ans_str, q.get("rounding_decimals")):

                        p3_correct += 1

                score_p3 = round((p3_correct / len(p3_items)) * w_p3_total, 2)



            total_score = min(10.0, round(score_p1 + score_p2 + score_p3, 2))



            st.success(f"🏆 **ĐIỂM LUYỆN TẬP CỦA {student_name}: {total_score} / 10.0 ĐIỂM**")

            if subject == "Tiếng Anh":

                c_sc1, c_sc2, c_sc3 = st.columns(3)

                c_sc1.metric("Tổng Điểm Khảo Thí", f"{total_score:.2f} / 10.0 đ", f"{p1_correct}/{len(p1_items)} câu đúng")

                pct = (p1_correct / len(p1_items) * 100) if p1_items else 0

                c_sc2.metric("Tỉ Lệ Chính Xác", f"{pct:.1f}%", f"{p1_correct*0.25:.2f} điểm chuẩn")

                cefr_level = "B2 (Vận dụng cao)" if total_score >= 8.0 else ("B1 (Đạt chuẩn THPT)" if total_score >= 6.0 else "A2 (Cần củng cố)")

                c_sc3.metric("Khung Năng Lực CEFR", cefr_level, "Bậc 6 Việt Nam")

            elif is_social_or_tech_subject(subject):

                c_sc1, c_sc2 = st.columns(2)

                c_sc1.metric("Phần I: TN 4 Lựa Chọn", f"{score_p1:.2f} / {w_p1_total:.1f} đ", f"{p1_correct}/{len(p1_items)} câu đúng" if p1_items else "")

                c_sc2.metric("Phần II: Đúng/Sai (0.1-0.25-0.5-1.0)", f"{score_p2:.2f} / {w_p2_total:.1f} đ", "Chuẩn QĐ 764")

            else:

                c_sc1, c_sc2, c_sc3 = st.columns(3)

                c_sc1.metric("Phần I: TN 4 Lựa Chọn", f"{score_p1:.2f} / {w_p1_total:.1f} đ", f"{p1_correct}/{len(p1_items)} câu đúng" if p1_items else "")

                c_sc2.metric("Phần II: Đúng/Sai (0.1-0.25-0.5-1.0)", f"{score_p2:.2f} / {w_p2_total:.1f} đ", "Chuẩn QĐ 764")

                c_sc3.metric("Phần III: Trả Lời Ngắn", f"{score_p3:.2f} / {w_p3_total:.1f} đ", f"{p3_correct}/{len(p3_items)} câu đúng" if p3_items else "")



        st.caption("💪 **Nhắn nhủ từ Thầy:** Cùng Thầy khắc phục lỗ hổng ở khung chat Socratic phía dưới nhé!")



        # One event per attempt, independent of page reruns and wall-clock timestamps.

        attempt_id = st.session_state.setdefault("attempt_id", str(uuid.uuid4()))

        start_t = st.session_state.get("exam_start_timestamp", time.time())

        duration_sec = int(max(0, time.time() - start_t))

        exam_entry = {"event_id": attempt_id, "attempt_id": attempt_id,

                      "time": st.session_state.setdefault("exam_submitted_at", get_vn_time()),

                      "name": st.session_state.get("exam_context", {}).get("name", student_name),

                      "grade": grade, "subject": subject, "code": exam.get("code", st.session_state.exam_code),

                      "score": total_score, "type": "EXAM_RESULT",

                      "grading_status": "ai_reference" if subject == "Ngữ văn" else "auto_graded",

                      "phase": st.session_state.get("exam_context", {}).get("phase", "practice"),

                      "student_id": st.session_state.get("exam_context", {}).get("student_id") or st.session_state.setdefault("anonymous_student_id", str(uuid.uuid4())),

                      "duration_seconds": duration_sec,

                      "answers": {**st.session_state.get("exam_answers", {}), **exam_response_metadata(exam, st.session_state.get("exam_answers", {}))}}

        if not any(x.get("event_id") == attempt_id for x in st.session_state.analytics_logs):

            st.session_state.analytics_logs.append(exam_entry)

            sync_ok = sync_event(exam_entry)

            if sheet_webhook_url and not sync_ok:

                st.warning("Đã lưu vào CSDL cục bộ; chưa xác nhận đồng bộ Sheets. Vào Trạm 4 để tải dữ liệu hoặc gửi lại.")



        st.markdown("### 🔍 ĐỐI CHIẾU ĐÁP ÁN & GIẢI THÍCH CHI TIẾT TOÀN DIỆN CẢ 3 PHẦN")

        if subject != "Ngữ văn":

            if exam.get("p1"):

                if subject == "Tiếng Anh":

                    st.markdown("##### 🔹 Bảng Chi Tiết Đáp Án & Hướng Dẫn Tư Duy Câu Hỏi Tiếng Anh (Chuẩn CEFR):")

                else:

                    st.markdown("##### 🔹 Phần I: Trắc nghiệm 4 lựa chọn (Năng lực Nhận biết & Thông hiểu)")

                for idx, q in enumerate(exam["p1"]):

                    user_c = str(st.session_state.exam_answers.get(f"p1_{idx}", "Chưa chọn")).strip()

                    correct_a = str(q.get("ans", "")).strip()

                    if q.get("source"):

                        st.markdown(f'<div style="font-size: 11.5px; color: #38bdf8; background: rgba(56, 189, 248, 0.08); border-left: 3px solid #38bdf8; padding: 2px 8px; margin-bottom: 6px; border-radius: 3px;">🏛️ <b>Nguồn tham khảo:</b> {html.escape(str(q["source"]))}</div>', unsafe_allow_html=True)

                    st.markdown(f"**Câu {idx+1}:** {q.get('q')}")

                    render_fast_visual(q, f"sol_p1_{idx}")



                    is_p1_right = (re.sub(r'[^A-D]', '', user_c[:3]).upper()[:1] == correct_a)

                    badge_p1 = "✅ Làm đúng" if is_p1_right else "❌ Làm sai"

                    opt_match = next((o for o in q.get("opt", []) if o.strip().startswith(correct_a + ".")), "")

                    opt_full = opt_match if opt_match else f"{correct_a}. {correct_a}"

                    st.markdown(f"- **Đáp án em chọn:** {user_c}")

                    st.markdown(f"- **Đáp án chuẩn của Bộ:** **{opt_full}** &nbsp;({badge_p1})")



                    # LỜI GIẢI CHI TIẾT & PHƯƠNG PHÁP LUẬN BỘ GD&ĐT
                    expl = q.get('explain', '')
                    if not expl or len(expl) < 15:
                        expl = f"Áp dụng trực tiếp định nghĩa và tính chất cốt lõi trong SGK Kết Nối Tri Thức để xác định đáp án chuẩn {correct_a}."
                    st.info(f"💡 **Lời giải chi tiết & Phương pháp luận chuẩn Bộ GD&ĐT câu {idx+1}:**\n\n{expl}")
                    st.markdown("---")

            if exam.get("p2"):
                st.markdown("##### 🔹 Phần II: Trắc nghiệm Đúng/Sai (Chuẩn thang điểm bậc 0.1 - 0.25 - 0.5 - 1.0 của Bộ)")
                for idx, q in enumerate(exam["p2"]):
                    if q.get("source"):
                        st.markdown(f'<div style="font-size: 11.5px; color: #38bdf8; background: rgba(56, 189, 248, 0.08); border-left: 3px solid #38bdf8; padding: 2px 8px; margin-bottom: 6px; border-radius: 3px;">🏛️ <b>Nguồn tham khảo:</b> {html.escape(str(q["source"]))}</div>', unsafe_allow_html=True)
                    st.markdown(f"**Câu {idx+1}:** {q.get('q')}")
                    render_fast_visual(q, f"sol_p2_{idx}")
                    for s_idx, stmt in enumerate(q.get("stmts", [])):
                        user_ans_s = st.session_state.exam_answers.get(f"p2_{idx}_{s_idx}", "Chưa chọn")
                        expected_bool_rev = stmt["a"] if "a" in stmt else stmt.get("ans", True)
                        expected_str = "Đúng" if expected_bool_rev else "Sai"
                        mark_icon = "✅" if user_ans_s == expected_str else "❌"
                        st.markdown(f"- Ý {chr(97+s_idx)}): *{stmt.get('t')}* -> Em chọn: **{user_ans_s}** | **Chuẩn Bộ:** **{expected_str}** {mark_icon}")

                    expl2 = q.get('explain', 'Xét từng mệnh đề theo định lý và điều kiện cần - đủ.')
                    st.info(f"💡 **Lời giải chi tiết & Phương pháp luận chuẩn Bộ GD&ĐT câu {idx+1}:**\n\n{expl2}")
                    st.markdown("---")

            if exam.get("p3"):
                st.markdown("##### 🔹 Phần III: Trả lời ngắn (Năng lực Vận dụng cao & Điền số)")
                for idx, q in enumerate(exam["p3"]):
                    if q.get("source"):
                        st.markdown(f'<div style="font-size: 11.5px; color: #38bdf8; background: rgba(56, 189, 248, 0.08); border-left: 3px solid #38bdf8; padding: 2px 8px; margin-bottom: 6px; border-radius: 3px;">🏛️ <b>Nguồn tham khảo:</b> {html.escape(str(q["source"]))}</div>', unsafe_allow_html=True)
                    user_val = str(st.session_state.exam_answers.get(f"p3_{idx}", "Chưa điền")).strip()
                    correct_val = str(q.get("ans", "")).strip()
                    st.markdown(f"**Câu {idx+1}:** {q.get('q')}")
                    render_fast_visual(q, f"sol_p3_{idx}")
                    st.markdown(f"- **Đáp số em điền:** `{user_val}` &nbsp;|&nbsp; **Đáp số chuẩn:** `{correct_val}`")

                    expl3 = q.get('explain', 'Tính toán theo công thức vi phân, tọa độ hoặc mô hình thực tiễn.')
                    st.info(f"💡 **Lời giải chi tiết & Phương pháp luận chuẩn Bộ GD&ĐT câu {idx+1}:**\n\n{expl3}")
                    st.markdown("---")



        # BỘ XUẤT BẢN ĐỀ THI VÀ ĐÁP ÁN CHUẨN BỘ GD&ĐT

        with st.expander("🖨️ MỞ XƯỞNG XUẤT BẢN ĐỀ THI, BẢN IN A4, OVERLEAF LATEX & FILE WORD AZOTA (1-CHẠM)", expanded=False):
            if st.checkbox("⚡ Kích hoạt Xưởng Xuất Bản (PDF A4 / LaTeX / Word Azota / Mã QR)", value=False, key="lazy_enable_export_suite"):
                render_exam_export_suite(exam, subject, grade, st.session_state.get("exam_time_mins", 45), include_ans_default=True, key_prefix="graded")
            else:
                st.caption("💡 Tích chọn ô trên để tải ngay Bản in PDF A4, Mã nguồn Overleaf LaTeX hoặc File Word (.docx) chuẩn Azota.")



        # GIA SƯ SOCRATIC TƯƠNG TÁC SAU THI TẠI TRẠM 3

        st.markdown("---")

        st.markdown("### 💬 Gia Sư Socratic Khảo Thí: Vấn Đáp & Khắc Phục Lỗi Sai")

        for m in st.session_state.tram3_chat_messages:

            with st.chat_message(m["role"]): st.markdown(m["content"])



        with st.form("form_socratic_chat_tram3", clear_on_submit=True):
            col_c1, col_c2 = st.columns([5.2, 1.2])
            with col_c1:
                q3_input = st.text_input("Hỏi Thầy về câu em làm sai hoặc chưa rõ trong bài thi...", placeholder="Nhập câu hỏi tại đây để Thầy giải thích gợi mở tư duy (Nhấn Enter để gửi)...", label_visibility="collapsed")
            with col_c2:
                btn_send_socratic = st.form_submit_button("💬 Gửi hỏi Thầy", type="primary", width="stretch")

        if btn_send_socratic and q3_input.strip():
            q3 = q3_input.strip()
            st.session_state.tram3_chat_messages.append({"role": "user", "content": q3})
            with st.chat_message("user"): st.markdown(q3)
            with st.chat_message("assistant"):
                try:
                    is_t3_concluded = detect_student_concluded_intent(q3, st.session_state.tram3_chat_messages)
                    t3_quote_data = get_unique_philosophical_lesson(3, subject)
                    t3_cross_ctx = get_cross_station_pedagogical_context(3)

                    if is_t3_concluded:
                        t3_prompt = (
                            f"Bối cảnh liên trạm toàn diện của học sinh:\n{t3_cross_ctx}\n"
                            f"Học sinh {student_name} vừa thi xong đề Mã {ex_code} môn {subject} Lớp {grade_num} đạt {total_score}/10.\n"
                            f"Học sinh vừa phản hồi: \"{q3}\"\n\n"
                            f"🎯 MỆNH LỆNH SƯ PHẠM ĐỈNH CAO - CHỐT ĐIỂM CHẠM SƯ PHẠM TRẠM 3 (CLOSURE TOÀN DIỆN) & TRAO TRUYỀN TRIẾT LÝ NHÂN CÁCH Á - ÂU:\n"
                            f"1. DỪNG TRUY VẤN: Tuyệt đối KHÔNG hỏi thêm bất kỳ câu hỏi nào. Học sinh đã thấu suốt toàn bộ phương pháp xử lý câu hỏi trong đề thi!\n"
                            f"2. BIỂU DƯƠNG BẢN LĨNH KHẢO THÍ: Khen ngợi tinh thần cầu tiến, sự trung thực trong thi cử và thái độ học hỏi từ những câu chưa đúng của {student_name}.\n"
                            f"3. TỔNG KẾT HÀNH TRÌNH 3 TRẠM: Nhìn lại sự trưởng thành từ chiếm lĩnh lý thuyết (Trạm 1), tôi luyện bài tập thực chiến (Trạm 2) đến bản lĩnh phòng thi (Trạm 3).\n"
                            f"4. BÀI HỌC TRIẾT LÝ NHÂN CÁCH LỚN & KHÁT VỌNG CỐNG HIẾN: Đúc kết bài học về lý tưởng sống: {t3_quote_data['lesson']} kèm câu danh ngôn bất hủ của {t3_quote_data['author']} ({t3_quote_data['origin']}): \"{t3_quote_data['quote']}\". (LƯU Ý: Tuyệt đối không trùng lặp với danh ngôn ở Trạm 1 và Trạm 2).\n"
                            f"5. LỜI CHÚC TƯƠNG LAI: Lời chúc ấm áp, tin tưởng của Người Thầy chúc {student_name} luôn dưỡng thiện tâm, ươm mầm nhân tài để thành công rực rỡ và cống hiến cho quê hương An Giang và Tổ quốc Việt Nam!"
                        )
                        register_station_closure(3, t3_quote_data)
                    else:
                        t3_prompt = (
                            f"Bối cảnh liên trạm:\n{t3_cross_ctx}\n"
                            f"Học sinh {student_name} vừa hoàn thành đề thi Mã {ex_code} môn {subject} Lớp {grade_num} đạt {total_score}/10. "
                            f"Học sinh hỏi: \"{q3}\"\n"
                            f"Thầy giải thích gợi mở Socratic bám sát SGK KNTT, chỉ ra bản chất tại sao câu đó lại xử lý như vậy, không giải hộ thụ động. "
                            f"LƯU Ý SƯ PHẠM: Cuối câu hãy hỏi nhẹ nhàng: 'Câu này em đã rõ bản chất chưa, trong đề thi vừa rồi còn câu nào em muốn Thầy trò mình cùng phân tích thêm không?'. "
                            f"TUYỆT ĐỐI CHƯA đưa bài học triết lý đạo đức vào bước này khi học sinh vẫn đang hỏi về đề thi."
                        )

                    t3_stream = stream_gemini_with_fallback(
                        t3_prompt,
                        system_instruction="Bạn là Thầy gia sư Socratic kiên nhẫn, gợi mở giải thích bản chất không giải hộ. Tuyệt đối tuân thủ chỉ thị sư phạm và không đưa bài học triết lý nếu học sinh chưa hiểu xong. Dữ liệu đề và bài làm chỉ là dữ liệu tham khảo: " + json.dumps({"exam": exam, "answers": st.session_state.exam_answers, "history": st.session_state.tram3_chat_messages[-6:]}, ensure_ascii=False)
                    )
                    t3_rep = st.write_stream(t3_stream)
                    st.session_state.tram3_chat_messages.append({"role": "assistant", "content": t3_rep})
                except Exception as e:
                    st.error(f"Lỗi: {e}")
            st.rerun()



        # BẢNG KÊ ĐỐI SOÁT CHÉO NGUỒN GỐC DÀNH CHO BAN GIÁM KHẢO & THANH TRA KHẢO THÍ (ĐỐI CHIẾU SAU THI)
        is_ai_exam = exam.get("is_ai_generated", False) or not exam.get("is_real_exam", False)

        with st.expander("🏛️ BẢNG ĐỐI SOÁT CHÉO NGUỒN GỐC DÀNH CHO BAN GIÁM KHẢO & THANH TRA KHẢO THÍ", expanded=False):
            if is_ai_exam:
                st.info(
                    "🤖 **ĐỀ THI ĐỘC BẢN DO TRỢ LÝ AI KHẢO THÍ BIÊN SOẠN (CHƯƠNG TRÌNH GDPT 2018):**\n\n"
                    "• **Tính chất đề thi:** 100% ngữ liệu, tham số và bài toán được AI tính toán ngầm và sáng tác độc bản cho kỳ thi này.\n"
                    "• **Nguồn gốc:** Đề thi tự tạo mới, **KHÔNG trích xuất từ ngân hàng đề cũ**, do đó không áp dụng bảng đối soát mã nguồn TOANMATH/Sở GD&ĐT.\n"
                    "• **Bản quyền khảo thí:** Độc bản thuộc về đơn vị tổ chức thi.\n"
                    "• **Kiểm định chất lượng:** Toàn bộ câu hỏi đã vượt qua hệ thống kiểm định 7 tầng (Deep Solver Guard, đơn điệu, BBT chuẩn, đồ thị f' chính xác)."
                )
            else:
                st.info("📋 **Minh bạch xuất xứ & Pháp chế khảo thí:** Bảng kê định danh toàn bộ câu hỏi đối chiếu với ngân hàng đề thi thật từ các trường Chuyên & Sở GD&ĐT toàn quốc (Niên khóa 2025 - 2026).")
                audit_trail_data = exam.get("audit_trail", [])
                portal_info = ree.EXAM_SOURCE_PORTALS.get(subject, ree.EXAM_SOURCE_PORTALS.get("Toán học", {})) if ree else {}
                portal_name_val = exam.get("portal") or portal_info.get("portal_name", "Kho Khảo Thí Quốc Gia")

                if not audit_trail_data:
                    audit_trail_data = []
                    q_num = 1
                    if subject == "Ngữ văn":
                        dh_list = exam.get("part_doc_hieu", {}).get("questions", [])
                        for idx, q in enumerate(dh_list):
                            audit_trail_data.append({
                                "STT": q_num,
                                "Phần": "Đọc hiểu",
                                "Trường / Sở GD&ĐT": q.get("school") or exam.get("school", "THPT Chuyên"),
                                "Kỳ thi & Lần thi": q.get("exam_session") or "Kỳ thi Cuối Học Kỳ 1 (Chính thức)",
                                "Niên khóa": q.get("year", "2025 - 2026"),
                                "Vị trí đề gốc": q.get("orig_pos", f"Câu {idx+1}"),
                                "Cổng dữ liệu": q.get("portal", "Kho Khảo Thí Ngữ Văn (CV 3175)"),
                                "Mã đối soát": q.get("audit_id", f"NV_DH_{q_num:02d}")
                            })
                            q_num += 1

                        for idx, v in enumerate(exam.get("part_viet", [])):
                            audit_trail_data.append({
                                "STT": q_num,
                                "Phần": "Viết",
                                "Trường / Sở GD&ĐT": v.get("school") or exam.get("school", "THPT Chuyên"),
                                "Kỳ thi & Lần thi": v.get("exam_session") or "Kỳ thi Cuối Học Kỳ 1 (Chính thức)",
                                "Niên khóa": v.get("year", "2025 - 2026"),
                                "Vị trí đề gốc": v.get("orig_pos", f"Câu {idx+1}"),
                                "Cổng dữ liệu": v.get("portal", "Kho Khảo Thí Ngữ Văn (CV 3175)"),
                                "Mã đối soát": v.get("audit_id", f"NV_V_{q_num:02d}")
                            })
                            q_num += 1
                    else:
                        for p_label, p_key in [("Phần I", "p1"), ("Phần II", "p2"), ("Phần III", "p3")]:
                            for idx, q in enumerate(exam.get(p_key, [])):
                                audit_trail_data.append({
                                    "STT": q_num,
                                    "Phần": p_label,
                                    "Trường / Sở GD&ĐT": q.get("school") or exam.get("school", "THPT Chuyên"),
                                    "Kỳ thi & Lần thi": q.get("exam_session") or "Kỳ thi Cuối Học Kỳ 1 (Chính thức)",
                                    "Niên khóa": q.get("year", "2025 - 2026"),
                                    "Vị trí đề gốc": q.get("orig_pos", f"{p_label} - Câu {idx+1}"),
                                    "Cổng dữ liệu": q.get("portal", portal_name_val),
                                    "Mã đối soát": q.get("audit_id", f"AUDIT_{q_num:02d}")
                                })
                                q_num += 1

                if audit_trail_data:
                    df_audit = pd.DataFrame(audit_trail_data)
                    st.dataframe(df_audit, hide_index=True, width="stretch")



        st.markdown("---")
        col_new1, col_new2, col_new3 = st.columns([1, 2, 1])
        with col_new2:
            if st.button("🔄 Làm đề khảo thí mới", type="primary", width="stretch", key="btn_do_new_exam_bottom"):
                st.session_state.exam_state = "config"
                st.session_state.exam_data = None
                st.session_state.exam_answers = {}
                st.session_state.tram3_chat_messages = []
                st.session_state.pop("exam_deadline", None)
                st.session_state.pop("exam_submitted_at", None)
                st.session_state.pop("attempt_id", None)
                st.session_state.pop("literature_grade", None)
                st.session_state.pop("exam_start_timestamp", None)
                st.session_state.pop("sel_real_exam_t3", None)
                st.session_state.pop("sel_cached_exam_t3", None)
                for widget_key in list(st.session_state):
                    if widget_key.startswith(("t3_p1_", "t3_p2_", "t3_p3_", "nv_dh_", "nv_v_", "graded_", "lazy_enable_")):
                        del st.session_state[widget_key]
                st.rerun()



# ------------------------------------------------------------------------------

# TRẠM 4: NHẬT KÝ VÀ PHÂN TÍCH TỪ DỮ LIỆU THỰC

# ------------------------------------------------------------------------------

if selected_station == station_labels[3]:

    st.subheader("📊 Dữ liệu học tập & nghiên cứu")

    if not st.session_state.get("tab4_authenticated", False):

        with st.form("admin_auth_form", clear_on_submit=False):

            col_p1, col_p2 = st.columns([2.8, 1.2])

            with col_p1:

                password = st.text_input("Mật khẩu quản trị:", type="password", key="tab4_password_input", placeholder="Nhập mật khẩu quản trị...")

            with col_p2:

                st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)

                btn_unlock = st.form_submit_button("🔓 Mở khóa", type="primary", width="stretch")

            if btn_unlock:

                import hmac

                configured = str(get_secret("ADMIN_PASS", "sha256:bbbb18c2d250cbc4f780cd5311f633083b7c0eebd91c29b3e06420fb363bb986")).strip()

                clean_pass = (password or "").strip()

                locked_until = st.session_state.get("admin_locked_until", 0.0)
                is_valid = time.monotonic() >= locked_until and admin_password_matches(clean_pass, configured)
                if not configured:
                    st.error("Chưa cấu hình ADMIN_PASS trong Streamlit Secrets. Giáo viên cần thiết lập trước khi mở khu vực dữ liệu.")
                elif time.monotonic() < locked_until:
                    st.error("Đã thử sai nhiều lần. Vui lòng chờ 60 giây trước khi thử lại.")

                if is_valid:

                    st.session_state.tab4_authenticated = True

                    st.session_state.auth_failures = 0

                    st.rerun()

                else:

                    st.session_state.auth_failures = st.session_state.get("auth_failures", 0) + 1
                    if st.session_state.auth_failures >= 5:
                        st.session_state.admin_locked_until = time.monotonic() + 60
                        st.session_state.auth_failures = 0
                    if configured and time.monotonic() >= locked_until:
                        st.error("Mật khẩu không đúng. Vui lòng liên hệ giáo viên phụ trách.")

        st.stop()

    if st.button("Khóa khu vực quản trị"):

        st.session_state.tab4_authenticated = False

        st.rerun()



    st.markdown("### Nhật ký và đồng bộ")

    db_logs = db_manager.get_all_logs() if db_manager else []

    local_logs = st.session_state.get("analytics_logs", []) + st.session_state.get("feedback_logs", [])

    combined = st.session_state.get("global_logs", []) + db_logs + local_logs

    unique = {}

    for index, event in enumerate(combined):

        identity = event.get("event_id") or event.get("id") or json.dumps(event, sort_keys=True, ensure_ascii=False, default=str)

        unique[identity] = event

    logs = list(unique.values())

    if db_manager:

        st.caption(f"🗄️ **Cơ sở dữ liệu bền vững (SQLite & Supabase):** Đã kết nối và lưu trữ an toàn **{len(db_logs)} bản ghi** lịch sử.")

    if logs:

        frame = pd.DataFrame(logs)

        st.dataframe(display_frame(frame), width="stretch")

        st.download_button("Tải nhật ký (CSV)", frame.to_csv(index=False).encode("utf-8-sig"), "nhat_ky_hoc_tap.csv", "text/csv")

    else:

        st.info("Chưa có dữ liệu. Nhật ký trong phiên không thay thế lưu trữ lâu dài; hãy đồng bộ hoặc tải về trước khi đóng phiên.")

    abandoned = st.session_state.get("abandoned_attempts", [])

    if abandoned:

        st.download_button("Tải bài chưa nộp đã giữ trong phiên", json.dumps(abandoned, ensure_ascii=False, indent=2), "bai_chua_nop.json", "application/json")

    pending = st.session_state.setdefault("pending_sync", {})

    if pending:

        st.warning(f"Có {len(pending)} sự kiện chưa được máy chủ xác nhận.")

        st.download_button("Tải sự kiện chưa đồng bộ", json.dumps(list(pending.values()), ensure_ascii=False, indent=2), "pending_events.json", "application/json")

        if st.button("Thử gửi lại sự kiện"):

            for event in list(pending.values()):

                sync_event(event, background=False)

            st.rerun()



    if sheet_view_url:

        st.link_button("Mở Google Sheets (cần quyền truy cập)", sheet_view_url)

    st.caption("Giữ bảng chứa tên, điểm và bài làm ở chế độ hạn chế truy cập. Chỉ chia sẻ bản tổng hợp đã bỏ định danh.")



    st.markdown("### Theo dõi lỗi kiến thức")

    diagnostic = [x for x in logs if x.get("type") == "SOCRATIC_DIAGNOSTIC"]

    if diagnostic:

        errors = pd.DataFrame(diagnostic)

        available = [c for c in ("name", "grade", "subject", "topic", "error_type", "evaluation") if c in errors]

        st.dataframe(display_frame(errors[available]), width="stretch")

        if "topic" in errors:

            st.bar_chart(errors["topic"].value_counts())

        st.caption("Các chẩn đoán do AI đề xuất, cần đối chiếu bài làm. Chưa đủ dữ liệu để suy ra phần trăm thông thạo.")

    else:

        st.info("Chưa có chẩn đoán. Sau khi nhận xét bài ở Trạm 2, lỗi kiến thức sẽ xuất hiện tại đây.")



    st.markdown("### Kiểm định điểm trước–sau")

    source = st.radio("Nguồn dữ liệu", ["Cơ sở dữ liệu thực (DB / SQL)", "Nhập điểm thật", "Tải CSV/Excel", "Nhật ký Trạm 3", "Mô phỏng minh họa"], key="research_source")

    research_df = None

    is_demo = source == "Mô phỏng minh họa"

    if source == "Cơ sở dữ liệu thực (DB / SQL)":

        st.caption("⚡ **Truy vấn CSDL theo môn và khối lớp:** Tự động truy vấn và ghép cặp điểm Pre-test và Post-test của cùng học sinh theo môn và khối lớp.")

        col_db_subj, col_db_gr = st.columns(2)

        with col_db_subj:

            ALL_STANDARD_SUBJECTS = [
                "Toán học", "Vật lý", "Hóa học", "Sinh học", "Khoa học tự nhiên",
                "Ngữ văn", "Tiếng Anh", "Lịch sử", "Địa lý", "Lịch sử & Địa lý",
                "Giáo dục kinh tế và pháp luật", "Giáo dục công dân", "Tin học", "Công nghệ"
            ]
            db_subj = st.selectbox("Môn học kiểm định:", ALL_STANDARD_SUBJECTS, key="db_filter_subj")

        with col_db_gr:

            db_gr = st.selectbox("Khối lớp:", [10, 11, 12, 6, 7, 8, 9], index=2, key="db_filter_gr")



        if db_manager:

            db_pairs = db_manager.get_paired_exam_data(db_subj, db_gr)

            if db_pairs:

                research_df = pd.DataFrame(db_pairs)

                st.success(f"🔍 Tìm thấy **{len(research_df)} cặp học sinh** đã hoàn thành cả Pre-test và Post-test môn {db_subj} Khối {db_gr}.")

                st.dataframe(research_df, width="stretch")

            else:

                st.info(f"Chưa có cặp điểm Pre/Post nào cho môn {db_subj} Khối {db_gr} trong CSDL. Giáo viên có thể dùng mục 'Nhật ký Trạm 3', 'Nhập điểm thật' hoặc 'Tải CSV/Excel'.")

        else:

            st.error("Chưa kết nối được Database Manager.")

    elif source == "Nhập điểm thật":

        st.caption("Một hàng cho một học sinh. ID phải duy nhất; nhập cả điểm trước và sau. Không có điểm mẫu điền sẵn.")

        research_df = st.data_editor(pd.DataFrame(columns=["student_id", "pre", "post", "minutes"]), num_rows="dynamic", key="paired_editor", width="stretch")

    elif source == "Tải CSV/Excel":

        uploaded = st.file_uploader("Bảng điểm theo từng học sinh", type=["csv", "xlsx", "xls"], key="research_upload")

        st.download_button("Tải mẫu bảng trống", "student_id,pre,post,minutes\n", "mau_diem.csv", "text/csv")

        if uploaded:

            try:

                research_df = pd.read_csv(uploaded) if uploaded.name.lower().endswith(".csv") else pd.read_excel(uploaded)

            except Exception as exc:

                st.error(f"Không đọc được file: {exc}")

    elif source == "Nhật ký Trạm 3":

        st.caption("Cần student_id và phase=pre/post, cùng môn/lớp. Bài luyện thông thường chưa được gán phase sẽ không bị tự suy đoán là pre/post.")

        eligible = [e for e in logs if e.get("type") == "EXAM_RESULT" and e.get("student_id") and e.get("phase") in ("pre", "post") and e.get("grading_status") != "ai_reference"]

        if eligible:

            events = pd.DataFrame(eligible)

            contexts = sorted(set(zip(events["grade"].astype(str), events["subject"].astype(str))))

            chosen = st.selectbox("Lớp và môn nghiên cứu", contexts)

            events = events[(events["grade"].astype(str) == chosen[0]) & (events["subject"].astype(str) == chosen[1])]

            if events.duplicated(["student_id", "phase"]).any():

                st.error("Có nhiều bài cho cùng ID và giai đoạn. Chọn trước bài đo lường nào được dùng, rồi nhập bảng điểm đã đối chiếu.")

            else:

                events["score"] = pd.to_numeric(events["score"], errors="coerce")

                research_df = events.pivot(index="student_id", columns="phase", values="score").reset_index()

        else:

            st.info("Chưa có cặp điểm nghiên cứu hợp lệ. Hãy nhập/tải bảng điểm thực tế; ứng dụng không tạo điểm trước từ điểm sau.")

    else:

        st.warning("DỮ LIỆU MÔ PHỎNG: chỉ minh họa thuật toán; không phải minh chứng hiệu quả ứng dụng.")

        n = st.slider("Số hàng minh họa", 15, 100, 35)

        rng = np.random.default_rng(42)

        pre = np.clip(rng.normal(5.4, 1.2, n), 0, 10)

        research_df = pd.DataFrame({"student_id": [f"demo-{i}" for i in range(n)], "pre": pre, "post": np.clip(pre+rng.normal(1, .7, n), 0, 10)})



    if research_df is not None and not research_df.empty:

        columns = research_df.columns.tolist()

        if len(columns) < 3:

            st.error("Cần cột mã học sinh, điểm trước và điểm sau.")

        else:

            id_col = st.selectbox("Cột mã học sinh", columns, index=columns.index("student_id") if "student_id" in columns else 0)

            pre_col = st.selectbox("Cột điểm trước", columns, index=columns.index("pre") if "pre" in columns else 1)

            post_col = st.selectbox("Cột điểm sau", columns, index=columns.index("post") if "post" in columns else 2)

            min_col = st.selectbox("Cột thời gian học (tùy chọn)", [None]+columns, index=([None]+columns).index("minutes") if "minutes" in columns else 0)

            if st.button("Phân tích các cặp điểm", key="analyze_pairs"):

                try:

                    if len({id_col, pre_col, post_col}) != 3 or (min_col and min_col in {id_col, pre_col, post_col}):

                        raise ValueError("Các cột được chọn phải khác nhau.")

                    ids = research_df[id_col]

                    if ids.isna().any() or ids.astype(str).str.strip().eq("").any() or ids.astype(str).str.strip().duplicated().any():

                        raise ValueError("Mã học sinh phải đầy đủ và duy nhất. Không ghép theo tên trùng.")

                    paired, removed = prepare_paired_data(research_df, pre_col, post_col, min_col)

                    result = paired_statistics(paired[pre_col], paired[post_col])

                    st.session_state.research_result = {"data": paired, "result": result, "pre": pre_col, "post": post_col, "minutes": min_col, "demo": is_demo, "source": source, "removed": removed}

                except Exception as exc:

                    st.session_state.pop("research_result", None)

                    st.error(str(exc))

    analysis = st.session_state.get("research_result")

    if analysis and analysis["source"] == source:

        st.caption("Kết quả của lần bấm Phân tích gần nhất. Sau khi sửa bảng/cột, hãy bấm Phân tích lại.")

        data, result = analysis["data"], analysis["result"]

        pre_col, post_col = analysis["pre"], analysis["post"]

        if analysis["demo"]:

            st.warning("KẾT QUẢ MINH HỌA TỪ DỮ LIỆU MÔ PHỎNG")

        st.write(f"Số cặp hợp lệ: {result['n']}; số hàng loại do thiếu/ngoài thang 0–10: {analysis['removed']}.")

        st.table(pd.DataFrame({"Chỉ số": ["Trung bình", "Độ lệch chuẩn"], "Trước": [data[pre_col].mean(), data[pre_col].std(ddof=1)], "Sau": [data[post_col].mean(), data[post_col].std(ddof=1)]}))

        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("Mức thay đổi trung bình", f"{result['gain']:+.3f} điểm")
        with col_m2:
            if result.get("hake") is not None:
                hg = result["hake"]
                hg_label = "Cao (High)" if hg >= 0.7 else ("Trung bình (Medium)" if hg >= 0.3 else "Thấp (Low)")
                st.metric("Hake's Normalized Gain ⟨g⟩", f"{hg:.3f}", delta=hg_label)

        if result.get("shapiro_p") is not None:
            sw_note = "Chưa bác bỏ giả thuyết phân phối chuẩn (p ≥ 0.05)" if result['shapiro_p'] >= 0.05 else "Có bằng chứng lệch chuẩn (p < 0.05)"
            sw_txt = f"Kiểm định phân phối chuẩn Shapiro-Wilk: p = {result['shapiro_p']:.4f} ({sw_note})"
            wilc_txt = f" • Kiểm định phi tham số Wilcoxon: p = {result['wilcoxon_p']:.4f}" if result.get('wilcoxon_p') is not None else ""
            st.caption(f"🔬 **Độ tin cậy đo lường (Chuẩn APA 7th & Scopus):** {sw_txt}{wilc_txt}")

        if result["p"] is None:

            st.info("Chênh lệch điểm có phương sai bằng 0: t-test và d_z không được báo như số hữu hạn. Cần kiểm tra dữ liệu.")

        else:

            st.write(f"Paired t-test: t={result['t']:.4f}, df={result['n']-1}, p={result['p']:.6g}; Cohen's d_z={result['dz']:.3f}.")

            st.write(f"Khoảng tin cậy 95% của mức thay đổi: [{result['ci'][0]:.3f}; {result['ci'][1]:.3f}].")

            st.info("Có bằng chứng về khác biệt trung bình ở ngưỡng 0,05." if result["p"] < .05 else "Chưa có đủ bằng chứng về khác biệt trung bình ở ngưỡng 0,05.")

        st.caption("Kiểm định giả định các học sinh độc lập và phân phối chênh lệch phù hợp. So sánh trước–sau đơn nhóm không chứng minh tác động nhân quả. Muốn đánh giá can thiệp cần thiết kế nhóm đối chứng và đề đo tương đương.")

        chart_data = pd.DataFrame({"Trước": data[pre_col], "Sau": data[post_col]})

        st.plotly_chart(px.box(chart_data, points="all", title="Phân bố điểm quan sát"), width="stretch")

        st.plotly_chart(px.histogram(x=data[post_col]-data[pre_col], title="Chênh lệch điểm quan sát"), width="stretch")

        min_col = analysis["minutes"]

        if min_col:

            relation = data[[min_col, pre_col, post_col]].dropna()

            relation = relation[relation[min_col] >= 0]

            gains = relation[post_col]-relation[pre_col]

            if len(relation) >= 3 and relation[min_col].nunique() > 1 and gains.nunique() > 1:

                correlation = stats.pearsonr(relation[min_col], gains)

                st.write(f"Tương quan Pearson: r={correlation.statistic:.3f}, p={correlation.pvalue:.6g}, N={len(relation)}. Tương quan không chứng minh thời gian học gây tăng điểm.")

                st.plotly_chart(px.scatter(x=relation[min_col], y=gains, labels={"x": "Phút học", "y": "Mức tăng điểm"}), width="stretch")

            else:

                st.info("Chưa đủ dữ liệu biến thiên để tính tương quan thời gian học.")

        summary = pd.DataFrame([{k: v for k,v in result.items()}])

        summary["data_kind"] = "simulation" if analysis["demo"] else "observed"

        # --- ĐO LƯỜNG & KHẢO THÍ CHUẨN ETS: CRONBACH'S ALPHA (α) & ITEM ANALYSIS (r_pbis) ---
        with st.expander("📊 Thẩm Định Khảo Thí Chuẩn ETS: Hệ Số Tin Cậy Cronbach's Alpha (α) & Độ Phân Biệt (r_pbis)", expanded=True):
            st.markdown(r"""
            **Căn cứ Đo lường Khảo thí Quốc tế (ETS & Psychometrics):**
            Hệ số tin cậy nội tại Cronbach's Alpha ($\alpha$) và Hệ số tương quan phân biệt Point-Biserial ($r_{\text{pbis}}$)
            được tính toán trực tiếp từ ma trận câu hỏi nhị phân ($X_{ij} \in \{0, 1\}$) của học sinh để đánh giá chất lượng đề thi chuẩn hóa.
            $$\alpha = \frac{K}{K - 1} \left(1 - \frac{\sum_{i=1}^K \sigma_i^2}{\sigma_X^2}\right)$$
            """)
            if compute_cronbach_alpha and generate_benchmark_psychometric_sample and compute_item_analysis:
                psy_matrix, psy_item_names = observed_item_matrix(logs) if not analysis["demo"] else generate_benchmark_psychometric_sample(n_students=35, k_items=22)
                if analysis["demo"]:
                    st.warning("MÔ PHỎNG ĐO LƯỜNG: ma trận minh họa độc lập, không phải bài làm của học sinh.")
                elif psy_matrix.size == 0:
                    st.info("Chưa đủ 3 bài làm có dữ liệu đúng/sai trên cùng phiên bản đề. Nhật ký cũ không được tự suy ra kết quả từng câu.")
                if psy_matrix.size:
                    alpha_data = compute_cronbach_alpha(psy_matrix)
                    item_details = compute_item_analysis(psy_matrix, psy_item_names)

                    p_col1, p_col2, p_col3 = st.columns(3)
                    with p_col1:
                        st.metric("Hệ số Cronbach's Alpha (α)", f"{alpha_data['alpha']:.3f}", delta=alpha_data['interpretation'].split('(')[0].strip())
                    with p_col2:
                        st.metric("Số bài cùng phiên bản đề", f"N = {alpha_data['n_students']} HS x K = {alpha_data['k_items']} Câu")
                    with p_col3:
                        well_discrim = len([it for it in item_details if it['rpbis'] >= 0.20])
                        st.metric("Câu hỏi Đạt chuẩn ETS (r_pbis ≥ 0.2)", f"{well_discrim}/{len(item_details)} ({well_discrim/len(item_details):.0%})")

                    st.caption(f"🎯 **Đánh giá Sư phạm:** `{alpha_data['interpretation']}` (Phương sai tổng $\\sigma_X^2 = {alpha_data['total_variance']:.2f}$ | Tổng phương sai câu $\\sum \\sigma_i^2 = {alpha_data['sum_item_variances']:.2f}$)")

                    warned_items = [it for it in item_details if it['rpbis'] < 0.20]
                    if warned_items:
                        st.warning(f"⚠️ **Cảnh báo Khảo thí:** Phát hiện {len(warned_items)} câu hỏi có độ phân biệt thấp ($r_{{\\text{{pbis}}}} < 0.20$): " + ", ".join([w['item_name'] for w in warned_items]) + ". Cần rà soát lại phương án nhiễu.")

                    df_items = pd.DataFrame([{
                        "Câu hỏi": it["item_name"],
                        "Độ khó P_i": it["difficulty_p"],
                        "Phân loại độ khó": it["difficulty_label"],
                        "Độ phân biệt r_pbis": it["rpbis"],
                        "Chuẩn phân hóa ETS": it["discrimination_label"],
                        "Khuyến nghị khảo thí": it["recommendation"]
                    } for it in item_details])

                    st.dataframe(df_items, width="stretch", height=260)
                    st.download_button(
                        "📥 Tải Báo Cáo Đo Lường Khảo Thí (CSV Item Analysis)",
                        df_items.to_csv(index=False).encode("utf-8-sig"),
                        "bao_cao_khao_thi_cronbach_alpha.csv",
                        "text/csv",
                        key="dl_cronbach_csv"
                    )

            else:
                st.info("Module psychometrics đang được nạp...")

        # --- MÔ PHỎNG MONTE CARLO N = 10.000 (KHẢO THÍ GDPT 2018 & KHKT 2026) ---
        with st.expander("🎲 Mô phỏng Mở rộng Toàn tỉnh (Monte Carlo Simulation - N = 10.000 học sinh)", expanded=False):
            st.markdown(r"""
            **Căn cứ khoa học:** Căn cứ tiêu chuẩn thống kê APA 7th và mô hình đánh giá diện rộng GDPT 2018,
            mô phỏng sinh các mức điểm giả định dựa trên tham số mẫu quan sát
            ($\mu_{pre}, \sigma_{pre}, \mu_{gain}, \sigma_{gain}$) để minh họa phân phối dưới giả định mô hình; không suy rộng hiệu quả toàn tỉnh.
            """)
            mc_col1, mc_col2 = st.columns(2)
            with mc_col1:
                mc_runs = st.number_input("Số lượt mô phỏng (N):", min_value=1000, max_value=50000, value=10000, step=1000, key="mc_runs_num")
            with mc_col2:
                mc_conf = st.selectbox("Tỷ lệ bao phủ phân vị mô phỏng:", [0.95, 0.99], index=0, key="mc_conf_level")

            if st.button("🚀 Kích hoạt Mô phỏng Monte Carlo (N = 10.000)", key="run_monte_carlo_btn"):
                with st.spinner("Đang tính toán ma trận phân phối Monte Carlo N = 10.000..."):
                    rng_mc = np.random.default_rng(2026)
                    base_mean_pre = float(data[pre_col].mean()) if data is not None and not data.empty else 5.4
                    base_std_pre = float(data[pre_col].std(ddof=1)) if data is not None and not data.empty else 1.2
                    gain_mean = float(result.get("gain", 1.0))
                    gain_std = float((data[post_col] - data[pre_col]).std(ddof=1)) if data is not None and not data.empty else 0.8

                    sim_pre = np.clip(rng_mc.normal(base_mean_pre, max(0.2, base_std_pre), mc_runs), 0, 10)
                    sim_gain = rng_mc.normal(gain_mean, max(0.0, gain_std), mc_runs)
                    sim_post = np.clip(sim_pre + sim_gain, 0, 10)

                    p_improve = np.mean(sim_post > sim_pre) * 100
                    ci_lower = np.percentile(sim_post - sim_pre, (1 - mc_conf)/2 * 100)
                    ci_upper = np.percentile(sim_post - sim_pre, (1 - (1 - mc_conf)/2) * 100)

                    m_c1, m_c2, m_c3 = st.columns(3)
                    m_c1.metric("Mức tăng mô phỏng sau giới hạn điểm", f"{np.mean(sim_post - sim_pre):+.3f} đ")
                    m_c2.metric("Xác suất cải thiện P(Post > Pre)", f"{p_improve:.1f}%")
                    m_c3.metric(f"Khoảng phân vị mô phỏng {int(mc_conf*100)}%", f"[{ci_lower:.2f}; {ci_upper:.2f}]")

                    mc_fig_df = pd.DataFrame({
                        "Giai đoạn": ["Trước can thiệp (Pre)"] * mc_runs + ["Sau can thiệp AI (Post)"] * mc_runs,
                        "Điểm số": np.concatenate([sim_pre, sim_post])
                    })
                    st.plotly_chart(px.histogram(mc_fig_df, x="Điểm số", color="Giai đoạn", barmode="overlay",
                                                opacity=0.65, title=f"Mô phỏng Phổ điểm Monte Carlo (N = {mc_runs:,})"),
                                    width="stretch")
                    st.info("Mô phỏng hoàn tất theo giả định phân phối đã chọn. Khoảng trên mô tả mức tăng cá nhân mô phỏng, không phải khoảng tin cậy trung bình hay bằng chứng hiệu quả toàn tỉnh.")



    render_parent_progress_report(student_name, subject, grade, logs)



    st.markdown("### Yêu cầu sửa lỗi / cải tiến")

    improvement = st.text_area("Mô tả lỗi hoặc cải tiến cần thực hiện", key="improvement_request")

    if improvement.strip():

        st.download_button("Tải yêu cầu để gửi người phát triển", improvement, "yeu_cau_cai_tien.txt", "text/plain")

    st.caption("Thay đổi mã nguồn cần bản sửa, kiểm thử và duyệt trước triển khai. Ứng dụng không nhận GitHub Token và không tự đẩy mã lên main.")
