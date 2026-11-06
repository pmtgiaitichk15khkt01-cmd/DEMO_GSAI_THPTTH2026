from copy import deepcopy
import unittest
from services.cognitive_levels import assessment_content_hash, validate_cognitive_review, validate_reference_item


class CognitiveReviewGateTests(unittest.TestCase):
    def test_malformed_mapping_and_future_source_cannot_crash_or_pass(self):
        for malformed in (None, '9', 9, {}):
            result = validate_reference_item({'mapped_grades': malformed, 'mapped_outcomes': malformed},
                subject='Toán học', grade=9, outcome_id='outcome9')
            self.assertFalse(result['eligible'])
        r = deepcopy(self.review); r['curriculum_source']['read_on'] = '2027-01-01'
        self.assertFalse(self.check(r)['verified'])

    def test_entrance_grade10_is_not_automatically_grade10_curriculum(self):
        item = dict(issuer_type='department', issuer='Sở mẫu', source_url='https://example.org/exam',
            school_year='2025-2026', exam_type='entrance_grade10', paper_sha256='fixture-paper',
            answer_sha256='fixture-answer', source_locator='Câu 1', curriculum='CT2018',
            subject='Toán học', mapped_grades=[9], mapped_outcomes=['outcome9'],
            independent_answer_check='passed', published_level='VDC')
        good = validate_reference_item(item, subject='Toán học', grade=9, outcome_id='outcome9')
        self.assertTrue(good['eligible'])
        self.assertEqual(good['official_level_claim'], '')
        self.assertFalse(validate_reference_item(item, subject='Toán học', grade=10, outcome_id='outcome9')['eligible'])
        item['known_error'] = True
        self.assertFalse(validate_reference_item(item, subject='Toán học', grade=9, outcome_id='outcome9')['eligible'])

    def setUp(self):
        self.q = {'q': 'Một câu đã thẩm định', 'ans': 'A', 'level': 'NB', 'solution_steps': ['Đối chiếu dữ kiện']}
        self.review = dict(subject='Toán học', grade=10, topic='Bài 1',
            content_sha256=assessment_content_hash(self.q), reviewed_level='NB', reviewer='local-review-record',
            learning_outcome='Yêu cầu cần đạt đã đối chiếu', solution_rubric='Lời giải kiểm độc lập',
            cognitive_reason='Nhớ lại dữ kiện đã học', cognitive_operations=['Nhớ lại'],
            assessment_purpose='practice', recheck_after='2026-11-30',
            curriculum_source={'url':'https://example.org/ct','locator':'Mục đã đọc','read_on':'2026-11-02','document_status':'final','read_scope':'relevant_content'},
            textbook_source={'url':'https://example.org/kntt','locator':'Bài đã đọc','read_on':'2026-11-02','document_status':'final','read_scope':'relevant_content'},
            legal_basis=[{'code':'fixture-only','url':'https://example.org/law','locator':'Điều đã đọc',
                'checked_on':'2026-11-02','effective_from':'2021-09-05','applicable_purpose':'practice'}])

    def check(self, review=None, question=None):
        return validate_cognitive_review(question or self.q, review or self.review,
            subject='Toán học', grade=10, topic='Bài 1', as_of='2026-11-02')

    def test_complete_record_and_changed_answer_or_solution(self):
        self.assertTrue(self.check()['verified'])
        for key in ('ans', 'solution_steps', 'q'):
            q = deepcopy(self.q); q[key] = 'changed'
            self.assertFalse(self.check(question=q)['verified'])

    def test_cross_grade_future_expired_or_wrong_purpose_never_pass(self):
        for field, value in [('effective_from','2026-12-01'), ('effective_until','2026-11-02'),
                             ('applicable_purpose','graduation_exam')]:
            r = deepcopy(self.review); r['legal_basis'][0][field] = value
            self.assertFalse(self.check(r)['verified'])
        r = deepcopy(self.review); r['grade'] = 12
        self.assertFalse(self.check(r)['verified'])

    def test_ai_self_claim_and_long_solution_are_not_review(self):
        self.assertFalse(validate_cognitive_review(self.q, {}, subject='Toán học', grade=10,
            topic='Bài 1', as_of='2026-11-02')['verified'])
        r = deepcopy(self.review); r['reviewed_level'] = 'VDC'
        self.assertIn('missing_advanced_transfer_reason', self.check(r)['issues'])
        r['advanced_transfer_reason'] = 'Căn cứ chuyển giao đã thẩm định riêng'
        self.assertEqual(self.check(r)['reference_bucket'], 'Vận dụng')

    def test_book_sample_or_unknown_edition_does_not_validate_final_mapping(self):
        for status in ('sample', 'draft', None):
            r = deepcopy(self.review); r['textbook_source']['document_status'] = status
            self.assertIn('non_final_or_unverified_textbook_source', self.check(r)['issues'])

    def test_contents_or_catalog_cannot_stand_in_for_reading_actual_content(self):
        for field in ('curriculum_source', 'textbook_source'):
            for scope in ('contents_only', 'catalog_only', 'title_only', None):
                with self.subTest(field=field, scope=scope):
                    r = deepcopy(self.review); r[field]['read_scope'] = scope
                    result = self.check(r)
                    self.assertFalse(result['verified'])
                    self.assertIn('relevant_content_not_read_' + field, result['issues'])
