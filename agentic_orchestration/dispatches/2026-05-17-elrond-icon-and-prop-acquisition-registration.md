# 2026-05-17 — elrond — Icon + interactable-prop acquisition registration (post-Matt-acquire)

**Authority:** Matt L3 2026-05-17 (~00:30 EDT). Matt acquired 7 asset packs covering most of your icon + prop PRIMARY shortlist. Register these acquisitions, refresh the manifests, and document final gap status.
**Type:** Pattern A — ~30-60 min micro-task; manifest update + gap-status refresh; no curation re-run.
**Predecessor:** Elrond icon + interactable-prop curation (`agentic_orchestration/dispatches/2026-05-17-elrond-icon-and-prop-curation-queued.md` — shipped earlier tonight).

---

## What Matt acquired (all in `reincarnated-demo/public/assets/`)

1. **`DireDungeon_Items_Loot/`** — DerNachbar Dire Dungeon Items + Loot ($10 CC-BY-4.0). 259 items; comprehensive floor loot + UI icons. Was your #1 PRIMARY.
2. **`Magic_Potions_Pack_V1/`** — magic potion sprites (verify contents; likely SODA-equivalent). Contains `Individual_Icons/` + `Spritesheet.png`.
3. **`craftpix-net-189780-free-top-down-pixel-art-guild-hall-asset-pack/`** — guild hall (armor mannequin + weapon rack source). **Closes G-ARMOR-MANNEQUIN**.
4. **`craftpix-net-255216-free-basic-pixel-art-ui-for-rpg/`** — slot-frame UI infrastructure. Supports G-RARITY procedural overlay path.
5. **`craftpix-net-809047-free-animated-magic-book-pixel-art-asset-pack/`** — animated magic book (decoration / lore asset; not in your prior spec but useful).
6. **`19.07c - Treasure Chests 1/`** — Seliel the Shaper Mana Seed treasure chests (free, commercial OK). 5 chest types + open/closed + 3 color swaps. Was your #3 PRIMARY.
7. **`20.05b - Breakable Pots 1/`** — Seliel breakable pots with 3-frame break animation (free). Was on your free-tier PRIMARY list.

**One PRIMARY not acquired:** Mucho Pixels Dungeon Tileset Pack ($4.95) — was your bundled chest + coffin + weapon-stand + pots source. The Seliel + DireDungeon combo covers MOST of what Mucho Pixels would have provided.

---

## Required reading

1. `agentic_orchestration/research/curated/icons-and-props-subset-vs2a-selection-2026-05-17.md` — your prior selection doc; the source of truth for what gaps existed
2. `agentic_orchestration/research/curated/floor-loot-subset-vs2a-2026-05-17.jsonl` — floor-loot manifest
3. `agentic_orchestration/research/curated/ambient-props-subset-vs2a-2026-05-17.jsonl` — ambient-props manifest
4. `agentic_orchestration/research/curated/ui-icons-subset-vs2a-2026-05-17.jsonl` — UI-icons manifest
5. The 7 acquired pack directories (above) — verify contents match expected coverage

---

## Scope

### Item 1 — Per-pack content verification

For each of the 7 acquired packs, inspect contents (ls + image-spritesheet inspection at a high level). Verify:

- **DireDungeon_Items_Loot:** confirm 259 items present; check items_outlines for rarity-tier variant glyphs
- **Magic_Potions_Pack_V1:** check Individual_Icons/ count; confirm fill-level variants present OR document G-FILL still open
- **CraftPix Guild Hall:** confirm armor mannequin + weapon rack sprites in PNG/ subdir; close G-ARMOR-MANNEQUIN
- **CraftPix Basic Pixel Art UI for RPG:** confirm slot-frame infrastructure assets; supports G-RARITY procedural overlay path
- **CraftPix Animated Magic Book:** new asset; document for bonus UI/lore coverage
- **Treasure Chests 1 (Seliel):** verify chest types + open/closed states; check if any "coffin-style" chests exist (could close G-COFFIN partially)
- **Breakable Pots 1 (Seliel):** confirm 4 color variants + break animation frames

### Item 2 — Update manifests with `acquired_path` field

For each manifest row corresponding to an acquired pack, add an `acquired_path` field pointing to the relative path under `reincarnated-demo/public/assets/`. Example:

```json
{
  "asset_id": "dire-dungeon.floor-loot.weapon-sword.001",
  "vendor": "DerNachbar",
  "pack_origin": "Dire Dungeon Items + Loot",
  "cost_usd": 10,
  "attribution_class": "cc-by-4.0",
  "curation_status": "PRIMARY",
  "acquired_path": "DireDungeon_Items_Loot/DireDungeonItemsTileset_by_DerNachbar (v1.0).png",
  "render_notes": "..."
}
```

This makes the manifests drax-consumable for the eventual post-VS2a M5 panel redesigns + ambient prop dispatches.

### Item 3 — Refresh gap status

Update the selection doc with closure status per gap:

| Gap | Prior status | Post-acquisition status |
|---|---|---|
| **G-FILL** (potion fill-level) | PARKED Path-A recommended | ??? (depends on Magic_Potions_Pack_V1 content) |
| **G-RARITY** (rarity-tier UI borders) | PARKED Path-A recommended | Supported via CraftPix Basic UI slot-frame infrastructure + procedural overlay in drax (Path A still); document infrastructure now available |
| **G-ARMOR-MANNEQUIN** (helmet/helmless variants) | Flagged not-load-bearing | **CLOSED** via CraftPix Guild Hall |
| **G-COFFIN** (open-state coffin) | PARTIAL via Mucho Pixels (not acquired) | ??? (depends on Treasure Chests 1 content; may need to flag as still OPEN if no coffin-style chest in pack) |

### Item 4 — Surface remaining gaps

If any gaps remain open after this registration, surface them with explicit recommendations:
- Coffin coverage: if G-COFFIN remains OPEN, recommend either (a) acquire Mucho Pixels Dungeon Tileset Pack ($4.95) for the bundled coffin, or (b) defer coffins to post-VS2a (not load-bearing for VS2a)
- Fill-level: if Magic_Potions_Pack_V1 doesn't have fill states, recommend Path A (size-tier proxy) per your prior dispatch

### Item 5 — Acquisition cost rollup update

Original PRIMARY $18.20 included DireDungeon ($10) + Mucho Pixels ($4.95) + SODA ($3.25).
Actual Matt-acquired cost: DireDungeon ($10) + 6 free packs = **$10 actual**.

Update the summary doc cost rollup to reflect actual outlay vs prior estimate.

### Item 6 — Hive log + tag

- PRE-SIGNAL § 14.1.1 before hive-log append (rocket D10 in flight; legolas DoE crawl in flight)
- STATE entry: 7 packs registered; gap closure deltas documented; cost rollup updated
- HANDOFF → drax: manifests now have `acquired_path` for drax to consume directly in post-VS2a M5 panel redesigns
- No tag (curation update; not code; standard authoring discipline)

---

## Out of scope (DO NOT)

- ❌ DO NOT re-run the full curation pipeline; this is a registration micro-task
- ❌ DO NOT extend to new vendor crawls
- ❌ DO NOT make Path-B recommendations on G-FILL / G-RARITY unless new evidence emerges from pack inspection
- ❌ DO NOT modify drax-side ingest pipeline (drax will consume `acquired_path` when ready)
- ❌ DO NOT touch the legolas-2 broader catalogue survey output
- ❌ DO NOT extend to character/monster/VFX assets

---

## Acceptance criteria

- [ ] 7 packs verified for content
- [ ] Manifests updated with `acquired_path` field where applicable
- [ ] Gap closure status refreshed (G-FILL / G-RARITY / G-ARMOR-MANNEQUIN / G-COFFIN)
- [ ] Selection doc updated with post-acquisition status
- [ ] Cost rollup updated ($10 actual vs $18.20 estimate)
- [ ] Remaining gaps surfaced (if any)
- [ ] Hive-log STATE entry
- [ ] HANDOFF → drax (manifests acquire-path-ready)

---

## Coordination

- **PRE-SIGNAL § 14.1.1** — rocket D10 implementation + legolas DoE crawl in flight; multiple agents may write hive log
- **No new tags** — curation update only
- **Drax (downstream consumer):** your output ready for drax's post-VS2a M5 panel redesigns + ambient prop dispatches

---

*Dispatched 2026-05-17 by knight-rider per Matt L3 post-acquisition. ~30-60 min. Append completion record when done.*

---

## Completion record — elrond — 2026-05-17

**Status:** COMPLETE.
**PRE-SIGNAL § 14.1.1:** honored before hive-log append (`git fetch origin`; last commit `5b849dd` rocket D10; no concurrent hive-log writers).
**Tag:** none (curation/registration update; manifest re-emission only).

### Acceptance criteria — all met

- [x] **7 packs verified for content** — § Item 1 below.
- [x] **Manifests updated with `acquired_path` field** — schema v1.0 → v1.1; rows now carry `acquisition_status` + `acquired_path*` keys + `acquired_date` + `acquired_cost_usd` + `acquisition_notes`.
- [x] **Gap closure status refreshed** — table below; both at top of selection doc AND in per-gap sections.
- [x] **Selection doc updated with post-acquisition status** — new "Post-acquisition status" section at top of `icons-and-props-subset-vs2a-selection-2026-05-17.md`.
- [x] **Cost rollup updated ($10 actual vs $18.20 estimate)** — both in selection doc + manifest headers.
- [x] **Remaining gaps surfaced** — § Remaining surfacings below.
- [x] **Hive-log STATE entry** — appended at `phase-1-p1-log.md` tail.
- [x] **HANDOFF → drax** — manifests acquire-path-ready; documented in hive entry.

### Item 1 — per-pack content verification

| Pack | Content findings |
|---|---|
| `DireDungeon_Items_Loot/` | 214 base items + 137,602 animated outline frames (10 glow colors × 32 frames × 2 modes per item across 6 weapon types + 3 armor types + jewelry + shields + gems + potions + scrolls/tomes + orbs/trinkets). **Critical finding:** potions folder ships explicit `healing_big/medium/small.png` + `mana_big/medium/small.png` — 3-tier fill/size variants at native vendor level. items_outlines/ folder gives single-color outlined (black) variants suitable for UI display. |
| `Magic_Potions_Pack_V1/` | 25 individual potions (5 colors × 5 shapes: classic/heart/round/skull/square); 1 spritesheet + 25 Individual_Icons + PSD + ASEPRITE + Tiled_files folders. **License.txt is 35 bytes** — vendor identity unclear; license needs legolas-3 verification. Functional substitute for SODA + AquaSenshi but loses explicit type-labels (health/mana/poison/energy/speed). |
| `craftpix-net-189780-...-guild-hall-asset-pack/` | 3 mannequin designs × 4-frame destruction animation (`Attacked_Manequin1/2/3_with_shadow.png` + without-shadow variants); plus weapon racks, banner stands, bookshelves, banner displays in `Interior_objects.png`; plus guild NPCs (citizens, fighters, mages). **Critical finding:** mannequins are multi-state (destruction animation), not single-state — materially upgrades G-ARMOR-MANNEQUIN expectation. |
| `craftpix-net-255216-...-basic-pixel-art-ui-for-rpg/` | Inventory + Equipment + Shop + Craft + Settings + Win_loose + Buttons + Action_panel + Circle_menu + Main_menu screens. **Inventory + Equipment screens contain rarity-coloured gem slot indicators** (blue/orange/red visible) — supports G-RARITY procedural overlay path. Equipment.png shows paper-doll character with helm + sword + shield (armor-stand-equivalent UI panel). |
| `craftpix-net-809047-...-animated-magic-book-...` | **BONUS pack (not in shortlist).** 12-frame book open/close animation across cover→opened states; Icons.png contains per-element skill icon sets (fire/nature/water/lightning) at 8 frames per icon × rarity tiers; pages_appear/disappear sheets; bookmark variants. Logged in `BONUS_ACQUISITIONS` in build script for downstream visibility. |
| `19.07c - Treasure Chests 1/` | Single 160×192px spritesheet — 5 chest designs × ~12 rows (open/closed × 3 color swaps, ~15 variants total). **No coffin-style variant** — G-COFFIN remains OPEN. 16-bit Mana Seed style register. |
| `20.05b - Breakable Pots 1/` | Composite breakable pots.png (128×128) + 4 explicit color variant sheets (gray/red/white/yellow) — **4 colors not 3 as legolas crawled** (minor uplift). 3-frame breaking animation + 6 shard particles per pot design. Mana Seed style. |
| `Destructible Objects Sprite Sheet.png` (bare) | Elthen Destructible Objects acquired as bare PNG at assets root (no folder). Contains barrels, crates, rocks/stones, signs, sign-posts × 3-state intact + 4-frame destruction frames + shard particles per object. |

### Item 2 — manifest updates

Build script `agentic_orchestration/research/scripts/build_icons_and_props_subset_vs2a_2026_05_17.py` extended with `ACQUISITIONS` dict (asset_id → acquired metadata) + `BONUS_ACQUISITIONS` list (out-of-shortlist packs).

Schema bumped v1.0 → v1.1 on all three manifests:
- Per-row additions: `acquisition_status` (`ACQUIRED` | `NOT-ACQUIRED`), `acquired_path`, `acquired_path_*` (per-asset-category sub-keys), `acquired_date`, `acquired_cost_usd`, `acquisition_notes`.
- Header additions: `_acquisition_cost_usd_actual_this_subset`, `_acquired_pack_origins`, `_primary_packs_not_acquired`. Pre-existing `_acquisition_cost_usd_primary_only` renamed `_acquisition_cost_usd_primary_only_estimate` for clarity.
- Header now references this dispatch as `_dispatch_ref` with prior dispatch in `_predecessor_dispatch_ref`.

Rows touched (14 ACQUIRED rows across 3 manifests):

| Manifest | ACQUIRED count | NOT-ACQUIRED count |
|---|---:|---:|
| `floor-loot-subset-vs2a-2026-05-17.jsonl` | 4 | 25 |
| `ambient-props-subset-vs2a-2026-05-17.jsonl` | 5 | 20 |
| `ui-icons-subset-vs2a-2026-05-17.jsonl` | 5 | 20 |
| **Total** | **14** | **65** |

### Item 3 — gap closure status refresh

| Gap | Pre-acquisition | Post-acquisition | Driver |
|---|---|---|---|
| **G-FILL** (potion fill-level) | PARKED Path A | **MATERIALLY ADVANCED** | DireDungeon `potions/` folder ships `healing_big/medium/small.png` + `mana_big/medium/small.png` natively |
| **G-RARITY** (UI borders) | PARKED Path A | **INFRASTRUCTURE IN HAND** | CraftPix Basic UI Inventory/Equipment slot frames with rarity-coloured gem indicators + DireDungeon `animatedOutlines/` 10-color glow folder (137,602 frames) |
| **G-ARMOR-MANNEQUIN** (armor stand) | flagged not load-bearing | **CLOSED + UPGRADED** | Guild Hall 3 mannequin designs × 4-frame destruction animation; multi-state coverage exceeds single-state expectation |
| **G-COFFIN** (open coffin) | PARTIALLY CLOSED | **RE-OPENED** | Mucho Pixels not acquired (was sole coverer); Seliel chests pack has no coffin variants |
| G-AI-POLICY (Pixel-1992) | OPEN governance | UNCHANGED | governance question separate |
| G-CCBYSA (OGA share-alike) | strict-defer | UNCHANGED | already closed |

### Item 4 — remaining surfacings

1. **G-COFFIN re-opened.** Recommendation: defer to post-VS2a (not load-bearing for primary slot). If coffin becomes load-bearing later: acquire Mucho Pixels $4.95 (bundles coffin + bonus chest state-coverage) OR commission custom coffin sprite (~$50-150). Mucho Pixels would also recover chest-multi-state-coverage detail (locked/unlocked/opened in gold + silver tiers; 7-weapons-on-stand variant; 4-pot-types-broken).
2. **Magic_Potions_Pack_V1 provenance verification.** Vendor metadata unclear (license.txt 35 bytes). Flag for legolas-3 verification at next crawl. Until then, manifest stamps `vendor TBD`, treats as commercial-license assumption, does not publish attribution claim.
3. **Bonus Animated Magic Book pack** (outside shortlist; acquired). Logged in `BONUS_ACQUISITIONS` build-script list. Useful as UI decoration / skill-icon backup (per-element 8-frame icon sets fire/nature/water/lightning).

### Item 5 — cost rollup update

| Line | Pre-acquisition estimate | Post-acquisition actual |
|---|---:|---:|
| Dire Dungeon Items (CC BY 4.0) | $10.00 | $10.00 |
| Mucho Pixels Dungeon Tileset Pack | $4.95 | $0.00 (not acquired) |
| SODA 150 Stylized Potions | $3.25 | $0.00 (substituted free) |
| 6 free PRIMARY packs (AquaSenshi/Seliel×2/Elthen/CraftPix×2) | $0.00 | $0.00 |
| **De-duplicated PRIMARY total** | **$18.20** | **$10.00** |
| Bonus pack (Magic Book) | $0.00 | $0.00 |
| **Savings vs estimate** | — | **$8.20 (-45.1%)** |

### Item 6 — hive log + tag

- ✅ PRE-SIGNAL § 14.1.1 honored before hive-log append.
- ✅ STATE entry appended to `agentic_orchestration/hive-mind/phase-1-p1-log.md` tail (~line 6489+).
- ✅ HANDOFF → drax: manifests now have `acquired_path` for drax to consume directly in post-VS2a M5 panel redesigns + ambient prop dispatches. No drax-side ingest pipeline modification required.
- ✅ HANDOFF → legolas: Magic_Potions_Pack_V1 vendor/license verification queued (low-priority).
- ✅ HANDOFF → knight-rider: registration micro-task complete; no further routing required.
- ✅ No new tag (curation update; standard authoring discipline per dispatch § Item 6).

### Files touched

- `agentic_orchestration/research/curated/floor-loot-subset-vs2a-2026-05-17.jsonl` — regenerated (schema v1.1)
- `agentic_orchestration/research/curated/ambient-props-subset-vs2a-2026-05-17.jsonl` — regenerated (schema v1.1)
- `agentic_orchestration/research/curated/ui-icons-subset-vs2a-2026-05-17.jsonl` — regenerated (schema v1.1)
- `agentic_orchestration/research/curated/icons-and-props-subset-vs2a-selection-2026-05-17.md` — added Post-acquisition section + per-gap annotations + § 4.1 Acquired? column
- `agentic_orchestration/research/scripts/build_icons_and_props_subset_vs2a_2026_05_17.py` — added `ACQUISITIONS` dict + `BONUS_ACQUISITIONS` list + acquisition-status emission in `curate_row` + actual-cost rollup in `build_subset` + summary print
- `agentic_orchestration/hive-mind/phase-1-p1-log.md` — STATE entry appended
- This dispatch file — completion record appended

*Completed 2026-05-17 by elrond. ~45 min Pattern A micro-task.*
