import ast
import logging
import unittest
from pathlib import Path
from unittest.mock import Mock, patch
from types import SimpleNamespace


class TextFirstImportTests(unittest.TestCase):
    def load(self, extract, parse):
        path = Path(__file__).resolve().parents[1] / 'real_exam_engine.py'
        tree = ast.parse(path.read_text(encoding='utf-8'))
        node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'parse_file_direct_with_ai')
        ns = {'extract_text_from_file_upload': extract, 'parse_raw_exam_text': parse, 'logging': logging}
        exec(compile(ast.Module(body=[node], type_ignores=[]), str(path), 'exec'), ns)
        return ns[node.name]

    def test_text_files_never_send_binary_and_preserve_teacher_context(self):
        for name in ('exam.txt', 'exam.TEX', 'exam.md'):
            with self.subTest(name=name):
                text = r'PHẦN I. Câu 1: $x^2$ A. 1 B. 2 C. 3 D. 4'
                extract = Mock(return_value=text)
                result = {'p1': [{'q': text}], 'p2': [], 'p3': []}
                parse = Mock(return_value=result)
                caller = Mock(side_effect=AssertionError('unexpected binary/provider call'))
                run = self.load(extract, parse)
                self.assertIs(run(b'raw', name, 'Tiếng Anh', 6, 'source', 'title', caller, 'keep original'), result)
                extract.assert_called_once_with(b'raw', name)
                parse.assert_called_once_with(text, 'Tiếng Anh', 6, 'source', 'title', ai_caller=caller, user_prompt='keep original')
                caller.assert_not_called()

    def test_visual_files_still_attempt_existing_binary_path(self):
        for name, mime in [('exam.pdf', 'application/pdf'), ('exam.docx', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')]:
            with self.subTest(name=name):
                part = Mock(side_effect=RuntimeError('offline binary probe'))
                modules = {'google.genai': SimpleNamespace(types=SimpleNamespace(Part=SimpleNamespace(from_bytes=part)))}
                extract, parse = Mock(return_value='fallback text'), Mock(return_value={})
                with patch.dict('sys.modules', modules):
                    self.load(extract, parse)(b'visual', name, 'Toán', 12, 's', 't', Mock())
                part.assert_called_once_with(data=b'visual', mime_type=mime)
                parse.assert_called_once()


if __name__ == '__main__':
    unittest.main()
