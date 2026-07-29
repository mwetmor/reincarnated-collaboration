# G-4 v2 — KIT SPEC — `gd-werewolf-kitcal-1` on MEASURED identity + H-2 band redraft

**▶ ROLE: SPEC-AUTHOR — G-4 redraft, phase P-2 of run `KC1-2026-07-27` (KIT-CAL-1).**
**Author:** named `gandalf` sub-agent · **Conductor:** gandalf (`RUN-CONDUCTOR`)
**Authority:** charter `gandalf/notes/2026-07-27-kit-cal-1-run-charter.md` §12–§14; §14.5 (*"Kit-spec + H-2
bands now redraft on measured identity"*); G-4 v1 §6.5 (the pre-registered redraft trigger, fired).
**Supersedes:** `gandalf/notes/2026-07-28-kitcal1-g4-kit-spec.md` (v1) **in total.** v1 is retained in
git as the ATTESTED-era draft; where v1 and v2 disagree, **v2 governs** and §7 says which instrument
forced each change.

**Fixture:** `GD-R2-werewolf` (session `GP-gd-2026-07-26-s1`) · **Kit id:** `gd-werewolf-kitcal-1`
**Instruments that landed between v1 and v2:** T11/**G-7** (`.gdc` save parse, legolas) · **G-6**
(313-still screenshot read, galadriel) · **G-5a** (GD level-12 opposition ledger, legolas) · **G-5b**
(sim opposition census, gamora) · Matt's testimony reconciliation (charter §14.5).

**Status:** **DRAFT for HALT H-2.** §6 bands do not bind until Matt pins them (§8 pin-sheet).

> **⚠ AMENDED 2026-07-28 (run `WR1-2026-07-28`, cell WR1-SPEC-AMEND).** Three spec amendments are
> appended at **§10** per the KC1 terminal verdict §A-8.3 (*"Kit spec v2 cannot be quoted again until
> three amendments land"*). They touch **§6.3** (tier-weighting + boss-tier window membership),
> **§6.2 S-1** (coincidence-floor clause) and **§6.2 S-2** (re-registration off the pinned residual).
> **No band, predicate or ruled sentence below is rewritten** — §10 corrects by appendix, and where
> §10 and the original text conflict, **§10 governs for all FUTURE batteries only.** Every KC1 grade
> stands exactly as pre-registered.

---

## §0 — What changed, in one paragraph, and the sentence that governs reading this

v1 was written when the kit's identity was **inferred**: no ranks, no gear, no attributes, a
level guessed at 12, and a standing assumption that the werewolf line was unallocated. Every one of
those is now **MEASURED**, by two or three independent instruments that agree. The kit is bigger than
v1 thought — **five allocated nodes, not three; six damage channels, not two; two static conversions;
an unmodelled crit-gated sustain proc; an unmodelled reserved aura** — and, decisively, **it was not
constant across R2.** v1's central simplification (R2 = "the fixture", a single stationary
build) is falsified by G-6's dated rank series. §6 therefore re-cuts the band window.

> **The governing sentence is unchanged from v1, and the new evidence strengthens it.** Per
> **R-KC1-9** the primary claim is **structural**, not numeric. §4's mechanism manifest is the
> centerpiece; §6's numbers are corroboration and must never be read as the verdict. Per **R-KC1-12**,
> when a signature does not reproduce and instrument error is excluded, **the default attribution is
> that the sim is wrong**, and the deliverable is a **genre-gap map first, tuning target second**.

**Grade vocabulary (R-KC1-1).**

| Grade | Meaning |
|---|---|
| **MEASURED** | read byte-exact from a named source by an instrument on this run (`.arz` record path · `.gdc` block · screenshot at ≥1× native · `fixtures.db` row) |
| **DERIVED** | arithmetic over MEASURED values; the derivation is shown inline |
| **ATTESTED-retired** | was a v1 testimony/inference grade; **superseded by measurement.** Kept only where the retirement is itself informative |
| **UNCERTAIN** | two instruments disagree, or one instrument's semantics are unresolved; named, never smoothed |
| **UNKNOWN** | named gap; nothing is inferred into it |

---

## §1 — MEASURED IDENTITY

### 1.1 Character

| # | Field | Value | Grade | Source |
|---|---|---|---|---|
| 1.1a | Character | `Fresh Character 01`, male, non-hardcore | MEASURED | G-7 §1 (`.gdc` header) |
| 1.1b | Mastery | `playerclass10` = **Berserker** (GDX3, *Fangs of Asterkarn*); **single mastery** (`masteriesAllowed=2`, one used) | MEASURED | G-7 §8 |
| 1.1c | **Level** | **13** — *not 12* | MEASURED | G-7 §6; proven twice from `.arz` arithmetic (XP threshold; attribute bytes). `play_stats.maxLevel` **lags at 12**, which is what the HUD and every G-6 still showed |
| 1.1d | **Attributes** | physique **122** · cunning **74** · spirit **50** | MEASURED | G-7 §7 |
| 1.1e | Attribute allocation | **12 points: 9 physique / 3 cunning / 0 spirit** (base 50/50/50, +8 per point) | DERIVED from 1.1d | G-7 §6 check 2; `attributePointsUnspent = 0` |
| 1.1f | Base pools | health **454.0** · energy **250.0** — the **pre-modifier attribute layer**, NOT in-game max HP | MEASURED | G-7 §7. Closes to the byte from `playerlevels.dbr`: `250 + 9×20 + 3×8 = 454` |
| 1.1g | Difficulty | **Normal**, 1 player (`difficulty=128`, `greatestDifficulty=0`) | MEASURED | G-7 §1.12 — **v1 carried this UNKNOWN**; it fixes the G-5a opposition pak index to 0 |
| 1.1h | Campaign | **shipping Act-1 production tuning**, console-enabled `save\user\` slot — *not* a custom campaign | MEASURED / ATTESTED | charter §14.4 C-5 (Matt) |
| 1.1i | Devotion | **zero assigned** — 3 earned, 3 unspent, 0 reclaimed, all 62 `devotionLevel = 0` | MEASURED | G-7 §2 A1 (conjunctive test **passes**; refund loophole closed). Corroborated: `shrinesRestored = 3` = points earned; G-6 §7.2 found the Devotion tab never opened in 313 stills |
| 1.1j | Potions | health 0 / mana 0 | MEASURED | G-7 §2 A5; G-6 (36 stills) |
| 1.1k | Components / augments | **none, on any slot** | MEASURED | G-7 §3.1 — the fixture is un-componented, which removes a whole class of hidden stat sources |
| 1.1l | `save_identity` | `uid` is **16 zero bytes** → falls back to `sha256:0be3a99f…d5ee91` | MEASURED | G-7 §9. Carries different semantics (byte-state, not character) — flagged for elrond |

**Player combat rates, MEASURED and directly pinnable (v1 had none of these):**

| # | Quantity | Value | Grade | Consequence |
|---|---|---|---|---|
| 1.1m | `hitsInflicted` / `hitsReceived` | **1606 / 500** | MEASURED (G-7 §1.9) | the intake-side denominator the sim must reproduce |
| 1.1n | `criticalHitsInflicted` / `…Received` | **66 / 0** | MEASURED (G-7 §1.10) | **player crit rate = 66/1606 = 4.11 %** — pins `crit_chance`, and **gates Battle Surge** (§1.4) |
| 1.1o | `greatestDamageInflicted` / `…Received` | 1093.807 / 260.498 | MEASURED (G-7 §1.11) | a one-sided existence check on both tails |
| 1.1p | hits per skill press | 1606 / 680 presses = **2.362** | DERIVED (**semantics UNCERTAIN** — whether `hitsInflicted` counts DoT ticks is unresolved) | a *second, independent* instrument on AoE breadth, orthogonal to A. See §6.2 note |

*(Presses: claws 358 + charge 175 + `defaultweaponattack` 74 + onslaught 54 + `defaultkickattack` 19 = 680. All MEASURED, T-A endpoints + G-6 F-G6-7.)*

### 1.2 The allocation ledger — **five point-consuming nodes, not three**

`character_skills` v8, 62 entries; 8 are the build, 54 are engine defaults + GDX3 potion stubs.

| Record path (**the R-KC1-7 identity join key**) | English | Rank | max | `Class` | Points | Grade |
|---|---|---|---|---|---|---|
| `records/skills/playerclass10/_classtraining_class10.dbr` | Berserker (mastery bar) | **5** | 50 | `Skill_Mastery` | 5 | MEASURED |
| `records/skills/playerclass10/werewolf1.dbr` | **Werewolf** | **16** *(hard max)* | 16 | `Skill_Shapeshift` | 16 | MEASURED ×2 (G-7, G-6) |
| `records/skills/playerclass10/onslaught1.dbr` | **Onslaught** | **13** | 16 | `Skill_WeaponPool_BasicAttack` | 13 | MEASURED ×2 |
| `records/skills/playerclass10/werewolf1b.dbr` | **Blight of Ch'thon** | **1** | 1 | `Skill_Transmuter` | 1 | MEASURED ×2 |
| `records/skills/playerclass10/passive02.dbr` | **Battle Surge** | **1** | 12 | `Skill_PassiveOnCritBuffSelf` | 1 | MEASURED (G-7 §4; source-confirmed §1.4 below) |
| `records/skills/playerclass10/amatokpact1.dbr` | **Amatok's Pact** | **1** | 12 | `Skill_BuffRadiusToggled` | 1 | MEASURED (G-7 §4; source-confirmed §1.4) |
| `records/skills/playerclass10/werewolf1_skill01_claws.dbr` | **Feral Claws** | **16** *(mirrors transform)* | 16 | `Skill_AttackWeapon` | **0 — granted** | MEASURED |
| `records/skills/playerclass10/werewolf1_skill02_charge.dbr` | **Rip and Tear** | **16** *(mirrors)* | 16 | `Skill_AttackPathCharge` | **0 — granted** | MEASURED |

**Budget closes (DERIVED, G-7 §4.1):** `5 + 16 + 13 + 1 + 1 + 1 = 37` hard points against
`12 level-ups × 3 = 36` + **1 quest reward**; `skillPointsUnspent = 0`.

**Ranks are BASE HARD POINTS — no `+skills` inflation** (G-7 §4.1, three independent lines: zero
`augmentAllLevel`/`augmentSkillLevel*` targeting `playerclass10` on any equipped item;
`itemSkills` list length 0; the budget arithmetic above). **This is what lets the sim pin to a single
compiled rank rather than a rank-plus-gear distribution.**

**Measured-absent** (G-7 §4; G-6 §5 by effect-absence in the transform tooltip): `werewolf2`
(bleed + life-leech + crit-damage on claws — **v1's single largest declared sensitivity, now closed
in the spec's favour**), `werewolf3` (charge cooldown-refresh), `onslaught1b/2/3`, `passive01/03/04`,
`rallyingcry*`, `wereraven*`, `leap*`, `bloodborne1`, `heartofastekarn1`, `windsofasterkarn*`,
`bonechillingcry1`, `amatokpact2/3`.

**G-6's UNCERTAIN row is CLOSED here** (its REQUEST #1 and #2, routed to me). The two 1/12 nodes are
**`passive02` = Battle Surge** (`Skill_PassiveOnCritBuffSelf`) and **`amatokpact1` = Amatok's Pact**
(`Skill_BuffRadiusToggled`). Both carry `skillMaxLevel = 12`, matching the observed `1 / 12` counters.
**Neither is a `Skill_Modifier`** — so the square-vs-circle node shape in GD's mastery UI does *not*
mark modifier-vs-standalone here; the square is most plausibly the toggled aura. Rank is unaffected
either way (both are 1), so the residual is cosmetic. Grade: node identity **MEASURED**; the
square↔which-node mapping **UNKNOWN and immaterial**.

### 1.3 The two actives, at their measured rank 16 (MEASURED, `.arz` re-read this pass)

`werewolf1.dbr` sets `activeSkillSet = 1`; claws and charge carry `skillSet = 1`; `onslaught1` carries
**no** `skillSet` → set 0 → **excluded while transformed**. v1 §2's ruling stands, now with a **fifth**
corroborating line: G-6 F-G6-4 read the transform's own tooltip — ***"…cannot trigger weapon pool
skills."*** The game told the player, in words, in the same window.

**Feral Claws @ rank 16** — `Skill_AttackWeapon`, `distanceProfile=Melee`, `ignoreDisruption=True`:

| Field | @1 | @12 | @13 | **@16** | Grade |
|---|---|---|---|---|---|
| `skillTargetNumber` | 2 | 4 | 5 | **5** | MEASURED (`.arz`) + tooltip-confirmed *"5 Target Maximum"* |
| `skillTargetAngle` | 90° | 130° | 150° | **150°** | MEASURED + tooltip *"150 Degree Attack Arc"* |
| `weaponDamagePct` | 70 | 130 | 135 | **150** | MEASURED + tooltip *"150% Main Hand Damage (69–85)"* |
| `offensivePierceMin` | 12 | 177 | 192 | **237** | MEASURED + tooltip *"237 Piercing Damage"* |
| `skillManaCost` | 2 | 4 | 5 | **5** | MEASURED |
| Radius / reach | — | — | — | **NOT IN THE RECORD** | **UNKNOWN, structurally** — `Skill_AttackWeapon` is a *basic-attack modifier*; reach is the weapon's, not the skill's |

**Rip and Tear (charge) @ rank 16** — `Skill_AttackPathCharge`, `distanceProfile=Long`,
`targetingMode=Point`:

| Field | Value @16 | Grade |
|---|---|---|
| `weaponDamagePct` | **295** | MEASURED + tooltip *"295% Main Hand … 295% Off-Hand"* |
| `offensivePierceMin` | **375** | MEASURED + tooltip |
| `offensiveSlowBleedingMin` / `…DurationMin` | **270 / s × 3.0 s = 810 total** | MEASURED (`.arz` array is **per second**; the tooltip's *"810 Bleeding Damage over 3 Seconds"* is the product — **the derivation is now proven, not assumed**) |
| `skillCooldownTime` | **4.0 s** | MEASURED + tooltip |
| `waveDistance` / `skillTargetRadius` / `endRadiusMultiplier` | **14.0 m / 2.5 m / ×1.5** | MEASURED + tooltip |
| `characterRunSpeedModifier` | **+200 %** | MEASURED + tooltip |
| `offensiveKnockdownMin` | 0.5 s | MEASURED + tooltip |
| `timeBetweenAttacks` / `maxMoveRatio` / `secondarySkillDistance` | 100 ms / 2.0 / 1.0 | MEASURED |
| `skillManaCost` | 42 | MEASURED + tooltip |

**Ten `.arz` fields were independently confirmed against the running game's own tooltips at rank 16,
and three more at rank 12** (G-6 §5.1). The extraction is verified against the shipping client, not
merely parsed.

> **The transform grants no stats.** Re-verified this pass: `werewolf1.dbr`'s non-zero field set
> contains **no `characterLife*`, no attribute, no resistance, no weapon-flag** — only
> `activeSkillSet`, `grantedSkills`, mana cost, `notDispelable`, and mesh/anim/sound replacement.
> **This falsifies G-7 §7's tentative reading that the 759→1600 step is "the shape a shapeshift
> transform produces."** It is not; it is gear (§1.7), and G-6 itemised 87.6 % of it.

**One UNCERTAIN, carried not smoothed:** G-6 read claws' displayed pierce at rank 12 as **103**
where the `.arz` array holds **177**. Rank 16 matches exactly (237/237). Consequence is confined to
the pre-2918 window, which §6 does not band. Crop preserved (G-6 §8 item b).

### 1.4 The two nodes v1 missed entirely — **both switch on mid-R2**

Both allocated in the same window, `play_time` ∈ **(2918, 3619]** (G-6 §3.1: locked at f170, live at
f209). Both source-read this pass from `GDX3.arz`.

**(a) Battle Surge — `records/skills/playerclass10/passive02.dbr` — the unmodelled SUSTAIN channel**

| Field | Value @ rank 1 | Grade |
|---|---|---|
| `Class` | **`Skill_PassiveOnCritBuffSelf`** | MEASURED |
| `onHitActivationChance` | **100.0** | MEASURED (tooltip: *"100% Chance of Activating"*) |
| `skillActiveDuration` | **3.0 s** | MEASURED + tooltip |
| `skillCooldownTime` | **6.0 s** | MEASURED + tooltip |
| `skillLifePercentBuffDuration` | **8.0** (% max health **per second**) | MEASURED + tooltip *"Restores 8% Health Per Second"* |
| `characterManaRegen` | +4.0 / s | MEASURED + tooltip |
| `skillMaxLevel` / `skillTier` | 12 / 2 | MEASURED |

**Mechanic, sim-abstract:** *on a critical hit, if off cooldown, apply a 3-second self-heal-over-time
of 8 % max HP per second; 6-second recharge; no keypress.* **Ceiling per proc = 24 % of max HP.**
It never appears in `Skills Used` because it is not pressed — which is exactly why **no instrument in
this run saw it** until G-6 read a tooltip.

**Magnitude bound, DERIVED and load-bearing.** Procs are gated by crits: **66 crits over the whole
run** (§1.1n). Ceiling = 66 × 24 % of the pool at the time — 66 × 182.2 HP at the R2 pool (759) =
**12,025 HP**; higher if any proc landed at the R3 pool (1600 → 384 HP). Measured `life_healed` for
the run is **12,468.06**. Heals are capped by missing HP, so the realized figure is strictly below the
ceiling. **Reading: Battle Surge is very plausibly the *dominant* healing channel, and cannot be the
*only* one** — the residual routes to the Vampiric Silver Band's attack-damage-converted-to-health
(§1.6). Grade: **DERIVED**, falsifiable by a per-proc reconstruction against the globe series.

**Consequence for the charter's own rulings, stated because it cuts against them:** G-2c ruled the
survivability channel CLOSED (null) on the premise that within-R2 EHP is a monotone function of the
clock with zero residual variance. **That premise held for the HP *pool*. It did not hold for
*recovery*.** A crit-gated regeneration proc switching on mid-regime is a second survivability lever,
inside the regime, invisible to every EHP-vs-behaviour instrument G-2c ran. The null is not
overturned — it is **re-scoped**: it is a null about the pool, not about survivability.

**(b) Amatok's Pact — `amatokpact1.dbr` → `amatokpact1_buff.dbr` — the unmodelled RESERVED AURA**

| Field | Value @ rank 1 | Grade |
|---|---|---|
| `Class` (node / buff) | `Skill_BuffRadiusToggled` / `SkillBuff_Passive` | MEASURED |
| `characterManaLimitReserve` | **50.0** (reserved energy) | MEASURED + tooltip |
| `skillTargetRadius` | **12.0 m** | MEASURED + tooltip |
| `defensiveProtection` (**armor**) | **+16** | MEASURED + tooltip *"+16 Armor"* |
| `characterDefensiveAbility` | **+20** | MEASURED + tooltip |
| `offensiveColdMin` / `Max` | **+5 / +6 flat cold** | MEASURED (`.arz`); tooltip reads **6–8 → 8–10 → 9–10** across the run |
| `offensiveSlowPhysicalGlobal` / `…BleedingGlobal` / `…XOR` | `True` | MEASURED |

**Mechanic, sim-abstract:** *a toggled aura reserving 50 energy that adds **flat cold damage to the
character's attacks** and grants +16 Armor / +20 DA within 12 m.* **It is an added-damage rider, not a
damage-pulsing area effect** — the `offensive*` fields sit on a `SkillBuff_Passive`, and GD's grammar
for that is "added to your hits." Any reading of it as an area DoT is wrong; I record that because I
considered it and it would have mis-explained §6's B-signature.

The tooltip-vs-source delta (5–6 at source, 8–10 in play) is gear amplification — the fixture carries
+% cold on shoulders (*Magestorm*), gloves and shoulders (*of Frostbite*), and legs. Grade: source
**MEASURED**; the in-play values **MEASURED-by-screenshot**; the reconciliation **DERIVED**.

**This lands squarely in the gap v1 §1.8 left open** — *"armour remains an uninstrumented candidate…
`mitigation_delta` must be a free parameter fitted to the intake tail."* Part of the armour is now
named, and it is **not gear** and **not at the R2/R3 boundary**: it switches on **mid-R2**.

### 1.5 Blight of Ch'thon — a static, total retype (MEASURED; **not** a sim mechanism)

| Field | Value | Grade |
|---|---|---|
| `Class` / `skillMaxLevel` | `Skill_Transmuter` / **1** | MEASURED |
| `conversionInType` → `conversionOutType` | **Pierce → Chaos** | MEASURED |
| `conversionPercentage` | **100.0** | MEASURED + tooltip *"100% Piercing Damage converted to Chaos Damage"* |
| Every offensive/defensive/retaliation field | **0.0** | MEASURED — it buys one mechanic and one mesh, nothing else |
| Live from | `play_time` ≤ **3619**, bracketed to (2918, 3619] | MEASURED (G-6 §4) |

**Per charter §14.6, this compiles STATICALLY into the kit spec as retyped damage — the sim needs no
conversion mechanism.** Concretely: **claws' 237 flat and charge's 375 flat are CHAOS, not pierce**,
for the entire band window. G-6's pixel-level oddity (the transform tooltip still printing "Piercing
Damage" after allocation) is recorded as a **tooltip-display artifact**, resolved by the §14.6 ruling.

### 1.6 Gear, and the **six damage channels + two conversions**

Twelve slots, ten filled + shield. All record paths MEASURED (G-7 §3.1); all rolled values
MEASURED-by-screenshot (G-6 §7.1); **all four attested names matched character-for-character by both
instruments** (4/4 EXACT, twice, independently).

| Slot | Display name | Base record (join key) | Rolled values read |
|---|---|---|---|
| **weapon** | **Poisoned Pusquill's Tail of Corrosion** — Rare 1H Mace | `records/items/gearweapons/blunt1h/b015b_blunt.dbr` | 14–40 Physical · 6–12 Acid · **1.78 attacks/s** · **50 Poison over 5 s** · +18 % Acid · +38 % Poison w/ +64 % duration · **18 % Physical→Acid** · **+242 Health** |
| **off-hand** | Bernard's Slightly-Chewed Buckler of Protection — Rare | `records/items/gearweapons/shields/b013a_shield.dbr` | (shield; **carries off-hand damage — see below**) |
| **amulet** | **Menacing Putrid Necklace of Protection** — Rare | `…/necklaces/b001_necklace.dbr` | +21 % Poison · +14 Cunning · **+321 Health** |
| **torso** | **Mystic Salvaged Armor of Menhir's Wall** — Common base + Rare suffix | `records/items/geartorso/a02_torso002.dbr` | **58 Armor** · **+76 Health** · +13 DA · +5 % Spirit · +Phys/Bleed res |
| **waist** | **Mystic Woven Cord of Soulwarding** — Common base + Rare suffix (GDX1) | `…/waist/a02_waist001.dbr` | **7 Armor** · +11 % Physical · +17 % Vitality · **+98 Health** |
| head | Sheltering Salvaged Helmet of the Dranghoul | `records/items/gearhead/a03_head002.dbr` | +OA · +DA · +% health regen · +% cold res |
| shoulders | Magestorm Fur-lined Mantle of Frostbite | `records/items/gearshoulders/a03_shoulder01.dbr` | 16 Armor · +8 % cold · +8 % lightning · +9 % pierce · +8 OA |
| legs | Glacial Patchwork Leggings of the Fox | `records/items/gearlegs/a02_legs01.dbr` | 16 Armor · +cold/+frostburn · +8 Cunning · +38 Spirit |
| feet | Vigorous Reinforced Greaves | `records/items/gearfeet/a02_feet02.dbr` | 12 Armor · **+75 Health** |
| hands | Stalwart Hide Gloves of Frostbite | `records/items/gearhands/a02_hands01.dbr` | +DA mod · +% cold |
| ring1 | **Vampiric** Silver Band | `…/rings/a001_ring02.dbr` | **+% attack damage converted to health** · +energy regen |
| ring2 | Silver Band of Prowess | `…/rings/a001_ring02.dbr` | +Cunning |
| medal / relic | *(empty)* | — | — |

**Matt's "major/minor" split partitions exactly along base-rarity** (weapon + amulet are Rare *bases*;
torso + belt are Common bases with Rare-class *suffixes*) — the intuition was structurally right, the
word "green" over-reached. Recorded because testimony held up better than its own vocabulary.

**THE SIX DAMAGE CHANNELS (v1 carried TWO).** Every row MEASURED unless marked.

| # | Channel | Source, exactly | Magnitude at the band window | Grade |
|---|---|---|---|---|
| **1** | **Physical** | weapon base 14–40, delivered through `weaponDamagePct` (claws 150 %, charge 295 % main-hand) | tooltip: claws *150 % Main Hand (69–85)*; charge *295 % Main Hand (135–166)* | MEASURED |
| **2** | **Acid** | weapon base 6–12 acid **+ 18 % Physical→Acid conversion** (weapon affix) **+ 18 % acid damage** | rides channel 1's magnitude | MEASURED (**conversion #2** — see below) |
| **3** | **Chaos** | claws **237** + charge **375** flat, **100 % Pierce→Chaos** (Blight of Ch'thon) | 237 / 375 per hit | MEASURED (**conversion #1**) |
| **4** | **Poison DoT** | weapon prefix/suffix *"Poisoned … of Corrosion"* — **50 damage over 5 s**, amplified +38 % magnitude / +64 % duration (weapon) + 21 % (amulet) | ~5 ticks at the T-B-measured **1.000 s** period | MEASURED. *(This lands legolas's `componentName`-vs-affix hypothesis: **neither** — it is the weapon's own affix roll.)* |
| **5** | **Bleed DoT** | charge `offensiveSlowBleedingMin` @16 — **270/s × 3.0 s = 810** | on every charge press (175 over the run) | MEASURED |
| **6** | **Cold** | Amatok's Pact flat adder (+5–6 source / 8–10 in play) — **plus** Onslaught's `offensiveColdMin`, which **cannot fire** (set-0 exclusion) | flat per hit | MEASURED |

**TWO STATIC CONVERSIONS, both compile at spec time per charter §14.6:**
**(i) 100 % Pierce → Chaos** (Blight of Ch'thon, §1.5) — ruled.
**(ii) 18 % Physical → Acid** (weapon affix) — **G-6 REQUEST #3, ruled here: same treatment.** It is
a fixed percentage on a fixed weapon with no state dependence, so it is arithmetic on the compiled
magnitudes, not a mechanism the sim must own. **Grade: ruling, veto-open.**

**A seventh contributor v1 and v2-draft-1 both nearly missed: OFF-HAND DAMAGE.** The charge tooltip
reads **"295 % Off-Hand Damage (177–181)"** *alongside* main-hand (135–166) — the form strikes with
both hands, and the off-hand is the **shield**. Off-hand damage is **larger** than main-hand here.
The kit spec must compile main-hand + off-hand into the per-press magnitude; the sim needs no
dual-wield mechanism, but a single-weapon compile **understates the kit's output by roughly a factor
of two on charge.** Grade: MEASURED-by-tooltip; the exact GD dual-strike arbitration is **UNKNOWN**
(whether both land per press, or alternate) → **named band-width input, §6.2.**

### 1.7 The gear step, itemised — `ehp_multiplier` is no longer a fitted parameter

| Source | +Health | Grade |
|---|---|---|
| Weapon — *Poisoned Pusquill's Tail of Corrosion* | **+242** | MEASURED |
| Amulet — *Menacing Putrid Necklace of Protection* | **+321** | MEASURED |
| Belt — *Mystic Woven Cord of Soulwarding* | **+98** | MEASURED |
| Torso — *Mystic Salvaged Armor of Menhir's Wall* | **+76** | MEASURED |
| **Four attested items** | **+737** | DERIVED (sum) |
| **Measured step (T-A max-HP series)** | **759 → 1600 = +841** | MEASURED |
| **Residual** | **+104** = level-up base HP (11→12→13) + physique | DERIVED |

**87.6 % itemised from four flat `+Health` affixes.** v1 carried `ehp_multiplier = 2.11 [MEASURED]`
with `mitigation_delta = UNKNOWN, fitted`. **v2 retires the fit for the HP half outright.**

**Armour, now partly named:** 58 (torso) + 16 (shoulders) + 16 (legs) + 12 (feet) + 7 (belt) =
**≥109 Armor from gear** (helm / gloves / shield not read), **+16 from the Amatok's Pact aura** — and
the aura's contribution arrives **mid-R2, not at the boundary.** `mitigation_delta` is no longer a
free parameter; it is a partially-itemised quantity with a named residual.

**Boundary placement is unchanged and remains DERIVED-NONIDENTIFYING:** no combat between `play_time`
5808 and 6475, so every candidate boundary in the 230 s bracket partitions the engagement data
**identically**. G-5 must not spend error budget there.

### 1.8 **THE A-STEP IS DATED — R2 IS NOT A-STATIONARY** (G-6 F-G6-5; the v1 assumption that broke)

The transform's rank governs the claws rank, which governs target count and arc. G-6's dated series
× §1.3's arrays:

| `play_time` | lvl | transform | **targets** | **arc** | wpn dmg % | tooltip-confirmed |
|---|---|---|---|---|---|---|
| 960 | 2 | 1 | **2** | 90° | 70 % | — |
| 1457 | 3 | 3 | **3** | 110° | 84 % | — |
| 1789 | 4 | 5 | **3** | 110° | 95 % | — |
| 2605 | 6 | 12 | **4** | 130° | 130 % | **YES (f153)** |
| **2918** | 7 | 15 | **5** | **150°** | 145 % | — |
| 3621 → end | 8–13 | **16** | **5** | **150°** | **150 %** | **YES (f210)** |

R2 spans `play_time` 1134–6052. **Within R2 the target cap climbs 2→3→4→5 and the arc 90°→150°,
capping at `play_time` ≈ 2918 — under 40 % of the way through the regime.** Then, in
`play_time` ∈ (2918, 3619], **three further nodes light up at once** (Blight of Ch'thon, Battle Surge,
Amatok's Pact). **R2 contains a build-composition event that no v1 instrument represented.**

**Two facts that constrain the §6 window choice, both computed from the banked per-engagement ledger
this pass:**

1. **R2's first engagement starts at `play_time` 1470.** The 2-target claws window (ranks 1–2, 90°)
   contains **zero R2 engagements.** The fixture never measured A at 2 targets. *(This matters
   because v1 §4.1a's consolation — "at claws ranks 1–2 the sim's fixed 90° cone is an exact match" —
   applies to a rank window with **no fixture data**. See §4.)*
2. **R2's composition is materially different either side of the boundary**, and the difference is
   **not** where v1 would have guessed:

| Window | n eng | kills | kill-events | bursts | **A** [95 % boot] | **B** [95 % boot] | C |
|---|---|---|---|---|---|---|---|
| R2 whole | 77 | 647 | 372 | 169 | **1.7392** [1.6266, 1.8577] | **2.2012** [1.9480, 2.5058] | 2.1948 |
| R2 pre-2918 | 23 | 168 | 102 | 57 | 1.6471 [1.4526, **1.8632**] | 1.7895 [1.5238, **2.0625**] | 2.4783 |
| R2 post-2918 | 54 | 479 | 270 | 112 | 1.7741 [**1.6473**, 1.9130] | 2.4107 [**2.0574**, 2.8333] | 2.0741 |
| **R2b: post-3619** | **49** | **421** | **239** | **99** | **1.7615** | **2.4141** | **2.0204** |

All MEASURED-from-banked-ledger (`galadriel/captures/2026-07-28-gd-playtest-v1-g2b/g2b-per-engagement.csv`,
harness-v1 burst threshold 1.5 s; 20,000-resample engagement-level bootstrap, seed 20260728).

> **A does NOT move detectably across the A-step boundary (CIs overlap heavily). B DOES
> (×1.347, CIs nearly disjoint).** This is the opposite of the naive expectation and it is the single
> most consequential finding in this redraft — see §6.1 S-2.

### 1.9 Controls, timebase, and the corrections carried forward

| Property | Value | Grade |
|---|---|---|
| Deaths | **2**, at `play_time` **3156** and **5453** (**not** 2837 / 5152 — those are `pts_s`) | MEASURED; charter §13.3 **C-3** |
| R2 internal compound gear event | `play_time` ≈ **3256** — +36.9 % pool **and** the run's only `shield_block_chance` change (15.0 → 18.0) | MEASURED; charter §13.3 **C-2** |
| Shield | worn **long before** level 12 — **not** part of the level-12 acquisition event | MEASURED (block series; G-7 §3.3) |
| Coverage | R2 frame **90.11 %**; R3 **75.89 %**, 4 of 16 R3 engagements at **zero** | MEASURED |
| `life_healed` rejection | R1 0.20 % · R2 1.26 % · **R3 15.15 %** | MEASURED |
| `defaultkickattack` | 4 → 19 presses over the run; not in v1's record table | MEASURED (G-6 F-G6-7). Trivial in magnitude; recorded so it is not re-discovered |

**⚠ SWITCH: SPEC-AUTHOR → DRIFT-CRITIC — correction C-6, against my own charter §13.3.**

Charter §13.3 **C-1** states *"the 72.4 %-EHP anchor hit **is death 1**"* and concludes that
R-KC1-8's claim that death 1 was invisible to every instrument is **wrong**. **C-1's labelling is
itself wrong, and C-3 (three bullets later, same section) is why.** Queried against the banked
engagement ledger:

- The **only** engagement in the fixture with `hp_min_observed = 0` is **e082**, `play_time` 5447–5450,
  drop 541 on a 747 pool = **72.42 %** — i.e. the death at `play_time` **5453**, which is
  chronologically the **SECOND** death.
- The death at `play_time` **3156** falls in **no engagement window at all** (e040 ends ≈3050; the
  next window opens later).

So R-KC1-8's original statement was **correct**: one death (the earlier one, `play_time` 3156) is
genuinely invisible to the engagement instrument; the other (`play_time` 5453) is visible as a
floor-censored terminal drop. C-1 correctly identified the visible anchor and **mis-numbered it**,
because it was written in the pre-C-3 timebase. **C-6: the 72.4 % anchor is death 2. R-KC1-8's
death-visibility clause stands as originally written, with C-3's timebase substituted.** → **M10
rider for elrond**, amending the C-1 text banked in `harness_version`.

**A second, band-relevant fact falls out:** e082 — the engagement carrying the fixture's single
largest hazard event — sits at **intake coverage 0.681**. **A coverage ≥ 0.80 gate excludes the
fixture's worst hit.** That is a band-design decision, not a detail (§6.3, pin-sheet item P-5).

---

## §2 — THE COMPILED KIT (what a G-5 harness builds, sim-abstract)

Every value below traces to §1. **No fitted parameters remain except the two marked.**

```
KIT gd-werewolf-kitcal-1  @ MEASURED IDENTITY (Berserker L13, band window play_time >= 3619)

PLAYER
  max_hp                 759  (R2b)  ->  1600 (R3)     [MEASURED; +737 of the step itemised]
  armor                  >=109 gear + 16 aura = >=125   [MEASURED-partial; helm/gloves/shield UNREAD]
  crit_chance            0.0411  (66 crits / 1606 hits) [MEASURED, run-aggregate]
  attributes             physique 122 / cunning 74 / spirit 50   [MEASURED]
  attack cadence         1.78 attacks/s (weapon)        [MEASURED, tooltip]
  block                  15.0% -> 18.0% at play_time 3256  [MEASURED; NOT the gear-step mechanism]

ACTIVES (two; Onslaught is set-0 and CANNOT FIRE)
  claws   geometry = ARC, 150 deg, TARGET CAP 5, reach = weapon melee reach [UNKNOWN]
          magnitude = 150% main-hand + off-hand (shield) + 237 flat CHAOS
          cost 5 energy, no cooldown (basic-attack modifier)
  charge  geometry = PATH, 14.0 m travel, 2.5 m radius (x1.5 terminal)
          magnitude = 295% main-hand + 295% off-hand + 375 flat CHAOS
                    + BLEED 270/s for 3.0 s
          cooldown 4.0 s, +200% run speed, knockdown 0.5 s, cost 42

DOTs
  poison  50 over 5 s, tick period 1.000 s, +38% magnitude / +64% duration / +21%   [weapon; R3 only]
  bleed   810 over 3 s, on every charge press                                        [R2 AND R3]

PASSIVE / TOGGLE  (v1 modelled NEITHER)
  battle_surge   trigger on_crit (100% chance if off cooldown)
                 -> self heal-over-time, 8% max_hp/s for 3.0 s, 6.0 s recharge
  amatok_aura    reserve 50 energy -> +16 armor, +20 DA, +5..6 flat cold on hits, 12 m radius

STATIC COMPILES (charter 14.6 — no sim mechanism required)
  100% Pierce -> Chaos     [Blight of Ch'thon]          -> retype claws 237 / charge 375
   18% Physical -> Acid    [weapon affix]               -> split channel 1 magnitude

STILL FITTED (2, down from 3)
  mitigation_delta_residual   helm/gloves/shield armor UNREAD; GD armor absorption 70%
  offense_delta_offhand       dual-strike arbitration UNKNOWN (both per press? alternating?)
```

---

## §3 — OPPOSITION PIN (H-3 inputs, carried by reference)

G-5a × G-5b compose into the comparability verdict already filed at charter §14.6. Carried here only
as the spec's boundary conditions:

| # | Input | Value | Source |
|---|---|---|---|
| O-1 | GD level-12 Normal/1P trash HP | 181 – 821 | G-5a §2 |
| O-2 | GD per-hit damage band, **all tiers** | **33 – 67** ≈ **2.5 % of the 1600 pool**, ≈ **5.4 % of 759** | G-5a §4 |
| O-3 | Tier differentiation axis | **HP, not damage** (200× HP span against a 2× damage span) | G-5a §4 |
| O-4 | Concurrency cap | `numAttackSlots = 4` → ≈ 4 × 41 = 164 dmg/round ≈ 10.3 % of the post-gear pool | G-5a §3 |
| O-5 | Pack sizes, Act-1 pools | 1–8 (zombie), 2–9 (boar), 3–10 (skeleton), 8–16 (skeleton ambush); champion 10–50 % | G-5a §3 — **wider than v1's corpus-wide 3–6 prior; use G-5a's zone-specific pools** |
| O-6 | Injection into the sim | **YES, no engine code change** (`run_spatial_fight` / `entity_from_monster_dict` / `SpatialFightEngine`); GD precedent in-tree (`tsf6_track_a_harness.py`) | G-5b §0, §2 |
| O-7 | Blocking gaps | **BQ-3** (player `max_hp` floor 10,000 + hardcoded-zero defence on the projection path) and likely-**ABSENT attack-slot arbitration** | charter §14.6 |
| O-8 | **Units ruling** | comparison runs in **normalized units — TTK in seconds, intake as a fraction of max HP** — because absolute player HP cannot be pinned below 10,000 | **G-5b §7.3, ADOPTED into §6 below** |

**Two G-5a risks the bands must not silently absorb:** the `monsterAttributePak` multiplicative
composition is **DERIVED by contradiction, not proven** (§1f), and weapon-wielder damage excludes the
rolled weapon. Both are validatable **against this fixture itself** — the predicted 33–67 band against
the measured intake distribution and `hitsReceived = 500`. That validation is a **pre-G-5 gate**, not
a band.

---

## §4 — MECHANISM-REQUIREMENTS MANIFEST — **DELTA against v1 §4**

**⚠ SWITCH: SPEC-AUTHOR → DRIFT-CRITIC.** §1–§3 authored a spec; this section judges the sim against
it, read-only. The seam is live and declared.

v1's manifest graded 21 mechanism classes across the three signatures: **1 ABSENT** (A3, target cap),
**1 PRESENT-MISCALIBRATED** (A2, fixed 90° cone), everything else PRESENT-CALIBRATABLE. **Those grades
stand.** v2 changes their *severity* and adds four classes the measured kit demands.

### 4.1 A2 and A3 are worse than v1 read them — because the band window moved

v1 §4.1a offered a consolation: *"at claws ranks 1–2 the sim's 90° cone is an **exact match**. The
fixture's own R2 is therefore reproducible today if the rank was low."* **The rank was not low, and
the low-rank window contains no fixture data** (§1.8 fact 1). The band window (§6) requires
**150° arc, 5-target cap**. Against that:

| Class | v1 grade | v2 grade | What changed |
|---|---|---|---|
| **A2** — cone / arc geometry | PRESENT-MISCALIBRATED *(with a low-rank exact-match escape)* | **PRESENT-MISCALIBRATED — escape retired** | `CONE_HALF_ANGLE_RAD = π/4` (90° full) vs the fixture's **150°**. The sim under-covers by 60° across the entire comparison window. **BQ-2 is now on the critical path, not a future concern.** |
| **A3** — target-count cap | ABSENT | **ABSENT — and now load-bearing in the opposite direction** | GD caps at 5; the sim's cone returns **every** target in the wedge. Against G-5a's zone pools (up to 8–16, O-5), an uncapped 150°-equivalent geometry **over-kills**. v1 framed A3's absence as a breadth *limitation*; at measured density it is a breadth *runaway*. |

**Net: both A-step gaps now bite inside the band window, in opposite directions, and they partially
cancel.** A narrower-than-GD arc with no cap, against packs larger than the cap, can produce
approximately the right A for entirely the wrong reason. **That is a D-1-pattern trap** (a legible,
wrong answer) and G-5 must report the *mechanism* alongside the number: if A lands in band, the
manifest grades still govern the verdict per R-KC1-9.

### 4.2 FOUR NEW CLASSES the measured kit demands (v1 had no row for any of them)

| # | Mechanism class | Obligation | Grade | Evidence / the check still needed |
|---|---|---|---|---|
| **D1** | **Crit-gated self-buff trigger** (`on_crit` → apply an effect to the **attacker**) | **genre-obligatory** — on-crit/on-kill triggers are the ARPG proc grammar (D2 on-striking charges, D3 legendary procs, PoE trigger gems, GD's whole `Skill_PassiveOn*` family) | **PRESENT-SUBSTRATE / ABSENT-CONSEQUENCE** | The event **is** emitted (`damage_resolver.py:1349` `events.append("on_crit")`) and a Wave-C dispatcher **does** consume the tick event log (`spatial_engine.py:3592 _wave_c_process_tick_events`). But the mark-consume path reads **defender** marks (`_defender.combatant_state.active_effects`) and dispatches a consequence at the defender; **no consumer applies a self-buff to the attacker on `on_crit`** — the only literal `"on_crit"` consumer site anywhere under `simulation/` is the emitter itself. **CHECK FOR GAMORA:** can `_wave_c_dispatch_consequence` target the attacker? If yes → PRESENT-CALIBRATABLE. If no → **ABSENT, and it routes to the build queue as BQ-4.** |
| **D2** | **Percent-of-max-HP heal-over-time** | genre-obligatory | **PRESENT-CALIBRATABLE, with a unit mismatch** | `effect_resolver.py:121-129` `heal_over_time` exists, ticks, caps correctly (`min(tick_heal, max_hp - hp)`), and feeds `heals_received` / `bc_signals.hot_recovered`. But `tick_heal` is **flat**, GD's is **% max HP per second**. At a pinned `max_hp` this is a harness-side constant — a compile, not a mechanism gap. Tick period already matches (`DOT_TICK_INTERVAL = 1.0` vs GD's 1.000 s). |
| **D3** | **Reserved-resource toggled aura granting flat added damage + armor + DA** | genre-obligatory | **PRESENT-CALIBRATABLE** | `class_dict` carries `resource_economy{}` incl. **reservations** and `aura_geometry{}` (G-5b §5.1); `spatial_engine.py:3065 _refresh_aura_statmod_riders` refreshes stat riders from live aura carriers each tick. **Caveat:** the armor half is blocked by **BQ-3** (projection-path defence hardcoded to zero) — a *player-pinning* gap, already on the queue, not a new one. |
| **D4** | **Static damage-type conversion at spec-compile** | **not required — deliberately** | **N/A by ruling** | Charter §14.6 rules both conversions compile statically. Listed to **close the class**, so nobody later reads "the sim has no conversion mechanism" as a gap. It is not. |

### 4.3 Revised manifest summary

| Signature | Classes (v1 → v2) | PRESENT-CALIBRATABLE | PRESENT-MISCALIBRATED | ABSENT / pending |
|---|---|---|---|---|
| **(i) A-step** | 6 → 6 | 3 (A1, A4, A5) | **1 (A2 — escape retired, now on the critical path)** | 1 (A3) + 1 deprecated trap (A6) |
| **(ii) B DoT-tail** | 8 → 8 | 6 (B1–B6) | 0 | 1 correctly-absent (B8) · 1 naming item (B7) |
| **(iii) Gear-step** | 7 → 7 | 6 (C1–C6) | 0 | 1 correctly-absent-for-this-kit (C7) |
| **(iv) Kit composition — NEW** | — → 4 | 2 (D2, D3) | 0 | **1 pending-check (D1 → possible BQ-4)** · 1 closed-by-ruling (D4) |

> **Headline, v2:** the genre-gap map is still small and still geometric — **A2 and A3, both on the
> A-step, both geometry** — but **the low-rank escape hatch is gone**, and there is **one new
> candidate absence (D1, the crit-trigger consequence)** whose resolution is a single question to
> gamora. **BQ-1** (target-count cap) and **BQ-2** (per-skill / rank-scaling cone) are re-issued at
> raised priority; **BQ-3** (player HP floor + zero-defence projection path) is carried from §14.6;
> **BQ-4** (attacker-targeted trigger consequence) is **conditional on the D1 check**.

**G-5 pre-flight assertions, four (G-5b §7.2, endorsed):** `pack_proxy_size == 0` on every combatant ·
`apply_mob_hp_difficulty_multiplier = False` · `len(mob["skills"]) > 0` for **every** injected mob
(a skill-less mob is **silently pacifist** — G-5b's probe measured `dmg_taken = 0.0` across 3 fights,
8 mobs, 16 s) · an **explicit recorded decision** on `SPATIAL_DAMAGE_SCALE = 0.6`.

---

## §5 — ADAPTER SPEC (AD-1 … AD-9): **carried from v1 §5 unchanged**, plus three riders

The architectural law is unchanged and must not erode: **the sim never sees pixels; the adapter never
touches mechanics.** Requirements AD-1 … AD-9 stand verbatim (v1 §5.3). Three riders from v2's
evidence:

| # | Rider | Why |
|---|---|---|
| **AD-10** | The adapter must emit a **`kit_epoch`** column alongside `harness_version`, keyed to the §1.8 rank/composition schedule. | R2 is not one build. A ledger that cannot say *which* build produced a row cannot support the §6 window ruling, and the next fixture (C2 EoR) will have the same problem the moment the player levels. |
| **AD-11** | **Untriggered / unpressed channels must be emitted**, not inferred from press counters. | Battle Surge and Amatok's Pact are invisible to `Skills Used` **by construction**. A press-counter-derived ledger structurally cannot see them. This is the generalizable lesson of G-6 F-G6-6, and it will recur on every passive-heavy kit. |
| **AD-12** | Coverage must be emitted **per engagement, not only per regime**, and the band's coverage gate must be a **declared parameter**, not a hardcoded 0.80. | §1.9: a 0.80 gate excludes the fixture's single worst hazard event (e082, coverage 0.681). Whether that exclusion is right is a *decision*; it must be visible as one. |

---

## §6 — H-2 ACCEPTANCE BANDS — v2 REDRAFT (DRAFT until Matt pins)

### 6.0 Preamble — three sentences that outrank every number below

> **1.** Per **R-KC1-9** these are **secondary corroboration**. **A band miss with all three structural
> signatures reproduced is a PASS with a tuning note. A band hit with a signature absent is a FAIL.**
> **2.** Per **G-5b §7.3 / O-8**, every band is stated in **normalized units** — **TTK in seconds** and
> **intake as a fraction of max HP** — because the sim's player HP floor (10,000) makes absolute HP
> parity unreachable. This turns the floor from a fudge into a non-issue.
> **3.** **G-5 runs the coverage gate FIRST** (charter T-5). Bands are read only after it.

### 6.1 THE WINDOW RULING — and the fork Matt pins

**The problem v1 did not have.** v1 banded "R2" as one thing. §1.8 shows R2 contains a rank climb
(target cap 2→5, arc 90°→150°, weapon damage 70 %→150 %) **and** a three-node composition event.
**A sim pinned to one compiled kit cannot represent both halves of R2.** The window must be
kit-exact or the comparison is against a moving target.

**Three candidate windows, all measured (§1.8), with their costs:**

| Option | Window | n eng | kills | A | B | Kit-exactness |
|---|---|---|---|---|---|---|
| **W-a** | R2 whole (`play_time` 1134–6052) | 77 | 647 | 1.7392 | 2.2012 | **NO** — spans a rank climb + a composition event |
| **W-b** | R2 post-cap (`≥ 2918`) | 54 | 479 | 1.7741 | 2.4107 | **PARTIAL** — cap is stationary, but 5 engagements predate Blight/Battle Surge/Amatok |
| **W-c ← MY LEAN** | **R2b, post-composition (`≥ 3619`)** | **49** | **421** | **1.7615** | **2.4141** | **YES** — every node in §1.2 allocated, cap at 5, arc 150°, transform maxed |

**I choose W-c (`play_time ≥ 3619`) and mark it Matt-pinnable (P-1).** Five reasons, in order of
weight:

1. **Kit-exactness is the binding constraint, not A-stationarity.** The sim compiles one kit. W-c is
   the only window where the fixture *was* that kit. W-b's extra 5 engagements were played without
   Pierce→Chaos, without the sustain proc, and without the armour aura — three of the six things §2
   compiles.
2. **The A cost of segmenting is nil.** A pre-2918 = 1.6471 [1.4526, 1.8632] vs post = 1.7741
   [1.6473, 1.9130] — **CIs overlap heavily.** Discarding 23 engagements costs almost nothing in A,
   because A barely moved across the A-step. *(That is itself a finding: the multi-kill signature is
   dominated by pack geometry, not by the marginal target-cap increment.)*
3. **The B cost of NOT segmenting is severe.** B pre-2918 = 1.7895 [1.5238, 2.0625] vs post = 2.4107
   [2.0574, 2.8333] — a **×1.347 lift with nearly disjoint CIs, and NO DoT was added at that
   boundary.** Carrying W-a would band a B contaminated by a within-window regime change of almost
   exactly the size of the signal S-2 is trying to detect (see §6.1a).
4. **Intake barely weakens.** W-b carries 84.1 % of R2's gated intake; W-c carries 76.0 %.
5. **W-c costs only 5 engagements against W-b** (49 vs 54) and A/B move by < 1 %.

**Cost, stated plainly:** W-c retains **49 of 77 R2 engagements (63.6 %) and 421 of 647 kills
(65.1 %)**. The discarded 28 engagements are **retained as report-only**, exactly as R1/R3 are.

#### 6.1a — The S-2 confound this window ruling exists to remove

v1's S-2 read: *"adding a DoT lifts B and not A, not C."* The measured comparison v1 drew was
R2 → R3, B 2.27 → 2.94 (**×1.30**). But the **within-R2** lift at the composition boundary is
**×1.347** — *larger*, and **no DoT was added there**. If B rises by the same amount for a reason
that is not a DoT, then **B alone does not identify the DoT-tail signature**, and v1's S-2 was
weaker than it read.

**Segmenting to W-c repairs it.** Like-for-like, W-c → R3 is **B 2.4141 → 2.9412 = ×1.218**, against
a within-R2 lift that is now *outside* both windows. The S-2 claim becomes: *the DoT-tail lift is
×1.22 on a kit-exact base*, which is a smaller, honest, and **testable** claim, rather than a larger
contaminated one. **This is the redraft's single most important numeric correction and it makes the
target harder, not easier.**

**What most plausibly caused the within-R2 B lift** (offered as hypothesis, not banked): weapon damage
% climbed 130→150 and the target cap 4→5 over the same span, so more kills land inside a single
sustained burst. **B measures sustained throughput, not DoT specifically.** Any future fixture must
carry that caveat.

### 6.2 STRUCTURAL TARGETS (PRIMARY — these outrank §6.3–6.4)

> **⚠ AMENDED — S-1 by §10.2, S-2 by §10.3 (2026-07-28).** The S-1 control predicate below
> (`A ∈ [0.98, 1.05]`) is a **defective instrument** — see §10.2. The S-2 predicate below is
> **degenerate on both legs** — see §10.3. Both rows stand as the pre-registered text KC1 was graded
> against; **neither may be quoted forward as-written.** S-3 stands unamended (see §10.4).

| # | Claim | Window | Fixture value (grade) | **Pass/fail predicate** | Honorable-fallback category on miss |
|---|---|---|---|---|---|
| **S-1** | **A-step exists**: a single-target basic attack yields A ≈ 1; an arc-with-cap kit yields A > 1, at `.arz`-plausible density | R1 (control) vs **W-c** | R1 **A = 1.000** exactly (43 kills / 43 kill-events, 0 multi-kills, p = 7.0e-11); **W-c A = 1.7615** (MEASURED) | Single-target arm returns A ∈ [0.98, 1.05]; arc arm returns **A > 1.25** at G-5a pack sizes (O-5), **without** needing density outside those pools | **(ii) sim-mechanics divergence** if the arc arm fails at plausible density; **(iv) mechanism-class absence** if it fails *because* A3 (no target cap) or A2 (90° cone) is the proximate cause — which G-5 must state, not infer |
| **S-2** | **The DoT-tail lift is confined to B**: adding a DoT lifts kill-events-per-burst, and moves **neither A nor C** | **W-c → R3**, like-for-like | **B ×1.218** (2.4141 → 2.9412, MEASURED); A 1.7615 → 1.9000 (**CIs overlap** — A is *not* claimed to move); C 2.0204 → 2.1250 | Adding the poison DoT to the compiled kit lifts **B by ≥ 1.10×**, with **A and C each within their bootstrap CI** of the no-DoT arm | **(ii)** if B fails to lift; **(iii) fixture-measurement error** if A or C also moves — because that reproduces the §6.1a confound and indicts the *segmentation*, not the sim |
| **S-3** | **The gear step inverts hazard SHAPE, not just scale** | W-c → R3 | Worst-drop **p99: 33.02 % → 7.38 %** EHP; **max: 72.42 % → 8.50 %** EHP; drops ≥ 10 % EHP: **27 of 332 → 0 of 109** (all MEASURED, `fixtures.db`) | A ×2.11 EHP step **plus** the itemised mitigation (§1.7) drives the **≥10 %-EHP drop count to zero or near-zero** and the p99 worst-drop **below 12 % EHP** — i.e. a fall in *normalized* worst-hit, not merely in raw HP | **(ii)** if the sim's hazard tail survives the step; **(iv)** if it survives *because* player defence cannot be pinned — **BQ-3**, already known |

**A note on S-1's second instrument.** §1.1p gives a fully independent AoE-breadth check:
**1606 hits / 680 presses = 2.362 hits per press**. If `hitsInflicted` excludes DoT ticks, the sim's
mean `len(targets_hit)` per player skill press should land near 2.36 at G-5a densities. **Its
semantics are UNCERTAIN**, so it is offered as a **diagnostic, not a band** — but a sim that returns
5.0 hits/press (uncapped 150°-equivalent against 8-mob packs) versus a fixture at 2.36 would expose
A3 directly, which A alone may not.

### 6.3 SECONDARY NUMERIC BANDS — normalized units, W-c window

> **⚠ AMENDED by §10.1 (2026-07-28).** Eleven of the twelve bands below bind to "W-c", a window whose
> **sim-side membership was never pinned** for a composition-*designed* battery, and every aggregate
> below is a function of a **tier-weighting rule that was never pre-registered** (verdict §2.3). No
> band below is citable — as pass OR fail — on any battery until it is read through §10.1's cut rule.

All fixture values MEASURED from `fixtures.db` (`regime_stat` / `v_engagement_wide`, session
`GP-gd-2026-07-26-s1`, segmentation `S1-gap5s-v1`) or DERIVED from the banked per-engagement ledger,
**re-cut to W-c this pass. None is inherited from v1's arithmetic.**

| # | Quantity | Window | Fixture (grade) | **Proposed band** | Width rationale |
|---|---|---|---|---|---|
| **N-1** | Median encounter duration | W-c | **4.5 s** (R2 whole; MEASURED) | **3.0 – 7.0 s** | 4.5 s at 0.5 s sampling = 9 samples ≈ 11 % quantization. ≈ ±50 %. |
| **N-2** | Mean / median duration ratio | W-c | **1.311** (post-2918; DERIVED) | **1.10 – 1.80** | Right-skew is the shape claim; the ratio tests skew without pinning either moment. |
| **N-3** | Max encounter duration | W-c | 27.5 s (R2); 37.5 s (all-106) | **≥ 18 s present** | One-sided *existence* test. Maxima are not bandable at n = 49. |
| **N-4** | **A** — kills per kill-event | W-c | **1.7615** (MEASURED from ledger; W-c bootstrap CI ≈ [1.63, 1.91] by continuity with W-b) | **1.45 – 2.10** | Now a *read* value, not v1's derived 1.74. Band ≈ ±3× the CI half-width, absorbing density-sweep spread. |
| **N-5** | **B** — kill-events per burst | W-c | **2.4141** (MEASURED) | **1.95 – 3.00** | B is the most robust of the three at the instrument-canonical 1.5 s burst grain. |
| **N-6** | **C** — bursts per encounter | W-c | 2.0204 | **DECLARED NON-TARGET** (R-KC1-9) | Player + level routing. Reported, never scored. |
| **N-7** | Fraction of encounters with **zero** recorded intake | W-c, coverage ≥ 0.80 | **0.378** (14 of 37; MEASURED) | **within ±0.15 absolute** | The zero-inflation *is* the hazard shape, and it is the most coverage-sensitive quantity on the table. |
| **N-8** | Median encounter intake, **% of max HP** | W-c, cov ≥ 0.80 | **1.79 %** (MEASURED) | **0.5 % – 5.0 %** | Normalized per O-8. Wide because 37 engagements and a zero-inflated distribution. |
| **N-9** | **Worst single drop per encounter, % of max HP — median** | W-c, cov ≥ 0.80 | **1.79 %** (MEASURED) | **0.8 % – 5.0 %** | The per-hit hazard *floor*. Pairs with N-10 to bracket the distribution without pinning a mean. |
| **N-10** | **Worst single drop, % of max HP — p90** | W-c, cov ≥ 0.80 | **16.82 %** (MEASURED) | **8 % – 30 %** | The tail. **This is the single best one-number summary of hazard shape** and the band most likely to catch a mis-pinned opposition. |
| **N-11** | Largest single intake event, % of max HP | W-c, **coverage-gate OFF** | **72.42 %** (MEASURED; **floor-censored — it is death 2**, true damage ≥ 541) | **≥ 40 % present** | One-sided existence test: the sim must be *capable* of a near-lethal single hit. Censoring makes an upper band meaningless. **Requires the gate off — see P-5.** |
| **N-12** | Share of total intake carried by drops ≥ 10 % EHP | **R2 whole only** | **46.82 %** (MEASURED) | **30 % – 65 %**, **flagged NOT-RECUT** | ⚠ This is the one band that **cannot** be re-cut to W-c from the store — it is drop-level, and `regime_stat` holds it only at regime grain. Either accept it at R2-whole grain with the non-stationarity caveat, or commission a galadriel `tb_rollup.py` re-cut. **Pin-sheet P-4.** |

### 6.4 The Q2 terminal-concentration qualifier (charter §13.2) — **carried, and it got sharper**

G-2c ruled the R2 intake tail **genuine but LATE**: ≥40 HP hits ×4.70 exposure-matched (p = 9.3e-6),
with **5.8 % of covered time holding 43 % of intake.** Re-cut to W-c this pass:

| Cut | n eng (cov ≥ 0.80) | Total intake | Median intake, %EHP | Median worst-drop, %EHP |
|---|---|---|---|---|
| W-c, all | 37 | 3,188 HP | 1.79 % | 1.79 % |
| W-c **minus the terminal 8 engagements** | 34 | 1,565 HP | 1.56 % | 1.56 % |
| **The terminal 8 alone (3 covered)** | **3** | **1,623 HP** | **87.9 %** | **41.9 %** |

> **Three engagements carry 50.9 % of W-c's measured intake.** Every band in §6.3 that reads a mean or
> a tail is a statement about a distribution with a three-point mass at its end. **N-10 and N-11 in
> particular must be read as "the fixture is capable of this," not "the fixture does this
> routinely."** A sim that reproduces the *median* and misses the *tail* has missed the more important
> half — and vice versa. **This qualifier travels with every §6.3 row, always.**
> *(And it carries its own coverage caveat: C-4 — globe OCR coverage degrades exactly where this mass
> lands, ρ = −0.432.)*

### 6.5 R3 — report-only, and it never travels bare

Per R-KC1-9, R1 and R3 are **report-only**; no band binds them. Every R3 figure carries **both**
conditions or it is not quoted:

> **R3 figures are (a) POST-GEAR-STEP and (b) COVERAGE-HOLED** — 4 of 16 engagements (33 kills) at
> zero coverage; `life_healed` rejection **15.15 %** against R2's 1.26 %; **R3 mean intake is 163.3
> (delta-gated) or 188.4 (frame-gated)** and **must never travel as a bare number.**

R3's role is **structural only**: it is the evidence for S-2 and S-3. Its 16 engagements could not
support a band and are not asked to.

---

## §7 — v1 → v2 DELTA: what changed, and which instrument forced it

| # | v1 said | v2 says | Forced by | Consequence |
|---|---|---|---|---|
| 1 | Level ~11–12 | **Level 13** | **G-7** (`.gdc` + two `.arz` arithmetic checks) | Sets the G-5a opposition level and the attribute pin |
| 2 | Skill ranks **UNKNOWN** — "the single largest identity gap" | **All 8 rows MEASURED** | **G-7** + **G-6**, independently, agreeing | The gap is closed; §6's bands re-centre on a known rank |
| 3 | Three skills modelled (claws, charge, Onslaught-inert) | **Five allocated nodes; two of them unmodelled mechanics** | **G-6** (tooltips) + **G-7** (rank list) | §2 gains a sustain channel and an aura; §4 gains four manifest rows |
| 4 | `werewolf1b` **"likely untaken"** | **ALLOCATED 1/1 — 100 % Pierce→Chaos** | **G-6** and **G-7** (both, blind to each other); Matt reconciled | The kit's flat damage is **chaos**, not pierce, for the whole band window |
| 5 | `werewolf2` = "the spec's largest sensitivity" | **Measured-absent.** Sensitivity **closed in the spec's favour** | **G-6** (effect-absence in the tooltip) + **G-7** | v1's biggest declared risk evaporates |
| 6 | **Two** damage channels (physical + pierce) | **Six channels + two static conversions + off-hand** | **G-6 §7.1 / F-G6-10** | The compiled magnitude in §2 roughly doubles on charge and re-types entirely on the flat component |
| 7 | `ehp_multiplier` MEASURED, `mitigation_delta` **free, fitted** | **87.6 % of the HP step itemised**; ≥125 Armor named | **G-6 F-G6-9** | One fitted parameter retired; the other partially named |
| 8 | Poison DoT: period only, magnitude UNKNOWN, source hypothesized as a component | **50 over 5 s, +38 %/+64 %/+21 %, source = the weapon's own affix roll** | **G-6 F-G6-10** | legolas's `componentName` hypothesis is falsified — recorded because it was correctly banked as a hypothesis, not adopted |
| 9 | **R2 is "the fixture"** — one stationary build | **R2 is not A-stationary and not composition-stationary.** Band window re-cut to `play_time ≥ 3619` | **G-6 F-G6-5** (the dated rank series) | **The largest structural change in this redraft.** §6.1 |
| 10 | A ≈ 1.74, **DERIVED by arithmetic**, band 1.35–2.20 | **A = 1.7615 MEASURED** on the W-c window, band 1.45–2.10 | banked G-2b per-engagement ledger, re-cut this pass | v1's arithmetic was very nearly right (1.7392 whole-R2); the band tightens because the value is now read |
| 11 | B = 2.27, band 1.80–2.90; S-2 lift ×1.30 | **B = 2.4141 MEASURED**, band 1.95–3.00; **S-2 lift corrected to ×1.218** | ledger re-cut + the §6.1a confound | **The target got harder.** v1's B was 3 % high and its S-2 lift was contaminated |
| 12 | Intake bands in raw HP + a median/max ratio hedge | **All bands in normalized units (% max HP, TTK seconds)** | **G-5b §7.3** (player HP floor 10,000 unreachable) | The HP-floor problem becomes a non-issue instead of a fudge |
| 13 | Density prior: corpus-wide pools, **3–6 centred on 4** | **G-5a's zone-specific Act-1 pools: 1–8 / 2–9 / 3–10 / 8–16, champion 10–50 %** | **G-5a §3** | Wider and *actual*; v1's prior was adequate-for-a-sweep and is now superseded by measurement |
| 14 | A2's escape hatch: *"at ranks 1–2 the sim's 90° cone is an exact match"* | **Escape retired** — the band window is 150°/5-target and the low-rank window has **zero fixture engagements** | §1.8 fact 1, computed this pass | **BQ-2 moves onto the critical path** |
| 15 | Difficulty **UNKNOWN** (`notes.md` absent) | **Normal, 1 player, shipping Act-1 tuning** | **G-7 §1.12** + Matt's **C-5** | Fixes the G-5a pak index to 0 — every opposition number depends on it |
| 16 | *(no row)* | **C-6: the 72.4 % anchor is death 2, not death 1; R-KC1-8's death-visibility clause stands** | ledger query this pass, against charter §13.3 C-1 | M10 rider for elrond; a self-correction on my own correction |
| 17 | *(no row)* | **G-6's two out-of-seam REQUESTS closed**: the 1/12 nodes are `passive02` + `amatokpact1`; the 18 % Physical→Acid conversion compiles statically | `.arz` reads this pass | G-6's open items discharged |

**What did NOT change, and is worth saying:** the §2 **replacement ruling** (Onslaught is excluded by
set partition, not augmented) survived four new instruments and gained a fifth line — the game's own
tooltip text. The **adapter spec** AD-1…AD-9 stands unamended. The **manifest's B and C sections**
(6/6 and 6/6 present) stand unamended. **v1's structural reading was right; its identity was wrong.**

---

## §8 — H-2 PIN SHEET — the minimal set Matt must ratify

Everything below is a **decision**, not a finding. Each has my lean, and each is veto-open. G-5
cannot execute until P-1, P-2 and P-3 are pinned; P-4 … P-8 can ride as declared defaults if Matt
prefers.

| # | Decision | Options | **My lean** | Cost of the alternative |
|---|---|---|---|---|
| **P-1** | **The band window.** R2 is not one build. | **W-a** R2 whole (77 eng) · **W-b** ≥2918 (54) · **W-c** ≥3619 (49) | **W-c.** Kit-exact; A costs nothing to segment; B is badly confounded if we don't (§6.1a) | W-a bands a moving kit and inflates the S-2 target by ~10 % for a non-DoT reason |
| **P-2** | **Ratify the §6.2 structural targets S-1 / S-2 / S-3** with their predicates | as drafted · amend · reject | **as drafted**, noting S-2's lift is now **×1.218**, not v1's ×1.30 | Un-preregistered structure = the run can move its own goalposts |
| **P-3** | **Ratify the §6.3 numeric bands N-1 … N-12** as *secondary corroboration* | as drafted · widen · narrow | **as drafted.** They are deliberately wide; false precision at n = 49 teaches nothing | Narrower bands convert honest misses into noise |
| **P-4** | **N-12 (tail-dominance share) cannot be re-cut to W-c from the store.** | (a) accept at R2-whole grain with the non-stationarity caveat · (b) commission a galadriel `tb_rollup.py` re-cut · (c) drop N-12 | **(a) accept with the caveat.** It is one band of twelve, and (b) costs a galadriel lane for marginal tightening | (b) delays G-5; (c) loses the best single tail statistic |
| **P-5** | **The coverage gate is a decision, not a default.** A ≥0.80 gate **excludes the fixture's worst hazard event** (e082, coverage 0.681, the 72.4 % drop). | (a) gate at 0.80 for N-7…N-10, **off** for N-11 *(as drafted)* · (b) gate everything at 0.80 · (c) gate everything at 0.60 | **(a).** Distribution bands want clean data; an *existence* test wants the event | (b) makes N-11 untestable; (c) admits 15 low-coverage engagements into every distribution band |
| **P-6** | **D1 — the crit-trigger consequence.** Battle Surge needs an attacker-targeted `on_crit` consequence; the sim emits the event but I found no consumer that self-buffs. | (a) route the one-question check to gamora **before** G-5 · (b) run G-5 with Battle Surge unmodelled and declare it · (c) open BQ-4 now | **(a).** It is one question, it is cheap, and the answer decides whether the kit's whole sustain channel is expressible | (b) runs the comparison with a known-absent mechanic and pre-poisons S-3's intake side |
| **P-7** | **Off-hand damage.** The shield contributes 295 % off-hand on charge (177–181), *larger* than main-hand. GD's dual-strike arbitration is UNKNOWN. | (a) compile **both** hands into the per-press magnitude · (b) main-hand only · (c) hold G-5 for a `.arz`/animation resolution | **(a), declared as an upper bound**, with (b) run as a sensitivity arm | (b) alone understates charge output ~2×; (c) is a new lane for a factor the bands can absorb |
| **P-8** | **G-5a's `monsterAttributePak` composition is DERIVED by contradiction, not proven** (§3). | (a) validate against this fixture's own intake distribution + `hitsReceived = 500` **before** G-5 · (b) run and treat a miss as unattributable | **(a).** It is free — the fixture is the validator — and it is exactly R-KC1-12's "exclude instrument error first" | (b) makes every intake-side miss confounded between kit model and opposition model |

**Two things I am NOT asking Matt to pin, and why:** the **manifest grades** (§4) are measurements
against code, not preferences — they bind regardless. The **charter §7 honorable-fallback categories**
are already ratified; §6.2 merely names which category each miss routes to, in advance, so the
decomposition is pre-committed rather than argued afterward.

---

## §9 — PROVENANCE

**`.arz` reads performed this pass (read-only, zero failures):** `passive02` · `amatokpact1` ·
`amatokpact1_buff` · `werewolf1` · `werewolf1_skill01_claws` · `werewolf1_skill02_charge` (all GDX3),
via `agentic_orchestration/gandalf/scratch/2026-07-28-kitcal1-g4-arz/g4_arz_probe.py` — a thin wrapper
importing legolas's proven `ArzArchive` (`research/scripts/gd_arz_adapter_2026_07_24.py`). **No new
parser was written.** Corpus: `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/`.

**`fixtures.db` queried (read-only), schema `fixtures-v0.6`:** `regime_stat` (R1/R2/R3 ×
engagement_seconds, intake_pc_ehp, hp_drop_pc_ehp, hp_drop_size, frac_intake_from_drops_ge_10pc_ehp,
kills_per_engagement) · `v_engagement_wide` (106 engagements) · `session_regime` · `segmentation_run`
· `measure_dict`. **A/B are NOT ingested** (`C-AB-NOT-INGESTED`, queued **M10**); the store itself
names the address, and I re-cut from it:
`galadriel/captures/2026-07-28-gd-playtest-v1-g2b/g2b-{abc-factors,per-engagement}.csv`. Bootstrap:
20,000 engagement-level resamples, seed 20260728.

**Sim files audited (read-only, no modification):** `simulation/damage_resolver.py` ·
`simulation/effect_resolver.py` · `simulation/combatant.py` ·
`simulation/spatial_gauntlet/spatial_engine.py` · `…/spatial_resolver_adapter.py` ·
`…/proxy_population.py`.

**Upstream notes consumed in full:** G-4 v1 · charter §§12–14 · `legolas/notes/…g7-gdc-save-findings.md`
· `galadriel/notes/…g6-skill-screenshots.md` · `legolas/notes/…g5a-gd-level12-opposition-ledger.md` ·
`gamora/notes/…g5b-sim-opposition-census.md`.

**No production code written. No telemetry written. No canonical doc amended.**

**Signed:** gandalf (`SPEC-AUTHOR` / `DRIFT-CRITIC`), 2026-07-28.
*v2 supersedes v1 in total. G-5 remains held on **HALT H-2** (P-1, P-2, P-3) and on **H-3**.*

---
---

# §10 — AMENDMENT — 2026-07-28 — THE THREE OWED SPEC AMENDMENTS

**▶ ROLE: SPEC-AUTHOR (DRIFT-CRITIC posture — amending predicates this seam authored).**
**Cell:** `WR1-SPEC-AMEND` of run `WR1-2026-07-28` (charter §8.3, conductor-claimed).
**Authorizing verdict:** `gandalf/notes/2026-07-28-kitcal1-g5-efficacy-verdict.md` **§A-8.3**
(*"Kit spec v2 cannot be quoted again until three amendments land: §6.3 gains a tier-weighting rule
and an explicit boss-tier window-membership clause (§7.3, unchanged); §6.2 S-2 is re-registered on an
instrument that is not a pinned residual; §6.2 S-1 gains its coincidence-floor clause. All three are
spec amendments, not re-grades."*)
**Cross-confirmed:** KC1 charter `…2026-07-27-kit-cal-1-run-charter.md` §14.28 (the coincidence floor,
reproduced at event level), §14.31/§14.33 (S-2's registered instrument proven unsatisfiable **by
construction**), §14.38 (terminal). **Enumeration is EXACTLY three; no fourth was found owed** (§10.4).

### §10.0 — The rule that governs reading §10

> **These are amendments to INSTRUMENTS, not re-grades of RESULTS.** Every band, every predicate and
> every grade in run `KC1-2026-07-27` stands exactly as pre-registered — including the three misses
> these repairs explain. §10 binds **forward only**: the first battery it governs is WR1's post-wave
> re-run, and it is pinned **BEFORE** that battery executes. *Repairing a predicate before results
> exist is preregistration; repairing it after they exist is goalpost-moving. The date on this section
> and the run-state it was written into are the whole of its legitimacy — check them.*
>
> **The general law KC1 taught, carried above all specifics** (verdict §A-8.3): *a fixture-side
> statistic does not keep its meaning when carried onto a designed battery. The fixture's window was
> composition-**sampled**; the sim's is composition-**designed**. Every statistic whose value depends
> on what varied — B, and every tier-weighted aggregate — degenerates across that join.*

---

## §10.1 — AMENDMENT 1 — §6.3 gains a tier-weighting rule and a boss-tier window-membership clause

**Authority:** verdict **§2.3** (*"A DEFECT IN MY OWN SPEC — the window's membership for the boss tier
was never pinned"*) + **§7.3** (*"Kit spec v2 §6.3 must gain a tier-weighting rule and an explicit
boss-tier window-membership clause before any band from it is quoted again"*), consolidated at §A-8.3.

**The defect.** On the fixture side W-c is unambiguous (`play_time ≥ 3619` inside R2 — a natural
49-engagement sequence that demonstrably contains the boss encounter). On the sim side there is no
natural sequence: there is a 4-tier battery with **equal seed counts**. §6.3 never said which tiers
constitute W-c. The report labelled the whole run `window_id: "W-c"` (boss **in**); the conductor's
dispatch framing read boss **out**. Both readings were defensible and the spec did not adjudicate.

**AMENDED RULE — R-A1. Sim-side window membership and cut arithmetic.** Any battery quoting a §6.3
band must report **two cuts, both, always**:

| Cut | Membership | Status |
|---|---|---|
| **CUT-1** | trash + champion + mixed_pack (packs only) | **MANDATORY** — the robustness cut |
| **CUT-2** | packs + boss **Arm A only** | **MANDATORY** — the like-for-like-with-fixture-W-c cut |
| **CUT-3** | all tiers, all arms | **ILLEGITIMATE. May be computed; may never be graded.** |

- **Arm B never enters an aggregate.** Arms A/B are *the same encounter under two door values*; Arm A
  is canonical (charter §14.26). Pooling both double-counts the boss to 40 % of the sample. CUT-3 is
  named illegitimate **in the spec** precisely because in KC1 it was the cut that most **flattered**
  N-4 — the most flattering cut must be disqualified by rule, not by the grader's restraint.
- **Weighting inside a cut is equal-seed unweighted pooling over encounters** — never a per-tier mean
  of means, never a fixture-frequency reweight. Stated so the arithmetic is not re-invented per lap.

**AMENDED RULE — R-A2. Three-state grading.** **PASS** only where *both* legitimate cuts pass;
**MISS** where *both* miss; **CUT-DEPENDENT** where they disagree. A **conservative binary**
(cut-dependent → MISS) must be reported alongside, and the verdict must state whether it changes under
either presentation. *(In KC1 the disagreements split one each way — N-1 passed on CUT-1 and missed on
CUT-2; N-3 and N-4 missed on CUT-1 and passed on CUT-2 — which is the evidence that the third state is
not a device for absorbing misses. It must not become one; if a future lap's cut-dependencies all fall
the same way, that asymmetry is itself a reportable finding.)*

**AMENDED RULE — R-A3. Weighting-free per-tier table is CO-EQUAL, not supplementary.** Because every
aggregate is weighting-contingent, each §6.3 band must be accompanied by its per-tier decomposition
(the verdict §3.1 table shape). Where the aggregate and the per-tier reads disagree in direction, the
**per-tier read is the durable evidence** and the verdict must say so.

**AMENDED RULE — R-A4. The boss-overweight caveat travels with every tail band.** CUT-2's boss is
~25 % of encounters against roughly **2–6 %** of the fixture's W-c engagements. CUT-2 therefore
**over**-weights the sim's heaviest tier. Any tail band (N-10, N-11, N-12) that misses **low** under
CUT-2 has missed robustly to the distortion that would most help it; any tail band that passes **only**
on CUT-2 must be reported as suspect for exactly that reason.

**Composition:** R-A1..R-A4 are additive to §6.3. **No band value, no band width and no fixture value
in §6.3 is changed by this amendment.**

---

## §10.2 — AMENDMENT 2 — §6.2 **S-1** gains its coincidence-floor clause · **THE A-FLOOR PREDICATE REPAIR**

**Authority:** verdict **§A-2** in full — §A-2.1 (the control's literal miss, conceded first), §A-2.2
(three pre-registered facts establishing instrument-not-sim), §A-2.3 (the A-lift with its unplanned
negative control), **§A-2.4** (*"§6.2's S-1 control predicate must gain a coincidence-floor clause…
plus `hits/press = 1.0` promoted from diagnostic to co-equal predicate"*). Event-level reproduction:
KC1 charter **§14.28** + Gate-2 `…-gate2-gamora-g5-s1control.md`.

**The defect, stated exactly.** S-1's control leg reads *"Single-target arm returns A ∈ [0.98, 1.05]."*
**That band assumed A's floor is 1.0.** It is not. Claws compile at `cooldown_seconds = 0.0` and the
sim has **no player attack-speed model**, so sequential *single-target* kills land inside one 0.5 s
`kill_event_bin_s`: one kill per 0.1 s tick, eight kills into three bins. `compute_abc` is not buggy.
**A's floor in this battery is 2.667 / 1.333 / 1.200 / 1.000 by tier** — a property of the *pinned kit
and the binning grain*, not of the geometry S-1 exists to test. The control therefore missed the band
**letter** at every pack tier while the signature the leg exists to establish **reproduced**: the
pre-registered second instrument read `hits/press = 1.0000` on every tier, every seed, max 1.0 across
150 fights — no press ever touched two bodies — and the A-step it exists to isolate read
**×1.50 / ×1.50 / ×1.25** over the floor, with a **×1.0000** boss-tier negative control.

### THE REPAIRED S-1 PREDICATE (binding on all future batteries)

> **S-1 — "the A-step exists" — REPAIRED PREDICATE, three legs, ALL THREE REQUIRED:**
>
> **Leg 1 — GEOMETRY NEUTRALIZATION (promoted: diagnostic → co-equal predicate).** The control arm
> must return **mean `len(targets_hit)` per player skill press = 1.000, and max = 1.0 over every fight
> in the arm.** This — not A — is what establishes that the control's multi-target geometry is
> neutralized. *(§6.2's closing note offered `hits/press` as a diagnostic because its **fixture**-side
> semantics are UNCERTAIN — `hitsInflicted` may or may not count DoT ticks. That uncertainty is
> **fixture-side only**; on the **sim** side `len(targets_hit)` is exact and unambiguous. The promotion
> is therefore of the SIM-SIDE instrument only; the fixture-side 2.362 hits/press comparison remains a
> diagnostic, exactly as originally written.)*
>
> **Leg 2 — THE COINCIDENCE-FLOOR CLAUSE.** *The control leg is graded against **the control's own
> measured A**, not against 1.0, whenever `cooldown_seconds = 0.0` on the compiled kit **or** no
> player attack-speed model is compiled.* Under that condition the control's per-tier A **IS** the
> floor, by definition; it is a measured constant of the battery, and **no band binds it.** The
> control's A must be **reported per tier** (it is the denominator of Leg 3) and it must be
> **verified degenerate** — mean = min = max across all seeds — or the floor is not a floor and S-1 is
> NOT-EVALUABLE.
>
> **Leg 3 — THE A-LIFT (this is the graded leg; it replaces the absolute-A test).** Grade
> **`A_lift = A_canonical ÷ A_control`, per tier, at matched seeds**, not `A_canonical` against a
> constant. **The arc arm passes iff `A_lift > 1.25` at the G-5a pack sizes, without needing density
> outside those pools.** *The **1.25 constant is transplanted verbatim from the pre-registered
> predicate** (§6.2 S-1: "arc arm returns A > 1.25 at G-5a pack sizes"). It is not a new threshold and
> it was not chosen with knowledge of any result — this repair moves the constant from the wrong
> denominator to the right one and changes nothing else. That is the entire claim to legitimacy here,
> and if the constant had been re-picked, the repair would be goalpost-moving.*
>
> **Leg 3b — THE NEGATIVE-CONTROL ORDERING CHECK (required report; ONE-SIDED, no magnitude band).**
> The battery must include at least one **spread** tier where the arc has nothing to catch
> (`hits/press` ≈ 1.0 on the canonical arm). On that tier, `A_lift` must read **strictly below the
> smallest pack-tier lift.** Ordering is what the signature claims — *the A-step appears where breadth
> appears and vanishes where breadth vanishes*. **No numeric band is set here, because none was
> pre-registered and inventing one now would be exactly the error Leg 3's constant avoids.** A
> violation of the ordering is a **NOT-REPRODUCED** verdict for S-1, not a tuning note.
>
> **Confound clause (required check, not an assumption).** Before any lift is quoted, the two arms
> must be shown **outcome-comparable at the tiers where the lift is measured** — matched win rate,
> matched DoT rows and HP, matched kill counts. Divergences confined to tiers *outside* the lift
> measurement do not invalidate it, but must be named. *(In KC1 all divergences were boss-tier; the
> three pack tiers delivered identical DoT and 30/30 wins in both arms.)*
>
> **Honorable-fallback routing (UNCHANGED from §6.2 as pre-registered):** **(ii) sim-mechanics
> divergence** if the arc arm fails at plausible density; **(iv) mechanism-class absence** if it fails
> *because* A3 (no target cap) or A2 (90° cone) is the proximate cause — which the grading lap must
> **state, not infer.**

**What the repaired predicate grades that the old one could not.** The old predicate graded a
**band letter on an absolute statistic whose floor was a battery artifact**. The repaired predicate
grades the **SIGNATURE**: geometry provably neutralized (Leg 1), floor measured rather than assumed
(Leg 2), the step isolated as a ratio over that floor (Leg 3), and the step shown to *disappear where
its mechanism disappears* (Leg 3b). Applied to KC1's banked numbers it returns **REPRODUCED** — which
is the verdict §A-2.4 already reached on the evidence, now reachable by the instrument itself.

### Preregistration pin — and one correction to this cell's dispatch

**Pinned 2026-07-28, BEFORE the WR1 post-wave battery executes.** WR1 charter §4 sequences
*"extraction + specs in parallel … → mechanism builds M-1..M-9 … → full battery re-run (same seeds
74000800×30, sequential) → gates G-A/G-B graded."* This section lands in the specs phase; no post-wave
number exists. The repair is preregistration.

> **⚠ CORRECTION, filed rather than smoothed.** The dispatch that commissioned this cell stated that
> the repaired A-floor predicate *"is what gate G-A of run WR1 will be graded with."* **It is not.**
> WR1 charter §2 defines **G-A** as the **S-3** gate (*normalized fall ÷ EHP ratio reads 2.12-class,
> not 1.000*) — the S-1 repair does not touch it. What the repaired predicate governs is the
> **S-1 structural re-read** on WR1's post-wave battery (and every battery after). The
> preregistration requirement the dispatch was protecting is **satisfied either way** — the repair is
> pinned pre-results — but the gate letter is wrong and a predicate repair filed under the wrong gate
> is exactly the kind of drift this cell exists to prevent. *Naming it costs nothing; leaving it would
> have put a mis-addressed instrument into the WR1 grading lap.*

---

## §10.3 — AMENDMENT 3 — §6.2 **S-2** is re-registered off the pinned residual

**Authority:** verdict **§A-3** — §A-3.1 (*"the predicate is not merely unsatisfiable — it is also
unfalsifiable, and the second half is worse"*), §A-3.2 (the lever measured live), **§A-3.3**
(*"S-2 must be re-registered on the kill-time-delta instrument with a band set from **fixture** data,
before KIT-CAL-2 runs"*). Cross-confirmed: KC1 charter §14.31/§14.33 (Gate-2's six-order-of-magnitude
sweep proving leg (a) **unsatisfiable by construction**), §14.38.

**The defect, both legs.**
- **Leg (a) — *"lifts B by ≥ 1.10×"* — UNSATISFIABLE BY CONSTRUCTION.** B held flat at 1.0000 on three
  of four tiers across **six orders of magnitude** of DoT magnitude. B is a ratio-decomposition
  statistic; the battery's design **pins its product**, so B cannot move for any intervention that
  does not change what the design pinned. A predicate no intervention can satisfy is not strict — it
  is null.
- **Leg (b) — *"with A and C each within their bootstrap CI of the no-DoT arm"* — UNFALSIFIABLE, and
  worse.** It is satisfied *by the same degeneracy* that kills leg (a): where the statistics cannot
  move, they are trivially "unchanged." A predicate whose failure condition cannot occur passes
  vacuously and certifies nothing.

**AMENDED RULE — R-A5. S-2 is UNGRADEABLE on the §6.2 instrument. It may not be scored, and its
absence may not be counted against the sim.** Any battery reading §6.2 as-written must record S-2 as
**INSTRUMENT-VOID** — *not reproduced* for §6.0's arithmetic (an instrument defect of the grader's own
must never buy the run a better verdict), and *not absent* for the honorable-fallback decomposition
(the sim was never validly asked; grading it a sim inadequacy converts the **grader's** instrument
defect into the **builder's** calibration verdict — the error R-KC1-23 already refused once).

**AMENDED RULE — R-A6. The replacement instrument, registered by SHAPE now and by NUMBER before the
next battery.** S-2's claim is re-expressed on **paired kill-time delta** — DoT-arm vs no-DoT-arm
median kill time at matched seeds, per tier — with **DoT share of delivered damage** as its co-reported
second instrument. Both are **product-independent**: neither is a component of a ratio the battery
design pins.

> **BLOCKING PRECONDITION (R-A7).** The band for the kill-time-delta instrument **must be MEASURED
> from `fixtures.db` (the W-c → R3 like-for-like cut) before the battery that grades it runs.** Until
> that fixture measurement lands, **S-2 remains UNGRADEABLE and must be reported as such.** Explicitly
> and by name: KC1's measured values — kill-time ratio **×0.9160** (8.40 % cut, 60/60 paired) and DoT
> share **1.295 % → 6.215 %** (×4.80) — **are NOT the band and must never be promoted into one.** They
> were measured after the registered predicate was found null, in full knowledge of the result any
> threshold would have to admit. *A threshold authored after the measurement is not a threshold, it is
> a description wearing a predicate's costume.* They may be quoted as **prior-lap magnitudes for
> sizing the fixture-side cut** — never as goalposts.

**AMENDED RULE — R-A8. The general instrument-selection law, carried into §6.2 permanently.**
*A ratio-decomposition statistic whose product is pinned by battery design carries **zero** information
about any intervention that does not change the product.* Before any future structural target is
registered on a decomposition component (A, B, C or any successor), the spec must state **what the
battery design holds fixed** and demonstrate that the candidate statistic is free to move under the
intervention it is meant to detect. **Two of this spec's twelve bands and one of its three signatures
were defective for that single reason, and it was foreseeable.**

**Honorable-fallback routing** for the re-registered S-2 is otherwise **unchanged** from §6.2 as
pre-registered: **(ii)** if the lift fails to appear; **(iii) fixture-measurement error** if the
segmentation is implicated.

---

## §10.4 — WHY THERE IS NO FOURTH AMENDMENT (S-3, and the enumeration check)

The enumeration was tested against the possibility of a fourth, because verdict **§A-4.2** records
that **both of S-3's acceptance legs are VACUOUS** — the ≥10 %-EHP drop count was 0 on the *pre*-step
side too, and the p99 worst-drop was already inside the "< 12 % post-step" target before the step. Any
step at all, including no step, would have passed both legs. That is a real instrument defect of the
same family as §10.2 and §10.3.

**It is nonetheless NOT a fourth owed amendment, for two reasons, both external to this cell:**

1. **§A-8.3 enumerates exactly three**, and it is the terminal consolidation. §A-4 files no
   "owed to the spec" line — because S-3's *substantive* verdict did not depend on its legs. The
   predicate **pre-committed its own failure attribution** (honorable-fallback column: *"(iv) if it
   survives because player defence cannot be pinned"* — BQ-3, named before results), and §A-4.3
   graded it **NOT REPRODUCED** on a discriminating statistic despite a clean letter sweep.
2. **The repair already exists upstream, in a live charter.** WR1 charter §2 defines **G-A** as
   *"normalized fall ÷ EHP ratio reads 2.12-class (fixture), not 1.000 (pure scale)"* — precisely the
   discriminating instrument §A-4.3 used, and precisely what S-3's vacuous legs could not test.
   **G-A supersedes S-3's acceptance legs for the WR1 battery.** Duplicating it here would fork the
   instrument across two documents.

> **Recorded for the KIT-CAL-2 spec, not executed here:** when §6.2 is next redrafted, S-3's legs
> should be replaced by the G-A form (**normalized fall ÷ EHP pool ratio**, banded from fixture), and
> every acceptance leg in §6.2 should be checked for **pre-step satisfaction** — the vacuity test
> §A-4.2 discovered. That is a redraft item under the next run's charter, **not** one of the three
> amendments KC1 ruled owed, and it is filed here so it is not lost.

---

## §10.5 — PROVENANCE + STATUS

- **Every fixture value, band, predicate and grade in §§0–9 is UNCHANGED.** §10 adds rules and marks
  two §6.2 rows and one §6.3 block as not-quotable-as-written. Nothing was silently rewritten; the
  three inline banners (header, §6.2, §6.3) point here and alter no ruled text.
- **No number was computed in this cell.** Every figure quoted above is transcribed from the KC1
  terminal verdict (`…-kitcal1-g5-efficacy-verdict.md` §2.3, §3, §3.1, §A-2, §A-3, §A-4, §A-8.3) or
  from the KC1 charter §14.28 / §14.31 / §14.33 / §14.38. **No fixture value was recomputed** —
  recomputing goalposts at amendment time is the same failure as recomputing them at grading time.
- **Sources read:** KC1 terminal verdict (full) · KC1 run charter §14.x (amendment/predicate rulings)
  · WR1 charter `…-2026-07-28-wr1-wave-relay-run-charter.md` §2 (gates), §4 (sequencing), §8.3 (cell
  claim). **No production code, no engine-repo write, no canonical doc amended.**
- **Status of the spec after §10:** **QUOTABLE AGAIN**, under §10's rules, for batteries executed
  after 2026-07-28. **S-2 remains UNGRADEABLE until R-A7's fixture-side band lands.**
- **Veto-open.** Per the KC1/WR1 ledger convention, every rule above is open to Matt's veto; the
  §10.2 dispatch correction (G-A ≠ S-1) is carried to the conductor explicitly.

**Signed:** gandalf (`SPEC-AUTHOR` / `DRIFT-CRITIC`), cell `WR1-SPEC-AMEND`, 2026-07-28.
