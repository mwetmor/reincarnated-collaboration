# Research — GD AI State Tables: Complete Enumeration — 2026-07-25

**Mode:** A (analytical / binary inspection)
**Commissioner:** gandalf
**Binary:** `/Users/admin/Games/vendor/grim-dawn/Game.dll` (8,865,792 bytes — confirmed match)
**Method:** `strings -a -t d Game.dll` piped to awk/grep; `xxd` for boundary verification. All offset claims are decimal file offsets into `Game.dll` unless stated otherwise. `Engine.dll` and `Grim Dawn.exe` searched for cross-checks.
**Crawl date:** 2026-07-25

---

## Summary

Table 3 (ControllerMonster AI State) has exactly **40 entries** in the string table at `Game.dll` 5418372–5418812. The prior "40" claim was numerically correct but the enumeration was incomplete. The full table is reproduced below. `RepositionForAttack` is entry #5 in this table (CamelCase, no spaces — the spaced form "Reposition for Attack" does not exist anywhere in any of the three binaries). `AlertBeforePursue` is entry #40 and is confirmed present with RTTI and method symbols proving it is a live class with `OnBegin`, `OnUpdate`, `OnEnd`, and `HandleEvent` implementations. The two debug-overlay labels appear to draw from different tables: Table 1 (Action State) supplies one label and Table 3 (ControllerMonster AI State) supplies the other. Table 3 contains four words that also appear in Table 1 (`Idle`, `Attack`, `Dying`, `Move`) — these are independent entries in disjoint tables, not shared references.

---

## Complete Table 3 Enumeration — ControllerMonster AI State

**Region:** `Game.dll` offsets 5418372–5418812 (440 bytes)
**Entry count:** 40 (OBSERVED — counted from the `strings -t d` output)
**Boundary evidence:** documented in the boundary section below.

| Index | Offset   | String               | Byte length (incl. null) |
|-------|----------|----------------------|--------------------------|
| 1     | 5418372  | Idle                 | 5                        |
| 2     | 5418380  | Startup              | 8                        |
| 3     | 5418388  | Attack               | 7                        |
| 4     | 5418396  | Pursue               | 7                        |
| 5     | 5418404  | RepositionForAttack  | 20                       |
| 6     | 5418424  | JumpAttack           | 11                       |
| 7     | 5418436  | Roam                 | 5                        |
| 8     | 5418444  | Flee                 | 5                        |
| 9     | 5418452  | WanderPause          | 12                       |
| 10    | 5418464  | Wander               | 7                        |
| 11    | 5418472  | Dying                | 6                        |
| 12    | 5418480  | Return               | 7                        |
| 13    | 5418488  | FollowLeader         | 13                       |
| 14    | 5418504  | Dead                 | 5                        |
| 15    | 5418512  | NavigateObstacle     | 17                       |
| 16    | 5418532  | DefendLeader         | 13                       |
| 17    | 5418548  | Charge               | 7                        |
| 18    | 5418556  | Move                 | 5                        |
| 19    | 5418564  | Panic                | 6                        |
| 20    | 5418572  | DodgeAttack          | 12                       |
| 21    | 5418584  | Confused             | 9                        |
| 22    | 5418596  | Paralyze             | 9                        |
| 23    | 5418608  | Trapped              | 8                        |
| 24    | 5418616  | Immobile             | 9                        |
| 25    | 5418628  | KnockedDown          | 12                       |
| 26    | 5418640  | Stunned              | 8                        |
| 27    | 5418648  | Scared               | 7                        |
| 28    | 5418656  | Sleeping             | 9                        |
| 29    | 5418668  | WaitToAttack         | 13                       |
| 30    | 5418684  | Patrol               | 7                        |
| 31    | 5418692  | QuestWalk            | 10                       |
| 32    | 5418704  | QuestMove            | 10                       |
| 33    | 5418716  | QuestUseSkill        | 14                       |
| 34    | 5418732  | QuestPlayAnimation   | 19                       |
| 35    | 5418752  | TakeHit              | 8                        |
| 36    | 5418760  | GettingUp            | 10                       |
| 37    | 5418772  | UseSkillOnPoint      | 16                       |
| 38    | 5418788  | UseSkillOnAlly       | 15                       |
| 39    | 5418804  | Emote                | 6                        |
| 40    | 5418812  | AlertBeforePursue    | 17                       |

---

## Boundary Evidence

### Lower boundary (5418372)

OBSERVED: `xxd` of offset range 5418340–5418380 shows the 32 bytes immediately preceding `Idle` (5418372) are the tail of the string `ControllerMonster::ChooseBestSkill picked an invalid skill for %s\0` followed by null padding. The `Idle` at 5418372 follows a `\x00\x00\x00` pad region that terminates that error-message string. This is a qualitatively different class of string (error format) from the tightly-packed state-name strings, so the break is unambiguous.

OBSERVED: At 5418236 and 5418244, there are two earlier occurrences of `Idle` and `Roam` in a much shorter two-entry sequence, followed immediately by `ControllerMonster::GetHomePosition() : No monster!` — a different string cluster, not a continuation of a state name table.

### Upper boundary (5418812 + 17 = 5418829)

OBSERVED: `xxd` of offset 5418812 shows `AlertBeforePursue\x00\x00\x00` (the string plus 3 null bytes of padding), followed at 5418832 by `Dead\x00\x00\x00\x00`, then `Startup\x00` at 5418840, then `Patrol Points\x00\x00\x00` at 5418848. These are not continuation of the state table — `Patrol Points` is a display label for patrol-path geometry, and the sequence `Dead / Startup` appears to be a different initialization list. Structural break is confirmed.

### Count confidence

The awk extraction `$1 >= 5418372 && $1 <= 5418812` yields exactly 40 lines. Cross-check: the arithmetic (5418829 - 5418372 = 457 bytes / 40 entries = ~11.4 bytes/entry avg) is consistent with the observed distribution of short names (4–6 bytes) and longer names (12–20 bytes). The `strings` tool defaults to minimum length 4; no entry in this table is shorter than 4 characters, so no entry would be suppressed.

---

## Question 1 — Where does "Reposition for Attack" live?

**Finding:** The spaced-form `"Reposition for Attack"` does not exist in `Game.dll`, `Engine.dll`, or `Grim Dawn.exe`. Zero hits in all three binaries. (OBSERVED: `grep -c "Reposition for Attack"` returns 0 across all three string extraction files.)

The CamelCase form `RepositionForAttack` exists in `Game.dll` at many locations (OBSERVED: 100+ hits in `Game.dll` alone), principally in two categories:

1. **String table entry** — `Game.dll` offset 5418404, Table 3 index #5. This is the state name literal.
2. **RTTI symbols** — a full class `ControllerMonsterStateRepositionForAttack@GAME` is present with constructors (offsets 6709233, 6709297), destructor, vtable, and a complete method set: `OnBegin` (7898093), `OnEnd` (7905531), `OnUpdate` (7915320), `HandleEvent` (not present for this class — OBSERVED: not in HandleEvent list), `AllyDied`, `AllyNeedsHelp`, `Attacked`, `ClosestEnemyFound`, `Confused`, `EndOfPathReached`, `EnemyFound`, `LostSlot`, `LowHealth`, `PathFailed`, `ProjectileNotification`, `ProjectileResultCallback`, `RequestAttack`, `RequestMove`, `ShouldFindClosestEnemy`, `ShouldFindEnemy`.

**Conclusion:** "Reposition for Attack" as Matt reported it is either (a) how the human eye parses `RepositionForAttack` on a debug overlay rendering CamelCase without spaces, or (b) a runtime string-formatting step inserts spaces — but no such format string was found in the binary. The state is Table 3, index #5, offset 5418404. It is NOT a fourth table. There is no fourth table.

---

## Question 2 — Is AlertBeforePursue real and reachable?

**String existence:** CONFIRMED. OBSERVED at `Game.dll` 5418812, Table 3 entry #40.

**RTTI confirmation:** The class `ControllerMonsterStateAlertBeforePursue@GAME` exists with:
- Constructors at 6705874 (copy), 6705936 (from `ControllerMonster*`)
- Destructor at 6841992
- Assignment operator at 6907596
- Vtable at 6998217
- `OnBegin` at 7896646 (linkage: `UAEXXZ` — virtual, no arguments)
- `OnUpdate` at 7914053 (linkage: `UAEXH@Z` — virtual, int argument)
- `OnEnd` at 7904239
- `HandleEvent` at 7772464 (linkage: `MAEXABVName@2@@Z` — takes a `Name` object)

The `HandleEvent` override is significant: only a minority of monster states override `HandleEvent` (most inherit the base class implementation). The fact that `AlertBeforePursue` has its own `HandleEvent` implementation (OBSERVED) is consistent with the hypothesis that it responds to specific trigger events — the name-based event system is how GD's controller FSM receives external stimuli (player sighted, ally attacked, projectile incoming, etc.).

**Reachability from binary:** CANNOT DETERMINE. The binary inspection reveals the class exists and has full implementation. What cannot be determined from strings alone is: (a) which event name(s) `HandleEvent` checks to transition out of `AlertBeforePursue`, (b) what condition sets `AlertBeforePursue` as the active state, (c) what anger threshold or timer drives its `OnUpdate` loop. These questions require either disassembly of those four functions or a live measurement protocol. A clean "cannot determine" is the correct answer for the transition conditions.

---

## Question 3 — Do the two debug overlay positions draw from different tables?

**Hypothesis:** top-left draws Table 3 (Controller AI State), bottom-right draws Table 1 (Action State).

**Evidence supporting:** OBSERVED. Table 1 strings all carry the prefix `"Action State: "` baked into each literal (e.g., `"Action State: Idle"`, `"Action State: Attack"`). This means they are not format-string + enum-index rendered labels — they are pre-concatenated strings in a lookup table. The rendering code for this table prints the entire pre-concatenated string. Table 3 strings are bare names without any prefix. Both are qualitatively distinct draw operations.

OBSERVED: Matt reports seeing words like `Idle`, `Attack`, `Dying`, `Move` in BOTH overlay positions. Table 1 contains `Action State: Idle`, `Action State: Attack`, `Action State: Dying`, `Action State: Move` (with the prefix). Table 3 contains bare `Idle`, `Attack`, `Dying`, `Move` (without prefix). If the bottom-right position renders the full Table 1 string including prefix, it would show `Action State: Idle` — which at small overlay font size would abbreviate visually to just `Idle`. This is consistent with the hypothesis.

OBSERVED: `Roam`, `Pursue`, `RepositionForAttack` are in Table 3 but NOT in Table 1 (confirmed: `grep -w "Walk" / "Roam" / "Pursue"` on the Table 1 region returns no hits for Roam/Pursue). These are the words Matt saw only top-left.

**Evidence against or not found:** No format string or draw-call function name was found in the `strings` output that would identify exactly which code emits each label or which screen coordinate is targeted. `debugDrawWorld` is a string at `Game.dll` 2765720 but no adjacent strings name a two-label pattern.

**Verdict:** The hypothesis is SUPPORTED by indirect evidence (structural difference between pre-concatenated Table 1 strings vs. bare Table 3 strings; vocabulary disjunction matching Matt's observations). It is not CONFIRMED because the actual render call paths are not identifiable from string extraction alone — that requires disassembly. The hypothesis should be treated as the working model for the measurement protocol design but flagged as unconfirmed at the code level.

---

## Question 4 — Does Table 3 contain the overlap words, and what does that mean?

**OBSERVED:** Table 3 contains `Idle` (index #1), `Attack` (index #3), `Dying` (index #11), `Move` (index #18). It does NOT contain `Walk`.

Table 1 contains `Action State: Walk` (offset 5192884) but Table 3 has no `Walk` entry. Matt reported seeing `Walk` in BOTH positions — this is the one word that creates a tension with the hypothesis. Possible resolutions: (a) the Table 3 `Move` state drives a walking animation and the debug overlay label for move-at-walk-speed shows `Walk` via the Table 2 animation-state layer, (b) `Walk` appears in a Table 3 duplicate region that this inspection did not find, or (c) Matt's observation of `Walk` at the top-left position reflects a different rendering path than expected.

**Structural finding:** `Idle`, `Attack`, `Dying`, and `Move` exist independently in both Table 1 (with `Action State:` prefix) and Table 3 (bare). They are independent string literals at different offsets — NOT shared references. Seeing `Idle` top-left and `Idle` bottom-right means the monster is simultaneously in ControllerMonster AI State `Idle` AND Action State `Idle` — two separate state machines agree. This is mechanistically sensible: the Controller AI FSM selects the goal-state (`Idle`), and the Action State FSM executes the motor action (`Idle`). They are not the same layer falling back to each other.

---

## RTTI State Class Count vs. String Table Count

OBSERVED: The RTTI constructor list for `ControllerMonsterState*@PAVControllerMonster@` yields 42 distinct class names. The string table at 5418372–5418812 yields 40 entries. The discrepancy is two classes:

- `ControllerMonsterStateReturnFast` — in RTTI (constructor at 6709552), NOT in Table 3 string table.
- `ControllerMonsterStateHidden` — in RTTI (constructor at 6707407 referencing `PAVControllerMonsterHidden@` not `PAVControllerMonster@` — a different base controller), NOT in Table 3.
- `ControllerMonsterStateSleep` — in RTTI (OnUpdate at 7915543), NOT in Table 3 as `Sleep`. Table 3 has `Sleeping` (index #28). These are likely the same state; the class name suffix and the string table entry differ.

So: the string table has `Sleeping` where the RTTI has `Sleep`, and two additional classes (`ReturnFast`, `Hidden`) are not represented by entries in Table 3. These classes may self-report via a different naming mechanism, or they may inherit the base state's name string. This is INFERRED from naming pattern; it cannot be confirmed from string extraction.

---

## Coverage Boundaries — What Was NOT Established

### Cannot determine from this inspection:

1. **Transition conditions for `AlertBeforePursue`.** `HandleEvent` and `OnUpdate` are real functions at confirmed offsets but their instruction content was not disassembled. What anger threshold, timer, or event name triggers entry into or exit from `AlertBeforePursue` is unknown. Correct method: live measurement or disassembly of `OnBegin@ControllerMonsterStateAlertBeforePursue` (7896646) and `OnUpdate@...` (7914053).

2. **Which screen position renders which table.** The two-label render paths were not traced. The hypothesis (top-left = Table 3, bottom-right = Table 1 with prefix) is consistent with observed evidence but not confirmed at the code level.

3. **`Walk` at both overlay positions.** Matt reportedly saw `Walk` in both the top-left and bottom-right positions. Table 3 does not contain a `Walk` entry. This is unresolved — it may involve the Table 2 animation-state layer or a rendering path not visible from string extraction.

4. **`ReturnFast` and `Hidden` display names.** These RTTI-confirmed classes have no entry in Table 3. Whether they appear on the debug overlay and under what name is unknown.

5. **Whether Table 3 is the ONLY ControllerMonster AI state enumeration table.** The `strings` extraction found this table cleanly, but a second separate enumeration table for the same state space cannot be ruled out purely from string extraction. The count (40 string entries, 42 RTTI classes, with reasonable explanations for the 2-entry gap) is internally consistent, which raises confidence but is not a proof of completeness.

### Confirmed absent:

- `"Reposition for Attack"` (spaced form) — definitively absent from all three binaries.
- Table 3 does not contain `Walk`.
- No fourth state table was found. `RepositionForAttack` is Table 3 entry #5.

---

## Source Evidence Index

| Claim | Source / method |
|-------|-----------------|
| Table 3 offsets and entry count | `strings -a -t d Game.dll` + `awk '$1 >= 5418372 && $1 <= 5418812'` — OBSERVED |
| Lower boundary evidence | `xxd -s 5418340 -l 50 Game.dll` — OBSERVED |
| Upper boundary evidence | `xxd -s 5418812 -l 60 Game.dll` — OBSERVED |
| "Reposition for Attack" absence | `grep -c "Reposition for Attack"` on all three string extraction files — OBSERVED, 0 hits |
| `RepositionForAttack` in Table 3 | `awk '$1 >= 5418372 && $1 <= 5418812'` row at 5418404 — OBSERVED |
| `AlertBeforePursue` RTTI class | Constructor at 6705936, OnBegin at 7896646, OnUpdate at 7914053, HandleEvent at 7772464 — OBSERVED |
| 42 RTTI classes | `grep "QAE@PAVControllerMonster@" + ControllerMonsterState filter` — OBSERVED |
| Table 1 pre-concatenated format | `awk '$1 >= 5192736 && $1 <= 5193156'` — OBSERVED, all entries begin "Action State: " |
| Table 3 overlap words (Idle/Attack/Dying/Move) | `grep -w "Idle\|Attack\|Dying\|Move"` on Table 3 awk slice — OBSERVED |
| Walk absent from Table 3 | `grep -w "Walk"` on Table 3 awk slice — OBSERVED, no hits |
| Walk present in Table 1 | `grep -w "Walk"` on Table 1 awk slice — OBSERVED at 5192884 |
