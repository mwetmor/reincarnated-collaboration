# Astra burst lane — HITL RUN PLAN (Run C-1, the human-in-the-loop session) → overnight autonomous continuation

> **STATUS:** DRAFT v0.9 (2026-09-11) — pending X1 smoke for the "state at HITL start" section (§ 2). Author + conductor: gandalf (RUN-CONDUCTOR). **Purpose (Matt 2026-09-11):** *"end this session and begin the next session fresh at the HITL run start … make one goal of the HITL run to pass all of the Matt-needed/HITL questions/gates so that we can follow that up with an overnight autonomous run."*
> **Reads for the fresh session (in order):** `.claude/agents/gandalf.md` → `agentic_orchestration/operating-procedures/gandalf.md` § 1 (charter-freshness gate) → `canonical/00-ground-state.md` → `canonical/reap-die-rise-game/painted-2d-pipeline/00-system.md` (+ its § 7 SYNC check) → **this plan** → `agentic_orchestration/gandalf/notes/2026-09-11-astra-burst-lane-run-charter.md` → `astra_test_01/burst/runs/C-1/ledger.json`. Do NOT re-walk the TEST-02 corpus.

---

## 0. The one goal

**Leave the HITL session with the ARCHITECT gate fully RESOLVED** — every Matt-gated fork ruled (Q72 a–g, K1 identity picked, G6b decided, the bible v0 committed, the probe set frozen), the first three milestones seen (identity · turnaround · first loop), and the GO word given — so the overnight run has **no question it can hit that only Matt can answer**. Anything the overnight run cannot decide, it HALTs on; the HITL session's job is to make that set empty.

## 1. Pre-conditions (all must be TRUE before the HITL session starts; the fresh session verifies them in ≤ 10 min)

| # | Condition | How verified |
|---|---|---|
| P1 | T0-a, T0-b, T0-c DELIVERED, reviewed, **frozen** (`MANIFEST.sha256` matches the tree). T0-c carries **two named-red acceptance cases** (O3 template mode is blind to primitive-family bleed: F04 inside=1/outside=0; comparator therefore does not reject F04) — **T0-d is HITL step 0** and must turn them green: audit fixes (forbidden-tool regex on tool names only; TOOLING add_dir deliverables accepted), **O3b radial-symmetry/ring-family detector**, O9 declared-absent-PART controls, resolved model recorded per burst in the ledger, then the R9 extensions (SPEC § 6 T0-d row) | `shasum -c` over the manifest; T0-d receipt + green suite |
| P2 | **X1 ran 2026-09-11 (art ✓; lane VOID on audit defects F-1…F-5, ledger R-2).** P2 now reads: **T0-d makes the lane pass X1's calibration** — image_calls (via `generated_images/` diff) == receipt `calls_used` == 2 on a re-run of the X1 GENERATE task; no false violations on a CHECK burst; `plate_uniformity` reported; burst context minimal (verified: no repo AGENTS.md text in X1's stream) | `runs/C-1/ledger.json` X1-gen-02 exit 0 |
| P3 | `00-system.md § 7` SYNC hashes match (manual `shasum` until `check_sync.py` lands in T0-d) | conductor act |
| P4 | Legolas R6–R8 + R9 findings read by the conductor (they are inputs to the vocabulary grill) | this plan § 4 carries the option sets |
| P5 | Matt's review path works: `~/Desktop/Astra Burst Review - <date>/` with a Chrome-playable MP4 (Matt: *"they work in chrome"*) | first packet at K1 |
| P6 | Codex auth live (`codex login status`), one open Codex lane, no other Codex session in the repo | conductor act |

**If P2 is not met at session start, X1 is the first act of the HITL session (≈10 min), before any ruling.**

## 2. State at HITL start — filled after X1

**As of session close 2026-09-11:** T0-a ✓ frozen · T0-b ✓ frozen (46 tests) · T0-c ✓ frozen on substance (69 tests; **2 named-red**: O3 template mode blind to primitive-family bleed; comparator does not reject F04) · **X1 ✓ on art, VOID on lane** — the smoke found five audit/gate defects (ledger ruling R-2: image detector reads 0 vs true 2; repo-wide snapshot blames conductor commits; forbidden-tool regex matches the repo's own name; system-skill reads must be whitelisted; plate_uniformity + alpha floor missing) → all are **T0-d acceptance criteria** · images used **2 / 250** (true; audit said 0) · Astra effort now **HIGH** (X1 ran medium) · model verified `gpt-6-astra` · ledger: 5 bursts, rulings R-1/R-2 · legolas R6–R9 returned and folded · canon home live (`painted-2d-pipeline/`) · Q72 open (the agenda) · no push (77+ commits ahead of origin; push is Matt's word).

## 2b. HITL session progress (live; conductor updates as steps land)

| Step | State | Evidence |
|---|---|---|
| 1 | ✓ P1–P6 verified | ledger R-3: P1 one stale MANIFEST row (SPEC.md doc drift) · P3 10/10 SYNC · P6 codex-cli 0.153.4 · origin/main == HEAD |
| 0 (T0-d1) | ✓ DELIVERED + FROZEN | ledger R-4: pre-fix wrapper VOID upheld as audit result, ACCEPT on substance — 86 tests / 84 green (the two reds are T0-d2's); `check_sync.py` live; phantom image call corrected; MANIFEST 110 rows |
| 2 (X1-gen-02) | ✓ DELIVERED through the fixed wrapper | exit 0 · zero violations · image_calls 2 (generated_images/ truth) == calls_used 2 · model/effort/CLI recorded. **Art finding (bible SCALE):** size stated in SOURCE px does not land either (asked ≈380 px/30 %: satchel 48 %, staff head 21 %×66 %; X1-gen-01 relative: 51 %/73 %) → SCALE is a post-process (registration downscale), never a prompt instruction. Plates clean (99.5 % / 98.8 % within ±8). Satchel grain again exceeds the restraint register at prop scale (O8's case) |
| 0 (T0-d2) | ✓ DELIVERED exit 0 + FROZEN | ledger R-5: first clean TOOLING audit under the fixed wrapper; O3b catches F04 bleed (14 ≥ 3) — the T0-c reds green; **two new named reds: O3b counts filled discs (boot toe / face / fist)** → T0-d3 staged; O9 part-inventory set + `calibrate_transcriber.py`; F-5; all R9 extensions; 118 tests / 116 green |
| 2 (X1-chk-02) | ✓ substance / VOID on receipt semantics | ledger R-6: `calls_used` undefined for CHECK → self-reported command count; BURST_RULES v1.2 defines it; plates 99.6 % / 98.9 %; alpha floor → G9 border 0; spill 0; halo 0 |
| 3 (X0-T) | ▶ chain running (X0-T-1..4) | inputs: `runs/C-1/x0t/` (hand inventory re-counted at native; 38/36-question sets; strict schemas) + `fixtures/x0t/` crops; scored by `calibrate_transcriber.py` at chain end |
| 0 (T0-d3) | staged, fires after the chain | O3b annulus discrimination (hollow-centre / inner-edge; synthetic filled discs must count 0; acceptance unchanged) — required before K1's CHECK and the overnight run |
| 4–10 | Matt present | grill packet staged: `~/Desktop/Astra Burst Review - 2026-09-11/00 Grill packet` |

## 3. The session script (≈ 2.5 h with Matt; steps 4–10 need Matt present; 1–3 do not)

| Step | Min | What | Output |
|---|---|---|---|
| 0 | 25 | **T0-d TOOLING burst** (0 images; through the wrapper) → review → freeze → the two T0-c red cases must be green (F04 outside ≥ 3; comparator rejects F04) — else HALT before Matt is asked anything | frozen tree; ledger |
| 1 | 10 | Fresh-session start: charter-freshness gate; SYNC check; ledger read; P1–P6 | go / fix-first |
| 2 | 10 | (if needed) X1 smoke | ledger X1 |
| 3 | 10 | **X0-T transcriber calibration**, bursts 1–4 fired (0 images) — runs while Matt is grilled in step 4; results read at step 6 | `runs/C-1/artifacts/X0-T-*` |
| 4 | 25 | **ELICITOR — vocabulary grill → Bible v0 (F04 Keepers)** — § 4 option sets; Matt rules | rulings ledgered |
| 5 | 10 | **Locks** — resolution table (unrepeatable) · direction-count policy · paintover policy · biome mood · G6b default · ToS disposition (Matt reads the terms) | Q72 struck |
| 6 | 10 | Bible v0 authored live from the rulings (`bible/f04-keepers.json`, schema v0.1); comparator stub validates; **probe set frozen** (`model_drift_probe` set = K1's 3 master prompts + refs); commit | bible committed |
| 7 | 20 | **K1 identity** — 1 GENERATE burst → 3 masters (+ 1 retry burst with Matt's notes if none acceptable) → **Matt picks** → JUDGE + TRANSCRIBE on the pick (X0-T's reliability number now in hand) → milestone packet | master approved |
| 8 | 30 | **K2 turnaround** — 7 GENERATE bursts + CHECK (G1/G2/G3/G7, O1–O8 at native + display size) + JUDGE (control) + PACK → **Matt sees the sheet** | turnaround approved / repair list |
| 9 | 25 | **K3 first loop** — idle-S + walk-S via edit-canvas; CHECK G5/G6/G6b/G11; JUDGE; PACK MP4 → **Matt rules G6b as shipping bar (or not)** | first loop approved |
| 10 | 10 | **ARCHITECT re-gate + overnight charter**: § 11 rows 7/13/25 → RESOLVED; overnight scope + caps + HALT rules confirmed; **Matt's GO word**; launch; session ends | overnight running |

If K2 or K3 FAILs twice in-session → that is a HALT and the overnight run does **not** launch on that path; Matt rules the medium change (F5 method C / bar / pause) in the room, which is precisely why these three milestones are in the HITL window.

## 4. The vocabulary grill — option sets (pre-drafted so step 4 is fast; leans are leans, Matt rules)

**V1 — Signature motif (scope: character; placements measured by O3).**
(a) **a single open ring with one radial hour-mark** — reads at 8 px; template-matchable; goes on the tabard chest and as the rod head (one shape, two placements) *(lean)* · (b) the astrolabe kept as the rod head only, **controlled** — supplied as an isolated reference crop + a positive-plainness clause ("every other surface is plain and undecorated"); the "does an isolated motif crop increase bleed" experiment rides on it · (c) an hourglass / clock-face — on-theme, figurative, hard to keep clean small · (d) no motif — identity by silhouette + materials only (safest vs bleed, weakest faction read).
**V2 — Materials + the machine-legible palette rule (PARTS[].palette_bin).** Set: ivory linen (shirt) · navy wool (tabard) · chestnut leather (harness, satchel, boots) · brass (buckles, rod) · white-lacquered plate + gold trim (advanced) · dark hair. Rule: **no two adjacent parts share a hue bin** (O6 reads parts deterministically; failure modes named: AA borders → 1–2 px erosion; shading → a*b* classification; the art pays for it). Lean: adopt, with the *deliberately unmeasured* parts named (face, hair highlights).
**V3 — Plain-surface budget.** (a) *"one motif, two placements, everything else plain planes"* (Hades/Bastion restraint; F04 clarity) *(lean)* · (b) up to four placements + trim on plate edges · (c) material-driven ornament only (wear, stitching, rivets at load points; no motif on cloth).
**V4 — Construction table (the class with the least precedent and the most need — R6 clause 2).** Every strap terminates at a named part; every fastener closes a named gap; belt count = 1; harness = 1 diagonal, shoulder→opposite hip, carrying the satchel; pauldron asymmetry only on the advanced set (left, oversized). Lean: adopt verbatim; it is ours to author.
**V5 — PILLARS (2–3 filter statements, D4 precedent).** e.g. *"Instruments, not ornaments"* · *"Clean planes, one light"* · *"Every strap carries something."* Lean: those three.
**V6 — LIGHT / SCALE.** Key upper-left (fixed, from the brief); `feature_size_px` per class at 512 canvas; XAG-118 thresholds copied into `element_palette`.

## 5. Locks (step 5) — decision-shaped

**L1 Resolution table (unrepeatable mint-time lock; R9 7.3).** Native cell 627 px → hero ≈ 240 px at 1×. On-screen hero height: 1080p ≈ 240 px (1×) · 1440p ≈ 320 px (1.33×, mild upscale) · 4K ≈ 480 px (2× — visibly soft unless minted at 2×). Options: (a) mint at 627 and accept 1440p as the ceiling *(cheap; lean for the TEST)* · (b) mint 2×2 sheets at 2048 via the API path (ruled out for C-1 by F4) · (c) mint hero frames as single-cell 1254 px (1 frame/call, 4× the calls). Deck floor: 9 px glyph height at 1280×800 for any UI art.
**L2 Direction-count policy.** 8 for heroes and humanoids; for symmetric large monsters, per-animation counts (D2's 1/2/4/8/16) — **but never mirrored under the fixed key light** (F3). Lean: adopt.
**L3 Human paintover.** (a) forbidden in C-1 (pure Astra test; invalidation graph stays clean) *(lean for C-1)* · (b) permitted, marked `human_edited → do_not_regenerate`.
**L4 Biome mood.** (a) baked into plates (one plate = one mood; larger library) · (b) graded at runtime (D2R shipped HDR grading; Godot 2D `CanvasModulate`/shader; smaller library) *(lean: (b), because F6's plate library size is the cost driver)*.
**L5 G6b** — rule now (median bar as shipping bar) or at the K3 milestone with the numbers in view *(lean: at K3)*.
**L6 ToS** — Matt reads OpenAI consumer terms vs business terms for a subscription-authenticated lane; records the disposition (Q72 g). Not delegable.

## 6. X0-T — the hand inventory the transcriber is calibrated against (gandalf, from the native crops viewed 2026-09-11; counts marked ~ are uncertain and must be re-viewed at step 3)

Closed part list (F04 Keeper): hair · face · shirt · tabard · belt · satchel · harness_strap · pauldron_L · pauldron_R · bracer_L · bracer_R · trousers · boots · rod · rod_head · **declared-absent controls: helmet, cape, shield, second_belt**.
- **F04 starter (E07V/art/F04.png, left figure):** hair 1 · face 1 · shirt 1 · tabard 1 · belt 1 · satchel 1 (left hip, brass dial clasp) · harness_strap 1 (diagonal) · pauldron_L 0 · pauldron_R 0 · bracer_L 1 · bracer_R 1 · trousers 1 · boots 2 · rod 0 · rod_head 0 · **sigil-like geometric emblems total ~4** (satchel clasp, tabard hem diagram ×2, belt) · helmet 0 · cape 0 · shield 0 · second_belt 0.
- **F04 advanced (right figure):** hair 1 · face 1 · shirt 1 · tabard 1 · belt 1 (+ a second strap band ~1 — *the functional-implausibility case*) · satchel 1 · harness_strap 1 · pauldron_L 1 (large, emblem) · pauldron_R 1 (smaller) · bracer_L 1 · bracer_R 1 · trousers 1 · boots 2 · rod 1 · rod_head 1 (astrolabe) · **sigil-like emblems total ~7** (pauldron, chest boss, tabard panels ×3, belt, rod head) · controls 0.
- **F03 starter / advanced (E07V/art/F03.png):** part list swaps rod→rifle; counts: coat 1 · shirt 1 · belt 1 (+ tool loops) · pouch 2 · straps ~3 (doubled, load-bearing unclear — the R6 clause-2 case) · rivets: many (not counted; a density metric, O4) · controls: helmet 0, cape 0, shield 0, staff 0.
Question sets are generated from the bible stub by `transcribe/questions.py` (T0-c); the comparator scores presence precision/recall and count ±1 agreement; **controls must be caught 100 %**.

## 7. The overnight autonomous run (fires only on the step-10 GO)

Scope (charter § 7 slate, from where the HITL session ended): X2 → X3 (if needed) → X4 → X5 → X6 → X8 → continuation (Keeper: remaining 7 directions × idle/walk/cast) under the 250-image cap; every experiment CHECK + JUDGE (+ TRANSCRIBE where the part list applies); PACK a milestone packet per experiment into the Desktop review folder; **HALT** on the charter § 8 rules and leave a HALT packet (ledger + last review + diagnosis + decision-shaped fork). The morning packet = ledger summary + review index + the open forks. The conductor for the overnight run is a **gandalf session left running with the ledger as its state** (no Codex autonomy — the bursts are still typed and capped; the *loop* is ours).

## 8. Fresh-session restart prompt (paste verbatim into a new `claude --agent gandalf` session)

> You are gandalf. Run session-start per OP § 1 including the charter-freshness gate (read `.claude/agents/gandalf.md` and `operating-procedures/gandalf.md` § 2 from disk). Then read `canonical/reap-die-rise-game/painted-2d-pipeline/00-system.md` and verify its § 7 SYNC hashes; then `agentic_orchestration/gandalf/notes/2026-09-11-astra-burst-lane-hitl-run-plan.md` and execute it from § 1 (pre-conditions). You are RUN-CONDUCTOR for Run C-1; Astra does all labour via `astra_test_01/burst/lane/run_burst.py`; you write no code. Matt is present for steps 4–10. Do not re-walk `astra_test_01/design/` (HISTORICAL). Begin.

---

Tracker-delta: none (plan; state moves at execution).

— gandalf, 2026-09-11
