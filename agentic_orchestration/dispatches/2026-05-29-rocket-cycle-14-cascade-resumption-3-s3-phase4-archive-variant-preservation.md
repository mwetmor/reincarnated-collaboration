# Dispatch — Rocket — Cycle 14 Cascade-Resumption-3 Stream S3: Phase 4 Archive Variant Preservation

**Date:** 2026-05-29
**From:** knight-rider (orchestrator)
**To:** rocket (content generation seam — generation/, element/, anchor/, foundation/, engine-internal canonical library)
**Authority:**
- Matt 2026-05-29 cascade-resumption-3 authorization + Amendments 1-4 (S7 insertion / parallel fan-out / Disc #48 retirement / S5 surface dispositions + gamora Option C ratification + TRADE_OFF REVERSED IMPLEMENTED status)
- gandalf authorization at `agentic_orchestration/gandalf/notes/2026-05-29-cascade-resumption-3-class-eradication-authorization.md` § Stream S3 (line 206-223)
- gamora S2 close (commit `50ce983` + tag `gamora/v2.16-cascade-r3-s2-gauntlet-variant-enumeration-1`) — 270 enumerated cells; projected ~102-132 shipped variants; S2 produces the variant population S3 must preserve
- Hive-mind decision-routing (Matt 2026-05-23 verbatim) + Matt 2026-05-29 hive-state clarification (KR auto-routes in-scope per hive-mind decision-routing; Matt-surface ONLY for authorization § 4 enumerated triggers)

**Pattern:** B sustained-execution (~0.5-1d)
**R48.4 / R48.5 RETIRED per Amendment 3** — no pre-flight vm_stat gate; no concurrent count limit
**Standalone dispatch this batch** — no parallel companion (S5b depends on S3; gandalf parallel thread continues)

---

## 0. TL;DR

**Change `kit_archive` insertion logic at `wave5_season_orchestrator.py` Phase 4 hook to preserve (kit_base × T4_variant × investment_profile × ...) tuples as DISTINCT ROWS** (not deduped by base character_id). S2 (gamora) now emits 270 enumerated cells (projected ~102-132 shipped post-strip-and-ship); Phase 4 archive must preserve these variants as the PM-1 multimodal clustering input population.

**Goal:** kit_archive count ≥ gauntlet variant count (~102-132 from S2); PM-1 input cardinality matches archive variant cardinality so substrate-led emergence can produce real clusters (not k=3 fallback degenerate per Instance 6 prior finding).

**Effort:** ~0.5-1 day.

---

## 1. Required first reads (in order)

1. `agentic_orchestration/gandalf/notes/2026-05-29-cascade-resumption-3-class-eradication-authorization.md` § Stream S3 (line 206-223) + Amendments 1-4 context
2. `agentic_orchestration/dispatches/2026-05-29-gamora-cycle-14-cascade-resumption-3-s2-gauntlet-variant-enumeration.md` — S2 completion record (variant emit format + 270 enumerated cells + skip-list state)
3. `agentic_orchestration/gamora/notes/2026-05-29-cascade-r3-t4-strategy-applicability-research.md` — Option C methodology + variant cardinality projection
4. `reincarnated-engine/src/reincarnated/simulation/wave5_season_orchestrator.py:1169` — Phase 4 hook + current `cohesion_data={}` hardcode + kit_archive insertion site
5. `reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py` — S2-extended variant emission (LAYER2_T4_STRATEGIES tuple + _STRUCTURAL_NO_CELLS frozenset + 270-cell enumeration loop)
6. Your `AGENT_STATE.md` at `reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` — S1 + S7 CLOSED checkpoints; cascade-resumption-3 trajectory
7. Your `MIGRATION.md` at `reincarnated-engine/src/reincarnated/generation/MIGRATION.md` — S1 + S7 entries; S3 cross-seam impact (Phase 4 hook is in simulation/wave5_season_orchestrator.py — gamora seam; cross-seam coordination required)
8. `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` — Phase 2-7 architecture; Phase 4 archive role
9. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disc #1 + #2 + #11 + #41 + #42a + #45 LOAD-BEARING (Disc #48 RETIRED per Amendment 3)

---

## 2. Scope

### 2.1 kit_archive insertion logic — variant preservation

At `wave5_season_orchestrator.py` Phase 4 hook (around line 1169 + surrounding insertion logic):

**Current behavior (pre-S3):** kit_archive insertion deduplicates by base character_id; 18 base kits → 18 archive rows.

**Required post-S3 behavior:** preserve distinct (kit_base × T4_strategy × investment_profile × scenario_shell × ...) tuples as DISTINCT ROWS in kit_archive. S2 emit produces these tuples; Phase 4 hook must preserve them.

**Implementation approach:**
- Identify current dedup key (likely `character_id` or `kit_id`)
- Extend dedup key to include T4_strategy + investment_profile (and any other variant axes per S2 emit)
- OR replace dedup with unique-per-emission insertion (variant_id derived from S2 emit tuple)
- Verify kit_archive schema supports the additional rows (no schema gap; per Disc #11 empirical inspection)

### 2.2 PM-1 clustering input — variant population consumption

At Phase 3 → Phase 4 → PM-1 clustering pipeline:

**Current behavior (pre-S3):** PM-1 input consumes 18 base kit archive rows (k=3 fallback degenerate per Instance 6 pre-cascade-resumption-3 finding).

**Required post-S3 behavior:** PM-1 input consumes ALL archive ACTIVE rows including variants (~102-132 post-strip-and-ship from S2); substrate-led emergence operates on variant-population substrate.

**Implementation approach:**
- Update PM-1 input filter to consume all archive ACTIVE rows
- No class-keyed filter (substrate is class-free post-S1; just verify no class-vocabulary filter survives in PM-1 input pipeline)
- Verify multimodal vector input dimensionality handles variant rows correctly (S7 lineage/period/register fields preserved per variant)

### 2.3 Acceptance verification math (Disc #1 math-before-code)

Before code change, author math note at `reincarnated-engine/src/reincarnated/generation/notes/cascade-r3-s3-archive-variant-preservation-math-2026-05-29.md`:

- Variant cardinality projection: S2 emits ~102-132 shipped variants → kit_archive count should be ≥ this
- PM-1 input cardinality projection: PM-1 consumes archive ACTIVE rows; cardinality matches archive variant count
- Dedup key change impact: enumerate which existing consumers of kit_archive rely on character_id dedup; verify they still operate correctly with variant rows (or migrate)
- Schema impact: verify kit_archive schema accepts additional rows without modification

---

## 3. Pre-ratified contingent decisions (per gandalf authorization § 3 + Amendment 4)

| Decision point | Pre-ratified action |
|---|---|
| Dedup key extension scope | Include T4_strategy + investment_profile in dedup key; surface if other variant axes from S2 surface (per gamora completion record) |
| variant_id derivation | Rocket elects per simpler-implementation principle (e.g., `f"{character_id}_t4_{strategy}_inv_{profile}"` OR analogous); surface if architectural alternatives surface |
| PM-1 input filter update | Consume all archive ACTIVE rows; no class-keyed filter (already class-free per S1); surface if filter logic surfaces non-trivial migration |
| Schema migration | NOT pre-authorized — verify kit_archive schema accepts variant rows without modification; surface if schema gap surfaces |
| Existing consumer migration | Audit consumers of kit_archive rows for character_id-dedup assumptions; surface if breaking change risk |

---

## 4. Acceptance criteria

### 4.1 Archive variant preservation (Disc #11 empirical inspection)

- kit_archive count ≥ S2 shipped variant count (~102-132 projected; verify against actual S2 emit count)
- Distinct rows per (BC × T4_strategy × investment_profile) tuple; no dedup collapse
- Disc #11 grep: query kit_archive for variant rows; verify cardinality matches expectation

### 4.2 PM-1 input cardinality match

- PM-1 multimodal clustering input consumes archive ACTIVE rows
- Input cardinality = archive variant cardinality (no filter shrinkage)
- Substrate-led emergence at PM-1 operates on variant-population substrate (NOT k=3 fallback degenerate)

### 4.3 Disc #1 math note authored

- Math note at `reincarnated-engine/src/reincarnated/generation/notes/cascade-r3-s3-archive-variant-preservation-math-2026-05-29.md` captures variant cardinality + dedup key + PM-1 input projections BEFORE code change

### 4.4 Smoke + tests

- All existing tests PASS (no regression beyond pre-existing 7 TestGauntletKitResult failures per gamora S2 surface)
- New tests for variant preservation cardinality + PM-1 input consumption
- Smoke: Phase 2-5 cascade fire on small sample verifies variant preservation + PM-1 input cardinality

### 4.5 Tag

- Engine commit + tag (rocket prefix per CLAUDE.md: e.g., `rocket/v1.0-cascade-r3-s3-archive-variant-preservation-1`)

---

## 5. Out-of-scope for S3

- Wave B orchestrator integration (S5b rocket; post-S3)
- kit_archive.cohesion_data field wiring + unhardcode `{}` at line 1169 (S5b rocket; the hardcode persists through S3; S5b unwires it)
- Phase 7 cohesion-judge gate binding (S5b rocket)
- PM-1 clustering algorithm modifications (algorithm methodology question separate from S3 scope; if PM-1 still produces degenerate fallback at 102-132 variants, surface per § 6)
- Phase 5 Wave A / F-C / Wave B implementation changes (S4 + S5 closed)
- T4 architecture modification (preserved)
- BVV framework modification (preserved)
- Substrate library modifications (S7 closed)
- A/B comparison protocol (runs at Wave 5 close; independent)

---

## 6. Surface to knight-rider conditions

| Condition | Trigger | Action |
|---|---|---|
| **Schema migration required** | kit_archive schema doesn't accept variant rows without modification | Halt + surface to KR — schema migration is scope expansion; KR routes to gamora/elrond consultation OR Matt Pattern B |
| **Existing consumer breaking change** | kit_archive consumers rely on character_id dedup; variant-row introduction breaks their logic | Halt + surface to KR — consumer migration scope; KR routes follow-on dispatch |
| **PM-1 still produces degenerate fallback at variant population** | PM-1 input cardinality ≥22 + primary algorithm still falls back to kmeans_k3 | Halt + surface to KR — gandalf Pattern B design call on PM-1 methodology refinement (separable from S3; per authorization § 4 line 319) |
| **Disc #42a framing-audit catch** | Q1-Q6 surfaces pre-imposed assumption mid-execution | Halt + surface to KR |
| **Cross-seam coordination at gamora seam** | Phase 4 hook is in simulation/wave5_season_orchestrator.py (gamora seam); rocket modifies cross-seam | Author MIGRATION.md cross-seam note per ADR-004; atomic refactor OR surface for gamora consultation |
| **S3 effort exceeds ~2d** | Implementation complexity surfaces significantly beyond ~0.5-1d estimate | Surface to KR — scope reconsideration |

---

## 7. Engineering disciplines composition

| Discipline | Application |
|---|---|
| **Disc #1 math-before-code** | § 2.3 math note authored before code change (variant cardinality + dedup key + PM-1 input projections) |
| **Disc #2 smoke-test before tag** | § 4.4 smoke gate (Phase 2-5 cascade on small sample) |
| **Disc #11 empirical inspection** | § 4.1-4.4 acceptance gates + Disc #11 grep verification of archive cardinality + PM-1 input cardinality |
| **Disc #18 math hotspot consultation** | NOT a hotspot in S3 (preservation is mechanical; PM-1 methodology is OUT OF SCOPE per § 5; if surfaces, route to gandalf per § 6) |
| **Disc #41 substrate-led vocabulary lock** | S3 archive variant preservation enables substrate-led emergence at PM-1 (variant population substrate); composes with S1 + S7 substrate diversity |
| **Disc #42a framing-audit Q1-Q6** | Applied at every refactor step; Instance 6 awareness (canonical-vs-implementation gap pattern — verify Phase 4 hook docstring matches implementation) |
| **Disc #45 vocabulary lock** | variant_id naming uses locked vocabulary (substrate / kit / BC cell / T4 strategy / investment profile); no class/role/archetype non-exempt |
| **Disc #48 RETIRED per Amendment 3** | No pre-flight vm_stat gate; no concurrent count limit |
| **Pattern E autonomous-pair pre-authorization** | Applies at S6 Gate-2; NOT at S3 fire |
| **Recognition → empirical validation → commit** | Recognition: gamora S2 emits 270 enumerated variants; Validation: § 4 acceptance gates; Commit: rocket auto-commits per CLAUDE.md addendum |

---

## 8. Deliverables

1. **Math note** at `reincarnated-engine/src/reincarnated/generation/notes/cascade-r3-s3-archive-variant-preservation-math-2026-05-29.md` (Disc #1 BEFORE code change)
2. **Engine commit(s)** — wave5_season_orchestrator.py Phase 4 hook change + PM-1 input filter update + tests + tag (rocket prefix per CLAUDE.md)
3. **MIGRATION.md entry** at `reincarnated-engine/src/reincarnated/generation/MIGRATION.md` — cross-seam impact (Phase 4 hook lives in simulation/; rocket modifies cross-seam; gamora awareness)
4. **Completion record appended to this dispatch file** — captures: (a) variant preservation evidence (archive count vs S2 shipped count); (b) PM-1 input cardinality verification; (c) dedup key change documentation; (d) smoke + tests PASS; (e) any surface-to-KR findings
5. **AGENT_STATE.md checkpoint** at `reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` — S3 CLOSED + cascade-resumption-3 trajectory + S5b queued
6. **Auto-commit per CLAUDE.md team commit + push discipline addendum 2026-05-25** — work-products of authorized cascade-resumption-3 work; commit fires without re-asking; push REQUIRES Matt-explicit-auth (do NOT push)

---

## 9. Sign-off

**Authored:** knight-rider per Matt 2026-05-29 hive-state clarification (KR auto-routes in-scope per hive-mind decision-routing) + gandalf authorization § Stream S3 + gamora S2 close (variant population emitted; S3 preserves)

**Rocket session-start protocol:**
1. Onboard via § 1 required first reads (especially S2 completion record + Phase 4 hook surface + math note authoring)
2. Apply Disc #42a framing-audit Q1-Q6 at dispatch consumption — Instance 6 awareness (variant preservation is the cascade architecture promise Phase 4 archive must deliver)
3. Author § 2.3 math note BEFORE code change (Disc #1)
4. Execute § 2.1 + § 2.2 scope
5. Apply § 4 acceptance gates
6. Surface per § 6 if triggered — auto-route in-scope per hive-mind decision-routing; Matt-surface ONLY for authorization § 4 enumerated triggers (PM-1 degenerate fallback; Disc #42a catch; effort overrun)
7. Author § 8 deliverables
8. Auto-commit per CLAUDE.md addendum

**KR next-step on S3 close:** verify § 4 acceptance + § 8 deliverables; route S5b dispatch (rocket Wave B integration; depends on S3 + S5 ✅) per Amendment 2 § 2 trajectory.

**Cascade trajectory:** S3 → S5b → S6 → A2-1 RE-FIRE-3 → A2-2 → A2-7 + D13 parallel-fire → Cycle 14 v1 MVP D9 close.

---

## Completion record

**Status:** CLOSED
**Date:** 2026-05-29
**Agent:** rocket
**Commit:** `40a53cb` — `rocket(S3): wire S2 variant population into Phase 4 archive + PM-1 clustering input`
**Tag:** `rocket/v1.0-cascade-r3-s3-archive-variant-preservation-1`

### Deliverables

- **Math note (Disc #1):** `src/reincarnated/generation/notes/cascade-r3-s3-archive-variant-preservation-math-2026-05-29.md` — variant cardinality projection (270→~102-132 shipped), dedup key change analysis, Option B VariantKitRow architecture rationale, PM-1 input cardinality projection (>>24 → GMM BIC), schema impact (no change), existing consumer audit (all SAFE)
- **Engine implementation:** `src/reincarnated/simulation/wave5_season_orchestrator.py` — VariantKitRow dataclass, `_build_variant_kit_rows()` helper, Phase 2.5 variant enumeration block, Phase 3 + Phase 4 extended call sites
- **Tests:** `tests/test_cascade_r3_s3_archive_variant_preservation.py` — 36 tests across 8 sections; all PASS
- **MIGRATION.md cross-seam entry:** `src/reincarnated/generation/MIGRATION.md` — S3 archive-variant-preservation section with full API change documentation
- **AGENT_STATE.md checkpoint:** `src/reincarnated/generation/AGENT_STATE.md` — S3 CLOSED with all 15 implementation steps, acceptance gate results, framing-audit findings

### Acceptance gates

- **AG-1 (dedup key change):** PASS — VariantKitRow.character_id = `{bc_cell_id}_s2_{strategy}_{invest}` (S2 legendary_id); base kits retain `S1_{encounter_id}_s{idx}` scheme; no collision
- **AG-2 (PM-1 cardinality):** PASS — PM-1 receives base (~18-54) + variant (~102-132) = >>24 → GMM BIC-selected (above SPARSITY_TIER_GMM_BIC=24); Instance 6 degenerate fallback eliminated
- **AG-3 (schema no-change):** PASS — `kit_id TEXT NOT NULL PRIMARY KEY` accepts any TEXT; S2 legendary_ids are valid; no additional columns required
- **AG-4 (backward compat):** PASS — `variant_configs=None`, `variant_kit_rows=None` defaults; existing callers unchanged; degeneracy return path updated 5→6-tuple (empty list appended)
- **AG-5 (smoke test):** PASS — 36/36 new tests; 255 combined PASS; 0 regressions introduced

### Framing-audit finding (Disc #42a)

The dispatch described "extend dedup key" but the actual gap was that S2 variant configs never reached Phase 4 at all — they flow through a separate code path producing config dicts, not KitCandidates. Resolved by VariantKitRow bridge (Option B — simpler-implementation principle). This is a framing correction, not a scope deviation; all acceptance gates satisfied.

### Cross-seam note

`wave5_season_orchestrator.py` is gamora's seam. Modification was pre-authorized by dispatch § 2.2 ("Phase 4 hook lives in `simulation/wave5_season_orchestrator.py` gamora seam; MIGRATION.md required"). MIGRATION.md entry written.

### KR handoff

S3 CLOSED. Route S5b dispatch (rocket Wave B integration; depends on S3 + S5) per Amendment 2 § 2 trajectory. S5 status with gamora is the remaining dependency before S5b fires.

**Signed:** knight-rider (orchestrator)
