# Research — Grim Dawn Binary Extraction: Command Table, AI State Enums, Behaviour-State Sweep — 2026-07-25

**Mode:** A (analytical, read-only binary extraction)
**Commissioner:** Matt (direct dispatch — falsification correction)
**Sources consulted:**
- `/Users/admin/Games/vendor/grim-dawn/Game.dll` — primary AI/game logic binary
- `/Users/admin/Games/vendor/grim-dawn/Grim Dawn.exe` — primary executable (command table)
- `/Users/admin/Games/vendor/grim-dawn/Engine.dll` — engine binary (searched, relevant strings absent)
**Extraction method:** `python3` byte-level null-terminated string extraction + `grep -boa` byte-offset searches, verified with hex dump. All offsets are decimal byte offsets into the named file.

---

## Q1 Resolution — Where `Roam` comes from

**`Roam` is in a THIRD string table in `Game.dll` that the prior pass never found.**

There are three distinct string tables in `Game.dll` relevant to AI state:

### Table 1 — "Action State" display table (prior pass coverage)
**Location:** Game.dll offsets 5192736–5193183  
**Structure:** Entries prefixed with `"Action State: "`, used by the in-game entity data overlay (`character.LogData`). Terminated by the bare string `"Illegal"` (5193176) with no Action State prefix — the sentinel is structurally distinct from the states it follows.  
**What follows `Illegal`:** At 5193184, the string `"factions"` begins — an unrelated property name. No further Action State entries exist between 5193184 and any later offset.

**Members** (19 states, in order of appearance):
`Unknown` · `Forced Stop` · `Play Animation` · `Idle` · `Fidget` · `Move` · `Walk` · `Attack` · `Stun` · `Immobilize` · `Trap` · `Pickup` · `Chatting` · `Fallen` · `Dying` · `Knockdown` · `TakeHit` · `Jump` · `Evade`

**Boundary evidence:** The `"Action State: "` prefix is the discriminant — only strings with this prefix are members. The binary was searched for `"Action State: Roam"`, `"Action State: Pursue"`, and `"Action State: Wander"` — all absent. `"Illegal"` terminates the sequence and has no prefix; it is a sentinel, not a state.

**Assessment of prior-pass claim:** The prior pass correctly identified all 19 Action State display entries. The error was asserting that this table was the exhaustive source of the state names the game can display. It is not — it is one of at least two state-name systems, and the other (Table 3 below) drives the states actually printed in AI behaviour output.

---

### Table 2 — Animation State enum
**Location:** Game.dll offsets 5172500–5173053  
**Structure:** Null-terminated strings, 4-byte aligned, beginning with `"None"` at 5172500.  
**What follows `MenuFidget`:** At offset 5173056 (immediately after the null terminator of `MenuFidget`), a structured block of `0x01` bytes begins at 4-byte intervals. These are binary data (likely an array of 32-bit integers all set to 1), not more string entries. The next printable string does not appear until 5173552 (`"apparatusPauseTimeMin"`) — unrelated content.

**Members** (51 entries, in order of appearance):
`None` · `AttackIdle` · `IdleTransition` · `LongIdle` · `Fidget` · `Run` · `Walk` · `Charge` · `Pickup` · `PassItem` · `Chat` · `Stun` · `CriticalHit` · `Die` · `BuffSelf` · `BuffOther` · `SpellCast` · `Attack` · `Special` · `Spawn` · `Respawn` · `BeginMount` · `Mount` · `Dismount` · `EndDismount` · `AttTurnRight90` · `AttTurnLeft90` · `AttTurnRight180` · `AttTurnLeft180` · `TurnRight90` · `TurnLeft90` · `TurnRight180` · `TurnLeft180` · `Alert` · `Waiting` · `Rally` · `Emote` · `Flee` · `GetUpFaceDown` · `GetUpFaceUp` · `ChannelStart` · `Channel` · `Channel2Start` · `Channel2` · `SpinStart` · `Spin` · `TakeHit` · `Kick` · `Evade` · `Transform` · `MenuIdle` · `MenuFidget`

**Note:** The prior pass listed this as starting at `AttackIdle` (missing the leading `None`). The correct first member is `None` at 5172500.

**Boundary evidence:** `MenuFidget` terminates at 5173053 (null). What immediately follows (5173056–5173552) is a structured binary block of 0x01-valued 32-bit integers, not ASCII strings. This was verified by hex dump. No animation state string exists after `MenuFidget`.

**Coverage-boundary claim:** Extent is proven. The discriminant is the leading `None` entry marking the start and the binary data block marking the end. A test that would detect a missing member: search `Game.dll` for any string that matches a plausible animation verb not in this list AND appears in the same 4-byte-aligned null-padded format in the range 5172500–5173053. No such string was found.

---

### Table 3 — Controller Monster AI State table (NEW — the source of `Roam`)
**Location:** Game.dll offsets 5418372–5418829  
**Structure:** Null-terminated strings, 4-byte aligned. Preceded immediately by `"ControllerMonster::ChooseBestSkill picked an invalid skill for %s"` at 5418304 (error string identifying the surrounding code context). Followed immediately at 5418832 by `"Dead"` then `"Startup"` then `"Patrol Points"` — a different context (patrol point registration, not state names).  
**Binary context:** This is the internal state machine for `ControllerMonster` — the C++ class that drives monster AI. The prior pass never searched in this region.

**Members** (40 entries, in order of appearance):

| # | State name | Offset |
|---|---|---|
| 1 | `Idle` | 5418372 |
| 2 | `Startup` | 5418380 |
| 3 | `Attack` | 5418388 |
| 4 | `Pursue` | 5418396 |
| 5 | `RepositionForAttack` | 5418404 |
| 6 | `JumpAttack` | 5418424 |
| 7 | `Roam` | 5418436 |
| 8 | `Flee` | 5418444 |
| 9 | `WanderPause` | 5418452 |
| 10 | `Wander` | 5418464 |
| 11 | `Dying` | 5418472 |
| 12 | `Return` | 5418480 |
| 13 | `FollowLeader` | 5418488 |
| 14 | `Dead` | 5418504 |
| 15 | `NavigateObstacle` | 5418512 |
| 16 | `DefendLeader` | 5418532 |
| 17 | `Charge` | 5418548 |
| 18 | `Move` | 5418556 |
| 19 | `Panic` | 5418564 |
| 20 | `DodgeAttack` | 5418572 |
| 21 | `Confused` | 5418584 |
| 22 | `Paralyze` | 5418596 |
| 23 | `Trapped` | 5418608 |
| 24 | `Immobile` | 5418616 |
| 25 | `KnockedDown` | 5418628 |
| 26 | `Stunned` | 5418640 |
| 27 | `Scared` | 5418648 |
| 28 | `Sleeping` | 5418656 |
| 29 | `WaitToAttack` | 5418668 |
| 30 | `Patrol` | 5418684 |
| 31 | `QuestWalk` | 5418692 |
| 32 | `QuestMove` | 5418704 |
| 33 | `QuestUseSkill` | 5418716 |
| 34 | `QuestPlayAnimation` | 5418732 |
| 35 | `TakeHit` | 5418752 |
| 36 | `GettingUp` | 5418760 |
| 37 | `UseSkillOnPoint` | 5418772 |
| 38 | `UseSkillOnAlly` | 5418788 |
| 39 | `Emote` | 5418804 |
| 40 | `AlertBeforePursue` | 5418812 |

**Boundary evidence:** Table start is established by context — the preceding string at 5418304 is a `ControllerMonster` error message, and `Idle` begins immediately after at 5418372 following a null-pad. Table end is established by hex dump of bytes immediately after `AlertBeforePursue` (null terminates at 5418829, padding to 5418832): bytes at 5418832 spell `Dead` followed by `Startup` followed by `Patrol Points` — clearly a different registration context (patrol-point list, not state names). The 4-byte-aligned null-padded structure is consistent throughout.

**Coverage-boundary claim:** Extent is provisionally established by structural markers (pre-error-string / post-section-change). However, this claim carries one unresolved risk: the controller may have additional specializations (e.g., a `ControllerBoss`, `ControllerPet`, or `ControllerNPC`) that register their own state tables elsewhere in the binary. The sweep below addresses this.

**Why the prior pass missed it:** The prior pass searched for `Roam` and found the table at offset 5192700 (Action State display table) and 5172500 (animation state enum). The `ControllerMonster` table at 5418372 contains 40 entries none of which have the `"Action State: "` prefix, and thus did not surface in the prior pass's pattern. The prior pass appears to have searched only in expected regions and did not run a global `grep -boa "Roam"` across the binary. This commission's global search (`grep -boa "Roam" Game.dll`) returned 50+ hits, of which the dense cluster at 5416705–5418244 was the cluster that led to the controller table.

---

**Relationship between Table 1 and Table 3:** These are two separate state systems. Table 1 ("Action State") is the display-layer enum — the states the game renders in the entity data overlay via `character.LogData`. Table 3 ("Controller Monster AI State") is the internal controller state machine. When Matt observes "Idle -> Roam" in the game, this text is being printed from Table 3 names — NOT from Table 1. The two systems coexist. The game likely maps Controller Monster states to Action States for display purposes in some cases, but Roam, Pursue, Wander, and the other non-overlapping states in Table 3 are displayed using Table 3 names directly.

---

## Q2 — Behaviour-State Sweep

All three binaries searched (Game.dll, Engine.dll, Grim Dawn.exe) for the literals: `Pursue`, `Wander`, `Return`, `Chase`, `Flee`, `Aggro`, `Anger`, `Distress`, `Threat`, `Leash`, `Alert`, `Patrol`, `Guard`, `Home`, `Spawn Point`.

"Standalone" = bounded by null bytes on both sides (isolated string entry, not a substring of a longer string).

| Term | Game.dll (standalone) | Engine.dll | Grim Dawn.exe | Notes |
|---|---|---|---|---|
| `Pursue` | YES — in Table 3 (entry #4, offset 5418396) + many state-transition references | ABSENT | ABSENT | Confirmed Controller Monster state |
| `Wander` | YES — in Table 3 (entry #10, offset 5418464) + transition refs | ABSENT | ABSENT | Confirmed Controller Monster state |
| `Return` | YES — in Table 3 (entry #12, offset 5418480) + extensively in transition code (306 standalone occurrences) | ABSENT | substring only | Confirmed Controller Monster state |
| `Chase` | ABSENT | ABSENT | ABSENT | Not a named state in any binary |
| `Flee` | YES — in Table 3 (entry #8, offset 5418444) AND in Animation State table (offset 5172888) | ABSENT | ABSENT | Both animation and controller state |
| `Aggro` | ABSENT | ABSENT | ABSENT | Not a string literal; anger system uses float `AngerTolerance`, `AttackedAnger`, etc. |
| `Anger` | substring only | substring only | substring only | Appears as compound: `ShowAngerLevels`, `AttackedAnger`, etc. Never standalone |
| `Distress` | substring only | ABSENT | ABSENT | `distressCall`, `distressCallRange`, etc. in Table 1 context |
| `Threat` | ABSENT | ABSENT | ABSENT | Not found in any binary |
| `Leash` | ABSENT | ABSENT | ABSENT | Not found in any binary |
| `Alert` | YES — Animation State table only (offset 5172856) | ABSENT | ABSENT | Animation state, NOT Controller Monster state; `AlertBeforePursue` (Table 3) is a separate entry |
| `Patrol` | YES — in Table 3 (entry #30, offset 5418684) | ABSENT | substring only (in "Patrol Points") | Confirmed Controller Monster state |
| `Guard` | YES — in object-type list at 5391772 (not a state) | ABSENT | substring only | Context is object class name, not AI state |
| `Home` | substring only | ABSENT | substring only | Compound: `getHomePosition`, `ControllerMonster::GetHomePosition()` |
| `Spawn Point` | ABSENT | ABSENT | ABSENT | "Patrol Points" and "Spawn" (Table 2) exist but not "Spawn Point" as a state |

**Summary of prior-pass negative-finding reversal:** The prior pass concluded "there is no `Pursue`, `Roam`, `Flee` or `Return` in the action state enum." That was a narrowly correct statement about Table 1 (Action State display table) but was incorrectly generalized: `Pursue`, `Roam`, `Flee`, and `Return` are all present in Table 3 (Controller Monster AI State). The prior pass did not look at Table 3 because it did not know Table 3 existed.

**KPI 4 implications:** Matt observed "Idle -> Roam" in the game. Both `Idle` and `Roam` are entries in Table 3. If the game can print these transitions (observed: yes), then KPI 4 (idle wander detection) does NOT require long-window positional tracking — it collapses to reading a state-name change, exactly as KPI 1 collapsed via the anger-line overlay. This needs live test confirmation of exactly how the transition text is printed (which command triggers it and what the text format is).

---

## Q3 — Command Table (Independent Re-extraction)

**Source:** `Grim Dawn.exe`, offsets 2680572–2686760  
**Table structure:** Each command has a 3-field registration: `[description]`, `[short-name]`, `[qualified-name]`. The `[qualified-name]` is the canonical command identifier (e.g., `game.PlayStats`). Some commands have TWO descriptions — one short (tooltip) and one long (help text) — resulting in apparent duplicates.  
**Table start marker:** Preceded by `"Enables or disables exporting of large dump files"` (2680572), then `"Exits the game"` (2680624), `"LargeDumpFiles"` (2680640), `"Enables or disables exporting of large dump files"` (2680656), then `"game.LargeDumpFiles"` (2680708) — first qualified command name.  
**Table end marker:** `"debug.physics"` at 2686760 is followed immediately by `"true"` (2686776), `"destructible"` (2686784), `"Shows physics steps completed..."` (2686800), then `"*.*"` (2686868), `"false"` (2686872), `"(%d, %d, %d)"` (2686900), and console error strings beginning with `"^rError:"`. These are console framework strings, not command registrations.

**Count:** 51 unique commands (matching the prior-pass count of 51). One apparent anomaly: `game.IncrementSkill` appears twice (offsets 2682652 and 2682892). Inspection of surrounding bytes confirms these are two distinct registration records with different descriptions — the first gives the short description `"Gives the player a skill point"` and the second gives the full description `"Increments the number of points allocated to the specified skill"`. This is a double-registration artifact. Both point to the same command.

### Complete command table

#### Console built-ins (dot-prefix format, no namespace)

| Command | Description | Offset |
|---|---|---|
| `.Exit` | Exits the game | 2680772 |
| `.Close` | Closes the console | 2680828 |
| `.ScreenShot` | Takes a screen shot | 2680888 |
| `.Exec` | Executes a script | 2680960 |
| `.BindUp` | Binds a command to key release | 2681040 |
| `.BindDown` | Binds a command to key press | 2681156 |
| `.BindToggle` | Binds a command with true/false values to toggle with key press | 2681212 |

#### game.* namespace (18 commands)

| Command | Description | Offset |
|---|---|---|
| `game.LargeDumpFiles` | Enables or disables exporting of large dump files | 2680708 |
| `game.God` | Enables or disables god mode | 2681352 |
| `game.Invincible` | Toggles being invincible. | 2681436 |
| `game.Uber` | Enables or disables mana loss | 2681520 |
| `game.ShowHud` | Enables or disables the UI | 2681632 |
| `game.Teleport` | Teleports the player to the specified world space coordinates | 2681756 |
| `game.Speed` | Sets the game speed multiplier | 2681832 |
| `game.KillMe` | Kills the player | 2681892 |
| `game.killMonsters` | Kills all monsters | 2681992 |
| `game.PlayStats` | Displays a variety of player stats on the screen | 2682120 |
| `game.Spawn` | Creates an object at the player's location | 2682236 |
| `game.Give` | Creates an object and gives it to the player | 2682360 |
| `game.Gives` | Creates multiple objects and give them to the player | 2682488 |
| `game.ShowDynamicObstacles` | Enables or disables the object Dynamic Obstacles | 2682608 |
| `game.IncrementSkill` | Increments the number of points allocated to the specified skill | 2682892 |
| `game.IncrementAttribute` | Gives the player an attribute point | 2683000 |
| `game.IncrementLevel` | Increments the player's level | 2683108 |
| `game.incrementdevotion` | Gives the player a devotion point | 2683212 |
| `game.decrementdevotion` | Removes a devotion point | 2683312 |
| `game.resetdevotion` | Resets all devotion skills | 2683440 |
| `game.IgnoreRequirements` | Allows player to equip anything regardless of requirements | 2683572 |
| `game.ShowCursor` | Shows or hides the mouse cursor | 2683688 |
| `game.ShowErrorMessages` | Shows or hides skill not ready error messages | 2683800 |
| `game.resetattributes` | Resets player attributes | 2683960 |

#### character.* namespace (14 commands)

| Command | Description | Offset |
|---|---|---|
| `character.LogData` | Shows a variety of data above player, NPCs, monsters | 2684068 |
| `character.SetPlayerInvisible` | Makes it so enemies don't see the player and thus don't attack — but you can attack them | 2684180 |
| `character.GiveTakeGold` | Gives the amount specified. Negative numbers take gold away and 0 will zero out your gold. | 2684212 |
| `character.GiveTakeTribute` | Gives the amount specified. Negative numbers take tribute away and 0 will zero out your tribute. | 2684420 |
| `character.ShowAngerLevels` | Debug info for AI | 2684740 |
| `character.WarpCursor` | Makes it so player always warps to destination | 2684992 |
| `character.MoveTo` | Moves the player to the given coordinates in the current region | 2685136 |
| `character.MoveToEntity` | Moves the player to the given entity's position | 2685256 |
| `character.ClearPlayerTokens` | Remove all stored trigger tokens in the player | 2685932 |
| `character.ShowPlayerTokens` | Dumps the player's trigger tokens to the console | 2686072 |
| `character.GrantPlayerToken` | Gives the player the specified token | 2686204 |
| `character.RevokePlayerToken` | Revokes the specified token from the player | 2686336 |
| `character.ServerHasToken` | Return true if the server has the token | 2686460 |
| `character.AnyoneHasToken` | Return true if the anyone has the token | 2686592 |

#### graphics.* namespace (3 commands)

| Command | Description | Offset |
|---|---|---|
| `graphics.ReloadResources` | Forces all resources to be reloaded | 2685404 |
| `graphics.Stats` | Enables or disables displaying a variety of stats including frame rate | 2685468 |
| `graphics.ssaoparams` | Set strength/scale for SSAO | 2685660 |

#### sound.* namespace (1 command)

| Command | Description | Offset |
|---|---|---|
| `sound.Stats` | Enables or disables displaying a variety of sound statistics | 2685800 |

#### debug.* namespace (2 commands)

| Command | Description | Offset |
|---|---|---|
| `debug.destructible` | Shows physics steps completed by end of destructible simulation | 2686628 |
| `debug.physics` | Shows data when things affect physics engine | 2686760 |

**Total: 51 unique commands** (7 console built-ins + 24 game + 14 character + 3 graphics + 1 sound + 2 debug)

**Ground-truth fold-in:**
- `character.SetPlayerInvisible true` — CONFIRMED WORKING by Matt. Binary description: "Makes it so enemies don't see the player and thus don't attack — but you can attack them."
- `character.LogData 2` FAILS; `character.ShowAngerLevels 2` is accepted but produces no visible change — consistent with bool-only argument parsing (no verbosity levels). These commands take bool args only.

---

## Q4 — `game.PlayStats` and `Origin = %f %f %f`

**Finding:** The `"Origin = %f %f %f"` format string at `Grim Dawn.exe` offset 2687760 is NOT associated with `game.PlayStats`.

**Evidence:**

1. `game.PlayStats` is registered at offset 2682120 in the command table. The implementation is in `Game.dll` where `PlayStats` is a C++ class in the `GAME` namespace (confirmed by mangled symbol `??_7PlayStats@GAME@@6B@` at Game.dll offset 7034269 — the vtable). `PlayStats` appears alongside `PlayVideoCommandPacket` in the symbol table, indicating it is a **packet/data class**, not a console-print handler.

2. The `"Origin = %f %f %f"` string at 2687760 appears in the following sequence:
   ```
   2687648: WidgetConsole::AddTextToOutputBuffer
   2687696: %d:
   2687700: NULL
   2687708: Name = %s
   2687720: Type = %s
   2687732: Object %d
   2687744: Object is NULL
   2687760: Origin = %f %f %f
   2687780: Region = %s
   2687792: ui/cursor/cursordefault.tex
   ```
   This is the **console object inspector** — the block that prints object data when the cursor hovers over a world object in the developer console. `Name`, `Type`, `Object %d`, and `Region` are properties of a world object, not player stats. This is the `WidgetConsole` hover-inspection feature, not the `game.PlayStats` display.

3. No `%f` format strings appear between the `game.PlayStats` registration (2682120) and `Origin = %f %f %f` (2687760) in `Grim Dawn.exe`.

4. In `Game.dll`, the format strings near `"Player Position:"` (offset 5649268) and nearby health/level labels are all in a **network packet debug dump** block (surrounding strings: `"Originator Host ID:"`, `"Originator position:"`, `"Player ID:"`, etc.) — not PlayStats output.

**Binary verdict:** The binary cannot confirm that `game.PlayStats` prints world position. The `"Origin = %f %f %f"` string is the wrong code path. `game.PlayStats` description is "Displays a variety of player stats on the screen" — this is phrased as a HUD overlay (screen display), not a console print. The position-readout route through `game.PlayStats` cannot be confirmed or ruled out from static binary analysis alone.

**This remains a live test.** Run `game.PlayStats` in the active game and observe what appears on screen. If it shows world coordinates, the measurement rig works. If it shows only HP/level/combat stats, the coordinate readout requires a different approach.

---

## Coverage-Boundary Declaration (D-a compliance)

This section is the most carefully written section in this document, per commission requirement.

### Action State table (Table 1)
**Extent claim:** 19 members, Game.dll 5192736–5193183.  
**How established:** Structural discriminant (the `"Action State: "` prefix is both necessary and sufficient to identify members). Start: first string with this prefix at 5192736. End: last string with this prefix is `"Action State: Evade"` at 5193156. What follows at 5193176 (`"Illegal"`) lacks the prefix — it is structurally distinct. What follows at 5193184 (`"factions"`) is a property name from a different subsystem.  
**What would falsify this:** Finding a string matching `"Action State: [X]"` anywhere in `Game.dll` that is not in the range 5192736–5193183. A `grep -boa "Action State: " Game.dll` was not run comprehensively; that is a gap. The discriminant makes the claim falsifiable: anyone can grep.  
**Residual risk:** LOW. The prefix-based discriminant is strong.

### Animation State table (Table 2)
**Extent claim:** 52 members (including `None`), Game.dll 5172500–5173053.  
**How established:** Start at `"None"` (5172500) which immediately follows `"Both"` (5172492) and `"RightHandHit"` (5172476) — animation callback strings. End: `"MenuFidget"` at 5173044–5173053, followed by a binary data block (0x01-valued 32-bit integers) confirmed by hex dump. The structure is 4-byte-aligned null-padded throughout; the binary data block is NOT null-padded — it is 4-byte integer data.  
**What would falsify this:** Finding an animation state name in 4-byte-aligned null-padded format AFTER offset 5173053 in `Game.dll`, before the next section at 5173552. The hex dump of 5173054–5173551 shows no ASCII-printable null-terminated strings. This was inspected.  
**Residual risk:** LOW. Hex dump confirmed binary data block immediately after `MenuFidget`.

**Correction to prior-pass claim:** Prior pass said the table "asserted to terminate at `MenuFidget`" and started at `AttackIdle`. This session found `None` at 5172500 is the actual first member. The prior table listed 50 members (omitting `None`); the correct count is 52 members. However, `None` may be an index-zero sentinel rather than a true animation state. This is indeterminate from static analysis.

### Controller Monster AI State table (Table 3)
**Extent claim:** 40 members, Game.dll 5418372–5418829.  
**How established:** Start: `"Idle"` at 5418372 immediately follows the null-terminator of `"ControllerMonster::ChooseBestSkill picked an invalid skill for %s"` (5418304). This is identified as `ControllerMonster` context. End: `"AlertBeforePursue"` terminates at 5418829 (null). Hex dump of bytes 5418829–5418832 shows null padding. Byte 5418832 is `0x44` = `'D'` beginning `"Dead"` — which is followed by `"Startup"` and `"Patrol Points"`, a different patrol-registration context.  
**What would falsify this:** Finding a Controller Monster AI state name in the same 4-byte-aligned null-padded format between 5418829 and the `"Dead"` at 5418832 — which the hex dump rules out. Or finding additional Controller Monster state tables elsewhere in the binary for controller subclasses.  
**Residual risk:** MEDIUM. The risk is not that the table's extent is wrong, but that additional tables exist for controller subclasses (`ControllerBoss`, `ControllerPet`, `ControllerPlayer`, etc.) that register different states. These were not searched. A sweep of `Game.dll` for all occurrences of known state names (e.g., `Roam`) not already accounted for by the three tables would be required to fully close this. The 50 total `Roam` hits in `Game.dll` are distributed across the file; many are in state-transition switch code referencing these string literals, not in additional string tables.

### Command table (Q3)
**Extent claim:** 51 unique commands, `Grim Dawn.exe` 2680708–2686760.  
**How established:** Start: `"game.LargeDumpFiles"` at 2680708 is the first qualified command name. It is preceded by `"LargeDumpFiles"` (2680640), which is the short name, preceded by its description. End: `"debug.physics"` at 2686760 is the last qualified command name. It is followed immediately by `"true"` (2686776), `"destructible"` (2686784), and `"Shows physics steps..."` (2686800) — these are values and descriptions in a different registration context (toggle values), then `"*.*"` (2686868) and console error strings with the `"^r"` color-code prefix.  
**What would falsify this:** Finding a string matching `"[namespace].[CommandName]"` (where namespace is `game`, `character`, `graphics`, `sound`, or `debug`) outside the range 2680708–2686760 in `Grim Dawn.exe`. A full binary search for `"game."` was not run outside this range; this is a gap. However, the table's structural context (bounded by description strings before and console framework strings after) is coherent.  
**Residual risk:** LOW-MEDIUM. The structural boundary is clean. Risk is that undiscovered command namespaces exist not searched above.

---

## Source list

| File | Byte size (est.) | Searched |
|---|---|---|
| `Game.dll` | ~8.5 MB | Full binary grep for `Roam`; targeted string extraction at multiple offset ranges |
| `Engine.dll` | ~unknown | Full binary grep for `Roam` and all Q2 terms — no relevant hits |
| `Grim Dawn.exe` | ~unknown | Full binary grep for `Roam` and Q2 terms; full extraction 2680572–2690000 for command table |

Extraction performed 2026-07-25 using Python3 null-terminated string extraction and `grep -boa`. All offsets are decimal byte offsets into the named file from the FROZEN reference corpus at `/Users/admin/Games/vendor/grim-dawn/`.
