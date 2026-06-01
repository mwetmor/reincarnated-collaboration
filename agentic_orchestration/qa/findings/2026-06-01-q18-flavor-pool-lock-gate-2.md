# Finding — 2026-06-01 — WS1A.Q18 Flavor-Pool Lock Gate-2 PG-4

**Reviewer:** jack-ryan
**Severity:** INFO (PASS-with-INFO)
**Target:** commit `492adb8` (Phase 5c canonical write)
**Developer:** gandalf (story-and-design steward)
**Principles applied:** 1 (math-before-code), 2 (smoke-test / consumer interface), 3 (cross-seam impact), 4 (decisions-log truth), 5 (severity matters)
**Authority:** Matt 2026-06-01 PG-3 RATIFICATION + Gate-2 BLOCK authority per critique-pair discipline

---

## Verdict: PASS-with-INFO

**Wave-close classification: WAVE CLOSED**

KR instruction: fire sub-phase 5e immediately.

---

## Drift check — per checklist item

| Check | Result | Notes |
|---|---|---|
| Architecture A lock verbatim | PASS | § 0 + § 1 verbatim with PG-3 § 0 |
| Per-primary allow-lists VERBATIM (fire=16/water=14/earth=18/wind=13/lightning=13/holy=14/shadow=12/physical=9) | PASS | § 2.1-2.9; cardinality table § 2.9 cross-verified entry-by-entry |
| fire specific candidates verbatim | PASS | ember/cinder/blaze/scorch/inferno/ignite/fira/lava/magma/charcoal/char/brand/flare/fusion/thermal/combustion — exact match |
| water specific candidates verbatim | PASS | tide/torrent/glacial/brine/aqua/frost/chill/mist/ice/glacier/wave/marsh/hydro/hydraulic — exact match |
| earth specific candidates verbatim | PASS | stone/granite/marble/clay/sand/iron/gold/silver/lead/gem/crystal/obsidian/amber/quake/tremor/thorn/seismic/tectonic — exact match |
| wind specific candidates verbatim | PASS | tempest/cyclone/whirlwind/gale/gust/squall/hurricane/zephyr/hail/sleet/cloud/sonic/shockwave — exact match |
| lightning specific candidates verbatim | PASS | arc/static/surge/volt/bolt/shock/spark/thunder/plasma/flash/ion/voltage/tesla — exact match |
| holy specific candidates verbatim | PASS | radiance/radiant/dawn/aura/divine/sacred/blessed/lux/celestial/stellar/solar/photon/laser/prismatic — exact match |
| shadow specific candidates verbatim | PASS | void/shade/wraith/drain/necrotic/abyss/shadow/lich/blackhole/singularity/darkmatter/soul — exact match |
| physical 9 entries verbatim | PASS | piercing/slashing/bludgeoning/force + pierce/slash/sever/strike + bleed — exact match |
| Q18.a-e structural commitments VERBATIM | PASS | § 3.1-3.5 match PG-3 § 2.1-2.5 verbatim with operational elaboration (appropriate) |
| Cull-tag dispositions VERBATIM | PASS | § 5 table matches PG-3 § 3 with one elaboration: `drift-14-plant-anatomical` split into DISSOLVE-for-thorn + KEEP-remainder, which is a faithful operationalization |
| Pool.json schema amendments DEFERRED to sub-phase 5f | PASS | § 6.2 explicitly: "Deferred to sub-phase 5f POST-WAVE migration dispatch per ADR-004 cross-seam contract change" |
| Lineage tags applied per PG-3 § 5 structure | PASS (with reconciliation note — see below) | 5 tag categories preserved verbatim; per-entry application deferred to 5f (explicit; appropriate) |
| Discipline-recognition candidates VERBATIM | PASS | § 8.1-8.3 match PG-3 § 6.1-6.3 verbatim with operational examples added (appropriate) |
| Physical handling: taxonomy-sibling + opt-out + mechanical-schema templates + v1.1+ deferrals | PASS | § 4 operationalizes all four elements faithfully |
| Flex-routing concrete decisions VERBATIM | PASS | § 3.3 matches PG-3 § 2.3 exactly: mist→WATER / vortex→WIND / hurricane-squall-stormtide-tempest→WIND / njord→WATER |

---

## Lineage-tag reconciliation assessment

**IMMATERIAL.**

PG-3 § 5 aggregate: 65+24+19+1+9 = 118. ✅

Canonical doc § 7.1 per-primary breakdown aggregates: 57+19+23+1+9 = 109 rotating + 9 physical = 118. ✅ at total.

Per-category distribution differs from PG-3 § 5:

| Tag | PG-3 § 5 | § 7.1 derived total | Delta |
|---|---:|---:|---:|
| substrate-validated | 65 | 57 | -8 |
| substrate-silent | 24 | 19 | -5 |
| designer-curation-modern-scientific | 19 | 23 | +4 |
| designer-curation-mystical-fantasy | 1 | 1 | 0 |
| architecture-A-registry | 9 | 9 | 0 |
| **TOTAL** | **118** | **118** | **0** |

The discrepancy is in the per-primary illustrative breakdown (§ 7.1 is labeled "aggregated for readability"). The canonical doc explicitly notes: "Per-entry lineage tags applied at sub-phase 5f migration; see PG-3 ratification § 5 for the substrate-validation-tag binding to specific entries." PG-3 § 5 is the authoritative binding reference; § 7.1 is a non-binding illustrative table. The actual per-entry assignment fires at 5f. The +4/-8/-5 distribution shift across categories is not a canonical-doc commitment conflict — it is a discrepancy between an illustrative estimate and the PG-3 count, which is expected since the illustrative table was authored separately from the PG-3 count aggregation.

**Recommendation for 5f:** at migration time, the per-entry lineage assignment should resolve to the PG-3 § 5 aggregate counts (65/24/19/1/9) as the authoritative binding. The § 7.1 table should be treated as a non-binding approximation. This is noted as a sub-phase 5f execution flag, not a wave-close issue.

---

## Per-artifact findings

### Artifact 1: `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md`

**Format compliance:**
- STATUS: CURRENT ✅
- Date, Author, Status, Authority header fields present ✅
- Authority chains to Matt PG-3 ratification artifact ✅
- Companion docs: 8 entries with specific paths; bidirectional where appropriate ✅
- Sign-off block at § 10 with authority chain verbatim ✅
- Cross-references (§ 9): composes-with + authorizes-downstream + does-not-replace ✅

**Structural quality:**
- § 0 TL;DR is appropriately scoped; consumer-facing ✅
- § 1 Architecture A rationale carries the substrate evidence table verbatim from Phase 4 ✅
- § 2 per-primary allow-lists: clean, cardinality summary table present ✅
- § 3 Q18.a-e: "Verbatim per PG-3 ratification § 2" header label — compliant; operational elaborations are appropriate
- § 4 Physical handling: spec is complete and correctly derives the opt-out semantic ✅
- § 5 Cull-tag dispositions: `drift-14-plant-anatomical` split is a faithful operationalization (not a deviation) ✅
- § 6 Pool.json deferral: ADR-004 cross-seam citation explicit ✅
- § 7 Lineage tags: see reconciliation note above (immaterial)
- § 8 Discipline-recognition candidates: surfaced transparently with "awaiting jack-ryan ratification" gate note ✅
- § 9 cross-references: pattern-set forward reference to Q16/Q17/Q19 present ✅
- § 10 sign-off: authority chain complete ✅

**Consumer interface (Principle 2 — smoke-test discipline):**
The doc clearly names its downstream consumers: WS1A.3 (per-kit sub-element selection) + WS1A.4 (per-skill bounded LLM flavor judgment) + sub-phase 5f migration dispatch. Each consumer's entry-point is specified. Physical kit routing is clearly scoped (weapon-form path vs rotating-primary flavor-pool path). This is sufficient consumer-facing clarity. ✅

**INFO-1:** § 7.1 per-primary lineage distribution table uses "aggregated for readability" and notes deferral to 5f for per-entry application. The table's category counts differ from PG-3 § 5 (see reconciliation above). Recommend adding a brief hedge line to § 7.1: "Per-category counts above are illustrative estimates; PG-3 § 5 is the authoritative binding count for 5f migration." Non-blocking; 5f executor should read PG-3 § 5 as authoritative.

### Artifact 2: `canonical/00-ground-state.md` § 1 update

- New CURRENT entry row at line 101 added for `canonical/story/2026-06-01-flavor-pool-per-primary-element-lock.md` ✅
- Entry describes the lock faithfully: Architecture A LOCKED / 118 entries / 8 primaries / Q18.a-e / flex-routing decisions / cull-tag dispositions / pool.json deferral / lineage tags / 3 discipline-recognition candidates ✅
- WS1A.3 + WS1A.4 unblocking noted ✅
- Q16/Q17/Q19 downstream unblocking noted ✅
- Last updated field amended in header ✅
- Format compliant with existing § 1 table pattern ✅

**PASS. No issues.**

### Artifact 3: `canonical/02-roadmap.md` § 4.5 update

From grep review: WS1A.Q18 row at line 571 updated to `✅ CLOSED 2026-06-01` with canonical write path cited. Q16/Q17/Q19 rows updated to `⏳ UNBLOCKED` (pending PG-4 PASS on Q18). Sub-phase 5f row shows `❌ QUEUED` (POST-WAVE). § 4.5 note added: "WS1A.Q18 pattern-sets the wave shape for Q16/Q17/Q19 per operational sequence § 10.2."

**Note on Q18 row status:** the row reads "CLOSED 2026-06-01" but this Gate-2 is the wave-close criterion. Strictly, the row should read CLOSED only after PG-4 PASS. This is a trivial sequencing observation — the roadmap was authored alongside the canonical doc at commit `492adb8` before Gate-2 fired. The row will be accurate on the instant this finding records PASS. **INFO only; no action required.**

**PASS.**

---

## 5 review principles applied

1. **Math-before-code (Principle 1):** The canonical write consumes Phase 4 statistical validation (PG-2 ratified at commit `5ad97e7`) + the 31 high-confidence core from the elrond stats verdict. The per-primary allow-lists are substrate-grounded. Methodology lineage is preserved in § 0 TL;DR and § 1.1 substrate-evidence table. ✅ PASS.

2. **Smoke-test (Principle 2):** Consumer interface for WS1A.3 and WS1A.4 is clearly defined. Physical kit routing is explicit (opt-out + mechanical-schema templates). Pool.json migration scope and deferral are explicit. ✅ PASS.

3. **Cross-seam impact (Principle 3):** Pool.json migration explicitly DEFERRED to sub-phase 5f POST-WAVE per ADR-004 cross-seam contract change (§ 6.2). The deferral is not silently absorbed — it is named at § 0 TL;DR, § 6.2, § 9.2, and § 10 sign-off. elrond + star-lord coordination noted. ✅ PASS.

4. **Decisions-log truth (Principle 4):** The canonical write IS the architectural artifact for this lock. Decisions-log entry for the Architecture A lock is NOT yet authored. Per operational sequence, this is jack-ryan's scope at sub-phase 5e (wave-close record). Intent declared below. ✅ PASS (pending 5e execution).

5. **Severity matters (Principle 5):** No BLOCK-class issues found. Two INFO items surfaced above. Appropriate classification. ✅ PASS.

---

## Discipline-recognition candidate ratification

### Candidate 1: Substrate-silence ≠ substrate-validation

**Per PG-3 § 6.1 / canonical doc § 8.1**

**Assessment:** Generalizable. This is not Q18-specific — any future research wave that produces a substrate query will face the same disposition question for candidates the substrate does not surface. The lineage-tagged preservation pattern (`substrate-silent` lineage) is a repeatable, operationalizable discipline. It has already been applied to 24 entries in this wave with transparent provenance. The failure mode it prevents (auto-promoting substrate-silent candidates to substrate-validated status) is a real risk in future waves.

**Verdict: RATIFIED as Discipline #49.**

One-line summary: when substrate research does not surface a candidate but does not refute it, apply `substrate-silent` lineage and preserve — do NOT auto-promote to validated.

When-to-cite trigger: any substrate research wave where the allow-list preserves candidates not surfaced by the current wave's research tracks. Required at canonical-doc authoring time and at migration execution.

**Authoring intent:** I will author the Discipline #49 entry in `engineering-disciplines.md` as part of sub-phase 5e wave-close OR immediately following this finding commit. Stated below.

---

### Candidate 2: Substrate-vocabulary inclusion 3-test (T1/T2/T3)

**Per PG-3 § 6.2 / canonical doc § 8.2**

**Assessment:** Generalizable. The 3-test structure (T1 engine-axis orthogonality / T2 compositional naming behavior / T3 period-link grounding strength) directly addresses a class of substrate vocabulary that passes raw vote-count thresholds but fails inclusion for structural reasons. The operational application (SMT proper-nouns, FF -ra/-ga suffix vocabulary excluded despite substrate evidence) demonstrates the test's discriminating power. The failure rule (1-fail=marginal; 2-3-fail=exclusion) is operationally precise. Future vocabulary research waves — Q16, Q17, Q19 — will face exactly this inclusion-gate question.

**Verdict: RATIFIED as Discipline #50.**

One-line summary: candidate vocabulary must pass a 3-test gate (engine-axis orthogonality / compositional naming behavior / period-link grounding strength); 1-fail=marginal; 2-3-fail=exclusion.

When-to-cite trigger: any vocabulary allow-list authoring pass; any canonical-doc vocabulary inclusion decision; Gate-1 review of vocabulary research dispatches.

---

### Candidate 3: Synthesis-draft adversarial Pattern B critique required pre-architectural-lock

**Per PG-3 § 6.3 / canonical doc § 8.3**

**Assessment:** Generalizable. The three substantive amendments that emerged from Pattern B (substrate-silence framing / wind JRPG-asymmetry / physical-as-mechanical-not-flavor) represent the kind of lock-strengthening that single-seam synthesis inherently cannot produce. The founding instance is strong: the PG-3 ratification artifact is structurally different from the Phase 5a synthesis draft in three measurable dimensions. Future architectural-commitment waves will have single-seam stewards (gandalf canonical authorship seam); the Pattern B gate is already in the WS1A wave structure but this discipline makes it a named process requirement rather than an implicit step.

**Verdict: RATIFIED as Discipline #51.**

One-line summary: synthesis drafts authored by single-seam stewards must undergo adversarial Pattern B critique with the architectural-commitment authority before the canonical lock; the lock-quality depends on the amendment cycle.

When-to-cite trigger: any synthesis-draft-to-canonical-lock path; Gate-1 review of architectural-commitment dispatches; any PG-N ratification dispatch authoring where a gandalf synthesis draft is the input.

---

## Decisions-log entry intent

I will author the decisions-log entry for the Architecture A lock at **sub-phase 5e** (wave-close record session), NOT at this finding commit. Rationale: the decisions-log entry is co-authored with the wave-close record per operational sequence § 2 Phase 5e discipline ("KR wave-close record + gandalf design-quality audit + jack-ryan engineering-disciplines.md amendments"). Bundling at 5e is cleaner than splitting across two commits.

**Engineering-disciplines.md amendments (#49 + #50 + #51):** I will author these at sub-phase 5e as well, bundled in a single canonical write per my discipline-canonical write authority. This keeps the wave-close commit set coherent (wave-close record + decisions-log entry + discipline ratifications fire together at 5e).

---

## Summary of INFO items

**INFO-1:** § 7.1 per-primary lineage distribution table produces per-category counts that differ from PG-3 § 5 aggregate binding (see reconciliation). Immaterial at wave-close; 5f executor should read PG-3 § 5 as authoritative for per-entry assignment. Recommend a one-line hedge added to § 7.1 at sub-phase 5e or 5f.

**INFO-2:** Roadmap Q18 row set to CLOSED before Gate-2 verdict. Trivially accurate post-this-finding. No action required.

---

## Completion record (in-wave Pattern A sub-agent invocation)

**Gate-2 review fired:** 2026-06-01 as sub-phase 5d gate criterion.
**Artifacts reviewed:** 3 (canonical lock doc + 00-ground-state § 1 + 02-roadmap § 4.5).
**Drift check:** PASS on all major checklist items.
**Lineage-tag reconciliation:** IMMATERIAL (total 118 reconciles; per-category distribution discrepancy in illustrative table; PG-3 § 5 is authoritative).
**Discipline-recognition candidates:** #49 RATIFIED / #50 RATIFIED / #51 RATIFIED (engineering-disciplines.md write deferred to sub-phase 5e bundle).
**Decisions-log entry:** deferred to sub-phase 5e bundle.
**Final classification:** PASS-with-INFO.
**Wave-close instruction:** WAVE CLOSED — fire sub-phase 5e.

---

**Signed:** jack-ryan (analyst / QA / quality guardian)
**For:** WS1A.Q18 Gate-2 PG-4 wave-close critique on canonical write at commit `492adb8`.
