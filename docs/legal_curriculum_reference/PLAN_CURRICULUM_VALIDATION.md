# Yêu cầu bộ kiểm định chung — người dùng chốt30/10/2026

## Thứ tự
Yêu cầu mới nhất ngày30/10/2026: ưu tiên xây bộ kiểm định chung trước, sau đó tích hợp có kiểm soát và tiếp tục nghiệm thu Trạm3→Trạm1→Trạm2. Bắt đầu bằng kiểm kê bộ lọc đang có và bằng chứng nguồn; chưa bật chặn rộng hoặc thay UI. Yêu cầu này thay thứ tự cũ xây sau nghiệm thu. Tái dùng công cụ đồ thị/BBT/khôi phục/các guard đã có sau đánh giá phạm vi, không xây lại tùy tiện.

## Phạm vi mục tiêu
Đa môn, lớp6–12 theo danh mục hệ thống: nội dung, yêu cầu tùy biến, đồ thị/BBT/hình, đáp án duy nhất khi dạng câu yêu cầu, công thức/hiển thị, mức độ tư duy, CTGDPT2018, bộ Kết nối tri thức với cuộc sống đúng phiên bản/đính chính, văn bản Bộ mới và cũ còn hiệu lực tại thời điểm áp dụng. Không áp mẫu thi tốt nghiệp cho mọi lớp/môn.

## Thiết kế cần thẩm định trước tích hợp
1. Danh mục nguồn chính thức: văn bản gốc/phụ lục, cơ quan ban hành, ngày ban hành/hiệu lực, văn bản sửa đổi/thay thế/bãi bỏ, phạm vi áp dụng, ngày đối chiếu, phiên bản/hàm băm. Nguồn phụ chỉ hỗ trợ, không tự chứng minh hiệu lực.
2. Bản đồ môn/lớp/chủ đề/bài→yêu cầu cần đạt→trang/phiên bản SGK/SGV và đính chính. Chưa có nguồn đủ thì ghi chưa xác minh, không gán đạt hay sai.
3. Tiêu chí mức độ dựa trên thao tác tư duy/dữ kiện mới/bước suy luận/chuyển giao, minh chứng theo từng câu/ý. Không suy mức độ chỉ bằng động từ, độ dài hay vị trí phầnI/II/III. Nhãn đề xuất khác nhãn giáo viên đã duyệt.
4. Tách kiểm chắc chắn bằng mã/toán/cấu trúc khỏi đánh giá nội dung dựa nguồn và đánh giá sư phạm. Ghi kết luận kèm nguồn/lý do/phạm vi/độ tin cậy, không nhãn “chuẩn Bộ” tự phong.
5. Luồng đầu ra: soạn→kiểm→sửa hoặc thay nguyên câu chưa đạt→kiểm lại→xuất khi đạt hợp đồng áp dụng. Giới hạn số vòng/thời gian/token; không lặp vô hạn. Không âm thầm sửa key/options/giả nguồn. Hết ngân sách mà chưa đủ dữ liệu thì trạng thái rõ cho giáo viên, không bịa nội dung hoặc tuyên bố đạt.
6. Hiệu quả: kiểm cục bộ khôngAPI trước, nguồn/cache có phiên bản, chỉ kiểm lại thành phần đổi, gọiAI có mục đích cho phần cần đánh giá; không tăng trần gọi hiện hữu khi chưa được giải trình. Đo recall/falsepositive, chi phí/token và p50/p95 trước/sau.
7. Triển khai có kiểm hồi quy: bảo toàn giao diện/radio/3MCQ+2tự luận4PolyaT1/EXPLAINkhácSocratic/infographic/video/voice và các tính năng. Ma trận các môn/lớp, bộ ca đúng/sai/ngoài phạmvi, chạy shadow chỉ ghi nhận trước khi chặn hay sửa. Có rollback và báo cáo được–mất.

## Giới hạn cam kết
Đây là mục tiêu và kế hoạch, chưa phải bộ lọc đã hoàn thành. Không thể chứng nhận100% chuẩn mọi câu từ testfixture hoặc dữ liệu mô hình. Ngày hiện hành pháp quy phải được xác minh bằng nguồn chính thức khi triển khai; tài liệu này chưa cập nhật/kiểm hiệu lực pháp luật. Mức độ và nội dung học thuật cần chuyên môn/giáo viên duyệt ở phần chưa chứng minh tự động. Chỉ bỏ cảnh báo cho phạm vi có bằng chứng nghiệm thu tương ứng.
