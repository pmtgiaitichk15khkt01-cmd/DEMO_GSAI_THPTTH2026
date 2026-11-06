"""Small, deterministic guards for persisted Streamlit widget state."""


def switch_exam_request_context(state, previous, current):
    """Keep each subject/grade's draft, without carrying it into another one.

    Run before rendering the request widgets, as part of the existing context
    switch. Exam-specific request text belongs to the old attempt, not a draft.
    """
    if previous is None or previous == current:
        return
    keys = ("custom_matrix_prompt", "area_custom_prompt_main", "area_custom_prompt_gv")
    drafts = state.setdefault("exam_request_drafts", {})
    drafts[previous] = {key: state[key] for key in keys if key in state}
    for key in (*keys, "custom_request_text"):
        state.pop(key, None)
    for key, value in drafts.get(current, {}).items():
        if key in keys:
            state[key] = value


def valid_option_index(value, option_count):
    """Keep a real in-range index; reset stale labels/types to the first option.

    A label or numeric string is not an index: coercing it can silently select
    another exam after the subject/grade catalogue has changed.
    """
    if type(value) is int and 0 <= value < option_count:
        return value
    return 0
