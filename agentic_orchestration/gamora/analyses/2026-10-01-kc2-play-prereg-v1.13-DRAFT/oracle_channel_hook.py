#!/usr/bin/env python3
"""KC2-PLAY · prereg v1.13 DRAFT · the ORACLE-SIDE instrument for TA-X-08 identity 2 (gamora, 2026-10-01).

READ-ONLY on the engine. Runs drax's UNCHANGED G3 oracle tool (godot b4c1ff3,
`kc2_runtime/tools/kc2rt_g3_oracle_trace.py`, FILE 51f46965...) under `runpy`, with ONE added read-only hook:
`ChannelPolicyFold.observe` is wrapped to record, per call, the arguments the oracle passes and the fold's own
verdict for the tick (`self._verdict`, decided by `tick_apply` earlier in the same tick), then forwards to the
oracle's own method and returns its value unchanged. `run.simulate_wave` is wrapped only to bucket the calls by wave.

Nothing the oracle computes is replaced. The evidence that the hook is inert is that the trace this run writes is
byte-identical to the filed KP-177 trace (its `uncompressed_sha256` in the G3 MANIFEST 78bbcc8d...); the checker
asserts that per cell.

Why it is needed: identity 2's operands are a census term (from the trace) and a FOLD term (`n_released`) that the
trace does not carry. The fold term must come from the oracle, never from the port (dispatch rule: a restatement
is derived from the oracle's law, not from port output).

Usage: python3 oracle_channel_hook.py <tool.py> <salt> <trace_out.json> <ARM> <hook_out.json>
"""
import json
import os
import runpy
import sys

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True
sys.path.insert(0, "/Users/admin/Games/reincarnated-engine/src")

TOOL, SALT, TRACE_OUT, ARM, HOOK_OUT = sys.argv[1:6]

from reincarnated.simulation.kc2 import channel_policy as _cp  # noqa: E402
from reincarnated.simulation.kc2 import run as _kr  # noqa: E402

REC = {"arm": ARM, "salt": int(SALT), "waves": []}

_osw = _kr.simulate_wave


def _sw(*a, **kw):
    w = int(a[0] if a else kw["wave"])
    REC["waves"].append({"wave": w, "obs": [], "fold_report": None})
    return _osw(*a, **kw)


_kr.simulate_wave = _sw

_oobs = _cp.ChannelPolicyFold.observe


def _obs(self, *, run_tick, xy, already_suppressed):
    verdict = bool(self._verdict)            # the fold's own verdict for this tick (tick_apply), read before forwarding
    seq_ok = (self._verdict_seq == self.n_observe + 1)   # observe() increments n_observe first, then compares
    r = _oobs(self, run_tick=run_tick, xy=xy, already_suppressed=already_suppressed)
    if REC["waves"]:
        REC["waves"][-1]["obs"].append([int(run_tick), bool(already_suppressed), verdict, bool(r), bool(seq_ok)])
        REC["waves"][-1]["fold_report"] = {"armed": bool(self.armed), "n_ticks_released": int(self.n_ticks_released),
                                           "n_observe": int(self.n_observe), "n_apply": int(self.n_apply),
                                           "n_desync": int(self.n_desync),
                                           "n_ticks_already_suppressed": int(self.n_ticks_already_suppressed)}
    return r


_cp.ChannelPolicyFold.observe = _obs

# ── TA-X-16: the board's spawn-point KEYS, at the oracle's own filter. `pools_for` is the ONE place p06 is dropped
#    (wave_engine.py:305-307: `{sp: alts for sp, alts in by_sp.items() if sp != 6}` unless bonus_spawns_enabled).
#    Wrapped in both namespaces that call it (wave_engine's module global, and run.py's imported name); each call is
#    recorded with its caller, the flag it was passed, the keys it RETURNED, and the keys the unfiltered call
#    (flag=True) would have returned, computed by calling the oracle's own function once more (pure: it reads a
#    cached table and builds a dict).
from reincarnated.simulation.kc2 import wave_engine as _we  # noqa: E402

_opf = _we.pools_for


def _pf(wave, *, bonus_spawns_enabled=True):
    out = _opf(wave, bonus_spawns_enabled=bonus_spawns_enabled)
    if REC["waves"]:
        allk = sorted(_opf(wave, bonus_spawns_enabled=True).keys())
        REC["waves"][-1].setdefault("pools_for", []).append(
            [sys._getframe(1).f_code.co_name, int(wave), bool(bonus_spawns_enabled), sorted(out.keys()), allk])
    return out


_we.pools_for = _pf
_kr.pools_for = _pf

sys.argv = [TOOL, SALT, TRACE_OUT, ARM]
runpy.run_path(TOOL, run_name="__main__")

with open(HOOK_OUT, "w") as f:
    json.dump(REC, f)
print("[v113-hook]", ARM, SALT, "simulate_wave calls", len(REC["waves"]),
      "observe calls", sum(len(w["obs"]) for w in REC["waves"]))
