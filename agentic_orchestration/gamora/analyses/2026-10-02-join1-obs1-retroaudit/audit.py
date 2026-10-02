import json, sys, gzip, os
CAP = 4000 * (326.530612244898 / 4000)
def load(p):
    op = gzip.open if p.endswith(".gz") else open
    with op(p, "rt") as fh: return json.load(fh)
def summ_check(S, path):
    salts = S.get("salts"); N = len(salts) if isinstance(salts, list) else None
    out = {"path": path, "N": N, "kind": "summary"}
    pw = S.get("per_wave") or {}
    if isinstance(pw, str): out["note"] = "per_wave stringified"; return out
    missing = [w for w in range(151, 161) if str(w) not in pw and w not in pw]
    out["waves_missing_entirely"] = missing
    T = S.get("t_s_151_159")
    if N and T is not None and not missing:
        tot = sum(float((pw.get(str(w)) or pw.get(w))["mean_t_s"]) for w in range(151, 160)) * N
        out["W9_excess_s"] = round(tot - float(T), 3)
        out["W9_tol_s"] = round(N * 9 * 0.005 + 0.011, 3)
        out["W9_truncated"] = (tot - float(T)) > out["W9_tol_s"]
    i311 = (S.get("instruments311") or {}).get("time_into_w160") if isinstance(S.get("instruments311"), dict) else None
    if i311:
        ps = i311["per_salt"]
        out["w160_missing_salts"] = [salts[i] for i, x in enumerate(ps) if x is None]
        out["w160_survivor_t_s"] = [x["t_s"] for x in ps if x and not x["died"]]
        out["w160_timeout_stall_salts"] = [salts[i] for i, x in enumerate(ps) if x and not x["died"] and x["t_s"] >= CAP - 0.1]
    out["raised"] = S.get("raised")
    out["n_survive_160"] = S.get("n_survive_160")
    return out
def rows_check(D, path):
    rows = D["rows"]
    seat = [r for r in rows if isinstance(r, dict) and 151 <= int(r.get("wave", 0)) <= 160]
    waves = [int(r["wave"]) for r in seat]
    return {"path": path, "kind": "rows", "n_rows_151_160": len(seat), "complete": waves == list(range(151, 161)),
            "last_wave": waves[-1] if waves else None, "raised": D.get("raised"),
            "terminal": D.get("leg_a_terminal")}
def walk(o, path, found):
    if isinstance(o, dict):
        if "per_salt_ratio" in o and "per_wave" in o and "salts" in o:
            found.append(summ_check(o, path))
        if isinstance(o.get("rows"), list) and o["rows"] and isinstance(o["rows"][0], dict) and "wave" in o["rows"][0]:
            found.append(rows_check(o, path))
        if isinstance(o.get("extra"), dict) and "n_rows_151_159" in o["extra"]:
            found.append({"path": path, "kind": "j0_extra", "n_rows_151_159": o["extra"]["n_rows_151_159"],
                          "expected": 9 * len(o.get("salts", []))})
        for k, v in o.items(): walk(v, f"{path}/{k}", found)
    elif isinstance(o, list):
        for i, v in enumerate(o): walk(v, f"{path}[{i}]", found)
res = {}
for p in sys.argv[2:]:
    try:
        found = []; walk(load(p), "", found); res[p] = found
    except Exception as e:
        res[p] = [{"error": repr(e)}]
json.dump(res, open(sys.argv[1], "w"), indent=1, default=str)
for p, f in res.items():
    kinds = {}
    bad = []
    for x in f:
        kinds[x.get("kind", "err")] = kinds.get(x.get("kind", "err"), 0) + 1
        if x.get("error") or x.get("waves_missing_entirely") or x.get("W9_truncated") or x.get("w160_missing_salts") \
           or x.get("w160_timeout_stall_salts") or x.get("raised") or (x.get("kind") == "rows" and not x["complete"]) \
           or (x.get("kind") == "j0_extra" and x["n_rows_151_159"] != x["expected"]):
            bad.append({k: v for k, v in x.items() if k not in ("w160_survivor_t_s",)})
    print(f"{os.path.relpath(p, '/Users/admin/Games/reincarnated-collaboration/agentic_orchestration')}: {kinds} FLAGS={len(bad)}")
    for b in bad[:6]: print("    ", json.dumps(b, default=str)[:400])
