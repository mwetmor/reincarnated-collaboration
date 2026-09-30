"""C-9 T10-1e: a running fal.ai spend total, checked BEFORE every paid call.

N-C9-FAL-CAP recorded the lesson this exists for: "a per-service running spend total,
checked before any authorisation; a cap counted only at the end is not a cap." The $20
Phase-2 cap was crossed because the total was assembled after the fact. So every paid call
in the kit pipeline goes through `spend()`, which refuses BEFORE the call if it would take
the running total past the budget, and records the call after it returns.

BUDGET: $3.20, gandalf under R-C9-76, hard stop. It covers the four re-issue builds and the
four new painting-matched models, mattes included.

COST BASIS, from fal's own pricing API (GET /v1/models/pricing), not from memory:
  tripo3d/h3.1/multiview-to-3d   $0.01 per credit; a textured "detailed" multiview build
                                 is 40 credits = $0.40 (the ledger's recorded per-build
                                 price for every T9/T10/kit build)
  fal-ai/birefnet/v2             $0.0008 per COMPUTE SECOND. The usage endpoint returns 403
                                 for this key, so billed seconds cannot be read back. Each
                                 matte is charged here at its WALL-CLOCK seconds, which
                                 includes upload and queueing and so over-states compute:
                                 an upper bound, which is the right side to err on for a cap.

THE ARITHMETIC THAT SHAPES THE PLAN: eight builds are $3.20 exactly, so any matte at all
makes the eighth build cross the hard stop. That is known before the first call, and the
work is ordered so the build that does not fit is the one with the weakest prior.
"""
import json
import pathlib
import time
from datetime import datetime, timezone

LEDGER = pathlib.Path(__file__).resolve().parent / "kit_work" / "fal_spend_R-C9-76.json"
BUDGET = 3.20
PRICE = {"tripo3d/h3.1/multiview-to-3d": 0.40}
BIREFNET_PER_S = 0.0008
BIREFNET_RESERVE = 0.02        # held back before a matte: ~25 s of wall clock at the rate


def _load():
    if LEDGER.exists():
        return json.loads(LEDGER.read_text())
    return {"_what": "fal.ai spend under gandalf's $3.20 budget (R-C9-76), hard stop.",
            "_basis": "tripo $0.40 per build (40 credits at $0.01); birefnet at wall-clock "
                      "seconds x $0.0008/s, an upper bound on billed compute seconds.",
            "_starts_after": "Matt's $5.85 balance reading (R-C9-76, 19:30:59 EDT); every "
                             "earlier matte and build is already inside that number.",
            "budget_usd": BUDGET, "entries": []}


def total() -> float:
    return round(sum(e["usd"] for e in _load()["entries"]), 4)


def check(endpoint: str) -> float:
    """Refuse BEFORE the call if it could cross the budget. Returns the running total."""
    need = PRICE.get(endpoint, BIREFNET_RESERVE)
    t = total()
    if t + need > BUDGET + 1e-9:
        raise SystemExit("FAL BUDGET STOP: running $%.4f + $%.4f for %s would exceed the "
                         "$%.2f hard stop. Not called." % (t, need, endpoint, BUDGET))
    return t


def record(endpoint: str, what: str, seconds: float = None) -> float:
    d = _load()
    usd = PRICE.get(endpoint)
    if usd is None:
        usd = round((seconds or 0.0) * BIREFNET_PER_S, 5)
    d["entries"].append({"ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                         "endpoint": endpoint, "what": what, "usd": usd,
                         "wall_s": None if seconds is None else round(seconds, 2)})
    d["running_usd"] = round(sum(e["usd"] for e in d["entries"]), 4)
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps(d, indent=1) + "\n")
    return d["running_usd"]


class timed:
    """with timed() as t: ...  -> t.s is the wall-clock seconds of the block."""
    def __enter__(self):
        self.t0 = time.time()
        return self

    def __exit__(self, *a):
        self.s = time.time() - self.t0
        return False
