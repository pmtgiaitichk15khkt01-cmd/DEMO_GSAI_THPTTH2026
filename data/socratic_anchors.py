# VIP 74.1 - HỆ THỐNG GIA SƯ AI THPT 2026 (CHUẨN GDPT 2018 - BẢN VÁ HOÀN THIỆN ĐA MÔN & ĐA KHỐI LỚP)
# -*- coding: utf-8 -*-
"""SOCRATIC KNOWLEDGE ANCHORS DATA MODULE"""

import os
import sys
import re
import json
import math

SOCRATIC_KNOWLEDGE_ANCHORS = {
    "Toán học": [
        # 1. Đơn điệu & Đạo hàm
        {
            "keywords": ["đồng biến", "nghịch biến", "đơn điệu", "khoảng đồng biến", "khoảng nghịch biến"],
            "concept": "Tính đơn điệu của hàm số (SGK Toán 12 - KNTT)",
            "formula": "Cho hàm số $y = f(x)$ có đạo hàm trên khoảng $(a; b)$:\n- $f'(x) \\ge 0, \\forall x \\in (a; b) \\Rightarrow$ Hàm số **đồng biến** trên $(a; b)$.\n- $f'(x) \\le 0, \\forall x \\in (a; b) \\Rightarrow$ Hàm số **nghịch biến** trên $(a; b)$.\n*(Dấu bằng chỉ xảy ra tại hữu hạn điểm)*",
            "prompt": "Em hãy tính đạo hàm $f'(x)$, tìm các nghiệm của phương trình $f'(x) = 0$ và xét dấu của $f'(x)$ để kết luận khoảng biến thiên nhé!"
        },
        # 2. Cực trị
        {
            "keywords": ["cực trị", "cực đại", "cực tiểu", "điểm cực đại", "điểm cực tiểu", "giá trị cực", "số điểm cực trị"],
            "concept": "Cực trị của hàm số (SGK Toán 12 - KNTT)",
            "formula": "- Điều kiện cần: Nếu hàm số đạt cực trị tại $x_0$ thì $f'(x_0) = 0$ hoặc $f'(x_0)$ không xác định.\n- Điều kiện đủ: $f'(x)$ đổi dấu từ $(+)$ sang $(-)$ qua $x_0 \\Rightarrow x_0$ là **điểm cực đại**; đổi dấu từ $(-)$ sang $(+) \\Rightarrow x_0$ là **điểm cực tiểu**.\n*(Chỉ các nghiệm bội lẻ mới làm $f'(x)$ đổi dấu và tạo thành cực trị)*",
            "prompt": "Em hãy giải phương trình $f'(x) = 0$, đếm các nghiệm bội lẻ (nghiệm đơn) làm đạo hàm đổi dấu để tìm số điểm cực trị nhé!"
        },
        # 3. Giá trị lớn nhất & nhỏ nhất
        {
            "keywords": ["giá trị lớn nhất", "giá trị nhỏ nhất", "gtln", "gtnn", "max", "min"],
            "concept": "Giá trị lớn nhất và nhỏ nhất của hàm số trên đoạn $[a; b]$ (SGK Toán 12 - KNTT)",
            "formula": "Quy tắc tìm GTLN, GTNN trên đoạn $[a; b]$:\n1. Tính đạo hàm $f'(x)$, tìm các nghiệm $x_i \\in (a; b)$ của phương trình $f'(x) = 0$.\n2. Tính các giá trị: $f(a)$, $f(b)$ và các $f(x_i)$.\n3. $\\max_{[a; b]} f(x) = \\max\\{f(a), f(b), f(x_i)\\}$; $\\min_{[a; b]} f(x) = \\min\\{f(a), f(b), f(x_i)\\}$.",
            "prompt": "Em hãy tìm các nghiệm của $f'(x) = 0$ nằm trong đoạn $[a; b]$, tính giá trị hàm số tại các điểm đó và hai đầu mút rồi so sánh nhé!"
        },
        # 4. Tiệm cận
        {
            "keywords": ["tiệm cận đứng", "tiệm cận ngang", "tiệm cận xiên", "đường tiệm cận"],
            "concept": "Đường tiệm cận của đồ thị hàm số (SGK Toán 12 - KNTT)",
            "formula": "- Tiệm cận đứng: Đường thẳng $x = x_0$ nếu ít nhất một giới hạn $\\lim_{x \\to x_0^\\pm} y = \\pm\\infty$.\n- Tiệm cận ngang: Đường thẳng $y = y_0$ nếu $\\lim_{x \\to \\pm\\infty} y = y_0$.\n- Tiệm cận xiên: Đường thẳng $y = ax + b$ với $a = \\lim_{x \\to \\pm\\infty} \\frac{y}{x}$, $b = \\lim_{x \\to \\pm\\infty} (y - ax)$.",
            "prompt": "Với hàm phân thức, em hãy tìm nghiệm của mẫu số (không triệt tiêu với tử số) để xác định tiệm cận đứng, và xét tỉ số bậc cao nhất khi $x \\to \\pm\\infty$ để tìm tiệm cận ngang/xiên nhé!"
        },
        # 5. Tiếp tuyến
        {
            "keywords": ["tiếp tuyến", "hệ số góc", "phương trình tiếp tuyến"],
            "concept": "Phương trình tiếp tuyến của đồ thị hàm số (SGK Toán 12 - KNTT)",
            "formula": "Phương trình tiếp tuyến của đồ thị $y = f(x)$ tại tiếp điểm $M(x_0; y_0)$:\n$$y = f'(x_0)(x - x_0) + y_0$$\n- Hệ số góc của tiếp tuyến là $k = f'(x_0)$.",
            "prompt": "Em hãy tính đạo hàm $f'(x)$, thay hoành độ tiếp điểm $x_0$ vào để tìm hệ số góc $k$ và lập phương trình tiếp tuyến nhé!"
        },
        # 6. Nguyên hàm cơ bản
        {
            "keywords": ["nguyên hàm", "họ nguyên hàm", "f(x) dx", "bảng nguyên hàm"],
            "concept": "Nguyên hàm & Bảng nguyên hàm cơ bản (SGK Toán 12 - KNTT)",
            "formula": "- Tuyến tính: $\\int [a f(x) + b g(x)]dx = a\\int f(x)dx + b\\int g(x)dx$\n- Lũy thừa: $\\int x^\\alpha dx = \\frac{x^{\\alpha+1}}{\\alpha+1} + C$ ($\\alpha \\ne -1$); $\\int \\frac{1}{x}dx = \\ln|x| + C$\n- Mũ: $\\int e^x dx = e^x + C$; $\\int a^x dx = \\frac{a^x}{\\ln a} + C$\n- Lượng giác: $\\int \\cos x dx = \\sin x + C$; $\\int \\sin x dx = -\\cos x + C$",
            "prompt": "Em hãy tách biểu thức thành tổng các số hạng đơn giản và áp dụng trực tiếp công thức nguyên hàm cơ bản tương ứng nhé!"
        },
        # 7. Tích phân & Ứng dụng
        {
            "keywords": ["tích phân", "diện tích hình phẳng", "thể tích khối tròn xoay"],
            "concept": "Tích phân và Ứng dụng hình học (SGK Toán 12 - KNTT)",
            "formula": "- Định nghĩa: $\\int_a^b f(x)dx = F(b) - F(a)$ với $F'(x) = f(x)$.\n- Diện tích hình phẳng giới hạn bởi $y=f(x)$, trục $Ox$, $x=a$, $x=b$: $S = \\int_a^b |f(x)|dx$.\n- Thể tích tròn xoay quay quanh $Ox$: $V = \\pi \\int_a^b [f(x)]^2 dx$.",
            "prompt": "Em hãy xác định cận tích phân $[a; b]$, viết đúng công thức giải tích và áp dụng định lý Newton-Leibniz $F(b) - F(a)$ để tính nhé!"
        },
        # 8. Thể tích khối đa diện & Tròn xoay
        {
            "keywords": ["thể tích khối", "khối chóp", "lăng trụ", "lập phương", "khối nón", "khối trụ", "thể tích mặt cầu", "khối cầu"],
            "concept": "Thể tích các khối đa diện và khối tròn xoay (SGK Toán 12 - KNTT)",
            "formula": "- Lăng trụ & Khối hộp: $V = B \\cdot h$ (Khối lập phương cạnh $a$: $V = a^3$).\n- Khối chóp: $V = \\frac{1}{3} B \\cdot h$.\n- Khối nón: $V = \\frac{1}{3}\\pi r^2 h$; Khối trụ: $V = \\pi r^2 h$; Mặt cầu: $S = 4\\pi R^2$, $V = \\frac{4}{3}\\pi R^3$.",
            "prompt": "Em hãy xác định diện tích đáy $B$ và chiều cao $h$ vuông góc từ đỉnh xuống đáy rồi thế vào công thức chuẩn nhé!"
        },
        # 8.5. Góc trong không gian Oxyz (Góc giữa hai mặt phẳng, hai đường thẳng, hai vectơ)
        {
            "keywords": ["góc nghiêng", "góc giữa hai mặt phẳng", "góc giữa 2 mặt phẳng", "góc giữa hai vectơ", "góc giữa hai đường thẳng", "góc giữa đường thẳng và mặt phẳng", "vectơ pháp tuyến của mái nhà", "mặt phẳng nằm ngang", "góc giữa", "cosin của góc", "góc giữa hai véc-tơ", "góc giữa 2 véc tơ"],
            "concept": "Góc trong không gian Oxyz (SGK Toán 12 - KNTT)",
            "formula": "- **Góc giữa hai mặt phẳng $(P)$ và $(Q)$:** $\\cos \\alpha = \\frac{|\\vec{n}_1 \\cdot \\vec{n}_2|}{|\\vec{n}_1| \\cdot |\\vec{n}_2|} = \\frac{|A_1 A_2 + B_1 B_2 + C_1 C_2|}{\\sqrt{A_1^2 + B_1^2 + C_1^2} \\cdot \\sqrt{A_2^2 + B_2^2 + C_2^2}}$ ($0^\\circ \\le \\alpha \\le 90^\\circ$).\n- **Góc giữa hai vectơ:** $\\cos(\\vec{u}, \\vec{v}) = \\frac{\\vec{u} \\cdot \\vec{v}}{|\\vec{u}| \\cdot |\\vec{v}|} = \\frac{x_1 x_2 + y_1 y_2 + z_1 z_2}{\\sqrt{x_1^2+y_1^2+z_1^2} \\cdot \\sqrt{x_2^2+y_2^2+z_2^2}}$.\n- **Góc giữa hai đường thẳng:** $\\cos \\varphi = \\frac{|\\vec{u}_1 \\cdot \\vec{u}_2|}{|\\vec{u}_1| \\cdot |\\vec{u}_2|}$.\n- **Góc giữa đường thẳng và mặt phẳng:** $\\sin \\theta = \\frac{|\\vec{u} \\cdot \\vec{n}|}{|\\vec{u}| \\cdot |\\vec{n}|}$.",
            "prompt": "Em hãy xác định hai vectơ pháp tuyến (hoặc chỉ phương) tương ứng, sau đó áp dụng công thức cosin $\\cos \\alpha = \\frac{|\\vec{n}_1 \\cdot \\vec{n}_2|}{|\\vec{n}_1| \\cdot |\\vec{n}_2|}$ (chú ý luôn lấy dấu giá trị tuyệt đối ở tử số để $0^\\circ \\le \\alpha \\le 90^\\circ$) để tính góc nghiêng nhé!"
        },
        # 9. Tọa độ vectơ Oxyz
        {
            "keywords": ["tọa độ", "vectơ", "vecto", "oxyz", "tích vô hướng", "độ dài vectơ"],
            "concept": "Hệ tọa độ trong không gian Oxyz (SGK Toán 12 - KNTT)",
            "formula": "- $\\vec{AB} = (x_B - x_A;\\; y_B - y_A;\\; z_B - z_A)$.\n- Độ dài: $|\\vec{a}| = \\sqrt{x^2 + y^2 + z^2}$; $|\\vec{AB}| = \\sqrt{(x_B - x_A)^2 + (y_B - y_A)^2 + (z_B - z_A)^2}$.\n- Tích vô hướng: $\\vec{u} \\cdot \\vec{v} = x_1 x_2 + y_1 y_2 + z_1 z_2$.\n- Điều kiện vuông góc: $\\vec{u} \\perp \\vec{v} \\Leftrightarrow \\vec{u} \\cdot \\vec{v} = 0$.",
            "prompt": "Em hãy lấy tọa độ ngọn trừ tọa độ gốc tương ứng để tìm tọa độ vectơ, rồi tính độ dài hoặc tích vô hướng theo công thức nhé!"
        },
        # 10. Phương trình mặt cầu Oxyz
        {
            "keywords": ["mặt cầu", "phương trình mặt cầu", "tâm i", "bán kính r"],
            "concept": "Phương trình mặt cầu trong không gian Oxyz (SGK Toán 12 - KNTT)",
            "formula": "- Phương trình chính tắc tâm $I(a; b; c)$, bán kính $R$: $(x - a)^2 + (y - b)^2 + (z - c)^2 = R^2$.\n- Dạng khai triển: $x^2 + y^2 + z^2 - 2ax - 2by - 2cz + d = 0$ có tâm $I(a; b; c)$, bán kính $R = \\sqrt{a^2 + b^2 + c^2 - d}$ ($a^2+b^2+c^2-d > 0$).",
            "prompt": "Em hãy xác định tọa độ tâm $I(a; b; c)$ và bán kính $R$ từ giả thiết đề bài, lưu ý đổi dấu khi đưa vào ngoặc chính tắc nhé!"
        },
        # 11. Phương trình mặt phẳng & Đường thẳng Oxyz
        {
            "keywords": ["mặt phẳng", "vectơ pháp tuyến", "đường thẳng", "vectơ chỉ phương", "khoảng cách từ điểm"],
            "concept": "Mặt phẳng và Đường thẳng trong Oxyz (SGK Toán 12 - KNTT)",
            "formula": "- Mặt phẳng qua $M_0(x_0; y_0; z_0)$ có VTPT $\\vec{n}=(A; B; C)$: $A(x - x_0) + B(y - y_0) + C(z - z_0) = 0$.\n- Khoảng cách từ điểm $M(x_M; y_M; z_M)$ đến $(P): Ax+By+Cz+D=0$: $d(M, (P)) = \\frac{|Ax_M + By_M + Cz_M + D|}{\\sqrt{A^2 + B^2 + C^2}}$.\n- Đường thẳng qua $M_0$ có VTCP $\\vec{u}=(a; b; c)$: $\\frac{x - x_0}{a} = \\frac{y - y_0}{b} = \\frac{z - z_0}{c}$.",
            "prompt": "Em hãy tìm một điểm đi qua và vectơ chỉ phương / pháp tuyến tương ứng để lập phương trình hoặc tính khoảng cách nhé!"
        },
        # 12. Mũ & Logarit
        {
            "keywords": ["logarit", "log", "ln", "mũ", "luỹ thừa", "tập nghiệm của bất phương trình"],
            "concept": "Hàm số Mũ và Logarit (SGK Toán 12 - KNTT)",
            "formula": "- Điều kiện xác định của $\\log_a b$: cơ số $0 < a \\ne 1$, biểu thức $b > 0$.\n- Biến đổi: $\\log_a(x y) = \\log_a x + \\log_a y$; $\\log_a(\\frac{x}{y}) = \\log_a x - \\log_a y$; $\\log_a(x^\\alpha) = \\alpha\\log_a x$.\n- Bất phương trình $\\log_a f(x) > \\log_a g(x)$: Cùng chiều khi $a > 1$; Ngược chiều khi $0 < a < 1$ (kèm ĐKXĐ).",
            "prompt": "Em hãy đặt điều kiện xác định trước tiên, sau đó đưa về cùng cơ số và chú ý chiều của bất phương trình khi cơ số lớn hơn hay nhỏ hơn 1 nhé!"
        },
        # 13. Xác suất cổ điển & Xác suất có điều kiện
        {
            "keywords": ["xác suất", "biến cố", "xác suất có điều kiện", "xác suất toàn phần", "bayes", "biến cố độc lập"],
            "concept": "Xác suất & Biến cố (SGK Toán 12 - KNTT)",
            "formula": "- Xác suất cổ điển: $P(A) = \\frac{n(A)}{n(\\Omega)}$.\n- Xác suất có điều kiện: $P(A|B) = \\frac{P(AB)}{P(B)}$.\n- Công thức nhân xác suất: $P(AB) = P(A) \\cdot P(B|A)$.\n- Công thức xác suất toàn phần: $P(A) = \\sum P(B_i)P(A|B_i)$.",
            "prompt": "Em hãy xác định số phần tử không gian mẫu $n(\\Omega)$, số kết quả thuận lợi $n(A)$ hoặc lập sơ đồ hình cây để tính xác suất nhé!"
        },
        # 14. Mẫu số liệu ghép nhóm & Các số đặc trưng đo xu thế trung tâm, phân tán
        {
            "keywords": ["mẫu số liệu", "ghép nhóm", "khoảng biến thiên", "khoảng tứ phân vị", "độ lệch chuẩn", "phương sai", "trung vị", "tứ phân vị", "mốt"],
            "concept": "Các số đặc trưng của Mẫu số liệu ghép nhóm (SGK Toán 12 - KNTT)",
            "formula": "- **Khoảng biến thiên:** $R = a_k - a_1$ (Lấy đầu mút phải của nhóm cuối cùng trừ đầu mút trái của nhóm đầu tiên).\n- **Khoảng tứ phân vị:** $\\Delta_Q = Q_3 - Q_1$.\n- **Trung vị $M_e$:** $M_e = u_m + \\dfrac{\\frac{n}{2} - C}{n_m} \\cdot (u_{m+1} - u_m)$.\n- **Mốt $M_o$:** $M_o = u_j + \\dfrac{n_j - n_{j-1}}{(n_j - n_{j-1}) + (n_j - n_{j+1})} \\cdot (u_{j+1} - u_j)$.\n- **Phương sai & Độ lệch chuẩn:** $s^2 = \\frac{1}{n}\\sum n_i(c_i - \\bar{x})^2$; $s = \\sqrt{s^2}$.",
            "prompt": "Em hãy đối chiếu công thức số đặc trưng trong SGK KNTT (chú ý: khoảng biến thiên $R = a_k - a_1$ bằng đầu mút phải nhóm cuối trừ đầu mút trái nhóm đầu) để chọn phương án chuẩn xác nhé!"
        }
    ],
    "Vật lý": [
        {
            "keywords": ["dao động điều hòa", "con lắc", "chu kì", "tần số", "pha dao động", "li độ"],
            "concept": "Dao động điều hòa (SGK Vật lý 12 - KNTT)",
            "formula": "- Li độ: $x = A\\cos(\\omega t + \\varphi)$.\n- Vận tốc: $v = x' = -\\omega A\\sin(\\omega t + \\varphi) = \\omega A\\cos(\\omega t + \\varphi + \\frac{\\pi}{2})$.\n- Gia tốc: $a = v' = -\\omega^2 x = \\omega^2 A\\cos(\\omega t + \\varphi + \\pi)$.\n- Hệ thức độc lập: $x^2 + \\frac{v^2}{\\omega^2} = A^2$; $a = -\\omega^2 x$.",
            "prompt": "Em hãy xác định các đại lượng $A, \\omega, \\varphi$ từ giả thiết và áp dụng hệ thức độc lập thời gian để tính đại lượng cần tìm nhé!"
        },
        {
            "keywords": ["sóng cơ", "bước sóng", "sóng dừng", "giao thoa"],
            "concept": "Sóng cơ và Giao thoa sóng (SGK Vật lý 12 - KNTT)",
            "formula": "- Bước sóng: $\\lambda = v \\cdot T = \\frac{v}{f}$.\n- Sóng dừng 2 đầu cố định: $L = k\\frac{\\lambda}{2}$ ($k$ bụng sóng, $k+1$ nút).\n- Cực đại giao thoa: $d_2 - d_1 = k\\lambda$; Cực tiểu giao thoa: $d_2 - d_1 = (k + 0.5)\\lambda$.",
            "prompt": "Em hãy xác định vận tốc truyền sóng $v$ và tần số $f$ để tính bước sóng $\\lambda$, sau đó đối chiếu với điều kiện giao thoa/sóng dừng nhé!"
        },
        {
            "keywords": ["nhiệt độ", "nhiệt dung", "nhiệt hóa hơi", "nhiệt nóng chảy", "khí lý tưởng", "áp suất", "thể tích"],
            "concept": "Vật lý nhiệt & Thuyết động học phân tử chất khí (SGK Vật lý 12 - KNTT)",
            "formula": "- Phương trình Clapeyron-Mendeleev: $pV = nRT = \\frac{m}{\\mu}RT$.\n- Nhiệt lượng: $Q = mc\\Delta T$; Nhiệt chuyển thể: $Q = \\lambda m$ (nóng chảy), $Q = L m$ (hóa hơi).\n- Định luật I Nhiệt động lực học: $\\Delta U = A + Q$.",
            "prompt": "Em hãy tóm tắt các trạng thái $(p_1, V_1, T_1)$ và $(p_2, V_2, T_2)$, chú ý đổi nhiệt độ sang thang Kelvin ($T = t + 273$) để thế vào phương trình nhé!"
        }
    ],
    "Hóa học": [
        {
            "keywords": ["ester", "xà phòng hóa", "chất béo", "lipid", "thủy phân", "triglyceride"],
            "concept": "Ester - Lipid (SGK Hóa học 12 - KNTT & Danh pháp IUPAC)",
            "formula": "- Phản ứng xà phòng hóa ester: $RCOOR' + NaOH \\xrightarrow{t^o} RCOONa + R'OH$.\n- Thủy phân chất béo: $(RCOO)_3C_3H_5 + 3NaOH \\xrightarrow{t^o} 3RCOONa + C_3H_5(OH)_3$.\n- Bảo toàn khối lượng: $m_{ester} + m_{NaOH} = m_{muối} + m_{alcohol}$.",
            "prompt": "Em hãy xác định số mol các chất, viết phương trình phản ứng và áp dụng định luật bảo toàn khối lượng để tìm khối lượng muối hoặc alcohol nhé!"
        },
        {
            "keywords": ["glucose", "fructose", "saccharose", "carbohydrate", "tinh bột", "cellulose"],
            "concept": "Carbohydrate (SGK Hóa học 12 - KNTT)",
            "formula": "- Monosaccharide: Glucose ($C_6H_{12}O_6$) có nhóm $-CHO$ tráng bạc ra $2Ag$. Fructose có nhóm $C=O$, trong môi trường kiềm chuyển hóa thành glucose nên cũng tráng bạc.\n- Disaccharide: Saccharose ($C_{12}H_{22}O_{11}$) không tráng bạc, khi thủy phân tạo $1$ Glucose + $1$ Fructose.\n- Polysaccharide: Tinh bột, Cellulose thủy phân hoàn toàn tạo Glucose.",
            "prompt": "Em hãy đối chiếu công thức cấu tạo và nhóm chức đặc trưng để phân biệt khả năng phản ứng với thuốc thử Tollens ($AgNO_3/NH_3$) hoặc $Cu(OH)_2$ nhé!"
        }
    ],
    "Ngữ văn": [
        {
            "keywords": ["thể loại", "phương thức biểu đạt", "biện pháp tu từ", "đọc hiểu", "hình ảnh", "tác dụng"],
            "concept": "Đọc hiểu văn bản theo đặc trưng thể loại (SGK Ngữ văn 12 - KNTT)",
            "formula": "- Nhận diện: Thể thơ (tự do, 7 chữ, lục bát...), PTBĐ (biểu cảm, tự sự, nghị luận, thuyết minh...).\n- Phân tích BPTT: Gọi tên BPTT ➔ Chỉ ra từ ngữ/hình ảnh thể hiện ➔ Nêu tác dụng gợi hình, gợi cảm và làm nổi bật tư tưởng của tác giả.",
            "prompt": "Em hãy bám sát từ ngữ, hình ảnh trong ngữ liệu để chỉ rõ phương diện nghệ thuật và thông điệp mà tác giả gửi gắm nhé!"
        },
        {
            "keywords": ["nghị luận xã hội", "đoạn văn", "bài học", "thông điệp", "ý nghĩa"],
            "concept": "Viết đoạn văn nghị luận xã hội (200 chữ)",
            "formula": "- Mở đoạn: Dẫn dắt và nêu trực tiếp vấn đề nghị luận (1 câu).\n- Thân đoạn: Giải thích ngắn gọn ➔ Bàn luận, chứng minh (dẫn chứng thực tế xác thực) ➔ Mở rộng/phản đề.\n- Kết đoạn: Rút ra bài học nhận thức và hành động thiết thực cho bản thân.",
            "prompt": "Em hãy lựa chọn dẫn chứng thực tế tiêu biểu và liên hệ trách nhiệm của tuổi trẻ để bài viết giàu tính thuyết phục nhé!"
        }
    ],
    "Tiếng Anh": [
        {
            "keywords": ["pronunciation", "stress", "pronounced", "underlined", "primary stress"],
            "concept": "Pronunciation & Word Stress (CEFR Standards)",
            "formula": "- 2-syllable nouns/adjectives usually stress on 1st syllable (e.g., 'table, 'clever).\n- 2-syllable verbs usually stress on 2nd syllable (e.g., de'cide, pre'sent).\n- Endings with -tion, -sion, -ic stress on syllable right before (e.g., pro'tection, scien'tific).",
            "prompt": "Read each word aloud carefully and identify the syllable with higher pitch and longer duration to find the difference!"
        },
        {
            "keywords": ["relative clause", "which", "whom", "whose", "where", "conditional", "if", "unless"],
            "concept": "Grammar: Clauses & Conditionals",
            "formula": "- Relative Pronouns: Who (subject/people), Whom (object/people), Which (things), Whose (possession).\n- Conditionals: Type 1 (If + V_s/es, will + V0); Type 2 (If + V2/ed, would + V0); Type 3 (If + had V3/ed, would have V3/ed).",
            "prompt": "Look closely at the subject, tense of the main clause, and the role of the noun being replaced to choose the correct structure!"
        }
    ]
}

def sanitize_socratic_hint(hint_text, correct_answer="", q_text="", options=None, level="TH", subject="Toán học", grade_num=12):
    """
    HƯỚNG DẪN TƯ DUY SOCRATIC BÌNH DÂN HỌC VỤ (LUỒNG 1) - CHUẨN SƯ PHẠM QUỐC GIA.
    Nguyên tắc sư phạm bất biến:
      1. TUYỆT ĐỐI 100% KHÔNG BAO GIỜ GIẢI HỘ, KHÔNG PHUN RA ĐÁP ÁN (A/B/C/D, Đúng/Sai, hay số điền cuối cùng) HOẶC PHÉP TÍNH THAY SỐ CỤ THỂ.
      2. Cung cấp ĐIỂM TỰA KIẾN THỨC CỐT LÕI (Định lý, Công thức tổng quát SGK Kết Nối Tri Thức).
      3. Đưa ra CÂU HỎI ĐỊNH HƯỚNG TƯ DUY SOCRATIC để học sinh tự suy nghĩ và tự đặt bút tính toán.
    """
    subj_key = str(subject or "Toán học").strip()
    q_str = str(q_text or "").strip()
    q_lower = q_str.lower()
    corr_ans = str(correct_answer or "").strip()
    
    # 0. ƯU TIÊN TUYỆT ĐỐI CHO CÂU HỎI ĐỌC BẢNG BIẾN THIÊN (BBT) & ĐỒ THỊ (GỢI MỞ KỸ NĂNG, KHÔNG SPOIL ĐÁP ÁN)
    if any(k in q_lower for k in ["bảng biến thiên", "bbt", "bảng xét dấu"]):
        if any(k in q_lower for k in ["nghịch biến", "đồng biến"]):
            return (
                "🎯 **Kỹ năng đọc nhanh Bảng biến thiên (SGK Toán GDPT 2018):**\n"
                "- Quan sát dòng $y'$ (hoặc $f'(x)$): Khoảng nào mang dấu trừ ($-$) hoặc mũi tên dòng $y$ đi xuống ($\\searrow$) là khoảng **nghịch biến**.\n"
                "- Khoảng nào mang dấu cộng ($+$) hoặc mũi tên dòng $y$ đi lên ($\\nearrow$) là khoảng **đồng biến**.\n\n"
                "💡 **Gợi mở Socratic:** *Em hãy đối chiếu các khoảng phương án với dòng dấu của $y'$ để chọn khoảng chính xác nhé!*"
            )
        elif any(k in q_lower for k in ["cực đại", "cực tiểu", "cực trị"]):
            return (
                "🎯 **Kỹ năng đọc Cực trị từ BBT (SGK Toán GDPT 2018):**\n"
                "- Điểm cực đại $x_{CĐ}$: Nơi $y'$ đổi dấu từ $(+)$ sang $(-)$ (đỉnh nhô lên).\n"
                "- Điểm cực tiểu $x_{CT}$: Nơi $y'$ đổi dấu từ $(-)$ sang $(+)$ (đáy lõm xuống).\n\n"
                "💡 **Gợi mở Socratic:** *Lưu ý: 'Điểm cực trị của hàm số' là hoành độ $x$, còn 'Giá trị cực trị' là tung độ $y$ nhé!*"
            )
        elif any(k in q_lower for k in ["tiệm cận"]):
            return (
                "🎯 **Kỹ năng đọc Tiệm cận từ BBT (SGK Toán GDPT 2018):**\n"
                "- Tiệm cận đứng: Tại $x = x_0$ có dấu hai vạch song song ($||$) và ít nhất một bên $y \\to \\pm\\infty$.\n"
                "- Tiệm cận ngang: Giá trị hữu hạn của $y$ khi $x \\to \\pm\\infty$.\n\n"
                "💡 **Gợi mở Socratic:** *Em hãy kiểm tra hai đầu vô cực của dòng $x$ và các điểm gián đoạn hai vạch để tìm tiệm cận nhé!*"
            )
    elif any(k in q_lower for k in ["đồ thị của hàm số nào", "là của hàm số nào", "đường cong dưới đây"]):
        return (
            "🎯 **Kỹ năng nhận dạng hàm số từ Đồ thị (SGK Toán GDPT 2018):**\n"
            "1. Quan sát đường tiệm cận đứng và tiệm cận ngang/xiên.\n"
            "2. Kiểm tra giao điểm của đồ thị với trục tung $Oy$ (thay $x = 0$ để tìm $y$).\n"
            "3. Xét dấu hệ số bậc cao nhất dựa vào chiều của nhánh đồ thị bên phải cùng.\n\n"
            "💡 **Gợi mở Socratic:** *Em hãy dùng phương pháp loại trừ lần lượt 4 phương án dựa vào 3 đặc trưng trên nhé!*"
        )

    # 1. ƯU TIÊN 1: BÀI TOÁN TỐI ƯU KINH TẾ & THỰC TẾ (Doanh thu, Lợi nhuận, Chi phí, Sản xuất, Thể tích, Bơi ngược dòng, Nồng độ thuốc...)
    # Bắt buộc ưu tiên để không bị bắt nhầm vào Mũ/Logarit khi bài toán chứa ln(1+x) hoặc e^
    if any(k in q_lower for k in [
        "giá tour", "doanh thu", "lợi nhuận", "chi phí", "sản xuất", "thùng tôn",
        "hộp chữ nhật", "hộp không nắp", "diện tích bề mặt", "nồng độ thuốc",
        "bơi ngược dòng", "năng lượng tiêu hao", "tiêu hao", "tối ưu"
    ]):
        return (
            "🎯 **Định hướng mô hình hóa bài toán Tối ưu thực tế (SGK GDPT 2018):**\n"
            "- **Bước 1 (Chọn biến số & Tập xác định):** Gọi ẩn $x$ (hoặc $t, v$) là đại lượng thay đổi kèm điều kiện thực tế (ví dụ: $x > 0$ hoặc $v > 6$).\n"
            "- **Bước 2 (Thiết lập hàm mục tiêu):**\n"
            "  + Biểu diễn các đại lượng phụ thuộc theo ẩn số (Lợi nhuận = Doanh thu - Chi phí, Năng lượng tiêu hao $E(v) = c v^3 t$, hoặc Diện tích toàn phần $S(x)$).\n"
            "  + Xây dựng hàm số mục tiêu cần tối ưu: $f(x)$ (tìm GTLN hoặc GTNN).\n"
            "- **Bước 3 (Khảo sát cực trị):** Tính đạo hàm $f'(x) = 0$ hoặc áp dụng BĐT Cauchy để tìm điểm tối ưu.\n\n"
            "💡 **Gợi mở Socratic:** *Em hãy lập hàm số mục tiêu theo biến đề bài cho, tính đạo hàm tìm cực trị rồi đối chiếu với câu hỏi nhé!*"
        )

    # 2. ƯU TIÊN 2: BÀI TOÁN MẪU SỐ LIỆU GHÉP NHÓM (Thống kê Toán 12 KNTT)
    # Ưu tiên trước Xác suất để không bị gán nhầm sang P(A) = n(A)/n(Omega)
    if any(k in q_lower for k in ["trung vị", "tứ phân vị", "mốt", "độ lệch chuẩn", "phương sai", "ghép nhóm", "mẫu số liệu"]):
        return (
            "🎯 **Công thức Thống kê Mẫu số liệu ghép nhóm (SGK Toán 12 KNTT):**\n"
            "- **Cỡ mẫu:** $n = \\sum n_i$. Xác định nhóm chứa giá trị đặc trưng (với Trung vị $M_e$: vị trí $\\frac{n}{2}$).\n"
            "- **Công thức Trung vị $M_e$:** $M_e = u_m + \\dfrac{\\frac{n}{2} - C}{n_m} \\cdot (u_{m+1} - u_m)$, trong đó $C$ là tần số tích lũy nhóm trước, $n_m$ là tần số nhóm chứa $M_e$.\n"
            "- **Công thức Tứ phân vị $Q_1, Q_3$:** Tương tự với vị trí $\\frac{n}{4}$ và $\\frac{3n}{4}$.\n\n"
            "💡 **Gợi mở Socratic:** *Em hãy tính cỡ mẫu $n$, cộng dồn tần số để tìm đúng nhóm chứa trung vị $[u_m; u_{m+1})$ rồi thay số vào công thức nhé!*"
        )

    # 3. ƯU TIÊN 3: BÀI TOÁN HÌNH HỌC TỌA ĐỘ TRONG KHÔNG GIAN OXYZ
    # Ngăn chặn việc bắt nhầm sang công thức thể tích khối tròn xoay lớp 11
    if any(k in q_lower for k in ["trong không gian oxyz", "oxzy", "oxyz", "hệ tọa độ oxyz"]):
        if any(k in q_lower for k in ["mặt cầu", "bán kính mặt cầu", "ngoại tiếp tứ diện"]):
            return (
                "🎯 **Điểm tựa lý thuyết SGK Kết Nối Tri Thức:**\n"
                "*Phương trình & Bán kính Mặt cầu trong không gian Oxyz (SGK Toán 12 - KNTT)*\n\n"
                "- Phương trình chính tắc tâm $I(a; b; c)$, bán kính $R$: $(x - a)^2 + (y - b)^2 + (z - c)^2 = R^2$.\n"
                "- Với tứ diện vuông $OABC$ tại $O$ với $A(a; 0; 0), B(0; b; 0), C(0; 0; c)$:\n"
                "  + Tâm mặt cầu ngoại tiếp: $I(\\frac{a}{2}; \\frac{b}{2}; \\frac{c}{2})$.\n"
                "  + Bán kính mặt cầu ngoại tiếp: $R = \\frac{1}{2}\\sqrt{OA^2 + OB^2 + OC^2} = \\frac{1}{2}\\sqrt{a^2 + b^2 + c^2}$.\n\n"
                "💡 **Định hướng tư duy Socratic:**\n"
                "*Em hãy xác định độ dài 3 cạnh vuông góc $OA, OB, OC$ rồi áp dụng công thức bán kính mặt cầu ngoại tiếp tứ diện vuông nhé!*"
            )
        elif any(k in q_lower for k in ["mái nhà", "góc giữa hai mặt phẳng", "góc giữa mặt phẳng"]):
            return (
                "🎯 **Điểm tựa lý thuyết SGK Kết Nối Tri Thức:**\n"
                "*Góc giữa hai mặt phẳng trong không gian Oxyz (SGK Toán 12 - KNTT)*\n\n"
                "Cho hai mặt phẳng có VTPT lần lượt là $\\vec{n}_1$ và $\\vec{n}_2$:\n"
                "$$\\cos \\alpha = \\dfrac{|\\vec{n}_1 \\cdot \\vec{n}_2|}{|\\vec{n}_1| \\cdot |\\vec{n}_2|}, \\quad (0^\\circ \\le \\alpha \\le 90^\\circ)$$\n\n"
                "💡 **Định hướng tư duy Socratic:**\n"
                "*Em hãy tính tích vô hướng của hai vectơ pháp tuyến và chia cho tích hai độ dài để tìm góc $\\alpha$ nhé!*"
            )
        elif any(k in q_lower for k in ["khoảng cách ngắn nhất", "khoảng cách", "thiết bị bay", "đường bay", "khoảng cách từ", "trạm phát sóng", "rô-bốt", "robot"]):
            return (
                "🎯 **Phương pháp tọa độ giải bài toán Khoảng cách Oxyz (SGK GDPT 2018):**\n"
                "- **Bước 1 (Xác định yếu tố hình học):** Tìm tọa độ điểm mốc (ví dụ: $M(1;2;0)$ hoặc $O(0;0;0)$) và vectơ chỉ phương $\\vec{u} = \\vec{AB}$ của đường thẳng chuyển động.\n"
                "- **Bước 2 (Công thức khoảng cách từ điểm đến đường thẳng):** Khoảng cách ngắn nhất chính là độ dài hình chiếu vuông góc:\n"
                "  $$d(M, AB) = \\dfrac{|[\\vec{AM}, \\vec{AB}]|}{|\\vec{AB}|}$$\n"
                "- **Bước 3 (Hoặc phương pháp tam thức bậc hai):** Viết tọa độ điểm di động $P(t) \\in AB$ theo tham số $t$, lập biểu thức khoảng cách $MP(t) = \\sqrt{f(t)}$ và tìm giá trị nhỏ nhất của tam thức bậc hai $f(t)$.\n\n"
                "💡 **Gợi mở Socratic:** *Em hãy tính tọa độ vectơ $\\vec{AB}$, $\\vec{AM}$, tính tích có hướng $[\\vec{AM}, \\vec{AB}]$ rồi áp dụng công thức chia độ dài để ra khoảng cách ngắn nhất nhé!*"
            )

    # 4. XỬ LÝ ĐẶC THÙ CHO PHẦN II (ĐÚNG/SAI)
    # Trắc nghiệm Đúng/Sai: Tuyệt đối không phán "Ý a đúng, b sai"
    if (options is None or len(options) == 0) and (any(kw in q_lower for kw in ["mệnh đề", "khẳng định sau", "đúng hay sai", "mỗi ý"]) or ("đúng" in corr_ans.lower() and "sai" in corr_ans.lower())):
        return (
            "🎯 **Chiến lược kiểm định 4 Mệnh đề Đúng/Sai (SGK GDPT 2018):**\n"
            "- **Mệnh đề về ĐKXĐ / Tập xác định:** Kiểm tra điều kiện mẫu số khác 0 và biểu thức dưới căn bậc chẵn $\\ge 0$.\n"
            "- **Mệnh đề về Đơn điệu / Cực trị:** Tính đạo hàm $f'(x)$ và lập bảng xét dấu độc lập trên từng khoảng.\n"
            "- **Mệnh đề về Giá trị cụ thể:** Thay trực tiếp toạ độ / số liệu đề bài vào phương trình ban đầu.\n\n"
            "💡 **Gợi mở Socratic:** *Em hãy xét độc lập từng mệnh đề a), b), c), d) theo quy tắc cần và đủ để quyết định Đúng hay Sai nhé!*"
        )

    # 5. XỬ LÝ ĐẶC THÙ CHO PHẦN III (TRẢ LỜI NGẮN / VẬN DỤNG CAO)
    if (options is None or len(options) == 0) and corr_ans and any(c.isdigit() for c in corr_ans):
        # A. Tốc độ tăng trưởng / Đạo hàm thực tế
        if any(k in q_lower for k in ["vi khuẩn", "tốc độ tăng trưởng", "tốc độ phát triển", "quy luật s(t)", "vận tốc lớn nhất"]):
            return (
                "🎯 **Định hướng giải bài toán Tốc độ cực trị (SGK GDPT 2018):**\n"
                "- **Bước 1 (Hàm tốc độ):** Tốc độ tăng trưởng/vận tốc chính là đạo hàm cấp một của hàm số lượng: $v(t) = S'(t)$.\n"
                "- **Bước 2 (Tìm cực đại của tốc độ):** Để tốc độ $v(t)$ đạt giá trị lớn nhất, ta khảo sát hàm số $v(t)$ bằng cách giải phương trình đạo hàm: $v'(t) = S''(t) = 0$.\n"
                "- **Bước 3 (Kiểm tra điều kiện):** Đối chiếu nghiệm $t$ với khoảng xác định của thời gian trong đề bài.\n\n"
                "💡 **Gợi mở Socratic:** *Em hãy lấy đạo hàm $S'(t)$ để tìm hàm tốc độ, sau đó khảo sát cực trị của hàm tốc độ này để tìm thời điểm $t$ nhé!*"
            )
        # B. Hướng dẫn tổng quát có chiều sâu cho câu hỏi trả lời ngắn
        else:
            return (
                "🎯 **Chiến lược giải toán Trả lời ngắn & Vận dụng cao (Bộ GD&ĐT):**\n"
                "1. **Mô hình hóa:** Nhận diện đối tượng toán học/vật lý trung tâm và thiết lập phương trình liên hệ từ giả thiết bài toán.\n"
                "2. **Giải toán:** Áp dụng định lý giải tích, định luật bảo toàn hoặc công thức tọa độ chuyên môn để giải phương trình ẩn số.\n"
                "3. **Kiểm tra đáp số:** Rà soát điều kiện thực tế của biến số và làm tròn đúng định dạng phiếu thi (tối đa 4 ký tự).\n\n"
                "💡 **Gợi mở Socratic:** *Em hãy bám sát các đại lượng đã cho của đề bài, lập phương trình liên hệ và tính toán cẩn thận từng bước nhé!*"
            )

    # 6. TÌM KNOWLEDGE ANCHOR PHÙ HỢP TRONG KHO SGK GDPT 2018 (CHO TRẮC NGHIỆM 4 PHƯƠNG ÁN)
    anchors = SOCRATIC_KNOWLEDGE_ANCHORS.get(subj_key, [])
    if not anchors and subj_key in ["Toán", "Toán học"]:
        anchors = SOCRATIC_KNOWLEDGE_ANCHORS.get("Toán học", [])
    elif not anchors and "Văn" in subj_key:
        anchors = SOCRATIC_KNOWLEDGE_ANCHORS.get("Ngữ văn", [])
    elif not anchors and "Anh" in subj_key:
        anchors = SOCRATIC_KNOWLEDGE_ANCHORS.get("Tiếng Anh", [])
    elif not anchors and "Lý" in subj_key:
        anchors = SOCRATIC_KNOWLEDGE_ANCHORS.get("Vật lý", [])
    elif not anchors and "Hóa" in subj_key:
        anchors = SOCRATIC_KNOWLEDGE_ANCHORS.get("Hóa học", [])

    matched_anchor = None
    if anchors:
        for anc in anchors:
            if any(k in q_lower for k in anc["keywords"]):
                matched_anchor = anc
                break

    if matched_anchor:
        return (
            f"🎯 **Điểm tựa lý thuyết SGK Kết Nối Tri Thức:**\n"
            f"*{matched_anchor['concept']}*\n\n"
            f"{matched_anchor['formula']}\n\n"
            f"💡 **Định hướng tư duy Socratic:**\n"
            f"{matched_anchor['prompt']}"
        )

    # 3. BỨC TƯỜNG LỬA ANTI-LEAK FIREWALL: THANH LỌC LỜI GIẢI CHI TIẾT
    raw_h = str(hint_text or "").strip()
    if raw_h:
        sentences = re.split(r'[\n\r]+|[.!?]\s+(?=[A-ZÀÁẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬĐÈÉẺẼẸÊẾỀỂỄỆÌÍỈĨỊÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴ])', raw_h)
        clean_lines = []
        
        # Danh sách chuỗi cấm (Blacklist các phương án và đáp án)
        forbidden_snippets = []
        if options and isinstance(options, list):
            for opt in options:
                opt_clean = re.sub(r'^[A-D]\s*[\.\:\)]\s*', '', str(opt)).strip()
                if len(opt_clean) >= 3:
                    forbidden_snippets.append(opt_clean.lower())
        if corr_ans and len(corr_ans) >= 2:
            forbidden_snippets.append(corr_ans.lower())

        for s in sentences:
            s_clean = s.strip()
            if not s_clean: continue

            # 1. Chặn câu chứa từ khóa chỉ định đáp án
            if re.search(r'(?i)\b(?:do đó|suy ra|kết luận|chọn|đáp án|đáp số|kết quả(?:\s*là)?|phương án(?:\s*đúng)?|vậy|nghiệm là|ta được)\b', s_clean):
                continue

            # 2. Chặn câu phán Đúng/Sai theo từng ý: a) Đúng, Ý b sai, (a) Đúng...
            if re.search(r'(?i)(?:mệnh đề|ý)?\s*[\(\[]?[a-d][\)\]\.\:\-]?\s*(?:là\s*)?(?:đúng|sai|đ|s)\b', s_clean):
                continue
            if re.search(r'(?i)\b(?:ý|mệnh đề)\s*[a-d]\s*,\s*[a-d]', s_clean):
                continue

            # 3. Chặn câu tính toán cụ thể ra số học hoặc biểu thức có dấu = kèm số liệu
            if re.search(r'=\s*[-+]?\d+(?:[.,]\d+)?\b', s_clean) or re.search(r'=\s*\([^\)]*[-+]?\d+', s_clean):
                continue

            # 4. Chặn câu chứa nguyên văn phương án đúng
            s_lower = s_clean.lower()
            if any(snip in s_lower for snip in forbidden_snippets if len(snip) > 3):
                continue

            clean_lines.append(s_clean)

        # Chỉ chấp nhận nếu câu còn lại mang tính lý thuyết/phương pháp thuần túy
        if clean_lines and len(" ".join(clean_lines)) >= 25:
            safe_content = " ".join(clean_lines[:2])
            # Kiểm tra an toàn lần cuối
            if not any(k in safe_content.lower() for k in ["chọn", "đáp án", "đúng", "sai"]):
                return (
                    f"🎯 **Điểm tựa kiến thức:**\n{safe_content}\n\n"
                    f"💡 **Thử thách Socratic:** *Dựa vào định lý và công thức nền tảng trên, em hãy tự tay thực hiện phép tính để tìm ra kết quả chính xác nhé!*"
                )

    # 4. UNIVERSAL SOCRATIC FALLBACK (CHUẨN 3 BƯỚC KHÔNG BAO GIỜ CHỨA SỐ LIỆU HAY ĐÁP ÁN)
    if "Văn" in subj_key:
        return (
            "🎯 **Bước 1 (Nhận diện bản chất):** Đọc kỹ văn bản, xác định thể loại, phương thức biểu đạt và hoàn cảnh xuất xứ.\n\n"
            "🔑 **Bước 2 (Chiến lược tư duy):** Bám sát các từ ngữ, hình ảnh đặc sắc và biện pháp nghệ thuật trong đoạn trích.\n\n"
            "💡 **Gợi mở Socratic:** *Em hãy lập luận theo từng luận điểm rõ ràng và liên hệ bài học nhân sinh sâu sắc nhé!*"
        )
    elif "Anh" in subj_key:
        return (
            "🎯 **Step 1 (Core Knowledge):** Identify the grammar rule, tense, or phonetics pattern required by the sentence.\n\n"
            "🔑 **Step 2 (Clue Analysis):** Look for signal words, time expressions, or subject-verb relationships.\n\n"
            "💡 **Socratic Prompt:** *Eliminate incorrect distractors and apply the core rule to determine the right option!*"
        )
    else:
        return (
            "🎯 **Bước 1 (Nhận diện bản chất bài toán):** Xác định rõ giả thiết đề bài, dạng toán và công thức định lý tương ứng trong SGK Kết Nối Tri Thức.\n\n"
            "🔑 **Bước 2 (Chiến lược tư duy):** Thiết lập phương trình liên hệ giữa các đại lượng đã biết và đại lượng cần tìm, loại trừ các phương án không hợp lý về dấu hoặc đơn vị.\n\n"
            "💡 **Gợi mở Socratic:** *Em hãy tự tay thế số liệu từ đề bài vào công thức tổng quát để tính ra đáp số chính xác nhé!*"
        )



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


_LATEX_JSON_COLLISION_CMDS = (
    r"frac|dfrac|tfrac|forall|fbox|footnotesize|filldraw|fill|flat|"
    r"bar|beta|begin|binom|bf|textbf|bigcup|bigcap|bigoplus|bigotimes|big|Big|bigl|bigr|bullet|bot|boxed|backslash|"
    r"neq|ne|notin|ni|nu|nabla|nearrow|nwarrow|natural|neg|nleq|ngeq|nmid|noindent|newline|"
    r"right|rightarrow|longrightarrow|Rightarrow|Longrightarrow|rvert|rVert|rangle|rceil|rfloor|rho|varrho|rule|"
    r"to|text|textbf|textit|textrm|texttt|times|theta|vartheta|tau|tan|tanh|tilde|widetilde|triangle|top|tabular|tabularx|tikzpicture|tikz"
)

def pre_escape_json_latex(json_str: str) -> str:
    """Bảo vệ toàn vẹn 100% công thức LaTeX trước khi giải mã JSON, chống nuốt backslash và lỗi ASCII control."""
    s = json_str.replace('\ufeff', '').replace('\u200b', '').replace('\u00a0', ' ')
    # 1. Thoát toàn bộ các lệnh LaTeX trùng ký tự đầu với escape của JSON (\f, \b, \n, \r, \t)
    s = re.sub(rf'(?<!\\)\\({_LATEX_JSON_COLLISION_CMDS})(?![a-zA-Z])', r'\\\\\1', s)
    # 2. Thoát mọi backslash cô lập (bỏ 'u' đơn để bảo vệ \uparrow, \underline, \underset...)
    s = re.sub(r'(?<!\\)\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})', r'\\\\', s)
    return s


def safe_json_loads(raw):
    if not isinstance(raw, str) or not raw.strip():
        raise ValueError("AI không trả nội dung JSON.")
    value = raw.strip()

    # BƯỚC 1: Bóc tách markdown codeblock
    if value.startswith("```"):
        value = re.sub(r"^```(?:json)?\s*", "", value, flags=re.IGNORECASE)
        value = re.sub(r"\s*```$", "", value)

    # BƯỚC 2: Trích xuất chính xác khối JSON nằm giữa { đầu tiên và } cuối cùng
    first_brace = value.find('{')
    last_brace = value.rfind('}')
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        value = value[first_brace:last_brace+1]

    # BƯỚC 3: Tiền xử lý thoát backslash LaTeX và khử ký tự ngoại lai
    value = pre_escape_json_latex(value)

    # LẦN THỬ 1: Parse an toàn với chuỗi đã bảo vệ escape
    try:
        data = json.loads(value, strict=False)
        return fix_broken_latex_escapes(data)
    except Exception:
        pass



    # LẦN THỬ 2: Tự động sửa dấu nháy kép nội suy bên trong nội dung câu hỏi

    try:

        res_chars = []

        in_str = False

        esc = False

        for i, ch in enumerate(value):

            if ch == '\\' and not esc:

                esc = True; res_chars.append(ch); continue

            if ch == '"' and not esc:

                before = value[:i].rstrip()

                after = value[i+1:].lstrip()

                is_start = before.endswith(('{', '[', ',', ':', '"')) or before == ''

                is_end = after.startswith(('}', ']', ',', ':')) or after == ''

                if in_str:

                    if is_end: in_str = False; res_chars.append('"')

                    else: res_chars.append('\\"')

                else:

                    in_str = True; res_chars.append('"')

            else:

                res_chars.append(ch)

            esc = False

        data = json.loads("".join(res_chars), strict=False)

        return fix_broken_latex_escapes(data)

    except Exception:

        pass



    # LẦN THỬ 3: Khắc phục backslash chưa thoát và dấu phẩy thừa (Chuẩn hóa công thức toán LaTeX)

    v_clean = re.sub(r',\s*([\}\]])', r'\1', value)

    # Xử lý các lệnh LaTeX bắt đầu bằng ký tự escape của JSON (\f, \t, \b, \n, \r)

    v_escaped = re.sub(r'(?<!\\)\\(frac|dfrac|to|times|theta|tau|tan|text|beta|bar|binom|begin|bf)\b', lambda m: r'\\' + m.group(1), v_clean)

    # Thoát tất cả các backslash cô lập không thuộc escape sequence hợp lệ của JSON

    v_escaped = re.sub(r'(?<!\\)\\(?!["\\/bfnrtu]|u[0-9a-fA-F]{4})', r'\\\\', v_escaped)

    try:

        data = json.loads(v_escaped, strict=False)

        return fix_broken_latex_escapes(data)

    except Exception:

        pass



    # LẦN THỬ 4: Cân bằng ngoặc đóng LIFO (Stack-based) nếu bị cắt ngắn do cạn Token

    stack = []

    in_str = False

    esc = False

    for ch in v_escaped:

        if ch == '\\' and in_str:

            esc = not esc

            continue

        if ch == '"' and not esc:

            in_str = not in_str

            continue

        esc = False

        if not in_str:

            if ch == '{':

                stack.append('}')

            elif ch == '[':

                stack.append(']')

            elif ch in ('}', ']'):

                if stack and stack[-1] == ch:

                    stack.pop()



    closing = '"' if in_str else ''

    while stack:

        closing += stack.pop()

    balanced = re.sub(r',\s*$', '', v_escaped.rstrip()) + closing

    balanced = re.sub(r',\s*([\}\]])', r'\1', balanced)

    try:

        data = json.loads(balanced, strict=False)

        return fix_broken_latex_escapes(data)

    except json.JSONDecodeError as final_err:
        raise ValueError(f"JSON của AI chưa hợp lệ tại dòng {final_err.lineno}, cột {final_err.colno}. Hãy thử lại hoặc bấm khởi tạo lại đề.")
