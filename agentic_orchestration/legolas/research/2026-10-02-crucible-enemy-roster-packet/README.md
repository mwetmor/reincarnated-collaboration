# Crucible enemy roster: waves 151–160, for the C-9 animation and VFX build

**Date:** 2026-10-02 · **Agent:** legolas (UNKNOWN-RESEARCHER) · **Commissioner:** gandalf, for the C-9 session (Graphic Arts)
**Matt's goal (relayed, verbatim):** *"get the 3 characters up and running in terms of animations and VFX needed to have all 3 characters run the crucible/arena. We also need to create our enemies for the crucible/arena with their animations and VFx."*
**Roster of record:** kc2 pack **v3.8**, `kc2-model-pack-v3-E-s09-cp150-mech-v3p8-20261002_003532/model/` (`waves.json`, `monster_offense.json`, `monster_kinematics.json`, `projectiles.json`; the `⚑ v3p8_rows` fire ranges, emergence windows and stationary plant)
**Machine-readable:** `roster.json` (68 types → 466 member records, every ability, every clip, VFX refs, summoned bodies, sha256 of every input) · `wave_composition.csv` (one row per wave × spawn point × record, with a grade column)
**Access:** read-only throughout. No pack, oracle, port or vendor file was modified. The only writes are in this directory.

**Grades.** **DATAMINED**: read from GD's shipped data. The Edition IV `.arz` (via the range audit's `gdlib.py`, last-archive-wins = CRUCIBLE precedence) for every record field; the **Edition III animation census of 2026-08-08** (`legolas/notes/2026-08-08-kc2-threat-grammar-arz-boundary/anm_index.json` + `anm_events.json`) for clip frame counts and clip events, **because Edition IV ships no `.arc` archives**. **PACK**: a v3.8 row, id given. **INFERRED**: my arithmetic or classification, basis stated. **UNKNOWN**: not established, with what would settle it. Per-field grades are in `roster.json → field_grades`.

---

## Summary

1. **466 distinct creature records can spawn in waves 151–160, on 241 meshes but only 68 animation rigs.** A *type* in this packet is one rig: records whose animation table points at the same run clip. Meshes inside a type are reskins or variants of one skeleton. Expected bodies over the band: **172** with p06 OFF, the oracle of record (197.0 with p06 ON). *(INFERRED; count law DECODED, Lap V)*
2. **The 80 % tier is 19 rigs (81.2 % of bodies); the 95 % tier adds 16 more (35 rigs, 95.1 %).** The remaining 33 rigs together are 4.9 %, mostly single hero or boss records.
3. **The top five rigs carry 39 % of bodies:** Fleshwarped corruptions (aether-corruption), wraiths, Chthonian devourers, Ugdenbog crabs and Ugdenbog golems. All five are mainly trash.
4. **Peak concurrent roster bodies: wave 158, expected 33, envelope 27–42 (p95 38).** It is all ring trash: Chthonian devourers ~12, crabs ~8, sand lizards ~7. Waves don't overlap: a wave ends only when every proxy is dead. So the peak is bounded by one wave's total and reaches it if nothing dies inside the first 4 s. **Summoned bodies are on top and are not counted** (§ E). For context, the referent's measured living count was **19–36, median 25** (FOOTAGE, Lap U F-10). *(INFERRED)*
5. **Two humanoid skeletons cover 11 % of bodies (19.6) across 10 types.** These are the PC hero rigs, `creatures/pc/anm` (male, `hero01_*`) and `anm_heroine` (female, `heroine01_*`), with unarmed, 1H sword, 2H, gun1h and gun2h sets. Most of the bosses use them, and so do the Apparitions, the Possessed and Eldritch Armors and the Haunted Nobles/Champions. Building one male and one female humanoid rig serves all 10 types.
6. **The Carnivorous Plant (#10, 5.9 bodies) is a stationary turret** (PACK `V38-ST1-1`): walk and run are its combat-idle clip, and it never rotates. It arrives only at p05 on waves 151 and 153, with a 1.5 s sprout clip. **The Ugdenbog golems also summon it** (owner exposure 3.9 bodies, § E), so it is on screen more often than its wave count says.
7. **Wave 159 has 5–7 bosses at once, one per spawn point, and wave 160 has 4 nemeses or bosses** (§ B). A boss or nemesis is a single record, so their art cost is per record. The rig is usually shared, though (most use the humanoid, rylok, statue or colossus rigs).

---

## A. Priority tiers

Ordered by expected bodies on screen over waves 151–160 (p06 OFF). The *role mix* splits a rig's bodies by the role of the records that use it: trash (trash pools), champion-hero (HERO / BOUNTY / DEVOTION pools), boss (BOSS pools), nemesis (`/nemesis/` records). Size = `actorRadius × scale` (m) over the rig's members. Run speed = `characterRunSpeed × 3.209 m/s` (PACK K4-0).

### Tier 1 — 80 % of bodies (19 rigs)

| # | type (rig) | main names | bodies | cum % | role mix (bodies) | family | radius×scale m | run m/s | attack style (bodies-weighted) | weapon | p05? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `aetherialcorruption` | Fleshwarped Aberration / Fleshwarped Stormwalker / Fleshwarped Chilled One | 17.78 | 10.3 | trash 12.7, champion-hero 4.1, boss 1 | Aether Corruption | 0.56–0.92 | 3.69–4.01 | melee 59% · projectile 31% | unarmed | 11 |
| 2 | `wraith` | Wraith / Spiteful Wraith / Eldritch Spirit | 15.52 | 19.4 | trash 11.9, champion-hero 3.4, nemesis 0.2 | Undead | 0.35–0.46 | 2.25–3.21 | melee 49% · aura 19% · aoe 14% · projectile 12% | unarmed | 1.5 |
| 3 | `devourer` | Chthonian Hungerer / Chthonian Devourer / Chthonian Gorger | 13.02 | 26.9 | trash 12.6, champion-hero 0.4 | Chthonic | 0.32–0.8 | 3.21–4.17 | melee 72% · aoe 26% | unarmed | — |
| 4 | `crabmonstrosity` | Ugdenbog Crab / Ugdenbog Spikeshell / Ugdenbog Stoneshell | 11.51 | 33.6 | trash 8, champion-hero 3.3, boss 0.2 | Beast | 0.5–1.12 | 3.21 | melee 71% · projectile 15% · aoe 12% · summons on 34% of bodies | unarmed | — |
| 5 | `golemswamp_phase01` | Ugdenbog Golem / Ugdenbog Mossflinger / Jormundur ~ Diseased | 9.03 | 38.9 | trash 5.6, champion-hero 3.4 | Plant + Eldritch | 0.5–0.99 | 3.85–4.97 | aoe 66% · melee 17% · projectile 17% | unarmed | 3.1 |
| 6 | `hero01_unarmed` | Apparition / Possessed Armor / The Sentinel | 7.91 | 43.5 | trash 4.3, boss 2.3, nemesis 0.8, champion-hero 0.5 | Magical + Eldritch | 0.35–0.98 | 1.93–3.85 | projectile 40% · aoe 39% | unarmed | — |
| 7 | `sandlizard` | Moltenclaw / Sandclaw / Riftclaw | 7.46 | 47.8 | trash 7.5 | Beast | 0.25–0.94 | 2.89–3.21 | melee 84% · aoe 16% | unarmed | — |
| 8 | `wendigo` | Wendigo / Reaper of the Lost / Wendigo ~ Marroweater | 6.04 | 51.3 | trash 3.3, champion-hero 1.8, nemesis 0.7, boss 0.2 | Undead + Beast | 0.75–0.98 | 2.89–3.21 | melee 55% · projectile 26% · aura 17% | unarmed | — |
| 9 | `aetherialimp` | Aetherial Scamp / Aetherial Imp / Brolbos ~ Arctic | 5.98 | 54.8 | trash 5, champion-hero 1 | Aetherial | 0.52–0.68 | 3.21 | melee 91% | unarmed | 1 |
| 10 | `carnivorousplant01a_p1` | Carnivorous Plant | 5.87 | 58.2 | trash 5.9 | Plant + Eldritch | 0.77 | **stationary** | melee 50% · projectile 50% | unarmed | 5.9 |
| 11 | `basilisk` | Juvenile Basilisk / Venomgaze Basilisk / Stonegaze Basilisk | 5.78 | 61.6 | trash 3.5, champion-hero 1.8, boss 0.5 | Beast | 0.6–1.02 | 2.25–3.21 | aoe 70% · projectile 26% | unarmed | — |
| 12 | `cannibal` | Ugdenbog Wretch / Ugdenbog Turned / Ugdenbog Marked | 5.65 | 64.8 | trash 5.3, boss 0.3 | Undead + Human | 0.72–1 | 3.21–3.53 | melee 44% · projectile 40% · buff 12% | unarmed | — |
| 13 | `thornedhorrora01` | Rimethorn Horror / Rimethorn Terror / Rimethorn Monstrosity | 5.07 | 67.8 | trash 3.5, champion-hero 1.6 | Riftspawn | 0.52–1.15 | 3.53–3.72 | melee 66% · aoe 22% · projectile 12% | unarmed | — |
| 14 | `skeleton_01a` | Storm Revenant / Flame Revenant / Frost Revenant | 5.03 | 70.7 | trash 4.6, champion-hero 0.4 | Undead | 0.39–0.46 | 3.53–3.85 | projectile 63% · aoe 22% · aura 14% · summons on 15% of bodies | unarmed | — |
| 15 | `heroine01_unarmed` | Apparition / Janaxia, the Betrayer / Larria, the Hexxer | 4.29 | 73.2 | boss 2, trash 1.6, champion-hero 0.5, nemesis 0.2 | Human | 0.35–0.68 | 1.93–3.53 | projectile 74% · aoe 13% | unarmed | — |
| 16 | `voidfiend` | Voidlurker Blightbearer / Voidlurker / Voidlurker Pestilence | 4.04 | 75.5 | trash 3.7, champion-hero 0.3 | Chthonic | 0.4–0.75 | 2.57–2.89 | aoe 48% · projectile 30% · aura 21% | unarmed | — |
| 17 | `chthonianrylok` | Ekket'Zul, Progenitor of Darkness / Gabal'Thunn, the Visage of Madness / Void Rylok | 3.48 | 77.6 | trash 1.5, boss 1.5, champion-hero 0.3, nemesis 0.2 | Chthonic | 0.8–1.57 | 2.89–3.53 | melee 42% · projectile 28% · aoe 27% | unarmed | 1 |
| 18 | `aetherialbloater` | Aetherial Bloater / Aetherial Bileeater / Aetherial Regurgitator | 3.28 | 79.5 | trash 2.5, champion-hero 0.4, boss 0.3 | Aether Corruption | 0.75–1.15 | 2.89–3.53 | melee 65% · projectile 23% · summons on 14% of bodies | unarmed | — |
| 19 | `yeti` | Diremane Brute / Kubacabra, the Endless Menace / Diremane Icebreaker | 3.04 | 81.2 | trash 1.7, champion-hero 0.6, nemesis 0.5, boss 0.3 | Beast | 1.04–1.62 | 2.25–3.69 | projectile 39% · aoe 37% · aura 14% | unarmed | — |

### Tier 2 — to 95 % (16 rigs)

| # | type (rig) | main names | bodies | cum % | role mix (bodies) | family | radius×scale m | run m/s | attack style (bodies-weighted) | weapon | p05? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 | `giant` | Asterkarn Giant / Asterkarn Behemoth / The Underking | 2.31 | 82.6 | trash 1.8, nemesis 0.5 | Beastkin | 0.7–1 | 3.21–3.53 | melee 48% · projectile 30% · aoe 22% | Spear2h | — |
| 21 | `leech` | Void Parasite / Void Souldrinker / Void Leech | 2.13 | 83.8 | trash 2.1 | Chthonic | 0.72–0.92 | 3.21 | melee 76% · aoe 12% · projectile 12% | unarmed | — |
| 22 | `heroine01_sword1h` | Haunted Noble / Torraxsteria ~ Frozen / Olga Flamebearer | 1.96 | 85.0 | trash 1.5, champion-hero 0.4 | Undead | 0.35–0.6 | 1.93–3.21 | melee 81% · projectile 15% | Sword, Scepter | — |
| 23 | `chthonianservitor` | Lunal'Valgoth, Steward of Darkness / Chthonian Drone / Chthonian Servitor | 1.9 | 86.1 | trash 1.1, boss 0.5, champion-hero 0.3 | Chthonic + Insectoid | 0.5–1 | 3.37–3.85 | projectile 42% · melee 41% · aura 10% | unarmed | — |
| 24 | `possessedstatue` | The Steward / Risen Stone, Temple Guardian / Animated Keeper | 1.9 | 87.2 | boss 1, trash 0.9 | Construct + Eldritch | 0.6–2.25 | 3.21–3.53 | melee 49% · aoe 38% · projectile 13% | Spear2h | — |
| 25 | `gryphon01a` | Corvunox ~ Vampiric / Corrot ~ Diseased / Covull ~ Swift | 1.84 | 88.2 | champion-hero 1.6, boss 0.2 | Beast | 1.15–1.25 | 3.21–3.53 | projectile 76% · aoe 10% | unarmed | 1.5 |
| 26 | `groble01` | Groble ~ Frost Clan Warrior / Groble ~ Frost Clan Tracker / Groble ~ Frost Clan Scavenger | 1.7 | 89.2 | trash 1.7 | Beastkin | 0.48–0.59 | 3.21–3.69 | melee 100% | unarmed, Ranged2h, Axe | — |
| 27 | `hero01_sword1h` | Haunted Champion / Ixall, Phantom of the Korvan Wastes / Horvald Shieldbreaker | 1.59 | 90.2 | trash 1.3, champion-hero 0.2, nemesis 0.1 | Undead | 0.35–0.76 | 1.93–3.21 | melee 84% | Sword | — |
| 28 | `heroine01_gun2h` | Haunted Noble / Agalla Varos ~ Regenerator | 1.58 | 91.1 | trash 1.5 | Undead | 0.35–0.39 | 1.93 | projectile 99% | Ranged2h | — |
| 29 | `hero01_sword2h` | Haunted Champion / Baullos Gar ~ Electrified / Senal Thandris ~ Corrupted | 1.43 | 91.9 | trash 1.3, champion-hero 0.1 | Undead | 0.35–0.39 | 1.93 | melee 97% | Mace2h | — |
| 30 | `golembone_phase01` | Skeletal Monstrosity / Ilgorr, the Eternal / Skeletal Gargantuan | 1.14 | 92.6 | trash 0.6, champion-hero 0.3, boss 0.2 | Undead | 0.9–1.12 | 4.33–4.97 | aoe 46% · buff 45% · summons on 22% of bodies | unarmed | — |
| 31 | `aetherialfleshshaper` | Fleshweaver Haraxis / Fleshshaper Hinissius / Blazragarus | 1.02 | 93.2 | boss 0.8, champion-hero 0.3 | Aetherial | 0.54–0.82 | 3.21–3.85 | aoe 43% · projectile 43% · summons on 76% of bodies | unarmed | — |
| 32 | `chthonianherald` | Chthonian Herald / Chthonian Portent / Nyarlathon, Herald of Annihilation | 1 | 93.8 | trash 0.7, champion-hero 0.2, nemesis 0.2 | Chthonic | 0.8–1.06 | 3.21–3.53 | projectile 69% · aoe 22% | unarmed | — |
| 33 | `aetherialcolossus` | Galakros, the Mountain / Crognoth, the Blazing Vanguard / Stormtitan ~ Electrified | 0.92 | 94.3 | boss 0.5, champion-hero 0.4 | Aether Corruption | 1.2–1.35 | 3.53 | projectile 37% · melee 30% · aoe 27% · summons on 15% of bodies | unarmed | — |
| 34 | `wight01a` | Iglus Bloodmonger ~ Swift / Alluc the Thirster ~ Vampiric / Raddoth, Lord Hierophant | 0.69 | 94.7 | champion-hero 0.6, nemesis 0.1 | Undead | 0.33–0.78 | 3.21 | aoe 84% · buff 11% | Sword2h | 0.5 |
| 35 | `dreadguard_sword2h` | Grul'Thunn of the Crimson Tides / Zagal'Udal ~ Electrified / Wallan'Siin | 0.68 | 95.1 | boss 0.5, champion-hero 0.2 | Chthonic | 0.6–0.96 | 3.53–3.85 | aoe 85% · projectile 14% | Axe2h | — |

### Tier 3 — the tail (33 rigs, 4.9 % of bodies)

`wight02a` (Orbon the Martyr ~ Supporter, 0.58), `ghoul` (Plagius, the Decrepit, 0.57), `heroine01_sword1h_floating` (Yurra Voideye, 0.5), `manticore` (Mogara, the Prime Matriarch, 0.5), `roc` (Avinnia of the Western Winds, 0.5), `hellhound` (Siff Icehowl, 0.49), `dranghoul_01` (Crogg the Maimer, 0.41), `fleshhulk_unarmed` (Venarius, the Backbreaker, 0.4), `slith01` (Slathra, the Plagued, 0.38), `korvaaksascended01a` (Father Kymon, Avatar of Korvaak, 0.37), `run_01` (Nucus'Dal, 0.34), `woollyrhino` (Starhorn ~ Celestial, 0.33), `reanimator` (Valdaran, the Storm Scourge, 0.33), `skeleton_01a_b` (Zantarin, the Immortal, 0.27), `heroine01_gun1h` (Avris Marrowill, 0.25), `sandbeetle01a` (Margul the Rotting, 0.25), `stalker` (Benn'Jahr, the Colossal, 0.25), `zombiemutated02` (Ballior ~ Burning, 0.22), `zombie01_unarmed` (Palleod ~ Electrified, 0.19), `prawn` (Sicrix, the Skittering ~ Voidtouched, 0.19), `half-troll_corrupted_sword1h` (Narroth, the Behemoth ~ Electrified, 0.16), `spidergiant` (Shalloth, 0.12), `abomination` (Chthonian Unraveler, 0.11), `aetherialwisp` (Athraz, the Watcher, 0.11), `golembone_phase02` (Moosilauke, the Chillwind, 0.1), `harpy` (Rixna Plaguefeather, 0.09), `hero01_gun2h` (Oligeane Dar ~ Corrupted, 0.08), `avian` (Juknuuk Bloodfeather, 0.08), `weavil` (The Locust, 0.08), `dermapteran` (Vizier Haxin, 0.07), `troll` (Bogloth the Marrowdrinker, 0.07), `half-troll_sword1h` (Glukrog Lifedrinker, 0.07), `hero01_gun1h` (Ugdenbog Cannibal ~ Bloodsinger, 0; p06-only, 2.46 if p06 ON).

### Rig families: types that share one skeleton

| skeleton directory | bones | bodies | types sharing it |
|---|---|---|---|
| `creatures/enemies/chthonian/anm` | 30 | 13.27 | `devourer`, `stalker` |
| `creatures/pc/anm` | 56 | 11.02 | `hero01_unarmed`, `hero01_sword1h`, `hero01_sword2h`, `hero01_gun2h`, `hero01_gun1h` |
| `creatures/pc/anm_heroine` | 49 | 8.58 | `heroine01_unarmed`, `heroine01_sword1h`, `heroine01_gun2h`, `heroine01_sword1h_floating`, `heroine01_gun1h` |
| `creatures/enemies/skeleton/anm` | 39 | 5.29 | `skeleton_01a`, `skeleton_01a_b` |
| `creatures/enemies/wight/anm` | 78 | 1.27 | `wight01a`, `wight02a` |
| `creatures/enemies/golem/anm` | 46 | 1.24 | `golembone_phase01`, `golembone_phase02` |

Only multi-type families are listed; every other rig stands alone. A family is the same clip directory **and** the same bone count in the Ed III `.anm` header (DATAMINED). Equal bone count is necessary for a shared skeleton, not sufficient: I did not compare bone names (INFERRED). **The bone count splits directories that look shared.** `creatures/enemies/chthonian/anm` holds six types on at least five skeletons: devourer 30 and stalker 30 (listed above as one family), dreadguard 36, `run_01` 43 (Nucus'Dal and the other chthonian-minion heroes), abomination 56 and leech 57 bones. `wendigo/animations` holds two: wendigo 45 and cannibal 41.

---

## B. Wave composition, 151–160

Expected bodies, p06 OFF (the oracle of record). **Ring** = p01–p04, plain `Proxy`, all present at t = 0 with no spawn clip. **p05** = `ProxyAmbush`: absent until +4.0 s, then each body plays its spawn clip (PACK `V38-AM1/AM2/AM3`). **p06** = the bonus point, OFF in the oracle (`V11-P06-1`), shown for reference. The envelope is the Monte Carlo min–max of the wave's total. Every row by record is in `wave_composition.csv`.

| wave | ring | p05 | total (envelope) | p06 if ON | the rigs on screen (expected bodies) |
|---|---|---|---|---|---|
| 151 | 22 | 4.5 | **26.5** (24–29) | +0 | wraith 8.5, golemswamp_phase01 4.6, carnivorousplant01a_p1 2.9, heroine01_unarmed 1.6, hero01_unarmed 1.6, heroine01_gun2h 1.5, heroine01_sword1h 1.5, wendigo 1.5, hero01_sword2h 1.3, hero01_sword1h 1.3 |
| 152 | 14 | 3 | **17** (17–17) | +3 | basilisk 5, thornedhorrora01 5, crabmonstrosity 3.2, aetherialcorruption 3, aetherialfleshshaper 0.8 |
| 153 | 19 | 4.5 | **23.5** (23–24) | +3 | skeleton_01a 3.5, wendigo 3.5, carnivorousplant01a_p1 2.9, cannibal 2.7, golemswamp_phase01 1.8, giant 1.8, groble01 1.7, hero01_unarmed 0.5, heroine01_unarmed 0.5, heroine01_sword1h 0.3 |
| 154 | 11 | 0 | **11** (11–11) | +0 | hero01_unarmed 3.5, voidfiend 2.7, cannibal 2.6, dreadguard_sword2h 0.5, chthonianrylok 0.5, korvaaksascended01a 0.4, giant 0.3, yeti 0.3 |
| 155 | 16.3 | 0 | **16.3** (16–18) | +3 | aetherialcorruption 5.7, aetherialimp 5, wraith 4.7, hero01_unarmed 0.5, heroine01_unarmed 0.5 |
| 156 | 8.9 | 7 | **15.9** (14–17) | +7 | aetherialcorruption 7.5, heroine01_unarmed 1.5, aetherialbloater 1.3, golemswamp_phase01 1.2, voidfiend 1.1, possessedstatue 0.9, chthonianherald 0.7, basilisk 0.5, heroine01_sword1h_floating 0.5, hellhound 0.5 |
| 157 | 16.4 | 3 | **19.4** (15–21) | +3 | leech 2.1, yeti 2.1, aetherialbloater 1.7, chthonianrylok 1.7, aetherialcorruption 1.6, golemswamp_phase01 1.4, chthonianservitor 1.3, skeleton_01a 1.1, aetherialimp 1, devourer 0.7, golembone_phase01 0.6, wight01a 0.6, wight02a 0.6, sandlizard 0.4, ghoul 0.3, cannibal 0.3, woollyrhino 0.3, dranghoul_01 0.3 |
| 158 | 30 | 3 | **33** (27–42) | +3 | devourer 12.2, crabmonstrosity 8, sandlizard 7, gryphon01a 1.5, wraith 1.5, skeleton_01a 0.4, slith01 0.3 |
| 159 | 4.5 | 1 | **5.5** (5–7) | +0 | hero01_unarmed 1, chthonianrylok 1, chthonianservitor 0.5, manticore 0.5, possessedstatue 0.5 |
| 160 | 4 | 0 | **4** (4–4) | +3 | hero01_unarmed 0.8, wendigo 0.7, aetherialcolossus 0.5, possessedstatue 0.5 |

**p05 by wave** (ambush; bodies emerge at +4.0 s through their spawn clip):

- **151:** `livingplant_t3`, 4–5 bodies: Carnivorous Plant 2.94, Ugdenbog Golem 1.56
- **152:** 3 of 5 Fleshwarped heroes (`aetherialcorruption_hero`): Chromallus ~ Timewarped 0.6, Disallus ~ Diseased 0.6, Challdrus the Coldheart 0.6, Icallon ~ Arctic 0.6, Vanallius the Voracious 0.6
- **153:** `livingplant_t3`, 4–5 bodies: Carnivorous Plant 2.93, Ugdenbog Golem 1.56
- **156:** 7 of ONE element (fire / ice / lightning corruption pool): Fleshwarped Stormwalker 2.36, Fleshwarped Chilled One 2.33, Fleshwarped Scorcher 2.31
- **157:** 3 heroes from ONE of the imp / corruption / wight hero pools: Orbon the Martyr ~ Supporter 0.25, Iglus Bloodmonger ~ Swift 0.25, Jirro Stormcharger ~ Electrified 0.25, Alluc the Thirster ~ Vampiric 0.25, Brolbos ~ Arctic 0.2, Phigillius Stormbile 0.2, Phanolg the Iceborn 0.2, Ghalbar ~ Regenerator 0.2, Challdrus the Coldheart 0.2, Wourble ~ Reflective 0.2, Vanallius the Voracious 0.2, Chromallus ~ Timewarped 0.2, Icallon ~ Arctic 0.2, Disallus ~ Diseased 0.2
- **158:** 3 heroes from ONE of the wraith / hypporaven (gryphon rig) hero pools: Corvunox ~ Vampiric 0.38, Corrot ~ Diseased 0.38, Covull ~ Swift 0.38, Corvulux ~ Supporter 0.38, Sulvar the Endless Hungerer ~ Vampiric 0.3, Tildoom ~ Timewarped 0.3, Tulldar Endbringer ~ Celestial 0.3, Arcanom the Soulthief 0.3, Obliterus 0.3
- **159:** **boss**, one of two pools: Ekket'Zul, Progenitor of Darkness 0.5, Okaloth ~ "The Messenger" 0.5
- **154, 155, 160:** no p05 declared.

### Bosses and nemeses (w152–w160)

Each spawn point rolls one pool, and each boss pool holds exactly one record (the limit is 1), so a listed body is the *chance* that boss appears.

- **w154:** p01: Bloodlord Thalonis (0.5) / Brother Segarius, Vengeance of Kymon (0.25) / Father Kymon, Avatar of Korvaak (0.25) · p02: Grul'Thunn of the Crimson Tides (0.5) / Gabal'Thunn, the Visage of Madness (0.5) · p03: The Underking (0.3) / Kubacabra, the Endless Menace (0.3) / Nyarlathon, Herald of Annihilation (0.15) / Ixall, Phantom of the Korvan Wastes (0.12) / Kaisan, the Eldritch Scion (0.12)
- **w155:** p01: Dralgar, the Keeper of Burrwitch (1) · p02: Ishtal, the Mind Reaper (0.51) / Allostria, the Mindthief (0.49)
- **w156:** p01: Janaxia, the Betrayer (1) · p02: Stone Basilisk (0.51) / Siff Icehowl (0.49) · p03: Larria, the Hexxer (0.5) / Yurra Voideye (0.5)
- **w157:** p01: Blugrug the Living Plague (0.34) / Plagius, the Decrepit (0.33) / Packla, the Turning (0.33)
- **w159:** p01: Lunal'Valgoth, Steward of Darkness (0.5) / Mogara, the Prime Matriarch (0.5) · p02: Risen Stone, Temple Guardian (0.5, 2 records) / Avinnia of the Western Winds (0.25) / Ilgorr, the Eternal (0.25) / Venarius, the Backbreaker (0.25) / Inashkor, Temple Guardian (0.25) · p03: The Sentinel (1) · p04: Avris Marrowill (0.25) / Rimehorn (0.25) / Margul the Rotting (0.25) / Namadea, the Screecher (0.25) · p05: Ekket'Zul, Progenitor of Darkness (0.5) / Okaloth ~ "The Messenger" (0.5, 2 records)
- **w160:** p01: Shriek (0.1) / Moosilauke, the Chillwind (0.1) / The Iron Maiden (0.1) / Curate Ignus (0.1) / Zantarin, the Immortal (0.1) / Fabius "the Unseen" Gonzar (0.1) / Raddoth, Lord Hierophant (0.1) / Benn'Jahr, the Colossal (0.1) / Vinn "the Giant" Ozmald (0.1) / Valdaran, the Storm Scourge (0.1) · p02: Reaper of the Lost (0.2) / Kubacabra, the Endless Menace (0.2) / Reaper of Rot (0.2) / The Underking (0.2) / Grava'Thul, the Voiddrinker (0.2) · p03: Archmage Aleksander (0.5) / Reaper of the Lost (0.5) · p04: Galakros, the Mountain (0.5) / The Steward (0.5)
- **w152:** p04: Fleshweaver Haraxis (0.25) / Fleshshaper Hinissius (0.25) / Fleshweaver Krieg (0.25, 2 records) / Carraxus Foul (0.25)

**Peak concurrent roster bodies per wave** (= the wave's total, if nothing dies before p05 lands; INFERRED):

| wave | 151 | 152 | 153 | 154 | 155 | 156 | 157 | 158 | 159 | 160 |
|---|---|---|---|---|---|---|---|---|---|---|
| expected | 26.5 | 17 | 23.5 | 11 | 16.3 | 15.9 | 19.4 | 33 | 5.5 | 4 |
| max (p06 OFF) | 29 | 17 | 24 | 11 | 18 | 17 | 21 | 42 | 7 | 4 |
| max (p06 ON) | 29 | 20 | 27 | 11 | 21 | 24 | 24 | 45 | 7 | 7 |
| rigs with ≥ 0.5 expected bodies | 10 | 5 | 8 | 4 | 4 | 9 | 13 | 5 | 3 | 3 |
| rigs that can appear at all | 10 | 5 | 44 | 10 | 5 | 11 | 26 | 22 | 13 | 14 |

---

## C. Type cards — Tier 1

Each card covers who uses the rig, size, locomotion, the core clips of the lead record, then the abilities sorted by how many bodies use them. **GD fire range** is the v3.8 operating value (`gd_use_range_m`, HI limb, centre to centre; PACK `V38-GR2`). It is not the pack's legacy `reach_m`, which the range audit showed to be a projectile flight cap. Special slots are also gated by the creature's band annulus. Where one applies, the arrow gives the **window the special can actually fire in**: from the band minimum (when it binds) to the smaller of the fire range and the band maximum, both centre to centre (INFERRED from the DATAMINED terms on the same row). Example: the plant's mortar has a `Boss` profile (33.6 m) but a MediumRange band, so it fires from 3.6 to 23.1 m. Clip lengths: `dur_s = (frames−1)/30` at anim speed 1.0. **rel** = the release or impact frame, the first `*Hit` callback in the clip (or the first `PS*Start`). *inf* = the clip is the class-default clip (no special-anim ref; INFERRED). *ref unbound* = the skill names a special anim the table does not carry (UNKNOWN).

### 1. `aetherialcorruption` — Fleshwarped Aberration · 17.78 bodies (10.3 % cum.)

- **Lead record:** `records/creatures/enemies/aetherialcorruption_c01.dbr` (Fleshwarped Aberration, trash, GD class Champion)
- **Records:** 15 on 6 meshes. Names: Fleshwarped Aberration / Fleshwarped Stormwalker / Fleshwarped Chilled One / Fleshwarped Scorcher …
- **Role mix (bodies):** trash 12.66, champion-hero 4.12, boss 1 · **family:** Aether Corruption
- **Meshes (bodies):** `aetherialcorruption01a` 13.49, `aetherialcorruption01g` 1, `aetherialcorruption01c` 0.83, `aetherialcorruption01f` 0.83, `aetherialcorruption01e` 0.83, `aetherialcorruption01a_arctic` 0.8
- **Anim table(s):** `anm_aetherialcorruption` · style prefix `unarmed`
- **Size:** actorRadius 0.45–0.55 m · scale 1.25–2.05 · radius×scale 0.56–0.92 m · actorHeight 2 (template default; not a modelled height) · lead mesh bind-pose AABB height 2.98 *mesh units, Lap F caveat* *(DATAMINED)*
- **Locomotion:** characterRunSpeed 1.15–1.25 → **3.69–4.01 m/s** (INFERRED, × K4-0) · walkSpeed 0.8
- **Attack style:** melee 59% · projectile 31% *(INFERRED)* · weapon: unarmed
- **Core clips (lead):** idle `aetherialcorruption_combatidle_a01` 151f · run `aetherialcorruption_run_a01` 31f · walk `aetherialcorruption_walk_a01` 61f · attack ×3: `aetherialcorruption_attack_b01` 46f (hit f17), `aetherialcorruption_attack_d01` 49f (hit f29), `aetherialcorruption_attack_e01` 47f (hit f26) · spawn `aetherialcorruption_spawn_a01` 148f · take_hit `aetherialcorruption_gethit_a01` 21f · die: `aetherialcorruption_death_a01` 53f
- **Spawn:** ring 6.79 · p05 10.99 · waves 152 (3), 155 (5.7), 156 (7.5), 157 (1.6)
  - p05 emergence: Fleshwarped Stormwalker: `aetherialcorruption_spawn_a01` 148f → **2.45–4.9 s** (PACK `V38-AM3-2`)
  - p05 emergence: Fleshwarped Chilled One: `aetherialcorruption_spawn_a01` 148f → **2.45–4.9 s** (PACK `V38-AM3-1`)
  - p05 emergence: Fleshwarped Scorcher: `aetherialcorruption_spawn_a01` 148f → **2.45–4.9 s** (PACK `V38-AM3-3`)
  - p05 emergence: Challdrus the Coldheart: `aetherialcorruption_spawn_a01` 148f → **2.45–4.9 s** (PACK `V38-AM3-7`)
  - p05 emergence: Chromallus ~ Timewarped: `aetherialcorruption_spawn_a01` 148f → **2.45–4.9 s** (PACK `V38-AM3-10`)
  - p05 emergence: Icallon ~ Arctic: `aetherialcorruption_spawn_a01` 148f → **2.45–4.9 s** (PACK `V38-AM3-11`)
  - p05 emergence: Disallus ~ Diseased: `aetherialcorruption_spawn_a01` 148f → **2.45–4.9 s** (PACK `V38-AM3-9`)
  - p05 emergence: Vanallius the Voracious: `aetherialcorruption_spawn_a01` 148f → **2.45–4.9 s** (PACK `V38-AM3-8`)
- **Summons:** `trap_icespike_hero_a01` (limit 6, burst 1, ttl 12–15 s; granted)

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| initial | `aetherialcorruption_rotskin` | aura (toggled) | aura | 0 m/s · r 1 | 0.25/3.5 · aura 3.5 | applied at spawn (initial skill); no cast clip | poison 2 s; fire 2 s | 7: pfx_zombie_poisonaura01 | 9.22 |
| special1 | `aetherialcorruption_poisonprojectilenova` | projectile (ring / nova) | 6.31–6.49 → **0–6.49** [Medium] | 14 m/s · r 0.1 | — | `aetherialcorruption_roardouble_a01` 71f · rel f26 (0.87 s) | poison 5 s | 7: pfx_waterpoisonorb_impact, pfx_waterpoisonorb_flight | 8.4 |
| basic | `aetherialcorruption_poisonpincer` | melee (charge) | 2.81–2.99 | — | — | `aetherialcorruption_attack_c01_poison` 46f · rel f16 (0.53 s) | poison 2 s | 8: pfx_zombiemutant_aethersmash_warmup01, pfx_zombiemutant_aethersmash_warmup02 | 6.76 |
| basic | `aetherialcorruption_icepincer` | melee (charge) | 2.75–2.99 | — | — | `aetherialcorruption_attack_c01_cold` 46f · rel f16 (0.53 s) | — | 8: pfx_zombiemutant_aethersmash_warmup01, pfx_zombiemutant_aethersmash_warmup02 | 3.17 |
| basic | `aetherialcorruption_lightningpincer` | melee (charge) | 2.75 | — | — | `aetherialcorruption_attack_c01_lightning` 46f · rel f16 (0.53 s) | offensiveability 3 s | 9: pfx_zombiemutant_aethersmash_warmup01, pfx_zombiemutant_aethersmash_warmup02 | 2.36 |
| dying | `aetherialcorruption_detonate_lightning` | aoe | on death | — | 4 | fires at death (death clip) | lightning 3 s | 3: pfx_electricalblast_01 | 2.36 |
| initial | `aetherialcorruption_stormskin` | buff (toggled) | aura | 16 m/s · r 0.5 | — | applied at spawn (initial skill); no cast clip | lightning 2 s | 6: pfx_lightningorb_large01, pfx_lightningorb_impact01 | 2.36 |
| special1 | `aetherialcorruption_chillwind` | aura (timed) | 6.25 → **0–5** [Short] | — | 3.6 | `aetherialcorruption_attack_e01` 47f · rel f26 (0.87 s) *inf* | totalspeed 2 s; field/buff 6 s | 3: pfx_howlingwind | 2.33 |
| basic | `aetherialcorruption_firepincer` | melee (charge) | 2.75 | — m/s · r 0.5 | 2 | `aetherialcorruption_attack_c01_fire` 46f · rel f16 (0.53 s) | defensiveability 3 s; field/buff 4 s | 13: pfx_molotov_impact02, pfx_zombiemutant_aethersmash_warmup01 | 2.31 |
| initial | `aetherialcorruption_flameskin` | buff (toggled) | aura | — m/s · r 0.5 | 2 | applied at spawn (initial skill); no cast clip | field/buff 4 s | 5: pfx_molotov_impact02 | 2.31 |
| basic | `aetherialcorruption_aetherslam` | melee (charge) | 2.65–2.99 | — | — | `aetherialcorruption_attack_a01` 46f · rel f16 (0.53 s) | — | 9: pfx_zombiemutant_aethersmash_warmup01, pfx_zombiemutant_aethersmash_warmup02 | 2.19 |
| basic | `dralgar_aetherslam` | melee (charge) | 3.01 | — | — | `aetherialcorruption_attack_a01` 46f · rel f16 (0.53 s) | — | 9: pfx_zombiemutant_aethersmash_warmup01, pfx_zombiemutant_aethersmash_warmup02 | 1 |

*18 further abilities (hero/boss-only or < 0.25 expected bodies) are in `roster.json` → `types[0].abilities`.*

### 2. `wraith` — Wraith · 15.52 bodies (19.4 % cum.)

- **Lead record:** `records/creatures/enemies/wraith_a01.dbr` (Wraith, trash, GD class Common)
- **Records:** 18 on 11 meshes. Names: Wraith / Spiteful Wraith / Eldritch Spirit / Eldritch Spirit ~ Haunt …
- **Role mix (bodies):** trash 11.92, champion-hero 3.4, nemesis 0.2 · **family:** Undead, Eldritch
- **Meshes (bodies):** `wraith01a` 5.7, `wraith_eldritch01a` 4.01, `wraith01b` 1.33, `wraith_eldritch01b_fire01` 0.88, `wraith01b_vitality` 0.77, `wraith01b_deathly` 0.63 …
- **Anim table(s):** `anm_eldritchwraith`, `anm_wraith` · style prefix `unarmed`
- **Size:** actorRadius 0.35 m · scale 1–1.32 · radius×scale 0.35–0.46 m · actorHeight 2 (template default; not a modelled height) · lead mesh bind-pose AABB height 4.41 *mesh units, Lap F caveat* *(DATAMINED)*
- **Locomotion:** characterRunSpeed 0.7–1 → **2.25–3.21 m/s** (INFERRED, × K4-0) · walkSpeed 1
- **Attack style:** melee 49% · aura 19% · aoe 14% · projectile 12% *(INFERRED)* · weapon: unarmed
- **Core clips (lead):** idle `wraith_combatidle_a01` 101f · run `wraith_run_a01` 61f · attack ×3: `wraith_attack_a01` 48f (hit f19), `wraith_attack_b01` 44f (hit f21), `wraith_attack_c01` 37f (hit f14) · spawn `wraith_spawn_a01` 27f · take_hit `wraith_stun_a01` 81f · die: `wraith_death_a01` 45f
- **Spawn:** ring 14.03 · p05 1.49 · waves 151 (8.5), 153 (0.3), 155 (4.7), 156 (0.2), 157 (0.1), 158 (1.5), 160 (0.2)
  - p05 emergence: Sulvar the Endless Hungerer ~ Vampiric: `wraith_spawn_a01` 27f → **0.87 s** (PACK `V38-AM3-28`)
  - p05 emergence: Tulldar Endbringer ~ Celestial: `wraith_spawn_a01` 27f → **0.87 s** (PACK `V38-AM3-29`)
  - p05 emergence: Obliterus: `wraith_spawn_a01` 27f → **0.87 s** (PACK `V38-AM3-26`)
  - p05 emergence: Tildoom ~ Timewarped: `wraith_spawn_a01` 27f → **0.87 s** (PACK `V38-AM3-27`)
  - p05 emergence: Arcanom the Soulthief: `wraith_spawn_a01` 27f → **0.87 s** (PACK `V38-AM3-25`)

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| special1 | `wraith_shadowstrike` | melee (blink strike) | 10.19–10.27 → **0–10.27** [Long] | — | — | `wraith_attack_b01_vitality` 44f · rel f21 (0.7 s) | runspeed 3 s | 7: pfx_ghost_shadowstrike_impact, pfx_ghost_shadowstrike_cast | 10.5 |
| dying | `wraith_eruptionofdespair` | aura | on death | — | 6 | fires at death (death clip) | field/buff 6 s | 6: pfx_wraith_eruptiondespair_other, pfx_ghostlynova_green | 4.72 |
| special1 | `wraith_soulsiphon` | aura | 2.52 → **0–2.52** [Medium] | — | 7 | `wraith_attack_c01` 37f · rel f14 (0.47 s) *inf* | field/buff 3 s | 6: pfx_soulsiphonblue_buff_01, pfx_soulsiphonblue_02 | 4.69 |
| special2 | `wraith_illomen` | buff | 2.52 | — | — | `wraith_attack_c01` 37f · rel f14 (0.47 s) *inf* | lifeleach 1 s; field/buff 6 s | 3: pfx_illomenred_buff_01 | 4.1 |
| special1 | `eldritchwraith_shadowstrike` | melee (blink strike) | 10.19–10.24 → **5.69–10.24** [Long] | — | — | `wraith_attack_b01_vitality` 44f · rel f21 (0.7 s) | fire 3 s; runspeed 3 s | 7: pfx_ghost_shadowstrike_impact, pfx_ghost_shadowstrike_cast | 4.01 |
| dying | `eldritchwraith_eruptionofflame` | aura | on death | — | 6 | fires at death (death clip) | field/buff 6 s | 6: pfx_wraith_eruptionflame, pfx_ghostlynova_orange | 2.63 |
| special2 | `eldritchwraith_burningnova` | aoe | 2.49–2.52 → **0–2.52** [Short] | — | 4 | `wraith_attack_c01` 37f · rel f14 (0.47 s) *ref unbound* | fire 3 s; lifeleach 2 s; manaleach 2 s | 3: pfx_arcaneblast_large_03 | 2.63 |
| special2 | `wraith_leechnova` | aoe | 2.49 → **0–2.49** [Short] | — | 4 | `wraith_attack_c01` 37f · rel f14 (0.47 s) *inf* | lifeleach 2 s; manaleach 2 s | 3: pfx_generic_novaspectral_01 | 2.47 |
| special3 | `wraith_dreadaura` | aura | 2.49 → **0–2.49** [Short] | — | 6 | `wraith_attack_c01` 37f · rel f14 (0.47 s) *inf* | field/buff 6 s | 3: pfx_wraith_dreadaura_self | 2.47 |
| special3 | `eldritchwraith_burningpresence` | aura | 2.49 → **0–2.49** [Short] | — | 5 | `wraith_attack_c01` 37f · rel f14 (0.47 s) *inf* | field/buff 6 s | 3: pfx_wraith_burningaura | 1.75 |
| special3 | `wraith_despairaura` | aura | 2.52 → **0–2.52** [Short] | — | 6 | `wraith_attack_c01` 37f · rel f14 (0.47 s) *inf* | field/buff 6 s | 3: pfx_wraith_despairaura_self | 1.36 |
| basic | `wraith_sappingorbs` | projectile (burst) | 16.27 | 20 m/s · r 0.1 | 1.5 | `wraith_attack_c01` 37f · rel f14 (0.47 s) *inf* | — | 8: pfx_arcanecast_02, pfx_necroticmissile_flight | 1.33 |

*25 further abilities (hero/boss-only or < 0.25 expected bodies) are in `roster.json` → `types[1].abilities`.*

### 3. `devourer` — Chthonian Hungerer · 13.02 bodies (26.9 % cum.)

- **Lead record:** `records/creatures/enemies/chthoniandevourer_a01.dbr` (Chthonian Hungerer, trash, GD class Common)
- **Records:** 11 on 4 meshes. Names: Chthonian Hungerer / Chthonian Devourer / Chthonian Gorger / Narl'Sarroth …
- **Role mix (bodies):** trash 12.64, champion-hero 0.38 · **family:** Chthonic
- **Meshes (bodies):** `chthoniandevourer01a` 12.82, `chthoniandevourer01a_poison` 0.12, `chthoniandevourer01a_fire` 0.04, `chthoniandevourer01a_lightning` 0.04
- **Anim table(s):** `anm_chthonian_devourer` · style prefix `unarmed`
- **Size:** actorRadius 0.36–0.5 m · scale 0.9–1.6 · radius×scale 0.32–0.8 m · actorHeight 2 (template default; not a modelled height) · lead mesh bind-pose AABB height 2.1 *mesh units, Lap F caveat* *(DATAMINED)*
- **Locomotion:** characterRunSpeed 1–1.3 → **3.21–4.17 m/s** (INFERRED, × K4-0) · walkSpeed 1.15
- **Attack style:** melee 72% · aoe 26% *(INFERRED)* · weapon: unarmed
- **Core clips (lead):** idle `devourer_combatidle_a01` 21f · run `devourer_run_a01` 31f · attack ×2: `devourer_attack_a01` 25f (hit f11), `devourer_attack_b01` 24f (hit f12) · spawn `devourer_spawn_a01` 27f · take_hit `devourer_gethit_a01` 16f · die: `devourer_death_a01` 27f
- **Spawn:** ring 13.02 · p05 0 · waves 153 (0.2), 157 (0.7), 158 (12.2)
- **Summons:** `chthoniandevourer_a01_summon` (limit 8, burst 4, ttl 30 s; granted)

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| special1 | `chthoniandevourer_chomp` | melee | 2.41–2.54 → **0–2.54** [Medium] | — | — | `devourer_attack_a01` 25f ×0.85 · rel f11 (0.37 s) | — | 3: pfx_chaosstrike_impact | 5.84 |
| special1 | `chthoniandevourer_megachomp` | melee | 2.52–2.66 → **0–2.66** [Short] | — | — | `devourer_attack_a01` 25f ×0.85 · rel f11 (0.37 s) | — | 3: pfx_chaosstrike_impact | 3.66 |
| special1 | `chthoniandevourer_vomit` | aoe (wave / cone) | 2.52 → **0–2.52** [Short] | — | wave 3 long, 1→1 wide | `devourer_attackspit_a01` 51f · rel f37 (1.23 s) | poison 3 s | 1: zombiebarf_sprayfx (clip) | 3.28 |

*24 further abilities (hero/boss-only or < 0.25 expected bodies) are in `roster.json` → `types[2].abilities`.*

### 4. `crabmonstrosity` — Ugdenbog Crab · 11.51 bodies (33.6 % cum.)

- **Lead record:** `records/creatures/enemies/swampcrab_a01.dbr` (Ugdenbog Crab, trash, GD class Common)
- **Records:** 23 on 15 meshes. Names: Ugdenbog Crab / Ugdenbog Spikeshell / Ugdenbog Stoneshell / Sparkmucker ~ Thundering …
- **Role mix (bodies):** trash 7.99, champion-hero 3.28, boss 0.25 · **family:** Beast, Undead + Beast
- **Meshes (bodies):** `crabmonstrosity01a` 4.87, `crabmonstrosity01b` 3.35, `crabmonstrosity01e` 0.48, `crabmonstrosity01d` 0.38, `crabmonstrositysprings01a_lightning` 0.25, `crabmonstrositysprings01a_cold` 0.25 …
- **Anim table(s):** `anm_swampcrab` · style prefix `unarmed`
- **Size:** actorRadius 0.4–0.6 m · scale 1–2.8 · radius×scale 0.5–1.12 m · actorHeight 1.5 (template default; not a modelled height) · lead mesh bind-pose AABB height 2.16 *mesh units, Lap F caveat* *(DATAMINED)*
- **Locomotion:** characterRunSpeed 1 → **3.21 m/s** (INFERRED, × K4-0) · walkSpeed 0.7
- **Attack style:** melee 71% · projectile 15% · aoe 12% · summons on 34% of bodies *(INFERRED)* · weapon: unarmed
- **Core clips (lead):** idle `crabmonstrosity_combatidle_a01` 21f · run `crabmonstrosity_run_a01` 16f · walk `crabmonstrosity_walk_a01` 31f · attack ×2: `crabmonstrosity_attack_a01` 29f (hit f21), `crabmonstrosity_attack_c01` 27f (hit f19) · spawn `crabmonstrosity_spawn_a01` 54f · take_hit `crabmonstrosity_gethit_a01` 14f · die: `crabmonstrosity_death_a01` 21f
- **Spawn:** ring 11.51 · p05 0 · waves 152 (3.2), 153 (0.1), 157 (0.1), 158 (8)
- **Summons:** `swampcrab_a00_summon` (limit 8, burst 4, ttl 30 s; granted); `springscrab_a00_summon` (limit 8, burst 4, ttl 30 s; granted); `trap_lightningspike_hero_a01` (limit 6, burst 1, ttl 24–27 s; granted); `trap_icespike_hero_a01` (limit 6, burst 1, ttl 12–15 s; granted); `swampcrab_b01_summon` (limit 4, burst 1–2, ttl 25 s; granted) …

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| special1 | `swampcrab_clawslam` | melee | 2.59–3.09 → **0–3.09** [Short] | — | — | `crabmonstrosity_attack_d01` 21f · rel f12 (0.4 s) | — | 3: pfx_bloodstrike | 9.27 |
| special2 | `ghostcrab_waterbreath` | aoe (wave / cone) | 2.69–3.09 → **0–3.09** [Short] | — | wave 3.5 long, 1→1 wide | `crabmonstrosity_breathice_b01` 50f · rel f14 (0.47 s) | cold 6 s | 1: frostbreathfx (clip) | 4.63 |
| special3 | `swampcrab_waterspoutstrike` | melee | 2.69–3.09 → **0–3.09** [Short] | — | — | `crabmonstrosity_attack_b01` 35f ×0.85 · rel f12 (0.4 s) | — | 4: pfx_bloodstrike | 4.27 |
| tree_attack | `swampcrab_waterspout` | projectile (lobbed area) | 6.19–6.59 | — m/s · r 0.5 | 3 | `crabmonstrosity_attack_c01` 27f · rel f19 (0.63 s) *inf* | field/buff 5 s | 4: pfx_waterspout | 4.27 |
| special2 | `swampcrab_shellspin` | melee | 2.9 → **0–2.9** [Short] | — | — | `crabmonstrosity_attack_b01` 35f ×0.85 · rel f12 (0.4 s) | defensivereduction 3 s | 4: pfx_bloodstrike | 1.65 |
| special1 | `ghostcrab_clawslam` | melee | 3.09 → **0–3.09** [Short] | — | — | `crabmonstrosity_attack_d01` 21f · rel f12 (0.4 s) | cold 2 s | 3: pfx_chillingtouch_impact | 1 |
| special1 | `springscrab_clawslam` | melee | 3.09 → **0–3.09** [Short] | — | — | `crabmonstrosity_attack_d01` 21f · rel f12 (0.4 s) | — | 3: pfx_bloodstrike | 0.99 |
| special2 | `springscrab_shellspin` | melee | 3.09 → **0–3.09** [Short] | — | — | `crabmonstrosity_attack_b01` 35f ×0.85 · rel f12 (0.4 s) | defensivereduction 3 s | 4: pfx_bloodstrike | 0.99 |
| dying | `ghostcrab_ectoplasmpool` | projectile (lobbed area) | on death | — m/s · r 0.5 | 2.5 | fires at death (death clip) | totalspeed 1 s; field/buff 6 s | 4: pfx_ectoplasmpool | 0.8 |
| special2 | `ghostcrab_freezingspin` | projectile (ring / nova) | 10.84 → **5.34–10.84** [Medium] | 8 m/s · r 0.5 | 2 | `crabmonstrosity_attack_b01_ice` 35f ×0.85 · rel f12 (0.4 s) | cold 2 s; totalspeed 2 s | 10: pfx_icespikesground_impact01, pfx_frostorb_impact01 | 0.8 |
| special4 | `carraxus_poisonbreath` | aoe (wave / cone) | 2.81–3.21 → **0–3.21** [Short] | — | wave 5 long, 1.5→1.5 wide | `crabmonstrosity_breathpoison_b01` 50f · rel f14 (0.47 s) | poison 3 s | 1: zombiebarf_sprayfx (clip) | 0.48 |
| dying | `corrupted_aetherconflagration` | projectile (lobbed area) | on death | — m/s · r 0.5 | 3 | fires at death (death clip) | field/buff 6 s | 5: pfx_aetherring_warden_01 | 0.4 |

*31 further abilities (hero/boss-only or < 0.25 expected bodies) are in `roster.json` → `types[3].abilities`.*

### 5. `golemswamp_phase01` — Ugdenbog Golem · 9.03 bodies (38.9 % cum.)

- **Lead record:** `records/creatures/enemies/swampgolem_a01.dbr` (Ugdenbog Golem, trash, GD class Champion)
- **Records:** 14 on 7 meshes. Names: Ugdenbog Golem / Ugdenbog Mossflinger / Jormundur ~ Diseased / Ferrosius ~ Swift …
- **Role mix (bodies):** trash 5.62, champion-hero 3.41 · **family:** Plant + Eldritch
- **Meshes (bodies):** `golemswamp01a_phase01` 5.14, `golemswamp01d_phase01` 0.77, `golemswamp01g_phase02` 0.77, `golemswamp01f_phase01` 0.64, `golemswamp01e_phase01` 0.63, `golemswamp01a_phase01_infernal` 0.6 …
- **Anim table(s):** `anm_swampgolem_phase01` · style prefix `unarmed`
- **Size:** actorRadius 0.5–0.75 m · scale 1–1.32 · radius×scale 0.5–0.99 m · actorHeight 2 (template default; not a modelled height) · lead mesh bind-pose AABB height 6.3 *mesh units, Lap F caveat* *(DATAMINED)*
- **Locomotion:** characterRunSpeed 1.2–1.55 → **3.85–4.97 m/s** (INFERRED, × K4-0) · walkSpeed 1
- **Attack style:** aoe 66% · melee 17% · projectile 17% *(INFERRED)* · weapon: unarmed
- **Core clips (lead):** idle `golemswamp_phase01_combatidle_a01` 116f · run `golemswamp_phase01_walk_a01` 91f · attack ×2: `golemswamp_phase01_attack_a01` 51f (hit f34), `golemswamp_phase01_attack_b01` 51f (hit f26) · spawn `golemswamp_phase01_appearance_a01` 108f · take_hit `golemswamp_phase01_gethit_a01` 24f · die: `golemswamp_phase01_death_a01` 60f
- **Spawn:** ring 5.91 · p05 3.12 · waves 151 (4.6), 153 (1.8), 156 (1.2), 157 (1.4)
  - p05 emergence: Ugdenbog Golem: `golemswamp_phase01_appearance_a01` 108f → **3.57 s** (PACK `V38-AM3-31`)
- **Summons:** `livingplant_a01_summon` (limit 3, burst 1–3, ttl 20 s; granted)

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| special1 | `swampgolem_doubleswipe` | aoe (wave / cone) | 10.34–10.83 → **0–5.33** [Short] | — | wave 8 long, 3→5 wide | `golemswamp_phase01_attackspecial_a01` 81f ×0.85 · rel f25 (0.83 s) | attackspeed 3 s; poison 2 s | 2: poison_cast_fx (clip), acidarc_fx01 (clip) | 9.03 |
| basic | `swampgolem_stonethrash` | melee (charge) | 2.78–3.08 | — | — | `golemswamp_phase01_attack_a01` 51f · rel f34 (1.13 s) *ref unbound* | — | 4: pfx_clawslash_electrical_charge01fx, pfx_clawslash_electrical_charge02fx | 4.84 |
| special2 | `swampgolem_vinenova` | projectile (ring / nova) | 10.8–10.83 → **0–10.83** [Medium] | 11 m/s · r 0.5 | 2 | `golemswamp_phase01_attackrangedcharged_a01` 86f · rel f50 (1.67 s) | poison 2 s; totalspeed 2 s | 10: pfx_vinesground_flight01b, pfx_groble_poisonorb_impact01 | 4.06 |
| dying | `infernal_embernova` | projectile (ring / nova) | on death | 15 m/s · r 0.1 | 1 | fires at death (death clip) | defensiveability 2 s | 8: pfx_infernalember_flight01, pfx_infernalember_impact01 | 1.2 |
| special2 | `swampgolem_vineslam` | aoe (wave / cone) | 10.53 → **0–9.03** [Medium] | — | wave 15 long, 2→4 wide | `golemswamp_phase01_attackranged_a01` 86f · rel f50 (1.67 s) | poison 2 s; totalspeed 2 s | 8: pfx_vinesground_flight01b, pfx_groble_poisonorb_impact01 | 0.95 |
| initial | `voidtouched_chaosform` | aura (toggled) | aura | — | 5 · aura 5 | applied at spawn (initial skill); no cast clip | — | 3: pfx_voidtouched_chaosaura_self01 | 0.77 |
| special4 | `voidtouched_chaoschainlightning` | projectile (chain) | 16.83 → **0–10.33** [Medium] | — | — | `golemswamp_phase01_throw_a01` 61f · rel f26 (0.87 s) *inf* | — | 1: deathbolt1_chain | 0.77 |
| special5 | `voidtouched_chaosstrike` | melee (blink strike) | 3.08 → **0–3.08** [Long] | — | — | `golemswamp_phase01_attack_a01` 51f · rel f34 (1.13 s) *inf* | totalspeed 2 s | 3: pfx_chaosblink | 0.77 |
| initial | `diseased_diseasecloud` | aura (toggled) | aura | — | 4 · aura 4 | applied at spawn (initial skill); no cast clip | poison 2 s | 3: pfx_zombie_poisonaura01 | 0.64 |
| special4 | `diseased_gascloud` | projectile (lobbed area) | 16.83 | — m/s · r 0.5 | 3 | `golemswamp_phase01_throw_a01` 61f · rel f26 (0.87 s) *inf* | offensiveability 2 s; poison 2 s; field/buff 10 s | 4: pfx_poisoncloud_01 | 0.64 |
| initial | `infernal_emberbuff` | buff (toggled) | aura | 15 m/s · r 0.1 | 1 | applied at spawn (initial skill); no cast clip | defensiveability 2 s | 8: pfx_infernalember_flight01, pfx_infernalember_impact01 | 0.6 |
| tree_attack | `infernal_emberburstproc` | projectile (burst) | 16.83 | 15 m/s · r 0.1 | 1 | `golemswamp_phase01_throw_a01` 61f · rel f26 (0.87 s) *inf* | defensiveability 2 s | 8: pfx_infernalember_flight01, pfx_infernalember_impact01 | 0.6 |

*5 further abilities (hero/boss-only or < 0.25 expected bodies) are in `roster.json` → `types[4].abilities`.*

### 6. `hero01_unarmed` — Apparition · 7.91 bodies (43.5 % cum.)

- **Lead record:** `records/creatures/enemies/ghost_a02.dbr` (Apparition, trash, GD class Common)
- **Records:** 19 on 14 meshes. Names: Apparition / Possessed Armor / The Sentinel / Eldritch Armor …
- **Role mix (bodies):** trash 4.33, boss 2.26, nemesis 0.8, champion-hero 0.52 · **family:** Magical + Eldritch, Undead, Human, Eldritch, Aetherial + Human, Human + Eldritch, Bloodsworn + Human, Human + Aetherial
- **Meshes (bodies):** `ghost_m_a01` 1.63, `eldritcharmor01a` 1.38, `humanmale01a` 1, `eldritcharmor02a_lightning` 0.81, `humanmale12a` 0.58, `eldritcharmor02a_fire` 0.51 …
- **Anim table(s):** `anm_eldritcharmor`, `anm_eldritcharmor_bossfire`, `anm_ghost_male`, `anm_human` (+4) · style prefix `unarmed`
- **Size:** actorRadius 0.35–0.7 m · scale 1–1.9 · radius×scale 0.35–0.98 m · actorHeight 2 (template default; not a modelled height) · lead mesh bind-pose AABB height 0.42 *mesh units, Lap F caveat* *(DATAMINED)*
- **Locomotion:** characterRunSpeed 0.6–1.2 → **1.93–3.85 m/s** (INFERRED, × K4-0) · walkSpeed 0.7, 1
- **Attack style:** projectile 40% · aoe 39% *(INFERRED)* · weapon: unarmed
- **Core clips (lead):** idle `hero01_sword1h_idlecombat` 61f · run `hero01_unarmed_run` 25f · walk `hero01_walk_a01` 31f · attack ×2: `hero01_sword1h_attack_a01` 19f (hit f8), `hero01_sword1h_attack_b01` 19f (hit f8) · spawn `ghost_m_spawn_b01` 14f · take_hit `hero01_unarmed_gethit_a01` 21f · die: `hero01_death_a` 91f
- **Spawn:** ring 7.91 · p05 0 · waves 151 (1.6), 153 (0.5), 154 (3.5), 155 (0.5), 159 (1), 160 (0.8)
- **Summons:** `witchgodguardian_sentinel_crystal` (limit 5, burst 1, ttl 25 s; granted); `mindreaper_summon` (limit 2–4, burst 2–4, ttl 9–15 s; granted); `loghorrean_void` (limit 6, burst 1, ttl 9–12 s; granted); `chthonianminion_b01_summon` (limit 1–6, burst 1–2, ttl 60 s; granted); `chthonicshard_zap_b01_summon` (limit 4, burst 2–4, ttl 30 s; granted) …

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| special1 | `eldritcharmor_firecleave` | aoe (wave / cone) | 2.56 → **0–2.56** [Short] | — | wave 3 long, 3→4 wide | `hero01_sword1h_skill_firearc01` 29f · rel f14 (0.47 s) | — | 5: pfx_firestrike | 1.38 |
| special2 | `eldritcharmor_fireorb` | projectile | 16.31 → **8.81–16.31** [Long] | 16 m/s · r 0.3 | 1.5 | `hero01_sword1h_spellattack_b01` 19f · rel f10 (0.33 s) *inf* | — | 6: pfx_groble_fireball_huge_flight01, pfx_groble_fireball_huge_impact02 | 1.38 |
| chain_initial | `aetherialvanguard_arcanemissilenova` | projectile (ring / nova) | 16.38 | 14 m/s · r 0.3 | 0.5 | `hero01_unarmed_spell_nova_a01` 19f · rel f11 (0.37 s) | — | 9: pfx_arcanecast_02, pfx_arcanemissile_flight_01 | 1 |
| dying | `witchgodguardian_sentinel_deatheldritchblast` | aoe | on death | — | 10 | fires at death (death clip) | — | 3: abomination_vileeruption01 | 1 |
| special1 | `witchgodguardian_sentinel_eldritchbreath` | aoe (wave / cone) | 6.57 → **0–6.57** [Short] | — | wave 13 long, 2.5→2.5 wide | `hero01_sword1h_skill_eldritchbreath_a01` 41f · rel f21 (0.7 s) | ttl 15–35 s | 1: eldritchbreathfx01 (clip) | 1 |
| special2 | `witchgodguardian_sentinel_earthring` | projectile (ring / nova) | 16.82 → **0–10.32** [Medium] | 12 m/s · r 0.5 | 0.1 | `hero01_sword1h_attackspecial_groundstompfx_a01` 23f ×0.4 · rel f16 (0.53 s) | damagemult 3 s; ttl 15–35 s | 9: pfx_bloodstrike | 1 |
| special3 | `witchgodguardian_sentinel_eldritchrain` | aura (drop / mortar) | 19.82 | 15 m/s · r 0.5 | 1.8/15 | `hero01_sword1h_spell_aoe_a01` 21f · rel f10 (0.33 s) | field/buff 16 s; ttl 15–35 s | 7: pfx_firestorm_eldritch_flight01, pfx_firestorm_eldritch_impact01 | 1 |
| special5 | `witchgodguardian_sentinel_eldritchblast` | aoe | 3.07 → **0–3.07** [Medium] | — | 10 | `hero01_sword1h_spell_eldritchblast_long_a01` 95f ×1.5 · rel f86 (2.87 s) | poison 5 s | 4: abomination_vileeruption01 | 1 |
| basic | `eldritcharmor_lightningorb_strong` | projectile | 16.36 | 16 m/s · r 0.1 | 1.5 | `hero01_sword1h_spellattack_b01` 19f · rel f10 (0.33 s) *inf* | lightning 3 s | 6: pfx_lightningorb01_lg_flight, pfx_lightningorb01_lg_impact | 0.81 |
| special1 | `eldritcharmor_lightningorbburst` | projectile (burst) | 16.36 → **4.86–14.86** [Medium] | 16 m/s · r 0.1 | 1.5 | `hero01_sword1h_spellattack_b01` 19f · rel f10 (0.33 s) *inf* | — | 6: pfx_lightningorb01_lg_flight, pfx_lightningorb01_lg_impact | 0.81 |
| special2 | `eldritcharmor_rainoflightning` | aura (drop / mortar) | 19.36 | 30 m/s · r 0.5 | 2.2/8 | `hero01_sword1h_spellbuffself` 19f · rel f11 (0.37 s) *inf* | field/buff 8 s | 6: pfx_lightningskyshard_flight_01, pfx_lightningorb_impact01 | 0.81 |
| special3 | `eldritcharmor_lightningnet` | buff | 2.61 → **0–2.61** [Long] | — | 3 | `hero01_sword1h_spellbuffself` 19f · rel f11 (0.37 s) *inf* | field/buff 5 s | 3: pfx_lightningnet_02 | 0.81 |

*56 further abilities (hero/boss-only or < 0.25 expected bodies) are in `roster.json` → `types[5].abilities`.*

### 7. `sandlizard` — Moltenclaw · 7.46 bodies (47.8 % cum.)

- **Lead record:** `records/creatures/enemies/sandlizard_volcanic_a01.dbr` (Moltenclaw, trash, GD class Common)
- **Records:** 12 on 4 meshes. Names: Moltenclaw / Sandclaw / Riftclaw / Riftclaw ~ Flayer …
- **Role mix (bodies):** trash 7.46 · **family:** Beast, Beast + Eldritch
- **Meshes (bodies):** `eldritchlizard01b` 3.16, `sandlizard01a` 1.94, `eldritchlizard01a` 1.94, `sandlizard01b` 0.41
- **Anim table(s):** `anm_sandlizard` · style prefix `unarmed`
- **Size:** actorRadius 0.25–0.75 m · scale 1–1.25 · radius×scale 0.25–0.94 m · actorHeight 2 (template default; not a modelled height) · lead mesh bind-pose AABB height 2.7 *mesh units, Lap F caveat* *(DATAMINED)*
- **Locomotion:** characterRunSpeed 0.9–1 → **2.89–3.21 m/s** (INFERRED, × K4-0) · walkSpeed 1.2
- **Attack style:** melee 84% · aoe 16% *(INFERRED)* · weapon: unarmed
- **Core clips (lead):** idle `sandlizard_combatidle_a01` 46f · run `sandlizard_run_a01` 25f · walk `sandlizard_walk_a01` 41f · attack ×2: `sandlizard_attack_a01` 31f (hit f14), `sandlizard_attack_b01` 25f (hit f12) · spawn `sandlizard_spawn_a01` 51f · take_hit `wendigo_gethit_a01` 14f · die: `sandlizard_death_a01` 57f
- **Spawn:** ring 7.46 · p05 0 · waves 157 (0.4), 158 (7)

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| special2 | `sandlizard_leap` | aoe (leap) | 33.7 → **10.2–19.2** [Medium] | — | 2.8 · wave 15 long, —→— wide | `sandlizard_attackspecial_c01_leap` 26f · rel f19 (0.63 s) | bleeding 2 s; runspeed 0.5–1.6 s | 3: blitz1_impact | 1.6 |
| special1 | `eldritchlizard_doubleswipe` | melee | 2.84–2.95 → **0–2.95** [Short] | — | — | `sandlizard_attackspecial_b01` 37f · rel f8 (0.27 s) | — | 4: pfx_elementalstrike_impact | 1.59 |
| special1 | `volcaniclizard_firedoubleswipe` | melee | 2.84–2.95 → **0–2.95** [Short] | — | — | `sandlizard_attackspecial_b01_fire` 37f · rel f8 (0.27 s) | — | 4: pfx_firestrike | 1.46 |
| special1 | `sandlizard_doubleswipe` | melee | 2.34–2.95 → **0–2.95** [Short] | — | — | `sandlizard_attackspecial_b01` 37f · rel f8 (0.27 s) | — | 4: pfx_bloodstrike | 1.46 |
| special1 | `eldritchlizard_legclaw` | melee | 2.95–3.02 → **0–3.02** [Short] | — | — | `sandlizard_attackspecial_a01` 36f · rel f22 (0.73 s) | — | 8: pfx_elementalstrike_impact | 1.16 |
| special2 | `sandlizard_legclaw` | melee | 2.95–3.02 → **0–3.02** [Short] | — | — | `sandlizard_attackspecial_a01` 36f · rel f22 (0.73 s) | bleeding 3 s | 4: pfx_bloodstrike | 0.9 |
| special1 | `volcaniclizard_fireclaw` | melee | 2.95–3.02 → **0–3.02** [Short] | — | — | `sandlizard_attackspecial_a01_fire` 36f · rel f22 (0.73 s) | defensivereduction 3 s; fire 5 s | 4: pfx_bloodstrike | 0.89 |
| initial | `eldritchlizard_raptoraura` | aura (toggled) | aura | — | 10 · aura 10 | applied at spawn (initial skill); no cast clip | — | 5: pfx_buffaura_purple_self, pfx_buffaura_purple_other | 0.54 |
| special2 | `eldritchlizard_poisonbreath` | aoe (wave / cone) | 10.77 → **0–6.27** [Medium] | — m/s · r 0.5 | 2 · wave 4 long, 2→2 wide | `sandlizard_attackspecial_breath_a01` 83f · rel f16 (0.53 s) | poison 5 s; poison 2 s; field/buff 8 s | 5: pfx_poisonfield_small_01 | 0.54 |
| initial | `sandlizard_raptoraura` | aura (toggled) | aura | — | 10 · aura 10 | applied at spawn (initial skill); no cast clip | — | 5: pfx_buffaura_green_self, pfx_buffaura_green_other | 0.41 |
| special1 | `sandlizard_shreddingdoubleswipe` | melee | 3.02 → **0–3.02** [Short] | — | — | `sandlizard_attack_a01` 31f · rel f14 (0.47 s) *ref unbound* | bleeding 5 s; defensiveability 5 s | 3: pfx_bloodstrike | 0.41 |
| special3 | `sandlizard_charge` | melee (charge) | 3.02 → **8.27–3.02** [Long] | — | — | `sandlizard_attack_a01` 31f · rel f14 (0.47 s) *ref unbound* | bleeding 2 s; runspeed 0.5–1.6 s | 5: pfx_bloodstrike, blitz1_warmuploop | 0.41 |

*3 further abilities (hero/boss-only or < 0.25 expected bodies) are in `roster.json` → `types[6].abilities`.*

### 8. `wendigo` — Wendigo · 6.04 bodies (51.3 % cum.)

- **Lead record:** `records/creatures/enemies/wendigo_a01.dbr` (Wendigo, trash, GD class Common)
- **Records:** 16 on 6 meshes. Names: Wendigo / Reaper of the Lost / Wendigo ~ Marroweater / Wendigo ~ Flayer …
- **Role mix (bodies):** trash 3.32, champion-hero 1.77, nemesis 0.7, boss 0.25 · **family:** Undead + Beast
- **Meshes (bodies):** `wendigo01b` 2.45, `wendigo01a` 2.01, `wendigo02a_golden` 0.7, `wendigo01b_arcane` 0.34, `wendigo01b_infernal` 0.3, `wendigo01c` 0.25
- **Anim table(s):** `anm_wendigo` · style prefix `unarmed`
- **Size:** actorRadius 0.7–0.75 m · scale 1–1.4 · radius×scale 0.75–0.98 m · actorHeight 2 (template default; not a modelled height) · lead mesh bind-pose AABB height 4.7 *mesh units, Lap F caveat* *(DATAMINED)*
- **Locomotion:** characterRunSpeed 0.9–1 → **2.89–3.21 m/s** (INFERRED, × K4-0) · walkSpeed 1, 1.2
- **Attack style:** melee 55% · projectile 26% · aura 17% *(INFERRED)* · weapon: unarmed
- **Core clips (lead):** idle `wendigo_idlecombat_a01` 61f · run `wendigo_run_a01` 16f · walk `wendigo_walk_a01` 38f · attack ×2: `wendigo_attack_b01` 25f (hit f11), `wendigo_attack_a01` 31f (hit f15) · spawn `wendigo_spawn_a01` 15f · take_hit `wendigo_gethit_a01` 14f · die: `wendigo_death_a01` 46f
- **Spawn:** ring 6.04 · p05 0 · waves 151 (1.5), 153 (3.5), 157 (0.1), 159 (0.2), 160 (0.7)
- **Summons:** `wraith_b01_summon` (limit 12, burst 2, ttl 45 s; granted); `wraith_a01_summon` (limit 3–6, burst 2–4, ttl 30 s; granted)

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| special2 | `wendigo_tripleswipe` | melee | 2.93–3 → **0–3** [Short] | — | — | `wendigo_attack_c01` 58f · rel f11 (0.37 s) | bleeding 2 s | 3: pfx_bloodstrike | 3.08 |
| special3 | `wraith_soulsiphon` | aura | 2.93–3 → **0–3** [Medium] | — | 7 | `wendigo_attackspecial_howl_a01` 31f · rel f12 (0.4 s) *inf* | field/buff 3 s | 6: pfx_soulsiphonblue_buff_01, pfx_soulsiphonblue_02 | 2.72 |
| special2 | `wendigo_leechingslam` | melee | 2.93–3 → **0–3** [Short] | — | — | `wendigo_attackspecial_doubleslash_a01` 27f · rel f11 (0.37 s) | — | 4: pfx_bloodstrike | 2.46 |
| dying | `wendigo_crimsonpool` | projectile (lobbed area) | on death | — m/s · r 0.5 | 4 | fires at death (death clip) | bleeding 1 s; offensiveability 2 s; field/buff 8 s | 5: pfx_crimsonpool_wendigo | 2.09 |
| special2 | `wendigo_ram` | melee | 2.84–2.95 → **0–2.95** [Short] | — m/s · r 0.5 | 2.4 | `wendigo_attackspecial_ram_a01` 26f · rel f10 (0.33 s) | life 2 s; bleeding 1 s; offensivereduction 2 s; field/buff 5 s | 8: pfx_crimsonpool_ghoul, pfx_bloodstrike | 2.01 |
| tree_attack | `wendigocannibal_bloodpool` | projectile (lobbed area) | 6.34–6.45 | — m/s · r 0.5 | 2.4 | `wendigo_attack_a01` 31f · rel f15 (0.5 s) *inf* | bleeding 1 s; offensivereduction 2 s; field/buff 5 s | 5: pfx_crimsonpool_ghoul | 2.01 |
| special1 | `wendigo_tearflesh` | melee | 6.57 → **0–5.32** [Short] | — | — | `wendigo_attackspecial_tripleswipesunder` 58f ×0.6 · rel f11 (0.37 s) | damagemult 1 s | 5: pfx_bloodstrike | 0.7 |
| special3 | `wendigo_necroticnovainverse` | projectile (ring / nova) | 33.82 → **0–5.32** [Short] | 9 m/s · r 0.3 | — | `wendigo_attackspecial_howl_a01_double` 31f ×0.6 · rel f12 (0.4 s) | totalspeed 3 s | 7: pfx_ravager_deathorb, pfx_necroticmissile_impact | 0.7 |
| special5 | `wendigo_necroticnovaboomerang` | projectile (ring / nova) | 33.82 | 10 m/s · r 0.3 | — | `wendigo_attackspecial_howl_a01_double` 31f ×0.6 · rel f12 (0.4 s) | totalspeed 3 s | 7: pfx_ravager_deathorb, pfx_necroticmissile_impact | 0.7 |
| tree_attack | `wendigo_wpattack01` | melee | 3.07 | — | — | `wendigo_attackspecial_doubleslash_a01` 27f · rel f11 (0.37 s) | — | 1: dark_cast_fx (clip) | 0.7 |
| tree_attack | `wendigo_wpattack02` | melee | 3.07 | — | — | `wendigo_attack_c01` 58f · rel f11 (0.37 s) | — | 3: pfx_multistrike1_activate | 0.7 |
| tree_attack | `wendigo_wpattack03` | melee | 3.07 | — | — | `wendigo_attackspecial_ram_a01` 26f · rel f10 (0.33 s) | bleeding 2 s; defensiveability 3 s | 3: pfx_mortalstrike_impact | 0.7 |

*19 further abilities (hero/boss-only or < 0.25 expected bodies) are in `roster.json` → `types[7].abilities`.*

### 9. `aetherialimp` — Aetherial Scamp · 5.98 bodies (54.8 % cum.)

- **Lead record:** `records/creatures/enemies/aetherialimp_a01.dbr` (Aetherial Scamp, trash, GD class Common)
- **Records:** 7 on 6 meshes. Names: Aetherial Scamp / Aetherial Imp / Brolbos ~ Arctic / Phigillius Stormbile …
- **Role mix (bodies):** trash 4.97, champion-hero 1.01 · **family:** Aetherial
- **Meshes (bodies):** `aetherialimp01a` 4.97, `aetherialimp01a_arctic` 0.2, `aetherialimp01c` 0.2, `aetherialimp01d` 0.2, `aetherialimp01f` 0.2, `aetherialimp01e` 0.2
- **Anim table(s):** `anm_aetherialimp` · style prefix `unarmed`
- **Size:** actorRadius 0.8 m · scale 0.65–0.85 · radius×scale 0.52–0.68 m · actorHeight 2 (template default; not a modelled height) · lead mesh bind-pose AABB height — *mesh units, Lap F caveat* *(DATAMINED)*
- **Locomotion:** characterRunSpeed 1 → **3.21 m/s** (INFERRED, × K4-0) · walkSpeed 0.75, 1
- **Attack style:** melee 91% *(INFERRED)* · weapon: unarmed
- **Core clips (lead):** idle `aetherialimp_combatidle_a01` 61f · run `aetherialimp_run_a01` 25f · walk `aetherialimp_walk_a01` 21f · attack ×2: `aetherialimp_attack_a01` 30f (hit f10), `aetherialimp_attack_b01` 27f (hit f7) · spawn `aetherialimp_spawn_a01` 47f · take_hit `aetherialimp_gethit_a01` 17f · die: `aetherialimp_death_a01` 22f
- **Spawn:** ring 4.97 · p05 1.01 · waves 155 (5), 157 (1)
  - p05 emergence: Brolbos ~ Arctic: `aetherialimp_spawn_a01` 47f → **1.53 s** (PACK `V38-AM3-16`)
  - p05 emergence: Phigillius Stormbile: `aetherialimp_spawn_a01` 47f → **1.53 s** (PACK `V38-AM3-12`)
  - p05 emergence: Phanolg the Iceborn: `aetherialimp_spawn_a01` 47f → **1.53 s** (PACK `V38-AM3-13`)
  - p05 emergence: Ghalbar ~ Regenerator: `aetherialimp_spawn_a01` 47f → **1.53 s** (PACK `V38-AM3-15`)
  - p05 emergence: Wourble ~ Reflective: `aetherialimp_spawn_a01` 47f → **1.53 s** (PACK `V38-AM3-14`)
- **Summons:** `trap_icespike_hero_a01` (limit 6, burst 1, ttl 12–15 s; granted)

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| dying | `aetherialimp_goryeruption` | aoe | on death | — | 2.5 | fires at death (death clip) | — | 3: pfx_goryeruption | 3.27 |
| dying | `aetherialimp_aethereruption` | aoe | on death | — | 2.5 | fires at death (death clip) | offensiveability 3 s | 4: pfx_detonate_aether_01 | 2.71 |
| special1 | `aetherialimp_aetherfirestrike` | melee | 2.66–2.77 → **0–2.77** [Short] | — m/s · r 0.5 | 3 | `aetherialimp_attack_b01_special` 27f · rel f7 (0.23 s) | field/buff 4 s | 9: pfx_aetherfire, pfx_aetherstrike_impact | 2.71 |

*6 further abilities (hero/boss-only or < 0.25 expected bodies) are in `roster.json` → `types[8].abilities`.*

### 10. `carnivorousplant01a_p1` — Carnivorous Plant · 5.87 bodies (58.2 % cum.)

- **Lead record:** `records/creatures/enemies/livingplant_a01.dbr` (Carnivorous Plant, trash, GD class Common)
- **Records:** 1 on 1 meshes. Names: Carnivorous Plant
- **Role mix (bodies):** trash 5.87 · **family:** Plant + Eldritch
- **Meshes (bodies):** `carnivorousplant01a_p2` 5.87
- **Anim table(s):** `anm_carnivorousplant_p2` · style prefix `unarmed`
- **Size:** actorRadius 1.1 m · scale 0.7 · radius×scale 0.77 m · actorHeight 2 (template default; not a modelled height) · lead mesh bind-pose AABB height 14.46 *mesh units, Lap F caveat* *(DATAMINED)*
- **Locomotion:** **stationary** (`ControllerStationaryMonster`, PACK `V38-ST1-1`). It never moves or rotates (`disallowRotation = 1`), and its walk and run slots play the combat idle.
- **Attack style:** melee 50% · projectile 50% *(INFERRED)* · weapon: unarmed
- **Core clips (lead):** idle `carnivorousplant01a_p1_combatidle_a01` 121f · run `carnivorousplant01a_p1_combatidle_a01` 121f · attack ×1: `carnivorousplant01a_p2_attack_a01` 36f (hit f13) · spawn `carnivorousplant01a_p2_spawn_b01` 46f · take_hit `carnivorousplant01a_p1_gethit_a01` 19f · die: `carnivorousplant01a_p1_death_a01` 63f
- **Spawn:** ring 0 · p05 5.87 · waves 151 (2.9), 153 (2.9)
  - p05 emergence: Carnivorous Plant: `carnivorousplant01a_p2_spawn_b01` 46f → **1.5 s** (PACK `V38-AM3-30`)

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| special1 | `livingplant_bite` | melee | 2.86 → **0–2.86** [Short] | — | — | `carnivorousplant01a_p2_attack_b01` 51f · rel f13 (0.43 s) | bleeding 5 s | 3: pfx_bloodstrike | 5.87 |
| special2 | `livingplant_venomousseed` | projectile (drop / mortar) | 33.61 → **3.61–23.11** [Medium] | 30 m/s · r 1 | 1.5/2.5 | `carnivorousplant01a_p2_cast_b01` 44f · rel f19 (0.63 s) | poison 5 s | 7: pfx_acidorbthick01_lg_flight, pfx_acidorb_huge_impact01 | 5.87 |

### 11. `basilisk` — Juvenile Basilisk · 5.78 bodies (61.6 % cum.)

- **Lead record:** `records/creatures/enemies/basilisk_a01.dbr` (Juvenile Basilisk, trash, GD class Common)
- **Records:** 14 on 7 meshes. Names: Juvenile Basilisk / Venomgaze Basilisk / Stonegaze Basilisk / Stone Basilisk …
- **Role mix (bodies):** trash 3.51, champion-hero 1.76, boss 0.51 · **family:** Beast, Magical
- **Meshes (bodies):** `basilisk01a` 3.26, `basilisk01c` 0.76, `basilisk01f` 0.47, `basilisk01d` 0.33, `basilisk01e` 0.33, `basilisk01g` 0.33 …
- **Anim table(s):** `anm_basilisk`, `anm_basilisk_witchritual` · style prefix `unarmed`
- **Size:** actorRadius 0.6–0.72 m · scale 1–1.42 · radius×scale 0.6–1.02 m · actorHeight 2 (template default; not a modelled height) · lead mesh bind-pose AABB height 3.78 *mesh units, Lap F caveat* *(DATAMINED)*
- **Locomotion:** characterRunSpeed 0.7–1 → **2.25–3.21 m/s** (INFERRED, × K4-0) · walkSpeed 0.45, 0.6
- **Attack style:** aoe 70% · projectile 26% *(INFERRED)* · weapon: unarmed
- **Core clips (lead):** idle `basilisk_combatidle_a01` 57f · run `basilisk_run_a01` 35f · walk `basilisk_walk_a01` 49f · attack ×3: `basilisk_attack_a01` 38f (hit f13), `basilisk_attack_b01` 51f (hit f18), `basilisk_attack_c01` 36f (hit f15) · spawn `basilisk_spawn_a01` 47f · take_hit `basilisk_gethit_a01` 21f · die: `basilisk_death_a01` 37f
- **Spawn:** ring 5.78 · p05 0 · waves 152 (5), 153 (0.1), 156 (0.5), 157 (0.1)
- **Summons:** `trap_icespike_hero_a01` (limit 6, burst 1, ttl 12–15 s; granted)

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| special1 | `basilisk_acidbarf` | aoe (wave / cone) | 2.82–3.11 → **0–3.11** [Short] | — m/s · r 0.5 | 2 · wave 4 long, 2→2 wide | `basilisk_breath_a01` 45f · rel f16 (0.53 s) | poison 5 s; poison 2 s; field/buff 8 s | 5: pfx_poisonfield_small_01 | 2.64 |
| special2 | `basilisk_petrifyingglare` | aoe (wave / cone) | 2.9–3.11 → **0–3.11** [Medium] | — | wave 6 long, 1.4→2 wide | `basilisk_petrifyingglare_a01` 45f · rel f16 (0.53 s) | totalspeed 3 s | 2: generic_cast_fx (clip), basilisk_glarepath_fx01 (clip) | 2.55 |
| special1 | `basilisk_tailswipe` | aoe | 2.9–3.11 → **0–3.11** [Short] | — | 3.8 | `basilisk_attackspecial_a01` 44f · rel f16 (0.53 s) | physical 2 s | 3: blitz1_impact | 2.52 |
| basic | `basilisk_acidspit` | projectile | 16.57 | 18 m/s · r 0.1 | 1.5 | `basilisk_castattack_a01` 35f · rel f21 (0.7 s) *inf* | — | 6: pfx_poisonbolt_flight01, pfx_groble_poisonorb_impact01 | 1.21 |
| dying | `corrupted_aetherconflagration` | projectile (lobbed area) | on death | — m/s · r 0.5 | 3 | fires at death (death clip) | field/buff 6 s | 5: pfx_aetherring_warden_01 | 0.94 |
| basic | `stonebasilisk_acidbarf` | aoe (wave / cone) | 2.9 | — m/s · r 0.5 | 3 · wave 3.5 long, 1→1 wide | `basilisk_breath_a01` 45f · rel f16 (0.53 s) | offensiveability 2 s; poison 2 s; field/buff 6 s | 5: pfx_poisoncloud_01 | 0.51 |
| special1 | `stonebasilisk_homingspit` | projectile | 16.65 → **6.15–16.65** [Long] | 9 m/s · r 0.5 | 1.5 | `basilisk_castattack_a01` 35f · rel f21 (0.7 s) *inf* | — | 6: pfx_acidorb01_lg_flight, pfx_acidorb01_lg_impact | 0.51 |
| special2 | `stonebasilisk_petrifyingglare` | aoe (wave / cone) | 2.9 → **0–2.9** [Medium] | — | wave 6 long, 1.4→2 wide | `basilisk_petrifyingglare_a01` 45f · rel f16 (0.53 s) | totalspeed 5 s | 2: generic_cast_fx (clip), basilisk_glarepath_fx01 (clip) | 0.51 |
| special3 | `stonebasilisk_tailswipe` | aoe | 2.9 → **0–2.9** [Short] | — | 3.8 | `basilisk_attackspecial_a01` 44f · rel f16 (0.53 s) | — | 3: blitz1_impact | 0.51 |
| special4 | `stonebasilisk_acidprojectilenova` | projectile (ring / nova) | 6.4 → **6.15–6.4** [Long] | 16 m/s · r 0.1 | — | `basilisk_castbuff_a01` 55f ×1.15 · rel f23 (0.77 s) | poison 5 s | 7: pfx_acidorb01_lg_flight, pfx_acidorb01_lg_impact | 0.51 |
| tree_attack | `stonebasilisk_poisoncloudsecondary` | projectile (lobbed area) | 16.65 | — m/s · r 0.5 | 3 | `basilisk_castattack_a01` 35f · rel f21 (0.7 s) *inf* | offensiveability 2 s; poison 2 s; field/buff 6 s | 4: pfx_poisoncloud_01 | 0.51 |
| initial | `corrupted_aetheraura` | aura (toggled) | aura | — | 12 · aura 12 | applied at spawn (initial skill); no cast clip | — | 6: pfx_aethercorruptedaura_self01, pfx_aethercorruptedaura_other01 | 0.44 |

*13 further abilities (hero/boss-only or < 0.25 expected bodies) are in `roster.json` → `types[10].abilities`.*

### 12. `cannibal` — Ugdenbog Wretch · 5.65 bodies (64.8 % cum.)

- **Lead record:** `records/creatures/enemies/wendigocannibal_a01.dbr` (Ugdenbog Wretch, trash, GD class Common)
- **Records:** 9 on 9 meshes. Names: Ugdenbog Wretch / Ugdenbog Turned / Ugdenbog Marked / Packla, the Turning …
- **Role mix (bodies):** trash 5.32, boss 0.33, champion-hero 0 · **family:** Undead + Human
- **Meshes (bodies):** `wendigo_cannibal01a` 2.71, `wendigo_cannibal01c` 2.11, `wendigo_cannibal02a` 0.5, `wendigo_cannibal02b` 0.33, `wendigo_cannibal01c_fire` 0, `wendigo_cannibal02a_bloody` 0 …
- **Anim table(s):** `anm_cannibal` · style prefix `unarmed`
- **Size:** actorRadius 0.8 m · scale 0.9–1.25 · radius×scale 0.72–1 m · actorHeight 2 (template default; not a modelled height) · lead mesh bind-pose AABB height 3.94 *mesh units, Lap F caveat* *(DATAMINED)*
- **Locomotion:** characterRunSpeed 1–1.1 → **3.21–3.53 m/s** (INFERRED, × K4-0) · walkSpeed 0.75
- **Attack style:** melee 44% · projectile 40% · buff 12% *(INFERRED)* · weapon: unarmed
- **Core clips (lead):** idle `cannibal_combatidle_a01` 61f · run `cannibal_run_a01` 21f · walk `cannibal_walk_a01` 37f · attack ×2: `cannibal_attack_a01` 33f (hit f15), `cannibal_attack_b01` 27f (hit f11) · spawn: — · take_hit `cannibal_gethit_a01` 19f · die: `cannibal_death_a01` 21f
- **Spawn:** ring 5.65 · p05 0 · waves 153 (2.7), 154 (2.6), 157 (0.3)
- **Summons:** `trap_brambletrap_a01` (limit 6, burst 1, ttl 12–15 s; granted)

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| special1 | `wendigocannibal_hungeringswipe` | melee | 2.89–3.09 → **0–3.09** [Short] | — | — | `cannibal_attack_a01` 33f · rel f15 (0.5 s) *inf* | life 5 s | 3: pfx_bloodstrike | 2.6 |
| special2 | `wendigocannibal_bloodpool` | projectile (lobbed area) | 6.39–6.59 | — m/s · r 0.5 | 2.4 | `cannibal_cast_a01` 37f · rel f18 (0.6 s) *inf* | bleeding 1 s; offensivereduction 2 s; field/buff 5 s | 5: pfx_crimsonpool_ghoul | 2.11 |
| initial | `packla_leechingpresence` | aura (timed) | aura | — | 5 · aura 5 | applied at spawn (initial skill); no cast clip | field/buff 6 s | 3: pfx_wendigo_leechingpresence_self | 0.66 |
| initial | `wendigocannibal_bloodeningaura` | aura (toggled) | aura | — | 10 · aura 10 | applied at spawn (initial skill); no cast clip | — | 6: pfx_groblebloodlust_other01, pfx_wasp_hivemind_self01 | 0.5 |
| special2 | `wendigocannibal_bloodlink` | buff | 3.01–3.09 → **0–3.09** [Short] | — | — | `cannibal_cast_a01` 37f · rel f18 (0.6 s) *inf* | bleeding 1 s; field/buff 5 s | 3: pfx_groblebloodlust_self01 | 0.5 |
| special1 | `packla_devouringwave` | aoe (wave / cone) | 16.84 → **0–9.34** [Medium] | — | wave 16 long, 2→3.5 wide | `cannibal_attackspecial_thrash_a01` 41f · rel f17 (0.57 s) | — | 2: pfx_spectralwave_path01 | 0.33 |
| special2 | `packla_bonespines` | projectile (ring / nova) | 10.84 → **0–9.34** [Medium] | 20 m/s · r 0 | 2 | `cannibal_attackspecial_thrash_a01` 41f · rel f17 (0.57 s) | — | 7: pfx_bloodorb_impact | 0.33 |
| special3 | `packla_bloodlink` | buff | 3.09 → **0–3.09** [Short] | — | — | `cannibal_cast_a01` 37f · rel f18 (0.6 s) *inf* | bleeding 1 s; field/buff 5 s | 3: pfx_groblebloodlust_self01 | 0.33 |

*6 further abilities (hero/boss-only or < 0.25 expected bodies) are in `roster.json` → `types[11].abilities`.*

### 13. `thornedhorrora01` — Rimethorn Horror · 5.07 bodies (67.8 % cum.)

- **Lead record:** `records/creatures/enemies/thornedhorrorfrost_a01.dbr` (Rimethorn Horror, trash, GD class Champion)
- **Records:** 8 on 8 meshes. Names: Rimethorn Horror / Rimethorn Terror / Rimethorn Monstrosity / Everbarb ~ Reflective …
- **Role mix (bodies):** trash 3.49, champion-hero 1.58 · **family:** Riftspawn
- **Meshes (bodies):** `aetherhorrorb01` 1.85, `aetherhorrora01_frostranged` 0.92, `aetherhorrora01_frost_lg` 0.72, `aetherhorrorb01_reflective` 0.38, `aetherhorrora01_bramble` 0.38, `aetherhorrora01_arcane` 0.38 …
- **Anim table(s):** `anm_thornedhorror`, `anm_thornedhorrorfrost` · style prefix `unarmed`
- **Size:** actorRadius 0.8–1 m · scale 0.65–1.15 · radius×scale 0.52–1.15 m · actorHeight 2 (template default; not a modelled height) · lead mesh bind-pose AABB height 4.8 *mesh units, Lap F caveat* *(DATAMINED)*
- **Locomotion:** characterRunSpeed 1.1–1.16 → **3.53–3.72 m/s** (INFERRED, × K4-0) · walkSpeed 1.25, 1.28
- **Attack style:** melee 66% · aoe 22% · projectile 12% *(INFERRED)* · weapon: unarmed
- **Core clips (lead):** idle `thornedhorrora01_idle_01` 76f · run `thornedhorrora01_run_01` 21f · walk `thornedhorrora01_walk_01` 41f · attack ×3: `thornedhorrora01_attack_01` 51f (hit f23), `thornedhorrora01_attack_02` 51f (hit f22), `thornedhorrora01_attack_01` 51f (hit f23) · spawn: — · take_hit `thornedhorrora01_hit_react_01` 21f · die: `thornedhorrora01_death_01` 61f
- **Spawn:** ring 5.07 · p05 0 · waves 152 (5), 153 (0.1)
- **Summons:** `trap_brambletrap_a01` (limit 6, burst 1, ttl 12–15 s; granted); `trap_lightningspike_hero_a01` (limit 6, burst 1, ttl 24–27 s; granted)

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| special1 | `thornedhorrorfrost_iceslash` | melee | 2.61–2.98 → **0–2.98** [Short] | — | — | `thornedhorrora01_attack_crossswipe` 56f · rel f25 (0.83 s) | — | 4: pfx_chillingtouch_impact | 5 |
| special2 | `thornedhorrorfrost_avalanche` | aoe (wave / cone) | 10.73 → **0–10.73** [Medium] | — | wave 16 long, 2→2 wide | `thornedhorrora01_attack_3x_groundimpale` 86f · rel f27 (0.9 s) | totalspeed 2 s | 7: pfx_avalanche_appearance_01 | 2.23 |
| initial | `thornedhorrorfrost_chillingaura` | aura (toggled) | aura | — | 10 · aura 10 | applied at spawn (initial skill); no cast clip | totalspeed 2 s | 5: pfx_buffaura_blue_self, pfx_buffaura_blue_other | 1.85 |
| dying | `thornedhorrorfrost_icethornfield` | projectile (lobbed area) | on death | — m/s · r 0.5 | 3.8 | fires at death (death clip) | runspeed 1 s; field/buff 6 s | 4: pfx_briarfieldcold_01 | 1.64 |
| basic | `thornedhorrorfrost_iceshardburst` | projectile (burst) | 16.52 | 18 m/s · r 0.5 | 1 | `thornedhorrora01_cast_attack_01` 51f · rel f31 (1.03 s) *inf* | — | 7: pfx_icebolt_flight01, pfx_icespike_impact01 | 0.92 |
| initial | `arcane_elementalaura` | aura (toggled) | aura | — | 12 · aura 12 | applied at spawn (initial skill); no cast clip | — | 2: pfx_elementalaura_other01 | 0.38 |
| special3 | `arcane_elementaltempest` | aoe | 16.73 → **0–5.23** [Short] | — | 5.5 | `thornedhorrora01_cast_attack_01` 51f · rel f31 (1.03 s) *ref unbound* | — | 3: pfx_arcaneblast_huge_02 | 0.38 |
| special4 | `arcane_elementalbolt` | projectile | 16.73 | 14 m/s · r 0.3 | 2.5 | `thornedhorrora01_cast_attack_01` 51f · rel f31 (1.03 s) *inf* | fire 5 s | 10: pfx_elementaldispelbolt_flight, pfx_elementaldispelbolt_impact | 0.38 |

*3 further abilities (hero/boss-only or < 0.25 expected bodies) are in `roster.json` → `types[12].abilities`.*

### 14. `skeleton_01a` — Storm Revenant · 5.03 bodies (70.7 % cum.)

- **Lead record:** `records/creatures/enemies/skeleton_c03.dbr` (Storm Revenant, trash, GD class Champion)
- **Records:** 15 on 8 meshes. Names: Storm Revenant / Flame Revenant / Frost Revenant / Death Revenant …
- **Role mix (bodies):** trash 4.64, champion-hero 0.39 · **family:** Undead
- **Meshes (bodies):** `skeleton_baseheavy_fire_01a` 1.24, `skeleton_baseheavy_lightning_01a` 1.2, `skeleton_baseheavy_ice_01a` 1.16, `skeleton_baseheavy_deathly_01a` 0.66, `skeleton_baseheavy_01a` 0.57, `skeleton_basecaster_01a` 0.12 …
- **Anim table(s):** `anm_skeleton_fast` · style prefix `unarmed`
- **Size:** actorRadius 0.35 m · scale 1.12–1.3 · radius×scale 0.39–0.46 m · actorHeight 2 (template default; not a modelled height) · lead mesh bind-pose AABB height — *mesh units, Lap F caveat* *(DATAMINED)*
- **Locomotion:** characterRunSpeed 1.1–1.2 → **3.53–3.85 m/s** (INFERRED, × K4-0) · walkSpeed 1
- **Attack style:** projectile 63% · aoe 22% · aura 14% · summons on 15% of bodies *(INFERRED)* · weapon: unarmed
- **Core clips (lead):** idle `skeleton_01a_idle` 101f · run `skeleton_01a_runfast` 25f · attack ×3: `skeleton_01a_attack_a` 41f (hit f24), `skeleton_01a_attack_b` 46f (hit f22), `skeleton_01a_attack_a` 41f (hit f24) · spawn `skeleton_01a_spawn` 61f · take_hit `skeleton_01a_takehit` 16f · die: `skeleton_01a_death` 61f, `skeleton_01a_death_b` 24f
- **Spawn:** ring 5.03 · p05 0 · waves 153 (3.5), 157 (1.1), 158 (0.4)
- **Summons:** `skeleton_a02_summon` (limit 4, burst 2, ttl 30 s; granted); `skeleton_a01_summon` (limit 4, burst 2, ttl 30 s; granted); `skeleton_b02_knight_summon` (limit 4, burst 1, ttl — s; granted); `skeleton_c02_summon` (limit 2, burst 1, ttl 60 s; granted); `hellhound_undeadfaction_a01` (limit 4, burst 1, ttl 20 s; granted) …

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| special1 | `skeleton_fireballnova` | projectile (ring / nova) | 16.24–16.26 → **0–16.26** [Medium] | 12 m/s · r 0.1 | 1.5 | `skeleton_01a_special_slow` 61f · rel f46 (1.53 s) | fire 2 s | 6: pfx_ammomodification2_impact, pfx_groble_fireball_flight01 | 1.28 |
| special1 | `skeleton_chainlightning` | projectile (chain) | 16.24 → **3.74–16.24** [Medium] | — | — | `skeleton_01a_attack_a` 41f · rel f24 (0.8 s) *inf* | — | 1: chainlightning1 | 1.2 |
| special2 | `skeleton_ringofflame1` | aura (timed) | 5.99 → **0–4.74** [Short] | — | 4 | `skeleton_01a_attack_a` 41f · rel f24 (0.8 s) *inf* | fire 2 s; field/buff 8 s | 3: pfx_ringofflame01 | 1.2 |
| special1 | `skeleton_icenova_01` | aoe | 5.99 → **0–4.74** [Short] | — | 5 | `skeleton_01a_attack_a` 41f · rel f24 (0.8 s) *inf* | cold 3 s; runspeed 3 s | 3: pfx_iceexplosion01 | 1.12 |
| special2 | `skeleton_freezespike_01` | projectile | 16.24 → **4.74–15.74** [Medium] | 30 m/s · r 0.5 | — | `skeleton_01a_attack_a` 41f · rel f24 (0.8 s) *ref unbound* | — | 7: pfx_icebolt_flight01, pfx_icespike_impact01 | 1.12 |
| basic | `skeleton_undeathmissiles` | projectile (burst) | 16.24 | 40 m/s · r 0 | 1.5 | `skeleton_01a_attack_a` 41f · rel f24 (0.8 s) *inf* | — | 8: pfx_arcanecast_02, pfx_cultist_chaosbolt_flight01 | 0.66 |
| initial | `skeleton_undeathaura1` | aura (toggled) | aura | — | 10 · aura 10 | applied at spawn (initial skill); no cast clip | — | 8: pfx_wpn_vitality_other01 | 0.66 |
| special2 | `chthonicminion_novalifedrain01` | aoe | 2.49 → **0–2.49** [Short] | — | 4 | `skeleton_01a_attack_a` 41f · rel f24 (0.8 s) *inf* | lifeleach 2 s | 3: pfx_generic_novaspectral_01 | 0.66 |

*33 further abilities (hero/boss-only or < 0.25 expected bodies) are in `roster.json` → `types[13].abilities`.*

### 15. `heroine01_unarmed` — Apparition · 4.29 bodies (73.2 % cum.)

- **Lead record:** `records/creatures/enemies/ghost_a01.dbr` (Apparition, trash, GD class Common)
- **Records:** 12 on 6 meshes. Names: Apparition / Janaxia, the Betrayer / Larria, the Hexxer / Allostria, the Mindthief …
- **Role mix (bodies):** boss 1.99, trash 1.63, champion-hero 0.46, nemesis 0.2 · **family:** Human, Undead, Aetherial + Human, Bloodsworn + Human
- **Meshes (bodies):** `ghost_f_a01` 1.63, `humanfemale04a` 1, `possessedf_01a` 0.8, `humanfemale06c` 0.5, `humanfemale02b` 0.28, `kurnchthonic01a_m` 0.08
- **Anim table(s):** `anm_boss_puppetmaster`, `anm_ghost_female`, `anm_humanfemale`, `anm_humankurnfemale` (+1) · style prefix `unarmed`
- **Size:** actorRadius 0.35–0.5 m · scale 1–1.35 · radius×scale 0.35–0.68 m · actorHeight 2 (template default; not a modelled height) · lead mesh bind-pose AABB height 0.36 *mesh units, Lap F caveat* *(DATAMINED)*
- **Locomotion:** characterRunSpeed 0.6–1.1 → **1.93–3.53 m/s** (INFERRED, × K4-0) · walkSpeed 0.7, 1
- **Attack style:** projectile 74% · aoe 13% *(INFERRED)* · weapon: unarmed
- **Core clips (lead):** idle `heroine01_sword1h_idlecombat` 61f · run `heroine01_unarmed_run` 25f · walk `heroine01_walk_a01` 31f · attack ×2: `heroine01_sword1h_attack_a01` 19f (hit f8), `heroine01_sword1h_attack_b01` 19f (hit f8) · spawn `ghost_f_spawn_b01` 14f · take_hit `heroine01_unarmed_gethit_a01` 21f · die: `heroine01_death_a` 91f
- **Spawn:** ring 4.29 · p05 0 · waves 151 (1.6), 153 (0.5), 155 (0.5), 156 (1.5), 160 (0.2)
- **Summons:** `wraith_b01_summon` (limit 4, burst 2, ttl 40 s; granted); `winddevil_01` (limit 4, burst 1, ttl 12 s; granted); `skeletonfrost_b04_evoker_summon` (limit 12, burst 3, ttl 75 s; granted); `skeletonfrost_c02_summon` (limit 6, burst 2, ttl 45 s; granted); `necro2_nulltotem` (limit 5, burst 1, ttl 8 s; granted) …

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| chain_next | `witch_arcanemissilenova` | projectile (ring / nova) | 16.24 | 16 m/s · r 0.3 | 0.5 | `heroine01_unarmed_spell_nova_a01` 19f · rel f11 (0.37 s) | — | 9: pfx_arcanecast_02, pfx_arcanemissile_flight_01 | 1 |
| basic | `witch_necroticmissiles` | projectile (burst) | 16.3 | 20 m/s · r 0.1 | 1.5 | `heroine01_sword1h_spellattack_b01` 19f · rel f10 (0.33 s) *inf* | — | 8: pfx_arcanecast_02, pfx_necroticmissile_flight | 1 |
| special1 | `witch_commandoozenovaturret` | projectile (fan) | 33.3 → **5.8–15.8** [Long] | 10 m/s · r 0.5 | — | `heroine01_sword1h_skill_stormcaller_a01` 21f · rel f12 (0.4 s) | totalspeed 3 s | 6: pfx_chaos_fireball_huge_flight01, pfx_chaos_fireball_huge_impact01 | 1 |
| special2 | `witch_necroticprojectilenova` | projectile (ring / nova) | 6.05 → **0–6.05** [Medium] | 14 m/s · r 0.5 | 0.5 | `heroine01_unarmed_spell_nova_a01` 19f · rel f11 (0.37 s) | — | 6: pfx_necroticmissile_flight, pfx_necroticmissile_impact | 1 |
| special3 | `witch_goregeyser` | projectile (lobbed area) | 16.3 | — m/s · r 0.5 | 2.5 | `heroine01_sword1h_skill_stormcaller_a01` 21f · rel f12 (0.4 s) | bleeding 1 s; field/buff 6 s | 4: pfx_bloodspout | 1 |
| special5 | `witch_vitalityzap` | aoe | 19.3 → **5.8–15.8** [Long] | — | — | `heroine01_sword1h_spellattack_b01` 19f · rel f10 (0.33 s) *inf* | attackspeed 3 s | 10: pfx_evileye_impact_03, pfx_poisonbolt_01 | 1 |
| basic | `witch_arcanemissile` | projectile (fan) | 16.24 | 33 m/s · r 0.3 | 0.5 | `heroine01_sword1h_spellattack_b01` 19f · rel f10 (0.33 s) *inf* | — | 9: pfx_arcanecast_02, pfx_arcanemissile_impact_01 | 0.5 |
| special1 | `witch_commandaethernovaturret` | projectile (fan) | 33.24 → **5.74–15.74** [Long] | 9 m/s · r 0.5 | — | `heroine01_sword1h_skill_stormcaller_a01` 21f · rel f12 (0.4 s) | — | 7: pfx_aethermissile_flight01, pfx_aethermissile_impact01 | 0.5 |
| special3 | `witch_icebreath` | aoe (wave / cone) | 5.99 → **0–4.74** [Short] | — | wave 13 long, 2.5→2.5 wide | `heroine01_sword1h_skill_icebreath_a01` 41f · rel f21 (0.7 s) | cold 5 s | 1: icebreathfx01 (clip) | 0.5 |
| basic | `mindthief_icebolt` | projectile (burst) | 16.24 | 18 m/s · r 0.1 | 2 | `heroine01_sword1h_spellattack_b01` 19f · rel f10 (0.33 s) *inf* | cold 5 s; defensiveability 5 s; totalspeed 2 s | 7: pfx_icebolt_flight01, pfx_icespike_impact01 | 0.49 |
| special1 | `mindthief_shatteringice` | projectile | 16.24 → **3.74–14.74** [Medium] | 15 m/s · r 0.1 | 2.5 | `heroine01_sword1h_spellattack_b01` 19f · rel f10 (0.33 s) *inf* | — | 8: pfx_icebolt_flight01, pfx_icebolt_impact01 | 0.49 |
| special2 | `mindthief_skysharddevastation` | aura (drop / mortar) | 19.24 | 30 m/s · r 0.5 | 2.2/8 | `heroine01_sword1h_spell_doombolt_a01` 19f · rel f11 (0.37 s) | field/buff 8 s | 8: pfx_skyshard_flight01, pfx_skyshard_impact01 | 0.49 |

*30 further abilities (hero/boss-only or < 0.25 expected bodies) are in `roster.json` → `types[14].abilities`.*

### 16. `voidfiend` — Voidlurker Blightbearer · 4.04 bodies (75.5 % cum.)

- **Lead record:** `records/creatures/enemies/chthonianwretch_b01.dbr` (Voidlurker Blightbearer, trash, GD class Champion)
- **Records:** 15 on 3 meshes. Names: Voidlurker Blightbearer / Voidlurker / Voidlurker Pestilence / Vom'Zul …
- **Role mix (bodies):** trash 3.74, champion-hero 0.3 · **family:** Chthonic
- **Meshes (bodies):** `voidfiend01` 2.96, `voidfiend10_poison` 1.04, `voidfiend07` 0.04
- **Anim table(s):** `anm_chthonianvoidfiend` · style prefix `unarmed`
- **Size:** actorRadius 0.36–0.5 m · scale 1.1–1.5 · radius×scale 0.4–0.75 m · actorHeight 2 (template default; not a modelled height) · lead mesh bind-pose AABB height 2.62 *mesh units, Lap F caveat* *(DATAMINED)*
- **Locomotion:** characterRunSpeed 0.8–0.9 → **2.57–2.89 m/s** (INFERRED, × K4-0) · walkSpeed 1.15
- **Attack style:** aoe 48% · projectile 30% · aura 21% *(INFERRED)* · weapon: unarmed
- **Core clips (lead):** idle `voidfiend_idle_01` 61f · run `voidfiend_run_01` 21f · walk `voidfiend_walk_01` 31f · attack ×2: `voidfiend_attack_01` 43f (hit f15), `voidfiend_attack_02` 43f (hit f14) · spawn `voidfiend_spawn_01` 96f · take_hit `voidfiend_hitreact_01` 21f · die: `voidfiend_death_01` 56f
- **Spawn:** ring 4.04 · p05 0 · waves 153 (0.1), 154 (2.7), 156 (1.1), 158 (0.2)

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| dying | `chthonianwretch_causticeruption` | aoe | on death | — | 4.8 | fires at death (death clip) | poison 3 s | 3: pfx_causticeruption | 3.74 |
| special1 | `chthonianwretch_acidbreath` | aoe (wave / cone) | 2.48–2.52 → **0–2.52** [Short] | — m/s · r 0.5 | 2 · wave 3.5 long, 1→1 wide | `voidfiend_cast_barfacid_01` 51f · rel f19 (0.63 s) | poison 5 s; poison 2 s; field/buff 8 s | 5: pfx_poisonfield_small_01 | 2.5 |
| basic | `chthonianwretch_poisonorb` | projectile | 10.23 | 12 m/s · r 0.5 | 2.5 | `voidfiend_attack_02` 43f · rel f14 (0.47 s) *inf* | poison 10 s | 6: pfx_acidorb01_lg_flight, pfx_acidorb01_lg_impact | 1.45 |
| special3 | `chthonianwretch_causticpresence` | aura (timed) | 6.02 → **0–4.77** [Short] | — | 3.5 | `voidfiend_cast_buff_01` 61f · rel f45 (1.5 s) *inf* | field/buff 6 s | 3: pfx_zombie_poisonaura01 | 1.04 |

*21 further abilities (hero/boss-only or < 0.25 expected bodies) are in `roster.json` → `types[15].abilities`.*

### 17. `chthonianrylok` — Ekket'Zul, Progenitor of Darkness · 3.48 bodies (77.6 % cum.)

- **Lead record:** `records/creatures/enemies/chthonianrylok_a01.dbr` (Void Rylok, trash, GD class Common)
- **Records:** 16 on 11 meshes. Names: Ekket'Zul, Progenitor of Darkness / Gabal'Thunn, the Visage of Madness / Void Rylok / Eldritch Gargoyle …
- **Role mix (bodies):** trash 1.51, boss 1.5, champion-hero 0.27, nemesis 0.2 · **family:** Chthonic, Eldritch
- **Meshes (bodies):** `chthonianrylok01b_chaos` 0.53, `eldritchgargoyle01a` 0.52, `chthonianrylok01c_fire` 0.5, `eldritchgargoyle02b_fire` 0.5, `chthonianrylok01b` 0.42, `chthonianrylok01a` 0.38 …
- **Anim table(s):** `anm_chthonian_rylok`, `anm_chthonian_rylok_bossfire`, `anm_chthonian_rylok_winged`, `anm_gargoyle` (+1) · style prefix `unarmed`
- **Size:** actorRadius 0.8–0.9 m · scale 1–1.75 · radius×scale 0.8–1.57 m · actorHeight 2 (template default; not a modelled height) · lead mesh bind-pose AABB height 5.3 *mesh units, Lap F caveat* *(DATAMINED)*
- **Locomotion:** characterRunSpeed 0.9–1.1 → **2.89–3.53 m/s** (INFERRED, × K4-0) · walkSpeed 1, 1.15, 1.2
- **Attack style:** melee 42% · projectile 28% · aoe 27% *(INFERRED)* · weapon: unarmed
- **Core clips (lead):** idle `chthonianrylok_combatidle_a01` 39f · run `chthonianrylok_run_a01` 31f · walk `chthonianrylok_walk_a01` 37f · attack ×2: `chthonianrylok_attack_a01` 33f (hit f13), `chthonianrylok_attack_a02` 39f (hit f17) · spawn `chthonianrylok_spawn_a01` 20f · take_hit `chthonianrylok_gethit_a01` 15f · die: `chthonianrylok_death_a01` 29f
- **Spawn:** ring 2.48 · p05 1 · waves 153 (0.1), 154 (0.5), 157 (1.7), 159 (1), 160 (0.2)
  - p05 emergence: Ekket'Zul, Progenitor of Darkness: `chthonianrylok_spawn_c01_fire` 106f → **3.5 s** (PACK `V38-AM3-4`)
  - p05 emergence: Okaloth ~ "The Messenger": `chthonianrylok_roar_a01` 43f → **1.4–1.87 s** (PACK `V38-AM3-6`)
  - p05 emergence: Okaloth ~ "The Messenger": `chthonianrylok_roar_a01` 43f → **1.4–1.87 s** (PACK `V38-AM3-5`)
- **Summons:** `gabbalthunn_obsidianshard` (limit 5, burst 1, ttl 30 s; granted); `eldritchground` (limit 6, burst 1, ttl 12–15 s; granted); `chthonian02_void` (limit 2, burst 1, ttl 4–7 s; granted)

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| dying | `chthonicminion_chaosblast` | aoe | on death | — | 9 | fires at death (death clip) | life 2 s | 4: pfx_riftblast_01 | 1.19 |
| basic | `chthonianrylok_brutalchaos` | melee (charge) | 2.89–3.21 | — | — | `chthonianrylok_attackspecial_b01_fire` 45f · rel f14 (0.47 s) | — | 5: pfx_firerage_self02, pfx_firerage_self03 | 1.07 |
| basic | `gargoyle_brutalstrike` | melee (charge) | 2.89–3.14 | — | — | `chthonianrylok_attackspecial_b01_lightning` 45f · rel f14 (0.47 s) | — | 5: pfx_icerage_self02, pfx_icerage_self03 | 0.72 |
| special3 | `chthonianrylok_wingclaws` | melee | 3.05–3.21 → **0–3.21** [Short] | — | — | `chthonianrylok_attack_a01` 33f · rel f13 (0.43 s) *ref unbound* | bleeding 5 s | 3: pfx_bloodstrike | 0.69 |
| special1 | `gargoyle_doubleswipe` | aoe (wave / cone) | 10.64–10.8 → **0–5.3** [Short] | — | wave 4 long, 3→4 wide | `chthonianrylok_cleaveice` 45f ×0.8 · rel f13 (0.43 s) | totalspeed 2 s | 2: ice_cast_fx (clip), icearc_fx01 (clip) | 0.52 |
| special1 | `chthonianrylok_chaosclawswipes` | aoe (wave / cone) | 10.89–10.96 → **0–10.96** [Short] | — | wave 4 long, 3→4 wide | `chthonianrylok_castattack_a01` 35f · rel f18 (0.6 s) *ref unbound* | — | 1: dark_cast_fx (clip) | 0.51 |
| basic | `ekketzul_brutalchaos` | melee (charge) | 3.37 | — | — | `chthonianrylok_attackspecial_b01_fire` 45f ×0.9 · rel f14 (0.47 s) | — | 5: pfx_firerage_self02, pfx_firerage_self03 | 0.5 |
| dying | `ekketzul_fieryeruption` | aoe | on death | — | 8 | fires at death (death clip) | — | 3: pfx_arcaneblast_huge_03 | 0.5 |
| special1 | `ekketzul_chaosgust` | aoe (wave / cone) | 11.12 → **0–5.62** [Short] | — | wave 8 long, 3→4 wide | `chthonianrylok_attackspecial_a01_sunder` 73f ×0.9 · rel f17 (0.57 s) | damagemult 3 s; runspeed 1 s | 3: sunder_cast_fx (clip), sunder_overheadcast_fx (clip) | 0.5 |
| special2 | `ekketzul_firedoubleswipe` | aoe (wave / cone) | 6.87 → **0–5.62** [Short] | — | wave 9 long, 3→6 wide | `chthonianrylok_cleavefire` 45f ×0.8 · rel f14 (0.47 s) | — | 5: pfx_bloodstrike | 0.5 |
| special3 | `ekketzul_obsidianspineslam` | projectile (ring / nova) | 17.12 → **0–11.62** [Medium] | 10 m/s · r 0.5 | 0.1 | `chthonianrylok_attackspecial_c01` 39f ×0.9 · rel f22 (0.73 s) | — | 9: pfx_bloodstrike | 0.5 |
| special4 | `ekketzul_volcano` | projectile (lobbed area) | 11.12 | — m/s · r 1.8 | 1.5 | `chthonianrylok_castattack_a01` 35f · rel f18 (0.6 s) *inf* | fire 2 s; field/buff 10–14 s | 10: magi_volcano_fragment01, pfx_ammomodification2_impact | 0.5 |

*35 further abilities (hero/boss-only or < 0.25 expected bodies) are in `roster.json` → `types[16].abilities`.*

### 18. `aetherialbloater` — Aetherial Bloater · 3.28 bodies (79.5 % cum.)

- **Lead record:** `records/creatures/enemies/aetherialbloater_a01.dbr` (Aetherial Bloater, trash, GD class Common)
- **Records:** 10 on 2 meshes. Names: Aetherial Bloater / Aetherial Bileeater / Aetherial Regurgitator / Blugrug the Living Plague …
- **Role mix (bodies):** trash 2.52, champion-hero 0.42, boss 0.34 · **family:** Aether Corruption
- **Meshes (bodies):** `aetherialbloater01a` 2.95, `aetherialbloater01a_vitality` 0.34
- **Anim table(s):** `anm_aetherialbloater` · style prefix `unarmed`
- **Size:** actorRadius 0.75 m · scale 1–1.53 · radius×scale 0.75–1.15 m · actorHeight 2 (template default; not a modelled height) · lead mesh bind-pose AABB height — *mesh units, Lap F caveat* *(DATAMINED)*
- **Locomotion:** characterRunSpeed 0.9–1.1 → **2.89–3.53 m/s** (INFERRED, × K4-0) · walkSpeed 1
- **Attack style:** melee 65% · projectile 23% · summons on 14% of bodies *(INFERRED)* · weapon: unarmed
- **Core clips (lead):** idle `aetherialbloater_combatidle_a01` 45f · run `aetherialbloater_run_a01` 31f · walk `aetherialbloater_walk_a01` 45f · attack ×3: `aetherialbloater_attack_a01` 41f (hit f14), `aetherialbloater_attack_b01` 41f (hit f14), `aetherialbloater_attack_c01` 61f (hit f13) · spawn `aetherialbloater_spawn_a01` 31f · take_hit `aetherialbloater_gethit_a01` 17f · die: `aetherialbloater_death_a01` 40f
- **Spawn:** ring 3.28 · p05 0 · waves 153 (0.3), 156 (1.3), 157 (1.7)
- **Summons:** `aetherialworm_b01_summon` (limit 4–6, burst 2–4, ttl 30 s; granted); `aetherialworm_b02_summon` (limit 4–6, burst 2–4, ttl 30 s; granted); `aetherialworm_b03_summon` (limit 4–6, burst 2–4, ttl 30 s; granted); `aetherialworm_b04_summon` (limit 4–6, burst 2–4, ttl 30 s; granted); `aetherialcorruption_b03_summon` (limit 8, burst 2, ttl 30 s; granted)

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| basic | `aetherialbloater_bite` | melee (charge) | 2.95–3.08 | — | — | `aetherialbloater_bite_a01` 31f · rel f14 (0.47 s) | poison 8 s | 4: pfx_zombiemutant_aethersmash_warmup01, pfx_zombiemutant_aethersmash_warmup02 | 1.82 |
| special1 | `aetherialbloater_violentbarf` | projectile (burst) | 10.77–10.98 → **0–10.48** [Medium] | 20 m/s · r 0.8 | 1 | `aetherialbloater_vomittriple_a01` 51f · rel f15 (0.5 s) | poison 5 s | 7: pfx_bilespit_flight, pfx_aetherialbloater_gorechunk_impact | 1.21 |
| special2 | `aetherialbloater_barf` | aoe (wave / cone) | 2.95–3.08 → **0–3.08** [Short] | — m/s · r 0.5 | 2 · wave 5 long, 1→2 wide | `aetherialbloater_vomit_a01` 51f · rel f18 (0.6 s) | defensiveability 12 s; poison 12 s; poison 2 s; field/buff 8 s | 5: pfx_poisonfield_small_01 | 1.13 |
| basic | `aetherialbloater_biteweak` | melee (charge) | 2.84 | — | — | `aetherialbloater_bite_a01` 31f · rel f14 (0.47 s) | poison 8 s | 4: pfx_zombiemutant_aethersmash_warmup01, pfx_zombiemutant_aethersmash_warmup02 | 1.12 |
| special1 | `aetherialbloater_thrash` | melee | 2.95 → **0–2.95** [Short] | — | — | `aetherialbloater_attack_c01aether` 61f · rel f13 (0.43 s) | poison 3 s | 4: pfx_acidstrike | 0.95 |
| special3 | `aetherialbloater_vilecharge` | melee (charge) | 2.95 → **9.2–2.95** [Long] | — | — | `aetherialbloater_attack_a01` 41f · rel f14 (0.47 s) *ref unbound* | runspeed 0.5–1.6 s | 5: pfx_bloodstrike, blitz1_warmuploop | 0.95 |
| initial | `aetherialbloater_chokingpresence` | aura (toggled) | aura | — | 4 · aura 4 | applied at spawn (initial skill); no cast clip | poison 2 s | 6: pfx_trollhalfcave_dreadaura_other01, pfx_troll_overpoweringstench01 | 0.8 |
| initial | `aetherialbloater_plaguepresence` | aura (toggled) | aura | — | 8 · aura 8 | applied at spawn (initial skill); no cast clip | poison 2 s | — | 0.33 |
| special2 | `avris_bloodorbnova` | projectile (ring / nova) | 16.98 → **0–10.48** [Medium] | 12 m/s · r 0.5 | 1.5 | `aetherialbloater_roar_a01` 35f · rel f16 (0.53 s) *inf* | bleeding 3 s | 6: pfx_bloodorb_flight, pfx_bloodorb_impact | 0.33 |

*15 further abilities (hero/boss-only or < 0.25 expected bodies) are in `roster.json` → `types[17].abilities`.*

### 19. `yeti` — Diremane Brute · 3.04 bodies (81.2 % cum.)

- **Lead record:** `records/creatures/enemies/yetidire_a01.dbr` (Diremane Brute, trash, GD class Champion)
- **Records:** 12 on 6 meshes. Names: Diremane Brute / Kubacabra, the Endless Menace / Diremane Icebreaker / Diremane Rager …
- **Role mix (bodies):** trash 1.74, champion-hero 0.55, nemesis 0.51, boss 0.25 · **family:** Beast
- **Meshes (bodies):** `yetidire01a` 1.52, `yetiswamp01a_blood` 0.51, `yeti02a` 0.41, `yetidire01c_cold` 0.25, `yetidire01b` 0.22, `yetiswamp01a_vitality` 0.14
- **Anim table(s):** `anm_yeti`, `anm_yetinemesis` · style prefix `unarmed`
- **Size:** actorRadius 1–1.3 m · scale 0.8–1.6 · radius×scale 1.04–1.62 m · actorHeight 2 (template default; not a modelled height) · lead mesh bind-pose AABB height 5.53 *mesh units, Lap F caveat* *(DATAMINED)*
- **Locomotion:** characterRunSpeed 0.7–1.15 → **2.25–3.69 m/s** (INFERRED, × K4-0) · walkSpeed 0.8, 1.1
- **Attack style:** projectile 39% · aoe 37% · aura 14% *(INFERRED)* · weapon: unarmed
- **Core clips (lead):** idle `yeti_combatidle_a01` 41f · run `yeti_run_a01` 16f · walk `yeti_walk_a01` 41f · attack ×3: `yeti_attack_a01` 31f (hit f15), `yeti_attack_c01` 26f (hit f11), `yeti_attack_d01` 35f (hit f15) · spawn: — · take_hit `yeti_gethit_a01` 16f · die: `yeti_death_a01` 22f
- **Spawn:** ring 3.04 · p05 0 · waves 153 (0.2), 154 (0.3), 157 (2.1), 159 (0.3), 160 (0.2)
- **Summons:** `beast_bloodpool` (limit 4, burst 1, ttl 12 s; granted); `rimehorn_icespike_01` (limit 4, burst 2, ttl 12 s; granted)

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| special2 | `yetidire_icehowl` | aura | 3.45 → **0–3.45** [Medium] | — | 8 | `yeti_roar_a01` 41f · rel f18 (0.6 s) *inf* | cold 2 s; field/buff 5 s | 6: pfx_debuffoverhead_yellow_loop, pfx_yeti_iceroar_01 | 0.64 |
| special1 | `yetidire_glacialbreath` | aoe (wave / cone) | 11.2 → **0–4.7** [Short] | — | wave 9 long, 2→3 wide | `yeti_attackbreatha01` 41f ×0.7 · rel f18 (0.6 s) | — | 1: frostbreathfx (clip) | 0.55 |
| initial | `beast_selfaura` | buff (toggled) | aura | — m/s · r 0.5 | 2.4 | applied at spawn (initial skill); no cast clip | bleeding 1 s; field/buff 10 s | 5: pfx_crimsonpool_ghoul | 0.5 |
| special1 | `beast_bloodgore` | melee | 3.69 → **0–3.69** [Short] | — | — | `yeti_attack_b01` 35f · rel f20 (0.67 s) | bleeding 3 s; ttl 12 s | 5: pfx_crimsonpool_wendigo_end, pfx_bloodstrike | 0.5 |
| special2 | `beast_bloodbreath` | aoe (wave / cone) | 17.44 → **0–6.94** [Medium] | — | wave 12 long, 2→3.5 wide | `yeti_attackbreathblood_a01` 41f ×0.6 · rel f18 (0.6 s) | bleeding 2 s; ttl 12 s | 6: pfx_crimsonpool_wendigo_end, pfx_bloodorb_impact | 0.5 |
| special3 | `beast_bonespines` | aoe (wave / cone) | 7.19 → **0–4.94** [Short] | — | wave 8 long, 2→8 wide | `yeti_groundslam_single_a01` 46f · rel f12 (0.4 s) | bleeding 3 s | 8: pfx_soulscythe_appearance_01, pfx_soulscythe_target_01 | 0.5 |
| special4 | `beast_howl` | aoe | 7.19 → **0–4.94** [Short] | — | 8 | `yeti_roar_a01` 41f · rel f18 (0.6 s) | bleeding 5 s; totalspeed 3 s | 3: pfx_chthonianwarrior_roar_01 | 0.5 |
| tree_attack | `beast_crimsonpool_hitsecondary` | projectile (lobbed area) | 7.19 | — m/s · r 0.5 | 2.4 | `yeti_roar_a01` 41f · rel f18 (0.6 s) *inf* | bleeding 1 s; field/buff 10 s | 5: pfx_crimsonpool_ghoul | 0.5 |
| special1 | `yetidire_icespikenova` | projectile (ring / nova) | 17.03 → **0–6.53** [Short] | 8 m/s · r 0.75 | 1.5 | `yeti_groundslam_a01` 46f · rel f11 (0.37 s) | cold 3 s | 10: pfx_icespikes_ground01, pfx_icespikes_ground_impact01 | 0.39 |
| special2 | `yetidire_throwglacier` | projectile | 17.03 → **8.53–17.03** [Long] | 15 m/s · r 0.25 | 3 | `yeti_attack_overheadthrow` 70f · rel f47 (1.57 s) | — | 9: pfx_glacier_flight01, pfx_glacier_impact01 | 0.39 |
| chain_initial | `swampyeti_poisoncharge` | melee (charge) | 3.54 | — | — | `yeti_attack_a01` 31f · rel f15 (0.5 s) *inf* | poison 5 s | 3: pfx_chillingtouch_impact | 0.27 |
| special1 | `rimehorn_leap` | aoe (leap) | 17.46 → **6.96–13.96** [Long] | — | 6 · wave 18 long, —→— wide | `yeti_attack_jump` 51f · rel f17 (0.57 s) | cold 3 s; ttl 12 s | 15: pfx_chaosexplosion_01, pfx_arctictrap01_activate | 0.25 |

*20 further abilities (hero/boss-only or < 0.25 expected bodies) are in `roster.json` → `types[18].abilities`.*

## D. Tier 2 — compact cards

Top abilities per rig, by bodies using them. The full set is in `roster.json`.

### 20. `giant` — Asterkarn Giant / Asterkarn Behemoth / The Underking / Asterkarn Titan · 2.31 bodies

Lead `records/creatures/enemies/giant_a01.dbr` · 8 records / 8 meshes · role mix trash 1.81, nemesis 0.5 · family Beastkin · radius×scale 0.7–1 m · run 3.21–3.53 m/s · melee 48% · projectile 30% · aoe 22% · weapon Spear2h · p05 0

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| basic | `giant_cleavingstrikes` | melee (charge) | 2.79–3.05 | — | — | `giant_attack_a01` 31f · rel f17 (0.57 s) *inf* | physical 3 s | 6: pfx_troll_rage_self01, pfx_troll_rage_self02 | 1.81 |
| special1 | `giant_boulder` | projectile | 16.54–16.8 → **6.04–16.8** [Long] | 15 m/s · r 1 | 3 | `giant_throw_boulder_a01` 71f · rel f43 (1.43 s) | — | 9: pfx_bouldergranite_lg_flight01, pfx_bouldergranite_lg_impact01 | 0.9 |
| initial | `giant_stench` | aura (toggled) | aura | — | 6 · aura 6 | applied at spawn (initial skill); no cast clip | attackspeed 1 s; poison 1 s | 6: pfx_buffaura_green_other, pfx_troll_overpoweringstench01 | 0.65 |
| special1 | `giant_rottenedge` | aoe (wave / cone) | 10.68 → **0–5.18** [Short] | — | wave 8 long, 3→5 wide | `giant_cleavepoison_a01` 71f · rel f26 (0.87 s) | poison 5 s | 2: poison_cast_fx (clip), acidarc_fx01 (clip) | 0.65 |
| basic | `beast2_toxiccadence` | melee (charge) | 3.09 | — | — | `giant_ground_slam_a01` 55f · rel f15 (0.5 s) | poison 12 s | 2: golemrock_rocksmash_trail_fx01 (clip), groundstomp_radius_fxpak01 (clip) | 0.5 |

*12 further abilities (hero/boss-only or < 0.1 expected bodies) are in `roster.json` → `types[19].abilities`.*

### 21. `leech` — Void Parasite / Void Souldrinker / Void Leech · 2.13 bodies

Lead `records/creatures/enemies/chthonianleech_a01.dbr` · 3 records / 1 meshes · role mix trash 2.13 · family Chthonic · radius×scale 0.72–0.92 m · run 3.21 m/s · melee 76% · aoe 12% · projectile 12% · weapon unarmed · p05 0

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| special1 | `chthonianleech_vampiricswipe_01` | melee | 2.81 → **0–2.81** [Short] | — | — | `leech_attack_a01` 31f · rel f13 (0.43 s) *ref unbound* | lifeleach 3 s | — | 1.1 |
| special1 | `chthonianleech_megavampiricswipe_01` | melee | 2.89–3.01 → **0–3.01** [Short] | — | — | `leech_attack_a01` 31f · rel f13 (0.43 s) *ref unbound* | lifeleach 3 s | — | 1.03 |
| initial | `chthonianleech_despairaura` | aura (toggled) | aura | — | 7 · aura 7 | applied at spawn (initial skill); no cast clip | — | 6: pfx_chthonianleech_despair_loop01, pfx_chthonianleech_despair_selfloop01 | 0.52 |
| special2 | `chthonianleech_drainlife` | aoe | 19.76 → **9.26–19.26** [Long] | — | — | `leech_cast_a01` 41f · rel f28 (0.93 s) *inf* | — | — | 0.52 |
| basic | `chthonianleech_vilespit` | projectile | 19.64 | 12 m/s · r 0.1 | 2.5 | `leech_attackspit_a01` 21f · rel f13 (0.43 s) | — | 6: pfx_chthonianleech_vilespit_flight, pfx_chthonianleech_vilespit_impact01 | 0.52 |

### 22. `heroine01_sword1h` — Haunted Noble / Torraxsteria ~ Frozen / Olga Flamebearer / Ludia Bloodwhisper · 1.96 bodies

Lead `records/creatures/enemies/ghost_b02.dbr` · 8 records / 4 meshes · role mix trash 1.54, champion-hero 0.42 · family Undead · radius×scale 0.35–0.6 m · run 1.93–3.21 m/s · melee 81% · projectile 15% · weapon Sword, Scepter · p05 0

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| special1 | `ghost_shadowstrike` | melee (blink strike) | 10.19–10.23 → **0–10.23** [Long] | — | — | `heroine01_sword1h_skill_jumpattack02` 22f ×1.1 · rel f10 (0.33 s) | — | 6: pfx_ghost_shadowstrike_impact, pfx_ghost_shadowstrike_cast | 1.58 |
| initial | `frozen_icearmoraura` | aura (toggled) | aura | — | 12 · aura 12 | applied at spawn (initial skill); no cast clip | — | 6: pfx_iceshield_other01, pfx_iceshield_self01 | 0.21 |
| special4 | `frozen_freezebomb` | projectile | 16.32–16.44 → **0–16.44** [Long] | 15 m/s · r 0.1 | 2.5 | `heroine01_sword1h_spellattack_b01` 19f · rel f10 (0.33 s) *ref unbound* | — | 7: pfx_icebolt_flight01, pfx_icebolt_impact01 | 0.18 |
| basic | `humanascendant_lightningorbnova` | projectile (ring / nova) | 19.32 | 16 m/s · r 0.1 | — | `heroine01_sword1h_spell_nova_a01` 19f · rel f11 (0.37 s) | lightning 5 s | 6: pfx_lightningorb01, pfx_lightningorb_impact01 | 0.14 |
| special1 | `humanascendant_stormburst` | projectile (burst) | 16.32 → **4.82–15.82** [Medium] | 16 m/s · r 0.1 | 1.5 | `heroine01_sword1h_spellattack_b01` 19f · rel f10 (0.33 s) *inf* | lightning 5 s | 6: pfx_lightningorb01, pfx_lightningorb_impact01 | 0.14 |

*23 further abilities (hero/boss-only or < 0.1 expected bodies) are in `roster.json` → `types[21].abilities`.*

### 23. `chthonianservitor` — Lunal'Valgoth, Steward of Darkness / Chthonian Drone / Chthonian Servitor / Chthonian Harvester · 1.9 bodies

Lead `records/creatures/enemies/chthonianservitor_a01.dbr` · 10 records / 5 meshes · role mix trash 1.12, boss 0.5, champion-hero 0.28 · family Chthonic + Insectoid · radius×scale 0.5–1 m · run 3.37–3.85 m/s · projectile 42% · melee 41% · aura 10% · weapon unarmed · p05 0

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| special1 | `chthonianservitor_impale` | melee | 2.59–3.04 → **0–3.04** [Short] | — | — | `chthonianservitor_attack_c01` 37f ×0.85 · rel f18 (0.6 s) | bleeding 2 s | 4: pfx_bloodstrike | 1.11 |
| special1 | `lunalvalgoth_impale` | melee | 3.09 → **0–3.09** [Short] | — m/s · r 0.5 | 2.4 | `chthonianservitor_attack_c01_sunder` 37f ×0.8 · rel f18 (0.6 s) | bleeding 5 s; damagemult 3 s; bleeding 1 s; defensiveability 2 s; offensiveability 2 s; field/buff 10–15 s | 10: pfx_crimsonpool_ghoul, pfx_bloodstrike | 0.5 |
| special2 | `lunalvalgoth_spitburst` | projectile | 16.84 → **5.34–15.34** [Medium] | 14 m/s · r 0.1 | 1.5/2.4 | `chthonianservitor_attackspittriple_a01` 36f ×0.9 · rel f16 (0.53 s) | bleeding 3 s; bleeding 1 s; defensiveability 2 s; offensiveability 2 s; field/buff 10–15 s | 11: pfx_crimsonpool_ghoul, pfx_bloodorb_flight | 0.5 |
| special3 | `lunalvalgoth_triplechaoswave` | aoe (wave / cone) | 16.84 → **5.34–15.34** [Medium] | — | wave 16 long, 2→2 wide | `chthonianservitor_attackspittriple_a01` 36f ×0.9 · rel f16 (0.53 s) | — | 2: pfx_chaoswave_path01 | 0.5 |
| tree_attack | `lunalvalgoth_bloodpool_secondary` | projectile (lobbed area) | 6.59 | — m/s · r 0.5 | 2.4 | `chthonianservitor_cast_a01` 44f · rel f28 (0.93 s) *inf* | bleeding 1 s; defensiveability 2 s; offensiveability 2 s; field/buff 10–15 s | 5: pfx_crimsonpool_ghoul | 0.5 |

*23 further abilities (hero/boss-only or < 0.1 expected bodies) are in `roster.json` → `types[22].abilities`.*

### 24. `possessedstatue` — The Steward / Risen Stone, Temple Guardian / Animated Keeper · 1.9 bodies

Lead `records/creatures/enemies/statue_a02.dbr` · 9 records / 3 meshes · role mix boss 0.99, trash 0.9 · family Construct + Eldritch · radius×scale 0.6–2.25 m · run 3.21–3.53 m/s · melee 49% · aoe 38% · projectile 13% · weapon Spear2h · p05 0

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| basic | `statue_overwhelmingstrength` | melee (charge) | 2.69–3.34 | — | — | `possessedstatue_attack_a01` 31f · rel f11 (0.37 s) *inf* | physical 3 s | 6: pfx_troll_rage_self01, pfx_troll_rage_self02 | 0.9 |
| special1 | `statue_megapunch` | melee | 2.69–2.97 → **0–2.97** [Short] | — | 4.5 | `possessedstatue_attackspecial_f01` 65f ×1.15 · rel f49 (1.63 s) | physical 2 s; poison 3 s | 4: pfx_eldritchnova_01 | 0.72 |
| special2 | `statue_doubleswipe` | aoe (wave / cone) | 10.72–11.09 → **0–5.59** [Short] | — | wave 8 long, 3→5 wide | `possessedstatue_attackspecial_b01` 43f ×0.8 · rel f12 (0.4 s) | physical 2 s | 2: vitality_cast_fx (clip), bloodarc_fx01 (clip) | 0.5 |
| basic | `tombguardian_massiveswipe` | melee (charge) | 7.84 | — | — | `possessedstatue_attackspecial_a01_celestial` 46f · rel f13 (0.43 s) | cold 5 s | 9: pfx_icerage_self01, pfx_icerage_self03 | 0.5 |
| special1 | `tombguardian_megapunch` | melee | 4.34 → **0–4.34** [Short] | — | — | `possessedstatue_attackspecial_f01_sunder` 65f · rel f49 (1.63 s) | damagemult 5 s | 2: sunder_cast_fx (clip), sunder_overheadcast_fx (clip) | 0.5 |

*13 further abilities (hero/boss-only or < 0.1 expected bodies) are in `roster.json` → `types[23].abilities`.*

### 25. `gryphon01a` — Corvunox ~ Vampiric / Corrot ~ Diseased / Covull ~ Swift / Corvulux ~ Supporter · 1.84 bodies

Lead `records/creatures/enemies/hero/hypporaven_h03.dbr` · 6 records / 5 meshes · role mix champion-hero 1.59, boss 0.25 · family Beast · radius×scale 1.15–1.25 m · run 3.21–3.53 m/s · projectile 76% · aoe 10% · weapon unarmed · p05 1.51

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| special1 | `hypporaven_darkbreath` | projectile (burst) | 10.99–11.09 → **0–5.59** [Short] | 13 m/s · r 0.1 | 1 | `gryphon01a_attackspecial_b01_breathshadow` 101f · rel f26 (0.87 s) | life 3 s | 8: pfx_shadowbreath_flight01, pfx_shadowbreath_impact01 | 1.59 |
| initial | `vampiric_vampireaura` | aura (toggled) | aura | — | 12 · aura 12 | applied at spawn (initial skill); no cast clip | — | 5: pfx_vampiricaura_self01, pfx_vampiricaura_other01 | 0.38 |
| special2 | `vampiric_vitalitywave` | aoe (wave / cone) | 16.99 → **0–5.49** [Short] | — | wave 16 long, 2→3.5 wide | `gryphon01a_attack_a01` 22f · rel f12 (0.4 s) *inf* | — | 2: pfx_spectralwave_path01 | 0.38 |
| special3 | `vampiric_bloodlink` | buff | 3.24 → **0–3.24** [Medium] | — | — | `gryphon01a_attackspecial_a01` 46f · rel f12 (0.4 s) *inf* | bleeding 1 s; field/buff 5 s | 3: pfx_groblebloodlust_self01 | 0.38 |
| initial | `diseased_diseasecloud` | aura (toggled) | aura | — | 4 · aura 4 | applied at spawn (initial skill); no cast clip | poison 2 s | 3: pfx_zombie_poisonaura01 | 0.38 |

*5 further abilities (hero/boss-only or < 0.1 expected bodies) are in `roster.json` → `types[24].abilities`.*

### 26. `groble01` — Groble ~ Frost Clan Warrior / Groble ~ Frost Clan Tracker / Groble ~ Frost Clan Scavenger · 1.7 bodies

Lead `records/creatures/enemies/groblefrost_b01.dbr` · 3 records / 1 meshes · role mix trash 1.7 · family Beastkin · radius×scale 0.48–0.59 m · run 3.21–3.69 m/s · melee 100% · weapon unarmed, Ranged2h, Axe · p05 0

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| basic | `groble_froststrikes` | melee (charge) | 2.68 | — | — | `groble01_sword1h_attack_a01` 46f · rel f15 (0.5 s) *inf* | bleeding 3 s | 12: pfx_savagery_stack01, pfx_savagery_stack02 | 0.66 |
| tree_attack | `groble_explosiveicewps` | melee | 2.65 | — | 3.5 | `groble01_crossbow_attack_01` 31f · rel f3 (0.1 s) *inf* | — | 5: pfx_wpattack_cold_flight, pfx_iceexplosion01 | 0.52 |

### 27. `hero01_sword1h` — Haunted Champion / Ixall, Phantom of the Korvan Wastes / Horvald Shieldbreaker / Develos Ondal · 1.59 bodies

Lead `records/creatures/enemies/ghost_b03.dbr` · 6 records / 4 meshes · role mix trash 1.31, champion-hero 0.16, nemesis 0.12 · family Undead · radius×scale 0.35–0.76 m · run 1.93–3.21 m/s · melee 84% · weapon Sword · p05 0

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| special1 | `ghost_bladearc` | melee | 2.44–2.48 → **0–2.48** [Short] | — | — | `hero01_sword1h_skill_arcattack01` 29f ×1.4 · rel f14 (0.47 s) | — | 4: pfx_brutalimpact01 | 1.35 |
| basic | `ghost_cadence` | melee (charge) | 5.94 | — | — | `hero01_sword1h_skill_cadence01` 23f · rel f12 (0.4 s) | — | 7: pfx_ghost_cadenceauraa, pfx_ghost_cadenceaurab | 1.31 |
| basic | `eldritch2_eldritchbreath` | aoe (wave / cone) | 6.35 | — | wave 13 long, 2.5→2.5 wide | `hero01_sword1h_skill_eldritchbreath_a01` 41f · rel f21 (0.7 s) | poison 2 s | 1: eldritchbreathfx01 (clip) | 0.12 |
| special1 | `eldritch2_nullificationeye` | projectile | 16.6 | 14 m/s · r 0.3 | 3 | `hero01_sword1h_spellattack_b01` 19f · rel f10 (0.33 s) *inf* | fire 5 s | 10: pfx_elementaldispelbolt_flight, pfx_elementaldispelbolt_impact | 0.12 |
| special2 | `eldritch2_eldritcheyesnova` | projectile (ring / nova) | 16.6 → **0–9.1** [Short] | 15 m/s · r 0.4 | 0.25 | `hero01_sworddw_skill_summon_a01` 23f ×0.7 · rel f15 (0.5 s) | poison 2 s | 7: pfx_eyeorbital01_acid_flight, pfx_cultist_poisonbolt_impact01 | 0.12 |

*10 further abilities (hero/boss-only or < 0.1 expected bodies) are in `roster.json` → `types[26].abilities`.*

### 28. `heroine01_gun2h` — Haunted Noble / Agalla Varos ~ Regenerator · 1.58 bodies

Lead `records/creatures/enemies/ghost_b01.dbr` · 2 records / 1 meshes · role mix trash 1.54 · family Undead · radius×scale 0.35–0.39 m · run 1.93 m/s · projectile 99% · weapon Ranged2h · p05 0

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| special1 | `ghost_phantomblade` | projectile (burst) | 16.19–16.23 → **4.69–16.23** [Medium] | 30 m/s · r 0.1 | — | `heroine01_sword1h_skill_knifethrow01` 19f · rel f10 (0.33 s) | runspeed 3 s | 7: pfx_ghostdagger_flight, pfx_phantomblade1_impact | 1.58 |

*1 further abilities (hero/boss-only or < 0.1 expected bodies) are in `roster.json` → `types[27].abilities`.*

### 29. `hero01_sword2h` — Haunted Champion / Baullos Gar ~ Electrified / Senal Thandris ~ Corrupted / Stormbane ~ Electrified · 1.43 bodies

Lead `records/creatures/enemies/ghost_b04.dbr` · 4 records / 1 meshes · role mix trash 1.31, champion-hero 0.11 · family Undead · radius×scale 0.35–0.39 m · run 1.93 m/s · melee 97% · weapon Mace2h · p05 0

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| basic | `ghost_cadence` | melee (charge) | 5.94–5.98 | — | — | `hero01_sword2h_skill_cadence_a01` 25f ×1.2 · rel f12 (0.4 s) | — | 7: pfx_ghost_cadenceauraa, pfx_ghost_cadenceaurab | 1.43 |
| special1 | `ghost_bladearc` | melee | 2.44–2.48 → **0–2.48** [Short] | — | — | `hero01_sword2h_skill_arcattack_a01` 26f ×1.25 · rel f11 (0.37 s) | — | 4: pfx_brutalimpact01 | 1.43 |

*3 further abilities (hero/boss-only or < 0.1 expected bodies) are in `roster.json` → `types[28].abilities`.*

### 30. `golembone_phase01` — Skeletal Monstrosity / Ilgorr, the Eternal / Skeletal Gargantuan / Grum ~ Diseased · 1.14 bodies

Lead `records/creatures/enemies/skeletalgolem_c01.dbr` · 9 records / 6 meshes · role mix trash 0.61, champion-hero 0.28, boss 0.25 · family Undead · radius×scale 0.9–1.12 m · run 4.33–4.97 m/s · aoe 46% · buff 45% · summons on 22% of bodies · weapon unarmed · p05 0

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| special1 | `skeletalgolem_boneprison` | buff | 2.99–3.21 → **6.24–3.21** [Long] | — | 1/3 | `golembone_phase01_selfbuff_a01` 31f · rel f15 (0.5 s) *inf* | runspeed 2 s; field/buff 2–2.6 s | 5: pfx_boneprison_expire01 | 1.1 |
| special2 | `skeletalgolem_doublestrike` | aoe (wave / cone) | 10.74–10.96 → **0–5.46** [Short] | — | wave 8 long, 3→5 wide | `golembone_phase01_specialattack_a01` 81f ×1.3 · rel f25 (0.83 s) | — | 2: dark_cast_fx (clip), bloodarc_fx01 (clip) | 0.89 |
| special2 | `ilgorr_doublestrike` | aoe (wave / cone) | 10.89 → **0–5.39** [Short] | — | wave 10 long, 3→6 wide | `golembone_phase01_specialattack_a01_sunder` 81f · rel f25 (0.83 s) | damagemult 3 s; defensiveability 3 s; life 5 s; totalspeed 3 s | 3: sunder_cast_fx (clip), sunder_overheadcast_fx (clip) | 0.25 |
| initial | `diseased_diseasecloud` | aura (toggled) | aura | — | 4 · aura 4 | applied at spawn (initial skill); no cast clip | poison 2 s | 3: pfx_zombie_poisonaura01 | 0.12 |
| special4 | `diseased_gascloud` | projectile (lobbed area) | 16.96 → **6.46–16.96** [Long] | — m/s · r 0.5 | 3 | `golembone_phase01_throw_a01` 61f · rel f26 (0.87 s) *inf* | offensiveability 2 s; poison 2 s; field/buff 10 s | 4: pfx_poisoncloud_01 | 0.12 |

*9 further abilities (hero/boss-only or < 0.1 expected bodies) are in `roster.json` → `types[29].abilities`.*

### 31. `aetherialfleshshaper` — Fleshweaver Haraxis / Fleshshaper Hinissius / Blazragarus / Fleshweaver Krieg · 1.02 bodies

Lead `records/creatures/enemies/boss&quest/aetherialfleshshaper_haraxis.dbr` · 14 records / 7 meshes · role mix boss 0.75, champion-hero 0.27 · family Aetherial · radius×scale 0.54–0.82 m · run 3.21–3.85 m/s · aoe 43% · projectile 43% · summons on 76% of bodies · weapon unarmed · p05 0

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| tree_attack | `fleshshaperharaxis_aetherblaze` | projectile (lobbed area) | 6.15 | — m/s · r 0.5 | 4 | `aetherialfleshshaper_attack_a02` 41f · rel f12 (0.4 s) *inf* | field/buff 6 s | 5: pfx_aetherfire_large | 0.5 |
| basic | `aetherialfleshshaper_aetherfirewave` | aoe (wave / cone) | 10.38 | — | wave 15 long, 2→2.5 wide | `aetherialfleshshaper_roar_a01` 51f · rel f22 (0.73 s) | — | 2: pfx_aetherfirewave_path01 | 0.27 |
| basic | `fleshshaperharaxis_aetherfirewave` | aoe (wave / cone) | 10.4 | — | wave 15 long, 2→2.5 wide | `aetherialfleshshaper_roar_a01` 51f · rel f22 (0.73 s) | — | 2: pfx_aetherfirewave_path01 | 0.25 |
| special1 | `fleshshaperharaxis_aetherfirewavetriple` | aoe (wave / cone) | 10.4 → **0–10.4** [Medium] | — | wave 15 long, 2→2.5 wide | `aetherialfleshshaper_roartriple_a01` 51f · rel f16 (0.53 s) | — | 3: pfx_aetherfirewave_path01 | 0.25 |
| special2 | `fleshshaperharaxis_aetherboltnova` | projectile (ring / nova) | 6.15 → **0–6.15** [Short] | 9 m/s · r 0.5 | — | `aetherialfleshshaper_roartriple_a01` 51f · rel f16 (0.53 s) | — | 8: pfx_aethermissile_flight01, pfx_aethermissile_impact01 | 0.25 |

*27 further abilities (hero/boss-only or < 0.1 expected bodies) are in `roster.json` → `types[30].abilities`.*

### 32. `chthonianherald` — Chthonian Herald / Chthonian Portent / Nyarlathon, Herald of Annihilation / Chthonian Omen · 1 bodies

Lead `records/creatures/enemies/chthonianherald_a01.dbr` · 8 records / 3 meshes · role mix trash 0.69, champion-hero 0.17, nemesis 0.15 · family Chthonic · radius×scale 0.8–1.06 m · run 3.21–3.53 m/s · projectile 69% · aoe 22% · weapon unarmed · p05 0

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| chain_initial | `chthonianherald_teleport` | aoe (teleport) | 16.89 | — | 4.5 · wave 16 long, —→— wide | `chthonianherald_teleport_a01` 21f · rel f19 (0.63 s) | defensiveability 5 s; offensiveability 5 s | 7: pfx_chaoscastteleport_01, pfx_teleportchaos_radius_01 | 0.62 |
| chain_next | `chthonianherald_unleashchaoschannel` | projectile (fan) | 10.89 | 16 m/s · r 0.2 | 2 | `chthonianherald_channelforwards_a01` 121f · rel f37 (1.23 s) | — | 11: pfx_chaosball_chthonic_impact01, pfx_chaosball_chthonic_flight01 | 0.62 |
| special1 | `chthonianherald_triplechaosblast` | projectile | 16.64–16.8 → **0–16.8** [Long] | 6 m/s · r 0.6 | 2 | `chthonianherald_rearandtriplecast_a01` 93f · rel f32 (1.07 s) | — | 10: pfx_chaosball_chthonic_impact01, pfx_chaosball_chthonic_flight01 | 0.54 |
| basic | `chthonianherald_chaosblast` | projectile | 16.8–16.89 | 6 m/s · r 0.6 | 2 | `chthonianherald_basicspell_a01` 35f · rel f14 (0.47 s) *inf* | — | 10: pfx_chaoscastfastsoft_01, pfx_chaosball_chthonic_impact01 | 0.52 |
| basic | `chthonianherald_chaosblast_weak` | projectile | 16.64 | 6 m/s · r 0.6 | 2 | `chthonianherald_basicspell_a01` 35f · rel f14 (0.47 s) *inf* | — | 10: pfx_chaoscastfastsoft_01, pfx_chaosball_chthonic_impact01 | 0.34 |

*13 further abilities (hero/boss-only or < 0.1 expected bodies) are in `roster.json` → `types[31].abilities`.*

### 33. `aetherialcolossus` — Galakros, the Mountain / Crognoth, the Blazing Vanguard / Stormtitan ~ Electrified / Thunderfist ~ Electrified · 0.92 bodies

Lead `records/creatures/enemies/boss&quest/aetherialcolossus_galakros.dbr` · 12 records / 6 meshes · role mix boss 0.5, champion-hero 0.42 · family Aether Corruption · radius×scale 1.2–1.35 m · run 3.53 m/s · projectile 37% · melee 30% · aoe 27% · summons on 15% of bodies · weapon unarmed · p05 0

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| special1 | `galakros_poisongrenadeburst` | projectile (fan) | 20.19 → **5.69–13.69** [Medium] | 16 m/s · r 0.1 | 2.5 | `aetherialcolossus_cannonshot_a01_sunder` 38f ×0.75 · rel f11 (0.37 s) | damagemult 3 s; poison 3 s | 8: pfx_acidorb01_lg_flight, pfx_acidorb01_lg_impact | 0.5 |
| special2 | `galakros_poisonslam` | aoe | 6.94 → **0–6.94** [Short] | — | 8 | `aetherialcolossus_attackspecial_a01` 71f · rel f43 (1.43 s) | poison 2 s | 5: pfx_troll_poisonrift_radius | 0.5 |
| special3 | `galakros_roar` | aoe | 6.94 → **0–6.94** [Short] | — | 8 | `aetherialcolossus_roar_a01` 66f · rel f25 (0.83 s) | totalspeed 3 s; ttl 30 s | 3: pfx_yeti_howl_01 | 0.5 |
| special4 | `galakros_vilecharge` | melee (charge) | 3.44 → **9.69–3.44** [Long] | — | — | `aetherialcolossus_charged_end_a01` 41f · rel f2 (0.07 s) | defensiveability 5 s | 5: pfx_acidstrike, blitz1_warmuploop | 0.5 |
| special5 | `galakros_poisonstrike` | melee | 3.44 → **0–3.44** [Short] | — | — | `aetherialcolossus_attackspecial_a01` 71f · rel f43 (1.43 s) | — | 4: pfx_acidstrike | 0.5 |

*26 further abilities (hero/boss-only or < 0.1 expected bodies) are in `roster.json` → `types[32].abilities`.*

### 34. `wight01a` — Iglus Bloodmonger ~ Swift / Alluc the Thirster ~ Vampiric / Raddoth, Lord Hierophant · 0.69 bodies

Lead `records/creatures/enemies/hero/wight_h01.dbr` · 5 records / 2 meshes · role mix champion-hero 0.59, nemesis 0.1 · family Undead · radius×scale 0.33–0.78 m · run 3.21 m/s · aoe 84% · buff 11% · weapon Sword2h · p05 0.5

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| special2 | `wight_charge` | aoe (charge) | 19.16–19.62 → **6.66–19.62** [Long] | — | 2.5 · wave 16 long, —→— wide | `wight01a_attackspecial_charge_attack_01a` 46f · rel f3 (0.1 s) | — | 6: pfx_bloodstrike, pfx_chargetrail_deathly_01 | 0.69 |
| dying | `wight_deathrelease` | aoe | on death | — | 4 | fires at death (death clip) | — | 3: pfx_generic_novaspectral_01 | 0.59 |
| special1 | `wight_deathwind` | aoe | 5.91–5.94 → **0–3.69** [Short] | — | 6 | `wight01a_attackspecial_whirlwind_01a` 156f · rel f25 (0.83 s) | — | 8: pfx_whirlwinddeathly_lg01_loop | 0.59 |
| initial | `vampiric_vampireaura` | aura (toggled) | aura | — | 12 · aura 12 | applied at spawn (initial skill); no cast clip | — | 5: pfx_vampiricaura_self01, pfx_vampiricaura_other01 | 0.29 |
| special2 | `vampiric_vitalitywave` | aoe (wave / cone) | 16.16–16.19 → **0–3.69** [Short] | — | wave 16 long, 2→3.5 wide | `wight01a_attackbasic_melee_01a` 66f · rel f30 (1 s) *inf* | — | 2: pfx_spectralwave_path01 | 0.29 |

*5 further abilities (hero/boss-only or < 0.1 expected bodies) are in `roster.json` → `types[33].abilities`.*

### 35. `dreadguard_sword2h` — Grul'Thunn of the Crimson Tides / Zagal'Udal ~ Electrified / Wallan'Siin / Serethal'Siin · 0.68 bodies

Lead `records/creatures/enemies/boss&quest/chthoniantyrant_grulthunn.dbr` · 12 records / 4 meshes · role mix boss 0.5, champion-hero 0.18 · family Chthonic · radius×scale 0.6–0.96 m · run 3.53–3.85 m/s · aoe 85% · projectile 14% · weapon Axe2h · p05 0

| slot | skill | kind | GD fire range m (PACK V38-GR2) → with band, centre m | projectile speed · body r | AoE r m | clip · frames · release | DoT / field | VFX refs (n: key pfx) | bodies using |
|---|---|---|---|---|---|---|---|---|---|
| special1 | `grulthunn_bloodcleaves` | aoe (wave / cone) | 10.71 → **0–4.21** [Short] | — | wave 9 long, 3→6 wide | `dreadguard_sword2h_attackspecial_b01_vitality` 60f · rel f22 (0.73 s) | bleeding 3 s | 2: swipevitality02b_r_fx (clip), swipevitality02b_l_fx (clip) | 0.5 |
| special2 | `grulthunn_chargethrough` | aoe (charge) | 19.71 → **7.21–17.21** [Long] | — | 3.5 · wave 12 long, —→— wide | `dreadguard_sword2h_charge_01` 33f · rel f4 (0.13 s) | bleeding 3 s | 6: pfx_rush_hit_vitality_01, pfx_chargetrail01_vitality | 0.5 |
| special3 | `grulthunn_groundpound` | aoe (wave / cone) | 10.71 → **0–10.21** [Medium] | — | wave 18 long, 3→4 wide | `dreadguard_sword2h_groundpound_sunder_01` 101f · rel f20 (0.67 s) | damagemult 5 s | 10: pfx_spikesground_vitality_appearance01 | 0.5 |
| special4 | `grulthunn_whirlwind` | aoe | 6.46 → **0–4.21** [Short] | — | 5.5 | `dreadguard_sword2h_whirlwindcast_01` 121f · rel f42 (1.4 s) | bleeding 2 s; defensivereduction 3 s | 6: pfx_whirlwindvitality_lg01_loop, pfx_whirlwindvitality_lg01_cast | 0.5 |
| special3 | `chthonianwarrior_chaosbolt` | projectile (burst) | 16.44–16.8 → **6.94–16.8** [Long] | 40 m/s · r 0 | 1.5 | `dreadguard_sword2h_castattackburst_a01` 49f · rel f22 (0.73 s) | — | 6: pfx_cultist_chaosbolt_flight01, pfx_dmgabs_chaos_01 | 0.18 |

*17 further abilities (hero/boss-only or < 0.1 expected bodies) are in `roster.json` → `types[34].abilities`.*

## E. Summoned bodies: not in the count, on screen anyway

These records are spawned by roster members' skills (`spawnObjects`), not by the wave pools, so none of them is in the body counts above. How many exist at once depends on fight length and the owner's AI, so it is **UNKNOWN**. The cap per owner is datamined (`petLimit`). *Owner exposure* is the expected bodies of the owners that can cast the summon. It is an exposure proxy, **not** a pet count *(INFERRED)*. In an earlier oracle generation, the high-occupancy board held 620 spawned pets against 183 roster kills (Lap F `D-I2-2`). So this layer may matter for concurrency. Not re-measured on v3.8. **Several summoned records are not creatures** but traps, totems and crystals (Ice Spike, Bramble Trap, Storm Conduit, Sentinel's Beacon, Obsidian Shard, Wendigo Totem). Those are static VFX objects, not rigs; the blank rig-clip cells mark the ones with no run or idle clip.

| summoned record | name | owner exposure (bodies) | owner rigs | petLimit / burst / ttl s (per owner skill) | mesh | rig clip |
|---|---|---|---|---|---|---|
| `livingplant_a01_summon` | Carnivorous Plant | 3.89 | golemswamp_phase01 | 3/1–3/20 | `carnivorousplant01a_p2` | `carnivorousplant01a_p1_combatidle_a01` |
| `swampcrab_a00_summon` | Ugdenbog Crabling | 2.93 | crabmonstrosity | 8/4/30 | `crabmonstrosity01b` | `crabmonstrosity_run_a01` |
| `trap_icespike_hero_a01` | Ice Spike | 1.71 | aetherialcorruption, aetherialimp, avian, basilisk … | 6/1/12–15 | `spikesice03a` | `aetherialwisp_run` |
| `wraith_b01_summon` | Spiteful Wraith | 1.7 | heroine01_unarmed, wendigo | 12/2/45; 4/2/40 | `wraith01a` | `wraith_run_a01` |
| `skeleton_a02_summon` | Skeletal Archer | 1.01 | golembone_phase01, hero01_sword1h, skeleton_01a, skeleton_01a_b | 4/2/30; 4/4/— | `skeleton_basedefault_01a` | `skeleton_01a_runfast` |
| `witchgodguardian_sentinel_crystal` | Sentinel's Beacon | 1 | hero01_unarmed | 5/1/25 | `trap_obsidiansentry01a_eldritch` | `` |
| `springscrab_a00_summon` | Calcified Crabling | 0.99 | crabmonstrosity | 8/4/30 | `crabmonstrosity01b` | `crabmonstrosity_run_a01` |
| `ghost_a01_summon` | Apparition | 0.94 | golembone_phase01, hero01_sword2h | 12/3/30; 4/4/— | `ghost_f_a01` | `heroine01_unarmed_run` |
| `skeleton_a01_summon` | Skeletal Warrior | 0.86 | hero01_sword1h, heroine01_gun2h, skeleton_01a, skeleton_01a_b | 4/2/30 | `skeleton_01a` | `skeleton_01a_runfast` |
| `aetherialbloater_b01_summon` | Aetherial Bileeater | 0.77 | aetherialcolossus, aetherialfleshshaper | 3/1/30 | `aetherialbloater01a` | `aetherialbloater_run_a01` |
| `skeleton_b02_knight_summon` | Skeletal Knight | 0.74 | skeleton_01a, skeleton_01a_b | 4/1/— | `skeleton_baseheavy_01a` | `skeleton_01a_runfast` |
| `trap_brambletrap_a01` | Bramble Trap | 0.74 | cannibal, crabmonstrosity, dranghoul_01, thornedhorrora01 … | 6/1/12–15 | `trap_vinesground6x_01a` | `` |
| `trap_lightningspike_hero_a01` | Storm Conduit | 0.67 | chthonianherald, crabmonstrosity, dreadguard_sword2h, thornedhorrora01 | 6/1/24–27 | `trap_lightningspike01a` | `` |
| `aetherialcorruption_b03_summon` | Fleshwarped Scorcher | 0.58 | aetherialbloater, aetherialcolossus, aetherialfleshshaper | 3/1/40; 8/2/30 | `aetherialcorruption01a` | `aetherialcorruption_run_a01` |
| `aetherialcorruption_b02_summon` | Fleshwarped Stormwalker | 0.52 | aetherialfleshshaper | 3/1/40; 8/2/40 | `aetherialcorruption01a` | `aetherialcorruption_run_a01` |
| `mindreaper_summon` | Ishtal, the Mind Reaper | 0.51 | hero01_unarmed | 2–4/2–4/9–15 | `eldritcharmor02a_fireboss` | `hero01_unarmed_run` |
| `beast_bloodpool` | Wendigo Totem | 0.51 | yeti | 4/1/12 | `anomalya02_sigil` | `` |
| `aetherialcorruption_c01_summon` | Fleshwarped Aberration | 0.5 | aetherialfleshshaper | 4/1/30; 8/2/40 | `aetherialcorruption01a` | `aetherialcorruption_run_a01` |
| `loghorrean_void` | Entropic Void | 0.5 | hero01_unarmed | 6/1/9–12 | `anomalya01` | `aetherialwisp_run` |
| `chthonianminion_b01_summon` | Chthonian Bloodletter | 0.5 | hero01_unarmed | 1–6/1–2/60 | `chthonianminion01` | `run_01` |
| `chthonicshard_zap_b01_summon` | Obsidian Shard | 0.5 | hero01_unarmed | 4/2–4/30 | `trap_obsidiansentry01b` | `` |
| `rimehorn_icespike_01` | Rime Spike | 0.5 | yeti | 4/2/12; 4–8/1/12 | `spikesice03a` | `aetherialwisp_run` |
| `chthonianservitor_a01_summon` | Chthonian Drone | 0.5 | chthonianservitor | 12/3/30 | `chthonianservitor01a` | `chthonianservitor_walk_a01` |
| `winddevil_01` | Wind Devil | 0.5 | heroine01_unarmed | 4/1/12 | `anomalya01` | `aetherialwisp_run` |
| `aetherialvanguard_crystal` | Aleksander's Shard | 0.5 | hero01_unarmed | 6/2/45 | `aethercrystals01_summon` | `aetherialwisp_run` |

*75 summoned records in all; the full list, with owners and abilities, is in `roster.json → summoned_bodies`.* Many of them reuse a Tier-1 rig (crablings use `crabmonstrosity`, Spiteful Wraith uses `wraith`, Fleshwarped summons use `aetherialcorruption`, the plant summon uses the plant), so they add bodies to rigs already built rather than new rigs.

---

## F. Open questions and knowledge gaps

| # | question | state | what would settle it |
|---|---|---|---|
| G-1 | Pet / summon concurrency on v3.8 | Summoned bodies are uncounted (§ E). In an earlier oracle they outnumbered roster kills about 3:1. | A SIM census of pet spawns per wave on the v3.8 driver (gamora), or footage counts. |
| G-2 | Pool player-level gates | `ABS-POOL-GATE-ENFORCEMENT`: 22 pool slots carry min/maxPlayerLevel (for example the Korvaak messenger `_02` maxPlayerLevel 70 vs `_02b` min 70). Following Lap V, this packet does **not** enforce them. If GD enforces them, the w159 p05 messenger is always `_02b`, and a few compositions shift. | Decode the picker's gate test in `Game.dll sub_103583d0`. |
| G-3 | Clip playback speed | Durations assume anim speed 1.0. The record and anim-table speed composition is UNDECODED (`RESID-D1-1`). Where an anim speed other than 1 is listed (for example the corruption spawn at 2.0), the true playback length may be the clip ÷ speed. The p05 rows already carry both limbs (`V38-AM3` D_short / D_long). | Decode the speed hop (D-1 residual). |
| G-4 | Monster height | No record carries a modelled height: `actorHeight` is the template default 2.0. The Lap F mesh AABB is mesh-space bind pose and implausible on humanoid npc meshes (0.42). **Height is UNKNOWN** for every type. | Read the skeleton's root-to-head bone span from the `.msh` or `.anm` bone tables (not decoded). |
| G-5 | Unbound special-anim refs | 168 of 1980 ability rows name a `skillSpecialAnimationName` the record's table does not carry (for example bloater `Charge`, Krieg `SpikeShoot`). GD's fallback in that case is not decoded. The card shows the class-default clip, marked *ref unbound*. A further 37 rows resolve only under another style prefix of the same table (DATAMINED, flagged in `roster.json`). | Decode `Skill::GetSpecialAnimation` / the anim-table lookup miss path. |
| G-6 | Weapon → anim-style prefix | For 64 records with an equipped weapon, the style prefix (`spear2h`, `axe2h`, `sHanded` …) is INFERRED from the weapon item Class. The other 402 are unarmed (DATAMINED). | Decode `Character::GetAnimationStyle` (or the equivalent) in `Game.dll`. |
| G-7 | Skeleton sharing | Rig families need the same clip directory and the same bone count (checked; it splits `chthonian/anm` into five bone counts and `wendigo/animations` into two). Bone *names* were not compared, so two equal-count rigs could still differ. | Decode the `.anm` bone-name table (the census read only the count). |
| G-8 | Projectile visual radius | `projectile body r` is the projectile entity's `actorRadius` (collision/body). The visual size is set by its `.pfx` and mesh `scale`, which are not decoded here. | A `.pfx` decode, or footage. |
| G-9 | Edition drift | Record fields are Ed IV. Clip frames and events are Ed III (census 2026-08-08). The range audit found Ed II vs Ed IV unchanged on 1,555 / 1,557 range fields. Clip content drift between III and IV is unchecked, because IV ships no `.arc`. | Re-census when an Ed IV `.arc` set is on disk. |
| G-10 | Rank-dependent values | Monster skill values that are per-rank arrays (DoT magnitudes, some burst counts) are given as min–max. The monster's skill level at tier 16 is not resolved here. | Evaluate `skillLevel{i}` equations at the Crucible charLevel (the pack's offense rows already did this for damage). |

---

## G. How the numbers were made

1. **Bodies.** I reproduced the Lap V count law (DECODED, `Game.dll sub_10357590`): one weighted pool per spawn point per wave; champions first; regulars uniform on [lo, max]; the weighted picker skips exhausted `limit`s and stops on an empty roster. I ran it over the 139 pool rows of waves 151–160 (`pm4v_roster_arithmetic.csv`) with the member weights, limits and families of the pack's `waves.json → pools.pool_member`. Monte Carlo used 40,000 trials. Every spawn point's mean matches Lap V's `e_bodies` within 0.015, and the band total is 172.04 (Lap V: 172.083).
2. **Records.** Every one of the 466 pool members was read from the Ed IV `.arz` (winner record). That gave: mesh, scale, radius, height, controller, speeds, equipped weapon (loot table → item Class), anim table, the style-prefix clip set, and every special-anim ref.
3. **Abilities.** Each ability is one row of the range audit's `range_audit_per_attack.csv`, the oracle's loaded slot set with pack row ids. Each is joined to its v3.8 fire-range row (`V38-GR2-*`) or aura correction (`V38-GR3-*`), then to its Ed IV skill record, its children (`buffSkillName`, `autoCastSkill` …) and its projectile record, and finally to its animation through `skillSpecialAnimationName → <prefix>SpecialAnimRef<n> → clip`.
4. **Clips.** Frame counts, `*Hit` and `PS*Start` callbacks and `CreateEntity` FX come from the Ed III `.anm` census. The census keys strip the `creatures/` prefix.
5. **VFX.** I collected every `records/fx/*.dbr`, `.pfx` and fx `.msh` reachable from the skill, depth ≤ 3. Clip VFX are listed separately.
6. **Types.** Records are grouped by their run clip (the idle clip for the plant), ordered by expected bodies, and cut cumulatively at 80 % and 95 %.

Instruments: `s1_composition.py` → `s2_records.py` → `s3_build.py` → `s4_emit.py` → `s5_readme.py`. They lived in the session scratchpad and are not committed; the logic is described above and the input digests are below.

**Inputs (sha256):**

- pack v3.8 waves.json: `~/Games/reincarnated-engine/src/reincarnated/output/kc2-model-pack-v3-E-s09-cp150-mech-v3p8-20261002_003532/model/waves.json` — `195cbec17e2e1206…`
- pack v3.8 monster_offense.json: `~/Games/reincarnated-engine/src/reincarnated/output/kc2-model-pack-v3-E-s09-cp150-mech-v3p8-20261002_003532/model/monster_offense.json` — `eb66f07b181c92b5…`
- pack v3.8 monster_kinematics.json: `~/Games/reincarnated-engine/src/reincarnated/output/kc2-model-pack-v3-E-s09-cp150-mech-v3p8-20261002_003532/model/monster_kinematics.json` — `3fa60b06b198dcde…`
- pack v3.8 projectiles.json: `~/Games/reincarnated-engine/src/reincarnated/output/kc2-model-pack-v3-E-s09-cp150-mech-v3p8-20261002_003532/model/projectiles.json` — `ed32ff8a648d2b3c…`
- pack v3.8 monsters.json: `~/Games/reincarnated-engine/src/reincarnated/output/kc2-model-pack-v3-E-s09-cp150-mech-v3p8-20261002_003532/model/monsters.json` — `3839322955b7d4af…`
- Lap V pm4v_roster_arithmetic.csv: `~/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/2026-08-15-kc2-pm4-lap-v-roster-decode/pm4v_roster_arithmetic.csv` — `991f75cfdb43ddff…`
- range audit range_audit_per_attack.csv: `~/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/2026-10-01-kc2-enemy-range-audit/range_audit_per_attack.csv` — `a9aeae9d69411bac…`
- range audit gdlib.py (arz reader): `~/Games/reincarnated-collaboration/agentic_orchestration/legolas/research/2026-10-01-kc2-enemy-range-audit/scripts/gdlib.py` — `ab9eaa025e01dcda…`
- Ed III anm census anm_index.json: `~/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/2026-08-08-kc2-threat-grammar-arz-boundary/anm_index.json` — `59919fe2f4e20446…`
- Ed III anm census anm_events.json: `~/Games/reincarnated-collaboration/agentic_orchestration/legolas/notes/2026-08-08-kc2-threat-grammar-arz-boundary/anm_events.json` — `82f431ba30f1d6fc…`
- tag text extract tags_all.json (Ed I/III text): `~/Games/reincarnated-collaboration/agentic_orchestration/legolas/scratch/2026-08-07-u8-tierwave/tags_all.json` — `97111a1f466fd504…`
- Lap F pm4_body_radii.csv (engine data/kc2): `~/Games/reincarnated-engine/data/kc2/pm4_body_radii.csv` — `80517e398f05432f…`
- Ed IV database.arz: `~/Games/vendor/grim-dawn-edition-IV-20260929/database/database.arz` — `68761caed0f5c6b1…`
- Ed IV GDX1.arz: `~/Games/vendor/grim-dawn-edition-IV-20260929/gdx1/database/GDX1.arz` — `a3d0917dbff0337a…`
- Ed IV GDX2.arz: `~/Games/vendor/grim-dawn-edition-IV-20260929/gdx2/database/GDX2.arz` — `e40df57744bf751c…`
- Ed IV GDX3.arz: `~/Games/vendor/grim-dawn-edition-IV-20260929/gdx3/database/GDX3.arz` — `a5ae5024515272f2…`
- Ed IV SurvivalMode.arz: `~/Games/vendor/grim-dawn-edition-IV-20260929/mods/survivalmode/database/SurvivalMode.arz` — `fdfa9cbf3324a191…`
- Ed IV SurvivalMode1.arz: `~/Games/vendor/grim-dawn-edition-IV-20260929/survivalmode1/database/SurvivalMode1.arz` — `e4635a0b9428b4a5…`
- Ed IV SurvivalMode2.arz: `~/Games/vendor/grim-dawn-edition-IV-20260929/survivalmode2/database/SurvivalMode2.arz` — `031c38dfb0e77576…`
- Ed IV SurvivalMode3.arz: `~/Games/vendor/grim-dawn-edition-IV-20260929/survivalmode3/database/SurvivalMode3.arz` — `d5e32852d99fbf68…`

Prior legolas packets relied on: range audit (`2026-10-01-kc2-enemy-range-audit/`), ambush semantics (`2026-10-01-crucible-ambush-semantics/`), centre spawn (`2026-10-01-crucible-spawn-p05/`), Lap V roster decode (`notes/2026-08-15-kc2-pm4-lap-v-roster-decode/`), Lap F body radii (`notes/2026-08-13-kc2-pm4-lap-f-body-radii/`), the Ed III animation census (`notes/2026-08-08-kc2-threat-grammar-arz-boundary/`).

*legolas · C-9 Graphic Arts · Crucible enemy roster packet · 2026-10-02*
