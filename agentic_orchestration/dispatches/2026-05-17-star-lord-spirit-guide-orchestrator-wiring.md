# 2026-05-17 — star-lord — Spirit Guide orchestrator wiring (D15 follow-on)

**Authority:** Matt L3 standing delegation (sign-off pillar — "always toward Phase-1 completion").
**Type:** Pattern A — ~0.5 day.
**Predecessor:** star-lord D15 (`star-lord/v1.3-d15-llm-flavor-diversifier-1` @ `5ead304`); star-lord v1.4 telemetry schema (`star-lord/v1.4-perception-asymmetry-telemetry-schema-1` @ `0fce61a`).

---

## Why this matters

D15 shipped `build_spirit_guide_prompt()` — the Court-aware Spirit Guide referencing engine. **It's authored + tested but NOT YET CALLED from `season_orchestrator.py`.** Capability exists; orchestration call site doesn't. This dispatch closes that gap so substrate-coherent Spirit Guide voice actually reaches the consumers.

---

## Required reading

1. `reincarnated-engine/src/reincarnated/llm/spirit_guide_voice.py` — your D15 ship; `build_spirit_guide_prompt()` is the entry point you'll wire in
2. `reincarnated-engine/src/reincarnated/export/season_orchestrator.py` (or wherever the orchestrator lives) — current state; identify where Spirit Guide calls should fire
3. `agentic_orchestration/hive-mind/phase-1-p1-log.md` — your D15 ship STATE entry context

---

## Scope

### Item 1 — Identify orchestrator call sites

- Locate `season_orchestrator.py` (engine-side season generation pipeline)
- Identify which generation steps SHOULD produce Spirit Guide dialogue:
  - Class introduction (when a new class is generated; Spirit Guide may comment)
  - Anchor revelation (when season anchor is established)
  - Court-form ascension (when a form is added to Court)
  - Any other narrative beat where Spirit Guide voice contextualizes
- Document the integration points

### Item 2 — Wire `build_spirit_guide_prompt()` into orchestrator

For each integration point identified:
- Call `build_spirit_guide_prompt()` with appropriate parameters (substrate_identity from class, court state if available, current season number)
- Capture the LLM response (text)
- Store in season output (probably as `spirit_guide_voice` field in season metadata or per-class data)
- Discipline #11 attribution: include `engine_git_sha` in any persisted Spirit Guide voice for later debugging

### Item 3 — Token budget verification

Per D15 ship analysis: combined D6+D15 delta ≈ $0.09-0.12/regen above baseline. Verify orchestrator-side budget calls fall within this envelope. Surface any unexpected token-cost spikes as OBSERVATION.

### Item 4 — Tests

- Unit test: orchestrator calls Spirit Guide builder at expected integration points
- Integration test: a full season regen produces Spirit Guide voice in season metadata (or wherever it lives)
- Empty-court case: first-season generation handles empty court without crashing (D15 spec)

### Item 5 — MIGRATION.md + hive log

- `export/MIGRATION.md` entry documenting orchestrator wiring landed
- Hive-log STATE + HANDOFF → drax-loadout (if Spirit Guide voice surfaces in loadout's Court browser eventually) + HANDOFF → drax-demo (if Spirit Guide dialogue surfaces in demo gameplay)
- Tag `star-lord/v1.5-spirit-guide-orchestrator-wiring-1`

---

## Out of scope (DO NOT)

- ❌ DO NOT modify `spirit_guide_voice.py` (D15 already authored + tested)
- ❌ DO NOT touch simulation, demo, or loadout files
- ❌ DO NOT add new event types (telemetry stays at v2.5)
- ❌ DO NOT redesign orchestrator structure; wire calls only

---

## Acceptance criteria

- [ ] Orchestrator call sites identified + documented
- [ ] `build_spirit_guide_prompt()` wired into orchestrator at integration points
- [ ] Spirit Guide voice persisted in season output
- [ ] Token budget remains within $0.09-0.12/regen envelope
- [ ] Tests added (unit + integration)
- [ ] `export/MIGRATION.md` entry
- [ ] Hive-log STATE + HANDOFFs
- [ ] Tag `star-lord/v1.5-spirit-guide-orchestrator-wiring-1`

---

## Smoke test

- Run a fresh season regen
- Inspect season output for Spirit Guide voice content
- Verify substrate-coherent prose (fire classes have fire-themed Spirit Guide commentary; etc.)
- Token cost within envelope

---

*Dispatched 2026-05-17 by knight-rider per Matt sign-off pillar. ~0.5 day. Append completion record when done.*

---

## Completion record

**Completed:** 2026-05-17 by star-lord.
**Engine commit:** `5cc0a13`
**Tag:** `star-lord/v1.5-spirit-guide-orchestrator-wiring-1` @ `5cc0a13`

### Acceptance criteria — all met

- [x] Orchestrator call sites identified + documented (3 moments: anchor_revelation, class_introductions, ascension_threshold)
- [x] `build_spirit_guide_prompt()` wired into orchestrator at all three integration points
- [x] Spirit Guide voice persisted in `SeasonOutput.spirit_guide_voice` + written to `spirit_guide_voice.json`
- [x] Token budget within $0.09-0.12/regen envelope: ~$0.048 for N=10 classes (12 calls x ~$0.004)
- [x] 13 new tests GREEN in `tests/test_spirit_guide_orchestrator_wiring.py` (unit + integration + resilience)
- [x] `export/MIGRATION.md` v1.3 entry authored
- [x] Hive-log STATE + HANDOFF entries appended
- [x] Tag `star-lord/v1.5-spirit-guide-orchestrator-wiring-1` cut

### Files modified

- `src/reincarnated/generation/season_orchestrator.py` — wiring + new params + `_generate_spirit_guide_voice()` method
- `src/reincarnated/output/season_writer.py` — `spirit_guide_voice.json` write
- `src/reincarnated/export/MIGRATION.md` — v1.3 entry
- `src/reincarnated/export/AGENT_STATE.md` — session record
- `tests/test_spirit_guide_orchestrator_wiring.py` — 13 new tests

### Design decisions made during execution

1. **Integration point selection**: Three moments chosen — `anchor_revelation` (pre-descent; season-level context), `class_introductions` (per-class; substrate-specific), `ascension_threshold` (threshold; no substrate — season-level moment). Fired after `_name_everything()` so class names are available for Guide prompts.

2. **moment_type mapping**: All three use valid moment_type values from the `build_spirit_guide_prompt()` spec (`general_presence` for anchor + class, `ascension_threshold` for the threshold moment). Journey notes provide context for each call.

3. **Substrate resolution**: `foundation.get_element(element_name).identity` — returns `None` for `physical` (non-rotating) element, which is correct. `build_spirit_guide_prompt()` handles `substrate_identity=None` gracefully (no substrate context block in prompt).

4. **Warn-and-continue**: Individual LLM failures log at WARNING and omit the key from result. Season generation never fails due to Spirit Guide voice failure. Empty result dict is valid.

5. **Token cost**: 12 calls (1 anchor + 10 classes + 1 ascension) x ~$0.004 = ~$0.048. Within envelope.
