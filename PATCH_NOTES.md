# 🛠️ NHẬT KÝ BẢN VÁ HỆ THỐNG GSAI - THPT 2026

## 📌 LẦN CẬP NHẬT THỨ 2 (CHÍNH THỨC): NGÀY 06/10/2026 - 15:15:00 (GMT+7)
### 🏛️ 1. Chuẩn hóa Khảo thí Độc lập (Trạm 3) theo Pháp chế mới nhất của Bộ GD&ĐT (QĐ 764/QĐ-BGDĐT & TT 13/2026/TT-BGDĐT)
- **Môn Toán học:**
  - Cấu trúc: 12 câu TN nhiều lựa chọn (3,0 điểm) + 4 câu TN Đúng/Sai (4,0 điểm) + 6 câu Trả lời ngắn (3,0 điểm - 0,5đ/câu). Thời gian chuẩn: 90 phút.
  - Barem Đúng/Sai bậc thang chuẩn Bộ: Đúng 1 ý = 0,1đ; Đúng 2 ý = 0,25đ; Đúng 3 ý = 0,5đ; Đúng 4 ý = 1,0đ.
  - **Quy chuẩn Phiếu thi Phần III:** Áp dụng chặt chẽ quy định phiếu trả lời trắc nghiệm Bộ GD&ĐT có 4 cột tô đáp án. Khống chế học sinh điền tối đa 4 ký tự (`max_chars=4`), bao gồm cả dấu âm `-`, dấu phẩy `,` hoặc chấm `.`. AI prompt được thiết lập nghiêm cấm sinh đề có kết quả phân số hoặc dài hơn 4 ký tự.
- **Môn Ngữ văn:**
  - **100% Tự luận (Tuyệt đối không có trắc nghiệm):** Giao diện cấu hình ẩn hoàn toàn 3 ô nhập trắc nghiệm P.I/P.II/P.III; tự động kích hoạt card cấu trúc Tự luận chuẩn Bộ.
  - Cấu trúc: Phần I Đọc hiểu văn bản (4,0 điểm - Ngữ liệu mới ngoài SGK) + Phần II Viết (6,0 điểm: Đoạn văn NLXH 2,0 điểm khoảng 200 chữ + Bài văn NLVH 4,0 điểm).
  - Thời lượng: Chuẩn 120 phút.
- **Môn Khoa học Tự nhiên (Vật lý, Hóa học, Sinh học, KHTN):**
  - Cấu trúc: 18 câu TN (4,5 điểm) + 4 câu Đ/S (4,0 điểm) + 6 câu Trả lời ngắn (1,5 điểm - 0,25đ/câu). Thời gian: 50 phút. Tối đa 4 ký tự cho Phần III.
- **Môn Khoa học Xã hội & Tin học (Lịch sử, Địa lý, GDCD, GDKT-PL, Tin học):**
  - Cấu trúc: 24 câu TN (6,0 điểm) + 4 câu Đ/S (4,0 điểm). **Tuyệt đối KHÔNG có Phần III Trả lời ngắn** (chuẩn 100% QĐ 764). Thời gian: 50 phút.
- **Môn Tiếng Anh:**
  - Cấu trúc: 40 câu TN nhiều lựa chọn (10,0 điểm - 0,25đ/câu). 100% viết bằng tiếng Anh học thuật. Thời gian: 50 phút.

---

### 🔬 2. Phòng Lab Tương Tác Sư Phạm (Trạm 1) - Chuẩn Hóa Khoa Học 2D/3D & Phân Tuyến Liên Môn
- **Phân tuyến tuyệt đối môn Tự nhiên vs môn Xã hội:**
  - **Môn Xã hội (Ngữ văn, Lịch sử, Địa lý, GDKT-PL, GDCD, Tiếng Anh):** Ngăn chặn 100% không cho rơi vào đồ thị hàm số bậc 2, bậc 3 hay tích phân. Tự động kích hoạt Sơ đồ tư duy D3/Mermaid tóm tắt bản chất tri thức liên môn, chuẩn phong cách CEFR/KNTT.
  - **Môn Tự nhiên (Toán học, Vật lý, Hóa học, KHTN):**
    - **Khối tròn xoay 3D (Tích phân Ox):** Vẽ mặt tròn xoay Poly bằng Plotly Surface khép kín hoàn toàn ở 2 đầu tại 2 mặt cắt $x=a$ và $x=b$.
    - **Không gian Oxyz:** Dựng chuẩn gốc tọa độ $O(0,0,0)$, vectơ vị trí $\vec{OM}$ với mũi tên đậm, điểm hình chiếu vuông góc $M'$ lên $(Oxy)$ và tính toán tự động độ dài đại số $|\vec{OM}| = \sqrt{x^2+y^2+z^2}$.

---

### ⚡ 3. Tối Ưu Giải Thuật, API & Kiểm Thử Check VAR
- Dọn dẹp dòng gọi hàm duplicate `render_smart_lab(data)` ở Trạm 1.
- Hỗ trợ đầy đủ định dạng Gemini API Key mới bắt đầu bằng `AQ...` và `AIzaSy...`.
- Tối ưu re-render Plotly chart với dynamic keys.
- Vượt qua 100% bộ kiểm thử AST Scope, Symtable, Unit Tests và Logic Bareme QĐ 764.

---

## 📌 LẦN CẬP NHẬT THỨ 1: NGÀY 06/10/2026 - 11:30:00 (GMT+7)
- Cập nhật pool model Gemini (`gemini-2.5-flash`, `gemini-2.0-flash`, `gemini-1.5-flash`).
- Khởi tạo file `.streamlit/secrets.toml` và đẩy cấu hình `requirements.txt` chuẩn lên repository.
