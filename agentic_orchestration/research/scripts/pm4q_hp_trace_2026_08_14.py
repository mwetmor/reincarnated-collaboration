#!/usr/bin/env python3
"""RUN KC2-PM4 · LAP Q · I-Q1 — the 60 fps player-HP trace, and the U-P-N-1 discriminator.

Substrate
---------
  video  : /Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/
           eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4
           sha256 4c60960d98e9d729e17469044dbe7b4341b253d7d36ba26fe09564d6056a4de8
  ROI    : x in [520,780), y in [996,1026)  -- the health-orb bar readout (fixed HUD position)
  cadence: 60 fps over t in [683.0, 864.0]  -> 10,861 samples
  OCR    : Apple Vision, .accurate, languageCorrection OFF (ocr.swift, byte-identical to Lap N's)
  accept : read matches ^(\\d{1,5})/(20005|16368)$   (denominator = decoded health_max; free validator)

What the trace contains, structurally (PREREGISTRATION.md § 5.3):
  * a per-frame DRIP of +2 / +3 HP  -> health regeneration
  * discrete large STEPS            -> Eye-of-Reckoning ADCTH leech ticks
The step magnitude is the quantity U-P-N-1 disagrees about by a factor ~4.

READ-ONLY on every source.
"""
import json, csv, hashlib, collections, statistics as st

OUT = ("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/"
       "notes/2026-08-14-kc2-pm4-lap-q-heal-discriminator")
TRACE = "/tmp/pm4q/hp_trace.json"
T0, FPS = 683.0, 60.0

# --- pre-registered predicted magnitudes (Lap P emitted columns; PREREGISTRATION.md § 3) ---
PRED = {
    "COUPLED":   dict(med_lo=561.0,  med_hi=1435.6, p5=224.4,  p95=2053.6, mn=130.1, mx=2092.0,
                      hps_lo=6388.0,  hps_hi=17587.0),
    "DECOUPLED": dict(med_lo=2149.6, med_hi=5398.0, p5=1458.5, p95=5869.6, mn=371.8, mx=5977.2,
                      hps_lo=24477.0, hps_hi=66126.0),
}
REGEN_HP_S = 129.38          # Lap P § 5.5, sheet (camera-measured)
HEALTH_MAX = 20005           # Lap A sheet
WAVES = [(151, 683.0, 698.6), (152, 698.6, 714.9), (153, 714.9, 729.8), (154, 729.8, 744.0),
         (155, 744.0, 760.2), (156, 760.2, 780.4), (157, 780.4, 799.7), (158, 799.7, 812.7),
         (159, 812.7, 839.0), (160, 839.0, 864.0)]

# top-5 pre-registered recovery windows (fixed by the rule in PREREGISTRATION.md § 5.3)
WINDOWS = {1: (843.383, 843.917), 2: (862.167, 863.217), 3: (841.483, 842.233),
           4: (833.067, 835.267), 5: (822.083, 823.350)}
# Lap H-2 pm4h2_ring_density.csv, max nameplate contact at R=150 ground px (declared LOWER BOUND)
N_HI_WAVE = {158: 8, 159: 9, 160: 8}

STEP_MIN = 50        # separates a leech tick from the +2/+3 regen drip (see § "drip" below)
DEFICIT_MIN = 3000   # cap cannot bind a single tick at this deficit


def wave_of(t):
    for w, a, b in WAVES:
        if a <= t < b:
            return w
    return None


def main():
    d = json.load(open(TRACE))
    tr = sorted((int(k), v[0], v[1]) for k, v in d.items())
    idx = {i: (h, m) for i, h, m in tr}
    T = lambda i: T0 + i / FPS

    # ---------------- the regen drip (instrument positive control) ----------------
    # Split at 33 % health: Lap G/P's Menhir's Will circuit-breaker grants +120 hp/s BELOW 33 %.
    # The deep-deficit stretches are ALSO the no-contact stretches, so the sub-33 % subset is the
    # only place the drip is regeneration UNCONTAMINATED by sub-STEP_MIN leech ticks.
    drip_lo, drip_hi = [], []
    for i in range(tr[0][0] + 1, tr[-1][0] + 1):
        if i not in idx or (i - 1) not in idx:
            continue
        h0, m0 = idx[i - 1]
        s = idx[i][0] - h0
        if 0 < s < STEP_MIN and m0 - h0 >= DEFICIT_MIN:
            (drip_lo if h0 / m0 < 0.33 else drip_hi).append(s)
    drip = drip_lo + drip_hi
    drip_rate = st.mean(drip_lo) * FPS if drip_lo else float("nan")

    # ---------------- leech ticks ----------------
    def decreases_near(i, k=2):
        """True if HP fell in any frame within +-k of i -- a proxy for 'damage landed here'."""
        for j in range(i - k, i + k + 1):
            if j in idx and (j - 1) in idx and idx[j][0] < idx[j - 1][0]:
                return True
        return False

    ticks = []
    for i in range(tr[0][0] + 1, tr[-1][0] + 1):
        if i not in idx or (i - 1) not in idx:
            continue
        h0, m0 = idx[i - 1]
        h1, m1 = idx[i]
        step = h1 - h0
        if step < STEP_MIN:
            continue
        if m0 - h0 < DEFICIT_MIN:          # cap could bind
            continue
        if h1 >= m1:                       # step landed ON the cap -> truncated
            continue
        ticks.append(dict(frame=i, t_sec=round(T(i), 4), wave=wave_of(T(i)),
                          hp_before=h0, hp_after=h1, health_max=m0,
                          deficit_before=m0 - h0, step_raw=step,
                          step_net_of_regen=round(step - REGEN_HP_S / FPS, 2),
                          clean=int(not decreases_near(i))))

    vals = [x["step_net_of_regen"] for x in ticks]
    q = lambda p: st.quantiles(vals, n=100)[p - 1]

    # inter-tick cadence
    gaps = [(ticks[j]["frame"] - ticks[j - 1]["frame"]) / FPS
            for j in range(1, len(ticks))
            if 0 < ticks[j]["frame"] - ticks[j - 1]["frame"] <= 12]

    print("=" * 78)
    print("I-Q1 · PLAYER-HP TRACE — 60 fps, t in [683.0, 864.0]")
    print("=" * 78)
    print(f"accepted samples                  : {len(tr)} / 10861  ({100*len(tr)/10861:.2f} %)  "
          f"PC-3 (>=95 %) -> {'PASS' if len(tr)/10861 >= 0.95 else 'FAIL'}")
    print(f"health_max values observed        : {sorted(set(m for _,_,m in tr))}")
    print(f"HP min / max                      : {min(h for _,h,_ in tr)} / {max(h for _,h,_ in tr)}")
    full = sum(1 for _, h, m in tr if h >= m)
    print(f"frames at full health             : {full} ({100*full/len(tr):.2f} %)")
    print()
    print("--- INSTRUMENT POSITIVE CONTROL: the regen drip ---")
    print(f"sub-{STEP_MIN} increments, health < 33 % : n={len(drip_lo)}  "
          f"multiset={dict(collections.Counter(drip_lo).most_common(6))}  "
          f"-> {st.mean(drip_lo)*FPS:.2f} HP/s")
    print(f"sub-{STEP_MIN} increments, health >= 33 %: n={len(drip_hi)}  "
          f"multiset={dict(collections.Counter(drip_hi).most_common(6))}  "
          f"-> {st.mean(drip_hi)*FPS:.2f} HP/s  [CONTAMINATED by sub-{STEP_MIN} leech ticks]")
    print(f"Lap P decoded regen (sheet)       : {REGEN_HP_S:.2f} HP/s   "
          f"-> residual on the CLEAN subset {drip_rate - REGEN_HP_S:+.2f} HP/s "
          f"({100*(drip_rate/REGEN_HP_S-1):+.2f} %)")
    print(f"Menhir's Will (+120 hp/s below 33 %) would predict 249.38 HP/s below 33 % "
          f"-> MEASURED-ABSENT (observed {st.mean(drip_lo)*FPS:.2f})")
    print()
    print("--- LEECH TICKS (step >= 50 HP, deficit >= 3000, not truncated by the cap) ---")
    print(f"n ticks                           : {len(ticks)}")
    print(f"median inter-tick interval        : {st.median(gaps):.4f} s  "
          f"-> {1/st.median(gaps):.3f} ticks/s   (Lap P decoded 11.387 - 12.250 /s)")
    print(f"min / p5 / p25 / median / p75 / p95 / max :")
    print(f"   {min(vals):8.1f} {q(5):8.1f} {q(25):8.1f} {st.median(vals):8.1f} "
          f"{q(75):8.1f} {q(95):8.1f} {max(vals):8.1f}")
    print()
    print("--- THE DISCRIMINATOR ---")
    print("observed step = (heal per hit per body) x N_bodies,  N >= 1.")
    print("So OBSERVED/1 is an UPPER bound on per-body heal; larger N only lowers it.")
    print()
    print(f"{'arm':<11} {'median band':>20} {'board p5':>10} {'board min':>10} "
          f"{'obs median':>11} {'verdict on median':>22}")
    for arm, p in PRED.items():
        om = st.median(vals)
        v = ("INSIDE band" if p['med_lo'] <= om <= p['med_hi'] else
             f"{om/p['med_lo']:.2f}x BELOW band lo" if om < p['med_lo'] else
             f"{om/p['med_hi']:.2f}x ABOVE band hi")
        print(f"{arm:<11} {p['med_lo']:9.0f} - {p['med_hi']:<8.0f} {p['p5']:10.0f} "
              f"{p['mn']:10.0f} {om:11.1f} {v:>22}")
    print()
    clean = [x["step_net_of_regen"] for x in ticks if x["clean"]]
    print()
    print(f"CLEAN ticks (no HP decrease within +-2 frames -> no damage masking): "
          f"n={len(clean)}/{len(vals)}")
    if clean:
        cq = lambda p: st.quantiles(clean, n=100)[p - 1]
        print(f"   min {min(clean):.1f} | p25 {cq(25):.1f} | median {st.median(clean):.1f} "
              f"| p75 {cq(75):.1f} | max {max(clean):.1f}")
        for arm, p in PRED.items():
            cm = st.median(clean)
            v = ("INSIDE band" if p['med_lo'] <= cm <= p['med_hi'] else
                 f"{cm/p['med_lo']:.2f}x BELOW band lo" if cm < p['med_lo'] else
                 f"{cm/p['med_hi']:.2f}x ABOVE band hi")
            print(f"   {arm:<11} median band {p['med_lo']:.0f}-{p['med_hi']:.0f} -> {v}")
    print()
    for arm, p in PRED.items():
        below_min = sum(1 for v in vals if v < p['mn'])
        below_p5 = sum(1 for v in vals if v < p['p5'])
        below_medlo = sum(1 for v in vals if v < p['med_lo'])
        print(f"{arm:<11}: ticks below board MIN {below_min:4d}/{len(vals)} "
              f"({100*below_min/len(vals):5.1f} %) | below board p5 {below_p5:4d} "
              f"({100*below_p5/len(vals):5.1f} %) | below median-band lo {below_medlo:4d} "
              f"({100*below_medlo/len(vals):5.1f} %)")

    # ---------------- recovery windows + damage correction ----------------
    print()
    print("--- TOP-5 RECOVERY WINDOWS, damage-corrected (PREREGISTRATION.md § 5.3) ---")
    dmg = damage_by_window()
    win_rows = []
    for k in sorted(WINDOWS):
        a, b = WINDOWS[k]
        ia, ib = round((a - T0) * FPS), round((b - T0) * FPS)
        h0, h1 = idx[ia][0], idx[ib][0]
        dur = (ib - ia) / FPS
        net = (h1 - h0) / dur
        dmgv, dmgn = dmg.get(k, (0, 0))
        gross = (h1 - h0 + dmgv) / dur
        w = wave_of(a)
        nhi = N_HI_WAVE.get(w, 1)
        win_rows.append(dict(window=k, wave=w, t_start=a, t_end=b, dur_s=round(dur, 4),
                             hp_start=h0, hp_end=h1, gain=h1 - h0,
                             red_fct_events=dmgn, damage_taken_HP=dmgv,
                             net_rate_HP_s=round(net, 1), gross_rate_HP_s=round(gross, 1),
                             N_hi_wave=nhi,
                             DECOUPLED_thresh=round(PRED['DECOUPLED']['hps_lo'] * nhi, 0),
                             COUPLED_thresh_N1=PRED['COUPLED']['hps_hi']))
        print(f"  w{k} wave{w} t={a:.3f}-{b:.3f} dur={dur:.3f}s gain={h1-h0:6d} "
              f"redFCT={dmgn} dmg={dmgv:6d} | net={net:8.0f} gross={gross:8.0f} HP/s | "
              f"DECOUPLED needs >= {PRED['DECOUPLED']['hps_lo']*nhi:,.0f} (N_hi={nhi}) | "
              f"COUPLED@N=1 <= {PRED['COUPLED']['hps_hi']:,.0f}")

    r1 = sum(1 for r in win_rows if r['gross_rate_HP_s'] >= r['DECOUPLED_thresh'])
    r2a = sum(1 for r in win_rows if r['gross_rate_HP_s'] <= PRED['COUPLED']['hps_hi'])
    r2b = q(5) < PRED['DECOUPLED']['p5']
    print()
    print(f"RULE 1 (DECOUPLED)  windows meeting threshold : {r1}/5  (needs >= 2)  "
          f"-> {'FIRES' if r1 >= 2 else 'does NOT fire'}")
    print(f"RULE 2 (COUPLED)    windows <= COUPLED@N=1    : {r2a}/5  (needs >= 2)")
    print(f"RULE 2 (COUPLED)    tick p5 {q(5):.1f} < DECOUPLED board p5 "
          f"{PRED['DECOUPLED']['p5']:.1f} -> {r2b}")

    # ---------------- emit ----------------
    with open(f"{OUT}/pm4q_hp_trace.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["frame", "t_sec", "wave", "hp", "health_max", "deficit", "delta_hp"])
        prev = None
        for i, h, m in tr:
            w.writerow([i, round(T(i), 4), wave_of(T(i)), h, m, m - h,
                        "" if prev is None or prev[0] != i - 1 else h - prev[1]])
            prev = (i, h)
    with open(f"{OUT}/pm4q_heal_events.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(ticks[0].keys()) + [
            "provenance", "per_body_if_N1", "COUPLED_median_band_contains",
            "DECOUPLED_median_band_contains", "below_DECOUPLED_board_p5", "below_COUPLED_board_min"])
        w.writeheader()
        for x in ticks:
            v = x["step_net_of_regen"]
            # NOT FCT-derived: heal FCT is NOT DISPLAYED in the referent (findings § 2).
            w.writerow(dict(x, provenance="hp_trace_60fps_ocr_NOT_fct", per_body_if_N1=v,
                            COUPLED_median_band_contains=int(PRED['COUPLED']['med_lo'] <= v <= PRED['COUPLED']['med_hi']),
                            DECOUPLED_median_band_contains=int(PRED['DECOUPLED']['med_lo'] <= v <= PRED['DECOUPLED']['med_hi']),
                            below_DECOUPLED_board_p5=int(v < PRED['DECOUPLED']['p5']),
                            below_COUPLED_board_min=int(v < PRED['COUPLED']['mn'])))
    with open(f"{OUT}/pm4q_recovery_windows.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(win_rows[0].keys()))
        w.writeheader()
        w.writerows(win_rows)

    res = dict(
        pc3_accept_frac=round(len(tr) / 10861, 6),
        health_max_values=sorted(set(m for _, _, m in tr)),
        regen_measured_HP_s=round(drip_rate, 3), regen_decoded_HP_s=REGEN_HP_S,
        n_ticks=len(ticks),
        tick_rate_per_s=round(1 / st.median(gaps), 4),
        tick_min=min(vals), tick_p5=round(q(5), 1), tick_median=st.median(vals),
        tick_p95=round(q(95), 1), tick_max=max(vals),
        rule1_windows=r1, rule2a_windows=r2a, rule2b=bool(r2b),
    )
    json.dump(res, open("/tmp/pm4q/iq1_summary.json", "w"), indent=2)
    for n in ("pm4q_hp_trace.csv", "pm4q_heal_events.csv", "pm4q_recovery_windows.csv"):
        h = hashlib.sha256(open(f"{OUT}/{n}", "rb").read()).hexdigest()
        rows = sum(1 for _ in open(f"{OUT}/{n}")) - 1
        print(f"{n}: rows={rows} sha256={h}")


def damage_by_window():
    """Red (damage-taken) numeric FCT inside each pre-registered window.

    DECLARED DEPARTURE from PREREGISTRATION.md § 5.3: dedup is by VALUE within a 2.0 s
    neighbourhood, not by (value, +-40 px).  Reason, measured not assumed: GD floating combat
    text DRIFTS upward over its ~1.2-1.5 s lifetime (Lap N measured the lifetime), so a
    +-40 px positional key does not hold a single string together across the window and would
    have over-counted damage -- which would have biased the gross rate UPWARD, i.e. toward
    DECOUPLED.  The replacement rule is the conservative one for this lap's own lean.
    """
    import re
    from math import inf
    W = {1: (843.383, 843.917), 2: (862.167, 863.217), 3: (841.483, 842.233),
         4: (833.067, 835.267), 5: (822.083, 823.350)}
    rows = [r for r in csv.DictReader(open(f"{OUT}/pm4q_fct_colour.csv"))
            if r["colour_class"] == "red_taken" and r["is_hud"] == "0"
            and r["text_class"] in ("bare", "crit") and r["source"] == "window"]
    out = {}
    for k, (a, b) in W.items():
        cand = [r for r in rows if int(r["window"]) == k and a <= float(r["t_sec"]) <= b]
        seen, tot = [], 0
        for r in sorted(cand, key=lambda z: float(z["t_sec"])):
            m = re.match(r"^(\d[\d,]{0,9})", r["text"])
            if not m:
                continue
            v, t = int(m.group(1).replace(",", "")), float(r["t_sec"])
            # a damage-TAKEN number above health_max cannot be a hit the player survived, and he
            # never died in the referent -> such a read is an OCR merge of two strings.  Rejected.
            if v > HEALTH_MAX:
                continue
            # cluster: same drifting FCT string re-read across frames -> values within 5 %
            if any(abs(vv - v) <= 0.05 * max(vv, v) and abs(tt - t) <= 2.0 for vv, tt in seen):
                continue
            seen.append((v, t)); tot += v
        out[k] = (tot, len(seen))
    return out


if __name__ == "__main__":
    main()
