"""Bounded, content-free diagnostics for failed exam recovery."""
import json
import logging


_LOGGER = logging.getLogger("gsai.exam.recovery")
_SUBJECTS = {
    "Toán học", "Khoa học tự nhiên", "Ngữ văn", "Tiếng Anh",
    "Lịch sử & Địa lý", "Tin học", "Giáo dục công dân", "Công nghệ",
    "Vật lý", "Hóa học", "Sinh học", "Lịch sử", "Địa lý",
    "Giáo dục kinh tế và pháp luật",
}
_ACTIONS = {"needs_review", "recovered_from_formula", "recovered_from_inline_table", "bank_replacement", "ai_replacement"}
_REASONS = {
    "chemical_identity_mismatch", "missing_variation_table_limits", "graph_identification_formula_revealed",
    "invalid_question_structure", "missing_or_invalid_question_data",
    "missing_source_visual", "independently_detected_answer_mismatch",
    "outside_explicit_request", "outside_selected_topic",
}
_REPLACEMENT_REASONS = _REASONS | {
    "replacement_subject_mismatch", "replacement_grade_mismatch",
    "replacement_topic_mismatch", "replacement_visual_task_not_preserved",
    "replacement_level_mismatch", "replacement_response_error",
}


def _count(value):
    return min(value, 10000) if type(value) is int and value >= 0 else 0


def recovery_failure_summary(subject, grade, recovery):
    """Never serialize questions, answers, hashes, exception text or unknown fields."""
    data = recovery if isinstance(recovery, dict) else {}
    events = data.get("events", [])
    events = events if isinstance(events, list) else []
    safe = []
    for event in events[:32]:
        if not isinstance(event, dict):
            continue
        index = event.get("index")
        safe.append({
            "part": event.get("part") if event.get("part") in ("p1", "p2", "p3") else "unknown",
            "question": index + 1 if type(index) is int and 0 <= index < 10000 else None,
            "action": event.get("action") if event.get("action") in _ACTIONS else "unknown",
            "reason": event.get("reason") if event.get("reason") in _REASONS else "unknown",
        })
        if "replacement_rejection" in event:
            value = event["replacement_rejection"]
            safe[-1]["replacement_rejection"] = value if isinstance(value, str) and value in _REPLACEMENT_REASONS else "unknown"
        for key, allowed in (
            ("replacement_stage", {"provider", "decode", "envelope", "recover", "validate"}),
            ("replacement_error_type", {"ValueError", "TypeError", "KeyError", "AttributeError", "ImportError", "TimeoutError", "RuntimeError", "OtherError"}),
        ):
            if key in event:
                value = event[key]
                safe[-1][key] = value if isinstance(value, str) and value in allowed else "unknown"
    return {
        "subject": subject if isinstance(subject, str) and subject in _SUBJECTS else "unknown",
        "grade": grade if type(grade) is int and 6 <= grade <= 12 else None,
        "unresolved": _count(data.get("unresolved")),
        "ai_repair_calls": _count(data.get("ai_calls")),
        "events": safe,
        "events_truncated": len(events) > 32,
    }


def log_recovery_failure(subject, grade, recovery):
    """Diagnostics must not change the original publication decision or error."""
    try:
        summary = recovery_failure_summary(subject, grade, recovery)
        _LOGGER.warning("GSAI_RECOVERY_UNRESOLVED %s", json.dumps(summary, ensure_ascii=True))
    except Exception:
        # Logging is observational; a broken handler must not break exam recovery.
        pass
