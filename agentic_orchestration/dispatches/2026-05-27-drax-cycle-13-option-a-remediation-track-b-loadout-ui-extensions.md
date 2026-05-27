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
