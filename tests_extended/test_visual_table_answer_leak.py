import ast
import html
from pathlib import Path
import unittest
from copy import deepcopy
from unittest.mock import Mock

from services.bbt_display_contract import aligned_bbt_rows
from services.web_question_contract import graph_identification_answer_leak, WEB_QUESTION_INSTRUCTION
from services.context_recovery import repair_exam_context


class TestVisualTableAnswerLeak(unittest.TestCase):
    def test_double_bar_and_limits_preserved_and_aligned(self):
        raw = "x | -inf | -2 | -1 | 0 | +inf\ny' | + | 0 | - | || | - | 0 | +\ny | 2 | 4 | -inf || +inf | 0 | 2"
        rows = aligned_bbt_rows(raw)
        self.assertEqual(len(rows[1]), 10)
        self.assertEqual(rows[1][5], '||')
        self.assertEqual(rows[2][5], r'-\infty || +\infty')
        namespace = {'html': html}
        tree = ast.parse(Path('app.py').read_text(encoding='utf-8'))
        for name in ('_render_math_html_token', '_normalize_moet_bbt_grid', '_build_svg_bbt_from_rows', 'question_visual_html'):
            node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
            namespace['re'] = __import__('re')
            exec(compile(ast.Module(body=[node], type_ignores=[]), 'renderer-test', 'exec'), namespace)
        output = namespace['question_visual_html']({'bbt': raw})
        self.assertIn('<table', output)
        self.assertIn('∞', output)
        self.assertNotIn('-inf<', output)

    def test_bbt_text_cells_have_explicit_dark_foreground(self):
        import re
        from html.parser import HTMLParser
        namespace = {'html': html, 're': re}
        tree = ast.parse(Path('app.py').read_text(encoding='utf-8'))
        for name in ('_render_math_html_token', '_normalize_moet_bbt_grid', '_build_svg_bbt_from_rows'):
            node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
            exec(compile(ast.Module(body=[node], type_ignores=[]), 'bbt-contrast-test', 'exec'), namespace)
        class Cells(HTMLParser):
            def handle_starttag(self, tag, attrs):
                if tag == 'td':
                    style=dict(attrs).get('style','')
                    self.styles.append(style)
        for sign in (False, True):
            out=namespace['_build_svg_bbt_from_rows'](['x','-inf','0','2','+inf'],
                ["y'",'+','0','-','0','+'],['y','-inf','2','-2','+inf'],is_sign_table=sign)
            parser=Cells();parser.styles=[];parser.feed(out)
            self.assertTrue(parser.styles)
            for style in parser.styles:
                self.assertRegex(style, r'(?:^|;)color:')
            self.assertIn('#16a34a',out)
            self.assertIn('#dc2626',out)

    def test_missing_variation_direction_does_not_invent_alternating_arrows(self):
        namespace={'html':html, 're':__import__('re')}
        tree=ast.parse(Path('app.py').read_text(encoding='utf-8'))
        for name in ('_render_math_html_token','_normalize_moet_bbt_grid','_build_svg_bbt_from_rows'):
            node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
            exec(compile(ast.Module(body=[node],type_ignores=[]),'bbt-direction-test','exec'),namespace)
        x=['x',r'-\infty','1',r'+\infty']
        missing=['y',r'+\infty','0',r'+\infty']
        grid=namespace['_normalize_moet_bbt_grid'](x,[],missing)
        self.assertEqual(grid['y_arrows'],['',''])
        output=namespace['_build_svg_bbt_from_rows'](x,[],missing)
        self.assertNotIn('<svg',output)
        self.assertIn('∞',output)
        supplied=['y',r'+\infty',r'\searrow','0',r'\nearrow',r'+\infty']
        self.assertEqual(namespace['_normalize_moet_bbt_grid'](x,[],supplied)['y_arrows'],['down','up'])

    def test_missing_limits_not_invented(self):
        raw = "x | -inf | -2 | -1 | 0 | +inf\ny' | + | 0 | - | || | - | 0 | +\ny | 2 | 4 | || | 0 | 2"
        self.assertIsNone(aligned_bbt_rows(raw))

    def test_cubic_existing_contract_is_supported(self):
        rows = aligned_bbt_rows("x | -inf | -1 | 1 | +inf\ny' | + | 0 | - | 0 | +\ny | -inf | 2 | -2 | +inf")
        self.assertIsNotNone(rows)

    def test_leak_detection_does_not_remove_given_formula_tasks(self):
        q = {'q': r'Đường cong trong hình bên là đồ thị của hàm số nào? (Giả định đồ thị hàm bậc ba $y=x^3-3x$)'}
        self.assertTrue(graph_identification_answer_leak(q))
        self.assertFalse(graph_identification_answer_leak({'q': r'Cho hàm số $y=x^3-3x$. Tìm cực trị.'}))
        self.assertFalse(graph_identification_answer_leak({'q': 'Đường cong trong hình bên là đồ thị của hàm số nào?'}))
        self.assertNotIn('đồng thời nêu rõ hàm số số học tương ứng', WEB_QUESTION_INSTRUCTION)

    def test_existing_recovery_replaces_leak_without_mutating_source(self):
        q = dict(subject='Toán học', grade=12, topic='Khảo sát hàm số', level='TH',
                 q=r'Đường cong trong hình bên là đồ thị của hàm số nào? (Giả định $y=x^3-3x$)',
                 f=dict(type='func_3', a=1,b=0,c=-3,d=0),
                 opt=['A. y=x^3-3x','B. y=-x^3+3x','C. y=x^2','D. y=-x^2'], ans='A')
        before = deepcopy(q)
        valid = dict(q,q='Đường cong trong hình bên là đồ thị của hàm số nào?')
        ai=Mock()
        result=repair_exam_context({'p1':[q]},'Toán học',12,topics=['Khảo sát hàm số'],
                                  bank_provider=lambda *_:{'p1':[valid]},ai_generator=ai)
        self.assertEqual(result['context_recovery']['unresolved'],0)
        self.assertEqual(result['p1'][0]['q'],valid['q'])
        self.assertEqual(q,before)
        ai.assert_not_called()

    def test_two_row_table_data_is_not_lost(self):
        from services.bbt_display_contract import supplied_bbt_rows, missing_asymptote_limits
        raw="x | -inf | 1 | +inf\ny | +inf | 0 | +inf"
        self.assertEqual(len(supplied_bbt_rows(raw)),2)
        self.assertFalse(missing_asymptote_limits(raw))
        self.assertTrue(missing_asymptote_limits("x | -inf | -1 | +inf\ny' | - | || | -\ny | 2 | || | 2"))
