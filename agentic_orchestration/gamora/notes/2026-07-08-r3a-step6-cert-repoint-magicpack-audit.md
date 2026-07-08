# gamora completion note — R3a step-6: cert re-point (part a) + magic_pack band audit (part b)

**Author:** gamora (simulation seam)
**Date:** 2026-07-08
**For:** Gate-2 reviewer (jack-ryan). Matt fires the Gate-2 review + step-4-bis; routing to jack-ryan is not
  mine to do (per dispatch).
**Chain:** batch-2 autonomous chain, step R3a-6 (certification re-point). Ratified follow-through on Matt's
  A-ruling of gandalf's §4 acceptance-layer reframe; jack-ryan CLEARED-WITH-CONDITIONS
  (`qa/findings/2026-07-08-jackryan-s4-reframe-review.md`).
**Math note (authored BEFORE code, Disc #1):** `simulation/math/r3a-step6-magicpack-band-audit-2026-07-08.md`
**Tag:** `gamora/v-r3a-step6-cert-repoint-magicpack-audit-1`
**Cost:** $0 (code + math-note on existing data; no gauntlet re-runs).

---

## The two deliverables, and their verdicts

### Part (a) — certification re-point: CODE DELTA IS ZERO (reported truth)

The dispatch asked me to confirm whether any code path DEMANDS a tier-2 WR gradient / mid-mass distribution as a
pass condition, and to remove it if so — OR to report explicitly that the gradient was only ever an overlay
criterion in gandalf's note, never coded (which "would make the code delta near-zero and is a legitimate
outcome").

**It is that outcome, and it is not near-zero — it is exactly zero.** I re-verified the full gating spine
against source (`gauntlet_sim.py`):

```
season_emit (:966) → gauntlet_pass (:905) → family_certification_pass (:864)
  → family_passed (:850) → _shell_result_passed (:810)   ← the ONLY per-shell pass predicate
```

`_shell_result_passed` splits exactly two ways and neither demands a WR gradient:
- **CLEAR shells** (open_arena, chokepoint, magic_pack, elite_pack): `cohort_band[0] <= tier_2_kpm <=
  cohort_band[1]` (:847-848) — a KPM band range check. No WR term.
- **BOSS shells** (boss_with_adds, mini_boss): `tier_2_survival_rate >= SURVIVAL_FLOOR_BY_COHORT[cohort]`
  (:825-830) — a `>=` THRESHOLD on survival, i.e. **already a validity bit**, never a demanded gradient.

I also checked the only other place a mean survival is computed: `wave5_season_orchestrator.py:195-202` q3
(`resource_sustainability = mean tier_2_survival_rate`) — a season-QUALITY vector dimension, clamped [0,1],
reported/exported, NOT consumed by any pass gate. Grep of the seam returns ZERO `gradient`/`mid_mass`/`mid-mass`
hits in any gating path.

**So: the §4 WR-gradient acceptance criterion was ONLY EVER an overlay in gandalf's design note. The gate
already reads (i) a KPM band on clear shells and (ii) a survival validity-bit threshold on boss shells. There is
nothing to remove.** The reframe brings the acceptance CRITERION into line with what the code already does — no
code change to the gate is required. This matches (and is smaller than) jack-ryan's review §2 finding: "a SMALL
overlay-correction, not a re-architecture." The non-viability FLAG surface the dispatch part (a) mentions ("a
cell that cannot engage emits a flag rather than silently reading as a floor-fail") is ALREADY served by the
step-5 `tier_1_reject_breakout` in-JSON aggregate — `reject_below_floor` / `reject_no_kpm` ARE the flags; a cell
that kills zero shows `reject_no_kpm`, a cell that can't clear in time shows `reject_below_floor`. No new flag
machinery needed.

### Part (b) — magic_pack band audit (CONDITION 1): STALE, re-derived — but the DIAGNOSIS DIFFERS from step-5

`magic_pack` `(18.61, 100.00)` → **`(12.52, 102.86)`**. Density-anchored via `KPM = 24 × 60 / clear_s`
(exact for all_mobs_killed + KILLS_ONLY full clear). `_route_tier_1` byte-identical; every other shell
byte-identical.

**Provenance (Disc #13):** the T1.3 band (`02467b3f`, 2026-06-21) was p10/p90 of the OLD **4-MOB-PROBE**
540-fight in-domain population. magic_pack was re-rolled to a **24-mob** champion-pack-at-density room
(2026-07-07). The band is stale on BOTH endpoints — fit to a 6× smaller mob_count. (The 100.0 ceiling was a
4-mob 2.4s-clear p90; at 24 mobs it coincidentally maps to a ~14.4s clear, ~sane but by accident of the number,
not by density-anchoring.)

**The crux for Gate-2 — magic_pack is NOT the step-5 shape. It is genuinely TRIMODAL** (step-4 re-run data,
n=189):

| mode | cells | distinct kits | tier_1_kpm | implied clear | reading |
|---|---|---|---|---|---|
| LOW | 117 | 13 | 8.7–11.0 | 130–166s | TIMEOUT partial-clear (~17–22 of 24 killed at the 120s cap → CANNOT full-clear) — GENUINE below-floor |
| MID | 36 | 4 | 23.7–91.9 | 16–61s | healthy in-band |
| HIGH | 36 | 4 | 101–144 | 10–14s | power-fantasy faceroll tail |

Kit tripartition is CLEAN: 13/4/4 distinct kits, **ZERO LOW-HIGH kit overlap.** This is the opposite of step-5's
open_arena/chokepoint, where 100% of cells rejected ABOVE ceiling from ONE coherent mode (pure stale-ceiling
artifact). So my verdict is NOT "re-derive to admit the whole shifted mode" — it is:

- **Floor is NOT the load-bearing endpoint here.** The 117 LOW-mode timeouts reject below-floor whether the
  floor is the stale 18.61 OR the density-honest 12.52 (they cluster at ~8.7–11, below both). Re-deriving to
  12.52 makes the floor number density-HONEST (the 120s-window timeout anchor = what the room's win_condition
  actually demands) WITHOUT changing which cells reject. The 117 timeouts STAY below-floor as a genuine content
  finding — a FLAGGED non-viability (via the breakout), not an emission-gate under the reframe.
- **Ceiling is stale-low; re-derived it PASSES anti-curve-fit (rider-4).** Geometry ceiling 102.86 (~14s brisk
  champion-pack sweep of the shallow 32.7×14 clustered room) lands **~1.4 KPM ABOVE observed p90 (101.48)** —
  the honest-anchor signature (a curve-fit lands ON p90; the stale 100.0 sat on/below p90 = the 4-mob-era p90
  residue). It admits the HIGH-mode ~10–14s fast-clears (the §4-reframe's live discrimination signal; genre
  principle: a caster deleting trash is the power fantasy, NO mob-HP inflation).

**Honesty caveat I am surfacing (same class as jack-ryan's step-5 INFO note on the 24s choke ceiling):** the
~14s fast-sweep is a COARSE brisk-sweep judgement on a shallow-clustered room — thinner anti-curve-fit margin
(~1.4 KPM) than step-5 choke's funnel-throughput derivation (which had the room's documented AOE-concentration
cert intent to anchor to). The test passes, but if magic_pack later rails at the 102.86 ceiling, revisit with a
finer per-bite AOE-throughput model. I did NOT move the ceiling to green cells — it is geometry-grounded and
lands past p90 with headroom.

**Pure-KPM re-band effect (verified against the step-4 data):** in-band 36→**54** (+18 fast-clears admitted),
above-ceiling 36→**18**, below-floor **117** (unchanged). Note the breakout re-aggregation caveat below.

## Residual-reject breakout for magic_pack (dispatch asked for this)

Pre-audit state (from the step-4 re-run `tier_1_reject_breakout`, old band 18.61–100): magic_pack
**entered_tier2=36 / reject_above_ceiling=36 / reject_below_floor=117** (= the 117 below + 36 above the dispatch
cited, out of 189). Post-audit pure-KPM classification under the new band (12.52, 102.86): **in-band=54 /
below-floor=117 / above-ceiling=18** — the re-band admits +18 fast-clear cells (101–102.86 KPM) and shrinks the
above-ceiling tail to the extreme 122–144 faceroll (18 cells); the 117 timeout non-clears are unchanged
below-floor.

**Breakout re-aggregation caveat (surfaced, Disc #11):** `compute_tier_1_reject_breakout` run on the FROZEN
step-4 outcomes buckets `entered_tier2` from the OLD `tier_1_outcome==PROVISIONAL_PASS` decisions (36, old band)
— so on frozen data it reports `{entered:36, above:18, below:135}`, NOT the +18 the new band admits. The true
54-in-band only materializes on a RE-RUN where `_route_tier_1` re-decides against the new band. **This is a $0 /
no-re-run step** (dispatch scope), so the pure-KPM classification (54/117/18) is the honest projection of the
re-band's effect; the frozen-data re-aggregation is an artifact of running the aggregate over prior routing
decisions, not the re-band's effect. This is NOT a defect — it is the correct behavior of running a diagnostic
aggregate over a prior run's frozen decisions, flagged so the Gate-2 reviewer reads the 54 (not the 36) as the
re-band's admission.

## CONDITION 2 — boss KPM-primacy NOT applied (confirmed no-touch)

Boss shells keep gating on the survive-and-kill validity bit (`tier_2_survival_rate >= SURVIVAL_FLOOR`); KPM
band never consulted. `_BOSS_SHELL_GATE_TYPES` (:211-214) + the win-condition split (:192-204) unchanged. The
smoke asserts a boss shell with survival<floor and KPM=999 FAILS, and survival>=floor with KPM=0 PASSES —
proving KPM is ignored on boss shells. The boss_with_adds non-viability finding (117/189 kill zero mobs) is a
parallel CONTENT lane — not touched, not gating this re-point.

## Cohort-invariance + MIGRATION boundary

Cohort-invariance PRESERVED — single tuple ×4 columns, no branch; the LOW/MID/HIGH mode a kit lands in is
kit-driven (spans all 4 cohorts), not cohort-driven, so a single per-shell band is empirically justified.

**NO MIGRATION.md.** Internal to `simulation/`: one clear-shell band constant re-derived (`:462`), predicate
untouched, part (a) added zero code, and NO interface star-lord consumes changed (no telemetry/export/season_emit
schema field — only which cells land in-band, using fields already serialized). Same within-seam boundary as
step-5. **I explicitly state: no migration needed; the change is internal to simulation/.**

## What I did NOT do (dispatch out-of-scope guard)

No gauntlet re-runs ($0). No boss_with_adds content fix (parallel lane). No open_arena/chokepoint tuple change
(step-5 frozen, Gate-2 PASSED). No lethality-floor / game-feel work (post-demo Godot playtest). No descent
difficulty-ladder change (post-demo). No boss-shell gating change (CONDITION 2). No `_route_tier_1` predicate
change. No §4/reframe re-litigation.

## Artifacts + verification

- **Math note:** `simulation/math/r3a-step6-magicpack-band-audit-2026-07-08.md` (authored before code).
- **Code:** `gauntlet_sim.py:462` magic_pack tuple `(18.61,100.00)` → `(12.52,102.86)` + provenance comment.
  Part (a): zero code.
- **Smoke:** `scripts/gamora_r3a_step6_magicpack_cert_repoint_smoke_2026_07_08.py` — PASS (re-band +
  cohort-invariance + other-shells byte-identical + clear-shell KPM gate incl. admitted 102 tail + boss
  survival-bit gate KPM-ignored + breakout flags emit).
- **Regression:** `test_cycle13_wave5_gauntlet_sim` + `test_spatial_gauntlet_scenarios` = **77 green.**
- **Tag:** `gamora/v-r3a-step6-cert-repoint-magicpack-audit-1`.

**Smoke-line:** step-6 smoke PASS + 77 regression green; magic_pack (18.61,100.00)→(12.52,102.86); part (a)
code delta ZERO (WR gradient never coded); boss shells untouched (CONDITION 2); no MIGRATION.

---

**Signed:** gamora, 2026-07-08.
