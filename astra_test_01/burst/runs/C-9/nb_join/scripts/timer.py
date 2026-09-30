# nb_join step timing (the barbarian's JOIN moves) -- copied from nb_w2 (itself from so_d7).
#
#   python3 scripts/timer.py start <step> [--note "..."]
#   python3 scripts/timer.py wait  <step> <seconds> [--what "tripo poll"]
#   python3 scripts/timer.py end   <step> [--note "..."]
#   python3 scripts/timer.py table
#
# TWO CLOCKS, defined so they can be measured rather than estimated:
#   wall   end - start, including every second spent waiting on a generator.
#   agent  wall MINUS the recorded external waits. A generator's poll loop
#          reports its own duration with `wait`, so the subtraction uses a
#          measured number, not a guess about how long I was "really" working.
#
# What agent time is NOT: it is not "time the model spent thinking". It is
# wall-clock with the generator queues removed -- the part of the step that a
# faster pipeline could actually shorten. A step whose wall time is all wait
# is bounded by the vendor, not by us, and D5 needs to know which is which.
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(os.path.dirname(HERE), "work", "timing.jsonl")


def emit(rec):
    with open(LOG, "a") as f:
        f.write(json.dumps(rec) + "\n")


def load():
    if not os.path.exists(LOG):
        return []
    return [json.loads(x) for x in open(LOG) if x.strip()]


def arg(flag):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else ""


cmd = sys.argv[1]
if cmd in ("start", "end"):
    emit(dict(ev=cmd, step=sys.argv[2], t=time.time(), note=arg("--note")))
    print("%s %s @ %s" % (cmd, sys.argv[2], time.strftime("%H:%M:%S")))
elif cmd == "wait":
    emit(dict(ev="wait", step=sys.argv[2], s=float(sys.argv[3]), what=arg("--what")))
    print("wait %s %.0fs (%s)" % (sys.argv[2], float(sys.argv[3]), arg("--what")))
elif cmd == "table":
    ev = load()
    steps, order = {}, []
    for e in ev:
        s = steps.setdefault(e["step"], dict(start=None, end=None, wait=0.0, notes=[]))
        if e["step"] not in order:
            order.append(e["step"])
        if e["ev"] == "start" and s["start"] is None:
            s["start"] = e["t"]
        elif e["ev"] == "end":
            s["end"] = e["t"]
        elif e["ev"] == "wait":
            s["wait"] += e["s"]
        if e.get("note"):
            s["notes"].append(e["note"])
    tw = ta = tx = 0.0
    print("%-34s %9s %9s %9s  %s" % ("step", "wall", "wait", "agent", "note"))
    for k in order:
        s = steps[k]
        if s["start"] is None or s["end"] is None:
            print("%-34s %9s %9s %9s  %s" % (k, "open", "", "", "; ".join(s["notes"])[:70]))
            continue
        w = s["end"] - s["start"]
        a = max(w - s["wait"], 0.0)
        tw += w; tx += s["wait"]; ta += a
        print("%-34s %8.0fs %8.0fs %8.0fs  %s" % (k, w, s["wait"], a, "; ".join(s["notes"])[:70]))
    print("%-34s %8.0fs %8.0fs %8.0fs" % ("TOTAL", tw, tx, ta))
    print("%-34s %8.1fm %8.1fm %8.1fm" % ("", tw / 60, tx / 60, ta / 60))
