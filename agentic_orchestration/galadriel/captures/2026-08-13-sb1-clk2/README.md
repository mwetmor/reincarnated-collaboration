# SB-1 Cell CLK-2 — determinism conviction evidence

**Everything in this directory dated 2026-08-14 00:17–00:32 is FIRING-#1 SALVAGE**: it was
produced by CLK-2's first firing, which ran its probes correctly and then died having ended
its turn to wait (NOTE-84a). The probes survived; the cell did not. Firing #2 re-verified
every digest below from the raw byte lists before consuming any of it.

Everything dated 2026-08-14 later than that is FIRING #2's own work.

## What the salvage establishes (re-verified by firing #2, not taken on faith)

Leg under investigation is A2g-r's red FG-10 leg 1: `canon · undulating · tick0 1570 · FULL
320 frames`, which produced 3 distinct states across 4 passes (A·B·C·C).

| probe | leg | passes | post-prune verdict |
|---|---|---|---|
| a | `canon:on:1570:45` (short) | 4 | GREEN — `1318b5be76e6a78b…` ×4 |
| b | `canon:on:1570:full` (320) | 3 (+1 killed) | GREEN — `f651b328d9589efa…` ×3 |

`f651b328…` is the *exact* digest of A2g-r's passes 3 & 4. Five consecutive identical
full-span renders across two cells and two processes: the A·B·C·C red was a transient
walking to a warm attractor, and the system now sits in that attractor.

## NOTE-84b — the instrument finding

The probe writes **two** digest lists per pass:

- `*.raw.sha` — every frame Movie Maker wrote, **including all 60 tick-frozen preroll frames**
- `*.sha` — the same list after the preroll prune, i.e. exactly what the FG-10 gate compares

**Post-prune identical on every pass. Pre-prune different on every pass.** The live per-pass
variance fires *always*; it is confined to the preroll. Measured depth, full-span probe
(1-indexed lines of a 380-line list; preroll is lines 1–60):

| pair | n differing | deepest line | which lines |
|---|---|---|---|
| p1 vs p2 | 13 | 17 | 5–17 |
| p1 vs p3 | 1 | 18 | 18 |
| p2 vs p3 | 14 | 18 | 5–18 |
| p1 vs p4 (killed, 99 f) | 13 | 17 | 5–17 |
| p2 vs p4 (killed, 99 f) | **0** | — | — |

Deepest divergence ever observed across both probes: **line 23 of a 60-frame preroll**
(short probe). Margin to the measured span: ~37 frames.

⚑ **p2 and p4 are byte-identical over all 99 frames p4 got to write.** The preroll states
CLUSTER — they are not a random walk. Lines 1–4 agree on every pass; the variance opens at
line 5.

⚑ **Cache census unchanged across every pass** (project 148 files / 11,560 KB, user 174
files / 26,628 KB, identical at open and after all passes). Both probes ran `clear_cache=no`,
so the disk caches were already fully populated. The per-pass transient is in-process runtime
warm-up, **not** cache population. The cold side is NOT convicted by this salvage — that is
firing #2's item 1.

## The states, retro-named by pixel geography (firing #2)

Preroll frame 10 has two states across the three passes: A (p1 == p3) and B (p2 == p4).
Preroll frame 17 has two more: C (p1 == p2) and D (p3 alone).

`geography-firing1-stateA-vs-B-idx010.json`, `…-stateC-vs-D-idx017.json`:

- **82.02 %** of the frame differs; bbox is the **whole 1920×1080 frame**
- max abs channel delta **174**; mean over differing pixels **2.33**
- **47.8 %** of differing pixels are **±1** — dither-scale
- region grid is **flat** (every 4×4 cell 5.8–6.7 % of the difference): global, not localised

The amplified diffs show what those numbers are: a regular tiled diamond pattern at ±1/±2
across the entire ground plane, plus small bright clusters on each body and one strong
coloured arc at the central subject (the >8 tail, 28,862 px). A first-use rendering
difference on the ground material and the subject FX — **not** a diverged simulation.

⚑ `geography-firing1-CONTROL-idx060-measured.json` is the control: the first **measured**
frame, same two passes, **0 differing pixels**. The instrument reports zero when the frames
agree, so its non-zero readings mean something (NOTE-72).

## Contents

- `clk2-a-short1570.txt`, `clk2-b-full1570.txt` — probe run summaries
- `digests/` — every `.sha` (post-prune) and `.raw.sha` (pre-prune) list, both probes
- `evidence/*.log` — per-pass Godot logs
- `evidence/full1570-*.png` — one frame per distinct state, plus common controls
- `evidence/diff-*-amplified-x20.png` — the eyeball's copy of each state pair
- `evidence/geography-*.json` — the numbers behind those pictures
- `fg12-receipts-firing1.txt` — the prune receipts for the 1,239 + 424 frames not kept

Instrument: `reincarnated-godot/scripts/clk2_probe.sh` (committed by firing #2 — it ran
ungoverned in firing #1, and instruments get committed).
Geography tool: `agentic_orchestration/drax/tools/kc2_clk2_geography.py`.
