# gandalf — Stage 3 Phase 3 Distribution Report Sign-Off (composition policy § 7.4 empirical criterion)

**Date:** 2026-05-25
**Author:** gandalf (story-and-design steward)
**Authority:** composition policy v1 § 7.4 empirical-criterion-for-completion ("Per-axis distribution + per-tier counts + per-cell coverage reported to Matt + gandalf for sign-off") + dispatch `agentic_orchestration/dispatches/2026-05-24-elrond-cycle-10-stage-3-v1-scope-materialization.md` § 10 Gate routing
**Companion notes:**
- `agentic_orchestration/gandalf/notes/2026-05-25-phase-2-50-row-spot-check.md` (LOAD-BEARING — empirical evidence for distribution-report assessment)
- `agentic_orchestration/gandalf/notes/2026-05-25-so-1-2-4-sign-off-verdicts.md` (SO-1, SO-2, SO-4 Pattern A-light verdicts)
- `agentic_orchestration/gandalf/notes/2026-05-25-so-3-pattern-a-deep-verdict-roland-karna-stage-3-5-amendment.md` (SO-3 Pattern A-deep verdict)

---

## 0. TL;DR

**Distribution report (composition policy § 7.4 sign-off): PASS-WITH-CONDITIONS.**

The Phase 3 distribution report itself is a thorough + accurate accounting of Phase 2 sampler output against composition policy v1 targets. Per-axis distribution + per-tier counts + per-cell coverage are reported transparently with substrate-led discipline applied correctly throughout. elrond's recommendations on the four sign-off items are well-reasoned and architecturally sound.

The report PASSES the composition policy § 7.4 empirical criterion for distribution-report content + structure.

The PASS carries CONDITIONS related to v1_scope material quality (separate concern from report quality):

1. **50-row spot-check FAILS** (29/50 = 58%; threshold 80%) — v1_scope material requires Path-A remediation OR Phase 0c-extension before Phase 2 form-generation fires (per companion notes)
2. **SO-3 Pattern A-deep verdict adopts Path 2** — Wave 6 scope amends to ~30-60 entries
3. **SO-4 amendment proposes Phase 0c-extension** — Wave 5.5 add-on to close D1c-subtype-classifier gap

The report itself is sound; the v1_scope material it describes has remediable gate-gap issues. The report's accounting of "what was produced" is accurate; the question of "is what was produced sufficient" routes through the spot-check + SO-3/SO-4 amendments.

---

## 1. Sign-off criterion mapping (composition policy § 7.4)

Composition policy § 7.4 specifies the empirical-criterion-for-completion as:

| Criterion | Phase 3 report coverage | Sign-off verdict |
|---|---|---|
| v1_scope column populated on all 69K+ active rows | Populated; pre-population smoke 10/10 PASS | PASS |
| v1_scope subset size 1,700-3,100 items | 3,042 (within envelope; +1,342 over lower / -58 under upper) | PASS |
| Per-axis distribution reported | § 2.1 (register) + § 2.2 (cultural tradition) + § 2.3 (period) + § 2.4 (attribute) + § 2.5 (range) + § 2.6 (tempo) + § 2.7 (proxy density) + § 2.8 (military_modern composition trace) | PASS |
| Per-tier counts reported | § 1 per-tier table (S=532 / A=1,431 / B=1,056 / C=23) | PASS |
| Per-cell coverage reported | § 3.1 archetype-PCFS + § 3.2 substrate-cell PCFS + § 3.3 per-tier × per-cultural-tradition cross | PASS |
| Sign-off ask of Matt + gandalf | § 9 four-item sign-off ask | PASS — items addressed in companion notes |
| Gap-cell list passed to Stage 3.5 | § 4 + § 6 gap-list subsection | PASS — routes to Wave 6 |

All six composition policy § 7.4 criteria are covered by the Phase 3 report's content. **The distribution report itself PASSES § 7.4 empirical criterion.**

---

## 2. Substantive observations on the report

### 2.1 Report quality — high

- elrond's substrate-led discipline is applied correctly throughout (PCFS at archetype-level per Discipline #11; substrate-cell PCFS reported for transparency)
- The LP-fallback-not-fired decision (§ 5 sampling rationale + § 7 Finding 3) is well-justified empirically — the failures are genuinely policy/substrate-trade-off-bounded, not local-optima
- The Phase 3 NEW finding (Roland + Karna v1_scope-zero) demonstrates thorough auditing beyond the dispatch's pre-specified gates — elrond surfaces a load-bearing finding not pre-specified
- The named-bearer gap-list subsection (§ 6) is precise + directly consumable by Wave 6 dispatch authoring per Gate-1 amendment 3 requirement
- The v1.1+ queue capture (§ 7 Finding 1-4) is methodical + architecturally-decision-ready

### 2.2 Substantive content observations

**Observation 1 (PRAISE):** the substrate-cell vs archetype-cell PCFS resolution per Phase 2 § 3 + Phase 3 § 3 + Phase 2 § 11 decisions-log proposal is exactly the right substrate-led discipline application. Discipline #11 says: sample against substrate's actual vocabulary, aggregate to the design vocabulary where floor magnitudes apply. The proposal to retire amplitude from Sketch A OR materialize amplitude as a column is a v1.1+-appropriate architectural decision.

**Observation 2 (PRAISE):** the Mode-C operational substitute (§ 4 of sampling rationale) is creative + correct-given-constraints. The original spec referenced `rep_audit_mode_c_naming_allusion_suspected = 1` as a column that doesn't exist; the operational substitute (`register='military_modern' AND named_mythological_match IS NOT NULL`) is a valid + verified Phase 2 gate. As a SIGNATURE-LEVEL gate it works (0 leak under definition). The substitution's LIMITATION (semantic-layer Mode-C-by-period contamination is missed) is OUT OF SCOPE for the operational substitute as defined — and that's a separate v1.1+ queue item.

**Observation 3 (FLAG):** the cultural-tradition over-representation analysis in § 2.2 reaches the right conclusion (european + fantasy_generic = 83.1% over combined target of 45-53%). But framing as a Sidecar B priority signal undersells the magnitude: it's not "thin-cultural-tradition substrate enrichment is necessary" — it's that the v1 form-library will be **30-38pp more european + fantasy_generic-skewed than design intent** without Sidecar B + Stage 3.5 + Stage 4 fully landing. This is a significant compositional risk if Cycle 10 wave-cadence slips before all three land. Suggestion for elrond Phase 3 v1.1 amendment: surface this as a HIGH-priority cycle-internal risk rather than a Sidecar B priority signal.

**Observation 4 (FLAG):** the proxy_density "not yet materialized" finding in § 2.7 is correctly reported. But the implication for Sketch A composition policy targets (75% none / 10% light / 15% heavy) is that **the substrate-bound check on density distribution is structurally impossible until D3 Option A 5-tuple cell-pair sharing materializes density-discrimination at Phase 2 form-generation.** Composition policy § 2.4 stipulates this target band; if Phase 2 form-generation doesn't enforce it at the form-binding step, density distribution can drift. Flag for Phase 2 form-generation work.

**Observation 5 (FLAG):** the Phase 3 NEW finding (Roland + Karna substrate-resident-but-v1-zero) is well-stated but rests on the assumption that the substrate-tagged bearer rows are legitimate anchor seeds. Per gandalf SO-3 Pattern A-deep verdict (separate doc), empirical audit reveals that ~33% of Karna's substrate-tagged rows are Mode-C-by-semantics artifacts. The "9 of 12 substrate-present" Stage 1.5 finding is therefore overstated for Karna. This DOESN'T change the report's recommendation paths (the 3 paths offered are all valid responses to the finding) but it DOES change the right path selection (Path 2 over Path 1, per SO-3 verdict).

### 2.3 Findings on the report

- **§ 5 Phase 3 NEW finding (Roland + Karna)** — accurate as far as it goes; gandalf SO-3 verdict refines via empirical audit (separate doc)
- **§ 7 Finding 1 (substrate-cell vs Sketch-A amplitude vocabulary mismatch)** — well-stated v1.1+ queue item; decisions-log entry proposal (§ 11 sampling rationale) is appropriate for jack-ryan to ratify
- **§ 7 Finding 2 (Mode-C column not materialized)** — well-stated v1.1+ queue item; column materialization cost low; benefit moderate
- **§ 7 Finding 3 (PCFS-vs-register-share tension)** — well-stated v1.1+ queue item; architectural decision well-deferred
- **§ 7 Finding 4 (1,152 NULL-typed in v1_scope)** — well-stated; gandalf SO-4 amendment proposes Phase 0c-extension as Wave 5.5 add-on for cleaner Phase 2 form-generation entry conditions (separate doc)

---

## 3. Conditions on the PASS verdict

The distribution report PASSES the § 7.4 empirical criterion. The v1_scope MATERIAL the report describes has conditions attached:

### Condition 1: Path-A remediation OR Phase 0c-extension before Phase 2 form-generation

Per 50-row spot-check FAIL (29/50 = 58%), the v1_scope material contains substantial D1c-equivalent scope-creep + Mode-C-by-semantics contamination that should be remediated before Phase 2 form-generation fires against it. Two routing options:

- **Wave 5.5 add-on dispatch** — Phase 0c subtype-classifier extension on Tier-A NULL-subtype pool + Mode-C-by-semantics SQL eviction pass on v1_scope. Cost ~half-day elrond. Sequencing: between Wave 5 close and Wave 6 fire (or before Wave 7 fires regardless).
- **Stage 4 trust** — accept that Stage 4 mechanical-tagging will surface D1c-equivalent rows as NULL on proxy-fingerprint axes, allowing eviction then. Risk: Phase 2 form-generation may fire against contaminated v1_scope before Stage 4 lands.

**gandalf-lean:** Wave 5.5 add-on. Phase 0c-extension is the cleanest unblock + composes with the SO-4 amendment.

### Condition 2: Wave 6 scope amends to ~30-60 entries

Per SO-3 Pattern A-deep verdict (Path 2 — defensive Stage 3.5 amendment), Wave 6 scope amends to add GF-5* Roland (~3-5 entries) + GF-6* Karna (~3-5 entries) defensively. Total Stage 3.5 scope: ~30-60 entries vs original ~25-50.

### Condition 3: Mode-C-by-semantics eviction pass on v1_scope (separate from Phase 0c-extension)

The 50-row spot-check + SO-3 audit surfaced systemic Mode-C-by-semantics contamination affecting Sketch F anchor substrate-seed pools across multiple anchors (Karna Tank EX, Quetzalcoatl AIM-68, Thor Dark Elf Particle Rifle, Achilles Swiss sabre with sci-fi description, Grendel KelTec SUB-2000, Lugh Claíomh Solais but in modern period, etc.). The Mode-C operational substitute defined by elrond's substitute (`register='military_modern' AND named_mythological_match IS NOT NULL`) does NOT catch this pattern because the rows are tagged `register='historical'`.

**Specific eviction-candidate SQL signature** (gandalf-proposed):

```sql
-- semantic-layer Mode-C contamination — eviction candidates from v1_scope
SELECT id, canonical_name, register_canonical, historical_period_canonical,
       cultural_lineage_canonical, named_mythological_match
FROM weapon_knowledge_entries
WHERE v1_scope = 1
  AND named_mythological_match IS NOT NULL
  AND (
    -- modern-period + named-mythological-match overlap (Mode-C-by-period)
    historical_period_canonical IN ('contemporary', 'modern', 'industrial')
    OR
    -- canonical_name contains modern military signatures
    canonical_name LIKE '%UAV%' OR canonical_name LIKE '%missile%'
    OR canonical_name LIKE '%helicopter%' OR canonical_name LIKE '%submarine%'
    OR canonical_name LIKE '%aircraft%' OR canonical_name LIKE 'F-%'
    OR canonical_name LIKE '%MK-%' OR canonical_name LIKE 'AIM-%'
    OR canonical_name LIKE 'AGM-%' OR canonical_name LIKE 'SUB-%'
    OR canonical_name LIKE '%Type %'
    OR
    -- substrate-tagged fantasy_generic with sci-fi description signatures
    canonical_name LIKE '%Particle %' OR canonical_name LIKE '%Plasma %'
    OR canonical_name LIKE '%Quantum %' OR canonical_name LIKE '%Laser %'
  );
```

Expected eviction count from this SQL (informed estimate based on substrate audit): ~50-100 rows. Routes through Wave 5.5 add-on dispatch.

### Condition 4: v1.1+ queue captures

Per elrond Phase 3 § 7 findings + gandalf companion-note amendments:

- **v1.1+ Track candidate:** materialize `proxy_amplitude_class` column OR retire amplitude from Sketch A OR pursue joint amplitude/geometry extraction (Finding 1)
- **v1.1+ Track candidate:** materialize `rep_audit_mode_c_naming_allusion_suspected` as DB column (Finding 2)
- **v1.1+ architectural decision queue:** PCFS-archetype-gate ≥85% vs register-share-cap tension — accept substrate-led skew + retire ≥85% gate OR tighten register caps OR rebalance target_total downward (Finding 3 + gandalf SO-2 amendment)
- **v1.1+ priority signal:** Stage 4 mechanical-tagging is critical (Finding 4 + gandalf SO-4 amendment)

These are captured for jack-ryan canonical-write to engineering-disciplines.md + decisions-log per his territory.

---

## 4. Recommendation for knight-rider integration

| Element | Status | Routing |
|---|---|---|
| Phase 3 distribution report content + structure | **PASS § 7.4 empirical criterion** | Close as PASS |
| SO-1 historical register at +5.0pp edge | **RATIFY** (companion note) | Close per Matt sign-off |
| SO-2 PCFS 12/17 FAIL routing | **RATIFY-WITH-AMENDMENT** (companion note) | v1.1+ queue capture |
| SO-3 Roland + Karna v1_scope-zero | **PATH 2 — defensive Stage 3.5 amendment** (companion note) | Wave 6 dispatch scope amends to ~30-60 entries |
| SO-4 1,152 NULL-typed in v1_scope | **RATIFY-WITH-AMENDMENT** (companion note) | Wave 5.5 add-on: Phase 0c-subtype-classifier extension |
| 50-row spot-check | **FAIL** (29/50 = 58%) — load-bearing finding (companion note) | Wave 5.5 add-on (composes with SO-4 amendment + Mode-C-by-semantics eviction) |
| Mode-C-by-semantics contamination beyond SO-3 scope | **NEW finding** (this doc § 3 Condition 3) | Wave 5.5 add-on dispatch authoring (knight-rider authoring; gandalf curation) |
| v1.1+ queue captures | Per § 3 Condition 4 + companion notes | jack-ryan canonical-write territory |

---

## 5. Final empirical-criterion sign-off

### 5a. The Phase 3 distribution report itself: PASS

elrond's Phase 3 distribution report PASSES the composition policy v1 § 7.4 empirical-criterion-for-completion. The report's content + structure are sound; the findings + recommendations are architecturally appropriate; the substrate-led discipline application is correct throughout.

### 5b. The v1_scope material the report describes: PASS-WITH-CONDITIONS

The v1_scope material itself passes composition policy targets at the macro level (per-axis distribution + per-tier counts + envelope check + Phase 2 smoke + Mode-C operational-substitute leak check). But the 50-row spot-check + SO-3 audit revealed semantic-layer contamination that requires Wave 5.5 remediation before Phase 2 form-generation fires against the material.

### 5c. Stage 3 milestone tag readiness

Per dispatch § 7 final Stage 3 milestone tag `elrond/v0.0-cycle-10-stage-3-v1-scope-materialization`:

- This Phase 3 distribution report PASS sign-off (item 4 of 6) lands here
- Other items (Wave 6 fire authoring, Sidecar B closeout, Stage 4 closeout, Cycle 10 closeout) pending

**Recommendation:** Stage 3 milestone tag fires only after Wave 5.5 add-on (Phase 0c-extension + Mode-C-by-semantics eviction pass) lands AND Wave 6 amended scope (GF-5* + GF-6* additions) lands. Otherwise the tag would commit a contaminated v1_scope as the canonical Stage 3 output.

Alternative routing: Stage 3 milestone tag fires NOW on the Phase 3 report sign-off, with explicit "v1_scope material subject to Wave 5.5 amendment" caveat in the tag annotation. Cleaner sequencing but requires acknowledgment that Stage 3 output is iterating.

**gandalf-lean:** route the alternative — Stage 3 tag fires NOW with caveat, Wave 5.5 fires next as Stage 3.6 / Phase 4 add-on. knight-rider has authority to choose per autonomous-scope.

---

## 6. Sign-off

**Author:** gandalf (story-and-design steward)
**Date:** 2026-05-25
**Verdict:** **PASS-WITH-CONDITIONS** — Phase 3 distribution report passes composition policy v1 § 7.4 empirical criterion. v1_scope material the report describes carries 4 conditions (Wave 5.5 add-on Phase 0c-extension + Mode-C-by-semantics eviction; Wave 6 amended scope; v1.1+ queue captures) before Phase 2 form-generation fires against it.

**Empirical criterion to advance Stage 3 completion:** Wave 5.5 add-on dispatch lands + Wave 6 amended scope fires + Wave 6 gandalf curation completes + Stage 4 mechanical-tagging fires + post-Stage-4 v1_scope re-check passes (next gandalf 25-row re-spot-check ≥ 20/25)

**Routing actions for knight-rider:**
1. **Close Phase 3 distribution report sign-off as PASS** (composition policy § 7.4 empirical criterion satisfied)
2. **Author Wave 5.5 add-on dispatch** — Phase 0c-subtype-classifier extension + Mode-C-by-semantics eviction pass on v1_scope (composes SO-4 amendment + 50-row spot-check findings + this doc's Condition 3 SQL spec)
3. **Author Wave 6 dispatch amendment** — Stage 3.5 scope ~30-60 entries (GF-5* Roland + GF-6* Karna defensive additions)
4. **Capture v1.1+ queue items** per § 3 Condition 4 in `canonical/story/v1-1-plus-design-discipline-recognitions-2026-05-23.md` (gandalf to update if Matt ratifies)
5. **Choose Stage 3 milestone tag sequencing:** tag NOW with caveat (gandalf-lean) OR tag AFTER Wave 5.5 + Wave 6 land (cleaner; longer wait)

**Related notes:**
- `agentic_orchestration/gandalf/notes/2026-05-25-phase-2-50-row-spot-check.md`
- `agentic_orchestration/gandalf/notes/2026-05-25-so-1-2-4-sign-off-verdicts.md`
- `agentic_orchestration/gandalf/notes/2026-05-25-so-3-pattern-a-deep-verdict-roland-karna-stage-3-5-amendment.md`
- `agentic_orchestration/elrond/research/cycle-10-stage-3-2026-05-25/v1-scope-distribution-report.md` (subject of this sign-off)
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` § 7.4 (empirical criterion source)
