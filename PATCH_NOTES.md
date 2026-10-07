# 🛠️ NHẬT KÝ BẢN VÁ HỆ THỐNG GSAI - THPT 2026

## 📌 LẦN CẬP NHẬT THỨ 11 (CHÍNH THỨC): NGÀY 07/10/2026 - 12:45:00 (GMT+7)
### 🛡️ 1. Nâng Cấp Hệ Thống Điều Phối "BẤT TỬ" 24/7 (Immortal Key & Model Rotation)
- **Tối ưu hóa Bậc thang Mô hình (Optimal Model Hierarchy):**
  - Đưa `gemini-3-flash-preview` lên nhóm ưu tiên cao ngay sau bộ 3 siêu tốc (`3.6-flash`, `3.5-flash-lite`, `3.1-flash-lite`), giữ `3.5-flash` ở vị trí chiến lược.
  - Loại bỏ hoàn toàn các mã lỗi thời đã bị đóng cổng API (`gemini-2.5-flash`, `gemini-2.5-flash-lite`) để không tiêu tốn thời gian chờ.
- **Cơ chế Ghi nhớ Key Đắc Lực (`st.session_state.working_key`):**
  - Khi một Key trong nhóm 5 Key thực thi thành công, hệ thống tự động ghim Key đó làm vị trí #1 cho toàn bộ các lượt truy vấn tiếp theo trong phiên. Học sinh nhận kết quả ngay trong 1-2 giây mà không cần dò lặp lại.
  - Tự động xoay vòng sang Key kế tiếp ngay khi gặp mã `429 (RESOURCE_EXHAUSTED)` hoặc tự động loại trừ Key lỗi quyền (`401/403`).
- **Nạp Nhóm 5 Khóa Siêu Cường vào Cấu Hình Mặc Định (`secrets.toml`):**
  - Tích hợp 5 Key đã kiểm định sống 100% với hạn ngạch dồi dào, đảm bảo hệ thống chịu tải liên tục cho toàn trường.

---

## 📌 LẦN CẬP NHẬT THỨ 10 (CHÍNH THỨC): NGÀY 06/10/2026 - 23:20:00 (GMT+7)
### ⚡ 1. Khắc Phục Triệt Để Lỗi 503 UNAVAILABLE & Tối Ưu Hóa Điều Phối Gemini Bền Bỉ
- **Nguyên nhân cốt lõi phát hiện:**
  - Máy chủ Google AI Studio đang ghi nhận đột biến lưu lượng tải (High Demand Spike) trên một số model nhất định (`gemini-3.8-flash`, `gemini-3.5-flash`, `gemini-3-flash-preview`) gây lỗi `503 UNAVAILABLE`.
  - Các model thuộc thế hệ cũ (`gemini-2.5-flash`, `gemini-2.0-flash`, `gemini-1.5-flash`) đã bị đóng cổng API cho tài khoản mới dẫn tới lỗi `404 NOT_FOUND`.
  - Thứ tự fallback cũ vô tình bỏ quên các model đang hoạt động 100% trơn tru, khỏe khoắn với độ trễ cực thấp.
- **Giải pháp Điều phối Đa tầng Thông minh (Resilient Hierarchy Cascade):**
  - **Tối ưu danh sách `ALL_GEMINI_MODELS`:** Ưu tiên đưa các model đã kiểm chứng hoạt động tức thì lên đầu hàng đợi:
    1. `gemini-3.6-flash` (Hoạt động hoàn hảo, phản hồi siêu tốc)
    2. `gemini-3.5-flash-lite` (Hoạt động hoàn hảo, tải nhẹ, tiết kiệm tài nguyên)
    3. `gemini-3.1-flash-lite` (Hoạt động hoàn hảo, ổn định)
    4. `gemini-flash-lite-latest` (Dự phòng chuẩn của Google)
    5. `gemini-3.7-flash` & `gemini-3.5-flash` & `gemini-3.8-flash`
    6. `gemini-flash-latest` & `gemini-3-flash-preview` & `gemini-3.1-pro-preview`
  - **Loại bỏ triệt để các endpoint 404 đã khai tử:** Xóa vĩnh viễn `gemini-2.5-flash`, `gemini-2.0-flash`, `gemini-1.5-flash` khỏi danh sách để cơ chế fallback không bị nghẽn thời gian chờ.
  - **Bảo toàn 100% triết lý Socratic & Bút tích Giáo viên:** Tất cả tính năng chấm "Face to Face", vẽ mực đỏ check VAR, tick xanh OK chuẩn chỉ, đàm thoại đa môn lớp 6–12 vận hành hoàn hảo không gián đoạn.

---

## 📌 LẦN CẬP NHẬT THỨ 9 (CHÍNH THỨC): NGÀY 06/10/2026 - 23:00:00 (GMT+7)
### 🖋️ 1. Bút Tích Chấm Bài Trực Tiếp "Face to Face" Trên Ảnh (Trạm 2)
- **Vẽ trực tiếp Bút tích Giáo viên lên Ảnh bài làm (`annotate_student_work`):**
  - **Dòng Tick xanh OK chuẩn chỉ:** Vẽ khung viền xanh lá `#10b981` kèm huy hiệu `✅ [OK CHUẨN CHỈ]` cho các dòng/bước biến đổi đúng, lập luận chặt chẽ.
  - **Dòng Mực đỏ Check VAR khét lẹt:** Khoanh vùng bằng viền đỏ rực `#ef4444` kèm huy hiệu `🔴 [CHECK VAR KHÉT LẸT: Chỗ khuất tất]` cho các dòng có lỗi sai, thiếu điều kiện xác định hoặc ngộ nhận.
- **Trực quan hóa hình ảnh chấm cụ thể:** Hiển thị trực tiếp ảnh bài làm đã được chấm "Face to Face" trên giao diện để học sinh nhìn thấy rõ nét từng bước nhận xét của Thầy.
- **Cấu trúc nhận xét Socratic từng dòng minh bạch:** Tách bạch rõ 3 phần: (1) Check các bước làm đúng OK, (2) Đánh dấu chỗ khuất tất cần lưu ý, (3) Câu hỏi gợi mở Socratic dẫn dắt học sinh tự tay sửa lại bài.

---

## 📌 LẦN CẬP NHẬT THỨ 8 (CHÍNH THỨC): NGÀY 06/10/2026 - 22:35:00 (GMT+7)
### 📖 1. Chống Ảo Giác Số Trang SGK (Trạm 1 - Anti-Hallucination Guardrail)
- **Cơ chế nhận diện thông minh (Regex Guardrail):** Tự động phát hiện khi học sinh nhập truy vấn có chứa `Trang [số]` hoặc `Page [số]`.
- **Chỉ dẫn sư phạm trực quan:** Hiển thị cảnh báo giải thích rõ độ lệch số trang giữa các đợt in/tái bản của NXB Giáo Dục Việt Nam (2024, 2025, 2026); khuyến nghị nhập kèm tên chuyên đề, hoặc mở mục *📚 SGK Điện Tử* ở thanh bên, hoặc chụp ảnh trang sách nộp vào Trạm 2.
- **Kỷ luật AI trong Prompt:** Nghiêm cấm mô hình khẳng định bừa số trang vật lý nếu không có ngữ liệu chắc chắn 100%, bảo đảm bám sát Khung phân phối chương trình môn học chuẩn CT GDPT 2018.

### 📤 2. Tối Ưu Nộp Bài 1 Chạm & Hỗ Trợ Nộp Nhiều Trang Bài Làm (Trạm 2)
- **1 Nút Gửi Bài duy nhất (`st.popover`):** Giao diện tinh gọn, không phân mảnh tab. Nhấn nút mở ra khung chứa cả 2 phương thức để học sinh lựa chọn:
  - *📸 Cách 1:* Chụp trực tiếp bằng Camera (1 chạm kích hoạt).
  - *📁 Cách 2:* Tải file ảnh có sẵn từ thiết bị (hỗ trợ JPG, PNG, WEBP, HEIC của iPhone/Samsung).
- **Hỗ trợ nộp nhiều trang bài làm (Multi-page Submission):**
  - *Camera:* Cho phép chụp từng trang và bấm `➕ Thêm trang này vào bài làm` để tích lũy liên tiếp Trang 1, Trang 2, Trang 3... Có bộ đếm số trang và nút xóa làm lại.
  - *Tải file:* Kích hoạt `accept_multiple_files=True`, cho phép chọn cùng lúc nhiều bức ảnh từ máy.
  - *Lưới xem trước đa trang (Multi-page Grid Preview):* Tự động hiển thị các trang bài làm theo thứ tự rõ ràng trước khi gửi.
  - *Phân tích Multimodal toàn diện:* Toàn bộ danh sách ảnh bài làm được gửi đồng thời sang Gemini để Thầy Socratic đọc bài xuyên suốt từ trang đầu đến trang cuối.

---

## 📌 LẦN CẬP NHẬT THỨ 7 (CHÍNH THỨC): NGÀY 06/10/2026 - 21:00:00 (GMT+7)
### 📐 1. Nâng Cấp Toàn Diện Phòng Thí Nghiệm Ảo (Virtual Lab) - Mô Phỏng Không Gian 3D (Toán 11 & 12)
- **Khắc phục lỗi nhận diện nhầm Sơ đồ tư duy (Mermaid):**
  - Trước đây: Các câu hỏi tóm tắt lý thuyết, trắc nghiệm, tự luận về Hình học không gian (hình chóp, lăng trụ, quan hệ song song) bị xếp nhầm vào Mermaid do thiếu định nghĩa phân loại.
  - Sau bản vá: Bổ sung định dạng mô hình chuyên biệt `geometry_3d` trực tiếp trong `lab_prompt` và `available_labs`. Khi đề cập đến hình chóp $S.ABCD$, $S.ABC$, lăng trụ tam giác, hình hộp, hoặc quan hệ song song $d_1 \parallel d_2$, AI tự động xuất mô hình Plotly 3D tương tác.
- **Hỗ trợ đầy đủ các khối hình học không gian chuẩn SGK:**
  - Hình chóp tứ giác $S.ABCD$ (đáy bình hành, đỉnh $S$, trục đối xứng).
  - Hình chóp tam giác / tứ diện $S.ABC$.
  - Hình hộp chữ nhật / hình lập phương $ABCD.A'B'C'D'$.
  - Hình lăng trụ tam giác $ABC.A'B'C'$.
  - Hai đường thẳng song song trong không gian $d_1 \parallel d_2$.
  - Phân biệt nét đứt (dashed edges) cho các cạnh khuất và nét liền cho các cạnh nhìn thấy, kèm nhãn đỉnh rõ ràng.

### 🔄 2. Khắc Phục Triệt Để Hiện Tượng Khối Tròn Xoay 3D Bị Bẹp Dí (`revolve_ox`)
- **Nguyên nhân cốt lõi:** Trước đây Plotly cấu hình `aspectmode='data'`, khiến các trục tọa độ bị co giãn không đồng đều theo độ lệch số liệu giữa miền trục $Ox$ và biên độ hàm số $Oy, Oz$.
- **Giải pháp tối ưu chuẩn toán học:**
  - Chuyển sang `aspectmode='cube'` để đảm bảo tỉ lệ đồng dạng 1:1:1 giữa cả ba trục.
  - Sử dụng bán kính thực $r(x) = |f(x)|$ cho lưới tham số tròn xoay quanh trục $Ox$.
  - Khóa khoảng đối xứng đối với trục $Oy$ và $Oz$ theo bán kính cực đại $R_{\max}$, triệt tiêu 100% hiện tượng biến dạng méo mó hoặc bẹp dí.

### 📈 3. Bổ Sung Đồ Thị Tương Tác Hàm Số Mũ & Hàm Số Lôgarit Kèm Thanh Trượt (Toán 11 & 12)
- **Hàm số Mũ (`func_exp`):** Dạng tổng quát $y = k \cdot a^x + c$. Hỗ trợ cơ số Euler $e \approx 2.71828$ và cơ số tùy chọn qua thanh trượt. Trực quan hóa đường tiệm cận ngang $y = c$, tọa độ giao điểm và bảng tính biến thiên.
- **Hàm số Lôgarit (`func_log`):** Dạng tổng quát $y = k \cdot \log_a(x) + c$. Hỗ trợ lôgarit tự nhiên $\ln(x)$ và cơ số $a$ tùy chọn. Trực quan hóa miền xác định $x > 0$, đường tiệm cận đứng $x = 0$, điểm đặc biệt $(1, c)$ và đồ thị sắc nét.

---

## 📌 LẦN CẬP NHẬT THỨ 6 (CHÍNH THỨC): NGÀY 06/10/2026 - 20:30:00 (GMT+7)
### 🏛️ 1. Thổi Hồn "System Instruction Sư Phạm Thượng Đẳng" Cho Toàn Bộ 11 Môn Học (Lớp 6 - 12)
- **Chuẩn hóa triết lý Socratic Maieutics (Thuật đỡ đẻ tri thức):** Người Thầy AI trí tuệ, sáng suốt, ân cần, tuyệt đối không lặp lại lý thuyết như con vẹt máy móc, không giải hộ hay đưa sẵn đáp số.
- **Thích ứng chuyên sâu theo từng bản sắc bộ môn:**
  - *Toán học:* Dẫn dắt tư duy logic, trực quan không gian 3D, đào sâu bản chất điều kiện xác định.
  - *Vật lý / Hóa học / Sinh học / KHTN:* Đi từ hiện tượng tự nhiên, cơ chế phản ứng, bản chất thực nghiệm, 100% danh pháp quốc tế IUPAC & hệ SI.
  - *Ngữ văn:* Khai phóng cảm thức thẩm mỹ, đặc trưng thể loại ngoài SGK, rèn tư duy NLXH & NLVH độc lập.
  - *Tiếng Anh:* Tương tác văn phong tự nhiên chuẩn CEFR, giải nghĩa từ vựng theo ngữ cảnh sống động.
  - *Lịch sử, Địa lý, Lịch sử & Địa lý:* Phân tích quan hệ nhân quả, dòng chảy thời đại, không gian lãnh thổ và bài học thực tiễn.
  - *Tin học, GDCD, GDKT-PL:* Rèn tư duy giải thuật, tình huống pháp lý và phẩm chất công dân kỷ nguyên số.
- **Quy chuẩn hiển thị:** 100% Text & công thức $\text{\LaTeX}$ chuẩn mực ($...$), triệt tiêu các đoạn âm thanh/voice không cần thiết để tạo môi trường học tập tĩnh tâm cao độ.

### 💬 2. Tích Hợp Micro-Socratic Chatbox Đàm Thoại Ngữ Cảnh Sau Phần 1 (Trạm 1)
- Ngay sau khi đọc Tóm tắt cốt lõi (Phần 1), xuất hiện khung đối thoại Socratic mở đầu bằng câu hỏi khơi gợi bản chất của Thầy AI.
- Học sinh đàm thoại, giải đáp thắc mắc lý thuyết đến khi thực sự hiểu sâu rồi mới chuyển xuống làm Trắc nghiệm Phần 2 và Tự luận Phần 3.
- Khép kín ngữ cảnh trong `tram1_chat_history`, tự động làm mới khi đổi bài học.

### 🎯 3. Bộ Kiểm Soát Xung Đột Cấp Lớp Thông Minh (Smart Grade-Conflict Resolver)
- Tự động phát hiện khi học sinh ở không gian lớp này nhưng nhập bài học của lớp khác (ví dụ: đang ở Lớp 12 nhưng hỏi bài Lớp 11).
- Hiển thị hộp thoại Sư phạm ân cần với 2 lựa chọn: **Bấm 1-Click chuyển nhanh sang đúng Lớp** hoặc **Tự động biên soạn theo định hướng Ôn tập liên thông nền tảng** bổ trợ kiến thức.

### 📸 4. Khắc Phục Triệt Để Lỗi Nộp Ảnh Tự Luận & Bổ Sung Camera 1 Chạm (Trạm 2)
- **Tích hợp Camera 1 chạm (`st.camera_input`):** Học sinh dùng điện thoại chỉ cần bấm chụp trực tiếp, ảnh tự động xuất chuẩn PNG/JPEG gửi thẳng cho Thầy AI, triệt tiêu 100% lỗi định dạng.
- **Xử lý toàn diện ảnh HEIC:** Bổ sung thư viện `pillow-heif` vào `requirements.txt` và `app.py`, hỗ trợ mở trực tiếp file ảnh `.heic` từ iPhone/Samsung, kèm cảnh báo điều hướng thân thiện.

---

## 📌 LẦN CẬP NHẬT THỨ 5 (CHÍNH THỨC): NGÀY 06/10/2026 - 16:55:00 (GMT+7)
### 🐛 1. Khắc Phục Triệt Để Lỗi Khai Báo Biến `NameError: BIGDATA_CURRICULUM`
- **Nguyên nhân đã xử lý:** Từ điển `BIGDATA_CURRICULUM` trước đây được định nghĩa ở phần sau của file (trước Trạm 3), trong khi Trạm 1 được thực thi trước và gọi đến biến này ở dòng 2120 $\rightarrow$ Gây lỗi `NameError` trên môi trường Streamlit.
- **Giải pháp chuẩn hóa:** Di chuyển toàn bộ khối dữ liệu `BIGDATA_CURRICULUM` lên vị trí khai báo hằng số cơ sở dữ liệu ngay trước khối các Trạm học tập (trước dòng `station_labels`).
- **Cam kết bảo tồn dữ liệu:** Toàn bộ 100% cấu trúc ma trận chuyên đề của tất cả các môn (Toán, Lý, Hóa, Sinh, Văn, Sử, Địa, Tin học, GDKT-PL, KHTN, GDCD) từ Lớp 6 đến Lớp 12 được giữ nguyên vẹn không mất bất kỳ ký tự nào.
- **Kết quả:** Trạm 1 và Trạm 3 truy cập dữ liệu mượt mà, triệt tiêu 100% lỗi `NameError`.

---

## 📌 LẦN CẬP NHẬT THỨ 4: NGÀY 06/10/2026 - 16:20:00 (GMT+7)
### 🧠 1. Hệ Thống Kiểm Soát Xung Đột Sư Phạm Thông Minh (Smart Pedagogical Conflict Validator)
- Tự động phát hiện và hiển thị gợi ý sư phạm ân cần khi người dùng nhập yêu cầu xung đột quy chuẩn Bộ GD&ĐT:
  - Môn Ngữ văn: Hướng dẫn chuẩn 100% Tự luận (Đọc hiểu 4đ + Viết 6đ) theo QĐ 764. Nếu nhập tên tác phẩm trong SGK cũ $\rightarrow$ Gợi ý văn bản mới ngoài SGK chống học tủ.
  - Môn Toán học: Nhắc nhở quy chuẩn CT GDPT 2018 (đã loại bỏ hàm bậc 4 trùng phương) và chuyển sang hàm bậc ba/phân thức.
  - Môn KHXH & Tin học: Nhắc nhở quy chuẩn QĐ 764 chỉ có Phần I (24 câu) và Phần II (4 câu Đ/S).
### 🏛️ 2. Mô Hình Phân Tầng Mệnh Lệnh (Hierarchical Constraint Framework)
- Thiết lập 3 tầng thứ bậc: Cấp 1 (Pháp chế Bộ GD&ĐT bất biến), Cấp 2 (Nguyện vọng thích ứng của GV & HS), Cấp 3 (Đầu ra JSON Schema bền bỉ trên mọi dòng AI Gemini).

---

## 📌 LẦN CẬP NHẬT THỨ 3: NGÀY 06/10/2026 - 16:00:00 (GMT+7)
- Đồng bộ động Khối lớp Trạm 1 từ `BIGDATA_CURRICULUM` (chọn Lớp 9 hiện bài Lớp 9).
- Thiết lập rào chắn chống ảo giác số trang in SGK, liên kết trực quan với kho SGK Điện tử NXBGD ở thanh bên trái.
- Ngữ văn 100% ngoài SGK; Tiếng Anh chuẩn hóa ma trận 40 câu CEFR / THPT 2026.

---

## 📌 LẦN CẬP NHẬT THỨ 2: NGÀY 06/10/2026 - 15:15:00 (GMT+7)
- Chuẩn hóa Khảo thí Độc lập (Trạm 3) theo QĐ 764/QĐ-BGDĐT cho tất cả các môn.
- Nâng cấp Phòng Lab 3D Plotly khép kín (Toán khối tròn xoay, Oxyz) và Sơ đồ tư duy D3/Mermaid cho môn Xã hội.

---

## 📌 LẦN CẬP NHẬT THỨ 1: NGÀY 06/10/2026 - 11:30:00 (GMT+7)
- Cập nhật pool model Gemini, tạo secrets.toml và chuẩn hóa requirements.txt.
