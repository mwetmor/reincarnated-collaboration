# After Matt's K1′ pick: bible assets → the H1 master's content hash (asset_id slot-stable, R9); probe set → the H1 description, no reference; probe_set_sha256 re-frozen.
import sys, json, hashlib, pathlib
sys.path.insert(0, '/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'); pick = sys.argv[1].upper()
master = B/f'runs/C-1/artifacts/K1p-gen-01/k1p_master_{pick}.png'; mh = hashlib.sha256(master.read_bytes()).hexdigest()
brief = json.load(open(B/'briefs/K1p-gen-01.task.json'))['text']
desc = brief.split('DESCRIPTION (use it verbatim as the content of each call):\n',1)[1].split('\n\nCopy each output',1)[0].strip()
ps = B/'runs/C-1/probe_set.json'; P = json.load(open(ps))
P['probes'][0].update({'prompt': desc, 'references': [], 'expected_canvas': [1024, 1536]})
json.dump(P, open(ps,'w'), indent=1, ensure_ascii=False)
from oracles import model_drift_probe
frozen = model_drift_probe.freeze(ps)
ph = hashlib.sha256(ps.read_bytes()).hexdigest()
bp = B/'bible/f04-keepers.json'; b = json.load(open(bp))
old = b['assets'][0]['content_hash']; b['assets'][0]['content_hash'] = mh; b['probe_set_sha256'] = ph
json.dump(b, open(bp,'w'), indent=1, ensure_ascii=False)
from bible.validate import validate
print(json.dumps({'pick': pick, 'master': master.name, 'master_sha256': mh, 'old_asset_hash': old, 'probe_set_sha256': ph, 'freeze_returned': str(frozen)[:120], 'bible_validate': validate(b)}, indent=1))
