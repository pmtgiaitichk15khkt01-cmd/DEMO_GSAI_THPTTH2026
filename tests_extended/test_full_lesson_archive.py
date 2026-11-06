import ast
import json
import unittest
from pathlib import Path
from types import SimpleNamespace
from services.lesson_archive import encode_full_lesson,decode_full_lesson,MAX_BUNDLE_BYTES
from services.academic_context import subjects_for_grade

TEXT='PHẦN 1: BÀI HỌC\nNội dung gốc\nPHẦN 2: CÂU HỎI\nCâu 1: A?\nA. yes\nB. no\nCORRECT: A\nEXPLAIN: Because\nPHẦN 3: TỰ LUẬN\nCâu 1: Explain\n'


class FullLessonArchiveTests(unittest.TestCase):
    def test_roundtrip_preserves_full_text_and_keys_across_contexts(self):
        for grade in range(6,13):
            for subject in subjects_for_grade(grade):
                data=encode_full_lesson(TEXT,subject,grade,'topic','policy')
                restored=decode_full_lesson(data,subject,grade)
                self.assertEqual(restored['text'],TEXT)
                self.assertIn('CORRECT: A',restored['text'])
                self.assertIn('PHẦN 3',restored['text'])
                self.assertNotIn('quiz_states',restored)
                self.assertNotIn('messages',restored)

    def test_context_integrity_format_size_and_state_injection_rejected(self):
        data=encode_full_lesson(TEXT,'Tiếng Anh',10,'topic','policy')
        for subject,grade in [('Toán học',10),('Tiếng Anh',11)]:
            with self.assertRaises(ValueError):decode_full_lesson(data,subject,grade)
        bundle=json.loads(data);bundle['content']='changed'
        with self.assertRaises(ValueError):decode_full_lesson(json.dumps(bundle).encode(),'Tiếng Anh',10)
        for bad in [b'{bad',b'[]',b'x'*(MAX_BUNDLE_BYTES+1)]:
            with self.assertRaises(ValueError):decode_full_lesson(bad,'Tiếng Anh',10)
        bundle=json.loads(data);bundle.update(quiz_states={'1':True},api_key='not restored',accepted=True)
        restored=decode_full_lesson(json.dumps(bundle).encode(),'Tiếng Anh',10)
        self.assertNotIn('api_key',restored);self.assertNotIn('accepted',restored)

    def test_actual_download_block_works_without_prior_conditional_hashlib_import(self):
        tree=ast.parse((Path(__file__).parents[1]/'app.py').read_text(encoding='utf-8-sig'))
        nodes=sorted([n for n in ast.walk(tree) if isinstance(n,(ast.ImportFrom,ast.Import,ast.Assign,ast.Expr))],key=lambda n:n.lineno)
        start=next(n.lineno for n in nodes if isinstance(n,ast.ImportFrom) and n.module=='services.lesson_archive' and any(a.name=='encode_full_lesson' for a in n.names))
        end=next(n.lineno for n in nodes if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call) and any(k.arg=='key' and isinstance(k.value,ast.BinOp) and isinstance(k.value.left,ast.Constant) and k.value.left.value=='t1_download_full_' for k in n.value.keywords))
        block=[n for n in nodes if start<=n.lineno<=end]
        class State(dict):
            __getattr__=dict.__getitem__
        calls=[]
        st=SimpleNamespace(session_state=State(current_lesson=TEXT,current_topic='topic'),download_button=lambda *a,**k:calls.append((a,k)))
        ns={'st':st,'subject':'Tiếng Anh','grade_num':10,'CURRICULUM_POLICY_REVISION':'test','current_context_key':'10_English'}
        exec(compile(ast.Module(body=block,type_ignores=[]),'<actual-full-download>','exec'),ns)
        self.assertEqual(len(calls),1)
        self.assertEqual(decode_full_lesson(calls[0][0][1],'Tiếng Anh',10)['text'],TEXT)
