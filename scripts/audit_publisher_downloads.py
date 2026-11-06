"""Read public publisher download declarations; never expand sample downloads."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
import re
from urllib.parse import urljoin, urlparse

from archive_textbook_catalog import atomic_json
from trusted_source_session import source_session


def capability(source):
    def value(name):
        match=re.search(r'\b'+name+r'\s*:\s*(\[[^\n]*\]|true|false|\d+)',source)
        return json.loads(match[1]) if match else None
    allowed=value('download_book_pages')
    count=value('download_book_pages_count')
    urls=value('download_book_pages_urls')
    total=len(urls) if isinstance(urls,list) else None
    return dict(download_enabled=allowed, declared_download_pages=count,
                declared_reader_pages=total,
                download_scope=('download_disabled' if allowed is False
                                else 'sample_subset' if allowed and count is not None and total and count<total
                                else 'full_declared' if allowed and count is not None and total and count>=total
                                else 'unverified'),
                full_book_archived=False)


def audit(catalog_path, report_path):
    catalog=json.loads(Path(catalog_path).read_text(encoding='utf-8'))
    seeds={}
    for row in catalog['items']:
        for link in row.get('links',[]):
            url=urljoin(row['source_url'],link['url'])
            if urlparse(url).hostname=='taphuan.nxbgd.vn' and '/doc-sach/' in url:
                seeds.setdefault(url,dict(source_url=url,title=link['title'],catalog_sources=[]))['catalog_sources'].append(row['source_url'])
    report_path=Path(report_path)
    old=json.loads(report_path.read_text(encoding='utf-8')) if report_path.exists() else {'items':[]}
    results={r['source_url']:r for r in old['items']}
    def read(row):
        try:
            with source_session() as session:
                response=session.get(row['source_url'],timeout=(10,25));response.raise_for_status()
                return dict(row,status='read',**capability(response.text))
        except Exception as error:
            return dict(row,status='unavailable',error_type=type(error).__name__)
    with ThreadPoolExecutor(max_workers=2) as workers:
        for future in as_completed([workers.submit(read,row) for url,row in seeds.items() if url not in results]):
            row=future.result();results[row['source_url']]=row
            atomic_json(report_path,dict(seed_count=len(seeds),items=list(results.values()),
                                        scope='Publisher declarations only, not current edition approval or full-book archiving'))
    return dict(readers=len(results),sample_subset=sum(r.get('download_scope')=='sample_subset' for r in results.values()),
                full_declared=sum(r.get('download_scope')=='full_declared' for r in results.values()))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--catalog',required=True);parser.add_argument('--report',required=True)
    args=parser.parse_args();print(json.dumps(audit(args.catalog,args.report)))
