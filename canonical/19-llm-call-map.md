# LLM Call Map — Engine Reference

**Captured:** 2026-05-09 (post-Phase-3 merge, pre-Priority-02 gear implementation)

**Purpose:** A stable reference snapshot of where the engine calls the Anthropic API today, what each call does, and the projected delta when Priority 02 (gear) lands. Useful for cost monitoring, debugging unexpected call volume, and onboarding future sessions to the LLM-pipeline architecture.

This is engine state at a specific point in time. The call sites and counts may shift as future priorities ship; verify against current code before relying on these numbers.

## Architectural pattern

The engine consistently follows: **LLM as creative proposer, engine as deterministic validator.** The simulator, damage resolver, balance loop, and fight engine never call the LLM. The LLM is invoked only for:

- **Naming** (presentation: class names, skill names, monster names, trial names)
- **Element selection** (creative: choosing which seasonal elements to use, optionally proposing new elements to add to the pool)

This separation is structural. Mechanical generation and combat simulation are pure deterministic code. Adding new generation dimensions (Phases 1–3) added prompt context to existing calls but did not add new call sites.

## Current call sites (5 purposes, 2 logical phases)

### Phase A — Season setup (before generation)

| Purpose | Location | Frequency | Notes |
|---|---|---|---|
| `element_selection` | `src/reincarnated/element/selector.py` (`select_seasonal_elements`) | 1 call per season (occasionally 2–3 with retries on validation failure) | The LLM returns `{selections: ..., proposals: ...}` in one JSON response; any new-element proposals (`element_proposals`) happen *within* this call, not as a separate request |

### Phase B — `_name_everything` (after all mechanical generation, after balance loop)

Located in `src/reincarnated/generation/season_orchestrator.py`. Iterates over generated content and assigns names.

| Purpose | Per entity | Frequency per season |
|---|---|---|
| `skill_naming` | 1 call per skill | ~5 per class × 10 classes = ~50; ~3 per monster × 40 monsters = ~120; ~5 trial skills = ~5 |
| `class_naming` | 1 call per class | ~10 |
| `monster_naming` | 1 call per monster | ~40 (full bestiary — not just the 8-monster gauntlet; all 40 are named) |
| `trial_naming` | 1 call per trial boss | 1 |
| `gear_unique_naming` | 1 call per epic/legendary item | ~80 (gear pool) + ~10 (carried_gear epic+ items with no name) |

**Correction vs. original Phase 3 doc**: The original table listed monster naming as "~8 (gauntlet size)". This was wrong — `_name_everything` iterates the full `bestiary` list (40 monsters), not the 8-monster reference gauntlet. Monster skill naming is similarly ~120, not ~44.

## Calls per season (post-Priority-02, verified against season_001001)

| Source | Count |
|---|---|
| Element selection | ~1 (occasionally 2–3 with retries) |
| Class naming | ~10 |
| Class skill naming | ~50 |
| Monster naming | ~40 |
| Monster skill naming | ~120 |
| Trial naming | 1 |
| Trial skill naming | ~5 |
| Gear pool naming (epic/legendary) | ~80 |
| Carried gear naming (epic/legendary) | ~10 |
| **TOTAL** | **~317 calls per season** |

**Empirical verification**: season_001001 recorded 296 LLM calls at $0.74. The gap from this table's ~317 reflects seasonal variation (class and monster skill counts vary by generation). Treat ~300 as the working estimate.

## Foundation calls (one-time, not per-season)

These are NOT recurring per-season costs but worth noting:

| Purpose | When | Frequency |
|---|---|---|
| Canonical library generation | One-time setup (`generate-canonical-library` CLI command) | Once, per element × effect_category combination (~40+ entries) |
| Color label library generation | One-time setup | Once per 256 color bands (per the spectrum), cached to disk |

These run during initial engine setup and don't repeat for each season.

## What does NOT call the LLM

These are worth being explicit about because they could easily be assumed to:

- **Class generation** (stat templates, skill templates, ability grammar)
- **Monster generation** (archetype-driven, stat-based, ability-grammar-driven)
- **Trial generation**
- **Balance / convergence loop** (entirely deterministic; runs many fights but no LLM)
- **Combat simulation** (damage resolver, fight engine, effect resolution)
- **Telemetry recording**
- **Database migrations**

If a future change accidentally introduces an LLM call into one of these layers, it would represent a meaningful architectural drift. Worth catching during code review.

## Phase 02 (gear) call delta

Per the gear design (file 17) + the gear CLI prompt (file 18):

### What does NOT add calls

- **Common / uncommon gear (~95% of drops):** template-named, 0 LLM calls
- **Balance-loop convergence:** uses *mechanics-only mode* with unlabeled gear, 0 LLM calls
- **Spirit Guide engine API** (`evaluate_gear_swap`, `evaluate_class_health`, etc.): pure deterministic functions, 0 LLM calls
- **Element_proposals for gear:** none — gear inherits the season's existing element selections

### What DOES add calls

- **Rare / Epic / Legendary gear (~5% of drops):** 1 LLM call per item, **consolidated** (single JSON response producing `{name, flavor_text, visual_prompt}` for rare/epic; `{name, flavor_text, visual_prompt, color_signature}` for legendary). Color integration (added 2026-05-09 per design doc § "Color integration") flows as enriched prompt context (color_label from existing `ColorLabelLibrary.label_for()`) and as one additional JSON field on legendary tier — neither adds a new API call. Total stays at **one call per rare+ item.**

**Updated post-CP9 (2026-05-10):** the implementation uses a balanced pool model rather than drop-rate-distributed generation. The pool is fixed-size (10 items per slot × tier = ~200 items total, deterministically seeded). LLM naming is reserved for **epic and legendary tiers only**; rare uses an enriched template pattern (rare-specific adjective list distinguishes it from uncommon).

| Tier | Pool count (4 slots × 10) | Naming approach | LLM calls |
|---|---|---|---|
| Common | 40 | Template `<Material> <Slot>` | 0 |
| Uncommon | 40 | Template `<Adj> <Material> <Slot> of <Element>` | 0 |
| Rare | 40 | Template with rare-tier adjectives (master-forged / heirloom / etched / etc.) | 0 |
| Epic | 40 | LLM (consolidated: name, flavor_text, visual_prompt) | 40 |
| Legendary | 40 | LLM (with `color_signature`) | 40 |
| **Subtotal** | **200 items** | | **80 new calls** |

The original drop-rate-distributed projection assumed ~500 gear items/season and ~25 LLM calls (5% of drops named). The CP8 implementation initially named all rare/epic/legendary (~120 calls), then revised in CP9 to epic+ only (~80 calls). The revision was a deliberate design call — saturation degrades the LLM-naming layer's signal value, and template-named rare gear better supports the player's high-volume keep/vendor decision-making at the cognitive level. Pattern matching on `<Adj> <Material> <Slot> of <Element>` is faster than parsing "Glassworker's Edge" when scanning ~30+ rare drops per session.

Reserving LLM naming for epic+ (~40% of equipped gear at end-game; ~1% of raw drops) preserves the "this is special" signal value of unique names. Smuggling discovery moments live at epic+; that's where the load-bearing emotional payload of named items concentrates.

### New purpose enumeration

- `gear_unique_naming` — for rare+ items (the consolidated call producing name + flavor + visual_prompt + optional color_signature for legendary)

One new purpose, one new code path. Existing `TrackedLLMClient` infrastructure handles tracking, cost recording, and telemetry without changes.

## Total call delta per season

| Era | Calls per season |
|---|---|
| Phase 3 baseline (original doc, incorrect monster counts) | ~119 |
| Phase 3 baseline (corrected: full bestiary, not gauntlet-only) | ~227 |
| Original projection (drop-rate gear) | ~252 (+25) — superseded |
| CP8 initial (balanced pool, rare+ named) | ~347 (+120) — superseded |
| **Post-CP9 + canonical loadout naming (empirically verified)** | **~300 (+80 gear pool + ~10 carried gear)** |

The Phase 3 baseline table originally listed monster naming as "~8 (gauntlet size)" and monster skill naming as "~44". Both were wrong — the full 40-monster bestiary is named, producing ~40 monster names and ~120 monster skill names. The corrected Phase 3 baseline is ~227. The gear delta on top of that is +80 (gear pool) + ~10 (carried gear) = ~317, empirically observed at ~296-300.

The CP9 revision (LLM only at epic+) reduced the gear-naming volume by 33% vs. CP8 initial. Cost at typical Sonnet pricing: ~$0.74/season empirically (season_001001). Further tuning levers remain available if cost becomes material at scale:
- **Reduce pool size:** 5 items per (slot × tier) = ~40 LLM calls instead of ~80. Still sufficient epic+ variety for typical end-game drop accumulation.
- **Common-only template adjective lists:** if generation cost is ever a concern, simplify the template adjective lists rather than touching the LLM tiers.

## Pipeline timing with gear

Pipeline order with Priority 02 added (italic = new):

```
1. Season setup
   - Element selection                          [1 call]
2. Mechanical generation
   - Class generation                            [0 calls]
   - Monster generation                          [0 calls]
   - Trial generation                            [0 calls]
   - Gear catalog generation (mechanics-only)    [0 calls — NEW, but deliberately call-free]
3. Balance / convergence loop
   - Class × gauntlet fights                     [0 calls]
4. NAMING PHASE (_name_everything)
   - Class skills                                [~50 calls]
   - Class names                                 [~10 calls]
   - Monster skills                              [~120 calls]
   - Monster names                               [~40 calls]
   - Trial skills                                [~5 calls]
   - Trial name                                  [1 call]
   - Gear pool naming (epic/legendary only)      [~80 calls — gear]
   - Carried gear naming (epic/legendary only)   [~10 calls — canonical loadout pass]
5. Season writeup / persistence
   - 0 calls
```

Gear naming sits at the end of the existing naming phase, parallel to class/monster/trial naming. It does not change the order or timing of any existing call.

## Critical invariants to maintain

If any of these break in future implementation, LLM cost balloons:

1. **Gear naming is a single consolidated call** producing `{name, flavor_text, visual_prompt}` in one response. If accidentally split into 3 separate calls, cost triples.
2. **Balance loop uses mechanics-only mode** — no LLM calls during convergence. If named gear is generated during balance sampling, calls per season can spike to thousands.
3. **Element_proposals stays embedded** in the element_selection call. Don't accidentally promote it to a separate call site.
4. **Spirit Guide is deterministic.** No "ask the LLM whether this swap is good." If anything in the codebase suggests this pattern, that's an architectural drift to catch.
5. **No per-equip / per-swap LLM calls during play.** All Spirit Guide reasoning is mathematical at engine layer.

## Cost monitoring guidance

The `TrackedLLMClient` records each call to telemetry's `llm_calls` table with `purpose`, token counts, and cost. Useful queries:

```sql
-- Total cost per season
SELECT season_id, SUM(cost_usd), COUNT(*)
FROM llm_calls
GROUP BY season_id
ORDER BY season_id DESC;

-- Cost breakdown by purpose
SELECT purpose, COUNT(*), ROUND(SUM(cost_usd), 4)
FROM llm_calls
GROUP BY purpose
ORDER BY SUM(cost_usd) DESC;

-- Verify no unexpected purposes (e.g., during code review)
SELECT DISTINCT purpose FROM llm_calls;
```

If `purpose` shows values not in the documented enumeration above, that's an unexpected call site introduced by recent code — investigate.

## Cross-references

- `17-gear-and-spirit-guide-design.md` — Priority 02 gear design (the source of the +25 call delta)
- `collaboration-handoff/18-cli-priority-02-gear-prompt.md` — gear implementation CLI prompt
- `src/reincarnated/llm/tracked_client.py` — LLM call infrastructure
- `src/reincarnated/llm/naming.py` — naming call implementations
- `src/reincarnated/element/selector.py` — element selection LLM call
- `src/reincarnated/generation/season_orchestrator.py:401` — `_name_everything` (the naming phase entry point)
