# BẢN VÁ LỖI HỆ THỐNG GIA SƯ AI (NGÀY 06/10/2026)

## Các điểm đã nâng cấp và vá lỗi toàn diện:
1. **Tối ưu hóa cơ chế Fallback AI đa tầng:** Bổ sung các model ổn định (`gemini-2.5-flash`, `gemini-2.0-flash`, `gemini-1.5-flash`) vào danh sách `ALL_GEMINI_MODELS` bên cạnh gia phả Gemini 3.x, đảm bảo app luôn bền bỉ, không bị ngắt quãng kết nối.
2. **Tối ưu hóa hiệu năng biểu đồ Trạm 3:** Thay thế ID ngẫu nhiên bằng khóa định danh câu hỏi ổn định `q_id`, loại bỏ hoàn toàn hiện tượng render lại liên tục (flicker) trên canvas Plotly, giúp học sinh làm bài thi mượt mà.
3. **Cập nhật hỗ trợ tiền tố API Key mới:** Hỗ trợ chuẩn xác các mã API Key thế hệ mới bắt đầu bằng `AQ...` cùng với `AIzaSy...`.
4. **Cấu hình Local Dev an toàn:** Khởi tạo cấu hình secrets cho Streamlit đảm bảo mở khóa Trạm 4 không bị lỗi xác thực.
5. **Kiểm tra chuẩn xác các giải thuật:** Đạt chuẩn 100% các bài kiểm thử đơn vị cho Paired t-Test, Cohen's d, chuẩn CT GDPT 2018 và QĐ 764/QĐ-BGDĐT.
