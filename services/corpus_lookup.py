"""Scoped catalogue lookup adapted from the user's corpus-validator approach.

Matching titles is navigation evidence, never an academic or legal approval.
Build once per corpus version; lookup does not perform I/O or call an AI.
"""
from copy import deepcopy
from difflib import SequenceMatcher
import re
import unicodedata

from services.academic_context import academic_context


_ROMAN = {value: str(i) for i, value in enumerate(
    ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV"), 1)}


def normalize_title(value):
    text = unicodedata.normalize("NFC", str(value or "")).strip()
    text = re.sub(r"\b(chương|chủ đề|phần|unit)\s+([IVX]+)\b",
                  lambda m: m[1] + " " + _ROMAN.get(m[2].upper(), m[2]), text, flags=re.I)
    text = re.sub(r"\b(chương|chủ đề|phần|bài|tiết|unit|lesson)\s+0+(\d+)\b",
                  r"\1 \2", text, flags=re.I)
    # Preserve accents and item numbers: similar spelling is not an exact match.
    return " ".join(re.sub(r"[^\w\s]", " ", text.casefold()).split())


class CorpusLookup:
    def __init__(self, records):
        self._index = {}
        self.skipped_records = 0
        for book in records:
            if not isinstance(book, dict):
                self.skipped_records += 1
                continue
            try:
                context = academic_context(book.get("subject"), book.get("grade"))
            except ValueError:
                self.skipped_records += 1
                continue
            chapters = book.get("chapters")
            if not isinstance(chapters, list):
                self.skipped_records += 1
                continue
            for chapter in chapters:
                if not isinstance(chapter, dict) or not isinstance(chapter.get("lessons"), list):
                    continue
                for lesson in chapter["lessons"]:
                    if not isinstance(lesson, str) or not lesson.strip():
                        continue
                    row = {key: book.get(key, "") for key in
                           ("book_title", "book_url", "edition", "source_version", "checked_at")}
                    row.update(subject=context[0], grade=context[1],
                               chapter=chapter.get("chapter_title", ""), lesson=lesson)
                    self._index.setdefault(context, []).append(row)

    def lookup(self, grade, subject, lesson, chapter="", *, limit=3):
        context = academic_context(subject, grade)
        if type(limit) is not int or not 1 <= limit <= 20:
            raise ValueError("Candidate limit must be an integer from 1 to 20.")
        query, section = normalize_title(lesson), normalize_title(chapter)
        rows = self._index.get(context, [])
        base = {"subject": context[0], "grade": context[1], "academic_verified": False,
                "blocks_delivery": False, "candidates": []}
        if not query:
            return {**base, "status": "missing_query"}
        if not rows:
            return {**base, "status": "corpus_not_available"}
        exact, ranked = [], []
        for row in rows:
            title, heading = normalize_title(row["lesson"]), normalize_title(row["chapter"])
            score = SequenceMatcher(None, query, title).ratio()
            if section:
                score = min(score, SequenceMatcher(None, section, heading).ratio())
            if title == query and (not section or heading == section):
                exact.append(row)
            ranked.append((score, row))
        if exact:
            return {**base, "status": "exact_title_match" if len(exact) == 1 else "ambiguous_title_match",
                    "candidates": deepcopy(exact[:limit]), "match_count": len(exact)}
        ranked.sort(key=lambda item: item[0], reverse=True)
        return {**base, "status": "suggestions_only", "candidates": [
            {**deepcopy(row), "title_similarity": round(score, 4)} for score, row in ranked[:limit]]}
