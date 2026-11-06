"""Speaking branch: all seven grades and the guard for all 65 contexts."""
import ast
import json
from pathlib import Path
import unittest
from unittest.mock import MagicMock

from streamlit.testing.v1 import AppTest
from services.academic_context import subjects_for_grade
from services.english_speaking import speaking_units_for_grade, speaking_feedback_prompt


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / 'app.py').read_text(encoding='utf-8')
FUNCTION = next(n for n in ast.parse(SOURCE).body if isinstance(n, ast.FunctionDef)
                and n.name == 'render_voice_speech_tex_and_english_evaluator')
FUNCTION_SOURCE = ast.get_source_segment(SOURCE, FUNCTION)


class TestEnglishSpeakingContext(unittest.TestCase):
    def test_grade_examples_are_complete_without_mutating_existing_grade12_bank(self):
        advanced = {'Unit 1: Life stories': {'vocab': [{'word': 'test'}], 'passage': 'Example', 'q_reflex': 'Question?'}}
        for grade in range(6, 13):
            units = speaking_units_for_grade(grade, advanced)
            self.assertTrue(units)
            for title, data in units.items():
                self.assertIn(f'lớp {grade}', title)
                self.assertNotIn('Unit 1:', title)
                self.assertTrue(data['vocab'])
                self.assertTrue(data['passage'])
                self.assertTrue(data['q_reflex'].endswith('?'))
            if grade < 12:
                self.assertNotIn('Life stories', ' '.join(units))
        result = speaking_units_for_grade(12, advanced)
        next(iter(result.values()))['vocab'][0]['word'] = 'changed'
        self.assertEqual(advanced['Unit 1: Life stories']['vocab'][0]['word'], 'test')

    def test_all_65_contexts_keep_speaking_exclusive_to_english_station1(self):
        for grade in range(6, 13):
            for subject in subjects_for_grade(grade):
                if subject == 'Tiếng Anh':
                    continue
                with self.subTest(subject=subject, grade=grade):
                    mocked_st = MagicMock()
                    scope = {'st': mocked_st}
                    exec(compile(ast.Module(body=[FUNCTION], type_ignores=[]), 'speaking-context', 'exec'), scope)
                    scope[FUNCTION.name]('Tram 1', subject, grade)
                    self.assertEqual(mocked_st.mock_calls, [])

    def test_text_feedback_never_claims_to_have_heard_audio_in_any_grade(self):
        for grade in range(6, 13):
            for audio in (False, True):
                prompt = speaking_feedback_prompt(grade, 'QA topic', 'QA example', 'QA question?', audio)
                self.assertIn(f'Tiếng Anh lớp {grade}', prompt)
                self.assertIn('không quy đổi điểm thành IELTS/CEFR', prompt)
                self.assertIn('Có tệp âm thanh' if audio else 'không chấm phát âm', prompt)
                self.assertIn('bốn nhóm nhận xét', prompt)
                self.assertIn('mẫu diễn đạt tham khảo ngắn', prompt)

    def test_real_speaking_ui_switches_all_grades_and_keeps_recording_and_text(self):
        script = '''import streamlit as st
import json
def create_pedagogical_tts_component(*args): pass
def call_gemini_with_fallback(contents):
    st.session_state['captured_feedback_prompt'] = contents[-1]
    return 'Phản hồi QA mô phỏng.'
''' + FUNCTION_SOURCE + '''
grade = st.selectbox('Khối kiểm thử', list(range(6,13)))
render_voice_speech_tex_and_english_evaluator('Tram 1', 'Tiếng Anh', grade)
'''
        at = AppTest.from_string(script, default_timeout=15).run()
        for grade in range(6, 13):
            with self.subTest(grade=grade):
                next(s for s in at.selectbox if s.label == 'Khối kiểm thử').select(grade).run()
                self.assertEqual([e.message for e in at.exception], [])
                units = next(s for s in at.selectbox if s.label == '📚 Chọn chủ đề luyện nói theo lớp:')
                self.assertTrue(all(f'lớp {grade}' in value for value in units.options))
                self.assertTrue(at.get('audio_input'))
                text = next(t for t in at.text_area if t.key == f'eng_speech_input_Tram 1_{grade}')
                self.assertEqual(text.value, '')
                text.set_value('I have a book.').run()
        next(b for b in at.button if b.label == '📊 Góp ý bài nói theo lớp').click().run()
        self.assertEqual([e.message for e in at.exception], [])
        self.assertIn('không chấm phát âm', at.session_state['captured_feedback_prompt'])
        self.assertIn('Tiếng Anh lớp 12', at.session_state['captured_feedback_prompt'])
