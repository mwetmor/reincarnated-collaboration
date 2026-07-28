# G-6 evidence set — index

Curated crops cited by `galadriel/notes/2026-07-28-gd-playtest-v1-g6-skill-screenshots.md`.
Filenames encode `f<frame-id>_<x0>-<y0>-<x1>-<y1>_<tag>_x<upscale>` in **native 1920×1080 screen
coordinates**, so every crop is reproducible from the source still. Source stills:
`/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/screenshots/Screenshot (N).png`.

Evidence images are downscaled to ≤1000 px on the long side for repo weight — still well above the
~0.75×-native floor at which this UI's rank counters read. The full-resolution working set
(thumbs / sheets / crops / composites / grid / node-series / tooltips) is gitignored and
regenerable via `pipeline/gd-playtest-v1/g6_*.py`.

| File | Shows | Supports |
|---|---|---|
| `f351_580-520-900-600_blightpct_x6.png` | **"Current Level : 1 — 100% Piercing Damage converted to Chaos Damage"** | **F-G6-1** (the contradiction) |
| `f351_690-370-960-500_tip351b_x5.png` | tooltip title **"Blight of Ch'thon"** + flavour | F-G6-1 |
| `f351_690-490-960-640_tip351c_x5.png` | same tooltip's Current Level line beside the 16/16 node | F-G6-1 |
| `SERIES_blight.png` | Blight node: locked → **1/1** between `play_time` 2918 and 3619 | F-G6-1 (dating) |
| `f210_320-310-660-450_wt_x5.png` | **Feral Claws** block @ transform rank 16 — 5 lines, no bleed/leech/crit | **F-G6-2** (`werewolf2` absent) |
| `f210_320-440-660-575_wt_x5.png` | **Rip and Tear** block, part 1 (42 energy, 4 s recharge, 2.5 m area, 14 m range) | F-G6-3, §5.1 |
| `f210_320-570-660-705_wt_x5.png` | Rip and Tear part 2 (375 pierce, 810 bleed / 3 s, 0.5 s knockdown, +200% move) | F-G6-3, §5.1 |
| `f210_320-190-660-325_wt_x5.png` | transform tooltip head: **"…cannot trigger weapon pool skills."** + `Current Level : 16` | **F-G6-4** |
| `SERIES_rednode.png` | transform rank series 1→3→5→12→15→16, dated | §3.1, F-G6-5 |
| `SERIES_bluenode.png` | Onslaught rank series 1×6 → 4 → 7 → 10 → **13** | §3.1, F-G6-4 |
| `f348_450-250-730-380_t348_x5.png` | Onslaught tooltip @ end of run: 5 stacks, 158% MH, 143 cold, **Next Level : 14** | Onslaught = 13/16 |
| `f314_300-240-580-380_tC_x5.png` | Onslaught tooltip @ lvl 11: **Next Level : 11** (⇒ rank 10) | series cross-check |
| `f352_640-340-1000-740_tooltip_x3.png` | **Battle Surge** — 100% activate, 6 s recharge, 3 s, **8% health/sec** | **F-G6-6** (sustain) |
| `f316_620-240-950-380_pactB_x5.png` | reserved cold aura — 50 energy, 12 m radius, +20 DA, **+16 Armor** | F-G6-6 |
| `f349_665-420-945-800_cluster_x3.png` | the whole counter-bearing node cluster + connector topology | §3 rank table |
| `f349_680-440-900-570_gapA_x5.png` | Onslaught **13/16**, square **1/12**, circle **0/1** | §3 |
| `f349cluster_660-430_x6.png` | same three at 6× | §3 |
| `f349cluster_660-554_x6.png` | **16/16** transform + **1/1** Blight, connector visible | §3 |
| `f351_655-275-945-460_toprow_x4.png` | top pair **0/12**, **0/10** unallocated at end of run | §3 |
| `f210_670-600-810-680_rednode_x8.png` | transform counter **16 / 16** (hovered, bold) | §3.1 |
| `f68_670-600-810-680_rednode_x8.png` | same node **1 / 16** at `play_time` 960 | §3.1 |
| `SERIES_sq12.png` | square node: locked → **1/12** in the same mid-R2 window | F-G6-6 |
| `SERIES_battlesurge.png` | circle node: locked → **1/12**, same window | F-G6-6 |
| `SERIES_sq12hover.png` / `SERIES_circ12hover.png` | the hover-bold cue — **the UNCERTAIN pairing**, saved for human eyes | §3, §8(a) |
| `endrun2-composite_native.png` | tooltip-free two-pass robust composite of the end-run panel | §2 method |
| `f347_630-220-1020-620_charwin_x3.png` | end-of-run paperdoll, all slots filled | §7.1 |

### Gear — the four attested items, read off the tooltips

| File | Shows | Supports |
|---|---|---|
| `f323_230-195-640-330_weapon_x5.png` | **"Poisoned Pusquill's Tail of Corrosion" — Rare One-Handed Mace**, 14–40 Physical, 6–12 Acid, **1.78 Attacks/sec** | §7.1 (name verified vs testimony + G-7) |
| `f323_230-320-640-470_weapon2_x5.png` | **50 Poison Damage over 5 Seconds** · +38% Poison with +64% Duration · **18% Physical→Acid** · **+242 Health** | **F-G6-9**, **F-G6-10** |
| `f328_540-190-980-340_amuletR_x5.png` | **"Menacing Putrid Necklace of Protection"** (full title) | §7.1 |
| `f328_230-190-660-340_amulet_x5.png` | Rare Amulet · +21% Poison Damage · +14 Cunning · **+321 Health** | F-G6-9 |
| `f324_230-355-660-500_armor2_x4.png` | **"Mystic Salvaged Armor of Menhir's Wall"** · **58 Armor** · **+76 Health** · +13 Defensive Ability | F-G6-9 |
| `f299_410-555-850-720_belt4_x4.png` | **"Mystic Woven Cord of Soulwarding"** · 7 Armor · **+98 Health** | F-G6-9 |

Health decomposition: 242 + 321 + 98 + 76 = **+737** against the T-A measured step
**759 → 1600 = +841** — **87.6% itemised.**

**Not present, and that is a finding too:** no devotion-window frame exists in the 313; the
Devotion tab is visible in every skill-window frame and never selected.
