"""Stream source level claims. This inventories evidence, not semantic correctness."""
import argparse
from collections import Counter
import json
import lzma
from pathlib import Path
import sys

import ijson

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from services.cognitive_levels import normalize_level
from services.curriculum_policy import question_groups


def audit():
    question_claims, statement_claims, counts = Counter(), Counter(), Counter()
    files = []
    for path in sorted((ROOT / "data/real_exam_bank").glob("exams_*.json.xz")):
        records = 0
        with lzma.open(path, "rb") as stream:
            for exam in ijson.items(stream, "exams.item", use_float=True):
                records += 1
                counts["exam_records"] += 1
                for part, questions in question_groups(exam):
                    for q in questions:
                        if not isinstance(q, dict):
                            continue
                        counts["question_instances"] += 1
                        raw = str(q.get("level") or "MISSING")
                        question_claims[(part, raw)] += 1
                        if not normalize_level(q.get("level")):
                            counts["question_missing_or_ambiguous_level"] += 1
                        if not (q.get("learning_outcome") and q.get("cognitive_rationale") and q.get("solution_steps")):
                            counts["question_missing_stated_cognitive_evidence"] += 1
                        if not q.get("teacher_cognitive_review"):
                            counts["question_without_teacher_review_metadata"] += 1
                        for stmt in q.get("stmts", []):
                            if isinstance(stmt, dict):
                                counts["tf_statement_instances"] += 1
                                statement_claims[str(stmt.get("level") or "MISSING")] += 1
                                if not normalize_level(stmt.get("level")):
                                    counts["tf_statement_missing_or_ambiguous_level"] += 1
        files.append({"file": path.name, "exam_records": records})
    return {"method": "All shard records streamed; counts are instances, not unique items. No semantic or psychometric certification.",
            "counts": dict(counts), "files": files,
            "question_claims": [{"part": p, "claim": level, "instances": n} for (p, level), n in sorted(question_claims.items())],
            "statement_claims": dict(statement_claims)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result["counts"], ensure_ascii=True))
