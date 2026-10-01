# Research — JOIN-1 J4a: D2 Whirlwind Barbarian formulas, primary rows, gear and C-12 — 2026-10-01

**Mode:** A (analytical; primary-source probe)
**Commissioner:** gandalf (Run JOIN-1, wave J4a research leg)
**Consumers:** gamora (the D2 adapter / conversion key) → star-lord (kit rows) → drax
**Version for every number unless flagged:** Diablo II: Lord of Destruction, **expansion game, 1.13 txt data** (`fabd/diablo2 @ 45112569deb9384738ccafe5c24ebbb71f41c7c9`). Where D2R differs, the entry says so.
**Sister packet (re-used, not redone):** `agentic_orchestration/legolas/research/2026-10-01-join1-d2-animation-timing/`

## Files

| File | What it holds |
|---|---|
| `formulas.json` | 15 formula entries (F01–F15). Each has a label, a version, at least two sources, the cross-check result, the D2R difference, conflicts and open items |
| `primary_rows.json` | Skills.txt rows 151 and 149 and every operand row, as verbatim DATAMINED strings; per-level tables for slvl 1–60, verified against Arreat and Basin; the kit's runewords and bases resolved in 1.13 tables; file sha256s |
| `c12_home_frontier.md` | Commission C-12: the candidate home frontier points, source quality, the verdict and the re-entry criterion |

**Labels** (defined in `formulas.json`):
- **DATAMINED:** read from the 1.13 txt files, or a structure read from D2MOO source.
- **MODEL-VERIFIED:** formula structure read from D2MOO (`ThePhrozenKeep/D2MOO @ 5596f5cb`) and confirmed by Arreat Summit and/or Basin Wiki. Where a published table exists, it was reproduced numerically.
- **(partial):** a named sub-clause has only one source, or the sources conflict on it.
- **INFERRED** and **UNKNOWN:** as stated in each entry.

A generator rebuilt every table and asserted each one against its second source; it aborts on any mismatch. All checks passed (`primary_rows.json` → `verification_log`).

---

## Summary

1. **15 formulas, 11 fully MODEL-VERIFIED and 4 partial.** No formula rests on a single source at its core. The partial sub-clauses are:
   - which dual-wield hand sets the Whirlwind cadence (F02);
   - whether Ignore Target's Defense works on champions (F11);
   - the "attacking weapon only" dual-wield rule for CB and DS (F08, F09);
   - whether on-kill effects fire during Whirlwind (F14).
2. **The primary rows are DATAMINED and every per-level table reproduces exactly.**
   - Whirlwind (row 151): damage% = **−50 + 8·(slvl−1)**, AR% = **5·(slvl−1)**, mana = **12 + 0.5·slvl**. It references **no other skill row**.
   - Battle Orders (row 149): **+35 + 3·(slvl−1)%** to life, mana and stamina, for **750 + 250·(slvl−1) + 125·(Shout.blvl + BC.blvl)** frames. Its operand rows are Shout (138) and Battle Command (155).
3. **The kit record does NOT pin the off-hand axe, or either weapon's IAS.** In LoD 1.13 the code gives Whirlwind's cadence to the **left-hand (off-hand) weapon** for most of a whirl (INFERRED from D2MOO). So the axe's own IAS − WSM sets the hit rate.
4. **C-12: SEARCHED-UNLOCATED for a timed point, so home margin is `DEFERRED`.**
   - A capability anchor exists at MEDIUM confidence: the build clears **Hell Chaos Sanctuary** (Levels Id 108).
   - Every timed benchmark found is D2R, and D2R changed both Whirlwind laws that set clear speed.

---

## 1. Formula list

| Id | Formula | Label | Version | Core sources |
|---|---|---|---|---|
| F01 | Whirlwind damage per attack: weapon (ED on base) + Damage+ → %pool (WW calc1 + off-weapon %Damage + Str bonus + mastery + demon/undead; floor −90) → ×SrcDam/128 → crit ×2 → elemental adds | MODEL-VERIFIED | LoD 1.13 | D2MOO SUnitDmg.cpp · Basin Damage/Enhanced_Damage · Arreat WW table |
| F02 | Whirlwind hit law: cadence (sister law), one target per attack, melee-range click → one normal Attack, **no chance-to-cast procs**, uninterruptible after the first hit, mana paid once per whirl, **left hand sets D** | MODEL-VERIFIED (partial) | LoD 1.13 | sister LAW_WW_CADENCE · D2MOO SkillBar.cpp/Player.cpp · Arreat · Basin |
| F03 | Battle Orders: %, duration, synergies; uses the same stat as item "+% Max Life" (op 11, additive), so not item Vitality | MODEL-VERIFIED | LoD 1.13 (D2R same) | Skills/ItemStatCost · D2MOO D2StatList.cpp · Basin · Arreat |
| F04 | Attack rating: 5·(Dex−7) + tohit + 20, × (1 + tohit%) | MODEL-VERIFIED | LoD 1.13 | D2MOO Units.cpp · Basin · CharStats |
| F05 | Chance to hit = clamp(200·AR/(AR+DEF)·alvl/(alvl+dlvl), 5, 95) | MODEL-VERIFIED | LoD 1.13 | D2MOO · Arreat · Basin |
| F06 | Physical: flat DR then DR%; monsters have no ceiling (≥100 = immune); players clamped to [−100, 50] | MODEL-VERIFIED | LoD 1.13 | D2MOO · Arreat · Basin |
| F07 | Elemental resistance: difficulty penalty 0/−40/−100 (DATAMINED); player cap min(75 + max, 95), floor −100; absorb cap 40; item −enemy-res does not break immunity | MODEL-VERIFIED | LoD 1.13 | D2MOO · DifficultyLevels.txt · Arreat ×2 |
| F08 | Crushing Blow: current HP / {4, 8 boss/superunique, 10 player} × (0.5 + 0.5·players), ×2 ranged; reduced by DR > 0 | MODEL-VERIFIED (partial) | LoD 1.13 | D2MOO SkillItem.cpp · Basin |
| F09 | Deadly Strike / CS / mastery crit: mutually exclusive ×2 physical | MODEL-VERIFIED (partial) | LoD 1.13 | D2MOO · Basin · ItemStatCost |
| F10 | Open Wounds: 200 frames, drain/frame piecewise in clvl, ½ vs champion/unique | MODEL-VERIFIED | LoD 1.13 | D2MOO · Basin (identity asserted for clvl 1–99) |
| F11 | Ignore Target's Defense / −% Target Defense | MODEL-VERIFIED (partial) | LoD 1.13 | D2MOO · Basin (**champion conflict**) |
| F12 | Life and mana scaling: Barbarian 55 + 2/level + 4/Vit; mana 10 + 1/level + 1/Energy; how BO and item % combine | MODEL-VERIFIED | LoD 1.13 | CharStats · D2MOO ops 8/9/11 · Basin |
| F13 | Leech: % of physical dealt × MonStats Drain% ÷ {1, 2, 3} by difficulty | MODEL-VERIFIED | LoD 1.13 | D2MOO · DifficultyLevels/MonStats · Arreat |
| F14 | Demon/undead %damage, Prevent Heal, on-kill effects, weapon auras | MODEL-VERIFIED (partial) | LoD 1.13 | D2MOO · Basin · Runes/Properties |
| F15 | Normal-attack fallback, FCR, FHR, Whirlwind walk speed | MODEL-VERIFIED | LoD 1.13 | sister packet laws |

---

## 2. Primary rows (`primary_rows.json`)

### Row 151, Whirlwind

| Field | Value |
|---|---|
| srvst / srvdo | 38 / 76 |
| Animation | anim SQ, seqtrans A1, seqnum 10 |
| Weapons | weapsel 2, itypea1 `mele` |
| Mana | mana 25, lvlmana 1, manashift 7, minmana 1 |
| Damage | calc1 `ln12` with Param1 −50, Param2 8; SrcDam 128 |
| Attack rating | LevToHit 5 |
| Other | Param3 1 ("attacks per tick"); AttackNoMana 1; UseAttackRate empty; no synergy |

### Row 149, Battle Orders

| Field | Value |
|---|---|
| srvdo | 68 |
| Missile | `battleorders` (Vel 30, Accel −500, Range 15) |
| Aura stats | item_maxmana_percent, item_maxhp_percent, skill_staminapercent; all `ln34` with Param3 35, Param4 3 |
| Duration | auralencalc `ln12 + (Shout.blvl + Battle Command.blvl)·par8`, with Param1 750, Param2 250, Param8 125 |
| Mana | mana 7, manashift 8 |
| Animation | SC / SC |

### Operand rows

| Source | Row | What it supplies |
|---|---|---|
| Skills.txt | Shout (138) | BO duration synergy (blvl) |
| Skills.txt | Battle Command (155) | BO duration synergy (blvl) |
| Missiles.txt | `battleorders` | BO's area wave |
| SkillDesc.txt | `whirlwind`, `battle orders` | tooltip formulas |
| SkillCalc.txt | ln12, ln34, dm56 | formula definitions |
| ItemStatCost.txt | the BO aura stats and the vit/energy → life/mana links | how BO's % is applied |
| CharStats.txt | Barbarian | life/mana scaling operands |
| DifficultyLevels.txt | all rows | resist penalty, leech divisors |

**DifficultyLevels.txt is not in the local `raw/` dir.** It was fetched from the same fabd commit; its sha256 is recorded.

### Per-level tables

**The kit record uses no levels.** It pins no slvl, clvl or +skills, so slvl 1–60 tables are given. Key rows:

| slvl | WW damage % | WW AR % | WW mana | BO % | BO duration, no synergy |
|---|---|---|---|---|---|
| 1 | −50 | 0 | 12.5 | 35 | 30 s |
| 20 | +102 | +95 | 22 | 92 | 220 s |
| 30 | +182 | +145 | 27 | 122 | 320 s |

**D2R Whirlwind differs:** damage = 5·slvl + 25 and AR = 5·slvl + 45 (Basin).

**Considered and excluded:**
- **Sword Mastery 127 and Axe Mastery 128.** They are referenced by mechanism, not by the row or the kit record. Their data is included as `excluded_but_mechanism_relevant`. Because of `passiveitype`, a sword + axe loadout gets mastery on one hand only.
- **Berserk 152:** a scaffold variant only.
- **Leap Attack and Concentrate:** prerequisites only.
- **States.txt:** not acquired.

### Gear rows

The runewords and bases the kit record names are resolved in 1.13 Runes.txt + Gems.txt + Weapons.txt.

⚑ **1.13 Runes.txt has no row named "Grief".** Grief is row key `Runeword47`, identified by its runes Eth-Tir-Lo-Mal-Ral and its properties. Its "Rune Name" column reads "Widowmaker".

1.13 Grief:
- +340–400 damage;
- 30–40% IAS;
- ignore target defense;
- 1.875·clvl % damage to demons;
- −20–25% enemy poison resistance;
- +10–15 life per kill;
- 35% chance for Venom on striking;
- rune mods: −25% target defense, +2 mana per kill, 20% Deadly Strike, prevent monster heal, 5–30 fire damage.

---

## 3. Gear and IAS: open question 1 of the timing packet

**Answer: the kit record does not pin it.**
- The record names exactly one weapon with a base: **"Grief Phase Blade (mandatory damage)"**, and no IAS roll for it.
- It lists Fortitude, Enigma, Breath of the Dying, Death, Beast, Last Wish, Insight (merc) and Obedience **with no slot and no base**.
- It names **no off-hand at all**.
- The "sword main-hand + axe off-hand" loadout is **Matt's ruling in the Godot sprite contract** (`reincarnated-godot/docs/join1-sprite-cell-contract-2026-09-29.md`), not the kit record.

**What the gear would have to be** (LoD 1.13, Whirlwind cadence D from each weapon's own IAS − WSM; computed with the sister law):

| Weapon | Base WSM | Weapon IAS | WW D (ticks) | Weapon IAS needed for D = 4 |
|---|---|---|---|---|
| Grief **Phase Blade** (main, right) | −30 | 30–40 | **4** | ≥ 4 (any Grief roll) |
| Grief **Berserker Axe** | 0 | 30–40 | **6 at 30–33, 4 at 34–40** | ≥ 34 |
| Beast Berserker Axe | 0 | 40 | 4 | ≥ 34 |
| Breath of the Dying Berserker Axe | 0 | 60 | 4 | ≥ 34 |
| Death Berserker Axe | 0 | 0 | **8** | ≥ 34 (unreachable: Death has no IAS) |
| Last Wish Berserker Axe | 0 | 0 | **8** | ≥ 34 (unreachable) |

**Axe-legal kit runewords** (Runes.txt itypes): Grief, Death, Beast, Last Wish, and BotD (any weapon). **The record names no axe base.** Berserker Axe is the community standard: Maxroll lists Beast Berserker Axe and BotD Berserker Axe, and the D2R Uber Tristram video in C-12 runs Grief + Beast.

**Why the off-hand matters more than it looks** (F02, INFERRED from D2MOO):
- Whirlwind with `weapsel=2` picks the right-hand item, or the left-hand item when skill flag 0x2000 is set.
- The flag clears at whirl start and toggles after every attack.
- After the single tick-4 attack, two attacks per check leave the flag set. So **the left-hand weapon computes D for the rest of the whirl**, while both hands keep finding targets.
- A Death or Last Wish axe in the off-hand would therefore halve the hit rate (D 8 vs 4), even beside a Grief Phase Blade.

**To pin, Matt or the conductor needs to choose:**
1. the off-hand runeword and base;
2. the Grief IAS roll on each Grief;
3. whether the profile takes one mastery or two.

---

## 4. C-12: the home frontier point

See `c12_home_frontier.md`. **Verdict: SEARCHED-UNLOCATED for a timed point, so home margin is `DEFERRED`.** The re-entry criterion is printed there for the fidelity-cost table.

**Best evidence:**
- **Capability, MEDIUM:** Hell Chaos Sanctuary is the build's farm (Maxroll S14, the kit record's own citation, plus independent forum reports).
- **Best gear match:** Hell Chaos /players 8 "under 4 minutes" with Fortitude + double Grief. This is **hearsay**, D2R 2.5.
- **Hardest content:** Uber Tristram "under 3 minutes" with Grief + Beast. This is a **single YouTube title claim**, D2R S13, from an unknown channel.

All timed points are D2R, and D2R changed both Whirlwind damage% and the cadence law.

---

## 5. Open questions

| # | Question | What would settle it |
|---|---|---|
| Q1 | The off-hand runeword and base, both Grief IAS rolls, and one mastery or two (§ 3) | Matt or the conductor pins the loadout |
| Q2 | **Left hand sets the WW cadence** is INFERRED from D2MOO (a 1.10f reconstruction) | 1.13 capture: dual-wield a fast and a slow weapon, swap hands, frame-count the checks |
| Q3 | **Does ITD work on champions?** Basin says no; D2MOO's exclusion mask omits champions | 1.13 test vs a high-defense champion pack, or read the 1.13 D2Game binary |
| Q4 | Last Wish crushing blow: 1.13 Runes.txt says **40–50%**; Basin lists 60–70% | Conductor: confirm the 1.13 value governs (it is the pinned data) |
| Q5 | Do +life/+mana-after-kill (Grief, Enigma, Tir) fire on Whirlwind kills? | 1.13 test |
| Q6 | Mana paid once per whirl rests on D2MOO only | Capture |
| Q7 | MonStats `Drain(H)` is blank for `diablo` and `ubermephisto`. Under D2MOO that means no leech | 1.13 test |
| Q8 | If the profile carries Beast (Fanaticism lvl 9) or Last Wish (Might lvl 17), those aura rows (Skills 122, 98) become operands. Not pulled here | Conductor's loadout pin |
| Q9 | The kit record pins no slvl, clvl or attributes; every number above is a function of them | Model owner or conductor |
| Q10 | **Version.** The kit record's eras include D2R, and its own citations (Maxroll, DiabloBytes) are D2R guides; the data is 1.13 LoD. This packet uses the 1.13 law (as the sister packet's Q6) | Conductor confirms LoD 1.13 as JOIN-1's law |
| Q11 | States.txt was not acquired | Fetch from the same fabd commit if the adapter needs state flags |
| Q12 | DifficultyLevels.txt is used by F07 and F13 but is absent from the local `raw/` dir and its manifest | elrond, J-S7 manifest: consider adding it, sha256 `aaa1a5d9…` |
| Q13 | CharStats `ManaRegen = 120`: meaning not code-verified | D2MOO regen code or Basin Mana regeneration |

---

## Source list (accessed 2026-10-01)

**Primary**
- D2 1.13 txt tables, `fabd/diablo2 @ 45112569`: Skills, SkillDesc, SkillCalc, Missiles, CharStats, ItemStatCost, Properties, Runes, Gems, Weapons, MonStats, Levels, MonLvl.
  - Local copy: `agentic_orchestration/research/datamine-acquisition/d2/raw/`.
  - DifficultyLevels.txt from `https://raw.githubusercontent.com/fabd/diablo2/45112569deb9384738ccafe5c24ebbb71f41c7c9/code/d2_113_data/DifficultyLevels.txt`.
  - sha256 for every file is in `primary_rows.json`.
- D2MOO @ `5596f5cb6c5251a0a07c6637d26458b06099d516` (the same commit the sister packet read): https://github.com/ThePhrozenKeep/D2MOO. Files read:
  - D2Game: `UNIT/SUnitDmg.cpp`, `SKILLS/SkillBar.cpp`, `SKILLS/SkillItem.cpp`, `SKILLS/Skills.cpp`, `PLAYER/Player.cpp`, `MONSTER/Monster.cpp`, `MONSTER/MonsterUnique.cpp`;
  - D2Common: `D2Skills.cpp`, `D2StatList.cpp`, `Units/Units.cpp`, `Items/Items.cpp`, `include/D2Monsters.h`, `include/D2Composit.h`.

**Secondary**
- The Arreat Summit (Blizzard):
  - Barbarian Combat Skills: https://classic.battle.net/diablo2exp/skills/barbarian-combatskills.shtml
  - Warcries: https://classic.battle.net/diablo2exp/skills/barbarian-warcries.shtml
  - Basics, Characters: https://classic.battle.net/diablo2exp/basics/characters.shtml
  - Resistances: https://classic.battle.net/diablo2exp/basics/resistances.shtml
  - Difficulty: https://classic.battle.net/diablo2exp/basics/difficulty.shtml
- Basin Wiki, https://www.theamazonbasin.com/wiki/index.php?title= with these pages: Whirlwind, Battle_Orders, Crushing_Blow, Deadly_Strike, Open_Wounds, Attack, Damage, Damage_Reduced, Damage_Resist, Enhanced_Damage, Ignore_Target%27s_Defense, Life, Mana, Barbarian_(Diablo_II), Attack_Rating, Defense.
- Maxroll, Teo1904, Whirlwind Barbarian Endgame Build Guide (D2R S14): https://maxroll.gg/d2/guides/whirlwind-barbarian-guide

**Tertiary:** C-12 forum and video sources, listed in `c12_home_frontier.md`.

**Project inputs (read-only):**
- `gandalf/notes/2026-09-29-join-1-run-charter.md` (v0.5)
- `gandalf/notes/2026-09-28-join-key-architect-pass.md` § 8
- `research/curated/kits-export/d2-ww-barb.json`
- the sister packet
- `reincarnated-godot/docs/join1-sprite-cell-contract-2026-09-29.md` (loadout line only)
