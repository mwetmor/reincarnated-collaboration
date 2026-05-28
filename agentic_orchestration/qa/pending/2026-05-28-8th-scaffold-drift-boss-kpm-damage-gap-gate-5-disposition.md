# Gate-5 Disposition — 8th Scaffold-Drift Case — Boss-KPM Damage Formula Gap — 2026-05-28

**Reviewer:** jack-ryan
**Severity:** BLOCK (Pattern-B escalation — Matt design call required; Matt D2 re-evaluation hook triggered)
**Authority:** Gate-5 disposition per KR dispatch `agentic_orchestration/dispatches/2026-05-28-jack-ryan-gate-5-8th-scaffold-drift-disposition.md`; Matt D2 re-evaluation hook from Gate-4 ratification (verbatim: "if Track 1 surfaces 8th case materially extending scope, Matt re-evaluates"); Discipline #44 framing-refusal invoked by gamora at `f704599`
**Target:** engine `f704599` + tag `gamora/v2.0-option-f-track-1-per-damage-path-bands-1` + meta `1a2b5a3`
**Developer:** gamora
**Principles applied:** Review Principles 1, 2, 3, 4, 5
**Disciplines cited:** #11, #13a-partition, #18, #39, #40, #41, #42, #44, #45

---

## § 1 — Trigger + Scope

### § 1.1 D2 Re-Evaluation Hook: TRIGGERED

Matt Gate-4 ratification included verbatim: *"Re-evaluation hook: if Track 1 surfaces 8th case materially extending scope, Matt re-evaluates. Don't pre-empt."*

**Trigger condition: MET.** Track 1 closed at engine `f704599` with acceptance FAILED (3/18 emit; ≥12/18 required) AND surfaced findings that extend scope materially beyond the surface-framing gamora hand-back line. Both the surface framing and a deeper framing are load-bearing per Discipline #42. This disposition resolves both before routing to Matt Pattern-B.

### § 1.2 Disposition Scope

This Gate-5 disposition provides:
- § 2: Two-framing separation + Discipline #42 framing-audit
- § 3: Root-cause depth analysis (substrate constants + git/decision lineage)
- § 4: Six ranked options with scope, discipline compliance, and effort estimates
- § 5: Recommendation with rationale
- § 6: Cycle 14 v1 close-criterion impact per option
- § 7: Open questions for Matt Pattern-B ratification

What this disposition does NOT do: implement any option; amend canonical doc § 3.9 or the Track 1 math note; re-run gamora telemetry; retract gamora's sweep data.

---

## § 2 — Two Framings (Discipline #42 Framing-Audit)

### § 2.1 Surface Framing (Gamora Hand-Back Line)

> *"STR/DEX physical kits produce boss KPM=0 because `base_physical_damage_l50` (SC-6b) is uncalibrated against boss HP targets. INT/WIS-faith bands empirically grounded (82.192 INT-magical median; 75.949 WIS-faith median). STR/DEX FALLBACK to prior single-cohort bands."*

**Load-bearing elements of the surface framing:**
- 8 STR/DEX kits produce zero boss KPM observations in Track 1 sweep (verified: `boss_kpm_observations: []` for both `str_physical` and `dex_physical` in telemetry)
- `base_physical_damage_l50` (SC-6b substrate values: martial-heavy=177, martial-light=99, ranged=91 per SC-6b backfill `3c95883`) was computed as `family_baseline × amplitude_mean` — a substrate-design formula, NOT calibrated against endgame boss HP targets
- INT/WIS bands have empirical observations: `int_magical` has 3 observations (73.171, 82.192, 82.192); `wis_faith` has 7 observations (63.83, 68.182, 65.934, 82.192, 78.947, 75.949, 98.361)
- The FALLBACK bands for STR/DEX are the original single-cohort `COHORT_KPM_BAND` values (SC-7-calibrated for INT/WIS reference class) — not calibrated for physical paths

**Assessment of surface framing: CORRECT but UNDERSTATES the structural depth.**

### § 2.2 Deeper Framing (Gamora Empirical Sweep Finding — KR Discipline #42 Audit)

> *"Most kits — including INT kits — produce T1 REJECT at boss encounters (t2_kpm=0.0). Only `artillery_mage` has meaningful boss KPM. The vast majority of INT/WIS kits (int_01 standard_wizard, int_03 pyromantic_caster, int_04 red_mage, int_05 arcane_familiar, wis_01 channeling_cleric, etc.) all produce t1_kpm=0 / t2_kpm=0 at boss encounters."*

**Empirical verification from Track 1 telemetry:**

| Archetype | Kit count | Boss KPM observations | Producing observations |
|---|---|---|---|
| `str_physical` | 4 | 0 observations | 0/4 kits |
| `dex_physical` | 4 | 0 observations | 0/4 kits |
| `int_magical` | 5 | 3 observations: 73.171, 82.192, 82.192 | 2-3/5 kits (see below) |
| `wis_faith` | 5 | 7 observations: 63.83-98.361 | 3-5/5 kits |

**INT-magical critical finding:** With 3 observations from 5 kits, and artillery_mage being the only kit confirmed to produce meaningful boss KPM in prior smoke telemetry (Gate-4 § 1.1: artillery_mage was the sole INT/WIS kit with `season_emit=True` in the 7th-case smoke), the INT band midpoint (82.192) is **artillery_mage-outlier-driven**. The other 4 INT kits (standard_wizard, pyromantic_caster, red_mage, arcane_familiar) are strong candidates to be among the T1 REJECT population at boss encounters.

**Implication of the deeper framing:**
- 8/16 band cells are FALLBACK by explicit declaration (STR/DEX × 4 cohorts each)
- INT/WIS band calibration may be outlier-driven — 13/16 cells are FALLBACK or single-outlier-derived, per KR Discipline #42 audit
- The Track 1 infrastructure (per-archetype lookup, 16-cell table) is correct and operational, but 13+ of 16 band cells cannot produce season_emit improvement because underlying kits produce boss KPM≈0

**Are the two framings consistent?** YES. The surface framing is a correct partial observation. The deeper framing is its structural extension. Together: the boss HP vs. kit damage output gap is population-wide, not archetype-specific. SC-6b physical damage insufficiency AND SC-7 `BASE_SPELL_DAMAGE_L50` insufficiency for non-artillery kits AND the endgame boss HP anchor design are ALL co-implicated. The deeper framing materially extends scope beyond per-archetype calibration.

### § 2.3 Discipline #42 Q3 Decision

**Q3: Does the deeper framing require refusing this task (returning to KR for re-scoping)?**

NO. This disposition covers both framings. The deeper framing informs which options are architecturally sound vs. papering over the structural truth. Proceeding with both framings load-bearing in the options analysis.

---

## § 3 — Root-Cause Depth Analysis (Discipline #11)

### § 3.1 Substrate Constants Co-Implicated

Four constants interact at the boss-encounter KPM gate:

**Constant 1: `base_physical_damage_l50` (SC-6b)**
- Origin: SC-6b backfill, commit `3c95883`, rocket tag `rocket/v1.5-wave-0-5-track-d-content-emission` (Cycle 14 Wave 0.5)
- Formula: `family_baseline × amplitude_mean` (martial-heavy=177, martial-light=99, ranged=91)
- Calibration history: designed as a substrate-side absolute HP anchor per doc 47 § 4.2 decision (decisions-log 2026-05-27 § SC-6b entry). Explicitly NOT calibrated against boss KPM targets — the decision record states "substrate carries the magnitude; gamora calibrates final numerics via simulation per Block C Scaffold 1 § 1.4." That calibration never fired.
- Boss HP implication: CLASS_HP_REFERENCE = 20,000; boss HP factor range (9.0-14.0)× = 180,000-280,000 HP. At martial-heavy=177 base_physical_damage_l50 with L50 attribute scaling (~1 + 50×0.005 = 1.25 → ~221 effective), a STR kit attacking a 230,000 HP boss at ~120s fight duration would need sustained DPS of ~1,917 HP/s to achieve the minimum KPM floor. The boss fight at calibrated modifiers requires far higher throughput than SC-6b substrate values provide. **This is the first constant that introduced the boss-KPM gap** — when SC-6b was designed as `family_baseline × amplitude_mean` without a boss-KPM calibration target, the physical path inherited a value that produces KPM≈0 at endgame boss HP tiers.

**Constant 2: `BASE_SPELL_DAMAGE_L50` (SC-7)**
- Origin: SC-7 calibration, commit `e7af7db` (LOCKED)
- Values: T1=28144, T2=42216, T3=60978, T4=112575 (mult=93.81× convergence)
- Calibration history: calibrated for ONE reference archetype (INT/WIS magical reference class). Math note § 3 Q-SC7-2 explicitly deferred per-kit calibration. The calibration was correct for its stated scope.
- Boss HP implication: SC-7 produced 2-3/18 in-band at best (Gate-3 empirical ceiling). Even at the calibrated mult=93.81×, most INT/WIS kits produce T1 REJECT at boss encounters. Only `artillery_mage` (and to a lesser extent `holy_knight` and `ritual_mage` in the 7th-case smoke) produce meaningful boss KPM. SC-7 calibrated a value sufficient for ~1 reference archetype; non-artillery INT/WIS kits have different spell configurations, rotation densities, and skill base_damage values that produce KPM below the T1 threshold at boss HP tiers.
- **SC-7 is the second co-implicated constant**: it was calibrated against the right KPM target (boss encounter) for one kit; the same value does not produce in-band KPM across the INT/WIS population.

**Constant 3: Boss HP Scaling (`ENDGAME_TIER_HP_FACTOR_RANGE` + `BOSS_HP_DIFFICULTY_MULTIPLIER`)**
- Origin: Two independent HP scaling systems:
  - `endgame_mob_stat_profile.py` commit `ee15c96` (rocket SC-6 WU-R2, Cycle 13): `ENDGAME_TIER_HP_FACTOR_RANGE["boss"] = (9.0, 14.0)` on `CLASS_HP_REFERENCE = 20,000` → boss HP 180,000-280,000. Comment in source: "ANCHOR INTENTS, not locked simulation targets. Gamora calibrates final numerics via simulation per Block C Scaffold 1 § 1.4."
  - `BOSS_HP_DIFFICULTY_MULTIPLIER = 0.40` in `balance_loop.py` (revised 0.80 → 0.50 → 0.40 via R1 Blocker 3 disposition `5d6b3e8`). This multiplier applies to the balance loop convergence path, NOT to the gauntlet_sim path.
- Critical distinction: **The gauntlet sim uses endgame mob HP profiles directly from `endgame_encounter_catalog.py`, which references `endgame_mob_stat_profile.py`**. The `BOSS_HP_DIFFICULTY_MULTIPLIER = 0.40` from `balance_loop.py` applies to the Phase 3 balance loop, not to the Phase 7 gauntlet. These are two independent calibration contexts.
- The endgame_mob_stat_profile HP factor range (9.0-14.0)× CLASS_HP_REFERENCE = 180k-280k effective HP is the anchor used by the gauntlet. The comment "gamora calibrates final numerics" refers to calibration that was deferred to the Phase 7 gate — which is exactly where the failure is now surfacing.
- **Boss HP is the third co-implicated constant**: the endgame encounter HP anchors were set as "ANCHOR INTENTS" at Cycle 13 SC-6 with an explicit forward-link to gamora Phase 7 calibration. That calibration is the 8th-case resolution. The HP values themselves are not a calibration error — they are an unclosed scaffold.

**Constant 4: `TIER_1_REJECT_THRESHOLD = 0.30`**
- Origin: `t4_sim_cycling.py`, present in the codebase before Cycle 14 (inherited from B14.5 architecture)
- Function: kits with kpm_delta > 0.30 are T1-REJECTed; T2 full-sim does not run
- Boss-KPM gap question: at boss KPM=0 (zero kills), kpm_delta is undefined or infinite — these kits T1-REJECT trivially regardless of threshold value. A T1 REJECT threshold of 0.30 vs 0.45 or 0.60 would not change the outcome for kits producing zero boss kills.
- **Finding: T1 REJECT threshold is NOT a primary co-implicated constant.** The threshold is appropriate for the intended regime (kits producing non-zero KPM near the band). The problem is upstream: kits produce zero boss KPM, so the threshold is never exercised as a discriminator. Widening the T1 threshold would not admit any STR/DEX or non-artillery INT/WIS kits.

### § 3.2 Which Constant First Introduced the Gap

**Git blame lineage:**

1. `ee15c96` (Cycle 13 SC-6, 2026-05-27): `endgame_mob_stat_profile.py` established boss HP factor range (9.0-14.0)× with explicit comment "ANCHOR INTENTS, not locked simulation targets." This commit established the boss HP pool WITHOUT calibrating against any kit damage output. The "gamora calibrates final numerics" note was a deferred scaffold.

2. `3c95883` (Cycle 14 Wave 0.5, SC-6b): `base_physical_damage_l50` substrate backfill with `family_baseline × amplitude_mean` (martial-heavy=177). This commit set physical damage baselines WITHOUT running against the boss HP pool established in `ee15c96`. The decisions-log SC-6b entry acknowledges gamora calibration is expected; it did not fire.

3. `e7af7db` (Cycle 14, SC-7): `BASE_SPELL_DAMAGE_L50` calibrated at mult=93.81× for INT/WIS reference class. This calibration DID run against endgame boss encounters (math note § 12 records convergence against boss HP). It was sufficient for the reference archetype. Per-kit variation in spell density and rotation was not within SC-7 scope.

**First-introduction finding:** `ee15c96` (boss HP anchor design without per-kit damage calibration) and `3c95883` (physical damage without boss-KPM target) are the co-originating commits. Both carried explicit "calibration deferred" annotations. Neither is an engineering error — both are correctly documented scaffolds that have now arrived at their calibration gate. SC-7 (`e7af7db`) is the third constant, but it is the one that actually ran against the boss HP target (for one reference archetype). The 8th case is the surface of all three deferred calibrations meeting simultaneously at the Phase 7 gate.

### § 3.3 Discipline #39 Assessment

Discipline #39 (no-synthetic-stub-as-permanent-fallback) applies in a generalised form here:
- `base_physical_damage_l50` (SC-6b): substrate-derived placeholder not calibrated against endgame boss HP — a scaffold with pending calibration
- SC-7 single-reference-class calibration: calibrated for one kit, applied to 18 — a scaffold with pending per-kit extension
- Boss HP anchor design: "ANCHOR INTENTS" flag in source — an explicit scaffold
- STR/DEX FALLBACK bands in canonical doc § 3.9: FALLBACK notation explicitly acknowledges the calibration is not yet possible — Discipline #39 compliance requires this be RESOLVED, not accepted as permanent state

### § 3.4 Discipline #18 Compliance Question (Dispatch § 1.6)

**Question:** Does Track 1 telemetry NOW constitute the baseline that should fire Track 2 methodology consultation? Or is Track 1's failure-mode itself architectural (boss HP) rather than calibration (per-kit damage)?

**Finding: BOTH are true, and this distinction is load-bearing for option selection.**

Track 1 telemetry IS the baseline that should inform Track 2 methodology — Discipline #18 refinement § 18.2 is satisfied (baseline empirical signal has landed). The Track 2 methodology consultation can now fire with evidence: per-archetype variance data exists for INT/WIS; zero-signal data exists for STR/DEX.

However, Track 1's failure mode is NOT merely a calibration gap. It surfaces an architectural truth: the boss HP pool and kit damage outputs have never been jointly calibrated. Track 2 methodology consultation will need to address WHICH axis to fix first: (a) reduce boss HP to current kit output, (b) increase kit damage to current boss HP, or (c) replace the metric (Option C damage/HP%). This is not resolvable by calibration loop alone without a Matt architectural decision about which direction the calibration should flow.

**Implication for Discipline #18:** Track 2 methodology consultation should fire NOW (with Track 1 telemetry in hand), BUT the consultation must explicitly include the boss-HP-vs-kit-damage directional question as its opening design call. This is a new architectural decision that the dispatch § 1.6 question was pointing toward.

---

## § 4 — Six Options Ranked

### Option 1 — Boss HP Rebase to Current Kit-Damage Population (Cycle 14 immediate)

**Design:** Reduce endgame boss HP targets in `endgame_mob_stat_profile.py` to align with the empirical kit damage output distribution. The boss HP factor range (9.0-14.0)× CLASS_HP_REFERENCE is the "ANCHOR INTENTS" scaffold from `ee15c96`. Rebase to match what Track 1 INT/WIS kits actually produce at KPM=75-82 (the empirically observed median). Work backwards from the KPM target: at KPM=75 with Balanced cohort, desired boss HP = DPS × (1/KPM) × 60. Requires gamora empirical measurement to determine the current population-median DPS, then set boss HP factor range to produce KPM in the target band.

**What it resolves:**
- All 16 band cells: if boss HP is reduced to match population-median DPS, all archetype-median boss KPM rises to band range
- STR/DEX and INT/WIS kits both benefit from HP rebase
- Closes the endgame_mob_stat_profile scaffold ("ANCHOR INTENTS" → calibrated)
- D9 close criterion (≥12/18 × 3 seasons emit) potentially achievable in Wave 5 if rebase is correct

**What it does NOT resolve:**
- Per-kit variance: kits with below-median DPS still T1 REJECT if band is set at population median
- SC-6b physical damage values remain uncalibrated against any explicit target (they simply become "calibrated by boss HP rebase" rather than "calibrated by damage increase")
- Does not distinguish between archetype damage profiles — boss HP is a single value; per-kit variance remains
- Track 2 per-kit calibration still needed for full 16-cell empirical grounding

**Discipline compliance:**
- Discipline #11: PASS — empirical measurement of population DPS required before rebase; substrate-emergent
- Discipline #39/40: PARTIAL — closes the endgame_mob_stat_profile scaffold; does NOT close the SC-6b or SC-7 per-kit scaffolds
- Discipline #42: PASS — this option addresses both framings (population-wide, not archetype-specific)
- Discipline #13a-partition: WARN — boss HP is a single substrate value applied uniformly; per-archetype boss HP variance (STR boss vs INT boss) is not addressed

**Effort:** ~0.5-0.75d gamora (empirical DPS measurement sweep + rebase + smoke) + 0.25d jack-ryan canonical (endgame_mob_stat_profile retraction record per Discipline #40 case (c))
**Cycle 14 close trajectory:** PRESERVES — achievable in Wave 5 if sweep is fast. D9 close (≥12/18 × 3 seasons) achievable post-rebase.
**D7 escalation:** NOT required if rebase is a calibration decision (Matt Pattern-B for the option choice; gamora executes post-ratification)

**Recommendation rank: 1 (Cycle 14 primary path)**

---

### Option 2 — Staged: Boss HP Rebase for Cycle 14 Emit + Per-Kit Full Calibration Cycle 15

**Design:** Option 1 (boss HP rebase) for Cycle 14 Wave 5 emit signal; Cycle 15 sees full per-kit calibration sweep across all 18 kits × 4 cohorts, producing per-kit `base_physical_damage_l50` revision (SC-6b) AND per-kit `BASE_SPELL_DAMAGE_L50` variants (SC-7 extension) or option C metric replacement. This is the same two-track staged architecture that Option F (Gate-4) used: fix the solvable layer now; design the principled long-term architecture next cycle.

**What it resolves (Phase 1 / Cycle 14):** same as Option 1 above — boss HP rebase produces broad season_emit signal; D9 close criterion achievable.

**What it resolves (Phase 2 / Cycle 15):**
- Full per-kit calibration loop (18 kits × 4 cohorts; replaces per-archetype band with per-kit band per Track 2)
- SC-6b physical damage values recalibrated against the boss HP target (either boss HP post-rebase or original HP — whichever becomes the canonical target)
- SC-7 extension to per-kit calibration OR Option C damage/HP% metric
- Composes with D2 (per-encounter-type bands) as 2D band architecture at Cycle 15

**Discipline compliance:**
- All of Option 1's compliance, plus:
- Discipline #18: PASS — Cycle 15 Track 2 methodology consultation fires with Track 1 baseline in hand (now available); both HP-rebase telemetry and Track 1 telemetry inform Track 2 design
- Discipline #40: CLEAN — scaffolds are staged for retirement on explicit schedule (Cycle 14 boss HP scaffold retired; Cycle 15 per-kit calibration scaffold retired)

**Effort:** Option 1 effort for Cycle 14 + ~2-3d gamora for Cycle 15 per-kit calibration
**Cycle 14 close trajectory:** PRESERVES — same as Option 1
**D7 escalation:** NOT required for Cycle 14 Phase 1; Cycle 15 dispatch required for Phase 2

**Recommendation rank: 2 (preferred if Matt wants explicit Cycle 15 commitment on the record)**

---

### Option 3 — Per-Kit Damage Calibration (SC-6b AND SC-7 both per-kit, Cycle 14)

**Design:** Full per-kit calibration sweep across all 18 kits × 4 cohorts NOW. Produces per-kit `base_physical_damage_l50` target values for STR/DEX kits AND per-kit `BASE_SPELL_DAMAGE_L50` variants for INT/WIS kits. 72-value calibration table (18 kits × 4 cohorts) replaces the 16-value per-archetype table. Does NOT change boss HP.

**What it resolves:**
- All 18 kits calibrated against actual boss HP pool
- Intra-archetype variance addressed (no outlier-driven band)
- Full closure of SC-6b and SC-7 per-kit scaffolds
- Principled: damage values calibrated to the SAME boss HP pool, both physical and magical paths

**What it does NOT resolve:**
- Boss HP anchor design remains unclosed ("ANCHOR INTENTS" source comment)
- Per-encounter-type variance (D2 Cycle 15) still unaddressed
- Cycle 14 close trajectory: AT RISK — 2-3d gamora effort in Wave 5 may overrun

**Discipline compliance:**
- Discipline #11: PASS — empirical per-kit calibration loops are the gold standard
- Discipline #18: REQUIRES methodology consultation (D3 deferred; methodology for per-kit calibration vs. damage/HP% metric is the Track 2 design call)
- Discipline #40: CLEAN — retires all per-kit scaffolds in one pass
- Discipline #42: PASS — resolves deeper framing

**Effort:** ~2-3d gamora (18-kit calibration sweep) + ~0.5d jack-ryan canonical
**Cycle 14 close trajectory:** AT RISK — this is Cycle 14 if gamora execution is fast; Cycle 15 if methodology consultation (Discipline #18) is required first
**D7 escalation:** YES if Cycle 14 close is blocked by this option's size

**Recommendation rank: 4 (correct architecture; wrong timing unless Matt accepts Cycle 14 slip)**

---

### Option 4 — T1 REJECT Threshold Widen (0.30 → 0.45+)

**Design:** Widen `TIER_1_REJECT_THRESHOLD` in `t4_sim_cycling.py` to admit more kits to T2 full-sim evaluation by relaxing the T1 screen.

**Critical finding from root-cause analysis: THIS OPTION DOES NOT ADDRESS THE ROOT CAUSE.**

T1 REJECT fires when `kpm_delta > 0.30`. At boss KPM=0 (zero kills), `kpm_delta` is undefined / infinite — the kit T1-REJECTs trivially. Widening the threshold to 0.45 does not change the outcome for kits that kill zero bosses. A kit must produce at least one boss kill for T1 REJECT threshold to matter as a discriminator.

**Discipline compliance:**
- Discipline #11: FAIL — option is not empirically grounded; the telemetry shows the problem is upstream of T1 REJECT
- Discipline #42: FAIL — option addresses neither framing
- Discipline #40: FAIL — adds a new scaffold without retiring the underlying one
- Matt D2 precedent: "scaffolds get RESOLVED, not deliberately introduced"

**Effort:** ~0.1d gamora + 0.1d jack-ryan
**Cycle 14 close trajectory:** DOES NOT UNBLOCK — kits producing KPM=0 still T1 REJECT regardless of threshold value

**Recommendation rank: 6 (DO NOT PURSUE — empirically incoherent)**

---

### Option 5 — Cycle 14 Close-Criterion Amendment (Accept 3/18 Emit as Close)

**Design:** Amend the D9 close criterion (≥12/18 × 3 seasons emit) to accept Track 1 infrastructure delivery (16-cell band table operational; telemetry filed; canonical doc populated) as Cycle 14 v1 close, with the emit signal deferred to Cycle 15.

**What it resolves:** Allows v1 tag (`v1-cycle-14-no-classes-substrate-led`) to land; unblocks D13 P1-P9 parallel framework; closes Cycle 14 v1 administratively.

**What it does NOT resolve:**
- 8th scaffold-drift case remains open (scaffolds not retired)
- Discipline #39/40: both violated — scaffold values persist without retirement timeline
- Boss HP vs kit damage gap is not narrowed
- If D13 P1-P9 parallel seasons fire under the current 3/18 emit regime, produced seasons will not pass the Phase 7 gate — the parallel framework produces content the gate rejects

**Critical structural risk:** D13 fires P1-P9 parallel season production. If the gauntlet gate accepts only 3/18 kits, those parallel seasons produce near-empty kit archives. The downstream Phase 4 archive architecture (Discipline #46 per-cell bounding) and the Cycle 14 season quality story both depend on season_emit being substantially non-zero. Closing with 3/18 emit and then firing D13 produces structurally poor content at scale.

**Discipline compliance:**
- Discipline #39: FAIL — scaffolds persist indefinitely
- Discipline #40: FAIL — no retirement timeline
- Discipline #43 (design-quality audit): the wave-close audit would flag this as A5 architectural scaffold accumulation

**Effort:** ~0.1d KR (dispatch amendment) + jack-ryan decisions-log entry
**Cycle 14 close trajectory:** ARTIFICIALLY CLOSES — creates downstream quality debt

**Recommendation rank: 5 (AVOID unless Matt decides Cycle 14 v1 close has strategic value that outweighs the quality risk; requires explicit Matt authority)**

---

### Option 6 — Option C Damage/HP% Metric Replacement (Cycle 15 — already D3-deferred)

**Design:** Replace KPM entirely with `damage_fraction_per_fight = total_damage_dealt / encounter_total_HP`. This is class-agnostic: physical and magical kit DPS is normalized against the same encounter HP denominator. As described in Gate-4 disposition § 3, Option C (doc 47 § 3 variant).

**Status per D3 deferral:** This option was already scoped to Cycle 15 by Matt D3 ratification at Gate-4. It is included here for completeness and to verify the 8th case does not change the Cycle 15 routing.

**Deeper-framing update:** Option C becomes MORE attractive in light of the 8th case. The core problem is that physical damage (Path A, substrate-bound) and magical damage (Path B, engine-calibrated via SC-7) have independent calibration histories producing incomparable KPM at boss encounters. A damage/HP% metric normalizes across both paths using the encounter HP denominator — the metric is path-agnostic by construction. Track 1 telemetry now provides the concrete evidence of the independent-calibration problem, which Option C was designed to address architecturally.

**What changes with the 8th case:** Option C is not a Cycle 14 path (Discipline #18 methodology consultation required first; legolas Mode A), but it is now the most architecturally motivated Cycle 15 target. The 8th case's deeper framing (population-wide boss HP gap across BOTH damage paths) is precisely the failure mode Option C was designed to resolve.

**Discipline compliance:**
- Discipline #18: REQUIRES methodology lock before execution (legolas Mode A consultation)
- Discipline #11: PASS if consultation produces empirically grounded metric definition
- Discipline #40: CLEAN long-term — retires KPM, SC-6b-uncalibrated, SC-7 per-kit scaffolds in one architectural move

**Effort:** ~0.5d legolas Mode A + ~0.75d jack-ryan canonical + ~1.5d gamora = ~2.75d total
**Cycle 14 close trajectory:** CANNOT CLOSE Cycle 14 — D3-deferred to Cycle 15 per Matt

**Recommendation rank: 3 (for Cycle 15 architectural target, above per-kit calibration because it resolves the two-path divergence by design)**

---

## § 5 — Recommendation

**RECOMMEND: Option 1 (Boss HP Rebase) for Cycle 14 immediate emit, followed by Option 6 (Option C damage/HP%) at Cycle 15 as the principled long-term close.**

**The Cycle 14 rationale:**

Boss HP rebase is the correct lever for Cycle 14 because:

1. **It closes the "ANCHOR INTENTS" scaffold in `endgame_mob_stat_profile.py`** — the explicit source-code annotation at `ee15c96` deferred gamora calibration of boss HP to exactly this gate. The rebase is the calibration the scaffold was waiting for, not a workaround.

2. **It is the only option that resolves the deeper framing without adding per-kit complexity.** If boss HP is rebased to the current population-median DPS output, both STR/DEX kits (which have internally consistent DPS profiles at their SC-6b substrate values) AND INT/WIS kits (calibrated via SC-7 per-archetype values) will produce non-zero boss KPM. The per-archetype Track 1 infrastructure (operational at `f704599`) will produce meaningful band measurements after rebase.

3. **It does not invalidate Track 1 infrastructure.** After boss HP rebase, the 16-cell band table needs re-calibration (re-run Track 1 sweep against rebased boss HP), but the lookup architecture, gauntlet integration, and Discipline #45 vocabulary audit are all preserved. The rebase is a substrate input change; the gate infrastructure is correct.

4. **SC-6b `base_physical_damage_l50` calibration is preserved.** By rebasing boss HP to match kit output (rather than scaling kit output to match boss HP), SC-6b substrate values do not need to be modified in Cycle 14. This avoids a cross-seam rocket involvement at this stage.

5. **Matt D2 precedent is honored.** "Scaffolds get RESOLVED, not deliberately introduced." The HP rebase retires the endgame_mob_stat_profile scaffold via direct empirical calibration — not a workaround.

**If Matt prefers Option 2 (staged rebase + Cycle 15 full per-kit):** this is the defensible alternative that makes the Cycle 15 commitment explicit on record. Option 2 composes cleanly with Option 6 (Option C at Cycle 15): boss HP rebase for emit signal; Option C methodology lock + implementation at Cycle 15 replaces both the per-kit calibration loop AND the KPM metric in one architectural move.

**The Cycle 15 rationale for Option 6 over Option 3:**

Option 3 (per-kit KPM calibration) is the right architecture if KPM is the long-term metric. But Track 1 has now empirically confirmed the deeper framing: the problem is a two-path independent calibration that produces structurally incomparable KPM values. Option C (damage/HP%) is the architectural response that removes the two-path calibration dependency by normalizing to the encounter HP denominator. Pursuing per-kit KPM calibration at Cycle 15 would require 72 band values and would still inherit the two-path variance problem. Option C resolves both the calibration debt AND the metric architecture in one move.

---

## § 6 — Cycle 14 v1 Close-Criterion Impact Per Option

### D9 Close Criteria (≥12/18 × 3 seasons emit; Gate-2 PASS; A/B filed; #41-#46 batched; v1 tag)

| Option | D9 close (≥12/18 × 3 seasons) | Gate-2 PASS path | v1 tag timing |
|---|---|---|---|
| 1 Boss HP rebase | UNBLOCKS — rebase produces broad emit signal; ≥12/18 achievable post-rebase | Wave 5 post-rebase | Wave 5 if rebase lands ≤0.75d |
| 2 Staged rebase + Cycle 15 | UNBLOCKS (same as Option 1) | Same as Option 1 | Same as Option 1 |
| 3 Full per-kit calibration | AT RISK — 2-3d gamora effort; depends on Cycle 14 timeline remaining | Wave 5 if gamora is fast | Cycle 15 risk |
| 4 T1 threshold widen | DOES NOT UNBLOCK | N/A | N/A |
| 5 Close-criterion amendment | ARTIFICIALLY CLOSES (quality debt) | Administrative | Could land immediately |
| 6 Option C (Cycle 15) | CANNOT CLOSE Cycle 14 | Cycle 15 | Cycle 15 |

### D7 Escalation (3-fail/season → Matt Pattern-B)

- Options 1, 2: D7 does NOT fire for Cycle 14 execution; Matt Pattern-B call is THIS gate (D2 re-evaluation hook). After Matt ratifies option, gamora executes per-dispatch; no further D7 needed.
- Option 3: D7 may fire if calibration sweep encounters unexpected failures at per-kit level.
- Options 4, 5, 6: irrelevant for D7 in Cycle 14.

### D13 P1-P9 Parallel Framework

- Options 1, 2: PRESERVES D13 — once emit unblocked, P1-P9 parallel season production can fire with ≥12/18 emit expected. The parallel framework's quality story depends on broad kit emission.
- Option 3: PRESERVES if execution lands before D13 fires.
- Option 5: DEGRADES D13 — parallel seasons fire under 3/18 emit → near-empty kit archives across 9 parallel seasons.
- Options 4, 6: BLOCKS or DEGRADES D13 (emit not unblocked in Cycle 14).

### Cycle 14 Close Trajectory Update

At Gate-4 ratification: estimated ~4-7 days to v1 close. With 8th case:
- Option 1: adds ~0.75d (boss HP rebase + re-run Track 1 sweep smoke) → revised estimate 5-8 days
- Option 2: same as Option 1 for Cycle 14 component; adds Cycle 15 dispatch authoring (~0.25d)
- Option 3: adds 2-3d gamora + methodology consultation → 7-10 days; Cycle 14 slip risk
- Option 5: adds ~0 days; closes immediately; quality risk unacceptable per discipline audit

---

## § 7 — Open Questions for Matt Pattern-B Ratification

### Decision 1 — Ratify Option 1 (Boss HP Rebase) for Cycle 14 Wave 5?

Close the `endgame_mob_stat_profile.py` "ANCHOR INTENTS" scaffold via empirical calibration. Gamora runs: (1) population-DPS measurement sweep across all 18 kits at Balanced cohort; (2) boss HP factor range recalibration to produce KPM≈75 at population median; (3) re-run Track 1 sweep to populate the 16-cell band table with rebased HP values; (4) smoke acceptance ≥12/18 emit. Estimated ~0.5-0.75d gamora + 0.25d jack-ryan canonical (Discipline #40 case (c) retraction record for endgame_mob_stat_profile).

**If yes:** gamora fires boss HP rebase dispatch; Track 1 sweep re-run is sub-step of rebase; 16-cell band table re-populated with empirical values; FALLBACK notation retired for all cells that achieve signal; canonical doc § 3.9 updated per Discipline #40 case (c).

**If no (prefer Option 2 or 3):** see Decision 2/3 below.

### Decision 2 — If D1 is Yes: Commit Option 6 (Damage/HP% Metric) as Cycle 15 Architectural Target?

With Track 1 telemetry confirming the two-path independent calibration problem population-wide, Option C (damage/HP% metric) is the architecturally motivated Cycle 15 close. This decision establishes the Cycle 15 roadmap: legolas Mode A methodology consultation → jack-ryan canonical metric definition → gamora implementation → replace KPM gate with damage/HP% gate. Retires both the endgame_mob_stat_profile HP calibration AND the KPM architecture in one Cycle 15 move.

**Alternative (if Option 3 preferred):** Full per-kit KPM calibration at Cycle 15 (18 kits × 4 cohorts = 72 band values). Preserves KPM architecture; adds per-kit calibration depth. Composes with D2 (per-encounter-type) as 2D band at 18 × 5 × 4 = 360 values long-term. Higher calibration maintenance burden than Option C but less methodology-lock overhead.

### Decision 3 — Scope and Timing of Cycle 15 Track 2 Dispatch Authoring

Matt D3 ratification deferred Track 2 methodology consultation to Cycle 15. With Track 1 telemetry now in hand (per Discipline #18 refinement § 18.2), the Track 2 dispatch can be authored at Cycle 14 v1 close (before Cycle 15 begins). Does Matt want KR to author the Track 2 Cycle 15 dispatch immediately after v1 tag, or does the methodology consultation wait until Cycle 15 opens?

### Decision 4 — Handling of the Deeper Framing (13/16 FALLBACK or Single-Outlier Cells)

The KR Discipline #42 audit surfaced that 13/16 band cells in the current canonical doc § 3.9 are either FALLBACK (STR/DEX, 8 cells) or potentially single-outlier-driven (INT/WIS non-modal archetype cells). If Option 1 (boss HP rebase) is ratified, the Track 1 sweep re-run post-rebase should produce meaningful empirical observations across all 16 cells (provided the rebase correctly targets population-median DPS). The 13/16 concern resolves if the rebase is correct. However: if the rebase is incorrect or produces uneven results across archetypes, some FALLBACK cells may persist.

**Matt decision needed:** should the re-run Track 1 sweep target ≥2 observations per cell (minimum empirical grounding per Discipline #18) as an explicit acceptance criterion, or is the current ≥12/18 season_emit criterion sufficient? This operationalizes whether "per-cell empirical grounding" is a Cycle 14 close requirement or a Cycle 15 refinement.

---

## § 8 — Framing-Audit Summary (Discipline #42)

| Q | Question | Answer |
|---|---|---|
| Q1 | Load-bearing framing assumptions | Surface framing (STR/DEX uncalibrated physical damage) + Deeper framing (population-wide boss HP gap across BOTH damage paths) — BOTH load-bearing per KR Discipline #42 audit |
| Q2 | Refutation evidence sought | Track 1 telemetry (boss_kpm_observations = [] for STR/DEX; only 3 observations for INT; 13/16 cells FALLBACK or outlier-driven) — refutation evidence confirms deeper framing |
| Q3 | Do I refuse (Q3=YES)? | NO — both framings addressable; options analysis covers both |

**Framing-audit conclusion:** The surface framing UNDERSTATES the structural depth. The deeper framing is the architecturally correct characterization. Options 1 and 2 address the deeper framing (population-wide HP gap). Options 3 and 6 also address it. Options 4 and 5 address neither framing.

---

## What I Found

Track 1 infrastructure (`f704599`) is architecturally correct — the 16-cell per-archetype band table, gauntlet integration, Discipline #45 vocabulary audit, and MIGRATION.md § v1.38 are all sound. Track 1 cannot produce season_emit improvement because 13+ of 16 band cells have no empirical boss KPM signal (zero observations for STR/DEX; potentially outlier-driven for INT/WIS non-artillery kits). The root cause is that endgame boss HP targets (`endgame_mob_stat_profile.py`, commit `ee15c96`) were designed as "ANCHOR INTENTS" with explicit gamora calibration deferred to the Phase 7 gate — and that calibration has now arrived. Physical kit damage (`base_physical_damage_l50`, SC-6b commit `3c95883`) was set as a substrate formula not calibrated against boss HP. SC-7 (`BASE_SPELL_DAMAGE_L50`, commit `e7af7db`) was calibrated against boss HP for one reference archetype only. All three are correctly documented scaffolds; none is an engineering error. The 8th case is their joint arrival at the Phase 7 gate. The T1 REJECT threshold (0.30) is NOT co-implicated — it is never exercised as a discriminator for kits producing zero boss kills.

## Rationale

- **Discipline #39 / #40** (scaffold-as-drift): Three scaffolds converge at this gate (boss HP anchor, SC-6b physical damage, SC-7 per-kit). Each was correctly flagged at authoring time. Resolution by calibration is the obligation these scaffolds created. Boss HP rebase is the most parsimonious single calibration that closes the "ANCHOR INTENTS" scaffold and produces population-wide signal without cross-seam changes.
- **Discipline #42 / #44** (framing-audit / framing-refusal): Gamora's Discipline #44 invocation is correct and load-bearing. The deeper framing materially extends scope per the D2 re-evaluation hook trigger. Both framings must be resolved in the options package.
- **Discipline #18 refinement** (methodology consultation fires after baseline lands): Track 1 IS the baseline; the Track 2 methodology call can now fire. The boss-HP-vs-kit-damage directional decision is the opening question for Track 2.
- **ADR-002** (tiered approval): The boss HP rebase modifies `endgame_mob_stat_profile.py` (generation seam, owned by rocket per `ee15c96`). This is a cross-seam impact — the rebase touches rocket's substrate constants. Matt Pattern-B authorization is required before gamora fires a rebase that touches rocket's authored HP profile values.

## Action

- [ ] **Matt:** Decision 1 — ratify Option 1 (Boss HP Rebase) for Cycle 14 Wave 5; or choose Option 2 (staged) or Option 3 (full per-kit calibration)
- [ ] **Matt:** Decision 2 — commit Option C (damage/HP% metric) as Cycle 15 architectural target; or choose full per-kit KPM calibration (Option 3) as Cycle 15 alternative
- [ ] **Matt:** Decision 3 — timing of Track 2 Cycle 15 dispatch authoring (at v1 close or at Cycle 15 open)
- [ ] **Matt:** Decision 4 — per-cell empirical grounding criterion for Track 1 re-run (≥2 observations/cell as acceptance criteria, or ≥12/18 season_emit sufficient)
- [ ] **gamora (post-D1 ratification):** fire boss HP rebase dispatch; re-run Track 1 sweep; populate 16-cell band table empirically; smoke acceptance ≥12/18 emit
- [ ] **jack-ryan (post-D1 ratification):** Discipline #40 case (c) retraction record for `endgame_mob_stat_profile.py`; canonical doc § 3.9 update (FALLBACK cells retired per re-run results); decisions-log 8th scaffold-drift case entry
- [ ] **KR:** route Gate-5 disposition to Matt for D1-D4 ratification; author boss HP rebase dispatch post-ratification; author Track 2 Cycle 15 forward-dispatch per Decision 3 timing

## References

- `agentic_orchestration/dispatches/2026-05-28-jack-ryan-gate-5-8th-scaffold-drift-disposition.md` — dispatch authority
- `agentic_orchestration/cycle-14-wave-5-season-001/option-f-track-1-calibration-telemetry.json` — primary empirical evidence (boss_kpm_observations = [] for STR/DEX; 3 INT observations; 7 WIS observations)
- `reincarnated-engine/src/reincarnated/simulation/math/option-f-track-1-per-damage-path-kpm-bands-2026-05-28.md` — Track 1 math note
- `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` § v1.38 — gate semantic change + Discipline #44 invocation record
- `reincarnated-engine/design/math/phase-7-2-layer-joint-gate-thresholds-2026-05-27.md` § 3.9 + § 3.10 — canonical band table (FALLBACK notation) + Track 2 forward-link
- `reincarnated-engine/src/reincarnated/generation/endgame_mob_stat_profile.py` — boss HP anchor (ENDGAME_TIER_HP_FACTOR_RANGE; "ANCHOR INTENTS" scaffold; commit `ee15c96`)
- `reincarnated-engine/src/reincarnated/simulation/balance_loop.py` — `BOSS_HP_DIFFICULTY_MULTIPLIER = 0.40` (balance loop path, NOT gauntlet path — these are independent)
- `reincarnated-engine/design/decisions/decisions-log.md` § SC-6b — SC-6b decision record (base_physical_damage_l50; commit `3c95883`)
- `agentic_orchestration/qa/pending/2026-05-28-7th-scaffold-drift-cross-class-dps-gate-4-disposition.md` — Gate-4 template and precedent
- `agentic_orchestration/qa/pending/2026-05-28-sc7-f1-gate-3-disposition.md` — Gate-3 template and precedent
- `agentic_orchestration/cycle-14-hive-mind-state.md` § "8TH SCAFFOLD-DRIFT CASE LANDED 2026-05-28" — KR Discipline #42 framing-audit record
- `reincarnated-collaboration/canonical/47-damage-scaling-architecture-2026-05-27.md` § 3 — 4 damage-scaling paths canonical
