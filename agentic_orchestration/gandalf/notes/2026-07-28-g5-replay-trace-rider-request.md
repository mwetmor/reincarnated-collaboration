# RIDER REQUEST — G-5 harness: emit a replay-grade trace as a side artifact

**From:** gandalf (TCP / suite-architecture session, 2026-07-28)
**To:** gandalf (`RUN-CONDUCTOR`, run `KC1-2026-07-27` / KIT-CAL-1) — **delivered by Matt** (the
only legitimate channel into a running conduction; this is new input at a phase boundary, not an
edit to a launched cell — L-R respected)
**Authority:** Matt directive, 2026-07-28, this session. Veto-open to the receiving conductor as
run-internal sequencing always is; the fallback in §4 exists so a veto costs the program little.

---

## §1 — The ask, in one sentence

Before G-5's harness assembly freezes, add a **non-gating** emission rider: the harness writes a
**replay-grade trace** of each scenario run as a side artifact, so the TCP program can later render
the werewolf battle in Godot **without re-running G-5**.

Non-gating means exactly that: no exit predicate changes, no band changes, no calibration-verdict
dependency. If the rider threatens G-5 timing in any way, see §4 before dropping it.

## §2 — Why now, and why through you

The TCP suite-architecture session has chartered (Matt-approved in principle, shape "C+capstone")
a **REPLAY integration capstone**: engine emits a battle trace → Godot consumes and renders →
MP4. It is the first live evidence cell for the T6 seam fork (engine-side emission vs Godot-side
generation — the product's actual serial-content architecture) and the first cell where the two
programs meet: the sim that must be right, rendered by the pipeline that must be felt. Ground
truth arrives with the content — the render is judged against the sim's own measured series, so
verification is nearly free (the instrument-dominance law working for us, uniquely).

The only expensive path to that cell is retro-fitting: if G-5 runs without the trace, the capstone
requires re-running a chartered calibration finale with pre-registered A/B arms (R-KC1-18) — a
re-run for presentation reasons, which would be both wasteful and epistemically ugly. One
commission line now buys the option permanently.

Asset gate already cleared on our side: Matt located **Synty POLYGON — Werewolf**
(`SM_Chr_Werewolf_01`, rigged, 51 bones, 1.97 m humanoid height, 2 meshes / 2 materials). The
capstone's protagonist exists.

## §3 — Trace contents (constraints, not format — format is gamora's call within these)

Per scenario run (each tier, each A/B arm), a machine-readable stream (JSON-lines or equivalent),
schema-versioned, deterministic given the seed:

1. **Header:** run id, scenario tier, arm (A/B), seed, kit id (`gd-werewolf-kitcal-1`), opposition
   roster (record paths), schema version.
2. **Per-tick entity state** (or per-event with tick deltas — gamora's efficiency call): entity
   id, archetype/tier, position from the spatial layer, hp/max_hp, alive flag; facing if the
   spatial layer holds it.
3. **Events, timestamped:** spawn · skill activation (claws / charge / transform — the charge
   path matters: it is the L6∩L7 trail case) · hit (attacker, target, post-mitigation damage,
   channel) · crit · **leech heal** (the O-d door already receives the kernel's `on_lifesteal`
   event — this rider is a second consumer of an event that exists) · death · engagement
   boundaries (whatever grain H-1 ratified).
4. **Nothing derived** — raw series only; the consumer computes.

Cost read from your own ledger: the kernel events exist (`damage_resolver.py` `on_lifesteal`;
spatial layer holds positions and hp), so this is plausibly a writer in the harness driver, not a
mechanics change. If gamora prefers, star-lord's telemetry/export seam is the natural owner of
the writer — your sequencing call.

## §4 — Honorable fallback (pre-registered, so a veto is cheap)

If the rider cannot ride G-5 itself: **decouple** — after G-5's verdict lands, a follow-up
emission pass re-runs **only the canonical arm** (post flip-rule) with the writer attached, same
seeds. This costs one re-execution of settled scenarios, not a re-litigation of the run — but it
is strictly worse than riding along (a second execution is a second chance for drift), which is
why the ask is now, before harness assembly completes.

## §5 — What the receiving conductor should NOT take on

The replay cell itself — its charter, sequencing, gates, and the Godot side — stays in the TCP
program (capstone after TCP Waves α/β; it will not jump the queue). This rider asks KIT-CAL-1 for
exactly one thing: **don't let the trace evaporate.** Everything else is ours.

**Signed:** gandalf (TCP session), 2026-07-28. Veto-open, as always.
