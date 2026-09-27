# Dispatch — 2026-09-26 — drax — C-9: cathedral grey room on the Crucible arena

**From:** Matt's session (drafted with Claude, standing in for knight-rider)
**To:** drax
**Approved by:** Matt, 2026-09-26: *"Ok, go."*
**Estimated effort:** one session.
**Acceptance:** Matt sees and approves the grey room **before any painting** (R-C3-55a).

## Context

Run C-9 tests a challenger register (ART-1 "Illuminated Archive"). One of its two scenes is a **cathedral built on the EoR/Crucible arena footprint**. The grey room runs in parallel with gandalf's style gate so it is ready when Matt rules GO. The EoR Warlord *character* is dropped, but **the arena geometry stays**. R-KP-0c already makes the arena a swappable data object, so this cathedral should drop into the KC2-PLAY runtime as a skin over the same walkable geometry.

## Required reading

1. `matt_notes_handoff_docs/rdr-art-illuminated-archive-brief.md` § 4 (scene conventions): full-bleed crop; near side cut low (or a dissolvable near layer); back walls exit the frame; seams hide in dead space; **walkable = brightest and calmest**.
2. `matt_notes_handoff_docs/rdr-art-illuminated-archive-refs/README.md`: the arena→cathedral mapping table.
3. `…/cathedral-plan/antwerp-cathedral-grundriss.jpg` (the plan); `…/cathedral-look-alt/spinola-hours-f185-office-of-the-dead.jpg` (vault and height reference only).
4. `agentic_orchestration/galadriel/notes/crucible-arena-geometry-v1.json`: 177-vertex ring, 4 islands, 2 unwalked arcs, 6 green zones. **Ignore the file's own `scale` block** (superseded, WARN-8). **Use KC2-PLAY's registered `u = 0.285`** (KP-6, ratified KP-9) → about 57.3 × 76.7 m.
5. `canonical/reap-die-rise-game/painted-2d-pipeline/scene-builder-workflow.md` § 3 rows 1–2: grey-room conventions, organic rules, walkable clip.

## The mapping

| Arena feature | Cathedral element |
|---|---|
| North corridor + red door (spawn) | Entry through the choir screen into the crossing |
| Central oval | The crossing under the lantern: the brightest floor |
| NW / NE lobes | The transept arms |
| Two long thin E/W interior walls | Choir stalls |
| SW / S / SE lobes; the two small S islands | Ambulatory chapels; the altar and a tomb |
| Six green DoT zones | Rot-soaked chapel floor. **Enterable. Never pits, never collision.** |

## Scope

- [ ] Orthographic canvas at the ratified camera (yaw 47°, pitch 52.95°); Keeper scale 130 px at 1080p. Canvas size: your call, sized to the arena at `u = 0.285`.
- [ ] Deliverables, as for the cliffside v4 grey room: flat-shaded guide, depth map (uint16 mm), ID mask, walkable mask (clipped inside the canvas), **plus a separate DoT-zone mask** for the six green zones. The zones ship as interior points with radius upper bounds, not outlines: derive discs, and record that as provenance.
- [ ] Brief § 4 conventions applied: near-side walls cut at knee height (or authored as a separate near layer); back walls exit the top edge; no void or border anywhere (**full-bleed: this interior has no sky**).
- [ ] Chunk grid for painting (1536×1024 with 256 px overlaps, as in C-3), with seams placed in dead space where possible.
- [ ] Review image for Matt: the grey room beside the arena trace, with the mapping labelled.
- [ ] AGENT_STATE.md updated.

**Round-trip: not applicable.** No engine contract changes. If the walkable mask is later swapped into the KC2-PLAY runtime, that swap is a separate dispatch.

## Push

Commit as work lands. **No push without Matt's word.** This is not KC2-PLAY work, so that run's `reincarnated-godot` push extension does not cover it.
