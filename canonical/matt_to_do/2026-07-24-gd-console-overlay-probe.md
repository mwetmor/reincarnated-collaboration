# Matt to-do T8 — GD console overlay probe (the five-minute test)

**Raised:** 2026-07-24 by gandalf
**Revised:** 2026-07-25 — **v2, restructured as a three-rung ladder** after Matt hit the
Custom-Game precondition ("I can't make a custom game without a custom map").
**Status:** ✓ **DONE 2026-07-25.** Overlay read-out obtained — the anger overlay is a **directed
graph edge** (solid red mob→target line at the instant of commitment, correctly pointing at *other
mobs* during infighting), not the scalar the "number / bar / on-off" framing anticipated. That
framing was the wrong option space; the relational primitive is richer than any of its three
branches. `character.LogData true` prints green per-entity text carrying AI state and entity IDs.
Fixtures banked at `agentic_orchestration/gandalf/fixtures/2026-07-25-gd-anger-overlay/`.
**Successor: T9** — `agentic_orchestration/gandalf/pc-handoff/2026-07-25-gd-teleport-probe-directions.md`
(coordinates / teleport / the `SetPlayerInvisible` trial trigger).
**Why only Matt:** requires a running Grim Dawn on his PC. No agent can press a key in his game.

**PC-side copy (the operative one — self-contained, no repo access needed):**
`reincarnated` share → `agent-prompts/2026-07-24-gd-console-overlay-probe-directions.md`
**Screenshot drop:** share → `visual-artifacts/2026-07-24-gd-console-probe/`

---

---

## ✓ CONTAINER SOLVED 2026-07-25 — by Matt, and it beats every option we scoped

**An EMPTY folder inside `mods/`, opened as a Custom Game.** Console works;
`character.ShowAngerLevels true` toggles.

**Syntax correction: the argument is `true`, not `1`.** Both gandalf's v2 sheet and legolas's
report said `1`. Neither had verified it — it was inferred from the boolean-ish shape of the
command name. Recorded as a small instance of the same banked-inference shape.

**Why the empty mod is the *ideal* container, not merely an acceptable one.** Every option we
scoped — vanilla-passthrough copy, `ModdingTutorial`, Crucible — was an exercise in *which mod
changes the least*. An empty mod has **nothing to override with**: no `database.arz` exists in
it, so vanilla records load untouched. **Contamination is not mitigated; it is impossible by
construction.** That is a categorically stronger guarantee than verification-by-diff, and it
obtains the property gandalf's passthrough proposal would have bought with 280 MB of file copies.

**Design lesson worth keeping.** Both agents converged on "find the mod that adds the least" and
neither asked "what does the loader do when a mod adds *nothing*?" The search was framed as
*minimize the delta* when the available move was *make the delta not exist*. The null case was
outside the option space we generated — and it was reachable with `mkdir`.

**Open — must be resolved before any measurement is banked:** an empty mod ships no `Maps.arc`.
Which world does GD load? If it falls back to the main campaign world with normal spawns, this is
the cleanest instrument available and the arena question is closed too. If it loads a bare world,
the console is unlocked but we still need somewhere to point it. **Awaiting Matt's report.**

---

## What we're trying to learn

Whether `character.ShowAngerLevels` renders **a per-mob number**. GD mobs accumulate anger at
`SightAngerRate` 3.0/s outer and `InnerSightAngerRate` 12.0/s inner — a 4× ratio — and aggro on
threshold crossing. Resolving that ratio from vision tracking needs ~50 ms precision (hard,
expensive). If the overlay prints a number, the problem becomes OCR, and KPI 1 (aggro onset
radius) likely comes free, since onset *is* threshold crossing. **One screenshot decides between
a ~$0/hr instrument and a ~$31/hr one.**

## The v2 ladder — stop at the first rung that works

| Rung | Cost | What |
|---|---|---|
| **1** | 30 sec | **Press backtick in Campaign.** `Grim Dawn.exe` registers the full console command table *unconditionally*, `WidgetConsole::Render` bound to `accentgrave`, **no Custom-Game guard found in string data.** The "Custom Game only" claim came from 403'd community sources and may simply be false. |
| **2** | 2 min | **`autorun.txt`** in the install root containing `character.ShowAngerLevels 1`. The string appears in GD's init sequence *before* mod loading; Titan Quest (same engine lineage) uses it as a startup console script. Unconfirmed for GD. Fallback: the `/exec` launch flag, registered beside an "Executes a script" console command. |
| **3** | 15–30 min | **Build `ModdingTutorial` with the shipped `AssetManager.exe`.** Crate-authored, in-depot, and **defines zero controller records** — vanilla AI parameters pass through unmodified. Caveat: 2016 source vs the 2026-07 build; on build error Matt sends the error text rather than troubleshooting. |

**Command syntax correction:** the commands take an argument — `character.ShowAngerLevels 1`,
not the bare form. v1 of the sheet said the bare form.

## What is RULED OUT, and why it matters

- **Third-party overhaul mods (Grimarillion, Dawn of Masteries, Reign of Terror, …).** Every one
  ships its own `database.arz` — the exact file we froze and hashed, carrying the controller
  parameters under calibration. Measuring in one describes the mod, not the game, **while still
  producing plausible-looking numbers.** This is the commission's "instrument that changes the
  measured system" trap, and it fails silently.
- **The Crucible (`mods/survivalmode`)** — ruled out twice over. It is **not** in the Custom Game
  list (the exe hardcodes `tagPlayGameModeSurvival` as a separate mode with its own map-path
  handling), **and it is contaminated**: `ViewDistance` 80 vs vanilla 15–16 (5×),
  `MaxPursuitDistance` 125 vs 60–75, `distressCallRange` 50 vs 15–20 on 984/1083 creature records.
  175 controller records overridden in `SurvivalMode.arz` alone.

## Hypotheses I got wrong here — recorded, because the shape repeats

1. **"The tutorial's `TutorialWorld.map` is a 48-byte stub, so the tutorial isn't buildable."**
   False. I read `assets/Maps/` only; the world source lives in `source/Maps/TutorialWorld.wrl`
   (16,656 B) alongside `Region01.lvl` (1.2 MB). **The buildable path was in the install the whole
   time.** Same shape as the FoI/gdx1 error earlier this session: a conclusion drawn from a
   partial view of a namespace, stated as fact.
2. **The vanilla-passthrough mod — half right, half wrong.** Database side sound: mod `.arz`
   overrides matching vanilla records last-wins, so a byte-identical copy overrides every record
   with itself → zero delta. **Map side wrong:** `Levels.arc` is not usable as a mod's `Maps.arc`;
   the game expects a compiled world at `mods/<name>/resources/Maps.arc`. Also corrected: the mod
   ARZ must be named `database.arz`, not `<modname>.arz` (`SurvivalMode.arz` is a Crate-internal
   exception). **Routed to legolas before shipping rather than banked — the hypothesis was
   explicitly briefed as "confirm or destroy," and half of it was destroyed.**

## Read-out questions (unchanged from v1)

| Question | Decides |
|---|---|
| Number / bar / on-off? | OCR (~free) vs degraded vs CV-tracking (2 orders of magnitude more) |
| Per-mob or global? | Whether KPI 5 (distress-call propagation) is measurable at all |
| Legible at normal zoom? | Whether the protocol must constrain how Matt plays |
| Does `LogData` show position? | Direct onset-**distance** read vs pixel calibration — and GD's zoom is player-adjustable and the camera rotates, so calibration is genuinely messy |

## Related

- **Evidence base:** `agentic_orchestration/research/knowledge/gd/2026-07-25-gd-custom-game-console-unlock.md` (legolas — binary inspection of `Grim Dawn.exe`, modding-guide read, Crucible ARZ diff)
- Instrument scoping: `agentic_orchestration/research/knowledge/gd/2026-07-24-playtest-capture-instrument-scoping.md` § 2.4, § 8 item 8
- Commission: `agentic_orchestration/research/commissions/2026-07-24-gandalf-gd-playtest-capture-instrument-scoping.md`
- The five gaps this feeds: `agentic_orchestration/gamora/notes/2026-07-24-tsf6-track-a-run.md` § 3
