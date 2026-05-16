# Dispatch — 2026-05-16 — rocket — Form-bias Stage 2: abstract pair-structure (grouping layer) emission (VS2b S2; cadence Option II Stage 2)

**From:** knight-rider (authored per form-bias 5-entry batch Entry 5 cadence Option II Stage 2 + Matt 2026-05-16 Day 4 Tier 1 #4 confirmation)
**To:** rocket
**Approved by:** Matt at 2026-05-16 Day 4 ("YES to all 4 Tier 1")
**Status:** PENDING — HOLD-on-prior. Do NOT execute until your in-flight Step-1-bounded-review dispatch completes; rocket can only run one dispatch per session.
**Estimated effort:** 1-2 sessions (~4-8h); schema-additive work primarily; MIGRATION.md per ADR-004; no balance-affecting changes.
**Acceptance:** Abstract pair-structure (grouping-layer) fields added to engine schema additively alongside existing canonical-four; generator emits grouping-layer data per class; smoke season verifies field population; MIGRATION.md entry per ADR-004; intermediate tag.

---

## Context — Stage 2 of cadence Option II

Per form-bias 5-entry batch (`5d51b5a`) Entry 5 cadence Option II + cipher-width Outcome 2 lock (`1dff66d`):

> **Stage 2 — Abstract pair-structure (grouping layer) added alongside canonical-four.** Rocket emits per-season grouping data alongside existing canonical-four substrate. Additive. No removals. LLM still sees canonical-four at this stage (Stage 3 is when canonical-four hides from LLM via cipher migration). Verifies: grouping-layer infrastructure works; downstream consumers (drax / loadout / pimen integration / star-lord prompt prep) can begin consuming grouping data while canonical-four remains operative.

**Architectural context** (per cipher-width Outcome 2 + Foundation L2-decoupled):
- Substrate layer = canonical-four (internal mechanic; ARPG mechanics preserved)
- **Grouping layer = abstract pair-structure (THIS DISPATCH adds emission)**
- Vocabulary layer = per-season (star-lord Stage 2 separate dispatch generates)

Stage 1 (`rocket/v1.3-form-bias-stage-1-embodiment-axis @ 73db17f`) added embodiment-axis fields. This Stage 2 dispatch adds grouping-layer fields.

## What this dispatch does

### Step 1 — Schema field additions (additive grouping-layer)

Add the following fields to player class schema (or appropriate substrate location):

- **`grouping_pair_structure: dict[str, str]`** — abstract pair-structure labels keyed by canonical-four substrate; e.g., `{"fire": "kinetic_aggression", "water": "fluid_adaptation", "earth": "structural_resilience", "wind": "evasive_velocity"}` (illustrative; exact pair-structure vocabulary per cipher-width Outcome 2 architecture spec)
- **`grouping_season_id: str`** — per-season identifier for the grouping-layer vocabulary version (enables per-season variation while preserving per-class consistency within a season)
- **`grouping_layer_version: str`** — schema version of grouping layer for downstream consumer migration safety (e.g., `"v1.0"`)

Consult `canonical/story/form-bias-cadence-strategy.md` § 7.2 + cipher-width resolution entry (`1dff66d`) for the exact pair-structure vocabulary. If vocabulary is not fully specified, file finding for gandalf input; do NOT invent vocabulary unilaterally.

All fields are **additive** — existing class schema unchanged; canonical-four fields remain operative.

### Step 2 — Generator wiring

Update `class_generator.py` (and any related orchestration) to emit grouping-layer fields per class:

- `grouping_pair_structure` populated per canonical-four element with appropriate grouping label per cipher-width spec
- `grouping_season_id` derived from the regen's season_id
- `grouping_layer_version` = `"v1.0"` (or per current version constant)

Per-class consistency: within a single season, all classes share the same `grouping_pair_structure` mapping (consistent grouping vocabulary per season); per-class variation is in WHICH canonical-four elements they use, not in HOW those elements group.

### Step 3 — Tests + smoke

Per Discipline #2:
- Add unit tests for grouping-layer field presence + default values
- Smoke a 5-class season generation; verify all classes emit grouping_pair_structure, grouping_season_id, grouping_layer_version
- Within-season consistency check: all 5 classes share same grouping_pair_structure
- Verify NO existing tests fail (additive change should preserve all baseline behavior)
- Verify canonical-four fields still emit (Stage 2 is additive, NOT replacement)

### Step 4 — MIGRATION.md entry (cross-seam contract per ADR-004)

Append to `reincarnated-engine/src/reincarnated/generation/MIGRATION.md`. Document:
- 3 new grouping-layer fields with semantics
- Per-season-id consistency contract
- Cross-seam consumers:
  - **Star-lord** (Stage 2 separate dispatch + future Stage 3 cipher migration): consumes grouping-layer data for per-season cosmological-vocabulary generation call; Stage 3 is when LLM sees grouping abstract labels instead of canonical-four
  - **Drax** (Stage 4 future work): consumes grouping-layer for per-embodiment narrative-skin rendering
  - **Gamora** (Stage 2-3 doppelganger validation): consumes grouping-layer for per-season mechanical-signature variance check

### Step 5 — Intermediate tag + AGENT_STATE + completion record

- Tag: `rocket/v1.3-form-bias-stage-2-grouping-layer`
- AGENT_STATE.md updated
- Completion record at bottom filled

## Cross-seam considerations

- **Star-lord**: PARALLEL — star-lord Stage 2 dispatch (`agentic_orchestration/dispatches/2026-05-16-star-lord-form-bias-stage-2-cosmological-vocabulary.md`) consumes grouping-layer fields; both Stage 2 dispatches run in parallel per cadence Option II Parallelized framing
- **Drax**: READ-ONLY future; Stage 4 work consumes grouping layer for per-embodiment narrative skin
- **Gamora**: READ-ONLY; doppelganger validation per cadence Option II
- **Gandalf**: design-lineage owner of pair-structure vocabulary — if cipher-width Outcome 2 spec doesn't fully define vocabulary, surface as finding
- **Knight-rider**: notify at completion; Stage 3 cipher migration dispatch authoring activates with both Stage 2 dispatches complete

## Out of scope (explicit)

- **NO canonical-four removals.** Stage 2 is purely additive; canonical-four remains operative
- **NO LLM prompt-construction changes.** Stage 3 is when LLM sees grouping abstract labels; this dispatch only adds the fields
- **NO display-layer changes.** Stage 4 work
- **NO new pair-structure vocabulary invention.** If spec is incomplete, surface to gandalf
- **NO non-humanoid embodiment grouping.** VS2a humanoid-only per prior scope decision
- **NO per-season vocabulary generation.** Star-lord Stage 2 separate dispatch
- **NO doppelganger validation.** Gamora separate dispatch territory

## Required reading

- `canonical/story/form-bias-cadence-strategy.md` § 7.2 + § 9.1 (Stage 2 framing + rocket cascade item)
- 2026-05-16 form-bias 5-entry batch (committed `5d51b5a`) — Entry 5 cadence Option II Stage 2 framing
- 2026-05-16 cipher-width resolution entry (committed `1dff66d`) — Outcome 2 architecture context (pair-structure spec)
- Your prior form-bias Stage 1 dispatch + completion record (pattern reference)
- `reincarnated-engine/src/reincarnated/generation/class_schema.py` + `class_generator.py` (target files)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #1 (math-before-code: pair-structure vocabulary is design-locked); #2 (smoke); #11 (attribution); #12 (semantic-shifting: new fields enable Stage 3 cipher migration; semantic shift); #14 (internal-vs-generative schema separation: Stage 2 prepares Stage 3 cipher migration which #14 enforces)

## Acceptance criteria

- [ ] 3 grouping-layer fields added to class schema with documented semantics
- [ ] Generator emits all 3 fields with per-season-id consistency
- [ ] Unit tests pass (existing + new grouping-layer tests)
- [ ] Smoke season verifies field presence + within-season consistency
- [ ] Canonical-four fields still emit (additive preservation verified)
- [ ] MIGRATION.md entry filed per ADR-004 cross-seam contract
- [ ] Intermediate tag `rocket/v1.3-form-bias-stage-2-grouping-layer` cut
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified at completion

## Tag policy

- **Intermediate tag:** `rocket/v1.3-form-bias-stage-2-grouping-layer` at the commit closing schema + generator + tests pass.
- **Milestone tag:** none from this dispatch.

---

## Completion record

**Completed:** 2026-05-16
**Intermediate tag:** `rocket/v1.3-form-bias-stage-2-grouping-layer` @ `03fb8cb`
**Pair-structure vocabulary source used:** PROVISIONAL — illustrative labels from dispatch § Step 1 (dispatch 2026-05-16-rocket-form-bias-stage-2-grouping-layer.md). See vocabulary-spec-gap finding below.
**Smoke status:** GREEN — 5-class season smoke with season_id; all 3 fields populated on all classes; within-season consistency confirmed; canonical-four fields still emit unchanged. 48 new tests pass. 427-test baseline (class_generation + embodiment_axis + movement_speed + energy_types + role_orientation + range_profile) green.
**MIGRATION.md path:** `reincarnated-engine/src/reincarnated/generation/MIGRATION.md`
**Notes for knight-rider:**

VOCABULARY-SPEC-GAP FINDING — action required before Stage 3:

After reading cipher-width Outcome 2 resolution (1dff66d) and canonical/story/form-bias-cadence-strategy.md § 7.2 per dispatch instructions, the concrete abstract pair-structure label vocabulary is NOT specified in either source. Specifically:
- 1dff66d resolves the grouping STRUCTURE (Outcome 2; classical-element-anchored; single fixed grouping; fire/water/earth/wind substrate) but does NOT enumerate abstract label strings per element
- Strategy doc § 7.2 describes the grouping layer as "Primary Opposition / Secondary Opposition slots — abstract labels" without specifying what those label strings are

Action taken: Built infrastructure using illustrative labels from dispatch as PROVISIONAL values (`_GROUPING_PAIR_STRUCTURE_LABELS` in class_generator.py). Labels are clearly flagged PROVISIONAL-PENDING-GANDALF in code comments and MIGRATION.md.

Required: Knight-rider must commission gandalf to specify the abstract pair-structure label vocabulary. Per dispatch: "do NOT invent vocabulary unilaterally." The provisional labels (`kinetic_aggression`, `fluid_adaptation`, `structural_resilience`, `evasive_velocity`, `raw_force`) are scaffolding ONLY — they must NOT be treated as design-locked vocabulary in Stage 3 LLM prompts.

When gandalf provides vocabulary:
1. Update `_GROUPING_PAIR_STRUCTURE_LABELS` in `reincarnated-engine/src/reincarnated/generation/class_generator.py`
2. Bump `GROUPING_LAYER_VERSION` from "v1.0" to "v1.1"
3. Add MIGRATION.md entry for the vocabulary update
4. Notify star-lord (Stage 2 sister dispatch) and drax

Per-seam-id consistency contract is otherwise mechanically correct: all classes in a season share identical grouping_pair_structure, grouping_season_id, and grouping_layer_version. Infrastructure is ready for Stage 3 cipher migration once vocabulary is confirmed.

This dispatch + star-lord Stage 2 both completing unblocks Stage 3 cipher-migration dispatch authoring. Star-lord Stage 2 is the parallel sister dispatch; its status determines the joint unblock condition.
