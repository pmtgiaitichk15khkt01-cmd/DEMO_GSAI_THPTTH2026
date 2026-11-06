import unittest
from copy import deepcopy
from services.reviewed_solutions import apply_reviewed_solutions
from services.academic_context import subjects_for_grade


class ReviewedSolutionsTests(unittest.TestCase):
    def test_shared_binding_across_supported_subject_grade_contexts(self):
        # Structural contract matrix only; these are not real-lesson acceptance.
        for grade in range(6,13):
            for subject in subjects_for_grade(grade):
                exam={'subject':subject,'grade':grade,'year':2025,'code':'A',
                      'p1':[{'source_id':'I.1','q':'unchanged','opt':['a','b'],'ans':'B'}],
                      'p2':[{'source_id':'II.1','q':'unchanged TF','stmts':[{'t':'s','a':False}]}]}
                before=deepcopy(exam)
                doc={'archive_sha256':'source','subject':subject,'grade':grade,'year':2025,'variant':'A',
                     'records':{'I.1':{'answer':'B','explanation':'Reviewed MCQ'},
                                'II.1.a':{'answer':False,'explanation':'Reviewed TF'}}}
                result=apply_reviewed_solutions(exam,doc,'source')
                self.assertEqual(exam,before)
                self.assertEqual(result['p1'][0]['ans'],'B')
                self.assertFalse(result['p2'][0]['stmts'][0]['a'])
                self.assertIn('a) Sai:',result['p2'][0]['explain'])
                self.assertNotIn('academic_verified',result)

    def test_wrong_context_key_and_empty_explanation_fail_closed(self):
        exam={'subject':'Tin học','grade':12,'year':2025,'code':'0530',
              'p2':[{'source_id':'II.1','stmts':[{'t':'s','a':True}]}]}
        doc={'archive_sha256':'source','subject':'Tin học','grade':12,'year':2025,'variant':'0530',
             'records':{'II.1.a':{'answer':True,'explanation':'Reviewed'}}}
        for field,value in [('subject','Toán học'),('grade',11),('year',2026),('variant','0525'),('archive_sha256','other')]:
            bad=deepcopy(doc);bad[field]=value
            with self.assertRaises(ValueError):apply_reviewed_solutions(exam,bad,'source')
        for record in [{'answer':False,'explanation':'bad'},{'answer':1,'explanation':'bad'},
                       {'answer':True,'explanation':''}]:
            bad=deepcopy(doc);bad['records']['II.1.a']=record
            with self.assertRaises(ValueError):apply_reviewed_solutions(exam,bad,'source')
