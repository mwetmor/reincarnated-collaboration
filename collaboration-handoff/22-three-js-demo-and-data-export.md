# Pixi.js Demo and Engine Data Export — Companion Track

> **Library decision (2026-05-10, late):** the demo uses **Pixi.js**, not Three.js. The decision was made after considering that the ARPG genre is conventionally 2D top-down (Diablo / Last Epoch heritage); sprite-based art pipelines are more tractable than 3D mesh generation; performance headroom is larger; and the eventual Unity port targets a top-down view that maps more naturally from Pixi.js prototypes. The doc title still says "Three.js" in legacy text below; treat as historical. All implementation references should target Pixi.js. See file 24 for the updated demo CLI prompt and file 25 for the visual content R&D scope.

**Captured:** 2026-05-10 during Priority 02 (gear) implementation, after the playable-demo discussion clarified that the next experiential validation step for the engine is a real-time playable arena rather than a sim viewer.

**Status:** parallel side scope to the main engine roadmap. Not blocking Priority 02; can run concurrently with the back half of Priority 02 work or sequentially after.

## Why this exists

The engine generates rich content (classes, monsters, abilities, gear) but currently validates it only via convergence simulation. There's no way to actually *see* or *play* what the engine produces. The downstream value of building this side scope:

- **Experiential validation.** "Does this class feel fun to play?" can't be answered by convergence math; it needs a real-time loop with input.
- **Visual harness for design decisions.** Gear coherence, ability geometry, color palette work — all easier to evaluate against actual gameplay than against test outputs.
- **Natural precursor to the eventual game client** (Unity, etc.). Whatever ships eventually will need a stable engine→client data contract; the export layer is that contract.
- **Useful even without the demo.** A stable JSON export is needed for: web-based season browsers, debugging convergence outliers, integration with future tools (Meshy text-to-3D, eventual Unity port). The export layer is engine work that pays back regardless of whether the demo gets built.

## Scope summary

| Phase | Owner | Estimate |
|---|---|---|
| Engine: data export layer | Engine repo (Claude CLI) | ~1 week |
| demo1: Stationary playable + 3-stage boss encounter + boss-carried gear | Demo repo (separate Claude agent + family) | ~2.5–4 weeks |
| demo2: Movement + RNG loot + static themed map | Demo repo | ~3–4 weeks |
| **Total** | | **~6.5–9 weeks** |

**Note 2026-05-10:** the original three-phase plan (Phase 1 stationary / Phase 2 movement / Phase 3 loot) was restructured into a cleaner two-phase split. demo1 absorbs the multi-stage encounter mechanic and boss-carried gear visualization, giving it a complete fight → reward → equip → continue loop without RNG dependencies. demo2 distinguishes itself with movement + positional combat + a themed map + the RNG loot economy that depends on Priority 15.

The engine export layer can happen in parallel with the back half of Priority 02 (engine CLI bandwidth permitting) or immediately after Priority 02 wraps. The demo work happens against exported data and doesn't compete with engine bandwidth — the engine and demo agents work in separate repos with the JSON contract as the boundary.

The demo is built against **5–10 generated seasons** so the player has variety: each season exports as its own directory; the demo lets the player pick a season → pick a class → fight a boss from that season. Different seasons have different dimensional configurations, class rosters, and bosses, so the same demo replays as meaningfully different content per season.

---

## Part 1 — Engine data export layer

### Goal

Produce a stable JSON export of a generated season's content, sufficient for a real-time game client to render and play a class-vs-boss encounter end-to-end. Includes class definitions, monster definitions, ability specs, gear pool (post-Priority-02), and damage formula reference.

### Output structure

Each season exports to a directory:

```
exports/
  season_000093/
    metadata.json        # season ID, timestamp, dimensional config
    classes.json         # playable classes with stats + abilities + traits
    monsters.json        # bosses + gauntlet monsters
    abilities.json       # canonical ability spec library (referenced by classes / monsters)
    gear_pool.json       # post-Priority-02: tiered gear instances for drop sampling
    damage_formula.md    # text description of damage math for client implementers
    design_context.md    # one-page glossary: what the dimensional axes mean, energy types, role orientations
```

### JSON contracts (sketch — full schemas during implementation)

**metadata.json:**
```json
{
  "season_id": 93,
  "generation_timestamp": "2026-05-09T15:22:14Z",
  "engine_version": "1.7",
  "dimensional_config": {
    "axes": ["energy_type", "range_profile", "armor_weight", "damage_type", "role_orientation"],
    "active_geometries": ["ranged_physical", "fire_blast", "frost_nova", ...]
  },
  "class_count": 6,
  "boss_count": 3,
  "calibrated_stat_floors": {
    "heavy_floor_str": 92,
    "melee_floor_1h_str": 78,
    "melee_floor_2h_str": 110,
    "ranged_floor_dex": 96,
    "shield_floor_str": 62
  }
}
```

**classes.json:** array of classes, each with:
- `id`, `name`, dimensional axes (`energy_type`, `range_profile`, etc.)
- `stats`: STR / VIT / INT / WIS / DEX values
- `color`: value, palette
- `abilities`: array of ability specs referencing `abilities.json` entries by id
- `traits`: progression-source traits if any (Priority 14 placeholder; empty initially)
- `archetype_label`: emergent classification ("hunter", "fire_mage", etc.)

**monsters.json:** array of bosses + gauntlet, similar shape to classes plus:
- `tier`: trial-boss / gauntlet
- `ai_pattern`: descriptive (used by demo's AI logic)

**abilities.json:** canonical ability specs:
- `id`, `name`, `geometry` (ranged_physical, fire_blast, melee_swing, etc.)
- `element` (fire / water / wind / earth / physical)
- `cooldown_seconds`, `energy_cost`, `energy_type`
- `damage_magnitude`, `damage_scaling` (function of caster stats)
- `effect_metadata`: status effects, durations, secondary effects
- `targeting_mode`: self / projectile / aoe_at_cursor / directional / melee_swing

**gear_pool.json** (post-Priority-02): tiered gear instances ready for drop sampling:
- `tier`, `base_type`, `slot`, `handedness`
- `stats`: GearStats fields
- `traits`: gear-source traits
- `class_fit_profile`, `stat_requirements`
- `color_value`, `color_palette`, `color_signature` (legendary)
- `name`, `flavor_text` (rare+, populated by CP8 LLM naming)

**damage_formula.md:** plain-text or markdown reference describing the damage math the demo needs to re-implement in TypeScript. Should cover: base damage computation, crit roll + crit damage application, block roll + block damage reduction, armor reduction, status effect application. Pseudocode-level detail; not a full Python port.

**design_context.md:** one-page glossary explaining the dimensional vocabulary (energy types, range profiles, role orientations, geometry types) so the demo agent / family can understand what they're rendering without reading the full design docs.

### CLI command

```
python3 -m reincarnated.tools.export_season --season 93 --out exports/season_000093/
```

Options:
- `--season N`: which season to export (must already exist in telemetry DB)
- `--out PATH`: output directory (created if doesn't exist)
- `--include-gear / --no-gear`: gear pool requires Priority 02 complete; flag allows pre-Priority-02 partial export

Add a batch helper:
```
python3 -m reincarnated.tools.export_seasons --range 90-99 --out exports/
```
to produce 10 seasons at once for the demo.

### Engine CLI prompt (paste-ready)

```
Build the engine data export layer per `collaboration-handoff/22-three-js-demo-and-data-export.md` § "Part 1 — Engine data export layer".

Goal: a CLI command that exports a generated season's content as JSON files in a stable, documented format, suitable for consumption by a real-time game client (Three.js demo now, Unity later).

Two phases:

A. Pre-Priority-02 export (ship now or in parallel):
   - metadata.json, classes.json, monsters.json, abilities.json, damage_formula.md, design_context.md
   - Reads from the existing telemetry DB (a season must already be generated)
   - --no-gear flag for this mode
   - Acceptance: re-running export on the same season produces byte-identical JSON (deterministic)

B. Post-Priority-02 export extension (after CP10 wraps):
   - gear_pool.json added
   - Gear pool can be either pre-rolled (~50 instances per tier × 5 tiers ~ 250 instances) or generated on-demand by the consumer
   - For demo simplicity: pre-roll a fixed pool per season at export time

Schema details: see § "JSON contracts (sketch)" in file 22. Full schemas to be authored during implementation; coordinate with the demo Claude agent if any field is ambiguous.

Three implementation workstreams:

1. Schema definitions in `src/reincarnated/export/schemas.py` — frozen Pydantic for each output file. Include version field at top of each schema for forward compatibility.

2. Exporter logic in `src/reincarnated/export/season_exporter.py` — reads season state, transforms to schema, writes JSON. Deterministic: same input → byte-identical output.

3. CLI command in `src/reincarnated/tools/export_season.py` and a batch wrapper for multiple seasons.

Tests:
- Round-trip: export → re-load → assert structural equality
- Determinism: export same season twice → byte-identical files
- Schema completeness: every dimensional axis, every ability geometry, every gear field is captured
- Cross-reference integrity: ability ids in classes.json all exist in abilities.json
- damage_formula.md is human-authored; copy in from design doc and verify it covers the full damage pipeline

Acceptance criteria:
- 5+ seasons can be exported via the batch command without error
- Output files validate against schemas
- design_context.md exists as a hand-authored or template-generated reference
- A separate consumer (mock or actual demo) can read the JSON and reconstruct the season's content for display

Stop after the export layer ships, report in standard format, wait for go-ahead before any further work in this area.

Lookahead: post-Priority-02, this layer extends with gear_pool.json. The schema for that file should be drafted now (even if not populated until gear ships) so the demo agent has a stable target.
```

---

## Part 2 — Three.js demo

### Approach

- **Standalone repository** (recommended: `/Users/admin/Games/reincarnated-demo/` parallel to the engine repo). Or a sibling folder if the family prefers — either works.
- **Reads JSON exports** from `/Users/admin/Games/reincarnated-engine/exports/season_NNN/`.
- **Re-implements damage math in TypeScript** based on `damage_formula.md`. Lightweight; the math isn't complex enough to warrant a Python-JS bridge.
- **All real-time / positional / input concerns live in the demo**, not the engine. The engine stays a deterministic content + math source.
- **Uses 5–10 exported seasons as content variety** — the demo's main menu lets the player pick a season → pick a class → fight a boss from that season.

### demo1 — Stationary playable + wave-structured gauntlet + boss-carried gear (~3–5 weeks)

**Goal:** one playable class progressing through a wave-structured gauntlet — trash monsters → elite monsters → 3-stage progressive act-boss encounter — all stationary combat, abilities on keyboard, real-time resolution, complete fight → reward → equip → continue loop via boss-carried gear (no RNG drops needed).

**Wave structure:**
- Wave 1 (warm-up): 2-3 trash-tier monsters, sequential fights, easy
- Wave 2 (rising threat): 1-2 elite-tier monsters
- Waves 3-5 (climax): 3 act-bosses, one per stage, with brief recovery between
- Total: ~6-8 individual fights per playthrough

**Why this scope:** demo1 exercises everything the engine already produces. The ~8 gauntlet monsters per season become real opponents (not just data sitting in the export). The 3 act-boss classes (intentionally tuned outside the 50% balance window — undertuned ~40% / overtuned ~55–60%) provide the climax. Boss-carried gear gives the encounter loot meaning without requiring Priority 15's RNG loot economy.

**Loot distribution:** drops happen only from act-boss waves — each act-boss drops their carried_gear on defeat. Trash and elite monsters don't drop gear (consistent with current engine state; monsters don't carry gear — that's Priority 13 territory). Concentrating drops at boss waves is also more memorable: each boss kill is a distinct reward moment.

**What you build:**

*Core engine + presentation:*
- Three.js scene: camera, lighting, arena floor, two character meshes (placeholder geometry — colored capsules / cubes are fine initially)
- Real-time game loop with `requestAnimationFrame` and deltaTime
- Input system: keyboard event handling; abilities mapped to keys 1–5; basic attack on left-click or space
- Ability hotbar UI with real-time cooldown ticking
- Resource system per the class's `energy_type` (mana regen over time, rage gain on damage taken, focus/combo per-hit, stamina pool)
- Targeting modes per ability geometry:
  - Self-cast: instant
  - Projectile: fires toward cursor or facing direction; simple straight-line travel; collides with target
  - AOE at cursor: ground indicator at cursor; lands after cast time; hits anything in radius
  - Directional / melee swing: hits anything within range in front of caster
- Status effects (burn, stun, slow) ticking in real-time
- Damage application: re-implement formula from `damage_formula.md` (crit, block, armor)
- HUD: HP + resource bars for both characters, ability hotbar with cooldown indicators, status effect icons

*Multi-stage boss encounter:*
- A season's 3 act-boss classes are loaded as sequential boss phases. Player fights phase 1 → on defeat, phase 2 starts (player stays at current HP/resources, or refills — design call); → phase 3.
- Each phase has its own AI state machine (selects ability based on cooldown availability)
- Phase transitions are visible — brief pause, boss swap, optional dramatic prompt
- Win condition: defeat all 3 phases. Lose condition: player HP reaches 0 at any phase.

*Loot drops on boss defeat — harvested canonical loadouts:*
- **Both player classes AND act-bosses literally carry gear in the engine's design.** The carried_gear isn't algorithmically curated — it's harvested from convergence-loop simulation results. Each class's `carried_gear: list[GearInstance]` is populated post-convergence by selecting the loadout that performed best (highest win rate, with legendary preference as tiebreaker). This gives gear real provenance: "this is the gear that worked for this class when it actually fought."
- Engine task (~1.5 CPs): convergence persists per-fight loadout details; canonical loadout selection runs after convergence completes; class.carried_gear populated from the selection. Persisted to telemetry, exported in JSON, inherited by all downstream consumers.
- The carrying does NOT change combat behavior during convergence — convergence used the sampled per-fight loadouts, and the canonical loadout is just a *post-hoc selection* of which loadout to call canonical. Bosses combat as before; the gear is associated state on the class, capturing what worked historically.
- **demo1 player loads with the player class's canonical loadout as starting equipment** — instead of starting empty, the player begins with "the gear that performed well for this class in simulation." This skips RNG without skipping equipment.
- **demo1 act-bosses drop their canonical gear when defeated.** Predictable, memorable, narratively coherent. "The third boss carried Glassworker's Edge — that's the legendary that helped them win in 73% of their simulated fights, and now it's mine."
- Future game implementations (Unity, etc.) inherit this entire mechanic for free because the canonical loadouts live in engine state and flow through the data export.
- On phase defeat, gear drops visually (item appears at boss's last position, optionally animated upward then settling)
- Pickup mechanic: player presses F (or auto-pickup since stationary) to collect. Gear enters a simple inventory.
- Simple inventory UI showing collected gear with affixes
- Equip mechanic with stat-threshold validation per CP5b (`can_equip()` from the export's gear schema). Refuse equip with clear message if STR/DEX/INT insufficient.
- Stats update in real time when gear changes: HP bar resizes, ability cooldowns recalculate, etc.
- Player can equip dropped gear during the encounter (between phases) for upgraded stats facing the next stage — adds tactical depth ("which ability bonus matters most for the next boss?")

*End-of-encounter flow:*
- Win screen shows: time-to-defeat, gear collected, gear equipped, optional rating
- "Fight Again" button — same encounter resets; gear collected/equipped persists across runs (within session)
- "New Season" button — pick a different season's 3-stage encounter

**Out of scope for demo1:**
- Movement (demo2)
- RNG loot economy (demo2 — demo1 uses deterministic boss-carried gear)
- Static themed map / environment art (demo2)
- Cross-session progression / persistence (each browser session resets)

**Deliverable:** the player can pick a season, pick a class, fight a 3-stage boss encounter to victory or defeat, collect and equip the gear bosses dropped, and replay. demo1 ships independently — no blocking dependencies on Priority 13/14/15.

### Demo Phase 2 — Movement + positional combat (~1–2 weeks)

### demo2 — Movement + RNG loot economy + static themed map (~3–4 weeks)

**Goal:** add positional combat, a themed environment, and a real RNG-based loot loop on top of demo1. The encounter feel changes from "ability rotation against stationary opponents" to "positional ARPG with movement-aware combat and gear progression that compounds across runs."

**Prerequisite:** Priority 15 (Loot Economy Validation) should land before demo2's RNG loot is calibrated — otherwise the drop rates / class-awareness rules are guesswork. demo1's deterministic boss-carried gear is sufficient for showcasing the gear infrastructure; demo2's RNG loot is what validates the loot economy in real play.

**What you add (movement + positional combat):**
- Player movement on WASD; movement speed read from class definition (or derived per range_profile if not in JSON)
- Boss AI movement: state machine per range_profile — melee bosses approach, ranged bosses kite, hybrid bosses cycle. Each phase of the multi-stage encounter has its own movement disposition.
- Hit detection now positional:
  - Melee abilities: distance check + facing direction
  - Projectiles: simple physics; collide on contact with target
  - AOE: radius check at landing point; hits anything in radius
- Arena bounds: characters can't leave arena floor
- Optional: character-character collision (block movement through each other)
- Optional: facing direction (mouse aim or auto-face nearest target)

**What you add (static themed map):**
- Replace demo1's bare arena floor with a **themed map** fitting the season's anchor and elements. The map is static (no procedural map generation in demo2); each season's exported data drives a manually-authored themed environment.
- Visual identity: appropriate textures, lighting, set-pieces matching the anchor (e.g., a "Fading Glassworks" map has glass shards, kiln structures, broken furnaces; a "Smoke Spire" map has smoke plumes, ashen towers).
- The 3-stage boss encounter takes place in this single map; no transitions between maps.
- Optional environmental features (cover, line-of-sight obstacles) — design call; simpler is fine for first cut.
- This is where the family collaborator's art direction matters most.

**What you add (RNG loot economy on top of demo1's pickup/equip):**
- demo1's deterministic boss-carried gear is replaced (or supplemented) with RNG drops sampled from `gear_pool.json` per the locked loot model (one-week seasons, 70/30 smart-loot / pure-RNG hybrid)
- Drops sample from the season's gear pool; visual highlight by tier color (legendary glows brighter than epic, etc.)
- Stash UI for unequipped items (carries forward across runs within session)
- Equip / unequip with stat-threshold validation (already implemented in demo1; extends to stash-equipped swaps)
- "Fight Again" button restarts encounter; equipped gear persists; new RNG drops happen on subsequent boss defeats
- Optional: between-fight inventory management screen
- This is where Priority 15's design work pays off — the loot model produces equitable archetype outcomes if calibrated correctly.

**Out of scope for demo2:**
- Spirit Guide marginal-value recommendations (engine has the API but not in this demo scope)
- Cross-session progression / persistence (each browser session resets)
- Trading or vendor UI
- Procedural map generation (each map is hand-authored per season)
- Pathfinding (simple "move toward target" suffices)
- Dodge mechanic (Phase 5+ engine territory)

**Deliverable:** a full play loop — pick season → pick class → fight 3-stage encounter on themed map → RNG drops + boss-carried drops → equip → fight again — that demonstrates the engine's full content ecosystem in real-time gameplay.

### Demo Claude agent prompt (paste-ready)

```
You're starting work on the Reincarnated Demo — a Three.js playable arena that demos content generated by the Reincarnated Engine. Project context lives at `/Users/admin/Games/reincarnated-collaboration/`; engine code at `/Users/admin/Games/reincarnated-engine/`. You'll work in a separate demo repo (e.g., `/Users/admin/Games/reincarnated-demo/`) to keep concerns clean.

Read in order:

1. `/Users/admin/Games/reincarnated-collaboration/collaboration-handoff/22-three-js-demo-and-data-export.md` — THIS DOCUMENT. The full scope of the demo, the JSON data contract, and the two-phase implementation plan (demo1 + demo2). Note: the original three-phase plan was restructured 2026-05-10 into a cleaner two-phase split with boss-carried gear in demo1.
2. `/Users/admin/Games/reincarnated-engine/exports/season_000093/design_context.md` — engine glossary explaining the dimensional vocabulary you'll be rendering (energy types, range profiles, role orientations, ability geometries).
3. `/Users/admin/Games/reincarnated-engine/exports/season_000093/damage_formula.md` — damage math you need to re-implement in TypeScript.
4. The JSON files in `exports/season_000093/` — your actual data. Skim the structure of each.

You do NOT need to read the engine's source code or the engine's design docs in depth. The JSON contract is your scope — if the contract is missing something, surface it back to the engine team rather than going around it.

Architecture:
- Engine = content + math (already produced; you consume it as JSON)
- Demo = real-time game client (your scope; runs entirely in browser via Three.js + TypeScript)
- Damage math: re-implement in TypeScript per `damage_formula.md`. Don't try to call the Python engine at runtime; that adds complexity for no gain.

Work pattern (similar to the engine repo's CP pattern):
- Per phase, produce an implementation plan first (file in `notes/plans/`)
- Stop for plan review before implementing
- Implement in checkpoints (~1 day each); commit at each; report in built / learned / surprised / next format
- Don't make architectural decisions silently — surface them in the report

Phase 1 priorities (start here):
- Repo setup, Three.js + TypeScript project structure
- JSON loading: read a season export, parse, expose to game code
- Scene setup: arena, two characters (placeholder meshes), camera, lighting
- Real-time game loop with deltaTime
- Input system: keyboard + mouse, abilities on number keys
- One ability fully wired end-to-end (e.g., a basic projectile attack) — through targeting, animation, damage, status — before adding more
- Then expand to remaining ability types iteratively

Family collaborators:
- The project owner (Matt) and his 11-year-old son are co-collaborators on the engine project
- The son contributes gameplay feel, art direction, and class selection — when the demo is at a playable state, ask which classes / bosses he wants to playtest first
- The son is a capable collaborator; engage substantively, not condescendingly. Show him what's working, ask for his opinion, take his feedback seriously.

Constraints:
- No engine code modifications. The engine team owns that. If you need data the engine doesn't currently export, file a request in `collaboration-handoff/` (next available file number) and route through Matt.
- TypeScript, not vanilla JS — type safety on the JSON contract is high-value.
- Keep the dependency footprint small: Three.js, a small math lib if needed, that's about it. No heavy frameworks.
- Performance target: 60 FPS at full HD on a recent MacBook. The demo is not a stress test; 1v1 combat should run smoothly.

Stop after reading the materials above and respond with:
1. One-paragraph summary of your understanding of the scope (specifically that it's now a two-phase split: demo1 = stationary playable + multi-stage boss encounter + boss-carried gear; demo2 = movement + RNG loot + static themed map)
2. Questions or concerns about the JSON data contract (anything ambiguous? missing? expected format?)
3. Proposed demo1 implementation plan as a draft (high-level — don't get too deep; we'll iterate)

Wait for go-ahead before any code is written.
```

---

## Notes for the family collaborator (the project owner's son)

Hi! Here's what's happening with the demo, and where you can have the most fun helping shape it.

**What's getting built**

A real, playable mini-game where you pick a class your dad's engine has generated, then fight a 3-stage boss encounter — three different bosses one after another in the same fight, each one tougher and with different abilities. Like a tiny ARPG demo — you cast abilities mapped to keyboard keys, the bosses fight back, and when you defeat each boss they drop gear you can pick up and equip on the next stage. We're building it in two stages, each one adding something cool:

1. **demo1: Stationary fight + 3-stage boss encounter + gear drops.** Pick your class, pick your season, then fight a 3-boss encounter — phase 1, phase 2, phase 3 — in a single arena. Each boss drops gear when defeated; you can pick up the dropped items and equip them between phases. The next boss is tougher, but your gear is better. Both you and the bosses stand still — abilities only, no walking around yet.
2. **demo2: Movement + better loot + a real themed map.** Now the arena is a real environment that fits the season's theme (smoke spires, fading glassworks, whatever the season's anchor is — you'll have a big role in art direction here). You can move around with WASD. Bosses move too. Loot starts dropping randomly (not just from boss carriers), giving the game a real progression feel.

**Where your input matters most**

- **Class selection.** When the demo is playable, you get to pick which classes are the most fun to play first. Your dad will have generated several seasons of content — each one has different classes, different abilities. Your taste calls the shots on what to playtest.
- **Visual feel.** The demo will start with simple placeholder shapes (probably colored capsules or cubes for characters). When we get to making them look better, your art direction matters — character design, ability colors, what the abilities should *look* like when they fire.
- **What feels fun.** This is the most important thing. Your dad and the engine can math out balance numbers all day, but only a real player can say "this class feels boring" or "this ability is awesome." That feedback is genuinely load-bearing — it's the validation step the engine can't do on its own.
- **Boss design vibes.** When we're picking which monsters to build into bosses, you can weigh in on personality and intimidation factor. The engine generates them mechanically; your design instinct shapes which ones get spotlighted.

**What you don't need to worry about**

- The TypeScript code itself. A separate Claude agent will write that. You'll see it work; you don't have to read it.
- The engine internals. Those live with your dad. The demo just reads JSON files the engine produces.
- Bug fixing. That's the demo agent's job.

Your role is the most important kind: the *first real player*. Everyone else is making things; you're playing them and telling us what's good.

---

## Cross-references

- `canonical/16-project-roadmap.md` — main project roadmap (this side scope sits parallel to Priorities 13 + 14)
- `canonical/17-gear-and-spirit-guide-design.md` — gear architecture (drives `gear_pool.json` schema in Phase B export)
- `canonical/19-llm-call-map.md` — engine LLM call inventory (no LLM calls in the demo; engine handles all generation)
- `collaboration-handoff/20-cli-priority-02-cp3-prompt.md` and successors — Priority 02 implementation prompts (the demo's gear loop depends on Priority 02 wrapping)

## Status checkpoints

Update this section as the companion track progresses:

- [ ] Engine: data export layer (Phase A — pre-gear export, plus gear_pool.json now that Priority 02 is closed)
- [ ] Demo: demo1 — stationary playable + 3-stage boss encounter + boss-carried gear
- [ ] Demo: demo2 — movement + RNG loot + static themed map

## Pre-export readiness flags (from season_001001 inspection, 2026-05-09)

Three fixes needed in `season_writer.py` before the export layer ships — all are small changes to serialization functions:

1. **`carried_gear` not in class JSON** (HIGH): `_class_to_dict()` doesn't include `carried_gear`. The 4-slot gear data must be in `seasons/*/classes/class_NNN.json` for demo1 to access boss-drops. Fix: add `"carried_gear": player_class.carried_gear` to the dict.

2. **`geometry_type` not in skill JSON** (MEDIUM): `_skill_to_dict()` doesn't include ability geometry. Demo1 needs geometry (ranged_physical / line / circle / single_target) to know how to animate each ability. Fix: add `"geometry_type": skill.abilities[0].geometry if skill.abilities else None` (or equivalent — check Skill schema).

3. **`gear_pool.json` not in season output** (MEDIUM): `seasons/*/gear/` only has `catalog.json` (base types). Pre-rolled instances are DB-only. The export layer needs to write `gear_pool.json` (the 200 named instances per season).

Lower priority:
- `is_act_boss` flag: workaround is `balance_metadata.target_winrate != 0.5`; explicit flag is cleaner but not blocking
- `visual_prompt` for gear: exists in DB, not in JSON files; needed for Meshy integration in demo2

**Skill-name collisions** (4/10 classes in season_001001): see `test-plans/naming-polish-backlog.md` item 2. Fix the naming prompt before demo1 ships — identical ability names on the hotbar break UX.
