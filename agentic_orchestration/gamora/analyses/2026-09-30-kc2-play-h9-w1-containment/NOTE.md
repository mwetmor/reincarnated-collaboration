# H-9: the oracle's W1 containment under separation (prereg v1.9 § F.2j)

**STATUS:** evidence record · **Date:** 2026-09-30 · **Author:** gamora · **Run:** KC2-PLAY
**Class:** NOT-A-GRADED-RUN. It reads the oracle only: no oracle file was edited and nothing was tuned
(Law 3). No sealed cell was opened (K-7). The oracle is engine `266714dd`, whose `simulation/` and
`data/` are byte-identical to `96b4529a`.

## Verdict: OUTCOME 1, PASS

The oracle stays inside `R_wall = 43.758085029822276` m on every salt, with **zero** body clamps and
**zero** player clamps. `TA-X-10` and `TA-X-11` grade as written.

## Configuration

- **Cell:** P-n.3's `PW-FOLDED`: `SEALED-KMILL | SEP-ON`, with `contact_response='separate'` and
  geometry ON.
- **P-5:** the loader call `load_profiles(dot_corrections=True, winner_surface=from_x8(P-n.2),
  pool_lift=load(), c11a=C11aLoader(CLASS))`, plus `simulate_wave(c11a_corrections=C1+C2+C4)`.
- **W1:** the arm of record, `ArenaFold(armed=True, avoidance=True)`.
- **Salts:** 0–4.
- **R_wall:** recomputed from v3.6.1 `arena.json` as `max‖spawn‖ + placement_extents_m`, which
  equals the prereg value.

## The configuration is shown to be the right one, not assumed

With the arena fold absent (`M-POL-2`), and again disarmed (`W1-NULL`), the harness reproduces P-n.3
`PW-FOLDED` exactly:

- terminal waves `[156, 152, 155, 152, 152]`;
- seconds into the terminal wave `[7.184, 4.408, 7.02, 7.184, 6.122]`.

`W1-NULL` ≡ `M-POL-2` behaviourally, as `TA-X-04` requires.

W1 was run twice and gave byte-identical per-salt numbers both times, so the run is deterministic.

## W1, Leg A: stop at the player's first death (the graded semantics)

| salt | `max_body_radius_m` | margin to R_wall (m) | clamps body / player | terminal wave | max radius after a separation push (observation) |
|---|---:|---:|---|---:|---:|
| 0 | 43.404802385345796 | 0.353283 | 0 / 0 | 156 | 40.729753 |
| 1 | 41.97652009526441 | 1.781565 | 0 / 0 | 152 | 39.492579 |
| 2 | **43.40481520803243** | **0.353270** (the minimum) | 0 / 0 | 155 | 40.738023 |
| 3 | 41.97652009526441 | 1.781565 | 0 / 0 | 152 | 39.492577 |
| 4 | 43.40478928727287 | 0.353296 | 0 / 0 | 155 | 40.726218 |

## W1, Leg B: death-continued through w160 (a superset, sensitivity only)

- **Maximum:** 43.408257252633014 m on salt 1, a **margin of 0.349828 m**.
- **Clamps:** 0 / 0 on every salt.

## What the numbers mean

- **Separation does not bring any body near the wall.**
  - Over 1,622–6,948 displacements per salt, the largest post-push radius is 40.78 m.
  - No position after a separation push lies beyond R_wall.
  - The maximum is set by a body spawned at the rim of p01's box and measured after its first inward
    step.
  - This reproduces the sealed `[W1W]` maximum (43.404994665356945) to about 2e-4 m.
- **The margin is thin but structural.** About 0.353 m equals roughly one inward step at spawn. It is
  not a draw.
- **The premise in `clamp_body`'s docstring** ("no fold drives a body outward") is false in mechanism,
  but inert in measurement on this board.
- **Informational only (TA-X-06 relation, not graded):** W1's terminals differ from M-POL-2's on
  salt 0 (6.286 s vs 7.184 s into w156) and on salt 4 (w155 vs w152). The avoidance veto moves the
  fight.

## Files

- `h9_w1_containment.py`: the harness. It composes `make_runner`, `upn4._overrides` and
  `ArenaFold`. Its only patches are observation patches, restored in `finally`.
- `h9_out_W1.json`, `h9_out_M-POL-2.json`, `h9_out_W1-NULL.json`: the outputs.
