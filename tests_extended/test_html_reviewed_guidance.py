import unittest

from services.curriculum_policy import correct_reviewed_html_guidance
from services.lesson_sources import reviewed_lesson_sources, apply_reviewed_essay_labels


class ReviewedHTMLGuidanceTests(unittest.TestCase):
    topic = 'Tin học 12 KNTT: cấu trúc HTML và các thẻ văn bản cơ bản'

    def repair(self, text, subject='Tin học', grade=12, topic=None):
        return correct_reviewed_html_guidance(text, subject, grade, topic or self.topic)

    def test_fresh_real_lesson_does_not_disguise_supplied_errors_as_student_work(self):
        text = ('Bước 3: Thực hiện kế hoạch: (Học sinh tự liệt kê các lỗi như: thiếu dấu >, '
                'thiếu thẻ `<ol>` bao quanh `<li>`, nội dung trong `<head>` thiếu thẻ `<title>`...).')
        fixed = self.repair(text)
        self.assertNotIn('thiếu thẻ', fixed)
        self.assertIn('Em tự tìm lỗi', fixed)
        self.assertIn('Bước 3', fixed)
        code = '```text\n' + text + '\n```'
        self.assertEqual(self.repair(code), code)
        self.assertEqual(self.repair(text, 'Ngữ văn'), text)

    def test_observed_claims_are_qualified_without_changing_code_or_key(self):
        code = '```html\n<p>lớn và đậm nhất<br>Xin chào</p>\n```'
        text = ('Tiêu đề lớn và đậm nhất.\n'
                'Kiểm tra xem các thẻ đã có đủ thẻ đóng chưa?\n'
                'Sự khác biệt chính giữa việc sử dụng thẻ `<br>` và thẻ `<p>` khi trình bày văn bản là gì?\n'
                'D. `<p>` tạo ra một đoạn văn có khoảng cách phía trên và dưới.\nCORRECT: D\n'
                '`lớn và đậm nhất`\n' + code)
        fixed = self.repair(text)
        self.assertIn('chưa tùy chỉnh CSS', fixed)
        self.assertIn('br không có thẻ đóng', fixed)
        self.assertIn(code, fixed)
        self.assertIn('`lớn và đậm nhất`', fixed)
        self.assertIn('CORRECT: D', fixed)
        self.assertIn('D. `<p>` tạo ra một đoạn văn có khoảng cách phía trên và dưới.', fixed)
        self.assertEqual(self.repair(fixed), fixed)

    def test_observed_answer_giving_hint_becomes_student_task(self):
        text = ('Hướng dẫn bạn thay thế đoạn mã sai bằng các thẻ đúng: thêm thẻ `<title>`, '
                'sửa lại dấu `< >` cho `<h1>`, và bao quanh các thẻ `<li>` bằng thẻ danh sách phù hợp.')
        fixed = self.repair(text)
        self.assertNotIn('thêm thẻ', fixed)
        self.assertIn('tự đề xuất', fixed)
        self.assertIn('trước và sau', fixed)
        plan = ('Tìm các quy tắc bị vi phạm: (1) Nội dung tiêu đề trang phải nằm trong thẻ nào bên trong `<head>`? '
                '(2) Cú pháp đóng/mở thẻ `<h1>` đúng là gì? (3) Thẻ `<li>` có thể đứng độc lập mà không có thẻ cha '
                '(`<ul>` hoặc `<ol>`) không?')
        fixed_plan = self.repair(plan)
        self.assertNotIn('`<head>`', fixed_plan)
        self.assertNotIn('`<ol>`', fixed_plan)
        self.assertIn('tự xác định', fixed_plan)

    def test_other_subject_grade_topic_and_valid_guidance_stay_unchanged(self):
        text = 'Kiểm tra xem các thẻ đã có đủ thẻ đóng chưa?'
        for subject, grade, topic in [('Ngữ văn', 12, self.topic),
                                       ('Tin học', 11, self.topic),
                                       ('Tin học', 12, 'Mạng máy tính')]:
            self.assertEqual(self.repair(text, subject, grade, topic), text)
        valid = 'Hãy tự kiểm cấu trúc và đối chiếu mã nguồn với yêu cầu của đề.'
        self.assertEqual(self.repair(valid), valid)

    def test_source_covers_exact_combined_topic_without_approving_other_lessons(self):
        review = reviewed_lesson_sources('Tin học', 12, self.topic)
        self.assertEqual(review['status'], 'reviewed_requirements_source')
        self.assertIn('Bài 7', review['sources'][0]['locator'])
        self.assertIn('Bài 9', review['sources'][0]['locator'])
        self.assertNotIn('accepted', review)
        self.assertEqual(reviewed_lesson_sources('Tin học', 12, 'HTML nâng cao')['status'],
                         'missing_lesson_review')

    def test_actual_station1_gate_and_export_keep_the_reviewed_fix(self):
        import real_exam_engine as ree
        from tests.test_expert_patch_regressions import load_function
        from services.academic_context import academic_context
        from services.curriculum_policy import (correct_khtn8_lime_soil_confusion,
            validate_lesson_policy, T1_CONTEXT_REVISION)
        from services.lesson_export import build_lesson_html
        legacy = load_function('_legacy_sanitize_katex_latex')
        sanitize = load_function('sanitize_katex_latex', _legacy_sanitize_katex_latex=legacy)
        gate = load_function('station1_master_sovereign_brain_gate', ree=ree,
            academic_context=academic_context, validate_lesson_policy=validate_lesson_policy,
            sanitize_katex_latex=sanitize, CURRICULUM_POLICY_REVISION=T1_CONTEXT_REVISION,
            correct_khtn8_lime_soil_confusion=correct_khtn8_lime_soil_confusion)
        fixed = gate('Kiểm tra xem các thẻ đã có đủ thẻ đóng chưa?',
                     'Tin học', 12, self.topic)
        self.assertIn('br không có thẻ đóng', fixed)
        page = build_lesson_html('Tin học', 12, self.topic, fixed)
        self.assertIn('br không có thẻ đóng', page)
        self.assertIn('4489779231', page)

    def test_reviewed_debugging_level_matches_code_and_ignores_guidance_heading(self):
        review = reviewed_lesson_sources('Tin học', 12, self.topic)
        stem = review['assessment_decisions'][0]['question']
        text = ('**Câu 2. [Mức độ: VDC]** ' + stem
                + '\n**Gợi ý thực hiện theo 4 bước:**\n- **Bước 1: Tìm hiểu đề:** Quan sát.')
        fixed = apply_reviewed_essay_labels(text, 'Tin học', 12, self.topic)
        self.assertIn('[Mức độ: VD]', fixed)
        self.assertEqual(apply_reviewed_essay_labels(fixed, 'Tin học', 12, self.topic), fixed)
        other = text.replace('Bài 2', 'Bài 3')
        self.assertEqual(apply_reviewed_essay_labels(other, 'Tin học', 12, self.topic), other)

    def test_archived_tutor_tags_are_code_while_math_and_examples_are_preserved(self):
        text = r'Phân biệt $<head>$ và \(<body>\). Toán $a<b$ và $x^2$. `<p>`'
        fixed = self.repair(text)
        self.assertIn('`<head>`', fixed)
        self.assertIn('`<body>`', fixed)
        self.assertIn('$a<b$ và $x^2$', fixed)
        code = '```html\n$<head>$\n```\n`$<body>$`'
        self.assertEqual(self.repair(code), code)
        self.assertEqual(self.repair(fixed), fixed)

    def test_observed_closure_code_punctuation_is_not_math(self):
        text = r'Dấu $/$ và cặp ngoặc $<>$; toán $a<b$ và $a/b$.'
        fixed = self.repair(text)
        self.assertIn('`/`', fixed)
        self.assertIn('`<>`', fixed)
        self.assertIn('$a<b$ và $a/b$', fixed)
        self.assertEqual(self.repair(text, 'Toán học'), text)
        self.assertEqual(self.repair('```text\n' + text + '\n```'), '```text\n' + text + '\n```')
