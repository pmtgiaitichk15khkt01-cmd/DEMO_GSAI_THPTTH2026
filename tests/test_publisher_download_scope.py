import sys
from pathlib import Path
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from audit_publisher_downloads import capability


class PublisherDownloadScopeTests(unittest.TestCase):
    def test_urls_do_not_override_publisher_sample_limit(self):
        row=capability('download_book_pages:true, download_book_pages_count:2, download_book_pages_urls:["a","b","c","d"],')
        self.assertEqual(row['download_scope'],'sample_subset')
        self.assertFalse(row['full_book_archived'])

    def test_absent_or_disabled_setting_never_means_full_permission(self):
        self.assertEqual(capability('')['download_scope'],'unverified')
        disabled=capability('download_book_pages:false, download_book_pages_count:4, download_book_pages_urls:[1,2,3,4],')
        self.assertEqual(disabled['download_scope'],'download_disabled')
        self.assertFalse(disabled['full_book_archived'])

    def test_full_declared_does_not_mean_downloaded_or_reviewed(self):
        row=capability('download_book_pages:true, download_book_pages_count:2, download_book_pages_urls:["a","b"],')
        self.assertEqual(row['download_scope'],'full_declared')
        self.assertFalse(row['full_book_archived'])
