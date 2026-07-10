> **SUPERSEDED-BY-CANON (2026-07-10):** canonized verbatim + banner at
> `canonical/reap-die-rise-game/wc3-sc-custom-game-compendium.md` — read/edit THERE. This handoff
> original is retained as mobile-session lineage only.

# The WC3 & StarCraft Custom-Game Compendium

**Purpose:** exhaustive reference on the Blizzard custom-map ecosystem (StarCraft: Brood War UMS → Warcraft 3 → StarCraft 2 Arcade) for the Reap. Die. Rise. minigame template program. Design vocabulary, lineage claims, and the mapping to our taxonomy.
**On screenshots:** period screenshots are Blizzard-IP imagery and can't be reproduced here; this doc compensates with dense tables, and any genre can be rendered as an original anatomy diagram on request (one exists already: `reap-die-rise-endgame-mode-anatomy.svg`).
**Dates:** firm where history is settled; "~" where community memory is the only source. Authors named only where attribution is solid.

---

## 1. The Three Platforms

| Platform | Active era | Creation tool | Distribution | Persistence tech | Fate |
|---|---|---|---|---|---|
| **StarCraft: Brood War "UMS"** | 1998 → ~2011 West; Korea + niche to present | StarEdit (+ community SCMDraft); late-era **EUD exploits** unlocked absurd trigger power | Open Battle.net lobby list; map auto-transfers on join | Essentially none (per-session); EUD-era workarounds | **Remastered (2017) preserved ~99% of maps** — scene survives small but alive |
| **Warcraft 3 (RoC 2002 / TFT 2003)** | 2003–2010 golden age; alive today esp. Korea/China | **World Editor**: GUI triggers over JASS script, full asset library, hero/item/ability data all moddable | Open lobby list + auto-transfer; later **third-party host bots** (ENT, MakeMeHost, ~2011+) kept lobbies alive | **Save/load code strings** = serverless persistence → made ORPGs possible | Reforged (2020) broke the classic client & custom ecosystem — community fury; scene persists on community infra |
| **StarCraft 2 Arcade** | 2012 (patch 1.5) → present | Galaxy Editor (most powerful of the three) | **Curated, popularity-sorted Arcade** replaced the open lobby list | Bank files (real per-player persistence) | Rich-get-richer discovery; by Blizzard's own 2017 poll only **5% of SC2 players** counted Arcade as their primary mode; Premium (paid) maps added 2018 |

**Blizzard seeded each ecosystem with first-party exemplars:** WC3 shipped with **Warchasers** (dungeon-crawl RPG) and **Azure Tower Defense**; SC2's Blizzard arcade releases included **Left 2 Die**, **StarJeweled**, and **Aiur Chef**. The bundled maps taught audiences what "custom" meant.

---

## 2. Master Genre Map

| Genre | BW ur-maps | WC3 pillars | SC2 heirs | Core loop (one line) |
|---|---|---|---|---|
| AoS / MOBA | Aeon of Strife, Temple Siege | DotA → DotA Allstars; CHAOS (KR); Battle Tanks; Battleships | Aeon of Storms | Heroes + creep-wave lanes + base destruction |
| Tower Defense | Sunken/Turret/Bunker/Lurker D | Wintermaul, Element TD, Gem TD, Burbenog, Green Circle, Power Towers, Skibi's | Squadron TD | Static (or not) defenses vs. pathing waves |
| Send-TD "Wars" | (income-send protos) | Line Tower Wars, Wintermaul Wars | — | Defend your lane, spend to send at theirs |
| Hero-defends + send | — | **Hero Line Wars**, **Custom Hero Line Wars** | — | Piloted hero holds; income economy sends |
| Tug-of-war / auto-spawn | Desert Strike, Sandcastle Wars | **Castle Fight**, **Legion TD** | Nexus Wars, Desert Strike HotS → **Direct Strike** | Build spawners/fighters; armies auto-march & clash |
| Hero arena / brawl | Evolves | Angel Arena, **Warlock**, Pudge Wars, DBZ Tribute, Orc Gladiators, Hero Push | Monobattles (melee-variant) | Farm → team-fight → power-fantasy duels |
| Mass-army wars | Zone Control | **Footmen Frenzy**, Builders & Fighters, LOTR/Medieval Builder | Marine Arena | Auto-spawning armies + a hero; tier upgrades |
| Territory strategy | **Risk**, **Diplomacy** | Risk variants; Azeroth Wars, Lordaeron: The Aftermath, Dark Ages of Warcraft | — | Income-per-territory conquest; chat-rule politics |
| Co-op wave survival | Zombie Hotel, Protect Bob, Starship Troopers, Impossible scenarios | Enfo's Team Survival, Moo Moo, Special Forces, X Hero Siege, Helm's Deep | Night of the Dead, Undead Assault | Hold vs. escalating waves; loot/upgrade beats |
| Boss raid | — | **Impossible Bosses** | (raid-style arcade) | Pure boss-mechanics co-op, MMO-raid-as-map |
| Asymmetric predator / tag | Cat & Mouse, Jurassic Park | Sheep Tag, **Tree Tag**, Kodo Tag, **Vampirism**, **Island Defense**, Run Kitty Run | — | Hunter(s) vs. hiding/walling/teching survivors |
| Social deduction | **The Thing**, **Parasite** | Phantom | **Mafia**, Parasite 2 | Hidden roles; deduce the traitor before it's too late |
| Bounds / escape / precision | **Bounds** (thousands), Jail Break, Red Light Green Light, Run Zergling Run | Escape/maze maps | — | Obstacle-timing gauntlets; pure execution |
| Squad shooters / paintball | Sniper Elite, Team Fortress, V-TEC Paintball, 007 Arena, Counter-Strike ports | Special Forces | — | Small-unit PvP/PvE with RTS units as guns |
| RPG / ORPG | trigger RPGs | Warchasers; Twilight's Eve, Gaias Retaliation, TKoK, The Black Road, Sunken City | ARK Star; custom Campaign genre (2020) | Persistent heroes (save codes), dungeons, raids |
| Sandbox / roleplay | — | **Life of a Peasant (LOAP)**, Titan Land–style RP, Fantasy Life RP | — | Jobs, crime, houses, DM-spawned stories |
| Sports / party / ports | SCV Football, Zerg Soccer, Chess, Pac-Man, Mario Party | **Uther Party**, Tom & Jerry | StarJeweled, Aiur Chef, Nexus Word Wars | Minigame collections & genre ports |
| Autobattler (the second birth) | — | (Legion TD as bridge) | — (born in **Dota 2 customs**: Auto Chess, Jan 2019) | Draft + position; boards auto-fight |

---

## 3. Genre Dossiers

### 3.1 AoS → MOBA — the first genre-birth
The lineage: **Aeon of Strife** (BW, ~1999–2002) establishes heroes + lanes + creep waves. **Eul** ports the concept to WC3 as *Defense of the Ancients* (2003). After Eul steps back, variants merge into **DotA Allstars** (2004), led by **Guinsoo** (items/recipes, Roshan), then handed to **IceFrog** (~2005), whose relentless balance stewardship builds the competitive scene (Clan TDA, DotA-League, MYM). **Riot founds LoL around Guinsoo/Pendragon (2009); Valve hires IceFrog → Dota 2 (2013); HoN (2010).** A remix-culture map file became the century's biggest PC genre.

| Map | Platform | Era | Players | Loop | Legacy |
|---|---|---|---|---|---|
| Aeon of Strife | BW | ~1999 | 1–4 v AI → PvP | proto lanes/heroes | the ur-MOBA |
| Temple Siege | BW | mid-00s | 3v3 | spellcaster hero push | BW's flagship hero map, hosted for years |
| DotA (Eul) | WC3 RoC | 2003 | 5v5 | AoS with WC3 heroes | the fork that started it |
| **DotA Allstars** | WC3 TFT | 2004–10s | 5v5 | items, Roshan, 100+ heroes | → LoL, Dota 2, HoN; esports at global scale |
| CHAOS | WC3 (KR) | mid-00s | 5v5 | Korea's dominant AoS | parallel pro scene; Korea's DotA |
| Battle Tanks / Battleships | WC3 (EU) | mid-00s | teams | vehicle/naval AoS with shop economies | AoS skeleton, re-skinned loop |
| Fight of Characters / Bleach vs One Piece / DotA IMBA | WC3 KR/CN | late 00s | 5v5 | anime-hero AoS / modifier-DotA | regional giants; IP-remix culture at scale |

### 3.2 Tower Defense
TD as a *genre* crystallized inside BW customs — the census of what's still hosted reads like a taxonomy of its own: "God tower, bunker, sunken, turret, tank, marine, lurker, cannon" defenses. WC3 turned it into an art form.

| Map | Platform | Era | Loop | Innovation |
|---|---|---|---|---|
| Sunken D / Turret D family | BW | ~1999+ | co-op static defense | the genre's cradle |
| Wintermaul / Warcraft Maul | WC3 | 2003+ | classic maze TD | the WC3 baseline; "Maul" became the local word for TD |
| **Element TD** | WC3 | ~2006 | element-combo towers | build theory as depth → Element TD 2 standalone |
| Gem TD | WC3 | mid-00s | random gems → maze + combine | RNG-draft TD |
| Burbenog TD | WC3 | mid-00s | 4-player role TD | co-op role specialization; a most-hosted staple for a decade |
| Power Towers | WC3 | late 00s | energy-network towers | resource topology as mechanic |
| Poker Defense | BW (KR) | 00s | poker hands summon units | genre mash; Korean UMS icon |
| **Squadron TD** | SC2 | 2011+ | towers BECOME units each round, + send | TD×tug hybrid; long the top-played NA arcade map |

### 3.3 Send-TD Wars & Hero Line Wars
The **send economy** — spend income to attack the other lane, sends raise income — is this family's invention, and it's the direct ancestor of our Rung 2.

| Map | Platform | Loop | Note |
|---|---|---|---|
| Line Tower Wars | WC3 | maze your lane; send at 7 rivals | send-economics formalized |
| Wintermaul Wars | WC3 | team TD + send | |
| **Hero Line Wars** | WC3 | piloted hero holds; income sends | RDR Rung 2's literal ancestor |
| **Custom Hero Line Wars** | WC3 | assemble-your-hero from ability pools + line wars | kit-drafting bolted onto HLW — the teenagers pre-ran our Rung 2 + Rung 3 hybrid |

### 3.4 Tug-of-war / auto-spawn — the autobattler taproot
Players build; armies fight themselves. The purest macro genre, and the through-line to 2019's second genre-birth.

| Map | Platform | Era | Loop | Legacy |
|---|---|---|---|---|
| Desert Strike | BW → SC2 | 00s → 2010s | build economy; waves auto-march | the family's namesake |
| **Castle Fight** | WC3 (EU icon) | ~2007 | build spawner buildings ONLY | pure tug; still hosted daily in 2016 lobby logs |
| Nexus Wars | SC2 | 2010+ | SC2's Castle Fight | arcade evergreen |
| **Direct Strike** | SC2 | 2018 | positioning + economy tug | evolved from "Desert Strike HotS" by Tya; launched the **Premium Arcade** at $4.99 with rev-share, Sabotage & Switch modes |
| **Legion TD** | WC3 | ~2008–09 | build fighters that auto-battle + send | TD×tug bridge → Legion TD 2 standalone (2017+) |
| **→ Auto Chess** | Dota 2 custom | **Jan 2019** | draft/position; boards auto-fight | Drodo Studio's map birthed the autobattler genre: TFT (Jun 2019), Underlords, Hearthstone Battlegrounds — the substrate's SECOND genre-birth, 16 years after DotA |

### 3.5 Hero arena / physics brawl
| Map | Platform | Loop | Note |
|---|---|---|---|
| Angel Arena | WC3 | farm creeps → team-fight arena | the arena staple |
| **Warlock** | WC3 | AOE-knockback FFA on shrinking lava | physics-skill brawl; RDR template 5.7's ancestor |
| Pudge Wars | WC3 | hook duels, nothing else | single-mechanic mastery |
| DBZ Tribute | WC3 | asymmetric factions, radically different power-up paths | licensed progression-brawler, remembered as a design standout |
| Evolves | BW (+WC3 remakes) | kills evolve your species | kill-streak evolution arena |
| Orc Gladiators / Hero Push | WC3 | gladiator waves / push brawls | verified perennials in lobby logs |
| Monobattles | SC2 | melee, but each player builds ONE unit type | constraint-variant of the base game |

### 3.6 Mass-army wars
| Map | Platform | Loop | Note |
|---|---|---|---|
| **Footmen Frenzy** | WC3 | 3v3v3v3 auto-spawn armies + hero + spawn-tier upgrades | "Footies"; RDR template 5.4's ancestor; Custom Hero Footies variant exists |
| Marine Arena | SC2 | SC2's footies | evergreen |
| Zone Control | BW | spawning armies auto-fight over claimable zones | literally RDR template 5.10, twenty years early |
| Builders & Fighters / LOTR Builder / Medieval Builders | WC3 | asymmetric roles: builders supply, fighters spend | the builder-war genre — huge in lobby logs, rarely written about |

### 3.7 Territory strategy & diplomacy
| Map | Platform | Loop | Note |
|---|---|---|---|
| Risk | BW + WC3 | territory income conquest | board-game port at RTS scale; a BW top-5 genre to this day |
| Diplomacy ("Diplo") | BW + WC3 | negotiated grand strategy; rules enforced by chat | politics as the actual game |
| Azeroth Wars / Lordaeron: The Aftermath / Dark Ages of Warcraft | WC3 | lore-faction grand strategy with scripted events | WC3's Paradox-likes; LtA still actively hosted |
| Helm's Deep / LotR sieges | BW + WC3 | scripted scenario siege defense | cinematic set-piece genre |

### 3.8 Co-op wave survival & sieges — RDR Rung 1's family
| Map | Platform | Loop | Note |
|---|---|---|---|
| Zombie Hotel / Protect Bob / Starship Troopers | BW | hold vs. hordes | zombie survival topped BW charts |
| Impossible scenarios | BW | brutal holds vs. extreme CPU | a named BW genre of its own |
| **Enfo's Team Survival** | WC3 | team lane-hold vs. escalating waves, hero + support roles | the Horde Survival ancestor |
| Moo Moo | WC3 | early co-op hero defense | proto of the form |
| Special Forces | WC3 | squad objective missions vs. waves | co-op "shooter" energy in RTS clothes |
| **X Hero Siege** | WC3 | 8 players, 4 lanes, boss events, "double hero" chaos mode | the beloved power-fantasy siege — remembered as peak LAN insanity |
| **Impossible Bosses** | WC3 | co-op raid of pure boss mechanics | RDR Boss Rush (5.5) ancestor; MMO-raid-as-map |
| Night of the Dead / Undead Assault | SC2 | class/XP tactical zombie survival | the family's SC2 apex |

### 3.9 Asymmetric predator / tag / builder-defense
| Map | Platform | Loop | Note |
|---|---|---|---|
| Cat and Mouse | BW | mice build & hide; cats hunt | BW classic, still in the hosted census |
| Sheep Tag | WC3 | sheep wall with farms; shepherds hunt | speed-building as evasion |
| **Tree Tag** | WC3 | hide AS a tree among trees | prop-hunt prefigured, years before Garry's Mod |
| Vampirism (Fire/Beast/...) | WC3 | humans wall + tech; vampire feeds & scales | the arms-race asymmetry |
| **Island Defense** | WC3 | one Titan vs. a lobby of builders | the deep asymmetric builder-v-predator; 11-player lobbies |
| Jurassic Park | BW | survive the island | hide-and-survive scenario |
| Run Kitty Run | WC3 | co-op dodge gauntlet | pure evasion |

### 3.10 Social deduction — the hidden-role lineage
| Map | Platform | Loop | Legacy |
|---|---|---|---|
| The Thing | BW | infected among the crew | digital hidden-role proto |
| Parasite (→ Parasite 2) | BW → SC2 | alien puppets a crew member on a ship | the Among Us shape, a decade early |
| Phantom | WC3 | phantoms drain the team's gold; humans deduce | economy-tell deduction |
| Mafia | SC2 | classic Werewolf structure | **Town of Salem grew out of the SC2 Mafia community** — a custom map became a commercial social-deduction hit |

### 3.11 Bounds / escape / precision & squad shooters
BW's **bound** maps — explosion-timing obstacle runs — existed in the *thousands*; with obstacle/party races (Jail Break, Red Light Green Light, Run Zergling Run) they formed BW's execution-skill culture. WC3's escape/maze maps carried it forward. Parallel: BW's paintball/sniper squad-PvP family (Sniper Elite, Team Fortress, V-TEC Paintball, 007 Arena, Counter-Strike ports) — shooters built from RTS parts.

### 3.12 RPG / ORPG — persistence without servers
WC3's **save/load code strings** (your hero serialized into a chat code you paste next session) enabled true ORPGs on infrastructure that had none.

| Map | Platform | Note |
|---|---|---|
| Warchasers | WC3 (Blizzard-bundled, 2002) | the first-party seed RPG |
| Twilight's Eve ORPG | WC3 | job/class systems, endgame grinds |
| **Gaias Retaliation ORPG** | WC3 | the quality benchmark; developed and hosted for well over a decade, still maintained |
| TKoK (Kingdom of Kaliron) | WC3 | raid-tier boss design |
| The Black Road / Sunken City | WC3 | ORPG breadth / co-op dungeon crawl |
| ARK Star | SC2 (2018) | premium turn-based RPG by "Pirate" (Rock the Cabinet winner) |
| Custom Campaigns | SC2 (2020 Arcade genre) | map-to-map loading; co-op campaigns |

### 3.13 Sandbox / RP & party collections
**Life of a Peasant (LOAP)**: jobs, crime, cops, houses — GTA-roleplay culture inside WC3, prefiguring the Roblox/GTA-RP mode of play. DM-driven RP maps (Titan Land family, "Fantasy Life RP", even "Film Maker" lobbies) turned WC3 into a stage. **Uther Party** is the load-bearing one for us: a roulette of dozens of 60-second minigames — a minigame-of-minigames, i.e., RDR template 5.11's wrapper, shipped by hobbyists circa 2004. BW's port culture (SCV Football, Zerg Soccer, Chess, Pac-Man, Mario Party) and SC2's first-party novelties (StarJeweled, Aiur Chef, typing-defense Nexus Word Wars) round out the party shelf. Cultural substrate note: BW's **BGH/Fastest money-map + comp-stomp** scene was the casual on-ramp that fed all of this.

---

## 4. Innovation → Descendant Lineage

| Custom-map innovation | Where | Commercial descendant | Gap |
|---|---|---|---|
| Heroes + lanes + creeps | AoS (BW ~1999) → DotA Allstars (WC3 2004) | LoL (2009), HoN (2010), Dota 2 (2013) — the MOBA industry | ~6–10 yrs |
| Draft + auto-fighting boards | Legion TD (WC3) → **Auto Chess** (Dota 2 custom, Jan 2019) | TFT (Jun 2019), Underlords, HS Battlegrounds | **5 months** |
| Element/fighter TD depth | Element TD, Legion TD (WC3) | Element TD 2, Legion TD 2 (standalones) | — |
| Tug-of-war | Desert Strike (BW) | Direct Strike premium (2018, rev-share) | — |
| Hide-as-object | Tree Tag (WC3) | Prop Hunt family | — |
| Hidden-role deduction | The Thing / Parasite (BW), Mafia (SC2) | Town of Salem (from SC2 Mafia community); Among Us era | — |
| Survival-crafting PvPvE | Island Troll Tribes (WC3) | the survival-craft genre's shape | — |
| Life-sim roleplay servers | LOAP (WC3) | Roblox RP / GTA-RP culture | — |
| Serverless persistence | save/load codes (WC3 ORPGs) | account-progression norms | — |
| Rule flags at runtime | DotA's chat modes (-ap, -sd, -random, -em) | our packet params, two decades early | — |
| Third-party distribution | host bots (ENT, MakeMeHost) | community infra outliving the platform | — |
| Creator monetization | SC2 Premium Arcade (2018) | UGC rev-share models | arrived after the audience left |

**The headline:** the substrate birthed billion-dollar genres **twice** — MOBA (2003) and autobattler (2019) — and the second time the industry cloned it in *months*, not years. Shared engine + shared asset vocabulary + forkable rule layer + zero-friction lobbies = a genre foundry.

---

## 5. Why It Worked, Why It Died, What Survived

**Worked:** (1) shared combat vocabulary — every map reused units/heroes the player already knew, so a new map was 90% familiar; (2) zero-friction distribution — the map transferred when you joined the lobby; (3) a captive audience already owning the engine; (4) forkability — maps were files; DotA itself was a merge of forks; (5) casual lobby culture — short sessions, novelty-browsing, nobody tryhard at a map that's a week old.

**Died (where it died):** SC2 replaced the open lobby list with a curated, popularity-sorted Arcade — rich-get-richer discovery that strangled the long tail; contemporaries called BW's ease of testing/distribution the thing SC2 "failed to carry on." Blizzard's own poll put Arcade at 5% primary interest by 2017. Reforged (2020) then broke WC3's working ecosystem overnight — while StarCraft: Remastered (2017), which changed nothing, preserved ~99% of BW maps and its scene.

**Survived:** BW UMS is still hosted (a 2025 community census still ranks its live genres); WC3 customs persist on community hosting, with Korea and China running strong regional scenes (Korean random-defense maps, Bleach vs One Piece, DotA descendants). The energy of the *mass* audience migrated to Roblox and Fortnite Creative.

---

## 6. Mapping to the RDR Template Taxonomy

| RDR template | Direct ancestors | Notes |
|---|---|---|
| 5.1 Horde Survival | Enfo's, Moo Moo, zombie-survival family, Impossible scenarios | endgame candidate; the genre's deepest well |
| 5.2 Hero Line Wars | Hero Line Wars, Line Tower Wars | our Rung 2 is a faithful revival |
| 5.3 Kit-Draft Gauntlet | **Custom Hero Line Wars**, Custom Hero Wars/Footies/Survival | the "custom hero" modifier family = kit-drafting, proven |
| 5.4 Footmen Frenzy | Footmen Frenzy, Marine Arena | |
| 5.5 Boss Rush | Impossible Bosses, X Hero Siege | |
| 5.6 Tower/Hero Defense | Wintermaul→Element/Gem/Burbenog; Squadron TD | Squadron's towers-become-units is a kit-native twist worth stealing |
| 5.7 Warlock Arena | Warlock, Pudge Wars | |
| 5.8 Asymmetric Tag | Vampirism, Tree/Sheep Tag, Island Defense, Cat & Mouse | |
| 5.9 Payload/Escort | Helm's Deep-style scenario sieges (escort variants) | thinnest ancestry — watch it in playtests |
| 5.10 Control | **Zone Control (BW)** | the template existed verbatim in BW |
| 5.11 Party wrapper | **Uther Party** | the wrapper existed verbatim in WC3 |

**Genres the taxonomy deliberately doesn't cover** (and whether the kit substrate could ever host them): social deduction (poorly — identity/information games, not combat kits); territory diplo (poorly — macro, no piloted kit); bounds/escape (partially — a movement-kit gauntlet is conceivable); ORPG (out of scope — that's the main game itself); RP sandbox (no); tug-of-war/auto-battle (**yes, and well** — kits auto-piloted by the utility AI in lanes is Legion TD-shaped and sim-native; candidate for a future template 5.12).

## 7. Sources
Community records verified July 2026: Hive Workshop most-hosted analyses & lobby logs; StarEdit Network's live BW genre census (2022–2025 thread); TeamLiquid BW forums; NeoGAF/ResetEra UMS retrospectives; Blizzard News (Arcade patch 1.5, Premium Arcade 4.3/Direct Strike & ARK Star, SC2 10th-anniversary); StarCraft Wiki (Arcade history, 2017 5% poll); w3reforged / wc3maps.com map databases (incl. active Korean hosting). Settled genre history (DotA chain, Auto Chess chain) from the standard record.
