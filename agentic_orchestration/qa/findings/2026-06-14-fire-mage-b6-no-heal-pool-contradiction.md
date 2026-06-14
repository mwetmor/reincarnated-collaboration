# Finding — 2026-06-14 — fire-mage-b6-no-heal-pool-contradiction

**Reviewer:** jack-ryan (DEV-MODE)
**Severity:** INFO (APPROVE — within ADR-002 within-seam authority; no Matt decision needed)
**Target:** engine commit `9a46731` (fire_mage B6 fallback fix)
**Developer:** rocket

---

**Provenance (scribe note — gandalf):** this finding was authored by the **jack-ryan DEV-MODE sub-agent**, invoked by gandalf on 2026-06-14 as the Gate-2 half of the fire_mage-fix review, with a conclusion-free brief (the sub-agent was not told gandalf's design read, preserving two-witness independence). The sub-agent ran **read-only** and could not write to disk; this file is gandalf's **faithful transcription** of jack-ryan's returned verdict, captured for the durable Gate-2 record. The verbatim verdict fragments are marked below. This composes with the gandalf design-half (`agentic_orchestration/gandalf/notes/2026-06-14-two-generation-rulings-b6-kit-band-and-theme-element-flavor-pool.md` Ruling A) and the rocket resolution log (collab `6c99c55`).

---

## Gate-2 Finding — fire_mage B6 no_heal-pool fix (commit `9a46731`, rocket)

**Reviewer:** jack-ryan · **Severity: INFO (APPROVE)** · **Target:** `9a46731` · **Developer:** rocket

### Verbatim verdict (jack-ryan)

> **Severity:** INFO (APPROVE — within ADR-002 within-seam authority).
>
> The fix is correct, minimal, correctly-scoped, and the validation is real. [...] regression-safety structurally proven. [...]
>
> water_mage's composed constraints are `['require_chill_or_slow', 'require_heal_or_hot', 'require_primary_attack_skill']` — `no_heal_skill` is absent, so the gate does NOT fire [for water_mage]. [...] fire_controller and water_controller both carry `no_heal_skill` [...] auto-covered. [...]
>
> Matt: no decision needed.

### What jack-ryan found (scribe summary of the above)

1. **The fix is correct and minimal.** The `_sample_free_roles` guard drops `"sustain"` from the free-role pool precisely when `"no_heal_skill" in template.special_constraints` — additive (+11 lines, one function; 204 insertions / 0 deletions per the diff), no behavior change to any archetype that does not carry the `no_heal_skill` constraint. The constraint contradiction that forced fire_mage to retry-exhaust → fall back to the pre-B6 5-skill generator (the false-green Ruling A surfaced) is removed at its root: the builder no longer tries to satisfy a heal-bearing role under a no-heal constraint.

2. **Regression-safety is structurally proven, not asserted.** The guard fires ONLY under `no_heal_skill`; every other archetype's free-role sampling is byte-identical. The blast radius is exactly the set of archetypes carrying `no_heal_skill`.

3. **The blast radius is correctly enumerated and auto-covered.** jack-ryan independently traced the composed constraints of the adjacent archetypes:
   - **water_mage** carries `require_chill_or_slow` + `require_heal_or_hot` + `require_primary_attack_skill` — **`no_heal_skill` absent** → the new guard does NOT fire for water_mage. Its separate 1/29 sub-band item (Ruling A §named-followups) has a *different* root cause and is correctly NOT touched by this fix.
   - **fire_controller** and **water_controller** both carry `no_heal_skill` → **auto-covered** by the same guard; the fix generalizes correctly to every no-heal archetype without per-archetype special-casing.

4. **No Matt decision required.** The change is within rocket's seam and within jack-ryan's ADR-002 within-seam INFO/APPROVE authority. The validation (kits now compose at the B6 band, no fallback) is real.

### Verdict
**INFO — APPROVE.** The fire_mage B6 fallback defect (kits silently falling back to the pre-B6 5-skill path since 2026-05-12 because the `no_heal_skill` constraint and the `sustain` free-role were mutually unsatisfiable) is fixed correctly, minimally, and with the blast radius correctly enumerated and auto-covered. No regression surface beyond the no-heal archetype set, which is exactly the set intended. Composes with the test-rewrite (`f48dde8` — `test_fire_mage_kit_size_in_b6_band` now asserts the real B6-band contract, retiring the false-green `{5,6}` invariant).

### References
- `~/Games/reincarnated-engine/src/reincarnated/generation/b6_kit_builder.py` (`_sample_free_roles` guard — drops `sustain` when `no_heal_skill` constrained)
- `~/Games/reincarnated-engine/src/reincarnated/generation/archetype_composer.py` (fire+burst_damage ⇒ `no_heal_skill`; water+burst_damage ⇒ `require_heal_or_hot`)
- `~/Games/reincarnated-engine/tests/test_role_orientation.py` (`test_fire_mage_kit_size_in_b6_band` — the retired-false-green rewrite)
- `agentic_orchestration/gandalf/notes/2026-06-14-two-generation-rulings-b6-kit-band-and-theme-element-flavor-pool.md` (Ruling A — the design half; false-green discovery)
- `~/Games/reincarnated-engine/design/decisions/decisions-log.md:860-872` (earth_caster deferred-restoration precedent; :864 fire_mage/earth_caster pre-B6-fallback note since 2026-05-12)

---

## gandalf close-note (scribe, non-jack-ryan)

**Disposition at capture (2026-06-14):** the critique pair on the fire_mage fix converged — jack-ryan Gate-2 = **INFO/APPROVE** (above) + gandalf design Ruling A endorses the fix as MORE design-coherent than anticipated (the guard honors `no_heal_skill` as the glass-cannon fire-mage identity rather than relaxing the constraint to fit a heal role). **No Matt decision is gated by this finding** — it is within rocket's seam + jack-ryan's ADR-002 within-seam authority. The verdict is captured here for the durable Gate-2 record; the commit (`9a46731`) is part of the push-ready bundle pending Matt's push authorization. The **water_mage 1/29 sub-band** item is explicitly NOT resolved by this fix (different root cause: `require_heal_or_hot`, the opposite constraint) — routed to rocket for instrumented diagnosis FIRST, then a separate gandalf ruling (do not rule blind — the same discipline that corrected Ruling A's hypothesized binding constraint).
