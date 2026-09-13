# Run C-3 — conductor state (read FIRST after a compaction; the ledger is the truth, this is the map)

- Charter: `agentic_orchestration/gandalf/notes/2026-09-13-astra-burst-lane-run-C-3-charter.md` (6e7bfa8c7450). GO = C-1 R-57. Ledger: `runs/C-3/ledger.json` (cap 120).
- Conductor scripts (session scratchpad; copy into `runs/C-3/conductor_scripts/` at close): `cl.py` (ledger writer: rulings/milestones/halts/grok_calls/notes; `show`), `wave.sh <log> <id:TYPE>…` (briefs from `briefs/C-3/`, `--run C-3`), `grok_clip.sh <cell> <still> [suffix] [extra prompt]`, `clips_seq.sh <log> <cell:still>…` (halts at 3 consecutive failures), `mk_p2.py`, `mk_p2_judge.py`, `mk_prompts.py`, `mk_tooling.py`, `freeze.sh`, `restamp.py`.
- Data: `runs/C-3/k2c_facing_table.json` (derived geometry, R-C3-1), `runs/C-3/matrix_prompts.json` (40 cells, R-C3-3). SPEC § 7 = the T3a-1…T3f contracts.

## Rulings so far
- R-C3-1: R-43's E geometry was inverted — derived table governs (E/NE/SE staff NEAR). FLAG for C-4 (veto-open).
- R-C3-2: P2 before P1; clips during T3; nothing measured before its instrument is frozen.
- R-C3-3: prompts frozen; cast = tip glint only (VFX composited in P5).

## Phase status
- P0 done. P2: 7 GENERATE delivered (8 images); JUDGE K2c-jdg-01 (hidden control = image 5, mirror(W) claimed E).
- P3: S clips from master C running (`clipsS.log`). Other 7 directions after P2 judge.
- P1: T3 briefs T3a-1…T3f written; T3a-1 fires after the P2 judge closes (TOOLING never overlaps a burst). Re-freeze pins the SPEC § 7 edit first.
- Suite baseline: 184 run / 178 green; reds = 4 T0-d3 motif + test_synthetic_contract_and_grid + test_k3_combat_report_only (T3c fixes).
