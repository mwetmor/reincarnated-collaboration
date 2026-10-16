"""JOIN-1 J4b rows 23 / 24 on the --rb-row2324-trace arms, graded against engine 6587ffe8 (gamora, 2026-10-16).

usage: python3 r2324_grade.py <d2_primary_dir> <dot_gd_dir> <chill_off_dir> <car2_dir> <out.json>
Each dir holds <ARM>-join/{J4B-ROWS-*.json, DRIVE.jsonl, GDDOT.jsonl} (the trace files may sit in <ARM>-join or <ARM>).
Row 23: d2 per application = rate x len_eff for a 'replace' row (the applied length, post-resist), rate x 1 for an
'ignore_one_frame' row (car2 / traced-primary `dots` rows); gd per application = GDDOT d_effective (post-table), at
the same mitigation stage (post_resist required, else NO VERDICT). Per-cell mean; paired over cells, d2 <= gd.
Row 24: moving tick = d > 0 in DRIVE; per-cell mean d over moving ticks; d2 <= off. Row identity on chilled ticks.
"""
import glob, importlib.util, json, math, os, sys

W = "/Users/admin/Games/reincarnated-engine-j4b-cert"
spec = importlib.util.spec_from_file_location("g", W + "/src/reincarnated/simulation/scripts/gamora_join4b_grade.py")
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
PRIM, DOT, CHILL, CAR2, OUT = sys.argv[1:6]
ARMS = ("M0", "M-POL-2", "M-POL-2-NULL", "W1", "W1-NULL")


def trace(base, name):
    rows = []
    for A in ARMS:
        for sub in ("-join", ""):
            p = f"{base}/{A}{sub}/{name}.jsonl"
            if os.path.exists(p):
                rows += [json.loads(l) for l in open(p) if l.strip()]
                break
    return rows


def dots(base):
    out = {}
    for p in glob.glob(f"{base}/*-join/J4B-ROWS-*.json"):
        d = json.load(open(p)); out[f"{d['arm']}|{d['salt']}"] = d.get("dots", [])
    return out


res = {}
# identity of the traced primary's J4B-ROWS dots with car2's
dp, dc = dots(PRIM), dots(CAR2)
res["traced_primary_dots_equal_car2"] = dp == dc

# ── row 23 ──
d2 = {}
for k, rows in dp.items():
    vals = []
    for r in rows:
        fr, tk, dec, form, fam, aid, total, len_f, len_eff, rate = r[:10]
        vals.append(rate * len_eff if dec == "replace" else rate * 1.0)
    d2[k] = (sum(vals) / len(vals)) if vals else None
gd_rows = trace(DOT, "GDDOT")
stages = sorted({r.get("mitigation_stage") for r in gd_rows})
gd, base_eq = {}, {"n_rows": len(gd_rows), "n_equal": 0, "max_abs_diff": 0.0}
by = {}
for r in gd_rows:
    by.setdefault(f"{r['arm']}|{r['salt']}", []).append(r)
    diff = abs(r["d_base"] - r["d_effective"]); base_eq["max_abs_diff"] = max(base_eq["max_abs_diff"], diff)
    base_eq["n_equal"] += r["d_base"] == r["d_effective"]
for k, rr in by.items():
    gd[k] = sum(r["d_effective"] for r in rr) / len(rr)
gd_base = {k: sum(r["d_base"] for r in rr) / len(rr) for k, rr in by.items()}
row23 = {"mitigation_stages_in_GDDOT": stages, "d_base_vs_d_effective": base_eq,
         "n_applications": {"d2": sum(len(v) for v in dp.values()), "gd": len(gd_rows)}}
if stages != ["post_resist"]:
    row23["verdict"] = "NO VERDICT (gd mitigation stage not post_resist / undeterminable)"
else:
    both = sorted(k for k in d2 if d2[k] is not None and gd.get(k) is not None)
    row23["cells_paired"] = len(both)
    row23["dropped"] = sorted(set(list(d2) + list(gd)) - set(both))
    if len(both) < 6:
        row23["verdict"] = f"NO VERDICT ({len(both)} pairs)"
    else:
        row23.update(g.paired({k: d2[k] for k in both}, {k: gd[k] for k in both}, direction="<="))
        row23["printed_pre_diminish_base"] = g.paired({k: d2[k] for k in both}, {k: gd_base[k] for k in both},
                                                      direction="<=")
res["row23"] = row23

# ── row 24 ──
def drive_stats(base):
    rows = trace(base, "DRIVE")
    per, viol, n_chilled, landings = {}, [], 0, {}
    prev = {}
    for r in rows:
        k = f"{r['arm']}|{r['salt']}"
        s = per.setdefault(k, [0.0, 0])
        if r["d"] > 0:
            s[0] += r["d"]; s[1] += 1
        if r["chilled"]:
            n_chilled += 1
            if not prev.get(k):
                landings[k] = landings.get(k, 0) + 1
        prev[k] = r["chilled"]
        # row identity: displacement == scale x proposed whenever she moves; scale 0.5 (or floored >= 0.25) on chill
        if r["d"] > 0:
            want = (r["scale"] * r["proposed_dx"], r["scale"] * r["proposed_dy"])
            ok = (math.isclose(r["dx"], want[0], rel_tol=1e-12, abs_tol=1e-15)
                  and math.isclose(r["dy"], want[1], rel_tol=1e-12, abs_tol=1e-15)
                  and math.isclose(r["d"], math.hypot(r["dx"], r["dy"]), rel_tol=1e-12, abs_tol=1e-15)
                  and ((0.25 <= r["scale"] <= 0.5) if r["chilled"] else r["scale"] == 1.0))
            if not ok and len(viol) < 20:
                viol.append(r)
            elif not ok:
                viol.append(None)
    return {k: (v[0] / v[1] if v[1] else None) for k, v in per.items()}, len(viol), n_chilled, landings, len(rows)

m2, v2, c2, l2, n2 = drive_stats(PRIM)
mo, vo, co, lo, no = drive_stats(CHILL)
both = sorted(k for k in m2 if m2[k] is not None and mo.get(k) is not None)
row24 = {"rows": {"d2": n2, "off": no}, "row_identity_violations": {"d2": v2, "off": vo},
         "chilled_ticks": {"d2": c2, "off": co}, "chill_landings_on_her": {"d2": sum(l2.values()), "off": sum(lo.values()),
                                                                           "d2_cells_with_any": len(l2)},
         "cells_paired": len(both)}
if sum(l2.values()) == 0:
    row24["verdict"] = "REACHED-INSENSITIVE (no chill reached her in any cell)"
elif len(both) < 6:
    row24["verdict"] = f"NO VERDICT ({len(both)} pairs)"
else:
    row24.update(g.paired({k: m2[k] for k in both}, {k: mo[k] for k in both}, direction="<="))
res["row24"] = row24
json.dump(res, open(OUT, "w"), indent=1, default=str)
print(json.dumps(res, default=str)[:3000])
