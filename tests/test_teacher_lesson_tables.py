"""Exercise the actual Station 1 renderer against lost-row regressions."""
import html
import unittest
from unittest.mock import patch
from services.curriculum_policy import correct_khtn8_lime_soil_confusion

from tests.test_expert_patch_regressions import load_function


class TeacherLessonTableTests(unittest.TestCase):
    def test_observed_polya_plan_does_not_reintroduce_touch_or_taste(self):
        source = ('Nước xà phòng, nước vắt từ quả cam, nước tinh khiết.\n'
                  'Xác định môi trường của từng mẫu dựa trên kiến thức thực tế '
                  '(Ví dụ: Cam có vị chua thì chứa chất gì? Xà phòng có cảm giác nhờn thì thuộc loại nào?).')
        fixed = correct_khtn8_lime_soil_confusion(source, 'Khoa học tự nhiên', 8)
        self.assertNotIn('cảm giác nhờn', fixed)
        self.assertIn('không nếm hoặc chạm mẫu', fixed)
        self.assertEqual(correct_khtn8_lime_soil_confusion(fixed, 'Khoa học tự nhiên', 8), fixed)
        self.assertEqual(correct_khtn8_lime_soil_confusion(source, 'Ngữ văn', 8), source)

    @classmethod
    def setUpClass(cls):
        cls.render = staticmethod(load_function('render_pedagogical_lesson_visuals', html=html,
            sanitize_svg_for_markdown=lambda svg: svg,
            _parse_bbt_cells_safe=load_function('_parse_bbt_cells_safe')))

    def test_chemistry_does_not_substitute_fixed_gas_or_cell_for_other_lessons(self):
        for grade in range(6, 13):
            with self.subTest(grade=grade), patch('precision_visual_engine.build_gas_preparation_model') as gas, \
                    patch('precision_visual_engine.build_daniell_cell_model') as cell:
                for source in ('Thu khí H2 bằng đẩy nước trong ống nghiệm.',
                               'Điều chế O2 bằng đun nóng rồi thu khí bằng đẩy nước.',
                               'Pin điện hóa bạc: xác định anode, cathode và cầu muối.',
                               'C2H4 là chất khí. Nêu tính chất của chất này.'):
                    self.assertEqual(self.render(source, 'Hóa học', grade), source)
                gas.assert_not_called()
                cell.assert_not_called()

    def test_matching_explicit_chemistry_diagrams_are_kept(self):
        with patch('precision_visual_engine.build_gas_preparation_model', return_value={'svg': '<svg>gas</svg>'}) as gas:
            rendered = self.render('Điều chế C2H4 bằng đun nóng, thu bằng đẩy nước.', 'Hóa học', 11)
            gas.assert_called_once_with('C2H4')
            self.assertIn('<svg>gas</svg>', rendered)
        with patch('precision_visual_engine.build_daniell_cell_model', return_value={'svg': '<svg>cell</svg>'}) as cell:
            self.assertIn('<svg>cell</svg>', self.render('Sơ đồ pin Daniell.', 'Hóa học', 12))
            cell.assert_called_once()

    def test_live_ph_table_keeps_all_three_samples(self):
        source = ('| Dung dịch | Giá trị pH |\n|---|---|\n'
                  '| Nước chanh | 3 |\n| Nước tinh khiết | 7 |\n| Nước xà phòng | 10 |\n')
        self.assertEqual(self.render(source, 'Khoa học tự nhiên', 8), source)

    def test_multirow_table_is_not_partially_converted_as_frequency_table(self):
        source = ('| Giá trị | 1 | 2 |\n|---|---|---|\n'
                  '| n | 3 | 4 |\n| Ghi chú | thấp | cao |\n')
        self.assertEqual(self.render(source, 'Tin học', 8), source)

    def test_two_row_frequency_table_still_renders_without_losing_values(self):
        source = '| Nhóm | [0; 5) | [5; 10) |\n|---|---|---|\n| Tần số | 3 | 7 |\n'
        for newline in ('\n', '\r\n'):
            with self.subTest(newline=repr(newline)):
                result = self.render(source.replace('\n', newline), 'Toán học', 11)
                self.assertIn('<table', result)
                for value in ('[0; 5)', '[5; 10)', '>3</td>', '>7</td>'):
                    self.assertIn(value, result)


if __name__ == '__main__':
    unittest.main()
