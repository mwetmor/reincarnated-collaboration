# Research — VFX oracles for the H1 painted-2D register — 2026-09-14

> **STATUS:** CURRENT — legolas Mode A (commissioned by gandalf, RUN-CONDUCTOR, Run C-3 → VFX lane; brief `agentic_orchestration/gandalf/requests/2026-09-14-legolas-mode-a-vfx-oracles.md`). Filed by gandalf from the agent's returned text (the harness blocks sub-agent repo writes).

**Evidence classes:** VERIFIED (primary source read) · MEASURED (first-hand, method stated) · DERIVED (computed from VERIFIED/MEASURED) · PRACTITIONER-REPORT (talk summary, forum, secondary article) · INTERNAL (our repos, path given).

**Access note:** YouTube was not bot-blocked this session (yt-dlp works with `SSL_CERT_FILE` pointed at certifi). All footage: YouTube, 1920×1080 at 60 / 59.94 fps. Footage used for measurement only; all downloads deleted.

---

## 1. TL;DR — recommended oracle stack

**Process headline.** Hades does not hand-draw effects on 2s. In the shipped data an effect is a **stack of short flipbooks played at 30–120 fps (median 60)**, **tinted at runtime from shared greyscale sheets**; most effects add a **black-tinted duplicate of the same sheet on a dark layer** (`FX_Dark`) beside the **additive** layer; on top sit **fixed-length constants** — a 0.1 s flash, a light disc, a 3 s ground scorch decal. Timing is hand-set per frame: in `Fx.sjson` Slides **64 % of drawn frames are held 1 game frame and 31 % held 2** (VERIFIED). In footage **every frame is a new drawing at 60 fps**; the painted look comes from **flat hard-edged planes, a white core, one dominant hue and dark shapes**, not from low frame rates.

**Outcome headline** (Hades strikes, frame by frame): **peak in 0–1 frames** once anticipation is over (anticipation is a separate telegraph layer: 0.75 s in data, ≈ 1.2 s in footage); **area halves in 2–7 frames**; a **low-value residue** of 15–25 % of peak area lingers 0.3–1 s; **hue is one family** (circular SD 10–24° on saturated pixels); **saturated body** (median S 0.74–0.78) **around a desaturated white core** (S 0.02–0.27) that is **13–40 % of effect area at peak**. The D2R contrast effect is pale (median S 0.18–0.33).

| Kind | What |
|---|---|
| **Closed-form outcome measures** | O1 phase envelope (area/peak per frame) · O2 visible life · O3 white-core fraction and its order (flash-first / core-last) · O4 hue circular SD · O5 core-vs-edge saturation (core saturating during dissipation) · O6 extent in body-heights vs gameplay radius · O7 projectile speed in body-heights/s · O8 drawing-change rate · O9 secondary-layer budget (flash, decal, light, hit-stop, shake) |
| **Judge axes** (not closed-form; from Matt's verdicts) | directionality / facing-lock (R-C3-28) · frame-to-frame boil / "choppiness" (R-C3-28) · matte halo (R-C3-28) · liveness (R-C3-83) · "reads as painted planes, not rendered noise" · ground component follows owner (L7 §12) |
| **Process precedent** | The **Hades data model ported to Godot 2D**: `AnimatedSprite2D` with per-frame durations · `CanvasItemMaterial` Add layer + Mix black-tinted duplicate · tweened flash `Sprite2D` · ground decal `Sprite2D` · `Engine.time_scale` hit-stop |
| **Exemplar set** (§ 2.1) | E1 Hades Zeus bolt (Theseus variant) · E2 Hades II water splash on hit · E3 Hades kill-hit flash · E4 Hades II Hecate eruption pillar · E5 D2R Frozen Orb (contrast) |
| **Route order** (T4) | (c) procedural Godot baseline → (d) hybrid: painted phase silhouettes + shader → (b) image-to-video for the additive glow layer only → (a) GPT-image for silhouettes and masks only |

---

## 2. Oracle table

**Units.** BH = body-heights. Zagreus 130 ± 4 px upright and 0.945 px/engine unit (2026-09-13 run-speed finding, room B-1 camera) → 1 BH ≈ 137.6 engine units (DERIVED). Keeper 130 px → BH × 130 = Keeper px.

| # | Measure | Definition | Closed-form? | Reference values | Class · source |
|---|---|---|---|---|---|
| O1 | **Rise** | Frames from first effect pixel to peak area | Yes | E1 bolt **≤ 1 frame** · E4 pillar **0 frames** (full on its first frame, twice) · E2 splash: white flash at onset, body peak **+6 frames** | MEASURED (frame sheets + area masks, 59.94/60 fps) |
| O1 | **Anticipation layer** | Separate telegraph before the strike | Yes (duration) | Theseus Zeus bolt `Fuse = 0.75` s with ground preview decal · Hecate pillar ring → eruption ≈ **1.2 s** | VERIFIED `EnemyProjectiles.sjson` `TheseusLightningBolt` · MEASURED |
| O1 | **Decay** | area(t)/peak after peak | Yes | E4 pillar 1: 1.00 → .85 → .53 → .35 → .24 → .20 by +5 f, residue plateau → .15 by +23 · E4 pillar 2: 1.00 → .91 → .57 → .37 → .29 → .26, then .21 at +17 · E2 splash: energy (Σ ΔV) peak → ≤ 50 % in **7 frames** (0.12 s), residue plateau from +9 | MEASURED (hue-gated connected-component area, full res) |
| O2 | **Visible life** | Onset to < 10 % of peak | Yes | E1 **4 frames** (2 bright + 2 fading; 67 ms) · E2 **16–20 frames** (0.27–0.33 s) · E3 victim flash **3 frames** · E4 body 5–6 frames, then residue ≥ 0.8 s | MEASURED |
| O2 | **Data life** | NumFrames ÷ PlaySpeed | Yes | `Fx.sjson` Books (n = 2,810): **p10 0.23 · p25 0.34 · p50 0.59 · p75 1.0 · p90 1.6 s** · PlaySpeed p10/50/90 = **30/60/100** · frames p10/50/90 = **14/32.5/60** | VERIFIED (parsed `xuqifzz/hades-mod-tutorial` @7e06338) |
| O3 | **White-core fraction** | Share of effect pixels with V > .95 and S < .2 (or .25) | Yes | E2 **.28 → .40 (+3) → .20 (+6) → .03 (+10)** flash-first · E4 **.19 → .21 → .26 → .26 → .17 → .08** core-last (core outlives body) · E1 .01–.02 (pale-yellow core) · D2R .14–.18 | MEASURED |
| O4 | **Hue unity** | Circular SD of hue over pixels with S > .3 | Yes | E1 **10–18°** (hue 46–52°) · E2 **12–15°** (193–197°; 42° on the flash frame incl. red damage number) · E3 **21–24°** · E4 **12–14°** (158–166°) · D2R 11–31° (208–211°) | MEASURED |
| O5 | **Saturation structure** | Median S of brightest 10–20 % vs dimmest 25–30 % of effect px | Yes | At peak core paler than edge: E1 core .20–.27 / edge .49–.61 · E2 core .02–.10 / edge .44–.64 · during dissipation core saturates: E2 core .73–.79 at +10…+15 · body median S: E4 **.74–.78** · D2R **.18–.33** | MEASURED |
| O6 | **Extent (visual)** | Effect bbox ÷ body height | Semi (needs body height in the clip) | E1 width ≈ 80–130 px ≈ **0.7–1.1 BH**, height ≥ 650 px (off ROI/screen) ≈ **≥ 5.5–7.7 BH** · E2 ≈ 210–245 px ≈ **1.8–2.2 BH** · E4 width 524–639 px ≈ **4.4–5.4 BH**, height ≥ 782–853 px (off-screen) ≈ **≥ 6.6–7.2 BH** | MEASURED; body heights from action poses (Zagreus 105–110 px, Melinoë ≈ 107 px) × 1.1 → ≈ 115–120 px upright (DERIVED) |
| O6 | **Gameplay radius** | DamageRadius → BH | Yes | Zeus `LightningStrike*` radius 200 × ScaleX 1.175 → **1.7 BH** half-width, ScaleY 0.56 (iso ellipse) · Poseidon cast 500 → **3.6 BH**, ScaleY 0.6 · Theseus bolt 250 → **1.8 BH**, ScaleY 0.5 · cast Range 1100 → **8.0 BH** | VERIFIED `PlayerProjectiles.sjson` / `EnemyProjectiles.sjson` → DERIVED |
| O7 | **Projectile speed** | units/s → BH/s | Yes | Bloodstone cast (`RangedWeapon`) Speed 900 → **6.5 BH/s** · Poseidon / Artemis cast 1200 → **8.7** · Zeus cast 1600 → **11.6** · Keeper 130 px: 850 / 1130 / 1510 px/s | VERIFIED → DERIVED; **not cross-checked in footage** |
| O7 | **D2 contrast speed** | Missile Vel ÷ RunVelocity 9 × 4.4 BH/s | Yes (assumption) | firebolt / fireball 20 → 9.8 · icebolt 12 → 5.9 · frozenorb 10 → 4.9 · frozenorbbolt 18 → 8.8 BH/s | VERIFIED Vel (`fabd/diablo2` 1.13 `Missiles.txt`) → DERIVED; assumes shared units (unverified) |
| O8 | **Drawing-change rate** | Unique drawings/s at native fps | Yes | Footage E1/E2/E4: **new drawing every frame at 60** · Data: `Fx.sjson` Slides **2,694 × 1-frame, 1,302 × 2, 131 × 3, 47 × 4, 814 skipped** · E1 sheet `LightningBoltZeusFx`: 30 drawings, first 20 on an alternating skip pattern, last 10 every frame → 20 shown = 0.33 s | MEASURED · VERIFIED; ⚠ data 20 frames vs footage 4 visible — unresolved |
| O9 | **Flash constant** | Short additive flash on impact | Yes | `particle_quickflash`: 147 variants; commonest **0.1 s at StartAlpha 0.5, scale 1.2 → 1.0** (23), then 0.3 s (17) | VERIFIED |
| O9 | **Ground layers** | Decal / nova / light | Yes | Zeus strike: ground nova 20 f @60 (0.33 s) terrain additive · **scorch decal 3.0 s**, α .85 · light disc `AuraBasicFillCircle` **0.2 s** (FX_Add_Top) · Theseus bolt: nova 44 f @75 (0.59 s) **+ black duplicate @70** + ground crack 1 s | VERIFIED `Fx.sjson` chains |
| O9 | **Victim hit flash** | Unit tint on hit | Yes | Data: `Color.Red`, fraction 1 → 0, **Duration 0.03 s** · Footage (kill): **3 frames** flat red silhouette + 3-frame white bloom at contact, then chunk shatter ≥ 20 frames | VERIFIED `CombatPresentation.lua` `DoUnitHitFlash` · MEASURED E3 |
| O9 | **Hit-stop** | Sim slow on hit | Yes | Hades 1 `WeaponData.lua` (198 two-step entries): slow to **0.01× (123) / 0.25× (49) / 0.1× (19)**; slow + lerp-back **median 0.12 s** (0.02–0.26) · sword: 0.04 s wait → 0.1× → 0.01 s → lerp 0.03 · Hades II staff hit: 0.08 → 0.1× → 0.03 + lerp 0.07 · staff Omega hit: 0.03 → 0.1× → 0.02 + lerp 0.10 | VERIFIED values; semantics DERIVED from `DoWeaponFireSimulationSlow`; H2 from `cevasonic/Hades-II-Mod` `Scripts/ProjectileData_Melinoe.lua` @eeae74c (community copy) |
| O9 | **Screen shake** | Distance / duration | Yes | Hades 1: 224 entries, Distance **median 3** (2–15), Duration **median 0.12 s** (0.2–0.7 at extremes) · Hades II Omega hit: Distance 6, Duration 0.34 s, Angle 90 | VERIFIED (units unverified) |
| O10 | **Value bimodality** (candidate) | Mode count of L* histogram inside the effect mask | Yes, uncalibrated | E1, E2: **2 modes** (dark + bright plane) · E4: 2 (both bright) · **D2R: 1** | MEASURED, n = 4, mask-sensitive — inspect only until calibrated (cf. I-7) |
| J | **Dark contour on effects** | Dark stroke / underlay at effect edge | Judge (+ data) | E1: **thin dark stroke along the bolt edge; bolt goes dark as it fades** (frames 9–11) · E2 / E4: **no outline**; shape from dark interior holes and navy shadow planes · Data: 133 `FX_Dark` entries; **56 of 78 dark sheets are the same sheet also drawn additive** | MEASURED (visual, full-res crops) · VERIFIED |
| J | **Dissipation mode** | How it dies | Judge | E2: hard-edged cyan planes **erode from the centre** into a ring, then small pieces; value drops (navy), hue holds · E4: pillar narrows to single beams, then green particulate · E1: bright → dark silhouette → gone | MEASURED (visual) |

### 2.1 Exemplars and timestamps

| Id | Effect | Source (YouTube) | Time |
|---|---|---|---|
| E1 | Zeus lightning bolt, Theseus Zeus call (same bolt sheet as the Zeus god power) | `ijwA_J29j1k` (RagingMonkey, 4K60 no commentary) | **1745.63 s** (telegraph rings from ≈ 1744.9) |
| E2 | Water splash on hit, Hades II (owner inferred player-side; not confirmed) | `5WiYcx9SjZU` (MOBA Nest, Poseidon run) | **605.42 s** |
| E3 | Kill hit: sword dash-strike, victim red flash, shatter | `-2b7GGWNz54` (Silent Longplays P1) | **126.28 s** |
| E4 | Hecate green eruption pillars (enemy) | `5WiYcx9SjZU` | **612.92 s** and **613.43 s** |
| E5 | D2R Frozen Orb (contrast) | `b5a-iIras34` (Infinite Gaming, D2R sorceress, Hell) | **≈ 3025.0 s** |

Rejected: `mx7HUJETVVY` (jump-cut montage, webcam) · `Tl93fMw5wkA` (menus/house in window) · `L4zq-MZdHyM` (screen-filling flashes). The player-side Zeus attack-boon strike and the Bloodstone cast travel were not isolated (§ 6).

---

## 3. Process table

| Game | Medium | Layers | Frames / fps | Blend | Contour on FX? | Directionality | Source · class |
|---|---|---|---|---|---|---|---|
| **Hades** | Flipbooks (`Type=Book`, 2,957) + fixed sprites (`Constant`, 1,712) + retimed flipbooks (`Slide`, 201) + `Random`. **112 of 126 god-variant families share one texture**, recoloured at runtime (`Color` / `AddColor` / `Start*`–`End*` RGB). Authoring tool not primary-sourced (secondary: Photoshop / Maya / After Effects) | body sheet (`Standing` / `FX_Standing_Add`) · **black duplicate** (`FX_Dark`) · displacement (`FX_Displacement`) · quickflash 0.1 s · ground nova (`FX_Terrain_Add`) · scorch/crack decal (1–3 s) · light disc · particles (`VelocityMin/Max`) | Book PlaySpeed median **60** (30–120); per-frame holds in Slides (**31 % held 2 frames**); random PlaySpeed ranges (e.g. 50–70) | `_Add` groups read additive; `Standing` alpha — **inferred from group names**; 1,093 Books additive vs 396 Standing | Some sheets painted with a dark stroke (E1); systemic **dark underlay duplicate** (56 of 78) | `AngleFromOwner = Take`, `UseOwnAngle`, `RandomFlipHorizontal`, `FlipVertical`, `IsometricSkew`, `PostRotateScaleY` ≈ 0.5–0.62 (ground squash). **Rotated at runtime, not baked per direction** | VERIFIED (parsed data) |
| **Hades II** | Same engine family; animation sjson **not public** | Footage (E2, E4): flat hard-edged planes, white core, dark interior holes, particulate residue; one gold line-drawn (contour-only) shield effect | 60 fps new drawing per frame (footage) | not found | E2 / E4 no outline; one line-art effect | not found | MEASURED · scripts VERIFIED (community copy) |
| **Diablo II** | Pre-rendered in 3ds Max → 8-bit sprites | missile sprite + **per-missile light** (radius, RGB in data) + separate explosion missile + unit overlays (61 of 293 behind the unit) | AnimSpeed **16 fps** on 649 of 684 missiles; firebolt 5 f, icebolt 6, frozenorb 16, frost nova 14 | `Trans = 1` "darker = more transparent" on 411 of 595; overlays black = transparent 284 of 293 | Cannot survive the blend (DERIVED) | **Baked**: 16 dirs on 113 missiles, 32 on 98, 8 on 53, 1 on 366 | VERIFIED (`fabd/diablo2`) + PRACTITIONER-REPORT (Phrozen Keep) |
| **Cuphead** | Pencil/ink on paper, coloured in Photoshop; Unity particles also used | not found | Animation **24 fps "on the ones"**, gameplay 60 | not found | not verified | not found | VERIFIED (Moldenhauer, Game Developer) |
| **Dead Cells** | 3D rendered small, no AA, cel shaded, normal map per frame | "VFX … movement, impact and strength" | 30 fps | "a blend mode or two" | not found | not found | VERIFIED (Vasseur) |
| **Hollow Knight** | Photoshop PNGs; Unity + 2D Toolkit | lighting "with soft transparent shapes"; Unity particles | not found | not found | not found | side view | PRACTITIONER-REPORT (Unity) |
| Children of Morta / Eastward / Sea of Stars | Hand-drawn pixel art | **dynamic engine lighting on hand-drawn sprites** | not found | not found | not found | not found | VERIFIED (CoM postmortem) / secondary |
| Hyper Light Drifter / Skul / Transistor / Pyre / Ori / Rayman | Medium only; FX specifics not found | — | — | — | — | — | — |

**What carries to our Godot 2D stack** (DERIVED; Godot APIs VERIFIED at docs.godotengine.org): body → `AnimatedSprite2D` with `SpriteFrames` per-frame durations (Slide holds) · glow → `CanvasItemMaterial` Add · dark underlay → same frames, `modulate` black, Mix, sorted beneath · flash → additive `Sprite2D` tween 0.1 s, α 0.5, scale 1.2 → 1.0 · scorch → Mix `Sprite2D`, 3 s fade · light → additive radial `Sprite2D`, 0.2 s · hit-stop → `Engine.time_scale` 0.01–0.25 for 0.04–0.12 s. **Per-god runtime tint of greyscale sheets** = one painted mask per effect family with element colour as a parameter (agrees with INTERNAL `vfx-pipeline.md` §2). **Directionality from runtime rotation + ground squash (Y ≈ 0.5–0.62), not baked directions** — opposite of D2; far cheaper for hand-painted assets; answers R-C3-28.

---

## 4. Principles as testable rules (T2)

Primary texts: Riot *League of Legends VFX Style Guide* (2017, Wayback PDF) · Mike Lyndon GDC 2018 *Zip! Thwack! Ping!* notes · GDC 2017 *Art Directing VFX for Stylized Games* slides (ADVFX) · Motomura GDC 2015 transcript (GGXrd) · Hi-Fi Rush GDC 2024 deck (HFR). **No source gives an anticipation : peak : dissipation ratio**; O1 supplies footage values.

| Id | Rule (checkable) | Test on our frames | Source · class |
|---|---|---|---|
| P1 | Anticipation → peak → dissipation | area × luminance curve has one clear peak with rise and fall | LoL p.32 · VERIFIED; footage: anticipation often a separate telegraph layer (O1) |
| P2 | Outro lower in value, saturation, opacity than peak | mean V, S, α in outro < peak window | LoL p.32 · VERIFIED; ⚠ E2 contradicts on S (O5) |
| P3 | Energy fades through ≥ 1 of value, hue, saturation, opacity, size | ≥ 1 outro channel slope clearly negative | LoL p.32 · VERIFIED |
| P4 | Keep linger short | time to < 10 % peak area; max from O2 | LoL p.36 · VERIFIED |
| P5 | Non-linear timing: fast rise, ease out | rise / fall ≪ 1 (footage 0–1 vs 4–20 frames) | LoL p.35; Lyndon · VERIFIED |
| P6 | Impacts reach peak almost at once | frames to 80 % of peak ≤ 1 (E1, E4) | Lyndon · VERIFIED |
| P7 | Games animate FX too slowly | compare shape-change rate with reference | Lyndon · VERIFIED |
| P8 | An effect reduces to 4–6 key poses | key silhouettes read at 4–6 frames | Lyndon · VERIFIED |
| P9 | Primary layer beats secondary on value range, opacity, edge sharpness, motion | per-layer statistics | LoL p.6–7 · VERIFIED |
| P10 | Visual edge matches gameplay radius at ground level | collider overlay; extent within ±N % (O6) | LoL p.8–9 · VERIFIED |
| P11 | Visual loudness scales with gameplay tier | Spearman ρ > 0 tier vs S / α / area | LoL p.10–11 · VERIFIED |
| P12 | Never pure 0 / 100 % value or saturation | share at V = 1 or S = 1 ≈ 0; ⚠ Hades clips V = 1 in 13–40 % (O3) | LoL p.13–14 · VERIFIED |
| P13 | Bright centre | radial V profile peaks in inner ~30 % (fork's threshold) | LoL p.15–16 · VERIFIED |
| P14 | One dominant hue; complementary secondary | hue circular SD ≤ ~15–25° (O4) | LoL p.21 · VERIFIED |
| P15 | Effect palette wider in V and S than the caster's | IQR effect > IQR Keeper | LoL p.20 · VERIFIED |
| P16 | Hand-painted shapes, concise detail, soft + sharp edges mixed | Laplacian variance capped; edge-sharpness histogram bimodal | LoL p.28–29 · VERIFIED |
| P17 | Fast movers need a streak shape | major axis along velocity, aspect > 1 above X BH/s (O7) | LoL p.30 · VERIFIED |
| P18 | Offset layer timing | per-layer peaks/decays differ (Hades: flash 0.1 s, nova 0.33–0.59 s, decal 1–3 s, dark duplicate at 70 vs 75) | Lyndon · VERIFIED |
| P19 | Micro-anticipation ("b-boom") | secondary spike within a few frames of peak (E2 flash → body +6) | Lyndon · VERIFIED |
| P20 | Stylised smoke: 3 stepped tones, hard erosion edge | k = 3 colour clusters; bimodal α; boundary shrinks while interior α = 1 (E2 erodes from centre) | ADVFX (Kladis) · VERIFIED |
| P21 | Hold frames, don't interpolate, for a 2D look | stepped frame-difference trace; ⚠ Hades footage changes every frame at 60 (holds exist in data on a 60 fps base) | GGXrd p.27–29 · VERIFIED |
| P22 | Cut frames out of a sim | Fortnite "20 of ~50"; Hades Slide skips do the same (814; E1 20 of 30) | ADVFX · VERIFIED |
| P23 | 2s = 12 drawings/s, 3s = 8/s at 24 fps | unique drawings/s | ANN lexicon · PRACTITIONER-REPORT |
| P24 | Frame-rate modulation: primary motion on 1s, rest on 2s/3s | drawings/s per layer | Wave Motion Cannon · PRACTITIONER-REPORT |
| P25 | Kanada lineage: angular bolts, hard colour blocks, light against dark | polygon-vertex angles; adjacent light/dark blocks | Sakuga Blog (search summary) · PRACTITIONER-REPORT |
| P26 | Impact frames: 1–2 monochrome / inverted frames | global value inversion or saturation collapse at hit (nearest Hades: victim flat red 3 frames, E3) | Sakuga Blog glossary · PRACTITIONER-REPORT |
| P27 | Tone steps from thresholds; AA only at the border | discrete value bands, 1–2 px transitions | HFR · VERIFIED |

**Not sourced:** Gilland *Elemental Magic* I/II primary text BLOCKED (Internet Archive lending-restricted, Google Books 429, Routledge 403) — no Gilland rule sourced · Blizzard/Riot VFX Bootcamp (video only) · Overwatch stylised-FX talk (no slides) · Hi-Fi Rush FX timing (deck covers rendering only) · Trümpler RiME talk (video only) · Kanada / Matsumoto essays (403) · realtimevfx ratio thread (none) · no Supergiant FX GDC talk found.

---

## 5. Route assessment (T4)

**Deciding blend constraint** (DERIVED; Godot Mix / Add / Sub / Mul / Premult VERIFIED): **additive cannot draw a dark contour.** Hades pairs its additive sheet with a **Mix black duplicate**, so a dark component needs a real alpha layer; a route without clean alpha can supply only the glow layer.

| Route | Fit to oracle | Risks | Precedent | Cheapest first experiment (≤ 2 h, Godot 4.6 2D) |
|---|---|---|---|---|
| **(c) Procedural Godot 2D** (CanvasItem shader + CPUParticles2D) | **Exact** on O1/O2 (curves, per-frame durations), O4/O5 (gradient ramp), O8 (`fixed_fps`, stepped TIME), directionality (rotation, `particle_flag_align_y`), O9 (tweens, `time_scale`) | noise reads as "tech texture" unless masks are painted; contour needs a mask or edge pass | RiME alpha erosion (simonschreibt.de) · godotshaders "Wobbly hand-painted" stepped time (VERIFIED code) · LoL "always hand draw your shapes" (secondary) · Hades runtime tint and rotation (VERIFIED) | Frost lance as the **Hades stack**: greyscale painted lance mask along +X · additive body with 3-stop ramp + Mix black duplicate · 0.1 s α .5 flash · 0.2 s light disc · 3 s decal · 0.06 s hit-stop at 0.1× · rotate through 8 facings. Tests O1–O5, O8, O9, directionality |
| **(d) Hybrid:** painted phase silhouettes + shader motion | Best overall (DERIVED): painted planes carry H1 shape; shader carries timing, tint, erosion, rotation | silhouettes are route-(a) outputs → declare grain scale in source px (INTERNAL `2026-09-11-ai-tells…` §1.5); erosion gradient must be computed (distance transform) — image models don't paint one deliberately | Hades shared sheets + runtime tint + dark duplicate (VERIFIED) · LoL painted shapes + engine motion · EmberGen posterised anime explosions (80.lv, PRACTITIONER-REPORT) | Three silhouettes (gather / peak / spent) → `AnimatedSprite2D` with O1 durations (peak ≤ 1 f, halve in 2–7, residue 15–25 %) + posterise + centre-out erosion on the spent frame (E2). A/B against (c) in the T3o picker; Matt judges "painted planes" |
| **(b) Painted keyframe + image-to-video** | Poor on O1/O4/O8 (unplanned motion, hue pulsing, 24 fps output — Grok 768×1168, 24 fps, 6.04 s, MEASURED on our 71 calls); no clean alpha | boil, keying halo on contours, internal cuts, per-clip cost | TransPixeler / TransAnimate RGBA research, text-to-video only (VERIFIED abstracts) · Veo 3.1 `last_frame` (VERIFIED; forum: 8 s requirement) · Grok `last_frame` conflict unresolved (R11) | One Grok clip from a painted peak on #000, decimated 24 → 12 → measure O1 single peak, frame-to-frame hue σ, O4. **Additive glow layer only** |
| **(a) GPT-image flipbook sheets** | single frames can match H1; fails O1 (double peak, R-C3-19), directionality (R-C3-28), boil (R-C3-28), grain-scale consistency (§1.5) | per-cell redraw; no timing control; radial compositions | INTERNAL C-3 ledger; Sprite Sheet Diffusion "still struggles…" (VERIFIED abstract); API `background: "transparent"` (VERIFIED) | Four directional silhouettes on transparent background → measure feature size in source px and hue across canvases. **Silhouette / mask source only** |

**Order** (DERIVED; consistent with Hades precedent): (c) → (d) → (b) glow-only → (a) masks-only.

### Internal corpus (T5) — what carries
- **`canonical/reap-die-rise-engine/vfx-pipeline.md`** — carries: one kit per family; cast → travel → impact → residual slots; ground-readable component per slot; premultiplied alpha; judging from the runtime camera. Dies: GPUParticles3D, decals, SubViewport dual view. ⚠ its D3 continuously-morphing noise conflicts with the flat planes seen in Hades II (E2/E4).
- **`agentic_orchestration/gandalf/vfx-feature-registry.md`** FF-01…15 — camera-agnostic families mapping to O-measures (lifecycle FF-11, effect-as-light FF-12, screen shake FF-07). ⚠ instruments `cv_width`, `sat_dist_norm`, `halo_softness` are **disqualified** (I-7) — do not reuse.
- **C-3 ledger** — socket tolerance 6 px; single-peak and final-alpha-0 checks; approved embers 6–14 particles, 0.8–1.6 s, 20–60 px/s, glow flicker 3–8 Hz ± 35 %.
- ⚠ **Canon conflict:** `style-register.md` says character scale 17 % and "Hades ~8 %"; measured Zagreus is **12.0 %** (130 px); the brief uses 12.5 %.
- **Matt's verdicts (judge axes):** R-C3-28 "no directionality… a stationary south-facing snowflake"; "alot of matte white/glow"; "choppiness on top of the smooth animation" · R-C3-83 (paraphrase) "too static — add particle fire" · L7 §12 "the floor portion of the aura doesn't follow"; "We dont need the cone" · R-32 "motion structure beats brightness", later amended to hue identity co-dominant.

---

## 6. Gaps
1. Hades II FX sjson not public; only Scripts (`ProjectileData_*.lua`) in a community repo — E2/E4 layer structure is footage-only.
2. Player-side Zeus attack-boon strike and Bloodstone cast travel not isolated in clean footage (Zeus-heavy video was a jump-cut montage; E1 is the Theseus Zeus bolt — same family, verified chain, enemy-cast); O7 speeds data-derived only.
3. Omega cast not found (green pentagram circles in the sampled Hades II window were Hecate's — E4).
4. E1 data vs footage: `LightningBoltZeusFx` 20 of 30 drawings (0.33 s) vs ≈ 4 visible frames; tail visibility and `DurationFrames = 0` semantics unverified.
5. Blend semantics of Hades group names (`_Add`, `FX_Dark`) inferred from names and black tints; no renderer definition; screen-shake units unknown.
6. Automated value-band counting not yet a valid instrument (difference masks exclude dark layers; hue-gated masks give 1–2 modes; O10 candidate-only, n = 4); § 2 J band counts are visual reads.
7. Extents partly clipped (bolt, pillar off-screen/ROI → heights are lower bounds); body heights from action poses × 1.1 (DERIVED).
8. Owners inferred: E2 splash (player-side, water) and the gold line-drawn shield effect not confirmed.
9. D2 speed conversion assumes shared Vel/RunVelocity units; a Frozen Orb footage check had multiple orbs — not completed.
10. Blocked: Gilland (primary); Blizzard/Riot bootcamp, Overwatch FX, RiME talks (video only); Hi-Fi Rush VFX breakdown (403); sakuga essays (403); Supergiant FX authoring medium (no primary).
11. Not opened: Transistor / Pyre data files (same SGG format, likely queryable); Silksong; Dust.
12. Hit-stop and shake data-only, not measured in footage.

---

## Sources (accessed 2026-09-14)
**Data:** [xuqifzz/hades-mod-tutorial](https://github.com/xuqifzz/hades-mod-tutorial) @7e06338 (`Game/Animations/Fx.sjson` and other animation files, `Game/Projectiles/{Player,Enemy,}Projectiles.sjson`, `Scripts/WeaponData.lua`, `Scripts/CombatPresentation.lua`) · [cevasonic/Hades-II-Mod](https://github.com/cevasonic/Hades-II-Mod) @eeae74c (`Scripts/ProjectileData_Melinoe.lua`) · [fabd/diablo2](https://github.com/fabd/diablo2) 1.13 (`Missiles.txt`, `Overlay.txt`, `CharStats.txt`)

**Footage (measurement only):** YouTube [ijwA_J29j1k](https://www.youtube.com/watch?v=ijwA_J29j1k) · [5WiYcx9SjZU](https://www.youtube.com/watch?v=5WiYcx9SjZU) · [-2b7GGWNz54](https://www.youtube.com/watch?v=-2b7GGWNz54) · [b5a-iIras34](https://www.youtube.com/watch?v=b5a-iIras34) · rejected [mx7HUJETVVY](https://www.youtube.com/watch?v=mx7HUJETVVY), [Tl93fMw5wkA](https://www.youtube.com/watch?v=Tl93fMw5wkA)

**Principles:** [LoL VFX Style Guide (Wayback)](https://web.archive.org/web/2017/https://nexus.leagueoflegends.com/wp-content/uploads/2017/10/VFX_Styleguide_final_public_hidpjqwx7lqyx0pjj3ss.pdf) · [Lyndon GDC 2018](https://gdcvault.com/play/mediaProxy.php?sid=1025417) · [ADVFX GDC 2017](https://gdcvault.com/play/mediaProxy.php?sid=1024715) · [HFR GDC 2024](https://gdcvault.com/play/mediaProxy.php?sid=1034330) · [Motomura GGXrd](https://www.ggxrd.com/Motomura_Junya_GuiltyGearXrd.pdf) · Sakuga Blog glossary · vfxapprentice blog

**Routes:** Godot docs [CanvasItemMaterial](https://docs.godotengine.org/en/stable/classes/class_canvasitemmaterial.html) · [CPUParticles2D](https://docs.godotengine.org/en/stable/classes/class_cpuparticles2d.html) · [SpriteFrames](https://docs.godotengine.org/en/stable/classes/class_spriteframes.html) · [godotshaders Wobbly](https://godotshaders.com/shader/wobbly-effect-hand-painted-animation/) · [VFXDoc alpha erosion](https://vfxdoc.readthedocs.io/en/latest/shaders/alpha-erosion/) · [RiME stylised VFX](https://simonschreibt.de/gat/stylized-vfx-in-rime/) · [80.lv EmberGen anime](https://80.lv/articles/making-anime-inspired-stylized-3d-explosions-with-jangafx-s-embergen) · [OpenAI image guide](https://developers.openai.com/api/docs/guides/image-generation) · [Veo docs](https://ai.google.dev/gemini-api/docs/veo) · arXiv [2501.03006](https://arxiv.org/abs/2501.03006), [2503.17934](https://arxiv.org/pdf/2503.17934), [2412.03685](https://arxiv.org/abs/2412.03685)

**Process (non-Hades):** [Schaefer D2 postmortem](https://www.gamedeveloper.com/design/postmortem-blizzard-s-i-diablo-ii-i-) · [Cuphead](https://www.gamedeveloper.com/art/animating-i-cuphead-i-the-verve-of-the-1930s-with-the-tech-of-now) · [Dead Cells (Vasseur)](https://www.gamedeveloper.com/production/art-design-deep-dive-using-a-3d-pipeline-for-2d-animation-in-i-dead-cells-i-) · [Unity Hollow Knight](https://unity.com/made-with-unity/hollow-knight) · [CoM postmortem](https://www.gamedeveloper.com/design/postmortem-children-of-morta) · [Phrozen Keep Missiles.txt](https://d2mods.info/forum/kb/viewarticle?a=364)

**Internal:** `canonical/reap-die-rise-engine/vfx-pipeline.md` · `canonical/reap-die-rise-story/style-register.md` · `agentic_orchestration/gandalf/vfx-feature-registry.md` · `agentic_orchestration/drax/notes/2026-07-31-vfx-bakeoff.md` · `astra_test_01/burst/runs/C-3/ledger.json` · `agentic_orchestration/legolas/research/2026-09-11-ai-tells-bibles-oracles/findings.md` · `agentic_orchestration/legolas/research/2026-09-13-hades-run-speed/findings.md` · `agentic_orchestration/research/vfx-p2-dossiers/`

**Scratchpad hygiene:** all footage deleted (~626 MB this session, plus the three Hades MP4s left by the 2026-09-13 session); downloaded PDFs/HTML deleted. Remaining text only: Hades data clone (19 MB), a Python venv, analysis scripts. Nothing from footage in the repo.
