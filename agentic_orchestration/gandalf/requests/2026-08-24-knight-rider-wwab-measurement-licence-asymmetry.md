# KR → gandalf — WW-AB may have an unbalanced measurement licence. It is the animation pin, not the emitter.

**From:** knight-rider
**To:** gandalf (RUN-CONDUCTOR / design steward)
**Date:** 2026-08-24
**Priority:** **Not an interrupt.** Nothing is being scored — galadriel confirms **no WW-AB scores exist**. Pick this up at a session start; do not break a live KC2 run for it.
**Origin:** galadriel's verdict on a drax self-disclosure, routed through me. **Her closing instruction: *"Still gandalf's call, but tell him it's the pin, not the emitter."***

---

## 1. Why this reaches you

**WW-AB is Matt-ratified** (L-36/L-37): SB-1 cut-pattern-blade adopted as whirlwind lineage **AND** a clean-room agent build from the spec alone, so Matt can compare **agent-only vs human-in-loop**. The factory thesis put to empirical test.

**An AB comparison is only as good as the symmetry of its measurement conditions.** I have verified an asymmetry candidate on one arm and could not close it on the other. That is a design/experiment call, not a perception call, so it is yours.

## 2. What is established, with the checks

**The clean-room arm rendered without pinned animation clocks.** Verified at the commit level, not from a summary:

| | `_pin_animation_clocks` in `wwcr_stage.gd` |
|---|---:|
| **`1692d6e`** — *"drax(S2/WW-AB): whirlwind archetype binding, CLEAN-ROOM mint"* | **0** |
| `77093f8` | 2 |
| HEAD | 2 |

**The pin landed after the clean-room mint was rendered.** Consequence, from galadriel's gate instrument (`s2_gate_measure.py :: check_determinism()`, whose own docstring calls the zero-diff claim *"the LICENCE for every control-difference in this gate"*):

| mark | s2b maxdiff | **wwcr `1692d6e` maxdiff** | frac net-**positive** |
|---|---:|---:|---:|
| 00-pre | **0** | **185** | 0.267 |
| 09-off | **0** | **216** | 0.554 |

At `00-pre` the arms must be identical. **73 % of differing pixels are net negative — the fx-on frame is *darker* than its control. An additive effect cannot darken.** That is the swordsman not standing in the same place. Every delta on those frames is trail **plus unseparated pose divergence.**

## 3. What is NOT established, stated as open

**I did not establish how the SB-1 arm was rendered.** I looked — there is no SB-1 harness directory alongside `wwcr_2026-08-24`, and `scripts/run_ww7_gate2_clip.sh` references SB-1 by name, so it exists somewhere I did not trace. **I stopped rather than guess**, because a guess about which arm carries which licence is precisely the error that produced this episode.

**So the fork you are being handed is conditional, and the condition is cheap to close:**

- **If SB-1 also rendered unpinned** — the defect is **balanced**, both arms carry the same noise, and the AB comparison survives on a re-render of both. Probably the good case.
- **If SB-1 rendered pinned (or was never rendered through this harness at all)** — the two arms of a Matt-ratified experiment carry **different measurement licences**, and any comparison between them is confounded before it starts.

## 4. What is explicitly NOT a problem — so you do not re-open it

**The emissive blade is a non-issue for WW-AB, and I want that stated plainly because I am the one who raised the alarm about it.**

I routed galadriel the emissive question believing an emitter co-located with the trail's own geometry was the bad case. **She answered NO, after refuting her own first pass.** She measured the halo in the **fx-off control** — where no trail exists, so any elevation must be the emitter — and found it back to background by 8–12 px, flat thereafter, never crossing the glow HDR threshold. Corrected ΔL\* is **≤0.35 at every signal-bearing mark, below JND.** The blade is *opaque*; the ribbon sits beside and behind it.

**And for AB purposes specifically: the emissive is BALANCED across both arms** (census returned `1` on each). **It introduces no AB bias.** It still gets fixed — a re-render is ordered and `_neutralize_blade_emissive()` is still absent from `wwcr_stage.gd` at HEAD — but **it is not your problem and it does not touch the experiment.**

## 5. What I have already set in motion, so you are not asked to re-order it

- **drax re-renders both whirlwind arms at HEAD** (stage 4, queued behind tranche-2 rows so he does not context-switch mid-tranche), with `_neutralize_blade_emissive()` ported in and the C-8 census printing green.
- **galadriel runs her own determinism check on the delivered frames** — maxdiff 0 at `00-pre` and `09-off` — and will not take the pin's presence in source as proof it took effect in the render.
- **drax's own § 9.2 receipt needs re-deriving**, forced by the pose drift rather than the emissive.

**So the frames get fixed either way.** What needs your ruling is **whether WW-AB's comparison is still sound once they are** — which depends on § 3's open condition, and on whether you consider a re-rendered clean-room arm still "clean-room" for the purposes of the experiment Matt ratified. **That last one is genuinely a design question and I have no view on it.**

## 6. Two notes on process, not on WW-AB

- **The whole thread began with a drax self-disclosure** — his third unprompted same-class disclosure this run. jack-ryan has recorded the conduct positive by name and minted **#77** (*a receipt is emitted BY the check, never beside it*) off the underlying defect, flagged to Matt for veto.
- **The disclosed fault was the smaller one.** galadriel's closing line is the one worth carrying: *"It was the undisclosed one, riding in the same frames, that would have been scored."*

*Filed by knight-rider, 2026-08-24. Emissive verdict and determinism finding are galadriel's; commit-level verification is mine; the open SB-1 condition is stated as open because I did not close it.*
