# Mint Kit Dossier — d3-call-of-the-ancients

**corpus_kit_id:** `d3-call-of-the-ancients`
**folk_name:** Call of the Ancients Barbarian / IK Ancients Barbarian
**game:** d3
**status:** positive
**era_year:** 2017
**stabilization_patch:** v2.6.1 (October 2017 — Immortal King set major buffs cemented the CotA loop as a dominant identity)
**for_roster_kits:** K5
**mint_priority:** HIGH
**authored:** legolas, 2026-07-13
**dossier_class:** paste-ready (S1 parallel track, elrond ingest)

---

## Provenance + Genre Lineage

Call of the Ancients (CotA) is a Diablo 3 Barbarian skill that summons three named ancestral warriors — Talic (whirlwind specialist), Korlic (leap specialist), and Madawc (multi-hit specialist) — to fight alongside the player for a duration. It descends from D2's "Grin of the Ancients" lore and the D2 Necromancer skeleton army archetype (heavy proxy), but represents a "proxy-light" design: the ancestral warriors fight alongside the Barbarian rather than replacing the Barbarian as the primary damage actor.

The build identity crystallized with the Immortal King (IK) 6-piece set, whose "Endless Wrath" bonus makes both Wrath of the Berserker (WotB) and Call of the Ancients permanent as long as the player spends Fury with attacks. The 6-piece bonus (4,000% damage increase when both skills are active) effectively turns CotA into a permanent summon, removing the call/expire temporal loop and making the ancestral warriors a persistent presence during combat. This is a design divergence from the native CotA behavior (temporal burst), producing two distinguishable kit identities: CotA-standalone (proxy-light temporal burst) and IK-CotA (proxy-light permanent).

Genre lineage: D2 Act V Anya's "Call to the Ancients" lore (narrative ancestor, not mechanical); D3 vanilla Barbarian (2012, CotA exists as standalone cooldown skill); RoS-era IK set rework (2014+) created the permanent-proxy variant; patch 2.6.1 (2017) was the dominant era.

## Era + Build-Version History

| Era | Game version | Notable event |
|---|---|---|
| May 2012 | Diablo 3 launch (v1.0) | Call of the Ancients introduced as Barbarian skill; cooldown-based, temporary summon; not dominant build element |
| March 2014 | Reaper of Souls (v2.0) | Adventure Mode + Greater Rifts introduced; IK set existed but CotA not yet dominant anchor |
| April 2016 | v2.4.0 (Patch 2.4 / Season 5) | Barbarian set reworks; IK set received significant changes |
| October 2017 | **v2.6.1** (Season 12) | **Stabilization** — IK 4-piece reduces WotB/CotA cooldown by 3s per 10 Fury spent; IK 6-piece = 4,000% bonus damage when BOTH active. "Overhaul of the guide to reflect the 2.6.1 buffs that made this build the best build of the season for Barbarians" (Icy Veins changelog) |
| October 2017 | v2.6.4 (Season 12 cont.) | IK 6-piece damage bonus nearly tripled again; IK HotA Barbarian = top Barbarian build |
| 2018–2026 | v2.7.x (ongoing) | IK HotA Barbarian remains viable; updated guides for Seasons 29/37/39 (patches 2.7.6–2.7.8) |

## Mechanical Identity

The IK CotA Barbarian summons three named ancestral warriors (Talic, Korlic, Madawc) and simultaneously activates Wrath of the Berserker, then sustains both permanently by spending Fury via attacks (each 10 Fury spent reduces both cooldowns by 3 seconds, enabling indefinite refresh). The player is the primary damage actor using Hammer of the Ancients (HotA) while the three ancestors fight alongside. The "proxy-light" classification captures this accurately: ancestors augment but do not replace the Barbarian's own contribution.

K5 (roster proxy-light STR anchor) maps to this kit — the genus-defining "STR melee hero with persistent ancestral companions." The corpus evidence note describes this accurately: "K5 proxy-light classification; ancestors augment but don't replace player."

## Engine-Prefix Claims

| Slot | Value | Confidence | Evidence |
|---|---|---|---|
| attr | STR | HIGH | Barbarian class = STR primary archetype throughout D3; all Barbarian skills and sets benefit from Strength (primary stat increases damage) |
| range | melee | HIGH | Barbarian plays in melee range; Hammer of the Ancients and Wrath of the Berserker are melee skills; ancestors fight at melee range |
| tempo | low | MED | Player input cadence during optimal IK HotA play is moderate-low: build sequences cooldown refresh via Fury-spending rather than high-frequency input. Some spikiness during WotB activation phases. Note: "high" was tagged in megaprobe (likely referencing burst-window cadence); MED is the more accurate IK-CotA engagement tempo |
| amp | spiky | MED | IK 6-piece bonus only active when BOTH WotB and CotA are up (the summon window); damage outside the window drops dramatically. Within the window, HotA hits are very high. Burst-window identity = spiky amplitude pattern. |
| proxy | light | MED | Ancestors fight alongside but player (via HotA) is the primary DPS contributor; the set explicitly synergizes player damage while both skills are active rather than delegating to ancestors. |
| commit | instant | HIGH | CotA cast is instant (no wind-up or channel); instant summon call. |

## Raw Descriptors

**geo:** At-target summon: player targets a location and the three ancestors materialize there. They roam a large zone (~25-unit radius from cast point) chasing enemies autonomously. The ancestors have distinct behaviors (Talic whirls, Korlic leaps, Madawc multi-strikes). Large-zone effective footprint.

**ctrl:** No meaningful crowd control; ancestors do not crowd-control enemies. WotB provides player a brief CC-immunity window (fear/stun immunity). CotA provides no CC.

**mob:** Barbarian has full movement freedom during CotA; no movement restriction imposed by the summon mechanic. The core loop involves the Barbarian dashing/leaping into melee (using skills like Furious Charge or Leap) with ancestors following autonomously.

**def:** Immortal King set provides: "damage reduced by 50%" from the Aughild's set bonus (commonly run in conjunction). Barbarian defense is high HP + mitigation; not an evasion build. Wrath of the Berserker provides brief invulnerability frames on activation in some rune configurations.

**econ:** Fury economy. Fury is generated by attacking; the IK 4-piece set converts Fury spending into cooldown reduction for WotB and CotA, creating a perpetual resource loop. Resource ceiling: Fury pool (capped at ~100 base). Cooldown refresh cadence: with 100 Fury and standard attack speed, both cooldowns are sustainably managed.

**elem:** Physical primary (Hammer of the Ancients baseline). Common elemental overlays: Bane of the Trapped (physical amplification); fire/cold conversion via Flavor of Time and Obsidian Ring of the Zodiac (situational). Ancestors' own damage types mirror Barbarian's equipped weapon/gems.

## Sources (live URLs)

- [IK HotA Barbarian Build — Icy Veins](https://www.icy-veins.com/d3/barbarian-hota-build-with-immortal-king) — primary build documentation; confirms 2.6.1 buff history and set bonus mechanics (LIVE — fetched 2026-07-13)
- [IK HotA Barbarian Guide Season 39 — Maxroll](https://maxroll.gg/d3/guides/ik-hota-barbarian-guide) — current meta documentation with skill setup showing CotA "Together as One" rune (LIVE — confirmed in search 2026-07-13)
- [IK Charge Barbarian Guide — Maxroll](https://maxroll.gg/d3/guides/ik-charge-barbarian-guide) — alternate IK variant showing longevity of set (LIVE)
- [S16 IK HotA — DiabloFans](https://www.diablofans.com/builds/101972-s16-immortal-king-hammer-of-the-ancients) — Season 16 (2019) historical documentation (LIVE)
- [IK HotA 2.6.4 Guide — Odealo](https://odealo.com/articles/the-best-barbarian-build-for-season-12-diablo-3-patch-2-6-1) — patch 2.6.4 era guide; notes 2.6.1 as the buff wave (LIVE)

## Knowledge Gaps

- Elrond reconcile needed: is this a distinct corpus row from any existing `d3-ik-hota` record, or should this be a proxy-lens note on an existing entry? Recommendation: DISTINCT ROW focused on proxy-light classification (the CotA summoning identity as a standalone pattern, even if the canonical chassis uses HotA as the primary DPS vehicle)
- Exact Fury thresholds for permanent CotA maintenance not verified via live source (known from training data: 4-piece = 3s reduction per 10 Fury)
- Season 39 viability tier not specifically measured (Icy Veins labels it "mid-tier solo GR" as of patch 2.7.8 Season 39)
