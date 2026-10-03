"""jack-ryan H-5: KP-213 every-image corrigendum — does the instrument close a path ONLY when some image carries
every consumed column, cell-equal, and would it catch a second image that lacks one? Run on a committed POST
capture against the written v3.11 pack (and in-memory tampered copies of it). Read-only on the pack bytes."""
import copy, json, os, sys
from reincarnated.export.kc2_baton_v3p4p2_emit import _load_pack
from reincarnated.export import kc2_v3p11_closure as C
from reincarnated.export import kc2_v3p7_inputs as I
from reincarnated.export import kc2_v3p7p1_law as L
OUT = C.OUT_ROOT
MD, RD = "kc2-model-pack-v3-E-s09-cp150-mech-v3p11-20261002_192143", "kc2-reference-pack-v3-E-s09-cp150-mech-v3p11-20261002_192143"
model, mv = _load_pack(MD, "99711727"); ref, rv = _load_pack(RD, "af58ef40")
assert mv["recomputed_pack_digest"].startswith("99711727") and rv["recomputed_pack_digest"].startswith("af58ef40")
cap_name = sys.argv[1] if len(sys.argv) > 1 else "kc2-v3p11-POST-capture-M0-hs0-20261002_192143.json"
cap = json.load(open(os.path.join(OUT, cap_name), encoding="utf-8"))
MULTI = ("data/kc2/pm2_tg2_monster_timing.csv", "data/kc2/pm4i_wave_damage_modifier.csv")

def summary(model_, law="every"):
    idx = I.PackIndex(model_, ref)
    t = C.closure_table(cap, model_, ref, idx=idx) if law == "every" else C.closure_table_v3p7p1_literal(cap, model_, ref, idx=idx)
    v = L.v127p1_closure(t)
    rows = {r["rel"]: {"status": r["status"], "row": r.get("row"), "why": r.get("why"), "how": r.get("how")}
            for r in t["files"] if r.get("rel") in MULTI}
    return {"V-127p1_violations": v["n_violations"], "multi_image_rows": rows}

def find(m, rid):
    def w(o):
        if isinstance(o, dict):
            if o.get("id") == rid: return o
            for x in o.values():
                r = w(x)
                if r is not None: return r
        elif isinstance(o, list):
            for x in o:
                r = w(x)
                if r is not None: return r
    return w(m)

consumed = cap["csv_columns"]
def cols_for(rel):
    for k, v in consumed.items():
        if k.endswith(rel):
            return v
    return None
out = {"capture": cap_name, "consumed_cols": {rel: cols_for(rel) for rel in MULTI}}
out["A_untampered_every_image"] = summary(model)
out["B_untampered_v3p7p1_literal_first_image"] = summary(model, law="first")
# C: the newer (complete) pm2_tg2 image loses one consumed column the older image also lacks
old = find(model, "IC7-F-22")["value"]["columns"]
cc = cols_for(MULTI[0]) or {}
use = cc.get("cols") if isinstance(cc, dict) else None
cand = [c for c in (use or []) if c not in old]
m2 = copy.deepcopy(model)
img = find(m2, "IC7-F-V311-04")["value"]
drop = cand[0] if cand else None
if drop:
    j = img["columns"].index(drop)
    img["columns"].pop(j)
    for row in img["cells"]:
        row.pop(j)
out["C_second_image_lacks_consumed_column"] = {"dropped": drop, **summary(m2)}
# D: one consumed cell of the newer pm4i image altered
m3 = copy.deepcopy(model)
img = find(m3, "IC7-F-V311-05")["value"]
cc4 = cols_for(MULTI[1]) or {}
use4 = cc4.get("cols") if isinstance(cc4, dict) else img["columns"]
old4 = find(model, "IC7-F-37")["value"]["columns"]
col = [c for c in use4 if c not in old4][0]
j = img["columns"].index(col)
img["cells"][3][j] = img["cells"][3][j] + "1"
out["D_second_image_one_consumed_cell_altered"] = {"column": col, **summary(m3)}
print(json.dumps(out, indent=1, ensure_ascii=False, default=str))
