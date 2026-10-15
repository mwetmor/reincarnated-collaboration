"""BLOCK-1 (jack-ryan 4bf8738a9; KP-477): the leech-reconciled per-cell HP-chain identity, evaluated
independently on BOTH arms (ADDENDUM-A CORR-1 s2, CORR-2 ss2-3).

  sum(applied, GO)  ==  sum(hp_initial - hp_final, GO-BODIES)  +  leech_heal_hp

Her arm: hpchain grains (/Users/admin/Games/join3c-bulk/hpchain/her), leech from HPCHAIN.jsonl; HPCHAIN hp_fall
cross-checked; off-ledger falls checked from J4B-ROWS packets in emission order (a body's HP before a packet
must equal its HP after the previous packet on it, starting at hp_initial).
His arm: gb-fix flinch-on grains, leech from JOIN-PROVENANCE cells[..]['go']['leech_heal_hp'].
Read-only. Usage: python3 block1_identity.py <out.json>
"""
import glob, json, sys

def rows(p):
    return [json.loads(l) for l in open(p) if l.strip()]

ARMS = ('M0', 'M-POL-2', 'M-POL-2-NULL', 'W1', 'W1-NULL')
out = {}
for side, base in (('her', '/Users/admin/Games/join3c-bulk/hpchain/her'),
                   ('his', '/Users/admin/Games/join3c-bulk/gb-fix/arms/his')):
    worst = 0.0; fails = []; falls = 0; n = 0; per = []
    for A in ARMS:
        go = rows(f'{base}/{A}-join/GO.jsonl'); gb = rows(f'{base}/{A}-join/GO-BODIES.jsonl')
        if side == 'her':
            hc = rows(f'{base}/{A}-join/HPCHAIN.jsonl')
            heal = {r['salt']: r['leech_heal_hp'] for r in hc}; hpf = {r['salt']: r['hp_fall'] for r in hc}
        else:
            prov = json.load(open(f'{base}/{A}-join/JOIN-PROVENANCE.json'))['cells']
            heal = {int(k.split('|')[1]): v['go']['leech_heal_hp'] for k, v in prov.items()}; hpf = {}
        for s in range(5):
            app = sum(r['applied'] for r in go if r['salt'] == s)
            fall = sum(r['hp_initial'] - r['hp_final'] for r in gb if r['salt'] == s)
            res = app - fall - heal[s]; rel = abs(res) / max(1, app); worst = max(worst, rel); n += 1
            per.append({'cell': f'{A}|{s}', 'applied': app, 'hp_fall': fall, 'leech_heal_hp': heal[s],
                        'residual': res, 'rel': rel})
            if rel > 1e-9:
                fails.append((A, s, res))
            if side == 'her' and abs(hpf[s] - fall) > 1e-6 * max(1, fall):
                fails.append((A, s, 'hp_fall mismatch', hpf[s], fall))
        if side == 'her':
            for p in glob.glob(f'{base}/{A}-join/J4B-ROWS-*.json'):
                d = json.load(open(p)); hp = {}
                for b in gb:
                    if b['salt'] == d['salt']:
                        hp[b['actor_id']] = b['hp_initial']
                for pk in d['packets']:
                    t = pk['target_id']; before = pk['hp_after'] + pk['applied']
                    if t in hp and before < hp[t] - 1e-9 * max(1, hp[t]):
                        falls += 1
                    hp[t] = pk['hp_after']
    out[side] = {'cells': n, 'worst_rel': worst, 'fails': fails,
                 'off_ledger_falls': falls if side == 'her' else
                 'not derivable from his GO (no hp_after); port identity_pass', 'per_cell': per}
    print(side, {k: v for k, v in out[side].items() if k != 'per_cell'})
json.dump(out, open(sys.argv[1], 'w'), indent=1, default=str)
