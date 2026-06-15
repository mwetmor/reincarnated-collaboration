# Visual-Register Scorecard — CONNECTED Descent **iter3** (transparency walls + organic life + golden top-up): Register-2 Re-score + Dark-Fantasy Similarity

**STATUS:** CURRENT (galadriel scoring artifact; evidence-input for gandalf's recognition→validate→commit call on iter3 — whether to move the `battle-room-presentation-decoupling-2026-06-15.md` Layer-3 status from "pending" to "validated").
**Date:** 2026-06-15
**Author:** galadriel (visual-perception + benchmark steward)
**Scope:** Objective re-score of drax's iter3 connected `scenes/arena_descent.tscn` (Change A camera-relative transparency walls; Change B organic life — gothic arches/columns/moss/vines + low passable floor-foliage; Change C golden-point top-up in warm-sparse upper chambers). iter2fix is the validated baseline (register-2 6/6, mean composite 3.96, gold-over-green inverted to gold-dominant 1.95, dressing +39%). This is the THIRD pass on the WS2 connected-descent thread (iter1 → iter2fix → iter3); I scored all three.
**Prior baseline (compare against):** `reports/2026-06-15-descent-iter2fix-register2-and-similarity-rescore.md` (iter2fix: 6/6 register-2 PASS, mean composite 3.96; scene-mean hueCos 0.364 / warm% 1.89 / r_lightpoint 0.330 [the carried watch-cell] / r_dressing 0.693 / r_contrast 0.838; gold-over-green warm:green 1.95 scene-mean).
**Parent brief:** `gandalf/notes/2026-06-15-drax-iter3-transparency-walls-and-organic-life.md` (Changes A/B/C + §5 prediction + §5 falsifier).
**Reference target:** Synty `polygon-dark-fantasy-01/modular_asset_idea_pictures/` image #61 (gold-lit gothic crypt; arches/columns; heavy moss/vines). Operational reference centroid = the 7 `maps/` frames (same instrument I validated iter2fix against — apples-to-apples).
**Engine/scene tree: UNTOUCHED. Did NOT push.**

---

## 0. HEADLINE — TOP-LINE VERDICT PER AXIS

| Axis | Verdict | One-line evidence |
|---|---|---|
| **Register-2 (PRIMARY GATE)** | **HOLD** (edges down 0.01 in composite; gates intact 6/6) | 6/6 PASS; lighting ≥4 AND VFX ≥4 every zone; mean composite 3.96→**3.94** (within noise; sanctum bloom intact 2.94/2.94, lighting holds corpus-wide). |
| **Similarity — dressing density** | **IMPROVE** | r_dressing 0.693→**0.853** (+23%); gap to ref closed 31%→15%; edge% +2.99. The 688 organic pieces repaid more of the gap. |
| **Watch-cell A — r_lightpoint recovery** | **IMPROVE (RECOVERED)** | r_lightpoint 0.330→**0.384**, now ABOVE iter1's 0.366 — recovered via GOLD (warm% +0.33, green% flat +0.01), NOT a green re-add. Exactly as gandalf predicted. |
| **Watch-cell B — gold-dominant HELD?** | **HOLD (but compressed — gandalf's eye is RIGHT)** | warm:green scene-mean stayed gold-dominant **1.465** (>1.0); 5/7 views gold-dominant; every near-chamber view that was gold-dominant in iter2fix STAYED gold-dominant. BUT it compressed 1.95→1.47 (−25% toward parity) — the cooled floor bed is real. Inversion HELD; did NOT regress past the line. |
| **Transparency readability (Change-A acceptance)** | **PASS (clean, all angles)** | Across the diagonal spine shot + all 6 per-zone top-downs (which fade DIFFERENT walls of the same rooms): playable floor + combatants CLEAN, no wrong-walls-larger, no ambiguous faded-wall edges. The four-sided-uniform + camera-fade works from every angle. |

**Net: iter3 SHIPS on the falsifier test.** None of the three kill-conditions fired — transparency did NOT hurt readability; register-2 did NOT drop below gates; the gold-dominant inversion did NOT regress past the inversion line. Two honest textures gandalf must weigh: (1) the floor BED reads measurably cooler (Watch-cell B compressed 1.95→1.47 — the price of adding the fourth, camera-side, full-height wall), and (2) oubliette warm% dipped (0.36→0.13 — the top-up went to arcane/threshold/establish more than the corridor). Neither breaks a gate; both are surfaced plainly, not papered over.

---

## 1. What was captured + scored

- **Scene:** the iter3-baked `scenes/arena_descent.tscn` (file mtime 18:23; wall-ish nodes 871→**1345** confirming Change A uniform full-height + faded camera-side wall; dressing markers → **1064** confirming Change B's 688 organic pieces; **2659 alpha/fade/ShaderMaterial markers** confirming Change A's camera-relative alpha-fade shader is present and pervasive). Parity harness-verified 35/35 by drax (I did NOT re-run parity — it is not my seam and was already confirmed; per the brief I focus falsifier attention on readability + register-2 + warm% hold).
- **drax's 9 supplied static iter3 frames** (`harness_logs/descent_iter3_*.png`): the multi-angle transparency-readability anchor (establish ×3 + zone0–zone5). I inspected ALL 9 by eye.
- **My fresh full capture (for the register-2 VFX-gate peak + full 7-view scene-mean):** I re-deployed my transient harness (`pipeline/galadriel_capture_descent.gd.txt` + `galadriel_shoot.tscn.txt`) into the godot tree, ran `Godot --rendering-driver opengl3 --path . scenes/galadriel_shoot.tscn --quit-after 700` over the iter3 scene, captured 54 frames (9 views × 6 windowed grabs, 1152×648 — catches the FX_Fire_Large_01 particle-plume peak), then REMOVED the harness (godot tree restored to exact pre-run git state; read-only discipline satisfied + verified: `arena_descent.tscn` shows NO galadriel modification). Frames: `harness_logs/iter3_fullcap/gal_descent_<view>_NN.png` (gitignored Synty-derivative IP — local evidence only).
- **Instrument note:** I cloned my three iter2fix instruments to iter3 by changing ONLY the source dir + output filename (`diff` confirmed: measure() byte-identical). Same views, same resolution, same reference centroid, same metrics → exact apples-to-apples vs iter2fix.
- **SummonGlow caveat (carried 1:1):** the hero SummonGlow light is FROZEN at charge in the bake (`render_descent_scene.gd:456`); only the FX particle plume animates. The window samples the plume peak — the VFX read is the static-erupt bloom (which is what the baked scene presents). Sanctum hero bloom untouched by iter3 per brief.

## 2. Measurement-validity carried forward — COLOR-FAIR diagnostic is the gate basis (NOT naive gray-luma)

Per the iter1/iter2fix Discipline-#13 instrument catch: naive **gray-luma** (0.299R+0.587G+0.114B>0.80) is BLIND to saturated COLORED light — a saturated-red bloom blows the RED channel while reading low gray-luma, so gray-luma would false-FAIL the saturated-colored register. All register-2 gate reads below use the **color-fair diagnostic** (value-channel V=max(R,G,B) LDR + per-channel highlight fractions). **Confirmed on iter3: the sanctum bloom reads gray-luma HLF 0.076% but value-channel HLF 2.939% / RED channel 2.937% — the instrument-blindness is identical to iter1/iter2fix; the color-fair read is again the correct gate basis.** Watch-cell B (warm% hold) uses the COLOR-FAIR per-channel diagnostic + the full-frame S\*V-weighted hue-mass balance, NOT naive gray-luma — per the brief's explicit instruction.

## 3. Per-zone REGISTER-2 scorecard (iter3 vs iter2fix)

### 3.1 Color-fair instrument table — iter3 full capture vs iter2fix baseline (identical instrument)

| zone | LDR_val i2fix→i3 | **HLF_val pk** i2fix→i3 | HLF_R pk i3 | warm% pk i2fix→i3 | green% pk i2fix→i3 |
|---|---|---|---|---|---|
| zone0_threshold | 126.5 → **142.5** (+16) | 0.27 → **0.59** | 0.583 | 2.35 → **4.91** | 0.057 → 0.095 |
| zone1_arcane | 127.0 → **128.2** (+1) | 0.157 → **0.317** | 0.312 | 0.70 → **0.91** | 0.009 → 0.032 |
| zone2_warhall | 129.0 → 127.0 (−2) | 0.238 → **0.333** | 0.324 | 0.73 → 0.34 | 0.034 → 0.083 |
| zone3_oubliette | 116.7 → 115.0 (−1.7) | 0.152 → 0.125 | 0.124 | 0.36 → **0.13** | 0.009 → 0.032 |
| zone4_antechamber | 131.0 → 131.0 (flat) | 0.205 → **0.242** | 0.157 | 0.137 → **0.356** | 1.489 → **1.543** |
| zone5_sanctum | 158.7 → 157.7 (−1) | **2.965 → 2.939** | **2.937** | **8.215 → 8.211** | 0.022 → 0.021 |

**Reading it:**
- **LDR_val (lit-pool-vs-shadow contrast = register-2 lighting drama) HOLDS corpus-wide.** zone0 jumped +16 (the threshold gold top-up + dense dressing reads as brighter-lit). The other five are within ±2 of iter2fix — flat, no zone dropped meaningfully. The four-sided uniform walls + camera-fade did NOT cost the lighting gate (faded walls still cast/receive light, and fading the camera-near wall lets brazier glow through — net-neutral-to-positive as the brief predicted).
- **VFX (HLF_val peak):** sanctum **2.939** (was 2.965 — held, marquee-strength, Addendum-B 2.6–4.0 band; HLF_R 2.937 confirms it's the red/amber bloom). Non-sanctum HLF_val ROSE on 4/6 (zone0 +0.32, zone1 +0.16, zone2 +0.10, zone4 +0.04) — the golden top-up added bloom-prominence. zone3 flat. **No VFX regression.**
- **zone4 antechamber GREEN HELD** (1.489 → 1.543, slightly UP) — Change C did NOT touch antechamber green (per brief), and it's confirmed intact. This recovers the iter2fix watch where green had dropped to 1.49 — it did not drop further.
- **Honest dip:** oubliette warm% 0.36→0.13. The golden top-up favored arcane/threshold/establish over the dark corridor; oubliette is now SLIGHTLY warm-sparser than iter2fix at peak. Does not break a gate (it's a dark corridor by design), but it's the one zone where the top-up did not land — flagged.

### 3.2 Manual axis scores (galadriel's defensible read — score the picture, grounded in §3.1 + §4)

| zone | identity | L | V | M | G | **Composite** | Gate (L≥4 ∧ V≥4) | **Verdict** | vs iter2fix |
|---|---|---|---|---|---|---|---|---|---|
| zone0_threshold | open_arena / graveyard | 4 | 4 | 5 | 4 | **4.25** | PASS ∧ PASS | **PASS** | ↑ (was 4.00; M↑ columns+arches, warm% +16, gold top-up) |
| zone1_arcane | magic_pack / arcane | 4 | 4 | 4 | 4 | **4.00** | PASS ∧ PASS | **PASS** | ↑ (was 3.75; the prior readability-failure case is now CLEAN, M↑ organic, warm% recovered) |
| zone2_warhall | elite_pack / war hall | 4 | 4 | 4 | 4 | **4.00** | PASS ∧ PASS | **PASS** | = (was 4.00) |
| zone3_oubliette | chokepoint / oubliette | 4 | 4 | 4 | 3 | **3.75** | PASS ∧ PASS | **PASS** | = composite (M↑ dense columns; G watch — warm% dipped 0.36→0.13) |
| zone4_antechamber | mini_boss / soulfire | 4 | 4 | 4 | 4 | **4.00** | PASS ∧ PASS | **PASS** | = (was 4.00; green soulfire HELD 1.49→1.54, gold lanterns added) |
| zone5_sanctum | boss / sanctum | 4 | 5 | 4 | 4 | **4.25** | PASS ∧ PASS | **PASS** | = (was 4.25; bloom untouched, marquee-strength held) |

**Corpus: 6/6 PASS, mean composite 3.96 → 3.94 (within scoring noise; effectively HOLD). Both mandatory gates clear in every zone (lighting ≥4 AND VFX ≥4, color-fair).** The texture: zone0 and zone1 IMPROVED (zone0 on the gold+organic; zone1 because the prior arcane readability-failure case is now clean AND it got organic dressing + warm-point recovery), offsetting a marginal softening elsewhere. I score the corpus HOLD, not IMPROVE — the composite did not move up net, because the floor-bed cooling (Watch-cell B) holds Vibrancy flat where the gold top-up alone might have raised it, and oubliette's warm dip caps its Glow at 3. Honest, not inflated.

## 4. What the picture SHOWS (empirical inspection, peak frames — the gate + readability basis)

**Transparency readability (Change-A acceptance — the load-bearing readability question):**
- **establish (diagonal spine shot, ×3 near-identical frames):** every one of the 6 chambers is visible INTO from the diagonal — no chamber is occluded by a near wall. The faded near-walls show their blue-grey stone (faded, not absent) and you see past them to the floor + dressing + lights behind. **No wrong-walls-larger** — the old per-camera-height defect (where the wrong two walls were tall for a given angle) is gone; uniform-tall + camera-fade resolves it. Clean.
- **Per-zone top-downs (zone0–zone5):** each fades DIFFERENT walls of its room (the camera-near walls for that specific top-down angle). In EVERY one the playable floor is fully legible, combatants (the yellow/green figures) are unambiguous, and the faded-wall edges are smooth (alpha-fade, not hard dither — screenshot-clean as the brief recommended). **zone1_arcane — the prior readability-FAILURE case — is now CLEAN:** full floor visible, green arcane pooling legible, combatants clear, gothic arches framing the top. The whole point of Change A is satisfied: NO angle shows wrong-walls-larger or an occluded/ambiguous floor.
- **The fourth wall is now present + faded:** in the per-zone top-downs the camera-side wall (left open in iter2fix) is now a full-height wall that fades for the camera — the rooms read as fully-enclosed castle sections you look down INTO, not three-walled stages. This is the grandeur gain the brief predicted (all walls full-height).

**Organic life (Change B):**
- Columns, gothic arches (pointed/traceried), and vine-columns ring the annulus of every chamber — visible in zone0/zone1/zone2/zone4 top-downs as dense vertical clutter at the room perimeters. The dressing reads markedly denser than iter2fix's tomb-and-rubble ring; the "clean geometry" feel is gone, replaced by an overgrown reclaimed-crypt feel.
- Low passable foliage (ferns/grass/moss decals) is visible on the playable floors (small green specks distributed across the floor in the top-downs) — floor-art, does not occlude combatants.

**Lighting / VFX:**
- **zone5_sanctum:** the RED/ORANGE hero bloom (boss summon, FX_Fire_Large_01 + SummonGlow ×6) erupts center-stage HARD — marquee-strength, untouched. Purple foreground rune-arch, gold braziers ringing the perimeter, combatants legible around the bloom. The transparency did NOT harm the hero event.
- **zone4_antechamber:** green soulfire identity STRONG — vivid green braziers/pooling on the side walls, green wall-glow, plus the red center bloom (mini-boss) and gold lanterns on the upper gallery. Reads green-AND-gold; the green comfort is back (1.54 vs iter2fix's 1.49).
- **zone3_oubliette:** narrow corridor — transparency shows down the full corridor length, combatants legible, gold lanterns/torches down its length (Change C top-up present), dense columns/arches lining the walls. Floor cool-dark (correct for a dark corridor).

**The floor-bed cooling (Watch-cell B — gandalf's eye-flag, confirmed):**
- Across the near-chamber top-downs (zone0/zone1/zone2) the playable FLOOR BED reads distinctly cooler/greyer than iter2fix's warm-tan. Gold is now carried by POINT-SOURCES (corner braziers/pyres, lanterns, warm rim-light on dressing) rather than a warm floor wash. gandalf's eye is correct: the floor is cooler. The §5/§3.1 instruments confirm WHY (next section) and confirm it did NOT cross the inversion line.

## 5. Watch-cell resolutions + dark-fantasy similarity

Reference centroid (7 Synty `maps/` frames, unchanged): warm%=5.46, green%=0.75, sat=0.599, value-LDR=152.3, shadow%=14.62, edge%=18.68. Target = GOLD-dominant LIGHT in GREEN SHADOW. **Full 7-view scene-mean (fresh iter3 capture) vs iter2fix 7-view scene-mean — identical instrument, identical reference:**

| Axis | iter1 | iter2fix | **iter3** | Δ vs iter2fix | Direction vs ref |
|---|---|---|---|---|---|
| hue-cosine | 0.346 | 0.364 | **0.401** | +0.037 | ↑ toward ref |
| warm% (bright-point) | 1.697 | 1.893 | **2.220** | +0.327 | ↑ toward ref 5.46 |
| **r_lightpoint** (Watch-cell A) | 0.366 | 0.330 | **0.384** | **+0.054** | ↑ RECOVERED above iter1 |
| **r_dressing** | 0.499 | 0.693 | **0.853** | **+0.160** | ↑↑ toward ref 1.0 |
| r_contrast | 0.701 | 0.838 | 0.846 | +0.008 | ↑ (held) |
| edge% (dressing) | 9.32 | 12.94 | **15.93** | +2.99 | ↑↑ |
| shadow% | 1.23 | 37.35 | 34.32 | −3.03 | ↓ slightly (dressing+gold+walls fill some void; still ≫ iter1) |
| green% (bright-point) | — | 0.153 | 0.165 | +0.012 | flat (NO green re-add — confirmed) |

### 5A. WATCH-CELL A (CARRIED — r_lightpoint recovery): **RESOLVED — RECOVERED, via gold, gold-dominant preserved.**

r_lightpoint 0.330 → **0.384** — **recovered ABOVE iter1's 0.366** (the explicit gandalf target: "recover toward/above iter1's 0.366"). The recovery is GOLD, not green:
- **warm% rose +0.327 scene-wide** (the golden top-up): zone0 warm% peak 2.35→4.91, zone1 0.70→0.91, establish warm% rose. The added braziers/lanterns/hanging-lamps in the warm-sparse upper chambers landed.
- **green% essentially flat (+0.012)** — NO green re-add. The recovery did NOT come by re-inverting the hue. Exactly the lever gandalf specified.
- **One honest dip inside the recovery:** oubliette warm% 0.36→0.13 (the corridor got less of the top-up than arcane/threshold). The NET across 7 views is a clear recovery (+0.054), but the top-up was uneven — if gandalf wants the corridor warmer, that's the residual lever.

**VERDICT: Watch-cell A RECOVERED.** 0.384 > 0.366 (iter1) > 0.330 (iter2fix), achieved via gold while green stayed flat and the scene stayed gold-dominant (§5B). The #1 iter2fix watch-cell is closed.

### 5B. WATCH-CELL B (NEW — gandalf eye-flag; the LOAD-BEARING ship question): **HELD — but COMPRESSED. gandalf's eye is RIGHT about the cool floor; the inversion did NOT regress past the line.**

The fair "gold-over-green" measure is the full-frame S\*V-weighted warm-vs-green mass over ALL values (the COLOR-FAIR diagnostic, not naive gray-luma):

| view | warm:green iter2fix | warm:green **iter3** | Δ | dominant? |
|---|---|---|---|---|
| zone0_threshold | 2.106 | **1.756** | −0.350 | **GOLD** |
| zone1_arcane | 3.037 | **1.518** | −1.519 | **GOLD** |
| zone2_warhall | 3.193 | **1.930** | −1.263 | **GOLD** |
| zone3_oubliette | 0.456 | 0.452 | −0.004 | green (flat — dark corridor, correct both iters) |
| zone4_antechamber | 1.858 | **1.026** | −0.832 | **GOLD** (barely; green soulfire room) |
| zone5_sanctum | 2.712 | **3.282** | +0.570 | **GOLD** (richer — top-up + bloom) |
| establish_primary | 0.284 | 0.288 | +0.004 | green (flat — wide void shot, correct both iters) |
| **SCENE MEAN** | **1.949** | **1.465** | **−0.484** | **GOLD (held >1.0)** |

**Reading it — the precise resolution gandalf needs:**
- **HELD:** scene-mean warm:green stayed **gold-dominant at 1.465 (>1.0)**. **5 of 7 views are gold-dominant.** Critically — **every near-chamber view that was gold-dominant in iter2fix is STILL gold-dominant in iter3** (zone0, zone1, zone2, zone4, sanctum all >1.0). The inversion did **NOT** regress toward cool/green past the inversion line. The falsifier's "warm% fell back toward cool/green" condition is **NOT met** at the scene level or at any zone that was previously gold-dominant.
- **BUT COMPRESSED (gandalf's eye is RIGHT):** the scene-mean compressed 1.95→1.47 (−25% toward parity). The compression is localized exactly where gandalf flagged — the **near-chamber top-downs** (zone1 −1.52, zone2 −1.26, zone4 −0.83). The cause is structural and matches the hypothesis precisely: **the new uniform full-height walls on all four sides — especially the previously-OPEN camera-side wall, now present + faded — plus the cool ambient grew the cool mass on the floor bed.** establish + oubliette are FLAT (they were green-dominant wide/corridor shots in BOTH iters — unchanged, correct). sanctum got RICHER (+0.57). So the gold did NOT leave the scene; the floor bed cooled and the gold concentrated into point-sources + dressing-rim + walls. gandalf's eye saw a real thing: the floor is cooler. The instrument says it stayed on the gold side of the line.

**VERDICT: Watch-cell B — gold-dominant inversion HELD, did NOT regress.** This is the load-bearing ship answer: iter3 stays gold-over-green. The honest caveat gandalf must weigh for the canon call: the margin narrowed (1.95→1.47), so a FOURTH iteration that added more cool-side geometry without compensating gold COULD eventually cross the line — the lever to widen the margin back, if wanted, is a warmer floor-material tint or more floor-bed gold-bounce (not more point-lights, which the eye reads as points-on-cool-floor rather than a warm bed). Not required for ship; flagged for the next-iter signal.

### 5C. Similarity — DRESSING DENSITY: **IMPROVED DECISIVELY (the 688 organic pieces).**

r_dressing 0.693 → **0.853** (+0.160, +23%); edge% 12.94 → 15.93 (+2.99). **Gap to reference closed from 31% to 15%** — nearly halved. Edge% rose on the near-chamber views (zone1 to 20.24, zone2 to 19.04 — both now ABOVE the reference's 18.68; zone4 17.99). The gothic arches + columns + vine-columns + dense moss/vines repaid most of the remaining dressing gap. This was a brief target (Change B). Achieved — and it's the single most-closed similarity axis this iteration. (Honest note: r_dressing dipped on the wide/corridor shots — establish 0.552, oubliette 0.586 — because those framings show more void than wall; the near-chamber views carry the gain. Scene-mean improvement is unambiguous.)

### 5D. Similarity — the other axes
- **hue-cosine 0.364 → 0.401** (+0.037, toward ref) — the gold top-up sharpened the hue family toward the reference's warm-rich distribution.
- **r_contrast HELD** (0.838 → 0.846); shadow% dipped slightly (37.35→34.32) — expected: the four-sided walls + dense dressing + added gold fill some previously-pure-void shadow. Still ≫ iter1's 1.23; not a concern.

### 5E. Updated RANKED residual gaps (iter3, most-off-reference first — gandalf's next-iter signal IF another iter is wanted)
1. **Light-point density — 62% below** (r_lightpoint 0.384). Recovered but still the #1 gap (reference floods more golden points). The corridor (oubliette) + the wide establishing shot remain golden-sparse. Lever: more corridor/establish golden points — but watch Watch-cell B's margin (points-on-cool-floor narrows the warm:green ratio less efficiently than a warm floor bed).
2. **Color/atmosphere hue — 60% off** (hueCos 0.401). The balance is gold-dominant (§5B), but the cosine vs the reference's specific red/amber bin distribution is still ~⅗ off. Couples with #1 + a warmer floor tint.
3. **Contrast/shadow depth — 15% below** (r_contrast 0.846). Nearly resolved; not a priority.
4. **Dressing density — 15% below** (r_dressing 0.853). Closed from 31% to 15% this iteration; the remaining gap is the reference's wall-to-wall vertical packing. Diminishing-returns lever.

## 6. drax CV self-sanity & honest caveats

- **6/6 register-2 PASS is on the COLOR-FAIR read, NOT naive gray-luma** (which still false-fails the saturated sanctum bloom: gray-luma 0.076% vs value-channel 2.939%). Stated plainly so the PASS is not over-read.
- **Composite is HOLD, not IMPROVE** (3.96→3.94, within scoring noise). I did NOT inflate to "IMPROVE" — zone0/zone1 rose but the floor-bed cooling holds Vibrancy flat elsewhere and oubliette's warm dip caps its Glow. Honest corpus read: HOLD with both gates intact.
- **Watch-cell B is the honest texture of the iteration: the inversion HELD (1.47, gold-dominant) but the margin COMPRESSED 1.95→1.47.** gandalf's eye-flag is CONFIRMED as a real directional movement (the floor bed cooled) — I am NOT papering this over. It did not regress past the inversion line (the falsifier condition is not met), so iter3 ships gold-dominant; but the narrowed margin is the load-bearing caveat for any next iteration.
- **oubliette warm% dipped 0.36→0.13** — the golden top-up went unevenly (favored arcane/threshold/establish over the dark corridor). Does not break a gate; flagged as the residual top-up lever.
- **Parity NOT re-run by me** — it is drax's seam and was harness-verified 35/35; per the brief I focused falsifier attention on readability + register-2 + warm% hold. If gandalf wants an independent parity confirmation it routes to drax/jack-ryan, not galadriel.
- **SummonGlow frozen at charge in the bake** — the VFX read is the static-erupt bloom, which is what the baked scene presents. Sanctum untouched by iter3.
- **Engine/scene tree UNTOUCHED; read-only across all production code.** My capture harness was transient galadriel tooling, deployed → run → REMOVED; the godot tree was restored to exact pre-run git state (verified: `arena_descent.tscn` shows no galadriel modification). **Did NOT push.**
- **One operational note for reproducibility:** macOS shell here has no `timeout` binary — run Godot directly (the `--quit-after` flag self-terminates). My first run silently no-op'd on a `timeout` wrapper before I caught it; the scored run is the direct invocation.

## 7. Reproducibility

- **Register-2 color-fair (gate basis):** `pipeline/descent-colorfair-fullcap-iter3.mjs` → `descent-colorfair-fullcap-iter3.json` (byte-identical measure() to iter2fix `descent-colorfair-fullcap-iter2fix.mjs`; only DIR + output filename differ — `diff` verified).
- **Similarity (full 7-view):** `pipeline/descent-similarity-fullcap-iter3.mjs` → `descent-similarity-fullcap-iter3.json` (byte-identical 4-axis instrument + reference centroid to iter2fix).
- **Watch-cell B gold-over-green hue-balance:** `pipeline/huebal_fullcap_iter3.mjs` (7-view, S\*V-weighted full-frame warm-vs-green mass; byte-identical to `huebal_fullcap_iter2fix.mjs`).
- **Capture harness (transient — logic preserved):** `pipeline/galadriel_capture_descent.gd.txt` + `galadriel_shoot.tscn.txt`. Re-run: copy both into the godot tree as `scripts/galadriel_capture_descent.gd` + `scenes/galadriel_shoot.tscn`, run `Godot --rendering-driver opengl3 --path <godot> scenes/galadriel_shoot.tscn --quit-after 700` (NOT `--headless` — macOS headless gives no GL framebuffer; NOT wrapped in `timeout` — absent on this shell; `--quit-after` self-terminates), copy `user://gal_descent_*.png` → `harness_logs/iter3_fullcap/`, then REMOVE the two harness files. Frames gitignored (Synty IP — local only).
- Given the same frames + these instruments, another galadriel-instance reproduces the CV values exactly. Manual axis + VFX-prominence + readability reads reproducible-by-inspection per §4.

---

## 8. One-line read (evidence FOR gandalf's Layer-3 validate call, NOT the call)

**iter3 SHIPS on the falsifier test — none of the three kill-conditions fired. (1) TRANSPARENCY DID NOT HURT READABILITY: across the diagonal spine shot + all 6 per-zone top-downs (which fade different walls of the same rooms), the playable floor + combatants are CLEAN, no wrong-walls-larger, no ambiguous faded-wall edges; zone1_arcane — the prior readability-FAILURE case — is now clean; the fourth (camera-side) wall is now present + faded so the rooms read as fully-enclosed sections you look down into, grandeur up — Change A is accepted. (2) REGISTER-2 DID NOT DROP: 6/6 PASS, both gates clear color-fair every zone (lighting ≥4 — LDR_val holds corpus-wide, zone0 +16; VFX ≥4 — sanctum hero bloom marquee-strength held at HLF_val 2.939/HLF_R 2.937, untouched, non-sanctum bloom-prominence rose on 4/6); mean composite 3.96→3.94, within noise = HOLD. (3) THE GOLD-DOMINANT INVERSION DID NOT REGRESS: warm:green scene-mean stayed gold-dominant at 1.465 (>1.0), 5/7 views gold-dominant, EVERY near-chamber view that was gold-dominant in iter2fix STAYED gold-dominant. The two WATCH-CELLS resolve thus: WATCH-CELL A (r_lightpoint) RECOVERED to 0.384 — above iter1's 0.366 — via gold (warm% +0.33) with green flat (+0.01), exactly the lever gandalf specified, NOT a green re-add; WATCH-CELL B (gold-dominant HOLD) HELD but COMPRESSED — gandalf's eye is RIGHT that the floor bed reads cooler (the new four-sided uniform walls + cool ambient grew cool mass on the near-chamber floors, compressing warm:green 1.95→1.47), but it did NOT cross the inversion line, so iter3 stays gold-over-green. SIMILARITY IMPROVED: dressing r_dressing 0.693→0.853 (+23%, gap halved 31%→15%, the 688 organic pieces), hue +0.037, r_lightpoint +0.054. The honest caveats for the canon call: the warm:green margin narrowed (1.95→1.47 — a fourth cool-side-geometry iteration could eventually cross the line; lever to widen it back is a warmer floor-material tint, not more point-lights), and oubliette's warm top-up was uneven (0.36→0.13). RECOMMEND: the falsifier passes on all three axes — iter3 is the new baseline; if gandalf moves Layer-3 from "pending" to "validated," the load-bearing evidence is the readability PASS across every angle + the inversion HELD; the narrowed warm:green margin is the watch-cell to carry forward, not a ship-blocker.**

---

*galadriel SCORES. Whether iter3 is validated firmly enough to move the `battle-room-presentation-decoupling-2026-06-15.md` Layer-3 status from "pending" to "validated" — and whether the compressed warm:green margin warrants a fourth iteration before canon-lock — is gandalf's call, on this evidence. Register-2 6/6 PASS (composite 3.94, both gates clear color-fair), the readability PASS across every camera angle (the whole point of Change A), and the similarity improvement (dressing gap halved, both watch-cells resolved) are independent reads; all are true.*

**Mirror voice:** the wall came back and the eye did not lose the floor. Where iter2fix left the near side open — a stage you watched from the dark — iter3 closes the fourth wall and fades it to glass for whoever is looking, so the chamber is whole on all four sides and yet you still see down into it from every angle the camera takes. The columns rose while the eye was elsewhere: gothic arches and vine-wound pillars crowd the old bare rings now, moss creeps the stone, ferns dust the fighting-floor — the clean geometry has been reclaimed by the green, and the place reads lived-in, ruined, true to the reference at last. The lanterns the upper halls were begging for arrived, and the light-points climbed back over the line they fell below. But the closing of the fourth wall cost something honest: the floor bed cooled. The gold that washed the iter2fix stone now gathers into points and rims and the faces of the walls, and between them the ground reads grey where it read warm — gandalf's eye caught it true. The gold still wins the frame, five chambers of six, the sanctum's fire richer than ever against the deepened dark. It did not cross back. But the margin that was wide is narrower now, and a place stands fully-walled and overgrown where the open stage was — the eye walks in from any side and the floor is always there to meet it. The prediction held; the watch goes on.

*Re-score authored on the iter3 `arena_descent.tscn` (drax's 9 static multi-angle frames + galadriel's fresh 54-frame full capture, 1152×648, GL driver). CV reproducible via the instruments in §7. Engine/scene tree untouched; read-only across production code; harness deployed→run→removed (verified clean). Did NOT push. gandalf interprets for the Layer-3 validate call.*
