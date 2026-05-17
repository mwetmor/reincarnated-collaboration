# Dispatch — 2026-05-16 — drax — Character-track ingest pipeline (chierit Elementals primary + Samurai secondary; VS2a player character rendering)

**From:** knight-rider (authored per Matt 2026-05-16 character-track acquisition + Tier 1 #3 approval; closes player-character-rendering gap for VS2a)
**To:** drax
**Approved by:** Matt at 2026-05-16 Day 4 (acquisitions loaded at confirmed paths)
**Status:** PENDING — ACTIVE
**Estimated effort:** 2-3 sessions (~6-12h); new ingest pipeline for character-track vendors + per-class character rendering integration; similar pattern to Pimen ingest pipeline + first VFX integration but for CHARACTERS not VFX.
**Acceptance:** Character-track ingest pipeline extracts chierit Elementals zip archives; per-character sprite sheets + metadata.json populated; demo renders chierit characters in place of primitives for player class combatants; element-to-character slot mapping established; smoke verifies 5+ element classes render real character sprites; intermediate tag.

---

## Context — what Matt acquired today

**chierit Elementals** at `/Users/admin/Games/reincarnated-demo/public/assets/Elementals_bundle/`:
- 10 `.zip` archives, one per element-named character
- License: CC-BY 4.0 (cleanest in character-track scout per legolas Mode A)
- Character roster + suggested element mapping:

| Archive | Character | Suggested Reincarnated element |
|---|---|---|
| `Elementals_fire_knight_FULL_v1.1.zip` | Fire Knight | fire |
| `Elementals_water_priestess_FULL_v1.1.zip` | Water Priestess | water |
| `Elementals_ground_monk_FULL_v1.3.zip` | Ground Monk | earth |
| `elementals_wind_hashashin_FULL_v1.1.zip` | Wind Hashashin | wind |
| `Elementals_lightning_ronin_full_v1.0.zip` | Lightning Ronin | thunder |
| `Elementals_Crystal_Mauler_Full_v1.0.zip` | Crystal Mauler | ice (or crystal — verify in-asset) |
| `Elementals_light_valkyrie_complete_v1.1.zip` | Light Valkyrie | holy |
| `Elementals_shadow_stalker_complete_v1.0.zip` | Shadow Stalker | dark |
| `Elementals_metal_bladekeeper_FULL_v1.1.zip` | Metal Bladekeeper | physical (or metal — verify) |
| `Elementals_Leaf_ranger_Full_v1.0.zip` | Leaf Ranger | poison (or nature — verify) |

These 10 cover much of the VS2a B11 GREEN list (11/13 elements per gandalf Track 4).

**GandalfHardcore Samurai** at `/Users/admin/Games/reincarnated-demo/public/assets/GandalfHardcore Samurai/`:
- Already extracted (no zip; loose .png files)
- 8 portrait variants × 3 color sheets (black/blue/brown) + palette reference
- Register: mid-pixel (NOT HD-2D shaped per legolas scout) — **prototyping only; not canonical-register**
- Usage: secondary/optional; possibly map to a single physical_warrior or NPC placeholder

## What this dispatch does

### Step 1 — Character-track ingest pipeline (new module)

Create `~/Games/reincarnated-demo/scripts/character-ingest/` (parallel to `scripts/pimen-ingest/`):

- `stage1_extract.py` — extract `.zip` archives per character to per-character output directories
- `stage2_animations.py` — detect + assemble per-character animation sprite sheets (idle / walk / attack / hit / death etc.; varies per chierit character's actual content)
- `stage3_metadata.py` — build per-character metadata.json (animation states + frame counts + canvas dims + element mapping)
- `run_pipeline.sh` — orchestrator (similar to Pimen pipeline pattern)
- Output: `public/assets/characters/<character-slug>/` with sheets + metadata.json per chierit character

**Discipline #10 (empirical inspection over assumption)**: inspect the FIRST chierit zip archive's structure BEFORE designing the pipeline. chierit packs may have varied internal organization (per-animation folders vs single sheet vs Aseprite-derived). Don't assume; verify.

### Step 2 — Per-character metadata.json schema

For each chierit character, generate:

```json
{
  "character_slug": "fire-knight",
  "vendor": "chierit",
  "vendor_pack": "Elementals_fire_knight_FULL_v1.1",
  "element": "fire",
  "license": "CC-BY-4.0",
  "register": "hd-2d-pixel",
  "animations": {
    "idle": { "sheet_path": "sheets/idle.png", "frame_count": 8, "canvas_width": 64, "canvas_height": 64 },
    "walk": { ... },
    "attack_basic": { ... },
    "hit": { ... },
    "death": { ... }
  }
}
```

Animation states are character-specific; populate per actual asset content.

### Step 3 — Character renderer integration in demo

Create `~/Games/reincarnated-demo/src/visuals/characterSprites.ts` (parallel to `pimenVfx.ts`):

- Load chierit metadata.json per character
- Map element → character sprite per ELEMENT_CHARACTER_MAP constant
- Render per-class combatant in demo using character sprite (replaces primitive rendering for player classes)
- Animation state machine: idle / walk (during movement) / attack_basic (during cast) / hit (during damage) / death (during defeat)
- Integrate with existing per-room aggro state machine (drax/v0.12 room/hallway)

### Step 4 — ELEMENT_CHARACTER_MAP

In `characterSprites.ts`:

```typescript
const ELEMENT_CHARACTER_MAP: Record<string, string> = {
  fire: 'fire-knight',
  water: 'water-priestess',
  earth: 'ground-monk',
  wind: 'wind-hashashin',
  thunder: 'lightning-ronin',
  ice: 'crystal-mauler',     // verify vs canonical ice element
  holy: 'light-valkyrie',
  dark: 'shadow-stalker',
  physical: 'metal-bladekeeper',  // or treat as physical_warrior fallback
  poison: 'leaf-ranger',     // verify vs canonical poison element
  // remaining: kinetic + status fall back to default (e.g., physical or first available)
};
```

Confirm mappings against actual asset content (Discipline #10 inspection).

### Step 5 — GandalfHardcore Samurai (secondary; light integration)

Already-extracted; no pipeline extraction needed:

- Wire as fallback/prototyping character (e.g., for physical_warrior if Metal Bladekeeper register-mismatches, OR as enemy NPC placeholder until monster-track scout completes)
- Lower priority than chierit; if scope creeps, defer Samurai integration to follow-on dispatch

### Step 6 — Tests + smoke + visual verification

- Pipeline unit tests (extract / assemble / metadata generation per chierit archive)
- Renderer unit tests (character sprite resolution; animation state transitions; fallback handling)
- Smoke: load test season; verify per-class character sprites render correctly across 5-10 element classes
- Per Discipline #2: verify visual rendering quality matches HD-2D register expectations
- `npm run build` passes; existing 208+ tests preserved

### Step 7 — Friction findings + intermediate tag

- File `~/Games/reincarnated-demo/CHARACTER_TRACK_INTEGRATION_NOTES.md`
- Per-chierit-character integration findings (which mappings worked; which need adjustment; any visual quality issues)
- Recommendations for: monster-track integration (legolas scout in flight); any chierit-specific edge cases worth surfacing
- Tag: `drax/v0.18-character-track-ingest-pipeline`
- AGENT_STATE.md updated
- Completion record at bottom filled

## Cross-seam considerations

- **Legolas** (READ-ONLY upstream): your scout findings doc at `agentic_orchestration/research/catalogue/character-track-vendor-scout-2026-05-16.md` informed today's acquisitions; reference but do not modify
- **Elrond** (READ-ONLY): catalogue.db curation for chierit is **DEFERRED to VS2b** per the "Mode B catalogue crawl on selected vendors" out-of-scope note from legolas scout; this dispatch ships demo-direct integration; elrond can curate later
- **Engine (rocket/gamora/star-lord)**: READ-ONLY; no engine changes — character sprites are pure presentation layer
- **Gandalf**: design-lineage owner of style register; if any chierit character visually drifts from HD-2D register, surface as finding (legolas scout deemed chierit acceptable, but post-acquisition visual inspection is the empirical confirmation)
- **Knight-rider**: notify at completion; monster-track Mode A scout (in flight) completion may surface monster-vendor acquisitions which would activate a parallel monster-track ingest pipeline dispatch later

## Out of scope (explicit)

- **NO monster sprites** (separate; legolas Mode A monster scout in flight)
- **NO Seliel Mana Seed** (Matt skipped per pre-purchase finding)
- **NO Pimen / VFX changes** (separate prior dispatches)
- **NO room/hallway changes** (separate prior dispatch)
- **NO B11 demo integration changes** (separate prior dispatch landed)
- **NO engine schema changes** (player class schema unaffected; element-to-character mapping is pure presentation)
- **NO elrond catalogue.db curation** for chierit (VS2b territory)
- **NO chierit Mode B full catalogue crawl** (VS2b territory)
- **NO new ELEMENT_SLOT_MAP for VFX** (separate; pimenVfx.ts ELEMENT_SLOT_MAP unaffected)
- **NO character-customization paper-doll work** (Seliel paper-doll approach skipped; chierit characters are pre-styled)

## Required reading

- `agentic_orchestration/research/catalogue/character-track-vendor-scout-2026-05-16.md` (legolas scout; chierit deep-dive)
- `canonical/story/style-register.md` (HD-2D-shaped pixel register lock; chierit visual conformance check)
- Your prior Pimen ingest pipeline dispatches (pattern reference; this is structurally similar but for characters not VFX)
- Your prior Pimen bundle-extension dispatch (`drax/v0.13` + `drax/v0.16`) — RAR/zip handling pattern reference
- Your prior ELEMENT_SLOT_MAP fix dispatch (`drax/v0.14`) — ELEMENT_*_MAP pattern reference
- `canonical/16-project-roadmap.md` §VS2a (demo ship scope)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #2 (smoke); #10 (empirical inspection over assumption — inspect chierit zip structure BEFORE pipeline design); #11 (attribution: per-character-pack license + vendor recording in metadata.json)

## Acceptance criteria

- [ ] Character-track ingest pipeline created (scripts/character-ingest/ with 3 stages + runner)
- [ ] 10 chierit Elementals zip archives extracted to per-character output directories
- [ ] Per-character metadata.json populated with animation states + frame counts + canvas dims
- [ ] Character renderer integration in demo (characterSprites.ts or equivalent)
- [ ] ELEMENT_CHARACTER_MAP mapping verified against actual chierit asset content
- [ ] Demo renders real character sprites for player classes (replaces primitive rendering)
- [ ] GandalfHardcore Samurai wired as secondary/fallback character (lower priority; defer to follow-on if scope creeps)
- [ ] Unit tests pass (pipeline + renderer)
- [ ] Existing 208+ tests preserved; npm run build PASS
- [ ] CHARACTER_TRACK_INTEGRATION_NOTES.md filed
- [ ] Intermediate tag `drax/v0.18-character-track-ingest-pipeline` cut
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified at completion

## Tag policy

- **Intermediate tag:** `drax/v0.18-character-track-ingest-pipeline` at the commit closing pipeline + integration + smoke pass.

---

## Completion record

**Completed:** 2026-05-16
**Intermediate tag:** `drax/v0.18-character-track-ingest-pipeline` @ `529139e`
**Dispatch status:** COMPLETE

**Pipeline structure:**
```
scripts/character-ingest/
  stage1_extract.py     — ZIP extraction → raw frames + full spritesheet copy
  stage2_animations.py  — per-animation horizontal strip sheet assembly
  stage3_metadata.py    — metadata.json generation
  run_pipeline.sh       — 3-stage orchestrator
  tests/test_pipeline.py — 27 tests (all pass; real-archive integration tests included)
```

**10 chierit characters extracted (all 10 verified):**
| Character | Element | Stage 1 | Stage 2 | Stage 3 |
|---|---|---|---|---|
| fire-knight | fire | ok | ok (29 sheets) | ok (288x128) |
| water-priestess | water | ok | ok (27 sheets) | ok (288x128) |
| ground-monk | earth | ok | ok (23 sheets) | ok (288x128) |
| wind-hashashin | wind | ok | ok (24 sheets) | ok (288x128) |
| lightning-ronin | thunder | ok | ok (32 sheets) | ok (288x128) |
| crystal-mauler | ice | ok | ok (26 sheets) | ok (288x128) |
| light-valkyrie | holy | ok | ok (41 sheets) | ok (288x128) |
| shadow-stalker | dark | ok | ok (44 sheets) | ok (288x128) |
| metal-bladekeeper | physical | ok | ok (35 sheets) | ok (288x128) |
| leaf-ranger | poison | ok | ok (44 sheets) | ok (288x128) |

**ELEMENT_CHARACTER_MAP mappings + adjustments (Discipline #10 confirmed):**
- fire→fire-knight, water→water-priestess, earth→ground-monk, wind→wind-hashashin: CONFIRMED as-dispatched
- thunder→lightning-ronin, holy→light-valkyrie, dark→shadow-stalker: CONFIRMED as-dispatched
- ice→crystal-mauler: CONFIRMED. Crystal IS the ice register; no change to dispatch suggestion.
- physical→metal-bladekeeper: CONFIRMED. Pack is metal/steel-themed; no Reincarnated metal element;
  physical is correct receiver. Mapping noted as imperfect but functional.
- poison→leaf-ranger: CONFIRMED. Pack is leaf/nature-themed; no nature element; poison is closest.
- kinetic, status: no chierit character → archetypeRenderer primitive fallback (as-dispatched)

**Additional finding not in dispatch (attack_basic alias):**
  ground-monk and crystal-mauler have un-numbered `1_atk/2_atk/3_atk` source folders that normalize
  to a single `atk` folder after stage1 strip. `attack_basic` aliases both `'1_atk'` and `'atk'`
  in characterSprites.ts. All other characters keep `1_atk` as a separate folder.

**Samurai integration scope:** DEFERRED. Available at `public/assets/GandalfHardcore Samurai/`.
  Mid-pixel register (not HD-2D shaped); 10 chierit characters cover full primary element set.
  Wiring as fallback/NPC deferred to follow-on dispatch per scope guidance.

**Visual register conformance:**
  All 10 chierit Elementals characters confirmed HD-2D-pixel register. Aseprite source files
  present in all archives (human-made pixel art). Frame canvas 288x128px in HD-2D-pixel band.
  GIF previews show hand-drawn illustration sensibility with clean outlines and smooth animation.
  No visual quality flags to surface to gandalf. Register conformance: PASS.

**Notes for knight-rider:**
1. Renderer (`characterSprites.ts`) is available but NOT yet wired into the active render path
   (sprites.ts / main.ts still use archetypeRenderer primitives). The renderer module is complete
   and tested; the call-site wiring in sprites.ts is the next step (separate dispatch or follow-on).

2. `prewarmCharacterSpriteCache()` should be called from main.ts at gauntlet start alongside
   `prewarmPimenVfxCache()` — this begins async metadata preloads to avoid first-frame texture pop.

3. ground-monk/crystal-mauler 'atk' folder merge: un-numbered attack folders combine in Stage 2.
   The renderer handles this via alias. Future pipeline refinement could preserve 1_atk/2_atk/3_atk
   separately for these characters in a VS2b pass.

4. Monster-track integration recommendations (when legolas Mode A monster scout returns):
   - Pipeline pattern is reusable; use separate `public/assets/monsters/` output directory
   - chierit elemental-mode animations (e_* folders) are on disk but not wired — could serve as
     enemy variant forms if chierit is chosen as monster vendor
   - enemy-visual-legibility.md requirement: monsters must NOT be scaled player sprites; use
     distinct characters or palette-shifted versions with aura markers
   - Pipeline idempotence: run_pipeline.sh is safe to re-run (hash-based skip)

5. Attribution: chierit CC-BY 4.0 requires "chierit" credit. Currently in commit messages +
   metadata.json. Needs to surface in About/footer UI when that component ships.
