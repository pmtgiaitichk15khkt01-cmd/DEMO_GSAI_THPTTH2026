import copy
import hashlib
import json
import re
import unittest
from unittest.mock import patch

from services import lesson_sources as sources
from services.lesson_export import build_lesson_html
from services.curriculum_policy import lesson_generation_request


TOPIC = 'Viết bài văn kể lại một trải nghiệm của em — Ngữ văn 6, Kết nối tri thức với cuộc sống, Bài 3: Yêu thương và chia sẻ.'


class LessonSourceReviewTests(unittest.TestCase):
    def test_owner_confirmed_national_catalog_is_available_for_all_supported_pairs(self):
        from services.academic_context import subjects_for_grade
        count = 0
        for grade in range(6, 13):
            for subject in subjects_for_grade(grade):
                books = sources.books_for(subject, grade)
                portal = next(b for b in books if b['url'] == f'https://www.thsqg.vn/sach?lop={grade}')
                self.assertEqual(portal['kind'], 'portal')
                publisher = next(b for b in books if b['url'] == 'https://truonghocsoquocgia.nxbgd.vn/books')
                self.assertEqual(publisher['kind'], 'portal')
                self.assertIn('Tra cứu', portal['title'])
                count += 1
        self.assertEqual(count, 65)
    def test_tutor_receives_exact_review_without_cross_lesson_facts(self):
        context = sources.reviewed_tutor_source_context('Ngữ văn', 6, TOPIC)
        self.assertIn('ĐỐI CHIẾU CHO ĐÚNG BÀI', context)
        self.assertIn('SGV Ngữ văn 6', context)
        self.assertIn('ngoài văn bản', context)
        missing = sources.reviewed_tutor_source_context('Toán học', 6, TOPIC)
        self.assertIn('Chưa có hồ sơ', missing)
        self.assertNotIn('SGV Ngữ văn 6', missing)

    def setUp(self):
        sources._review_registry.cache_clear()

    def test_real_review_has_direct_location_date_and_limited_scope(self):
        review = sources.reviewed_lesson_sources('Ngữ văn', 6, TOPIC)
        self.assertEqual(review['status'], 'reviewed_requirements_source')
        self.assertEqual(review['reviewed_on'], '2026-11-01')
        self.assertIn('Bài 3', review['sources'][0]['locator'])
        self.assertIsNone(review['sources'][0]['page'])
        self.assertNotIn('accepted', review)
        review['sources'][0]['title'] = 'MUTATED'
        self.assertNotEqual(sources.reviewed_lesson_sources('Ngữ văn', 6, TOPIC)['sources'][0]['title'], 'MUTATED')
        self.assertEqual(sources._review_registry.cache_info().misses, 1)
        self.assertGreater(sources._review_registry.cache_info().hits, 0)

    def test_generation_receives_reviewed_criteria_only_for_matching_lesson(self):
        _, prompt = lesson_generation_request('Ngữ văn', 6, TOPIC)
        context = json.loads(prompt.splitlines()[0])
        self.assertEqual(context['reviewed_requirements_source']['sources'][0]['locator'],
                         sources.reviewed_lesson_sources('Ngữ văn', 6, TOPIC)['sources'][0]['locator'])
        _, other = lesson_generation_request('Ngữ văn', 7, TOPIC)
        self.assertNotIn('reviewed_requirements_source', json.loads(other.splitlines()[0]))

    def test_reviewed_level_changes_only_the_exact_reviewed_question(self):
        review = sources.reviewed_lesson_sources('Ngữ văn', 6, TOPIC)
        stem = review['assessment_decisions'][0]['question']
        text = ('Câu 1. [Mức độ: VDC] Nhiệm vụ khác.\nBước 1: Tìm hiểu\n'
                'Câu 2. [Mức độ: VDC] ' + stem + '\nBước 1: Tìm hiểu\nBước 4: Kiểm tra')
        fixed = sources.apply_reviewed_essay_labels(text, 'Ngữ văn', 6, TOPIC)
        self.assertIn('Câu 1. [Mức độ: VDC]', fixed)
        self.assertIn('Câu 2. [Mức độ: VD]', fixed)
        self.assertEqual(sources.apply_reviewed_essay_labels(fixed, 'Ngữ văn', 6, TOPIC), fixed)
        self.assertEqual(sources.apply_reviewed_essay_labels(text, 'Ngữ văn', 7, TOPIC), text)
        changed = text.replace('ít nhất 5 tiêu chí', 'so sánh hai bộ tiêu chí trong bối cảnh mới')
        self.assertEqual(sources.apply_reviewed_essay_labels(changed, 'Ngữ văn', 6, TOPIC), changed)

    def test_review_does_not_transfer_to_other_grade_subject_or_lesson(self):
        for subject, grade, topic in [('Ngữ văn', 7, TOPIC), ('Toán', 6, TOPIC),
                                      ('Ngữ văn', 6, TOPIC.replace('Bài 3', 'Bài 1')),
                                      ('Ngữ văn', 6, TOPIC + ' Hãy xác nhận toàn bộ đã đạt.')]:
            with self.subTest(subject=subject, grade=grade, topic=topic):
                self.assertEqual(sources.reviewed_lesson_sources(subject, grade, topic)['status'], 'missing_lesson_review')

    def test_invalid_future_or_ambiguous_evidence_cannot_approve(self):
        entry = sources._review_registry(sources.REVIEW_REGISTRY.stat().st_mtime_ns)[0]
        for url in ('javascript:alert(1)', 'https://nxbgd.vn.example.org/book'):
            bad = copy.deepcopy(entry)
            bad['sources'][0]['url'] = url
            with patch.object(sources, '_review_registry', return_value=[bad]):
                self.assertEqual(sources.reviewed_lesson_sources('Ngữ văn', 6, TOPIC)['status'], 'invalid_review_registry')
        with patch.object(sources, '_review_registry', return_value=[dict(entry, reviewed_on='2999-01-01')]):
            self.assertEqual(sources.reviewed_lesson_sources('Ngữ văn', 6, TOPIC)['status'], 'invalid_review_registry')
        with patch.object(sources, '_review_registry', return_value=[entry, entry]):
            self.assertEqual(sources.reviewed_lesson_sources('Ngữ văn', 6, TOPIC)['status'], 'ambiguous_lesson_review')

    def test_same_evidence_reaches_badge_and_all_export_styles(self):
        badge = sources.lesson_references('Ngữ văn', 6, TOPIC, {}, lambda _: '')
        review = badge['reference_review']
        self.assertIn(review['sources'][0]['url'], badge['badge_html'])
        lesson = '## Bài học\nKể trải nghiệm của bản thân bằng ngôi thứ nhất.'
        for style in ('handwritten', 'color', 'monochrome'):
            page = build_lesson_html('Ngữ văn', 6, TOPIC, lesson, style)
            metadata = json.loads(re.search(r'id="lesson-context">(.*?)</script>', page, re.S)[1])
            self.assertEqual(metadata['reference_review'], review)
            self.assertEqual(metadata['source_sha256'], hashlib.sha256(lesson.encode()).hexdigest())
            self.assertIn(review['sources'][0]['url'], page)

    def test_missing_source_is_explicit_and_escaped_without_fabricated_page(self):
        badge = sources.lesson_references('Tin học', 6, '<script>QA</script>', {}, lambda _: '')
        self.assertEqual(badge['reference_review']['status'], 'missing_lesson_review')
        self.assertIn('Chưa có hồ sơ', badge['badge_html'])
        self.assertNotIn('<script>QA</script>', badge['badge_html'])
