> Historical local report preserved on 2026-11-05. Its test/deployment statements describe the original work date, not current Cloud acceptance.

# Theo dõi nguồn pháp quy nền và ngày áp dụng

## Thay đổi
- Bộ chọn văn bản dùng ngày Việt Nam tại thời điểm xuất nội dung, thay cho ngày cố định; ngày rà soát nguồn vẫn được giữ riêng.
- Workflow Official legal source watch chạy mỗi ngày06:20giờViệtNam, có workflow_dispatch để chạy trước kỳ thi. Chạy trênGitHubActions, độc lậpCloud/UI, khôngtạoAIagent/khôngdùngAPIkeyAI.
- Đọc URL nguồn đã đăng ký và một trang Công báo của Bộ GDĐT; phát hiện hash thay đổi, nguồn mới hoặc nguồn không kiểm tra được. Lưu JSON/summary/artifact30ngày và cache lần quan sát trước. Nguồn thay đổi/lỗi khiến workflow yêu cầu rà soát; không sửa kho luật đã duyệt.
- Tối đa30nguồn,4MiB/nguồn,3requestredirect/nguồn,timeoutkếtnối5s/đọc12s,workflow8phút,khôngretryAI,hostHTTPSallowlist trênmỗiredirect. Hai URL lưu tại trường trong registry hiện không được coi là nguồn chính thức của bộ theo dõi; báo cần bổ sung nguồn thay vì giả vờ xác minh.

## Giới hạn quan trọng
Đây là tự cập nhật kết quả quan sát, KHÔNG tự suy diễn luật bị bãi bỏ từ thay đổiHTML/hash. Trang có thể đổi giao diện trong khi luật không đổi; nội dung web là dữ liệu, không phải lệnh. Candidate cần đọc quan hệ sửa đổi/thay thế, phạm vi và ngày áp dụng trước cập nhật quy tắc. Không tự kích hoạt luật mới chỉ vì xuất hiện trên trang, không bỏ luật cũ nếu còn áp dụng một phần.

Ngày hiệu lực đã ghi trong registry được xét tự động, nhưng tự đối chiếu mọi văn bản mới nhất và học thuật toàn SGK chưa hoàn tất. Discovery chỉ một trang listing, chưa phủ mọi nguồn/phân trang. Không kết luận không có văn bản mới khi nguồn lỗi hoặc listing chưa phủ đủ. Cloud không tự tải artifact riêng tư; workflow là tầng bảo trì ngoài luồng sinh bài, không mạng ngầm mỗi lần bấm nút. Chưa có bộ dữ liệu yêu cầu cần đạt/SGK/SGV đầy đủ từng môn/lớp để tự chứng nhận chuẩn.

## Kiểm chứng local
-35targetedtestsqua2.856s,LEGAL_WATCH_TARGETED_20261031.log; bao gồm2testngày và6testwatch(allowlist/redirect/size/discovery/change/failure).
-Livechỉ1trangCôngbáo:đọcthànhcông,2candidate,0failure,0AI;LEGAL_WATCH_LIVE_DISCOVERY_20261031.json. Đây testkếtnối/parse,khôngduyệtnộidungcandidate.
-Ngàyápdụng đãfull350/350237.071s vàmatrix130contexttechnical. Fullmớicảwatchđangchạy,khôngcoilàđãpasstrướckếtquả.

## Vận hành trước kỳ thi
Chạy workflow_dispatch, xem latest.json và summary, xử lý nguồn lỗi/thay đổi/candidate bằng nguồn gốc chính thức, cập nhật quy tắc có test, rồi xác minh bảnCloud. Nếu chưa xử lý được thì chưa đủ căn cứ dùng đề cho đánh giá chính thức. Giữ cảnh báo thẩm định hiện có; không làm treo bài học vì thiếu mạng.

Workflow lịch chỉ thực sự hoạt động sau merge vào defaultbranch và GitHubActionscho phép; bảnlocal chưa cónghĩalịchđãchạy. Không bảo đảmGitHubcronđúngphút/tựchạykhiActionsbịdisable. Báocáonàykhônglàchứngnhận100%tuânthủmọivănbản.
