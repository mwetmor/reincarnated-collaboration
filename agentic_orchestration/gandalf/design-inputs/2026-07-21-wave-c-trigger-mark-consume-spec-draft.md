# Wave-C Trigger + Mark-Consume Spec — STOP-WORK PUSHBACK (not the requested draft)

> **STATUS: PUSHBACK / STOP-WORK — the requested artifact was NOT authored, by design-stewardship decision.**
> **Date:** 2026-07-21
> **Author:** gandalf (SPEC-AUTHOR work unit → escalated to DRIFT-CRITIC on premise-collision)
> **Authority:** gandalf role mandate — *"Recommend, do not unilaterally rescope. Push back hard when ideas don't fit."* + Discipline #11 (empirical inspection over assumption) + canon-conflict rule #3 (decisions-log is temporal ground truth). This file occupies the path the task named so the parent finds the output where it expects it; the content is the correct call, not the literal one.
> **⚠ SWITCH:** SPEC-AUTHOR (draft-a-new-spec) → DRIFT-CRITIC (the-spec-already-exists-as-ratified-remote-truth). I refuse to mint a duplicate authority surface for a BUILD-AUTHORIZED, LANDED spec.

---

## §0 — The one-sentence finding

**The Wave-C trigger + mark-consume spec already exists, already passed Gate-1 AND Gate-2, and is already BUILT and pushed to remote-truth in the live engine.** Authoring a fresh "pre-build DRAFT for Matt ratification" would create a duplicate, drift-inducing, ruling-reopening competitor to a landed spec — the precise failure the doc-lifecycle governance system exists to prevent. **I did not write it. Here is the evidence and the recommended action.**

---

## §1 — What the task brief assumed vs. what the repository is

| Brief premise | Repository reality (2026-07-21) |
|---|---|
| "Wave C's spec does not exist; Matt directed drafting it NOW in parallel." | Spec **exists** at `canonical/reap-die-rise-engine/wave-c-trigger-mark-engine-spec.md` — 1,640 lines, authored 2026-07-17 by gandalf (SPEC-AUTHOR). |
| "pre-build DRAFT for Matt ratification." | Spec is **GATE-1 PASSED — BUILD-AUTHORIZED** (DRIFT-CRITIC PASS-WITH-CORRECTIONS `f2511469`; jack-ryan Gate-1 PASS-WITH-AMENDMENTS folded `ce63f756`; decisions-log 5961–6111). |
| Banner: "refreshes on Wave A/B closeout." | **Wave-A CLOSED-VERIFIED** (Gate-2 PASS, engine `4929c6c`). **Wave-B BUILT + GATE-2 PASS, REMOTE TRUTH** (engine `b850800`). Both closed days ago. |
| Wave order A → B → **C** still pending. | **Wave-C BUILT + GATE-2 PASS, REMOTE TRUTH** (engine `b850800..941dbbf`, 11 commits + 8 tags; census V10 = 97.5%, spec ceiling hit exactly; Discipline #62 ratified). There is even a **Wave-D LANDED** beyond it (engine `8d8bd26`, census V12 = 99.29% projected), which consumed Wave-C's Gate-2 fidelity-deferral ledger. |

The brief describes a moment in project time that is **four-plus days and four build waves stale.** Every load-bearing ruling it hands me to "honor" (Q23 rider grammar, mint discipline, MAX_CHAIN_DEPTH runaway guard, the genre anchors) is already honored *in the landed spec and in shipped code.*

**Sequencing note:** the pause-2 rulings the brief cites (`v3-mechanics-leverage-v1.md` PAUSE-2 block, 2026-07-12) ARE real and ARE the governing record — but they *authorized* the Wave-A→B→C build fan-out. That fan-out then ran to completion. The brief was written against the pause-2 snapshot as if the fan-out had not yet fired. It fired, gated, and landed.

---

## §2 — Engine reality: the primitives the brief asks me to spec are already in the live tree

Every item in the brief's "SPEC MUST COVER" list is already implemented and Gate-2-verified. Cited by `path:line`, as the brief demanded:

| Brief-required coverage item | Where it lives, SHIPPED |
|---|---|
| (3) anti-degeneracy budget — chain-depth cap (PoE CWDT lesson) | `MAX_CHAIN_DEPTH: int = 1` — `spatial_engine.py:326` (LOCKED; assert in `_wave_c_apply_mark ~:2790`; WC-13 CONCUR). This IS the CWDT runaway guard the brief asks me to "design INTO the spec." |
| (4) mark mechanics — application / stack / consume / anti-spam | `MARK_EFFECT_NAME_PREFIX = "mark:"` — `spatial_engine.py:330`; `_WAVEC_MARK_IDENTITIES` frozenset `:335`; mark iterator `:394`; `mark:<identity>` on defender `combatant_state` per the spec's `ActiveEffect` state model. |
| (1) trigger event vocabulary — on-hit / on-kill / on-crit / on-block / on-mark | `on-mark-apply` / `on-mark-consume` — `resource_economy.py:130-131`; `on_block` event emission — `damage_resolver.py:1041, :1085`; `on_kill` — `:1133`; `on_crit` — `:1284`; dedicated `trigger_handler.py` ("on_hit, on_kill, on_threshold, etc."). |
| (2) binding grammar — skills / riders / T4 | Wave-B single-trigger primitive at `resource_economy.py:68` (`proc_trigger_condition`, "single-trigger primitive ONLY"); Wave-C chain-grammar layered on top per the spec §2.7 extension-hook. Deflect routed as **def-bin rider** (`deflect_condition` — `resource_economy.py:105`), honoring the Q23 rider precedent exactly. |
| (7) sim consumption points | `_wave_c_apply_mark` / `_wave_c_process_tick_events` / `_wave_c_dispatch_consequence` / `_wave_c_dispatch_bt` in `spatial_engine.py` (per `AGENT_STATE.md:5336`, tag `gamora/v1.10-wavec-1`, smoke 12/12). |
| (6) builder-spender / TH carve-out | `damage-taken-converts` bin LIFTED — `bc_target_composer.py:266`; `_DEFERRED_ECON_BINS = frozenset()` (empty) `:108`; `hp` cost-type contract widened `:286` (the Gate-1 MAJOR-1 fold). |
| (5) mark-consume as cadence + genre precedent | Spec §2.1–§2.10 already cites PoE1 Assassin's/Warlord's Mark consume, D4 Vulnerable→Lucky-Hit, GD Devouring Swarm marks — the exact anchors the brief names, plus the RDR spirit-guide mark identity riding the same grammar. |

The brief-named **`lacks_life_steal` T4 trigger-signal precedent** is real and lives at `t4_synergy_scan.py:79, :93, :425` — but it is a *pre-existing* precedent the landed spec already builds on, not a gap to fill.

**Conclusion:** there is no engine gap here for a spec to address. The gap the brief imagines was closed at engine `941dbbf` (Wave-C Gate-2) and confirmed intact at `8d8bd26` (Wave-D Gate-2, MAX_CHAIN_DEPTH=1 re-verified at `spatial_engine.py:326`).

---

## §3 — Why writing the duplicate would be a stewardship failure (not just redundant)

This is not "the work is already done, so skip it." It is "doing the work as instructed would actively damage the canon." Three concrete harms:

1. **Duplicate authority surface.** Two documents both claiming to be "the Wave-C trigger + mark-consume spec," one BUILD-AUTHORIZED-and-LANDED in `canonical/`, one fresh DRAFT in `gandalf/design-inputs/`. The doc-lifecycle governance system (`canonical-doc-format.md §6`) exists precisely to prevent competing truth surfaces. A future agent grepping for the Wave-C spec would hit both and not know which governs. *(Genre-shop analogy: this is the Diablo III pre-launch "two live copies of the itemization doc" failure mode — one team built against the stale copy. The fix was single-source authority. We have single-source authority; a duplicate DRAFT breaks it.)*

2. **Reopening ratified rulings.** The landed spec carries **nine veto-open rulings WC-13..WC-21** plus Gate-1's 3-MAJOR/4-MINOR fold, all closed in decisions-log 5961–6111 and re-affirmed at Gate-2 (245/245 own-run). A fresh DRAFT presenting these as open `[MATT-FORK]` choices would invite Matt to re-litigate decisions his own gates already closed — and would contradict **canon-conflict rule #3: decisions-log is temporal ground truth.** Re-opening closed-and-built rulings is negative-value churn.

3. **Drift against shipped code.** Any fresh draft would inevitably diverge in small ways (field names, cap values, vocabulary) from the code that actually shipped (`spatial_engine.py`, `resource_economy.py`, `bc_target_composer.py`). The moment a "spec" disagrees with the built-and-verified engine, it becomes a drift-generator. Discipline #13 (implicit-pillar drift) names this as a first-order hazard; my role charter names *catching drift before others can* as core duty. The correct move is to not create the drift source.

---

## §4 — What I recommend instead (the honest deliverable)

**Primary recommendation — NO-OP on Wave-C spec authoring.** The spec exists, is ratified, is built, is remote truth. Nothing is owed here. If the parent/orchestrator needs a Wave-C reference, route to the authoritative artifact:

- **The spec:** `canonical/reap-die-rise-engine/wave-c-trigger-mark-engine-spec.md` (BUILD-AUTHORIZED; §-list in §5 below).
- **The rulings:** decisions-log `~/Games/reincarnated-engine/design/decisions/decisions-log.md` 5961–6111 (Gate-1) + the WC-13..21 stamp at the spec's end.
- **The build record:** engine `b850800..941dbbf` (11 commits + 8 tags); census V10 = 97.5%.
- **The delta tracker:** `canonical/current-to-end-state/current-to-end-state-engine.md:59–63` (RETURNED → GATE-1 → IMPLEMENTATION → GATE-2 → CENSUS V10, the full Wave-C lifecycle).

**Escalation to Matt (design-critical, so I use my direct path — role charter "parallel escalation"):** The task brief that spawned me carried a stale project snapshot. Two possibilities, and Matt should disambiguate before any further Wave-C-labeled work fires:

- **(A) The brief is simply stale** — it was drafted against the 2026-07-12 pause-2 moment and the sender didn't have the 2026-07-17 build-landing state. Then: no action; Wave-C is done. *(This is my strong lean — the evidence is overwhelming.)*
- **(B) Matt actually wants something genuinely new** that got mis-labeled "Wave-C trigger + mark-consume." Candidates that ARE live and unbuilt, and could be what was meant:
  - **The Wave-D residue** — orbit per-tick loop wiring + placed-lane per-cast wiring, registered as tracked residue (decisions-log 6203; a hypothetical "Wave-E" if Matt authorizes further engineering waves). This is real forward work, but it is fidelity-wiring, not trigger/mark-grammar.
  - **A trigger-grammar *deepening*** — e.g., revisiting the LOCKED `MAX_CHAIN_DEPTH=1` cap to 2 (the Poet's-Pen-of-Poet's-Pen edge, ESCALATION (a) in the landed spec, ruled LOCKED-at-1 veto-open). If Matt now wants depth-2, that is a *spec amendment* to the existing doc, authored in-place — NOT a fresh competing DRAFT.
  - **The battle-sim AI / proxy-behavior grammar session** (Matt-registered 2026-07-15, tracker line 931 / 223) — the larger AI question Matt explicitly opened and did not want to get wrong. That is genuinely unspecced. But it is not trigger/mark-consume.

**If Matt confirms (B) and it is a trigger-grammar amendment:** I author it as a **`## AMENDMENT` block appended to the existing landed spec** (per `canonical-doc-format.md` amendment discipline — reconcile-not-amputate), re-run the DRIFT-CRITIC → Gate-1 chain on the delta only, and touch nothing already built. I do **not** start a parallel document.

---

## §5 — Section list of the LANDED spec (so no one re-derives what exists)

For reference — this is what already covers every "SPEC MUST COVER" item in the brief:

- §0 TL;DR · §NG Non-goals · §1 What already EXISTS
- **§2 TRIGGER + MARK-CONSUME (headliner)** — 2.1 delegated ruling · 2.2 mechanic def · 2.3 trigger + consequence vocabulary · 2.4 emission fields · **2.5 chain-depth cap LOCKED runaway guard** · 2.6 mark state model · 2.7 Wave-B proc-loop interaction · 2.8 QD lattice invariant · 2.9 DL-03 conformance · 2.10 calibration guardrails
- §3 econ:BT block-trigger (8 kits, folded into trigger family — mint discipline honored)
- §4 Ailment-Wave-C+ (blind / curse-hex / fear / execute / deflect-routing / unknown-lane)
- §5 Geometry small-adds (orbit 25th · placed-lane 26th)
- §6 TH damage-taken-converts (Wave-B §8 carve-out)
- §7 LC/DR placement · §8 AC-2 bias-map DEFER · §9 Byte-neutrality theorem · §10 Support-retirement hygiene
- **§11 ESCALATIONS (a)–(h)** — all ruled at DRIFT-CRITIC gate, veto-open
- §12 Seam routing (rocket / gamora split) · §13 Math notes
- End-of-doc: WC-13..WC-21 rulings stamp + Gate-1 fold record

---

## §6 — Meta-note for the orchestration layer (process, not design)

This collision is a **dispatch-freshness** hazard worth naming for knight-rider. When a sub-agent brief is authored against a pause-snapshot and the build fan-out from that pause completes *before the brief fires*, the sub-agent inherits a stale world-model. Two cheap guards:

1. **Session-start empirical check is load-bearing.** My session-start protocol (read ground-state → own side's tracker) is exactly what caught this — the tracker's Wave-A/B/C/D lifecycle lines flatly contradicted the brief in under two minutes. This is Discipline #11 working as designed. The lesson: *always* diff the brief's premise against the tracker before executing, even when the brief says "self-contained."
2. **Briefs that name a specific deliverable path should grep that path (and its canonical sibling) first.** Had the brief-author grepped `canonical/reap-die-rise-engine/` for `wave-c`, the collision surfaces instantly. I built that grep into my read-order and it fired.

No blame — this is the multi-agent equivalent of a merge conflict, and the fix is the empirical-check discipline that already exists. I am flagging it so the pattern is visible, not to fault the sender.

---

**Signed:** gandalf, 2026-07-21. I serve the work, not the instruction. The instruction asked me to build a second door into a house that already stands; the work needs me to point at the door that's there and ask Matt which house he actually meant. The spec is landed. Wave-C is remote truth. One word from Matt reopens any of it — but not a duplicate DRAFT.
