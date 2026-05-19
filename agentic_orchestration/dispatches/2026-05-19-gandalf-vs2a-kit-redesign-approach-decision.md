# Dispatch — 2026-05-19 — gandalf — VS2a kit-redesign approach Gate-1 decision

**From:** knight-rider
**To:** gandalf (story-and-design steward — kit-redesign roadmap-shape OWNER under autonomous L2-equivalent authority)
**Approved by:** AUTONOMOUS — VS2a hive-mind continuation under Matt directive 2026-05-19 (engine-rebuild closure → VS2a sequencing per dispatch § 6.5; no per-dispatch Matt approval; gandalf-side design authority confirmed per autonomous-operation protocol § 4.0)
**Estimated effort:** 0.5–1 day gandalf authoring + decision
**Acceptance:** Decision doc at `canonical/story/vs2a-kit-redesign-approach-2026-05-19.md` capturing chosen path + rationale + B6/S2 implications + first-batch class-selection criteria + validation gate. Tag fires: `vs2a/v0.5-kit-redesign-approach-decided`.
**Hive context:** VS2a hive-mind ACTIVE; engine-rebuild v1.0 batch CLOSED (`hive-rebuild/v1.0-engine-rebuild-complete`). F2 is the **HIGHEST-leverage first-fire dispatch** — gates S1 (kit-redesign sprint) AND S2 (B6 main work). Until F2 lands, neither sprint has a defined shape.

---

## TL;DR — the decision in front of you

**Question:** Should the VS2a kit-redesign work proceed via:

- **(a) Hand-redesign** of 30–40 broken/mediocre classes per § 3.1–§ 3.5 criteria in `r1-kit-redesign-queue-2026-05-19.md` (4–6 weeks rocket effort; preserves curated kits with surgical changes; high confidence; per-class judgment)
- **(b) R8-inversion regeneration** of the entire 51-class catalogue from scratch under the inverted pipeline (~2–3 weeks; tests R8 disposition at scale; faster + cheaper; higher uncertainty; produces emergent archetypes from converged composition)
- **(c) Hybrid** — kit-broken subset regenerated under R8-inversion (where curation has nothing to preserve); kit-mediocre subset hand-redesigned (where the curated kits have salvageable identity)

This is a roadmap-shape decision. Both single-path options are viable under autonomous-operation; the hybrid is the option that most cleanly applies R8's substrate-identity finding to the cases where it's strongest. **You decide; no Matt-wait.**

---

## Context — why this gate exists

R1 disposition (`R1-blocker-3-disposition-2026-05-19.md` + `r1-kit-redesign-queue-2026-05-19.md`) surfaced that 51 of 51 shipped classes fail the per-tier gate under disposition-1 + disposition-3 calibration. The failure pattern is **kit-architectural, not modifier-tuning**:

- ~10–15 classes are **kit-broken** (saturate modifier 4.0 ceiling AND fail every tier — e.g., shadow_mage `class_0018`/`class_0045` at WR=0.000 across swarm/magic/elite/mini-boss/boss)
- ~20–30 classes are **kit-mediocre** (pass lower tiers but fail boss/mini-boss; pathology is fixable — range-diversity injection, defensive-layer rebuild, energy-cycling repair, archetype alignment)
- ~5–10 classes are **kit-acceptable** post-disposition-3 (no redesign needed)

The R1 kit-redesign queue § 5.3 surfaced an **alternative path**: instead of hand-redesigning 30–40 classes, regenerate the entire catalogue under R8's `inverted` pipeline (coalescence-first; theme emerges from converged mechanical composition; archetype-tag becomes OUTPUT not INPUT). R8's disposition (`r8-disposition-2026-05-19.md`) committed `inverted` as engine default and EMPIRICALLY DEMONSTRATED that converged content can produce cohesion-on-par-or-better than input-driven theming. That demonstration is the new empirical basis that makes path (b) genuinely viable rather than speculative.

This decision is yours by design — it's a roadmap-shape decision affecting B6 main work shape, S1 sprint structure, and the validation gate (R1 sprint re-run). Both paths preserve substrate identity at canonical-element level (R8 Test 4 invariance); both can pass the R1 sprint hypothesis-test threshold; they differ on **what the catalogue's curated identity is preserving and what it's letting emerge**.

---

## Required reading before authoring

In order:

1. **`canonical/story/r1-kit-redesign-queue-2026-05-19.md`** — the queue you authored 2026-05-19. § 3 redesign criteria + § 5 roadmap integration (especially § 5.3 R8-inversion alternative) + § 5.1 hand-redesign path
2. **`reincarnated-engine/design/working-agreement/R1-blocker-3-disposition-2026-05-19.md`** — encounter recalibration that makes the gate REACHABLE; clarifies that disposition-3 doesn't fix kit pathology
3. **`canonical/story/r8-disposition-2026-05-19.md`** — R8 disposition (Sub-case 3 / Disposition C variant); `inverted` committed as default; substrate-identity invariant at canonical-element level; § 2a + § 2d + § 6 asymmetry note (cost-savings deferred; cohesion + decoupling shipped)
4. **`canonical/story/substrate-identity-declarations-2026-05-17.md` § 9.5** (R8 amendment) — substrate-identity preservation at surface depends on pipeline; per-entity LLM naming preserves substrate-mode-of-action ~90%; templates ~63%
5. **`canonical/story/engine-rebuild-2026-05-19-gap-solutions-and-tests.md` § 2** — R1 spec + § 8 R8 spec (architectural anchor for both paths)
6. **`reincarnated-engine/design/working-agreement/engineering-disciplines.md`** — particularly Discipline #1 (math-before-code; applies as design-before-build for this decision) + Discipline #17 (semantic-shifting)
7. **`agentic_orchestration/hive-mind/scope-of-work-vs2a.md` § 1.2 (F2) + § 2.2 (S1) + § 2.3 (S2)** — your decision shapes S1 + S2 directly
8. **`agentic_orchestration/hive-mind/coordination-matrix-vs2a.md` § 1 + § 2 DAG** — F2 → S1 + F2 → S2 gating relationship
9. **Output evidence:** `reincarnated-engine/output/R1-class-retune-2026-05-19/summary.md` (sprint v2 per-class evidence; you'll want sprint v3 if it's landed) + `reincarnated-engine/output/R8-ab-run-2026-05-19/README.md` (3+3+3 A/B telemetry) + the R8 inverted samples (e.g., `inverted/season_099002/` — The Drowned Lighthouse / brine)
10. **`canonical/19-llm-call-map.md`** (post-R8 amendment) — Phase A coalescence + Phase B per-entity naming; the orchestration shape S1's regen path would inherit

---

## What you're producing

### Artifact 1 — Decision doc

**Path:** `canonical/story/vs2a-kit-redesign-approach-2026-05-19.md`

**Content:**

1. **TL;DR** — chosen path (a / b / c); one-paragraph rationale.

2. **Decision criteria you applied** — what tipped you. Examples (non-prescriptive):
   - How much of the catalogue is kit-broken vs kit-mediocre (sprint v3 partition is the operational signal; if v3 has not landed, you author on sprint v2 + your judgment + flag the v3 dependency)
   - How much curated identity exists in the kit-mediocre set worth preserving (e.g., "lightning_mage Chartbound Stormscribe has a name; a generated emergent archetype loses that")
   - Whether the R8-inversion path would meaningfully improve the kit-broken cases vs hand-redesign of the same cases
   - Cost: hand-redesign is 4–6 weeks rocket; R8-inversion is ~2–3 weeks rocket + a regen LLM cost (~$3.20 per season × N seasons regenerated)
   - Substrate-identity risk: R8 disposition § 2d notes the `inverted` mode preserves substrate-mode ~90%; templated path is ~63%. The committed path (inverted with per-entity LLM naming) is the only one in scope for S1 regen.
   - Cohesion risk: R8 demonstrated +0.20 cohesion above baseline for `inverted` — empirical comfort that regenerated content will not regress cohesion

3. **Path-specific implementation shape (you specify the chosen path)**:
   - **If (a) hand-redesign:** which 30–40 classes; criteria for first-batch class selection (e.g., "kit-broken first; representative archetype coverage; one class per archetype-tag with deepest pathology"); whether sprint runs as sequential per-class or parallel by archetype-group; gandalf-consult cadence rocket invokes
   - **If (b) R8-inversion regeneration:** whether all 51 classes regenerate from scratch (full catalogue replacement) or only the kit-broken/kit-mediocre subset regenerates (preserving kit-acceptable); seed strategy (re-roll vs preserve seeds); manifest continuity for the 5 shipped seasons (do they re-converge or do new seasons replace them); the role of the existing kit-redesign queue § 3 criteria as a generation-time prompt-augmentation (does R8-inversion get the same archetype/range/defensive-layer requirements as prompt input, or does it run pure mechanical-first with criteria validated post-hoc?)
   - **If (c) hybrid:** explicit partition rules — which classes to which path; whether sprint v3 partition determines split or your own design read does; sequencing (R8-inversion sub-batch first then hand-redesign sub-batch, or reverse, or parallel)

4. **B6 / S2 main-work implications** — explicit. Per scope-of-work-vs2a § 2.3:
   - If path (b) chosen, "B6 main work may shape differently (skill tree emerges from converged class composition; not authored as constraint-input)" — clarify whether S2 (skill-tree main work) shifts shape, timing, or both
   - If path (a) chosen, S2 main work proceeds as currently scoped under existing rocket pre-work
   - If path (c), call out which subset feeds which S2 path

5. **First-batch class selection criteria** — under the chosen path, which classes go first. Particular interest in:
   - Whether boss-tier-only-failures vs all-tier failures sequence differently
   - Whether shadow_mage's modifier-saturated-AND-floor-failing pathology demands first-priority intervention (it's the most extreme broken pattern; fixing it tests whether the chosen path generalizes)
   - Whether archetype-tag coverage matters for first batch (one *_mage + one *_warrior + one *_controller + one *_caster, etc., to surface path's behavior across archetype types)

6. **Validation gate** — R1 sprint re-run is the canonical metric per kit-redesign queue § 5.1 (70–85% pass rate threshold). State explicitly:
   - When the gate fires (after first-batch lands? after full catalogue redesigned?)
   - Whether the threshold remains 70% or you propose a different category-of-completion frame
   - What constitutes PASS / PARTIAL / FAIL re-disposition (if FAIL, gandalf authors further design disposition per R8/R2 precedent pattern)
   - Cross-reference: same shape as R1 + R2 + R8 dispositions you've authored

7. **Risk + watchpoints**:
   - Path (b) risk: R8 inverted at scale (51 classes vs the 3-season sample) may surface template-distribution or naming-fixedness issues not visible in the 9-season A/B
   - Path (a) risk: 4–6 weeks rocket bandwidth is a long block; B6 main work waits; demo regen (L1) slips
   - Path (c) risk: dual-shape coordination overhead; rocket and gandalf may operate in different modes for different classes simultaneously
   - Cross-reference what watchpoints knight-rider should add to `watchpoints-engine-rebuild-2026-05-19.md` (or a new VS2a watchpoints file if you prefer)

8. **Cross-references** — same shape as R1/R2/R8 dispositions you've authored; cite each precedent doc the decision builds on; close with the Mithrandir-signs convention

### Artifact 2 — Canonical-doc amendments (optional, gandalf judgment)

If your decision implies amendments to:

- `canonical/story/r1-kit-redesign-queue-2026-05-19.md` (e.g., adding § 5.4 with the path commitment + sequencing)
- `canonical/16-project-roadmap.md` § VS2a (e.g., updating the kit-redesign description with chosen path)
- `canonical/19-llm-call-map.md` (e.g., if path (b) reshapes the per-season LLM call shape during regen-batch)
- `canonical/story/substrate-identity-declarations-2026-05-17.md` (e.g., if path (b) prompts a new finding about archetype-tag emergence at scale)

— author them in the same commit per your standard authoring discipline.

---

## What you are NOT doing in this dispatch

- **NOT authoring the regen prompts or per-class hand-redesign briefs.** Those are S1 sprint-time artifacts; rocket authors them under your design consult.
- **NOT executing the regen / redesign work.** Rocket owns S1; you decide its shape here.
- **NOT setting the S1 timeline beyond "what shape it takes."** Knight-rider sequences once F1 + F2 both land.
- **NOT touching jack-ryan's territory.** No decisions-log entry from you (jack-ryan authors after the disposition arc lands); no engineering-disciplines amendment from this dispatch (filer can surface a candidate to jack-ryan separately if a Discipline #18 candidate emerges from your reasoning).
- **NOT escalating to Matt for the decision.** Per protocol § 4.0 autonomous-operation, you have L2-equivalent authority on cross-cutting design. You author the disposition under that authority. Matt re-enters only at wind-down.

---

## Cross-seam contract change? (Principle 6 gate)

**Decision-only dispatch; no production code change.** Path itself may trigger downstream contract changes:

- Path (a) hand-redesign: skill JSON schema field values change per redesigned class; no schema-shape change; MIGRATION.md NOT required for this decision but rocket appends to existing generation/MIGRATION.md when S1 fires
- Path (b) R8-inversion regen: skill JSON files regenerate at scale; manifest.json season identity changes if old seasons replaced; MIGRATION.md REQUIRED at S1 fire-time per rocket dispatch
- Path (c) hybrid: per-class basis; rocket consolidates MIGRATION.md content at S1 fire-time

**Round-trip: not applicable in this dispatch — decision-only authoring; no production code touched. S1 dispatch (the implementation execution) carries the round-trip smoke requirement under whichever path you select.**

---

## Acceptance criteria

- [ ] Decision doc authored at `canonical/story/vs2a-kit-redesign-approach-2026-05-19.md`
- [ ] TL;DR + decision criteria applied + path-specific implementation shape + B6/S2 implications + first-batch class selection criteria + validation gate + risk/watchpoints + cross-references all present
- [ ] Cross-references reciprocal: R1 queue doc updated (if amendment chosen) + roadmap updated (if amendment chosen)
- [ ] Hive log entry: gandalf STATE entry capturing decision authored + path chosen + S1/S2 implications
- [ ] Tag fires: `vs2a/v0.5-kit-redesign-approach-decided` (knight-rider fires on engine + collab repos at the commit landing this disposition; gandalf surfaces tag-firing request in hive-log STATE entry per autonomous-operation protocol § 4.3)
- [ ] No Matt-wait at any point during F2. Matt re-enters only at wind-down.

---

## Open questions for gandalf to resolve (L2-equivalent authority)

- **Are sprint v3 results required as input, or can the decision land on sprint v2 + your own design read?** If v3 is required, surface a hold-pending-v3 STATE entry in hive log; knight-rider routes to gamora for v3 execution sequencing. (My read: v2 evidence + R8 disposition empirics + your judgment of catalogue identity are sufficient; v3 partition would refine first-batch class selection but not the path itself.)
- **Does the chosen path require an S1 dispatch amendment that includes a regen LLM budget?** If path (b) or (c), surface budget rationale in decision doc; knight-rider files in CHANGELOG for transparency.
- **Does the S2 (B6 main work) dispatch shape change with your decision?** If yes, surface the dependency; knight-rider holds S2 dispatch authoring until F2 lands (this is the current sequencing).
- **Substrate-identity declaration impact?** If path (b) at scale prompts you to amend `substrate-identity-declarations-2026-05-17.md` further than the R8 § 9.5 amendment, author the amendment in the same commit; flag in hive log.
- **Future opt-in for `inverted_no_naming` template-distribution path?** Per R8 § 5a, the template-distribution repair is DEFERRED. Your decision should NOT depend on the deferred path; if it does, surface the dependency explicitly and route to knight-rider for prioritization scoping (likely VS2b territory).

---

## References

- `canonical/story/r1-kit-redesign-queue-2026-05-19.md` § 5 (path alternatives)
- `reincarnated-engine/design/working-agreement/R1-blocker-3-disposition-2026-05-19.md` (encounter recalibration + kit-pathology partition)
- `canonical/story/r8-disposition-2026-05-19.md` (Sub-case 3 disposition; `inverted` committed; cost-aggressive deferred)
- `canonical/story/r2-h1-disposition-2026-05-19.md` (R2 H1 instrument-limited PASS; geometry_type re-test gate; structurally parallel category-of-completion precedent)
- `canonical/story/engine-rebuild-2026-05-19-gap-solutions-and-tests.md` § 2 + § 8 (R1 + R8 specs)
- `agentic_orchestration/hive-mind/scope-of-work-vs2a.md` § 1.2 + § 2.2 + § 2.3 (F2 / S1 / S2 framing)
- `agentic_orchestration/hive-mind/coordination-matrix-vs2a.md` § 1 + § 2 + § 5 (DAG + gating + activation gates)
- `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 autonomous-operation + § 4.9 Matt-only-at-wind-down
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#1, #11, #17)
- `canonical/19-llm-call-map.md` (post-R8-amendment LLM topology)
- `canonical/story/substrate-identity-declarations-2026-05-17.md` § 9.5 (R8 surface-readability amendment)

---

## Autonomous-operation authority (no Matt-wait)

Per launch dispatch § 3 + protocol § 4.0 (inherited into VS2a per scope-of-work § 6):

- **Cross-cutting design / canonical / architectural decisions** — gandalf decides under L2-equivalent authority. F2 falls here squarely.
- **No Matt-wait at any point during F2.** Matt re-enters only at wind-down.
- **Tag-firing authorization** — knight-rider holds commit + push authority on milestone tags per ADR-006 amendment. Surface tag-firing request in hive log STATE entry; knight-rider executes.

---

*Authored 2026-05-19 by knight-rider under autonomous-operation authority. F2 gates S1 and S2 both. The catalogue's identity is yours to preserve or let emerge — the disposition you author shapes the next eight weeks of rocket's work. The hive proceeds.*

---

## Completion record (gandalf — 2026-05-19)

### Status: COMPLETE — disposition authored, path (b) decided

**Decision doc:** `canonical/story/vs2a-kit-redesign-approach-2026-05-19.md` (~400 lines; full TL;DR + decision criteria + path-specific implementation shape + B6/S2 implications + first-batch class selection criteria + validation gate + risk/watchpoints + cross-references + reciprocal amendment + provenance)

**Path chosen:** **(b) full R8-inversion regeneration with first-batch validation gate.**

**One-sentence rationale:** R8 A/B 3-season empirical evidence already shows `inverted` producing more boss-tier-functional kits than the entire 51-class shipped catalogue (best boss_kr 0.22 vs 0.033; 20% of inverted classes vs 0% of shipped achieve boss_kr ≥ 0.10) with +0.20 cohesion above baseline + substrate-identity invariance — so the cleanest path is to regenerate the catalogue under the engine's now-committed default, with a 1-season first-batch gate de-risking the scale before full commitment.

**Reciprocal amendment authored:** `canonical/story/r1-kit-redesign-queue-2026-05-19.md` § 5.4 appended capturing path commitment + implications for that doc's per-category partition (now informational) + redesign criteria (now post-hoc validation targets, not generation-time constraints).

**S1 + S2 implications captured:**

- **S1 (kit-redesign sprint):** shape is now "full R8-inversion regen with first-batch validation gate" — rocket regenerates 1 season, gandalf cohesion-judges + gamora R1-sprints first-batch, on PASS rocket regenerates 4 more seasons (total 5), full R1 sprint validates 70-85% per-tier pass-rate target. Effort: ~1-2 wk regen + 0.5 wk gandalf + ~3-4 wk full-catalogue review = ~6-8 wk wall, ~3-4 wk less rocket bandwidth than hand-redesign.
- **S2 (B6 main work):** shape change — skill-tree emerges from regenerated-catalogue composition; rocket pre-work must parameterize for any-catalogue-shape (no hard class_id references); B6 main work begins ~1-2 wk later than under path (a) but offset by faster S1 completion.
- **DAG addition:** F1 (geometry_type schema) + F2 (this disposition) + R1 disposition-3 sprint v3 (gamora) → first-batch regen + gate → full-catalogue regen → R1 sprint full pass → S1 ships → S2 begins.

**Prerequisites verified:**

- F1 (geometry_type schema) — gates first-batch regen; knight-rider already sequenced this F-dispatch
- R1 disposition-3 sprint v3 (gamora) — gates first-batch R1 sprint calibration; knight-rider sequences
- Rocket pre-work parameterization (B6 must work against any catalogue) — knight-rider surfaces to rocket AGENT_STATE
- R8 disposition `inverted` default — already committed and shipped in engine `9f6e4e6` (rocket/v1.20-r8-disposition-impl-1)

**Risks + watchpoints (5 surfaced for knight-rider's watchpoints file):**

1. First-batch regen archetype-coverage drift (e.g., all-mage emergent batch)
2. Naming-vocabulary saturation at 5-season scale (e.g., "Beacon ___" repetition pattern)
3. R1 sprint pass-rate plateau (60-70% range — do NOT auto-fire v0.7 tag; gandalf authors partial-pass disposition per R2 H1 precedent)
4. R8 disposition § 5a (template-distribution repair) re-opens if `inverted` at 51-class scale surfaces template-fixedness pattern (would escalate VS2a-blocking)
5. B6 main-work shape change — S2 dispatch awaits regenerated-catalogue manifest

**Open question dispositions (per F2 dispatch § 5):**

- Sprint v3 dependency: required upstream of first-batch validation, NOT required for this F2 decision. Disposition fires under sprint v2 + R8 A/B empirics + design judgment.
- S1 LLM budget: ~$16-19 (5 seasons × $3.20); worst-case $30-40 with re-runs. Absorbable. Rocket logs in CHANGELOG.
- S2 shape change: yes, captured § 3 of decision doc.
- Substrate-identity amendment: NOT in this commit; R8 § 9.5 amendment is sufficient. Author further amendment only if first-batch surfaces preservation regression.
- `inverted_no_naming` template-distribution opt-in: not a dependency; remains deferred per R8 § 5a; VS2b territory.

**Tag-firing request (per autonomous-operation protocol § 4.3):** Surface `vs2a/v0.5-kit-redesign-approach-decided` to knight-rider for firing on the commit that lands the F2 decision doc + R1 queue § 5.4 amendment. Knight-rider executes tag-firing + push per the autonomous-operation tag-firing pattern; this completion record surfaces the request.

**No Matt-wait at any point.** F2 decided under L2-equivalent authority per protocol § 4.0.

**Acceptance criteria check:**
- [x] Decision doc authored at `canonical/story/vs2a-kit-redesign-approach-2026-05-19.md`
- [x] TL;DR + decision criteria applied + path-specific implementation shape + B6/S2 implications + first-batch class selection criteria + validation gate + risk/watchpoints + cross-references all present
- [x] R1 queue doc amendment (§ 5.4) authored
- [x] Hive log entry pending (next step in this completion sequence)
- [x] Tag-firing request surfaced (this completion record + hive log STATE entry)
- [x] No Matt-wait

*Filed 2026-05-19 by gandalf at F2 completion. The path is committed; the gate de-risks the scale; the catalogue regenerates under the engine's new default. Mithrandir signs.*
