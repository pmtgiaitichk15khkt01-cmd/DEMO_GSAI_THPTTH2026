# Kiểm kê ban đầu bộ kiểm định — 30/10/2026

Base đọc mã: 5b5aaa1a1e7840f1ef07384652947417baed9602. Chưa sửa runtime, chưa gọi AI, chưa chạy lại test.

| Thành phần đang có | Khả năng chứng minh hiện tại | Khoảng thiếu cần xử lý |
|---|---|---|
| services/curriculum_policy.py: legal_references | Lọc khoảng ngày theo registry | Mặc định dùng POLICY_DATE=2026-10-24; ngày hiệu lực trong JSON không tự chứng minh còn hiệu lực tại ngày xuất. Cần kiểm bản gốc, quan hệ sửa đổi và phạm vi áp dụng; không chỉ đổi sang ngày hôm nay rồi coi đã cập nhật. |
| policy_prompt | Yêu cầu đúng môn/lớp/KNTT và phân biệt luyện tập với tốt nghiệp | Prompt không phải chứng cứ học thuật; chưa có truy xuất yêu cầu cần đạt/trang sách cho từng câu. |
| validate_lesson_policy | Kiểm khai báo môn/lớp ở một số dòng đầu và mâu thuẫn địa lý hẹp | Không kiểm toàn bộ kiến thức bài học; không được gọi đây là kiểm định CT2018 đầy đủ. |
| prepare_exam_for_delivery | Kiểm cấu trúc, môn/lớp khai báo, yêu cầu phạm vi hẹp; giữ payload và ghi hash | curriculum_audit chủ động đặt academic_verified=False/needs_teacher_review là đúng giới hạn; không đổi True chỉ vì mã chạy qua. |
| data/curriculum_source_audit_20261024.json | Báo cáo lịch sử tự khai kiểm kho: 33.679 bản đề, 948.902 lượt câu | Báo cáo ghi toàn bộ bản đề thiếu minh chứng yêu cầu cần đạt/trang/phiên bản. Đây là số liệu báo cáo cũ, chưa chạy lại hay xác nhận độc lập trong lượt này. |
| Đồ thị/BBT/phục dựng | Các guard và renderer sẵn có, PR59 vừa sửa căn bảng/lộ công thức | Tái dùng, bổ sung bằng chứng cụ thể. Câu dựng lại phải có dữ kiện đồng nhất và đáp án được kiểm; không xem đồ thị vẽ được là câu đúng. |

## Phần việc kế tiếp, phạm vi hẹp
1. Đọc kiểm thử policy và bộ đánh giá mức độ đang có; lập hợp đồng kết quả chung có các trạng thái đạt kiểm kỹ thuật/chưa đủ căn cứ/sai đã chứng minh, lý do, nguồn, phiên bản, phạm vi và fingerprint nội dung.
2. Đối chiếu nguồn gốc chính thức của registry đang có qua Chrome được phép, lưu URL/đoạn phụ lục/ngày truy cập và giới hạn xác minh; không coi tên miền hoặc ngày checked_at là bằng chứng đủ.
3. Thiết kế bản đồ yêu cầu cần đạt + SGK/SGV/đính chính. Chưa có nguồn thì chưa thẩm định, không tự gán đạt và không chặn cả bài hợp lệ bằng suy đoán.
4. Mỗi quy tắc có ca sai, ca đúng dễ bị chặn nhầm, ca ngoài phạm vi. Chạy chế độ chỉ ghi nhận trước khi tích hợp sửa/thay, giữ trần gọi và UI.

Nghiệm thu nội dung không thay thế nghiệm thu vận hành/độ trễ/giữ chức năng. Không có một định dạng đề Bộ chung cho mọi lớp/môn; cần xác định loại đánh giá và văn bản áp dụng. Chưa xác minh pháp quy mới trong lượt này, chưa chứng nhận học thuật toàn ma trận.
