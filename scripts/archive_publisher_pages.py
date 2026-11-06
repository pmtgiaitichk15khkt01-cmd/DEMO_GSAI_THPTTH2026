"""Archive only page sets explicitly declared fully downloadable by publisher."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from urllib.parse import urlparse

from PIL import Image
from archive_textbook_catalog import atomic_json, slug
from audit_publisher_downloads import capability
from trusted_source_session import source_session


def archive(source_url, directory, recheck_memory_indices=(), recheck_network_indices=()):
    root=Path(directory).resolve()
    repository=Path(__file__).resolve().parents[1]
    if root==repository or repository in root.parents:
        raise ValueError('Book pages belong outside Git')
    with source_session() as session:
        response=session.get(source_url,timeout=(10,25));response.raise_for_status()
        source=response.text
    scope=capability(source)
    if scope['download_scope']!='full_declared':
        raise ValueError('Publisher has not declared this complete page set downloadable')
    urls=json.loads(re.search(r'\bdownload_book_pages_urls\s*:\s*(\[[^\n]*\])',source)[1])
    if any(urlparse(u).hostname!='taphuan.nxbgd.vn' or '/storage/upload/' not in urlparse(u).path for u in urls):
        raise ValueError('Unexpected publisher page origin')
    folder=root/'NXBGD-full-declared'/slug(urlparse(source_url).path.split('/')[-1])
    folder.mkdir(parents=True,exist_ok=True)
    manifest=folder/'manifest.json'
    prior=json.loads(manifest.read_text(encoding='utf-8')) if manifest.exists() else {'pages':[]}
    pages={r['index']:r for r in prior['pages']}
    repair_history=list(prior.get('repair_history',[]))
    for index in recheck_memory_indices:
        row=pages.get(index)
        if not row or row.get('status')!='failed' or row.get('error_type')!='MemoryError':
            raise ValueError('Explicit memory repair must target a recorded MemoryError')
        if any(r.get('index')==index for r in repair_history):
            raise ValueError('A repaired page requires investigation instead of repeated retries')
        repair_history.append(dict(row,repair='disk-streaming/single-worker patch verification'))
        del pages[index]
    if recheck_network_indices:
        with source_session() as probe:
            for index in recheck_network_indices:
                row=pages.get(index)
                if not row or row.get('status')!='failed' or row.get('error_type')!='ConnectionError':
                    raise ValueError('Network recovery verification must target a recorded ConnectionError')
                if any(r.get('index')==index for r in repair_history):
                    raise ValueError('Do not repeatedly retry a repaired page')
                response=probe.head(row['source_url'],timeout=(10,20),allow_redirects=False)
                if response.status_code!=200 or not response.headers.get('Content-Type','').startswith('image/'):
                    raise ValueError('Page source has not recovered; preserve failure')
                repair_history.append(dict(row,repair='Explicit recovery check after HEAD200; pooled single-worker download',
                                           recovery_status=response.status_code,recovery_content_type=response.headers.get('Content-Type')))
                del pages[index]
    for row in pages.values():
        if row.get('status')=='archived':
            p=folder/row['path']
            with p.open('rb') as stream:
                digest=hashlib.sha256()
                for chunk in iter(lambda:stream.read(65536),b''):digest.update(chunk)
            if digest.hexdigest()!=row['sha256']:
                raise ValueError('Archived page changed; preserve and investigate')

    def fetch(index,url):
        row=dict(index=index,source_url=url)
        pending=None
        try:
            digest=hashlib.sha256();size=0
            with page_session.get(url,stream=True,timeout=(10,40)) as response:
                response.raise_for_status()
                with tempfile.NamedTemporaryFile(dir=folder,suffix='.pending',delete=False) as out:
                    pending=Path(out.name)
                    for chunk in response.iter_content(65536):
                        size+=len(chunk)
                        if size>20*1024*1024:raise ValueError('Page exceeds limit')
                        digest.update(chunk);out.write(chunk)
            with Image.open(pending) as image:
                image.verify()
            sha=digest.hexdigest();name=f'page-{index:04d}__{sha[:16]}.png'
            dest=folder/name;os.replace(pending,dest)
            row.update(status='archived',path=name,sha256=sha,bytes=size)
        except Exception as error:row.update(status='failed',error_type=type(error).__name__)
        finally:
            if pending is not None:pending.unlink(missing_ok=True)
        return row
    pending_pages=[(i,u) for i,u in enumerate(urls,1) if i not in pages]
    if not pending_pages:
        return dict(expected=len(urls),archived=sum(r['status']=='archived' for r in pages.values()),manifest=str(manifest))
    # Exactly one worker owns the pooled connection; no concurrent Session use.
    with source_session() as page_session, ThreadPoolExecutor(max_workers=1) as workers:
        for job in as_completed([workers.submit(fetch,i,u) for i,u in pending_pages]):
            row=job.result();pages[row['index']]=row
            atomic_json(manifest,dict(source_url=source_url,download_scope=scope,
                        expected_pages=len(urls),pages=sorted(pages.values(),key=lambda r:r['index']),
                        repair_history=repair_history,
                        all_declared_pages_archived=len(pages)==len(urls) and all(r['status']=='archived' for r in pages.values()),
                        edition_reviewed=False,content_reviewed=False))
    return dict(expected=len(urls),archived=sum(r['status']=='archived' for r in pages.values()),manifest=str(manifest))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--url',required=True);parser.add_argument('--directory',required=True)
    parser.add_argument('--verify-memory-fix-indices',type=int,nargs='*',default=[])
    parser.add_argument('--verify-network-recovery-indices',type=int,nargs='*',default=[])
    args=parser.parse_args();print(json.dumps(archive(args.url,args.directory,args.verify_memory_fix_indices,args.verify_network_recovery_indices)))
