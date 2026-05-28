# Gate-6 Disposition — Case 8 Empirical Re-Disposition (79× Gap Quantification) — 2026-05-28

**Reviewer:** jack-ryan
**Severity:** BLOCK (Pattern-B escalation — Matt architectural call required; empirical quantification closes pre-empirical optionality)
**Authority:** Dispatch `agentic_orchestration/dispatches/2026-05-28-jack-ryan-gate-6-case-8-empirical-re-disposition.md`; gamora empirical DPS sweep at engine `d83049a`; post-rebase Track 1 telemetry `option-f-track-1-post-rebase-telemetry.json`; Gate-5 D1+D2+D3 ratifications (hive-mind state); jack-ryan Gate-5 disposition at `3251b6d`
**Target:** engine `d83049a` + tag `gamora/v2.1-boss-hp-rebase-1` + meta `2959db3`
**Developer:** gamora (boss HP rebase executor)
**Principles applied:** Review Principles 1, 2, 3, 4, 5
**Disciplines cited:** #11, #18, #39, #40 case (c), #42

---

## § 1 — Trigger + Scope

### § 1.1 Escalation Signal: Empirical 79× DPS Gap Confirmed

Option 1 (Boss HP Rebase) executed correctly per Matt Gate-5 D1 ratification. Boss HP `(9.00, 14.00)` → `(10.50, 12.60)` per gamora math note `boss-hp-rebase-case-8-resolution-2026-05-28.md` § 11.4 (Amendment B p25/p75 spread; population Balanced median KPM=77.448 anchor). The rebase IS the calibration the ANCHOR INTENTS scaffold was waiting for — that aspect of D1 rationale holds.

**What D1 could not anticipate:** the empirical DPS sweep (math note § 11.3) found that STR/DEX physical DPS ≈ 3,750 HP/s vs INT/WIS magical DPS ≈ 297,000 HP/s — a 79× gap. Boss HP at KPM=75 per path: physical ~3,000 HP (factor 0.15×); magical ~237,500 HP (factor 11.88×). No single boss HP value spans 79×. The acceptance criterion (≥12/18 emit) was NOT MET: 3/18 post-rebase (same as pre-rebase).

**This is NOT a 9th case.** Gate-5 § 2.2 deeper framing explicitly diagnosed population-wide two-path divergence as the structural root cause. The 79× figure is empirical quantification of that structure, not a new finding. Gate-5 § 5 warning is now empirically validated: *"Option 6 (damage/HP%) resolves that architectural truth by design rather than adding 72 per-kit KPM calibration values that still inherit the two-path divergence problem."*

### § 1.2 Scope of This Gate-6 Disposition

This disposition provides:
- § 2: Empirical signal capture (verbatim telemetry + math-note derivations)
- § 3: Re-rank of Options 2/3/5/6 against empirical 79× anchor
- § 4: Cycle 14 v1 close trajectory re-assessment per option
- § 5: Discipline #18 refinement consideration — legolas Mode A consultation timing
- § 6: § 3.11 retraction-loop framing amendment
- § 7: Recommendation + rationale
- § 8: Open questions for Matt Pattern-B ratification

What this disposition does NOT do: implement any option; amend gamora's canonical doc § 3.9 or MIGRATION.md § v1.39; retract gamora's `v2.1` tag or boss HP rebase values; pre-author Option 6 metric formulation specifics.

---

## § 2 — Empirical Signal Capture (Discipline #11)

### § 2.1 Post-Rebase Telemetry — Verbatim Source

**Source:** `agentic_orchestration/cycle-14-wave-5-season-001/option-f-track-1-post-rebase-telemetry.json`
**Run at:** 2026-05-28T12:13:38Z (gamora post-rebase Track 1 sweep; authority: Matt D1 ratification 2026-05-28)

| Archetype | Kit count | Boss KPM observations | Median KPM (Balanced) |
|---|---|---|---|
| `str_physical` | 4 | **0** ([] — zero observations) | 0.0 |
| `dex_physical` | 4 | **0** ([] — zero observations) | 0.0 |
| `int_magical` | 5 | [73.171, 82.192, 82.192] (3 obs) | 82.192 |
| `wis_faith` | 5 | [63.83, 68.182, 65.934, 82.192, 78.947, 75.949, 98.361] (7 obs) | 75.949 |

**Band table post-rebase:** functionally identical to pre-rebase (STR/DEX: FALLBACK notation RETAINED; INT/WIS: unchanged values). Boss HP midpoint shift +1,000 HP (+0.4%) was insufficient to change which kits produce KPM signal.

**Season emit post-rebase: 3/18.** Same as pre-rebase. Acceptance criterion (≥12/18) NOT MET.

### § 2.2 DPS Gap Derivation (Math Note § 11.3 Verbatim)

From gamora math note § 11.3 (DPS sweep at boss HP 15,000 test level; direct fight test on STR heavy_barbarian kit):
- STR/DEX physical DPS: 5/5 fights killed; DPS range 2,941–5,000 HP/s; **median ≈ 3,750 HP/s**
- Boss HP at KPM=75 for physical path: `3,750 × 60 / 75 = **3,000 HP** (factor 0.15×)`
- INT/WIS magical DPS (back-calculated from Track 1 Balanced median KPM=77.448, boss HP mid=230,000): `77.448 × 230,000 / 60 = **297,000 HP/s**`
- Boss HP at KPM=75 for magical path: `297,000 × 60 / 75 = **237,600 HP** (factor 11.88×)`

**Gap: 79×.** This is the empirical quantification of the structural two-path divergence diagnosed at Gate-5 § 2.2. No single boss HP value spans 79×.

### § 2.3 What the Rebase Accomplished (Keeping D1 Rationale Intact)

The ANCHOR INTENTS scaffold in `endgame_mob_stat_profile.py` (commit `ee15c96` line 43) IS closed. Boss HP is now calibrated to the INT/WIS population at KPM=75. The rebase executed exactly what D1 rationale described: "rebase IS the calibration SC-6 deferred to Phase 7 gate." The boss HP factor range (10.50, 12.60) is now empirically grounded to the INT/WIS population DPS.

The acceptance criterion failure is not a rebase execution failure — it is confirmation that the structural two-path divergence is 79× wide, which no boss HP value can span. MIGRATION.md § v1.39 correctly records both: "the calibrated range is correct for the INT/WIS population; the physical path gap is the pre-identified Cycle 15 scope item."

---

## § 3 — Re-Rank: Options 2/3/5/6 Against Empirical 79× Gap

Options are re-ranked from the Gate-5 set (Option 1 was executed and confirmed). Option 4 (T1 threshold widen) remains excluded — math note § 11.2 confirms the T1 REJECT fires at KPM=15 when band_center=75.0 (kpm_delta=0.8 >> 0.30), and widening the threshold does not change the outcome for kits producing KPM≈0 at the calibrated boss HP.

---

### Option 6 — Cycle 15 Option C Metric Replacement (Promoted to First-Tier Recommendation)

**Design:** Replace KPM with `damage_fraction_per_fight = total_damage_dealt / encounter_total_HP`. Class-agnostic, path-agnostic metric denominated by the encounter's own HP. Physical and magical damage both contribute to `total_damage_dealt`; the denominator is `encounter_total_HP` — shared across both paths. Two-path divergence absorbed at metric definition layer.

**Post-empirical assessment:**

The 79× gap is not a calibration magnitude problem. Physical DPS at 3,750 HP/s is what `family_baseline × amplitude_mean` (SC-6b) produces; that formula produces consistent internal values for the physical path. The structural issue is that SC-6b and SC-7 have independent calibration origins and produce DPS values that differ by 79×. Per-kit KPM calibration inherits this: any 72-value calibration table (18 kits × 4 cohorts) must either (a) set STR/DEX boss HP targets at ~3,000 HP (unfeasible — at 3,000 HP, a single hit overkills most bosses) or (b) set different per-kit boss HP pools (different boss encounters per archetype — architectural fragmentation) or (c) calibrate per-kit damage multipliers to produce the same DPS despite different formula paths (large-scale substrate surgery). Option 6 eliminates the dependency by changing what is measured: damage as a fraction of encounter HP converges regardless of which formula path produced the damage.

**Discipline compliance:**
- Discipline #11: PASS — metric is empirically grounded to encounter HP denominator; measurable from fight output
- Discipline #18: REQUIRES legolas Mode A methodology consultation before Cycle 15 dispatch authoring (Matt Gate-5 D2 pre-flight; see § 5 below)
- Discipline #39/40: CLEAN long-term — retires KPM gate scaffold, STR/DEX FALLBACK bands, SC-6b-uncalibrated scaffold, SC-7 per-kit extension scaffold in one architectural move
- Discipline #42: PASS — addresses the deeper framing (population-wide two-path divergence) by design, not calibration

**Effort post-empirical:** unchanged from Gate-5 D2 estimate — ~0.5d legolas Mode A consultation + ~0.75d jack-ryan canonical metric definition + ~1.5-2d gamora implementation = ~2.75-3.25d. Plus mini-boss tier calibration scope deferred in Amendment A (separate Cycle 15 item).

**Cycle 14 v1 close trajectory:** CANNOT close Cycle 14 alone. Cycle 15 scope per Matt D2. However: if Option 5 provides the Cycle 14 administrative close, Option 6 fires immediately at Cycle 15 entry → combined path resolves in ~3.75-4.25d from the Option 5 close decision.

**Risk register post-empirical:** LOW — empirical 79× gap removes the theoretical alternative of per-kit KPM calibration being sufficient. The gap is not a calibration magnitude shortfall addressable by adjusting multipliers; it is a two-path formula divergence. Option 6 is now MORE strongly motivated than at Gate-5, not less. The pre-flight (legolas Mode A consultation) is the only remaining uncertainty — see § 5.

**Discipline #39 / D3 composition:** Option 6 subsumes D2 Phase 2 per-encounter-type KPM bands (per § 3.13 — encounter-type-agnostic metric eliminates the encounter-type × archetype × cohort dimensionality). Also makes the KPM ceiling 600.0 investigation lower-stakes (if KPM is replaced, ceiling becomes historical artifact; investigation retains diagnostic value for Option 6 implementation).

**Recommendation rank: 1 (architectural resolution; correct Cycle 15 target)**

---

### Option 3 — Per-Kit Damage Calibration NOW (SC-6b advance, Cycle 14)

**Design:** Full per-kit calibration sweep across all 18 kits × 4 cohorts in Cycle 14. Produces per-kit `base_physical_damage_l50` revision (SC-6b) AND per-kit spell damage variants (SC-7 extension) calibrated against boss HP targets.

**Post-empirical re-assessment:**

The 79× gap changes the calculus. At Gate-5, Option 3 was ranked #4 (correct architecture; wrong timing). Post-empirical, Option 3 faces a harder constraint: SC-6b physical damage calibration against the current boss HP pool (210k-252k at new factor range) requires per-kit `base_physical_damage_l50` values to be multiplied by ~79×. That is not a calibration adjustment — it is a substrate-scale redesign. The SC-6b formula (`family_baseline × amplitude_mean`) produced martial-heavy=177, martial-light=99, ranged=91. To produce DPS ≈ 297,000 HP/s (the INT/WIS calibrated level), per-kit physical damage values would need to reach ~40,000-60,000 HP/s baseline — a factor of ~200-300× above the current SC-6b substrate values.

**This is feasible** (multiply SC-6b values by the required factor; the formula infrastructure supports arbitrary values) but it would represent a large-scale substrate surgery that: (a) requires math-note justification for the new SC-6b values (Discipline #1); (b) requires rocket cross-seam review for the substrate constant change scope; (c) still leaves the two-path metric divergence in place at the KPM layer (per-kit KPM calibration inherits the two-path problem as noted at Gate-5 § 5).

**Partial architectural resolution at cost of full SC-6b substrate surgery.** Option 3 closes the 79× DPS gap via calibration; it does NOT close the two-path metric divergence. A physical kit with 297k HP/s would score KPM in the INT/WIS band range — but the calibration is a numerical coincidence, not a metric architecture. Option 6 eliminates the metric architecture problem; Option 3 papers over it with large-scale calibration.

**Discipline compliance post-empirical:**
- Discipline #11: PASS — per-kit empirical calibration is the gold standard
- Discipline #39: PARTIAL — closes SC-6b/SC-7 scaffolds via calibration; two-path divergence persists as architectural debt
- Discipline #18: REQUIRES methodology consultation (how to calibrate SC-6b at 79× scale; what is the source-of-truth formula post-calibration)
- Discipline #40: PARTIAL — retires scaffolds but at the cost of a new large-scale calibration table that inherits the divergence

**Effort post-empirical:** INCREASED from Gate-5 estimate. Gate-5 estimate was ~2-3d gamora. Post-empirical: SC-6b surgery at 79× scale requires: (a) Discipline #1 math note for new SC-6b values (~0.5d jack-ryan/gamora); (b) rocket cross-seam review for substrate surgery (~0.25d coordination); (c) gamora per-kit calibration sweep (~2-3d gamora). Total: ~3-4d, at the boundary of Cycle 15 scope.

**Cycle 14 v1 close trajectory:** AT HIGH RISK. SC-6b substrate surgery at 79× scale is Cycle 15-scope work dressed as Cycle 14 execution. If methodology consultation fires (Discipline #18 requirement), Cycle 14 close slips to Cycle 15 timeline.

**Risk register post-empirical:** HIGH RISK (post-empirical). The 79× calibration surgery is a deeper rabbit hole than per-kit KPM calibration implied at Gate-5. It is NOT equivalent to the "72 band values" framing from Gate-5 — it requires fundamental SC-6b redesign. The substrate surgery may surface additional cases (#9 or beyond) as newly calibrated physical damage paths interact with other game systems.

**Recommendation rank: 3 (feasible but large-scale; not preferred Cycle 14 path; better as Cycle 15 fallback IF Option 6 consultation surfaces blockers)**

---

### Option 2 — Option 5 Cycle 14 Close + Option 6 Cycle 15 (Composite Path)

**Design:** Accept 3/18 emit as Cycle 14 v1 close (infrastructure delivery tag); fire Option 6 metric replacement at Cycle 15 entry as the architectural close. This is the same composite-path architecture that Gate-5 identified as the alternative if Option 1 (boss HP rebase) plus Option 2 were preferred.

**Post-empirical re-assessment:**

At Gate-5, this composite was described as "defers architectural resolution to Cycle 15 as originally planned" — which was framed against Option 1's ability to unblock D9 close criterion in Cycle 14. Post-empirical: Option 1 did NOT unblock D9 (3/18 post-rebase = same as pre-rebase). This means Option 2 is no longer "deferring from Cycle 14 close" — the Cycle 14 D9 close criterion IS already deferred by the empirical outcome of Option 1.

Option 2 is now the **composite that acknowledges the empirical reality** without trying to extend Cycle 14 scope. It closes Cycle 14 administratively at the infrastructure delivery level and routes the architectural resolution to Cycle 15 where Option 6 (D2-ratified) is the planned fix.

**What Option 2 specifically comprises post-empirical:**
1. **Option 5 component** (~0.1d KR): amend D9 close criterion to accept Cycle 14 v1 = Track 1 infrastructure delivery (per-archetype band table operational; 3/18 emit at Cycle 14; calibration gap documented as Cycle 15 item). Semantic of v1 tag: "no-classes substrate-led infrastructure landed; per-damage-path Phase 7 gate operational; emit 3/18 at Cycle 14 (physical path two-path divergence deferred Cycle 15 per D2)."
2. **Option 6 component** (Cycle 15, ~2.75-3.25d): damage/HP% metric replacement per Matt D2 ratification. Subsumes D2 Phase 2 per-encounter-type bands. Legolas Mode A pre-flight per D2 ratification.

**Gate interaction:** the D9 close criterion amendment requires Matt D7 authority (Matt holds close-criterion amend authority per ADR-002 tiered approval). This is a known escalation path — Gate-6 surfaces it as explicit rather than implicit.

**Discipline compliance:**
- Discipline #39: WARN — scaffolds (STR/DEX FALLBACK, SC-6b uncalibrated, mini-boss tier) persist into Cycle 15. Explicitly staged for retirement under Option 6, not left indefinitely.
- Discipline #40: CONDITIONAL PASS — retirement timeline is explicit (Cycle 15 Option 6). The FALLBACK notation now reads as canonical marker of two-path divergence (see § 6 framing amendment) rather than transient artifact.
- Discipline #13a-partition: PASS — physical path divergence is structural, not an oversight; Option 2 correctly routes it to architectural resolution
- D13 P1-P9 parallel framework: the downstream quality concern from Gate-5 § 4 Option 5 applies here — parallel season production under 3/18 emit produces near-empty physical kit archives. This is the primary quality cost of Option 2's Cycle 14 close.

**Effort:** ~0.1d KR (close-criterion amendment) + ~0.25d jack-ryan (decisions-log 8th-case resolution entry + § 3.11 framing update) + Cycle 15 Option 6 effort.

**Cycle 14 v1 close trajectory:** IMMEDIATE administrative close (0.1d); Cycle 15 architectural close ~2.75-3.25d from Cycle 15 entry. If legolas Mode A consultation fires concurrently with Cycle 14 D13 P1-P9 (if those are compatible), Cycle 15 entry can fire immediately on Cycle 14 tag.

**Risk register post-empirical:** MODERATE. The D13 P1-P9 quality debt is real — parallel seasons under 3/18 emit produce content with limited physical-archetype representation. The risk is accepted as time-bounded (Cycle 15 Option 6 resolves) but is non-trivial for player-facing content quality in the interim.

**Recommendation rank: 2 (correct composite path; moderate quality debt that is time-bounded)**

---

### Option 5 — Cycle 14 Close-Criterion Amendment Alone (Accept 3/18 Emit; No Cycle 15 Commit Upgrade)

**Design:** Amend D9 close criterion to accept Cycle 14 v1 close at 3/18 emit as infrastructure delivery, with NO promoted Cycle 15 architectural commitment beyond the existing D2 ratification.

**Post-empirical re-assessment:**

At Gate-5, Option 5 was ranked #5 with AVOID guidance due to: (a) Disciplines #39/#40 violation from scaffolds persisting without retirement timeline; (b) D13 P1-P9 downstream quality debt. Post-empirical, Option 5 is essentially the Option 2 path MINUS the legolas consultation timing acceleration for Option 6.

**The distinction between Option 5 (standalone) and Option 2 (composite) post-empirical:**
- Option 5 standalone: administrative close, Cycle 15 proceeds per existing D2 ratification but WITHOUT explicit Gate-6 re-commitment to legolas consultation timeline or pre-authorization for Cycle 15 early entry.
- Option 2 composite: administrative close PLUS explicit routing of legolas consultation into Cycle 14 final wave (pre-authorizing Cycle 15 Option 6 dispatch authoring at Cycle 14 v1 tag).

The standalone Option 5 is weaker because it leaves the Cycle 15 Option 6 in the "ratified but not yet dispatched" state without a concrete pre-flight action. Given the 79× empirical confirmation, the Matt Pattern-B ratification at Gate-6 is the right venue to also confirm the legolas consultation timing — this is the difference between Option 5 and Option 2.

**Discipline compliance:**
- Discipline #39: FAIL (standalone) — scaffolds persist without retirement timeline visible at Gate-6; D2 ratification exists but is not re-committed at this gate
- Discipline #40: WARN — retirement is implicit in D2 ratification; explicitly re-routing at this gate to Option 2 framing makes it CONDITIONAL PASS
- D13 P1-P9 quality debt: same as Option 2 (applies to both paths)

**Effort:** ~0.1d (same as Option 2 Cycle 14 component). The delta is zero effort — Option 5 standalone vs Option 2 composite is a framing decision, not an effort decision.

**Cycle 14 v1 close trajectory:** IMMEDIATE — same as Option 2.

**Recommendation rank: 4 (dominated by Option 2; no additional effort required to promote to Option 2; Option 5 standalone leaves Cycle 15 less pre-authorized)**

---

## § 4 — Cycle 14 v1 Close Trajectory Re-Assessment Per Option

### D9 Close Criteria (≥12/18 × 3 seasons emit; Gate-2 PASS; A/B filed; v1 tag)

| Option | D9 close post-empirical | Gate-2 PASS path | v1 tag timing | v1 semantic |
|---|---|---|---|---|
| Option 6 alone (Cycle 15 promote) | CANNOT close Cycle 14 | Cycle 15 | Cycle 15 | N/A |
| Option 3 (per-kit calibration NOW) | AT HIGH RISK — SC-6b surgery 79× scale; methodology consultation required | Cycle 15 if consultation fires | Cycle 15 risk | Full per-archetype emit |
| Option 2 (Opt 5 + C15 Opt 6) | ADMINISTRATIVE CLOSE — amend to infrastructure delivery | D7 close-criterion amend | Immediate | "no-classes substrate-led infra; emit 3/18; physical path C15" |
| Option 5 (standalone) | ADMINISTRATIVE CLOSE — same as Option 2 | Same | Immediate | Same as Option 2 |

### D7 Escalation (Close-Criterion Amend Authority)

- **Options 2 and 5:** D7 fires — D9 close criterion amendment (3/18 accept) requires Matt explicit authority per ADR-002. This is the Matt Pattern-B question at Gate-6.
- **Option 3:** D7 may fire if SC-6b surgery encounters unexpected failures or scope expansion; methodology consultation is the primary gating item.
- **Option 6 (Cycle 15):** D7 not applicable within Cycle 14.

### D13 P1-P9 Parallel Framework Impact

- **Options 2 and 5 (immediate Cycle 14 close):** P1-P9 parallel seasons fire under 3/18 emit → 15/18 kits produce near-empty kit archives. Physical-archetype kits (8 STR/DEX) contribute zero emit; INT/WIS non-artillery kits (10-12 kits) also produce near-zero boss KPM. The 3 passing kits (artillery_mage, and the WIS kits that produce signal) dominate season content under the current gate. This is the primary quality cost of any Option-5-adjacent path.
- **Option 3:** P1-P9 preserves after per-kit calibration lands; higher kit diversity expected.
- **Option 6 (Cycle 15 primary):** P1-P9 fires at Cycle 15 entry post-Option-6 implementation, where damage/HP% metric gates all kits path-agnostically. Expected broader kit diversity. The delay vs Option 2 is the Option 6 implementation time (~2.75-3.25d).

### Cycle 14 Close Trajectory — Revised Estimates

Pre-empirical Gate-5 estimate: ~4-6 days to v1 close (under Option 1 success assumption). Post-empirical re-assessment:

| Option | Cycle 14 close estimate | Cycle 15 commitment | Total to architectural close |
|---|---|---|---|
| Option 2 (RECOMMENDED) | Immediate (0.1d amendment) + push/tag | Cycle 15 Option 6: ~2.75-3.25d from entry | ~3-4d total (C14 tag + C15 Option 6) |
| Option 3 | At risk; ~3-4d + methodology; Cycle 15 risk | N/A (closes in Option 3) | ~3-4d + uncertainty |
| Option 5 (standalone) | Immediate (same as Option 2) | Existing D2 — no pre-authorization upgrade | ~3-4d C15 Option 6 (same as Option 2 but less committed) |
| Option 6 advance (promote C14) | ~3.5-4.5d from legolas consultation fire | N/A | ~3.5-4.5d from consultation |

**Observation:** Option 2 and "Option 6 promoted to Cycle 14" have converging timelines (~3-4d) when legolas consultation is accounted for in both. The distinguishing factor is Discipline #18 compliance: Option 6 requires methodology consultation BEFORE implementation; Option 2 fires consultation concurrently with Cycle 14 administrative close and gates Option 6 implementation on consultation output. Option 2 is the path that correctly respects Discipline #18 sequencing.

---

## § 5 — Discipline #18 Refinement: Legolas Mode A Consultation Timing

### § 5.1 The Discipline #18 Gate Question

Matt Gate-5 D2 pre-flight (verbatim at hive-mind state): *"legolas Mode A methodology consultation on metric formulation (~half day) before Cycle 15 dispatch authoring fires."*

Dispatch § 1.3 question: does the post-rebase Track 1 telemetry (79× empirical gap) NOW constitute the baseline empirical signal per Discipline #18 refinement? If so, consultation can fire DURING Cycle 14 rather than waiting for Cycle 15 entry.

### § 5.2 Determination: YES — Baseline Signal Criterion MET

**Discipline #18 refinement § 18.2** states methodology consultation at extension hotspots fires AFTER baseline empirical signal lands. Track 1 IS the baseline. Per Phase 7 doc § 3.10 (Track 2 forward-link): *"Track 1 provides the baseline empirical signal. Before Track 2 methodology is locked... per-archetype KPM variance distributions... physical-vs-magical path divergence magnitude... how wide is the KPM gap..."*

The empirical 79× gap answers the Phase 7 doc § 3.10 framing question explicitly: physical-vs-magical path divergence = 79×. All three baseline empirical questions enumerated in § 3.10 are now answerable:

1. "Are 4 archetypes sufficient, or is intra-archetype variance high enough to warrant per-kit Track 2 Option A?" → Answer: 4 archetypes are NOT sufficient to span 79× divergence; the divergence is at formula-path level, not intra-archetype level. This argues FOR Option C (damage/HP%) over Option A (per-kit KPM) as Track 2.
2. "Do archetype bands vary meaningfully across cohorts, or are per-archetype bands cohort-stable?" → Track 1 telemetry shows INT/WIS bands are cohort-variant (DPS-min-maxer: 73.562-122.603; Defensive: 47.671-79.452). Physical path bands are FALLBACK. Cohort variation is real but secondary to the formula-path divergence.
3. "How wide is the KPM gap between STR-physical and INT-magical at the same cohort level?" → **79×** (empirically confirmed at gamora math note § 11.3).

**Conclusion:** all three Discipline #18 baseline questions are answered. Methodology consultation can fire DURING Cycle 14 in parallel with the Option 2/5 administrative close.

### § 5.3 Operational Implication

**Legolas Mode A consultation CAN fire during Cycle 14 wave 5-close activities.** This is the correct sequencing under Discipline #18 — consultation fires after baseline lands (Track 1 + rebase telemetry IS the baseline) and before Option 6 dispatch authoring (which produces the Discipline #1 math note that locks metric definition and gamora implementation spec).

**Specific trigger:** Gate-6 disposition landing (this document) is the trigger for KR to queue legolas Mode A consultation dispatch. The consultation does not gate Cycle 14 v1 tag — it gates Cycle 15 Option 6 dispatch authoring.

**Discipline #18 pre-authorization pattern:** Matt Gate-5 D2 pre-flight already pre-authorized consultation at Cycle 15 entry. Gate-6 finding advances that pre-authorization: consultation fires during Cycle 14 close wave (concurrent with Option 2 administrative close steps) rather than waiting for Cycle 15 entry. This is NOT a scope expansion — it is earlier execution of a D2-pre-authorized item.

---

## § 6 — § 3.11 Retraction-Loop Framing Amendment

### § 6.1 Prior Framing (Phase 7 Doc § 3.11 as Authored — Third Iteration Pre-Rebase Result)

Phase 7 doc § 3.11 Step 4 stated the retraction completion criterion as: *"§ 3.9 FALLBACK notation absent; all 16 cells populated with post-rebase Track 1 empirical values; gamora tag `gamora/v2.1-boss-hp-rebase-1` cut; smoke ≥12/18 season_emit verified."*

This retraction was authored in a pre-empirical state — when it was expected that boss HP rebase would produce broad emit signal and populate all 16 cells with physical kit observations.

### § 6.2 What the Rebase Actually Produced

Post-rebase Track 1 sweep (`option-f-track-1-post-rebase-telemetry.json`): STR/DEX still produce zero boss KPM observations (boss_kpm_observations: [] for both str_physical and dex_physical). FALLBACK notation RETAINED post-rebase. The gamora tag `gamora/v2.1-boss-hp-rebase-1` is cut; the smoke criterion (≥12/18) was NOT met.

**Result:** the § 3.11 retraction completion criterion AS WRITTEN cannot be met by Option 1 alone. FALLBACK notation will not become "absent" via boss HP rebase — it can only become absent via Option 6 (damage/HP% metric replaces KPM entirely, making FALLBACK bands moot) or Option 3 (SC-6b surgery calibrates physical DPS to 79× current values, producing physical kit boss KPM signal).

### § 6.3 Proposed § 3.11 Framing Amendment

**The FALLBACK notation is no longer a transient artifact awaiting rebase completion. It is now a CANONICAL MARKER of the two-path divergence architectural finding.**

Specifically: FALLBACK in STR/DEX cells = the empirically-confirmed signature that the physical damage formula path (SC-6b substrate-bound, `family_baseline × amplitude_mean`) and the magical damage formula path (SC-7 engine-calibrated, `BASE_SPELL_DAMAGE_L50`) diverge by 79× in DPS output. The FALLBACK is not a "calibration not yet possible" notation — it is a "calibration not possible under current metric architecture" notation.

**Proposed replacement for § 3.11 Step 4 retraction completion criterion:**

> *FALLBACK retraction-loop SUSPENSION: gamora post-rebase Track 1 sweep (tag `gamora/v2.1-boss-hp-rebase-1`) confirms FALLBACK notation RETAINED as Case 8 structural finding per MIGRATION.md § v1.39. FALLBACK is NOT a transient calibration artifact — it is a canonical marker of the 79× physical-vs-magical DPS divergence (math note `boss-hp-rebase-case-8-resolution-2026-05-28.md` § 11.3). The retraction loop does NOT close via boss HP rebase. FALLBACK retirement tied to Cycle 15 Option 6 metric replacement (damage/HP% metric makes FALLBACK bands moot — metric is path-agnostic) OR Option 3 SC-6b calibration to bridge the 79× gap (restores per-path boss KPM signal at calibrated DPS). Until one of those conditions is met, FALLBACK cells in § 3.9 are the correct canonical state.*

**Cite:** Discipline #40 case (c) — retraction record update; Discipline #42 — framing consistency between § 3.11 retraction criterion and empirical finding.

### § 6.4 What Remains Unchanged

Phase 7 doc §§ 3.9, 3.12, 3.13 are not amended by this Gate-6 disposition. Specifically:
- § 3.9 FALLBACK notation is RETAINED and is now correctly annotated as "Case 8 structural finding" per the gamora update noted in that section's current text (already updated by gamora in the third iteration of this document; the text at § 3.9 already reads "FALLBACK notation (STR-physical, DEX-physical) — RETAINED post-rebase (Case 8 structural finding)"). Gate-6 confirms that framing is correct.
- § 3.13 Option 6 Cycle 15 forward-link remains canonical (D2-ratified; pre-flight noted). Gate-6 adds: legolas consultation can fire during Cycle 14 (per § 5 above).
- The FALLBACK → Option 6 forward-link in § 3.9 reads: *"When physical DPS is recalibrated OR when Option 6 (damage/HP% metric) replaces KPM, physical kit FALLBACK bands will be replaced with empirical values."* This is correct and is reinforced by Gate-6 findings.

---

## § 7 — Recommendation + Rationale

### § 7.1 Recommended Path

**RECOMMEND: Option 2 (Composite — Option 5 Cycle 14 Administrative Close + Option 6 Cycle 15 Architectural Close) with Legolas Mode A Consultation Firing Concurrently During Cycle 14 Close Wave.**

**Primary rationale:**

1. **Empirical confirmation removes pre-empirical optionality.** Option 1 was the right lever to attempt (it closed the ANCHOR INTENTS scaffold and produced the 79× empirical measurement). The 79× gap is now the empirical ground truth. Options 3 and 6 are the two architectural responses. Option 3 requires 79× SC-6b surgery; Option 6 eliminates the metric dependency. Gate-5 § 5 warning is now empirically validated. Option 6 is the correct architectural path.

2. **Option 2 respects Discipline #18 sequencing.** Firing legolas Mode A consultation now (per § 5.2 determination that baseline signal criterion is MET) means Cycle 15 dispatch authoring can fire immediately at Cycle 14 tag rather than waiting for Cycle 15 entry to trigger consultation. The Option 2 composite with concurrent consultation produces the tightest path to architectural close (~3-4d: 0.1d C14 amendment + 0.5d consultation + 2.75-3.25d C15 Option 6).

3. **Option 3 is not the right Cycle 14 response post-empirical.** The 79× gap requires SC-6b values to be re-authored at ~200-300× the current substrate values. This is a substrate-scale redesign, not a calibration sweep. It inherits the two-path metric divergence problem even if executed correctly. Discipline #39: resolves the calibration debt but not the architectural metric debt. Option 6 resolves both in one move.

4. **D13 P1-P9 quality debt is accepted as time-bounded.** The primary downside of Option 2's Cycle 14 administrative close is that D13 parallel seasons fire at 3/18 emit. This is acknowledged in full — physical-archetype kit content will be near-absent in Cycle 14 parallel output. The debt is time-bounded by Cycle 15 Option 6 implementation. If Matt judges the D13 quality cost unacceptable, Option 6 promotion to Cycle 14 scope is the alternative (see § 8 Decision 1 alt).

5. **FALLBACK as canonical marker is now the correct framing.** The § 3.11 retraction loop does not close via rebase; it closes via Option 3 or Option 6. Under Option 2, FALLBACK closes at Cycle 15 when Option 6 metric replacement makes the band-based gate moot. This is a clean architectural narrative: FALLBACK documented the divergence; Option 6 eliminates the metric that made the divergence visible as a gate problem.

---

## § 8 — Open Questions for Matt Pattern-B Ratification

### Decision 1 — Ratify Option 2 (Administrative Cycle 14 Close + Cycle 15 Option 6)?

**Context:** Post-rebase telemetry confirms 3/18 emit (same as pre-rebase). Boss HP rebase accomplished the ANCHOR INTENTS scaffold closure but cannot span the 79× two-path DPS divergence. Option 2 amends D9 close criterion to accept Cycle 14 v1 as Track 1 infrastructure delivery tag at 3/18 emit; routes architectural resolution to Cycle 15 Option 6 per existing D2 ratification.

**If yes:** KR fires close-criterion amendment dispatch (~0.1d); jack-ryan updates § 3.11 framing and files decisions-log case 8 canonical scaffold resolution entry; KR queues legolas Mode A consultation dispatch concurrent with Cycle 14 close activities; Cycle 14 v1 tag at infrastructure delivery level; Cycle 15 opens with Option 6 dispatch pre-authorized.

**If no (prefer Option 6 promoted to Cycle 14 scope):** see Decision 1 alt below.

### Decision 1 Alt — Option 6 Promoted to Cycle 14 (Fire Legolas Consultation + Option 6 as Cycle 14 Close Path)?

**Context:** If Matt judges the D13 P1-P9 quality debt of Option 2 (3/18 emit across parallel seasons) unacceptable, Option 6 can be promoted to Cycle 14 scope. Timeline ~3.5-4.5d from legolas consultation fire. The Discipline #18 baseline criterion is now met (§ 5.2), so consultation CAN fire immediately. Option 6 implementation gates on consultation output (locked metric definition) before gamora dispatch fires.

**If yes:** KR fires legolas Mode A consultation dispatch immediately; jack-ryan authors Option 6 canonical metric definition post-consultation; gamora Option 6 implementation dispatch fires on canonical metric landing; Cycle 14 v1 close at Option 6 implementation + ≥12/18 emit under new metric. D13 P1-P9 fires AFTER Option 6 close (higher quality baseline). Timeline ~3.5-4.5d vs Option 2's ~3-4d total.

**Delta between Option 2 and Option 1 alt is ~0.5-1d** in total wall-clock time with comparable discipline compliance. The key trade-off: Option 2 closes Cycle 14 immediately (0.1d) and fires Option 6 in Cycle 15; Option 1 alt delays Cycle 14 close by ~3.5-4.5d but D13 fires at higher quality.

### Decision 2 — Legolas Mode A Consultation Timing Confirmation

**Context:** Jack-ryan determination (§ 5.2) is that post-rebase Track 1 telemetry constitutes the Discipline #18 baseline empirical signal. Consultation CAN fire during Cycle 14 rather than waiting for Cycle 15 entry. Matt D2 pre-flight pre-authorized consultation at Cycle 15 entry. Gate-6 is proposing to advance that pre-authorization to Cycle 14 close wave.

**Specific question for Matt:** confirm that legolas Mode A consultation fires during Cycle 14 close wave (concurrent with D7 close-criterion amendment or Option 6 Cycle 14 dispatch, depending on Decision 1 outcome). Or: retain Cycle 15 entry as the consultation trigger per D2 pre-flight as written.

### Decision 3 — § 3.11 Framing Amendment Authorization

**Context:** Jack-ryan proposes to update Phase 7 doc § 3.11 retraction completion criterion to reflect "FALLBACK-as-canonical-marker-of-two-path-divergence" rather than "FALLBACK-as-transient-artifact-awaiting-rebase." The amendment replaces the "FALLBACK notation absent" completion criterion with "FALLBACK retraction tied to Option 3 or Option 6 closing conditions."

This is a within-seam canonical doc amendment under jack-ryan seam authority (ADR-002: documentation-only changes are jack-ryan-approvable). However, because it modifies a LOAD-BEARING math note with Matt-ratified content, surfacing here for confirmation before executing.

**If authorized:** jack-ryan amends Phase 7 doc § 3.11 Step 4 per § 6.3 proposal above and commits per CLAUDE.md addendum auto-commit authority.

---

## What I Found

Boss HP rebase (`gamora/v2.1-boss-hp-rebase-1`, engine `d83049a`) executed correctly and closed the `endgame_mob_stat_profile.py` ANCHOR INTENTS scaffold as designed. The rebase produced no change in season emit (3/18 post-rebase = 3/18 pre-rebase) because the boss HP midpoint moved by only +1,000 HP (+0.4%) — insufficient to change which kits produce boss KPM signal. The DPS sweep (math note § 11.3) confirmed the empirical 79× gap: STR/DEX physical DPS ≈ 3,750 HP/s vs INT/WIS magical DPS ≈ 297,000 HP/s. No single boss HP value spans 79×. Gate-5 § 5 warning is empirically validated. The correct Cycle 15 path is Option 6 (damage/HP% metric replacement), which resolves the two-path divergence at metric layer. Option 3 (SC-6b surgery at 79× scale) is feasible but inherits the metric architecture problem. Option 2 (administrative Cycle 14 close + Cycle 15 Option 6) is the recommended immediate path.

## Rationale

- **Discipline #11** (empirical inspection over assumption): 79× gap is empirical ground truth; it eliminates the "calibration shortfall addressable by adjustment" interpretation. Post-empirical analysis supersedes pre-empirical option ranking.
- **Discipline #18** (methodology-before-execution): post-rebase Track 1 telemetry satisfies the Discipline #18 baseline signal criterion enumerated in Phase 7 doc § 3.10. Legolas Mode A consultation can fire in Cycle 14 per this determination.
- **Discipline #39/40** (scaffold lifecycle): boss HP ANCHOR INTENTS scaffold is closed. STR/DEX FALLBACK bands are NOT a Discipline #39 violation in their current state — they are canonical markers of architectural structure awaiting Option 6 metric replacement (a named, dated, Matt-ratified resolution path). They become Discipline #39 violations only if Option 6 slips without a replacement retirement gate.
- **Discipline #40 case (c)**: § 3.11 retraction completion criterion requires amendment per empirical finding. The "FALLBACK notation absent" criterion cannot be met by any rebase; it is now tied to Option 6 or Option 3 execution.
- **Discipline #42** (framing consistency): Gate-5 deeper framing (population-wide two-path divergence) is now empirically quantified. Gate-6 options analysis is consistent with that framing — Option 6 is the architectural response to the framing; Options 3 and 5 are partial responses; Option 6 is the complete one.

## Action

- [ ] **Matt:** Decision 1 — ratify Option 2 (administrative Cycle 14 close + Cycle 15 Option 6); OR Decision 1 alt — promote Option 6 to Cycle 14 scope for higher D13 quality
- [ ] **Matt:** Decision 2 — confirm legolas Mode A consultation timing (Cycle 14 concurrent per jack-ryan determination, or retain Cycle 15 entry per D2 pre-flight)
- [ ] **Matt:** Decision 3 — authorize § 3.11 framing amendment (jack-ryan seam discretion per ADR-002; surfaced for LOAD-BEARING content confirmation)
- [ ] **KR (post-Decision 1):** fire D7 close-criterion amendment dispatch (Option 2) OR legolas Mode A consultation dispatch (Decision 1 alt); author Cycle 14 v1 tag semantics per Matt ratification
- [ ] **jack-ryan (post-Decision 3 auth):** amend Phase 7 doc § 3.11 Step 4 per § 6.3 framing proposal; file decisions-log case 8 canonical scaffold resolution entry
- [ ] **legolas (post-Decision 2 timing confirmation):** Mode A methodology consultation on Option 6 `damage_fraction_per_fight` metric formulation per Phase 7 doc § 3.13 pre-flight questions

## References

- `agentic_orchestration/dispatches/2026-05-28-jack-ryan-gate-6-case-8-empirical-re-disposition.md` — dispatch authority
- `agentic_orchestration/cycle-14-wave-5-season-001/option-f-track-1-post-rebase-telemetry.json` — empirical 79× gap anchor (str_physical/dex_physical: boss_kpm_observations=[]; post-rebase; `gamora/v2.1-boss-hp-rebase-1`)
- `reincarnated-engine/src/reincarnated/simulation/math/boss-hp-rebase-case-8-resolution-2026-05-28.md` § 11.3 — DPS sweep: STR/DEX ≈ 3,750 HP/s; gap 79×
- `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` § v1.39 — cross-seam rebase record; FALLBACK RETAINED; "no star-lord action required"
- `reincarnated-engine/design/math/phase-7-2-layer-joint-gate-thresholds-2026-05-27.md` §§ 3.9, 3.11, 3.13 — LOAD-BEARING canonical (FALLBACK notation; retraction loop; Option 6 forward-link)
- `agentic_orchestration/qa/pending/2026-05-28-8th-scaffold-drift-boss-kpm-damage-gap-gate-5-disposition.md` — Gate-5 prior-art; six ranked options; § 5 recommendation (empirically validated at Gate-6)
- `agentic_orchestration/cycle-14-hive-mind-state.md` § "CASE 8 EMPIRICAL ESCALATION 2026-05-28" — KR empirical escalation record + § 3.11 framing amendment note
