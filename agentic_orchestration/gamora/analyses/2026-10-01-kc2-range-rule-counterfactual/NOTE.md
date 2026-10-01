# KC2-PLAY · KP-199: what GD's fire-range rule does to lethality (a counterfactual)

> ## ⚑ NOT-A-GRADED-RUN
> This is a diagnostic counterfactual. No sealed cell was opened, re-run or moved. The oracle (engine `22cd2288`), the pack and the port were all read-only. Every patch is an in-process wrap, undone in `finally`. **Nothing was tuned.** No arm is a candidate oracle. An arm that lands near the referent is a number, not a proposal.

**Seat:** gamora · **Conductor:** gandalf · **Date:** 2026-10-01 · **Ledger:** KP-199 ("gamora prices the range rule's lethality effect in memory, so Matt sees its size before the cut")

## Method

- **Harness.** `gamora_kc2_play_c11a_fold_pricing_2026_09_30.run_arm("PW-FOLDED")` plus `c11._capture`, reused the way legolas's `p05_counterfactual.py` uses them. This is the M-POL-2 seat, the oracle state behind ×3.17.
  - Salts 0–19, waves 151–160, Leg B death-continued, landed grain.
  - Run from the engine checkout at `d2d9ee1f`. It differs from `22cd2288` only by new JOIN-1 scripts; no oracle file differs.
  - `PYTHONDONTWRITEBYTECODE=1`, so nothing was written into the engine.
- **Inputs.** legolas's range audit (collab `2eb2ca138`):
  - `range_audit_per_attack.csv`, keyed `(record, slot, pack_skill)`. 1,814 of the 1,816 AI-initiated rows match a loaded slot, all of them exactly: 0 rows have a `pack_reach_m` that disagrees with the loaded `reach_m`. Every patched slot is listed by `pack_row_id` (old → new) under `patched_rows_by_mode` in the results JSON.
  - `p05_spawn_activation.csv` supplies `gd_spawn_anim_s` and the special slots' `Timeout`. All 31 p05 records are present, and all 520 p05 bodies had animation data.
- **"AI-initiated"** means `delivery_class` starts with `AI-INITIATED`: the basic, chain_initial, chain_next, tree_attack and special1–5 slots. These rows were left as packed in every arm:
  - `initial`, `toggled_aura` and `dying`;
  - the 15 aura rows legolas flags (not in scope here).
- **Metric** (KP-135): landed hp/s to the player over waves 151–159, pooled across salts, ÷ 1605.6.
- **Noise.** Each arm's delta against A0 is a **paired per-salt** mean, with a t-based 95% interval (n = 20, and n = 5 for the 0–4 subset).

### The arms

| arm | `reach_m` on AI-initiated slots | spawn |
|---|---|---|
| **A0** | as packed (control) | as oracle |
| **A1** | `gd_use_range_centre_m_HI` | as oracle |
| **A2** | `gd_use_range_centre_m_LO` | as oracle |
| **A3** | HI | GD p05 spawn behaviour (below) |
| **A4** | `min(pack, HI)`: the over-range rows clipped, the short rows left alone | as oracle |
| **A5** *(added)* | as packed | GD p05 spawn behaviour: separates A3's two halves |
| **A6** *(added)* | `max(pack, HI)`: the short rows raised, the over-range rows left alone (A4's mirror) | as oracle |
| **A1-BAND** *(sensitivity)* | `gd_reference_reach_m`: HI, with specials capped at the band max (`min(ladder+radii+0.5, bandMax+radii)`) | as oracle |

### Which parts of GD's spawn behaviour A3 and A5 model

- **The 4.0 s pre-spawn absence.** The oracle *already* does this (`P05_FIRST_ARRIVAL_S = 4.0`: a body is not on the board before then). The drawn, un-hittable hold exists only in the port. So no patch was needed, and A3 does not differ from A0 on this piece.
- **The spawn animation**, for `gd_spawn_anim_s` (by record) after release, implemented in four parts:
  1. `is_opportunity` returns False, so there are no swings and no aura ticks.
  2. `note_position` does not anchor φ, so the swing clock starts at the first in-reach tick after the animation.
  3. Pursuit travel is suppressed through the mover's existing named hold (`mech_hold_until_t_s`).
  4. The body stays on the board, so it can be hit and **killed**. 25 bodies (A3) and 50 bodies (A5) died during their animation.
- **Specials are armed after their `Timeout`.** A p05 body's special slot cannot be offered before `anim end + Timeout`. This is **composed with** the incumbent `delay_s` wave-clock gate rather than replacing it: it only defers, and the incumbent gate is untouched.

### What was left out, and why

- **The order of acquisition and the alert hold.** The armed B-5 alert hold runs *concurrently* with the animation (the max of the two), not sequentially. Sequential is not decoded. Concurrent is the lower-deferral reading.
- **Pets summoned by p05 bodies** are not deferred.
- **Animation speed** is taken as 1.0 (legolas's `INFERRED`).
- **The special-band minimum** (`bandMin`) is not modelled. It would need a second gate in `choose_slot`, so A1-BAND carries the band max only.
- **GD's ranged monsters stop at their use range** (README § 7). The oracle still halts every body at 2.4 m. That pursuit rule is untouched, and the direction of its effect is not priced here.

## Results (salts 0–19; the 0–4 subset in brackets)

The A6 numbers come from a second run, `…_A6_raise-only_salts0-19.json`, whose A0 is bit-identical to the main file's.

| arm | ratio vs referent | Δ vs A0, paired mean [95% CI] | mean leg-A death wave | salts dying in 151 | deaths per salt, 151–160 (Leg B) | `t_s` pooled, 151–159 |
|---|---|---|---|---|---|---|
| **A0** | **×3.243** (×3.170 ✓) | — | 154.3 | 1/20 | 3.25 | 2,530 s |
| A1 (HI) | ×3.501 (×2.955) | +0.188 [−0.03, +0.40] | **151.25** | **18/20** | **5.75** | 1,941 s |
| A2 (LO) | ×3.647 (×3.321) | +0.324 [+0.08, +0.57] | 151.45 | 16/20 | 5.05 | 2,098 s |
| A3 (HI + spawn) | ×3.586 (×3.723) | +0.287 [+0.08, +0.49] | 151.6 | 16/20 | 5.80 | 1,985 s |
| A4 (clip only) | **×3.030** (×3.070) | **−0.212 [−0.35, −0.07]** | 154.2 | 1/20 | 2.90 | 2,616 s |
| A5 (spawn only) | ×3.158 (×3.143) | −0.083 [−0.21, +0.04] | 154.75 | 0/20 | 3.25 | 2,554 s |
| A6 (raise only) | ×3.456 | +0.201 [+0.06, +0.35] | 151.2 | 18/20 | 6.45 | — |
| A1-BAND | ×3.531 (×3.402) | +0.242 [+0.04, +0.44] | 151.15 | 19/20 | 5.10 | 2,089 s |

- **The control reproduces exactly:** ×3.1703 on salts 0–4, ×3.2431 on 0–19, and leg-A terminals `[156, 152, 155, 152, 152]` with the same t-into-wave values.
- **Salt noise:** the per-salt SD of the control ratio is 0.169 (0.186 on salts 0–4).
- **Two numbers have to be read together: the ratio and the deaths.** Under Leg B a death ends the wave, so `t_s` (the denominator) shrinks when deaths rise. In A1 that loss is −23%. The ratio therefore understates how much more lethal A1, A3 and A6 are. **The death columns are the less ambiguous reading.**

### Landed hp/s by source (waves 151–159, pooled)

| arm | ranged | melee | aura/initial | dying | summon | p05 | ring | **> 12.69 m (off-screen)** | ≤ 3 m |
|---|---|---|---|---|---|---|---|---|---|
| A0 | 2,645 | 1,052 | 1,049 | 248 | 83 | 722 (13.9%) | 4,278 | **995 (19.1%)** | 2,122 |
| A1 | 3,497 | 875 | 853 | 136 | 116 | 842 (15.0%) | 4,523 | 1,037 | 1,579 |
| A2 | 3,647 | 908 | 885 | 184 | 106 | 805 | 4,825 | 994 | 1,829 |
| A3 | 3,637 | 906 | 782 | 174 | 107 | 787 (13.7%) | 4,717 | 934 | 1,667 |
| A4 | 2,432 | 901 | 1,097 | 235 | 80 | 734 | 3,937 | **747** | 2,069 |
| A5 | 2,596 | 1,024 | 984 | 269 | 75 | **629 (12.4%)** | 4,250 | 954 | 2,074 |
| A6 | 3,425 | 882 | 863 | 130 | 113 | 1,004 | 4,302 | 1,260 | 1,464 |

How the classes are defined:
- **Ranged vs melee** follows the slot's GD `distanceProfile`: Melee or absent counts as melee, anything else as ranged. The classification is fixed across arms.
- **Hit distance** is measured from the source to the player at the cast.
- **Small classes:** about 130 hp/s are `other/unkeyed` (pet or child-skill rows), and about 6 are DoT ticks with no position.

## My read

1. **The range rule does not explain the ×3.17, and adopting it in full moves the oracle further from the referent, not closer.**
   - In A1 the ratio does not fall (+8% pooled; the CI spans 0).
   - The player now dies in **wave 151** on 18 of 20 salts, against 1 of 20 in A0 and wave 160 in the referent. Deaths per salt rise from 3.25 to 5.75.
   - The LO limb (A2), the band-capped sensitivity (A1-BAND) and A3 with spawn behaviour all tell the same story.
2. **Taken by direction, the rule has two opposing halves of similar size, and the "too short" half wins:**
   - **Clipping the 809 over-range rows (A4)** gives −6.6% on the ratio, with a CI that excludes 0. Off-screen landed damage falls by a quarter (995 → 747 hp/s), but the death wave does not move (154.2) and deaths per salt fall only from 3.25 to 2.90. **This is Matt's off-screen complaint, and it is real but small: it is worth about 0.2 of the 3.2.**
   - **Raising the 1,005 short rows (A6)** gives +6.6%, a CI that excludes 0, and death in wave 151 on 18 of 20 salts. Most of these rows are the 2.4 m melee fallback applied to attacks that GD fires from Moderate or Long range. Raised, ring bodies start their swing clocks and fire from 9–17 m on spawn, before the pilot reaches them. Ranged ring damage goes from 2,346 to 3,154 hp/s in A1.
3. **GD's spawn behaviour is a small lethality lever (A5):**
   - −2.6%, with a CI that spans 0;
   - p05's share of landed damage falls from 13.9% to 12.4%;
   - 50 p05 bodies die inside their animation;
   - the death wave moves from 154.3 to 154.75.

   On top of GD ranges (A3 vs A1) it is within noise. It matches what Matt felt: he no longer gets shot instantly by bodies that are still spawning. **But it is fidelity, not calibration. It is the eighth mechanism that does not close the ×3.**
4. **Answering the conductor's question directly:**
   - The over-range half of the range rule explains about 6–7% of the ×3.17.
   - The spawn behaviour explains about 2–3% at most.
   - The rule *in full* explains none of it, because its other half adds about as much lethality again and moves the death wave from 154 to 151.

   This is a pricing, not an objection to v3.8. Ruling (1), "both directions, because it is GD's own rule", is a fidelity ruling, and these numbers say that **v3.8 will make the oracle deadlier, and the re-derived expected values will move away from the referent.** That should be seen before the prereg v1.14 budget is spent.
5. **A candidate interaction, flagged and not priced.** The oracle still marches every body to 2.4 m. GD's ranged bodies stop at their use range (README § 7). With longer GD reach, bodies in the oracle fire from range **and** keep closing into the pilot's kill zone. Which way this pursuit rule moves lethality is unknown. It is the next lever this result points at; it belongs to a separate commission.

## Files

- `range_rule_counterfactual.py`: the script. Run it from `reincarnated-engine/src` as `python3 <path> 20 A0,A1,... <out.json>`. The full set takes about 13 minutes.
- `range_rule_counterfactual_results_PW-FOLDED_salts0-19.json`: arms A0 to A5 and A1-BAND. Per arm and for the 0–4 subset it carries:
  - the per-salt ratios;
  - the leg-A terminals;
  - the Leg B death waves;
  - the source breakdowns (`by_cls`, `by_grp`, `by_bin`, `by_grp_cls`);
  - burst statistics;
  - spawn telemetry;
  - `deltas_vs_A0`;
  - the patched rows by mode.
- `range_rule_counterfactual_results_A6_raise-only_salts0-19.json`: A0 (identical) and A6.

*gamora · KC2-PLAY · KP-199 · 2026-10-01 · NOT-A-GRADED-RUN*
