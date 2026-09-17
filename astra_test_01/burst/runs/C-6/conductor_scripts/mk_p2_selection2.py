# Final P2 selection for the STANDING set (R-C6-22): per direction, the attempt with the most checklist TRUEs (scale excluded);
# tie → the later attempt; any remaining FALSE → a named flag for the packet. usage: mk_p2_selection2.py <judgment relpath>=<label> ...
# Each judgment's candidates are mapped to image paths via its brief's references (skipping the control).
import json, pathlib, sys
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'); A = B/'runs/C-6/artifacts'
KEYS = ['eyes_blue','head_level','head_aligned','no_skull_buckle','no_skull_shoulder','no_skull_book','ribcage_steel','tome_master_ornament','hands_exactly_two','hands_in_front','scythe_held_out','buckle_detail','standing_upright','camera_matches']
attempts = {}  # dir -> list of (label, path, checklist, axes, seen)
for arg in sys.argv[1:]:
    jrel, label = arg.split('=')
    bid = pathlib.Path(jrel).parent.name
    brief = json.load(open(B/f'briefs/C-6/{bid}.task.json')); refs = brief['references']
    j = json.load(open(B/jrel))
    for c in j['candidates']:
        ref = refs[c['image']-1]; p = ref['path']
        if 'control_mirror' in p: continue
        d = c['claimed']; attempts.setdefault(d, []).append(dict(label=label, path=p.split('astra_test_01/burst/')[-1], checklist=c['checklist'], axes=c['axes'], seen=c['seen_facing'], mirrored=c['mirrored']))
sel = {}
for d in ['S','SW','W','NW','N','NE','E','SE']:
    best = None
    for i, a in enumerate(attempts.get(d, [])):
        cl = a['checklist']; trues = sum(1 for k in KEYS if cl.get(k) is True); falses = [k for k in KEYS if cl.get(k) is False]
        score = (0 if a['mirrored'] else 1, trues, i)
        if best is None or score >= best[0]: best = (score, a, falses)
    score, a, falses = best
    flags = [f"{k}" for k in falses]
    sel[d] = dict(stands=a['label'], path=a['path'], trues=score[1], flags=flags, axes=a['axes'], seen=a['seen'], considered=[(x['label'], sum(1 for k in KEYS if x['checklist'].get(k) is True)) for x in attempts[d]])
    print(d, a['label'], 'trues', score[1], 'FLAGS' if flags else 'clean', flags)
json.dump(dict(rule='R-C6-22: most checklist TRUEs (scale excluded), tie → later attempt; remaining FALSE → named flag', keys=KEYS, selection=sel), open(B/'runs/C-6/p2_selection_final.json','w'), indent=1)
