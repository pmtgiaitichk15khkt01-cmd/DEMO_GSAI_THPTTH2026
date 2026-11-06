import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import archive_publisher_pages as archive


class PublisherPageArchiveTests(unittest.TestCase):
    def session(self,text,data=b''):
        class Response:
            status_code=200
            headers={'Content-Type':'image/png'}
            def __enter__(self):return self
            def __exit__(self,*_):pass
            def raise_for_status(self):pass
            def iter_content(self,_):return iter([data])
        class Session:
            def __enter__(self):return self
            def __exit__(self,*_):pass
            def get(self,*_,**__):
                response=Response();response.text=text;return response
            def head(self,*_,**__):return Response()
        return Session()

    def test_sample_scope_never_fetches_page_data(self):
        text='download_book_pages:true,download_book_pages_count:1,download_book_pages_urls:["a","b"],'
        with tempfile.TemporaryDirectory() as directory,patch.object(archive,'source_session',return_value=self.session(text)) as session:
            with self.assertRaises(ValueError):archive.archive('https://taphuan.nxbgd.vn/book',directory)
            self.assertEqual(session.call_count,1)
            self.assertFalse(list(Path(directory).iterdir()))

    def test_full_page_set_hashes_and_resumes_without_page_requests(self):
        image=Image.new('RGB',(2,2),'white');stream=io.BytesIO();image.save(stream,format='PNG')
        text='download_book_pages:true,download_book_pages_count:2,download_book_pages_urls:["https://taphuan.nxbgd.vn/storage/upload/a.png","https://taphuan.nxbgd.vn/storage/upload/b.png"],'
        with tempfile.TemporaryDirectory() as directory,patch.object(archive,'source_session',side_effect=lambda:self.session(text,stream.getvalue())) as session:
            result=archive.archive('https://taphuan.nxbgd.vn/book',directory)
            self.assertEqual(result['archived'],2)
            manifest=json.loads(Path(result['manifest']).read_text(encoding='utf-8'))
            self.assertTrue(manifest['all_declared_pages_archived'])
            self.assertFalse(manifest['edition_reviewed'])
            self.assertEqual(session.call_count,2)
            archive.archive('https://taphuan.nxbgd.vn/book',directory)
            self.assertEqual(session.call_count,3)
            manifest['pages'][0]=dict(index=1,source_url='https://taphuan.nxbgd.vn/storage/upload/a.png',status='failed',error_type='MemoryError')
            manifest['all_declared_pages_archived']=False
            Path(result['manifest']).write_text(json.dumps(manifest),encoding='utf-8')
            archive.archive('https://taphuan.nxbgd.vn/book',directory)
            self.assertEqual(session.call_count,4)  # Failed pages are not automatically retried.
            fixed=archive.archive('https://taphuan.nxbgd.vn/book',directory,recheck_memory_indices=(1,))
            self.assertEqual(session.call_count,6)  # One source read and one pooled page session.
            self.assertEqual(fixed['archived'],2)
            repaired=json.loads(Path(result['manifest']).read_text(encoding='utf-8'))
            self.assertEqual(len(repaired['repair_history']),1)
            self.assertEqual(repaired['repair_history'][0]['error_type'],'MemoryError')
            repaired['pages'][1]=dict(index=2,source_url='https://taphuan.nxbgd.vn/storage/upload/b.png',status='failed',error_type='ConnectionError')
            Path(result['manifest']).write_text(json.dumps(repaired),encoding='utf-8')
            fixed=archive.archive('https://taphuan.nxbgd.vn/book',directory,recheck_network_indices=(2,))
            self.assertEqual(fixed['archived'],2)
            history=json.loads(Path(result['manifest']).read_text(encoding='utf-8'))['repair_history']
            self.assertEqual(history[-1]['recovery_status'],200)
            with self.assertRaises(ValueError):archive.archive('https://taphuan.nxbgd.vn/book',directory,recheck_network_indices=(2,))
