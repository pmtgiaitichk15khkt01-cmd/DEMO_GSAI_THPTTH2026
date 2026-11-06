import copy
import unittest
from unittest.mock import Mock, patch
from services.legal_source_watch import DISCOVERY_URL, EducationLinks, fetch_source, official_url, scan_sources


class LegalSourceWatchTests(unittest.TestCase):
    def test_allowlist_rejects_official_lookalikes_and_credentials(self):
        for url in ('http://congbao.chinhphu.vn/a', 'https://congbao.chinhphu.vn.evil.test/a', 'https://user:pass@congbao.chinhphu.vn/a', 'https://127.0.0.1/a'):
            self.assertFalse(official_url(url))
        self.assertTrue(official_url(DISCOVERY_URL))

    def response(self, *, status=200, headers=None, body=b'document'):
        response = Mock(status_code=status, headers=headers or {'Content-Type': 'text/html'})
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        response.iter_content.return_value = [body]
        return response

    def test_redirect_to_nonofficial_host_is_never_requested(self):
        client = Mock()
        client.get.return_value = self.response(status=302, headers={'Location': 'https://evil.test/p'})
        with self.assertRaises(ValueError):
            fetch_source(DISCOVERY_URL, client)
        self.assertEqual(client.get.call_count, 1)

    def test_body_limit_is_enforced_without_whole_response_read(self):
        client = Mock()
        client.get.return_value = self.response(body=b'12345')
        with patch('services.legal_source_watch.MAX_BYTES', 4), self.assertRaises(ValueError):
            fetch_source(DISCOVERY_URL, client)
        client.get.return_value.read.assert_not_called()

    def test_discovery_only_returns_official_relevant_candidates(self):
        parser = EducationLinks(DISCOVERY_URL)
        parser.feed('<a href="/new.htm">Sửa chương trình phổ thông</a><a href="https://evil.test/law">sách giáo khoa</a><a href="/other">Lãi suất</a>')
        self.assertEqual(len(parser.links), 1)
        self.assertEqual(parser.links[0]['status'], 'candidate_requires_applicability_review')

    def test_first_changed_and_unchanged_never_modify_or_certify_registry(self):
        registry = {'documents': [{'code': 'fixture', 'url': 'https://congbao.chinhphu.vn/doc'}]}
        before = copy.deepcopy(registry)
        def get(url):
            return {'url': url, 'sha256': 'same', 'bytes': 5, 'content_type': 'text/html'}, b'<p>ok</p>'
        first = scan_sources(registry, {}, checked_at='2026-10-31', fetcher=get)
        self.assertEqual(len(first['changes']), 2)
        second = scan_sources(registry, first, checked_at='2026-11-01', fetcher=get)
        self.assertEqual(second['status'], 'no_observed_change')
        self.assertFalse(second['legal_validity_verified'])
        self.assertEqual(registry, before)
        changed = copy.deepcopy(first)
        changed['observations']['fixture']['sha256'] = 'old'
        self.assertIn({'code': 'fixture', 'reason': 'changed'}, scan_sources(registry, changed, checked_at='2026-11-01', fetcher=get)['changes'])

    def test_failure_is_reported_and_not_interpreted_as_no_change(self):
        report = scan_sources({'documents': []}, {}, checked_at='2026-10-31', fetcher=Mock(side_effect=TimeoutError()))
        self.assertEqual(report['status'], 'review_required')
        self.assertEqual(report['failures'][0]['reason'], 'TimeoutError')
        self.assertFalse(report['registry_modified'])


if __name__ == '__main__':
    unittest.main()
