"""jack-ryan H-5 (runtime side): every pack KEY the v3.8-v3.11 fold code names ("module.NAME" strings, k3/k12/d4/a8
callee keys, oi1/rg1/il1/dc1/cg1 row ids, IC7-* ids) must exist as a row in pack v3.11. Lists each with its row id(s)."""
import json, os, re, sys
RT, M = sys.argv[1], sys.argv[2]
FILES = ["sim/kc2rt_gd_engage.gd", "sim/kc2rt_composition.gd", "sim/kc2rt_mutators.gd", "sim/kc2rt_lineup.gd",
         "sim/kc2rt_pilot_move.gd", "sim/kc2rt_arm_config.gd", "sim/kc2rt_contact_bridge.gd", "sim/kc2rt_roster.gd",
         "sim/kc2rt_fight.gd", "sim/kc2rt_board.gd", "sim/kc2rt_rng.gd", "sim/kc2rt_summons.gd", "sim/kc2rt_laws.gd",
         "loader/kc2rt_v3p8.gd", "loader/kc2rt_v3p11.gd"]
keys, ids = {}, {}
def walk(o, member):
    if isinstance(o, dict):
        if "id" in o and isinstance(o.get("id"), str):
            ids.setdefault(o["id"], member)
            for kk in ("key", "callee", "target", "prior_row"):
                if isinstance(o.get(kk), str):
                    keys.setdefault(o[kk], []).append(o["id"])
            v = o.get("value")
            if isinstance(v, dict):
                for kk in ("key", "callee", "site", "superseded_by_key"):
                    if isinstance(v.get(kk), str):
                        keys.setdefault(v[kk], []).append(o["id"])
        for x in o.values(): walk(x, member)
    elif isinstance(o, list):
        for x in o: walk(x, member)
for f in os.listdir(M):
    if f.endswith(".json"): walk(json.load(open(os.path.join(M, f), encoding="utf-8")), f)
allkeys = list(keys)
pat_key = re.compile(r'"((?:[a-z_0-9]+\.)+[A-Za-z_][A-Za-z_0-9]*(?:\.[A-Za-z_0-9]+)*(?:\([a-z_0-9]+\))?)"')
pat_id = re.compile(r'"((?:IC7|V3\d+|V39|V310|V311|V38)-[A-Z0-9-]+)"')
res = {"found": [], "missing": []}
for f in FILES:
    p = os.path.join(RT, f)
    if not os.path.exists(p): continue
    for i, line in enumerate(open(p, encoding="utf-8"), 1):
        code = line.split("#")[0] if not f.endswith(".cpp") else line
        for m in pat_key.finditer(code):
            k = m.group(1)
            if k.endswith((".json", ".csv", ".gd", ".py", ".md", ".txt")) or k.startswith(("res.", "user.")): continue
            hits = keys.get(k) or keys.get("reincarnated.simulation.kc2." + k) or keys.get("reincarnated.simulation." + k)
            if not hits:
                hits = [kk for kk in allkeys if kk.endswith("." + k) or kk.endswith(k)][:3]
            (res["found"] if hits else res["missing"]).append((f, i, k, (hits or [])[:3]))
        for m in pat_id.finditer(code):
            k = m.group(1)
            (res["found"] if k in ids else res["missing"]).append((f, i, k, [ids.get(k)]))
print("found", len(res["found"]), "missing", len(res["missing"]))
for r in res["missing"]: print("MISSING\t%s:%d\t%s" % r[:3])
json.dump(res, open(sys.argv[3], "w"), indent=0, default=str)
