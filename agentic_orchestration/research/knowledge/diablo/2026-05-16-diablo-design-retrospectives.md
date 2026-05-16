# Research — Diablo Design Retrospectives (I through Immortal) — 2026-05-16

**Mode:** A (analytical)
**Commissioner:** knight-rider (on behalf of Gandalf)
**Sources consulted:** David Brevik GDC 2016 postmortem (Gamedeveloper.com), VGChartz Diablo retrospective, PC Gamer (Diablo, D3 AH), Engadget (D3 Reaper of Souls), GameSpot (D3 AH article, D4 Season 1), Wikipedia (Diablo IV, Vessel of Hatred), Blizzard official blog, Dexerto, ComicBook.com, GameRevolution, SVG, CriticalHit.net, BlizzardWatch

---

## Summary

The Diablo franchise across five titles traces a design arc: from horror-inflected dungeon crawler where atmosphere and intimacy were paramount (D1), to genre-defining loot and class-archetype system (D2), to a contested accessibility pivot derailed by the auction house disaster and then course-corrected by Reaper of Souls (D3), to a modern-loot reconciliation attempt that stumbled in Season 1 but recovered through iteration (D4), to a mobile-first monetization experiment that prioritized revenue extraction over fairness (Immortal). Each entry surfaces distinct design lessons. D2 remains the genre's reference point because it achieved a rare synthesis: deep class identity, a layered loot system with legendary items that became culturally legible, and a difficulty structure that rewarded mastery without gating casuals until they chose to engage harder content.

---

## Findings

### Title 1 — Diablo I (1996)

#### What the Design Chose

**Genre origin story — turn-based to real-time conversion:**
Diablo was originally conceived as a turn-based party RPG in the Rogue/Nethack lineage. David Brevik initially opposed the shift to real-time gameplay. He was overruled internally, implemented it in a single Saturday, and immediately recognized the result as transformative: "oh my god, that was awesome." The conversion from tile-based-turn to continuous real-time action is the founding moment of the action-RPG genre.

**Horror over high fantasy:**
The deliberate tone choice was "dark, evil" over traditional high-fantasy adventure. The art direction drew from Italian zombie films and personal visits to churches, catacombs, and castles. Religious iconography — churches, religious artifacts, deicide — was central to the aesthetic. This was a break from contemporaneous RPGs (Warcraft, Baldur's Gate) which used sunlit, heroic aesthetics. The result: Diablo felt like a horror game, not an adventure game. Early reviews' most common descriptor was "atmospheric."

**Accessibility as a design principle:**
Brevik and the team disliked RPGs that required 25 minutes of character creation. The interface passed the "mom test" — could a non-gamer play it? Menu philosophy was borrowed from Doom (minimalistic, immediate). The hotbar was invented in the final three months of development; previously a single potion slot existed. The goal was: into the dungeon as fast as possible.

**Sound design as atmosphere:**
The technical constraint of limited graphics was compensated with masterful sound design. Music and sound effects carried more atmospheric weight than visuals. Matt Uelman's soundtrack became famous in its own right.

**Randomization from Rogue DNA:**
Dungeon layout, item drops, quest groups were all procedurally generated. The quest randomization system (indicated by fountain color and Wounded Townsman status) created meaningful replay differentiation — multiple playthroughs experienced different quest combinations.

**Class asymmetry:**
Three classes (Warrior, Rogue, Sorcerer) with distinct stat caps and role constraints. Sorcerers needed spell book drops for advancement (resource dependency). Warriors required balanced stat investment. Rogues excelled at ranged versatility. The asymmetry was real — not just numerical differences but mechanically distinct ways to engage the dungeon.

**Permanent consequences:**
Shrines and enemies could permanently alter stats and equipment. This reflected "hardcore roots of RPGs" — meaningful risk, not just incremental progress. Later entries softened or removed permanence.

#### What Echoes Forward

- Horror tone established what "Diablo" *means* as an aesthetic identity; every subsequent entry has negotiated its relationship to this origin
- Single-town, intimate scope (one town, four dungeon styles, six musical tracks) contrasted with later entries' scope inflation
- Class asymmetry as a design goal — D2 deepened it, D3 softened it, D4 tried to restore it
- The foundational loot loop — kill enemy, item drops, check stats, upgrade or discard — invented here in its action-RPG form

**Sources:** Gamedeveloper.com (Brevik interview), VGChartz retrospective, CriticalHit.net, SVG, BlizzardWatch

---

### Title 2 — Diablo II (2000)

#### What the Design Chose

**Skill tree structure (the genre's template):**
The skill tree concept came from Brevik's love of Civilization II's tech tree. Each of the seven classes had three skill trees (27 trees total), organized in tiers with level requirements (level 6, 12, 18, 24, 30 for successive tiers). This created meaningful build commitment — you could not master all skills; you chose a specialization and invested in it.

Key design properties:
- Skills synergize with each other within and across trees, creating emergent build possibilities not explicitly telegraphed to the player
- Items could boost individual skills, entire skill trees, or all skills — creating gear-build interaction layers
- The "synergy system" (added in 1.10 patch) formalized cross-skill investment payoffs

**Itemization — the genre's reference standard:**
The D2 item system is the most frequently cited as the model for what good ARPG itemization looks like. Why it worked:
- Items were legible at a glance — "find useful stuff all the time and at all levels"
- Named uniques ("Shako," "Enigma," "Stone of Jordan," "Windforce") became culturally famous within the community — items with identity, not just stats
- Magic-find system gave players control over loot probability distribution — agency within RNG
- The treasure class system assigned monster types specific loot ranges based on area level, creating a connection between where you farm and what you find
- Multiple item tiers: Normal → Magic (blue) → Rare (yellow) → Set → Unique → Crafted → Rune Words — each tier had distinct acquisition and power patterns

**Rune Words — emergent late-game crafting:**
The rune word system (inserting specific rune combinations into socketed items) added a crafting layer that interacted with the base item type, creating highly variable power potential. Items like "Enigma" (teleportation on a body armor) became so powerful they defined entire character strategies.

**Difficulty ladder (Normal → Nightmare → Hell):**
Three full playthroughs of the same content at escalating difficulty. Each pass revealed different item drop ranges and monster abilities. This design assumed the game was worth replaying multiple times — and it was.

**Class design archetypes:**
Seven classes with genuinely distinct mechanical identities: Barbarian (melee, physical mastery), Sorceress (elemental magic), Necromancer (summoning + curses), Amazon (ranged + thrown), Paladin (aura-based buffs + holy power), Druid (shapeshifting + nature magic), Assassin (traps + martial arts combos). Each had builds that diverged significantly from within-class defaults; the Necromancer who focused on poisoning was mechanically distinct from the one who summoned armies.

#### Why D2 Became the Genre Reference Point

Community analysis consistently cites: the combination of meaningful build investment decisions, culturally legible named items, end-game content that didn't expire (farming specific bosses forever), and a difficulty structure that was hard enough to feel earned but not so gated as to exclude engagement with its systems. The items felt *real* — not statistical abstractions but objects with history.

The auction house in D3 illustrated what D2 didn't have: a marketplace that could short-circuit the farming loop. D2's lack of integrated trading made the loot hunt the primary activity. Finding your own Shako was a story. Buying one from the AH was not.

**Sources:** Gamedeveloper.com, diablo2.io, DiabloFans community retrospective (https://www.diablofans.com/forums/read-only-diablo-forums/diablo-iii-general-discussion/32182-what-made-d2s-itemization-so-good), Game Design Forum Reverse Design series (http://thegamedesignforum.com/features/RD_D2_5.html)

---

### Title 3 — Diablo III (2012) + Reaper of Souls (2014)

#### Launch — What Went Wrong

**The Auction House:**
Blizzard built both a gold auction house and a real-money auction house (RMAH) into the launch game, believing it would provide "convenient and secure" trading. The result:
- The game was visibly balanced to push players toward the AH — loot felt repetitive and worthless without it
- Players checked the AH first and played the game second
- The core fantasy ("kill enemies → get loot → upgrade") was short-circuited; the loot hunt became a shopping experience
- Jay Wilson (game director) acknowledged within two months of launch that he regretted implementing the AH
- The AH inverted the design philosophy of D2 — the thing D2 made into a story (finding your Shako) was turned into a transaction

**Accessibility pivot:**
D3 aimed to broaden the audience beyond D2's core. This meant softer class identities (classes that felt more interchangeable in early game), a more colorful aesthetic (moving away from D1's horror tone), and streamlined character creation. The community read this as a dilution — D2 players felt D3 was designed for people who hadn't played D2.

**Inferno difficulty disaster:**
The hardest difficulty was designed to wall players unless they purchased gear through the AH. This explicitly monetized the difficulty gap, confirming community suspicions that the AH was load-bearing for the game's design.

#### Reaper of Souls (2014) — The Course Correction

Blizzard shut down the AH on March 18, 2014 — the first major reversal of a shipping design choice in the franchise.

**Loot 2.0:**
- Items redesigned to drop more frequently and to be more personally appropriate (smart loot — items skewed toward your class)
- Legendary items given unique mechanics rather than just high stats — bringing back the D2 identity of named items
- Mystic artisan introduced for targeted item improvement

**Adventure Mode + Rifts:**
New content structure that divorced the loot hunt from replaying the campaign. Rifts (randomized dungeons) became the primary endgame activity.

**Season system introduction:**
Periodic fresh starts on seasonal ladders — players reset and race through content with new seasonal rewards. This addressed the "end-state stagnation" problem by providing recurring reasons to restart.

**Verdict:**
Reaper of Souls is widely regarded as the game D3 should have shipped as. The course-correction validated the D2-era design principle: the loot hunt must be the core activity; anything that substitutes for it destroys the game's purpose.

**Sources:** PC Gamer (https://www.pcgamer.com/diablo-3-reaper-of-souls-loot-system-designed-to-cut-the-legs-out-from-the-auction-house/), GameSpot (https://www.gamespot.com/articles/ten-years-later-lessons-from-diablo-iiis-auction-house-disaster-have-not-been-remembered/1100-6503489/), Engadget, Blizzard official blog (https://news.blizzard.com/en-gb/article/10974978/diablo-iii-auction-house-update)

---

### Title 4 — Diablo IV (2023) + Vessel of Hatred (2024)

#### Launch and Initial Reception

Released June 5, 2023. Critics praised narrative and atmosphere — the return to D1's dark horror aesthetic was widely noted positively. The game's open world structure (Sanctuary as explorable region rather than hub-and-dungeon) was new to the franchise.

Initial player numbers were strong; Blizzard reported 1.5 billion hours played by BlizzCon 2023.

#### Season 1 Backlash — The Design Community Flashpoint

Season 1 (Season of the Malignant) launched with patch notes that included **wide-ranging nerfs across all five classes.** The community's reaction was extreme:
- Metacritic user scores collapsed (PS5: 1.8/5575 ratings; PC: 2.2/7261 ratings) — sustained review bombing, not a single spike
- Reddit thread summarized community sentiment: *"Fixed an issue where players were having fun."*
- The Sorcerer, already regarded as the weakest class, received significant nerfs alongside the universal nerfs — the class was effectively unplayable for many builds
- Community director Adam Fletcher acknowledged publicly: *"We know it is bad. We know it is not fun. We ourselves know that it's not the greatest play experience for players out there."*
- Patch 1.1.1 committed to: reverting nerfs, Sorcerer/Barbarian improvements, increased monster density, inventory improvements

**Design lesson identified by community:** The initial D4 launch balanced around long-term seasonal engagement rather than immediate player power expression. Nerfs before players had established their power fantasies created backlash disproportionate to the actual balance changes. The PoE 2 developers commented publicly that they were watching D4's Season 1 situation carefully as a lesson in community management.

#### Season Structure — Recovery and Iteration

After Season 1, Blizzard leaned into:
- Season of Blood (Season 2) — 14,000 words of patch notes driven by community feedback; widely regarded as the turning point
- Seasonal Leaderboards introduced (The Gauntlet — weekly challenge dungeons)
- Each season added new mechanics layered on the base game

**Vessel of Hatred Expansion (October 7, 2024)**
- New region: Nahantu (jungle biome, corruption-themed)
- New class: **Spiritborn** — uses spirit guardians (Gorilla, Eagle, Centipede, Jaguar) to channel different power modes; considered by community to be mechanically innovative and stronger than launch classes
- Critical and commercial success — the expansion is generally seen as the game finding its identity

**Current Design Discourse (2024–2026):**
- Community debates persist around: loot density vs. item quality tension; seasonal reset cadence; endgame activity diversity
- D4 is no longer seen as a failed game but as one that took multiple seasons to understand what it was
- Comparison point with PoE2 (early access Dec 2024): Two AAA ARPGs with different philosophy — D4's broader accessibility vs. PoE2's depth emphasis

**Sources:** Wikipedia (Diablo IV), GameSpot (Season 1), GameRevolution, Dexerto, ComicBook.com, GamingBolt (https://gamingbolt.com/diablo-4s-first-season-what-went-wrong), Blizzard news

---

### Title 5 — Diablo Immortal (2022)

#### Platform and Design Choices

Released June 2022 for mobile (iOS/Android) with later PC port. Developed with NetEase (Chinese mobile developer) to target the mobile-first global market. The core game (combat, dungeons, class fantasy) received broadly positive feedback as a mobile ARPG — smooth controls, good production value, genuine Diablo atmosphere on mobile.

#### Monetization — What Prioritized Over Gameplay Fairness

The controversy centers on **Legendary Gems** — the primary power-scaling system in the endgame and PvP:
- Legendary Gems are rare drops or purchasable via Eternal Crests (premium currency)
- 5-star gems (the highest tier) have an extremely low natural drop rate
- Community estimates: spending $15–$20/month for meaningful progression; **$10,000–$100,000+ to reach competitive PvP power levels**
- The system is gacha-adjacent: random gem quality within a rated tier, with upgrade costs escalating exponentially
- PvP (the most engagement-focused content) was effectively pay-to-win: players who spent could not be matched by free players in gem quality

**Blizzard's Defense:**
Senior officials argued that 99.5% of all game content was accessible without spending. This is technically true — the PvE campaign and most content was completable free. But the endgame progression wall and PvP imbalance were explicit consequences of the monetization design.

**Regulatory and Industry Fallout:**
- EU antitrust scrutiny flagged Immortal's mechanics
- The controversy became a case study in mobile game monetization ethics; game developer community discussions (GDC, Discord) used Immortal as a teaching example for where "free-to-play done wrong" ends up
- Multiple content creators produced viral breakdowns of the full cost-to-max-power calculations

**What the Team Prioritized:**
- Accessible Diablo experience on mobile — largely achieved
- Revenue extraction from a whaling model — achieved at cost to community trust and brand reputation
- The game is technically still running and generating revenue; the monetization model did not fail commercially, only in terms of community perception and long-term franchise trust

**Lesson for the Community:**
Immortal demonstrated that the Diablo brand has enough pull to drive initial installs even in a controversy-laden monetization context. But community resentment calcified around the game — it became the genre's most cited example of monetization as a design principle taking precedence over player welfare.

**Sources:** Washington Post (https://www.washingtonpost.com/video-games/2022/06/14/diablo-immortal-pay-to-win-monetization/), GamesRadar, Dexerto, Sportskeeda, Games Learning Society

---

## Knowledge Gaps Not Resolved

- **D2's development postmortem in full:** Brevik's 2016 GDC talk covers D1 extensively; D2's development process is less thoroughly sourced in accessible retrospectives
- **D3 internal design documents:** Jay Wilson's statements are available; the full internal design philosophy documentation is not public
- **D4 current state (2025–2026):** Vessel of Hatred review data is from late 2024; ongoing seasonal development post-expansion was not fully sourced
- **D1 specific audio design breakdown:** Uelman's compositions are widely praised; a detailed retrospective on sound design choices was not found in available sources

---

## Source List

| Source | URL | Type |
|---|---|---|
| Gamedeveloper.com — Brevik 20 Years Later | https://www.gamedeveloper.com/design/20-years-later-david-brevik-shares-the-story-of-making-i-diablo-i- | Primary (developer retrospective) |
| GDC Vault — Classic Game Postmortem: Diablo | https://gdcvault.com/play/1023469/Classic-Game-Postmortem | Primary (GDC talk) |
| VGChartz — Diablo Retrospective | https://www.vgchartz.com/article/445845/the-light-returns-to-tristram-a-diablo-retrospective/ | Secondary |
| DiabloFans — D2 Itemization Discussion | https://www.diablofans.com/forums/read-only-diablo-forums/diablo-iii-general-discussion/32182-what-made-d2s-itemization-so-good | Secondary (community) |
| Game Design Forum — Reverse Design D2 | http://thegamedesignforum.com/features/RD_D2_5.html | Secondary (design analysis) |
| PC Gamer — D3 Reaper of Souls loot | https://www.pcgamer.com/diablo-3-reaper-of-souls-loot-system-designed-to-cut-the-legs-out-from-the-auction-house/ | Secondary |
| Blizzard — AH shutdown announcement | https://news.blizzard.com/en-gb/article/10974978/diablo-iii-auction-house-update | Primary (official) |
| GameSpot — 10 Years Later, D3 AH Lessons | https://www.gamespot.com/articles/ten-years-later-lessons-from-diablo-iiis-auction-house-disaster-have-not-been-remembered/1100-6503489/ | Secondary |
| GameSpot — D4 Season 1 Backlash | https://www.gamespot.com/articles/diablo-4-season-1-nerfs-spark-backlash-as-blizzard-plans-to-address-feedback/1100-6516104/ | Secondary |
| GamingBolt — D4 Season 1 What Went Wrong | https://gamingbolt.com/diablo-4s-first-season-what-went-wrong | Secondary |
| Washington Post — Immortal P2W | https://www.washingtonpost.com/video-games/2022/06/14/diablo-immortal-pay-to-win-monetization/ | Secondary |
| Wikipedia — Diablo IV | https://en.wikipedia.org/wiki/Diablo_IV | Primary (encyclopedic) |
| Wikipedia — Diablo IV: Vessel of Hatred | https://en.wikipedia.org/wiki/Diablo_IV:_Vessel_of_Hatred | Primary (encyclopedic) |

*Accessed: 2026-05-16*
