# Sam Gate-1 Finding — Paired Pre-Fire Review: WS1 + WS3 Commissions

**Date:** 2026-06-10
**Author:** sam (PC-side QA gatekeeper)
**Mode:** DESIGN-MODE Gate-1 (pre-fire; paired commissions)
**Authority:** Matt 2026-06-10 directive — Gate-1 pre-fire requirement on WS1 + WS3 before mantis fires per critique-pair-gate-protocol § 3
**Pattern:** OP Pattern A-deep (file artifact verdict; paired commissions feeding vertical-slice spike critical path)

**Subjects reviewed:**
- `agentic_orchestration/dispatches/2026-06-10-david-h-ws1-data-layer-kit-corpus-ingestion-commission.md`
- `agentic_orchestration/dispatches/2026-06-10-david-h-ws3-materialization-cinematic-sequencer-commission.md`

**Context evidence read:**
- `canonical/story/2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md` § 2.1 + § 2.5 + § 11.2 + § 12 (CANONICAL lock)
- `agentic_orchestration/dispatches/2026-06-08-david-h-ue-mcp-bridge-spike-AMENDMENT-db-lyon-primary.md` (db-lyon tooling baseline)
- `agentic_orchestration/qa/findings/2026-06-08-david-h-ue-mcp-bridge-spike-db-lyon-primary-gate-2.md` (Sam's own prior Gate-2: WARN-001 + WARN-002 disposition)
- `agentic_orchestration/dispatches/2026-06-10-david-h-earth-avatar-vertical-slice-spike-AMENDMENT.md` (vertical-slice spike absorbs WS1+WS2+WS3 + WARN-002 BP-mutation pre-fire gate)
- `C:\dev\reincarnated-unreal\Reincarnated\AGENT_STATE.md` (mantis state — closed; awaiting routing)
- PC filesystem inspection at `C:\dev\` (sibling-repo presence check)

---

## 0. TL;DR

**Verdicts:**

| Commission | Verdict | Findings |
|---|---|---|
| **WS1** | **PASS-WITH-AMENDMENTS** | 1 BLOCK (source-JSON staging), 2 WARN, 2 INFO |
| **WS3** | **PASS-WITH-AMENDMENTS** | 0 BLOCK, 3 WARN, 1 INFO |

**Cross-dispatch consistency:** 1 INFO (parallel-fire feasibility under UE single-Editor-instance constraint warrants explicit sequencing guidance for david-h).

**Routing implication:** Matt's directed parallel-fire of WS1 + WS3 is preserved AT THE COMMISSION-AUTHORIZATION layer (both PASS). At the EXECUTION layer, david-h must route the source-JSON precondition BLOCK on WS1 BEFORE mantis can execute WS1 Phase 1 (the BLOCK is precondition-level, not commission-rejection). WS3 Phase WS3.1 (Sequencer asset authoring with placeholder mesh) can fire in parallel with WS1 source-JSON staging because WS3 does not consume WS1 DataTable data until Phase WS3.2's matched-kit composition. Parallel-fire feasibility is preserved with sequenced phasing.

**No Mac-jack-ryan consultation triggered by this Gate-1.** All findings resolve within PC-seam scope. The decisions-log entry proposal from prior Sam Gate-2 (Proposal 1 — db-lyon adoption) remains in flight per `agentic_orchestration/sam/notes/2026-06-08-proposal-mac-jack-ryan-db-lyon-decisions-log.md`.

---

## 1. WS1 review — per-principle

### 1.1 Math-before-code (Principle #1; Discipline #1)

Partially satisfied with one structural gap. The WS1 commission cites Branch A canonical (§ 10 + § 11 + § 12), Phase 2 elrond MVP, Legolas zodiac corpus, and atomic-substrate-registry as substrate-trace. Each cited source has its own math foundation (legolas two-round research baseline; elrond Phase 2 sidecar; substrate-registry CANONICAL).

**Gap:** the commission does NOT specify cross-DataTable foreign-key SCHEMA design — only criterion #6 mentions foreign-key resolvability (`kit_id ↔ star_sign_id ↔ primitive_family_id`). The DataTable schema design choice (string FK vs FName FK vs DataTable row-handle UE-idiomatic) has performance and idiomaticity implications and is left to mantis discretion. This is a reasonable defer FOR ROUTINE UE schema choice — DataTable row-handles are the UE-idiomatic pattern — but the commission could surface it as an explicit "mantis-chooses-UE-idiom" framing rather than leaving silent.

**Severity:** WARN (WARN-WS1-A below). Not BLOCK because UE-idiomatic row-handles are the obvious default and mantis can be expected to land it correctly.

### 1.2 Smoke-gate coverage (Principle #2)

Adequate at commission scope. Acceptance criteria #1-#7 form a coherent smoke-gate ladder (struct definition → ingestion → row-count match → row inspection → persistence → FK resolution → Sam Gate-2). Per-DataTable inspection is implicit in criterion #4 ("sample row inspection passes per DataTable"). David-H wave-close (criterion #8) closes the loop.

No gaps at this layer.

### 1.3 Cross-seam impact (Principle #3; Principle #6; ADR-004)

**BLOCK condition found.** Commission § 1.3 states: "JSON sources live at Mac-side meta-repo + engine-repo + loadout-repo paths. PC-side requires: Mac → PC sync via git (already operational per CLAUDE.md addendum)."

PC filesystem inspection contradicts this assumption:

| Source repo | Cited content | PC clone presence at C:\dev\ |
|---|---|---|
| meta-repo (`reincarnated-collaboration`) | Legolas zodiac corpus | PRESENT (corpus YAMLs verified at `legolas/research/2026-06-09-zodiac-substrate-corpus/`) |
| engine repo (`reincarnated-engine`) | Engine kit corpus cycle-14 output (`seasons/` dir) | **ABSENT — repo not cloned on PC** |
| loadout repo (`reincarnated-loadout`) | Phase 2 elrond `kit_star_sign_assignments.json` sidecar | **ABSENT — repo not cloned on PC** |
| meta-repo or other | Atomic-substrate-registry Layer 0 (20 families) as JSON | **ABSENT — only the canonical-story narrative doc exists (`canonical/story/2026-06-06-atomic-substrate-registry.md`); no machine-readable JSON sidecar surfaced** |
| meta-repo or other | Experiential axes (hypothesis-flow § 1.8) as JSON | **ABSENT — narrative canonical exists; machine-readable JSON sidecar not surfaced** |

This is a CROSS-HOST contract gap. The commission presumes Mac → PC sync covers all 5 sources via existing git pull discipline, but only ONE of the 5 sources (legolas zodiac corpus) is reachable from the PC clone of the meta-repo. The other 4 require either (a) cloning engine + loadout repos on PC, (b) emitting JSON exports from those repos into the meta-repo, or (c) Mac-side authoring of staging JSONs into meta-repo before WS1 fires.

**Severity:** BLOCK-WS1-A. WS1 cannot ingest sources it does not have. Mantis would hit this in Phase 1 (step 4 `fill_datatable_from_json` requires source JSON path) and stall. Pre-fire resolution required.

### 1.4 Decisions-log as truth (Principle #4)

Authority claims compliant. Commission cites Branch A canonical, Phase 2 elrond MVP, atomic-substrate-registry CANONICAL, hypothesis-flow § 1.8 multi-axis architecture, § 12 canonical lock. All are existing canonical commitments.

**Observation:** the in-flight Sam Proposal 1 to Mac-jack-ryan (db-lyon adoption decisions-log entry) is not yet ratified at the decisions-log layer. The WS1 commission proceeds on the spike-PASS authorization at AMENDMENT § 6.1 + Sam Gate-2 PASS-with-WARN. This is acceptable — the spike-PASS provides empirical authorization independent of the decisions-log canonical write timing. INFO-only flag.

### 1.5 Severity calibration + criterion sufficiency

Acceptance criteria #1-#8 cover the right surface but could be tightened on TWO points:

- **Criterion #3 row-count match** is too coarse. "Row counts match source JSON entry counts" without per-DataTable expected-count numerals leaves mantis to extract them at execution time. Expected counts SHOULD be in the commission: DT_KitStarSign=37 (per Phase 2 MVP); DT_StarSign=423 (per legolas corpus); DT_PrimitiveFamily=20 (per atomic-substrate-registry Layer 0); DT_Kit=TBD (per current cycle-14 output — needs cycle-14 export count surfacing); DT_ExperientialAxis=TBD (per hypothesis-flow § 1.8 axis count). Half are specified; half are TBD. WARN to surface explicit expected counts.
- **Criterion #6 cross-DataTable foreign-key resolvability** is a runtime semantic check, not a structural check. The criterion would benefit from a single concrete worked example: "given DT_KitStarSign row with kit_id=X and star_sign_id=Y, lookup of X in DT_Kit returns the corresponding kit row AND lookup of Y in DT_StarSign returns the corresponding star sign row." WARN to add worked-example assertion.

**Severity:** WARN-WS1-B + WARN-WS1-C (cumulative; one finding each below).

### 1.6 Cross-seam round-trip discipline (Principle #6)

Cross-seam contract change present: Mac-engine kit-corpus JSON schema ↔ UE-DataTable C++ struct schema is a NEW cross-seam contract surface. WS1 does not specify whether MIGRATION.md is required at this boundary. Per Principle #3 + ADR-004, cross-seam interface changes require MIGRATION.md before milestone-tag fires.

**Disposition:** WS1 commission is pre-tag (criterion #8 is wave-close memo, NOT milestone tag). The MIGRATION.md gate would activate at downstream milestone-tag (likely post-vertical-slice-spike). Acceptable to defer to that point. INFO-only at this Gate-1 layer.

However: WS1 § 1.1 surfaces 5 distinct cross-seam contracts (one per DataTable) and the commission does NOT identify which is the source-of-truth schema for engine ↔ UE round-trip. If engine kit corpus schema changes in cycle-15, do downstream UE DataTables auto-re-ingest, or does mantis re-author C++ structs? This is a forward-loaded INFO (durability question, not blocker at WS1 scope).

**Severity:** INFO-WS1-A (MIGRATION.md trigger condition surfacing for downstream consumption).

### 1.7 Discipline citations review

- **Discipline #46 (db-streaming + anti-materialization)** — cited correctly. DataTables are materialized JSON ingest at canonical layer; downstream consumers should NOT materialize sub-tables at runtime. The WS1 commission flags this correctly for downstream awareness.
- **D7 AI-tell line** — cited correctly. JSON ingestion is engine-pregenerated; no runtime LLM. No issue.
- **ADR-006 (read-only-by-default external systems)** — cited; BUSL-1.1 base evaluation grant covers WS1. Correct.
- **Recognition-validate-commit** — cited; WS1 IS empirical validation of db-lyon at production scope. Correct.
- **Sam WARN-002 Blueprint-mutation pre-fire gate** — cited in WS1 § 3 but qualified as "separate gate; vertical-slice spike scope." This routing is CORRECT — WS1 does not trigger Blueprint mutation (only DataTable + struct compilation). The vertical-slice spike AMENDMENT § 2.1 reproduces the gate at vertical-slice scope. Routing is consistent.

### 1.8 Estimated wall-clock

"1-3 weeks UE mantis work per Mantis convention" — reasonable. WS1 spans 5 DataTables, each requiring struct authoring + DataTable asset creation + JSON ingestion + verification. Per-DataTable cycle ~2-4 days × 5 = ~2-3 weeks. Convention-consistent with prior mantis port estimates. No concern.

---

## 2. WS1 findings (BLOCK / WARN / INFO)

### BLOCK-WS1-A — Source-JSON staging assumption broken at PC layer (5 of 5 sources affected; 1 reachable)

**Severity:** BLOCK (precondition-level; does not reject commission, but mantis CANNOT execute Phase 1 without resolution)

**Summary:** Commission § 1.3 asserts "JSON sources... flow Mac → origin → PC per existing pull discipline." PC filesystem inspection reveals only the legolas zodiac corpus (1 of 5 cited sources) is reachable from the PC clone of the meta-repo. Engine kit corpus (engine repo), Phase 2 elrond kit-star-sign sidecar (loadout repo), atomic-substrate-registry primitives JSON, and experiential-axes JSON sources are either in repos NOT cloned on PC (engine, loadout) or do not exist as machine-readable JSON sidecars (only canonical-story narrative docs exist for the substrate-registry + experiential axes).

**Evidence:**
- `ls C:\dev\` returns `reincarnated-collaboration` + `reincarnated-unreal` only; no `reincarnated-engine` or `reincarnated-loadout` clones present
- `find C:\dev\reincarnated-collaboration -name "kit_star_sign*"` returns no matches (Phase 2 sidecar not propagated into meta-repo)
- `find C:\dev\reincarnated-collaboration -name "*kit_corpus*" -o -name "*atomic-substrate*"` returns ONLY the canonical-story narrative doc (no JSON sidecar)
- `agentic_orchestration/legolas/research/2026-06-09-zodiac-substrate-corpus/` IS present with corpus YAMLs (legolas zodiac IS reachable)

**Recommended remediation (David-H to route to Matt or Mac-KR):** Choose ONE of three paths before mantis Phase 1 fires:

1. **Path A — Clone engine + loadout repos on PC.** Adds `C:\dev\reincarnated-engine\` and `C:\dev\reincarnated-loadout\` to PC sibling clones; preserves single-source-of-truth at engine/loadout origin. Requires Mac-side push discipline to keep PC clones current. Adds atomic-substrate-registry + experiential-axes JSON sidecar emission to engine repo (not yet existing).
2. **Path B — Emit Mac-side staging JSON exports into meta-repo before WS1 fires.** Engine emits cycle-14 kit corpus snapshot to `agentic_orchestration/staging/ws1/kits/`; loadout emits Phase 2 sidecar snapshot to `agentic_orchestration/staging/ws1/kit_star_sign/`; gandalf or rocket authors atomic-substrate-registry JSON sidecar to `agentic_orchestration/staging/ws1/primitive_families/` per Layer 0 20-family canonical; gandalf or rocket authors experiential-axes JSON sidecar per hypothesis-flow § 1.8. Single-repo PC pull then captures all sources. Trade-off: staging-JSON discipline must be sustained for future cycles.
3. **Path C — Hybrid (legolas zodiac via meta-repo; engine + loadout via PC clone; substrate + axes JSON emitted to meta-repo staging).** Minimal cloning + minimal staging.

**Cite:** Principle #3 (cross-seam impact); ADR-004 (cross-seam handoff); WS1 § 1.3 staging assumption.

**Routing:** This BLOCK is precondition-level. WS1 commission text does not need re-authoring; the source-JSON staging path needs ratification. David-H surfaces to Matt or Mac-KR for which-path-A/B/C decision. WS1 commission can amend § 1.3 in-place once path is ratified, OR david-h authors a pre-fire memo capturing the chosen path. WS3 Phase WS3.1 can fire in parallel with this resolution (WS3.1 does not consume WS1 data; only WS3.2 onward does).

---

### WARN-WS1-A — Cross-DataTable foreign-key schema choice undeclared

**Severity:** WARN

**Summary:** Acceptance criterion #6 asserts cross-DataTable FK resolvability without specifying the FK representation pattern. UE-idiomatic patterns differ: (a) string-keyed FK lookups via `DataTable->FindRow<T>(FName(*kit_id_string))`; (b) UE `FDataTableRowHandle` typed references; (c) bare FName fields. Each has different ergonomics for downstream Blueprint authoring and editor-time validation. Mantis discretion is acceptable but leaving silent risks rework if downstream WS3 cinematic composition expects a different pattern than mantis chose.

**Recommended remediation:** Add to commission § 1.1 (or § 1.2): "FK representation: mantis chooses UE-idiomatic pattern (recommended: `FDataTableRowHandle` typed reference for editor-time FK validation); document chosen pattern in WS1 wave-close memo for WS3 + vertical-slice spike downstream consumption."

**Cite:** Principle #3 (downstream consumer surface); Discipline #1 (math-before-code at schema-design layer).

---

### WARN-WS1-B — Expected row counts incomplete in criterion #3

**Severity:** WARN

**Summary:** Criterion #3 ("Row counts match source JSON entry counts") cites only 3 of 5 expected counts (37 kit-sign, 423 star-signs, 20 primitive families). DT_Kit and DT_ExperientialAxis row counts are TBD. Without explicit numerals, mantis derives counts at execution time, and Sam Gate-2 cannot verify "match" without independent count extraction. Hardens the verification gate.

**Recommended remediation:** Surface explicit row-count numerals in criterion #3:
- DT_Kit = N (current cycle-14 export count; gandalf or rocket surfaces from latest cycle-14 run)
- DT_ExperientialAxis = N (hypothesis-flow § 1.8 axis count; gandalf surfaces; ~4-7 axes per the multi-axis architecture)

If the counts cannot be surfaced at commission-author time, criterion #3 should specify "row count matches source JSON entry count AND is documented in wave-close memo for Sam Gate-2 verification" so the verification path is unambiguous.

**Cite:** Principle #2 (smoke-gate adequacy); Discipline #11 (empirical-first verifiability).

---

### WARN-WS1-C — Cross-DataTable FK criterion lacks worked example

**Severity:** WARN

**Summary:** Criterion #6 ("Cross-DataTable foreign keys resolvable") is a semantic statement without an operational check. Sam Gate-2 verification would require independent FK-resolution test authoring. Adding a single worked example provides reproducible verification.

**Recommended remediation:** Append to criterion #6: "Worked example: given DT_KitStarSign row with kit_id=X and star_sign_id=Y, lookup of X in DT_Kit returns the matching kit row AND lookup of Y in DT_StarSign returns the matching star-sign row. Document one such worked example per kit-to-star-sign Phase 2 MVP triplet in wave-close memo."

**Cite:** Principle #2 (smoke-gate operationalization); Discipline #10 (single-variable change attribution at verification layer).

---

### INFO-WS1-A — MIGRATION.md trigger condition surfacing for downstream consumption

**Severity:** INFO

**Summary:** WS1 establishes 5 cross-seam contracts (engine kit JSON ↔ UE DT_Kit; loadout sidecar JSON ↔ UE DT_KitStarSign; legolas corpus YAML ↔ UE DT_StarSign; substrate JSON ↔ UE DT_PrimitiveFamily; axes JSON ↔ UE DT_ExperientialAxis). Per ADR-004, milestone-tag fires require MIGRATION.md at cross-seam interface change. WS1 commission is pre-tag (wave-close memo, not milestone tag). MIGRATION.md trigger activates at downstream tag — typically vertical-slice spike completion.

**Recommended remediation (informational; not blocking):** Add to WS1 § 3 discipline citations: "MIGRATION.md required at first milestone-tag downstream of WS1 (likely post-vertical-slice spike). Wave-close memo surfaces each of the 5 cross-seam contracts in stable form for downstream MIGRATION.md authoring." Defer to downstream Sam Gate-2 at milestone-tag time.

**Cite:** Principle #3 (cross-seam contract surfacing); ADR-004 (cross-seam handoff).

---

### INFO-WS1-B — Decisions-log entry for db-lyon adoption still in flight to Mac-jack-ryan

**Severity:** INFO

**Summary:** WS1 cites db-lyon `aaaeb85` as empirical authorization. Sam Proposal 1 to Mac-jack-ryan (decisions-log entry for db-lyon adoption) was filed 2026-06-08 and remains in flight. WS1 proceeds on spike-PASS authorization independent of decisions-log canonical-write timing. No blocker; flag for downstream coherence.

**Cite:** Sam Gate-2 INFO-001 (2026-06-08); sam-OP § 6.6.

---

## 3. WS3 review — per-principle

### 3.1 Math-before-code (Principle #1)

Satisfied. WS3 cites canonical § 2.5 materialization cinematic intent + § 12.9 spirit guide voice patterns + db-lyon Sequencer 7/7 PASS. The cinematic structure (§ 1.1 7-step sequence) is sourced from existing canonical commitments and prior Veo materialization prompt vocabulary (per cosmograph-pivot § 7 PARKED→ recontextualized). Math foundation is sound at design-intent layer.

**Observation:** keyframe transition math (4-phase spirit form transformation: concretization → racial → elemental → weapon) is left to mantis discretion. This is appropriate — keyframe transition timing is a craft decision better made empirically at the Sequencer authoring layer than pre-specified in commission. INFO-only observation.

### 3.2 Smoke-gate coverage (Principle #2)

Adequate at commission scope. Acceptance criteria #1-#12 form a complete smoke-gate ladder (Sequencer asset creation → 5-track structure → 4-phase transformation → voice integration → camera composition → playback → persistence → performance → WS1 composition → Gate-2 → wave-close → D7 preservation).

**Gap:** criterion #8 ("Performance: cinematic playback smooth at AAA fidelity") is qualitative. "Smooth" is unverifiable without a target framerate. At AAA fidelity per the vertical-slice spike AMENDMENT criterion #13 ("60 FPS at AAA fidelity per TSR+TAA"), WS3 cinematic should hold the same target. WARN to specify.

### 3.3 Cross-seam impact (Principle #3)

WS3 declares "independent of WS2 Niagara verification" in STATUS line. Verification:
- WS3 cinematic uses Sequencer (validated 7/7 in spike), NOT Niagara
- WS3 § 1.2 action table uses only Sequencer actions (`create_sequence`, `add_track`, `add_section`, `set_keyframe`, `save_asset`, `play_sequence`, `get_sequence_metadata`)
- WS3 § 1.1 cinematic sequence does include a "VFX track" (criterion #2: "5 tracks present: camera / transform / VFX / audio / spirit guide voice"). If "VFX track" implies Niagara emitter spawning at cinematic moments, then WS3 indirectly depends on `add_emitter_to_system` (the WARN-001 surface from prior Sam Gate-2). This is ambiguous in the commission.

**Severity:** WARN-WS3-A. Clarify VFX track scope — placeholder VFX (Sequencer particle-track without Niagara), OR Niagara-driven VFX (gated on WARN-001 resolution).

WS3 declares dependency on WS1 ("DataTables provide matched-kit data for cinematic composition"). Per § 7 sign-off, "can fire in parallel with WS1 since Sequencer authoring is independent of DataTable contents." This is true for Phase WS3.1 (cinematic asset authoring with placeholder data) but criterion #9 ("Composition with WS1 (DataTables provide matched-kit data for cinematic) operational") REQUIRES WS1 GREEN. So WS3 fires in parallel WITH PHASE PARTITION: WS3.1 can fire in parallel with WS1 staging-JSON resolution; WS3.2-WS3.4 + criterion #9 verification require WS1 GREEN before completion. The commission text could surface this phase-partition more explicitly.

**Severity:** WARN-WS3-B (phase-partition surfacing).

### 3.4 Decisions-log as truth (Principle #4)

Authority claims compliant. WS3 cites § 2.5 + § 12.9 + canonical 40 D28-D32 + D7 AI-tell line. All canonical. No overreach.

### 3.5 Severity calibration + criterion sufficiency

Twelve criteria are appropriate scope. Three observations:

- Criterion #4 ("Spirit guide voice plays at sequence start + end per § 12.9 template") — voice "plays" implies an audio asset is present. WS3 § 5 out-of-scope rules OUT "Voice acting recording (human-cast post-canonical-voice-character-lock per § 12.13)" + "Music + SFX (canonical 38 D7 — human-composed; deferred)." So criterion #4 cannot mean human voice acting. It means templated TTS or placeholder voice asset. WARN to disambiguate: "Spirit guide voice integration validated via templated TTS placeholder OR silent caption track; canonical voice-acting deferred per § 12.13."
- Criterion #8 ("Performance: cinematic playback smooth at AAA fidelity") — qualitative; needs framerate target. WARN-WS3-C below.
- Criterion #12 ("D7 AI-tell line preserved (spirit guide voice templated; no raw LLM dialogue)") — correctly cited. No issue. The D7 line is structurally preserved by the templated voice approach + narrow-LLM-blank-fill per canonical 38 D7 reference.

### 3.6 Cross-seam round-trip discipline (Principle #6)

Cross-seam contract: WS1 DataTable matched-kit data ↔ WS3 Sequencer cinematic composition. WS3 § 1.1 step 1 references "matched kit" as a runtime parameter to the cinematic; this is a runtime data binding, not a structural contract. MIGRATION.md not triggered at WS3 scope.

WS3 composition with § 12.9 spirit guide narration template is a content-level contract; the template structure (§ 12.9 table) is canonical. No round-trip concern.

### 3.7 Discipline citations review

- **D7 AI-tell line** — cited correctly. Templated voice; no raw LLM dialogue.
- **Canonical 40 D28-D32 spirit guide neutral data-oracle voice** — cited; preserved.
- **§ 12.9 voice patterns** — cited; preserved.
- **Recognition-validate-commit** — cited; WS3 IS empirical validation of § 2.5 materialization cinematic intent. Correct.

**Missing:** the WS3 commission does NOT cite ADR-006 (db-lyon BUSL-1.1 license posture). WS1 cites this; WS3 uses the same tooling and should reference it for parallel discipline. INFO-only.

### 3.8 Estimated wall-clock

"1-3 weeks UE mantis work per Mantis convention" — reasonable for 5-phase Sequencer cinematic with voice integration + camera composition + 4-phase transformation. Convention-consistent. No concern.

---

## 4. WS3 findings (BLOCK / WARN / INFO)

### WARN-WS3-A — VFX track scope ambiguous (placeholder Sequencer particle track vs Niagara-driven)

**Severity:** WARN

**Summary:** Criterion #2 requires 5 tracks including "VFX." If VFX track implies Niagara emitter spawning via Sequencer Niagara integration, WS3 indirectly depends on `add_emitter_to_system` (prior Sam Gate-2 WARN-001 — windowed-mode verification pending). If VFX track is Sequencer-native particle-system track (or empty/placeholder), no Niagara dependency. The commission is silent.

**Recommended remediation:** Add to commission § 1.2 (or § 2 Phase WS3.1 acceptance): "VFX track scope: Sequencer-native particle-system track or placeholder track at WS3 baseline; full Niagara cluster-rune VFX integration deferred to vertical-slice spike assembly (gates on WS2 GREEN per Option B Niagara windowed-mode verification)."

**Cite:** Sam Gate-2 WARN-001 (2026-06-08); Principle #3 (cross-seam impact at tooling layer).

---

### WARN-WS3-B — Phase-partition for WS1 dependency surfacing

**Severity:** WARN

**Summary:** § 7 sign-off states "can fire in parallel with WS1 since Sequencer authoring is independent of DataTable contents" but criterion #9 ("Composition with WS1 ... operational") requires WS1 GREEN. The partition is implicit: Phase WS3.1 (asset authoring) can parallel WS1 staging-JSON resolution; Phase WS3.2-WS3.4 + criterion #9 require WS1 GREEN. The commission could make this explicit so david-h doesn't accidentally route WS3 criterion-#9 verification before WS1 GREEN.

**Recommended remediation:** Append to § 7 sign-off "Gates on:" line: "Gates on: WS1 GREEN for Phase WS3.2-WS3.5 + criterion #9 verification ONLY; Phase WS3.1 (Sequencer asset authoring with placeholder data) can fire in parallel with WS1 staging-JSON resolution."

**Cite:** Principle #3 (cross-seam dependency surfacing).

---

### WARN-WS3-C — Performance criterion #8 needs framerate target

**Severity:** WARN

**Summary:** Criterion #8 "Performance: cinematic playback smooth at AAA fidelity" is qualitative. Per vertical-slice spike AMENDMENT criterion #13 (60 FPS at AAA fidelity per TSR+TAA), WS3 cinematic should hold the same target. "Smooth" is not Gate-2-verifiable; "60 FPS minimum during cinematic playback per TSR+TAA pipeline" is.

**Recommended remediation:** Replace criterion #8 with: "Performance: cinematic playback holds ≥60 FPS at AAA fidelity per TSR+TAA pipeline (target consistent with vertical-slice spike AMENDMENT criterion #13)."

**Cite:** Principle #2 (smoke-gate verifiability); Discipline #11 (empirical-first verifiability).

---

### WARN-WS3-D — Criterion #4 voice integration scope unclear (templated TTS vs human voice acting deferred per § 12.13)

**Severity:** WARN

**Summary:** Criterion #4 requires spirit guide voice to "play" at sequence start + end. WS3 § 5 out-of-scope excludes voice acting recording (deferred per § 12.13). The criterion implicitly assumes templated TTS placeholder OR silent caption track. Disambiguation prevents mantis from over-scoping.

**Recommended remediation:** Update criterion #4 to: "Spirit guide voice integration validated via templated TTS placeholder OR silent caption track per § 12.9 template structure. Canonical human voice-acting recording deferred per § 12.13."

**Cite:** Principle #2 (smoke-gate scoping clarity); D7 AI-tell line (templated structure preservation).

---

### INFO-WS3-A — ADR-006 (db-lyon BUSL-1.1 posture) not cited in discipline section

**Severity:** INFO

**Summary:** WS3 uses db-lyon Sequencer tooling. WS1 cites ADR-006 in its discipline section; WS3 does not. Parallel discipline framing would benefit from including ADR-006 in WS3 § 4. Minor.

**Recommended remediation:** Add to WS3 § 4 discipline citations: "ADR-006 — read-only-by-default external systems; db-lyon BUSL-1.1 base evaluation grant covers WS3 same as WS1."

**Cite:** Principle #3 (consistent discipline-framing across paired commissions).

---

## 5. Cross-dispatch consistency findings

### INFO-CROSS-A — Parallel-fire feasibility under UE single-Editor-instance constraint

**Severity:** INFO

**Summary:** Matt's directive 2026-06-10 specified WS1 + WS3 fire in parallel. UE Editor cannot run two concurrent Editor instances on the same project without worktree isolation. WS1 (DataTable authoring + JSON ingestion) and WS3 (Sequencer asset authoring) BOTH require the UE Editor running with `Reincarnated.uproject`. Practical parallel-fire requires ONE of:

1. **Sequential session pattern within a single mantis invocation** — mantis runs WS1 Phase 1 (struct authoring) in one Editor session, closes Editor, opens for WS3 Phase WS3.1 (Sequencer asset authoring), closes Editor, returns to WS1 Phase 1.5 (JSON ingestion), etc. High context-switch cost; not true parallelism.
2. **Interleaved phasing** — mantis fires WS1 BLOCK-WS1-A staging-JSON resolution (which is david-h + Matt + Mac-side routing; not mantis Editor time) IN PARALLEL with WS3 Phase WS3.1 (mantis Editor-time Sequencer asset authoring with placeholder data). This is the practical parallel-fire path: WS3.1 fires immediately; WS1 fires after BLOCK-WS1-A is resolved.
3. **Worktree isolation per UE project** — would require duplicating `C:\dev\reincarnated-unreal\Reincarnated\` into a worktree clone; non-trivial overhead for a single-mantis-executor pattern. Not recommended unless explicitly authorized.

**Recommended disposition:** Path 2 (interleaved phasing) preserves Matt's parallel-fire intent without overhead. David-H routes:
1. WS3 Phase WS3.1 mantis fires immediately (no preconditions; uses db-lyon Sequencer tooling validated 7/7)
2. WS1 BLOCK-WS1-A staging-JSON resolution routes to Matt or Mac-KR in parallel (Mac-side action)
3. Once BLOCK-WS1-A resolves, WS1 mantis fires
4. WS3 Phase WS3.2-WS3.5 + criterion #9 verification fires after WS1 GREEN

This preserves the spirit of Matt's parallel-fire directive while honoring UE single-Editor-instance constraint.

**Cite:** Mantis OP (single-Editor-instance constraint); Principle #5 (severity matters; coordination concern surfaced as INFO not BLOCK).

---

## 6. Pre-fire amendments — concrete edit list

### WS1 amendments (PASS-WITH-AMENDMENTS; block resolution prerequisite)

**Must-resolve before Phase 1 fires (BLOCK-WS1-A):**
- David-H routes source-JSON staging path A/B/C decision to Matt or Mac-KR. Until resolved, WS1 Phase 1 does NOT fire. Commission text amendment to § 1.3 can wait until path is ratified, OR david-h authors a pre-fire memo capturing the chosen path.

**Should-edit (WARN-WS1-A/B/C):**
- § 1.1 or § 1.2: add FK representation guidance — "mantis chooses UE-idiomatic pattern (recommended: `FDataTableRowHandle` typed reference); document chosen pattern in WS1 wave-close memo"
- § 2 criterion #3: surface explicit row-count numerals for DT_Kit (cycle-14 export count) + DT_ExperientialAxis (hypothesis-flow § 1.8 axis count); if not surfaceable at commission-author time, add "AND is documented in wave-close memo for Sam Gate-2 verification"
- § 2 criterion #6: append worked-example assertion per Phase 2 MVP triplet

**Could-edit (INFO-WS1-A/B; defer to downstream consumption):**
- § 3: surface MIGRATION.md downstream trigger condition for vertical-slice spike consumption
- (no action) db-lyon decisions-log entry in flight to Mac-jack-ryan; downstream coherence flag

### WS3 amendments (PASS-WITH-AMENDMENTS; no block)

**Should-edit (WARN-WS3-A/B/C/D):**
- § 1.2 or § 2 Phase WS3.1: clarify VFX track scope as Sequencer-native or placeholder; full Niagara VFX integration deferred to vertical-slice spike
- § 7 sign-off "Gates on:" line: surface phase-partition (Phase WS3.1 can fire in parallel with WS1 staging-JSON resolution; Phase WS3.2-WS3.5 + criterion #9 require WS1 GREEN)
- § 2 criterion #8: replace qualitative "smooth" with "≥60 FPS at AAA fidelity per TSR+TAA pipeline"
- § 2 criterion #4: disambiguate voice integration as templated TTS placeholder OR silent caption track; canonical human voice-acting deferred per § 12.13

**Could-edit (INFO-WS3-A):**
- § 4 discipline citations: add ADR-006 db-lyon BUSL-1.1 posture parallel to WS1 framing

---

## 7. Routing implication

**Per-commission verdict:**
- WS1: PASS-WITH-AMENDMENTS (1 BLOCK at precondition layer; 3 WARN at criterion-sharpening layer; 2 INFO at coherence layer)
- WS3: PASS-WITH-AMENDMENTS (0 BLOCK; 4 WARN at criterion-sharpening layer; 1 INFO at coherence layer)

**Routing decision for david-h:**

1. **WS3 Phase WS3.1 fires immediately** per cross-dispatch consistency INFO-CROSS-A Path 2. Mantis can author Sequencer asset + 5 tracks (criterion #1 + criterion #2) using db-lyon validated 7/7 Sequencer tooling with placeholder data. No WS1 dependency at Phase WS3.1. The WARN amendments to WS3 are NOT precondition-level; mantis can be routed to WS3.1 with david-h capturing the amendments in routing memo OR david-h amending the commission in-place.

2. **WS1 BLOCK-WS1-A staging-JSON resolution routes to Matt or Mac-KR in parallel.** This is a Mac-side decision (Path A: clone repos on PC; Path B: Mac-side staging JSON emission into meta-repo; Path C: hybrid). Once ratified, WS1 commission § 1.3 amends in-place (or david-h authors pre-fire memo) and mantis WS1 Phase 1 fires.

3. **WS3 Phase WS3.2-WS3.5 + criterion #9 verification fires after WS1 GREEN** per phase-partition surfaced in WARN-WS3-B.

4. **Vertical-slice spike assembly fires after all preconditions GREEN** (WS1 + WS2 + WS3 + Sam WARN-002 BP-mutation pre-fire gate + Phase 5 drax amendment GREEN per vertical-slice spike AMENDMENT § 2).

**Parallel-fire preservation:** Matt's parallel-fire directive is preserved at the COMMISSION-AUTHORIZATION layer (both PASS-WITH-AMENDMENTS) AND at the EXECUTION layer (WS3.1 + WS1 BLOCK-resolution parallel). UE single-Editor-instance constraint is honored via phase-partition rather than violated.

**No Mac-jack-ryan consultation triggered by this Gate-1.** All findings resolve within PC-seam scope OR route to Matt / Mac-KR for cross-seam staging decisions (not cross-cutting decisions-log or engineering-discipline writes).

**ADR-002 tiered-approval scope:** WARN and INFO items are PC-seam-internal commission amendments + criterion-sharpening; david-h has authority to surface amendments in routing memo without further Matt escalation. BLOCK-WS1-A staging-JSON path-A/B/C decision escalates to Matt (cross-seam coordination at Mac-side scope).

---

## 8. Sign-off

**Reviewer:** sam (PC-side QA gatekeeper)
**Mode:** DESIGN-MODE Gate-1 (paired pre-fire review; OP Pattern A-deep file artifact verdict)
**Date:** 2026-06-10
**Commit:** auto-commit per CLAUDE.md PC team auto-commit table (sam row: "PC-seam Gate-1 / Gate-2 findings")
**Push:** per PC-seam standing wave-close push pattern at next wave-close (this finding accumulates with mantis WS3.1 + WS1 BLOCK-resolution + downstream wave commits; pushes together)

**Downstream routing:**
- David-H: consumes Gate-1 verdict; routes WS3 Phase WS3.1 to mantis immediately; routes WS1 BLOCK-WS1-A staging-JSON path-A/B/C decision to Matt or Mac-KR; amends commissions in-place per § 6 edit list OR captures amendments in routing memo
- Matt: receives BLOCK-WS1-A staging-JSON path-A/B/C decision via david-h surfacing; ratifies path
- Mac-KR: cross-host fetch at next Mac session; consumes BLOCK-WS1-A surfacing if Mac-side staging emission is chosen (Path B or C)
- Mantis: receives WS3 Phase WS3.1 routing from david-h; executes Sequencer asset authoring + 5-track structure with placeholder data using db-lyon Sequencer tooling
- Mac-jack-ryan: no consultation triggered by this Gate-1; Sam Proposal 1 (db-lyon decisions-log entry) remains in flight from 2026-06-08 separately

**End of Gate-1 finding.**
