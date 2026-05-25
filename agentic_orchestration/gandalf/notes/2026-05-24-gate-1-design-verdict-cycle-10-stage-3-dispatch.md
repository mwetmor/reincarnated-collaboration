# Gate-1 Design-Side Verdict — Cycle 10 Stage 3 Execution Dispatch

**Reviewer:** gandalf (design-side critique-pair)
**Date:** 2026-05-24
**Under review:** `agentic_orchestration/dispatches/2026-05-24-elrond-cycle-10-stage-3-v1-scope-materialization.md`
**Spec:** `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` (D1-D7 LOCKED)
**Pattern:** A-deep
**Mode:** Gate-1 DESIGN-MODE pre-fire critique
**Counterpart:** jack-ryan firing in parallel on process-side

---

## VERDICT: PASS-WITH-AMENDMENTS

The dispatch faithfully executes D1-D7 + Architecture B + Option α/β/C. Composition policy is correctly cited, scope boundaries are clean, downstream gates are correctly enumerated, the v1_scope_composition_trace JSON schema captures what Phase 5 cohesion-coalescence + Stage 3.5 gap-fill targeting + post-mortem evaluation will need. The methodology-consult sequencing per Discipline #18.2 (consult AFTER baseline) is correctly applied — Phase 1 legolas Mode A fires AFTER Stage 1+1.5+2+2.5 baseline, BEFORE Phase 2 execution.

**Five amendments warranted before publish-to-fire-ready.** None are blocking; all are tightening that pays back at Phase 2 execution or downstream re-sample.

---

## Amendments (numbered; ordered by load-bearingness)

### Amendment 1 — Tier-S row count discrepancy (dispatch § 2 vs policy § 11.1)

**Issue:** dispatch § 2 cites "Tier S 1,126" but composition policy § 11.1 cites "Tier S 1,065". 61-row delta unexplained. The classifier output in § 2 then says "1,126 Tier-S rows" classified into 449 handheld + 316 siege + 130 accessory + 125 armor + 52 art + 31 other + 23 ammo = 1,126. So the dispatch number is internally consistent with the classifier output, but the composition policy spec disagrees.

**Risk:** Phase 2 sampling against wrong Tier-S denominator changes auto-include count expectation, could mask under-inclusion bug at smoke-test gate (§ 8 says "100% of Tier-S handheld inclusion" — but against what denominator?).

**Remediation:** Add one line at dispatch § 2 or § 4.1 reconciling the delta — e.g., "Tier-S count moved 1,065 → 1,126 between composition policy authoring and pre-Stage-3 classifier run; classifier-output denominator is binding for Phase 2." OR confirm the policy doc number was a snapshot lag and the 1,126 is correct. Either is fine; the explicit reconciliation is what's missing.

### Amendment 2 — D1c excluded-rows trace flagging (dispatch § 4.1)

**Issue:** Dispatch § 4.1 says D1c excluded rows get `composition_trace.notes = "D1c excluded — scope deferred to v1.1+"` — but the JSON schema § 3.4 has no `rule` enum value for D1c-excluded rows. Schema enumerates only INCLUSION rules. For excluded rows, what's `rule`? `null`? An omitted column? A new `rule: "d1c_excluded_scope_deferred"` enum value?

**Risk:** Phase 5 cohesion-judge OR future v1.1+ re-sample post-armor-slot work needs to find these rows by trace query. If they're flagged only by free-text notes, they're not queryable. If `composition_trace` is NULL for `v1_scope = 0`, the excluded-with-reason becomes lost data.

**Remediation:** Add `d1c_excluded_scope_deferred` to the `rule` enum in § 3.4, OR explicitly state in § 3.4 that `v1_scope = 0` rows have `composition_trace = NULL` and exclusion-reason lives elsewhere (e.g., derived from `weapon_kind_classified_subtype` column at query time). Pick one; document.

### Amendment 3 — Sketch F 4-anchor gap-fill flag missing from JSON schema rule enum

**Issue:** Dispatch § 3.5 distribution-report section bullet "Sketch F anchor coverage" correctly identifies that 4 of 12 substrate-thin anchors (Hattori Hanzō / Lu Bu / Moctezuma / Gilgamesh) are queued for Stage 3.5 gap-fill per D5. Good. But the JSON schema § 3.4 `rule` enum has `sketch_f_anchor` (for substrate-resident anchors) and `stage_3_5_gap_fill_pending` (generic) — there's no specific flag distinguishing **substrate-resident Sketch F anchor** from **substrate-missing Sketch F anchor routed to Stage 3.5**. The two are operationally different post-Phase-2:
- Substrate-resident: ALREADY in v1_scope at Phase 2 completion
- Substrate-missing: NOT in v1_scope at Phase 2 (because the substrate row doesn't exist); routes to Stage 3.5 author-and-insert

**Risk:** Stage 3.5 dispatch needs to target precisely the 4 missing anchors. If they're not distinctly flagged at Phase 2, gandalf has to re-derive the gap-list from policy § 5.2 table at Stage 3.5 dispatch authoring — manual lookup; error-prone.

**Remediation:** Either (a) add `sketch_f_anchor_substrate_missing_stage_3_5_target` as a distinct enum value alongside `sketch_f_anchor` and `stage_3_5_gap_fill_pending`, OR (b) in § 3.5 distribution-report section, require the gap-cell list to include a **named-bearer gap-list subsection** explicitly listing Hattori Hanzō / Lu Bu / Moctezuma / Gilgamesh as Stage 3.5 targets. (a) is more queryable; (b) is lighter-weight. Either resolves the targeting gap.

### Amendment 4 — Option C cross-attribute substrate flag at sampling boundary (dispatch § 4.5)

**Issue:** Dispatch § 4.5 says Option C "cross-attribute substrate permitted with ω-penalty signal flagged in `composition_trace.matching_policy = 'option_c_cross_attribute_omega_penalty'`." Composition policy § 3.3 specifies Option C applies to **Red Mage (melee-INT)** / **Monk-archetype (melee-WIS)** / **Holy Knight (melee-WIS-mixed)** — three specific hybrid cells.

What's not specified in the dispatch: at Phase 2 sampling, how does the sampler KNOW which substrate row counts as "cross-attribute" for these cells? The composition policy Cell roster at § 4.1 says Cell 15 Red Mage = `(melee, high, flat, INT)` — but if the sampler is pulling STR-melee substrate (per policy § 4.1 Cell 15 lock: "Phase 5 cohesion-judge composes over STR-melee substrate base + INT-flavored kit"), then EVERY substrate row going to Cell 15 is cross-attribute by construction.

So the Option-C ω-penalty trace is ALWAYS-ON for Cells 15, 23, and Holy Knight, not a per-row branch. Dispatch reads as if it's a per-row decision; it's actually a per-cell architectural fact.

**Risk:** Sampler implementer (elrond) reads § 4.5 and tries to write a per-row Option-C branch — wasted dev cycle; potential misclassification if the per-row logic mis-tags borderline rows.

**Remediation:** Tighten § 4.5 Option C bullet to: "Option C cells (Cell 15 Red Mage / Cell 23 Monk-archetype / Holy Knight) — substrate pulled from primary-attribute-of-physical-vector pool (e.g., STR-melee for Red Mage); ω-penalty flag set on ALL rows entering these cells via `composition_trace.matching_policy = 'option_c_cross_attribute_omega_penalty'` by construction, not per-row evaluation." This makes the architectural fact explicit and saves elrond a branch.

### Amendment 5 — military_modern trim weight not yet bound; smoke-test will surface but flag earlier

**Issue:** § 4.2 says "sampling weight reduced ~80%" with the explicit caveat that the specific weight gets recorded in `sampling-algorithm-rationale.md` at Phase 2 launch. § 15 lists this as open question for elrond+gandalf to finalize. That's correct routing.

But composition policy § 1.2 + § 2.1 set the target as "military_modern ~5-8% of v1_scope" (slight trim from substrate's 8.4%). An 80% sampling-weight reduction will produce ROUGHLY 2,258 × 0.20 = ~450 military_modern Tier-A rows out of an estimated 1,700-3,100 v1_scope = 15-26% share. That's WAY above the 5-8% target unless the constrained-sampling against the target weight overrides the per-row sampling weight.

This is internally resolvable (the constrained-sampling against per-axis target weight will trim further) but the 80% number in § 4.2 + the 5-8% target in policy § 2.1 don't compose obviously. The naive reader (or the sampler at first pass) might pick 80% trim, see 15-26% military_modern share, and not know whether that's by-design or a bug.

**Risk:** Phase 2 smoke at § 8 says "flag any axis where actual >±5pp from target" — military_modern at 15-26% vs 5-8% target trips smoke as +7-21pp deviation, smoke-gate fails, design-call re-engagement. Avoidable if § 4.2 names the relationship between per-row sampling weight (80% reduction) and per-axis target weight (5-8%).

**Remediation:** Add one sentence at § 4.2 end: "The 80% sampling-weight reduction is the INITIAL trim; final military_modern v1_scope share is further constrained by per-axis target weight § 2.1 (5-8%) at the constraint-satisfaction layer of the sampling algorithm. Phase 2 smoke § 8 measures against the per-axis target, not the per-row weight."

---

## What landed well (worth preserving on amendment iteration)

1. **JSON schema § 3.4 covers the right vocabulary** for Phase 5 cohesion-coalescence + post-mortem + Stage 3.5 gap-fill targeting + future re-sample post-enrichment. The `axis_contributions` sub-object is the right shape; the `matching_policy` enum maps cleanly to Option α/β/C; the `filter_passes` array supports future genre-filter extensibility per Architecture B.
2. **Phase 0b scope-and-owner assignment to gandalf is correctly sized** (~30 min). The substrate-fit lookup for `accessory_weapon_integrated` → parent-weapon-kind compatibility is exactly the kind of cultural-tradition + mechanical-fit cross-reference that's design-side, not data-eng-side. Tsuba/menuki/quiver/bayonet-lug → katana/wakizashi/tanto/bow/crossbow/rifle/musket mappings are within gandalf operating-knowledge. I accept this owner assignment.
3. **Sidecar B / Stage 3.5 / Stage 4 are correctly out-of-scope for Stage 3 v1 sampling** and correctly flagged in composition_trace for downstream re-sample. The "fires AFTER Sidecar B + Stage 3.5 + Stage 4 land; separate dispatch at that point" framing for Stage 3.7 re-sample preserves substrate optionality per Variant C.
4. **The 5-tuple cell-pair sharing (§ 4.4) correctly lists all 5 routing-ambiguous pairs** matching composition policy § 4.2 verbatim. Floor accounting respects the shared 4-tuple substrate — the architectural decision per D3 Option A is correctly executed.
5. **Architecture B substrate-genre-flagging via the new `v1_scope_genre_filter` column** is exactly the right shape. The column is extensible for future commercial profiles (sci-fi / cyberpunk / future-historical) per Architecture B § 6.2 without schema-migration on the v1 substrate.
6. **The legendary canonical-pair set-bonuses awareness** is correctly DEFERRED (per § 6: "no engine code touched"; per § 12 disciplines: per future canonical doc per § 6.4 of policy). Stage 3 substrate curation does not need to materialize legendary-pair tagging — that's downstream loot architecture work. Correct scope discipline.

---

## Items I considered but determined NOT amendment-worthy

- **Stage 4 mythological-NULL rescue flag mechanism (§ 4.9):** dispatch correctly states these get `composition_trace.rule = 'stage_4_mythological_rescue_pending'` on the currently-NULL-typed mythological rows. Schema § 3.4 enumerates this rule. Clean.
- **Sketch F substrate-resident anchors (8 of 12)**: dispatch § 3.5 says these report "9 of 12 substrate-present." Policy § 5.2 table shows 12 anchors, 4 marked "YES Stage 3.5 gap-fill required" leaving 8 substrate-resident. 9 vs 8 — one-row delta, possibly Stage 1.5 extracted_named_bearer surfacing an anchor not in the original 12 OR my count being off-by-one. Not load-bearing; just note for the dispatch.
- **Tier-3-lineage filtering (Mode-C contamination):** § 8 post-population smoke correctly verifies "Tier-3-lineage: 0 rows in v1_scope via named-mythological-match path." Correct. Discipline #25 semantic-layer rep-audit working at consumption boundary as intended.
- **No drift on universal archetypal naming OR bi-modal form library lock.** These are Phase 5 concerns, not Stage 3 substrate-binding concerns. Correctly out-of-scope.

---

## Rationale

The dispatch is correctly authored against the locked composition policy and Architecture B. The five amendments are tightening — not corrections of design-intent fidelity. Knight-rider can integrate these amendments inline (each is a 1-2 line edit) and publish-to-fire-ready, OR can ship as-is and accept the resulting smoke-test re-engagement at amendments 1, 4, 5 (amendments 2, 3 are data-quality and don't trip smoke; they manifest as Phase 3 re-derivation work for gandalf).

Recommendation: **integrate all five amendments inline; re-publish; fire.** Cost is ~15 min of dispatch edits vs ~30-60 min of re-engagement later. Pattern A-deep critique-pair is doing its job at the cheapest boundary.

---

## Decision-routing per Matt 2026-05-23 hive-mind directive

Within design-side critique-pair authority. No Matt escalation needed — these are amendment-class findings, not BLOCK-class. Knight-rider integrates verdict + jack-ryan verdict; knight-rider decides publish-to-fire-ready vs revise.

---

**Signed:** gandalf
**For:** Gate-1 design-side critique-pair clearance on Cycle 10 Stage 3 execution dispatch
**Verdict:** PASS-WITH-AMENDMENTS (5 amendments; all tightening; none BLOCK)
