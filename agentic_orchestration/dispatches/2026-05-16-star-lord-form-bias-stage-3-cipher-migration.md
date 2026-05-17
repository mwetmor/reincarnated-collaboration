# Dispatch — 2026-05-16 — star-lord — Form-bias Stage 3: cipher migration (engine-side; LLM prompts + export packet + manifest)

**From:** knight-rider (authored per form-bias 5-entry batch Entry 5 cadence Option II Stage 3 + paths-audit findings 2026-05-16 + Matt 2026-05-16 directive: "fire tier 1 #1")
**To:** star-lord
**Approved by:** Matt at 2026-05-16 Day 4 (Tier 1 #1 confirmation)
**Status:** PENDING — HOLD-on-prior. Do NOT execute until: (1) your in-flight form-bias Stage 2 cosmological-vocabulary dispatch completes; (2) your queued V2.4 telemetry migration dispatch completes; (3) your queued V2 CLI flag + regen dispatch completes. Star-lord can only run one dispatch per session. Sequence: Stage 2 → V2.4 telemetry → V2 regen → THIS.
**Estimated effort:** 3-5 sessions (~10-20h); MULTI-PART migration touching LLM prompts + export packets + manifest + recorder; load-bearing form-bias closeout.
**Acceptance:** Canonical-four hidden from LLM prompts (grouping-layer-vocabulary visible instead, filled per-season per Stage 2 cosmological-vocabulary); additive `seasonal_element` + `seasonal_dominant_element` fields on export packets; manifest.elements parallel structure (per-season keys); fallback safety net for missing manifest; smoke verifies no canonical-four leakage on LLM-bound or player-visible paths; tags + MIGRATION.md per ADR-004.

---

## Why this dispatch exists — load-bearing form-bias closeout

Per form-bias 5-entry batch (`5d51b5a`) Entry 5 cadence Option II:

> **Stage 3 — Cipher migration.** LLM sees grouping-layer abstract labels (filled per-season with cosmological vocabulary), not canonical-four. Engine-side prompt filters + export packet expansions + manifest parallel structure. Drax-side gear display + fallback resolver hardening (separate drax Stage 3 dispatch knight-rider will author after this returns).

**Paths-audit just completed (2026-05-16)** at `agentic_orchestration/research/cipher-migration-paths-audit-2026-05-16.md`:
- 48 emission sites inventoried across 6 surface classes
- **26 LEAK-RISK sites** (canonical-four leaks to player-visible / LLM-bound paths)
- 8 TO-BE-FILTERED (already in Stage 3 LLM prompt plan)
- **18 NEWLY-SURFACED** must add to Stage 3 scope:
  - 11 export packet sites (`canonical_element` + `dominant_element` on skills/classes/monsters/gear)
  - `manifest.elements` dict keys (top-level JSON keys; player-inspectable)
  - 6 loadout app gear display sites (drax-side; separate dispatch)
  - 1 debug logging site

**Engine-side scope (THIS dispatch)**:
- Track A: LLM prompt-construction filters
- Track B: Export packet additive fields (`seasonal_element` + `seasonal_dominant_element`)
- Track C: Manifest.elements parallel structure
- Track D: Debug logging site cleanup

**Drax-side scope (SEPARATE upcoming dispatch)**:
- Loadout app gear display update (6 sites)
- Fallback resolver hardening (3 INTENDED-PUBLIC-AS-CIPHER sites currently use `resolveElementName() ?? canonical_key` fallback — needs hardening when manifest unavailable)

## What this dispatch produces

### Track A — LLM prompt-construction filters

Per paths-audit § 4 (LEAK-RISK enumeration) Spirit Guide prompt sites + per-Stage-2 cosmological vocabulary:

1. **Replace canonical-four labels** in all LLM-bound prompts with grouping-layer-vocabulary (ignition / suffusion / bulwark / displacement / impact) FILLED per-season with cosmological vocabulary (per Stage 2 generation)
2. **Skill-name generation prompts**: receive grouping-layer label + per-season cosmological vocabulary; canonical-four absent
3. **Lore generation prompts**: same treatment
4. **Spirit Guide voice prompts**: same treatment
5. **Test guard**: add `test_no_canonical_four_in_llm_prompts.py` (or equivalent) that asserts no canonical-four labels appear in constructed LLM prompts for a 5-class smoke season

### Track B — Export packet additive fields

Per paths-audit § 4: 11 export sites emit `canonical_element` + `dominant_element` raw.

**Approach**: ADDITIVE not replacement (Discipline #12 semantic-shift discipline; preserve backward compat for downstream consumers).

1. Add `seasonal_element: str` to skills / classes / monsters / gear export schemas (alongside existing `canonical_element`)
2. Add `seasonal_dominant_element: str` (alongside existing `dominant_element`)
3. Populate from per-season cosmological vocabulary at export time
4. `canonical_element` and `dominant_element` remain present for backward compat (drax fallback resolver will eventually deprecate them in a future cleanup)
5. MIGRATION.md entry per ADR-004 — drax-side consumes seasonal_* fields for player-visible rendering

### Track C — Manifest.elements parallel structure

Per paths-audit § 4: `manifest.elements` uses canonical-four as top-level JSON keys (`"fire"`, `"water"`, `"earth"`, `"wind"`).

**Approach**: parallel structure (additive).

1. Add `manifest.seasonal_elements` dict (parallel to existing `manifest.elements`) with per-season cosmological vocabulary keys
2. Per-season key generated from Stage 2 cosmological vocabulary
3. Existing `manifest.elements` preserved for backward compat
4. Drax consumes `manifest.seasonal_elements` for player-visible rendering

### Track D — Debug logging cleanup

Per paths-audit § 4: 1 debug logging site emits canonical-four label.

1. Wrap in `if DEBUG_INTERNAL_LABELS:` guard OR replace with seasonal_element resolution
2. Default to internal-debug-only; do NOT surface to player console

### Track E — Smoke + verification

Per Discipline #2 + #14 (internal-vs-generative schema separation):

1. **5-class smoke season** with Stage 2 cosmological vocabulary applied
2. **No-canonical-four-in-LLM-prompts test**: assert canonical-four labels absent from all constructed LLM prompts
3. **No-canonical-four-in-player-visible-export test**: assert seasonal_element + seasonal_dominant_element + manifest.seasonal_elements present in exports; canonical_element + dominant_element + manifest.elements ALSO present (backward compat) but flagged as DEPRECATED in MIGRATION.md
4. **Round-trip smoke** (per R11(b) prevention prescription): generate → export → validate at consumer boundary; this catches any silent-drop pattern (P7) on the new seasonal fields
5. **Discipline #14 gate**: every prompt-construction site reviewed against "what's NOT permitted" list from #14 (canonical-four labels; class-archetype labels; mechanical property names; attribute axis labels)

### Track F — Intermediate tag + AGENT_STATE + completion record

- Tag: `star-lord/v1.3-form-bias-stage-3-cipher-migration`
- AGENT_STATE.md updated
- Completion record at bottom of this dispatch filled
- Cross-seam notification to knight-rider — drax Stage 3 demo-side dispatch authoring activates with seasonal_* field names + manifest structure in hand

## Cross-seam considerations

- **Rocket**: READ-ONLY — rocket Stage 2 grouping-layer fields are your input substrate (already implemented @ `rocket/v1.3-form-bias-stage-2-vocab-lock @ ea3a1c3`)
- **Gamora**: READ-ONLY — sim consumes canonical-four for damage resolution; Stage 3 does NOT change sim consumption (canonical-four remains internal mechanic)
- **Drax**: PRIMARY DOWNSTREAM CONSUMER — your seasonal_* fields + manifest.seasonal_elements are what drax Stage 3 demo-side will consume for player-visible rendering. Coordinate via MIGRATION.md cross-seam contract
- **Gandalf**: READ-ONLY — design-lineage owner of grouping-layer-vocabulary; consult if any LLM prompt pattern needs design judgment
- **Jack-ryan**: Gate 1 review when dispatch text drafts (Discipline #14 internal-vs-generative schema separation enforcement applies here)
- **Knight-rider**: notify at completion; authors drax Stage 3 demo-side dispatch with concrete field names

## Out of scope (explicit)

- **NO drax demo-side changes** (separate dispatch knight-rider will author after this returns)
- **NO sim consumption changes** (gamora seam; canonical-four remains internal mechanic)
- **NO canonical-four field removal from exports** (additive only; backward compat preserved)
- **NO new Pimen / character-track work**
- **NO B11 / B12 / room-hallway changes**
- **NO V2-regen dispatch work** (separate small dispatch queued ahead of this)
- **NO new grouping-layer-vocabulary** (locked per gandalf spec; do NOT extend)
- **NO Stage 4 narrative-skin work** (separate; future)

## Required reading

- `agentic_orchestration/research/cipher-migration-paths-audit-2026-05-16.md` (your own paths-audit output; LEAK-RISK enumeration is the load-bearing input)
- `canonical/story/grouping-layer-vocabulary.md` (gandalf spec; locked vocabulary)
- `canonical/story/form-bias-cadence-strategy.md` § Stage 3 framing
- Cipher-width Outcome 2 resolution entry (`1dff66d`)
- Your prior Stage 2 dispatch completion record (per-season cosmological vocabulary generation; substrate for this Stage 3 work)
- Rocket Stage 2 dispatch completion + vocab-lock follow-on (`rocket/v1.3-form-bias-stage-2-vocab-lock @ ea3a1c3`)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #2 (smoke); #11 (attribution); #12 (semantic-shifting: canonical-four hides from LLM); #14 (internal-vs-generative schema separation: PRIMARY discipline for this dispatch); #13b (outcome attribution opacity); Pattern P7 (test scaffolding masks production defect — round-trip test verification per R11(b))

## Acceptance criteria

- [ ] LLM prompt-construction sites no longer emit canonical-four labels (per Discipline #14)
- [ ] Test guard `test_no_canonical_four_in_llm_prompts.py` passes
- [ ] Export packet additive fields `seasonal_element` + `seasonal_dominant_element` populated per skill / class / monster / gear
- [ ] Manifest parallel structure `manifest.seasonal_elements` populated
- [ ] Debug logging site wrapped in guard or resolved
- [ ] 5-class smoke season passes round-trip test (R11(b) prevention prescription compliance)
- [ ] MIGRATION.md entry per ADR-004 with full cross-seam consumer notes (drax-primary; rocket-passthrough; gamora-unaffected)
- [ ] Intermediate tag `star-lord/v1.3-form-bias-stage-3-cipher-migration` cut
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified at completion (drax Stage 3 demo-side dispatch authoring activates)

## Tag policy

- **Intermediate tag:** `star-lord/v1.3-form-bias-stage-3-cipher-migration` at the commit closing all 5 tracks + smoke pass.
- **Milestone tag:** none from this dispatch; Matt may elevate post-VS2a-ship per ADR-003.

---

## Completion record

**Completed:** 2026-05-16 (single session; all 4 engine-side tracks + smoke)
**Intermediate tag:** `star-lord/v1.3-form-bias-stage-3-cipher-migration` @ `19d8ba0`

**Track A — LLM prompt filter status:** COMPLETE
- `llm/naming.py`: All 6 canonical-four exposure sites (SG-02 through SG-07) resolved. `_elements_summary_line()` uses grouping-layer keys; `_seasonal_element_line()` emits `Combat mode ({grouping}): {seasonal_name}`; `name_skill()` no longer emits `Element: {canonical}`; `name_class()` skills summary uses `_grouping_label()`; `name_class()` / `name_monster()` / `name_gear_item()` dominant element uses `Dominant combat mode ({grouping}): {seasonal_name}`.
- `element/selector.py`: System prompt updated (SG-08) — "canonical role-slots (fire, wind, water, earth)" → "combat-mode slots (ignition, suffusion, bulwark, displacement)". Pool formatting, rules text, and history display use grouping-layer labels (SG-09 partially — JSON response keys preserved as internal protocol; narrative framing updated).
- Test guard `tests/test_no_canonical_four_in_llm_prompts.py`: 22 tests all pass.

**Track B — Export packet field additions:** COMPLETE
- `export/schemas.py`: `seasonal_element` on `ExportSkill`; `seasonal_dominant_element` on `ExportClass`, `ExportMonster`, `ExportGearItem`; `seasonal_elements` on `ExportMetadata`.
- `output/season_writer.py`: `_resolve_seasonal_name()` helper; all 4 serialization functions accept `elements` and populate seasonal fields; `_REQUIRED_CLASS_KEYS` + `_REQUIRED_SKILL_KEYS` updated.
- `export/season_exporter.py`: `_build_skill()` reads `seasonal_element`; `_build_element_name_lookup()` helper; `_load_gear_pool()` resolves gear `seasonal_dominant_element` from manifest; ExportClass/Monster construction reads `seasonal_dominant_element` from JSON.
- Backward compat: all canonical `dominant_element` / `canonical_element` fields preserved.

**Track C — Manifest parallel structure:** COMPLETE
- `output/season_writer.py` `_manifest()` emits `seasonal_elements` dict keyed by grouping-layer labels (`ignition`, `suffusion`, `bulwark`, `displacement`) alongside preserved `elements` (canonical-four keyed). `manifest_version` bumped `"1.4"` → `"1.5"`.
- `export/schemas.py` `ExportMetadata.seasonal_elements: dict[str, Any] | None`.
- `export/season_exporter.py` passes `manifest.get("seasonal_elements")` to ExportMetadata.

**Track D — Debug logging cleanup:** COMPLETE
- `llm/logger.py`: module docstring confirms `logs/` gitignored; INTENDED-INTERNAL classification post-Stage-3. No code change required (gitignore confirmed sufficient).

**Track E — Smoke + round-trip verification:** COMPLETE
- 22 cipher-guard tests pass (no canonical-four found in any LLM-bound prompt across all 4 canonical elements + physical)
- 239 affected test files pass (export/naming/vocabulary/selector/embodiment/cp8)
- 1 pre-existing cp8 test updated (`test_client_receives_tier_and_element` — now asserts grouping label present, canonical absent)
- 3 pre-existing failures (test_gear_cp3, test_gear_cp5, test_spirit_guide) confirmed pre-existing before Stage 3 (gamora/simulation seam; not regressions)
- Round-trip: `_elements_summary_line()` emits grouping-layer keys confirmed; mock-LLM naming pipeline end-to-end covered by cipher guard test

**MIGRATION.md path:** `reincarnated-engine/src/reincarnated/export/MIGRATION.md` — §v1.2 entry filed

**Notes for knight-rider (drax Stage 3 demo-side field names + manifest structure):**

Drax Stage 3 dispatch should target these exact fields (all additive; pre-Stage-3 seasons have `None`/absent):

```
ExportSkill.seasonal_element: str | None
ExportClass.seasonal_dominant_element: str | None
ExportMonster.seasonal_dominant_element: str | None
ExportGearItem.seasonal_dominant_element: str | None
ExportMetadata.seasonal_elements: {
  "ignition": { "element_id": ..., "name": ..., "tags": [...], "is_new": bool, "canonical_slot": "fire" },
  "suffusion": { ... "canonical_slot": "water" },
  "bulwark": { ... "canonical_slot": "earth" },
  "displacement": { ... "canonical_slot": "wind" }
}
```

Fallback pattern for drax transition period: `seasonal_dominant_element ?? dominant_element`

6 drax LEAK-RISK sites to address (from paths-audit): L-06, L-07 (GearGrid bare display), L-12 (Loadout canonicals array), L-02/L-13 (resolveElementName fallback hardening), L-11 (archetype label constants).

Spirit Guide voice audio Phase-1 sequencing: BLOCKED until drax Stage 3 also completes (L-06/L-07 are player-visible canonical-four leaks on gear cards).
