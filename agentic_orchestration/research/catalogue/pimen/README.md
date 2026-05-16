# Pimen Catalogue — Research Files

**Source:** https://pimen.itch.io (single creator, commercial pixel-art VFX + character assets)
**Catalogued by:** legolas (Mode B)
**Viability gate:** PASSED (all three tracks) — 2026-05-16

## Files in this directory

| File | Description | Rows |
|---|---|---|
| `sample-2026-05-16.json` | Historical sample (20 rows, Mode B sample pass) | 20 |
| `full-2026-05-16.jsonl` | **Authoritative full crawl** (all 46 rows; sample packs re-crawled for freshness) | 46 |

**Disposition:** `sample-2026-05-16.json` is retained as the historical Mode B sample record. `full-2026-05-16.jsonl` supersedes it for curation purposes — all 20 sample packs were re-crawled and their rows are included in the full file with updated data. Do not use the sample file for downstream curation; use the full file.

## Crawl statistics — full-2026-05-16.jsonl

| Metric | Value |
|---|---|
| Total rows | 46 |
| Free (cost = 0) | 19 |
| Paid (cost > 0) | 27 |
| VFX category | 44 |
| Enemy category | 1 |
| Character category | 1 |
| hd2d-pixel resolution band | 21 |
| retro resolution band | 4 |
| tiny resolution band | 1 |
| unknown resolution band | 20 |
| Aseprite source included | 13 |
| CC-BY licensed | 2 |
| commercial-royalty-free licensed | 44 |

## Element coverage

| Element | Pack count |
|---|---|
| fire | 3 (01/02/03) |
| water | 3 (01/02/03) |
| earth | 3 (01/02/03) |
| wind | 3 (01/02/03) |
| thunder | 3 (01/02/03) |
| ice | 2 (01/02) |
| dark | 1 (03-tier only) |
| holy | 1 (03-tier only) |
| acid | 1 (03-tier only) |
| wood | 1 (03-tier only) |
| multi (bundles) | 2 (Mega Pack 01 + 02) |
| non-element | 23 (buff/debuff, battle, smoke, character, misc) |

## Notable findings for downstream agents

1. **CC-BY exception (2 packs):** `pixel-battle-effects` and `cutting-and-healing` require attribution. All other Pimen packs are commercial-royalty-free with no attribution required.
2. **Buff/Debuff Pack 09 register outlier:** 24x24 canvas vs 48-64px for packs 01-08. Likely retro register — verify at curation.
3. **Battle VFX Projectile at 12x12:** Tiny resolution band — retro register; unlikely to composite with hd2d-pixel assets.
4. **13 packs include Aseprite source files:** Enables layer-separated wiring. Note: Buff/Debuff Pack 01 does NOT include Aseprite (packs 02-09 do). Explosion Effect uses older `.ase` format.
5. **Earth Spell Effect 03 includes an enemy character:** Earth Elemental (6 animation cycles) bundled with spell VFX — cross-category content, tagged `includes-enemy-character`.
6. **Frame count data discrepancy for Earth Elemental:** Values differ between sample crawl and re-crawl — possible pack update. Re-crawl values used in full file.
7. **Mega Pack 01 Aseprite discrepancy:** Sample noted Aseprite files included; re-crawl finds no Aseprite confirmation. Verify at acquisition.
8. **Many non-square canvases:** Dark Spell (8/12 effects), Smoke N Dust 02 (6/14 effects), Wood Spell (3/12 effects), others. Drax canvas-padding concern documented per-row.
9. **20 rows with unknown resolution_band:** Mostly free/early packs where canvas sizes are not stated on product pages. Visual inspection required at curation.
