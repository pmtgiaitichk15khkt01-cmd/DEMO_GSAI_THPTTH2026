"""Authored speaking examples by grade, not quotations or certified SGK units."""
from copy import deepcopy
import re
from services.academic_context import normalize_grade


_SAMPLES = {
    6: ('School things', [('book', '/bʊk/', 'quyển sách'), ('pen', '/pen/', 'bút mực'),
                        ('ruler', '/ˈruːlə/', 'thước kẻ'), ('bag', '/bæɡ/', 'cặp, túi')],
        'This is my school bag. I have two books, a pen and a ruler. I like my school.',
        'What school things do you have in your bag?'),
    7: ('Hobbies', [('hobby', '/ˈhɒbi/', 'sở thích'), ('read', '/riːd/', 'đọc'),
                    ('draw', '/drɔː/', 'vẽ'), ('garden', '/ˈɡɑːdən/', 'khu vườn')],
        'My hobby is reading. I read books after school. At weekends, I draw pictures with my friends.',
        'What is your hobby, and when do you do it?'),
    8: ('Leisure activities', [('leisure', '/ˈleʒə/', 'thời gian rảnh'), ('relax', '/rɪˈlæks/', 'thư giãn'),
                              ('prefer', '/prɪˈfɜː/', 'thích hơn'), ('outdoor', '/ˈaʊtdɔː/', 'ngoài trời')],
        'In my leisure time, I enjoy cycling with my friends. I prefer outdoor activities because they help me relax.',
        'Which leisure activity do you prefer, and why?'),
    9: ('Local community', [('community', '/kəˈmjuːnəti/', 'cộng đồng'), ('local', '/ˈləʊkəl/', 'địa phương'),
                            ('volunteer', '/ˌvɒlənˈtɪə/', 'tình nguyện viên'), ('support', '/səˈpɔːt/', 'hỗ trợ')],
        'Our local community has a small library. Volunteers help younger children read there. I would like to support this activity.',
        'What could you do to help people in your local community?'),
    10: ('Family life', [('housework', '/ˈhaʊswɜːk/', 'việc nhà'), ('share', '/ʃeə/', 'chia sẻ'),
                         ('responsibility', '/rɪˌspɒnsəˈbɪləti/', 'trách nhiệm'), ('routine', '/ruːˈtiːn/', 'thói quen thường ngày')],
         'In my family, we share the housework. I wash the dishes after dinner, while my brother cleans the floor. Sharing responsibilities helps us care for one another.',
         'How does your family share household responsibilities?'),
    11: ('Healthy habits', [('balanced', '/ˈbælənst/', 'cân bằng'), ('habit', '/ˈhæbɪt/', 'thói quen'),
                            ('active', '/ˈæktɪv/', 'năng động'), ('routine', '/ruːˈtiːn/', 'thói quen thường ngày')],
         'I am trying to build healthy habits. I keep a regular daily routine and make time for physical activity. I also try to balance my study time with rest.',
         'Which habit would you like to improve, and how could you change your routine?'),
}


def speaking_units_for_grade(grade, advanced_examples):
    grade = normalize_grade(grade)
    if grade == 12:
        # Retain the existing four examples, without inventing SGK unit numbers.
        result = {}
        for title, value in advanced_examples.items():
            title = re.sub(r'^Unit\s*\d+\s*:\s*', '', title)
            result[f'Mẫu mở rộng lớp 12: {title}'] = deepcopy(value)
        return result
    title, words, passage, question = _SAMPLES[grade]
    return {f'Mẫu luyện nói lớp {grade}: {title}': {
        'vocab': [dict(word=word, ipa=ipa, meaning=meaning) for word, ipa, meaning in words],
        'passage': passage, 'q_reflex': question}}


def speaking_feedback_prompt(grade, topic, example, question, has_audio):
    grade = normalize_grade(grade)
    evidence = ('Có tệp âm thanh: chỉ nhận xét phát âm, ngắt nghỉ và độ trôi chảy khi nghe được rõ; '
                'đánh dấu chỗ không nghe rõ, không bịa bản chép lời.' if has_audio else
                'Chỉ có văn bản: không chấm phát âm, ngữ điệu, tốc độ hoặc độ trôi chảy thực tế; '
                'không giả vờ đã nghe âm thanh.')
    return (f'Bạn là gia sư Tiếng Anh lớp {grade}. Chủ đề luyện nói do ứng dụng biên soạn: {topic}. '
            f'Câu hỏi: {question}\nVí dụ tham khảo, không phải trích SGK: {example}\n'
            + evidence + '\nGóp ý ngắn bằng tiếng Việt, phù hợp lớp: nội dung, từ vựng, ngữ pháp; '
            'Giữ bốn nhóm nhận xét: nội dung và mạch lạc; từ vựng; ngữ pháp; phát âm và ngắt nghỉ (nhóm cuối chỉ khi đủ âm thanh). '
            'Nêu tối đa hai điểm cần sửa có dẫn chứng từ bài học sinh; đề nghị học sinh tự sửa trước. '
            'Giữ mục gợi ý cải thiện và mẫu diễn đạt tham khảo ngắn, phù hợp lớp; không thay thành bài làm hoàn chỉnh của học sinh. '
            'Đặt một câu hỏi nối tiếp bằng tiếng Anh vừa sức. Không tự nhận là giám khảo chính thức; '
            'không quy đổi điểm thành IELTS/CEFR, không hứa Band 8.0. Nếu thiếu dữ liệu, nói rõ phần chưa đánh giá được.')
