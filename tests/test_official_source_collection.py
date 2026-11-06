import importlib.util
from pathlib import Path
import tempfile
from unittest.mock import patch
import unittest

spec = importlib.util.spec_from_file_location('source_collection', Path('scripts/collect_official_exam_sources.py'))
collector = importlib.util.module_from_spec(spec); spec.loader.exec_module(collector)


class SourceCollectionTests(unittest.TestCase):
    def discovery(self):
        return {'years': [{'exam_year':2026, 'school_year':'2025-2026', 'index_url':'https://example.org/index',
            'links':[{'url':'https://bcp.cdnchinhphu.vn/answer.pdf', 'label':'Môn mẫu'}]}]}

    def response(self, data):
        class Response:
            url = 'https://bcp.cdnchinhphu.vn/answer.pdf'
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def raise_for_status(self): pass
            def iter_content(self, size): yield data
        return Response()

    def test_verified_cache_prevents_second_network_call(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch.object(collector.requests, 'get', return_value=self.response(b'%PDF-test')) as get:
                first = collector.collect(self.discovery(), root, root/'manifest.json')
                with patch.object(Path, 'read_bytes', side_effect=AssertionError('Whole source must not be loaded into RAM')):
                    second = collector.collect(self.discovery(), root, root/'manifest.json')
                self.assertEqual(get.call_count, 1)
                self.assertEqual(first, second)

    def test_non_pdf_never_becomes_archived_source_or_automatic_retry(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with patch.object(collector.requests, 'get', return_value=self.response(b'<html>error</html>')) as get:
                first = collector.collect(self.discovery(), root, root/'manifest.json')
                collector.collect(self.discovery(), root, root/'manifest.json')
                self.assertEqual(first[0]['status'], 'download_failed_no_retry')
                self.assertEqual(get.call_count, 1)
                self.assertFalse(list(root.glob('*.download')))
