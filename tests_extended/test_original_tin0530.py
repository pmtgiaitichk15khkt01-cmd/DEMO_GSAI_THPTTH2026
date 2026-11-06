import hashlib
import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from services.official_paper import original_tin0530, PACKS
from services.bank_storage import read_curated_exam_packs
from services.exam_delivery import exam_delivery_held


class OriginalTin0530Tests(unittest.TestCase):
    def test_both_pathways_preserve_official_keys_and_source_archive(self):
        source = PACKS / 'tin_2025_0530.json.xz'
        before = hashlib.sha256(source.read_bytes()).hexdigest()
        for pathway, expected in [('CS', ['II.1','II.2','II.3','II.4']),
                                  ('ICT', ['II.1','II.2','II.5','II.6'])]:
            exam = original_tin0530(pathway)
            self.assertEqual(len(exam['p1']), 24)
            self.assertEqual([q['source_id'] for q in exam['p2']], expected)
            self.assertEqual(exam['duration'], 50)
            self.assertEqual(''.join(q['ans'] for q in exam['p1']), 'BAADDABCBDAABADDCCDDBDBC')
            self.assertEqual(exam['p1'][6]['ans'], 'B')
            self.assertTrue(all(q['is_real_bank_question'] and not q['is_ai_generated']
                                for part in ('p1','p2') for q in exam[part]))
            self.assertEqual(exam['p2'][-1]['orig_pos'], expected[-1])
            self.assertIn('app_reuse_review_issues', exam['p1'][6])
            self.assertFalse(exam_delivery_held(exam))
            self.assertFalse(exam['curriculum_audit']['academic_verified'])
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), before)
        original = read_curated_exam_packs(PACKS, subject='Tin học', grade=12)[0]
        self.assertTrue(exam_delivery_held(original))
        self.assertTrue(original['p1'][6]['source_review_issues'])

    def test_pathway_required_and_vietnamese_names_supported(self):
        for invalid in ['', 'common', None, 'unknown']:
            with self.assertRaises(ValueError):
                original_tin0530(invalid)
        self.assertEqual(original_tin0530('Tin học ứng dụng')['pathway'], 'ICT')
        self.assertEqual(original_tin0530('Khoa học máy tính')['pathway'], 'CS')

    def test_changed_source_checksum_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = json.loads((PACKS/'tin_2025_0530.manifest.json').read_text(encoding='utf8'))
            manifest['archive_sha256'] = '0'*64
            (Path(tmp)/'tin_2025_0530.manifest.json').write_text(json.dumps(manifest),encoding='utf8')
            with self.assertRaises(ValueError):
                original_tin0530('CS', directory=tmp)

    def test_new_hold_or_modified_key_is_not_bypassed(self):
        original = read_curated_exam_packs(PACKS, subject='Tin học', grade=12)[0]
        for mutation in ['hold', 'key', 'statement']:
            exam = deepcopy(original)
            if mutation == 'hold':
                exam['p1'][0]['source_review_issues'] = ['unread_source']
            elif mutation == 'key':
                exam['p1'][0]['ans'] = 'D'
            else:
                exam['p2'][0]['stmts'][0]['a'] = False
            with patch('services.official_paper.read_curated_exam_packs', return_value=[exam]):
                with self.assertRaises(ValueError):
                    original_tin0530('CS')

    def test_curated_pack_hash_and_station_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = json.loads((PACKS/'tin_2025_0530.manifest.json').read_text(encoding='utf8'))
            (Path(tmp)/manifest['filename']).write_bytes(b'wrong file')
            receipt = Path(tmp)/'tin_2025_0530.manifest.json'
            receipt.write_text(json.dumps(manifest),encoding='utf8')
            with self.assertRaises(ValueError):
                read_curated_exam_packs(tmp,subject='Tin học',grade=12)
            manifest['station'] = 1
            receipt.write_text(json.dumps(manifest),encoding='utf8')
            self.assertEqual(read_curated_exam_packs(tmp,subject='Tin học',grade=12),[])

    def test_real_scoring_service_gives_ten_and_does_not_reward_blanks(self):
        from services.scoring_service import grade_part1, grade_part2
        for track in ('CS', 'ICT'):
            exam = original_tin0530(track)
            answers = {f'p1_{i}': q['ans'] for i, q in enumerate(exam['p1'])}
            for i, question in enumerate(exam['p2']):
                answers.update({f'p2_{i}_{j}': 'Đúng' if stmt['a'] else 'Sai'
                                for j, stmt in enumerate(question['stmts'])})
            self.assertEqual(grade_part1(exam['p1'], answers, subject='Tin học'), (6.0, 24, 24))
            self.assertEqual(grade_part2(exam['p2'], answers), (4.0, 16, 16))
            self.assertEqual(grade_part1(exam['p1'], {}, subject='Tin học')[0], 0)
            self.assertEqual(grade_part2(exam['p2'], {})[0], 0)

    def test_mixed_pool_does_not_gain_original_only_or_specialized_questions(self):
        import real_exam_engine as engine
        pool = engine.get_baseline_questions_pool('Tin học', 12)
        rows = [q for part in ('p1', 'p2') for q in pool[part]
                if q.get('source_variant') == '0530' and q.get('source_year') == 2025]
        self.assertEqual(len(rows), 25)
        self.assertNotIn('I.7', [q['source_id'] for q in rows])
        self.assertTrue(all(q['source_track'] == 'common' for q in rows))

    def test_curated_common_units_have_independent_reviews_in_source_context(self):
        from services.cognitive_runtime import independent_exam_audit
        exam = read_curated_exam_packs(PACKS, subject='Tin học', grade=12)[0]
        audit = independent_exam_audit(exam, 'Tin học', 12, as_of='2026-11-05')
        self.assertEqual(audit['verified_records'], 31)

    def test_original_ui_branch_persists_duration_and_avoids_recovery(self):
        import ast
        source = (PACKS.parents[1]/'app.py').read_text(encoding='utf-8-sig')
        tree = ast.parse(source)
        branches = [n for n in ast.walk(tree) if isinstance(n, ast.If)
                    and isinstance(n.test, ast.Name) and n.test.id == 'original_paper_mode'
                    and any(isinstance(c, ast.Call) and isinstance(c.func, ast.Name)
                            and c.func.id == 'original_tin0530' for c in ast.walk(n))]
        self.assertEqual(len(branches), 1)
        active = ast.Module(body=branches[0].body, type_ignores=[])
        self.assertIn('st.session_state.exam_time_mins = 50', ast.unparse(active))
        calls = [c.func.id for c in ast.walk(active) if isinstance(c, ast.Call)
                 and isinstance(c.func, ast.Name)]
        self.assertNotIn('enrich_exam_data', calls)
        self.assertNotIn('call_gemini_with_fallback', calls)

    def test_original_numbering_preserves_ict_five_six_without_touching_scoring(self):
        from services.official_paper import original_question_number, original_print_context
        exam = original_tin0530('ICT')
        self.assertEqual([original_question_number(exam,q,i) for i,q in enumerate(exam['p2'],1)], [1,2,5,6])
        self.assertEqual(original_question_number({}, {'source_id':'II.6'}, 4), 4)
        self.assertEqual(original_print_context(exam)['duration'],50)
        forged = deepcopy(exam);forged['code']='9999'
        with self.assertRaises(ValueError):
            original_print_context(forged)

    def test_actual_export_headers_keys_and_code_for_both_original_pathways(self):
        import contextlib,io
        with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
            import app
            for track in ['CS','ICT']:
                exam = original_tin0530(track)
                before = deepcopy(exam)
                for style in ['form1','form2']:
                    markup,tex = app.build_exam_exports(exam,'Tin học','Lớp 12',45,
                        include_answers=True,template_style=style,show_support_qr=False)
                    self.assertIn('data-original-paper="2025-0530"',markup)
                    self.assertIn('ĐỀ THI TỐT NGHIỆP THPT NĂM 2025',markup)
                    self.assertIn('Thời gian: 50 phút',markup)
                    self.assertNotIn('Kỳ thi KSCL',markup)
                    self.assertNotIn('ĐỀ KHẢO SÁT CHẤT LƯỢNG',markup)
                    self.assertIn('không phải bản PDF gốc',markup)
                    self.assertNotIn('```',markup)
                    self.assertNotIn('```',tex)
                    self.assertIn('exam-source-code',markup)
                    self.assertIn('BẢNG KHÓA ĐÁP ÁN VÀ ĐIỂM LUYỆN TẬP',markup)
                    self.assertNotIn('MA TRẬN CHẤM ĐIỂM CHUẨN BỘ',markup)
                    if track == 'ICT':
                        self.assertIn('trả lời các câu 1, 2, 5, 6',markup)
                        self.assertIn('trả lời các câu 1, 2, 5, 6',tex)
                        self.assertIn("bold;'>Câu 5</td>",markup)
                        self.assertIn("bold;'>Câu 6</td>",markup)
                        self.assertIn(r'\textbf{Câu 5}',tex)
                        self.assertIn(r'\textbf{Câu 6}',tex)
                    self.assertEqual(exam,before)
