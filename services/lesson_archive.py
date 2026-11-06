"""Portable full lesson content; no grades, credentials or chat-state replay."""
import hashlib
import json
from services.academic_context import canonical_subject, normalize_grade

MAX_BUNDLE_BYTES = 4 * 1024 * 1024


def encode_full_lesson(text, subject, grade, topic, policy_revision):
    if not isinstance(text,str) or not text.strip():
        raise ValueError('Bài học chưa có nội dung để lưu.')
    bundle={'format':'GSAI_FULL_LESSON_V1','subject':canonical_subject(subject),
            'grade':normalize_grade(grade),'topic':str(topic),'policy_revision':str(policy_revision),
            'content':text,'content_sha256':hashlib.sha256(text.encode('utf-8')).hexdigest()}
    data=json.dumps(bundle,ensure_ascii=False,indent=2).encode('utf-8')
    if len(data)>MAX_BUNDLE_BYTES:
        raise ValueError('Bản bài học vượt giới hạn4MB.')
    return data


def decode_full_lesson(data, subject, grade):
    if not isinstance(data,bytes) or len(data)>MAX_BUNDLE_BYTES:
        raise ValueError('Tệp bài học không hợp lệ hoặc vượt4MB.')
    try:
        bundle=json.loads(data.decode('utf-8-sig'))
    except (UnicodeError,ValueError) as error:
        raise ValueError('Không đọc được tệp bài học JSON.') from error
    if not isinstance(bundle,dict) or bundle.get('format')!='GSAI_FULL_LESSON_V1':
        raise ValueError('Không đúng định dạng bản lưu đầy đủ.')
    if (canonical_subject(bundle.get('subject',''))!=canonical_subject(subject)
            or normalize_grade(bundle.get('grade',''))!=normalize_grade(grade)):
        raise ValueError('Bản lưu khác môn/lớp đang chọn; hãy chọn đúng ngữ cảnh trước.')
    text=bundle.get('content')
    if (not isinstance(text,str) or not text.strip() or
            hashlib.sha256(text.encode('utf-8')).hexdigest()!=bundle.get('content_sha256')):
        raise ValueError('Nội dung bản lưu đã thay đổi hoặc không đầy đủ.')
    # Explicit allowlist: a file cannot restore claimed scores or inject session keys.
    return {'text':text,'subject':canonical_subject(subject),'grade':normalize_grade(grade),
            'topic':str(bundle.get('topic') or ''),'content_sha256':bundle['content_sha256']}
