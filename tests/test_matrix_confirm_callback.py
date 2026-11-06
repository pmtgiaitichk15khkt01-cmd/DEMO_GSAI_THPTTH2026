import ast
from pathlib import Path
import unittest


class MatrixConfirmCallback(unittest.TestCase):
    def test_confirmation_commits_in_callback_before_widgets(self):
        tree = ast.parse(Path('app.py').read_text(encoding='utf-8'))
        buttons = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
                   and isinstance(n.func, ast.Attribute) and n.func.attr == 'button'
                   and any(k.arg == 'key' and isinstance(k.value, ast.Constant)
                           and k.value.value == 'btn_confirm_cp_explicit' for k in n.keywords)]
        self.assertEqual(len(buttons), 1)
        callback = next(k.value for k in buttons[0].keywords if k.arg == 'on_click')
        self.assertEqual(callback.id, 'handle_custom_prompt_commit')
        self.assertFalse(any(isinstance(n, ast.If) and isinstance(n.test, ast.Name)
                             and n.test.id == 'btn_confirm_cp' for n in ast.walk(tree)))
