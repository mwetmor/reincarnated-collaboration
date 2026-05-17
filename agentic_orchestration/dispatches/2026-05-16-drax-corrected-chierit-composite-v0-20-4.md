# Dispatch — 2026-05-16 — drax — Corrected chierit composite (v0.20.4) — scales informed by legolas Section 4

**From:** knight-rider (authored per legolas pixel-scale research completion 2026-05-16; corrected scale candidates inform the actual chierit-scale selection)
**To:** drax
**Approved by:** Matt at 2026-05-16 Day 4 ("fire all three follow-ons")
**Status:** PENDING — v0.20.3 has returned (tag `drax/v0.20.3-gandalf-chierit-composite-scale-strip @ a49b305`); v0.20.4 may now execute.
**Estimated effort:** ~30 min; mirrors v0.20.3 pattern with new scale candidates only. Same Python/PIL harness from v0.20.2/v0.20.3 already in place.

**Gate-1 bypass rationale:** Matt-directed, single-seam (demo-only), reversible (artifact only), small scope. Per CHANGELOG rubric.

**Acceptance summary:** Second chierit composite PNG at `agentic_orchestration/gandalf/findings/2026-05-16-chierit-character-scale-inspection-strip-corrected.png` (≤2MB) rendered at corrected scale candidates (0.7 / 0.9 / 1.1) bracketing legolas's Section 4 recommendation (~0.91-1.14). Same layout as v0.20.3 (11 rows × 3 scale columns + HD-2D target band overlay). Companion notes file documents scale-revision rationale.

---

## Why this dispatch exists

Your in-flight v0.20.3 chierit composite renders at scales 0.25 / 0.35 / 0.45 (bracket of current default 0.35). **Legolas pixel-scale research returned with a critical finding:**

> "Current characterSprites.ts default scale 0.35 renders characters at only ~31px (character art height), against an 80-100px HD-2D register target. The required scale is approximately 0.91–1.14 — roughly triple the current value. The strip images at 0.25/0.35/0.45 that drax generated all sit far below the HD-2D register floor."

The v0.20.3 composite is still useful (clean visual gap demonstration) but does not let gandalf select final scales. **This v0.20.4 dispatch produces the actual scale-selection artifact** at corrected candidates.

## Cross-seam contract change?

**Round-trip: not applicable** — demo-internal artifact generation only; no schema or contract change. Per R11(b) Principle 6.

## What this dispatch produces

### Required artifact 1 — corrected composite PNG

Path: `agentic_orchestration/gandalf/findings/2026-05-16-chierit-character-scale-inspection-strip-corrected.png`

**Scale candidates:** **1.5 / 2.0 / 2.5**
- Anchored on YOUR v0.20.3 per-character figure-content measurements (NOT legolas's full-canvas estimate, which assumed 128px content vs actual 34-57px content)
- v0.20.3 per-character bands: Shadow Stalker reaches 80-100 px @ 1.4-1.8× ; Light Valkyrie @ 1.5-1.9× ; most chierit characters @ 1.8-2.3× ; Ground Monk (smallest, 34px content) @ 2.4-2.9×
- 1.5 = lower-half bracket (catches Shadow Stalker + Light Valkyrie in band)
- 2.0 = middle (catches most chierit in band)
- 2.5 = upper bracket (catches Ground Monk + Water Priestess + Wind Hashashin)

This bracket spans the per-character variance. Gandalf can scan to see which characters land cleanly inside the HD-2D 80-100 px band at each scale, and identify cases where a single uniform scale won't satisfy all characters (likely outcome: per-character scale lookup needed).

(Knight-rider note: if gandalf sends amended scales BEFORE you start this dispatch via separate request, use those instead and document. Otherwise these are the correct candidates given v0.20.3's measurements.)

### Layout — IDENTICAL to v0.20.3

- 11 chierit-track character rows × 3 scale columns
- HD-2D target band overlay (80-100 px horizontal guidelines) anchored at ground-level baseline
- Sort by element family (same order as v0.20.3): metal-bladekeeper → fire-knight → water-priestess → ground-monk → wind-hashashin → crystal-mauler → light-valkyrie → shadow-stalker → lightning-ronin → leaf-ranger → samurai
- Per-row labels: character name + element label
- Per-thumbnail labels: rendered pixel-height numeric (e.g., `@ 0.7 → 78 px tall`; `@ 0.9 → 100 px tall`; `@ 1.1 → 122 px tall`)
- Same Samurai handling decision you made in v0.20.3 (keep consistent)

### Constraints (mirror v0.20.3)

- Neutral background; idle first frame only; no VFX
- Same camera distance for all three scale candidates
- Single PNG; ≤2MB

### Required artifact 2 — companion notes file

Path: `agentic_orchestration/gandalf/findings/2026-05-16-chierit-character-scale-inspection-strip-corrected-notes.md`

Required content:
- Scale-revision rationale: legolas Section 4 finding (current 0.35 ≈ 31 px vs 80-100 px target; ~3× gap; required 0.91-1.14)
- Cross-reference to v0.20.3 composite (the obsolete-but-still-useful gap-visualization)
- chierit intrinsic source-sheet (288×128 confirmed)
- Any rendering anomalies at the higher scales (some characters may show pixelation/blur at 1.1×; document)
- Samurai handling carry-forward (same decision as v0.20.3)

## Out of scope (explicit)

- **NO chierit scale refactor.** Composite generation only. Per-character scale-revision dispatch is the natural follow-on AFTER gandalf consumes both composites + math-impossibility rulings + legolas screenshot follow-on.
- **NO scale candidates beyond 0.7/0.9/1.1.** (Unless gandalf sends revised candidates before you start.)
- **NO Samurai animation-sheet sourcing** (P6.d territory).
- **NO monster composite touchpoints.** Separate v0.20.2 (already complete) owns that.
- **NO black-screen-related changes** (fixed at f54da43).

## Required reading

- Legolas pixel-scale research: `agentic_orchestration/research/knowledge/character-monster-pixel-scale-2026-05-16.md` (especially Section 4 chierit synthesis)
- Your v0.20.3 dispatch + completion record (when filed) — pattern + Samurai handling decision to carry forward
- `agentic_orchestration/gandalf/findings/2026-05-16-chierit-character-scale-inspection-strip-notes.md` — when v0.20.3 lands

## Acceptance criteria

- [ ] Composite PNG at `agentic_orchestration/gandalf/findings/2026-05-16-chierit-character-scale-inspection-strip-corrected.png` (≤2MB)
- [ ] 11 rows × 3 scale columns (or 10 if Samurai handling = omit per v0.20.3 decision)
- [ ] Scales: 0.7 / 0.9 / 1.1 (unless gandalf-amended)
- [ ] HD-2D target band overlay legible
- [ ] Per-thumbnail pixel-height numerics legible
- [ ] Companion notes file with scale-revision rationale + v0.20.3 cross-reference
- [ ] No new TS errors; tests pass
- [ ] Intermediate tag `drax/v0.20.4-corrected-chierit-composite` cut
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified with: composite path, notes path, file size, tag hash, any per-character sizing concerns at new scales

## Tag policy

- **Intermediate tag:** `drax/v0.20.4-corrected-chierit-composite` at the commit producing the composite + notes file.
- **Milestone tag:** none.

---

## Completion record

**Completed:** 2026-05-16
**Composite PNG path:** `agentic_orchestration/gandalf/findings/2026-05-16-chierit-character-scale-inspection-strip-corrected.png`
**Notes file path:** `agentic_orchestration/gandalf/findings/2026-05-16-chierit-character-scale-inspection-strip-corrected-notes.md`
**File size:** 233.3 KB (1013 x 5074 px; within 2MB limit)
**Intermediate tag:** `drax/v0.20.4-corrected-chierit-composite @ 3bf9680` (demo repo, script commit)
**Tests status:** TypeScript clean (npx tsc --noEmit PASS); no test suite changes (pure artifact generation)

**Notes for knight-rider:**

Scale candidates 1.5/2.0/2.5 confirmed correct. All 10 chierit characters measured; key result:

**No single uniform scale hits the HD-2D 80-100px band for all characters.** Three groups emerge:
- Group A (1.5x in band): Shadow Stalker 86px, Light Valkyrie 80px
- Group B (2.0x in band): Metal Bladekeeper 84px, Fire Knight 88px, Lightning Ronin 86px, Leaf Ranger 88px
- Group C (2.5x in band): Water Priestess 92px, Ground Monk 85px, Wind Hashashin 92px, Crystal Mauler 98px

Per-character scale lookup is the indicated path. A uniform 2.0x would put 4 characters in band, but Group A overshots (114/106px) and Group C undershots (68-78px).

**Viewport implication at 2.5x:** 288px canvas * 2.5 = 720px wide per character. At 2.0x: 576px wide. Two-character combat (player + enemy) at 2.0x requires ~1152px horizontal canvas — not viable without a viewport redesign or bbox-anchored rendering that renders only the figure content region (24-60px content_w) rather than the full 288px canvas. All composite cells are h-clipped (canvas wider than cell; figure content fits cleanly). This is called out prominently in the composite header.

**Rendering anomalies documented in notes:**
1. Horizontal canvas clipping at all three scales (all characters) — transparent padding, figure visible
2. Pixelation at 2.0x and 2.5x (nearest-neighbor; expected for pixel art)
3. Ground Monk float: 15px visible hover at 2.5x (content bottom at row 121, not 127)
4. Shadow Stalker and Light Valkyrie above band at 2.0x and 2.5x

**Samurai:** Option (a) carry-forward — portrait renders at 960/1280/1600px at these scales; band not applicable; cells are heavily h-clipped showing portrait fragment only.
