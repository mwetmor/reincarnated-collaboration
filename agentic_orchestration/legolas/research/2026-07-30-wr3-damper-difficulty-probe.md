# Research — WR3 damper × difficulty probe — 2026-07-30

**Mode:** A (analytical / primary-source probe)
**Commissioner:** gandalf, RUN-CONDUCTOR, run WR3-KITE-COMMIT
**Hypothesis under test (Matt, verbatim):** *"I wonder if the dampening numbers have to do with difficulty setting..?"*
**Sources:** vendor pin `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/` (`database.arz` + GDX1-3,
93,190 records swept), legacy `/Users/admin/Games/vendor/grim-dawn/Game.dll` (symbol strings),
`Text_EN.arc` × 4 (20,245 tags), the referent `.gdc`, and three third-party `.gdc` saves fetched
read-only from `github.com/ChrisElison/GDParser`. Web used as tertiary corroboration only.
**Scratch:** `agentic_orchestration/legolas/scratch/2026-07-30-wr3-diffprobe/` (`e1_unwind.py`, `e2_veteran.py`)

**Grades:** **M** = measured//read directly from a primary artifact · **C** = concluded from M by
stated arithmetic · **D** = derived with a modelling assumption · **T** = tertiary (community)

---

## 0. VERDICT

**PARTIALLY DIFFICULTY-KEYED — and the probe found something bigger than the question asked.**

Three findings, in ascending order of consequence:

1. **The pak stage IS difficulty-keyed. Decisively, mechanically, exactly.** (M)
   `balancingadjustment_mp+difficulty_enemies01.dbr` carries **12-element arrays = 3 difficulties ×
   4 player counts**. `offensiveTotalDamageModifier = [−25 ×4, +25 ×4, +40 ×4]`. The −25 the run has
   been carrying is **slot 0 = Normal, 1 player**. Matt's instinct is correct: a clean round −25 % *is*
   a difficulty-table entry. It is the Normal cell of one.

2. **The pool stage is NOT difficulty-keyed — but it is monster-level-keyed, and that makes it
   difficulty-*sensitive*.** (M/C) `armorbase0N`'s `offensiveTotalDamageModifier` is a 200-entry
   rank array ramping **+1 percentage point per rank**, and the rank is the monster's `charLevel`.
   It is not a damper; it is a **level-normalising ramp** that starts at −90 and crosses zero at
   monster level 88. The "damping" is an artefact of reading a level-1-to-88 ramp at level 18.

3. **THE REFERENT SAVE WAS NOT PLAYED ON PLAIN NORMAL. The difficulty byte is `128`, not `0`.** (M)
   `0x80` is a flag bit over difficulty index 0. GD's only per-character overlay on Normal is
   **Veteran**, whose enemy adjustment record carries **`offensiveTotalDamageModifier +40`** and
   **`characterLifeModifier +140`**. Cross-checked empirically: two third-party saves parse as plain
   `0` (fresh Normal) and `2` (Ultimate). `128` is not a difficulty index.

**What this does to the run's open paradox:** the Veteran mutator multiplies monster outgoing damage
by **×1.40** (separate stage) or **×2.14** (pooled). Under either reading **the S2_FULL ceiling clears
both measured numbers** — 354.1 or 541.9 against targets of 260.498 / 273.704. **The 2.9 % ceiling
shortfall that was the entire mechanical basis for provisionally adopting S1_PAK (R-WR3-28) is
erased.** The paradox does not need S1_PAK to resolve. It needed the difficulty setting — exactly as
Matt suspected, though not by the route the commission anticipated.

**Answer to the DECISION QUESTION (§6), stated plainly:** **No — there is no difficulty-conditional
reading under which ×0.75 is what a Normal-difficulty player experiences.** ×0.75 is the pak alone.
On Normal the boss chain does not *reach* a composite of 0.75 until monster level **75**. S1_PAK is
not "the Normal-difficulty composition"; **S2_FULL is.** But S2_FULL × Veteran is reachable, and that
is the reading the save's own difficulty byte supports.

---

## 1. Q1 — the pak stage: provenance traced completely

### 1.1 Where it lives, and how the engine reaches it

```
records/game/gameengine.dbr
    monsterAttributePak → records/game/balancingadjustment_mp+difficulty_enemies01.dbr
    playerAttributePak  → records/game/balancingadjustment_mp+difficulty_players01.dbr
    petAttributePak     → records/game/balancingadjustment_mp+difficulty_pets01.dbr
```
(M, `database.arz`.) Corroborated in `Game.dll` (M): `GameEngine::GetMonsterAttributePak`,
`GetPlayerAttributePak`, `GetPetAttributePak`, and the class `AttributePak` with its own
`GetOffensiveDamageAttributes(...)` / `GetCharAttributes(...)` accumulator entry points. **The pak is
an engine-level global applied to every monster** — which independently re-confirms the envelope
note's ruling that it is "not a peer of the skill-passive pool."

Template: `database/templates/attributepak.tpl`, `Class = AttributePak`.

### 1.2 The index scheme — 12 slots = 3 difficulties × 4 player counts

The decisive tell is `characterLifeMultModifier = [0, 90, 180, 270, 0, 90, 180, 270, 0, 90, 180, 270]`
(M) — a 4-cycle repeating 3 times, and 0/90/180/270 is transparently the 1-to-4-player multiplayer
health ramp. Every difficulty-varying field in the record moves in **blocks of 4**:

| field (enemies pak) | Normal (0–3) | Elite (4–7) | Ultimate (8–11) | grade |
|---|---|---|---|---|
| **`offensiveTotalDamageModifier`** | **−25** | **+25** | **+40** | **M** |
| `characterLifeModifier` | +50 | +320 | +580 | M |
| `characterDefensiveAbility` | +35 | +60 | +75 | M |
| `characterDefensiveAbilityModifier` | −15 | −8 | −8 | M |
| `characterAttackSpeedModifier` | −10 | 0 | 0 | M |
| `offensiveSlow*Modifier` (all DoT families) | −38 | −28 | −28 | M |
| `offensiveSlowDamageMultModifier` | 0 | +20 | +40 | M |
| `offensiveFreezeModifier` / `offensivePetrifyModifier` / `offensiveTrapModifier` | −20 | 0 | +10 | M |
| `offensiveStunModifier` | −30 | 0 | +25 | M |
| `offensiveAetherModifier` / `ChaosModifier` / `LifeModifier` | −20 | 0 | 0 | M |
| `offensivePierceModifier` | −8 | 0 | 0 | M |
| `defensiveReflectModifier` | −50 | −35 | −25 | M |
| `defensiveAbsorptionModifier` | −20 | −20 | −20 | M |

`Game.dll` names the selector: **`GameEngine::GetBalanceDifficulty()`** returning `unsigned int` (M).
Difficulty folder names in the binary are the Titan-Quest legacy triple **`Normal` / `Epic` /
`Legendary`** (M) — which is why the DBR field suffixes elsewhere read `Epic`/`Legendary`.

**So: the −25 % is not a mysterious global. It is `[Normal][1 player]` of a difficulty × party-size
table, and the same cell that yields −25 % yields +25 % on Elite and +40 % on Ultimate.**

### 1.3 Veteran and Ascendant are *mutators*, not difficulties

| record | archive | role | `offensiveTotalDamageModifier` | `characterLifeModifier` | grade |
|---|---|---|---|---|---|
| `balancingadjustment_challengemode_enemies01.dbr` | database | **Veteran** | **+40** (scalar) | **+140** | M |
| `balancingadjustment_ultramode_enemies01.dbr` | **GDX3** | **Ascendant** | **+165** (scalar) | **+850** | M |

Both are **scalars, not 12-arrays** — they are not difficulty-indexed; they are flat overlays.
`Game.dll` confirms the separate application path (M): `Mutator::GetAttributePak`,
`GameEngine::ContributeMutatorOffensiveDamageAttributes(...)`,
`GameEngine::ContributeMutatorCharAttributes(...)`, `GameEngine::FilterMutators(..., MutatorMode, ...)`.
Localisation binds the names (M): `tagChallengeDifficulty :: Veteran`;
`tagChallengeDifficultyDesc :: "Veteran Mode enhances Normal Difficulty ... Can be toggled on/off in
the main menu at any time."`; `tagChallengeDifficulty03 :: Ascendant`;
`tagDifficultyUltimateVeteran :: Ascendant Mode`.

Full Veteran enemy overlay (M): `characterLifeModifier +140` · `offensiveTotalDamageModifier +40` ·
`offensivePhysicalModifier +10` · `retaliationTotalDamageModifier +15` · `characterOffensiveAbility +25`
(+5 % mod) · `characterDefensiveAbility +15` (+5 % mod) · `characterAttackSpeed/SpellCastSpeed/RunSpeed
Modifier +5` each · `characterStrengthModifier +5` · **`spawnMaxAdj +1`** · **`spawnChampionMaxAdj +2`**.

---

## 2. Q2(a) — the pool stage: not difficulty-keyed, but a level ramp

### 2.1 What `armorbase0N` actually is

The Primordian record `records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr` (M) grants:

```
skillName3  = .../passive/armorbase05.dbr             skillLevel3 = charLevel*1
skillName1  = .../passive/damage_totaladjuster.dbr    skillLevel1 = (charLevel/25)+2
skillName2  = .../passive/damagebase_physical04.dbr   skillLevel2 = charLevel*1
charLevel   = charLevel*1+3
```

**`armorbase05`'s rank is the monster's own `charLevel`** (not `charLevel/4+1` — that equation drives
the *boss skills*, slots 6–10). Its `offensiveTotalDamageModifier` is a **200-entry array**, `−91 + rank`,
plateauing at **+25**:

| rank (= monster charLevel) | 1 | 13 | 18 | 45 | 55 | 75 | **88** | 100 | plateau |
|---|---|---|---|---|---|---|---|---|---|
| `armorbase05` (champ/hero/boss) | −90 | −78 | **−73** | −46 | −36 | −16 | **0** | +13 | +25 |
| `armorbase01/02` (trash) | −55 | −43 | −38 | −11 | +1 | … | — | +30 | +30 |

(M, `e1_unwind.py`.) `armorbase01/02` crosses zero at rank **56**; `armorbase03–06` at rank **88**.

**This reframes the whole "damper."** It is not a damper the designers bolted on to suppress monster
damage. It is a **normaliser against the base-damage curve**: `damagebase_physical04.offensivePhysicalMax`
runs 46 → 175 → 600 → 973 → 2,037 across the same rank range (M). `armorbase0N` bends that curve down
hard at low level and releases it progressively. Reading it at monster level 18 and calling the result
"×0.35" is accurate but tells you about *level 18*, not about the system.

`damage_totaladjuster` is a 6-entry array `[4, 8, 12, 16, 20, 24]` at rank `(charLevel/25)+2` (M) —
so +8 at charLevel 13–18, +12 at 25–49, +16 at 50–74, +20 at 75–99, +24 at 100+.

### 2.2 The unwind, quantified (the commission's explicit ask)

Composite outgoing factor = `(1 + Σpool/100) × (1 + pak/100)`, boss chain (M/C, `e1_unwind.py`):

| monster charLevel | pool | **Normal** | **Elite** | **Ultimate** |
|---|---|---|---|---|
| 13 | 0.30 | **0.2250** | 0.3750 | 0.4200 |
| **18 (referent)** | **0.35** | **0.2625** | 0.4375 | 0.4900 |
| 25 | 0.46 | 0.3450 | 0.5750 | 0.6440 |
| 45 | 0.66 | 0.4950 | 0.8250 | 0.9240 |
| 55 | 0.80 | 0.6000 | 1.0000 | 1.1200 |
| 75 | 1.04 | **0.7800** | 1.3000 | 1.4560 |
| 88 | 1.21 | 0.9075 | 1.5125 | 1.6940 |
| 100 | 1.49 | 1.1175 | 1.8625 | **2.0860** |

Trash chain (`armorbase01/02`): 0.4875 at cl 13 Normal → 0.7575 at cl 45 Normal → 2.1560 at cl 100 Ultimate.

**Two channels, one direction.** Between Normal-at-18 and Ultimate-at-100 the modifier chain alone
swings **×7.9** (0.2625 → 2.0860), *before* the base-damage curve's own ×11.6 growth. The
difficulty-keyed pak contributes ×1.87 of that; the level ramp contributes the rest.

### 2.3 Are monster levels themselves difficulty-keyed? — **corpus cannot fully close this**

What the corpus **does** say (M):
- All 32 `records/proxies/lvN_*.dbr` level-variance equations are **`averagePlayerLevel`-relative**
  and carry **only** a `Normal` suffix. There is **no `…EquationEpic` / `…EquationLegendary`** anywhere
  in 93,190 records. `lv6_hero` (the Primordian's) = `min (aPL+2)+(aPL/50)`, `max (aPL+3)+(aPL/50)`.
- A per-difficulty player-level clamp mechanism **exists but is dead**: `proxylimits.tpl` carries
  `min/maxPlayerLevelEquation{Normal,Epic,Legendary}` on 10 records (`limit_area000–008`,
  `limit_unlimited`), e.g. `limit_area001` = Normal 1–200 / Epic 40–60 / Legendary 80–100. **Its
  binding field `difficultyLimitsFile` appears on exactly ONE record in the entire corpus — and that
  record is `records/ui/mainmenu/mainmenu_creatureproxya01.dbr`, the main-menu background zombie** (M).
  Several `Legendary` clamps read 148–200 / 196–200, above GD's level cap of 100 — unretuned Titan
  Quest legacy. **This mechanism is not what re-levels GD monsters per difficulty.**
- `gameengine.dbr` carries `monsterLevelGapFixer = [0, 5, 7]` (M), difficulty-indexed;
  `Game.dll` exposes `Monster::GetCharLevelGapFixer`, `Character::…`, `Pet::…` (M). Semantics not
  recoverable from strings alone.

**Gap (U-1).** GD's per-difficulty region levels live in the world/level data (`Levels/*.map` inside
the `.arc` resources), **not** in the `.arz` database. I did not open them. So the *absolute* Elite /
Ultimate level of the Wightmire encounter is not corpus-derivable here, and I decline to import a
community number and present it as measured. **The §2.2 table is level-parameterised precisely so the
conductor can substitute any level reading without re-deriving anything.**

---

## 3. Q2(b) — is there any *other* difficulty-keyed damage multiplier?

**No. Complete enumeration, not a sample.** `gameengine.dbr` contains exactly **eight** 3-element
(difficulty-indexed) arrays across its 366 fields (M):

| field | Normal | Elite | Ultimate |
|---|---|---|---|
| `monsterLevelGapFixer` | 0 | 5 | 7 |
| `monsterAttackSpeedCapMin` | 20 | 30 | 40 |
| `monsterSpellCastSpeedCapMin` | 20 | 30 | 40 |
| `monsterRunSpeedCapMin` | 20 | 25 | 30 |
| `absoluteRunSpeedCapMin` | 40 | 30 | 20 |
| `monsterDefenseCap` | 100 | 100 | 100 |
| `playerDefenseCap` | 80 | 80 | 80 |
| `monsterSleepAggressionFalloffRate` | 0.25 | 0.25 | 0.25 |

**None multiplies monster damage or player damage-taken.** They are speed caps, defensive-ability
caps, an aggression rate, and a level-gap term. `pvpDamageMultiplier 0.20` and
`pvpCrowdControlDurationMultiplier 0.40` are scalars, PVP-only, not difficulty-indexed.

**Conclusion (C):** the *only* difficulty-keyed multiplier on monster outgoing damage in the entire
engine layer is `AttributePak.offensiveTotalDamageModifier`, plus the two flat mutator overlays
(Veteran +40, Ascendant +165). There is no second, hidden difficulty stage. The chain is closed.

---

## 4. Q3 — the calibration anchor, and a correction to community lore

The commission asked me to locate the community-known player resist penalty, on the theory that
finding it would map where difficulty-keyed combat modifiers live generally. **It does, and it lands
in the same record family — `balancingadjustment_mp+difficulty_players01.dbr`, wired at
`gameengine.dbr → playerAttributePak`** (M). That record contains **nothing but resistances**:

| player resist | Normal | **Elite** | **Ultimate** | grade |
|---|---|---|---|---|
| Fire, Cold, Lightning, Pierce, Poison | 0 | **−25** | **−50** | M |
| Aether, Chaos, Vitality (`defensiveLife`), Bleeding, Life-Leech (`defensiveSlowLifeLeach`) | 0 | **0** | **−25** | M |
| **Physical** | **absent from the record entirely** | — | — | M |

**This corrects the community shorthand.** The lore is "−25 Elite / −50 Ultimate, all resists." The
corpus says the penalty is **asymmetric**: only the five "top-row" resists take −25/−50; aether,
chaos, vitality, bleed and life-leech resist take **0/−25**; and **physical resist is never penalised
at all**. Tertiary corroboration is exact — the Grim Dawn wiki's Resistance page states *"on Elite the
top row resistances are hit for 25 %; in Ultimate that hit goes up to 50 % for the top, but it's only
25 % for the bottom (except for physical)"* (T).

**Why this matters more than the number:** it is an **independent validation of the §1.2 index
scheme**. The players pak has the same 12-slot layout, and reading slots 0–3 / 4–7 / 8–11 as
Normal / Elite / Ultimate reproduces a well-attested community fact *including its asymmetry and its
physical-resist exception*. The enemies pak's `[−25, +25, +40]` is read off the same ruler.

Two further confirmations of the ruler: the UI text tags are populated from these arrays —
`tagDifficultyDamage :: "* +{%d0}% Monster Damage"`, `tagDifficultyHealth :: "* +{%d0}% Monster Health"`,
`tagDifficultyResists :: "* {%d0}% Player Resistances"` (M) — and `difficulty_mastertable.dbr` binds
exactly the six buttons the pak layout implies: Normal / Veteran / Elite / Ultimate / UltimateVeteran,
plus a parallel Survival (Crucible) triple (M).

---

## 5. The finding the commission did not ask for — the referent was on **Veteran**

### 5.1 The measurement

Referent `.gdc`, `character_info` block (M):

```
isInMainQuest 0 · hasBeenInGame 1 · difficulty 128 · greatestDifficulty 0
money 7860 · compassState 3 · texture 'creatures/pc/hero02.tex'
```

`difficulty = 128 = 0x80`. **Not 0.**

**Parse alignment is independently corroborated**, twice. (i) `money` decodes as 7,860 and `texture`
as a valid asset path, so the byte cursor is not drifted. (ii) `ChrisElison/GDParser`'s
`CharacterReader.cs` declares the identical field order — `isInMainQuest, hasBeenInGame, difficulty,
greatestCampaignDifficulty, money, greatestCrucibleDifficulty, tributes` (M, read-only fetch).

### 5.2 The empirical cross-check

I parsed three third-party saves with the run's own parser (M):

| save | level | hardcore | **`difficulty`** | `greatestDifficulty` |
|---|---|---|---|---|
| `noquesthc.gdc` (fresh) | 1 | 1 | **0** | 0 |
| `Hellwrathh.gdc` | 100 | 0 | **2** | 2 |
| **referent `player.gdc`** | **13** | **0** | **128** | **0** |

**Third-party saves carry plain small indices — 0 for Normal, 2 for Ultimate. `128` is not a
difficulty index; it is difficulty 0 with bit 7 set** (C). GD's only per-character overlay on
difficulty 0 is **Veteran** (Ascendant would be `2 | 0x80 = 130`). `Game.dll` supplies the matching
API shape: **`GameInfo::GetGamePlusChallengeDifficulty()`** returning a single packed `unsigned int`,
and a `DisplayedDifficulty` enum distinct from `GameDifficulty` (M). Hardcore is a separate header
byte (=0); `difficultySkip` is a separate field (=0). Nothing else competes for the bit.

**Grade: C, high confidence.** I stop short of M because I have not seen a save known-by-provenance to
be Veteran. **That is the single cheapest way to close this** — see §7.

### 5.3 What Veteran does to the S-arm ceilings

Veteran multiplies monster outgoing damage by **×1.40** if the mutator is its own accumulator stage
(which the `ContributeMutator*` API shape suggests), or by **×2.14 at cl 18** if it pools into the
skill-passive pool. Applying both readings to the ceilings the discriminator note published (M/C,
`e2_veteran.py`):

| regime | ceiling | vs 260.498 | vs 273.704 |
|---|---|---|---|
| S1_PAK, no Veteran | 670.9 | reachable | reachable |
| **S2_FULL, no Veteran** | **252.9** | **short 2.9 %** | **short 7.6 %** |
| **S2_FULL + Veteran (separate stage)** | **354.1** | **REACHABLE** | **REACHABLE** |
| **S2_FULL + Veteran (pooled)** | **541.9** | **REACHABLE** | **REACHABLE** |
| S1_PAK + Veteran | 939.3 – 1,028.7 | reachable | reachable |

**The result is robust to the mutator-composition ambiguity: S2_FULL clears under both.** The 2.9 %
shortfall that the discriminator note correctly declined to call a falsification of S2_FULL, and that
was the sole mechanical basis for provisionally adopting S1_PAK, **does not survive the difficulty
byte.**

Note also the cost to S1: the discriminator's most persuasive positive evidence was the far-band nova
reproducing 269.66 against 273.704 "to the decimal." Under Veteran that fit becomes **377.5 — a 38 %
overshoot** (C). Veteran does not merely rescue S2; it **breaks S1's signature fit**.

### 5.4 The HP anchor is degenerate — it cannot arbitrate this

The envelope note's operator ruling rests on Primordian's measured `greatestMonsterKilledLifeAndMana =
15,822`, matched at 1.004× by the multiplicative rule at charLevel 18 *without* Veteran. Veteran's
`characterLifeModifier +140` would push that prediction to **38,138 (2.41× measured)** — apparently
fatal to §5.2.

**It is not, for two independent reasons.**

**(a) The save's own recorded monster level is 13, not 18.** `perDifficulty[0]` reads
`greatestMonsterKilledName tagSlithBossB02` — resolved via `Text_EN.arc` to **"Primordian, the
Forgotten One"**, and via the corpus to `slith_wightmirecave01.dbr` (M), so the attribution is
certain — with **`greatestMonsterKilledLevel = 13`**. The run derived charLevel 18–19 from
`lv6_hero` + the record's `charLevel*1+3` remap. The save disagrees with the derivation. And the
arithmetic is uncomfortably neat (C, `e2_veteran.py`):

> base HP required at level 13 **with** Veteran = **15,155**; back-solved base at level 18
> **without** Veteran = **36,531**; ratio **2.41×**. Veteran's life multiplier is **2.40×**.

**The two hypotheses predict the same HP to within 0.4 %.** "charLevel 18, no Veteran" and
"charLevel 13, Veteran" are numerically indistinguishable on this anchor. The 1.004 % fit is therefore
**not** evidence against Veteran — it is evidence that *one* of two compensating configurations holds.

**(b) Veteran is toggleable mid-playthrough.** `tagChallengeDifficultyDesc` (M): *"Can be toggled
on/off in the main menu at any time."* The difficulty byte records the state **at last save**, not the
state at every recorded event. `greatestMonsterKilledLifeAndMana` and `greatestDamageReceived` are
independent high-water marks set at different moments and **need not share a mutator state**. A
non-Veteran Primordian kill and a Veteran `greatestDamageReceived` are fully consistent with one save
file.

**Either way, the HP anchor does not refute Veteran, and the operator ruling it established is
untouched** — the multiplicative-vs-additive adjudication moved the prediction by 180 %, far outside
anything discussed here.

---

## 6. Q4 — the DECISION QUESTION, answered

> *"Is there a difficulty-conditional reading under which ×0.75 is what a Normal-difficulty player
> experiences?"*

**No.** ×0.75 is the pak stage in isolation, and the pak never appears in isolation: `armorbase0N` is
carried by **1,221 of 1,307 Monster records (93.4 %)** (M, prior work) and cannot be dropped for one
monster without dropping it game-wide. From §2.2, on Normal a boss-chain monster's composite reaches
0.75 only at **charLevel 75**; a trash-chain monster only at **charLevel 44**. Neither is within reach
of a level-13 character's world. **S1_PAK is not the Normal composition of anything.**

**The Normal-difficulty composition is ×0.2625 — S2_FULL — and the difficulty finding *strengthens*
that reading rather than rescuing S1.** Before this probe, ×0.2625 looked like a suspiciously harsh
number of unclear provenance. It now has a coherent design rationale: it is one cell of a
level-normalising ramp crossed with the Normal cell of a difficulty table, and it unwinds monotonically
and sensibly all the way to ×2.09 at Ultimate/level-100. **It is a designed value, not an artefact of
mis-composition.**

**So the paradox resolves — but by inverting the provisional ruling, not by confirming it:**

| | files compose to | world behaved like | reconciled? |
|---|---|---|---|
| Commission's framing | ×0.2625 | ×0.75 | difficulty gate hoped for |
| **This probe** | **×0.2625 × 1.40 (Veteran) = ×0.3675** | ceiling 354.1 ≥ 273.704 | **yes — S2_FULL + Veteran** |

**Recommendation to the conductor (advisory; the ruling is Matt's):**

1. **Re-open R-WR3-28.** Its stated basis — "S2 cannot produce the measured numbers from any
   reachable source" — is falsified by the Veteran mutator under both composition readings. This is
   not a marginal correction; it reverses the direction of the evidence.
2. **Adopt the difficulty-parameterised operator, not a scalar.** Carry
   `outgoing = base × (1 + Σpool(charLevel)/100) × (1 + pak[difficulty]/100) × mutators`, with §2.2 as
   the lookup. A single scalar damper was always going to mis-transfer to any other level or
   difficulty; the run should stop shopping for one.
3. **Do not port the ×0.2625 into engine work as "GD's damper."** It is the value at *one* level on
   *one* difficulty. The transferable design fact is the **shape**: GD normalises early-game monster
   damage with a per-level ramp that fully releases by the level cap, and layers a small
   difficulty multiplier (−25 / +25 / +40) on top. That shape is the reusable finding.

---

## 7. Unknowns, and what would close them

| id | unknown | what would settle it |
|---|---|---|
| **U-1** | Absolute monster levels per difficulty for a given region. Not in `.arz`; lives in `Levels/*.map` inside the `.arc` resources. | Parse the level `.arc`s (my `arc_text.py` already reads ARC v3 — the blocker is the `.map` payload schema, not the container), **or** one Elite/Ultimate save's `greatestMonsterKilledLevel`. |
| **U-2** | **Is `0x80` definitively the Veteran bit?** (Currently C, from: 128 is not a valid index; third-party saves read 0 and 2; `GetGamePlusChallengeDifficulty` packs game+challenge into one int; no other candidate flag.) | **Cheapest decisive test in this table:** one save known-by-provenance to be Veteran-on. Matt can produce this in ~2 minutes — start any character with Veteran toggled on, save, read the byte. **I recommend this before the conductor rules.** |
| **U-3** | Does the Veteran mutator compose as its own multiplicative stage (×1.40) or pool with the skill passives (×2.14 at cl 18)? | Immaterial to the verdict — S2_FULL clears under both — but it moves the *magnitude*. Would need a measured Veteran monster HP or hit. |
| **U-4** | The save records `greatestMonsterKilledLevel = 13`; the proxy chain derives charLevel 18–19. Is the field the monster's level, or something else (e.g. player level at kill, which was also 13)? | Cross-read the same field on a save where player level and monster level demonstrably differ. `Hellwrathh.gdc` (level 100) has an empty `perDifficulty` name, so it does not serve. |
| **U-5** | `monsterLevelGapFixer [0, 5, 7]` semantics. Difficulty-indexed and level-related, so potentially relevant to U-1. | Disassembly of `Monster::GetCharLevelGapFixer`, or in-game observation. |

**What I did *not* do, deliberately:** I did not import a community number for Act-1 Elite/Ultimate
monster levels and present it as a measurement. §2.2 is level-parameterised instead, so the conductor
can substitute any level reading without re-deriving anything.

---

## 8. Source list

**Primary — corpus (M).** `/Users/admin/Games/vendor/grim-dawn-edition-II-20260724/`:
`database/database.arz`, `gdx1/GDX1.arz`, `gdx2/GDX2.arz`, `gdx3/GDX3.arz` (93,190 records swept).
Records cited: `records/game/gameengine.dbr` · `records/game/balancingadjustment_mp+difficulty_{enemies,players,pets}01.dbr` ·
`records/game/balancingadjustment_challengemode_enemies01.dbr` · `records/game/balancingadjustment_ultramode_enemies01.dbr` (GDX3) ·
`records/skills/nonplayerskills/passive/armorbase01.dbr`, `…/armorbase05.dbr`, `…/damage_totaladjuster.dbr`, `…/damagebase_physical04.dbr` ·
`records/creatures/enemies/boss&quest/slith_wightmirecave01.dbr` ·
`records/proxies/lv6_hero.dbr`, `…/lv4_champion+.dbr`, `…/limit_area000–008.dbr`, `…/limit_unlimited.dbr` ·
`records/proxies/boss&quest/boss&questpools/p_wightmire_slitha01.dbr` ·
`records/ui/mainmenu/difficultywindow/difficulty_mastertable.dbr` and its label records.

**Primary — localisation (M).** `resources/Text_EN.arc` + `gdx1–3/resources/Text_EN.arc`, 20,245 tags.

**Primary — binary (M).** `/Users/admin/Games/vendor/grim-dawn/Game.dll`, exported-symbol strings
(`AttributePak`, `Mutator`, `GameEngine::GetBalanceDifficulty`, `GameInfo::GetGamePlusChallengeDifficulty`,
`Monster::GetCharLevelGapFixer`, `ContributeMutator*`).

**Primary — saves (M).** Referent `player.gdc`; and read-only fetches from
`github.com/ChrisElison/GDParser` — `noquesthc.gdc`, `Hellwrathh.gdc`, `playersoldier.gdc` (this last
fails our parser past the header; not used), and `CharacterReader.cs` for field-order corroboration.
Accessed 2026-07-30.

**Tertiary (T).** Grim Dawn wiki — Resistance page (Elite/Ultimate resist penalty asymmetry,
"except for physical") and Difficulty page; `grimdawn.com/guide/game-settings/game-difficulties/`
(Veteran is a toggle over Normal). Accessed 2026-07-30. Used **only** to corroborate §4; every number
in this note is corpus-sourced.

**Prior artifacts relied on.** `research/2026-07-30-gd-l13-reference-envelope.md` §2 (composition
operator, HP anchor 15,822, base-HP chain) · `research/2026-07-30-wr3-wave-blizzard-payloads.md` §1.3 ·
`research/2026-07-30-wr3-damage-discriminator.md` (ceilings 670.9 / 252.9, far-band nova 269.66).

**Scratch (this probe).** `agentic_orchestration/legolas/scratch/2026-07-30-wr3-diffprobe/e1_unwind.py`
(difficulty × level unwind tables), `e2_veteran.py` (Veteran re-basing, HP degeneracy).
Read-only throughout; nothing outside this deliverable and that scratch directory was modified.
