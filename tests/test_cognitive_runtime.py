import ast
import copy
import json
from pathlib import Path
import tempfile
import unittest
from services.cognitive_runtime import review_binding, independent_question_audit, independent_exam_audit
from services.cognitive_levels import assessment_content_hash


class RuntimeReviewTests(unittest.TestCase):
    def test_exact_independent_record_context_purpose_and_shared_payload(self):
        from tests.test_cognitive_review_gate import CognitiveReviewGateTests
        fixture=CognitiveReviewGateTests(); fixture.setUp()
        q=fixture.q; shared={'code':'original'}
        review=copy.deepcopy(fixture.review)
        review['assessment_purpose']='station1_self_study'
        for basis in review['legal_basis']:basis['applicable_purpose']='station1_self_study'
        digest=assessment_content_hash(review_binding(q,shared));review['content_sha256']=digest
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'reviews.json'
            path.write_text(json.dumps({'schema_version':1,'reviews':{digest:review}}),encoding='utf-8')
            def check(question=q,**change):
                args=dict(subject='Toán học',grade=10,topic='Bài 1',purpose='station1_self_study',
                          shared_context=shared,as_of='2026-11-02',registry_path=path)
                args.update(change)
                return independent_question_audit(question,**args)
            self.assertTrue(check()['verified'])
            for change in ({'grade':11},{'purpose':'station3_assessment'},
                           {'shared_context':{'code':'changed'}},{'as_of':'2026-12-01'}):
                self.assertFalse(check(**change)['verified'])
            changed=copy.deepcopy(q);changed['ans']='B'
            self.assertFalse(check(changed)['verified'])
            path.write_text('{bad',encoding='utf-8')
            self.assertFalse(check()['verified'])

    def test_generated_claims_never_approve_and_tf_context_is_bound(self):
        exam={'topic':'Bài 1','p2':[{'q':'context','stmts':[{'t':'A','a':True}, {'t':'B','a':False}]}]}
        original=copy.deepcopy(exam)
        audit=independent_exam_audit(exam,'Toán học',10,as_of='2026-11-02')
        self.assertEqual(audit['verified_records'],0)
        self.assertEqual(len(audit['rows']),3)
        changed=copy.deepcopy(exam);changed['p2'][0]['q']='other context'
        other=independent_exam_audit(changed,'Toán học',10,as_of='2026-11-02')
        self.assertNotEqual(audit['rows'][1]['content_sha256'],other['rows'][1]['content_sha256'])
        self.assertEqual(exam,original)
        claim={'q':'Self claim','cognitive_audit':{'verified':True},'reviewer':'AI'}
        self.assertFalse(independent_question_audit(claim,subject='Toán học',grade=10,
            topic='Bài 1',purpose='station1_self_study',as_of='2026-11-02')['verified'])

    def test_actual_t1_and_t3_paths_invoke_independent_sidecar(self):
        root=Path(__file__).parents[1]
        for filename,target in [('app.py','independent_lesson_quiz_audit'),
                                ('services/curriculum_policy.py','independent_exam_audit')]:
            tree=ast.parse((root/filename).read_text(encoding='utf-8-sig'))
            self.assertTrue(any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name)
                                and n.func.id==target for n in ast.walk(tree)))

    def test_batch_loads_registry_once_without_bank_or_api(self):
        from unittest.mock import patch
        from services.cognitive_runtime import independent_lesson_quiz_audit
        q={'q':'A','stmts':[{'t':'one','a':True},{'t':'two','a':False}]}
        with patch('services.cognitive_runtime._load_reviews', return_value={}) as load:
            independent_exam_audit({'p2':[q,q]},'Toán học',10,as_of='2026-11-02')
            self.assertEqual(load.call_count,1)
        with patch('services.cognitive_runtime._load_reviews', return_value={}) as load:
            rows=independent_lesson_quiz_audit([q,q],'Toán học',10,'Bài 1','lesson',as_of='2026-11-02')
            self.assertEqual(load.call_count,1)
            self.assertTrue(all(not r['verified'] for r in rows))

    def test_delivery_preserves_payload_and_review_is_per_statement(self):
        from unittest.mock import patch
        from services.curriculum_policy import prepare_exam_for_delivery
        from tests.test_cognitive_review_gate import CognitiveReviewGateTests
        fixture = CognitiveReviewGateTests(); fixture.setUp()
        question = {'q':'Context', 'stmts':[{'t':'one','a':True}, {'t':'two','a':False}, {'t':'three','a':True}, {'t':'four','a':False}]}
        exam = {'topic':'Bài 1', 'p2':[question]}
        original = copy.deepcopy(exam)
        digest = assessment_content_hash(review_binding(question['stmts'][0], review_binding(question)))
        review = copy.deepcopy(fixture.review)
        review.update(content_sha256=digest, assessment_purpose='station3_assessment', recheck_after='2099-01-01')
        for basis in review['legal_basis']: basis['applicable_purpose']='station3_assessment'
        with patch('services.cognitive_runtime._load_reviews', return_value={digest:review}):
            delivered = prepare_exam_for_delivery(exam, 'Toán học', 10)
        rows = delivered['independent_cognitive_audit']['rows']
        self.assertEqual([r['verified'] for r in rows], [False, True, False, False, False])
        self.assertEqual(delivered['p2'], original['p2'])
        self.assertEqual(exam, original)
        self.assertFalse(delivered['curriculum_audit']['academic_verified'])

    def test_reading_list_is_audited_and_malformed_record_fails_closed(self):
        from unittest.mock import patch
        q = {'q':'reading question', 'ans':'A'}
        with patch('services.cognitive_runtime._load_reviews', return_value={}):
            audit = independent_exam_audit({'part_doc_hieu':[q]}, 'Ngữ văn', 9)
        self.assertEqual(len(audit['rows']), 1)
        digest = assessment_content_hash(review_binding(q))
        for malformed in (None, [], 'approved', True):
            with patch('services.cognitive_runtime._load_reviews', return_value={digest:malformed}):
                result = independent_question_audit(q, subject='Ngữ văn', grade=9,
                    topic='Bài 1', purpose='station1_self_study')
            self.assertFalse(result['verified'])

    def test_actual_t1_render_assignment_binds_current_lesson(self):
        from types import SimpleNamespace
        from unittest.mock import patch
        from tests.test_cognitive_review_gate import CognitiveReviewGateTests
        fixture = CognitiveReviewGateTests(); fixture.setUp()
        tree = ast.parse((Path(__file__).parents[1]/'app.py').read_text(encoding='utf-8-sig'))
        assignment = next(n for n in ast.walk(tree) if isinstance(n, ast.Assign)
            and isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Name)
            and n.value.func.id == 'independent_lesson_quiz_audit')
        from services.cognitive_runtime import independent_lesson_quiz_audit
        state = {'current_topic':'Bài 1', 'current_lesson':'original lesson'}
        digest = assessment_content_hash(review_binding(fixture.q, {'lesson':'original lesson'}))
        review = copy.deepcopy(fixture.review)
        review.update(content_sha256=digest, assessment_purpose='station1_self_study', recheck_after='2099-01-01')
        for basis in review['legal_basis']: basis['applicable_purpose']='station1_self_study'
        env = dict(st=SimpleNamespace(session_state=state), quiz_list=[fixture.q], subject='Toán học',
            grade_num=10, independent_lesson_quiz_audit=independent_lesson_quiz_audit)
        code = compile(ast.fix_missing_locations(ast.Module(body=[assignment], type_ignores=[])), 'actual T1 assignment', 'exec')
        with patch('services.cognitive_runtime._load_reviews', return_value={digest:review}):
            exec(code, env)
            self.assertTrue(state['t1_independent_cognitive_audit'][0]['verified'])
            state['current_lesson']='changed lesson'
            exec(code, env)
            self.assertFalse(state['t1_independent_cognitive_audit'][0]['verified'])

    def test_same_question_review_cannot_cross_assessment_context(self):
        from unittest.mock import patch
        from tests.test_cognitive_review_gate import CognitiveReviewGateTests
        fixture = CognitiveReviewGateTests(); fixture.setUp()
        context = {'exam_type':'graduation_reference_practice', 'curriculum':'CT2018'}
        exam = dict(context, topic='Bài 1', p1=[fixture.q])
        review = copy.deepcopy(fixture.review)
        review.update(content_sha256=assessment_content_hash(review_binding(fixture.q,
            {'assessment_context':context})), assessment_purpose='station3_assessment')
        for basis in review['legal_basis']: basis['applicable_purpose']='station3_assessment'
        with patch('services.cognitive_runtime._load_reviews', return_value={review['content_sha256']:review}):
            self.assertTrue(independent_exam_audit(exam,'Toán học',10,as_of='2026-11-02')['rows'][0]['verified'])
            for key,value in [('exam_type','periodic_assessment'),('curriculum','CT2006'),
                              ('assessment_purpose','other_use'),('textbook','other_book')]:
                changed = copy.deepcopy(exam); changed[key]=value
                self.assertFalse(independent_exam_audit(changed,'Toán học',10,
                    as_of='2026-11-02')['rows'][0]['verified'])
            stripped = copy.deepcopy(exam); stripped.pop('exam_type')
            self.assertFalse(independent_exam_audit(stripped,'Toán học',10,
                as_of='2026-11-02')['rows'][0]['verified'])

    def test_assessment_context_binds_tf_parent_and_reading_rows(self):
        exam = {'exam_type':'practice','p2':[{'q':'Context','stmts':[{'t':'A','a':True}]}],
                'part_doc_hieu':{'passage':'Read this','questions':[{'q':'Explain','ans':'A'}]}}
        original = copy.deepcopy(exam)
        first = independent_exam_audit(exam,'Ngữ văn',9)
        exam['exam_type']='periodic_assessment'
        other = independent_exam_audit(exam,'Ngữ văn',9)
        self.assertEqual(len(first['rows']),3)
        self.assertTrue(all(a['content_sha256'] != b['content_sha256']
            for a,b in zip(first['rows'],other['rows'])))
        self.assertEqual(original['p2'],exam['p2'])
        self.assertEqual(original['part_doc_hieu'],exam['part_doc_hieu'])

    def test_explicit_prerequisite_retains_outcome_grade_and_requires_evidence(self):
        from unittest.mock import patch
        from tests.test_cognitive_review_gate import CognitiveReviewGateTests
        fixture=CognitiveReviewGateTests(); fixture.setUp()
        q=copy.deepcopy(fixture.q); q['mapped_outcome_grades']=[10]
        shared={'assessment_context':{'exam_type':'practice'}}
        review=copy.deepcopy(fixture.review)
        review.update(content_sha256=assessment_content_hash(review_binding(q,shared)),
            assessment_grade=12,outcome_grade=10,prerequisite_use_reason='Explicit earlier-grade prerequisite review')
        def check(r=review, question=q, grade=12, context=shared):
            with patch('services.cognitive_runtime._load_reviews',return_value={review['content_sha256']:r}):
                return independent_question_audit(question,subject='Toán học',grade=grade,
                    topic='Bài 1',purpose='practice',shared_context=context,as_of='2026-11-02')
        good=check(); self.assertTrue(good['verified'])
        self.assertEqual(good['mapped_outcome_grade'],10)
        self.assertEqual(good['assessment_grade'],12)
        for key in ('assessment_grade','outcome_grade','prerequisite_use_reason'):
            changed=copy.deepcopy(review);changed.pop(key)
            self.assertFalse(check(changed)['verified'])
        changed=copy.deepcopy(q);changed['mapped_outcome_grades']=[11]
        self.assertFalse(check(question=changed)['verified'])
        self.assertFalse(check(grade=11)['verified'])
        self.assertFalse(check(grade=10)['verified'])
        self.assertFalse(check(context={})['verified'])

    def test_tf_containers_do_not_claim_aggregate_level_or_count_as_pending_answers(self):
        exam={'p2':[{'q':'Shared task','level':'VDC','stmts':[
            {'t':'Recall','a':True,'level':'NB'},{'t':'Interpret','a':False,'level':'TH'}]}]}
        audit=independent_exam_audit(exam,'Toán học',10,as_of='2026-11-02')
        self.assertEqual(audit['response_units'],2)
        self.assertEqual(audit['context_containers'],1)
        self.assertEqual(audit['pending_records'],2)
        parent=audit['rows'][0]
        self.assertEqual(parent['record_role'],'statement_container')
        self.assertFalse(parent['verified'])
        self.assertNotIn('reviewed_level',parent)
        self.assertEqual(parent['status'],'context_bound_only')

    def test_valid_record_cannot_override_known_source_or_shared_context_hold(self):
        from unittest.mock import patch
        from tests.test_cognitive_review_gate import CognitiveReviewGateTests
        fixture=CognitiveReviewGateTests();fixture.setUp()
        for location in ('question','parent','reading'):
            q=copy.deepcopy(fixture.q);shared={}
            if location=='question':q['source_review_issues']=['Missing premise']
            if location=='parent':shared={'question':{'q':'Shared','source_review_issues':['Missing premise']}}
            if location=='reading':shared={'reading':{'passage':'Text','source_review_issues':['Unverified attribution']}}
            review=copy.deepcopy(fixture.review)
            digest=assessment_content_hash(review_binding(q,shared));review['content_sha256']=digest
            with patch('services.cognitive_runtime._load_reviews',return_value={digest:review}):
                result=independent_question_audit(q,subject='Toán học',grade=10,topic='Bài 1',
                    purpose='practice',shared_context=shared,as_of='2026-11-02')
            self.assertFalse(result['verified'])
            self.assertEqual(result['delivery_status'],'held_source_issue')
            self.assertIn('unresolved_source_review_hold',result['issues'])
            self.assertEqual(result['reviewed_level'],'')

    def test_one_held_statement_does_not_hold_unflagged_sibling(self):
        exam={'p2':[{'q':'Shared','stmts':[
            {'t':'Held','a':True,'source_review_issues':['Missing premise']},
            {'t':'Other','a':False}]}]}
        audit=independent_exam_audit(exam,'Toán học',10)
        self.assertEqual(audit['held_source_records'],1)
        self.assertEqual(audit['needs_review_records'],1)
        self.assertEqual(audit['pending_records'],2)
        self.assertEqual(audit['rows'][2]['delivery_status'],'needs_teacher_review')
