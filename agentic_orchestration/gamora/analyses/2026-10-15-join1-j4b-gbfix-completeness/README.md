# JOIN-1 · J4b: completeness on the corrected GB (godot a381c21), under jack-ryan's POST-HOC (P) + (i)/(ii) form (gamora, 2026-10-15)

- **Inputs:** `/Users/admin/Games/join3c-bulk/gb-fix/arms/`.
  - All 105 pins in `evidence/join1/j4b-hook/gb-fix/grains_sha256.json` verified first (pin file sha256 `1a17de52…`).
  - Against the `2ca2298` pins, only GB and JOIN-PROVENANCE changed (20 files).
  - G1–G7: 70 / 70 match `manifest-port.json`.
- **Grader:** engine `a99d2af3` (`completeness_restated` and the ruling-2 checks), with failing tests `93c40dea` committed first. Run in the dedicated worktree.
- **The CORR-4 test stays recorded FALSE AS PRE-STATED.** This is the post-hoc rule jack-ryan stated in collab `826520a1d`.

## (1) Precondition (P), computed independently: PASS on both arms (all 50 cells)

| | Targets without a span | Records outside their target's span |
|---|---|---|
| her, new GB | 0 | 0 |
| his, new GB | 0 | 0 |
| her, old GB (`2ca2298`) | 204 | 55 |
| his, old GB (`2ca2298`) | 0 | 35,292 |

My "outside" count is `on ≤ t < off`, so it includes records before `on_tick`. That explains 55 here against jack-ryan's 53.

## (2) Completeness under (i)/(ii): PASS. All 63 orphans are TERMINAL (her 3, his 60)

For every orphan:
- the last tick at which any body (roster or pet) is alive in its cell equals the orphan's tick, so (i) holds;
- the target's death tick equals the orphan's tick, so (ii) holds.

The full per-orphan table is in `orphans_63.md`.

## (3) Effect gate (b) and flinch duty, old GB vs new GB
- **Gate (b), own movement in a window:** 0 violations on every arm, with both the old and the new GB. Gates (a) and (c) also PASS on the new GB.
- **Flinch duty, mean over arms by wave (151 → 160):**

  | Side | GB | 151 | 152 | 153 | 154 | 155 | 156 | 157 | 158 | 159 | 160 |
  |---|---|---|---|---|---|---|---|---|---|---|---|
  | his | old | 0.025 | 0.028 | 0.034 | 0.004 | 0.028 | 0.025 | 0.026 | 0.026 | 0.017 | 0.011 |
  | his | **new** | 0.033 | 0.028 | 0.034 | 0.004 | 0.028 | **0.063** | **0.054** | 0.028 | **0.058** | **0.043** |
  | her | old | 0.0002 | 0.0007 | 0.0001 | 0.019 | 0.006 | 0.019 | 0.013 | 0.002 | 0.033 | 0.034 |
  | her | new | 0.0002 | 0.0007 | 0.0001 | 0.019 | 0.006 | 0.019 | 0.016 | 0.002 | 0.032 | 0.033 |

  - His rise is on the pet-heavy waves. The old pet spans ended early, which dropped pets' locked ticks from the numerator.
  - Every value stays ≤ 0.063, so near-permanent flinch does not occur.
