# nb_join's COPY of nb_d2/scripts/31_meshy_fetch.py (sha256 254b417ac573..., read-only for this lane: the scene drax owns it),
# changed ONLY where it writes: ROOT is nb_join, so clips land in nb_join/anims/ and the ledger is nb_join/work/meshy_fetch.json
# (the conductor: never nb_d2/work/meshy_fetch.json). The lint and the body-rig guard are nb_d2's, read in place:
# 21_lint_export from nb_d2/scripts, the body rig from nb_d2/work/clip_sources.json -- so a fetch on any other rig is REFUSED
# exactly as 31 refuses it. Test a refusal with an INVALID key (MESHY_API_KEY=invalid): a guard that fails then spends nothing.
#
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
ROOT = os.path.dirname(HERE)                                        # nb_join
NB_D2 = os.path.join(os.path.dirname(ROOT), "nb_d2")                  # read-only: its lint and its rig registry
OUT = os.path.join(ROOT, "anims")
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, os.path.join(NB_D2, "scripts"))
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
        L = lint.lint(dst, skeleton=False)
        rec["lint"] = dict(verdict=L["verdict"], fails=L["fails"],
                           warns=L["warns"], clips=list(L["clips"]))
        print("%-14s %5.2f MB  LINT %-5s %s"
              % (nm, rec["mb"], L["verdict"], (L["fails"] or [""])[0][:100]))
    json.dump(D, open(W, "w"), indent=1)
    raise SystemExit(0)

rig = sys.argv[1]
specs = [x.split(":", 1) for x in sys.argv[2:] if not x.startswith("--")]
# THE BODY'S RIG, or a refusal. D2's clips were fetched on 01a0eb6a -- nb_t8's MESHY-mesh candidate,
# not the Tripo body chosen in T8 (01a0eb7e) -- and every one came in on the wrong skeleton. The
# provenance registry names the body's rig; a fetch on any other needs --other-rig, said out loud.
_REG = os.path.join(NB_D2, "work", "clip_sources.json")
_body_rig = (json.load(open(_REG)).get("body_rig") or {}).get("meshy_rig_task") if os.path.exists(_REG) else None
if _body_rig and rig != _body_rig and "--other-rig" not in sys.argv:
    sys.exit("REFUSED: rig %s is not this body's (%s, work/clip_sources.json body_rig); pass --other-rig to fetch for "
             "another skeleton on purpose" % (rig, _body_rig))
# THE RECORD IS MERGED, not overwritten: an earlier version wrote only this run's clips, so every
# fetch erased the record of the ones before it (their tasks, credits and lints)
# ...and two ways it could still forget a PAID task (fixed for D7 pass 2):
#   * a ledger in the older FLAT shape ({name: record}, no "clips"/"spent" keys -- the shape
#     --download-only already accepts) read as EMPTY here, and the first write replaced it whole;
#   * a refetch under a name already on record replaced that record, and with it the earlier
#     task id and its credits; a failed POST replaced a good record with an error.
# Now the flat shape is read as clips, a replaced paid record is kept under "superseded", and an
# error is appended to the record instead of replacing it. `spent` stays the running total of
# money spent, which a superseded record is still part of.
_W = os.path.join(ROOT, "work", "meshy_fetch.json")
_prev = json.load(open(_W)) if os.path.exists(_W) else {}
if _prev and "clips" not in _prev and "spent" not in _prev:
    _prev = dict(clips=_prev, spent=sum((v.get("credits") or 0) for v in _prev.values() if isinstance(v, dict)))
out, spent = dict(_prev.get("clips", {})), 0


def keep_paid(nm, rec):
    """out[nm] = rec, carrying any earlier PAID record for this name under 'superseded'."""
    old = out.get(nm)
    if isinstance(old, dict) and old.get("task"):
        rec["superseded"] = old.pop("superseded", []) + [old]
    elif isinstance(old, dict) and old.get("superseded"):
        rec["superseded"] = old["superseded"]
    out[nm] = rec


for nm, aid in specs:
    dst = os.path.join(OUT, "%s.glb" % nm)
    if os.path.exists(dst):
        print("%-14s already on disk, skipped" % nm, flush=True)
        continue
    r = call("POST", "/v1/animations", dict(rig_task_id=rig, action_id=int(aid)))
    tid = r.get("result")
    if not tid:
        print("%-14s NO TASK: %s" % (nm, r), flush=True)
        if isinstance(out.get(nm), dict) and out[nm].get("task"):
            out[nm].setdefault("errors", []).append(dict(action_id=int(aid), error=str(r)[:200]))
        else:
            out[nm] = dict(action_id=int(aid), error=str(r)[:200])
        continue
    s, st, el = poll("/v1/animations", tid)
    cr = s.get("consumed_credits")
    spent += cr or 0
    url = glb_url(s)
    # THE RIG, PER CLIP. The record kept only the last run's rig at top level, so a fetch on another
    # rig silently re-labelled every earlier clip -- and D2's clips WERE fetched on another rig
    # (01a0eb6a, nb_t8's Meshy-mesh candidate, not the Tripo body's 01a0eb7e; T12 2026-09-30).
    rec = dict(action_id=int(aid), task=tid, status=st, rig=rig,
               credits=cr, seconds=round(el))
    if st == "SUCCEEDED" and url:
        subprocess.run(["curl", "-s", "-L", url, "-o", dst], check=False)
        rec["file"] = dst
        rec["mb"] = round(os.path.getsize(dst) / 1e6, 2)
        try:
            L = lint.lint(dst, skeleton=False)
            rec["lint"] = dict(verdict=L["verdict"], fails=L["fails"],
                               warns=L["warns"], clips=list(L["clips"]))
        except Exception as e:
            rec["lint"] = dict(verdict="ERROR", fails=[str(e)])
    keep_paid(nm, rec)
    print("%-14s %-9s %3ss  %s credits  %s  LINT %s %s"
          % (nm, st, round(el), cr, rec.get("mb", "-"),
             rec.get("lint", {}).get("verdict", "-"),
             (rec.get("lint", {}).get("fails") or [""])[0][:90]), flush=True)
    json.dump(dict(rig=rig, spent=int(_prev.get("spent", 0)) + spent, clips=out), open(_W, "w"), indent=1)
print("\nTOTAL CREDITS SPENT: %s (record total %s)" % (spent, int(_prev.get("spent", 0)) + spent), flush=True)
json.dump(dict(rig=rig, spent=int(_prev.get("spent", 0)) + spent, clips=out), open(_W, "w"), indent=1)
