# Dispatch — 2026-05-16 — legolas — Fire_Lord_Creativkind intrinsic-size measurement

**From:** knight-rider (authored per Matt directive Day-4 close: gandalf v2 Path A-prime Matt-decision #2 AUTHORIZE — Mode A intrinsic-size measurement to unblock MONSTER_SCALE_BY_SLUG refactor for 2 affected slugs)
**To:** legolas
**Approved by:** Matt at 2026-05-16 Day 4
**Status:** PENDING
**Mode:** A (analytical; file inspection)
**Estimated effort:** ~30 min; hard cap 45 min
**Budget:** $0 LLM

**Gate-1 bypass rationale:** Matt-directed, single-seam (legolas-only), read-only file inspection, bounded time. Per CHANGELOG rubric.

**Acceptance summary:** Fire_Lord_Creativkind intrinsic frame dimensions + animation frame counts + sheet layout type documented in research doc amendment. Knight-rider notified — unblocks drax MONSTER_SCALE_BY_SLUG refactor for fire-elemental (Case A swap target) + god-of-lightning (Case D palette-shift swap target).

---

## Why this dispatch exists

Gandalf v2 Path A-prime lookup table (`canonical/story/per-slug-scale-lookup-path-a-prime-2026-05-16.md`) operationalizes:
- **fire-elemental:** Case A swap target → Fire_Lord_Creativkind (VS2b queued; tier-coherence violation accepted at scale 0.85)
- **god-of-lightning:** Case D palette-shift swap → Fire_Lord_Creativkind thunder-palette-shifted (active VS2a swap per Matt-decision)

MONSTER_SCALE_BY_SLUG refactor cannot ship correct scale values for either of these slugs without Fire_Lord's intrinsic frame size. Matt-decision #2 (gandalf v2 return): AUTHORIZE legolas Mode A measurement. Sequence ahead of refactor.

## Cross-seam contract change?

**Round-trip: not applicable** — research output amendment; no schema or contract change; no production state modified. Per R11(b) Principle 6.

## What this dispatch produces

Amendment to your existing research doc: `agentic_orchestration/research/knowledge/character-monster-pixel-scale-2026-05-16.md` — append Fire_Lord_Creativkind entry to Section 2 (CreativeKind intrinsic source-sheet sizes).

### Required measurements

Per Fire_Lord_Creativkind pack at `/Users/admin/Games/reincarnated-demo/public/assets/CreativeKind/` (asset already on disk per drax v0.20 ingest):

- Pack name + path
- **Intrinsic frame dimensions** (e.g., 256×256, 192×192) — source-sheet pixel size per animation frame
- **Figure-content bbox** (if practical via PIL or visual inspection) — actual character art height excluding transparent padding (mirror the drax v0.20.4 chierit measurement methodology)
- Sheet layout type (combined-sheet vs per-animation-separated vs row_per_anim)
- Animation frame counts per state (idle / walk / attack / hurt / death)
- Anchor point convention
- Any palette-shift readiness notes (is the sprite element-signal already neutral, or does it strongly carry fire-orange/red signal that the thunder-palette-shift will need to overwrite?)

### Sources

1. CreativeKind asset pages (vendor docs)
2. On-disk pack at `/Users/admin/Games/reincarnated-demo/public/assets/CreativeKind/Fire_Lord*/` (you choose the exact subdirectory after `ls` the CreativeKind tree)
3. Drax v0.20 ingest-pipeline output (if metadata sidecar exists in `~/Games/reincarnated-demo/scripts/monster-ingest/`)
4. Drax `MONSTER_TRACK_INTEGRATION_NOTES.md` (may have intrinsic-size notes if Fire_Lord was inspected during v0.20)

### Output integration

- Append to existing Section 2 of research doc (DO NOT rewrite earlier sections)
- Update Section 4 synthesis table with Fire_Lord recommended scale per Path A-prime tier-ranges:
  - Fire_Lord as fire-elemental swap (elite tier 110-156 px range) → scale recommendation
  - Fire_Lord as god-of-lightning thunder-palette boss swap (boss tier 275-480 px range) → scale recommendation (may need different scale value per use-case)
- Flag any mathematical impossibility (per the existing math-impossibility rulings methodology)

## Out of scope (explicit)

- **NO new vendor catalogue work** (Mode A; bounded to Fire_Lord measurement only)
- **NO palette-shift implementation recommendation** (drax-seam; out of legolas lane)
- **NO acquisition recommendations** (Fire_Lord already on disk)
- **NO recommendation on whether to use Fire_Lord for fire-elemental OR god-of-lightning OR both** (gandalf already decided both per v2 + Matt locked god-of-lightning palette-shift)
- **NO commentary on Fire_Lord's other potential uses** beyond the two surfaced VS2a/VS2b slots

## Required reading

- Your existing research doc: `agentic_orchestration/research/knowledge/character-monster-pixel-scale-2026-05-16.md` (Section 2 + Section 4 patterns)
- Gandalf v2 per-slug lookup: `canonical/story/per-slug-scale-lookup-path-a-prime-2026-05-16.md` (Fire_Lord references)
- Gandalf math-impossibility rulings: `canonical/story/sprite-scale-math-impossibility-rulings-2026-05-16.md` (Case A + Case D contexts)
- Drax `MONSTER_TRACK_INTEGRATION_NOTES.md` (if exists)

## Acceptance criteria

- [ ] Fire_Lord_Creativkind entry appended to Section 2 of research doc (intrinsic dims + frame counts + sheet layout + anchor + palette-shift readiness)
- [ ] Section 4 synthesis updated with Fire_Lord recommended scale per Path A-prime tier ranges
- [ ] Mathematical impossibility flagged if applicable
- [ ] Per-data-point source attributed (file path)
- [ ] Time-cap honored (≤ 45 min)
- [ ] Knight-rider notified with: doc path, Fire_Lord intrinsic dims summary, recommended scale per use-case, any unanticipated findings

## Tag policy

- **No git tag** (research persona; file timestamp suffices)

---

## Completion record

**Completed:** 2026-05-16
**Fire_Lord intrinsic dims:** 128×128 px per frame (all animations, all 5 color variants)
**Sheet layout:** per-animation separated (Pattern F — same class as Lich Pattern A; 9 distinct animation files per color variant; 5 color variants)
**Animation frame counts:** idle:16 / run:16 / casting:32 / atk1:16 / atk2:16 / atk3:32 / atk4:16 / hurt:3 / death:15 (162 total frames per variant)
**Palette-shift readiness:** NO TINTING NEEDED — Variant 1 already blue/purple-dominant (thunder register); Variant 5 = fire/orange (strong-fire-signal, 96.8% red-dominant). Thunder use case should use V1 directly. Fire use case uses V5.
**Recommended scale (fire-elemental swap, elite tier):** 2.93× (idle 132 px at elite midpoint; nearest-neighbor HARD REQ; attack frames extend to 358 px peak — expected design behavior)
**Recommended scale (god-of-lightning thunder-palette swap, boss tier):** MATH IMPOSSIBILITY — see Section 4e. Fire_Lord (128px canvas, 45px idle content) cannot achieve persistent boss-tier presence (287–460 px) within viable upscale limits. Best-achievable is 2.35× (atk4 peak 287 px at boss floor; idle 106 px reads as above-elite). Requires gandalf/matt decision on tier-coherence-violation scope before drax can assign a scale value.
**Mathematical impossibility:** FLAGGED for Case D (boss tier). Case A (elite tier) has no impossibility.
**Time spent:** ~35 min
**Notes for knight-rider:** (1) Case A (elite swap) is unblocked — scale 2.93×, V5 palette, anchor-offset ~+25 px source-px needed. (2) Case D (boss thunder swap) is BLOCKED on a design decision: Fire_Lord is architecturally elite-sized, not boss-sized. The gandalf v2 lookup table placeholder (~2.0×) was based on an incorrect 256px frame assumption; actual is 128px. Recommend routing Case D back to gandalf+matt as a new decision item before the MONSTER_SCALE_BY_SLUG refactor assigns a scale value for the thunder boss slot. (3) Per-slug lookup v2 Case E entry needs: frame updated to 128×128 (not 256×256), idle_content_H = 45 px, scale = 2.93× for elite use (Case A), math-impossibility flag for boss use (Case D), color_variant = 1 for thunder / 5 for fire, no_palette_tinting_required.
