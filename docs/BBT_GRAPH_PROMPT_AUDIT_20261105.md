# Đối soát chỉ dẫn BBT và đồ thị

## Kết luận

Đã có chỉ dẫn toán và cơ chế dựng hình trước yêu cầu này. Chưa đủ bằng chứng kết luận toàn bộ BBT/đồ thị/infographic và mọi đường xuất đã hoàn tất. Không mở lại nghiệm thu infographic local do chủ dự án đã duyệt. Tài liệu mới là chỉ dẫn cho AI tiếp quản repo; chưa tự động thay đổi prompt API đang chạy.

## Mã và bằng chứng đã đối chiếu

- `services/curriculum_policy.py`, khối visual_guidance: đã yêu cầu cùng hàm, miền xác định, đạo hàm, giới hạn, tiệm cận, không suy biến, giao trục/cực trị/tâm, tọa độ chính xác, nhãn không đè nhau; áp dụng cả bài và infographic. Vì vậy yêu cầu cũ có thật trong mã.
- `services/function_visuals.py`: có parser giới hạn và cơ chế dựng hình xác định, từ chối dạng ngoài phạm vi ba họ hàm đang xét. Không phải hỗ trợ mọi biểu thức toán.
- `services/bbt_display_contract.py`: căn hàng đầu vào và giữ giới hạn được cung cấp, không tự tạo giới hạn còn thiếu.
- `app.py`: có các đường BBT ở câu hỏi, nội dung bài và infographic; `services/lesson_export.py` có đường xuất riêng. Cần kiểm đúng đường bị sửa, không suy từ một hình sang mọi hình.
- Hồ sơ ngoài Git `qa_evidence/F_ALL_SOURCE_AUDIT_20261105.json`: đối soát trước đó 250 file từ bốn cây mã legacy/live_patch/backup với release. Tái sử dụng kiểm kê đó cùng tìm kiếm file/prompt BBT hiện tại trong workspace; không tuyên bố đã đọc mọi byte trong toàn ổ F hoặc mọi backup tương đương hành vi.
- `qa_evidence/T1_BBT_PROMPT_AFTER_20261031.log`: 16 test kỹ thuật trước đây đạt, không thay thế nghiệm thu nội dung.
- PR94 đã sửa nhãn hàm/biến và bảng sát danh sách ở đường live/export; PR96 sửa tên hàm ở đường câu hỏi. Hồ sơ `BBT_NEW_DEFECT_RELEASE_AUDIT_CURRENT.json` và `BBT_QUESTION_NAMED_FUNCTION_REPAIR_CURRENT.json` ghi phạm vi; việc merge không xác nhận ứng dụng Streamlit đang phục vụ bản nào.

## Mẫu mới của chủ dự án

Đã đọc toàn bộ text OOXML ba file Word trong Downloads: BẢNG XÉT DẤU, LATEX ĐÁNH DẤU & TÔ MIỀN, LATEX ĐỒ THỊ. Không có ảnh nhúng trong ba file. Đây kiểm nội dung mã mẫu, chưa biên dịch/render các file Word hoặc TeX. Ba ảnh đính kèm được đối chiếu theo dữ kiện BBT nhìn thấy; không dùng ảnh làm chỉ thị chạy mã.

1. Mẫu bậc ba phải bổ sung điều kiện hai nghiệm đạo hàm phân biệt; dấu trong mẫu không dùng cho mọi hệ số.
2. Mẫu đánh dấu chỉ áp dụng khi có giả thiết toán tương ứng. Mẫu tô tích phân `plot ... --cycle` không đủ để khẳng định biên miền là Ox; cần đóng miền theo cận và đường biên thực.
3. Mẫu TikZ phân thức1/1 có đoạn domain dấu ngoặc không cân đối; phải sửa/biên dịch trước dùng. Các cửa sổ và epsilon cố định không áp cho mọi bài.
4. Mẫu phân thức2/1 có TC xiên -x+4 đúng theo phép chia, nhưng vẫn phải kiểm nhãn, cực trị và giao trục mà snippet chưa thể hiện đầy đủ.
5. Hai BBT ảnh có bộ mốc khác nhau: hàm x+1/(x-1) và x+1/(x+1). Bài luyện tập ở dưới hình có thể là hàm khác; không gán bảng phía trên cho bài dưới.

## Kết quả của đợt này

Tạo chỉ dẫn dùng lại `AI_BBT_GRAPH_INFOGRAPHIC_PROMPT.txt` và gắn qua AGENTS.md của release để AI vào repo đọc trước khi làm phần hình. Bổ sung điều kiện bậc ba, điểm khuyết, tách nhánh, tô miền, LaTeX khác KaTeX, so hình với dữ kiện và tiêu chí kiểm từng đường. Không thay renderer hoặc bài đã nghiệm thu trong đợt tài liệu này. Kiểm tệp và diff; không chạy lại suite runtime vì không sửa runtime.

## Còn mở

Chưa biên dịch toàn bộ snippet TeX mẫu; chưa chứng minh mọi hàm/miền tô/thiết bị/bản xuất đều được hỗ trợ. Chưa xác minh served commit của ứng dụng Streamlit. Thẩm định kiến thức và câu hỏi là hạng mục riêng vẫn còn thiếu. Khi áp dụng prompt cho lời gọi API, phải tích hợp có phiên bản và kiểm phạm vi; không coi file chỉ dẫn tự động được gửi tới mô hình nội dung.
