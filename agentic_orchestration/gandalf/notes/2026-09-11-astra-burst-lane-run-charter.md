# Astra burst lane — RUN CHARTER v1.0 (Run C-1: "Keeper of Hours")

> **STATUS (v1.1 partial, 2026-09-11):** legolas R6–R8 RETURNED (`legolas/research/2026-09-11-ai-tells-bibles-oracles/findings.md`) — SPEC § 4 rewritten to O1–O9; X0-T added; `cv2` absent; bible schema v0.1 adopted. R9 (scope discovery) in flight. **T0-a building.** DRAFT — **PAUSED BY MATT 2026-09-11 on the AI-tell question** (motif bleed on the F04 figure). ARCHITECT gate (§ 11) is CLEAN except the launch word and two milestone-gated items; **K1 now additionally GATED on Faction Bible v0 + the legolas R6–R8 return** (row 25). Nothing has fired. Author + conductor: gandalf (`RUN-CONDUCTOR`, Matt ruling F7 2026-09-11). Labour: **100 % Astra** (`gpt-6-astra` via `codex exec` bursts, ChatGPT subscription, built-in `image_gen` only — F4 as corrected 2026-09-11).
> **Lineage:** `2026-09-11-astra-burst-lane-review-and-architecture.md` (verdict, § 6 architecture, § 10 rulings); `operating-procedures/desirable-run-pattern.md` (fit test passed, review § 6.7); the brief `codex-3d-modeling/ASTRA TEST 01 painted character vfx.md` (gates 1–10 inherited verbatim); `astra_test_01/design/VISUAL_TARGET.md` + `E07V/FEEDBACK_2026-09-11.md` (Matt's visual rulings); `FACTION_KEY.md` (F04 vocabulary).
> **What this run answers:** *Can Astra, held to strict guidelines, produce painted-2D sprite sheets, a modular gear layer, VFX and a scene plate that pass numeric gates and an independent perceptual judge — 100 % via Astra?* Two consecutive experiment-level FAILs after their diagnosed retries = HALT to Matt, who rules whether that is "Astra ruled out" (which opens the non-Astra path discussion, F6a).

---

## 1. Authority and interface

- **Conductor:** gandalf, foreground. Authors briefs from this charter, invokes bursts, reads receipts and check JSON, views milestone images, keeps the ledger, routes milestones + HALTs to Matt. **Writes no code.** In-run design authority at *reasoning* boundaries only (recorded in the veto-open ledger § 9); *commitment* boundaries HALT to Matt.
- **Labour:** Astra, in typed bursts (§ 4). Astra writes the tooling (once), generates, checks, judges (separate instance), annotates, packs.
- **Out of the run (Matt, "no bulky agentic team infrastructure"):** star-lord, galadriel, drax, legolas. jack-ryan **Gate-1 is waived for the testing phase by that ruling; Gate-2 on the run's close-out is unchanged** (it sits outside the run).
- **Matt interface (declared):** (1) the **GO word** launches T0/X1; (2) **milestones** — identity masters (pick 1 of 3) · turnaround sheet · first loop · first VFX composite · first plate + derived mask — each delivered as a standalone `review.html` + Chrome-playable MP4 copied to `~/Desktop/Astra Burst Review - <date>/` plus a ≤10-line chat summary; (3) **any experiment-level FAIL** surfaced immediately; (4) **HALT** conditions (§ 8); (5) the veto-open ledger of conductor rulings.
- **Push:** commit-only; no push word for this workstream. **Spend:** $0 new (built-in only). **Session concurrency:** ~~one Codex lane, serial bursts~~ → parallel waves for non-TOOLING bursts, TOOLING serial (R-13; `AGENTS.md § 3`). **Concurrency (Matt ruling 2026-09-12, ledger R-13): non-TOOLING bursts (GENERATE / CHECK / JUDGE / TRANSCRIBE / LABEL / ANNOTATE / PACK) may run in PARALLEL WAVES — default wave size 4, larger permitted for a homogeneous wave (the subscription has the headroom); TOOLING bursts stay SERIAL and never overlap any other burst (they write into the shared frozen tree); a wave RESERVES its image caps against the ledger before launch (images_used + Σ caps ≤ run cap); every burst keeps its own workdir, thread-scoped image truth and locked ledger append. The rate-limit HALT rule (three consecutive backoffs) is unchanged.**

## 2. Register card (FROZEN for the run; extracted verbatim into `astra_test_01/burst/REGISTER_CARD.md` by T0)

```
REGISTER CARD — Run C-1 — v1.0 — do not reinterpret; every line is a constraint
STYLE: painted 2D, illustrated, high-res. Not pixel art. Not cel-shaded. F04 CLARITY: clean
  material planes, restrained surface texture, readable small silhouettes, no conspicuous
  brush/pixel grain (Matt: "F01 and F02 seem to show too many brush strokes or pixels").
  Environmental richness and local light-spill on floors/walls in the F03 manner.
  Anchors: E07V/art/F04.png (figures + observatory), E07V/art/F03.png (light/detail),
  run_03/evidence/vfx_style_match.png (painted VFX edge language).
LIGHT: single key from SCREEN UPPER-LEFT, fixed for every frame of every direction; the light
  never rotates with the character. Deep cool low-value ambient; readable shadows, never pure
  black. Slight rim on the key-facing silhouette edge. Spell light is the ONLY warm/saturated
  source and appears only on cast frames. NO floor shadows in sprite frames.
CAMERA: projection C (Godot-informed elevated three-quarter; constants in
  astra_test_01/design/experiments/E01/projection-candidates.json → "C"). All 8 directions are
  the same camera with the CHARACTER rotated. Directions in this order: S SW W NW N NE E SE.
  NO MIRRORING. Weapon stays in the same anatomical hand in every direction.
CANVAS: every delivered frame 512×512, feet pivot at (256,400), S-idle standing height ≈ 240 px.
  Generation happens on 2×2 sheets (1254² native → 627-px cells); frames are registered
  by uniform downscale + translation only (no per-frame scale, no upscaling — ever).
PLATE: all generated art on flat pure #00ff00; matting is done by frozen tools, never in-prompt.
FACTION F04 — Keepers of Hours: ceremonial armor, arcane instruments, deliberate ornamental
  geometry; monumental stonework, fractured observatories. Blue / ivory / brass. No source-game
  names, no copied characters.
FORBIDDEN in prompts: "Diablo", "Last Epoch", any studio/franchise/character name; "pixel art";
  "3D render"; "cel shaded".
```

**Two pre-registered instrument refinements (no bar lowered; both reported):**
- **G2** reports two quantities: the *root anchor* (atlas pivot, ±4 px literal gate) and the *planted-sole contact* trajectory (run_02's own recommendation). The literal gate stays literal.
- **G6b** is registered beside the literal G6: seam MAD ≤ *median* internal adjacent-pair MAD. **G6 (literal) remains the recorded brief gate; G6b is a second instrument.** Whether G6b becomes the shipping bar is **Matt's ruling at the first-loop milestone** — not the conductor's, and never a rescue of a failing candidate.

## 3. Pilot subjects

- **X2–X4:** the run_03 hooded battle-mage — existing 224 frames, existing failures to repair (`astra_test_01/run_03/character/frames/`). Its projection is the brief's 45°/2:1 (that is fine: X2–X4 test *mechanisms*, not projection).
- **K1–K3, X5, X6:** a **new F04 Keeper of Hours.** Identity spec (STORYWRIGHT, one paragraph — ratified when Matt picks the master at K1):
  > **[AMENDED AT K1, Matt 2026-09-12: a young WOMAN; the STARTER carries no insignia — chest plain, no ring head on the staff (plain walnut shaft, brass ferrules); the ring-with-hour-mark is reserved as an earned advanced-set motif; Bible v0.1. Face (Matt at K1, second set): a smooth, softly rounded chin with NO cleft and a soft jawline — a chin cleft reads masculine.]** A young archivist of the Keepers (a young woman), early 20s, dark curly hair tied back, sun-browned; ivory shirt under a blue sleeveless tabard cut with a single pale geometric sigil, brass-buckled leather harness, a satchel of instruments on the LEFT hip; **weapon: a brass-headed astrolabe-rod held in the RIGHT hand**, its ringed head the silhouette read at 64 px together with the hair mass. Starter outfit as above; **advanced outfit:** white-and-gold segmented plate over the same body, one oversized pauldron on the LEFT shoulder (asymmetry is the second 64-px read), astrolabe-rod unchanged. Face fully visible (no helmet by default; helmet visibility is a separate toggle).
- **Scene plate (X6):** an F04 **observatory chamber** — monumental stone, fractured dome, brass orrery, one N exit and one S exit.

## 4. Typed bursts — the rules (extracted verbatim into `astra_test_01/burst/BURST_RULES.md` by T0)

**Every burst:** a fresh `codex exec` (`--ephemeral`, profile `astra-burst`, `-C` a workdir **outside the repo** — `~/astra-burst/runs/<run>/<burst>/` — so no `AGENTS.md`/`CLAUDE.md` context loads; measured boot ≈ 19K tokens), `-s workspace-write` scoped to that workdir, `</dev/null`, `--json` event stream captured, `--output-schema receipt.schema.json -o receipt.json`. **Receipt field semantics (v1.2, 2026-09-12 — X1-chk-02 VOID):** `calls_used` = the number of `image_gen` calls made, and NOTHING else — it is 0 for every burst type except GENERATE and LABEL (tool/command counts are censused by the wrapper, never self-reported); the wrapper VOIDs any receipt whose `calls_used` disagrees with the `generated_images/` truth source. **Hard caps (v1.1):** GENERATE / CHECK / JUDGE / TRANSCRIBE / LABEL / ANNOTATE / PACK ≤ 15 min wall, ≤ 20 tool calls; **TOOLING ≤ 40 min, ≤ 60 tool calls** (T0-a measured 7.4 min / 10 calls for the smallest module); image calls per type below. Prompt = REGISTER CARD + BURST RULES + TASK + REFERENCES (`-i`, roles named) + RETURN (schema). Forbidden in every burst: `web__run`, `collaboration.*`, reading anything outside the workdir and the frozen tools path (Codex's own loaded skills — `$CODEX_HOME/skills/.system/` and the agent-skills path `~/.agents/skills/` — are permitted and expected reads — X1 F-4, 2026-09-11; K1-pack-01, 2026-09-12), writing anything outside `out/`, creating or modifying code (TOOLING excepted), declaring PASS/FAIL (only the conductor's gates and the JUDGE rubric produce verdicts, and JUDGE produces *scores*).

| Type | May | May not | Image cap | Output |
|---|---|---|---|---|
| **TOOLING** (T0, once; re-run only by a new TOOLING burst) | write code under `astra_test_01/burst/tools/` (via `--add-dir`); run self-tests | generate images; touch anything else in the repo | 0 | tools + `tools/MANIFEST.sha256` + self-test JSON; **conductor DRIFT-CRITIC review, then FROZEN** |
| **GENERATE** | call `image_gen`; `view_image` on given references; copy outputs to `out/`; sha256 them | any code; any file outside `out/`; any web | per task (≤ 4–12) | PNGs + receipt |
| **CHECK** | run frozen tools on named inputs; write `checks.json` | image calls; code; edit inputs | 0 | `checks.json` |
| **JUDGE** (separate instance — never the generating context) | `view_image` on candidates + anchors + the hidden control; write `judgment.json` (per-axis scores + one-line reasons) | image calls; code; see any receipt or prior judgment | 0 | `judgment.json` |
| **ANNOTATE** (X6) | `view_image`; write polygon JSON (walkable / blocked / occluder / exit bands) | image calls; code | 0 | `annotation.json` |
| **PACK** | run frozen pack/preview tools; write sheets, `atlas.json`, engine-neutral manifest, `review.html`, MP4, Godot port notes | image calls; code | 0 | review packet |
| **TRANSCRIBE** (separate instance — never the generating context; v1.1, legolas R8 § 3.2) | `view_image` on the candidate(s) + anchors; answer the question set — **presence/absence and per-part counts against the closed part list ONLY, never coordinates, never open vocabulary**; write `inventory.json` (strict schema) | image calls; code; bounding boxes; seeing any receipt or prior inventory; any file outside `out/` | 0 | `inventory.json` |
| **LABEL** (route-2 part masks; v1.1) | call `image_gen` in EDIT mode on the given approved frame: repaint each declared part in its flat label colour, change nothing else; copy output to `out/` | any code; any other generation; any file outside `out/` | ≤ 2 | label PNG + receipt |

**Wrapper audit after every burst (deterministic, conductor-side, written by T0):** event-stream census (image calls, tool names, write paths) · receipt schema valid · every listed file exists with matching sha256 · no forbidden tool · caps respected. Any violation → the burst is **VOID** (not FAIL): rerun once with the violation named; a second VOID → HALT.

**Two-attempt rule with scope guard:** inside an experiment, one diagnosed retry per burst. A second failure returns to the conductor, who may change *method within the hypothesis* (guide, reference set, generate→edit-canvas, chaining) and registers it in the ledger — **never medium** (no rigs, meshes, renderers, textures-on-geometry). Medium changes are Matt's.

## 5. Frozen tools (T0 builds; lineage named so nothing is reinvented)

`guides.py` (run_02 → projection **C** constants) · `pipeline.extract` chroma matting, particle-safe (run_02) · `registration_preflight.measured_anchor` (run_02) · `turnaround.py` / `check.py` gates G1–G3, G5, G6 + **G6b**, G9 (run_03) · `check_vfx.py` (run_03) · `package.py` + `preview_template.html` (run_03; **plain HTML player stays; Pixi viewer-only per F7c is added *only* for X6's mask overlay + y-sort** — no sim/doors/nav/shadows/bones/shaders, and the rule is printed in the file header) · **new:** `drift48.py` (G11: 48-px downsample, neighbour diff; consecutive < frame-0-vs-cast-05 comparator — G5 restated) · `mask_composite.py` (X3/X5: |variant − base| thresholded + dilated inside a declared region box; **base pixels outside the mask byte-identical**; G12 ≥ 99 % preserved) · `plate_scale.py` (X6: scale plate so the declared doorway height = 480 px ± 10 %; exit centres within ±10 % width bands; G13) · `rasterize_annotation.py` · `audit_burst.py` (§ 4 wrapper audit) · `run_burst.py` (templating + `codex exec` + audit + ledger) · `receipt.schema.json` · **self-tests with known-bad inputs** (run_02's seven instrument tests as the model: checkerboard rejection, upscaling rejection, clipped-sole rejection, wrong-side light, shifted mask, repeated-lead, swollen bag). **Freeze = MANIFEST.sha256 + self-tests green + conductor review.**

## 6. JUDGE rubric (extracted into `astra_test_01/burst/JUDGE_RUBRIC.md` by T0) — **v1.1 note (legolas R8):** the ownership / functional-implausibility class (CHI 2025: 58.7 % prevalence, 64.1 % human detection — the most prevalent AND least-caught) is the class a JUDGE most often passes; it is reached only by **O9 TRANSCRIBE→COMPARE** (presence + counts against the bible's closed part list, declared-absent controls, counts cross-checked by O3). JUDGE keeps the taste residue (§ 3.9 backlog); `TRANSCRIBE` is a distinct burst type

Five axes, 1–5, one-line reason each. **Mandatory:** axes 1–3 ≥ 4. Composite ≥ 3.8. Judged at native and at 64 px.

| # | Axis | Anchor |
|---|---|---|
| 1 | **Register fidelity** — F04 clarity (clean planes, restrained texture, no grain) | `E07V/art/F04.png` figures |
| 2 | **Identity persistence** vs the approved master (face, hair mass, costume elements, proportions, accessory count) | the approved master |
| 3 | **Light obedience** — key upper-left; spell the only saturated source | `run_03` cast frame (`vfx_style_match.png`, left) |
| 4 | **Silhouette read at 64 px** (rod head + hair / pauldron distinct) | `run_03/character/turnaround_64px.png` |
| 5 | **Brush-register consistency** across frames and with VFX | `run_03/evidence/vfx_style_match.png` |

**Known-bad controls — one hidden control in every JUDGE batch; a judge that passes its control VOIDS the batch:** (a) a horizontally mirrored candidate (key now upper-right) must fail axis 3; (b) `E05W` low-poly pilot crop (`design/experiments/E05W/evidence/batch-04/review.png` figure) must fail axis 1; (c) for plates, `E07V/art/F01.png`'s bottom-right doorway must fail the doorway-side check; (d) for gear, a 20-px-shifted overlay must fail identity. Two VOID judgments in a run → HALT.

## 7. The slate (order fixed; image caps per experiment; run cap 250)

| # | Experiment | Hypothesis / falsifier | Bursts | Image cap |
|---|---|---|---|---|
| **T0** | TOOLING — build + freeze § 5; extract card/rules/rubric; execute **F8** (HISTORICAL banners on `design/START_HERE.md` + `PROGRESS.json`; retire the campaign pointer in `.agents/skills/painted-character-vfx/`; harvest list → `astra_test_01/burst/HARVEST.md`) | tools pass self-tests incl. known-bad inputs; else no run | 1–2 TOOLING | 0 |
| **X1** | Lane smoke — GENERATE a Keeper satchel + rod on green plate (2 calls), CHECK matting/alpha, JUDGE with control, PACK a 1-page review; audit + ledger round-trip; **verify the burst context is minimal** (event stream shows no repo `AGENTS.md`/`CLAUDE.md` injection) | any audit/receipt/hash failure = fix T0 before X2 | 1 each type | 4 |
| **X0-T** | **Transcriber calibration** (legolas R8 gap 2 — no published reliability figure for VLM part-inventory transcription on illustrated images): gandalf hand-authors the part inventory of the F04 + F03 figures (presence + counts against the closed PARTS list, with ≥ 2 declared-absent controls); 4–8 TRANSCRIBE bursts answer DSG-shaped question sets; comparator scores agreement + control catch-rate | precision/recall on presence ≥ 0.9 and counts within ±1 on ≥ 80 % of parts, controls caught 100 % — else O9 stays advisory and K1's ownership check falls to Matt's eye (recorded) | 4–8 TRANSCRIBE, 1 CHECK | 0 |
| **X2** | Idle seams via **edit-canvas**: the six failing run_03 directions (SW NW N NE E SE), approved idle-00 in slot 0 of every 2×2 canvas, every new frame generated with an approved neighbour in-canvas (chaining proposed by Astra in the X2 registration, conductor approves) | ≥ 5/6 pass G6b (report G6 literal too); *falsifier:* edit mode repaints the seed → generation cannot hold pixels → X3 mandatory | 6 GEN (+≤6 retry), 1 CHECK, 1 JUDGE | 14 |
| **X3** | Masked composite (conductor-side `mask_composite.py`): generated moving regions onto the locked base | G12 ≥ 99 %; G6/G6b rerun; G11 | 1 CHECK, 1 JUDGE | 0 |
| **X4** | Rear-view gait with numbered-foot silhouette guide (N NW NE walk) | correct alternating lead ≥ 2/3 (JUDGE + G5/G11) | 3 GEN (+≤3), CHECK, JUDGE | 8 |
| **K1** | **Keeper identity** — 3 masters from § 3 spec (+3 with Matt's notes if none acceptable; then HALT) | **MILESTONE: Matt picks** | 1–2 GEN, JUDGE | 6 |
| **K2** | Keeper turnaround — 7 directions, master + C guide | G1–G3, G4/G7 (JUDGE); **MILESTONE: Matt sees the sheet** | 7 GEN (+≤7), CHECK, JUDGE, PACK | 16 |
| **K3** | Keeper idle-S + walk-S (edit-canvas) | G5, G6/G6b, G11; **MILESTONE: first loop** (Matt rules G6b-as-shipping-bar here) | 4 GEN (+≤4), CHECK, JUDGE, PACK | 12 |
| **X5** | **Gear layer, Method B** — advanced outfit on S idle + walk composited onto the locked base | G12 ≥ 99 %; JUDGE identity + 64-px read; *falsifier:* the overlay cannot be isolated → Method C (separate layer sheet) registered | 3 GEN (+≤3), CHECK, JUDGE | 14 |
| **X6** | **Scene plate** — F04 observatory, N/S exits in edge bands, doorway-side rule; 3 candidates → Matt picks 1 → one edit-pass doorway fix (SSIM ≥ 0.98 outside the edit box) → ANNOTATE masks → JUDGE (control (c)) → PACK with Pixi-viewer mask overlay + y-sort of the Keeper against the orrery; prop sheet (chest closed/open) | G13; masks agree with the painting on JUDGE; **MILESTONE: first plate + mask** | 3 GEN (+≤3), ANNOTATE, CHECK, JUDGE, PACK | 12 |
| **X8** | **VFX material impact set** — frost impact on flesh + stone (2 modules) + one blood-decal atlas sample (Matt's F01 splatter reference) via the run_03 frost pipeline | G8 (JUDGE axis 5), G9 alpha, emissive-from-energy; **MILESTONE: first VFX composite**; *note:* built-in moderation refusing gore is recorded as a finding, not retried | 3 GEN (+≤3), CHECK, JUDGE, PACK | 12 |
| **T0-d** | Lane extensions (R9 — SPEC § 6 row): check_sync, provenance_capture, ref_provenance, model_drift_probe (define + first run), pse_check (XAG-118), matte_quality, sheet_consistency, receipt/bible field extensions | tests green; probe set frozen; `check_sync` returns 0 on the committed tree | 1 TOOLING | 0 |
| — | **Continuation clause:** if K3 + X5 pass and Matt says GO at the first-loop milestone, the run continues into full Keeper coverage (remaining 7 directions × idle/walk/cast) under the remaining cap | | | ≤ 150 |

Sum of caps ≈ 98 before the continuation clause; run cap **250**.

## 8. HALT rules (to Matt; the run does not decide)

Two consecutive experiment-level FAILs after their diagnosed retries · two VOID bursts in a row · a JUDGE passing its control twice · three consecutive rate-limit backoffs (subscription throttling; the run_01 "rate increased" case) · any write outside `out/` · run cap reached · any question that is a medium change or a bar change. A HALT packet = the ledger + the last review + a one-paragraph diagnosis + the fork, decision-shaped.

## 9. Ledger and records

**v1.1 (R9):** receipts gain `generator.observed_fingerprint` (probe-set distance — the built-in path exposes no model id) and `regeneratable_until`; **the approved PNG is the artifact of record, not the prompt**; `model_drift_probe.py` RUNS at K1 and at every burst-day boundary (probe set frozen + hashed into the bible); C2PA provenance captured at ingest **before** matting; only first-party assets may condition a mint. `astra_test_01/burst/runs/C-1/ledger.json` — conductor-owned, never written by a burst: `bursts[] {id, type, experiment, images_used, tool_calls, minutes, audit, receipt_sha, verdict_source}`, `images_used/cap`, `experiments[] {status PLANNED|RUNNING|DELIVERED|PASS|FAIL|VOID|HALTED}`, `milestones[]`, `halts[]`, `rulings[]` (veto-open conductor rulings, each with the reasoning boundary it sat at). Approved PNGs stay local (repo `*.png` ignore policy) + in the Desktop review folders; receipts, JSON, HTML, manifests and hashes are committed.

## 10. Codex profile (conductor writes `~/.codex/astra-burst.config.toml` at launch; shown here for Matt's eyes first)

```toml
model = "gpt-6-astra"
model_reasoning_effort = "high"        # Matt 2026-09-11: Astra ALWAYS at HIGH effort — every burst type, no per-burst downgrade
approval_policy = "never"
sandbox_mode = "workspace-write"
# no plugins, no mcp_servers — the global config's Vercel plugin throws AuthRequired every session
[features]
js_repl = false
```
Base instructions per burst are the brief; no AGENTS.md is loaded because the workdir is outside the repo (verified by X1).

---

## 11. ARCHITECT PASS — open-questions gate (every decision the run will hit)

| # | Decision the run hits | Class | Where resolved / criterion |
|---|---|---|---|
| 1 | Register (2D painted vs hybrid vs 3D) | **RESOLVED** | F1 = painted 2D, no hedge; 3D lock untouched |
| 2 | Camera / projection | **RESOLVED** | F2 = C (Matt's prior act) |
| 3 | Light rule / mirroring | **RESOLVED** | F3 (Matt's brief) |
| 4 | Canvas, pivot, height, direction order, plate | **RESOLVED** | the brief; run_02/03 |
| 5 | Image path | **RESOLVED (corrected)** | built-in only; API parity = non-Astra path, deferred; T25 withdrawn |
| 6 | Pilot subjects | **RESOLVED** | F1a |
| 7 | Keeper identity *spec* text (§ 3) | **RESOLVED 2026-09-12** | ratified by Matt's K1 pick: master L (K1-gen-04, text-designed; young woman, plain starter, no insignia) — ledger R-12 |
| 8 | Conductor / labour / other seams | **RESOLVED** | F7, F6a; Gate-1 waived for testing; Gate-2 unchanged |
| 9 | Harness | **RESOLVED** | F7c Pixi viewer-only (X6 only); plain HTML player otherwise |
| 10 | Scene model + which plate | **RESOLVED** | F6; F04 observatory |
| 11 | Gear method order | **RESOLVED** | B first (§ 7 X5); C as registered fallback |
| 12 | Judging | **RESOLVED** | separate Astra instance + § 6 rubric + known-bad controls |
| 13 | G6b as shipping bar | **GATED+TRACKED (re-gated 2026-09-12, R-17)** | deferred to oracle-tuned gates: legolas R10/R10b returned → T1 gait contract calibrated → loops re-run and compared to the oracle → then Matt rules; K3's numbers (walk G6 literal 3.058 vs 3.009 fails, G6b ≤ 3.459 passes) are the recorded case |
| 14 | Budget / halt | **RESOLVED (default, veto-open)** | 250 images; HALT on 2 consecutive FAILs — Matt's "see above"; corrects at will |
| 15 | Edit-canvas chaining scheme (3 calls per 8-frame loop, seed/neighbour-in-canvas) | **RESOLVED-BY-CHARTER, detail delegated** | Astra proposes in the X2 registration; conductor approves (reasoning boundary; ledgered) |
| 16 | Mask / plate-scale thresholds (G12 99 %, doorway 480 ± 10 %, bands ± 10 %) | **RESOLVED-BY-CHARTER, pre-registered** | frozen at T0 before any candidate is generated |
| 17 | Milestone cadence | **RESOLVED** | per stage + any FAIL |
| 18 | Corpus disposition | **RESOLVED** | F8, executed in T0 |
| 19 | Codex profile creation (a write to `~/.codex/`) | **RESOLVED-BY-F7** | conductor's instrument; contents shown § 10 |
| 20 | Burst context isolation (no repo AGENTS.md) | **GATED+TRACKED** | X1 verifies from the event stream; fallback = `-c project_doc_max_bytes=0` or a burst-local AGENTS.md override |
| 21 | Blood / gore under built-in moderation | **GATED+TRACKED** | X8 records a refusal as a finding (feeds the non-Astra/API discussion if it ever opens) |
| 22 | Non-humanoid forms, full roster, 3 tiers × 100 | **OUT OF SCOPE** | Run C-2+ (KR build wave after this run) |
| 23 | Factions ↔ Glitch Archive fold | **OUT OF SCOPE** | STORYWRIGHT session (F9) |
| 24 | Launch | **RESOLVED for the HITL run (GO given 2026-09-11/12; T0 → K3 executed); OVERNIGHT AUTONOMOUS RUN NOT LAUNCHED (Matt, R-17: oracle-first)** | next launch = the post-oracle HITL session; overnight slate draft kept at the plan note |
| 26 | **Animation oracle + gait tooling** (walk/idle cycle rules, numbered-foot guides, breath spec; T1 contract) | **GATED+TRACKED** | empirical criterion: legolas R10/R10b findings returned (in flight 2026-09-12) → T1 gates calibrated on the measured reference → idle-S + walk-E re-run and compared to the oracle. Everything standing on loops (composite proof, gear-on-loops, continuation) waits behind it |
| 27 | Pilot subject for the remaining slate (run_03 mage vs the Keeper) | **OPEN — Matt** | conductor lean: retire the mage; the Keeper is the pilot |
| 28 | Advanced-set motif placements (the reserved ring-with-hour-mark) | **OPEN — Matt** | ruled when X5 is chartered; default lean pauldron_L + staff head, count 1 each |
| 25 | **AI-tell control** — faction bible (motif placement/exclusions, material inventory, construction logic, plain-surface budget), register-card TELL-CONTROL block, JUDGE axis 6 (tell audit; F04 advanced-figure crop as known-bad control), deterministic oracles feeding the bible (bible ↔ oracle loop) | **GATED+TRACKED** | legolas Mode A R6/R7/R8 commissioned 2026-09-11 (`gandalf/requests/2026-09-11-legolas-mode-a-ai-tells-art-bibles-oracles.md`); then Bible v0 (gandalf) + vocabulary grill (Matt) → charter v1.1. **K1 does not fire before.** T0/X1–X4 have no bible dependency (mechanism repairs on the existing mage) — may fire on Matt's word while research runs |

**Gate verdict (amended 2026-09-11): CLEAN for T0/X1–X4; K1 onward GATED on row 25.** No OPEN Matt-gated fork remains before launch except the launch word. Items 7 and 13 are correctly milestone-gated (they cannot be decided before the artifact exists). No new `matt_decision_needed/` rows are warranted.

— gandalf, 2026-09-11
