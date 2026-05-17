# Dispatch — 2026-05-16 — star-lord — Form-bias Stage 2: per-season cosmological-vocabulary generation call (VS2b S2; cadence Option II Stage 2)

**From:** knight-rider (authored per form-bias 5-entry batch Entry 5 cadence Option II Stage 2 + Matt 2026-05-16 Day 4 Tier 1 #4 confirmation)
**To:** star-lord
**Approved by:** Matt at 2026-05-16 Day 4 ("YES to all 4 Tier 1")
**Status:** PENDING — HOLD-on-prior. Do NOT execute until your in-flight fresh regen completes AND your queued cipher-migration paths-audit dispatch returns; star-lord can only run one dispatch per session. Sequence: regen → paths-audit → THIS.
**Estimated effort:** 1-2 sessions (~4-8h); per-season cosmological-vocabulary LLM call + integration with rocket's grouping-layer emit; MIGRATION.md per ADR-004.
**Acceptance:** Per-season cosmological-vocabulary generation call lands at LLM prompt-construction layer; consumes rocket Stage 2 grouping-layer fields (`grouping_pair_structure`, `grouping_season_id`, `grouping_layer_version`); emits per-season vocabulary that maps grouping pair-structure labels to per-season cosmological labels; smoke verifies generation; MIGRATION.md entry; intermediate tag.

---

## Context — Stage 2 of cadence Option II (star-lord half)

Per form-bias 5-entry batch (`5d51b5a`) Entry 5 cadence Option II + cipher-width Outcome 2 + per-season vocabulary coupling β (`1dff66d`):

> **Stage 2 — Per-season cosmological-vocabulary generation call integrated with grouping layer.** Star-lord emits an LLM call that generates per-season cosmological vocabulary mapping grouping pair-structure abstract labels to per-season concrete vocabulary (e.g., grouping label `"kinetic_aggression"` → season-N vocabulary `"solar fury"`). The per-season vocabulary becomes the LLM-visible vocabulary at Stage 3 cipher migration; at Stage 2, both vocabularies are present (canonical-four still primary; per-season vocabulary additive).

**Architectural context** (per cipher-width Outcome 2):
- Substrate layer = canonical-four (LLM still sees at Stage 2; hides at Stage 3)
- Grouping layer = abstract pair-structure (rocket Stage 2 emit; this dispatch consumes)
- **Vocabulary layer = per-season (THIS DISPATCH generates)**

Coupling β (per `1dff66d`) — per-season vocabulary is generated as in-prompt constraint at season-generation time; not pre-baked per-pair-structure (preserves per-season variation).

## What this dispatch does

### Step 1 — LLM call design (per-season cosmological-vocabulary generation)

In the LLM prompt-construction layer (likely `reincarnated-engine/src/reincarnated/llm/` or equivalent), add a per-season generation call that:

**Input:**
- Season-id (from regen orchestration)
- Grouping pair-structure mapping (from rocket Stage 2 schema field `grouping_pair_structure`)
- Cosmological-vocabulary generation prompt template (consult `canonical/story/form-bias-cadence-strategy.md` § 7.2 + cipher-width spec for the exact prompt shape; if not fully specified, surface to gandalf)

**Output:**
- Per-season cosmological vocabulary dict: keyed by grouping pair-structure label (e.g., `"kinetic_aggression"`); valued by per-season concrete vocabulary (e.g., `"solar fury"`)
- Vocabulary stored as part of season metadata (per-season artifact)

### Step 2 — Per-class consumption integration

Each generated class's `grouping_pair_structure` (rocket Stage 2 emit) gets resolved through the per-season cosmological vocabulary at LLM prompt-construction time for downstream LLM calls (skill name generation, lore text, etc.):

- Skill-name prompts continue to receive canonical-four labels (Stage 2 — Stage 3 hides canonical-four)
- Skill-name prompts ADDITIONALLY receive per-season cosmological vocabulary as in-prompt constraint
- This is the "both vocabularies present" Stage 2 state

### Step 3 — Schema additions for per-season vocabulary persistence

Add fields/storage for per-season cosmological vocabulary:

- Per-season metadata table or JSON artifact storing the vocabulary dict
- Per-class telemetry (if applicable) capturing which per-season vocabulary was used (Discipline #11 attribution)

Star-lord owns the storage decision per your seam conventions.

### Step 4 — Tests + smoke

Per Discipline #2:
- Unit tests for LLM call construction + response parsing
- Mock LLM smoke: verify per-season vocabulary dict generated for a test season; verify mapping shape correct (all grouping pair-structure keys present in output)
- Integration smoke: 5-class season generation invokes per-season cosmological-vocabulary call; per-class skill-name prompts receive both vocabularies; classes generate successfully

### Step 5 — MIGRATION.md entry

Append to `reincarnated-engine/src/reincarnated/export/MIGRATION.md` (or appropriate star-lord-owned MIGRATION):

- Per-season cosmological-vocabulary generation call introduced
- Schema additions for per-season vocabulary persistence
- Cross-seam consumers:
  - **Rocket** (READ-ONLY upstream): consumes rocket Stage 2 grouping-layer fields; rocket changes here require coordination
  - **Future Stage 3** (cipher migration): per-season vocabulary becomes LLM-visible primary; canonical-four hides; this dispatch's per-season vocabulary IS the cipher Stage 3 unlocks
  - **Drax** (Stage 4): per-season vocabulary surfaces in loadout/demo display (per-embodiment narrative skin)
  - **Gamora** (doppelganger validation): per-season cosmological vocabulary affects per-season mechanical-signature variance

### Step 6 — Intermediate tag + AGENT_STATE + completion record

- Tag: `star-lord/v1.3-form-bias-stage-2-cosmological-vocabulary`
- AGENT_STATE.md updated
- Completion record at bottom filled

## Cross-seam considerations

- **Rocket**: PARALLEL (Stage 2 sister dispatch); rocket Stage 2 grouping-layer emit is your input substrate; do NOT modify rocket files; coordinate via MIGRATION.md
- **Drax**: READ-ONLY future Stage 4 consumer
- **Gamora**: READ-ONLY; doppelganger validation
- **Gandalf**: design-lineage owner of per-season vocabulary generation prompt template — if spec is incomplete, surface as finding
- **Knight-rider**: notify at completion; Stage 3 cipher-migration dispatch authoring activates with both Stage 2 dispatches complete + paths-audit findings consumed

## Out of scope (explicit)

- **NO Stage 3 cipher migration.** Stage 3 hides canonical-four from LLM; this dispatch only ADDS per-season vocabulary as in-prompt constraint
- **NO canonical-four removals.** Stage 2 is purely additive
- **NO display-layer changes.** Stage 4 work
- **NO new vocabulary-generation-prompt invention.** If spec is incomplete, surface to gandalf
- **NO per-season vocabulary tuning beyond defaults.** Tuning is Matt-decision territory; this dispatch lands the mechanism

## Required reading

- `canonical/story/form-bias-cadence-strategy.md` § 7.2 + § 9.2 (Stage 2 framing + star-lord cascade item)
- 2026-05-16 form-bias 5-entry batch (committed `5d51b5a`) — Entry 5 cadence Option II Stage 2 framing
- 2026-05-16 cipher-width resolution entry (committed `1dff66d`) — per-season vocabulary coupling β (in-prompt constraint)
- Your prior cipher-migration paths-audit dispatch (`agentic_orchestration/dispatches/2026-05-16-star-lord-cipher-migration-paths-audit.md`) — findings inform Stage 3 dispatch authoring; awareness of paths is also useful here for Stage 2 mechanism design
- Rocket Stage 2 dispatch (`agentic_orchestration/dispatches/2026-05-16-rocket-form-bias-stage-2-grouping-layer.md`) — your input substrate contract
- `reincarnated-engine/src/reincarnated/llm/` (target files for LLM call construction)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #2 (smoke); #11 (attribution: per-season vocabulary used per class); #12 (semantic-shifting: per-season vocabulary becomes primary at Stage 3); #14 (internal-vs-generative schema separation: Stage 2 prepares cipher gate)

## Acceptance criteria

- [ ] Per-season cosmological-vocabulary LLM call constructed + integrated
- [ ] Rocket Stage 2 grouping-layer fields consumed correctly
- [ ] Per-season vocabulary persisted (storage decision per star-lord seam conventions)
- [ ] Per-class skill-name prompts receive both canonical-four + per-season vocabulary as in-prompt constraint
- [ ] Unit tests + mock-LLM smoke pass
- [ ] Integration smoke: 5-class season generation with per-season vocabulary works end-to-end
- [ ] MIGRATION.md entry filed per ADR-004
- [ ] Intermediate tag `star-lord/v1.3-form-bias-stage-2-cosmological-vocabulary` cut
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified at completion

## Tag policy

- **Intermediate tag:** `star-lord/v1.3-form-bias-stage-2-cosmological-vocabulary` at the commit closing LLM call + integration + tests pass.
- **Milestone tag:** none from this dispatch.

---

## Completion record

**Completed:** 2026-05-16
**Intermediate tag:** `star-lord/v1.3-form-bias-stage-2-cosmological-vocabulary` @ commit `5b0285b`
**Per-season vocabulary storage location:**
- `seasons/<id>/cosmological_vocabulary.json` — full per-season artifact (slot fills + rationale + attribution)
- `manifest.json["cosmological_vocabulary"]` — compact block (slot_fills + grouping_layer_version); null when LLM not available

**Mock-LLM smoke status:** PASSED — 53/53 `tests/test_cosmological_vocabulary.py` pass. Covers: PerSeasonVocabulary contract, prompt construction + anti-bias scaffolding, generate_cosmological_vocabulary() happy path + validation + fallback paths, prompt injection helper, naming function integration (mock LLM), SeasonOutput field presence.

**Integration smoke status:** PASSED (mock-LLM level) — `tests/test_naming.py` (16), `tests/test_export.py` (31), `tests/test_integration.py` (18): all pass. Backward compat verified (cosmological_vocabulary=None → no vocab line in prompt; identical behavior to pre-dispatch). Full 5-class season smoke with real LLM not run at dispatch time (requires ANTHROPIC_API_KEY; real regen is Matt-authorized batch scope).

**MIGRATION.md path:** `reincarnated-engine/src/reincarnated/export/MIGRATION.md` — "Form-bias Stage 2 — per-season cosmological vocabulary (2026-05-16)" section appended. Documents: three-layer architecture context, new/modified files, artifact schema, manifest vocabulary block, LLM cost note, retry/fallback behavior, backward compatibility, cross-seam consumer notes.

**Notes for knight-rider:**

1. **Stage 3 dispatch ready to author.** Both Stage 2 dispatches complete (rocket Stage 2 grouping-layer @ `rocket/v1.3-form-bias-stage-2-grouping-layer`; star-lord Stage 2 cosmological vocabulary @ `star-lord/v1.3-form-bias-stage-2-cosmological-vocabulary`) + paths-audit complete. Stage 3 scope is larger than originally planned — see `agentic_orchestration/research/cipher-migration-paths-audit-2026-05-16.md` Section 4 for full breakdown. Recommended decomposition: Stage 3a (engine-side: LLM prompt filters + export schema additions + manifest elements block) + Stage 3b (drax-side: gear display + resolver fallback hardening). Stage 3a is star-lord seam; Stage 3b is drax seam.

2. **Manifest version bump 1.3 → 1.4** is in the commit. Drax manifest consumers that use `manifest_version` for feature-gating should check `>= "1.4"` for cosmological_vocabulary presence. The `cosmological_vocabulary` block is `null` for pre-Stage-2 seasons.

3. **V2.4 telemetry migration is next on my queue.** Per dispatch context: "After this returns, your queue chain is: V2.4 telemetry migration. Then queue is empty." Awaiting V2.4 dispatch authoring via knight-rider per ADR-006 + dispatch trail requirements.

4. **Pre-existing gamora-seam test failures unchanged** (4 tests: test_different_seeds_vary, test_geared_player_deals_more_damage, test_cooldown_factor_applied_in_fight, test_weak_fit_against_impossible_opponent). Not caused by this dispatch. Route to gamora via knight-rider if not already queued.

5. **Rocket follow-on dispatch** (update `_GROUPING_PAIR_STRUCTURE_LABELS` from provisional → locked vocabulary per grouping-layer-vocabulary.md implementation handoff): the locked vocabulary IS already in class_generator.py (`commit ea3a1c3` / `rocket/v1.3-form-bias-stage-2-vocab-lock`). That dispatch is already complete per the message context. No action needed.

6. **Gandalf: prompt template spec is sufficient.** grouping-layer-vocabulary.md § "For star-lord" provided a complete prompt scaffold. No gaps surfaced. The anti-bias instruction (do not use fire/water/earth/wind/flame/ice/frost etc.) is in the system prompt. Open Question Q1 from the vocabulary doc (simultaneous vs sequential pair exposure): I defaulted to simultaneous exposure (all 5 slots + both pairs in one call per naming-triad.md § Q75 one-call-per-season pattern). Validate at Stage 3 gate if cross-pair interactions surface in early Stage-2 generation findings.
