import unittest
from html import unescape
from services.exam_code_text import source_text_html, code_text_latex
from tests.test_expert_patch_regressions import load_function


class PrintCodeTests(unittest.TestCase):
    def test_print_code_preserves_indentation_and_escapes_html(self):
        code = 'if a < 2:\n    print("<script>")\n    a += 1'
        result = source_text_html('Đoạn mã:\n```python\n'+code+'\n```')
        self.assertIn('class="exam-source-code"',result)
        self.assertNotIn('```',result)
        self.assertNotIn('<script>',result)
        self.assertIn(code,unescape(result))

    def test_math_sanitizer_never_changes_code_dollars_or_backslashes(self):
        render = load_function('sanitize_print_math_text',sanitize_katex_latex=lambda x:x)
        render.__globals__['sanitize_print_math_text'] = render
        code = '```python\n    x = "$"; path = r"\\left"\n```'
        self.assertIn(code,render('Đoạn mã '+code))

    def test_latex_code_escapes_commands_and_preserves_indentation(self):
        code = '```sql\n    SELECT a_b, "$" FROM T;\n```'
        result = code_text_latex(code)
        self.assertIn(r'\ \ \ \ SELECT',result)
        self.assertIn(r'a\_b',result)
        self.assertIn(r'\$',result)
        self.assertNotIn('```',result)
        render = load_function('latex_text')
        render.__globals__['latex_text']=render
        self.assertEqual(render(code),result)
