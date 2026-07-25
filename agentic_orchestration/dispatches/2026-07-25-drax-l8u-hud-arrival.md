# DISPATCH — TCP-L8-U: mode (ii) HUD ARRIVAL — the combat HUD, yours to design

**From:** gandalf (`RUN-CONDUCTOR`) · **To:** drax (presentation seam) · **Date:** 2026-07-25
**Authorization:** Matt, 2026-07-25 — L8 flipped to **(ii)-first**, running in parallel with L5/L7.
**Lap:** L8 UI (T4-UI). **This lap needs no new harness — a HUD is judgeable from a still.**

## §0 — Why this lap matters more than its size suggests

L8 is the program's **strongest untested case for the wire.** Every prior lap compared tools on
tasks where a script could always win on iteration cost. A HUD inverts the economics: at N≈12
controls with ~40 layout iterations, a **~150 ms wire nudge** competes against a **15–30 s script
edit → relaunch → screenshot** cycle. If the wire is ever going to win, it wins here.

**But this cell is the ARRIVAL, not the comparison.** You design the HUD. The three-tool comparison
runs afterwards against whatever contract your answer produces. **Your authoring clock is the datum**
that every later cell is measured against.

## §1 — The brief, verbatim and complete

> **"Author the combat HUD for this game. What is on it, where it sits, and how it reads at a
> glance — all yours."**

That is the entire spec. Layout, anchoring, what gets surfaced and what does not, theme, typography,
whether it is diegetic or chrome — **all yours**, each logged as a **veto-open ruling with
reasoning.**

## §2 — Your ancestry, and it is real

**This is `reincarnated-loadout/`'s home ground and it is YOURS** — you own that app. Read it. Read
the engine's actual systems rather than inventing a fantasy of them: the game is *Reap. Die. Rise.*,
a solo ARPG with elements, gear, skills, traits, and a **spirit guide**. `canonical/reap-die-rise-engine/`
and `canonical/reap-die-rise-story/` exist and are legitimate inheritance, exactly as a real UI
author would use them.

**Mode (ii) is NOT blind.** Production ancestry is yours to read. **Declare what you read.**

★ **The one thing I will insist on, because it is a design position and not a preference:** a HUD's
job is to answer *"am I about to die, and what can I do about it"* **in peripheral vision, during
combat, without being looked at directly.** Diablo II's orbs are readable as *shape* at the edge of
attention; a numeric readout is not. If you diverge from that, **diverge deliberately and say why** —
that is a ruling, not a mistake.

## §3 — Hard constraints (three, and only three)

1. **Your floor is `~/Games/mcp-lab/l8ui/` — a NEW project.** Create it.
   **`~/Games/mcp-lab/project/` is FORBIDDEN** — a blind L5a cell is live there.
   `~/Games/mcp-lab/l7vfx/` belongs to a concurrent cell. `~/Games/mcp-lab/harness/` is not needed
   and not yours this cell.
2. **The HUD is judged OVER GAMEPLAY, never on a grey card.** Composite it over a real 3D frame at
   the ARPG camera — the crypt is available (copy `~/Games/mcp-lab/project/scene_before.tscn` **out**,
   read-only, mode 0444 stays; verify sha `d45db0f507f6b835e14447c9ceb7e7e6bd645e070bc1fe1241dd6e8522de1966`
   at start and end). **A HUD that reads on a flat background and disappears over stone has failed
   the only test that matters.**
3. **Two resolutions, minimum** — a 16:9 desktop framing and one materially different aspect. Anchor
   behaviour under resize is most of what UI tooling is actually being tested on, and a layout that
   only works at one size is not a layout.

Method — H, the installed **W-MUR** wire, `.tscn` authoring, or any mix — **is yours**, logged as a
ruling. **L-J binds: W-PRO stays parked.**

## §4 — What you ship

1. **FIRST_INTENT banked verbatim + authoring-clock start, before any work** (TCP-32 — includes
   thinking).
2. **Stills over gameplay at both resolutions**, plus a **legibility argument you can defend**: at
   minimum, show the HUD over the *brightest* and *darkest* regions of a real frame. Contrast
   failures live in exactly the places a hand-picked screenshot avoids.
3. **A control-count + node-count census** — this is what the (i) comparison will be sized against,
   so it must be exact.
4. **Rulings, veto-open, with reasoning.** Read-list declared.
5. ★ **An ITERATION LOG** — how many layout passes it took, and what each one changed. **This is the
   lap's real payload**: the wire's case rests entirely on per-iteration cost, and nobody has ever
   measured how many iterations a HUD actually takes. Count them.
6. **Clock closed** — authoring separate from execution.

## §5 — Exit predicate

1. §4.1–§4.6 present. 2. Substrate sha + 0444 verified at start AND end. 3. `mcp-lab/project/` and
`mcp-lab/l7vfx/` demonstrably untouched. 4. `user://` clean; your project stays — it is the (i)
cells' floor.

**Honorable fallback (L-F):** an attributed blocker plus your best partial layout is a **PASS.**
**Ceiling-finding is a PASS (L-G).**

**Report to:** `agentic_orchestration/drax/notes/2026-07-25-tcp-l8u-hud-arrival-report.md`
**HALT to gandalf:** any need to touch another cell's floor; any finding that re-scopes the lap.
**HALT to Matt:** if the HUD design requires a game-systems decision that is not yet made — that is
a **story/design ruling**, not yours to invent, and inventing one would silently commit the project
to it.

**Signed:** gandalf, 2026-07-25 (`RUN-CONDUCTOR`). **Name anything in this dispatch that steered
you.** §2's Diablo II sentence is my prime suspect — I stated a design position on purpose, and if it
foreclosed an answer you would otherwise have reached, **that is a defect in my dispatch and I want
it on the record.**
