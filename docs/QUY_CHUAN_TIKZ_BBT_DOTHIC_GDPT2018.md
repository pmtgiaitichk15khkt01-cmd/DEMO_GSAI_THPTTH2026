# BỘ QUY CHUẨN KỸ THUẬT TIKZ VECTOR, BẢNG XÉT DẤU (BXD), BẢNG BIẾN THIÊN (BBT) VÀ ĐỒ THỊ GIẢI TÍCH
## Chương trình Giáo dục Phổ thông 2018 - SGK Kết Nối Tri Thức với Cuộc Sống
*Dự án Nghiên cứu Khoa học Kỹ thuật 2026 - Tác giả Thầy Phạm Minh Trí*

---

## 1. NGUYÊN TẮC CỐT LÕI
1. **Tính sư phạm chuẩn mực 100%:** Mọi bảng xét dấu (BXD), bảng biến thiên (BBT) và đồ thị toán học do Hệ thống AI sinh ra bắt buộc phải tuân theo đúng mẫu chuẩn LaTeX / TikZ / pgfplots sư phạm, tương thích tuyệt đối khi biên dịch trên Overleaf cũng như hiển thị trực tiếp trên Giao diện Gia Sư AI.
2. **Thích ứng Đa chế độ (Light Mode & Dark Mode):** BBT và BXD hiển thị trên Web phải tự động tương thích với Chế độ Tối (Dark Mode) của học sinh, đảm bảo chỉ số x, y', y, nghiệm, dấu (+, -), vạch kép tiệm cận đứng (||) và phân số có độ tương phản cao (Contrast Ratio > 7:1 theo WCAG AAA), sắc nét, không bị chìm.

---

## 2. QUY CHUẨN BẢNG XÉT DẤU (BXD) VỚI GÓI `tkz-tab`
Sử dụng gói `tkz-tab` với lệnh khởi tạo `\tkzTabInit` và lệnh xét dấu `\tkzTabLine`.

### Trường hợp 1: Hàm bậc ba $y = ax^3 + bx^2 + cx + d$ có hệ số $a > 0$
Đạo hàm $y' = 3ax^2 + 2bx + c$ có 2 nghiệm phân biệt $x_1 < x_2$.
Quy tắc xét dấu "trong trái, ngoài cùng": `+, 0, -, 0, +`.
```latex
\begin{tikzpicture}
    \tkzTabInit[nocadre, lgt=1.5, espcl=3]
        {$x$/0.7, $y'$/0.7} % Khai báo 2 dòng: x và y'
        {$-\infty$, $x_1$, $x_2$, $+\infty$} % Các cột giá trị của x
    \tkzTabLine{,+,0,-,0,+,} % Dòng xét dấu cho y'
\end{tikzpicture}
```

### Trường hợp 2: Hàm bậc ba có hệ số $a < 0$
Quy tắc xét dấu "trong trái, ngoài cùng": `-, 0, +, 0, -`.
```latex
\begin{tikzpicture}
    \tkzTabInit[nocadre, lgt=1.5, espcl=3]
        {$x$/0.7, $y'$/0.7} % Khai báo 2 dòng: x và y'
        {$-\infty$, $x_1$, $x_2$, $+\infty$} % Các cột giá trị của x
    \tkzTabLine{,-,0,+,0,-,} % Dòng xét dấu cho y'
\end{tikzpicture}
```

### Bảng biến thiên đầy đủ 3 dòng (Hàm bậc ba $a > 0$):
```latex
\begin{tikzpicture}
    \tkzTabInit[nocadre, lgt=1.5, espcl=2.5]
        {$x$/0.7, $y'$/0.7, $y$/2}
        {$-\infty$, $x_1$, $x_2$, $+\infty$}
    \tkzTabLine{,+,0,-,0,+,}
    \tkzTabVar{-/ $-\infty$, +/ $y_1$, -/ $y_2$, +/ $+\infty$}
\end{tikzpicture}
```

---

## 3. QUY CHUẨN ĐÁNH DẤU VÀ TÔ MIỀN HÌNH HỌC (TIKZ & TKZ-EUCLIDE)

### 3.1. Đánh dấu đoạn thẳng bằng nhau
```latex
\tkzMarkSegments[mark=||](A,B A,C)
```

### 3.2. Đánh dấu góc vuông
```latex
\tkzMarkRightAngles[size=0.17](A,B,C)
```

### 3.3. Đánh dấu góc tròn
```latex
\tkzMarkAngles[size=0.7cm,arc=ll,mark=|](A,B,C)
```

### 3.4. Gán nhãn cho góc
```latex
\tkzLabelAngles[pos=1,rotate=30](A,B,C){$\alpha$}
```

### 3.5. Tô miền đa giác
```latex
\tkzFillPolygon[color=green!80, fill opacity=0.5](A,B,C)
```

### 3.6. Tô miền hình phẳng / Tích phân
```latex
\fill[pattern=north east lines,opacity=0.8] plot[domain=-1:3](\x,{(\x)^3-3*(\x)^2-\x+3})--cycle;
```

---

## 4. QUY CHUẨN LATEX ĐỒ THỊ HÀM SỐ CHUẨN BỘ GD&ĐT

### 4.1. Đồ thị hàm bậc hai (Parabol Lớp 10)
```latex
\begin{tikzpicture}[scale=1,>=stealth, font=\footnotesize, line join=round, line cap=round]
	\def\a{1} \def\b{-4} \def\c{3} % Hệ số
	\def\xmin{-6} \def\xmax{6}
	\def\ymin{-7} \def\ymax{7}
	\draw[color=gray!50,dashed] (\xmin,\ymin) grid (\xmax,\ymax);
	\draw[->] (\xmin,0)--(\xmax,0) node [below]{$x$};
	\draw[->] (0,\ymin)--(0,\ymax) node [left]{$y$};
	\node at (0,0) [below left]{$O$};
	\clip (\xmin+0.1,\ymin+0.1) rectangle (\xmax-0.5,\ymax-0.1);
	\draw[smooth,samples=300] plot(\x,{\a*(\x)^2+\b*(\x)+\c});
\end{tikzpicture}
```

### 4.2. Đồ thị hàm bậc ba (Lớp 12)
```latex
\begin{tikzpicture}[scale=1,>=stealth, font=\footnotesize, line join=round, line cap=round]
	\def\a{1} \def\b{-6} \def\c{9} \def\d{1} % Hệ số
	\def\xmin{-6} \def\xmax{6}
	\def\ymin{-8} \def\ymax{8} 
	\draw[color=gray!50,dashed] (\xmin,\ymin) grid (\xmax,\ymax); 
	\draw[->] (\xmin,0)--(\xmax,0) node [below]{$x$};
	\draw[->] (0,\ymin)--(0,\ymax) node [left]{$y$};
	\node at (0,0) [below left]{$O$};
	\clip (\xmin+0.1,\ymin+0.1) rectangle (\xmax-0.5,\ymax-0.1);
	\draw[smooth,samples=300] plot(\x,{\a*(\x)^3+\b*(\x)^2+\c*(\x)+\d});
\end{tikzpicture}
```

### 4.3. Đồ thị hàm bậc bốn trùng phương (Chỉ dùng khi có yêu cầu đặc biệt)
```latex
\begin{tikzpicture}[scale=1,>=stealth, font=\footnotesize, line join=round, line cap=round]
	\def\a{1} \def\b{-4} \def\c{3} % Hệ số
	\def\xmin{-6} \def\xmax{6}
	\def\ymin{-8} \def\ymax{8} 
	\draw[color=gray!50,dashed] (\xmin,\ymin) grid (\xmax,\ymax); 
	\draw[->] (\xmin,0)--(\xmax,0) node [below]{$x$};
	\draw[->] (0,\ymin)--(0,\ymax) node [left]{$y$};
	\node at (0,0) [below left]{$O$};
	\clip (\xmin+0.1,\ymin+0.1) rectangle (\xmax-0.5,\ymax-0.1);
	\draw[smooth,samples=300] plot(\x,{\a*(\x)^4+\b*(\x)^2+\c});
\end{tikzpicture}
```

### 4.4. Đồ thị hàm phân thức bậc nhất / bậc nhất $y = \frac{ax+b}{cx+d}$
Tách làm 2 nhánh đồ thị ngắt quãng tại tiệm cận đứng $x = -\frac{d}{c}$, vẽ tiệm cận đứng và tiệm cận ngang nét đứt:
```latex
\begin{tikzpicture}[scale=1,>=stealth, font=\footnotesize, line join=round, line cap=round]
	\def\a{2} \def\b{-1} \def\c{1} \def\d{1} % Hệ số
	\def\xmin{-7} \def\xmax{7}
	\def\ymin{-8} \def\ymax{8}
	\draw[color=gray!50,dashed] (\xmin,\ymin) grid (\xmax,\ymax);
	\draw[->] (\xmin,0)--(\xmax,0) node [below]{$x$};
	\draw[->] (0,\ymin)--(0,\ymax) node [left]{$y$};
	\node at (0,0) [below left]{$O$};
	\clip (\xmin+0.1,\ymin+0.1) rectangle (\xmax-0.1,\ymax-0.1);
	\draw[smooth,samples=300,domain=\xmin:(-\d/\c-0.1)] plot(\x,{(\a*(\x)+\b)/(\c*(\x)+\d)});
	\draw[smooth,samples=300,domain=(-\d/\c+0.1:\xmax)] plot(\x,{(\a*(\x)+\b)/(\c*(\x)+\d)});
	\draw[dashed] (-\d/\c,\ymin)--(-\d/\c,\ymax); % Tiệm cận đứng
	\draw[dashed] (\xmin,\a/\c)--(\xmax,\a/\c);   % Tiệm cận ngang
\end{tikzpicture}
```

### 4.5. Đồ thị hàm phân thức bậc hai / bậc nhất $y = \frac{ax^2+bx+c}{dx+e}$ (pgfplots)
Sử dụng gói `pgfplots` với `axis lines=middle`, hiển thị tiệm cận đứng và tiệm cận xiên nét đứt màu đỏ:
```latex
\begin{tikzpicture}
    \begin{axis}[
        grid=major,
        grid style={dashed, gray!50},
        axis lines=middle,
        xlabel=$x$,
        ylabel=$y$,
        xmin=-10, xmax=5,
        ymin=-15, ymax=15,
        samples=200,
        clip=true,
    ]
        \node[below left, font=\small] at (axis cs:0,0) {$O$};
        % Nhánh 1 bên trái tiệm cận đứng x = -2
        \addplot[blue, thick, no markers, domain=-10:-2.01] {(-x^2+2*x-1)/(x+2)};
        % Nhánh 2 bên phải tiệm cận đứng x = -2
        \addplot[blue, thick, no markers, domain=-1.99:5] {(-x^2+2*x-1)/(x+2)};
        % Tiệm cận đứng x = -2 (màu đỏ, nét đứt)
        \addplot[dashed, red, thick, no markers] coordinates {(-2, -15) (-2, 15)};
        % Tiệm cận xiên y = -x + 4 (màu đỏ, nét đứt)
        \addplot[dashed, red, thick, no markers, domain=-10:5] {-x+4};
    \end{axis}
\end{tikzpicture}
```

### 4.6. Đồ thị hàm lũy thừa
```latex
\begin{tikzpicture}[scale=1,>=stealth, font=\footnotesize, line join=round, line cap=round]
	\def\xmax{6} \def\ymax{7}
	\draw[color=gray!50,dashed] (-0.9,-0.9) grid (\xmax,\ymax);
	\draw[->] (-0.9,0)--(\xmax,0) node [below]{$x$};
	\draw[->] (0,-0.9)--(0,\ymax) node [left]{$y$};
	\node at (0,0) [below left]{$O$};
	\clip (-0.9,-0.9) rectangle (\xmax-0.5,\ymax-0.2);
	\draw[smooth,samples=300,domain=0:\xmax] plot(\x,{(\x)^2.5});
	\draw[smooth,samples=300,domain=0:\xmax] plot(\x,{\x});
	\draw[smooth,samples=300,domain=0:\xmax] plot(\x,{(\x)^0.3});
	\draw[smooth,samples=300,domain=0:\xmax] plot(\x,{(\x)^(-1.3)});
	\draw[dashed] (1,0) node[below]{$1$}--(1,1)--(0,1)node[left]{$1$};
\end{tikzpicture}
```

---

## 5. KHAI BÁO GÓI BẮT BUỘC TRÊN OVERLEAF LATEX
Khi xuất mã nguồn đề thi Overleaf (`.tex`), tài liệu phải luôn bao gồm đầy đủ các gói:
```latex
\usepackage{tikz,pgfplots}
\usepackage{tkz-tab}
\usepackage{tkz-euclide}
\usetikzlibrary{patterns,calc,angles,quotes}
\pgfplotsset{compat=1.18}
```
