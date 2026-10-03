"""jack-ryan H-5: re-run of star-lord's v3.11 closure proof OFF THE WRITTEN BYTES, on FRESH captures made by me
(stem kc2-v3p11-JR, tag argv[1]) in a scratch copy of engine 969fbd8d. Mirrors kc2_baton_v3p11_emit.cut()'s
post-write block (validate V-152..V-157, inertness, seeds, sweeps, predecessors, K-7) without writing any pack,
and adds: mutation-gate verdict census, EXEMPT-class census, NOT-IN-PACK strict per capture, a semantic
comparison of my closure tables against star-lord's committed POST tables (paths normalised)."""
import collections, copy, json, os, sys
from reincarnated.export import kc2_baton_v3p11_emit as EM
from reincarnated.export import kc2_v3p11_closure as C
from reincarnated.export import kc2_v3p11_rows as R
from reincarnated.export import kc2_v3p7_inputs as I
from reincarnated.export import kc2_v3p7p1_law as L
from reincarnated.export.kc2_baton_v3p4p2_emit import _load_pack
from reincarnated.export.kc2_baton_v3_schema import verify_pack_on_disk
from reincarnated.export.kc2_baton_v3p4_emit import verify_k7
sys.setrecursionlimit(10000)
TAG = sys.argv[1]; OUTP = sys.argv[2]
MD, RD = "kc2-model-pack-v3-E-s09-cp150-mech-v3p11-20261002_192143", "kc2-reference-pack-v3-E-s09-cp150-mech-v3p11-20261002_192143"
RECEIPT = json.load(open(os.path.join(C.OUT_ROOT, "kc2-baton-v3-cut-receipt-v3p11-20261002_192143.json"), encoding="utf-8"))
want_sha = RECEIPT["outputs"]["⚑ ROWSET_sha256"]
k7_pre = verify_k7()
written, wv = _load_pack(MD, "99711727"); written_ref, rv = _load_pack(RD, "af58ef40")
base, base_ref, _ = EM.load_base()
tree, hand = EM.with_hand(base)
caps, bares, files, sweeps = C.load_captures("kc2-v3p11-JR", TAG)
# ⚑ DECLARED NORMALISATION (instrument environment, not model): (1) the checkout path. The pack carries some
#   oracle-script constants whose VALUE is a host path of the checkout of record (/Users/admin/Games/
#   reincarnated-engine/...: e.g. IC7-K-V311-0075 ENGINE_SRC, -0067 W1_GLOB) as STRICT rows, so a re-run from any
#   other checkout differs on exactly those. The checkout root is rewritten in the constants' and composition
#   calls' VALUES only; file paths (opens, csv_columns, mutation scan) keep the scratch copy, which is what is read.
#   (2) CPython's importlib bytecode TEMP files (`__pycache__/<m>.cpython-312.pyc.<id>`, written then renamed when a
#   fresh copy compiles), which the audit hook's own `.pyc` filter is meant to skip but does not match.
import re as _re
_ROOT = I.ENGINE_ROOT
def _rew(o):
    if isinstance(o, str): return o.replace(_ROOT, "/Users/admin/Games/reincarnated-engine")
    if isinstance(o, list): return [_rew(x) for x in o]
    if isinstance(o, dict): return {k: _rew(v) for k, v in o.items()}
    return o
RAW = {}
NORM_LOG = {}
for _k, _c in list(caps.items()):
    RAW[_k] = _c
    _n = copy.deepcopy(_c)
    _n["constants"] = _rew(_n["constants"]); _n["composition_calls"] = _rew(_n.get("composition_calls") or [])
    _drop = [p for p in list(_n["opens"]) if _re.search(r"/__pycache__/[^/]+\.pyc\.\d+$", p)]
    for p in _drop: _n["opens"].pop(p)
    NORM_LOG[_k] = {"pyc_temp_opens_dropped": len(_drop),
                    "constants_rewritten": sum(1 for a, b in zip(json.dumps(_c["constants"], sort_keys=True, default=str).split(","), json.dumps(_n["constants"], sort_keys=True, default=str).split(",")) if a != b)}
    caps[_k] = _n
idx_w = I.PackIndex(written, written_ref)
tables = {k: C.closure_table(c, written, written_ref, idx=idx_w) for k, c in caps.items()}
fresh_post = C.derive(caps, sweeps, tree, base_ref)["rowsets"]
fresh_hand = R.derive(base)
off = EM.validate(written, written_ref, base=base, base_ref=base_ref, fresh=fresh_post, fresh_hand=fresh_hand,
                  tables=tables, sweeps=sweeps, want_sha=want_sha)
inert = C.inertness(caps, bares)
recon = C.reconcile(tables, caps, sweeps["0"], idx_w)
face_recon = written["model/meta.json"][EM.FACE_KEY]["⚑ listed_inputs_reconciliation"]["items"]
seeds = {job: C._c(C.input_keys(caps[f"{job}|0"])) == C._c(C.input_keys(caps[f"{job}|1"]))
         and tables[f"{job}|0"]["summary"] == tables[f"{job}|1"]["summary"] for job in C.JOBS}
sweeps_agree = sweeps["0"]["bindings"] == sweeps["1"]["bindings"]
preds = {}
for label, dd, dig in (("v3.8 model", C.V38_MODEL_DIR, C.V38_MODEL_DIGEST), ("v3.8 reference", C.V38_REFERENCE_DIR, C.V38_REFERENCE_DIGEST)):
    got = verify_pack_on_disk(os.path.join(C.OUT_ROOT, dd))
    preds[label] = got["recomputed_pack_digest"] == dig and got["n_digest_mismatch"] == 0
k7_post = verify_k7()
# mutation gate + exempt census
mg = collections.Counter(); mg_keys = collections.defaultdict(set); ex = collections.Counter()
for k, t in tables.items():
    for g in t["mutation_gate"]:
        mg[g["verdict"]] += 1; mg_keys[g["verdict"]].add(g["key"])
    for sec in L.SECTIONS:
        for r in t[sec]:
            if r.get("status") == "EXEMPT":
                ex[(sec, str(r.get("exempt"))[:40])] += 1
nip = C.not_in_pack_counts(tables)
# compare with star-lord's committed POST closure tables (semantic, paths normalised)
ROOT = I.ENGINE_ROOT; ALIAS = os.path.join(os.path.dirname(ROOT), "reincarnated-collaboration")
def norm(o):
    s = json.dumps(o, sort_keys=True, ensure_ascii=False, default=str)
    return s.replace(ROOT, "/Users/admin/Games/reincarnated-engine").replace(ALIAS, "/Users/admin/Games/reincarnated-collaboration")
def rowview(t):
    out = {}
    for sec in L.SECTIONS:
        for r in t[sec]:
            key = r.get("key") or f"{r.get('repo')}:{r.get('rel')}"
            out[f"{sec}|{key}"] = (r.get("status"), r.get("row"), str(r.get("exempt"))[:60])
    return out
cmp = {}
for k, t in tables.items():
    job, hs = k.split("|")
    p = os.path.join(C.OUT_ROOT, f"kc2-v3p11-POST-closure-table-{job}-hs{hs}-20261002_192143.json")
    theirs = json.load(open(p, encoding="utf-8"))
    mine_v, their_v = json.loads(norm(rowview(t))), json.loads(norm(rowview(theirs)))
    diff_keys = sorted(set(mine_v) ^ set(their_v))
    diff_vals = sorted(x for x in set(mine_v) & set(their_v) if mine_v[x] != their_v[x])
    cmp[k] = {"n_rows_mine": len(mine_v), "n_rows_theirs": len(their_v), "summary_equal": norm(t["summary"]) == norm(theirs["summary"]),
              "keys_only_one_side": diff_keys[:12], "n_keys_only_one_side": len(diff_keys),
              "value_diffs": [(x, mine_v[x], their_v[x]) for x in diff_vals[:12]], "n_value_diffs": len(diff_vals)}
# inputs equal star-lord's POST captures (normalised)
same_inputs = {}
for k, c in caps.items():
    job, hs = k.split("|")
    theirs = json.load(open(os.path.join(C.OUT_ROOT, f"kc2-v3p11-POST-capture-{job}-hs{hs}-20261002_192143.json"), encoding="utf-8"))
    same_inputs[k] = norm(C.input_keys(c)) == norm(C.input_keys(theirs))
_raw_tab = {k: C.closure_table(c, written, written_ref, idx=idx_w) for k, c in RAW.items()}
raw_viol = {k: L.v127p1_closure(t)["n_violations"] for k, t in _raw_tab.items()}
raw_sites = {k: [str(s)[:200] for s in L.v127p1_closure(t)["sites"]] for k, t in _raw_tab.items()}
rep = {
    "normalisation": NORM_LOG, "RAW_V127p1_violations_before_normalisation": raw_viol, "RAW_sites": raw_sites,
    "packs": {"model": wv["recomputed_pack_digest"], "reference": rv["recomputed_pack_digest"]},
    "validation": off, "inertness_all": inert["all_inert_and_reproducing"], "inertness": inert,
    "recon_equals_face": norm(recon) == norm(face_recon),
    "recon_blocking": [r for r in recon if "⛔" in r["verdict"]],
    "hash_seeds_agree": seeds, "static_sweeps_agree_seeds": sweeps_agree,
    "static_sweep_modules": len({b["key"].rsplit(".", 1)[0] for b in sweeps["0"]["bindings"]}),
    "static_sweep_n_bindings": len(sweeps["0"]["bindings"]),
    "predecessors_untouched": preds, "K-7": {"pre": k7_pre["all_unchanged"], "post": k7_post["all_unchanged"]},
    "NOT_IN_PACK_strict_per_capture": {k: sum(v.values()) for k, v in nip.items()},
    "mutation_gate_verdicts": dict(mg), "mutation_gate_keys": {k: sorted(v) for k, v in mg_keys.items()},
    "exempt_census": {f"{a}|{b}": n for (a, b), n in sorted(ex.items())},
    "vs_starlord_POST_tables": cmp, "inputs_equal_starlord_POST_captures": same_inputs,
    "capture_files_sha256": files,
}
json.dump(rep, open(OUTP, "w"), indent=1, ensure_ascii=False, default=str)
print(json.dumps({"verdict": off["verdict"], "gates": off["⚑ v3p11_gate_violations"],
                  "V156": {k: v["n_violations"] for k, v in off["V-156_closure_v3p7p1_law"]["per_capture"].items()},
                  "static": {h: v["n_violations"] for h, v in off["V-156_closure_v3p7p1_law"]["static_sweep"].items()},
                  "mg_clean": off["V-156_closure_v3p7p1_law"]["mutation_gate_clean"], "mg": dict(mg),
                  "inert": inert["all_inert_and_reproducing"], "seeds": all(seeds.values()), "sweeps": sweeps_agree,
                  "modules": rep["static_sweep_modules"], "preds": preds, "K7": rep["K-7"],
                  "NIP": rep["NOT_IN_PACK_strict_per_capture"], "recon_eq_face": rep["recon_equals_face"],
                  "cmp": {k: (v["summary_equal"], v["n_keys_only_one_side"], v["n_value_diffs"]) for k, v in cmp.items()},
                  "same_inputs": same_inputs, "raw_viol": raw_viol, "norm": NORM_LOG}, indent=1, default=str))
