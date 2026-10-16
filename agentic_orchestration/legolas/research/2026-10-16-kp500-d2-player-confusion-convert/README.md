# KP-500: does a D2 player have a confusion or convert state? (2026-10-16)

**Commissioner:** gandalf (citation request from jack-ryan Gate-2 `ec3d78cd5` INFO-1). The KP-500 ruling says the GD Confusion and Convert families have no effect on the D2 Sorceress. The GD side is confirmed in code; this file sources the D2 side.

**Verdict: CONFIRMED.** A D2 player has no state that makes them attack randomly, lose control of their targeting, or switch sides.
- Every D2 skill that applies such a state (Confuse, Attract, Conversion, Mind Blast's conversion) and the AI curses (Dim Vision, Terror) admit **monsters only**, by an explicit unit-type test in code.
- No monster in LoD 1.13 or D2R 3.x carries any of these skills.
- **The player-side analogue is loss of action, not loss of control:** Stun (and hit recovery). Freeze is not one, because on a player it becomes Cold (chill). Neither stands in for Confusion or Convert. See § 3.

**Sources**
- **D2MOO** @ `5596f5cb6c5251a0a07c6637d26458b06099d516` (1.10f), cited files copied into `captures/`.
- **LoD 1.13 tables:** `research/datamine-acquisition/d2/raw/Skills.txt` and `MonStats.txt` (fabd/diablo2 @ 45112569).
- **D2R 3.x tables:** blizzhackers/d2data @ `fc469993` (`skills.json`, `monstats.json`, patch 3.3.93847), captured.
- **Basin wiki (secondary):** raw pages for Confuse, Attract, Conversion, Mind Blast and Stun, captured.
- **Re-derivation:** `python3 -I verify_kp500.py` writes `kp500_facts.json`; the last run had 0 failures. It checks every anchor below and runs the table scans.

**Read-only. No graded-margin file opened.**

## 1. The states exist, but only monsters can receive them

`D2States.h` defines `STATE_CONVERSION` (L69), `STATE_ATTRACT` (L73) and `STATE_CONFUSE` (L75). Every path that applies one of them tests the target's unit type first.

| Skill (LoD Id) | Applier, D2MOO 1.10f | Player excluded by | Grade |
|---|---|---|---|
| **Confuse** (81, Necromancer; `srvdofunc` 61) | `SKILLS_SrvDo061_Confuse` (`SkillNec.cpp` L652) → per-target callback `sub_6FD0C060` (L719) | L723: `pUnit->dwUnitType != UNIT_MONSTER` → return 0 | DATAMINED |
| **Attract** (86, Necromancer; `srvdofunc` 59) | `SKILLS_SrvDo059_Attract` (L559); radius callback `sub_6FD0BDA0` (L626) | `sub_6FD15190(target, AISPECIALSTATE_INVALID)` on the target (L570) and in the radius (L632). It returns false for any non-monster (see below) | DATAMINED |
| **Conversion** (116, Paladin; `srvdofunc` 79) | `SKILLS_SrvDo079_Conversion` (`SkillPal.cpp` L1110) | L1131: `pTarget->dwUnitType == UNIT_MONSTER && … && sub_6FD15190(…)`. Against a player it is just an ordinary hit (`SUNITDMG_DrainItemDurability`) | DATAMINED |
| **Mind Blast** (273, Assassin; `srvdofunc` 51), the conversion part | `SKILLS_AuraCallback_MindBlast` (`SkillAss.cpp` L2219), which sets `STATE_CONVERSION` (L2240) | L2223: `pUnit->dwUnitType == UNIT_MONSTER && !hireling && …` | DATAMINED |
| **Dim Vision / Terror** (71 / 77): the AI-altering curses | generic curse callback `sub_6FD0B450` (`SkillNec.cpp` L295) | L302: `pUnit->dwUnitType != UNIT_MONSTER` → return 0 for the AI curses | DATAMINED |

**The shared gate.** `sub_6FD15190` (`Skills.cpp` L3909) defers to `AIUTIL_CanUnitSwitchAi` (`AiUtil.cpp` L1324). That function returns FALSE whenever `pUnit->dwUnitType != UNIT_MONSTER` (L1326). A player has no AI to switch, and the AI special-state table (`AiStates.h` L6) lists only monster AI states. **DATAMINED.**

**Why alignment alone would not do it.** `STATLIST_GetUnitAlignment` (`D2StatList.cpp`) returns EVIL by default for a unit without an alignment state, so the alignment test by itself would not exclude a player. **The explicit unit-type tests above are what exclude players.** **DATAMINED.**

**Secondary source.** The Basin pages say Confuse "can only be cast on normal and minion monsters"; Attract "only applies to one normal or minion monster"; Conversion and Mind Blast "only convert normal and minion monsters". This independently agrees with the code. **MODEL-VERIFIED.**

## 2. No monster can apply them to the Sorceress

- **LoD 1.13 Skills.txt.** The only skills carrying `auratargetstate` ∈ {confuse, attract, conversion, terror, dimvision, taunt}, or `srvdofunc` ∈ {51, 59, 61, 79}, are player-class skills:
  - Dim Vision, Terror, Confuse, Attract (Necromancer);
  - Conversion (Paladin);
  - Howl, Taunt, Grim Ward (Barbarian);
  - Mind Blast (Assassin).

  None is a monster-only row. **DATAMINED.**
- **LoD 1.13 MonStats.txt:** 735 rows × `Skill1`–`Skill8`. **Zero** monsters list any of those skills. **DATAMINED.**
- **D2R 3.x:** the same nine skills, all class skills, and **zero** of 751 `monstats.json` rows list one. **DATAMINED.**
- Even if a monster or a PvP player cast one, § 1's unit-type gates would refuse a player target. **DATAMINED (1.10f); INFERRED (D2R; server closed, but the skill columns are the same).**

## 3. Is there a player-side analogue to map instead?

There is no analogue for **Confusion** (random targeting) or **Convert** (switching sides). D2 players have no AI-driven target selection to corrupt, and alignment-switching is applied only to monsters. **DATAMINED.**

The control effects that **do** land on a D2 player are a different family: losing the ability to act, not losing control of what you act on.
- **Stun.** `SUnitDmg.cpp` L1333–1335 applies stun to any non-monster, capped at 250 frames. It sets `STATE_STUNNED` (L1366). A stunned player who takes a hit is forced into GetHit (L2029), which cancels a pending cast; see the Meteor folder, Q3. **DATAMINED.**
- **Hit recovery / knockback.** These are the GetHit and knockback mode changes already modelled in the port. **DATAMINED** (Meteor folder).
- **Freeze is not a player state in 1.10f.** `SUNITDMG_ApplyFreezeState` (L1645) turns freeze into the Cold (chill) state when the defender is a player (L1658–1661). **DATAMINED (1.10f); INFERRED for D2R.**

**Recommendation (my inference; the mapping is the conductor's call):**
- Keep **Confusion → no effect** and **Convert → no effect** for the D2 Sorceress.
- Do not fold either into Stun. GD has its own Stun / Freeze families, and mapping those to D2 Stun or chill is a separate question.

## Files
- `captures/`:
  - the D2MOO sources (`SkillNec`, `SkillPal`, `SkillAss`, `Skills`, `AiUtil`, `AiStates.h`, `SUnitDmg`, `D2States.h`, `D2StatList`);
  - `d2data/skills.json` and `d2data/monstats.json` (D2R @ `fc469993`);
  - the Basin raw pages.

  The sha256 values are in `kp500_facts.json`.
- `verify_kp500.py` re-derives every line anchor and runs the table scans. Its output is `kp500_facts.json`.
