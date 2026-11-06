"""Lossless, bounded-memory XZ backup in independently readable page groups."""
import argparse
import hashlib
import json
import lzma
import os
from pathlib import Path
import tarfile

from archive_textbook_catalog import atomic_json


def digest(stream):
    value=hashlib.sha256()
    for chunk in iter(lambda:stream.read(65536),b''):value.update(chunk)
    return value.hexdigest()


def pack(manifest_path, group_size=25):
    if group_size<1 or group_size>50:raise ValueError('Page group must be between 1 and 50')
    manifest_path=Path(manifest_path).resolve();root=manifest_path.parent
    data=json.loads(manifest_path.read_text(encoding='utf-8'))
    pages=sorted(data['pages'],key=lambda r:r['index'])
    if not data.get('all_declared_pages_archived') or len(pages)!=data['expected_pages']:
        raise ValueError('Incomplete book cannot be packed as complete')
    if len({p['index'] for p in pages})!=len(pages):raise ValueError('Duplicate page index')
    for page in pages:
        p=(root/page['path']).resolve()
        if root not in p.parents or page['status']!='archived':raise ValueError('Invalid archived page path')
        with p.open('rb') as stream:
            if digest(stream)!=page['sha256']:raise ValueError('Source page hash changed')
    folder=root/'backup-xz';folder.mkdir(exist_ok=True);groups=[]
    for offset in range(0,len(pages),group_size):
        batch=pages[offset:offset+group_size];name=f'pages-{batch[0]["index"]:04d}-{batch[-1]["index"]:04d}.tar.xz'
        dest=folder/name;pending=dest.with_suffix('.pending')
        try:
            with lzma.open(pending,'wb',filters=[{'id':lzma.FILTER_LZMA2,'dict_size':1024*1024}]) as out:
                with tarfile.open(fileobj=out,mode='w|') as archive:
                    for page in batch:archive.add(root/page['path'],arcname=page['path'],recursive=False)
            expected={p['path']:p['sha256'] for p in batch};seen=set()
            with lzma.open(pending,'rb') as inp,tarfile.open(fileobj=inp,mode='r|') as archive:
                for member in archive:
                    if not member.isfile() or member.name not in expected:raise ValueError('Unexpected archive member')
                    with archive.extractfile(member) as stream:
                        if digest(stream)!=expected[member.name]:raise ValueError('XZ page hash round-trip failed')
                    seen.add(member.name)
            if seen!=set(expected):raise ValueError('Missing packed page')
            os.replace(pending,dest)
            with dest.open('rb') as stream:sha=digest(stream)
            groups.append(dict(path=name,first_page=batch[0]['index'],last_page=batch[-1]['index'],
                               bytes=dest.stat().st_size,sha256=sha,pages_verified=len(seen)))
            atomic_json(folder/'manifest.json',dict(source_url=data['source_url'],expected_pages=len(pages),
                        groups=groups,all_groups_verified=sum(r['pages_verified'] for r in groups)==len(pages),
                        compression='XZ LZMA2 dictionary 1MiB; tar stream; page groups',edition_reviewed=False))
        finally:pending.unlink(missing_ok=True)
    return dict(groups=len(groups),pages_verified=sum(r['pages_verified'] for r in groups),
                xz_bytes=sum(r['bytes'] for r in groups),raw_bytes=sum(p['bytes'] for p in pages))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--manifest',required=True);parser.add_argument('--group-size',type=int,default=25)
    args=parser.parse_args();print(json.dumps(pack(args.manifest,args.group_size)))
