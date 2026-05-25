# Dispatch — 2026-05-25 — rocket — Cycle 12 Layer 2 BC-target subspace generator (kit identity)

**From:** knight-rider
**To:** rocket (generation seam — engine content-generation owner)
**Approved by:** Matt 2026-05-25 (Cycle 12 framing brief bulk-ratification — interface contract § 4 LOCKED + Q3 Option B AUGMENT + Q4 Option B parallel-after-Gate-1; KR autonomously orchestrates Layer 2 dispatch authoring per scope-doc § 1)
**Estimated effort:** ~2-3 weeks rocket
**Acceptance:** BC-target subspace generator produces `PlayerClass` instances per framing brief § 4 contract (with Gate-1 amendments applied); generator implements MC-1 Hybrid H3 cell sampling + MC-2 hybrid filter-then-sample substrate-binding + gandalf Option B routing; AUGMENT pattern preserves legacy `ClassGenerator` as fallback; round-trip smoke (generator emits PlayerClass → star-lord JSON serialize → loadout consumes); jack-ryan Gate-2 PASS

---

## Context

Cycle 12 (full new engine parallel-build per Option γ) opens with rocket parallel-firing Layer 2 (kit identity) and Layer 3 (skill content) per framing brief § 8 + scope-doc § 1. **Layer 2 produces the `PlayerClass` kit identity** — the BC-target subspace generator that consumes substrate from v1_scope per cell-match + substrate-binding and emits PlayerClass instances downstream consumers (Layer 3 skill content; Layer 4 multi-dim convergence; Layer 6 § 8 alteration wire-up) consume.

**All 5 pre-Layer-2 prereqs ✅ CLEARED (per Cycle 12 state file Wave 0/0.5):**
1. jack-ryan Gate-1 ✅ — CLEAR-WITH-AMENDMENTS (7 WARN + INFO-4)
2. legolas MC-1 ✅ — Hybrid H3 sampling
3. legolas MC-2 ✅ — hybrid filter-then-sample substrate-binding
4. gandalf comp-policy § 4 ✅ — Option B (12-cell overrides + default heuristic)
5. elrond pre-Layer-2 prep ✅ — per-cell register breakdown + coherence matrix variant 2.C

**KR direct DB verification finding (Discipline #11; resolves elrond gap 1):** actual v1_scope=1 row count = **2,293** (NOT 3,042 from Cycle 10 wind-down quote). Tier-A drift since Cycle 10 (1,431 → 675; loss of 756 rows). Distribution: H 1,202 (52.4%) + F 1,022 (44.6%) + Myth 37 (1.6%) + MM 32 (1.4%); per-tier S=539, A=675, B=1,056, C=23. **Rocket Layer 2 generator MUST consume actual substrate state (2,293 rows), NOT the framing-brief-era 3,042 quote.** Capture discrepancy in math-note for v1.1+ elrond reconciliation queue.

Fires in PARALLEL with Layer 3 dispatch (skill content; same rocket seam — sub-agent instances are independent). Q4 Option B parallel sequencing means L2 + L3 produce coordinated outputs against the LOCKED framing brief § 4 contract.

---

## Required reading before starting

### Authority-of-record (LOCKED canon — primary load-bearing references)

- **`agentic_orchestration/gandalf/notes/2026-05-25-cycle-12-new-engine-parallel-build-framing-brief.md`** — § 4 PlayerClass interface contract (RATIFIED + LOCKED; primary scope target) + § L9 (mechanical vs semantic substrate split — load-bearing for `mechanical_substrate_triple`) + § L11 (strict 4-tuple matching for gauntlet sim) + § 2 (Layer 2 scope statement)
- **`agentic_orchestration/cycles/cycle-12-hive-mind-scope.md`** — § 1 (autonomous-scope authorities) + § 5 (escape-hatch triggers) + § 6 (pre-resolved known-unknowns)
- **`canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md`** — Architecture B Phase 2 substrate-binding spec (primary load-bearing)
- **`canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md`** — § 3 (Option α/β/C matching strategies) + § 4 (thin-cell resolution + 12-cell explicit routing locked at Stage 3) + § 5 (per-cell coverage)
- **`canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`** — 8 BC axes + 22-cell BC roster + 5-tuple cell coordinate system (range × tempo × amplitude × attribute × proxy-density)

### Methodology + critique-pair inputs (consume directly)

- **`agentic_orchestration/legolas/research/cycle-12-mc-1-bc-target-cell-sampling-methodology-2026-05-25/methodology-recommendation.md`** — Hybrid H3 deterministic per-cell-fired-once enumeration with substrate pre-filter + composition-policy-weighted ordering (primary L2 sampling methodology)
- **`agentic_orchestration/legolas/research/cycle-12-mc-2-substrate-binding-heuristics-2026-05-25/methodology-recommendation.md`** — Hybrid filter-then-sample with soft coherence weighting (score = 0.40·tier + 0.35·cell_match + 0.15·element_weapon_kind_coherence + 0.10·novelty); thin-cell-fallback cascade (relax weapon_mechanical_profile sub-dims first; element last); cheapest-refuting-test (50-kit spot-check; ≥90% coherence + ≥25% diversity + ≤10% deep-relaxation)
- **`agentic_orchestration/gandalf/notes/2026-05-25-comp-policy-section-4-coverage-gap-confirmation.md`** — Option B verdict + verdict memo § 3 dispatch text (12-cell explicit override list per-cell runtime behavior + default heuristic for un-routed cells + escape-hatch triggers)
- **`agentic_orchestration/qa/findings/2026-05-25-gate1-cycle-12-interface-contract.md`** — Gate-1 7 WARN + 3 INFO findings (action items for L2 dispatch authoring per finding F1-F7 + INFO-3/4)

### Substrate artifacts (consume as Layer 2 inputs)

- **`agentic_orchestration/elrond/cycle-12-pre-layer-2/per-cell-register-breakdown-2026-05-25.md`** — empirical per-cell register skew (5 cells ≥85% single-register; bimodal distribution); informs cell-weight parameter selection
- **`agentic_orchestration/elrond/cycle-12-pre-layer-2/element-weapon-kind-coherence-matrix-2026-05-25.md`** — 3 matrix variants; **consume variant 2.C row-normalized** for MC-2's `w_coherence × element_weapon_kind_coherence_score` scoring function; note keyword-inference caveat (no `element` column on substrate; v1.1+ schema-evolution candidate)
- **Substrate DB:** `/Users/admin/Games/reincarnated-loadout/data/telemetry.db` table `weapon_knowledge_entries` (actual v1_scope=1 row count = 2,293 per KR direct verification 2026-05-25)

### Engineering-disciplines + cross-seam

- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — load-bearing: #1 (math-before-code) + #2 (smoke-test) + #8 (schema validation at export boundary) + #11 (empirical inspection) + #18 (methodology-before-execution) + #19/#19.1 (background processes + cheapest-refuting-test) + #25 (semantic-layer rep-audit)
- `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` § v1.3 (Cycle 11 schema extensions — `t4_alteration_output` shape + 4 new fields)
- `~/Games/reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` (rocket seam state; current ClassGenerator implementation context)
- Cycle 11 § 8 implementation: `~/Games/reincarnated-engine/src/reincarnated/generation/mechanic_alteration.py` (6 strategies including DEFENSIVE_TRADEOFF — input semantics for `t4_alteration_output` field)
- ADR-004 MIGRATION.md cross-seam requirement

---

## Math-before-code (per Discipline #1)

Author math-note at `~/Games/reincarnated-engine/src/reincarnated/generation/notes/cycle-12-layer-2-bc-target-subspace-generator-2026-05-25.md` BEFORE implementation fires, covering:

### Math 1 — Cell sampling distribution (MC-1 Hybrid H3)

- Substrate pre-filter: enumerate 22 BC roster cells; per-cell substrate row count from v1_scope=1 (actual 2,293-row state); classify each cell as BLOCKED (zero eligible) / THIN (<5 rows; configurable floor) / READY
- Per-cell-fired-once base enumeration in descending policy-weight order (composition policy v1 § 2)
- Multi-fire extension for N_kits > 22: additional quota proportional to policy weights
- Tier S substrate draws first within each cell

### Math 2 — Substrate-binding heuristic (MC-2 hybrid filter-then-sample)

- Score function: `score = 0.40 × tier_weight + 0.35 × cell_match + 0.15 × element_weapon_kind_coherence + 0.10 × novelty`
  - `tier_weight`: Tier S=1.0; A=0.75; B=0.5; C=0.25 (proposal; rocket may refine)
  - `cell_match`: per Option α/β/C matching strategy per composition policy § 3 (L11 strict 4-tuple for gauntlet sim)
  - `element_weapon_kind_coherence`: lookup against elrond matrix variant 2.C row-normalized [0, 1]
  - `novelty`: anti-repetition penalty (per-cell instance counter / total instances)
- Filter to top-k = max(3, N_candidates // 5)
- Sample from filtered set with residual tier weights
- Thin-cell-fallback cascade (trigger <5 candidates): relax in order weapon_mechanical_profile sub-dims → tempo → range → energy_type → element (element LAST — element incoherence most expensive for Phase 5 narration)
- Graceful-fail: return UNGENERABLE (not NULL triple) — surfaces enrichment needs to substrate-curation v1.1+ queue

### Math 3 — Composition policy § 4 routing (gandalf Option B)

- For each of 12 LOCKED § 4.1 cells: apply explicit per-cell runtime behavior per gandalf verdict memo § 3 (FOLD, Stage 3.5 filter, Sidecar B filters, § 8.6 proxy-spawn flags, Option C cross-attribute, etc.)
- For un-routed cells (including Cells 11 Red Mage + 20 Holy Knight + 22 Monk + 24 Artillery Mage): apply default hybrid filter-then-sample heuristic per MC-2; thin-cell-fallback cascade fires if substrate is thin
- Capture cell-routing-source provenance (LOCKED vs DEFAULT) on PlayerClass for downstream audit
- Cells 14/15/17/23 routed per § 4.1 (in LOCKED 12) — thin-cell-fallback is runtime safety net only

### Math 4 — Per-cell register-share targeting (MC-1 surprise 1 + elrond gap finding)

- Per gandalf comp-policy + MC-1 surprise 1: composition policy v1 § 1 aggregate register-share targets (~50-55% historical / ~30-35% fantasy / ~10-15% mythological / ~5% military_modern) apply at AGGREGATE generation scale, NOT per-cell weights
- Per elrond per-cell register breakdown: per-cell distributions are bimodal (5 cells ≥85% single-register); rocket Layer 2 weights per-cell FIRING FREQUENCY (not per-cell register weights) to hit aggregate targets
- Actual v1_scope distribution (KR-verified): H 52.4% + F 44.6% + Myth 1.6% + MM 1.4% — mythological + military_modern are critically thin; aggregate targeting via firing-frequency weighting can compensate within fire budget

### Math 5 — Per-cell BLOCKED / THIN classification + reporting

- Pre-fire substrate audit: classify each of 22 cells as BLOCKED / THIN / READY
- Surface per-cell substrate count + register breakdown in audit log
- BLOCKED cells route per comp-policy § 4.1 (12 cells locked); un-routed BLOCKED cells (Cells 11, 22, 24 per elrond gap finding) route default + thin-cell-fallback per gandalf Option B

---

## Cross-seam contract change? (Principle 6 gate)

**Yes.** Layer 2 generator EMITS `PlayerClass` instances consumed by Layer 3 (parallel) + Layer 4 + Layer 6 + star-lord JSON export + loadout app. PlayerClass shape locked per framing brief § 4 contract (with Gate-1 amendments applied per scope below).

**Round-trip smoke REQUIRED per Principle 6:**
- Generator emits `PlayerClass` instance (Python dataclass)
- Star-lord serializes through JSON export (consume existing star-lord schema; new fields per Gate-1 amendments require star-lord MIGRATION.md update if any field is new vs Cycle 11 Wave 1)
- Loadout app consumes back (consume existing TS interface or update if shape changes)
- Round-trip fixture should cover: a class with t4_alteration_output populated; a class with t4_alteration_output null; a class with off_hand_item populated; a class with off_hand_item null

**MIGRATION.md REQUIRED per ADR-004:**
- `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` extend with new entry (`§ v1.4 Cycle 12 Layer 2 PlayerClass shape` or rocket judgment)
- Document Gate-1 amendments applied (WARN-2 mechanical_substrate_triple vocabulary; WARN-4 StatDistribution defined + Optional pre-Layer-4; WARN-6 JSON-primitive constraint on generation_params; WARN-7 generation_seed required; INFO-4 engine_version="v2.0" required)
- Document AUGMENT pattern: legacy ClassGenerator preserved as fallback; new generator default; source_library discriminates ("generator_v2" vs "legacy_classgenerator")
- Document substrate-curation v1.1+ queue (v1_scope row-count reconciliation; element column schema evolution; cells 11/20/22/24 § 4.1 amendment)

---

## Scope (rocket Layer 2 BC-target subspace generator implementation)

### Gate-1 amendment integration (REQUIRED at L2 dispatch consumption)

Per jack-ryan Gate-1 finding (CLEAR-WITH-AMENDMENTS 7 WARN + INFO-4 recommended):

- **WARN-2 — mechanical_substrate_triple vocabulary:** the field is `tuple[element_str, weapon_kind_subtype_str, weapon_mechanical_profile_label_str]` where the third element is a defined vocabulary string matching `weapon_kind_classified_subtype` patterns in the DB (per Cycle 12 Wave 0 SC-2 backfill: 10-value canonical enum + Cycle 10 Stage 0a enum). Rocket may EITHER keep tuple-of-strings shape with documented vocabulary OR promote to structured `MechanicalSubstrateTriple` dataclass for type safety (rocket judgment per dispatch open question)
- **WARN-4 — StatDistribution type + Optional pre-Layer-4:** define `StatDistribution` as named type (or alias `dict[str, float]` keyed by STR/INT/WIS/DEX per attribute system canonical). Mark Layer-4-populated fields `Optional[...]` pre-Layer-4: `stat_allocation: Optional[StatDistribution]`, `attribute_coupling: Optional[list[str]]`, `converged_modifier: Optional[float]`. Layer 2 emits stub PlayerClass (Layer-4 fields = None); Layer 3 composes against stub; Layer 4 populates
- **WARN-6 — generation_params JSON-primitive constraint:** constrain `generation_params` values to `Union[str, int, float, bool, None, list, dict]` (JSON-primitives recursive). Enforce via Discipline #8 schema validation at export boundary (Pydantic `model_validator` OR explicit `json.dumps(generation_params)` round-trip in smoke)
- **WARN-7 — generation_seed required:** `generation_seed: int` is REQUIRED-not-nullable per Disciplines #1 + #10 (deterministic reproducibility load-bearing for algorithm validation; canonical precedent: `generate-season --seed N` discipline)
- **INFO-4 — engine_version field:** add `engine_version: str` REQUIRED field to PlayerClass; value `"v2.0"` for new engine path (distinct from legacy ClassGenerator's path); prevents Cycle 10 Sidecar A telemetry-gap pattern recurrence per Discipline #7

### Methodology integration (REQUIRED at L2 implementation)

- **MC-1 Hybrid H3 sampling**: substrate pre-filter + per-cell-fired-once enumeration + multi-fire extension + Tier-S-first within cell
- **MC-2 hybrid filter-then-sample substrate-binding**: scoring function + filter top-k + sample with tier weights + thin-cell-fallback cascade
- **gandalf comp-policy § 4 Option B routing**: 12-cell LOCKED override + default heuristic for un-routed; cells 11/20/22/24 default + v1.1+ § 4.1 amendment queue flag
- **MC-1 surprise 1 + elrond per-cell register**: per-cell empirical distributions weight per-cell firing frequency (NOT per-cell register weights); aggregate targets via firing-frequency weighting

### AUGMENT pattern (Q3 Option B)

- Legacy `ClassGenerator.generate()` PRESERVED as fallback (not deprecated; not removed)
- New `BcTargetSubspaceGenerator.generate()` (or rocket naming judgment) is production-default
- BOTH generators emit PlayerClass shape (per § 4 contract)
- `source_library` field discriminates: `"generator_v2"` (new) vs `"legacy_classgenerator"` (legacy)
- Test scaffolding can fall back to legacy for regression
- Post-v1.1 stability, consider deprecating legacy per Q3 Option A (NOT Cycle 12 scope)

### L11 strict 4-tuple matching enforcement

- Generator enforces STRICT 4-tuple cell-match (per composition policy § 3 Option α/β/C strict-match patterns) for gauntlet sim kit generation
- v1.1+ broader equip flexibility for actual player-game equip is a separate design concept (per framing brief § L11; deferred Pattern-B design call)
- Document strict-match enforcement at generator level (not contract-instance-level per Gate-1 cross-cutting finding)

### Cells 14/15/17/23 substrate-thin handling

- Per MC-1 surprise 2 + gandalf verdict: all 4 cells are in LOCKED 12 per § 4.1; substrate is thin OR zero for these cells
- Rocket Layer 2 consumes § 4.1 explicit routing for each (FOLD; Stage 3.5 filter; Sidecar B filters; § 8.6 proxy-spawn flags per gandalf verdict memo § 3)
- Thin-cell-fallback cascade per MC-2 § 5.2 is runtime safety net (not primary routing for these cells)

### Cells 11/20/22/24 default-heuristic + v1.1+ amendment queue

- Per gandalf Option B: cells 11 (Red Mage) + 22 (Monk) + 24 (Artillery Mage) are un-routed in § 4.1 — Layer 2 applies default hybrid filter-then-sample + thin-cell-fallback
- Cell 20 (Holy Knight): per gandalf verdict — Option C cross-attribute candidate; default hybrid heuristic applies; v1.1+ canonical amendment queued for one-line § 4.1 addition
- Capture provenance on PlayerClass (cell-routing-source = "default_heuristic_v1.1_amendment_queued" OR similar; rocket naming judgment)

### Substrate state alignment (KR direct DB verification)

- Generator consumes actual v1_scope=1 state at `/Users/admin/Games/reincarnated-loadout/data/telemetry.db` (2,293 rows per KR 2026-05-25 verification)
- Document Tier-A drift since Cycle 10 wind-down (1,431 → 675; loss of 756 rows) in math-note for v1.1+ elrond reconciliation queue
- Use elrond per-cell register breakdown artifact for cell-weight parameter selection
- Use elrond coherence matrix variant 2.C for MC-2 scoring; note keyword-inference caveat (no `element` column; v1.1+ schema-evolution)

### Smoke + acceptance gates

- **Smoke gate 1**: generator produces N=22 kits (one per cell base enumeration); for each kit, verify PlayerClass shape conforms to § 4 contract (with Gate-1 amendments)
- **Smoke gate 2 (per MC-2 cheapest-refuting-test)**: 50-kit spot-check; verify ≥90% coherence (element × weapon_kind pairings reasonable) + ≥25% unique-row diversity + ≤10% deep-relaxation (cascade level 3+)
- **Smoke gate 3 (round-trip)**: emit PlayerClass → star-lord JSON serialize → loadout deserialize → field-presence + shape check
- **Smoke gate 4 (AUGMENT)**: legacy ClassGenerator continues to produce PlayerClass shape; both paths smoke independently

---

## Out of scope (explicit non-goals)

- Layer 3 skill content (separate dispatch fires in PARALLEL; same rocket seam but different sub-agent instance)
- Layer 4 multi-dim convergence (fires after L2+L3 lock; MC-3 consult gates L4)
- Layer 6 § 8 wire-up + L9 opportunity-scan refactor (fires after L4 lands)
- Layer 7 BDI test framework (DEFERRED to v1.1 per scope-doc § 0)
- Star-lord schema changes beyond MIGRATION.md cross-seam documentation (star-lord makes its own decisions on schema)
- Loadout app changes (drax consumes new shape per MIGRATION.md; separate seam)
- Algorithm § 8 v1.1 strategies (4 sim-extension-required + proxy-spawn) — v1.1+ per Cycle 11 P2b
- T4-B v1 catalogue contents — parallel-track gandalf + Matt design call; NOT in Cycle 12 scope
- Broader weapon-equip flexibility (L11 deferred concept) — v1.1+ design concept
- Substrate-curation v1.1+ items (element column schema evolution; v1_scope reconciliation; Cells 11/20/22/24 § 4.1 amendment; broader pf2ools-quarantined cleanup per SC-2 anomalies) — capture in MIGRATION.md + math-note for v1.1+ queue; NOT in this dispatch
- Architectural amendments to PlayerClass / SkillTree / ConvergenceResult / Layer 6 wire-up contract (LOCKED per framing brief § 4; escalate to gandalf via KR if rocket implementation surfaces contract gap — per scope-doc § 5 escape-hatch)

---

## Acceptance criteria

- [ ] Math-note authored at `~/Games/reincarnated-engine/src/reincarnated/generation/notes/cycle-12-layer-2-bc-target-subspace-generator-2026-05-25.md` BEFORE implementation per Discipline #1
- [ ] `BcTargetSubspaceGenerator` (or rocket naming judgment) implemented per MC-1 + MC-2 + gandalf Option B + Gate-1 amendments
- [ ] PlayerClass dataclass implemented per § 4 contract + Gate-1 amendments (engine_version + generation_seed required; Layer-4 fields Optional; StatDistribution defined; JSON-primitive generation_params)
- [ ] AUGMENT pattern: legacy ClassGenerator preserved; new generator default; source_library discriminator
- [ ] L11 strict 4-tuple matching enforced at generator level
- [ ] 12 LOCKED cells routed per comp-policy § 4.1 (gandalf verdict memo § 3 per-cell behavior)
- [ ] Un-routed cells (incl. 11/20/22/24) route default hybrid heuristic + thin-cell-fallback; v1.1+ § 4.1 amendment captured
- [ ] Substrate state aligned (2,293 v1_scope=1 rows from KR-verified state)
- [ ] Smoke gates 1-4 PASS per § Scope smoke section
- [ ] Round-trip smoke: PlayerClass → JSON → consumer back PASS per Principle 6
- [ ] MIGRATION.md authored (extend `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` § v1.4 or rocket naming) per ADR-004
- [ ] Cheapest-refuting-test (50-kit spot-check ≥90% coherence + ≥25% diversity + ≤10% deep-relaxation) PASS per MC-2 § 5.2 + Discipline #19.1
- [ ] No regression on existing engine code (regression suite PASS)
- [ ] AGENT_STATE.md updated at session end
- [ ] Tag: `rocket/v0.1-cycle-12-layer-2-bc-target-subspace-generator-2026-05-25` (or per-sub-component intermediate tags acceptable per rocket discretion)

---

## Open questions for the agent to resolve

- Whether `mechanical_substrate_triple` stays as `tuple[element_str, weapon_kind_subtype_str, weapon_mechanical_profile_label_str]` OR promotes to structured `MechanicalSubstrateTriple` dataclass for type safety (rocket judgment; either is contract-compliant)
- Whether tier weights in MC-2 scoring function (S=1.0/A=0.75/B=0.5/C=0.25) are the right starting point OR rocket refines empirically; document in math-note
- Whether thin-cell-fallback floor threshold is 5 candidates (MC-2 default) OR rocket adjusts after running smoke against actual substrate state (2,293 rows; many cells likely THIN given the smaller-than-quoted substrate)
- Whether wind/lightning critical-thin substrate (8 + 5 rows S+A+B per elrond) warrants alteration to MC-2 scoring (e.g., element-weight floor for these elements specifically) OR thin-cell-fallback cascade is sufficient
- Whether KR should pre-fire elrond v1.1+ reconciliation dispatch on Tier-A drift (756 lost rows since Cycle 10) OR rocket Layer 2 implementation proceeds against current 2,293-row substrate without reconciliation (RECOMMEND: proceed; capture in math-note + MIGRATION.md; v1.1+ reconciliation is separate workstream)
- Whether `BcTargetSubspaceGenerator` should consume per-cell register breakdown artifact directly OR rocket re-runs SQL at runtime (rocket judgment; recommend consume artifact for reproducibility per Discipline #10)
- Whether AUGMENT layer needs a feature-flag mechanism (e.g., env var to toggle between generators) OR source_library discriminator alone suffices (rocket judgment per testing harness needs)

---

## References

- `agentic_orchestration/gandalf/notes/2026-05-25-cycle-12-new-engine-parallel-build-framing-brief.md` § 4 (contract LOCKED) + § L9 + § L11
- `agentic_orchestration/cycles/cycle-12-hive-mind-scope.md`
- `agentic_orchestration/qa/findings/2026-05-25-gate1-cycle-12-interface-contract.md` (Gate-1 7 WARN + 3 INFO)
- `agentic_orchestration/legolas/research/cycle-12-mc-1-bc-target-cell-sampling-methodology-2026-05-25/methodology-recommendation.md`
- `agentic_orchestration/legolas/research/cycle-12-mc-2-substrate-binding-heuristics-2026-05-25/methodology-recommendation.md`
- `agentic_orchestration/gandalf/notes/2026-05-25-comp-policy-section-4-coverage-gap-confirmation.md`
- `agentic_orchestration/elrond/cycle-12-pre-layer-2/per-cell-register-breakdown-2026-05-25.md`
- `agentic_orchestration/elrond/cycle-12-pre-layer-2/element-weapon-kind-coherence-matrix-2026-05-25.md`
- `canonical/story/qd-engine-end-to-end-workflow-2026-05-24.md`
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md`
- `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md`
- `canonical/story/attribute-system-2026-05-24.md` (STR/INT/WIS/DEX for StatDistribution definition)
- `~/Games/reincarnated-engine/src/reincarnated/export/MIGRATION.md` § v1.3
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`

---

## Sign-off

**Author:** knight-rider (orchestrator)
**Authority:** Matt 2026-05-25 Cycle 12 framing brief bulk-ratification (Q1 Option γ + Q3 Option B AUGMENT + Q4 Option B parallel-after-Gate-1) + KR autonomously orchestrates Layer 2 dispatch authoring per scope-doc § 1
**Status:** FIRE — all 5 pre-Layer-2 prereqs cleared; fires in parallel with Layer 3 dispatch

**Matt-touch sequence:** rocket Layer 2 implementation lands (~2-3 weeks) → jack-ryan Gate-2 validates → KR captures in state file; integrates into Layer 4 + Layer 6 sequencing (Layer 4 fires after L2+L3 lock + MC-3 methodology consult); if rocket surfaces contract gap requiring framing brief § 4 amendment, KR routes to gandalf via § 5 escape-hatch
