# KIT-CAL-1 — sustain decomposition of the client's `Life healed` — 2026-07-28

**Mode:** A (analytical / primary-source probe)
**Run:** KC1-2026-07-27 · **Conductor:** gandalf · **Agent:** legolas (UNKNOWN-RESEARCHER)
**Trigger:** Matt's challenge — *"Life healed ~5,649 is healing the sim werewolf won't have; that
deficit is too large for a faithful G-5 unless part of it is natural regen that CAN be carried in."*
**Access:** read-only. Parsed save (own G-7/U-1 work), Edition-II corpus, galadriel's T-A/T-B ledgers.

---

## SUMMARY

**The 5,649 is not a Battle Surge deficit, and it is not a healing-throughput measurement at all.**

Four findings carry the ruling:

1. **`Life healed` is clamped — overheal is not counted, and respawn refill is not counted.** Proven
   three ways (§1). The counter therefore measures **cumulative post-mitigation damage taken and
   recovered from**, not the kit's healing capacity. Lifetime total ÷ `hitsReceived` = **24.94 HP per
   hit**, landing exactly on the G-5a ledger's post-mitigation trash damage. It is a damage-intake
   statistic wearing a healing statistic's name.
2. **≈52 % of the 5,649 accrues out of or beside combat** — 21.6 % strictly (>5 s from any
   engagement), a further 30.8 % within ±5 s. That is **Constitution**, a live mechanic in this
   edition, measured at a hard ceiling of **26.4 % of max health per second** against the corpus's
   `acceleratedLifeRegenPercent = 25.0`. A fight-scoped sim that starts fights at full HP already
   accounts for this. It is not a deficit.
3. **The kit has life leech, and nobody has been counting it.** Ring-1 prefix *Vampiric*,
   `offensiveLifeLeechMin = 5.0` (jitter 35 % → **3.25–6.75 % ADCTH**), firing on all **1,606**
   hits inflicted. Its healing *capacity* (~16,000 HP) exceeds the entire run's realised healing.
   The in-fight healing is clamp-limited, not source-limited — and leech, not Battle Surge, is the
   term most likely capturing the clamp.
4. **Battle Surge's ceiling is 2,883 HP (51 %) and its realistic contribution is ≈1,500 HP (≈27 %).**
   The binding constraint is not the 66 crits — it is that **69.1 % of in-engagement frames are at
   full health** and only **3.7 %** carry a deficit as large as one proc. Battle Surge overheals on
   most procs, and overheal is not counted.

**And the stat contradiction dissolves.** `lastHitBy` (273.70) is not damage — it is the **Offensive
Ability of the last monster that attacked**, matching Plague Walker's ledger OA of **274** to 0.3.
`lastHit` (312.89) is the last target's **Defensive Ability**. No contradiction with
`greatestDamageReceived`, which survives as a clean **post-mitigation single-event bound of 260.50 HP**
for the entire run — boss included. §14.10 gets a client-side ceiling.

---

## 0. Provenance of the number, and a correction to its timestamp

`Life healed` is **not** in the `.gdc` `play_stats` block (my G-7 parse enumerates all 31 fields;
none is a heal counter) and **not** in the character-sheet Records panel. The Records panel's full
tag family in the merged 20,394-tag `Text_EN` corpus is exactly six entries —
`tagRecordTime` · `tagRecordDeath` · `tagRecordMonsterKills` · `tagRecordChampionKills` ·
`tagRecordHighestDamage` · `tagRecordHighestDamageTaken` (+ `tagRecordHighestMonster`). **No
`Life healed` tag exists anywhere in the corpus.**

→ **`Life healed` is a `game.PlayStats` dev-console field with an English-hardcoded label**, engine-
internal, unlocalised. Confidence **HIGH** (exhaustive negative search across 8 merged `Text_EN.arc`).

**Exact value, from galadriel's T-A 2 fps ledger** (`ta-full-2fps-gated.csv`, 13,633 samples):

| `play_time` | `pts_s` | `life_healed` | note |
|---|---|---|---|
| 3156 | 2837.0 | **3,446.85** | `deaths` 0 → 1 |
| **5453** | **5151.5** | **5,649.87** | `deaths` 1 → **2** — this is frame 281 |
| 7088 | 6816.0 | **12,468.06** | end of run |

Frame 281 is **the death-2 frame**. The 5,649.87 is the lifetime total at the instant of the second
death, not a mid-run sample. Anything reasoning from it is reasoning from a death boundary.

---

## 1. Q1 — WHAT `Life healed` INCLUDES

### 1.1 It counts only HP actually restored. Overheal is NOT counted. Confidence **HIGH**.

Three independent proofs:

**(a) Dead-flat plateaus while alive and fighting.** Of 12,286 consecutive 0.5 s sample pairs,
**11,228 (91.4 %) show exactly zero change**; 1,058 are positive; **zero are negative**. In the
`play_time` 2400–2699 bucket the counter moves **+1.62 HP over 299 s** across 13 kills. Passive regen
never stops running — so if overheal counted, that bucket could not be flat.

**(b) Respawn refill is not counted.** At death 1 the counter takes its last increment (+0.45) on the
death sample and then reads **3,446.85 for 28 consecutive samples** through the entire death/respawn
sequence. The respawn HP grant does not register.

**(c) The arithmetic closes against an independent ledger.**
`12,468.06 / hitsReceived 500 = ` **24.94 HP per hit received.** The G-5a level-12 opposition ledger
gives Act-1 trash at **33–52 damage/hit pre-mitigation** against **3–10 armor**. A clamped counter
must yield mean post-mitigation damage per hit; an unclamped one is unbounded. It yields 24.94.

### 1.2 Source-by-source inclusion

| Source | Included? | Evidence | Confidence |
|---|---|---|---|
| Passive health regeneration | **YES** | The clockwork family — 86 s of dead-constant +0.805 HP / 0.5 s (`play_time` 3070–3156, cv 0.136 over 112 samples), running while HP falls toward death 1 | HIGH |
| **Constitution** (out-of-combat fast regen) | **YES** | The fast OOC family, ceiling 26.4 % maxHP/s (§2.2) | HIGH |
| Skill heals (Battle Surge) | **YES** (structurally; not isolable) | Same buff channel as any % maxHP/s restore; no exclusion mechanism exists | MEDIUM-HIGH |
| Life leech / ADCTH | **YES** (structurally; not isolable) | Same; and the in-combat rate (5.09 HP/s mean, §2.1) cannot be produced by regen alone | MEDIUM-HIGH |
| Health potions | untestable here | `healthPotionsUsed = 0` — Matt's deliberate control | — |
| Death/respawn refill | **NO** | §1.1(b) | HIGH |
| Overheal | **NO** | §1.1(a)(c) | HIGH |

**Cheapest empirical test for the two MEDIUM-HIGH rows** (if the ruling needs them upgraded): a
2-minute L0 world-monster trial. `game.PlayStats` before → unequip the *Vampiric* ring → fight one
zombie to a known HP deficit → `game.PlayStats` after; repeat with the ring on. The delta isolates
ADCTH's contribution to the counter directly. Same rig with Battle Surge unallocated isolates the
on-crit term. Both are single-fight, single-variable, and use the rig gandalf already has.

### 1.3 The framing that answers the challenge

Because the counter is clamped, **`Life healed` is not a measure of healing throughput. It is a
measure of damage absorbed and recovered from.** 5,649 HP by `play_time` 5453 means the character
took ≈5,649 HP of post-mitigation damage over 90:53 and got it back. Asking "can the sim reproduce
5,649 HP of healing" is the wrong question; the right one is "does the sim's werewolf recover from a
comparable damage intake" — and 52 % of that recovery happens between fights, where a fight-scoped
sim gets it for free.

---

## 2. THE MEASURED DECOMPOSITION

Method: galadriel's T-A 2 fps `life_healed` series differenced pair-wise (gaps ≤1.01 s only, 94.1 %
coverage of the accrual to `play_time` 5453), classified against her T-B engagement windows
(106 kill-clustered engagements, `gap_threshold_s = 5.0`, covering 880 of 882 kills).

### 2.1 By combat state — to `play_time` 5453 (covered accrual **5,300.9 HP**)

| class | HP | share | seconds | share of time | **HP/s** |
|---|---|---|---|---|---|
| **IN** — inside a kill-engagement window | **2,520.7** | **47.6 %** | 495.0 | 10.1 % | **5.09** |
| **PAD5** — within ±5 s of one | **1,634.3** | **30.8 %** | 691.0 | 14.1 % | **2.37** |
| **OUT** — >5 s from any engagement | **1,145.9** | **21.6 %** | 3,728.0 | 75.9 % | **0.31** |

(Full run, for reference: IN 4,470.8 / PAD5 3,961.7 / OUT 3,015.3 — same shape.)
The 332.6 HP of OCR-uncovered accrual pro-rates across the three buckets without moving the shares.

**Read:** 47.6 % of the number is in-fight. 52.4 % is out-of-fight or peri-fight recovery.

### 2.2 By rate class — Constitution isolated

Classifying each sample against `0.08 × maxHP/s` (the Battle Surge floor rate), with `maxHP` stepped
from galadriel's G-2c plateau table (366 / 443 / 451 / 471 / 491 / 672 / 707 / 747 / 759 / 1600):

| class (to `play_time` 5453) | HP | seconds | mean HP/s |
|---|---|---|---|
| FAST (≥8 % maxHP/s), in-combat (±3 s) | 2,223.2 | 32.5 | 68.4 |
| SLOW, in-combat | 1,557.0 | 250.5 | 6.2 |
| **FAST, out-of-combat** | **1,161.9** | 13.0 | **89.4** |
| SLOW, out-of-combat | 358.8 | 107.5 | 3.3 |

**The out-of-combat fast family saturates at a hard ceiling.** Nine independent samples read
**98.45 HP per 0.5 s against `maxHP` 747** — i.e. **26.4 % of max health per second** — and the
R3 samples at `maxHP` 1600 top out at 23.5 %. p90 across all 70 OOC samples above 20 HP/s = **0.264**.

Corpus: `records/creatures/pc/malepc01.dbr` carries **`acceleratedLifeRegenPercent = 25.0`** and
**`characterConstitution = 300.0`**, identically across all four `.arz` layers. The measured 26.4 %
is that constant plus the passive floor riding on it. **Constitution identified, MEASURED, closed.**

Mechanics, verbatim from `Text_EN` (`tagTutorialTip45Text{A,B,C,D}`, `tagQuickTip45`, `tagQuickTip46`):
out-of-combat only; drains a finite pool; **refills on level-up, on death, and on Food Ration /
Untouched Meal pickups**; when exhausted, fast OOC regen stops. `records/game/gameengine.dbr` sets
`combatIdleTime = 1.2` — the out-of-combat threshold.

*(This also explains the run's rate structure: the fast family clusters immediately after level-ups
and the two deaths, exactly where Constitution refills.)*

---

## 3. Q2 — PASSIVE HEALTH REGEN AT END-STATE, FROM SOURCE

**Base:** `records/creatures/pc/malepc01.dbr` → **`characterLifeRegen = 1.0`** HP/s. Flat.
`records/creatures/pc/playerlevels.dbr` carries `lifeIncrement`, `manaIncrement`, attribute
increments — **no regen increment**. `records/game/combatformulas.dbr` carries no life-regen equation.
Regen is a flat engine-side sum, not derived from any attribute.

**All 12 equipped records scanned** (base + prefix + suffix + component + augment on each) for the
`characterLifeRegen*` family. **Exactly one hit in the whole kit:**

| slot | item | affix record | regen field |
|---|---|---|---|
| head | Helmet | `suffix/b_ar014_arje.dbr` — **"of the Dranghoul"** | **`characterLifeRegenModifier = 10.0`** (`lootRandomizerJitter = 28.0` → rolled **7.2 – 12.8 %**) |

**Corrections to genre memory — both checked, both wrong if assumed:**

- **Torso "of Menhir's Wall"** (`suffix/b_ar002_ar.dbr`) — `characterLife = 100.0`,
  `characterDefensiveAbility = 12.0`, `defensiveBleeding = 10.0`, `defensiveProtectionModifier = 4.0`.
  **No regen.** Menhir's Wall is a flat-health/DA suffix in this edition, not a regen suffix.
- **Belt "of Soulwarding"** (`gdx1 suffix/b_ar103_ar_a.dbr`) — `characterLife = 80.0`,
  `defensiveAether = 10.0`, `offensiveLifeModifier = 14.0`, `offensivePhysicalModifier = 12.0`,
  `augmentSkillLevel1 = 2`. **No regen, no leech.** `offensiveLife` is *vitality damage*, not lifesteal
  — a live trap in the field-name schema.
- Feet "Vigorous" (`prefix/aa007a_lifemod_01.dbr`) = `characterLifeModifier = 5.0` — max health, not regen.
- No components, no augments, no relic, no medal equipped. **Zero devotion allocated**
  (`devotionPointsUnspent = 3` == `totalDevotionUnlocked = 3` — Matt's control holds).

**Skill-side regen — all four allocated nodes resolved, all negative:**

| record | class | regen? | what it actually grants |
|---|---|---|---|
| `werewolf1.dbr` (transform, 16/16) | `Skill_Shapeshift` | **NO** — `characterLifeRegenModifier = 0.0`, and the record has **no** `characterLifeRegen` field at all | mesh/anim/FX replacement + `grantedSkills` only; **every** stat field is 0.0 |
| `amatokpact1_buff.dbr` (the cold aura, 1/12) | `SkillBuff_Passive` | **NO** | DA +20, `defensiveProtection` 16, cold 5–6, `characterManaLimitReserve` 50 |
| `onslaught1.dbr` (13/16) | `Skill_WeaponPool_BasicAttack` | **NO** | cold min, `weaponDamagePct`, combo charge |
| `werewolf1b.dbr` — Blight of Ch'thon (1/1) | `Skill_Transmuter` | **NO** | 100 % Pierce → Chaos |
| `_classtraining_class10.dbr` (Berserker bar, 5) | `Skill_Mastery` | **NO** | str/dex/int/life/mana tables only |

**U-1's "the transform grants zero stats" is VERIFIED with no regen exception.**

### Computed end-state passive regen

**1.0 × (1 + 0.10) = 1.10 HP/s** (band **1.07 – 1.13** across the affix's 28 % jitter).

### One honest residual — flagged, not papered over

The measured clockwork floor at level 7–8 is **1.61 HP/s** (0.805 HP per 0.5 s, cv 0.136 over 112
consecutive samples, `play_time` 3070–3156). That **exceeds** the 1.10 the source predicts by
≈0.5 HP/s. The floor also *rises with level* (0.46 @ L2 · 0.62 @ L3 · 1.00 @ L5 · 1.62 @ L7–8 ·
2.54 @ L8-late · 2.90 @ L9 · 3.23 @ L11) — and at L2 it sits *below* the flat base of 1.0, which no
"base + %" reading can produce.

**I could not resolve the scaling law from the corpus.** Candidates not eliminated: a per-level regen
term held outside `playerlevels.dbr`; a difficulty-side adjustment (`character_info.difficulty = 128`,
`records/game/balancingadjustment_mp+difficulty_players01.dbr` not yet decompiled against it); or the
clockwork family being a slow Constitution trickle rather than passive regen. **Graded UNRESOLVED.**
It does not move the decomposition — even at 1.61 HP/s the always-on floor is ≤3.6 % of the 5,649 in
strictly-in-combat time — but it should not be carried forward as settled.

---

## 4. Q3 — BOUNDING BATTLE SURGE

**Source, verbatim.** `records/skills/playerclass10/passive02.dbr`, `Skill_PassiveOnCritBuffSelf`,
`skillDisplayName = tagGDX3…` → **"Battle Surge"**, `skillMaxLevel = 12` (matches G-6's "1/12 square").

| field | rank 1 | meaning |
|---|---|---|
| `onHitActivationChance` | **100.0** | every crit procs it |
| `skillCooldownTime` | **6.0 s** | ICD |
| `skillActiveDuration` | **3.0 s** | buff length |
| `skillLifePercentBuffDuration` | **8.0** | rendered by `tagBonusLifePercentBuff` = *"Restores {%.0f0}% Health Per Second"* |

**The commission's stated parameters are CONFIRMED from source**: 8 % max health **per second** for
3 s = **24 % maxHP per proc**, 100 % on crit, 6 s ICD. (`characterManaRegen` is also granted — energy,
not health.)

### The bounds

| bound | value | reasoning |
|---|---|---|
| procs, lifetime | **≤ 66** | `criticalHitsInflicted = 66`; 100 % proc chance, 6 s ICD ⇒ procs ≤ crits |
| procs by `play_time` 5453 | **≈ 49** | pro-rated on kills (655 / 882 = 74 %) |
| naïve ceiling | 49 × 0.24 × 747 = **8,780 HP** | **not binding** — exceeds the number being explained |
| **measured ceiling** | **2,882.7 HP (51.0 %)** | Σ min(Δ, 0.08·maxHP·Δt) over every in-combat sample to 5453. Requires Battle Surge active in *every* in-combat healing sample — impossible at 3 s / 6 s duty cycle. A genuine over-estimate. |
| **the real constraint — the clamp** | | Across 9,004 in-engagement frames at 15 fps: **69.1 % are at full health**; median deficit **0 HP**; p75 **10 HP**; p90 **70 HP** — against a proc size of **161 HP** (24 % of 672). **Only 3.7 % of in-combat frames carry a deficit as large as one proc.** |

**Plausible band: 700 – 2,880 HP. Point estimate ≈ 1,500 HP ≈ 27 % of the 5,649**
(≈49 procs × ≈30 HP realised per proc, the rest overhealed and uncounted).

**Battle Surge is a burst-heal on a kit that spends most of its combat time at full health.** Its
measured contribution is bounded by the deficit available to it, not by its own throughput.

---

## 5. Q4 — LIFE LEECH IN THE KIT: **YES**

| source | record | field | value |
|---|---|---|---|
| **Ring 1 prefix "Vampiric"** | `records/items/lootaffixes/prefix/ao008a_lifeleech_01.dbr` | **`offensiveLifeLeechMin = 5.0`** | `lootRandomizerJitter = 35.0` → rolled **3.25 – 6.75 %** |

Rendered by `DamageLifeLeech` = *"{%t0}% **of Attack Damage converted to Health**"* — this is ADCTH,
not the `offensiveSlowLifeLeach*` DoT family. (The record's `FileDescription = "3%"` is a stale
designer label; the live value is 5.0.)

**Nothing else leeches.** No `offensiveLifeLeech*` on any other of the 12 records, none on the
transform, the aura, Onslaught, Feral Claws or Rip and Tear. G-6's F-G6-2 already established
`werewolf2` — the node that carries *"a bleed DoT, a life-leech and a crit-damage bonus"* — is
**absent**. This ring is the kit's only lifesteal.

**Why this matters more than its size suggests.** ADCTH fires on **all 1,606 hits inflicted**. At
~5 % of a per-hit damage in the 150–300 range it carries **≈12,000–24,000 HP of healing capacity** —
more than the entire run's realised healing. **The in-fight healing is clamp-limited, not
source-limited.** And leech, firing ~24× more often than Battle Surge, arrives first at most of the
deficit each incoming hit creates.

> **This is the finding gamora most needs.** If the sim models ADCTH, the in-fight half of the 5,649
> is largely representable *today* and the BQ-4 deficit collapses to the Battle Surge share alone.

---

## 6. Q5 — THE `lastHitBy` / `greatestDamageReceived` "CONTRADICTION": DISSOLVED

**`lastHit` and `lastHitBy` are not damage.** They are the **Defensive Ability of the last monster
attacked** and the **Offensive Ability of the last monster that attacked** — the operands of the
character sheet's hit-chance lines.

**Evidence, four strands:**

1. **UI structure.** `records/ui/character/characterinfotab1/charinfo_statsdarollover.dbr`:
   Line1 `tagCharStatsDA` "Defensive Ability" → Line2 `tagCharStatsDALast` **"Last Attacked By:"** →
   Line3 `tagCharStatsDAHit` "Chance to be Hit:" → Line4 "Chance to be Crit:". Lines 3–4 are computed
   by `combatformulas.dbr .probabilityToHitEquation(offensiveAbilityDV, defensiveAbilityDV)` — so the
   panel *must* carry the attacker's OA. `charinfo_statsoarollover.dbr` is the mirror image.
2. **Save-block adjacency.** `play_stats` pairs `lastHit` / `lastHitBy` with `lastMonsterHit` /
   `lastMonsterHitBy` = `tagEnemyZombieSoldierA01` (**Rotting Soldier**) / `tagEnemyZombieG01`
   (**Plague Walker**).
3. **The decisive number.** G-5a ledger §2: **Plague Walker** (`zombie_g01`) at `charL` 12 —
   **OA = 274**, **damage/hit = 37–45**. The save reads **`lastHitBy = 273.7040`**. A match to 0.3 on
   OA; and a **6.7× impossibility** as damage, with `criticalHitsReceived = 0` ruling out any crit
   multiplier. *A Plague Walker cannot deal 273.70 damage.*
4. **Corroboration.** **Rotting Soldier** (`zombie_soldiera01`, `charLevel = charLevel*1+1`) — ledger
   DA = 329 @ `charL` 13; the same equation at `charL` 12 gives **≈313**. Save reads
   **`lastHit = 312.888`**.

**Confidence HIGH.** Strand 3 alone is decisive.

### The bonus: two M-grade opposition values, and a §14.10 ceiling

**These fields are now assets, not noise.** They are **directly measured, save-resident (M-grade)**
opposition values at the run's end-state:

| field | value | is | validates |
|---|---|---|---|
| `lastHitBy` | **273.704** | Plague Walker **OA**, `charL` 12 | G-5a's D-grade OA derivation to **0.11 %** |
| `lastHit` | **312.888** | Rotting Soldier **DA**, `charL` 12 | G-5a's D-grade DA derivation to **≈0.03 %** (one spawn-level assumption) |

**`greatestDamageReceived = 260.4977`** now stands alone as the damage-receipt field —
`tagRecordHighestDamageTaken` / *"Most damage your character has ever received at one time."*

**It is post-mitigation.** Confidence **MEDIUM-HIGH**: galadriel's 15 fps globe series contains a
**single-frame (67 ms) drop of 304 HP** at `pts` 5504. A pre-mitigation maximum cannot be exceeded by
a post-mitigation observation, so 260.50 must be post-mitigation, and the 304 is two hits inside one
frame pair (multi-attacker melee at 0.77 hits/s across engagements makes this ordinary).

> **§14.10 bound, client-side.** Across the whole run — Act 1, Normal, 1 player, levels 1–13,
> **7 champion kills, 3 hero kills, and the boss `tagSlithBossB02` (Primordian, the Forgotten One,
> level 13, life+mana 15,822)** — **no single damage event exceeded 260.50 HP post-mitigation**,
> against pools of 366 – 759. That is **≤ 34.9 %** of the largest pool.
>
> **The deaths were compounding, not one-shots.** The death-2 window's `drop_max` is **541 HP** over a
> 3 s window — ≥3 hits — against a 747 pool.

**Caveat to carry:** it is not established whether `greatestDamageReceived` is updated by
damage-over-time ticks. If DoTs register per tick the bound is still per-event; if excluded it covers
direct hits only. Not resolvable from the corpus; resolvable by one L0 trial against a bleeding
enemy.

---

## 7. THE DECOMPOSITION TABLE

**Target: `Life healed` = 5,649.87 at `play_time` 5453 (frame 281, the death-2 frame).**

| # | Source | HP estimate / band | share | in-combat? | Sim-representable **today**? |
|---|---|---|---|---|---|
| 1 | **Constitution — strictly out of combat** (>5 s from any engagement) | **1,146** (measured, 21.6 % of covered accrual) | 20 % | **OUT** | **Implicitly YES** — a fight-scoped sim starting fights at full HP already grants this. Not a deficit. |
| 2 | **Constitution — peri-combat rapid refill** (±5 s of an engagement; 26.4 % maxHP/s ceiling) | **1,634** (measured) | 29 % | **OUT** (post-fight) | **Implicitly YES** — same. Not a deficit. |
| 3 | **Passive health regen**, 1.10 HP/s computed (1.61 measured, §3 residual) | **≤ 400** in-combat; ≤ 800 with the measured floor | ≤ 7 % | **BOTH** | **YES** — flat HP/s, standard |
| 4 | **ADCTH leech** — *Vampiric* ring, 3.25–6.75 %, on 1,606 hits | **900 – 1,800** (residual after 3 and 5, within the 2,521 in-fight total) | 16 – 32 % | **IN** | **RULING NEEDED** — YES if the sim models ADCTH; BQ-4 if not. **The pivotal question.** |
| 5 | **Battle Surge** — 8 % maxHP/s × 3 s, ≤49 procs, clamp-limited | **700 – 2,880**, point **≈1,500** | 12 – 51 %, **point 27 %** | **IN** | **NO — BQ-4** (gandalf's ruling; gamora P-6) |
| 6 | Health potions | **0** | 0 % | — | n/a (Matt's control) |
| 7 | Devotion, transform, aura, Onslaught, claws, charge | **0** — corpus-verified, all zero | 0 % | — | n/a |
| — | *OCR-uncovered accrual* | *333 (5.9 %), pro-rates across 1–5* | — | — | — |

**Roll-up against Matt's challenge:**

| bucket | HP | share |
|---|---|---|
| **Out-of-fight recovery** (rows 1 + 2) — sim gets it free | **≈2,780** | **52 %** |
| **In-fight, representable today** (row 3 + row 4 *if ADCTH is modelled*) | **≈1,300 – 2,200** | **23 – 39 %** |
| **In-fight, genuinely absent** (row 5, Battle Surge) | **≈1,500** (band 700 – 2,880) | **27 %** (band 12 – 51 %) |

---

## 8. WHAT THIS MEANS FOR THE G-5 FIDELITY RULING

*(Reported as inference, kept separate from the evidence above. The ruling is gandalf's and Matt's.)*

1. **The premise of the challenge does not hold as stated.** The 5,649 is not healing the sim werewolf
   won't have. **At most 51 %, and realistically ~27 %, is Battle Surge.** The majority is out-of-fight
   recovery that a fight-scoped sim already reproduces by construction.
2. **The number is a damage-intake statistic.** Clamped, it equals post-mitigation damage taken and
   survived. The fidelity question is not "can the sim heal 5,649" but "does the sim's werewolf absorb
   a comparable intake" — and `24.94 HP per hit received` is the calibration target that actually
   falls out of it, not 5,649.
3. **The load-bearing open item is ADCTH, not Battle Surge.** A 5 % lifesteal ring firing on 1,606 hits
   has more healing capacity than the entire run realised. If the sim models ADCTH, the in-fight
   deficit is ~27 % of the number. If it does not, the sim is missing the *larger* of the two in-fight
   sources — and nobody has been tracking it. **Route to gamora.**
4. **Two cheap experiments would close the remaining bands** (§1.2): one L0 trial with the *Vampiric*
   ring unequipped isolates ADCTH's share of the counter; one with Battle Surge unallocated isolates
   the on-crit share. Single-variable, single-fight, on the rig that already exists.

---

## 9. KNOWLEDGE GAPS NOT RESOLVED

| gap | status | cheapest next step |
|---|---|---|
| The passive-regen scaling law (§3 residual: 1.61 measured vs 1.10 computed; floor rises with level and sits *below* base at L2) | **UNRESOLVED** | Read `Health Regeneration` directly off a character-sheet screenshot at a known level — galadriel's `gd-gp-calib-c2-sheet` rig already crops that panel |
| Whether `greatestDamageReceived` aggregates DoT ticks | **UNRESOLVED** | One L0 trial vs a bleeding/poison enemy |
| Whether `Life healed` counts potion heals | **untestable in this run** (0 used) | One potion in an L0 trial |
| Exact ADCTH / Battle Surge split inside the 2,521 in-fight HP | **BANDED, not resolved** | The two ablation trials in §8.4 |
| The rolled values of the two jittered affixes (regen 7.2–12.8 %, leech 3.25–6.75 %) | seeds known (`1128683692` ring, `71443720` helm); jitter RNG not reversed | Read the item tooltips off a screenshot — or accept the band |
| `character_info.difficulty = 128` decoded against `balancingadjustment_mp+difficulty_players01.dbr` | not attempted | low priority; affects §3 only |

---

## SOURCE LIST

**Primary — corpus** (`/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/`, accessed 2026-07-28;
4 `.arz` layers merged in override order base → gdx1 → gdx2 → gdx3, 93,190 records; 8 `Text_EN.arc`
merged, 20,394 tags):

- `records/creatures/pc/malepc01.dbr` — `characterLifeRegen 1.0` · `characterConstitution 300.0` · **`acceleratedLifeRegenPercent 25.0`**
- `records/creatures/pc/playerlevels.dbr` · `records/game/gameengine.dbr` (`combatIdleTime 1.2`) · `records/game/combatformulas.dbr`
- `records/skills/playerclass10/` — `passive02.dbr` (**Battle Surge**) · `werewolf1.dbr` · `werewolf1b.dbr` · `amatokpact1.dbr` + `amatokpact1_buff.dbr` · `onslaught1.dbr` · `werewolf1_skill01_claws.dbr` · `werewolf1_skill02_charge.dbr` · `_classtraining_class10.dbr`
- `records/items/lootaffixes/` — `prefix/ao008a_lifeleech_01.dbr` · `suffix/b_ar014_arje.dbr` · `suffix/b_ar002_ar.dbr` · `gdx1 suffix/b_ar103_ar_a.dbr` · `prefix/aa007a_lifemod_01.dbr`
- `records/creatures/enemies/zombie_g01.dbr` · `zombie_soldiera01.dbr`
- `records/ui/character/characterinfotab1/charinfo_stats{oa,da}rollover.dbr` · `characterinfotab3/statssection/charinfo_greatestdamagetakenrollover.dbr`
- `Text_EN.arc` — `tagTutorialTip45Text{A,B,C,D}` · `tagQuickTip{06,45,46}` · `tagBonusLifePercentBuff` · `DamageLifeLeech` · `tagCharLifeRegen{,Modifier}` · `tagCharStatsDALast` · `tagRecord*` family

**Primary — save:** `agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7/parsed.json`,
`gear_resolved.json` (own G-7/U-1 parse of `player.gdc`, `_version` 12 play-stats block).

**Primary — client telemetry (galadriel):**
`captures/2026-07-26-gd-playtest-v1/ta-full-2fps-gated.csv` (13,633 samples, `life_healed` series) ·
`captures/2026-07-26-gd-playtest-v1-tb/tb-engagement-windows.json` (106 engagements) ·
`tb-intake-frames.jsonl.gz` (19,348 frames @ 15 fps) · `tb-intake-windows.json` · `tb-crosscheck-healing.json`

**Team notes cited:** `legolas/notes/2026-07-28-kitcal1-g5a-gd-level12-opposition-ledger.md` (OA/DA/damage
ledger) · `galadriel/notes/2026-07-28-gd-playtest-v1-g2c-survivability.md` (max-HP plateau table) ·
`galadriel/notes/2026-07-28-gd-playtest-v1-g6-skill-screenshots.md` (rank table, F-G6-2) ·
`gandalf/notes/2026-07-26-gd-playtest-v1-artifact-verification.md` (the 12,468.06 end-of-run read).

**Analysis scripts (scratch, reproducible):**
`agentic_orchestration/legolas/scratch/2026-07-28-gdc-parse-g7/` — `arz_index.py`, `arc_text.py`,
`lib_corpus.py`, `dumpnz.py`.
