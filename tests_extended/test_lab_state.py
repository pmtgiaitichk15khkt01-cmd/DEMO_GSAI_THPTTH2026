import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from streamlit.testing.v1 import AppTest
from services.lab_state import lab_control_scope


class TestLabState(unittest.TestCase):
    def test_same_payload_order_does_not_reset_controls(self):
        self.assertEqual(lab_control_scope({'a': 1, 'b': 2}), lab_control_scope({'b': 2, 'a': 1}))

    def test_model_context_and_explicit_reselection_get_new_controls(self):
        old = lab_control_scope({'a': 1}, 'Toán học', 'Lớp 12', 0)
        for args in [({'a': 3}, 'Toán học', 'Lớp 12', 0),
                     ({'a': 1}, 'Vật lý', 'Lớp 12', 0),
                     ({'a': 1}, 'Toán học', 'Lớp 11', 0),
                     ({'a': 1}, 'Toán học', 'Lớp 12', 1)]:
            self.assertNotEqual(old, lab_control_scope(*args))

    def test_new_model_uses_its_coefficients_after_student_edits_old_model(self):
        import database
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as folder:
            with patch.object(database, 'db_manager', database.DatabaseManager(Path(folder) / 'lab.db')), \
                 patch('requests.sessions.Session.request', return_value=SimpleNamespace(status_code=200, content=b'', text='')):
                at = AppTest.from_file(str(root / 'app.py'), default_timeout=90).run()
                at.session_state['lab_data'] = {'type': 'func_3', 'a': 1, 'b': -3, 'c': 0, 'd': 2}
                at.run()
                key = next(s.key for s in at.slider if s.key.startswith('lab_f3_a__'))
                at.slider(key=key).set_value(2.0).run()
                self.assertEqual(at.slider(key=key).value, 2.0)
                at.session_state['lab_data'] = {'type': 'func_3', 'a': 3, 'b': 2, 'c': 1, 'd': 1}
                at.run()
                self.assertEqual([e.message for e in at.exception], [])
                current = next(s for s in at.slider if s.key.startswith('lab_f3_a__'))
                self.assertNotEqual(current.key, key)
                self.assertEqual(current.value, 3.0)
