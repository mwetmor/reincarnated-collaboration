# Run C-9 Phase 2 · BV2-FID: barrow_v2 at barrow v1's fidelity, then the w151–160 arena inside it — charter v0.1

**STATUS:** v0.2 — **Gate-1 = GO-WITH-FOLDS** (jack-ryan, `qa/findings/2026-10-06-bv2f-charter-gate1.md`, `a4fde16b6`); every finding folded at § 12 (R-C9-163). M0 ruled (R-C9-162). Phase 0 running. **A Gate BLOCK halts the steps the reviewer scopes it to** (a BLOCK-narrow halts only its named step).
**Authored:** 2026-10-06, gandalf (RUN-CONDUCTOR), fresh session per R-C9-160.
**Course of record:** `2026-10-06-barrow-v2-fidelity-run-architecture.md` ("the plan"). This charter makes the plan executable: it adds lanes, caps, HALTs, decidable target-states, the ARCHITECT gate and three conductor corrections (§ 9). **Where the charter and the plan disagree, the charter governs; the ledger governs both.**
**Parent run:** Run C-9 (`2026-09-26-illuminated-archive-run-C-9-charter.md`). Ruling IDs continue the C-9 series from **R-C9-161**. Ledger: `astra_test_01/burst/runs/C-9/ledger.json`.
**Workstream prefix:** `BV2F` (bursts, milestones, halts: `M-C9-BV2F-*`, `H-C9-BV2F-*`).

---

## § 0 — Intent

**Matt, R-C9-156:** *"play the arena shortly after in the barrow_v2 as we imagined in the painting but in true 3D like the barrow v1."* **R-C9-160:** the R-C9-159 SW section *"still isn't up to the same standards as barrow_v1."*

**Terminal artifact:** barrow_v2 (sketch A + sketch B's stream, layout_v2 v6) as a **level of `runs/C-9/barrow_full/godot/`**, painted, taken and lit by **v1's own pipeline**, passing the v1-parity harness and **Matt's walk (M3)**; then w151–160 played inside it over the sealed KC2 runtime (**M4**).

**The one invariant (plan § 0):** under v1's fixed-direction ortho camera, **one painting at the game camera is the complete in-game view of every static surface.** Every rule below protects it.

## § 1 — Bounded substrate (frozen at launch; sha256 recorded in Phase 0.3)

| Item | Path | Role |
|---|---|---|
| Look of record | `barrow_v2/sites/BV3r2-A.png`, `BV3r2-A_spawns.png` (+ BV3r2-B's stream) | composition and identity only, never scale |
| Quality bar | `barrow_full/` (painting `paint/barrow_full_painted.png` sha `eecb42661af4…`; take; godot level) | positive control |
| Layout + rules | `barrow_v2/layout_v2.json` (v6; `version` field 3) + `tools/validate_layout_v2.py` R1–R13 | geometry of record |
| Negative controls | R-C9-159 (`barrow_full/godot/data/barrow_v2_sw/`, `barrow_v2/section_v1cam/look/`); R-C9-158 (`barrow_v2/section_sw/`) | harness calibration |
| v1 toolchain | the ten tools in plan § 4 Phase 0.3 | frozen by sha |
| Model kit | `barrow_v2/models/builds/`, `barrow_full/web_painted/models/barrow/` | reuse; C7 rebuilds only |
| KC2 runtime (Phase 4) | `reincarnated-godot/kc2_runtime` at the REFERENT-v1 sealed r2 tag (`534febc`, runtime `5b5a539e`) | vendored by SHA, no edits |

## § 2 — Principles (binding; plan § 3, restated as rules)

1. **One painting is the world.** Every static texel comes from one stitched painting at ≥ 100.6 px/m. Primitives and terrain by projection; real models by game-camera bakes from that painting (v1 `t5_06b_bake.py`). No other painted texture enters the level, except entries in the deviation register.
2. **Unlit statics, lit movers** (v1's two-sun law).
3. **The greybox is the shape of record.** Real models, uniform scale (≤ 10% per-axis), class tints, no plants in the guide.
4. **Replicate literally; deviate only on the record** (§ 7). No new pipeline stage without a Matt gate.
5. **Compose for the play window.** Matt judges play-camera screens plus a map.
6. **Measure parity before Matt looks.** Matt sees only harness-passing work, or a decision request.
7. **One variable at a time, on the pilot only.**
8. **Sequential.** Phase 4 starts after M3 (R-C9-156).

## § 3 — Fit test (desirable-run pattern § 3)

| Criterion | Holds? | Why |
|---|---|---|
| Bounded substrate | YES | § 1; frozen by sha in Phase 0.3 |
| Decidable target-state | YES | § 5: each phase closes on harness rows + Gate-2 + a Matt gate |
| Pre-drainable forks | YES | M0 (a)–(d) drained at launch; the remainder are GATED at M1–M4 (§ 8) |
| Authority-resident | YES, with one hand-off | Phases 0–3 are C-9 / drax / galadriel. Phase 4.1's arena-geometry divergence is a **Sim Session (KC2) ruling**, requested at M3 |

## § 4 — Lanes (seams execute; the conductor writes no production code)

| Lane | Agent | Owns | RESUME file |
|---|---|---|---|
| **LV** | drax | level frame, models, class-tinted guide, screens, greybox app | `runs/C-9/barrow_v2/fid/RESUME_LV.md` |
| **PT** | drax | positive control, frozen toolchain, paint, take, bake, build, life (heather, snow, water) | `runs/C-9/barrow_v2/fid/RESUME_PT.md` |
| **PH** | galadriel | parity harness P1–P11, calibration, per-chunk auto-QA, blind test | `runs/C-9/barrow_v2/fid/RESUME_PH.md` |
| **AR** | drax (joint with the Sim Session's drax) | Phase 4 presenter, intents, enemy bodies | opened at M3 |
| Gate | jack-ryan | Gate-1 on this charter; Gate-2 at every phase close | — |

**Lane law:** every lane keeps its RESUME current at every commit (state, next step, exact re-run commands). A lane that halts writes its HALT into its **RESUME and hand-back**; **only the conductor writes `ledger.json`** (rulings, halts, milestones) and commits it (I-4: no lost-update race).

## § 5 — Phases, target-states, Matt gates

### Phase 0 — re-baseline + parity harness (0 images, $0) · closes on Gate-2 → conductor report to Matt (no Matt gate)

| Step | Lane | DONE when |
|---|---|---|
| 0.1 Positive control | PT | v1 re-rendered at HEAD reproduces: ID self-test pass; unlit-vs-painting mean diff 15.5 (±0.5); heather 52% on tufts (±2 pts); frame time within 10.9–12.4 ms. Any miss = **HALT** (the baseline is not what we think) |
| 0.2 Frame fix (C6, DEV-4) | LV | a function `world = R_y(47°)·sim` in one place, sign proven by a two-anchor test; anchors + features rendered at the play camera and overlaid on sketch A's screen positions; **topology and orientation agree** (judged by the conductor; scale ignored) |
| 0.3 Frozen toolchain | PT | the ten v1 tools copied to `barrow_v2/fid/v1tools/` with `SHA256SUMS`, byte-identical to their v1 sources; a `verify` step every later lane script calls first; only frame and grid are parameters, in a separate config |
| 0.4 Parity harness | PH | P1–P11 implemented; **calibration table**: v1 passes every row; R-C9-159 fails at least P1, P2/P3, P4 (cellularity); every quality row discriminates v1 from 159 (§ 9 C-1) |

### Phase 1 — design freeze + blockout (0–4 images, ≤ $8 fal) · **M1**

- 1.2 Model kit v3 (LV): only what C7 broke (barrow front, longhall at true proportions, the wreck per M0(b)); uniform scale; a 53° top view in every multiview sheet.
- 1.3 Class-tinted guide (LV): v1's recipe and v1's own tint values for shared classes; new distinct tints for rock, wood, shingle, shore ice, sea, stream; no plants; 100.6 px/m over the paint envelope, as 1536×1024 tiles on the final grid.
- 1.4 **M1:** 12–16 play-camera stills at the M0(c) zoom, a labelled top-down map, a walkable greybox app. **No painting before M1 passes.**
- DONE: validator R1–R13 green on the frozen layout; harness P6 (geometry vs layout) green on the guide; Gate-2; M1.

### Phase 2 — the pilot (≈ 56–64 images) · **M2**

- Final grid chosen first (9×11 nominal; DEV-1). W-A "home ground", then W-B "the coast", each a 4×4 sub-block of it.
- v1's brief (`rules` verbatim), v1's reference as IMAGE 2, DEV-3 identity plates on hero chunks only; per-chunk notes **generated from the ID render**.
- Take, bake, build into barrow_full; heather from painted tufts; snow; DEV-5 water.
- **W-A first. If W-A fails parity, HALT: the replication is wrong, not the content. Forensic, then one variable, re-run W-A only. W-B does not start.**
- DONE: P1–P11 green on both windows; Gate-2; **M2** = stills + film of each window beside v1 at the same zoom.

### Phase 3 — the whole site (≈ 130–150 images incl. repairs) · **M3**

- Remaining chunks under v1's wavefront driver; per-chunk auto-QA (invention check first, then P5–P7); seam repair ≤ 1 per seam and ≤ 15% of chunks; P4 drift checked against the pilot statistics, master transfer only if P4 drifts.
- Full take and build; heather ≈ 4–5k sprays; snow field resized (DEV-6); desktop painting texture (DEV-7).
- DONE: harness green site-wide; desktop app + walk film; Gate-2; **M3 = Matt walks the level.**

### Phase 4 — w151–160 inside barrow_v2 (0 images) · **M4** (joint with the Sim Session; starts after M3)

As plan § 4 Phase 4, steps 4.1–4.7. **Desktop only.** DONE: PLAY in barrow_v2 reproduces the ORACLE event stream for w151–160 under the registered divergences (headless, G3 tools); 0 frames > 16.7 ms at the w160 peak; Gate-2; **M4 = Matt plays it.** Frame-time window: the w160 peak, first 5 s warm-up excluded (I-3).

## § 6 — Caps and HALT rules

| Limit | Value | On breach |
|---|---|---|
| Astra images, this run | **≈ 250**, counted on **BV2F-prefixed bursts only** (the shared C-9 `images_used` is not the run counter); sub-caps **Ph1 4, Ph2 70, Ph3 160**, reserve 16. A W-A re-paint after the first pilot pass overruns Ph2 **by design**: the first W-A failure is a sub-cap HALT to the conductor | HALT the lane at its sub-cap; the conductor re-bases or asks Matt |
| Seam repairs | ≤ 1 per seam, ≤ 15% of chunks (Ph3) | HALT to the conductor |
| Positive control drift | step 0.1 re-run at every phase Gate-2; the painting sha `eecb4266…` + `godot/data/painted/` shas before/after every lane run; `git status --porcelain -- barrow_full/` shows only allowlisted new paths | **HALT the run** (the control moved) |
| Astra usage-limit message | — | driver exit 7, lane HALT, RESUME written |
| fal | ≤ $10 run total (Phase 1 ≤ $8); per-lane ledgers | HALT |
| Meshy | not planned; 10-credit guard stands | — |
| Disk (`df -h /System/Volumes/Data`) | gate 20 GiB; lanes halt at 21 | HALT heavy work; **Matt runs deletions** |
| Heavy work | `runs/C-7/conductor_scripts/heavy_lock.py C-9 -- <cmd>` for every Godot/Blender render | — |
| Harness | first failing gate stops the phase | forensic → one variable → pilot only |
| New pipeline stage, or any departure not in § 7 | — | **HALT to Matt** (commitment boundary) |
| Frozen-tool sha mismatch | — | HALT the lane |

## § 7 — Deviation register (each entry: reason + measured A/B before it is relied on)

| DEV | Departure from v1 | Reason | Measurement owed |
|---|---|---|---|
| DEV-1 | Grid ≈ 9×11 canvases instead of 4×4 | site is 5.3× v1's window | P5 seams + P4 drift across rows vs v1's spread |
| DEV-2 | New classes/tints: rock, wood, shingle, shore ice, sea, stream | v1 had no coast or buildings | P4 per-class stats; tint separability in the ID/class map |
| DEV-3 | Sketch A identity plates on hero chunks, true scale, "subject only" label | v1's concept has no wreck, hall or cave | A/B on one hero chunk in W-B: with vs without plate, P6 invention check + conductor read |
| DEV-4 | Site rotated into v1's camera, `R_y(47°)` | sketch A / layout_v2 composed at yaw 0; v1's engine fixed at yaw 47 | 0.2 overlay proof |
| DEV-5 | Animated water over the painted sea; floes bob with rest-pose UVs | R-C9-159(4) | P2 exemption scoped to the water motion layers only; P9 film |
| DEV-6 | Snow field resized to the 85 m floor | v1's field is 47.2 m | P9 trail coverage; P10 |
| DEV-7 | Desktop painting texture 11,776×8,704 (web tiling later) | size | P1 at the play camera; P10 |
| *DEV-8 (only if M0(c) ≠ v1 zoom)* | Play zoom differs from v1's 19×13 m | M0(c) | P1 still ≥ 100.6 px/m painted; screen-pixel sampling recorded |

A departure found in flight that is not here is a HALT, not an entry.

## § 8 — Open-questions gate (ARCHITECT)

| # | Decision | State |
|---|---|---|
| M0(a) | Water | **RESOLVED R-C9-162:** one sea level; wreck beached in shore ice; west lagoon + spit removed (LV, Phase 1; validator green) |
| M0(b) | Wreck | **RESOLVED R-C9-162:** rebuilt to read from 53° above, ~12–14 m, from a top-down sheet (Phase 1.2) |
| M0(c) | Play zoom | **RESOLVED R-C9-162:** v1's 19×13 m; DEV-8 not opened |
| M0(d) | Image guard | **RESOLVED R-C9-162:** `images_cap` 1,500 → 1,750 (ledger updated) |
| G-1 | Grid exact size (9×11 nominal) | GATED: fixed at Phase 2 start from the M0(c) zoom and the paint envelope; conductor ruling |
| G-2 | Whether a low-frequency master colour transfer is used | GATED: only if P4 drifts beyond the pilot spread in Phase 3 |
| G-3 | Phase 4 arena geometry = barrow_v2 floor polygon as a registered divergence | GATED: **Sim Session ruling**, requested at M3 |
| G-4 | The 170 unmapped roster records (kit-map or token) | GATED: KC2's ruling, Phase 4 |
| G-5 | A web build of the arena (wasm contact solver + shadow bit-equality, KP-234) | OUT OF SCOPE: separate Matt decision |
| G-6 | The barrow_full web page update with barrow_v2 | OUT OF SCOPE until M3; loadout pushes deploy Vercel (R-C9-117) and are fresh-ask |

## § 9 — Conductor corrections to the plan (folded here)

- **C-1 · Discriminator rule scope.** The plan says "a metric that cannot tell v1 from 159 is discarded." That is right for the **quality** rows (P1–P6, P11). P7 (clean floor), P8 (heather share), P9 (life), P10 (performance) are **constraints**: they keep a positive control (v1 passes) but are not discarded for failing to separate 159, which shares v1's engine systems. Discarding them would delete the guards for exactly what 158 lacked.
- **C-2 · Negative-control roles.** R-C9-159 is the primary negative control for P1–P6 and P11. R-C9-158 is the negative control for P9 (it had no heather wind, no moving water, no snow trail). It ran v1's method outside v1's engine, so it is **not** required to fail the quality rows; where it passes them, that is evidence the harness measures the method, not the host.
- **C-3 · P11 judge.** The blind judge is a **fresh named galadriel sub-agent** spawned by the conductor with crops only (no paths, no labels), so PH cannot judge its own harness.
- **C-4 · Phase 0 runs ahead of Gate-1** because it spends nothing and writes only to `barrow_v2/fid/` and the lanes' RESUMEs; nothing in Phase 0 is relied on until Gate-2.

## § 10 — Standing laws carried in

- `git commit --only <paths>`; `git status --porcelain -- <paths>` before; `git show --stat HEAD` after; `git -C` for every cross-repo op; never `git add -A`.
- Push (W-6): **collab: push-as-work-lands under R-C9-71/84; engine: none (no BV2F paths); reincarnated-godot: none by this conductor — the Sim Session conductor releases (R-C9-84); loadout and demo: fresh-ask.** The missing CLAUDE.md record of R-C9-71/84 is routed to knight-rider.
- Keys via `source ~/.zshrc`, never printed. refs_guard: no franchise, studio or artist names in prompts or filenames.
- Matt runs deletions. Never work around a permission denial.
- No sleep, time-of-day or session-length language in any report to Matt.

## § 11 — Matt interface

Matt is on Remote Control (phone). The conductor sends: one short line per phase transition or HALT; decision requests only via AskUserQuestion, one recommendation per question; look packets at M1–M4 as a few sheets plus one film, not directories.

## § 12 — Gate-1 folds (jack-ryan `a4fde16b6`; conductor ruling R-C9-163). These GOVERN over conflicting text above.

**B-1 → two-tier freeze (step 0.3).**
- **Tier A, byte-identical** (frame-free): `guided_paint.py`, `guided_stitch.py`, `heather_instances.py`, `hero_surface.py`, `t5_06b_bake.py`, `nb_t8/scripts/t5_06a_surface.py`, `wave.sh`, `refs_guard.py`, `make_layout.py`, and `cfg_t10bf.json` (its `rules`, `refs`, caps).
- **Tier B, minimal patches** (frame-bearing): `capture_blockout.gd`, `capture_ids.gd`, `paint_world_prep.py`, `take_from_paint.py`, `t10bf_drive.sh`. Each patch is a committed diff against the v1 source touching **only allowlisted constants and paths** (frame, grid, scene, I/O roots, burst prefix, exit code). Registered as **DEV-9**. Path-relative tools (`HERE`/`ROOT`) get their roots by an allowlisted Tier-B-style env/arg patch or are invoked from a pinned cwd — whichever leaves Tier A byte-identical.
- **`SHA256SUMS` holds two shas per file:** the v1 source read **from git at a pinned commit** (never computed from the copies) and the shipped file. **`verify` checks the files actually executed:** drivers invoke only `fid/v1tools/` paths, and `verify` fails if any v1-original path appears in a command line.

**W-1 → per-row negative controls.** Each row's negative control is the attempt that showed its defect: P1–P4, P11 → R-C9-159; **P5 → R-C9-158** (seams); **P6 invention check → R-C9-155 BVP re-test-2 blocks** (invented doors); a seeded failure where no real one exists. **Constraint rows P7–P10 each show RED once.** Rule: **"re-instrumented or discarded; never threshold-tuned."** The quality/constraint split freezes at the Phase 0 Gate-2; reclassifying a failing row later is a HALT. § 9 C-1/C-2 are amended accordingly.

**W-2 → recorded targets.** Each 0.1 target is written as {record file, field, tool + args, configuration}, tolerances from the record's own spread. The plan's "52%" and "10.9–12.4 ms" are **withdrawn** as targets (ledger prose; recorded heather share 0.44–0.47, `take/build/overlay_check.json`, `painted_prep.json`). **P8's threshold is re-derived from the reproduced v1 value**, not 50%.

**W-3 → DEV entries** (measurement owed before each is relied on):

| DEV | Departure | Measurement / authority |
|---|---|---|
| DEV-9 | Tier-B patches to frame-bearing tools (B-1) | diff confined to allowlist; v1 re-run through patched tools reproduces 0.1 |
| DEV-10 | Per-chunk notes generated from the ID render (W-3a) — needs a per-chunk text field in the painter (Tier-B patch to `guided_paint.py`) | W-A A/B: P6 invention count with vs without notes on the same chunks |
| DEV-11 | Per-chunk DEV-3 plate attachment mechanism (W-3b) — Tier-B patch to `guided_paint.py` | W-B hero-chunk A/B (as DEV-3) |
| DEV-12 | v1 `rules` with v1-site nouns substituted (W-3c): a published substitution table, all other words verbatim | diff of rules text = substitution table only |
| DEV-13 | Seam-repair canvases (W-3d) — new stage | **Matt pre-authorization at M2** |
| DEV-14 | Low-frequency master colour transfer (W-3e, G-2) — new stage | **Matt pre-authorization at M2**, and only if P4 drifts |
| DEV-15 | Driver exit 7 on usage limit (W-3f) — part of the Tier-B `t10bf_drive.sh` patch | dry-run with a simulated limit message |

**W-4 → the pilot is a proof, not a keeper.** Option (iv), conductor ruling: pilot chunks are **not** kept; Phase 3 paints the full 9 × 11 grid in v1's wavefront order from the origin, so every chunk gets v1's left/top/top-right paste and no structural pilot-edge seams arise. If a pilot window happens to sit at the wavefront origin (option i), its chunks may be kept. Cost: ≈ +32 images, inside the 250 run cap (Ph3: 99 chunks + ≤ 15 repairs ≤ 160). This keeps the painter v1-pure (option ii would patch the paste rule) and leaves the repair budget for real seams (option iii would spend it on known ones).

**W-5 → write scope.** Step 0.1 writes only to `fid/pc/`; v1 scripts are read-only; barrow_v2 levels **extend** them; Phase 0 puts nothing into `barrow_full/godot`. Control-drift HALT added to § 6.

**W-6 → § 10 push line rewritten** (above).

**W-7 → instruments.** P2 = **lineage chain** (each texture's input sha through the producing tool's manifest back to the painting sha). P3 = **per class**, labelled "rendered-vs-painting residual" (v1's unlit 15.5 is the reference). Phase-1 P6 is judged against the **layout_v2 polygons**, not the guide's own class map. P4 for new classes (sea, shingle, shore ice): a named nearest v1 class, or the class-agnostic cellularity detector only.

**INFO.** I-1: P11 n = 40 pairs, with v1-vs-v1 null pairs, metadata and filenames stripped, identical crop sizes; the power table is printed on the row. I-2: step 0.2 is decided by the cyclic order of the six anchor bearings matching sketch A, each within ±15°; P9 by water-mask flow > 0, floe UV drift 0 px on a marker, snow-trail coverage % of floor. I-3: folded in § 6. I-4: folded in § 4. I-5: noted.

---
**Signed:** gandalf, RUN-CONDUCTOR. **Anchors:** plan (this date), handoff session-2 §§ 2, 6, ledger R-C9-144..160, `barrow_full/take/build_plan.md` § 1.
