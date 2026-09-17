# Run C-6 charter — the Necromancer: scene-camera master → turnaround → Grok motion → cells → playable (v1.1 — FORKS RULED; at jack-ryan Gate-1)

> **STATUS:** v1.1 — gandalf (ELICITOR → ARCHITECT), 2026-09-17; **v1.1 amendment (conductor session, recording Matt's rulings of 2026-09-17, ledger `M-C6-P0-FORKS`):** F1–F6 accepted as recommended; F7 added and ruled — no image cap and no Grok clip cap (the constraint is the weekly Grok token allowance; out-of-budget = external-state HALT); P3 clip order; P4 cast-landmark wording corrected (conductor script, not a T3 parameter). v1.0 was: supersedes the v0.1 draft of 2026-09-15 (`2026-09-15-necromancer-run-C-6-charter.md`). Conductor: **a second gandalf session** (`RUN-CONDUCTOR`, intent residency: the charter's author is the conductor; this session hands it over with the ledger). Pattern: `operating-procedures/desirable-run-pattern.md` §§ 1–6. Lineage: Run C-3 (the Keeper, `2026-09-13-astra-burst-lane-run-C-3-charter.md`) — **same lane, same frozen T3 tools, a second character**; deviations in § 3.
> **Founding rulings (`astra_test_01/burst/runs/C-6/ledger.json`):** R-C6-0 (character 2 = end-game Necromancer; text-designed; STOP after the master) · R-C6-1 (N1-master-cam-02 accepted as design master) · R-C6-2 (Matt: the scythe is *baked in*) · R-C6-3 (Matt: the unarmed set is a possible future lap, not this one) · R-C6-4 (N2 scythe failed Matt's eye: wrong size, bent) · **R-C6-5 (Matt 2026-09-16: "I landed on the final master version" — a first-party app render supersedes N1/N2 as the design master; N3-final-cam-01 re-drew it at the 53° scene camera and stands on the path in the web scene at 14 % figure height — Matt: "The necromancer looks great").**
> **Runs concurrently with Run C-5 (the fire lane, the other gandalf session)** under the concurrency ruling R-13 — § 7 carries the coordination law.

## 0. Intent (one sentence)
Produce the end-game Necromancer as a **complete playable 8 × 5 cell matrix in the painted cliffside scene** — the Keeper's pipeline re-run on a second identity holding a two-handed scythe — so that Matt can walk him through the clearing and cast at the dummies on the Mac (and later the web build), and so that the character lane is proven **repeatable**.

## 1. Bounded substrate (frozen at launch)
| item | path | state |
|---|---|---|
| **Design master (Matt, first-party, FINAL)** | `agentic_orchestration/gandalf/design-inputs/2026-09-16-c6-necromancer-app-master-FINAL.png`; staged `runs/C-6/artifacts/N1-refs/necro_master_final_app.png` (green plate, 1254², frontal-low camera) | R-C6-5 |
| **Animation master at the scene camera** | `runs/C-6/artifacts/N3-final-cam-01/necro_final_cam.png` (53° camera re-mint of the FINAL master: identity, scythe blade up-left, tome, horn) | R-C6-5, M-C6-N3-CAM; Matt: "looks great" (web10) |
| Scythe design (Matt) | `runs/C-6/artifacts/N1-refs/scythe_design_v1.png` | filed |
| Scene camera + register facts | `canonical/reap-die-rise-game/painted-2d-pipeline/00-system.md` (53° pitch, **151-px figure = 14 %** per `runs/C-5/artifacts/CS-parallax-in-v10/walkable.json`, linear filter, gl_compatibility) | CANON (the v0.1 draft's 130 px is superseded) |
| Lane tools (frozen) | `astra_test_01/burst/MANIFEST.sha256` — **the current freeze at launch** (record its sha in R-C6-6); T3a–T3f cut/matte/bands/encode/godot + the T4/FL exporter | frozen by C-5's conductor; C-6 does NOT re-freeze |
| Keeper exemplars + PROPOSED bands | `runs/C-3/cells_v7/*` (40 cells), `oracle/bands_from_exemplar.py` outputs, `runs/C-3/conductor_scripts/` (grok_clip.sh, clips_seq*.sh, cut_signed*.py, fold_clips.py, join_check.py, mk_p4_check.py, assemble_cells.py, matrix_questions.json) | C-3, report-only bands |
| Playable scene | the latest `runs/C-5/cliffside_v<N>` staged by C-5 (v40 at this writing: 18 kits, real targets, capsule collider) | C-5 |
| Image budget | **none** (Matt F7): the V20 sentinel stays in `runs/C-6/ledger.json`; images counted + reported | separate ledgers |
| Grok budget | **no clip cap** (Matt F7): the binding constraint is the weekly Grok token allowance (size unknown; expected < the Keeper's 71 clips for 40 cells). Every call ledgered in `grok_calls[]`; an out-of-budget reply is an **external-state HALT** on P3 — HALT packet, cells to date kept, resume on Matt's word | R-C6-6 |

## 2. Decidable target-state (the run checks these itself)
1. `runs/C-6/cells/<dir>_<anim>/` exists for all **40 cells** (8 directions × idle/walk/run/jump/cast), each with `numbers.json`, `registration.json`, a 1:1 MP4 and the Lanczos 2× review MP4 — the artefact shape of `runs/C-3/cells_v7/`.
2. Every cell's CHECK report exists with every band row **`passed: null` where the band is PROPOSED** (report, never verdict — C-3 § 7 unchanged).
3. `runs/C-6/sockets_v2.json` carries `cast_<dir>` rows with the **scythe-blade release socket** (the blade's inner curve), derived by the FL-1a/FL-5 rule (the far tip along the facing) and audited with a marked sheet per direction.
4. A PACK export of the cliffside scene with `--cells runs/C-6/cells --sockets runs/C-6/sockets_v2.json` imports headless with **0 errors** and casts fire bolt B east with a `contact` on the shield dummy (the C-5 probe `probe_events.gd`, KIT_CYCLES=9).
5. `matrix.html` lists all 40 cells with numbers and packet links; a Desktop packet shows the turnaround sheet and the eight cast release frames.
Fallbacks (ledgered, veto-open, C-3 § 8 verbatim): a direction failing geometry twice → best candidate *flagged*; a clip with a head-down opening → one re-generate, then *flagged*; a cell whose period cannot be found → the prompted period *flagged*.

## 3. What differs from C-3 (named deviations)
| | C-3 (Keeper) | C-6 (Necromancer) | why |
|---|---|---|---|
| Master origin | Astra-minted in-lane (K1p) | **Matt's FINAL app render → N3 scene-camera re-mint (done)** | R-C6-5 |
| Weapon | staff, near/far hand per direction | **two-handed scythe**: haft crosses the torso; the blade is the tallest landmark; per direction the blade side follows the *anatomical right* (no mirroring, C-3 F3); the horn stays on his left shoulder | R-C6-2 |
| Turnaround geometry reference | earlier K2 drafts as geometry-only IMAGE 2 | **none exist** → P2 runs the C-1 two-pass shape: a geometry-only draft per direction (K2-class) *then* the identity mint (K2c-class) from N3 | no prior turned drafts |
| Figure height | 130 px | **151 px (14 %)** — the T3 tools scale cells by the sockets canvas; the exporter applies figure_height_px from walkable.json | Matt 2026-09-16 |
| Gear tier / VFX | starter↔advanced swap; frost bolt | **none** (VFX come from C-5's kits at the cast socket) | R-C6-3 |
| Cast socket | staff tip | **scythe blade socket** (inner curve of the blade) — `runs/C-6/sockets_v2.json`, conductor-authored data, audited like FL-5 Part B | weapon |
| Scene proof | Godot stub + Pixi wheel | the **real cliffside scene** (latest C-5 staged project) with the necro as the player; a `cliffside_v<N>-necro` staging; web route only on Matt's word | C-5 exists |
| Concurrency | sole run | **parallel with C-5** under R-13 (§ 7) | Matt 2026-09-17 |

## 4. Sequence
| phase | what | bursts | images |
|---|---|---|---|
| **P0 launch** | Matt rules § 5 forks; jack-ryan Gate-1 on this charter; GO → R-C6-6 (records the MANIFEST sha at launch, the no-cap posture (F7), the C-5 staged project version, this charter's path + sha12) | — | 0 |
| **P1 master check** | N3-final-cam-01 is the animation master (Matt accepted it on the path); one look at 512 with the Keeper beside it for scale (report only) | 0 (+1 N3-r1 only if Matt names a defect) | ≤ 2 |
| **P2 turnaround** | 7 geometry drafts (SW W NW N NE E SE) → 7 identity mints from N3 with the draft as geometry-only IMAGE 2 → JUDGE with a mirrored control, geometry axis (blade side = anatomical right; horn = left shoulder) → retry once per direction | 14 GEN (+≤ 7), 2 JDG, 1 PACK | ≤ 42 |
| **P3 clips** | Grok i2v, one per cell (40), C-3 § 6 prompt skeleton + the necro identity line + *"the scythe stays in both hands, blade up"*; conductor-driven, sequential; **order idle → walk → run across all 8 directions, then cast, then jump** (a partial week yields a walkable necro — conductor ruling, veto-open); HALT on 3 consecutive failures or a Grok out-of-budget reply | 40 Grok (+ ≤ 1 re-generate per cell) | 0 |
| **P4 cells** | per clip CUT → CHECK → TRANSCRIBE → PACK with the frozen T3 tools, waves of 4; one-shot landmarks for cast = the **blade tip**. NOTE (v1.1): `oracle/staff_tip.py` is a frozen RANSAC *staff-line* instrument with no landmark parameter; the Keeper's cast landmark lived in **conductor scripts** (`runs/C-3/conductor_scripts/cast_keys.py`, `regions.py`). C-6 writes its own conductor script for the blade tip (topmost alpha extent / far-tip rule) — conductor tooling, not a T3 tool change, § 7.1 respected | 40 × 4 | 0 |
| **P5 sockets + scene** | `sockets_v2.json` (blade socket, far-tip rule, marked audit sheet) → PACK `cliffside_v<N>-necro` (`--cells runs/C-6/cells --sockets runs/C-6/sockets_v2.json`) → headless import proof → `probe_events` east cast → Desktop packet; web route only on Matt's word | 1 PACK | 0 |
| **P6 close** | ledger, `matrix.html`, handoff note, push on Matt's word; **C-7 = Matt's verdict session** | — | — |

## 5. Forks for Matt (ELICITOR — one recommendation each) — **RULED 2026-09-17: "Accept all" (F1–F6 = (a)); F7 ruled as below**
| # | fork | **recommendation** | alternatives / tradeoff |
|---|---|---|---|
| F1 | cell set | **(a) all 5 animations (idle/walk/run/jump/cast) — parity with the exporter's state machine and the Keeper** | (b) 4 (drop jump): −8 clips, but Space plays nothing for him |
| F2 | motion source | **(a) Grok i2v for all 40 clips** (the character is at the right camera and register; C-3 proved the path) | (b) the no-video path (Astra keyframes + T3 interpolation) — unproven for characters; a second experiment inside a production run |
| F3 | gates | **(a) reuse the Keeper's PROPOSED bands, report-only; no new bands minted in-run** | (b) derive necro-specific bands from his own first passed cells — a bar change mid-run, which C-3 § 8 halts on |
| F4 | scene delivery | **(a) a separate staged project `cliffside_v<N>-necro` (necro is the player); the Keeper's stays as is; web route only on your word** | (b) a character-select toggle — a TOOLING row (exporter + input map), which C-6 may not fire while C-5 runs |
| F5 | cast socket | **(a) the scythe blade's inner curve as the release socket** (the fire erupts off the blade) | (b) the haft's top end; (c) the free hand |
| F6 | the master gate | **(a) N3-final-cam-01 as delivered is the animation master — no further mint** (you accepted it on the path) | (b) one N3-r1 pass with a named defect first |
| F7 *(added at launch)* | budgets | conductor proposed a Grok clip cap of 80; **Matt ruled: no image cap and no Grok clip cap** — the weekly Grok token allowance is the constraint and Grok's own out-of-budget reply is the stop | recorded in § 1 + § 4 P3 |

## 6. Matt interface
Eyes at: the P2 turnaround contact sheet (report, not gate — fallback proceeds flagged), the P5 packet (eight cast frames with the blade socket marked; the scene east cast), and the staged project on the Mac. Red-flag pings only otherwise; packets under `~/Desktop/Astra Burst Review - <date>/`; commits auto-fire (`--only` on named paths); pushes and web routes on Matt's word only. HALTs write a HALT packet and stop.

## 7. Concurrency law with Run C-5 (binding on C-6's conductor)
1. **No TOOLING burst and no freeze/restamp from C-6.** The frozen tool tree (`export/`, `oracle/`, `tests/`, `MANIFEST.sha256`, `00-system.md` § 7) is C-5's; C-6 consumes the current freeze and writes only data (briefs, its ledger, `runs/C-6/**`, `sockets_v2.json`). If C-6 genuinely needs a tool change, it files the ask in the account note and HALTs that phase until C-5's conductor schedules it.
2. **Memory (8 GB Mac):** no headless Godot and no test suite from C-6 while a C-5 TOOLING is in flight — check `/private/tmp/claude-501/-Users-admin-Games-reincarnated-collaboration/*/scratchpad/c5_*.log` for a `WAVE START` without `WAVE DONE`. GENERATE/JUDGE/Grok/CUT/CHECK are fine at any time.
3. **Launch bursts detached** (`runs/C-5/conductor_scripts/wave_detached.sh` + `wait_wave.sh` — copy both into `runs/C-6/conductor_scripts/` and point `--run C-6`); never chain a burst behind a long foreground command (LD-2).
4. **Git:** shared working tree; `git commit --only <named paths>` only; never `add -A`; pre-commit check `git status --porcelain -- <paths>`; pushes are Matt's.
5. **Disk:** ~45 GB free at handover; purge Grok frame dumps after cutting; `df -h /` before any download.
6. **Ledgers are separate** (`runs/C-6/ledger.json`, `cl.py` from C-3's scripts with `--run C-6`); image caps reserve against C-6's own cap only.

## 8. Safeties carried
Preregistered target-state (§ 2); jack-ryan Gate-1 before GO and Gate-2 on the close; veto-open ledger; conductor writes no code (sockets JSON + briefs + ledger only); provenance roots per lane rules (references staged under `runs/C-6/artifacts/N1-refs`); the charter-freshness rule (re-read this file + OP § 2 + the desirable-run pattern after any compaction).
