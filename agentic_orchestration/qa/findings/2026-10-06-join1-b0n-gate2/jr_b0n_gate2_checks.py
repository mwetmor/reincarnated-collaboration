"""jack-ryan · JOIN-1 B0-N Gate-2 — the independent checks, in one re-runnable instrument.

Read-only on every repo and on corpus.db. Writes only to <out_dir>. Derives every figure the finding quotes;
nothing is relayed from the README under review.

Inputs (all paths absolute):
  JR      = the reviewer's scratch dir holding the re-runs (R2, NCB1, R3F32 emitted with gamora's committed harness,
            engine 6d0240e3, from bindings PREPARED BY THE REVIEWER from a scratch corpus the reviewer built:
            corpus.db.pre-js4b-stamping backup (FILE 0d73475a…) + the two committed stamping SQLs), plus the
            s47 re-runs (sealed worktree 969fbd8d and mainline HEAD) and the 591-record compile outputs.
Run:  python3 jr_b0n_gate2_checks.py <JR> <out_json>
"""
from __future__ import annotations

import gzip
import hashlib
import importlib.util
import json
import os
import sqlite3
import sys
from collections import Counter

JR, OUT = sys.argv[1], sys.argv[2]
ENG = "/Users/admin/Games/reincarnated-engine"
COL = "/Users/admin/Games/reincarnated-collaboration"
GAM = f"{COL}/agentic_orchestration/gamora/analyses/2026-10-06-join1-b0n-numeric-selfjoin"
FIX = f"{ENG}/src/reincarnated/simulation/output/join1-gm-fixture-v1/oracle"
CUR = f"{COL}/agentic_orchestration/research/curated"
rep: dict = {}


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


# ── 1. J-S8 manifest pin + corpus digests + J-S4b ROWSETs under the stamping generator's own law ──
rep["js8_manifest_FILE_sha256"] = sha(f"{FIX}/manifest.json")
spec = importlib.util.spec_from_file_location(
    "st", f"{ENG}/src/reincarnated/simulation/scripts/gamora_join1_js4b_rule_stamping_2026_10_06.py")
st = importlib.util.module_from_spec(spec)
spec.loader.exec_module(st)
rows = {}
for name, f in [("pre_stamp_backup", f"{CUR}/corpus.db.pre-js4b-stamping-20261006T231654Z-backup"),
                ("reviewer_laneP", f"{JR}/laneP.db"),
                ("gamora_laneP", f"{JR}/../b0n/corpus2/corpus_laneP.db"),
                ("LIVE_corpus_of_record", f"{CUR}/corpus.db")]:
    c = sqlite3.connect(f"file:{f}?mode=ro", uri=True)
    rows[name] = {"FILE_sha256": sha(f), "js4b_ROWSET": st.rowset(c, "gd-eor-warlord-referent"),
                  "sibling_ROWSET": st.rowset(c, "gd-eor-warlord")}
    c.row_factory = None
    rows[name]["rctxgeo_desc_has_amendment"] = bool(c.execute(
        "select instr(description,'SCOPE AMENDMENT 2026-10-06') from normalization_rule where rule_id='R-CTX-GEO'"
    ).fetchone()[0])
    rows[name]["js4b_stamped_rows"] = c.execute(
        "select rule_id, count(*) from kit_numeric where kit_id='gd-eor-warlord-referent' and rule_id is not null "
        "group by 1").fetchall()
rep["corpora"] = rows

# ── 2. coverage: all 104 record rows bound / disposed / derived (gamora R1 table vs the corpus) ──
t = json.load(open(f"{GAM}/runs/R1/binding_table.json"))
bound = {k for b in t["bindings"] for k in b["record_rows"]}
unb = {x["numeric_key"]: x["disposition"] for x in t["record_rows_unbound"]}
der = set(t["derived_check_rows"])
c = sqlite3.connect(f"file:{CUR}/corpus.db.pre-js4b-stamping-20261006T231654Z-backup?mode=ro", uri=True)
rec = {r[0] for r in c.execute("select numeric_key from kit_numeric where kit_id='gd-eor-warlord-referent'")}
rep["coverage"] = {"record_rows": len(rec), "bound": len(bound), "unbound": len(unb), "derived": len(der),
                   "union_equals_record": (bound | set(unb) | der) == rec,
                   "overlaps": len(bound & set(unb)) + len(bound & der) + len(set(unb) & der),
                   "unbound_dispositions": dict(Counter(unb.values())),
                   "UNDISPOSED": [k for k, d in unb.items() if d == "UNDISPOSED"]}

# ── 3. reviewer re-runs vs J-S8 and vs gamora's runs (ROWSET per grain) ──
runs = {}
for r, g in [("R2", "R2"), ("NCB1", "NCB1"), ("R3F32", None)]:
    mine = json.load(open(f"{JR}/{r}/compare.json"))
    e = {"reproduces_all_7": mine["reproduces_all_7"],
         "grain_rowset_equal_to_JS8": {k: v["rowset_equal"] for k, v in mine["grains"].items()},
         "manifest_obs1": {k: v for k, v in json.load(open(f"{JR}/{r}/run/manifest.json"))["obs1_completeness"].items()
                           if k in ("n_complete", "n_cells", "truncated_or_failed")}}
    if g:
        theirs = json.load(open(f"{GAM}/runs/{g}/compare.json"))
        e["rowset_equal_to_gamora_run"] = {k: mine["grains"][k]["rowset_run"] == theirs["grains"][k]["rowset_run"]
                                           for k in mine["grains"]}
        mb = json.load(open(f"{JR}/{r}/bindings.json"))["bindings"]
        tb = json.load(open(f"{GAM}/runs/{g}/bindings.json"))["bindings"]
        e["bindings_identical_to_gamora"] = mb == tb
    for gg in ("G4", "G5"):
        if not mine["grains"][gg]["rowset_equal"]:
            e[gg] = {k: mine["grains"][gg].get(k) for k in ("cells_differing", "n_bodies_in_disc_sum_run",
                                                              "terminal_wave_flips", "terminal_reason_flips")}
    runs[r] = e
rep["reviewer_runs"] = runs


def load_g4(d):
    p = os.path.join(d, "G4.jsonl")
    data = open(p).read() if os.path.exists(p) else gzip.open(p + ".gz", "rt").read()
    return {(x["arm"], x["salt"], x["tick"]): x for x in map(json.loads, data.splitlines())}


R, X = load_g4(FIX), load_g4(f"{JR}/NCB1/run")
dirn = Counter()
for cell in sorted({k[:2] for k in R}):
    for tk in sorted(k[2] for k in R if k[:2] == cell):
        a, b = R[cell + (tk,)], X.get(cell + (tk,))
        if b is None or any(a[f] != b[f] for f in a):
            d = (b or a)["n_bodies_in_disc"] - a["n_bodies_in_disc"]
            dirn["up" if d > 0 else "down" if d < 0 else "equal"] += 1
            break
rep["ncb1_first_divergence_direction"] = dict(dirn)

# ── 4. P4 scored from gamora's committed probes (the prediction list is the math note's, verbatim) ──
pr = json.load(open(f"{GAM}/runs/R2/probes.json"))["probes"]
pred_r = ["B-01", "B-03", "B-12", "B-14", "B-15", "B-17", "B-24", "B-25", "B-31", "B-34", "B-35"]
pred_n = ["B-09", "B-10", "B-11", "B-08", "B-28", "B-29"]
rep["P4"] = {"predicted_reached_hit": [b for b in pred_r if pr[b]["verdict"] == "REACHED"],
             "predicted_reached_miss": [b for b in pred_r if pr[b]["verdict"] != "REACHED"],
             "predicted_not_reached_held": [b for b in pred_n if pr[b]["verdict"] == "NOT-REACHED"],
             "probe_reached_all": [b for b, v in pr.items() if v["verdict"] == "REACHED"]}
rep["P4"]["score"] = f'{len(rep["P4"]["predicted_reached_hit"])}/{len(pred_r)}'

# ── 5. s4.7: canonical equality (wall_s excluded) of four graded V311-FULL outputs + vs pass-4 artifact ──
def canon(p):
    def s(o):
        if isinstance(o, dict):
            return {k: s(v) for k, v in o.items() if k != "wall_s"}
        if isinstance(o, list):
            return [s(x) for x in o]
        return o
    return hashlib.sha256(json.dumps(s(json.load(open(p))), sort_keys=True, separators=(",", ":")).encode()).hexdigest()


s47 = {"reviewer_sealed_969fbd8d": f"{JR}/s47_sealed/graded_V311-FULL.sealed.json",
       "reviewer_HEAD": f"{JR}/s47_head/graded_V311-FULL.rerun.json",
       "gamora_sealed": f"{GAM}/s47/graded_V311-FULL.sealed969fbd8d.json",
       "gamora_HEAD_faf59dd2": f"{GAM}/s47/graded_V311-FULL.rerun.json",
       "pass4_artifact_of_record": f"{COL}/agentic_orchestration/gamora/analyses/2026-10-02-kc2-v3p11-oracle-pass4/graded_V311-FULL.json"}
rep["s47_canonical"] = {k: canon(v) for k, v in s47.items()}
ev = json.load(open(f"{JR}/s47_head/s47_evidence.json"))
rep["s47_reviewer_HEAD_closure"] = {k: v for k, v in ev["closure"].items() if k != "files_not_tracked"}
rep["s47_instrument_verdict_field"] = ev["verdict"]

# ── 6. KC-1 blast radius: reviewer's 591-record compile, ccd89e38^ vs ccd89e38, corpus 0d73475a ──
a, b = json.load(open(f"{JR}/all_old.json")), json.load(open(f"{JR}/all_new.json"))
moved = {k: {"element": [a[k]["element"], b[k]["element"]], "notes_len": [len(a[k]["notes"]), len(b[k]["notes"])]}
         for k in a if a[k] != b[k]}
rep["kc1_compile_diff"] = {"n_records": len(a), "n_differ": len(moved), "moved": moved,
                           "compile_errors": [len([1 for v in d.values() if isinstance(v, str)]) for d in (a, b)]}

# ── 7. the GD family table KC-1 collides with (sealed oracle) ──
sys.path.insert(0, "/Users/admin/Games/reincarnated-engine-join1-v311/src")
from reincarnated.simulation.kc2 import threat as th  # noqa: E402  (read-only import of the sealed tree)
rep["sealed_RESIST_PCT"] = {k: th.RESIST_PCT[k] for k in ("Physical", "Pierce", "Bleeding", "Fire")}

# ── 8. finding (ii): the live armour operand in J-S8 G2 is per-region (I-24), and armour BINDS ──
br, regions = Counter(), Counter()
for line in gzip.open(f"{FIX}/G2.jsonl.gz", "rt"):
    x = json.loads(line)
    if x["family"] in ("Physical", "SlowPhysical"):
        br["any_overflow" if "overflow" in x["armour_branch"] else "all_absorb"] += 1
        for reg in x["regions"]:
            regions[(reg[0], reg[1])] += 1
rep["G2_physical_armour"] = {"branch": dict(br),
                             "distinct_region_armour_values": sorted({f"{r}={v}" for (r, v) in regions}),
                             "aggregate_3557_used_as_a_region_value": any(abs(v - 3557.0) < 1e-9 for (_, v) in regions)}

json.dump(rep, open(OUT, "w"), indent=1, default=str)
print(json.dumps({k: rep[k] for k in ("coverage", "P4", "ncb1_first_divergence_direction")}, indent=1))
