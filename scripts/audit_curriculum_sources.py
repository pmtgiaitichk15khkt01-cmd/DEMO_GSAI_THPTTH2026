"""Offline inventory of every shard record; metadata is not academic validation."""
import argparse
from collections import Counter
import hashlib
import json
import lzma
from pathlib import Path
import re
import sys

import ijson

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from data.curriculum_data import BIGDATA_CURRICULUM
from kntt_sgk_library import KNTT_DIGITAL_LIBRARY
from services.academic_context import academic_context, canonical_subject, subjects_for_grade
from services.curriculum_policy import POLICY_DATE, check_current_facts, question_groups


def audit():
    counts, contexts, samples = Counter(), Counter(), []
    signatures = set()
    files = []
    for path in sorted((ROOT / "data/real_exam_bank").glob("exams_*.json.xz")):
        record_count = 0
        with lzma.open(path, "rb") as stream:
            for exam in ijson.items(stream, "exams.item", use_float=True):
                record_count += 1
                counts["exam_records"] += 1
                subject, grade = canonical_subject(exam.get("subject")), exam.get("grade")
                try:
                    subject, grade = academic_context(subject, grade)
                    contexts[(subject, grade)] += 1
                except ValueError:
                    counts["invalid_exam_context"] += 1
                if not any(re.match(r"https?://", str(exam.get(k, ""))) for k in ("url", "source_url", "original_url")):
                    counts["exam_without_declared_http_source_url"] += 1
                if not exam.get("curriculum_evidence"):
                    counts["exam_without_curriculum_outcome_evidence"] += 1
                if not exam.get("textbook_evidence"):
                    counts["exam_without_textbook_page_or_revision_evidence"] += 1
                for part, questions in question_groups(exam):
                    for question in questions:
                        counts["question_instances"] += 1
                        if not isinstance(question, dict):
                            counts["invalid_question_structure"] += 1
                            continue
                        text = str(question.get("q", ""))
                        signatures.add(hashlib.sha256(text.strip().encode()).digest()[:16])
                        if not question.get("topic"):
                            counts["question_without_topic"] += 1
                        if not question.get("source_url"):
                            counts["question_without_direct_source_url"] += 1
                        if "63" in text or "64" in text:
                            try:
                                check_current_facts(text)
                            except ValueError:
                                counts["stale_current_geography_claims"] += 1
                                if len(samples) < 8:
                                    samples.append({"file": path.name, "code": exam.get("code"), "part": part, "q": text[:250]})
        files.append({"file": path.name, "records": record_count})
    counts["distinct_question_texts"] = len(signatures)
    rows = [{"subject": subject, "grade": grade, "bank_records": contexts[(subject, grade)],
             "editorial_topic_suggestions": len(BIGDATA_CURRICULUM.get(subject, {}).get(grade, []))}
            for grade in range(6, 13) for subject in subjects_for_grade(grade)]
    books = [book for subjects in KNTT_DIGITAL_LIBRARY.values() for values in subjects.values() for book in values]
    return {"checked_at": POLICY_DATE, "method": "Stream all exam records in every compressed subject shard; inspect metadata and narrow current-fact conflicts. No claim of checking every academic answer.",
            "counts": dict(counts), "files": files, "contexts": rows,
            "missing_contexts": [row for row in rows if not row["bank_records"]],
            "book_navigation_entries": len(books), "book_navigation_unique_urls": len({b["url"] for b in books}),
            "curriculum_topic_status": "editorial_suggestions_not_verified_textbook_table_of_contents",
            "stale_claim_samples": samples}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = audit()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"counts": report["counts"], "shards": len(report["files"]), "contexts": len(report["contexts"])}, ensure_ascii=True))
