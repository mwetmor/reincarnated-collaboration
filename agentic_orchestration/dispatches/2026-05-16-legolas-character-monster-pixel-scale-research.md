# Dispatch — 2026-05-16 — legolas — Mode A research: character + monster pixel-scale empirical data

**From:** knight-rider (authored per gandalf request file `agentic_orchestration/gandalf/requests/2026-05-16-legolas-character-monster-pixel-scale-research.md`; Matt-relayed Day 4 close)
**To:** legolas
**Approved by:** Matt at 2026-05-16 Day 4 (relayed gandalf's commission with explicit endorsement framing)
**Status:** PENDING
**Mode:** A (analytical web research; read-only)
**Estimated effort:** 1-2 hours; hard time cap at 2 hours.
**Budget:** $0 LLM (research + file inspection only)
**Gate-1 bypass rationale:** Matt-directed (via gandalf), single-seam (legolas-only), read-only, bounded time cap, reversible (research output is a doc — does not modify any production state). Per CHANGELOG rubric.

**Acceptance summary:** Single research-findings doc at `agentic_orchestration/research/knowledge/character-monster-pixel-scale-2026-05-16.md` with three primary sections (chierit intrinsic sizes / CreativeKind intrinsic sizes / HD-2D shipped-game reference) + synthesis table. Per-data-point source attributed (URL or file path). Findings-blockers surfaced if any section cannot be populated from available sources. Time-cap honored.

---

## Why this commission exists

Gandalf is authoring the per-slug scale lookup table that drax's eventual `MONSTER_SCALE_BY_SLUG` refactor dispatch will consume. Without empirical intrinsic-pixel-size data + HD-2D shipped-game reference measurements, gandalf's recommendations are "eyeballing the screenshot strip" — workable but not falsifiable. Your research grounds the table in measured data.

Gandalf's genre-side framework is already authored (Day 4 council response: Diablo size hierarchy + HD-2D pixel-art register + per-tier ratio recommendations). This commission fills the three empirical gaps gandalf cannot supply from training alone.

## Cross-seam contract change?

**Round-trip: not applicable** — research output is a read-only doc; no contract changes; no production state modified. Per R11(b) Principle 6.

## What this dispatch produces

Single doc at: `agentic_orchestration/research/knowledge/character-monster-pixel-scale-2026-05-16.md`

### Section 1 — chierit Elementals intrinsic source-sheet pixel sizes (HIGH priority)

For each of the 10 chierit archives currently at `/Users/admin/Games/reincarnated-demo/public/assets/Elementals_bundle/`, document:

- Archive filename (e.g., `Elementals_fire_knight_FULL_v1.1.zip`)
- Character name (Fire Knight, Water Priestess, Ground Monk, etc.)
- **Intrinsic frame dimensions** (e.g., 288×128, 64×64) — source-sheet pixel size per animation frame BEFORE any scale factor applied
- Animation frame counts per state (idle / walk / attack / hurt / death)
- Anchor point convention (top-left? center? feet?)
- Any per-character metadata.json content relevant to scale

**Sources (priority order):**
1. chierit itch.io asset pages (primary; canonical author docs)
2. Existing metadata.json files in `/Users/admin/Games/reincarnated-demo/public/assets/Elementals_bundle/` (secondary; drax-extracted)
3. Direct file inspection if neither covers it (use `unzip -l` or similar; do NOT modify archives)

**Knight-rider note:** drax's `characterSprites.ts:31` empirically confirmed chierit frames as 288×128 across all 10 characters. Verify and extend with frame-count + anchor data per character.

### Section 2 — CreativeKind monster vendor intrinsic source-sheet pixel sizes (HIGH priority)

For each of the 11 VS2a monsters in `ENEMY_TIER_CHARACTER_MAP` (drax-canonical, in `~/Games/reincarnated-demo/src/visuals/monsterSprites.ts:73`):

- `goblin-mage` (trash)
- `mutant-skeleton` (trash)
- `evil-eye` (trash)
- `sword-warrior` (trash)
- `crystal-golem` (elite)
- `fire-elemental` (elite)
- `demon-mage` (elite)
- `lich` (mini_boss)
- `hellfire-rhino` (mini_boss)
- `angel-guardian` (boss / act_boss)
- `god-of-lightning` (boss / act_boss)

Per monster:
- Source vendor (confirm CreativeKind for all; flag any from other vendors)
- Pack name / archive name
- **Intrinsic frame dimensions** per animation frame
- Combined-sheet vs per-animation-separated (drax flagged some as combined-sheet — Crystal_Golem, Mutant_Skeleton, etc.; confirm which)
- Animation frame counts per state
- Anchor point convention

**Sources:**
1. CreativeKind asset pages (vendor docs)
2. Source-sheet files on disk at `/Users/admin/Games/reincarnated-demo/public/assets/CreativeKind/`
3. Drax's v0.20 ingest-pipeline output (metadata sidecar files in `~/Games/reincarnated-demo/scripts/monster-ingest/` or in `MONSTER_TRACK_INTEGRATION_NOTES.md`)
4. Drax's v0.20.1 completion record (`drax/v0.20.1-sprite-scale-strip-and-black-screen-fix`) explicitly notes: Angel 256×192, Lich 176×128, evil-eye 64×64 — extend with the remaining 8

### Section 3 — HD-2D pixel-art shipped-game character height reference (MEDIUM priority)

Specific pixel heights of player-character sprites in shipped HD-2D titles at 1080p default camera distance. Three reference titles:

- **Sea of Stars (Sabotage, 2023)** — Zale or Valere at world-map default zoom
- **Octopath Traveler (Square Enix, 2018)** — any of the 8 protagonists at default field-exploration zoom
- **Eiyuden Chronicle: Hundred Heroes (505 Games, 2024)** — protagonist at default exploration zoom

**Sources:**
- Gameplay screenshots from major review sites (IGN, GameSpot, RPS, EGM) at confirmed 1080p
- YouTube gameplay video frame-grabs (document the URL + timestamp for traceability)
- Existing forum / GameDev / pixel-art-community discussions on HD-2D sprite scales

**Method:** measure character pixel height at ground level (feet to top of head, not including hair/hat protrusions) on screenshots confirmed at 1080p native rendering.

**Tolerance:** ±5 px acceptable. Goal is to confirm the 80-100 px HD-2D-register range, not pixel-precision.

### Section 4 — Operational synthesis (your work product)

Close the doc with a synthesis table:

- chierit characters: target rendered pixel height in Reincarnated demo to match HD-2D register → recommended scale factor per character
- 11 monsters: target rendered pixel height per tier (per gandalf's recommendation table — swarm 55-75px, elite 90-115px, mini-boss 130-180px, boss 225-360px) → recommended scale factor per monster
- Flag any monsters where intrinsic source-sheet pixel size makes the target ratio mathematically impossible without quality loss (e.g., a 32×32 source can't render at 200 px tall cleanly without upscaling artifacts)

The synthesis is the actionable artifact drax + gandalf consume directly.

## Constraints (gandalf-locked)

- **Mode A strictly.** No catalogue crawl. No vendor outreach. No asset acquisition.
- **Read-only across all sources.** You may inspect files in the demo repo for metadata; do NOT modify them.
- **Budget:** $0 LLM. Pure web research + file inspection.
- **Time cap: 2 hours.** If you hit findings-blockers in Section 1 or 2 (vendor pages don't ship pixel sizes; metadata.json missing intrinsic dims), surface and STOP rather than expand scope.

## Out of scope (explicit)

- **NO Mode B catalogue crawl.** This commission is bounded analytical research, not a vendor inventory pass.
- **NO acquisition recommendations.** Out of scope; that's separate vendor-discovery work.
- **NO scale-factor recommendations BEYOND the synthesis table.** The lookup-table authorship is gandalf's work; you supply the empirical inputs and surface mathematical constraints.
- **NO commentary on whether to expand to additional vendors.** P6.d character-track sub-commission is queued separately; this commission is bounded to the current 11+10 pool.

## Required reading

- `agentic_orchestration/gandalf/requests/2026-05-16-legolas-character-monster-pixel-scale-research.md` (gandalf's full spec)
- `~/Games/reincarnated-demo/public/assets/Elementals_bundle/` (chierit archives + any metadata)
- `~/Games/reincarnated-demo/public/assets/CreativeKind/` (monster source sheets)
- `~/Games/reincarnated-demo/MONSTER_TRACK_INTEGRATION_NOTES.md` (drax-authored; may contain intrinsic-size notes)
- `~/Games/reincarnated-demo/CHARACTER_TRACK_INTEGRATION_NOTES.md` (drax-authored)
- Drax v0.20.1 completion record (notes 3 monster intrinsic sizes; extend)

## Acceptance criteria

- [ ] Doc lands at `agentic_orchestration/research/knowledge/character-monster-pixel-scale-2026-05-16.md`
- [ ] Section 1 populated for all 10 chierit characters (or findings-blocker surfaced)
- [ ] Section 2 populated for all 11 monsters (or findings-blocker surfaced)
- [ ] Section 3 populated for at least 2 of 3 HD-2D reference titles (or findings-blocker)
- [ ] Section 4 synthesis table actionable (recommended scale per character + per monster + flagged mathematical-impossibility cases)
- [ ] Per-data-point source attributed (URL or file path)
- [ ] Time-cap honored (≤ 2 hours)
- [ ] Knight-rider notified at completion with: doc path, section-completeness status (all 3 / some blocked), any surprising findings

## Tag policy

- **No git tag** (research output; legolas commissions don't tag per persona rules)
- File timestamp + git commit on the research output doc suffices for traceability.

---

## Completion record

**Completed:** _<date>_
**Doc path:** _<path>_
**Sections populated:** _<S1/S2/S3 status>_
**Findings-blockers (if any):** _<list>_
**Total time:** _<minutes>_
**Notes for knight-rider:**
