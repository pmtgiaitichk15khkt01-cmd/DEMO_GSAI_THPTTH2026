"""Shared instructions for data the existing web renderer can display."""
import re


def graph_identification_answer_leak(question):
    """Only flag a numeric formula appended to an explicit identification task."""
    raw = str(question.get('q', ''))
    from services.academic_context import folded
    text = folded(raw)
    identifies = re.search(r'(?:do thi|la do thi) (?:cua )?ham so nao', text)
    return bool(identifies and re.search(r'\b(?:y|f\s*\(\s*x\s*\))\s*=\s*[^$\n]*x', raw))

WEB_QUESTION_INSTRUCTION = r'''
HỢP ĐỒNG CÂU HỎI TRÊN WEB:
- q/opt/stmts chỉ chứa văn bản, công thức KaTeX trong $...$ hoặc $$...$$; không chèn tài liệu LaTeX, center, tikzpicture, tkzTab hoặc mã vẽ vào các chuỗi này.
- Câu đọc đồ thị phải kèm dữ liệu hình trong cùng object: ví dụ f={"type":"func_3","a":1,"b":0,"c":-3,"d":1}. Các hệ số phải là số; không dùng chữ tham số thay hệ số của hình. Nếu hỏi nhận dạng đồ thị của hàm số nào, công thức tạo hình chỉ nằm trong f và explain nội bộ; KHÔNG ghi công thức đáp án trong q, chú thích, tiêu đề hình hoặc câu “Giả định đồ thị ...”. Giữ công thức ở các phương án để học sinh tự nhận dạng.
- Bảng biến thiên dùng trường bbt là chuỗi nhiều dòng phân cách bằng |, ví dụ: "x | -inf | -1 | 1 | +inf\ny' | + | 0 | - | 0 | +\ny | -inf | 3 | -1 | +inf". Không dùng mã TikZ làm hình web. Bảng số liệu dùng mslgn_data với groups và freq cùng độ dài.
- Mỗi câu trắc nghiệm có đúng một phương án đúng. Tự xét cả bốn phương án độc lập: một khoảng con của khoảng đồng biến/nghịch biến cũng là phương án đúng, không chỉ khoảng tối đại. Không đặt hai khoảng cùng thỏa mãn.
- Thiếu dữ liệu hình thì biên soạn lại toàn câu và các phương án/khóa chấm đồng bộ, giữ đúng môn/lớp/chủ đề/mức độ; không đoán hình gốc hoặc chỉ sửa một đáp án.
'''


def replacement_schema(part, subject, grade, topics, level=''):
    question = {'subject': subject, 'grade': grade, 'topic': topics[0] if topics else '',
                'q': 'Nội dung đầy đủ của một câu thay thế', 'level': level,
                'explain': 'Lập luận nội bộ để kiểm tra khóa chấm',
                'socratic_hint': 'Một câu hỏi gợi mở theo ngữ cảnh, không nêu lời giải hoặc đáp án'}
    if part == 'p1':
        question.update(opt=['A. ...', 'B. ...', 'C. ...', 'D. ...'], ans='A')
    elif part == 'p2':
        question['stmts'] = [{'t': f'Mệnh đề {i}', 'a': True} for i in range(1, 5)]
    else:
        question['ans'] = 'Đáp số cùng đơn vị/quy tắc làm tròn phù hợp'
    return {'replacement_question': question}


def replacement_question_object(response):
    """Accept one unambiguous question, never select from multiple candidates."""
    if not isinstance(response, dict):
        raise ValueError('Replacement response must contain a question object.')
    # One explicit transport wrapper is equivalent to the requested root.
    if set(response) == {'output'} and isinstance(response['output'], dict):
        response = response['output']
    containers = {'p1', 'p2', 'p3', 'questions', 'question', 'output'}
    if 'replacement_question' in response:
        item = response['replacement_question']
        if not isinstance(item, dict) or any(k in response for k in containers | {'q'}):
            raise ValueError('Ambiguous replacement response.')
        return item
    # A bare complete question carries its own identity; do not fill metadata.
    if (isinstance(response.get('q'), str) and response['q'].strip()
            and {'subject', 'grade', 'topic'} <= response.keys()
            and not any(k in response for k in containers)):
        return response
    raise ValueError('Replacement response must contain one identified question.')
