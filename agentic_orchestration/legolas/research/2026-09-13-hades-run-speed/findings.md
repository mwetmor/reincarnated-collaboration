# Hades run speed — scale-free, for the Keeper's movement tuning

> **STATUS:** CURRENT — legolas Mode A research (commissioned by gandalf, RUN-CONDUCTOR, Run C-3, for Matt's "tune to Hades run speed, walk as a ratio"). Filed by gandalf verbatim from the agent's return (the harness blocked the sub-agent's own write). Evidence classes: VERIFIED (primary source read) · MEASURED (method stated) · DERIVED · PRACTITIONER-REPORT.

**Headline:** Zagreus runs **≈ 3.9 of his own body-heights per second**. For the 130-px Keeper that is **≈ 510 px/s — 3.8× our current 135 px/s.** Zagreus fills nearly the same share of the screen as the Keeper (12.0 % vs 12.5 %), so the body-height and screen-height routes agree; the data files and the footage agree too (540 engine units/s ≈ 511 px/s at 1080p).

## TL;DR

| Game | Quantity | Value | Unit | Evidence | Source |
|---|---|---|---|---|---|
| Hades 1 | Zagreus base run speed | **540.0** | engine units/s | VERIFIED | `Game/Units/PlayerUnits.sjson` → `_PlayerUnit.Speed = 540.0` (patch v1.38290 files, repo `xuqifzz/hades-mod-tutorial` @69989f4a) |
| Hades 1 | Speed the run animation is authored for | **540.0** | units/s | VERIFIED | `CharacterAnimationsHero.sjson` → `ZagreusRun.NativeMoveSpeed = 540.0`; `RoomPresentation.lua` `local defaultSpeed = 540` (3 further independent copies agree) |
| Hades 1 | **Run speed, scale-free** | **3.9 ± 0.2** (median 3.97, 5 runs) | **body-heights/s** | MEASURED | 1080p60 no-commentary footage (§ Method) |
| Hades 1 | Run speed at the game's own camera | **0.47 ± 0.01** (median 511 px/s, 9 runs) | screen-heights/s | MEASURED | same footage |
| Hades 1 | Zagreus standing height at gameplay camera | **130 ± 4 px @1080p (12.0 % of screen height)** | px | MEASURED | 5 upright standing frames |
| Hades 1 | Pixels per engine unit at the observed camera | ≈ 0.945 | px/unit | DERIVED | 511 ÷ 540 |
| Hades 1 | Run cycle | 32 frames @ PlaySpeed 60 = 0.533 s; footfalls on frames 1 and 16 | — | VERIFIED + MEASURED | data record; footage repeats the pose every ≈ 16 frames @ 60 fps (PlaySpeed = frames/s) |
| Hades 1 | Run stride | **1.05 body-heights per step** (144 units), 2.10 per cycle, 3.75 steps/s | body-heights | DERIVED | 540 × 16/60 |
| Hades 1 | Dash data | BlinkMaxRange 400 · WeaponRange 300 · BlinkDuration 0.21 s | units, s | VERIFIED | `PlayerWeapons.sjson` → `RushWeapon` |
| Hades 1 | Dash distance | **2.9 body-heights** if BlinkMaxRange governs, **2.2** if WeaponRange does | body-heights | DERIVED (not measured) | governing field unknown |
| Hades 1 | Walk speeds (cutscene only) | 130 `ZagreusWalk` · 115 `ZagreusWalk2` · 95 `ZagreusDeadWalk` → **0.241 / 0.213 / 0.176 × run** | units/s | VERIFIED | `Scripts/RoomPresentation.lua` |
| Hades 1 | Low-speed fields | `LowSpeedAnimation "ZagreusWalk"`, `LowSpeedFraction 0.2`, `LowSpeedThreshold 0.5` | — | VERIFIED values; semantics unverified | `PlayerUnits.sjson` |
| Diablo II | Walk / run velocity | **6 / 9**, all 7 classes → **walk = 0.667 × run** | D2 velocity units | VERIFIED | `CharStats.txt` (1.13) `WalkVelocity` / `RunVelocity` |
| Diablo II | Unit meaning | "yards/s" (maxroll.gg) vs "Tile Units/s, 1 TU ≈ 2/3 yard" (mannm.org) | — | PRACTITIONER-REPORT (conflicting) | ratio is unit-free |
| PoE / Last Epoch / Grim Dawn | Sourced player walk:run pair | **none** | — | VERIFIED absence (PoE, GD) / gap (LE) | R10 findings § 1.7 |
| Keeper | **Run at Hades pace** | **≈ 510 px/s** (481–533) = 5.1 m/s | px/s @1080p | DERIVED | 3.9 × 130; screen route 0.473 × 1080 = 511 |
| Keeper | Walk options | 341 (D2 ratio) · 123 (Hades cutscene walk) · 102 (Hades LowSpeedFraction) | px/s | DERIVED | ratios × 511 |

## Method (video route)
- **Footage.** Primary: YouTube `-2b7GGWNz54` (Silent Longplays, "[PC] Hades No Commentary Full Playthrough Part 1/9"), 1920×1080@60, fresh save, first escape; only Athena and Ares boons (no move-speed change). Secondary `_QlbBF3z5Gg` had no standing frame, so it was not converted (raw 440–485 px/s). Rejected: Steam v1.0 Gameplay Showcase (cuts every 1–2 s, text cards, boons).
- **Camera speed was not used as hero speed.** The Hades camera leads Zagreus (616 vs 531 px in one run) and zooms ±2–3 % within a room; that shortcut gave ~580 px/s instead of ~510.
- **Background alignment:** every 4 frames, 60–100 floor patches matched and a scale+shift model fitted (residual 0.16–0.33 px/step); chained steps give camera zoom over time and put the hero in fixed room coordinates.
- **Hero position:** automatic frame differencing after alignment, and manual belt-point reads on 3× gridded crops at each run end.
- **Run selection:** straight runs ≥ ~1 s, fit error ≤ 12 px, each checked by eye for a pure run pose; attacks and turns dropped.
- **Room B-1 (converted to the standing-frame zoom):** 516.6 (127.833–128.900 s, 1.07 s, manual), 507.4 (auto, 1.0 s), 487.9 (134.80–135.83 s, 1.03 s, manual), 521.3 (0.87 s, auto), 516.2 (0.93 s, auto) → median 516, ±3.5 %.
- **Later rooms (raw px/s):** 513.0 (204 s, horizontal, 1.13 s), 514.9 (205 s), 510.8 (275 s, horizontal, 1.53 s), 505.5 (397 s, horizontal, 1.27 s). No measurable difference between horizontal and ±30° runs.
- **Height:** hair top to sole, relaxed standing, at 166.2 / 170.5 / 179 / 188 / 189 s: 130.7 / 135 / 125 / 130 / 128 → **129.9 ± 3.6 px**. Combat-ready wide stance ≈ 117 px (≈ 0.9× upright). The earlier R10 "~100 px" came from stills at a different zoom.
- **Engine units → pixels from data alone is blocked:** rooms set their own zoom and the map dump has no object positions; `Tallness = 200` is not the visual height (measures ≈ 137 units).

## Keeper arithmetic (DERIVED)
`runs/C-3/cells/run_E/registration.json`: 8 output frames @ 12 fps (0.667 s) cut from native frames 87→103 of a 24 fps clip; the file's own detected period is 18 native frames = 0.75 s (confidence 0.54), inconsistent with the 0.667 s span; `numbers.json` carries no stride/slip. At 511 px/s with the current cycle each step covers 170 px = **1.31 body-heights vs Zagreus' 1.05**; to match Hades' stride-to-height the cycle must be 0.533 s = the same 8 frames at **15 fps**.

## Open gaps
- Which dash field governs dash length (2–3 hand-measured dashes in a cleared room settle it, ~15 min).
- Pixels per engine unit at zoom 1.0 · what `LowSpeedFraction` does · the walk animation's default PlaySpeed · whether `Speed 540` differed at v1.0 (footage agreeing with the data argues against) · numeric GD / LE run speeds.

## Sources
- [xuqifzz/hades-mod-tutorial](https://github.com/xuqifzz/hades-mod-tutorial) · [NikkelM/Hades-II-HadesBiomes](https://github.com/NikkelM/Hades-II-HadesBiomes) · [fabd/diablo2 CharStats.txt](https://github.com/fabd/diablo2) · [maxroll D2 run/walk mechanics](https://maxroll.gg/d2/resources/run-walk-mechanics) · [mannm.org D2 Walking and Running](https://www.mannm.org/d2library/faqtoids/run_eng.html) · [PoE forum: movement units](https://www.pathofexile.com/forum/view-thread/1766818) · [YouTube -2b7GGWNz54](https://www.youtube.com/watch?v=-2b7GGWNz54) · [YouTube _QlbBF3z5Gg](https://www.youtube.com/watch?v=_QlbBF3z5Gg) · [Steam Hades store page](https://store.steampowered.com/app/1145360/)

Downloaded footage (~540 MB) stayed in the session scratchpad only; never committed.
