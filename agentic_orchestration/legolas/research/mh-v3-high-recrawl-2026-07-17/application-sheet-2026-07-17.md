# Application Sheet — Mob-harvest-v3 HIGH-tier Provenance-Integrity Re-crawl — 2026-07-17

**For:** Elrond (mechanical DB application)
**Crawl date:** 2026-07-17
**Landed ailment vocab reference:** {damage-amp, freeze, stun, poison-dot, taunt, blind, curse/hex, fear, instant-kill, deflect} + soft_control variants (slow, root/immobilize, knockback, silence, burn/DoT, marking)

Iron law: every row cites live URLs OR is marked UNVERIFIABLE / PHANTOM with search trail. Row counts reconcile with index summary block (12 verified-authentic + 1 re-key-clean + 0 phantom + 0 unverifiable = 13 total).

---

## BATCH (13 kits)

---

### 1. `di-cyclone-monk-pvp` — "Cyclone CC Monk"

**disposition:** **verified-authentic**
**target action for Elrond:** no correction required. Add source_urls to populate the currently-empty field (row lacks source_urls). Optional flag `mh-v3-recrawl-verified-2026-07-17:legolas`.

**corpus row context:**
- `kit_id`: `di-cyclone-monk-pvp`
- `folk_name`: `Cyclone CC Monk`
- `game`: `di`
- `provenance_tag`: `mobile-harvest-v3`
- `source_date`: `2026-07-12`
- `source_urls`: EMPTY

**Entity existence — CONFIRMED:**
- DI Monk class exists (launch class 2022); Cyclone Strike is a Focus-tree skill

**Mechanic verification — CONFIRMED:**
- Cyclone Strike is a real DI Monk skill: "forcibly pulls enemies towards the Monk's location, followed by a 12 yard-radius blast that deals Holy damage"
- PvP CC role explicit: "long-range crowd control tool that pulls enemies within range of the Monk's melee devastation"
- Documented essence variants: **Tempest's Heart** (Cyclone Strike knocks away instead of pulls); paired with **Freedom's Gale** (Imprisoned Fist stun) as canonical PvP combo

**live URL(s):**
- https://diablo.fandom.com/wiki/Cyclone_Strike — Diablo Wiki entry
- https://www.wowhead.com/diablo-immortal/guide/wizard-skills-primary-attacks (Wowhead DI skill DB scope confirms Cyclone Strike Focus classification cross-referenced)
- https://gamerant.com/diablo-immortal-best-cyclone-strike-monk-build-skills-gear-gems-reforge/ — GameRant Cyclone Strike Monk build
- https://gamerant.com/diablo-immortal-best-pvp-battleground-monk-build-skills-gear-gems-reforge/ — GameRant Cyclone Strike PvP Battleground Monk build
- https://www.icy-veins.com/diablo-immortal/monk-cyclone-storm-build-guide-for-raids — Icy Veins Cyclone Storm Monk raid guide
- https://mbaker2307.wixsite.com/mbakerdesign/mystic-wind-cyclone-strike-monk/ — Mystic Wind Cyclone Strike Monk build guide

**evidence quote (mechanic):** GameRant Cyclone Strike PvP build (verbatim summary): "the crowd control from Cyclone Strike is typically paired with other abilities for devastating effect. Anybody who gets hit by the blow will be stuck in place for several seconds, freeing the Monk to use Cyclone Strike against every target hit... The Cyclone Helicopter build is recommended for PvP, focusing on sustained pressure and defensive uptime."

**PvP complaint-tier pattern:** verified — Cyclone Strike Monk is a canonical PvP archetype, actively iterated on across the 2022-2026 lifecycle.

**Landed vocab mapping:** Pull (soft-control lineage) + Stun (via Imprisoned Fist paired) + Knockback (via Tempest's Heart essence). All landed vocab.

---

### 2. `di-bone-wall-necro-pvp` — "Bone Wall Disruption Necro"

**disposition:** **verified-authentic**
**target action for Elrond:** no correction required. Add source_urls (currently EMPTY). Optional flag `mh-v3-recrawl-verified-2026-07-17:legolas`.

**corpus row context:**
- `kit_id`: `di-bone-wall-necro-pvp`
- `folk_name`: `Bone Wall Disruption Necro`
- `game`: `di`
- `provenance_tag`: `mobile-harvest-v3`
- `source_date`: `2026-07-12`
- `source_urls`: EMPTY

**Entity existence — CONFIRMED:**
- DI Necromancer class exists (launch class 2022); Bone Wall is a real Necromancer skill

**Mechanic verification — CONFIRMED:**
- Bone Wall is a real DI Necromancer skill; "creates a wall to block movement and interrupt channeled skills"
- PvP role: "crowd control centerpiece in PvP builds"; "block choke points in the arena with Bone Wall or imprison enemies with it while keeping them in place with Bone Spikes"
- Legendary enhancements documented: **Pyre's Allure** (off-hand shield making Bone Wall ignitable via Soulfire), **Exhumant's Backbone** (converts Bone Wall to Bone Pillars with stun)

**live URL(s):**
- https://diablo.fandom.com/wiki/Bone_Wall_(Diablo_Immortal) — Fandom Bone Wall (DI) entry
- https://immortal.maxroll.gg/build-guides/bone-wall-necromancer-pvp-guide-battlegrounds-rite-of-exile — Maxroll dedicated Bone Wall Necromancer PvP guide (Battlegrounds + Rite of Exile)
- https://www.icy-veins.com/diablo-immortal/necromancer-bone-spear-pvp-build-guide — Icy Veins Necro PvP (adjacent verification)
- https://www.dexerto.com/diablo/best-diablo-immortal-necromancer-builds-1870129/ — Dexerto 2026 Necromancer meta
- https://www.diablofans.com/builds/109604-pvp-bone-spear-necro — DiabloFans PvP Necro build

**evidence quote (mechanic + PvP role):** Maxroll dedicated guide (via WebSearch): "When using Bone Wall as a crowd control tool, players should lock enemies down with strategically placed Bone Walls (turned into Bone Pillars via Exhumant's Backbone), and ignite them with Soulfire. Players should position their Bone Pillars well, only using them to stun in emergency situations, instead use Bone Spikes as the first stun option, and plant 2 Bone Wall's Bone Pillars in strategic locations."

**Landed vocab mapping:** Movement-block + interrupt (immobilize soft-control) + Stun (via Bone Pillar variant) + DoT-burn (via Pyre's Allure ignite). All landed vocab.

---

### 3. `di-bombardment-wizard-pvp` — "Bombardment Artillery Wizard"

**disposition:** **verified-authentic**
**target action for Elrond:** no correction required, but MEDIUM-HIGH confidence: folk_name derived from essence-modified Meteor, not from a standalone skill. Optional flag `folk-name-essence-derived-2026-07-17:legolas` for pattern-tracking. Add source_urls (currently EMPTY).

**corpus row context:**
- `kit_id`: `di-bombardment-wizard-pvp`
- `folk_name`: `Bombardment Artillery Wizard`
- `game`: `di`
- `provenance_tag`: `mobile-harvest-v3`
- `source_date`: `2026-07-12`
- `flags`: `kb-only-backfill-attempted-2026-07-16` (S8 signal — prior verification failure)
- `source_urls`: EMPTY

**Entity existence — CONFIRMED:**
- DI Wizard class exists (launch class 2022); Meteor is a real Wizard skill

**Mechanic verification — RESOLVED WITH NUANCE:**
- "Bombardment" is **NOT** a standalone Wizard skill in DI
- "Continuous Bombardment" IS a real Meteor essence: "makes Meteor drop several meteorites in a direction, knocking enemies away and Stunning them, unlocked by equipping the Legendary pants Fragments upon Fragments"
- "Bombardment's Toll" IS a real Legendary shoulder item
- **The archetype is community-adopted and REAL** — "Bombardment Artillery Fire PvP Wizard" appears in multiple 2026 tier lists and meta videos as an active PvP archetype, matching corpus harvest window 2026-07-12

**live URL(s):**
- https://diablo.fandom.com/wiki/Meteor_(Diablo_Immortal) — Fandom Meteor DI entry (source of Continuous Bombardment essence documentation)
- https://game8.co/games/Diablo-Immortal/archives/378701 — Game8 "Bombardment's Toll: Effects and Associated Builds" (Legendary shoulder item + build associations)
- https://www.youtube.com/watch?v=-DO37h0nBKY — "The ONLY PvP Wizard Meta Builds You Need in 2026!" (Bombardment Artillery among featured archetypes)
- https://www.dexerto.com/diablo/best-diablo-immortal-wizard-builds-1872848/ — Dexerto 2026 Wizard meta analysis
- https://www.icy-veins.com/diablo-immortal/wizard — Icy Veins Wizard class overview

**evidence quote (essence mechanic):** Fandom Meteor entry (via WebSearch): "Continuous Bombardment is an essence that makes Meteor drop several meteorites in a direction, knocking enemies away and Stunning them, unlocked by equipping the Legendary pants Fragments upon Fragments."

**evidence quote (community archetype existence):** WebSearch 2026 tier list summary: "The Bombardment Artillery Fire PvP Wizard build is featured as a meta option in 2026, described as offering 'Insane Damage + High Range'. This build appears across multiple tier list and meta analysis videos from throughout 2026."

**Skepticism-caveat:** Dexerto's 2026 meta analysis (dexerto.com/diablo/best-diablo-immortal-wizard-builds) narrows viable Wizard PvP options to "Disintegrate, the arc and wind freeze path, and Scorch" — NOT Bombardment. This suggests Bombardment Artillery is a community-discussed but NOT top-tier meta build in current 2026. The archetype IS real and CURRENT (matches harvest window), just not first-tier.

**Diagnosis of `kb-only-backfill-attempted-2026-07-16` flag:** the prior verification failure likely happened because "Bombardment" alone doesn't resolve to a skill; requires understanding the essence-modification pattern. This re-crawl resolves that gap.

**Landed vocab mapping:** Knockback + Stun (Continuous Bombardment essence effects); DoT-burn (adjacent Rolling Meteor essence); Freeze (adjacent Snowstorm essence). All landed vocab, though the specific "Bombardment Artillery" archetype's CC signature is knockback + stun.

**Why NOT phantom (checking against di-spiritform precedent):**
- The mechanic name ("Continuous Bombardment") EXISTS verbatim in official/wiki source (unlike di-spiritform's "spirit form" which did not)
- The community archetype ("Bombardment Artillery") EXISTS in multiple cited 2026 sources (unlike di-spiritform's colloquial "spirit form" which returned "No links found")
- The kit represents a real, temporally-current archetype — just derived from an essence rather than a base skill

---

### 4. `d2-ghost-pvp` — "Ghost"

**disposition:** **re-key-clean**
**target action for Elrond:** re-key from `d2-ghost-pvp` → `d2-ghost-assassin-pvp` (or `d2-ghost-sin`). Update folk_name from bare `Ghost` → `Ghost Assassin (WW/Trap)`. Populate source_urls. Optional flag `mh-v3-recrawl-rekey-2026-07-17:legolas`.

**corpus row context:**
- `kit_id`: `d2-ghost-pvp`
- `folk_name`: `Ghost`
- `game`: `d2`
- `provenance_tag`: `mobile-harvest-v3`
- `source_date`: `2026-07-12`
- `source_urls`: EMPTY

**Entity existence — CONFIRMED (with class clarification):**
- D2 Assassin class exists (Lord of Destruction expansion, 2001); Ghost is a canonical **Assassin** PvP build archetype
- D2 Barbarian class also exists BUT does NOT have a "Ghost" build — the docket rationale's "could be Ghost-Warrior Barb build" speculation is INCORRECT per multiple cited sources

**Mechanic verification — CONFIRMED (with re-key required):**
- Ghost Assassin is a WW/Trap hybrid: "a mix of hybrid and whirlwind assassin builds — they teleport and have traps like a hybrid, but emphasize the WW damage like a WW assassin. A ghost is basically a pure WW assassin armed with teleport and low level traps for stun."
- Core skills: high Mind Blast (stun), Fade (DR + curse-duration reduction + resist), Whirlwind, low-level trap complement, Dragon Flight (teleport-strike)
- Signature mechanic: high Open Wounds stacking on WW weapons ("negative health regeneration" that lasts 8s, unresistable, cancels regen)
- Anti-caster specialization: "The Ghostsin is meant to be played against casters, and can incapacitate them with Mind Blast as soon as the spellcaster is within reach and trying to cast a spell."

**live URL(s):**
- https://www.purediablo.com/forums/threads/pvp-ww-ghost-assassin-guide-v2-0-by-tienje.1070/ — PureDiablo canonical PvP WW Ghost Assassin guide V2.0 by TienJe
- https://diablo2.diablowiki.net/Guide:PvP_C/C_WW_Shadow_Assassin_v1.10,_by_Voide — DiabloWiki PvP WW Shadow Assassin guide (Ghost lineage predecessor)
- https://www.items7.com/blog/how-to-build-a-ghost-sin-by-skibum/ — items7.com Ghost Sin build guide by Skibum
- https://www.icy-veins.com/d2/whirlwind-assassin-whirlwindsin-build — Icy Veins WW Assassin build (Ghost is WW+trap variant)
- https://maxroll.gg/d2/guides/whirlwind-assassin — Maxroll WW Assassin endgame guide (Season 14)
- https://www.rpgstash.com/blog/top-10-d2r-pvp-builds — rpgstash Top 10 D2R PvP builds (Ghost Assassin featured)
- https://forums.d2jsp.org/topic.php?t=78040170&f=87&o=10 — d2jsp forum "Ghost Assassin Vs Barb" thread (confirms Ghost = Assassin, not Barb, in PvP discourse)
- https://www.purediablo.com/forums/threads/pvp-ww-trapper-hybrid-guide-by-happyassassin.1068/ — PureDiablo PvP WW/Trapper Hybrid guide (Ghost lineage)

**evidence quote (Ghost = Assassin):** items7.com Skibum Ghost Sin guide (via WebSearch): "Ghosts are a mix of hybrid and whirlwind assassin builds - they teleport and have traps like a hybrid, but emphasize the WW damage like a WW assassin."

**evidence quote (NOT Barbarian):** PureDiablo Ghost Assassin guide V2.0 by TienJe (via WebSearch): "As a result of their build, they come equipped with high level Mind Blast and Fade. Fade adds 1% DR per level, lowers curse duration, and adds resistance. Mind Blast stuns characters, adds stun duration, and does minor damage." (Mind Blast is a Shadow Discipline Assassin skill, not Barbarian.)

**Docket-rationale correction:** the HIGH-tier docket §4 rationale for this kit read "verify this maps to a specific archetype in D2 PvP guide corpus (could be Ghost-Warrior Barb build, or lay-shorthand for an evasion tactic)." Neither speculation is correct. The Ghost archetype IS the Assassin WW/Trap build; the current `d2-ghost-pvp` kit_id + terse `Ghost` folk_name is under-specified and creates classifier ambiguity risk.

**Why re-key-clean rather than verified-authentic:**
- The bare `Ghost` folk_name is under-specified for a D2 game with 7 classes (5 launch + Assassin + Druid; Warlock added 2026); it does NOT self-identify as Assassin
- The kit_id `d2-ghost-pvp` similarly lacks class-anchor
- Downstream classifiers reading `Ghost` as a folk_name have no route to disambiguate from adjacent Ghost-adjacent constructs (Ghost farming build for MF is a common Barb activity; "ghost" is a common lay-descriptor for stealth/evasion)
- Re-keying to `d2-ghost-assassin-pvp` with folk_name `Ghost Assassin (WW/Trap)` preserves the atlas signal AND resolves the ambiguity

**Landed vocab mapping (post re-key):** Stun (Mind Blast) + Open Wounds bleed (DoT-adjacent, physical damage-over-time) + Damage reduction (Fade, self-buff not CC). Primary CC is Stun; Open Wounds is landed as bleed-DoT-adjacent per element vocabulary.

---

### 5. `d2-wl-blood-boil` — "Blood Boil Warlock"

**disposition:** **verified-authentic**
**target action for Elrond:** no correction required. Existing source_urls contains only aoeah.com; recommend augmenting with Maxroll + Icy Veins per this re-crawl. Optional flag `mh-v3-recrawl-verified-2026-07-17:legolas`.

**corpus row context:**
- `kit_id`: `d2-wl-blood-boil`
- `folk_name`: `Blood Boil Warlock`
- `game`: `d2`
- `provenance_tag`: `mobile-harvest-v3`
- `source_date`: `2026-07-12`
- `source_urls`: `["https://www.aoeah.com/news/4387--d2r-best-warlock-builds-for-leveling--endgame-season-13"]` (sole-source per S10 signal)

**Entity existence — CONFIRMED:**
- D2R Warlock class launched February 14, 2026 via "Reign of the Warlock" expansion (Patch 3.2); pre-dates 2026-07-12 corpus source_date by 5 months
- Blood Boil is a real Warlock skill in the Demon skill tree

**Mechanic verification — CONFIRMED:**
- Blood Boil is a real skill: "creates a Fire and Physical damage eruption around each of his [Warlock's] minions"
- Archetype: "Demon Blood Boil Warlock is a new Summoner in the game that forms pacts with Demons and blows them up to inflict massive pain on his foes"
- Core skills: Blood Boil + Summon Tainted + Demonic Mastery + Engorge (heal-minion companion)
- Popular through Season 13 and Season 14 despite nerfs ("even Nerfed but still S-Tier")

**live URL(s):**
- https://maxroll.gg/d2/guides/blood-boil-warlock-guide — Maxroll endgame Season 14 Blood Boil Warlock guide
- https://www.icy-veins.com/d2/blood-boil-warlock-build — Icy Veins Blood Boil Warlock build
- https://www.icy-veins.com/d2/blood-boil-warlock-build-bis-gear-runes — Icy Veins BiS gear + runes
- https://www.icy-veins.com/d2/blood-boil-warlock-build-skills — Icy Veins skill breakdown
- https://d2db.net/warlock-blood-boil-build — d2db build guide
- https://www.rpgstash.com/blog/d2r-warlock-blood-boil-build — rpgstash Blood Boil guide
- https://www.iggm.com/news/diablo-2-resurrected-season-14-best-starter-build-summon-tainted-blood-boil-warlock — IGGM Season 14 starter build
- https://www.u4gm.com/diablo-2-resurrected/blog-budget-blood-boil-warlock-in-diablo-2-resurrected-season-13 — u4gm Season 13 budget guide

**evidence quote (mechanic):** Maxroll Blood Boil Warlock guide (via WebSearch): "Blood Boil is a massive power boost for the Warlock, as it now gives him the ability to have a Corpse Explosion level of power without needing corpses around. He can have a total of up to 3 Demons at a time and mainly focuses on Tainteds for large AoE Fire Damage."

**Sole-source concern dissolved:** aoeah.com was low-authority sole source per the docket S10 signal; multi-source verification via Maxroll + Icy Veins + IGGM + d2db + u4gm + rpgstash removes the sole-source risk.

**Landed vocab mapping:** Fire + physical damage (elemental, not CC); minion detonation (adjacent to Corpse Explosion — landed). No primary CC ailment — this is a damage-forward summoner archetype.

---

### 6. `d2-wl-tainted-summoner` — "Tainted Summoner Warlock"

**disposition:** **verified-authentic**
**target action for Elrond:** no correction required. Existing source_urls contains only rpgstash.com; recommend augmenting with Maxroll + Icy Veins + D2Emu. Optional flag `mh-v3-recrawl-verified-2026-07-17:legolas`.

**corpus row context:**
- `kit_id`: `d2-wl-tainted-summoner`
- `folk_name`: `Tainted Summoner Warlock`
- `game`: `d2`
- `provenance_tag`: `mobile-harvest-v3`
- `source_date`: `2026-07-12`
- `source_urls`: `["https://www.rpgstash.com/blog/d2r-warlock-skill-trees-guide-chaos-demon-eldritch"]` (sole-source per S10 signal)

**Entity existence — CONFIRMED:**
- D2R Warlock class launched Feb 14 2026 (see kit #5 detail)
- Summon Tainted is a real skill in the Warlock's Demon tree

**Mechanic verification — CONFIRMED:**
- Summon Tainted is a real Warlock skill: "a fire-based summon that adds a fire damage dealer to your army and serves as Engorge fodder while providing supplementary fire damage"
- The archetype "Summoner Warlock" (Tainted variant) has dedicated Maxroll endgame guide
- Also documented as "Demon Warlock" in Icy Veins + D2Emu (synonymous archetype terminology)

**live URL(s):**
- https://maxroll.gg/d2/guides/summoner-warlock-guide — Maxroll Summoner Warlock endgame Season 14 guide
- https://d2emu.com/guides/builds/warlock-demon — D2Emu Demon Warlock build guide
- https://www.icy-veins.com/d2/demon-warlock-build — Icy Veins Demon Warlock build
- https://www.iggm.com/news/diablo-2-resurrected-ladder-season-13-warlock-summoner-leveling-build — IGGM Summoner Warlock leveling (Season 13)
- https://www.iggm.com/news/diablo-2-resurrected-season-14-best-starter-build-summon-tainted-blood-boil-warlock — IGGM Season 14 Tainted+Blood Boil
- https://diablobytes.com/d2-resurrected/builds/summoner-warlock/ — DiabloBytes Summoner Warlock SSF guide
- https://www.d2itemstore.com/blogs/diablo-2-guides/summoner-warlock-build — d2itemstore build guide
- https://www.youtube.com/watch?v=mEPvxlEJaMg — YouTube Summon Tainted Warlock build

**evidence quote (mechanic):** Maxroll Summoner Warlock guide (via WebSearch): "The Summon Tainted Blood Boil hybrid build stands head and shoulders above the rest among Warlock builds. This build shifts the focus toward maximizing the damage output of Summon Tainted minions rather than sticking to the traditional Blood Boil specialization path."

**evidence quote (core skills):** Maxroll: "For skill point allocation, you need to max out Summon Tainted, Blood Boil, Demonic Mastery, and Blood Oath to fully benefit from synergy bonuses, and additionally points are invested in Golem to bolster frontline survivability and draw enemy fire."

**Sole-source concern dissolved:** rpgstash was sole source per docket S10 signal; multi-source verification (Maxroll + Icy Veins + D2Emu + IGGM + DiabloBytes + d2itemstore) removes the sole-source risk.

**Landed vocab mapping:** Fire damage (element) + minion detonation (adjacent to Corpse Explosion — landed). Not primary CC.

---

### 7. `d2-wl-echoing-strike` — "Echoing Strike Warlock"

**disposition:** **verified-authentic**
**target action for Elrond:** no correction required (already has 3 URLs; well-sourced). Optional flag `mh-v3-recrawl-verified-2026-07-17:legolas`.

**corpus row context:**
- `kit_id`: `d2-wl-echoing-strike`
- `folk_name`: `Echoing Strike Warlock`
- `game`: `d2`
- `provenance_tag`: `mobile-harvest-v3`
- `source_date`: `2026-07-12`
- `source_urls`: `["https://www.rpgstash.com/blog/d2r-warlock-skill-trees-guide-chaos-demon-eldritch", "https://maxroll.gg/d2/guides/echoing-strike-warlock-guide", "https://odealo.com/articles/echoing-strike-warlock-build-for-diablo-2-resurrected"]`

**Entity existence — CONFIRMED:**
- D2R Warlock class launched Feb 14 2026 (see kit #5 detail)
- Echoing Strike is a real signature Warlock skill in the Chaos/Eldritch tree

**Mechanic verification — CONFIRMED:**
- Echoing Strike is a real skill: "creates echoes of your melee weapon that move forward and then come back at you, piercing enemies during the entire process"
- Synergizes with Hex Purge for "powerful magical eruptions that tear through tightly packed enemies"
- Widely considered strongest current-season build: "The build is widely considered one of the strongest in the current season and performs exceptionally well at endgame content"

**live URL(s) (augmentation to existing 3):**
- https://maxroll.gg/d2/guides/echoing-strike-warlock-guide — Maxroll endgame Season 14 guide (already in row)
- https://www.icy-veins.com/d2/echoing-strike-warlock-build — Icy Veins Echoing Strike Warlock
- https://www.icy-veins.com/d2/echoing-strike-warlock-build-skills — Icy Veins skill breakdown
- https://odealo.com/articles/echoing-strike-warlock-build-for-diablo-2-resurrected — Odealo guide (already in row)
- https://www.mmoexp.com/News/d2r-echoing-strike-warlock-builds-insane-damage-and-uber-capable-setup.html — MMOexp guide
- https://www.rpgstash.com/blog/d2r-season-13-echoing-strike-warlock-build-guide — rpgstash Season 13 guide
- https://www.ezg.com/blog/diablo-2-resurrected-patch-3-2-the-ultimate-echoing-strike-warlock-build-guide — EZG Patch 3.2 guide
- https://www.aoeah.com/news/4398--d2r-best-echoing-strike-warlock-builds-endgame-budget — AoEAH endgame + budget
- https://www.youtube.com/watch?v=6RgpgKHdb4E — YouTube Echoing Strike Warlock build guide

**evidence quote (mechanic):** Maxroll guide (via WebSearch): "The skill allocation starts with 1 point each into Echoing Strike, Sigil: Lethargy, and Summon Defiler, then maxes out Hex Purge, Mirrored Blades, Hex Bane, and Demonic Mastery... The Warlock has the same breakpoints as the Necromancer in Diablo II: Resurrected—Reign of the Warlock DLC, and it is recommended that you aim for the 125 FCR breakpoint (9 frames) to make Echoing Strike perform a lot smoother."

**Landed vocab mapping:** Magic damage (element) + Hex/curse (via Hex Purge/Hex Bane — landed as curse/hex). Notable ailment vocab (curse/hex) matches Warlock class flavor entirely.

---

### 8. `d2-wl-fire` — "Fire Warlock"

**disposition:** **verified-authentic**
**target action for Elrond:** no correction required (already has 4 URLs; well-sourced). Optional flag `mh-v3-recrawl-verified-2026-07-17:legolas`.

**corpus row context:**
- `kit_id`: `d2-wl-fire`
- `folk_name`: `Fire Warlock`
- `game`: `d2`
- `provenance_tag`: `mobile-harvest-v3`
- `source_date`: `2026-07-12`
- `source_urls`: `["https://maxroll.gg/d2/news/diablo-ii-resurrected-reign-of-the-warlock-expansion", "https://www.rpgstash.com/blog/d2r-warlock-skill-trees-guide-chaos-demon-eldritch", "https://maxroll.gg/d2/guides/fire-warlock-guide", "https://www.icy-veins.com/d2/fire-warlock-build"]`

**Entity existence — CONFIRMED:**
- D2R Warlock class launched Feb 14 2026 (see kit #5 detail)
- Fire Warlock is a canonical archetype using three real Warlock Chaos-tree fire skills

**Mechanic verification — CONFIRMED:**
- Fire Warlock uses three canonical fire skills: **Apocalypse** (large pentagram burst), **Flame Wave** (linear AoE), **Ring of Fire** (circular AoE)
- "Iconic build that lights up entire screens of monsters"
- "Apocalypse is a throwback to Diablo 1, which draws a large pentagram on the ground and burst for massive fire damage after a short while"
- Natural -xx Enemy Fire Resistance from Apocalypse enables immunity-breaking

**live URL(s) (augmentation to existing 4):**
- https://maxroll.gg/d2/guides/fire-warlock-guide — Maxroll endgame Season 14 (already in row)
- https://www.icy-veins.com/d2/fire-warlock-build — Icy Veins Fire Warlock build (already in row)
- https://maxroll.gg/d2/guides/fire-warlock-leveling-build-guide — Maxroll Season 13 leveling
- https://gamerant.com/diablo-2-resurrected-fire-warlock-build-beginner/ — GameRant beginner guide
- https://diablobytes.com/d2-resurrected/builds/fire-warlock/ — DiabloBytes Apocalypse AoE Leveling
- https://www.aoeah.com/news/4387--d2r-best-warlock-builds-for-leveling--endgame-season-13 — AoEAH Season 13 leveling+endgame
- https://www.items7.com/news/endgame-fire-warlock-actually-wrecks-build-guide-diablo-2-resurrected — Items7 endgame guide
- https://www.rpgstash.com/blog/d2r-warlock-apocalypse-build — rpgstash Apocalypse build guide

**evidence quote (mechanic):** Maxroll Fire Warlock guide (via WebSearch): "The Fire Warlock is a Ranged Caster that takes advantage of three very powerful Fire skills - Ring of Fire, Flame Wave, and Apocalypse, all with large Area of Effect Fire Damage... The skill allocation prioritizes: Apocalypse, Flame Wave, Ring of Fire, Demonic Mastery (10 Skill Points), Summon Defiler (Up to 57%), and Blood Oath (all remaining points)."

**Landed vocab mapping:** Fire damage (element) + fire immunity break (adjacent mechanic — landed as damage-amp adjacent). Primary shape is damage-forward, not CC-forward.

---

### 9. `d2-wl-abyss` — "Abyss Warlock"

**disposition:** **verified-authentic**
**target action for Elrond:** no correction required (2 URLs; well-sourced). Optional flag `mh-v3-recrawl-verified-2026-07-17:legolas`.

**corpus row context:**
- `kit_id`: `d2-wl-abyss`
- `folk_name`: `Abyss Warlock`
- `game`: `d2`
- `provenance_tag`: `mobile-harvest-v3`
- `source_date`: `2026-07-12`
- `flags`: (degenerate-famous flag per docket S7 signal)
- `source_urls`: `["https://maxroll.gg/d2/guides/abyss-warlock-build-guide", "https://maxroll.gg/d2/guides/abyss-warlock-leveling-build-guide"]`

**Entity existence — CONFIRMED:**
- D2R Warlock class launched Feb 14 2026 (see kit #5 detail)
- Abyss is a real Warlock skill in the Eldritch tree

**Mechanic verification — CONFIRMED:**
- Abyss is a real skill: "creates a tear in the ground pulling enemies towards it while dealing Magic damage. Abyss pulls targets in and deals AoE damage over time before detonating for massive damage. It's best used against Bosses and tough Elites"
- Archetype identity: "very few monsters in Diablo 2 Resurrected have Magic Immunity" — Abyss Warlock is a magic-damage league-starter
- Distinctive playstyle from Miasma Chain: "constantly place chains ahead of you and guide enemies into their corruption path rather than simply aiming directly at them"

**live URL(s):**
- https://maxroll.gg/d2/guides/abyss-warlock-build-guide — Maxroll endgame guide (already in row)
- https://maxroll.gg/d2/guides/abyss-warlock-leveling-build-guide — Maxroll leveling guide (already in row)
- https://www.icy-veins.com/d2/warlock-overview — Icy Veins Warlock overview (Abyss included)
- https://maxroll.gg/d2/resources/warlock-overview — Maxroll Warlock overview
- https://odealo.com/articles/abyss-warlock-build-for-diablo-2-resurrected — Odealo Season 14 Abyss guide
- https://diablo2.io/skills/abyss-t1676858.html — diablo2.io skill DB Abyss entry (skill data)

**evidence quote (mechanic):** Maxroll Abyss Warlock guide (via WebSearch): "Abyss creates a tear in the ground pulling enemies towards it while dealing Magic damage. Abyss pulls targets in and deals AoE damage over time before detonating for massive damage."

**Docket S7 degenerate-famous flag context:** the docket noted "Abyss" name-shape is a D4 Necromancer keyword and speculated cross-game bleed risk. Verification via multiple D2R-native authoritative sources (Maxroll, Icy Veins, Odealo, diablo2.io) confirms Abyss is a REAL D2R Warlock skill — not a cross-game bleed. The D4 Necromancer "Abyss" adjacency is coincidental, not a phantom trigger.

**Landed vocab mapping:** Magic damage (element) + pull (soft-control, landed) + DoT (adjacent to burn/DoT — landed). Notable dual signature: pull + DoT.

---

### 10. `hot-landsknecht-grenades` — "Grenade Landsknecht"

**disposition:** **verified-authentic**
**target action for Elrond:** no correction required. Populate source_urls (currently EMPTY). Optional flag `mh-v3-recrawl-verified-2026-07-17:legolas`.

**corpus row context:**
- `kit_id`: `hot-landsknecht-grenades`
- `folk_name`: `Grenade Landsknecht`
- `game`: `hot` (Halls of Torment)
- `provenance_tag`: `mobile-harvest-v3`
- `source_date`: `2026-07-12`
- `flags`: degenerate-famous + kb-only-backfill (docket S7 + S8 signals)
- `source_urls`: EMPTY

**Entity existence — CONFIRMED:**
- Halls of Torment (HoT) is a real game (Steam AppID 2218750)
- Landsknecht is a real HoT character/class

**Mechanic verification — CONFIRMED:**
- Grenade builds are a documented Landsknecht playstyle
- Steam Community discussion documents build strategy: "you can ignore grenade passives and just get physical skills like morning star and ring of blades, since the more physical damage you do the more often grenades proc. However, it's actually projectile damage, not physical damage that affects grenade procs"
- YouTube demonstrates the build in play (video "Trying out grenade build on Landsknecht")

**live URL(s):**
- https://steamcommunity.com/app/2218750/discussions/0/7953990088758033015/ — Steam Community "Landschnecht Grenade Build" thread
- https://www.youtube.com/watch?v=bF5kS1D0BDs — YouTube "Trying out grenade build on Landsknecht"

**evidence quote (build strategy):** Steam Community discussion (via WebSearch): "you can ignore grenade passives and just get physical skills like morning star and ring of blades, since the more physical damage you do the more often grenades proc. However, it's actually projectile damage, not physical damage that affects grenade procs."

**Diagnosis of prior verification failure (kb-only-backfill flag):** initial verification may have failed if the search targeted the game name "Hunters on Tempest" (a misinterpretation of the `hot-` prefix) or if the discovery route didn't reach Steam Community. Actual game = Halls of Torment. Verification succeeds via Steam Community + YouTube once the game identity is correct.

**Docket S7 degenerate-famous flag context:** grenade builds in HoT are documented as high-throughput but proc-dependent; the "degenerate-famous" label reflects community perception, not phantom-hood.

**Note on source density:** HoT is a smaller-scale game (Steam early-access era), and its community's build discourse is thinner than mainstream ARPG discourse. The finding relies on 2 direct sources but is well-anchored despite thin corpus. This is NOT unverifiable — verification is confirmed by the Steam thread's community consensus + YouTube demonstration.

**Landed vocab mapping:** Physical + projectile damage (element/damage-type). Grenades imply AoE + knockback. Not primary CC.

---

### 11. `ud-seal-veil-daimonios` — "Seal/Veil Resource Build (Daimonios)"

**disposition:** **verified-authentic**
**target action for Elrond:** no correction required (has 1 URL — pocketgamer.com; sole-source per S10 but authoritative for UD build corpus). Optional flag `mh-v3-recrawl-verified-2026-07-17:legolas`.

**corpus row context:**
- `kit_id`: `ud-seal-veil-daimonios`
- `folk_name`: `Seal/Veil Resource Build (Daimonios)`
- `game`: `undecember`
- `provenance_tag`: `mobile-harvest-v3`
- `source_date`: `2026-07-12`
- `source_urls`: `["https://www.pocketgamer.com/undecember/builds/"]` (sole-source per S10 signal)

**Entity existence — CONFIRMED:**
- Undecember (LINE Games ARPG) is a real game with active Season 7 as of 2026-07 window
- Daimonios is a known top-tier UD build designer/streamer whose builds are referenced in community

**Mechanic verification — CONFIRMED:**
- The build uses seal skills + Veil mechanic
- Core resource-management technique: "get a high-level Improved Technique rune and link them together to lower the resource cost. This build is based on the design by top player Daimonios"
- Pocket Gamer Season 7 build hub documents this as a featured meta build

**live URL(s):**
- https://www.pocketgamer.com/undecember/builds/ — Pocket Gamer Season 7 builds hub (source of Daimonios attribution)

**evidence quote (mechanic + Daimonios attribution):** Pocket Gamer Season 7 builds hub (via WebSearch): "The build uses many seal skills plus Veil, and it's very important to get a high-level Improved Technique rune and link them together to lower the resource cost. This build is based on the design by top player Daimonios."

**Sole-source concern:** the row has only Pocket Gamer as source. Pocket Gamer is a mid-tier mobile-gaming publication with legitimate UD coverage. The build IS real per this source, but a single-source verify is qualitatively thinner than the d2-wl kits' multi-source verifies. Recommendation: elrond consider whether sole-source is disqualifying for HIGH-confidence census purposes. If sole-source is not disqualifying, this remains verified-authentic; if elrond has a stricter multi-source rule, this could drop to a partial-verify.

**Note on why the sole-source is NOT phantom:** the source is authoritative for the UD build corpus, the build description is technically coherent (seal + veil + Improved Technique rune is UD-mechanically-valid), and the "Daimonios" attribution is a real community-figure name (not a fabricated attribution). Compare to the void-rift precedent where the sole-source (aoeah.com tier list) was ALSO the only source AND the build described conflicted with the game's actual class roster — this row does not have either failure mode.

**Landed vocab mapping:** Seal skills are UD's channeled/laid-plane skills; Veil is a stealth/dodge-adjacent mechanic. Not primary CC in the elemental sense — resource-management build shape.

---

### 12. `ud-cwc-spin-caster` — "Whirlwind CwC Blizzard (Ya55)"

**disposition:** **verified-authentic**
**target action for Elrond:** no correction required (has 1 URL — pocketgamer.com; sole-source per S10 but multi-season YouTube corroboration confirms). Optional flag `mh-v3-recrawl-verified-2026-07-17:legolas`.

**corpus row context:**
- `kit_id`: `ud-cwc-spin-caster`
- `folk_name`: `Whirlwind CwC Blizzard (Ya55)`
- `game`: `undecember`
- `provenance_tag`: `mobile-harvest-v3`
- `source_date`: `2026-07-12`
- `source_urls`: `["https://www.pocketgamer.com/undecember/builds/"]` (sole-source per S10 signal)

**Entity existence — CONFIRMED:**
- Undecember is a real game; Whirlwind + Blizzard is a canonical UD build combination
- "Spell Activation while Channeling" rune is UD's Cast-while-Channeling equivalent

**Mechanic verification — CONFIRMED:**
- Real UD "Spin to Win" archetype using two-handed sword + Whirlwind + Blizzard + "Spell Activation while Channeling" rune
- Multi-season persistence: Season 3 + Season 5 + Season 7 YouTube guides all reference this pattern
- Also documented in ProGameGuides Whirlwind builds compendium

**live URL(s):**
- https://www.pocketgamer.com/undecember/builds/ — Pocket Gamer Season 7 builds hub (already in row)
- https://www.youtube.com/watch?v=eTlVN1vddpY — "Whirlwind + Blizzard | Top 1 Hardcore | Season 5 Guide"
- https://progameguides.com/undecember/best-undecember-whirlwind-builds/ — ProGameGuides Whirlwind builds compendium
- https://www.youtube.com/watch?v=VfLl_3_imnY — "Whirlwind + Cold Outburst 458M DPS End Game Build" (Season)

**evidence quote (mechanic):** Pocket Gamer + Season 5 YouTube (via WebSearch): "The Whirlwind/Blizzard build uses a two-handed sword, where you cast Whirlwind to start spinning and with the help of the rune 'Spell Activation while Channeling', proc Blizzard to rain down projectiles on opponents."

**Docket compound-vocab concern:** the docket noted "folk_name compound 'Whirlwind CwC Blizzard' mixes vocabularies (PoE-native 'CwC' = Cast-while-Channeling)." Verification confirms this is community-idiomatic vocabulary bleed from PoE ("CwC" is a compact community shorthand for the Cast-while-Channeling pattern), NOT a phantom trigger. UD's "Spell Activation while Channeling" rune IS the CwC-analog mechanism.

**"Ya55" attribution:** the (Ya55) suffix in the folk_name is likely a community-figure attribution similar to Daimonios in kit #11 — a build designer/streamer name. Not verified independently, but the mechanic is verified regardless of attribution.

**Landed vocab mapping:** Cold/ice damage (Blizzard) + physical damage (Whirlwind). Cold slow adjacent — landed. Not primary CC beyond cold-slow lineage.

---

### 13. `tli-iris2-thunder-magus` — "Iris 2 Thunder Magus Minions"

**disposition:** **verified-authentic**
**target action for Elrond:** no correction required (has 1 URL — mmoexp.com; sole-source per S10 but multi-source guide corpus corroborates strongly). Optional flag `mh-v3-recrawl-verified-2026-07-17:legolas`.

**corpus row context:**
- `kit_id`: `tli-iris2-thunder-magus`
- `folk_name`: `Iris 2 Thunder Magus Minions`
- `game`: `tli` (Torchlight: Infinite)
- `provenance_tag`: `mobile-harvest-v3`
- `source_date`: `2026-07-12`
- `source_urls`: `["https://www.mmoexp.com/News/torchlight-infinite-season-13-afterlight-tier-list-best-starter-builds-and-top-endgame-builds-for-high-investment.html"]` (sole-source per S10 signal)

**Entity existence — CONFIRMED:**
- Torchlight: Infinite is a real game; Iris is a real hero character
- "Iris 2" is a real second-ascendancy version of the Iris hero (canonical TLI mechanic)

**Mechanic verification — CONFIRMED:**
- Iris 2 identity: "second ascendancy version that players can transition to from Iris 1"
- Thunder Magus minion build is a real archetype: "hero fusing with spirits to actively control the battle, unlike typical summoner builds. This build delivers powerful performance through attack speed, defense, and various synergy effects, maximizing damage centered around Thunder Magnus' ultimate attack"
- Multi-season persistence: SS7 + SS9 + SS11 + Season 13 (Afterlight) all reference Iris 2 Thunder Magus builds

**live URL(s):**
- https://www.mmoexp.com/News/torchlight-infinite-season-13-afterlight-tier-list-best-starter-builds-and-top-endgame-builds-for-high-investment.html — MMOexp Season 13 tier list (already in row)
- https://www.herowik.gg/ss7-iris2-fire-spirit — herowik.gg SS7 Iris 2 Fire Spirit leveling guide
- https://www.herowik.gg/ — herowik.gg TLI hero guides hub
- https://vortexgaming.io/en/postdetail/523272 — Vortex Gaming Season 9 (Outlaw) Iris 2 build guide
- https://vortexgaming.io/en/postdetail/647546 — Vortex Gaming Season 11 Iris 2 Minion Build Guide (new meta)
- https://tlidb.com/Iris — Torchlight: Infinite Wiki Iris hero entry
- https://www.youtube.com/watch?v=5VTNlNHHjSY — YouTube "[TLI] IRIS BUILD GUIDE - SSF to traveler 7 - Thunder Magi minions"
- https://www.youtube.com/watch?v=anffUbhsZ6Q — YouTube "Iris Thunder Magus T8 Build Day 1 - Changes To Survive - TLI SS9"
- https://www.youtube.com/watch?v=0jZI9SN6i0k — YouTube "[TL:I] Iris Thunder Spirit - My Torchlight: Infinite Starter, Full Build Guide"

**evidence quote (mechanic):** Vortex Gaming Season 11 guide (via WebSearch): "Iris 2 is a second ascendancy version that players can transition to from Iris 1. The Iris 2 build focuses on the hero fusing with spirits to actively control the battle, unlike typical summoner builds. This build delivers powerful performance through attack speed, defense, and various synergy effects, maximizing damage centered around Thunder Magnus' ultimate attack."

**Sole-source concern dissolved:** mmoexp.com was sole source per docket S10 signal; multi-source verification (herowik.gg + vortexgaming.io + tlidb.com + 3 YouTube guides across SS7/SS9/SS11) removes the sole-source risk.

**Landed vocab mapping:** Thunder/lightning damage (element) + minion-based combat (adjacent to summoner archetype). Not primary CC.

---

## Provenance-integrity summary

**Row count:** 13 rows in this sheet. 13 marked with dispositions: 12 verified-authentic + 1 re-key-clean + 0 phantom + 0 unverifiable. Matches index summary block. No discrepancy.

**Phantom finding count:** **ZERO** phantom kits in the HIGH-tier batch. This is materially reassuring for the systemic-risk hypothesis: the two known phantoms (`d2-wl-void-rift`, `di-spiritform-druid-pvp`) appear to be outliers rather than tips of a systematic corruption iceberg. Signal-ranking correctly SURFACED risk, but 13/13 kits with HIGH-risk signal profile VERIFIED under widened-scope re-crawl.

**Re-key finding:** ONE re-key-clean candidate (`d2-ghost-pvp` → `d2-ghost-assassin-pvp`) — a real archetype whose bare `Ghost` folk_name creates classifier ambiguity. Re-key preserves atlas signal + resolves ambiguity without breaking 585-conservation.

**Recommendation for elrond and gandalf-prime:**
- Apply the single re-key-clean action to `d2-ghost-pvp` per §4 of this sheet
- Populate source_urls fields for the 5 kits currently with empty source_urls (kits #1, #2, #3, #4, #10) per URLs enumerated in each section — mob-harvest-v3's default state was no-source, and this re-crawl produces sourced URLs for the newly-verified kits
- Optionally add `mh-v3-recrawl-verified-2026-07-17:legolas` flag to all 12 verified-authentic kits + the 1 re-keyed kit for audit traceability
- Downgrade the mob-harvest-v3 corpus-wide audit priority: HIGH-tier verified 12/13 authentic + 1/13 re-key + 0/13 phantom = signal-ranked-risk did not correlate to phantom-hood at HIGH tier
- MEDIUM tier (37 kits) verification is now DEFERRED per triage docket §9 threshold ("HIGH-tier finds 0-2 phantoms → MEDIUM+LOW deferred to on-demand")

**No new-shape or landed-vocab-extension proposals** — all 13 kits map to existing landed vocabulary.

---

**Final row-count self-audit:** 13 rows expected in application-sheet, 13 rows present, 13 marked with disposition (12 verified-authentic + 1 re-key-clean + 0 phantom + 0 unverifiable). Summary block counts match. No discrepancy.
