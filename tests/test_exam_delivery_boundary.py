import ast
import copy
import json
import logging
import os
from pathlib import Path
import re
import tempfile
import types
import unittest
from services.exam_delivery import exam_delivery_held

class DeliveryBoundaryTests(unittest.TestCase):
    def test_holds_cover_wrapper_reading_and_statement_without_mutation(self):
        for exam in ({'source_review_issues':['hold']},
                     {'p2':[{'stmts':[{'source_review_issues':['hold']}]}]},
                     {'part_doc_hieu':{'questions':[{'source_review_issues':['hold']}]}}):
            original=copy.deepcopy(exam)
            self.assertTrue(exam_delivery_held({'data':exam}))
            self.assertEqual(exam,original)
        self.assertFalse(exam_delivery_held({'p1':[{'q':'valid'}]}))

    def test_actual_cache_adapter_rejects_held_baseline_and_disk_cache(self):
        tree=ast.parse((Path(__file__).parents[1]/'app.py').read_text(encoding='utf-8-sig'))
        fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='get_cached_exams')
        fn.decorator_list=[]
        held={'code':'held','p1':[{'q':'original','source_review_issues':['premise']} ]}
        good={'code':'good','p1':[{'q':'valid'}]}
        with tempfile.TemporaryDirectory() as folder:
            Path(folder,'Tin_học_lop12_held.json').write_text(json.dumps({'data':held}),encoding='utf-8')
            namespace=dict(ree=types.SimpleNamespace(get_baseline_full_exams=lambda *a:[held,good]),
                           EXAM_CACHE_DIR=folder,os=os,re=re,json=json,logging=logging)
            exec(compile(ast.Module(body=[fn],type_ignores=[]),'<actual-cache-adapter>','exec'),namespace)
            rows=namespace['get_cached_exams']('Tin học',12)
            self.assertEqual([r['code'] for r in rows],['good'])
            self.assertIn('source_review_issues',held['p1'][0])

    def test_actual_reviewed_0525_is_held_and_valid_question_not_erased(self):
        import lzma
        path=Path(__file__).parents[1]/'data/real_exam_bank/exams_Tin_h_c.json.xz'
        from services.bank_storage import iter_exam_shard
        matches=[e for e in iter_exam_shard(path) if str(e.get('code'))=='0525'
                 and e.get('year')==2026]
        self.assertEqual(len(matches),1)
        exam=matches[0]
        self.assertTrue(exam_delivery_held(exam))
        self.assertEqual(len(exam['p1']),24)
        self.assertTrue(exam['p1'][13]['source_review_issues'])
        self.assertFalse(exam_delivery_held({'p1':[exam['p1'][0]]}))
