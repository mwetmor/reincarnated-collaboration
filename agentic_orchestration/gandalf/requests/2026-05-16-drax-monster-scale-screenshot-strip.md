# Gandalf request to knight-rider — drax monster-scale screenshot strip for gandalf visual inspection

**From:** gandalf
**To:** knight-rider (for drax dispatch authoring)
**Date:** 2026-05-16 (Day 4 close)
**Authorized by:** Matt at 2026-05-16 Day 4 ("yes, authorize the legolas commission and screenshot strip")
**Type:** Visual-inspection artifact generation; small dispatch
**Estimated effort:** 1-2 hours drax

---

## Why this request exists

Gandalf visual-inspection standing item: post-B11-demo-integration, the 11 VS2a monsters are wired at a single `DEFAULT_MONSTER_SCALE = 0.28` constant. Drax flagged this as estimated; per-monster tuning needed.

Matt offered (and gandalf accepted) a screenshot-strip iteration path instead of live-playthrough inspection — cheaper loop, full bestiary comparable in one glance, side-by-side judgment of ratios across the tier hierarchy.

This dispatch produces the inspection artifact gandalf needs to author the per-slug scale lookup table that knight-rider's next drax dispatch (`DEFAULT_MONSTER_SCALE` → per-slug lookup refactor) will consume.

---

## What drax produces

A **single composite image** showing all 11 VS2a monsters at three scale candidates, side-by-side with the chierit player character as size reference.

### Image layout

```
                     SCALE 0.20         SCALE 0.28         SCALE 0.35
                  ┌────────────┐    ┌────────────┐    ┌────────────┐
  [PLAYER REF]    │ Crystal    │    │ Crystal    │    │ Crystal    │
  Fire Knight     │ Golem      │    │ Golem      │    │ Golem      │
  (chierit)       │ (boss)     │    │ (boss)     │    │ (boss)     │
  current scale   │ XXX px     │    │ XXX px     │    │ XXX px     │
                  └────────────┘    └────────────┘    └────────────┘

                  ┌────────────┐    ┌────────────┐    ┌────────────┐
  [PLAYER REF]    │ Hellfire   │    │ Hellfire   │    │ Hellfire   │
                  │ Rhino      │    │ Rhino      │    │ Rhino      │
                  │ (mini-boss)│    │ (mini-boss)│    │ (mini-boss)│
                  │ XXX px     │    │ XXX px     │    │ XXX px     │
                  └────────────┘    └────────────┘    └────────────┘
  ... (11 rows total, one per monster slug)
```

### Required elements per row

- **Player reference at LEFT of each row** — chierit Fire Knight (or chosen reference chierit) rendered at its current scale, anchored at ground-level so it sits visually adjacent to the monster on the same baseline
- **Monster name label** above the three thumbnails (e.g., "Crystal_Golem")
- **Tier label** below the monster name (e.g., "boss" / "mini-boss" / "elite" / "magic" / "swarm" — per `ENEMY_TIER_CHARACTER_MAP`)
- **Rendered pixel height numeric** below each thumbnail (e.g., "@ 0.20 → 102 px tall"; "@ 0.28 → 142 px tall"; "@ 0.35 → 178 px tall") — measured from monster sprite's ground-anchor to top-of-sprite (excluding any non-body protrusions if possible; if not, full bounding box height)

### Constraints

- **Neutral background** — single muted color (slate grey or off-white) so eye focuses on monster + scale comparison
- **Same camera distance for all three scale candidates** — only `DEFAULT_MONSTER_SCALE` value varies; everything else identical
- **Idle animation frame** — use the monster's idle anim first frame for visual stability (not mid-action where pose distorts apparent height)
- **No combat VFX in frame** — pure rendering, no skill effects firing
- **All 11 monsters in one image** — single PNG/JPG; rows stacked vertically; reasonable file size (≤ 2MB for fast inspection)

### Sorting order

Order rows by intended tier ascending (so visual flows from smallest-intended to largest-intended monsters):
1. Swarm tier monsters first (top of image)
2. Magic tier
3. Elite tier
4. Mini-boss tier
5. Boss tier last (bottom of image)

This lets gandalf's eye scan top-to-bottom and verify the tier hierarchy reads correctly.

---

## Output location

Save the composite image at:
`agentic_orchestration/gandalf/findings/2026-05-16-monster-scale-inspection-strip.png`

(plus thumbnail-strip-generation script if drax wants to make this repeatable — recommended but not required)

Drax adds an accompanying short notes file at:
`agentic_orchestration/gandalf/findings/2026-05-16-monster-scale-inspection-strip-notes.md`

Notes content:
- Source-sheet intrinsic pixel size per monster (if drax knows from acquisition; otherwise flag as "see Legolas commission")
- chierit Fire Knight current scale value used as reference
- Any rendering anomalies drax noticed mid-generation (e.g., "Crystal_Golem combined-sheet cycles all anims; idle frame extracted manually for this strip")

---

## Acceptance

- Single composite image at the specified path; 11 rows × 3 scale columns + player ref column
- Per-row labels (name + tier + pixel-height numeric) legible at full image size
- Notes file accompanies with the listed content
- knight-rider notified on completion; gandalf consumes for per-slug scale recommendation authoring

---

## What this unblocks

- gandalf authors per-slug scale lookup table (`agentic_orchestration/gandalf/findings/2026-05-16-monster-scale-recommendation.md` is the anticipated follow-on artifact)
- knight-rider authors drax refactor dispatch: convert `DEFAULT_MONSTER_SCALE` constant to per-slug lookup keyed off `ENEMY_TIER_CHARACTER_MAP`, populated from gandalf's table
- VS2a critical-path resolved on monster-scale hierarchy — no longer "single constant; tune in playtest" but "designed table; validate in playtest"

---

## Sequencing relative to Legolas commission

Legolas commission (`2026-05-16-legolas-character-monster-pixel-scale-research.md`) and this drax dispatch can run **in parallel**. Legolas's findings (intrinsic source-sheet sizes) refine gandalf's eventual recommendation; the screenshot strip lets gandalf judge the *rendered* output at three candidates regardless of source-sheet sizes. Both feed into the same recommendation artifact.

If Legolas completes first: gandalf may ask drax to add a 4th scale-candidate column tuned per the intrinsic-size data before running the inspection pass.
If drax completes first: gandalf judges from the strip while Legolas research runs; final recommendation reconciles both inputs.

---

## What this dispatch does NOT cover

- Per-monster-tier scale lookup TABLE — that's gandalf's authoring after consuming this artifact
- The actual refactor of `DEFAULT_MONSTER_SCALE` to per-slug lookup — separate drax dispatch knight-rider authors next
- Combined-sheet animation slicing (Crystal_Golem etc. play all anims in sequence) — VS2b territory per drax's prior call; this dispatch uses idle-frame-only so the issue doesn't confound scale judgment
- Per-animation per-frame anchor refinement — out of scope; idle-frame baseline anchoring sufficient

---

— gandalf, 2026-05-16 (Day 4 close)
