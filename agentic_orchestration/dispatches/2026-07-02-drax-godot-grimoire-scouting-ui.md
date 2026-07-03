# Dispatch — 2026-07-02 — drax — grimoire + scouting UI, minimal (D8)

**From:** knight-rider
**To:** drax
**Approved by:** Matt 2026-07-02 (one-realm §6.5)
**Estimated effort:** 2–4 days
**Acceptance:** minimal grimoire (visibly numbered pages, "page N of 400+") + scouting glyph preview at the Goldilocks fork, consuming the III.8 label→glyph mapping.
**Status:** FIRES against bundle-v1 (`star-lord/v-one-realm-bundle-LOCKED-2` @ `08e6f24`) — D4 CLOSED. PARALLEL-SAFE (UI-independent of the combat path); can fire alongside D5/D6. **D8 gear rider (relay §4):** build against the 11-slot `gear_representative` schema NOW; consume the populated gear pool when Lane B2 (gear pass) lands — a mid-wave data swap, non-blocking. **bundle-v1 is the development bridge** (relay §1). Gate-1 (jack-ryan + gandalf grimoire-fantasy) required.

## Context

§6.5 + §4: "Grimoire + scouting UI, minimal (numbered pages; glyph preview)." This is how a 10-kit demo carries a 400-kit hook honestly (§4, §20a/§20c): the **grimoire-as-record with visibly numbered pages** ("page N of 400+") + **scouting glyphs previewing archetypes the demo never spawns** — cheap, showable, honest gestures that make the scale claim credible without shipping the scale. The glyphs consume the engine's III.8 **label→glyph mapping** (MVP-CRITICAL), which maps presentation vocabulary to emergent clusters (Discipline #41 — does NOT pre-impose a taxonomy). `archetype_tag` + `role_orientation` are already emitted; the mapping bridges engine labels (fire_mage, hunter) to the doc's glyph vocabulary (glass cannon / bruiser / controller).

## Required reading before starting

- `canonical/reap-die-rise-game/one-realm-mvp-scope.md` §4 (grimoire numbered pages + scouting glyphs, MVP-critical), §6.5, §8 (§20c legibility compression — what the demo validates)
- `current-to-end-state-engine.md` III.8 (the label→glyph mapping — MVP-CRITICAL; `archetype_tag`+`role_orientation` already surfaced in the demo UI; needs the mapping, not new generation; Discipline #41 respected)
- `canonical/reap-die-rise-story/` grimoire/summoning fantasy sections (story-tracker A11 — claimed souls usable/summonable; the grimoire IS a summoning fantasy)
- D4 loader (the grimoire reads bundle records for page content + glyph inputs)

## Cross-seam contract change? (Principle 6 gate)

Consumes existing emitted fields (`archetype_tag`, `role_orientation`) via a presentation-side label→glyph mapping. The mapping is a presentation artifact (Discipline #41 — maps to emergent clusters, no pre-imposed taxonomy).
- `Round-trip: not applicable — consumes already-emitted archetype_tag/role_orientation via a presentation-side mapping; no engine schema change. If the mapping reveals a missing emitted field, flag to star-lord/rocket (do not invent Godot-side).`

## Scope

- [ ] Minimal grimoire UI: visibly numbered pages, "page N of 400+" (the honest scale gesture)
- [ ] Scouting glyph preview at the Goldilocks fork (§1 Structure-1 lieutenant fork)
- [ ] Consume the III.8 label→glyph mapping (engine labels → glyph vocabulary; Discipline #41 — no pre-imposed taxonomy)
- [ ] Glyphs preview archetypes the demo never spawns (the honest 400-hook gesture, §4)
- [ ] Min-spec check per D10
- [ ] AGENT_STATE updated
- [ ] Tag: `drax/v-godot-grimoire-scouting-ui-1`

## Acceptance criteria

- [ ] Grimoire shows numbered pages ("page N of 400+") — the scale claim gesture
- [ ] Scouting glyphs preview at the fork, driven by the III.8 label→glyph mapping
- [ ] The mapping respects Discipline #41 (presentation vocabulary → emergent clusters; no taxonomy pre-imposed)
- [ ] Glyphs legibly compress archetype identity (§20c — the demo validates legibility compression)

## Out of scope (explicit non-goals)

- Full grimoire depth / temporal summoning (§13, launch) / spawn-influence economy (§12, launch)
- Vendor economy / hand-in consequences beyond one reaction line (§4 STUBBED)
- New generation or new emitted fields (consume what's emitted; flag gaps, don't invent)
- The full 400-page content (numbered pages is a *gesture*, not 400 authored pages)

## Quality criterion

**Game-quality goal:** a 10-kit demo makes the 400-kit promise honestly — numbered grimoire pages + scouting glyphs are the cheap, showable, honest gestures (§4, §20a/§20c) that let store copy claim scale credibly.

**Refutation conditions (surface if any apply):**
- The label→glyph mapping pre-imposes a taxonomy (Discipline #41 violation — glyphs must map to emergent clusters)
- Numbered pages imply content the demo can't back (dishonest gesture — the pages are a scale *claim* rendered, not a promise of 400 playable pages in-demo)
- Glyphs are illegible (§20c legibility compression failing — this is a thing the demo validates)
- The grimoire fantasy contradicts the story-side summoning register (A11)

## Open questions for the agent to resolve (document)

- Glyph visual vocabulary (coordinate with gandalf/galadriel register + the III.8 mapping)
- Whether the label→glyph mapping is authored Godot-side or needs an engine-side manifest (flag to star-lord if the latter)

## References

- one-realm-mvp-scope.md §4/§6.5/§8 · current-to-end-state-engine.md III.8 · reap-die-rise-story A11
- MASTER: `2026-07-02-one-realm-mvp-build-MASTER.md`
