import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import archive_public_textbook as books
import archive_textbook_catalog as catalog


class TextbookArchiveTests(unittest.TestCase):
    def test_real_pdf_roundtrip_and_resume_without_second_download(self):
        import pymupdf
        with pymupdf.open() as doc:
            doc.new_page()
            payload=doc.tobytes()
        class Response:
            def __enter__(self): return self
            def __exit__(self,*_): pass
            def raise_for_status(self): pass
            def iter_content(self,_): return iter([payload])
        row=dict(grade=6,subject='Toán',book_type='SGK',title='SGK Test',provider='test',
                 source_url='https://example.org/book',observed_source_url='https://example.org/book',observed_title='SGK Test',download_url='https://example.org/file.pdf')
        with tempfile.TemporaryDirectory() as folder, patch.object(books.requests,'get',return_value=Response()) as get:
            receipt=books.archive(row,folder)
            self.assertEqual(receipt['pages'],1)
            self.assertTrue(receipt['xz_roundtrip'])
            self.assertFalse(receipt['edition_reviewed'])
            self.assertEqual(books.archive(row,folder),receipt)
            get.assert_called_once()
            (Path(folder)/receipt['path']).write_bytes(b'corrupt')
            with self.assertRaises(ValueError): books.archive(row,folder)
            get.assert_called_once()

        with tempfile.TemporaryDirectory() as folder, patch.object(books.requests,'get',return_value=Response()):
            with self.assertRaises(ValueError):books.archive(dict(row,expected_min_pdf_pages=2),folder)
            self.assertFalse(list(Path(folder).rglob('*.pdf')))

    def test_seed_catalog_keeps_grade_and_source_aliases_without_duplicates(self):
        seeds=catalog.seed_catalog()
        self.assertEqual(len({r['source_url'] for r in seeds}),len(seeds))
        self.assertEqual({r['grade'] for r in seeds if r['provider']=='thsqg'},set(range(6,13)))
        self.assertTrue(all(r['aliases'] for r in seeds))

    def test_html_cannot_be_accepted_as_book_pdf(self):
        class Response:
            def __enter__(self):return self
            def __exit__(self,*_):pass
            def raise_for_status(self):pass
            def iter_content(self,_):return iter([b'<html>Sign in</html>'])
        row=dict(grade=6,subject='Toán',book_type='SGK',title='Test',source_url='https://example.org/book',observed_source_url='https://example.org/book',observed_title='Test',download_url='https://example.org/login')
        with tempfile.TemporaryDirectory() as folder, patch.object(books.requests,'get',return_value=Response()):
            with self.assertRaises(ValueError):books.archive(row,folder)
            self.assertFalse(list(Path(folder).rglob('*.pdf')))
            self.assertFalse(list(Path(folder).rglob('*.pending')))

    def test_stale_browser_page_is_rejected_before_network_or_file_write(self):
        row=dict(source_url='https://example.org/teacher-book',observed_source_url='https://example.org/english7',observed_title='English 7')
        with tempfile.TemporaryDirectory() as folder, patch.object(books.requests,'get') as get:
            with self.assertRaises(ValueError): books.archive(row,folder)
            get.assert_not_called()
            self.assertFalse(list(Path(folder).iterdir()))
