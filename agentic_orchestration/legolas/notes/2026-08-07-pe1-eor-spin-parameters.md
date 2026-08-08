# PROBE P-E1 — Eye of Reckoning channel parameters from the `.arz` — 2026-08-07

**Mode:** A (analytical / primary-source extraction)
**Agent:** legolas (UNKNOWN-RESEARCHER)
**Commissioner:** gandalf (RUN-CONDUCTOR), KC2-SIM Phase A
**Access mode:** read-only throughout. Nothing outside this repo was written; the vendor tree was
opened read-only by the banked `.arz` / `.arc` adapters only.
**Scratch:** `agentic_orchestration/legolas/scratch/2026-08-07-pe1-eor/`
**Uncommitted** per commission (conductor centralises commits at gate closes).

---

## VERDICT BLOCK

**Five of six targets close DB-CITED. One sub-parameter — the *unit* of the energy drain — does not,
and it is a 6.25× fork, so it is named rather than blended.**

- **Tick cadence is DB-resident, not engine-hardcoded.** `timeBetweenAttacks = 200` on
  `eyeofreckoning1.dbr`, and the skill's **own display tag states the engine-effective value and its
  attack-speed law verbatim**: *"At 100% Attack Speed, Eye of Reckoning deals damage and drains
  Energy every 0.16s."* The DB→tooltip conversion is **× 0.8 ms per unit**, verified exactly on
  **two distinct values across nine skills, zero exceptions**. The commission's pre-declared
  ESTIMATED fallback is **not needed**.
- **Radius is 3.0 m, scalar, and immovable.** No per-rank growth, and **no EoR modifier anywhere in
  the corpus alters radius, cadence, channel duration, or energy cost** — a corpus-wide scan of all
  26 EoR-family records. Gear moves damage only.
- **Total rank 26 is arithmetically closed, and it corrects prior art.** Allocated 15 (`.gdc`)
  + 11 from gear = **exactly 26** = `skillUltimateLevel`. This independently reproduces gandalf's
  ceremony-lane grimtools reading from two lanes that never touched each other. **The save-parse
  note § 2.5's attribution of that bonus is wrong in both of its named sources** (§ 6 below).
- **THE ONE GAP — energy-drain unit.** `skillManaCost[26] = 16.0` is DB-CITED. Whether that is
  **16/second** or **16/tick (= 100/s at 100% attack speed, and attack-speed-scaling)** is
  **UNRESOLVED**. My own 2026-07-28 note ruled per-tick; this pass found real evidence on both
  sides and will not quietly ratify either. § 4.3 gives both models, the footage bound, and a
  one-screenshot closure lever.

**Closure verdict at the foot of the note.**

---

## 0 — Substrate and integrity

### 0.1 Corpus path resolution (commission said `~/Games/vendor/grim-dawn/`)

The commission names `~/Games/vendor/grim-dawn/`. That tree is the raw depot pull and **carries no
`gdx3/` (Fangs of Asterkarn)**. The Edition-II corpus at
`~/Games/vendor/grim-dawn-edition-II-20260724/` is a **strict superset** and is what I read.
They are the same data where they overlap:

```
md5 grim-dawn/database/database.arz              = 20d47784be5f93124636992f9e5562e2
md5 grim-dawn-edition-II-20260724/database/…arz  = 20d47784be5f93124636992f9e5562e2   ✓ identical
```

`GDX1.arz` / `GDX2.arz` are byte-size-identical across both trees. **`GDX3.arz` exists only in
Edition-II**, and it *is* load-bearing here — it carries the live Sandreaver Bracers record (§ 5).
Reading `~/Games/vendor/grim-dawn/` alone would have silently returned a pre-FoA item.

| Archive | Read | Role |
|---|---|---|
| `database/database.arz` | ✓ | base game; devotion, templates-adjacent |
| `gdx1/database/GDX1.arz` | ✓ | AoM; Gutsmasher base, Warborn base |
| `gdx2/database/GDX2.arz` | ✓ | **FG — EoR lives here**; Warborn/Gutsmasher EoR wiring |
| `gdx3/database/GDX3.arz` | ✓ | FoA; Sandreaver live record, two MI EoR modifiers |
| `resources/Text_EN.arc` ×4 | ✓ | display tags, UI format tags |
| `database/templates.arc` | ✓ | **field semantics + units** (819 templates) |

**Precedence rule applied throughout:** later archive wins. Every "live" value below is from the
highest-precedence archive containing the record, and the archive is named on every row.

### 0.2 Corpus is pinned at 1.3.0.0; the sitting ran 1.3.0.5

Per the patch-delta probe (2026-08-04), the endgame-kit join surface is **join-safe** across that
gap. This pass adds a positive check: the 1.3.0.0 patch note *"Eye of Reckoning: increased %
Weapon damage scaling with rank to 39%, 50% by max ultimate rank. Added % Crowd Control and % Max
Crowd Control resist for the caster while channeling"* is **present in the extracted record** —
`weaponDamagePct[16] = 39`, `weaponDamagePct[26] = 50`, and both `defensiveCrowdControl` arrays
exist. **The corpus is confirmed post-1.3.0.0 on this exact record.**

### 0.3 Tooling (all read-only, all in scratch)

`dump.py`, `dump_nz.py` (non-trivial-field filter), `arzgrep.py`, `byclass.py`, `byfield.py`,
`modscan.py`, `eorscan.py`, `eorgrant.py`, `tpl.py`, `tags.py` — over the banked adapters
`research/scripts/gd_arz_adapter_2026_07_24.py` and `gd_arc_reader_2026_07_26.py`.

---

## 1 — TARGET 1: tick cadence — **DB-CITED**

### 1.1 The record field

```
records/skills/playerclass09/eyeofreckoning1.dbr        [GDX2.arz]
    Class                 = 'Skill_AttackRadiusSpin'
    templateName          = 'database/templates/skill_attackradiusspin.tpl'
    timeBetweenAttacks    = 200          (int)
```

Template-authored semantics, verbatim from `templates.arc :: skill_attackradiusspin.tpl`:

```
Variable { name = "timeBetweenAttacks"  type = "int"
           description = "Time between hits to enemies along the path" }
```

**This is the damage-application period. It is DB-resident.** The commission's pre-declared
"engine-side hardcoded → ESTIMATED" fallback does not fire.

### 1.2 The engine-effective value, stated by the skill itself

`gdx2/resources/Text_EN.arc :: tagsgdx2_skills.txt`, tag `tagGDX2Class09SkillDescription07A`
(the in-game EoR description), final sentence **verbatim**:

> *"Requires a melee weapon. **At 100% Attack Speed, Eye of Reckoning deals damage and drains Energy
> every 0.16s.**"*

**This single sentence answers three of the commission's questions at once:** the cadence (0.16 s),
that attack speed modifies it, and that the energy drain is on the *same* interval as the damage.

### 1.3 The DB→engine conversion, verified rather than assumed

The DB says 200; the tooltip says 0.16 s. That is a 0.8 factor, and it is **not** a rounding — it
reproduces exactly on every channelled skill in the corpus that states its interval:

| Skill | record | `timeBetweenAttacks` | stated interval | ×0.8 ms check |
|---|---|---:|---:|:--:|
| **Eye of Reckoning** | `playerclass09/eyeofreckoning1` | **200** | **0.16 s** | ✓ |
| Voracious Reach (relic) | `itemskillsgdx2/relics/hungeringreach` | 200 | 0.16 s | ✓ |
| Winds of Asterkarn | `playerclass10/windsofasterkarn1` | 200 | 0.16 s | ✓ |
| Albrecht's Aether Ray | `playerclass05/aetherray1` | 300 | 0.24 s | ✓ |
| Flames of Ignaffar | `playerclass07/purifyingflame1` | 300 | 0.24 s | ✓ |
| Drain Essence | `playerclass08/lifetap1` | 300 | 0.24 s | ✓ |
| Acid Purge (component) | `tagGDX1CompSkillA104Desc` | 300† | 0.24 s | ✓ |
| Obliteration (item) | `tagItemSkillD146Desc` | 300† | 0.24 s | ✓ |
| Conflagration (relic) | `tagRelicSkillC008Desc` | 300† | 0.24 s | ✓ |

† tag-side only; the three item/component skills were matched by tag text, not by record.

**Two distinct DB values, nine skills, zero exceptions.**
`period_at_100%_speed (s) = timeBetweenAttacks × 0.0008`.
Equivalently `timeBetweenAttacks` is denominated in **0.8 ms quanta (1250 Hz)**.

*Corroboration that the unit is real and not a display convention:* Soulfire's sibling field
`projectilePeriod` is typed **`real`** and holds `0.2` (plain seconds), while `timeBetweenAttacks`
is typed **`int`**. The two live in the same record family with different units — consistent with
`timeBetweenAttacks` being a quantised integer field rather than plain milliseconds.

### 1.4 Attack-speed law

**DB-CITED that the coupling exists** ("At 100% Attack Speed…"). **INFERRED that it is simple
inverse proportionality:**

```
tick_period(s) = 0.16 × (100 / attack_speed_percent)
tick_rate(Hz)  = 6.25 × (attack_speed_percent / 100)
```

The DB does not state the functional form; inverse proportionality is the only form under which
"at 100% attack speed" is a meaningful qualifier, and it matches the family convention (the beam
skills use "at 100% **Cast** Speed" identically). Grade this line **INFERRED (strong)**.

**Corroborating that attack speed is a live variable inside the channel:** two GDX3 monster-infrequent
EoR modifiers grant attack speed *scoped to the skill* —
`itemskillsgdx3/skillmodifiers/mi/axe2h_b306_eyeofreckoning.dbr` and `…b307_…`, each
`characterAttackSpeedModifier = 20.0`. Neither is in this build.

**In-build attack-speed contribution found:** the Warborn set grants
`characterAttackSpeedModifier = [0.0, 0.0, 10.0, 10.0]` — **+10% at 3 pieces**, and the build wears
exactly 3 (§ 5.3). The build's *total* attack speed is a character-sheet quantity this probe cannot
reach; it must come from the frame corpus.

### 1.5 Channel state machine — the fields the spec's § channel-state-machine needs

```
Class                = 'Skill_AttackRadiusSpin'
  └─ includes         database/Templates/SkillChanneled.tpl
duration             = 0.25      (SkillChanneled, template default 0.2)
useResetsDuration    = True      (SkillChanneled, template default 1)
canUseWhileMoving    = True
delayMovement        = True
rotationSpeedMultiplier = 0.35   "Multiplier applied to player rotation speed while skill is active"
skillCooldownTime    = (absent → 0)      no cooldown
expansionTime        = (absent → 0)      radius does not expand over time
targetingMode        = 'Point'
distanceProfile      = 'Melee'
```

**Reading (INFERRED, from template structure):** the channel is implemented as a **0.25 s
self-refreshing effect** — holding the button re-issues the skill, and `useResetsDuration` restamps
the 0.25 s window. Release therefore leaves a **≤ 0.25 s tail** before the effect lapses.
`duration` is **not** the tick period; `timeBetweenAttacks` is. `rotationSpeedMultiplier = 0.35`
means the player turns at **35 % of normal turn rate while channelling** — a real handling
constraint the sim should carry, because it caps how fast the 3 m disc can be re-aimed.

**Weapon gating (DB-CITED):** `Sword, Axe, Mace, Dagger, Scepter, Sword2h, Axe2h, Mace2h, Spear2h
= True`; `Ranged1h/2h, Staff, Magical, Shield, Offhand = False`. Gutsmasher is `Mace2h` → legal.
**This is the DB-side confirmation of the § 3.1 set-II hazard**: swapping to an empty weapon set
makes EoR *unusable*, not merely weaker.

---

## 2 — TARGET 2: radius — **DB-CITED**

```
skillTargetRadius = 3.0        (scalar — NOT a per-rank array)
expansionTime     = absent (0) — no growth over channel time
```

**Unit is MEASURED, not assumed.** Our own KIT-CAL-1 pass pinned this exact field against
screenshot text twice — `skillTargetRadius = 2.5` → *"2.5 Meter Target Area"*, and
`skillTargetRadius = 12.0` → *"12 Meter Radius"*
(`legolas/notes/2026-07-28-kitcal1-u1-kit-values-and-boss.md` §§ 137, 222). The field renders 1:1
as metres. **EoR = 3.0 m radius disc.**

**No per-rank growth, and no modifier can move it.** A corpus-wide scan (`modscan.py`) of all
**26** EoR-family records — every item skill-modifier, every set modifier, both player records —
found **zero** occurrences of `skillTargetRadius`, `timeBetweenAttacks`, `duration`,
`expansionTime` or `skillManaCost` outside the base record. **Radius, cadence, channel duration and
drain are fixed constants for every EoR build in the game.** Gear moves damage, conversion and
attack speed only.

Contrast for the sim's geometry model: Soulfire's orbiting projectile carries its own
`projectileExplosionRadius = 0.2` and is independent of the 3 m disc (§ 4.4).

---

## 3 — TARGET 4: per-tick damage basis — **DB-CITED**

All arrays on `eyeofreckoning1.dbr` are **26 elements** (`skillMaxLevel = 16`,
`skillUltimateLevel = 26`), index 0 = rank 1.

### 3.1 Base skill, per tick

| Field | @ rank 26 | Note |
|---|---:|---|
| `weaponDamagePct` | **50.0 %** | template: *"Percentage weapon damage to use for each skill level"* |
| `offensivePhysicalMin` / `Max` | **162 – 182** | flat physical add |
| `offensiveFireMin` | **138** | **flat, min only — `offensiveFireMax` is absent from the record** |
| `defensiveCrowdControl` | 25.0 % | 1.3.0.0 addition, caster CC resist while channelling |
| `defensiveCrowdControlMaxResist` | 25.0 % | 1.3.0.0 addition |

`offensiveFireMax` genuinely does not exist in the record — fire is a **point value, not a range**.
Do not model it as 138–138 by accident of a defaulting parser; model it as flat.

### 3.2 Patch-note cross-validation of the damage basis

Independent confirmation that the extraction is reading the right fields, from the 1.3.0.0 notes
(banked `scratch/2026-08-01-eor-addendum/raw_155979.txt`):

| Patch line (verbatim) | DB field | Match |
|---|---|:--:|
| *"Eye of Reckoning: increased % Weapon damage scaling with rank to **39%**, **50%** by max ultimate rank"* | `weaponDamagePct[16]=39`, `[26]=50` | **✓✓** |
| *"Added % Crowd Control and % Max Crowd Control resist for the caster while channeling the skill, scaling with rank"* | both `defensiveCrowdControl*` arrays present | ✓ |
| *"Soulfire: increased % Damage Reduction scaling with rank to **20%** by rank 12, **30%** by max ultimate rank"* | `eyeofreckoning2.offensiveTotalDamageReductionPercentMin[12]=20`, `[22]=30` | **✓✓** |
| *"Mythical Wrath of Tenebris: increased % Weapon damage modifier for EoR to **24%**"* | `mi`/`legendary/axe2h_d206_eyeofreckoning.weaponDamagePct = 24.0` | **✓** |

The last row is doubly useful: it establishes that a `Skill_Modifier`'s `weaponDamagePct` is
**additive to the base skill's %**, because Crate calls it *"% Weapon damage **modifier** for Eye of
Reckoning"*. That licenses the arithmetic in § 5.4.

---

## 4 — TARGET 3: energy drain — **value DB-CITED, unit UNRESOLVED**

### 4.1 The field

```
skillManaCost = [4,4,5,5,5,6,6,7,7,8,8,9,9,10,10,11,11,12,12,13,13,14,14,15,15,16]   (ranks 1..26)
skillManaCost[26] = 16.0
```

Template `templatebase/skill_activated.tpl` declares `skillManaCost` as `real` with **no description
string** — the DB does not name its unit.

### 4.2 What the DB does say

- The EoR description tag: *"deals damage **and drains Energy** every 0.16s"* — the drain is
  **discretised onto the damage tick**. DB-CITED.
- `tags_ui.txt` carries **both** `ManaCost = "Energy Cost"` **and**
  `ManaCostPerSecond = "Energy Cost per Second"`, plus a third,
  `ActiveManaCost = "Active Energy Cost per Second"` for reserve auras. So the UI has a dedicated
  per-second label for channels — but the label does not tell us whether the *stored* number is the
  per-second figure or a per-tick figure the UI multiplies up.
- `tagClass05SkillDescription06B` (Disintegration, the Aether Ray modifier), verbatim:
  *"**Energy Cost increase is per damage interval.**"* Its own `skillManaCost` is 3–20 against the
  base ray's 12–87. Crate wrote that clarification **because this one differs from the base's
  display** — which is consistent with per-tick storage + per-second display, and equally
  consistent with per-second storage. **It does not discriminate.**

### 4.3 The fork, stated plainly

| | **M1 — stored value is per SECOND** | **M2 — stored value is per TICK** |
|---|---|---|
| EoR drain @ rank 26, 100% AS | **16 / s** | **100 / s** (16 ÷ 0.16) |
| Scales with attack speed? | **No** | **Yes**, linearly |
| @ ~180% AS (plausible for this build) | 16 / s | **~180 / s** |
| Albrecht's Aether Ray @ r26 (87) | 87 / s | 362 / s |
| Winds of Asterkarn @ r26 (45) | 45 / s | 281 / s |

**Evidence for M2 (per tick):**
1. **Magnitude band.** Oathkeeper *per-cast* skills cost 14–32 at rank 1 (Aegis 14, Vire's Might 22,
   Judgment 30, Ascension 32). *Per-repetition* skills cost 1–4 — **Righteous Fervor `[1,1,1,2,…]`**,
   EoR `[4,4,5,…]`. EoR sits unambiguously in the repetition band, not the cast band. **Strong.**
   (This is the argument my 2026-07-28 note ruled on, and it survives re-examination.)
2. Tag phrasing puts damage and drain in the same clause on the same interval.
3. fordprefect's own build rationale, verbatim: *"You need **Scales** for energy regen."* A build
   spending a whole constellation on energy implies a large drain, not a 16/s one.
4. **Scales supplies exactly the right order of magnitude.** Tip the Scales
   (`records/skills/devotion/tier2_02f_skill.dbr`, bound in this build to Presence of Virtue at
   `cast_@enemyonanyhit_33%`) carries `offensiveSlowManaLeachMin = 200` over
   `offensiveSlowManaLeachDurationMin = 2.0 s` on `skillCooldownTime = 1.0` — i.e. up to
   **~100–200 energy/s of leech, near-continuously up under a multi-target channel.** That is the
   income M2 needs and M1 does not.

**Evidence for M1 (per second):**
1. The dedicated `ManaCostPerSecond` UI label exists at all.
2. M2 implies Albrecht's Aether Ray costs **362 energy/s** at ultimate rank and Winds of Asterkarn
   **281/s**. Those are extreme even for GD's most notorious energy hogs.

### 4.4 Footage bound — **ESTIMATED**, and it does not break the tie

Measured off the in-flight galadriel capture set
(`galadriel/captures/2026-08-07-eor-sittings/work/`, full frames at 1920×1080, read-only; energy
globe cropped and upscaled by me at `scratch/2026-08-07-pe1-eor/energy-{800,strip}.png`):

| frame | energy globe |
|---|---|
| `s2-full-200.png` | **1594 / 2576** |
| `s2-full-500.png` | **1594 / 2576** |
| `s2-full-800.png` (wave 158, active combat) | **1508 / 2576** |
| `s2-full-1000.png`, `-1030.png` | **1594 / 2576** |
| commission's cited point (wave ~156, channelling) | **1477 / 2576** |

**1594 recurs identically at four timestamps spanning 830 s. That is a ceiling, not a coincidence** —
the build **reserves ≈ 982 energy**. Reserve sources confirmed in the DB:
`presenceofvirtue1_buff.characterManaLimitReserve` (200 at total rank 16),
`presenceofvirtue2` (100 @ 10), `presenceofvirtue3` (107 @ 11),
`fieldcommand1buff` (175 @ 11), `fieldcommand2` (42 @ 9) — **624 flat accounted for from five
skills alone**, before `characterManaLimitReserveModifier` percentages and unenumerated sources.
The reserve mechanic itself is MEASURED-pinned in our prior art
(`characterManaLimitReserve = 50.0` → *"50 Energy Reserved"*, kitcal1-u1 § 221).

**Therefore the operative reading is: effective usable ceiling ≈ 1,594, and sustained channelling
draws the bar down only 86–117 below that ceiling before it recovers.**

**Why this still does not settle it.** A ~100-energy dip per wave is trivially explained by M1
(16/s gross, near-parity with regen). It is *also* explained by M2 **if** Tip the Scales' ~100–200/s
leech is up most of the time — which, at 6–11 ticks/s across a 3 m disc full of Crucible enemies and
a 1 s proc cooldown, it would be. **Both models survive the footage.** I decline to ratify either
on a fit.

### 4.5 The closure lever — cheap, one artefact

**One screenshot of the Eye of Reckoning skill tooltip.** The tooltip renders a
`ManaCostPerSecond` line.

- If it reads **≈ 16** → **M1**, and my 2026-07-28 § 6 ruling is wrong.
- If it reads **≈ 100** → **M2**, confirmed, and drain scales with attack speed.

No other measurement is needed. The skill tree is two keypresses from the Crucible lobby.

**Until then, the spec must carry the drain as a switch, not a number.** If forced to pick one for
a first fit, pick **M2 at 100/s @ 100% AS scaled by attack speed** — it is the reading with three
independent supports and it is the reading our prior art already banked; but tag it and expect to
move it.

---

## 5 — TARGET 5: rank scale, and the rank-26 closure

### 5.1 Rank arithmetic — **MEASURED, and it closes exactly on 26**

The `.gdc` stores **allocated** rank; grimtools shows **total**. Composing this probe's item records
with the save-parse note's allocated ranks:

| Source | record (live archive) | field | +EoR |
|---|---|---|---:|
| allocated | `player.gdc :: character_skills` | `eyeofreckoning1.level` | **15** |
| **Gutsmasher** | `items/gearweapons/melee2h/d107_blunt2h` [GDX2] | `augmentSkillName2` / `Level2` | **+4** |
| **Warborn Visor** | `items/upgraded/gearhead/d028_head` [GDX2] | `augmentSkillName1` / `Level1` | **+2** |
| **Warborn Chestguard** | `items/upgraded/geartorso/d026_torso` [GDX2] | `augmentSkillName4` / `Level4` | **+2** |
| **Sandreaver Bracers** | `items/gearhands/d206_hands` [**GDX3**] | `augmentSkillName4` / `Level4` | **+2** |
| **Kaisan's Burning Eye** | `items/gearaccessories/necklaces/b201e_necklace` [GDX2] | **`augmentAllLevel = 1`** | **+1** |
| Warborn set 4-pc | `items/lootsets/itemset_d025b` | `augmentSkillLevel4 = [0,0,0,3]` | **+0** (3 pieces worn) |
| | | **TOTAL** | **26** |

**15 + 11 = 26 = `skillUltimateLevel`.** This reproduces gandalf's ceremony-lane grimtools reading
**from two lanes that never touched each other** — the `.gdc` and the `.arz`. Item 1′ of the
save-parse grade summary can be upgraded on this axis.

**Soulfire total rank = 15**: allocated 12 + Warborn Pauldrons `augmentSkillName4 = eyeofreckoning2`
`Level4 = 2` + necklace `augmentAllLevel = 1`. (`skillMaxLevel = 12`, `skillUltimateLevel = 22`.)

### 5.2 Per-rank table, ranks 15–26 — **DB-CITED**

`records/skills/playerclass09/eyeofreckoning1.dbr` [GDX2.arz]. Arrays are 26 long; row *n* is
index *n−1*. **Cite rank 26.**

| rank | `weaponDamagePct` | `offensivePhysicalMin` | `offensivePhysicalMax` | `offensiveFireMin` | `skillManaCost` | `defensiveCrowdControl` | `…MaxResist` |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 15 | 38 | 80 | 88 | 66 | 10 | 14 | 14 |
| **16** *(alloc. cap)* | **39** | 85 | 94 | 70 | 11 | 15 | 15 |
| 17 | 40 | 91 | 101 | 75 | 11 | 16 | 16 |
| 18 | 41 | 97 | 108 | 80 | 12 | 17 | 17 |
| 19 | 42 | 103 | 115 | 85 | 12 | 18 | 18 |
| 20 | 43 | 109 | 122 | 90 | 13 | 19 | 19 |
| 21 | 44 | 115 | 129 | 95 | 13 | 20 | 20 |
| 22 | 45 | 122 | 137 | 101 | 14 | 21 | 21 |
| 23 | 46 | 129 | 145 | 107 | 14 | 22 | 22 |
| 24 | 47 | 139 | 156 | 116 | 15 | 23 | 23 |
| 25 | 48 | 149 | 167 | 125 | 15 | 24 | 24 |
| **26** *(build; ultimate)* | **50** | **162** | **182** | **138** | **16** | **25** | **25** |

Soulfire (`eyeofreckoning2`, 22-element arrays), neighbourhood of the build's rank 15:

| rank | `offensiveLightningMin` | `offensiveTotalDamageReductionPercentMin` |
|---:|---:|---:|
| 12 *(alloc. cap)* | 195 | 20 % |
| 13 | 212 | 21 % |
| 14 | 229 | 22 % |
| **15** *(build)* | **246** | **23 %** |
| 16 | 263 | 24 % |
| 22 *(ultimate)* | 402 | 30 % |

`offensiveTotalDamageReductionPercentDurationMin = 2.0 s` (scalar).

### 5.3 Warborn set: the build wears 3 of 4 — what that gates

`records/items/lootsets/itemset_d025b.dbr` — `FileDescription = 'Warborn Armor'`,
`setMembers = [gearhead/d028_head, geartorso/d026_torso, gearshoulders/d026_shoulder,
gearweapons/blunt1h/d008_blunt]`. The build wears the three armour pieces and **not** the 1H mace
(it wears Gutsmasher, a 2H). Piece-count-indexed arrays therefore read at **index 2**:

| set field | array | **@ 3 pieces** |
|---|---|---:|
| `characterAttackSpeedModifier` | `[0, 0, 10, 10]` | **+10 %** ← feeds § 1.4 |
| `offensivePhysicalMin` / `Max` | `[0,0,18,18]` / `[0,0,30,30]` | +18–30 |
| `defensiveAbsorptionModifier` | `[0, 10, 10, 10]` | +10 % |
| `defensiveBonusProtection` | `[0, 120, 120, 120]` | +120 armour |
| `augmentSkillLevel4` (→ EoR) | `[0, 0, 0, 3]` | **+0** |
| `itemSkillModifierControl` | `[0, 0, 0, 1]` | **0 → set skill-modifiers OFF** |

`itemSkillModifierControl` is template-documented as *"Determines on/off (1/0) of skill modifiers"*.
At 3 pieces it is **0**, so **none of the set's three `modifierSkillName` entries is active** —
including `set_d025_eyeofreckoning` (+5 % weapon damage). **Do not credit the build with it.**

### 5.4 Composed per-tick basis at the build's rank 26

| Component | Source | Value |
|---|---|---|
| Weapon damage % | base `weaponDamagePct[26]` | 50 % |
| + Gutsmasher modifier | `mace2h_d107_eyeofreckoning.weaponDamagePct` | **+14 %** |
| + Warborn set modifier | gated off at 3 pieces (§ 5.3) | +0 % |
| **Total weapon damage per tick** | | **64 %** |
| Flat physical | base `offensivePhysicalMin/Max[26]` | 162 – 182 |
| + Sandreaver | `hands_d206_eyeofreckoning.offensivePhysicalMin` | +24 |
| Flat fire | base `offensiveFireMin[26]` | 138 (flat) |
| **Fire → Physical** | Gutsmasher `conversionPercentage = 100` | **all 138 becomes physical** |
| **Composed flat, all physical** | | **≈ 324 – 344** |
| Crit damage | Warborn Visor `offensiveCritDamageModifier` | +12 % |
| Bleed | Gutsmasher 330 / 3 s (+50 % dmg mod, +100 % duration mod) + Sandreaver 210 / 3 s | 540 / 3 s pre-modifier |

**Ordering caveat, flagged not resolved:** GD's application order for
`conversion` vs `offensive*Modifier` vs global %-damage bonuses is **not** stated in the DBRs. The
324–344 figure assumes conversion is applied to the skill's own flat fire before global modifiers.
Grade the *components* DB-CITED and the *composition* **INFERRED**.

---

## 6 — TARGET 6: modifier nodes on EoR in the build-of-record — **DB-CITED**

### 6.1 Active in this build

| Item (slot) | modifier record [archive] | Effect on EoR |
|---|---|---|
| **Gutsmasher** (WS1 main) | `itemskillsgdx2/skillmodifiers/upgradedgdx2/mace2h_d107_eyeofreckoning.dbr` [GDX2] | `weaponDamagePct +14` · **`conversionInType Fire → conversionOutType Physical`, `conversionPercentage 100`** · `offensiveSlowBleedingMin 330` / `DurationMin 3.0` · `offensiveSlowBleedingModifier +50` · `offensiveSlowBleedingDurationModifier +100` |
| **Sandreaver Bracers** (hands) | `…/skillmodifiers/legendary/hands_d206_eyeofreckoning.dbr` [GDX2] | `offensivePhysicalMin +24` · `offensiveSlowBleedingMin 210` / `3.0 s` |
| **Warborn Visor** (head) | `…/skillmodifiers/upgradedgdx2/head_d028_eyeofreckoning.dbr` [GDX2] | `offensiveCritDamageModifier +12` |
| Warborn set (3 pc) | `…/skillmodifiers/upgradedgdx2/set_d025_eyeofreckoning.dbr` | **INACTIVE** — `itemSkillModifierControl` = 0 at 3 pieces (§ 5.3) |

**Attachment is verified from the item side, not assumed:** each item record carries a matched
`modifiedSkillName<i> = records/skills/playerclass09/eyeofreckoning1.dbr` /
`modifierSkillName<i> = <the modifier record>` pair. Full wiring in
`scratch/2026-08-07-pe1-eor/` (`eorscan.py` output).

### 6.2 The load-bearing one

**Gutsmasher's `Fire → Physical @ 100%` is the mechanism that makes this a "2H **Physical** EoR"
build.** EoR's own base damage is Physical + Fire; the weapon deletes the fire split entirely.
Any sim of this fixture that models EoR as a mixed physical/fire skill is modelling a *different*
build. This is a single record field and it changes the whole damage-type profile.

### 6.3 What **no** modifier does — the negative result that bounds the sim

Corpus-wide across all 26 EoR-family records: **not one** touches `timeBetweenAttacks`,
`skillTargetRadius`, `duration`, `expansionTime` or `skillManaCost`. The only levers gear has on the
channel are `weaponDamagePct`, flat/DoT damage adds, damage-type `conversion*`, crit modifiers, and
`characterAttackSpeedModifier`. **Cadence, radius and drain are build-invariant constants** — a
useful simplification for the spec, and a stronger claim than "we didn't find any".

### 6.4 Soulfire's own geometry (separate cadence — do not fold into the disc)

```
records/skills/playerclass09/eyeofreckoning2.dbr   Class = SkillSecondary_AttackProjectileOrbiting
  projectilePeriod              = 0.2      (real, seconds)
  projectileExplosionRadius     = 0.2
  skillProjectileNumber         = 1
  projectilePiercingChance      = 100.0
  projectileDirection           = 'Counterclockwise'
  projectileStart               = 'Front'
  skillProjectileTargetGroundOnly = True
```

Soulfire spawns **one piercing orbiting projectile every 0.2 s**, independent of the 3 m disc and of
`timeBetweenAttacks`. Whether `projectilePeriod` also takes the ×0.8 conversion is **UNKNOWN** — no
tag states an interval for it, and its `real`/seconds typing suggests it does not. **Flagged.**

**And note:** Soulfire's damage is `offensiveLightningMin` — **Lightning**, despite the name.
Gutsmasher converts **Fire→Physical only**, so Soulfire's lightning is *not* converted. This build
therefore emits a genuine, un-converted Lightning component (246 per projectile at rank 15) on top
of an otherwise all-physical profile. Easy to miss; easy to mis-model.

---

## 7 — Corrections to our own prior art

1. **`legolas/notes/2026-08-05-eorwarlguts-save-parse.md` § 2.5 — the gear attribution is wrong in
   both named sources.** It states *"Gutsmasher — `augmentMasteryLevel1 = 2`, `augmentMasteryLevel2
   = 2` → +2 to **every Soldier and Oathkeeper** skill"* and *"Warborn Visor — `augmentMasteryLevel1/2
   = 1` → +1 to both masteries."* Measured:
   - Gutsmasher `augmentMasteryName1 = _classtraining_class01` (**Soldier**),
     `augmentMasteryName2 = _classtraining_class03` (**Occultist**). **Not Oathkeeper.**
   - Warborn Visor `augmentMasteryName1 = class01` (**Soldier**), `augmentMasteryName2 = class08`
     (**Necromancer**). **Not Oathkeeper.**
   - **No equipped item grants any Oathkeeper mastery rank.** The mastery route contributes **zero**
     to EoR.
   **The conclusion of § 2.5 survives intact — 15 allocated, 26 total, scales are different — but
   the arithmetic behind it is now correct and complete (§ 5.1), and it lands on exactly 26 instead
   of gesturing at it.** The rule *"never compare a `.gdc` rank to a grimtools rank"* stands.
2. **Same note § 3.1 — the set-II hazard is sharper than recorded.** EoR's weapon gate
   (`Mace2h = True`, all ranged/caster types `False`) means an empty weapon set II does not merely
   drop DPS and mastery ranks: **it makes the build's only damage skill uncastable.** The
   recommendation to populate set II or disarm the swap key is upgraded from prudent to necessary.
3. **`legolas/notes/2026-07-28-eor-unlock-timing.md` § 6 — put back in play, not overturned.** Its
   per-tick ruling rests on the magnitude-band argument, which survives re-examination and gains a
   fourth support here (Tip the Scales' ~100–200/s leech is sized for an M2 drain). But its
   supporting claim that the ×0.8 relation implies per-tick storage is a **non sequitur** — the
   relation fixes the *interval*, not the *unit* — and the footage ceiling (§ 4.4) is equally
   consistent with M1. **§ 6 should be restamped from a ruling to a leading hypothesis until the
   tooltip screenshot lands.**
4. **Same note § 6, minor:** its cross-check table lists three channelled skills for the ×0.8
   relation. It is now **nine**, two distinct DB values, zero exceptions (§ 1.3).
5. **`legolas/notes/2026-07-23-kf23-harvest-gd.md` — a banked external claim is stale.** It records
   *"Flames of Ignaffar … ticks every 0.3s at 100% cast speed"* from a Steam discussion. The current
   DB + tag say **0.24 s** (`timeBetweenAttacks = 300`). Either the community source predates a
   cadence change or it read the raw DB value as milliseconds. **Prefer the tag.** Same note's
   "energy cost per second per rank — FULL GAP" for Flames of Ignaffar is **now closed**:
   `purifyingflame1.skillManaCost = [7,8,9,10,11,13,15,17,19,22,24,27,30,33,36,39,…,69]`.
6. **Corpus-path note for future commissions.** `~/Games/vendor/grim-dawn/` has **no GDX3**.
   Any join that touches FoA-era item records must read
   `~/Games/vendor/grim-dawn-edition-II-20260724/`. Reading the shorter tree returns pre-FoA records
   *silently* — no error, just an older row (§ 0.1).

---

## 8 — Open / unresolved

| # | Item | Why open | What closes it |
|---|---|---|---|
| **P1** | **`skillManaCost` unit on a channel: per second vs per tick (6.25× at 100% AS)** | DB declares no unit; both readings have independent support; footage is consistent with both once reserve + Tip the Scales are accounted (§ 4) | **One screenshot of the EoR skill tooltip.** ≈16 → M1; ≈100 → M2 |
| P2 | Whether the per-second drain scales with attack speed | Entailed by P1 (M2 yes, M1 no) | same screenshot |
| P3 | The build's total attack speed % | Character-sheet quantity; DB gives only the +10 % Warborn 3-pc contribution | one character-sheet frame |
| P4 | The build's energy regen / s | Not reachable from skill records; needed to convert the 86–117 dip into a drain | same character-sheet frame |
| P5 | Whether `projectilePeriod` (Soulfire, 0.2 s) takes the ×0.8 conversion | No tag states a Soulfire interval; `real`/seconds typing argues no | frame-level count of orbiting projectiles over a fixed window |
| P6 | Damage application order: `conversion` vs `offensive*Modifier` vs global % | Not stated in any DBR or template | comparison of a tooltip's composed number against the component fields |
| P7 | Provenance of the 0.8 factor | Empirically exact on 9 skills, but the *reason* (engine quantum? animation base-rate?) is unknown | not needed for the sim; noted for completeness |
| P8 | Reserve accounting: 624 flat found vs ≈982 observed | I enumerated Soldier + Oathkeeper skills only; `…ReserveModifier` percentages and item/devotion sources not swept | full reserve sweep, or one character-sheet frame |

---

## 9 — Source list

**Primary — game data** (all read-only, `~/Games/vendor/grim-dawn-edition-II-20260724/`, accessed
2026-08-07)

- `gdx2/database/GDX2.arz` :: `records/skills/playerclass09/eyeofreckoning1.dbr` · `eyeofreckoning2.dbr` ·
  `presenceofvirtue{1_buff,2,3}.dbr` · `righteousfervor1.dbr` ·
  `records/skills/itemskillsgdx2/skillmodifiers/**/*_eyeofreckoning.dbr` (20 records) ·
  `records/skills/itemskillsgdx2/relics/hungeringreach.dbr` ·
  `records/items/{upgraded/gearhead/d028_head, upgraded/geartorso/d026_torso,
  upgraded/gearshoulders/d026_shoulder, gearweapons/melee2h/d107_blunt2h,
  gearaccessories/necklaces/b201e_necklace, lootsets/itemset_d025b}.dbr`
- `gdx3/database/GDX3.arz` :: `records/items/gearhands/d206_hands.dbr` (**live** Sandreaver) ·
  `records/skills/playerclass10/windsofasterkarn1.dbr` ·
  `records/skills/itemskillsgdx3/skillmodifiers/mi/axe2h_b30{6,7}_eyeofreckoning.dbr`
- `gdx1/database/GDX1.arz` :: `records/skills/playerclass07/purifyingflame1.dbr` ·
  `playerclass08/lifetap1.dbr` · `records/items/gearrelic/d114_relic.dbr`
- `database/database.arz` :: `records/skills/playerclass05/aetherray{1,2}.dbr` ·
  `records/skills/devotion/tier2_02f_skill.dbr` (Tip the Scales) ·
  `records/skills/playerclass01/{fieldcommand1buff,fieldcommand2}.dbr`
- `database/templates.arc` (via `~/Games/vendor/grim-dawn/`) :: `skill_attackradiusspin.tpl` ·
  `skillchanneled.tpl` · `templatebase/{skill_base,skill_activated,skill_attack,skill_radius}.tpl` ·
  `itemset.tpl`
- `resources/Text_EN.arc` + `gdx{1,2,3}/resources/Text_EN.arc` :: `tags_skills.txt` ·
  `tagsgdx{1,2,3}_skills.txt` · `tags_ui.txt`

**Primary — developer text**

- Grim Dawn v1.3.0.0 patch notes, thread 155979 (banked
  `legolas/scratch/2026-08-01-eor-addendum/raw_155979.txt`), lines 136, 405, 655

**Primary — measured artefacts**

- `galadriel/captures/2026-08-07-eor-sittings/work/s2-full-{200,500,800,1000,1030}.png`
  (1920×1080; energy globe read at full res, read-only) — § 4.4
- `player.gdc` allocated ranks, via `legolas/notes/2026-08-05-eorwarlguts-save-parse.md` § 2.2

**Internal**

- `legolas/notes/2026-08-01-eor-endgame-build-of-record.md` §§ 1.4–1.8
- `legolas/notes/2026-08-05-eorwarlguts-save-parse.md` §§ 2.2, 2.5, 3, 3.1
- `legolas/notes/2026-07-28-eor-unlock-timing.md` § 6
- `legolas/notes/2026-07-28-kitcal1-u1-kit-values-and-boss.md` §§ 137, 221–222 (unit M-pins)
- `legolas/notes/2026-08-04-gd-1305-patch-delta-probe.md` (corpus pin, join safety)
- `legolas/notes/2026-07-23-kf23-harvest-gd.md` (stale external cadence claim, § 7.5)

---

## CLOSURE VERDICT

**PARTIAL** — targets 1 (cadence + attack-speed law), 2 (radius), 4 (per-tick damage basis),
5 (rank scale, closed exactly on 26) and 6 (modifier nodes) all **CLOSED-DB-CITED**; target 3
(energy drain) is **DB-CITED in value, UNRESOLVED in unit** — named gap **P1/P2**: `skillManaCost`
per-second vs per-tick, a 6.25× fork at 100% attack speed, closable by one screenshot of the Eye of
Reckoning tooltip.

---

**Signed:** legolas, 2026-08-07. The cadence was in the database after all — and the skill's own
description sentence told us the law, the interval and the drain coupling in one line, which is
worth more than the field it explains. What the database would not say is what a single number
*means*; that one costs a screenshot.
