# Wind-down memo — progression toward battle-sim + gen-pipeline completion

**STATUS:** MEMO (gandalf wind-down survey + progression diagram + autonomous-run-eligibility classification)
**Date:** 2026-06-18
**Author:** gandalf (story-and-design steward)
**Purpose:** map the steps remaining toward (A) **battle-sim completion** and (B) **engine gen-pipeline completion**; classify each step blocked vs unblocked; identify which steps a **pre-authorization note converts to autonomous-run-eligible** (Matt's "overnight run" question).
**Method:** reconciled against disk — two Explore surveys of `reincarnated-engine/` (simulation seam + generation seam) + the gear-spec §7 architecture record + the catalogue substrate. Cited file:line throughout. NOT from session memory.
**Survey-mode discipline:** §1–§4 report **what EXISTS** (descriptive). §5–§6 are the forward classification Matt asked for (the "what unblocks" judgment) — kept separate from the state survey per the cross-cutting rule.

---

## 0. The shape in one line

**Each pipeline is blocked at exactly ONE gandalf chokepoint — battle-sim at the Stage-2c band ruling, gen-pipeline at the §7.1 manifest design-owned half — and both chokepoints are mine to clear.** Clear those two (a focused gandalf work-item each, authorable from on-disk substrate, neither needs Matt), add the already-given "flip all 3" + one push pre-authorization, and a single unattended run can take **both pipelines most of the way to completion.** The only items that genuinely cannot ride an unattended run are the push gate (ADR-006), two design calls (keystone-ceiling, caster-coverage) whose *investigations* can run while the *calls* park, and the procgen-tool adoption (Tier-3, off both critical paths).

---

## 1. What "completion" means (the two targets)

- **(A) Battle-sim complete** = the measurement apparatus is **honest** (geometry-aware spatial resolution [#1], faithful-loadout kit power [#3], MOB_HP-anchored [✓ locked 1.5x]) AND the mobs/min bands are **ruled + wired** (Stage-2c→2d) AND the open balance questions are **dispositioned** (W-F adoption live; keystone-ceiling + caster-coverage either fixed or explicitly parked with a criterion). "Done" for a gauntlet run is empirically defined: 18 SC-6 endgame encounters, terminal pass-floor 9-of-18 in-band per cohort per kit (`gauntlet_sim.py:109,158`).
- **(B) Gen-pipeline complete** = the gear-spec asset path runs **end-to-end** (manifest → master ShaderMaterial → constrained-LLM fill → L4 adapter → render), the catalogue substrate feeds it, and the six-profile emission apex lands. Procgen-assembly tooling is **off this path** (Tier-3, deferred — nothing depends on it).

---

## 2. Battle-sim progression diagram

```
BATTLE-SIM COMPLETION
═════════════════════
 ✓ MOB_HP 1.5x LOCKED (arena.py:49) ─────────────┐ (composes with #3)
                                                  ▼
 #1 geometry-fix ──▶ #2 proxy-track ON ──▶ #3 keystone-faithful ON
 (104bfbc)            (af5c8b2,+remeasure)   (gamora/v-keystone…-2,+remeasure)
 [PRE-AUTH:           [PRE-AUTH]              [PRE-AUTH]
  "flip all 3"]                                   │
      │                                           ▼
      │                                    archive re-measure
      │                                           │
      │                                           ▼
      │                              band-refit?  ⟵ GANDALF Tier-2
      │                              (pre-specifiable drift threshold;
      │                               under→bands hold, over→PARK)
      ▼
 spatial-proxy ─┐
  mechanic port │      ┌── Stage-2c BAND RULING  ◄══ GANDALF CHOKEPOINT #1
 [additive build]│     │   (AGENT_STATE:4269 "READY FOR GANDALF";
      │          │     │    n=3078 data on disk — I can clear now)
      │          │     ▼
      │          │  Stage-2d band wiring  [additive, gated on 2c]
      │          │
      └──────────┴────────────┐
                              ▼
                      W-F ADOPTION  ──▶ measurement apparatus HONEST + LIVE
                  (gated on #1 + proxy-port + Stage-2c)

 OPEN — design judgment, NOT on the additive path:
   • keystone-ceiling "over-tuned" ticket  (1.000 zero-variance ceiling;
       investigation autonomous, the CALL parks)
   • caster coverage-bound failure  (session-13: 3.3× HP move = ΔWR ~0.02;
       spatial/timeout limit, independent of mob HP; needs gandalf scenario-
       design spec BEFORE implementation is eligible)

 LOWER-CONFIDENCE / further-out (surfaced, not fully traced):
   • BC-coordinate cutover Stage-2 Unit-2+ (deferred pending a gandalf review)
   • open-shell floor residual (Stage-2c sub-question)
```

## 3. Gen-pipeline progression diagram

```
GEN-PIPELINE COMPLETION
═══════════════════════
 ✓ §7.6 StyleProfile ruling (DONE — styleprofile-output-shape-ruling-2026-06-17)
 ✓ catalogue substrate (157 packs / 62,281 assets; 5-axis tagged;
                         Option-A consumption rule: bind iff mode ∈ {A,B})
 ✓ §7.2 restyle-leaf build (rocket 5f85014; Gate-2 869c31b; conformance ENDORSED)
        │
        ▼
 §7.1 MANIFEST  ◄══ GANDALF CHOKEPOINT #2
   = design-owned half (GANDALF — element-flavor tint/finish menu +
                        provisional metal/leather labels + intent)
   + substrate slice  (ELROND — per-mesh mode + zone-count + sockets;
                       IN-FLIGHT, dispatched 837dd7f)
   [design-half: I can clear now │ elrond-slice: additive, already moving]
        │
        ▼
 §7.2 master ShaderMaterial (rocket)  [additive, gated on §7.1]
        │
        ├──▶ §7.3 star-lord constrained-LLM fill  [additive, gated]
        ├──▶ §7.5 drax L4 adapter → Godot .tres   [additive, gated]
        │
        ▼
   end-to-end GEAR-SPEC GEN COMPLETE ──▶ six-profile set apex (emission aura)

 PARALLEL / DEFERRED — off the critical path:
   • §7.4 galadriel render pass — locks provisional metal/leather labels
       (additive; one import render; fires once any mesh imports)
   • procgen-assembly tool — Tier-3, Matt-gated; NOTHING depends on it
   • B0 descent render run-to-green — gandalf-driven, in-flight (separate sub-pipeline)
```

---

## 4. Node-by-node — blocked vs unblocked

| Node | Pipeline | State | Blocked on |
|---|---|---|---|
| MOB_HP 1.5x anchor | sim | ✓ DONE (locked this session) | — |
| #1 geometry-fix flip | sim | in-flight (run prompt authored) | Matt's "flip all 3" given → only PUSH |
| #2 proxy-track flip + re-measure | sim | in-flight | same |
| #3 keystone-faithful flip + re-measure | sim | in-flight | same |
| **Stage-2c band ruling** | sim | **blocked-on-gandalf** | **gandalf (CHOKEPOINT #1)** |
| Stage-2d band wiring | sim | gated | Stage-2c |
| band-refit-after-#3 | sim | gated | #3 re-measure (pre-specifiable) |
| spatial-proxy mechanic port | sim | gated | additive build |
| W-F adoption | sim | gated | #1 + proxy-port + Stage-2c |
| keystone-ceiling ticket | sim | OPEN | design call (gandalf+Matt) |
| caster coverage-bound | sim | OPEN | gandalf scenario-design spec |
| §7.6 ruling | gen | ✓ DONE | — |
| catalogue substrate | gen | ✓ DONE | — |
| §7.2 restyle-leaf | gen | ✓ BUILT (unpushed) | — |
| **§7.1 manifest design-half** | gen | **blocked-on-gandalf** | **gandalf (CHOKEPOINT #2)** |
| §7.1 elrond substrate slice | gen | in-flight (837dd7f) | additive dispatch |
| §7.2 master ShaderMaterial | gen | gated | §7.1 |
| §7.3 star-lord LLM-fill | gen | gated | §7.1 + §7.2 |
| §7.5 drax L4 adapter | gen | gated | §7.2 |
| §7.4 galadriel render pass | gen | DEFERRED (additive) | mesh import (parallel-able) |
| procgen tool adoption | gen | DEFERRED | Matt Tier-3 (off-path) |
| PUSH (both pipelines) | — | standing gate | Matt (ADR-006) |

---

## 5. Autonomous-run eligibility — what a pre-authorization note unblocks

Three classes (this is the answer to Matt's "which can be unblocked with a pre-authorization note for an overnight run"):

**Class (i) — ALREADY pre-authorized (the note exists or is trivial):**
- **The three flag-flips (#1/#2/#3).** Matt said "flip all 3"; the run prompt (`requests/2026-06-17-kr-flag-flip-run-prompt.md`) is the note. Unattended-safe because the one design hinge — the band-refit-after-#3 — **parks** rather than auto-fires (pre-registered drift threshold; under→bands hold, over→PARK for gandalf). Residual Matt-gate: the PUSH only.

**Class (ii) — UNBLOCKABLE by a gandalf pre-clear (the high-leverage move):**
The two chokepoints are mine. Clearing them is a focused gandalf work-item each (authorable from on-disk substrate — the n=3078 characterization for Stage-2c; the §7.6 ruling + six-profile architecture for the §7.1 design-half), **neither needs Matt.** Clearing them converts a large downstream from blocked → autonomous-eligible additive builds:
- **Stage-2c band ruling cleared** → unblocks Stage-2d band wiring + (with proxy-port) W-F adoption.
- **§7.1 manifest design-half cleared** (+ elrond's in-flight slice) → unblocks §7.2 master ShaderMaterial → §7.3 LLM-fill + §7.5 L4 adapter → **end-to-end gear-spec gen.**
- Plus the always-additive items that ride alongside: spatial-proxy mechanic port, §7.4 galadriel render pass.

**Class (iii) — genuinely CANNOT ride an unattended run (Matt or live-design):**
- **The PUSH gate** (ADR-006) — unless Matt pre-authorizes a push-pattern for the run ("push at run-close"), as the charter convention allows.
- **keystone-ceiling "over-tuned" CALL** — the *investigation* (loss-variance under varied keystone magnitudes) is autonomous-eligible; the *design call* parks for Matt/gandalf.
- **caster coverage-bound failure** — needs a gandalf **scenario-design spec** before any implementation is eligible (it's a spatial/coverage/timeout fix, independent of mob HP — the flip run does NOT touch it). I can author that spec; then implementation becomes eligible.
- **procgen-assembly tool adoption** — Tier-3 cost/tooling, Matt's call. Off both critical paths, so it blocks nothing.

---

## 6. The pre-authorization note — what it would take to maximally advance both pipelines unattended

If Matt wants a single unattended autonomous run that takes both pipelines as far as they can go, the charter needs exactly three inputs:

1. **Two gandalf pre-clears (mine — next gandalf session, not Matt's):**
   - Stage-2c band ruling (from the on-disk n=3078 data) — a genuine ruling, not a rubber-stamp; it's the highest-leverage single gandalf item in the battle-sim pipeline.
   - §7.1 manifest design-owned half (element-flavor tint/finish menu + provisional labels) — the highest-leverage single gandalf item in the gen pipeline.
   - *(Optional third, lower-leverage: the caster-coverage scenario-design spec — converts that OPEN item to eligible. Worth doing if the run has headroom.)*

2. **The "flip all 3" run** (already authorized) folded into the same charter, with the band-refit-after-#3 set to **PARK on drift** (pre-registered threshold) so it's unattended-safe.

3. **One Matt input: a push pre-authorization** ("push at run-close," per the standing charter convention) — otherwise every commit accumulates unpushed and the run's value sits on disk until the next Matt session.

**Decision envelope for the run (the 2026-06-17 three-tier pattern):**
- **Tier 1 (autonomous):** all additive builds (§7.2 master shader, §7.3, §7.5, §7.4 render, spatial-proxy port, Stage-2d wiring) close via the jack-ryan Gate-2 critique-pair + my pre-registered endorse-criteria.
- **Tier 2 (PARK for gandalf — do NOT decide):** band-refit if #3 re-measure drifts past threshold; any keystone-ceiling interaction; any schema contradiction.
- **Tier 3 (PARK for Matt):** push (unless pre-authorized); keystone-ceiling design call; procgen adoption; any locked-decision re-open (MOB_HP 1.5x / band fit beyond mechanical refit).

**What the run would deliver if all three inputs are in place:** battle-sim measurement apparatus honest + live (flips ratified, bands ruled+wired, W-F adopted); gen-pipeline end-to-end gear-spec generation (manifest→shader→fill→adapter→render). That is the bulk of BOTH completion targets in one unattended pass — bounded by the two design calls that correctly park (keystone-ceiling, caster-coverage) and the push gate.

---

## 7. Sign-off

The two pipelines are not blocked on Matt and they are not blocked on engineering capacity — they are each blocked on **one gandalf ruling I have not yet authored.** That is the actionable finding: the next gandalf session's highest-leverage work is clearing Stage-2c (band ruling) and §7.1 (manifest design-half), because those two pre-clears are what convert "blocked" into "an unattended run can finish it." The flip run is authorized and routed; the push and the two design calls are the named residual.

**Signed:** gandalf, 2026-06-18.
