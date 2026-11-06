"""Give controls a new identity when their model/context/request changes."""
import hashlib
import json


def lab_control_scope(data, subject='', context='', revision=0):
    payload = json.dumps([subject, context, revision, data], sort_keys=True,
                         ensure_ascii=False, default=str, separators=(',', ':'))
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()[:16]
