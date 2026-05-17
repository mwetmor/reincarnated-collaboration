# Request — drax chierit-composite scale-inspection strip (companion to monster composite)

**From:** knight-rider (drafted at Matt's directive 2026-05-16 Day 4 close: "author the gandalf request file for chierit composite too")
**To:** knight-rider (for drax dispatch authoring)
**Date:** 2026-05-16 (Day 4 close)
**Authored in:** gandalf request channel as extension to gandalf's `2026-05-16-drax-monster-scale-screenshot-strip.md` commission
**Authorized by:** Matt at 2026-05-16 Day 4 (extending original directive: "Please ship 11 monsters at the 3 scales and also 11 characters")
**Type:** Visual-inspection artifact generation; small follow-on dispatch
**Estimated effort:** ~1 hour drax (harness exists; layout mirror of monster composite)

---

## Why this request exists

Gandalf's original commission (`2026-05-16-drax-monster-scale-screenshot-strip.md`) scoped chierit characters as the REFERENCE (single scale, anchor for monster comparison) rather than as a VARIABLE being tuned. That framing serves gandalf's monster-side analysis well.

**Matt's directive at Day 4 close extends scope:** chierit character scale also needs tuning. The standing chierit-scale-tuning item (carried since Day 3) has not been resolved. The 80-100 px HD-2D target gandalf identified applies to player characters too — and the current chierit scale (0.35) renders at ~100×45 px, which may or may not be the right anchor.

Drax's v0.20.1 work already produced three chierit grid PNGs at scales 0.25 / 0.35 / 0.45 (separated by scale, not composited). This commission asks for a SINGLE composite mirroring the gandalf monster composite format so the same ratio-judgment ergonomics apply.

---

## What drax produces

A **single composite PNG** showing all 11 chierit-track characters (10 chierit Elementals + 1 GandalfHardcore Samurai) at three scale candidates side-by-side.

### Image layout

```
                     SCALE 0.25         SCALE 0.35         SCALE 0.45
                  ┌────────────┐    ┌────────────┐    ┌────────────┐
  [HD-2D TARGET]  │ fire-      │    │ fire-      │    │ fire-      │
   80-100 px      │ knight     │    │ knight     │    │ knight     │
   reference      │ (fire)     │    │ (fire)     │    │ (fire)     │
   band           │ XXX px     │    │ XXX px     │    │ XXX px     │
                  └────────────┘    └────────────┘    └────────────┘
                  ... (11 rows total, one per chierit character)
```

### Required elements per row

- **Character name** above the three scale thumbnails (e.g., "fire-knight", "water-priestess", "GandalfHardcore-samurai")
- **Element label** below character name (e.g., "fire" / "water" / "earth" / "wind" / "ice" / "light" / "shadow" / "lightning" / "metal" / "nature" / "physical" — per the chierit ELEMENT mapping in `characterSprites.ts`)
- **Rendered pixel height numeric** below each thumbnail (e.g., "@ 0.25 → 72 px tall"; "@ 0.35 → 100 px tall"; "@ 0.45 → 130 px tall") — measured feet-to-top-of-head (excluding hair/hat protrusions if practical; otherwise full bounding box)

### Reference overlay (replaces player-ref column from monster composite)

Because chierit IS the player character (no smaller "player" anchor exists), the reference for character-scale judgment is the **HD-2D pixel-art register target band**:

- Render a faint horizontal band or pair of guidelines spanning the 80-100 px height zone, anchored at the same ground-level baseline as the character sprites
- Label: "HD-2D target: 80-100 px (per gandalf canonical-element register; Sea of Stars / Octopath Traveler / Eiyuden Chronicle baseline)"
- This lets gandalf scan top-to-bottom and verify which scale lands each character cleanly inside the band

### Constraints (mirror monster composite spec)

- **Neutral background** — same single muted color used in monster composite (slate grey or off-white)
- **Same camera distance for all three scale candidates** — only the character scale value varies
- **Idle animation frame** — first frame of idle anim for each character
- **No combat VFX** in frame
- **All 11 characters in one image** — single PNG/JPG; rows stacked vertically; ≤ 2MB

### Sorting order

Order rows by element family (lets gandalf judge whether scale should vary by element archetype):
1. Physical / kinetic (metal-bladekeeper)
2. Fire (fire-knight)
3. Water (water-priestess)
4. Earth / ground (ground-monk)
5. Wind (wind-hashashin)
6. Ice / crystal (crystal-mauler)
7. Light (light-valkyrie)
8. Shadow (shadow-stalker)
9. Lightning (lightning-ronin)
10. Nature / leaf (leaf-ranger)
11. GandalfHardcore-samurai (placed last; note: portrait-only, no animation sheets — see "Samurai handling" below)

(Element family order matches the canonical-element substrate; not load-bearing for the composite's purpose but consistent with the cosmology.)

### Samurai handling

Drax's v0.20.1 noted GandalfHardcore Samurai is portrait-only (640×640) with no animation sheets. Two options:
- **(a) Include as-is** — render the 640×640 portrait at three scales (0.25 / 0.35 / 0.45) so gandalf sees the scale comparison against the chierit sprites. Acknowledge in the per-row label: "(portrait only; no anim sheets)".
- **(b) Omit Samurai from this composite** — 11 → 10 rows; document omission in companion notes file as "Samurai deferred until animation sheets are sourced; see P6.d character-track sub-commission."

Drax picks based on artifact ergonomics; either is acceptable. If (a), the scale candidates may need to differ for Samurai (640×640 source vs 288×128 chierit source) — drax may choose narrower Samurai-only candidates and label them differently.

---

## Output location

Save the composite image at:
`agentic_orchestration/gandalf/findings/2026-05-16-chierit-character-scale-inspection-strip.png`

Companion notes file at:
`agentic_orchestration/gandalf/findings/2026-05-16-chierit-character-scale-inspection-strip-notes.md`

Notes content:
- chierit intrinsic source-sheet pixel size (288×128 per drax's prior empirical confirmation) — confirm and extend per-character if any deviation
- Current chierit scale (0.35) explanation — what rendered pixel height does this currently produce
- Samurai handling decision (option a or b above) + rationale
- Any rendering anomalies (e.g., "ground-monk idle frame has anchor offset that visually misaligns against the HD-2D target band")
- Cross-reference to monster composite (`agentic_orchestration/gandalf/findings/2026-05-16-monster-scale-inspection-strip.png`) so gandalf can reason about character + monster scales together

---

## Acceptance

- Single composite image at the specified path; 11 rows × 3 scale columns
- HD-2D target band reference overlay legible
- Per-row labels (name + element + pixel-height numeric) legible at full image size
- Notes file accompanies with the listed content
- knight-rider notified on completion; gandalf consumes alongside the monster composite for unified per-slug scale recommendation authoring

---

## What this unblocks

- gandalf authors per-character chierit scale recommendation alongside the per-monster recommendation
- knight-rider authors a drax chierit-scale-revision dispatch consuming gandalf's recommendation
- VS2a character-scale-tuning standing item (carried since Day 3) is closed

---

## Sequencing relative to monster composite and Legolas commission

- **Parallel to drax monster composite dispatch** (`2026-05-16-drax-gandalf-composite-scale-inspection-strip.md`). Both consume the same `scale-strip.html` harness; drax may produce them in one session or separate per their own scoping.
- **Independent of Legolas commission** — Legolas Section 1 (chierit intrinsic sizes) refines the eventual scale recommendation but does not block composite production. If Legolas finishes first, gandalf may request a 4th scale column tuned to Legolas data.
- **Output consumed by gandalf in unified pass.** Gandalf's recommendation artifact will reference both composites + Legolas synthesis.

---

## What this dispatch does NOT cover

- Per-character scale-lookup TABLE — gandalf's authoring after consuming this artifact
- The actual refactor of chierit scale constant to per-character lookup — separate drax dispatch knight-rider authors next
- Per-element scale variation logic — out of scope; gandalf may recommend uniform vs per-element after seeing the composite
- Samurai full wiring (animation sheets) — deferred to P6.d character-track sub-commission per drax v0.20.1 notes

---

— knight-rider, 2026-05-16 (Day 4 close); drafted in gandalf request channel at Matt's directive to extend gandalf's monster commission with the chierit companion
