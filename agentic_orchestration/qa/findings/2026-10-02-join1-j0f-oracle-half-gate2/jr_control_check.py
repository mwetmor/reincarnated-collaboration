"""jack-ryan, J0-F Gate-2: re-check the control runs' recorded outputs against the frozen fixture,
per cell and per grain, independently of gamora's cmp.py. Reads only the stored grain files.

usage: python3 jr_control_check.py <frozen_dir> <control_dir> [<control_dir> ...]
"""
import gzip, json, sys, pathlib, collections


def load(d):
    d = pathlib.Path(d)
    m = json.loads((d / "manifest.json").read_text())
    g = {}
    for name, info in m["grains"].items():
        p = d / info["file"]
        b = p.read_bytes()
        if p.suffix == ".gz":
            b = gzip.decompress(b)
        rows = [json.loads(x) for x in b.decode().splitlines() if x]
        by = collections.defaultdict(list)
        for r in rows:
            by[(r["arm"], r["salt"])].append(r)
        for k in by:
            by[k].sort(key=lambda r: tuple(r[c] for c in m["schema"][name]["key"]))
        g[name] = by
    return m, g


fm, fg = load(sys.argv[1])
cells = sorted({k for by in fg.values() for k in by})
for cd in sys.argv[2:]:
    cm, cg = load(cd)
    red = collections.Counter()
    firsts = {}
    beyond_nonzero = 0
    tick_order_ok = 0
    for c in cells:
        fd = {}
        for gname in fg:
            a, b = fg[gname].get(c, []), cg[gname].get(c, [])
            if a != b:
                red[gname] += 1
                i = next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
                fd[gname] = (a[i]["tick"] if i < len(a) and "tick" in a[i] else
                             (b[i]["tick"] if i < len(b) and "tick" in b[i] else None))
        beyond_nonzero += sum(1 for r in cg["G4"].get(c, []) if r["n_bodies_halted_beyond_d_engage"])
        if "G4" in fd and (("G1" not in fd) or (fd["G4"] is not None and fd["G1"] is not None and fd["G4"] <= fd["G1"])):
            tick_order_ok += 1
        firsts[f"{c[0]}|{c[1]}"] = fd
    o1 = cm.get("obs1_completeness", {})
    reasons = collections.Counter(r["terminal_reason"] for c in cells for r in cg["G5"].get(c, []))
    print(json.dumps({"control_dir": cd, "status": cm["status"], "emitter": cm["emitter"]["FILE_sha256"][:12],
                      "red_cells_per_grain": dict(red), "g4_beyond_nonzero_rows": beyond_nonzero,
                      "g4_first_div_tick_le_g1_or_g1_green": tick_order_ok,
                      "obs1": f"{o1.get('n_complete')}/{o1.get('n_cells')}",
                      "g5_reasons": dict(reasons),
                      "sample_first_div_ticks": {k: firsts[k] for k in list(firsts)[:10]}}, indent=1))
