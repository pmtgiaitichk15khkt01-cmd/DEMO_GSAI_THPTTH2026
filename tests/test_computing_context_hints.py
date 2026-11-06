import unittest

from data.socratic_anchors import sanitize_socratic_hint
from services.academic_context import subjects_for_grade


class TestComputingContextHints(unittest.TestCase):
    def test_live_html_body_question_gets_task_specific_fallback_without_tag_answer(self):
        question = 'Trong cấu trúc của một trang HTML, toàn bộ nội dung mà người dùng nhìn thấy trên trình duyệt phải đặt ở đâu?'
        generic = 'Em cần xác định đầu vào, đầu ra hoặc quy tắc hoạt động nào trong tình huống được nêu?'
        fixed = sanitize_socratic_hint(generic, q_text=question, subject='Tin học', grade_num=12)
        self.assertIn('thông tin về tài liệu', fixed)
        self.assertNotEqual(fixed, generic)
        self.assertNotIn('body', fixed.lower())
        self.assertNotIn('head', fixed.lower())
        valid = 'Em sẽ phân loại vai trò của các thành phần trong tài liệu như thế nào?'
        self.assertEqual(sanitize_socratic_hint(valid, q_text=question, subject='Tin học'), valid)
    def test_archived_html_order_cue_is_repaired_without_naming_the_answer(self):
        question = 'Thẻ HTML nào dùng để tạo danh sách có thứ tự?'
        options = ['A. `<ul>`', 'B. `<ol>`', 'C. `<li>`', 'D. `<p>`']
        leaked = 'Trong tiếng Anh, từ Order có nghĩa là gì? Nó liên quan gì đến việc sắp xếp theo trình tự 1, 2, 3?'
        fixed = sanitize_socratic_hint(leaked, 'B', question, options, subject='Tin học', grade_num=12)
        self.assertNotEqual(fixed, leaked)
        self.assertNotIn('Order', fixed)
        self.assertNotIn('<ol>', fixed)
        self.assertNotIn('1, 2, 3', fixed)
        supplied = 'Em cần phân biệt vai trò của phần tử bao ngoài và từng mục như thế nào?'
        self.assertEqual(sanitize_socratic_hint(supplied, 'B', question, options,
                         subject='Tin học', grade_num=12), supplied)

    def test_live_cpu_metaphor_is_replaced_without_changing_valid_hint(self):
        question = 'Phát biểu nào sau đây về CPU là ĐÚNG?'
        leaked = "Thành phần nào được ví như 'bộ não' điều phối mọi hoạt động suy nghĩ và tính toán của máy tính?"
        options = ['A. Lưu trữ lâu dài', 'B. CPU là bộ não, tính toán và điều khiển',
                   'C. Hiển thị', 'D. Thiết bị ra']
        for grade in range(6, 13):
            result = sanitize_socratic_hint(leaked, 'B', question, options,
                                            subject='Tin học', grade_num=grade)
            self.assertIn('phân biệt', result)
            self.assertNotIn('bộ não', result)
            self.assertTrue(result.endswith('?'))
        supplied = 'Em sẽ dùng tiêu chí nào để kiểm tra chức năng của từng thành phần?'
        self.assertEqual(sanitize_socratic_hint(supplied, q_text=question,
                                              subject='Tin học'), supplied)

    def test_live_storage_and_connection_fallbacks_match_task_without_solution(self):
        storage = sanitize_socratic_hint('', '4096',
            'Thẻ nhớ dung lượng 16 GB, bức ảnh 4 MB; tối đa bao nhiêu ảnh?', subject='Tin học')
        self.assertIn('cùng đơn vị', storage)
        self.assertIn('phần dư', storage)
        for value in ('4096', '1024', '16', '4 MB'):
            self.assertNotIn(value, storage)
        connection = sanitize_socratic_hint('', q_text=
            'Sự đa dạng của các thiết bị số và khả năng kết nối của chúng', subject='Tin học')
        self.assertIn('từng nhận định', connection)
        self.assertNotIn('HDMI', connection)

    def test_all_contexts_keep_unrelated_valid_hints(self):
        hint = 'Em cần đối chiếu dữ kiện nào trước khi kiểm tra phát biểu?'
        for grade in range(6, 13):
            for subject in subjects_for_grade(grade):
                self.assertEqual(sanitize_socratic_hint(hint, q_text='Nhiệm vụ học tập.',
                    subject=subject, grade_num=grade), hint)
        self.assertNotIn('CPU', sanitize_socratic_hint('', q_text='CPU', subject='Ngữ văn'))

    def test_live_card_count_does_not_ask_for_file_count_or_assume_file_splitting(self):
        question = ('Một tệp video có dung lượng là 4 GB. Lưu tệp vào các thẻ nhớ '
                    'có dung lượng mỗi thẻ là 1024 MB thì cần ít nhất bao nhiêu thẻ nhớ?')
        for grade in range(6, 13):
            result = sanitize_socratic_hint('', '4', question, subject='Tin học', grade_num=grade)
            self.assertIn('số thiết bị', result)
            self.assertIn('điều kiện chia tệp', result)
            self.assertNotIn('số tệp', result)
            self.assertNotIn('4', result)
            self.assertNotIn('1024', result)
        supplied = 'Em cần kiểm tra giả thiết nào trước khi xác định số thẻ cần dùng?'
        self.assertEqual(sanitize_socratic_hint(supplied, q_text=question, subject='Tin học'), supplied)


if __name__ == '__main__':
    unittest.main()
