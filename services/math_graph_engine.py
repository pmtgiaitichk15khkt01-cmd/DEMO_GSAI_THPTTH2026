# VIP 76.0 - HỆ THỐNG GIA SƯ AI THPT 2026 (CHUẨN GDPT 2018)
# -*- coding: utf-8 -*-
"""
DỊCH VỤ XUẤT ẢNH WEBP ĐỒ THỊ & BẢNG BIẾN THIÊN (BBT) CHUẨN SƯ PHẠM BỘ GD&ĐT
Tách độc lập từ app.py để giảm tải và tăng tốc độ khởi chạy ứng dụng.
"""
import io
import base64
import re
import json
import math
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

try:
    import precision_visual_engine as pve
except ImportError:
    pve = None

@st.cache_data(show_spinner=False, max_entries=512)
def render_bbt_to_webp_base64(raw_bbt: str) -> str:

    """Mã hóa Bảng biến thiên thành ảnh WebP chuẩn sư phạm Bộ GD&ĐT.

    Bao phủ 4 dạng: Bảng xét dấu 2 hàng, Phân thức 1/1, Phân thức 2/1 và Hàm liên tục trên R (Bậc 3)."""

    try:
        try:
            import precision_visual_engine as pve
            raw_bbt = pve.heal_bbt_mathematics(raw_bbt)
        except Exception:
            pass
        raw_str = str(raw_bbt).strip()
        raw_str = re.sub(r'\\+nearrow\b|\\nearrow', '↗', raw_str)
        raw_str = re.sub(r'\\+searrow\b|\\searrow', '↘', raw_str)
        raw_str = raw_str.replace('>>', '↗').replace('>', '↗')
        raw_str = re.sub(r'\\n(?!earrow)', '\n', raw_str)
        lines = [l.strip() for l in raw_str.split('\n') if l.strip() and '---' not in l]
        if len(lines) < 2: return ""

        def clean_token(v):
            s = str(v).replace('$', '').strip()
            s = s.replace(r'+\infty', '+∞').replace(r'-\infty', '-∞').replace(r'\infty', '∞')
            s = s.replace('+inf', '+∞').replace('-inf', '-∞').replace('inf', '∞')
            s = re.sub(r'\\+(?:nearrow|searrow)', '', s).replace('↗', '').replace('↘', '').strip()
            s = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', r'\1/\2', s)
            return s



        row_x_parts = [clean_token(p) for p in lines[0].split('|') if clean_token(p)]

        cells_x = row_x_parts[1:] if len(row_x_parts) > 1 else []

        M = len(cells_x)

        if M < 2: return ""



        # -------------------------------------------------------------

        # DẠNG 1: BẢNG XÉT DẤU ĐẠO HÀM (2 HÀNG: x và y')

        # -------------------------------------------------------------

        if len(lines) == 2:

            N = (M - 1) * 2 + 1

            col_w_header = 0.95

            col_w_slot = 1.05

            total_w = col_w_header + N * col_w_slot

            fig, ax = plt.subplots(figsize=(total_w, 1.6), dpi=140)

            ax.axis('off')

            fig.patch.set_facecolor('#ffffff')

            ax.set_facecolor('#ffffff')

            y_top_b = 2.0; y_div_x = 1.0

            ax.plot([0, total_w, total_w, 0, 0], [0, 0, y_top_b, y_top_b, 0], color='black', lw=1.2)

            ax.plot([0, total_w], [y_div_x, y_div_x], color='black', lw=1.0)

            ax.plot([col_w_header, col_w_header], [0, y_top_b], color='black', lw=1.2)

            ax.text(col_w_header/2, 1.5, r'$x$', ha='center', va='center', fontsize=12, fontweight='bold')

            ax.text(col_w_header/2, 0.5, r"$y'$", ha='center', va='center', fontsize=12, fontweight='bold')

            slot_x = [col_w_header + (i + 0.5) * col_w_slot for i in range(N)]

            for k, vx in enumerate(cells_x):
                ax.text(slot_x[2 * k], 1.5, vx, ha='center', va='center', fontsize=11)

            # Phân tách chính xác dấu (+, -) và nghiệm (0, ||) trong bảng xét dấu
            raw_yp_str = lines[1].split('|', 1)[-1] if '|' in lines[1] else lines[1]
            clean_signs = re.findall(r'[+-]', raw_yp_str)
            # Điền các dấu vào các khoảng giữa (cột lẻ 1, 3, 5, ... 2*k+1)
            for k in range(min(M - 1, len(clean_signs))):
                ax.text(slot_x[2 * k + 1], 0.5, clean_signs[k], ha='center', va='center', fontsize=13, fontweight='bold')
            # Điền số 0 (hoặc ||) ngay dưới các nghiệm x_k ở giữa (cột chẵn 2, 4, ... 2*k)
            for k in range(1, M - 1):
                xc_k = slot_x[2 * k]
                if '||' in lines[1]:
                    ax.plot([xc_k - 0.04, xc_k - 0.04], [0, y_div_x], color='black', lw=1.2)
                    ax.plot([xc_k + 0.04, xc_k + 0.04], [0, y_div_x], color='black', lw=1.2)
                else:
                    ax.text(xc_k, 0.5, '0', ha='center', va='center', fontsize=12)

            ax.set_xlim(-0.05, total_w + 0.05)

            ax.set_ylim(-0.05, y_top_b + 0.05)

            buf = io.BytesIO()

            plt.savefig(buf, format='webp', bbox_inches='tight', pad_inches=0.03, facecolor='#ffffff')

            plt.close(fig)

            buf.seek(0)

            return f"data:image/webp;base64,{base64.b64encode(buf.read()).decode('utf-8')}"



        line_yp = lines[1]

        line_y = lines[2] if len(lines) >= 3 else ''

        has_double_bar_yp = ('||' in line_yp) or ('║' in line_yp)

        has_double_bar_y = ('||' in line_y) or ('║' in line_y)



        has_zero_in_yp = ('0' in line_yp)

        is_double_bar_at_end = (line_y.strip().endswith('||') or line_y.strip().endswith('║') or line_yp.strip().endswith('||') or line_yp.strip().endswith('║'))



        # -------------------------------------------------------------

        # DẠNG 2: HÀM PHÂN THỨC BẬC 1/1 CÓ TIỆM CẬN ĐỨNG (M = 3 mốc: -∞, x0, +∞ và x0 là tiệm cận)

        # -------------------------------------------------------------

        if M == 3 and (has_double_bar_yp or has_double_bar_y) and not has_zero_in_yp and not is_double_bar_at_end:

            fig_w, fig_h = 5.2, 2.35

            fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=140)

            ax.axis('off')

            fig.patch.set_facecolor('#ffffff')

            ax.set_facecolor('#ffffff')

            y_top_b = 3.3; y_div_x = 2.5; y_div_yp = 1.8

            col_w = [0.95, 0.95, 1.25, 0.70, 1.25, 0.95]

            total_w = sum(col_w)

            x_edges = [0]

            for w in col_w: x_edges.append(x_edges[-1] + w)

            x_centers = [(x_edges[i] + x_edges[i+1])/2 for i in range(len(col_w))]

            ax.plot([0, total_w, total_w, 0, 0], [0, 0, y_top_b, y_top_b, 0], color='black', lw=1.2)

            ax.plot([0, total_w], [y_div_x, y_div_x], color='black', lw=1.0)

            ax.plot([0, total_w], [y_div_yp, y_div_yp], color='black', lw=1.0)

            ax.plot([x_edges[1], x_edges[1]], [0, y_top_b], color='black', lw=1.2)

            ax.text(x_centers[0], 2.9, r'$x$', ha='center', va='center', fontsize=12, fontweight='bold')

            ax.text(x_centers[0], 2.15, r"$y'$", ha='center', va='center', fontsize=12, fontweight='bold')

            ax.text(x_centers[0], 0.9, r'$y$', ha='center', va='center', fontsize=12, fontweight='bold')

            ax.text(x_centers[1], 2.9, cells_x[0], ha='center', va='center', fontsize=11)

            ax.text(x_centers[3], 2.9, cells_x[1], ha='center', va='center', fontsize=11)

            ax.text(x_centers[5], 2.9, cells_x[2], ha='center', va='center', fontsize=11)



            xc = x_centers[3]

            ax.plot([xc - 0.04, xc - 0.04], [0, y_div_x], color='black', lw=1.2)

            ax.plot([xc + 0.04, xc + 0.04], [0, y_div_x], color='black', lw=1.2)



            clean_signs = re.findall(r'[+-]', line_yp.split('|', 1)[-1] if '|' in line_yp else line_yp)

            sgn_L = clean_signs[0] if clean_signs else '+'

            sgn_R = clean_signs[1] if len(clean_signs) > 1 else sgn_L

            ax.text(x_centers[2], 2.15, sgn_L, ha='center', va='center', fontsize=12)

            ax.text(x_centers[4], 2.15, sgn_R, ha='center', va='center', fontsize=12)



            parts_y = re.split(r'\|\||║', line_y)

            left_y_str = parts_y[0] if parts_y else ''

            right_y_str = parts_y[1] if len(parts_y) > 1 else ''



            def get_sub_tokens(s):

                s = re.sub(r'^[yY]\s*\|?', '', s)

                s = clean_token(s)

                return [t for t in re.findall(r'[+-]?\s*∞|[-+]?\d+(?:[.,/]\d+)?', s) if t]



            tokens_L = get_sub_tokens(left_y_str)

            tokens_R = get_sub_tokens(right_y_str)

            y_b, y_m, y_t = 0.35, 0.90, 1.45



            if sgn_L == '+':

                v_sL = tokens_L[0] if tokens_L else "2"

                v_eL = tokens_L[1] if len(tokens_L) > 1 else "+∞"

                y_s = y_m; y_e = y_t

                ax.text(x_centers[1], y_s, v_sL, ha='center', va='center', fontsize=11)

                ax.text(xc - 0.15, y_e, v_eL, ha='right', va='center', fontsize=11)

                ax.annotate('', xy=(xc - 0.35, y_e - 0.1), xytext=(x_centers[1] + 0.3, y_s + 0.1),

                            arrowprops=dict(arrowstyle="->", color='black', lw=1.5))

            else:

                v_sL = tokens_L[0] if tokens_L else "2"

                v_eL = tokens_L[1] if len(tokens_L) > 1 else "-∞"

                y_s = y_m; y_e = y_b

                ax.text(x_centers[1], y_s, v_sL, ha='center', va='center', fontsize=11)

                ax.text(xc - 0.15, y_e, v_eL, ha='right', va='center', fontsize=11)

                ax.annotate('', xy=(xc - 0.35, y_e + 0.1), xytext=(x_centers[1] + 0.3, y_s - 0.1),

                            arrowprops=dict(arrowstyle="->", color='black', lw=1.5))



            if sgn_R == '+':

                v_sR = tokens_R[0] if tokens_R else "-∞"

                v_eR = tokens_R[1] if len(tokens_R) > 1 else "2"

                y_s = y_b; y_e = y_m

                ax.text(xc + 0.15, y_s, v_sR, ha='left', va='center', fontsize=11)

                ax.text(x_centers[5], y_e, v_eR, ha='center', va='center', fontsize=11)

                ax.annotate('', xy=(x_centers[5] - 0.3, y_e - 0.1), xytext=(xc + 0.35, y_s + 0.1),

                            arrowprops=dict(arrowstyle="->", color='black', lw=1.5))

            else:

                v_sR = tokens_R[0] if tokens_R else "+∞"

                v_eR = tokens_R[1] if len(tokens_R) > 1 else "2"

                y_s = y_t; y_e = y_m

                ax.text(xc + 0.15, y_s, v_sR, ha='left', va='center', fontsize=11)

                ax.text(x_centers[5], y_e, v_eR, ha='center', va='center', fontsize=11)

                ax.annotate('', xy=(x_centers[5] - 0.3, y_e + 0.1), xytext=(xc + 0.35, y_s - 0.1),

                            arrowprops=dict(arrowstyle="->", color='black', lw=1.5))



            ax.set_xlim(-0.05, total_w + 0.05)

            ax.set_ylim(-0.05, y_top_b + 0.05)

            buf = io.BytesIO()

            plt.savefig(buf, format='webp', bbox_inches='tight', pad_inches=0.03, facecolor='#ffffff')

            plt.close(fig)

            buf.seek(0)

            return f"data:image/webp;base64,{base64.b64encode(buf.read()).decode('utf-8')}"



        # -------------------------------------------------------------

        # DẠNG 3: HÀM PHÂN THỨC BẬC 2/1 (M = 5 mốc: -∞, x1, x_tc, x2, +∞)

        # -------------------------------------------------------------

        elif M == 5 and (has_double_bar_yp or has_double_bar_y or any(w in line_yp for w in ['||', '║'])):

            col_w_header = 0.95

            col_w_slot = 0.85

            N = 9

            fig_w = col_w_header + N * col_w_slot

            fig_h = 2.45

            fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=140)

            ax.axis('off')

            fig.patch.set_facecolor('#ffffff')

            ax.set_facecolor('#ffffff')



            y_top_b = 3.3; y_div_x = 2.5; y_div_yp = 1.8

            total_w = col_w_header + N * col_w_slot

            x_header_end = col_w_header



            ax.plot([0, total_w, total_w, 0, 0], [0, 0, y_top_b, y_top_b, 0], color='black', lw=1.2)

            ax.plot([0, total_w], [y_div_x, y_div_x], color='black', lw=1.0)

            ax.plot([0, total_w], [y_div_yp, y_div_yp], color='black', lw=1.0)

            ax.plot([x_header_end, x_header_end], [0, y_top_b], color='black', lw=1.2)



            ax.text(x_header_end/2, 2.9, r'$x$', ha='center', va='center', fontsize=12, fontweight='bold')

            ax.text(x_header_end/2, 2.15, r"$y'$", ha='center', va='center', fontsize=12, fontweight='bold')

            ax.text(x_header_end/2, 0.9, r'$y$', ha='center', va='center', fontsize=12, fontweight='bold')



            slot_x = [x_header_end + (i + 0.5) * col_w_slot for i in range(N)]



            # Hàng x: đặt tại các mốc chẵn 0, 2, 4, 6, 8

            for k in range(5):

                ax.text(slot_x[2 * k], 2.9, cells_x[k], ha='center', va='center', fontsize=11)



            # VẠCH ĐÔI TIỆM CẬN ĐỨNG: Nằm chính xác tại slot_x[4] (mốc thứ 3 cells_x[2])

            xc = slot_x[4]

            ax.plot([xc - 0.04, xc - 0.04], [0, y_div_x], color='black', lw=1.2)

            ax.plot([xc + 0.04, xc + 0.04], [0, y_div_x], color='black', lw=1.2)



            # Hàng y': Hai điểm cực trị có số 0

            ax.text(slot_x[2], 2.15, '0', ha='center', va='center', fontsize=12)

            ax.text(slot_x[6], 2.15, '0', ha='center', va='center', fontsize=12)



            # 4 dấu đạo hàm tại slot 1, 3, 5, 7

            clean_signs = re.findall(r'[+-]', line_yp.split('|', 1)[-1] if '|' in line_yp else line_yp)

            s1 = clean_signs[0] if len(clean_signs) > 0 else '+'

            s2 = clean_signs[1] if len(clean_signs) > 1 else '-'

            s3 = clean_signs[2] if len(clean_signs) > 2 else '-'

            s4 = clean_signs[3] if len(clean_signs) > 3 else '+'

            ax.text(slot_x[1], 2.15, s1, ha='center', va='center', fontsize=12)

            ax.text(slot_x[3], 2.15, s2, ha='center', va='center', fontsize=12)

            ax.text(slot_x[5], 2.15, s3, ha='center', va='center', fontsize=12)

            ax.text(slot_x[7], 2.15, s4, ha='center', va='center', fontsize=12)



            # Hàng y: Tách hai nhánh qua tiệm cận đứng

            parts_y = re.split(r'\|\||║', line_y)

            left_y_str = parts_y[0] if parts_y else ''

            right_y_str = parts_y[1] if len(parts_y) > 1 else ''



            tokens_L = [clean_token(t) for t in re.findall(r'[+-]?\s*∞|[-+]?\d+(?:[.,/]\d+)?', clean_token(left_y_str)) if t]

            tokens_R = [clean_token(t) for t in re.findall(r'[+-]?\s*∞|[-+]?\d+(?:[.,/]\d+)?', clean_token(right_y_str)) if t]



            # Dự phòng nếu dòng y không có vạch đôi mà chỉ có chuỗi liền

            if not tokens_R and len(tokens_L) >= 4:

                half = len(tokens_L) // 2

                tokens_R = tokens_L[half:]

                tokens_L = tokens_L[:half]



            nums_L = [t for t in tokens_L if '∞' not in t]

            y_L_val = nums_L[0] if nums_L else "-2"



            nums_R = [t for t in tokens_R if '∞' not in t]

            y_R_val = nums_R[0] if nums_R else "2"



            y_b, y_m, y_t = 0.35, 0.90, 1.45



            # Nhánh trái: vẽ theo dấu s1, s2

            if s1 == '+':

                ax.text(slot_x[0], y_b, r'$-\infty$', ha='center', va='center', fontsize=11)

                ax.text(slot_x[2], y_t, y_L_val, ha='center', va='center', fontsize=11, fontweight='500')

                ax.text(xc - 0.12, y_b, r'$-\infty$', ha='right', va='center', fontsize=11)

                ax.annotate('', xy=(slot_x[2] - 0.25, y_t - 0.1), xytext=(slot_x[0] + 0.25, y_b + 0.1),

                            arrowprops=dict(arrowstyle="->", color='black', lw=1.5))

                ax.annotate('', xy=(xc - 0.25, y_b + 0.1), xytext=(slot_x[2] + 0.25, y_t - 0.1),

                            arrowprops=dict(arrowstyle="->", color='black', lw=1.5))

            else:

                ax.text(slot_x[0], y_t, r'$+\infty$', ha='center', va='center', fontsize=11)

                ax.text(slot_x[2], y_b, y_L_val, ha='center', va='center', fontsize=11, fontweight='500')

                ax.text(xc - 0.12, y_t, r'$+\infty$', ha='right', va='center', fontsize=11)

                ax.annotate('', xy=(slot_x[2] - 0.25, y_b + 0.1), xytext=(slot_x[0] + 0.25, y_t - 0.1),

                            arrowprops=dict(arrowstyle="->", color='black', lw=1.5))

                ax.annotate('', xy=(xc - 0.25, y_t - 0.1), xytext=(slot_x[2] + 0.25, y_b + 0.1),

                            arrowprops=dict(arrowstyle="->", color='black', lw=1.5))



            # Nhánh phải: vẽ theo dấu s3, s4

            if s4 == '+':

                ax.text(xc + 0.12, y_t, r'$+\infty$', ha='left', va='center', fontsize=11)

                ax.text(slot_x[6], y_b, y_R_val, ha='center', va='center', fontsize=11, fontweight='500')

                ax.text(slot_x[8], y_t, r'$+\infty$', ha='center', va='center', fontsize=11)

                ax.annotate('', xy=(slot_x[6] - 0.25, y_b + 0.1), xytext=(xc + 0.25, y_t - 0.1),

                            arrowprops=dict(arrowstyle="->", color='black', lw=1.5))

                ax.annotate('', xy=(slot_x[8] - 0.25, y_t - 0.1), xytext=(slot_x[6] + 0.25, y_b + 0.1),

                            arrowprops=dict(arrowstyle="->", color='black', lw=1.5))

            else:

                ax.text(xc + 0.12, y_b, r'$-\infty$', ha='left', va='center', fontsize=11)

                ax.text(slot_x[6], y_t, y_R_val, ha='center', va='center', fontsize=11, fontweight='500')

                ax.text(slot_x[8], y_b, r'$-\infty$', ha='center', va='center', fontsize=11)

                ax.annotate('', xy=(slot_x[6] - 0.25, y_t - 0.1), xytext=(xc + 0.25, y_b + 0.1),

                            arrowprops=dict(arrowstyle="->", color='black', lw=1.5))

                ax.annotate('', xy=(slot_x[8] - 0.25, y_b + 0.1), xytext=(slot_x[6] + 0.25, y_t - 0.1),

                            arrowprops=dict(arrowstyle="->", color='black', lw=1.5))



            ax.set_xlim(-0.05, total_w + 0.05)

            ax.set_ylim(-0.05, y_top_b + 0.05)

            buf = io.BytesIO()

            plt.savefig(buf, format='webp', bbox_inches='tight', pad_inches=0.03, facecolor='#ffffff')

            plt.close(fig)

            buf.seek(0)

            return f"data:image/webp;base64,{base64.b64encode(buf.read()).decode('utf-8')}"



        # -------------------------------------------------------------

        # DẠNG 4: HÀM LIÊN TỤC TRÊN R (BẬC 3, BẬC 4, ĐA THỨC)

        # -------------------------------------------------------------

        else:

            N = (M - 1) * 2 + 1

            col_w_header = 0.95

            col_w_slot = 1.15

            fig_w = max(4.5, col_w_header + N * col_w_slot)

            fig_h = 2.40



            fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=140)

            ax.axis('off')

            fig.patch.set_facecolor('#ffffff')

            ax.set_facecolor('#ffffff')



            y_top_b = 3.3; y_div_x = 2.5; y_div_yp = 1.8

            total_w = col_w_header + N * col_w_slot

            x_header_end = col_w_header



            ax.plot([0, total_w, total_w, 0, 0], [0, 0, y_top_b, y_top_b, 0], color='black', lw=1.2)

            ax.plot([0, total_w], [y_div_x, y_div_x], color='black', lw=1.0)

            ax.plot([0, total_w], [y_div_yp, y_div_yp], color='black', lw=1.0)

            ax.plot([x_header_end, x_header_end], [0, y_top_b], color='black', lw=1.2)



            ax.text(x_header_end/2, 2.9, r'$x$', ha='center', va='center', fontsize=12, fontweight='bold')

            ax.text(x_header_end/2, 2.15, r"$y'$", ha='center', va='center', fontsize=12, fontweight='bold')

            ax.text(x_header_end/2, 0.9, r'$y$', ha='center', va='center', fontsize=12, fontweight='bold')



            slot_x = [x_header_end + (i + 0.5) * col_w_slot for i in range(N)]



            for k, vx in enumerate(cells_x):

                ax.text(slot_x[2 * k], 2.9, vx, ha='center', va='center', fontsize=11)



            clean_signs = re.findall(r'[+-]', line_yp.split('|', 1)[-1] if '|' in line_yp else line_yp)

            for k in range(min(M - 1, len(clean_signs))):

                ax.text(slot_x[2 * k + 1], 2.15, clean_signs[k], ha='center', va='center', fontsize=12)



            for k in range(1, M - 1):

                ax.text(slot_x[2 * k], 2.15, '0', ha='center', va='center', fontsize=12)



            # Vẽ vạch đôi nếu có || ở biên phải (ví dụ tại x = 7 của nửa khoảng [-5; 7))

            has_double_bar_end = (line_y.strip().endswith('||') or line_y.strip().endswith('║') or line_yp.strip().endswith('||') or line_yp.strip().endswith('║'))

            if has_double_bar_end:

                xc_r = slot_x[2 * (M - 1)]

                ax.plot([xc_r - 0.04, xc_r - 0.04], [0, y_div_x], color='black', lw=1.2)

                ax.plot([xc_r + 0.04, xc_r + 0.04], [0, y_div_x], color='black', lw=1.2)



            clean_y_str = clean_token(line_y)
            raw_y_cells = [clean_token(p) for p in line_y.split('|') if clean_token(p) and clean_token(p).lower() != 'y']
            raw_tokens = [t for t in re.findall(r'[+-]?\s*∞|[-+]?\d+(?:[.,/]\d+)?', clean_y_str) if t]

            # Kiểm tra trường hợp ký hiệu giải tích dạng chữ: y(x_1), y(x_2)
            has_symbolic_extrema = any(('y(' in c.lower() or 'f(' in c.lower() or 'y_' in c.lower() or 'cd' in c.lower() or 'ct' in c.lower()) for c in raw_y_cells)

            # Kiểm tra xem các giá trị cực trị có bị gán toàn số 0 giả mạo không:
            num_tokens = [t for t in raw_tokens if '∞' not in t]
            is_bogus_zeros = len(num_tokens) > 0 and all(abs(float(t.replace(',', '.'))) < 1e-4 for t in num_tokens)

            if has_symbolic_extrema:
                if clean_signs == ['+', '-', '+']:
                    clean_y_items = ['-∞', 'y(x₁)', 'y(x₂)', '+∞'][:M]
                elif clean_signs == ['-', '+', '-']:
                    clean_y_items = ['+∞', 'y(x₁)', 'y(x₂)', '-∞'][:M]
                else:
                    clean_y_items = ['-∞', 'y(x₁)', 'y(x₂)', '+∞'][:M]
            elif is_bogus_zeros or not raw_tokens:
                if clean_signs == ['+', '-', '+']:
                    clean_y_items = ['-∞', '1', '-2', '+∞'][:M]
                elif clean_signs == ['-', '+', '-']:
                    clean_y_items = ['+∞', '-2', '1', '-∞'][:M]
                elif clean_signs == ['-', '+', '-', '+']:
                    clean_y_items = ['+∞', '-2', '2', '-2', '+∞'][:M]
                elif clean_signs == ['+', '-', '+', '-']:
                    clean_y_items = ['-∞', '2', '-2', '2', '-∞'][:M]
                else:
                    clean_y_items = ['-∞', '1', '-2', '+∞'][:M]
            elif len(raw_tokens) < M:
                healed_items = list(raw_tokens)
                if not healed_items:
                    healed_items = ['-∞' if clean_signs and clean_signs[0] == '+' else '+∞']
                while len(healed_items) < M:
                    k_curr = len(healed_items) - 1
                    s_sign = clean_signs[k_curr] if k_curr < len(clean_signs) else '+'
                    if s_sign == '+':
                        prev_val = healed_items[-1]
                        if prev_val == '-∞': healed_items.append('-2' if clean_signs == ['+', '-', '+'] else '1')
                        elif '∞' in prev_val: healed_items.append('+∞')
                        else:
                            try: healed_items.append(str(int(float(prev_val)) + 2))
                            except Exception: healed_items.append('+∞')
                    else:
                        prev_val = healed_items[-1]
                        if prev_val == '+∞': healed_items.append('1' if clean_signs == ['-', '+', '-'] else '-2')
                        elif '∞' in prev_val: healed_items.append('-∞')
                        else:
                            try: healed_items.append(str(int(float(prev_val)) - 2))
                            except Exception: healed_items.append('-∞')
                clean_y_items = healed_items[:M]
            else:
                clean_y_items = raw_tokens[:M]



            y_b, y_t = 0.35, 1.45

            parsed_vals = []

            for item in clean_y_items:

                s = str(item).strip()

                if '+∞' in s: parsed_vals.append(('pos_inf', float('inf')))

                elif '-∞' in s: parsed_vals.append(('neg_inf', float('-inf')))

                else:

                    try:

                        clean_s = s.replace(',', '.').strip()
                        if '/' in clean_s:
                            num_part, den_part = clean_s.split('/', 1)
                            v = float(num_part.strip()) / float(den_part.strip())
                        else:
                            v = float(clean_s)

                        parsed_vals.append(('num', v))

                    except Exception:

                        parsed_vals.append(('num', 0.0))



            finite_sorted = sorted(list(set([p[1] for p in parsed_vals if p[0] == 'num'])))

            has_pos = any(p[0] == 'pos_inf' for p in parsed_vals)

            has_neg = any(p[0] == 'neg_inf' for p in parsed_vals)



            bound_low = y_b + (0.35 if has_neg else 0.10)

            bound_high = y_t - (0.35 if has_pos else 0.10)

            if bound_high <= bound_low:

                bound_low = y_b + 0.25

                bound_high = y_t - 0.25



            val_map = {}

            if len(finite_sorted) == 1:

                val_map[finite_sorted[0]] = (bound_low + bound_high) / 2

            elif len(finite_sorted) > 1:

                step_h = (bound_high - bound_low) / (len(finite_sorted) - 1)

                for idx_v, fv in enumerate(finite_sorted):

                    val_map[fv] = bound_low + idx_v * step_h



            y_levels = []

            for p in parsed_vals:

                if p[0] == 'pos_inf': y_levels.append(y_t)

                elif p[0] == 'neg_inf': y_levels.append(y_b)

                else: y_levels.append(val_map.get(p[1], (bound_low + bound_high) / 2))



            for k in range(min(M - 1, len(clean_signs))):

                sgn = clean_signs[k]

                if sgn == '+' and y_levels[k] >= y_levels[k+1]:

                    y_levels[k] = min(y_levels[k], y_levels[k+1] - 0.35)

                elif sgn == '-' and y_levels[k] <= y_levels[k+1]:

                    y_levels[k] = max(y_levels[k], y_levels[k+1] + 0.35)



            for k in range(M):

                offset_x = 0.18 if (k == M - 1 and has_double_bar_end) else 0.0

                ax.text(slot_x[2 * k] - offset_x, y_levels[k], clean_y_items[k], ha='center', va='center', fontsize=11, fontweight='500')



            for k in range(M - 1):

                sgn = clean_signs[k] if k < len(clean_signs) else ('+' if y_levels[k+1] > y_levels[k] else '-')

                is_up = (sgn == '+')

                # Đảm bảo mũi tên luôn có độ dốc chéo dứt khoát, chống lỗi bẹp ngang

                if is_up:

                    y_s = y_levels[k] + 0.08

                    y_e = max(y_s + 0.18, y_levels[k+1] - 0.08)

                else:

                    y_s = y_levels[k] - 0.08

                    y_e = min(y_s - 0.18, y_levels[k+1] + 0.08)

                ax.annotate('', xy=(slot_x[2*k + 2] - 0.25, y_e),

                            xytext=(slot_x[2*k] + 0.25, y_s),

                            arrowprops=dict(arrowstyle="->", color='black', lw=1.5))



            ax.set_xlim(-0.05, total_w + 0.05)

            ax.set_ylim(-0.05, y_top_b + 0.05)

            buf = io.BytesIO()

            plt.savefig(buf, format='webp', bbox_inches='tight', pad_inches=0.03, facecolor='#ffffff')

            plt.close(fig)

            buf.seek(0)

            return f"data:image/webp;base64,{base64.b64encode(buf.read()).decode('utf-8')}"



    except Exception:

        return ""

@st.cache_data(show_spinner=False, max_entries=512)
def render_math_graph_to_webp_base64(graph_data, extra_points=None, xlabel=r'$x$', ylabel=r'$y$') -> str:

    """Vẽ Đồ thị 2D chuẩn Bộ GD&ĐT (Đa môn STEM, bước nhảy động O(1), số bám sát trục Oxy, chống đè chữ)."""

    try:

        if isinstance(graph_data, str):

            try: graph_data = json.loads(graph_data)

            except Exception: return ""

        if not isinstance(graph_data, dict):

            return ""



        dtype = str(graph_data.get("type", ""))

        a = float(graph_data.get("a", 1.0))

        b = float(graph_data.get("b", 0.0))

        c = float(graph_data.get("c", 0.0))

        d = float(graph_data.get("d", 0.0))

        e = float(graph_data.get("e", 0.0))



        key_points = []

        asymptotes_v = []

        asymptotes_h = []

        slant_asymptote = None



        if dtype in ("func_3", "cubic"):

            def f(x): return a*x**3 + b*x**2 + c*x + d

            key_points.append((0.0, d, "y_int", False))

            if a != 0:

                xi = -b / (3.0 * a)

                key_points.append((xi, f(xi), "I", True))

                delta_p = b**2 - 3.0*a*c

                if delta_p > 1e-6:

                    x1 = (-b - math.sqrt(delta_p)) / (3.0 * a)

                    x2 = (-b + math.sqrt(delta_p)) / (3.0 * a)

                    key_points.append((x1, f(x1), "CĐ/CT", True))

                    key_points.append((x2, f(x2), "CĐ/CT", True))



        elif dtype in ("parabola", "parabola_fprime"):

            def f(x): return a*x**2 + b*x + c

            key_points.append((0.0, c, "y_int", False))

            if a != 0:

                xv = -b / (2.0 * a)

                key_points.append((xv, f(xv), "Đỉnh", True))



        elif dtype == "func_1_1":

            if c != 0:

                x_asymp = -d / c

                y_asymp = a / c

                asymptotes_v.append(x_asymp)

                asymptotes_h.append(y_asymp)

                key_points.append((x_asymp, y_asymp, "I", False))

                if d != 0: key_points.append((0.0, b / d, "y_int", False))

                if a != 0: key_points.append((-b / a, 0.0, "x_int", False))

            def f(x):

                denom = c*x + d

                denom = np.where(np.abs(denom) < 1e-5, np.nan, denom)

                return (a*x + b) / denom



        elif dtype == "func_2_1":

            if d != 0:

                x_asymp = -e / d

                asymptotes_v.append(x_asymp)

                m_slant = a / d

                n_slant = (b*d - a*e) / (d**2)

                slant_asymptote = (m_slant, n_slant)

                A_num, B_num, C_num = a*d, 2.0*a*e, b*e - c*d

                delta_num = B_num**2 - 4.0*A_num*C_num

                if delta_num > 1e-5 and A_num != 0:

                    x1 = (-B_num - math.sqrt(delta_num)) / (2.0*A_num)

                    x2 = (-B_num + math.sqrt(delta_num)) / (2.0*A_num)

                    denom1, denom2 = d*x1 + e, d*x2 + e

                    if abs(denom1) > 1e-4: key_points.append((x1, (a*x1**2 + b*x1 + c)/denom1, "CĐ/CT", True))

                    if abs(denom2) > 1e-4: key_points.append((x2, (a*x2**2 + b*x2 + c)/denom2, "CĐ/CT", True))

                if e != 0: key_points.append((0.0, c / e, "y_int", False))

            def f(x):

                denom = d*x + e

                denom = np.where(np.abs(denom) < 1e-5, np.nan, denom)

                return (a*x**2 + b*x + c) / denom

        else:

            return ""



        if extra_points:

            for ep in extra_points:

                try:

                    if isinstance(ep, (int, float)):

                        ep_x = float(ep)

                        key_points.append((ep_x, f(ep_x), "", True))

                except Exception: pass



        all_x = [0.0] + [p[0] for p in key_points if math.isfinite(p[0])] + asymptotes_v

        all_y = [0.0] + [p[1] for p in key_points if math.isfinite(p[1])] + asymptotes_h

        all_x = [x for x in all_x if abs(x) < 50]

        all_y = [y for y in all_y if abs(y) < 50]



        min_x, max_x = min(all_x), max(all_x)

        min_y, max_y = min(all_y), max(all_y)

        dx = max(1.8, (max_x - min_x) * 0.40)

        dy = max(1.8, (max_y - min_y) * 0.40)



        x_low = math.floor(min_x - dx)

        x_high = math.ceil(max_x + dx)

        y_low = math.floor(min_y - dy)

        y_high = math.ceil(max_y + dy)



        # THUẬT TOÁN NICE NUMBERS O(1): Phân bổ bước nhảy thích ứng theo độ lớn thực tế từ AI

        def get_adaptive_step(span: float) -> int:

            raw = max(1.0, span / 7.0)

            pow10 = 10 ** math.floor(math.log10(raw))

            ratio = raw / pow10

            return int((1 if ratio <= 1.5 else (2 if ratio <= 3.5 else (5 if ratio <= 7.5 else 10))) * pow10)



        step_x = get_adaptive_step(x_high - x_low)

        step_y = get_adaptive_step(y_high - y_low)



        # Khoảng đệm an toàn đầu trục chống đè chữ x, y

        pad_x = max(0.5, step_x * 0.45)

        pad_y = max(0.5, step_y * 0.45)



        fig, ax = plt.subplots(figsize=(3.8, 3.4), dpi=140)

        fig.patch.set_facecolor('#ffffff')

        ax.set_facecolor('#ffffff')



        ax.set_xlim(x_low - 0.2, x_high + pad_x + 0.2)

        ax.set_ylim(y_low - 0.2, y_high + pad_y + 0.2)



        # 1. Đưa trục tọa độ Ox, Oy về đúng tâm Zero (0, 0)

        ax.spines['left'].set_position('zero')

        ax.spines['bottom'].set_position('zero')

        ax.spines['right'].set_color('none')

        ax.spines['top'].set_color('none')

        ax.spines['left'].set_linewidth(1.1)

        ax.spines['bottom'].set_linewidth(1.1)



        # 2. Lưới tọa độ thanh mảnh chuẩn SGK

        ax.grid(True, linestyle='--', color='#e2e8f0', alpha=0.8, lw=0.7)



        # 3. Điền các con số nguyên NGAY TRÊN TRỤC Ox và Oy (ẩn số 0 ở gốc để không đè chữ O)

        ax.xaxis.set_major_locator(plt.MultipleLocator(step_x))

        ax.yaxis.set_major_locator(plt.MultipleLocator(step_y))

        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{int(v)}" if math.isclose(v, round(v), abs_tol=1e-4) and not math.isclose(v, 0, abs_tol=1e-4) and v <= x_high else ""))

        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{int(v)}" if math.isclose(v, round(v), abs_tol=1e-4) and not math.isclose(v, 0, abs_tol=1e-4) and v <= y_high else ""))

        ax.tick_params(axis='both', which='major', labelsize=9.5, pad=2)



        # 4. Mũi tên đầu trục Ox, Oy và nhãn trục (đặt tách rời hoàn toàn, không đè số tick)

        ax.plot(x_high + pad_x, 0, ">k", clip_on=False, markersize=5)

        ax.plot(0, y_high + pad_y, "^k", clip_on=False, markersize=5)

        ax.text(x_high + pad_x + 0.08, -0.35 * step_y, xlabel, fontsize=11, fontweight='bold', ha='left', va='center')

        ax.text(-0.35 * step_x, y_high + pad_y + 0.08, ylabel, fontsize=11, fontweight='bold', ha='center', va='bottom')

        ax.text(-0.25 * step_x, -0.30 * step_y, r'$O$', fontsize=10, style='italic', ha='right', va='top')



        # 5. Đường tiệm cận đứng, ngang, xiên (nếu có)

        for xv in asymptotes_v:

            ax.axvline(xv, color='#dc2626', linestyle='--', lw=1.0, alpha=0.85)

        for yh in asymptotes_h:

            ax.axhline(yh, color='#dc2626', linestyle='--', lw=1.0, alpha=0.85)

        if slant_asymptote:

            m_s, n_s = slant_asymptote

            xs = np.linspace(x_low, x_high, 100)

            ax.plot(xs, m_s*xs + n_s, color='#dc2626', linestyle='--', lw=1.0, alpha=0.85)



        # 6. Vẽ đường cong đồ thị (Vector hóa NumPy song song cực nhanh)

        if dtype in ("func_1_1", "func_2_1") and asymptotes_v:

            xv = asymptotes_v[0]

            x_l = np.linspace(x_low, xv - 0.04, 250)

            x_r = np.linspace(xv + 0.04, x_high, 250)

            for x_br in [x_l, x_r]:

                y_br = f(x_br)

                mask = np.isfinite(y_br) & (y_br >= y_low - 2) & (y_br <= y_high + 2)

                ax.plot(x_br[mask], y_br[mask], color='#1d4ed8', lw=1.8)

        else:

            x_vals = np.linspace(x_low, x_high, 400)

            y_vals = f(x_vals)

            mask = np.isfinite(y_vals) & (y_vals >= y_low - 2) & (y_vals <= y_high + 2)

            ax.plot(x_vals[mask], y_vals[mask], color='#1d4ed8', lw=1.8)



        # 7. Dóng nét đứt các điểm quan trọng (Tâm I, Cực trị) xuống Ox, Oy

        for px, py, label, should_dong in key_points:

            if not (x_low <= px <= x_high and y_low <= py <= y_high): continue

            ax.plot(px, py, 'o', color='#b91c1c' if label in ("CĐ/CT", "Đỉnh") else '#0f172a', markersize=3.5)



            if should_dong:

                if abs(py) > 0.15:

                    ax.plot([px, px], [0, py], color='#4b5563', linestyle=':', lw=0.9)

                if abs(px) > 0.15:

                    ax.plot([0, px], [py, py], color='#4b5563', linestyle=':', lw=0.9)



            if label == "I":

                ax.text(px + 0.12 * step_x, py + 0.12 * step_y, r'$I$', fontsize=10, fontweight='bold', color='#0f172a')



        buf = io.BytesIO()

        plt.savefig(buf, format='webp', bbox_inches='tight', pad_inches=0.03, transparent=False, facecolor='#ffffff')

        plt.close(fig)

        buf.seek(0)

        b64_data = base64.b64encode(buf.read()).decode('utf-8')

        return f"data:image/webp;base64,{b64_data}"

    except Exception:
        return ""

