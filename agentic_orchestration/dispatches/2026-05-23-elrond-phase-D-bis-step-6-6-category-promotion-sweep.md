# Dispatch — 2026-05-23 — elrond — Phase-D-bis Step 6.6 (category-promotion sweep for non-game sources)

**From:** knight-rider
**To:** elrond (Pattern-B execution; data steward / Phase-D-bis amendment)
**Approved by:** Matt 2026-05-23 ("Yes, this is the obvious solution. Please fire Phase-D-bis Step 6.6 — category-promotion sweep for non-game sources.")
**Estimated effort:** ~6–10 hours wall-clock per your own E1 audit estimate (Step 6.6 implementation + Step 7 F4 re-run + acceptance gates). May land in a single sitting or split across two; your call based on Step 7 embedding-cache hit-rate.
**Acceptance:** ~30K–36K rows promoted from `weapon_kind='unknown'` to `weapon_kind='category'`; Step 7 F4 cross-source merge re-runs cleanly on the enlarged pool; v_category_sample grows from 16,699 → ~52K rows with the multi-cultural lineage distribution your audit projected; new acceptance gates pass empirically; MIGRATION.md written; tag cut.

---

## Why this is firing

Your own E1 diagnostic (`agentic_orchestration/elrond/notes/2026-05-23-phase-E-1-bis-E1-lineage-audit.md`) revealed that the 94.46% fantasy_generic figure in Legolas's Phase E-1 PCA was NOT a Step 6.5 lineage-mapper bug (which is sound), NOR a real substrate property — it was a **v_category_sample filter artifact**. Step 4 (named_template routing) is hardcoded to only touch 12 TRPG/MMO/ARPG game sources; museum / encyclopedia / modern-military canonical rows (~35,960 estimated) sit at `weapon_kind='unknown'` and never enter v_category_sample. Phase E-1 ran PCA on 23% of the substrate — the fantasy-source slice only — because the other 77% (the museum/historical fraction that gandalf's cleaning-policy § 5 framework was designed around) was filtered out before the math.

Gandalf authored the Phase E-1-bis verdict at `agentic_orchestration/gandalf/notes/2026-05-23-phase-E-1-bis-design-fit-verdict.md` framing the question as "labels broken vs labels-correct-but-substrate-monocultural." Your E1 audit returned a third disposition (filter-membership artifact). Matt reviewed both and authorized the Step 6.6 fix as the obvious next move.

This dispatch executes the fix you scoped. It does NOT re-open methodology questions (gandalf's A1+D1 lock vs B/C-family choices) — those are deferred until Phase E-1 re-fires on the corrected pool and produces empirical results worth re-evaluating against.

## Required reading before starting

1. **Your own E1 audit**: `agentic_orchestration/elrond/notes/2026-05-23-phase-E-1-bis-E1-lineage-audit.md` — the disposition, the proposed fix scope, the ~52K-row projection, and the recommended acceptance approach
2. **Your Phase D math note** (already authored): `agentic_orchestration/elrond/research/phase-D-cleaning-pipeline-2026-05-23/phase-D-math-note.md` — § 5 backup discipline; § 6 acceptance-gate framework; gives you the precedent for math-anchored gate design
3. **Your Phase D completion summary**: `agentic_orchestration/elrond/research/phase-D-cleaning-pipeline-2026-05-23/phase-D-completion-summary.md` — § 1 footnote already acknowledges the structural gap this dispatch resolves
4. **Cleaning-policy § 5.2** (gandalf): `canonical/story/cleaning-policy-design-2026-05-22.md` — confirms the design intent that museum/encyclopedia/modern-military rows participate in the analysis pool (not just engine-consumption time filter)
5. **Gandalf E1 verdict**: `agentic_orchestration/gandalf/notes/2026-05-23-phase-E-1-bis-design-fit-verdict.md` — for Pattern-6 fidelity framing (this fix preserves "no axis pre-imposition")
6. **Legolas Phase E-1 features deliverable**: `agentic_orchestration/legolas/research/phase-E-pattern-6-2026-05-23/phase-E-1-features.md` — the F2 weight table that surfaced the 94.46% figure (the downstream consumer that v_category_sample feeds)

## Math-before-code

You already did the math in your E1 audit. Confirm or refine the following pre-implementation:

1. **Per-source promotion eligibility predicate.** State the exact SQL predicate for which `weapon_kind='unknown'` rows are eligible for promotion to `category`. Required conditions per your E1 audit:
   - `dedup_status IN ('canonical','unprocessed')`
   - `weapon_kind='unknown'` (not ammo, not unique, not FP-demoted, not already category/named_template)
   - `source_library IN (<explicit historical-sources list>)` — enumerate the full list before coding
   - `canonical_name NOT IN (<Step 5 FP-pattern set>)` — make sure FP-pattern set is the same predicate Step 5 used
   - Optional: `wieldable_humanoid IS NOT NULL OR <reasonable default>` — depends on whether v_category_sample's `wieldable_humanoid IN (...)` filter would re-exclude rows you just promoted

2. **Projected row counts per source** (from your audit table). State expected promotions per source_library so the post-run audit can compare actual-vs-expected:
   - royal_armouries: ~5,631 (the surviving canonicals)
   - met-museum: ~3,844
   - wikipedia: ~8,324
   - wikidata: ~12,319 (NB: most of these will carry lineage=unknown, which is fine for the engine sampler)
   - odin-army-tradoc: ~3,998
   - army-recognition: ~62
   - cataclysm-dda: ~929
   - gta-v-data: ~183
   - **Expected total: ~35,290 rows promoted**

3. **wieldable_humanoid coverage on the newly-promoted rows.** This is the second filter in v_category_sample (`wieldable_humanoid IN ('one_hand','two_hand','shoulder_supported','either')`). What fraction of the newly-promoted museum/encyclopedia/modern-military rows currently have a non-null `wieldable_humanoid` value? If many are null, v_category_sample post-promotion won't grow as much as the 35,290 figure suggests. Decide pre-implementation whether Step 6.6 also needs to populate `wieldable_humanoid` from structured_properties (parallel to Step 6.5 extending mid-pipeline to populate wieldable_humanoid via source-driven rules — per your Phase D completion summary's documented Step 6.5 variance). If yes, scope a 6.6.b sub-step or extend 6.6 to handle it.

4. **Secondary regex fix** (small, rides along). Your E1 audit flagged `(re.compile(r"\b(inca|peru|andean|amazon|brazil|colombia)", re.I), "south_american_indigenous")` as matching "Incantation" and "Amazon" in D&D descriptions, mis-routing ~500 rows. Either:
   - Tighten the regex (`\b(inca|peru|andean|brazil|colombia)\b` — drop `amazon` since it's ambiguous; or require word-boundary endings; or add a negative lookbehind for "incantation"), OR
   - Document the fix is deferred to a separate dispatch to avoid scope creep.
   - Your call. If you take it on, the ~500 rows that currently mis-map need re-labeling — small SQL UPDATE; not load-bearing on the overall Step 6.6 acceptance.

5. **Unknown-lineage sampling pass — self-dispositioning sub-scope (Matt 2026-05-23 follow-up).** Of the ~70,693 non-merged rows in the underlying substrate, ~12,920 (~18%) carry `cultural_lineage_canonical='unknown'`. Your own E1 audit characterized these structurally (wikidata's sparse `country_of_origin` field accounts for ~9,912 of them) but did NOT sample the actual rows. Matt's question: are these rows genuinely unknown, or are they recoverable via better extraction logic?

   **Required as part of this math-note phase:** sample 50 rows from each major unknown-source contributor (wikidata, wikipedia, odin-army-tradoc, met-museum — at minimum; add cataclysm-dda and others if their unknown-bucket size warrants). For each sample, capture `canonical_name + description_text[:500] + structured_properties`. Categorize each row into one of four buckets:
   - **(α) Genuinely unknown** — description too generic ("Sword", "Bow"); no structured cues; no regional vocabulary in name
   - **(β) Regex-recoverable** — description contains a clear regional cue ("Burgundian arming sword", "Naginata from the Edo period") that CULTURE_REGEX_PATTERNS doesn't currently capture
   - **(γ) Structured-field-recoverable** — additional structured fields beyond what Step 6.5 currently consults carry regional signal (e.g., wikidata's `instance_of`, `material`, `subclass_of`, name parsing; met-museum's `place` field if not already consumed; odin's `manufacturer_country` if distinct from `origin_countries`)
   - **(δ) Human-judgment-needed** — ambiguous; cross-cultural; genuinely contested

   Report the per-source distribution across α/β/γ/δ in the math note.

   **Self-disposition rule:** elrond decides scope based on the sample distribution.
   - **If β+γ combined ≥ 20% of any major source's unknown-bucket:** add a Step 6.6.b sub-step that extends the regex/structured-field extraction logic for that source, then re-runs Step 6.5 lineage assignment on the source's currently-unknown rows ONLY (do not touch rows that already have a confident lineage assignment — additive only). Document the proposed regex/field extensions in the math note for Matt visibility before coding.
   - **If β+γ < 20% across all major sources:** unknown disposition is correct for the bulk of those rows. No Step 6.6.b. Document that the diagnostic confirmed unknown is genuine, and proceed with Step 6.6 as authored.
   - **Borderline cases (10-20%):** elrond's call. Erring toward extending scope is preferred (we'd rather Phase E-1 see correct labels than re-fire on partial labels) but cost has to be reasonable. Document the reasoning.

   **Scope of Step 6.6.b if it fires:** must be additive only (no relabeling of rows that already have non-unknown labels), and must complete before Step 6.6 promotes rows to `weapon_kind='category'` so the newly-promoted rows enter v_category_sample with the best-available lineage labels. Step 7 F4 re-run already in scope handles any downstream effects.

Document all five decisions in a math note before coding. Following the Phase D pattern: `agentic_orchestration/elrond/research/phase-D-bis-step-6-6-2026-05-23/phase-D-bis-math-note.md` (create a new sub-directory under elrond/research/ for this work; the Phase D directory should stay frozen as its tag).

## Cross-seam contract change? (Principle 6 gate)

**YES.** This dispatch modifies `v_category_sample` — a view consumed by legolas Phase E-1 pipeline. The view's row count and row composition both change materially:
- Row count: 16,699 → ~52K (projected)
- Composition: 98.6% TRPG/MMO/ARPG game-source → ~36% european / ~33% fantasy_generic / ~16% east_asian / ~25% unknown / smaller buckets (per your E1 audit Q5 projection)
- The `weapon_kind`, `cultural_lineage_canonical`, and other column values remain semantically unchanged on the rows themselves; only the row-membership of the view changes (newly-included museum/encyclopedia/modern-military rows).

**Round-trip smoke required.** Acceptance-criteria includes:
- Round-trip smoke: query `v_category_sample` post-Step-6.6 + post-Step-7-re-run; verify row count matches projection (~52K ± 10%); verify per-source membership counts match your projected table; verify lineage distribution matches projection; verify a sample of 30 randomly-selected newly-promoted rows are genuinely category-eligible weapons (not consumables, not ammo, not FP, not unique-by-canonical-name).

**Downstream consumer impact:** legolas Phase E-1 will re-run against this enlarged pool. That re-fire is OUT OF SCOPE for this dispatch (knight-rider will author a separate legolas continuation dispatch once Step 6.6 + Step 7 re-run lands and is tagged). MIGRATION.md must call out:
- The legolas Phase E-1 deliverables (features.md, axis-discovery.md, axis-loadings.json, clusters.md) ARE now stale and MUST be regenerated on the enlarged pool.
- The DB tables `clusters`, `cluster_membership`, `weapon_knowledge_entries.cluster_id` are still empty (smoke skipped DB writes, full mode died mid-Deliverable-3) so no cluster invalidation needed.
- The gandalf canonical-axis discussion in `canonical/story/hive-mind-protocol-weapon-library-import-2026-05-22.md` § 6.4 is unaffected by this dispatch — methodology lock (F5 PCA-primary) is not amended; only the upstream pool the methodology operates on is corrected.

## Scope

- [ ] `phase-D-bis-math-note.md` written documenting the eligibility predicate, projected row counts per source, wieldable_humanoid handling decision, secondary regex fix disposition, AND unknown-lineage sampling pass with α/β/γ/δ distribution per source + Step 6.6.b self-disposition
- [ ] **(Conditional)** Step 6.6.b implementation script at `agentic_orchestration/elrond/research/phase-D-bis-step-6-6-2026-05-23/scripts/09b_step6_6b_unknown_lineage_recovery.py` IF the math-note sampling disposition triggers it (per math-before-code §5 rule)
- [ ] Step 6.6 implementation script at `agentic_orchestration/elrond/research/phase-D-bis-step-6-6-2026-05-23/scripts/09_step6_6_category_promotion_sweep.py` (numbering continuation from 08_step6_5; runs AFTER 6.6.b if 6.6.b fires)
- [ ] Pre-step backup of `weapon_knowledge_entries` (Phase D math note § 5 discipline)
- [ ] Step 6.6 run executed; log written; row counts captured
- [ ] Step 7 F4 cross-source merge re-run on the enlarged candidate pool (embedding cache reused for stable rows; new embeddings computed only for newly-promoted rows)
- [ ] Secondary regex fix applied to ~500 mis-mapped rows OR deferred-with-documentation
- [ ] Acceptance gates (a)-(d) evaluated per the math note; results documented
- [ ] Round-trip smoke per Principle 6: v_category_sample post-fix → projected-vs-actual comparison; lineage distribution audit; 30-row category-eligibility sample audit
- [ ] MIGRATION.md written at `agentic_orchestration/elrond/research/phase-D-bis-step-6-6-2026-05-23/MIGRATION.md`
- [ ] Phase-D-bis completion summary written
- [ ] Tag: `elrond/phase-D-bis-step-6-6-2026-05-23` (seam-prefix intermediate; local only; do NOT push without Matt approval)

## Acceptance criteria

- [ ] **(a) Promotion-eligibility precision.** Random-sample audit of 50 newly-promoted rows: false-promotion rate (rows that should not have been promoted to category — e.g., consumables, ammo, FP-pattern entries, ambiguous non-weapons) ≤ 2.0% target / ≤ 5.0% hard. Match Phase D Gate (d) misclassification posture.
- [ ] **(b) Promotion-eligibility recall.** Random-sample audit of 50 rows still at `weapon_kind='unknown'` post-Step-6.6: missed-promotion rate (rows that SHOULD have been promoted but weren't) ≤ 5.0%. Anything systematically missed needs to surface as a Phase-D-bis flag or be fixed before tagging.
- [ ] **(c) Step 7 F4 cross-source merge stability.** Pre-existing `knowledge_entry_canonical_merge` entries (1,194 components from your original Phase D Block (e)) remain stable; no spurious re-clustering of previously-merged entries. New cross-source merges from the newly-promoted rows are documented as a delta (additions only, not modifications).
- [ ] **(d) v_category_sample post-fix profile.** Row count: ~52,000 ± 10% (47K–57K). Lineage distribution within ±5 percentage-points of your E1 audit projection (european ~44%, fantasy_generic ~33%, east_asian ~16%, unknown ~25%, smaller buckets ~10%). Per-source membership matches your projected table within ±10% per source.
- [ ] **Round-trip smoke:** v_category_sample query post-Step-6.6 + post-Step-7-re-run; row-count + per-source + per-lineage projection comparisons all pass; 30-row sample category-eligibility audit reports FP rate ≤ 2.0% / hard ≤ 5.0%.
- [ ] **No regression on original Phase D acceptance gates.** Re-evaluate gates (a)-(d) from Phase D on the post-Step-6.6 + post-Step-7 state. FP rate in v_category_sample stays ≤ 1.5% target / ≤ 3.0% hard. Residual duplication stays ≤ 4.0%. Field-coverage floors all ≥ thresholds from your Phase D math note § 6. weapon_kind misclassification rate stays at ≤ 2% on all 3 sub-axes (note: the "category" sub-axis is the one being mutated; the other two should be unchanged).
- [ ] **(Optional, if you take on the secondary regex fix)** South-american-indigenous bucket post-fix carries only the 17 rows that legitimately match (per your audit; the 5 wikipedia + 7 ODIN + 5 from other sources). Currently 509 (with ~500 mis-mapped from "Incantation"/"Amazon").
- [ ] AGENT_STATE.md or equivalent elrond checkpoint updated at session end
- [ ] Tag: `elrond/phase-D-bis-step-6-6-2026-05-23`

## Out of scope (explicit non-goals)

- **Step 6.5 (lineage normalizer) re-run.** Labels are correct; no need to touch the mapper. If you take on the secondary regex fix, that is a one-line code change + targeted SQL UPDATE, NOT a Step 6.5 re-run.
- **Steps 1, 2, 3, 4, 5, 6 re-runs.** Phase D as committed (tag `elrond/phase-D-cleaning-pipeline-2026-05-23`) remains durable. Step 6.6 is purely additive.
- **Step 7 F4 cross-source merge IS in scope** because the newly-promoted category rows become merge candidates against existing TRPG/MMO/ARPG category rows. Re-run only the F4 logic; don't re-run F1 RA (TIERED collapse already executed in Step 2).
- **Phase E-1 re-fire.** Legolas re-running PCA + HDBSCAN on the enlarged pool is a separate dispatch knight-rider authors AFTER this dispatch completes and tags. Your completion summary should explicitly note that Phase E-1 re-fire is queued, not part of this scope.
- **Methodology decisions (F5 lock, A1/B1/C1 choice).** All deferred until empirical results from the re-fired Phase E-1 are in hand.
- **canonical/ story-doc amendments.** Gandalf authors design-side docs; if this work surfaces design-side updates needed, surface to knight-rider at completion for gandalf coordination.
- **DB push to origin.** Tags local-only per ADR-001. Do NOT push without Matt approval.

## Open questions for elrond to resolve + document

1. **wieldable_humanoid coverage** (math-note §3 above). Decide pre-implementation: populate during Step 6.6 from structured_properties (extends Step 6.5 source-driven rules pattern), or accept that some newly-promoted rows won't appear in v_category_sample because of the wieldable_humanoid filter. Document the decision and projected row-count impact.

2. **Secondary regex fix disposition.** Take on or defer? Document.

3. **Step 7 F4 re-run scope.** Re-cluster only the newly-promoted rows against the existing canonical pool? Or full F4 re-cluster of all candidate rows (with embedding-cache reuse)? The former is faster; the latter is more thorough. Justify your choice in the math note.

4. **Tag granularity.** Single `elrond/phase-D-bis-step-6-6-2026-05-23` tag, or split into Step 6.6 sub-tag + Step 7 re-run sub-tag (matching your Phase D block-tag discipline)? Your call; defaults to single tag for a focused amendment, multi-tag for cleaner audit if Step 7 re-run is non-trivial.

5. **wikidata's 80% unknown lineage.** Of the ~12,319 wikidata rows projected for promotion, ~9,912 carry `cultural_lineage_canonical='unknown'`. These will enter v_category_sample with unknown lineage labels. The math-before-code §5 sampling pass directly addresses this — the per-source α/β/γ/δ distribution will tell us whether the wikidata unknowns are genuinely unknown (α-dominant) or recoverable (β/γ-meaningful). The §5 self-disposition rule then determines whether Step 6.6.b fires to recover them. Document the outcome explicitly: either "unknown is design-intended for these rows" (with sample evidence) or "Step 6.6.b fired to recover X rows; remaining unknowns are design-intended."

6. **Step 6.6.b acceptance criteria** (if it fires). What's the success bar for recovery? Suggested floor: of the rows Step 6.6.b targets, ≥ 60% should successfully receive a non-unknown lineage label, and the false-recovery rate (rows that get a wrong lineage label rather than staying unknown) should be ≤ 5% per random-sample audit. If your math note proposes different thresholds, justify.

## What knight-rider does after your return

1. Read your completion summary + acceptance-gate results
2. If acceptance passes cleanly: author the legolas continuation dispatch (Pattern-B) to re-fire Phase E-1 on the enlarged v_category_sample. Same pipeline; new pool. Legolas will produce fresh features.md / axis-discovery.md / clusters.md, this time on the corrected substrate.
3. If acceptance has framing-variance findings (Phase D Block (e) precedent): surface to Matt with disposition options
4. If any gate fails hard: route to jack-ryan + gandalf critique-pair before re-fire
5. After legolas re-fires Phase E-1: review the new axis-discovery output; if axes 2-4 NOW stabilize (gandalf's hypothesis), proceed to Phase E-2 designer-labeling; if not, re-open the gandalf A1/B1/C1 option-set against the corrected empirical evidence
6. Phase D milestone-tag promotion candidate (`v0.2-weapon-library-substrate-cleaned`) deferred to await this Phase-D-bis fix + Phase E-1 re-fire; the milestone-tag should reflect the corrected substrate, not the pre-bis version

## Tag at completion

```
elrond/phase-D-bis-step-6-6-2026-05-23
```

Seam-prefix per ADR-001. Local-only. No push without Matt approval.

## References

- Original Phase D dispatch: `agentic_orchestration/dispatches/2026-05-23-elrond-phase-D-cleaning-pipeline.md`
- Phase D tag: `elrond/phase-D-cleaning-pipeline-2026-05-23` (durable; not modified)
- Phase D commit: `9e7d14b` (durable; not modified)
- Original Phase E-1 dispatch: `agentic_orchestration/dispatches/2026-05-23-legolas-phase-E-1-pattern-6-axis-discovery.md` (PARKED pending this fix + re-fire)
- Phase E-1 crash-triage handoff: `agentic_orchestration/skill_handoff_2026-05-23-phase-E-1-crash-triage.md` (smoke-artifact hypothesis refuted by full-data result; full-data result re-explained by E1 audit)
- Gandalf E1 verdict: `agentic_orchestration/gandalf/notes/2026-05-23-phase-E-1-bis-design-fit-verdict.md`
- Elrond E1 audit (THIS DISPATCH'S TRIGGER): `agentic_orchestration/elrond/notes/2026-05-23-phase-E-1-bis-E1-lineage-audit.md`
- Knight-rider option-set: `agentic_orchestration/knight-rider/notes/2026-05-23-phase-E-1-bis-remediation-options.md` (preserved but partially obviated by E1 audit findings)
- Cleaning-policy (design-side canonical): `canonical/story/cleaning-policy-design-2026-05-22.md` § 5.2 (source-driven mapping rules — Step 6.5 honors these; Step 6.6 honors the same source-driven gating)
- Hive-mind protocol weapon-library-import (design-side canonical): `canonical/story/hive-mind-protocol-weapon-library-import-2026-05-22.md` § 6 Pattern-6 doctrine (preserved; Step 6.6 does not amend)
- Variant-cluster-policy (design-side canonical): `canonical/story/variant-cluster-policy-assignments-2026-05-23.md` (preserved; downstream Phase E-3/E-4 work; not touched)
- ADRs: ADR-001 (tag protocol), ADR-004 (cross-seam coordination via MIGRATION.md)

---

**Signed:** knight-rider (dispatch authored 2026-05-23 per Matt "fire" authorization; Gate-1 ratification skipped per direct Matt direction — this is a Phase-D-bis amendment within elrond's existing Phase D execution scope, fix is additive and rollback-safe per elrond's own E1 audit. Gandalf retained in the loop via verdict preserved in the option-set lineage; not re-invoked because the disposition is a data-correction not a design-amendment.)
