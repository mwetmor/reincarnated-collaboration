"""JOIN-1 J4b tier-2: grade ONE arm against its REGISTERED prediction (gamora, 2026-10-15). Read-only.

usage: python3 t2_grade.py <arm> <out.json>
Reference: the corrected car2 primary. Grader functions: gamora_join4b_grade.py (0ab979a7) imported from the cert
worktree; replay: gamora_join4b_row_replay_2026_10_15.py at engine 98e22f2f (r_DMG / r_HP bound per arm).
"""
import collections, glob, hashlib, importlib.util, json, os, subprocess, sys

ARM_NAME, OUT = sys.argv[1], sys.argv[2]
W = "/Users/admin/Games/reincarnated-engine-j4b-cert"
SP = "/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/ac232ef8-034a-45e4-8e9f-65834cd599f9/scratchpad"
T2 = "/Users/admin/Games/join3c-bulk/t2"
PRIM = "/Users/admin/Games/join3c-bulk/car2/primary"
PACK = W + "/src/reincarnated/output/kc2-rulebook-pack-v5.1-20261015_134952"
TAPES = "/Users/admin/Games/join3a-bulk-evidence/j4b-tapes-4e6ed5b3"
OPS = ("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/"
       "2026-10-14-join1-c13-enemy-anchor/j4b_r_hp_arm_operands.json")
ARMS = ("M0", "M-POL-2", "M-POL-2-NULL", "W1", "W1-NULL")
H = 40000
spec = importlib.util.spec_from_file_location("g", W + "/src/reincarnated/simulation/scripts/gamora_join4b_grade.py")
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
X = W + "/src/reincarnated/simulation/scripts/gamora_join4b_row_replay_2026_10_15.py"
rows = lambda p: [json.loads(l) for l in open(p) if l.strip()]
B = os.environ.get("T2_ARM_DIR", f"{T2}/{ARM_NAME}")
work = os.environ.get("T2_WORK", f"{SP}/t2grade/{ARM_NAME}")
os.makedirs(work + "/all", exist_ok=True)
out = {"arm": ARM_NAME}

# ── pins ──
pf = f"{B}/grains_sha256.json"
p = json.load(open(pf)); ok = 0
for k, (sz, v) in p.items():
    b = open(f"{B}/{k}", "rb").read(); ok += hashlib.sha256(b).hexdigest() == v and len(b) == sz
out["pins"] = {"pin_file": pf, "pin_file_sha256": hashlib.sha256(open(pf, "rb").read()).hexdigest(), "n": len(p), "ok": ok}

# ── assemble ──
def cat(dst, srcs):
    with open(dst, "wb") as f:
        for s in srcs:
            if os.path.exists(s):
                f.write(open(s, "rb").read())
for gname in ("G1", "G2", "G3", "G4", "G5", "G6", "G7"):
    cat(f"{work}/all/{gname}.jsonl", [f"{B}/{A}/{gname}.jsonl" for A in ARMS])
for gname in sorted({os.path.basename(x) for x in glob.glob(f"{B}/M0-join/*.jsonl")}):
    cat(f"{work}/all/{gname}", [f"{B}/{A}-join/{gname}" for A in ARMS])
for A in ARMS:
    d = f"{work}/arm_{A}"; os.makedirs(d, exist_ok=True)
    for s in glob.glob(f"{B}/{A}/G*.jsonl") + glob.glob(f"{B}/{A}-join/*.jsonl"):
        t = f"{d}/{os.path.basename(s)}"
        if not os.path.lexists(t):
            os.symlink(s, t)

# ── replay, bound per arm ──
bind = []
if ARM_NAME == "r2":
    bind = ["--r-hp-row", "anchor_r_hp_R2", "--r-hp-hex", "403d272050fb8969", "--r-hp-operands", OPS]
elif ARM_NAME == "nonladder":
    bind = ["--r-hp-row", "anchor_r_hp_nonladder", "--r-hp-hex", "404b079f4cb4c5d6", "--r-hp-operands", OPS]
bind += ["--r-dmg-row", "RB-A-anchor_r_dmg", "--r-dmg-hex", "4053a558dda37d80"]
if ARM_NAME.startswith("body-"):
    bind += ["--body-off", ARM_NAME[len("body-"):]]
rep = {"verdicts": [], "prov_mm": 0, "bad_by_class": collections.Counter(), "n_by_class": collections.Counter()}
for A in ARMS:
    o = f"{work}/replay_{A}.json"
    subprocess.run([sys.executable, X, "check", f"{B}/{A}-join", "--pack", PACK, "--l21", f"{B}/l21.json"
                    if os.path.exists(f"{B}/l21.json") else f"{PRIM}/l21.json", "--tapes", TAPES, *bind, "--out", o],
                   check=False, stdout=subprocess.DEVNULL)
    r = json.load(open(o)); rep["verdicts"].append(r["verdict"]); rep["prov_mm"] += len(r["provenance_mismatches"])
    rep["binding"] = {"r_dmg": r["params"]["r_dmg_binding"], "r_hp": r["params"]["r_hp_binding"]}
    for c in r["cells"].values():
        for cls, (n, b) in c["checks"].items():
            rep["n_by_class"][cls] += n; rep["bad_by_class"][cls] += b
out["replay"] = rep

# ── identity ──
worst, fails, falls = 0.0, [], 0
for A in ARMS:
    go = rows(f"{B}/{A}-join/GO.jsonl"); gb = rows(f"{B}/{A}-join/GO-BODIES.jsonl"); hc = rows(f"{B}/{A}-join/HPCHAIN.jsonl")
    heal = {r["salt"]: r["leech_heal_hp"] for r in hc}
    for s in range(5):
        app = sum(r["applied"] for r in go if r["salt"] == s)
        fall = sum(r["hp_initial"] - r["hp_final"] for r in gb if r["salt"] == s)
        rel = abs(app - fall - heal[s]) / max(1, app); worst = max(worst, rel)
        if rel > 1e-9:
            fails.append((A, s, rel))
    for pth in glob.glob(f"{B}/{A}-join/J4B-ROWS-*.json"):
        d = json.load(open(pth)); hp = {b["actor_id"]: b["hp_initial"] for b in gb if b["salt"] == d["salt"]}
        for pk in d["packets"]:
            t = pk["target_id"]; before = pk["hp_after"] + pk["applied"]
            if t in hp and before < hp[t] - 1e-9 * max(1, hp[t]):
                falls += 1
            hp[t] = pk["hp_after"]
out["identity"] = {"cells": 25, "worst_rel": worst, "fails": fails, "off_ledger_falls": falls}

# ── gates ──
run = g.load_run(work + "/all")
gates = {"runs": g.runs_gate(run), "obs1": g.obs1(run), "per_arm": {}}
for A in ARMS:
    ra = g.load_run(f"{work}/arm_{A}")
    e = g.effect_gates(ra, attack_mode="reset"); cr = g.completeness_restated(ra, kit="d2-fire-sorc-c14")
    orph = [o for v in cr.get("cells", {}).values() for o in v["orphans"]]
    gates["per_arm"][A] = {"effect": e["verdict"], "dot": g.dot_conservation(ra)["verdict"], "completeness": cr["verdict"],
                           "P": cr["precondition"]["verdict"], "orphans": len(orph),
                           "terminal": sum(o["terminal"] for o in orph)}
out["gates"] = gates

# ── metrics ──
prim = g.load_run(SP + "/car2/her")
# a cell that RAISED (a refusal) is a named result, never a silent drop: graded on the remaining cells
refused = {f"{r['arm']}|{r['salt']}": r["terminal_reason"] for r in run["G5"] if str(r["terminal_reason"]).startswith("raised")}
out["refused_cells"] = {k: pv_r for k, pv_r in refused.items()}
cells = sorted(c for c in prim["cells"] if g._key(c) not in refused)
out["n_cells_graded"] = len(cells)
mp = {c: g.cell_metrics(prim, c, H=H) for c in cells}
ma = {c: g.cell_metrics(run, c, H=H) for c in cells}
key = g._key


def prov(base):
    cs = {}
    for A in ARMS:
        cs.update(json.load(open(f"{base}/{A}-join/JOIN-PROVENANCE.json"))["cells"])
    return cs


def jrows(base):
    d = {}
    for pth in glob.glob(f"{base}/*-join/J4B-ROWS-*.json"):
        x = json.load(open(pth)); d[f"{x['arm']}|{x['salt']}"] = x
    return d


pv_a, pv_p = prov(B), prov(PRIM)
out["refused_cells"] = {k: {"terminal": v, "raised_reason": pv_a.get(k, {}).get("raised_reason")} for k, v in refused.items()}
cnt = lambda pv: {k: v["j4b_kit"]["counters"] for k, v in pv.items()}
ca, cp = cnt(pv_a), cnt(pv_p)
out["counters_total"] = {"arm": dict(sum((collections.Counter(v) for v in ca.values()), collections.Counter())),
                         "primary": dict(sum((collections.Counter(v) for v in cp.values()), collections.Counter()))}
out["unpredicted"] = {"M_a": {"arm": sum(m["survived"] for m in ma.values()), "primary": sum(m["survived"] for m in mp.values())},
                      "M_c_whole": {"arm": sum(m["M_c"] for m in ma.values()), "primary": sum(m["M_c"] for m in mp.values())}}
item = {}
K = [key(c) for c in cells]
if ARM_NAME in ("r2", "nonladder"):
    a = {c: ma[c]["offered_per_tick"] for c in cells}; pr = {c: mp[c]["offered_per_tick"] for c in cells}
    if ARM_NAME == "r2":
        item = dict(g.paired(a, pr, direction="<="), registered="offered per tick (RAW): R2 <= R1 (paired totals; ADDENDUM-A s C)")
    else:
        item = dict(g.paired(pr, a, direction="<="), registered="offered per tick (RAW): R1 <= non-ladder (paired totals; total_her = R1, total_him = non-ladder)")
    item["M_c_unordered"] = {"arm": out["unpredicted"]["M_c_whole"]["arm"], "R1": out["unpredicted"]["M_c_whole"]["primary"]}
elif ARM_NAME.startswith("body-"):
    a = {c: ma[c]["applied"] for c in cells}; pr = {c: mp[c]["applied"] for c in cells}
    th, ta = sum(pr.values()), sum(a.values())
    item = dict(g.paired(a, pr, direction="<="), registered="body off -> her sum damage dealt (sum applied, whole cell) falls, paired totals (base s 9; rows 11-14)")
    item["verdict"] = "TRUE" if ta < th else ("FALSE" if ta > th else "NOT FALLEN (tie)")
    src = {"body-fire_ball": ("fire_ball",), "body-meteor": ("meteor",), "body-pyre": ("meteorfire", "pyre"),
           "body-splash": None}[ARM_NAME]
    jr = jrows(B); n_src = collections.Counter(); app_src = collections.Counter()
    for x in jr.values():
        for pk in x["packets"]:
            n_src[pk.get("source")] += 1; app_src[pk.get("source")] += pk.get("applied", 0.0)
    item["signature_packets_by_source"] = {k: [n_src[k], app_src[k]] for k in n_src}
elif ARM_NAME == "block-gd":
    a = {c: ma[c]["intake"] for c in cells}; pr = {c: mp[c]["intake"] for c in cells}
    item = dict(g.paired(a, pr, direction=">="), registered="NC-J4b-BLOCK / NC-ROW19: sum intake higher with block off (gd 0.0) than d2, paired totals (A1 s C)")
    item["blocks"] = {"arm": out["counters_total"]["arm"].get("blocks"), "primary": out["counters_total"]["primary"].get("blocks")}
    item["block_draws"] = {"arm": out["counters_total"]["arm"].get("block_draws"), "primary": out["counters_total"]["primary"].get("block_draws")}
elif ARM_NAME in ("potion-gd", "potion-none"):
    def cps(m, pvc, k):
        return pvc[k]["casts"] / (m["ticks"] * 0.0816326530612245)
    a = {c: cps(ma[c], ca, key(c)) for c in cells}; pr = {c: cps(mp[c], cp, key(c)) for c in cells}
    surv = {"d2_belt": sum(m["survived"] for m in mp.values()), "arm": sum(m["survived"] for m in ma.values())}
    surv["verdict"] = "TRUE" if surv["d2_belt"] >= surv["arm"] else "FALSE"
    item = {"registered": "NC-ROW21: d2-belt >= " + ARM_NAME.split("-")[1] + " on survival and on realised casts/s in the mana-bound phase",
            "survival": surv,
            "casts_per_s": dict(g.paired(pr, a, direction=">="),
                                operationalisation="whole-cell casts/s (the mana-bound phase is not delimited in registration): POST-HOC")}
    item["drinks"] = {"arm": out["counters_total"]["arm"].get("potions"), "primary": out["counters_total"]["primary"].get("potions")}
elif ARM_NAME == "dot-gd":
    def per_app(base, run_, jr):
        res = {}
        gc = {f"{r['arm']}|{r['salt']}": r for r in (run_["GC"] or [])}
        for k in K:
            n = len(jr.get(k, {}).get("dots", [])) if jr.get(k) else 0
            res[k] = (gc[k]["landed"] / n) if (k in gc and n) else None
        return res
    jp, ja = jrows(PRIM), jrows(B)
    pa, aa = per_app(PRIM, prim, jp), per_app(B, run, ja)
    both = [k for k in K if pa[k] is not None and aa[k] is not None]
    item = {"registered": "NC-J4b-ROW23: per landed DoT application, intake d2 <= gd, paired over cells, sign test; totals NOT graded",
            "n_applications": {"d2": sum(len(x.get("dots", [])) for x in jp.values()), "gd": sum(len(x.get("dots", [])) for x in ja.values())},
            "cells_formable": len(both)}
    if both:
        item.update(g.paired({k: pa[k] for k in both}, {k: aa[k] for k in both}, direction="<="))
    else:
        item["verdict"] = "NO VERDICT (the gd arm carries no per-application rows)"
elif ARM_NAME == "chill-off":
    item = {"registered": "NC-J4b-ROW24: row identity on chilled ticks; per-moving-tick displacement d2 <= off, sign test",
            "verdict": "NO VERDICT: the contract carries no per-tick player displacement trace (NO-ARM-ITEMS s 2)",
            "chill_landings": {"arm": out["counters_total"]["arm"].get("fa_chill"), "primary": out["counters_total"]["primary"].get("fa_chill")}}
elif ARM_NAME == "resist-referent":
    def per_hit(run_, k):
        g1 = [r for r in run_["G1"] if f"{r['arm']}|{r['salt']}" == k and r.get("hit")]
        g3 = sum(r["intake_hp"] for r in run_["G3"] if f"{r['arm']}|{r['salt']}" == k)
        return g3 / len(g1) if g1 else None
    pr = {k: per_hit(prim, k) for k in K}; a = {k: per_hit(run, k) for k in K}
    both = [k for k in K if pr[k] is not None and a[k] is not None]
    item = dict(g.paired({k: pr[k] for k in both}, {k: a[k] for k in both}, direction=">="),
                registered="NC row 25: paired sum intake per landed hit, hers >= the Warlord's RESIST_PCT map (A4 s 5)",
                metric="per cell: sum G3 intake_hp / landed G1 hits")
elif ARM_NAME == "static-off":
    jr = jrows(B)
    n = sum(1 for x in jr.values() for pk in x["packets"] if "static" in str(pk.get("source")))
    item = {"registered": "row 28: 'off' gives zero Static packets", "static_packets": n,
            "static_casts": out["counters_total"]["arm"].get("static_casts"),
            "verdict": "TRUE" if n == 0 else "FALSE"}
out["item"] = item
json.dump(out, open(OUT, "w"), indent=1, default=str)
print(json.dumps({"arm": ARM_NAME, "pins": out["pins"]["ok"], "replay": rep["verdicts"], "prov_mm": rep["prov_mm"],
                  "bad": {k: v for k, v in rep["bad_by_class"].items() if v}, "ident": out["identity"]["worst_rel"],
                  "falls": falls, "item": {k: v for k, v in item.items() if k not in ("registration_caveats",)}}, default=str)[:3000])
