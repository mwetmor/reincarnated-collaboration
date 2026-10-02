# E1 Meshy spend ledger: check() BEFORE every paid POST (refuses past the 40-credit cap, counting the
# account balance drop as the truth), record() AFTER with the balance read back.
import json, os, subprocess, datetime, fcntl
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LED = os.path.join(ROOT, "meshy_spend_R-C9-132.json")
def balance():
    r = subprocess.run(["curl", "-s", "--max-time", "30", "https://api.meshy.ai/openapi/v1/balance",
                        "-H", "Authorization: Bearer " + os.environ["MESHY_API_KEY"]], capture_output=True, text=True)
    return json.loads(r.stdout)["balance"]
def spent():
    d = json.load(open(LED)); b = balance()
    return max(sum(e.get("credits") or 0 for e in d["entries"]), d["balance_at_start"] - b), b
def check(need, what):
    s, b = spent(); cap = json.load(open(LED))["cap_credits"]
    if s + need > cap:
        raise SystemExit("MESHY CAP STOP: spent %d + %d for %s would exceed %d. Not called." % (s, need, what, cap))
    return s
def record(what, credits, task=None):
    with open(LED + ".lock", "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        d = json.load(open(LED)); b = balance()
        d["entries"].append(dict(ts=datetime.datetime.now().isoformat(timespec="seconds"), what=what, credits=credits, task=task, balance_after=b))
        d["spent_by_entries"] = sum(e.get("credits") or 0 for e in d["entries"]); d["spent_by_balance"] = d["balance_at_start"] - b
        json.dump(d, open(LED, "w"), indent=1)
        return d["spent_by_entries"], d["spent_by_balance"]
