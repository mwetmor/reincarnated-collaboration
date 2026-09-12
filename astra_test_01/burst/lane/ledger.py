"""Conductor-owned ledger: locked read/modify and atomic replacement."""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', value):
        raise ValueError('invalid run or burst identifier')
    return value


def empty():
    return dict(bursts=[], images_used=0, images_cap=250, experiments={}, milestones=[], halts=[], rulings=[])


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def append(run, entry):
    # Preserve generator {observed_fingerprint, probe_set_sha256} and
    # regeneratable_until verbatim; conductor fills wrapper-written nulls.
    # Preserve provenance and both image instruments verbatim. Only image_calls
    # (the generated-files truth source) contributes to the run budget.
    entry = dict(entry)
    path = ROOT / 'runs' / identifier(run) / 'ledger.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    with (path.parent / '.ledger.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        data = json.loads(path.read_text()) if path.exists() else empty()
        if any(b['id'] == entry['id'] for b in data['bursts']):
            raise ValueError('duplicate burst id')
        if type(entry['image_calls']) is not int or entry['image_calls'] < 0:
            raise ValueError('invalid image count')
        data['bursts'].append(entry)
        data['images_used'] += entry['image_calls']
        fd, temp = tempfile.mkstemp(prefix='.ledger-', dir=path.parent)
        try:
            with os.fdopen(fd, 'w') as stream:
                json.dump(data, stream, indent=2)
                stream.write('\n')
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temp, path)
        finally:
            if os.path.exists(temp):
                os.unlink(temp)
    return data
