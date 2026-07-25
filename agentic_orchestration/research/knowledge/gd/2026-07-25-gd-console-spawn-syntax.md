# Research — GD Console Argument Syntax (`game.Spawn` + toggles) — 2026-07-25

**Mode:** A (analytical) · **Commissioner:** Matt (direct; unblocks live probe)
**Companions:** `2026-07-25-gd-console-command-table.md` · `2026-07-25-gd-custom-game-console-unlock.md`

---

## Summary

The documented `game.Spawn` form is **one quoted, forward-slash, full record path including `.dbr`**:
`game.spawn "records/items/bonusitems/bonus_summonwisp.dbr"` (Crate forum, 2016 — DOCUMENTED-EXAMPLE).
Matt's four probe results are all consistent with a tokenizer that accepts an unquoted token only when it
contains no path separator; quoting is the fix and Matt has not yet tested it. Separately, **the spawn path
Matt used does not exist** — there is no `records/creatures/monsters/` tree in GD; monsters live under
`records/creatures/enemies/`. On the toggles: exported symbol signatures in `Grim Dawn.exe` show
`Character::ShowAngerLevels(bool)` and `Engine::CharacterCommandLogEnable(bool)` take **one bool**, while
`PlayStats::Display(void)` takes **zero arguments** — so `game.PlayStats true` is an arity error, and bare
`game.PlayStats` is the working form (which explains the panel appearing anyway).

---

## F1 — `game.Spawn` syntax — quoted, slashes, `.dbr`, ONE argument

**DOCUMENTED-EXAMPLE.** Crate Entertainment forum, "Console Commands Reference" (topic 32174), post #3 by
Grim_Dawg, 2016-05-07, verbatim:

> "File paths go between double quotation marks ("). On my keyboard (US layout) I have to type shift+' but
> the console registers this poorly so be careful. Example: game.spawn "records/items/bonusitems/bonus_summonwisp.dbr"
> […] Also, console is not capital letter sensitive."

Note the embedded warning: **the console registers the `"` keypress poorly on US layouts.** If Matt types
quotes and nothing changes behaviour, the quote character may simply not have been accepted into the input
buffer. Check the echoed line visually before pressing Enter.

**DOCUMENTED-EXAMPLE.** Same topic, post #2 by rorschachrev (the person who dumped the command table from the
exe): *"You can use autocomplete on files. Most arguments are an integer or series of integers."*
Secondary corroboration (G2A guide): typing a partial path displays a matching path and **Tab autofills it**.
This is the single most valuable probe affordance we have — it makes the console emit its own canonical
argument form.

**INFERENCE (high confidence).** The mangled symbol in `Grim Dawn.exe` @2934341 is
`?CreateEntity@GameEngine@GAME@@QAEXABVWorldCoords@2@ABV?$basic_string@…@Z` →
`void GAME::GameEngine::CreateEntity(WorldCoords const&, std::string const&)`. The console handler supplies
the player's `WorldCoords`; the command therefore takes **exactly one string argument**. No count, no level,
no team argument exists. Adding a second token will produce "Incorrect arguments".

**INFERENCE (medium-high).** Tokenizer model that fits all four of Matt's data points: an unquoted token is
accepted only if it is a bare identifier (alphanumerics + `.`); `/` and `\` make it un-tokenizable, so the
parser rejects before dispatch. `zombie01.dbr` passed because it is a bare identifier; it then failed
downstream at `TableDepot::Unable to open file (…)` because relative names are not resolved against
`records/`. Quoting is what the documented form uses, and is the untested cell.

---

## F2 — The record path Matt used does not exist (VERIFIED, primary source)

Parsed `~/Games/vendor/grim-dawn/database/database.arz` (34,114 records) with our own adapter. There is **no
`records/creatures/monsters/` subtree**. The complete `records/creatures/` layout is:

| Subtree | Record count |
|---|---|
| `records/creatures/enemies/` | 1,638 |
| `records/creatures/npcs/` | 445 |
| `records/creatures/pc/` | 24 |
| `records/creatures/anomalies/` | 20 |
| `records/creatures/testdummy*.dbr` | 5 (flat) |

**Verified-existing spawn targets** (all `Class = Monster`):

| Record path | What it is |
|---|---|
| `records/creatures/enemies/zombie_a01.dbr` | Common zombie; controller `records/controllers/enemy/controller_zombiea01.dbr` |
| `records/creatures/enemies/zombie_b01.dbr` | Common zombie (poison); **same** controller as `zombie_a01` |
| `records/creatures/enemies/zombie_c01.dbr` | Champion ("Fury") |
| `records/creatures/testdummy.dbr` | Static test dummy (also `testdummy_killable.dbr`, `testdummy_scaleable.dbr`) |

**Bonus — ground truth for the calibration read-out.** `controller_zombiea01.dbr` holds
`ViewDistance 15.0` · `SightAngerRate 3.0` · `InnerSightAngerRate 12.0` · `MaxPursuitDistance 75.0` ·
`PursuitTime 10000` · `WanderDistance 4.0`. Spawn `zombie_a01` and the live overlay should agree with these.

---

## F3 — Toggle/boolean convention: arity differs per command

**INFERENCE (high confidence, from exported symbol signatures in `Grim Dawn.exe`).** `_N` = bool, `XZ` = void:

| Console command | Symbol | Arg type |
|---|---|---|
| `character.ShowAngerLevels` | `?ShowAngerLevels@Character@GAME@@QAEX_N@Z` | **1 bool** |
| `character.LogData` | `?CharacterCommandLogEnable@Engine@GAME@@QAEX_N@Z` | **1 bool** |
| `character.SetPlayerInvisible` | `?SetInvisible@Character@GAME@@QAEX_N@Z` | 1 bool |
| `game.God` / `game.Invincible` | `?SetGod@…X_N@Z` / `?SetInvincible@…X_N@Z` | 1 bool |
| `game.ShowErrorMessages` | `?ShowErrorMessages@Character@GAME@@QAEX_N@Z` | 1 bool |
| **`game.PlayStats`** | `?Display@PlayStats@GAME@@QAEXXZ` (+ `?Dump@…XXZ`) | **ZERO args** |

This resolves the PlayStats anomaly cleanly: `game.PlayStats true` is an arity error, and the panel Matt saw
came from a zero-arg invocation. **Type `game.PlayStats` bare.**

**COMMUNITY-CLAIM, contested.** The token form for bools is `true`/`false`, space-separated. Topic-32174 OP:
*"Many of them work with true of false, example: > game.PlayStats true"* — but that OP explicitly admits
*"I was not able to find information about the parameters received by each of this commands"*, and we now know
that specific example is wrong. The one independent empirical report is post #4 (Spelbound, 2016):
*"'character.WarpCursor true' and '…false' turns this feature on and off."*
Binary corroboration: `Grim Dawn.exe` holds the literals `' true'` and `' false'` **with leading spaces** at
2687556/2687624/2687632/2687640, adjacent to `WidgetConsole::Render` — exactly the strings `.BindToggle`
would append to build `<command> true`. So `true`/`false` is engine-constructed and should parse.

**Unresolved conflict, flagged not averaged.** `character.SetPlayerInvisible true` is recorded as confirmed
working by Matt, yet `character.ShowAngerLevels true` errored — both are 1-bool commands. Meanwhile
`character.ShowAngerLevels 2` was accepted and `character.LogData 2` was not. No source explains this.
Probe both `true` and `1`.

---

## F4 — Mode gating and spawned-monster behaviour

- **DOCUMENTED-EXAMPLE.** Console is Custom-Game-only: topic-32174 OP, *"go to a custom game (it dosen't work
  in the main campaing)"*. Post #21 (Hellows, 2021) adds a second gate: *"the console only shows up in single
  player mode. I always run host server in my worlds so it wasn't working."* — do not host a server.
- **NOT FOUND.** No source — primary, secondary, or tertiary — documents whether console-spawned monsters
  aggro, grant XP, or drop loot normally. Searched Crate forums, Steam discussions, Reddit, guide sites.
  Treat as a live observation for Matt's next sitting, not a known.
- **NOT FOUND.** `character.ShowAngerLevels` accepts a bool per signature, but no source documents whether it
  needs `game.Spawn`ed monsters vs. world-placed ones.

---

## Next probe commands — priority order

Console: Custom Game, single-player (not hosted), backtick/`~`. Commands are case-insensitive.

```
1.  game.PlayStats                                              # zero args — F3 predicts this works bare
2.  character.ShowAngerLevels true                              # then, if "Incorrect arguments":
3.  character.ShowAngerLevels 1
4.  character.LogData true                                      # then, if it errors:  character.LogData 1
5.  game.Spawn records/creatures/                               # type this, DO NOT press Enter — press TAB
                                                                # the console autofills its own canonical form.
                                                                # SCREENSHOT WHAT IT PRODUCES. This is the
                                                                # highest-value single action of the sitting.
6.  game.Spawn "records/creatures/enemies/zombie_a01.dbr"       # the documented quoted form
7.  game.spawn "records/creatures/testdummy_killable.dbr"       # fallback target if 6 parses but nothing appears
```

On step 6: **look at the echoed input line before pressing Enter.** Per Grim_Dawg, US-layout `shift+'` often
fails to register in the console buffer. If the `"` is missing on screen, paste the line from clipboard
instead (Ctrl+V into the console) rather than retyping.

If step 6 parses but nothing spawns, the failure has moved from parser to `TableDepot` — report the exact
`TableDepot::Unable to open file (…)` string, since it echoes the resolved name and tells us what prefix the
resolver expected.

---

## Knowledge gaps not resolved

- No community-documented `game.Spawn` example targeting a **creature** record was found anywhere; every
  documented example spawns an item. The creature case is untested in public sources.
- The exact console tokenizer rule (why `/` rejects) is inferred, not observed. Only a disassembly of the
  arg-parse routine, or the Tab-autocomplete output from step 5, will settle it.
- No source on spawned-monster aggro/XP/loot fidelity.
- FearlessRevolution's console-enabler thread (a likely-rich source) returns 403 to agent fetch.

## Source list

| Source | Type | Accessed |
|---|---|---|
| `forums.crateentertainment.com/t/console-commands-reference/32174` (full 22-post thread, JSON API) | Primary — community, incl. binary-dump author | 2026-07-25 |
| `gamerant.com/grim-dawn-console-command-list-help/` | Tertiary — guide site | 2026-07-25 |
| `g2a.com/news/features/guide/grim-dawn-console-commands-cheats-guide/` (via search index) | Tertiary — guide site | 2026-07-25 |
| `steamcommunity.com/app/219990/discussions/0/1457328927848941160` | Tertiary — no working syntax | 2026-07-25 |
| `fearlessrevolution.com/viewtopic.php?t=10727` | Not retrievable (403) | 2026-07-25 |
| `~/Games/vendor/grim-dawn/Grim Dawn.exe` — mangled-symbol + console-string extraction | Primary — binary | 2026-07-25 |
| `~/Games/vendor/grim-dawn/database/database.arz` — 34,114 records via `gd_arz_adapter_2026_07_24.py` | Primary — game data | 2026-07-25 |
