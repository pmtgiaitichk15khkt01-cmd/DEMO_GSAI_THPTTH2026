# -*- coding: utf-8 -*-
"""
HỆ THỐNG QUY CHUẨN TIKZ VECTOR, BẢNG XÉT DẤU (BXD) VÀ ĐỒ THỊ CHUẨN SƯ PHẠM BỘ GD&ĐT
Dự án Nghiên cứu Khoa học Kỹ thuật 2026 - Tác giả Thầy Phạm Minh Trí.
Tương thích hoàn toàn với 3 tài liệu chuẩn:
- BẢNG_XÉT_DẤU.docx (tkz-tab)
- LATEX_ĐÁNH_DẤU_&_TÔ_MIỀN.docx (tkz-euclide, patterns)
- LATEX_ĐỒ_THỊ.docx (pgfplots, hàm bậc 2, bậc 3, trùng phương, nhất biến, 2/1, lũy thừa)
"""

SYSTEM_PROMPT_TIKZ_BBT_GRAPH_SPEC = r"""
[CHỈ THỊ CỐT LÕI VỀ BẢNG BIẾN THIÊN (BBT), BẢNG XÉT DẤU (BXD) VÀ ĐỒ THỊ TIKZ CHUẨN BỘ GD&ĐT]:
Khi câu hỏi hoặc bài giảng sinh Bảng xét dấu (BXD), Bảng biến thiên (BBT) hoặc Đồ thị TikZ, BẮT BUỘC tuân thủ 100% cú pháp mẫu sau:

1. BẢNG XÉT DẤU (BXD) DÙNG GÓI tkz-tab:
   - Cú pháp chuẩn 2 dòng (x và y'):
     \begin{tikzpicture}
         \tkzTabInit[nocadre, lgt=1.5, espcl=3]{$x$/0.7, $y'$/0.7}{$-\infty$, $x_1$, $x_2$, $+\infty$}
         \tkzTabLine{,+,0,-,0,+,}
     \end{tikzpicture}
   - Quy tắc dấu hàm bậc ba: Nếu a > 0 thì (+, 0, -, 0, +); nếu a < 0 thì (-, 0, +, 0, -).
   - Nếu có tiệm cận đứng tại x0 thì thay '0' bằng 'd' hoặc vạch đôi: \tkzTabLine{,+,,d,,+,}

2. BẢNG BIẾN THIÊN ĐẦY ĐỦ 3 DÒNG:
   - Cú pháp chuẩn:
     \begin{tikzpicture}
         \tkzTabInit[nocadre, lgt=1.5, espcl=2.5]{$x$/0.7, $y'$/0.7, $y$/2}{$-\infty$, $x_1$, $x_2$, $+\infty$}
         \tkzTabLine{,+,0,-,0,+,}
         \tkzTabVar{-/ $-\infty$, +/ $y_1$, -/ $y_2$, +/ $+\infty$}
     \end{tikzpicture}

3. ĐÁNH DẤU HÌNH HỌC & TÔ MIỀN:
   - Đánh dấu đoạn: \tkzMarkSegments[mark=||](A,B A,C)
   - Đánh dấu góc vuông: \tkzMarkRightAngles[size=0.17](A,B,C)
   - Đánh dấu góc tròn: \tkzMarkAngles[size=0.7cm,arc=ll,mark=|](A,B,C)
   - Gán nhãn góc: \tkzLabelAngles[pos=1,rotate=30](A,B,C){$\alpha$}
   - Tô miền đa giác: \tkzFillPolygon[color=green!80, fill opacity=0.5](A,B,C)
   - Tô miền tích phân: \fill[pattern=north east lines,opacity=0.8] plot[domain=a:b](\x,{f(\x)})--cycle;

4. ĐỒ THỊ GIẢI TÍCH (TIKZ & PGFPLOTS):
   - Trục toạ độ chuẩn: \draw[color=gray!50,dashed] (\xmin,\ymin) grid (\xmax,\ymax); \draw[->] (\xmin,0)--(\xmax,0) node [below]{$x$}; \draw[->] (0,\ymin)--(0,\ymax) node [left]{$y$}; \node at (0,0) [below left]{$O$};
   - Hàm bậc 3: \draw[smooth,samples=300] plot(\x,{\a*(\x)^3+\b*(\x)^2+\c*(\x)+\d});
   - Hàm nhất biến y = (ax+b)/(cx+d): ngắt 2 miền domain=\xmin:(-\d/\c-0.1) và domain=(-\d/\c+0.1:\xmax); tiệm cận đứng \draw[dashed] (-\d/\c,\ymin)--(-\d/\c,\ymax); tiệm cận ngang \draw[dashed] (\xmin,\a/\c)--(\xmax,\a/\c);
   - Hàm phân thức bậc 2 trên bậc 1 y = (ax^2+bx+c)/(dx+e): Sử dụng pgfplots \begin{axis}[grid=major, grid style={dashed, gray!50}, axis lines=middle, xlabel=$x$, ylabel=$y$] với 2 nhánh addplot domain qua tiệm cận đứng, và addplot nét đứt màu đỏ cho tiệm cận đứng và tiệm cận xiên.
"""


def get_tikz_packages_latex_header() -> list:
    """Trả về danh sách các gói LaTeX TikZ cần thiết cho Overleaf."""
    return [
        r"\usepackage{tikz,pgfplots}",
        r"\usepackage{tkz-tab}",
        r"\usepackage{tkz-euclide}",
        r"\usetikzlibrary{patterns,calc,angles,quotes}",
        r"\pgfplotsset{compat=1.18}",
    ]


def inject_tikz_spec_into_prompt(prompt_text: str, subject: str = "Toán") -> str:
    """Tự động nhúng quy chuẩn TikZ vào prompt biên soạn nếu là môn Toán hoặc môn có đồ thị."""
    subj_lower = str(subject).lower()
    if any(k in subj_lower for k in ["toán", "toan", "math"]):
        return prompt_text + "\n\n" + SYSTEM_PROMPT_TIKZ_BBT_GRAPH_SPEC
    return prompt_text
