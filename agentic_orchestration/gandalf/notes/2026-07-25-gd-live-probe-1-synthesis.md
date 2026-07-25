# GD Live Probe 1 — synthesis of Matt's PC results (T9 round 1)

**Author:** gandalf (SPEC-AUTHOR), 2026-07-25
**Raw evidence (governs):** `research/knowledge/gd/live-probe-1/GD-console-notes-matt-raw.md` + two banked screenshots + three full-res screenshots Matt sent in-session (console error lines read directly)
**Probe sheet executed:** `gandalf/pc-handoff/2026-07-25-gd-probe2-SIMPLE-checklist.md` (T9 round 1)

---

## 1. Three live state-name confirmations — the T4 oracle WORKS

The console/anger overlay displays `ControllerMonster` state names **verbatim** during play.
Matt observed, live:

| State | Context | Status vs holdings |
|---|---|---|
| **`AlertBeforePursue`** | Yelling zombies, pre-pursuit beat | **CONFIRMED** — the D-b telegraph state's live existence, exactly as predicted on the probe sheet |
| **`Startup`** | Buried / prone "dead" zombies rising before attack; "very common" | **CONFIRMED + grounded** — Startup's live presentation is the dormant-spawn unearthing beat |
| **`followtheleader`** | Boss fight | **CONFIRMED** — pack-hierarchy family (FollowTheLeader) exists in live combat, boss-adjacent |

**Consequence:** every inferred state-transition binding in G1-C can get its one live
confirmation through this readout. The live game is functioning as the bankable oracle the
twin analysis (§ 4) requires — no instrumentation beyond the console overlay needed for
state-name verification.

## 2. The scarcity observation CORROBORATES the census binding (independently)

Matt: *"I haven't found enough instances of AlertBeforePursue yet… so far it doesn't feel
different based on range."*

Elrond's census (same day, independent lane): `EmoteBeforePursuingChance` — non-zero on 93.0%
of controllers, **mode 20**. If the binding is right, the alert beat fires ~**1 in 5** spots.
Matt's difficulty *finding* instances is exactly what a 20%-chance parameter predicts. And
"doesn't feel different based on range" fits the binding's structure: the anger **rates**
govern *when pursuit triggers*; the emote itself is a chance-gated beat, not a range-scaled
duration. The scarcity IS the evidence. (Binding remains labelled INFERENCE — this is
convergent corroboration, not proof; exit condition still open.)

## 3. Spawn rig — FAILED as tested, with a precise diagnosis from Matt's screenshots

Empirical ladder (console lines read from the full-res screenshots):

| Attempt | Result |
|---|---|
| `game.Spawn` (no args) | `Error: Incorrect arguments` |
| `game.Spawn records/creatures/monsters/zombie/zombie01.dbr` | `Error: Incorrect arguments` — **rejected at the parser**, never reaches entity creation |
| `game.Spawn records\creatures\…` (backslashes) | same parse-level error |
| `game.Spawn zombie01.dbr` (bare token) | **PASSES parsing** → `GameEngineInboundInterface::CreateEntity(): Trying to create zombie01.dbr` → no spawn (record not resolvable by relative name) |
| (arg literal `true`) | `CreateEntity(): Trying to create true` → `TableDepot::Unable to open file (true)` |

**Reading:** single tokens reach `CreateEntity` and are handed to `TableDepot` as record
paths; slash-containing paths die at argument parsing. Leading hypothesis (UNBANKED): the
tokenizer splits on path separators or requires quoting — `game.Spawn "records/…/zombie01.dbr"`
is the top retry candidate. **Routed to legolas Mode A** (community-documented working
examples) rather than banked — five banked-inference failures this week; this is the sixth
candidate and it stays a hypothesis.

**Additional syntax finding:** `game.PlayStats true` / `game.playStats true` /
`character.ShowAngerLevels true` ALL produced `Incorrect arguments` errors — yet the
PlayStats panel displays and the anger overlay evidently ran. The `<command> true` folk
syntax is wrong or partial; the working toggle form is part of the legolas commission.

## 4. Rig-shape verdict — L0 IS RUNNABLE NOW, spawn is a convenience not a blocker

Confirmed instruments:

- **`character.WarpCursor true`** *(as noted by Matt — worked)*: instant, whole-screen hops.
  **Aggro-on-pass: YES** — warping past a monster pulls it, and may trigger respawns.
  Positioning tool with a pull hazard; warp into position BEFORE approaching the target.
- **`game.killMonsters`**: instant kill of all on-screen monsters — the **trial reset /
  field-isolation tool**. Clear the field, then engage one fresh zombie.
- **`game.PlayStats` panel** (screenshot-verified fields): Play Time · deaths · **kills** ·
  potions used · max level · *Damage per second* (read 0.00 at capture — interpretation open:
  windowed/instantaneous, needs an in-combat capture) · **Skills Used with per-skill counts**
  (`defaultweaponattack.dbr : 9`) · Life healed · Shield block chance. An **aggregate session
  ledger** — kill-delta + skill-use-delta per trial; NOT per-hit damage.
- **Per-hit damage**: not yet demonstrated. `character.LogData true` console lines during a
  fight is the open question for round 2 (the captured console shows level-streaming + quest
  Lua lines, no damage lines — but no fight was in progress at capture).

**L0 world-monster rig (available today):** killMonsters to clear → walk/warp to a fresh
zombie → PlayStats screenshot before → fight to death → PlayStats screenshot after → console
screenshot (state names + any LogData lines). No spawn command required. The spawn-identity
rig remains preferable for *known-record* fixtures (and for J4 level-controlled HP/OA/DA
calibration) — pending legolas syntax findings.

## 5. Register/queue updates made with this synthesis

- Twin note § 6 gap 1 (T9 items 1–3): **round 1 DONE** — WarpCursor ✓, PlayStats ✓ (aggregate),
  killMonsters ✓ (bonus), Spawn OPEN with diagnosis + legolas commission in flight
- Twin note § 6 gap 4 (unit calibration): PlayStats ledger + LogData round-2 question noted
- `matt_to_do` T9 row: round 1 complete; round 2 sheet (SIMPLE v2) on the pi share
- Probe sheet v2: `gandalf/pc-handoff/2026-07-25-gd-probe3-SIMPLE-v2.md` → share copy

**Signed:** gandalf, 2026-07-25. The oracle answered; three states stood up and named themselves.
