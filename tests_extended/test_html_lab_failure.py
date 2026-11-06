import ast
import json
from pathlib import Path
import re
from types import SimpleNamespace
import unittest


class HTMLLabFailureTests(unittest.TestCase):
    def test_failed_html_request_does_not_invent_or_reuse_a_different_model(self):
        tree = ast.parse(Path('app.py').read_text(encoding='utf-8'))
        node = next(n for n in ast.walk(tree) if isinstance(n, ast.Try)
                    and any(isinstance(s, ast.Assign) and any(
                        isinstance(t, ast.Name) and t.id == 'raw_json' for t in s.targets)
                        and 'call_gemini_with_fallback' in ast.dump(s) for s in n.body))
        class State(dict):
            __getattr__ = dict.__getitem__
            __setattr__ = dict.__setitem__
        def offline(*args, **kwargs):
            raise RuntimeError('offline provider failure')
        for command, topic in [('Vẽ cấu trúc HTML', ''),
                               ('Lập sơ đồ tư duy', 'HTML và cấu trúc trang web')]:
            with self.subTest(command=command):
                state = State(current_topic=topic, lab_data={'type': 'oxyz'})
                warnings = []
                ns = dict(st=SimpleNamespace(session_state=state, warning=warnings.append),
                          subject='Tin học', grade_num=12, is_social_subject=False,
                          lab_command=command, lab_prompt='QA', re=re,
                          call_gemini_with_fallback=offline,
                          available_labs={'default': {'type': 'func_3'}})
                exec(compile(ast.Module(body=[node], type_ignores=[]), 'actual-lab-request', 'exec'), ns)
                self.assertIsNone(state.lab_data)
                self.assertEqual(len(warnings), 1)
                self.assertIn('Chưa dựng được Lab HTML', warnings[0])

    def test_wrong_model_is_rejected_but_valid_html_diagram_is_preserved(self):
        tree = ast.parse(Path('app.py').read_text(encoding='utf-8'))
        node = next(n for n in ast.walk(tree) if isinstance(n, ast.Try)
                    and any(isinstance(s, ast.Assign) and any(
                        isinstance(t, ast.Name) and t.id == 'raw_json' for t in s.targets)
                        and 'call_gemini_with_fallback' in ast.dump(s) for s in n.body))
        class State(dict):
            __getattr__ = dict.__getitem__
            __setattr__ = dict.__setitem__
        for payload in [{'type': 'func_3', 'a': 1},
                        {'type': 'mermaid'},
                        {'type': 'mermaid', 'code': None},
                        {'type': 'mermaid', 'code': '   '},
                        {'type': 'mermaid', 'code': 'graph TD\nH[html] --> B[body]'}]:
            state = State(current_topic='HTML', lab_data=None)
            warnings = []
            ns = dict(st=SimpleNamespace(session_state=state, warning=warnings.append),
                      subject='Tin học', grade_num=12, is_social_subject=False,
                      lab_command='Vẽ sơ đồ cấu trúc HTML', lab_prompt='QA', re=re, json=json,
                      call_gemini_with_fallback=lambda *a, **kw: json.dumps(payload),
                      safe_json_loads=json.loads, available_labs={})
            exec(compile(ast.Module(body=[node], type_ignores=[]), 'actual-lab-request', 'exec'), ns)
            if payload['type'] == 'mermaid' and isinstance(payload.get('code'), str) and payload['code'].strip():
                self.assertEqual(state.lab_data, payload)
                self.assertEqual(warnings, [])
            else:
                self.assertIsNone(state.lab_data)
                self.assertEqual(len(warnings), 1)
