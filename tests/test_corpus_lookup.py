import copy
import unittest

from services.academic_context import subjects_for_grade
from services.corpus_lookup import CorpusLookup, normalize_title


def book(subject, grade, lesson="Bài 1. Nội dung QA", chapter="Chương I. Chủ đề QA"):
    return {"subject": subject, "grade": grade, "book_title": "QA fixture, not a textbook",
            "book_url": "https://example.invalid/fixture",
            "chapters": [{"chapter_title": chapter, "lessons": [lesson]}]}


class TestCorpusLookup(unittest.TestCase):
    def test_every_supported_context_stays_scoped_without_certification(self):
        data = [book(subject, grade) for grade in range(6, 13) for subject in subjects_for_grade(grade)]
        before = copy.deepcopy(data)
        lookup = CorpusLookup(data)
        for station in (1, 3):
            for row in data:
                with self.subTest(station=station, subject=row["subject"], grade=row["grade"]):
                    result = lookup.lookup(row["grade"], row["subject"], "Bài 01: Nội dung QA", "Chương 1: Chủ đề QA")
                    self.assertEqual(result["status"], "exact_title_match")
                    self.assertEqual(result["candidates"][0]["subject"], row["subject"])
                    self.assertEqual(result["candidates"][0]["grade"], row["grade"])
                    self.assertFalse(result["academic_verified"])
                    self.assertFalse(result["blocks_delivery"])
        self.assertEqual(data, before)

    def test_geography_alias_cannot_become_physics_or_split_integrated_subject(self):
        lookup = CorpusLookup([book("Địa lí", 12), book("Lịch sử và Địa lí", 6)])
        self.assertEqual(lookup.lookup(12, "Địa lý", "Bài 1. Nội dung QA")["subject"], "Địa lý")
        self.assertEqual(lookup.lookup(6, "Lịch sử & Địa lý", "Bài 1. Nội dung QA")["subject"], "Lịch sử & Địa lý")
        self.assertEqual(lookup.lookup(12, "Vật lí", "Bài 1. Nội dung QA")["status"], "corpus_not_available")

    def test_fuzzy_result_is_only_a_suggestion_and_never_rewrites_input(self):
        lookup = CorpusLookup([book("Toán", 6, "Bài 1. Tập hợp")])
        query = "Bài 99. Tích phân lượng giác"
        result = lookup.lookup(6, "Toán", query)
        self.assertEqual(result["status"], "suggestions_only")
        self.assertNotIn("is_valid", result)
        self.assertFalse(result["academic_verified"])

    def test_duplicate_titles_require_book_disambiguation(self):
        lookup = CorpusLookup([book("Toán", 6), book("Toán", 6)])
        self.assertEqual(lookup.lookup(6, "Toán", "Bài 1. Nội dung QA")["status"], "ambiguous_title_match")

    def test_bad_or_empty_records_do_not_erase_good_context(self):
        lookup = CorpusLookup([{}, None, book("Toán", 6)])
        self.assertEqual(lookup.skipped_records, 2)
        self.assertEqual(lookup.lookup(6, "Toán", "")["status"], "missing_query")
        for limit in (0, -1, True, 21):
            with self.assertRaises(ValueError):
                lookup.lookup(6, "Toán", "QA", limit=limit)

    def test_numbers_and_accents_are_not_deleted_to_force_an_exact_match(self):
        self.assertNotEqual(normalize_title("Bài 1. Tập hợp"), normalize_title("Bài 2. Tập hợp"))
        self.assertNotEqual(normalize_title("Tập hợp"), normalize_title("Tap hop"))

    def test_results_cannot_mutate_shared_index(self):
        lookup = CorpusLookup([book("Anh", 6, "Lesson 1. Getting started", "Unit IV. Home")])
        first = lookup.lookup(6, "Tiếng Anh", "Lesson 1. Getting started", "Unit 4. Home")
        first["candidates"][0]["lesson"] = "changed"
        self.assertNotEqual(lookup.lookup(6, "Anh", "Lesson 1. Getting started")["candidates"][0]["lesson"], "changed")
