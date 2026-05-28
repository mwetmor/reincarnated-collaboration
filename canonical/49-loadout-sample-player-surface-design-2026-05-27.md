# 49 — Loadout vs Sample Player-Surface Design

> **STATUS:** CURRENT (load-bearing as of 2026-05-27 evening) — canonical player-surface architecture for the Reincarnated loadout app (drax seam at `reincarnated-loadout/`). Locks the Loadout tab (sandbox / theorycraft / build planner) vs Sample tab (immutable historical snapshot) distinction. Authored per Matt 2026-05-27 evening clarification that the distinction "wasn't documented [or] communicated explicitly... I think has been causing confusion." This doc closes the gap.

**Date:** 2026-05-27 evening
**Author:** gandalf (story-and-design steward)
**Status:** CANONICAL — load-bearing for drax/star-lord/rocket work touching the loadout app + downstream Cycle 14 Wave 5 player-surface composition; future Wave 4 + Wave 5 dispatches consume this doc as authority
**Authority:** Matt 2026-05-27 verbatim "Loadout: Each character from the season which passed the gauntlet. Their skill trees should be empty and able to be filled per node requirements and one T4 should be unlockable. Gear slots should be empty and you should be able to select from the catalogue of gear which fits that character/slot... Sample: Each character with the skill node selection/investment/T4 and gear that they passed the gauntlet with. The character's statistics should be immutable, representing the character that passed the gauntlet as it was."
**Companion docs:**
- `canonical/00-ground-state.md` — ground-state oracle (this doc registers as new CURRENT entry)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` — gear architecture; sets + legendary mechanics; per-kit T4 + supporting chain composition; Wave 4 dependency for Loadout gear pool
- `canonical/41-progression-framework-2026-05-27.md` § 2-4 — L50 hybrid progression framework; ~70-point endgame anchor per § 4 + doc 40 Block A3
- `canonical/47-damage-scaling-architecture-2026-05-27.md` § 4 — physical/magical/hybrid damage formulas; published for Loadout-side live stat calculator
- `canonical/48-cycle-14-class-roster-2026-05-27.md` — PRESERVED-FOR-COMPARISON; no-classes architectural commitment preserved at player-surface layer
- `agentic_orchestration/gandalf/notes/2026-05-27-no-classes-architectural-recommitment.md` — substrate-led discipline; vocabulary lock applies to player-facing tab labels
- `agentic_orchestration/gandalf/notes/2026-05-27-path-1-phase-4-5-7-cycle-14-scope-expansion.md` — Path (1) Cycle 14 architecture; Wave 4 gear pool dependency
- `agentic_orchestration/gandalf/notes/2026-05-27-path-iii-faction-assembly-extension.md` — Path (III) faction-assembly extension; primary_faction_pair + inter-faction relationship narratives surfaced via drax loadout summary
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Discipline #45 (generative-architecture vocabulary lock) applies at player-surface labels

---

## 0. TL;DR

**Two distinct player-surface intents:**

| Tab | Intent | State |
|---|---|---|
| **Loadout** | Sandbox / theorycraft / build planner | **Empty starting state**; player invests skill nodes per requirements; player toggles ONE T4 capstone unlockable; player selects gear from catalog of gear-that-fits-this-kit; stats update live |
| **Sample** | Immutable historical snapshot | Character AS gauntlet-passed; **statistics IMMUTABLE**; represents the character that survived gauntlet + Phase 7 2-layer joint-gate as it was committed |

**Player consequence:** Loadout drives **theorycraft + replayability + future experience-level progression** (Cycle 15+); Sample drives **narrative recognition + canonical reference + game-state integrity**.

**Engine architecture:** single source-of-truth emission (gauntlet-passed kit + committed investment + committed gear loadout); drax derives Loadout tab from Sample state by stripping investment + presenting available options.

**Wave 4 dependency:** both tabs require Wave 4 (T4-attuned gear + D21 acquisition curve) to land for full loadout composition.

---

## 1. The Loadout vs Sample distinction — design intent

### 1.1 Loadout tab — sandbox / theorycraft / build planner

**Intent:** the player explores "what could this character become?" — speculative theorycrafting across skill investment + T4 choice + gear selection.

**Functional spec:**

- **Per-character selection:** player picks a kit from the season's surviving cohort (post Phase 7 2-layer joint-gate SHIPPED-WORTHY verdict; per pre-ratification #1)
- **Skill tree starts EMPTY:** all nodes uninvested; per-node investment slots visible per kit's emergent chain structure (chain_count + chains + supporting chain + T4 candidates per Path (1) Wave 1.5 Stage 3 Option α emission)
- **Per-node requirements:** node investment respects prerequisites + chain depth + branching gates per doc 40 § 8.3.1 (D69 branching gated by depth ≥4 nodes)
- **Total skill points budget:** ~70-point endgame anchor per doc 41 § 4 + doc 40 Block A3; future L50 progression scaling per doc 41 § 2-3 hybrid progression framework
- **T4 toggle:** player toggles ONE of N capstones unlockable (per kit's emergent T4 candidates; chain_count − 1 capstones per D83); ONE T4 active at a time per D66 sharpened
- **Branching investment:** chains with depth ≥4 nodes allow branching per D69 wide-vs-tall lever
- **Gear catalog:** player browses gear-that-fits-this-kit (filtered by primary_stat + weapon_type_family + season's gear pool emit + substrate weapon library per SC-6b)
- **Gear slot selection:** player equips gear into appropriate slots (main weapon + off-hand + sets + legendary per Wave 4 architecture)
- **Live stat calculator:** as player invests nodes + selects gear, character statistics update in real-time per damage scaling formulas (doc 47 § 4)
- **Persistence:** user-per-kit-per-build theorycraft saved (drax-side database; user-scoped storage)
- **Reset:** player can reset investment + clear gear selections; sandbox semantics
- **Future capability** (flagged for Cycle 15+): experience levels modify stat scaling; affects Loadout calculator and Sample display

**Genre precedent:** Path of Exile's Path of Building (community theorycraft tool); Diablo IV armory + build planner; Last Epoch in-app build planner; Lost Ark stat allocator. **Standard ARPG genre pattern.**

**Player intent verbatim per Matt 2026-05-27:** "The goal is for myself or any user to theorycraft as to how they might improve or change the character across nodes/gear/T4 and eventually experience levels (TBD; future capability)."

### 1.2 Sample tab — immutable historical snapshot

**Intent:** the player sees the character AS gauntlet-passed — canonical reference + narrative anchor + game-state integrity.

**Functional spec:**

- **Per-character display:** same kit set as Loadout (gauntlet-passed survivors); but state is COMMITTED + READ-ONLY
- **Skill investment LOCKED:** whatever investment Phase 4 + Phase 5 + gauntlet sim ratified as the kit's combat-validated configuration
- **Active T4 LOCKED:** specific capstone the kit used during gauntlet (per `active_t4_chain` runtime marker per Rocket Stage 3)
- **Gear loadout LOCKED:** specific gear instances generated for gauntlet (per Wave 4 architecture; specific T1/T2/T3+ gear; sets; legendary)
- **Statistics IMMUTABLE:** stat values computed at gauntlet time + frozen
- **No editing:** player cannot modify any aspect of Sample state
- **Canonical reference:** Sample is the "official" character for this season; Court of Forms accumulates ascended Spirits in this state (Cycle 15+ Court mechanics)
- **Player consequence:** "what IS this character right now?" — narrative recognition + canonical anchor

**Player intent verbatim per Matt 2026-05-27:** "The character's statistics should be immutable, representing the character that passed the gauntlet as it was."

### 1.3 Why both tabs matter (composition rationale)

The two tabs serve **distinct player-experience intents** that don't collapse into each other:

- **Loadout without Sample:** loses canonical anchor; players can't reference "what the character actually IS"; Court of Forms accumulation loses meaning
- **Sample without Loadout:** loses theorycrafting + replayability + future progression; player has no way to engage build-craft beyond passive observation
- **Both together:** Sample = canonical reference; Loadout = exploration space — the classic ARPG genre pattern

**Genre-canonical precedent (composition):**
- PoE: in-game character (Sample) + Path of Building (Loadout)
- D4: current character (Sample) + Armory build planner (Loadout)
- LE: current build (Sample) + Loot Lizard planner (Loadout)

---

## 2. Engine emission requirements per tab

### 2.1 What Sample tab requires (engine-side)

Sample = the kit AS gauntlet-passed. Engine currently emits this as the primary committed-state output:

| Data dimension | Current engine emission | Notes |
|---|---|---|
| Kit shape (chain structure + T4 candidates + supporting chain) | ✅ Path (1) Wave 1.5 Stage 3 Option α | Per-kit emergent identity |
| Active T4 | ✅ `active_t4_chain` runtime marker | Per D66 sharpened ONE T4 at a time |
| Skill node investment (as gauntlet-passed) | ⏳ Implicit in gauntlet sim output; may need explicit emission | Per-skill content + investment level reached during gauntlet |
| Gear loadout (specific instances) | ⏳ Partial — `gear_representative.main_weapon` ✅; Sets + Legendary pending Wave 4 | Wave 4 dependency |
| Statistics (final committed values) | ⏳ Computed at gauntlet time; needs explicit emission | Per doc 47 damage scaling + doc 41 progression |
| Faction membership | ✅ ExportFactionCluster (Star-lord Seam 3) | PM-2 D-Hybrid output |
| Inter-faction relationships | ⏳ ExportFactionRelationship (Path III F-C; Wave 3 pending) | Player-facing narrative |
| Substrate-anchor metadata | ✅ `substrate_named_personage_anchor` (D-Sharpened) | Tooltip surface |

**Net:** Sample tab can be largely populated from current engine emission + Wave 4 gear loadout. Wave 4 close unblocks full Sample.

### 2.2 What Loadout tab requires (engine-side)

Loadout = empty + investment options + gear catalog. Engine needs to publish:

| Data dimension | Required for Loadout | Current status |
|---|---|---|
| Kit shape (chain structure; same as Sample) | ✅ Per-kit emergent identity (Path (1)) | Same source as Sample |
| Per-node investment slots + prerequisites | ⏳ Implicit in chain structure; needs explicit schema | Could derive from kit shape + doc 40 § 8.3 |
| Total skill points budget | ⏳ ~70-point endgame anchor per doc 41 § 4 + doc 40 Block A3 | Documented; needs drax-accessible publication |
| Branching gates (depth ≥4 nodes) | ⏳ Implicit in chain depth; needs explicit flag per node | Derive from kit shape |
| T4 candidate list | ✅ Per-kit T4 capstones (chain_count − 1) | Per Math Note 3 emergence |
| Available gear catalog | ⏳ Wave 4 gear pool + substrate weapon library filter | Wave 4 dependency |
| Stat calculator formula | ⏳ Doc 47 § 4 damage formulas + doc 41 progression scaling | Documented; needs drax-accessible publication |
| Empty starting state | ⏳ Derived from kit shape; explicit "uninvested" representation needed | Drax-side derivation |

**Net:** Loadout tab requires Sample-state emission + derivation/publication of investment schemas + gear catalog + stat formulas.

### 2.3 Dual-derivation pattern (gandalf-recommend hybrid approach)

**Engine emits single source-of-truth committed-state JSON per kit.** Drax derives both tabs from this:

```
Engine Output (single source per kit):
{
  "kit_id": ...,
  "kit_shape": {
    "chain_count": 3 | 4,
    "chains": [{name, node_count, branching_eligible}, ...],
    "supporting_chain": {name, t3_cap_node_count, intrinsic_theme},
    "t4_candidates": [{capstone_id, chain_id, archetype_descriptor}, ...]
  },
  "kit_committed_state": {
    "active_t4_chain": "chain_X_capstone_Y",
    "skill_investment": {node_id: points_invested, ...},
    "gear_loadout": {slot_id: {gear_instance_id, gear_metadata}, ...},
    "final_stats": {stat_name: value, ...}
  },
  "kit_metadata": {
    "kit_name_canonical": "Crimson Reaver",
    "kit_name_placeholder": "STR_Heavy_Norse_kit_001",
    "substrate_named_personage_anchor": "Lu Bu" | null,
    "primary_faction_pair_flag": bool,
    "phase7_gate_status": "shipped_worthy",
    "...": "..."
  },
  "season_metadata": {
    "skill_points_budget_endgame": 70,
    "gear_catalog_pool_id": "season_001_gear_pool",
    "stat_formula_version": "doc_47_v1"
  }
}

Drax-side derivation:
- Sample tab consumes: kit_shape + kit_committed_state + kit_metadata (read-only display)
- Loadout tab consumes: kit_shape + kit_metadata (display) + kit_committed_state INVERTED to "empty starting state" + season_metadata (budget + catalog reference + formula)
- Drax stat calculator: consumes stat_formula_version reference + per-investment/per-gear calculations
- Drax user persistence: per-user-per-kit theorycraft state saved separately (NOT in engine emission)
```

**Single source of truth.** Engine commits canonical state. Drax derives Loadout's "starting empty" by zeroing committed state + presenting options. Sample reads committed state directly. No dual emission; clean architectural separation.

---

## 3. Star-lord Track C transform implications

Star-lord Track C transforms engine output (`output/cycle-14-production-season-001/`) into drax-consumable JSON. Per § 2.3 single-source-of-truth pattern:

**Transform requirements:**

| Engine output field | Track C transform | Drax consumption |
|---|---|---|
| `kit_archive` entry | Pass-through as `kit_shape` + `kit_committed_state` | Sample direct; Loadout via derivation |
| `gear_representative` + Wave 4 gear instances | Pass-through as `kit_committed_state.gear_loadout` | Both tabs |
| Phase 5 cohesion-judge output | Pass-through as `kit_metadata.kit_name_canonical` etc. | Both tabs (player-facing labels) |
| ExportFactionCluster | Pass-through as `kit_metadata.faction_*` | Both tabs + Summary tab |
| Per-season metadata (skill budget; gear catalog) | New emission as `season_metadata` | Loadout (catalog reference + stat formula) |
| canonical_archetype_register | Pass-through to Court tab (Cycle 15+) | Court tab |

**NEW emission needed: `season_metadata`** publishing:
- `skill_points_budget_endgame: 70` (per doc 41 § 4 + doc 40 Block A3)
- `gear_catalog_pool_id` (reference to season's full gear pool; Wave 4 produces)
- `stat_formula_version: "doc_47_v1"` (reference to canonical damage scaling)
- Future: `experience_level_curve` (Cycle 15+ progression scaling)

**Star-lord seam concern:** verify Track C transform emits `season_metadata` + full `kit_committed_state` (currently focused on gauntlet sim output; theorycraft surface requires explicit publication).

---

## 4. Drax-side implementation patterns

### 4.1 Loadout tab implementation guidance

**Per-tab state machine:**

```
LOADOUT_TAB_STATE = {
  current_kit_id: <selected from season's SHIPPED-WORTHY survivors>,
  current_kit_shape: <pass-through from engine>,
  user_investment: <player-modified; persisted per user>,
  user_t4_active: <player-toggle; one of kit_shape.t4_candidates>,
  user_gear_selections: <player-selected per slot; from gear catalog>,
  computed_stats: <derived from investment + gear + stat formula>,
  saved_builds: [<user theorycraft snapshots>]
}
```

**Core interactions:**

1. Kit selection: load kit_shape; reset user_investment to zero state; clear user_gear_selections; compute baseline stats
2. Node investment: validate prerequisites + chain depth + branching gates per kit_shape; update computed_stats live
3. T4 toggle: switch user_t4_active among kit_shape.t4_candidates; recompute stats
4. Gear selection: filter season_metadata.gear_catalog_pool by kit fit (primary_stat + weapon_type_family); validate slot compatibility; recompute stats
5. Save build: persist user's theorycraft snapshot per kit
6. Load build: restore previously saved theorycraft

**Stat calculator architecture:**

Stat formula per doc 47 § 4.2/4.3/4.4 (physical/magical/hybrid) + doc 41 progression scaling. Implement as pure function:

```typescript
function computeKitStats(
  kit_shape: KitShape,
  user_investment: NodeInvestmentMap,
  user_t4_active: T4CapstoneId,
  user_gear_selections: GearLoadout,
  stat_formula_version: string
): ComputedStats {
  // ... per doc 47 + doc 41 formulas
}
```

Pure function = testable + reactive (re-runs on any input change) + deterministic.

### 4.2 Sample tab implementation guidance

**Per-tab state machine (minimal; read-only):**

```
SAMPLE_TAB_STATE = {
  current_kit_id: <selected from season's SHIPPED-WORTHY survivors>,
  display_data: <pass-through from engine kit_committed_state>
}
```

**Core interactions:**

1. Kit selection: load kit_committed_state; display read-only
2. (NO editing capability)

Sample tab is fundamentally simpler than Loadout. Display + tooltip + analytics-link, no state mutation.

### 4.3 Composition with other tabs

| Tab | Data dependency | Cycle 14 status |
|---|---|---|
| **Summary** | Per-faction grouping; primary_faction_pair narrative; inter-faction relationships (Path III F-C); seasonal hero; character flavor text | Gates on Wave 3 close (F-C + LLM narrative) |
| **Loadout** | Per § 4.1; season_metadata; gear catalog (Wave 4); stat formula (doc 47); user persistence | Gates on Wave 4 close (gear pool); season_metadata publication |
| **Sample** | Per § 4.2; kit_committed_state | Gates on Wave 4 close (gear loadout); Phase 7 IMPL close (verdict emission) |
| **Encounters** | Encounter set + per-kit Phase 7 verdict per encounter | Gates on Phase 7 IMPL close (encounter sweep) |
| **Analytics** | Star-lord telemetry; cohort KPM distribution; pairwise distance; verdict tracking | Gates on Phase 7 IMPL close + Wave 5 close |
| **Court** | canonical_archetype_register first-emergence (single-season view for Cycle 14 v1) | Minimal v1 OK; full Court mechanics Cycle 15+ |

---

## 5. Wave 4 dependency tracking

Both Loadout and Sample tabs gate on Wave 4 close (T4-attuned gear cohesion + D21 acquisition curve). Wave 4 produces:

1. **Per-season gear pool** (Loadout catalog source)
2. **Per-kit gear loadout** (Sample gear display + Loadout starting state baseline)
3. **D21 acquisition curve calibration** (Loadout context: rarity awareness for gear selection)
4. **T4-attuned gear annotation** (Loadout filtering: T4-aligned gear surfaces preferentially for that kit's T4 capstones)
5. **Set bonuses + legendary multipliers** (Sample stat correctness + Loadout stat calculator inputs)

**Without Wave 4:** Loadout tab is functional for skill investment + T4 toggle but lacks gear selection. Sample tab is functional for shape display but lacks gear loadout.

---

## 6. Future capability — experience levels (Cycle 15+ scope)

Per Matt 2026-05-27 verbatim "eventually experience levels (TBD; future capability)":

Experience-level progression scales stats per level (per doc 41 § 2-3 hybrid progression framework). Implications:

- **Loadout calculator** must support level-driven stat scaling (TBD level cap; TBD per-level scaling formula)
- **Sample tab** shows kit at fixed L50 cap (canonical commit point per doc 41 § 4)
- **Pre-L50 progression** is Cycle 15+ scope (per doc 41 § 4 deferred items)

**Cycle 15+ extension:** when experience-level progression lands, Loadout tab adds level-slider; Sample tab remains L50-fixed (canonical).

---

## 7. Player UX surface composition

### 7.1 Loadout drives theorycraft

Player asks "what could this Crimson Reaver become?" — investigates:
- Different T4 capstone choices (which capstone synergizes with the kit's substrate + supporting chain theme?)
- Skill node investment variations (depth-vs-breadth lever per D69; specialization vs versatility)
- Gear catalog exploration (what gear synergizes with this kit's T4 + element + supporting chain?)
- Build snapshots (save multiple builds per kit for comparison)

**Engagement loop:** speculation → simulation → comparison → save → iterate. Drives replayability + cross-season build-craft engagement.

### 7.2 Sample drives narrative recognition

Player asks "who IS my Crimson Reaver?" — recognizes:
- The specific T4 capstone the Spirit chose during gauntlet
- The gear the Spirit fought with
- The cohesion-judge LLM canonical name + flavor text
- The substrate-anchored named-personage (Lu Bu) tooltip surface (per D-Sharpened metadata)
- The faction relationships and primary-pair narrative (per Path III F-C)

**Engagement loop:** recognition → identification → narrative-immersion → Court accumulation (Cycle 15+). Drives narrative engagement + canonical character identity.

### 7.3 Composition value

Theorycraft (Loadout) + Recognition (Sample) compose to ARPG genre's central engagement pattern:
- Players invest in EXISTING characters (Sample) by understanding their POTENTIAL (Loadout)
- Sample becomes the canonical reference Loadout speculates against
- Court of Forms (Cycle 15+) accumulates Sample identities as canonical Spirit-archetype lineage

---

## 8. Composition with no-classes architectural commitment

Per `agentic_orchestration/gandalf/notes/2026-05-27-no-classes-architectural-recommitment.md`:

- **Loadout tab DOES NOT display "class"** — kits are substrate-emergent identities; "Crimson Reaver" is a Phase 5 LLM canonical name + emergent archetype-shape, not a class taxonomy
- **Sample tab DOES NOT display "class"** — same architectural commitment
- **Faction label DOES display** (per ExportFactionCluster + PM-2 LLM canonical) — but faction is post-hoc cluster identity, not pre-authored taxonomy
- **Substrate-anchor METADATA displays** in tooltip (per D-Sharpened) — "Spirit lineage: Lu Bu" not "Class: Warrior"

**Discipline #45 (vocabulary lock) applies at player-surface labels.** Drax tab labels MUST NOT use "class" vocabulary. Acceptable substitutes: "Spirit / Form / Kit / Archetype / Faction Member" depending on context.

---

## 9. Cross-references

### 9.1 Canonical docs (composes with)

- `canonical/00-ground-state.md` — needs amendment (this doc registered as new CURRENT entry; § 2.5 canonical vocabulary updated for Loadout/Sample distinction)
- `canonical/39-qd-engine-end-to-end-workflow-2026-05-24.md` § 5.7 Phase 7 (joint-gate verdict produces SHIPPED-WORTHY kits — these populate both tabs)
- `canonical/40-gear-balance-guide-architecture-2026-05-26.md` § 8.3 + D66 + D71 + D83 + Block A3 (chain architecture + T4 unlock economics + 70-point endgame anchor)
- `canonical/41-progression-framework-2026-05-27.md` § 2-4 (L50 hybrid + season cardinality)
- `canonical/46-concentration-architecture-2026-05-27.md` (concentration discipline at kit + cluster + faction layers)
- `canonical/47-damage-scaling-architecture-2026-05-27.md` § 4 (damage formulas; Loadout stat calculator authority)
- `canonical/48-cycle-14-class-roster-2026-05-27.md` PRESERVED-FOR-COMPARISON (no-classes architectural commitment preserved at player-surface)

### 9.2 Operational + agent docs

- `agentic_orchestration/gandalf/notes/2026-05-27-no-classes-architectural-recommitment.md` (vocabulary lock at player-surface labels)
- `agentic_orchestration/gandalf/notes/2026-05-27-path-1-phase-4-5-7-cycle-14-scope-expansion.md` (Wave 4 gear pool dependency)
- `agentic_orchestration/gandalf/notes/2026-05-27-path-iii-faction-assembly-extension.md` (primary_faction_pair + inter-faction relationships at Summary tab)
- `agentic_orchestration/gandalf/notes/2026-05-27-path-1-failure-modes-scope-creep-drift-register.md` (Wave 4 gear pool composition dependency add-on candidate)

### 9.3 Discipline composition

- Discipline #1 (math-before-code): Loadout stat calculator implements published formulas (doc 47); not novel math
- Discipline #11 (empirical inspection): drax verifies stat calculator outputs against engine-side reference computations
- Discipline #41 (pre-authored taxonomy interrogation): no class taxonomy at player-surface; faction labels emergent
- Discipline #42 (framing-audit): drax dispatch authoring verifies tab semantic correctness
- Discipline #43 (design-quality audit at wave-close): gandalf audits drax tab integration at Wave 4 + Wave 5 close
- Discipline #45 (generative-architecture vocabulary lock): tab labels NO "class" vocabulary
- Discipline #46 § 7 (per-cell bounding): drax-side queries against per-kit data are bounded by kit count (~28-32 per season; trivial)

---

## 10. Sign-off

**Author:** gandalf (story-and-design steward)
**Status:** CANONICAL — load-bearing player-surface design lock for Loadout app (drax seam at `reincarnated-loadout/`) + Cycle 14 Wave 4 + Wave 5 integration authority
**Authority:** Matt 2026-05-27 verbatim distinction articulation per § 1.1 + § 1.2; closes the documentation gap Matt flagged as "lack of documentation and communication from myself, I think, has been causing confusion"
**Composition:** with no-classes architectural recommitment + Path (1) Cycle 14 scope expansion + Path (III) faction-assembly extension + doc 40 gear architecture + doc 41 progression framework + doc 47 damage scaling + Discipline #45 vocabulary lock

**For:** the canonical lock of Loadout (sandbox/theorycraft/build planner; empty starting state; live stat calculator; gear catalog selection; T4 toggle; user persistence) vs Sample (immutable historical snapshot; gauntlet-passed character; read-only canonical reference). Engine emits single source-of-truth committed-state JSON; drax derives Loadout via inversion + catalog/formula publication. Wave 4 gear pool gates both tabs. Future experience-level progression Cycle 15+ extends Loadout calculator. No-classes vocabulary applies at player-surface labels. Player-experience composition: theorycraft (Loadout) + recognition (Sample) drives ARPG genre engagement pattern + Court of Forms accumulation (Cycle 15+).

**Signed:** gandalf (story-and-design steward)
