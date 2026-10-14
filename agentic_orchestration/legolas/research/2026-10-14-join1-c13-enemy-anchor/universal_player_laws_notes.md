# C-13 / KP-426: universal player laws for both D2 kits (LoD 1.13), provenance notes

**Scope:** what monsters do *to* the Fire Sorceress and the WW Barbarian: control effects received, chill, poison and other damage over time received, stamina, Barbarian mana regeneration, life regeneration and Replenish Life, and the Barbarian's belt.

**Files**
- `universal_player_laws.json` holds the data.
- `scripts/universal_player_laws.py` regenerates it. The script asserts every table value and every code line it relies on against the captured second source, and aborts on any mismatch. Two runs produced byte-identical output.
- Run with `python3 scripts/universal_player_laws.py`. It writes no bytecode when `PYTHONDONTWRITEBYTECODE=1` is set.

**Sources**
- **1.13 data:** `fabd/diablo2 @ 45112569` (the local J-S7 copy). Tables used: CharStats, ItemStatCost, DifficultyLevels, Armor.
- **Game code:** D2MOO @ `5596f5cb`, which is a reconstruction of version 1.10f, not 1.13.
  - `captures/d2moo-SUnitDmg.cpp`
  - `captures/d2moo-Units.cpp`
  - `captures/universal/d2moo-PlrModes.cpp`
- **Basin wiki:** 19 raw pages in `captures/universal/`.
- **Arreat Summit:** `basics/resistances`, plus `captures/potions/arreat-basics-characters.shtml` and `arreat-items-*-belts.shtml`.
- **Kit record:** `research/curated/kits-export/d2-ww-barb.json`.
- The sha256 of every input is in the JSON under `inputs_sha256`.

**Grades**
- **DATAMINED:** read directly from a txt table or the kit record.
- **MODEL-VERIFIED:** the structure comes from the D2MOO code and at least one community source confirms it.
- **INFERRED:** one source only, or shown by the code only through absence.

## The laws

| # | Law | Grade |
|---|---|---|
| 1a | **Stun on a player** is capped at 250 frames (10 s) and is not scaled by difficulty. The player is **not incapacitated**: any hit landing during the stun forces hit recovery, even a zero-damage hit. The latest stun replaces whatever length remains. | MODEL-VERIFIED (code, Basin Stun_length) |
| 1b | **Players have no frozen-solid state in PvM.** Freeze length and Freezes Target applied to a player both become **chill**. Only normal and minion monsters are frozen. | MODEL-VERIFIED (code `ApplyFreezeState`, Basin Freeze_length, Basin Freezes_Target) |
| 1c | **No Hell or PvM duration halving for players.** DifficultyLevels `MonsterColdDivisor` and `MonsterFreezeDivisor` (Nightmare 2/2, Hell 4/4) apply only when a monster is the target. Against a player, the Hell **−100 resist penalty** enters the length reduction instead (see 2b), so an under-resisted player is chilled **longer**, up to ×2. | MODEL-VERIFIED (code, Basin Cold_Damage, Basin Cold_Resist) |
| 1d | **Cannot Be Frozen** sets the hit's cold and freeze length to 0. **Half Freeze Duration** halves them once and does not stack. Both are applied before resistance, so CR 75 % plus HFD gives ⅛ length. Neither one stops Holy Freeze or Decrepify. | MODEL-VERIFIED (code, Basin, Arreat) |
| 1e | **Knockback:** the player is pushed back and goes into hit recovery; it doesn't happen while frozen. **Conflict on distance:** Basin says "up to 3 sub-tiles"; D2MOO sets a path distance of 5, in units it doesn't define. | MODEL-VERIFIED (partial) |
| 1f | **No root or immobilize effect exists for players.** Slows from cold length, Holy Freeze (from Aura-Enchanted uniques), Decrepify and Slows Target **add together**, with floors at **25 % velocity** and **15 % attack rate**. | MODEL-VERIFIED (code `Units.cpp`, Basin) |
| 2a | **Chill** sets **−50** on velocity %, attack rate and other-animation rate (players' chill effectiveness is −50). **Casting is not slowed:** cast speed reads only FCR. Block speed (FBR) and hit-recovery speed (FHR) are not slowed either. Whirlwind runs on attack rate, so chill does slow it (INFERRED). | MODEL-VERIFIED (code, Basin Chill_effectiveness, Arreat "move and attack much more slowly"). That casting is unaffected comes from code plus Basin's silence. |
| 2b | **Chill length:** frames = cold length × (100 − CR_eff)/100. CR_eff is the displayed cold resist after the Hell −100 penalty, clamped to [−100, min(75 + max cold res, 95)], with a minimum of 1 frame. A second chill only **extends** the remaining time; the magnitude stays at −50. | MODEL-VERIFIED (code, Basin Cold_Resist, Basin Cold_Damage) |
| 3a | **Poison does not stack.** A new poison replaces the current one (both rate and length) only if its per-frame rate is equal or greater; a weaker poison is ignored. | MODEL-VERIFIED (code, Basin Poison_Damage) |
| 3b | **Poison length reduction:** length × (100 − PLR_eff)/100, where PLR_eff = item PLR **−100 in Hell** (−40 in Nightmare), clamped to [−100, 75]. An unresisted player in Hell takes **×2 length**. Poison *damage* is reduced separately, by poison resist. | MODEL-VERIFIED (code `Plen` row, Basin PLR) |
| 3c | **Poison cannot kill a player.** The regeneration step floors life at 1 point; a later direct hit can still kill. | MODEL-VERIFIED (code `EVENTS_HpRegen`, Basin Poison_Damage) |
| 3d | **Burn damage over time** follows the same replace-if-stronger rule, and its damage-table entry has no resist row. | INFERRED (single code source) |
| 4a | **Stamina drain:** 2 × RunDrain (= 40/256 points per frame; RunDrain is 20 for both classes) × (body-armour speed/10 + 1, integer division) × (1 − Slower Stamina Drain). That is **3.906 points/s** at base. Drain happens only while running outside town. | MODEL-VERIFIED (code, CharStats DATAMINED, Basin Stamina_Drain) |
| 4b | **Running at zero stamina:** at 0 stamina a run order becomes a walk (town-walk in town). | MODEL-VERIFIED (code, Basin Stamina) |
| 4c | **Stamina regeneration per frame:** +max/256 standing (full in 10.24 s); +max/512 walking, only if at least 1 point (full in 20.48 s); 0 while running, attacking or casting. All scaled by Heal Stamina %. | MODEL-VERIFIED (partial: the code is the only source for the rate) |
| 4d | **Base stamina:** Sorceress = 74 + (clvl − 1) + (Vit_total − 10). Barbarian = 92 + (clvl − 1) + (Vit_total − 25). Item Vitality counts, because vitality op 9 feeds maxstamina; Battle Orders adds stamina %. At clvl 90 on the parent's sheet: **228** (MAXBLOCK, Vit 75) or **533** (NODEX, Vit 380). | MODEL-VERIFIED (CharStats DATAMINED, Basin class tables, J4a F12) |
| 5 | **Barbarian mana regeneration is identical to the Sorceress's H09.** CharStats ManaRegen = 120 for **both** classes, giving about 120 s from empty to full at 0 % bonus. This also closes **J4a F12's open item** on what ManaRegen means. | MODEL-VERIFIED (code `EVENTS_ManaRegen`, CharStats, Basin Regenerate_Mana, J4b H09) |
| 6 | **Life regeneration:** players have no natural life regeneration. **Replenish Life +N** = N/256 life per frame = **N × 25/256 life/s**. It is added raw to hit points, which are stored in 1/256 points (ItemStatCost: hpregen has no ValShift, hitpoints has ValShift 8). It nets against poison and still applies while poisoned. | MODEL-VERIFIED (code, ItemStatCost DATAMINED, Basin, Arreat) |
| 7 | **The Barbarian's belt:** `d2-ww-barb.json` names **no belt**, so this is a **conductor default**. Reference table (Armor.txt belt type → slots): Belt (type 0) 12; Sash (type 1) 8; Plated Belt (type 3) 16; Light Belt (type 4) 8; Heavy Belt (type 5) 12; every exceptional and elite belt (type 6) 16; no belt = 4. | Absence: DATAMINED. Table: MODEL-VERIFIED (Armor.txt plus Arreat #Boxes plus the Belts index; asserted equal) |

## Gaps and conflicts
- **Version:** D2MOO is 1.10f. None of the sources showed a 1.13 change to these laws.
- **Knockback distance:** Basin's 3 sub-tiles against D2MOO's path distance 5 (units unknown). Unresolved.
- **Stamina regeneration and burn damage over time** rest on a single source.
- **Belts.txt is missing from the 1.13 mirror,** so the slot index comes from a D2R 3.0 mirror. It agrees with Arreat on all seven bases checked.
- **Hit-recovery threshold** (outside this scope; noted only): D2MOO's `sub_6FCC1870` uses a max-life divisor per hit class (8/16/32/64) with random bands. The common community rule is "1/12 of max life". The two conflict; I didn't pursue it.
- **Monster stun sources** against players weren't enumerated. Only the law above is given.
