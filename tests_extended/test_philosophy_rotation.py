import ast
from pathlib import Path
import random
from types import SimpleNamespace
import unittest


class PhilosophyRotationTests(unittest.TestCase):
    def test_closure_history_survives_lesson_change_without_student_content(self):
        tree = ast.parse(Path('app.py').read_text(encoding='utf-8'))
        fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                  and n.name == 'register_station_closure')
        class State(dict):
            __getattr__ = dict.__getitem__
            __setattr__ = dict.__setitem__
        state = State(current_topic='Bài Toán', subject='Toán học')
        env = {'st': SimpleNamespace(session_state=state)}
        exec(compile(ast.Module(body=[fn], type_ignores=[]), 'actual-register', 'exec'), env)
        quote = {'quote': 'Câu đã kiểm', 'author': 'Tác giả', 'lesson': 'Giữ lời hứa', 'student': 'PRIVATE'}
        env[fn.name](1, quote)
        state.update(current_topic='Bài Văn', subject='Ngữ văn')
        env[fn.name](1, quote)
        self.assertEqual(len(state['philosophical_teaching_history']), 1)
        self.assertNotIn('student', state['philosophical_teaching_history'][0])
        self.assertIn('Câu đã kiểm', state['used_philosophical_quotes'])

    def test_verified_quotes_do_not_repeat_after_authors_have_appeared(self):
        tree = ast.parse(Path('app.py').read_text(encoding='utf-8'))
        bank = next(n for n in tree.body if isinstance(n, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == 'CROSS_STATION_PHILOSOPHY_BANK' for t in n.targets))
        fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                  and n.name == 'get_unique_philosophical_lesson')
        used = []
        env = {'st': SimpleNamespace(session_state={'used_philosophical_quotes': used}), 'random': random}
        exec(compile(ast.Module(body=[bank, fn], type_ignores=[]), 'actual-controller', 'exec'), env)
        expected = [q for q in env['CROSS_STATION_PHILOSOPHY_BANK'][1] if q.get('source_verified')]
        seen = set()
        for i in range(len(expected)):
            result = env[fn.name](1, 'Ngữ văn' if i % 2 else 'Toán học', 'kiểm tra và luyện tập')
            self.assertTrue(result.get('source_verified'))
            self.assertNotIn(result['quote'], seen)
            seen.add(result['quote'])
            used.extend([result['quote'], result['author']])
        exhausted = env[fn.name](1)
        self.assertEqual(exhausted['quote'], '')
        self.assertFalse(exhausted['source_verified'])
