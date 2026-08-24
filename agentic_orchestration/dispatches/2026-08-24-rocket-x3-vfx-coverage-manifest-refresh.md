# Dispatch — 2026-08-24 — rocket — X-3 (`vfx_coverage_manifest.json` refresh)

**Status:** PENDING — **routing, NOT a Step-2 blocker.** Sequence at your convenience.
**From:** knight-rider (VFX archetype-binding run close, carve-out #2 § routings)
**To:** rocket (element seam)
**Approved by:** Matt, 2026-08-24
**Pattern:** B (dedicated session; the grading pass is the bulk of it)

---

## Context

The VFX archetype-binding run **SEALED 2026-08-24**. T-A binds 24 canonical VFX archetypes; T-K binds 1,135 kit-skills to them. The whole binding rests on a claim in the **Tier-1** layer: that **element parameterization ships with the base binding** — one authored effect, recoloured per element.

That claim is graded for **42 of 100** allow-list elements. It is asserted for the other 58.

The sealed spec routes the gap to you (§ 6.2, X-3) and names it precisely: **20 LIVE-slot pool elements** (fire 6 / water 6 / earth 4 / wind 4) are allow-list but carry no `vfx_mapping_tier`; **38 more** sit in the three vocab-frozen slots (`lightning` / `holy` / `shadow`, frozen per `substrate-expansion-decision-2026-05-17.md` § 7, enforced at load-time in `pool.py _validate_pool_invariants`).

**Why this is not urgent and is also not optional.** The slot binding works regardless of grade — Step 2 mints against archetypes, not against element tiers, so nothing in the build wave waits on you. But *"recolour survivability is graded"* is currently true only for the graded 42. The manifest's own tier vocabulary is what makes that sentence checkable, and right now more than half the pool is outside it.

---

## The artifact

`reincarnated-engine/data/seasonal_elements/vfx_coverage_manifest.json` — `version: "1.0"`, `generated_date: "2026-05-17"`, entries carrying:

```
id · vfx_mapping_tier (A–E) · vfx_catalogue_mapping_clean · canonical_pair_leak · substrate_native · rationale
```

Tier semantics are in the file's own `source_attribution`: **A** = direct vendor catalogue · **B** = palette-shift clean · **C** = composite required · **D** = custom-commission, or biological/organic rendering incoherent · **E** = non-visual.

**Do not silently re-define those tiers.** If the grading pass finds the vocabulary insufficient (e.g. a case that is "palette-shift clean but only against a `PAYLOAD-CARRIED` surface"), that is a **finding worth more than a forced fit** — surface it rather than stretching a letter.

---

## Scope

- [ ] **Confirm the counts against the file before grading anything.** The 42/100, the 20 LIVE-slot breakdown (fire 6 / water 6 / earth 4 / wind 4), and the 38 frozen-slot figure all arrived as prose. Derive them yourself from `vfx_coverage_manifest.json` + `pool.json` and state what you got. (Discipline #19.1 — cheapest refuting test; and **derive-don't-hand-list** is now standing build instruction.)
- [ ] **Grade the 20 LIVE-slot allow-list elements.** These are the ones that can actually be selected into a season, so they carry the real risk. Each gets `vfx_mapping_tier` + `vfx_catalogue_mapping_clean` + `rationale`, in the existing vocabulary.
- [ ] **Grade the 38 vocab-frozen entries, or state explicitly why they are deferred.** They are reserved for Phase-1 P1 introduction and cannot be selected today. Grading them now is cheap insurance; *not* grading them is defensible — **but the manifest must say which, so the next reader is not left inferring from absence.**
- [ ] **Bump `version` and `generated_date`;** extend `source_attribution` with this pass's basis. A refreshed manifest that still says `2026-05-17` is a lie about its own freshness.
- [ ] Smoke: `pool.py _validate_pool_invariants` still passes; the vocab freeze still enforces; no allow-list element loses a tier it already had
- [ ] Tag `rocket/v<X.Y>-x3-vfx-coverage-refresh`

## Grading input — use the run's evidence, don't re-derive it

The sealed spec gives you two things the 2026-05-17 pass did not have:

1. **The Tier-1 surface classes** (§ 3.0): `PAYLOAD-CARRIED` / `TRAIL-BOUNDED` / `FIELD-CARRIED`. Recolour survivability is **not uniform across them** — the binding consequence of record is *"a tinted weapon-trail stays physical; a tinted field IS Eye of Reckoning."* An element that recolours cleanly on a payload may not on a field. If your grading finds that tier depends on surface class, **say so** — that is a manifest-schema finding (a tier-per-surface-class cell), and it belongs to this pass even if the schema change does not.
2. **C-3, measured:** additive stacking blows to white; floor albedo **0.085** reads correctly where 0.20 washes the frame. **Any recolour-survivability judgment taken against the wrong albedo is a judgment taken against a lie.** If your grade rests on rendered evidence, name the albedo it was rendered at.

## Cross-seam contract change? (Principle 6 gate)

**Potentially YES — the manifest is consumed at pool load.**

- If entries are added/graded but the **entry shape does not change**: `Round-trip: not applicable because the manifest schema is unchanged; only field VALUES are added to existing entries, and pool-load validation is exercised by the smoke.` State it in those terms.
- **If you add a field** (e.g. a per-surface-class tier cell), that IS a contract change: **MIGRATION.md required per ADR-004**, plus `Round-trip smoke: production-path season generation reading the refreshed manifest → pool load → element selection, with a field-presence check on the new field and a no-regression check on the existing tier field.`
- Silence on this field is a Gate-1 BLOCK per REVIEW_PROCESS Principle 6.

## Acceptance criteria

- [ ] Counts derived from the artifact and stated — not inherited from this dispatch's prose
- [ ] 20 LIVE-slot allow-list elements graded with rationale
- [ ] 38 frozen entries graded OR explicitly deferred **in the file**, with the reason
- [ ] `version` / `generated_date` / `source_attribution` refreshed
- [ ] Vocab freeze still enforced; no element loses an existing tier
- [ ] Round-trip clause satisfied or explicitly not-applicable with a stated reason
- [ ] Tag cut

## Quality criterion

**Game-quality goal:** that **every element a season can actually roll produces a VFX read the player can identify as that element** — that a water skill looks like water at the gameplay camera and not like a blue fire skill. Tier-1 recolour is the mechanism by which 1,135 skills inherit 24 authored effects; the manifest is the only place where "will this recolour actually work" is written down. **An ungraded element is an untested promise**, and it fails on the day a season rolls it.

**Refutation conditions** (surface to knight-rider before executing if any apply):
- The 42/100 or 20-element counts do not reproduce against the file — the finding needs re-derivation, not a grading pass
- The A–E vocabulary cannot express what you actually find — a schema finding, worth more than a forced letter
- Grading requires rendered evidence that does not exist yet — say what would need rendering and at what albedo; **do not grade from imagination and mark it as measured**
- The manifest turns out to be consumed somewhere that makes a value-only change contract-visible

## Out of scope

- **Re-opening the vocab freeze.** `lightning` / `holy` / `shadow` remain frozen per `substrate-expansion-decision-2026-05-17.md` § 7. Grading a frozen entry is fine; unfreezing it is not this dispatch.
- **Adding elements to `pool.json`.** Grading only.
- Any VFX authoring (presentation seam) or archetype work (T-A is sealed law — **HALT to Matt**).
- X-1 / X-2 (`orbit` mapping, `vortex_pull` displacement) — routed to gamora.

## References

- Sealed spec § 6.2 (X-3) · § 3.0 (surface classes) · § 2.3 (C-3 albedo)
- `reincarnated-engine/data/seasonal_elements/vfx_coverage_manifest.json`
- `substrate-expansion-decision-2026-05-17.md` § 7 · `pool.py _validate_pool_invariants`
- `gandalf/requests/2026-08-24-knight-rider-carveout2-step2-build-wave.md`

---

## Gate record

- jack-ryan Gate-1 DESIGN-MODE: **pending at authoring time** — Gate-1 batch review, 2026-08-24.
