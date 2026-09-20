# Run C-8 charter — the EoR Warlord (pixel-overworld regime): stills → clips → cells → playable (v1.0, forks RULED live 2026-09-20)

> **STATUS:** v1.0 — gandalf (RUN-CONDUCTOR; the same session that conducted C-6, intent resident), 2026-09-20. **Forks ruled live by Matt** (R-C8-0: W1–W6) — this note records the charter the rulings define; jack-ryan Gate-2 at the close. Lineage: C-6 (method, scripts, the E1 probe that produced the seeds), C-3 (cell shape, frozen tools). Ledger: `astra_test_01/burst/runs/C-8/ledger.json`.
> **Born from:** Matt's camera observation 2026-09-20 (consistency over angle; Grok's native uprighting) and the E1 probe (R-C6-39 / M-C6-E1-RESULT): an overworld-proportioned pixel figure HOLDS its elevated view under Grok; realistically-proportioned 53° figures do not, in paint or pixel.

## 0. Intent
The EoR Warlord as a playable 8-direction character in the cliffside scene — resting idle, walk, run, jump, cast, and the Eye-of-Reckoning SPIN attack — proving the pixel-overworld regime as a full character, beside the Keeper and the Necromancer.

## 1. Bounded substrate
| item | path |
|---|---|
| Seeds (5 unique, one knight) | `runs/C-8/artifacts/e1_pixel_warlord_{S_r1,SW,E,NE,N}.png` — Grok stills from one reference (S r1; the others image-edited from it); padded `runs/C-8/artifacts/pad/pad_<D>.png` (1024×1536, 70 %, pure-green) |
| Mirrors (F17a) | W←E, SE←SW, NW←NE at the cell level |
| Prompts | `runs/C-8/matrix_prompts.json` (`mk_prompts_c8.py`; attack spin rate from the wwcr whirlwind VFX, `reincarnated-godot/scripts/wwcr_whirlwind.gd`) |
| Tools | the frozen T3 set + exporter as pinned per wave (C-6 § 7.7 discipline); Astra dark until T25 — conductor-run cuts, packets, exports as in C-6 P4/P5 |
| VFX | the EoR whirlwind VFX from the Godot 3D work (W2) — binding to the spin attack is a C-5/exporter question once the `attack` state exists |
| Scene | `runs/C-6/artifacts/CS-props-trio` (Keeper + Necromancer standing stills) on `CS-parallax-in-v10` |

## 2. Target state (decidable)
1. `runs/C-8/cells/<anim>_<dir>/` for 8 dirs × {idle, walk, run, jump, cast, attack} — 48 cells (30 unique + 18 mirrored), C-3 artefact shape; complete-cell rule as C-6 predicate 1.
2. CHECK reports, report-only (no proposed bands exist for this figure — numbers only, stated per row).
3. `runs/C-8/sockets_v2.json`: cast release socket = the mace head at the slam (script proposes, sheet decides).
4. Export of the five exporter states (idle/walk/run/jump/cast) imports with 0 errors; 8-direction movement + jump probe; east cast contact. **`attack` cells staged** for the exporter extension (TOOLING; Astra-gated) — not an exit predicate of this run.
5. `matrix.html`, `repeatability.json` (vs C-6).

## 3. Rulings (Matt, R-C8-0)
W1 idle = resting idle only · W2 attack = EoR spin, looping, VFX-matched spin rate · W3 cast = shield slam, socket at the mace head · W4 resting idle at ease (mace grounded, breath) · W5 run included · W6 order walk, run, (idle), attack, cast, jump.

## 4. Sequence
Wave 1 walk ×4 + run ×5 (S walk in hand) → wave 2 idle ×5 → wave 3 attack ×5 → wave 4 cast ×5 → wave 5 jump ×5 → cuts/CHECK per wave (conductor, frozen tools) → mirrors → sockets → export → proof → packet. ~29 Grok clips + retries; Grok's weekly cap is the HALT (F7 posture).

## 5. Carried disciplines
C-6 § 7 concurrency law (heavy lock; no TOOLING; `runs/C-3/**` read-only; sha per wave; disk floor); head-level mandate (R-C6-11); size-lock + no-new-objects idle clauses (R-C6-33/36); camera-never-changes clause (E1); veto-open ledger; **register: a LAP DECISION in the pixel-overworld regime — recognition record owed; `style-register.md` stays locked pending canon.**
