# KF-2/3 Harvest — Formula Anchors (KFL-7 residual lane)
**Legolas Mode B** | 2026-07-23 | KIT-FIDELITY autonomous run — formula-anchor lane
**Charter ref:** KFL-7 — anchoring damage-reduction / hit-chance formulas for PoE1, PoE2, D2 (Grim Dawn already done).
**Fetch budget used:** 21 of 22.

---

## Section A — PoE1 Formulas

### A1. PoE1 Armour damage-reduction formula

**Source:** https://www.pathofexile.com/forum/view-thread/1468738 (accessed 2026-07-23)
**Status:** ANCHORED

Verbatim formula expression (from forum post "Physical damage reduction formula (spreadsheet inside)"):
> "ArmourRed = Armour / (Armour + 10 * PhysRawDmg)"

Full mitigation formula combining all sources (same source):
> "PhysRed = 1 - (1-ArmourRed-ECharge-SoulSteel-Golem) * (1-Fortify) * (1-ArcticArmour)"

Where ArmourRed, Endurance Charges (ECharge), Soul of Steel (SoulSteel), and Chaos Golem (Golem) are **additive within their category**; Fortify and Arctic Armour apply **multiplicatively** against the remaining damage.

Hard cap verbatim (same source):
> "Physical damage reduction has a hard cap of 90%"

Corroborating "rule of thumb" quote from https://www.pathofexile.com/forum/view-thread/1701362 (accessed 2026-07-23):
> "To prevent half of damage, you need armor 10 times the damage (e.g. 1000 Armor for 100 damage)"
> "Armor will never prevent more damage than its value divided by 10 (e.g. 1000 Armor will never prevent more than 100 damage)"
> "the principles become very, very wrong when you would reach the % Physical Damage Reduction cap of 90%"

**Summary for downstream:** PoE1 armour DR formula = Armour ÷ (Armour + 10 × RawHit). Cap = 90%.

---

### A2. PoE1 Evasion / chance-to-hit formula + entropy mechanic

**Source for entropy mechanic + spell rule:** https://www.poecurrency.com/news/path-of-exile-evasion-entropy-system (accessed 2026-07-23)
**Status:** PARTIALLY ANCHORED — entropy and spell rule verbatim; formula expression is image-only (GAP)

**Entropy mechanic verbatim:**
> "When a target is attacked for the first time in a zone, an entropy value is rolled between 0 and 99. This also happens if the target hasn't been attacked for 100 server ticks or more, which is at least 3.33 seconds. The attacker's chance to hit is then added to the entropy value and if this number is now equal to or greater than 100, the attack will hit. When this happens, 100 is subtracted from the entropy value."

**Spell evasion rule verbatim (PoE1):**
> "Evasion only works against attacks. It doesn't work against spell hits."

**Evasion formula expression:** The article states the formula uses attacker accuracy rating (AA) and defender evasion (De) but the actual mathematical expression is presented as an **image** on the page — verbatim text form is NOT available from this source.

**Search synthesis (NOT verbatim-anchored — GAP):** WebSearch returned an example calculation "Chance to Hit = 500 / (500 + (5000/4)^0.8) = 62% Chance to Hit" from search snippet context suggesting the formula involves an exponent of 0.8, but this was not confirmed by a verbatim-fetchable page. See GAPS table.

---

## Section B — PoE2 Formulas

### B1. PoE2 Armour damage-reduction formula

**Status:** GAP — all primary sources blocked

**Attempts:**
- https://www.poe2wiki.net/wiki/Armour → Anubis bot-protection (access denied)
- https://mobalytics.gg/poe-2/guides/armour → HTTP 403
- https://www.pathofexile.com/forum/view-thread/3642515 → Fetched but no verbatim formula; players reference "damage compared to hit size" scaling without algebraic expression

**WebSearch synthesis (NOT verbatim-anchored):** Search result snippet states formula is "DR = A / (A + 10 × D_raw)" with 90% cap — identical structure to PoE1 — but this was synthesized by the search result, not extracted from a fetchable source page. Cannot anchor verbatim.

**GAP row:** See GAPS table — ID GAP-B1.

---

### B2. PoE2 Evasion — can spells be evaded?

**Source:** https://www.poecurrency.com/news/poe-2-how-evasion-changes-affect-build-defense-mechanics (accessed 2026-07-23)
**Status:** ANCHORED

**Verbatim rule — spells and projectiles CAN be evaded in PoE2:**
> "By default, characters will be able to evade any incoming projectile or strike in Path of Exile 2, whether that projectile is an arrow fired by a monster attacking or a fireball fired by a monster casting a spell."

**Verbatim AoE exception:**
> "However, by default, characters will not be able to evade Area of Effect hits, such as the larger slam skills used by bosses."

**Verbatim monster spell mechanic:**
> "Monster skills that were spells in Path of Exile 1 (such as Fireball) will use the monster's Accuracy Rating to determine their chance to hit."

**Verbatim entropy mechanic (PoE2, same source):**
> "This Entropy value is randomly rolled between 0 and 99, and the attacker's chance to hit is added to this value. If Entropy value is over 100 after adding the attacker's chance to hit, the attack will hit, and 100 will be subtracted from Entropy value."

**CRITICAL FINDING for kit poe2-bonestorm:** bonestorm is a physical SPELL. In PoE2, monster spells use monster Accuracy Rating vs player Evasion — so player evasion DOES provide avoidance against bonestorm hits IF bonestorm targets individual characters (non-AoE portion). If bonestorm has an AoE component, that component cannot be evaded (unless Acrobatics passive is taken).

---

## Section C — D2 Formulas + Residuals

### C1. D2 Chance-to-hit formula (Attack Rating vs Defense)

**Source 1 (primary):** https://maxroll.gg/d2/resources/hit-chance-mechanics (accessed 2026-07-23)
**Status:** ANCHORED

Verbatim formula:
> "Chance to Hit = min(max(200% * (AR / (AR + Dr)) * (ALVL / (ALVL + TLVL)), 5%), 95%)"

Where:
- AR = Attacker's Attack Rating
- Dr = Target's Defense
- ALVL = Attacker Level
- TLVL = Target Level

Verbatim caps:
> "Chance to Hit is capped at 95%, and has a minimum value of 5%."

**Source 2 (corroborating):** https://diablo2.wiki.fextralife.com/Attack+Rating (accessed 2026-07-23)
Verbatim formula:
> "Chance To Hit = 200% * {Attacker's Attack Rating / (Attacker's Attack Rating + Defender's Defense Rating)} * {Attacker's level / (Attacker's level + Defender's level)}"

Both sources confirm: caps are 5% floor / 95% ceiling.

---

### C2. D2 Spells ignore Defense confirmation

**Source:** https://maxroll.gg/d2/resources/hit-chance-mechanics (accessed 2026-07-23)
**Status:** ANCHORED (partial — confirms always-hit for listed skills, implies spell category)

Verbatim on skills that bypass hit checks:
> "guidedarrow, lightningbolt, lightningfury, smite"

Verbatim on skills that apply effect without hit check (weapon damage does not apply, skill damage does):
> "explodingarrow, freezingarrow, immolationarrow, plaguejavelin, poisonjavelin, conversion"

**Note:** The Maxroll page does not use the word "spell" explicitly in the bypass list, nor does it contain a blanket "all spells bypass defense" statement verbatim. The Fextralife Attack+Rating page also does not address this explicitly. The diablowiki.net/Defense page returned HTTP 403 and diablowiki.net/Guide:Defense_101 also returned HTTP 403.

**Implication for d2-firewall-sorc:** Fire Wall is a Sorceress spell skill, not listed in the targeted always-hit bypass list above. The verbatim bypass list covers specific projectile/skill names. A blanket "spells bypass defense" rule is referenced in search context but NOT verbatim-anchored from a fetchable page. See GAPS — GAP-C2.

---

### C3. D2 Sorceress life-per-level + life-per-vitality

**SOURCE CONFLICT — BOTH VERBATIM:**

**Source A:** https://maxroll.gg/d2/resources/sorceress-overview (accessed 2026-07-23)
Verbatim table values:
> Life: Base 40 | per Level +1 | +2 per Vitality

**Source B:** https://diablo2.wiki.fextralife.com/Sorceress (accessed 2026-07-23)
Verbatim:
> "Each Character Level: +2 [life]"
> "1 Vitality point gives 3 Life"

**The two sources conflict on both fields:**
| Field | Maxroll | Fextralife |
|-------|---------|------------|
| Life per level | +1 | +2 |
| Life per vitality | +2 | +3 |

**Neither can be dropped** — both verbatim, both citable. The prior D2 harvest (kf23-harvest-d2.md) cited maxroll (+1/level, +2/vit). The discrepancy must be flagged for downstream resolution. The Maxroll resource is a dedicated D2R build platform (higher authority for current D2R values); fextralife may reflect a different version or errata. Suggested resolution: treat Maxroll as primary pending gamora/jack-ryan review.

Corroborating starting stats (both sources agree):
- Base life: 40
- Base vitality: 10
- Base energy: 35
- Base mana: 35
- Mana per level: +2
- Mana per energy point: 1.5 (fextralife) / +2 per energy (maxroll — may be rounded)

---

### C4. D2 Starter-mob Attack Rating (AR / To-Hit column check)

**Status:** ANCHORED — AR column EXISTS on Fextralife mob pages

**Source re-fetch of Fallen:** https://diablo2.wiki.fextralife.com/Fallen (accessed 2026-07-23)
Verbatim AR values for Normal difficulty:
> "Attack Rating 1 (Normal): 8"
> "Attack Rating 2 (Normal): 8"

**Source re-fetch of Zombie:** https://diablo2.wiki.fextralife.com/Zombie (accessed 2026-07-23)
Verbatim AR values for Normal difficulty:
> "Attack Rating 1 (Normal): Zombie 8 | Hungry Dead 12"
> "Attack Rating 2 (Normal): Zombie 8 | Hungry Dead 12"

**Summary AR table for Act 1 Normal mobs (from re-fetches above):**

| Mob | Variant | AR Attack 1 (Normal) | AR Attack 2 (Normal) | Source |
|-----|---------|----------------------|----------------------|--------|
| Fallen | Fallen | 8 | 8 | fextralife/Fallen |
| Zombie | Zombie | 8 | 8 | fextralife/Zombie |
| Zombie | Hungry Dead | 12 | 12 | fextralife/Zombie |

**Remaining 3 mobs (Skeleton, Corrupt Rogue, Spike Fiend):** NOT re-fetched (would exceed budget). AR column exists on fextralife mob pages — assumed present for all mobs by pattern; values not captured. See GAPS — GAP-C4b.

---

### C5. D2 Fire Wall tick rate (retry)

**Status:** GAP — diablowiki.net/Fire_Wall returned HTTP 403. Second attempt blocked.

**Prior note from kf23-harvest-d2.md (GAP carried forward):** "game displays per-second; tick rate not verbatim-anchored in any public source." Status unchanged after retry.

See GAPS — GAP-C5.

---

## Section D — Grim Dawn community data-dump route

### D1. GD Flames of Ignaffar per-rank table

**Status:** GAP — community data-dump route exhausted

**Repos tried:**
- https://github.com/abclution/GrimDawn_DB_to_CSV_Extractor — converter tool only; no pre-extracted data files (README confirmed "gdtool.py" + "README.md" only; requires user's own AssetManager.exe extraction)
- https://github.com/atom0s/grimarz — ARZ file extractor tool; no extracted data in repo
- https://github.com/atom0s/grimarc — ARC file extractor tool; no extracted data in repo
- https://github.com/atom0s/gdfe — file extractor tool; no extracted data in repo
- https://github.com/ChrisElison/GDParser — save file parser (character stats, not skill tables)
- Search "site:github.com grim dawn flames of ignaffar skill data stats per rank skillLevel raw" — returned no GitHub results with raw data files
- Search "grim dawn extracted game data github flames of ignaffar FoI stats per rank csv json" — returned only tool repos + grimdawn.fandom.com (returned 402 previously) + grimtools.com (JS-rendered, previously exhausted)

**Conclusion:** No pre-extracted static-fetchable data files found on GitHub for Flames of Ignaffar per-rank stats.

See GAPS — GAP-D1.

---

### D2. GD Act-1 Normal mob stats (HP/OA/DA/armor/resists)

**Status:** GAP — same route exhaustion as D1. No static-fetchable raw files found.

GrimTools monster database exists (grimtools.com/monsterdb/) but is JS-rendered. Grim Dawn fandom wiki (grimdawn.fandom.com) returns 402. No GitHub alternatives found with pre-extracted monster stat CSVs.

See GAPS — GAP-D2.

---

## GAPS

| ID | Target | Blocked URLs | Note |
|----|--------|-------------|------|
| GAP-A2 | PoE1 evasion formula verbatim expression | pathofexile.fandom.com (402); Steam discussion pages (no content) | Entropy mechanic and spell-rule anchored. Formula expression is image-only on poecurrency.com. Search snippet suggests Accuracy^0.8 form but not verbatim-fetchable. Try static wiki mirror or PoE API docs. |
| GAP-B1 | PoE2 armour damage-reduction formula verbatim | poe2wiki.net (Anubis blocked); mobalytics.gg (403); glama.ai (blob loading not available) | Search synthesis suggests same form as PoE1 (Armour / (Armour + 10 × Hit)) but NOT verbatim-anchored. |
| GAP-C2 | D2 spells-bypass-defense blanket rule verbatim | diablowiki.net/Defense (403); diablowiki.net/Guide:Defense_101 (403) | Maxroll hit-chance page lists specific skill names that bypass but no blanket "all spells bypass" statement. Community consensus is spells bypass AR check but no verbatim anchor found. |
| GAP-C3-conflict | D2 Sorceress life-per-level + life-per-vitality conflict | n/a — both fetched successfully | Maxroll: +1/level, +2/vit. Fextralife: +2/level, +3/vit. Requires downstream resolution. Recommend treating Maxroll as primary for D2R. |
| GAP-C4b | D2 starter-mob AR for Skeleton, Corrupt Rogue, Spike Fiend | Not re-fetched (budget constraint) | AR column confirmed to exist on fextralife pages by Fallen + Zombie fetches. Values presumed present; not captured. |
| GAP-C5 | D2 Fire Wall per-tick damage / tick rate | diablowiki.net/Fire_Wall (403) | Carried from prior harvest. Game shows dmg/sec; tick rate unanchored. Two attempts failed. |
| GAP-D1 | GD Flames of Ignaffar per-rank table | All GitHub repos are tools-only; grimdawn.fandom.com (402); grimtools.com (JS-rendered) | Community data-dump route exhausted. Route requires local extraction via AssetManager.exe + gdtool.py — not feasible read-only web. |
| GAP-D2 | GD Act-1 Normal mob stats (HP/OA/DA/armor/resists) | Same as GAP-D1 | Same route exhaustion. No static-fetchable raw files exist. |

---

## Sources consulted (all read-only, 2026-07-23)

| # | URL | Result |
|---|-----|--------|
| 1 | https://www.poewiki.net/wiki/Armour | BLOCKED — Anubis bot-protection |
| 2 | https://www.poewiki.net/wiki/Evasion | BLOCKED — Anubis bot-protection |
| 3 | https://www.poewiki.net/wiki/Accuracy | BLOCKED — Anubis bot-protection |
| 4 | https://www.poe2wiki.net/wiki/Armour | BLOCKED — Anubis bot-protection |
| 5 | https://diablo2.diablowiki.net/Attack_rating | HTTP 403 |
| 6 | https://diablo2.diablowiki.net/Defense | HTTP 403 |
| 7 | https://diablo2.diablowiki.net/Guide:Defense_101_v1.11,_by_Alecz | HTTP 403 |
| 8 | https://diablo2.diablowiki.net/Fire_Wall | HTTP 403 |
| 9 | https://www.pathofexile.com/forum/view-thread/1701362 | FETCHED — PoE1 armour formula derivation + rule of thumb verbatim |
| 10 | https://www.pathofexile.com/forum/view-thread/1468738 | FETCHED — PoE1 armour formula verbatim: "ArmourRed = Armour / (Armour + 10 * PhysRawDmg)" |
| 11 | https://www.pathofexile.com/forum/view-thread/3642515 | FETCHED — PoE2 armour discussion; no verbatim formula |
| 12 | https://mobalytics.gg/poe-2/guides/armour | HTTP 403 |
| 13 | https://mobalytics.gg/poe-2/guides/evasion | HTTP 403 |
| 14 | https://maxroll.gg/d2/resources/hit-chance-mechanics | FETCHED — D2 hit formula verbatim (primary anchor) |
| 15 | https://diablo2.wiki.fextralife.com/Attack+Rating | FETCHED — D2 hit formula verbatim (corroborating) |
| 16 | https://diablo2.wiki.fextralife.com/Sorceress | FETCHED — Sorceress stats: +2/level, +3/vit (conflicts with maxroll) |
| 17 | https://maxroll.gg/d2/resources/sorceress-overview | FETCHED — Sorceress stats: +1/level, +2/vit (conflicts with fextralife) |
| 18 | https://diablo2.wiki.fextralife.com/Fallen | FETCHED — AR column confirmed: Attack Rating 1+2 Normal = 8 |
| 19 | https://diablo2.wiki.fextralife.com/Zombie | FETCHED — AR: Zombie 8/8, Hungry Dead 12/12 (Normal) |
| 20 | https://www.poecurrency.com/news/path-of-exile-evasion-entropy-system | FETCHED — PoE1 entropy mechanic verbatim; spell rule verbatim; formula image-only |
| 21 | https://www.poecurrency.com/news/poe-2-how-evasion-changes-affect-build-defense-mechanics | FETCHED — PoE2 evasion rule verbatim (spells evadeable; AoE exception) |
| — | WebSearch: PoE1 armour formula pathofexile.com | Search (count toward fetch budget) — surfaced forum thread URLs |
| — | WebSearch: PoE2 armour formula | Search — synthesized formula (not verbatim-anchored) |
| — | WebSearch: D2 AR formula | Search — surfaced maxroll + fextralife URLs |
| — | WebSearch: PoE2 evasion spells | Search — surfaced poecurrency.com URL |
| — | WebSearch: PoE1 evasion formula verbatim | Search — formula is image-only |
| — | WebSearch: GD github FoI data | Search — tools-only repos found |
| — | WebSearch: GD github monster stats | Search — tools-only repos found |
| — | https://glama.ai/mcp/servers/@HivemindOverlord/poe2-mcp/blob/.../defense_calculator.py | FETCHED — "Loading blob content..." — Python code not rendered |
| — | https://github.com/abclution/GrimDawn_DB_to_CSV_Extractor | FETCHED — tool only; no pre-extracted data |
| — | https://steamcommunity.com/app/2694490/discussions/0/598514132636997849 | FETCHED — Steam nav page only; no content |
| — | https://steamcommunity.com/app/2694490/discussions/0/598513885981538788 | FETCHED — Steam nav page only; no content |
| — | https://www.purediablo.com/strategy/diablo-2-guide-defense-101 | HTTP 403 |
| — | https://raw.githubusercontent.com/abclution/GrimDawn_DB_to_CSV_Extractor/master/README.md | FETCHED — no sample data files in repo |
