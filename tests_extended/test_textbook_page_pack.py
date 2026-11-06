import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from pack_textbook_pages import pack


class TextbookPagePackTests(unittest.TestCase):
    def test_groups_stream_roundtrip_and_changed_source_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);pages=[]
            for i in range(1,4):
                data=('unique scientific page '+str(i)).encode();name=f'page-{i}.png';(root/name).write_bytes(data)
                pages.append(dict(index=i,path=name,status='archived',sha256=hashlib.sha256(data).hexdigest(),bytes=len(data)))
            p=root/'manifest.json';d=dict(source_url='https://example.org/book',expected_pages=3,pages=pages,all_declared_pages_archived=True)
            p.write_text(json.dumps(d),encoding='utf-8');result=pack(p,2)
            self.assertEqual(result['groups'],2);self.assertEqual(result['pages_verified'],3)
            receipt=json.loads((root/'backup-xz/manifest.json').read_text(encoding='utf-8'))
            self.assertTrue(receipt['all_groups_verified']);self.assertFalse(receipt['edition_reviewed'])
            old=(root/'backup-xz/pages-0001-0002.tar.xz').read_bytes()
            (root/'page-1.png').write_bytes(b'changed')
            with self.assertRaises(ValueError):pack(p,2)
            self.assertEqual((root/'backup-xz/pages-0001-0002.tar.xz').read_bytes(),old)

    def test_incomplete_book_cannot_be_marked_packed(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/'manifest.json';p.write_text(json.dumps(dict(expected_pages=3,pages=[],all_declared_pages_archived=False)),encoding='utf-8')
            with self.assertRaises(ValueError):pack(p)
            self.assertFalse((p.parent/'backup-xz').exists())
