# KP-481 follow-up: mana-debit timing for Fire Ball, Fire Bolt, Static Field and Meteor (2026-10-15)

**Commissioner:** gandalf (JOIN-1). The Meteor ruling debits mana at the action frame "only for skills whose handler order is cited". This file cites that order for the other three skills, and for Meteor alongside them.
**Pin:** D2MOO `5596f5cb6c5251a0a07c6637d26458b06099d516` (1.10f), the same pin as `README.md`. Cited files are in `captures/` and are byte-identical to the pin.
**Tables:**
- LoD 1.13 `Skills.txt` (sha256 `59601208…cdc07`).
- D2R 3.x `captures/d2data/skills.json` (blizzhackers `fc469993`).

**Re-derivation:** `python3 -I verify_mana_debit.py` writes `mana_debit_facts.json`; the last run had 0 failures. It checks:
- every line anchor below,
- the table values,
- that start-table index 0 and do-table index 0 are both `nullptr`,
- that the lines in the handler occur in the order the argument depends on.

**Read-only. No graded-margin file opened.**

**D2R caveat (applies to every answer).** The D2R server code is closed. For all four skills, every Skills.txt column that bears on debit timing has the same value in D2R 3.x as in LoD 1.13: `srvstfunc`, `srvdofunc`, `srvmissile`, `usemanaondo`, `startmana`, `AttackNoMana`, `LineOfSight`, `interrupt`. That equality is DATAMINED. The behaviour built on those columns is DATAMINED for 1.10f and INFERRED for D2R.

## The two code paths (shared by all four skills)

**Start path.** It runs at the request frame, when the player enters the cast mode.
- `PLRMODE_StartXY_AttackCastThrowKickSpecialSequence` (`PlrModes.cpp` L852) does two things in order:
  1. schedules the action-frame `EVENTTYPE_MODECHANGE` event through `sub_6FCBCE70`;
  2. calls `sub_6FD12FD0`, which reaches `sub_6FD12950(…, a5 = 0)` (`Skills.cpp` L2336) at L2675.
- `sub_6FD12950`, in order:
  - L2344: **mana-sufficiency check** `!a5 && !sub_6FD10CE0(pUnit)` → return 0. This only checks; it does not debit.
  - L2364–2408: **line-of-sight gate**, only if `lineofsight` ≠ 0. It ray-traces from the player to the target point (the target unit, else the path's first point) with the per-type mask (`D2Common_11026`, `D2Skills.cpp` L3184), and returns 0 if blocked.
  - L2417: looks up `gpSkillSrvStartFnTable_6FD408B0[srvstfunc]`. Index 0 is `nullptr` (L64–66), so an **empty `srvstfunc` returns 1 here without debiting**.
  - L2427–2433: **this is the only start-time debit**, and it happens only when a start function exists, returns nonzero, and `usemanaondo` is not set.
- **If `sub_6FD12950` returns 0:** `sub_6FC817D0(pGame, pUnit, 0, 5, 0, 0, 1)` at L2678 forces mode 5. That is `PLRMODE_StartXY_Neutral` (`PlrModes.cpp` L159), which deletes the per-frame events and clears the used skill. The action frame never comes, so **no debit, no effect, and the cast is aborted on the request frame**.

**Action-frame path.** The scheduled event goes through `sub_6FC81600` → `sub_6FC80EE0` → `sub_6FD13410` (`Skills.cpp` L2745) → `D2GAME_SKILLS_Handler_6FD12BA0(…, a5 = 1, a6 = 0, a7 = 0)` (L2445). The handler, in source order:

| Line | Step |
|---|---|
| L2490 | `usemanaondo` only: return 0 if the mana check fails |
| L2504 | `nResult = pDoFunc(…)`. Do-table index 0 is `nullptr` (L160–162), so an empty `srvdofunc` leaves `nResult = 0` |
| L2507–2552 | if `srvmissile` is valid: create it through `sub_6FD11420` (L2548), then **`nResult = 1` unconditionally** (L2551). The creator's return value is not read |
| L2554 | `if (!nResult) return 0;` |
| L2559 | `if (a5)` |
| L2563–2566 | **debit**, if there is no start function, or `usemanaondo` is set |
| L2574–2577 | delay (Meteor only) |

**The debit.** `D2GAME_SKILLMANA_Consume_6FD10A50` (L1063):
- cost = `(mana + (slvl−1)·lvlmana) << manashift` when slvl > 1 (L1085), floored at `minmana << 8`;
- if `STAT_MANA < cost` it **returns 0 without debiting** (L1101). The handler ignores that return value;
- otherwise it subtracts the cost: `STATLIST_AddUnitStat(STAT_MANA, −cost)` (L1106);
- slvl is the level including +skills (`SKILLS_GetSkillLevel(…, 1)`, `D2Skills.cpp` L1993).

## (a) Fire Bolt (Id 36) and Fire Ball (Id 47)

The rows are `srvstfunc` empty, `srvdofunc` empty, `srvmissile` = `firebolt` / `fireball`, `lineofsight` empty, `usemanaondo` empty, `interrupt` = 1. **DATAMINED, both versions.**

- **When mana is spent:**
  - **At skill start: no debit.** The mana check at L2344 runs. There is no line-of-sight gate (`lineofsight` = 0). The start function is null, so L2417 returns 1.
  - **At the action frame:** the do-function is null, so `nResult = 0` (L2504). Then the `srvmissile` branch **creates the missile** (L2548) and sets `nResult = 1` (L2551). **The debit follows**, at L2563–2566, because there is no start function.
  - So the order is skill start (no debit) → action frame → missile created → mana debited. The last two are in **one server call on one game frame**.

  **DATAMINED (1.10f); INFERRED (D2R).**
- **Interrupted before the action frame: no debit.** GetHit (`PlrModes.cpp` L840) and Block (L822) delete the action-frame event (`SUnit.cpp` L1466). The `interrupt` = 1 bit lets the interruption through (`PlrModes.cpp` L113), with the same Concentration / Concentrate exception as for Meteor. The handler never runs. **DATAMINED / INFERRED (D2R).**
- **Failed missile creation: mana is still spent.**
  - `nResult = 1` is set at L2551 whatever `sub_6FD11420` returns.
  - On this path there is **no point validation at all**. The creator (`Skills.cpp` L1463) fails only if:
    - the target resolves to x = 0 or y = 0 (L1493), or
    - `MISSILES_CreateMissileFromParams` (`Missiles.cpp` L70) finds no owner, no record, or no room at the origin.
  - There is no distance cap and no collision test at the aim point. A bolt aimed into a wall is created and then collides in flight.
  - So an "invalid point" is not a category for these two skills. Even the degenerate failure spends the mana.

  **DATAMINED (1.10f); INFERRED (D2R).**

## (b) Static Field (Id 42)

The row is `srvstfunc` empty, `srvdofunc` = 20, `srvmissile` empty, **`lineofsight` = 4**, `usemanaondo` empty, `interrupt` = 1. **DATAMINED, both versions.**

- **`SrvDo020` runs before the debit: confirmed.** `SKILLS_SrvDo020_StaticField` (`SkillSor.cpp` L406) is called at L2504. The debit is at L2563–2566, behind the gate at L2554. **DATAMINED.**
- **No targets in range: mana is still spent.**
  - `SrvDo020` fails only if the Skills.txt or DifficultyLevels.txt record is missing.
  - Otherwise it walks the area through `sub_6FD0FE80(…, nAuraRange, …, SKILLS_AuraCallback_StaticField, …)` (L433) and **returns 1 unconditionally**.
  - So `nResult = 1` and the debit runs whether 0 or N units were hit. A cast with no target in range is a valid cast and costs its mana.

  **DATAMINED (1.10f); INFERRED (D2R).**
- **Start-time gate that is easy to miss: `lineofsight` = 4** (`SKILLSLOS_PLAYER_FLYING`, `SkillsTbls.h` L112). This sets mask `COLLIDE_DOOR | COLLIDE_MISSILE_BARRIER` (`Skills.cpp` L2396).
  - At start, the ray from her to the target point (the target unit, else the clicked or path point) is traced. If a door or missile barrier blocks it, start returns 0 and the cast is **aborted on the request frame**: no animation, no debit.
  - The check is skipped if the point is (0,0).
  - Static's *effect* is centred on her, but the *gate* uses the aim point.

  **DATAMINED (1.10f); INFERRED (D2R).**
- **Pre-action interrupt:** no debit, by the same mechanism as (a). **DATAMINED / INFERRED (D2R).**

## (c) Columns that change debit timing, for the four skills

| Column / condition | Code effect | FBolt | FBall | Static | Meteor |
|---|---|---|---|---|---|
| `srvstfunc` (non-empty) | debit moves to **start**, after the start function succeeds (L2427–2433), unless `usemanaondo` is set | empty | empty | empty | empty |
| `usemanaondo` | forces the **action-frame** debit even with a start function (L2563), and adds a do-frame mana check that aborts the do-function (L2490) | empty | empty | empty | empty |
| `srvdofunc` / `srvmissile` | decide **whether** `nResult` = 1, i.e. **whether** the action-frame debit happens: a do-function's return (Meteor `SrvDo028` can return 0; Static `SrvDo020` cannot), or `srvmissile` → always 1 | missile | missile | do 20 | do 28 |
| `lineofsight` ≠ 0 | start-time abort, before any debit | 0 | 0 | 4 | 4 |
| `startmana` | a usability requirement only (`D2Common_SKILLMANA_CheckStartStat`, `D2Skills.cpp` L1858). No debit | empty | empty | empty | empty |
| `AttackNoMana` | when out of mana, swaps to the Attack skill at request time (`PlrMsg.cpp` `sub_6FC83340`). Not a timing change | empty | empty | empty | empty |
| `minmana` / `mana` / `lvlmana` / `manashift` | amount only, not timing | — | — | — | — |
| `interrupt` = 1 | allows a pre-action interrupt (no debit) | 1 | 1 | 1 | 1 |
| state `BLOOD_MANA` / item-charge skill | debits life or a charge instead of mana, at the same point | n/a | n/a | n/a | n/a |

**Verdict for (c):** **no column moves the debit off the action frame for any of the four skills.** All four debit inside `D2GAME_SKILLS_Handler_6FD12BA0` at L2563–2566, after the effect and only if the effect succeeds.
- **Fire Bolt, Fire Ball and Static Field** always succeed once the action frame is reached.
- **Meteor** can fail at the action frame (see `README.md` Q4).

**DATAMINED (1.10f) for the code; DATAMINED that the D2R columns are identical; INFERRED for D2R behaviour.**

## Side findings (not asked; recorded for the port contract)

1. **Mana drained between start and action frame.** `Consume` returns 0 and debits nothing when `STAT_MANA < cost` (L1101). The handler does not check that return value, so the effect has already fired: **the cast is free**. Mana sufficiency is checked only at start (L2344), except for skills with `usemanaondo`. **DATAMINED (1.10f).**
2. **The cost uses total slvl** (base + bonus, `D2Skills.cpp` L1993) in both the check and the debit. The check (`sub_6FD10CE0`, L1178) does not apply the `minmana` floor; the debit does. **DATAMINED.**

## Erratum to `README.md` Q4 (Meteor)

`README.md` Q4 said an invalid Meteor point "still plays the full cast animation". **That is incomplete.**
- Meteor also has `lineofsight` = 4, so a point whose ray from her is blocked by a door or missile barrier is **aborted at start**, on the request frame, with no animation (gate above, `Skills.cpp` L2364–2408 and L2678).
- Only the do-function failures play the animation first: collision at the point (mask 5), distance > 100, or no point. In those cases there is no missile, no mana and no delay, as stated.
- Q2's "Meteor has no start function, so no start debit" stands. Q1, Q3 and Q5 stand.
