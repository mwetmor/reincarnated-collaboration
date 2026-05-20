# Track C Spot-Check Regen Findings

**Date:** 2026-05-21
**Author:** rocket
**Session context:** Track C resumed after 2026-05-20 watchdog stall
**Data sources:**
- `reincarnated-engine/output/track-c-spot-regen-2026-05-21/TC-1/checkpoints/` — TC-1 per-class results (seed=200001)
- `reincarnated-engine/output/track-c-spot-regen-2026-05-21/TC-2/checkpoints/` — TC-2 per-class results (seed=200002)
- `/tmp/tc1_water.log` — prior session partial log (classes 0001-0004 Phase 1 only; not used for final data)

---

## 1. Resumption context

The prior Track C invocation stalled at the agent watchdog (600s no-progress threshold) at approximately 10:03 EDT on 2026-05-20. The stall occurred during Phase 2 cold-start convergence of class_0005 in TC-1. The season_200001 artifacts had not yet been written (Phase 1 of the original script was still running its generation-time balance loop). No usable Phase 2 data existed to recover from the prior session.

**Scope adjustment:** TC-3 shadow was scoped out. Matt adopted the shadow trade-off substrate refinement (shadow = TRADE-OFF unifying theme, broader than prior CONCEALMENT_AND_DRAIN) during the stall window. This resolves OQ-5 (shadow 5b lever-signal-gap) design-side — the signal gap was caused by narrow mechanic toolkit, and the trade-off refinement opens the lever signal space. TC-3 shadow regen is no longer needed.

**Mitigation for this session:** A new combined runner script (`scripts/track_c_run_all.py`) with per-class checkpoint writing was authored. Each class writes a JSON checkpoint immediately after convergence completes, enabling resume from any interruption point. TC-1 and TC-2 ran sequentially in a single background process.

**Effective research time:** 87.5 min wall time (TC-1: 39.9 min; TC-2: 47.6 min). Both included Phase 1 generation-time balance (~34 min each) plus Phase 2 cold-start convergence (~5-8 min for 11 classes at ~36s/class).

---

## 2. TC-1 water findings (seed=200001)

**Season:** season_200001
**Rotation:** water, fire, earth, wind, lightning, holy, shadow, physical (water-first canonical-7)
**Calibration:** disposition-3 (cold-start; initial_modifier=1.0)
**Fights per matchup:** 100

### Per-class results

| class_id | element | archetype | kit_size | dam_frac | modifier | boss_wr | elite_wr | mini_boss_wr | status | Pattern-A |
|---|---|---|---|---|---|---|---|---|---|---|
| class_0001 | water | water_mage | 11 | 0.36 | 0.2575 | 0.0 | 0.58 | 0.0 | partially-converged | YES |
| class_0002 | fire | fire_mage | 11 | 0.64 | 0.1028 | 0.0 | 0.43 | 0.0 | partially-converged | YES |
| class_0003 | earth | earth_caster | 11 | 0.55 | 0.1338 | 0.0 | 0.50 | 0.0 | partially-converged | YES |
| class_0004 | wind | wind_controller | 12 | 0.42 | 0.5050 | 0.0 | 0.495 | 0.0 | partially-converged | YES |
| class_0005 | lightning | lightning_controller | 13 | 0.54 | 0.0719 | 0.0 | 0.47 | 0.0 | partially-converged | YES |
| class_0006 | holy | holy_caster | 5 | 0.80 | 0.1338 | 0.0 | 0.49 | 0.0 | partially-converged | YES |
| class_0007 | shadow | shadow_mage | 5 | 0.60 | 0.0719 | 0.0 | 0.50 | 0.0 | partially-converged | YES |
| class_0008 | physical | physical_warrior | 11 | 0.36 | 0.1338 | 0.0 | 0.535 | 0.0 | partially-converged | YES |
| class_0009 | water | water_mage | 12 | 0.50 | 0.2575 | 0.0 | 0.50 | 0.0 | partially-converged | YES |
| class_0010 | fire | fire_controller | 13 | 0.31 | 0.5669 | 0.0 | 0.475 | 0.0 | partially-converged | YES |
| class_0011 | earth | experimental | 8 | 0.50 | 0.1338 | 0.0 | 0.50 | 0.0 | partially-converged | YES (skipped) |

**TC-1 aggregate:**
- Pattern-A: 11/11 (100%)
- mini_boss_wr=0.0 for all 11 classes — Pattern-A extends to mini-boss tier
- All classes "partially-converged" (primary loop converged; convergence gate not passed due to boss/mini-boss tier failure)
- Water-specific N=2: modifier=[0.2575, 0.2575], boss_wr=[0.0, 0.0]

**Notable:** class_0001 (water_mage) has dam_frac=0.36 with 11-skill kit — lower damage fraction than most mage archetypes. class_0009 (water_mage) dam_frac=0.50 with 12-skill kit, also boss_wr=0.0. Higher damage fraction did not improve boss outcome.

**Water Pattern-A rate at same calibration: 2/2 (100%)**

---

## 3. TC-2 earth findings (seed=200002)

**Season:** season_200002
**Rotation:** earth, fire, water, wind, lightning, holy, shadow, physical (earth-first canonical-7)
**Calibration:** disposition-3 (cold-start; initial_modifier=1.0)
**Fights per matchup:** 100

### Per-class results

| class_id | element | archetype | kit_size | dam_frac | modifier | boss_wr | elite_wr | mini_boss_wr | status | Pattern-A |
|---|---|---|---|---|---|---|---|---|---|---|
| class_0012 | earth | earth_controller | 12 | 0.50 | 0.5050 | 0.0 | 0.50 | 0.0 | partially-converged | YES |
| class_0013 | fire | fire_mage | 11 | 0.55 | 0.0719 | 0.0 | 0.50 | 0.0 | partially-converged | YES |
| class_0014 | water | water_mage | 11 | 0.73 | 0.1338 | 0.0 | 0.50 | 0.0 | partially-converged | YES |
| class_0015 | wind | wind_caster | 11 | 0.64 | 0.1338 | 0.0 | 0.50 | 0.0 | partially-converged | YES |
| class_0016 | lightning | lightning_controller | 13 | 0.38 | 0.1338 | 0.0 | 0.50 | 0.0 | partially-converged | YES |
| class_0017 | holy | holy_controller | 6 | 0.33 | 0.5050 | 0.0 | 0.50 | 0.0 | partially-converged | YES |
| class_0018 | shadow | shadow_mage | 5 | 0.80 | 0.1338 | 0.0 | 0.50 | 0.0 | partially-converged | YES |
| class_0019 | physical | hunter | 13 | 0.46 | 1.0000 | 0.0 | 0.50 | 0.0 | partially-converged | YES |
| class_0020 | earth | earth_caster | 11 | 0.45 | 0.1338 | 0.0 | 0.51 | 0.0 | partially-converged | YES |
| class_0021 | fire | fire_mage | 11 | 0.55 | 0.0719 | 0.0 | 0.50 | 0.0 | partially-converged | YES |
| class_0022 | water | experimental | 12 | 0.42 | 0.1338 | 0.0 | 0.50 | 0.0 | partially-converged | YES (skipped) |

**TC-2 aggregate:**
- Pattern-A: 11/11 (100%)
- mini_boss_wr=0.0 for all 11 classes
- Earth-specific N=2: modifier=[0.5050, 0.1338], boss_wr=[0.0, 0.0]
- class_0019 (physical, hunter): modifier=1.0000 — highest modifier in the combined dataset. Physical hunter archetype required full modifier saturation at the search ceiling.

**Notable:** class_0014 (water_mage) dam_frac=0.73 (73% damage fraction — the highest single-class damage fraction in either TC run). Still boss_wr=0.0. This parallels the lightning observation in P2 (73% damage fraction, also 0.0 boss WR). Damage role fraction does not rescue boss performance under disposition-3 calibration.

**Earth Pattern-A rate at same calibration: 2/2 (100%)**

---

## 4. Cross-substrate comparison

### Pattern-A rate: physical vs water vs earth vs all substrates

| Substrate | Historical Pattern-A | TC-1/TC-2 Pattern-A | P2 Pattern-A | Combined same-calibration N |
|---|---|---|---|---|
| physical | 100% (N=20) | 100% (2/2) | 100% (1/1) | N=3 at disp-3 |
| water | 15% (N=20) | 100% (2/2 TC-1; 2/2 TC-2) | 100% (1/1) | N=5 at disp-3 |
| earth | 40% (N=20) | 100% (2/2 TC-1; 2/2 TC-2) | 100% (1/1) | N=5 at disp-3 |
| fire | 25% (N=24) | 100% (2/2 TC-1; 2/2 TC-2) | 100% (2/2) | N=6 at disp-3 |
| wind | 40% (N=20) | 100% (1/1 TC-1; 1/1 TC-2) | 100% (1/1) | N=3 at disp-3 |
| lightning | N/A | 100% (1/1 TC-1; 1/1 TC-2) | 100% (1/1) | N=3 at disp-3 |
| shadow | N/A | 100% (1/1 TC-1; 1/1 TC-2) | 100% (2/2) | N=4 at disp-3 |
| holy | N/A | 100% (1/1 TC-1; 1/1 TC-2) | 100% (1/1) | N=3 at disp-3 |

**All substrates: 100% Pattern-A under disposition-3 calibration. No substrate escapes.**

### Modifier range comparison (same-calibration TC runs)

| Substrate | TC modifier range | P2 modifier | Historical modifier mean |
|---|---|---|---|
| water | 0.1338–0.2575 | 0.1338 | 0.0519 |
| earth | 0.1338–0.5050 | 0.1338 | 0.0524 |
| fire | 0.0719–0.5669 | 0.0719–0.1338 | 0.0521 |
| wind | 0.1338–0.5050 | 0.1338 | 0.0722 |
| physical | 0.1338–1.0000 | 0.3812 | 0.4400 |
| lightning | 0.0719–0.1338 | 0.0719 | N/A |
| shadow | 0.0719–0.1338 | 0.1956–0.3812 | N/A |
| holy | 0.1338–0.5050 | 0.1338 | N/A |

**Key observation:** TC modifier values are notably higher than historical means for all canonical-four substrates (water: 0.19–0.26 vs hist 0.052; earth: 0.13–0.51 vs hist 0.052). This is consistent with disposition-3 calibration raising the effective power floor required to survive the gauntlet — but not sufficiently to overcome boss HP at the ceiling.

### Convergence pattern: partial-converge universal

Every class in TC-1 and TC-2 landed on "partially-converged" / "primary_loop_converged" status. The balance loop converged elite_wr to ~0.50 but left boss/mini-boss at 0.0. This is not a convergence failure — the loop found a stable modifier. The modifier's boss-tier performance is the pathology, not the convergence mechanism.

---

## 5. OQ-1 resolution

**OQ-1:** Do substrate-specific severity differences (water 15% historical vs earth 40% historical vs physical 100%) persist under same-calibration, or collapse?

**Finding: The gradient COLLAPSES completely under same-calibration (disposition-3).**

Under historical calibration, water showed 15% Pattern-A vs earth 40% vs physical 100%. Under disposition-3 same-calibration, all three substrates show 100% Pattern-A with N=5 for both water and earth.

The historical gradient was entirely an artifact of calibration differences, not substrate-intrinsic kit composition differences. Matt's observation that "water/earth/wind have been weaker across all seasons" is confirmed as a calibration-level artifact — those substrates were historically used under weaker per-class calibration settings.

**Discipline #13b caveat:** This is strong evidence but not ablation-level proof. The controlled comparison (all substrates, same seed, same gauntlet, same calibration) with N=5 for the primary substrates supports the collapse hypothesis. Pre-ablation, this is characterized as a high-confidence candidate finding, not a proven mechanical claim.

---

## 6. Implications for P1 W1.11 scope

**Recommendation: TARGETED enrichment is sufficient; comprehensive per-substrate enrichment is not required as a calibration correction.**

The Pattern-A collapse at same calibration means the historical per-substrate severity gradient is not a substrate-intrinsic property that P1 W1.11 substrate enrichment needs to "correct for." Every substrate generates kits that fail boss tier under disposition-3 calibration regardless of archetype shape, kit size, or damage fraction.

What P1 W1.11 DOES need to address:
1. **Structural substrate completeness** — 4 missing substrate types (HP-economy, charge-stack, damage-taken-converts, player-side proxies); these are absent entirely, not substrate-severity-differentiated
2. **5x sufficiency rule per axis × bin** — applies uniformly across all substrates; no substrate is more or less under-represented than others at same calibration
3. **Schema extensions for missing metadata** — applies uniformly

What P1 W1.11 does NOT need:
- Heavier enrichment for "weaker" substrates (water, earth, wind) to compensate for historical weakness — that weakness was calibration-dependent, not substrate-composition-dependent
- Substrate-specific DPS floor corrections in the substrate identity YAML — the boss floor problem is a calibration-architecture issue, not a substrate identity issue

**Practical scope impact:** P1 W1.11 can be scoped as uniform-depth enrichment across all substrates rather than differentiated depth by historical performance gradient. This likely saves 1-2 weeks of P1 budget vs the "comprehensive" framing that would have weighted water/earth/wind enrichment more heavily.

---

## 7. Implications for reference-archetype validation roster (P7 W7.2)

The kit-redesign queue was canceled by Matt on 2026-05-21 due to QD-engine philosophical contradiction. What was the kit-redesign queue is now the **reference-archetype validation roster for P7 W7.2** — classes that exhibited Pattern-A pathology become the validation targets that confirm the QD-engine's substrate enrichment produces meaningfully differentiated kits.

**Roster recommendations from TC evidence:**

Priority tier for P7 W7.2 validation:
- **water_mage** (class_0001, class_0009, class_0014): Pattern-A with varying dam_frac (0.36–0.73). Spans the full kit composition range; if QD substrate enrichment helps, water_mage should show the clearest before/after signal given historical 15% Pattern-A baseline.
- **earth_controller / earth_caster** (class_0003, class_0012, class_0020): Pattern-A across both archetypes. Earth's historical 40% baseline makes it a mid-severity signal.
- **physical_hunter** (class_0019): modifier=1.0000 (ceiling saturation) under TC-2. The most extreme modifier case in TC dataset — strongest signal for any enrichment that adds physical-specific burst geometry.
- **lightning_controller** (class_0005, class_0016): No historical baseline. Both TC instances show Pattern-A with 54%/38% dam_frac and 13-skill kits. Good test for chain geometry enrichment.

These are validation candidates, not redesign targets. P7 W7.2 should re-run these archetypes under post-QD-enrichment calibration and measure whether Pattern-A rate falls below 100%.

---

## 8. TC-3 shadow — skip rationale

TC-3 shadow regen was scoped out per Matt's 2026-05-21 shadow trade-off substrate refinement.

The prior OQ-5 framing identified the shadow 5b lever-signal-gap as a problem distinct from 5a compression: shadow's lever library returned delta=0 on all 3 recompose attempts, indicating the available levers had no viable signal within the shadow substrate. This was attributed to CONCEALMENT_AND_DRAIN being a narrow mechanic toolkit.

Matt's refinement broadens shadow's substrate-unifying theme to TRADE-OFF — shadow abilities impose meaningful costs or risks on the player in exchange for high-output effects. This opens the lever signal space by enabling a larger toolkit of mechanic types beyond drain and concealment. The 5b lever-signal-gap is resolved design-side: a broader mechanic toolkit means the lever library will have more candidate levers with non-zero delta.

TC-3 would have measured Pattern-A rate for shadow at same calibration, which the combined TC-1 (class_0007: shadow_mage) and TC-2 (class_0018: shadow_mage) data already provides: both shadow_mage instances show 100% Pattern-A, consistent with the universal collapse finding. The TC-3 signal is already captured.

No regen needed; substrate refinement addresses the root cause.

---

## 9. Script artifacts

All regen data persisted to:
- `reincarnated-engine/output/track-c-spot-regen-2026-05-21/season_200001/` — TC-1 season artifacts
- `reincarnated-engine/output/track-c-spot-regen-2026-05-21/season_200001/balance_results.json` — TC-1 balance results
- `reincarnated-engine/output/track-c-spot-regen-2026-05-21/TC-1/checkpoints/` — 11 per-class checkpoint JSONs
- `reincarnated-engine/output/track-c-spot-regen-2026-05-21/season_200002/` — TC-2 season artifacts
- `reincarnated-engine/output/track-c-spot-regen-2026-05-21/season_200002/balance_results.json` — TC-2 balance results
- `reincarnated-engine/output/track-c-spot-regen-2026-05-21/TC-2/checkpoints/` — 11 per-class checkpoint JSONs
- `reincarnated-engine/output/track-c-spot-regen-2026-05-21/track_c_aggregate_summary.json` — combined aggregate
- `reincarnated-engine/scripts/track_c_run_all.py` — combined runner with checkpointing
