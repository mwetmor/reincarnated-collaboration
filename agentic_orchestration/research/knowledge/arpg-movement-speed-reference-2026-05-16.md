# Research — ARPG Movement Speed Reference — 2026-05-16

**Mode:** A (analytical)
**Commissioner:** Gandalf (for Matt's design question)
**Sources consulted:** Maxroll D2, Amazon Basin D2 Wiki, Tommigustafsson speed reference, Diablo Fandom Wiki, diablo2.diablowiki.net, PoE Affix Net, poe2wiki.net, lastepoch.tunklab.com, Last Epoch forums, d4guides.gg, diablo4.wiki.fextralife.com, Blizzard D4 forums, GrimDawn Steam discussions, Torchlight IDB, Game Design Forum (D2 reverse design analysis)

---

## Summary (4 sentences)

Across the major ARPGs, early-game players typically match or slightly trail trash monsters, with the designed intent being that FRW/movement gear becomes the first meaningful gear axis that lets players outpace average enemies. By midgame, all Tier 1 games have players comfortably faster than standard trash (delta roughly +10–30% advantage), while a subset of faster-moving monster archetypes (fetishes, leapers, some PoE packs) remain threatening specifically because they close that gap. At endgame, the delta widens dramatically in PoE (player can be 100–170% above base, monsters remain roughly at base) and collapses in D3 (hard 25% gear cap keeps endgame players only modestly faster). D4 occupies a middle position post-launch with a raised 200% cap but a design that channels mobility through skill effects rather than pure stat accumulation.

---

## Tier 1 Games

### Diablo II / D2:Resurrected

**Design philosophy:** Movement is a gear-gated progression axis; unbuffed early players can be outrun by fast monster types; FRW is the primary boot affix with diminishing-returns scaling. Skill-based FRW (Vigor, Burst of Speed, Frenzy) bypasses the DR formula and is the dominant speed source in late game.

**Base speeds (patch 1.14 / D2R 2.7+; source: Maxroll D2, Amazon Basin Wiki — both agree):**
- Walk: 6 yards/s
- Run: 9 yards/s
- Minimum (fully chilled/cursed): 1.5 yards/s
- Charge (Paladin): 22.5 yards/s, unaffected by FRW items

**FRW mechanics:**
Item-based FRW uses diminishing returns: Effective FRW = (150 × FRW) / (150 + FRW). Every 1% effective FRW adds 0.06 yards/s to both walk and run. Skill-based FRW uses the same per-point rate but with no DR.

| FRW (item) | Effective FRW | Run speed (yds/s) |
|---|---|---|
| 0% | 0% | 9.0 |
| 50% | ~33% | ~11.0 |
| 100% | 60% | ~12.6 |
| 150% | 75% | ~13.5 |
| 200% | ~85% | ~14.1 |
| 325% (Barb max) | ~102% | ~15.1 |

Armor penalties: heavy armor + heavy shield each subtract 0.40 yards/s; combined penalty -0.80 yards/s to run speed (reducing base run to ~8.2 yards/s before FRW).

**Monster speed data:**
Specific per-monster yards/second values are not publicly available from any primary wiki source; the datamined files exist in modding communities (Phrozen Keep, d2mods.info) but no comprehensive public table exists. What is confirmed:
- Monster speeds vary; the game uses an internal rating scale (1 = very slow, 10 = fast, 10+ = very fast)
- Zombies: very slow (rating 1–2); players walk faster than zombies at base
- Fallen/Fallen Shaman: moderate walker, runs when fleeing (Shamans run on low HP)
- Fetishes and Leapers: explicitly documented as "fast relative to normal-speed character" — designed to be threatening to unbuffed players
- Champion modifiers: +20% FRW (Normal), +150% FRW (Fanatic), -50% FRW (Ghostly)
- Unique Boss modifier "Extra Fast": +10% to +60% FRW

**Player vs. monster delta by stage:**

| Stage | Definition | Player run speed | Trash monster speed (est.) | Delta |
|---|---|---|---|---|
| Early (Act 1, L1–20) | No FRW gear, medium armor | ~8.2 yds/s | 4–8 yds/s (zombie–fallen range) | Player at parity or slightly behind fast types |
| Mid (Act 3–4, L30–50) | ~60–100% FRW from gear | ~11–12.6 yds/s | 5–9 yds/s | Player +25–40% faster than trash |
| Late (A85 farming, full gear) | 150–200% item + skill FRW | 13–15+ yds/s | 5–9 yds/s | Player +60–100% faster than trash; Fanatic champions can still match |

**Patch anchor:** Patch 1.14d (ladder) / D2R 2.7 (essentially identical speed mechanics). No breakpoint table exists for FRW because the formula produces a continuous result, not a frame-rounded one.

**Sources:**
- https://maxroll.gg/d2/resources/run-walk-mechanics
- https://www.theamazonbasin.com/wiki/index.php/Walk/run_speed
- http://tommigustafsson.narod.ru/movementspeed.html (note: uses different base values — 4 walk/6 run — likely pre-1.09 data or alternate frame interpretation; Maxroll/Amazon Basin consensus of 6/9 preferred)
- https://thegamedesignforum.com/features/RD_D2_6.html (design analysis)

---

### Diablo III

**Design philosophy:** Movement is a comfort/speed-farming stat, not a survival axis; a hard 25% cap from gear and Paragon points prevents extreme values; active skills and shrines bypass the cap for burst mobility. Base speed is identical for all classes and most monsters.

**Base speed:** 100% = approximately 6 yards/s (confirmed by multiple community and wiki sources; same rate for all heroes and most trash monsters).

**Movement speed sources and caps:**
- Gear (boots, legendary affixes): up to +25% total, hard cap from gear + Paragon combined
- Paragon Points: 0.5% per point, max 50 points = +25% (eats into the same 25% cap)
- Fleet Footed (Monk passive): +10%, stacks above the 25% gear cap (passive category)
- Barbarian Sprint: +40% for 3 seconds (skill, not subject to cap)
- Shrines: temporary, not subject to cap

**Player speed by stage:**

| Stage | Level range | Player MS (% of base) | Player speed (yds/s est.) |
|---|---|---|---|
| Early (Normal, L1–30) | L1–30 | 100% (no gear MS) | ~6.0 |
| Mid (Acts 1–4 Hell, L50–60) | L50–60 | ~110–115% (moderate gear) | ~6.6–6.9 |
| Late / Paragon (Torment rifts) | L70+, Paragon 200+ | 125% (cap from gear/Paragon) | ~7.5; Monk with Fleet Footed ~8.1; Sprint bursts to ~8.4 |

**Monster speed data:**
Blizzard has not published monster movement speed tables. Community consensus (from multiple forum threads, Maxroll) is that base trash monsters run at approximately 100% (matching unbuffed player base speed). Some monster types run at 125–135% (equivalent to capped players); certain elites and bosses with "Fast" or "Vortex" affixes exceed this. The design intent is that geared players at 125% comfortably outpace standard trash.

| Stage | Player MS | Trash monster MS | Delta |
|---|---|---|---|
| Early | ~100% (6.0 yds/s) | ~100% (6.0 yds/s) | 0 — parity |
| Mid | ~110–115% (6.6–6.9 yds/s) | ~100% (6.0 yds/s) | +10–15% |
| Late | ~125% (7.5 yds/s) | ~100% (6.0 yds/s) | +25%; passive/skill players at +35–40% |

**Patch anchor:** Patch 2.7.x (current live; movement speed cap has been 25% since RoS launch in 2014, unchanged).

**Sources:**
- https://www.diablowiki.net/Movement_Speed
- https://us.forums.blizzard.com/en/d3/t/what-is-the-max-movement-speed/19659
- https://us.forums.blizzard.com/en/d3/t/paragon-movement-speed/61560

---

### Diablo IV

**Design philosophy:** Movement is a utility affix (mobility category) that appears only on boots and amulets; the cap was raised post-beta from 125% to 200% to allow more build expression; mounts exist for overworld traversal only (not in dungeons); temporary skill effects (Evade, class abilities) are the primary mobility layer.

**Base speed:** 100% = approximately 6 yards/s (same reference as D3; Blizzard uses consistent yardage across the franchise).

**Movement speed sources:**
- Boots: +20–24% movement speed (rolls on Sacred/Ancestral; no tempering)
- Amulet: +20–24% movement speed (same roll range, same class: All)
- Max from gear stacking (boots + amulet): up to ~48% above base
- Temporary buffs (Evade, Barb War Cry, Sorc Glass Cannon): not subject to cap; can push to 200%+ briefly
- Cap: 200% (confirmed post-beta; source: Blizzard forum June 2023)

**Player speed by stage:**

| Stage | Definition | Player MS | Player speed (yds/s est.) | Notes |
|---|---|---|---|---|
| Early (Kyovashad, L1–30) | No movement affixes | 100% | ~6.0 | Base speed only |
| Mid (L50–70 Sacred gear) | Moderate affixes | ~115–125% | ~6.9–7.5 | One boots roll typical |
| Late (L100, Ancestral BiS) | Optimal affix stacking | ~140–148% | ~8.4–8.9 | Both boots + amulet MS rolled; excludes skill buffs |

**Monster speed data:**
No datamined or published monster speed table exists publicly for D4. Community observation (forum threads, Maxroll beginners guide) indicates most standard trash tracks or slightly trails the player at mid-game gear levels. Certain fast monster types (Fallen runners, Corrupted Rogues, Fallen Hounds) are noted to close distance quickly and are presumed to exceed the 100% base. No quantified values sourced.

**Mount speed:** Overworld only; base mount speed is described as substantially faster than foot movement (Blizzard noted a 14% speed increase to mounts at some patch); mount does not scale with movement speed stat; dungeons prohibit mounts. Treat mount as a category-separate system.

**Patch anchor:** Season 4 (Loot Reborn, May 2024) — movement speed affix ranges confirmed at 20–24%. Cap confirmed at 200% since launch (post-beta change pre-June 2023).

**Sources:**
- https://diablo4.wiki.fextralife.com/Movement+Speed
- https://d4guides.gg/en/database/affixes/movement-speed
- https://us.forums.blizzard.com/en/d4/t/just-noticed-movement-speed-cap-has-been-raised-from-125-to-200-since-beta/37349

---

### Path of Exile (PoE 1)

**Design philosophy:** Movement speed is treated as a primary itemization axis — every boot can roll MS%; the absence of a hard cap (unlike D3/D4) means late-game players can be dramatically faster than monsters; movement skills (Flame Dash, Shield Charge, Dash) are a parallel system on top of base MS, making PoE players the fastest in class among Tier 1 ARPGs by endgame.

**Base speed:** 3.7 meters/second (approximately 4.0 yards/second, as confirmed by community sources referencing the PoE Wiki). The game does not use a walk/run distinction — all movement is run-equivalent. Speed is expressed as % of base (base = 100%).

**Boot affix tiers (Evasion Boots example — consistent across boot types for MS affix):**

| Tier name | Item level req | MS value |
|---|---|---|
| Runner's | 1 | 10% |
| Sprinter's | 15 | 15% |
| Stallion's | 30 | 20% |
| Gazelle's | 40 | 25% |
| Cheetah's | 55 | 30% |
| Hellion's | 86 | 35% |

Crafting (Tora bench at level 6): 13–17%. Essence of Zeal: 20–32% (fixed roll).

**Key movement speed buffs (all stack additively with gear MS):**
- Quicksilver Flask: +40% MS for 6 seconds
- Onslaught buff: +20% MS (plus +20% attack/cast speed)
- Devoto's Devotion (unique helmet): +10–20% MS
- Queen of the Forest (unique body armor): up to +50% MS at high evasion
- Boot enchant: +10% if not hit recently
- Adrenaline buff: +25% MS
- No hard cap on movement speed from passive/item stacking

**Player speed by stage (typical, not extreme outlier builds):**

| Stage | Definition | Total MS (% of base) | Speed (approx m/s) | Notes |
|---|---|---|---|---|
| Early (Acts 1–3, L1–40) | Starter boots (Runner's or Sprinter's), no flask | ~110–115% | ~4.1–4.3 | Flask inactive; typical new player |
| Mid (Acts 4–10, L40–70) | Gazelle's or Cheetah's boots + Quicksilver | ~155–170% (flask active) / ~125–130% (inactive) | 5.7–6.3 active / 4.6–4.8 inactive | Quicksilver is core league-start flask |
| Late (endgame maps, L80+) | Hellion's boots + Onslaught + Quicksilver + passives | ~200–250% (typical); 300%+ (optimized speed builds) | 7.4–9.3 / 11+ optimized | No cap; Pathfinder ascendancy builds reach 300%+ |

**Monster speed data:**
PoE does not publish monster speed tables. Community and wiki sources confirm:
- Base monster movement speed = 100% (same as player base)
- Map modifier "Monsters have increased Movement Speed": rolls at roughly 15–30% increased (specific roll range not publicly documented in a wiki table)
- Magic monsters: immune to slows below 75% of base speed; Rare: 70% minimum; Unique: 50% minimum
- Rare-rarity monsters with speed mods can match or exceed early-game players
- At endgame with Quicksilver + Onslaught active, player is typically 100–150% faster than any base-speed monster

| Stage | Player MS | Trash monster MS | Delta |
|---|---|---|---|
| Early | ~110–115% (4.1–4.3 m/s) | ~100% (3.7 m/s) | +10–15%; some pack types match player |
| Mid | ~130% inactive / ~155–170% active (4.8–6.3 m/s) | ~100% (3.7 m/s) | +30–70% depending on flask state |
| Late | ~200–250% typical (7.4–9.3 m/s) | ~100% (3.7 m/s) | +100–150%; player far outpaces all base-speed monsters |

**Patch anchor:** 3.24 Necropolis (March 2024) — boot affix tiers unchanged since ~3.10. Hellion's (35%) affix added in approximately 3.16. Flask values (Quicksilver 40%) stable since launch.

**Sources:**
- https://www.poeaffix.net/bt-ev.php
- https://www.poewiki.net/wiki/Quicksilver_Flask
- https://www.poewiki.net/wiki/Onslaught
- https://loltank.com/2023/05/10/how-to-improve-movement-speed-for-path-of-exile-character

---

## Tier 2 Games

### Diablo I

**Design philosophy:** Movement is constant and uniform; no FRW system, no movement speed gear axis. Character class does not affect base speed; speed differentiation is introduced in Diablo II.

**Base speed:** Not published in yards/second by any primary source. Community wiki notes: "Character movement speed in Diablo I is constant, and is the same for most monsters." No numeric value in yards/second confirmed from any public reference material.

**Gap:** The absence of a speed gear axis is the defining design point. All characters walk at the same speed; the game's difficulty comes from density and combat, not a chase/flee dynamic.

**Sources:**
- https://diablo.fandom.com/wiki/Movement_Speed (Fandom wiki, movement speed comparison across franchise)
- Search results consistently confirm the constant-speed design with no numeric value available

---

### Diablo Immortal

**Design philosophy:** Movement speed functions similarly to D3 with a percentage-based system; a cap exists (community reports suggest ~20% cap from gear for some classes, though documentation is inconsistent across patches). The mobile form factor de-emphasizes movement speed as a primary stat axis.

**Data availability:** Numeric base speed in yards/second is not published. Cap confirmed at approximately 20% from gear (single class-specific Crusader report; may vary by class). No monster speed table published.

**Gap:** Insufficient public documentation for quantitative reference. Video guides exist but without citable numeric tables. Recommend treating as "D3-lite" speed design — flat percentage system with a low gear cap.

**Sources:**
- https://us.forums.blizzard.com/en/diablo-immortal/t/movement-speed-capped/11084

---

### Last Epoch (1.0)

**Design philosophy:** No hard movement speed cap; movement speed is a boots-slot prefix only; game pace described by community as slower than PoE and D2; no flask system; no movement skills that dramatically multiply base speed. Developers have noted concern about "movement speed creep."

**Base speed:** Not published in meters/second or yards/second by any primary source. The game expresses speed as % of base (base = 100%).

**Boot prefix tiers (Increased Movement Speed):**

| Tier | Min % | Max % |
|---|---|---|
| 1 | 5% | 7% |
| 2 | 8% | 9% |
| 3 | 10% | 11% |
| 4 | 12% | 14% |
| 5 | 15% | 18% |

Additional sources: boot implicit affixes (~15% max on some base types); unique items (Mourningfrost: up to 29%); rings (unusual cases reaching 65% before L10, not representative of standard gear).

**Player speed by stage (approximate from community discussion):**

| Stage | Total MS (% of base) | Notes |
|---|---|---|
| Early (Campaign, L1–40) | ~100–107% | Usually no MS gear |
| Mid (Monolith, L60–80) | ~112–120% | One T3–T4 boots roll typical |
| Late (Empowered Monolith, L90+) | ~120–136% | T5 boots + unique/implicit stacking; some outlier builds higher |

**Monster speed:** One community forum post notes "monsters are too slow right now" (pre-1.0 EA). No published numeric values. Delta at midgame estimated as player slightly faster (+15–25%) with class variance (Sentinel feels fastest; Necromancer/Druid feel slowest).

**No cap** confirmed by community sources and developer discussion.

**Patch anchor:** 1.0 launch (February 2024).

**Sources:**
- https://lastepoch.tunklab.com/affix/increased_movement_speed
- https://forum.lastepoch.com/t/movement-speed/14348
- https://forum.lastepoch.com/t/movement-speed-creep-and-blasting-dev-blog-affix-feedback/62709

---

### Grim Dawn

**Design philosophy:** Movement speed is a percentage stat with a hard cap at 135%; base = 100%; the game deliberately avoids a "zoom-zoom" meta; movement speed sources are limited (boots affix, some devotion nodes, two boot components); developer-stated intent is measured, deliberate exploration.

**Base speed:** 100% (expressed in-game as percent; no yards/second value published by any primary source).

**Cap:** 135% (hard cap confirmed across multiple community sources; reaching cap is achievable by mid-endgame through gear + components).

**Component values:**
- Mark of the Traveller (boots component): +8% movement speed
- Mark of Mogdrogen (boots component): movement speed bonus (value unconfirmed from this research pass)

**Player speed by stage:**

| Stage | Total MS (% of base) | Notes |
|---|---|---|
| Early (Acts 1–2, L1–35) | ~100–108% | Little MS gear available |
| Mid (Acts 3–5, L40–70) | ~115–125% | Component + boots affix |
| Late (endgame, L85+) | 135% (cap) | Players routinely cap by this point with any MS priority |

**Monster speed:** No published table. Community describes most enemies as noticeably slower than capped players; the 135% cap means player advantage is bounded. No specific monster type speed values sourced.

**Patch anchor:** v1.2.0.0 (Fangs of Asterkarn, 2023).

**Sources:**
- https://steamcommunity.com/app/219990/discussions/0/2533741983661714407/
- https://grimdawn.fandom.com/wiki/Game_Mechanics (403 on direct fetch; data from search result snippets)

---

### Torchlight II

**Design philosophy:** Movement speed is a percentage multiplier; base is expressed in meters/second rather than yards/second; no hard cap documented from primary sources; boots affix provides incremental bonuses.

**Base speed:** 6.5 meters/second (approximately 7.1 yards/second — notably faster base than Diablo games). Source: TLIDB (Torchlight Infinite/II database).

**Boot affix example:** +9.2% movement speed (individual roll example cited); no full tier table located in this research pass.

**Formula:** Total MS = Base × (1 + all non-additive bonuses) × (1 + additive bonus 1) × (1 + additive bonus 2)...

**Gap:** No monster speed data sourced; no comprehensive affix tier table found. The Torchlight franchise has substantially less community documentation infrastructure than the Diablo series or PoE.

**Patch anchor:** Version 1.25.5.6 (last major patch).

**Sources:**
- https://tlidb.com/en/Movement_Speed

---

### Path of Exile 2 (Early Access)

**Design philosophy shift from PoE 1:** GGG intentionally reduced movement skill availability (Flame Dash equivalent is scarce; Shield Charge lacks PoE1 fluidity); movement speed penalties are multiplicative in PoE2 vs. additive offset in PoE1, reducing the efficiency of stacking; boots remain primary MS gear slot; effective player speeds are lower than late-game PoE1.

**Base speed:** 3.7 meters/second (same as PoE1; consistent base).

**Boot affix:** Community guides reference 25–30% as a solid roll; dedicated crafting articles describe "50% movement speed boots" as a high-tier crafting goal (achievable through deterministic crafting in EA 0.3+). The PoE1 tier table structure (Runner's through Hellion's) does not directly apply to PoE2's different affix system.

**Key difference:** No Quicksilver Flask equivalent in PoE2 EA; movement skills are the primary mobility layer but are fewer and less fluid than PoE1. Community consensus is that effective late-game movement speed in PoE2 is substantially lower than PoE1 — "slower and more deliberate" is the dominant community descriptor.

**Patch anchor:** EA 0.3 (2025).

**Sources:**
- https://www.mmopixel.com/news/poe-2-0-3-mobility-problem-boot-slots-and-movement-speed-issues
- https://vortexgaming.io/en/postdetail/553500

---

## Cross-Game Synthesis

### Unit normalization note

Different games use different units. Converting to a comparable form:
- D2: yards/s. 1 yard (D2 definition) = 32 px horizontal / 16 px vertical (isometric). Approximately 0.91 meters.
- D3/D4: percent of base; base ~6 yards/s (~5.5 m/s) from community consensus.
- PoE1/PoE2: percent of base; base 3.7 m/s (~4.1 yards/s).
- Torchlight II: meters/s (6.5 m/s base).
- Last Epoch, Grim Dawn: percent of base; no meters/second value published.

**For comparison, all speeds normalized to percent of each game's base:**

| Game | Early player MS | Mid player MS | Late player MS (typical, not outlier) |
|---|---|---|---|
| Diablo I | 100% (constant) | 100% | 100% |
| Diablo II | 100–105% (unbuffed) | ~125–140% (FRW gear) | ~145–170% (full gear, no skill FRW) / 200%+ (Vigor/BoS/Frenzy) |
| Diablo III | 100% | ~110–115% | ~125% (cap); 135% with Fleet Footed |
| Diablo IV | 100% | ~115–125% | ~140–148% from gear; skill effects push beyond |
| Path of Exile 1 | ~110–115% (no flask) | ~155–170% (Quicksilver active) | ~200–250% typical; 300%+ speed builds |
| Path of Exile 2 | ~110–115% | ~130–140% | ~160–190% (substantially below PoE1 late-game) |
| Last Epoch | ~100–107% | ~112–120% | ~120–136% |
| Grim Dawn | ~100–108% | ~115–125% | 135% (cap) |
| Torchlight II | ~100% | ~110–120% | ~125–135% (estimated) |

### Average player MS across games by stage

(Excluding Diablo I and Immortal as insufficient data; averaging the six games with enough data)

| Stage | Average player MS (% of base) | Range |
|---|---|---|
| Early | ~104% | 100–115% |
| Mid | ~128% | 110–170% |
| Late | ~170% | 125–300%+ |

The extremely wide late-game range is almost entirely due to PoE1's uncapped system.

### Monster MS across games by stage

Published monster speed data is genuinely sparse across all titles. The most useful confirmed data:
- **D2:** Zombies ~50–67% of player base walk; Fallen/moderate monsters ~75–100% of base; Fetishes/Leapers can exceed base
- **D3:** Base trash ~100% of player base; some fast types ~125–135%
- **D4:** Estimated ~100% base trash; some monster types faster (no numeric confirmation)
- **PoE1:** Base monsters at 100% of player base; map mods add 15–30%

No game publishes a comprehensive monster speed table as first-party documentation. All monster values above involve some community estimation.

### The delta pattern

**D2:** Delta starts near zero or negative (some fast monsters outrun unbuffed early players — this is intentional as a gear-pressure design). By late game the delta inverts strongly (+60–100% player advantage for trash; champion packs with Fanatic modifier can still match). The design actively uses fast monsters as skill checks on undergeared characters.

**D3:** Delta starts at zero (both player and trash at 100% base) and grows to exactly +25% at late game. The cap means the delta ceiling is designed and bounded — Blizzard chose to limit how fast players could pull away from monsters. Speed farming efficiency is deliberately constrained.

**D4:** Delta starts near zero, grows to approximately +40–48% at cap from gear. Less extreme than PoE; skill effects create burst mobility that temporarily widens it. Design intent appears to be that monsters remain present and threatening without a hard cap creating a ceiling — but the practical cap effect is similar to D3 for normal play.

**PoE1:** This is the outlier. Delta starts slightly positive (+10–15%), explodes at midgame (+30–70% with Quicksilver) and becomes enormous at endgame (+100–150% above base-speed monsters). The design intent is player agency and the "zoom-zoom" experience; monsters that want to threaten players must either have projectiles, telegraphed telegraphs, or be specifically fast-typed. Standard trash packs are farming resources that players can outrun at will.

**PoE2:** GGG explicitly dialed back the PoE1 delta by reducing movement skill availability and making penalties multiplicative. The result is a game closer to the D4 band (+30–60% typical late-game delta) while retaining the itemization emphasis on boots.

**Last Epoch / Grim Dawn / Torchlight II:** All cluster in the moderate band — late-game player advantage of +20–35% over standard trash, with no extreme outliers in either direction.

### Where the delta widens vs. narrows

- **Early game:** All games converge near parity or slight player disadvantage. This appears to be a universal design choice — early game should feel threatening; players earn their movement advantage through gear and levels.
- **Mid game:** PoE1 is the strongest outlier (flask economy creates large mid-game delta). D2 also diverges significantly if players have FRW gear. D3 and Last Epoch remain conservative.
- **Late game:** Delta widens everywhere, but ceiling differs dramatically. PoE1 is uncapped and player-empowering. D3's hard 25% cap produces the flattest endgame delta. D4's 200% cap is high but achievable only with both gear slots plus skill effects.

**Design observation:** The games that widen the delta most at endgame (PoE1, high-FRW D2 builds) tend to shift the difficulty from "can I outrun/survive this?" to "how do I kill this fast enough?" The games that maintain a narrow delta (D3, LE, GD) keep spatial awareness and positioning relevant at all stages.

---

## Knowledge Gaps Not Resolved

1. **D2 monster speed table in yards/second:** No publicly indexed table exists. Values exist in game files (charstats.txt and associated data) accessible to modders; the Phrozen Keep community likely has partial data but was not indexable in this research pass. The qualitative speed ratings (1–10 scale) are documented but not converted to yards/second.

2. **D3 monster speed in yards/second:** Blizzard has not published this. The "approximately 100% base = 6 yards/s" for monsters is inferred from the design-intent discussion (same rate as player), not datamined.

3. **D4 monster speed (any unit):** No datamined or developer-published values found. All D4 monster speed content is observational/qualitative.

4. **PoE1 map modifier MS range:** The "monsters have increased movement speed" map modifier range was confirmed to exist but specific minimum-to-maximum roll values are not documented in a publicly indexed table. PoEDB would have this data but was not accessible in this pass.

5. **Diablo Immortal quantitative data:** Cap value appears to be ~20% but only one class-specific forum report supports this. No base speed in m/s or yds/s.

6. **Torchlight II full boot affix tier table:** Only one example roll cited; no tier structure sourced.

7. **GDC or developer statement specifically on player-vs-monster speed delta as design choice:** No primary developer statement on this specific design axis was located. The Game Design Forum's reverse-design analysis of D2 provides secondary-source design intent, but no Blizzard or GGG developer has made a citable statement on intended player-vs-monster speed ratios.

---

## Source List

| Source | Type | URL |
|---|---|---|
| Maxroll D2 Run/Walk Mechanics | Community guide (primary for mechanics) | https://maxroll.gg/d2/resources/run-walk-mechanics |
| Amazon Basin D2 Wiki — Walk/run speed | Community wiki | https://www.theamazonbasin.com/wiki/index.php/Walk/run_speed |
| Tommigustafsson Movement Speed Reference | Community datamining (pre-1.09 values — use with caution) | http://tommigustafsson.narod.ru/movementspeed.html |
| Amazon Basin D2 Wiki — Faster Run/Walk | Community wiki | https://www.theamazonbasin.com/wiki/index.php/Faster_Run/Walk |
| Diablowiki.net Faster Run Walk | Community wiki | https://diablo2.diablowiki.net/Faster_Run_Walk |
| Game Design Forum D2 Reverse Design | Secondary source / design analysis | https://thegamedesignforum.com/features/RD_D2_6.html |
| Diablowiki.net Movement Speed | Community wiki (franchise-wide) | https://www.diablowiki.net/Movement_Speed |
| Blizzard D3 Forum — MS cap discussion | Primary (Blizzard forum) | https://us.forums.blizzard.com/en/d3/t/what-is-the-max-movement-speed/19659 |
| PoE Affix Net — Evasion Boots | Community database | https://www.poeaffix.net/bt-ev.php |
| PoE Wiki — Quicksilver Flask | Primary wiki | https://www.poewiki.net/wiki/Quicksilver_Flask |
| PoE Wiki — Onslaught | Primary wiki | https://www.poewiki.net/wiki/Onslaught |
| PoE Wiki — Movement Speed | Primary wiki | https://www.poewiki.net/wiki/Movement_speed |
| PoE movement speed improvement guide | Community guide | https://loltank.com/2023/05/10/how-to-improve-movement-speed-for-path-of-exile-character |
| PoE 2 mobility analysis | Community analysis | https://vortexgaming.io/en/postdetail/553500 |
| D4 Wiki Fextralife — Movement Speed | Community wiki | https://diablo4.wiki.fextralife.com/Movement+Speed |
| D4 Guides — Movement Speed affix | Community database | https://d4guides.gg/en/database/affixes/movement-speed |
| Blizzard D4 Forum — MS cap history | Primary (Blizzard forum) | https://us.forums.blizzard.com/en/d4/t/just-noticed-movement-speed-cap-has-been-raised-from-125-to-200-since-beta/37349 |
| Last Epoch Tunklab — MS affix tiers | Community database | https://lastepoch.tunklab.com/affix/increased_movement_speed |
| Last Epoch Forums — MS discussion | Community forum | https://forum.lastepoch.com/t/movement-speed/14348 |
| Torchlight IDB — Movement Speed | Community database | https://tlidb.com/en/Movement_Speed |
| GrimDawn Steam — MS cap discussion | Community forum | https://steamcommunity.com/app/219990/discussions/0/2533741983661714407/ |
| D2mods.info — velocity modding discussion | Modding community | https://d2mods.info/forum/viewtopic.php?t=56305 |
