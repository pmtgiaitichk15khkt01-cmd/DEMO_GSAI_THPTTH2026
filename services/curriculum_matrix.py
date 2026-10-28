# VIP 76.0 - HỆ THỐNG GIA SƯ AI THPT 2026 (CHUẨN GDPT 2018)
# -*- coding: utf-8 -*-
"""
DỊCH VỤ MA TRẬN & BẢN ĐẶC TẢ ĐỀ THI CHUẨN BỘ GD&ĐT (Theo QĐ 764/QĐ-BGDĐT, CV 3175, TT 22/2021)
Phân tách độc lập, chuẩn chỉ theo từng môn học, đúng quy chuẩn sư phạm và pháp chế.
"""
import textwrap

def render_subject_exam_matrix_spec(subject: str, grade_num: int):

    """

    Hiển thị Khung Ma Trận & Bản Đặc Tả Đề Thi Chuẩn Bộ GD&ĐT (Theo QĐ 764/QĐ-BGDĐT, CV 3175, TT 22/2021)

    100% phân tách độc lập, chuẩn chỉ theo từng môn học, đúng quy chuẩn sư phạm và pháp chế.

    """

    if subject == "Ngữ văn":

        return f"""

        <div style="background: rgba(15, 23, 42, 0.7); border: 1.5px solid #0284c7; border-radius: 8px; padding: 12px 14px; margin-bottom: 8px;">

            <div style="color: #38bdf8; font-weight: 700; font-size: 14.5px; margin-bottom: 8px;">

                🏛️ Khung Ma Trận & Bản Đặc Tả Đề Thi 100% Tự Luận - Môn Ngữ văn (Lớp {grade_num}):

            </div>

            <div style="color: #e2e8f0; font-size: 12.5px; margin-bottom: 10px; line-height: 1.5;">

                ⚖️ <i>Căn cứ pháp quy: Quyết định số 764/QĐ-BGDĐT & Công văn số 3175/BGDĐT-GDTrH (Ngữ liệu 100% mới ngoài SGK, tiếp cận theo đặc trưng thể loại, đánh giá thực chất năng lực học sinh, tuyệt đối không dùng văn mẫu). Đề thi tự luận chung toàn quốc (không phân mã đề trắc nghiệm). Thời gian làm bài: 120 phút.</i>

            </div>

            <table style="width: 100%; border-collapse: collapse; font-size: 13px; color: #cbd5e1;">

                <tr style="border-bottom: 1.5px solid #334155; color: #38bdf8; font-weight: 600; background: rgba(30, 41, 59, 0.5);">

                    <td style="padding: 8px;">Phần thi / Cấu trúc</td>

                    <td style="padding: 8px;">Dạng thức & Số điểm</td>

                    <td style="padding: 8px;">Cấp độ nhận thức (Nhận biết & Thông hiểu)</td>

                    <td style="padding: 8px;">Cấp độ nhận thức (Vận dụng & Sáng tạo)</td>

                </tr>

                <tr style="border-bottom: 1px solid #1e293b;">

                    <td style="padding: 8px;"><b>PHẦN I: ĐỌC HIỂU</b><br><span style="color: #94a3b8; font-size: 11.5px;">(1 ngữ liệu mới ngoài SGK)</span></td>

                    <td style="padding: 8px; color: #34d399; font-weight: 600;"><b>4.0 điểm</b><br>(3 - 4 câu hỏi tự luận)</td>

                    <td style="padding: 8px;">• <b>Nhận biết (1.0đ):</b> Xác định thể loại, phương thức biểu đạt, nhân vật, chi tiết, từ ngữ hình ảnh tiêu biểu.<br>• <b>Thông hiểu (1.5đ):</b> Hiểu ý nghĩa chi tiết/hình tượng, tác dụng của biện pháp tu từ, tình cảm thái độ tác giả.</td>

                    <td style="padding: 8px;">• <b>Vận dụng (1.5đ):</b> Rút ra thông điệp cuộc sống sâu sắc nhất, bài học nhân sinh gắn liền thực tiễn bản thân; bày tỏ quan điểm đồng tình / không đồng tình với tư tưởng của tác giả.</td>

                </tr>

                <tr>

                    <td style="padding: 8px;"><b>PHẦN II: VIẾT</b><br><span style="color: #94a3b8; font-size: 11.5px;">(Tự luận làm văn)</span></td>

                    <td style="padding: 8px; color: #34d399; font-weight: 600;"><b>6.0 điểm</b><br>(Gồm 2 câu hỏi viết)</td>

                    <td style="padding: 8px;">• <b>Câu 1 - Đoạn NLXH (2.0đ):</b> Viết đoạn văn khoảng 200 chữ bàn về một vấn đề/tư tưởng xã hội gợi mở từ ngữ liệu Đọc hiểu. Yêu cầu mở đoạn trực tiếp, cắt nghĩa rõ ràng.</td>

                    <td style="padding: 8px;">• <b>Câu 2 - Bài NLVH (4.0đ):</b> Viết bài văn hoàn chỉnh phân tích, so sánh hoặc đánh giá nét đặc sắc về nội dung và nghệ thuật của tác phẩm/đoạn trích ngoài SGK theo đặc trưng thể loại; có liên hệ mở rộng và phong cách cá nhân.</td>

                </tr>

            </table>

        </div>

        """

    elif subject == "Tiếng Anh":

        return f"""

        <div style="background: rgba(15, 23, 42, 0.7); border: 1.5px solid #0284c7; border-radius: 8px; padding: 12px 14px; margin-bottom: 8px;">

            <div style="color: #38bdf8; font-weight: 700; font-size: 14.5px; margin-bottom: 8px;">

                🏛️ Khung Ma Trận & Bản Đặc Tả Đề Thi 40 Câu Trắc Nghiệm - Môn Tiếng Anh (Lớp {grade_num}):

            </div>

            <div style="color: #e2e8f0; font-size: 12.5px; margin-bottom: 10px; line-height: 1.5;">

                ⚖️ <i>Căn cứ pháp quy: Quyết định số 764/QĐ-BGDĐT & Khung năng lực ngoại ngữ 6 bậc dùng cho Việt Nam (tương đương CEFR B1 - B2). 100% Trắc nghiệm 4 lựa chọn (A, B, C, D) gồm 40 câu hỏi; KHÔNG CÓ Đúng/Sai (Phần II) và KHÔNG CÓ Điền số (Phần III). Thời gian làm bài: 50 phút. Mỗi câu 0.25 điểm x 40 = 10.0 điểm.</i>

            </div>

            <table style="width: 100%; border-collapse: collapse; font-size: 13px; color: #cbd5e1;">

                <tr style="border-bottom: 1.5px solid #334155; color: #38bdf8; font-weight: 600; background: rgba(30, 41, 59, 0.5);">

                    <td style="padding: 8px;">Mảng kiến thức / Dạng bài</td>

                    <td style="padding: 8px;">Số câu & Dạng thức</td>

                    <td style="padding: 8px;">Nhận biết & Thông hiểu</td>

                    <td style="padding: 8px;">Vận dụng & Vận dụng cao</td>

                </tr>

                <tr style="border-bottom: 1px solid #1e293b;">

                    <td style="padding: 8px;"><b>1. Phonetics (Ngữ âm)</b></td>

                    <td style="padding: 8px;">4 câu (4 chọn 1)</td>

                    <td style="padding: 8px;">Phát âm nguyên âm / phụ âm cơ bản, trọng âm từ 2 âm tiết.</td>

                    <td style="padding: 8px;">Trọng âm từ 3 âm tiết trở lên có hậu tố đặc biệt.</td>

                </tr>

                <tr style="border-bottom: 1px solid #1e293b;">

                    <td style="padding: 8px;"><b>2. Language Focus (Ngữ pháp & Từ vựng)</b></td>

                    <td style="padding: 8px;">12 câu (4 chọn 1)</td>

                    <td style="padding: 8px;">Thì động từ, câu bị động, mạo từ, giới từ, đại từ quan hệ ngoài SGK.</td>

                    <td style="padding: 8px;">Collocations, Phrasal verbs nâng cao, Idioms thông dụng, từ đồng nghĩa/trái nghĩa trong văn cảnh.</td>

                </tr>

                <tr style="border-bottom: 1px solid #1e293b;">

                    <td style="padding: 8px;"><b>3. Functional Exchanges (Giao tiếp)</b></td>

                    <td style="padding: 8px;">2 câu (4 chọn 1)</td>

                    <td style="padding: 8px;">Lời cảm ơn, xin lỗi, đề nghị, đáp lại lời khen trong đời sống.</td>

                    <td style="padding: 8px;">Bày tỏ quan điểm đồng tình / không đồng tình trong ngữ cảnh xã hội.</td>

                </tr>

                <tr style="border-bottom: 1px solid #1e293b;">

                    <td style="padding: 8px;"><b>4. Cloze Test (Đọc điền khuyết)</b></td>

                    <td style="padding: 8px;">5 câu (1 đoạn văn)</td>

                    <td style="padding: 8px;">Liên từ (Connectors), đại từ quan hệ, lượng từ (Quantifiers).</td>

                    <td style="padding: 8px;">Từ vựng chuyên đề học thuật (Academic vocabulary in context).</td>

                </tr>

                <tr style="border-bottom: 1px solid #1e293b;">

                    <td style="padding: 8px;"><b>5. Reading Comprehension (Đọc hiểu)</b></td>

                    <td style="padding: 8px;">12 câu (2 bài đọc)</td>

                    <td style="padding: 8px;">Xác định ý chính (Main idea), tìm kiếm thông tin chi tiết (Factual details).</td>

                    <td style="padding: 8px;">Từ quy chiếu (Reference), suy luận ngữ cảnh (Inference), thái độ tác giả (Tone/Attitude).</td>

                </tr>

                <tr>

                    <td style="padding: 8px;"><b>6. Sentence Transformation & Combining</b></td>

                    <td style="padding: 8px;">5 câu (4 chọn 1)</td>

                    <td style="padding: 8px;">Chuyển đổi câu đồng nghĩa (Câu gián tiếp, câu điều kiện, so sánh).</td>

                    <td style="padding: 8px;">Đảo ngữ (Inversion), câu điều kiện kết hợp, rút gọn mệnh đề quan hệ.</td>

                </tr>

            </table>

        </div>

        """

    elif subject == "Toán học":

        return f"""

        <div style="background: rgba(15, 23, 42, 0.7); border: 1.5px solid #0284c7; border-radius: 8px; padding: 12px 14px; margin-bottom: 8px;">

            <div style="color: #38bdf8; font-weight: 700; font-size: 14.5px; margin-bottom: 8px;">

                🏛️ Khung Ma Trận & Bản Đặc Tả Đề Thi Phân Hóa 3 Phần - Môn Toán học (Lớp {grade_num}):

            </div>

            <div style="color: #e2e8f0; font-size: 12.5px; margin-bottom: 10px; line-height: 1.5;">

                ⚖️ <i>Căn cứ pháp quy: Quyết định số 764/QĐ-BGDĐT. Cấu trúc 3 phần trắc nghiệm phân hóa năng lực, thời gian 90 phút. Tuyệt đối không dùng hàm trùng phương x^4 (đã loại bỏ khỏi CT 2018).</i>

            </div>

            <table style="width: 100%; border-collapse: collapse; font-size: 13px; color: #cbd5e1;">

                <tr style="border-bottom: 1.5px solid #334155; color: #38bdf8; font-weight: 600; background: rgba(30, 41, 59, 0.5);">

                    <td style="padding: 8px;">Phần thi / Cấu trúc</td>

                    <td style="padding: 8px;">Số câu & Dạng thức</td>

                    <td style="padding: 8px;">Nhận biết & Thông hiểu</td>

                    <td style="padding: 8px;">Vận dụng & Vận dụng cao</td>

                </tr>

                <tr style="border-bottom: 1px solid #1e293b;">

                    <td style="padding: 8px;"><b>Phần I: TN Nhiều lựa chọn</b></td>

                    <td style="padding: 8px; color: #34d399; font-weight: 600;">12 câu (3.0đ)<br>(0.25đ / câu)</td>

                    <td style="padding: 8px;">Khái niệm, định lý, công thức SGK KNTT, nhận diện bảng biến thiên, đồ thị hàm bậc ba, phân thức, Oxyz.</td>

                    <td style="padding: 8px;">Tính toán cơ bản, bài toán nhận biết điều kiện và nghiệm đơn giản.</td>

                </tr>

                <tr style="border-bottom: 1px solid #1e293b;">

                    <td style="padding: 8px;"><b>Phần II: TN Đúng / Sai</b></td>

                    <td style="padding: 8px; color: #34d399; font-weight: 600;">4 câu (4.0đ)<br>(Mỗi câu 4 ý a,b,c,d)</td>

                    <td style="padding: 8px;">Ý a, b kiểm tra dữ kiện bài toán, tính chất hình học, giới hạn, đạo hàm cơ bản.</td>

                    <td style="padding: 8px;">Ý c, d tính toán sâu, biện luận tham số m, liên hệ liên môn, phát hiện bẫy ngộ nhận (Thang điểm: 0.1 - 0.25 - 0.5 - 1.0đ).</td>

                </tr>

                <tr>

                    <td style="padding: 8px;"><b>Phần III: TN Trả lời ngắn</b></td>

                    <td style="padding: 8px; color: #34d399; font-weight: 600;">6 câu (3.0đ)<br>(0.5đ / câu)</td>

                    <td style="padding: 8px;">Giải quyết bài toán thực tế đơn giản, thống kê mẫu số liệu ghép nhóm.</td>

                    <td style="padding: 8px;">Mô hình hóa toán học, bài toán cực trị thực tế, tối ưu hóa kinh tế, Oxyz nâng cao. Điền số thực/nguyên ≤ 4 ký tự.</td>

                </tr>

            </table>

        </div>

        """

    elif subject == "Vật lý":

        return f"""

        <div style="background: rgba(15, 23, 42, 0.7); border: 1.5px solid #0284c7; border-radius: 8px; padding: 12px 14px; margin-bottom: 8px;">

            <div style="color: #38bdf8; font-weight: 700; font-size: 14.5px; margin-bottom: 8px;">

                🏛️ Khung Ma Trận & Bản Đặc Tả Đề Thi Phân Hóa 3 Phần - Môn Vật lý (Lớp {grade_num}):

            </div>

            <div style="color: #e2e8f0; font-size: 12.5px; margin-bottom: 10px; line-height: 1.5;">

                ⚖️ <i>Căn cứ pháp quy: Quyết định số 764/QĐ-BGDĐT. Cấu trúc 3 phần trắc nghiệm phân hóa năng lực, thời gian 50 phút. 100% chuẩn hệ đơn vị đo lường quốc tế SI, mô hình hóa các quá trình vật lý, đồ thị dao động, sóng và nhiệt động lực học. Tuyệt đối không dùng danh pháp hay phản ứng Hóa học.</i>

            </div>

            <table style="width: 100%; border-collapse: collapse; font-size: 13px; color: #cbd5e1;">

                <tr style="border-bottom: 1.5px solid #334155; color: #38bdf8; font-weight: 600; background: rgba(30, 41, 59, 0.5);">

                    <td style="padding: 8px;">Phần thi / Cấu trúc</td>

                    <td style="padding: 8px;">Số câu & Dạng thức</td>

                    <td style="padding: 8px;">Nhận biết & Thông hiểu</td>

                    <td style="padding: 8px;">Vận dụng & Vận dụng cao</td>

                </tr>

                <tr style="border-bottom: 1px solid #1e293b;">

                    <td style="padding: 8px;"><b>Phần I: TN Nhiều lựa chọn</b></td>

                    <td style="padding: 8px; color: #34d399; font-weight: 600;">18 câu (4.5đ)<br>(0.25đ / câu)</td>

                    <td style="padding: 8px;">Khái niệm, định luật vật lý cơ bản, công thức và đơn vị SI (Vận tốc, Gia tốc, Lực, Động năng, Thế năng, Chu kỳ, Bước sóng, Cường độ dòng điện, Từ trường, Nhiệt dung riêng...).</td>

                    <td style="padding: 8px;">Tính toán đơn giản, biến đổi công thức vật lý, giải thích hiện tượng tự nhiên và đời sống.</td>

                </tr>

                <tr style="border-bottom: 1px solid #1e293b;">

                    <td style="padding: 8px;"><b>Phần II: TN Đúng / Sai</b></td>

                    <td style="padding: 8px; color: #34d399; font-weight: 600;">4 câu (4.0đ)<br>(Mỗi câu 4 ý a,b,c,d)</td>

                    <td style="padding: 8px;">Ý a, b kiểm tra bản chất hiện tượng vật lý, sơ đồ bố trí thí nghiệm, đọc thông số đồ thị dao động/sóng.</td>

                    <td style="padding: 8px;">Ý c, d tính toán định lượng sâu, biện luận đồ thị biến thiên nhiệt độ - áp suất, mạch điện RLC, cảm ứng điện từ (Thang điểm: 0.1 - 0.25 - 0.5 - 1.0đ).</td>

                </tr>

                <tr>

                    <td style="padding: 8px;"><b>Phần III: TN Trả lời ngắn</b></td>

                    <td style="padding: 8px; color: #34d399; font-weight: 600;">6 câu (1.5đ)<br>(0.25đ / câu)</td>

                    <td style="padding: 8px;">Tính toán giá trị đại lượng vật lý cơ bản (Hiệu suất, Chu kỳ sóng, Điện trở tương đương, Nhiệt lượng).</td>

                    <td style="padding: 8px;">Bài toán mô hình kỹ thuật thực tiễn, tối ưu năng lượng, vật lý hạt nhân và công nghệ bán dẫn. Điền số ≤ 4 ký tự.</td>

                </tr>

            </table>

        </div>

        """

    elif subject == "Hóa học":

        return f"""

        <div style="background: rgba(15, 23, 42, 0.7); border: 1.5px solid #0284c7; border-radius: 8px; padding: 12px 14px; margin-bottom: 8px;">

            <div style="color: #38bdf8; font-weight: 700; font-size: 14.5px; margin-bottom: 8px;">

                🏛️ Khung Ma Trận & Bản Đặc Tả Đề Thi Phân Hóa 3 Phần - Môn Hóa học (Lớp {grade_num}):

            </div>

            <div style="color: #e2e8f0; font-size: 12.5px; margin-bottom: 10px; line-height: 1.5;">

                ⚖️ <i>Căn cứ pháp quy: Quyết định số 764/QĐ-BGDĐT. Cấu trúc 3 phần trắc nghiệm phân hóa năng lực, thời gian 50 phút. 100% chuẩn danh pháp quốc tế IUPAC theo CT GDPT 2018 (Ester, Lipid, Amine, Amino acid, Carbohydrate, Polymer, Phức chất...).</i>

            </div>

            <table style="width: 100%; border-collapse: collapse; font-size: 13px; color: #cbd5e1;">

                <tr style="border-bottom: 1.5px solid #334155; color: #38bdf8; font-weight: 600; background: rgba(30, 41, 59, 0.5);">

                    <td style="padding: 8px;">Phần thi / Cấu trúc</td>

                    <td style="padding: 8px;">Số câu & Dạng thức</td>

                    <td style="padding: 8px;">Nhận biết & Thông hiểu</td>

                    <td style="padding: 8px;">Vận dụng & Vận dụng cao</td>

                </tr>

                <tr style="border-bottom: 1px solid #1e293b;">

                    <td style="padding: 8px;"><b>Phần I: TN Nhiều lựa chọn</b></td>

                    <td style="padding: 8px; color: #34d399; font-weight: 600;">18 câu (4.5đ)<br>(0.25đ / câu)</td>

                    <td style="padding: 8px;">Cấu tạo nguyên tử, liên kết hóa học, biến thiên enthalpy chuẩn, cân bằng hóa học, gọi tên IUPAC và nhận diện nhóm chức hữu cơ.</td>

                    <td style="padding: 8px;">Dự đoán tính chất hóa lý, viết phương trình phản ứng, tính pH dung dịch, tính số mol / khối lượng chất phản ứng.</td>

                </tr>

                <tr style="border-bottom: 1px solid #1e293b;">

                    <td style="padding: 8px;"><b>Phần II: TN Đúng / Sai</b></td>

                    <td style="padding: 8px; color: #34d399; font-weight: 600;">4 câu (4.0đ)<br>(Mỗi câu 4 ý a,b,c,d)</td>

                    <td style="padding: 8px;">Ý a, b kiểm tra hiện tượng thí nghiệm hóa học thực hành, nhận định cấu trúc phân tử, cân bằng ion trong dung dịch.</td>

                    <td style="padding: 8px;">Ý c, d tính toán định lượng sâu, biện luận sơ đồ chuyển hóa hữu cơ/vô cơ, pin điện hóa và thế điện cực chuẩn (Thang điểm: 0.1 - 0.25 - 0.5 - 1.0đ).</td>

                </tr>

                <tr>

                    <td style="padding: 8px;"><b>Phần III: TN Trả lời ngắn</b></td>

                    <td style="padding: 8px; color: #34d399; font-weight: 600;">6 câu (1.5đ)<br>(0.25đ / câu)</td>

                    <td style="padding: 8px;">Tính toán đơn giản về hiệu suất phản ứng, phần trăm khối lượng, nồng độ mol, biến thiên enthalpy.</td>

                    <td style="padding: 8px;">Bài toán sản xuất công nghiệp thực tế, tối ưu hóa quá trình mạ điện/luyện kim, xử lý môi trường hóa chất. Điền số ≤ 4 ký tự.</td>

                </tr>

            </table>

        </div>

        """

    elif subject == "Sinh học":

        return f"""

        <div style="background: rgba(15, 23, 42, 0.7); border: 1.5px solid #0284c7; border-radius: 8px; padding: 12px 14px; margin-bottom: 8px;">

            <div style="color: #38bdf8; font-weight: 700; font-size: 14.5px; margin-bottom: 8px;">

                🏛️ Khung Ma Trận & Bản Đặc Tả Đề Thi Phân Hóa 3 Phần - Môn Sinh học (Lớp {grade_num}):

            </div>

            <div style="color: #e2e8f0; font-size: 12.5px; margin-bottom: 10px; line-height: 1.5;">

                ⚖️ <i>Căn cứ pháp quy: Quyết định số 764/QĐ-BGDĐT. Cấu trúc 3 phần trắc nghiệm phân hóa năng lực, thời gian 50 phút. Đánh giá toàn diện năng lực Nhận thức sinh học, Tìm hiểu thế giới sống và Vận dụng kiến thức di truyền - sinh thái thực tiễn.</i>

            </div>

            <table style="width: 100%; border-collapse: collapse; font-size: 13px; color: #cbd5e1;">

                <tr style="border-bottom: 1.5px solid #334155; color: #38bdf8; font-weight: 600; background: rgba(30, 41, 59, 0.5);">

                    <td style="padding: 8px;">Phần thi / Cấu trúc</td>

                    <td style="padding: 8px;">Số câu & Dạng thức</td>

                    <td style="padding: 8px;">Nhận biết & Thông hiểu</td>

                    <td style="padding: 8px;">Vận dụng & Vận dụng cao</td>

                </tr>

                <tr style="border-bottom: 1px solid #1e293b;">

                    <td style="padding: 8px;"><b>Phần I: TN Nhiều lựa chọn</b></td>

                    <td style="padding: 8px; color: #34d399; font-weight: 600;">18 câu (4.5đ)<br>(0.25đ / câu)</td>

                    <td style="padding: 8px;">Cơ chế di truyền phân tử (DNA, RNA, Mã di truyền), Nguyên phân - Giảm phân, Quy luật Mendel, Cấu trúc hệ sinh thái và bảo vệ môi trường.</td>

                    <td style="padding: 8px;">Phân biệt các dạng đột biến gen/NST, giải thích cơ chế điều hòa biểu hiện gen, chuỗi và lưới thức ăn.</td>

                </tr>

                <tr style="border-bottom: 1px solid #1e293b;">

                    <td style="padding: 8px;"><b>Phần II: TN Đúng / Sai</b></td>

                    <td style="padding: 8px; color: #34d399; font-weight: 600;">4 câu (4.0đ)<br>(Mỗi câu 4 ý a,b,c,d)</td>

                    <td style="padding: 8px;">Ý a, b kiểm tra dữ liệu nghiên cứu di truyền học, sơ đồ thí nghiệm vi sinh vật, chu trình tuần hoàn vật chất.</td>

                    <td style="padding: 8px;">Ý c, d phân tích phả hệ di truyền người, biện luận kiểu gen cơ thể bố mẹ, xác định tần số alen và cân bằng di truyền Hardy-Weinberg (Thang điểm: 0.1 - 0.25 - 0.5 - 1.0đ).</td>

                </tr>

                <tr>

                    <td style="padding: 8px;"><b>Phần III: TN Trả lời ngắn</b></td>

                    <td style="padding: 8px; color: #34d399; font-weight: 600;">6 câu (1.5đ)<br>(0.25đ / câu)</td>

                    <td style="padding: 8px;">Tính số liên kết hydrogen, số nucleotide từng loại, số loại kiểu gen tối đa trong phép lai đơn giản.</td>

                    <td style="padding: 8px;">Tính xác suất sinh con mang bệnh trong phả hệ, tính tần số hoán vị gen, bài toán chọn giống và năng suất sinh học. Điền số ≤ 4 ký tự.</td>

                </tr>

            </table>

        </div>

        """

    elif subject == "Khoa học tự nhiên":

        return f"""

        <div style="background: rgba(15, 23, 42, 0.7); border: 1.5px solid #0284c7; border-radius: 8px; padding: 12px 14px; margin-bottom: 8px;">

            <div style="color: #38bdf8; font-weight: 700; font-size: 14.5px; margin-bottom: 8px;">

                🏛️ Khung Ma Trận & Bản Đặc Tả Đề Thi Tích Hợp - Môn Khoa học tự nhiên (Lớp {grade_num}):

            </div>

            <div style="color: #e2e8f0; font-size: 12.5px; margin-bottom: 10px; line-height: 1.5;">

                ⚖️ <i>Căn cứ pháp quy: Thông tư 22/2021/TT-BGDĐT & Chương trình GDPT 2018 KNTT. Tích hợp 3 mạch nội dung: Chất và sự biến đổi của chất (Hóa học IUPAC), Năng lượng và sự biến đổi (Vật lý SI), Vật sống và Môi trường (Sinh thái & Sinh học).</i>

            </div>

            <table style="width: 100%; border-collapse: collapse; font-size: 13px; color: #cbd5e1;">

                <tr style="border-bottom: 1.5px solid #334155; color: #38bdf8; font-weight: 600; background: rgba(30, 41, 59, 0.5);">

                    <td style="padding: 8px;">Mảng nội dung KHTN</td>

                    <td style="padding: 8px;">Phân bố dạng thức</td>

                    <td style="padding: 8px;">Nhận biết & Thông hiểu</td>

                    <td style="padding: 8px;">Vận dụng & Thực hành</td>

                </tr>

                <tr style="border-bottom: 1px solid #1e293b;">

                    <td style="padding: 8px;"><b>1. Năng lượng & Biến đổi (Vật lý)</b></td>

                    <td style="padding: 8px;">Phần I (TN) + Phần II (Đ/S)</td>

                    <td style="padding: 8px;">Lực, Áp suất, Đòn bẩy, Mạch điện, Quang học, Năng lượng cơ học theo hệ SI.</td>

                    <td style="padding: 8px;">Tính công cơ học, tính công suất điện, thiết kế thí nghiệm quang học đời sống.</td>

                </tr>

                <tr style="border-bottom: 1px solid #1e293b;">

                    <td style="padding: 8px;"><b>2. Chất & Biến đổi chất (Hóa học)</b></td>

                    <td style="padding: 8px;">Phần I (TN) + Phần II (Đ/S)</td>

                    <td style="padding: 8px;">Nguyên tử, Bảng tuần hoàn, Axit - Bazơ, Kim loại - Phi kim theo danh pháp IUPAC.</td>

                    <td style="padding: 8px;">Tính khối lượng dung dịch, nồng độ %, viết PTHH và xử lý hiện tượng thực tế.</td>

                </tr>

                <tr>

                    <td style="padding: 8px;"><b>3. Vật sống & Môi trường (Sinh học)</b></td>

                    <td style="padding: 8px;">Phần I (TN) + Phần II (Đ/S)</td>

                    <td style="padding: 8px;">Tế bào, Các hệ cơ quan ở người, Di truyền học cơ bản, Hệ sinh thái KNTT.</td>

                    <td style="padding: 8px;">Giải thích cơ chế thích nghi, bảo vệ sức khỏe con người và đa dạng sinh học.</td>

                </tr>

            </table>

        </div>

        """

    elif subject == "Lịch sử":

        return f"""

        <div style="background: rgba(15, 23, 42, 0.7); border: 1.5px solid #0284c7; border-radius: 8px; padding: 12px 14px; margin-bottom: 8px;">

            <div style="color: #38bdf8; font-weight: 700; font-size: 14.5px; margin-bottom: 8px;">

                🏛️ Khung Ma Trận & Bản Đặc Tả Đề Thi Phân Hóa 2 Phần - Môn Lịch sử (Lớp {grade_num}):

            </div>

            <div style="color: #e2e8f0; font-size: 12.5px; margin-bottom: 10px; line-height: 1.5;">

                ⚖️ <i>Căn cứ pháp quy: Quyết định số 764/QĐ-BGDĐT. Cấu trúc 2 phần trắc nghiệm phân hóa năng lực, thời gian 50 phút (24 câu Phần I + 4 câu Phần II; KHÔNG CÓ Phần III). Khảo sát năng lực tư duy phản biện lịch sử và trích xuất tư liệu gốc.</i>

            </div>

            <table style="width: 100%; border-collapse: collapse; font-size: 13px; color: #cbd5e1;">

                <tr style="border-bottom: 1.5px solid #334155; color: #38bdf8; font-weight: 600; background: rgba(30, 41, 59, 0.5);">

                    <td style="padding: 8px;">Phần thi / Cấu trúc</td>

                    <td style="padding: 8px;">Số câu & Dạng thức</td>

                    <td style="padding: 8px;">Nhận biết & Thông hiểu</td>

                    <td style="padding: 8px;">Vận dụng & Vận dụng cao</td>

                </tr>

                <tr style="border-bottom: 1px solid #1e293b;">

                    <td style="padding: 8px;"><b>Phần I: TN Nhiều lựa chọn</b></td>

                    <td style="padding: 8px; color: #34d399; font-weight: 600;">24 câu (6.0đ)<br>(0.25đ / câu)</td>

                    <td style="padding: 8px;">Sự kiện lịch sử, mốc thời gian, nhân vật, bối cảnh ra đời các tổ chức quốc tế và phong trào cách mạng Việt Nam.</td>

                    <td style="padding: 8px;">Giải thích nguyên nhân thắng lợi, ý nghĩa lịch sử, tính chất cách mạng, so sánh hai giai đoạn lịch sử.</td>

                </tr>

                <tr>

                    <td style="padding: 8px;"><b>Phần II: TN Đúng / Sai</b></td>

                    <td style="padding: 8px; color: #34d399; font-weight: 600;">4 câu (4.0đ)<br>(Mỗi câu 4 ý a,b,c,d)</td>

                    <td style="padding: 8px;">Ý a, b trích dẫn đoạn tư liệu lịch sử gốc, văn kiện Đảng, phát biểu của các nguyên thủ quốc gia.</td>

                    <td style="padding: 8px;">Ý c, d đánh giá giá trị tư liệu, rút ra bài học kinh nghiệm cho công cuộc xây dựng và bảo vệ Tổ quốc hôm nay (Thang điểm: 0.1 - 0.25 - 0.5 - 1.0đ).</td>

                </tr>

            </table>

        </div>

        """

    elif subject in ["Địa lý", "Địa lí"]:

        return f"""

        <div style="background: rgba(15, 23, 42, 0.7); border: 1.5px solid #0284c7; border-radius: 8px; padding: 12px 14px; margin-bottom: 8px;">

            <div style="color: #38bdf8; font-weight: 700; font-size: 14.5px; margin-bottom: 8px;">

                🏛️ Khung Ma Trận & Bản Đặc Tả Đề Thi Phân Hóa 2 Phần - Môn Địa lí (Lớp {grade_num}):

            </div>

            <div style="color: #e2e8f0; font-size: 12.5px; margin-bottom: 10px; line-height: 1.5;">

                ⚖️ <i>Căn cứ pháp quy: Quyết định số 764/QĐ-BGDĐT. Cấu trúc 2 phần trắc nghiệm phân hóa năng lực, thời gian 50 phút (24 câu Phần I + 4 câu Phần II; KHÔNG CÓ Phần III). Khảo sát kỹ năng đọc Atlat, phân tích biểu đồ và bảng số liệu thống kê kinh tế - xã hội.</i>

            </div>

            <table style="width: 100%; border-collapse: collapse; font-size: 13px; color: #cbd5e1;">

                <tr style="border-bottom: 1.5px solid #334155; color: #38bdf8; font-weight: 600; background: rgba(30, 41, 59, 0.5);">

                    <td style="padding: 8px;">Phần thi / Cấu trúc</td>

                    <td style="padding: 8px;">Số câu & Dạng thức</td>

                    <td style="padding: 8px;">Nhận biết & Thông hiểu</td>

                    <td style="padding: 8px;">Vận dụng & Vận dụng cao</td>

                </tr>

                <tr style="border-bottom: 1px solid #1e293b;">

                    <td style="padding: 8px;"><b>Phần I: TN Nhiều lựa chọn</b></td>

                    <td style="padding: 8px; color: #34d399; font-weight: 600;">24 câu (6.0đ)<br>(0.25đ / câu)</td>

                    <td style="padding: 8px;">Quy luật địa lí tự nhiên, phân bố dân cư, tài nguyên thiên nhiên, đọc trang Atlat Địa lí Việt Nam.</td>

                    <td style="padding: 8px;">Phân tích cơ cấu kinh tế các vùng, chuyển dịch cơ cấu ngành, biến đổi khí hậu và phát triển bền vững.</td>

                </tr>

                <tr>

                    <td style="padding: 8px;"><b>Phần II: TN Đúng / Sai</b></td>

                    <td style="padding: 8px; color: #34d399; font-weight: 600;">4 câu (4.0đ)<br>(Mỗi câu 4 ý a,b,c,d)</td>

                    <td style="padding: 8px;">Ý a, b kiểm tra dữ liệu bảng số liệu xuất nhập khẩu, tăng trưởng GDP, số liệu khí tượng thủy văn.</td>

                    <td style="padding: 8px;">Ý c, d tính toán tốc độ tăng trưởng, so sánh quy mô/cơ cấu, biện luận giải pháp phát triển kinh tế biển đảo và liên kết vùng (Thang điểm: 0.1 - 0.25 - 0.5 - 1.0đ).</td>

                </tr>

            </table>

        </div>

        """

    elif subject in ["Lịch sử và Địa lý", "Lịch sử & Địa lý", "Lịch sử và Địa lí", "Lịch sử & Địa lí"]:
        return f"""
        <div style="background: rgba(15, 23, 42, 0.7); border: 1.5px solid #0284c7; border-radius: 8px; padding: 12px 14px; margin-bottom: 8px;">
            <div style="color: #38bdf8; font-weight: 700; font-size: 14.5px; margin-bottom: 8px;">
                🏛️ Khung Ma Trận & Bản Đặc Tả Đề Thi Phân Hóa - Môn Lịch sử và Địa lý (Lớp {grade_num}):
            </div>
            <div style="color: #e2e8f0; font-size: 12.5px; margin-bottom: 10px; line-height: 1.5;">
                ⚖️ <i>Căn cứ pháp quy: Chương trình GDPT 2018 cấp THCS (Bộ GD&ĐT). Tích hợp 2 phân môn Lịch sử & Địa lí với 2 dạng thức: Trắc nghiệm nhiều lựa chọn & Trắc nghiệm Đúng/Sai.</i>
            </div>
            <table style="width: 100%; border-collapse: collapse; font-size: 13px; color: #cbd5e1;">
                <tr style="border-bottom: 1.5px solid #334155; color: #38bdf8; font-weight: 600; background: rgba(30, 41, 59, 0.5);">
                    <td style="padding: 8px;">Phần thi / Phân môn</td>
                    <td style="padding: 8px;">Số câu & Dạng thức</td>
                    <td style="padding: 8px;">Nhận biết & Thông hiểu</td>
                    <td style="padding: 8px;">Vận dụng & Vận dụng cao</td>
                </tr>
                <tr style="border-bottom: 1px solid #1e293b;">
                    <td style="padding: 8px;"><b>Phần I: TN Nhiều lựa chọn</b></td>
                    <td style="padding: 8px; color: #34d399; font-weight: 600;">24 câu (6.0đ)<br>(12 câu Sử + 12 câu Địa)</td>
                    <td style="padding: 8px;">Sự kiện, nhân vật lịch sử trọng đại, quy luật tự nhiên, địa hình và vị trí địa lý.</td>
                    <td style="padding: 8px;">Đọc Atlat, biểu đồ kinh tế, giải thích nguyên nhân - kết quả của các sự kiện lịch sử.</td>
                </tr>
                <tr>
                    <td style="padding: 8px;"><b>Phần II: TN Đúng / Sai</b></td>
                    <td style="padding: 8px; color: #34d399; font-weight: 600;">4 câu (4.0đ)<br>(2 câu Sử + 2 câu Địa)</td>
                    <td style="padding: 8px;">Ý a, b kiểm tra dữ liệu tư liệu lịch sử gốc và bảng thống kê địa lí dân cư.</td>
                    <td style="padding: 8px;">Ý c, d phân tích bài học lịch sử, tính toán tốc độ tăng trưởng và liên hệ thực tiễn (0.1 - 0.25 - 0.5 - 1.0đ).</td>
                </tr>
            </table>
        </div>
        """

    elif subject in ["Giáo dục Kinh tế và Pháp luật", "GDKT&PL", "Giáo dục kinh tế và pháp luật", "Giáo dục công dân"]:

        return f"""

        <div style="background: rgba(15, 23, 42, 0.7); border: 1.5px solid #0284c7; border-radius: 8px; padding: 12px 14px; margin-bottom: 8px;">

            <div style="color: #38bdf8; font-weight: 700; font-size: 14.5px; margin-bottom: 8px;">

                🏛️ Khung Ma Trận & Bản Đặc Tả Đề Thi Phân Hóa 2 Phần - Môn GDKT & Pháp luật (Lớp {grade_num}):

            </div>

            <div style="color: #e2e8f0; font-size: 12.5px; margin-bottom: 10px; line-height: 1.5;">

                ⚖️ <i>Căn cứ pháp quy: Quyết định số 764/QĐ-BGDĐT. Cấu trúc 2 phần trắc nghiệm phân hóa năng lực, thời gian 50 phút (24 câu Phần I + 4 câu Phần II; KHÔNG CÓ Phần III). Khảo sát năng lực điều chỉnh hành vi pháp luật và phân tích tình huống kinh tế đời sống.</i>

            </div>

            <table style="width: 100%; border-collapse: collapse; font-size: 13px; color: #cbd5e1;">

                <tr style="border-bottom: 1.5px solid #334155; color: #38bdf8; font-weight: 600; background: rgba(30, 41, 59, 0.5);">

                    <td style="padding: 8px;">Phần thi / Cấu trúc</td>

                    <td style="padding: 8px;">Số câu & Dạng thức</td>

                    <td style="padding: 8px;">Nhận biết & Thông hiểu</td>

                    <td style="padding: 8px;">Vận dụng & Xử lý tình huống</td>

                </tr>

                <tr style="border-bottom: 1px solid #1e293b;">

                    <td style="padding: 8px;"><b>Phần I: TN Nhiều lựa chọn</b></td>

                    <td style="padding: 8px; color: #34d399; font-weight: 600;">24 câu (6.0đ)<br>(0.25đ / câu)</td>

                    <td style="padding: 8px;">Khái niệm cung - cầu, giá cả thị trường, lạm phát, thất nghiệp, hệ thống chính trị và các quyền tự do cơ bản của công dân.</td>

                    <td style="padding: 8px;">Hiểu vai trò của ngân sách nhà nước, chính sách bảo hiểm, trách nhiệm pháp lý của công dân trong xã hội.</td>

                </tr>

                <tr>

                    <td style="padding: 8px;"><b>Phần II: TN Đúng / Sai</b></td>

                    <td style="padding: 8px; color: #34d399; font-weight: 600;">4 câu (4.0đ)<br>(Mỗi câu 4 ý a,b,c,d)</td>

                    <td style="padding: 8px;">Ý a, b trích dẫn tình huống thực tế về kinh doanh, giao kết hợp đồng lao động, thực thi quyền dân chủ.</td>

                    <td style="padding: 8px;">Ý c, d phân định hành vi vi phạm pháp luật dân sự / hành chính / hình sự, tư vấn giải pháp ứng xử đúng pháp luật (Thang điểm: 0.1 - 0.25 - 0.5 - 1.0đ).</td>

                </tr>

            </table>

        </div>

        """

    elif subject == "Tin học":

        return f"""

        <div style="background: rgba(15, 23, 42, 0.7); border: 1.5px solid #0284c7; border-radius: 8px; padding: 12px 14px; margin-bottom: 8px;">

            <div style="color: #38bdf8; font-weight: 700; font-size: 14.5px; margin-bottom: 8px;">

                🏛️ Khung Ma Trận & Bản Đặc Tả Đề Thi Phân Hóa 2 Phần - Môn Tin học (Lớp {grade_num}):

            </div>

            <div style="color: #e2e8f0; font-size: 12.5px; margin-bottom: 10px; line-height: 1.5;">

                ⚖️ <i>Căn cứ pháp quy: Quyết định số 764/QĐ-BGDĐT. Cấu trúc 2 phần trắc nghiệm phân hóa năng lực, thời gian 50 phút (24 câu Phần I + 4 câu Phần II; KHÔNG CÓ Phần III). Đánh giá tư duy thuật toán, kỹ năng lập trình Python/C++ và kiến trúc hệ thống mạng - CSDL.</i>

            </div>

            <table style="width: 100%; border-collapse: collapse; font-size: 13px; color: #cbd5e1;">

                <tr style="border-bottom: 1.5px solid #334155; color: #38bdf8; font-weight: 600; background: rgba(30, 41, 59, 0.5);">

                    <td style="padding: 8px;">Phần thi / Cấu trúc</td>

                    <td style="padding: 8px;">Số câu & Dạng thức</td>

                    <td style="padding: 8px;">Nhận biết & Thông hiểu</td>

                    <td style="padding: 8px;">Vận dụng & Tối ưu giải thuật</td>

                </tr>

                <tr style="border-bottom: 1px solid #1e293b;">

                    <td style="padding: 8px;"><b>Phần I: TN Nhiều lựa chọn</b></td>

                    <td style="padding: 8px; color: #34d399; font-weight: 600;">24 câu (6.0đ)<br>(0.25đ / câu)</td>

                    <td style="padding: 8px;">Cú pháp ngôn ngữ lập trình Python, kiểu dữ liệu danh sách/từ điển, kiến trúc mạng máy tính, bảng trong CSDL quan hệ.</td>

                    <td style="padding: 8px;">Đọc hiểu đoạn mã nguồn, dự đoán kết quả đầu ra, thiết kế câu truy vấn SQL đơn giản.</td>

                </tr>

                <tr>

                    <td style="padding: 8px;"><b>Phần II: TN Đúng / Sai</b></td>

                    <td style="padding: 8px; color: #34d399; font-weight: 600;">4 câu (4.0đ)<br>(Mỗi câu 4 ý a,b,c,d)</td>

                    <td style="padding: 8px;">Ý a, b kiểm tra dữ kiện giải thuật tìm kiếm, sắp xếp, mô hình an toàn mạng và bản quyền phần mềm.</td>

                    <td style="padding: 8px;">Ý c, d phân tích độ phức tạp thời gian O(n), phát hiện lỗi logic trong mã nguồn, tối ưu hóa thuật toán đệ quy/quy hoạch động (Thang điểm: 0.1 - 0.25 - 0.5 - 1.0đ).</td>

                </tr>

            </table>

        </div>

        """

    elif subject == "Công nghệ":

        return f"""

        <div style="background: rgba(15, 23, 42, 0.7); border: 1.5px solid #0284c7; border-radius: 8px; padding: 12px 14px; margin-bottom: 8px;">

            <div style="color: #38bdf8; font-weight: 700; font-size: 14.5px; margin-bottom: 8px;">

                🏛️ Khung Ma Trận & Bản Đặc Tả Đề Thi Phân Hóa 2 Phần - Môn Công nghệ (Lớp {grade_num}):

            </div>

            <div style="color: #e2e8f0; font-size: 12.5px; margin-bottom: 10px; line-height: 1.5;">

                ⚖️ <i>Căn cứ pháp quy: Quyết định số 764/QĐ-BGDĐT. Cấu trúc 2 phần trắc nghiệm phân hóa năng lực, thời gian 50 phút (24 câu Phần I + 4 câu Phần II; KHÔNG CÓ Phần III). Khảo sát năng lực thiết kế kỹ thuật, đọc bản vẽ cơ khí - điện tử và ứng dụng công nghệ đời sống.</i>

            </div>

            <table style="width: 100%; border-collapse: collapse; font-size: 13px; color: #cbd5e1;">

                <tr style="border-bottom: 1.5px solid #334155; color: #38bdf8; font-weight: 600; background: rgba(30, 41, 59, 0.5);">

                    <td style="padding: 8px;">Phần thi / Cấu trúc</td>

                    <td style="padding: 8px;">Số câu & Dạng thức</td>

                    <td style="padding: 8px;">Nhận biết & Thông hiểu</td>

                    <td style="padding: 8px;">Vận dụng & Thiết kế kỹ thuật</td>

                </tr>

                <tr style="border-bottom: 1px solid #1e293b;">

                    <td style="padding: 8px;"><b>Phần I: TN Nhiều lựa chọn</b></td>

                    <td style="padding: 8px; color: #34d399; font-weight: 600;">24 câu (6.0đ)<br>(0.25đ / câu)</td>

                    <td style="padding: 8px;">Tiêu chuẩn bản vẽ kỹ thuật, vật liệu cơ khí, linh kiện điện tử, sơ đồ mạch điều khiển, công nghệ trồng trọt / chăn nuôi KNTT.</td>

                    <td style="padding: 8px;">Đọc hiểu sơ đồ nguyên lý hoạt động của thiết bị, quy trình gia công cơ khí và an toàn lao động.</td>

                </tr>

                <tr>

                    <td style="padding: 8px;"><b>Phần II: TN Đúng / Sai</b></td>

                    <td style="padding: 8px; color: #34d399; font-weight: 600;">4 câu (4.0đ)<br>(Mỗi câu 4 ý a,b,c,d)</td>

                    <td style="padding: 8px;">Ý a, b kiểm tra dữ liệu sơ đồ mạch điện thông minh, hệ thống cơ cấu truyền động, quy trình công nghệ sinh học.</td>

                    <td style="padding: 8px;">Ý c, d tính toán công suất thiết bị, phát hiện sự cố kỹ thuật, tối ưu hóa quy trình thiết kế và đánh giá hiệu quả kinh tế (Thang điểm: 0.1 - 0.25 - 0.5 - 1.0đ).</td>

                </tr>

            </table>

        </div>

        """

    else:

        return f"""

        <div style="background: rgba(15, 23, 42, 0.7); border: 1.5px solid #0284c7; border-radius: 8px; padding: 12px 14px; margin-bottom: 8px;">

            <div style="color: #38bdf8; font-weight: 700; font-size: 14.5px; margin-bottom: 8px;">

                🏛️ Khung Ma Trận & Bản Đặc Tả Đề Thi Chuẩn Bộ GD&ĐT - Môn {subject} (Lớp {grade_num}):

            </div>

            <div style="color: #e2e8f0; font-size: 12.5px; margin-bottom: 10px; line-height: 1.5;">

                ⚖️ <i>Căn cứ pháp quy: Quyết định số 764/QĐ-BGDĐT & Chương trình GDPT 2018 KNTT. Cấu trúc trắc nghiệm phân hóa năng lực, thời gian 50 phút.</i>

            </div>

            <table style="width: 100%; border-collapse: collapse; font-size: 13px; color: #cbd5e1;">

                <tr style="border-bottom: 1.5px solid #334155; color: #38bdf8; font-weight: 600; background: rgba(30, 41, 59, 0.5);">

                    <td style="padding: 8px;">Phần thi / Cấu trúc</td>

                    <td style="padding: 8px;">Số câu & Dạng thức</td>

                    <td style="padding: 8px;">Nhận biết & Thông hiểu</td>

                    <td style="padding: 8px;">Vận dụng & Vận dụng cao</td>

                </tr>

                <tr style="border-bottom: 1px solid #1e293b;">

                    <td style="padding: 8px;"><b>Phần I: TN Nhiều lựa chọn</b></td>

                    <td style="padding: 8px; color: #34d399; font-weight: 600;">24 câu (6.0đ)<br>(0.25đ / câu)</td>

                    <td style="padding: 8px;">Khái niệm cơ bản, quy luật kỹ thuật, thiết kế công nghệ và giải pháp thực tiễn.</td>

                    <td style="padding: 8px;">Ứng dụng công nghệ, phân tích sơ đồ nguyên lý hoạt động.</td>

                </tr>

                <tr>

                    <td style="padding: 8px;"><b>Phần II: TN Đúng / Sai</b></td>

                    <td style="padding: 8px; color: #34d399; font-weight: 600;">4 câu (4.0đ)<br>(Mỗi câu 4 ý a,b,c,d)</td>

                    <td style="padding: 8px;">Ý a, b kiểm tra quy trình công nghệ, tiêu chuẩn kỹ thuật an toàn.</td>

                    <td style="padding: 8px;">Ý c, d tính toán kinh tế kỹ thuật, xử lý sự cố công nghệ thực tiễn (Thang điểm: 0.1 - 0.25 - 0.5 - 1.0đ).</td>

                </tr>

            </table>

        </div>

        """

import textwrap
_raw_render_subject_exam_matrix_spec = render_subject_exam_matrix_spec

def render_subject_exam_matrix_spec(subject: str, grade_num: int) -> str:
    res = _raw_render_subject_exam_matrix_spec(subject, grade_num)
    if res and isinstance(res, str):
        return "\n".join(line.lstrip() for line in res.splitlines())
    return ""

