# EN-E2: fold an en60 MX adoption record into the body's graft record of record (work/<g>_graft.json) so en09 (speeds from the
# source root travel) and the kit scripts (clip source labels) read the ADOPTED clips. The pre-adoption record is kept as
# work/<g>_graft_rec.json (written once). python3 scripts/en61_merge_graft.py <g>
import json, os, sys, shutil
g = sys.argv[1]; W = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'work')
G, REC, MX = (os.path.join(W, f % g) for f in ('%s_graft.json', '%s_graft_rec.json', '%s_mx_graft.json'))
if not os.path.exists(REC): shutil.copy(G, REC)
d = json.load(open(REC)); m = json.load(open(MX))
for k, v in m['clips'].items():
    v = dict(v, adopted='R-C9-150 MX audition pick (en60)'); d['clips'][k[5:] if k.startswith('__mx_') else k] = v
d['mx_adoption'] = dict(record=os.path.basename(MX), replaced=sorted(k[5:] for k in m['clips']))
json.dump(d, open(G, 'w'), indent=1); print('MERGED', g, d['mx_adoption'])
