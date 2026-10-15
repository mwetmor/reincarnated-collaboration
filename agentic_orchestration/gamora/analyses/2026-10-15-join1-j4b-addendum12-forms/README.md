# JOIN-1 · J4b: the ADDENDUM-12 § 5 engine forms (gamora, 2026-10-15)

The forms were built in the engine, each commit ALONE (failing tests first, then code). All J4b suites pass, 129/129, in the dedicated worktree at engine `3248d176`.

| Form | Failing tests | Code |
|---|---|---|
| lock machine `d2/locks.py` | `7591b967`, `68f8cb8c` | `292a872c`, `62f02583` |
| streams / tapes `d2/streams.py` | `2a4fae4d` | `151af36c` |
| geometry `d2/geometry.py` | `35e127b5` | `1c1d2a12` |
| stamina (`sheet.py`) | `e68d8951` | `3ae7ccae` |
| chill counter + rebase (`laws.py`) | `e68d8951` | `f4d2e0cf` |
| dot_frames (`receivers.py`) | `e68d8951` | `3248d176` |

**Files:**
- **`locks_grid.json`:** the lock grid for the port mirror, 42 player + 8 monster scenarios. Inputs are float.hex, and `observed` is the form's output. It was emitted at `3248d176` with `emit_grid(SCEN, MON, P, L21)`, with the L-21 constants as pack rows and the attack timer set to freeze.
- **`tape_sample_M0_s0_block.json`:** a 100-value sample tape (`block:d2-fire-sorc`, M0 salt 0), showing the serving format.

Nothing here has been shipped to drax. The conductor releases.

## Re-emitted after CORRIGENDUM-4 (engine `ae5b67bb`; code `d071f249` / `3f54a448`; failing tests `e0973a8e`)
- **`locks_grid.json`:** L-21 is now RESET (`reanchor_at` = lock end).
- **`tape_sample_…`:** now on `block:d2-fire-sorc-c14`. The stream ids carry the kit id, so every seed changed.
- Emitted at engine `3f54a448`; J4b suites 129/129 in the dedicated worktree.

## Re-emitted after ADDENDUM-13 + CORRIGENDUM-1 (the L-21 world form)
- **`locks_grid.json`:** 56 scenarios, now including the Warlord's sources through the same trigger law, with the WORLD qualifying map in `l21.qualifying`.
- **New forms:**
  - `BodyLock.qualifying_hit` (engine `e4c0ab52`; failing tests `bac5b8b8`);
  - `ledger_pass` (engine `e003e656`; failing tests `b0db74e8`). Its own tests cover the mixed-ledger case.
- Emitted at engine `e003e656`; J4b suites pass in the dedicated worktree.
