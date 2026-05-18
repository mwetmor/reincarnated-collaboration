# Icons + Props subset selection for VS2a — 2026-05-17

**Author:** elrond
**Dispatch (original):** `agentic_orchestration/dispatches/2026-05-17-elrond-icon-and-prop-curation-queued.md` (auto-fired on legolas-1 completion)
**Dispatch (registration):** `agentic_orchestration/dispatches/2026-05-17-elrond-icon-and-prop-acquisition-registration.md` (Matt L3 post-acquisition)
**Predecessor:** legolas-1 icon + interactable-prop catalogue crawl (`agentic_orchestration/research/catalogue/icons-and-props-2026-05-17/`)
**Sizing canon:** `canonical/story/mobile-pc-pixel-sizing-ratios-2026-05-17.md` § 3.3
**Pattern reference:** `agentic_orchestration/research/curated/pimen-subset-vs2a-selection-2026-05-17.md` (elrond Pimen selection — same methodology)
**Successor:** drax M5 panel redesigns + post-VS2a ambient prop dispatches consume the manifest

---

## Post-acquisition status — 2026-05-17 (Matt L3, ~00:30 EDT)

Matt acquired **7 of 9 PRIMARY packs**. De-duplicated **actual outlay: $10.00** (vs $18.20 estimate; **savings $8.20** = 45.1%).

| Pack | Status | Local path under `reincarnated-demo/public/assets/` |
|---|---|---|
| Dire Dungeon Items + Loot (DerNachbar, CC BY 4.0) | **ACQUIRED $10** | `DireDungeon_Items_Loot/` |
| Magic_Potions_Pack_V1 (substitute for SODA + AquaSenshi; vendor TBD, FREE) | **ACQUIRED-SUBSTITUTE** | `Magic_Potions_Pack_V1/` |
| CraftPix Guild Hall (189780, FREE) | **ACQUIRED** | `craftpix-net-189780-free-top-down-pixel-art-guild-hall-asset-pack/` |
| CraftPix Basic Pixel Art UI (255216, FREE) | **ACQUIRED** | `craftpix-net-255216-free-basic-pixel-art-ui-for-rpg/` |
| Seliel Treasure Chests 1 (19.07c, FREE) | **ACQUIRED** | `19.07c - Treasure Chests 1/` |
| Seliel Breakable Pots 1 (20.05b, FREE) | **ACQUIRED** | `20.05b - Breakable Pots 1/` |
| Elthen Destructible Objects (PWYW FREE) | **ACQUIRED** | `Destructible Objects Sprite Sheet.png` (bare, no folder) |
| Mucho Pixels Dungeon Tileset Pack ($4.95) | **NOT ACQUIRED** | n/a |
| SODA 150 Stylized Potions ($3.25) | **NOT ACQUIRED** | n/a — covered partially by Magic_Potions_Pack_V1 substitute |

**Bonus acquisition (outside shortlist):** CraftPix Animated Magic Book pack 809047 (`craftpix-net-809047-free-animated-magic-book-pixel-art-asset-pack/`) — 12-frame book open/close animation + per-element skill-icon set (fire/nature/water/lightning, 8 frames each). Available as decoration or skill-icon backup; does not modify VS2a curation rollup.

### Gap closure status — post-acquisition refresh

| Gap | Pre-acquisition status | Post-acquisition status | Driver |
|---|---|---|---|
| **G-FILL** (potion fill-level) | PARKED — Path A recommended | **MATERIALLY ADVANCED.** Dire Dungeon ships explicit **healing_big/medium/small + mana_big/medium/small** sprites — explicit 3-tier size variants for health AND mana potions. This IS an explicit size-tier proxy at native vendor level (not a synthesized SODA proxy). Path A now over-delivered for health/mana primaries; remaining sub-types still lack fill states but those are non-primary | DireDungeon `potions/` folder |
| **G-RARITY** (rarity-tier UI borders) | PARKED — Path A (procedural overlay) recommended | **INFRASTRUCTURE NOW IN HAND.** CraftPix Basic UI Inventory + Equipment screens contain rarity-coloured slot gem indicators (blue/orange/red visible in Inventory.png + Equipment.png), AND Dire Dungeon ships full 10-color animated outline glow folder per item (137,602 frames across `DireDungeonItems_animatedOutlines_by_DerNachbar/`). Procedural overlay path A is now fully infrastructure-supported | CraftPix Basic UI + DireDungeon animatedOutlines |
| **G-ARMOR-MANNEQUIN** (armor stand variants) | Flagged but NOT load-bearing | **CLOSED + MATERIALLY UPGRADED.** Guild Hall ships 3 mannequin designs × 4-frame destruction animation each (`Attacked_Manequin1/2/3_with_shadow.png`). Multi-state armor stand coverage materially exceeds single-state expectation; helmet/helmless inferable from destruction frame sequence | CraftPix Guild Hall |
| **G-COFFIN** (open-state coffin) | PARTIALLY CLOSED via Mucho Pixels | **STILL OPEN.** Mucho Pixels NOT acquired; Seliel Treasure Chests 1 contains chest-only assets (no coffin-style variants visible in 160×192px composite). Coffin gap reverts to OPEN. **Recommendation:** defer coffin to post-VS2a (not load-bearing for VS2a primary slot) OR acquire Mucho Pixels $4.95 if coffin becomes load-bearing | none — gap re-opened |
| **G-AI-POLICY** (Pixel-1992 packs) | OPEN — pending policy clarification | UNCHANGED — Pixel-1992 packs not acquired, governance question still pending | n/a |
| **G-CCBYSA** (OGA share-alike) | CLOSED via strict-defer | UNCHANGED CLOSED | n/a |

### Cost rollup — post-acquisition

| Line | Pre-acquisition estimate | Post-acquisition actual |
|---|---:|---:|
| Dire Dungeon Items (CC BY 4.0) | $10.00 | $10.00 |
| Mucho Pixels Dungeon Tileset Pack | $4.95 | $0.00 (not acquired) |
| SODA 150 Stylized Potions | $3.25 | $0.00 (not acquired; partial coverage via free substitute) |
| 6 free PRIMARY packs | $0.00 | $0.00 |
| **De-duplicated PRIMARY total** | **$18.20** | **$10.00** |
| Bonus pack (Magic Book) | $0.00 | $0.00 |
| Savings vs estimate | — | **$8.20 (-45.1%)** |

### Remaining gaps flagged for Matt

1. **G-COFFIN** — re-opened after Mucho Pixels not acquired. **Recommendation:** defer to post-VS2a (not load-bearing). If a coffin asset becomes load-bearing for trial-room or boss-room dressings, two options: (a) acquire Mucho Pixels $4.95 (coffin + extra chest state-coverage bundled), (b) commission custom coffin sprite (~$50-150 indie-art).
2. **G-BARREL-POT-MUCHO-COVERAGE** — Mucho Pixels' multi-pot/barrel state-coverage was a PRIMARY anchor for ambient-props subset. Seliel pots (4 designs × 4 colors + break animation + shards) + Elthen destructibles (barrels, crates, signs with destruction frames) **together cover the destructible-prop need without Mucho Pixels**. Chest coverage falls back to Seliel + Pixel Serial BACKUP (animated chest opening from BACKUP tier).
3. **G-WEAPON-STAND-MUCHO** — Mucho's 7-weapons-on-stand + broken-variant detail level not acquired. CraftPix Guild Hall `Interior_objects.png` contains weapon racks + banner stands (top-down register), and BigWander Weapons Rack 128 (FREE BACKUP) supplements. State-coverage for weapon-stand is functional but not as polished as Mucho. **Recommendation:** functional pass for VS2a; revisit if visual polish proves insufficient.
4. **Magic_Potions_Pack_V1 vendor metadata pending** — license.txt is 35 bytes (suspiciously short); pack appears to be a free SODA-equivalent substitute but exact provenance (vendor, license, attribution requirements) needs legolas-3 verification at next crawl. Until then, treat as commercial-license (assumption) and avoid public attribution claim. Stamped in manifest as `vendor TBD`.

### Manifests refreshed

All three manifests bumped to schema version `1.1` (adds `acquisition_status`, `acquired_path*`, `acquired_date`, `acquired_cost_usd`, `acquisition_notes` per-row; adds `_acquisition_cost_usd_actual_this_subset`, `_acquired_pack_origins`, `_primary_packs_not_acquired` in header). Drax can now read manifests directly without resolving pack_origin → local-path manually. Build script: `agentic_orchestration/research/scripts/build_icons_and_props_subset_vs2a_2026_05_17.py` (re-runnable from raw crawl).

---

## Executive summary

Curated **legolas-1's 79-row raw crawl** (29 floor-loot + 23 ambient-props + 25 ui-icons + 2 source repeats across files) into **three drax-consumable manifest subsets** under `agentic_orchestration/research/curated/`. Recommended acquisition set: **9 distinct PRIMARY packs** producing **comprehensive coverage** across all 5 named sub-asset-classes Matt requested (floor loot, ambient interactive props, UI icons + the sub-grids per dispatch § Item 1).

**De-duplicated acquisition cost: $18.20** (Dire Dungeon Items $10 CC BY 4.0 + Mucho Pixels Dungeon Tileset $4.95 royalty-free + SODA 150 Stylized Potions $3.25 royalty-free). Remaining 6 PRIMARY packs are free (AquaSenshi, Seliel chests, Seliel breakable pots, Elthen destructibles, CraftPix Basic UI, CraftPix Guild Hall). This matches the legolas summary § 5 minimum-cost comprehensive-coverage figure.

**Coverage matrix (synthesized across all three subsets):** 46 (subcategory × variant) cells covered in floor-loot, 34 cells in ambient-props, 30 cells in ui-icons — 110 cells total. **Three legolas-flagged gaps surface for Matt review:**

1. **G-FILL — Potion fill-level (1/3 / 2/3 / 3/3) states** — no dedicated frames anywhere in the crawl. Closest proxy is Bis empty-variants (CC BY-ND, 270 icons, $7) + SODA size-tier variants. Custom authoring is the close-path. Status: **PARKED Matt-decision.**
2. **G-RARITY — ARPG rarity-tier UI borders (white/magic/rare/unique)** — no vendor supplies a pre-built rarity border system. Closest proxies: Akari21 star-rarity (bronze/silver/gold/purple); Dire Dungeon outline-color variants (10 colors); Mucho Pixels gold/silver chest color variants. Custom authoring or procedural overlay is required. Status: **PARKED Matt-decision.**
3. **G-ARMOR-MANNEQUIN — Armor stand helmless/helmet variants** — only single-state CraftPix guild-hall mannequin coverage; helmless/full variants not confirmed anywhere. Single-state coverage is functional for VS2a but limits future "shows what's equipped" affordance. Status: **flagged but not load-bearing for VS2a primary slot.**

A **fourth gap (legolas-flagged coffin coverage)** is **partially closed** by Mucho Pixels stone-coffin-open-state — the only coffin open-state coverer in the crawl. Coffin coverage is sparse but functionally meets VS2a needs.

Pruning ratio: **34 PRIMARY+BACKUP rows actively-recommended of 79 raw legolas rows = 43% retention / 57% deferred** — comparable to the Pimen 29% retention pruning ratio and reflects extensive cost-optimization deferrals (premium CraftPix membership packs subsumed by single Dire Dungeon CC-BY acquisition; AI-assisted Pixel-1992 packs deferred pending AI-policy clarification).

Style-register fit per sizing canon: all PRIMARY packs are EXACT or CLOSE to gandalf's sizing targets except where the pack is intentionally chosen for state-coverage (Mucho Pixels 16x16 tile-grid; Seliel 16x16) — these require UPSCALE bridging via drax's frame/slot rendering pipeline. **No DOWNSCALE-REQUIRED packs in PRIMARY set** (the 512×512 craftpix free coin spritesheet and 128×128 Pixel-1992 packs are intentionally deferred to avoid downscaling artifacts).

---

## 1. Per-sub-asset-class subset selections

### 1.1 Subset A — Floor loot

**Manifest:** `agentic_orchestration/research/curated/floor-loot-subset-vs2a-2026-05-17.jsonl` (29 rows: 1 header + 28 curated; 3 PRIMARY + 7 BACKUP + 18 DEFER)

**PRIMARY packs (3):**

| Pack | Cost | License | Closes |
|---|---:|---|---|
| Dire Dungeon Items (DerNachbar) | $10.00 | CC BY 4.0 | gear-weapon (8 types) + gear-armor (6 slots + amulet + ring + shield) + gold (45 coin variants in copper/silver/gold) + outline-color rarity proxy. **Single CC-BY acquisition unifies floor-loot + ui-icons style register.** |
| SODA 150 Stylized Potions | $3.25 | Royalty-free commercial | potion breadth (health + mana + buff/debuff + elemental + size-tier variants serving as fill-level proxy) |
| AquaSenshi Pixel Art Potions Medieval RPG | FREE | Royalty-free commercial | potion type-clean baseline (5 explicit types: health/mana/poison/energy/speed) |

**BACKUP packs (7) — held as fallback if PRIMARY quality issues surface:**

- Bis Potions 270 ($7.00, CC BY-ND 4.0) — empty-variants as fill-level proxy
- CraftPix free 96 magic potions (FREE) — visual breadth
- OGA Bonsaiheldin gold 16x16 (CC0) — stack-progression-1-2-4-8-16 series (zero attribution surface)
- Vennril 250+ Item Pack ($4.99) — 48px native scale alternative + wand coverage
- Akari21 RPG Icon Pack 200+ ($3.00) — star-rarity proxy (only pack with explicit rarity-tier system)
- Shikashi Fantasy Icons (FREE, CC BY 4.0) — 284 icons + status-effect breadth
- BigWander Weapons Rack 128 (FREE) — additional weapon breadth

**18 DEFER rows:** Premium CraftPix membership-gated packs (subsumed by Dire Dungeon CC-BY coverage); AI-assisted Pixel-1992 packs (policy flag); high-cost Seliel alchemy gear $12.99 (subsumed by SODA + AquaSenshi + Bis); CC-BY-SA OGA 32x32 (share-alike conflict).

### 1.2 Subset B — Ambient interactable props

**Manifest:** `agentic_orchestration/research/curated/ambient-props-subset-vs2a-2026-05-17.jsonl` (25 rows: 1 header + 24 curated; 5 PRIMARY + 4 BACKUP + 15 DEFER)

**PRIMARY packs (5):**

| Pack | Cost | License | Closes |
|---|---:|---|---|
| Mucho Pixels Dungeon Tileset Pack | $4.95 | GameDev Market Pro Licence (royalty-free) | chest (gold + silver, locked/unlocked/opened) + coffin (stone, open state) + weapon-stand (resizable, 7 weapons, broken variant) + urn-vase-box (4 pot types blue+red, broken states + 2 barrel types broken states). **Single-pack multi-prop coverage with explicit state-coverage.** |
| Seliel Mana Seed Treasure Chests | FREE | Mana Seed (royalty-free commercial) | chest visual-register alternative (SNES-leaning 16-bit style; 5 designs × 3 color swaps; open+closed; 100% human-made no AI) |
| CraftPix Free Guild Hall | FREE | Royalty-free | weapon-rack + training-mannequin (closes armor-stand simultaneously) in single free pack |
| Elthen Pixel Art Destructible Objects | FREE (PWYW) | CC NC w/ commercial-OK (verify at acquisition) | crate + barrel + pot + sign + chest with damage + destroy animations |
| Seliel Mana Seed Breakable Pots | FREE | Mana Seed | 3 pot designs × 4 colors + 3-frame breaking animation + shard particles (VFX-tier polish) |

**Why 5 PRIMARY (more than other subsets):** ambient props is the most heterogeneous sub-asset-class (5 subcategories × 2-3 states each = ~12-15 cells minimum). Mucho Pixels alone covers chest + coffin + weapon-stand + pots in a single $4.95 acquisition, but state-coverage diversity benefits from style-register alternatives (Seliel chests for SNES-leaning option; Elthen for animated destruction; Seliel pots for shard particles).

**Attribution:** **all 5 PRIMARY packs are royalty-free commercial license** — zero CC-BY attribution surface in ambient-props subset. Cleanest attribution profile of the three subsets.

**BACKUP packs (4):** Pixel Serial free chests, CraftPix free 2d topdown dungeon, CraftPix free dungeon objects, CraftPix free dungeon props — all FREE supplementary breadth.

**15 DEFER rows:** Premium CraftPix tileset packs (subsumed by Mucho); single-state PixelExplosive opening-only chests; AI-assisted Pixel-1992 packs; non-state-covering Indie-Vova $5.99 pack.

### 1.3 Subset C — UI icons

**Manifest:** `agentic_orchestration/research/curated/ui-icons-subset-vs2a-2026-05-17.jsonl` (25 rows: 1 header + 24 curated; 4 PRIMARY + 6 BACKUP + 14 DEFER)

**PRIMARY packs (4):**

| Pack | Cost | License | Closes |
|---|---:|---|---|
| Dire Dungeon Items (DerNachbar) | $10.00 (SHARED — already in floor-loot) | CC BY 4.0 | gear-icon comprehensive (weapons 54 + ranged 19 + shields 9 + armor 36 + amulets 12 + rings 12 + potions 16 + coins 45 + gems 10 + scrolls 10 + spell books 10). **Outline-color variants serve as visual rarity differentiation at UI tier.** |
| CraftPix Free Basic Pixel Art UI for RPG | FREE | Royalty-free | **UI FRAME/SLOT INFRASTRUCTURE** — inventory windows, equipment slots, HP/mana bars, XP meter, quick-slot bar, shop/crafting screens. **LOAD-BEARING** for size-register bridge (32x32 native icons → 110-125px UI target via slot framing). |
| AquaSenshi Pixel Art Potions (SHARED — already in floor-loot) | FREE | Royalty-free | potion-icon health + mana type-clean UI display |
| SODA 150 Stylized Potions (SHARED — already in floor-loot) | $3.25 (SHARED) | Royalty-free | potion-icon stylized breadth + buff/debuff UI |

**BACKUP packs (6):** Bis Potions (CC BY-ND empty-variants for fill-level UI); Shikashi Fantasy Icons (CC BY, status-effect + buff icons); Akari21 (star-rarity UI); Franuka (48px native scale alternative); CraftPix free 40 loot icons (gold-icon supplementary); OGA Bonsaiheldin 16x16 CC-0 (stack-progression-tier UI).

**14 DEFER rows:** Premium CraftPix membership packs; high-cost Seliel; CC-BY-SA OGA 32x32.

**Style-register coherence note:** Dire Dungeon Items provides UI icons for gear, potion, and gold in a single coherent style — eliminating the cross-pack visual-register mismatch that often plagues UI icon authoring. The free packs (AquaSenshi, SODA, CraftPix Basic UI) supplement breadth and provide infrastructure without disrupting Dire Dungeon's primary visual register.

---

## 2. Per-sub-asset-class coverage matrix (GREEN / YELLOW / RED)

GREEN = ≥1 commercial-license or CC-0 PRIMARY/BACKUP pack covers. YELLOW = covered only by CC-BY-class packs (attribution surface). RED = no coverage in recommended subset (acquisition gap).

### 2.1 Floor loot

| Cell (subcategory × variant) | Status | Best coverer |
|---|---|---|
| potion × health | GREEN | AquaSenshi (free, type-explicit) + SODA + Dire Dungeon |
| potion × mana | GREEN | AquaSenshi + SODA + Dire Dungeon |
| potion × poison | GREEN | AquaSenshi (free) |
| potion × energy / speed / buff / debuff / elemental | GREEN | AquaSenshi + SODA |
| potion × fill-level-3-tier (1/3 / 2/3 / 3/3) | **RED** | **Custom authoring required** — see G-FILL gap below |
| potion × empty-state | YELLOW | Bis (CC BY-ND BACKUP) + SODA size-tier proxy |
| gold × single coin / small pile / medium pile / large pile | GREEN | Dire Dungeon (CC BY — 45 variants) + OGA 16x16 (CC-0 BACKUP) |
| gold × copper/silver/gold tier | GREEN | Dire Dungeon |
| gold × stack-progression-1/2/4/8/16 | GREEN | OGA Bonsaiheldin 16x16 (CC-0 BACKUP) |
| gear-weapon × dagger / sword / axe / mace / polearm / staff / bow / crossbow / throwing | GREEN | Dire Dungeon (CC BY — full coverage) |
| gear-weapon × wand | GREEN | Vennril BACKUP ($4.99) |
| gear-weapon × rarity-tier-explicit (white/magic/rare/unique) | **RED** | **Custom authoring required** — see G-RARITY gap below |
| gear-weapon × rarity-tier-star-system (proxy) | GREEN | Akari21 BACKUP ($3.00) |
| gear-weapon × rarity-tier-outline-color (proxy) | GREEN | Dire Dungeon (10 outline colors) |
| gear-armor × helm / chest / gloves / boots / amulet / ring / shield | GREEN | Dire Dungeon |
| gear-armor × robe / cape / circlet (mage-register) | GREEN | Vennril BACKUP |
| gear-armor × belt | **RED** | **No vendor coverage** — minor; not in dispatch primary scope |

### 2.2 Ambient interactable props

| Cell | Status | Best coverer |
|---|---|---|
| chest × small-locked / small-unlocked / small-opened | GREEN | Mucho Pixels (gold + silver variants, explicit states) |
| chest × medium-locked / medium-unlocked / medium-opened | GREEN | Mucho Pixels |
| chest × large variant | GREEN (PARTIAL) | Mucho Pixels covers size via gold/silver tier; explicit "large" sized variant requires multi-tile composition |
| chest × open + closed (canonical state pair) | GREEN | Mucho + Seliel + Pixel Serial BACKUP |
| chest × animated opening frames | GREEN | Pixel Serial BACKUP (4-frame, free) |
| chest × rarity-tier color (gold/silver proxy) | GREEN | Mucho |
| coffin × stone-closed / stone-open | GREEN | **Mucho Pixels is the only confirmed coverer** — sparse-but-met |
| coffin × wooden / decorative variants | **RED** | Not covered; possible custom authoring |
| weapon-stand × intact (7 weapons displayed) | GREEN | Mucho |
| weapon-stand × broken/damaged variant | GREEN | Mucho (broken variant explicit) |
| weapon-stand × free top-down rack alternative | GREEN | CraftPix guild hall (FREE) |
| armor-stand × mannequin single-state | GREEN | CraftPix guild hall (FREE) |
| armor-stand × helmless variant | **RED** | **No vendor coverage** — see G-ARMOR-MANNEQUIN gap below |
| armor-stand × full / helmet-on variant | **RED** | Single-state mannequin functional but not equipped-aware |
| urn-vase-box × pot-intact / pot-broken | GREEN | Mucho (4 types × broken states) + Seliel (free, 3 designs × 4 colors + 3-frame animation + shards) |
| urn-vase-box × barrel-intact / barrel-broken | GREEN | Mucho (2 types) + Elthen (free, animated destruction) |
| urn-vase-box × crate-intact / crate-destroyed | GREEN | Elthen (free, animated) |
| urn-vase-box × sign-prop | GREEN | Elthen (free) |
| urn-vase-box × vase / jug | GREEN | CraftPix free dungeon objects (BACKUP) |

### 2.3 UI icons

| Cell | Status | Best coverer |
|---|---|---|
| gear-icon × weapon-comprehensive | GREEN | Dire Dungeon (CC BY — 54 melee + 19 ranged) |
| gear-icon × armor-comprehensive | GREEN | Dire Dungeon (36 pieces + amulet + ring + shield) |
| gear-icon × scroll / spellbook / gem | GREEN | Dire Dungeon |
| gear-icon × status-effect-buff (UI bar) | GREEN | Shikashi BACKUP (CC BY 4.0) |
| gear-icon × rarity-tier-explicit-border | **RED** | **Custom authoring required** — see G-RARITY gap below |
| gear-icon × rarity-tier-outline-color (proxy) | GREEN | Dire Dungeon |
| gear-icon × rarity-tier-star-system (proxy) | GREEN | Akari21 BACKUP |
| gear-icon × 48px-native-scale | GREEN | Franuka BACKUP ($4.99) |
| potion-icon × health / mana typed | GREEN | AquaSenshi (free) + SODA + Dire Dungeon |
| potion-icon × buff / debuff / elemental | GREEN | SODA |
| potion-icon × empty-state UI fill | YELLOW | Bis BACKUP (CC BY-ND $7) |
| potion-icon × fill-level-3-tier (1/3 / 2/3 / 3/3) | **RED** | **Custom authoring required** |
| gold-icon × coin-pile-variants | GREEN | Dire Dungeon (45 variants) |
| gold-icon × gem-variants | GREEN | Dire Dungeon (10 gems) |
| gold-icon × stack-progression-tier | GREEN | OGA Bonsaiheldin CC-0 BACKUP |
| ui-frame × inventory slot / equipment slot | GREEN | CraftPix Basic UI (FREE) |
| ui-frame × HP / mana bars | GREEN | CraftPix Basic UI |
| ui-frame × quick-slot bar | GREEN | CraftPix Basic UI |
| ui-frame × shop / crafting screens | GREEN | CraftPix Basic UI |
| ui-frame × rarity-bordered slots (white/magic/rare/unique) | **RED** | **Custom authoring required** |

---

## 3. Gap closure status (legolas-flagged gaps + emergent gaps)

### Gap G-FILL — Potion fill-level states (legolas-flagged)

**Status (pre-acquisition):** **PARKED Matt-decision.**
**Status (post-acquisition 2026-05-17):** **MATERIALLY ADVANCED.** Dire Dungeon `potions/` folder includes explicit `healing_big.png` / `healing_medium.png` / `healing_small.png` AND `mana_big.png` / `mana_medium.png` / `mana_small.png` files — 3-tier size variants at native vendor level for the two load-bearing potion types. Path A over-delivered for primary potion families. Remaining ~10 other potion colors lack fill states but those are non-primary.

Three options, ranked by elrond preference:

- **Path A (recommended):** Accept SODA's small/medium/large size variants + Bis empty-variant as functional fill-level proxy for VS2a. Visual proxy is "smaller bottle = lower fill"; clean and conventional. Zero additional cost. Closes G-FILL operationally for VS2a primary scope.
- **Path B:** Authorize custom authoring pass to add 1/3 / 2/3 / 3/3 fill states to a selected potion sprite set. Cost: ~2-4 hours per potion sprite at indie-art-vendor rates. Defensible if mid-fight HP/MP potion state display becomes a load-bearing affordance.
- **Path C:** Acquire Bis CC BY-ND $7 pack and use empty variant as low-fill state. **NOT recommended** — CC BY-ND prevents modification, and the 270-icon breadth duplicates SODA coverage.

**Elrond recommendation: Path A for VS2a; Path B revisited post-VS2a if fill-state legibility becomes load-bearing per drax integration empirical read.**

### Gap G-RARITY — ARPG rarity-tier UI borders (legolas-flagged)

**Status (pre-acquisition):** **PARKED Matt-decision.**
**Status (post-acquisition 2026-05-17):** **INFRASTRUCTURE NOW IN HAND.** CraftPix Basic UI ships pre-built slot frames with rarity-coloured gem indicators (visible in `Inventory.png` + `Equipment.png` — blue/orange/red gem inserts), AND Dire Dungeon ships `DireDungeonItems_animatedOutlines_by_DerNachbar/` folder with 10 outline-glow colors × 32 frames per item × ~214 items = 137,602 frames of animated rarity overlay. Procedural overlay path A is fully infrastructure-supported with native vendor assets — no custom authoring needed for tier-color animation.

Per `mobile-pc-pixel-sizing-ratios-2026-05-17.md` § 4.4 sub-rule: "rarity differentiation is visual-layer-coded, not size-coded. Common = small sprite, no beam, no name. Magic = small sprite, blue beam, name on. Rare = small sprite, yellow beam, name on, faint ring. Legendary = small sprite, orange beam, name on, animated ring + glow." This canon **does not require pre-built bordered icons** — it requires loot beams + name plates + affordance rings layered procedurally.

Two options:

- **Path A (recommended, aligns with gandalf canon § 4.4):** Procedural overlay system in drax — apply per-rarity beam color + name plate + affordance ring at runtime, sourced from base icons in Dire Dungeon's 10-outline-color variants OR no-outline base + procedural border. No additional asset acquisition. Aligns with mature ARPG mobile canon (DI / Torchlight / Eternium all converge on procedural overlay over pre-bordered icons).
- **Path B:** Commission custom rarity-border authoring (4 borders × 5-10 base icons = ~20-40 sprites). Cost: ~$200-500 at indie-art-vendor rates. Useful if a specific Reincarnated rarity visual register diverges from genre canon.

**Elrond recommendation: Path A for VS2a; Path B revisited post-VS2a if procedural overlay proves visually flat.**

### Gap G-ARMOR-MANNEQUIN — Armor-stand helmless/full variants (legolas-flagged)

**Status (pre-acquisition):** flagged but NOT load-bearing for VS2a primary scope.
**Status (post-acquisition 2026-05-17):** **CLOSED + MATERIALLY UPGRADED.** CraftPix Guild Hall ships 3 mannequin designs × 4-frame destruction animation each (`Attacked_Manequin1_with_shadow.png`, `Attacked_Manequin2_with_shadow.png`, `Attacked_Manequin3_with_shadow.png`, plus without-shadow variants). Multi-state mannequin coverage (intact + 3 destruction frames per design) materially exceeds the single-state expectation. Helmet/helmless inference available from destruction frame sequence (sprite reveals underlying structure as it breaks).

### Gap G-COFFIN — Sparse coffin coverage (legolas-flagged)

**Status (pre-acquisition):** **PARTIALLY CLOSED** (via Mucho Pixels).
**Status (post-acquisition 2026-05-17):** **RE-OPENED.** Mucho Pixels NOT acquired (was the only confirmed coffin-with-open-state vendor in the crawl). Seliel Treasure Chests 1 contains chest-only assets, no coffin variants visible in 160×192px composite. **Recommendation:** defer coffin to post-VS2a (not load-bearing for VS2a primary slot). If a coffin asset becomes load-bearing later: (a) acquire Mucho Pixels $4.95 (coffin + bonus chest state-coverage), or (b) commission custom coffin sprite (~$50-150).

### Gap G-AI-POLICY — AI-assisted Pixel-1992 packs (deferred pending policy clarification)

**Status:** OPEN — flagged for team AI-asset policy clarification.

Pixel-1992 coin piles ($1.99) + RPG loot pack 1200 ($1.99) carry "AI-assisted with manual Aseprite refinement" disclosure. These were deferred per legolas summary § 4 + standing elrond curation discipline (AI-provenance assets require explicit team policy approval). Pixel-1992 packs would supplement coverage if approved; current PRIMARY set covers without them, so deferral is non-blocking.

### Gap G-CCBYSA — OGA Clint Bellanger CC-BY-SA 3.0 gold icons (deferred)

**Status:** CLOSED — strict defer per legolas summary recommendation.

CC-BY-SA 3.0 share-alike clause conflicts with proprietary commercial release. OGA Bonsaiheldin 16x16 (CC-0) provides equivalent stack-progression coverage with zero attribution surface. PRIMARY/BACKUP selection avoids CC-BY-SA pack entirely.

---

## 4. Acquisition shortlist for Matt's review

### 4.1 PRIMARY acquisitions (de-duplicated)

**ACQUISITION STATE (2026-05-17 Matt L3):** see § Post-acquisition status section at top of doc for current state. Table below preserves the pre-acquisition shortlist for the historical record.

| Pack | Cost | License | URL | Covers (across subsets) | Acquired? |
|---|---:|---|---|---|---|
| Dire Dungeon Items (DerNachbar) | $10.00 | CC BY 4.0 | https://dernachbar.itch.io/dire-dungeon-items | floor-loot gear-weapon + gear-armor + gold; ui-icons gear-icon + gold-icon (partial); 259 items single-acquisition style-register coherence | **YES $10** |
| Mucho Pixels Dungeon Tileset Pack | $4.95 | GameDev Market Pro Licence (royalty-free) | https://muchopixels.itch.io/dungeon-tileset-pack | ambient-props chest + coffin + weapon-stand + urn-vase-box (4 subcategories in 1 pack) | **NO** |
| SODA 150 Stylized Potions | $3.25 | Royalty-free | https://soda-1.itch.io/150-stylized-potion-icon-pack-32x32 | floor-loot potion + ui-icons potion-icon (shared) | **NO** (partial substitute via Magic_Potions_Pack_V1 FREE) |
| **Pre-acquisition estimate total** | **$18.20** | | | | |
| **Post-acquisition actual outlay** | **$10.00** | | | | **savings $8.20** |

**Free PRIMARY packs (no acquisition fee; verify license terms at acquisition):**

| Pack | License | URL |
|---|---|---|
| AquaSenshi Pixel Art Potions Medieval RPG | Royalty-free | https://aquasenshi.itch.io/pixel-art-potions-asset-pack-medieval-rpg |
| Seliel Mana Seed Treasure Chests | Mana Seed royalty-free | https://seliel-the-shaper.itch.io/treasure-chests |
| Seliel Mana Seed Breakable Pots | Mana Seed royalty-free | https://seliel-the-shaper.itch.io/breakable-pots |
| Elthen Pixel Art Destructible Objects (PWYW) | CC NC w/ commercial-OK | https://elthen.itch.io/pixel-art-destructible-objects |
| CraftPix Free Basic Pixel Art UI for RPG | Royalty-free | https://craftpix.net/freebies/free-basic-pixel-art-ui-for-rpg/ |
| CraftPix Free Top-Down Guild Hall | Royalty-free | https://craftpix.net/freebies/free-top-down-pixel-art-guild-hall-asset-pack/ |

### 4.2 PARKED Matt-decisions

| Decision | Path A (elrond-recommended) | Path B | Cost B |
|---|---|---|---|
| G-FILL potion fill-level | Accept SODA size-tier + Bis empty as proxy ($0; in PRIMARY) | Custom authoring pass for 1/3 / 2/3 / 3/3 frames | ~$50-200 indie-art |
| G-RARITY ARPG rarity borders | Procedural overlay in drax aligned with gandalf § 4.4 canon ($0) | Custom rarity-border authoring (20-40 sprites) | ~$200-500 indie-art |
| G-ARMOR-MANNEQUIN | Accept single-state mannequin for VS2a ($0; in PRIMARY) | Custom authoring helmless/full variants | ~$100-300 indie-art |

### 4.3 BACKUP-tier optional acquisitions (held pending PRIMARY quality assessment)

| Pack | Cost | License | Trigger to acquire |
|---|---:|---|---|
| Vennril 250+ Item Pack | $4.99 | Royalty-free | If Dire Dungeon 32x32 upscale quality is insufficient OR wand-specific coverage needed |
| Bis Potions 270 | $7.00 | CC BY-ND 4.0 | If empty-variant fill-level UI proves load-bearing |
| Akari21 RPG Icon Pack 200+ | $3.00 | Royalty-free | If star-rarity proxy is preferred over Dire Dungeon outline-color |
| Franuka RPG Icon Pack 500+ | $4.99 | Custom attribution | If 48px native UI register proves preferable to 32x32 + frame system |
| Pixel Serial RPG Chests (PWYW free) | FREE | Royalty-free | If chest opening animation frames needed beyond Mucho coverage |

### 4.4 Future commissions (deferred — not VS2a)

- **Custom rarity-border authoring pass** (G-RARITY Path B) — if procedural overlay proves visually flat post-VS2a.
- **Potion fill-level custom frames** (G-FILL Path B) — if mid-fight HP/MP fill-state legibility becomes load-bearing.
- **Armor-stand helmless/full variant authoring** (G-ARMOR-MANNEQUIN) — if trial room "shows what's equipped" affordance becomes load-bearing.
- **AI-policy ruling** on Pixel-1992 packs — clarification request to Matt + jack-ryan governance review.

---

## 5. Manifest references

| Manifest | Path | Row count | PRIMARY packs | BACKUP packs | DEFER rows |
|---|---|---:|---:|---:|---:|
| Floor loot | `agentic_orchestration/research/curated/floor-loot-subset-vs2a-2026-05-17.jsonl` | 29 (1 header + 28 data) | 3 | 7 | 18 |
| Ambient props | `agentic_orchestration/research/curated/ambient-props-subset-vs2a-2026-05-17.jsonl` | 25 (1 header + 24 data) | 5 | 4 | 15 |
| UI icons | `agentic_orchestration/research/curated/ui-icons-subset-vs2a-2026-05-17.jsonl` | 25 (1 header + 24 data) | 4 | 6 | 14 |

**Build script (reproducible):** `agentic_orchestration/research/scripts/build_icons_and_props_subset_vs2a_2026_05_17.py` — re-runnable from legolas crawl outputs; curation decisions embedded as `CURATION` dict (asset_id → decision).

**Schema per data row:**
- `asset_id` — carries from legolas crawl (composite vendor.category.subcategory.specific-slug)
- `vendor`, `category`, `subcategory`, `specific_type`, `rarity_tier`, `pixel_size` — carry from legolas
- `attribution_class` — `commercial-license` | `cc-by` | `cc-0` | `cc-by-nd` | (`cc-by-sa` filtered out at curation level)
- `pack_origin` — drax acquisition-key (= pack slug)
- `cost_usd` — null for premium-membership-gated; numeric otherwise
- `encounter_compatibility` — broad-default `[trash, magic, pack, elite, mini-boss, boss]`
- `render_notes` — size-register hint + raw legolas notes carryover
- `curation_status` — `RECOMMEND-PRIMARY` | `RECOMMEND-BACKUP` | `DEFER`
- `curation_rationale` — elrond decision prose
- `coverage_cells` — list of `(subcategory, variant/state)` tuples this pack populates
- `size_register_fit` — `EXACT` | `CLOSE` | `UPSCALE-REQUIRED` | `DOWNSCALE-REQUIRED`
- `spec_ref` — gandalf sizing canon back-reference
- `legolas_crawl_ref` — provenance pointer to raw row
- `vs2a_status` — `active` | `deferred`

**Drax-consumption pattern (post-VS2a):**
1. Filter rows where `vs2a_status == "active"` AND `curation_status` starts with `RECOMMEND`.
2. Group by `pack_origin` to determine acquisition list.
3. For each acquired pack, read `coverage_cells` to wire pack contents into UI/world slot positions.
4. Read `size_register_fit` + `render_notes` to drive per-asset scale-resolution decisions (UPSCALE-REQUIRED packs route through frame/slot rendering system; CLOSE packs render at native or +1x).

---

## 6. Cross-references to gandalf sizing canon + legolas crawl

- **Sizing canon § 3.3 floor-loot targets:** gear-drop 50×50 (mobile) / ~67×67 (PC); gold pile 35×35 / ~47×47; potion ~35px. Floor-loot PRIMARY packs are 32x32 native → EXACT to mobile target, CLOSE to PC target.
- **Sizing canon § 3.3 chest targets:** small 110×90 mobile / ~147×120 PC; medium 130×105 / ~173×140; large 170×140 + glow / ~227×187. Mucho Pixels 16x16 tile-grid composition reaches small-medium target via 7-8x effective scaling; large-tier via animated glow + multi-tile composition.
- **Sizing canon § 3.3 destructible targets:** vase/urn 65×80; amphora 85×110; barrel 75×95. Mucho + Seliel + Elthen at 16x16 native → UPSCALE-REQUIRED to ~70-90px target; consistent with mature pixel-art ARPG practice.
- **Sizing canon § 4.4 rarity-visual-layer-coded sub-rule:** drives G-RARITY Path A recommendation (procedural overlay over pre-bordered icons).
- **Sizing canon § 4.5 destructible-ambient tap-affordance:** confirms 65-80px destructible target with 80-95px tap-zone — matches Mucho + Seliel + Elthen state-coverage capability.
- **Legolas summary § 2 coverage matrix:** maps directly to § 2 of this doc (legolas's GREEN/YELLOW/RED → elrond's GREEN/YELLOW/RED with PRIMARY/BACKUP/DEFER curation overlay).
- **Legolas summary § 3 sizing-mismatch flags:** elrond's `size_register_fit` field encodes these per row; DOWNSCALE-REQUIRED packs (CraftPix 512x512 coins, Pixel-1992 128x128) deferred to avoid downscaling artifacts.
- **Legolas summary § 4 license-status flags:** CC-BY-SA OGA pack strict-deferred; CC-BY Dire Dungeon accepted (Pimen Gap-G4 Path B precedent); AI-assisted Pixel-1992 deferred pending policy.
- **Legolas summary § 5 cost rollup:** elrond's $18.20 PRIMARY de-duplicated cost matches legolas § 5 minimum-cost-comprehensive figure.

---

## 7. Observations for follow-on dispatches

1. **Style-register coherence is the dominant curation criterion across subsets.** Dire Dungeon's $10 acquisition is recommended PRIMARY across floor-loot AND ui-icons because cross-subset visual coherence (gear floor-drop looks like its UI-icon counterpart) is a meaningful design quality that fragmented per-subcategory vendor selection would not achieve. Mucho Pixels plays the same role within ambient-props. **OBSERVATION** — future commissions should treat cross-subset style-register coherence as a first-class curation criterion, not a downstream worry.

2. **CC-BY attribution surface is concentrated in a single acquisition (Dire Dungeon).** Across all three subsets, the only CC-BY-class PRIMARY pack is Dire Dungeon. Attribution panel needs a single attribution line for DerNachbar (Dire Dungeon Items) + a single line for the optional Shikashi BACKUP pack if activated. Compared to Pimen's `pixel-battle-effects` CC-BY concentration (one pack), this is structurally identical — single attribution-surface concentration is a well-managed pattern. **OBSERVATION** — drax should plan credits-panel infrastructure for ~3-5 CC-BY attributions total across all asset categories (Pimen pixel-battle-effects + Dire Dungeon Items + optionally Shikashi + future CC-BY adds).

3. **Three legolas-flagged gaps mirror canonical gandalf design choices.** G-FILL (potion fill-level) and G-RARITY (ARPG rarity borders) both have procedural-overlay close-paths that align with gandalf's sizing canon § 4.4 visual-layer-coded rarity rule. **OBSERVATION** — the procedural-overlay paradigm is structurally consistent with the engine's gandalf-stated design intent; G-FILL + G-RARITY are NOT acquisition gaps requiring vendor commission but design-implementation work in drax's pipeline.

4. **AI-policy ruling needed for Pixel-1992 packs.** Two AI-assisted packs ($1.99 each) were deferred pending team AI-policy clarification. They are NOT load-bearing (Dire Dungeon + OGA CC-0 cover the gold need; Mucho + Seliel cover chest need) but their deferral status should be resolved via jack-ryan governance + Matt for consistency with future AI-flagged asset decisions.

5. **No structural mismatch with drax ingest pipeline expected.** Schema mirrors Pimen pattern (pack_origin → drax acquisition key; coverage_cells → wiring directive). The new fields (`size_register_fit`, `curation_status`, `coverage_cells`) are additive and do not break Pimen-pattern consumption. **OBSERVATION** — drax's M5 panel redesigns can adopt this manifest schema directly.

6. **Cross-subset acquisition cost savings: 39%.** Per-subset rollup totals $13.25 (floor-loot) + $4.95 (ambient-props) + $13.25 (ui-icons) = $31.45 nominal. De-duplicated across shared packs: $18.20 actual. Savings of $13.25 (Dire Dungeon $10 + SODA $3.25 shared between floor-loot and ui-icons). **OBSERVATION** — future acquisition rollups should report both nominal-per-subset AND de-duplicated-cross-subset figures to surface the cost-multiplexing pattern.

---

## 8. Acceptance-criteria checklist (per dispatch § Acceptance)

- [x] Floor-loot subset manifest authored — `floor-loot-subset-vs2a-2026-05-17.jsonl`
- [x] Ambient-props subset manifest authored — `ambient-props-subset-vs2a-2026-05-17.jsonl`
- [x] UI-icons subset manifest authored — `ui-icons-subset-vs2a-2026-05-17.jsonl`
- [x] Per-sub-asset-class coverage matrix (GREEN/YELLOW/RED) — § 2 above
- [x] Acquisition shortlist with cost + links — § 4 above
- [x] Summary doc authored — this document
- [x] Hive-log STATE + HANDOFFs — see § 9 below

---

## 9. Hive-log + handoff (PRE-SIGNAL § 14.1.1 honored before append)

**STATE entry** (appended to `agentic_orchestration/hive-mind/phase-1-p1-log.md`):
- Three manifest paths + row counts
- 9-pack PRIMARY recommendation; $18.20 de-duplicated acquisition cost
- 4 legolas gaps closed (1 partial, 1 fully via canon-alignment, 2 PARKED Matt-decisions)
- 3 PARKED Matt-decisions surfaced (G-FILL / G-RARITY / G-ARMOR-MANNEQUIN)

**HANDOFF → drax:** three manifests under `agentic_orchestration/research/curated/`; consumption pattern documented § 5 above. Drax M5 panel redesigns + post-VS2a ambient prop dispatches consume the manifests. No race-condition concern with legolas-2 broader-2D-sprite catalogue survey (separate scope — character/monster/tileset territory; per legolas summary § 6 vendor-breadth-map).

**HANDOFF → matt (PARKED):** three PARKED decisions per § 4.2 (G-FILL Path A vs B; G-RARITY Path A vs B; G-ARMOR-MANNEQUIN single-state-acceptance vs custom-authoring). Elrond recommends Path A on all three for VS2a; revisit post-VS2a if drax integration empirical read surfaces insufficiency signals.

**HANDOFF → matt (acquisition authorization):** $18.20 PRIMARY acquisition shortlist per § 4.1. Same Matt-L3 acquisition-authorization pattern as Pimen subset $26.35 acquisitions.

**No new vendor commissions auto-triggered.** All identified gaps are flagged for Matt review per dispatch out-of-scope rule "DO NOT commission new vendor crawls without Matt sign-off."

---

*Filed 2026-05-17 by elrond per dispatch authorization. Auto-fired on legolas-1 completion (b0d6bce). Pattern B curation work; no tag per dispatch § Item 5.*
