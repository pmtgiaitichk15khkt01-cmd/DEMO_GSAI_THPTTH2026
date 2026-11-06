import unittest
from services.text_boundaries import option_markdown_label
from services.academic_context import subjects_for_grade
from qa_runtime import mcq_answer_matches


class TestOptionMarkdownLabel(unittest.TestCase):
    def test_observed_interval_and_existing_math_are_rendered_once(self):
        self.assertEqual(option_markdown_label(r'D. (0; +\infty)'), r'D. $(0; +\infty)$')
        self.assertEqual(option_markdown_label(r'A. $(-\infty;0)$'), r'A. $(-\infty;0)$')
        value = r'B. (-\infty;0) và (2;+\infty)'
        self.assertEqual(option_markdown_label(value), r'B. $(-\infty;0)$ và $(2;+\infty)$')
        self.assertEqual(option_markdown_label(option_markdown_label(value)), option_markdown_label(value))

    def test_nonmath_and_code_are_preserved_across_subject_grade_contexts(self):
        values = ['A. English sentence.', 'B. Địa lí Việt Nam', 'C. (0; 2)',
                  r'D. `print("(0; +\infty)")`', 'A. $x$ $y$']
        for grade in range(6,13):
            for subject in subjects_for_grade(grade):
                for value in values:
                    with self.subTest(grade=grade,subject=subject,value=value):
                        self.assertEqual(option_markdown_label(value),value)

    def test_display_does_not_rewrite_raw_option_or_scoring_identity(self):
        options = [r'A. (0;+\infty)', 'B. 0', 'C. 1', 'D. 2']
        before = list(options)
        labels = [option_markdown_label(value) for value in options]
        self.assertNotEqual(labels[0], options[0])
        self.assertEqual(options,before)
        self.assertTrue(mcq_answer_matches({'opt':options,'ans':'A'}, options[0]))
