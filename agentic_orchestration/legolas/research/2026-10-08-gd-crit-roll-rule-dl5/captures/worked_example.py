"""D-L5 worked example — the decoded Grim Dawn PTH roll (Game.dll x64 build 24825149, func 0x10d810).

ROLL = max(100, PTH) * u,  u ~ U(0,1)  (Park-Miller 31-bit, float32)
miss iff PTH < 100 and ROLL > PTH ; PTH <= 70 -> x(PTH/70), no crit
else tier multiplier = pthDamageModifier_i for the highest i with ROLL > pthThreshold_i (else x1.0)
crit iff multiplier > 1.0 ; crit damage % ADDED to the tier multiplier (SECONDARY + footage, not binary-traced)
"""
EDGES = (0.0, 90.0, 105.0, 120.0, 130.0, 135.0, float("inf"))
MULTS = (1.0, 1.1, 1.2, 1.3, 1.4, 1.5)


def pth(oa, da):
    return ((((oa / ((da / 3.5) + oa)) * 300) * 0.3) + (((((oa * 3.25) + 10000) - (da * 3.25)) / 100) * 0.7)) - 50


def outcome_shares(p):
    p = max(p, 55.0)
    r = max(100.0, p)
    if p <= 70.0:
        return {"miss": (r - p) / r, p / 70.0: p / r}
    out = {"miss": (r - p) / r}
    for k, m in enumerate(MULTS):
        lo, hi = EDGES[k], min(EDGES[k + 1], p)
        out[m] = max(0.0, hi - lo) / r
    return out


def summarize(oa, da, crit_damage=0.57):
    p = pth(oa, da)
    s = outcome_shares(p)
    hit = 1.0 - s["miss"]
    crit = sum(v for k, v in s.items() if k != "miss" and k > 1.0)
    e_tier = sum(k * v for k, v in s.items() if k != "miss" and k > 1.0) / crit if crit else float("nan")
    e_hit_no_cd = sum(k * v for k, v in s.items() if k != "miss") / hit
    e_hit_cd = sum((k + (crit_damage if k > 1.0 else 0.0)) * v for k, v in s.items() if k != "miss") / hit
    return p, s, crit, e_tier, e_hit_no_cd, e_hit_cd


if __name__ == "__main__":
    for da in (2011.53, 2770.09):
        p, s, crit, e_tier, e0, e1 = summarize(3259.0, da)
        shares = ", ".join(f"{k}: {v:.4f}" for k, v in s.items() if v)
        print(f"OA 3259 vs DA {da}: PTH {p:.4f} | {shares} | crit {crit:.4f} | "
              f"E[tier|crit] {e_tier:.4f} | E[x|crit] incl +57% {e_tier + 0.57:.4f} | "
              f"E[x|hit] no CD {e0:.5f} | E[x|hit] +57% CD {e1:.5f}")
