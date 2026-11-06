import sys
from pathlib import Path
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from discover_publisher_catalogs import book_links, archive_details, page_links


class CatalogDiscoveryTests(unittest.TestCase):
    def test_pagination_uses_actual_publisher_paths_and_keeps_grade_scope(self):
        source='''<ul class="pagination"><a href="/tap-huan/page-1?grade=11">1</a><a href="/tap-huan/page-2?grade=11">2</a><a href="/tap-huan/page-2?grade=11">Next</a><a href="/tap-huan/page-3?grade=12">wrong grade</a><a href="https://example.org/tap-huan/page-2?grade=11">external</a></ul>'''
        self.assertEqual(page_links(source,'https://taphuan.nxbgd.vn/tap-huan?grade=11',11),['https://taphuan.nxbgd.vn/tap-huan/page-2?grade=11'])

    def test_detail_archive_rejects_repository_before_read_or_network(self):
        with self.assertRaises(ValueError):archive_details(Path(__file__).resolve().parents[1])

    def test_catalog_deduplicates_links_without_cross_grade_or_external_source(self):
        content='''<a href="/tap-huan/chi-tiet-sach/toan11">Toán 11</a>
        <a href="/tap-huan/chi-tiet-sach/toan11">Toán 11</a>
        <a href="/tap-huan/chi-tiet-sach/toan12">Toán 12</a>
        <a href="https://example.org/chi-tiet-sach/toan11">Toán 11</a>'''
        rows=book_links(content,'https://taphuan.nxbgd.vn/tap-huan?grade=11',11)
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]['title'],'Toán 11')
        self.assertFalse(rows[0]['full_book_archived'])
        self.assertEqual(rows[0]['status'],'discovered_not_reviewed')
