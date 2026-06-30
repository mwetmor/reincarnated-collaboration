# Decisions-log entry DRAFTS — weapon-as-identity Phase 1 (TWO entries)

This file now stages TWO decisions-log entries for jack-ryan canonical-write (gandalf design-fit DONE; Matt commit-framing directive 2026-06-14 applied):
- **Entry A** — the L1 identity-layer COMMIT (Matt's precise framing: proxy-rooted, literal-weapon-root deferred). NEW, below.
- **Entry B** — the § 1.2 ratio-targeting (caster-cycling) decision. As previously drafted, further down.

---

## Entry A — L1 identity-layer commit (Matt-directed framing 2026-06-14)

> jack-ryan: canonical-write this with the framing EXACT. Matt's directive verbatim: *"the commit is L1 only, on an element→scaling-attribute proxy that is gate-equivalent to the literal weapon by an empirical data-invariant, not a structural one. The decisions-log entry should say 'L1 committed; proxy-rooted; literal-weapon-root deferred as time allows' — not 'weapon-as-identity built.'"*

### 2026-06-14: Weapon-as-identity L1 identity layer COMMITTED — proxy-rooted (element→scaling-attribute), gate-equivalent to literal weapon-root by an EMPIRICAL data-invariant (not structural); literal-weapon-root DEFERRED

**Decision:** The L1 weapon-family identity layer (physical / caster / hybrid) of the weapon-as-identity architecture is COMMITTED — **L1 only.** The committed implementation does NOT root identity on the literal selected weapon's `weapon_type_family` (the spec's `selected_weapon.weapon_type_family`): the orchestrator path (`_compose_class_from_coordinate`) does not bind a weapon at the identity-derivation point. Identity is instead derived via a **PROXY** — `dominant_element → ELEMENT_SCALING_ATTRIBUTE → primary attribute → family-class` (`weapon_identity.py` / `class_generator.py:631`). **This is "L1 committed; proxy-rooted; literal-weapon-root deferred as time allows" — NOT "weapon-as-identity built."**

The proxy is **gate-equivalent to the literal weapon-root by an EMPIRICAL DATA-INVARIANT, not a structural guarantee:** in the live `v1_scope=1` pool the `primary_stat × weapon_type_family` partition never crosses the physical/caster boundary (INT/WIS → caster families, STR/DEX → physical families; `hybrid` is the sole cross-cutting family and is counted caster-side in the binary gate either way) — verified at Gate-2 by live cross-tab. The code does NOT enforce this partition; it is a property of the current data. If the pool's `primary_stat → family` partition changes (a future enrichment, a re-curation, a primary_stat that binds across the boundary), the proxy could silently diverge from the literal bound family.

**NOT committed by this entry:** the literal weapon-root (DEFERRED, as-time-allows, no gate scheduled); L2 skill-composition / proxy-primary (remains DRAFT / empirically-gated — see Entry B + the 2026-06-12 charter); L3 behavioral descriptor (unchanged); Phase-2 physical-kit composition off the weapon cross-product (separate gate).

**Reasoning:** The proxy is acceptable to commit now because (a) the gate measures the REALIZED bound `weapon_type_family` mix of the assembled roster — NOT the derived proxy — so a caster cell that martial-fallbacks WOULD be caught; (b) the § 4 gate fired green on bound families (40.74% physical / 59.26% caster-side in-band; ≥90% caster-family + 0% martial-fallback on caster cells; grep-clean of the deleted `dominant_element=="physical"` pseudo-element identity read AND the `ARCHETYPE_TEMPLATES.get→effective_power_tier` label→template identity lookup); (c) the actual smuggle the spec targets — pseudo-element identity — IS genuinely deleted. The proxy delivers the design outcome under current data while the trap is removed. Committing the literal weapon-root now would require restructuring the orchestrator to bind the weapon upstream of identity derivation — deferred as time allows, not load-bearing for the gate.

**The risk this entry preserves visibility on:** the equivalence is DATA-CONTINGENT. A future pool change that lets a `primary_stat` bind across the physical/caster boundary would break the invariant silently. The realized-bound-family measurement guardrail (Entry B § 1.2) is the RUNTIME catch; the literal-weapon-root is the STRUCTURAL fix, deferred.

**Alternatives considered:**
- Commit as "weapon-as-identity built" (literal weapon-root): rejected by Matt 2026-06-14 — the literal root was not built; recording it as built would mislead and would erase the data-invariant dependency from the record.
- Block the commit until the literal weapon-root ships: rejected — the proxy is gate-equivalent under current data and removes the actual smuggle; deferring the structural form does not block the design outcome, and the runtime guardrail catches divergence.

**Status:** Active — L1 committed proxy-rooted (Matt-ratified 2026-06-14). Literal-weapon-root DEFERRED (as-time-allows; no gate scheduled). L2 DRAFT, L3 unchanged. Empirical-data-invariant dependency recorded; runtime guardrail (realized-bound-family measurement, Entry B) is the catch. Validated by the § 4 gate on the built code (commit `7fc25a4`, tag `rocket/v1.2-weapon-as-identity-phase-1`).

**Related:**
- `agentic_orchestration/gandalf/notes/2026-06-14-weapon-as-identity-generation-spec.md` (§ 2 the literal-weapon-root intent the proxy stands in for)
- `canonical/story/weapon-as-identity-surface-recognition-2026-06-14.md` (recognition record — commit flips to L1-proxy-committed / literal-root-deferred)
- `~/Games/reincarnated-engine/src/reincarnated/generation/notes/2026-06-14-weapon-as-identity-phase-1-math-note.md`
- jack-ryan Gate-2 finding (the live `primary_stat × weapon_type_family` cross-tab establishing the data-invariant)
- Entry B below (the § 1.2 ratio guardrail — the runtime catch for divergence)
- commit `7fc25a4` / tag `rocket/v1.2-weapon-as-identity-phase-1`

---

## Entry B — § 1.2 ratio-targeting (caster-cycling)

**Authored by:** knight-rider, 2026-06-14 (DRAFT for jack-ryan review + canonical-write per decisions-log ownership; gandalf design-fit review before code commits)
**Source directive:** Matt verbatim 2026-06-14 — *"21% casters will not suffice, so we will need to cycle through the caster set until we reach the physical vs caster (regular or proxy) ratio we desire. This needs to be in the engine docs and must be part of the process."*
**Operationalizes:** gandalf weapon-as-identity spec § 1.2 (`agentic_orchestration/gandalf/notes/2026-06-14-weapon-as-identity-generation-spec.md`)

> jack-ryan: please review for accuracy + decisions-log ownership, then canonical-write into `~/Games/reincarnated-engine/design/decisions/decisions-log.md` AFTER gandalf design-fit review. The L1-hard / L2-DRAFT distinction is the load-bearing thing to verify I have stated correctly.

---

### 2026-06-14: Ratio-targeted caster-cycling is a standing generation-process requirement — output ratio is the controlled variable, NOT pool-proportional (two-layer split)

**Decision:** The weapon-as-identity generation pipeline MUST hit a target physical : caster-side OUTPUT ratio across the generated roster — the output ratio is a controlled variable, NOT an artifact of substrate availability. Two distinct rates at two distinct layers are governed separately:

- **L1 — weapon-family ratio (HARD-LOCK).** `target_physical_caster_ratio` = **40–45% physical : 55–60% caster-side**, where caster-side = regular casters (caster-arcane / caster-faith weapons) + proxy casters. Canonical-locked per Discipline #57 + Matt 2026-06-02; empirical anchor QDX-5 = 43.2% / 56.8% (PASS). A first-class, Matt-tunable generation parameter, NOT pool-proportional. The pool's natural family share (~79% physical / ~21% caster on the cycle-14 `v1_scope=1` pool) is explicitly NOT the target — the gap between ~21% and ~57% caster-side is what this requirement exists to close.
- **L2 — proxy-primary composition-rate (DRAFT, empirically gated — NOT a hard lock).** `proxy_primary_composition_rate` ≈ 15–25% of total roster (Matt recall "23%" sits at the top of band). This is a skill-composition rate NESTED within the caster-side bloc — a caster-family weapon hosts EITHER a regular-caster OR a proxy-primary composition. It is a SEPARATE lever at a DIFFERENT layer, NOT governed by weapon-cycling. It remains a recognition-record DRAFT (design prior, not committed constant) until the gamora proxy-reachability + emergent-combat centroid pass resolves; plumbing may be built against the DRAFT, but the number is not a committed generation target until that gate clears.

**The mechanism (caster-cycling):** the caster sub-pool (463 rows `v1_scope=1`; → ~635 after the magic-anchor sim_props pass) is far smaller than the physical sub-pool (1,966). To fill a caster quota ABOVE the pool's natural ~21% share, the process cycles the caster set — re-drawing WITH REUSE — rather than being capped at the pool share. This is design-legitimate because the weapon is the identity ROOT, not the whole kit: the same weapon drawn for N kits yields N distinct kits (different element, spirit, skill-composition, bc_cell). Weapon reuse ≠ kit repetition; staves recurring across a caster roster is genre-true. Set-size and target-ratio are coupled levers — growing the caster set (the magic-anchor sim_props pass) reduces repetition at any target ratio.

**The current-catalog steady-state (the validate-step finding — recorded so the reframe is permanent):** On the cycle-14 `v1_scope=1` catalog the guardrail verifies-only — the catalog's STR/DEX/INT/WIS = 8:10 attribute-mix (`ENDGAME_ENCOUNTER_CATALOG`) already delivers 44.4% physical / 55.6% caster-side, in-band on both axes — so active reuse-cycling fires only on catalog drift. This is the DESIGNED steady-state, not a gap: the requirement is the OUTPUT ratio as a controlled variable, and a guardrail that fires zero times on the current input but exists as a hard contract is the strongest honoring of "must be part of the process." The drift-injection smoke (re-Gate requirement) exercises the corrective branch so the guardrail ships proven, not dormant. The guardrail measures the realized bound `weapon_type_family` mix of the assembled roster, NOT the catalog attribute-mix as a proxy (it must catch a caster cell that martial-fallbacks, not trust the catalog's promise).

**Standing-requirement status (Matt directive):** this is NOT an optional balance knob. It is a standing requirement of the weapon-selection pipeline, encoded as (a) an explicit generation-process step in code, (b) an entry in the engine generation docs, and (c) this decisions-log entry. Enforcement locus (bc_target composition-rate vs selection-layer quota vs both) is rocket's design call; the binding requirement is the verified output ratio (spec § 4.4), not the mechanism.

**Reasoning:** Family-aware per-bc_cell selection (spec § 1.1) prevents *within-cell* skew but does NOT control the *across-roster output ratio* — if the bc_cells mirror the pool's ~21% caster share, the roster's caster output collapses back to ~21%, which Matt ruled insufficient. The genre-aligned target (40–45 / 55–60) reflects ARPG class-distribution norms (caster + proxy-summoner seats are structural, not minority-flavor); QDX-5's 43.2/56.8 empirical anchor confirms it is reachable. The two-layer separation is load-bearing: conflating the L1 weapon-family ratio with the L2 proxy composition-rate would either over-cycle the caster set (treating proxy share as a third family quota) or hard-wire an empirically-ungated 23% — both errors. L1 is hard now; L2 stays DRAFT until its own evidence gate.

**Alternatives considered:**
- Cap caster output at the pool's natural ~21% share: rejected by Matt directive — under-represents the caster + proxy-summoner seats relative to genre norms; "21% will not suffice."
- Grow the caster sub-pool large enough to hit the target by uniform sampling (no reuse): deferred, not rejected — the magic-anchor sim_props pass grows the set (533 → ~635) and reduces required reuse, but cannot reach a 1,966-row physical-pool parity; reuse remains the mechanism, set-growth the mitigation.
- Hard-wire the L2 proxy share at 23%: rejected — proxy-primary architecture is a recognition under empirical gate (2026-06-12 charter); 23% is a design prior, plumbed-against-DRAFT only.

**Status:** DRAFT (entry not yet canonical-written) — Matt-directed 2026-06-14 (verbatim above). Canonical-write pending gandalf design-fit review.

> **jack-ryan Gate-1 fix (apply at canonical-write):** do NOT carry "DRAFT" as the entry lifecycle status into the log — the L1 decision IS a committed standing requirement (Matt-directed, hard-locked), so the entry's lifecycle status is **Active**; the L2 DRAFT is a *parameter state*, not the entry state. The canonical-written Status line must read:
> `**Status:** Active — L1 40/60 HARD-LOCK (Matt-directed 2026-06-14, Discipline #57); L2 proxy-rate DRAFT (gated on gamora reachability + emergent-combat centroid pass, KR-tracked). Validated by spec § 4.4 output-ratio gate (rocket Phase-1 build).`
> This prevents a future reader mistaking the whole ratio-targeting decision for un-committed.

**Related:**
- `agentic_orchestration/gandalf/notes/2026-06-14-weapon-as-identity-generation-spec.md` § 1.2 (the requirement), § 4.4 (the gate)
- `agentic_orchestration/dispatches/2026-06-14-rocket-weapon-as-identity-phase-1.md` (the build)
- decisions-log `2026-06-12: Proxy-primary architecture CHARTERED as recognition` (the L2 DRAFT gate lineage)
- Discipline #57 (genre-aligned physical/caster distribution); QDX-5 anchor `qa/findings/2026-06-02-qdx-phase-3-qdx-5-gate-2.md` (43.2/56.8 PASS)
- `canonical/story/weapon-as-identity-surface-recognition-2026-06-14.md` (the recognition record this serves)
