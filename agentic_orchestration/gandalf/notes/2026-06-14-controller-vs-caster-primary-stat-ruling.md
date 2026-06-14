# Controller-vs-caster primary-stat ruling — bless the shared cap, retire the legacy invariant

**Type:** design-contract ruling (gandalf seam) — resolves the D6-surfaced `test_role_orientation.py` failures #1–3.
**Date:** 2026-06-14
**Author:** gandalf
**Authority:** Matt-authorized 2026-06-14 ("Take the controller-vs-caster ruling").
**Empirical grounding:** Explore-agent composition audit, 2026-06-14 (full composed profiles + control-coupling trace + pre-D3 git recovery; cited inline).
**Companion docs:**
- `agentic_orchestration/rocket/notes/2026-06-14-d6-surfaced-pre-existing-role-orientation-failures.md` — the surfacing (rocket; routes #1–3 to this ruling).
- `canonical/37-form-bias-diagnosis-and-recovery.md` — the form-bias discipline this rhymes with (differentiate on real axes, not a flat damage scalar).

---

## 0. TL;DR — RULING (b): bless the shared primary-stat cap; RETIRE the invariant

The three failing tests assert *"a controller has LESS primary-damage stat (wisdom/int) than the pure caster."* **Retire that invariant. Do NOT restore the −20 primary differential.** The D3 composition model — which locks the element's scaling stat at 160 for every same-element archetype and differentiates on the 110-point secondary budget — is **more genre-coherent than the pre-D3 hardcoded differential, not less.** rocket rewrites tests #1–3 to assert the differentiation that *actually* defines controller-vs-caster now (equal primary; **higher vitality + lower dexterity/crit**). Composition is unchanged. This is a test-contract change, not a generation-logic change.

---

## 1. The three load-bearing facts (empirical, not assumed)

1. **Primary stat is DAMAGE-ONLY — not control-coupled.** CC application chance, CC duration (root/knockback/silence/chill/shock), and CC magnitude are nowhere scaled by the attacker's wisdom/int. Hard-control duration = the skill's `duration_seconds` param + a flat gear `control_duration_bonus` (`damage_resolver.py:986-987`). Only DoT *tick damage* scales with int/wis (`+0.3%/pt`, `damage_resolver.py:984`) — a damage path, not control. **A controller with less primary stat keeps full control; it loses only incidental damage.** This kills the "double-penalty" objection in *both* directions — and reveals the legacy invariant was never protecting control; it was a pure damage nerf.

2. **Differentiation already survives on secondaries — and it is richer than rocket's note assumed.** rocket framed (b) as "differentiating only on vitality." The audit shows it is vitality **AND dexterity**: earth_controller vs earth_caster = **+10 VIT, −11 DEX**; fire_controller vs fire_mage = **+20 VIT, −16 DEX** (at equal primary 160). DEX maps to crit-chance + dodge. So the current controller is **tankier and steadier-damage (low crit)**; the caster is **squishier and swingier (high crit)**.

3. **Pre-D3 differential (recovered from git `31f2c14`):** controller = −20 primary / +20 vitality, with the explicit comment *"Phase 2 controllers: −20 primary-damage stat, +20 vitality vs damage counterpart."* D3 collapsed the primary delta (140→160) and trimmed the vitality premium (90→80).

## 2. The ruling and why (genre DNA decides it)

**The primary/core stat is NOT how the ARPG canon differentiates a control build from a damage build of the same caster family — and encoding it that way makes the controller a strictly-worse caster.**

- **Diablo III Wizard / Diablo IV Sorcerer:** Intelligence is the single core stat; *every* build — Slow-Time/Frost control or Archon nuke — stacks it to the cap. You never take *less* Int to be a controller.
- **Diablo II Sorceress:** a Frozen-Orb control build and a Fireball nuke build draw from the *same* stat allocation; identity lives in the skill tree.
- **Path of Exile:** a curse/control-leaning build and a crit-nuker of the same class share the same core-attribute passives; identity is gems/clusters/ascendancy. Speccing *less* Int for "control" would be strictly worse — the canon never does it.

The through-line: **core stat is maxed by all builds of a caster family; control-vs-damage identity lives in the SKILL KIT, with crit/defense distribution as the supporting lean — never in a reduced core stat.** The pre-D3 "−20 primary" was the genre *anomaly*. D3 corrected it.

**And D3's relocated differentiation is the more interesting one.** Pre-D3, the controller was just "the nuker with less damage and more HP" — a linear downgrade. D3's controller is a **low-variance tanky battle-mage** (max core damage stat, low crit, high vitality — stands in the fray locking things down) against the caster's **high-variance glass-cannon nuker** (max core damage stat, high crit, squishy — artillery). That is a *real* archetypal split, and it is the genre-classic one.

**The differentiation was never the stat block's job to carry.** Controller-vs-caster identity is the SKILL KIT (control skills vs nuke skills, handled by role-orientation skill allocation). The stat block only needs to *lean* correctly — tankier/steadier for the controller — which it now does. The legacy test over-indexed the stat block to carry archetypal weight that lives in the kit.

## 3. The cert-wave rhyme (why this is the same lesson twice)

D3 differentiates controller-vs-caster on **vitality (Defensive axis) and crit-variance (Variance axis)** — the exact axes the new 8-axis *spatial* engine discriminates. The pre-D3 model differentiated on a **flat primary-damage scalar** — precisely the 1D-legible, spatially-blind dimension the whole cert wave (and the form-bias diagnosis, doc 37) is retiring. Restoring the −20 primary would re-import the flat-scalar habit into the stat layer at the very moment we are deleting it from the combat layer. **Retiring the invariant is consistent with the project's spine; restoring it would fight it.**

## 4. What rocket does (test-contract change; composition UNCHANGED)

Rewrite the three failing assertions in `tests/test_role_orientation.py` to lock the *real* contract:

- `test_..._controller_has_less_X_than_..._caster` (#1, #2) → assert **equal primary** (`controller.primary == caster.primary == 160`) AND the live differentiation: `controller.vitality > caster.vitality` AND `controller.dexterity < caster.dexterity`.
- `test_control_class_uses_controller_stat_template` (#3) → assert the controller template is selected AND carries the higher-vitality / lower-dexterity lean vs the damage-caster — NOT a lower primary.

No `config/roles.yaml` change, no composition change. The `_PRIMARY_STAT_ALLOCATION[scaling_attribute] = 160` primary-first rule is **ratified** as the engine's stat-composition philosophy: *your element's scaling stat is your primary, you max it, your role shapes the remaining 110.* Low gate (no production behavior changes; tests encode a ratified contract) — jack-ryan aware as a Gate-2 doc-grade item, not a behavior gate.

## 5. Tuning follow-ons (named; NOT folded into this ruling)

- **Vitality premium thinness (tuning, not structural):** the earth controller's survivability premium is now +10 VIT (was +20). If playtest/sim shows controllers feel too squishy, the lever is the **`control` role vitality floor** (raise from 80) — NOT the primary-stat differential. Recognition→validate→commit: gate on Defensive-axis (Axis-4) separation once the spatial engine measures it.
- **Cross-element status-resist asymmetry (separate ruling owed):** the audit surfaced that fire_controller has wisdom 5 → ~1% own status-resist, while earth_controller has wisdom 160 → ~32% — a *control archetype* that is highly susceptible to control, an artifact of fire's scaling stat being int (wisdom becomes a dump stat). Is that a feature (fire = volatile/control-prone) or an incoherence (a controller bad at resisting control)? **Separate gandalf design question** — routed, not ruled here.

## 6. Disposition

- **Ruling: (b) RETIRE the invariant.** rocket rewrites tests #1–3 per §4 (warm rocket session). Composition unchanged.
- **#4 (B6 skill-count / fire_mage retry-fail)** and the **theme-element-vs-flavor-pool drift** remain separate gandalf design-contract confirmations — NOT resolved by this ruling.
- **Status-resist cross-element asymmetry (§5)** → separate gandalf ruling, queued.
- KR: when batch-planning, the generation-triage unit = this test-rewrite + #4 + theme-element + the Q4 code-flip, all rocket-seam, gandalf-contract-gated.

---

**Signed:** gandalf, 2026-06-14
**For:** the controller-vs-caster primary-stat ruling — bless the D3 shared primary cap and retire the legacy "controller has less primary stat" invariant, because primary stat is damage-only (not control-coupled), the ARPG canon maxes the core stat for all builds of a caster family and differentiates on skills + crit/defense (never a reduced core stat), and D3's relocated vitality/crit-variance differentiation lands on the very Defensive/Variance axes the spatial engine discriminates — the same flat-scalar habit the cert wave exists to retire.
