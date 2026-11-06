import ast
import json
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch
from tests.test_expert_patch_regressions import load_function


class Station1ClosureTests(unittest.TestCase):
    def test_owner_required_character_lesson_is_not_reduced_to_praise(self):
        self.run_reply(reply='Bài giảng nhân sinh.')
        self.assertIn('BẮT BUỘC có một bài giảng triết lý nhân sinh và đạo đức', self.last_prompt)
        self.assertIn('DƯỠNG THIỆN TÂM – ƯƠM NHÂN TÀI', self.last_prompt)
        self.assertIn('2–3 đoạn', self.last_prompt)
        self.assertNotIn('tối đa 160 từ', self.last_prompt)

    def test_station1_selects_verified_asian_and_european_thinkers_by_context(self):
        import random
        tree = ast.parse((Path(__file__).resolve().parents[1] / 'app.py').read_text(encoding='utf-8'))
        node = next(n for n in tree.body if isinstance(n, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == 'CROSS_STATION_PHILOSOPHY_BANK' for t in n.targets))
        bank = ast.literal_eval(node.value)
        state = {}
        choose = load_function('get_unique_philosophical_lesson', st=SimpleNamespace(session_state=state),
                               random=random, CROSS_STATION_PHILOSOPHY_BANK=bank)
        east = choose(1, 'Ngữ văn', 'Em chưa biết, chưa hiểu và còn thắc mắc')
        west = choose(1, 'Tin học', 'Em kiểm bằng chứng, sửa sai rồi thử lại')
        self.assertEqual(east['author'], 'Khổng Tử')
        self.assertEqual(west['author'], 'Marcus Aurelius')
        for item in (east, west):
            self.assertTrue(item['source_verified'])
            self.assertTrue(item['source_url'].startswith('https://classics.mit.edu/'))
            self.assertTrue(item['source_locator'])
            self.assertTrue(item['translation_note'])
        state['used_philosophical_quotes'] = [east['quote'], east['author']]
        self.assertNotEqual(choose(1, 'Ngữ văn', 'chưa hiểu')['author'], east['author'])

    def test_negated_or_past_mastery_is_not_a_closure(self):
        detect = load_function('detect_student_concluded_intent')
        for message in ('Em chưa nắm vững rồi', 'Lúc trước em đã hiểu bài, giờ em còn băn khoăn',
                        'Em không có ý nói em đã hiểu bài', 'Em đã hiểu bài nhưng vẫn lúng túng'):
            with self.subTest(message=message):
                self.assertFalse(detect(message))

    def test_explicit_no_more_questions_is_a_conclusion(self):
        detect = load_function('detect_student_concluded_intent')
        for message in ('Dạ em không còn thắc mắc.', 'Em hiểu bài rồi, không có thắc mắc.', 'Dạ hết thắc mắc rồi thầy.',
                        'Em đã hiểu bài và muốn chuyển sang luyện tập.'):
            with self.subTest(message=message):
                self.assertTrue(detect(message))

    def test_new_question_or_unresolved_confusion_is_not_closed(self):
        detect = load_function('detect_student_concluded_intent')
        for message in ('Em không còn thắc mắc phần trước nhưng thầy cho em hỏi thêm?', 'Em chưa hết thắc mắc.', 'Em không hiểu.', 'Em chưa hết câu hỏi.', 'Em hiểu bài rồi nhưng không hiểu vì đổi dấu.', 'Em hiểu bài rồi nhưng chỗ này tại sao đổi dấu?',
                        'Em đã hiểu bài nhưng tại sao quỳ đổi màu?'):
            with self.subTest(message=message):
                self.assertFalse(detect(message))

    def closure_try(self):
        tree = ast.parse((Path(__file__).resolve().parents[1] / 'app.py').read_text(encoding='utf-8'))
        return next(node for node in ast.walk(tree) if isinstance(node, ast.Try) and
                    any(isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id=='t1_ans' for t in n.targets)
                        for child in node.body for n in ast.walk(child)))

    def run_reply(self, reply='', failure=False, subject='Toán học', grade=8,
                  message='Em không còn thắc mắc.', closed=False):
        class State(dict):
            __getattr__ = dict.__getitem__
        state=State(tram1_chat_history=[], tram1_understood=closed)
        register=Mock()
        class Slot:
            def __init__(self): self.markdown = Mock()
            def container(self): return self
            def __enter__(self): return self
            def __exit__(self, *_): return False
        st=SimpleNamespace(session_state=state,
            write_stream=Mock(side_effect=RuntimeError('offline') if failure else None,return_value=reply),
            empty=Slot, error=Mock())
        ns=dict(json=json,st=st,grade_num=grade,t1_input=message,t1_hist_ctx='',t1_sys_inst='',subject=subject,student_name='QA',
            detect_student_concluded_intent=lambda *a:True,get_unique_philosophical_lesson=lambda *a:{'lesson':'Kiên trì','author':'FixtureAuthor','origin':'fixture','quote':'test'},get_cross_station_pedagogical_context=lambda *a:'',register_station_closure=register,
            stream_gemini_with_fallback=Mock(return_value=iter(())),sanitize_katex_latex=lambda s:s,
            chemical_display_markdown=lambda s:s)
        exec(compile(ast.Module(body=[self.closure_try()],type_ignores=[]),'t1-closure-try','exec'),ns)
        self.last_stream = ns['stream_gemini_with_fallback']
        self.last_state = state
        self.last_prompt = self.last_stream.call_args.args[0] if self.last_stream.called else ''
        return register

    def test_post_closure_thanks_ends_without_api_or_new_question(self):
        register = self.run_reply(message='EM CẢM ƠN THẦY RẤT NHIỀU Ạ!', closed=True)
        self.last_stream.assert_not_called()
        register.assert_not_called()
        self.assertTrue(self.last_state['tram1_understood'])
        self.assertNotIn('?', self.last_state['tram1_chat_history'][-1]['content'])

    def test_thanks_with_new_question_is_not_suppressed(self):
        from services.socratic_context import is_post_closure_thanks
        self.assertFalse(is_post_closure_thanks('Em cảm ơn thầy, nhưng tại sao đạo hàm đổi dấu?', True))
        self.assertFalse(is_post_closure_thanks('Em cảm ơn thầy rất nhiều ạ!', False))
        self.assertFalse(is_post_closure_thanks('Em cảm ơn nhưng em chưa hiểu', True))

    def test_thanks_can_recover_completed_closing_from_same_chat(self):
        from services.socratic_context import is_post_closure_thanks
        history = [{'role': 'assistant', 'content': 'Nguồn: Internet Classics Archive. Thầy chúc em học tốt ở Trạm 2.'}]
        self.assertTrue(is_post_closure_thanks('Em cảm ơn thầy rất nhiều ạ!', False, history))
        self.assertFalse(is_post_closure_thanks('Cảm ơn thầy nhưng vì sao?', False, history))
        self.assertFalse(is_post_closure_thanks('Em cảm ơn thầy!', False,
            [{'role': 'assistant', 'content': 'Chào em, bài này tìm hiểu đạo hàm.'}]))

    def test_owner_moral_closure_is_present_for_every_supported_subject_grade(self):
        from services.academic_context import subjects_for_grade
        # Parse once: this checks the real closure branch across contexts without
        # calling a provider or rebuilding the full Streamlit application65times.
        node = self.closure_try()
        count = 0
        with patch.object(self, 'closure_try', return_value=node):
            for grade in range(6, 13):
                for subject in subjects_for_grade(grade):
                    with self.subTest(subject=subject, grade=grade):
                        register = self.run_reply(reply='Phản hồi kiểm thử.', subject=subject, grade=grade)
                        self.assertIn('BẮT BUỘC có một bài giảng triết lý nhân sinh và đạo đức', self.last_prompt)
                        self.assertIn('DƯỠNG THIỆN TÂM – ƯƠM NHÂN TÀI', self.last_prompt)
                        self.assertIn(f'Học sinh đang học lớp {grade}', self.last_prompt)
                        self.assertIn('Không hỏi thêm', self.last_prompt)
                        self.assertIn('không gán tác giả', self.last_prompt)
                        register.assert_called_once()
                        count += 1
        self.assertEqual(count, 65)

    def test_closure_keeps_lesson_without_unverified_quote_attribution(self):
        self.run_reply(reply='Kiên trì và trung thực.')
        self.assertIn('Kiên trì', self.last_prompt)
        self.assertIn('không gán tác giả', self.last_prompt)
        self.assertNotIn('FixtureAuthor', self.last_prompt)
        self.assertIn('không nhầm đạo hàm cấp một', self.last_prompt)

    def test_station2_closure_prompt_does_not_depend_on_station1_locals(self):
        tree=ast.parse((Path(__file__).resolve().parents[1]/'app.py').read_text(encoding='utf-8'))
        node=next(n for n in ast.walk(tree) if isinstance(n,ast.Assign)
            and any(isinstance(t,ast.Name) and t.id=='prompt_msg' for t in n.targets)
            and 'TRẠM 2 (CLOSURE)' in ast.dump(n.value))
        ns=dict(t2_cross_ctx='',history_context='',q='Em hiểu rồi',student_name='QA',
            t2_quote_data={'lesson':'Trung thực','author':'QA','origin':'fixture','quote':'test'})
        exec(compile(ast.Module(body=[node],type_ignores=[]),'t2-closure-isolation','exec'),ns)
        self.assertIn('Trạm 3',ns['prompt_msg'])

    def test_stream_error_or_empty_reply_does_not_register_closure(self):
        self.run_reply(failure=True).assert_not_called()
        self.run_reply(reply='').assert_not_called()

    def test_new_lesson_chat_does_not_inherit_previous_understanding(self):
        class State(dict):
            __getattr__ = dict.__getitem__
            __setattr__ = dict.__setitem__
        tree = ast.parse((Path(__file__).resolve().parents[1] / 'app.py').read_text(encoding='utf-8'))
        node = next(n for n in ast.walk(tree) if isinstance(n, ast.If) and
                    'tram1_active_chat_key' in ast.dump(n.test))
        from services.academic_context import subjects_for_grade
        for grade in range(6,13):
            for subject in subjects_for_grade(grade):
                state=State(tram1_active_chat_key='previous',tram1_chat_history=[],
                    tram1_understood=True,tram1_closure_info={'quote':'old'},
                    used_philosophical_quotes=['old'],current_topic='New lesson')
                ns=dict(st=SimpleNamespace(session_state=state),chat_context_key=f'{subject}_{grade}_new',student_name='QA',subject=subject)
                exec(compile(ast.Module(body=[node],type_ignores=[]),'t1-chat-reset','exec'),ns)
                self.assertFalse(state.get('tram1_understood'), (subject,grade))
                self.assertNotIn('tram1_closure_info',state)
                self.assertEqual(state['used_philosophical_quotes'],['old'])

    def test_successful_reply_registers_closure_once(self):
        self.run_reply(reply='Em hãy giữ tính trung thực và kiên trì trong học tập.').assert_called_once()


if __name__ == '__main__':
    unittest.main()
