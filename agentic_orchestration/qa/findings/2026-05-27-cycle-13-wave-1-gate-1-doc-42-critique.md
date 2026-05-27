# Finding — 2026-05-27 — Cycle 13 Wave 1 Gate-1 Critique: Doc 42 Partition INTENT

**Reviewer:** jack-ryan
**Severity:** PASS-with-WARN (0 BLOCK; 3 WARN; 4 INFO)
**Target:** commit `64d1e33` — `canonical/42-stat-sheet-modifier-partition-intent-2026-05-27.md`
**Developer:** gandalf
**Principles applied:** Principles 1 / 2 / 3 / 4 / 5; Disciplines #1.2 / #11 / #18 / #18.2 / #23 / #26 / #27 / #29 / #30 / #31 / #32

---

## Verdict

**PASS-with-WARN.** Rocket Wave 1 implementation dispatch authoring may proceed. Three WARN conditions (W1–W3) must be folded into rocket Wave 1 dispatch acceptance criteria before rocket fires. Specifically: W1 (normalization claim amendment) must be resolved by gandalf in doc 42 before W1.2 schema implementation to prevent a foreseeable rocket implementation error; W2 (prefix/suffix schema field) must appear in W1.2 dispatch; W3 (SC-4 expansion fold-in) must be scoped explicitly in KR dispatch authoring. The four INFO items are notes for the record — no blocking action.

---

## What I found — 7 critique dimensions

### Dimension 1 — Architectural alignment (Discipline #18 + #11) — doc 42 vs doc 40 amendments + closeout Block B + Verdicts B.2/B.3/B.4/D.1

**Verdict: INFO.**

Empirical spot-check performed at doc 40 § 3.6 (post-2026-05-27 amendment), closeout § 3.1-3.3, Verdict B.2, Verdict B.3, Verdict B.4, and doc 42 cross-references.

**Confirmed aligned:**
- 9-category surface: doc 40 amended § 3.6 CONFIRMS categories 1-9 exactly matching doc 42 § 2.1 column headers. No drift.
- 11-slot taxonomy: doc 40 amended § 3.6 states "1 main-hand + 1 off-hand + 5 armor + 4 accessory = 11 slots" — matches doc 42 exactly (main-hand / off-hand / head / chest / hands / feet / legs / amulet / ring × 2 / belt). Confirmed.
- 6 principles: doc 40 amended § 3.6 lists 6 principles verbatim; doc 42 § 6 reproduces them with full operational detail. Aligned.
- Per-rarity grid: doc 42 § 3 matches closeout § 3.2 rarity × modifier count table; slight naming normalization (Legendary T0 explicit) is consistent improvement, not drift.
- T4-attunement annotation (Tier-1+2 only): doc 42 § 3 and § 5.8 correctly confine T4-attunement to Tier-1+2 legendary + all sets per D33 + D51 amended. Aligned.
- Content-compositional attunement framing: doc 42 § 5.8 explicit — annotation is METADATA, not runtime toggle. Matches closeout § 3.4 "gear's content IS the attunement" exactly. Aligned.

**One resolved discrepancy documented for the record:** Verdict B.2 (pre-amendment verdicts doc) listed an 8-slot taxonomy (no legs, no belt). Doc 40 amendment and closeout § 3.2 lock 11-slot. Doc 42 correctly uses 11-slot. The verdicts doc is a pre-amendment artifact and is correctly superseded. No action required.

**Cite:** Discipline #11 (empirical inspection over assumption). Cross-references verified in doc 40 § 3.6 and closeout §§ 3.1-3.3.

---

### Dimension 2 — SC-4 5 methodology gates closure verification (Gates 1-5)

**Verdict: INFO.**

All 5 gates verified against doc 42 § 7 closure table and cross-referenced to legolas SC-4 base research.

| Gate | Closure status | Doc 42 location | Empirical verification |
|---|---|---|---|
| Gate 1 — Prefix/suffix binary | ADOPTED | § 7 table row 1; § 5.x implicit split | SC-4 § S6 principle 1 confirmed by legolas cross-ARPG consensus |
| Gate 2 — Tag taxonomy | DEFERRED v1.1+ | § 7 table row 2 | D4/LE flat-pool adopted correctly per Verdict B.3 |
| Gate 3 — Item-type domain | LOCKED per 11-slot taxonomy | § 7 table row 3; § 2.1 matrix | Doc 40 § 3.6 confirms 11-slot; doc 42 matrix IS the domain assignment |
| Gate 4 — Skill-level affix | LOCKED; helms + amulets only | § 7 table row 4; principle 5 | Verdict B.3 + SC-4 Gate 4 confirm LE precedent |
| Gate 5 — Proc/trigger routing | LOCKED HYBRID | § 7 table row 5; § 5.7 On-trigger samples | SC-4 Finding 1 cross-ARPG consensus confirmed by legolas |

All 5 gates closed. The Gate 5 HYBRID boundary (numerical-trigger at Rare+/Epic+ vs added-skill triggered-passive at legendary-exclusive) is correctly operationalized in § 5.7.

**Cite:** Discipline #11 empirical verification. Principle 4 (decisions-log as single source of truth for Verdicts B.2/B.3/B.4).

---

### Dimension 3 — SC-4 expansion compose-check (5th synergy category + Pattern 9+10 + 9-category verification)

**Verdict: WARN (W3 — see action below).**

The SC-4 expansion research (legolas `2026-05-27-arpg-sc-4-expansion-9-category-synergy-degenerate-patterns.md`) produces three findings with Wave-informing timing classifications:

- **Wave-1-informing (doc 42 relevance):** Topic 1 §§ 1.1-1.4 — 9-category verification. The expansion research confirms 9-category is "architecturally sound and non-standard by design" — valid internal granularity. Three specific divergences documented (Crit split, Build-identity unique, Resistance-Penetration combined). The expansion explicitly deems "no amendment to 9-category lock required." Doc 42 does NOT explicitly acknowledge these divergences or cite the expansion research as verification substrate. The verification IS done (legolas did the work); doc 42 just doesn't cite it.

- **Wave-2-informing:** Scaling-interaction 5th synergy category addition (Topic 2 §§ 2.2-2.3) and Pass 1/Pass 2 empirical validation for first-do-no-harm (Discipline #32). These are EXPLICITLY Wave-2-informing per legolas classification. Doc 42 does NOT need to fold these in — they gate on rocket Wave 2 T4 synergy scan, not Wave 1 partition implementation. Correct to omit.

- **Wave-4-informing:** Pattern 9 + Pattern 10 v1 catalog extension candidates (Topic 3 §§ 3.4-3.5). Correctly out of scope for doc 42.

**Gap:** Doc 42 does not acknowledge the SC-4 expansion research in § 1 (Architectural foundation cross-references) or § 7 (SC-4 methodology gates closure). The Wave-1-informing 9-category verification result is load-bearing for the framing-audit (Discipline #23 Q2: "what would refute 9-cat × 11-slot?") but the citation chain from doc 42 → SC-4 expansion verification is absent. Rocket could proceed without knowing the expansion research exists or that the 9-category divergences were explicitly studied.

**WARN W3:** Before rocket Wave 2 dispatch authoring, KR must ensure the Scaling-interaction 5th synergy category and Pattern 9+10 catalog extensions surface in the Wave 2 T4 synergy scan dispatch explicitly. This is NOT a doc 42 amendment (expansion correctly scoped to Wave 2/4) but IS a KR dispatch-authoring responsibility.

**Recommended action:** gandalf amend doc 42 § 1 companion-docs table to add the SC-4 expansion research reference with explicit timing classification (Wave-1-informing: 9-cat verification ✓; Wave-2-informing: scaling-interaction + Pattern 9+10). One-line amendment. Prevents the expansion findings from being orphaned relative to the partition intent doc.

**Cite:** Discipline #11 (empirical inspection — expansion findings must be traceable from partition intent doc). Principle 4 (decisions-log traceability).

---

### Dimension 4 — Recommendation depth (Discipline #1.2) — sub-wave W1.0-W1.8 implementation-readiness

**Verdict: INFO (with one scoped observation).**

Sub-wave structure W1.0-W1.8 (doc 42 § 9.6) assessed against implementation-readiness criterion: can rocket fire WITHOUT requiring re-clarification dispatches?

**W1.0 (trait dispatch):** Specification is thin. `canonical/story/v1-trait-vocabulary-minimum-viable-2026-05-XX.md` is listed as a future artifact with placeholder date (`XX`). The 55-entry pool is gandalf-owned work; the sequencing dependency is clear ("fires Wave 0/parallel; rocket D8 lands BEFORE Wave 1 partition cycle completion"). This is pre-implementation — the dependency is correctly declared. No claim about already-existing code lines. Discipline #1.2 not violated (this is design-spec, not math-note claiming code behavior). INFO — acceptable for Wave 1 dispatch authoring; the trait vocabulary file must exist before rocket D8 fires.

**W1.2 (schema extension):** Affinity-tier field + tier-restriction field + T4-attunement annotation field all specified to sufficient schema-design depth (§ 9.2-9.3). Sub-wave gate is "jack-ryan Gate-1 critique on schema" — appropriate; Wave 1 implementation dispatch will need its own Gate-1 for the schema PR. Rocket receives enough specification to draft the schema without re-clarification.

**W1.3-W1.5 (matrix, tier-restriction, magnitude bands):** § 9.2-9.4 provide concrete implementation patterns (pseudocode-level). Sufficient for rocket to implement without re-clarification. Starting-estimate magnitude bands correctly declared as "STARTING ESTIMATES" subject to gamora SC-7 calibration post-Wave-1. Per Discipline #18.2: numerical calibration fires AFTER baseline empirical data. Correctly sequenced.

**W1.7 (cross-cohesion validation):** The validation criterion in § 9.5 is specific enough (4 cohort archetypes × spot-check sim × 3 pass criteria). No ambiguity for gamora. Pass criterion cites Discipline #26. Correct.

**One scoped observation (INFO, not WARN):** W1.6 (trait integration D8 + D9) specifies "config/traits/ YAML schema + loader + class_generator integration" — sufficient for D8. But D9 (element/mechanic-gating on gear-affix trait surface) is deferred to Wave 4 while the sub-wave table places it under W1.6. This creates a sub-wave table vs § 8 sequencing text conflict: § 8 says "D9 element/mechanic-gating lands during Wave 4 (gear gen implementation)"; the W1.6 sub-wave table entry says "D8: per-class intrinsic trait pool integration + D9: element/mechanic-gating." Rocket may include D9 in W1.6 scope when it should be Wave 4. Gandalf should clarify the sub-wave table: W1.6 = D8 ONLY; D9 = Wave 4.

**Cite:** Discipline #1.2 (math-note claims cite code line references — no such claims made here; design-spec only; no violation). Discipline #18.2 (numerical calibration timing — correctly sequenced).

---

### Dimension 5 — Playability gate composition (Discipline #26)

**Verdict: INFO.**

Principle 6 (cross-cohesion validation) in doc 42 § 6 and § 9.5 operationalizes Discipline #26 with appropriate specificity:

- 4 cohort archetypes named (DPS-min-maxer / Balanced / Defensive / Hybrid) — matches Block C scaffolding
- 3 explicit pass criteria enumerated (build-diversity emerges; no cohort locked out of progression node; resource-model-gating doesn't break build-diversity; off-affinity preserves gap-filling)
- gamora ownership assigned (spot-check sim)
- BC-axis cells named as the validation coordinate system (principle 6 + § 9.5: "per BC-axis cells")
- Wave 1 close criterion (§ 10) lists gamora Gate-2 PASS as a required item before Wave 1 closes

The doc correctly punts magnitude-band calibration to gamora SC-7 (post-Wave-1) per Discipline #18.2. This is the right sequencing: affinity matrix validation (playability-in-structure) is Wave 1; magnitude-band calibration (playability-in-number) is SC-7.

**One observation (INFO):** § 9.5 specifies "gamora runs spot-check sim on representative kits from each of 4 cohort archetypes" but does not name how many representative kits per archetype constitute a meaningful spot-check. The Block C scaffolding (§ 4 calibration scaffolding companion doc) may contain this specification. Rocket Wave 1 dispatch should include a reference to the Block C scaffolding for the gamora W1.7 work-unit.

**Cite:** Discipline #26 (playability-AND-in-band sim criterion). Discipline #18.2 (consultation at extension hotspots fires after baseline).

---

### Dimension 6 — Minimum-viable trait integration (Verdict D.1) — 55-entry pool operationalization

**Verdict: INFO.**

Doc 42 § 8 correctly operationalizes Verdict D.1 Path (c) PARTIAL at the specification depth appropriate for Wave 1 intent:

- Pool size math: 5 traits × 11 archetypes = 55 entries — consistent with Verdict A.2 chain count (3-4) and "~2 traits per chain" distribution
- Per-archetype composition: 1 element-tagged + 1 mechanic-tagged + 2 stat-flavored + 1 ability-flavored — sufficient for gandalf to author the vocabulary file
- Surface location: T3-only supporting chain per Option C + D83 — correctly aligned with closeout § 2.1
- Floor implementation: L1 ONLY (Cycle 13 minimum-viable); L12/L25/L38 deferred to Cycle 14+ with explicit empirical-evidence triggers named — correct per Discipline #11 operational application (empirical criterion names what gates re-engagement, not time-passage)
- Gear-affix trait surface: element/mechanic-gated per `class_schema.py:46-47` — a Discipline #1.2 code-line reference is provided. Verifiable.
- Deferred items: expansion to 10/class, Phase 5 cohesion-judge integration, rank calibration — all have explicit empirical gates. Correct.

**Cite:** Principle 4 (Verdict D.1 alignment verified). Discipline #11 (empirical inspection of code reference `class_schema.py:46-47` — reference exists; acceptability depends on rocket Gate-2 verification that the file and line exist). Discipline #1.2 (code-line reference provided).

---

### Dimension 7 — Cross-doc consistency (#11 + #23) + discipline compose-check (#18/#26/#27/#29/#30/#31/#32)

**Findings: 1 WARN (W1) + 1 WARN (W2) + 1 INFO**

#### Framing-audit per Discipline #23 three-question protocol (doc 42 § 11)

Doc 42 § 11 applies the framing-audit:
- Q1 (what would refute): "any of the 4 reference ARPGs runs a meaningfully different partition" — correctly named
- Q2 (cheapest refuting test): "verified per SC-4 cross-ARPG consensus" — the cheapest refuting test IS the legolas SC-4 research. The test has been run and produced a PASS (no amendment needed). Correct.
- Q3 (alternative framing): implicit ("operationalizes per consensus") — the alternative framing question (gear archetypes as organizing principle instead of affinity matrix) raised in the dispatch is not explicitly addressed. This is acceptable — the framing-audit at structural layer is satisfied; the alternative-framing stress-test is documented in the dispatch but not required in the intent doc itself.

Framing-audit is complete at the structural layer. No violation.

#### Discipline compose-check

| Discipline | Citation in doc 42 | Assessment |
|---|---|---|
| #18 methodology-before-execution | § 7 + § 9.4 + § 11 | Cited and applied. Gate satisfied. |
| #18.2 consultation timing | § 7 + § 9.4 | SC-7 fires post-Wave-1 per #18.2. Correct. |
| #23 framing-audit | § 11 | Applied at structural layer. Correct. |
| #26 playability | § 6 principle 6 + § 9.5 + § 10 | Cited explicitly (Discipline #26). Correct. |
| #29 commitment-to-consequence | § 11 | Cited explicitly. Locks stated with consequence. Correct. |
| #27 dual-effect capstone | NOT CITED | Wave 2 implementation citation required per dispatch dimension 7 |
| #30 sim methodology naming | NOT CITED | gamora SC-7 composes with #30; Wave 1 dispatch should note |
| #31 dual-effect separability | NOT CITED | Wave 2 implementation citation required per dispatch dimension 7 |
| #32 first-do-no-harm | NOT CITED | Wave 2 T4 synergy scan implementation; not Wave 1 scope |

**WARN W1 — Normalization claim ambiguity in doc 42 § 2 (Discipline #1.2 risk):**

Doc 42 § 2 states: "Affinity tier sum constraint: per slot, sum of all 9 categories' affinity weights = 100%. The matrix per § 2.1 sums to 100% per slot already."

This claim is technically false under literal reading. The raw tier-weight sum per slot ranges from 190 (Legs) to 255 (Amulet) — NOT 100% — because multiple categories share the same tier label and multiple Primary categories (at weight 50 each) appear in each slot. The correct interpretation (from § 9.2 step 2) is that 50/30/15/5 are RELATIVE tier weights that are normalized per slot during implementation. But the § 2 "sums to 100% already" claim directly contradicts this.

Consequence: rocket implementing § 2 literally would set Primary=50%, Secondary=30%, Tertiary=15%, Off=5% as per-category absolute probabilities. A slot with 3 Primary categories would assign 150% total probability to primary categories — implementation would crash or silently renormalize incorrectly.

This is a WARN not a BLOCK because the correct interpretation is available in § 9.2 and a competent implementer will read both sections. But the ambiguity creates a foreseeable implementation error. Gandalf must amend § 2 to replace "sums to 100% per slot already" with "uses relative tier weights that are normalized per slot during implementation per § 9.2 step 2."

**Cite:** Discipline #1.2 (math-note claims must be verifiable; this claim is verifiable as false). Discipline #11 (empirical inspection surfaces the contradiction).

**WARN W2 — Prefix/suffix binary as schema field not mandated in W1.2 dispatch scope (SC-4 Gate 1):**

Doc 42 § 7 Gate 1 closure states: "Rocket implementation should carry the binary as a schema field per SC-4 Gate 1 (cannot be retrofitted easily)." The phrasing "should carry" is advisory, not required. The W1.2 sub-wave acceptance criteria (§ 10) does not list the prefix/suffix schema field as a required deliverable — it lists "per-slot affinity-tier field + per-modifier tier-restriction field + T4-attunement annotation field" only.

SC-4 Gate 1 explicitly notes "cannot be retrofitted easily" — this is the cheapest refuting test per Discipline #19.1. If rocket omits the prefix/suffix field from the W1.2 schema, retrofitting it in Wave 4 or later will require schema migration on all generated gear. The advisory phrasing in § 7 and the omission from § 10 close criteria create the risk that rocket defers this field.

Recommendation: KR rocket Wave 1 dispatch must specify the prefix/suffix binary schema field as a REQUIRED deliverable in W1.2 (not advisory). Gate-2 verification criterion: schema includes `modifier_polarity` (or equivalent field name) with enum `prefix | suffix` per SC-4 Gate 1.

**Cite:** Principle 3 (cross-seam impact called out; schema fields added in W1.2 are consumed by Wave 2 T4 algorithm). SC-4 Gate 1 closure text in doc 42 § 7.

**INFO — Disciplines #27 / #31 / #32 cite gaps (Wave 2 scope):**

Disciplines #27 (dual-effect capstone), #31 (dual-effect separability), and #32 (first-do-no-harm) are correctly Wave 2 scope. Doc 42 § 11 cites 6 disciplines (#1.1 + #18 + #18.2 + #23 + #26 + #29) but does not note the Wave 2 discipline citations. This is informational only — these disciplines gate on Wave 2 T4 algorithm implementation, not Wave 1 partition intent. The rocket Wave 2 dispatch must invoke these disciplines explicitly. No action on doc 42.

**Cite:** Disciplines #27 / #31 / #32 (Wave 2 citations; informational for KR dispatch authoring reference).

---

## Severity summary

| ID | Severity | Finding |
|---|---|---|
| W1 | WARN | § 2 "sums to 100% already" normalization claim is technically false; corrective amendment required before W1.2 implementation |
| W2 | WARN | Prefix/suffix binary schema field is advisory in § 7 but absent from § 10 close criteria; must be REQUIRED in rocket Wave 1 dispatch |
| W3 | WARN | SC-4 expansion research not cited in doc 42 companion docs; expansion findings will be orphaned relative to partition intent doc unless referenced |
| I1 | INFO | W1.6 sub-wave table includes D9 (Wave 4 scope); clarification needed to prevent rocket from including D9 in W1.6 scope |
| I2 | INFO | § 9.5 spot-check sim does not specify kit count per archetype; rocket dispatch should reference Block C scaffolding for this parameter |
| I3 | INFO | Disciplines #27 / #31 / #32 absent from § 11 discipline compose-check; acceptable (Wave 2 scope); KR must include in Wave 2 dispatch |
| I4 | INFO | 9-category ARPG divergences (Crit split; Build-identity unique; Res-Pen combined direction) are verified by SC-4 expansion research but uncited in doc 42 |

---

## Rationale

- **PASS verdict:** All 5 SC-4 methodology gates are verifiably closed. 9-category × 11-slot matrix is internally consistent. 6 principles are correctly operationalized. Sub-wave structure is implementation-ready for rocket to execute. Minimum-viable trait integration is specified at sufficient depth. Architectural alignment with doc 40 amendments and closeout locks is confirmed by empirical spot-check. No principle violation of a type that blocks implementation.

- **WARN (not BLOCK) on normalization (W1):** The correct implementation path is recoverable from § 9.2. A BLOCK would require that the doc is unimplementable as written; this doc is implementable correctly if rocket reads both § 2 and § 9.2. The risk is foreseeable confusion, not architectural invalidity. BLOCK threshold not reached.

- **WARN (not BLOCK) on schema field (W2):** Schema field omission from close criteria is a dispatch-authoring fix (KR), not a doc 42 fix. The information exists in § 7; it needs to be operationalized as a required deliverable in the rocket dispatch.

- **WARN (not BLOCK) on SC-4 expansion (W3):** The expansion research correctly scopes its three topics to Wave-1-informing / Wave-2-informing / Wave-4-informing. Doc 42 not citing it does not block implementation; it creates a traceability gap.

**Cite:** Review Principles 1-5. Disciplines #1.2 / #11 / #18 / #18.2 / #23 / #26 / #29. ADR-002 (direct APPROVE — design-discussion canonical doc amendment).

---

## Action

- [ ] **Gandalf (W1 — required before W1.2 rocket fires):** Amend doc 42 § 2 "Affinity tier sum constraint" to: "per slot, the 9 per-category weights (derived from tier labels using relative tier weights 50/30/15/5 per tier) are normalized to sum = 100% during implementation per § 9.2 step 2. The raw tier-weight sum is not 100% before normalization; the normalization step in § 9.2 is required."
- [ ] **KR (W2 — required in rocket Wave 1 dispatch authoring):** Add prefix/suffix binary schema field as REQUIRED deliverable in W1.2 sub-wave scope and acceptance criteria. Gate-2 criterion: schema includes `modifier_polarity` (or equivalent) with enum `prefix | suffix`.
- [ ] **KR (W3 — required before Wave 2 dispatch authoring):** Ensure rocket Wave 2 T4 synergy scan dispatch cites SC-4 expansion research (Scaling-interaction 5th synergy category + Pattern 9+10 catalog) explicitly. Optionally: gandalf amend doc 42 § 1 to add SC-4 expansion as companion doc with timing classification.
- [ ] **Gandalf (I1 — recommended before W1.6 fires):** Clarify W1.6 sub-wave table: scope is D8 ONLY. D9 (element/mechanic-gating on gear-affix trait surface) is Wave 4 scope per § 8 sequencing text. Remove D9 from W1.6 sub-wave table entry to prevent rocket from including it in Wave 1 scope.
- [ ] **KR (I2 — include in gamora W1.7 dispatch):** Reference Block C scaffolding companion doc for kit-count-per-archetype specification in the gamora spot-check sim work-unit.

---

## Next-action sequence for KR

1. Route W1 to gandalf for doc 42 § 2 amendment (minor; one-paragraph rewrite)
2. With W1 resolved, proceed to authoring rocket Wave 1 implementation dispatch incorporating:
   - W2 (prefix/suffix binary as REQUIRED W1.2 deliverable)
   - I1 (D9 scoped to Wave 4, not W1.6)
   - I2 (Block C scaffolding reference for gamora W1.7)
3. Route W3 to gandalf for doc 42 § 1 companion-doc amendment OR hold for Wave 2 dispatch authoring
4. Wave 2 dispatch must invoke Disciplines #27 / #31 / #32 and SC-4 expansion explicitly (I3)

---

## References

- `/Users/admin/Games/reincarnated-collaboration/canonical/42-stat-sheet-modifier-partition-intent-2026-05-27.md` — critiqued artifact (528 lines; 12 sections)
- `/Users/admin/Games/reincarnated-collaboration/canonical/40-gear-balance-guide-architecture-2026-05-26.md` — § 3.6 (post-2026-05-27 amendment) spot-checked for alignment
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-pre-launch-design-session-closeout.md` — §§ 2.1 / 2.2 / 3.1-3.4 / 7 / 9 verified
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-05-26-cycle-13-design-session-pattern-a-deep-verdicts.md` — Verdicts B.2 / B.3 / B.4 / D.1 spot-checked
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/research/cycle-13/2026-05-27-arpg-sc-4-expansion-9-category-synergy-degenerate-patterns.md` — SC-4 expansion; Topic 1 (Wave-1-informing); Topic 2 (Wave-2-informing); Topic 3 (Wave-4-informing)
- `/Users/admin/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #1.2 / #11 / #18 / #18.2 / #23 / #26 / #27 / #29 / #30 / #31 / #32
- Normalization math: python3 empirical verification at review time — raw tier-weight sums range 190-255 per slot (not 100%); § 9.2 normalization step confirmed correct
