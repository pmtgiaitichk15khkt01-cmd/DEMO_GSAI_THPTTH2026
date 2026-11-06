import ast
import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch

import real_exam_engine as engine
from services.bank_storage import (BoundedCache, exam_storage_identity,
    read_exam_cache_records, save_exam_cache_snapshot)
from services.cache_metadata import cached_exam_label, distinct_exam_labels


def paper(text='first', subject='Tin học', grade=12):
    return {'subject':subject,'grade':grade,'year':2025,'code':'0530',
            'title':'same title','p1':[{'q':text,'opt':['1','2','3','4'],'ans':'B'}],
            'p2':[],'p3':[]}


class TeacherArchivePreservationTests(unittest.TestCase):
    def test_legacy_is_unchanged_and_same_code_revisions_remain_selectable(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'teacher.json'
            original={'exams':[paper('legacy')]}
            path.write_text(json.dumps(original),encoding='utf-8')
            before=path.read_bytes();incoming=paper('new');untouched=deepcopy(incoming)
            with patch.object(engine,'TEACHER_EXAMS_FILE',str(path)):
                for exam in [incoming, incoming, paper('other'),paper('math','Toán học'),paper('grade11',grade=11)]:
                    self.assertTrue(engine.save_teacher_uploaded_exam(exam))
                tin=engine.load_teacher_uploaded_exams('Tin học',12)
                self.assertEqual({q['p1'][0]['q'] for q in tin},{'legacy','new','other'})
                self.assertEqual(len(engine.load_teacher_uploaded_exams('Toán học',12)),1)
                self.assertEqual(len(engine.load_teacher_uploaded_exams('Tin học',11)),1)
            self.assertEqual(path.read_bytes(),before)
            self.assertEqual(incoming,untouched)
            self.assertEqual(len(list(Path(str(path)+'.versions').glob('*.json'))),4)
            labels=distinct_exam_labels(['Mã0530']*len(tin),tin)
            self.assertEqual(len(set(labels)),3)

    def test_broken_legacy_archive_is_never_replaced_or_silently_emptied(self):
        for raw in [b'{broken',b'{"exams": {}}',b'[]',b'{"exams":[42]}']:
            with tempfile.TemporaryDirectory() as tmp:
                path=Path(tmp)/'teacher.json';path.write_bytes(raw)
                with patch.object(engine,'TEACHER_EXAMS_FILE',str(path)):
                    self.assertFalse(engine.save_teacher_uploaded_exam(paper()))
                self.assertEqual(path.read_bytes(),raw)
                self.assertFalse(Path(str(path)+'.versions').exists())

    def test_parallel_saves_keep_all_revisions_and_idempotent_repeats(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'teacher.json'
            with patch.object(engine,'TEACHER_EXAMS_FILE',str(path)):
                inputs=[paper(str(i%8)) for i in range(24)]
                with ThreadPoolExecutor(max_workers=8) as executor:
                    self.assertTrue(all(executor.map(engine.save_teacher_uploaded_exam,inputs)))
                self.assertEqual(len(engine.load_teacher_uploaded_exams('Tin học',12)),8)
                self.assertFalse(path.exists())

    def test_full_catalogue_keeps_teacher_and_ai_with_same_printed_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'teacher.json';cache=Path(tmp)/'data'/'exam_cache'
            with patch.object(engine,'TEACHER_EXAMS_FILE',str(path)), \
                 patch.object(engine,'BASE_DIR',tmp), \
                 patch.object(engine,'_FAST_EXAM_LIST_CACHE',BoundedCache(8),create=True), \
                 patch.object(engine,'get_shard_exams',return_value=[paper('source')]):
                self.assertTrue(engine.save_teacher_uploaded_exam(paper('teacher A')))
                self.assertTrue(engine.save_teacher_uploaded_exam(paper('teacher B')))
                save_exam_cache_snapshot(cache,{'subject':'Tin học','grade':12,'code':'0530','data':paper('AI A')})
                (cache/'broken.json').write_text('{bad',encoding='utf-8')
                save_exam_cache_snapshot(cache,{'subject':'Tin học','grade':12,'code':'0530','data':paper('AI B')})
                rows=engine.get_baseline_full_exams('Tin học',12)
                self.assertEqual({q['p1'][0]['q'] for q in rows},{'source','teacher A','teacher B','AI A','AI B'})
                self.assertEqual(len({exam_storage_identity(q) for q in rows}),5)
                self.assertTrue(engine.save_teacher_uploaded_exam(paper('teacher C')))
                self.assertEqual(len(engine.get_baseline_full_exams('Tin học',12)),6)

    def test_identity_preserves_unfamiliar_scientific_and_source_context(self):
        original=paper()
        first=exam_storage_identity(original)
        for key in ('shared_context','exam_session','visuals','custom_scientific_context'):
            self.assertNotEqual(first,exam_storage_identity(dict(original,**{key:'different'})))
        self.assertEqual(first,exam_storage_identity(dict(original,uploaded_at='later')))

    def test_cache_reader_accepts_legacy_and_snapshots_by_context_not_filename(self):
        with tempfile.TemporaryDirectory() as tmp:
            for subject,grade,text in [('Tin học',12,'new'),('Tin học',11,'grade11'),('Toán học',12,'math')]:
                save_exam_cache_snapshot(tmp,{'subject':subject,'grade':grade,'code':'0530','data':paper(text,subject,grade)})
            legacy={'subject':'Tin học','grade':12,'code':'0530','data':paper('old')}
            (Path(tmp)/'legacy_lop12_0530.json').write_text(json.dumps(legacy),encoding='utf-8')
            rows=read_exam_cache_records(tmp,'Tin học',12)
            self.assertEqual({r['data']['p1'][0]['q'] for r in rows},{'new','old'})

    def test_actual_app_cache_picker_reads_both_filename_formats(self):
        root=Path(__file__).parents[1]
        tree=ast.parse((root/'app.py').read_text(encoding='utf-8-sig'))
        node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='get_cached_exams')
        node.decorator_list=[];ns={'__file__':str(root/'app.py')}
        import os,logging
        class Ree:
            def get_baseline_full_exams(self,*args):return []
        with tempfile.TemporaryDirectory() as tmp:
            save_exam_cache_snapshot(tmp,{'subject':'Tin học','grade':12,'code':'0530','data':paper()})
            ns.update(os=os,json=json,logging=logging,ree=Ree(),EXAM_CACHE_DIR=tmp)
            exec(compile(ast.Module(body=[node],type_ignores=[]),'<actual-app-cache>','exec'),ns)
            self.assertEqual(len(ns['get_cached_exams']('Tin học',12)),1)
