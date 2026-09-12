"""Atomic conductor dependency DAG keyed by slot-stable asset_id, not hash.

record accepts generated/approved/human_edited/do_not_regenerate/invalidated.
human_edited is immediately protected as do_not_regenerate. Invalidating that
asset marks its invalidated flag but NEVER removes the regeneration lock;
all dependents are still traversed. invalidate returns the seed plus transitive
dependents. Files are runs/<run>/deps.json; tests patch ROOT under tests/tmp.
"""
from contextlib import contextmanager
import fcntl
import json
import os
from pathlib import Path
import re
import tempfile
from lane.ledger import identifier

ROOT=Path(__file__).resolve().parents[1]
STATES={'generated','approved','human_edited','do_not_regenerate','invalidated'}


def _asset_id(value):
    if not isinstance(value,str) or not value.strip():raise ValueError('Nonempty asset_id required')
    return value


def _acyclic(assets):
    active=set();done=set()
    def visit(key):
        if key in active:raise ValueError('Dependency cycle')
        if key in done:return
        active.add(key)
        for dep in assets.get(key,{}).get('deps',[]):visit(dep)
        active.remove(key);done.add(key)
    for key in assets:visit(key)


@contextmanager
def _transaction(run):
    path=ROOT/'runs'/identifier(run)/'deps.json';path.parent.mkdir(parents=True,exist_ok=True)
    with (path.parent/'.deps.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        data=json.loads(path.read_text()) if path.exists() else dict(assets={})
        yield data
        fd,tmp=tempfile.mkstemp(prefix='.deps-',dir=path.parent)
        try:
            with os.fdopen(fd,'w') as stream:
                json.dump(data,stream,indent=2,sort_keys=True);stream.write('\n')
                stream.flush();os.fsync(stream.fileno())
            os.replace(tmp,path)
        finally:
            if os.path.exists(tmp):os.unlink(tmp)


def record(run,asset_id,content_hash,deps,state):
    _asset_id(asset_id)
    if not isinstance(content_hash,str) or not re.fullmatch('[0-9a-f]{64}',content_hash):
        raise ValueError('content_hash must be lowercase sha256')
    if not isinstance(deps,(list,tuple)):raise ValueError('deps must be a list of asset IDs')
    deps=list(deps)
    for dep in deps:_asset_id(dep)
    if len(deps)!=len(set(deps)) or asset_id in deps:raise ValueError('Duplicate or self dependency')
    if state not in STATES:raise ValueError('Unknown asset state')
    with _transaction(run) as data:
        old=data['assets'].get(asset_id)
        if old and old['state']=='do_not_regenerate' and state not in ('human_edited','do_not_regenerate','invalidated'):
            raise ValueError('Human-edited asset is do_not_regenerate')
        protected=state in ('human_edited','do_not_regenerate') or bool(old and old['state']=='do_not_regenerate')
        row=dict(asset_id=asset_id,content_hash=content_hash,deps=deps,
                 state='do_not_regenerate' if protected else state,
                 invalidated=state=='invalidated')
        data['assets'][asset_id]=row;_acyclic(data['assets'])
    return row


def invalidate(run,asset_id):
    _asset_id(asset_id)
    with _transaction(run) as data:
        assets=data['assets']
        if asset_id not in assets:raise ValueError('Unknown asset_id')
        affected={asset_id};queue=[asset_id]
        while queue:
            changed=queue.pop()
            for key,row in assets.items():
                if changed in row['deps'] and key not in affected:
                    affected.add(key);queue.append(key)
        for key in affected:
            row=assets[key];row['invalidated']=True
            if row['state']!='do_not_regenerate':row['state']='invalidated'
    return affected
