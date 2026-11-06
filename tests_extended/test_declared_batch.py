import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import archive_declared_batch as batch


class DeclaredBatchTests(unittest.TestCase):
    def test_incomplete_book_stops_queue_without_retry_or_sampling_disabled_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);source=root/'caps.json'
            source.write_text(json.dumps({'items':[
                dict(title='SGK Toán 10',source_url='full10',download_scope='full_declared'),
                dict(title='SGK Toán 6',source_url='full6',download_scope='full_declared'),
                dict(title='SGV Toán 10',source_url='disabled',download_scope='download_disabled')]}),encoding='utf-8')
            with patch.object(batch,'archive',return_value=dict(archived=1,expected=2)) as archive,patch.object(batch,'pack') as pack:
                state=batch.run(source,root)
                archive.assert_called_once_with('full10',root)
                pack.assert_not_called();self.assertEqual(state['status'],'stopped_at_incomplete_book')
                self.assertFalse(state['scope_complete']);self.assertFalse((root/'declared_batch.active').exists())

    def test_existing_active_batch_prevents_duplicate_work(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'declared_batch.active').write_text('123',encoding='ascii')
            with patch.object(batch,'archive') as archive:
                with self.assertRaises(FileExistsError):batch.run(root/'not-read.json',root)
                archive.assert_not_called()

    def test_corrupt_cached_backup_is_not_silently_reused(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);book=root/'NXBGD-full-declared/book';backup=book/'backup-xz';backup.mkdir(parents=True)
            (book/'manifest.json').write_text(json.dumps(dict(source_url='full10',expected_pages=1,all_declared_pages_archived=True)),encoding='utf-8')
            (backup/'a.tar.xz').write_bytes(b'changed')
            (backup/'manifest.json').write_text(json.dumps(dict(all_groups_verified=True,groups=[dict(path='a.tar.xz',pages_verified=1,sha256='bad')])),encoding='utf-8')
            source=root/'caps.json';source.write_text(json.dumps({'items':[dict(title='SGK Toán 10',source_url='full10',download_scope='full_declared')]}),encoding='utf-8')
            with patch.object(batch,'archive') as archive:
                with self.assertRaises(ValueError):batch.run(source,root)
                archive.assert_not_called();self.assertFalse((root/'declared_batch.active').exists())
