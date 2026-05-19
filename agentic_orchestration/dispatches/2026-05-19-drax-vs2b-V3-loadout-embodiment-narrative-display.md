# Dispatch — 2026-05-19 — drax — VS2b V3 loadout embodiment-narrative display surface

**From:** knight-rider
**To:** drax (presentation seam — loadout-first embodiment display OWNER)
**Approved by:** PRE-APPROVED in batch (Matt 2026-05-19); fires when V1 + V2 + V4 land
**Estimated effort:** ~1–1.5 weeks drax (per spec § 13 estimate: scaffolding 2-3 days + engine integration 1-2 days + polish 2 days + chierit tooling 1 day)
**Acceptance:** Per § Acceptance. Tag fires: `vs2b/v0.3-loadout-embodiment-display-shipped`.
**Hive context:** VS2b hive — V3 is the player-facing surface for VS2b substrate-realignment work. Loadout-first (per gandalf spec); demo-side embodiment is post-VS2b.

---

## Context

Per `canonical/story/embodiment-display-loadout.md` § 15 "For drax (when dispatch lands)":

> 1. Read this spec end-to-end before scaffolding
> 2. Call back on § 12 open questions before locking visual conventions
> 3. Build component scaffolding against mocked beat content until `embodiment_narrative_beat` field ships
> 4. Surface any spec ambiguity to gandalf via knight-rider (not improvise)

V3 implements the per-class header surface that lets non-humanoid embodiment become a real player experience in VS2b. Diablo III class-select screen is canonical reference (portrait + voice-line + one paragraph); Reincarnated extends with per-season variation + embodiment-revealing language.

---

## Required reading

In order:
1. `canonical/story/embodiment-display-loadout.md` — END TO END (per spec § 15 "For drax" recommendation 1). Particularly:
   - § 1 strategic frame
   - § 4 visual structure
   - § 5 naming surface (anchor → spirit name → embodiment-flavored name)
   - § 6 beat-quality conventions
   - § 7 exemplar beats
   - § 8 mobile responsiveness
   - § 9 accessibility
   - § 10 typography
   - § 11 component composition
   - § 12 open questions (call back on these BEFORE locking visual conventions)
   - § 13 implementation cascade (your work breakdown)
2. V1 dispatch + completion record (schema field definition)
3. V2 dispatch + completion record (export packet emission shape)
4. V4 dispatch + completion record (chierit element-reconciliation; slot assignments locked)
5. `canonical/story/cosmology-reincarnated.md` (Wheel / Earth Self / seasonal descent — conceptual layer this surface surfaces)
6. `canonical/story/court-of-forms.md` (Court framing + dual-label pattern C8)
7. `canonical/story/naming-triad.md` (display structure)
8. `canonical/story/style-register.md` (HD-2D-shaped pixel-art register)
9. `reincarnated-loadout/AGENT_STATE.md` (your last checkpoint)
10. `reincarnated-loadout/src/` (existing class-related surfaces; existing typography/responsive patterns)
11. F4 dispatch + drax B6 skill-tree UI design dispatch (sibling visual surface pattern; co-locates with class-header)
12. `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## Scope

### Component scaffolding (per spec § 13 immediate, no engine dependency)

- [ ] Class-header component scaffolded in `reincarnated-loadout/src/` per spec § 4 visual structure + § 11 component composition
- [ ] Placeholder portrait + placeholder beat (mocked) until V1 + V2 ship; component renders against mock data first
- [ ] Typography exploration per spec § 10 + HD-2D register
- [ ] Mobile responsiveness implementation per spec § 8 (portrait + landscape + tablet + desktop)
- [ ] chierit portrait crop tooling: idle-frame extraction → 96×96 crop (per spec § 13 + V4 element reconciliation locks slot assignments)

### Engine integration (gated on V1 + V2)

- [ ] Consume `embodiment_narrative_beat` field from export packet (replaces mock)
- [ ] Spirit name display per spec § 5 (consumes Stage 2 cosmological-vocabulary — already shipped)
- [ ] Beat content rendering: canonical-four labels fully hidden per Stage 3 cipher migration (already shipped)
- [ ] L3 per-season vocabulary present in beat content

### Polish + accessibility

- [ ] Mobile tuning per spec § 8 + § 9
- [ ] Accessibility per spec § 9 (screen-reader + contrast + focus management)
- [ ] Visual smoke screenshot captured (drax direct capture per galadriel sub-agent restriction in effect)
- [ ] AGENT_STATE.md updated

### Spec § 12 open-questions resolution

- [ ] Read spec § 12 open questions; route to gandalf via hive log for any spec ambiguity (per spec § 15 "For drax" recommendation 4 — surface, do NOT improvise)

---

## Cross-seam contract change? (Principle 6 gate)

**Consumer-side; drax-internal contract.** No new cross-seam contract change (V1 + V2 carried producing-side contracts).

**MIGRATION.md** at `reincarnated-loadout/MIGRATION.md` if drax-internal contracts shift (component API; data shape between scaffolding + engine integration phases). L1 drax decision.

**Round-trip smoke**: end-to-end fixture — season load → manifest read → V1 field present → V2 LLM beat present → drax loadout renders → screenshot capture. Field-presence + canonical-four-leak check.

---

## Acceptance criteria

- [ ] Spec read end-to-end before scaffolding (drax surfaces in hive log STATE entry)
- [ ] § 12 open questions resolved via gandalf hive log routing
- [ ] Class-header component scaffolded; placeholder data rendering
- [ ] V1 + V2 + V4 integration: beat from export packet; chierit portrait per V4 slot assignment
- [ ] Mobile + desktop responsive validated
- [ ] Accessibility per spec § 9
- [ ] Visual smoke screenshot captured (gandalf register-coherence review via hive log)
- [ ] Round-trip smoke
- [ ] AGENT_STATE.md updated
- [ ] Hive log: STATE on scaffolding start + REQUEST entries to gandalf for § 12 open questions + STATE on engine integration + STATE on completion
- [ ] Tag: `vs2b/v0.3-loadout-embodiment-display-shipped`

---

## Out of scope

- V1 schema field (rocket; upstream)
- V2 LLM beat generation (star-lord; upstream)
- V4 chierit reconciliation (gandalf; upstream)
- Demo-side embodiment surface (post-VS2b per spec § 14)
- Spirit Guide voice surface (separate doc + dispatch territory)
- Trial/Mirror/Passage ritual moment displays (separate canonical docs; post-VS2b)
- Build-coach verdicts (Stage A7 territory)
- Season-roster overview / Court of Forms canvas (separate surface; post-VS2b)
- Beat regeneration UI (out per spec § 14)
- Audio voice-line for beats (per `audio-strategy-phase0.md`; Phase 1+)
- Localization (post-Phase-0)

---

## Open questions for drax

- **Spec § 12 open questions** — route to gandalf via hive log; do NOT improvise (spec § 15 "For drax" item 4)
- **chierit portrait crop convention** — 96×96 per spec § 13; locked
- **Mock-to-live transition** — L1 drax. Component remains stable across mock/live data swap; design API to be data-source-agnostic
- **Per-class layout consistency** — per spec § 4; document deviations if any per archetype
- **F4 skill-tree co-location** — V3 class-header sits adjacent to F4 skill-tree UI in loadout layout. L1 drax decides layout composition (vertical stack vs side-by-side vs tabs)
- **Loadout vs demo surface differentiation** — spec is loadout-only for V3; demo-side embodiment is post-VS2b. Confirm no V3 work touches demo (per scope discipline).

---

## References

- `canonical/story/embodiment-display-loadout.md` (spec; FULL)
- V1 + V2 + V4 dispatches (upstream)
- `canonical/story/cosmology-reincarnated.md` + `court-of-forms.md` + `naming-triad.md` + `style-register.md`
- F4 dispatch (sibling surface; B6 skill-tree UI)
- `reincarnated-loadout/AGENT_STATE.md`
- `agentic_orchestration/hive-mind/scope-of-work-vs2b.md` § 2.3 (V3)
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## Autonomous-operation authority + activation gate

**Activation gate:** V1 + V2 + V4 land (schema field + LLM beat + chierit slot assignments all operational).

**Post-activation:** drax L1 within seam; gandalf consult on spec § 12 open questions + visual-register coherence review. No Matt-wait.

---

*Authored 2026-05-19 by knight-rider under pre-approval-batch authority. V3 is the surface where the player meets their form. The story does the work; the body follows later. Diablo III reference; Reincarnated extension; per-season variation.*
