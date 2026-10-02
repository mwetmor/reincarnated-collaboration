#!/usr/bin/env python3
"""H-6 (jack-ryan): compares the gate's RE-RUN of gamora's committed instruments (oracle_trace_v3p11.py x36, audit_v1p15.py x5,
check_v1p14.py, check_v1p15.py, derive_v1p14.py; run from scratch copies by h6_rerun_gamora_instruments.sh) to the committed
outputs. Only `wall_s` (and the gz FILE digests that embed it, `files`) and derive's engine HEAD may differ.
Usage: h6_rerun_compare.py <scratch dir h6jr> <out.json>"""
import glob, gzip, json, os, sys
H, OUT = sys.argv[1], sys.argv[2]
G = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gamora/analyses"
R = {"traces": {}, "audits": {}}
for f in sorted(glob.glob(f"{H}/rerun114/raw/*.json")):
    b = os.path.basename(f); a = json.load(open(f)); c = json.load(gzip.open(f"{G}/2026-10-02-kc2-play-prereg-v1.14/oracle_trace/{b}.gz"))
    a.pop("wall_s"); c.pop("wall_s"); R["traces"][b] = a == c
for f in sorted(glob.glob(f"{H}/rerun115/raw/*.json")):
    b = os.path.basename(f); a = json.load(open(f)); c = json.load(gzip.open(f"{G}/2026-10-02-kc2-play-prereg-v1.15/audit_out/{b}.gz"))
    a.pop("wall_s"); c.pop("wall_s"); R["audits"][b] = a == c
def strip(o):
    if isinstance(o, dict): return {k: strip(v) for k, v in o.items() if k not in ("files", "wall_s")}
    if isinstance(o, list): return [strip(x) for x in o]
    return o
R["results_v1p14.json equal (minus files)"] = strip(json.load(open(f"{H}/rerun114/results_v1p14.json"))) == strip(json.load(open(f"{G}/2026-10-02-kc2-play-prereg-v1.14/results_v1p14.json")))
R["results_v1p15.json equal"] = strip(json.load(open(f"{H}/rerun115/results_v1p15.json"))) == strip(json.load(open(f"{G}/2026-10-02-kc2-play-prereg-v1.15/results_v1p15.json")))
a = json.load(open(f"{H}/rederive/derive_v1p14.json")); c = json.load(open(f"{G}/2026-10-02-kc2-play-prereg-v1.14/derive_v1p14.json"))
diffs = sorted(k for k in set(a) | set(c) if a.get(k) != c.get(k))
R["derive_v1p14.json top-level keys differing"] = diffs
R["derive engine block differs only in HEAD"] = {k: v for k, v in a["engine"].items() if k != "HEAD"} == {k: v for k, v in c["engine"].items() if k != "HEAD"}
R["derive self_check_failures (re-run)"] = a.get("self_check_failures")
R["summary"] = {"traces_equal": sum(R["traces"].values()), "traces": len(R["traces"]),
                "audits_equal": sum(R["audits"].values()), "audits": len(R["audits"])}
json.dump(R, open(OUT, "w"), indent=1, sort_keys=True)
print(json.dumps({k: v for k, v in R.items() if k not in ("traces", "audits")}, indent=1))
