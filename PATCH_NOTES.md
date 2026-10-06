# 🛠️ NHẬT KÝ BẢN VÁ HỆ THỐNG GSAI - THPT 2026

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
