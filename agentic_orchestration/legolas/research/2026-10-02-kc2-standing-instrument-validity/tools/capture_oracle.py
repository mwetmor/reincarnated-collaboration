"""INERT trajectory capture on the v3.10 oracle (V310-FULL), read-only.

Wraps kc2.locomotion.Mover.step (outermost, beneath gamora's net_observer) and records, at every step call,
the body's PRE-step position (= end of the previous tick, after separation), the true player position (the
simulate_wave frame's px, py at mover-stepping time), the body's HP fraction, radius, step travel and the
engagement mode. Writes NOTHING back and draws no random number.

usage (from <snapshot>/src):  python3 capture_oracle.py <cfg> <salt_a-salt_b> <out.npz>
"""
import sys, json, math, numpy as np
sys.dont_write_bytecode = True
from reincarnated.simulation.kc2 import locomotion as lo
from reincarnated.simulation.scripts import gamora_kc2_play_v3p10_oracle_2026_10_02 as V10
from reincarnated.simulation.scripts import gamora_kc2_c11_lethality_decomposition_2026_09_29 as c11

ROWS = []
IDS = {}
CUR = {"salt": -1}
real_step = lo.Mover.step

def _sw_frame():
    f = sys._getframe(2)
    while f is not None and f.f_code.co_name != "simulate_wave":
        f = f.f_back
    return f

def cap_step(self, dt_s, player_xy, **kw):
    pre = self.xy
    r = real_step(self, dt_s, player_xy, **kw)
    f = _sw_frame()
    if f is None:
        return r
    L = f.f_locals
    if CUR.get("fid") is not f:
        CUR["fid"] = f
        CUR["inv"] = CUR.get("inv", -1) + 1
    aid = self.actor_id
    is_pet = "_pet" in aid
    hp = None
    try:
        if is_pet:
            ps = L.get("pet_state", {}).get(aid)
            if ps is not None:
                hp = float(ps["hp"]) / max(1e-9, float(ps["hp_max"]))
        else:
            a = L["actors"][aid]
            hp = float(a["hp"]) / max(1e-9, float(a["hp_max"]))
    except Exception:
        hp = None
    mode = "x"
    fo = V10._CUR.get("f")
    try:
        eng = fo.v39.eng
        if hasattr(eng, "mode_of"):
            mode = eng.mode_of(aid) or "x"
    except Exception:
        pass
    key = (CUR["salt"], int(L.get("wave")), aid)
    if key not in IDS:
        IDS[key] = len(IDS)
    post = self.xy
    tp = (float(L["px"]), float(L["py"]))
    try:
        e = fo.v39.eng
        if getattr(e, "repositions", False) and getattr(e, "_pxy", None) is not None:
            tp = (float(e._pxy[0]), float(e._pxy[1]))
    except Exception:
        pass
    ROWS.append((CUR["salt"], int(L.get("wave")), int(kw.get("tick", -1)), float(kw.get("t_s", float("nan"))),
                 IDS[key], int(is_pet), pre[0], pre[1], float(L["px"]), float(L["py"]),
                 -1.0 if hp is None else hp, float(self.radius_m), float(self.last_step_travel_m),
                 "APRWx".index(mode) if mode in "APRWx" else 4, post[0], post[1], tp[0], tp[1], CUR["inv"]))
    return r

lo.Mover.step = cap_step
real_c11_run_arm = c11.run_arm
def c11_run_arm(runner, arm, s, period, *a, **kw):
    CUR["salt"] = int(s)
    return real_c11_run_arm(runner, arm, s, period, *a, **kw)
c11.run_arm = c11_run_arm

def main():
    cfg, sl, outp = sys.argv[1], sys.argv[2], sys.argv[3]
    a, b = (int(x) for x in sl.split("-"))
    salts = tuple(range(a, b + 1))
    period = V10.FP._period()
    res = V10.run_one(cfg, salts, period)
    summ = V10.summarise(res, salts)
    arr = np.array(ROWS, dtype=float)
    ids = np.array([[k[0], k[1], v] for k, v in IDS.items()], dtype=float)
    names = [k[2] for k in IDS]
    np.savez_compressed(outp, rows=arr, ids=ids, period=period)
    json.dump({"cfg": cfg, "salts": salts, "period": period, "names": names,
               "ratio": summ["ratio_vs_referent"], "per_salt": summ["per_salt_ratio"],
               "still_frac_by_H2_band_151_160": summ["instruments"]["still_frac_by_H2_band_151_160"],
               "body_steps_by_band": summ["instruments"]["body_steps_by_band"],
               "still_frac_2p46_4p92m": summ["instruments"]["still_frac_2p46_4p92m"],
               "instruments310": summ["instruments310"], "leg_a_terminals": summ["leg_a_terminals"],
               "hbands": V10.HB},
              open(outp.replace(".npz", "_summary.json"), "w"), indent=1, default=str)
    print("rows", arr.shape, "ratio", summ["ratio_vs_referent"], "sf", summ["instruments"]["still_frac_by_H2_band_151_160"])

if __name__ == "__main__":
    main()
