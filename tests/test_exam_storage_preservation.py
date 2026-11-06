import ast
import hashlib
import json
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from services.bank_storage import save_exam_cache_snapshot
from services.official_paper import PACKS, original_tin0530


class ExamStoragePreservationTests(unittest.TestCase):
    def test_same_code_different_payload_never_overwrites_legacy_or_new_cache(self):
        with tempfile.TemporaryDirectory() as directory:
            legacy = Path(directory) / 'Tin_hoc_lop12_0530.json'
            legacy.write_bytes(b'legacy-source')
            base = {'subject':'Tin học','grade':12,'code':'0530',
                    'saved_at':'first','data':{'p1':[{'q':'A','ans':'B'}]}}
            first = Path(save_exam_cache_snapshot(directory, base))
            first_bytes = first.read_bytes()
            same = dict(base, saved_at='later')
            self.assertEqual(save_exam_cache_snapshot(directory, same), str(first))
            other = dict(base, data={'p1':[{'q':'different','ans':'C'}]})
            second = Path(save_exam_cache_snapshot(directory, other))
            self.assertNotEqual(first, second)
            self.assertEqual(first.read_bytes(), first_bytes)
            self.assertEqual(legacy.read_bytes(), b'legacy-source')
            self.assertEqual(json.loads(second.read_text(encoding='utf-8')), other)

    def test_concurrent_identical_saves_publish_one_complete_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            record = {'subject':'Tin học','grade':12,'code':'0530','data':{'p1':[]}}
            with ThreadPoolExecutor(max_workers=8) as executor:
                paths = list(executor.map(lambda _:save_exam_cache_snapshot(directory,record),range(24)))
            self.assertEqual(len(set(paths)), 1)
            self.assertEqual(json.loads(Path(paths[0]).read_text(encoding='utf-8')), record)
            self.assertFalse(list(Path(directory).glob('*.tmp')))

    def test_repeated_actual_original_open_and_caller_mutation_do_not_change_sources(self):
        sources = list(PACKS.glob('tin_2025_0530.*'))
        before = {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
        for _ in range(8):
            for track in ('CS','ICT'):
                exam = original_tin0530(track)
                self.assertEqual(len(exam['p1']),24)
                self.assertEqual(exam['p1'][0]['ans'],'B')
                exam['p1'][0]['ans']='D'
                exam['p1'][0]['explain']='caller changed'
                exam['p2'].clear()
        after = {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
        self.assertEqual(before, after)
        self.assertEqual(original_tin0530('CS')['p1'][0]['ans'],'B')

    def test_both_generated_cache_writers_delegate_to_no_clobber_storage(self):
        root = Path(__file__).parents[1]
        for file, function in [('app.py','save_exam_to_cache'),
                               ('real_exam_engine.py','ingest_ai_generated_exam_to_bank')]:
            tree=ast.parse((root/file).read_text(encoding='utf-8-sig'))
            node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==function)
            calls=[n for n in ast.walk(node) if isinstance(n,ast.Call)]
            self.assertTrue(any(isinstance(n.func,ast.Name) and n.func.id=='save_exam_cache_snapshot'
                                for n in calls))
            self.assertFalse(any(isinstance(n.func,ast.Name) and n.func.id=='open'
                                 and len(n.args)>1 and isinstance(n.args[1],ast.Constant)
                                 and n.args[1].value=='w' for n in calls))
