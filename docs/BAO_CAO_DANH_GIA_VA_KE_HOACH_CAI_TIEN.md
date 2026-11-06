# Đánh giá dự án Gia Sư AI và kế hoạch cải tiến

Ngày đánh giá: 24/10/2026. Thư mục nguồn: `VIP_DEMO_GSAITHPT2026-main/VIP_DEMO_GSAITHPT2026-main`.

## 1. Kết luận điều hành

Dự án có nền tảng tốt để phát triển thành công cụ hỗ trợ tự học: quy trình 4 trạm rõ ràng, nội dung tiếng Việt, ngân hàng đề cục bộ, nhập tài liệu, trực quan hóa và xuất đề. Tuy nhiên, bản hiện tại cần sửa các vấn đề bảo mật, tính đúng của chấm điểm và tính trung thực của chỉ số nghiên cứu trước khi sử dụng cho đánh giá học sinh hoặc đưa ra kết luận hiệu quả KHKT.

Ưu tiên đề xuất: **bảo vệ dữ liệu → chấm đúng → phân biệt dữ liệu thật/mẫu → kiểm chứng nội dung → cải tổ kiến trúc → mở rộng tính năng**.

Không nên ưu tiên bổ sung thêm thuật ngữ AI hoặc mở rộng phạm vi môn học trong giai đoạn đầu. Giá trị cần chứng minh là học sinh hiểu bài tốt hơn, kết quả được lưu đúng và giáo viên kiểm tra được nguồn gốc.

## 2. Phạm vi và phương pháp

- Kiểm kê 29 tệp Python; đọc các luồng chính trong app, engine đề thi, lưu trữ, nhập tài liệu, mô hình dữ liệu và các service; rà soát engine hình ảnh, infographic, chương trình học, CI và bộ kiểm thử.
- Phân tích AST: `app.py` có 20.316 dòng, khoảng 906 KB; `real_exam_engine.py` có 3.568 dòng. Phát hiện một hàm cấp module bị định nghĩa hai lần trong app.
- Chạy `python -m unittest discover -s tests -v`: **26 kiểm thử được chạy, tất cả đạt**, Python 3.14.5. Thời gian 0,515 giây là thời gian runner báo, không bao gồm toàn bộ khởi động tiến trình và import.
- Chạy riêng `python tests/test_multi_subject_grade_integrity.py`: script báo cả 15 tình huống đa môn/đa lớp đạt. Chúng hiện không nằm trong 26 test unittest nêu trên.
- Giải nén, đọc và đếm toàn bộ 13 shard `.json.xz` theo môn; thực hiện so sánh thân câu hỏi và thử riêng các hàm có nghi vấn.
- Không sửa mã nghiệp vụ. Việc import ứng dụng để chạy test có thể khởi tạo SQLite/cache như hành vi sẵn có của dự án.
- Chưa kiểm thử giao diện trên điện thoại, tải đồng thời, triển khai cloud, API Gemini thật, Supabase thật, hay độ chính xác OCR bằng tập ảnh chuẩn. Không coi test import app là bằng chứng hoàn thành kiểm thử giao diện.
- Không thẩm định từng đáp án trong gần một triệu lượt câu, không xác minh quyền sử dụng từng tài liệu và không kết luận tính tuân thủ văn bản giáo dục chỉ từ README.

## 3. Kiến trúc hiện tại

| Thành phần | Vai trò | Nhận xét |
|---|---|---|
| `app.py` | Streamlit, giao diện 4 trạm, AI, chấm điểm, báo cáo, thống kê, xuất bản | Tập trung quá nhiều trách nhiệm; thay đổi nhỏ có thể ảnh hưởng nhiều luồng |
| `real_exam_engine.py` | Đọc kho đề, chuẩn hóa, trộn đề, nhập và ghi dữ liệu | Có cache và phân mảnh theo môn; cần quản trị nguồn gốc, đồng thời và tính bất biến |
| `precision_visual_engine.py` | Phục dựng và kiểm soát ngữ cảnh hình vẽ | Có kiểm thử hồi quy cho lỗi gán hình sai môn; vẫn cần kiểm chứng nội dung thay vì suy ra hình từ đáp án |
| `lesson_infographic_engine.py` | Tóm tắt, ví dụ và SVG | Có giá trị trải nghiệm; nhiều nội dung theo mẫu, cần rà soát tính đúng từng môn/lớp |
| `exam_file_extractor.py` | Đọc DOCX/PDF, OMML, phát hiện nhu cầu OCR | Đã xử lý nhiều trường hợp thực tế; cần bộ tài liệu chuẩn và giới hạn tài nguyên |
| `database.py`, `schema.sql` | SQLite, đồng bộ Supabase | Có truy vấn tham số hóa và WAL; schema chạy thực tế yếu hơn schema tài liệu |
| `models/`, `services/` | Chuẩn hóa dữ liệu, chấm, BKT, lịch ôn, đo lường | Là hướng tách lớp phù hợp nhưng chưa trở thành nguồn xử lý duy nhất |
| `tests/`, `.github/workflows/ci.yml` | Kiểm thử và CI Python 3.10/3.11 | Có nền tảng hồi quy; còn thiếu kiểm thử bảo mật, lưu trữ và số liệu nghiên cứu |

## 4. Ưu điểm cần giữ

1. **Luồng học tập có chủ đích:** học lý thuyết → nộp bài/đối thoại → luyện tập → theo dõi. Đây là cấu trúc dễ tổ chức thử nghiệm sư phạm.
2. **Định hướng gợi mở:** có xử lý gợi ý Socratic, xác nhận khi OCR không rõ và thông điệp cần giáo viên duyệt. Nên tiếp tục phát triển thành hành vi có thể đo lường.
3. **Khả năng dùng tại trường:** hỗ trợ Word/PDF, in đề, LaTeX, dữ liệu CSV và SQLite; không phụ thuộc AI cho mọi thao tác ngân hàng đề.
4. **Trực quan hóa phong phú:** SVG, bảng biến thiên, đồ thị và mô hình 3D có tiềm năng giúp học sinh hiểu bản chất.
5. **Có nỗ lực kiểm soát lỗi thực tế:** kiểm thử tránh gán bảng biến thiên sang môn khác, bảo toàn đồ thị và xuất đủ câu hỏi.
6. **Đã có service và model riêng:** có thể tái cấu trúc từng phần mà không cần viết lại toàn bộ sản phẩm.
7. **Một số biện pháp kỹ thuật tốt:** SQL dùng tham số, SQLite WAL, cache theo môn, giới hạn AST cho một luồng biểu thức trong app, xử lý timeout và che khóa trong một số thông báo AI.

## 5. Phát hiện ưu tiên cao

### F01 — P0: Mật khẩu quản trị viết sẵn vẫn được chấp nhận

**Bằng chứng:** `app.py:19847–19857`. Điều kiện đăng nhập chấp nhận mật khẩu cố định bằng hai nhánh riêng, rồi mới kiểm tra giá trị cấu hình bằng `hmac.compare_digest`.

**Tác động:** đặt mật khẩu riêng không vô hiệu hóa mật khẩu cũ trong mã nguồn. Sau đăng nhập, Trạm 4 gọi `get_all_logs()` để lấy dữ liệu toàn hệ thống.

**Sửa:** bỏ hoàn toàn nhánh mật khẩu cố định; thiếu secret thì khóa chức năng quản trị. Bổ sung giới hạn thử sai, thời hạn phiên và kiểm tra quyền ở thao tác đọc/xuất dữ liệu. Khi dùng nhiều trường/lớp, chuyển sang tài khoản và quyền theo phạm vi.

**Nghiệm thu:** mật khẩu cũ luôn bị từ chối, kể cả khi secret có hoặc không có; người chưa có quyền không thể xem/xuất nhật ký.

### F02 — P0: Ranh giới xử lý biểu thức SymPy chưa an toàn

**Bằng chứng:** `services/neuro_symbolic_verifier.py:22`, đặc biệt lời gọi `sp.sympify(s, locals=local_dict)`. Chuỗi chỉ được thay thế regex; `local_dict` còn đưa cả module `sp` vào phạm vi. Chưa có parser giới hạn cú pháp hoặc worker giới hạn tài nguyên tại service này.

Tài liệu chính thức SymPy cảnh báo `sympify` dùng `eval` và không nên nhận đầu vào chưa làm sạch: [SymPy Basic Operations](https://docs.sympy.org/latest/tutorials/intro-tutorial/basic_operations.html).

**Sửa:** parse theo grammar toán học cho phép, dựng trực tiếp đối tượng SymPy từ cây cú pháp đã kiểm tra, cấm attribute/lời gọi ngoài danh sách; xử lý phép toán nặng trong tiến trình riêng có timeout và giới hạn tài nguyên. Chỉ chuyển sang `parse_expr` không tự giải quyết vấn đề vì parser đó cũng dùng eval.

**Nghiệm thu:** cú pháp ngoài toán học bị từ chối trước đánh giá; biểu thức quá phức tạp hết hạn có kiểm soát; không làm treo ứng dụng. Chưa thực hiện khai thác lỗ hổng trên môi trường triển khai.

### F03 — P1: Chấm điểm có thể nhận đáp án sai

**Bằng chứng tái hiện:**

```text
numeric_answer_matches('2.4', '2') → True
numeric_answer_matches(0, 0) → False
grade_part2([{'stmts':[{'t':'sample','a':'false'}]}],
            {'p2_0_0':'Đúng'}) → (0.1, 1, 1)
```

**Nguyên nhân:** tự suy độ làm tròn từ số chữ số đáp án; `value or ''` làm mất số 0; chuỗi `'false'` được coi là truthy. Hàm so đáp án số còn được sao chép trong `app.py:2821` và service. Ví dụ số 0 dạng số là lỗi ở biên API; luồng giao diện chuyển thành chuỗi có thể không gặp lỗi này.

**Sửa:** chính sách chấm là metadata bắt buộc của câu hỏi: so chính xác, làm tròn theo đề hoặc dung sai riêng; chuẩn hóa boolean ngay đầu vào; chỉ giữ một service chấm. Kiểm tra đủ cấu trúc đề trước khi chấm, không tự suy thang điểm từ tên môn trong nhiều nơi.

**Nghiệm thu:** bộ đáp án chuẩn có số 0, số âm, dấu phẩy thập phân, số nguyên, biên dung sai, thiếu đáp án và string boolean đều đúng; app và xuất báo cáo dùng cùng kết quả.

### F04 — P1: Chỉ số BKT được dựng từ chuỗi giả lập

**Bằng chứng:** `services/bkt_service.py:108–136` tạo `simulated_seq`; tham số mặc định đặt P(T) Socratic = 0,35 và truyền thống = 0,08. `app.py:13270` truyền tỷ lệ đúng cố định 0,75 và hiển thị diễn giải về hiệu quả.

**Tác động:** sự khác biệt giữa hai mô hình có sẵn trong giả định. Không thể dùng kết quả đó để chứng minh học sinh thực tế tiến bộ hoặc Socratic tốt hơn 4,3 lần. Các trục dùng chung xác suất cuối chuỗi, chưa phải truy vết từng kỹ năng.

**Sửa:** ghi từng quan sát thật theo học sinh/kỹ năng/câu hỏi/thời gian/mức gợi ý; cập nhật và lưu trạng thái riêng; gắn nhãn mô phỏng cho kết quả giả lập; chỉ ước lượng và so sánh tham số khi có dữ liệu độc lập.

### F05 — P1: Bảng đo lường khảo thí đang dùng dữ liệu sinh ngẫu nhiên

**Bằng chứng:** `app.py:20219–20220` luôn gọi `generate_benchmark_psychometric_sample(n_students=35, k_items=22)` tại khối hiển thị Cronbach và phân biệt câu hỏi.

**Tác động:** chỉ số hiển thị không phản ánh các bài thi đang lưu. Hàm `extract_item_matrix_from_attempts` có tồn tại nhưng chưa được dùng tại khối này. Khi đưa đáp án chữ A/B vào hàm đó, cả hai đều thành 0, vì không đối chiếu đáp án chuẩn. Ghép theo khóa vị trí `p1_0` giữa các đề khác nhau còn có thể trộn các câu khác nội dung.

**Sửa:** lưu `question_id`, phiên bản câu, đáp án đã chọn và kết quả đúng/sai tại lúc nộp; phân nhóm đúng đề hoặc tập câu chung; chỉ tính khi đủ dữ liệu thật. Dữ liệu demo cần chế độ và nhãn riêng. Không cắt alpha âm về 0 để che hiện tượng bất thường; phân biệt chỉ số tương quan item-total và item-rest.

**Nghiệm thu:** từ một bộ bài làm chuẩn, truy ngược từng ô ma trận về bản ghi gốc; kết quả đối chiếu phép tính độc lập; thiếu dữ liệu thì hiển thị chưa đủ dữ liệu.

### F06 — P1: Monte Carlo đưa ra kết luận vượt phép tính

**Bằng chứng:** `app.py:20278–20308`: độ lệch chuẩn gain lấy từ điểm post thay vì hiệu số; lấy percentile mức tăng cá nhân rồi gắn nhãn khoảng tin cậy; thông báo hoàn tất khẳng định Gaussian `p < 0.001` dù trong khối không có phép kiểm định tương ứng.

**Sửa:** xác định mô phỏng dùng cho câu hỏi nào; dùng dữ liệu chênh lệch bắt cặp, mô hình hóa tương quan khi cần; phân biệt khoảng phân vị dự báo và khoảng tin cậy trung bình. Gỡ kết luận p-value viết sẵn. Không suy hiệu quả toàn tỉnh từ mô phỏng phân phối.

**Nghiệm thu:** báo cáo được giả định, seed, cỡ mẫu thật, số lượt mô phỏng và cách tính; không có kết luận mà phép tính chưa hỗ trợ.

### F07 — P1: Kiểm chứng toán có sai số logic và cờ xác minh gây hiểu nhầm

**Bằng chứng:** `verify_calculus_function('x^3')` trả `critical_points: [0.0]`; hàm audit đếm số nghiệm đạo hàm bằng 0 để suy số cực trị. Nhưng x³ không có cực trị. `app.py:4018–4020` gắn `neuro_symbolic_verified=True` chỉ từ `audited` và `verified`, chưa loại trường hợp `hallucination_detected=True`.

**Sửa:** phân loại điểm dừng bằng đổi dấu đạo hàm hoặc lập luận hợp lệ, xét miền xác định; tách `parsed`, `computed`, `answer_checked`, `answer_consistent`. Không gắn cờ đã kiểm chứng đáp án khi mới tính được hàm.

**Nghiệm thu:** x³ có 0 cực trị, x⁴ có 1; đáp án sai dù parse được phải bị chặn/cảnh báo. Kiểm tra thêm điểm khuyết và giới hạn một phía.

### F08 — P1: Định danh và lưu kết quả có nguy cơ ghi đè hoặc gán sai lớp

**Bằng chứng:** `database.py:130–136`: ID học sinh rơi về tên/anonymous; ID lần thi thiếu trở thành chuỗi `'None'`; `INSERT OR REPLACE` có thể thay bản ghi cùng ID. `grade=10` hoặc `'10'` bị mặc định thành 12 vì không chứa chữ `Lớp`.

**Sửa:** ID học sinh độc lập tên hiển thị; UUID bắt buộc cho sự kiện; parse lớp bằng một hàm chung; ràng buộc hợp lệ và giao dịch; idempotency theo đúng ID, không âm thầm thay thế dữ liệu khác.

**Nghiệm thu:** hai học sinh cùng tên tách biệt; hai sự kiện thiếu ID không ghi đè; lớp số và lớp chuỗi đều lưu đúng; dữ liệu lỗi bị từ chối rõ ràng.

### F09 — P1: Schema và đồng bộ chưa bảo đảm tính toàn vẹn

**Bằng chứng:** bảng SQLite tạo trong `database.py` không có CHECK/foreign key như `schema.sql`; chưa bật `PRAGMA foreign_keys`. Đồng bộ dùng daemon thread từng lần ghi, không có outbox bền vững/retry. Payload exam/diagnostic được gửi mà chưa thấy đồng bộ student tương ứng trong luồng này; có thể lỗi FK khi dùng schema cloud đã cung cấp. `_sync_to_supabase` chỉ coi 200/201 là thành công, trong khi phản hồi 204 cũng cần được xử lý nếu cấu hình trả tối thiểu.

**Sửa:** migration versioned, schema thống nhất; outbox SQLite cùng transaction với lần ghi, retry/backoff và trạng thái lỗi; upsert student trước bản ghi phụ thuộc; đo và log phản hồi không chứa secret.

**Nghiệm thu:** mất mạng/khởi động lại vẫn đồng bộ đủ và không trùng; vi phạm ràng buộc bị chặn ở cả local/cloud; có kiểm thử hợp đồng API giả lập.

## 6. Ngân hàng đề và nguồn gốc

Đã xác nhận **33.679 bản ghi đề** trong 13 shard XZ. Trong các trường câu hỏi được đếm, có **947.012 lượt xuất hiện câu hỏi**. Khi lấy trường `q`/`question`/`prompt`, chuẩn hóa khoảng trắng và chữ hoa/thường, có **3.111 thân câu khác nhau trên toàn bộ các shard**.

Đây là số thân câu, không phải số câu hỏi hoàn chỉnh duy nhất: phương án, mệnh đề, dữ liệu hình và tham số có thể khác nhau. Ngữ văn dùng cấu trúc riêng nên không được suy rằng môn này không có câu hỏi chỉ vì bộ đếm p1/p2/p3 không tìm thấy. Không cộng bản master và bản nén khác để tránh đếm trùng vật lý.

Kiểm tra bổ sung trên p1/p2/p3, băm JSON của các trường `q`, `opt`, `stmts`, `ans`, `f`, `bbt`, `geom_3d`, `mslgn_data` (giữ thứ tự danh sách, sắp khóa JSON) cho **3.171 tổ hợp nội dung khác nhau** trong 947.012 lượt. Đây vẫn là định nghĩa theo các trường đã chọn, có thể bỏ sót dữ liệu hình ở trường khác; không phải thẩm định ngữ nghĩa hay kết luận mọi bản ghi trùng đều có thể xóa an toàn. Cần đưa phép đếm có phiên bản này thành công cụ audit chính thức và bổ sung schema Ngữ văn (`part_doc_hieu`, `part_viet`).

| Shard môn | Số bản ghi đề | Lượt câu được đếm | Thân câu khác nhau trong môn |
|---|---:|---:|---:|
| Địa lý | 1.840 | 51.520 | 390 |
| Công nghệ | 4.240 | 117.120 | 362 |
| GDKT&PL | 2.400 | 65.600 | 72 |
| Hóa học | 1.840 | 51.520 | 347 |
| Khoa học tự nhiên | 2.401 | 65.296 | 88 |
| Lịch sử | 1.840 | 51.520 | 340 |
| Lịch sử & Địa lý | 2.400 | 65.600 | 72 |
| Ngữ văn | 320 | Cấu trúc riêng | Chưa đếm theo schema riêng |
| Sinh học | 1.840 | 51.520 | 333 |
| Tiếng Anh | 4.240 | 166.400 | 572 |
| Tin học | 4.240 | 117.120 | 362 |
| Toán học | 4.238 | 92.276 | 259 |
| Vật lý | 1.840 | 51.520 | 298 |

**Kết luận:** số đề trong README được xác nhận về lượng bản ghi. Tuyên bố “gần 1 triệu câu hỏi độc nhất” chưa được xác nhận và cần thay bằng số liệu có định nghĩa rõ ràng.

Các vấn đề bổ sung:

- `real_exam_engine.py:2368` nạp đề AI và đặt đồng thời `is_real_bank_question=True`, `is_ai_harvested=True`. Cần phân loại nguồn độc lập: tài liệu gốc, giáo viên biên soạn, AI sinh, biến thể.
- Một số luồng tự điền tên trường/chuyên trang khi thiếu nguồn. Nhãn nguồn do phần mềm điền không phải bằng chứng tài liệu gốc.
- Mỗi câu cần URL/tệp gốc, trang, hash tài liệu, thời điểm nhập, phương pháp trích xuất, người duyệt và lịch sử phiên bản; thiếu bằng chứng thì hiển thị chưa xác minh.
- Kho chung cần hàng đợi duyệt; đề mới không tự được coi là nội dung chuẩn. Tách kho riêng giáo viên và nội dung được phép công bố.
- `append_exam_to_national_shard` đọc-sửa-ghi XZ; cần khóa hoặc một writer và thay tệp nguyên tử để tránh mất cập nhật khi nhiều phiên ghi cùng lúc.
- Có cả XZ và Zstandard nhưng loader shard hiện ưu tiên XZ/Gzip/JSON, không dùng Zstandard ở nhánh đã đọc. Cần chọn định dạng theo benchmark thật, tránh hai bản nội dung lệch nhau.
- SHA-1/fingerprint chỉ phục vụ nhận diện trùng, không chứng minh bảo mật đề thi hoặc chống lộ đáp án.

## 7. Cá nhân hóa, quyền riêng tư và tài liệu

- `app.py:1623` gọi lịch ôn không truyền nhật ký; service tự đưa ba ví dụ Toán/Hóa. Không đủ cơ sở coi đây là lịch cá nhân của học sinh. `level[:2]` cũng làm VDC trùng VD. Cần lưu lịch sử review, độ bền và thời điểm thực, hiển thị trạng thái rỗng khi chưa có dữ liệu.
- README nói dữ liệu riêng không truyền về máy chủ trung gian, nhưng Streamlit xử lý phía server, gọi Gemini và có SQLite/Supabase/webhook. Cần sơ đồ luồng dữ liệu đúng với triển khai; không khẳng định mọi thứ chỉ ở localStorage.
- Có trường tên học sinh, tên trường và nhật ký. Mã học sinh là biện pháp định danh thay thế, không tự bảo đảm ẩn danh hoàn toàn. Cần tối thiểu hóa dữ liệu, quyền xem/xuất, thời hạn lưu và chức năng xóa.
- Có tệp DB trong gói dự án; chưa mở nội dung cá nhân để đánh giá này. Cần xác nhận đó là dữ liệu mẫu trước khi chia sẻ hoặc đóng gói; bổ sung quy tắc ignore DB/WAL/SHM cho dữ liệu runtime và cung cấp seed riêng.
- Các khẳng định “khử 100% ảo giác”, thời gian truy vấn dưới 5ms, nạp dưới 0,05 giây và khuyến nghị 25–35 phút/ngày cần bằng chứng hoặc cách diễn đạt có giới hạn. Không suy thời lượng tối ưu từ tương quan đơn giản.
- Chưa thấy manifest/service worker riêng trong danh mục tệp; chức năng thêm biểu tượng lên màn hình không tự chứng minh hỗ trợ offline toàn bộ. Cần kiểm thử và mô tả đúng phạm vi offline: kho đề, AI, OCR, đồng bộ.

## 8. Khả năng bảo trì, kiểm thử và trải nghiệm

- `render_subject_exam_matrix_spec` được định nghĩa ở `app.py:13502` và `14461`; định nghĩa sau ghi đè trước. Xóa trùng sau khi xác định hành vi mong muốn.
- Logic chấm, chuẩn hóa, xử lý hình và xuất bản đan xen. Có luồng “auto-heal” thay nội dung/phương án: cần lưu bản gốc, diff và trạng thái duyệt để giáo viên kiểm tra thay đổi.
- Các `except Exception` nuốt lỗi khiến tính năng có thể thất bại âm thầm. Dùng mã lỗi, log có ngữ cảnh và thông báo có thể hành động; phân biệt không có dữ liệu với lỗi hệ thống.
- Requirements phần lớn không khóa phiên bản; thiếu chỉ dẫn phiên bản Python triển khai thống nhất. Tạo môi trường tái lập và lockfile sau khi kiểm thử.
- Bộ test hiện tập trung trực quan hóa và khả năng gọi hàm. `test_exam_preflight_auto_heal` chưa chạy toàn bộ preflight mà chỉ gọi sanitizer. `test_multi_subject_grade_integrity.py` có `run_all_tests()` riêng, không được unittest tự thu thập như TestCase; nhánh thất bại chỉ print, không trả mã lỗi khác 0.
- Cần test database độc lập bằng DB tạm; không import UI để test thống kê và chấm điểm. Dùng Streamlit AppTest cho chuyển trạm, đổi môn/lớp, hết giờ/nộp hai lần và quyền quản trị.
- Trải nghiệm cần kiểm tra trên màn hình hẹp: giảm đoạn mô tả dài, phân vai học sinh/giáo viên rõ, giữ một hành động chính mỗi bước; thông báo tiến độ AI, retry và chi phí dễ hiểu.
- Đo chất lượng SVG/PDF/Word bằng render và kiểm tra thực tế; kiểm tra công thức, hình bắt buộc, ngắt trang, tiếng Việt, tương phản và bàn phím.

## 9. Kế hoạch cải tiến 6 tuần

Ước lượng cho một người phát triển chính, có giáo viên hỗ trợ duyệt nội dung. Thời lượng là dự kiến; không bao gồm thời gian thu thập đầy đủ bằng chứng nghiên cứu.

| Giai đoạn | Công việc cụ thể | Kết quả nghiệm thu | Phụ thuộc |
|---|---|---|---|
| Ngày 1–3 | F01, F02; bảo vệ khu vực dữ liệu; gắn nhãn demo ở BKT/lịch ôn/Cronbach; gỡ kết luận p-value viết sẵn | Không còn mật khẩu cố định; parser có ranh giới an toàn; dữ liệu mô phỏng nhận diện được | Bản sao cấu hình triển khai, dữ liệu kiểm thử |
| Ngày 4–7 | F03, F07; thống nhất scorer; schema đáp án và trạng thái kiểm chứng | Toàn bộ ca chấm chuẩn đạt; câu sai đáp án không mang cờ xác minh đúng | Chính sách chấm do giáo viên xác nhận |
| Tuần 2 | F08, F09; UUID, migration, FK/CHECK, outbox; backup/restore; item response có question_id/version | Không ghi đè sai; lớp đúng; restart/mất mạng không mất sự kiện; khôi phục được backup | Schema đã chốt |
| Tuần 3 | Chuẩn hóa nguồn gốc; audit trùng toàn nội dung; schema Ngữ văn; kho duyệt; chọn tập nội dung tin cậy | Mỗi câu phát hành có nguồn hoặc nhãn AI rõ ràng; giáo viên duyệt được bản sửa; báo cáo số lượng tái lập | CSDL và ID ổn định |
| Tuần 4 | Dùng dữ liệu thật cho BKT/review/psychometrics; sửa Monte Carlo; tách chế độ nghiên cứu và demo | Truy ngược được từ chỉ số đến dữ liệu gốc; thiếu mẫu không sinh kết luận | Nhật ký quan sát thật và rubric |
| Tuần 5 | Tách UI 4 trạm, AI gateway, scoring, research, repository; xóa định nghĩa trùng; lock dependencies; CI bắt toàn bộ test | Import service không dựng UI; test hồi quy đầy đủ; build tái lập | P0/P1 đã ổn định |
| Tuần 6 | AppTest, đánh giá OCR/đáp án với giáo viên, kiểm thử điện thoại/tải, đo latency và chi phí, pilot nhỏ | Biên bản lỗi và số liệu thật; tài liệu cài đặt, vận hành, giới hạn cập nhật | Tập câu/tài liệu chuẩn, người dùng thử |

Phạm vi pilot nên chọn **một môn và một khối có giáo viên duyệt** trước, chẳng hạn Toán 12 nếu phù hợp mục tiêu đề tài. Các môn khác có thể giữ khả dụng với trạng thái chất lượng minh bạch; việc có danh mục 13 môn không đồng nghĩa đã xác minh nội dung của cả 13 môn.

## 10. Backlog có thể triển khai

| ID | Đầu việc | Ưu tiên | Công dự kiến | Bằng chứng hoàn thành |
|---|---|---|---|---|
| B01 | Bỏ mật khẩu cố định, kiểm tra quyền đọc/xuất | P0 | 0,5–1 ngày | Test secret thiếu/sai/đúng và dữ liệu riêng |
| B02 | Parser toán và worker giới hạn tài nguyên | P0 | 1–3 ngày | Test cú pháp cấm, timeout, biểu thức hợp lệ |
| B03 | Một scorer, metadata dung sai, chuẩn boolean | P1 | 1–2 ngày | Bộ ca vàng do giáo viên xác nhận |
| B04 | Sửa phân loại cực trị và cờ verification | P1 | 1–2 ngày | x³/x⁴, miền xác định, đáp án sai |
| B05 | UUID, parse lớp và migration schema | P1 | 2–3 ngày | DB tạm và kiểm thử trùng/replay |
| B06 | Outbox retry, trạng thái đồng bộ, backup | P1 | 2–3 ngày | Kiểm thử mất mạng/khởi động lại/khôi phục |
| B07 | Nguồn gốc, phiên bản, kiểm duyệt và báo cáo trùng | P1 | 3–5 ngày + duyệt | Manifest nội dung và báo cáo tái lập |
| B08 | Nhật ký từng câu, ma trận chấm theo question_id | P1 | 2–3 ngày | So khớp thủ công từng ô một tập mẫu |
| B09 | Tách demo và dữ liệu thật, sửa thống kê/mô phỏng | P1 | 2–4 ngày | Báo cáo n/giả định/công thức đúng |
| B10 | BKT và lịch ôn từ quan sát thật | P2 | 3–5 ngày | Trạng thái riêng học sinh/kỹ năng, không có mẫu ẩn |
| B11 | Tách module, xóa trùng, gom xử lý lỗi | P2 | 4–6 ngày | Test dịch vụ độc lập, AppTest hồi quy |
| B12 | CI đầy đủ, lock dependencies, chỉ số vận hành | P2 | 2–3 ngày | Pipeline thất bại khi ca đa môn thất bại |
| B13 | Mobile, accessibility, xuất bản và load test | P2 | 3–5 ngày | Biên bản QA và kết quả đo |

Các ước lượng có thể chồng lấn, không cộng máy móc thành lịch cố định. Hạng mục dữ liệu phụ thuộc thời gian giáo viên duyệt.

## 11. Tiêu chí đo sau cải tiến

Các ngưỡng dưới đây là **mục tiêu đề xuất**, chưa phải kết quả hiện tại:

- 100% ca chấm điểm chuẩn đã thống nhất được chấm đúng; không bỏ qua biên dung sai/số 0/boolean.
- 100% câu phát hành thuộc tập pilot có trạng thái nguồn và duyệt; chỉ số quy mô phân biệt số đề, lượt câu, nội dung khác nhau và biến thể.
- Không mất/ghi đè sự kiện trong bộ test replay, restart và mất mạng; backup khôi phục thành công.
- Không truy cập chéo dữ liệu giữa tài khoản/phạm vi trong test quyền.
- Báo cáo OCR theo độ đúng trường đáp án/công thức và tỷ lệ cần xác nhận, có phân loại ảnh mờ và nhiều trang.
- Báo cáo gia sư theo rubric giáo viên: đúng kiến thức, gợi mở phù hợp, không tiết lộ đáp án sớm, biết yêu cầu làm rõ. Đánh giá độc lập với tập prompt phát triển.
- Đo p50/p95 latency cho nạp lạnh/nạp ấm, RAM theo số phiên và chi phí mỗi lượt học; đặt SLO sau benchmark, không ghi số hiệu năng từ chú thích mã.
- Thực nghiệm ghi rõ học sinh thật, cách phân nhóm, pre/post tương đương, mất mẫu và mức sử dụng. Có nhóm đối chứng khi muốn kết luận hiệu quả can thiệp; báo cáo bất định và hạn chế thay vì dùng mô phỏng làm bằng chứng nhân quả.

## 12. Thứ tự bắt đầu

Đợt sửa đầu tiên nên gồm B01–B04 và việc nhận diện dữ liệu demo, sau đó B05–B06. Đây là phần làm cho sản phẩm đáng tin hơn ngay lập tức. Sau khi chấm đúng và lưu đúng, mới mở rộng đánh giá nội dung và đo hiệu quả học tập.
