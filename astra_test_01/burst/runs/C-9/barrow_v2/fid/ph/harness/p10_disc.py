#!/usr/bin/env python3
"""P10 DISCIPLINE (jack-ryan pilot-4 Gate-2 § 3; R-C9-267/268; pre-registered in calibration.md § 48 (c)).
  p10_disc.py set <out_dir> <scene> <view> [--runs 3] [--burn-ms N]
     per run: QUIESCENCE precondition (30 s of 1 Hz `ps` samples before launch: no non-Godot, non-render-path process
     averaging > 10 % CPU; else wait and re-check, up to 20 tries, then HALT) -> launch under the heavy lock -> IN-RUN
     PROCESS LOG at 1 Hz (proclog.jsonl); the run is VOID iff a non-Godot, non-render-path process exceeds 25 % CPU for
     >= 1 s while Godot runs. A VOID run -> the set of 3 is re-run; two VOID sets -> HALT.
  p10_disc.py score <dir_with_runs> -> worst p99 (binding, <= 16.7), DETERMINISTIC HITCH (binding: a frame > 25 ms
     recurring within +-0.5 s of window time in >= 2 of 3 runs = FAIL), burst-excluded p99 + bursts (report only).
  p10_disc.py witness -> v1 barrow_painted.tscn uv:0,1 x3 (the session witness; envelope = its p50 +- 0.5 ms)
Render-path processes (logged, never VOID triggers: they serve the measured Godot window): WindowServer, kernel_task."""
import json
import os
import subprocess
import sys
import threading
import time

import numpy as np

C9 = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9"
G = "/Applications/Godot.app/Contents/MacOS/Godot"
LOCK = "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-7/conductor_scripts/heavy_lock.py"
H = C9 + "/barrow_v2/fid/ph/harness/godot"
RENDER_PATH = ("WindowServer", "kernel_task")
OFFENDERS = ("mediaanalysisd", "photoanalysisd", "mds_stores", "backupd", "mdworker", "mds")


def ps():
    out = subprocess.run(["ps", "-A", "-o", "pid=,pcpu=,comm="], capture_output=True, text=True).stdout
    rows = []
    for l in out.splitlines():
        p = l.strip().split(None, 2)
        if len(p) == 3:
            try:
                rows.append((int(p[0]), float(p[1]), p[2]))
            except ValueError:
                pass
    return rows


def _excluded(comm):
    c = os.path.basename(comm)
    return "Godot" in comm or c in RENDER_PATH or c == "ps"


def quiescent(seconds=30):
    acc = {}
    me = os.getpid()
    for _ in range(seconds):
        for pid, cpu, comm in ps():
            if pid == me or _excluded(comm):
                continue
            acc.setdefault((pid, comm), []).append(cpu)
        time.sleep(1)
    avg = {k: sum(v) / seconds for k, v in acc.items()}
    over = sorted(((round(a, 1), os.path.basename(k[1]), k[0]) for k, a in avg.items() if a > 10.0), reverse=True)
    return not over, over


def gate():
    st = os.statvfs("/System/Volumes/Data")
    return st.f_bavail * st.f_frsize / 2 ** 30 >= 21


def one_run(out, scene, view, burn=None, loop=None, idle=False):
    os.makedirs(out, exist_ok=True)
    for t in range(20):
        ok, over = quiescent()
        with open(os.path.join(out, "quiescence.json"), "w") as f:
            json.dump({"try": t + 1, "ok": ok, "over_10pct_avg_30s": over}, f)
        if ok:
            break
        print("[p10] not quiescent:", over[:5], flush=True)
    else:
        return {"halt": "never quiescent", "over": over}
    if not gate():
        return {"halt": "disk < 21 GiB"}
    cmd = ["python3", LOCK, "C-9", "--", G, "--path", ".", "--resolution", "1920x1080", "--script", H + "/ph_life.gd", "--",
           "perf", scene, out, view] + (["--burn-ms", str(burn)] if burn else []) + (["--loop", loop] if loop else []) + (["--idle"] if idle else [])
    log = open(os.path.join(out, "log.txt"), "w")
    proc = subprocess.Popen(cmd, cwd=C9 + "/barrow_full/godot", stdout=log, stderr=subprocess.STDOUT)
    plog = open(os.path.join(out, "proclog.jsonl"), "w")
    void = []
    stop = threading.Event()

    def logger():
        while not stop.is_set():
            rows = ps()
            godot = any("Godot" in c for _, _, c in rows)
            hot = [(round(cpu, 1), os.path.basename(c), pid) for pid, cpu, c in rows if cpu > 25.0 and not _excluded(c)
                   and pid != os.getpid()]
            top = sorted(((round(cpu, 1), os.path.basename(c)) for pid, cpu, c in rows if cpu > 5.0), reverse=True)[:8]
            plog.write(json.dumps({"t": round(time.time(), 1), "godot_running": godot, "over25_nonGodot": hot, "top": top}) + "\n")
            plog.flush()
            if godot and hot:
                void.append(hot)
            time.sleep(1)
    th = threading.Thread(target=logger, daemon=True)
    th.start()
    rc = proc.wait()
    stop.set()
    th.join()
    plog.close()
    log.close()
    res = {"rc": rc, "void": bool(void), "void_samples": void[:5]}
    with open(os.path.join(out, "discipline.json"), "w") as f:
        json.dump(res, f)
    return res


def run_set(base, scene, view, runs=3, burn=None, label="start"):
    for attempt in range(2):
        voided = False
        for i in range(1, runs + 1):
            d = os.path.join(base, "%s_%d%s" % (label, i, "" if attempt == 0 else "_set%d" % (attempt + 1)))
            r = one_run(d, scene, view, burn)
            print("[p10]", d, r, flush=True)
            if r.get("halt"):
                return {"halt": r}
            if r["void"]:
                voided = True
                break
        if not voided:
            return {"ok": True, "attempt": attempt + 1}
    return {"halt": "two VOID sets"}


def score(base, label):
    import re
    runs = sorted(d for d in os.listdir(base) if re.fullmatch(re.escape(label) + r"_\d+(_set\d+)?", d) and os.path.exists(os.path.join(base, d, "trace.json")))
    rows, hitch_times = [], []
    for d in runs:
        perf = json.load(open(os.path.join(base, d, "perf.json")))
        tr = json.load(open(os.path.join(base, d, "trace.json")))
        w = np.array(tr["window_frames_ms"])
        t = np.cumsum(w) / 1000.0                    # window (walk) time, s
        slow = w > 16.7
        burst = np.zeros_like(slow)
        i = 0
        while i < len(w):
            if slow[i]:
                j = i
                while j + 1 < len(w) and slow[j + 1]:
                    j += 1
                if j > i:
                    burst[i:j + 1] = True
                i = j + 1
            else:
                i += 1
        keep = w[~burst]
        hi = [round(float(t[k]), 2) for k in np.where(w > 25.0)[0]]
        hitch_times.append(hi)
        disc = json.load(open(os.path.join(base, d, "discipline.json"))) if os.path.exists(os.path.join(base, d, "discipline.json")) else {}
        rows.append({"run": d, "p50": perf["p50_ms"], "p99": perf["p99_ms"], "max": perf["max_ms"], "void": disc.get("void"),
                     "frames_over_25ms_at_s": hi[:20], "n_over_16_7": int(slow.sum()), "bursts": int(sum(1 for k in range(1, len(w)) if burst[k] and not burst[k - 1]) + int(burst[0])),
                     "p99_burst_excluded_report_only": round(float(np.percentile(keep, 99)), 3) if len(keep) else None})
    rec = []
    for a in range(len(hitch_times)):
        for ta in hitch_times[a]:
            n = 1 + sum(any(abs(ta - tb) <= 0.5 for tb in hitch_times[b]) for b in range(len(hitch_times)) if b != a)
            if n >= 2:
                rec.append({"t_s": ta, "runs_sharing": n})
    worst = max(r["p99"] for r in rows) if rows else None
    return {"runs": rows, "worst_p99": worst, "p99_pass": worst is not None and worst <= 16.7,
            "deterministic_hitches": rec, "hitch_pass": not rec,
            "pass": worst is not None and worst <= 16.7 and not rec and not any(r["void"] for r in rows)}


LOOPS = {   # § 50 (c): the re-routed P10 walks on rp4, proven by position trace (renders/walk_probe/, walk_check.py)
    "start": "-10.77,5.75;-3.25,1.26;-1.75,6.83;-6.5,7.5",
    "sea": "-17.5,3.5;-16.2,1.0;-17.0,-1.0;-18.0,2.0"}


SEA_IDLE = ("uv:-28.56,-1.45", "R-C9-276 REPORT-ONLY: the old sea position (where the default loop stuck, PT r268), him IDLE (standing)")


def window(base, scene, first_window, paused, envelope_from=None, views=None):
    """§ 48 (c) amendment A + R-C9-276. Inside a scheduled QUIET WINDOW, fresh-process runs per round i (3 rounds):
    W_i (v1 witness), then each candidate view's run i. Candidate views (R-C9-276): start + sea (BINDING; proven loops,
    § 50 (c)) and sea_idle (REPORT-ONLY: the old sea position, him standing). Each run under the quiescence precondition and
    the 1 Hz VOID log. Binding per binding view: worst-of-3 p99 <= 16.7 and the deterministic hitch. Report-only: sea_idle,
    and the paired P p50 - preceding W p50. First window: the 3 W runs RECORD the envelope (p50 range +- 0.5 ms).
    Launch DETACHED:  nohup python3 p10_disc.py window <base> <scene> --first --paused "..." > <base>/driver.log 2>&1 &"""
    views = views or [("start", "uv:0,0", LOOPS["start"], False, True), ("sea", "uv:0,0", LOOPS["sea"], False, True),
                      ("sea_idle", SEA_IDLE[0], None, True, False)]
    os.makedirs(base, exist_ok=True)
    wlog = {"start": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "paused_by_conductor": paused, "first_window": first_window,
            "order": "per round: W, " + ", ".join(v[0] for v in views), "views": [{"name": v[0], "view": v[1], "loop": v[2], "idle": v[3],
                                                                                 "binding": v[4]} for v in views], "runs": []}

    def save():
        json.dump(wlog, open(os.path.join(base, "window_log.json"), "w"), indent=1)
    save()
    for i in range(1, 4):
        seq = [("W", "res://scenes/barrow_painted.tscn", "uv:0,1", None, False)] + [(v[0], scene, v[1], v[2], v[3]) for v in views]
        for lab, sc, vw, lp, idl in seq:
            d = os.path.join(base, "%s_%d" % (lab, i))
            r = one_run(d, sc, vw, None, lp, idl)
            wlog["runs"].append({"run": "%s_%d" % (lab, i), "result": r, "t": time.strftime("%H:%M:%S")})
            save()
            if r.get("halt") or r.get("void"):
                wlog["halt_or_void"] = {"run": "%s_%d" % (lab, i), "result": r}
                wlog["stop"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
                save()
                return wlog
    W = score(base, "W")
    wp50 = {x["run"]: x["p50"] for x in W["runs"]}
    if first_window:
        env = [round(min(wp50.values()) - 0.5, 3), round(max(wp50.values()) + 0.5, 3)]
        session_void = False
    else:
        env = json.load(open(envelope_from))["envelope_p50"]
        session_void = any(not (env[0] <= x <= env[1]) for x in wp50.values())
    res = {}
    for v in views:
        sc_ = score(base, v[0])
        pairs = [{"round": i, "P_p50": [x for x in sc_["runs"] if x["run"] == "%s_%d" % (v[0], i)][0]["p50"],
                  "W_p50": wp50["W_%d" % i]} for i in range(1, 4)]
        for p in pairs:
            p["diff_report_only"] = round(p["P_p50"] - p["W_p50"], 3)
        res[v[0]] = {"binding": v[4], "score": sc_, "paired_report_only": pairs}
    binding_views = [v[0] for v in views if v[4]]
    wlog.update(stop=time.strftime("%Y-%m-%dT%H:%M:%S%z"), witness=W, candidates=res, envelope_p50=env,
                envelope_recorded_here=first_window, session_void=session_void,
                binding={"views": binding_views, "pass": (not session_void) and all(res[b]["score"]["pass"] for b in binding_views),
                         "per_view": {b: {"worst_p99": res[b]["score"]["worst_p99"], "hitch_pass": res[b]["score"]["hitch_pass"],
                                          "pass": res[b]["score"]["pass"]} for b in binding_views}})
    save()
    return wlog


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "set":
        burn = float(a[a.index("--burn-ms") + 1]) if "--burn-ms" in a else None
        runs = int(a[a.index("--runs") + 1]) if "--runs" in a else 3
        label = a[a.index("--label") + 1] if "--label" in a else "run"
        print(json.dumps(run_set(a[1], a[2], a[3], runs, burn, label)))
    elif a[0] == "score":
        print(json.dumps(score(a[1], a[2] if len(a) > 2 else "run"), indent=1))
    elif a[0] == "window":
        # window <base> <scene> --first | --envelope <window_log.json of the founding window>  [--paused "..."]
        first = "--first" in a
        env = a[a.index("--envelope") + 1] if "--envelope" in a else None
        paused = a[a.index("--paused") + 1] if "--paused" in a else ""
        r = window(a[1], a[2], first, paused, env)
        print("window done", json.dumps(r.get("binding", r.get("halt_or_void"))))
    elif a[0] == "witness":
        base = a[1]
        r = run_set(base, "res://scenes/barrow_painted.tscn", "uv:0,1", 3, None, "v1")
        s = score(base, "v1")
        p50s = [x["p50"] for x in s["runs"]]
        s["envelope_p50"] = [round(min(p50s) - 0.5, 3), round(max(p50s) + 0.5, 3)] if p50s else None
        s["set"] = r
        json.dump(s, open(os.path.join(base, "witness.json"), "w"), indent=1)
        print(json.dumps(s, indent=1))
