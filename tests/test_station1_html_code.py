import unittest

import real_exam_engine as ree
from services.academic_context import academic_context, subjects_for_grade
from services.curriculum_policy import (T1_CONTEXT_REVISION as CURRICULUM_POLICY_REVISION,
    correct_khtn8_lime_soil_confusion, validate_lesson_policy)
from tests.test_expert_patch_regressions import load_function


class Station1HTMLCodeTests(unittest.TestCase):
    def test_cleanup_preserves_html_literals_in_inline_and_fenced_code(self):
        text = 'Thẻ `<p>`, `<br>`, `<b>` và `<i>`\n```html\n<p>Xin chào<br>lớp 12</p>\n```'
        self.assertEqual(ree.deep_clean_pua_and_artifacts(text), text)

    def test_cleanup_still_removes_prose_markup_and_artifacts(self):
        text = '<b>Kiến thức</b>\u200b \ue000 và `<b>`'
        self.assertEqual(ree.deep_clean_pua_and_artifacts(text), 'Kiến thức  và `<b>`')

    def test_actual_station1_gate_preserves_code_for_all_supported_contexts(self):
        legacy = load_function('_legacy_sanitize_katex_latex')
        sanitize = load_function('sanitize_katex_latex', _legacy_sanitize_katex_latex=legacy)
        gate = load_function('station1_master_sovereign_brain_gate', ree=ree,
            academic_context=academic_context, validate_lesson_policy=validate_lesson_policy,
            sanitize_katex_latex=sanitize,
            CURRICULUM_POLICY_REVISION=CURRICULUM_POLICY_REVISION,
            correct_khtn8_lime_soil_confusion=correct_khtn8_lime_soil_confusion)
        source = 'Mã minh họa: `<p>` và `<br>`.\n```html\n<p>Nội dung</p>\n```\n$x<2$'
        count = 0
        for grade in range(6, 13):
            for subject in subjects_for_grade(grade):
                with self.subTest(subject=subject, grade=grade):
                    self.assertEqual(gate(source, subject, grade), source)
                    count += 1
        self.assertEqual(count, 65)


if __name__ == '__main__':
    unittest.main()
