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
