# Drax Pattern-A Response — Cycle 14 Tab Integration Verification

> **STATUS:** CURRENT — Pattern-A deep response to gandalf query `2026-05-27-drax-pattern-a-query-cycle-14-tab-integration.md`. Authored 2026-05-27.

**Author:** drax (loadout seam owner)
**Date:** 2026-05-27
**Authority:** gandalf Pattern-A query routed via KR; Matt Cycle 14 Cycle 14 Wave 5 data emission
**Required reading consumed:**
- `canonical/49-loadout-sample-player-surface-design-2026-05-27.md` — CONSUMED
- `agentic_orchestration/gandalf/notes/2026-05-27-no-classes-architectural-recommitment.md` — CONSUMED
- `agentic_orchestration/gandalf/notes/2026-05-27-path-iii-faction-assembly-extension.md` — CONSUMED
- Star-lord Seam 3 commits `bf7f659` + `94f8c88` — CONSUMED

---

## Discipline #42 framing-audit (applied at session-start)

**Q1 — Framing soundness:** Query is well-formed. Per-tab questions are concrete and verifiable against current code. No contradictions in the multi-question structure. Framing is sound.

**Q2 — Presupposition check:** One clarification on Q-Summary-6 ("Replace prior Canary season's data"). The current `/pitch` route is a hardcoded marketing page (`Pitch.tsx`) referencing seasons `002011`-`002015` and a `Canary of the Drowned Seam` hero. This is NOT a dynamically-fed season summary grouped by season or faction. The "Canary" appears as `className: 'Canary of the Drowned Seam'` in `pitchData.ts`. There is no Summary tab that currently renders live engine output in season-grouped or faction-grouped form. Q-Summary-6 asks whether replacement is "a config swap OR substantive integration work" — it is substantive new integration work, not a config swap, because the current route is a static pitch page.

**Q3 — Discipline #44 framing-refusal:** No refusal triggered. Query is executable.

---

## 1. Current state per tab

### 1.1 Summary tab (route: `/pitch`)

**Current implementation:** Static marketing Pitch page (`Pitch.tsx`). Hardcoded data in `src/data/pitch/pitchData.ts`:
- 5 seasons listed: `season_002011` through `season_002015` (5 canonical-4 historical seasons)
- Hero of the Engine: `Canary of the Drowned Seam` (hardcoded from `season_002013`)
- No dynamic engine data consumption — no `useSeasonData` hook, no faction schema wiring
- No season grouping OR faction grouping — flat static list of season hype pieces
- No ExportFactionCluster schema consumption whatsoever
- Character images: placeholder state with `portraitPath` fields populated for some; actual image rendering gated on star-lord portrait pipeline (Phase 2 per Pitch.tsx comment)

**Stat cards hardcoded:** `{ label: 'Classes', value: 55 }` — this is a Discipline #45 violation (player-facing "Classes" label) AND an accuracy problem (55 is stale; does not reflect current or Cycle 14 kit count).

**Seasonal hero selection:** H-5 hybrid mechanism (gandalf-recommend) does NOT exist. No engine emission selects seasonal hero. Hero is hardcoded in `pitchData.ts`. New work required.

**Canary season replacement:** The `v2_narrow_phase_5` data (35 Phase 5 forms; current engine output on the Loadout/Sample tabs) does NOT appear in the Pitch summary at all. The Pitch page is entirely disconnected from the `useSeasonData` hook. Replacement of Canary-season data with Cycle 14 first-new-engine-season data requires substantive integration work: new season-aware Summary component, dynamic data feed from `useSeasonData` or equivalent, faction-grouping architecture (currently absent).

**Q-Summary-1:** Grouping is neither-by-season-nor-by-faction — it is a static list. Faction grouping for Cycle 14 requires new architecture.
**Q-Summary-2:** ExportFactionCluster not consumed anywhere in loadout src. Zero wiring to `faction_label_canonical`, `cluster_compactness`, `cosine_similarity_max`, `diversity_flag`, `primary_pair_flag`, `gb_selection_rationale`, `pairwise_distance_distribution`.
**Q-Summary-3:** ExportFactionRelationship not yet emitted by engine (Wave 3 pending). Drax wiring effort = new architecture once schema lands.
**Q-Summary-4:** Seasonal hero mechanism = NOT PRESENT. New work.
**Q-Summary-5:** No character images rendered from engine output. `portraitPath` fields are `null` in most entries in `pitchData.ts`. Cycle 14 sidecar would require new image component + legolas-supplied paths + galadriel AI-tell pass. Not currently scaffolded.
**Q-Summary-6:** Canary season data replacement = substantive integration work, not config swap (see framing-audit above).

### 1.2 Loadout tab (route: `/`)

**Current implementation:** `Loadout.tsx` — fully functional interactive skill investment UI. Consumes `useSeasonData` hook which glob-discovers season manifest + class JSON files. Currently loads `v2_narrow_phase_5` as the "sample-season" (35 Phase 5 forms from engine production run).

**Doc 49 § 1.1 compliance per dimension:**

(a) Empty skill tree at startup: **PARTIAL.** `baselineAllocations()` initializes all skills to rank 1, not 0. This is not "empty" per doc 49 § 1.1 spec (all nodes uninvested). The loadout starts with 1 point in every skill, not a truly uninvested state. This is a gap vs doc 49.

(b) Per-node investment respecting prerequisites + chain depth + branching gates (D69): **NOT IMPLEMENTED.** `src/components/SkillTree/` renders skills as individual investment widgets without chain structure, depth tracking, or D69 branching gates. The engine's `chain_count` + `chains` structure from Path (1) Wave 1.5 Stage 3 Option α is not yet emitted (pre-Wave 3); current class JSON has flat `skills[]` arrays, not hierarchical chain structure. Gate: Wave 1.5 Stage 3 engine emission.

(c) ONE T4 capstone toggleable: **PARTIAL.** T4AlterationPanel exists and renders T4 data. The design-mode toggle exists. However, the T4 toggle is a design-mode inspection surface, not a player-facing "choose one of N capstones" mechanism per doc 49. There is no "select among N T4 candidates" UX. Gate: T4 candidate list emission from engine.

(d) Gear catalog filtered by kit fit: **PARTIAL.** Gear pool exists (`season_002328` gear pool via `useSeasonData`). Gear renders in `GearGrid` component. Filtering by `primary_stat + weapon_type_family` for Cycle 14 kit fit is not implemented — current filter is legacy per Yomi season. Wave 4 dependency for full T4-attuned gear pool.

(e) Live stat calculator per doc 47 § 4: **NOT IMPLEMENTED.** No `computeKitStats()` function or equivalent. No reference to doc 47 formulas in loadout source. Stats displayed are pass-through from engine emission (`balance_metadata` fields). Cycle 14 stat calculator requires new implementation.

(f) User per-kit-per-build theorycraft persistence: **PARTIAL.** `designMode` localStorage flag exists (`drax_design_mode`). No per-kit build-snapshot save/load mechanism. No `saved_builds[]` structure. This is new work.

**Reset capability (Q-Loadout-6):** "Reset" sets allocations back to `baselineAllocations()` (rank 1 per skill), not to zero state. This is not sandbox reset per doc 49.

**Season_metadata consumption:** NOT consumed. `skill_points_budget_endgame`, `gear_catalog_pool_id`, `stat_formula_version` fields do not exist in current data or hooks.

**Doc 49 §2.3 dual-derivation pattern:** NOT implemented. Current Loadout.tsx reads class JSON directly without `kit_committed_state` + `kit_shape` + `kit_metadata` layer. The doc 49 schema is a prospective target, not a current state.

### 1.3 Sample tab (route: `/sample`)

**Current implementation:** `Sample.tsx` — displays current season's class data in read-only inspection mode. Consumes `useSeasonData`. Has `designMode` toggle (read-only display enhancement, not editing).

**Doc 49 § 1.2 compliance per dimension:**

(a) Immutable read-only display of kit AS gauntlet-passed: **PARTIAL.** Read-only display exists and functions. BUT: the data currently shown is pre-Phase 7 engine output (no gauntlet verdict for Cycle 14; Phase 7 IMPL is `gamora eca0aa5` F-10 CLOSED but not yet run against cycle-14 production data). For the current `v2_narrow_phase_5` data, the "gauntlet-passed" status is placeholder (`phase7_gate_status: "placeholder"` per ExportFactionCluster default).

(b) Skill investment LOCKED at gauntlet-passed state: **NOT YET APPLICABLE.** No committed-investment schema from engine (Wave 1.5 Stage 3 Option α not yet emitted). Current skill display is flat skills with rank allocations. There is no `kit_committed_state.skill_investment` field in current data.

(c) Active T4 LOCKED per `active_t4_chain`: **NOT CONSUMED.** `active_t4_chain` field is not present in current class JSON schema. T4AlterationPanel renders T4 data from `t4_alteration_output` (the narration/strategy analysis), not a committed active-T4-chain field. New schema field required.

(d) Gear loadout LOCKED per specific gear instances: **NOT PRESENT.** Gear display exists for the Cycle 13 DB view (via `Cycle13SampleSection` — now retired from Sample.tsx per Track C REVISED Step 2). Current Sample.tsx shows `WeaponSlot` from `gear_representative.main_weapon` (present and rendering). Full gear loadout locked state requires Wave 4 gear instance emission.

(e) Statistics IMMUTABLE per gauntlet-time computation: **NOT IMPLEMENTED.** No `final_stats` field from engine committed state. Current stats shown are live `balance_metadata` values (modifier, win_rate_estimate, etc.), not gauntlet-time frozen stats.

**No editing enforcement:** Sample.tsx has no edit controls — read-only is structurally enforced by absence of investment widgets on this page. Q-Sample-3 answer: read-only enforcement is operational by construction, not by explicit guard.

**Faction composition in Sample tab (Q-Sample-4):** faction membership is NOT surfaced. No faction field in current class JSON. This is Summary-tab territory per doc 49 §4.3 composition table.

**Substrate_anchored_personage gate (D-Sharpened):** The `substrate_anchored_personages` field in ExportFactionCluster is not consumed anywhere in loadout. No risk of leakage since the field is not wired. If/when faction data is surfaced in drax tabs, this field MUST be gated to tooltip/metadata-only display, NOT player-facing label. Current state: field absent from consumer = gate intact by absence.

### 1.4 Analytics tab (route: `/analytics`)

**Current implementation:** `Analytics.tsx` + `useAnalytics.ts` + analytics components. Consumes all discovered seasons via `useSeasonData`. Shows aggregate stats, archetype distributions, modifier ranges, per-season summary cards, encounter analytics.

**Q-Analytics-1 star-lord telemetry consumption:**
- Cohort KPM band distribution: NOT present. No KPM band data in current analytics schema.
- Phase 7 verdict tracking: NOT present. `phase7_gate_status` not in analytics data model.
- G-B pairwise distance distribution: NOT present. `gb_selection_rationale` + `pairwise_distance_distribution` not consumed.
- Substrate-anchor distribution (D-Sharpened): NOT present. No substrate_anchored_personages in analytics.
- LLM call volume + cost tracking: NOT present. No SC-3/Phase III F-C cost tracking.

**Q-Analytics-2 F-C inter-faction analytics:** NOT wired. Relationship_type distribution, tension_narrative diversity, ai_tell_compliance_score tracking — all absent. Wave 3 dependency.

**Q-Analytics-3 gandalf design-quality audit verdicts:** NOT surfaced. No PASS/PASS-with-design-concerns/DRIFT-DETECTED verdict display. This is a new capability requiring both engine emission and drax surfacing.

**Vocabulary violation in Analytics:** `StatBadge label="Classes"` at line 30 of Analytics.tsx is a player-facing "Classes" label. Discipline #45 violation. Should be "Kits" or "Forms" per no-classes vocabulary.

### 1.5 Encounters tab (route: `/encounters`)

**Current implementation:** `Encounters.tsx` — scatter plot visualization of class performance vs encounter slots. Consumes `encounter_analytics_*.json` files from `public/data/`.

**Q-Encounters-1 encounter set:** Displays Cycle 13 reference encounters (`encounter_analytics_*.json` files). Multiple files present: `002011`, `002012`, `002013`, `002014`, `002015`, `002328` plus `encounter_analytics.json`. No Cycle 14 encounter analytics file exists yet (Phase 7 IMPL not yet run against Cycle 14 data).

**Q-Encounters-2 per-encounter-difficulty + Phase 7 verdict:** NOT present. Phase 7 verdict per (kit × encounter) tuple does not exist in current `encounter_analytics_*.json` schema. This gates on Phase 7 IMPL close (gamora bridge `eca0aa5` is IMPL-ready but not yet run against Cycle 14 production season).

**Q-Encounters-3 spatial vs scalar:** Current Encounters tab consumes scalar gauntlet output only (encounter_analytics JSON from `gauntlet_sim.py`). No spatial gauntlet hooks. Spatial gauntlet remains R2 research per gamora Pattern-A finding.

**Vocabulary violations in Encounters tab (Discipline #45):**
- Line 454 player-facing button label: `"Per-class"` — should be `"Per-kit"` or `"Per-form"`
- Line 469: `"Each card = one class · points show..."` — "class" visible to player in this label
- Line 470: `"...all ${analytics.class_ids.length} classes' performance..."` — "classes" visible to player
- Line 483 comment: `{/* Per-class view */}` — comment only, not player-facing
- Line 355 comment: `"class efficiency"` — comment only

**Non-exempt player-facing vocabulary violations in Encounters:** lines 454, 469, 470. These need redaction per Discipline #45 + no-classes recommitment.

### 1.6 Court tab (route: `/court`)

**Current implementation:** `CourtBrowser.tsx` — full filter + sort + search browser for Court of Forms. Consumes `public/data/court.json` via `useCourtData` hook.

**Q-Court-1 current population:** `court.json` = `{ "schema_version": "1.0", "forms": [] }` — empty array. Court tab renders empty state for first-time players. No data.

**Q-Court-2 Cycle 14 v1 scope:** Confirmed minimal single-season view is appropriate. Full Court mechanics (cross-season Spirit accumulation, ascension records, archetype-shape lineage tracking) are Cycle 15+ per `project_earth_meta_layer` memory and per doc 49 § 1.2 "Canonical reference: Sample is the 'official' character for this season; Court of Forms accumulates ascended Spirits in this state (Cycle 15+ Court mechanics)."

**Q-Court-3 canonical_archetype_register:** NOT consumed by drax. The CourtBrowser consumes `CourtForm` type which is a drax-side type, not engine's `canonical_archetype_register` schema. Court data population requires engine emission of canonical_archetype_register at Math Note 5 E2 first-emergence (Wave 5 commit). Currently: no such emission exists for Cycle 14.

**Vocabulary in Court tab:** `CourtBrowser.tsx` line 372: `{/* Season + archetype row */}` — comment only. `COURT_ROLE_LABEL` constant exists in `courtTypes.ts` — uses "role" vocabulary in display labels. This is on the court card display. Lower priority but worth auditing.

### 1.7 Cross-tab findings

**Q-Cross-1 Vocabulary lock compliance (Discipline #45) — complete inventory of player-facing violations:**

| File | Location | Violation | Severity |
|---|---|---|---|
| `Analytics.tsx:30` | `StatBadge label="Classes"` | "Classes" player-facing label | HIGH — visible on landing |
| `Encounters.tsx:454` | Button label `"Per-class"` | "class" in interactive control | HIGH — interactive UI |
| `Encounters.tsx:469` | Description string | "one class · points show" | HIGH — visible description |
| `Encounters.tsx:470` | Description string | "all ${n} classes' performance" | HIGH — visible description |
| `Pitch.tsx:22` | Stat card `label: 'Classes'` | "Classes" player-facing stat card | HIGH — landing stat |
| `Pitch.tsx:83` | Prose text | "class names" | MEDIUM — marketing prose |
| `Pitch.tsx:110` | Prose text | "class names" | MEDIUM — marketing prose |

The `Pitch.tsx` prose references (lines 83, 110) are in marketing copy that explains the engine generates "class names." These describe the OLD architecture. They should eventually be updated but are lower urgency than interactive UI labels.

**Q-Cross-2 Token cost — drax LLM call volume:** ZERO. Drax makes no LLM calls. All LLM-generated content is consumed as pre-baked text from engine emission (faction_label_canonical, faction_identity_narrative, T4 narration fields). Correct.

**Q-Cross-3 Star-lord Track C transform consumption:** Drax currently does NOT consume a Track C transformed output. Drax consumes class JSON files directly from `data/` season folders (via Vite glob in `useSeasonData.ts`). The doc 49 §2.3 schema (`kit_shape` / `kit_committed_state` / `kit_metadata` / `season_metadata`) does not exist in current class JSON. Track C transform has not yet produced a Cycle 14 drax-consumable output.

---

## 2. Implementation gaps per dimension

### 2.1 Engine schema consumption gaps

| Schema / Field | Tab | Gap |
|---|---|---|
| ExportFactionCluster (21 fields) | All tabs | Zero consumption. No faction_label_canonical, cluster_compactness, cosine_similarity_max, diversity_flag, primary_pair_flag, gb_selection_rationale, pairwise_distance_distribution. |
| ExportFactionRelationship (Wave 3 pending) | Summary | Not emitted yet; drax wiring architecture does not exist |
| kit_committed_state schema (doc 49 §2.3) | Loadout / Sample | Not emitted yet; no Track C transform exists for Cycle 14; current schema is flat class JSON |
| season_metadata (skill_points_budget, gear_catalog_pool_id, stat_formula_version) | Loadout | Not emitted; not in manifest schema |
| active_t4_chain field | Sample | Not emitted; T4AlterationPanel renders narration data, not committed-T4-chain state |
| Phase 7 verdict per kit (phase7_gate_status canonical) | Sample / Encounters / Analytics | Placeholder only; Phase 7 IMPL not run against Cycle 14 production data |
| canonical_archetype_register | Court | Not emitted for Cycle 14; Math Note 5 E2 first-emergence at Wave 5 |
| substrate_anchored_personages | (gated) | Not consumed — gate intact by absence. Must remain gated when faction data lands |

### 2.2 Doc 49 compliance gaps

| Doc 49 spec | Current state | Gap |
|---|---|---|
| §1.1(a) Empty skill tree at startup | Initializes to rank 1 per skill | Gap: "empty" state not yet defined; baseline is rank 1, not 0 |
| §1.1(b) Per-node prerequisites + chain depth + D69 branching | Flat skill list; no chain structure | Gate: Wave 1.5 Stage 3 Option α emission |
| §1.1(c) ONE T4 capstone toggleable | Design-mode inspection only | Gap: player-facing T4 selection UX not built |
| §1.1(d) Gear catalog filtered by kit fit | Legacy Yomi gear pool | Gap: Wave 4 dependency; no primary_stat + weapon_type_family filter |
| §1.1(e) Live stat calculator (doc 47 §4) | Not implemented | Gap: computeKitStats() absent; doc 47 formulas not referenced |
| §1.1(f) User theorycraft persistence | designMode flag only | Gap: no per-kit build snapshot save/load |
| §1.2(b) Skill investment LOCKED at gauntlet state | Flat skills; no committed-investment field | Gate: engine emission |
| §1.2(c) active_t4_chain LOCKED | Not emitted | Gate: engine emission |
| §1.2(d) Gear loadout LOCKED | main_weapon only; no full loadout | Gate: Wave 4 |
| §1.2(e) Statistics IMMUTABLE | balance_metadata; not frozen gauntlet stats | Gate: engine emission |
| §2.3 Dual-derivation pattern | Not implemented | Gate: Track C transform + new drax hooks |

### 2.3 Vocabulary lock (Discipline #45) compliance gaps

Player-facing violations confirmed (see §1.7 above). Priority redaction list:

1. `Analytics.tsx:30` — `label="Classes"` → `label="Kits"` (one line)
2. `Encounters.tsx:454` — button `"Per-class"` → `"Per-kit"` (one line)
3. `Encounters.tsx:469` — description string `"one class · points show..."` → `"one kit · points show..."` (one line)
4. `Encounters.tsx:470` — description string `"all ${n} classes' performance"` → `"all ${n} kits' performance"` (one line)
5. `Pitch.tsx:22` — stat card `label: 'Classes'` → `label: 'Kits'` (one line)

Pitch.tsx prose (lines 83, 110) reference "class names" in historical marketing copy describing old engine behavior. These are deferred to a broader Pitch.tsx rewrite when Cycle 14 data lands.

### 2.4 Wave 4 dependency gaps

Both Loadout and Sample tabs gate on Wave 4 (T4-attuned gear + D21 acquisition curve) per doc 49 §5:
- Loadout gear catalog: requires Wave 4 per-season gear pool emission
- Sample gear display: `main_weapon` only currently; full gear loadout locked display requires Wave 4 specific gear instances
- Gear slot filtering by T4-attunement: Wave 4 dependency

---

## 3. Effort estimates per gap

### 3.1 Vocabulary lock redactions (Discipline #45) — LOW effort

5 targeted string changes across 3 files. ~30 minutes. Can fire as standalone dispatch or bundled with first Cycle 14 drax integration dispatch. No schema dependency. Should fire now.

### 3.2 Pitch/Summary tab — Cycle 14 faction-grouped re-architecture — HIGH effort

Replacing the static Pitch page with a dynamically-fed faction-grouped Summary requires:
- New data model: faction-grouped display architecture (ExportFactionCluster consumption)
- New hooks: consume faction_clusters.json per season via Track C transform
- New components: faction card, inter-faction relationship panel (F-C), primary-pair indicator
- Seasonal hero selection: H-5 hybrid mechanism requires engine emission OR manual curation
- Character images: legolas portrait pipeline (Phase 6 deferred Cycle 15+ OR lighter G-2 sidecar)

Estimate: 1-2 weeks drax work. Gates on:
- Wave 3 close (ExportFactionRelationship)
- Track C transform producing faction_clusters.json per season

### 3.3 Loadout tab doc 49 compliance — HIGH effort (phased)

Phase A (can start now, no engine gate):
- Fix empty-state initialization (rank 0 vs rank 1): LOW — 1 day
- Fix reset to true zero state: LOW — 0.5 days
- Build per-kit build snapshot save/load (localStorage): MEDIUM — 2-3 days

Phase B (gates on engine):
- Chain structure rendering per Wave 1.5 Stage 3 Option α: MEDIUM — 1 week
- T4 candidate selection UX (one-of-N toggle): MEDIUM — 3-4 days (after engine emits T4 candidate list)
- Gear catalog filter by kit fit: MEDIUM — 2-3 days (after Wave 4)

Phase C (gates on doc 47 + engine):
- Live stat calculator (computeKitStats per doc 47 §4): HIGH — 1-2 weeks (requires doc 47 formula implementation + test harness + engine reference computation for Discipline #11 validation)

### 3.4 Sample tab doc 49 compliance — MEDIUM effort (mostly engine-gated)

- Read-only enforcement already operational (no editing controls present)
- active_t4_chain display: LOW once engine emits field (1-2 hours)
- Skill investment locked display: MEDIUM once kit_committed_state emitted (2-3 days)
- Full gear loadout display: MEDIUM once Wave 4 emits per-kit instances (2-3 days)
- Statistics immutable display: LOW once final_stats emitted (1 day)

Net drax effort for Sample: mostly waiting on engine emission. Pre-wire hooks and types: MEDIUM — 2-3 days.

### 3.5 Analytics tab Cycle 14 schema wiring — MEDIUM effort

- KPM band distribution display: MEDIUM — requires star-lord telemetry schema change + new analytics component (2-3 days)
- Phase 7 verdict tracking: MEDIUM — requires phase7_gate_status in analytics feed (1-2 days)
- G-B pairwise distance display: LOW-MEDIUM — scatter/histogram component once data emitted (1-2 days)
- F-C analytics (relationship_type distribution): MEDIUM — Wave 3 dependency (1-2 days once data lands)
- gandalf design-quality audit verdicts: MEDIUM-HIGH — requires new data feed + display architecture (3-4 days)

### 3.6 Encounters tab Phase 7 IMPL wiring — MEDIUM effort (engine-gated)

- Per-encounter difficulty + Phase 7 verdict: MEDIUM — gates on Phase 7 IMPL producing encounter sweep output; drax consumption once schema lands (2-3 days)
- Encounter_analytics.json for Cycle 14: LOW — once gamora bridge runs against Cycle 14 season, new encounter_analytics file drops in. Existing Encounters.tsx picks it up via existing hooks if schema matches.

### 3.7 Court tab canonical_archetype_register — LOW effort (engine-gated)

CourtBrowser infrastructure exists. court.json empty. Wiring canonical_archetype_register to court.json format: LOW — 1-2 days once engine emits (Track C transform + format alignment).

### 3.8 Summary of net Cycle 14 effort estimates

| Workstream | Effort | Engine gate | Dispatch needed |
|---|---|---|---|
| Vocabulary lock redactions (#45) | 0.5 days | NONE | Yes (small) |
| Summary/Pitch tab faction-grouped re-architecture | 1-2 weeks | Wave 3 + Track C | Yes (large) |
| Loadout Phase A (empty state + reset + persistence) | 1 week | NONE | Yes (medium) |
| Loadout Phase B (chain structure + T4 toggle + gear filter) | 1-1.5 weeks | Wave 1.5 Stage 3 + Wave 4 | Yes (medium) |
| Loadout Phase C (stat calculator) | 1-2 weeks | doc 47 publication to drax | Yes (large) |
| Sample tab pre-wire hooks + types | 3 days | NONE | Bundled with Loadout B |
| Analytics Cycle 14 schema wiring | 1 week | Phase 7 IMPL + Wave 3 | Yes (medium) |
| Encounters Phase 7 verdict wiring | 2-3 days | Phase 7 IMPL | Bundled with Analytics |
| Court canonical_archetype_register | 1-2 days | Wave 5 (Math Note 5 E2) | Bundled with Loadout B |

**Net timeline estimate for full Cycle 14 drax integration:** ~5-7 weeks total drax sub-agent work, with several parallel-runnable threads and multiple engine-gated threads. Given Wave 3, Wave 4, Phase 7 IMPL, and Wave 5 are upstream dependencies, the realistic "fully-integrated" end state aligns with Wave 5 production season commit.

**Minimal integration (Summary + Loadout + Sample core; defer Analytics + Encounters + Court polish):** ~2-3 weeks.

---

## 4. Routing recommendations

### 4.1 Immediate — no engine gate

**Dispatch A — Vocabulary lock (Discipline #45) redaction:**
- Files: `Analytics.tsx`, `Encounters.tsx`, `Pitch.tsx`
- Scope: 5 targeted string changes (lines identified in §1.7)
- Effort: 0.5 days
- Priority: FIRE NOW — violations are present in production at `reincarnated-loadout.vercel.app`
- Note: Pitch.tsx prose lines 83/110 deferred to Pitch re-architecture dispatch

**Dispatch B — Loadout Phase A (empty state + reset + build persistence):**
- Files: `Loadout.tsx`, new localStorage build-snapshot module
- Scope: fix rank-0 initialization, true reset to zero state, per-kit build save/load
- Effort: 1 week
- No engine dependency. Can fire immediately after Dispatch A.

### 4.2 Engine-gated dispatches (fire when upstream dependency lands)

**Dispatch C — Summary tab faction-grouped re-architecture:**
- Gate: Wave 3 close (ExportFactionRelationship) + Track C transform (faction_clusters.json per Cycle 14 season)
- Scope: new faction-grouped Summary architecture replacing static Pitch page; ExportFactionCluster consumption; primary-pair indicator; inter-faction relationship panel; seasonal hero selection mechanism
- Effort: 1-2 weeks
- Pattern-B trigger: seasonal hero selection mechanism (H-5 hybrid per gandalf recommend) — if engine won't emit a top-3 seasonal hero shortlist, a Matt design call is needed on whether curation is acceptable at this stage

**Dispatch D — Loadout Phase B + Sample pre-wire (chain structure + T4 toggle + gear filter):**
- Gate: Wave 1.5 Stage 3 Option α emission (chain structure) + Wave 4 (gear pool)
- Scope: chain-aware skill investment UI, T4 candidate selection toggle, gear catalog filter by kit fit, Sample committed-state display
- Effort: 1.5-2 weeks
- Bundled: Court canonical_archetype_register wiring

**Dispatch E — Loadout Phase C (stat calculator per doc 47 §4):**
- Gate: doc 47 §4 published to drax-accessible form (currently canonical but not wired to drax; no Track C season_metadata yet)
- Scope: computeKitStats() pure function, live stat update on investment/gear/T4 change, Discipline #11 validation against engine reference computations
- Effort: 1-2 weeks
- This is the highest-complexity single drax deliverable in Cycle 14

**Dispatch F — Analytics + Encounters Cycle 14 wiring:**
- Gate: Phase 7 IMPL close (gamora bridge run against Cycle 14 production season) + Wave 3 (F-C analytics)
- Scope: KPM band display, Phase 7 verdict tracking, G-B pairwise distance chart, F-C relationship_type distribution, per-encounter Phase 7 verdict in Encounters tab
- Effort: 1 week

### 4.3 Pattern-B engagement triggers (Matt design calls)

One item surfaces a potential Matt design call:

**Seasonal hero selection mechanism (Q-Summary-4):** H-5 hybrid (substrate-led top-3 + gandalf curation) is gandalf's recommendation but requires either:
- Engine emission of a top-3 shortlist (new engine schema field), OR
- A committed curation step (gandalf selects from top-3 per season), OR
- Matt signs off that curation-only is acceptable for Cycle 14 v1

Recommend: KR surfaces this to Matt as a scoping question before Dispatch C fires. Low urgency now (Dispatch C gates on Wave 3 anyway), but the answer affects the Dispatch C scope.

---

## 5. Open questions requiring Matt design call

**Q-Open-1: Seasonal hero selection mechanism for Summary tab.** Engine-emitted shortlist vs gandalf curation vs Matt curation — who selects the seasonal hero per season, and how? Dispatch C scope depends on this answer.

**Q-Open-2: Summary tab identity.** The current `/pitch` route is a marketing page (investor/collaborator-facing). The faction-grouped Season Summary Matt requested for Cycle 14 is a player-facing analytical surface. Should these be two routes (keep `/pitch` as marketing, add `/summary` as the faction-grouped view), or replace `/pitch` entirely? Affects dispatch scope and routing architecture.

**Q-Open-3: Loadout empty-state initialization.** Doc 49 §1.1(a) specifies "all nodes uninvested" (rank 0). Current implementation initializes to rank 1 per skill (minimum investment). Is the design intent truly rank-0 start (player invests every point from scratch), or does rank-1 initialization represent the minimum viable state a character must have? The doc 49 spec is clear (rank 0) but the current behavior may reflect an intentional minimum-viable-investment floor. Clarify before Dispatch B fires.

---

## 6. D-Sharpened invariance gate verification

Per task brief requirement: confirm substrate_anchored_personage gating in loadout summary code.

**Verdict: Gate intact by absence.** `substrate_anchored_personages` field from ExportFactionCluster is not consumed anywhere in `/Users/admin/Games/reincarnated-loadout/src/`. Grep confirms zero references. There is no faction data consumption of any kind in the current loadout app — therefore no leakage risk at present.

**When faction data lands (Dispatch C):** the substrate_anchored_personages field MUST be routed to tooltip/metadata-only display per gandalf Wave 3 Seam 1 §5.5 + §6.8 + §10.2. A `// TODO(drax): D-Sharpened gate — substrate_anchored_personages is metadata only; NEVER player-facing label` annotation must be added at the point of consumption. This will be enforced in Dispatch C scope.

**Gate-2 grep audit pattern** (for Dispatch C acceptance criteria): `grep -rn "substrate_anchored_personage" src/` must return ONLY tooltip/metadata consumption paths — no label renders, no heading renders, no player-facing string interpolation.

---

## Completion record

**Authored:** 2026-05-27
**Author:** drax (loadout seam owner)
**Pattern:** A-deep file output (multi-question structure warranted)
**Output path:** `agentic_orchestration/drax/notes/2026-05-27-cycle-14-tab-integration-pattern-a-response.md`
**Follow-on dispatches identified:** A (vocab lock — IMMEDIATE), B (Loadout Phase A — IMMEDIATE), C (Summary re-architecture — Wave 3 gated), D (Loadout Phase B + Sample — Wave 4 gated), E (stat calculator — doc 47 gated), F (Analytics + Encounters — Phase 7 IMPL gated)
**Pattern-B triggers:** Q-Open-1 (seasonal hero selection), Q-Open-2 (Summary tab identity), Q-Open-3 (Loadout empty-state spec)
**Commit:** pending per CLAUDE.md auto-commit pattern
