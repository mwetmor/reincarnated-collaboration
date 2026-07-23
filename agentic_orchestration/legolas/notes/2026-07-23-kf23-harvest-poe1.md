# KF-2/3 Harvest — Path of Exile 1 (poe1-cyclone)
**Legolas Mode B** | 2026-07-23 | Kit: `poe1-cyclone` (Cyclone Slayer)
**Charter ref:** KFL-3 — starter set = white-tier early maps (zone level 68), iconic well-documented mobs.

---

## KIT SIDE (KF-2 input)

### VERSION PIN — CRITICAL FOR JOIN-KEY

The corpus citation for `poe1-cyclone` is `[3.15] Cyclone Build (League Starter) | Berserker | Expedition | Path of Exile 3.15` (pathofexile.com/forum/view-thread/3078559, accessed 2026-07-23).

**Confirmed verbatim from that forum thread:** "deals 59% of Base Damage, and has 59% Effectiveness of Added Damage at gem level 20"

**poedb.tw (current, 2026-07-23):** Shows level 20 Cyclone at 150% of base / 150% effectiveness of added damage.

**Search-confirmed history:** Cyclone was buffed in patch 3.27 (October 2025) from 44-59% → 61-111% scaling; poedb.tw current may reflect a further change or display at different gem quality.

**ELROND PIN REQUIRED:** The join-key for poe1-cyclone must be pinned to a specific version. The corpus-cited build is 3.15 (59%). The current DB (poedb.tw) reflects a substantially different value. Recommend elrond pins to 3.15 era (59%) per the corpus citation; if the documented build point is to be updated, the kit_citation must be amended first. This is a version-pinning gap that threatens KF-2 join-key accuracy.

**Both values are filed below; source and version labeled for each.**

### Cyclone Skill Gem — Level Progression Table

#### VERSION A: 3.15 era (corpus-cited build point)
**Source:** pathofexile.com/forum/view-thread/3078559 (accessed 2026-07-23)
Verbatim: "deals 59% of Base Damage, and has 59% Effectiveness of Added Damage at gem level 20"
Verbatim: Gem link: "Cyclone - Impale - Infused Channelling - Brutality - Melee Physical Damage - Rage"

Only gem level 20 value confirmed verbatim. Full per-level table for 3.15 era not directly fetched (wiki blocked, forum thread doesn't embed full table).

#### VERSION B: Current (poedb.tw — post-3.27)
**Source:** poedb.tw/us/Cyclone (accessed 2026-07-23) — labeled as "dataset" class in corpus

Verbatim from poedb.tw:
- "Attack Speed: 300% of base"
- "(82—150)% of base" [damage at gem levels 1–20]
- "Effectiveness of Added Damage: (82—150)%"
- "Radius: 16"
- "Mana Cost: (2—3) Mana"
- "Movement Speed Penalty: (20—30)% less Movement Speed"
- "AoE Scaling: 15% increased Area of Effect per 0.1 metre additional Melee Strike Range"
- "Quality Bonus: (0—5)% increased Area of Effect per 0.1 metre additional Melee Strike Range"

**poedb.tw Level Progression Table (verbatim):**

| Gem Lvl | Req Level | Str | Dex | Mana Cost | Base Dmg % | Move Speed Penalty |
|---------|-----------|-----|-----|-----------|-----------|-------------------|
| 1 | 28 | 29 | 42 | 2 | 81.6% | 30% |
| 2 | 31 | 32 | 46 | 3 | 85.2% | 29% |
| 3 | 34 | 35 | 50 | 3 | 88.8% | 29% |
| 4 | 37 | 37 | 54 | 3 | 92.4% | 28% |
| 5 | 40 | 40 | 58 | 3 | 96% | 28% |
| 6 | 42 | 42 | 61 | 3 | 99.6% | 27% |
| 7 | 44 | 44 | 63 | 3 | 103.2% | 27% |
| 8 | 46 | 46 | 66 | 3 | 106.8% | 26% |
| 9 | 48 | 48 | 69 | 3 | 110.4% | 26% |
| 10 | 50 | 49 | 71 | 3 | 114% | 25% |
| 11 | 52 | 51 | 74 | 3 | 117.6% | 25% |
| 12 | 54 | 53 | 76 | 3 | 121.2% | 24% |
| 13 | 56 | 55 | 79 | 3 | 124.8% | 24% |
| 14 | 58 | 57 | 82 | 3 | 128.4% | 23% |
| 15 | 60 | 59 | 84 | 3 | 132% | 23% |
| 16 | 62 | 60 | 87 | 3 | 135.6% | 22% |
| 17 | 64 | 62 | 90 | 3 | 139.2% | 22% |
| 18 | 66 | 64 | 92 | 3 | 142.8% | 21% |
| 19 | 68 | 66 | 95 | 3 | 146.4% | 21% |
| 20 | 70 | 68 | 98 | 3 | 150% | 20% |

### Cyclone — Mechanic notes for KF-2 join-key

Cyclone is a CHANNEL-MOVE skill. It deals weapon damage per hit in a radius while the player moves. Key mechanic: the "300% of base" attack speed modifier means Cyclone's attack rate = (character base attack speed with weapon) × 3.0. Damage per hit = weapon physical DPS × (effectiveness%) with the weapon's inherent damage range. There is no single-hit "damage roll" separate from weapon damage — the kit damage is fundamentally WEAPON-DEPENDENT.

**JOIN-KEY NOTE FOR GAMORA:** poe1-cyclone damage cannot be expressed as a fixed source_value independent of weapon. The correct source_value captures WEAPON DPS at the documented build point × effectiveness%. Kit numeric rows should capture: (a) effectiveness % (59% per 3.15 era, 150% per current poedb), (b) weapon physical DPS at documented build point (gap — see below), (c) attack speed multiplier (300% = 3.0×). The normalization_rule must compose these. This is a formula-rule not a scalar-rule.

### Character Attributes / Defense — Cyclone Slayer Build Point

**Source:** maxroll.gg Cyclone Slayer guide + poe-vault.com + overgear.com (all accessed 2026-07-23)

What IS anchored verbatim:
- "~96% Crit Chance in top-end gear" — poe-vault.com [3.20] guide
- "6k life pool" — overgear.com Cyclone build guide
- "75%" cap for Fire/Cold/Lightning resistances — maxroll guide
- "Precise Technique requires your Accuracy to be higher than your maximum Life to grant 40% more damage" — maxroll (mechanic ref)
- Weapon target: "Exquisite Blade with 650+ dps" / "850+ in endgame" — overgear
- Gem requirement: Cyclone available "at level 28" (maxroll)
- "Flesh and Stone Now requires 35% Mana reservation" (forum build thread)
- Character build uses Slayer ascendancy: "50% increased Accuracy Rating" / "15% more damage" from Impact / "10% reduced damage taken while leeching" from Brutal Fervour / "25% DPS increase" from Headsman

**GAPS — Character stat sheet:**
- Specific attribute values (Strength, Dexterity, Intelligence) at build point: GAP
- Life pool exact value: PARTIAL — "6k" quoted but not verbatim stat sheet
- Armor/Evasion: GAP
- Block: Slayer builds do not use block (not melee block); gap
- Resist percentages exact values: GAP — only cap target (75%) stated
- Attack speed at build point: GAP
- Crit multiplier: GAP
- Weapon physical DPS verbatim at build point: PARTIAL — "650+ dps" target only

---

## KF-3 MONSTER SIDE — PoE1 White Maps (Zone Level 68)

**Difficulty tier:** White (T1) maps, zone level 68 — the earliest endgame map tier. Chosen per KFL-3 "early-accessible, well-documented" criterion; Cyclone Slayer is an endgame build (Acts 1-10 are leveling; the documented build fights maps).
**Source for all monster stats:** poedb.tw (accessed 2026-07-23) — labeled as "dataset" class in corpus.

### MOB 1: Cannibal Female (Zone Level 68 — Ledge/Waterways map archetype)

Source URL: https://poedb.tw/us/Cannibal (accessed 2026-07-23)

| Stat | CannibalFemale Level 6 (Act 1 baseline) | CannibalFemaleThrowFire Level 68 (Map) |
|---|---|---|
| Life | 48 | 6,433 |
| Armour | 59 | 28,790 |
| Evasion Rating | 191 | 5,450 |
| Damage | 8 | 374 |
| Attack Time | 1.995 sec | 1.995 sec |
| Fire Resist | 0% | 0% |
| Cold Resist | 0% | 0% |
| Lightning Resist | 0% | 0% |
| Chaos Resist | 0% | 0% |
| Critical Strike Chance | 5% | 5% |

Verbatim quote: "CannibalFemale (Level 83): Life: 32,017 | Armour: 92,477 | Evasion Rating: 9,039 | Damage: 900 | Attack Time: 1.995 | Resistances: Fire 0%, Cold 0%, Lightning 0%, Chaos 0% | Critical Strike Chance: +5%"
Verbatim quote (Level 6 Act baseline): "Life: 48 | Armour: 59 | Evasion Rating: 191 | Damage: 8 | Attack Time: 1.995 | Resistances: all 0% | Critical Strike Chance: +5%"

### MOB 2: Goatman (Zone Level 68 — Dried Lake/Tower map archetype)

Source URL: https://poedb.tw/us/Goatman (accessed 2026-07-23)

| Stat | GoatmanLeapSlamAbberathGauntlet (Level 68) |
|---|---|
| Life | 7,077 |
| Armour | 28,790 |
| Evasion Rating | 4,976 |
| Damage | 616 |
| Attack Time | 1.2 sec |
| Fire Resist | 40% |
| Cold Resist | 0% |
| Lightning Resist | 0% |
| Chaos Resist | 0% |
| Critical Strike Chance | 5% |
| Damage Range | 493–740 |

Verbatim quote: "GoatmanLeapSlamAbberathGauntlet (Level 68): Life: 7,077 | Armor: 28,790 | Evasion Rating: 4,976 | Damage: 616 | Attack Time: 1.2 | Fire Resistance: 40% | Cold/Lightning/Chaos Resistance: 0% | Critical Strike Chance: 5% | Base Damage Range: 493—740"
Verbatim quote (shared multipliers): "Life multiplier 110% | Damage multiplier 165% | Attack Distance 4 ~ 7"

### MOB 3: Corrupted Rhoa (Zone Level 68 Map)

Source URL: https://poedb.tw/us/Corrupted_Rhoa (accessed 2026-07-23)
Search-confirmed data: poedb.tw search result verbatim

| Stat | RhoaSkeletonBlackMap (Level 68) |
|---|---|
| Life | 7,205 |
| Armour | 35,988 |
| Evasion Rating | 4,739 |
| Damage | 601 |
| Attack Time | 1.395 sec |
| Fire Resist | 0% |
| Cold Resist | 40% |
| Lightning Resist | 0% |
| Chaos Resist | 0% |
| Critical Strike Chance | 5% |
| Special Modifier | "60% increased Attack Speed" |

Verbatim quote: "RhoaSkeletonBlackMap (Level 68): Life: 7,205 | Armour: 35,988 | Evasion Rating: 4,739 | Damage: 601 | Attack Time: 1.395 | Resistances: Fire 0%, Cold 40%, Lightning 0%, Chaos 0% | Crit: 5%"

### MOB 4: Infested Rhoa (Zone Level 68)

Source URL: https://poedb.tw/us/Infested_Rhoa (accessed 2026-07-23)

| Stat | Value |
|---|---|
| Life | 4,503 |
| Armour | 35,988 |
| Evasion Rating | 4,739 |
| Damage | 374 |
| Attack Time | 1.395 sec |
| Fire Resist | 0% |
| Cold Resist | 40% |
| Lightning Resist | 0% |
| Chaos Resist | 0% |
| Critical Strike Chance | 5% |
| Model Size | 115% |
| Experience Multiplier | 120% |

Verbatim quote: "Life: 4,503 | Armor: 35,988 | Evasion Rating: 4,739 | Damage: 374 | Attack Time: 1.395 | Resistances: Fire 0%, Cold 40%, Lightning 0%, Chaos 0% | Crit: 5%"

### MOB 5: Albino Rhoa (Zone Level 68 — special)

Source: search result verbatim from poedb.tw search synthesis (2026-07-23)
Verbatim: "Albino Rhoa (Level 68): Life: 7,720 | Armour: 34,548 | Damage: 0 | Attack Time: 1.395"

Note: Damage = 0 is likely a special/non-attacking variant (Albino Rhoas do not attack directly in game).

### Additional Rhoa variants (zone 68) — search result verbatim
Source: poedb.tw search results synthesis (2026-07-23)

| Monster | Level | Life | Armour | Damage | Attack Time |
|---|---|---|---|---|---|
| Primal Rhoa | 68 | 24,318 | 34,548 | 523 | 0.93 sec |
| Saqawine Rhoa | 68 | 28,950 | 35,988 | 560 | 1.395 sec |
| Tercel Rhoa | 68 | 8,235 | 35,988 | 598 | 1.395 sec |

---

## GAPS — Kit Side

| Field | Status |
|---|---|
| Cyclone damage effectiveness at 3.15 build point — full level table | PARTIAL — level 20 = 59% verbatim (forum post); no per-level table for 3.15 era fetched |
| Cyclone damage effectiveness version pinning | GAP — critical version discrepancy (59% vs 150%); must pin to 3.15 or update corpus citation |
| Weapon physical DPS at documented build point | PARTIAL — "650+ dps" target; no verbatim stat sheet |
| Character attributes (Str/Dex/Int) | GAP |
| Life pool exact | PARTIAL — "6k life pool" quoted; not stat-sheet verbatim |
| Armor/Evasion exact values | GAP |
| Attack speed at build point | GAP |
| Crit multiplier | GAP |
| Fire/Cold/Lightning/Chaos resist exact values | GAP — only 75% cap target |

## GAPS — Monster Side

| Field | Status |
|---|---|
| Monster damage range (min/max) for most poedb mobs | PARTIAL — poedb shows "Damage" as a single value (likely average or calculated); min/max range only found for Goatman (493-740) |
| Monster attack speed (attacks per second) | PARTIAL — attack TIME given (e.g., 1.395 sec/attack); must invert for attacks/sec |
| Normal-rarity vs magic/rare monster HP multipliers | GAP — poedb entries are single-rarity variant; magic/rare scale not verbatim-anchored for these specific mobs |

---

## Sources consulted (all read-only, 2026-07-23)

| URL | Result |
|---|---|
| https://poedb.tw/us/Cyclone | Fetched — full level table verbatim, current version (post-3.27) |
| https://www.pathofexile.com/forum/view-thread/3078559 | Fetched — 3.15 era, 59% verbatim; gem links |
| https://www.poewiki.net/wiki/Cyclone | ACCESS DENIED (Anubis protection) |
| https://pathofexile.fandom.com/wiki/Cyclone | HTTP 402 |
| https://www.poe-vault.com/guides/ultimate-cyclone-slayer-build-guide | Fetched — "Out of date", ~96% crit only |
| https://www.poe-vault.com/guides/murder-on-a-budget-cyclone-slayer-passive-skill-tree-gem-links | Fetched — gem links only, PoB external |
| https://maxroll.gg/poe/build-guides/cyclone-shockwave-slayer-league-starter | Fetched — stat targets only (75% resist cap) |
| https://overgear.com/guides/poe/cyclone-slayer-build-guide/ | Fetched — "6k life pool", "650+ dps weapon" |
| https://poedb.tw/us/Cannibal | Fetched — level 6 and level 68 variants, verbatim |
| https://poedb.tw/us/Goatman | Fetched — level 68 variant, verbatim |
| https://poedb.tw/us/Corrupted_Rhoa | Fetched — level 68 variant, verbatim |
| https://poedb.tw/us/Infested_Rhoa | Fetched — level 68 variant, verbatim |
| https://pathofexile.fandom.com/wiki/Monster_resistances | HTTP 402 |
| https://pathofexile.fandom.com/wiki/Monster_level | HTTP 402 |
| poedb.tw search (Rhoa variants) | Search synthesis — Primal/Saqawine/Tercel/Albino Rhoa level 68 stats |
