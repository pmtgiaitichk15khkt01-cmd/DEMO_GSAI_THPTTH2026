"""Offline evidence-readiness audit, never an academic approval or output gate.

Evidence is a separate, locally maintained record. Fields emitted by a model
are claims, not independent validation. No network, retries or payload edits.
"""
from datetime import date
import hashlib
import json
from pathlib import Path
from copy import deepcopy

from services.academic_context import academic_context


DIMENSIONS = ("curriculum", "textbook", "legal", "scientific", "cognitive")
OUTCOME_REGISTRY = Path(__file__).resolve().parents[1] / "data/curriculum_outcome_overrides.json"


def outcome_reference(outcome_id, subject, grade, *, on_date):
    """Retrieve a scoped amendment by explicit ID, never a keyword ban.

    No match is unknown, not proof of compliance. A removed required outcome
    does not itself prove every question mentioning its terminology is invalid.
    The registry is read on explicit audit use only, not on app navigation.
    """
    subject, grade = academic_context(subject, grade)
    day = date.fromisoformat(on_date)
    registry = json.loads(OUTCOME_REGISTRY.read_text(encoding="utf-8"))
    if day < date.fromisoformat(registry["effective_from"]):
        return None
    for item in registry["items"]:
        if item["id"] == outcome_id and (item["subject"], item["grade"]) == (subject, grade):
            return {**deepcopy(item), "source_code": registry["source_code"],
                    "checked_at": registry["checked_at"],
                    "status": "reference_requires_question_review",
                    "textbook_alignment_verified": False, "academic_verified": False,
                    "blocks_delivery": False}
    return None


def content_fingerprint(payload):
    """Bind evidence to the complete submitted payload, including visuals/keys."""
    return hashlib.sha256(json.dumps(
        payload, ensure_ascii=False, sort_keys=True, allow_nan=False,
        separators=(",", ":"),
    ).encode("utf-8")).hexdigest()


def audit_evidence_readiness(payload, subject, grade, *, on_date, evidence=None):
    """Report missing/stale/conflicting evidence without rejecting lesson content.

    `on_date` is required: no hidden frozen policy date. Even complete metadata
    means ready for substantive review, not that the cited source is authentic,
    still legally applicable, or that the question is scientifically correct.
    """
    subject, grade = academic_context(subject, grade)
    day = date.fromisoformat(on_date)
    fingerprint = content_fingerprint(payload)
    record = evidence if isinstance(evidence, dict) else {}
    issues = []
    if record.get("content_sha256") != fingerprint:
        issues.append("missing_or_changed_content_binding")
    if record.get("subject") != subject or record.get("grade") != grade:
        issues.append("missing_or_conflicting_context")
    checks = {}
    for dimension in DIMENSIONS:
        row = record.get(dimension)
        missing = []
        if not isinstance(row, dict):
            row = {}
        for field in ("source_id", "source_version", "locator", "rationale", "reviewer"):
            if not isinstance(row.get(field), str) or not row[field].strip():
                missing.append(field)
        try:
            checked = date.fromisoformat(row.get("checked_at", ""))
            if checked > day:
                missing.append("checked_at_in_future")
        except (ValueError, TypeError):
            missing.append("checked_at")
        if dimension == "legal":
            # A validity interval alone does not establish legal applicability.
            for field in ("applicability", "amendment_review"):
                if not isinstance(row.get(field), str) or not row[field].strip():
                    missing.append(field)
            try:
                start = date.fromisoformat(row.get("effective_from", ""))
                end = row.get("effective_until")
                end = date.fromisoformat(end) if end else None
                if start > day or (end is not None and (day >= end or end <= start)):
                    missing.append("outside_recorded_validity")
            except (ValueError, TypeError):
                missing.append("validity_dates")
        checks[dimension] = {"metadata_complete": not missing, "missing": missing}
    ready = not issues and all(row["metadata_complete"] for row in checks.values())
    return {"subject": subject, "grade": grade, "on_date": day.isoformat(),
            "content_sha256": fingerprint, "issues": issues, "dimensions": checks,
            "status": "ready_for_source_review" if ready else "insufficient_evidence",
            "academic_verified": False, "blocks_delivery": False}
