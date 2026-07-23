# KF-2/3 Harvest — Path of Exile 2 (poe2-bonestorm)
**Legolas Mode B** | 2026-07-23 | Kit: `poe2-bonestorm` (Bonestorm Witch Hunter/Blood Mage, 0.3 era)
**Charter ref:** KFL-3 — starter set = early-accessible, well-documented PoE2 mobs.

---

## KIT SIDE (KF-2 input)

### Bonestorm Skill Gem — Level Progression Table (VERBATIM)

**Source 1:** poe2db.tw/us/Bonestorm (accessed 2026-07-23) — labeled as "dataset" class in corpus
**Source 2 (corroborating):** pathofexile2.wiki.fextralife.com/Bonestorm (accessed 2026-07-23)

Verbatim from poe2db.tw:
- "Deals (4—116) to (7—175) Physical Damage" [projectile, gem levels 1–20]
- "Deals (3—89) to (5—134) Physical Damage" [explosion, gem levels 1–20]
- "Cost: (5.92—60.57) Mana per second" [scales with gem level and charge consumption rate]
- "Cast Time: 0.12 sec"
- "Critical Hit Chance: 15.00%"
- "Projectile Speed: 27 metres per Second"
- "Explosion radius is 0.5 metres"
- "+0.7 metres to explosion radius if a Power Charge was Consumed"
- "40% more Area of Effect per Power Charge Consumed"
- "Fires +1 Projectiles" / "Can fire up to 20 Projectiles"
- "200% more Impale Magnitude" (both projectile and explosion)
- Quality: "(0—10)% more Cast Speed" / "(0—20)% chance to not remove Charges on use"

**poe2db.tw Level Progression Table (verbatim):**

| Gem Lvl | Req Level | Int | Mana/sec | Projectile Dmg | Explosion Dmg |
|---------|-----------|-----|----------|----------------|---------------|
| 1 | 0 | 4 | 6 | 4–7 | 3–5 |
| 2 | 3 | 9 | 7 | 6–9 | 5–7 |
| 3 | 6 | 14 | 8 | 8–12 | 6–9 |
| 4 | 10 | 21 | 10 | 10–16 | 8–12 |
| 5 | 14 | 28 | 11 | 13–20 | 10–15 |
| 6 | 18 | 35 | 13 | 16–24 | 12–18 |
| 7 | 22 | 41 | 14 | 19–29 | 15–22 |
| 8 | 26 | 48 | 16 | 23–34 | 18–26 |
| 9 | 31 | 57 | 18 | 27–40 | 21–31 |
| 10 | 36 | 65 | 21 | 31–47 | 24–36 |
| 11 | 41 | 74 | 23 | 36–55 | 28–42 |
| 12 | 46 | 82 | 26 | 42–63 | 32–48 |
| 13 | 52 | 92 | 29 | 48–72 | 37–56 |
| 14 | 58 | 103 | 33 | 55–83 | 42–63 |
| 15 | 64 | 113 | 36 | 63–94 | 48–72 |
| 16 | 66 | 116 | 40 | 71–107 | 55–82 |
| 17 | 72 | 126 | 45 | 81–121 | 62–93 |
| 18 | 78 | 137 | 50 | 91–137 | 70–105 |
| 19 | 84 | 147 | 55 | 103–155 | 79–119 |
| 20 | 90 | 157 | 61 | 116–175 | 89–134 |

Note: Mana cost column above is "Mana per second" (channel skill). This is NOT a per-cast cost.

### Bonestorm — Mechanic notes for KF-2 join-key

Bonestorm is a CHANNEL skill that consumes Power Charges during the channel. Per the kit_mapping: "wind-up (channel accumulates shard count) — longer hold = more shards released." Key mechanics:

1. **Physical spell damage** — not weapon damage. Source_value is the skill's own damage range (not weapon-dependent). This makes it simpler than poe1-cyclone for join-key derivation.
2. **Power Charge consumption** is the channel mechanic. Each consumed Power Charge adds +0.7m explosion radius and 40% more AoE. Max 20 projectiles.
3. **Crit chance 15%** — base crit is high (15% vs typical 5%). Crit multiplier from gear/passives is critical for expected damage. The corpus probe fact for poe2-bonestorm (control family): ailment = "bleed" with centrality="rider" — Impale (Sunder) is the primary mark, "200% more Impale Magnitude" is verbatim anchored.
4. **Two-component damage:** projectile hit + explosion on impact. Both deal physical. The join-key should capture BOTH components' source_values.
5. **Build context:** the forum thread [PoE2 0.3] 2in1 Witch Hunter build notes: "Bonestorm increases the effect of Impale by 3x! So instead of 30%, we're storing 90% of the damage." Verbatim quote: "Impale stores 30% of the Hit damage you deal" → Bonestorm increases to "90%."
6. **Deadeye variant:** "Unlimited Boneworks — Turning Bonestorm into a Non-Channeling skill with the Deadeye ascendancy" — corpus kit is the channeling version (Witch Hunter/Blood Mage).

**JOIN-KEY NOTE FOR GAMORA:** poe2-bonestorm has two source_value entries per gem level: (a) projectile physical damage and (b) explosion physical damage. The kit's expected damage per full release = (projectiles_fired × projectile_hit) + (projectiles_fired × explosion). Max shard count = 20. The normalization rule must express this as: total = N_shards × (proj_damage + explosion_damage) where N_shards is 1–20 depending on channel duration. Recommend pinning N_shards to 10 (midpoint) for the documented build point unless a specific shard count is documented.

**Mana cost at build point:** "619 per second" quoted by a commenter for a level-25 gem setup (game8.co build page, accessed 2026-07-23). Verbatim: "619 per second." Note: this is level 25 (beyond the gem level 20 table above); level 20 mana cost = 61/sec per table.

### Character Attributes / Defense — Bonestorm Build Point

**Source:** game8.co, mmomax.com, pathofexile.com/forum builds (all accessed 2026-07-23)

What IS anchored verbatim:
- "Bonestorm [at gem level 25] costs 619 per second" — game8.co commenter (verbatim)
- "200% more Impale Magnitude" — poe2db.tw (verbatim)
- "15.00% Critical Hit Chance" (base) — poe2db.tw (verbatim)
- "about 100% increased Cast Speed on your gear" — PoE2 forum build thread (verbatim)
- "about 60-70 Spirit" requirement — forum thread (verbatim)
- Wand: "+5 and 80+ crit" — forum thread (verbatim; gear requirement not stat sheet)
- Energy Shield is primary defense layer (qualitative from all guides)
- Intelligence is primary attribute (qualitative; Int requirement scales from 4 to 157 per gem level table)
- Crit multiplier: builds target high values (not verbatim-anchored in any reachable guide)
- "Decimating Strike: instantly removes 5–30% of their Max Life" — forum thread (verbatim; a Witch Hunter ascendancy mechanic, not the skill itself)
- "Culling Strike: Instantly kills enemies below 30% for white mobs" — forum thread (verbatim)

**GAPS — Character stat sheet (all):**

| Field | Status |
|---|---|
| Energy Shield pool at documented build point | GAP |
| Life pool at build point | GAP |
| Armor/Evasion | GAP |
| Block | GAP |
| Fire/Cold/Lightning/Chaos resist exact values | GAP |
| Attack speed / cast speed exact | PARTIAL — "100% increased Cast Speed" target from forum (verbatim) |
| Crit chance at build point | GAP — base 15% from gem; total with gear/passives not anchored |
| Crit multiplier | GAP |
| Strength/Dexterity/Intelligence exact values | GAP — Int scales with gem (4-157 per table); total character stat not anchored |
| Power Charge count at build point | GAP — relevant for AoE and shard count |

---

## KF-3 MONSTER SIDE — PoE2 Early Access, Act 1 / Early Maps

**Context:** PoE2 is in Early Access (0.3 era as of charter date). The monster database at poe2db.tw is an SPA that returns 404 for most named monster paths attempted. The /us/Monster page yielded a baseline level scaling table. No specific named Act 1 mob stats were fetchable with verbatim anchors from individual monster pages.

**What IS anchored:**

### Monster Level Scaling Table (PoE2 baseline)
Source: poe2db.tw/us/Monster (accessed 2026-07-23)
Verbatim: Per-level baseline stats for PoE2 monsters.

| Monster Level | Damage | Life | Armour | Evasion | Accuracy |
|---|---|---|---|---|---|
| 1 | 9.16 | 15 | 5 | 24 | 32 |
| 2 | 10.26 | 20 | 8 | 30 | 35 |
| 3 | 11.39 | 24 | 11 | 36 | 39 |
| 4 | 12.57 | 28 | 15 | 43 | 43 |
| 5 | 13.78 | 33 | 19 | 49 | 48 |

Verbatim: "maximum physical damage reduction +% [75]" and "base maximum all resistances +% [75]" as standard monster properties.
Verbatim: Early-stage creature modifiers cited include "Flathead Younglings (70% damage/life)" and "Feral Primates (65% damage/life)."

### Monster resistances note (PoE2 Act 1)
Source: poe2db.tw/us/ (monster section, accessed 2026-07-23) + PoE2 mechanics
PoE2 act 1 monsters: majority of early undead/humanoid mobs have 0% elemental resists at Normal difficulty. Physical damage cap = 75%.

### GAP VERDICT — PoE2 Monster Side
Named Act 1 PoE2 mobs (Zombie, Skeleton, Goatman, etc.) cannot be fetched with verbatim per-mob stat anchors from poe2db.tw — the SPA renders monster pages as dynamic content not accessible to WebFetch. The level scaling table is anchored but is a formula-level anchor, not a per-mob anchor. This is a **partial gap**: for elrond, the formula-based approach (level scaling table × monster-specific multiplier) is the available data; per-mob verbatim stats require alternative sourcing (datamining community, game files, or a rendering-capable fetch tool).

Recommendation: Elrond should use the level-scaling table + the corpus probe_facts qualitative context for the Bonestorm build encounter tier to estimate PoE2 monster expected-received values. Per-mob verbatim fetches are a next-lap admission per §5 of the charter.

---

## Sources consulted (all read-only, 2026-07-23)

| URL | Result |
|---|---|
| https://poe2db.tw/us/Bonestorm | Fetched — complete level table, skill stats verbatim |
| https://pathofexile2.wiki.fextralife.com/Bonestorm | Fetched — corroborating skill stats verbatim |
| https://www.pathofexile.com/forum/view-thread/3852711 | Fetched — Impale/Sunder mechanic verbatim (30% → 90%) |
| https://www.pathofexile.com/forum/view-thread/3706145 | Fetched — cast speed target, Spirit requirement, gear requirements verbatim |
| https://game8.co/games/Path-of-Exile-2/archives/490217 | Fetched — "619 mana/sec" verbatim (gem level 25); no stat sheet |
| https://www.mmomax.com/news/path-of-exile-2-bonestorm-build-guide... | Fetched — qualitative only; no stat values |
| https://poe2db.tw/us/Monster | Fetched — baseline level scaling table verbatim |
| poe2db.tw/us/Skeleton, /Zombie, /Cannibal, /Goatman, /SkeletonMelee, /ZombieRibbedSlowVersion, /SkeletonWalker, /BoneDeacon | All 404 — SPA monster name paths not resolving via WebFetch |
| https://pathofexile2.wiki.fextralife.com/Enemies | Fetched — descriptive only, no numeric stats |
