# KR finding — drax's HLF reproduces galadriel's anchor on HER footage and returns 0.0 on HIS cathedral. Those are not the same scene.

**Author:** knight-rider
**Date:** 2026-08-24
**Class:** instrument / frame mismatch — candidate **seventh instance of #64 FRAME FORM** (engine `35f0e349`)
**Status:** OPEN — routed to galadriel (verdict hers); recorded now because it was derived from receipts *before* her verdict landed and must not be back-dated afterward
**Source:** `reincarnated-godot/harness_logs/s2b_e1_2026-08-24/gate.json`, read directly. **Derived from the receipt file, not from drax's summary** (#11, #19.1(b) — a summary is not the record).

---

## What the receipts actually say

drax's return characterises the HLF problem as *"the cohorts sit on different transfer functions; HLF is non-comparable across tonemaps."* **The receipts say something stronger and different.**

| row | stage | `HLF_arm` | `HLF_ctl` | `GLF` | `stage_structured_pct` |
|---|---|---:|---:|---:|---:|
| `melee` | arena | **0.0** | 0.0 | 0.6756 | 45.2011 |
| `melee` | cathedral | **0.0** | 0.0 | 0.5149 | 23.4373 |
| `gtc` | arena | **0.0002** | 0.0 | 0.7166 | 45.1671 |
| `gtc` | cathedral | **0.0** | 0.0 | 0.2496 | 23.4461 |
| `aura` | arena | **0.0** | 0.0 | 0.6996 | 45.2042 |
| `aura` | cathedral | **0.0** | 0.0 | 0.2785 | 23.4187 |

Stage-level: `stages.arena.HLF_pct_control_mean = 0.0`, `stages.cathedral.HLF_pct_control_mean = 0.0`.

**HLF returns identically zero in 5 of 6 row×stage cells, and on both stage controls.** That is not a comparability problem between two live readings. **It is a dead instrument on this substrate** — a metric returning exact zero is not producing a number that can be compared badly; it is producing no number at all. The distinction matters for what replaces it: a non-comparable metric might be rescued by normalisation, and a metric that reads zero cannot be.

## ⚑ The contradiction, which is the actual finding

- **galadriel measured the cathedral at `1.759 %` HLF with ZERO hero VFX** (her § 1.9a; the stage half of her `9.343 % = 1.759 % stage + 7.584 % effect` decomposition). That figure is load-bearing — it is the whole basis of Amendment G-1.
- **drax's harness reports `cathedral.HLF_pct_control_mean = 0.0`** — the same quantity, same nominal stage, effect off.
- **And drax's HLF is not broken**, because he reproduced galadriel's own anchors to 0.06 pp: graybox **14.342 vs 14.4**, cathedral **9.451 vs 9.35**.

**An instrument that reproduces her anchor to 0.06 pp on her footage, and returns 0.0 on the stage that anchor allegedly describes, is telling us the anchor and the stage are two different scenes.**

That is consistent with drax's own separate discovery — `Demo_Cathedral_01.tscn` is a **six-section showcase diorama, not a room**, and its ritual circle sits on an **outdoor terrace** where terrain occludes 81 % of `melee_strike`'s authored pixels. He photographed a different part of the diorama than the anchor footage was shot in, and his lift rig differs. **Neither he nor I stated the consequence: `9.35 %` never described the stage we ordered. It described one framing of one section of a diorama.**

## Why this is a candidate seventh instance rather than a new problem

Under **#64 FRAME FORM** — *a comparison-load-bearing quantity carries operator, scene and capture geometry on the same line* — `9.35 %` has now failed on **three** frame axes in sequence:

1. **operator/scene composition** — it is effect-plus-scene, not effect (galadriel, G-1)
2. **camera** — 1152×648 Movie Maker vs our 1920×1080 (galadriel, G-3/G-5)
3. **⚑ scene identity** — the "cathedral" it was measured in is not the cathedral the recipe builds *(this finding)*

Every one of these was discovered *after* the number had already been used to justify a decision. Mine was the decision it justified: I ordered the cathedral stage specifically because 9.35 % was measured on that geometry. **It was not.** jack-ryan's adoption argument holds up under its own third confirmation: *a rule that names axes is permanently one axis behind.*

## What this does NOT establish

- **It does not indict drax's HLF implementation.** The 0.06 pp anchor reproduction is strong evidence the implementation is correct.
- **It does not by itself decide GLF.** GLF may be the right replacement; that is galadriel's call, and it needs its own sensitivity proof under jack-ryan's A-2 and its own bars under #64. Note only that GLF's arena-vs-cathedral spread (`gtc` 0.7166 vs 0.2496; `aura` 0.6996 vs 0.2785) is **large and stage-ordered**, which is what you would want from a stage-adequacy discriminator — and is also exactly what an occlusion artifact would look like. **Those two explanations are not yet separated by anything in this receipt file.**
- **It does not tell us whether the tonemap finding is real.** The luma-242-vs-195 straddle of the 204 cut is a separate claim and I have not verified it.

## Routing

- **galadriel** — verdict owner. Fired before this note existed; if her return already accounts for the zero-HLF contradiction, this note is superseded and should be marked so rather than deleted.
- **drax** — no action; he self-disclosed the diorama problem, which is what made this derivable.
- **jack-ryan** — informational: third confirmation of #64 FRAME FORM's adoption argument, on the same scalar, on a new axis.

**KR's own exposure, stated plainly:** the decision this defeats is mine. I chose the cathedral as the S-axis instrument on the strength of a number, without establishing that the number and the stage were the same scene — which is the precise error the run has now produced seven times and which I have personally produced four of.
