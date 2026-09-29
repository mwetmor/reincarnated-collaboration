# T8 step 1: Meshy rig + library animations for the barbarian.
#
#   python3 scripts/08_meshy.py probe
#   python3 scripts/08_meshy.py rig <input_task_id> [height_m]
#   python3 scripts/08_meshy.py anim <rig_task_id> <name>:<action_id> ...
#
# curl-based because this Python's SSL cannot reach the API directly (the
# pattern 02_meshy_model.py already uses). The key comes from the environment
# and is never written to a file, a log or stdout.
import json, os, subprocess, sys, time
K = os.environ["MESHY_API_KEY"]
BASE = "https://api.meshy.ai/openapi"


def call(method, path, body=None, timeout="120"):
    args = ["curl", "-s", "--max-time", timeout, "-X", method, BASE + path,
            "-H", "Authorization: Bearer " + K]
    if body is not None:
        args += ["-H", "Content-Type: application/json", "-d", json.dumps(body)]
    r = subprocess.run(args, capture_output=True, text=True)
    try:
        return json.loads(r.stdout or "{}")
    except json.JSONDecodeError:
        return {"_raw": r.stdout[:400], "_err": r.stderr[:200]}


def poll(path, tid, every=15, cap=1800):
    t0 = time.time()
    s = {}
    while True:
        s = call("GET", "%s/%s" % (path, tid))
        st = s.get("status")
        if st in ("SUCCEEDED", "FAILED", "CANCELED", "EXPIRED") or time.time() - t0 > cap:
            return s, st, time.time() - t0
        time.sleep(every)


cmd = sys.argv[1]
if cmd == "probe":
    # what does the motion library expose, and under what path? Asked rather
    # than assumed -- a wrong guess here is spent credits, not an error.
    for p in ("/v1/motions?page_size=200", "/v1/animations/actions?page_size=200",
              "/v1/animations/library?page_size=200", "/v1/actions?page_size=200",
              "/v1/rigging", "/v1/animations"):
        r = call("GET", p)
        if isinstance(r, list):
            print("GET %-42s -> LIST of %d" % (p, len(r)))
            if r and "action_id" in r[0]:
                json.dump(r, open("work/motions.json", "w"), indent=1)
                print("     wrote work/motions.json (%d actions)" % len(r))
            continue
        if "message" in r and len(r) <= 2:
            print("GET %-42s -> %s" % (p, str(r["message"])[:90]))
            continue
        res = r.get("result")
        n = len(res) if isinstance(res, list) else None
        print("GET %-42s -> keys %s%s" % (p, list(r.keys())[:6],
                                          "" if n is None else "  (%d items)" % n))
        if n:
            json.dump(r, open("work/motions.json", "w"), indent=1)
            print("     first item keys: %s" % list(res[0].keys())[:10])
            print("     wrote work/motions.json")
elif cmd == "rigfile":
    # Meshy rigs an EXTERNAL model through `model_url`, and that field accepts
    # a data: URI -- discovered by probing, not assumed: with a URL it cannot
    # reach the error is "failed to download model file", and with a 44-byte
    # data URI it becomes "failed to invoke pose estimation", which means the
    # bytes arrived. So a local GLB can be rigged without hosting it anywhere.
    import base64
    src = sys.argv[2]
    body = dict(model_url="data:model/gltf-binary;base64,"
                + base64.b64encode(open(src, "rb").read()).decode())
    if len(sys.argv) > 3:
        body["character_height"] = float(sys.argv[3])
    tmp = "work/_rigreq.json"
    json.dump(body, open(tmp, "w"))
    print("posting %s as a data URI (%.1f MB of JSON)"
          % (src, os.path.getsize(tmp) / 1e6), flush=True)
    r = subprocess.run(["curl", "-s", "--max-time", "600", "-X", "POST",
                        BASE + "/v1/rigging", "-H", "Authorization: Bearer " + K,
                        "-H", "Content-Type: application/json", "-d", "@" + tmp],
                       capture_output=True, text=True)
    os.remove(tmp)
    r = json.loads(r.stdout or "{}")
    tid = r.get("result")
    print("rig task", tid, {k: v for k, v in r.items() if k != "result"}, flush=True)
    assert tid, "no task id -- not spending further"
    s_, st, el = poll("/v1/rigging", tid)
    json.dump(s_, open("work/res_rig_tripo.json", "w"), indent=1)
    print(st, "%.0fs" % el, "credits", s_.get("consumed_credits"),
          (s_.get("task_error") or {}).get("message", ""), flush=True)
elif cmd == "rig":
    body = dict(input_task_id=sys.argv[2])
    if len(sys.argv) > 3:
        body["character_height"] = float(sys.argv[3])
    r = call("POST", "/v1/rigging", body)
    tid = r.get("result")
    print("rig task", tid, {k: v for k, v in r.items() if k != "result"}, flush=True)
    assert tid, "no task id -- not spending further"
    s, st, el = poll("/v1/rigging", tid)
    json.dump(s, open("work/res_rig.json", "w"), indent=1)
    print(st, "%.0fs" % el, "credits", s.get("consumed_credits"),
          (s.get("task_error") or {}).get("message", ""), flush=True)
elif cmd == "anim":
    rig = sys.argv[2]
    out = {}
    for spec in sys.argv[3:]:
        nm, aid = spec.split(":", 1)
        r = call("POST", "/v1/animations", dict(rig_task_id=rig, action_id=int(aid)))
        tid = r.get("result")
        print("%-8s task %s %s" % (nm, tid, {k: v for k, v in r.items() if k != "result"}),
              flush=True)
        if not tid:
            continue
        s, st, el = poll("/v1/animations", tid)
        json.dump(s, open("work/res_anim_%s.json" % nm, "w"), indent=1)
        out[nm] = dict(task=tid, status=st, credits=s.get("consumed_credits"))
        print("   %s %s %.0fs credits %s" % (nm, st, el, s.get("consumed_credits")),
              flush=True)
    json.dump(out, open("work/anims.json", "w"), indent=1)
