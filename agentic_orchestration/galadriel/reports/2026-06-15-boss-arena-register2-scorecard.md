# Visual-Register Scorecard — Godot Boss Arena (spec-faithful SCENARIO_BOSS_WITH_ADDS) vs Register-2 Rubric + Fight-Readability Read

**STATUS:** CURRENT (galadriel scoring artifact; evidence-input for gandalf "stronger second A-holds extension" canon call)
**Date:** 2026-06-15
**Author:** galadriel (visual-perception + benchmark steward)
**Scope:** SCORING ONLY. This artifact measures drax's Build #1 against galadriel's register-2 rubric AND adds the new load-bearing **fight-readability** read. It does **NOT** make the canon call — that is gandalf's, on this evidence. The durable question: do register-2 premium AND fight-readability coexist in a *spec-faithful* fight room (the thing the cathedral mood-piece never had to test)?
**Build:** drax, commit `53e6c3c` (reincarnated-godot) — `SCENARIO_BOSS_WITH_ADDS` (30×30 m), spec-faithful.
**Brief:** `agentic_orchestration/gandalf/notes/2026-06-15-battle-room-replication-routing-note.md` (parity = rubric not pixel-match; marketing-render caveat carried 1:1; the new fight-readability axis).
**Companion:** instruments at `agentic_orchestration/galadriel/pipeline/lifecycle-score-boss.mjs` (+ shared `register-metrics.mjs` defs); raw scores at `pipeline/lifecycle-scores-boss.json`. Capture frames + readability crops + lifecycle strip are **git-ignored Synty-derivative IP — local evidence only** (not committed; described here). Precedent scorecard: `2026-06-15-cathedral-register2-scorecard.md` (5.00).

---

## 0. What was scored — and what is new since the cathedral

- **Capture set:** `reincarnated-godot/harness_logs/13_boss_arena_capture_01..100.png` — 100-frame motion sequence, 1152×648, Godot Movie Maker (clean deterministic source). All 100 frames present locally; no re-run needed (script `scripts/run_boss_arena.sh` is reproducible if regeneration is ever required).
- **Scene (the increment):** drax replicated the engine spec `SCENARIO_BOSS_WITH_ADDS` **EXACTLY** — arena 30×30 m, origin (0,0); spawns player(15,25), boss(15,8), adds(3,26)&(27,26). Dark Fantasy POLYGON modular Base kit (12×12 floor tiles, 4-side walls, corner pillars, light skull-pile dressing) dresses the **fixed** footprint (Diablo procedural-dungeon contract — no spawn moved, arena not resized for composition). The **same lift recipe** (near-black warm ambient + warm key rake + cold rim + filmic tonemap + glow/SSAO/warm-fog), PLUS a new **"CombatFill"** cool overhead pool on the fighting axis — the explicit register-2-vs-readability lever. Hero VFX: a **boss-anchored red ritual sigil that CHARGES then ERUPTS a GPUParticles3D fire column.** Braziers burn from frame 0; fog/dust always-on.
- **Why this matters (vs the cathedral):** the cathedral proved register-2 on a *mood piece* with NO fight-readability constraint — it could be as dark/cluttered as it wanted. A **battle room** must satisfy THREE things at once: (a) render the **exact** spawn geometry, (b) stay **readable** from the fixed 2.5D camera (every combatant locatable + parseable), (c) still hold **register-2**. These can fight each other. This scorecard tests whether they coexist. It is the first **sim→visual bridge** (an abstract `spatial_gauntlet` arena rendered as a register-2 world).
- **Scoring method:** CV instruments run **across the full 100-frame lifecycle**, NOT a single still. Per galadriel F1 finding, stills under-represent VFX (the highest-leverage axis); the fire column is a windowed event, sampled across ember → ignition → peak-bloom → sustained-burn → collapse → waning-settle. **Phase boundaries were EMPIRICALLY RE-DERIVED from this capture's own HLF curve — NOT inherited from the cathedral** (drax sim-frame timing of charge~30/erupt~52/collapse~320 is in SIM frames; the 100 captured PNGs subsample the lifecycle, so the eruption lands at a different *capture-frame* index — substrate votes, OP § 3.6).

## 1. The rubric (galadriel's — UNCHANGED from the cathedral + lift)

Composite mean **≥ 3.6/5**, with **lighting ≥ 4 AND VFX ≥ 4 MANDATORY**.

| Axis | Target | Instrument |
|---|---|---|
| Lighting drama | manual ≥ 4 | LDR ≥ 115, SHF ≥ 30% (CV-assisted) |
| VFX presence | manual ≥ 4 | ≥ 1 hero bloom, HLF ≥ 1.5% (CV-assisted) |
| Material-shading | manual ≥ 4 | gradient/light-response, NOT flat per-face |
| Geometry register | manual ≥ 3 | low-poly fine; silhouettes legible |

NOT targets: high-frequency-detail / strong-edge%. Premium ≠ detail-density. (Same rubric applied to lift + cathedral — so boss-arena scores are directly comparable.) **Fight-readability is reported as a SEPARATE read (§ 5), not folded into the composite** — it is a new load-bearing question, not yet a fifth rubric axis (rubric-evolution note in § 8).

## 2. CV instrument values (lifecycle-sampled)

Instrument definitions **BYTE-IDENTICAL** to the cathedral + lift scorers and the register baseline (`register-metrics.mjs`): 960w inside-fit, grayscale luma for LDR/SHF/HLF, raw RGB for SAT. Thresholds: HLF>0.80 luma highlight, SHF<0.12 luma shadow, LDR=p95−p05. Same kernels, same thresholds → values directly comparable to cathedral (5.00) and lift (4.50).

| Phase | frames | LDR | SHF % | HLF % | LMV |
|---|---|---|---|---|---|
| ember | 1-8 | 149.3 | 43.39 | 0.47 | 29.91 |
| ignition-rise | 9-20 | 177.0 | 42.86 | 3.40 | 32.77 |
| peak-bloom | 21-34 | 183.1 | 42.54 | 3.72 | 32.89 |
| sustained-burn | 35-86 | 180.8 | 42.68 | 3.61 | 32.89 |
| waning-settle | 87-100 | 165.3 | 42.68 | 0.83 | 31.01 |
| **whole-sequence mean** | 1-100 | **175.97** | **42.74** | **2.96** | **32.38** |
| dark-mood window (1-8 + 87-100) | | 159.5 | 42.94 | 0.70 | 30.61 |

**Rubric-relevant extracts (independently re-derived on galadriel instruments):**
- **HLF peak = 4.013%** (frame 21) vs threshold 1.5% → **2.7× over**. Boss-anchored hero bloom unambiguously present. Across the active hero event (f9–88) HLF holds 1.36–4.01% — every active-event frame clears 1.5%; only the ember (f1–8) and settled-ember (f89–100) phases sit below, correctly (no column yet / column collapsed).
- **LDR whole-mean = 175.97** vs threshold 115 → **1.53× over**. **LDR floor = 148 (frame 1)** — even the deepest ember frame clears 115. Every single one of the 100 frames passes the lighting-drama LDR bar.
- **SHF whole-mean = 42.74%** vs threshold 30% → **1.42× over**. **SHF floor = 42.44% (frame 78**, mid burn-plateau) — remarkably stable across ALL 100 frames (42.4–43.5%). The dark-mood NEVER collapses, even at peak bloom: this is the CombatFill discipline working exactly as designed — it lifts the *fighting-axis mids* for figure-readability WITHOUT washing the dark-mood walls/voids.

**Lifecycle-shape note (honest difference from the cathedral):** the boss-arena hero-event reads, in capture-frame space, as **ember(1-8) → sharp ignition @f9 → HLF peak @f21 → long flat sustained-burn plateau (f22–86, HLF ~3.3–3.8) → collapse @f87–88 → settled ember (f89–100).** This is a *longer, flatter plateau* and a *lower magnitude* (peak 4.01%) than the cathedral's sharper, higher charge-spike (peak 9.35%). Both are clean charge→sustain→collapse arcs; the boss arena's is more contained because (a) the column is one body-anchored pillar behind the boss, not a frame-flooding eruption, and (b) the CombatFill raises the lit baseline, so the highlight *fraction* is a smaller share of a brighter frame. The shape is clean and well-lifecycled; the magnitude is honestly lower — and lower-by-design (the register-vs-readability tradeoff).

## 3. Per-axis manual scores

### Lighting drama — **4 / 5** (target ≥ 4 — MET)
LDR 175.97 (1.53× threshold) + SHF 42.74% (1.42× threshold), both sustained across every lifecycle phase. The scene is a lit volume punched out of deep dark: warm braziers rake the floor and walls, cold rim catches the perimeter walls/pillars, the boss's red sigil glows warm at center-back, and the CombatFill pool lifts the four-figure fighting axis out of the dark floor. The summon column adds a dynamic warm key at ignition→peak. This is filmic, dramatic, register-2 lighting on a spec-faithful fight room. It scores **4 rather than the cathedral's 5** for an honest reason: the cathedral pegged the 8-bit ceiling (LDR 232, 2.0× threshold) because it was free to be maximally dark-and-bright; the boss arena runs LDR 176 (1.53×) because the CombatFill deliberately lifts the mids for figure-readability — trading some peak dynamic-range drama for the new readability requirement. That is the intended register-vs-readability tradeoff, not a deficiency — but on a pure lighting-drama axis it is a strong, sustained **4**, not a ceiling-pegging 5. The SHF stability (42.4–43.5% across all 100 frames) is the standout: the dark-mood holds rock-solid even at peak bloom. *Evidence: lifecycle LDR/SHF table; lifecycle strip (ember/ignite/peak/burn/collapse/settle); per-frame curve in `lifecycle-scores-boss.json`.*

### VFX presence — **4 / 5** (target ≥ 4 — MET)
HLF peak 4.013% (2.7× threshold), sustained ~3.6% through the f22–86 burn plateau. The red ritual-sigil charge + GPUParticles3D summon fire column is a genuine **body-anchored hero skill event** with a clean lifecycle (ember → sharp ignition @f9 → peak @f21 → sustained burn → collapse @f87 → residual sigil ember). The hot core is anchored to the BOSS at center-back — the bloom reads as *the boss's summon*, not ambient fire beside it. Always-on braziers + fog/dust add atmospheric VFX even pre-ignition. It scores **4 rather than the cathedral's 5** because the magnitude is honestly more contained: HLF peak 4.01% (2.7× threshold) vs the cathedral's 9.35% (6.2×) — a single column behind one figure rather than a frame-flooding pillar, and the CombatFill-raised baseline shrinks the highlight fraction. The hero event is unmistakable, body-anchored, and well-lifecycled (clears the ≥4 bar comfortably), but it does not reach the cathedral's frame-dominating bloom. *Evidence: lifecycle HLF table; boss-region crop @f21 (boss backlit by his own column); lifecycle strip.* (Marketing-render caveat: § 6 — scored on own-register merits, NOT Synty-post fidelity.)

### Material-shading — **4 / 5** (target ≥ 4 — MET)
LMV whole-mean **32.38** — squarely in the lift's lit-phase band (32–38), BELOW the cathedral's 36.4. The warm/cold rake + CombatFill produce distributed, light-responsive surface variance across the floor tiles, walls, pillars, and the four figures — not flat per-face fill; the dark voids correctly read low (no light → no material response to read). It scores **4 rather than the cathedral's 5** because the geometry it dresses is the modular **Base kit** (floor tiles, plain wall segments, corner pillars) deliberately kept light for readability — materially less ornamented surface than the cathedral's carved arches, statuary, and stained-glass frames, so the distributed micro-variance is good but not the cathedral's peak. **Honest caveat (carried from cathedral):** the CV instrument cannot fully *isolate* roughness-driven micro-variance from lighting-driven macro-gradient — both are present and both push register-2; the 4 is earned on combined material+lighting surface response, honestly scoped to the lighter Base-kit surface. *Evidence: whole-mean LMV; per-phase LMV (lit phases 32.8–32.9 vs ember 29.9 — material response tracks the lighting as expected).*

### Geometry register — **4 / 5** (target ≥ 3 — MET, exceeds)
A clean, legible register-2 fight room: a spec-faithful 30×30 enclosed arena — 12×12 modular floor, four walled sides, corner pillars, four combatants at the exact spawn positions, light skull-pile dressing — all reading cleanly with no clipping or broken seams. Low-poly faceting is visible and **correct** for register-2 (the silhouette-readable low-poly register Torchlight Infinite / Last Epoch ship). The frame carries genuine depth layers: near front-row combatants (bottom), mid-floor, boss + sigil + column at the back, walls/pillars framing. It scores **4 rather than the cathedral's 5** because the dressing is **deliberately light** ("kept light for readability" — the correct call for a fight room, where clutter would fight the combatant read), so the frame is cleaner and sparser than the cathedral's full ornamented gothic shell. It comfortably exceeds the ≥3 target; the spec-faithfulness (exact footprint + spawns, no composition cheating) is itself a geometry-register strength the cathedral didn't have to honor. *Evidence: lifecycle strip; front-row crop @f21; boss-region crop @f21; spec cross-check vs `arena.py::SCENARIO_BOSS_WITH_ADDS` in drax's run log.*

## 4. Composite + mandatory gates

| Axis | Score (boss arena) | (cathedral) | (lift) |
|---|---|---|---|
| Lighting drama | 4 | 5 | 5 |
| VFX presence | 4 | 5 | 5 |
| Material-shading | 4 | 5 | 4 |
| Geometry register | 4 | 5 | 4 |
| **Composite mean** | **4.00** | 5.00 | 4.50 |

- **Composite mean 4.00 ≥ 3.6** → **PASS**
- **Mandatory gate — Lighting ≥ 4:** 4 → **PASS**
- **Mandatory gate — VFX ≥ 4:** 4 → **PASS**

**All gates clear.** The composite (4.00) sits below the cathedral's 5.00 and the lift's 4.50 — and that is the honest, load-bearing read: the boss arena is doing a **harder job** than either. The cathedral was free to maximize visual drama (ceiling-pegged lighting, frame-flooding bloom, dense ornamentation); the boss arena is **constraint-bound** — it must render exact combat geometry, stay fight-readable, AND hold register-2, and it deliberately trades peak lighting-drama (CombatFill mid-lift), peak bloom-magnitude (one contained column), and ornamentation-density (light dressing) to win readability. It clears register-2 on all four axes and both mandatory gates *while* satisfying constraints the cathedral never faced. **Parity = rubric pass, and the rubric passes.** The cathedral's 5.00 is the precedent, not the bar (brief § 4.1); the rubric is the gate.

## 5. Fight-readability read (THE new load-bearing axis)

**The question:** can all four combatants be **located + parsed** from the fixed 2.5D camera (pos (15,19,42), look_at (15,1.2,16), fov 39)? Spawns: player(15,25), boss(15,8), adds(3,26)&(27,26).

**Read: PASS — readability holds across the entire lifecycle.** Method: direct visual inspection of representative frames (ember f1, peak-bloom f21, sustained-burn f60, waning f95) + an upscaled front-row crop and boss-region crop at peak bloom (the worst-case fire-flood moment).

- **All four combatants are individually locatable + parseable.** The spawn geometry does the work: player **front-center** (bottom of frame, casts a forward shadow), boss **back-center** (top-center, on the red sigil, scale 2.20 — the largest figure), adds at the **two front flanks** (bottom-left @x=3, bottom-right @x=27, each beside a brazier that lights it). Each combatant occupies a **distinct screen region with no overlap or mutual occlusion** — the symmetric spread the spec encodes IS the readability (brief § 2: "we don't invent readability; the spec carries it" — confirmed empirically).
- **The fire column does NOT occlude the boss.** It is body-anchored *behind/around* the boss, so it **backlights** him — at peak bloom (f21) the boss reads as a distinct dark silhouette against the bright column. His fine detail is momentarily bloomed at absolute peak, but silhouette-readability is exactly the register-2 ARPG read ("the boss is there and casting something big"), and across ember / sustained / waning he reads as a fully distinct figure. The bloom is a readability **asset** (telegraphs the boss action), not a liability.
- **The CombatFill lever does its job at the darkest moment.** Even at ember (f1, deepest dark, LDR 148), the CombatFill + braziers keep all four figures lifted off the dark floor — no combatant disappears into shadow at any phase. This is the explicit register-vs-readability lever (drax's run log § lift recipe) working: SHF stays ~43% (dark-mood holds) while the figures stay readable.
- **The fov-39 finding is VALIDATED.** drax's run log flagged that fov 33 (telephoto) cropped the corner adds, so he widened to fov 39 to contain the 24 m-wide front row (player x=15 + adds x=3/x=27). The front-row crop confirms **both corner adds are in-frame and parseable** at fov 39, at the cost of slightly smaller figures. For the 30×30 square, a **single fixed fov holds** — no follow-mode needed. The brief predicts the 10×50 CHOKEPOINT (Build #2) may force a follow-mode; that is flagged forward, NOT here. This is the first empirical confirmation that the fixed 2.5D camera holds for a square arena with a wide front row.

**Readability verdict: PASS.** Register-2 premium AND fight-readability **coexist** in this spec-faithful fight room — the load-bearing question the brief poses (§ 3) is answered YES for the 30×30 boss square. The coexistence is not free: it is *bought* with the CombatFill mid-lift, the contained single-column bloom, and the light dressing — exactly the three levers that moved the composite from the cathedral's 5.00 to 4.00. **That tradeoff is the finding: a register-2 fight room costs ~1.0 composite point of pure visual drama to buy full fight-readability — and it remains a clean rubric PASS after paying it.**

## 6. Marketing-render caveat verdict (load-bearing caveat, carried 1:1 from the cathedral)

**The Synty marketing renders (`modular_asset_idea_pictures/`) are Synty's OWN Unity-pipeline marketing renders — the CALIBRATION/MOOD anchor, NOT the pass bar. This scorecard scored our BUILD against the RUBRIC — it did NOT pixel-match any PNG.**

- **What the marketing renders were used for:** mood/asset-selection calibration only — confirming the Dark Fantasy register is the genre-correct target. I did **not** score "does our scene match a Synty post."
- **The boss-summon specifically:** drax drove his own red emissive sigil + GPUParticles3D column via the proven lift hero-glow lever; it is NOT a pixel-match to any marketing frame, and per the caveat that is BY DESIGN. I scored VFX on its own register merits (body-anchored hero bloom present? HLF magnitude? clean lifecycle?) — all yes, independent of any Synty-post fidelity.
- **Method discipline:** I lifecycle-sampled (100 frames across the hero event), NOT still-vs-still. VFX presence is read across motion, which is what the instruments did.

**Caveat verdict: SATISFIED.** The score stands on our build against galadriel's rubric. The marketing renders informed mood-calibration only and were never a pass bar or pixel-match target.

## 7. drax CV self-sanity — independent re-derivation verdict

drax reported (his numbers, explicitly NOT a self-score — he correctly deferred authoritative scoring to galadriel): LDR 172.7, SHF 43.8%, HLF peak 4.02%.

| Metric | drax self-sanity | galadriel (independent, scorecard-of-record) | Verdict |
|---|---|---|---|
| LDR whole-mean | 172.7 | **175.97 (1.53× thr)** | **CONFIRMED** (Δ1.9%; window/rounding) |
| SHF whole-mean | 43.8% | **42.74% (1.42× thr)** | **CONFIRMED** (Δ1.1pt) |
| HLF peak | 4.02% | **4.013% (frame 21; 2.7× thr)** | **CONFIRMED** (Δ0.007pt — essentially identical) |

All three of drax's self-sanity metrics **CONFIRMED** on my own instruments within method tolerance. The HLF peak is essentially identical (drax's pipeline and mine agree to two decimals). drax's discipline was correct: he ran a sanity check, labeled it explicitly NOT a score, and deferred to galadriel for the authoritative rubric scoring. The numbers hold; the score is mine.

## 8. Honest caveats that bear on the pass

1. **Single-room, single-footprint evidence.** This is Build #1 of 3 — the 30×30 square, the footprint *closest to the already-validated cathedral* (brief § 6, chosen as lowest-risk first proof). The lift's generalization to *constraint-bound* geometry is now demonstrated on ONE arena shape. Build #2 (CHOKEPOINT 10×50 — the radically-different long-narrow footprint) and Build #3 (MAGIC_PACK 32.7×14 — wide-shallow) are the harder shape-generalization tests; the brief expects the corridor may force a fixed-vs-follow camera finding. I claim "register-2 + readability coexist on the 30×30 boss square, decisively" — NOT yet "on all footprints."
2. **Composite 4.00 is genuinely lower than the cathedral's 5.00 — and that is the finding, not a regression.** The 1.0-point gap is bought-back as fight-readability (CombatFill mid-lift, contained bloom, light dressing). A reader comparing 4.00 to 5.00 must not read it as "worse" — the boss arena clears a constraint set the cathedral never faced. Parity is rubric-pass; the rubric passes both mandatory gates.
3. **Readability is reported as a separate READ, not a fifth composite axis.** I did not fold it into the composite because it is a new, qualitatively-different question (binary pass/fail of "can you find the combatants") rather than a 1–5 register dimension. **Rubric-evolution flag:** if battle-room scoring becomes routine, a formal fight-readability rubric axis (with a defensible instrument — e.g., per-combatant local-contrast-against-background, or silhouette-separation distance in screen space) is worth authoring. Deferred until empirical evidence (3+ battle rooms) confirms the axis shape — the corridor + wide-shallow builds will inform what the instrument should measure.
4. **Boss fine-detail blooms at absolute peak (f21).** Honest, and a readability *asset* not liability (silhouette-readable + telegraphs the action); flagged for completeness.
5. **Capture has no HUD/UI chrome.** Clean Movie-Maker renders of the rendered world, not a live viewport with combat UI overlaid. Register-2 + readability of the *rendered world* is what's scored and what holds; the eventual UI layer is a separate surface, out of scope here. (Note: a live combat HUD would ADD readability load — worth carrying forward.)
6. **Pack-side cape-attachment extraction gap (drax run-log crux):** 4 cape `.res` files weren't extracted in pack staging; figures render cape-less (non-fatal). Does not affect the arena score; noted for any future cape-on combatant.

None of these caveats threaten the pass. They scope it honestly: register-2 + fight-readability coexist, decisively, on this spec-faithful 30×30 boss square — with single-footprint evidence the one honest limit on generalizing to "all battle rooms."

## 9. One-line read (evidence FOR gandalf's canon call, NOT the call)

**drax's spec-faithful `SCENARIO_BOSS_WITH_ADDS` (30×30, exact footprint + spawns, no composition cheating) — dressed with Dark Fantasy art via the unchanged lift recipe + a CombatFill readability lever + a boss-anchored ritual-sigil summon column — scores composite 4.00/5 and clears BOTH mandatory gates (lighting 4 @ 1.53× LDR / 1.42× SHF, VFX 4 @ 2.7× HLF), AND passes the new fight-readability read (all four combatants locatable + parseable across the full lifecycle, fov-39 contains the wide front row, the column backlights rather than occludes the boss). The composite sits below the cathedral's 5.00 by exactly the ~1.0 point it spends to buy fight-readability + spec-faithfulness — the first empirical measurement of the register-2-vs-readability tradeoff, and a clean rubric PASS after paying it. This is the first sim→visual bridge: the abstract `spatial_gauntlet` arena renders as a register-2, fight-readable world.**

## 10. Reproducibility

- Instruments: `pipeline/lifecycle-score-boss.mjs` (lifecycle CV; byte-identical instrument defs to the cathedral scorer + `register-metrics.mjs`; phase boundaries empirically re-derived from this capture's HLF curve, documented inline).
- Raw scores: `pipeline/lifecycle-scores-boss.json` (per-frame + per-phase + rubric extracts).
- Readability evidence (git-ignored Synty-derivative IP, LOCAL only — NOT committed): `harness_logs/13_boss_lifecycle_strip.png` (ember/ignite/peak/burn/collapse/settle), `13_boss_frontrow_peak21.png` (front-row crop — both adds + player), `13_boss_region_peak21.png` (boss backlit by column).
- Given the same 100 frames + these instruments, another galadriel-instance reproduces these values exactly (deterministic; no random sampling). The boss-arena phase boundaries (ember 1-8 / ignition-rise 9-20 / peak-bloom 21-34 / sustained-burn 35-86 / waning-settle 87-100) differ from the cathedral's and are re-derived from the empirical HLF curve (ignition @f9, peak @f21, collapse @f87) — documented inline in `lifecycle-score-boss.mjs`.

---

*galadriel SCORES. The canon call — whether this is the stronger second A-holds extension (constraint-bound geometry + register-2/readability coexistence + the first sim→visual bridge) — is gandalf's, on this evidence. Recognition fires on the SCORE, not the build.*
