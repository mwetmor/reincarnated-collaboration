"""legolas 2026-10-01 -- THE LETHALITY HUNT, Leg 1: audit of the referent intake denominator.

READ-ONLY. Re-derives the referent's waves-151..159 landed-intake rate exactly as gamora's C-11 harness
does (`gamora_kc2_c11_lethality_decomposition_2026_09_29.referent()`: sum of negative frame-to-frame HP
deltas inside each wave's contiguous window / window length), from the committed Lap-Q trace, then
tests each candidate error against the trace itself.

    python3 referent_audit.py <out.json>
"""
import csv, json, sys, collections, hashlib
TRACE = ("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/"
         "2026-08-14-kc2-pm4-lap-q-heal-discriminator/pm4q_hp_trace.csv")
EOR_TICKS_PER_S = 11.408        # Lap Q 6(b), measured on this trace (inside Lap L's decoded bracket)
FPS = 60.0

raw = open(TRACE, "rb").read()
R = list(csv.DictReader(open(TRACE)))
fr = [(int(r["frame"]), float(r["t_sec"]), int(r["wave"]) if r["wave"] else -1, int(r["hp"]),
       int(r["health_max"])) for r in R]
W9 = range(151, 160)

def wave_stats(skip_maxhp_steps=False):
    out = {}
    for w in range(151, 161):
        f = [x for x in fr if x[2] == w]
        t0 = f[0][1]
        dur = f[-1][1] - f[0][1] + 1.0 / FPS
        dec, inc, maxhp_steps = [], [], []
        for i in range(1, len(f)):
            d = f[i][3] - f[i - 1][3]
            if f[i][4] != f[i - 1][4]:                       # health_max changed this frame
                maxhp_steps.append((round(f[i][1], 4), f[i - 1][4], f[i][4], d))
                if skip_maxhp_steps:
                    continue
            if d < 0:
                dec.append((f[i][1] - t0, -d))
            elif d > 0:
                inc.append((f[i][1] - t0, d))
        I = sum(v for _, v in dec); H = sum(v for _, v in inc)
        tail = 0
        for x in reversed(f):
            if x[3] >= x[4]:
                tail += 1
            else:
                break
        out[w] = {"dur_s": round(dur, 4), "intake_hp": I, "heal_hp": H,
                  "intake_hp_per_s": round(I / dur, 1),
                  "net_hp_change": f[-1][3] - f[0][3],
                  "intake_first10s_hp": sum(v for t, v in dec if t < 10.0),
                  "first_decrement_t_s": round(min((t for t, _ in dec), default=float("nan")), 2),
                  "frac_frames_at_full": round(sum(1 for x in f if x[3] >= x[4]) / len(f), 3),
                  "idle_tail_at_full_s": round(tail / FPS, 2),
                  "n_decrement_frames": len(dec),
                  "max_single_frame_decrement": max((v for _, v in dec), default=0),
                  "health_max_steps": maxhp_steps}
    return out

def pooled(st):
    I = sum(st[w]["intake_hp"] for w in W9); D = sum(st[w]["dur_s"] for w in W9)
    return I, D, I / D

base = wave_stats(False)
I, D, rate = pooled(base)
fixed = wave_stats(True)
I2, D2, rate2 = pooled(fixed)

# frame-update quantisation: do HP changes land on every frame, or on a coarser sim grid?
hp = [x[3] for x in fr]; mx = [x[4] for x in fr]
d = [0] + [hp[i] - hp[i - 1] for i in range(1, len(hp))]
drip = [i for i in range(1, len(d)) if 1 <= d[i] <= 3]
tick = [i for i in range(1, len(d)) if d[i] >= 50]
decf = [i for i in range(1, len(d)) if d[i] < 0]
gaps = lambda L: dict(sorted(collections.Counter(L[i] - L[i - 1] for i in range(1, len(L))).items())[:10])
below = [i for i in range(1, len(d)) if hp[i - 1] < mx[i - 1] and hp[i] < mx[i]]
p_tick_below = sum(1 for i in below if d[i] >= 50) / len(below)
p_tick_cap = EOR_TICKS_PER_S / FPS
mask_cap = 1.0 / (1.0 - p_tick_cap)

oracle_A0 = 5207.1          # gamora KP-201 A0 / legolas p05 PACK arm, PW-FOLDED salts 0-19, landed 151-159
oracle_first10 = 5327.0     # same arm, first 10 s of each wave
I10 = sum(base[w]["intake_first10s_hp"] for w in W9); D10 = sum(min(10.0, base[w]["dur_s"]) for w in W9)
tails = sum(base[w]["idle_tail_at_full_s"] for w in W9)

out = {
    "trace": TRACE, "trace_sha256": hashlib.sha256(raw).hexdigest(), "n_frames": len(fr),
    "method_reproduced": {"pooled_151_159_intake_hp": I, "pooled_dur_s": round(D, 3),
                          "pooled_intake_hp_per_s": round(rate, 1),
                          "matches_C11_1605p6": abs(rate - 1605.6) < 0.05},
    "per_wave": base,
    "E1_health_max_step_counted_as_intake": {
        "pooled_intake_hp_excluding_maxhp_frames": I2,
        "pooled_intake_hp_per_s_corrected": round(rate2, 1),
        "delta_pct": round((rate2 / rate - 1) * 100, 2),
        "ratio_A0_before_after": [round(oracle_A0 / rate, 4), round(oracle_A0 / rate2, 4)]},
    "E2_masking_by_same_frame_heal": {
        "update_grid": {"drip_frame_gaps": gaps(drip), "tick_frame_gaps": gaps(tick),
                        "decrement_frame_gaps": gaps(decf),
                        "parity_drip": dict(collections.Counter(i % 2 for i in drip)),
                        "parity_decrement": dict(collections.Counter(i % 2 for i in decf))},
        "p_visible_tick_per_below_full_frame": round(p_tick_below, 4),
        "p_tick_per_frame_at_decoded_channel_cadence": round(p_tick_cap, 4),
        "hard_cap_multiplier_if_every_coincident_hit_fully_hidden": round(mask_cap, 4),
        "C11_estimate_multiplier": round(1848 / 1606, 3)},
    "E3_window_composition": {
        "pooled_first10s_hp_per_s": round(I10 / D10, 1),
        "oracle_first10s_hp_per_s": oracle_first10,
        "ratio_first10s": round(oracle_first10 / (I10 / D10), 3),
        "idle_tails_at_full_s_151_159": round(tails, 2),
        "rate_excluding_idle_tails": round(I / (D - tails), 1)},
    "E4_heal_over_intake_is_a_telescoping_identity": {
        w: {"heal_minus_intake": base[w]["heal_hp"] - base[w]["intake_hp"],
            "net_hp_change": base[w]["net_hp_change"]} for w in range(151, 161)},
    "bounds": {
        "most_generous_true_referent_hp_per_s": round(rate2 * mask_cap, 1),
        "ratio_floor_A0": round(oracle_A0 / (rate2 * mask_cap), 3)},
}
json.dump(out, open(sys.argv[1], "w"), indent=1)
print(json.dumps({k: out[k] for k in ("method_reproduced", "E1_health_max_step_counted_as_intake",
                                       "E3_window_composition", "bounds")}, indent=1))
print("masking", {k: v for k, v in out["E2_masking_by_same_frame_heal"].items() if k != "update_grid"})
