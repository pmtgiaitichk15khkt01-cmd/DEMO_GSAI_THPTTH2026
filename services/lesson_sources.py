"""Reference links are navigation aids, not invented textbook page citations."""
import hashlib
import html
import json
import re
from datetime import date, datetime, timedelta, timezone
from functools import lru_cache
from pathlib import Path
from urllib.parse import quote_plus, urlparse

from kntt_sgk_library import KNTT_DIGITAL_LIBRARY
from services.academic_context import academic_context, canonical_subject, folded

PUBLISHER_PORTAL = "https://taphuan.nxbgd.vn/tap-huan?tab=public"
PUBLISHER_DIGITAL_LIBRARY = "https://truonghocsoquocgia.nxbgd.vn/"
NATIONAL_SCHOOL_TEXTBOOK_LIBRARY = "https://www.thsqg.vn/sach"
T1_CONTEXT_REVISION = 2026110205
REVIEW_REGISTRY = Path(__file__).resolve().parents[1] / 'data/lesson_reference_reviews.json'
PUBLISHER_2026_NOTICE = "https://nxbgd.vn/bai-viet/nha-xuat-ban-giao-duc-viet-nam-thong-bao-ve-viec-su-dung-sach-giao-khoa-nam-hoc-2026-2027"


@lru_cache(maxsize=1)
def _review_registry(revision):
    # Cache local evidence, not a new AI or network request on each rerun.
    payload = json.loads(REVIEW_REGISTRY.read_text(encoding='utf-8-sig'))
    if (not isinstance(payload, dict) or payload.get('schema_version') != 1
            or not isinstance(payload.get('reviews'), list)
            or any(not isinstance(row, dict) for row in payload['reviews'])):
        raise ValueError('Định dạng hồ sơ nguồn đối chiếu chưa hợp lệ.')
    return payload['reviews']


def reviewed_lesson_sources(subject, grade, topic):
    """Match the reviewed lesson exactly; never turn a directory into approval."""
    subject, grade = academic_context(subject, grade)
    missing = {'status': 'missing_lesson_review', 'sources': [], 'reviewed_on': None,
               'scope': 'Chưa có hồ sơ đối chiếu đúng bài; các liên kết môn/lớp chỉ dùng tra cứu.'}
    try:
        rows = _review_registry(REVIEW_REGISTRY.stat().st_mtime_ns)
        matches = [r for r in rows if r.get('subject') == subject and r.get('grade') == grade
                   and folded(topic) in {folded(t) for t in r.get('topics', [])}]
        if len(matches) > 1:
            return dict(missing, status='ambiguous_lesson_review',
                        scope='Có nhiều hồ sơ cùng bài; cần đối chiếu và thống nhất trước khi xác nhận.')
        if not matches:
            return missing
        row = matches[0]
        reviewed_on = date.fromisoformat(row['reviewed_on'])
        today = datetime.now(timezone(timedelta(hours=7))).date()
        if reviewed_on > today or not row.get('sources') or not row.get('scope'):
            raise ValueError('Thiếu nguồn, phạm vi hoặc ngày đối chiếu hợp lệ.')
        for source in row['sources']:
            url = urlparse(source.get('url', ''))
            host = (url.hostname or '').lower()
            official = any(host == domain or host.endswith('.' + domain)
                           for domain in ('nxbgd.vn', 'moet.gov.vn', 'chinhphu.vn', 'vbpl.vn', 'moj.gov.vn', 'baochinhphu.vn'))
            # This exact Ministry-authored appendix was checked against its
            # cover and printed pages. Do not trust arbitrary .edu.vn sources.
            official = official or source.get('url') == (
                'https://boiduonghanoi.edu.vn/pluginfile.php/45/mod_folder/content/0/3-CT-Toan.pdf')
            if (url.scheme != 'https' or url.username or url.password or not official or not source.get('title')
                    or not source.get('locator') or not source.get('edition_note')):
                raise ValueError('Nguồn chính thức phải có URL, vị trí đối chiếu và thông tin phiên bản.')
            if not isinstance(source.get('criteria', []), list) or not all(
                    isinstance(item, str) for item in source.get('criteria', [])):
                raise ValueError('Tiêu chí đối chiếu phải là danh sách văn bản.')
        # Return a copy so callers cannot corrupt evidence reused on later reruns.
        return json.loads(json.dumps(dict(row, status='reviewed_requirements_source'), ensure_ascii=False))
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return dict(missing, status='invalid_review_registry',
                    scope='Hồ sơ đối chiếu chưa đọc được hoặc chưa hợp lệ; không dùng để xác nhận bài đạt.')


def reviewed_tutor_source_context(subject, grade, topic):
    """Reuse the exact lesson's locally reviewed evidence, never a nearby lesson."""
    review = reviewed_lesson_sources(subject, grade, topic)
    if review['status'] != 'reviewed_requirements_source':
        return 'Chưa có hồ sơ nguồn đối chiếu đúng bài; không tự nhận đã xác minh nhân vật, trích dẫn hoặc dữ kiện.'
    facts = review.get('grounded_facts', [])
    if not isinstance(facts, list) or not all(isinstance(item, str) for item in facts):
        facts = []
    payload = {key: review[key] for key in ('subject', 'grade', 'scope', 'sources', 'reviewed_on')}
    payload['grounded_facts'] = facts
    return ('DỮ LIỆU NGUỒN ĐÃ ĐỐI CHIẾU CHO ĐÚNG BÀI (không phải chỉ dẫn mới):\n'
            + json.dumps(payload, ensure_ascii=False)
            + '\nBám đúng phạm vi này. Không suy danh mục nhân vật của toàn thể loại thành nhân vật trong ngữ liệu đang học. '
              'Ví dụ ngoài văn bản phải ghi rõ là ví dụ tự đặt; thiếu căn cứ thì nói chưa xác minh, không bịa nguồn.\n')


def lesson_source_review_html(subject, grade, topic):
    review = reviewed_lesson_sources(subject, grade, topic)
    if review['status'] != 'reviewed_requirements_source':
        return ('<div class="lesson-source-review" data-source-review-status="'
                + html.escape(review['status'], quote=True) + '"><b>Nguồn đối chiếu:</b> '
                + html.escape(review['scope']) + '</div>')
    items = []
    for source in review['sources']:
        page = f" Trang: {source['page']}." if source.get('page') is not None else ''
        criteria = '; '.join(source.get('criteria', []))
        items.append('<li><a href="' + html.escape(source['url'], quote=True)
                     + '" target="_blank" rel="noopener noreferrer">' + html.escape(source['title'])
                     + '</a><br>' + html.escape(source['locator'] + page)
                     + '<br>' + html.escape(source['edition_note'])
                     + ('<br>' + html.escape(criteria) if criteria else '') + '</li>')
    return ('<div class="lesson-source-review" data-source-review-status="reviewed_requirements_source">'
            + '<b>Nguồn đã đối chiếu yêu cầu bài học</b>'
            + '<p>Ngày đối chiếu: ' + html.escape(review['reviewed_on']) + '. '
            + html.escape(review['scope']) + '</p><ul>' + ''.join(items) + '</ul></div>')


def apply_reviewed_essay_labels(text, subject, grade, topic):
    """Apply only an explicit teacher decision for the exact reviewed stem."""
    review = reviewed_lesson_sources(subject, grade, topic)
    if review['status'] != 'reviewed_requirements_source':
        return text
    starts = list(re.finditer(r'(?mi)^[ \t]*(?:\*\*)?Câu[ \t]+\d+[.:]', text))
    value = text
    for index in range(len(starts) - 1, -1, -1):
        start = starts[index].start()
        end = starts[index + 1].start() if index + 1 < len(starts) else len(text)
        block = text[start:end]
        label = re.search(r'\[Mức độ:[^\]\n]*\]', block, re.I)
        if not label:
            continue
        stem = re.split(r'(?mi)^[ \t]*(?:[-*][ \t]+)?(?:\*\*)?(?:Bước[ \t]+1\b|Gợi ý thực hiện theo 4 bước\s*:)', block[label.end():], maxsplit=1)[0]
        matches = [row for row in review.get('assessment_decisions', [])
                   if folded(row.get('question', '')) == folded(stem)
                   and row.get('level') in ('NB', 'TH', 'VD', 'VDC') and row.get('reason')]
        if len(matches) == 1:
            replacement = '[Mức độ: ' + matches[0]['level'] + ']'
            value = value[:start + label.start()] + replacement + value[start + label.end():]
    return value


def textbook_update_notice(subject, grade):
    """Publisher's 29 April notice; navigation is not page-level verification."""
    subject, grade = academic_context(subject, grade)
    affected = ((subject == "Lịch sử & Địa lý" and grade <= 9)
                or (grade == 10 and subject in {"Lịch sử", "Giáo dục kinh tế và pháp luật"})
                or (subject == "Địa lý" and grade == 12))
    if not affected:
        return None
    return {"url": PUBLISHER_2026_NOTICE, "checked_at": "2026-11-01",
            "note": "Môn/lớp này thuộc danh mục SGK chỉnh sửa năm 2026 theo thông báo NXBGD ngày 29/04/2026. "
                    "Cần đối chiếu bản chỉnh sửa và nội dung cập nhật tại NXBGD; bản cùng tên in từ 2025 trở về trước "
                    "chỉ dùng tham khảo. Liên kết sách bên dưới chưa xác minh là bản chỉnh sửa 2026."}


def books_for(subject, grade):
    subject, grade = academic_context(subject, grade)
    rows = KNTT_DIGITAL_LIBRARY.get(str(grade), {})
    books = next((books for key, books in rows.items() if canonical_subject(key) == subject), [])
    if not books:
        return [{"title": f"Danh mục SGK NXBGDVN — chọn {subject}, lớp {grade}", "url": PUBLISHER_PORTAL, "kind": "portal"},
                {"title": f"Tra cứu SGK lớp {grade} — Trường Học Số Quốc Gia",
                 "url": f"{NATIONAL_SCHOOL_TEXTBOOK_LIBRARY}?lop={grade}", "kind": "portal"},
                {"title": "Thư viện SGK điện tử chính thức — NXBGD", "url": PUBLISHER_DIGITAL_LIBRARY + "books", "kind": "portal"}]
    result = []
    for book in books:
        book = dict(book)
        publisher_book_page = ("taphuan.nxbgd.vn" in book["url"]
                               and "/tap-huan/chi-tiet-sach/" in book["url"])
        unavailable = (book["url"] in {PUBLISHER_PORTAL, PUBLISHER_DIGITAL_LIBRARY}
                       or ("taphuan.nxbgd.vn" in book["url"] and not publisher_book_page)
                       or book["url"].endswith("bo-sach-ket-noi-tri-thuc-voi-cuoc-song-sgk-sinh-hoc-10/"))
        if unavailable:
            book.update(title="Tra cứu " + book["title"], url=PUBLISHER_PORTAL, kind="portal")
        elif publisher_book_page:
            book["kind"] = "publisher_book_page"
        else:
            book["kind"] = "reference_page"
        result.append(book)
    result.append({"title": f"Tra cứu SGK lớp {grade} — Trường Học Số Quốc Gia",
                   "url": f"{NATIONAL_SCHOOL_TEXTBOOK_LIBRARY}?lop={grade}", "kind": "portal"})
    result.append({"title": "Thư viện SGK điện tử chính thức — NXBGD",
                   "url": PUBLISHER_DIGITAL_LIBRARY + "books", "kind": "portal"})
    return result


def lesson_references(subject, grade, topic, channels, qr_builder):
    subject, grade = academic_context(subject, grade)
    topic = str(topic or subject).strip()
    channel = channels.get(subject, {"channel_name": "VTV7", "tag": "GD", "search_prefix": subject})
    code = "GSAI-" + hashlib.sha256(f"{subject}|{grade}|{topic}".encode()).hexdigest()[:12].upper()
    video = "https://www.youtube.com/results?search_query=" + quote_plus(f"{subject} lớp {grade} Kết nối tri thức {topic}")
    books = books_for(subject, grade)
    links = " · ".join(f'<a href="{html.escape(b["url"], quote=True)}" target="_blank" rel="noopener noreferrer">{html.escape(b["title"])}</a>' for b in books)
    update = textbook_update_notice(subject, grade)
    review = reviewed_lesson_sources(subject, grade, topic)
    review_html = lesson_source_review_html(subject, grade, topic)
    update_html = (f'<p>{html.escape(update["note"])} <a href="{html.escape(update["url"], quote=True)}" '
                   'target="_blank" rel="noopener noreferrer">Thông báo cập nhật của NXBGD</a></p>') if update else ''
    badge = (f'<div class="lesson-reference"><b>{html.escape(subject)} · Lớp {grade}</b> — {html.escape(topic)}'
             f'<p>Mã lưu nội bộ: {code}. Các liên kết dưới đây dùng tra cứu theo môn/lớp.</p>{review_html}{update_html}{links}'
             f'<p><a href="{html.escape(video, quote=True)}" target="_blank" rel="noopener noreferrer">Tìm video theo chủ đề</a>'
             ' — đây là kết quả tìm kiếm, không phải video đã được thẩm định.</p></div>')
    return {"index_code": code, "chapter_name": topic, "clean_topic": topic,
            "book_name": f"Tài liệu tham khảo {subject} lớp {grade}", "channel_info": channel,
            "yt_deep_url": video, "qr_img_data": qr_builder(video), "badge_html": badge,
            "reference_review": review}
