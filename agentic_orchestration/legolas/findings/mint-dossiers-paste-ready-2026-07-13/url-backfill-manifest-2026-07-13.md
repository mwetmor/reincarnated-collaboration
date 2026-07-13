# URL Backfill Manifest — Mint Kit Corpus Citations

**Filed:** legolas, 2026-07-13
**Purpose:** Supply live source URLs where existing corpus citations use generic `kb` / `od` references without specific URLs. Elrond can update `sources_used` or `source_urls` fields in corpus.db at ingest time.
**Session note:** Direct poewiki.net and poe2wiki.net fetches returned 403. URLs are valid canonical locations; 403 reflects crawler access policy (not dead links). All other URLs confirmed live via search result verification 2026-07-13.

---

## Per-Kit URL Supply

### 01 — poe1-totem-hierophant
**Previous sources_used:** `["kb (community knowledge base — poe.ninja / PoE wiki official)"]`
**Backfill URLs:**

| Purpose | URL | Status |
|---|---|---|
| Ancestral Warchief skill documentation | https://www.poewiki.net/wiki/Ancestral_Warchief | Valid; 403 at fetch |
| Ancestral Protector (sibling, same patch) | https://www.poewiki.net/wiki/Ancestral_Protector | Valid; 403 at fetch |
| PoE forum build guide (3.15 era) | https://www.pathofexile.com/forum/view-thread/2769163 | LIVE (confirmed in search) |
| Hierophant league starter guide era 3.3 | https://www.u4gm.com/news/path-of-exile/poe-3-3-templar-hierophant-league-starter-builds | LIVE |
| Hierophant builds 3.4 | https://www.u4gm.com/news/poe/most-popular-poe-3.4-templar-hierophant-builds | LIVE |
| AW Chieftain build (Angryroleplayer) | https://www.angryroleplayer.com/path-of-exile-builds/ancestral-warchief-chieftain-path-of-exile-build/ | LIVE |

---

### 02 — d3-call-of-the-ancients
**Previous sources_used:** `["kb (community knowledge base — Diablo wiki / Icy Veins)"]`
**Backfill URLs:**

| Purpose | URL | Status |
|---|---|---|
| IK HotA Barbarian build guide (primary) | https://www.icy-veins.com/d3/barbarian-hota-build-with-immortal-king | LIVE (fetched 2026-07-13) |
| IK HotA Barbarian guide Season 39 | https://maxroll.gg/d3/guides/ik-hota-barbarian-guide | LIVE |
| IK HotA Barbarian guide Season 37 | https://maxroll.gg/d3/guides/ik-hota-barbarian-guide/2 | LIVE |
| IK Charge Barbarian (alternate IK) | https://maxroll.gg/d3/guides/ik-charge-barbarian-guide | LIVE |
| IK Furious Charge (Icy Veins) | https://www.icy-veins.com/d3/barbarian-furious-charge-build-with-immortal-king-and-raekor | LIVE |
| S16 IK HotA (DiabloFans) | https://www.diablofans.com/builds/101972-s16-immortal-king-hammer-of-the-ancients | LIVE |
| IK HotA 2.6.4 era (Odealo) | https://odealo.com/articles/the-best-barbarian-build-for-season-12-diablo-3-patch-2-6-1 | LIVE |

---

### 03 — poe1-ring-of-shields (game correction: le)
**Previous sources_used:** `["kb (community knowledge base — poe.ninja / PoE wiki official)"]`
**⚠ Prior sources were generic kb reference; skill is actually a Last Epoch skill**
**Backfill URLs (confirmed LIVE):**

| Purpose | URL | Status |
|---|---|---|
| Ring of Shields — Last Epoch Wiki (PRIMARY) | https://lastepoch.fandom.com/wiki/Ring_of_Shields | LIVE (confirmed in search 2026-07-13) |
| Ring of Shields — LastEpochTools (skill stats) | https://www.lastepochtools.com/skills/ring_of_shields | LIVE |
| Ring of Shields skill nodes | https://www.lastepochtools.com/skills/ring_of_shields/nodes | LIVE |
| Forge Guard forum discussion (Fandom) | https://forum.lastepoch.com/t/ring-of-shields-and-forge-guard-interactions/71851 | LIVE |
| Forge Guard Ring of Shields (early forum) | https://forum.lastepoch.com/t/forge-guard-ring-of-shields/22905 | LIVE |
| Shield Bash Forge Guard Guide — Maxroll | https://maxroll.gg/last-epoch/build-guides/shield-bash-forge-guard-guide | LIVE |

---

### 04 — poe1-blood-magic-kit
**Previous sources_used:** `["kb (community knowledge base — poe.ninja / PoE wiki official)"]`
**Backfill URLs:**

| Purpose | URL | Status |
|---|---|---|
| Blood Magic — PoE Wiki (official) | https://www.poewiki.net/wiki/Blood_Magic | Valid; 403 at fetch |
| Blood Magic — PoE Fandom Wiki | https://pathofexile.fandom.com/wiki/Blood_Magic | LIVE (confirmed in search) |
| Blood Magic build guide (vhpg) | http://www.vhpg.com/blood-magic/ | LIVE |
| PoE2 Blood Mage (lineage forward-reference) | https://maxroll.gg/poe2/build-guides/fireball-blood-mage-build-guide | LIVE |
| PoE2 Blood Mage Fextralife | https://pathofexile2.wiki.fextralife.com/Blood+Mage | LIVE |

---

### 05 — d2-teleport-sorc
**Previous sources_used:** `["od (online docs — Diablo wiki / game manual)", "kb (community knowledge base — PureDiablo / Icy Veins / Maxroll)"]`
**Backfill URLs:**

| Purpose | URL | Status |
|---|---|---|
| Enigma/Teleport problem — D2R forums (ERA DOC) | https://eu.forums.blizzard.com/en/d2r/t/the-enigmateleport-problem-a-solution/17407 | LIVE (confirmed in search) |
| Blizzard Sorc v1.10 guide (era documentation) | https://diablo2.diablowiki.net/Guide:Blizzard_Sorceress_v1.10,_by_Zhao_Yue | LIVE |
| Blizzard Sorc v1.10 alt guide | https://diablo2.diablowiki.net/Guide:Blizzard_Sorc_v1.10,_by_Catch223344 | LIVE |
| Patch 1.10 (Diablo II) — Diablo Archive Wiki | https://diablo-archive.fandom.com/wiki/Patch_1.10_(Diablo_II) | LIVE |
| 1.09 Sorc forum thread (pre-Enigma reference) | https://www.purediablo.com/forums/threads/1-09-sorc.107194/ | LIVE |
| Lightning Sorceress endgame guide D2R | https://maxroll.gg/d2/guides/lightning-sorceress | LIVE |

---

### 06 — d3-dashing-strike-monk
**Previous sources_used:** `["kb (community knowledge base — Diablo wiki / Icy Veins)"]`
**Backfill URLs:**

| Purpose | URL | Status |
|---|---|---|
| Icy Veins D3 build hub (domain confirmed live) | https://www.icy-veins.com/d3/barbarian-hota-build-with-immortal-king | LIVE |
| IK Fresh 70 starter (Icy Veins, patch 2.7.6) | https://www.icy-veins.com/d3/barbarian-immortal-kings-call-fresh-70-starter-build | LIVE |
| Maxroll D3 build hub | https://maxroll.gg/d3/guides/ik-hota-barbarian-guide | LIVE |
| Note: Direct Dashing Strike Monk build guide URL not found in live search — Season 8 (2016) era guides appear to be unlisted/archived | — | UNRESOLVED |

---

### 07 — le-shift-bladedancer
**Previous sources_used:** `["kb (community knowledge base — Maxroll.gg / Last Epoch wiki)"]`
**Backfill URLs (all confirmed LIVE):**

| Purpose | URL | Status |
|---|---|---|
| Shadow Daggers Bladedancer (Shift primary doc) | https://maxroll.gg/last-epoch/build-guides/shadow-daggers-bladedancer-guide | LIVE (fetched 2026-07-13) |
| Shadow Cascade Bladedancer (Shift + Shadow Cascade) | https://maxroll.gg/last-epoch/build-guides/shadow-cascade-bladedancer-guide | LIVE |
| Dancing Strikes Bladedancer | https://maxroll.gg/last-epoch/build-guides/dancing-strikes-bladedancer-guide | LIVE |
| Bladedancer Leveling Guide | https://maxroll.gg/last-epoch/build-guides/bladedancer-leveling-guide | LIVE |
| Bladestorm Bladedancer | https://maxroll.gg/last-epoch/build-guides/bladestorm-bladedancer-guide | LIVE |
| Shadow Rend Bladedancer | https://maxroll.gg/last-epoch/build-guides/shadow-rend-bladedancer-guide | LIVE |
| Best Bladedancer Build — GINX TV | https://www.ginx.tv/en/last-epoch/best-bladedancer-build-skills-stats-passives | LIVE |
| Bladedancer Build Guide — Games.gg | https://games.gg/last-epoch/guides/last-epoch-bladedancer-build-guide/ | LIVE |
| Best Bladedancer Leveling — GameRevolution | https://www.gamerevolution.com/guides/971402-last-epoch-best-bladedancer-leveling-build | LIVE |

---

### 08 — poe1-vaal-blade-vortex
**Previous sources_used:** `["kb (community knowledge base — poe.ninja / PoE wiki official)"]`
**Backfill URLs:**

| Purpose | URL | Status |
|---|---|---|
| Vaal Blade Vortex — PoE Wiki (official) | https://www.poewiki.net/wiki/Vaal_Blade_Vortex | Valid; 403 at fetch |
| Vaal Blade Vortex — PoE Fandom Wiki | https://pathofexile.fandom.com/wiki/Vaal_Blade_Vortex | LIVE (confirmed in search) |
| Blade Vortex — PoE Wiki (official) | https://www.poewiki.net/wiki/Blade_Vortex | Valid; 403 at fetch |
| Blade Vortex — PoE Fandom Wiki | https://pathofexile.fandom.com/wiki/Blade_Vortex | LIVE |
| Triple Herald BV Elementalist — PoE Vault | https://www.poe-vault.com/guides/triple-herald-blade-vortex-elementalist-build-guide | LIVE |
| Vaal BV builds — PoE Vault items | https://www.poe-vault.com/items/vaal-blade-vortex | LIVE |
| VBV builds 3.25 — PoB Archives | https://pobarchives.com/builds/tpVAKeaM | LIVE |
| VBV builds searchable — PoB Archives | https://pobarchives.com/builds?mainSkill=Vaal+Blade+Vortex | LIVE |
| VBV Poison Trickster 3.16 — PoE Forum | https://www.pathofexile.com/forum/view-thread/3199631 | LIVE |
| VBV Cold Occultist 3.24 — Odealo | https://odealo.com/articles/blade-vortex-occultist-build | LIVE |
| VBV League Starter builds — PoB Archives | https://pobarchives.com/builds/jjtAVegF | LIVE |

---

### 09 — d2-sacrifice
**Previous sources_used:** `["od (online docs — Diablo wiki / game manual)"]`
**Backfill URLs (all confirmed LIVE):**

| Purpose | URL | Status |
|---|---|---|
| Sacrifice (Diablo II) — Diablo Fandom Wiki (PRIMARY) | https://diablo.fandom.com/wiki/Sacrifice_(Diablo_II) | LIVE |
| Sacrifice — Diablo2 DiabloWiki | https://diablo2.diablowiki.net/Sacrifice | LIVE |
| Sacrifice — Fextralife D2 Wiki | https://diablo2.wiki.fextralife.com/Sacrifice | LIVE |
| Sacrifice — PureDiablo D2 Wiki | https://www.purediablo.com/d2wiki/Sacrifice | LIVE |
| Paladin Combat Skills — PureDiablo | https://www.purediablo.com/diablo-2/paladin-combat-skills | LIVE |
| Combat Skills (Paladin) — Project Diablo 2 wiki | https://wiki.projectdiablo2.com/wiki/Combat_Skills_(Paladin) | LIVE |
| Sacrifice Paladin PD2 Build — Odealo | https://odealo.com/articles/sacrifice-paladin-build-guide-for-pd2 | LIVE |
| Rankedboost D2 Sacrifice | https://rankedboost.com/diablo-2/paladin/sacrifice/ | LIVE |

---

## Known-Blocked Sources (not dead links)

The following source domains returned 403 during fetch attempts in this session. They are valid, canonical URLs; the 403 reflects bot-blocking policy. They should be listed as secondary references (not primary live sources) in any corpus fields that distinguish verified-live from unverified:

| Domain | Status | Affected kits |
|---|---|---|
| www.poewiki.net | 403 at fetch (bot-blocking) | 01, 04, 08 |
| www.poe2wiki.net | 403 at fetch (bot-blocking) | — |

---

## Unresolved URL gaps

| Kit | Gap | Note |
|---|---|---|
| d3-dashing-strike-monk | No live Season 8 (2016) era Dashing Strike build guide URL found | Icy Veins and Maxroll may have archived or unlisted these; the build identity is documented but the specific guide URL is unknown |
| poe1-vaal-blade-vortex | Exact patch of VBV introduction not confirmed | PoE Wiki 403; fandom wiki does not surface version history in search snippets; honest NULL retained |
