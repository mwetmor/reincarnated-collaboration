# JOIN-1 · J4b: engine checks on the graded arms (v5.1, runtime fb49080f) and the PREREG-ADDENDUM-C input (gamora, 2026-10-15)

- **Inputs:** godot `2ca2298`. All 105 pins in `grains_sha256.json` (sha256 `e8345d6c…`) were verified, plus 70 / 70 G-grain digests against each `manifest-port.json`.
- **Engine:** row replay `7f611592` (GHR join); grader `faf07f5f` → `32bcb035`. All J4b suites pass 189 / 189 at `32bcb035`, run in the dedicated worktree.
- **Files:**
  - `row_replay_50_cells.json`: her 25 cells, every class, all PASS; his 25 cells, GH / GR against GHR and the tapes, all PASS.
  - `grader_arms51.json`: the effect gates and completeness for both arms, and his flinch duty per wave (mean 0.004–0.034). Note: its dot-conservation entries predate the `running_at_end` fix.
  - `dot_conservation_32bcb035.json`: dot conservation at `32bcb035`, 25 / 25 PASS. The rule as first stated HALTs M-POL-2 s1, where the residual equals `running_at_end`.
  - `prereg_c.json`: the PREREG-ADDENDUM-C input (waves {159, 160}).
- **⚑ gethit completeness, as pre-stated: HALT on his arm.** 14 of 60 orphans are not on the final run tick. The cause and the proposed restatement are in PREREG-ADDENDUM-C § 3.
