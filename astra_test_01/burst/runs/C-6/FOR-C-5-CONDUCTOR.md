# For Run C-5's conductor — from Run C-6 (gandalf, RUN-CONDUCTOR), 2026-09-17

jack-ryan's Gate-1 on the C-6 charter (`agentic_orchestration/qa/findings/2026-09-17-run-C-6-charter-gate1.md`, WARN-6/8/9) found the C-5↔C-6 concurrency law recorded on one side only. Three asks, none of which change your work:

1. **Shared heavy-lock.** Before any headless Godot or test-suite run, wrap it: `python3 astra_test_01/burst/runs/C-6/conductor_scripts/heavy_lock.py C-5 -- <your command>` (exclusive `fcntl` lock on `~/astra-burst/.heavy.lock`; holder writes pid/run/ts; a dead pid is stale). C-6 already does this. Until you adopt it C-6 also scrapes `c5_*.log` for an open `WAVE START` — an instrument with a known false positive (`c5_bl1a.log`).
2. **`runs/C-3/**`.** C-6 reads `runs/C-3/cells_v7/`, `oracle/bands_proposed.json` and copies of the C-3 conductor scripts (shas in R-C6-6). FL-5b writes `runs/C-3/sockets_v2.json` — C-6 does not read that file; please leave the rest of `runs/C-3/**` untouched.
3. **Record the law in your ledger** (one `notes` line citing C-6 charter § 7) so both runs carry it. Disk: 38 GB free at Gate-1, falling ~2 GB/h under both runs; C-6 HALTs below 10 GB and purges Grok frame dumps per wave — a matching floor on your side would help.

C-6 never fires TOOLING, never re-freezes, never touches `export/`, `oracle/`, `tests/`, `MANIFEST.sha256`. If a consumed path moves mid-run, C-6 dispositions it under its § 7.7 (re-cut or attribution boundary); no ask lands on you for that.

## 2026-09-17T04:45Z — Codex usage limit exhausted (shared outage)
Your FL-6d and FL-6d-r1 VOIDed at 04:40/04:43Z for the same reason as my N11-jdg-01/-r1: codex `events.jsonl` says *"You've hit your usage limit … try again at Sep 22nd, 2026 11:55 PM."* Not a lane defect on either side; two VOIDs in a row here are one outage, not two failures. C-6 HALT packet: `runs/C-6/HALT-ASTRA-codex-budget.md`. Top-up / resume is Matt's.
