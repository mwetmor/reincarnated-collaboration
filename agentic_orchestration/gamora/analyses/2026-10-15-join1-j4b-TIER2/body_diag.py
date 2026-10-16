"""Diagnostics printed beside the body-off NCs (NOT graded): ticks, per-tick M-c, kills, monster leech heal, splash
signature. usage: python3 body_diag.py <arm> <out.json>"""
import collections, glob, importlib.util, json, sys
W = "/Users/admin/Games/reincarnated-engine-j4b-cert"
SP = "/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/ac232ef8-034a-45e4-8e9f-65834cd599f9/scratchpad"
spec = importlib.util.spec_from_file_location("g", W + "/src/reincarnated/simulation/scripts/gamora_join4b_grade.py")
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
arm = sys.argv[1]
B = f"/Users/admin/Games/join3c-bulk/t2/{arm}"; P = "/Users/admin/Games/join3c-bulk/car2/primary"
ra = g.load_run(f"{SP}/t2grade/{arm}/all"); rp = g.load_run(SP + "/car2/her")
refused = {(r["arm"], r["salt"]) for r in ra["G5"] if str(r["terminal_reason"]).startswith("raised")}
cells = sorted(c for c in rp["cells"] if c not in refused)
ma = {c: g.cell_metrics(ra, c, H=40000) for c in cells}; mp = {c: g.cell_metrics(rp, c, H=40000) for c in cells}
rows = lambda p: [json.loads(l) for l in open(p) if l.strip()]
def heal(base):
    return sum(r["leech_heal_hp"] for A in ("M0", "M-POL-2", "M-POL-2-NULL", "W1", "W1-NULL")
               for r in rows(f"{base}/{A}-join/HPCHAIN.jsonl"))
def counters(base):
    t = collections.Counter()
    for A in ("M0", "M-POL-2", "M-POL-2-NULL", "W1", "W1-NULL"):
        for v in json.load(open(f"{base}/{A}-join/JOIN-PROVENANCE.json"))["cells"].values():
            t.update(v["j4b_kit"]["counters"])
    return t
ca, cp = counters(B), counters(P)
out = {"ticks": {"arm": sum(m["ticks"] for m in ma.values()), "primary": sum(m["ticks"] for m in mp.values())},
       "M_c_per_tick_whole": g.paired({c: ma[c]["M_c"] for c in cells}, {c: mp[c]["M_c"] for c in cells}, direction="<="),
       "kills": {"arm": ca.get("kills"), "primary": cp.get("kills")},
       "monster_leech_heal": {"arm": heal(B), "primary": heal(P)},
       "M_a": {"arm": sum(m["survived"] for m in ma.values()), "primary": sum(m["survived"] for m in mp.values())}}
if arm == "body-splash":
    grp = collections.defaultdict(list)
    for p in glob.glob(f"{B}/*-join/J4B-ROWS-*.json"):
        d = json.load(open(p))
        for pk in d["packets"]:
            if pk["source"] == "fire_ball":
                grp[(d["arm"], d["salt"], pk["tick"], pk["draw"]["draw_index"])].append(pk["applied"])
    out["splash_signature"] = {"explosions": len(grp),
                               "explosions_with_more_than_one_nonzero_target": sum(1 for v in grp.values() if sum(1 for x in v if x > 0) > 1),
                               "secondary_rows_zero": sum(sum(1 for x in v if x == 0) for v in grp.values())}
json.dump(out, open(sys.argv[2], "w"), indent=1, default=str)
print(json.dumps({k: (v if not isinstance(v, dict) or "total_her" not in v else {x: v[x] for x in ("total_her", "total_him", "n_pos", "n_neg", "p_two_sided")}) for k, v in out.items()}, default=str))
