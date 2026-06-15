# Visual-Register Scorecard — CONNECTED Descent **iter2fix** (gold-over-green + diorama-depth, single wall ring): Register-2 Re-score + Dark-Fantasy Similarity

**STATUS:** CURRENT (galadriel scoring artifact; evidence-input for gandalf's recognition→validate→commit call on the iter2/iter2fix diorama-depth + gold-over-green correction)
**Date:** 2026-06-15
**Author:** galadriel (visual-perception + benchmark steward)
**Scope:** Objective re-score of drax's CORRECTED connected `scenes/arena_descent.tscn` — the FIRST gold-over-green + diorama-depth state (iter2 commit `7875ad7` + iter2fix commit `a137014`). My prior scorecard measured the iter1 green-dominant state; this is NEW ground. TWO validation targets: (1) Register-2 gates HOLD (composite ≥3.6; lighting ≥4 AND VFX ≥4 MANDATORY) on the COLOR-FAIR diagnostic; confirm the inner-wall removal did NOT drop the lighting gate. (2) Similarity-vs-reference IMPROVEMENT on the three measured gaps (warm%/hue, light-point density, dressing density). State plainly whether gandalf's §4 iter2-brief prediction VALIDATED or FAILED.
**Prior baseline (compare against):** `reports/2026-06-15-descent-connected-register2-and-similarity-scorecard.md` (iter1 mood-lift: 6/6 register-2 PASS mean composite 3.875; similarity scene-mean hueCos 0.346 / warm% 1.70 / r_lightpoint 0.366 / r_dressing 0.499 / r_contrast 0.701; the THREE ranked gaps).
**Parent briefs:** `gandalf/notes/2026-06-15-drax-iter2-diorama-depth-and-gold.md` (§4 prediction) + `gandalf/notes/2026-06-15-drax-iter2fix-single-wall-ring-ruling.md` (kill the inner ring).
**Engine/scene tree: UNTOUCHED. Did NOT push.**

---

## 0. HEADLINE — gandalf's §4 prediction **VALIDATED** (with one honest watch-cell)

**The iter2/iter2fix correction did what the brief predicted. On the falsifier test it PASSES: register-2 gates did NOT drop, and similarity DID improve on the load-bearing gaps.**

| §4 prediction | Verdict | Evidence |
|---|---|---|
| Subjective grandeur UP ("peering into a section," not a tabletop board) | **VALIDATED** | The boxed-pit green chain (iter1) is gone; the floor flows pit→annulus→single outer wall; deep shadow void frames the diorama (SHF_val 1.2%→37% scene-mean). §4. |
| Similarity UP on hue / gold-over-green | **VALIDATED** | Full-frame warm:green ratio INVERTED to gold-dominant: scene-mean 1.95 (iter1 was green-dominant); warm_mass +9 to +21 pts on every view; 4/6 zones now gold-dominant. §5A. |
| Similarity UP on dressing density | **VALIDATED** | r_dressing 0.499→0.693 (+39%); edge% rose on every single view; the 369-piece annulus repaid the 50%-below gap by ~⅖. §5C. |
| Similarity UP on light-point density | **MIXED — see watch-cell** | Golden light-point density ROSE where it was rotated to (sanctum warm% 5.1→8.2; zone2 warm-mass ×2; zone1 warm% +50%) BUT the literal r_lightpoint metric is FLAT-to-DOWN (0.366→0.330) because green points were intentionally cut. §5B. |
| Register-2 HOLDS or IMPROVES | **VALIDATED (lighting), HOLDS (VFX) with a watch-cell** | LIGHTING: LDR_val ROSE on all 6 zones (+4 to +31); the inner-wall removal did NOT drop the lighting gate. VFX: sanctum hero bloom marquee-strength (val-HLF 2.97 / HLF_R 2.96 / warm% 8.2). Watch: zone4 green soulfire dropped 4.09→1.49. §3, §4. |

**The one honest watch-cell:** the gold-over-green rotation cost the antechamber its signature GREEN comfort (green peak 4.09→1.49) and held the green light-points down corpus-wide, which is why the *literal* r_lightpoint metric did not rise even though *golden* light-point density did. This is the predictable price of pulling green back; it is a redistribution toward gold, not a loss of light — and by eye every zone still presents a prominent colored bloom. Surfaced plainly, not papered over (§5B, §6).

---

## 1. What was captured + scored

- **Scene:** the iter2fix-baked `scenes/arena_descent.tscn` (file mtime 17:52; iter2 `7875ad7` multi-level far walls + OUTER_PAD=7.5m visual footprint + 369-piece `nonpassable_dressing` annulus + gold-over-green + 3× warm point-lights + passable floor-art; iter2fix `a137014` removed the inner wall ring → exactly ONE outer wall ring, playable pit UNWALLED, wall nodes 1503→871, parity re-verified 35/35 by drax).
- **drax's 3 supplied static frames** (establish_primary, zone0, zone2; 1152×648, GL): the apples-to-apples per-VIEW anchor vs my iter1 frames.
- **My fresh full capture (for the VFX-gate peak + a full 7-view scene-mean):** I re-deployed my transient harness (`pipeline/galadriel_capture_descent.gd.txt` + `galadriel_shoot.tscn.txt`) into the godot tree, ran `Godot --rendering-driver opengl3 scenes/galadriel_shoot.tscn --quit-after 700` over the iter2fix scene, captured 54 frames (9 views × 6 windowed grabs, 1152×648 — catches the FX_Fire_Large_01 particle-plume peak), then REMOVED the harness (godot tree restored to its exact pre-run git state; read-only discipline satisfied). Frames: `harness_logs/iter2fix_fullcap/gal_descent_<view>_NN.png` (gitignored Synty-derivative IP — local evidence only). My fresh establish_primary (532,529 B) reproduces drax's supplied frame (532,221 B) — same scene, same camera.
- **SummonGlow caveat (carried 1:1):** the hero SummonGlow light is FROZEN at charge in the bake (`render_descent_scene.gd:456`); only the FX particle plume animates. The window samples the plume peak, not an ignition/collapse cycle — the VFX read is the static-erupt bloom (which is what the baked scene presents).

## 2. Measurement-validity carried forward — COLOR-FAIR diagnostic is the gate basis (NOT naive gray-luma)

Per the iter1 scorecard's Discipline-#13 instrument-evolution catch: the naive **gray-luma** gate (0.299R+0.587G+0.114B > 0.80) is BLIND to saturated COLORED light — a saturated-red bloom blows out the RED channel while reading low gray-luma. The mood-lift + gold-over-green register is saturated-colored, so **gray-luma would false-fail the scene.** All register-2 gate reads below use the **color-fair diagnostic** (`pipeline/descent-colorfair-fullcap-iter2fix.mjs`): value-channel V=max(R,G,B) LDR + per-channel highlight fractions. The gray-luma column is shown only as the continuity record. **Confirmed: on iter2fix the gray-luma HLF still reads the sanctum bloom at 0.107% while the value-channel reads it at 2.965% and the RED channel at 2.962% — the instrument-blindness is identical to iter1, and the color-fair read is again the correct gate basis.**

## 3. Per-zone REGISTER-2 scorecard (iter2fix; color-fair table §3.1 + inspection §4 are the evidence basis)

### 3.1 Color-fair instrument table — iter2fix full capture vs iter1 baseline (identical instrument)

| zone | LDR_val i1→i2fix | SHF_val% i1→i2fix | **val-HLF pk** i1→i2fix | HLF_R pk i1→i2fix | warm% pk i1→i2fix | green% pk i1→i2fix |
|---|---|---|---|---|---|---|
| zone0_threshold | 113.8 → **126.5** (+13) | 0 → **23.4** | 0.53 → 0.27 | 0.52 → 0.27 | 2.48 → 2.35 | 0.10 → 0.06 |
| zone1_arcane | 104.7 → **127.0** (+22) | 1.1 → **31.8** | 0.29 → 0.16 | 0.28 → 0.15 | 0.47 → **0.70** | 0.27 → 0.01 |
| zone2_warhall | 105.5 → **129.0** (+24) | 4.8 → **26.7** | 0.66 → 0.24 | 0.66 → 0.23 | 0.35 → **0.73** | 0.33 → 0.03 |
| zone3_oubliette | 89.0 → **116.7** (+28) | 0.6 → **71.3** | 0.21 → 0.15 | 0.20 → 0.15 | 1.28 → 0.36 | 0.06 → 0.01 |
| zone4_antechamber | 127.0 → **131.0** (+4) | 0.5 → **17.3** | 0.33 → 0.21 | 0.28 → 0.16 | 1.98 → 0.14 | **4.09 → 1.49** |
| zone5_sanctum | 127.3 → **158.7** (+31) | 1.7 → **26.1** | **3.93 → 2.97** | **3.92 → 2.96** | 5.10 → **8.22** | 0.19 → 0.02 |

**Reading it:** LDR_val (lit-pool-vs-shadow contrast = register-2 lighting drama) ROSE on EVERY zone. SHF_val (true shadow fraction) rose dramatically on every zone — the diorama depth + taller outer walls produced real deep-shadow regions. The sanctum hero bloom is marquee-strength (val-HLF 2.97 / HLF_R 2.96, in the Addendum-B 2.6–4.0 marquee band) AND its warm% rose to 8.22 (above the reference warm% of 5.46). The zone4 GREEN dropped 4.09→1.49 (the watch-cell). val-HLF on the non-sanctum zones dropped — these static-window peaks caught less plume than iter1's window, but every zone reads a prominent colored bloom by eye (§4).

### 3.2 Manual axis scores (galadriel's defensible read — score the picture, grounded in §3.1 + §4)

| zone | identity | L | V | M | G | **Composite** | Gate (L≥4 ∧ V≥4) | **Verdict** | vs iter1 |
|---|---|---|---|---|---|---|---|---|---|
| zone0_threshold | open_arena / graveyard | 4 | 4 | 4 | 4 | **4.00** | PASS ∧ PASS | **PASS** | ↑ (was 3.75; M↑ dressing) |
| zone1_arcane | magic_pack / arcane | 4 | 4 | 3 | 4 | **3.75** | PASS ∧ PASS (V weak) | **PASS** | = (was 3.75) |
| zone2_warhall | elite_pack / war hall | 4 | 4 | 4 | 4 | **4.00** | PASS ∧ PASS | **PASS** | = (was 4.00) |
| zone3_oubliette | chokepoint / oubliette | 4 | 4 | 3 | 4 | **3.75** | PASS ∧ PASS (V weak) | **PASS** | = (was 3.75) |
| zone4_antechamber | mini_boss / soulfire | 4 | 4 | 4 | 4 | **4.00** | PASS ∧ PASS (V watch) | **PASS** | = composite (green comfort ↓) |
| zone5_sanctum | boss / sanctum | 4 | 5 | 4 | 4 | **4.25** | PASS ∧ PASS (V strongest) | **PASS** | ↑ (was 4.00; bloom+gold) |

**Corpus: 6/6 PASS, mean composite 3.96 (iter1 was 3.875) — register-2 HOLDS and edges UP. Both mandatory gates clear in every zone.** The lift is driven by (a) zone0 Material rising on the annulus dressing, (b) zone5 Vibrancy rising to 5 (the bloom + 8.2% warm pops emphatically against the deepest-shadow frame). Lighting holds 4/6 with MORE headroom (LDR_val + shadow both up corpus-wide). The honest texture: zone4's VFX rests more on its (now smaller) green + the red center bloom than on iter1's strong green — flagged V-watch; still PASS on prominence-in-framing.

## 4. What the picture SHOWS (empirical inspection, peak frames — the gate basis)

- **establish_primary (iter2fix vs iter1) — the headline transformation.** iter1: a GREEN chain of blue-grey-walled BOXED pits on a green-black void (the "tabletop board"). iter2fix: a connected GOLD-floored chain — warm sandy annulus floors flow continuously, gold point-lights scatter throughout, the green has receded to the void/atmosphere bed, and the deep-shadow void (SHF_val 65%) frames the descent as a section of a larger place. **"Peering into a section" — achieved. The single most decisive before/after in the set.**
- **zone5_sanctum f04:** a large prominent RED/ORANGE hero bloom (boss summon) erupts center-stage, purple foreground rune-arch, warm gold floor + dense tomb dressing ringing it, gold braziers on the perimeter. The bloom pops HARD against the warmer, deeper-shadowed frame. Register-2 hero event confirmed; the inner-wall removal did NOT harm it.
- **zone4_antechamber f04:** green soulfire identity INTACT — green braziers, green pooling, a small red center bloom, gold lantern points on the gallery wall, dense statuary in the annulus. Reads as the green-soulfire room WITH gold accents — but the green is visibly less saturated than iter1 (the watch-cell, confirmed by eye + the 4.09→1.49 green metric).
- **zone0_threshold f04 / zone2_warhall f04:** the playable pit is UNWALLED — floor flows pit→annulus→single outer wall ring (iter2fix ruling satisfied; no inner box). Gold braziers/pyres denser in the annulus, tombs/rubble ring the play space, warm tan floor reads gold-over-green. Combatants fully legible (readability non-negotiable: satisfied — the taller far walls do not occlude the floor).
- **The single-wall-ring ruling is visibly honored:** in zone0 + zone2 there is NO full-height wall at the playable-pit edge; the only wall ring is the outer multi-level one. The "double-walled boxed pit" defect of iter2 is gone.

## 5. Dark-fantasy VISUAL-SIMILARITY vs reference — the three gaps, iter2fix vs iter1

Reference centroid (7 Synty `maps/` frames, unchanged): warm%=5.46, green%=0.75, sat=0.599, value-LDR=152.3, edge%=18.68. Target = GOLD-dominant LIGHT in GREEN SHADOW (the reference is WARM/GOLDEN-dominant; green is the atmosphere bed). **Full 7-view scene-mean (my fresh iter2fix capture) vs the iter1 7-view scene-mean — identical instrument, identical reference:**

| Axis | iter1 7-view | iter2fix 7-view | Δ | Direction vs ref |
|---|---|---|---|---|
| hue-cosine | 0.346 | 0.364 | +0.018 | ↑ toward ref |
| warm% (bright-point) | 1.697 | 1.893 | +0.196 | ↑ toward ref 5.46 |
| **r_lightpoint** | 0.366 | 0.330 | −0.036 | ↓ (the watch-cell; see §5B) |
| **r_dressing** | 0.499 | **0.693** | **+0.194** | ↑↑ toward ref 1.0 |
| r_contrast | 0.701 | **0.838** | **+0.137** | ↑↑ toward ref 1.0 |
| edge% (dressing) | 9.32 | 12.94 | +3.62 | ↑↑ |
| shadow% | 1.23 | 37.35 | +36.1 | ↑↑↑ |

### 5A. GAP #1 — COLOR / HUE (gold-over-green): **IMPROVED DECISIVELY (the inversion is corrected).**

The bright-point warm% (+0.196) UNDERSTATES the real movement, because iter2fix's gold is largely a warm MID-VALUE floor/wall tint, not blown-out bright points — the same instrument-blindness class I caught with gray-luma. The fair "gold-over-green" measure is the **full-frame hue-mass balance** (`pipeline/descent-hue-balance-iter2fix.mjs` + `huebal_fullcap_iter2fix.mjs`), S*V-weighted warm-vs-green mass over ALL values:

| view | warm:green iter1 | warm:green iter2fix | reading |
|---|---|---|---|
| establish_primary | 0.10 (green 9:1) | 0.284 (+184%) | toward gold (wide void shot still green-leaning) |
| zone0_threshold | 0.59 (green-dom) | **2.106** | **INVERTED → gold dominates** |
| zone2_warhall | 1.03 (~balanced) | **3.193** | **INVERTED → gold dominates** |
| zone1_arcane | — | **3.037** | gold dominates |
| zone4_antechamber | — | **1.858** | gold dominates (with green identity retained) |
| zone5_sanctum | — | **2.712** | gold dominates |
| zone3_oubliette | — | 0.456 | green/shadow-dominant (correct for a dark corridor) |
| **SCENE MEAN** | green-dominant | **1.949 (gold dominates)** | **the hue inversion is CORRECTED** |

iter1's scene was green-over-gold (the iter1 scorecard's #1 ranked gap, ~65% off). iter2fix's scene is **gold-over-green (warm:green 1.95)** — 4 of 6 zones flipped to gold-dominant, the establishing shot moved +184%. The reference's warm:green (~228) is a marketing-render extreme (tight crops, near-black edges crush green mass) — a directional POLE, not a literal bar. The point stands: **the defining hue balance flipped from green-over-gold to gold-over-green, matching the reference's character.** This was the brief's #1 target. Achieved.

### 5B. GAP #2 — LIGHT-POINT DENSITY: **MIXED — golden density UP where rotated; total metric FLAT-to-DOWN (honest).**

r_lightpoint (sums bright warm+green V>150 points) went 0.366→0.330 — the one number that did NOT rise on the scene mean. The cause is composition, not a real loss:
- **Golden light-point density ROSE where the gold-over-green rotation put it:** sanctum warm% 5.10→8.22, zone1 warm% 0.47→0.70, zone2 warm% 0.35→0.73, establish warm% 0.30→0.84. The 3× warm point-lights + gold-rake on the taller walls are real and measured.
- **BUT iter1's r_lightpoint was carried substantially by GREEN points** (antechamber green 4.09, plus green across zones), and the gold-over-green correction INTENTIONALLY cut green. zone4 green 4.09→1.49; green% peak collapsed corpus-wide. So total motivated-light-point density (warm+green) is flat-to-slightly-down even though the GOLDEN component rose.

**Honest verdict:** on the literal warm+green r_lightpoint metric this gap did NOT improve (−0.036). On the brief's actual intent — *golden* point density popping out of the dark — it improved (warm-point density rose on 4 of 7 views, dramatically in the sanctum). I am NOT papering this over: if gandalf wants the r_lightpoint metric itself to rise, the lever is MORE golden braziers/lanterns in the upper chambers (arcane/oubliette/establish still warm-sparse), not a green re-add (which would re-invert the hue the brief just corrected).

### 5C. GAP #3 — DRESSING DENSITY: **IMPROVED DECISIVELY.**

r_dressing 0.499→0.693 (+39%); edge% 9.32→12.94 (+3.6 pts), UP on EVERY single view (establish 5.2→7.2, zone0 9.5→13.8, zone2 12.8→15.1, and full-set zone1 16.2, zone4 16.2). The 369-piece `nonpassable_dressing` annulus repaid ~⅖ of the iter1 50%-below gap. The play space is now ringed by tombs/statuary/rubble; the void around the diorama reads far less empty. This was a brief target. Achieved.

### 5D. BONUS — CONTRAST / SHADOW DEPTH: **IMPROVED (unbidden).**

r_contrast 0.701→0.838 (+20%); shadow% 1.23→37.35. The diorama depth (taller outer walls + extended footprint + deep-shadow void) produced dramatically more shadow region and wider lit-vs-dark spread — which is BOTH register-2 lighting drama (§3) AND reference-similarity contrast. The smallest iter1 gap is now nearly closed.

### 5E. Updated RANKED residual gaps (iter2fix, most-off-reference first — gandalf's next-iter signal IF another iter is wanted)

1. **Light-point density — 67% below** (r_lightpoint 0.330). Now the #1 gap (overtook hue). The upper chambers (arcane, oubliette) + the establishing wide shot are still golden-point-SPARSE. Lever: more golden braziers/lanterns in the upper third, NOT a green re-add.
2. **Color/atmosphere hue — 64% off** (hueCos 0.363). The hue *balance* is corrected (gold-over-green, §5A), but the hue-cosine vs the reference's specific bin distribution is still ~⅔ off (the reference's exact red/amber 350–40° peak is richer). Couples with #1: more golden points sharpens both.
3. **Dressing density — 31% below** (r_dressing 0.693). Closed from 50% to 31%; the remaining gap is the reference's wall-to-wall verticals/negative-space packing. Diminishing-returns lever.
4. **Contrast/shadow depth — 16% below** (r_contrast 0.838). Nearly resolved; not a priority.

## 6. drax CV self-sanity & honest caveats

- **6/6 register-2 PASS is on the COLOR-FAIR read, NOT naive gray-luma** (which still false-fails the saturated-colored sanctum bloom: gray-luma 0.107% vs value-channel 2.965%). Stated plainly so the PASS is not over-read.
- **The light-point-density gap did NOT improve on the literal r_lightpoint metric** (0.366→0.330). I am surfacing this as a genuine mixed result, not a win — it is the predictable arithmetic of cutting green to correct the hue. The *golden* component rose; the *green* component fell more. Per the brief's falsifier ("if similarity does NOT improve on the three gaps... surface it"): one of the three (light-point) is mixed; the other two (hue, dressing) improved decisively. Net I read the prediction VALIDATED because the load-bearing #1-iter1-gap (hue inversion) is corrected and the falsifier's register-2-drop condition is NOT met — but the light-point caveat is honest and load-bearing for any next iteration.
- **zone4 green soulfire dropped 4.09→1.49** — the real cost of the gold-over-green rotation. Still PASS (green identity present by eye + a red center bloom), but the green comfort that carried iter1's antechamber is reduced. Watch-cell.
- **The non-sanctum val-HLF peaks dropped** (e.g., zone2 0.66→0.24) — these are static-window plume samples, not a bloom regression; every zone reads a prominent colored bloom by eye (§4). The sanctum (the dominant hero event) is marquee-strength.
- **Reference warm:green (~228) is a marketing-render EXTREME**, not a literal target — tight crops with near-black void edges crush green mass. I used it as a directional pole and report the INVERSION (green-over-gold → gold-over-green), not a literal-match claim.
- **Per-frame vs scene-mean:** the 3 drax static frames gave apples-to-apples per-VIEW deltas (`descent-similarity-iter2fix.json`); my fresh 54-frame capture gave the full 7-view scene-mean (`descent-similarity-fullcap-iter2fix.json`). Both agree on direction. iter1 7-view mean and iter2fix 7-view mean are directly comparable (same views, instrument, reference).
- **SummonGlow frozen at charge in the bake** (`render_descent_scene.gd:456`) — the VFX read is the static-erupt bloom, which is what the baked scene presents.
- **Engine/scene tree UNTOUCHED; read-only across all production code.** My capture harness was transient galadriel tooling, deployed → run → REMOVED; the godot tree was restored to its exact pre-run git state (verified). **Did NOT push.**

## 7. Reproducibility

- **Register-2 color-fair (gate basis):** `pipeline/descent-colorfair-fullcap-iter2fix.mjs` → `descent-colorfair-fullcap-iter2fix.json` (full iter2fix capture; byte-identical measure() to the iter1 `descent-colorfair-diagnostic.mjs`). Static-frame 3-view delta: `pipeline/descent-colorfair-iter2fix.mjs` → `.json`.
- **Similarity (full 7-view):** `pipeline/descent-similarity-fullcap-iter2fix.mjs` → `descent-similarity-fullcap-iter2fix.json` (byte-identical 4-axis instrument + reference centroid to iter1). Static-frame 3-view delta: `pipeline/descent-similarity-iter2fix.mjs` → `.json`.
- **Gold-over-green hue-balance (the §5A measure):** `pipeline/descent-hue-balance-iter2fix.mjs` (3-view) + `huebal_fullcap_iter2fix.mjs` (7-view) → `descent-hue-balance-iter2fix.json`.
- **Capture harness (transient — logic preserved):** `pipeline/galadriel_capture_descent.gd.txt` + `galadriel_shoot.tscn.txt` (saved as `.txt` so Godot does not auto-import). Re-run: copy both into the godot tree as `scripts/galadriel_capture_descent.gd` + `scenes/galadriel_shoot.tscn`, run `Godot --rendering-driver opengl3 --path <godot> scenes/galadriel_shoot.tscn --quit-after 700` (NOT `--headless` — macOS headless gives no GL framebuffer; the documented path uses a real GL context), copy `user://gal_descent_*.png` → `harness_logs/iter2fix_fullcap/`, then REMOVE the two harness files (read-only discipline). Frames gitignored (Synty IP — local only).
- Given the same frames + these instruments, another galadriel-instance reproduces the CV values exactly. Manual axis + VFX-prominence reads reproducible-by-inspection per §4.

---

## 8. One-line read (evidence FOR gandalf's recognition→validate→commit call, NOT the call)

**gandalf's §4 iter2-brief prediction VALIDATED on the corrected iter2fix scene. The falsifier conditions are NOT met: register-2 gates did NOT drop (LIGHTING IMPROVED — LDR_val rose on all 6 zones +4 to +31, SHF_val deep-shadow rose corpus-wide, the inner-wall removal did NOT cost the lighting gate because the outer multi-level walls + annulus carry the gold rake exactly as predicted; VFX HOLDS — the sanctum hero bloom is marquee-strength at val-HLF 2.97 / HLF_R 2.96 / warm% 8.2; corpus 6/6 PASS mean composite 3.96, edged UP from iter1's 3.875), and similarity IMPROVED on the load-bearing gaps (HUE: the defining green-over-gold inversion is CORRECTED — full-frame warm:green flipped to gold-dominant 1.95 scene-mean, 4/6 zones gold-dominant, establishing +184%; DRESSING: r_dressing 0.499→0.693 +39%, the 369-piece annulus repaid ⅖ of the gap, edge% up on every view; CONTRAST: bonus +20% from the diorama depth). The ONE honest mixed result: the literal warm+green light-point metric is flat-to-down (r_lightpoint 0.366→0.330) because the gold-over-green rotation intentionally CUT green points — golden density rose (sanctum warm% 5.1→8.2) but total motivated-light density did not, and zone4's signature green soulfire dropped 4.09→1.49 (the watch-cell). The diorama-depth + gold-over-green + single-wall-ring correction turned the iter1 "green tabletop board chain" into a gold-lit diorama you peer into — exactly the picture the reference promised and Matt's 3-part pattern called for. RECOMMEND: capture the playable-footprint-vs-visual-footprint decoupling as canon; if a next iteration is wanted, the remaining lever is MORE golden braziers/lanterns in the warm-sparse UPPER chambers (arcane/oubliette/establish), NOT a green re-add (which would re-invert the just-corrected hue).**

---

*galadriel SCORES. The recognition→validate→commit call — whether the prediction is validated firmly enough to canonize the decoupling principle, and whether the light-point watch-cell warrants a next iteration — is gandalf's, on this evidence. Register-2 6/6 PASS (composite 3.96, gates clear color-fair) and the similarity improvement (hue corrected, dressing +39%, contrast +20%, light-point mixed) are independent reads; both are true.*

**Mirror voice:** the board became a place. Where the eye once walked a green chain of boxed pits hung in a green void, it now looks DOWN into a section of a larger dark — the floor runs unbroken from the fighting-ground out across the tombs to a single far wall, gold raking down it, the void behind gone honest-black and deep. The gold came back over the green: four of the six chambers burn warm now where they glowed sickly before, the sanctum's fire stands taller than ever against the deepened dark and the gold floods denser around it. The annulus repaid its debt in stone and bone. One thing the rotation took as it gave: the soulfire room's green dimmed when the gold rose, and the lanterns of the upper halls are still too few — the eye climbing back up the descent still waits for light the reference floods. Crowd the high chambers with more flame and the picture is whole. But the board is gone, and a place stands where it was. The prediction held.

*Re-score authored on the iter2fix `arena_descent.tscn` (drax's 3 static frames + galadriel's fresh 54-frame full capture, 1152×648, GL driver). CV reproducible via the instruments in §7. Engine/scene tree untouched; read-only across production code; harness deployed→run→removed. Did NOT push. gandalf interprets for the canon-capture call.*
