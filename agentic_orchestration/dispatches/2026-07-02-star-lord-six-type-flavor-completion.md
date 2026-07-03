# Dispatch — 2026-07-02 — star-lord (+ gandalf curation) — six-type flavor completion (B3, Lane B)

**From:** knight-rider
**To:** star-lord (emission wiring) · gandalf (curation pass)
**Approved by:** Matt 2026-07-02 (relay §2 ruling 2 — all-six-types demo bundle, FULL LLM flavor; the one-realm §5.1 holds OVERRULED; ledger PART B — both emitters built+validated, wiring-only)
**Estimated effort:** 1–2 days (wiring + curation; the emitters exist)
**Acceptance:** the demo bundle carries **named, flavored content across all six types** — monsters, skills, gear, factions, weapons — LLM-generated then human-curated. No stub names ship.
**Status:** Lane B (sequence within lane — fires after B2 in the star-lord session; independent of B1). Gate-1 (jack-ryan DESIGN-MODE — cross-seam schema/flavor touch) required before execution. gandalf curation rides the same unit.

## Context

Matt ruled (relay §2 ruling 2): the demo bundle ships **all six content types with FULL LLM flavor** — the §5.1 "weapons/factions/gear held" position is overruled; both emitters are BUILT + validated, this is a **wiring-only** pass. The **D7 AI-tell line governs**: LLM generates, **we curate** — no raw model output ships unreviewed (the demo is judged on feel; a tell-y name is a feel break). Monster names/flavor are a HARD MUST (relay B3: "stubs unshippable"); skill `flavor_text`, gear names, and faction/weapon block wiring complete the set.

**Division of labor:** star-lord owns the emission wiring (call the existing generators, thread output into the bundle, validate). gandalf owns the curation pass (read the generated flavor, flag/fix tell-y or off-register output against the style-register; the curation is design-track, not a rewrite). The unit closes when both are done.

## Required reading before starting

- `canonical/current-to-end-state/current-to-end-state-serial-content-emission.md` PART B (the emitter state — built+validated, wiring-only) + D.1 gap queue
- `agentic_orchestration/gandalf/notes/2026-07-02-kr-relay-two-lane-fire-order.md` §2 ruling 2 (all-six-types, full LLM flavor) + §4 B3 row (AI-tell line)
- `canonical/reap-die-rise-story/style-register.md` (the register curation enforces — gandalf's authority)
- `src/reincarnated/export/one_realm_bundle_assembler.py` (where the six blocks thread into the bundle)
- `src/reincarnated/llm/` — the generators: `name_monster()` · `name_skill()` (skill `flavor_text`) · `name_gear_item()` (gear names — rides after B2 populates the pool) · `emit_faction_block()` · `emit_weapon_descriptor()` (weapon descriptor — ledger D.1 #4)
- `src/reincarnated/export/MIGRATION.md` (latest LOCKED entry — after B2's v1.84)

## Cross-seam contract change? (Principle 6 gate — YES)

Populates flavor fields drax's loader reads (monster names, skill flavor_text, gear names, faction/weapon blocks).
- `Round-trip: MIGRATION.md entry documenting the six-type flavor shape drax consumes; drax confirms the flavored bundle loads (names render, no stub-name fallbacks trip). Cross-seam contract → MIGRATION before tag (ADR-004).`

## Scope

- [ ] **Monster names/flavor (HARD MUST)** — wire `name_monster()`; every emitted monster carries a real name + flavor (no `monster_NNN` stubs)
- [ ] **Skill `flavor_text`** — wire `name_skill()` flavor_text into the skill blocks
- [ ] **Gear names** — wire `name_gear_item()` (consumes B2's populated gear pool; if B2 hasn't landed in-session, gate this sub-item on B2 and note it)
- [ ] **Faction block wiring** — `emit_faction_block()` threaded into the bundle
- [ ] **Weapon descriptor wiring** — `emit_weapon_descriptor()` (ledger D.1 #4)
- [ ] **gandalf curation pass** — read the generated flavor against the style-register; flag/fix tell-y or off-register output (D7 AI-tell line — LLM generates, we curate)
- [ ] `validate_bundle()` passes (all six blocks present + populated; III.7 clean; no telemetry keys)
- [ ] MIGRATION.md entry (six-type flavor shape)
- [ ] Empirically verify (Discipline #11): no stub-name fallbacks in the emitted bundle; sample-inspect flavor across all six types
- [ ] AGENT_STATE updated (star-lord)
- [ ] Tag: `star-lord/v-six-type-flavor-completion-1`

## Acceptance criteria

- [ ] All six content types carry named, flavored content in the bundle (no stubs)
- [ ] gandalf curation pass complete — flavor reads in-register, no AI-tell survivors
- [ ] validate_bundle passes; MIGRATION entry lands
- [ ] Round-trip: drax confirms the flavored bundle loads (names render)

## Out of scope (explicit non-goals)

- The demo EMISSION RUN (B4) — this wires flavor into the EXISTING season-001 bundle; B4 is the fresh gauntlet-passed run
- Proxy-T4 suite (B1) — independent
- v2 roster curation (B5)
- Re-generating the roster — flavor-completes what's emitted

## Quality criterion

**Game-quality goal:** the demo bundle reads like an authored game, not a stub-filled scaffold — every monster/skill/gear/faction/weapon carries a name a player would believe a human wrote. The six-type completeness is what lets store copy and the grimoire (D8) show real content.

**Refutation conditions (surface if any apply):**
- An emitter is NOT actually built/validated (relay claims wiring-only — if a generator needs real build work, surface; it's a scope change)
- Raw LLM output ships without curation (D7 AI-tell line violation — gandalf curation is mandatory, not optional)
- Gear naming blocks on B2 not having landed (note the dependency; don't emit stub gear names)
- Flavor contradicts the style-register or the reap-die-rise death-faith frame (gandalf catches at curation)
- A "name" is actually a tell-y template that reads as machine-generated (the demo exists to not tell that lie — §8)

## Open questions for the agent to resolve (document; escalate to KR)

- Whether gear naming can complete in THIS pass or genuinely gates on B2's populated pool (default: gate the gear sub-item on B2; the other five types don't)
- Curation depth: full read vs. sampled spot-check per type (gandalf's call — bias toward full for monsters/skills, the high-count surfaces)

## References

- serial-emission ledger PART B + D.1 #4 · relay §2 ruling 2 + §4 B3 (AI-tell line) · style-register
- MASTER: `2026-07-02-one-realm-mvp-build-MASTER.md` (Lane B)
