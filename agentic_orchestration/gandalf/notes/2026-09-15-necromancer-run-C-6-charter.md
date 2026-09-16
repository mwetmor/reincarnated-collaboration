# Run C-6 charter — the Necromancer: master → turnaround → motion → cells → playable (DRAFT v0.1, awaiting Matt's fork rulings + jack-ryan Gate-1)

> **STATUS:** DRAFT — gandalf (ELICITOR → ARCHITECT), 2026-09-15. Conductor: gandalf (`RUN-CONDUCTOR`, intent residency). Pattern: `operating-procedures/desirable-run-pattern.md` §§ 1–6. Lineage: Run C-3 (the Keeper matrix run, `2026-09-13-astra-burst-lane-run-C-3-charter.md`) — this run is **the same lane, the same tools, a second character**; every deviation from C-3 is named in § 3.
> **Founding rulings (ledger `runs/C-6/ledger.json`):** R-C6-0 (character 2 = end-game Necromancer; text-designed; grip classes as direction; STOP after the master), R-C6-1 (Matt: N1-master-cam-02 IS the design master), R-C6-2 (Matt: the scythe is *baked in*), R-C6-3 (Matt: the unarmed set is a possible future lap, not this one).

## 0. Intent (one sentence)
Produce the end-game Necromancer as a **complete playable 8 × 5 cell matrix in the painted cliffside scene** — the Keeper's pipeline re-run on a second identity holding a two-handed scythe — so that Matt can walk him through the clearing and cast at the dummies on the web build, and so that the character lane is proven **repeatable**, not a one-off.

## 1. Bounded substrate (frozen at launch)
| item | path | state |
|---|---|---|
| Design master (accepted) | `runs/C-6/artifacts/N1-master-cam-02/necro_master_cam_02.png` (1254², green, figure 706 px) | R-C6-1 |
| Scythe design (Matt, first-party) | `runs/C-6/artifacts/N1-refs/scythe_design_v1.png` | filed |
| **Animation master** = master + scythe | `runs/C-6/artifacts/N2-master-scythe-01/necro_master_scythe_01.png` | **N2 in flight; Matt's eye gates it (§ 5)** |
| Scene camera + register facts | `canonical/reap-die-rise-game/painted-2d-pipeline/00-system.md` (53° pitch, 130-px figure at the camera, `default_texture_filter` linear, gl_compatibility) | CANON |
| Lane tools (frozen) | `astra_test_01/burst/MANIFEST.sha256` **49a9dbf151bb** (T3a–T3f cut/matte/bands/encode/godot + T4a–T4f VFX) | frozen 2026-09-15 |
| Keeper exemplars + PROPOSED bands | `runs/C-3/cells/*`, `oracle/bands_from_exemplar.py` outputs | C-3, report-only |
| Playable scene | `runs/C-5/cliffside_v21` (v19 clearing, seven dummies, kits_v9, T4b/T4f) | C-5 R-C5-14 |

## 2. Decidable target-state (the run checks these itself)
1. `runs/C-6/cells/<dir>_<anim>/` exists for all **40 cells** (8 directions × idle/walk/run/jump/cast), each with `numbers.json`, `registration.json`, a 1:1 MP4 and the Lanczos 2× review MP4 — the same artefact shape as `runs/C-3/cells/`.
2. Every cell's CHECK report exists with every band row **`passed: null` where the band is PROPOSED** (report, never verdict — C-3 § 7 unchanged).
3. A PACK export of the cliffside scene with `--cells runs/C-6/cells` imports headless with **0 errors** and drax's deploy-truth shows the second route serving 200.
4. `matrix.html` lists all 40 cells with numbers and packet links.
Fallbacks (ledgered, veto-open, C-3 § 8 verbatim): a direction failing geometry twice → best candidate *flagged*; a clip with a head-down opening → one re-generate, then *flagged*; a cell whose period cannot be found → the prompted period *flagged*.

## 3. What differs from C-3 (named deviations)
| | C-3 (Keeper) | C-6 (Necromancer) | why |
|---|---|---|---|
| Master origin | Astra-minted in-lane (K1p) | Matt's app design → in-lane camera re-mint (N1) → scythe bake (N2) | R-C6-0/2 |
| Weapon | staff, near/far hand per direction | **two-handed scythe**: haft crosses the torso; blade is the tallest landmark; per direction the blade side follows the *anatomical right* (no mirroring, C-3 F3) | R-C6-2 |
| Turnaround geometry reference | earlier K2 drafts as geometry-only IMAGE 2 | **none exist** → P2 runs the C-1 two-pass shape: a geometry-only draft per direction (K2-class) *then* the identity mint (K2c-class) from the master | no prior turned drafts |
| Gear tier / VFX | starter↔advanced swap; frost bolt | **none** (no gear swap; VFX come from C-5's kits at the cast socket) | R-C6-3 scope |
| Cast socket | staff tip | **scythe blade socket** (the blade's inner curve) — `sockets_v2.json` gains a `necro` entry (conductor-authored data, not code) | weapon |
| Scene proof | Godot stub + Pixi wheel | the **real cliffside scene** (`cliffside_v21`) with the necro as the player; drax route `/playtest/cliffside-necro/` | C-5 exists now |

## 4. Sequence
| phase | what | bursts | images |
|---|---|---|---|
| **P0 launch** | Matt rules § 5 forks; jack-ryan Gate-1 on this charter; GO → R-C6-4; `images_cap` = 80 | — | 0 |
| **P1 animation master** | N2 (in flight) → Matt's eye → if FAIL, one N2-r1 with the named reason → **STOP at Matt's word** (R-C6-0 discipline carried) | 1 (+1) | ≤ 4 |
| **P2 turnaround** | 7 geometry drafts (SW W NW N NE E SE) → 7 identity mints from the master with the draft as geometry-only IMAGE 2 → JUDGE with a mirrored control, geometry axis (blade side = anatomical right; horn = anatomical left shoulder) → retry once per direction | 14 gen (+≤ 7), 2 jdg, 1 pack | ≤ 42 |
| **P3 clips** | Grok i2v, one per cell (40), C-3 § 6 prompt skeleton + the necro identity line + *"the scythe stays in both hands, blade up"*; conductor-driven, sequential; HALT on 3 consecutive failures | 40 Grok | 0 |
| **P4 cells** | per clip CUT → CHECK → TRANSCRIBE → PACK with the frozen T3 tools, waves of 4; one-shot landmarks for cast = the **blade tip** (T3a's "staff-tip" landmark re-pointed by parameter, no code) | 40 × 4 | 0 |
| **P5 scene** | `sockets_v2.json` + necro entry → PACK `cliffside_v22-necro` (`--cells runs/C-6/cells`) → headless import proof → drax web9 (second route) → Desktop packet | 1 PACK | 0 |
| **P6 close** | ledger, `matrix.html`, handoff, push; **C-7 = Matt's verdict session** | — | — |

## 5. Forks for Matt (ELICITOR — one recommendation each; rule with a word)
| # | fork | **recommendation** | alternatives / tradeoff |
|---|---|---|---|
| F1 | cell set | **all 5 animations (idle/walk/run/jump/cast) — parity with the exporter's state machine and the Keeper** | 4 (drop jump): −8 clips, but the scene's Space key would play nothing for him |
| F2 | motion source | **Grok i2v for all 40 clips (weekly balance is back; the character is now at the right camera and register, which un-shelves Q78 b's reason)** | the no-video path (Astra keyframes + T3 interpolation) — unproven for characters; would be a second experiment inside a production run |
| F3 | gates | **reuse the Keeper's PROPOSED bands, report-only; no new bands minted in-run** | derive necro-specific bands from his own first passed cells — a bar change mid-run, which C-3 § 8 halts on |
| F4 | scene delivery | **second route `/playtest/cliffside-necro/` (necro is the player); Keeper route untouched** | a character-select toggle in the scene — a TOOLING row (exporter + input map) before anything is playable |
| F5 | the animation-master gate | **Matt's eye on N2 (or N2-r1) is the only gate; no in-lane geometry judge on a still** | a JUDGE burst on the composite — spends images on what one look settles |

## 6. Matt interface
Eyes at: the N2 composite (P1 gate), the P2 turnaround contact sheet (report, not gate — fallback proceeds flagged), and the web9 route. Red-flag pings only otherwise; packets on the Desktop under `Astra Burst Review - <date>/`; push as you go (standing pattern). HALTs write a HALT packet and stop.

## 7. Safeties carried
Preregistered target-state (§ 2); jack-ryan Gate-1 before GO and Gate-2 on the close; veto-open ledger; conductor writes no code (sockets JSON + briefs + ledger only); provenance roots per lane rules (references staged under `runs/C-6/artifacts/N1-refs`).
