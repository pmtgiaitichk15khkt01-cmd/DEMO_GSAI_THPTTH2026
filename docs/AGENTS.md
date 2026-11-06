# Quy trình tiếp tục dự án GSAI

Khi bắt đầu hoặc tiếp tục phiên trong workspace này, đọc `F:/FINAL KHKT 2026/qa_evidence/HANDOFF_CURRENT.md` trước. Đây là checkpoint hiện tại; các nhật ký dài là lịch sử và có mốc đã cũ. Chỉ đọc thêm tài liệu/mã liên quan đến mục đang xử lý, không đọc lại toàn hội thoại hay chạy lại toàn bộ test không có lý do.

- Sau checkpoint, đọc `F:/FINAL KHKT 2026/qa_evidence/CHECKLIST_CURRENT.md` để làm đúng mục kế tiếp. Đóng lỗi của cặp đang kiểm trước khi chọn cặp mới; tái dùng bài thật và bằng chứng còn đúng phiên bản, chỉ sinh bài còn thiếu.
- Đối chiếu local/GitHub ở đầu ca và trước phát hành; sau CI/merge kiểm Cloud bằng Chrome MCP. Ghi riêng commit local, origin/main, thay đổi chưa push và lần xác nhận Cloud gần nhất. Gộp các sửa đổi đã kiểm thành đợt phát hành; không coi mỗi lần sửa file là bắt buộc push. Yêu cầu mới ngày02/11/2026: phát hành các bản vá local đã hoàn thành; chủ dự án kiểm các cặp còn lại sau. Không tự đánh dấu đủ65 cặp đã nghiệm thu.

- Thứ tự người dùng chốt: Trạm 3 → Trạm 1 → Trạm 2. Giữ các lỗi phát sinh trong bản kiểm, không mất mục khi đổi phiên.
- UI chỉ thao tác qua Chrome MCP. Không lấy quyền điều khiển desktop/native. Mã chỉ sửa local, kiểm thử rồi mới push/CI/triển khai; giữ nguyên giao diện và tính năng. Nếu cần đổi rộng, giải trình được–mất trước.
- Phân biệt đã sửa local, qua CI, merge, Cloud đã nạp và nghiệm thu. Không tuyên bố toàn bộ kiến thức/chương trình/KNTT chính xác từ test fixture hoặc mở được đề.
- Tiết kiệm quota: tái dùng bằng chứng còn đúng commit; thử không API trước; không bấm tạo lại khi yêu cầu trước chưa rõ kết quả; không tự tăng retry hay trần gọi AI. Không bỏ kiểm chứng cần thiết để tiết kiệm.
- Không commit cache đề, dữ liệu học sinh, DB, khóa hoặc bản ghi giọng. Chỉ stage file cụ thể.
- Trước kết thúc/chuyển việc, cập nhật HANDOFF_CURRENT.md: commit/nhánh, test và log, trạng thái Cloud, request đang chạy, mục kế tiếp. Cập nhật bản kiểm khi có bằng chứng mới. Không ghi bí mật trong bàn giao.

Yêu cầu mới nhất của người dùng có ưu tiên cao hơn các hướng dẫn này.

Ngoại lệ người dùng cho phép ngày02/11/2026: Automation heartbeat mỗi giờ trong chat01a19217-68eb-7253-8135-be797724e7e2, IDti-p-n-i-nghi-m-thu-gsai-tr-m-3-1-2, để tiếp nghiệm thuTrạm1 theo checkpoint/checklist; không chạy chồng/APItrùng. Không tự tạo thêm lịch hoặc phiênAI. Chỉ báo hoàn thành, lỗi cần user xử lý hoặc cần quyết định.

Bổ sung02/11/2026: Automation phải thực hiện phần việc nghiệm thu còn thiếu ở local mỗi lượt khi không có tác vụ trùng; không chỉ đọc checkpoint/kiểm health rồi kết thúc. Theo hàng đợi qa_evidence/T1_LOCAL_ACCEPTANCE_QUEUE_CURRENT.json: đóng cặp dở rồi kiểm tiếp các cặp môn/lớp chưa có bài thật. Chỉ đánh dấu đạt theo bằng chứng; nếu thiếu điều kiện bắt buộc thật sự phải báo đúng việc cần người dùng, không lặp im lặng.

Bắt buộc ca sau đọc qa_evidence/T1_OWNER_ACCEPTANCE_REQUIREMENTS.md: đây là các yêu cầu nghiệm thu cụ thể của chủ dự án, không tự thay bằng chuẩn kỹ thuật đơn thuần hoặc giảm phạm vi. Đọc cùng checkpoint/checklist trước tiếp công việc.

Yêu cầu cốt lõi02/11/2026: Khi HS đã hiểu và không còn hỏi, gia sư Trạm1 phải có bài giảng nhân sinh/đạo đức gắn ngữ cảnh, danh ngôn triết gia Á–Âu có nguồn, ngoài lời khen; DƯỠNG THIỆN TÂM–ƯƠM NHÂN TÀI là cái hồn hệ thống. Không tự rút thành1–2câu/khen chung vì giới hạn độ dài; đọc phần bổ sung đầu T1_OWNER_ACCEPTANCE_REQUIREMENTS.md.

Quyết định chủ dự án 05/11/2026: Bản vá đã đủ bằng chứng local phải commit và push ngay các file cụ thể trong cùng vòng việc, theo tiếp CI/merge/Cloud; không để bản vá đã kiểm ở local chờ gom muộn. Phân biệt push nhánh, tích hợp main và Cloud đã nạp.

Bổ sung chủ dự án05/11/2026 về BBT/đồ thị/infographic: trước làm phần hình, đọc release_station1_20261031/docs/AI_BBT_GRAPH_INFOGRAPHIC_PROMPT.txt và báo cáo BBT_GRAPH_PROMPT_AUDIT_20261105.md. Không coi file chỉ dẫn là bằng chứng đã hoàn thành mọi hình hoặc tự được chèn vào API. Giữ đóng nghiệm thu owner; lịch vẫn tắt.

Yêu cầu chủ dự án05/11/2026: Phần đồ thị phải vẽ hình thực; gióng cực trị/tâm tới hai trục, ghi giao trục, giữ tọa độ vô tỷ chính xác và tránh đè nhãn. Prompt API và prompt infographic phải có yêu cầu này. Chi tiết ở AGENTS repo và docs/AI_BBT_GRAPH_INFOGRAPHIC_PROMPT.txt.

Quy tắc bắt buộc05/11/2026: mọi AI vào làm hình/đồ thị/BBT trong infographic phải đọc docs/AI_BBT_GRAPH_INFOGRAPHIC_PROMPT.txt trong release và checkpoint trước thao tác. Nền hình/BBT và nhãn phải trong suốt để đúng nền infographic, không mảng trắng riêng; giữ nét gióng, tọa độ chính xác và chống đè nhãn.

Chủ dự án05/11/2026: Giọng nữ hiện tại đang chạy tốt, giữ nguyên provider/nguồn âm thanh/cache/luồng phát. Chỉ sửa kết nối và dịch vụ hai giọng Thầy Trí/giọng nam. Ưu tiên miễn phí, dùng được Android/iOS/macOS/Windows và không phụ thuộc PC chủ dự án; không claim đã đạt khi thiếu backend/kiểm thực.
