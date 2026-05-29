# Cascade-Resumption-4 — Path X (Phase 4 Archive → Phase 5 PM-1) Authorization

> **STATUS:** CURRENT — Cycle 14 cascade-resumption-4 master authorization. Authored by gandalf 2026-05-29 evening late post-cascade-resumption-3-Instance-6-#5-resolution. Routes to KR for rocket dispatch.
>
> **Composes with:** cascade-resumption-3 (CLOSED at A2-1 RE-FIRE-3 + Amendment 6 + Amendment 7 + Amendment 7a + Amendment 8); jack-ryan Gate-2 Instance 6 #5 PASS-with-INFO; rocket Instance 6 #5 investigation (config_to_kit collision finding). Cascade-resumption-4 is a NARROW wire-up change + Phase 5+ re-fire only — no Phase 2-4 re-fire required (Phase 4 archive intact from A2-1 RE-FIRE-3 production run).

**Date:** 2026-05-29 evening late
**Author:** gandalf (story-and-design steward)
**Authorized:** Matt 2026-05-29 evening late ("Path X — fire cascade-resumption-4" verbatim + "yes, option (i)" Wave B scope confirmation)
**Composition:** cascade-resumption-4 work program; Cycle 14 v1 close trajectory

---

## 0. TL;DR

Phase 5 PM-1 input is changed from `passing_kits + variant_passing_rows` (Phase 3 _s2 output; 598 members) to Phase 4 Pareto-2 archive output (34 mixed-sample base kits per Amendment 6). Phase 5 LLM re-fire only (no Phase 2-4 re-fire; archive intact). Wave B operates on all 34 archive kits per Matt option (i). Per-season cost ~$0.30; 3-season ~$1.00.

**Headline change:** Phase 5 faction labels + Wave B kit names operate on the Pareto-2 design-selected population. Phase 7 join becomes 100% overlap (every archive kit has both mechanical_pass AND cohesion gate input). Player-facing experience aligns with shipped-kit identity.

---

## 1. Election rationale (Path X over Path B / Y / Z)

Per jack-ryan Disc #42a Q1-Q6 framing audit (commit `eb14ec3`) + gandalf design-fit verdict (Pattern A-deep), the disconnect is **architectural intent, not bug.** Both Phase 4 → Phase 5 AND Phase 3 → Phase 5 architectures are individually valid. The design call resolves which intent holds.

**Path X (Phase 4 archive → Phase 5 PM-1) elected on three principles:**

1. **Designer-writes-substrate principle** (`canonical/story/2026-05-29-designer-writes-substrate-player-names-experience-principle.md`): the substrate players experience IS the substrate. Phase 4 Pareto-2 selection IS the design-selected substrate; Phase 5 LLM curation should operate on it, not on the broader Phase 3 candidate pool that includes mechanical-noise variants.

2. **Variants are loadout flavors, not faction-membership candidates.** S2 variant naming patterns (`_eca_low` / `_tor_low` / `_rc_max` etc.) are `(t4_strategy × investment_tier)` mechanical variations of base kits. They are not player-facing entities for faction emergence. Letting 585 variant rows inform faction signal dilutes substrate emergence.

3. **Phase 7 join coherence.** If Phase 4 archive feeds both Phase 7 mechanical gate AND Phase 5 PM-1, the join is 100% overlap. Faction labels + Wave B names map 1:1 to shipped-worthy kits. Currently (Phase 3 _s2 path) only 6 of 34 archive kits get LLM curation.

**PM-1 sparsity tier verified safe at n=34:** stays in NONE tier (GMM k∈{3,4} BIC-selected; identical algorithm to current behavior). PM-1's tier thresholds (20-40 SPARSITY_TIER_GMM_BIC range) suggest the original design point was Phase-4-archive-scale input, not 598-row variant-inclusive input.

**Cost asymmetry favors Path X:** ~0.5-1d rocket implementation + ~$1.00 LLM re-fire across 3 seasons (<2% of $50 cap) vs Path B (close-as-is + spec amendment) deferring player-facing coherence improvement to Cycle 15+.

---

## 2. Composition with rocket Instance 6 #5 investigation findings

**Rocket finding (Instance 6 #5 investigation, commits `764e732` + `bb9a507`):** `config_to_kit` collision at `season_generation_pipeline.py:1424-1428`:

```python
for enc_idx, kit in enumerate(kits_to_sim):
    kit_configs = _build_legendary_config(kit, enc_idx)
    for cfg in kit_configs:
        all_configs.append(cfg)
        config_to_kit[cfg["legendary_id"]] = kit  # ← OVERWRITE on collision
```

`legendary_id` is BC-cell-keyed (no `_sN` sample suffix). For each BC cell's 3 substrate samples (s0/s1/s2), the dict OVERWRITES — last-written-wins. The last sample is s2 (sequential generation order). This is the underlying mechanism producing `passing_kits` s2-only character.

**Composition with Path X:** Path X CIRCUMVENTS the collision rather than fixing it. Phase 4 archive receives all 54 base kits directly from Phase 2 (before the gauntlet submission step where collision fires); the archive has full mixed-sample distribution (s0=18, s1=9, s2=7) per A2-1 RE-FIRE-3 empirical verification.

**The collision becomes Cycle 15+ canonical-write target:** if downstream needs `passing_kits` for ANY purpose with full sample fidelity (variant emission expansion; per-sample telemetry; Cycle 15+ Bound 3 / Bound 6 / per-skill-emitter work), the collision fix is required. For Cycle 14 v1 + Path X scope, Phase 4 archive routing makes the collision non-load-bearing for player-facing output.

**Cumulative Disc #42a Instance 6 pattern at SIX surfaces** (Wave B phantom + Variant Pareto-dominance + Sub-fix 3 namespace-only + Amendment 7 hybrid metadata-only + Phase 4→Phase 5 disjoint + config_to_kit collision). Wave-close canonical-write priority elevated.

---

## 3. Composition with jack-ryan Instance 6 #5 framing audit

**Jack-ryan findings (commit `eb14ec3`; doc at `agentic_orchestration/qa/pending/2026-05-29-jack-ryan-cascade-r3-instance-6-5-framing-audit-canonical-record.md`):**

- **Disc #42a Q1-Q6 audit:** WARN at Q1/Q2/Q3/Q4/Q6; INFO at Q5. NOT a wave-close BLOCKER.
- **Sub-fix 2 Pareto-2 archive is NOT decorative** in architectural sense (serves A/B comparison + cross-season quality tracking) — only "decorative for THIS RUN's PM-1 clustering" is correct narrow framing.
- **New Disc #42a sub-case proposed:** "Layer-isolation-vs-integration gap" — pipeline stages individually correct; inter-stage data flow source different than architecturally assumed. Distinguished from component-existence (Surface 1) and structural-vs-behavioral (Surfaces 3-4).
- **Disc #42a Q4 amendment recommended** (NOT new Disc #50): when downstream stage `input_cardinality` is orders-of-magnitude different from upstream stage output count, stop and verify data flow source explicitly.

**Composition with Path X:** jack-ryan's PASS-with-INFO disposition supports closing cascade-resumption-3 with current production output intact (not blocked); cascade-resumption-4 fires as a separate refinement work program. Per-season re-fire IS in jack-ryan's recommendation if Matt elects Phase 4 → Phase 5 (which Matt did). The Disc #42a Q4 amendment lands at Cycle 14 wave-close canonical-write (jack-ryan's territory).

---

## 4. Composition with gamora Instance 6 #5 investigation (in-flight)

Gamora dispatch fired by KR per gandalf REDIRECT § 5; investigating Phase 7 join logic + 13/54 mechanical pass rate + sample distribution within `passing_kits`. Findings TBD at time of authoring. Gamora findings will likely surface:

- Why Phase 7 ships 22 of 34 archive kits (mechanical_pass criterion)
- Whether the 13/54 Phase 3 acceptance rate is structurally low OR is a `config_to_kit` collision artifact (related to rocket finding)
- Whether `passing_kits` sample distribution is purely s2 OR mixed

**Composition with Path X:** Path X is independent of gamora findings. Gamora's data informs Cycle 14 wave-close canonical-write attention (mechanical gate calibration; collision fix scope) but does not gate cascade-resumption-4 execution. If gamora surfaces a Phase 7 mechanical gate BLOCKER, surface to gandalf for re-deliberation; otherwise cascade-resumption-4 fires per this authorization.

---

## 5. Scope — narrow wire-up + Phase 5+ re-fire

### 5.1 Code change (rocket implementation)

**File:** `reincarnated-engine/src/reincarnated/simulation/wave5_season_orchestrator.py`
**Lines:** 825-836 (PM-1 input construction)

**Current state (post-A2-1-RE-FIRE-3):**
```python
base_kit_datas = [_build_pm1_kit_data(k, k.character_id) for k in passing_kits]
variant_kit_datas = [_build_pm1_kit_data(vr, vr.character_id) for vr in variant_passing_rows]
surviving_kit_datas = base_kit_datas + variant_kit_datas
```

**Path X target state:**
```python
# Path X: Phase 5 PM-1 input = Phase 4 Pareto-2 archive output
# Cascade-resumption-4 election: Phase 4 archive provides design-selected substrate
# Variants are loadout flavors, not faction-membership candidates (per cascade-resumption-4 § 1.2)
phase4_accepted_kits = _load_phase4_archive_for_pm1(phase4_archive_path)  # or similar
surviving_kit_datas = [
    _build_pm1_kit_data(k, k.character_id) for k in phase4_accepted_kits
]
log.info(
    "[PM-1][Path X] PM-1 input: %d Phase 4 archive kits (mixed-sample Pareto-2 winners)",
    len(surviving_kit_datas),
)
```

**Backward compatibility:** if Phase 4 archive contains 0 kits (degenerate season), retain a fallback path to `passing_kits` with explicit WARN log. Path X target state expects archive ≥ 8 kits (PM-1 KMEANS_K2 floor) for normal operation.

### 5.2 Phase 5 + Phase 7 re-fire (rocket execution)

- Phase 2 + Phase 3 + Phase 4: NO RE-FIRE (intact from A2-1 RE-FIRE-3; archive preserved in `kit_archive.db`)
- Phase 5 PM-1 + Wave A + F-C + Wave B: RE-FIRE on 34 archive kits
- Phase 7 mechanical + cohesion gate: RE-FIRE on Phase 5 output

### 5.3 Wave B scope (Matt option (i) — all 34 archive kits)

- Wave B operates on all 34 Phase 4 archive kits (NOT subset of Phase 7 shipped_worthy)
- Reasoning: cohesion judge needs Wave B names for cluster cohesion evaluation; running Wave B on archive ensures all clustered kits have names; if Phase 7 ships more than current 22 post-Path-X, no Wave B re-fire needed
- Cost: ~34 kits × ~$0.01/name = ~$0.34 per season; ~$1.02 across 3 seasons

### 5.4 Tests (~5-10 new)

- PM-1 input cardinality = Phase 4 archive size (assert n=34 ± archive variance per season)
- Sample distribution in PM-1 input matches Phase 4 archive (s0/s1/s2 mixed)
- Phase 7 cohesion gate cluster_id assignment: 100% of archive kits have cluster_id (vs current ~17.6%)
- Backward compat: Phase 4 → PM-1 wire-up works at n ≥ 8 (KMEANS_K2 floor); WARN + fallback at n < 8

---

## 6. Acceptance criteria

### 6.1 Behavioral verification

| Test | Expected outcome |
|---|---|
| PM-1 input cardinality | 34 (or archive size for the season; ≥ 8 SPARSITY floor) |
| PM-1 sparsity branch | NONE (gmm_bic_sweep) at n=34 |
| GMM cluster count | k=3 or k=4 (BIC-selected) |
| Phase 5 cluster member sample distribution | Mixed s0/s1/s2 matching Phase 4 archive (s0=18, s1=9, s2=7) |
| Phase 5 cluster element distribution | All 8 elements present at primary mono layer (preserving Amendment 7 acceptance) |
| Wave B kit_count | 34 (all archive kits named) |
| Phase 7 cluster_id assignment coverage | 100% of archive kits have cluster_id |

### 6.2 Cost verification

| Stage | Per-season cost target |
|---|---|
| Wave A (faction labels for 3-4 clusters) | ~$0.02 |
| F-C cohesion judge | Included in Wave A or ~$0.01 |
| Wave B (34 kit names) | ~$0.34 |
| **Per-season total** | **~$0.37** |
| **3-season total** | **~$1.10** (<2% of $50 cap) |

### 6.3 Composition preservation

| Existing acceptance | Preserved? |
|---|---|
| Amendment 6 Sub-fix 1 (S7 deepcopy; 54 distinct substrate bindings at Phase 2) | ✅ unchanged |
| Amendment 6 Sub-fix 2 (Pareto-2 lineage partition; 34 archive winners) | ✅ now consumed by Phase 5 |
| Amendment 6 Sub-fix 3 (S8 Bound 4 paired-joint-sampling; namespace-only acceptable) | ✅ unchanged |
| Amendment 7 (E4c element coverage; all 8 elements at primary mono) | ✅ now visible at Phase 5 |
| Amendment 7a (per-chain element wiring; hybrid behavioral at skill emitter) | ✅ unchanged |
| Amendment 8 (Matt-gate retired; $50 cap re-imposed) | ✅ unchanged (Path X stays well under cap) |

---

## 7. Discipline composition

| Discipline | Application |
|---|---|
| **Designer-writes-substrate principle** | Path X aligns Phase 5 LLM curation with design-selected substrate (Pareto-2 archive); the curation layer operates on the substrate the designer wrote |
| **Disc #41 substrate-led discipline** | Substrate variance from Sub-fix 1 (S7) + Sub-fix 2 (lineage partition) NOW reaches player-facing emergence layer |
| **Disc #42a framing-audit (Q1-Q6)** | Jack-ryan Q4 amendment proposed; Layer-isolation-vs-integration gap sub-case documented; Cycle 14 wave-close canonical-write target |
| **Disc #18 math hotspot consultation** | Not load-bearing for Path X (no new math; configuration change only) |
| **Disc #19 background processes** | Rocket dispatch fires sequentially under KR coordination; Phase 5 re-fire is local LLM call (~30sec); no parallel-fan-out resource conflict |
| **Recognition → empirical validation → commit** | Recognition (disjoint population found); empirical validation (jack-ryan + rocket investigations confirmed; sparsity tier verified); commit (Path X authorized via this doc) |

---

## 8. Cycle 14 wave-close canonical-write candidates accumulating

Append to existing wave-close deferred list:

1. **Disc #42a Q4 amendment** — "pipeline cardinality-mismatch verification at downstream input gate" (jack-ryan canonical-write territory)
2. **Disc #42a Layer-isolation-vs-integration gap sub-case** — formal sub-case classification
3. **config_to_kit collision fix scope** — Cycle 15+ if variant fidelity + per-sample telemetry needed
4. **PM-1 input source explicit documentation** — gandalf canonical write recording Path X election + Phase 4-archive-as-PM-1-input architectural intent
5. **Bound 4 spec-language reconciliation** — gandalf canonical write closing the structural-vs-behavioral ambiguity
6. **Cumulative Disc #42a Instance 6 pattern record** — 6 surfaces in one work program; pattern category documentation
7. **Designer-writes-substrate principle Layer 1.5 amendment** (coupling architecture per ARPG research sprint synthesis)
8. **Doc 52 promotion** (experiential archetype dimension; locked vocabulary)
9. **Lineage-as-skill-flavor coupling** (Cycle 15+ design call)
10. **STR pool expansion candidate** (genre-canon STR-fire-warrior etc.)
11. **DEX disposition Cycle 15+ revisit** (Option A vs B vs C re-deliberation)
12. **Hybrid rate empirical calibration** (17.5% midpoint; observe production data)

---

## 9. KR routing instructions

### 9.1 Dispatch sequence

1. **KR confirms cascade-resumption-3 CLOSED** (all Amendments 1-8 + Amendment 7a + Instance 6 #5 investigation findings consolidated)
2. **KR dispatches cascade-resumption-4 to rocket** with reference to this authorization at `agentic_orchestration/gandalf/notes/2026-05-29-cascade-resumption-4-path-x-phase4-feeds-phase5-authorization.md`
3. **Rocket implements** § 5.1 wire-up + § 5.4 tests; ~30-60min code work; auto-commit per CLAUDE.md addendum
4. **Jack-ryan Gate-2 quick review** of cascade-resumption-4 (composition verification; backward compat verification; acceptance criteria § 6)
5. **Rocket fires Phase 5+ re-fire** on season_001 (~50sec; ~$0.37 LLM); auto-commit
6. **KR consolidates** Phase 5 output + Phase 7 verdict + cost actual vs projected; surface to Matt at consolidation
7. **Pattern E pre-authorization fires seasons 002-003** under $50 cap monitoring per Amendment 8

### 9.2 Hive-state routing (Matt 2026-05-23 directive in force)

- KR auto-routes in-scope cascade-resumption-4 work without Matt re-surface
- Matt-surface explicit triggers (UNCHANGED from cascade-resumption-3 Amendment 4 + Amendment 8):
  - $50 soft cap approach OR breach
  - R48 violations (Discipline #49)
  - Gate-2 material-fail (jack-ryan BLOCK)
  - Wave B spec-gap surfaces
  - Third material-fail in any phase
  - Framing-audit catches load-bearing assumption refutation
  - PM-1 cardinality < 8 (SPARSITY floor breach at Path X archive consumption)

### 9.3 Wave B scope explicit lock

Wave B option (i) authorized per Matt verbatim "yes, option (i)" — Wave B operates on all 34 Phase 4 archive kits per season. NOT subset of Phase 7 shipped_worthy. Cost ~$0.34/season; ~$1.02 across 3 seasons.

---

## 10. Sign-off

**Authored:** gandalf (story-and-design steward) per Matt 2026-05-29 evening late "Path X — fire cascade-resumption-4" + "yes, option (i)" verbatim
**Composition:** Cycle 14 v1 close trajectory; cascade-resumption-4 work program

**For KR:** route cascade-resumption-4 to rocket with reference to this authorization; coordinate Phase 5+ re-fire post-rocket Gate-2 PASS; consolidate season_001 output for Matt surface.

**For rocket:** implement § 5.1 wire-up at `wave5_season_orchestrator.py:825-836`; add § 5.4 tests; preserve backward compat per § 5.1 fallback; auto-commit per CLAUDE.md addendum.

**For jack-ryan Gate-2:** verify § 6 acceptance criteria; verify Amendment 6 + 7 + 7a composition preserved; close cumulative Disc #42a Instance 6 pattern record for wave-close attention (six surfaces now documented).

**For Matt:** consolidated season_001 output surfaces post-Phase-5-re-fire; cost actual vs $1.00 projection; Phase 7 ship count actual vs current 22; per-element distribution at primary mono layer; faction labels for 3-4 clusters; Wave B names for 34 kits.
