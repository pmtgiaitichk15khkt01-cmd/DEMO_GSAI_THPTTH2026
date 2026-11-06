import gzip
import json
import lzma
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from services.bank_storage import BoundedCache, read_exam_shard, content_identity, mark_ai_exam_provenance, calibration_eligibility


class TestBankMemory(unittest.TestCase):
    def test_actual_calibration_pool_fails_closed_without_independent_registry(self):
        import real_exam_engine as engine
        pool = {'p1':[{'q':'Q', 'is_real_bank_question':True,
                      'source_verification':'verified', 'reference_review':{'approved':True}}], 'p2':[], 'p3':[]}
        with patch.object(engine, 'get_baseline_questions_pool', return_value=pool), \
             tempfile.TemporaryDirectory() as directory, patch.object(engine, 'BASE_DIR', directory):
            result = engine.get_verified_calibration_questions_pool('Toán học', 10)
            self.assertFalse(result['p1'])
            self.assertEqual(result['audit']['excluded'], 1)
            self.assertEqual(result['audit']['status'], 'no_verified_anchors')

    def test_adn_school_or_self_declared_real_does_not_approve_reference(self):
        q = {'qid':'ADN-cua-kho-cu', 'q':'Q', 'school':'Trường nổi tiếng', 'is_real_bank_question':True,
             'source_verification':'verified'}
        context = dict(subject='Toán học', grade=10, part='p1')
        result = calibration_eligibility(q, None, **context)
        self.assertFalse(result['eligible'])
        review = {**context, 'content_adn':result['content_adn'],
            **{k:'reviewed-fixture' for k in ('paper_source_url','paper_sha256','answer_source_url','answer_sha256',
                 'source_locator','reviewer','reviewed_on','curriculum_outcome_locator')},
            'original_item_match':'passed','answer_check':'passed','curriculum_mapping':'passed'}
        self.assertTrue(calibration_eligibility(q, review, **context)['eligible'])
        self.assertFalse(calibration_eligibility(dict(q,q='changed'), review, **context)['eligible'])
        self.assertFalse(calibration_eligibility(dict(q,is_ai_generated=True), review, **context)['eligible'])
    def test_actual_question_pool_retains_ai_origin_and_does_not_invent_issuer(self):
        import real_exam_engine as engine
        exams = [{'code':'AI', 'subject':'Toán học', 'grade':10, 'is_ai_harvested':True,
                  'p1':[{'q':'Câu thử', 'opt':['1','2','3','4'], 'ans':'A'}]}]
        with patch.object(engine, 'get_baseline_full_exams', return_value=exams), \
             patch.object(engine, '_QUESTIONS_POOL_CACHE', BoundedCache(4)), \
             patch.object(engine, 'is_toxic_defective_question', return_value=False), \
             patch.object(engine, 'attach_question_visuals', side_effect=lambda q, **kw:q):
            pool = engine.get_baseline_questions_pool('Toán học', 10)
            self.assertTrue(pool['p1'][0]['is_ai_generated'])
            self.assertFalse(pool['p1'][0]['is_real_bank_question'])
            self.assertEqual(pool['p1'][0]['source_verification'], 'not_official_exam')
            self.assertIn('Chưa xác minh', pool['p1'][0]['school'])

    def test_generated_exam_cannot_keep_claimed_official_flags(self):
        source = {'is_real_bank_question':True, 'p1':[{'q':'Q', 'is_ai_generated':False, 'is_real_bank_question':True}]}
        marked = mark_ai_exam_provenance(source)
        self.assertFalse(marked['is_real_bank_question'])
        self.assertTrue(marked['p1'][0]['is_ai_generated'])
        self.assertEqual(marked['source_verification'], 'not_official_exam')
        self.assertTrue(source['is_real_bank_question'])
    def test_grade_filter_keeps_only_requested_grade_without_changing_all_api(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'bank.json.xz'
            exams = [{'code':str(i), 'grade':i, 'p1':[{'q':'x^2'}]} for i in (6, 9, 12)]
            with lzma.open(path, 'wt', encoding='utf-8') as stream:
                json.dump({'exams': exams}, stream)
            self.assertEqual(read_exam_shard(path, grade='9'), [exams[1]])
            self.assertEqual(read_exam_shard(path), exams)
            self.assertEqual(read_exam_shard(path, grade=10), [])
    def test_actual_multi_index_does_not_overwrite_colliding_legacy_qids(self):
        import real_exam_engine as engine
        exam = {'subject': 'Toán học', 'grade': 10, 'p1': [
            {'qid': 'same-old-id', 'q': 'x^2', 'ans': 'A'},
            {'qid': 'same-old-id', 'q': 'x2', 'ans': 'B'}]}
        with patch.object(engine, 'get_shard_exams', return_value=[exam]), \
             patch.object(engine, '_MULTI_INDEX_BY_TOPIC_LEVEL', {}), \
             patch.object(engine, '_MULTI_INDEX_BY_TOPIC', {}), \
             patch.object(engine, '_MULTI_INDEX_BY_PART', {}), \
             patch.object(engine, '_QUESTION_STORE_BY_QID', {}), \
             patch.object(engine, '_INDEXED_SUBJECTS', set()):
            engine.build_multi_dimensional_index('Toán học', force=True)
            self.assertEqual(len(engine._QUESTION_STORE_BY_QID), 2)
            self.assertEqual({q['q'] for q in engine._QUESTION_STORE_BY_QID.values()}, {'x^2', 'x2'})
            self.assertEqual(exam['p1'][0]['qid'], 'same-old-id')
    def test_content_adn_replaces_colliding_random_ids_without_losing_alias(self):
        first = {'qid': 'NAT_RANDOM_123', 'q': 'x^2', 'ans': 'A'}
        second = dict(first, q='x2')
        context = dict(subject='Toán học', grade=10, part='p1')
        a, b = content_identity(first, **context), content_identity(second, **context)
        self.assertNotEqual(a['qid'], b['qid'])
        self.assertEqual(a['legacy_qids'], ['NAT_RANDOM_123'])
        self.assertEqual(content_identity(a, **context), a)
        self.assertEqual(first['qid'], 'NAT_RANDOM_123')
        self.assertNotEqual(content_identity(first, **dict(context, grade=11))['qid'], a['qid'])
        self.assertNotEqual(content_identity(first, **context, shared_context={'text':'other'})['qid'], a['qid'])
    def test_all_formats_keep_exact_content_and_mutation_isolation(self):
        sample = [{"code": str(i), "p1": [{"q": "Một chuỗi câu hỏi lặp lại", "opt": ["cùng đáp án", "khác"], "ans": "A"}]} for i in range(3)]
        with tempfile.TemporaryDirectory() as directory:
            for suffix, opener in ((".json", open), (".json.gz", gzip.open), (".json.xz", lzma.open)):
                for root in (sample, {"exams": sample}):
                    path = Path(directory) / ("bank" + suffix)
                    with opener(path, "wt", encoding="utf-8") as stream:
                        json.dump(root, stream, ensure_ascii=False)
                    actual = read_exam_shard(path)
                    self.assertEqual(actual, sample)
                    self.assertIs(actual[0]["p1"][0]["q"], actual[1]["p1"][0]["q"])
                    actual[0]["p1"][0]["opt"][0] = "changed"
                    self.assertEqual(actual[1]["p1"][0]["opt"][0], "cùng đáp án")

    def test_lru_evicts_least_recently_used(self):
        cache = BoundedCache(2)
        cache["one"] = 1
        cache["two"] = 2
        self.assertEqual(cache.get("one"), 1)
        cache["three"] = 3
        self.assertEqual(set(cache), {"one", "three"})

    def test_explicit_removal_preserves_order_and_empty_behavior(self):
        cache = BoundedCache(3)
        for key in ("one", "two", "three"):
            cache[key] = key.upper()
        self.assertEqual(cache.popitem(last=False), ("one", "ONE"))
        self.assertEqual(cache.popitem(), ("three", "THREE"))
        self.assertEqual(cache.popitem(), ("two", "TWO"))
        with self.assertRaises(KeyError):
            cache.popitem()

    def test_scanned_exam_remix_missing_helper_regression(self):
        import real_exam_engine as engine
        exam = {"code": "qa", "p1": [{"q": "Câu hỏi chữ", "opt": ["A. 1", "B. 2"], "ans": "A"}], "p2": [], "p3": []}
        enriched = engine.enrich_exam_visuals_jit(exam, "Lịch sử", 12)
        self.assertEqual(exam["p1"][0]["ans"], enriched["p1"][0]["ans"])
        enriched["p1"][0]["opt"][0] = "changed"
        self.assertEqual(exam["p1"][0]["opt"][0], "A. 1")

    def test_third_subject_releases_derived_caches(self):
        import real_exam_engine as engine
        with patch.object(engine, "_SHARD_CACHE", BoundedCache(2)), \
             patch.object(engine, "_QUESTIONS_POOL_CACHE", BoundedCache(4)), \
             patch.object(engine, "_FAST_EXAM_LIST_CACHE", BoundedCache(8), create=True), \
             patch.object(engine, "_MULTI_INDEX_BY_TOPIC_LEVEL", {}), \
             patch.object(engine, "_MULTI_INDEX_BY_TOPIC", {}), \
             patch.object(engine, "_MULTI_INDEX_BY_PART", {}), \
             patch.object(engine, "_QUESTION_STORE_BY_QID", {}), \
             patch.object(engine, "_INDEXED_SUBJECTS", set()), \
             patch.object(engine, "get_raw_baseline_data", return_value={}), \
             patch.object(engine.os.path, "exists", return_value=False):
            engine.get_shard_exams("qa-one")
            engine.get_shard_exams("qa-two")
            engine._QUESTIONS_POOL_CACHE["old"] = ["stale"]
            engine._MULTI_INDEX_BY_PART["old"] = ["stale"]
            engine.get_shard_exams("qa-three")
            self.assertEqual(len(engine._SHARD_CACHE), 2)
            self.assertFalse(engine._QUESTIONS_POOL_CACHE)
            self.assertFalse(engine._MULTI_INDEX_BY_PART)
