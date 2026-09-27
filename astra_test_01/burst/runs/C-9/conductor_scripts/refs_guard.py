# C-9 attach guard (charter § 1 / HALT H-guard): refs_guard.py <task.json> [...]
# Every reference must be (a) an attach_to_generator:true row of the ART-1 refs ledger (sha match), (b) a C-9 derived
# input listed in runs/C-9/inputs/manifest.json (sha match), or (c) lane substrate on the ALLOW list (sha pinned here).
# Any look-only file, any sha matching an attach:false row, any forbidden name in the task text -> exit 1 (HALT, never retry).
import sys, json, hashlib, pathlib, re
ROOT = pathlib.Path('/Users/admin/Games/reincarnated-collaboration')
REFS = ROOT/'matt_notes_handoff_docs/rdr-art-illuminated-archive-refs'
INP = ROOT/'astra_test_01/burst/runs/C-9/artifacts/inputs'
ALLOW = {  # lane substrate: path -> sha256 (pinned when first used; conductor edit + ledger note to add a row)
 str(ROOT/'astra_test_01/burst/runs/C-3/artifacts/CS-guides/chunk_A_guide.png'): '77217a4a3bba573b1bb28617f830e29d9bc886fec3e9ff9f97f0693954ffbb55',
}
FORBID = re.compile(r'final\s*fantasy|yoshida|square\s*enix|ivalice|ramza|delita|agrias|vagrant\s*story|tactics\s*ogre|hollow\s*knight|\bchibi\b|\banime\b', re.I)
sha = lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
rows = [json.loads(l) for l in (REFS/'ledger.jsonl').read_text().splitlines() if l.strip()]
ok_sha = {r['sha256'] for r in rows if r.get('attach_to_generator') is True}
bad_sha = {r['sha256'] for r in rows if r.get('attach_to_generator') is False}
inp = json.loads((INP/'manifest.json').read_text())['sha256']
fail = []
for t in sys.argv[1:]:
    task = json.loads(pathlib.Path(t).read_text())
    if FORBID.search(task['text']): fail.append(f'{t}: forbidden name in text: {FORBID.search(task["text"]).group(0)!r}')
    for ref in task['references']:
        p = pathlib.Path(ref['path']); s = sha(p)
        if 'look-only' in str(p) or s in bad_sha: fail.append(f'{t}: LOOK-ONLY reference {p}'); continue
        if s in ok_sha: continue
        if p.parent == INP and inp.get(p.name) == s: continue
        if str(p) in ALLOW and (ALLOW[str(p)] in (None, s)): continue
        fail.append(f'{t}: unregistered reference {p} ({s[:12]})')
print('\n'.join(fail) if fail else f'refs_guard OK ({len(sys.argv)-1} task(s))'); sys.exit(1 if fail else 0)
