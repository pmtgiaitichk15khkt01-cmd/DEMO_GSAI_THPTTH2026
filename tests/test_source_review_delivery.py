import unittest
from copy import deepcopy
from unittest.mock import patch
import real_exam_engine as engine


class SourceReviewDeliveryTests(unittest.TestCase):
    def test_explicit_question_hold_blocks_delivery_without_mutating_archive(self):
        original = {'q': 'A source question', 'source_review_issues': ['missing premise']}
        saved = deepcopy(original)
        self.assertTrue(engine.is_toxic_defective_question(original))
        self.assertEqual(original, saved)
        self.assertFalse(engine.has_unresolved_source_review({'q': 'Unflagged'}))

    def test_original_paper_is_held_not_silently_shortened(self):
        held = {'subject': 'Tin học', 'grade': 12, 'code': 'held',
                'p1': [{'q': 'Q1'}, {'q': 'Q2', 'source_review_issues': ['missing premise']}],
                'p2': [], 'p3': []}
        good = {'subject': 'Tin học', 'grade': 12, 'code': 'good',
                'p1': [{'q': 'Q1'}], 'p2': [], 'p3': []}
        saved = deepcopy(held)
        with patch.object(engine, 'get_shard_exams', return_value=[held, good]), \
             patch.object(engine, 'load_teacher_uploaded_exams', return_value=[]), \
             patch.object(engine, 'BASE_DIR', '__no_source_delivery_fixture__'), \
             patch.object(engine, '_FAST_EXAM_LIST_CACHE', {}, create=True):
            for enriched in (False, True):
                # Hold detection must run before visual enrichment can remove Q2.
                rows = engine.get_baseline_full_exams('Tin học', 12, enrich_visuals=enriched)
                self.assertEqual([r['code'] for r in rows], ['good'])
        self.assertEqual(held, saved)

    def test_individual_pool_keeps_valid_items_and_original_positions(self):
        held = {'subject': 'Tin học', 'grade': 12, 'code': 'held',
                'p1': [{'q': 'First'}, {'q': 'Held', 'source_review_issues': ['missing premise']},
                       {'q': 'Third'}], 'p2': [], 'p3': []}
        with patch.object(engine, 'get_shard_exams', return_value=[held]), \
             patch.object(engine, 'load_teacher_uploaded_exams', return_value=[]), \
             patch.object(engine, 'BASE_DIR', '__no_source_delivery_fixture__'), \
             patch.object(engine, '_FAST_EXAM_LIST_CACHE', {}, create=True), \
             patch.object(engine, '_QUESTIONS_POOL_CACHE', {}):
            self.assertEqual(engine.get_baseline_full_exams('Tin học', 12), [])
            pool = engine.get_baseline_questions_pool('Tin học', 12)
            self.assertEqual([q['q'] for q in pool['p1']], ['First', 'Third'])
            self.assertTrue(pool['p1'][1]['orig_pos'].endswith('3'))
            self.assertEqual(engine.get_baseline_full_exams('Tin học', 12), [])

    def test_atomic_import_repeated_and_conflicting_identity(self):
        import tempfile
        from pathlib import Path
        from services.bank_storage import append_exam_atomic, iter_exam_shard
        exam = {'subject': 'Tin học', 'grade': 12, 'year': 2026, 'code': '0525',
                'school': 'Issuer', 'exam_type': 'official', 'p1': [{'q': 'Original'}]}
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'exam.json.xz'
            self.assertTrue(append_exam_atomic(path, exam))
            original = path.read_bytes()
            self.assertFalse(append_exam_atomic(path, dict(exam, added_at='later')))
            with self.assertRaises(ValueError):
                append_exam_atomic(path, dict(exam, p1=[{'q': 'Changed'}]))
            self.assertEqual(path.read_bytes(), original)
            self.assertEqual(len(list(iter_exam_shard(path))), 1)

    def test_failed_replace_preserves_shard_and_removes_temporary(self):
        import tempfile
        from pathlib import Path
        from services.bank_storage import append_exam_atomic
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'exam.json.xz'
            first = {'code': '1', 'p1': []}
            append_exam_atomic(path, first)
            saved = path.read_bytes()
            with patch('os.replace', side_effect=OSError('simulated write failure')):
                with self.assertRaises(OSError):
                    append_exam_atomic(path, {'code': '2', 'p1': []})
            self.assertEqual(path.read_bytes(), saved)
            self.assertEqual(list(Path(folder).iterdir()), [path])

    def test_committed_import_clears_derived_views(self):
        from contextlib import ExitStack
        names = ('_SHARD_CACHE', '_FAST_EXAM_LIST_CACHE', '_QUESTIONS_POOL_CACHE',
                 '_MULTI_INDEX_BY_TOPIC_LEVEL', '_MULTI_INDEX_BY_TOPIC',
                 '_MULTI_INDEX_BY_PART', '_QUESTION_STORE_BY_QID', '_INDEXED_SUBJECTS')
        caches = {name: {'stale': True} for name in names}
        with ExitStack() as stack:
            for name, cache in caches.items():
                stack.enter_context(patch.object(engine, name, cache, create=True))
            writer = stack.enter_context(patch('services.bank_storage.append_exam_atomic', return_value=True))
            self.assertTrue(engine.append_exam_to_national_shard(
                {'subject': 'Tin học', 'grade': 12, 'p1': [], 'p2': [], 'p3': []}))
            writer.assert_called_once()
            self.assertTrue(all(not cache for cache in caches.values()))
