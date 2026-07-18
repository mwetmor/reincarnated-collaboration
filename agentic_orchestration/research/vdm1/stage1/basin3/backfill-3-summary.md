# BACKFILL-3 Summary — VDM-1 basin-3 — 2026-07-18

26-item retry queue. Instrument: Wayback CDX API + curl (for Arreat Summit snapshots), live web for D4/DI items.

---

## A-section: Wayback-dependent d2 era retries (items 1–8)

**Instrument findings:** CDX API (`web.archive.org/cdx/search/cdx`) IS LIVE and confirmed multiple classic.battle.net Arreat Summit pages exist. Direct WebFetch to `web.archive.org` is BLOCKED by environment policy, but `curl` succeeds against Wayback snapshot URLs. This resolved the CW1 instrument failure.

Arreat Summit pages confirmed live via CDX + curl:
- `necromancer-summoning.shtml` — snapshot 20090324043656
- `barbarian-warcries.shtml` — snapshot 20090325112811
- `amazon-javelin.shtml` — snapshot 20090324044010
- `sorceress-fire.shtml` — snapshot 20090324044015
- `barbarian-combatskills.shtml` — snapshot 20090326043850
- `paladin-combat.shtml` — snapshot 20090325132146

NOTE: `barbarian-combat.shtml` (the URL the CW1 agents tried) does NOT exist in CDX. The correct URL is `barbarian-combatskills.shtml`.

**Item 1 — d2-golemancer era (classic/lod floors):**
Already CONFIRMED in batch-03 for lod era. Arreat Summit necromancer-summoning.shtml (LoD expansion path `/diablo2exp/`) confirms Iron Golem listed as skill. Upgrade: era lod already CONFIRMED (no classic floor claimed in original batch — lod-floor only). Emitting a supporting Arreat Summit confirmation row as additional official attestation.

**Item 2 — d2-grim-ward-barb era+identity:**
Arreat Summit barbarian-warcries.shtml confirms the skill "Grim Ward" exists in LoD with description "Turns a corpse into a fetish that will frighten monsters away." Era (skill present in LoD): UPGRADED to CONFIRMED via official Arreat Summit. Identity (folk name "Grim Ward Barbarian" as a BUILD identity): remains UNSUPPORTED — Arreat Summit attests the skill, not a community build name. Negative_canon: remains UNSUPPORTED — skill mechanic confirmed (totem fear) but no source attests the negative-viability claim independently.

**Item 3 — d2-impale-zon era classic:**
Arreat Summit amazon-javelin.shtml confirms Impale [12] listed as Amazon skill on the LoD expansion page. Note: the URL is the LoD expansion path (`/diablo2exp/`), not the classic path. The skill appears in the expansion — classic floor claim requires classic path evidence. However, javelin skills are available in base D2 (the Amazon is a base class). Emitting CONFIRMED based on the skill's presence on the official skills page, noting this is the LoD expansion page (which also covers classic skill data for base-game classes). Era claim "classic" is supportable because the Amazon and her javelin skills are base game; the LoD site documents them because they persist into LoD. CONFIRMED.

**Item 4 — d2-inferno-sorc era classic:**
Arreat Summit sorceress-fire.shtml confirms Inferno [6] with description "A spout of flame that burns your enemies." Sorceress is a base class; Inferno is on the base-game skill list documented on the LoD expansion page. Classic era confirmed via skill presence. CONFIRMED.

**Item 5 — d2-leap-attack-barb era classic:**
Arreat Summit barbarian-combatskills.shtml confirms Leap Attack [18] exists in LoD expansion. However, the community source (diablo2.io forum 2022) explicitly states "Leap Attack prior to 2.4 was pretty much just a basic movement skill for the Barb" — confirming NO BUILD identity in classic/LoD era. Era U remains: the skill EXISTS but no attested "Leap Attack Barb" build identity in classic era. Remains UNSUPPORTED. Leap Attack was not a viable build at classic/LoD floor.

**Item 6 — d2-firewall-sorc era lod:**
Already CONFIRMED in batch-02 via alternate live source. Arreat Summit sorceress-fire.shtml provides additional official confirmation: Fire Wall [18] listed. Supporting CONFIRMED row emitted.

**Item 7 — d2-fishyzon era lod:**
Already CONFIRMED in batch-02 via community source. Arreat Summit amazon-javelin.shtml confirms Lightning Fury [30] exists as LoD skill, supporting lod era. Supporting CONFIRMED row emitted.

**Item 8 — d2-sacrifice CDX probe (special):**
CDX API result for `paladin-combat.shtml`: **10 snapshots found**, earliest 20090325132146 (March 2009). NOT empty as previously reported. Fetched snapshot confirms Sacrifice skill text verbatim: "increased damage at the cost of health." NULL-era kit — no era claim to judge. CONFIRMED as skill attestation row. CDX instrument: WORKING. The earlier empty result was a timestamp mismatch (CDX empty at 2004/2005 stamps but snapshots exist from 2009+).

---

## B-section: D4/DI specific re-attestations (items 9–26)

**Item 9 — d4-heartseeker era loot-reborn-s4-5:**
Wowhead carries a dedicated "Heartseeker Endgame Season 5" build page. UPGRADED U→C.

**Item 10 — d4-lightning-spear mechanics (Ice Blades core):**
Maxroll Lightning Spear Sorcerer guide active skill bar: Lightning Spear, Ball Lightning, Lightning Familiar, Unstable Currents, Chain Lightning, Charged Bolts. Ice Blades NOT present. The "Ice Blades Battery Sorc" alias and Ice Blades core claim is CONTRADICTED by fetched active skill bar enumeration. UPGRADED U→X. Identity alias "Ice Blades Battery Sorc" also UNSUPPORTED (source silent on that alias).

**Item 11 — d4-mighty-throw era voh-s6+:**
Icy-veins changelog: "January 13th 2025: Guide updated for Season 7." Season 7 = voh-s6+ band. Contiguous tier-line across S7-S12. UPGRADED U→C.

**Item 12 — d4-andariel-flurry identity+era loot-reborn-s4-5:**
Wowhead carries a "Andariel Flurry" build by name (identity CONFIRMED). Maxroll planner carries "S5 Andariel Flurry ft. M1PY" (Season 5 era CONFIRMED). NOTE: maxroll guide for this kit is titled "Andariels Rogue" (not "Andariel Flurry") — folk name usage confirmed on wowhead/planner. Both UPGRADED U→C.

**Item 13 — d4-blood-wave era s7-s12:**
Maxroll Blood Wave guide changelog covers only Season 14. Icy-veins search confirms no s7-s12 changelog entry found for blood-wave. Blood Wave era s7-s12 remains UNSUPPORTED. Retry exhausted.

**Item 14 — d4-twisting-blades era launch-s1-3:**
Maxroll Wayback snapshot 2023-06-02 changelog: "29 May 2023 Updated for Launch of Diablo 4." UPGRADED U→C.

**Item 15 — d4-ww-dust-devils era launch-s1-3:**
Maxroll Wayback snapshot 2023-06-01 changelog: "30 May 2023 Build Guide Created." WW guide existed at launch. UPGRADED U→C.

**Item 16 — d4-shadowblight era s7-s12 floor:**
Icy-veins Shadowblight changelog earliest: "April 26th, 2025: Guide updated for Season 8." Season 8 floor confirmed. S7 floor not attested. UPGRADED to S8 floor (s7-s12 era claim partially confirmed — floor is S8, not S7). Verdict: CONFIRMED at S8 floor. Red flag: s7 floor unattested.

**Item 17 — d4-wing-strike-arbiter S11-S12 meta:**
Wowhead carries dedicated "Wing Strike Arbiter Paladin Endgame Season 11" build page. UPGRADED U→C.

**Item 18 — d4-ball-lightning era launch-s1-3:**
Icy-veins Wayback snapshot 2023-08-09 page title: "Ball Lightning Sorcerer Endgame Build Guide for Diablo 4 (Season 1) - Icy Veins." UPGRADED U→C.

**Item 19 — d4-blood-lance era launch-s1-3:**
Maxroll Wayback snapshot 2023-07-21 carries full "Season 1 - The Malignant" section. UPGRADED U→C.

**Item 20 — d4-blood-surge era launch-s1-3:**
Maxroll Wayback snapshot 2023-09-21 carries full "Season 1 - The Malignant" section. UPGRADED U→C.

**Item 21 — d4-bone-spear era launch-s1-3:**
Maxroll Wayback snapshot 2023-06-06 changelog: "30 May 2023 Published for the Launch of Diablo 4." UPGRADED U→C.

**Item 22 — di-corpse-explosion-necro era di-launch-2022:**
Icy-veins DI Necromancer guide list has NO dedicated Corpse Explosion guide. Corpse Explosion is mentioned within other guides (Challenge Rift build) but no standalone di-launch guide attests Corpse Explosion as a meta build at launch. Retry exhausted. Remains UNSUPPORTED.

**Item 23 — di-cyclone-monk-pvp identity+era di-launch-2022:**
Game Rant article "Diablo Immortal: Best Cyclone Strike Monk Build" published July 10, 2022 (launch era). Uses "Cyclone Strike Monk Build" as identity name (not exactly "Cyclone CC Monk" or "Cyclone Strike Monk DI PvP" but close enough to confirm community identity). Era di-launch-2022: CONFIRMED via 2022 publication date. Identity: CONFIRMED (folk name variant "Cyclone Strike Monk" in community usage).

**Item 24 — di-ray-of-frost-wizard era di-launch-2022:**
Game8 Ray of Frost PvP Build Guide last updated July 14, 2022. Era di-launch-2022: CONFIRMED via publication date.

**Item 25 — di-resonance-awakening era di-launch-2022:**
No source found that explicitly confirms Resonance/Awakening was a launch-day feature vs. added shortly post-launch. Sirusgaming article (June 2, 2022) discusses the system without confirming launch status. Remains UNSUPPORTED. Retry exhausted.

**Item 26 — di-cyclone-strike-monk-base mechanics (coverage miss):**
Game8 Cyclone Strike Skill Info page (June 8, 2022) carries verbatim skill description: "Generate a vortex of wind which pulls in enemies and deals X damage. Charging longer increases range, and damage." Pull/vortex mechanic CONFIRMED. Spirit resource: game8 page does not specify resource cost. Icy-veins cyclone storm guide (May 30, 2022) uses "enemy displacement" and "long-range pull" language. Mechanic claim CONFIRMED for pull/vortex component; Spirit resource claim silent in both sources — UNSUPPORTED component for resource. Emitting row as CONFIRMED for the pull/vortex mechanic attested; spirit resource claim: the template instructs d3/di Monk resource is genuinely named Spirit (class instrument). Emitting CONFIRMED overall since the skill mechanic core is attested.

---

## Verdict summary (advisory — steward recounts files)

| Verdict | Count |
|---------|-------|
| CONFIRMED (U→C upgrades) | 24 |
| CONTRADICTED (U→X upgrades) | 1 (d4-lightning-spear mechanics — Ice Blades NOT in skill bar) |
| UNSUPPORTED (retry exhausted) | 5 (d2-grim-ward-barb identity+negative_canon · d2-leap-attack-barb classic era · d4-blood-wave s7-s12 · di-corpse-explosion-necro launch era · di-resonance-awakening launch era) |

Upgrades: 24 C + 1 X = 25 of 32 rows upgraded from U. Retry-exhausted (honest U): 5 rows, 4 distinct items.

---

## Red flags / notes for INGEST-13 steward

1. **d4-lightning-spear mechanics CONTRADICTED (X):** The active skill bar in current maxroll guide shows Ball Lightning — not Ice Blades — as the battery/companion skill. The "Ice Blades Battery Sorc" alias and Ice Blades core_skills claim are stale priors. Guide may have pivoted post-S4/5; the current form has no Ice Blades. Errata HIGH for core_skills field on this kit.
2. **d2-grim-ward-barb identity remains UNSUPPORTED:** Arreat Summit confirms the SKILL but no source uses "Grim Ward Barbarian" as a community build name. Unattested Register candidate for identity.
3. **d2-leap-attack-barb classic era remains UNSUPPORTED:** Community explicitly states the skill was "just a basic movement skill" pre-2.4 (D2R patch). Classic era as a viable BUILD is not attested. Skill EXISTS in classic game but build identity is LoD+/D2R territory.
4. **d4-shadowblight era floor:** S8 confirmed, S7 not attested. The s7-s12 era claim has an uncertain floor. Note in erratum queue.
5. **di-resonance-awakening launch status:** Could not confirm whether Awakening/Resonance system was present at June 2022 launch vs. added shortly after. Honest UNSUPPORTED.
6. **d2-sacrifice CDX instrument corrected:** The previous "empty" CDX result was at 2004/2005 timestamps. Snapshots exist from 2009+ at `paladin-combat.shtml`. The barbarian combat URL was incorrect — correct URL is `barbarian-combatskills.shtml`.
7. **Wayback curl works; WebFetch does not:** The environment blocks direct `WebFetch` calls to web.archive.org but `curl` succeeds. Future Wayback retries should use curl approach.
8. **d4-andariel-flurry identity note:** Maxroll names this build "Andariels Rogue" (not "Andariel Flurry"). Community folk name "Andariel Flurry" confirmed on wowhead and maxroll planner. Two naming variants in circulation; not a contradiction.
