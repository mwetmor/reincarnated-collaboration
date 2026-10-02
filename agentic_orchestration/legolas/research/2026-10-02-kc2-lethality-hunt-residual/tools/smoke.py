"""Crash-only smoke test (salt 0). Prints ONLY whether the arm ran and its mechanism telemetry
counters; no ratio, no death wave, no landed figure is printed or written (pre-registration
discipline: outcomes are not inspected before the prediction file is committed)."""
import sys
import traceback

import hunt2
import arms_extra as AX

arm = sys.argv[1]
AX.TEL.clear()
try:
    res = hunt2.run(arm, (0,))
    raised = res["salts"]["0"].get("raised")
    print(arm, "RAN; raised:", raised)
    print("telemetry:", dict(sorted(AX.TEL.items())))
except Exception:                                   # noqa: BLE001
    print(arm, "EXCEPTION")
    traceback.print_exc()
