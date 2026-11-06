import ast
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import Mock


class LabReviewedContextTests(unittest.TestCase):
    def test_lab_receives_same_repaired_lesson_as_screen_not_unreviewed_raw(self):
        class State(dict):
            __getattr__ = dict.__getitem__
        tree = ast.parse((Path(__file__).parents[1] / 'app.py').read_text(encoding='utf-8'))
        node = next(n for n in ast.walk(tree) if isinstance(n, ast.If)
                    and 'current_lesson' in ast.dump(n.test)
                    and any(isinstance(x, ast.Name) and x.id == 'reviewed_lesson_text' for x in ast.walk(n)))
        gate = Mock(return_value='Reviewed lesson with corrected attribution')
        ns = dict(st=SimpleNamespace(session_state=State(current_lesson='Unreviewed raw attribution', current_topic='Exact topic')),
                  subject='Ngữ văn', grade_num=10, CURRICULUM_POLICY_REVISION=123,
                  station1_master_sovereign_brain_gate=gate, full_context_blocks=[])
        exec(compile(ast.Module(body=[node], type_ignores=[]), 'actual-lab-context', 'exec'), ns)
        self.assertIn('Reviewed lesson with corrected attribution', ns['full_context_blocks'][0])
        self.assertNotIn('Unreviewed raw attribution', ns['full_context_blocks'][0])
        gate.assert_called_once_with('Unreviewed raw attribution', subject='Ngữ văn', grade=10,
                                     topic='Exact topic', policy_revision=123)
