# Finding — 2026-06-15 — gate1-gamora-b6-reshape-scoping-signature

**Reviewer:** jack-ryan
**Severity:** WARN (CLEAR-WITH-AMENDMENTS — 2 amendments, neither blocks; both are correctness fixes to §3 before the caster arm fires)
**Target:** math-note commit `d355af0` (`src/reincarnated/simulation/math/b6-reshape-scoping-per-tier-shape-degeneracy-signature-2026-06-15.md`)
**Developer:** gamora
**Mode:** DESIGN-MODE — Gate-1 on the MANDATORY signature criterion (the decisive gate per dispatch Sequence)
**Principles applied:** #1 (math-before-code), #4 (decisions-log/criterion as truth — the signature IS the truth-act here), #11 (empirical inspection over assumption), #12 (no new semantic), Review-Principle #1 (math-before-code), #6 (cross-seam round-trip)

## Verdict

**CLEAR-WITH-AMENDMENTS.** The core signature — elements 1+2, the §1 locked-constant table, the sanity anchor, and the Discipline-#12 reuse — is rigorous, code-cited correctly, and genuinely un-steerable on its thresholds. I verified every locked constant and the recorded B/CELL-4/rogue vectors against source; they match byte-for-byte. The discriminator's threshold-symmetry claim (§2.3) holds.

Two amendments are required before the caster arm (Leg 3) runs. **A1 is a factual error in the caster-kit source mechanism (§3.1) that I empirically falsified — it does not change the conclusion but the math-note must not ship a false code-claim.** A2 is a logical-asymmetry tightening in the caster 2b reduction (§3.2). Neither blocks; both are correctness fixes folded before Leg 3.

---

## What I found

I checked the five things the dispatch asked me to scrutinize. Findings by question:

### Q4 — Elements 1+2 code-cited correctly? **YES. Clean.**
Verified live against source:
- `MODIFIER_SEARCH_FLOOR=0.01` (`balance_loop.py:318`), `CEILING=4.0` (:319), `TOLERANCE=0.03` (:60) — all confirmed.
- `TIER_FLOORS` = swarm 0.65 / magic 0.55 / elite 0.45 / mini_boss 0.20 / boss 0.30 (`:532-538`); `TIER_CEILINGS` = 0.80 / 0.70 / 0.60 / 0.50 / 0.45 (`:539-545`) — confirmed exactly.
- kills-only semantic for boss/mini_boss (`:690` comment block; timeouts=losses) — confirmed; the math-note's claim that a sub-floor "includes the all-timeout 0.0 case" is correct.
- `converged = abs(target − convergence_wr) ≤ TOLERANCE*2` (`:1212`) — confirmed.
- `MODIFIER_FLOOR_NEAR=0.015` is correctly characterized as an **analysis band** over the existing constant, not a new engine threshold. **Discipline #12 is clean** — no new engine semantic introduced; balance_loop.py is read-only here.
- Sanity anchor (§4): I re-read B's recorded JSON. CELL-4/rogue env `final_modifier=0.0101`, swarm `1.0`, elite/mini_boss/boss `0.0/0.0/0.0`; b6 `converged=true`, elite `0.75` / mini_boss `0.6667` / boss `0.9667`. The signature fires True there by construction — **anchor holds, exactly as gamora hand-verified.** This is a genuine pre-flight unit-test on the criterion at zero new fights (Discipline #11). Good.

One INFO note (not an amendment): on CELL-4/rogue the env **magic** tier is `0.5` vs floor `0.55` — also sub-floor. Element 2a deliberately scopes the upper-band conjunction to elite/mini_boss/boss only (excludes magic). That is a defensible choice (magic is mid-band, not "upper"), and the signature still fires. No action; recording it because the coverage map should not silently treat magic-sub-floor cells as clean.

### Q1 — Is the discriminator un-steerable / is "byte-for-byte symmetric" true? **Threshold-symmetry: YES. 2b-reduction: needs A2.**
The §2.3 thresholds (`MODIFIER_FLOOR_NEAR=0.015`, all-three-upper-tiers-sub-floor, over-ceiling-swarm precondition) are identically the elements-1+2 thresholds. There is no looser caster bar on the 1a/2a/1b half. That part of the anti-steer is real.

**But §3.2 is where the asymmetry hides, exactly as the dispatch predicted.** On the envelope arm, 2b requires an **external matched comparison arm** (the b6 kit) that converges AND clears the upper tiers — i.e. proof that *some* modifier resolves the cell, so the collapse is a SHAPE problem not a broken kit. The caster arm has no legacy net, so §3.2 reduces 2b to the self-contained `NOT(caster_result.converged AND all-upper ≥ floor)`. **These two predicates are not equivalent, and the substitution quietly changes what "collapse" proves:**

- Envelope 2b proves: *a different converging modifier clears the upper tiers* → the single global modifier provably *cannot* shape this cell that *is* shapeable → per-tier-SHAPE degeneracy.
- Caster self-contained form proves only: *this kit's own single-modifier run did not converge-with-upper-cleared.* That is **strictly looser** — it fires on a kit that is simply globally-broken (no modifier resolves it), which is NOT a per-tier-shape degeneracy. The load-bearing distinction that 2b was built to draw (shape-degenerate vs just-broken) is **lost on the caster arm.**

This is the soft seam. A globally-broken caster kit (bad composition, not a shape problem) would read as "casters collapse → ARCHITECTURAL" under the self-contained form, over-claiming the more-consequential finding. The asymmetry runs *toward* architectural here, not toward the convenient envelope-only — but a diagnostic that can over-fire is as unreliable as one that can under-fire. See A2.

### Q2 — Is the INCONCLUSIVE branch correct or an escape hatch? **Correct in intent; needs one guard (A2 sub-point).**
The branch (§2.3 AMBIGUOUS) correctly prevents the false-negative steer: if no caster cell drives its own swarm over-ceiling (1b never holds), collapse *couldn't* be observed, so it must NOT be scored "casters don't collapse." That is the right anti-steer and I credit it.

The residual risk the dispatch flags: can INCONCLUSIVE be used to *dodge* a real collapse by stopping early? Two things make it abusable as written, and A2 closes both:
1. There is **no pre-registered floor on how hard the harness must try** to satisfy 1b before declaring inconclusive. §3.3 locks exactly 4 caster cells at one power/seed structure. If none happens to drive swarm ≥0.80, the pass declares inconclusive and stops — with no obligation to widen power/seed until at least one hot caster cell exists. The recommendation-to-widen is mentioned but not *binding*.
2. INCONCLUSIVE and the looser self-contained 2b interact badly: a cell could be excluded-as-inconclusive on one reading or over-fired-as-architectural on another, depending on which branch the harness evaluates first. The branch precedence is not pre-registered.

### Q3 — Is the caster-kit source legitimate / apples-to-apples? **The PROBE is legitimate. The MECHANISM described in §3.1 is factually wrong — A1.**
I verified the probe equivalence empirically and it is sound: a composed caster `list[Skill]` stamped on a structural PlayerClass enters the identical `balance_class()` (`:930`) — same single-global-modifier binary search, same bands, same kills-only, same gauntlet. **The caster and physical arms genuinely differ only at template-derivation.** Apples-to-apples on the probe: confirmed.

**However, §3.1 step-2's stated mechanism is false.** The math-note claims: "`B6KitBuilder.build(archetype_tag)` looks up `ARCHETYPE_TEMPLATES.get(archetype_tag)` (:82) — which does NOT contain the composed caster tags, so a direct `build('fire_mage', ...)` would raise `ValueError` (:83-84). The harness therefore registers the `compose_all_templates` output into the builder's template lookup at HARNESS scope (a harness-side dict merge)..."

I empirically falsified this:
- `ARCHETYPE_TEMPLATES` is built at module import by `_build_archetype_templates()` (`b6_archetype_templates.py:346`), which calls `compose_from_config()` (:334) → `compose_all_templates()` (`archetype_composer.py:893`) and **merges the composed templates in** (`:340`). The four caster tags `fire_mage / water_mage / earth_caster / wind_caster` **are already present** in `ARCHETYPE_TEMPLATES` at import (I enumerated all 24 keys; the four casters are there).
- A direct `b6_builder.build("fire_mage", "fire", 50, rng, energy_type="mana", range_profile="medium")` **SUCCEEDS** and returns a valid 11-skill mana-gated caster kit (geometry/role/element/energy all populated). It does NOT raise `ValueError`.

So the "harness-side dict-merge of `compose_all_templates` over the builder's `ARCHETYPE_TEMPLATES` view" that §3.1 describes as *necessary* is **not necessary** — and if literally implemented as a merge-over-the-module-dict it would be (a) redundant and (b) a needless mutation of a shared generation-module object that risks the A3 "modify no composer" boundary. The correct, simpler, A3-clean path is: **call `b6_builder.build("fire_mage", ...)` directly** — the composed caster template is already resolvable. No merge, no module mutation.

This does not change any verdict-conclusion (the probe is still valid; casters still flow through the identical loop). It is a false code-claim in a math-note whose whole authority rests on being code-cited — it must be corrected, and the harness must use the direct-build path, not a dict-merge that the math-note's own (wrong) premise motivated.

### Q5 — Anything that would make the answer unreliable?
Covered by A1 (false mechanism → wrong/needless harness construction) and A2 (looser caster 2b → over-fire risk + unguarded inconclusive). Cross-seam §6 boundary assert is correctly symmetric (the caster-arm `_assert_boundary` is its own explicit check, not inherited — Principle 6 satisfied; no MIGRATION.md needed, read-side confirmed). Resource bound §5.3 (~1223s, smoke-subset-first, peak-RSS check) is defensible and consistent with B's measured 509s baseline.

## Rationale

- **A1** grounds in **Discipline #11** (empirical inspection over assumption — the math-note asserted an unverified code behavior that is false on inspection) and **Discipline #1 / Review-Principle #1** (math-before-code: a code-cited criterion that mis-cites the code it rests on is not yet correct). Also touches **A3** (the false premise motivates a module-dict mutation that the A3 "modify no composer" boundary disfavors).
- **A2** grounds in **Review-Principle #1** and the dispatch's own A1 amendment (the Leg-3 discriminator must be the *most* tightly pre-registered, not the softest): the self-contained 2b reduction is strictly looser than the envelope 2b and can over-fire "architectural" on a merely-broken caster kit, plus the inconclusive branch lacks a binding try-harder floor and a pre-registered branch precedence.

## Action

- [ ] **gamora (A1 — correctness fix to §3.1, before Leg 3):** Correct §3.1 step-2. The four caster tags are already in `ARCHETYPE_TEMPLATES` at module import (via `_build_archetype_templates` → `compose_from_config` → `compose_all_templates`, `b6_archetype_templates.py:334,340,346`); a direct `b6_builder.build("fire_mage"/"water_mage"/"earth_caster"/"wind_caster", ...)` SUCCEEDS and is the correct, A3-clean caster-kit source. Drop the "harness-side dict-merge over `ARCHETYPE_TEMPLATES`" mechanism (it is unnecessary and risks mutating a shared generation-module object). Keep the §3.3 cell-set and the identical-`balance_class()` probe claim — those are correct.
- [ ] **gamora (A2 — tighten the caster discriminator + inconclusive guard, before Leg 3):** (i) On the caster arm, do NOT silently substitute the looser self-contained form for envelope-2b without recording the distinction. Where a caster collapse fires, **additionally report whether the caster kit is shape-degenerate vs globally-broken** — e.g. probe whether ANY modifier in `[FLOOR, CEILING]` clears the upper tiers (the b6-style "a converging arm exists" existence check, applied to the caster's own modifier sweep), so an "architectural" verdict is not over-claimed on a merely-broken kit. If the self-contained form is retained as the headline predicate, pre-register that headline collapse = self-contained, and the shape-vs-broken split is reported alongside as the qualifier that distinguishes architectural-shape from broken-kit. (ii) Pre-register a **binding** rule that INCONCLUSIVE may only be declared after the §3.3 cell-set has been widened on power/seed until at least one caster cell satisfies 1b (swarm ≥ 0.80) OR a stated, bounded widening budget is exhausted — not on first-pass failure of the 4 locked cells. (iii) Pre-register branch precedence: a cell that satisfies 1b is evaluated for collapse; only cells where 1b is unsatisfiable across the widened set feed the inconclusive verdict.
- [ ] **gamora:** Re-commit the amended math-note; the amendments are folded-and-re-checkable at Gate-2 (no second Gate-1 halt required — A1/A2 are correctness tightenings, not new scope). No run fires until the amended note is committed.
- [ ] **Matt:** No decision needed (WARN, within ADR-002 jack-ryan approval scope for a diagnostic criterion). Flag only: the §3.2 looser-2b asymmetry means an "architectural" Leg-3 result must carry the shape-vs-broken qualifier before it reframes "envelope bug → architecture needs per-tier shape" at the gandalf+Matt scoping call.

## References

- Math-note under review: `reincarnated-engine/src/reincarnated/simulation/math/b6-reshape-scoping-per-tier-shape-degeneracy-signature-2026-06-15.md` (`d355af0`)
- Dispatch: `agentic_orchestration/dispatches/2026-06-15-gamora-b6-reshape-scoping-pass.md`
- Prior dispatch Gate-1: `agentic_orchestration/qa/findings/2026-06-15-gate1-gamora-b6-reshape-scoping-pass.md` (`fdd8057`)
- Caster-source falsification: `reincarnated-engine/src/reincarnated/generation/b6_kit_builder.py:68-101` (build → ARCHETYPE_TEMPLATES.get at :82); `b6_archetype_templates.py:316-346` (`_build_archetype_templates` merges composed at :340; `ARCHETYPE_TEMPLATES` at :346); `archetype_composer.py:718` (`compose_all_templates`), `:877-893` (`compose_from_config` → calls compose_all_templates), `:844-847` (canonical_four_tags = fire_mage/water_mage/earth_caster/wind_caster). Empirically: all 4 caster tags present in ARCHETYPE_TEMPLATES; direct `build("fire_mage")` returns 11-skill kit.
- Constants verified: `balance_loop.py:318-319` (modifier floor/ceiling), `:532-545` (TIER_FLOORS/CEILINGS), `:60` (TOLERANCE), `:686-697` (kills-only), `:1212` (converged), `:930` (balance_class).
- B evidence (sanity anchor): `reincarnated-engine/output/g7-hold-sim-b6-prereq-B-20260615.json` (CELL-4/rogue vectors match math-note §2/§4); B harness `reincarnated-engine/scripts/g7_hold_sim_b6_prereq_B_2026_06_15.py:69-76,78-81,133-146,368-377`.
