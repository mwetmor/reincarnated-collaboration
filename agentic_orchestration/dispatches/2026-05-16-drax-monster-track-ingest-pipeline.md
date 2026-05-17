# Dispatch — 2026-05-16 — drax — Monster-track ingest pipeline (CreativeKind Tier-2 bundle; VS2a enemy combatant rendering)

**From:** knight-rider (authored per Matt 2026-05-16 Tier-2 acquisition: CreativeKind 26-pack bundle $84.99 + Tier 1 monster-track scout commission)
**To:** drax
**Approved by:** Matt at 2026-05-16 Day 4 (Tier 2 confirmed; assets loaded at confirmed path)
**Status:** PENDING — HOLD-on-prior. Do NOT execute until your in-flight character-wire-up dispatch (`drax/v0.19-character-wire-up-void-attribution` work) completes; drax can only run one dispatch per session (per-seam AGENT_STATE.md sharing).
**Estimated effort:** 2-3 sessions (~6-12h); new monster-track ingest pipeline + per-encounter-tier monster rendering integration; pattern reference: chierit character-track pipeline (`drax/v0.18`).
**Acceptance:** Monster-track ingest pipeline assembles CreativeKind monster sprite sheets + metadata.json; subset of 10-13 monsters selected covering trash/elite/mini-boss/boss tiers; demo renders monster sprites in place of archetypeRenderer primitives for enemy combatants; ENEMY_TIER_CHARACTER_MAP established (per encounter tier OR per-monster-name lookup); wave-composition integration with rocket's wave_composition_rules.py per-wave AI pool selection; smoke verifies visible monsters in demo; intermediate tag.

---

## Why this dispatch exists — closes enemy combatant rendering gap

Per drax v0.12 room/hallway + v0.15 B11 demo + v0.18 character-track + v0.19 character-wire-up dispatches:

- Player characters render real chierit sprites (post v0.19)
- VFX render real Pimen / Pixogen Lite sprites
- **Enemy combatants STILL render as archetypeRenderer primitives** — visual mismatch with the player + VFX polish

Per Matt Tier-2 CreativeKind acquisition + legolas monster-track scout (`agentic_orchestration/research/catalogue/monster-track-vendor-scout-2026-05-16.md`):

- CreativeKind monster line confirmed pixel-art register (Pattern P8 / Drift-13 cleared per scout)
- Lich pack has 29-frame Casting state directly pairing with B11 caster-channel mechanics
- License: VERIFY (provisionally clear per scout; no Patreon gate — verify on a pack page when convenient)

## What's in the acquired bundle

Per inspection at `/Users/admin/Games/reincarnated-demo/public/assets/CreativeKind/` (30+ directories; bundle is MORE than the advertised 26 packs):

### Monster sprites (PRIMARY value)

**Tier 1 — Trash mobs / common enemies**: 8_sword_warrior (red/black/blue/nopreviewgif), Goblin_Mage, Evil_alien_creature (1/2/4 + Egg), Evil_Eye, Mutant_skeleton, Dark_Soul, SpearWarrior, Warrior (+ Warrior_New_Color + Warrior_v2_with_jump)

**Tier 2 — Elite / specialty enemies**: Demon_mage (+ nopreviewgif variant), blue_mage, red_mage, Archimage, Crystal_golem, Fire_Elemental, Crystal_Wisp, Elemental_mage, Magic_Wisp_Pack

**Tier 3 — Mini-boss**: Lich (29-frame Casting; legolas-flagged for B11 caster pairing), Hellfire_Rhino, Fire_Lord, God_of_Lightning (Light + Dark versions)

**Tier 4 — Boss**: Angel_Guardian, Angel_Mage, angel_v1

### Supplementary VFX (NOT this dispatch's primary scope)

Dark_Hole, Energy_Ball (+ Explosion), Fire_attack, Lightning_horizontal, Lightning_vertical, sword_sprite — already-have-equivalent via Pimen / Pixogen; defer to VS2b consideration.

## What this dispatch does

### Step 1 — Monster-track ingest pipeline (new module)

Create `~/Games/reincarnated-demo/scripts/monster-ingest/` (parallel to `scripts/character-ingest/` from v0.18):

- **Stage 1 — Assembly**: CreativeKind ships as already-extracted directories (no zip; no unpack needed). Detect animation sheets per monster directory (PNG/GIF formats; mixed canvas sizes per legolas scout).
- **Stage 2 — Metadata**: build per-monster metadata.json (animation states + frame counts + canvas dims + tier classification + element-flavor-tags if applicable)
- **Stage 3 — Runner**: orchestrator shell script (similar pattern to character-ingest)
- Output: `public/assets/monsters/<monster-slug>/` with sheets + metadata.json per monster

**Discipline #10 (empirical inspection over assumption)**: inspect 2-3 monster directory structures BEFORE designing the pipeline. CreativeKind packs may have varied internal organization (per-animation-folder vs flat sheets vs Aseprite-derived vs preview-gif-included). Don't assume; verify.

### Step 2 — Monster subset selection (10-13 monsters total)

Per Reincarnated wave composition needs + dispatch dispatch scope discipline (NOT ingest all 30+), select representative subset:

**Suggested initial subset** (drax discretion; consult elrond-curated catalogue conventions where applicable):

| Tier | Suggested monsters | Wave usage |
|---|---|---|
| Trash (Wave 1-3 adds) | Goblin_Mage / Mutant_skeleton / Evil_Eye / 8_sword_warrior_red / Evil_alien_creature_1 | most common; high spawn rate |
| Elite (Wave 3-4) | Crystal_golem / Fire_Elemental / Demon_mage | mid-tier; lower spawn rate |
| Mini-boss (Wave 5) | Lich (priority — B11 caster pairing) / Hellfire_Rhino | per-wave-5 boss-room encounter |
| Boss (Wave 6-7) | Angel_Guardian / God_of_Lightning_Light_Version | act-boss encounters |

Document the selection rationale in CHARACTER_TRACK_INTEGRATION_NOTES.md (or new MONSTER_TRACK_INTEGRATION_NOTES.md).

### Step 3 — Monster renderer integration in demo

Create `~/Games/reincarnated-demo/src/visuals/monsterSprites.ts` (parallel to `characterSprites.ts` from v0.18):

- Load per-monster metadata.json
- ENEMY_TIER_CHARACTER_MAP: tier-classification → monster slug (e.g., `{trash: [...], elite: [...], mini_boss: [...], boss: [...]}`)
- Render per-encounter monster using sprite (replaces archetypeRenderer primitive for enemy combatants)
- Animation state machine: idle / attack / hit / death (varies per monster's actual content)
- Integrate with per-room aggro state machine (v0.12) + B11 demo integration (v0.15)

### Step 4 — Wave-composition integration

Rocket landed `wave_composition_rules.py` for Wave 4 pack composition (close/medium range bias for small rooms). Monster rendering should respect this:

- Wave-N AI pool from engine → monsterSprites.ts resolves to tier-appropriate monster sprite(s)
- Variety: spawn different monsters within a tier (don't always Goblin_Mage for trash; rotate per encounter)
- Per-element flavor: where possible, match monster element-flavor to encounter element (Fire_Elemental for fire encounters; Crystal_golem for ice/earth; etc.)

This is presentation-only; engine logic unaffected.

### Step 5 — Tests + smoke + visual verification

- Pipeline unit tests (assembly / metadata generation per CreativeKind monster pack)
- Renderer unit tests (monster sprite resolution; tier classification; fallback handling)
- Smoke: load test season; verify monster sprites render across Wave 1-7 (trash / elite / mini-boss / boss tiers all visible)
- Existing 232+ tests preserved; npm run build PASS

### Step 6 — Attribution credits update

Per CreativeKind license (custom non-CC; legolas scout VERIFY provisionally clear — verify license terms when convenient):

- Add "Monster sprites by CreativeKind" to demo credits surface (existing surface added in v0.19)
- Cite license URI per scout's notes
- Drax discretion on credits format

### Step 7 — Friction findings + intermediate tag

- File or update `~/Games/reincarnated-demo/MONSTER_TRACK_INTEGRATION_NOTES.md`
- Per-monster integration findings; visual quality notes
- Recommendations for: which monsters from the unused 17+ packs might warrant future integration (VS2b expansion territory)
- Any CreativeKind VFX packs that could supplement Pimen/Pixogen if obvious gap-closers (Dark_Hole as void-variant? defer unless clear value)
- Tag: `drax/v0.20-monster-track-ingest-pipeline`
- AGENT_STATE.md updated
- Completion record at bottom filled

## Cross-seam considerations

- **Engine (rocket/gamora/star-lord)**: READ-ONLY; no engine changes — monsters are presentation layer
- **Rocket**: READ-ONLY; rocket's `wave_composition_rules.py` provides per-wave AI pool data; you consume it
- **Gamora**: READ-ONLY; sim mechanics (B11 sim-side geometry resolution per `gamora/v1.3-b11-sim-side-geometry-resolution`) unaffected
- **Star-lord**: READ-ONLY
- **Legolas** (READ-ONLY upstream): scout findings at `agentic_orchestration/research/catalogue/monster-track-vendor-scout-2026-05-16.md` informed today's acquisition; reference but do not modify
- **Elrond** (READ-ONLY): catalogue.db curation for CreativeKind monster line is DEFERRED to VS2b per "Mode B catalogue crawl on selected vendors" out-of-scope from scout; this dispatch ships demo-direct integration
- **Gandalf**: design-lineage owner of style register; if any CreativeKind monster visually drifts from HD-2D register, surface as finding (post-acquisition visual inspection)
- **Knight-rider**: notify at completion; closes the enemy-combatant rendering gap from drax v0.12 room/hallway dispatch + v0.19 wire-up

## Out of scope (explicit)

- **NO chierit / player-character work** (v0.19 covered)
- **NO Samurai work** (already-deferred)
- **NO room/hallway changes**
- **NO B11 demo / sim changes** (already complete)
- **NO engine schema changes** (presentation layer only)
- **NO CreativeKind VFX integration** (Pimen + Pixogen Lite cover VFX; CreativeKind VFX is supplementary; defer to VS2b decision)
- **NO ingest of all 30+ CreativeKind packs** — pick 10-13 representative subset; document deferred packs as VS2b candidates
- **NO Mode B catalogue crawl on CreativeKind** (VS2b territory)
- **NO new monster-vendor acquisitions** (CreativeKind covers the gap for VS2a)
- **NO per-monster customization paper-doll work** (monsters ship pre-styled)
- **NO procedural-monster generation** (separate VS2b+ design)

## Required reading

- `agentic_orchestration/research/catalogue/monster-track-vendor-scout-2026-05-16.md` (legolas scout; CreativeKind deep-dive)
- `canonical/story/style-register.md` (HD-2D-shaped pixel register lock)
- Your prior `drax/v0.18-character-track-ingest-pipeline @ 529139e` (pattern reference; structurally similar)
- Your prior `drax/v0.19-character-wire-up-void-attribution` (call-site wiring pattern + credits surface)
- `~/Games/reincarnated-demo/scripts/character-ingest/` (pipeline pattern reference)
- `~/Games/reincarnated-demo/src/visuals/characterSprites.ts` (renderer pattern reference)
- `reincarnated-engine/src/reincarnated/generation/wave_composition_rules.py` (wave AI pool data source)
- `reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disciplines #2 (smoke); #10 (empirical inspection over assumption); #11 (attribution: CreativeKind license citation)

## Acceptance criteria

- [ ] Monster-track ingest pipeline created (scripts/monster-ingest/ with assembly + metadata stages + runner)
- [ ] 10-13 CreativeKind monsters selected covering trash/elite/mini-boss/boss tiers
- [ ] Per-monster metadata.json populated
- [ ] Monster renderer integration in demo (monsterSprites.ts or equivalent)
- [ ] ENEMY_TIER_CHARACTER_MAP established
- [ ] Demo renders real monsters for enemy combatants (replaces primitives)
- [ ] Wave-composition integration: per-wave AI pool resolves to tier-appropriate monsters
- [ ] Existing 232+ tests preserved; npm run build PASS
- [ ] Credits surface updated with CreativeKind attribution
- [ ] MONSTER_TRACK_INTEGRATION_NOTES.md (or equivalent) filed
- [ ] Intermediate tag `drax/v0.20-monster-track-ingest-pipeline` cut
- [ ] AGENT_STATE.md updated
- [ ] Knight-rider notified at completion

## Tag policy

- **Intermediate tag:** `drax/v0.20-monster-track-ingest-pipeline` at the commit closing pipeline + integration + smoke pass.

---

## Completion record

**Completed:** 2026-05-16
**Intermediate tag:** `drax/v0.20-monster-track-ingest-pipeline @ 88a0dc3`

**Pipeline structure:**
- `scripts/monster-ingest/stage1_assemble.py` — copies canonical variant sheets from pre-extracted CreativeKind dirs
- `scripts/monster-ingest/stage2_metadata.py` — measures dims, derives layout, writes metadata.json
- `scripts/monster-ingest/run_pipeline.sh` — 2-stage orchestrator; 11/11 monsters assembled, 0 errors
- `scripts/monster-ingest/tests/test_pipeline.py` — 35 tests (all pass)
- Discipline #10 finding: 5 distinct directory patterns (A-E) across CreativeKind packs

**Monster subset selected (11 from 30+):**

| Tier | Slug | Source Pack | Element Flavor |
|---|---|---|---|
| trash | goblin-mage | Goblin_Mage_Creativekind | none |
| trash | mutant-skeleton | Mutant_skeleton | dark |
| trash | evil-eye | Evil_Eye | none |
| trash | sword-warrior | 8_sword_warrior__red | physical |
| elite | crystal-golem | Crystal_golem_creativekind | ice |
| elite | fire-elemental | Fire_Elemental_Creativekind | fire |
| elite | demon-mage | Demon_mage_creativekind | dark |
| mini_boss | lich | Lich_Creativekind | dark |
| mini_boss | hellfire-rhino | Hellfire_Rhino_Creativekind | fire |
| boss | angel-guardian | Angel_Guardian_Creativekind | holy |
| boss | god-of-lightning | God_of_Lightning_Light_Version_Creativekind | thunder |

**ENEMY_TIER_CHARACTER_MAP mappings + any adjustments:**
- `trash`: ['goblin-mage', 'mutant-skeleton', 'evil-eye', 'sword-warrior']
- `standard` (engine default): ['goblin-mage', 'sword-warrior'] — maps to trash visuals
- `elite`: ['crystal-golem', 'fire-elemental', 'demon-mage']
- `mini_boss`: ['lich', 'hellfire-rhino']
- `boss`: ['angel-guardian', 'god-of-lightning']
- `act_boss`: ['angel-guardian', 'god-of-lightning']
- Element-preference: fire→fire-elemental, ice→crystal-golem, dark→demon-mage, physical→sword-warrior

**Wave-composition integration approach:**
- `resolveMonsterSlug(tier, encounterElement, encounterSeed)` — element-preference first, then seed-based rotation
- `encounterElement` = combatant.dominantElement (from engine output) → visual variety per encounter element
- `encounterSeed` = slot index (i in loadWave loop) → 4 trash adds in one wave = 4 different monster types
- Engine AI pool data (wave_composition_rules.py tier assignments) → demo tier string → monsterSprites resolver
- Presentation-only: engine mechanics unaffected

**Visual register conformance findings:**
- Lich (176x128): firmly HD-2D-pixel. Per-animation sheets clean. CONFIRMED
- Crystal_Golem (168x141): HD-2D-pixel. Non-standard 141px height (not power of 2)
- Goblin_Mage (96x96): mid-to-HD-2D-pixel border; hand-drawn illustration confirmed
- Fire_Elemental (192x68): unusual 68px frame height; flat sideview aesthetic
- All 11 monsters: hand-drawn pixel art; no AI-generated content per product pages
- Cross-vendor coherence: CreativeKind VFX (Tier-1 in prior dispatches) + monster sprites same register

**Unused packs deferred for VS2b:**
- Dark_Soul_Creativekind — dark trash variant
- Evil_alien_creature_1/2/4 + Egg — swarmer/sci-fi archetype
- SpearWarrior, Warrior/Warrior_New_Color/Warrior_v2_with_jump — warrior variants
- blue_mage / red_mage / Archimage / Elemental_mage — additional caster elite variants
- Crystal_Wisp / Magic_Wisp_Pack — swarmer magical
- Fire_Lord_Creativkind — humanoid fire boss (strong VS2b candidate)
- God_of_Lightning_Dark_Version — dark lightning boss variant
- Angel_Mage_Creativekind / angel_v1 — secondary boss variants
- Demon_mage_nopreviewgif_Creativekind — alternate Demon_Mage pack
- VFX packs: Dark_Hole (void-variant), Energy_Ball, Fire_attack, Lightning_horizontal/vertical, sword_sprite

**Notes for knight-rider:**
- Enemy-combatant rendering gap (from v0.12 room/hallway dispatch) is closed. VS2a presentation layer is now ~feature-complete: player sprites (chierit v0.19) + monster sprites (CreativeKind v0.20) + VFX (Pimen + Pixogen Lite).
- Visual inspection needed: DEFAULT_MONSTER_SCALE=0.28 is estimated. Matt should run demo with a season containing fire/dark/ice/physical elements to see each monster tier render. Scale tuning likely needed per monster.
- God-of-Lightning: 256x256 single-frame only. The pack may have more animation content not yet surfaced — worth inspecting if the boss-tier encounter feels static.
- Combined-sheet monsters (Crystal_Golem, Mutant_Skeleton, Evil_Eye, Hellfire_Rhino, Angel_Guardian): play all frames in sequence. This works for VS2a but per-animation slicing (idle/attack/death states) would require frame-boundary documentation from vendor or manual inspection. File as VS2b item if per-state monster animation is desired.
- TODO(drax) items filed in MONSTER_TRACK_INTEGRATION_NOTES.md (5 open items).
