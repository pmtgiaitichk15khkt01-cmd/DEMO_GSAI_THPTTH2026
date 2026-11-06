import ast
import copy
import json
import re
import tempfile
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from services.context_recovery import model_from_explicit_formula
from services.neuro_symbolic_verifier import clean_latex_math_to_sympy_expr, verify_calculus_function
from services.recovery_diagnostics import recovery_failure_summary

ROOT = Path(__file__).resolve().parents[1]
TREE = ast.parse((ROOT / 'app.py').read_text(encoding='utf-8'))


def load_function(name, **env):
    node = copy.deepcopy(next(n for n in TREE.body if isinstance(n, ast.FunctionDef) and n.name == name))
    node.decorator_list = []
    ns = {'re': re, 'json': json, **env}
    exec(compile(ast.Module(body=[node], type_ignores=[]), 'app-expert-test', 'exec'), ns)
    return ns[name]


class ExpertRegressionTests(unittest.TestCase):
    def test_braced_exponent_inside_fraction(self):
        expression = clean_latex_math_to_sympy_expr(r'\frac{x^{2}+1}{x-1}')
        self.assertIsNotNone(expression)
        report = verify_calculus_function(r'\frac{x^{2}+1}{x-1}')
        self.assertTrue(report['verified'])
        self.assertEqual(report['asymptotes']['vertical'], [1.0])

    def test_fractional_cubic_recovery_from_actual_entry_point(self):
        model = model_from_explicit_formula(r'Cho đồ thị $y=\frac{1}{3}x^3-x^2+1$.')
        self.assertIsNotNone(model)
        self.assertAlmostEqual(model['a'], 1/3)
        self.assertEqual(model['b'], -1)
        self.assertIsNone(model_from_explicit_formula(r'$y=\frac{1}{0}x^3+1$'))

    def test_diagnostics_keep_known_reason_codes(self):
        for reason in ('chemical_identity_mismatch', 'missing_variation_table_limits', 'graph_identification_formula_revealed'):
            r = recovery_failure_summary('Toán học', 12, {'events': [{'part': 'p1', 'index': 0, 'action': 'needs_review', 'reason': reason}]})
            self.assertEqual(r['events'][0]['reason'], reason)

    def test_formatting_does_not_replace_second_derivative_with_cubic_formula(self):
        f = load_function('_legacy_format_pedagogical_math')
        result = f("Xét $y'' = 0$ cho hàm số đang học.")
        self.assertIn("y''", result)
        self.assertNotIn(r'\frac{b}{3a}', result)
        self.assertEqual(result.count('$') % 2, 0)

    def test_shuffle_keeps_correct_index_when_option_text_is_duplicated(self):
        f = load_function('parse_quiz_questions', sanitize_katex_latex=lambda s:s,
                          format_pedagogical_math=None, annotate_question=lambda q:q)
        text = 'Câu 1: Một câu hỏi\nA. cùng chữ\nB. cùng chữ\nC. khác\nD. nữa\nCORRECT: A\nDòng giải thích tiếp'
        with patch('random.shuffle', side_effect=lambda items: items.reverse()):
            q = f(text)[0]
        self.assertEqual(q['correct'], 'D')
        self.assertNotIn('Gợi ý tự suy luận!', q['explain'])

    def test_page_filter_handles_unknown_page_without_broadcasting(self):
        f = load_function('annotations_for_page')
        anns = [{'page':1,'label':'one'},{'page':'2','label':'two'},
                {'page':'bad','label':'bad'},{'label':'missing'},{'page':True,'label':'bool'}]
        self.assertEqual([a['label'] for a in f(anns, 2, 3)], ['two'])
        self.assertEqual([a['label'] for a in f(anns, 1, 3)], ['one'])
        self.assertEqual(f([{'label':'legacy'}], 1, 1), [{'label':'legacy'}])

    def test_timer_synchronizes_visible_answers_before_rerun(self):
        class State(dict):
            __getattr__ = dict.__getitem__
            __setattr__ = dict.__setitem__
        state = State(exam_state='testing', exam_deadline=time.time()-5,
                      exam_answers={'p1_0':'old'}, exam_data={'p1':[{}], 'p2':[{'stmts':[{}]}], 'p3':[{}]},
                      t3_p1_0='B. new', t3_p2_0_0='Sai', t3_p3_0='1,5', t3_p1_99='stale')
        st = SimpleNamespace(session_state=state, rerun=lambda **kwargs:None)
        load_function('render_exam_clock', st=st, time=time, get_vn_time=lambda:'now')()
        self.assertEqual(state['exam_answers'], {'p1_0':'B. new','p2_0_0':'Sai','p3_0':'1,5'})
        self.assertEqual(state['exam_state'], 'graded')

    def test_paired_aliases_do_not_lose_pre_post_pair(self):
        from database import DatabaseManager
        with tempfile.TemporaryDirectory() as tmp:
            db = DatabaseManager(Path(tmp)/'test.db')
            conn = db._get_connection()
            for idx, subj, phase, score in [('a','Vật lí','pre',4),('b','Vật lý','post',6)]:
                conn.execute('INSERT INTO exam_attempts (id,student_id,grade_level,subject,exam_code,score,phase) VALUES (?,?,?,?,?,?,?)',
                             (idx,'synthetic',12,subj,'QA',score,phase))
            conn.commit()
            rows = db.get_paired_exam_data('Vật lý',12)
            conn.close()
            self.assertEqual(len(rows), 1)
            self.assertEqual((rows[0]['pre'],rows[0]['post']), (4,6))

    def test_docx_budget_checked_before_decompression(self):
        import io, zipfile
        from exam_file_extractor import extract_docx
        payload = io.BytesIO()
        with zipfile.ZipFile(payload, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr('word/document.xml', b' '*(25*1024*1024+1))
        with self.assertRaisesRegex(ValueError, '25MB'):
            extract_docx(payload.getvalue())

    def test_url_guard_blocks_redirect_and_attachment_private_targets(self):
        import real_exam_engine as engine
        response = SimpleNamespace(status_code=302, headers={'Location':'http://127.0.0.1/secret'}, close=lambda:None)
        with patch('socket.getaddrinfo', return_value=[(2,1,6,'',('8.8.8.8',443))]), patch.object(engine.requests, 'get', return_value=response) as get:
            with self.assertRaises(ValueError):
                engine._public_get('https://example.org/start', timeout=2)
            get.assert_called_once()
        with patch.object(engine.requests, 'get') as get:
            with self.assertRaises(ValueError):
                engine._public_get('http://127.0.0.1/a.pdf', timeout=2)
            get.assert_not_called()

    def test_url_guard_keeps_public_redirects_supported(self):
        import real_exam_engine as engine
        first = SimpleNamespace(status_code=302, headers={'Location':'/download.pdf'}, close=lambda:None)
        final = SimpleNamespace(status_code=200, headers={})
        with patch('socket.getaddrinfo', return_value=[(2,1,6,'',('8.8.8.8',443))]), patch.object(engine.requests, 'get', side_effect=[first,final]) as get:
            self.assertIs(engine._public_get('https://example.org/start', timeout=2), final)
            self.assertEqual(get.call_count,2)
            self.assertFalse(get.call_args.kwargs['allow_redirects'])

    def test_export_and_review_boolean_expressions_match_scoring(self):
        from qa_runtime import normalize_bool, mcq_answer_matches
        function = next(n for n in TREE.body if isinstance(n, ast.FunctionDef) and n.name == 'build_exam_exports')
        join = next(n.value for n in ast.walk(function) if isinstance(n, ast.Assign)
                    and any(isinstance(t,ast.Name) and t.id == 'answer' for t in n.targets)
                    and isinstance(n.value,ast.Call) and isinstance(n.value.func,ast.Attribute) and n.value.func.attr == 'join')
        value = eval(compile(ast.Expression(body=join), 'export-answer-test','eval'),
                     {'normalize_bool':normalize_bool,'q':{'stmts':[{'a':'false'},{'a':'true'},{}]}})
        self.assertEqual(value, 'a: Sai; b: Đúng; c: Chưa xác định')
        q = {'opt':['apple','banana','cherry','date'], 'ans':'B'}
        assignment = next(n for n in ast.walk(TREE) if isinstance(n,ast.Assign)
                          and any(isinstance(t,ast.Name) and t.id=='is_p1_right' for t in n.targets))
        result = eval(compile(ast.Expression(body=assignment.value), 'review-test','eval'),
                      {'mcq_answer_matches':mcq_answer_matches,'q':q,'user_c':'banana'})
        self.assertTrue(result)

    def test_annotation_unicode_font_is_passed_to_pillow(self):
        import os, logging
        from PIL import Image, ImageDraw, ImageFont
        f = load_function('annotate_student_work', Image=Image, ImageDraw=ImageDraw,
                          ImageFont=ImageFont, os=os, logging=logging)
        image = Image.new('RGB',(400,200),'white')
        original = ImageDraw.ImageDraw.text
        fonts = []
        def capture(draw, *args, **kwargs):
            fonts.append(kwargs.get('font'))
            return original(draw,*args,**kwargs)
        with patch.object(ImageDraw.ImageDraw,'text',capture):
            result = f(image,[{'box':[100,100,500,800],'type':'ok','label':'Biến đổi đúng'}])
        self.assertEqual(result.size,image.size)
        self.assertTrue(fonts)
        self.assertTrue(all(isinstance(font,ImageFont.FreeTypeFont) for font in fonts))

    def test_shared_bank_write_requires_existing_admin_authentication(self):
        from unittest.mock import Mock
        node = next(n for n in ast.walk(TREE) if isinstance(n,ast.If)
                    and isinstance(n.test,ast.Call) and isinstance(n.test.func,ast.Attribute)
                    and n.test.func.attr=='button' and n.test.args
                    and isinstance(n.test.args[0],ast.Constant) and n.test.args[0].value=='🏛️ Nạp Shard Quốc Gia')
        writer = Mock()
        st = SimpleNamespace(session_state={}, button=lambda *args,**kwargs:True, warning=Mock(), spinner=Mock())
        exec(compile(ast.Module(body=[node],type_ignores=[]),'shard-auth-test','exec'),
             {'st':st,'ree':SimpleNamespace(append_exam_to_national_shard=writer),'p_gv':{}})
        writer.assert_not_called()
        st.warning.assert_called_once()
        st.spinner.assert_not_called()

    def test_rejected_bank_draft_does_not_crash_or_start_exam(self):
        from unittest.mock import Mock
        node = next(n for n in ast.walk(TREE) if isinstance(n,ast.If)
                    and isinstance(n.test,ast.BoolOp) and any(isinstance(v,ast.Name) and v.id=='blended' for v in n.test.values))
        original = {'old':'keep'}
        st = SimpleNamespace(session_state=SimpleNamespace(exam_data=original),error=Mock())
        enrich = Mock(side_effect=ValueError('Draft cannot be used'))
        exec(compile(ast.Module(body=[node],type_ignores=[]),'bank-boundary-test','exec'),
             {'blended':{'p1':[{}]},'st':st,'enrich_exam_data':enrich,'custom_matrix_prompt':'',
              'original_paper_mode':False})
        self.assertIs(st.session_state.exam_data,original)
        st.error.assert_called_once_with('Draft cannot be used')

    def test_wrong_topic_level_does_not_disqualify_unlabelled_valid_replacement(self):
        from tests.test_statistics_topic_conflict import statistics,cubic,FUNCTIONS
        from services.context_recovery import repair_exam_context
        candidate = cubic()
        candidate.pop('level')
        result = repair_exam_context({'p1':[statistics()]},'Toán học',12,topics=FUNCTIONS,
                                     bank_provider=lambda *_:{'p1':[candidate]})
        self.assertEqual(result['context_recovery']['unresolved'],0)
        self.assertNotIn('level',result['p1'][0])
        self.assertFalse(result['p1'][0]['replacement_audit']['academic_verified'])

    def test_seen_duplicates_do_not_consume_replacement_validation_budget(self):
        from tests.test_context_recovery import TestContextRecovery
        from services.context_recovery import repair_exam_context
        helper = TestContextRecovery()
        source = helper.missing()
        duplicate = dict(source, subject='Toán học', grade=12)
        candidate = helper.replacement()
        result = repair_exam_context({'p1':[source]},'Toán',12,topics=['Hàm số'],
                                     bank_provider=lambda *_:{'p1':[duplicate]*250+[candidate]})
        self.assertEqual(result['context_recovery']['unresolved'],0)
        self.assertEqual(result['p1'][0]['q'],candidate['q'])
