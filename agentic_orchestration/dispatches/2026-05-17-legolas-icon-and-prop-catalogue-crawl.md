# 2026-05-17 — legolas — Icon + interactable-prop catalogue crawl (Mode B)

**Authority:** Matt L3 2026-05-17 (~21:30 EDT). Commission for asset sourcing across 9 categories spanning floor loot, ambient interactable props, and UI icons.
**Type:** Pattern B — Mode B systematic catalogue crawl; ~1-2 days; read-only across vendor sources.
**Predecessor:** gandalf v1.7 mobile-vs-PC pixel sizing & ratio canon (`canonical/story/mobile-pc-pixel-sizing-ratios-2026-05-17.md`) — your sizing target reference; elrond Pimen subset selection pattern (`agentic_orchestration/dispatches/2026-05-17-elrond-pimen-subset-selection-vs2a.md`) — output schema reference.
**Downstream:** Elrond curation dispatch (queued; auto-fires when this crawl lands).

---

## Why this matters

We have well-tuned VFX sourcing (Pimen + CodeManu integration in flight via drax step-3). What's missing is the **prop + icon sourcing layer** that gives the gauntlet visual depth at the non-VFX surfaces:

- **Floor loot** — potions/gold/gear drops on the dungeon floor (currently un-rendered or placeholder)
- **Ambient interactable props** — chests/coffins/weapon-stands/armor-stands/urns-vases-boxes (currently absent)
- **UI icons** — gear/potion/gold icons for inventory + character screen (currently placeholder or absent for character screen, which Matt flagged as "haven't developed yet")

Gandalf's pixel-sizing canon established sizing TARGETS for all of these. Your crawl finds the actual vendor assets that match.

---

## Required reading

1. `canonical/story/mobile-pc-pixel-sizing-ratios-2026-05-17.md` — gandalf's sizing canon (your target):
   - World-sprite mobile = PC × 0.75
   - PIXELS_PER_METER = 48 invariant
   - Touch targets: 88px floor / 110-125px action canon
   - Gear drops ~32px world-space
   - Treasure chests ~80px
   - Vases ~40px (destructibles 0.7-0.9× player-sprite-height)
   - UI icons 110-125px mobile / smaller PC
2. `agentic_orchestration/research/curated/pimen-subset-vs2a-selection-2026-05-17.md` — elrond's output schema reference (you partition similarly)
3. `agentic_orchestration/qa/findings/2026-05-16-gandalf-step-b-gate3-review.md` — Step B Tier-1 vendor candidates (you've crawled some; check baseline)
4. `agentic_orchestration/research/catalogue/` — existing vendor catalogues you've authored (pimen + others?); avoid re-crawling
5. `reincarnated-demo/public/assets/` — current acquired asset inventory (chierit / CreativeKind / Deathbringer / Elementals_bundle / Frostwindz / GandalfHardcore Samurai / Holy_Spell_Effects_Creativekind / Impact FX Pack_Codemanu / pimen / PixelArtRPGVFXLite / characters / monsters)

---

## Scope — 9 categories across 3 sub-asset-classes

### Sub-asset-class 1 — Floor loot (world-space; small sprites)

For each:
- **Potions (health + mana)** — small bottle sprites on floor; per-color variants
- **Gold** — pile sprites; ideally multi-size for stack-amount variation (small/medium/large)
- **Gear drops (weapons / armor / etc.)** — on-floor sprite per gear-type per rarity:
  - White / magic / rare / unique tier variants (ARPG canon)
  - Weapon types: sword / staff / bow / dagger / hammer / wand / shield / axe (or vendor coverage permitting)
  - Armor types: helm / chest / boots / gloves / belt / amulet / ring (or vendor coverage)

Sizing target: ~32px (per gandalf canon).

### Sub-asset-class 2 — Ambient interactable props (world-space; medium sprites)

For each:
- **Chests** — small / medium / large variants; open + closed states (animation frames preferred but separate static sprites acceptable)
- **Coffins** — open + closed; ideally with destruction/transformation frames
- **Weapon stands** — single + grouped variants; with/without weapon placed
- **Armor stands** — single + grouped; helmless/full variants
- **Urns / Vases / Boxes** — multiple visual variants per category; intact + destroyed frames preferred (ARPG canon)

Sizing target: 0.7-0.9× player-sprite-height for destructibles (per gandalf canon); chests ~80px; vases ~40px.

### Sub-asset-class 3 — UI icons (UI-space; clean pixel-perfect at-rest)

For each:
- **Gear icons** — per gear-type per rarity (same matrix as floor drops but UI-clean register):
  - Weapons + armor + accessories
  - White / magic / rare / unique tinted borders or frames
- **Potion icons** — health + mana; ideally with multiple "fill levels" (3/3, 2/3, 1/3, empty)
- **Gold icon** — typically a coin + counter glyph

Sizing target: 110-125px mobile / smaller PC (per gandalf canon).

---

## Vendor crawl list

**Already-known vendors (catalogue may exist; check before re-crawling):**
- Pimen (mega-pack-elemental-icons already in current acquisition — check for prop/loot packs)
- CraftPix (premium; flagged in Phase-2 acquisitions queue for wood-nature)
- Pixogen
- Fellor (crystal-themed; flagged in Phase-2 queue)
- CodeManu (Impact FX Pack acquired today; check their other categories)
- CreativeKind (Holy_Spell_Effects acquired; check icon/prop coverage)
- Frostwindz (Deathbringer character-tier; probably not icons but verify)
- Pipoya (referenced in earlier dispatches)

**Newcomer candidates (your call to crawl):**
- Kenney (CC-0 prolific game-dev asset author)
- OpenGameArt (premium-licensed bundles only — not CC-BY low-effort)
- GameDev Market (commercial)
- Game Art 2D
- Itch.io's game-asset section (filter for commercial license)
- Free-Game-Assets / 7Soul / similar pixel-prolific authors

Crawl breadth at your discretion; explicit-license-clean is the only filter (no unclear-license inclusions).

---

## Output structure

Author your findings at `agentic_orchestration/research/catalogue/icons-and-props-2026-05-17/`:

### File 1 — `floor-loot.jsonl`

Rows per asset:
```json
{
  "asset_id": "vendor.category.subcategory.001",
  "vendor": "<vendor-name>",
  "vendor_url": "<asset-page-url-or-pack-url>",
  "category": "floor-loot",
  "subcategory": "potion" | "gold" | "gear-weapon" | "gear-armor",
  "specific_type": "health-potion" | "mana-potion" | "gold-pile-large" | "sword" | "helm" | etc.,
  "rarity_tier": "white" | "magic" | "rare" | "unique" | null,
  "pixel_size": "32x32" | "48x48" | etc.,
  "attribution_class": "cc-0" | "cc-by" | "commercial-license",
  "pack_origin": "<pack-slug-or-name>",
  "cost_usd": <number or null>,
  "notes": "..."
}
```

### File 2 — `ambient-props.jsonl`

Same schema; `category: "ambient-prop"`; subcategory: chest / coffin / weapon-stand / armor-stand / urn-vase-box.

### File 3 — `ui-icons.jsonl`

Same schema; `category: "ui-icon"`; subcategory: gear-icon / potion-icon / gold-icon.

### File 4 — `summary.md`

Document:
1. Vendors crawled (with citation/URL)
2. Coverage matrix per sub-asset-class (which subcategories are well-covered vs sparse)
3. Sizing-mismatch flags (assets that don't fit gandalf's canon — too small / too large / wrong register)
4. License-status flags (CC-BY rows separately listed; commercial-license rows separately listed)
5. Cost rollup if known (mostly for premium packs)
6. Cross-references to gandalf's sizing canon + the elrond Pimen subset pattern

---

## Out of scope (DO NOT)

- ❌ DO NOT make acquisition decisions (Matt-authority via downstream elrond curation + Matt sign-off)
- ❌ DO NOT modify the elrond Pimen subset manifest (consume schema pattern only)
- ❌ DO NOT crawl unclear-license sources (filter at intake)
- ❌ DO NOT extend to VFX vendor assets (separate scope — drax step-3 covers VFX)
- ❌ DO NOT extend to character/monster sprite catalogues (separate scope — already have those acquisitions)
- ❌ DO NOT pre-empt elrond curation (your output is RAW catalogue; elrond curates the subset)
- ❌ DO NOT make recommendations on interaction-mechanics (loot tables, chest-open animations as gameplay logic — engine/gandalf design seam)

---

## Acceptance criteria

- [ ] Floor-loot JSONL filed
- [ ] Ambient-props JSONL filed
- [ ] UI-icons JSONL filed
- [ ] Summary.md authored (vendors crawled, coverage matrix, license flags, cost rollup)
- [ ] All rows have license-class + pack-origin documented
- [ ] Sizing-mismatch flags noted where applicable
- [ ] Hive-log STATE + HANDOFF → elrond
- [ ] No tag (research/catalogue work; standard authoring discipline applies)

---

## Coordination

- **PRE-SIGNAL § 14.1.1** before hive-log appends; pull-rebase before commits
- **Parallel work in flight:** drax step-3 VS2a first VFX integration + drax SEASON_IDS micro-task (both demo-repo work; you're collab-repo only — no conflict)
- **Pre-authorized for parallel-vendor-crawl breadth:** crawl as broadly as your time allows; elrond curates downstream

---

*Dispatched 2026-05-17 by knight-rider per Matt L3. ~1-2 days. Append completion record when done.*

---

## Completion Record

**Completed:** 2026-05-17 by legolas
**Output path:** `agentic_orchestration/research/catalogue/icons-and-props-2026-05-17/`
**Files:**
- `floor-loot.jsonl` — 29 rows (potions: 10, gold: 7, gear-weapon: 7, gear-armor: 5)
- `ambient-props.jsonl` — 23 rows (chests: 8, coffins: 2, weapon-stands: 5, armor-stands: 3, urns/vases/boxes: 5)
- `ui-icons.jsonl` — 25 rows (gear-icons: 9, potion-icons: 9, gold-icons: 7)
- `summary.md` — vendors crawled, coverage matrix, sizing flags, license flags, cost rollup, vendor breadth map

**Acceptance criteria:**
- [x] Floor-loot JSONL filed
- [x] Ambient-props JSONL filed
- [x] UI-icons JSONL filed
- [x] Summary.md authored
- [x] All rows have license-class + pack-origin documented
- [x] Sizing-mismatch flags noted
- [x] Hive-log STATE + HANDOFF appended
- [x] No tag (research/catalogue work)

**Key findings:**
- Pimen: VFX-only confirmed — zero icon/prop/loot content
- Best comprehensive pack: Dire Dungeon Items ($10, CC BY 4.0, 259 items)
- Best prop pack: Mucho Pixels Dungeon Tileset ($4.95 — chest+coffin+weapon-stand+pots with states)
- Rarity-border system: NOT FOUND in any vendor catalogue — custom authoring required
- AI-assisted flag: Pixel-1992 packs
- CC-BY-SA flag: OGA Clint Bellanger gold icons (share-alike clause)
- Sizing gap: all packs 16x16 or 32x32 native; 110-125px UI target bridged by drax frame/slot pipeline
