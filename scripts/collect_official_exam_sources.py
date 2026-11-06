"""Archive discovered official PDF sources once, with hashes and provenance.

Downloads are not item extraction, scientific review or an assertion of levels.
Source files live outside the repository. No retry or AI call is performed.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile
from urllib.parse import urlparse
import requests


def atomic_json(path, payload):
    temporary = path.with_suffix('.pending.json')
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    os.replace(temporary, path)


def file_sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(65536), b''):
            digest.update(block)
    return digest.hexdigest()


def collect(discovery, directory, manifest_path):
    directory.mkdir(parents=True, exist_ok=True)
    previous = json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else {'items': []}
    items = {row['source_url']: row for row in previous['items']}
    wanted = {}
    for year in discovery['years']:
        for link in year['links']:
            url = link['url']
            if urlparse(url).hostname != 'bcp.cdnchinhphu.vn' or not urlparse(url).path.lower().endswith('.pdf'):
                continue
            wanted[url] = {'source_url': url, 'index_url': year['index_url'], 'exam_year': year['exam_year'],
                           'school_year': year['school_year'], 'label': link['label']}
    def fetch(row):
        temporary = None
        try:
            with requests.get(row['source_url'], timeout=(10, 30), stream=True) as response:
                response.raise_for_status()
                digest = hashlib.sha256(); size = 0; prefix = b''
                with tempfile.NamedTemporaryFile(dir=directory, suffix='.download', delete=False) as stream:
                    temporary = Path(stream.name)
                    for block in response.iter_content(65536):
                        if not prefix: prefix = block[:5]
                        size += len(block)
                        if size > 25 * 1024 * 1024:
                            raise ValueError('source_exceeds_25MiB_manual_review_needed')
                        digest.update(block); stream.write(block)
                if prefix != b'%PDF-':
                    raise ValueError('response_is_not_pdf')
                sha = digest.hexdigest(); target = directory / (sha + '.pdf')
                os.replace(temporary, target); temporary = None
                return {**row, 'status': 'archived_not_item_reviewed', 'sha256': sha,
                        'bytes': size, 'local_file': str(target), 'final_url': response.url}
        except Exception as error:
            return {**row, 'status': 'download_failed_no_retry', 'error_type': type(error).__name__}
        finally:
            if temporary: temporary.unlink(missing_ok=True)
    pending = []
    for url, row in wanted.items():
        old = items.get(url, {})
        if old.get('status') == 'archived_not_item_reviewed':
            path = Path(old['local_file'])
            if path.is_file() and file_sha256(path) == old['sha256']:
                continue
        # A previous failed download needs an explicit reviewed retry decision.
        if old.get('status') == 'download_failed_no_retry':
            continue
        pending.append(row)
    with ThreadPoolExecutor(max_workers=3) as executor:
        for future in as_completed([executor.submit(fetch, row) for row in pending]):
            row = future.result(); items[row['source_url']] = row
            atomic_json(manifest_path, {'scope': 'source_archival_not_item_or_level_acceptance',
                'items': list(items.values())})
    return list(items.values())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--discovery', type=Path, required=True)
    parser.add_argument('--directory', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, required=True)
    args = parser.parse_args()
    rows = collect(json.loads(args.discovery.read_text(encoding='utf-8')), args.directory, args.manifest)
    print(json.dumps({'records': len(rows), 'archived': sum(x['status'] == 'archived_not_item_reviewed' for x in rows),
                      'failed': sum(x['status'] == 'download_failed_no_retry' for x in rows)}))
