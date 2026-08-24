# Dispatch — 2026-08-24 — rocket — X-3 (`vfx_coverage_manifest.json` refresh)

**Status:** PENDING — **routing, NOT a Step-2 blocker.** Sequence at your convenience.
**From:** knight-rider (VFX archetype-binding run close, carve-out #2 § routings)
**To:** rocket (element seam)
**Approved by:** Matt, 2026-08-24
**Pattern:** B (dedicated session; the grading pass is the bulk of it)

---

## Context

The VFX archetype-binding run **SEALED 2026-08-24**. T-A binds 24 canonical VFX archetypes; T-K binds **1,134** kit-skills to them (1,135 is the assigned count; 1,134 is the bound count post-hold — gandalf, L-41). The whole binding rests on a claim in the **Tier-1** layer: that **element parameterization ships with the base binding** — one authored effect, recoloured per element.

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

  ⚠ **Take that instruction seriously — gamora just proved it earns its keep, on this exact run, hours ago.** She was handed two counts in prose (18 skills, and a "corroborating" 6) and told to reconcile them. Neither was the count. **The 6 turned out to be `generation/MIGRATION.md:229` — *"6 Wave-C kits WILL get this tag at S5"* — future tense, not a census at all**, read as a measurement by every downstream reader including me. And the 18 didn't reproduce either: the real population is **21**, of which 18 is merely the ordinal-0 subset that `primary_geometry` happens to read. Three skills were mis-gauged *and* invisible to the assert that was supposed to catch it. **My prose numbers above have exactly the same provenance as hers did.**

- [ ] ⚠ **ROUTED TO YOU BY gamora (X-1 completion, `gamora/v1.4-x1-orbit-spatial-map`): fix the V9 wording in `generation/MIGRATION.md:229`.** The line reads as a census and is actually a forward commitment. It has already been misread once, by me, in a dispatch. **Rewrite it so its tense is unmistakable** — a future commitment and a measured count must not be expressible in the same sentence shape. This is small, it is in your seam, and it removes a live trap rather than documenting one.
- [ ] **Grade the 20 LIVE-slot allow-list elements.** These are the ones that can actually be selected into a season, so they carry the real risk. Each gets `vfx_mapping_tier` + `vfx_catalogue_mapping_clean` + `rationale`, in the existing vocabulary.
- [ ] **Grade the 38 vocab-frozen entries, or state explicitly why they are deferred.** They are reserved for Phase-1 P1 introduction and cannot be selected today. Grading them now is cheap insurance; *not* grading them is defensible — **but the manifest must say which, so the next reader is not left inferring from absence.**
- [ ] **Bump `version` and `generated_date`;** extend `source_attribution` with this pass's basis. A refreshed manifest that still says `2026-05-17` is a lie about its own freshness.
- [ ] Smoke: `pool.py _validate_pool_invariants` still passes; the vocab freeze still enforces; **before/after `d1_status` census across all 100 entries** (see the Principle 6 gate — grading PROMOTES entries the loader had auto-demoted, so the selectable set moves)
- [ ] Tag `rocket/v<X.Y>-x3-vfx-coverage-refresh`

## Grading input — use the run's evidence, don't re-derive it

The sealed spec gives you two things the 2026-05-17 pass did not have:

1. **The Tier-1 surface classes** (§ 3.0): `PAYLOAD-CARRIED` / `TRAIL-BOUNDED` / `FIELD-CARRIED`. Recolour survivability is **not uniform across them** — the binding consequence of record is *"a tinted weapon-trail stays physical; a tinted field IS Eye of Reckoning."* An element that recolours cleanly on a payload may not on a field. If your grading finds that tier depends on surface class, **say so** — that is a manifest-schema finding (a tier-per-surface-class cell), and it belongs to this pass even if the schema change does not.
2. **C-3, measured:** additive stacking blows to white; floor albedo **0.085** reads correctly where 0.20 washes the frame. **Any recolour-survivability judgment taken against the wrong albedo is a judgment taken against a lie.** If your grade rests on rendered evidence, name the albedo it was rendered at.

## Cross-seam contract change? (Principle 6 gate)

**Potentially YES — the manifest is consumed at pool load.**

- ⚠ **A value-only change here IS selection-visible.** `pool.py:95-102` auto-demotes any allow-list entry lacking `vfx_catalogue_mapping_clean` to `eligible` at load (Drift-14 invariant; `element/MIGRATION.md:186`). Grading the 20 ungraded LIVE-slot allow-list elements will PROMOTE them back to `allow-list` and change the set a season can select. **"Only field values changed" is NOT a valid not-applicable reason on this artifact.**
  **Required:** `Round-trip smoke: production-path season generation reading the refreshed manifest → pool load → element selection, with a before/after d1_status census across all 100 entries and an explicit statement of which elements changed status and why.`
- **If you add a field** (e.g. a per-surface-class tier cell), that IS a contract change: **MIGRATION.md required per ADR-004**, plus `Round-trip smoke: production-path season generation reading the refreshed manifest → pool load → element selection, with a field-presence check on the new field and a no-regression check on the existing tier field.`
- Silence on this field is a Gate-1 BLOCK per REVIEW_PROCESS Principle 6.

## Acceptance criteria

- [ ] Counts derived from the artifact and stated — not inherited from this dispatch's prose
- [ ] 20 LIVE-slot allow-list elements graded with rationale
- [ ] 38 frozen entries graded OR explicitly deferred **in the file**, with the reason
- [ ] `version` / `generated_date` / `source_attribution` refreshed
- [ ] Vocab freeze still enforced; **before/after `d1_status` census filed for all 100 entries; every membership change is intended and named**
- [ ] Round-trip smoke green — **`not applicable` is NOT available on this dispatch** (see the Principle 6 gate)
- [ ] Tag cut

## Quality criterion

**Game-quality goal:** that **every element a season can actually roll produces a VFX read the player can identify as that element** — that a water skill looks like water at the gameplay camera and not like a blue fire skill. Tier-1 recolour is the mechanism by which 1,134 bound skills inherit 24 authored effects; the manifest is the only place where "will this recolour actually work" is written down. **An ungraded element is an untested promise**, and it fails on the day a season rolls it.

**Refutation conditions** (surface to knight-rider before executing if any apply):
- The 42/100 or 20-element counts do not reproduce against the file — the finding needs re-derivation, not a grading pass
- The A–E vocabulary cannot express what you actually find — a schema finding, worth more than a forced letter
- Grading requires rendered evidence that does not exist yet — say what would need rendering and at what albedo; **do not grade from imagination and mark it as measured**
- The `pool.py:95-102` auto-demote behavior does not reproduce as described — that would change the Principle 6 gate above, and the gate is stated on my reading, not yours; **check it before you rely on it**
- The manifest turns out to be consumed somewhere ELSE that makes a value-only change contract-visible

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

- jack-ryan Gate-1 DESIGN-MODE: **PASS-WITH-FINDINGS → **amendments applied 2026-08-24**** — Gate-1 batch review, 2026-08-24.
  My not-applicable branch was wrong and was the branch rocket would have taken: `pool.py:95-102` auto-demotes ungraded allow-list entries at load, so grading them **promotes them back** and moves the selectable set. Round-trip smoke is now REQUIRED with a before/after `d1_status` census across all 100 entries.
  Amendments approved by jack-ryan directly under **ADR-002** (dispatch documents are documentation-only). **Nothing in this batch escalated to Matt.**

---

## Completion record

**Status:** COMPLETE — 2026-08-24, rocket.
**Tag:** `rocket/v1.4-x3-vfx-coverage-refresh` · commit `0a07c144` · pushed to `origin/main`.
**Smoke:** `src/reincarnated/element/smoke_x3_vfx_coverage.py` (NEW, in-repo, self-contained) — **45 GREEN / 0 RED**.

### AC-1 — counts derived, not inherited

| Prose in this dispatch | Derived from the artifacts | Verdict |
|---|---|---|
| 42 of 100 allow-list graded | 100 allow-list in `pool.json`; 42 have a manifest entry | reproduces |
| 20 LIVE-slot: fire 6 / water 6 / earth 4 / wind 4 | fire 6 / water 6 / earth 4 / wind 4 | **reproduces exactly** |
| 38 in the three vocab-frozen slots | lightning 12 / holy 14 / shadow 12 | **reproduces exactly** |

Unlike gamora's X-1, the handed figures held. **But 42 was concealing a second number.** The post-load allow-list count is **38**, not 42: `tempest`/`cyclone`/`squall`/`hurricane` are graded Tier C `clean=false` from the Drift-14 wind-storm cull and are demoted on purpose. The demote population is **62, not 58**. "Graded" and "selectable" are different sets that had been used interchangeably.

**Gap provenance (not in the dispatch):** all 58 unmanifested entries entered `pool.json` **2026-06-01** via the WS1A Q18 lock, 15 days after v1.0 was generated. Recorded at the time at `element/MIGRATION.md:185`. A staleness gap, not a grading omission.

### The `pool.py:95-102` gate — checked, not relied on

Auto-demote reproduces exactly as described. **But the gate's consequence does not.** `selector.py:167` builds `active_pool` excluding only `quarantine`, so `eligible` entries were **already selectable** at `1.0` weight vs `D1_ALLOW_LIST_WEIGHT = 2.0`. This is a **sampling-weight change, not a set-membership change**. Measured, N=4,000 seeds × 4 slots — promoted-share: fire 11.7→20.4 %, water 22.6→36.4 %, wind 5.5→10.5 %, **earth 0.0→0.0 %**. Filed for gamora in `element/MIGRATION.md`.

### Before/after `d1_status` census (all 214 pool entries)

| | allow-list | eligible | quarantine |
|---|---|---|---|
| before | 38 | 62 | 114 |
| after | **48** | **52** | 114 |

**10 changes, all promotions, all `eligible → allow-list`, every one intended and named:** `inferno`, `fira`, `thermal`, `aqua`, `hydro`, `torrent`, `glacial`, `chill`, `hydraulic`, `zephyr`. **Zero demotions.** Predicted before running; matched exactly.

### AC-2 — 20 LIVE-slot graded (10 promoted, 10 held back)

Earth gained **zero**: the 29-row substrate inventory has no seismic substrate, so `quake`/`tremor`/`seismic`/`tectonic` are Tier C composite. `whirlwind` held at C — a member of the **culled** drift-14-wind-storm-cluster; grading it clean would have silently re-admitted a culled member from the element side. `sonic` → E (auditory cluster is uniformly non-visual). `shockwave` → C (kinetic mega-cluster, not wind). `ignite`/`combustion` bound by sibling `ignition` (C). `fusion` → C.

**Basis:** catalogue-adjacency at *substrate* granularity + binding sibling precedent. **No effect was rendered; no grade cites an albedo** — per the refutation condition, grades were not invented and marked as measured. Where a better tier needed a render, the worse tier was taken.

### AC-3 — the 38 explicitly DEFERRED in the file, with reason

**Grading them would have broken the freeze this pass was meant to respect.** `_VOCAB_FREEZE_IDS` is a 4-id frozenset; `umbra` is not in `pool.json`, so it enforces **3 of the 38**. The other 35 are held out *incidentally*, by the Drift-14 gate firing on manifest absence. Grading them `clean=true` promotes all 35. Recorded in-file at `deferred_grading`. `vocab_freeze_note` also **corrected** — its "none currently in pool.json" was true on 2026-05-17 and false since 2026-06-01.

### AC-4/5/6/7

`version` 1.0→**1.1**, `generated_date`→**2026-08-24**, `source_attribution` extended with this pass's basis. Vocab freeze still enforced (asserted in smoke). Round-trip smoke green through the production path `pool load → element selection → season slots`. Tag cut and pushed.

### Routed fix delivered (gamora, X-1)

`generation/MIGRATION.md:229` rewritten as a **PROJECTED-vs-MEASURED table** with tense marked, plus a stated convention for all future roster figures in that file. Measured read-only over `corpus.db`, n=1,224 kit-skills, reproduced across five corpus copies: **0** kits carry the `orbit` effect tag (the rule has never fired), **0** carry `placed_lane`/`walls_demand`; separately **21** carry `geometry_value == "orbit"` from elrond's curation. Independently reproduced gamora's 21.

### Findings raised to knight-rider — NOT taken here

1. **Freeze enforcement should be substrate-driven, not a 4-id list.** Selection-visible: `spark` (`substrate_native=lightning`, `flex_slots=["wind"]`, Tier A, clean) survives load as allow-list and **is selectable into the wind slot today** — a live vocab-freeze leak predating this pass. A substrate predicate would demote it and change output for every existing seed. Own dispatch, gamora consulted.
2. **Schema finding, per the dispatch's § "Grading input" invitation: tier depends on surface class.** Six grades are Tier C purely because their identity is *displacement, not colour* — a tinted payload keeps its element read; a tinted field does not. `vfx_mapping_tier` should be a per-surface-class cell. **Surfaced in `schema_findings` rather than forced into a letter; A–E semantics unchanged.**

### Out-of-scope respected

`AOE_GEOMETRIES` **untouched** — verified still 16 entries, `orbit` absent. Vocab freeze not re-opened. No elements added to `pool.json`. No VFX authoring, no archetype work.

`pytest -k "element or pool or selector"`: 529 pass, 7 fail — **all 7 verified pre-existing** by re-running at baseline with only my own paths stashed.
