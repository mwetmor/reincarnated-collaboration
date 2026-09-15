# Legolas Mode A — Chronicon · Children of Morta · The Slormancer: VFX atlas pull + oracle measurement (filed by gandalf)

> **STATUS:** CURRENT — research findings, Legolas (UNKNOWN-RESEARCHER), commissioned by gandalf (RUN-CONDUCTOR, Run C-3 VFX lane) per Matt 2026-09-15 (Chronicon → + Children of Morta → + The Slormancer). Commission: `agentic_orchestration/gandalf/requests/2026-09-15-legolas-chronicon-vfx-atlas-pull.md`. Filed verbatim from the sub-agent's text return. Samples (18; atlas now 72) live ONLY at `~/Games/vendor/vfx-atlas/` — study-only, never an image-model reference, never committed. Sub-agent ran serial, one decode at a time, peak ~190 MB RSS.

---

# Chronicon, Children of Morta and The Slormancer: VFX atlas pull (gandalf, Run C-3 VFX lane, 2026-09-14)

All three titles are done: 18 samples added (6 each), and the atlas now holds **72**. Every sample has been through our oracle and has the atlas traits filled in. `atlas.html` has been rebuilt and shows them. Nothing was written into the repo. Everything lives under `~/Games/vendor/vfx-atlas/`, which is study-only and never an image-model reference.

**Headline answers**
1. **Chronicon** draws its effects off the 3-px art grid, at screen resolution, with bloom. At its busiest it turns into a white-out: 22% of the frame is near-white.
2. **Children of Morta:** Matt's claim that its VFX read better holds up, but not for the reasons he listed. It barely uses white (0.1% near-white at its busiest), keeps saturation high, and puts a bright glow halo and floor light around each effect. It never darkens the ground and never outlines effects. Hue contrast against the ground is not a consistent rule.
3. **The Slormancer** is mixed, decided by measurement. Its signature shapes (the wave projectile, the summons) are pixel art on its 4-px grid, with flat banded colour steps. Fire bursts, novas, rims and lightning are soft and drawn at screen resolution. At full density it stays readable by avoiding white, lighting the whole room in the element's colour, and using black "void" shapes.

## 0. Method and host compliance
- **Plate.** Each sample was cut from a Steam trailer (1080p DASH chunks fetched directly; no full trailers downloaded) or one YouTube clip capped at 720p. Crops were streamed with `vid.sh`. Each crop was masked with the atlas hue formula plus exclusion boxes, then written as an exact-black plate in `plate/`, because the oracle rejects gameplay crops that aren't on a black plate.
- **Two instruments on the same plate.**
  - Atlas O1–O9 (the style measures defined in `findings.md`): `_tools/measure.py`, saved as `measures.json`.
  - Oracle: `python3 -m oracle.vfx_measure <plate> --fps <src> --plate black --body-h-px <bh> --ref oracle/vfx_reference_hades.json`, saved as `measure.json`.
- **Extra probes (scratchpad scripts, read-only):**
  - Art-grid test: gradient energy at the art-pixel period.
  - `edge.py`: edge hardness (`hard_share`) and flat-run share.
  - `bgdim.py`: brightness of the 2–8 px ring around the effect vs the ground.
  - Common-gate screen coverage.
  - Effect hue vs ground hue.
- **Guardrails held.** Strictly serial, no sub-agents, one decode at a time. The largest process measured was about 190 MB RSS. All downloaded clips were deleted after cropping. The watchdog never fired.
- **Evidence classes:** VERIFIED (primary read) / MEASURED (instrument or visual read) / PRACTITIONER-REPORT / INFERRED.
- **Capture caveats (MEASURED):**
  - Chronicon's trailer is a 60 fps container, but about half its frames are duplicates, so real content is about 32–36 fps. Frame counts are roughly double the drawings; ms values are still valid.
  - Children of Morta's trailers are 30 fps (the "11 facts" trailer has 31% duplicates).
  - Slormancer's trailer is true 60 fps.
  - Everything is lossy h264, which puts artefacts at 4- and 8-px spacing. The Slormancer ×4 grid call leans on a nearest-neighbour zoom for that reason.
- **Body heights:**
  - Chronicon: 81 px (MEASURED, ±10%).
  - Children of Morta: 90 px (INFERRED from a crouched ~65 px sprite, ±15%).
  - Slormancer: 70 px (MEASURED, ±15%).
  - Hades: 115–120 px (existing oracle).

## 1. Samples (all accessed 2026-09-14)
Every folder `samples/<id>/` has `frames/`, `plate/`, `loop.webp`, `contact.png`, `meta.json` (source URL, trailer time, fps, crop, body height), `measures.json`, `measure.json` and `record.json`. The schema matches the existing samples, with `plate/` and `measure.json` added.

**Chronicon (Subworld, Steam 375480).** Launch Trailer, Steam movie 256812623, 1080p60, unless noted.

| id | Trailer time | Content | Reliability |
|---|---|---|---|
| `chronicon-projectile` | 16.05–16.85 s | yellow star-tipped bolts with sparkle trail, sunburst impact | MEDIUM |
| `chronicon-aoe-burst` | 105.05–105.82 s | fill-disc flash, flame-petal ring nova, radial yellow ray fan | MEDIUM |
| `chronicon-chain` | 78.10–79.10 s | white-cyan jagged arcs, white impact discs, black pixel smoke | LOW-MED |
| `chronicon-ground-field` | 84.00–85.00 s | tiled flame sprites on a lava-crack decal; skill INFERRED to be a Blaze-type trail | LOW-MED |
| `chronicon-summon` | YouTube `Za2J_HYT7v4` (720p60), 50.25–51.25 s | cyan spectral minion pack from a Warlock summoner build | LOW |
| `chronicon-density-ceiling` | 112.00–113.00 s ("Extreme endgame builds") | hundreds of white star sprites plus bloom | MEDIUM for coverage |

**Children of Morta (Dead Mage, Steam 330020).** "11 facts" = movie 256915020; Co-Op = movie 256873778; both 1080p30.

| id | Source and time | Content | Reliability |
|---|---|---|---|
| `children-of-morta-projectile` | Co-Op 43.10–44.30 s | red-orange fireball volleys | LOW-MED |
| `children-of-morta-aoe-burst` | 11 facts 107.20–108.30 s | charge, starburst, screen-filling cyan mandala, dark fragments | MEDIUM |
| `children-of-morta-beam` | 11 facts 101.85–103.05 s | room-wide magenta wavy laser lattice with glow bands | MEDIUM |
| `children-of-morta-ground-field` | 11 facts 89.40–90.80 s | purple dome with glyph lattice, full lifecycle | MEDIUM |
| `children-of-morta-summon` | Co-Op 61.90–62.70 s | translucent mint spectral figure, lights the floor | LOW-MED |
| `children-of-morta-density-ceiling` | Co-Op 46.40–47.60 s | 4-player chaos; densest moment in the three trailers | MEDIUM |

**The Slormancer (Slormite Studios, Steam 1104280).** Release Trailer, movie 257130346, 1080p60.

| id | Trailer time | Content | Reliability |
|---|---|---|---|
| `slormancer-projectile` | 72.85–73.85 s | screen-wide flat banded wave-beam with white core | HIGH for timing/edges |
| `slormancer-aoe-burst` | 46.08–46.95 s | white starburst, chained spiky blue novas; onset cut by trailer | LOW-MED |
| `slormancer-beam` | 70.00–71.00 s | thin blue tether, violet chain lightning, fading ice spikes | LOW-MED |
| `slormancer-ground-field` | 34.40–35.60 s | black void disc pools with purple rims | LOW-MED; mask tracks rims only |
| `slormancer-summon` | 93.20–94.20 s | pixel lilac spectral minions plus crescent guard | MEDIUM |
| `slormancer-density-ceiling` | 29.30–30.30 s | room-filling fire explosions, room lit orange | MEDIUM |

## 2. Measurements (MEASURED unless marked)

### 2a. Per sample: oracle `measure.json` (life/half from the oracle; "c" = censored lower bound) plus atlas O7 speed

| id | rise f / ms | half ms | life ms | white core at peak / max, order | hue SD° / mean° | S bright15 / dim25 / median | width × height (body heights) | L* modes (O10) | residue |
|---|---|---|---|---|---|---|---|---|---|
| chron-projectile | 14 / 233 | 67 | 417 | .00 / .65 core-last | 7.4 / 55 | .52/.69/.54 | 3.3×2.9 | 1 | .02 |
| chron-aoe-burst | 7 / 117 | 83 | 533 | .02 / .70 core-last | 10.3 / 52 | .75/.75/.70 | 10.8×8.9 | 1 | .12 |
| chron-chain | 19 / 317 | 67 | 600 | .56 / .90 core-last | 5.7 / 184 | .03/.38/.15 | 6.0×5.2 | 2 | .50 |
| chron-ground-field | 26 / 433 | – | >800c | .16 / .19 | 9.0 / 37 | .37/.68/.58 | 11.1×6.0 | 2 | .84 |
| chron-summon | 23 / 383 | – | >1000c | .14 / .26 | 7.1 / 178 | .78/.89/.85 | 17.7×8.8 | 2 | .54 |
| chron-density | 21 / 350 | – | >1000c | **.93** | 6.4 / 51 | **.05/.06/.04** | 14.8×8.6 | 1 | .89 |
| CoM-projectile | coverage | – | >1200c | .00 / .11 | 14.0 / 4 | .76/.80/.83 | 12.4×7.7 | 1 | .70 |
| CoM-aoe-burst | 7 / 233 | 133 | 500 | .25 / .70 core-last | 4.8 / 170 | .15/.55/.45 | 16×10 (exceeds crop) | 3 | .07 |
| CoM-beam | holds | – | >1200c | .00 / .01 | 14.5 / 336 | .77/.78/.75 | 11.1×6.9 | 2 | .83 |
| CoM-ground-field | 6 / 200 | 600 | 1000 | .00 / .68 core-last | 6.6 / 270 | .60/.83/.79 | 3.4×5.4 | 3 | .00 |
| CoM-summon | 17 / 567 | – | >800c | .00 / .01 | 5.5 / 156 | .64/.64/.65 | 7.8×5.5 | 4 | .96 |
| CoM-density | coverage | – | >1200c | .08 / .24 | **48.7** / 311 | .41/.98/.95 | 14.5×8.6 | 2 | .88 |
| slorm-projectile | wave full in 1 drawing (frames 22→23 = .13→1.0) | 150 | 583 | .00 / .02 | 9.0 / 205 | .71/.83/.81 | 14.4×5.3 | 4 | .02 |
| slorm-aoe-burst | 10 / 167 (onset truncated) | 200 | >867c | .01 / .03 | 9.0 / 210 | .53/.74/.66 | 15.1×10.4 | 1 | .67 |
| slorm-beam | 2 / 33 | 233 | 700 | .00 / .54 | 4.9 / 189 | .65/.65/.66 | 11.7×8.1 | 1 | .20 |
| slorm-ground-field | rims build | – | >1200c | .02 / .12 | 6.5 / 270 | .51/.54/.53 | 8.7×6.2 | 2 | .52 |
| slorm-summon | persistent | – | >1000c | .15 / .18 | 9.5 / 275 | .11/.55/.52 | 13.2×6.0 | 4 | .96 |
| slorm-density | 25 / 417 | – | >1000c | .01 / .02 | 8.8 / 34 | .63/.77/.70 | 15.6×11.4 | 2 | .72 |

**Oracle vs the Hades reference (descriptive only).** No sample lands in the fast-strike rise band (0–1 frames), except Slormancer's wave (1 drawing from onset) and its beam spikes (2 frames). No sample hits the Hades decay curve past its first point. The Hades hue band is only met by chron-projectile, chron-aoe, CoM-beam, CoM-projectile and slorm-density.

### 2b. Five-column comparison

Hades and D2R columns come from `vfx_reference_hades.json`, the oracle findings E1/E2/E4/E5, and the atlas records `hades2-*` and `d2r-frozen-orb`.

| Measure | Chronicon | Children of Morta | Slormancer | Hades / II | D2R |
|---|---|---|---|---|---|
| Art pixel : screen at 1080p | **3** (VERIFIED dev post; MEASURED scene 3-px period 1.22–1.78) | **~3** (MEASURED weak: sprite 3/6-px period 1.27–1.28, 8× zoom); dev report says "about 4×" (PRACTITIONER-REPORT). **Conflict, not averaged** | **4** (MEASURED: 4-px period 2.6× on a calm frame, 4-px staircase in zoom; shares codec periods, so zoom-backed) | n/a, HD painted | n/a, 3D |
| Effects on the art grid? | **No**: effect 3-px period 1.03–1.09 vs scene 1.22–1.78 | **Partly**: dome lattice and mandala 1.24–1.25 (scene 1.07–1.14); glows, bolts, beam ~1.0 | **Mixed**: wave (4-px period 2.3×, flat share .93) and summons (5.4×, hard .68) on grid; fire, novas, void rims soft (hard .01–.08) | HD painted flipbooks (VERIFIED Fx.sjson) | 3D particles |
| Edge `hard_share`, effect (scene) | .00–.24 (.18–.37) | .00–.37 (.19–.42) | .01–.68 (.13–.43) | not run | not run |
| Rise, isolated bursts | 117 ms (7 frames, about 4 drawings) | 200–233 ms | 1 drawing (wave), 33 ms (spikes), 167 ms (novas) | E1/E4: 0–1 frames; E2 body +6 frames | continuous recast |
| Area halves in | 67–83 ms | 133 ms (burst), 600 ms (dome) | 150–233 ms | 2–7 frames (33–117 ms) | n/a |
| Visible life | 417–600 ms | 500–1000 ms | 583–700 ms | E1 67 ms; E2 270–330 ms; E4 body 5–6 frames + residue ≥0.8 s | n/a |
| White core at peak (max) | .00–.56 (to .93), mostly core-last | .00–.25 (to .70 in bursts; glows ≈0) | **≈0** (.00–.15) | .13–.40, E2 flash-first / E4 core-last | .14–.31 |
| Hue SD at peak | 5.7–10.3° | 4.8–14.5° (density 48.7°) | 4.9–9.5° | 10–18° (oracle); 8.9–14.1° (atlas) | 6.5° (atlas); 11–31° (oracle) |
| Median S, effect | .04–.85 (white-heavy holy/lightning) | .45–.95 | .52–.81 | .74–.86 | .18–.38 |
| L* modes (O10, inspect only) | 1–2 | 1–4 | 1–4 | 2 | 1 |
| Width at peak (body heights) | 3.3–10.8; density 14.8 | 3.4–16 | 11.7–15.6 | 0.7–5.4 | ~6 by px, no body height |
| Glow ring vs ground / effect vs ring (V) | +.12–.32 / +.26–.50 | +.09–.41 / +.10–.55 | +.12–.30 / +.19–.29 | not run (gap) | not run |
| Densest moment: near-white share of crop | **22% median** | **0.1%** (max 2%) | **0.1%** | – | – |
| Densest moment: bright-effect coverage | 38% (grass inflates) | 4.5% (max 11.6%) | 18.8% (max 24%) | – | – |
| Dark separation | opaque black pixel smoke, scorch blobs under flames | none on effects; foreground rocks occlude effects; characters have dark pixel rims | **black void discs**, dark character outlines, unlit dark rooms | FX_Dark duplicates (VERIFIED: 56 of 78 dark sheets also drawn additive) | none |
| Ground during casts | no darkening | **brightens** (scene V +.07 to +.09 for burst and summon) | rooms lit in the element's colour (fight room V .45 vs ~.15 unlit) | nova/decal/light disc layers (VERIFIED) | light pool |
| Effect hue vs ground hue at peak | 25–146° | 6–165° (not consistent) | 2–11° in lit rooms; 76–77° in dark rooms | – | – |
| Content fps in trailer | ~32–36 effective | 21–30 | 57–60 | 60 | 60 |

### 2c. Children of Morta: how effects stay readable over detailed painted ground
Matt asked specifically about this.
- **Dark separation or outline on effects: absent.** MEASURED: the dark-edge check is false on all 6 samples, and edge brightness is at or above the interior on the dome and mandala. What CoM does instead is a **bright soft glow halo**: the ring around the effect sits +.16 to +.41 above the ground. Foreground rock sprites overlap the dome (MEASURED visual), so effects are depth-sorted into the scene rather than pasted on top.
- **Local light layer: present.** MEASURED: the summon lifts ground brightness from .24 to .31 and green-lights the floor tiles; the mandala lifts it from .18 to .27; fireballs spill red light onto the violet floor. This matches Dead Mage's public account of HD lighting over pixel sprites (§3).
- **Ground darkening during casts: not observed.** MEASURED: ground brightness rises or holds in every sample.
- **Effect grid vs scene grid:** the pixel-drawn shape layers (glyph lattice, mandala ornament) sit on a ~3-px grid. Glows, beams and bolt halos are smooth HD (MEASURED weak). INFERRED: pixel "shape" sprites plus HD light and glow.
- **Palette contrast per element: not a rule.** Effect-to-ground hue distance ranges from 6° (mint summon on a green room) to 165° (cyan mandala on brown). The magenta beam reads on light ochre sand by hue with almost no value step: effect over ring is only +.10. INFERRED: CoM carries legibility by **saturation plus a bright halo plus no white**, with hue contrast taken opportunistically per biome.

### 2d. Slormancer: painted or pixel?
**Both** (MEASURED, one caveat: codec artefacts share the 4-px period, so the 4-px period ratios alone are not proof; the nearest-neighbour zooms and flat shares carry the call).
- **Signature skill shapes and summons are pixel art on the ×4 grid, with painterly-flat banded value work.**
  - The wave has 3 flat bands (dark blue / cyan / white), a 4-px staircase edge, flat-run share .93, and 4-px period 2.3× (12-px period 3.1×).
  - Summons show hard_share .68 and 4-px period 5.4×.
- **Explosions, novas, rims and lightning are not pixel.** They are soft, screen-resolution, additive particles: fire hard_share .013, novas .047, void rims .076. Lightning strokes are 1–3 screen px, which is thinner than one art pixel.

**How it holds legibility across the screen at full density (MEASURED; mechanism INFERRED):**
- Almost no white anywhere: 0.1% near-white even with 19–24% of the crop covered by bright effect.
- Effects stay saturated (median S .52–.81).
- Each fight room is lit in the element's colour, so the ground takes the effect's hue (2–11° apart) and the effects separate by brightness (ring +.19 to +.30, effect over ring +.19 to +.29).
- Black void shapes and the dark pixel outlines on characters supply the negative contrast.

## 3. Process notes

**Chronicon / Subworld**
- **Engine.** GameMaker: Studio 1.4 (VERIFIED, dev Squarebit, Steam thread, 2018-03-19). Ported to GMS 2.1.5 in 0.82.0 (VERIFIED patch notes, 2018-09-22; the same patch "Improved visuals of lights, glow, and bloom effects").
- **Grid.** The game view is 640×360, "enlarged to pixel perfect resolutions: 1280x720 (x2) 1920x1080 (x3)" (VERIFIED, Squarebit, 2017-03-15, Steam thread 135511455874163822; restated 2021-03-13 in 4627984302698151568). Effects are drawn off that grid (MEASURED, §2b).
- **Shaders.** Heat distortion, water ripple and glow/bloom sliders (VERIFIED 0.75.1, 2018-03-20). Post-processing "bloom, heat effect, water/lava" (VERIFIED 1.20.0, 2021-03-24).
- **Particles.**
  - A "Particle Intensity" setting added "to reduce particle clutter" (VERIFIED 1.20.0).
  - A "reverse nova" particle type (VERIFIED 0.96.2, 2020-01-22).
  - Auto-cleanup of on-hit visuals "if there are very many" (VERIFIED 1.0, 2020-08-21).
  - Blending retuned "to produce better, less over-saturated, light blending" (VERIFIED 1.53.0, 2025-08-27). **Our footage predates this**, so the measured white-out may be lower in the current build.
- **Screen shake.** A Screenshake Intensity option exists (PRACTITIONER-REPORT, community post, 2017-05-24). Per-skill reductions: Detonation (VERIFIED 1.0) and Leap (VERIFIED 1.20.0).
- **Hit-stop:** no source found.
- **Damage numbers.** Depth-sorted with auto-cleanup (VERIFIED 1.0).
- **Additive blending.** Footage read (MEASURED visual).
- **Palette rules per element:** no source. INFERRED from measured hue means: fire/holy 37–55°, lightning/cold 178–184°, holy/lightning heavy on white.
- **Team.** Solo developer until 2021 (VERIFIED, subworldgames.com/about).
- All patch notes come from the Steam news API for app 375480.

**Children of Morta / Dead Mage**
- **Unity.** VERIFIED: their Hierarchical Finite State Machine tool was built "within Unity Editor", and a "customized rendering pipeline that helped us integrate some unique lighting techniques with a standard 2D pixel art pipeline" (Amir Fassihi, Game Developer postmortem, 2020-11-02).
- **"Puppets" and "about 4×".** Pixel animations "stretched… about 4 times" to HD with "high-res dynamic lights… The puppets are pixelated but we shine them with real lights": PRACTITIONER-REPORT. I only saw this in a search summary of TechRaptor; the page returned 403 and I could not read it. It conflicts with my ~3× measurement.
- **Engadget.** "layered with lighting effects and shadows" (VERIFIED, Engadget, 2018-03-22).
- **Hand-drawn frames.** "Every frame… drawn by hand" (VERIFIED, postmortem).

**The Slormancer / Slormite Studios**
- **Engine.** "Made with GameMaker: Studio 1.4" (VERIFIED, dev "Ashmore", Steam FAQ, 2020-06-24). Later GMS2 migration and #GameMaker tagging: PRACTITIONER-REPORT (search summaries only).
- **Release.** 1.0 on 2025-05-13 (VERIFIED, Steam API).
- **Team.** Two people, Nice, France (PRACTITIONER-REPORT, presskit via search summary).
- **×4 grid and mixed pixel/soft effects:** MEASURED only. No developer statement on VFX found.

## 4. What carries to a painted-pixel register (64–128 px native, over painted backgrounds)
The part that carries is Children of Morta's and Slormancer's split: **pixel-drawn shape sprites on the art grid, with the glow, light spill and fade on a separate HD layer.** The pixel shape keeps the silhouette sharp against busy painted detail, and the light layer ties the effect into the ground instead of pasting it on top. Take Slormancer's **flat 2–4-band value ramps with almost no white**, which kept its densest moment readable at 19–24% effect coverage. Take CoM's **bright halo plus floor light** (+.16 to +.41 around effects).

What breaks:
1. **Chronicon-style white bloom stacking.** At 22% near-white it erases enemies, and over painted ground it would erase the painting too.
2. **Effects drawn off-grid at screen resolution next to pixel characters.** Chronicon's effects do this; it mixes two resolutions and softens edges once our backgrounds carry more detail.
3. **Relying on hue contrast.** CoM's own hue distances run 6–165° and Slormancer tints rooms to the effect hue. Over a detailed painted ground the separation has to come from brightness (halo, white-free banded cores, or a black shape like Slormancer's void discs), not from hue.
4. **Density vs contour.** At 64–128 px native a character is only 64–128 art pixels tall, while these effects span 10–16 body heights at peak. A screen-filling mandala or fire carpet leaves nothing for a painted contour to hold. Cap burst width at roughly 3–6 body heights (Hades' range) and keep the full-screen ornaments as rare punctuation.

## 5. Gaps
1. All footage is lossy trailer video with edited cuts and frame duplication. Rise/onset is truncated on several samples (marked); summon and density lifecycles are censored; `slorm-ground-field` masks only the rims, not the black pools.
2. The pixel-vs-soft call relies on 4-px periods that h264 also produces, so zoom backs it. A lossless capture or an asset rip would settle it; both need a purchase or install.
3. Children of Morta's art scale conflicts: my ~3× vs the reported ~4×. The Unity blog and TechRaptor pages were unreadable (404/403), and the Wayback Machine was rate-limited.
4. Chronicon's footage predates its 1.53.0 blending change.
5. No hit-stop or screen-shake measurements for any title. No developer VFX statements for Chronicon (beyond patch notes) or Slormancer.
6. The ring/edge/hue probes were not run on Hades or D2R (no frames or plates kept for D2R), so those rows are blank.
7. No Chronicon trailer footage of a true chain skill, and no Slormancer or CoM ground DoT with a full lifecycle.
8. The atlas store grew from ~385 MB to 1.4 GB, because `frames/` and `plate/` are kept per the brief; the disk has 24 GB free. I also left a few scratch PNGs and an empty `mtmp/` in `_work/` (the deletion was blocked).
9. Sources I relied on for developer statements: Steam threads [375480/…/2949168687320829309](https://steamcommunity.com/app/375480/discussions/0/2949168687320829309/), [4627984302698151568](https://steamcommunity.com/app/375480/discussions/0/4627984302698151568/), [1291817208482158876](https://steamcommunity.com/app/375480/discussions/0/1291817208482158876/), [1104280 FAQ](https://steamcommunity.com/app/1104280/discussions/0/2552901289730292846/); [Subworld about](https://www.subworldgames.com/about/); [CoM postmortem](https://www.gamedeveloper.com/design/postmortem-children-of-morta); [Engadget 2018](https://www.engadget.com/2018-03-22-children-of-morta-hands-on-indie-xbox-gdc.html); [TechRaptor](https://techraptor.net/gaming/previews/how-dead-mage-created-art-for-children-of-morta) (unread, 403); [Slormite presskit](https://www.slormitestudios.com/presskit); Steam store/news APIs for 375480, 330020, 1104280.

Files are in `/Users/admin/Games/vendor/vfx-atlas/`:
- `atlas.json`
- `atlas.html`
- `samples/chronicon-*`
- `samples/children-of-morta-*`
- `samples/slormancer-*`
- `_work/traits_chronicon.json`
- `_work/traits_com.json`
- `_work/traits_slorm.json`
