# Current State → End State — Battle-Sim + Content-Emission Pipeline

**STATUS:** DESIGN SURVEY + FORWARD MAP (authored for the systematic-planning pass Matt requested)
**Date:** 2026-06-18
**Author:** gandalf (story-and-design steward)
**Purpose:** for EACH of the two systems Matt named — (I) the **battle simulation** and (II) the **full content-emission pipeline** — map the *current state* (what exists, on disk, cited), the *end state* (where we want to be, with a design-anchored definition), and the *space between* (every known blocker / missing component, each explained). Then (III) the bridge that joins them, and (IV) an owner map. This is the artifact we plan from.
**Method:** reconciled against disk THIS session — two thorough Explore reconnaissance passes (simulation seam + emission seam) plus direct gandalf verification of every load-bearing claim (W-F meaning, faction-writer absence, NPC absence, summon/companion taxonomy, gauntlet pass-floor, Godot consumption). File:line throughout.
**Supersedes:** the diagrams in `agentic_orchestration/gandalf/notes/2026-06-18-pipeline-completion-progression-memo.md` (the wind-down memo) — this doc is the disk-verified, expanded version. Where they conflict, this governs.
**Survey-mode discipline:** within each PART, the *Current state* subsections are descriptive (what IS, cited). The *End state* and *The gap* subsections are the forward judgment (what SHOULD be / what's wrong). They are kept structurally separate per the cross-cutting rule.

---

## PART 0 — Shared frame (read first)

### 0.1 The two systems and how they relate

```
  CONTENT-EMISSION PIPELINE                 BATTLE SIMULATION
  (produces a season's content)             (consumes content; measures + plays it)
  ───────────────────────────               ─────────────────────────────────────
  generates kits / monsters /        ──▶    (a) BALANCE APPARATUS  — headless gauntlet
  factions / npcs / gear /                       that decides what content ships
  weapons / flavortext                      (b) PLAYABLE COMBAT   — the fight model a
        │                                        player experiences
        │   one Godot-consumable                      │
        ▼   sim-ready bundle                          ▼
  ════════════════════════ THE GODOT REPLICA ════════════════════════
  Godot loads the bundle AND re-implements the combat model faithfully
  (TODAY: Godot renders arena geometry only — consumes no content, runs no combat)
```

The pipeline **feeds** the sim. The sim has **two faces**: the headless balance apparatus (Python, the authority) and the eventual playable combat (the Godot replica). The end state for the whole effort is operational, not component-checklist:

> **North star:** run one driver → get a complete, balanced season bundle → Godot loads it → that season's kits/monsters/factions/etc. are playable in a fight model faithful to the Python authority.

### 0.2 The four non-kit entity families (governs the pipeline's "npc" and "summon" rows)

A taxonomy correction that prevents schema sprawl downstream. There are **four** families of "things in a fight that are not the player's kit," and they are distinct:

| Family | What it is | Current state | Season-1 scope? |
|---|---|---|---|
| **Monsters** | combat fodder / enemies | generator exists (`monster_generator.py:382`), emitted by old track only | YES |
| **Summons / proxies** | constructs spawned BY a summoner kit's skills | rides on kit skill data (`skill_schema.py:166–203`, 7 proxy fields); sim models as COUNT proxy-population (`proxy_population.py`) + Set #6 capstone (`proxy_commander.py`); **not a separate content type** | YES (embedded in summoner kits) |
| **Companions** | Hall-of-Heroes allies that fight ALONGSIDE the player | framework exists (`companion_generation.py`), corpus ZERO, **season ≥2 by design** (`MIN_COMPANION_SEASON=2`); a modifier-vector behaviour, not a kit | **NO — season 2+** |
| **NPCs** | world-population characters (faction reps, vendors, story-bearers, spirit-guide) | **ZERO infrastructure — no schema, no generator** | YES (the headline gap) |

**Consequence for planning:** "all content types for a season-1 bundle" = kits (incl. summoner kits, which carry their summons) + monsters + factions + npcs + gear + weapons + flavortext. **Companions are correctly out of season-1 scope.** When the NPC spec is authored, it must be defined *against* monsters / summons / companions so we share a substrate rather than minting a fifth bespoke schema.

---

## PART I — BATTLE SIMULATION: current → end

### I.1 Current state — what the battle-sim IS (descriptive, cited)

**The fight engine** (the spatial engine is now the sole live path; the old 1D duel sim is retired):
- `SpatialFightEngine` — `simulation/spatial_gauntlet/spatial_engine.py:1169`; entry `run_spatial_fight()` `:2110`; core loop `run()` `:1369`. Tick-based (0.1s steps): per-tick player action → mob action → HP/status → win/timeout check.
- Damage resolution: `simulation/damage_resolver.py` — 7×7 cross-substrate resistance matrix; physical / magical / hybrid routing (Discipline #38).

**The balance apparatus** (the headless gauntlet that decides what ships):
- `run_gauntlet_sim()` — `simulation/gauntlet_sim.py:1344`; phases W5G.0 setup (`:1381`), W5G.1 execution (`:1405`), W5G.2 pass-verification + result authoring (`:1415`).
- **Terminal pass definition (verified directly):** `gauntlet_pass(cohort)` = `eligible_encounters_passed(cohort) >= GAUNTLET_ELIGIBLE_PASS_FLOOR_W_ALPHA_6` — **≥ 9 of 18 encounters in-band per cohort** (`gauntlet_sim.py:616–636`, floor const `:158`). A kit ships iff `season_emit` = passes **≥1 of 4 cohorts** (`:638–646`). Cohorts: DPS-min-maxer / Balanced / Defensive / Hybrid.
- **In-band** = `tier_2_kpm` (mobs/min) within `ENCOUNTER_COHORT_KPM_BAND[enc_type][cohort]`.

**The measurement honesty fixes — all LIVE as of 2026-06-18:**
- **F1 geometry-honest spatial resolution** — RATIFIED LIVE (`6f3d689`, ratified `f32e48a`); unconditional, no flag (`spatial_engine.py:237–361`). Circle/AOE classes now deal proper area damage.
- **MOB_HP 1.5× anchor** — `arena.py:49` (`MOB_HP_DIFFICULTY_MULTIPLIER = 1.5`); applies to swarm/magic/elite tiers in open_arena + chokepoint. Locked; restores a non-degenerate WR surface after the F1 fix.
- **FLIP #2 — proxy-population tracking ON** — `track_proxy_population=True` (`spatial_engine.py:1195, :2130`); COUNT-only (Axis-2A), byte-identical to OFF for mobs/min.
- **FLIP #3 — keystone-faithful ON** — `apply_max_profile_investment=True` (`combatant.py:486`, `spatial_engine.py:2132`); "kit power" now means the faithful max-profile loadout (keystone multiplier 8.19× per ratification).
- **KPM bands LIVE** — `ENCOUNTER_COHORT_KPM_BAND` (`gauntlet_sim.py:206–323`), 6 encounter types × 4 cohorts, cohort-invariant per shell, fit to the n=3078 empirical distribution: open_arena (9.90, 15.53), chokepoint_corridor (11.65, 15.88), magic_pack (6.06, 11.43), elite_pack (5.65, 10.00), boss_with_adds (2.49, 3.78), mini_boss (0.57, 3.30).

**The BC-coordinate cutover — Stage 2 (in progress):** the 8-axis Battle-Coordinate tuple is replacing the archetype *label* as the structural hub. Tri-state keying is wired (`ai_strategies.py:312–382`): PRIMARY = `bc_target` 8-tuple role priority; FALLBACK = `ARCHETYPE_ROLE_PRIORITY[archetype]`; UNKNOWN = registry default. **The legacy shim still exists**: `ARCHETYPE_ROLE_PRIORITY` (31 entries, `:52–102`), `_PLAYER_CONTROLLER_ARCHETYPES` (8 members, `:45–50`). This session's gandalf gate (BC Stage-2 envelope ACCEPT) cleared the design half; Stage-3 "prove-then-delete" has **not** begun.

**Summons + companions in the sim:** summon constructs modeled as a proxy-population (`proxy_population.py`) with the Set #6 capstone calibrated (`proxy_commander.py:39–71`); companion modifier-vector application + caps + WR-delta guard exist (`balance_loop.py:128–271`) but the companion corpus is ZERO (season ≥2).

### I.2 Current-state process flow

```
A FIGHT (one encounter)
  build CombatantState (kit; apply_max_profile_investment ON → faithful loadout)
   → SpatialFightEngine.run(): tick 0.1s { player act → mob act → resolve dmg (resistance 7×7)
        → status/HP → proxy-count telemetry → win? timeout? } → FightResult (+ 8-axis BC events)

A GAUNTLET RUN (one kit's verdict)
  W5G.0 load 18 SC-6 encounters × 4 cohorts, MOB_HP 1.5×
   → W5G.1 run all fights (F1 geometry live)
   → W5G.2 tier_2_kpm vs ENCOUNTER_COHORT_KPM_BAND → ≥9/18 per cohort?
        → season_emit = pass ≥1 cohort
```

### I.3 End state — where the battle-sim should be (forward judgment)

The battle-sim is "done" when **both faces** are complete:

**(a) The balance apparatus is honest AND architecturally clean:**
1. Measurement honesty: ✓ effectively reached (F1 + MOB_HP + flips #2/#3 + mobs/min bands all live).
2. **BC-coordinate cutover COMPLETE** — Stage-3 prove-then-delete done; the archetype-label shim (`ARCHETYPE_ROLE_PRIORITY`, `_PLAYER_CONTROLLER_ARCHETYPES`, the generation-side `ARCHETYPE_TEMPLATES` / `legacy_archetype_shim`) removed; BC-coordinate is the sole structural hub. (The tri-state FALLBACK/LOUD-DEFAULT must survive until the prove step passes — Disc #12/#39.)
3. **Open balance questions dispositioned** — keystone-ceiling resolved (or parked with a criterion); caster coverage-bound fixed (or scenario-spec'd).
4. **Summon balance calibrated** — `proxy_power_per` / `proxy_max_active` moved off scaffold defaults to gamora-calibrated values.

**(b) The playable combat is portable** — the fight model is faithfully reproduced in the Godot replica (Part III), and the design pillars that have a combat surface are runnable (notably the **trial-room boss gallery**, whose 2D sim path is currently `NotImplementedError`).

### I.4 The gap — every known battle-sim blocker, explained

| # | Blocker / missing component | What it is & why it matters | Owner | What clears it |
|---|---|---|---|---|
| B1 | **BC Stage-3 prove-then-delete** | Tri-state shim still live (`ai_strategies.py:45–102`). Until the prove step runs and the legacy label-keying is deleted, the pipeline has two structural hubs (label + coordinate). This is the single biggest *architectural* incompleteness in the sim. | gamora (impl) + jack-ryan (Gate-2) + gandalf (design confirm) | the prove run (BC-keying equivalence already 16/16 at 0.00) + the delete; my Stage-2 ACCEPT this session unblocked it |
| B2 | **keystone-ceiling (open_arena mean_wr=1.000, zero variance)** | A 1.000 WR with no loss variance is a *ceiling, not a measurement* — it degrades any balance run leaning on open_arena. Distinct from MOB_HP (locked) and FLIP #3 (both correctly did NOT absorb it). | gandalf (call) + gamora (sweep) | **investigation** (keystone-magnitude sweep at fixed MOB_HP 1.5× — does any magnitude restore sub-1.000 WR with variance?) is autonomous-eligible; the **design call** parks for gandalf+Matt |
| B3 | **caster coverage-bound failure** | Session-13: a 3.3× HP reduction moved fire_mage swarm WR only ~0.02. Casters fail on a **spatial/coverage/timeout limit independent of mob HP**, in the swarm/open-arena group-clear. Class-fantasy consequence: caster archetypes feel unfairly punished in a scenario the apparatus over-weights. | gandalf (scenario-design spec) → gamora (impl) | a gandalf scenario-design spec (telegraph windows / arena geometry / timeout calibration for the swarm cohort), then impl becomes eligible |
| B4 | **summon construct calibration** | `proxy_power_per`, `proxy_max_active` are SCAFFOLD defaults (1.0) (`skill_schema.py:182–198`). Summoner kits *function* but their army's power is not yet calibrated against the §7 budget math. Not an existence gap — a balance gap. | gamora | calibrate against the proxy budget math in the spatial sim |
| B5 | **trial-gallery 2D sim path** | `balance_loop.py:2881` raises `NotImplementedError` — the trial-gallery balance path was a 1D-duel diagnostic, retired with the 1D deletion; there is **no 2D single-trial-boss scenario yet**. The trial-room boss gallery is a confirmed design pillar, so this is a real gap for the *game* even though the gauntlet doesn't need it. | gamora (impl) + gandalf (scenario design) | a spatial single-boss scenario spec + port |
| B6 | **dual-element scaling TODO** | `damage_resolver.py:869` — `dual_element_factor = 1.0  # TODO: read from T4 DUAL_ELEMENT_ADDITION context`. Dual-element skills currently get a neutral factor; their intended scaling is unwired. Low blast radius, but a known fidelity gap. | star-lord/gamora | wire the T4 context |
| B7 | **Discipline #39 1.75× scaffold** | `damage_resolver.py:416` — a universal 1.75× placeholder modifier "guarantees Target 4." A scaffold standing in for proper per-kit modifier calibration. | gamora | real modifier calibration |
| B8 | **W-F (Wave-F) consolidation** | *Verified meaning:* "Wave-F" is a forward gated wave, NOT "weapon-faithful." It covers (i) deleting the retired 1D sim, (ii) optionally adopting the reduced-spatial-substrate (`reduced_spatial_substrate.py`, default OFF — a faster search-grade path), (iii) deriving the other 3 cohort keys of `SPATIAL_ENCOUNTER_KPM_BAND` (currently partial/placeholder), (iv) boss-room BC discrimination. **This is consolidation/optimization, NOT a correctness blocker** — the live apparatus is already honest without it. | gamora | a deliberate Wave-F gate (lower priority than B1–B3) |

**Note on B8 — a memo correction:** the wind-down memo framed "W-F adoption" as the step that makes the apparatus "HONEST + LIVE." That was imprecise. The apparatus is *already* honest+live (F1 + flips + bands). W-F is the next consolidation wave; it should be sequenced after the correctness items (B1–B3), not treated as a gate on completion.

### I.5 End-state process flow (target)

```
A GAUNTLET RUN (end state)
  W5G.0 18 encounters × 4 cohorts, MOB_HP 1.5×
   → W5G.1 fights keyed SOLELY by BC-coordinate (no archetype-label fallback — B1 done)
   → W5G.2 ≥9/18 per cohort; caster cohorts measured by FAIR swarm scenario (B3 done);
        open_arena yields a real distribution (B2 resolved); summoner kits balanced (B4)
   → season_emit verdict
  PLUS: trial-gallery boss scenario runnable (B5); the same combat model is the spec the
        Godot replica reproduces (Part III)
```

---

## PART II — CONTENT-EMISSION PIPELINE: current → end

### II.1 Current state — what the pipeline IS (descriptive, cited)

**There is no single end-to-end driver. There are TWO emit tracks that do not meet.**

**TRACK NEW (cycle-14 wave5) — kit/faction-rich, emits to the LOADOUT app:**
- `scripts/run_season_production.py:58` → `wave5_season_orchestrator.run_season_production():2902` → P2 kit-candidates → 2.5 variant-enum → 3 gauntlet+PM1 → 4 mechanical-archive (`kit_archive.db`) → 4.5 PM1-rerun → 5 cohesion-judge LLM (faction identity / season name / inter-faction relationships / per-kit names) → 7 joint-gate → `cycle14_wave5_emitter.emit_season():920`.
- Output → `reincarnated-loadout/data/cycle-14-wave-5-season-{N}/`: `manifest.json` (`:1031`), `classes/*.json` (`:1035–1050`).
- **Faction data is written to SIDECAR files** in `loadout/data/` (`cycle14-season-001-faction-clusters.json`, `wave-b-identities.json`), read separately by the loadout app (`cycle14SeasonData.ts:26–28`) — NOT embedded in the manifest.
- **KIT-ONLY:** no monsters; `main_weapon` / `secondary_item` set to null (`:577–578`); skill `flavor_text` passed through verbatim from phase2 (`:354`); names sourced from the wave-b sidecar.

**TRACK OLD (`season_exporter`) — produces the genuinely sim-ready bundle, but crippled:**
- `cli.py:159` `cmd_export_season` → `season_exporter.export_season():566` → `_export_season_inner():652` → `exports/<id>/{metadata.json:776, classes.json:777, monsters.json:778, gear_pool.json:779, gauntlet_recipe.json:786}`.
- **kit/monster/gear-only** — factions ABSENT (verified: grep `faction` in `season_exporter.py` = empty), npcs ABSENT, weapon = null.
- Its **`generate-season` CLI driver is DELETED** — the docstring at `cli.py:6` is an orphan; no handler is registered.

**The Godot consumer:** `~/Games/reincarnated-godot/` exists, but `data/` holds **only `arena_scenarios.json`** (a serialization of `arena.py` geometry). Its scripts *render scenes* (`render_descent_scene.gd`, `render_arena_room.gd`, spell-VFX bakers). It consumes **zero season content** and runs **no combat.**

**Schemas that exist** (`generation/schemas.py`): `ExportSeason` (`:1165`, with `faction_clusters:1174` + `faction_relationships:1177`), `ExportClass` (`:264`), `ExportMonster` (`:306`), `ExportGearItem` (`:328`), `ExportWeaponDescriptor` (`:223`), `ExportSkill` (`:244`), `ExportFactionCluster` (`:588`), `ExportFactionRelationship` (`:733`), `ExportMetadata` (`:372`). **No `ExportNPC`.**

### II.2 Current-state process flow

```
THE TWO TRACKS THAT DON'T MEET
══════════════════════════════
 TRACK NEW: run_season_production → P2..P7 → cycle14_wave5_emitter.emit_season()
            ──▶ loadout/data/.../{manifest.json, classes/*.json}  + faction/wave-b SIDECARS
            (kits ✓ · monsters ✗ · factions→sidecar · weapons null · npcs ✗)

 TRACK OLD: cli export-season → season_exporter._export_season_inner()
            ──▶ exports/<id>/{metadata, classes, monsters, gear_pool, gauntlet_recipe}.json
            (kits ✓ · monsters ✓ · gear ✓ · factions ✗ · weapons null · npcs ✗)  [driver DELETED]

 GODOT:     reincarnated-godot/data/arena_scenarios.json  (geometry only; no season content)

 ► No path emits all content types into ONE sim-ready bundle. No path reaches Godot.
```

### II.3 Per-content-type state (the honest table)

| Content type | Generated? | Schema? | In sim-ready bundle? | Evidence |
|---|---|---|---|---|
| **kits** | ✓ | ✓ ExportClass | ✓ both tracks | `classes.json`; cycle14 `:1035–1050` |
| **factions** | ✓ (Phase-5 LLM) | ✓ but **writer absent** | ✗ (sidecar in loadout only) | schema `:1174`; cycle14 reads `:939` then discards; old track has none |
| **monsters** | ✓ | ✓ ExportMonster | ✓ old track / **✗ cycle-14** | `monster_generator.py:382`; `season_exporter:740`; cycle-14 uses fixtures (`ENDGAME_ENCOUNTER_CATALOG`) |
| **npcs** | ✗ | **✗ none** | ✗ | no `ExportNPC`, no generator anywhere |
| **gear** | ✓ | ✓ ExportGearItem | ✓ old track | `gear_pool.json:779` |
| **weapons** | ◐ (substrate binding) | ✓ ExportWeaponDescriptor | ✗ (always null) | `substrate_weapon_binding.py:171`; cycle14 null `:577–578`; no `weapons.json` |
| **flavortext** | ✓ class/monster/gear; ◐ cycle-14 | ✓ ExportSkill.flavor_text | partial | `naming.py`; cycle14 passthrough `:354` |
| **summons** | ✓ (rides on kit skills) | ✓ (proxy fields on ExportSkill) | ✓ *if* kit skill data emits | `skill_schema.py:166–203` (see Part 0.2) |
| **companions** | ✗ corpus ZERO | framework only | n/a (season ≥2) | `companion_generation.py:7`, `MIN_COMPANION_SEASON=2` |

### II.4 End state — where the pipeline should be (forward judgment)

> **One driver emits all season-1 content types into a single Godot-consumable, sim-ready bundle.**

End-state bundle (season 1) = **kits** (incl. summoner kits carrying their summons) + **monsters** + **factions** + **npcs** + **gear** + **weapons** + **flavortext**, in one coherent set of files, produced by **one driver**, validated by the joint-gate, and **loadable by the Godot replica**. Companions are explicitly deferred (season 2+). The split is closed: the kit/faction-rich generation feeds the same bundle that carries monsters/gear, and that bundle is what Godot reads.

### II.5 The gap — every known pipeline blocker, explained

| # | Blocker / missing component | What it is & why it matters | Owner | What clears it |
|---|---|---|---|---|
| P1 | **THE SPLIT (the spine blocker)** | The kit/faction-rich track emits to the loadout app; the bundle-producing track is kit/monster/gear-only with its driver deleted. No single driver emits all types into one sim-ready bundle. Everything else is downstream of fixing this. | star-lord + rocket (plumbing) | a single driver that routes cycle-14 content through (or replaces) `season_exporter` |
| P2 | **faction writer absent** | Schema present (`schemas.py:1174`), data generated, but **no code writes `faction_clusters` to the bundle** (verified: not in `season_exporter`; cycle-14 reads then discards to disk). | star-lord (plumbing) | gated on **gandalf faction content-shape spec** (which fields are sim-load-bearing vs presentation) — §7.2(2) of the wind-down memo |
| P3 | **monsters not in cycle-14 track** | `monster_generator.py` is wired only into the old track; the cycle-14 track uses fixed `ENDGAME_ENCOUNTER_CATALOG` encounters. A complete season needs generated seasonal monsters in the unified bundle. | rocket + star-lord | wire monster generation into the unified driver |
| P4 | **NPCs missing entirely** | No schema, no generator. The only fully-absent season-1 content type. This is the **headline gandalf design item** — what *is* an NPC in the seasonal-journey frame, defined against the four-family taxonomy (Part 0.2). | gandalf (content spec) → rocket/star-lord (build) | a gandalf NPC content spec (ExportNPC fields + content-gen intent), then the build |
| P5 | **weapon descriptor null** | Identity lives in `substrate_weapon_binding` but `main_weapon` is always null; no `weapons.json`. The sim/Godot can't show or use weapon identity. Lighter than NPC — the binding already exists; this is wiring-shape. | star-lord (plumbing) | gated on a **gandalf weapon content-shape spec** (is a weapon a type or a gear-subtype; what the sim needs) |
| P6 | **cycle-14 flavor/naming split** | Cycle-14 skill flavor is passthrough and names come from a sidecar; flavor coverage is uneven across content types. Player-facing texture inconsistency. **D7 discipline binds** any expansion (templated structure + narrow LLM blanks, never raw LLM at major moments). | star-lord (plumbing) + gandalf (flavor intent) | unify flavor emission in the driver |
| P7 | **Godot consumes no season content** | Godot reads only `arena_scenarios.json`; it has no loader for kits/monsters/factions/etc. Even a perfect bundle isn't *consumed* yet. (See Part III — this is half the bridge.) | drax/galadriel (Godot side) | a Godot season-bundle loader |

---

## PART III — The bridge: how the pipeline output becomes a playable Godot battle-sim

Matt's phrasing — "the replica of the battle sim to run" in Godot — names a target that has **two unbuilt halves**, and being honest about both is what makes the plan real:

**Bridge-half 1 — content consumption.** Godot must read the season bundle (kits/monsters/factions/npcs/gear/weapons/flavortext). Today it reads only arena geometry. This is gated on the pipeline producing the bundle (Part II) AND a Godot-side loader (P7).

**Bridge-half 2 — combat-model parity.** Godot must *reproduce the Python sim's combat faithfully* — the same damage resolution, resistance matrix, geometry resolution, tick model, status/ailment behaviour. **This is largely greenfield in Godot.** Today Godot does scene *rendering* (descent scenes, arena rooms, spell VFX) — not combat. The Python `SpatialFightEngine` is the authority; a GDScript/C# re-implementation is a substantial, currently-unstarted effort.

This is why "battle-sim completion" and "pipeline completion" are necessary but **not sufficient** for the playable end state. The parity bridge is the third large workstream, and it deserves its own line in the plan rather than being folded silently into either system. There is already encouraging scaffolding: `arena_scenarios.json` is *explicitly a serialization of `arena.py`* and there's a `check_descent_parity.py` script — the team is already thinking in parity terms on the *geometry* axis. Combat parity is the larger, next axis.

```
PIPELINE (Part II)  ──bundle──▶  GODOT LOADER (P7)  ──┐
                                                       ├──▶  PLAYABLE SEASON
BATTLE-SIM model (Part I) ──parity re-impl (bridge-2)─┘     (the north star)
```

---

## PART IV — Owner map (who clears what)

- **gandalf (design specs, no code):** B2 keystone-ceiling call · B3 caster scenario-design spec · B5 trial-gallery scenario design · P2 faction content-shape · P4 **NPC content spec (headline)** · P5 weapon content-shape · P6 flavor intent · pre-registered endorse-criteria (the lever that makes additive downstream autonomous-eligible).
- **gamora (sim impl):** B1 BC Stage-3 · B2 sweep · B3/B5 impl · B4 summon calibration · B7 modifier calibration · B8 Wave-F.
- **rocket + star-lord (emission plumbing):** P1 unified driver · P2 faction writer · P3 monster wiring · P5 weapon wiring · P6 flavor unification · B6 dual-element wiring.
- **jack-ryan:** Gate-2 on B1 (BC implementation) and each additive build.
- **drax / galadriel (Godot side):** P7 season loader · bridge-half 2 (combat parity) scaffolding.
- **Matt:** push gate (ADR-006); the keystone-ceiling design call; any locked-decision re-open.

---

## PART V — Open questions for the planning pass

1. **Sequencing priority within the battle-sim:** B1 (BC Stage-3) is the biggest architectural item and is now unblocked by this session's ACCEPT. Do we close B1 before or in parallel with the open balance questions (B2/B3)? My lean: B1 first (it removes a whole structural hub; B2/B3 measure cleaner against a single hub).
2. **Pipeline-first vs sim-first:** the content-emission spine (P1–P5) and the battle-sim items (B1–B5) are largely independent. The unattended-run analysis (wind-down memo §5–§6) says a single pre-authorized run can advance BOTH. Do we want that, or a focused sim-completion pass first?
3. **NPC scope decision (P4):** does the spirit-guide (doc 17, already designed) emit through the NPC path or separately? Are combatant-NPCs in season-1 scope, or narrative-only? This decision sizes P4.
4. **Bridge-2 timing:** when does combat-parity re-implementation in Godot start? It's the longest pole to the playable north star and currently unstarted. It should not stay invisible in the plan.
5. **Companion confirmation:** confirm companions stay season-2+ (current code enforces it) so we don't accidentally scope them into the season-1 bundle.

---

**Signed:** gandalf, 2026-06-18. The space between here and the end state is now mapped and disk-verified. Two systems, one bridge: the battle-sim is ~one architectural item (B1) + three balance dispositions (B2–B4) from a clean authority; the pipeline is one spine-join (P1) + the faction/weapon writers (P2/P5) + the NPC build-from-zero (P4) from a complete bundle; and the Godot replica needs both halves of the bridge (content loader + combat parity) before a season is playable. Ready to plan.
