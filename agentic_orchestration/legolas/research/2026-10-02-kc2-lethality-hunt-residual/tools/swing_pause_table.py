"""DATAMINED: min/maxSwingPause per roster + pet record, Edition II (referent era), CRUCIBLE
precedence (whole record from the last archive carrying it), via the record's `controller`.
Cross-checked against the oracle's own pinned pm2_tg2_monster_timing.csv ctrl_* columns."""
import csv
import json
import pickle
import sys

sys.path.insert(0, "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/"
                   "research/2026-10-01-kc2-enemy-range-audit/scripts")
import gdlib  # noqa: E402

H = "/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/ac232ef8-034a-45e4-8e9f-65834cd599f9/scratchpad/hunt2"
D = pickle.load(open(f"{H}/out/probe_s0.pkl", "rb"))
recs = set()
for w, d in D.items():
    for a in d["actors"]:
        recs.add(a["record_path"])
    for p in d["wave"].get("pets") or []:
        recs.add(p["record_path"])
ed = gdlib.Edition("II")
timing = {r["record"]: r for r in csv.DictReader(open(f"{H}/eng/data/kc2/pm2_tg2_monster_timing.csv"))}
out = {}
n_check = n_agree = 0
for rec in sorted(recs):
    arc, r = ed.winner(rec)
    if r is None:
        out[rec] = {"status": "RECORD-ABSENT"}
        continue
    ctrl = r.get("controller")
    row = {"archive": arc, "controller": ctrl, "Class": r.get("Class")}
    if ctrl:
        carc, c = ed.winner(ctrl)
        if c is not None:
            row.update({"ctrl_archive": carc, "ctrl_class": c.get("Class"),
                        "minSwingPause": c.get("minSwingPause"), "maxSwingPause": c.get("maxSwingPause")})
        else:
            row["status"] = "CONTROLLER-ABSENT"
    t = timing.get(rec)
    if t and t.get("ctrl_minSwingPause") not in (None, "", "None"):
        n_check += 1
        ok = (abs(float(t["ctrl_minSwingPause"]) - float(row.get("minSwingPause") or 0)) < 1e-6 and
              abs(float(t["ctrl_maxSwingPause"]) - float(row.get("maxSwingPause") or 0)) < 1e-6)
        n_agree += ok
        row["pm2_timing_agrees"] = ok
    out[rec] = row
json.dump({"edition": "II", "precedence": "CRUCIBLE (last archive wins)", "n_records": len(out),
           "cross_check_vs_pm2_timing": {"n": n_check, "agree": n_agree}, "records": out},
          open(sys.argv[1], "w"), indent=1)
print(len(out), "records; cross-check", n_agree, "/", n_check)
miss = [k for k, v in out.items() if v.get("minSwingPause") is None]
print("no pause fields:", len(miss), miss[:12])
