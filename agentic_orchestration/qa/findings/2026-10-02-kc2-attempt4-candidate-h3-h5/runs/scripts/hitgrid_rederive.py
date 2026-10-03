"""jack-ryan independent re-derivation of join1-hitchance-grid-v1 G1H ROWSET.
(1) ROWSET of gamora's frozen G1H.jsonl by the manifest's ROWSET_LAW; (2) rows recomputed from inputs.json + draws by
calling the 969fbd8d oracle's threat.probability_to_hit / threat.resolve_hit directly; (3) NC-H1 PTH_MINIMUM 55->5 RED count."""
import sys, json, struct, hashlib, os
ENG, GRID = sys.argv[1], sys.argv[2]
sys.path.insert(0, ENG); sys.dont_write_bytecode = True
from reincarnated.simulation.kc2 import threat
def f64(x): return None if x is None else 'f64:' + struct.pack('>d', float(x)).hex()
def unhex(h): return None if h is None else struct.unpack('>d', bytes.fromhex(h))[0]
FIELDS = ["oa", "da", "pth_in", "roll", "pth_effective", "hit", "damage_multiplier", "crit_tier"]
FLOATS = {"oa", "da", "pth_in", "pth_effective", "damage_multiplier"}
def rowstr(r):
    a = [r["section"], r["row_id"]] + [f64(r[k]) if k in FLOATS and r[k] is not None else r[k] for k in FIELDS]
    return json.dumps(a, separators=(',', ':'), ensure_ascii=False)
def rowset(rows):
    return hashlib.sha256("\n".join(rowstr(r) for r in sorted(rows, key=lambda r: (r["section"], r["row_id"]))).encode()).hexdigest()
frozen = [json.loads(l) for l in open(os.path.join(GRID, 'oracle/G1H.jsonl'))]
inp = json.load(open(os.path.join(GRID, 'inputs.json')))['rows']
dr = json.load(open(os.path.join(GRID, 'draws/HITGRID_s0.json')))
streams = dr.get('streams') or {}
entries = list(streams.values())[0] if streams else dr['entries']
def compute():
    out = []
    for i, row in enumerate(sorted(inp, key=lambda r: r['row_id'])):
        e = entries[i]; assert e[2] == 'randint' and list(e[3]) == [1, 100] and e[1] == row['row_id']
        roll = int(e[4])
        if row['section'] == 'R':
            oa = da = None; pth = unhex(row['pth_in_f64'])
        else:
            oa, da = unhex(row['oa_f64']), unhex(row['da_f64']); pth = threat.probability_to_hit(oa, da)
        hit, mult, tier = threat.resolve_hit(pth, roll)
        out.append({"section": row['section'], "row_id": row['row_id'], "oa": oa, "da": da, "pth_in": pth, "roll": roll,
                    "pth_effective": max(pth, threat.PTH_MINIMUM), "hit": bool(hit), "damage_multiplier": float(mult), "crit_tier": int(tier)})
    return out
base = compute()
saved = threat.PTH_MINIMUM; threat.PTH_MINIMUM = 5.0
ctl = compute(); threat.PTH_MINIMUM = saved
bmap = {(r['section'], r['row_id']): rowstr(r) for r in base}
red = sum(1 for r in ctl if rowstr(r) != bmap[(r['section'], r['row_id'])])
print(json.dumps({"threat_py_sha256": hashlib.sha256(open(threat.__file__, 'rb').read()).hexdigest(),
  "rowset_of_frozen_G1H": rowset(frozen), "rowset_recomputed": rowset(base), "n_rows": len(base),
  "frozen_vs_recomputed_rows_equal": sorted(map(rowstr, frozen)) == sorted(map(rowstr, base)),
  "NC_H1_pth_minimum_5_red": red, "NC_H1_control_rowset": rowset(ctl)}, indent=1))
