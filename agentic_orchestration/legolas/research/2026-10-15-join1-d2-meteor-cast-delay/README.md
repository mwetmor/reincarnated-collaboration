# Research: D2 Meteor cast delay, primary source (2026-10-15)

**Mode:** A (analytical), primary-source probe
**Commissioner:** gandalf (JOIN-1 conductor), for the Sorceress's Meteor delay in the J4b port
**Read-only:** yes. I did not open any J4b graded-margin result file. Nothing in `reincarnated-engine` was touched.

**Sources**
- **D2MOO** @ `5596f5cb6c5251a0a07c6637d26458b06099d516`. This is a 1.10f server/common reconstruction. The cited files are copied in `captures/` and are byte-identical to the pinned tree.
- **LoD 1.13 tables:** `research/datamine-acquisition/d2/raw/Skills.txt` (sha256 `59601208…cdc07`) and `Missiles.txt` (`9d6794a5…def53`). Source is fabd/diablo2 @ 45112569; the byte sizes match MANIFEST.md.
- **D2R 3.x tables:** blizzhackers/d2data `json/skills.json`, last commit `fc469993` ("Updated for patch 3.3.93847"). Captured copy sha256 `b40393a3…35956`.
- **Blizzard:** D2R Patch 2.4 Balance PTR notes, https://news.blizzard.com/en-us/article/23765907 (captured HTML).
- **Basin wiki (secondary):** the `Meteor` and `Cast_rate` pages (raw wikitext, captured).
- **Re-derivation:** `python3 -I verify_meteor_delay.py` re-derives every value and line anchor below from these captures. It writes `meteor_delay_facts.json`; the last run had 0 failures.

**Version note.** The pinned build guide (Maxroll, d2planner `gca1a0l6`) is a **D2R** build. The D2R server binary is closed source. My code-level evidence is 1.10f (D2MOO); my D2R evidence is data tables plus Blizzard's notes. Each answer below states which version it holds for.

## Summary

- **Value:** Meteor's delay is **30 game frames (1.2 s)**.
  - LoD: Skills.txt column `delay`.
  - D2R: column `localdelay` (per-skill); `globaldelay` is empty.
- **When it starts:** at the **action frame**, when the do-function runs. The delay is set in the same server call that creates the `meteorcenter` missile and deducts the mana. It is not set at skill start.
- **Interrupted before the action frame** (GetHit, which also covers stun, or Block): the do-function never runs, so **no delay, no mana spent, no missile**.
- **Point with no monster:** a ground cast **is** legal. The delay **is set**, provided the do-function succeeds:
  - the point is non-zero,
  - it is within distance 100 (`UNITS_GetDistanceToCoordinates`),
  - it is not blocked by wall or missile-barrier collision at missile size 1.

  If the point fails these checks, the cast animation plays, but no delay is set and no mana is spent. (Erratum: a point with a door or missile barrier on the line of sight is instead aborted at start, with no animation; see Q4.)
- **Resets:** nothing in the 1.10f code resets the delay. It ends only at expiry, or when the player unit is created or destroyed (joining or leaving a game). **Level or area change does not reset it.**

## Findings

### Q1. Value and field: 30 frames

- **LoD 1.13 Skills.txt, row `Meteor` (Id 56):**
  - `delay` = 30
  - `srvstfunc` = empty
  - `srvdofunc` = 28
  - `srvmissile` = empty
  - `srvmissilea` = `meteorcenter`
  - `usemanaondo` = empty
  - `interrupt` = 1
  - `anim` = SC

  **DATAMINED.**
- **How the engine reads the field:** it is a formula field, evaluated by `SKILLS_EvaluateSkillFormula(pUnit, pSkillsTxtRecord->dwDelay, …)` (`D2Game/src/SKILLS/Skills.cpp` L2574). It is added to `pGame->dwGameFrame` (L1746). The unit is therefore **game frames**, and the constant 30 evaluates to 30. **DATAMINED.**
- **D2R 3.x skills.json, Meteor:**
  - `localdelay` = 30, `globaldelay` absent.
  - The plain `delay` column no longer exists.
  - `srvdofunc` 28, `srvstfunc` absent, `usemanaondo` absent.

  **DATAMINED.**
- **Seconds:** 30 frames = 1.2 s at 25 frames per second.
  - The Basin Meteor page states "1.2, global (LoD) / 1.2, local (D2R)".
  - The frame rate itself is not proven in the captured code. Its grading is in "Knowledge gaps", item 3.
- **Global vs local:**
  - **LoD:** `SKILLS_CheckSkillDelay` (`D2Common/src/D2Skills.cpp` L1870) blocks *any* skill whose delay formula is > 0 while the single `STATE_SKILLDELAY` is on the player. It is reached through `SKILLS_GetUseState` → `SKILLUSTATE_BLOCKED` (L1605). So in LoD the delay is **global** across all delayed skills. Skills with no delay (Fire Bolt, Static Field) are never blocked. **DATAMINED.**
  - **D2R ≥ 2.4:** the delay is **per-skill**. Blizzard's notes say: *"using a skill with a Casting Delay will no longer add the cooldown to all other skills that have Casting Delays"*, and the Meteor bullet reads *"Casting Delay will no longer share its cooldown…"*. The D2R `localdelay` column agrees. **DATAMINED (data and official notes).**
- **Port consequence:** under the D2R build this is a Meteor-only 30-frame lockout. Fire Bolt and Static Field are never blocked by it.

### Q2. When the delay starts: the action frame, in the same call as the missile and the mana

The call chain, with each link cited:

1. **Cast request** (`PlrMsg.cpp` `sub_6FC83340`, L812): if `SKILLS_GetUseState` returns USABLE, the cast mode starts at (X,Y).
2. **Mode start** (`PlrModes.cpp` `PLRMODE_StartXY_AttackCastThrowKickSpecialSequence`, L852): sets the path target to (X,Y), then calls `sub_6FD12FD0` → `sub_6FD12950(…, a5=0)` (`Skills.cpp` L2336).
3. **Meteor has no `srvstfunc`.** `gpSkillSrvStartFnTable_6FD408B0[0]` is `nullptr`, so `sub_6FD12950` returns 1 at L2417–2425 **without consuming mana** and without setting a delay.
4. **Action-frame event is scheduled at mode start:** `sub_6FCBCE70` (`SUnit.cpp` L1523) schedules `EVENTTYPE_MODECHANGE` at the game frame of the animation's action-flag frame.
5. **Event dispatch at that frame:** `sub_6FC81600` (`PlrModes.cpp` L1422) indexes by mode. Index 10 is `PLRMODE_CAST` (`Player.h` L23), which maps to `sub_6FC80EE0` (L1059), then `sub_6FD13410` (`Skills.cpp` L2745), then `D2GAME_SKILLS_Handler_6FD12BA0(…, a5=1, 0, 0)` (L2445).
6. **Inside the handler, in order:**
   1. the do-function `SrvDo028_Meteor…` (`SkillSor.cpp` L896) creates `meteorcenter` (L2500–2505);
   2. `if (!nResult) return 0;` (L2554);
   3. mana is consumed, because the skill has no start function (L2563–2566);
   4. `nDelay = Evaluate(dwDelay)` and, if `nDelay > 0` and the unit is a player, `D2GAME_SKILLS_SetDelay_6FD11C00` runs (L2574–2577).

   **DATAMINED (1.10f).**
- **Expiry:** the delay expires at `dwGameFrame(action) + 30`. A `STATE_SKILLDELAY` statlist is created with expire frame F+30, plus an `EVENTTYPE_REMOVESTATE` event at F+30 (L1744–1765). That event runs `STATLIST_UpdateStatListsExpiration`, which frees the statlist when `dwExpireFrame <= nFrame` (`D2StatList.cpp` L1855). So the state is up on frames F … F+29 and is removed while frame F+30 is processed. **DATAMINED.**
- **Interval between Meteors:** action-to-action interval ≥ 30 frames plus the next cast's frames-to-action. Basin states the same rule: "interval = action frame + delay; delays begin at the action frame". **MODEL-VERIFIED** (code chain plus a secondary source). FCR shortens only the frames-to-action term; nothing shortens the 30.
- **D2R:** the same start point is **INFERRED**. Basin states that D2R delays also begin at the action frame, but there is no D2R code.
- **Impact timing (not asked, but relevant to the port):** the impact lands 60 frames after the action frame (`Missiles.txt` `meteorcenter` Range = 60). Basin says the same: "2.4 second (60 frame) delay between … action frame and impact". **MODEL-VERIFIED.**

### Q3. Interrupted before the missile frame: no delay, no mana

- **Interrupting modes delete the pending action event.**
  - `PLRMODE_StartXY_GetHit` (L840) and `PLRMODE_StartXY_Block` (L822) each call `UNITS_SetUsedSkill(pPlayer, 0)` and `D2GAME_DeletePlayerPerFrameEvents_6FCBCE50`. That function deletes `EVENTTYPE_MODECHANGE` and `EVENTTYPE_ENDANIM` (`SUnit.cpp` L1466).
  - So the action-frame event never fires. The do-function, the mana deduction (step 6.3) and `SetDelay` (step 6.4) never run.
  - Because Meteor has no start function, mana was **not** deducted at step 3 either.

  **DATAMINED.**
- **Is the interruption allowed?**
  - `sub_6FC81890` (L1594) permits GETHIT or BLOCK to replace CAST.
  - `D2GAME_PLRMODES_First_6FC7F340` (L82–150) lets any change through when the used skill's `interrupt` bit is set. Meteor has `interrupt` = 1 (bit mapped at `SkillsTbls.cpp` L516). The exception is `STATE_CONCENTRATION` (a roll) or `STATE_CONCENTRATE`.
  - **Player GetHit trigger** (`SUnitDmg.cpp` L2027–2031): `DAMAGERESULTFLAG_GETHIT` and (stunned, or the hit passes the `sub_6FCC1870` damage-vs-max-life threshold) leads to `sub_6FC817D0(…, mode 4 = GETHIT, …)`. **Stun on a player is applied through GetHit mode**, so it interrupts in the same way.

  **DATAMINED.**
- **Hit after the action frame:** the delay survives. `DeletePlayerPerFrameEvents` removes only MODECHANGE and ENDANIM, never REMOVESTATE, and nothing touches `STATE_SKILLDELAY`. **DATAMINED.**
- **D2R:** the same behaviour is **INFERRED**. There is no D2R code; D2R Meteor still has no `srvstfunc` and no `usemanaondo`.
- **This matches the J4b row-replay observation** in the gamora commit message (`c2431b3fd`): short-gap Meteors are "consistent with delay set only on a resolved action". In D2, a preempted Meteor leaves no delay.

### Q4. Cast with no target unit: legal, and the delay is set if the point is valid

- **Request side:** the location-cast handler `sub_6FC83340` requires only USABLE. It needs no target unit, and the mode is started with an (X,Y) path target. **DATAMINED.**
- **Do side:** `SrvDo028` → `sub_6FD15340` (`Skills.cpp` L3981) takes the target unit if one exists, otherwise `PathGetFirstPoint` (the clicked ground point). It returns false if:
  - the point is (0,0), or
  - `COLLISION_CheckMaskWithSizeXY(room, x, y, size, size, 5)` hits. Mask 5 = `COLLIDE_WALL` (0x1) | `COLLIDE_MISSILE_BARRIER` (0x4) (`D2Collision.h` L41/43). `meteorcenter` Size = 1.

  `D2GAME_CreateMissile_6FD115E0` (L1520) then fails if `UNITS_GetDistanceToCoordinates > 100` (L1549). That metric is max(|dx|,|dy|) + min/2 in unit coordinates (`Units.cpp`). **DATAMINED.**
- **Verdict:** an empty ground point gives a successful do-function, so mana is spent and the delay is set. An invalid point (wall or barrier, out of range, or no point) still plays the full cast animation, but `nResult` = 0, so **no missile, no mana, no delay**. **DATAMINED (1.10f); INFERRED for D2R.**
- **Port note:** if the J4b AI can aim at an invalid point, the D2-faithful outcome is a wasted cast animation with no delay. The port's contract would need a row for that case.
- **ERRATUM (KP-481 follow-up, same day):** this answer missed Meteor's start-time line-of-sight gate (`lineofsight` = 4, mask DOOR | MISSILE_BARRIER, `Skills.cpp` L2364-2408 and L2678). A point whose ray from her is blocked by a door or missile barrier is **aborted at start**, on the request frame, with **no animation**. Only the do-function failures above (collision at the point, distance > 100, no point) play the animation first. See `README-KP481-mana-debit.md`.

### Q5. Does D2 ever reset the delay? No; it only expires

- **Full-tree search of the pinned D2MOO** (17 MB shallow clone, every `.cpp` and `.h`):
  - `STATE_SKILLDELAY` appears only in `SetDelay` (`Skills.cpp` L1749/1758/1761), the check (`D2Skills.cpp` L1872) and the enum.
  - No call anywhere deletes `EVENTTYPE_REMOVESTATE` events.
  - A unit's whole timer list is cleared only in `PLAYER_Create` (`Player.cpp` L80) and `PLAYER_Destroy` (`Player.cpp` L140, leaving the game).
  - There is no level-change, act-change, waypoint or death reset. **DATAMINED (1.10f; negative search over the full tree).**
- **Name trap:** `EVENTTYPE_REMOVESKILLCOOLDOWN` (14) is unrelated to skill delays. Its callback `sub_6FCBDF90` (`SUnit.cpp`) clears the player's teleport-coordinate history, 50 frames after a position warp. **DATAMINED.**
- **Practical effect:** the delay is only 30 frames and level transitions take longer, so it lapses during any transition anyway.
  - If the port resets the delay at wave start, that is a port-side choice, not D2 behaviour.
  - The difference matters only if a wave starts fewer than 30 frames after a Meteor action frame.

  **INFERRED.**
- **D2R:** **UNKNOWN** at code level. Nothing in the 2.4 notes mentions a reset.

## Knowledge gaps not resolved

1. **D2R server code is closed.** Every timing, interrupt and no-target claim for D2R is INFERRED from 1.10f code plus unchanged D2R table fields and Basin's statement. The value (30) and local scope are DATAMINED for D2R.
2. **Same-frame ordering at F+30.** Within one game frame, it is not established whether event processing (state removal) runs before or after the incoming cast packets. A recast is possible on frame F+30 or F+31 (±1 frame). This was not resolved from the captured code. **RESOLVED (tie-order follow-up):** cast requests are processed between frame updates, under the game lock. A request is accepted at the earliest at stamp F+30 (the delay is removed during update F+30), and the new animation starts at F+31. See `README-tie-order-and-recast.md` § 2.
3. **25 frames per second** is not shown in the captured code. Grade: MODEL-VERIFIED via Basin's "1.2 s = 30 frames" and "2.4 s = 60 frames", which is consistent with the 60-frame Missiles.txt range.
4. **The `sub_6FC81890` CAST clause** `dwGameFrame <= ENDANIM-frame + 5` is not relied upon here. Only its explicit GETHIT/BLOCK disjunct is cited.

## Files
- `README-tie-order-and-recast.md`, `verify_tie_order.py` and `tie_order_facts.json`: the same-frame hit-vs-action order and the recast stamp (closes gap 2).
- `README-KP481-mana-debit.md`, `verify_mana_debit.py` and `mana_debit_facts.json`: the KP-481 follow-up (mana-debit timing for Fire Bolt, Fire Ball, Static Field and Meteor), plus the Q4 erratum.
- `captures/`: the D2MOO sources (`d2moo-*.cpp/.h`), `d2data/skills.json`, the Basin raw pages and the Blizzard 2.4 notes HTML. Their sha256 values are in `meteor_delay_facts.json`.
- `verify_meteor_delay.py` re-derives the values and line anchors. `meteor_delay_facts.json` is its output.
