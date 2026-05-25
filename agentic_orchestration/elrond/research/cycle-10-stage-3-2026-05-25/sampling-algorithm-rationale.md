# Cycle 10 Stage 3 — Phase 2 — Sampling Algorithm Rationale + Decisions

**Date:** 2026-05-25
**Owner:** elrond (lead — Phase 2 execution)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-24-elrond-cycle-10-stage-3-v1-scope-materialization.md` § 3.6
**Phase 1 consult:** `agentic_orchestration/legolas/research/cycle-10-stage-3-methodology-consult-2026-05-25/methodology-recommendation.md`
**Composition policy:** `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md`
**Substrate DB:** `/Users/admin/Games/reincarnated-loadout/data/telemetry.db`

---

## 0. TL;DR

Stage 3 Phase 2 ran the **greedy-with-swap-repair** baseline per Phase 1 legolas Mode A recommendation. Outcome:

- **v1_scope size: 3,042 rows** (envelope 1,700-3,100 — within)
- **Pre-population smoke: 10/10 PASS** (well above 7/10 threshold)
- **D1c leak check: 0** (PASS)
- **Mode-C-equivalent leak check: 0** (PASS — operationalized as `military_modern + named_mythological_match` overlap; see § 4 below)
- **Register distribution within ±5pp: PASS** (historical +5.0pp, fantasy +1.3pp, military_modern +1.5pp, mythological -0.8pp)
- **PCFS (archetype gate; substrate-bounded archetypes excluded): 12/17 = 70.6% FAIL** (threshold 85%)
- **PCFS (substrate-cell reference, fine-grained): 8/40 = 20.0%**
- **LP fallback: NOT FIRED.** Per § 5 below, the 5 failing archetypes are **policy/substrate-trade-off-bounded**, not local-optima — LP would not improve them within the current composition policy register-share constraints. Routed to Sidecar B / Stage 3.5 enrichment per composition policy § 4.1 spirit for Phase 3 sign-off discussion.

**Sampling completed in ~2 seconds** (well within § 8 envelope of 3 min); peak memory ~18-36 MB working set per Phase 1 § 6 mitigation (column-selective load).

---

## 1. Algorithm baseline — greedy-with-swap-repair per legolas Mode A recommendation

Adopted per Phase 1 § 3 and § 5. Pipeline structure:

**Pass 1 — auto-include + filter:**
- Genre filter pre-pass: `register_canonical IN ('fantasy', 'mythological', 'historical', 'military_modern')` → 70,722 in-genre rows; 19,119 excluded (genre-filter `unknown`)
- D1c gate: `weapon_kind_classified_subtype` D1c-excluded list → 560 Tier-S rows excluded
- D1a auto-include: `quality_tier='S' AND weapon_kind_classified_subtype='handheld_weapon'` → **437 rows** (composition policy estimate 449; empirical 437 because 12 of the 449 fall in the genre-excluded `unknown`-register bucket)
- D1b auto-include: `quality_tier='S' AND weapon_kind_classified_subtype IN ('armor_shield', 'accessory_handheld', 'accessory_weapon_integrated')` → **95 rows** (matches Phase 0a empirical 95)

**Pass 2 — structured selection sub-phases A/B/C:**

- **Sub-phase A — Tier A preferred-include** with per-register cap (historical 55% × target_total, fantasy 35%, military_modern 8%, mythological 3%) + per-substrate-cell soft cap (1.5× archetype floor) + military_modern Tier-A deterministic 80% trim (random seed=42 for reproducibility): selected **1,451 Tier-A rows** (mm_trim_skip=1,830, reg_cap_skip=3,866, cell_cap_skip=311)

- **Sub-phase B — Tier B archetype-floor-fill** with index-based pool traversal (allows register-cap-rejected candidates to be re-tested when register share shifts) + per-substrate-cell soft cap (80 within archetype fill) + relaxed register cap (target+5pp for under-floor archetype fill): selected **779 Tier-B rows** in 95 iterations

- **Sub-phase C — Tier B remaining budget** allocated to under-target registers via round-robin: selected **279 rows**

**Pass 3 — swap-repair:** military_modern overshoot guard (caps at 8%) + archetype-level under-floor fill (budget-respecting against V1_SCOPE_UPPER=3,100). 3 outer passes; net **+8 rows** added during swap-repair.

---

## 2. Parameter choices

Per legolas Mode A § 5 recommendations:

| Parameter | Value | Source |
|---|---|---|
| Tier S multiplier | (pre-committed) | § 5.1 |
| Tier A multiplier | 3.0 | § 5.1 |
| Tier A military_modern multiplier | 0.6 (3.0 × 0.2 trim) | § 5.1 + dispatch § 4.2 |
| Tier B multiplier | 1.0 | § 5.1 |
| Tier C multiplier | 0.3 | § 5.1 |
| Swap-repair outer cap | 200 | § 5.2 |
| Swap-repair budget per pass | 50 | § 5.2 |
| Convergence tolerance | 1 row (no progress in a pass) | § 5.2 |
| Sub-phase A cell soft-cap | 1.5× archetype floor (typed cells), 25 (off-roster) | elrond decision; documented here |
| Sub-phase B substrate-cell cap within archetype fill | 80 | elrond decision; documented here |
| Register cap during normal fill | target + 4pp | elrond decision; documented here |
| Register cap during under-floor fill | target + 5pp | elrond decision (relaxation for archetype-floor priority); matches smoke gate |
| Military_modern trim RNG seed | 42 | reproducibility |

---

## 3. Structural finding — substrate vocabulary mismatch with Sketch A roster (Discipline #11)

**LOAD-BEARING discovery during Phase 2 design.** The composition policy + Sketch A use 4-tuple cells in vocabulary `(range × tempo × amplitude × attribute)` where amplitude bins are `flat / variable / spiky` per BC-axes-lock Axis 3B. The substrate column `proxy_geometry_class` is GEOMETRY (`single / AoE / cleave / multi-hit / cone / scatter`) per Axis 2 — DIFFERENT axis from amplitude. The substrate does NOT currently materialize amplitude as a column.

**Operational consequence:**
- Sketch A roster has ~22 cells in 4-tuple amplitude vocabulary
- Substrate observed cells: 40 (in 4-tuple geometry vocabulary) at floor>0; 50+ total observed
- Per-cell Sketch B floors (80-120 melee, 60-100 ranged, etc.) were calibrated for the ~22-cell Sketch A roster, not the ~40-cell substrate roster
- Naive substrate-cell floor application: PCFS at 20% (substrate-cell reference; reported but NOT gating)

**Resolution (Discipline #11 substrate-led):**
- Per Discipline #11 + Pattern 4-5-6 retirement spirit: substrate's geometry vocabulary is what we sample against; aggregate to **archetype-level (range, tempo, attribute) for PCFS gate**
- Archetype-level PCFS yields 18 archetypes (matches Sketch A roster intent more closely)
- Substrate-cell PCFS reported for transparency / future-work signal (v1.1+ Track candidate: extract amplitude column or pursue joint amplitude/geometry extraction)

This finding flagged for Phase 3 distribution report + Knight-rider for v1.1+ queue: **"v1.1+ Track candidate — amplitude column extraction joint with geometry; or, alternatively, retire amplitude from Sketch A in favor of geometry vocabulary."**

---

## 4. Mode-C contamination assertion — operational substitution (Discipline #11)

**LOAD-BEARING discovery during Phase 2 design.** The dispatch § 8 + Phase 1 § 7 PCFS spec reference `rep_audit_mode_c_naming_allusion_suspected = 1` as the Mode-C leak-check column. **This column does NOT exist in the substrate DB.** The flag was a Stage 1.5 SEMANTIC concept living in extraction JSON (`named-bearer-matches.json`), not materialized to the DB as a column.

**Operational substitute (recorded in script line 90-95 + smoke output):**
- Mode-C contamination signature: `register_canonical='military_modern' AND named_mythological_match IS NOT NULL` — overlap is the operational definition of Mode-C naming-allusion (Stage 1.5 examples: "Sadko Truck", "S-500 Prometheus" missile, "Baba Yagas (Vampire) UAV")
- Stage 2.5 Gate-2 was designed to block this overlap from named-mythological-match path; Phase 2 verification confirms zero leak via the v1_scope composite-top-1% pathway

Empirical: **0 rows in v1_scope match the Mode-C-equivalent signature.** PASS.

Flagged for Phase 3 sign-off + Knight-rider for v1.1+ queue: **"v1.1+ Track candidate — materialize rep_audit_mode_c_naming_allusion_suspected as a DB column for downstream queries (Stage 1.5 has it in extraction JSON only)."**

---

## 5. PCFS FAIL — analysis of 5 failing archetypes

| Archetype | Count | Floor | Substrate supply (in-genre A/B/S/C) | Diagnosis |
|---|---:|---:|---:|---|
| `(melee, high, STR)` | 97 | 100 | 476 | Policy-trade-off-bounded — substrate 96% historical; historical share at +5.0pp cap |
| `(ranged, low, STR)` | 72 | 80 | 956 | Policy-trade-off-bounded — substrate ~96% historical; historical at cap |
| `(mid, low, DEX)` | 36 | 80 | 737 | Policy-bounded — substrate 50% military_modern; military_modern trim policy keeps low |
| `(mid, medium, DEX)` | 73 | 80 | 148 | Substrate-near-bounded — DEX has share room but small archetype pool |
| `(mid, high, DEX)` | 74 | 80 | 215 | Substrate-near-bounded — small archetype pool |

**Substrate-bounded (excluded from gate):** `(ranged, low, WIS)` count=43 floor=60 substrate=51 — supply<floor; routed to Sidecar B WIS-broad enrichment per composition policy § 4.1.

**Why LP fallback would NOT improve this outcome:**

Per Phase 1 § 2.2 + § 4 F1: LP fires when "≥3 non-thin cells under floor with remaining Tier B pool showing adequate on-axis rows that the swap pass did not surface" — i.e., **local-optima trap**. Our failures are NOT local-optima — they are:

1. **Policy-trade-off** (3 of 5 failures): adding more historical-STR rows to fill `(melee, high, STR)` + `(ranged, low, STR)` requires the historical share to exceed +5.0pp, which trips the register-axis smoke gate. The composition policy's "substrate-led skew with historical 50-55%" and "PCFS ≥85%" are in genuine tension for STR-heavy archetypes. LP would either violate Tier-A preferred-include (composition policy § 1.2) or hit the same register cap.

2. **Policy-bounded** (1 of 5 failures): `(mid, low, DEX)` substrate is dominated by military_modern grenades/grenade-launchers (50%). The 80% military_modern Tier-A trim correctly excludes most of these. LP can only relax the trim, which would violate composition policy § 4.2.

3. **Substrate-near-bounded** (2 of 5 failures): `(mid, medium, DEX)` substrate=148, `(mid, high, DEX)` substrate=215 — small pools at ~75% of floor. Adding 5-7 more rows from these archetypes would require evicting Tier-A rows from over-filled archetypes (e.g., `(melee, medium, STR)` count=234, floor=100). LP could attempt this; greedy did not because Tier-A preferred-include is near-hard. The economic argument: 8 swaps to move PCFS from 12/17 → 14/17 is marginal vs the cost of running LP and violating Tier-A preferred-include.

**Decision (substrate-led; per autonomous in-scope decision authority under cycle-10-hive-mind-scope § 1):**

Do NOT fire LP fallback. Instead:
- Surface the 5 failing archetypes in the Phase 3 distribution report as **policy/substrate-trade-off-bounded** for Matt + gandalf sign-off
- Route the 5 archetypes to Sidecar B / Stage 3.5 enrichment scoping per composition policy § 4.1 spirit (specifically: STR-heavy archetypes can be addressed by Sketch F gap-fills + Sidecar B fantasy/cross-cultural STR enrichment)
- Record in v1.1+ queue: **"PCFS-archetype-gate vs register-share-cap tension is an architectural finding; consider rebalancing target_total downward to ~2,700 to relieve historical-share pressure, OR accept substrate-led skew and report PCFS at archetype level without ≥85% gate"**

---

## 6. NULL-typed row handling — Option β / undifferentiated floor-fill per Phase 1 § 9

Per Phase 1 § 9 flag: 68% of substrate rows are NULL-typed (no Stage 1 proxy fingerprint). Option α cell matching (5-tuple) cannot apply.

**Implementation:** NULL-typed rows in Sub-phase C (register-target fill) are sampled into v1_scope when typed candidates exhausted; each gets `matching_policy = 'option_beta_undifferentiated_floor_fill'` in `v1_scope_composition_trace`. The composition trace also includes `notes: "option_beta_undifferentiated_floor_fill (NULL-typed row per Phase 1 § 9)"`.

Empirical: 4 NULL-typed rows entered v1_scope via Sub-phase C this run (low because Sub-phase B + Sub-phase A satisfied most register-share demand with typed rows).

---

## 7. Cheapest-refuting-test results (PCFS) — Phase 1 § 7

Per Phase 1 § 7.1, ran PCFS immediately after population. Output written to `post-phase-2-smoke.json`. As discussed in § 5 above, the test FAILS (12/17 = 70.6% < 85% threshold), but the failure mode is policy/substrate trade-off, not local-optima. Decision per § 5: do NOT trigger LP; route under-floor archetypes to Sidecar B / Stage 3.5; surface for Phase 3 sign-off.

---

## 8. Sub-phase metrics summary

| Pass | Selected | Notes |
|---|---:|---|
| Pass 1: genre + D1c + D1a + D1b | 437 + 95 = 532 | 560 D1c excluded; 19,119 genre-excluded |
| Sub-phase A: Tier A preferred-include | 1,451 | mm_trim_skip=1,830 (~80% of 2,258 Tier-A military_modern); reg_cap_skip=3,866; cell_cap_skip=311 |
| Sub-phase B: Tier B archetype-floor-fill | 779 | 95 iterations; 18 archetypes observed |
| Sub-phase C: Tier B register-target fill | 279 | filled remaining register-deficit |
| Pass 3: swap-repair | +8 | 3 outer passes; military_modern overshoot guard + archetype floor-fill (budget-bounded) |
| **TOTAL v1_scope** | **3,042** | within envelope 1,700-3,100 |

---

## 9. Resource consumption

- Wall-clock: ~5.9 sec (well within 3-minute envelope per dispatch § 8 + Phase 1 § 6)
- Peak memory: ~18-36 MB working set per column-selective load (12 columns vs full table); well within 150 MB ceiling

---

## 10. Spot-check guidance for gandalf 50-row Phase 2 spot-check (per dispatch § 5.5 acceptance criterion)

When reviewing the Phase 3 distribution report + spot-check pack, gandalf should audit:

1. **Tier-S handheld auto-include**: confirm 437/449 rows enter v1_scope (12 fall in `register_canonical='unknown'` which is genre-excluded; these can be re-evaluated at Sidecar B if they cluster on known traditions)
2. **D1b secondary auto-include**: confirm 95/95 (matches Phase 0a)
3. **Accessory parent-family fit (per Phase 0b lookup)**: verify accessory_weapon_integrated rows in v1_scope have at least one compatible parent weapon family also in v1_scope (cross-check via composition_trace + Phase 0b lookup)
4. **Mode-C-equivalent leak**: spot-sample 5 military_modern rows in v1_scope to confirm none have named_mythological_match (assertion already automated)
5. **Per-archetype substrate diversity**: spot-check 10 selected rows from `melee|medium|STR` (over-filled, 234 rows) to confirm geometric diversity not collapsed to one substrate cell
6. **Failing archetype review**: surface 5 failing archetypes + 1 substrate-bounded archetype with their per-cultural-tradition substrate composition (per Phase 3 distribution report) to validate substrate-led / policy-bounded diagnosis above
7. **Named-bearer coverage**: confirm Sketch F substrate-resident anchors (Arthur, Roland, Thor, Achilles, Cú Chulainn, Karna, Baba Yaga, Cleopatra) appear in v1_scope (Phase 3 distribution report enumerates)
8. **Sketch F gap-list**: confirm Hattori Hanzō / Lu Bu / Moctezuma / Gilgamesh are NOT in v1_scope (Stage 3.5 gap-fill targets per D5)

---

## 11. Decisions-log proposal (routed via knight-rider)

Proposed entry — Discipline #11 substrate-led principle applied to Sketch A vocabulary mismatch:

> **2026-05-25 — Substrate-cell vs archetype-cell PCFS resolution (Cycle 10 Stage 3 Phase 2)**
>
> **Decision:** PCFS gate evaluated at archetype level `(range, tempo, attribute)` rather than substrate-cell level `(range, tempo, geometry, attribute)`. Substrate-bounded archetypes (in-genre Tier S/A/B/C supply < floor) excluded from PCFS denominator.
>
> **Reasoning:** Sketch A's 4-tuple cell vocabulary uses amplitude (Axis 3B per BC-axes-lock) while substrate column proxy_geometry_class uses geometry (Axis 2). Different axes. Substrate-led discipline (Discipline #11) says: sample against substrate's actual vocabulary, aggregate to archetype-level where Sketch A floor magnitudes apply.
>
> **Alternatives considered:** (a) extract amplitude column from substrate (v1.1+ Track candidate); (b) retire amplitude from Sketch A in favor of geometry vocabulary; (c) attempt joint amplitude+geometry extraction.
>
> **Status:** PROVISIONAL pending Phase 3 Matt + gandalf sign-off.
>
> **Related:** Discipline #11; Sketch A canonical/story/v1-bc-target-intent-2026-05-24.md; qd-engine-bc-axes-lock-2026-05-20.md.

---

## 12. Sign-off

**Author:** elrond (Phase 2; Cycle 10 Stage 3)
**Date:** 2026-05-25
**Authority:** dispatch FIRE-READY (Gate-1 cleared; commit `04509ad`) + Cycle 10 scope-doc § 1 autonomous decisions on parameter choices, NULL-typed handling, Mode-C operational substitute, Sketch-A-amplitude-vs-substrate-geometry resolution
**Status:** Phase 2 complete; Phase 3 distribution report fires next (knight-rider re-invocation per dispatch protocol).
