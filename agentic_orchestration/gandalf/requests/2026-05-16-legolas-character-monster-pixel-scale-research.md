# Gandalf request to knight-rider — Legolas Mode A commission: character-monster pixel-scale empirical research

**From:** gandalf
**To:** knight-rider (for Legolas dispatch authoring)
**Date:** 2026-05-16 (Day 4 close)
**Authorized by:** Matt at 2026-05-16 Day 4 ("yes, authorize the legolas commission and screenshot strip")
**Type:** Research commission — Mode A (analytical web research; read-only)
**Estimated effort:** 1-2 hours

---

## Why this commission exists

VS2a chierit character ingest + 11-monster wiring (CreativeKind) lands at a per-monster scale-tuning gate (drax's open item; flagged on completion of B11 demo integration today). Drax used `DEFAULT_MONSTER_SCALE = 0.28` as an estimated single constant; gandalf flagged this as Discipline #13a-risk (single-constant can't honor genre tier-hierarchy across vendors at different intrinsic source-sheet sizes).

**Genre-side framework already authored** by gandalf at 2026-05-16 (Day 4 council response): Diablo size hierarchy + HD-2D pixel-art register reference + per-tier ratio recommendations. **Empirical gaps remain** — three specific data points I can't supply from training and need to ground the per-slug scale lookup table.

Without these, scale-tuning becomes "drax + gandalf eyeballing the screenshot strip" — workable but not falsifiable. With these, the per-slug lookup table becomes a measured artifact.

---

## What Legolas should produce

A single research-findings doc at `agentic_orchestration/research/knowledge/character-monster-pixel-scale-2026-05-16.md` with three sections:

### Section 1 — chierit Elementals intrinsic source-sheet pixel sizes (HIGH priority)

For each of the 10 chierit archives currently at `/Users/admin/Games/reincarnated-demo/public/assets/Elementals_bundle/`, document:
- Archive filename
- Character name (Fire Knight, Water Priestess, etc.)
- **Intrinsic frame dimensions** (e.g., 64×64, 128×128, 96×112) — source-sheet pixel size per animation frame BEFORE any scale factor applied
- Animation frame counts per state (idle / walk / attack / hurt / death)
- Anchor point convention (top-left? center? feet?)
- Any per-character metadata.json content relevant to scale

**Sources:**
- chierit itch.io asset pages (primary; canonical author documentation)
- Existing metadata.json files in `/Users/admin/Games/reincarnated-demo/public/assets/Elementals_bundle/` (secondary; drax-extracted)
- Direct file inspection if itch.io pages don't ship pixel-size docs

**Why critical:** determines what scale factor produces the 80-100 px HD-2D target. Without this, gandalf's scale lookup table for monsters is calibrated against an unknown reference.

### Section 2 — CreativeKind monster vendor intrinsic source-sheet pixel sizes (HIGH priority)

For each of the 11 VS2a monsters drax has wired:
- Source vendor (confirm CreativeKind for all; flag any from other vendors)
- Pack name / archive name
- **Intrinsic frame dimensions** per animation frame
- Combined-sheet vs per-animation-separated (drax has flagged some are combined-sheet; confirm which)
- Animation frame counts per state
- Anchor point convention

**Monster slugs to research** (per `ENEMY_TIER_CHARACTER_MAP` — drax-canonical):
- Crystal_Golem
- Hellfire_Rhino
- Goblin_Mage
- Lich
- Mutant_Skeleton
- (plus the remaining 6 — pull the full list from drax repo `src/scenes/encounter.ts` or `ENEMY_TIER_CHARACTER_MAP` const)

**Sources:**
- CreativeKind asset pages (vendor docs)
- Source-sheet files at known drax-acquired paths
- Direct file inspection for intrinsic sizes if vendor docs lack specifics

### Section 3 — HD-2D pixel-art shipped-game character height reference (MEDIUM priority)

Specific pixel heights of player-character sprites in shipped HD-2D titles at 1080p default camera distance. Three reference titles:
- **Sea of Stars (Sabotage, 2023)** — measure protagonist (Zale or Valere) at "world map default zoom" pixel height
- **Octopath Traveler (Square Enix, 2018)** — measure any of the 8 protagonists at default field-exploration zoom
- **Eiyuden Chronicle: Hundred Heroes (505 Games, 2024)** — measure protagonist at default exploration zoom

**Sources:**
- Gameplay screenshots from major review sites (IGN, GameSpot, RPS) at 1080p
- Direct gameplay video frame-grabs (YouTube; documented timestamps for traceability)
- Existing forum / GameDev / pixel-art-community discussions on HD-2D sprite scales

**Method:** measure character pixel height at ground level (feet to top of head, not including hair/hat protrusions) on screenshots confirmed at 1080p native rendering.

**Tolerance:** ±5 px acceptable. We want to confirm the 80-100 px range, not precision to the pixel.

### Section 4 — Operational summary (your synthesis)

Close the doc with a synthesis table:
- chierit characters: target rendered pixel height in Reincarnated demo to match HD-2D register → recommended scale factor per character
- 11 monsters: target rendered pixel height per tier → recommended scale factor per monster
- Flag any monsters where the intrinsic source-sheet pixel size makes the target ratio mathematically impossible without quality loss (e.g., a 32×32 source can't render at 200 px tall cleanly without massive upscaling artifacts)

The synthesis is the actionable artifact drax + gandalf will consume directly.

---

## Constraints

- **Mode A only.** No catalogue crawl. No vendor outreach. No asset acquisition. Pure read-only research.
- **Read-only across all sources.** You can inspect files in the demo repo for metadata; you do NOT modify them.
- **Budget:** $0 LLM (this is web-research + file-inspection scout work; no generation needed)
- **Time cap:** 2 hours. If you hit findings-blockers in Section 1 or 2 (vendor pages don't ship pixel sizes; metadata.json missing intrinsic dims), surface and STOP rather than expand scope.

---

## Acceptance

- Doc lands at `agentic_orchestration/research/knowledge/character-monster-pixel-scale-2026-05-16.md`
- All three primary sections populated (Section 1 + 2 + 3); operational summary in Section 4 actionable
- Per-data-point source attributed (URL or file path)
- Findings-blockers surfaced if Section 1 or 2 cannot be populated from available sources

---

## What this unblocks

- gandalf's per-slug scale lookup table recommendations (cannot finalize without Section 1 + 2 data)
- drax screenshot strip generation calibration (knowing intrinsic source sizes lets drax pick more useful scale-factor candidates than the initial 0.20 / 0.28 / 0.35 anchors)
- knight-rider drax refactor dispatch: convert `DEFAULT_MONSTER_SCALE` to per-slug lookup keyed off `ENEMY_TIER_CHARACTER_MAP`, populated from gandalf's recommendation table
- Forward-reference: when additional monster-track vendors are crawled (per P6.d character-track sub-commission), the same Section 1 + 2 methodology applies — this commission becomes the template

---

— gandalf, 2026-05-16 (Day 4 close)
