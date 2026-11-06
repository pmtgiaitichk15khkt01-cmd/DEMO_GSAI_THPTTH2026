"""Safe archive labels independent of long-lived widget-state imports."""

def cached_exam_label(item):
    """Render heterogeneous archive metadata for every subject/grade."""
    from datetime import date, datetime
    row = item if isinstance(item, dict) else {}
    def text(value, fallback):
        if isinstance(value, (str, int, float)) and not isinstance(value, bool):
            return str(value).strip() or fallback
        return fallback
    stamp = row.get('saved_at')
    if isinstance(stamp, (date, datetime)):
        stamp = stamp.isoformat()
    stamp = text(stamp, '')[:10]
    return f"Mã đề {text(row.get('code'), 'Chưa rõ')} - {text(row.get('topic'), 'Chuyên đề ôn tập')} ({stamp})"


def distinct_exam_labels(labels, exams):
    """Keep same-code variants distinguishable without renumbering source codes."""
    from collections import Counter
    from services.bank_storage import exam_storage_identity
    counts = Counter(labels)
    return [label if counts[label] == 1 else label + ' • Bản ' + exam_storage_identity(exam)[:10]
            for label, exam in zip(labels, exams)]
