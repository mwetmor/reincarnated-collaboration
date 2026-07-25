# GD probe #2 — coordinates, teleport, and the invisibility trigger

**For:** Matt, at the PC, in the empty-mod Custom Game with the console working
**From:** gandalf
**Date:** 2026-07-25
**Est. time:** 10–20 min. Stop at the first rung that gives a clean answer; the later rungs
are only there if the earlier ones fail.

**Screenshot drop:** the `reincarnated` share → `visual-artifacts/2026-07-25-gd-teleport-probe/`

---

## 0. Terminology I got sloppy about — "open the console"

When I said *"open the console and hover over a monster,"* I meant **the same thing you have
already been doing**: press the **backtick / tilde key** (`` ` `` — above Tab, left of 1) to
bring up the command line where you typed `character.ShowAngerLevels true`.

There is no second, deeper, developer-only console. One console, one key. When I say "with
the console open," I mean the command line is on screen and accepting input.

Sorry for inventing a mode that doesn't exist.

---

## 1. Why this probe matters more than the last one

The anger-line probe answered *"can we see it?"* — yes, and better than hoped: the red line is
a **relationship**, not a number. It tells us who is angry at whom, which is richer than any
scalar readout would have been.

This probe answers a bigger question: **can we stop watching and start running experiments?**

Right now the plan is "Matt plays, something records, we analyse the footage." That means
waiting for the game to happen to produce a clean measurement. If teleport works, the plan
changes shape entirely:

> Kill everything in an area → spawn one known monster → teleport yourself to an
> **exactly known distance** from it → become visible → time how long until the red line
> appears.

That is not observation. That is a **controlled trial with a set independent variable**. And
critically, it **deletes the hardest technical problem in the whole program**: we would no
longer need to estimate distance from pixels (camera zoom is adjustable, the camera rotates,
elevation changes break the mapping — it was going to be genuinely messy). If we *set* the
distance, we never have to *measure* it.

So: this is the highest-value 15 minutes available to us right now.

---

## 2. Safety first — read this before typing anything

- **Do not do this on a Hardcore character.** Obvious, but stated.
- **Teleporting to a bad coordinate can drop you inside terrain or off the map.** The reliable
  escape is the **world map / rift fast-travel** — that always relocates you to a valid spot,
  regardless of where you ended up. Know where your nearest rift is before you start.
- **Before you begin, note where you are** (nearest rift name / zone name). If a teleport goes
  wrong, fast-travel out; don't try to walk out.
- Nothing in this probe writes to the database or modifies anything persistent. Worst case is
  a stuck character, fixed by fast-travel.

---

## 3. THE LADDER — stop at the first rung that works

### Rung 0 — Can we READ a coordinate? *(30 seconds, do this first)*

Everything else gets easier if this works.

1. Open the console (backtick).
2. **With the console still open, move the mouse cursor over a monster** and hold it there.
3. Watch for text appearing — in the console area or on screen — of roughly this shape:

```
Object 78642
Name = ...
Type = ...
Origin = 1234.56 12.00 -678.90
Region = ...
```

**What I'm looking for is the `Origin =` line with three numbers.** That is a world-space
position. If it prints, we can read any entity's exact location, and Rung 3 becomes trivial.

Try hovering over: a monster, an NPC, a destructible barrel, a wall, the ground. It's possible
the inspector only responds to certain object classes.

**Report:** did anything print on hover? Screenshot if yes. If nothing at all prints, say so —
a clean negative is a real answer and we move to Rung 1.

---

### Rung 1 — `character.MoveToEntity` *(the safe one — no coordinates needed)*

This is the rung I most want to work, because it requires knowing **nothing** about the
coordinate system.

1. `character.LogData true` — the green text appears above monsters.
2. **Find the entity ID** in that green text. It should be a number in square brackets, like
   `[78642]`. (If you're not sure which number is the ID, screenshot the green text and I'll
   point at it.)
3. Move somewhere you can see a monster at a distance.
4. Open console, type: `character.MoveToEntity 78642` (using the ID you actually read).

**Expected:** you are relocated to that monster's position.

**Report:**
- Did it move you? To the monster, or somewhere else?
- Any error text in the console?
- Did it work on a monster in a **different room / across the map**, or only nearby ones?
- Does it work on an entity you can't currently see?

**Why this matters even though it puts you at distance ≈ 0:** it proves the game will
relocate the player on command, it proves the entity IDs in the green text are usable as
handles, and combined with Rung 3 it gives us a way to get *near* a target before positioning
precisely.

---

### Rung 2 — `character.MoveTo` *(arity probe — cheap, do it while you're here)*

We don't know how many arguments this takes. The binary help says *"Moves the player to the
given coordinates in the current region"* — note **current region**, so these are probably
region-local, not world coordinates.

1. Type `character.MoveTo` with **no arguments at all** and press Enter.
2. **Screenshot whatever error prints.** Console error messages usually state the expected
   argument count and types, which is exactly what we want to learn.
3. If it prints a usage string, follow it. If it prints nothing useful, try `character.MoveTo 0 0`
   and then `character.MoveTo 0 0 0` and note which one is rejected.

Also worth doing for `game.Teleport` before Rung 3 — a bare `game.Teleport` may print its
expected arguments and save us guessing.

---

### Rung 3 — `game.Teleport` *(the payoff — needs a coordinate from Rung 0 or 1)*

Binary help text: *"Teleports the player to the specified world space coordinates."* Three
floats: `game.Teleport <x> <y> <z>`.

**Do NOT guess absolute coordinates.** Don't try `game.Teleport 0 0 0` — that's the world
origin and is very likely inside terrain or in void. We work by **relative displacement from
a coordinate we actually read.**

#### 3a. If Rung 0 worked (you can read `Origin`)

1. Hover a monster, read its `Origin = X Y Z`. Write the three numbers down.
2. `game.Teleport X Y Z` — using those exact numbers. **Expected: you land on the monster.**
   This confirms the coordinate system is shared between the hover-read and the teleport.
3. Now the axis test: from that same monster's origin, try each of these in turn, returning
   to the monster between each:
   - `game.Teleport (X+20) Y Z`
   - `game.Teleport X Y (Z+20)`
   - `game.Teleport X (Y+20) Z`

   **What we learn:** two of these should move you horizontally along the ground. One should
   put you 20 units in the air (or underground). **Report which axis is the vertical one.**
   My expectation — stated so you can prove me wrong — is that **Y is up** and X/Z are the
   ground plane, because this engine descends from Titan Quest. But I have not verified it,
   so treat it as a guess.

#### 3b. If Rung 0 failed but Rung 1 worked

1. `character.MoveToEntity <id>` to land on a monster. You now know you are *at* its position,
   even though you don't know what that position is numerically.
2. That's not enough for `game.Teleport` on its own — we still have no numbers. **In this
   case, skip 3a and go straight to § 4**, which works fine on MoveToEntity alone.

---

## 4. THE ACTUAL EXPERIMENT — and the trick that makes it work

Here is the thing I want you to try even if the teleport rungs are messy, because it may be
the single most useful capability we've found:

**`character.SetPlayerInvisible` is an experiment trigger.**

You already confirmed it works — monsters stop noticing you and drop to `Idle` / `Roam`. That
means the sequence is:

1. `character.SetPlayerInvisible true` — you are now a ghost. Monsters ignore you.
2. **Position yourself precisely** while invisible — walk, or teleport, to exactly where you
   want to be relative to a monster. Take all the time you need; nothing reacts to you.
3. `character.ShowAngerLevels true` and `character.LogData true` — overlays on.
4. **`character.SetPlayerInvisible false`** — and *that instant is the start of the trial.*
5. Count / record until the red line appears and the monster commits to pursuit.

Step 4 is the part that matters. Every measurement we need has the shape *"how long after X
does Y happen"* — and until now we had no clean **X**. Walking toward a monster gives you a
fuzzy start instant. Flipping visibility gives you a **sharp** one.

**Please try this once and report:**
- **Does anger reset when you go invisible?** Specifically: let a monster aggro on you (red
  line up), then `SetPlayerInvisible true`. Does the line drop immediately? Then go
  `false` again — does it re-aggro **instantly** (anger was retained) or after a **delay**
  (anger was reset to zero)? This one answer determines whether the whole trial design above
  is valid or has to be redesigned.
- **Roughly how long** between going visible and the red line appearing, when you're standing
  a moderate distance away? A rough count is fine — "about a second," "instant," "two or
  three seconds." I'm not asking for precision here, only an order of magnitude.
- **Does distance change that delay?** Stand very close vs. fairly far. My expectation, again
  stated so you can falsify it: **close should be about 4× faster than far.** If it's the
  same either way, that tells us something important and I'd rather know now.

---

## 5. Two more commands worth a 30-second try

| Command | What to check |
|---|---|
| `game.PlayStats` (no arguments) | It says "Displays a variety of player stats on the screen." **Does any of it look like a position / coordinate?** I don't think it will — I believe it's a HUD overlay of character stats — but if it prints coordinates, it solves Rung 0 outright. Screenshot whatever appears. |
| `game.killMonsters` (no arguments) | Clears the area. Confirm it works and that it's local (nearby only) rather than map-wide. This is the "reset the experiment" button, so I want to know its blast radius. |

---

## 6. What to send back

In rough order of value to me:

1. **Rung 0 result** — does hovering print `Origin`? Screenshot either way.
2. **Rung 1 result** — did `character.MoveToEntity <id>` relocate you? Any error text?
3. **The § 4 invisibility question** — does anger reset when you go invisible and come back?
4. Screenshot of the green `character.LogData` text at readable zoom, **so I can identify
   which number is the entity ID.**
5. The axis answer from Rung 3a, if you got that far.
6. `game.PlayStats` screenshot.

If a rung fails, **say it failed and stop** — don't troubleshoot. A clean "it errored, here's
the error" is worth more to me than a workaround, because the error text is itself data about
how the command expects to be called.

---

## 7. What I do NOT know here, stated plainly

Two of us — me and legolas — have now each shipped a confident claim about these commands that
turned out wrong (`1` vs `true` was the last one, and you found it). So, explicitly:

- **I do not know the argument count for `character.MoveTo`.** Rung 2 is a probe, not a test.
- **I do not know which axis is vertical.** The Y-up guess comes from engine lineage, not
  from evidence.
- **I do not know whether the units in `game.Teleport` are the same units as the monster
  parameters we pulled out of the game's database.** They probably are, but "probably" is
  exactly the kind of assumption that has bitten this project four times in a week. If the
  teleport rig works, we test it: put yourself at a set offset from a monster and check
  whether the red line appears at the boundary the database predicts. If it does, the units
  are confirmed and we have measured a real number instead of guessing one.
- **I do not know whether the hover-inspector needs something enabled first.** If plain
  hovering prints nothing, that's a negative worth recording, not necessarily a dead end.
