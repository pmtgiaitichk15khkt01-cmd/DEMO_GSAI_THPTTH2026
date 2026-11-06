"""Resumeable public textbook catalog archive; catalog HTML is not a full book.

No login, access-control bypass, retry, or AI call. Book files require public
download links discovered in source pages. Archives stay outside the Git tree.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import lzma
import os
from pathlib import Path
import sys
import unicodedata
import re
from urllib.parse import urljoin, urlparse

import requests
from lxml import html

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from kntt_sgk_library import KNTT_DIGITAL_LIBRARY


def slug(value):
    value = unicodedata.normalize('NFKD', value.replace('đ', 'd').replace('Đ', 'D'))
    value = ''.join(c for c in value if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', '-', value.lower()).strip('-')[:140] or 'unknown'


def seed_catalog():
    rows = []
    for grade in range(6, 13):
        rows.append(dict(grade=grade, subject='catalog', title=f'THSQG lop {grade}',
                         source_url=f'https://www.thsqg.vn/sach?lop={grade}', provider='thsqg'))
        for subject, books in KNTT_DIGITAL_LIBRARY.get(str(grade), {}).items():
            for book in books:
                rows.append(dict(grade=grade, subject=subject, title=book['title'],
                                 source_url=book['url'], provider=urlparse(book['url']).hostname))
    rows.append(dict(grade=None, subject='catalog', title='NXBGD electronic catalog',
                     source_url='https://truonghocsoquocgia.nxbgd.vn/books', provider='nxbgd'))
    unique = {}
    for row in rows:
        unique.setdefault(row['source_url'], dict(row, aliases=[]))['aliases'].append(
            {k: row[k] for k in ('grade', 'subject', 'title')})
    return list(unique.values())


def atomic_json(path, value):
    pending = path.with_suffix('.pending.json')
    pending.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    os.replace(pending, path)


def collect(directory, limit=None):
    directory = Path(directory).resolve()
    repository = Path(__file__).resolve().parents[1]
    if directory == repository or repository in directory.parents:
        raise ValueError('Book archive must be outside the repository')
    directory.mkdir(parents=True, exist_ok=True)
    manifest = directory / 'manifest.json'
    old = json.loads(manifest.read_text(encoding='utf-8')) if manifest.exists() else {'items': []}
    items = {r['source_url']: r for r in old['items']}
    seeds = seed_catalog()
    wanted = [r for r in seeds if r['source_url'] not in items]
    if limit is not None:
        wanted = wanted[:limit]

    def fetch(row):
        result = dict(row, full_book_archived=False)
        try:
            with requests.get(row['source_url'], timeout=(10, 25), stream=True) as response:
                response.raise_for_status()
                raw = bytearray()
                for chunk in response.iter_content(65536):
                    raw.extend(chunk)
                    if len(raw) > 16*1024*1024:
                        raise ValueError('Catalog response exceeds limit')
            digest = hashlib.sha256(raw).hexdigest()
            folder = directory / ('Lop-%02d' % row['grade'] if row['grade'] else 'Danh-muc') / slug(row['subject']) / 'Chi-muc'
            folder.mkdir(parents=True, exist_ok=True)
            dest = folder / (slug(row['title'])+'__'+digest[:16]+'.html.xz')
            pending = dest.with_suffix('.pending')
            with lzma.open(pending, 'wb', filters=[{'id': lzma.FILTER_LZMA2, 'dict_size': 1024*1024}]) as stream:
                stream.write(raw)
            with lzma.open(pending, 'rb') as stream:
                if hashlib.sha256(stream.read()).hexdigest() != digest:
                    raise ValueError('Archive round-trip mismatch')
            os.replace(pending, dest)
            doc = html.fromstring(bytes(raw))
            links = []
            for node in doc.xpath('//a[@href]|//iframe[@src]'):
                url = urljoin(row['source_url'], node.get('href') or node.get('src'))
                if urlparse(url).scheme not in ('http', 'https'):
                    continue
                if any(s in url for s in ('/sach/', '/doc-sach/', 'drive.google.com/', '.pdf')):
                    links.append({'title': node.text_content().strip()[:500], 'url': url})
            result.update(status='catalog_archived', path=str(dest.relative_to(directory)),
                          sha256=digest, raw_bytes=len(raw), xz_bytes=dest.stat().st_size,
                          discovered_links=list({r['url']:r for r in links}.values()))
        except Exception as error:
            result.update(status='source_unavailable', error_type=type(error).__name__)
        return result

    with ThreadPoolExecutor(max_workers=2) as workers:
        for job in as_completed([workers.submit(fetch, r) for r in wanted]):
            result = job.result()
            items[result['source_url']] = result
            atomic_json(manifest, {'schema_version':1, 'grades':list(range(6,13)),
                                  'seed_count':len(seeds), 'full_books_complete':False,
                                  'compression':'XZ/LZMA2 dictionary 1MiB; catalog only',
                                  'items':list(items.values())})
    return {'seed_count':len(seeds), 'processed':len(items),
            'catalog_archived':sum(r['status']=='catalog_archived' for r in items.values()),
            'unavailable':sum(r['status']=='source_unavailable' for r in items.values()),
            'full_books_complete':False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', required=True)
    parser.add_argument('--limit', type=int)
    args = parser.parse_args()
    print(json.dumps(collect(args.directory, args.limit)))
