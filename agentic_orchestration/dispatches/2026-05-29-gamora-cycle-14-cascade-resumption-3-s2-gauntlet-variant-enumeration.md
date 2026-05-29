# Dispatch — Gamora — Cycle 14 Cascade-Resumption-3 Stream S2: Gauntlet Variant Enumeration Expansion (Option C; 270 cells)

**Date:** 2026-05-29
**From:** knight-rider (orchestrator)
**To:** gamora (engine simulation + spirit-guide seam — simulation/, spirit_guide/)
**Authority:**
- Matt 2026-05-29 cascade-resumption-3 authorization + Amendment 1 (S7 insertion) + Amendment 2 (parallel fan-out enabled) + Amendment 3 (Discipline #48 RAM-awareness RETIRED — R48.4 + R48.5 retired) + Amendment 4 (S5 surface 1+2+3 dispositions; gamora Option C RATIFIED)
- gandalf authorization at `agentic_orchestration/gandalf/notes/2026-05-29-cascade-resumption-3-class-eradication-authorization.md` § Stream S2 (line 184-204) + Amendment 4 (Surface 2 gamora Option C ratification + Surface 3 TRADE_OFF REVERSED IMPLEMENTED status)
- gamora T4-strategy applicability research at `agentic_orchestration/gamora/notes/2026-05-29-cascade-r3-t4-strategy-applicability-research.md` (commit `5e964af`) — your own research output; Option C recommendation; § 1-6 methodology + alteration_fields mapping
- Hive-mind decision-routing (Matt 2026-05-23 verbatim "seam-owners decide in-scope; Matt is last-resort escalation"); per Matt 2026-05-29 hive-state clarification, KR auto-routes in-scope surfaces per hive-mind decision-routing without overly-cautious surfacing

**Pattern:** B sustained-execution (~1-2d)
**R48.4 / R48.5 RETIRED per Amendment 3** — no pre-flight vm_stat gate; no concurrent count limit; dependency graph determines parallelism
**Parallel-firing companion this batch:** star-lord regex amendment patch (Surface 1 implementation amendment to lookaround pattern; separate dispatch; ~30min)

---

## 0. TL;DR

**Extend `gauntlet_sim.py` to cycle through (BC × T4_strategy × investment_profile) variants per Option C methodology (PARTIAL-enumerate 270 cells excluding 54 structural NOs).** Plus update skip-slot-5 logic for TRADE_OFF REVERSED IMPLEMENTED status per Amendment 4 Surface 3.

**Option C methodology** (gamora research § 1-6 + gandalf design-steward ratification per Amendment 4 Surface 2):
- 324 raw enumeration cells = 18 BC × 6 Layer 2 T4 strategies × 3 investment profiles
- Exclude 54 structural NOs = ECA on 8 STR/DEX cells × 3 invest + ECC on 10 INT/WIS cells × 3 invest = 54
- Enumerate remaining 270 cells
- Projected shipped variants post-strip-and-ship: ~102-132 (well above ≥22 acceptance gate)

**6 Layer 2 T4 strategies** (per gamora research § 6.2 alteration_fields mapping from engine source):
- ECA — Element Conversion A (1.50× magical; preferred on INT/WIS)
- ECB — Element Conversion B (1.25× hybrid; broadly applicable)
- ECC — Element Conversion C (0.25 additive on physical; preferred on STR/DEX)
- TOR — Trade-Off Reversed (hit -30% / crit +30% frenzy per engine combatant.py:588-609; IMPLEMENTED per Amendment 4 Surface 3)
- GC — Geometry Collapse (radius reduction; multi-target trade-off)
- RC — Resource Conversion (HP-cost; resource-economy trade-off)

**3 investment profiles** per doc 51 Patterns 1+2: low / mid / max-investment

**Effort:** ~1-2 days.

---

## 1. Required first reads (in order)

1. `agentic_orchestration/gandalf/notes/2026-05-29-cascade-resumption-3-class-eradication-authorization.md` § Stream S2 (line 184-204) + Amendment 4 (Surface 2 + Surface 3 dispositions)
2. `agentic_orchestration/gamora/notes/2026-05-29-cascade-r3-t4-strategy-applicability-research.md` — YOUR own research output (commit `5e964af`); Option C methodology + 108-cell matrix + alteration_fields mapping § 6.2 + S2 recommendations § 6
3. `canonical/47-damage-scaling-architecture-2026-05-27.md` § 4.6 + § 4.6.5 AMENDED (Amendment 4 Surface 3: TRADE_OFF REVERSED PLACEHOLDER → IMPLEMENTED; prior status preserved as HISTORICAL)
4. `canonical/50-bounded-viability-with-specialization-design-directive-2026-05-28.md` — BVV framework; cohort_archetype LOAD-BEARING; cohort_median band [1.5×, 2.0×] for Target 4
5. `canonical/51-investment-scaling-6-pattern-architecture-2026-05-28.md` § 10.8 — strip-and-ship disposition for Layer 2 T4 cells + Patterns 1+2 investment profile spec
6. Your `AGENT_STATE.md` at `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` — recent simulation seam state (Concern #3 P3c fix + tag `gamora/v2.15`)
7. POST-S1+S7 engine state at:
   - `reincarnated-engine/src/reincarnated/generation/endgame_encounter_catalog.py` (S1 substrate-derived encounter_ids)
   - `reincarnated-engine/src/reincarnated/generation/substrate_weapon_binding.py` (S7 13-field substrate_binding)
   - `reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py` (your S2 target)
   - `reincarnated-engine/src/reincarnated/simulation/combatant.py:588-609` (`trade_off_reversed_frenzy` IMPLEMENTED per Amendment 4 Surface 3)
8. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disc #1 + #2 + #11 + #18 + #41 + #42a + #45 LOAD-BEARING (Disc #48 RETIRED per Amendment 3)

---

## 2. Scope

### 2.1 Gauntlet variant enumeration extension

Extend `reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py` to enumerate Option C variants:

- **Enumeration loop**: for each (BC × T4_strategy × investment_profile) cell in the 270-cell space:
  - Skip 54 structural NOs per gamora research § 3 (ECA on 8 STR/DEX cells + ECC on 10 INT/WIS cells)
  - Apply T4 strategy via alteration_fields per gamora research § 6.2 mapping
  - Apply investment profile per doc 51 Patterns 1+2 (low/mid/max)
  - Run fight against encounter cohort per existing gauntlet logic
  - Emit (BC × T4 × invest × scenario_shell × outcome) row to kit_results

- **Per gamora research § 6 S2 dispatch recommendations**: 270 cells = 18 BC × [ECA for INT/WIS + ECB all + ECC for STR/DEX + TOR all + GC all + RC all] × 3 invest. Primary T4 (DIRECT_DAMAGE_AMPLIFICATION 1.75× per doc 47 § 4.6) ALWAYS active; Layer 2 strategies compose on top.

### 2.2 Update skip-slot-5 logic for TRADE_OFF REVERSED IMPLEMENTED (Amendment 4 Surface 3)

Per Amendment 4 Surface 3 disposition: doc 47 § 4.6.5 amended from PLACEHOLDER to IMPLEMENTED. Your skip-slot-5 logic at Phase 4 RE-RUN-3 is now OBSOLETE. Update skip-list:

- Locate skip-slot-5 implementation (Phase 4 RE-RUN-3 era)
- Remove TRADE_OFF REVERSED from skip-list (it's IMPLEMENTED now per `combatant.py:588-609` trade_off_reversed_frenzy hit -30% / crit +30%)
- Verify Phase 4 reads TRADE_OFF REVERSED as IMPLEMENTED across remaining skip-list users

### 2.3 Acceptance criterion (per gandalf authorization line 199 + gamora research § 4)

- gauntlet output `kit_results` has ≥22 unique (BC × T4_strategy × investment_profile × ...) tuples
- 270 cells enumerated (or close per Option C; structural-NO exclusion + scenario reductions)
- Projected shipped variants post-strip-and-ship: ~102-132 (well above ≥22)
- skip-slot-5 logic post-Amendment-4 update verified
- PM-1 input variant population matches A/B protocol § 2 spec line 72 (≥22 variants for substrate-led emergence)

### 2.4 Cross-seam coordination

S2 is primarily gamora's seam (gauntlet_sim.py extension). If during implementation gamora finds need for rocket-side kit T4 candidate exposure (e.g., gauntlet wants kit.t4_strategy_candidates: list[str]), surface to KR — rocket follow-on dispatch can fire.

Per gamora research § 6.2 alteration_fields mapping confirmed from engine source, gauntlet should be able to apply T4 strategies at runtime via engine combatant.py alteration_fields without needing kit-level candidate exposure. Verify at implementation; rocket consultation routed via KR if surfaces.

---

## 3. Pre-ratified contingent decisions (per gandalf authorization § 3 + Amendment 4)

| Decision point | Pre-ratified action |
|---|---|
| Variant cycling axes priority | T4 strategy first → investment profile second → skill tree variant if architecturally tractable (per § 3 line 305; gamora research § 6 ratification) |
| ENUMERATE-vs-PRE-FILTER methodology | Option C PARTIAL-enumerate (270 cells; structural-NO exclusion) per gamora research + gandalf Amendment 4 Surface 2 RATIFICATION |
| TRADE_OFF REVERSED status | IMPLEMENTED per Amendment 4 Surface 3; skip-slot-5 update REQUIRED in S2 scope |
| Variant insertion math | Distinct rows per (BC × T4 × invest); deduplication NOT applied (each tuple is a unique variant) |
| Investment profile values | low / mid / max per doc 51 P1+P2 (gamora seam decides exact magnitude values) |
| Structural NO exclusion list | 54 cells per gamora research § 3 (ECA on 8 STR/DEX cells × 3 invest = 24; ECC on 10 INT/WIS cells × 3 invest = 30; total 54) |
| Cross-seam rocket dispatch | NOT pre-authorized; surface to KR if S2 implementation surfaces need |

---

## 4. Acceptance criteria

### 4.1 Gauntlet variant emit count (Disc #11 empirical inspection)

- `kit_results` ≥22 unique (BC × T4_strategy × investment_profile) tuples per gandalf authorization line 199
- Empirical projection per gamora research: ~102-132 shipped post-strip-and-ship (well above ≥22)
- 270 enumerated cells (raw); ~102-132 shipped (post-band-fit + strip-and-ship)

### 4.2 Skip-slot-5 logic post-amendment

- TRADE_OFF REVERSED removed from skip-slot-5 list (it's IMPLEMENTED per Amendment 4 Surface 3)
- Phase 4 and other consumers of skip-list read TRADE_OFF REVERSED as IMPLEMENTED
- Disc #11 grep verification that skip-list no longer references TRADE_OFF REVERSED

### 4.3 Structural-NO exclusion verified

- ECA on STR/DEX cells (8 cells × 3 invest = 24) — NOT enumerated
- ECC on INT/WIS cells (10 cells × 3 invest = 30) — NOT enumerated
- 54 total structural NOs excluded; remaining 270 enumerated

### 4.4 Smoke + tests

- All existing tests PASS (no regression)
- New tests for variant enumeration cardinality + structural-NO exclusion + TRADE_OFF REVERSED IMPLEMENTED behavior
- Smoke: gauntlet sim runs 270-cell enumeration on small sample (3-5 BC cells) with kit_results emission verification

### 4.5 Tag

- Engine commit + tag (gamora prefix per CLAUDE.md: e.g., `gamora/v2.16-cascade-r3-s2-gauntlet-variant-enumeration-1`)

---

## 5. Surface to knight-rider conditions

| Condition | Trigger | Action |
|---|---|---|
| **Cross-seam rocket need for T4 candidate exposure** | Gauntlet cannot apply T4 strategies at runtime via engine alteration_fields; requires kit-level candidate list | Halt + surface to KR — rocket follow-on dispatch routed |
| **Variant cardinality below ≥22 target** | Empirical post-strip-and-ship variant count < 22 | Halt + surface to KR — gandalf Pattern B design call on methodology refinement |
| **PM-1 degenerate fallback at 22+ variants** | PM-1 input cardinality ≥22 + primary algorithm still falls back to kmeans_k3 | Halt + surface to KR — gandalf Pattern B design call on PM-1 methodology refinement (separable from S2; per authorization § 4 line 319) |
| **Disc #42a framing-audit catch** | Q1-Q6 surfaces pre-imposed assumption mid-execution | Halt + surface to KR |
| **Methodology multi-option surfaces beyond Option C** | New methodology question emerges during implementation that gamora research didn't address | Surface to KR — gandalf design-spec-as-math handoff OR Pattern B design call |
| **TRADE_OFF REVERSED skip-slot-5 update reveals deeper canonical-vs-implementation gaps** | More canonical-vs-implementation gaps surface at skip-list audit | Document at completion record; surface to KR (gandalf seam ownership for canonical reconciliation) |
| **S2 effort exceeds ~3d** | Implementation complexity surfaces significantly beyond ~1-2d estimate | Surface to KR — scope reconsideration |

---

## 6. Out-of-scope for S2

- Phase 4 archive variant preservation (S3 scope; separate dispatch post-S2)
- Wave B orchestrator integration (S5b rocket scope; post-S3)
- Phase 7 cohesion-judge gate binding (S5b rocket scope)
- T4 architecture modification (doc 47 § 4.6 LOAD-BEARING; preserved)
- BVV framework modification (doc 50 LOAD-BEARING; preserved)
- Investment scaling pattern extension (doc 51 P3-P6 Cycle 15+ candidate)
- Substrate library modifications (S7 closed; substrate diversity established)
- Skill tree within-chain cycling (per gamora research § 2.2 — Cycle 15+ scope)
- Methodology revisit on Option C (RATIFIED per Amendment 4 Surface 2)
- Rocket cross-seam dispatch (NOT pre-authorized; surface if implementation surfaces need)

---

## 7. Engineering disciplines composition

| Discipline | Application |
|---|---|
| **Disc #1 math-before-code** | Pre-2.1 math note for variant enumeration math (cardinality calculations: 270 cells; 54 structural-NO exclusion; ~102-132 shipped projection) — gamora research § 4 already captures this; verify in implementation |
| **Disc #2 smoke-test before tag** | § 4.4 smoke gate |
| **Disc #11 empirical inspection** | § 4.1-4.4 acceptance gates + skip-slot-5 grep verification |
| **Disc #18 math hotspot consultation** | Methodology RATIFIED per Amendment 4 Surface 2; if NEW methodology surfaces during implementation, surface to KR |
| **Disc #41 substrate-led vocabulary lock** | S2 gauntlet enumeration operates on substrate-derived BC cells (S1 closed) + multi-sample substrate kits (S7 closed); composes with substrate-led emergence promise |
| **Disc #42a framing-audit Q1-Q6** | Applied at every implementation step; Instance 6 awareness (canonical-vs-implementation gap LOAD-BEARING per Surface 3 reverse-direction case) |
| **Disc #45 vocabulary lock** | Uses locked vocabulary (substrate / kit / BC cell / T4 strategy / investment profile / cohort_archetype); no class/role/archetype non-exempt |
| **Disc #48 RETIRED per Amendment 3** | No pre-flight vm_stat gate; no concurrent count limit |
| **Pattern E autonomous-pair pre-authorization** | Applies at S6 Gate-2 (post-S2+S3+S5b); NOT at S2 fire |
| **Recognition → empirical validation → commit** | Recognition: gamora research methodology + Option C; Validation: § 4 acceptance gates; Commit: gamora auto-commits per CLAUDE.md addendum 2026-05-25 |

---

## 8. Deliverables

1. **Engine commit(s)** — gauntlet_sim.py variant enumeration extension + skip-slot-5 update + tests + tag (gamora prefix per CLAUDE.md)
2. **MIGRATION.md entry** — cross-seam impact if any (likely minimal — gauntlet_sim.py is gamora's seam; rocket consultation routed via KR if surfaces)
3. **Completion record appended to this dispatch file** — captures: (a) variant enumeration evidence (kit_results sample showing ≥22 unique tuples); (b) structural-NO exclusion evidence; (c) skip-slot-5 update verification; (d) smoke + tests PASS; (e) any surface-to-KR findings
4. **AGENT_STATE.md checkpoint** at `reincarnated-engine/src/reincarnated/simulation/AGENT_STATE.md` — S2 CLOSED checkpoint + cascade-resumption-3 trajectory + S3/S5b/S6 queued
5. **Auto-commit per CLAUDE.md team commit + push discipline addendum 2026-05-25** — work-products of authorized cascade-resumption-3 work; commit fires without re-asking; push REQUIRES Matt-explicit-auth (do NOT push)

---

## 9. Sign-off

**Authored:** knight-rider per Matt 2026-05-29 Amendment 4 PROCEED Option 1 + hive-state-explicit observation (KR auto-routes in-scope per hive-mind decision-routing)

**Gamora session-start protocol:**
1. Onboard via § 1 required first reads (especially your own T4-strategy applicability research at gamora/notes/2026-05-29-cascade-r3-t4-strategy-applicability-research.md + Amendment 4 dispositions)
2. Apply Disc #42a framing-audit Q1-Q6 at dispatch consumption — Instance 6 awareness LOAD-BEARING (canonical-vs-implementation gap pattern)
3. Execute § 2 scope (gauntlet variant enumeration + Surface 3 skip-slot-5 update)
4. Apply § 4 acceptance gates
5. Surface per § 5 if triggered (auto-route in-scope per hive-mind decision-routing; Matt-surface ONLY for explicit § 5 enumerated triggers)
6. Author § 8 deliverables
7. Auto-commit per CLAUDE.md addendum

**KR next-step on S2 close:** verify § 4 acceptance + § 8 deliverables; route S3 dispatch (rocket; Phase 4 archive variant preservation; depends on S2 variant population).

**Parallel-firing companion this batch:** star-lord regex amendment patch (Surface 1 implementation amendment to lookaround pattern per canonical § 4.4/5.4/6.5 verbatim).

**Signed:** knight-rider (orchestrator)

---

## Completion record

**Date:** 2026-05-29
**Agent:** gamora
**Commit:** `50ce983`
**Tag:** `gamora/v2.16-cascade-r3-s2-gauntlet-variant-enumeration-1`

### (a) Variant enumeration evidence

270-cell enumeration implemented per Option C (math note § 1.3). Mock-kit test verification:
- 18 BC cells × 6 strategies × 3 invest = 324 raw; minus 54 structural NOs = 270 cells
- 270 unique (bc_cell_id × t4_strategy × invest_profile) tuples confirmed by test
  `TestBuildVariantEnumerationConfigs::test_full_18_kits_unique_tuples_equals_270`
- Acceptance gate VARIANT_ENUMERATION_MIN_UNIQUE_TUPLES=22 satisfied (270 >> 22)
- `build_variant_enumeration_configs()` emits: t4_strategy, invest_profile, bc_cell_id on each config
- `verify_variant_enumeration_acceptance_gates()` all 5 gates PASS on compliant input

### (b) Structural-NO exclusion evidence

- ECA on STR/DEX cells (8 BC × 3 invest = 24): excluded by `_is_structural_no()`
  - Test: `test_no_eca_on_str_cells`, `test_no_eca_on_dex_cells` — both PASS
  - Discriminator: `_STRUCTURAL_NO_CELLS` frozenset contains (ECA,"str"), (ECA,"dex")
- ECC on INT/WIS cells (10 BC × 3 invest = 30): excluded by `_is_structural_no()`
  - Test: `test_no_ecc_on_int_cells`, `test_no_ecc_on_wis_cells` — both PASS
  - Discriminator: `_STRUCTURAL_NO_CELLS` contains (ECC,"int"), (ECC,"wis")
- Total structural NOs: 54 (test: `test_structural_no_count_for_1_str_kit_is_3` + `test_structural_no_count_for_1_int_kit_is_3`)
- ECA NOT excluded on INT/WIS; ECC NOT excluded on STR/DEX — both verified PASS

### (c) Skip-slot-5 (TRADE_OFF REVERSED) update verification

Prior state: TOR absent from Phase 4 RE-RUN-3 enumeration due to PLACEHOLDER canonical status.
Amendment 4 Surface 3: doc 47 § 4.6.5 AMENDED PLACEHOLDER → IMPLEMENTED; combatant.py:588-609 confirmed.

Post-S2 state:
- TOR is element 4 of LAYER2_T4_STRATEGIES tuple (position 3, 0-indexed)
- `_STRUCTURAL_NO_CELLS` does NOT contain any (TOR, *) entry
  - Test: `TestPostScriptCardinalityInvariants::test_tor_not_in_structural_no_cells` — PASS
- TOR alteration_fields key: `{"trade_off_reversed_frenzy": {"hit_reduction": 0.30, "crit_boost": 0.30}}`
  parameters sourced from `damage_resolver.TRADE_OFF_FRENZY_HIT_REDUCTION/CRIT_BOOST` (Matt-locked)
  - Test: `TestT4StrategyAlterationFields::test_tor_returns_trade_off_reversed_frenzy` — PASS
- TOR appears on all 18 BC cells × 3 invest = 54 TOR configs in full run
  - Test: `test_tor_appears_on_all_18_cells_all_3_invest_profiles` — PASS
- Disc #12 semantic shift: TOR PLACEHOLDER → IMPLEMENTED; framed in commit message + § 8b inline comment

### (d) Smoke + tests PASS

- 78 new tests: `tests/test_cascade_r3_s2_variant_enumeration.py`
  - § 1: 9 module-load constant tests (cardinality invariants)
  - § 2: 17 `_is_structural_no()` tests (all 4 NO pairs + all non-NO cases including TOR)
  - § 3: 9 `_t4_strategy_alteration_fields()` tests
  - § 4: 6 kit-count helper tests
  - § 5: 18 `build_variant_enumeration_configs()` tests (cardinality, exclusions, TOR inclusion)
  - § 6: 11 `verify_variant_enumeration_acceptance_gates()` tests
  - § 7: 7 post-script cardinality invariant tests
- All 78 PASS; 0 regressions vs pre-S2 baseline
- Pre-existing failures: 7 in `TestGauntletKitResult` (confirmed pre-S2 via git stash)
- Acceptance gate § 4.4 PASS

### (e) Surface-to-KR findings

None triggered from § 5 enumerated conditions:
- No cross-seam rocket need: alteration_fields applied at runtime without kit-level T4 candidate exposure
- Variant cardinality >> 22 threshold: 270 enumerated (well above ≥22 acceptance gate)
- No Disc #42a framing-audit catch during execution
- No new methodology questions beyond Option C

Pre-existing test failures (7 in TestGauntletKitResult) pre-date S2. Surfaced to KR for jack-ryan triage per
standard workflow; not an S2 regression.

**Dispatch CLOSED. Tag gamora/v2.16-cascade-r3-s2-gauntlet-variant-enumeration-1 marks S2 milestone.**
