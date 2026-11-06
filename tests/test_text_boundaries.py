import ast
import re
import unittest
from pathlib import Path

from services.academic_context import subjects_for_grade
from services.curriculum_policy import lesson_prompt
from services.text_boundaries import preserve_math_and_code, student_essay_text


class TestLessonBoundaries(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = Path(__file__).resolve().parents[1].joinpath('app.py').read_text(encoding='utf-8')
        wanted = {'sanitize_katex_latex', '_legacy_sanitize_katex_latex',
                  'format_pedagogical_math', '_legacy_format_pedagogical_math'}
        nodes = [n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name in wanted]
        cls.functions = {'re': re}
        exec(compile(ast.Module(body=nodes, type_ignores=[]), 'math-boundaries', 'exec'), cls.functions)

    def test_math_meaning_and_display_survive_both_normalizers_all_contexts(self):
        examples = [r'$x$ $y$', r'$$\frac{1}{2}$$',
                    r'$x=A\cos(\omega t+\varphi)$; $R=2\,\Omega$',
                    r'$\ce{2H2 + O2 -> 2H2O}$',
                    '```python\nprint(r"\\omega")\n```']
        for grade in range(6, 13):
            for subject in subjects_for_grade(grade):
                for example in examples:
                    with self.subTest(subject=subject, grade=grade, example=example):
                        value = self.functions['sanitize_katex_latex'](example)
                        value = self.functions['format_pedagogical_math'](value)
                        self.assertEqual(value, example)

    def test_metadata_hidden_without_removing_polya_or_question(self):
        source = ('Câu 1. Nhiệm vụ học tập\nBước 1: Tìm hiểu đề\nEm biết gì?\n'
                  'COGNITIVE_STEPS: [\n "PRIVATE_REASONING",\n "OTHER_PRIVATE"\n]\n'
                  'OUTCOME: author metadata\nCOGNITIVE_REASON: author reason\n'
                  'Bước 4: Kiểm tra và nhìn lại\nEm tự đối chiếu thế nào?')
        result = student_essay_text(source)
        self.assertNotIn('PRIVATE', result)
        self.assertNotIn('author', result)
        self.assertIn('Câu 1.', result)
        self.assertIn('Bước 1:', result)
        self.assertIn('Bước 4:', result)
        self.assertIn('Em tự đối chiếu thế nào?', result)

    def test_native_delimiters_convert_without_changing_body_or_code(self):
        source = r'\(x\) và \[\frac{1}{2}\]' + '\n`\\(literal code\\)`'
        expected = r'$x$ và $$\frac{1}{2}$$' + '\n`\\(literal code\\)`'
        for name in ('sanitize_katex_latex', 'format_pedagogical_math'):
            self.assertEqual(self.functions[name](source), expected)

    def test_damaged_metadata_does_not_consume_next_exercise(self):
        value = student_essay_text('COGNITIVE_STEPS: [bad json\nCâu 2. Hãy tự làm.\nBước 1: Tìm hiểu đề')
        self.assertIn('Câu 2.', value)
        self.assertIn('Bước 1:', value)

    def test_live_bold_author_metadata_does_not_reach_student(self):
        for marker in ('**OUTCOME:**', '**OUTCOME**:', '__OUTCOME:__', '- **OUTCOME:**'):
            source = ('Câu 1. Viết bài văn.\n' + marker + ' PRIVATE_OUTCOME\n'
                      '**COGNITIVE_REASON:** PRIVATE_REASON\n'
                      '**COGNITIVE_STEPS:** [\n "PRIVATE_STEP"\n]\n'
                      'Bước 1: Tìm hiểu đề\nCâu 2. Tự đánh giá.')
            with self.subTest(marker=marker):
                value = student_essay_text(source)
                self.assertNotIn('PRIVATE', value)
                self.assertIn('Bước 1: Tìm hiểu đề', value)
                self.assertIn('Câu 2. Tự đánh giá.', value)

    def test_reserved_token_collision_keeps_user_text(self):
        source = 'GSAIPRESERVE literal $x$ $y$'
        self.assertEqual(preserve_math_and_code(source, lambda s: s), source)

    def test_prompt_restores_product_contract_without_numeric_requirement(self):
        for grade in range(6, 13):
            for subject in subjects_for_grade(grade):
                with self.subTest(subject=subject, grade=grade):
                    value = lesson_prompt(subject, grade, 'Chủ đề kiểm thử')
                    self.assertIn('đúng 3 câu trắc nghiệm', value)
                    self.assertIn('đúng 2 câu tự luận', value)
                    for step in range(1, 5):
                        self.assertIn(f'Bước {step}:', value)
                    self.assertIn('Không dùng EXPLAIN thay HINT', value)
                    self.assertIn('Phần 1 vẫn được giải thích lý thuyết', value)
