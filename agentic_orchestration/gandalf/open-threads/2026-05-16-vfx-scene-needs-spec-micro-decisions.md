# Open thread — 2026-05-16 — VFX scene-needs spec micro-decisions (gandalf input requested)

**Parked by:** knight-rider (relaying Matt's 2026-05-16 Day 4 directive — sequencing the upcoming VFX scene-needs spec commission)
**Audience:** gandalf (primary; design-instinct judgment); Matt (decision-maker)
**Status:** OPEN — awaiting gandalf input on 2 (optionally 3) micro-decisions
**Resolution gates:** Matt + gandalf converge on the 2-3 micro-decisions below. Once converged, knight-rider activates the VFX scene-needs spec dispatch (drafted alongside this memo at `agentic_orchestration/dispatches/2026-05-16-gandalf-drax-vfx-scene-needs-spec.md` with placeholders) and the dispatch becomes the joint gandalf+drax work product.

---

## Why this thread exists

Per Matt's question 2026-05-16 Day 4 — sequencing the eventual attribution-pipeline work (the build-time pipeline that maps engine-substrate-tagged skills → catalogue-substrate-tagged VFX assets for demo rendering):

> *"Should we leave the 'pipeline for 2D object attribution to combatants and VFXs' up to a named agent owner? ... Would it be best to define scope of vfx first by making our decision on elements/canonical first? We also may make concrete decisions on embodiment type and other axes."*

Knight-rider's recommendation (per the answer in the orchestration log):

- Option A (named agent owner split — drax+elrond shared pipeline; build-time deterministic) is the right architecture for Reincarnated's team topology + scope
- The 4-step sequence is: (1) commission VFX scene-needs spec NOW; (2) VS2a ad-hoc attribution; (3) VS2b formalized schema; (4) optional star-lord LLM-optimization addition
- The substrate-level scene-needs spec CAN be authored NOW without waiting on cipher-width, foundation-layer, D1, or per-season-vocabulary sub-locks (all four are downstream-independent of the spec at substrate granularity)

But two specific sub-decisions would tighten the spec's VS2a-substrate scope (optional, not blocking; spec absorbs either way). **Gandalf input requested on these specifically because they touch design-instinct territory** — the strategic-axis lock + the form-bias cadence Option II + the asymmetric Q3 framing all bear on them.

---

## Sub-decision A — VS2a element vocabulary commitment

**The question:** at the player-facing surface for VS2a, do skills/encounters/VFX present their element-vocabulary as:

- **(a1)** Canonical-four labels (fire / water / earth / wind) — the engine's current LLM-visible state per pre-Stage-3 cadence Option II timing. Per the 2026-05-16 form-bias 5-entry batch (committed `680a3f1` + `5d51b5a`), Stage 3 cipher migration is sequenced AFTER Stages 1+2; VS2a's 3-4 month window doesn't naturally include Stage 3.
- **(a2)** Per-season vocabulary at the player-facing surface — would accelerate Stage 3 cipher migration to land before VS2a ships. Stronger isekai-canon-narrative-skin demonstration; tighter coupling with VS2b's Substrate Realignment.

**Knight-rider's recommendation: (a1)** for VS2a — preserves the cadence Option II sequencing; avoids coordination risk (Risk 1: drax bandwidth saturation); keeps VS2a's "updated gauntlet showcase" narrative distinct from VS2b's "Substrate Realignment" narrative.

**Gandalf input requested on:**

1. Does (a1) honor the strategic-axis lock cleanly? Sub-lock (b) Isekai-canon-primary at narrative-skin and convergence layers — does keeping canonical-four at VS2a's player-facing surface betray that lock, or is it acceptable "Phase-0 hybrid" framing where the player sees canonical-four labels but the substrate-mechanic stays narrative-skin-ready for later?
2. Does (a2) — accelerating Stage 3 to VS2a — produce demo2-side value that justifies the coordination risk? Or would the visible payoff land BETTER as VS2b's headline feature?
3. Is there a hybrid framing I'm missing? E.g., "VS2a uses canonical-four for combat-text + UI labels; per-season vocabulary lands only in flavor-text and naming-triad surfaces." Would that satisfy the strategic-axis lock without forcing full Stage 3?

---

## Sub-decision B — VS2a embodiment scope

**The question:** what embodiments does VS2a's roster cover?

- **(b1)** Humanoid-only — minimal scope; matches the engine's current generation state; preserves bandwidth for B6/B10 V2/B11/Pimen first integration. Per the form-bias cadence Option II, Stage 4 embodiment-narrative-skin display work doesn't ship until after Stage 3 — so VS2a-as-humanoid-only is the natural cadence-aligned read.
- **(b2)** Includes Slime + Spider + Dragon-Hatchling (or some subset) as embodiment-axis-aware classes — exercises form-bias Stage 1 (embodiment-axis schema additive) + Stage 4 (display) earlier; visibly demonstrates the asymmetric Q3 gap close.

**Knight-rider's recommendation: (b1)** for VS2a — per the form-bias cadence Option II, Stage 4 display work is sequenced AFTER Stage 3; VS2a is the "updated gauntlet showcase"; embodiment differentiation is the visible deliverable of VS2b (Substrate Realignment). Keeping VS2a humanoid-only preserves the VS2a-vs-VS2b narrative distinction.

**Gandalf input requested on:**

1. Does (b1) match the asymmetric Q3 finding's spirit? Cluster A (the one isekai-canon-incompatible cluster) is in scope for resolution at Stage 1+ migration; would (b1) leave the player thinking "ARPG-canon-comfortable, nothing-isekai-visible-yet" → that's exactly the strategic-axis lock's Phase-0 promise. But does keeping humanoid-only feel like a missed opportunity for VS2a to start telegraphing the isekai variance?
2. Does (b2) — including 1-3 non-humanoid embodiments at VS2a — produce visible payoff worth the bandwidth cost? The per-embodiment narrative-skin rendering work isn't trivial; drax bandwidth is the binding constraint.
3. Is there a partial framing? E.g., "VS2a is humanoid-only for COMBAT + LOADOUT but includes 1-2 non-humanoid embodiments as PRE-TRIAL CHARACTER-SELECT preview." Would that preserve cadence sequencing while telegraphing VS2b?

---

## Sub-decision C (optional) — Spec deliverable scope

**The question:** the VFX scene-needs spec itself — how wide should its deliverable be?

- **(I) VS2a-only substrate-level** — ~30-50 lines per scene type. Enumerates VFX slots for the gauntlet's 7 content-type encounters (trash / magic / pack / elite / boss / mini-boss / trial) + cast/projectile/impact/status/ambient slot-types per skill archetype. Locked at canonical-four element vocabulary (if (a1)) + humanoid embodiment (if (b1)). Authored as substrate-level enumeration with explicit "VS2b cipher-width expansion lands as an amendment" placeholder.
- **(II) VS2a + VS2b forward-looking** — ~80-120 lines per scene type. Same VS2a structure PLUS placeholder slots for cipher-width-expanded substrate-tags (anticipates Pimen-9 OR cipher-width-experiment outcome) PLUS per-embodiment narrative-skin renaming hooks PLUS Stage 4 amendment-trigger placeholders.

**Knight-rider's recommendation: (I)** for the first authoring pass — Option I is enough for VS2a's actual deployment; Option II's forward-looking content can land as a separate amendment when the cipher-width sub-lock resolves (post-Step-B + elrond emergent-grouping analysis). Authoring Option II now would commit prematurely; Option I keeps the spec rotation-safe across the four deferred sub-locks.

**Gandalf input requested on:**

- Is there value in Option II's forward-looking placeholders that I'm undervaluing? Specifically: would drax's ad-hoc attribution work at VS2a (per knight-rider's 4-step plan #2) benefit from seeing the eventual VS2b shape, even speculative?
- Or does Option II's speculative scope risk drax+elrond optimizing for placeholders that don't land?

---

## Routing — what knight-rider does after the conversation

Per the answers gandalf surfaces (in this thread or directly with Matt):

- **If (a1)+(b1)+(I) chosen** (knight-rider's recommended path): knight-rider activates the dispatch at `agentic_orchestration/dispatches/2026-05-16-gandalf-drax-vfx-scene-needs-spec.md` (status PENDING — ACTIVE; the placeholders get hard-locked to (a1)+(b1)+(I)). Dispatch fires (Matt-authorized) as a joint gandalf+drax session.
- **If any (a2)/(b2)/(II) chosen**: knight-rider amends the dispatch's placeholders to the chosen alternatives; reissues for Matt approval before activation.
- **If gandalf surfaces a hybrid (e.g., the partial framings in A.3 / B.3 above)**: knight-rider drafts the hybrid into the dispatch; reissues for Matt approval before activation.

The dispatch is authored with substrate-level scaffolding so any of the (a1/a2)/(b1/b2)/(I/II) combinations slot in cleanly — no re-authoring required; only the placeholder values change.

---

## What this thread does NOT do

- Does NOT pre-commit to any of the four catalogue-track sub-locks (cipher-width / Foundation layer / D1 / per-season vocabulary coupling). All four are downstream-independent of these micro-decisions.
- Does NOT commit drax+elrond bandwidth. The dispatch activation is Matt-authorized post-conversation.
- Does NOT replace the gandalf+drax joint session itself — the spec authoring IS the gandalf+drax session content; this memo only sets the framing for that session.

---

## Cross-references

- `agentic_orchestration/dispatches/2026-05-16-gandalf-drax-vfx-scene-needs-spec.md` (the dispatch awaiting these micro-decisions; placeholders embedded)
- `reincarnated-engine/design/decisions/decisions-log.md` 2026-05-16 form-bias 5-entry batch (committed `5d51b5a`) — strategic-axis lock + cadence Option II + four sub-locks deferred
- `reincarnated-engine/design/decisions/decisions-log.md` 2026-05-16 ailment-deferral entry (committed `680a3f1`) — companion entry confirming the form-bias cadence's empirical health
- `canonical/story/form-bias-cadence-strategy.md` § 5 + § 7 (strategic-axis + cadence Option II detail)
- `canonical/16-project-roadmap.md` §VS2a + §VS2b (workstream framing)
- `canonical/story/style-register.md` (locked HD-2D-pixel register; affects spec scope)
- `canonical/story/embodiment-narrative-layer.md` (Stage 1 + Stage 4 source)
- Knight-rider's 4-step plan answer in the orchestration log (the parent framework this micro-decision-thread sequences against)
