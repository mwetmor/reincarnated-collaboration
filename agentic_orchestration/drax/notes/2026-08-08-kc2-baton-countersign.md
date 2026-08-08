# KC2-SIM — baton/v1 WAYPOINTS BUNDLE, drax COUNTER-SIGN

**Author:** drax (demo / loadout / godot presentation seam)
**Date:** 2026-08-08 · KC2-SIM autonomous run, conductor gandalf, Phase D
**Counter-signing:** `src/reincarnated/export/MIGRATION.md` top entry, engine `28b578fe`
**Authority:** ADR-004 cross-seam handoff · § 11 signed surface · my coverage sign
`drax/notes/2026-08-08-kc2-baton-coverage-sign.md` (23 MUST + 5 SHOULD, the AC-11.3 acceptance bar)
**Evidence re-run from my seat:** `python3 -m pytest tests/test_baton_v1.py -q` → **86 passed**.
No `.py` touched. Engine tree carries gamora's uncommitted simulation work; nothing of hers read or
written.

---

## Verdict

**SIGNED, WITH ONE NAMED OBJECTION (OBJ-1) on `config.arena.path_coverage`.**

Ten of eleven rows counter-signed unconditionally, **including both breaking ones**. OBJ-1 does not
gate `28b578fe`; it gates the **Phase-E emit**.

## Per-item

| item | verdict | why, from the consumer seat |
|---|---|---|
| `positions_provenance` **str → object** (BREAKING) | **SIGNED** | Right call, and I'd have asked for it. A consumer cannot branch on prose. Back-compat cost **confirmed zero from my seam**: `grep -ril` over `reincarnated-demo/`, `reincarnated-loadout/`, `reincarnated-godot/` → **0 hits** for `baton_v1`, `positions_provenance`, `arena_ref`, `D-ARENA`. The `baton` hits in `reincarnated-godot/scripts/*.gd` are WR1/WR2 grading batons. Star-lord's claim holds. Cheapest hour this will ever cost. |
| `arena_ref` **new + REQUIRED** (BREAKING) | **SIGNED** | I want the `arena_archive` requirement specifically. 36 % p06 divergence on the arena declared for s1 = an emitter ring a third wrong. An honest `UNDISCRIMINATED` I can refuse to draw beats a map name I draw confidently and wrongly. |
| `actors[].path[]` carrying **`run_tick`** | **SIGNED — keep the deviation** | Exactly the join I want. Int-tick join against `circle_sweep`, never float `t_s` across a JSON round-trip. In GDScript that is the difference between a working `Dictionary` lookup and a silent miss. **Do not strike it.** |
| `path_model` / `path_interpolation` shipped IN the artifact | **SIGNED** | A rule in a note is a rule I get wrong in six months. In the wire it is a rule I read. |
| **`path_coverage`** | **OBJ-1 — OBJECTION** | See below. Measured. Zero-byte remedy. |
| Size ≈ 560 KB / 3.2 % on 17.4 MB | **SIGNED, not close** | My ≈ 22 MB is a *projection* from the coverage-sign note, not a cap; that note's real escalation threshold is **~100 MB** (sidecar/NDJSON split). 17.96 MB is fine. **Do not spend the `rows-compact` mitigation here — bank it** to pay for OBJ-1 if needed. |
| `arena_id` re-word · `fixture_p06_state_grade` · `u9_bonus_spawn_state` default · `D-ARENA-CITED` rename | **SIGNED** | I match on no declaration id today, so the rename is free. Struck-not-aliased is right — an alias lets the false claim keep validating. |

## OBJ-1 — the melee window has no position rule

Measured in memory off the emitted fixture wire, not asserted:

- monster lifetime ticks (spawn → death, else wave `tick_end`): **854**
- inside `[path[0].run_tick, path[-1].run_tick]`: **229**
- **no rule yields a position: 625 ticks = 73.2 %**
- monster-target event rows inside the span (`G-LOCO-ONE-TRAJECTORY` bites): **46**
- monster-target rows outside it (`baton_v1_validator.py:845` `continue`s): **339 = 88 %**
- all 13 actors: `path[-1].run_tick == engage_tick` exactly; death 17–65 ticks later

Three consequences: (1) `path_interpolation` says UNDEFINED there while `path_coverage` says it rides
the event rows — two shipped rules, two answers, and picking is the thing the artifact exists to stop
me doing; (2) at a post-engage tick with no row, neither rule yields anything, and the body is on
screen for 73 % of its life — so "REPLAY, never re-simulate" is not executable over most of the render
window; (3) 88 % of emitted monster positions are cross-checked by nothing, in exactly the window the
schema delegates to them, which also narrows my own signed § F.5 `_approach_audit()` obligation to
27 % of ticks.

**Remedy costs zero bytes** — the knots are already on the wire. Union `path[]` with the actor's own
emitted event positions (`target_x/target_y` where it is `target_id`, `source_x/source_y` where it is
`source_id`) under the same piecewise-linear `run_tick` law: **coverage 854/854 = 100 %, residual gap
0**. All 8 death rows carry `target_x`, so the terminal knot is free. Three edits, star-lord's to
make: re-word the two rule strings (UNDEFINED = pre-spawn + post-terminal only); stop the L845 skip so
the melee window has a falsification instrument at all; widen `Scene.actor_position()` and the
`R-LOCO-1-HITTEST` loop bounds so the reference semantics cover the window I render. If the sim's
post-engage motion turns out not to be piecewise-linear between sparse knots, that is the "more knots
are owed" result Option 1 was ruled on — emit them and spend the banked `rows-compact` mitigation.

## Obligations I accept (additional to coverage-sign § F.1–F.7)

- **O-1** Cast `run_tick` to `int` at the GDScript JSON boundary before any `Dictionary` key or
  `circle_sweep` join — Godot's JSON number typing is version-dependent, and keying uncast would
  reintroduce by accident the float-key failure `run_tick` was carried to prevent. Never key on `t_s`.
- **O-2** First loader reads `positions_provenance` as an object, branching on `emitter_geometry` and
  `arena_selection` separately.
- **O-3** Scene identity keyed on **(`arena_archive`, `arena_key`)**, never map name alone.
  `UNDISCRIMINATED` or `emitter_radii.grade == "SYNTHETIC"` suppresses emitter-ring VFX and says so on
  the banner.
- **O-4** Replay only. No position derived from `d_engage_m` + `player_path`, from `v_ref`, or from
  any re-simulation. Where the baton gives no position I render a visible UNDEFINED state and file it.
- **O-5** Default arms + `push_warning` on `path_model`, `path_target_policy`,
  `path_node_assignment_rule`, `fixture_p06_state_grade`, declaration ids.
- **O-6** Re-measure real artifact size on the first Phase-E emit; report the number whichever way it
  lands, against ~100 MB — not against a remembered 22 MB.

## Not raised as objections (named so the silence is deliberate)

- `path_model`'s home at `config.arena` vs `config.model` — I don't care; I read it either way.
- `G-` vs `AC-11.4x` id conventions — conductor's § 11 row-landing, not a consumer concern.
- The `arena_ref` enumeration being map-name-keyed — star-lord already routed it to the conductor and
  the schema requiring `arena_archive` protects me in the meantime. Sufficient.
