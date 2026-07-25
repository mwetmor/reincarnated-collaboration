# Matt to-do T8 — GD console overlay probe (the five-minute test)

**Raised:** 2026-07-24 by gandalf
**Status:** READY TO RUN
**Time:** ~5 minutes, plus however long it takes to find a mob pack
**Why only Matt:** requires a running Grim Dawn on his PC. No agent can press a key in his game.
**PC-side copy:** `reincarnated` share → `agent-prompts/2026-07-24-gd-console-overlay-probe-directions.md`
(self-contained; no repo access needed). **Screenshot drop:** share → `visual-artifacts/2026-07-24-gd-console-probe/`

---

## What we're trying to learn

Grim Dawn has a debug console command, `character.ShowAngerLevels`, documented in exactly five
words: *"Debug information for AI."* Legolas could not find a single screenshot, video, or
firsthand account of what it actually renders — the Crate forum 403'd, and no aggregator shows it.

**Anger is the hardest thing we need to measure.** GD's mobs accumulate "anger" toward the
player at `SightAngerRate` 3.0/s in the outer view zone and `InnerSightAngerRate` 12.0/s in the
inner zone — a 4× ratio — and aggro fires when anger crosses a threshold. Resolving a 4× ratio
from *watching mobs move* needs roughly 50 ms timing precision, which is a hard and expensive
computer-vision problem.

If `ShowAngerLevels` prints **a number per mob**, that entire problem becomes "read the number."
And aggro onset radius (the other headline KPI) probably comes free, because onset *is* anger
crossing threshold — so we'd get two of the five gaps from one overlay.

**One screenshot decides between a $0/hour instrument and a $31/hour one.**

## The steps

1. **Launch Grim Dawn.**

2. **Get to Custom Game.** Main menu → the Custom Game / mod-launch path. *(See the note below
   on why this is needed — and why it's less of a problem than I first made it sound.)*

3. **Open the console.** Press **tilde** `~`. If nothing happens, try **apostrophe** `'`.

   ⚠ **This is the one step nobody could confirm from a primary source.** If neither key opens a
   console, **stop** — don't hunt. Tell me what you saw and I'll have legolas pin the exact
   procedure from Crate's own forum before you spend more time on it.

4. **Type:** `character.ShowAngerLevels` and press Enter. Close the console.

5. **Walk toward a pack of ordinary trash mobs** — nothing special, ideally 3+ of them so we can
   see whether the overlay is per-mob or global. Stop just as they notice you.

6. **Screenshot.** Then take a second one from closer in, mid-fight.

7. **Now type:** `character.LogData`, close the console, and **screenshot again** near the same
   mobs. This one is documented as *"displays a variety of data above player, NPCs, and monsters."*
   If it shows world coordinates, it's worth as much as the anger overlay.

8. **Drop the images** into the share at `visual-artifacts/2026-07-24-gd-console-probe/` (folder
   already created — no need to report a path; I read it from the Mac side).

## What I'm actually reading out of those images

| Question | Why it decides something |
|---|---|
| Number, bar, or on/off indicator? | A **number** → OCR, near-free, high precision. A **bar** → still usable, degraded. **On/off** → we fall back to computer-vision tracking, and the cost goes up by two orders of magnitude. |
| Per-mob or one global readout? | Distress-call propagation (KPI 5) needs to know *which* mob woke. A global readout can't answer it. |
| Legible at your normal zoom? | If it only reads at maximum zoom-in, the capture protocol has to constrain how you play. |
| Does `LogData` include position? | If yes, aggro-onset **distance** becomes a direct read instead of a pixel-calibration estimate — and legolas established that GD's camera zoom is player-adjustable and rotates, so the estimate route is genuinely messy. |

**If it turns out to be numeric and per-mob:** a short screen recording of you walking toward a
pack until they aggro would be worth more than any further research I could commission. Don't
bother yet — screenshots first.

## Bonus observation, if it's cheap

Does mob behaviour *feel* different in Custom Game versus your normal save — spawn density,
how quickly things notice you, pack composition? Your read is the only oracle we have on that.
Not a blocker (see below); just useful.

---

## "Why bother with Custom Game mode at all?" — the answer

**Your instinct is right, and I overstated the risk.** Here's the corrected picture.

**Custom Game is a container, not a rules change.** The AI parameters we're calibrating against
(`ViewDistance`, `SightAngerRate`, `MaxPursuitDistance`, `PursuitTime`, and the rest) live in the
`.arz` archives, and those load identically either way — we have the bytes, frozen and hashed,
and there is only one set of them. What a container *could* plausibly change is which mobs spawn
where and how zones seed. That would affect our **sampling**, not the parameter values.

**And we already hold the control.** TSF6-TRACK-A established that pursuit distance is
parameter-faithful in our sim to +0.15%, against a `MaxPursuitDistance` we read straight from the
`.arz`. So the moment you're in Custom Game, we can measure one mob's leash and compare it to the
number we already know it should be. **If the leash matches the file, the container is clean** —
and if it doesn't, we've learned something more interesting than we were looking for. We don't
have to *worry* about contamination; we can *test* it, cheaply, using ground truth we already own.

**The bigger point, which is the one you were reaching for.** If Custom Game is where modding
lives, that's not a hazard — **it's a laboratory.** Free play was never going to produce clean
measurements anyway: aggro-onset radius needs repeated approach-until-noticed runs at controlled
distances, and distress-call propagation is a 75%-chance event that needs dozens of trials to
estimate a rate. You cannot get either by playing normally and hoping. A purpose-built arena —
one known mob type, known spawn point, flat open ground, repeatable — is exactly what the
measurement needs, and Custom Game is the door to it.

So the honest revision: **Custom Game isn't a tax we pay to get the console. It's probably where
the real measurement work happens.** The console is just the first thing we found behind the door.

---

## Related

- Research: `agentic_orchestration/research/knowledge/gd/2026-07-24-playtest-capture-instrument-scoping.md` (§ 2.4 the console commands; § 8 item 8 — the undocumented-overlay boundary this test closes)
- Commission: `agentic_orchestration/research/commissions/2026-07-24-gandalf-gd-playtest-capture-instrument-scoping.md`
- The five gaps this feeds: `agentic_orchestration/gamora/notes/2026-07-24-tsf6-track-a-run.md` § 3 (gap register)
