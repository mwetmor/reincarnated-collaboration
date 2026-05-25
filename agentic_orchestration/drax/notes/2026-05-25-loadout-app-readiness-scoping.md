# Loadout App Readiness Scoping — 2026-05-25

**Lead author:** drax (player-facing surface)
**Co-owner surface:** star-lord (data plumbing; cross-referenced via canonical/story/loadout-analytics-suite-information-architecture-2026-05-18.md § 4-5 + infrastructure recognition record)
**Date:** 2026-05-25
**Dispatch authority:** `agentic_orchestration/dispatches/2026-05-25-drax-and-star-lord-loadout-app-readiness-scoping.md`
**Status:** SCOPING MEMO — returns to Matt for scope-lock before any implementation fires

---

## 0. Purpose

This memo scopes what the loadout app (`reincarnated-loadout/`) needs to be ready for three near-term uses:

1. **T4-B post-mortem interface** — Matt + gandalf review engine-generated forms, compare algorithm T4 outputs, hand-author T4 alternatives for ~5-10 forms. This is the critical-path motivating driver: loadout app must be ready when algorithm § 8 output lands (~3-5 weeks from now).
2. **v1.0 player-facing form display** — the form a player sees when they start a season (weapon slot, off-hand slot, attributes, skill tree, archetype name).
3. **Ongoing analytics + story surface** — the existing `/analytics` page and `/the-work` suite (loadout-analytics IA already authored; star-lord data-manifest work partially scoped).

Each use has different readiness requirements. This memo scopes them separately.

---

## 1. Current loadout app state (what EXISTS)

### 1.1 Routes and pages (as of last AGENT_STATE entry 2026-05-18)

| Route | Component | Status |
|---|---|---|
| `/pitch` (labeled "Summary" in nav) | `Pitch.tsx` | LIVE — season hype surface, cosmological pair prose, hero portrait scaffolding |
| `/` | `Loadout.tsx` | LIVE — class selector, skill tree, gear grid (Yomi season, synthesized loadout) |
| `/sample` | `Sample.tsx` | LIVE — sample build selector across all seasons |
| `/analytics` | `Analytics.tsx` | LIVE — full analytics dashboard (10+ charts, SubstrateHeatmap, SeasonSummaryCards, ArchetypeStackedBar, ModifierRangeChart, SeasonTimelineChart, etc.) |
| `/encounters` | `Encounters.tsx` | LIVE — scatter plot encounter analytics (season_001005 + 002011-002015) |
| `/court` | `CourtBrowser.tsx` | LIVE — Court of Forms browser; shows empty state until rocket ships export_json() |

### 1.2 Data layer

- 11 seasons in `data/`: 5 historical (001001-001005) + 5 canonical-7 (002011-002015) + 1 Yomi (002328)
- `manifest.json` + `classes/class_NNNN.json` per season
- `data/encounter_analytics.json` + per-season variants
- `public/data/court.json` bootstrap (empty envelope)
- `data/vfx-manifest.json` v1.1 (VFX wiring for 7 substrates)

### 1.3 Current class data schema (relevant fields present)

The class JSON currently has:
- `name`, `flavor_text`, `title_completion`, `archetype_tag`
- `dominant_element`, `seasonal_dominant_element`
- `energy_type`, `role_orientation`, `range_profile`
- `stat_distribution` (STR/DEX/INT/WIS/VIT)
- `skills[]` with `canonical_element`, `seasonal_element`, `geometry_type`, `role`, `tier`, `chain_id`, `chain_position`
- `balance_metadata`
- `is_retired?`

### 1.4 What the current app does NOT have

- Any display of a weapon slot or off-hand item slot (gear grid exists for Yomi gear pool, but it is not "form weapon" — it is the generic loot pool)
- Mechanical profile display (range/geometry/tempo/amplitude BC axes surfaced to player)
- Attribute coupling display (which attribute the class/skills scale with — data exists in stat_distribution but no explicit attribute-coupling display per skill or weapon)
- Cohesion-judge archetypal name display (current `name` field IS the LLM-named form name; no "archetype" field distinct from `archetype_tag`)
- Skill tree with T4 alteration rendering (current skill tree renders tiers 1-4 but has no "regime-change/T4-alteration" display surface — `skill.tier` exists but T4 special_effect/alteration output not in current schema)
- Off-hand item slot (no `secondary_item` or equivalent field in current class JSON)
- `v1_scope` flag handling (substrate DB concept; not yet in class JSON)
- Stage 3.5 gap-fill provenance display
- Stage 4 mechanical-tagging fields in display layer

### 1.5 What the app DOES have that's load-bearing for T4 post-mortem

- Skill tree rendering per form (SkillTree.tsx) — FUNCTIONAL for current 4-tier structure
- Class selector across all seasons — FUNCTIONAL
- Stats display (stat_distribution surfaced in Loadout.tsx) — FUNCTIONAL
- Skill detail panel with flavor text — FUNCTIONAL

---

## 2. Data plumbing surface (star-lord cross-reference)

This section cross-references star-lord's existing scoping and flags gaps for follow-up star-lord invocation.

### 2.1 Current engine→loadout data flow

The current flow is MANUAL EXPORT + STATIC FILES:

```
Engine runs season generation (Python)
  → outputs season_NNNNNN/manifest.json + classes/class_NNNN.json
  → (manual) star-lord or drax copies to reincarnated-loadout/data/season_NNNNNN/
  → npm run build bundles new data
  → Vercel preview deploy or production deploy
```

No CI/CD pipeline exists. No live DB read from loadout. All data is static JSON bundled at build time.

### 2.2 What the loadout app needs from the engine for T4 post-mortem

The T4 post-mortem interface requires the engine to emit per-form output that includes the algorithm § 8 result. Per skill-system § 8.4, the algorithm output bundle includes:

```
alteration_type: string
alteration_specific: { source, target, rate, trade_off: {amplitude, tempo} }
manifestation: "T4_active_skill" | "rank2_passive" | "rank3_passive"
bind_axis: string
estimated_eta: float
thematic_anchor: string
llm_naming_template: string (Phase 5 fills)
```

This output does NOT currently exist in the class JSON schema. It is gated on algorithm § 8 implementation (rocket seam; ~1-2 weeks post-Cycle-10). When rocket ships the algorithm, star-lord's export pipeline must emit this bundle alongside the existing class JSON fields.

**Star-lord gap flagged:** schema extension required to include `t4_alteration_output` (or equivalent) in the class JSON. Field naming and schema to be agreed between rocket (producer) and star-lord (exporter) + drax (consumer). This is a pre-implementation coordination item for star-lord to scope separately.

### 2.3 v1_scope flag handling

The `v1_scope` flag is a substrate-DB-level concept (`weapon_knowledge_entries.v1_scope BOOLEAN`), not yet surfaced in the class JSON. Per the dispatch scope, the loadout app "must read v1_scope flag" — but for the T4 post-mortem use case, the relevant question is:

**Does the loadout app need to filter displayed classes by v1_scope?**

Answer: In the T4 post-mortem context, the engine generates forms FROM the v1_scope-flagged substrate. The loadout app consumes engine output (class JSONs) that already reflect v1_scope filtering at generation time. The loadout app does not need direct access to the substrate DB or the raw v1_scope flag — it only needs to display what the engine emitted.

The class JSON may optionally carry a `v1_scope` field as metadata (for display transparency), but this is v1.1+ territory. The display filter is already handled upstream at engine generation.

**Exception:** if the loadout app is expected to display both v1_scope and non-v1_scope forms (for T4 comparison work), then a `v1_scope_membership` flag on the class JSON would be useful. This is a question for star-lord + Matt to resolve at scope-lock.

### 2.4 Off-hand item schema integration

Per off-hand-items canonical doc, off-hand items are in `weapon_knowledge_entries` with `slot_eligibility` flag. In the class JSON, a form with an off-hand item would need a `secondary_item` field (or equivalent) carrying the off-hand item record.

This field does NOT currently exist in the class JSON. It is gated on:
1. Sidecar B substrate sourcing (elrond; ~1-2 days)
2. Architecture B Phase 2 generation pulling specific off-hand items from substrate
3. Star-lord export pipeline emitting `secondary_item` alongside existing class JSON structure

**Star-lord gap flagged:** `secondary_item` field addition to class JSON export schema. No implementation in current MIGRATION.md. This is a schema contract item to be coordinated between rocket (generator), star-lord (exporter), and drax (consumer).

### 2.5 Stage 3.5 gap-fill provenance transparency

Per dispatch requirement, the loadout app should surface `source_library = 'engine_authored_gap_fill_v1'` provenance. This would display to Matt/gandalf during T4 post-mortem as a flag: "this form's substrate is engine-authored, not crawled."

Implementation path: add optional `source_library` field to class JSON (star-lord export carries it when `weapon_knowledge_entries.source_library = 'engine_authored_gap_fill_v1'`). Loadout displays a small badge or flag when present.

**Not a blocking dependency for v1.0.** Can be added at T4 post-mortem time without disrupting other surfaces.

### 2.6 Stage 4 mechanical-tagging in display layer

Stage 4 adds `range/geometry/tempo/amplitude` mechanical-axis tags to weapon substrate rows. These are the BC axes the loadout app would surface as a "mechanical profile" display.

Current class JSON has `range_profile` (present) but NOT explicit `tempo` or `amplitude` fields from BC axes (skill structure carries geometry/tempo/amplitude implicitly via skill roles and effect_category, but there's no top-level form mechanical profile display).

**Star-lord gap flagged:** if v1.0 should surface BC mechanical profile, star-lord's export needs to include top-level `mechanical_profile: {range, geometry, tempo, amplitude}` field per form. Alternatively, drax can derive a summary display from the skill structure that already exists. The latter avoids a schema change but is less authoritative.

**Recommendation for Matt scope-lock:** at v1.0, derive mechanical profile summary from existing skill data (avoidance of schema change); expose explicit mechanical-tagging fields at v1.1+ when Stage 4 work lands and is stable.

### 2.7 Pi-Postgres / Vercel reachability (G4 cross-reference)

Per infrastructure recognition record § 6.1 and § 7 D4: the loadout app currently reads ALL data from static JSON bundled at build time. It does NOT connect to any database at runtime. This means the current architecture is ENTIRELY COMPATIBLE with Vercel deployment regardless of Pi-Postgres decisions.

If a future version of the loadout app connects to a live database (for real-time analytics, court browser, or T4 post-mortem session tracking), the G4 Vercel reachability constraint applies: the loadout DB would need to be either (a) hosted Postgres (Supabase/Neon) accessible via internet OR (b) Pi-Postgres with Tailscale-to-Vercel routing.

**Scope-lock recommendation:** v1.0 stays static-JSON; live-DB connection is v1.1+ territory gated on G4 resolution. This removes all infrastructure dependency from v1.0 implementation.

### 2.8 Cadence model recommendation

**Manual-export-to-static-JSON remains the right cadence for v1.0** because:
- Current engine is not running in production; seasons are generated per session
- All 11 existing seasons were already imported manually; pattern is established
- Adding CI/CD requires infrastructure decisions (Pi-Postgres or hosted) that are deferred per G1/G4
- T4 post-mortem is a bounded session, not a live-feed scenario

When the T4 post-mortem session fires, star-lord generates the forms, exports the class JSONs (with algorithm § 8 output fields included), drax bundles them into the app, and Matt/gandalf review via a preview deploy. No CI/CD needed for this workflow.

---

## 3. Player-facing surface (drax lead)

### 3.1 T4 post-mortem interface — what's needed

The T4 post-mortem use case is: Matt + gandalf review algorithm-generated T4 alterations for ~30-40 v1 forms; hand-author T4 alternatives for ~5-10 forms; compare.

For this use case, the loadout app needs to surface PER FORM:

1. **Form identity** — name (LLM-named), archetype, substrate element, cultural-tradition flavor text
2. **Main weapon display** — weapon name + tier + cultural-tradition + mechanical profile (range/geometry/tempo/amplitude summary)
3. **Off-hand item display** — item name + category (shield/tome/focus/horn/etc.) + mechanical function
4. **Attributes display** — STR/INT/WIS/DEX values (already in stat_distribution; just needs display surface)
5. **Skill tree display** — existing SkillTree.tsx is FUNCTIONAL; but needs T4 alteration node rendering:
   - Current: renders skill tier badge (T1/T2/T3/T4) from `skill.tier` field
   - Needed: render T4 alteration description when `t4_alteration_output` field is present; display `alteration_type`, `alteration_specific`, and `estimated_eta` in a readable format for Matt/gandalf review
6. **T4 comparison panel** — side-by-side or toggle view showing algorithm T4 output vs hand-authored alternative (for ~5-10 forms). This is NET-NEW UI.
7. **Provenance flag** — visual indicator when form substrate is `engine_authored_gap_fill_v1`

Current gap assessment for T4 post-mortem:

| Surface | Current state | Gap |
|---|---|---|
| Form identity | PRESENT (name, flavor_text, archetype_tag) | NONE |
| Main weapon display | ABSENT | NET-NEW: schema field + display component |
| Off-hand item display | ABSENT | NET-NEW: schema field + display component (gated on Sidecar B) |
| Attribute display | PARTIAL (stat_distribution shown; no explicit STR/INT/WIS/DEX coupling labels) | SMALL: add attribute coupling labels to stats display |
| Skill tree | PRESENT (SkillTree.tsx functional for tiers 1-4) | MEDIUM: add T4 alteration panel/node display when field present |
| T4 comparison panel | ABSENT | NET-NEW: the post-mortem authoring interface |
| Provenance flag | ABSENT | SMALL: badge when `source_library = 'engine_authored_gap_fill_v1'` |

### 3.2 v1.0 player-facing form display — what's needed

v1.0 player-facing form display is what a player sees at season start. Based on the dispatch scope and current app state:

**IN scope for v1.0 player-facing:**

1. **Form identity panel** — name, flavor_text, archetype (existing + improvements)
2. **Weapon slot display** — main weapon: name, tier badge, element, cultural flavor. Currently absent; needs schema field from engine export.
3. **Off-hand item slot display** — name, category, mechanical function. Currently absent; gated on Sidecar B substrate completion.
4. **Attribute display** — STR/INT/WIS/DEX with scaling-attribute indicators (e.g., "INT builds scale arcane skills"). Currently stat_distribution is shown as raw numbers; add coupling label.
5. **Skill tree** — EXISTING and functional. Enhancement for T4 alteration rendering when algorithm lands.
6. **Cohesion-judge archetypal name** — the `name` field IS the Phase 5 LLM-named form name. Currently displayed. No schema gap here; the display IS already the cohesion-judge output. The "cohesion-judge naming display" requested in dispatch § 2 is satisfied by the existing name field.
7. **Substrate/element display** — already in Loadout.tsx (seasonal_dominant_element, element badge). No new gap.

**Gap assessment for v1.0 player-facing:**

| Surface | Gap level | Notes |
|---|---|---|
| Main weapon display | MEDIUM | Net-new schema field required (star-lord export) + new WeaponSlot component |
| Off-hand slot display | MEDIUM | Net-new schema field + new OffHandSlot component; gated on Sidecar B completion |
| Attribute coupling labels | SMALL | Cosmetic improvement to existing stats display; no schema change needed |
| T4 alteration node rendering | MEDIUM | New rendering path in SkillTree.tsx when t4_alteration_output present; can degrade gracefully when absent |
| Skill tree quality | ALREADY ADEQUATE | SkillTree.tsx is functional; no blocking gap for v1.0 launch |

### 3.3 Skill tree surface note (algorithm § 8 gating)

The dispatch correctly identifies skill tree display as gated on algorithm § 8 implementation. However, SkillTree.tsx already renders the existing 4-tier structure correctly. The gating is specifically on T4 ALTERATION RENDERING — displaying the regime-change description that algorithm § 8 produces.

This means:
- v1.0 CAN ship with the existing skill tree rendering (before algorithm § 8 lands)
- Algorithm § 8 output requires a display update (T4 alteration panel) but does not require rebuilding the skill tree from scratch
- The T4 post-mortem interface builds ON TOP of the existing skill tree; it is an additive enhancement, not a replacement

### 3.4 Cohesion-judge naming display timing

Per dispatch § 5 open question: cohesion-judge naming is already present — the `name` and `flavor_text` fields on each class JSON ARE the Phase 5 LLM cohesion-judge output. These have been present since the earliest engine exports.

The question of "when do engine-authored archetypal names land in loadout app surface" has already been answered: they are THERE NOW in every season. The T4 post-mortem does not add a new naming surface; it adds an alteration display surface alongside the existing name.

### 3.5 Variant C multi-profile implications

Per dispatch § 2 and dispatch § 5 open question: the loadout app could become multi-profile (different game engine configurations) under Variant C. This is v1.1+ territory. The scoping implication for v1.0: do not architect the class selector, season picker, or weapon slot display in ways that hard-code Reincarnated-specific assumptions that cannot be parameterized later.

Specifically: the class selector is currently tied to `reincarnated-loadout/data/season_*/` paths. This is fine for v1.0. For Variant C compatibility, the data layer would need a profile/product-config abstraction. That is v1.1+ work, not now.

---

## 4. Cross-cutting

### 4.1 v1.0 MUST-HAVE list (explicit)

The following items are MUST-HAVE for the loadout app to serve the T4 post-mortem use case (the critical-path driver) AND provide v1.0 player-facing form display:

| # | Item | Surface | Gated on | Effort (drax) |
|---|---|---|---|---|
| M1 | Main weapon field in class JSON + WeaponSlot display component | Player-facing + T4 post-mortem | Star-lord export schema extension | ~1 day: new component + schema consumption |
| M2 | Off-hand item field in class JSON + OffHandSlot display component | Player-facing + T4 post-mortem | Sidecar B substrate completion + star-lord export schema extension | ~1 day: new component + schema consumption |
| M3 | T4 alteration output field in class JSON + rendering in SkillTree.tsx | T4 post-mortem (critical path) | Algorithm § 8 implementation (rocket) + star-lord export schema extension | ~1.5 days: T4 alteration panel in SkillTree + T4ComparisonPanel component |
| M4 | Attribute coupling labels in stats display | Player-facing | None (cosmetic; data already present) | ~0.25 day |
| M5 | Provenance flag display (`engine_authored_gap_fill_v1` badge) | T4 post-mortem | Star-lord schema extension (small) | ~0.25 day |
| M6 | T4 comparison panel for post-mortem authoring (~5-10 forms) | T4 post-mortem | M3 + algorithmic output in class JSON | ~1.5 days: panel UI + form-by-form comparison view |

**Total drax implementation effort: ~5.5 days** (assuming star-lord schema extensions land before drax implementation starts)

**Star-lord schema extension effort (estimate for star-lord to validate):**
- `t4_alteration_output` field addition to class JSON: ~0.5-1 day (schema + export pipeline update)
- `main_weapon` field addition to class JSON: ~0.5-1 day (schema + export pipeline update)
- `secondary_item` field addition to class JSON: ~0.5-1 day (schema + export pipeline update; gated on Sidecar B)
- `source_library` field pass-through: ~0.25 day
- Total star-lord estimate: ~1.75-3.25 days

**Engine effort (rocket):**
- Algorithm § 8 implementation: ~1-2 weeks (already scoped in gandalf request; parallel with W1.13/W1.20)

### 4.2 v1.1+ deferred list (explicit)

The following items are explicitly deferred to v1.1+:

| # | Item | Why deferred | Notes |
|---|---|---|---|
| D1 | `/the-work` analytics suite (6-arc narrative surface) | Already scoped in loadout-analytics IA; not blocking T4 post-mortem or player v1.0 launch | Fires when star-lord data-manifest work lands |
| D2 | Live DB connection (Pi-Postgres or hosted) | Gated on G1/G4 infrastructure decisions; static JSON is adequate for v1.0 | See Pi recognition record § 7 D4 |
| D3 | CI/CD pipeline for automated form exports | Gated on Pi-Postgres + Docker infrastructure decisions | Manual export workflow adequate for v1.0 |
| D4 | Variant C multi-profile loadout abstraction | Design-only at this stage; no production user base yet requiring multiple profiles | v1.1+ when Variant C commercial work fires |
| D5 | Explicit BC mechanical-profile surface (from Stage 4 tagging) | Stage 4 work not yet complete; can derive summary from existing skill data for v1.0 | Add explicit field when Stage 4 mechanical-tagging is stable |
| D6 | VIT attribute display (separate from STR/INT/WIS/DEX) | VIT deferred to v1.1+ per attribute-system canonical doc | Add when VIT added to engine |
| D7 | Spirit-guide explainer dialogue display | Requires templated dialogue authoring (gandalf; ~12-15 templates) + spirit-guide UX surface design | Post-T4-post-mortem territory |
| D8 | Faction-proxy spawn display | Gated on proxy-spawn-template in algorithm § 8.6 output | Post-algorithm implementation review |
| D9 | Sub-element flavor display surface | Gated on stable sub-element canonical doc (renamed 2026-05-24 from "element canonical-pair flavor") | Add when sub-element architecture doc lands |
| D10 | Perception-test metrics surface (D27) | Infrastructure under design; no measurements yet | See analytics IA § 4 P2-B |
| D11 | Named-bearer attribution visible display | Currently buried in flavor_text; may warrant explicit surface for T4 post-mortem | Consider for post-mortem UX pass |
| D12 | Cross-season cohesion metrics | Requires comparator pass across seasons | Analytics IA § 4 P2-D |
| D13 | Legendary canonical-pair set-bonus display | Set-bonus regime-change is post-Phase-5 loot architecture territory | Post-loot-architecture canonical doc |

### 4.3 Resource-bounds projection per surface area

**Drax effort:**

| Surface area | Scope | Effort |
|---|---|---|
| M1 (main weapon display) | 1 component + schema consumption | ~1 day |
| M2 (off-hand slot display) | 1 component + schema consumption | ~1 day |
| M3 (T4 alteration rendering) | SkillTree enhancement + new T4 panel | ~1.5 days |
| M4 (attribute coupling labels) | Cosmetic stats update | ~0.25 day |
| M5 (provenance flag) | Badge component + conditional render | ~0.25 day |
| M6 (T4 comparison panel) | Net-new panel UI | ~1.5 days |
| Integration smoke-test + deploy | Build + preview verification | ~0.5 day |
| **Total drax v1.0 MUST-HAVE** | | **~6 days** |

**Star-lord effort:**

| Surface area | Scope | Effort |
|---|---|---|
| `t4_alteration_output` schema + export | Schema extension + pipeline update | ~0.5-1 day |
| `main_weapon` field schema + export | Schema extension + pipeline update | ~0.5-1 day |
| `secondary_item` field schema + export | Schema extension + pipeline update (gated on Sidecar B) | ~0.5-1 day |
| `source_library` pass-through | Additive field | ~0.25 day |
| Test export of 1 sample form with all new fields | Smoke validation | ~0.25 day |
| **Total star-lord schema work** | | **~2-3.5 days** |

**Engine effort (rocket, already scoped):**

- Algorithm § 8 implementation: ~1-2 weeks (parallel with W1.13/W1.20)
- This is the primary timeline driver; loadout work cannot smoke-test M3/M6 until algorithm output exists

**Timeline estimate to T4 post-mortem readiness:**
- Algorithm § 8 implementation: ~1-2 weeks (rocket; critical path)
- Star-lord schema extensions: ~2-3.5 days (can run in parallel with algorithm implementation)
- Drax implementation: ~6 days (runs after schema extensions land; can start M1/M2/M4/M5 before M3/M6)
- **Wall-clock to T4 post-mortem readiness: ~3 weeks** (algorithm implementation dominates; loadout work fits inside that window)

### 4.4 Sequencing recommendation

```
Post-Cycle-10 parallel work (~1-2 weeks):
  ├─ rocket: algorithm § 8 implementation (critical path)
  ├─ star-lord: schema extensions (t4_alteration_output + main_weapon + secondary_item)
  │   [star-lord can start on t4_alteration_output schema spec + main_weapon immediately;
  │    secondary_item waits on Sidecar B substrate completion]
  └─ drax: M1 + M2 + M4 + M5 implementation (no dependency on algorithm)
     [M3 + M6 wait on algorithm output schema from star-lord]
       ↓
Algorithm output schema confirmed by star-lord (field name + structure locked)
       ↓
Drax implements M3 + M6 (T4 alteration rendering + comparison panel)
       ↓
Smoke test: npm run build clean + dev server renders Loadout route with new fields
       ↓
Star-lord exports sample set of ~5-10 forms with algorithm output included
       ↓
Drax bundles new season data + Vercel preview deploy
       ↓
Matt/gandalf T4 post-mortem session via preview deploy
       ↓
Matt approves → Vercel production deploy (per ADR-006)
```

### 4.5 Pi recognition record cross-references (G4)

Per infrastructure recognition record § 7 D4 + § 5 on Vercel reachability:

- G4 is: "drax + star-lord scope Vercel reachability constraint; produces yes/no on Tailscale-to-Vercel viability"
- Current assessment: **G4 is NOT BLOCKING for v1.0 loadout work.** The static-JSON architecture does not require any Pi-Postgres or live-DB connection. Vercel serves the bundled static assets with no runtime DB connectivity required.
- G4 becomes relevant if v1.1+ live-DB connection is pursued. At that point, the hosted-Postgres option (Supabase/Neon) is simpler for Vercel and avoids the Tailscale routing complexity entirely.
- **G4 resolution recommendation:** hosted-Postgres for the loadout DB (if live-DB ever needed); Pi-Postgres for engine-internal DBs (telemetry, catalogue). This splits the concerns cleanly and avoids Tailscale-to-Vercel complexity.

### 4.6 Variant C implications summary

Variant C (engine-as-general-product) implies:
- Multiple game products could each have their own loadout app consuming the same engine
- Or one loadout app with profile/product-config switching
- Current loadout app is hardwired to Reincarnated (class JSONs, season structure, element vocabulary, etc.)

v1.0 commitment: build the v1.0 features (M1-M6) cleanly (good component boundaries, typed interfaces, no magic strings for product-specific assumptions beyond what's necessary). This does not require v1.1+ abstractions NOW, but good component hygiene avoids Variant C lock-in.

Specific flags for implementation:
- `WeaponSlot.tsx` and `OffHandSlot.tsx` should take typed props from the class JSON rather than importing Reincarnated-specific constants internally
- The `v1_scope` filter (if ever surfaced) should be configurable, not hardcoded
- The `/the-work` analytics suite (v1.1+) is more Reincarnated-specific and that is fine; it is explicitly a "story of THIS engine" surface

---

## 5. Summary table: what fires when

| Work item | Seam owner | Status | Fires when |
|---|---|---|---|
| Algorithm § 8 implementation | rocket | Not started | Immediately post-Cycle-10; Discipline #18 consult first |
| star-lord schema extensions (t4 + weapon + off-hand) | star-lord | Not started | Immediately post-Cycle-10; parallel with algorithm |
| Drax M1+M2+M4+M5 (no algo dependency) | drax | Not started | After star-lord weapon + off-hand fields scoped |
| Drax M3+M6 (T4 rendering + comparison panel) | drax | Not started | After star-lord t4_alteration_output schema confirmed |
| T4 post-mortem preview deploy | drax | Not started | After all M1-M6 complete + sample forms exported |
| Matt/gandalf T4 post-mortem session | Matt + gandalf | Awaiting readiness | ~3 weeks post-Cycle-10 close |
| Production deploy | drax (with Matt approval per ADR-006) | Not started | After Matt T4 post-mortem session closes |

---

## 6. Open questions for Matt scope-lock

1. **v1_scope flag on class JSON** — should v1_scope be surfaced as metadata in the class JSON for transparency during T4 post-mortem, or is engine-generation-from-v1_scope-substrate sufficient? Drax recommendation: keep it internal; flag the provenance (gap-fill badge) but not the raw v1_scope boolean.

2. **T4 comparison panel format** — for ~5-10 forms where Matt hand-authors T4 alternatives: side-by-side display (algorithm output LEFT, hand-authored RIGHT) or toggle display (ALGORITHM / HAND-AUTHORED toggle)? Drax weak preference: toggle (cleaner on mobile). Matt's preference determines component design.

3. **Off-hand slot blocking vs non-blocking for T4 post-mortem** — Sidecar B substrate sourcing is not yet complete. If T4 post-mortem should include off-hand items, it must wait on Sidecar B + star-lord schema extension. If T4 post-mortem can proceed with main weapon only (and off-hand deferred to v1.0 production launch), it can fire earlier. Drax recommendation: T4 post-mortem proceeds with main weapon only; off-hand display added for v1.0 production.

4. **`/the-work` analytics suite (D1 in v1.1+ deferred list)** — per loadout-analytics IA 2026-05-18, this is a significant suite of 6 arcs. Is it still in scope for the post-T4-post-mortem implementation wave, or has it moved to a separate track? Drax notes it is well-specified and ready to implement once star-lord's data-manifest work lands.

5. **Vercel production deploy authorization pattern** — per ADR-006, Matt authorizes per production deploy. For T4 post-mortem, does Matt want to review via preview deploy only, or does he want a production deploy afterward? If preview-only for T4 post-mortem, that simplifies the flow (no ADR-006 trigger until after post-mortem closes).

---

## 7. Cross-references

- `agentic_orchestration/dispatches/2026-05-25-drax-and-star-lord-loadout-app-readiness-scoping.md` — dispatch authority
- `agentic_orchestration/gandalf/requests/2026-05-24-knight-rider-t4-reframing-and-loadout-readiness.md` — parent context + motivation
- `canonical/story/loadout-analytics-suite-information-architecture-2026-05-18.md` — v1.1+ analytics suite IA
- `canonical/story/skill-system-2026-05-24.md` § 8 — algorithm § 8 spec (T4 alteration output schema)
- `canonical/story/off-hand-items-2026-05-24.md` — off-hand item schema + categories
- `canonical/story/attribute-system-2026-05-24.md` — 4-attribute system (STR/INT/WIS/DEX)
- `canonical/story/weapon-substrate-composition-policy-v1-2026-05-24.md` — v1_scope + Sidecar B scope
- `canonical/story/infrastructure-raspberry-pi-postgres-and-closed-loop-pipeline-2026-05-25.md` § 7 D4, § 6.1 — G4 Vercel reachability; loadout DB location
- `reincarnated-loadout/AGENT_STATE.md` — current loadout app state (last updated 2026-05-18)

---

## 8. Sign-off

**Lead author:** drax (player-facing surface lead)
**Co-reference:** star-lord (data plumbing surface per canonical IA § 5 + infrastructure recognition record)
**Date:** 2026-05-25
**Status:** SCOPING MEMO — returns to Matt for scope-lock

**Matt-touch sequence:** Matt reads this memo → scope-locks v1.0 MUST-HAVE list (M1-M6 confirmed or amended) → knight-rider routes implementation dispatch(es) → implementation fires in parallel with algorithm § 8 work (rocket)

**Outstanding star-lord coordination items (flag for star-lord follow-up invocation):**
1. Schema extension spec for `t4_alteration_output` field (coordinate with rocket on field names)
2. Schema extension spec for `main_weapon` field (what fields from weapon_knowledge_entries to include)
3. Schema extension spec for `secondary_item` field (when Sidecar B lands)
4. G1 measurement (SQLite write-contention failure rate) — per infrastructure recognition record § 9 Step 1
5. G4 scoping (Vercel reachability) — hosted-Postgres recommendation per § 4.5 above; confirm or counter

---

**Signed:** drax
**For:** scoping memo covering data plumbing surface (star-lord cross-reference), player-facing surface (drax lead), v1.0 MUST-HAVE (M1-M6), v1.1+ deferred list (D1-D13), resource-bounds projection (~6 drax days + ~2-3.5 star-lord days + ~1-2 weeks rocket algorithm), Pi recognition record G4 cross-reference, and Variant C implications. Returns to Matt for scope-lock before any implementation fires.
