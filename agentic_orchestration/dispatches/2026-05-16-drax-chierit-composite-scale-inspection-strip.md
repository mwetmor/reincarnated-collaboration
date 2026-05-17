# Dispatch — 2026-05-16 — drax — Chierit composite scale-inspection strip (companion to v0.20.2 monster composite)

**From:** knight-rider (authored per gandalf-channel request file `agentic_orchestration/gandalf/requests/2026-05-16-drax-chierit-composite-scale-strip.md`; Matt-directed Day 4 close)
**To:** drax
**Approved by:** Matt at 2026-05-16 Day 4 ("fire drax now")
**Status:** PENDING
**Estimated effort:** 1 session (~1h); harness exists from v0.20.1; this dispatch mirrors v0.20.2 layout pattern with HD-2D-band overlay instead of player-ref column.
**Gate-1 bypass rationale:** Matt-directed extension to gandalf's monster commission; single-seam (demo-only); reversible (artifact only); small scope. Per CHANGELOG rubric.

**Acceptance summary:** Single composite PNG at `agentic_orchestration/gandalf/findings/2026-05-16-chierit-character-scale-inspection-strip.png` (≤2MB) showing 11 chierit-track character rows × 3 scale columns. HD-2D target band (80-100 px) overlaid as horizontal guidelines on each scale column. Each row labeled with character name + element + per-thumbnail rendered-pixel-height numeric. Companion notes file at `agentic_orchestration/gandalf/findings/2026-05-16-chierit-character-scale-inspection-strip-notes.md`.

---

## Why this dispatch exists

Matt's Day-4 directive ("ship 11 monsters at the 3 scales and also 11 characters") covered both monster + character composites. Gandalf's monster commission (and the corresponding v0.20.2 dispatch) covers the monster side. **This dispatch closes the character side.**

Gandalf's monster composite uses chierit Fire Knight as the SIZE REFERENCE (chierit is the anchor for monsters being tuned). This chierit composite reverses the framing: chierit IS the variable; the reference becomes the **HD-2D pixel-art register target band** (80-100 px height zone per gandalf's canonical-element register — Sea of Stars / Octopath Traveler / Eiyuden Chronicle baseline).

Closes the standing chierit-scale-tuning item carried since Day 3.

## Cross-seam contract change?

**Round-trip: not applicable** — demo-internal artifact generation only; no schema or contract change. Per R11(b) Principle 6.

## Coordination with in-flight v0.20.2

The v0.20.2 monster composite dispatch may still be in-flight when you start this. Both use the same `scale-strip.html` harness. Sequencing options:

- **(a)** If v0.20.2 is complete or near-complete: pick it up after v0.20.2 lands; extend the harness with chierit composite mode in a separate commit
- **(b)** If v0.20.2 is mid-flight in another session: queue this; do NOT race the harness edits

Drax judges; if conflict risk is real, prefer (b). The chierit composite is not critical-path — the monster composite is the load-bearing artifact for gandalf's recommendation-table authoring.

## What this dispatch produces

### Required artifact 1 — composite PNG

Path: `agentic_orchestration/gandalf/findings/2026-05-16-chierit-character-scale-inspection-strip.png`

Layout:

```
                          SCALE 0.25         SCALE 0.35         SCALE 0.45
                       ┌────────────┐    ┌────────────┐    ┌────────────┐
  HD-2D target         │ fire-      │    │ fire-      │    │ fire-      │
   band overlay        │ knight     │    │ knight     │    │ knight     │
   (80-100 px          │ (fire)     │    │ (fire)     │    │ (fire)     │
    horizontal lines)  │ XXX px     │    │ XXX px     │    │ XXX px     │
                       └────────────┘    └────────────┘    └────────────┘
                       ... (11 rows total, sorted by element family)
```

**Row order (per chierit ELEMENT mapping in `characterSprites.ts`):**
1. `metal-bladekeeper` (physical / kinetic)
2. `fire-knight` (fire)
3. `water-priestess` (water)
4. `ground-monk` (earth / ground)
5. `wind-hashashin` (wind)
6. `crystal-mauler` (ice / crystal)
7. `light-valkyrie` (light)
8. `shadow-stalker` (shadow)
9. `lightning-ronin` (lightning)
10. `leaf-ranger` (nature / leaf)
11. `GandalfHardcore-samurai` (placed last; see Samurai handling below)

**Per-row required elements:**
- **Character name** above the three scale thumbnails
- **Element label** below character name
- **Rendered pixel height numeric** per thumbnail (e.g., `@ 0.25 → 72 px tall`; `@ 0.35 → 100 px tall`; `@ 0.45 → 130 px tall`) — measured feet-to-top-of-head (excluding hair/hat protrusions if practical; otherwise full bounding box)

### HD-2D target band overlay (replaces player-ref column from monster composite)

Render a faint horizontal band or pair of guidelines spanning the **80-100 px height zone**, anchored at the same ground-level baseline as the character sprites. Label legibly: `"HD-2D target: 80-100 px (per gandalf canonical-element register)"`.

This lets gandalf scan top-to-bottom and verify which scale lands each character cleanly inside the band.

### Samurai handling — drax picks

Drax's v0.20.1 noted GandalfHardcore Samurai is portrait-only (640×640) with no animation sheets. Two options:

- **(a) Include as-is** — render the 640×640 portrait at three scales (0.25 / 0.35 / 0.45) so gandalf sees scale comparison against chierit. Label clearly: `"(portrait only; no anim sheets — see P6.d sub-commission)"`. May want narrower Samurai-only scale candidates if 640×640 overwhelms the chierit-tuned scales.
- **(b) Omit Samurai** — 11 → 10 rows; document omission in companion notes as `"Samurai deferred until animation sheets are sourced; see P6.d character-track sub-commission."`

Either is acceptable. Decision belongs to drax based on artifact ergonomics.

### Constraints (mirror monster composite spec)

- **Neutral background** — same muted color used in monster composite
- **Same camera distance for all three scale candidates** — only chierit scale value varies
- **Idle animation first frame** — visual stability
- **No combat VFX** in frame
- **Single PNG; ≤2MB**

### Required artifact 2 — companion notes file

Path: `agentic_orchestration/gandalf/findings/2026-05-16-chierit-character-scale-inspection-strip-notes.md`

Required content:
- chierit intrinsic source-sheet pixel size (288×128 per drax's prior empirical confirmation) — confirm and extend per-character if any deviation
- Current chierit scale (0.35) explanation — what rendered pixel height does this currently produce against the HD-2D 80-100 px target band
- Samurai handling decision (option a or b) + rationale
- Any rendering anomalies (e.g., "ground-monk idle frame has anchor offset that visually misaligns against the HD-2D target band")
- Cross-reference to monster composite (`agentic_orchestration/gandalf/findings/2026-05-16-monster-scale-inspection-strip.png`) so gandalf reasons about character + monster scales together

## Out of scope (explicit)

- **NO chierit scale refactor.** Composite generation only. Per-character scale-revision dispatch is the natural follow-on knight-rider authors AFTER gandalf consumes both composites.
- **NO new scale candidates beyond 0.25 / 0.35 / 0.45.** Mirror v0.20.1 chierit candidates. (Gandalf may request 4th column tuned to legolas-supplied intrinsic-size data AFTER seeing this composite + legolas synthesis; separate follow-on.)
- **NO Samurai animation-sheet sourcing.** P6.d character-track sub-commission territory.
- **NO black-screen-related changes** (already fixed at `f54da43`).
- **NO monster composite touchpoints.** Separate v0.20.2 dispatch owns that.

## Required reading

- `agentic_orchestration/gandalf/requests/2026-05-16-drax-chierit-composite-scale-strip.md` (knight-rider-drafted request stub; full spec)
- `agentic_orchestration/dispatches/2026-05-16-drax-gandalf-composite-scale-inspection-strip.md` (v0.20.2 monster composite; harness pattern reference)
- Your v0.20.1 completion record (harness exists; chierit scales 0.25/0.35/0.45 already used)
- `~/Games/reincarnated-demo/src/scale-strip.ts` + `scale-strip.html` (harness)
- `~/Games/reincarnated-demo/src/visuals/characterSprites.ts` — chierit ELEMENT mapping for sort order

## Acceptance criteria

- [ ] Composite PNG at `agentic_orchestration/gandalf/findings/2026-05-16-chierit-character-scale-inspection-strip.png` (≤2MB)
- [ ] 11 rows × 3 scale columns (or 10 if Samurai option b chosen); rows sorted by element family
- [ ] HD-2D target band (80-100 px) overlaid as horizontal guidelines on each scale column
- [ ] Per-row labels: character name + element label
- [ ] Per-thumbnail labels: rendered pixel-height numeric
- [ ] Neutral background; idle first frame only; no VFX
- [ ] Companion notes file at `agentic_orchestration/gandalf/findings/2026-05-16-chierit-character-scale-inspection-strip-notes.md`
- [ ] Samurai handling decision documented in notes
- [ ] No new TS errors (`tsc --noEmit` clean)
- [ ] Existing tests pass (`npm run test`)
- [ ] Intermediate tag `drax/v0.20.3-gandalf-chierit-composite-scale-strip` cut
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified with: composite path, notes path, Samurai handling chosen, file size, tag hash

## Tag policy

- **Intermediate tag:** `drax/v0.20.3-gandalf-chierit-composite-scale-strip` at the commit producing the composite + notes file.
- **Milestone tag:** none.

---

## Completion record

**Completed:** 2026-05-16
**Composite PNG path:** `agentic_orchestration/gandalf/findings/2026-05-16-chierit-character-scale-inspection-strip.png`
**Notes file path:** `agentic_orchestration/gandalf/findings/2026-05-16-chierit-character-scale-inspection-strip-notes.md`
**File size:** 158.5 KB (833 × 3744 px; well within 2MB limit)
**Samurai handling:** Option (a) — included as portrait (640×640 Portrait1.png at 3 scales). Rationale: portrait-at-scale comparison is informative to gandalf even without animation sheets; shows the 640px portrait-to-game-sprite size discrepancy visually. Labeled prominently "(portrait only — no anim sheets — see P6.d sub-commission)".
**Intermediate tag:** `drax/v0.20.3-gandalf-chierit-composite-scale-strip @ a49b305`
**Tests status:** 294/294 PASS; `tsc --noEmit` PASS

**Notes for knight-rider:**

PRIMARY FINDING: The 0.25/0.35/0.45 scale candidates are all far below the HD-2D target.

All 10 chierit characters use a uniform 288×128 canvas, but the character figure (opaque pixels) occupies only 34-57px of that canvas height, concentrated at the bottom of the frame. At the current game scale 0.35, Fire Knight renders at 45px full-frame but only 15px figure height. The HD-2D 80-100px target requires the figure height to be in band — not the full-frame height.

**Required scales to reach HD-2D band (figure content height):**
- Shadow Stalker (57px figure): ~1.40x–1.75x
- Light Valkyrie (53px figure): ~1.51x–1.89x
- Leaf Ranger / Fire Knight / Lightning Ronin (43-44px): ~1.82x–2.33x
- Metal Bladekeeper (42px): ~1.90x–2.38x
- Crystal Mauler (39px): ~2.05x–2.56x
- Water Priestess / Wind Hashashin (37px): ~2.16x–2.70x
- Ground Monk (34px, smallest): ~2.35x–2.94x

This is a structural finding: reaching the HD-2D register from chierit's 288×128 canvas format requires a ~4-8x scale increase from current 0.35 value. Companion notes flag the viewport implications (288px canvas at scale 2.0 = 576px wide). The per-character scale refactor dispatch should address both the scale value and whether to trim canvas padding in chierit exports (if available) or accept smaller character figures in the Reincarnated viewport register.

**Per-character sizing concerns (mirrors v0.20.2 format):**
1. Ground Monk: smallest figure (34px) + content bottom at row 121 (not 127) — slight ground float, visible at scale ≥1.5x
2. Shadow Stalker: tallest figure (57px) — reaches HD-2D band with smallest scale increase
3. Light Valkyrie: second tallest (53px) — same as above
4. Samurai portrait: 640×640 frame at 0.25 → 160px (above band; well above); animation-sheet scaling not applicable until P6.d
