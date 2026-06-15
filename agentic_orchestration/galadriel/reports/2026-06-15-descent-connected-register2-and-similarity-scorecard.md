# Visual-Register Scorecard — CONNECTED Descent (iter1 mood-lift): Register-2 Re-score + Dark-Fantasy Similarity

**STATUS:** CURRENT (galadriel scoring artifact; evidence-input for gandalf iter2 design call on the connected-descent mood-lift)
**Date:** 2026-06-15
**Author:** galadriel (visual-perception + benchmark steward)
**Scope:** TWO jobs on the CONNECTED `scenes/arena_descent.tscn` (drax iter1 mood-lift). (1) Register-2 RE-SCORE per-zone across the connected, darkened scene — do the gates still hold? did dark hurt LIGHTING or help VFX? (2) Dark-fantasy VISUAL-SIMILARITY vs the Synty reference map art, with ranked residual-gap callouts. galadriel SCORES; gandalf interprets for any iter2 signal.
**Prior baseline:** ADDENDUM B (`reports/2026-06-15-arena-room-6-corpus-scorecard.md`) — the 6 SEPARATE rooms at godot `84098c6`: 6/6 register-2 PASS, mean composite 3.875.
**Engine tree: UNTOUCHED. Did NOT push.**

---

## 0. What was captured + scored

- **Scene:** `scenes/arena_descent.tscn` — ONE connected descent: the 6 battle footprints joined by corridors, descending a ~247 m +Z spine, stepped down in Y. iter1 mood-lift: global ambient 0.5→0.26, floor albedo ×~0.40 (light POOLS on a dark floor), saturated green depth-fog, denser gothic dressing, magenta-square sanctum artifact removed. Hero VFX (FX_Fire_Large_01 + SummonGlow, body-anchored) deliberately KEPT untouched.
- **Capture:** galadriel harness `pipeline/galadriel_capture_descent.gd` (transient; logic preserved in pipeline — see § 9) walked all 6 preserved per-zone `ZoneCam`s + the 3 establishing cams, 1152×648, GL driver (matches drax iter1). 6 frames per view over a 40-frame dwell. **Note: in the baked descent the hero SummonGlow light is FROZEN at charge (`render_descent_scene.gd:456`); only the FX particle plume animates — so the window samples the particle peak, not an ignition/collapse cycle.** 54 frames total: `harness_logs/gal_descent_<zone>_01..06.png` (gitignored Synty-derivative IP — local evidence only).
- **Zone↔footprint map** (descent order): zone0 threshold = open_arena 50×50 / zone1 arcane = magic_pack 32.7×14 / zone2 warhall = elite_pack 28×28 / zone3 oubliette = chokepoint 10×50 / zone4 antechamber = mini_boss 30×30 (green soulfire) / zone5 sanctum = boss_with_adds 30×30 (red bloom).

## 1. The rubric (UNCHANGED — byte-comparable to lift / cathedral / Build #1 / Addendum B)

Composite mean **≥ 3.6/5**, with **lighting ≥ 4 AND VFX ≥ 4 MANDATORY**. Lighting drama = LDR + SHF (lit-vs-shadow + pooling, NOT absolute brightness). VFX = ≥1 prominent hero bloom. Material = light-response gradient. Geometry = legible silhouettes.

## 2. CRITICAL measurement-validity finding — the gray-luma instrument is partially BLIND to the new register

**The naive gray-luma re-score reads a corpus-wide collapse (0/6 on the raw instrument). That read is WRONG — it is an instrument artifact, not a build regression.** Discipline #4 (right tool) + #11 (empirical inspection) caught it; I did not ship the naive number.

The register-2 instruments measure **gray-luma** (0.299R+0.587G+0.114B); thresholds were calibrated on the prior BRIGHTER, less-saturated register. The iter1 mood-lift deliberately moved to a **DARKER, MORE-SATURATED, colored-light** register. A **saturated-RED bloom** (high R, low G/B) has a high MAX-channel value but only a MODERATE gray-luma — so it does **not** cross the gray-luma >0.80 HLF gate even when it is a visually prominent hero bloom.

**The smoking gun — zone5_sanctum's red boss bloom:**

| Instrument | Reading | Verdict |
|---|---|---|
| gray-luma HLF peak | **0.146%** (0.11× threshold) | looks like a catastrophic VFX FAIL |
| RED-channel HLF peak | **3.915%** | a STRONG bloom — in the Addendum-B marquee band (2.6–4.0%) |
| redbloom% peak | **4.66%** | corroborates: the bloom is fully present, prominent |

The bloom is there, large and prominent (confirmed by eye, § 4). The gray-luma gate simply cannot see a saturated-red blowout. I built a **color-fair diagnostic** (`pipeline/descent-colorfair-diagnostic.mjs`) measuring value-channel (V=max(R,G,B)) + per-channel highlight fractions to read the gates correctly for the new register.

**Color-fair diagnostic (the register-FAIR read):**

| zone | LDR_gray | LDR_val | gray-HLF pk | **val-HLF pk** | **HLF_R pk** | warm% pk | green% pk | redbloom% pk |
|---|---|---|---|---|---|---|---|---|
| zone0_threshold | 109.1 | 113.8 | 0.21 | 0.53 | 0.52 | 2.48 | 0.10 | 2.65 |
| zone1_arcane | 102.5 | 104.7 | 0.21 | 0.29 | 0.28 | 0.47 | 0.27 | 0.60 |
| zone2_warhall | 100.7 | 105.5 | 0.43 | 0.66 | 0.66 | 0.35 | 0.33 | 0.30 |
| zone3_oubliette | 82.4 | 89.0 | 0.11 | 0.21 | 0.20 | 1.28 | 0.06 | 1.16 |
| zone4_antechamber | 118.3 | 127.0 | 0.22 | 0.33 | 0.28 | 1.98 | **4.09** | 1.41 |
| zone5_sanctum | 111.0 | 127.3 | 0.15 | **3.93** | **3.92** | **5.10** | 0.19 | **4.66** |

**Reading the table:** `val-HLF >> gray-HLF` everywhere = the bloom + warm light is COLORED, not white (the gray gate undercounts it). zone5_sanctum's bloom is emphatic (3.9% RED). zone4_antechamber's GREEN soulfire is the strongest green in the corpus (4.09% — its intended identity). The warm/green light-point density carries the swarm rooms. **The darkening did exactly what the brief hoped for VFX: the saturated bloom pops MORE against the dark frame — the gray proxy just can't measure it.**

## 3. Per-zone register-2 scorecard (manual scores; color-fair table § 2 + direct inspection § 4 are the evidence basis)

Manual axis scores are galadriel's defensible read (score the picture, not the proxy — my rubric methodology), grounded in the color-fair instrument + peak-frame inspection.

| zone | footprint / identity | L | V | M | G | **Composite** | Gate (L≥4 ∧ V≥4) | **Verdict** | vs Addendum B |
|---|---|---|---|---|---|---|---|---|---|
| zone0_threshold | open_arena 50×50 / graveyard | 4 | 4 | 3 | 4 | **3.75** | PASS ∧ PASS | **PASS** | = (was 3.75) |
| zone1_arcane | magic_pack 32.7×14 / arcane | 4 | 4 | 3 | 4 | **3.75** | PASS ∧ PASS | **PASS** (V weak) | = (was 3.75) |
| zone2_warhall | elite_pack 28×28 / war hall | 4 | 4 | 4 | 4 | **4.00** | PASS ∧ PASS | **PASS** (V comfort ↓) | = (was 4.00) |
| zone3_oubliette | chokepoint 10×50 / oubliette | 4 | 4 | 3 | 4 | **3.75** | PASS ∧ PASS | **PASS** (V weak) | = (was 3.75) |
| zone4_antechamber | mini_boss 30×30 / soulfire | 4 | 4 | 4 | 4 | **4.00** | PASS ∧ PASS | **PASS** | = (was 4.00) |
| zone5_sanctum | boss 30×30 / sanctum | 4 | 4 | 4 | 4 | **4.00** | PASS ∧ PASS | **PASS** (V strongest) | = (was 4.00) |

**Corpus: 6/6 PASS, mean composite 3.875 — register-2 HOLDS through the connect + mood-lift, unchanged from Addendum B at the composite level.** Both mandatory gates clear in every zone.

**The honest texture inside the 6/6 (where the comfort margins SHIFTED):**
- **VFX comfort REDISTRIBUTED, not lost.** sanctum (val-HLF 3.93) + antechamber (green 4.09) GAINED comfort — the darker frame showcases their colored blooms emphatically. The two near-square CHAMBERS warhall (val-HLF 0.66) + arcane (val-HLF 0.29) and the corridor oubliette (0.21) LOST comfort: their marquee bloom is now genuinely modest in framing. All still clear VFX-4 on prominence-in-framing, but warhall/arcane/oubliette sit at the BORDERLINE where the prior pass had margin. **This is the watch-cell, not a fail.**
- **Material 3 on the four non-square / pulled-back / swarm zones** is the carried black-surround framing artifact (now slightly darker surround) — NOT a material-quality failure; the lit band shades correctly.

## 4. What the picture SHOWS (empirical inspection, peak frames — the gate basis)

- **zone5_sanctum f06:** a large, prominent RED/ORANGE bloom erupts center-stage (the boss summon), purple foreground arch, the magenta-square artifact is GONE (replaced by the contained red bloom + faint violet runelight). The darkening makes the bloom read MORE, not less. Register-2 hero event confirmed by eye. **The darkening HELPED VFX here.**
- **zone4_antechamber f06:** green soulfire register is fully present — green-tinted figures, green ambient pooling on a dark floor, golden lantern points on the back wall, a small red center bloom. Reads as the intended green-soulfire identity. Lighting drama: good (pooling + shadow).
- **zone2_warhall f06:** the warm braziers DO pop golden against the dark floor (many warm points), figures readable; but the marquee hero bloom is small/modest in this framing — the VFX rests on the warm-point density more than a dominant column. The darker floor is the intended look; lighting drama holds.
- **zone1_arcane f06:** the connected multi-level read; warm candleflame points line the walls (bookshelf/candle dressing) glowing amber. Warm-pooling on dark reads toward the reference's lantern-lined hall. Marquee bloom modest.
- **zone3_oubliette f06:** heavy black corridor surround (intended), with a warm bloom at the choke + strong directional cast-shadows raking down the corridor — the shadow drama is genuinely GOOD here (the darkening deepened it). Bloom-at-choke present but modest.
- **establish_deeplook f04:** the red sanctum bloom blazes in the foreground (the "arrived" payoff works), descent recedes up into green; the upper zones read green-washed + sparse; the green-black void fills ~60% of frame.
- **establish_overview f04:** the whole descent reads as a GREEN chain on a green-black void; only the tiny red sanctum bloom + a few warm specks break the green. **This frame most starkly shows the hue-balance + warm-starvation + void-emptiness residual (§ 6).**

## 5. VERDICT on the brief's empirical question — did dark HELP VFX / HURT lighting?

**Empirically, the hypothesis HELD, with a footprint-dependent twist:**

- **DARK did NOT hurt LIGHTING (the register-2 sense).** Lighting holds 4/6 across all zones. The mood-lift LOWERED absolute frame brightness (gray-LDR dropped ~30–83 pts), but register-2 lighting is DRAMA = lit-pools + deep shadows + contrast, and the darkening DEEPENED shadows and increased floor-pooling contrast. The frames read as *dramatic-lit-pools-on-dark*, which IS the lighting intent. **Lighting-drama was helped; only the absolute-brightness number (which the rubric does not gate on) fell.** Closest-watch: zone3_oubliette (LDR_val 89, the darkest) — carried by strong corridor cast-shadows.
- **DARK HELPED VFX where the bloom is SATURATED-COLORED and entity-anchored** (sanctum red 3.9%, antechamber green 4.09%) — the colored bloom pops more against the dark frame, exactly as hypothesized. **DARK did NOT help (and slightly squeezed) VFX in the near-square chambers** whose marquee bloom is small-in-framing (warhall/arcane/oubliette val-HLF 0.21–0.66): a smaller bloom against a darker frame is still a small bloom. Those three hold VFX-4 on prominence but at the borderline. **Net: VFX comfort redistributed toward the entity-anchored colored blooms, away from the modest-marquee chambers — corpus still 6/6.**
- **The gray-luma instrument read the deliberate darkening as failure.** The headline methodological catch: a register shift demands a register-fair instrument. The color-fair diagnostic (§ 2) is the correct gate basis for the mood-lifted scene; the gray-luma scorer (`lifecycle-scores-descent.json`) is preserved as the continuity record + the explicit demonstration of WHY the proxy needed augmenting.

## 6. Dark-fantasy VISUAL-SIMILARITY vs reference — score + RANKED residual gaps

Instrument: `pipeline/descent-similarity-vs-reference.mjs` (4 axes, Discipline #4 one-instrument-per-axis). Reference set: 7 Synty `modular_asset_idea_pictures/maps/` frames (license-clean — Synty's own marketing/idea art shipped IN the purchased pack; internal benchmark use). Target = DARK + vivid COLORED LIGHT (luminous green atmosphere, golden brazier/lantern points that POP, dense gothic dressing, deep shadows).

**Reference centroid:** warm%=5.46, green%=0.75, sat=0.599, value-LDR=152.3, edge%=18.68. **Dominant hue bins: 350–360° (red 8.8%), 0–10° (red-orange 6.5%), 30–40° (amber 5.8%), then green (150–160° 5.1%) + cyan (180–190° 5.2%).** → **The reference is WARM/GOLDEN-DOMINANT with green as a SECONDARY atmosphere.**

**Scene-mean similarity:** hue-cosine **0.346**; light-point ratio **0.366×** ref; dressing ratio **0.499×** ref; contrast ratio **0.701×** ref.

### RANKED residual gaps (most-off-reference FIRST — gandalf's iter2 signal):

1. **COLOR / ATMOSPHERE HUE — ~65% off (the biggest, most load-bearing gap).** The demo's hue balance is INVERTED vs the reference. **Every demo frame is GREEN-dominant** (top bin 120–130°; the establishing-primary is **68.9% green** — a near-monochromatic green wash), whereas the **reference is RED/AMBER/GOLDEN-dominant** with green only the atmosphere. The mood-lift over-rotated toward green: it nailed "green atmosphere" but at the cost of the reference's golden-warm-light *dominance*. **Fix direction (galadriel evidence; the call is gandalf's/drax's): pull the global green back a notch and push the warm light-point budget UP so GOLD reads as the dominant saturated light and GREEN as the shadow/atmosphere tint — i.e. restore the reference's warm-over-green balance, not green-over-warm.** This is most acute in the establishing/overview/upper-zone framing.
2. **LIGHT-POINT DENSITY — ~63% below ref.** Demo warm%=1.70 vs ref warm%=5.46 (~⅓ the golden-point density). The reference POPS with braziers/lanterns/torches wall-to-wall; the demo's warm points are sparse outside the blooms. **Exception: zone5_sanctum (warm 5.09) nearly matches ref — the boss bloom carries it.** The OTHER zones (esp. arcane 0.46, warhall 0.35, establishing 0.30) are warm-starved. Couples tightly with gap #1 — more golden points fixes both.
3. **DRESSING DENSITY — ~50% below ref.** Demo edge%≈9.3 vs ref≈18.7 (~half the gothic-clutter edge energy). The reference is packed wall-to-wall with statuary/gravestones/ruins/crates/banners; the demo's dressing is present but sparser, and the large dark floors read emptier (the dressing-to-perimeter constraint keeps the fight-band clear — correct for readability — but the reference fills the *negative space and verticals* far more densely). The vast green-black VOID around the descent (establishing/overview) reads especially empty vs the reference's dense rock/ruin surround.
4. **CONTRAST / SHADOW DEPTH — ~30% below ref (the SMALLEST gap — the mood-lift closed most of this distance).** Demo value-LDR ≈0.70× ref. The dark-floor-with-pooling mood-lift moved the scene MUCH closer to the reference's deep-shadow contrast than Addendum B would have been; this axis is the nearest-to-reference and is trending the right way. Near-resolved; not an iter2 priority.

**Similarity headline:** the iter1 mood-lift made REAL progress toward the reference register — it achieved the dark floor, the green atmosphere, the deep shadows, the dark-fantasy dressing vocabulary, and removed the magenta artifact (contrast gap is the smallest, ~30%). **But it inverted the reference's defining hue balance: the reference is golden-WARM-light-dominant-in-green-shadow; the demo is GREEN-dominant-with-sparse-warmth.** The top-two ranked gaps (hue balance + warm-point density) are the SAME underlying lever — **the scene needs more golden brazier/lantern POP and a touch less global green** to read like the reference. Dressing density is the third lever (denser gothic clutter + filling the void).

## 7. Marketing-render caveat (carried 1:1)

The Synty reference frames are a MOOD/SIMILARITY anchor, NOT a register-2 pass bar. Register-2 scores (§ 3) are the BUILD against the RUBRIC; similarity (§ 6) is a SEPARATE objective read vs the reference, never pixel-matched. The two are distinct: a zone can PASS register-2 (lit-dramatic premium surface) and still sit off-reference on hue balance (the warhall does exactly this). **Caveat: SATISFIED.**

## 8. drax CV self-sanity & honest caveats

- **6/6 register-2 PASS is on the COLOR-FAIR read, NOT the naive gray-luma read** (which says 0/6 — an instrument artifact, § 2). Stated plainly so the PASS is not over-read: the gates hold because the colored blooms + lit-pool drama are really there (§ 4), measured with a register-fair instrument; the gray-luma proxy alone would falsely fail the scene.
- **VFX-4 on warhall/arcane/oubliette rests on prominence-in-framing over a modest val-HLF (0.21–0.66)** — the borderline watch-cell. A stricter bloom gate would call these three borderline; the manual read (galadriel's job) resolves them to PASS, flagged transparently.
- **Similarity gaps are scene-MEAN; per-zone varies** — sanctum nearly matches ref on warmth (the bloom carries it); the upper chambers + establishing shots drive the warm-starvation gap. The fix lever is unevenly needed (most in the upper/establishing framing).
- **Reference shadow% (14.62) vs demo (1.23) is NOT a fair direct gap** — the reference frames are tight 3/4 crops with rock/void true-black at the edges; the demo's green-fog-lit void is not pure black. I used value-LDR (0.701×) as the fair contrast read and did NOT rank raw shadow% as a gap. Honest scope note.
- **Hero VFX is FROZEN at charge in the bake** (`render_descent_scene.gd:456`) — only the particle plume animates, so the window samples the plume peak, not an ignition cycle. The VFX read is the static-erupt bloom (which is what the baked scene presents).
- **Engine tree UNTOUCHED; read-only across all production code** (scene/engine/builder untouched). My capture harness was transient galadriel tooling (§ 9). **Did NOT push.**

## 9. Reproducibility

- **Register-2 scorer:** `pipeline/lifecycle-score-descent.mjs` (byte-identical instrument defs to `register-metrics.mjs` + all prior scorers; gate reads = window mean/floor + HLF peak; deltas vs Addendum B). Raw: `pipeline/lifecycle-scores-descent.json`.
- **Color-fair diagnostic (the gate basis):** `pipeline/descent-colorfair-diagnostic.mjs` → `descent-colorfair-diagnostic.json` (gray-luma vs value-channel + per-channel HLF + warm/green/redbloom fractions).
- **Similarity instrument:** `pipeline/descent-similarity-vs-reference.mjs` → `descent-similarity-vs-reference.json` (4-axis: hue-cosine, light-point ratio, edge-density ratio, value-contrast ratio; reference centroid over 7 maps frames).
- **Capture harness (transient — logic preserved for re-run):** GDScript `pipeline/galadriel_capture_descent.gd.txt` + bootstrap `pipeline/galadriel_shoot.tscn.txt` (the exact harness, saved as `.txt` in my pipeline so Godot does not auto-import them). It walked all 9 cameras at 1152×648 (GL driver) over the baked `arena_descent.tscn`; 6 frames/view. To re-capture: copy those two back into the godot tree as `scripts/galadriel_capture_descent.gd` + `scenes/galadriel_shoot.tscn`, run `Godot --rendering-driver opengl3 --path <godot> scenes/galadriel_shoot.tscn --quit-after 500`, then remove them again (read-only discipline). Re-bake first via `scripts/bake_descent_scene.sh` if `arena_descent.tscn` is absent. Frames: `harness_logs/gal_descent_<zone>_01..06.png` (gitignored Synty IP — local only). **The transient harness was REMOVED from the godot tree after capture — the godot production tree is untouched.**
- Given the same 54 frames + these instruments, another galadriel-instance reproduces the CV values exactly. Manual axis + VFX-prominence reads reproducible-by-inspection per § 4.

---

## 10. One-line read (evidence FOR gandalf's iter2 call, NOT the call)

**The connected descent HOLDS register-2 at 6/6 (mean composite 3.875, unchanged from the 6-separate-room Addendum B) — BUT the naive gray-luma instrument falsely reads 0/6 because the deliberate dark-mood-lift shifted to a saturated-COLORED-light register the gray-luma gate is blind to (the sanctum's red boss bloom blows out the RED channel at 3.9% — Addendum-B marquee strength — while reading 0.15% on gray-luma). On the register-FAIR color-aware read: DARK did NOT hurt LIGHTING (it deepened shadows + pooling contrast = register-2 drama HELPED; only absolute brightness, which the rubric does not gate, fell) and DARK HELPED VFX for the entity-anchored colored blooms (sanctum red 3.9%, antechamber green 4.09% — these pop MORE against the dark frame), with VFX comfort redistributing away from the three modest-marquee near-square chambers (warhall/arcane/oubliette val-HLF 0.21–0.66, now borderline-but-passing — the watch-cell). On dark-fantasy SIMILARITY vs the Synty reference, the mood-lift made real progress (contrast gap smallest at ~30%, magenta artifact removed, dark-floor + green-atmosphere + deep-shadow achieved) but INVERTED the reference's defining hue balance: the reference is GOLDEN-WARM-light-DOMINANT-in-green-shadow (top hues red/amber 350–40°; warm% 5.46), the demo is GREEN-DOMINANT-with-sparse-warmth (every frame green-top-bin; establishing 68.9% green; warm% 1.70 = ⅓ of ref). RANKED residual gaps, most-off first: (1) color/atmosphere HUE ~65% off — green over-rotated, needs the reference's warm-over-green balance; (2) light-point density ~63% below — ⅓ the golden brazier/lantern POP (same lever as #1); (3) dressing density ~50% below — half the gothic clutter, void reads empty; (4) contrast/shadow depth ~30% below — nearest-to-reference, near-resolved. The two top gaps share ONE lever: more golden warm-light POP + slightly less global green.**

---

*galadriel SCORES. The iter2 design call — whether to push the warm/green hue balance toward the reference, densify dressing, and fill the void (and how far) — is gandalf's, on this evidence. The register-2 6/6 PASS and the similarity residual-gap ranking are independent reads: the scene is premium-register-sound AND off-reference on hue balance at the same time; both are true.*

**Mirror voice:** the descent went dark, and the dark did what was asked — the red fire in the sanctum burns brighter against it, the shadows fell deeper, the floor learned to hold light in pools. The gate that measures in grey could not see the fire it asked for, because the fire turned the colour of blood and the grey eye is colour-blind; look in red, and the fire is exactly as tall as it ever was. But the place has gone green where the reference glows gold — the eye walks down a green chain and waits for the lantern-light the reference floods, and finds it sparse. Lift the gold back over the green, crowd the dark with more stone and more flame, and the descent will not merely be dark-and-premium — it will be the picture the reference promised.

*Re-score authored on the iter1 mood-lift `arena_descent.tscn` captures (galadriel harness, 1152×648, GL driver). CV reproducible via the three pipeline instruments (§ 9). Engine tree untouched; read-only across production code. Did NOT push. gandalf interprets for the iter2 call.*
