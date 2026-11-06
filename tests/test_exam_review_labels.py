import unittest
from copy import deepcopy
from qa_runtime import mcq_key_option, mcq_answer_matches
from services.exam_delivery import question_solution_text, answer_source_label
from services.official_paper import original_tin0530


class ReviewLabelsTests(unittest.TestCase):
    def test_original_mcq_explanations_preserve_scope_and_css_caveat(self):
        for track in ('CS', 'ICT'):
            exam = original_tin0530(track)
            self.assertTrue(all('không phải lời giải do Bộ ban hành' in
                                question_solution_text(q) for q in exam['p1']))
            self.assertIn('display:flex', question_solution_text(exam['p1'][6]))
            self.assertIn('a) Đúng:', question_solution_text(exam['p2'][0]))
            self.assertTrue(all('không phải lời giải do Bộ ban hành' in question_solution_text(q) for q in exam['p2']))

    def test_explanation_from_other_source_or_wrong_key_is_rejected(self):
        import json
        from pathlib import Path
        from unittest.mock import patch
        read_text = Path.read_text
        for field in ('archive', 'key'):
            def altered(path, *args, **kwargs):
                text = read_text(path, *args, **kwargs)
                if path.name.endswith('.solutions.json'):
                    payload = json.loads(text)
                    if field == 'archive':
                        payload['archive_sha256'] = 'wrong'
                    else:
                        payload['records']['I.1']['answer'] = 'D'
                    return json.dumps(payload)
                return text
            with patch.object(Path, 'read_text', altered):
                with self.assertRaises(ValueError):
                    original_tin0530('CS')

    def test_key_option_uses_same_index_as_scoring_for_prefixed_and_plain_options(self):
        for options in [['<i>','<img>','<p>','<ol>'],['A. one','B. two','C. three','D. four']]:
            q={'opt':options,'ans':'B'};before=deepcopy(q)
            result=mcq_key_option(q)
            self.assertNotEqual(result,'B. B')
            self.assertTrue(mcq_answer_matches(q,options[1]))
            self.assertEqual(q,before)
        self.assertEqual(mcq_key_option({'opt':['one','two'],'ans':'B'}),'B. two')

    def test_missing_key_or_option_is_not_invented(self):
        self.assertEqual(mcq_key_option({'opt':['one'],'ans':''}),'Chưa xác định')
        self.assertIn('chưa có nội dung',mcq_key_option({'ans':'B'}))

    def test_missing_explanation_is_explicit_and_short_real_explanation_is_retained(self):
        self.assertIn('Chưa có lời giải độc lập',question_solution_text({}))
        self.assertEqual(question_solution_text({'explain':'x=2'}),'x=2')
        self.assertEqual(question_solution_text({'expl':'Theo dữ kiện gốc'}),'Theo dữ kiện gốc')

    def test_ministry_key_attribution_requires_reviewed_original_source_context(self):
        self.assertNotIn('Bộ',answer_source_label({'is_ai_generated':True}))
        exam=original_tin0530('ICT')
        self.assertIn('Khóa Bộ',answer_source_label(exam))
        exam['original_source_archive_sha256']='wrong'
        self.assertNotIn('Bộ',answer_source_label(exam))
