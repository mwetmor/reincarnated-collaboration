# METEOR2 COPY (R-C9-80 two-handed Meteor search): ROOT is so_d7/meteor2, so clips land in meteor2/anims and the ledger is meteor2/work/meshy_fetch.json -- so_d7/export and so_d7/anims are untouched.
# Fetch library animations for the barbarian's own rig, then LINT each one.
#
#   MESHY_API_KEY=... python3 scripts/31_meshy_fetch.py <rig_task_id> \
#        <name>:<action_id> ...
#
# Native to his rig: no retarget, no role map, no fidelity loss. 3 credits each.
#
# EVERY FETCHED CLIP IS LINTED before it is allowed near the export. Meshy's
# own Idle action shipped a constant Hips scale of 1.176471 -- 20/17, a 1.70 m
# source retargeted to a 2.00 m target -- which made the barbarian 17.6% bigger
# whenever he stood still and survived T8 and D2 untouched. That was one library
# action out of the four fetched. There is no reason to expect these eleven to
# be cleaner, and every reason to check.
import json, os, subprocess, sys, time
K = os.environ["MESHY_API_KEY"]
BASE = "https://api.meshy.ai/openapi"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "anims")
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "scripts"))  # meteor2: lint from so_d7/scripts
import importlib
lint = importlib.import_module("21_lint_export")


def call(method, path, body=None, timeout="120"):
    args = ["curl", "-s", "--max-time", timeout, "-X", method, BASE + path,
            "-H", "Authorization: Bearer " + K]
    if body is not None:
        args += ["-H", "Content-Type: application/json", "-d", json.dumps(body)]
    r = subprocess.run(args, capture_output=True, text=True)
    try:
        return json.loads(r.stdout)
    except Exception:
        return {"_raw": r.stdout[:400]}


def poll(path, tid, every=15, cap=1800):
    t0 = time.time()
    while time.time() - t0 < cap:
        s = call("GET", "%s/%s" % (path, tid))
        st = s.get("status")
        if st in ("SUCCEEDED", "FAILED", "CANCELED"):
            return s, st, time.time() - t0
        time.sleep(every)
    return {}, "TIMEOUT", time.time() - t0


def glb_url(s):
    """The animate task puts it at result.animation_glb_url. An earlier version
    of this looked for result.glb and result.model_urls.glb, found neither, and
    downloaded nothing -- while the POSTs had already spent the credits. The
    tasks persist server-side, so a later GET recovered every file for free, but
    the lesson is the ordinary one: a key that is absent reads exactly like a
    task that produced nothing."""
    r = s.get("result")
    if isinstance(r, dict):
        for k in ("animation_glb_url", "glb", "model_glb_url", "GLB"):
            if r.get(k):
                return r[k]
    for k in ("model_urls", "output"):
        v = s.get(k)
        if isinstance(v, dict):
            for kk in ("animation_glb_url", "glb", "GLB"):
                if v.get(kk):
                    return v[kk]
    return None


if "--download-only" in sys.argv:
    # re-GET every task recorded earlier and pull its GLB. Free: no new task.
    W = os.path.join(ROOT, "work", "meshy_fetch.json")
    D = json.load(open(W))
    clips = D.get("clips", D)
    for nm, rec in clips.items():
        tid = rec.get("task")
        dst = os.path.join(OUT, "%s.glb" % nm)
        if not tid or os.path.exists(dst):
            continue
        s = call("GET", "/v1/animations/%s" % tid)
        u = glb_url(s)
        if not u:
            print("%-14s no url: status=%s keys=%s"
                  % (nm, s.get("status"), list((s.get("result") or {}))[:6]))
            continue
        subprocess.run(["curl", "-s", "-L", u, "-o", dst], check=False)
        rec["file"] = dst
        rec["mb"] = round(os.path.getsize(dst) / 1e6, 2)
        L = lint.lint(dst)
        rec["lint"] = dict(verdict=L["verdict"], fails=L["fails"],
                           warns=L["warns"], clips=list(L["clips"]))
        print("%-14s %5.2f MB  LINT %-5s %s"
              % (nm, rec["mb"], L["verdict"], (L["fails"] or [""])[0][:100]))
    json.dump(D, open(W, "w"), indent=1)
    raise SystemExit(0)

rig = sys.argv[1]
specs = [x.split(":", 1) for x in sys.argv[2:]]
# MERGE, NEVER OVERWRITE. This used to start from an empty dict and write only the
# current run's clips back, so a second invocation erased every earlier task id --
# including cast126's, which was recovered from the account list precisely so a
# paid task would not vanish from the record. A ledger that forgets on rerun is not
# a ledger.
_W = os.path.join(ROOT, "work", "meshy_fetch.json")
_prev = json.load(open(_W)) if os.path.exists(_W) else {}
out = dict(_prev.get("clips", _prev if "clips" not in _prev and "spent" not in _prev else {}))
spent = sum((v.get("credits") or 0) for v in out.values())
print("ledger carries %d earlier clip(s), %d credits" % (len(out), spent), flush=True)
for nm, aid in specs:
    dst = os.path.join(OUT, "%s.glb" % nm)
    if os.path.exists(dst):
        print("%-14s already on disk, skipped" % nm, flush=True)
        continue
    r = call("POST", "/v1/animations", dict(rig_task_id=rig, action_id=int(aid)))
    tid = r.get("result")
    if not tid:
        print("%-14s NO TASK: %s" % (nm, r), flush=True)
        out[nm] = dict(action_id=int(aid), error=str(r)[:200])
        continue
    s, st, el = poll("/v1/animations", tid)
    cr = s.get("consumed_credits")
    spent += cr or 0
    url = glb_url(s)
    rec = dict(action_id=int(aid), task=tid, status=st,
               credits=cr, seconds=round(el))
    if st == "SUCCEEDED" and url:
        subprocess.run(["curl", "-s", "-L", url, "-o", dst], check=False)
        rec["file"] = dst
        rec["mb"] = round(os.path.getsize(dst) / 1e6, 2)
        try:
            L = lint.lint(dst)
            rec["lint"] = dict(verdict=L["verdict"], fails=L["fails"],
                               warns=L["warns"], clips=list(L["clips"]))
        except Exception as e:
            rec["lint"] = dict(verdict="ERROR", fails=[str(e)])
    out[nm] = rec
    print("%-14s %-9s %3ss  %s credits  %s  LINT %s %s"
          % (nm, st, round(el), cr, rec.get("mb", "-"),
             rec.get("lint", {}).get("verdict", "-"),
             (rec.get("lint", {}).get("fails") or [""])[0][:90]), flush=True)
    json.dump(dict(rig=rig, spent=sum((v.get("credits") or 0) for v in out.values()), clips=out),
              open(os.path.join(ROOT, "work", "meshy_fetch.json"), "w"), indent=1)
spent = sum((v.get("credits") or 0) for v in out.values())
print("\nTOTAL CREDITS ON THIS LEDGER: %s" % spent, flush=True)
json.dump(dict(rig=rig, spent=spent, clips=out),
          open(os.path.join(ROOT, "work", "meshy_fetch.json"), "w"), indent=1)
