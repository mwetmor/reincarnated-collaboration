# Dispatch — 2026-05-16 — star-lord — Cipher-migration paths-audit (P6 forward audit CRITICAL #2) + R11(d) recorder fail-loud

**From:** knight-rider (authored per gandalf P6 forward audit `canonical/story/p6-forward-audit-2026-05-16.md` § VS2b S3 CRITICAL recommendation + Drift-12 R11(d) routing per Matt 2026-05-16 Day 4 directive)
**To:** star-lord
**Approved by:** Matt at 2026-05-16 Day 4 ("R11 routing fold it into the dispatch")
**Status:** PENDING — HOLD-on-prior. Do NOT execute until star-lord V2.2+V2.3 DB migration completes + fresh-regen post-V2.1-emission-gap-fix completes; star-lord can only run one dispatch per session. Sequence: V2.2+V2.3 migration → fresh regen → THIS.
**Estimated effort:** 2-3 sessions (~6-10h); paths-audit is inventory + classification work + R11(d) recorder fail-loud addition is small code change; combined dispatch ships both deliverables.
**Acceptance:** Canonical-four paths-audit document filed at `agentic_orchestration/research/cipher-migration-paths-audit-2026-05-16.md` enumerating every site emitting canonical-four labels across 6 surface classes; per-site classification (INTENDED-INTERNAL / INTENDED-PUBLIC-AS-CIPHER / LEAK-RISK / TO-BE-FILTERED); plus recorder.py fail-loud-on-silent-drop logic added per R11(d) prevention prescription (Pattern P7); intermediate tag for the recorder code change; MIGRATION.md entry per ADR-004.

---

## Why this dispatch exists

### Track A — Paths-audit (P6 forward audit CRITICAL recommendation)

Per `canonical/story/p6-forward-audit-2026-05-16.md` § VS2b S3 (Hide canonical-four from LLM — cipher migration):

> **Severity: CRITICAL** (for VS2b S3 ship). The cipher migration's value is undermined if canonical-four labels leak through any non-LLM path that touches player or public-facing surfaces. **Recommend: paths-audit dispatch to star-lord** before S3 implementation begins. Inventory every place canonical-four labels appear in: (1) telemetry events; (2) export packet fields; (3) Spirit Guide prompt templates; (4) Spirit Guide voice output; (5) loadout app data display; (6) debug logging at any level. For each, classify as INTENDED-INTERNAL / INTENDED-PUBLIC-AS-CIPHER / LEAK-RISK / TO-BE-FILTERED. Without this audit, S3 ships with the cipher leaking through unaudited paths.

**Form-bias cadence positioning**: form-bias Stage 1 (embodiment-axis additive) just landed today @ `rocket/v1.3-form-bias-stage-1-embodiment-axis @ 73db17f`. Stage 2 (grouping-layer; dispatch authoring pending) and Stage 3 (cipher migration; star-lord prompt-construction changes) are sequenced behind Stage 1. **This paths-audit MUST precede form-bias Stage 3 implementation** — Stage 3 is where canonical-four hides from LLM; the audit tells Stage 3 every non-LLM surface that needs same-treatment filtering.

### Track B — Recorder fail-loud-on-silent-drop (Drift-12 R11(d))

Per `canonical/story/drift-audit.md` Drift-12 + Pattern P7 + R11 recommendation (gandalf filed 2026-05-16 Day 4) routes (d) **recorder-side fail-loud-on-silent-drop** to star-lord at next recorder.py touch. Matt directed (2026-05-16) "R11 routing fold it into the dispatch."

The Drift-12 instance: `loadout_json: None` silently skipped 1114 rows in recorder.py line 477's `is None → continue` guard. Pattern P7 — test scaffolding (star-lord v2.1 smoke synthetic loadout_json injection) masked the production gap. The structural root cause beyond the test workaround: **the recorder silently skipped on None instead of failing loud or logging-and-counting**.

**Folding (d) into this dispatch**: since this dispatch already brings star-lord into recorder.py for paths-audit work, the recorder fail-loud change is small additional scope. Two-for-one efficiency.

## What this dispatch produces

### Track A — Paths-audit document

Output: `agentic_orchestration/research/cipher-migration-paths-audit-2026-05-16.md` (gandalf consumes for form-bias Stage 3 dispatch authoring)

**Structure:**

#### Section 1 — Audit methodology
- Search-pattern strategy (grep for canonical-four element names + element pool entries; cross-reference with substrate-tag emission sites)
- Inclusion criteria (any code path that emits / logs / persists / displays / passes-to-LLM a canonical-four label)
- 6 surface classes from P6 forward audit recommendation:
  1. Telemetry events (engine-side recorder + emission paths)
  2. Export packet fields (engine → external consumer payloads)
  3. Spirit Guide prompt templates (LLM-bound text)
  4. Spirit Guide voice output (LLM response handling + display)
  5. Loadout app data display (drax-side rendering)
  6. Debug logging at any level (Python logging, print, console.log, etc.)

#### Section 2 — Per-site enumeration (the load-bearing inventory)

For each canonical-four label emission site, document:
- File path + line number
- Code context (one-line excerpt)
- Surface class (which of the 6 above)
- Per-site classification (one of):
  - **INTENDED-INTERNAL** — site stays canonical-four; internal-only path; no leak risk (e.g., generation-side substrate tracking)
  - **INTENDED-PUBLIC-AS-CIPHER** — site already designed to surface per-season vocabulary, not canonical-four (e.g., player-facing UI label resolver)
  - **LEAK-RISK** — site emits canonical-four label on a public-facing path; **REQUIRES filtering before Stage 3 ship**
  - **TO-BE-FILTERED** — known leak-risk site with planned filter at Stage 3 implementation (subset of LEAK-RISK that's already in Stage 3 plan)

#### Section 3 — Per-surface-class summary
- Per class: total sites; INTENDED-INTERNAL count; LEAK-RISK count; TO-BE-FILTERED count
- Observation on which surface classes are most leak-prone

#### Section 4 — LEAK-RISK enumeration (the load-bearing output for Stage 3)
- All LEAK-RISK sites listed; per-site recommendation for filter approach
- Priority tier (must-fix-for-Stage-3 vs nice-to-fix-with-Stage-3-followon)

#### Section 5 — Recommendations for form-bias Stage 3 dispatch authoring
- Concrete filter-implementation guidance per LEAK-RISK site
- Cross-seam consumer notes (drax loadout display; gamora telemetry; rocket generation; etc.)
- Rubric-extension recommendations if the 6-surface-class taxonomy proves insufficient

### Track B — Recorder fail-loud-on-silent-drop

Code change in `reincarnated-engine/src/reincarnated/telemetry/recorder.py`:

**Current pattern** (recorder.py line 477 + similar sites):
```python
if loadout_json is None:
    continue
```

**Replace with fail-loud-on-silent-drop pattern** (your design call on exact form; suggested shape):
```python
if loadout_json is None:
    self._silent_drop_counter['loadout_json_none'] += 1
    self._logger.warning(
        f"recorder skipped entry due to None loadout_json; "
        f"row_count={self._silent_drop_counter['loadout_json_none']}; "
        f"first-occurrence inspect: {entry.get('class_name')=} {entry.get('encounter_index_within_room')=}"
    )
    continue
```

**Acceptance for Track B:**
- Skip-counter dict added to recorder state (per-skip-class counters)
- Warning logger emits at WARN level on each skip with diagnostic context
- At recorder-close / batch-complete, summary log emits total skips per class (e.g., "recorder skipped 1114 entries: 1114 due to None loadout_json")
- Smoke test: synthetic loadout_json=None entry triggers warning + counter increment
- Audit all `is None → continue` patterns elsewhere in recorder.py and apply the fail-loud pattern uniformly
- Per Discipline #12 (semantic shift): documented in MIGRATION.md as v1.6 entry

## Cross-seam considerations

### Track A — Paths-audit
- **Rocket**: READ-ONLY upstream — rocket emits canonical-four labels at generation; Section 2 inventory should include generation-side emissions
- **Gamora**: READ-ONLY — sim consumes canonical-four for damage resolution; sim-side emission sites are paths-audit candidates
- **Drax**: READ-ONLY downstream — loadout app data display is surface class #5; drax-side label-resolution sites need inventory
- **Gandalf**: PRIMARY DOWNSTREAM CONSUMER — paths-audit output is direct input to form-bias Stage 3 dispatch authoring
- **Elrond**: NO interaction
- **Knight-rider**: notify at completion; Stage 3 dispatch authoring activates with paths-audit findings in hand

### Track B — Recorder fail-loud
- **Gamora**: READ-ONLY — gamora's recorder fixes from V2.1 emission-gap-fix dispatch interact with this change; verify fix is preserved
- **Knight-rider**: notify at completion; MIGRATION.md v1.6 entry filed

## Out of scope (explicit)

- **NO form-bias Stage 3 implementation** — Stage 3 is a separate future dispatch; this is the AUDIT that informs Stage 3 authoring
- **NO filtering / cipher migration code changes** — only INVENTORY + CLASSIFICATION; actual filter implementation is Stage 3 work
- **NO recorder refactor beyond fail-loud pattern** — surgical change only; broad recorder cleanup is separate scope
- **NO Spirit Guide implementation changes** — paths-audit identifies prompt-template sites; doesn't modify them
- **NO drax loadout app changes** — paths-audit identifies display sites; drax does any actual changes in Stage 4
- **NO retrospective backfill on Drift-12 silent-dropped rows** — those rows are gone; fresh regen produces clean data going forward
- **NO V2.x DB schema changes** — recorder code-side fail-loud only; no telemetry schema migration

## Required reading

- `canonical/story/p6-forward-audit-2026-05-16.md` § VS2b S3 (CRITICAL recommendation; your scope source)
- `canonical/story/drift-audit.md` Drift-12 + Pattern P7 + R11 (Track B framing)
- `canonical/story/form-bias-cadence-strategy.md` § Stage 3 cipher migration (downstream consumer of Track A)
- `canonical/story/pre-llm-substrate-inventory.md` (canonical-four label inventory; baseline for grep patterns)
- `reincarnated-engine/src/reincarnated/telemetry/recorder.py` (Track B target file)
- `reincarnated-engine/src/reincarnated/export/MIGRATION.md` (your prior v2.x pattern; v1.6 entry target)
- Your prior dispatches' MIGRATION.md entries (pattern reference for the v1.6 entry framing)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #2 (smoke); #12 (semantic-shift: recorder behavior change); #13a (implementation-vs-intent drift — paths-audit IS this discipline applied); #14 (internal-vs-generative schema separation — the discipline this audit operationalizes)

## Acceptance criteria

### Track A — Paths-audit
- [ ] Audit doc at `research/cipher-migration-paths-audit-2026-05-16.md` filed
- [ ] All 6 surface classes inventoried
- [ ] Per-site classification per the 4-tier rubric
- [ ] LEAK-RISK enumeration with per-site filter recommendation
- [ ] Section 5 recommendations for Stage 3 dispatch authoring
- [ ] Cross-references to P6 forward audit + Drift-12 + form-bias cadence

### Track B — Recorder fail-loud
- [ ] Skip-counter dict added; per-class counter tracking
- [ ] WARN-level logger on each silent skip with diagnostic context
- [ ] Batch-complete summary log emits total skips per class
- [ ] Audit of all `is None → continue` patterns in recorder.py; apply uniformly
- [ ] Smoke test for None-trigger → warning + counter increment
- [ ] MIGRATION.md v1.6 entry filed (Discipline #12 semantic-shift note)
- [ ] Intermediate tag `star-lord/v1.3-recorder-fail-loud` at the recorder code change commit
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified at completion

## Tag policy

- **Intermediate tag:** `star-lord/v1.3-recorder-fail-loud` at the commit closing recorder fail-loud + tests pass. (Track B has code; Track A is analytical research output, tag-less per convention.)
- **Milestone tag:** none from this dispatch.

---

## Completion record

**Completed:** 2026-05-16

**Track A — Paths-audit doc path:**
`agentic_orchestration/research/cipher-migration-paths-audit-2026-05-16.md`

**Track A — LEAK-RISK site count:**
26 LEAK-RISK sites across 48 total (8 of 26 are TO-BE-FILTERED / already in Stage 3 plan; 18 are newly surfaced). Export packet (surface class 2) is the highest-concentration surface at 11/11 sites LEAK-RISK. Stage 3 scope must expand beyond LLM prompt filters to include export schema additions and manifest elements block restructuring.

**Track B — Intermediate tag:**
`star-lord/v1.3-recorder-fail-loud` at commit `9baa4f8`

**Track B — Smoke status:**
PASSED. 12/12 new tests in `tests/test_recorder_fail_loud.py`. 99/99 total telemetry suite (zero regressions). Acceptance criteria verified: skip-counter dict initialized; per-class counter increments on each skip; WARN-level log emitted with count + diagnostic; `summary_drops()` emits aggregate at close; NullRecorder stubs work; non-None entries still persisted normally.

**Track B — MIGRATION.md v1.6 path:**
`reincarnated-engine/src/reincarnated/export/MIGRATION.md` § v1.6 (appended)

**Notes for knight-rider:**

1. **Stage 3 scope expansion**: The paths-audit surfaced 18 LEAK-RISK sites not currently in the Stage 3 plan. Stage 3 must be decomposed into: (a) engine-side LLM prompt filters + export schema additions + manifest elements block (star-lord/rocket seam); (b) drax-side gear display + fallback resolver hardening (drax seam). Recommend Stage 3 dispatch authors acknowledge this decomposition explicitly.

2. **P2-A fallback leak (resolveElementName in drax)**: The `?? canonical_key` fallback in both `SkillDetailPanel.tsx` and `Loadout.tsx` is a structural weak point that returns canonical-four labels when manifest lookup fails. Low-priority for Stage 3 but should be hardened to return a neutral placeholder rather than leaking the canonical label.

3. **R11(b) cross-seam round-trip discipline — 2nd P7 instance in 1 day**: The `season_writer.py` form-bias silent-drop (fixed commit `4bbc906`) and the recorder.py `loadout_json: None` silent-drop (now fail-loud'd by Track B) are both Pattern P7 instances. R11(b) cross-seam round-trip discipline — where a field is generated, exported, imported at the consumer boundary, and validated end-to-end — would have caught both. This is flagged for knight-rider consideration for a future discipline/process dispatch. NOT being actioned autonomously per dispatch routing rules.

4. **LLM call logger (D-03)**: The `logs/llm_YYYYMMDD.jsonl` files persist canonical-four labels from all LLM prompt text. Verify `logs/` is in `.gitignore`. No code change required now (log files are developer-only); flagged for Stage 3 follow-on.

5. **Queue chain continues as dispatched**: form-bias Stage 2 cosmological-vocabulary commission → V2.4 telemetry migration. Both are sequenced and ready for dispatch authoring.
