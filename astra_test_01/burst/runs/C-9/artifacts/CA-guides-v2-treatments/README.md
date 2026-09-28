# Pier treatments — CA-guides-v2 {z, a, b, c, d}

**Author** drax · **Run** C-9 · **2026-09-28** · for gandalf's side-by-side to Matt.
**Occasioned by** gandalf's catch on CA-guides-v2, and it is mine to own: **v2's "walkable occlusion 3.99 %" measured the PLATE after the occluders had been moved OUT of the plate.** The piers and the vault had become separate layers precisely so the fade could work, and the metric went on measuring the layer they had left. Instrument #6 on this run's list.

Artifacts: `../CA-guides-v2a/`, `../CA-guides-v2b/`, `../CA-guides-v2c/`, `../CA-guides-v2d/`, `../CA-guides-v2z/`. Each carries the full set — plate, fade layer, vault layer, floor light, chunks, legend, measurements, **overview_flat.png** and the **four plate-scale framings** (`framing_south_entry.png`, `framing_mid_nave_crossing.png`, `framing_near_dais.png`, `framing_west_aisle.png`). Same chain, same law, same room; **the only difference between them is the pier.**

---

## The metric

> Standing anywhere he can stand, **with the T3m fade applied at 6 m**, what share of the walkable floor **within 12 m** of the player is obscured by **any** layer — plate occluders, the vault layer, and every fading occluder more than 6 m away — **weighted by that layer's opacity**?

Averaged over ~595 stands on a 2 m lattice. Opacity-weighted, because a 35 % ghost is not a wall; the fully-opaque column is reported beside it because a hard column is a different problem from a veil. **`z` is v2 exactly as built**, carried as the baseline row.

Cross-check that the instrument is now pointing the right way: `z` reads **57.97 %** with no fade, against gandalf's independently measured **58.9 %** behind the pier layer. Different definitions, same place. v2's own 3.99 % is not on this scale at all.

## Results

| | treatment | **floor hidden within 12 m, fade at 6 m** | of which fully opaque | no fade at all | vault floor coverage | pier-in-frame |
|---|---|---|---|---|---|---|
| **z** | **BASELINE** — v2 as built, all piers solid full height | **51.51 %** | 51.51 % | 57.97 % | 12.16 % | 100.00 % |
| **a** | **GHOSTED SHAFTS** — solid to 4 m, 35 % above | **32.10 %** | **21.60 %** | 35.31 % | 12.16 % | 99.59 % |
| **b** | **RUINED ARCADE** — two thirds broken at 2–7 m | **16.74 %** | 16.74 % | 21.71 % | **0.44 %** | 100.00 % |
| **c** | **FEWER, SLIMMER** — 9.5 m bays, 1.4 m section, intact | **31.16 %** | 31.16 % | 34.46 % | 7.88 % | 100.00 % |
| **d** | **GRADED GHOST** *(drax's fourth)* — solid to 4 m, then 0.60 / 0.30 / 0.12 by height | **29.12 %** | **21.60 %** | 33.15 % | 12.16 % | 99.59 % |

**Walkable residual is −4.547e-13 m² in all five.** The room did not move: every treatment re-solves the limb width against the same measured 2354.341224 m² with its own pier count and section.

## What the numbers say

**d dominates a.** Identical hard occlusion (21.60 %, same 4 m solid base), identical indoor read (99.59 %), but **3 points less soft obscuration** — because the part of a shaft that hides *distant* floor is its *upper* part, and that is also the part the player never needs to read as an obstacle. A flat 35 % trades those against each other; a ramp keeps both. If a ghost is chosen, **d is the ghost**.

**b is the readability winner and the ceiling loser.** 16.74 % is a third of the baseline and half of anything else — but **44 of 55 vault bays fall with the piers that carried them** (crack law E3, as instructed), leaving **0.44 %** vault coverage and **no vault at all in three of its four framings**. b buys the floor by giving up the ceiling layer, which is the thing R-C9-53 named as the *primary* indoor carrier. That is a design trade, not a measurement, and it is Matt's.

**c is the weakest of the three on its own terms.** Fewer, slimmer piers give the **worst hard occlusion** of any non-baseline option (31.16 %, vs 21.60 % for a/d) — 22 full-height solid columns hide more opaque floor than 36 columns solid only to 4 m. Its one advantage is an honest, unghosted look and a thinner vault (7.88 %, fewer bays).

**A middle nobody asked for, if Matt wants it:** b's ruin rule applied to d's bands — broken piers where they cost most, graded ghosts on the survivors — would land near 20 % while keeping the vault. Say the word and it is one run.

## The vault, and a second instrument correction

gandalf: *"ribs and edges only, never over more than a thin share of the floor. Report its floor coverage."*

First cut drew boundary ribs, diagonals and a filled cell, and **measured 30.49 %**. A rib at 34 m throws a band of its own width across the floor, and there is a great deal of rib. Reduced to **transverse ribs and springers only, section 0.45 m** (from 0.7), which is the arch you see crossing the frame rather than a net of stone: **12.16 %** for the 6.5 m-bay variants, **7.88 %** for c's 9.5 m bays, **0.44 %** for b. The cells are gone in all five.

*"Thin" is now a number and it is 12 %.* If that is still too much, the next lever is dropping the springers (they are the vertical stubs at the pier tops) or restricting the layer to the frame edges proper.

## Settlements carried in, unchanged

Fading props are not in the plate — plinth plus floor behind (signed off) · the floor is painted **soft and even** and the shafts become the **T3q runtime additive layer**, with `floor_light.png` as that layer's **mask**, at the declared artistic **46.07°** · arm bay 5.589 m accepted · the fade radius is a runtime parameter, 6.0 m used here for the metric and the framing preview · three pools, crossing piers and R4 cut low, the north stair on the playable side.

## Conflicts and open items

1. **b's vault.** 44 of 55 bays fall. Faithful to the instruction and to the crack law; fatal to the ceiling layer. Named, not softened.
2. **c's arm bays are 11.338 m**, outside the 9–10 m band asked for. Between the west wall and the crossing pier line the arms run 22.68 m: 2 bays gives 11.338, 3 gives 7.559. Neither is in band; 11.338 is the nearer. (The nave and chancel land at 9.029 and 9.794, both in band.)
3. **The ghost opacities are DECLARED.** 35 % is gandalf's suggestion; d's 0.60 / 0.30 / 0.12 are mine, chosen so the ramp reaches the vault springing at roughly the opacity of the vault ribs themselves. The guide renders each band as its own id class (`nave_pier`, `pier_ghost_1..3`) with the opacity in `legend.json`, so the runtime can retune without a rebuild.
4. **Pier-in-frame dips to 99.59 % for a and d.** The 0.41 % are stands where only ghosted shaft is in frame and no solid base; the indoor read is intact there, it is the *detector* that requires solid `nave_pier` pixels. Not a defect in the arena.
5. **The metric is opacity-weighted, which is a model.** A 0.12 veil is counted as hiding 12 % of the floor behind it. That is a reasonable stand-in for legibility, not a measurement of it. The honest test of a ghost is a human looking at the framings, which is what this set is for.
