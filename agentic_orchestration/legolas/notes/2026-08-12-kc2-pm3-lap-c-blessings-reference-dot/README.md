# KC2-PM3 — Lap C: measured blessings · measured reference truth · DoT semantics

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Conductor:** gandalf (`RUN-CONDUCTOR`) · **2026-08-12**
**Charter:** `agentic_orchestration/gandalf/notes/2026-08-12-kc2-pm3-run-charter.md` (Lap C row)
**Mode:** read-only primary-source probe. Two substrates, both frozen:
the Edition-III GD corpus (`/Users/admin/Games/vendor/grim-dawn-edition-III-20260808`, 84,829
record paths, 8-archive last-wins overlay via `s2_lib.E3`) and the reference capture
(`/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4`,
1,034.100 s, 1920×1080, h264, 60 fps).
**Laws honoured:** GL-12 decode-never-estimate · NOTE-9 every quantity asserts its population ·
instrument schemas declared in the scripts' own docstrings · cliffs named, never improvised past.

---

## THE THREE HEADLINES

### 1. Matt bought **no blessings**. He bought **four defences** — and they were the arena's entire capacity.

Measured from pixels, not genre knowledge. The tribute counter steps **145 → 140 → 135 → 130 → 125**
at video **t = 477 / 484 / 502 / 510 s**, and the Defense-Site dialog visible in each of those frames
names what was being bought. In order:

| # | video t | purchase | record | cost |
|---|---:|---|---|---|
| 1 | 477 | **Deathchill Beacon** | `records/creatures/defenses/turret_ice.dbr` | 5 Tributes + 10,000 Iron Bits |
| 2 | 484 | **Stormcaller Beacon** | `records/creatures/defenses/turret_lightning.dbr` | 5 + 10,000 |
| 3 | 502 | **Inferno Beacon** | `records/creatures/defenses/turret_fire.dbr` | 5 + 10,000 |
| 4 | 510 | **Vanguard Banner** | `records/creatures/defenses/banner_offense.dbr` | 5 + 10,000 |

Identity is a **game-authored join**, not a name match: each creature's `description` field is a
localization tag (`tagDefense_Turret02` → "Deathchill Beacon", `tagDefense_Turret03` → "Stormcaller
Beacon", `tagDefense_Turret01` → "Inferno Beacon", `tagDefense_Banner02` → "Vanguard Banner") and
each dialog's prose matches its record's contents exactly (the Deathchill text promises *"slowing
their advance and reducing Offensive Ability, with a chance to freeze"* — `turretice_icebolt.dbr`
carries `offensiveSlowRunSpeed`, `offensiveSlowOffensiveAbility` and `offensiveFreezeChance = 50`).

Corroboration that this is the **complete** purchase set: the tribute counter does not move again
for the remaining **358 s** of the capture (t = 510 → 868, change-detector threshold 3.2 on the
counter crop over 539 consecutive frame-pairs, t = 400…939; the only supra-threshold events in that
whole window are the arena load-in at t = 424–446, the four purchases, and the death screen at
t = 868–874). The Crucible awards tribute only at tier boundaries and at run end
(`survival/rewards.lua :: playerTierTributesGlobalMP` / `playerTributesGlobalMP`), and he died
inside tier 16, so no income and no further spend.

**⚑ Charter consequence.** The re-based ranking's item #1 — *"Crucible tribute blessings + banner —
the largest un-modeled term"* — resolves as **four defence-site constructions and zero celestial
blessings.** `Blessing of Ulo` / `Empyrion's Guidance` / `Might of Amatok` / `Ulzuin's Pact` were
**not** in the reference run. The matrix's BLESSINGS-ON arm therefore models a *counterfactual*, not
Matt. The four blessings are decoded anyway and shipped in the same CSV, flagged
`[NOT PURCHASED - measured]`, so the arm can be run — but its result is not a comparator against the
reference. **The reference run is BLESSINGS-OFF, DEFENCES-ON.**

**⚑ Second charter consequence — the fold is much smaller than the ranking assumed.** Of 182 decoded
effect rows on the four purchases, exactly **6 land on the player**: the Vanguard Banner's aura, and
only inside an **8 m radius**.

| what the player actually gets | value | condition |
|---|---:|---|
| `characterOffensiveAbility` | **+80** | within 8 m of the Vanguard Banner |
| `characterOffensiveAbilityModifier` | **+4 %** | ″ |
| `offensiveTotalDamageModifier` | **+100 %** | ″ |
| `retaliationTotalDamageModifier` | **+100 %** | ″ |

Rank is EXACT and free of assumptions: `banner_offense.dbr` grants `banneroffense_aura` at
`skillLevel3 = 1` — a literal, so the 2-entry arrays read at index 0 with no parameter.
The game's own tooltip for it (`tagDefense_Banner02_Skill01Desc`) reads *"The Banner fills you with
rage, increasing % Offensive Ability, % Crit damage and % All damage."*
The three beacons give the player **nothing**; they are independent stationary allied entities
(`Class = Monster`, `ControllerStationaryMonster`, `ViewDistance = 24 m`) with their own HP and
their own output at enemies. Their effect on survival is *kill throughput and enemy debuffs*, not
player stats.

**The four defences are POSITIONAL and FIXED.** The Crucible's own Lua declares exactly four defence
points in the arena (`mods/survivalmode/resources/Scripts.arc :: game/survival/defenses.lua`,
`defensePointId = {0,0,0,0}`; state enum `0 none / 1 BannerDefense / 2 BannerOffense / 3 TurretFire /
4 TurretIce / 5 TurretLightning / **6 Wall**`), spawned at the site's own coordinates via
`Character.Create(dbr, CharacterCreateArgs())`. Matt filled all four. This is the direct interaction
with the PM-3 CLUSTER movement policy: **a density centroid that drifts more than 8 m from the
Vanguard Banner costs the player +100 % damage, and one outside ~24 m of a beacon costs its fire.**

### 2. Reference truth pinned: **died on wave 160.** Not 159.

Matt remembered "159 or 160". The HUD carries a persistent wave counter (red digits left of the
minimap, box `(1580, 134, 64, 34)`), classified per-second by template IoU over 218 frames:

| wave | start (video s) | elapsed | duration | terminal |
|---:|---:|---:|---:|---|
| 151 | 682 | 0 | 16 | CLEARED |
| 152 | 698 | 16 | 17 | CLEARED |
| 153 | 715 | 33 | 15 | CLEARED |
| 154 | 730 | 48 | 14 | CLEARED |
| 155 | 744 | 62 | 16 | CLEARED |
| 156 | 760 | 78 | 20 | CLEARED |
| 157 | 780 | 98 | 19 | CLEARED |
| 158 | 799 | 117 | 14 | CLEARED |
| 159 | 813 | 131 | 26 | CLEARED |
| **160** | **839** | **157** | **29** | **DEATH** |

Fight window **682 → 868 s = 186 s**, ten waves, duration min/median/max **14 / 17 / 29 s**.
Fight start is `Lokarr, Master of the Crucible` with **"Start on Wave 150"** highlighted under the
cursor at t = 680; the counter flips 0 → 151 at t = 682. Death is a fade-to-black at t ≈ 868
(6 fps sub-sample puts the fade onset in [867.8, 868.2]); at t = 880 the on-screen objective reads
**"You have failed, your Compensation awaits in the Treasure Chamber"** with the counter still on
160. `evidence/t880-you-have-failed-wave-160.jpg`.

**⚑ The gap the run is trying to close is therefore 4 waves, not 3–4: sim dies wave 156 (5 cleared),
Matt died wave 160 (9 cleared).** And the pacing curve is now a real comparator — the reference
player was clearing a wave every ~17 s and *slowed sharply on his last two* (26 s, then 29 s to
death), which is the signature a survival curve should be checked against, not just the terminal
wave number.

Wall-clock cross-check (IS-V2): the HUD clock reads 9:45:15 PM at t = 470, and 21:37:25 + 470 s =
21:45:15 **exactly** — video time is 1× real time with zero drift. Death wall-clock 21:51:53.

### 3. DoT audit: **R-PM2-1 was RIGHT — and is now measured, not defaulted.** Three corrections found.

Full argument in `dot-semantics.md`. Summary:

* **SEM-1 RATIFIED.** GD composes a DoT line from `DamageDurationPoison` (" Poison Damage") +
  `DamageSingleFormatTime` (" over {N} Seconds"). A number printed *over N seconds* is a **total**.
  The PM-2 fold's `dot_dps_if_field_is_total` reading is correct; no change to gamora's arithmetic.
* **CORRECTION A — resistance cap decoded, Lap A gap G-2 CLOSED.**
  `records/game/gameengine.dbr :: playerDefenseCap = [80, 80, 80]`. The fold applied the sheet's
  **85 %** bleed resistance uncapped. Clamped to 80 ⇒ **bleed damage taken ×1.333**. (Residual
  CLIFF C-3: whether the sheet prints pre- or post-cap is UI behaviour, undecodable — flagged for
  conductor sign-off rather than silently applied.)
* **CORRECTION B — `aetherialcorruption_rotskin` is a toggled damaging AURA, not a swing.**
  `Class = Skill_BuffAttackRadiusToggled`, `skillTargetRadius = 3.5 m`, template carries
  `skillActiveManaCost` / `skillActiveLifeCost` (per-second upkeep = sustained toggle). PM-2
  consumed it as an `initial`-slot attack on the one-slot-per-opportunity clock, which both
  displaced the carrier's weapon swing and mis-shaped the aura. Net direction is not decidable
  (tick rate is engine-side, CLIFF C-4b) but the geometry is: **continuous, positional, 3.5 m** —
  and 4–5 distinct carriers sit on this roster.
* **CORRECTION C — the duration axis is missing from the fold.** `tagCharStatsPoisonDurationInfo`:
  *"The percent bonus to the duration … **The damage per second is not increased.**"* ⇒ total scales
  with duration. Harmless for the reference run (the measured sheet carries **no** defensive
  duration-reduction row) but **not** harmless for a BLESSINGS-ON arm: `blessingulo_buff` grants
  `defensivePoisonDuration = 50`, a flat halving of incoming poison *total* on top of 80 % resistance.
* **RATIFIED, no change:** PM-2 §A.1's `Poison`→acid and `Life`→vitality joins. `DefensePoison` is
  literally *"Poison & Acid Resistance"* — one stat covers the instant and the DoT half.
* **STACKING — address found, function not.** `gameengine.damageMagnitude = 100.0`, template
  description *"Decreasing same type duration damage"*. The rule's form is engine-side (CLIFF C-4).
  **Ruling for gamora: do not model a stacking rule**; keep per-application summation and carry the
  over-read on the wire.

Bonus corroboration for the sim's own constants: `gameengine.meleeTargetDistance = 2.4` — the sim's
`locomotion.D_ENGAGE_M = 2.4 m` is not a convention, it is Crate's number.

---

## FILE MAP

| file | grain | rows |
|---|---|---:|
| `measured-blessing-sheet.csv` | one row per granted stat effect | **259** |
| `measured-reference-truth.csv` | one row per fought wave | 10 |
| `measured-reference-events.csv` | one row per pinned setup/fight event | 9 |
| `dot-semantics.md` | deliverable 3, prose + citations | — |
| `evidence/*.jpg` | 9 in-frame crops backing every video-measured claim | — |

**Instruments** (`agentic_orchestration/research/scripts/`, schemas declared in their docstrings):

| script | what it does |
|---|---|
| `pm3c_video_2026_08_12.py` | frame basis, region boxes, MAD change-detection, contact sheets (IS-V1…IS-V4) |
| `pm3c_blessings_2026_08_12.py` | decodes the four purchases + the four blessings → `measured-blessing-sheet.csv` (IS-B1…IS-B5) |
| `pm3c_reference_2026_08_12.py` | emits the wave timeline + event table (IS-R1…IS-R4) |

All three import Lap B's `pm2b_lib_2026_08_12` / `s2_lib` unchanged — **the corpus basis, overlay
order and offensive-taxonomy derivation are inherited, not restated.** No instrument was rebuilt.

### `measured-blessing-sheet.csv` — column contract

`purchase_n` (1–4 = bought at that video second · 0 = decoded-but-NOT-purchased blessing) ·
`purchase_name` · `purchase_video_t` · `tribute_cost` · `ironbits_cost` · `source_record` ·
`source_display_name` (from the record's own localization tag) · `effect_record` ·
`effect_archives` (which of the 8 archives carry it) · `effect_display_name` ·
`effect_description` (the game's own tooltip) · `stat` · `stat_group` (from
`templatebase/parameters_offensive.tpl`, derived not hand-listed) · `stat_kind` ·
**`value_at_rank`** · `value_raw_array` (the full array, so any rank can be re-read) ·
**`applies_to`** · **`delivery`** · `rank_equation` · `rank_used` · `skill_active_duration_s` ·
**`rank_basis`** · `note`.

### Rank-basis census (NOTE-9 — this is the population every value above asserts)

| basis | rows | meaning |
|---|---:|---|
| `SCALAR` | 177 | rank-invariant field; no resolution needed |
| `ARRAY[200]@rank100:EXACT` | 24 | `armorbase03` on the defence body, `skillLevel2 = charLevel*1` |
| `EQUATION@charLevel=100` | 36 | the defence's own bio equations (life/DA/OA), evaluated |
| `ARRAY[60]@rank26:EXACT` | 12 | turret output, `skillLevel3 = charLevel/4+1` → 26 |
| `ARRAY[2]@rank1:EXACT` | 5 | **the Vanguard Banner aura — literal rank, zero assumptions** |
| `ARRAY[60]@rank1:EXACT` | 1 | `passiveproperties_defense` on a banner (`skillLevel1 = 1`) |
| `DECLARED-ABSENT` | 4 | tier-2/3-only contracts that were **not** bought — named, not missing |
| **total** | **259** | of which 182 on purchased items, 73 on the not-purchased blessings |

`applies_to` census (rows carrying a stat): the defence object itself **148** · enemies **28** ·
**allies in radius (i.e. the player) 6** · player-self (blessings, counterfactual) 42 · pets only 31.
20 distinct effect records reached.

The 4 `DECLARED-ABSENT` rows are the tier-2/3 upgrades Matt did not buy, named so no downstream
consumer mistakes their absence for a decode failure: `banneroffense_frenzy` (the +35 % total-speed
pulse — banner tier 2+), `turretice_chillingsurge`, `turretfire_firestorm`,
`turretlightning_stormcaller`.

---

## CLIFFS

| id | cliff | status |
|---|---|---|
| **C-1** | resistance evaluated per-tick vs on-application | undecodable read-only; **inert** while player resistances are fight-constant |
| **C-2** | a player-built defence's `charLevel` binding — the Lua calls `Character.Create(dbr, CharacterCreateArgs())` with no level, so the turret rank equation `charLevel/4+1` has an unbound input. **Declared basis `charLevel = 100`** (player level, MEASURED off the main-menu card at t = 30) → rank 26. The full 60-entry arrays ride in `value_raw_array` so gamora can re-read at any rank without re-running me. |
| **C-3** | does the GD character sheet print pre- or post-cap resistance? (bears on the 85 → 80 bleed clamp) | UI behaviour; **flagged, not applied** |
| **C-4** | `damageMagnitude = 100.0` → the same-type-DoT decreasing function | engine-side; **do not model** |
| **C-4b** | toggled-aura tick period | engine-side; fold the 3.5 m geometry, declare the rate |
| **C-5** | the pristine save's `currentTribute = 999` does not reconcile with the video's 145 at arena load. The video is primary per the charter and its internal arithmetic closes exactly (145 − 4×5 = 125), so this is a **save-snapshot provenance question, not a measurement conflict**. Not chased. |

**Nothing in this lap was improvised past a cliff.** Where the corpus is silent the silence is a row.
