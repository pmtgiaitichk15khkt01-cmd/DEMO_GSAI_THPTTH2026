# 🛠️ NHẬT KÝ BẢN VÁ HỆ THỐNG GSAI - THPT 2026

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
