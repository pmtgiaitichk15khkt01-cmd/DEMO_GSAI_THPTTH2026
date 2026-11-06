"""Attach source-bound explanations across subjects; never approve knowledge by schema."""
from copy import deepcopy
from services.curriculum_policy import question_groups

PREFIX = 'Giải thích độc lập của ứng dụng, không phải lời giải do Bộ ban hành: '


def apply_reviewed_solutions(exam, dossier, archive_sha256):
    """Bind reviewed text to source revision, subject/grade/year/variant and key.

    Callers must first authenticate/read their source archive. This binding is
    not an independent semantic review and does not assign a Ministry level.
    """
    if not archive_sha256 or dossier.get('archive_sha256') != archive_sha256:
        raise ValueError('Lời giải không khớp phiên bản đề nguồn.')
    for field, exam_field in [('subject','subject'),('grade','grade'),('year','year'),('variant','code')]:
        if dossier.get(field) is None or str(dossier[field]) != str(exam.get(exam_field)):
            raise ValueError('Lời giải không khớp môn/lớp/năm/mã đề.')
    result = deepcopy(exam)
    records = dossier.get('records', {})
    for part, questions in question_groups(result):
        for question in questions:
            sid = question.get('source_id')
            if not sid:
                raise ValueError('Thiếu định danh câu nguồn để gắn lời giải.')
            if part == 'p2':
                explanations = []
                for index, statement in enumerate(question.get('stmts', [])):
                    letter = chr(ord('a') + index)
                    record = records.get(sid + '.' + letter, {})
                    if type(record.get('answer')) is not bool or record['answer'] != statement.get('a'):
                        raise ValueError('Lời giải không khớp khóa đúng/sai nguồn.')
                    text = record.get('explanation')
                    if not isinstance(text, str) or not text.strip():
                        raise ValueError('Thiếu nội dung giải thích đã đối chiếu.')
                    statement['explain'] = text
                    explanations.append(letter + ') ' + ('Đúng' if record['answer'] else 'Sai') + ': ' + text)
                question['explain'] = PREFIX + '\n\n' + '\n\n'.join(explanations)
            else:
                record = records.get(sid, {})
                if record.get('answer') != question.get('ans') or 'answer' not in record:
                    raise ValueError('Lời giải không khớp khóa của câu nguồn.')
                text = record.get('explanation')
                if not isinstance(text, str) or not text.strip():
                    raise ValueError('Thiếu nội dung giải thích đã đối chiếu.')
                question['explain'] = PREFIX + text
    return result
