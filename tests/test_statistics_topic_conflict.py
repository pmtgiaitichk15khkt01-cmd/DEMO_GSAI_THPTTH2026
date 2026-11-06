import copy
import unittest
from unittest.mock import Mock

from services.academic_context import subjects_for_grade
from services.context_recovery import repair_exam_context
from services.curriculum_policy import prepare_exam_for_delivery
from services.request_scope import explicit_request_scope, question_scope_issue, question_topic_issue


FUNCTIONS = ['Ứng dụng đạo hàm khảo sát & vẽ đồ thị hàm số']
STATISTICS = ['Các số đặc trưng đo mức độ phân tán (Mẫu ghép nhóm)']


def statistics():
    # Exact observed question text and incorrect bank topic, not an AI output fixture.
    return dict(subject='Toán học', grade=12, topic='Khảo sát và vẽ đồ thị hàm số', level='TH',
        q='Khảo sát thời gian (phút) tự học mỗi ngày của 50 học sinh, ta có bảng mẫu số liệu ghép nhóm sau:\nKhoảng biến thiên của mẫu số liệu ghép nhóm bằng:',
        opt=['A. 75 phút', 'B. 60 phút', 'C. 45 phút', 'D. 105 phút'], ans='A',
        mslgn_data={'groups': ['[30;45)', '[45;60)', '[60;75)', '[75;90)', '[90;105)'], 'freq': [6,14,18,8,4]})


def cubic():
    return dict(subject='Toán học', grade=12, topic='Khảo sát và vẽ đồ thị hàm số', level='TH',
        q='Hàm số $y=x^3+x$ có bao nhiêu điểm cực trị?',
        opt=['A. 0', 'B. 1', 'C. 2', 'D. 3'], ans='A')


class TestStatisticsTopicConflict(unittest.TestCase):
    def test_exact_observed_bad_topic_is_detected_from_content(self):
        q = statistics()
        before = copy.deepcopy(q)
        self.assertEqual(question_topic_issue(q, 'Toán học', FUNCTIONS), 'outside_selected_topic')
        self.assertEqual(question_scope_issue(q, explicit_request_scope('Toán', 'Chỉ khảo sát hàm bậc ba')), 'outside_explicit_request')
        self.assertEqual(q, before)

    def test_statistics_remains_available_for_correct_or_mixed_topics(self):
        for topics in (STATISTICS, FUNCTIONS + STATISTICS, []):
            self.assertEqual(question_topic_issue(statistics(), 'Toán học', topics), '')
        generator = Mock()
        result = repair_exam_context({'p1':[statistics()]}, 'Toán học', 12, topics=STATISTICS, ai_generator=generator)
        self.assertEqual(result['context_recovery']['unresolved'], 0)
        generator.assert_not_called()

    def test_bank_replacement_skips_mislabelled_statistics_and_delivers_cubic(self):
        source = {'p1':[statistics()]}
        before = copy.deepcopy(source)
        ai = Mock()
        result = repair_exam_context(source, 'Toán học', 12, topics=FUNCTIONS,
            bank_provider=lambda *_: {'p1':[dict(statistics(), q=statistics()['q'] + ' Chọn phương án đúng.'), cubic()]}, ai_generator=ai)
        self.assertEqual(result['context_recovery']['unresolved'], 0)
        self.assertEqual(result['p1'][0]['q'], cubic()['q'])
        self.assertEqual(result['p1'][0]['replacement_audit']['reason'], 'outside_selected_topic')
        self.assertEqual(source, before)
        ai.assert_not_called()
        self.assertEqual(prepare_exam_for_delivery(result, 'Toán học', 12)['p1'][0]['ans'], 'A')

    def test_mislabelled_statistics_is_not_accepted_as_ai_replacement(self):
        source = {'p1':[dict(cubic(), opt=[])]}
        result = repair_exam_context(source, 'Toán học', 12, topics=FUNCTIONS,
            ai_generator=lambda _: {'replacement_question':statistics()})
        self.assertEqual(result['context_recovery']['unresolved'], 1)
        self.assertEqual(result['p1'][0]['q'], source['p1'][0]['q'])

    def test_function_variation_and_statistical_function_model_are_not_blocked(self):
        for text in ('Cho hàm số bậc ba có bảng biến thiên như sau.',
                     'Cho hàm số $y=x^3+x$. Xét sự biến thiên.',
                     'Cho mẫu số liệu ghép nhóm được mô hình hóa bằng hàm số bậc ba. Xét đạo hàm.'):
            self.assertEqual(question_topic_issue(dict(statistics(), q=text), 'Toán học', FUNCTIONS), '')

    def test_other_subjects_and_grades_are_not_reclassified(self):
        checked = 0
        for grade in range(6,13):
            for subject in subjects_for_grade(grade):
                self.assertEqual(question_topic_issue(cubic(), subject, FUNCTIONS), '')
                if subject != 'Toán học':
                    self.assertEqual(question_topic_issue(statistics(), subject, FUNCTIONS), '')
                checked += 1
        self.assertEqual(checked, 65)


if __name__ == '__main__':
    unittest.main()
