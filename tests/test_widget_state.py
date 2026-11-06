import unittest

from services.widget_state import valid_option_index, switch_exam_request_context
from services.academic_context import subjects_for_grade


class TestScopedExamRequest(unittest.TestCase):
    def test_all_65_contexts_keep_their_own_draft_and_attempt_text_is_cleared(self):
        state = {"unrelated": "keep", "enable_ai_context_recovery": False}
        previous = "start"
        contexts = [(grade, subject) for grade in range(6, 13) for subject in subjects_for_grade(grade)]
        for current in contexts:
            switch_exam_request_context(state, previous, current)
            for key in ("custom_matrix_prompt", "area_custom_prompt_main", "area_custom_prompt_gv", "custom_request_text"):
                self.assertNotIn(key, state)
            for key in ("custom_matrix_prompt", "area_custom_prompt_main", "area_custom_prompt_gv"):
                state[key] = str(current) + key
            state["custom_request_text"] = "attempt text"
            previous = current
        switch_exam_request_context(state, previous, "end")
        previous = "end"
        for current in contexts:
            switch_exam_request_context(state, previous, current)
            for key in ("custom_matrix_prompt", "area_custom_prompt_main", "area_custom_prompt_gv"):
                self.assertEqual(state[key], str(current) + key)
            self.assertNotIn("custom_request_text", state)
            previous = current
        self.assertEqual(len(contexts), 65)
        self.assertEqual(state['unrelated'], 'keep')
        self.assertIs(state['enable_ai_context_recovery'], False)

    def test_station_change_and_initial_context_do_not_erase_request(self):
        for previous in (None, 'same'):
            state = {'custom_matrix_prompt': 'draft', 'custom_request_text': 'attempt'}
            switch_exam_request_context(state, previous, 'same')
            self.assertEqual(state, {'custom_matrix_prompt': 'draft', 'custom_request_text': 'attempt'})


class TestCachedExamSelection(unittest.TestCase):
    def test_preserves_valid_selection(self):
        self.assertEqual(valid_option_index(2, 4), 2)

    def test_resets_stale_labels_types_and_catalogue_bounds(self):
        for value in ('old exam label', '2', None, True, 1.5, [], {}, -1, 4):
            with self.subTest(value=value):
                self.assertEqual(valid_option_index(value, 4), 0)

    def test_catalogue_shrink_and_empty_catalogue(self):
        self.assertEqual(valid_option_index(3, 2), 0)
        self.assertEqual(valid_option_index(0, 0), 0)
