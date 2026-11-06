"""Sequential archive/backup of explicitly full-download publisher sources.

Stops on the first incomplete or failed book; no automatic retry, scheduler,
AI calls, or claim of curriculum/edition acceptance.
"""
import argparse
import json
import os
from pathlib import Path
import re

from archive_publisher_pages import archive
from archive_textbook_catalog import atomic_json
from pack_textbook_pages import pack, digest


def run(capabilities, directory):
    root=Path(directory).resolve();repo=Path(__file__).resolve().parents[1]
    if root==repo or repo in root.parents:raise ValueError('Book data must stay outside Git')
    root.mkdir(parents=True,exist_ok=True);lock=root/'declared_batch.active'
    descriptor=os.open(lock,os.O_WRONLY|os.O_CREAT|os.O_EXCL)
    os.write(descriptor,str(os.getpid()).encode());os.close(descriptor)
    report=root/'declared_batch_progress.json'
    state=dict(status='running',items=[],scope_complete=False,knowledge_accepted=False)
    try:
        data=json.loads(Path(capabilities).read_text(encoding='utf-8'))
        rows=[r for r in data['items'] if r.get('download_scope')=='full_declared']
        def order(row):
            match=re.search(r'(?<!\d)(1[012]|[6-9])(?!\d)',row.get('title',''))
            grade=int(match[1]) if match else 99
            return (0 if grade in (10,11,12) else 1,grade,row.get('title',''))
        rows.sort(key=order);state['declared_full_count']=len(rows)
        existing={}
        for manifest in (root/'NXBGD-full-declared').glob('*/manifest.json'):
            entry=json.loads(manifest.read_text(encoding='utf-8'));existing[entry['source_url']]=(manifest,entry)
        for row in rows:
            url=row['source_url'];current=dict(source_url=url,title=row.get('title',''),status='running')
            state['current']=current;atomic_json(report,state)
            previous=existing.get(url)
            backup=previous[0].parent/'backup-xz/manifest.json' if previous else None
            if previous and previous[1].get('all_declared_pages_archived') and backup and backup.exists():
                receipt=json.loads(backup.read_text(encoding='utf-8'))
                if receipt.get('all_groups_verified'):
                    if sum(g.get('pages_verified',0) for g in receipt.get('groups',[]))!=previous[1]['expected_pages']:
                        raise ValueError('Cached backup page count no longer matches source manifest')
                    for group in receipt['groups']:
                        path=(backup.parent/group['path']).resolve()
                        if backup.parent not in path.parents:raise ValueError('Unexpected cached backup path')
                        with path.open('rb') as stream:
                            if digest(stream)!=group['sha256']:raise ValueError('Cached backup hash changed')
                    current['status']='reused_verified_archive';state['items'].append(current);atomic_json(report,state);continue
            result=archive(url,root)
            if result['archived']!=result['expected']:
                current.update(status='incomplete',archive=result);state['items'].append(current)
                state['status']='stopped_at_incomplete_book';atomic_json(report,state);return state
            current.update(status='packing',archive=result);atomic_json(report,state)
            packed=pack(result['manifest'])
            current.update(status='archive_and_backup_verified',backup=packed)
            state['items'].append(current);atomic_json(report,state)
        state['status']='declared_full_sources_processed';state['all_declared_full_processed']=True
        state.pop('current',None);atomic_json(report,state);return state
    except Exception as error:
        state.update(status='stopped_at_error',error_type=type(error).__name__)
        atomic_json(report,state);raise
    finally:lock.unlink(missing_ok=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--capabilities',required=True);parser.add_argument('--directory',required=True)
    args=parser.parse_args();result=run(args.capabilities,args.directory)
    print(json.dumps(dict(status=result['status'],processed=len(result['items']),scope_complete=False)))
