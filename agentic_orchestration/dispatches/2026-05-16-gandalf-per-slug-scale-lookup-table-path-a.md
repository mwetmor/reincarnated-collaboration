# Dispatch — 2026-05-16 — gandalf — Per-slug scale lookup table (Path A re-anchor)

**From:** knight-rider (authored per Matt directive Day-4 close: "Path A — scale down to the common chierit player sprite. Scaling that up would just look awkward.")
**To:** gandalf
**Approved by:** Matt at 2026-05-16 Day 4 (Path A locked; chierit-scale operational call delegated to your authoring)
**Status:** PENDING
**Mode:** Design-track analytical (canonical-doc / findings-doc authoring)
**Estimated effort:** 1 session (~1.5-2h)

**Gate-1 bypass rationale:** Matt-directed (Path A explicitly locked), single-seam (gandalf authoring only), reversible (recommendation doc; not code).

**Acceptance summary:** Per-slug scale lookup table filed at `agentic_orchestration/gandalf/findings/2026-05-16-per-slug-scale-recommendation-path-a.md` (or canonical equivalent — your call). Path A tier ranges established (monsters scaled DOWN to chierit player baseline). Per-character chierit scale recommendation (operationalize "common chierit player sprite" — likely chierit default 0.35 → 1.0; document rationale). Per-monster scale recommendation for all 11 ENEMY_TIER monsters with quality-loss flags + tier-coherence violations called out per math-impossibility rulings. Schema-side recommendation for `width_or_height_priority` per-slug flag (per your forwarded analysis Case A). Knight-rider notified — recommendation is the input to the drax MONSTER_SCALE_BY_SLUG refactor + drax per-character chierit scale revision dispatches.

---

## Why this dispatch exists — Path A locked

Matt's decision: **Path A.** Re-anchor monster tier ranges proportionally DOWNWARD against actual chierit player baseline. **NOT Path B** (which would upscale chierit ~1.85× to reach an 80 px reference and trigger 1152-1440 px combat-view viewport pressure).

Matt's framing: "scale down to the common chierit player sprite. Scaling that up would just look awkward."

This collapses your math-impossibility rulings into Path A-anchored recommendations + dissolves the viewport pressure drax flagged in v0.20.4.

## Cross-seam contract change?

**Round-trip: not applicable** — recommendation-doc output; no schema or contract change. The downstream drax refactor dispatch carries its own round-trip discipline. Per R11(b) Principle 6.

## What this dispatch produces

### Part 1 — Chierit operational scale recommendation

The open question: what's the operational chierit default scale that makes "common chierit player sprite" land cleanly as the size reference?

Empirical inputs:
- chierit canvas: 288×128
- chierit figure-content per drax v0.20.4 PIL measurement: 34-57 px (Group A 53-57; Group B 42-44; Group C 34-39)
- Current default: 0.35 → renders figure content at ~12-20 px
- Per Matt: do NOT scale up to reach 80-100 px HD-2D target (would look awkward + trigger viewport pressure)

Pick + justify a chierit scale (or per-character scale lookup):
- **Option (i):** chierit default 1.0× → natural figure content 34-57 px → player baseline ~44 px (midpoint)
- **Option (ii):** chierit default keeps at 0.35 → ~15 px player baseline → monsters get re-anchored to tiny absolute sizes (swarm 9-13 px)
- **Option (iii):** per-character chierit scale lookup → normalize all chierit figure-content to a single target (e.g., all chierit render at ~50 px figure content)

My read (defer to you): Option (i) seems likely-correct — preserves chierit aesthetic variance + gives reasonable player baseline. Option (iii) homogenizes characters which loses chierit's natural design distinction. Option (ii) makes everything microscopic.

### Part 2 — Path A monster tier ranges

Re-anchor your Day-4 Diablo-hierarchy tier ranges against the chosen chierit player baseline. Assuming Option (i) chierit at 1.0× (player baseline ~44 px midpoint):
- **Trash:** 0.6-0.85× player → 26-37 px
- **Magic (engine doesn't ship this tier currently; flag for future):** 0.8-1.0× player → 35-44 px
- **Elite:** 1.0-1.3× player → 44-57 px
- **Mini-boss:** 1.5-2.0× player → 66-88 px
- **Boss:** 2.5-4.0× player → 110-176 px

Pick midpoints OR ranges per tier; you choose the doc format.

### Part 3 — Per-monster scale recommendation (11 monsters)

For each of the 11 ENEMY_TIER monsters, compute the scale factor that lands the monster's figure-content (per legolas Section 4 + drax v0.20.2 + drax v0.20.4 measurements) inside its tier range:

- `goblin-mage` (trash)
- `mutant-skeleton` (trash)
- `evil-eye` (trash, 64×64 intrinsic — small source)
- `sword-warrior` (trash, 280×280 intrinsic — large source with transparent padding; needs strong downscale per your rulings doc; 0.13-0.17× Path A)
- `crystal-golem` (elite)
- `fire-elemental` (elite, 192×68 intrinsic — width-dominant; per your rulings doc + forwarded analysis Case A, use width_or_height_priority schema flag)
- `demon-mage` (elite — row_index metadata may be missing; flag for legolas sweep or drax extension)
- `lich` (mini_boss)
- `hellfire-rhino` (mini_boss)
- `angel-guardian` (boss — per your rulings doc 1.30× upscale acceptable WITH nearest-neighbor enforcement; HARD REQ for drax)
- `god-of-lightning` (boss — animation_pack_incomplete; per your rulings doc, palette-shift Fire_Lord_Creativkind is the zero-cost VS2a swap recommendation)

Per monster: scale factor + tier-coherence flag (in-band / above / below) + quality-loss flag (none / acceptable-upscale / acceptable-downscale / nearest-neighbor-required).

### Part 4 — Schema-side recommendations for drax refactor

Per your forwarded analysis, the drax MONSTER_SCALE_BY_SLUG refactor should include:
- **`width_or_height_priority`** per-slug flag (for fire-elemental width-dominant case)
- **`texture.baseTexture.scaleMode = PIXI.SCALE_MODES.NEAREST`** enforcement for upscale > 1.0× (HARD REQ for angel-guardian; recommended forward discipline for any upscale)

Surface for knight-rider routing into the drax refactor dispatch.

### Part 5 — Open Matt-decisions surfaced for routing

- **god-of-lightning resolution path:** confirm zero-cost palette-shift Fire_Lord_Creativkind is operative for VS2a (vs Matt-authorized re-acquire of complete god-of-lightning pack)
- **Sword-warrior transparent-padding inspection:** per your rulings doc this is hygiene rather than blocking (pixel art downscales cleanly); recommend drax confirms bbox in completion record but no separate inspection dispatch needed

### Part 6 — Cross-references

- Drax v0.20.4 chierit composite + notes (Path A empirical confirmation)
- Drax v0.20.2 monster composite + notes (4 sizing concerns flagged)
- Legolas pixel-scale research Section 4 synthesis
- Legolas screenshot ground-truth follow-on (in flight; may refine ±5 px before you complete)
- Your math-impossibility rulings doc

## Out of scope (explicit)

- **NO drax refactor authoring** — knight-rider authors drax MONSTER_SCALE_BY_SLUG + chierit-scale-revision dispatches after your recommendation lands
- **NO vendor acquisition execution** — surface for Matt-decision routing
- **NO HD-2D-register revision** — your locked anchor; just operationalize at Path A scale
- **NO B6 / B11 / spirit guide / form-bias touchpoints** — separate work streams
- **NO chierit scale refactor execution** — drax-seam follow-on
- **NO opportunistic style-register doc revision** beyond what's required for Path A consistency

## Required reading

- Drax v0.20.4 chierit composite notes: `agentic_orchestration/gandalf/findings/2026-05-16-chierit-character-scale-inspection-strip-corrected-notes.md`
- Drax v0.20.2 monster composite notes: `agentic_orchestration/gandalf/findings/2026-05-16-monster-scale-inspection-strip-notes.md`
- Legolas pixel-scale research: `agentic_orchestration/research/knowledge/character-monster-pixel-scale-2026-05-16.md`
- Your math-impossibility rulings: `canonical/story/sprite-scale-math-impossibility-rulings-2026-05-16.md`
- Your prior canonical: `canonical/story/style-register.md`, `canonical/story/enemy-visual-legibility.md`, `canonical/story/b6-skill-tree-ui-scoping.md`, `canonical/story/embodiment-display-loadout.md`

## Acceptance criteria

- [ ] Doc filed at gandalf canonical / findings path (your call)
- [ ] Chierit operational scale recommendation with rationale (3 options framed; pick + justify)
- [ ] Path A monster tier ranges established (re-anchored to chosen chierit baseline)
- [ ] Per-monster scale recommendation for all 11 ENEMY_TIER monsters with tier-coherence + quality-loss flags
- [ ] Schema-side recommendations for drax MONSTER_SCALE_BY_SLUG refactor (width_or_height_priority + nearest-neighbor enforcement)
- [ ] Open Matt-decisions surfaced (god-of-lightning resolution path + sword-warrior padding confirmation)
- [ ] Cross-references to all relevant inputs
- [ ] Knight-rider notified with: doc path, chierit option chosen, any open Matt-decisions framed

## Tag policy

- No git tag (gandalf canonical / findings persona convention)

---

## Completion record

**Completed:** _<date>_
**Doc path:** _<path>_
**Chierit option chosen:** _<i / ii / iii + rationale>_
**Open Matt-decisions surfaced:** _<list>_
**Notes for knight-rider:**
