# Research — ARPG Genre Canon Encounter Metrology — 2026-07-07

**Mode:** A (analytical)
**Commissioner:** Gandalf (story/design steward), Matt-directed
**Sources consulted:** See Source List. Access date: 2026-07-07.

---

## Summary

Genre-canonical room dimensions, density, kill-rate, and TTK data were triangulated across Diablo 2/3/4, Path of Exile (PoE1), Last Epoch, and roguelite precedents (Hades). Unit conversions between each game's native measure and real-world meters are documented explicitly. The prior 30–50 targets-per-minute band (2026-05-17) is confirmed as appropriate for Family 1–2 engagement density; Family 4 runs substantially higher during active press. The most important genre-law finding: D3's playfield at standard resolution is 120 D3-yards × 120 D3-yards = ~36m × 36m visible, making a boss arena at 2-3 screens (70–100 D3-yards / 21–30m) genre-canonical. A hard gap exists on published absolute room-dimension data for D2/D3/D4 — no dev-side schema tables are public; all room-size findings are derived or community-inferred.

---

## Unit Conversion Reference (FIRST-CLASS per Law b)

| Engine | Native unit | Conversion to meters | Source | Confidence |
|---|---|---|---|---|
| Diablo 3 | "yard" (D3y) | 1 D3y ≈ 0.3 m (≈ 1 real-world foot) | Community measurement (Escapist article; DiabloFans forum; Diablo Wiki/Yards page; multiple independent community tests) | HIGH |
| Diablo 3 | "yard" | Character is ~6–7 D3y tall (≈ 1.8–2.1 m) | Community measurement (DiabloFans) | HIGH |
| Diablo 3 | "yard" | Screen radius = 60 D3y in all 4 directions at standard resolution → visible area 120 × 120 D3y = ~36 × 36 m | Community measurement (D2JSP forum, ROS-bot forum, multiple sources) | HIGH |
| Path of Exile 1 | "unit" pre-v3.22.1 | 1 unit = 0.1 m (10 units = 1 m) | PoE forum discussion; multiple PoE wiki references; confirmed v3.22.1 patch introduced explicit meters | HIGH |
| Path of Exile 1 | "meter" post-v3.22.1 | 1 PoE meter = 1 real-world meter | PoE forum thread; Witch character ≈ 1.62 m tall used as calibration reference | HIGH |
| Diablo 2 | sub-tile | Sub-tile = 36 × 18 pixels (isometric); tile = 160 × 80 pixels; 25 sub-tiles per tile | Phrozen Keep modding forum (primary: modder Q&A, 2000s community, multiple confirmations) | HIGH (pixel-level); LOW (real-world m conversion — see note) |
| Diablo 4 | not natively published | Community derived: 100m ≈ distance from training area to east bridge of Kyovashad using shoulder-width estimation | Community measurement (guided.news article) | MED |
| Last Epoch | not published | No community-derived unit-to-meter conversion found | — | GAP |
| Godot (our engine) | meters | 1 Godot unit = 1 m (native) | Engine spec | HIGH |

**D2 pixel-to-meter note:** A D2 tile is 160×80 pixels (isometric projection). At D2's native 800×600 resolution, roughly 5–6 tiles fit across the 800px width, giving ~5.5 × 160 = 880 px visible width. No community-agreed px-to-meter calibration found. The sub-tile/tile structure is solid for internal D2 level design reference but does not translate cleanly to a meter figure without an anthropometric anchor. **LOW confidence on any D2 meter estimate.**

---

## Room-Dimensions Table

| Family | Genre example | Native dims | Converted to meters | Conversion assumption | Notes | Confidence |
|---|---|---|---|---|---|---|
| **F1 Tight-interior dense-pack** | D3 crypt/cellar corridor tile | ~20–30 D3y wide × 30–50 D3y long | 6–9 m wide × 9–15 m long | 1 D3y = 0.3 m | D3 corridor tiles described as 1–2 "rooms" wide; 1 room ≈ 20–30 D3y. No published dev schema; community-inferred from skill range vs visible-screen geometry. | MED |
| **F1 Tight-interior dense-pack** | D4 corridor ("tube" design) | Not published in units | ~8–12 m wide corridor estimated | D4 world-scale calibration (100m = Kyovashad bridge); community feedback: "every dungeon is a tube layout" | D4 corridors are notably narrow per player feedback; Blizzard acknowledges. No exact m figure published. | LOW |
| **F1 Tight-interior dense-pack** | PoE corridor map (e.g., Cells) | Not published in units | ~12–18 m corridor width | PoE 1 unit = 0.1 m pre-v3.22; character is ~1.5 m wide; corridors ≈ 8–12 characters wide inferred from screenshots | Community-inferred; no published layout schema | MED |
| **F2 Open-field dispersed elites** | D3 open tileset (Fields of Misery, Battlefields) | ~80–120 D3y × 80–120 D3y effective engagement zone | 24–36 m × 24–36 m | 1 D3y = 0.3 m | Open D3 tilesets span multiple screens; 1 full D3 screen = ~36m visible. Open fields rated "top tier" for GR density. | MED |
| **F2 Open-field dispersed elites** | PoE open map (City Square, Dunes) | Not published in units | ~40–80 m × 40–80 m inferred | Character ≈ 1.62 m; open PoE maps described as covering much wider than screen | PoE open maps explicitly praised for movement with no walls. Larger than D3 equivalent. | LOW |
| **F3 Boss arena** | D3 Rift Guardian arena | ~80–100 D3y diameter | 24–30 m diameter | 1 D3y = 0.3 m | D3 boss areas are typically 1.5–2 full screens diameter. A 30 D3y radius = ~2 screens' reach from center. | MED |
| **F3 Boss arena** | PoE map boss arena | ~25–40 m diameter | 25–40 m (native meters post-v3.22) | Direct meters | PoE boss rooms described as fitting comfortably within ~2 screens; 5m extends beyond 16:9 border per forum calibration | MED |
| **F3 Boss arena** | D4 boss chambers | Not published | ~20–35 m diameter estimated | D4 world-scale calibration | Boss areas appear larger than corridors; no published dim | LOW |
| **F3 Boss arena** | Last Epoch boss room | "Small" arena type cited for Heorot's Arena, Rust Land Arena; "medium" for Magma Arena | Estimate: small ~15–20m diameter; medium ~25–35m diameter | No unit conversion confirmed | Qualitative from Last Epoch tools guide; no m conversion | LOW |
| **F4 Escape plow-through** | D2 Secret Cow Level | Wide open zone; 350–450 cows per area | Area estimated 60–90 m × 60–90 m | D2 no reliable px-to-m conversion; inferred from cow density description "no zone puts more monsters in your face per sq ft" | D2 cow level is explicitly the highest-density area; open layout, no corridors | LOW |
| **F4 Escape plow-through** | D3 cursed chest / Neph Rift floor | ~120 × 120 D3y visible per screen, multi-room | 36 × 36 m per screen-equivalent; multi-screen area | 1 D3y = 0.3 m | High-density runs use full-screen monster stacking | MED |
| **F4 Escape plow-through** | PoE Blight map | Wide-lane map; pump defense 5-min timer | ~40–80 m across active combat zone estimated | PoE meters; lane layout radiates from pump | 8 roots max; lanes radiate outward | MED |

**Screen-relative sizing reference (Law b sanity check):**
Our locked Godot camera (FOV 40, pitch -55°, distance 34m) gives a visible floor footprint estimated at approximately 28–35m wide × 20–26m deep (based on camera geometry; not measured in engine). Current floor-1 rooms are 20–30m. This aligns well with D3's single-screen equivalent of 36m. A "1-screen room" in our engine ≈ 24–30m. A boss arena at 2+ screens ≈ 40–60m diameter. **All four families should target: F1 tight ≈ 12–20m wide corridor or cell; F2 open ≈ 28–45m; F3 boss ≈ 30–50m diameter; F4 escape multi-room ≈ 40–60m.**

---

## Per-Family Anchor Tables

### Family 1 — Tight-interior dense-pack clear

| Metric | Value | Source | Confidence |
|---|---|---|---|
| Room footprint (genre canon) | 12–20m wide × 15–25m long | Derived: D3 corridor tile ~20–30 D3y × 30–50 D3y @ 0.3m/D3y; D4 "tube" corridors qualitatively narrower | MED |
| Monster density per room | 15–25 trash + 1–2 elite packs | Derived from D3 GR progression math: elite pack = 4% bar, trash = ~0.02–0.05% each; to fill bar in a few rooms need dense trash | MED |
| Pack composition — champion pack | 3–5 champions (same type, same affixes), no added minions | D3 Fandom wiki / Maxroll: "packs of 3 to 5 monsters"; Champions cannot spawn with Minions affix | HIGH |
| Pack composition — rare/boss pack | 1 rare leader + 3–4 minions (weaker than leader) | D3 Fandom wiki / Maxroll | HIGH |
| Pack composition — PoE magic pack | 5–10 normal monsters + 1 magic leader with 1 affix | PoE wiki; Magic monsters "spawn in smaller groups" | MED |
| Pack composition — PoE rare pack | 1 rare (3–4 affixes) alone or with 3–6 normal/magic followers | PoE wiki | MED |
| Trash:elite ratio (room) | ~8:1 to 15:1 trash per elite pack | Inferred from D3 GR progression: if elite = 4%, trash = 0.02–0.05%, need ~80–200 trash per ~5 elites to fill bar | MED |
| Kill rate target — F1 | 30–60 kills/min (active clear, tight space, blender pace) | Genre band: our prior 30–50/min band confirmed; D3 GR pushing expects rift fill via trash kill rate + elite pops | MED |
| TTK — white/trash at level | <0.5 seconds (effectively instant for a functional build) | D3 wiki: "trash mobs serve as cannon fodder, dying very quickly to any well-geared character"; community universal | HIGH |
| TTK — magic/blue mob | 0.5–2 seconds | Extrapolated from trash TTK + health multiplier; no direct source | LOW |
| TTK — champion/rare elite pack | 3–15 seconds (pack clear, not single mob) | D3: elite packs give 4% bar = significant combat unit; PoE: rare fights described as notable pauses; community sense | MED |
| Win rate expectation | Very high (>95%) — these rooms should not kill average players | Genre convention: tight rooms are obstacle-clearing, not survival threats; danger comes from density surprises + AoE overlap | MED |

### Family 2 — Open-field dispersed elites

| Metric | Value | Source | Confidence |
|---|---|---|---|
| Arena footprint (genre canon) | 28–50m wide × 28–50m (open zones) | D3: open tilesets span ~1–2 screens; 1 screen = 36m. PoE open maps wider. | MED |
| Monster count per zone | 30–60 total (spread, not stacked) | D3 GR: open layouts named "top tier" because monsters spread over wide area; PoE open maps have higher total monster counts but spread across more space | MED |
| Elite density | 3–6 elite packs per zone | D3 GR elites scale with floor size; open floors = more elites due to larger footprint; community guides cite 3–8 per floor as typical | MED |
| Elite affix count | D3: champion = 3 affixes; rare = 3–4 affixes. D4: 2–4 affixes per elite. PoE: magic = 1; rare = 3–4 | D3 Maxroll / D4 Maxroll elite guides | HIGH |
| Kill rate target — F2 | 20–40 kills/min (repositioning cost; spread reduces stacking) | Lower than F1 due to travel between packs; genre: open fields = deliberate engagement pacing | MED |
| TTK — elite/rare at level | 5–20 seconds per pack (functional build, appropriate level) | D3: boss conquest benchmark = ~30s for hard bosses; elite packs substantially faster. PoE: community commentary "5–10 seconds overpowered, 15–20 seconds reasonable" for bosses (translates to elites faster) | MED |
| TTK — boss champion (mini-boss in open zone) | 15–30 seconds | D3 Boss Mode conquest data (Torment X): ~30–60s for full bosses; open-zone champions = smaller targets | MED |
| Deaths per zone | <0.5 per 10 zones at appropriate level | D3 Hardcore guide: "at comfortable level, content clears in 4–10 min intervals"; deaths should be infrequent, not expected per-zone | MED |
| Win rate expectation | High (85–95%) — occasional elite affix combinations kill unprepared players | Genre: open zones are the competency check, not the fail state | MED |

### Family 3 — Single-target champion/boss (+ adds)

| Metric | Value | Source | Confidence |
|---|---|---|---|
| Arena footprint (genre canon) | 25–50m diameter (circle or wide rectangle) | D3: boss arenas ≈ 1.5–2 full screens; PoE boss arenas ≈ 25–40m; Last Epoch: small = ~15–20m, medium = ~25–35m (estimated) | MED |
| Add wave composition | 2–8 adds spawning in 1–3 waves during fight | D3 Rift Guardian has periodic add spawns; D4 elite packs spawn minions; PoE bosses spawn adds mid-fight. "During fight" add waves = genre standard | HIGH |
| Boss TTK — at-level (competitive/functional) | 15–90 seconds | PoE2 data (translatable): "15–20s reasonable, 5–10s overpowered" for major boss. D3 RG at appropriate GR = 1–6 min (but GR bosses are intentionally tanky); D3 Boss Mode conquest = 30–60s for story bosses at Torment X. Range: 15–90s depending on boss tier. | MED |
| Boss TTK — top-end optimized | 5–15 seconds | D3: speed-push builds specifically designed for sub-1-min RG. PoE: "5–10 seconds" for top combos. | HIGH |
| Add TTK (adds during boss fight) | 1–5 seconds per add | Adds are deliberately weaker than boss; community universal — adds die quickly to AOE pressure | MED |
| Danger profile | Boss = primary lethal threat; adds = resource drain / interrupt threat | Genre universal: boss kills players; adds punish if ignored | HIGH |
| Win rate expectation | 60–80% per attempt at appropriate level | Genre: boss rooms are the intended hard gate; softcore D3/PoE — dying occasionally in boss rooms is normal and expected | MED |
| Kill rate target — F3 | Not applicable in same sense; relevant metric is boss kill % success rate, not KPM | — | HIGH |
| Deaths per boss attempt | 0–1 at appropriate level normal (softcore) | D3: "spend time getting familiar with boss patterns"; PoE: "over 2500 hours and never beat an endgame boss" = bosses are legitimately deadly | HIGH |

### Family 4 — Escape plow-through (under clock)

| Metric | Value | Source | Confidence |
|---|---|---|---|
| Zone footprint | 40–80m × 40–80m (wide, multi-corridor or open) | D2 cow level described as "small area full of cows" but high density; D3 Neph Rift has multiple rooms per floor; PoE Blight = radiating lanes across a full map | MED |
| Enemy density multiplier vs. F1 | 2–4× trash density (the defining feature of this family) | D2 cow level: "350–450 cows" per area (highest density in game). PoE Blight: continuous spawn from 8 roots. D3: cursed chest events dramatically increase local density | HIGH |
| Mob count during active press | 50–150+ on screen or engaged simultaneously | D2 cow: 350–450 total in area; screen footprint at any moment = 20–50+ engaged. PoE Blight at full density: continuous stream from all roots | MED |
| Kill rate target — F4 | 60–150+ kills/min (the "mowing" feel) | This family's identity is high throughput; D3 community explicitly values "density for efficiency"; D2 cow level is the archetype for this feel | MED |
| Timer mechanics — PoE Incursion precedent | Initial 10 seconds; killing monsters extends duration; typical incursion ≈ 30–120 seconds total depending on kill rate | Multiple PoE sources confirm initial 10s and kill-to-extend mechanic; exact per-kill extension not confirmed in public sources (GAP) | MED (structure HIGH; per-kill extension GAP) |
| Timer generosity — intended success rate | High (80–90%+ players should escape if they keep moving) | Hades "Tight Deadline": 9-min timer per biome; designed as optional speedrun challenge, not standard failure mode. D3 Rift timer 15 min: designed to be clearable by functional builds | HIGH |
| Timer pressure structure | Two patterns: (a) kill-to-extend (PoE Incursion model) — timer replenished by kills; (b) pure countdown (Hades Tight Deadline, D3 Rift) — fixed time, player must clear before expiry | Confirmed for both patterns | HIGH |
| Continuous reinforcement | Spawns do not stop during the sequence; new waves arrive regardless of kill rate | PoE Blight: "5-minute pump defense with continuous spawn from up to 8 roots"; D3 cursed events: continuous spawning until cleared | HIGH |
| TTK for fodder in F4 | Sub-0.5 seconds each (player is temporarily overpowered) | Genre: the escape beat is the power fantasy — player should not be threatening to die to individual fodder. D2 cow: normal bovines die in ~1–3 hits from geared characters | HIGH |
| Player power state | Temporarily elevated (overpowered relative to fodder) | Genre convention: escape beat follows climax; player has just beaten the boss, inventory full, using final resources. Hades: "overpowered temporary forms" design principle (Zagreus mid-escape) | HIGH |
| Clock structure — roguelite precedent | Hades "Tight Deadline": 9 min per region (base), −2 min per rank increase. Intended for skilled players; not standard mode. Dead Cells: no explicit timed-escape mechanic (momentum-driven by enemy pressure, not clock) | Hades Steam community; speedrun guides | HIGH |

---

## Cross-Cutting Metrology

### How the genre measures throughput

| Metric | Used by | Range | Source | Confidence |
|---|---|---|---|---|
| Rift completion time | D3 community/competitive | 0:30–15:00 (15 min hard cap); competitive push = 2–8 min | D3 Maxroll GR guide; GR tier upgrade cutoffs (+1/+2/+3 for different time brackets) | HIGH |
| GR tier upgrade brackets | D3 Blizzard design | +1 at 10:00–15:00; +2 at 5:00–9:59; +3 at 0:00–4:59 | D3 Maxroll GR guide | HIGH |
| Maps per hour | PoE community | Not a published dev metric; community estimates 6–20 maps/hour depending on build speed | Inferred from clear speed discussion; no single published benchmark | LOW |
| Clear speed meta (PoE) | PoE community | T15 map in 26 seconds cited as extreme speed (anecdote); community norm likely 2–5 min per map | PoE forum clear speed meta thread | LOW |
| KPM (kills per minute) | Our prior research 2026-05-17 | 30–50 KPM band (prior finding) | Validated against D3 progression math: 100% bar ÷ ~0.03% per trash mob = ~3,300 trash needed over 15 min = ~220 per minute if only trash; practical = mix of trash + elite = ~40–80 KPM for functional play | MED |
| Progression fill — D3 | Blizzard design (derived) | Elite pack = 4% per pack. Trash = ~0.02–0.05% each (derived: progress orb = ~0.5%, and "each orb as valuable as 20–30 trash mobs") | D3 Diablo Wiki Progress Orb page; D3 Maxroll | MED |

**Validation of prior 30–50 KPM band:**
Working backwards from D3 GR math: to fill a 100% bar in ~10 minutes (typical competitive pace for functional builds), assuming a mixed kill diet of 70% trash + 30% elite contribution: trash at ~0.03% each requires ~2,100 trash kills (210/min), but elite packs (4% each, ~10–15 per floor) contribute ~40–60% of bar. Net functional KPM for a 10-minute rift = roughly 40–80 gross kills/min depending on density tileset. **The 30–50 KPM prior band is conservative but reasonable for F1/F2 baseline; F4 escape beat should target 80–150 KPM.**

### Canonical ratios

| Ratio | Value | Notes | Confidence |
|---|---|---|---|
| Trash:elite:boss TTK ratio (at level) | 1 : 15–30 : 60–200 | Trash = <0.5s; elite pack = 5–20s; boss = 30–90s. Ratios: trash=1, elite≈20–30×, boss≈100–200× | MED |
| Density ratio — corridor vs. open zone | ~1 : 2–3 (corridor has lower raw count but higher encounter rate per meter) | D3: open tilesets specifically valued for stacking; corridor rooms force linear engagement | MED |
| Elite fraction of total monsters per area | ~5–10% of total monsters are elites/champions | D3 GR: a functional rift has ~5–15 elite packs vs. hundreds of trash; PoE: packs are mostly normal with occasional magic/rare | MED |
| Fraction of playtime per encounter type | F1 tight: ~40%; F2 open: ~35%; F3 boss: ~15%; F4 escape: ~10% | Derived from run structure ("25-min descent"); these are design intent targets, not measured. | LOW |
| Room-size ratio — corridor : field : boss arena | 1 : 2–3 : 2–4 | F1 corridor ~15×20m; F2 field ~30×40m; F3 boss ~30–50m diameter | MED |

### Death-rate / difficulty canon

| Game | Mode | Expected death rate at appropriate level | Source | Confidence |
|---|---|---|---|---|
| Diablo 3 | Softcore, appropriate GR | Very low per run; GR is expected to be completable; deaths reset progress but are not game-ending | D3 Hardcore guide (by contrast: HC players treat even occasional SC death as unacceptable risk signal) | MED |
| Diablo 3 | Hardcore, appropriate content | Near-zero expected; "start at comfortable level"; content should feel non-threatening in isolation | D3 HC Survival Guide (Maxroll) | HIGH |
| Diablo 3 | Boss Mode conquest | Boss kill in 30–60 seconds; ~1–3 attempts per boss at Torment X | D3 Boss Mode Conquest Guide (Icy Veins) | HIGH |
| Path of Exile | Softcore mapping | Deaths acceptable and common; no death penalty in SC beyond minor losses | Community universal; "over 2500 hours never beaten endgame boss" = bosses kill players | HIGH |
| Path of Exile | Hardcore | Near-zero expected per map; HC players report losing characters to unexpected damage spikes | Community discourse | HIGH |
| Diablo 4 | Standard | Deaths expected in boss/elite fights; dungeon trash should not threaten healthy builds | Community discussion; D4 Maxroll NM dungeon guide | MED |
| Genre summary | — | **Trash should not threaten (>99% survival per room). Elites should require attention (deaths possible on unoptimized builds, ~5–15% per pack in very difficult content). Bosses are the gate — 20–40% death rate per attempt at appropriate level is genre-normal.** | Synthesized | MED |

---

## Knowledge Gaps

1. **D3 exact per-trash-mob progression %:** Community sources give only the derived figure "0.02–0.05% each" (back-calculated from "1 progress orb ≈ 20–30 trash mobs" and "1 orb = 0.5% bar"). No dev-side schema published.
2. **PoE Incursion exact per-kill timer extension:** Confirmed that kills extend the 10-second initial timer; exact seconds-per-kill not found in public sources.
3. **Published absolute room dimensions (any title):** No title has released a dev-side room-dimension table. All dimensions are community-inferred from skill range geometry, screenshot analysis, or qualitative descriptions. D2/D3/D4 room sizes are MED–LOW confidence.
4. **Last Epoch echo dimensions:** No unit-to-meter conversion exists; arena sizes given only as qualitative labels (small/medium). No community measurement thread found.
5. **PoE map absolute dimensions:** PoE confirmed meters are real-world meters, but individual map layout dimensions are not published. PoE maps range enormously by layout type.
6. **D4 dungeon room dims in meters:** D4 world-scale calibration exists (100m ≈ Kyovashad bridge length) but no dungeon-specific room measurements derived from this anchor in community sources.
7. **Formal KPM dev targets:** No title has published a formal KPM target in external-facing documentation. All KPM data is community-derived or back-calculated.

---

## Source List

| # | Source | Type | URL | Access date |
|---|---|---|---|---|
| S1 | Diablo Wiki — Yards | Community wiki | https://diablo.fandom.com/wiki/Yards | 2026-07-07 |
| S2 | The Escapist — "How Far is a Yard in Diablo 3?" | Community analysis | https://www.escapistmagazine.com/how-far-is-a-yard-in-diablo-3-shorter-than-you-think/ | 2026-07-07 |
| S3 | DiabloFans forum — Measuring Distance in Diablo 3 | Community forum | https://www.diablofans.com/forums/diablo-iii-general-forums/diablo-iii-general-discussion/120726-measuring-distance-in-diablo-3 | 2026-07-07 |
| S4 | D2JSP forum — A Diablo Screen is Measured in Yards | Community forum | https://forums.d2jsp.org/topic.php?t=82284462&f=21 | 2026-07-07 |
| S5 | ROS-Bot forum — Screen Yardage | Community forum | https://www.ros-bot.com/forums/general-discussion/screen-yardage-23288 | 2026-07-07 |
| S6 | PoE Forum — "How far is 2 meters?" | Community forum (direct fetch) | https://www.pathofexile.com/forum/view-thread/3644222 | 2026-07-07 |
| S7 | PoE Wiki — Distance | Community wiki | https://www.poewiki.net/wiki/Distance | 2026-07-07 |
| S8 | PoE Fandom Wiki — Distance | Community wiki | https://pathofexile.fandom.com/wiki/Distance | 2026-07-07 |
| S9 | GGG Dev Manifesto — Monster Density in Maps | Primary (developer) | https://www.pathofexile.com/forum/view-thread/2029695 | 2026-07-07 |
| S10 | Maxroll D3 — Greater Rift Explained | Community guide | https://maxroll.gg/d3/resources/greater-rift-explained | 2026-07-07 |
| S11 | Maxroll D3 — Greater Rifts Push Guide | Community guide | https://maxroll.gg/d3/resources/greater-rifts | 2026-07-07 |
| S12 | Diablo Wiki — Progress Orb | Community wiki | https://www.diablowiki.net/Progress_Orb | 2026-07-07 |
| S13 | Diablo Fandom Wiki — Progress Orb | Community wiki | https://diablo.fandom.com/wiki/Progress_orb | 2026-07-07 |
| S14 | Diablo Wiki — Greater Rifts | Community wiki | https://www.diablowiki.net/Greater_Rifts | 2026-07-07 |
| S15 | Phrozen Keep forum — Size of a Tile? | Modding community (primary technical) | https://d2mods.info/forum/viewtopic.php?t=46249 | 2026-07-07 |
| S16 | Phrozen Keep forum — Number of Tiles on Screen? | Modding community (primary technical) | https://d2mods.info/forum/viewtopic.php?t=55868 | 2026-07-07 |
| S17 | Diablo Archive Wiki — Area Size (Diablo II) | Community wiki | https://diablo-archive.fandom.com/wiki/Area_Size_(Diablo_II) | 2026-07-07 |
| S18 | D3 Boss Mode Conquest Guide — Icy Veins | Community guide | https://www.icy-veins.com/d3/boss-mode-conquest-guide | 2026-07-07 |
| S19 | D3 HC Survival Guide — Maxroll | Community guide | https://maxroll.gg/d3/resources/hardcore-guide | 2026-07-07 |
| S20 | D3 Champion Monsters — Diablo Fandom | Community wiki | https://diablo.fandom.com/wiki/Champion_monsters | 2026-07-07 |
| S21 | D4 Elite and Affixes Overview — Maxroll | Community guide | https://maxroll.gg/d4/resources/elites-affixes | 2026-07-07 |
| S22 | D4 Monster Density — PCGamesN | News | https://www.pcgamesn.com/diablo-4/monster-density | 2026-07-07 |
| S23 | D4 Nightmare Dungeons — Maxroll | Community guide | https://maxroll.gg/d4/resources/nightmare-dungeons | 2026-07-07 |
| S24 | Diablo 4 Map Size Calculation — guided.news | Community measurement | https://guided.news/en/special/diablo-4-total-map-size-of-the-open-world-calculated/ | 2026-07-07 |
| S25 | PoE Incursion Guide — OutOfGames | Community guide | https://outof.games/realms/pathofexile/guides/384-path-of-exile-incursion-league-mechanic-guide/ | 2026-07-07 |
| S26 | PoE Blight Wiki — poewiki.net | Community wiki | https://www.poewiki.net/wiki/Blight_(game_content) | 2026-07-07 |
| S27 | Hades — Tight Deadline mechanic | Community (Steam + speedrun guides) | https://steamcommunity.com/app/1145360/discussions/0/3106890248086001694/ | 2026-07-07 |
| S28 | PoE2 Patch 0.5.0 boss TTK analysis — EZG | Community analysis | https://www.ezg.com/blog/poe-2-patch-0-5-0-why-5-second-boss-kills-absolutely-killing-game-your-league-start-experience | 2026-07-07 |
| S29 | D3 Secret Cow Level — multiple sources | Community wiki | https://diablo.fandom.com/wiki/The_Secret_Cow_Level | 2026-07-07 |
| S30 | Last Epoch Arena Guide — multiple | Community guides | https://maxroll.gg/last-epoch/resources/beginner-arena-guide; https://www.lastepochtools.com/guide/section/echoes | 2026-07-07 |
| S31 | PoE Clear Speed Meta thread | Community forum | https://www.pathofexile.com/forum/view-thread/1661934 | 2026-07-07 |
| S32 | D3 GR Tier Upgrade brackets | Community guide | https://maxroll.gg/d3/resources/greater-rift-explained | 2026-07-07 |
