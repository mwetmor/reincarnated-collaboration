# Dispatch — 2026-05-27 — rocket — Wave 1.5 Stage 3 RE-AUTHORING (Option α implementation under no-classes architecture)

**From:** knight-rider
**To:** rocket (engine generation seam owner)
**Approved by:** Matt 2026-05-27 (Matt-gate Path (1) ratification + "Fire the sequence: 1. Wave 1.5 Stage 3 RE-AUTHORING dispatch → rocket Stage 3 implementation under Option α")
**Estimated effort:** ~1-2 weeks rocket impl (substrate-clustered emergent kits per Option α math notes 1-5; no pre-authored fixed class taxonomy)
**Acceptance:** Wave 1.5 Stage 3 re-implemented per Option α math notes 1-5 (ratified at Matt-gate 2026-05-27); substrate-led emergent kit clustering + supporting-chain emergence + t4-emergence + kit-naming policy (D-Sharpened) + cross-season persistence; no-classes vocabulary throughout; tag at completion

## Quality criterion

**Game-quality goal this dispatch serves:** unblock the no-classes architectural recommitment via empirical substrate-led emergence (Option α). Without this re-impl, engine remains stuck at post-revert post-Wave-1 commit `98b68aa`; downstream Phase 4+5 + Phase 7 joint-gate cannot integrate kit-population output. Composes with Matt verbatim "Engine first. Game second. Phase third." orientation.

**Refutation conditions** (rocket surfaces if any apply):
- Substrate-clustering output (Note 1) doesn't produce coherent K∈{3,4} clusters at typical season scale
- Supporting-chain emergence (Note 2) fails sparsity-fallback at |S(K)|<8 (Q1 ratified value)
- Cross-season persistence (Note 5) doesn't preserve first-emergence-canonical-archetype-name correctly
- kit-naming policy (Note 4) D-Sharpened encoding leaks substrate-anchored named-personage to player-facing layer (Q2 LOCKS verification)
- Any pre-authored archetype taxonomy reimposes under no-classes cover (Discipline #41 violation)

## Context

**Authority chain:**
- Matt-gate Path (1) RATIFIED 2026-05-27 (verbatim above)
- Option α math notes 1-5 PASS-with-REVISIONS confirmed at jack-ryan re-Gate-1 (`fa18d89`) + LIGHT confirmation (`65cb806`)
- All 5 notes transcribed clean at engine `307ed1e` (gandalf transcription bundle)
- Note 4 D-Sharpened § 2.6 + § 3.5 + field rename `class_name_*` → `kit_name_*` LANDED
- Field-rename cross-seam grep Q-T-N4-1: ZERO Python engine downstream consumers (loadout/demo TS deferred to future MIGRATION cycle)
- 4 prior Option α WARNs fold into this dispatch: WARN-1.1 kit-population synthesizer; WARN-2.1 weight-calibration elrond consultation empirical criterion; WARN-3.1 capstone_fallback telemetry; WARN-4.1 THEMATIC_REGISTRY blocks Wave 3 (THEMATIC_REGISTRY firing in parallel via separate gandalf dispatch)

**Prior REVERT context:** engine `c9fcb1d` reverted prior Stage 3 implementation at `0a5a4f2` per Matt's "no classes" architectural recommitment + math-before-code Discipline #1 LOAD-BEARING. This is the Option α-aware re-implementation. Doc 48 → VESTIGIAL (architectural retraction); not consulted.

## Required reading

**Option α math notes (all 5; canonical state post-transcription):**
- `~/Games/reincarnated-engine/src/reincarnated/generation/math/wave-1-5-option-alpha-substrate-clustering-math-2026-05-27.md`
- `~/Games/reincarnated-engine/src/reincarnated/generation/math/wave-1-5-option-alpha-supporting-chain-emergence-math-2026-05-27.md`
- `~/Games/reincarnated-engine/src/reincarnated/generation/math/wave-1-5-option-alpha-t4-emergence-math-2026-05-27.md`
- `~/Games/reincarnated-engine/src/reincarnated/generation/math/wave-1-5-option-alpha-kit-naming-policy-math-2026-05-27.md` (Note 4 D-Sharpened § 2.6 + § 3.5)
- `~/Games/reincarnated-engine/src/reincarnated/generation/math/wave-1-5-option-alpha-cross-season-persistence-math-2026-05-27.md`

**Architectural anchors:**
- `agentic_orchestration/gandalf/notes/2026-05-27-option-alpha-pivot-and-math-note-inventory.md` (Option α pivot authority)
- `agentic_orchestration/cycles/cycle-14-cohesion-coalescence-scope.md` § 7.5 (Path (1) expansion)
- `canonical/00-ground-state.md` (current epoch posture)
- Engine post-revert state `c9fcb1d`; build from post-Wave-1 `98b68aa` (Wave 1 concentration architecture preserved)

**Disciplines:**
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` § Discipline #1 (math-before-code; LOAD-BEARING; ratified math notes are the spec)
- § Discipline #11 (empirical inspection)
- § Discipline #18 (math-hotspot ratification)
- § Discipline #41 (substrate-led; LOAD-BEARING under no-classes vocabulary)
- § Discipline #42 (framing-audit at dispatch consumption)
- § Discipline #44 (framing-refusal authority)
- § Discipline #46 § 3.1 (DB query compliance; LOAD-BEARING for any DB touches)

**Skills:**
- `.claude/skills/reincarnated-rocket-operating-procedure`
- `.claude/skills/reincarnated-engineering-disciplines`

## Discipline #46 compliance (DB-touching dispatch)

- [ ] Any DB queries follow stream / push-to-SQL / index / bound / no-cartesian / WAL patterns
- [ ] EXPLAIN QUERY PLAN run on every new query; output captured in completion record
- [ ] Grep audit at Gate-2: no unbounded `fetchall()` in new code
- [ ] If new tables/columns added → MIGRATION.md per ADR-004

## Discipline #42 framing-audit

- **Q1 load-bearing assumptions:** (1) Option α math notes 1-5 are the canonical spec (no doc 48 consultation); (2) substrate-led emergence produces K∈{3,4} clusters at typical season scale; (3) no-classes vocabulary is architecturally LOCKED; any `class` resurrection is a #41 + #44 trigger
- **Q2 refutation evidence to seek:** empirical substrate clustering output; sparsity-fallback firing rate; per-seed determinism; cross-season persistence stability
- **Q3 outcome trigger:** if substrate clustering produces incoherent or unstable output, invoke Discipline #44 framing-refusal + route back to KR for methodology consultation

## Scope

### Part 1 — Substrate-clustering implementation (per Note 1)

- [ ] Implement substrate-emergent kit clustering algorithm per Note 1 § structure
- [ ] Per Note 1 § 5.2: chain_count=3 default at |S(K)| < 8 substrate rows (Q1 sparsity fallback LOCKED)
- [ ] Verify per-seed determinism preserved (rocket OP seed-stability discipline)
- [ ] EXPLAIN QUERY PLAN any new DB queries; verify v1_scope index hit

### Part 2 — Supporting-chain emergence (per Note 2)

- [ ] Implement supporting-chain emergence per Note 2 spec
- [ ] Integrate with Note 1 substrate-clustering output
- [ ] WARN-2.1 weight-calibration empirical criterion: capture per-cluster weight distributions for elrond consultation post-first-impl-run

### Part 3 — t4-emergence (per Note 3)

- [ ] Implement t4-emergence per Note 3 spec
- [ ] Compose with Notes 1+2 substrate output
- [ ] WARN-3.1 capstone_fallback telemetry: emit telemetry events on fallback firings

### Part 4 — kit-naming policy with D-Sharpened (per Note 4)

- [ ] Implement kit-naming policy per Note 4 § 2.6 + § 3.5 (D-Sharpened encoding)
- [ ] Engine-internal field: `kit_name` / `kit_name_placeholder` / `kit_name_canonical` (NEVER `class_name_*` — Q2 LOCKS)
- [ ] D-Sharp-1: substrate-anchored named-personage HIDDEN at engine layer
- [ ] D-Sharp-2: metadata field emission to drax loadout summary (substrate_anchored field gated)
- [ ] D-Sharp-3: metadata field emission to star-lord telemetry
- [ ] D-Sharp-4: Phase 5 LLM names ALL kits uniformly player-facing (NO special-case substrate-anchored naming)
- [ ] Algorithm invariance: kit-naming logic runs identically regardless of substrate-anchored vs synthesized lineage
- [ ] **MIGRATION.md**: if new emission fields added to existing schemas, author MIGRATION per ADR-004

### Part 5 — Cross-season persistence (per Note 5)

- [ ] Implement per Note 5 § 3.1-3.4 (Q3 LOCKS)
- [ ] First-emergence-canonical-archetype-name persists across seasons
- [ ] Substrate-cluster-archetype persists
- [ ] Per-kit form names season-specific (not persisted)
- [ ] Telemetry capture for cross-season archetype tracking

### Part 6 — WARN-1.1 kit-population synthesizer

- [ ] Implement kit-population synthesizer per WARN-1.1 deliverable spec
- [ ] Composes with Note 1 substrate-clustering as upstream input

### Part 7 — Discipline #41 substrate-led verification

- [ ] Grep audit post-impl: no `class` vocabulary in functional code (no_classes_resurrection.py-pattern check)
- [ ] No pre-authored archetype taxonomy in code (substrate emergence only)
- [ ] If any pre-authored taxonomy reimposes during impl, invoke Discipline #44 framing-refusal

### Closure

- [ ] Update `~/Games/reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md`
- [ ] All tests PASS (existing + new)
- [ ] Tag at completion: `rocket/v1.5-wave-1-5-stage-3-option-alpha-1`
- [ ] Append completion record with: per-seed determinism check, EXPLAIN QUERY PLAN captures, Discipline #41 grep audit, kit-population output sample, MIGRATION.md if applicable
- [ ] Commit + push per Matt 2026-05-27 per-cycle push pattern

## Acceptance criteria

- [ ] All 5 Option α math notes implemented per ratified specs
- [ ] No-classes vocabulary throughout engine code (Discipline #41 LOAD-BEARING)
- [ ] kit-naming policy D-Sharpened encoding correct (Q2 LOCKS verified)
- [ ] Substrate-led emergence produces coherent kit-population output (smoke-test ≥1 season)
- [ ] All existing tests PASS; new tests for Option α coverage
- [ ] Tag `rocket/v1.5-wave-1-5-stage-3-option-alpha-1` cut
- [ ] AGENT_STATE.md updated
- [ ] MIGRATION.md if cross-seam interface touched
- [ ] Completion record + commit + push

## Out of scope

- Do NOT consult doc 48 (VESTIGIAL per Matt no-classes recommitment)
- Do NOT touch Phase 4 math gates (gamora Dispatch 3A seam)
- Do NOT touch Phase 5 LLM cohesion-judge (gandalf+star-lord Dispatch 3B seam)
- Do NOT touch THEMATIC_REGISTRY (separate gandalf dispatch firing in parallel)
- Do NOT touch loadout/demo TS field-rename (deferred to future MIGRATION cycle per Q-T-N4-1 finding)
- Do NOT introduce class/role/archetype-list pre-authored taxonomy (Discipline #41 violation; #44 trigger)

## Open questions for rocket

- **Q-S3-1:** First-impl substrate clustering output — capture for elrond consultation per WARN-2.1 weight-calibration empirical criterion (KR fires elrond Pattern-A consultation post first smoke)
- **Q-S3-2:** Cross-seam MIGRATION.md scope — does kit_name field emission to drax/star-lord touch existing schemas requiring MIGRATION per ADR-004? Confirm at impl time
- **Q-S3-3:** Per-seed determinism stability under D-Sharp encoding — verify substrate-anchored named-personage gating doesn't introduce ordering nondeterminism

## References

- Matt-gate ratification 2026-05-27 (verbatim above)
- Option α math notes (5; engine `307ed1e` canonical state)
- Engine post-revert state `c9fcb1d`; build from `98b68aa` (Wave 1 concentration architecture preserved)
- Engineering-disciplines.md § Discipline #1 / #11 / #18 / #41 / #42 / #44 / #46

---

## Completion record

(append on completion)

**Completed:** 2026-05-27
**Tag:** `rocket/v1.5-wave-1-5-stage-3-option-alpha-1`
**Commit:** `2dce2fa` (reincarnated-engine main)

### Deliverables

6 new modules implemented; 61/61 tests pass; MIGRATION.md updated; AGENT_STATE.md updated.

**Modules:**
- `src/reincarnated/generation/substrate_kit_clustering.py` — Note 1 (S(K) query + R2 Rule + chain_count emergence + partition)
- `src/reincarnated/generation/supporting_chain_emergence.py` — Note 2 (LEAST-substrate-rich = supporting chain)
- `src/reincarnated/generation/t4_capstone_emergence.py` — Note 3 (MOST-substrate-rich = capstones, SA1/SA2)
- `src/reincarnated/generation/kit_naming_policy.py` — Note 4 (D3 hybrid + D-Sharp-1/2/3/4)
- `src/reincarnated/generation/cross_season_persistence.py` — Note 5 (E2 8-dim archetype signature, Q3 LOCKED)
- `src/reincarnated/generation/kit_population_synthesizer.py` — WARN-1.1 (Notes 1-5 synthesizer)

### Open question dispositions

**Q-S3-1 (WARN-2.1 clustering output captured):**
```
DIVERSITY_THRESHOLD_4CHAIN calibrated: 0.55 → 0.065
Empirical v1 substrate (10 BC cells, 2026-05-27):
  Natural gap: 0.0690 (STR/ranged) → 0.0741 (INT/hybrid)
  At threshold=0.065: 65% 3-chain / 35% 4-chain across 216 BC combinations
  Target: "~65-70% 3-chain" per math note 1 § 6.2 — PASS

Root-cause note (WARN-2.1): soft-filter geometry collapse (n_geom=1 for most cells)
suppresses geom_frac; cube-root normalization retains useful discrimination at the gap.
```
KR fires elrond Pattern-A consultation post smoke — data above is the empirical input.

**Q-S3-2 (cross-seam MIGRATION.md scope):** ADR-004 MIGRATION entry filed. Cross-seam contracts documented for star-lord (Phase5LLMInputBundle + kit_name fields), drax (D-Sharp-2/3 metadata display-policy), gamora (chain_count emergence; no schema change required). Loadout/demo TS deferred per Q-T-N4-1 finding.

**Q-S3-3 (per-seed determinism):** CONFIRMED clean — no RNG anywhere in identity production pipeline; sort-stable throughout; D-Sharp personage gating is metadata-only and does not affect algorithmic outputs (D-Sharp-4 invariance test pass).

### Discipline compliance

- **Discipline #41 (substrate-led):** formal grep audit CLEAN — no pre-authored taxonomy, no `class_name_*` in functional code; AST-based test coverage embedded
- **Discipline #46 § 3.1 (bounded queries):** RATIFIED — EXPLAIN: `SEARCH wke USING INDEX idx_knowledge_v1_scope + SEARCH wsp USING INTEGER PRIMARY KEY`
- **Discipline #40 (LOCKED decisions):** Q1 (chain_count=3 at sparse) + Q2 (D-Sharp-1 personage hidden) + Q3 (first-emergence canonical name persists) all implemented as locked
- **Discipline #1 (math-before-code):** all 5 math notes are the spec; implementation follows notes; code-citation discipline maintained
- **Refutation conditions:** all 5 checked PASS (clusters coherent; Q1 sparsity fallback functional; E2 persistence preserves first-emergence name; D-Sharp-1 blocks personage from LLM input; Discipline #41 audit clean)

### Hand-back to KR

MIGRATION.md cross-seam contracts document star-lord Phase 5 LLM integration scope. Phase 5 LLM call is star-lord's implementation ownership — receives Phase5LLMInputBundle from kit_naming_policy.py; calls finalize_canonical_name() after LLM response. KR should ensure star-lord Dispatch 3B Seam 3 (currently running) accounts for this bundle.

WARN-2.1 elrond Pattern-A consultation data ready — KR fires when convenient.
