# ARPG base run speeds (D2 / Grim Dawn / Last Epoch / PoE) vs Hades — body-heights per second

> **STATUS:** CURRENT — legolas Mode A research (commissioned by gandalf, RUN-CONDUCTOR, Run C-3, for Matt's R-C3-72 rule: "use the max of the group if it is below Hades"). Filed by gandalf from the agent's returned text (the harness blocks sub-agent repo writes). Method = `../2026-09-13-hades-run-speed/findings.md`. Evidence classes: VERIFIED · MEASURED · DERIVED · PRACTITIONER-REPORT.

## Summary
- **Diablo II is the fastest of the four and faster than Hades** on a screen-horizontal run: **4.4 body-heights/s**, 1.13× Hades; the VERIFIED 9 vs 6 velocities are confirmed in footage (measured run:walk 1.51). Keeper at 130 px ≈ 572 px/s.
- **Grim Dawn ≈ Hades** (3.8 bh/s, 0.97×). **Last Epoch (2.5) and Path of Exile (2.4) are much slower** (~0.6× Hades).
- **The rule does not apply cleanly:** the max (D2) is above Hades. The fastest game at or below Hades is **Grim Dawn: 3.8 bh/s → ≈ 494 px/s** for the Keeper.
- **D2 is strongly direction-dependent:** its 2:1 isometric view halves on-screen vertical movement. Averaged over all directions D2 reads ≈ 3.4 bh/s (0.87× Hades). The other three change much less with direction.
- **YouTube was bot-blocked for the whole session**; sources were Dailymotion press captures (GD, D2R; 30 fps) and Twitch VODs (LE, PoE; 1080p60).

## TL;DR

| Game | Base run speed (bh/s) | Evidence | Runs | Spread | Source |
|---|---|---|---|---|---|
| **Diablo II** (D2R footage) | **4.4 ± 0.25** screen-horizontal · ≈ 3.4 all-direction average (DERIVED) | MEASURED; agrees with VERIFIED 9/6 | 5 + 3 speed-6 calibration | run 545–586 px/s (±4 %) · height 121–130 px | Dailymotion `x89nvo1` |
| **Grim Dawn** | **3.8 ± 0.2** horizontal · 3.7 all 6 runs | MEASURED | 6 (3 horizontal) | 507–587 px/s · height 148 ± 4 px | Dailymotion `x89m2w0` |
| **Last Epoch** | **2.5 ± 0.15** | MEASURED | 6 horizontal (+3 diagonal) | 367–386 px/s (±2.5 %) · height 150 ± 6 px | Twitch `v2867500505` |
| **Path of Exile 1** | **2.4 ± 0.2** | MEASURED | 13 | 302–342 px/s (median 308) · height 130 ± 6 px | Twitch `v2870537085` |
| Hades (reference) | 3.9 ± 0.2 | MEASURED + VERIFIED 540 units/s | 5 | — | prior findings |

| Game | Ratio to Hades | Keeper run (bh/s × 130 px @1080p) |
|---|---|---|
| Diablo II (horizontal) | 1.13 | 572 px/s |
| Diablo II (all-direction average) | 0.87 | 442 px/s |
| Grim Dawn | 0.97 (all runs 0.95) | 494 px/s (all runs 481) |
| Last Epoch | 0.64 | 325 px/s |
| Path of Exile | 0.62 | 312 px/s |

| Game | Screen-heights/s | Hero height % of screen | Frame |
|---|---|---|---|
| D2R | 0.51 (horizontal) | 11.6 % | 2560×1088; 11.7 % in a second 1080p D2R capture |
| Legacy D2 | 0.48 (horizontal, DERIVED: 9 yd/s × 32 px/yd = 288 px/s ÷ 600) | not measured | 800×600 |
| Grim Dawn | 0.51 | 13.7 % | 1080 |
| Last Epoch | 0.35 | 13.9 % | 1080 |
| Path of Exile | 0.36 | 15.2 % | game area ≈ 855 px tall (letterboxed stream) |
| Hades | 0.47 | 12.0 % | 1080 |

**Walk speeds:** D2 WalkVelocity 6 vs RunVelocity 9 → walk = 0.667 × run (VERIFIED); measured walk 366 / 369 / 370 px/s = 6.0 yd/s = 2.9 bh/s, run:walk 1.51. Grim Dawn player record `walkSpeed 1.0` (VERIFIED value, meaning unverified; walking is not a player mode, not measured). PoE / LE: no sourced player walk speed.

## Method (all four)
- **Hero-locked camera verified per game** from a body point at run start/end (head, LE nameplate, PoE health bar); residual hero drift GD ≤ 16 px, D2R ≤ 6, LE ≤ 12, PoE ≤ 5 (template match 0.8). All four lock the camera to the hero (no Hades-style lead), so hero speed = ground scroll + measured drift.
- **Ground scroll:** frames paired 2–12 apart; ~60–90 textured 64-px patches matched by normalised cross-correlation, excluding hero box, HUD and webcam; per pair a horizontal/vertical shift varying linearly with screen row (perspective), read at the feet row; pairs chained across the run, bad pairs replaced by the neighbour average.
- **Hero height:** hair/hood top to sole, relaxed or upright frames only, 2–3× zoomed crops with a 10-px ruler, same footage and zoom as the runs.
- **Scale-free unit:** on-screen body height, including each game's camera tilt (as for Hades).

## Diablo II
- **Data (VERIFIED + PRACTITIONER-REPORT):** `CharStats.txt` RunVelocity 9 / WalkVelocity 6, all 7 classes. Basin Wiki "Walk/run speed" (cites Lurker Lounge, D2 Technical): speeds are **yards/s**; one yard = sub-tile corner-to-corner = **32 px horizontally, 16 px vertically**; visible area at 800×600 = 25 × 34.5 yards; chill = −50 speed → chilled run = 9 + 6×(−50)/100 = **6** (= walking). DERIVED legacy horizontal run 288 px/s, vertical 144 px/s at 800×600. Legacy sprite height: not sourced.
- **Video:** Dailymotion `x89nvo1` (jeuxvideo.com "Diablo II : Resurrected – Paladin Gameplay (début jeu)"), 2560×1088 @ 30 fps; flat isometric (all rows scroll within 1 %).
- **Speed-6 calibration:** 22.93–24.03 s 366 px/s (chilled) · 115.77–116.73 s 370 (chilled) · 230.33–233.37 s 369 (3.0 s upright walk) → **61.3 px per yard** horizontally.
- **Runs** (on screen → isometric-corrected, vertical doubled): 122.50–123.83 s near-horizontal 513 → **557** · 4.10–5.07 s 356 → **556** · 5.10–7.33 s 427 → **586** · 283.07–284.27 s 434 → **579** · 66.90–67.80 s 294 → **545**. Median 557 px/s = **9.1 yd/s** (matches VERIFIED 9); agreement across directions after correction confirms the 2:1 squash; DERIVED horizontal run 9 × 61.3 = 552.
- **Height:** paladin upright at 230.6 / 233.0 / 4.3 s: 123 / 120 / 124–134 px; second D2R source (Twitch `v2869240707`, 1080p60 druid at 105 / 125 / 140 s): 126 / 128 / 120 → **≈ 126 ± 5 px, 11.6–11.7 %**.
- **Result:** 557 / 126 = **4.4 bh/s** (4.2–4.8); all-direction average × 0.771 = **3.4 bh/s** (DERIVED); straight down/up the screen 552 / 2 / 126 = **2.2 bh/s**.
- Rejected: the druid's Werewolf-form runs (575–581 px/s, rough cross-check only) and chilled segments (calibration only).

## Grim Dawn
- **Data (values VERIFIED, units unresolved):** Edition III `database.arz` (2026-08-08), `records/creatures/pc/malepc01.dbr` / `femalepc01.dbr`: `characterRunSpeed 0.92`, `characterRunSpeedModifier 0.0`, `characterRunSpeedJitter 0.0`, `walkSpeed 1.0`, `actorHeight 3.0`, `actorRadius 0.32`, `scale 1.05`; template `database/templates/player.tpl`; run animations `.anm` (e.g. `creatures/pc/anm/hero01_sword1h_run.anm`). 0.92 is probably a multiplier on the run animation's root motion (not parsed) → **units/s not derived**. A search snippet (Nexus mod page, not opened) says a mod raises "0.92 to 1.6" — consistent, not verified.
- **Video:** Dailymotion `x89m2w0` (jeuxvideo.com "Grim Dawn : premières minutes", 2022-04-01), 1920×1080 @ 29.97; fresh character, first zone around Devil's Crossing; mild perspective (top row ~8 % slower).
- **Runs:** 318.78–319.98 s 172° **559** · 324.88–326.18 s 2° **587** · 359.05–360.15 s 9° **533** (horizontal set, median 559) · 206.40–207.37 s −17° 554 · 357.32–358.98 s 17° 507 · 289.75–290.75 s −27° 522 (all-runs median 543).
- **Height:** standing at 195 / 245 s: 147 / 150 → **148 ± 4 px (13.7 %)**; combat crouch ≈ 125; run pose ≈ 115–120.
- **Result:** 559 / 148 = **3.8 bh/s** horizontal (3.6–4.0); all runs 3.7 (3.4–4.0).

## Last Epoch
- **Data: BLOCKED / not found** (forum thread 14348 gives percentages only; fandom wiki HTTP 402; no datamined or official units/s; no local install).
- **Video:** Twitch `v2867500505` (pinchingloaf "Practice Leveling Runs | Primalist", 2026-09-07), 1080p60, fresh run in The Old Road (HP 110/110); first 262 s; overlays masked; lock checked with the nameplate.
- **Runs (near horizontal):** 8.80–9.68 s 371 · 9.70–10.80 s 367 · 19.37–21.10 s 375 (1.7 s) · 69.05–70.25 s 378 · 83.72–85.18 s 376 · 115.18–116.18 s 386 → median **375**; diagonal (−33° to −36°) 342–366.
- **Height:** upright 56.2 / 56.8 / 57.4 s ≈ 150–155; idle 141 / 149 s: 148 / 144 → **150 ± 6 px (13.9 %)**.
- **Result:** 375 / 150 = **2.5 bh/s** (2.35–2.68). Caveats: LE zoom is user-adjustable and changed after 180 s (runs 274–338 px/s, smaller hero) — only 8–116 s used with same-window heights; items picked up (staff, spear) — absence of movement-speed gear/passives assumed.

## Path of Exile 1
- **Data: PRACTITIONER-REPORT only** — forum thread 1766818, player "raics" (2016-11-13): *"the average run speed of an exile fresh off the boat was last clocked at 38 units per second"* (tongue-in-cheek, uncertain, no GGG reply); no unit conversion. poewiki behind an Anubis challenge (not bypassed); fandom HTTP 402.
- **Video:** Twitch `v2870537085` (jungroan "goal: beat act 1", 2026-09-10), 1080p60; repeated Act 1 restarts: Twilight Strand, ML 1, SSF, level 1–2 Shadow, no Quicksilver; game in the top ≈ 1920 × 855 px; inventory-open hero x ≈ 693 handled.
- **Runs (VOD time; px/s @ direction):** 807.65 s 309 @ −23° · **811.03 s 342 @ −15°** · 813.07 s 306 @ −23° · 849.90 s 314 @ −27° · 869.23 s 319 @ −29° · 873.83 s 308 @ −37° · 8.15 s 301 @ −28° · 12.23 s 303 @ −42° · 59.97 s 310 @ −26° (drift assumed 0) · 1605.48 s 303 @ −29° (2.9 s) · **1656.58 s 314 @ −17°** · 451.37 s 302 @ −96° (vertical) · 428.67 s 308 @ −42° (drift assumed 0) → median **308**; vertical ≈ diagonal (direction matters little).
- **Height:** standing/casting 19.5 / 21.0 / 23.0 s: 123 / 135 / 123 → **130 ± 6 px (15.2 % of the game area)**.
- **Result:** 308 / 130 = **2.4 bh/s** (2.2–2.8; the two most horizontal runs 2.4–2.6).

## Gaps
- YouTube bot-check block → GD/D2R are 30 fps press captures; one source per game for runs (D2R height cross-checked).
- Grim Dawn: what `characterRunSpeed 0.92` multiplies (parse `.anm` root motion).
- PoE: no verified units/s; camera tilt not measured.
- Last Epoch: no numeric data; absence of movement-speed gear in the window not verified.
- Legacy D2 sprite height at 800×600 unsourced; D2R scale = legacy scale assumed.
- **Direction convention:** D2 is strongly direction-dependent; Hades was measured with mixed directions (horizontal and ±30°). The Keeper choice must state its convention (horizontal-run max, or all-direction average).
- Footage: ≈ 1.2 GB `.mp4` deleted; derived stills remain in the session scratchpad only. Nothing from footage is in the repo.

## Sources (accessed 2026-09-13)
- Grim Dawn data (VERIFIED): `~/Games/vendor/grim-dawn-edition-III-20260808/database/database.arz` → `records/creatures/pc/malepc01.dbr`, `femalepc01.dbr`, `anm_malepc.dbr`, read with `agentic_orchestration/research/scripts/gd_arz_adapter_2026_07_24.py` (`ArzArchive`).
- D2: prior findings, `CharStats.txt` (fabd/diablo2) · [Basin Wiki – Walk/run speed](https://www.theamazonbasin.com/wiki/index.php/Walk/run_speed) · [maxroll D2 run/walk](https://maxroll.gg/d2/resources/run-walk-mechanics) · [purediablo FPS (25 fps game clock)](https://www.purediablo.com/d2wiki/FPS)
- PoE: [forum 1766818](https://www.pathofexile.com/forum/view-thread/1766818) · [poewiki Movement speed](https://www.poewiki.net/wiki/Movement_speed) (blocked)
- LE: [forum 14348](https://forum.lastepoch.com/t/movement-speed/14348) · [fandom Movement Speed](https://lastepoch.fandom.com/wiki/Movement_Speed) (402)
- Footage: [Dailymotion x89m2w0](https://www.dailymotion.com/video/x89m2w0) · [Dailymotion x89nvo1](https://www.dailymotion.com/video/x89nvo1) · [Twitch v2869240707](https://www.twitch.tv/videos/2869240707) · [Twitch v2867500505](https://www.twitch.tv/videos/2867500505) · [Twitch v2870537085](https://www.twitch.tv/videos/2870537085)
- Rejected: Dailymotion x8tkn0u (webcams, endgame), x8vr4xu (endgame, 720p), x18diw1 (720p24), x89nuz4 (dark).
