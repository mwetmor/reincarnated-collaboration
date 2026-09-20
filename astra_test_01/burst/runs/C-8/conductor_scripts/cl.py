# Conductor ledger writer for Run C-8 (conductor tooling, not lane code): flock + indent=2 + atomic replace.
# usage: cl.py <kind: rulings|milestones|halts|grok_calls|notes> '<json object>'   |  cl.py init  |  cl.py show [n]
import sys, json, os, fcntl, tempfile, datetime, pathlib
P = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-8/ledger.json')
def now(): return datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
def write(mut):
    P.parent.mkdir(parents=True, exist_ok=True)
    with (P.parent/'.ledger.lock').open('a') as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        d = json.loads(P.read_text()) if P.exists() else None
        d = mut(d)
        fd, t = tempfile.mkstemp(prefix='.ledger-', dir=P.parent)
        with os.fdopen(fd, 'w') as s: json.dump(d, s, indent=2, ensure_ascii=False); s.write('\n'); s.flush(); os.fsync(s.fileno())
        os.replace(t, P)
    return d
k = sys.argv[1]
if k == 'init':
    def m(d):
        assert d is None, 'ledger exists'
        return dict(bursts=[], images_used=0, images_cap=120, experiments={}, milestones=[], halts=[], rulings=[], grok_calls=[], run='C-8',
                    charter='agentic_orchestration/gandalf/notes/2026-09-20-warlord-run-C-8-charter.md', charter_sha256_12=None)
    write(m); print('init ok')
elif k == 'set':
    key, val = sys.argv[2], json.loads(sys.argv[3])
    def m(d): d[key] = val; return d
    write(m); print('set', key)
elif k == 'show':
    d = json.loads(P.read_text()); n = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    print('images', d['images_used'], '/', d['images_cap'], '| bursts', len(d['bursts']), '| grok', len(d.get('grok_calls', [])))
    for b in d['bursts'][-n:]: print(' B', b['id'], b['type'], 'exit', b['exit'], 'img', b['image_calls'], 'min %.1f' % b['minutes'], (b['audit'].get('violations') or [])[:3], b['audit'].get('execution_error'))
    for r in d['rulings'][-n:]: print(' R', r['id'], (r.get('topic') or r.get('ruling',''))[:110])
else:
    e = json.loads(sys.argv[2]); e.setdefault('ts', now())
    def m(d):
        d.setdefault(k, []); d[k].append(e); return d
    write(m); print('appended', k, e.get('id', ''))
