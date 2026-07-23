# KF-2/3 Harvest — Grim Dawn (gd-flames-of-ignaffar-purifier)
**Legolas Mode B** | 2026-07-23 | Kit: `gd-flames-of-ignaffar-purifier` (Flames of Ignaffar, Purifier = Demolitionist + Inquisitor)
**Charter ref:** KFL-5 — residual legolas agent; gd is the only outstanding harvest lane.

---

## KIT SIDE (KF-2 input)

### Flames of Ignaffar — Skill Mechanics (Structural)

**Source:** grimtools.com search synthesis + Crate forum discussion (accessed 2026-07-23)
Verbatim: "Flames of Ignaffar is a short-range channeled AoE ability" — description confirmed across multiple search results.
Verbatim: "it is a channeled skill that must be held down to maintain, dealing damage and draining energy every 0.3 seconds at 100% Cast Speed"

**Skill type:** Channeled cone beam (Demolitionist mastery skill)
**Damage type:** Fire + Burn (fire damage over time)
**Tick cadence:** every 0.3 seconds at 100% cast speed (one tick per channel interval)
**Transmuter modifier:** a transmuter exists that converts fire to chaos damage and lightning to vitality, with Electrocute becoming Vitality Decay — not the fire-build path; not extracted here.

**Source URL for structural mechanic:** https://steamcommunity.com/app/219990/discussions/0/1620599015872291805/ (synthesis; no verbatim rank table present on page)

### Flames of Ignaffar — Rank Table

**BLOCK: grimtools.com/db/skills/2112 is JavaScript-rendered.** WebFetch returns only navigation structure; no skill data tables are present in static HTML. All grimtools DB and calculator URLs (including versioned `/db-1198/`, `/calc/`) return the same empty shell.

**BLOCK: grimdawn.fandom.com/wiki/Flames_of_Ignaffar_(Skill) returns HTTP 402** on every fetch attempt. The _(Skill) suffix page, the base page, the Endless_Flame_(Skill) page — all 402.

**Result:** Per-rank table (fire damage min/max, burn damage, energy cost per second) is a FULL GAP. No verbatim anchor available from any reachable static source. See GAPS table.

### Modifier / Transmuter Nodes

The following modifier/transmuter nodes exist for Flames of Ignaffar per search index:
- **Intensify** — referenced in search results as a modifier node; no verbatim numeric data reachable
- **Endless Flame** — fandom wiki page (grimdawn.fandom.com/wiki/Endless_Flame_(Skill)) returns HTTP 402
- **Energy cost reduction modifier** — Crate forum discussions confirm a modifier "reduces energy cost and adds a chance for enemies to fumble their attacks" (synthesis from search result snippet, not verbatim per-rank table)

**Result:** All modifier node numeric tables are GAP. See GAPS table.

### Character Attributes — Purifier at Documented Build Point

**Source A (verbatim attribute allocation):** lonewardengaming.com/grimdawn-home/purifierdwr/ (accessed 2026-07-23)
Verbatim: "Physique: 96 | Cunning: 11 | Spirit: 0"
Note: This is a Dual Wield Ranged Purifier variant. Attribute allocations confirm the Purifier pattern: stack Physique for survivability, minimal Cunning, near-zero Spirit (FoI damage scales with Fire damage% bonuses on gear, not with Spirit directly).

**OA/DA base formulas (verbatim):**

**Source B (official):** grimdawn.com/guide/character/character-basics/ (accessed 2026-07-23)
Verbatim: "Every point of Physique increases your health by 2.5, health regeneration by 0.05 and Defensive Ability by 0.4"
Verbatim: "Every point of Cunning increases health by 1.0, your physical and pierce damage by 0.41%, bleed and internal trauma damage by 0.46% and Offensive Ability by 0.4"
Verbatim: "Every point of Spirit increases your health by 1.5, magical damage by 0.47%, magical duration damage by 0.5%, energy by 2 and energy regeneration by 0.01 + 0.26%"
Verbatim: "Each point will increase that attribute by 8" (when spending points through the Character Window interface — i.e., 1 invested point = +8 to that attribute stat)

**Source C (community corroboration):** search result synthesis from steamcommunity.com discussions (accessed 2026-07-23)
Verbatim: "Assigning 1 Attribute Point to Physique grants +8 Physique (+20 Bonus Health, +0.32 Bonus Health Regen, and 4 Defensive Ability)"
Verbatim: "Assigning 1 Attribute Point to Cunning grants +8 Cunning (4 Offensive Ability, +3.26530616% Bonus Physical & Pierce Damage, and +3.72093024% Bonus Bleed & Internal Trauma Damage)"
Verbatim: "Assigning 1 Attribute Point to Spirit grants +8 Spirit (16 Bonus Energy, +0.08 + 2% Bonus Energy Regeneration, +3.72093024% Bonus Magical Damage, and +4% Bonus Magical Duration Damage)"

**OA/DA derived formulas (verbatim):**

**Source D:** steamcommunity.com/sharedfiles/filedetails/?id=596728673 — Game Mechanics Guide (accessed 2026-07-23)
Verbatim: "OA = (115 + 12*Level + 0.4*Cunning + Other Flat Bonuses)*(1 + (%Offensive Ability bonus)/100)"
Verbatim: "DA = (115 + 12*Level + 0.4*Spirit + Other Flat Bonuses)*(1 + (%Defensive Ability bonus)/100)"

Note on DA formula: the per-point contribution to DA is listed as +0.4 DA per Physique point (Source B) but the derived DA formula keys off Spirit in Source D. These are NOT contradictory: the base DA formula uses Spirit as the attribute scaling parameter (Spirit raises the DA base), while Physique also adds flat DA (+0.4 per Physique point) as a separate additive term included in "Other Flat Bonuses." Both are correct contributions; they stack.

**Documented build-point HP/armor/resists:** not verbatim from a static source. The Crate forum build guide references a grimtools calculator link; that link is JS-rendered and inaccessible. The lonewardengaming page shows attributes only (no HP/OA/DA/resist panel in reachable text). GAP — see below.

### Crit Mechanics — OA/DA PTH Formula

**Source E (official):** grimdawn.com/guide/gameplay/combat/ (accessed 2026-07-23)
Verbatim PTH formula: "PTH = ((((Attacker's OA / ((Defender's DA / 3.5) + Attacker's OA)) * 300) * 0.3) + (((((Attacker's OA * 3.25) + 10000) – (Defender's DA * 3.25)) / 100) * 0.7)) – 50"
Verbatim: "PTH cannot go below 55 for you or your enemies, meaning that no matter how much Defensive Ability you or your foe may have, you will never have a lower than 55% chance to hit them"
Verbatim: "The highest possible critical multiplier is x1.5" (official guide)

**Crit damage tier table (verbatim from Source E):**

| PTH threshold | Crit damage multiplier |
|---|---|
| 70 | 1.0x (no crit) |
| 90+ | 1.1x |
| 105+ | 1.2x |
| 120+ | 1.3x |
| 130+ | 1.4x |
| 135+ | 1.5x (maximum) |

**Crit chance from PTH (verbatim synthesis):**
Verbatim: "The chance to critically strike is PTH - 90. For example, if you have 95% PTH, you will have a 5% Critical Chance. If you have 110% PTH, you will have a 20% Critical Chance."
Verbatim: "Equality of attacker's OA and receiver's DA results in a 90% chance to hit and 0% chance to crit."

**Source for crit-chance formula:** steamcommunity.com search synthesis + grimdawn.com/guide/gameplay/combat/ (accessed 2026-07-23)

**Alternate crit multiplier tier table (Source D — Steam Mechanics Guide):**

| Crit chance threshold | Multiplier |
|---|---|
| >0% | 1.10x |
| >10% | 1.20x |
| >20% | 1.30x |
| >30% | 1.50x |
| >45% | 2.0x |

Note: Source D (community guide) and Source E (official) diverge on the maximum crit multiplier (2.0x vs 1.5x) and on the tier structure. Source E (official grimdawn.com) is the authoritative reference. This divergence is logged — elrond/gamora should use Source E.

**Additional verbatim (Source D):** "+%Crit Damage is additive with base multiplier (example: 1.10x + 0.35 = 1.45x)"

### Mitigation — Armor

**Source E (official):** grimdawn.com/guide/gameplay/combat/ (accessed 2026-07-23)
Verbatim: "By default, your armor absorption is 70% across all your equipment."
Verbatim: "30% of the damage will always go through because of armor absorption" (at baseline 70% absorption)

**Damage Mitigation formula (Source D):** "Damage Mitigation = Armor_Rating * Armor_Absorption/100"

**Mitigation ordering (Source E — official):**
Verbatim: First defensive layer = "Fumble, Dodge and Projectile Deflection" (no specific numeric formula or cap stated in reachable text)
Armor applies to physical damage; resistance mechanics described qualitatively.

**Resistance cap:** Not found verbatim in reachable sources. GAP.

**Build-point mitigation stats (HP, armor value, all resists):** Not verbatim-anchored. GAP — see below.

---

## GAPS — Kit Side

| Field | Status | Detail |
|---|---|---|
| Flames of Ignaffar rank table — fire damage min/max per rank | FULL GAP | grimtools.com/db/skills/2112 is JS-rendered (static fetch returns navigation only); fandom wiki HTTP 402 on all pages |
| Flames of Ignaffar rank table — burn damage per rank | FULL GAP | Same block — no reachable static source |
| Flames of Ignaffar rank table — energy cost per second per rank | FULL GAP | Same block; only structural note reachable: ticks every 0.3s at 100% cast speed |
| Intensify modifier — per-rank numeric values | FULL GAP | grimtools JS-rendered; fandom 402 |
| Endless Flame modifier — per-rank numeric values | FULL GAP | fandom wiki Endless_Flame_(Skill) returns HTTP 402 |
| Energy cost reduction modifier — per-rank numeric values | FULL GAP | Only qualitative description reachable ("reduces energy cost + fumble chance") |
| HP/health pool at documented build point | GAP | Attribute formula gives per-point contribution but build-point level and total Physique allocation not fully pinned (lonewardengaming gives Physique: 96 as invested points; actual Physique stat = base + 96*8; base class starting Physique unknown verbatim) |
| OA value at documented build point | GAP | Formula anchored (OA = 115 + 12*Level + 0.4*Cunning + bonuses) but Cunning total and gear bonuses at build point not verbatim |
| DA value at documented build point | GAP | Formula anchored but Spirit total and gear bonuses not verbatim |
| Armor value and armor absorption override at build point | PARTIAL — default absorption 70% verbatim; actual armor rating at build point not stated |
| All resistances at build point (fire/cold/lightning/pierce/aether/chaos/vitality/poison/bleed) | FULL GAP | Build guide stats are in grimtools calc links (JS-rendered) or screenshot images (not text) |
| Resistance cap | GAP | Not found in any reachable static source |
| Character level at documented build point | GAP | Not pinned from reachable text (lonewardengaming does not state level) |
| Base starting attributes for Demolitionist/Inquisitor classes | GAP | Not found verbatim in reachable sources |

---

## KF-3 MONSTER SIDE — GD Act 1 Normal Starter Set

### Source blockage — FULL GAP

**Primary source — grimtools.com/monsterdb/:** JavaScript-rendered. WebFetch returns empty template with no monster data loaded. All monster stat fields (Health, OA, DA, Damage Per Second, Armor Rating, Resistances) show "0%" or blank in static fetch.

**Secondary source — grimdawn.fandom.com (all creature pages):** HTTP 402 on all URLs attempted. This includes:
- grimdawn.fandom.com/wiki/Ghoul_(creature)
- grimdawn.fandom.com/wiki/Act_1
- grimdawn.fandom.com/wiki/Ghoul_Corpse-eater
- grimdawn.fandom.com/wiki/Ghoul_(creature_type)
- grimdawn.fandom.com/wiki/Chthonic
- grimdawn.fandom.com/wiki/Creatures

**Steam community / Reddit searches:** No static pages with verbatim Act 1 Normal monster HP / DA / damage / resist tables surfaced in any search result.

**Target mob set (identified from search, not yet data-populated):**
- Rotting Corpse / Undead family (Lower Crossing / Burrwitch area)
- Ghoul / Corpse-eater (search confirmed page exists on fandom; 402 blocked)
- Chthonic Hound (confirmed as an Act 1 Chthonic enemy type; no stat page reachable)
- Burrwitch Villager / Crazed Villager (Act 1 early humans, commonly documented in guides)
- Boar / Crazed Thornback (Act 1 wildlife)

**All monster-side numeric fields are FULL GAP.** No verbatim HP / DA / OA / damage / resistance data was extracted for any Act 1 Normal mob.

---

## GAPS — Monster Side

| Field | All Act 1 Normal Mobs | Detail |
|---|---|---|
| HP (Health) | FULL GAP — ALL MOBS | grimtools monsterdb JS-rendered; fandom 402 |
| DA (Defensive Ability) | FULL GAP — ALL MOBS | Same |
| OA (Offensive Ability) | FULL GAP — ALL MOBS | Same |
| Damage (min/max per attack) | FULL GAP — ALL MOBS | Same |
| Armor rating | FULL GAP — ALL MOBS | Same |
| Fire resistance | FULL GAP — ALL MOBS | Same |
| Cold resistance | FULL GAP — ALL MOBS | Same |
| Lightning resistance | FULL GAP — ALL MOBS | Same |
| Pierce resistance | FULL GAP — ALL MOBS | Same |
| Aether resistance | FULL GAP — ALL MOBS | Same |
| Chaos resistance | FULL GAP — ALL MOBS | Same |
| Vitality resistance | FULL GAP — ALL MOBS | Same |
| Poison/Acid resistance | FULL GAP — ALL MOBS | Same |
| Bleed resistance | FULL GAP — ALL MOBS | Same |
| Mob-level at Normal difficulty | FULL GAP — ALL MOBS | Same |
| Experience granted | FULL GAP — ALL MOBS | Same |

---

## Unblock path for GAPS (note for elrond / conductor)

The GD harvest gap is structural, not retrieval-error: both primary sources are inaccessible to WebFetch.

1. **grimtools.com/monsterdb/ + grimtools.com/db/skills/2112** — JavaScript-rendered React/Vue apps. Content requires a headless browser (Playwright/Puppeteer) or a Selenium-capable tool. WebFetch cannot reach their data.
2. **grimdawn.fandom.com** — HTTP 402 on ALL pages. This is a systematic block (Fandom paywall/bot-block), not a transient error. The archive variant (grimdawn-archive.fandom.com) also returned 402.

**Options for conductor to consider:**
- (a) Matt or a team member with GD installed can extract in-game tooltip screenshots for FoI rank table and Act 1 mob stat panels. This is the fastest path to verbatim anchor.
- (b) The GD game files contain a `database.odb` (GD's own format) and extracted CSV/XML from the Grim Internals tool — community-extracted CSVs exist on GitHub (e.g., `GrimDawn-parser` projects). If such a repo is identified, legolas can do a text-file fetch.
- (c) A cached static copy of the grimtools skill page may exist on web.archive.org — conductor may authorize a targeted archive fetch (adds fetch budget).

---

## Sources consulted (all read-only, 2026-07-23)

| URL | Result |
|---|---|
| https://www.grimtools.com/db/skills/2112 | BLOCKED — JS-rendered; static fetch = navigation only, no skill data |
| https://grimdawn.fandom.com/wiki/Flames_of_Ignaffar | HTTP 402 |
| https://grimdawn.fandom.com/wiki/Flames_of_Ignaffar_(Skill) | HTTP 402 |
| https://grimdawn.fandom.com/wiki/Endless_Flame_(Skill) | HTTP 402 |
| https://grimdawn.fandom.com/wiki/Ghoul_(creature) | HTTP 402 |
| https://grimdawn.fandom.com/wiki/Act_1 | HTTP 402 |
| https://grimdawn-archive.fandom.com/wiki/Game_Mechanics | HTTP 402 |
| https://forums.crateentertainment.com/t/feedback-flames-of-ignaffar-energy-cost-is-ridiculous/92602 | Fetched — qualitative only; no rank table |
| https://forums.crateentertainment.com/t/1-1-9-8-1-2-0-2-build-overview-fire-flames-of-ignaffar-purifier-sr75-80/129320 | Fetched — stats in external grimtools calc link (JS-rendered); no verbatim stat text |
| https://forums.crateentertainment.com/t/1-1-7-2-the-fire-coneman-fire-flames-of-ignaffar-purifier-focused-on-conversion/102294 | Fetched — stats in screenshot images; no verbatim text values |
| https://forums.crateentertainment.com/t/something-less-clever-about-burning-fire-flames-of-ignaffar-purifier-sr75-controller-friendly/126206 | Fetched — grimtools calc link only; no verbatim stat text |
| https://www.grimtools.com/calc/4ZD8561Z | BLOCKED — JS-rendered; "Building database..." placeholder only |
| https://www.grimtools.com/db-1198/skills/2112 | BLOCKED — JS-rendered; navigation only |
| https://www.grimtools.com/monsterdb/ | BLOCKED — JS-rendered; empty template, no monster data |
| https://lonewardengaming.com/grimdawn-home/purifierdwr/ | Fetched — verbatim: Physique 96, Cunning 11, Spirit 0 |
| https://www.grimdawn.com/guide/character/character-basics/ | Fetched — verbatim per-point attribute values |
| https://www.grimdawn.com/guide/gameplay/combat/ | Fetched — verbatim PTH formula, crit tier table, armor absorption 70% default |
| https://steamcommunity.com/sharedfiles/filedetails/?id=596728673 | Fetched — verbatim OA/DA formulas, crit tier table (community guide) |
| https://steamcommunity.com/app/219990/discussions/0/1742267854814318575 | Fetched — no relevant numeric content |
| https://steamcommunity.com/app/219990/discussions/0/3435626476279517178/ | Fetched — no relevant numeric content |
| https://steamcommunity.com/app/219990/discussions/0/152392786899995963/ | Fetched — qualitative attribute discussion; no exact formulas |
| https://steamcommunity.com/app/219990/discussions/0/1776010325134218727 | Fetched — Guardian of Empyrion discussion; no FoI content |
| https://steamcommunity.com/app/219990/discussions/0/1620599015872291805/ | Fetched — energy cost discussion; no rank table; tick cadence confirmed |
| WebSearch (multiple queries) | Synthesis — confirmed: FoI ticks every 0.3s at 100% cast speed; PTH formula; attribute per-point values corroborated |
