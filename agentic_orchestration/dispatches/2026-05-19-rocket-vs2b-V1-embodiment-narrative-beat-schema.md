# Dispatch — 2026-05-19 — rocket — VS2b V1 `embodiment_narrative_beat` schema field

**From:** knight-rider
**To:** rocket (generation seam — schema + generator hook OWNER)
**Approved by:** PRE-APPROVED in batch (Matt 2026-05-19 "approved, proceed with VS2A → VS2B"); fires at VS2b kickoff (VS2a L1 ship)
**Estimated effort:** ~2–3 days rocket
**Acceptance:** Per § Acceptance. Tag fires: `vs2b/v0.1-embodiment-narrative-beat-schema`.
**Hive context:** VS2b hive — activates when VS2a L1 ships. V1 is the schema foundation for V2 (LLM call orchestration) and V3 (drax loadout display).

---

## Context

Per `canonical/story/embodiment-display-loadout.md` § 15 "For rocket+star-lord" recommendation 1:

> Confirm `embodiment_narrative_beat` field placement (generative-side schema per Discipline #14)

The narrative beat is a ≤40-word concrete-sensory description of what the player IS this season (per spec § 1 + § 4). It's a per-class-per-season string that the LLM generates post-mechanical-convergence using the season's L3 cosmological vocabulary + the class's `embodiment_tag` + `embodiment_anatomy_tags` + `embodiment_action_register`.

V1 adds the field; V2 (star-lord) orchestrates the LLM call to fill it; V3 (drax) renders it in loadout.

---

## Required reading

In order:
1. `canonical/story/embodiment-display-loadout.md` (full spec; particularly § 1 strategic frame + § 4 visual structure + § 13 implementation cascade + § 15 recommendations)
2. `canonical/story/embodiment-narrative-layer.md` (architectural framing; embodiment_tag + embodiment_anatomy_tags + embodiment_action_register semantics)
3. `canonical/story/substrate-identity-declarations-2026-05-17.md` § 9.5 (substrate-identity surface dependency on pipeline; per-entity LLM naming preserves substrate-mode-of-action)
4. F1 dispatch + completion record (`agentic_orchestration/dispatches/2026-05-19-rocket-plus-star-lord-vs2a-geometry-type-schema.md`) — same two-stage migration pattern (additive-nullable → non-null post-backfill) applies
5. `reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` (your last checkpoint)
6. `reincarnated-engine/src/reincarnated/generation/MIGRATION.md` (existing migrations)
7. `reincarnated-engine/src/reincarnated/generation/season_orchestrator.py` (generator pipeline; insertion point for LLM call hook)
8. Past form-bias Stage 1+2+3 dispatch completion records (`2026-05-16-rocket-form-bias-stage-1-embodiment-axis.md`, etc.) — companion field patterns
9. `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#13a/#13b/#14 + P7)
10. `agentic_orchestration/hive-mind/scope-of-work-vs2b.md` § 2.1 (V1) + coordination matrix § 1

---

## Math-before-code (Discipline #1)

Authoring required before implementation:

### Schema design draft

**Path:** `reincarnated-engine/design/working-agreement/V1-embodiment-narrative-beat-schema-2026-05-19.md`

Captures:

1. **Field definition.** `embodiment_narrative_beat: str` — single string, ≤40 words, sensory + concrete (per spec § 1)
2. **Field placement.** On `PlayerClass` schema (per Discipline #14 generative-side) — same level as `embodiment_tag` + `embodiment_anatomy_tags`
3. **LLM call hook signature.** Function signature for the per-class beat-generation call (consumed by star-lord V2). Input: class manifest fields (`embodiment_tag`, `embodiment_anatomy_tags`, `embodiment_action_register`, `archetype_tag`, per-season cosmological vocabulary). Output: beat string.
4. **Generator pipeline integration point.** Where in `season_orchestrator.py` the LLM call invokes (post-mechanical-convergence; co-resident with Stage 2 cosmological-vocabulary pipeline per spec § 13 "Gated on Stage 2 cosmological-vocabulary ship")
5. **Two-stage migration.** Additive-nullable initially → non-null enforcement post-backfill. Identical pattern to F1 geometry_type.
6. **Validator** with Pattern-P7 fail-loud on missing beat post-enforcement
7. **Cross-references** to spec § 5 (naming surface) + § 6 (beat quality conventions) + § 7 (exemplars)

Star-lord reads this design doc before V2 dispatch fires.

---

## Cross-seam contract change? (Principle 6 gate)

**YES** — additive class manifest field consumed by export (star-lord V2) + loadout (drax V3).

**MIGRATION.md REQUIRED:**
- Rocket appends to `reincarnated-engine/src/reincarnated/generation/MIGRATION.md` (additive field + generator hook + two-stage enforcement)

**Round-trip smoke** is V2's responsibility (LLM call orchestration's end-to-end fixture); V1's smoke is schema-validation + generator-hook integration.

---

## Scope

- [ ] Schema design draft authored at `reincarnated-engine/design/working-agreement/V1-embodiment-narrative-beat-schema-2026-05-19.md`
- [ ] `embodiment_narrative_beat` field added to `PlayerClass` schema (additive + nullable initially)
- [ ] LLM call hook signature defined for V2 consumption (star-lord implements actual orchestration)
- [ ] Generator pipeline insertion point selected (`season_orchestrator.py` modification ready for V2 to consume hook)
- [ ] Validator updated: non-null `embodiment_narrative_beat` enforced post-backfill (two-stage migration)
- [ ] MIGRATION.md appended at generation seam
- [ ] Smoke-test GREEN
- [ ] AGENT_STATE.md updated
- [ ] Tag fire request surfaced: `vs2b/v0.1-embodiment-narrative-beat-schema`

---

## Acceptance criteria

- [ ] Design draft authored before any production code change
- [ ] Schema field operational + nullable initially; non-null enforcement deferred until V2 backfill completes
- [ ] LLM call hook signature documented; star-lord consumes for V2
- [ ] MIGRATION.md appended
- [ ] Smoke-test GREEN
- [ ] AGENT_STATE.md updated
- [ ] Hive log entry: rocket STATE on start + HANDOFF on completion (to star-lord V2)
- [ ] Tag: `vs2b/v0.1-embodiment-narrative-beat-schema`

---

## Out of scope

- LLM beat-generation call orchestration (V2 — star-lord)
- Drax loadout rendering (V3 — drax)
- chierit portrait pipeline (V3 + V4 territory)
- Demo-side embodiment surface (post-VS2b per spec § 14)
- Beat content quality judgment (gandalf authors beat-quality rubric per spec § 15 "For gandalf" item 2; not V1 scope)
- Beat regeneration UI (out of VS2b per spec § 14)
- Localization (post-Phase-0 per spec § 14)
- Per-skill or per-monster beats (out of scope; this field is per-class-per-season only)

---

## Open questions for rocket

- **Generator pipeline insertion point** — L1 rocket. Co-resident with Stage 2 cosmological-vocabulary pipeline (which already shipped 2026-05-16) is the natural seam. Document choice in design draft.
- **Field type** — `str` per spec; ≤40 words is a CONTENT convention, not a schema constraint. L1 rocket. (Schema validator does not enforce word count; gandalf beat-quality rubric handles content.)
- **Backfill strategy** — for 5 shipped seasons, V1's two-stage migration nullable phase covers; V2 backfill (LLM call per-class-per-season) generates beats post-V1 ship. Document explicitly.
- **Beat presence per season** — generator hook called once per class per season; the field is per-class-per-season, NOT per-shipping-instance. L1 rocket.
- **L3 vocabulary integration** — post-Stage-3 cipher migration (already shipped 2026-05-16); LLM beat generation consumes per-season L3 vocabulary per spec § 1. Document upstream Stage-3 dependency.

---

## References

- `canonical/story/embodiment-display-loadout.md` (spec; full)
- `canonical/story/embodiment-narrative-layer.md` (architectural framing)
- `canonical/story/substrate-identity-declarations-2026-05-17.md` § 9.5
- F1 dispatch (two-stage migration pattern reference)
- `reincarnated-engine/src/reincarnated/generation/MIGRATION.md`
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md`
- `agentic_orchestration/hive-mind/scope-of-work-vs2b.md` § 2.1

---

## Autonomous-operation authority + activation gate

**Activation gate:** VS2a L1 ships → VS2b kickoff. No additional upstream gate within VS2b.

**Post-activation:** rocket L1 within seam; no Matt-wait. Surface to gandalf via hive log only if spec ambiguity surfaces.

---

*Authored 2026-05-19 by knight-rider under pre-approval-batch authority. V1 adds the field; V2 fills it; V3 renders it; the player meets the form they are.*
