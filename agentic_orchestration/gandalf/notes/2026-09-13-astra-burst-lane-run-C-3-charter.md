# Astra burst lane — Run C-3 charter: the MATRIX run (autonomous, overnight-class) — verdict-ready, not the verdict

> **STATUS:** DRAFT v1.0 — gandalf (ARCHITECT → RUN-CONDUCTOR), 2026-09-13. Authorized by Matt's rulings on forks A–H + scene = **both** (2026-09-13, ledger R-56). **Launches on Matt's GO word, from a FRESH `claude --agent gandalf` session using § 13** (charter-freshness rule; the C-2 session is ~5 h deep). Predecessors: `2026-09-11-astra-burst-lane-run-charter.md` (Run C-1; register card v1.1; burst rules; rubric), `2026-09-12-astra-burst-lane-hitl-run-C-2-plan.md` (EXECUTED), `canonical/reap-die-rise-game/painted-2d-pipeline/00-system.md`.

## 0. TL;DR
- **Question the run makes answerable (Matt's):** can the C-2 process — image model for identity + register, Grok i2v for motion, oracle cut, matte, register, gates — cover **all 8 directions × {idle, walk, run, jump, cast}**, carry **one gear tier** and **one weapon (staff)**, and land in **a simple playable scene**?
- **Shape (desirable-run pattern § 3):** F1 enumerable (the 8×5 matrix + gear + VFX + scene = 47 cells); F2 decidable **as "every cell has its evidence"** — not as the verdict (the gates were falsified at C-2, R-48/R-50: the eye is the authority); F3 forks drained (A–H ruled); F4 authority-resident at reasoning boundaries. **The VERDICT is reserved to Matt at HITL C-4** on the run's packets. A run that "reaches the verdict" autonomously would measure the matrix with the ruler C-2 proved wrong.
- **Exit (decidable):** T3 tests green (standing reds named) · 8 judge-verified H1 rest frames · 40 cells each with clip → cut loop → matte → registered frames → numbers vs PROPOSED bands → packet · gear probe (7 images) · frost-bolt VFX composited on the cast · Godot stub project passes a headless import · Pixi viewer wheel plays every cell · `matrix.html` · ledger complete. Any cell that cannot complete carries its reason and its fallback taken — that is a complete cell.
- **Budget:** run cap **120 Astra images** (149 remain of C-1's 250; C-3 keeps its own ledger `runs/C-3/ledger.json` with `images_cap` 120) · ~45 Grok clips (subscription; the CLI printed no cost line at C-2 — the halt counts clips) · wall-clock ≈ 10 h.

## 1. Authority and interface
| Role | Who | Does |
|---|---|---|
| Ruler | Matt | forks A–H + scene (ruled 2026-09-13); GO word; **the verdict at C-4**; halts; medium/bar changes |
| Conductor | gandalf (RUN-CONDUCTOR, fresh session) | charter, briefs, ledger, Grok headless calls (conductor-driven; 0 Astra images), harvest rulings on substance (R-4/R-35 precedent, always ledgered), packets; **writes no code** |
| Labour | Astra (typed bursts) | TOOLING (serial, T3) · GENERATE · CHECK · JUDGE · TRANSCRIBE · LABEL · PACK |
| Motion | Grok Imagine i2v via `~/.grok/bin/grok -p … --always-approve` (`image_to_video`, 6 s, 720p) | one clip per cell from the direction's judged rest frame |
| Outside | drax (folds the Godot stub into `reincarnated-godot` AFTER C-4), jack-ryan Gate-2 at close-out, legolas (none) | F7 unchanged |

**Conductor rules carried from C-2 (R-52 family):** open every background task's output before acting on its notification — a notification is not a receipt; never chain a launch behind `grep -c`; conductor ledger writes under `runs/<run>/.ledger.lock` (`flock`) with `indent=2`; no conductor writes under `burst/` while a TOOLING burst runs; references must sit under `runs/<run>/artifacts` or `run_0*` (R-37); PACK budgets sized to their media (R-52).

## 2. Register, bible, rulings carried
Register card **v1.1 (H1)** and bible **v0.3** unchanged (frozen at MANIFEST `4537800c3a7b`; T3 re-freezes). Rulings in force: R-23 (H1; ARPG-language default screen; 17 %), R-29 (bands — now PROPOSAL-ONLY per R-48/R-50), R-31/R-32 (advanced set: astrolabe staff head + the "Needle through Strata" provenance mark on pauldron_L; pilot = the female Keeper), R-43 (E-frame construction: staff in the far hand ✓; satchel AT THE SIDE; strap from behind the neck), R-51 (gaze forward from the first frame; per-facing bands), R-53 (matte edge; Lanczos + 1:1 review encodes), R-55 (cadence = the register's; walk 12 f @ 12 fps).

## 3. Forks ruled (Matt, 2026-09-13) — the substrate is fixed
| fork | ruling |
|---|---|
| A animation set | idle 16 f @ 8 · walk 12 f @ 12 · **run 8 f @ 12** · **jump 8 f one-shot** (crouch–launch–apex–land) · **cast 8 f @ 20** with the T4 lifecycle (travel 6 loop · impact 10) |
| B VFX | **one frost bolt on the cast**; edge anchor `astra_test_01/run_03/evidence/vfx_style_match.png`; T4 gates |
| C gear tier | **one swap, starter ↔ advanced on the same woman** (R-31 set), as a **paint-over of a passed loop's cut frames** (motion identical — Q75's primitive) |
| D weapons | **staff only**; sword = next run |
| E directions | **all 8 real** (no mirroring, F3) from an H1 K2′ turnaround of master C, judge-verified with the R-43 geometry |
| F gates | **re-derived from the two passed exemplars as PROPOSED bands; the run reports; the eye verdicts at C-4** — nothing re-commits in-run |
| G scene | **both**: a **Pixi viewer wheel** (plays every cell; no runtime — F7c intact) for judging speed + a **Godot 4.6 stub project** under `runs/C-3/godot/` (SpriteFrames + minimal scene: flat floor, move, idle↔walk↔run, jump, cast+VFX, gear toggle) for the playable verdict; headless import proof in-run |
| H budget | **120 Astra images**; ~45 Grok clips; halts § 8 |

## 4. Sequence (phases; serial TOOLING first; waves of 4 elsewhere)
| phase | what | bursts / calls | images |
|---|---|---|---|
| **P0 launch** | session-start + charter-freshness; SYNC 10/10; create `runs/C-3/ledger.json` (`images_cap` 120); copy the C-2 restart discipline; GO ledgered as R-C3-0 | — | 0 |
| **P1 T3 tooling** (§ 5) | six serial TOOLING bursts, each ≤ 40 min / 60 calls, DRIFT-CRITIC review after each, re-freeze after the last; **HALT** if two consecutive T3 bursts FAIL | T3a…T3f | 0 |
| **P2 turnaround** | 7 GENERATE (SW W NW N NE E SE) from master C with the derived geometry per direction (R-43 corrections: satchel at the side; strap from behind the neck; staff far/near per direction) → JUDGE with a mirrored control, geometry axis → per direction: retry once on geometry ≤ 3; second failure → **fallback: proceed with the best candidate, flagged** (no halt) | 7 gen (+≤ 7 retries), 2 jdg, 1 pack | ≤ 21 |
| **P3 clips** | Grok i2v, one per cell: 8 directions × {idle, walk, run, jump, cast} = 40; prompts from § 6 with the gaze line; conductor-driven, sequential; **HALT on 3 consecutive failures**; each clip → `runs/C-3/xvideo/in/<dir>_<anim>.mp4` (first-party) | 40 calls | 0 |
| **P4 cells** | per clip: CUT (T3's tool: split ≤ 4.4 s, matte, period/one-shot detection, resample, register — one scale + one translation per clip) → CHECK (gates vs PROPOSED bands, report-only; G1/G6c/G11; head-pitch) → TRANSCRIBE (X0-M motion questions, separate instance, control) → PACK (Lanczos 2× + 1:1 MP4s, oracle beside when one exists, numbers) — waves of 4 | 40 × 4 | 0 |
| **P5 gear + VFX** | gear: K1p-sig-01 (glyph template ×2 → JUDGE picks the candidate nearest R-k with a control; Matt ratifies at C-4) → K1p-adv-01 (the advanced woman still ×2) → LABEL/edit paint-over of the passed idle-S's 16 cut frames + walk-E's 12 (advanced set) → identity + preservation gates → packet. VFX: frost-bolt sheets (cast 8 / travel 6 / impact 10, run_03 method) → T4 gates → composited at the staff-tip socket on the cast-S loop → packet | ≤ 7 + 6 imgs; 3 chk; 2 pack | ≤ 13 |
| **P6 scene** | `godot_import.py` (T3) emits SpriteFrames `.tres` + `AnimatedSprite2D` scenes per cell into `runs/C-3/godot/` (a self-contained Godot 4.6 project: flat floor, `CharacterBody2D`, input map, state machine idle/walk/run/jump/cast, gear toggle, VFX layer) → headless import proof (`/Applications/Godot.app/Contents/MacOS/Godot --headless --path runs/C-3/godot --import`, exit 0 + no import errors) → Pixi viewer wheel (`runs/C-3/viewer/index.html`: direction wheel × animation buttons; plays clips; **no gameplay**) → `matrix.html` (the 8×5 grid with every cell's packet link + numbers) | 2 TOOLING-class steps inside T3f + 2 PACK | 0 |
| **P7 close** | ledger, milestones, handoff STATE REFRESH, tracker delta, packets 20+ on the Desktop, push; **C-4 = Matt's verdict session** | — | — |

## 5. T3 tooling rows (serial; each a TOOLING burst against SPEC § 6; "instrument before candidate")
| burst | builds | acceptance |
|---|---|---|
| **T3a cut tool** | `oracle/video_cut.py`: split ≤ 4.4 s at native fps (half-rate option), matte, **period detection with fallbacks** (walk/run: head-bob autocorrelation → stride = 2 bobs; idle: chest-width autocorrelation → else the prompted period; one-shots jump/cast: head-top rise/apex/landing and staff-tip rise/release/return from the landmarks), resample to N phases from a DOWN/rest/onset frame with the rotation reported, register with one uniform scale + one translation, strip + registration.json; **split as two bursts if needed (cap headroom, R-45)** | synthetic tests: a known-period sequence → period ± 1 frame; one-shot detection on a synthetic arc; the C-2 clips reproduce cut B's indices ± 1 |
| **T3b matte edge** | `gates/matte.py` gains `edge_mode='clamp'`: edge pixels' colour clamped to the nearest opaque neighbour (or premultiplied compositing) instead of un-premultiplying (R-53); `matte_quality.direct_luminance_fringe` re-defined against the pre-edit band | the C-2 video idle's fringe → ≤ 5 luma; alpha area lost ≤ 1 % |
| **T3c gates + bands** | `oracle/bands_from_exemplar.py`: PROPOSED idle/walk rows derived from the two passed exemplars (video idle; walk cut B) as target ± tolerance (report-only, `committed:false`, `proposed_from:` sha256); per-facing rows (E/W vertical; N/S lateral from plate-13 front/rear); LOCK lists → coherence checks (per-region 48-px drift vs re-draw); head-pitch proxy for W-7 (face-region centroid vs head-top over the loop); fix `test_k3_combat_report_only`; O7 resultant floor; `idle_bands --out` honoured for `--ours`; gait arm roles accept `near/far` | suite green except the named standing reds; the two exemplars score inside their own proposed bands |
| **T3d review encodes** | `review/encode.py`: Lanczos 2× + 1:1 MP4s, oracle-beside layout, seam pairs; PACK budgets sized (R-52) | C-2 cut B re-encoded identically |
| **T3e T4 VFX gates** | `gates/vfx_lifecycle.py`, `attachment.py`, `element_hue.py` (SPEC § 6 T4) + composite-at-socket | run_03 VFX evidence passes; a synthetic wrong-hue sheet fails |
| **T3f godot + viewer** | `export/godot_import.py` (SpriteFrames `.tres` + scenes + the stub project template) and `review/viewer_wheel.py` (Pixi viewer page generator; no runtime) | headless import exit 0 on a 2-cell fixture; the viewer page lists every cell |
Re-freeze after T3f (MANIFEST + SYNC); DRIFT-CRITIC review of each receipt before the next fires.

## 6. The matrix — cells and prompts
Cells = 8 directions × 5 animations. Rest frame per direction from P2 (S = master C). Prompt skeleton (from the C-2 clips that passed, R-48/R-50/R-55, plus R-51): *plate unchanged and empty; camera locked; figure centred at one size; same face/hair/costume/colours/staff/satchel every frame; hand-drawn 2D, one continuous shot, no cuts; loop closes (loops) / returns to rest (one-shots); **eyes on the horizon from the FIRST frame, head level**.* Per animation: idle = the C-2 idle prompt (a third bigger than life); walk = the C-2 walk prompt; run = "a brisk run in place, longer stride, arms pumping, torso leaning slightly forward, feet clearly leaving the ground"; jump = "from standing: crouch, launch, apex with knees tucked, land into a crouch and stand — one jump, then still"; cast = "raises the staff two-handed, a surge gathers at the astrolabe/tip, releases forward, returns to rest — one cast, then still". Direction words per facing from the K2 derived-geometry text. **Rule:** a clip whose head is down/turned in its first second is re-generated ONCE with the gaze line doubled; a second failure → the cell proceeds with the later stride/segment and is flagged.

## 7. Gates — report, never verdict
Every cell's CHECK reports: the animation-specific instrument (idle: breath/head/regions; walk/run: W-1…W-6 where the landmarks exist, G6c; jump/cast: the one-shot trajectory numbers + return-to-rest closure) **against the PROPOSED bands with `passed` = null on any band that is proposed**; G1 heights; G11 per pair; the head-pitch proxy; plate survival; the splice check. TRANSCRIBE (separate instance) answers the X0-M motion questions with a control. No burst writes PASS. `matrix.html` shows every number; the eye rules at C-4.

## 8. HALTs (to Matt; the run does not decide) + honorable fallbacks
- HALT: two consecutive T3 bursts FAIL · two VOID bursts in a row · a JUDGE passing its control twice · three consecutive Grok failures or a rate-limit streak · run cap 120 reached · any medium change (rigs, meshes, renderers) · any bar change (a band committed in-run) · any write outside `out/`.
- Fallbacks (ledgered, veto-open): a direction failing geometry twice → best candidate flagged; a clip with head-down opening → re-generate once, then later segment flagged; a cell whose period cannot be found → the prompted period (idle 2 s; walk/run from the sibling direction's stride) flagged; a timed-out burst with complete `out/` → conductor harvest on substance (R-4/R-35/R-45), always ledgered; the headless import failing → the project stub still ships with the error text; the gear paint-over failing identity → the geared still + a re-driven clip as the recorded alternative.

## 9. Ledger and records
`runs/C-3/ledger.json` (conductor-owned; `flock`; `indent=2`): bursts (wrapper), `grok_calls[]` (conductor: prompt sha256, clip sha256, duration, printed cost if any), rulings (R-C3-n), milestones per phase, halts. Receipts, JSON, HTML committed; PNG/MP4 local + Desktop (`Astra Burst Review - 2026-09-13/`). Push as you go (R-24 pattern, `reincarnated-collaboration`).

## 10. Rulings ledger (charter-time)
R-56 (Matt 2026-09-13): forks A–H ruled as § 3; scene = both. Conductor reasoning-boundary rulings expected in-run: per-direction geometry text; period fallbacks; harvests; segment choices; the glyph pick by judge (ratified at C-4).

## 11. ARCHITECT PASS — open-questions gate (every decision the run will hit)
| decision | class | disposition |
|---|---|---|
| animation set + specs (A) · VFX (B) · gear (C) · weapon (D) · directions (E) · gates proposal-only (F) · scene both (G) · cap 120 (H) | RESOLVED | Matt 2026-09-13 |
| register H1; bible v0.3; pilot; cadence 12 fps | RESOLVED | R-23 / R-j / R-55 |
| E-frame construction (satchel side; strap behind the neck; staff far hand) | RESOLVED (text) + in-run judge loop | R-43 |
| gaze forward from frame 0 | RESOLVED (prompt) + re-generate-once fallback | R-51 |
| the glyph template pick (K1p-sig-01) | **GATED** — judge picks nearest R-k with a control; **Matt ratifies at C-4** | R-k / § 5 |
| per-facing bands (N/S lateral) | GATED — measured from the S/N clips as proposals | R-51 |
| Q75 bases × gender | GATED — the gear paint-over is its primitive; ruling after C-4 | queue |
| Q77 vocabulary (court / house / provenance mark) | OPEN — story, not this run | queue |
| plate half of the pivot gate (X6) | OUT OF SCOPE this run (flat floor); the register lock stands | 00-system |
| Godot binary | RESOLVED — `/Applications/Godot.app` (4.6, project pin) | this pass |
| Grok spend | GATED — no cost line printed at C-2; halt counts clips (3 failures / rate-limit streak) | T30 |
| **GO word** | **OPEN — Matt** | § 13 |
Gate verdict: **CLEAN** — no OPEN Matt-gated decision the run will hit except the GO word; the glyph pick is gated with a named fallback.

## 12. Matt interface
Packets `~/Desktop/Astra Burst Review - 2026-09-13/`: 20 turnaround (8 judged frames) · 21–60 one per cell (or `matrix.html` as the front door) · 61 gear · 62 VFX · 63 the Godot stub (open in Godot 4.6: `runs/C-3/godot/project.godot`) · 64 the Pixi wheel (`runs/C-3/viewer/index.html`). **C-4** = the verdict session: Matt's eye on the matrix; then the answer to his question, cell by cell.

## 13. Restart prompt (paste into a FRESH `claude --agent gandalf` session; launches on the GO word)
> Session-start per OP § 1 incl. the charter-freshness gate (read `.claude/agents/gandalf.md` + OP § 2 from disk; read `operating-procedures/desirable-run-pattern.md` § 3–4). Then read, in order: (1) `agentic_orchestration/gandalf/notes/2026-09-12-astra-burst-lane-hitl-session-handoff.md` — the LAST STATE REFRESH block at the bottom is the lane's current state; (2) `canonical/reap-die-rise-game/painted-2d-pipeline/00-system.md` and verify § 7 SYNC via `astra_test_01/burst/lane/check_sync.py` (expect 10/10; MANIFEST 4537800c3a7b); (3) `astra_test_01/burst/runs/C-1/ledger.json` rulings R-42…R-56 and milestones M-K3p-idle-VIDEO / M-K3p-walk-PASS; (4) THIS charter `2026-09-13-astra-burst-lane-run-C-3-charter.md` §§ 1–12. You are RUN-CONDUCTOR for Run C-3 (the matrix run, autonomous, verdict-ready — NOT the verdict). Execute § 4 from P0: create `runs/C-3/ledger.json` with images_cap 120; T3 serial (§ 5) with DRIFT-CRITIC review after each burst and a re-freeze after T3f; then P2–P6 in waves of 4; Grok clips conductor-driven (`scratchpad` scripts of the C-2 shape: `~/.grok/bin/grok -p … --always-approve`, image_to_video, 6 s, 720p). Astra does all labour via `lane/run_burst.py` (TOOLING ≤ 40 min/60 calls serial; others ≤ 15/20); gandalf writes no code. Open every background task's output before acting on its notification. Halts per § 8; fallbacks ledgered. Push as you go. Matt is NOT present: HALT conditions write a HALT packet and stop; everything else runs to the § 0 exit. Begin at P0 only after the GO word is in the ledger.

Tracker-delta: game tracker SESSION-DELTA (C-3 chartered; gate CLEAN; awaiting GO) — written at launch, not now.

— gandalf, 2026-09-13 (ARCHITECT)
