"""Bounded official-source change watch. Detection is not legal approval."""
import hashlib
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit

import requests

OFFICIAL_HOSTS = {'congbao.chinhphu.vn', 'chinhphu.vn', 'vanban.chinhphu.vn',
                  'xaydungchinhsach.chinhphu.vn', 'moet.gov.vn', 'vqa.moet.gov.vn',
                  'vbpl.vn', 'datafiles.chinhphu.vn'}
DISCOVERY_URL = 'https://congbao.chinhphu.vn/van-ban-dang-cong-bao/bo-giao-duc-va-dao-tao-c4.htm'
MAX_BYTES = 4 * 1024 * 1024


def official_url(url):
    p = urlsplit(url)
    return (p.scheme == 'https' and p.hostname in OFFICIAL_HOSTS and
            not p.username and not p.password and p.port in (None, 443))


def fetch_source(url, session=None):
    """At most three requests, bounded body, no off-list redirects or retries."""
    client = session or requests.Session()
    try:
        for _ in range(3):
            if not official_url(url):
                raise ValueError('not_an_allowed_official_source')
            with client.get(url, timeout=(5, 12), stream=True, allow_redirects=False,
                            headers={'User-Agent': 'GSAI-source-watch/1.0'}) as response:
                if response.status_code in (301, 302, 303, 307, 308):
                    url = urljoin(url, response.headers.get('Location', ''))
                    continue
                response.raise_for_status()
                data = bytearray()
                for chunk in response.iter_content(32768):
                    data.extend(chunk)
                    if len(data) > MAX_BYTES:
                        raise ValueError('source_size_limit')
                content_type = response.headers.get('Content-Type', '')
                if not data or not any(t in content_type.lower() for t in ('html', 'pdf', 'text/')):
                    raise ValueError('empty_or_unsupported_source')
                return {'url': url, 'sha256': hashlib.sha256(data).hexdigest(),
                        'bytes': len(data), 'content_type': content_type}, bytes(data)
        raise ValueError('redirect_limit')
    finally:
        if session is None:
            client.close()


class EducationLinks(HTMLParser):
    def __init__(self, base):
        super().__init__()
        self.base, self.href, self.words, self.links = base, None, [], []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.href, self.words = dict(attrs).get('href'), []

    def handle_data(self, value):
        if self.href:
            self.words.append(value)

    def handle_endtag(self, tag):
        if tag != 'a' or not self.href:
            return
        title = ' '.join(' '.join(self.words).split())
        url = urljoin(self.base, self.href)
        if official_url(url) and any(k in title.casefold() for k in
                ('phổ thông', 'sách giáo khoa', 'đánh giá học sinh', 'thi tốt nghiệp')):
            if url not in {x['url'] for x in self.links} and len(self.links) < 100:
                self.links.append({'title': title[:1000], 'url': url,
                                   'status': 'candidate_requires_applicability_review'})
        self.href = None


def scan_sources(registry, previous, *, checked_at, fetcher=fetch_source):
    """No registry writes, activation, model calls or semantic inference."""
    prior = previous.get('observations', {}) if isinstance(previous, dict) else {}
    observations, failures, changes = {}, [], []
    targets = [('education_discovery', DISCOVERY_URL)]
    targets.extend((r['code'], r['url']) for r in registry['documents'])
    candidates = []
    for key, url in targets[:30]:
        if not official_url(url):
            failures.append({'code': key, 'reason': 'source_not_in_official_allowlist'})
            continue
        try:
            info, body = fetcher(url)
            observations[key] = {**info, 'checked_at': checked_at}
            old = prior.get(key, {})
            if old.get('sha256') != info['sha256']:
                changes.append({'code': key, 'reason': 'changed' if old else 'first_observation'})
            if key == 'education_discovery':
                parser = EducationLinks(info['url'])
                parser.feed(body.decode('utf-8', errors='replace'))
                candidates = parser.links
        except Exception as exc:
            # Do not record exception URLs, cookies, content or query credentials.
            failures.append({'code': key, 'reason': type(exc).__name__})
    return {'checked_at': checked_at, 'observations': observations, 'changes': changes,
            'failures': failures, 'candidates': candidates,
            'status': 'review_required' if changes or failures else 'no_observed_change',
            'academic_verified': False, 'legal_validity_verified': False,
            'discovery_coverage': 'one official listing page; not exhaustive',
            'registry_modified': False}
