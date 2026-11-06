"""Archive an explicitly discovered public PDF without login or access bypass."""
import argparse
import hashlib
import json
import lzma
import os
from pathlib import Path
import shutil
from urllib.parse import urlsplit

import requests

from archive_textbook_catalog import atomic_json, slug


def stream_digest(stream):
    digest = hashlib.sha256()
    for chunk in iter(lambda: stream.read(65536), b''):
        digest.update(chunk)
    return digest.hexdigest()


def archive(row, directory):
    observed = row.get('observed_source_url')
    if not observed or urlsplit(observed)._replace(fragment='').geturl().rstrip('/') != urlsplit(row['source_url'])._replace(fragment='').geturl().rstrip('/'):
        raise ValueError('Verified browser source URL must match the requested book before download')
    if not row.get('observed_title'):
        raise ValueError('Record the observed source title before download')
    directory = Path(directory).resolve()
    repo = Path(__file__).resolve().parents[1]
    if directory == repo or repo in directory.parents:
        raise ValueError('Keep book data outside Git')
    folder = directory / ('Lop-%02d' % row['grade']) / slug(row['subject']) / slug(row['book_type'])
    folder.mkdir(parents=True, exist_ok=True)
    source_id = hashlib.sha256(row['source_url'].encode('utf-8')).hexdigest()[:12]
    stem = slug(row['title']) + '__' + slug(row.get('provider', 'source')) + '__' + source_id
    receipt = folder / (stem + '.json')
    if receipt.exists():
        saved = json.loads(receipt.read_text(encoding='utf-8'))
        old = directory / saved['path']
        if old.is_file():
            with old.open('rb') as stream:
                digest = stream_digest(stream)
            if digest == saved['sha256']:
                return saved
        raise ValueError('Previous archive missing or changed; preserve receipt for investigation')
    pending = folder / (stem + '.pending')
    try:
        digest = hashlib.sha256()
        size = 0
        with requests.get(row['download_url'], stream=True, timeout=(10, 60)) as response:
            response.raise_for_status()
            with pending.open('wb') as out:
                for chunk in response.iter_content(65536):
                    size += len(chunk)
                    if size > 200*1024*1024:
                        raise ValueError('Public PDF exceeds 200MiB limit')
                    digest.update(chunk)
                    out.write(chunk)
        with pending.open('rb') as stream:
            if not stream.read(1024).lstrip().startswith(b'%PDF-'):
                raise ValueError('Response is not a PDF (login/confirmation/HTML is not a book)')
        import pymupdf
        with pymupdf.open(pending) as doc:
            pages = len(doc)
            if doc.is_encrypted or pages == 0:
                raise ValueError('Encrypted or empty PDF is not accepted')
            if row.get('expected_min_pdf_pages') and pages < row['expected_min_pdf_pages']:
                raise ValueError('Downloaded PDF has fewer pages than the verified source minimum')
        sha = digest.hexdigest()
        dest = folder / (stem + '__' + sha[:16] + '.pdf')
        os.replace(pending, dest)
        packed = dest.with_suffix('.pdf.xz')
        temp = packed.with_suffix('.pending')
        with dest.open('rb') as inp, lzma.open(temp, 'wb', filters=[{'id':lzma.FILTER_LZMA2,'dict_size':1024*1024}]) as out:
            shutil.copyfileobj(inp, out, length=65536)
        with lzma.open(temp, 'rb') as stream:
            restored = stream_digest(stream)
        if restored != sha:
            raise ValueError('XZ round-trip failed')
        os.replace(temp, packed)
        result = dict(row, status='pdf_archived', path=str(dest.relative_to(directory)),
                      sha256=sha, bytes=size, pages=pages, xz_path=str(packed.relative_to(directory)),
                      xz_bytes=packed.stat().st_size, xz_roundtrip=True,
                      completeness_verified=bool(row.get('expected_min_pdf_pages')),
                      edition_reviewed=False, all_pages_semantically_reviewed=False)
        atomic_json(receipt, result)
        return result
    finally:
        pending.unlink(missing_ok=True)


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--input',required=True)
    parser.add_argument('--directory',required=True)
    args=parser.parse_args()
    print(json.dumps(archive(json.loads(Path(args.input).read_text(encoding='utf-8')),args.directory),ensure_ascii=True))
