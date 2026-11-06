from copy import deepcopy
import ast
import hashlib
import json
from pathlib import Path
import unittest

from services.academic_context import subjects_for_grade
from services.lab_scope import preset_lab_label, preset_lab_note


class TestLabScope(unittest.TestCase):
    def test_existing_library_labels_and_payloads_remain_intact(self):
        root = Path(__file__).resolve().parents[1]
        manifest = json.loads((root / 'tests/fixtures/pr6_lab_presets_payload_sha256.json').read_text(encoding='utf-8'))
        nodes = [n.value for n in ast.walk(ast.parse((root / 'app.py').read_text(encoding='utf-8')))
                 if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'available_labs' for t in n.targets)]
        digest = hashlib.sha256('\n'.join(ast.dump(n, include_attributes=False) for n in nodes).encode()).hexdigest()
        self.assertEqual(len(nodes), manifest['count'])
        self.assertEqual(digest, manifest['sha256'])

    def test_computing_algorithm_preset_dispatches_diagram(self):
        from types import SimpleNamespace
        from services import lab_scope
        class State(dict):
            __getattr__ = dict.__getitem__
            __setattr__ = dict.__setitem__
        tree=ast.parse(Path('app.py').read_text(encoding='utf-8'))
        node=next(n for n in ast.walk(tree) if isinstance(n,ast.If) and 'Mở mô phỏng có sẵn' in ast.dump(n.test))
        label='Sơ đồ thuật toán & Cây nhị phân'
        original={label:{'type':'oxyz','x':2,'y':2,'z':2}}
        state=State(lab_intent_command_Tin10='Lệnh mô phỏng của yêu cầu trước')
        ns=dict(st=SimpleNamespace(button=lambda *a,**kw:True,session_state=state),available_labs=original,
            manual_lab=label,subject='Tin học',current_context_key='Tin10',
            resolve_preset_lab=getattr(lab_scope,'resolve_preset_lab',lambda *a:dict(a[-1])))
        exec(compile(ast.Module(body=[node],type_ignores=[]),'actual-lab-button','exec'),ns)
        self.assertEqual(state.lab_data['type'],'mermaid')
        self.assertIn('nhị phân',state.lab_data['code'])
        self.assertEqual(original[label]['type'],'oxyz')
        self.assertEqual(state.lab_request_revision,1)
        self.assertEqual(state['lab_intent_command_Tin10'], '')

    def test_higher_grade_preset_is_explicitly_an_extension(self):
        for grade in range(6, 12):
            value = preset_lab_label('Hàm bậc ba (KNTT 12)', 'Toán', grade)
            self.assertIn('Mở rộng, nhãn lớp 12', value)
            self.assertNotIn('KNTT', value)

    def test_same_grade_is_reference_not_textbook_certification(self):
        value = preset_lab_label('Hàm bậc ba (KNTT 12)', 'Toán', 12)
        self.assertIn('Mẫu tham khảo, nhãn lớp 12', value)
        self.assertNotIn('KNTT', value)

    def test_untagged_tools_do_not_get_an_invented_curriculum_grade(self):
        value = preset_lab_label('Hình hộp chữ nhật (3D)', 'Toán', 6)
        self.assertTrue(value.startswith('[Công cụ minh họa]'))

    def test_all_context_notes_do_not_claim_to_reconstruct_the_current_lesson(self):
        presets = {'Hàm bậc ba (KNTT 12)': {'type': 'func_3', 'a': 1, 'b': -3, 'c': 0, 'd': 2}}
        original = deepcopy(presets)
        for grade in range(6, 13):
            for subject in subjects_for_grade(grade):
                with self.subTest(subject=subject, grade=grade):
                    note = preset_lab_note(subject, grade)
                    self.assertIn(f'lớp {grade}', note)
                    self.assertIn('không tự lấy', note)
                    self.assertIn('chưa phải đối chiếu SGK', note)
                    for label in presets:
                        self.assertTrue(preset_lab_label(label, subject, grade))
        self.assertEqual(presets, original)
