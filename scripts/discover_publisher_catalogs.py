"""Archive grade catalogs and discovered book links without claiming full coverage."""
import argparse
import hashlib
import json
import lzma
from pathlib import Path
import re
from urllib.parse import urljoin, urlparse, parse_qs

from lxml import html
from archive_textbook_catalog import atomic_json
from trusted_source_session import source_session


def book_links(content, catalog_url, grade):
    doc=html.fromstring(content);rows={}
    for node in doc.xpath('//a[contains(@href,"/chi-tiet-sach/")]'):
        url=urljoin(catalog_url,node.get('href'))
        title=node.text_content().strip() or ' '.join(node.xpath('.//img/@alt'))
        if urlparse(url).hostname!='taphuan.nxbgd.vn':continue
        if not re.search(r'(?<!\d)'+str(grade)+r'(?!\d)',title):continue
        rows[url]=dict(title=title,source_url=url,grade=grade,catalog_url=catalog_url,
                       status='discovered_not_reviewed',full_book_archived=False)
    return list(rows.values())


def page_links(content, catalog_url, grade):
    doc=html.fromstring(content);urls=set()
    for node in doc.xpath('//ul[contains(@class,"pagination")]//a[@href]'):
        url=urljoin(catalog_url,node.get('href'));parsed=urlparse(url)
        number=re.fullmatch(r'/tap-huan/page-(\d+)',parsed.path)
        if parsed.hostname=='taphuan.nxbgd.vn' and number and 1<int(number[1])<=50 and parse_qs(parsed.query).get('grade')==[str(grade)]:urls.add(url)
    return sorted(urls)


def discover_pages(directory):
    root=Path(directory).resolve();repo=Path(__file__).resolve().parents[1]
    if root==repo or repo in root.parents:raise ValueError('Catalog archives must remain outside Git')
    manifest=root/'publisher_grade_catalogs.json';data=json.loads(manifest.read_text(encoding='utf-8'))
    with source_session() as session:
        for catalog in data['catalogs']:
            if catalog['status']!='catalog_archived':continue
            grade=catalog['grade'];source=lzma.decompress((root/catalog['path']).read_bytes())
            books={r['source_url']:r for r in catalog['books']};pages=catalog.setdefault('additional_pages',{})
            pending=page_links(source,catalog['url'],grade);seen=set()
            while pending:
                url=pending.pop(0)
                if url in seen:continue
                seen.add(url)
                if url in pages:
                    row=pages[url]
                    if row['status']!='catalog_archived':continue
                    content=lzma.decompress((root/row['path']).read_bytes())
                else:
                    try:
                        response=session.get(url,timeout=(10,25));response.raise_for_status();content=response.content
                        if len(content)>2*1024*1024:raise ValueError('Catalog response exceeds limit')
                        sha=hashlib.sha256(content).hexdigest();name=f'nxbgd-grade-{grade:02d}-catalog-page__{sha[:16]}.html.xz'
                        blob=lzma.compress(content,filters=[{'id':lzma.FILTER_LZMA2,'dict_size':1024*1024}]);assert lzma.decompress(blob)==content;(root/name).write_bytes(blob)
                        pages[url]=dict(status='catalog_archived',path=name,sha256=sha)
                    except Exception as error:
                        pages[url]=dict(status='unavailable',error_type=type(error).__name__);continue
                for row in book_links(content,url,grade):books[row['source_url']]=row
                pending.extend(u for u in page_links(content,url,grade) if u not in seen)
                catalog['books']=list(books.values());catalog['all_observed_catalog_pages_archived']=all(r['status']=='catalog_archived' for r in pages.values())
                atomic_json(manifest,data)
    return dict(catalogs=len(data['catalogs']),books=sum(len(r.get('books',[])) for r in data['catalogs']),scope_complete=False)


def discover(directory):
    root=Path(directory).resolve();repo=Path(__file__).resolve().parents[1]
    if root==repo or repo in root.parents:raise ValueError('Catalog archives must remain outside Git')
    root.mkdir(parents=True,exist_ok=True);manifest=root/'publisher_grade_catalogs.json'
    old=json.loads(manifest.read_text(encoding='utf-8')) if manifest.exists() else {'catalogs':[]}
    catalogs={row['grade']:row for row in old['catalogs']}
    with source_session() as session:
        for grade in range(6,13):
            if grade in catalogs:continue
            url=f'https://taphuan.nxbgd.vn/tap-huan?grade={grade}'
            try:
                response=session.get(url,timeout=(10,25));response.raise_for_status()
                content=response.content;sha=hashlib.sha256(content).hexdigest()
                path=root/f'nxbgd-grade-{grade:02d}__{sha[:16]}.html.xz'
                compressed=lzma.compress(content,filters=[{'id':lzma.FILTER_LZMA2,'dict_size':1024*1024}])
                if lzma.decompress(compressed)!=content:raise ValueError('Catalog round-trip failed')
                path.write_bytes(compressed)
                catalogs[grade]=dict(grade=grade,url=url,status='catalog_archived',sha256=sha,path=path.name,
                                     books=book_links(content,url,grade),all_grade_books_discovered=False)
            except Exception as error:
                catalogs[grade]=dict(grade=grade,url=url,status='unavailable',error_type=type(error).__name__)
            atomic_json(manifest,dict(catalogs=list(catalogs.values()),scope_complete=False,
                                     note='Only links present in fetched public catalog HTML; pagination and omitted books remain open'))
    return dict(catalogs=len(catalogs),book_links=sum(len(r.get('books',[])) for r in catalogs.values()),scope_complete=False)


def archive_details(directory):
    root=Path(directory).resolve();repo=Path(__file__).resolve().parents[1]
    if root==repo or repo in root.parents:raise ValueError('Detail archives must remain outside Git')
    catalog=json.loads((root/'publisher_grade_catalogs.json').read_text(encoding='utf-8'))
    manifest=root/'publisher_expanded_details.json'
    old=json.loads(manifest.read_text(encoding='utf-8')) if manifest.exists() else {'items':[]}
    results={row['source_url']:row for row in old['items']}
    previous=root/'nxbgd_catalog_tls_verified.json'
    if previous.exists():
        for row in json.loads(previous.read_text(encoding='utf-8'))['items']:
            if row['status']=='catalog_archived':results.setdefault(row['source_url'],row)
    with source_session() as session:
        for cat in catalog['catalogs']:
            for book in cat.get('books',[]):
                url=book['source_url']
                if url in results:continue
                row=dict(book)
                try:
                    response=session.get(url,timeout=(10,25));response.raise_for_status()
                    if response.url.rstrip('/')!=url.rstrip('/'):raise ValueError('Unexpected detail-page redirect')
                    source=response.content
                    if len(source)>2*1024*1024:raise ValueError('Detail page exceeds limit')
                    sha=hashlib.sha256(source).hexdigest();path=root/f'nxbgd-book-detail__{sha[:16]}.html.xz'
                    blob=lzma.compress(source,filters=[{'id':lzma.FILTER_LZMA2,'dict_size':1024*1024}]);assert lzma.decompress(blob)==source;path.write_bytes(blob)
                    doc=html.fromstring(source);links=[]
                    for a in doc.xpath('//a[@href]'):
                        link=urljoin(url,a.get('href'))
                        if '/doc-sach/' in link or urlparse(link).hostname=='drive.google.com':
                            links.append(dict(title=a.text_content().strip(),url=link))
                    row.update(status='catalog_archived',path=path.name,sha256=sha,links=links,observed_url=response.url)
                except Exception as error:row.update(status='unavailable',error_type=type(error).__name__)
                results[url]=row
                atomic_json(manifest,dict(items=list(results.values()),scope_complete=False))
    return dict(details=len(results),source_links=sum(len(r.get('links',[])) for r in results.values()),scope_complete=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--directory',required=True);parser.add_argument('--details',action='store_true');parser.add_argument('--pages',action='store_true')
    args=parser.parse_args();print(json.dumps(archive_details(args.directory) if args.details else discover_pages(args.directory) if args.pages else discover(args.directory)))
