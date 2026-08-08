#!/usr/bin/env python3
"""Assemble the final EoR per-wave tables from refined transition timestamps."""
import ast, json, sys, statistics

WORK = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-08-07-eor-sittings/work"

S2 = {151: 682.100, 152: 698.383, 153: 714.833, 154: 729.617, 155: 743.750,
      156: 760.083, 157: 780.300, 158: 799.433, 159: 812.617, 160: 838.867}
S2_DEATH = 943.600
S1_DEATH = 2253.633
S1_A2_START = 2398.917
S1_END = 2498.367


def load_refine(path):
    out = []
    for line in open(path):
        line = line.strip()
        if not line.startswith("{"): continue
        out.append(ast.literal_eval(line))
    return out


def main():
    br = json.load(open(f"{WORK}/s1-brackets.json"))
    ref = load_refine(f"{WORK}/s1-refine.log")
    n = min(len(br), len(ref))
    rows = []
    for b, r in zip(br[:n], ref[:n]):
        t = r["t_change"]
        inb = (b["lo"] - 0.8) <= t <= (b["hi"] + 0.8)
        rows.append({"from": b["from"], "to": b["to"], "t": t, "sep": round(r["sep"], 4),
                     "in_bracket": inb, "amb": r.get("amb_frames", 0)})
    print(f"# sitting 1 -- {n} refined transitions")
    bad = [r for r in rows if not r["in_bracket"]]
    lowsep = [r for r in rows if r["sep"] < 0.06]
    print(f"out-of-bracket: {len(bad)} -> {[(r['from'],r['to'],r['t']) for r in bad]}")
    print(f"low-sep(<0.06): {len(lowsep)} -> {[(r['from'],r['to'],r['sep']) for r in lowsep]}")

    print("\nwave  t_start    t_end      clear_s   flag")
    clears = []
    for i, r in enumerate(rows):
        w = r["to"] - 1 if r["from"] != 0 else 0
    # build wave table: wave N runs from transition into N to transition into N+1
    tstart = {}
    for r in rows:
        tstart[r["to"]] = r["t"]
    waves = sorted(tstart)
    for i, w in enumerate(waves):
        t0 = tstart[w]
        t1 = tstart[waves[i + 1]] if i + 1 < len(waves) else None
        if t1 is None:
            if w == 93:
                print(f"{w:4d}  {t0:8.3f}  {S1_DEATH:8.3f}  {S1_DEATH-t0:7.3f}  DEATH (not a clear)")
            else:
                print(f"{w:4d}  {t0:8.3f}  --        --      (table truncated)")
        else:
            fl = ""
            rr = next(x for x in rows if x["to"] == waves[i + 1])
            if rr["sep"] < 0.06: fl = "low-sep"
            if not rr["in_bracket"]: fl += " OUT-OF-BRACKET"
            print(f"{w:4d}  {t0:8.3f}  {t1:8.3f}  {t1-t0:7.3f}  {fl}")
            clears.append((w, t1 - t0))
    if clears:
        v = [c for _, c in clears]
        print(f"\nS1 attempt-1 cleared waves n={len(v)} mean={statistics.mean(v):.3f} "
              f"median={statistics.median(v):.3f} min={min(v):.3f} max={max(v):.3f} "
              f"stdev={statistics.stdev(v):.3f}")
        v10 = sorted(clears, key=lambda x: x[1])[:6]
        print("six fastest waves:", [(w, round(c, 2)) for w, c in v10])
        dec = {}
        for w, c in clears:
            dec.setdefault((w - 1) // 10 * 10 + 1, []).append(c)
        print("\nper-decade mean clear (s):")
        for k in sorted(dec):
            print(f"  waves {k:3d}-{k+9:3d}: n={len(dec[k]):2d} mean={statistics.mean(dec[k]):6.2f} "
                  f"min={min(dec[k]):6.2f} max={max(dec[k]):6.2f}")
    json.dump({"s1_transitions": rows, "s1_wave_start": tstart}, open(f"{WORK}/s1-final.json", "w"), indent=1)


if __name__ == "__main__":
    main()
