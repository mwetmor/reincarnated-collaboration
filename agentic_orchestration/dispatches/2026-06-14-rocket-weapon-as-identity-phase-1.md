# Dispatch — 2026-06-14 — rocket — weapon-as-identity generation build (PHASE 1 of 2)

**From:** knight-rider
**To:** rocket
**Approved by:** Matt 2026-06-14 (implementation authorized; gandalf spec Matt-locked)
**Estimated effort:** multi-day (Pattern B)
**Acceptance:** Phase-1 = the § 1.2 ratio gate (§ 4.4) fires green AND identity-smuggle removal (§ 4.3) confirmed AND caster coherence (§ 4.2) materially above pre-enrichment martial-fallback rate. **You do NOT commit the architecture** — you produce a math-note + Gate-1 result + the gate output for gandalf design-fit review.

## Context

gandalf's weapon-as-identity spec is authored and Matt-locked at `agentic_orchestration/gandalf/notes/2026-06-14-weapon-as-identity-generation-spec.md`. It operationalizes the recognition record (`canonical/story/weapon-as-identity-surface-recognition-2026-06-14.md`) whose state is **recognition LOCKED, validate DONE, commit DEFERRED**. This build IS the buildable validate step. It is NOT an architecture commit — per recognition→validate→commit, the commit stays deferred until the § 4 gate fires green and gandalf reviews.

This is the re-open trigger for your own deferred Stage-3b physical-fork machinery (your `AGENT_STATE.md` 2026-06-14 audit: G4/G5/G7/G8 HELD set, re-open criterion = "physical-pool expansion landing"). The BC-coordinate cutover already cleaned the *elemental* path of the label-as-input smuggle across three stages; this build extends the identical discipline onto the *physical/weapon* path. Do not re-import the trap the cutover spent three stages deleting.

**The one-line design move:** the selected weapon becomes BOTH the identity root (its `weapon_type_family`) AND the skill-composition surface — unifying what is currently split between the `dominant_element=="physical"` pseudo-element fork and the `classify_archetype → ARCHETYPE_TEMPLATES` label→template fallback.

### Why Phase 1 is scoped where it is

The spec recommends front-loading the **ratio** because it is the live Matt directive (verbatim): *"21% casters will not suffice, so we will need to cycle through the caster set until we reach the physical vs caster (regular or proxy) ratio we desire. This needs to be in the engine docs and must be part of the process."* Phase 1 = the § 2 selection spine + § 1.1 family-aware selection + § 1.2 ratio-cycling + the § 4.4 ratio gate. It directly validates "21% won't suffice — cycle the caster set to target" as a coherent, testable increment. **Phase 2 (separate dispatch) = § 3 physical-kit composition off the weapon cross-product + the full § 4 gate including the kit_size 10-13 proof.**

**Phasing interaction you must honor:** Phase 1 changes identity *derivation* (which family a cell roots on) and *selection ratio* (how many caster vs physical families the roster lands). It does NOT yet move physical-kit *composition* onto the weapon cross-product — that is Phase 2 (§ 3). Phase 1 physical kits MAY continue to compose via the existing HELD machinery until Phase 2 re-points them. Verify Phase 1 does not break physical-kit composition; the ratio is about *which families are selected*, not *how kits compose*.

## Required reading before starting

- `agentic_orchestration/gandalf/notes/2026-06-14-weapon-as-identity-generation-spec.md` — THE spec (§§ 1, 1.1, 1.2, 2, 4.2, 4.3, 4.4 are Phase-1 load-bearing)
- `canonical/story/weapon-as-identity-surface-recognition-2026-06-14.md` — the recognition record this validates
- Your own `src/reincarnated/generation/AGENT_STATE.md` 2026-06-14 Stage-3 audit (the HELD physical-fork set this re-opens)
- `~/Games/reincarnated-engine/src/reincarnated/generation/class_generator.py` §§ 605-664 — the element/energy fork being replaced (`is_physical` at :616-618; `classify_archetype → ARCHETYPE_TEMPLATES` at ~636-642)
- `~/Games/reincarnated-engine/src/reincarnated/generation/substrate_weapon_binding.py` § `select_n_substrate_weapons_per_bc_cell` (~line 457) — the per-bc_cell selection point (the § 1.1 / § 1.2 enforcement candidate)
- `~/Games/reincarnated-engine/src/reincarnated/generation/bc_target_composer.py` §§ 71-92 — the 8-tuple bc_target (the OTHER § 1.2 enforcement candidate)
- decisions-log: `2026-06-12: Proxy-primary architecture CHARTERED as recognition — commitment GATED on empirical evidence` (the L2 DRAFT discipline below traces to this)
- Discipline #1 (math-before-code), #57 (the genre-aligned physical/caster distribution lock)

## Math-before-code (Discipline #1) — THE load-bearing math, produce BEFORE any code

The enforcement-point choice IS the load-bearing math. Two distinct rates at two distinct layers; the math-note must keep them structurally separate:

1. **L1 weapon-family ratio (HARD-LOCK).** Given the live `v1_scope=1` family shares (physical sub-pool 78.7% / caster sub-pool 18.5% / hybrid 2.8%; → caster ~635 after the magic-anchor sim_props pass) and the target `target_physical_caster_ratio` = **40-45% physical : 55-60% caster-side** (canonical-locked, Discipline #57; QDX-5 anchor 43.2/56.8 PASS), compute: over a roster of N kits, what caster-set reuse multiplier does the target force? (caster-side quota / caster sub-pool size).
   **DENOMINATOR DISCIPLINE (jack-ryan Gate-1 amendment — do not start the math off an ambiguous base):** the caster sub-pool is **463 rows = caster-arcane + caster-faith ONLY** (→ ~635 after the magic-anchor pass). The 533 / 21.3% figure in the spec is caster+hybrid; **hybrid (70 rows, 2.8%) is its own L1 family, NOT folded into caster-side.** The § 4.4 caster-side gate denominator = caster-arcane + caster-faith weapons + proxy-caster compositions. Compute the reuse multiplier off the 463 (→635) caster-only base, not the 533 caster+hybrid figure. Show that the multiplier is design-acceptable — weapon reuse ≠ kit repetition (same Staff → different element/spirit/bc_cell/composition = distinct kit). Show the physical : caster gap this closes (target ~57% caster-side vs the pool's natural ~21%).
2. **The enforcement locus.** Two candidates (spec § 1.2): (a) bc_target composition emits caster-flavored cells at the target rate, or (b) the selection layer enforces the caster quota by cycling the caster set. You choose the locus (either/both); the math-note must justify the choice and show the binding requirement is the *verified output ratio* (§ 4.4), not the mechanism.
3. **L2 proxy-primary composition-rate (DIFFERENT LAYER — do not conflate with L1).** The math-note must explicitly state that `proxy_primary_composition_rate` (~15-25% of total roster) is an **L2 skill-composition** rate nested *within* the caster-side bloc — a caster-family weapon hosts EITHER a regular-caster OR a proxy-primary composition. It is governed by a separate parameter, NOT by weapon-cycling. The math-note must show the two rates compose without collision (L1 sets the family mix; L2 sub-divides the caster-side bloc into regular vs proxy).

Cite code at each load-bearing claim (Discipline #1.2 math-note code-citation).

## TWO DISCIPLINES THAT ARE NON-NEGOTIABLE (gandalf flags; KR enforces)

1. **Two ratios, two layers.** `target_physical_caster_ratio` (40-45% physical / 55-60% caster-side) is an **L1 weapon-family HARD-LOCK** (Discipline #57; QDX-5 anchor 43.2/56.8). The nested `proxy_primary_composition_rate` (~15-25%) is an **L2 skill-composition** rate — different layer, governed separately, NOT by weapon-cycling. Encode the L1 40/60 as a **hard process step now.**
2. **The L2 proxy share is a recognition-record DRAFT, empirically gated — do NOT hard-wire 23%.** You MAY build the L2 plumbing against the DRAFT prior (~15-25%, design prior not committed constant), but the number is NOT a committed target until the gamora proxy-reachability + emergent-combat centroid pass resolves (KR tracks that gate). The L1 40/60 IS hard — encode it as a hard process step now; the L2 share stays a tunable DRAFT parameter.

## Cross-seam contract change? (Principle 6 gate — KR completed at authoring time)

Does this dispatch add, modify, rename, or remove any field on a telemetry table / fight_log key / loadout dict key / export packet / inter-seam fixture?

**Assessment: NO for Phase 1 as scoped.** Phase 1 changes generation-internal identity *derivation* + the selection-layer family ratio. The `bc_target` 8-tuple contract is unchanged (the cutover established it; this build consumes it). The L2 runtime label (normal vs proxy-caster) and L3 bc_target descriptor are explicitly *unchanged* per spec § 2. Loadout/fight_log dict shapes unchanged.

**Round-trip: not applicable — no cross-seam contract change in this dispatch.**

**FLAG TO ROCKET (flips this to YES):** if your implementation introduces a NEW field on `PlayerClass` (e.g. an explicit `weapon_type_family` / identity attribute) that is consumed by simulation / export / loadout, that is a cross-seam contract change → write `MIGRATION.md` (ADR-004) AND add a round-trip smoke to acceptance. Surface this in the math-note if the design needs it; do not add a cross-seam field silently.

## Scope (Phase 1)

- [ ] **Math-note (Discipline #1) FIRST** — the enforcement-point math + the two-layer rate separation, code-cited. Halt for Gate-1 before code.
- [ ] § 2 — replace the `is_physical = (dominant_element=="physical" or energy_type in PHYSICAL_COST_TYPES)` derivation with weapon-family-rooted identity (`fam = selected_weapon.weapon_type_family`; physical = {martial-heavy, martial-light, ranged}; caster = {caster-arcane, caster-faith}; hybrid = {hybrid}). Delete the `dominant_element=="physical"` pseudo-element smuggle + the `classify_archetype → ARCHETYPE_TEMPLATES.get(archetype)` label→template identity fallback at ~636-642.
- [ ] § 1.1 — confirm family-aware per-bc_cell selection (caster cells draw the 463-row caster sub-pool; physical cells draw the 1,966-row physical sub-pool). If any path samples `v1_scope` uniformly to set identity, that is the skew bug — in scope to fix.
- [ ] § 1.2 — implement ratio-targeted caster-cycling as an **explicit generation-process step in code** (`target_physical_caster_ratio` as a first-class, Matt-tunable parameter defaulting to 40-45% / 55-60%, NOT pool-proportional), cycling (re-drawing WITH REUSE) the caster set to hit the target.
- [ ] § 1.2 — **document it in the engine generation docs** (Matt directive: "must be in the engine docs and must be part of the process"). The doc entry describes the ratio as a standing pipeline requirement, not an optional knob.
- [ ] § 1.2 — L2 `proxy_primary_composition_rate` plumbing built against the DRAFT prior (~15-25%), clearly marked DRAFT / empirically-gated, NOT a hard target.
- [ ] Confirm Phase 1 does not break physical-kit composition (which still rides the HELD machinery until Phase 2).
- [ ] Source identity from the **cycle-14 BALANCED pool** = `weapon_knowledge_entries.v1_scope = 1` (2,499 rows; the one with the manually-created caster rows from `agentic_orchestration/elrond/research/substrate-enrichment-2026-05-27/`). NOT the corpus, NOT the raw pre-enrichment 85.8%-martial pool.
- [ ] Smoke-test passes (Discipline #2; include resource-scaling rehearsal #2.1 if the roster-gen run is compute-heavy).
- [ ] MIGRATION.md — only if a cross-seam field is introduced (see Principle 6 flag above).
- [ ] AGENT_STATE.md updated at session end.
- [ ] Tag: `rocket/v1.2-weapon-as-identity-phase-1` (seam prefix; milestone tag is Matt-approved only).

## Acceptance criteria (Phase 1 = a SUBSET of the spec § 4 gate)

- [ ] **§ 4.4 (THE Phase-1 gate) — output ratio hits target.** A generated roster of N kits lands the physical : caster-side ratio within tolerance of `target_physical_caster_ratio`, demonstrably **by cycling the caster set, NOT capped at the pool's ~21% caster share.** Caster-side counts regular casters (caster-arcane/caster-faith) + proxy casters. Report the achieved ratio + the caster-set reuse multiplier. The ratio is present in the engine docs as a process step.
- [ ] **§ 4.2 — caster identity reads coherent.** N generated caster kits, ≥X% carry a caster-family main weapon from the 463-row caster sub-pool (NOT martial fallback). **X is LOCKED at the gandalf design-fit review (PRE-code), not left open into the build or set at re-Gate** (jack-ryan Gate-1 amendment — an unset acceptance threshold at code-time is a Discipline #1 gap). Floor = "materially better than the pre-enrichment martial-fallback rate."
- [ ] **§ 4.3 — no identity smuggle remains.** `grep` confirms no live path sets identity from `dominant_element=="physical"` or from a label→template lookup. (Same do-not-re-import-the-trap discipline as the BC-cutover.)
- [ ] Round-trip: not applicable because no cross-seam contract change (unless the Principle-6 flag fires; then add round-trip smoke).
- [ ] **DEFERRED to Phase 2:** § 4.1 (physical kit_size 10-13 off the weapon cross-product WITHOUT the sparse mechanic pools). Do NOT attempt the kit_size proof in Phase 1.

## Out of scope (explicit non-goals)

- **NO architecture commit.** Produce the gate result; gandalf reviews → commit fires (green) or spec revises (red).
- **NO Phase-2 physical-kit composition** (§ 3 weapon cross-product → kit_size 10-13). Separate dispatch after Phase-1 gate clears.
- **NO Stage-3b physical-fork deletion** (G4/G5/G7/G8). That is downstream of Phase 2 landing + its own gate; G7 carries a cross-seam HOLD-SIM gate (`balance_loop.py`, R-2) — do not delete on generation-only clearance.
- **NO hard-wiring the L2 23% proxy share.** DRAFT plumbing only.
- **NO `v1_scope=0→1` flip of the 102 magic-anchor rows.** That is a Matt-reversible deployment step in elrond's seam; the family-aware logic is count-independent, so Phase 1 runs against the live 2,499-row pool as-is.
- **NO caster-faith remediation** (§ 5 within-family heterogeneity) — open gandalf design call, deferred, non-gating for Phase 1.

## Open questions for the agent to resolve (document in the math-note)

- Enforcement locus: bc_target composition-rate (`bc_target_composer.py`) vs selection-layer quota (`substrate_weapon_binding.py`) vs both. Justify.
- Caster-set cycling mechanism: how reuse is drawn (round-robin / weighted / random-with-replacement) and how that interacts with within-cell family affinity (§ 1.1).
- How L1 family ratio and L2 proxy composition-rate compose without collision in code (the structural separation that prevents the two-ratio conflation).
- Whether identity needs a new `PlayerClass` field (Principle-6 trigger — decide + surface).

## References

- gandalf spec `2026-06-14-weapon-as-identity-generation-spec.md`; recognition record `weapon-as-identity-surface-recognition-2026-06-14.md`
- elrond `substrate-enrichment-2026-05-27/MIGRATION.md` (the manually-created caster weapons); `2026-05-27-caster-weapon-kind-audit.md`
- gandalf `2026-06-12-proxy-primary-architecture-recognition.md` § 3 (the L2 DRAFT prior)
- decisions-log `2026-06-12: Proxy-primary architecture CHARTERED as recognition`; QDX-5 `qa/findings/2026-06-02-qdx-phase-3-qdx-5-gate-2.md` (the 43.2/56.8 anchor)
- Disciplines #1 / #1.2 / #2 / #2.1 / #57

## Sequence (per-phase; KR-tracked)

rocket math-note → **jack-ryan Gate-1** → **gandalf design-fit review** → rocket code → **jack-ryan re-Gate**. KR brings the Phase-1 Gate-1 result + the § 1.2 decisions-log draft back for gandalf's design-fit review BEFORE code commits.
