# RUN KC2-PM4 — Lap H — contact-response camera decode

**Agent:** legolas (UNKNOWN-RESEARCHER) · **Conductor:** gandalf (RUN-CONDUCTOR) · **Ruling:** R-PM4-10
**Date:** 2026-08-13 · **Discipline:** GL-12 decode-never-estimate · NOTE-9 basis discipline · read-only on `/Volumes/reincarnated/`

---

## VERDICT — **UNDECIDABLE**

The contact RESPONSE fork (RESPONSE-1 "block-and-dwell" vs RESPONSE-2 "push-apart / lateral
resolution") **cannot be decided** from the reference footage against the pre-registered rubric.

Pre-registered rule: *≥3 independent pack-convergence episodes classified consistently one way with
0 contrary → that response is MEASURED; mixed or <3 decidable episodes → UNDECIDABLE (do NOT force it).*

**Result: 0 episodes OBS-A · 0 episodes OBS-B · 6 episodes UNDECIDABLE.** The rule fires UNDECIDABLE.
Per the charter that HALTs the run to Matt. **The fork is not resolved by this lap.**

This is a clean negative, not a failure to look: six episodes were extracted, motion-compensated and
read frame-by-frame, with three named, reproducible confounds established as the cause.

---

## File pins (SHA-256)

| file | sha256 | role |
|---|---|---|
| `/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-2/video/eor-warlord-wave-150-160-2026-08-05 21-37-25.mp4` | `4c60960d98e9d729e17469044dbe7b4341b253d7d36ba26fe09564d6056a4de8` | **reference footage — the fight of record** |
| `/Volumes/reincarnated/visual-artifacts/GD-matt-test/eor-test-1/video/eor-warlord-2026-08-04 21-09-31.mp4` | `cc428e944aa385e3cd147140b6271401947a2a98390157b6b3e7df427fe01155` | supplementary (PINNED ONLY — **not used**, see § Provenance) |

Reference footage: 1920×1080, h264, 60 fps, 62 046 frames, 1034.10 s, 479 438 089 bytes.

---

## Fight window located (measured, in-frame)

The reference fight occupies **video t ≈ 683.0 → 866 s**; everything before is pre-run.

| observation | t (video) | basis frame |
|---|---|---|
| Lokarr dialogue open, **"Start on Wave 150"** highlighted, run timer `00:00`, wave counter `0` | 682.00 | `evidence/ref-00-runstart-682.00.jpg` |
| wave counter reads **151** | 688 | wave-counter crop (`crop=140:90:1560:105`) |
| wave counter reads **160** | 840–842 | `evidence/E6-842.00.jpg` |
| player HP falling 9 296/20 005 | 862 | `evidence/ref-98-hpfalling-862.00.jpg` |
| **post-death**: player back at Lokarr's throne, HP 18 065/**18 065** (buff-set max, i.e. re-entered), energy 2 576/2 576 | 872.00 | `evidence/ref-99-postdeath-872.00.jpg` |

⇒ death lies in **864 < t_death < 872**; fight length ≈ **181–189 s**, consistent with the Lap C
measured reference truth of **186 s** and with the charter's 682→868 window. Wave-counter
transitions measured in-frame at 4 s sampling: 151@688 · 152@700 · 153@720 · 154@732 · 155@744 ·
156@756 · 157@780 · 158@800 · 159@816 · 160@840.

UI legend (wave counter, run timer, tribute, score multiplier) — `evidence/ref-01-ui-legend-700.00.jpg`.

---

## Episode table

Full rows with basis strings in `pm4h_episodes.csv`.

| episode | t (s) | wave | n monsters (approx) | max simultaneous melee contact (LOWER BOUND) | class |
|---|---|---|---|---|---|
| PM4H-E1 | 689.0–694.0 | 151 | 6–9 | ≥3 | UNDECIDABLE |
| PM4H-E2 | 770.0–774.0 | 156 | 8–12 | ≥2 | UNDECIDABLE |
| PM4H-E3 | 810.5–813.25 | 158 | 6–10 | ≥2 | UNDECIDABLE |
| PM4H-E4 | 779.0–784.0 | 157 | 10–14 | ≥3 | UNDECIDABLE |
| PM4H-E5 | 813.0–817.0 | 158–159 | 8–12 | ≥1 living (≥4 bodies incl. corpses) | UNDECIDABLE |
| PM4H-E6 | 838.0–846.0 | 159–160 | 10–16 | ≥2 | UNDECIDABLE |

**Basis for every contact count (NOTE-9):** "in melee contact" was counted as *a monster sprite whose
body edge abuts the player sprite in the named frame*. Every count is a **LOWER BOUND**, because the
player's own skill VFX bloom and the floating damage-number stack occlude precisely the annulus where
contact occurs. No count should be treated as a parameter; they are descriptive evidence only.

**Wave numbers** were read from the on-screen Crucible wave counter **in the same frame as the
episode**, not interpolated.

---

## Why UNDECIDABLE — the three confounds (each reproducible)

**C1 — corpse carpet.** Grim Dawn leaves monster corpses on the floor and they accumulate. By wave
~155 the arena floor is carpeted with them (`evidence/confound-C1-corpsecarpet-748.00.jpg`). A body
that holds position for seconds — the exact signature the rubric asks me to read as "inert blocked
rear rank" — is *indistinguishable in stills* from a corpse. PM4H-E3 is the sharpest case: the camera
is measured **static** over 810.50–813.25 (terrain pixel-identical between `E3-810.50.jpg` and
`E3-812.00.jpg`) and a clump of ≥4 bodies is **completely motionless for 1.5 s** — which reads as
textbook OBS-B until you notice every one of them is sprawled/prone and none carries a health-bar.
`evidence/E5-814.00.jpg` shows the player and a live hero standing **on top of** that same clump.

**C2 — VFX overdraw at the contact ring.** The build is an EoR Warlord; the player's own effects
plus the floating damage-number stack saturate a radius of roughly ±200 px around the player in the
majority of frames. That annulus *is* the contact ring. Adjacency between two bodies 1–2 m apart is
simply not resolvable there for most of the fight. (Compare the readable `evidence/E4-783.00.jpg`
against the typical `evidence/confound-C2-vfxoverdraw-697.00.jpg`.)

**C3 — terrain inside the engagement zone.** The Crucible arena floor carries raised platforms, step
blocks, pillar bases and Blessing/Banner totems standing inside the melee zone
(`evidence/E2-771.00.jpg`, `evidence/E4-781.00.jpg`). A monster that stops short may be terrain-blocked,
not body-blocked. Nothing in the footage separates the two.

**C4 — the episode definition is not instantiated by this content.** The rubric's episode is *"a pack
of ≥5 monsters converging on the player from one direction."* Crucible spawns from multiple points
around a circular arena and Matt repositions constantly, so bodies arrive on 3–5 distinct bearings at
once. A saturated surround **is** present throughout (E4, E6) — but under multi-point spawn geometry
a surround is not evidence of lateral resolution, because no lateral resolution was required to
produce it. The RESPONSE-2 signature and the arena's spawn design are confounded by construction.

---

## Method (reproducible)

1. `ffprobe`/`ffmpeg` (`/opt/homebrew/bin`), read-only on the share. Frames written as JPEG (the
   image reader downsamples large PNGs; JPEG at q4–q5 renders near-native and is what made body-level
   reading possible at all — recorded as a working note).
2. Coarse 1/10 fps contact sheets → located the combat block; wave-counter crop
   (`crop=140:90:1560:105`) sampled at 1/4 fps → wave-transition map.
3. **Camera-motion decode.** 4 fps grayscale frames (`crop=1920:760:0:100,scale=480:190`),
   luminance-clipped at 70 to suppress VFX, Hanning-windowed, **phase-correlated** pairwise. Output:
   per-frame camera translation for the whole fight → `method/camera_motion_4fps_683-866.npy`
   (columns: t, dx, dy in 480-space = ¼ native, correlation peak).
   - Gave the **static-camera windows** used for E3 (zero-displacement runs: 699.25–700.50,
     745.75–747.00, 771.25–772.50, 779.00–780.25, 810.50–813.25, 865.25–866.50).
   - Gave the **motion-compensated ("stabilized") crops** used for E2/E4
     (`method/stab_motion_compensate.py`) — world-fixed views in which only bodies move.
4. Player-relative crops (`crop=800:640:560:220`) for contact-ring reads; wide crops
   (`crop=1400:1000:260:60`) for bearing distribution.

**Self-corrections made during the lap (recorded per GL-12):**
- First phase-correlation pass (no luminance clipping) reported a 3.00 s static window at 812.00–815.00.
  Visual check falsified it — terrain had clearly moved by 814.0. Re-run with VFX suppression
  narrowed the true window to 810.50–813.25. The falsified pass is not used anywhere in the findings.
- Peak-translation magnitudes from phase correlation run ~30 % high: the 732.50–732.75 event was
  estimated at 318 native px/0.25 s, and direct landmark measurement on the two frames
  (`evidence/tertiary-dash-732.50.jpg` / `-732.75.jpg`, tracking the `94,059/94,059` nameplate) gives
  **≈236 px/0.25 s**. All translation figures in this file are therefore reported as *measured
  camera-translation rate with ±30 % method uncertainty*, not as speeds.
- An initial attempt to track bodies with a fixed off-centre crop was abandoned: the
  camera follows the player, so an off-centre fixed crop samples different world content each frame.
  Superseded by the player-relative and motion-compensated views.

---

## Tertiary observations (logged, NOT ruled)

**(a) High-speed player traversal (dash / charge).** 99 intervals in 683–866 s carry camera
translation ≥80 native px per 0.25 s. The largest, i.e. the strongest dash candidates:
`732.50–732.75` (verified by landmark: ≈236 px/0.25 s, ground charge-trail visible in
`evidence/tertiary-dash-732.75.jpg`), `821.75–822.75`, `825.75`, `820.75`, `844.25`, `847.75`,
`755.25`, `802.00`. Bearing on the run's movement-while-channeling / directional-motion limbs:
the reference fight contains **frequent** high-speed repositioning, not a pinned player.

**(b) Monster–monster interpenetration.** Between **living** bodies: **not observed** in any
low-VFX frame examined (`E4-782.00.jpg`, `E4-783.00.jpg`, `E5-814.00.jpg`, `E5-815.00.jpg`) — living
bodies abut but do not visibly overlap. This is *consistent with* the non-overlap invariant (R-PM4-8)
for living bodies, and is offered as corroboration only, not as a measurement. Between living bodies
and **corpses**: overlap is total and routine (`evidence/E5-814.00.jpg` — the player and a live hero
stand on a pile of prone bodies). **Corpses carry no footprint.** If the sim's non-overlap invariant
applies to dead bodies, that is a divergence from the reference.

**(c) A monster standing inside the player's footprint.** One candidate, flagged **uncertain**:
`evidence/E4-782.00.jpg`, where the ogre-form body carrying bar `205,997/233,250` sits with its
nameplate directly beneath the player's, its sprite overlapping the player's screen position. The
isometric projection makes "overlapping in screen space" and "co-located in world space"
indistinguishable here. Not asserted.

---

## Provenance — `eor-test-1` (NOT used)

Pinned above so the lap is reproducible, and **deliberately not drawn from**. The pre-registered rule
requires the verdict to stand on `eor-test-2` alone with `eor-test-1` as corroboration only. Since
`eor-test-2` yields zero decidable episodes, corroborating episodes from a prior sitting cannot move
the verdict off UNDECIDABLE — and mining a second sitting after a negative on the reference footage
would be selecting substrate against an outcome. Not done.

---

## What would decide the fork (for the conductor, not a recommendation on the fork itself)

Named plainly because "UNDECIDABLE" is only useful if the boundary is legible:

1. **A clean-board capture.** One or two Crucible waves recorded with player VFX minimised (or a
   low-VFX skill), no potion/aura clutter, player deliberately stationary for 4–5 s while a pack
   converges. Every confound above except C1 dissolves; C1 dissolves too on an early wave with an
   uncluttered floor. This is a **Matt-action** item (it needs a playtest, not a decode).
2. **Game-file decode of the collision/steering data.** Lap F already declared C-F2/C-F6 gaps in the
   game tables; whether a *steering/avoidance* record exists separately from the *body radius* record
   was not exhausted. This would be a fresh legolas lap, not a re-read of Lap F.
3. **Conductor ruling by declaration.** If neither of the above is affordable, the response is a
   *declared* model limb with a named caveat travelling downstream — the honest alternative to
   choosing by outcome, which Law 3 bars and which gamora correctly refused.

---

## Layout

```
2026-08-13-kc2-pm4-lap-h-contact-response/
├── README.md                  ← this file (verdict + episode table + pins + method + self-corrections)
├── pm4h_episodes.csv          ← one row per episode, with basis strings
├── evidence/                  ← 21 classified frames carrying the verdict
└── method/
    ├── stab_motion_compensate.py          ← motion-compensated crop generator
    └── camera_motion_4fps_683-866.npy     ← per-frame camera translation, whole fight
```

Scratch extraction (~168 MB of intermediate frames) was written to a `work/` directory and deleted
after evidence selection; every frame in `evidence/` is regenerable from the pinned video with the
crop specs recorded above.
