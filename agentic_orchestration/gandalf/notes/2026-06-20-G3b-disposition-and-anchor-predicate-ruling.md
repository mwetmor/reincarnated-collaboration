# gandalf ruling — G3b disposition + the anchor-predicate question (Phase-R hand-back, terminal step)

**Author:** gandalf
**Date:** 2026-06-20
**Type:** RULING (gate-disposition + design call). The two requested rulings are §1 (G3b PASS/not) and §2 (anchor predicate: Phase-6 blocker vs tuning input). §3 clears (or not) Phase 5.
**Workstream:** instrument-validity (`agentic_orchestration/gandalf/requests/2026-06-20-instrument-validity-workstream-KR-brief.md`). This is GATE G3b — the deferred Phase-2 rage falsifier, re-armed against the post-Phase-R real economies.
**Evidence read first-hand (not on report):** gamora measurement-note + RUN RESULT §7 (`reincarnated-engine/src/reincarnated/simulation/math/g3b-rearm-economy-distinguishability-2026-06-20.md`); result JSON (`agentic_orchestration/cycle-14-wave-5-season-001/g3b-rearm-distinguishability-smoke-20260620_190536.json`); rocket Phase-R Gate-2 (`agentic_orchestration/qa/findings/2026-06-20-phaseR-rocket-reference-economy-gate2.md`); my own G1 ruling (`gandalf/notes/2026-06-20-instrument-validity-G1-rocket-economy-prerequisite-RULING.md`); the STR §5a ruling (`gandalf/notes/2026-06-19-encounter-measurement-doctrine-spine.md` §5a — the load-bearing cross-reference for §2 below).

---

## 1. G3b disposition — **CONCUR: PASS**

The pre-registered falsifier was binary and sharp (brief §3 GATE G3; gamora measurement-note §4): G3b fails if **(a)** the rage branch does not materialize the build-spend rhythm (rage ≡ mana, or rage swarm ≡ rage anchor), or **(b)** the economies collapse to indistinguishable behavior (all pairwise TVD < 0.10). I read the result against those criteria, not against the disposition gamora self-assigned.

- **(a) rage branch materializes — clears.** Rage T4 (spender) firing rises +32.8pp swarm→anchor (45.7% → 78.5%), against a pre-registered ≥10pp criterion. The pool cycles witnessed: energy-at-cast median 50 (swarm, mid-build) vs 100 (anchor, built-to-full-then-dump), min 0.0 both classes (builds-from-0 / dumps-to-0). The burst→lull rhythm is real, on a real rage entity, for the first time in this workstream. rage ≠ mana (TVD 0.386 ≫ 0.10), the load-bearing pair.
- **(b) no collapse — clears.** 5 of 6 economy pairs distinguishable; rage/combo/stamina/mana produce visibly different tier distributions. The one sub-threshold pooled pair (rage-vs-stamina, 0.071) inverts by shell class (rage T4 climbs swarm→anchor; stamina T4 falls) — pooling masks per-shell divergence; it is not a collapse signal. Each is distinguishable from mana and combo.

Neither falsifier triggered. The one unmet sub-criterion (rage swarm T1 ≥ 60%; actual 44.4%) was predicated on the target-HP anchor gate, which §7.3 shows is inert at this HP scale — the rhythm is satisfied via the energy gate, which IS the build-spend mechanism. That sub-criterion was a prediction about the *route*, not the *rhythm*; the rhythm is the falsifier, and it fires. **G3b PASS confirmed.** And I record the methodological credit: gamora did not paper over the inert-predicate discovery to protect the PASS — §7.3 surfaces it as an empirical-inspection finding (Discipline #11) and routes it to me rather than burying it. That is exactly the gate discipline the workstream's instrument-validity frame requires.

---

## 2. The anchor-predicate question — **TUNING INPUT, not a Phase-6 blocker. BUT with a named, owned pre-Phase-6 work item that is NOT optional.** Read both halves.

This is the same class of call as my G1 ruling, and I will not resolve it expediently in either direction. The expedient-PASS answer ("rhythm fires, ship it, defer the predicate") and the expedient-BLOCK answer ("predicate inert, halt Phase 6") are both wrong. The honest answer turns on **what the Phase-6 instrument must measure to be honest**, which I fixed in §5a of the doctrine spine before this question existed. I am holding myself to that.

### 2.1 What Phase 6 actually measures (from my own brief §3 GATE G7 + §5a)

Phase 6 is the (A)-vs-(B) STR read. Its O-table (brief §G7) hinges entirely on one mechanism: **"STR boss survive+kill rises from 0.000 VIA THE RAGE-SPENDER LEVER"** (O1) — i.e. STR converts the anchor-gap from a wall into a choice *because the rage spender focus-fires the bleed on the designated anchor while cleaving the adds.* §5a is explicit and load-bearing: the anchor-gap is shippable as TEXTURE **only if STR has a LEVER — a target-priority / focus-fire option that lets a player CHOOSE to engage the anchor problem.** Without the lever, "ship STR with the anchor-gap as texture" is hollow — the PoE "reroll, your build can't do this" feel-bad. The lever IS the design move that makes the disposition honest.

### 2.2 The exact thing gamora found

The build-spend RHYTHM is genuine and encounter-driven (pool dynamics over fight shape: long boss fight → pool stays full → near-continuous spender; swarm → drains → build/spend alternate). **But that rhythm fires via the ENERGY threshold, not via target selection.** The `anchor_present = nearest_target.max_hp >= 600` predicate is INERT at the live spatial HP regime (swarm median ~39,750 HP, boss ~231,000 HP → `pct_ge_600 = 100%` on BOTH). So the spender does NOT focus-fire the designated high-value anchor *within* a mixed pack — it dumps on whatever is nearest once energy is up. The encounter-driven rhythm answers **G3b's distinguishability question** in full. It does **NOT** by itself deliver the **focus-fire SEMANTICS** that §5a names as the precondition for the STR disposition being honest.

### 2.3 The ruling — disambiguated by which question Phase 6 is asked

There are two distinct reads Phase 6 could run, and the predicate matters for one and not the other:

- **Read-1 (encounter-segregated): "does STR's rage economy turn the anchor-gap into a choice across encounter TYPES?"** — run STR on boss/mini_boss/elite_pack shells vs swarm shells separately; measure whether the rage-spender DPS-on-anchor clears the enrage timer on the anchored shells. For THIS read, the encounter-driven rhythm is **sufficient** — the spender genuinely dumps harder on long single-target boss fights (78.5% T4), which IS more bleed-on-boss, which IS the lever expressing itself at the encounter granularity §5a's clear-room step-function measured at. The inert predicate does not confound this read, because on a single-anchor boss shell "nearest target" IS the anchor.

- **Read-2 (mixed-pack focus-fire): "does STR SELECTIVELY focus-fire the designated anchor amid a mixed swarm+boss pack?"** — the true `elite_pack` / `boss_with_adds` bimodal case from §5a, where STR's measured failure was precisely **sinking 73–96% of damage into the adds instead of the anchor** (§5a, the melee target-allocation failure). For THIS read the inert predicate is a **confound that would make the instrument dishonest**: with `anchor_present` true everywhere, the spender has no signal to preferentially target the anchor over the adds — so a Phase-6 "STR still fails on elite_pack" result could not distinguish "the lever doesn't work" (a real O3 design finding) from "the lever was never actually pointed at the anchor" (an instrument defect). That is the exact fake-crater pattern the GATE-1 addendum caught on the KPM-reject gate, recurring one layer down. **I will not allow Phase 6 to manufacture a second fake STR crater.**

**The ruling:** the anchor predicate rescale is a **TUNING INPUT** — NOT a structural Phase-6 blocker — **IF Phase 6 runs Read-1** (encounter-segregated, the §5a clear-vs-anchor-shell structure). It becomes a **REQUIRED pre-Phase-6 work item IF Phase 6 runs Read-2** (mixed-pack focus-fire), because Read-2's honesty depends on the spender having a real anchor signal.

Given that §5a's measured STR failure is *specifically* the bimodal-pack allocation problem (the high-HP-anchor-amid-adds cell), the (A)-vs-(B) question Matt actually wants answered lives in Read-2 territory. **Therefore the predicate rescale is required before the DEFINITIVE (A)-vs-(B) read** — but NOT before Phase 6 *opens*, and NOT a Phase-5 dependency. Phase 6 can and should run Read-1 first as the encounter-segregated probe (it is honest, it is informative, it uses the lever as it currently fires), and the predicate-rescaled Read-2 follows as the focus-fire-definitive probe. This is a Phase-6-internal sequencing, not a chain blocker.

### 2.4 The work item (owner + criterion), since Read-2 needs it

- **What:** rescale the rage-spender's anchor predicate from the absolute `max_hp >= 600` to the live HP regime — anchor = `max_hp >= k × swarm-median` (relative), OR a boss-focus / priority-target flag keyed off encounter role rather than absolute HP. This is the predicate that selects WHICH target the `costliest_spender()` path fires on amid a mixed pack.
- **Owner:** **gamora** (simulation seam — it is the rage branch's target-selection logic in `_select_player_skill_v2`, same seam as the Phase-2 selector she built). Math-note-first per Discipline #1: the note states the chosen `k` (or flag semantics) and the expected swarm-vs-mixed-pack target-selection split BEFORE the change, so the rescale is itself falsifiable.
- **Criterion (pre-registered, mine to rule):** on a MIXED swarm+anchor shell (`elite_pack` / `boss_with_adds`), the rage spender's bleed must land on the designated high-HP anchor at a rate strictly and materially above its land-rate on the surrounding adds — concretely, **anchor-targeted spender fraction ≥ 60% on mixed shells** (the focus-fire is real), while swarm-only shells retain build/spend alternation (no false anchor on a uniform pack). If the rescale produces that split, the focus-fire lever is honest and Read-2 may fire. If it does NOT (spender still sprays), THAT is itself the O3 finding (the lever is not STR's anchor answer) — but it must be measured with a *working* predicate, not an inert one.
- **Recompose-first:** this is a predicate re-scale on an existing branch, not a new mechanism. Same disposition as every other fix in this workstream — port/activate the intent, do not invent. The intent (`costliest_spender` on the anchor) already exists; only its target-selection threshold is mis-scaled to a dead HP constant.
- **Sequencing:** it is a **Phase-6-internal** item that gates Read-2 only. It does NOT gate Phase 5, does NOT gate Phase 6 opening, does NOT reopen Phases 1–4. KR sequences it between Phase-6-Read-1 and Phase-6-Read-2.

### 2.5 What I am explicitly NOT doing

I am not blocking the chain on a predicate that is irrelevant to the composed re-baseline (Phase 5 measures the population's honest bands; the rage rhythm fires correctly via the energy gate for band-measurement purposes — the predicate rescale changes target-SELECTION within mixed packs, not the per-economy firing distribution Phase 5 re-fits against). And I am not waving Read-2 through on the encounter-driven rhythm alone, because §5a's whole disposition rests on a focus-fire lever that is real, and a lever that fires on "nearest" instead of "the anchor" is not the lever §5a ruled shippable. Both halves are load-bearing.

---

## 3. Is Phase 5 cleared to proceed? — **YES.**

Phase 5 (the ONE composed re-baseline) sits behind G3b in the chain and ends at a Matt band-approval halt (brief §2/§5 GATE G6). G3b is the last offense-side gate before the composed refit. With:

- **G3b PASS** (§1) — rotation faithfulness confirmed on the real economies; the selector branch is honest;
- the anchor-predicate item correctly classified as **Phase-6-internal**, NOT a Phase-5 dependency (§2.5) — it does not touch the per-economy firing distributions the refit measures;
- Phases 1–4 already landed PASS-WITH-INFO (per KR's hand-back), and Phase R landed Gate-2 PASS-WITH-INFO (the population now carries the real doc-48 economies, which is the very instrument Phase 5 must re-fit against);

**Phase 5 is CLEARED to proceed.** The post-Phase-R full-economy population IS the composed-instrument Phase 5 re-fits the bands against — for the first time the refit will be measured on a population whose every kit fires its real economy rhythm, not uniform mana-default. That is the whole point of the workstream: one honest refit at the tail.

Phase 5 runs to its own gate — **G6: jack-ryan structural Gate-2 (BLOCK authority — mechanism correctness, V-gates, semantic-shift continuity across all four+R boundaries, seed hygiene, no production-gate regression) → new bands → decisions-log → Matt band approval.** That halt is unchanged and remains a Matt decision. I am clearing the *design/thematic* gate that gated Phase 5's start; jack-ryan's structural gate and Matt's band approval are downstream and independent of this ruling.

---

## 4. Hand-back to KR — the three asks, concisely

1. **G3b disposition:** **PASS — concur.** Neither pre-registered falsifier triggered (rage materializes the build-spend rhythm, +32.8pp swarm→anchor; economies distinguishable, 5/6 pairs, rage-vs-mana TVD 0.386). The one unmet sub-criterion was a route-prediction, not the rhythm-falsifier.
2. **Anchor predicate:** **TUNING INPUT, not a chain blocker** — but with a **required pre-Read-2 work item** (NOT optional for the definitive (A)-vs-(B) read). Owner **gamora** (math-note-first); criterion **anchor-targeted spender fraction ≥ 60% on mixed swarm+anchor shells**; recompose-first predicate rescale (`max_hp >= 600` → relative-to-swarm-median or boss-focus flag). Phase-6-INTERNAL sequencing: Phase 6 opens with Read-1 (encounter-segregated, uses the lever as it fires today — honest and informative); the rescale gates Read-2 (mixed-pack focus-fire — the read that actually answers Matt's anchor-allocation question per §5a). Does NOT gate Phase 5.
3. **Phase 5 clearance:** **CLEARED to proceed.** Runs to its own G6 halt (jack-ryan structural Gate-2 + Matt band approval), unchanged.

**Why this is not expedient in either direction:** the encounter-driven rhythm is real (so I don't block the chain), AND §5a's STR disposition rests on a focus-fire lever that fires on the anchor (so I don't wave the definitive read through on a rhythm that fires on "nearest"). The predicate-rescale is the difference between Phase 6 honestly answering "does STR's lever turn the anchor-gap into a choice" and Phase 6 manufacturing a second fake STR crater — the exact pattern the GATE-1 addendum caught one layer up. I caught it one layer down.

---

**Signed:** gandalf, 2026-06-20. The rhythm fires; the lever, to be the lever §5a ruled shippable, must fire on the anchor, not on whatever is nearest. Phase 5 proceeds; the predicate-rescale is gamora's, owned and pre-registered, before the read that decides STR.
