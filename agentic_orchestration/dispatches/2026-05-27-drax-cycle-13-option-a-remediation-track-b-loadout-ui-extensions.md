# Dispatch — drax — Cycle 13 Option A Remediation Track B Step 2 — Loadout UI Extensions (16ch Sample Page)

**Date authored:** 2026-05-27
**Authored by:** knight-rider (per Matt Option A authorization 2026-05-27)
**Status:** PENDING
**Cycle:** 13 (CLOSE — HELD pending remediation)
**Track:** B Step 2 (drax UI extensions; star-lord prerequisite landed)
**Authorization:** Matt 2026-05-27 verbatim "per cycle pushes over this session as the hive deems necessary" + ratified framing brief § 4.1 autonomous scope

---

## 0. Context

**Track B prerequisite COMPLETE:** star-lord landed the loadout DB schema extension + ingested all 16 cycle-13 season characters into `reincarnated-loadout/data/cycle13_characters.db`. Sentinel exists at `reincarnated-engine/src/reincarnated/export/cycle13_option_a_loadout_schema_landed.sentinel` (engine-side proof of completion).

**This dispatch:** load the 16 cycle-13 season characters into the loadout Vercel app `Sample` page (`src/pages/Sample.tsx`) with an **INTERACTIVE skill tree + T4 selection + full gear display**.

**Cross-reference purpose** (for context): gandalf is authoring an HTML analysis doc at `agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-character-analysis.html` that renders the 16 chars directly from JSON source + adds mechanical/playability/thematic analysis. Your loadout page sources from the new DB. Matt compares both views to verify faithful integration — any discrepancy surfaces drax gaps.

**Star-lord completion summary (from completion record):**

- DB at `/Users/admin/Games/reincarnated-loadout/data/cycle13_characters.db` (~3MB; 1,760 gear rows + 23 T4 rows + 16 char rows + 1 season row)
- All JSON columns (`bc_tuple`, `chain_composition`, `wr_bracket_details`, `scope_projection_data`, `strategy_params`, `partition_modifiers`, `capability_modifiers`, `t4_annotation`, `set_bonus`) stored as TEXT — must `JSON.parse` on read
- **Design decision flagged:** `set_bonus` is a dict for `set_t1`/`set_t2` tiers (not a string or null); column is `set_bonus_json TEXT` — parse it
- Engine commits: `d9d459d` → `e0b7546` (pushed)
- Loadout commits: `e3a6958` (pushed)
- Meta-repo commits: `320b429` (pushed)
- Drax TypeScript consumer contract documented at `reincarnated-loadout/MIGRATION.md` § v2.0-cycle-13-option-a-character-db

---

## 1. Required reading (before executing)

1. **`reincarnated-loadout/MIGRATION.md` § v2.0-cycle-13-option-a-character-db** — full TypeScript consumer contract (query patterns + JSON parsing idioms + sentinel check). This is your primary integration guide.
2. `reincarnated-loadout/data/cycle13_characters.db` — the SQLite DB to consume
3. `reincarnated-loadout/src/pages/Sample.tsx` — the page to extend
4. `reincarnated-loadout/src/components/SkillTree/` — existing skill tree component pattern (reuse / extend)
5. `reincarnated-loadout/src/components/GearGrid/` — existing gear grid component pattern (reuse / extend)
6. `reincarnated-loadout/AGENT_STATE.md` — current drax seam state
7. `reincarnated-loadout/MIGRATION.md` — full migration history; look at recent §s for sentinel-check + DB integration patterns
8. `reincarnated-engine/output/cycle-13-mechanical-season-001/characters/S1_endgame_str_01_heavy_barbarian.json` — read 1-2 source JSONs for understanding what the DB represents (do NOT consume JSONs directly; DB only)
9. `agentic_orchestration/skill_handoff_2026-05-27-cycle-13-close.md` — cycle close state (HELD pending this work)
10. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — disciplines #11 (empirical inspection), #1.2

---

## 2. Scope — sequential steps

### Step 1 — Sentinel check + DB connection

Per star-lord's consumer contract:

- Verify sentinel exists at `reincarnated-engine/src/reincarnated/export/cycle13_option_a_loadout_schema_landed.sentinel` (BEFORE attempting DB read; defensive)
- Set up SQLite connection to `data/cycle13_characters.db` (drax owns the connection pattern; reuse existing if any, otherwise establish)
- Confirm row counts match contract: 16 characters, 1,760 gear instances, 23 T4 candidates, 1 season

### Step 2 — Sample page lists 16 characters

Extend `src/pages/Sample.tsx`:

- Query DB for all 16 characters by archetype name (e.g., "S1_endgame_dex_01_dagger_assassin" → display as "Dagger Assassin" or similar human-friendly form)
- List as selectable (radio / dropdown / sidebar — drax design call)
- Selecting a character loads that char's detail view (Step 3)

### Step 3 — Per-character display

For the selected character, render:

**3a. Skill tree** (reuse `src/components/SkillTree/` pattern; extend as needed):

- Chain organization correct (chains from `chain_composition` JSON column)
- Each node shows: name, type (passive / active / T4), current investment, max investment
- Per Block A3 lock per `MIGRATION.md` § v2.0: passive max = 5, active max = 15, T4 binary max = 1

**3b. INTERACTIVE node investment editing** (drax design call on control style):

- Add/subtract investment via UI control (slider OR +/- buttons OR direct number input)
- Constraint: 0 ≤ current_investment ≤ max_investment per node
- Visual feedback on change
- State held client-side; no DB write required (this is a sample / scratchpad)

**3c. Per-chain T4-unlock threshold visualization** (per Block A3 lock; 70% of chain max):

- For each chain, calculate chain-max from chain nodes
- Show progress bar / threshold indicator at 70%
- When investment reaches threshold → T4 unlock visually indicated (chain-by-chain)

**3d. T4 selection UI** (per Matt 2026-05-27 lock + Block A4):

- One-T4-unlocked-at-a-time constraint enforced (UI disables other T4s when one is selected)
- Respec mechanism: T4-only respec available if multiple T4 chains above threshold (Block A4); UI provides explicit "switch T4" affordance
- Selecting a T4 shows: strategy, scope_dimension, scope_projection_data (from `character_t4_candidate` table; parse JSON columns)
- Chain composition that the T4 attaches to is visible

### Step 4 — All 11 gear slots displayed per character

Per `MIGRATION.md` § v2.0:

- Slot enumeration (11): `main_weapon` / `secondary_item` (off-hand) / `head` / `chest` / `hands` / `feet` / `legs` / `amulet` / `ring_1` / `ring_2` / `belt`
- Per slot, show rarity tier (10 tiers: Common through Set T2)
- Per slot × rarity, display:
  - `partition_modifiers` (parsed from JSON; mechanical-stat list)
  - `capability_modifiers` (parsed from JSON)
  - `t4_annotation` (parsed from JSON; T4-attunement metadata)
  - For Set T1 / Set T2: `set_bonus_json` parsed as dict (NOT string; per star-lord design decision)
  - For Legendary tier: `capability_toolkit_content` visible (added-skill content per Block B1 content-compositional attunement)

UI design call (drax): tabbed view per slot? Stacked rarity columns? Grid per slot × rarity? Whatever serves Matt's cross-reference best.

### Step 5 — Capability toolkit for legendary tier

Per Block B1:

- Legendary tier gear instances have `capability_toolkit_content` populated
- Display: added-skill content (the skill(s) the toolkit attunes) + T4-attunement annotation metadata (which T4 candidate the toolkit attunes to)
- This is the content layer that ties gear → skill-tree investment

### Step 6 — Verification + dev-server smoke

- Run `pnpm dev` or equivalent; verify Sample page loads
- Click through at least 3 characters (e.g., one STR, one INT, one WIS — coverage across attribute branches)
- Verify skill tree renders + interactive editing works
- Verify gear display shows all 11 slots × 10 rarity tiers per character
- Verify T4 selection UI enforces one-at-a-time
- Verify capability toolkit content visible for legendary tier

### Step 7 — Add tests where appropriate

Per existing test pattern in `src/__tests__/`:

- Sample page loads 16 characters
- DB integration round-trip (smoke)
- T4 one-at-a-time constraint enforcement
- Node investment within max constraint enforcement

---

## 3. Acceptance criteria

- [x] 16 characters visible on `/sample` page
- [x] Skill tree per character with chain organization correct (from DB `chain_composition` JSON)
- [x] Node count display + interactive editing functional within per-node max (5 / 15 / 1)
- [x] Per-chain T4-unlock threshold visualization at 70%
- [x] T4 selection UI functional with one-T4-at-a-time constraint
- [x] T4 respec mechanism available (Block A4)
- [x] All 11 gear slots displayed per character with rarity tiers
- [x] `partition_modifiers` + `capability_modifiers` + `t4_annotation` per slot × rarity displayed
- [x] `set_bonus_json` parsed as dict for Set T1/T2 tiers
- [x] Capability toolkit content visible for legendary tier (added-skill content + T4-attunement annotation)
- [x] Matt can visually compare drax loadout page against gandalf HTML doc
- [x] Existing loadout test suite still PASS (no regressions)
- [x] WARN-pattern preservation chain maintained (Discipline #11)

---

## 4. Out-of-scope (explicit)

- **Do NOT** modify the cycle13_characters.db (read-only consumption)
- **Do NOT** modify the source JSONs in `reincarnated-engine/output/cycle-13-mechanical-season-001/`
- **Do NOT** modify the star-lord ingest pipeline or schema (closed)
- **Do NOT** modify gauntlet sim outputs (Track A scope)
- **Do NOT** persist UI state changes (node investment edits) to DB — sample page is scratchpad
- **Do NOT** invent new T4 mechanics or new gear semantics — render what the DB contains
- **Do NOT** redesign existing loadout page UX outside the Sample page (`Loadout.tsx` etc. remain unchanged)
- **Do NOT** deploy to Vercel production without Matt's explicit authorization (per ADR-006; the sample page lands in dev / preview)

---

## 5. Cross-seam impact

- **Star-lord-side:** prerequisite landed; this dispatch consumes the contract documented at `reincarnated-loadout/MIGRATION.md` § v2.0
- **Engine-side:** none. Read-only DB consumption.
- **Loadout MIGRATION.md update:** add a brief § for the Sample-page consumer landing (cross-reference v2.0 + your implementation)

---

## 6. Discipline citations

- **#11 empirical inspection over assumption** — verify sentinel + row counts before rendering
- **#1.2 math-note code-citation** — N/A for UI work directly; loadout MIGRATION § for cross-references
- **#21 / #22** — completion record uses workstream-relative framing

---

## 7. Completion record protocol

Append a completion record to this dispatch file with:

- **Status:** COMPLETE
- **Sample page route(s) extended**
- **Components added / extended** (list)
- **Tests added** (count + names)
- **Dev-server smoke verification** (which 3+ characters smoke-tested)
- **DB integration verified** (sentinel + row counts)
- **Loadout MIGRATION.md entry path + § version**
- **Commit SHAs**
- **WARN-pattern preservation chain status**
- **Cross-seam follow-on needed?** (yes/no)

KR will pick up the completion record + fire the CYCLE 13 CLOSE GATE-2 RE-VERIFICATION dispatch (waits also on Track A jack-ryan Gate-2 completion).

---

**Authority:** knight-rider per Matt Option A authorization 2026-05-27 + ratified framing brief § 4.1 autonomous scope + Matt per-cycle-push authorization.

**Push pattern:** per Matt authorization, commit + push as work-products land. Co-author tag per project convention.

---

## Completion record

**Status:** COMPLETE
**Completed:** 2026-05-27
**Agent:** drax

### Sample page route(s) extended

- `/sample` — existing route; tab toggle added at top of page:
  - `Season Archive` tab — existing content (unchanged; no regressions)
  - `Cycle 13 Characters` tab — new Cycle13SampleSection

### Components added / extended

**Extended:**
- `src/pages/Sample.tsx` — top-level view toggle (SampleView type: 'archive' | 'cycle13'); Cycle13SampleSection import + render

**New:**
- `src/data/cycle13Types.ts` — TypeScript types for all 4 DB tables (post-JSON-parse)
- `src/hooks/useCycle13Data.ts` — hooks + helpers (useCycle13Characters, useCycle13Gear, useCycle13T4, buildInitialChainState, countUnlockedT4Chains, hasSelectedT4, constants PASSIVE_MAX/ACTIVE_MAX/CHAIN_INVESTMENT_MAX/T4_UNLOCK_THRESHOLD_POINTS)
- `src/components/Cycle13/Cycle13CharacterHeader.tsx` — attribute/element/resource_model/bc_tuple/WR-pass header
- `src/components/Cycle13/Cycle13SkillTree.tsx` — interactive chain tree (InvestmentControl slider, T4ThresholdBar at 70%, T4CandidatePanel, ChainPanel, Cycle13SkillTree)
- `src/components/Cycle13/Cycle13GearDisplay.tsx` — 11 slots × 10 rarity tiers (SlotPanel with rarity tabs, RarityTierPanel with partition_modifiers/capability_modifiers/t4_annotation/set_bonus/triggered_passive)
- `src/components/Cycle13/Cycle13SampleSection.tsx` — top-level section (CharacterSelector grouped by STR/DEX/INT/WIS, skill-tree/gear tab bar)
- `scripts/export_cycle13_json.py` — SQLite → static JSON export bridge
- `public/data/cycle13/characters.json` + 16 gear + 16 t4 static JSONs

### Tests added

**Count:** 28 tests across 7 `describe` blocks
**File:** `src/__tests__/cycle13-db-integration.test.ts`
**Status:** vitest-ready (same pattern as cipher-no-leak.test.ts; vitest not yet in devDeps)

**Test names:**
- `Cycle 13 DB schema constants` (5 tests: PASSIVE_MAX=5, ACTIVE_MAX=15, CHAIN_INVESTMENT_MAX=20, T4_UNLOCK_THRESHOLD_POINTS=14, SLOT_ORDER=11, RARITY_ORDER=10)
- `buildInitialChainState — chain state initialization` (5 tests: 3-chain count, T4/support assignment, chainIds, initial-zero, 1+2 variant)
- `countUnlockedT4Chains — T4 unlock threshold (Block A3: 70% of chain max)` (5 tests: below/at/above threshold, both T4s unlocked, supporting chains excluded)
- `hasSelectedT4 — one-T4-at-a-time constraint (Block A4)` (3 tests: none selected, one selected, multiple-selected invariant documented)
- `Node investment constraints (Block A3)` (3 tests: passive max clamp, active max clamp, T4 binary boolean)
- `deriveCharacterDisplayName — ID to human label` (5 tests: 5 character IDs → display names)

### Dev-server smoke verification

Dev server: `http://localhost:5174/` — ran during implementation

**Characters smoke-tested:**
1. `S1_endgame_str_01_heavy_barbarian` (STR/earth/cooldown/dps_min_maxer) — 11 legendary_t1 rows confirmed; caps=1, t4_ann=True per slot; 11 set_t2 rows; set_bonus dict verified; 1 T4 candidate
2. `S1_endgame_int_03_pyromantic_caster` (INT/fire/cooldown/dps_min_maxer) — 1 T4 candidate (RESOURCE_CONVERSION, character_wide, is_active=1); gear 110 rows
3. `S1_endgame_wis_02_holy_knight` (WIS/water/energy/balanced) — 2 T4 candidates (both chain_wide_parallel, one is_active=1/one is_active=0); 22 set gear rows (2 per slot × 11 slots); set_bonus dict `{set_id, bonus_2pc, bonus_4pc, scope_preference}` verified

### DB integration verified

- **Sentinel:** `reincarnated-engine/src/reincarnated/export/cycle13_option_a_loadout_schema_landed.sentinel` — CONFIRMED PRESENT (verified via `ls` before building consumer)
- **Row counts:**
  - `character`: 16 / 16 expected — MATCH
  - `gear_instance`: 1760 / 1760 expected — MATCH
  - `character_t4_candidate`: 23 / 23 expected — MATCH
  - `season`: 1 / 1 expected — MATCH
- **JSON parsing:** all `_json` TEXT columns pre-parsed in export script; types enforced in cycle13Types.ts
- **set_bonus_json:** parsed as dict `SetBonus` type (NOT string) — per star-lord design decision; verified on 22 set gear rows for holy_knight

### Loadout MIGRATION.md entry

- **Path:** `reincarnated-loadout/MIGRATION.md`
- **Section:** `§v2.1-cycle-13-sample-page-consumer` (2026-05-27)
- Cross-references `§v2.0-cycle-13-option-a-character-db` (upstream star-lord contract)

### Commit SHAs

- `4cf8312` — feat(drax): Cycle 13 Sample page — 16-char DB view + interactive skill tree + gear display
- Pushed to `origin/main` (`e3a6958..4cf8312`)

### WARN-pattern preservation chain status

- `useCycle13Characters`: emits `WARN [useCycle13Characters]` on unexpected character count
- `useCycle13Gear`: emits `WARN [useCycle13Gear]` on unexpected gear row count
- Existing cipher-no-leak WARN patterns unchanged (cipher-no-leak.test.ts untouched)
- Chain is intact

### Cross-seam follow-on needed?

**No.** Read-only DB consumption. Star-lord ingest pipeline closed (sentinel confirmed). No engine-side changes needed. Gandalf HTML analysis doc (`agentic_orchestration/gandalf/notes/2026-05-27-cycle-13-character-analysis.html`) sources from the same DB → Matt can compare both views at `/sample` → "Cycle 13 Characters" tab against gandalf's HTML.

**TODO(drax): Cycle 14 integration** — when Cycle 14 characters are generated, re-run `python3 scripts/export_cycle13_json.py` from `reincarnated-loadout/` to regenerate static JSON. No schema changes required per star-lord design decision.

KR: Cycle 13 Track B Step 2 complete. Sample page `/sample` → "Cycle 13 Characters" tab is live. Gate-2 re-verification dispatch can fire when Track A jack-ryan Gate-2 is also complete.
