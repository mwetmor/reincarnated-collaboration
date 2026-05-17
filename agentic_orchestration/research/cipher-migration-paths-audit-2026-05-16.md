# Cipher Migration Paths-Audit — Canonical-Four Label Emission Inventory

**Authored:** 2026-05-16 by star-lord
**Dispatch source:** `agentic_orchestration/dispatches/2026-05-16-star-lord-cipher-migration-paths-audit.md` Track A
**Commissioned by:** P6 forward audit CRITICAL recommendation §VS2b S3 (`canonical/story/p6-forward-audit-2026-05-16.md`)
**Primary downstream consumer:** gandalf — form-bias Stage 3 dispatch authoring
**Baseline inventory reference:** `canonical/story/pre-llm-substrate-inventory.md` Cluster E (LLM-drift inventory)

---

## Section 1 — Audit Methodology

### Search strategy

The audit searched for canonical-four label emissions across six surface classes by:

1. Grepping engine source (`src/reincarnated/`) for literal strings `"fire"`, `"water"`, `"earth"`, `"wind"`, and field names `canonical_element`, `dominant_element`, `role_slot`, `fire_slot`, `wind_slot`, `water_slot`, `earth_slot`.
2. Reading every file with hits to classify the emission in context.
3. Separately grepping both consumer repos (`reincarnated-loadout/src/`, `reincarnated-demo/src/`) for the same patterns.
4. Examining Spirit Guide (`spirit_guide/spirit_guide.py`) specifically for prompt templates and LLM calls.
5. Examining the LLM call logger (`llm/logger.py`) to determine whether prompt text is persisted to disk.

### What counts as a canonical-four label emission

Any code path that:
- Includes the string `"fire"`, `"water"`, `"earth"`, or `"wind"` in the context of the element system (not incidental string matches)
- Includes `canonical_element`, `dominant_element`, or `role_slot` field references that carry canonical-four values
- Emits these labels into a surface visible to the player, stored in a player-accessible artifact, sent to the LLM, logged for debugging, or persisted in telemetry

### 6 surface classes (per P6 forward audit recommendation)

1. **Telemetry events** — engine-side recorder + emission paths into `telemetry.db`
2. **Export packet fields** — engine to external consumer JSON payloads (`exports/`)
3. **Spirit Guide prompt templates** — LLM-bound text (prompt construction)
4. **Spirit Guide voice output** — LLM response handling and display
5. **Loadout app data display** — drax-side rendering (`reincarnated-loadout/`)
6. **Debug logging** — Python `logging`, `print`, `console.log`, LLM call log files

### Classification rubric (4-tier)

| Classification | Meaning |
|---|---|
| **INTENDED-INTERNAL** | Emits canonical-four on an internal-only path; no player or public-facing exposure; correct behavior for Stage 3 |
| **INTENDED-PUBLIC-AS-CIPHER** | Already designed to surface per-season vocabulary to the player; resolves canonical-four to seasonal name before display |
| **LEAK-RISK** | Emits canonical-four label on a public-facing path that bypasses any per-season vocabulary resolution |
| **TO-BE-FILTERED** | Known LEAK-RISK with a planned filter at Stage 3 implementation; subset of LEAK-RISK already in Stage 3 plan |

---

## Section 2 — Per-Site Enumeration

### Surface Class 1: Telemetry Events (engine-side recorder)

| # | File + Line(s) | Code context | Classification | Notes |
|---|---|---|---|---|
| T-01 | `telemetry/recorder.py:116` | `for slot in ("fire", "wind", "water", "earth"):` in `record_seasonal_elements()` | **INTENDED-INTERNAL** | Writes `role_slot` column values to `seasonal_elements` table. Internal DB. Never player-facing. |
| T-02 | `telemetry/recorder.py:674` | `archetype, canonical_element` in `_insert_classes()` INSERT | **INTENDED-INTERNAL** | Writes `canonical_element` to `classes` table. Internal DB. Never player-facing. |
| T-03 | `telemetry/recorder.py:699` | `seasonal_name_by_element.get(pc.dominant_element)` | **INTENDED-INTERNAL** | `seasonal_element_name` column in `classes` stores the per-season NAME (not the canonical). The lookup resolves canonical_element to element_name before persisting. Correctly separated at the telemetry layer. |
| T-04 | `telemetry/recorder.py:711` | `archetype, canonical_element` in `_insert_monsters()` INSERT | **INTENDED-INTERNAL** | Writes `canonical_element` to `monsters` table. Internal DB. |
| T-05 | `telemetry/recorder.py:744` | `trial.dominant_element` in `_insert_trial()` | **INTENDED-INTERNAL** | Writes `canonical_element` to `trials` table. Internal DB. |
| T-06 | `telemetry/recorder.py:799` | `skill.canonical_element` in `_insert_skill()` INSERT | **INTENDED-INTERNAL** | Writes `canonical_element` to `abilities` table. Internal DB. |
| T-07 | `telemetry/migrations.py:297` | `role_slot TEXT NOT NULL -- 'fire', 'wind', 'water', 'earth'` | **INTENDED-INTERNAL** | Schema definition. The `seasonal_elements` table's `role_slot` column stores canonical-four slot identifiers as the lookup key. Internal. |

**Surface class 1 summary:** 7 sites; all INTENDED-INTERNAL. The telemetry DB is not player-facing and never surfaces to any consumer without the engine or a developer-tool query. Note: `seasonal_element_name` (T-03) correctly stores the per-season name, not the canonical label — this is the correctly-built separation that Stage 3 should propagate to other surfaces.

---

### Surface Class 2: Export Packet Fields

| # | File + Line(s) | Code context | Classification | Notes |
|---|---|---|---|---|
| E-01 | `export/schemas.py:16` | `canonical_element: str` field on `ExportSkill` | **LEAK-RISK** | `canonical_element` is a first-class field on the ExportSkill schema. It is written directly to `exports/season_XXXXXX/classes.json` and consumed by drax. Players can inspect the export packet in browser dev tools or via the loadout app's data layer. Stage 3 must either rename this field or filter it. |
| E-02 | `export/season_exporter.py:294` | `canonical_element=skill_json.get("canonical_element", "")` | **LEAK-RISK** | Exporter reads `canonical_element` from the seasons/ JSON and writes to `ExportSkill`. Same leak path as E-01 — the exporter is the pipe that carries the label to the consumer-facing artifact. |
| E-03 | `export/schemas.py:34` | `dominant_element: str` field on `ExportClass` | **LEAK-RISK** | `dominant_element` holds the canonical-four label (e.g. `"fire"`) on the exported class. Written to classes.json. Drax reads this field and displays it (see surface class 5 below). |
| E-04 | `export/schemas.py:49` | `dominant_element: str` field on `ExportMonster` | **LEAK-RISK** | Same pattern as E-03 for monsters. Written to monsters.json. |
| E-05 | `export/schemas.py:64` | `dominant_element: str | None` on `ExportGearItem` | **LEAK-RISK** | Same pattern for gear items. Written to gear_pool.json. Drax reads and displays this. |
| E-06 | `output/season_writer.py:152` | `"canonical_element": skill.canonical_element` in `_skill_to_dict()` | **LEAK-RISK** | The intermediate season artifact (seasons/ directory) also writes `canonical_element` into the class/monster/trial JSON files. These are not directly player-facing but they are the source for the exporter (E-01, E-02) and could be inspected directly. |
| E-07 | `output/season_writer.py:180` | `"dominant_element": player_class.dominant_element` in `_class_to_dict()` | **LEAK-RISK** | Same pattern for `dominant_element` on the intermediate class JSON. |
| E-08 | `output/season_writer.py:212` | `"dominant_element": monster.dominant_element` in `_monster_to_dict()` | **LEAK-RISK** | Same for monsters. |
| E-09 | `output/season_writer.py:316` | `"dominant_element": trial.dominant_element` in `_trial_to_dict()` | **LEAK-RISK** | Same for trial. |
| E-10 | `output/season_writer.py:109-118` | `elements_block` in `_manifest()` writes `{slot: {"element_id": ..., "name": ..., "tags": ..., "is_new": ...}}` keyed by `"fire"`, `"wind"`, `"water"`, `"earth"` | **LEAK-RISK** | The manifest.json emits the canonical-four slot names as the dict keys (e.g. `{"fire": {"name": "pitch", ...}}`). These keys are exposed in the export packet via `metadata.json`'s `elements` block. However, the VALUES (the per-season names like `"pitch"`) are the intended public-facing data. The KEYS are the leak. |
| E-11 | `export/schemas.py:108-109` | `elements: dict[str, Any]` in `ExportMetadata` | **LEAK-RISK** | The `elements` block in `metadata.json` directly exposes the canonical-four slot names as top-level dict keys. Example: `{"fire": {"name": "pitch", ...}, "wind": ...}`. Both loadout and demo read these keys for per-season name lookup. |

**Surface class 2 summary:** 11 sites; all LEAK-RISK. The export packet is the highest-concentration leak surface — canonical-four labels appear as JSON field names (E-01, E-03, E-04, E-05, E-06, E-07, E-08, E-09, E-10, E-11) and field values (E-03, E-04, E-05 values; E-06 through E-09 values). The export packet files are deployed to Vercel and accessible to any player.

**Stage 3 scope note:** E-10/E-11 (manifest elements keys) are the highest-priority items because both drax consumers use the canonical slot name as the lookup key to resolve per-season names (e.g. `manifest.elements["fire"]?.name`). Stage 3 must design a replacement lookup structure that doesn't expose canonical slot names as dict keys.

---

### Surface Class 3: Spirit Guide Prompt Templates (LLM-bound text)

| # | File + Line(s) | Code context | Classification | Notes |
|---|---|---|---|---|
| SG-01 | `llm/naming.py:10` | `_SLOT_ATTRS = {"fire": "fire_slot", ...}` | **INTENDED-INTERNAL** | Internal lookup dict mapping canonical slot names to Python attribute names. Never sent to LLM directly. |
| SG-02 | `llm/naming.py:26-36` | `_elements_summary_line()` builds `"Seasonal elements: fire={name}, wind={name}, ..."`  | **LEAK-RISK (TO-BE-FILTERED)** | This is the primary Cluster E drift site identified in `pre-llm-substrate-inventory.md`. The function prepends canonical-four slot labels (`fire=`, `wind=`, `water=`, `earth=`) to every class/monster/gear naming prompt. This is explicit canonical-four exposure to the LLM — the exact pattern Stage 3 must replace with per-season-vocabulary-keyed structure. |
| SG-03 | `llm/naming.py:85-89` | `_seasonal_element_line()` builds `"Seasonal element: {name}..."` then prompt includes `"Element: {skill.canonical_element}"` | **LEAK-RISK (TO-BE-FILTERED)** | Two hits in the skill naming prompt. The `_seasonal_element_line()` function correctly resolves canonical_element to the seasonal name for the line above it. But the explicit `"Element: {skill.canonical_element}"` on line 89 passes the canonical-four label verbatim (e.g. `"Element: fire"`) to the LLM. |
| SG-04 | `llm/naming.py:130` | `f"  - {s.name or s.role} ({s.canonical_element}, {s.role})"` in the skills summary section of `name_class()` prompt | **LEAK-RISK (TO-BE-FILTERED)** | Class naming prompt includes per-skill canonical element labels in the skills summary. The LLM receives strings like `"(fire, damage_over_time)"` for each skill. |
| SG-05 | `llm/naming.py:142` | `f"Dominant element: {player_class.dominant_element}"` in `name_class()` prompt | **LEAK-RISK (TO-BE-FILTERED)** | Class naming prompt explicitly states the dominant canonical-four element. Same pattern as SG-03. |
| SG-06 | `llm/naming.py:185` | `f"Dominant element: {monster.dominant_element}"` in `name_monster()` prompt | **LEAK-RISK (TO-BE-FILTERED)** | Monster naming prompt. Same pattern. |
| SG-07 | `llm/naming.py:250` | `f"Dominant element: {item.dominant_element or 'physical'}"` in `name_gear_item()` prompt | **LEAK-RISK (TO-BE-FILTERED)** | Gear naming prompt. Same pattern. |
| SG-08 | `element/selector.py:43-47` | `_SYSTEM_PROMPT` contains `"four canonical role-slots (fire, wind, water, earth)"` | **LEAK-RISK (TO-BE-FILTERED)** | Element selection system prompt explicitly names the canonical-four slots. This call is once-per-season. Stage 3 must redesign the system prompt to reference the grouping layer instead of canonical-four. |
| SG-09 | `element/selector.py:530-544` | Selection user prompt includes `"fire_slot"`, `"wind_slot"`, `"water_slot"`, `"earth_slot"` as JSON output key names in the OUTPUT JSON template | **LEAK-RISK (TO-BE-FILTERED)** | The LLM is asked to fill a structured JSON with canonical-four slot keys. This is deep coupling — the LLM response format itself is canonical-four-keyed. Stage 3 must replace this with grouping-layer-keyed output. |
| SG-10 | `canonical/library_generator.py:84-88` | One-time generation prompt includes `"- Element: {element}"` (canonical-four name) and `"- Element themes: ..."` | **INTENDED-INTERNAL** | Library generation is a one-time setup operation, not per-season. The canonical library itself is an internal engine artifact. However, per `pre-llm-substrate-inventory.md` §9 this is a Cluster E drift site. Classified INTENDED-INTERNAL because it is admin-only, one-time, and not player-facing. Stage 3 scope decision: whether to re-generate the library against grouping-layer vocabulary or leave it as canonical-four internal. |

**Surface class 3 summary:** 10 sites; 8 LEAK-RISK/TO-BE-FILTERED; 2 INTENDED-INTERNAL. The LLM prompt surface is universally exposing canonical-four labels — this is the Cluster E finding from `pre-llm-substrate-inventory.md` confirmed in code. Every naming call (skill, class, monster, gear) and the element selection call expose canonical-four labels directly to the LLM.

---

### Surface Class 4: Spirit Guide Voice Output (LLM response handling and display)

| # | File + Line(s) | Code context | Classification | Notes |
|---|---|---|---|---|
| V-01 | `spirit_guide/spirit_guide.py` (entire file) | Zero LLM calls; zero prompt templates | **INTENDED-INTERNAL** | The Spirit Guide engine-layer (`spirit_guide.py`) is a pure computation module — no LLM calls, no prompt templates, no voice output handling. It exposes structured advisory results (`SwapRecommendation`, `ClassHealthSignal`, `FormRecommendation`) to a future UI layer. The UI layer is not yet implemented. |

**Surface class 4 summary:** 1 site (the module as a whole); INTENDED-INTERNAL. The Spirit Guide has no current player-facing LLM voice output path. The player-facing UI layer that would surface Spirit Guide results is "far-future post-Priority-02 work" per the module's docstring. When that UI is built, its prompt templates must be audited for canonical-four exposure at that time. No Stage 3 action required.

---

### Surface Class 5: Loadout App Data Display (drax-side rendering)

| # | File + Line(s) | Code context | Classification | Notes |
|---|---|---|---|---|
| L-01 | `reincarnated-loadout/src/data/types.ts:11` | `canonical_element: string` field on `Skill` type | **LEAK-RISK** | TypeScript type mirrors the export schema. The field is used directly in rendering. |
| L-02 | `reincarnated-loadout/src/components/SkillTree/SkillDetailPanel.tsx:20` | `resolveElementName(canonical: string, manifest: SeasonManifest)` → `manifest.elements[canonical]?.name ?? canonical` | **INTENDED-PUBLIC-AS-CIPHER** | The resolver correctly maps canonical key to seasonal name. BUT: the `?? canonical` fallback returns the canonical-four label if the manifest lookup fails. This is a partial cipher — working when manifest is available; leaking when not. The fallback must be investigated as a failure-mode LEAK-RISK (see notes). |
| L-03 | `reincarnated-loadout/src/components/SkillTree/SkillDetailPanel.tsx:88` | `<Tag element={skill.canonical_element}>{elName}</Tag>` | **INTENDED-PUBLIC-AS-CIPHER** | The displayed text is `elName` (the resolved seasonal name). But `element={skill.canonical_element}` passes the canonical label as an HTML attribute (used for CSS class lookup). The attribute is in the DOM and inspectable via browser dev tools — a weak leak risk for players who inspect source. |
| L-04 | `reincarnated-loadout/src/components/SkillTree/SkillNode.tsx:23` | `ELEMENT_COLORS[skill.canonical_element]` | **INTENDED-INTERNAL** | Internal CSS class lookup using canonical-four as key. The user sees the color, not the key. |
| L-05 | `reincarnated-loadout/src/components/GearGrid/GearGrid.tsx:22-25` | `ELEMENT_COLORS = { fire: 'text-orange-400', ... }` | **INTENDED-INTERNAL** | Internal color constant keyed by canonical-four. User sees the color class. |
| L-06 | `reincarnated-loadout/src/components/GearGrid/GearGrid.tsx:161-163` | `{slot.item.dominant_element && (...){slot.item.dominant_element}}` | **LEAK-RISK** | Renders the raw `dominant_element` string directly to the player. Players see "fire", "water" etc. as the displayed element label on gear cards. This is a direct unresolved canonical-four display. |
| L-07 | `reincarnated-loadout/src/components/GearGrid/GearGrid.tsx:230-232` | `{slot.item.dominant_element.slice(0, 4)}` | **LEAK-RISK** | Abbreviated canonical-four label displayed in a compact gear slot view (e.g. "fire" truncated to "fire"). Same direct exposure as L-06. |
| L-08 | `reincarnated-loadout/src/components/analytics/ElementPie.tsx:7-10` | `fire: '#f97316', water: '#0ea5e9', earth: '#84cc16', wind: '#06b6d4'` color constants | **INTENDED-INTERNAL** | Internal chart color lookup. The chart displays segment sizes; color labels aren't rendered as text to the player. |
| L-09 | `reincarnated-loadout/src/hooks/useAnalytics.ts:185` | `elemMap.set(cls.dominant_element, ...)` | **INTENDED-INTERNAL** | Internal analytics aggregation using canonical-four as map key. Not rendered to player. |
| L-10 | `reincarnated-loadout/src/data/constants.ts:32-35` | `ELEMENT_COLORS` dict with canonical-four keys | **INTENDED-INTERNAL** | Internal CSS lookup table. |
| L-11 | `reincarnated-loadout/src/data/constants.ts:49-56` | Archetype labels like `fire_mage: 'Fire Mage'` | **LEAK-RISK** | The constant names embed canonical-four labels in archetype key strings (e.g. `fire_mage`). The display values (e.g. `'Fire Mage'`) also contain the canonical element. Stage 3 note: archetype display labels need per-season vocabulary substitution or these labels must be generated dynamically from manifest data. |
| L-12 | `reincarnated-loadout/src/pages/Loadout.tsx:71` | `const canonicals = ['fire', 'wind', 'water', 'earth']` | **LEAK-RISK** | An array of canonical-four labels used to iterate over `manifest.elements`. If the manifest key structure changes at Stage 3, this array literal must change. Also: variable name `canonicals` is loaded in the loadout bundle; inspectable in source maps. |
| L-13 | `reincarnated-loadout/src/pages/Loadout.tsx:122` | `manifest.elements[classData.dominant_element]?.name ?? classData.dominant_element` | **INTENDED-PUBLIC-AS-CIPHER** | Same resolver pattern as L-02. Working cipher; same fallback leak risk. |
| L-14 | `reincarnated-loadout/src/pages/Loadout.tsx:160` | `<Tag element={classData.dominant_element}>{dominantElementName}</Tag>` | **INTENDED-PUBLIC-AS-CIPHER** | Display text is the seasonal name; canonical-four passes as HTML attribute. Same DOM-inspectable weak leak risk as L-03. |

**Surface class 5 summary:** 14 sites; 4 INTENDED-INTERNAL; 3 INTENDED-PUBLIC-AS-CIPHER (with fallback LEAK-RISK); 6 LEAK-RISK. The loadout app has multiple categories of exposure: (a) direct display of canonical-four strings (L-06, L-07 — gear dominant element rendered raw), (b) the working cipher that correctly resolves canonical to seasonal name but has a `?? canonical` fallback that leaks if manifest unavailable (L-02, L-13), (c) canonical-four passed as HTML element attributes and array literals in bundle code (L-03, L-11, L-12, L-14).

---

### Surface Class 6: Debug Logging

| # | File + Line(s) | Code context | Classification | Notes |
|---|---|---|---|---|
| D-01 | `element/selector.py:416` | `log.info("D1 score for novel word '%s': %d/10 → %s", word, total, d1_status)` | **INTENDED-INTERNAL** | Logs D1 scoring results. Does not include canonical-four labels — only the proposed word and its score. INTENDED-INTERNAL (developer logging). |
| D-02 | `generation/season_orchestrator.py:369` | `log.debug("  Class %s: %.1f%% win rate", player_class.id, ...)` | **INTENDED-INTERNAL** | Does not include canonical-four labels. |
| D-03 | `llm/logger.py` | Logs every LLM call's prompt text (system + user, truncated to 500/1000 chars) to JSONL files in `logs/llm_YYYYMMDD.jsonl` | **LEAK-RISK** | The LLM call logger persists the first 500 chars of every system prompt and 1000 chars of every user prompt to disk. Since all LLM call sites pass canonical-four labels in their prompts (SG-02 through SG-09 above), the JSONL log files will contain canonical-four labels. If log files are not gitignored and are ever committed, shared, or accessible to users, this is a durable leak path. Confirm `logs/` is in `.gitignore`. |
| D-04 | `output/summary_formatter.py:20-31` | `elem = player_class.dominant_element` printed to CLI summary | **INTENDED-INTERNAL** | Developer-facing CLI output. Prints canonical-four element names. INTENDED-INTERNAL (only visible to developers running the engine CLI). |
| D-05 | `canonical/library_generator.py:62-63` | `print(f"  [{i}/{total}] {element.name}/{category}...")` | **INTENDED-INTERNAL** | Admin-only one-time generation CLI. Not player-facing. |

**Surface class 6 summary:** 5 sites; 3 INTENDED-INTERNAL; 1 LEAK-RISK (D-03, the LLM call logger). The LLM call logger is the only debug-logging LEAK-RISK — it persists canonical-four labels from all LLM prompt text to JSONL files on disk. The other logging sites are developer-only CLI output.

---

## Section 3 — Per-Surface-Class Summary

| Surface class | Total sites | INTENDED-INTERNAL | INTENDED-PUBLIC-AS-CIPHER | LEAK-RISK | TO-BE-FILTERED (subset of LEAK-RISK) |
|---|---|---|---|---|---|
| 1. Telemetry events | 7 | 7 | 0 | 0 | 0 |
| 2. Export packet fields | 11 | 0 | 0 | 11 | 0 |
| 3. Spirit Guide prompts | 10 | 2 | 0 | 8 | 8 |
| 4. Spirit Guide voice | 1 | 1 | 0 | 0 | 0 |
| 5. Loadout app display | 14 | 4 | 3 | 6+3 fallback | 0 |
| 6. Debug logging | 5 | 4 | 0 | 1 | 0 |
| **Total** | **48** | **18** | **3** | **26** | **8** |

**Observation on most leak-prone surface classes:**

The export packet (surface class 2) is the highest-density LEAK-RISK surface with 11 of 11 sites classified LEAK-RISK. Every field on every exported schema carries canonical-four labels — they are the primary data contract between engine and drax. The loadout app (surface class 5) is the most complex surface because it mixes INTENDED-PUBLIC-AS-CIPHER resolvers (the correct pattern) with bare canonical-four display (the leak).

The 3 INTENDED-PUBLIC-AS-CIPHER sites in the loadout app all use the pattern `manifest.elements[canonical_key]?.name ?? canonical_key` — the `?? canonical_key` fallback is the structural weak point. Under normal operation (manifest available) these are working cipher sites. Under failure mode (manifest unavailable) they become LEAK-RISK.

The LLM prompt surface (surface class 3) has universal exposure — no LLM call currently uses per-season vocabulary as the primary framing. This matches the `pre-llm-substrate-inventory.md` Cluster E finding. These are all classified TO-BE-FILTERED because Stage 3's explicit scope is the prompt-template filter.

---

## Section 4 — LEAK-RISK Enumeration for Stage 3

The following sites require filter implementation before Stage 3 ships. Sites are grouped by implementation pattern and priority tier.

### Priority 1 (must-fix for Stage 3 ship)

**P1-A: Export schema field `canonical_element` on skills**

Sites: E-01, E-02, E-06

The `canonical_element` field is a first-class named field in the export JSON contract. It appears in `classes.json` skills arrays and is read by both the loadout app (L-01) and the demo (`reincarnated-demo/src/types/engine.ts:114` reads `canonical_element: string`). Stage 3 filter approach: add a `seasonal_element` field alongside (or replacing) `canonical_element` in the export schema. The value is the per-season name resolved from the elements block. If replacing (breaking change), MIGRATION.md entry required and drax dispatch required. If adding alongside (additive), drax can migrate readers at its own pace.

**P1-B: Export schema field `dominant_element` on classes, monsters, gear**

Sites: E-03, E-04, E-05, E-07, E-08, E-09

Same pattern as P1-A. `dominant_element` holds the canonical-four string on every exported entity. Filter approach: add a `seasonal_dominant_element` field. Value is resolved the same way as P1-A using the metadata elements block. The canonical-four value can optionally remain for internal/analytics use if a breaking change is avoided.

**P1-C: Manifest elements block canonical-four keys**

Sites: E-10, E-11

The `elements` block in `metadata.json` uses canonical-four slot names as dict keys. Both drax consumers iterate `manifest.elements["fire"]` etc. as their lookup mechanism to resolve per-season names. Stage 3 filter approach: two options. (a) Replace the key structure with a list of `{slot, name, tags, is_new}` objects and update drax to iterate by slot property rather than by key. (b) Add a parallel `elements_by_seasonal_name` dict alongside the existing structure (additive). Option (a) is the cleaner cipher; option (b) is lower blast radius. Either way, drax changes are required and a MIGRATION.md entry is mandatory. The loadout app `canonicals` array literal (L-12) and `manifest.elements[canonical_key]` lookups (L-02, L-13) must both be updated.

**P1-D: LLM prompt canonical-four exposure (TO-BE-FILTERED)**

Sites: SG-02, SG-03, SG-04, SG-05, SG-06, SG-07, SG-08, SG-09

These are the explicit Stage 3 targets per the cipher migration plan. Filter approach: the `_elements_summary_line()` function (SG-02) must be replaced with a per-season-vocabulary-keyed summary that does not mention canonical slot names. The `"Element: {canonical_element}"` prompt lines (SG-03, SG-04, SG-05, SG-06, SG-07) must be replaced with seasonal element names. The `element/selector.py` system prompt (SG-08) must be updated to not mention canonical-four slot names. The JSON output template (SG-09) must use grouping-layer-neutral keys or per-season identifiers. These changes are the core Stage 3 implementation scope per `form-bias-cadence-strategy.md`.

**P1-E: Loadout app bare canonical-four display in GearGrid**

Sites: L-06, L-07

The gear grid renders `slot.item.dominant_element` directly as player-visible text. Once the export packet ships `seasonal_dominant_element` (P1-B), drax must update these render sites to consume the seasonal field instead. Until both engine-side (P1-B) and drax-side changes land, players see canonical-four labels on gear items.

### Priority 2 (fix with Stage 3 follow-on)

**P2-A: INTENDED-PUBLIC-AS-CIPHER fallback leak**

Sites: L-02, L-13 (and L-03, L-14 HTML attribute exposure)

The `?? canonical_key` fallback in `resolveElementName()` returns the canonical-four label if `manifest.elements[canonical]` is undefined. This is a failure-mode leak, not a normal-operation leak. Stage 3 follow-on: replace the fallback with `"unknown"` or a generic placeholder. Also: the HTML `element={canonical_element}` attributes (L-03, L-14) pass canonical-four labels into the DOM. Stage 3 follow-on: replace with a CSS-class lookup ID that doesn't expose canonical names (e.g. use element index or a color-only class).

**P2-B: Loadout archetype label constants with embedded canonical-four names**

Site: L-11 (`fire_mage`, `water_mage`, etc. in constants.ts)

These constant keys embed canonical-four labels. The display values (e.g. `'Fire Mage'`) also expose canonical labels to players. Stage 3 follow-on: replace display values with dynamically computed labels using the season manifest's per-season element names. The constant keys (used for internal lookup) can remain as canonical-four if the display path is corrected.

**P2-C: LLM call logger persisting canonical-four prompt text**

Site: D-03 (`llm/logger.py`)

The JSONL log files on disk contain canonical-four labels from all LLM prompts. Stage 3 follow-on: (a) confirm `logs/` is gitignored (high probability — verify), (b) optionally redact canonical-four labels from logged prompts once Stage 3 ships, or (c) accept that log files are developer-only artifacts not accessible to players and classify as INTENDED-INTERNAL post-Stage-3. Lowest-risk follow-on: add log directory to gitignore confirmation and leave log content unchanged (logs are transient and developer-only).

---

## Section 5 — Recommendations for Form-Bias Stage 3 Dispatch Authoring

### 5.1 Stage 3 scope boundary

Stage 3 as previously scoped targets LLM prompt-template filters only. Based on this audit, Stage 3 must also cover:

1. **Export schema additions** (P1-A, P1-B) — add `seasonal_element` and `seasonal_dominant_element` fields to export schemas. These can ship additively; existing `canonical_element` / `dominant_element` fields can remain for backward compat with pre-Stage-3 drax code.
2. **Manifest elements block** (P1-C) — the `manifest.elements` key structure must change or be supplemented. This has the widest blast radius (both drax consumers iterate these keys). A parallel lookup structure (additive) is the lower-risk option.
3. **Drax update cascade** (P1-E) — once the engine-side exports ship seasonal names, drax must update render sites. This is drax seam work, not star-lord seam work. Stage 3 dispatch for drax should be authored as a companion to the engine-side dispatch.

### 5.2 Recommended Stage 3 dispatch decomposition

Given the blast radius, Stage 3 implementation should decompose as:

- **Stage 3a — Engine side (star-lord/rocket seam):** LLM prompt-template filters in `llm/naming.py` and `element/selector.py`; add `seasonal_element` fields to export schemas; update manifest elements block. Tag: `star-lord/v1.3-stage-3a-export-cipher`. MIGRATION.md entry required.
- **Stage 3b — Drax side (drax seam):** Update loadout app gear display (L-06, L-07); update `resolveElementName()` fallback (L-02, L-13); update archetype display constants (L-11); update `manifest.elements` iteration pattern (L-12). Drax can ship this as an additive update once engine-side seasonal fields are available.

### 5.3 Canonical-four keys as internal lookup infrastructure

After Stage 3, canonical-four labels should remain as internal infrastructure keys in:
- Telemetry DB columns (`canonical_element`, `role_slot`) — correct; never player-facing
- Internal CSS class lookup tables (ELEMENT_COLORS in drax) — acceptable if not rendered as text
- Engine-internal Python dicts and slot mappings — correct; internal use only

The cipher is achieved when no player-facing surface emits a raw canonical-four string. The internal use of canonical-four as a lookup key (for color, for resistance resolution, for telemetry aggregation) does not break the cipher.

### 5.4 Cross-seam consumer notes

- **Rocket (generation seam):** No new emission sites beyond what is already in the export packet. Rocket is upstream of all these export fields; the filtering happens at the season_writer and exporter layer (star-lord seam). No rocket seam changes required for Stage 3a.
- **Gamora (simulation seam):** The simulator uses canonical-four internally for damage resolution (fire resistance, etc.). These are all INTENDED-INTERNAL and correctly isolated. No gamora seam changes required for Stage 3.
- **Drax (loadout/demo seam):** 6 LEAK-RISK sites in the loadout app (L-06, L-07, L-11, L-12, L-02 fallback, L-13 fallback). Stage 3b dispatch targets these. The demo (`reincarnated-demo`) also reads `canonical_element` and `dominant_element` from export JSON (types/engine.ts:114, 204) and uses them for VFX dispatch (`main.ts` — `skill.canonical_element` passed to audio/VFX systems). The demo's VFX dispatch path is INTENDED-INTERNAL (it determines color/effect type from the canonical key, not from player-visible text) — but needs audit at Stage 3b since it uses the same export field.
- **Gandalf (design/analysis seam):** The telemetry DB query surface (`canonical_element` column, `role_slot` column, `seasonal_element_name` column) is correctly designed — queries can use canonical-four as a stable analytical key while `seasonal_element_name` provides the per-season display. No gandalf-layer changes required.

### 5.5 Rubric extension recommendation

The 6-surface-class taxonomy from the P6 forward audit is sufficient for this inventory. One addition is recommended for the Stage 3 dispatch: add a 7th surface class — **"LLM call log artifacts"** — to cover the JSONL log files that persist prompt text to disk (D-03). This is a distinct surface from debug logging (live stderr/stdout) and from LLM prompt templates (the construction code). The log files are durable on-disk artifacts that could be included in shared debugging sessions. Recommend Stage 3 dispatch to explicitly address gitignore status of `logs/`.

---

## Appendix A — Full site count by classification

| Classification | Count | % of total |
|---|---|---|
| INTENDED-INTERNAL | 18 | 37.5% |
| INTENDED-PUBLIC-AS-CIPHER | 3 | 6.3% |
| LEAK-RISK (all) | 26 | 54.2% |
| — of which TO-BE-FILTERED | 8 | 16.7% |
| — of which not in Stage 3 plan | 18 | 37.5% |

**Total sites: 48**

The 18 LEAK-RISK sites not currently in the Stage 3 plan are the primary deliverable of this audit to gandalf's Stage 3 dispatch authoring. They concentrate in:
- Export packet fields (11 sites — P1-A through P1-C)
- Loadout app display (6 sites — P1-E and P2-A/B)
- LLM call logger (1 site — P2-C)

---

## Appendix B — Files audited

**Engine (`reincarnated-engine/src/reincarnated/`):**
- `telemetry/recorder.py`
- `telemetry/migrations.py`
- `export/schemas.py`
- `export/season_exporter.py`
- `output/season_writer.py`
- `output/summary_formatter.py`
- `llm/naming.py`
- `llm/logger.py`
- `llm/client.py`
- `element/selector.py`
- `canonical/library_generator.py`
- `spirit_guide/spirit_guide.py`
- `generation/season_orchestrator.py` (logging grep; no direct canonical-four log hits)

**Loadout app (`reincarnated-loadout/src/`):**
- `data/types.ts`
- `data/constants.ts`
- `components/SkillTree/SkillDetailPanel.tsx`
- `components/SkillTree/SkillTree.tsx`
- `components/SkillTree/SkillNode.tsx`
- `components/GearGrid/GearGrid.tsx`
- `components/analytics/ElementPie.tsx`
- `hooks/useAnalytics.ts`
- `pages/Loadout.tsx`

**Demo (`reincarnated-demo/src/`):**
- `types/engine.ts`
- `ui/classSelector.ts`
- `ui/combatHud.ts`
- `ui/seasonSelector.ts`
- `main.ts` (selective review for display paths)

---

*Authored by star-lord, 2026-05-16. Dispatch: 2026-05-16-star-lord-cipher-migration-paths-audit.md Track A.*
