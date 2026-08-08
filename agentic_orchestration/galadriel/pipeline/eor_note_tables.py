#!/usr/bin/env python3
"""Emit markdown per-wave tables for the EoR extraction note."""
import ast, json, statistics

WORK = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-08-07-eor-sittings/work"

S2 = {151: 682.100, 152: 698.383, 153: 714.833, 154: 729.617, 155: 743.750,
      156: 760.083, 157: 780.300, 158: 799.433, 159: 812.617, 160: 838.867}
S2_DEATH = 943.600
S1_DEATH = 2253.633


def load_refine(path):
    return [ast.literal_eval(l.strip()) for l in open(path) if l.strip().startswith("{")]


def s2_table():
    ws = sorted(S2)
    lines = ["| wave | t_start (video s) | t_end (video s) | clear (s) |",
             "|---:|---:|---:|---:|"]
    cl = []
    for i, w in enumerate(ws):
        t0 = S2[w]
        if i + 1 < len(ws):
            t1 = S2[ws[i + 1]]
            lines.append(f"| {w} | {t0:.2f} | {t1:.2f} | {t1-t0:.2f} |")
            cl.append(t1 - t0)
        else:
            lines.append(f"| {w} | {t0:.2f} | {S2_DEATH:.2f} (death) | {S2_DEATH-t0:.2f} — **not a clear** |")
    return "\n".join(lines), cl


def s1_table():
    br = json.load(open(f"{WORK}/s1-brackets.json"))
    ref = load_refine(f"{WORK}/s1-refine.log")
    n = min(len(br), len(ref))
    tstart, flags = {}, {}
    for b, r in zip(br[:n], ref[:n]):
        tstart[b["to"]] = r["t_change"]
        flags[b["to"]] = (r["sep"], (b["lo"] - 0.8) <= r["t_change"] <= (b["hi"] + 0.8))
    ws = sorted(tstart)
    lines = ["| wave | t_start (video s) | t_end (video s) | clear (s) | flag |",
             "|---:|---:|---:|---:|:--|"]
    cl = []
    for i, w in enumerate(ws):
        t0 = tstart[w]
        if i + 1 < len(ws):
            nw = ws[i + 1]
            t1 = tstart[nw]
            sep, inb = flags[nw]
            f = ("low-sep" if sep < 0.06 else "") + ("" if inb else " OUT-OF-BRACKET")
            lines.append(f"| {w} | {t0:.2f} | {t1:.2f} | {t1-t0:.2f} | {f} |")
            cl.append((w, t1 - t0))
        else:
            lines.append(f"| {w} | {t0:.2f} | {S1_DEATH:.2f} (death) | {S1_DEATH-t0:.2f} — **not a clear** | |")
    return "\n".join(lines), cl, flags, n


if __name__ == "__main__":
    t2, cl2 = s2_table()
    print("=== SITTING 2 ===")
    print(t2)
    print(f"\nn={len(cl2)} mean={statistics.mean(cl2):.2f} median={statistics.median(cl2):.2f} "
          f"min={min(cl2):.2f} max={max(cl2):.2f} sd={statistics.stdev(cl2):.2f}")
    t1, cl1, fl, n = s1_table()
    print("\n=== SITTING 1 (attempt 1) ===")
    print(t1)
    v = [c for _, c in cl1]
    print(f"\nn={len(v)} mean={statistics.mean(v):.2f} median={statistics.median(v):.2f} "
          f"min={min(v):.2f} max={max(v):.2f} sd={statistics.stdev(v):.2f}")
    print("fastest 8:", [(w, round(c, 2)) for w, c in sorted(cl1, key=lambda x: x[1])[:8]])
    print("slowest 8:", [(w, round(c, 2)) for w, c in sorted(cl1, key=lambda x: -x[1])[:8]])
    dec = {}
    for w, c in cl1:
        dec.setdefault((w - 1) // 10, []).append(c)
    print("\nper-decade:")
    for k in sorted(dec):
        d = dec[k]
        print(f"  waves {k*10+1:2d}-{k*10+10:2d}: n={len(d):2d} mean={statistics.mean(d):6.2f} "
              f"med={statistics.median(d):6.2f} min={min(d):5.2f} max={max(d):6.2f}")
    # boss-wave (multiples of 10) vs rest
    boss = [c for w, c in cl1 if w % 10 == 0]
    rest = [c for w, c in cl1 if w % 10 != 0]
    print(f"\nwaves ≡0 mod 10: n={len(boss)} mean={statistics.mean(boss):.2f}")
    print(f"other waves:      n={len(rest)} mean={statistics.mean(rest):.2f}")
    lows = [w for w, (s, i) in fl.items() if s < 0.06]
    outs = [w for w, (s, i) in fl.items() if not i]
    print(f"\nlow-sep transitions (into wave): {sorted(lows)}")
    print(f"out-of-bracket transitions:      {sorted(outs)}")
    # fractional-second structure test
    fr = [round(c % 1, 3) for c in v]
    near_int = sum(1 for f in fr if f < 0.25 or f > 0.75)
    print(f"\nintervals within 0.25s of an integer: {near_int}/{len(fr)} "
          f"(chance expectation {0.5*len(fr):.0f})")
