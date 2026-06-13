# BC Orphan-Lever Sizing Ruling — ONE-OFF RATIFIED

> **MEASUREMENT-FIDELITY STAMP (W-B, 2026-06-13): SEARCH-GRADE-VALID — conclusion HOLDS; measurement premise search-grade.**
> The **ONE-OFF (Axis-4 only) verdict STANDS** — it is a generation-side allocator-orphan finding decided on
> the SILENT-by-axis subtraction (5 on Axis-4, 0 everywhere), not on any 1D fight measurement, so the verdict
> is fidelity-independent and re-opens for nothing. What is stamped search-grade is the **measurement panel the
> downstream bridge acceptance reads against**: the defensive bridge's measured tank/mitigator/dodger/glass
> separation (the **25/22/23/26** result) is a **SEARCH-GRADE result on the 1D boss-duel panel** — it
> re-validates **commit-grade in W-F's boss room** (`boss_with_adds`, spatial). The § 4 acceptance criterion
> (MEASURED Axis-4 with dodger independently reachable) is therefore satisfied at search-grade now and pends
> commit-grade re-validation in W-F. NOT a HISTORICAL demotion — the discovery + sizing work is valid.
> Authority: `canonical/story/2026-06-13-combat-fidelity-drift-proofing-and-2d-certification-wave.md` § 3.2 +
> § 5 (W-F). Composes with the structural type-wall (cert wave § 3.1).

**Type:** sizing ruling (the gate this query instrument was built to fire); NOT the bridge spec
**Date:** 2026-06-13
**Author:** gandalf (story-and-design steward)
**Fidelity:** SEARCH-GRADE-VALID — conclusion holds; 25/22/23/26 is a 1D-panel result, commit-grade re-validation in W-F (see top stamp).
**Gates:** the eventual defensive-bridge design-spec-as-math (next step; this ruling sizes it)
**Inputs:**
- query instrument — `agentic_orchestration/gandalf/notes/2026-06-13-bc-orphan-lever-inventory-query.md` (commit `33d4fcf`)
- rocket's gen-side audit — `reincarnated-engine/src/reincarnated/generation/notes/bc-orphan-lever-inventory-2026-06-13.md` (engine commit `343c21b`)
- lock baseline — `canonical/story/qd-engine-bc-axes-lock-2026-05-20.md` § 3.7
**Routes to:** KR (verdict + fix-shape report); the bridge spec consumes this as its sizing premise

---

## 1. Verdict — RATIFIED: ONE-OFF (Axis-4 only)

I ratify rocket's ONE-OFF verdict. Not on deference — on the structural reasoning surviving the
refutation test the instrument was built to run.

**The evidence that decides it:** SILENT=true count by axis is 0/0/0/0/0/0/**5**/0. Every silent orphan
sits on Axis 4. The instrument's job was to find a SILENT orphan on a SECOND axis — that would have made
it a class and forced a general allocator-wiring pass. It found none. Axes 1, 2, 2A, 2B, 3A, 3B, 5 each
came back either WIRED, DEFERRED-lock (in the lock's OWN deferral registry — paper-trailed, not silent),
or GAP-sim (sim-seam, gamora — not a generation-side orphan). That is the subtraction the query defined:
`(reads-zero) − (lock-declared-deferrals) = SILENT`, and the remainder is Axis-4-only.

**The root cause is what makes one-off STRUCTURAL, not coincidental.** I verified rocket's two-mechanism
claim against the lock § 3.7 directly. Axis 4 is the only axis whose measurement formula consumes STAT
inputs (`HP`, `shield_pool`, `regen_per_sec`, `mitigation_fraction`, `evasion_misses`) rather than inputs
realized through skill metadata the sim already records (range, geometry, cc_tags, cd_seconds). Every other
axis reaches the kit through **mechanic selection** — the composer scores skills, the selected skills carry
the metadata, the sim measures it off the executed skills. That is a closed loop with no allocator gap.
Axis 4 alone reaches the kit through a **stat objective** (`DefensiveObjective`) that needs an
objective→stat allocator to land — and that allocator was never built. The orphan lives on Axis 4 *because*
Axis 4 is the only axis on Mechanism B, and Mechanism B's allocator is the single missing link. One missing
component, one axis. That is the definition of one-off, and it is architecturally entailed, not lucky.

**Refutation test passed (the instrument's self-check).** The four Axis-4 eHP rows REPRODUCED ORPHAN-gen/
SILENT; none came back WIRED. Had any come back WIRED, the keystone diagnosis would be refuted and the whole
fix line mis-aimed — that was the single most important thing this audit could have surfaced, and it didn't
surface it. `defensive_vitality_scale` greps to zero `src/` consumers. The diagnosis is confirmed, the fix
line is correctly aimed.

**Over-counting check (did rocket inflate the 5?).** No. I cross-read the lock § 3.7 deferral registry: it
explicitly defers `iframe_coverage` / `stealth_no_hit` / `reflection_redirected` ("NO — needs..."), and
rocket correctly classified those DEFERRED-lock, NOT silent. The 5 are clean. If anything the instrument was
conservative.

### 1.1 The gamora-confirm question — does the verdict hold without it? YES (separable footnote, not a gate)

The two GAP-sim rows rocket flagged for gamora (Axis-1 mobility measurement-reduction; Axis-5 statistical
resource-fraction read) are **sim-seam, not generation-side**, and by the query's own classification scheme a
GAP-sim row is "kit gets the stat but sim emits no telemetry" — a DIFFERENT bug class on a DIFFERENT seam
than the ORPHAN-gen class the defensive bridge fixes. **The one-off verdict is a generation-side
allocator-orphan finding, and it holds on the generation-side evidence alone.** Here is the load-bearing
distinction: even if gamora later confirms BOTH GAP-sim rows are genuine sim gaps, that would NOT make the
defensive orphan a class — it would surface a SEPARATE, sim-seam class (measurement gaps), which is a
different fix on a different seam, sequenced separately. The defensive bridge spec does not change shape based
on the gamora outcome.

So: **gamora-confirm is a separable footnote, not a gate on this verdict.** It should fire (the two rows are
real open questions and the sim seam owns them), but it does not block the bridge spec. I recommend KR route a
non-blocking gamora confirm in parallel with the bridge spec authoring. If gamora comes back and BOTH rows are
silent sim-gaps, that opens a sim-side measurement-orphan inventory as its own item — it does not retroactively
reclassify Axis-4.

---

## 2. Fix shape — CONTAINED defensive-bridge spec (the one-off path)

**Named:** contained defensive-bridge design-spec-as-math. NOT a general allocator-wiring pass.

**One-sentence scope:** build the single missing `DefensiveObjective`→stat allocator that reads the composed
defensive objective (`ehp_ratio_target` / `avoidance_target` / `preferred_affix`) and allocates eHP layers
(HP / shield_pool / regen_per_sec / mitigation_fraction) AND evasion-chance onto the kit, so that Axis-4's
already-live measurement formula reads non-default values — touching only the Axis-4 stat-objective seam,
leaving the seven mechanic-selection axes untouched.

**Why contained and not general:** a general allocator-wiring pass would be the right move ONLY if N>1 axes
carried silent orphans (the class path) — it would re-examine every axis's allocation seam. The evidence says
N=1. Authoring a general pass against a one-off would be the inverse of the framing-audit Q2 failure mode the
query was built to prevent: it would spend a fresh-cycle general-architecture move where the architecture needs
one bridge. The contained spec is correctly sized to the evidence.

---

## 3. The evasion second-orphan — IN SCOPE for the bridge spec, as a named sub-item (NOT separable)

The defensive bridge spec must cover **BOTH** the eHP levers AND evasion-chance allocation. Evasion is NOT a
separable sub-item, for one decisive reason: **they share the identical root cause and the identical fix
mechanism.** Both are `DefensiveObjective` outputs (`preferred_affix: evasion_high` is emitted by the SAME
composer that emits `ehp_ratio_target`) that dead-end because the SAME missing allocator never reads them onto
a kit stat. Splitting evasion into a separate item would author two halves of one allocator across two
work-units — the exact fragmentation the one-off verdict argues against.

But it gets a NAMED sub-item inside the spec because it is a SECOND, INDEPENDENT silent reason a bin is
dead, and the player consequence is distinct:

- **eHP orphan** → the tank/mitigator/glass eHP gradient never differentiates; the formula reads the
  element/energy vitality prior regardless of defensive label. Player consequence: a kit composed as a tank
  and a kit composed as glass have indistinguishable durability — the entire defensive class fantasy is flat.
- **evasion orphan** → the **dodger bin is unreachable, full stop.** `avoidance_rate` collapses to ~0 because
  kits carry no evasion stat for the live `a_evasion_misses` telemetry to count. Player consequence: one of
  the four defensive archetypes — the D3 Demon Hunter / D4 Rogue dodge-roll / PoE Trickster evade-stack
  fantasy named in the lock's own exemplar table — **cannot be expressed at all.** Not flattened; absent.

The spec must therefore honor a two-numerator structure: the eHP fix restores the tank↔glass gradient
(eHP_effective_ratio numerator), and the evasion fix restores dodger reachability (avoidance_rate numerator).
Both flow through the one allocator; both are validated against MEASURED Axis-4. One spec, two named levers,
two distinct player-consequence acceptance criteria.

---

## 4. Hand-off shape — what the bridge spec must honor

The spec is the next step and is NOT authored here. When it is authored (design-spec-as-math; rocket executes
the allocator per the math handoff), it must honor the following. Most are already on record; I add two.

**Already on record (carry forward):**

1. **jack-ryan guardrail — validate against MEASURED Axis-4, not a proxy.** Acceptance is the BC measurement
   formula reading a balanced bin distribution off SIMULATED kits — target 24/24/24/24 across
   tank/mitigator/dodger/glass — NOT a "glass takes less damage" intuition-proxy. The orphan existed for three
   weeks precisely because nobody checked the measured output; the fix is not done until the measurement
   confirms it.
2. **Differentiate eHP through HP / mitigation / avoidance allocation — NOT HP-bloat.** The tank↔glass gradient
   must be realized by allocating across the FOUR distinct eHP layers (HP, shield_pool, regen, mitigation_
   fraction) plus avoidance, so the bins are mechanically distinct, not a single HP slider. A tank that is
   "more HP" and a mitigator that is "even more HP" would pass a naive ratio check while collapsing the bins
   into one fantasy. The lock's hybrid-capture table (§ 3.7) depends on shield_pool / regen / mitigation being
   independently allocable — the allocator must preserve that.

**Added by this ruling (two):**

3. **The dodger bin is an independent acceptance gate, not an averaged-in cell.** Because evasion is a SECOND
   independent orphan with its own player-consequence (bin ABSENT, not flat), the spec's acceptance must check
   dodger reachability SEPARATELY — `avoidance_rate >= 0.40` must be ACHIEVABLE by an evasion-composed kit, not
   merely "the distribution is roughly even." A spec that fixes eHP and leaves avoidance near-zero would pass a
   three-bin check and still ship a dead archetype. Name dodger as its own gate.
4. **The allocator must NOT regress the element/energy vitality prior into incoherence.** Today vitality comes
   from `stat_allocator.allocate_stats(archetype_tag)` — the element/role prior. The bridge introduces a SECOND
   source (the defensive objective) for the same stat surface. The spec must define how the two COMPOSE — does
   the defensive objective SCALE the prior, OVERRIDE it, or ADD to it? — because an unspecified interaction is
   how the next silent inconsistency gets born. The cleanest design intent (subject to the math): the defensive
   objective is the AUTHORITY for the eHP gradient and the element/energy prior provides the BASE magnitude it
   scales — so a fire-glass and a fire-tank share an element flavor but diverge on the defensive axis as the
   label intends. The spec resolves this explicitly; it does not inherit it as an accident.

**Discipline framing for the spec (math-hotspot routing):** the bridge is a design-spec-as-math handoff
(gandalf authors the math; rocket executes the allocator). Axis-4 bin assignment is BC-axis-layer work; if the
spec's calibration of the eHP-layer weighting or the avoidance threshold touches a P2/P3/P5 methodology choice,
Discipline #18 methodology-consultation timing applies (fires AFTER a baseline allocator exists, not before —
per OP § 4.2). The empirical criterion that gates "spec done" is the MEASURED 24/24/24/24 with dodger
independently reachable — substrate evidence, not assertion (recognition → validate → commit).

---

## 5. Recap for KR

- **Verdict:** ONE-OFF (Axis-4 only) — RATIFIED. SILENT-by-axis = 5 on Axis-4, 0 everywhere. Root cause is
  structural (stat-objective vs mechanic-selection asymmetry; one missing allocator on one axis), not
  coincidental. Refutation self-check passed; over-counting check passed.
- **Fix shape:** CONTAINED defensive-bridge design-spec-as-math. One-sentence scope in § 2.
- **Evasion:** IN SCOPE, named sub-item — same root cause, same allocator, distinct player-consequence (dodger
  bin ABSENT, not flat). Two named levers in one spec.
- **gamora-confirm:** separable non-blocking footnote, NOT a gate. Route in parallel; it cannot reclassify
  Axis-4 (different bug class, different seam).
- **Hand-off:** spec must honor jack-ryan's two guardrails + two additions (dodger as independent gate;
  defensive-objective↔element-prior composition defined explicitly).
- **Next step:** author the bridge spec. Gated on this ruling — now ungated. NOT authored here.

---

**Signed:** gandalf, 2026-06-13
**For:** sizing the BC defensive-bridge fix before it is specced. Ratifies rocket's gen-side audit (engine
`343c21b`) against the lock § 3.7. Routes to KR; the bridge spec consumes this as its sizing premise.
