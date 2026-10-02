"""PRE-RUN MEASUREMENT on the CONTROL (v3.9 oracle of record, V39-FULL, salts 0-19) — inputs to the
pre-registration. ⚑ NOT-A-GRADED-RUN. Behaviour is the oracle's own, byte for byte (the CTRL arm of rj_arms.py,
proven equal to V39-FULL); this only COUNTS, through inert wrappers:

  m1  per tick, roster bodies in Attack whose chosen skill is Melee (slot demand on the player's 6 slots), and
      bodies in Attack or Pursue with a Melee choice within 6 m (requesters)
  m2  skill completions in reach with the SAME skill re-chosen, by randomRepositionChance (the RFA opportunity set)
  m3  Attack -> Pursue transitions that happen BEFORE the skill completes (the incumbent re-tests reach while the
      swing pause runs; GD does not: Attack::OnUpdate fires AttackEnemyOrReturn at timer <= 0 with no range test)
  m4  the converging solver's displacement of STANDING (Attack) roster bodies, and of moving ones

usage (from <snapshot>/src): python3 rj_control_measure.py <a-b> <out.json>
"""
from __future__ import annotations

import json
import math
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rj_arms as R  # noqa: E402
from reincarnated.simulation.kc2 import geometry as gm  # noqa: E402

M = {"m1_melee_attack_conc": Counter(), "m1_melee_requesters_6m": Counter(), "m2": Counter(),
     "m2_completions": 0, "m3_attack_to_pursue_before_completion": 0, "m3_attack_to_pursue_at_completion": 0,
     "m4_displaced_standing": 0, "m4_displaced_moving": 0, "m4_displaced_standing_m": 0.0,
     "m4_standing_pushed_out_of_reach": 0, "ticks": 0}
_LAST = {"tick": None}


def main() -> None:
    a, b = (int(x) for x in sys.argv[1].split("-"))
    salts = tuple(range(a, b + 1))
    base_iso = R.ge.GdEngagementFold.is_opportunity
    real_conv = gm.separate_overlaps_converging

    def iso(self, eng, aid, prof, tick):            # noqa: ANN001
        A0 = eng._ge_state.get(aid)
        mode0 = A0["mode"] if A0 else None
        need0 = A0["need"] if A0 else None
        S0 = A0["S"] if A0 else None
        busy0 = A0["busy_until"] if A0 else -1
        r = base_iso(self, eng, aid, prof, tick)
        A = eng._ge_state.get(aid)
        if _LAST["tick"] != (id(eng), tick):
            _LAST["tick"] = (id(eng), tick)
            M["ticks"] += 1
            conc = req = 0
            for k, st in eng._ge_state.items():
                if not R.ge._is_roster(k) or st["S"] is None or not self._alive_k(k):
                    continue
                rec = R.REG.movers[k].record if k in R.REG.movers else None
                mel = self._prof_k(rec, st["S"]) == "Melee"
                if mel and st["mode"] == "A":
                    conc += 1
                if mel and eng._ge_dist.get(k, 1e9) <= 6.0:
                    req += 1
            M["m1_melee_attack_conc"][conc] += 1
            M["m1_melee_requesters_6m"][req] += 1
        if A is not None and mode0 == "A" and A["mode"] == "P" and tick >= busy0:
            if need0:
                M["m3_attack_to_pursue_at_completion"] += 1
            else:
                M["m3_attack_to_pursue_before_completion"] += 1
        if (A is not None and need0 and mode0 == "A" and tick >= busy0 and S0 is not None and A["S"] is not None
                and not A["need"]):
            d = eng._ge_dist.get(aid, 1e9)
            if d <= A["S"].reach_m and S0.skill == A["S"].skill and S0.slot == A["S"].slot:
                rec = R.REG.movers[aid].record if aid in R.REG.movers else None
                pct = (R.REC.get(rec) or {}).get("randomRepositionChance") or 0
                M["m2"][str(pct)] += 1
        if A is not None and need0 and mode0 == "A" and tick >= busy0 and not A["need"]:
            M["m2_completions"] += 1
        return r

    def conv(live, *, fixed=(), player_xy=None, **kw):   # noqa: ANN001
        disp, st = real_conv(live, fixed=fixed, player_xy=player_xy, **kw)
        f = R.FOLD["f"]
        eng = f.eng if f is not None else None
        for i, (dx, dy) in disp.items():
            if i not in R.REG.movers or eng is None:
                continue
            A = eng._ge_state.get(i)
            if A is not None and A["mode"] == "A":
                M["m4_displaced_standing"] += 1
                M["m4_displaced_standing_m"] += math.hypot(dx, dy)
                m = R.REG.movers[i]
                px, py = player_xy
                d0 = math.hypot(m.xy[0] - px, m.xy[1] - py)
                d1 = math.hypot(m.xy[0] + dx - px, m.xy[1] + dy - py)
                if A["S"] is not None and d0 <= A["S"].reach_m < d1:
                    M["m4_standing_pushed_out_of_reach"] += 1
            else:
                M["m4_displaced_moving"] += 1
        return disp, st

    R.RJFold._alive_k = lambda self, k: self._alive(k)
    R.RJFold._prof_k = lambda self, rec, S: self._profile(rec, S)
    R.ge.GdEngagementFold.is_opportunity = iso
    gm.separate_overlaps_converging = conv
    try:
        res = R.run_arm("CTRL", salts)
    finally:
        R.ge.GdEngagementFold.is_opportunity = base_iso
        gm.separate_overlaps_converging = real_conv
    s = R.V9.summarise(res, salts)
    out = {"artifact_class": "PRE-RUN MEASUREMENT on the control (V39-FULL); behaviour unchanged",
           "salts": list(salts), "control_ratio_check": s["ratio_vs_referent"],
           "control_still_2p46_4p92": s["instruments"]["still_frac_2p46_4p92m"],
           "rj_modes": R.mode_band_summary(res, salts),
           "measures": {k: (dict(sorted(v.items())) if isinstance(v, Counter) else v) for k, v in M.items()}}
    json.dump(out, open(sys.argv[2], "w"), indent=1, default=str)
    print(json.dumps(out["measures"], default=str)[:3000])
    print("control check:", out["control_ratio_check"], out["control_still_2p46_4p92"])


if __name__ == "__main__":
    main()
