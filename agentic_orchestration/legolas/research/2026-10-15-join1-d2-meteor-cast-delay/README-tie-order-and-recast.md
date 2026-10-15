# Same-frame tie order (incoming hit vs her action frame) and the recast stamp after the Meteor delay (2026-10-15)

**Commissioner:** gandalf (JOIN-1). The questions:
1. When a GetHit-causing hit and her action-frame event fall on the same game frame, which runs first? ADDENDUM-4 § 3 resolves incoming hits before her action, and 4 graded Meteors sit on that tie.
2. Settle `README.md` gap 2: after a Meteor delay set at frame F, does the recast land on F+30 or F+31?

**Pin:** D2MOO `5596f5cb6c5251a0a07c6637d26458b06099d516` (1.10f). Cited files are in `captures/` and are byte-identical to the pin.
**Re-derivation:** `python3 -I verify_tie_order.py` re-finds every line anchor below and asserts the orderings. It writes `tie_order_facts.json`; the last run had 0 failures.
**Read-only. No graded-margin file opened.** I do not know the hit vehicle of the 4 tie Meteors; the rule below is stated by vehicle so the conductor can apply it.

**D2R caveat:** everything below is 1.10f code (DATAMINED). D2R's server is closed, so the same ordering in D2R is **INFERRED**. D2MOO notes `GAME_UpdateProgress` = 1.14d `Game.0x52D870`; that identifies the function, it does not prove the order.

## 1. Tie order: it depends on how the hit is delivered

**The frame skeleton.** `GAME_UpdateProgress` (`Game.cpp` L1790) does `++pGame->dwGameFrame` (L1794) and then `EVENT_IterateEvents(pGame)` (L1868). `EVENT_IterateEvents` (`Event.cpp` L179) runs the timer buckets **in a fixed order**:

| Order | Bucket | Lines |
|---|---|---|
| 1 | **missiles**: every-frame list, then this-frame slot | L186, L187 |
| 2 | **players**: every-frame list, then this-frame slot | L190, L191 |
| 3 | **monsters**: every-frame list, then this-frame slot | L194, L195 |
| 4 | objects, then items | L198–L203 |

A slot timer fires only when `nExpireFrame == dwGameFrame` (L219). **DATAMINED.**

**Her action frame is a player-bucket event.** It is the `EVENTTYPE_MODECHANGE` timer scheduled at cast start (`SUnit.cpp` `sub_6FCBCE70`), dispatched through `sub_6FC81600` (`PlrModes.cpp` L1422) → `sub_6FC80EE0` → the skill handler (missile, mana, delay). **DATAMINED.**

**Cancellation is a mode change.** A player GetHit is started from the damage path (`SUnitDmg.cpp` L2031, inside `SUNITDMG_ExecuteMissileDamage` L1934). `PLRMODE_StartXY_GetHit` (`PlrModes.cpp` L840) deletes her pending MODECHANGE / ENDANIM timers (`SUnit.cpp` L1466). So whichever runs first on the tie frame decides the outcome. **DATAMINED.**

### 1a. Missile-delivered hits (monster projectiles): the hit runs first, and the cast is cancelled

- Each missile carries an **every-frame** timer, created with `nExpireFrame = -1` and placed in the every-frame list (`Missiles.cpp` L54 → `Event.cpp` L514, L409).
- That timer runs `MISSMODE_SrvDoHandler` (`MissMode.cpp` L5194). For a basic missile, this leads to `MISSMODE_HandleMissileCollision` (L4866), then `MISSMODE_SrvDmgHitHandler`, then `MISSMODE_SetDamageFlags`, then `SUNITDMG_ExecuteMissileDamage` (L4760), and finally GetHit.
- All of that happens in **bucket 1**, before the player bucket. Her action event has already been deleted when bucket 2 runs: **no missile, no mana, no delay.**
- **This matches ADDENDUM-4 § 3.** **DATAMINED.**

### 1b. Melee / do-function hits (a monster's own action frame): her action runs first, and the skill fires

- A monster's attack resolves at **its** action-frame event, in **bucket 3** (`MONSTERMODE_EventHandler`, `MonsterMode.cpp` L2126).
- `SKILLS_SrvDo001_Attack_LeftHandSwing` (`Skills.cpp` L2025) queues the combat (L2064) and applies it immediately (L2074) through `SUNITDMG_DrainItemDurability` (a misnamed melee executor, `SUnitDmg.cpp` L2283). That calls `SUNITDMG_ExecuteMissileDamage` (L2388), then GetHit.
- Her player-bucket event has already run by then, so **the Meteor fires (missile, mana, delay)**. The GetHit then starts recovery, and the delay survives it (see `README.md` Q3).
- **This is the OPPOSITE of ADDENDUM-4 § 3.** **DATAMINED.**
- One branch is not traced: `SrvDo001` applies damage immediately only when `!STATES_CheckStateMaskOnUnit(pUnit, 38)`. Otherwise it sets `UNITFLAG_SKSRVDOFUNC` and defers. I did not follow which states are in mask 38. Grade: UNKNOWN for that branch.

### 1c. A monster missile spawned on the tie frame cannot hit on that frame

- A missile created during bucket 3 of frame t gets its every-frame timer pushed onto the missile list (`Event.cpp` L528), but bucket 1 of frame t has already run. **Its first update and collision is at frame t+1.**
- So "a monster fires at her and she casts on the same frame" resolves in her favour on frame t. **DATAMINED** (the ordering structure). I did not trace a full missile creation for an at-spawn collision path; a grep of `MISSILES_CreateMissileFromParams` found no damage call.

### 1d. Other damage sources

- Monster aura or periodic skills run on monster `EVENTTYPE_PERIODICSKILLS` / `PERIODICSTATS` timers, which are monster-bucket events, so they come after her action. **INFERRED** (bucket placement read; individual skills not traced).
- Object traps run in bucket 4, after her action. **INFERRED.**

### What this means for the port

| Hit vehicle on the tie frame | D2 1.10f outcome | ADDENDUM-4 § 3 |
|---|---|---|
| Projectile already in flight | hit first → GetHit → **her cast is cancelled** (no missile, mana or delay) | agrees |
| Monster melee swing (its action frame) | **her cast fires** (missile, mana, delay), then GetHit | disagrees |
| Monster spawning a missile this frame | her cast fires; the missile moves from t+1 | disagrees, if the port counts it as a same-frame hit |

The correct verdict for each of the 4 tie Meteors depends on which vehicle delivered the hit. A single rule that hits always resolve first is D2-faithful only for projectiles already in flight.

## 2. Recast after the Meteor delay: the request is accepted at stamp F+30, and the first animation frame is F+31

**How the delay is removed.**
- `D2GAME_SKILLS_SetDelay_6FD11C00` sets the expiry to `nDelay + dwGameFrame` = F+30 (`Skills.cpp` L1746). It schedules a player-bucket `EVENTTYPE_REMOVESTATE` timer at F+30.
- During update F+30 that timer runs `STATLIST_UpdateStatListsExpiration` (`MonsterMode.cpp` L2094), which frees the statlist because `dwExpireFrame <= nFrame` (`D2StatList.cpp` L1855).
- **By the end of update F+30 the delay is off.** **DATAMINED.**

**Requests are never processed in the middle of a frame.**
- Cast requests enter through a separate export, `GAME_ProcessNetworkMessages` (`Game.cpp` L1694), which calls `CCMD_ProcessClientMessage` (L1715; `CCmd.cpp` L218).
- That function takes the game's critical section (`GAME_GetGameByClientId` L2378 → `GAME_LockGame` → `D2_LOCK` L2445) and runs the packet handler **immediately** (`CCmd.cpp` L234).
- Frame updates take the same lock (`GAME_UpdateGamesProgress` L2154 → `GAME_UpdateProgress` L2173).
- So a request always sees the state **as of the last completed update**, and `dwGameFrame` equals that update's number. **DATAMINED.**

**What a request sees, by stamp:**
- **Stamp F+29** (processed after update F+29): the delay is still on. `SKILLS_GetUseState` returns `SKILLUSTATE_BLOCKED` (`D2Skills.cpp` L1605). `sub_6FC83340` (`PlrMsg.cpp` L812) starts a cast only on `USABLE` (L847), sends a message only on `NOMANA`, and otherwise returns 2. **The request is dropped, not queued**; the client has to send it again. **DATAMINED.**
- **Stamp F+30** (processed after update F+30): the delay is off, so the request is **accepted, and the cast mode starts at stamp F+30**. `sub_6FCBCE70` starts from `nFrame = dwGameFrame` (`SUnit.cpp` L1475) and does `++nFrame` before the first animation step (L1498). **The new cast's first animation frame is processed in update F+31**, and its action event fires at F+30 + n, where n is the frames-to-action counted from the request stamp. **DATAMINED.**

**Verdict:**
- The earliest recast is **accepted at F+30**, not F+31.
- Its animation begins at F+31.
- The minimum Meteor action-to-action interval is **30 + n**, which agrees with Basin's "interval = action frame + delay" (`README.md` Q2).
- **DATAMINED (1.10f); INFERRED (D2R).**

**What is still open, and why it does not change the stamp:**
- **Host loop order: UNKNOWN.** Whether the host (the single-player client's local server, or D2Server) drains network messages before or after the update within one wall-clock tick is not in D2MOO; those binaries are not reconstructed. It changes only real-time latency, not the rule "a request is accepted iff its stamp is at least F+30".
- **Client-side gating: UNKNOWN.** The client keeps its own copy of timed states, counting expiry down per client frame (`D2StatList.cpp` L1850, the `nFrame == 0` client branch). It may hold the request until its own copy lapses. The client code is not reconstructed, so any lag of a frame or so is unknown. For an AI-driven port with no client, the server rule above is the faithful one.

This closes `README.md` gap 2. The ±1 there is resolved in favour of acceptance at F+30 for the server.
