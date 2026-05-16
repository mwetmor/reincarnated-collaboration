# Demo1 Progress Tracker

**🔗 Live demo:** https://reincarnated-demo.vercel.app  *(shipped 2026-05-11, v1.2)*

**Last updated:** 2026-05-11 (🎉 **demo1 v1.2 shipping** — final cherry-on-top phase complete; sprite VFX integrated; Matt: "5x more enjoyable"; Vercel auto-deploying; engine queue (file 28) is the only major item remaining when project resumes)

## Re-playtest after Phase 4.5 (2026-05-10)

Matt played 3 classes through 7-wave gauntlet:

**Trenchwind Pitch-Caster (fire mage, mana):** ✅ Cleared in ~2 minutes. AI fixed; fights "fun"; used 2 mana potions plus between-wave heals. AI still slightly slower than player on cooldowns but acceptable.

**Trench Gale Brawler (stamina-as-resource):** ❌ Stuck at Wave 4 Mini-Boss. Stamina regen now sustainable; could spam abilities. But Mini-Boss had high defensive regen + low damage; couldn't push it below 80% HP. Eventually gave up. Matchup imbalance, not a bug.

**Abyssal Basalt Monk (mana, zero-cooldown fist):** ⚠️ Beat Wave 4 Mini-Boss using mana potions to fuel Basalt Wind Fist (0-cooldown spam). Died at Wave 5 Boss because out of potions. Class identity is "mana-battery": fist drains mana fast; potion-dependent for sustain.

**Findings:**
- Phase 4.5 fixes hold up — AI fires aggressively, heals target self, stamina/focus/combo/rage all feel right
- Player observation: combat is too frantic at current cooldown values; "spammed all 6 keys" because cooldowns kept coming up
- Player suggestion: slightly multiply cooldowns globally + map space bar to lowest-cooldown ability (Diablo-style)
- Balance observation: Trench Gale Brawler may have penetration gaps; Mini-Boss may have over-tuned regen
- Balance observation: Abyssal Basalt Monk's mana-battery design is interesting but potion-dependent

## Phase 4.5 — Polish pass before Phase 5 (post-playtest fixes)

**Status:** ✅ Complete (2026-05-10)

Triggered by family playtest #1 findings. Investigation phase before code (good engineering discipline). Seven bugs caught, all in resource math:

- [x] **AI cadence:** changed from 0.6-2.0s fixed cadence to 0.1s fast-tick. AI now fires any ready skill within 0.1s of cooldown availability. Cooldown-bound, not silence-bound.
- [x] **Heal targeting:** `showImpact()` takes explicit caster + target positions. Heal/shield numbers always appear at caster, regardless of geometry.
- [x] **Mana base regen** (Phase 4.5 #3): engine uses `5.0 × (1 + max(int,wis) × 0.002)`, not `max_mana × 0.01 × ...`. Fire mage: 12.5/sec total (was 9.4/sec). Primary fully sustained at canonical gear tier.
- [x] **Stamina-as-resource:** pool=150 flat, regen=20/sec flat. Was 1.72/sec — 11.6× too slow. Trench Gale Brawler was unplayable; now sustainable.
- [x] **Focus:** starts full (100), decays −5/sec passively, restores +10 per skill use. Was building from 0 at +1/sec — completely backwards direction.
- [x] **Combo:** max pool=5 (not 100). Builds 1 per primary_attack only. Skills costing >5 are intentionally unreachable in single window (design intent confirmed from engine source).
- [x] **Rage:** flat gains: +10 per hit dealt, +5 per hit taken (not damage-percentage-scaled).
- [x] 43/43 tests passing. TypeScript clean. PRD build updated. Tagged v0.4.5-phase4.5.

**Findings:**
- Fire mage was correctly tuned to be a near-continuous-cast class (0.5s primary cooldown is real and intentional). The "OP" feel is largely conflated with the AI passivity.
- Each non-mana energy type had at least one math error in the demo. `_ENERGY_CONFIGS` in engine source (`combatant.py:229`) is the ground truth; `damage_formula.md` has multiple errors and is unreliable for resource math.
- Per-energy-type identity is now genuinely mechanically distinct: mana (passive regen, tactical), stamina (passive regen, physical flavor), focus (decay + restore on use, rapid-fire tempo), combo (build to 5 + spend, patience pattern), rage (build from 0, reactive).

Live checklist mirroring `collaboration-handoff/24-cli-demo1-implementation.md`'s 6-phase structure (plus Phase 7 stretch). Update as phases land.

**How to use:** check sub-goals as the demo CLI agent reports completion. Each phase ends with a browser-runnable milestone — check that box only when the demo runs at port 4173 (PRD preview) successfully at that phase's level.

---

## Phase 1 — Project setup + scene + JSON loading + damage formula (~3-5 days)

**Status:** ✅ Complete (2026-05-10)

- [x] Repo + tooling setup (package.json, tsconfig, vite, vitest)
- [x] Pixi.js application basics (canvas, stage, ticker)
- [x] TypeScript type definitions matching engine exports
- [x] JSON season loader (cross-reference resolution)
- [x] Damage formula in TypeScript (crit, block, armor, DoT)
- [x] Audio system stub (Howler.js loaded, silent operation)
- [x] **Browser-runnable milestone:** scene visible, no errors

**Notes from Phase 1 report:**
- 40 unit tests passing
- Schema validated against actual JSON (caught: 2 act-bosses not 3; carried_gear is dict not array; 15 geometry types vs design_context.md's 8)
- Two open questions resolved: MANA_REGEN_SCALING (find in engine source) + monster damage modifier (1.0 for gauntlet monsters)

---

## Phase 2 — One ability end-to-end (~3-4 days)

**Status:** ✅ Complete (2026-05-10)

- [x] Input system (keyboard events, key state tracking)
- [x] Ability resolution pipeline (cooldown check, resource cost, target validation)
- [x] One ability fully wired (chose ranged_physical / fire projectile)
- [x] HP bar updates on damage
- [x] Cooldown indicator on hotbar
- [x] Resource cost deduction
- [x] Status effect (burn DoT) ticks correctly
- [x] Visual feedback (damage numbers, hit flash, projectile animation)
- [x] Audio: stub SFX on ability cast (still procedural; Tier 2 deferred to Phase 3)
- [x] **Browser-runnable milestone:** Press ability key → opponent takes damage → can win/lose by repeating ✓

**Phase 2 report highlights:**
- 42 unit tests passing
- Combat math validated: 690 dmg / 0.42s cooldown / 1639 DPS / 10s boss kill from primary alone
- Resolved Phase 1 open question: **MANA_REGEN_SCALING = 0.002** (found in math_model.py:16; multiplicative formula, not additive as `damage_formula.md` claimed)
- Dodge chance cap at 0.60 also corrected (was wrong in `damage_formula.md`)
- VFX shipped: projectiles with eased travel, AoE expand rings, melee X-slashes, hit flashes, floating damage numbers (crit gold + larger; heal green; miss grey)
- Combat HUD with cooldown timers, element-colored accents, win/lose overlay, restart-on-R
- Player loads with their class's canonical_gear; act-boss has theirs equipped — canonical-loadout architecture is live in browser ✓

**Notes for engine team (non-blocking):**
- `damage_formula.md` has at least two errors (mana regen formula, dodge cap). Worth a doc-correction pass in a future engine session. Demo works correctly because the agent went to engine source for ground truth.

---

## Phase 3 — All ability types + resource systems + status effects (~5-7 days)

**Status:** ✅ Complete (2026-05-10)

- [x] All 16 geometry types in actual JSON have distinct visuals (no silent failures; logged-warning fallback for unexpected types)
  - [x] projectile (animated circle, eased travel)
  - [x] ranged_physical (rotating arrow)
  - [x] single_target (instant element flash) — most common (100 occurrences)
  - [x] melee_strike (X-slash + secondary)
  - [x] melee_arc (fan arc sweep)
  - [x] circle / ground_targeted_circle (expanding ring at target)
  - [x] ground_slam (expanding ring at caster)
  - [x] cone (filled fan caster→target)
  - [x] line (directional rectangle)
  - [x] self_buff / self_cast (concentric rings)
  - [x] aura (persistent pulsing ring)
  - [x] totem (pulsing cross marker)
  - [x] beam_channel (animated line)
  - [x] teleport (starburst flash)
- [x] Resource systems per energy_type:
  - [x] mana (passive regen, INT/WIS-scaled multiplicative formula)
  - [x] stamina-as-resource (passive regen, VIT-scaled)
  - [x] focus (charges 1/sec from 0; precision burst pattern)
  - [x] combo (builds 1 per hit landed; finishers spend; **0-cost primary** — design insight)
  - [x] rage (infrastructure ready; no rage class in current 5 seasons)
- [x] Status effect glows (Pixi.js GlowFilter, priority order: stun > silence > burn > bleed > chill > root)
- [x] Full ability hotbar with cooldowns + costs + element-colored accents
- [x] Audio: per-(geometry × element) procedural Tier 1 + Tier 2 file-mapping wired (drop file → auto-replaces)
- [x] Class selector UI (8 playable classes, 2-column grid)
- [x] **Browser-runnable milestone:** Pick any class → fight placeholder → all 6 abilities fire distinctly with element-themed visuals + audio + status glows ✓

**Phase 3 report highlights:**
- All 16 actual geometry types handled (vs 8 in design_context.md sketch and 15 estimated in Phase 1)
- Combo system insight: it's a "free builder + paid finisher" pattern, structurally different from depletion-style resources
- Rage gap finding: 5 generated seasons produced zero rage classes (worth tracking; could be sample noise or generator bias)
- Tier 2 audio asset path is wired (`/assets/audio/sfx/ability_{geometry}_{element}.mp3`); drop files anytime to upgrade from Tier 1 procedural

---

## Phase 4 — Wave-structured gauntlet + AI (~6-8 days)

**Status:** ✅ Complete (2026-05-10) — tagged v0.4-phase4

**Phase 4 report highlights:**
- 7-wave gauntlet for season 001001 (10 opponents total: 3 trash → 2 standard → 1 elite → 1 mini-boss → 1 boss → 2 act-bosses)
- Tiered AI: simple (trash always-attacks) / smart (sorts by damage, 20% randomness) / optimal (full rotation, low-HP heals, ailment gap-fills)
- AI cadence scales by tier: trash 1.4-2.0s / act-boss 0.6-0.9s
- Monster infiniteResource flag — monsters are cooldown-limited, not mana-limited (separates monster instinctive combat from player tactical resource management)
- Combat log toggleable with H key; color-coded by event type
- Potion drops per tier (trash 1H, scaling up to boss/act-boss 3H+2M); auto-collect after 1.8s; Q/E to use 50% restore; glug SFX
- Between-wave screens with HP refill, potion count, next-wave preview
- Win/lose screens with class-aware retry / class-select buttons

**Findings worth tracking:**
- Wave 5 boss (Basalt Thrumcolossus, 176K HP) is ~107-second fight from primary-only DPS. Acceptable for boss-tier intentionality; family playtest will reveal whether it drags
- Gauntlet filter (`.opponents.length > 0`) defensively handles future seasons that might not generate all tiers

**This is the first family-playtest-worthy milestone.**

- [ ] Combatant construction:
  - [ ] Monster combatants from monsters.json (load by tier)
  - [ ] Act-boss combatants from classes.json (where is_act_boss=true)
- [ ] Wave orchestration state machine:
  - [ ] Wave 1: 2-3 trash monsters (sequential)
  - [ ] Wave 2: 2 standard monsters
  - [ ] Wave 3: 1 elite monster
  - [ ] Wave 4: 1 mini-boss
  - [ ] Wave 5: 1 boss-tier monster
  - [ ] Waves 6-7: 2 act-bosses (drops gear in Phase 5)
- [ ] AI state machine (per opponent: cooldown-aware, archetype-biased)
- [ ] **Combat log UI** (scrolling timestamped events, color-coded, minimize/expand toggle)
- [ ] **Name bars + subtitles:**
  - [ ] Player: name + class subtitle
  - [ ] Monster: name + tier subtitle
- [ ] **Potion drops on kill:**
  - [ ] Trash drops: 1 potion (health or mana)
  - [ ] Standard drops: 1-2 potions
  - [ ] Elite/mini-boss drops: 2-3 potions
  - [ ] Boss drops: 3-5 potions
  - [ ] Pickup auto OR press F
  - [ ] Each potion heals 50% max pool
  - [ ] Bound to keys (Q for health, E for mana)
- [ ] Audio: hit/damage/death SFX wired (Tier 2 curated or Tier 1 procedural)
- [ ] Audio: "glug" SFX on potion use
- [ ] Visual: Tier 2 composed sprites if integrated; else Tier 1 procedural
- [ ] Win/lose flow + restart functional
- [ ] **Browser-runnable milestone:** Full 7-wave gauntlet playable end-to-end

**Family playtest #1 happens here.** Take notes on:
- Does the gauntlet feel like a fight?
- Are tier transitions noticeable?
- Do abilities have appropriate SFX feedback?
- Which classes feel best to play?

---

## Phase 5 — Boss-carried gear drops + inventory + equip + UX fixes (~4-6 days)

**Status:** ✅ Complete (2026-05-10) — tagged v0.5-phase5

**STATIONARY demo1 loop fully functional.**

- [x] **UX Fix #1: Cooldown global multiplier (1.4×)** applied symmetrically. Fire mage primary 0.421s → 0.589s effective. Tactical pacing, not frantic.
- [x] **UX Fix #2: Space bar = primary attack** — `role === 'primary_attack'` skill always at index 0; Space + key 1 both fire it; "SPC" label + "PRIMARY" badge on slot 0
- [x] **UX Fix #3: Cooldown visualization** — ready skills pulse with element-colored glow (slot 0 brighter); locked skills show dense dark overlay + amber timer; no-resource skills dim. Ready/locked is at-a-glance obvious.
- [x] Drop visualization on act-boss defeat (4 ground icons per defeat)
- [x] **Color-tiered ground glow:**
  - [x] Common: no outline
  - [x] Uncommon: subtle gray outline
  - [x] Rare: blue outline + gentle pulse
  - [x] Epic: purple outline + stronger pulse
  - [x] Legendary: `color_signature` hex glow + pulsing width + inner fill
- [x] Hover tooltips show name, tier, stats
- [x] Drop chimes per tier (ascending triad legendary, 2-note epic, single rare)
- [x] InventoryState: 4 equipped slots + stash; player starts with canonical class gear
- [x] Equip validation: `stat_requirements` checked against base class stats; short-form keys (`str`/`dex`) correctly mapped to `strength`/`dexterity`
- [x] 2H weapon clearing off_hand slot handled
- [x] `player.updateGear()` recomputes aggregate stats — HP bars, cooldowns, damage all live
- [x] Inventory panel UI: I/F keys or "Inspect Gear" button on between-wave screen
- [x] Equipped slots with Unequip; stash with Equip (warning if stat-locked); inline failure messages
- [x] Between-wave flow: after Wave 6 defeat, "Inspect Gear (I)" overlay; can equip → SPACE to advance to Wave 7 with upgraded stats
- [x] **Browser-runnable milestone:** Full stationary demo1 loop — pick season → pick class → fight 7-wave gauntlet → defeat act-bosses → carried_gear drops → equip between waves → fight again ✓

**Phase 5 report highlights:**
- Cross-class equip refusal works correctly (Abyssal Gale Archer's bow requires DEX 82; fire mage with DEX 18 blocked, item goes to stash — matches cross-class smuggling design intent)
- Real-time stat updates are zero-cost via getter pattern — pays off in Phase 6 when movement touches stat reads
- Mechanically-meaningful upgrade flow: legendary weapon swap from Wave 6 boss meaningfully changes Wave 7 fight

**Family playtest #2 happens here.** Take notes on:
- Do drops feel exciting? Do legendaries land?
- Is the equip flow intuitive (I to inspect, click to equip, X to close)?
- Does the upgrade meaningfully change Wave 7?
- Is the new cooldown multiplier (1.4×) the right pace? Too slow? Too fast?
- Is the space-bar-as-primary feel right? Is the cooldown visualization clearer?
- What gear was most memorable?

---

## Phase 6 — Movement + positional combat (~1.5-2 weeks) — NEW

**Status:** ✅ Complete (2026-05-10) — tagged v0.6-phase6, pushed

- [x] Player WASD + Arrow movement; tickPlayerMove() at 60 FPS; diagonal normalized; clampToArena()
- [x] Movement speed derived from range_profile (no field in JSON): player close=200, medium=160, long=130 px/s
- [x] NPC AI movement state machine per range_profile (independent of 0.1s ability tick):
  - [x] close — approaches to 90px (melee adjacency); charges directly
  - [x] long — kites at 440px hover; retreats when player closes to 200px
  - [x] medium — orbits at 280px; backs off if player crowds inside 200px
  - [x] default/trash — simple approach to 280px
- [x] AI ability tick range pre-filter — pickAISkill() rejects melee skills until AI ≤120px (no more "casting melee from across the arena")
- [x] Auto-attack fallback (already in player code path) tightened to fire only within melee range
- [x] Positional hit detection via isInRange():
  - [x] melee_strike / melee_arc / ground_slam → ≤120px
  - [x] self_buff / self_cast / aura / totem / teleport → no range gate
  - [x] all other geometries → ≤580px
  - [x] Player skill activation range-gated at cast time; out-of-range presses fail silently
  - [x] **VFX positions captured at cast time** — projectile visuals travel original cast-time path regardless of target movement; gives evasion *feel* without needing travel-time hit detection (good convention; future effects follow)
- [x] Arena bounds: x: [116, 1164], y: [156, 604]; spawn player x≈316 / opponent x≈964
- [x] HUD stays screen-anchored; camera fixed overhead (centered-on-player deferred to Phase 7 if needed)
- [x] Gear/potion drops spawn at opponent's actual death position (captured before loadOpponent reset); potion-use floating numbers at player's current position
- [x] isPaused freeze covers movement; AI movement only runs in active combat state
- [x] Cooldown multiplier 1.4× from Phase 5 still applies
- [x] **Browser-runnable milestone:** ✓ — Player + NPCs move; positional combat works; ranged kiting and melee approach are both functional

**Phase 6 report highlights:**
- No `movement_speed` field exists anywhere in engine JSON (classes, monsters, skills) — speeds derived entirely synthetically. If engine ever adds the data, it's a one-file update.
- No `range` or `area_radius` field on skills either — only `geometry_type`. Range constants in movement.ts are synthetic.
- AI advisory positioning (no collision repulsion) — overlap is allowed, didn't visually look wrong in playtest.
- Beam-channel break rule simplified for Phase 6: breaks when target moves >60px lateral from cast-time aim line. Low priority to revisit unless beam classes feel wrong.

### Family playtest #2.5 (Phase 6) — 2026-05-10

**Wins:** Movement + positional combat work; ranged vs melee feel different; pause invariants hold.

**Issue surfaced:** combat feels cramped. Arena is 1048×448 px; long-range AI kite hovers at 440px (barely 2× across); melee NPCs move at player speed (200), no escape window. Matt feedback: "rooms should be bigger and the monsters a bit slower."

## Phase 6.1 — Arena + AI speed tuning (~half day)

**Status:** ✅ Complete (2026-05-10) — tagged v0.6.1-tuning, pushed

- [x] Arena scaled 1.5× → x: [116, 1688], y: [156, 828]; canvas 1800×944
- [x] AI_SPEED_MULTIPLIER = 0.85 applied at single chokepoint in tickAIMove
- [x] AI distance thresholds scaled with arena (long kite 440→660, medium drift 280→420, default approach 280→420)
- [x] Non-melee hit-detection RANGE_CAST scaled with arena (580→870); melee unchanged (120, absolute)
- [x] HUD/panels/combat log auto-adapt via CANVAS_WIDTH/HEIGHT constants
- [x] **Browser-runnable milestone:** ✓ — arena bigger and feels right for ranged kiting
- [x] Tag v0.6.1-tuning; pushed

**Phase 6.1 playtest #2.5 finding:** arena scale fixed cramped feeling; AI speed perception unchanged despite 0.85× multiplier (carried into Phase 6.2).

## Phase 6.2 — Elliptical arena + harder speed retune + geometry VFX scaling (~half day)

**Status:** ✅ Complete (2026-05-10) — tagged v0.6.2-tuning, pushed

- [x] **Elliptical arena** — clampToEllipse() via parametric projection (normalize displacement in unit-ellipse space, clamp norm ≤ 1, scale back); floor visual replaced with drawEllipse + boundary ring; both spawns verified at nlen=0.745 (well inside)
- [x] **Speed retune** — AI_SPEED_MULTIPLIER 0.85→0.75; player speeds bumped 200/160/130 → 220/180/150; chase margin (close) 30→55 px/s
- [x] **Geometry VFX scaling:**
  - cone: 90px → 784px (= ELLIPSE_RX, half major axis)
  - circle / ground_targeted_circle: 80px → 200px radius (≈¼ major axis)
  - ground_slam: 70px → 150px radius (proportional to melee adjacency)
  - line / melee / self / beam: unchanged (absolute or already correct)
- [x] **Browser-runnable milestone:** ✓ — arena elliptical, cone VFX appropriately sized
- [x] Tag v0.6.2-tuning; pushed

**Phase 6.2 playtest finding:**
- ✅ Arena elliptical and fits
- ✅ Cone VFX appropriately sized
- ⚠️ AI movement speed STILL not perceived as changed (second consecutive tuning pass with no felt effect despite 25 px/s margin increase). **Suspicious — needs investigation, not another tuning pass.** Recommended verification before Phase 7: add console.log to tickAIMove to confirm AI_SPEED_MULTIPLIER is actually being consumed in the velocity path. If math is right, defer; if multiplier isn't being applied, one-line fix.

## Phase 7 — Combatant rendering per LLM/class context (~1 week)

**Status:** ✅ Complete (2026-05-10) — tagged v0.7-phase7, pushed

**Tier decision:** **Tier 1.5** (enhanced procedural Graphics) shipped in lieu of true Tier 2 (Kenney sprite atoms). File 25 doesn't exist; no Kenney pack downloaded; CLI made the pragmatic call to ship functional rendering without external dependencies. archetypeRenderer.ts is the swap point for Tier 2 when assets land later.

- [x] All 19 archetype tags mapped (zero procedural fallback). Coverage: fire/water/earth/wind mages, hybrid_mage (most common at 11), 4 element controllers, hunter, physical_warrior/skirmisher, rogue, plus 6 monster archetypes (brute, caster, controller, sniper, swarmer, tank)
- [x] Body types: mage / archer / warrior / skirmisher / brute
- [x] Weapon overlays: staff / orb / bow / sword / shield / club / daggers
- [x] Element accent particles: 2-6 orbiting per archetype, color-tinted by element
- [x] Boss tier scaling: trash 0.7-0.8×, standard/elite 1.0×, mini-boss 1.2×, boss/act-boss 1.4-1.6× with extra particle aura
- [x] Movement integration: facing flip on direction; 2-frame bob animation
- [x] Status-effect glows from Phase 3 still render correctly on top
- [x] 60 FPS maintained at peak combatant count
- [x] **Browser-runnable milestone:** ✓ — sprites archetype-distinct at a glance

**Phase 7 playtest #4 confirmed:**
- ✅ Sprites match archetype/flavor text
- ✅ Elemental accents working
- ✅ Sprites face walking direction
- ✅ Monsters vary in size by tier

**Phase 7 report highlights:**
- archetypeRenderer.ts (270 lines) — clean integration point for Tier 2 swap later
- Zero archetypes fell back to procedural
- Architecture: bodyContainer + bossAura + orbitalParticles + bobbingPhase + auraPhase + tier in CombatantSprite interface
- tickCombatantAnimation() unified call for particles + bob + facing + boss aura

**Pre-Phase-7 speed verification result:** Math verified correct (chase margins close 55 / medium 45 / long 37.5 px/s). Implementation is right; perception gap is the issue. 55 px/s margin in 1568 px arena = ~28 sec to lap AI. Three tuning knobs available later: push multiplier to 0.60, add AI engagement wind-up, or asymmetric player-speed bump.

**Pending decision (deferred to post-Phase-9):**
- Tier 2 sprite atoms — Kenney pack choice (Tiny Heroes / Dungeon Tileset / LPC) + target resolution (32 / 48 / 64 px). Tier 1.5 ships demo1; Tier 2 is a small polish pass anytime later.

## Phase 8 — Polish + multi-season + per-season soundtrack + full Diablo UI (~8-12 days planned) — REORDERED + EXPANDED 2026-05-10

**Status:** ✅ Complete (2026-05-10) — tagged v0.8-phase8 (re-pointed after hot fix), pushed, playtest-verified. Tier 2 sprites split out to Phase 8.1.

- [x] **Season selector** — 5 tiles with anchor name, tagline, element pills, per-season chrome
- [x] **Lazy-load** — full season loaded on tile selection; metadata pre-loaded at startup
- [x] **HP + resource globes** — Diablo-style fluid fill, ornate frame, low-HP pulse
- [x] **Per-season music** — Howler streaming with crossfade; M toggle; +/- volume
- [x] **Class selector back button** + **end-of-encounter "New Season" / "Different Class"** buttons
- [x] **Belt/potion bar, ornate hotbar frames, character portrait, in-game per-season chrome tinting** — verified shipped in playtest (2026-05-10). Phase 8 spec fully met except Tier 2 sprites.
- [⏭️] **Tier 2 sprite atoms** — explicitly punted by CLI to Phase 8.1 (pack-decision was a stop-and-surface gate; CLI chose to ship multi-season work first rather than block on research)

**Path migration finding (worth memorializing):**
- Music + SFX moved from `/public/assets/audio/...` to `/public/audio/...` to resolve a git/macOS case-insensitive FS conflict. A stub file named `Assets` existed in remote that blocked rebase against the case-equivalent `assets/` directory.
- Eliminates the custom Vite plugin that handled `/assets/` routing; uses Vite's standard `public/` static-dir convention.
- **Runtime path is now `/audio/music/season_NNNNNN.mp3`** (not the originally-spec'd `/assets/audio/music/...`).
- Future demo work and any docs should reference the new path.

**Hot-fix landed (2026-05-10) — ticker state-guard regression:**
- Bug: `main.ts:697` ticker callback only guarded against `'selecting'` state; Phase 8's new `'season_menu'` state slipped through and hit actor-sprite code with undefined refs. PRD hung on "Loading season data..."; dev showed black screen.
- Fix: one-line change from `topState === 'selecting'` (blacklist) to `topState !== 'gauntlet'` (whitelist). Future-proof against any new non-gauntlet state.
- Pattern worth keeping: whitelist beats blacklist for state guards.
- Tag v0.8-phase8 re-pointed at the fix (single source of truth).
- Lesson for future phases: **acceptance criteria need execution-verified, not diff-verified.** Multi-season smoke test was specced in Phase 8 as a workstream but apparently not actually run; running it once would have caught this immediately. Phase 8.1 prompt should require a real smoke-test pass before tagging.

## Phase 8.0.1 — Demo bug bundle (pre-Phase-8.1) (~half day)

**Status:** 🟡 Code shipped but unverified — tagged v0.8.0.1, pushed; smoke test pending Matt's playtest; chill fidelity follow-up flagged

- [x] **Music fade** — Howler html5-mode timing fix: `play()` then `fade(0, target, duration, id)` inside `onplay` where sound ID is live. `fadeStarted` flag prevents double-fire.
- [x] **Speed (third pass)** — AI_SPEED_MULTIPLIER 0.75 → 0.55. New AI_ENGAGEMENT_WINDUP=0.7s exported from movement.ts; `aiWindupRemaining` timer reset in `loadOpponent()` per wave; game loop decrements; gates tickAIMove until 0. AI abilities fire during windup. Close chase margin: 99 px/s (was 55).
- [⚠️] **Chill on movement** — slowFactor getter shipped, BUT hardcoded 0.70 per chill stack instead of reading each chill's `slow_percent` param from JSON. Practical impact: chills with slow_percent=0.40 should produce 60% velocity but produce 70% (gentler than spec); chills with slow_percent=0.23 should produce 77% but produce 70% (harsher). Mean roughly OK by accident; individual abilities all off. **Follow-up fix needed: `factor *= (1.0 - chill.params.slow_percent)` per engine `combatant.py:163-170`.**
- [x] **Root on movement** — isRooted getter shipped; tick functions early-return if rooted (velocity=0)
- [x] **Smoke test** — Matt's playtest confirmed speed locked in. Surfaced 3 remaining bugs (music loop, knockback, chill not slowing); flow into Phase 8.0.2.
- [⏭️] Chill fidelity follow-up — bundled into Phase 8.0.2

**Phase 8.0.1 playtest results:**
- ✅ Speed feels great now (third pass landed)
- ✅ Music plays cleanly (fade-on-load fix worked)
- ❌ Music doesn't loop when track ends → Phase 8.0.2
- ❌ Knockback doesn't push or stagger → Phase 8.0.2 (engine had no consumer; demo is first)
- ❌ Chill glow fires but velocity unchanged → Phase 8.0.2 (wiring issue between active_effects and slowFactor)

## Phase 8.0.2 — Music loop, knockback, chill wiring (~half day planned, ~partial ship)

**Status:** 🟡 Partial ship — only visual fix landed; mechanical wiring + music loop + knockback NOT shipped despite incomplete CLI report claiming "wiring was correct"

**What actually shipped in 8.0.2:**
- ✅ GlowFilter shader conflict diagnosed (`@pixi/filter-glow@5.2.1` × `pixi.js@7.4.2`); replaced with hand-drawn Graphics ring as actor child (now tracks position)
- ✅ Type system `slow_percent` added to SkillEffectParams
- ✅ `slowPercent` field on ActiveAilment with engine-faithful slow_percent reading (replaced 8.0.1's hardcoded 0.70)
- ✅ Refresh logic improved: re-applying chill now uses Math.max for duration (extends rather than shortens — bug catch)

**What was claimed but is NOT working per Matt's playtest:**
- ❌ Chill velocity slow — visual is right, mechanical effect zero
- ❌ Root velocity stop — visual is right, mechanical effect zero
- (CLI's "addAilment path and slowFactor/isRooted wiring were correct the whole time" claim contradicted by playtest)

**What was silently dropped from 8.0.2:**
- ❌ Music loop fix — never shipped; track still ends and stops
- ❌ Knockback implementation — never shipped; ailment has no effect

**Diagnostic-discipline note:** third consecutive sub-phase (Phase 8 ticker, 8.0.1 chill hardcode + skipped smoke test, 8.0.2 partial ship) where work was claimed complete without execution-verification. Phase 8.0.3 prompt explicitly requires console-verified observations per fix before tagging.

## Phase 8.0.3 — Music gap, knockback, resisted feedback (~half day)

**Status:** ✅ Complete (2026-05-10) — tagged v0.8.0.3-partial; Matt's playtest confirmed all three bugs working ("huge win, everything worked exceptionally well"); promote to v0.8.0.3 by ask to CLI

- [x] **Music gap fix** — Web Audio mode swap (`html5: false`); gapless looping verified via absent onend event over 3+ loops
- [x] **Knockback implementation** — pioneering positional work (engine has no consumer); PX_PER_KNOCKBACK_UNIT=60; lerp over 0.2s; stagger gates velocity + ability cast; clamp to ellipse; dust VFX + screen-shake
- [x] **Resisted/applied visual feedback** — actor-child ring on success; "Resisted!" grey floater on miss; console-log application results
- [x] **Process discipline win** — CLI used partial-tag protocol (tag as `-partial` when interactive verification pending; promote to full tag after Matt verifies); broke the 3-sub-phase "tag-before-verify" anti-pattern; PROTOCOL TO KEEP for all future phases

**NOT in 8.0.3 scope (engine queue):**
- Per-skill ailment chance scaling (high-cost = 100%, low-cost = <35%) — Matt's design intent for engine team
- WIS-on-heal multiplier raise — heal balance feels too gentle at current 0.002× per WIS

- [ ] **Music loop** — Howler `loop: true` config (separate from Phase 8.0.1's fade timing fix)
- [ ] **Knockback** — pioneering demo implementation; engine has knockback in AILMENT_NAMES but NO consumer (engine is positional-stateless per Phase 3 memorialization). Demo is first real consumer:
  - PX_PER_KNOCKBACK_UNIT = 60 (tunable); push 200-440 px range
  - Push along attacker→defender vector over ~0.2s lerp
  - Stagger gates velocity AND ability cast for stagger_seconds (0.3-0.9 range)
  - Clamp to arena ellipse; small dust VFX + screen-shake on impact
- [ ] **Ailment system structural fix** — Matt's 2nd diagnostic round revealed: BOTH chill AND root show the visual circle but no effect, AND the circle doesn't follow the enemy. Diagnosis: Phase 3's status-effect "system" was actually a one-shot world-positioned VFX, not state-driven. `active_effects` was never populated for ailments. Three-part fix:
  - Populate `active_effects` when ailments resolve (chill/root/burn/bleed/knockback/silence) with params + duration_remaining; tick down each frame; remove on expiry
  - Render glow as child of actor's Pixi container (tracks position automatically); lifecycle tied to active_effects entries
  - Phase 8.0.1's slowFactor + isRooted getters then work correctly
- [ ] **Chill fidelity** — bundle 0.70 hardcode → JSON slow_percent fix into the same pass
- [ ] **CLI runs smoke test** in its own dev env before tagging — anti-pattern from Phase 8 + 8.0.1 needs to break here
- [ ] Tag v0.8.0.2; push

**Process lesson reinforcing Phase 8's:** "tag before smoke test" is a recurring anti-pattern. Phase 8.1 prompt should explicitly require the CLI to run the smoke test itself in its dev environment AND report concrete observations (e.g., "console clean across all 5 seasons; chill verified slowing Wave-2 standard NPC by ~30%; root verified fully stopping Mini-Boss") before tagging.

**Phase 8 playtest also surfaced an engine-side bug** (out of scope for 8.0.1): combo skill costs miscalibrated against pool size 5. 12/24 combo skills cost 13.7-30 — uncastable. Engine generator likely calibrated for old pool=100 value. Logged in engine state findings.

## Phase 8.1 — Tier 2 LPC sprites (~3-5 days planned, took longer due to LPC layout discovery)

**Status:** ✅ Complete (2026-05-10) — tagged v0.8.1, pushed, 5/5 archetype coverage confirmed in playtest

**5/5 archetype coverage with pre-composed LPC characters:**

| Archetype | Sprite | Format | License |
|---|---|---|---|
| mage | necromancer.png | 832×1344, 21-row full LPC | CC-BY-SA 3.0 |
| warrior | warrior.png (Baldric) | 576×256, **walk-only 4-row** | CC-BY 3.0 |
| archer | adventurer.png | 832×1344, 21-row full LPC | CC-BY-SA 3.0 |
| skirmisher | adventurer.png (shared with archer) | same | CC-BY-SA 3.0 |
| brute | brute.png (LPC Barbarian) | 576×256, **walk-only 4-row** | CC-BY-SA 3.0 |

**Architecture:** `BODY_SPRITE_CONFIG: Record<BodyKind, BodySpriteConfig>` — per-archetype config object; Phase 8.2 extends this same record with animation rect data per archetype. Clean swap point.

**Lessons captured:**
- Sanderfrenken Universal LPC Generator outputs base body LAYERS (intentionally headless, designed for compositing). Pre-composed full LPC characters from OpenGameArt are the correct asset class for direct use.
- LPC layout varies per source pack; ALWAYS empirically confirm idle frame via PIL row extraction or visual inspection before assuming row indices.
- Three iterations to land (y=512 wrong, y=640 wrong, pre-composed approach correct) — diagnostic approach lost time. Pattern: when first assumption fails, inspect-not-guess.
- ATTRIBUTION.md documents the CC-BY-SA chain.

**Phase 8.2 considerations from 8.1's deliverables:**
- Warrior + brute walk-only sheets have no slash/thrust/cast/shoot rows. Phase 8.2 uses **Option A** (weapon-overlay animation only; body stays in idle for those archetypes). Source-replacement queued as potential Phase 9 polish if disparity bothers playtest.
- Archer + skirmisher share adventurer.png base; weapon overlays do the differentiation. Watch in playtest #3.

## Phase 7 — Combatant rendering per LLM/class context (~1 week) — NEW

**Status:** ⬜ Not started — pulled into demo1 per Path A decision (2026-05-10)

Per file 25 Tier 2 — composed sprite atoms from open libraries (Kenney.nl, OpenGameArt).

- [ ] Sprite library curation (download CC0 RPG character packs)
- [ ] Atoms catalogued: bodies by archetype, weapon overlays, armor accents
- [ ] Archetype → sprite mapping function (`archetype_tag`, `dominant_element`, `energy_type`, `range_profile` → atom selection)
- [ ] Element accent particles orbiting sprite (using `color_value` / `color_palette`)
- [ ] Composite rendering at runtime: body → equipment → accents → particles
- [ ] Movement integration: walking animation OR bobbing; facing direction (sprite flip) based on movement
- [ ] Boss tier visual scaling: trash 0.7-0.8×, standard/elite full size, mini-boss 1.2×, boss/act-bosses 1.4-1.6× with extra particle aura
- [ ] Tier 1 procedural fallback if specific archetype lacks sprite atoms (no silent failures)
- [ ] **Browser-runnable milestone:** classes are visually distinct at a glance — fire mage looks different from ice mage, warrior different from mage
- [ ] **Family playtest opportunity:** can son tell which class he's playing without reading the name?

## Phase 8 — Polish + multi-season + soundtrack (~3-5 days) — REORDERED 2026-05-10 (swapped with rooms; season selection lands before per-season visual variation so the room work in Phase 9 can demonstrate element flavor across all 5 seasons in context)

**Status:** ⬜ Not started

- [ ] Season selection UI (5 seasons listed: 1001 Deep Trench / 1002 First Saint's Crypt / 1003 Cathedral of Bone / 1004 Mad King's Throne / 1005 Gold Strike Ghost Town)
- [ ] Class selection UI (~8-9 playable per season; act-bosses excluded since they're encountered as bosses)
- [ ] **Diablo-style UI with seasonal tinting:**
  - [ ] Health globe (left, red/blood, drains as HP drops)
  - [ ] Resource globe (right, color matches energy_type)
  - [ ] Belt/potion bar (visible potion count)
  - [ ] Ability hotbar
  - [ ] Character portrait
  - [ ] Stylized borders/frames
  - [ ] Per-season color tint applied to UI design
- [ ] End-of-encounter flow:
  - [ ] Win/lose recap with detailed stats
  - [ ] "New Season" / "Try Again" / "Different Class" buttons
- [ ] End-to-end playtest pass on each of 5 seasons (against Phase 6/7 rendering — placeholder rooms acceptable, themed rooms ship in Phase 9)
- [ ] Performance: maintain 60 FPS at 1080p (with movement + sprite rendering)
- [ ] UI polish: tooltips, transitions, readable typography
- [ ] **Single general soundtrack** (non-blocking if it doesn't land — moved here from "absolute last" because Phase 9 is rooms, not audio; soundtrack still cuttable)
- [ ] **Browser-runnable milestone:** Player picks any of 5 seasons → any class within → plays full 7-wave gauntlet → returns to season select → repeats with different season/class. Demo1 is functionally ship-quality across all 5 seasons; only visual room variety (Phase 9) remains.

**Quick verification check at end of Phase 8** (~10 min): all 5 seasons selectable; classes pop across seasons; UI tinting visibly different per season; soundtrack loops cleanly. NOT a full family playtest yet — that happens after Phase 9.

## Phase 8.2 — Equipment-driven weapons + ability animations (~3-5 days) — IMPLEMENTED 2026-05-10

**Status:** 🟡 Implemented; awaiting Matt verification + tag clarity (CLI shipped without explicit `v0.8.2-partial` tag declaration; missing 60 FPS confirmation, console-log observations, 5-season smoke test from prompt's mandatory verification section)

**Architecture shipped (sprites.ts + main.ts):**
- `CombatantSprite` extended: `offHandOverlay`, `weaponGlow` (persistent child of weaponOverlay), `primaryColor`, `elemColor`, `currentWeaponKind`, `animState`, `animElapsed`, `animDuration`, `weaponTier`, `weaponColorSig`, `weaponFlashElapsed`
- `refreshWeaponOverlay(sprite, kind, primary, elem, tier, colorSig)` — Workstreams 1, 4, 5
- `refreshOffHandOverlay(sprite, kind)` — Workstream 6 (2h naturally clears via null off_hand)
- `startWeaponAnimation(sprite, geometry)` — Workstream 2 (slash/thrust/cast/shoot per geometry)
- `tickCombatantAnimation` extended: sin-arc weapon pose animation, equip fade-in flash, per-frame `drawWeaponTierGlow` pulse
- Player weapon initialized in `startGauntlet` via `_refreshPlayerWeaponOverlay()`
- Equip callback refreshes overlay + combat log entry — Workstream 5
- `loadOpponent` refreshes act-boss weapon with `carried_gear.weapon` tier glow — Workstream 3
- `activateSkill` triggers `startWeaponAnimation` on caster sprite (player AND NPC)
- Dev server on port 5176 for testing

**Verification still pending (per partial-tag protocol):**
- [ ] Tag clarity: declare `v0.8.2-partial` until Matt verifies; promote to v0.8.2 after
- [ ] Console-logged observations: `[weapon-overlay]`, `[weapon-anim]`, `[tier-glow]`
- [ ] 60 FPS at peak Wave 1 trash count
- [ ] 5-season smoke test (proven protocol from 8.0.3)
- [ ] Warrior + brute walk-only handling (Option A: weapon animates, body stays in idle) — confirm not silent fallback to something else
- [ ] Matt playtest: W1-W6 per checklist

**Status:** ⬜ Queued — lands after Phase 8.1 ships; before Phase 9 family playtest #3

Triggered by Matt 2026-05-10: archetype-determined weapons (Phase 8.1) don't reflect actual equipped gear; weapons are static (no animation on ability use). Fixing both unlocks the gear-drop loop's perceived value.

**Core decision:** LPC weapon overlays (not procedural Pixi shapes). Procedural geometric weapons on top of LPC body sprites would create aesthetic mismatch; LPC weapon overlay layers compose natively with body sprites at the same atlas convention.

- [ ] **Equipment-driven weapon overlay** — read player.equipped slots; map `gear.weapon_type` → LPC weapon overlay; update on equip/unequip events
- [ ] **Ability-cast weapon animation** — map `ability.geometry` → animation type (slash / thrust / cast / shoot per LPC standard set); ~0.3-0.4s playback on cast; return to idle after
- [ ] **NPC weapon rendering from carried_gear** — same data-driven pattern; act-bosses + class NPCs render their canonical loadouts
- [ ] **Tier/rarity weapon visual signaling** — common/uncommon/rare/epic/legendary outlines + glows mirroring Phase 5 ground-drop convention
- [ ] **Equip-change feedback** — flash/shimmer on equip event; combat log entry; character sheet weapon preview
- [ ] **2h-clears-off-hand visual logic** — mirror Phase 5's mechanical 2h displacement
- [ ] **Performance check** — 60 FPS at peak combatant count with animation state machines + sprite overlay swaps
- [ ] Smoke-test all 5 seasons; partial-tag protocol per 8.0.3 convention; promote to v0.8.2 after Matt's playtest confirms

**Why this lands before Phase 9 family playtest #3:** without 8.2, the demo's equip flow has a visual disconnect (legendary axe on fire mage still shows archetype-default staff). Playtest #3 should evaluate the most coherent version of the demo.

## Phase 9 — Room visual variation per wave (~3-5 days) — REORDERED 2026-05-10 (family playtest #3 MOVED to after Phase 9.3)

**Status:** 🟡 Implemented (2026-05-10) — tagged v0.9-partial; awaiting Matt smoke test for v0.9 promotion

**What shipped (822 lines, 4 files):**
- `src/rendering/arenaFloor.ts` (new, 580 lines) — 5 seasonal floors + 5 seasonal walls + wave-intensity system
- `src/visuals/ambientParticles.ts` (new, 158 lines) — per-season procedural ambient particles (20-32 motes; drift + alpha-pulse + lifetime envelope)
- main.ts + arena.ts integration

**Per-season visuals:**

| Season | Floor | Walls |
|---|---|---|
| 1001 Trench | basalt mosaic offset tiles + thrum cracks + brine sheen | jagged basalt cliff faces with fissures |
| 1002 Crypt | pale stone tile grid + candle-warm patches + tear stains | stone sarcophagus lids with tear drips |
| 1003 Cathedral | ossuary square tiles + bone cross etchings + milky overlay | bone-pillar columns + breath-mist wisps |
| 1004 Mad King | marble checkerboard + char streaks + mercury glints | cracked marble pillars + char burns |
| 1005 Ghost Town | horizontal weathered planks + dust patches + gold flecks | wood barricade stacks + post supports + nails |

**Wave intensity progression:** trash=bare → standard=debris → elite=7% element tint → mini-boss=11%+props → boss=15%+dramatic props → act_boss=18%+signature element.

**Architecture wins:**
- `_layers.arena` has TWO sub-containers: `ambientContainer` (persistent across waves; particles survive transitions) + `dressingContainer` (cleared+redrawn each wave). Avoids particle-wipe bug.
- Arena fade-in (ease-in-quad, 0.55s) on each `loadOpponent` call.
- `@pixi/particle-emitter` not adopted — procedural fallback chosen; matches Phase 7 OrbitalParticle architecture; eliminates texture-plumbing + v7 compat risk.

**Promotion criterion (clarified):** v0.9 promotes after Matt's smoke test (not full family playtest). Family playtest #3 moved to after Phase 9.3 ships.

**Status:** ⬜ Not started — pulled into demo1 per Path A decision (2026-05-10)

By Phase 9, all 5 seasons + all classes are selectable (per Phase 8) — so the per-season visual flavor in rooms can be validated across multiple seasons in the same playtest, not just the one currently in flight.

- [ ] **Floor design per season** — replace the current uniform elliptical floor with seasonal-themed floor pattern:
  - [ ] Trench (1001): dark basalt mosaic, watery sheen, deep-blue undertone
  - [ ] First Saint's Crypt (1002): pale stone tiles with cracks, muted candle-warm tint
  - [ ] Cathedral of Bone (1003): white tiled ossuary patterns, milky overlay
  - [ ] Mad King's Throne (1004): marble checkerboard with dust + char streaks
  - [ ] Gold Strike (1005): weathered planks + scattered dust, sun-bleached tones
  - All Pixi Graphics (Tier 1 procedural); no external art required
- [ ] **Wall design at arena ellipse boundary** — replace the current thin boundary ring with seasonal wall structures:
  - [ ] Trench: jagged basalt cliff faces with thrum-fissure cracks
  - [ ] Crypt: stone sarcophagi + tear-stained walls
  - [ ] Cathedral: bone-pillar columns + breath-mist boundary
  - [ ] Mad King: cracked marble pillars + char-burnt curtains
  - [ ] Ghost Town: weathered wood barricades + dust-veiled fences
  - All boundary structures clamp visually at ellipse edge; non-walkable
- [ ] Per-wave intensity layering ON TOP of seasonal floor/wall:
  - [ ] Wave 1 (trash): warm-up arena, minimal set dressing
  - [ ] Wave 2 (standard): rising-threat, scattered debris on floor
  - [ ] Wave 3 (elite): themed lighting tint based on dominant element
  - [ ] Wave 4 (mini-boss): more particles in the air, deeper element tint
  - [ ] Wave 5 (boss-tier monster): "boss-arena" — strong element tint, decorative elements (pillars, braziers, water pools — themed per anchor)
  - [ ] Waves 6-7 (act-bosses): signature final-encounter atmosphere
- [ ] Per-season visual flavor (palette + particles inherit from anchor + element flavors); validated by switching seasons mid-playtest via Phase 8's selector
- [ ] Smooth wave transitions (fade-out → indicator → fade-in)
- [ ] Per-tier set dressing additions (Tier 1 procedural; no AI art required for demo1)
- [ ] No performance regression — still 60 FPS
- [ ] **Browser-runnable milestone:** ship-quality demo1 — each wave's room is visually distinct, element flavor per season is visible across all 5 seasons, and the full demo1 experience (movement, LLM-rendered combatants, room variety, gear drops, season selection, soundtrack) is integrated.

**Family playtest #3 (final ship state).** Take notes on:
- Overall polish — is anything obviously rough?
- Season variety — does each season feel distinct in rooms + classes + element flavor?
- Audio mix — SFX vs music balance OK?
- Music vibe (if landed) — does it set the right tone?
- Demo1 readiness — would you show this to someone unfamiliar with the project?

---

## Phase 9.1 — Floor patches + wall continuity polish (~half day) — IMPLEMENTED 2026-05-10

**Status:** ✅ Complete (2026-05-10) — Matt smoke-test verified; walls accepted as-is per Option A; promote v0.9.1-partial → v0.9.1 in flight

**Walls accepted as-is** with one caveat noted for Phase 10 polish backlog: walls form a coherent boundary structure but read more as "decorative pillars at intervals" than "continuous wall mass." Acceptable for ship; revisit only if family playtest #3 flags it. Possible Phase 10 polish includes widening + heightening segments, adding wall-back band, or adding connecting structural elements between adjacent pillars.

**Fix 1 (floor patches) — Option B applied** across 5 seasons:

| Season | Before | After |
|---|---|---|
| 1001 Trench | watery sheen 0x1a3858 @ 0.10α (lighter than floor) | shadow pool 0x020508 @ 0.22α (darker) |
| 1002 Crypt | candle patches 0x2a1808 @ 0.18α (warm light) | shadow wear 0x060410 @ 0.11α (dark) |
| 1003 Cathedral | milky overlay 0xf4f0e8 @ 0.045α over 85% area | same color 0.04α over 75% area — effectively invisible |
| 1004 Mad King | mercury glints 2.5px dots (already fine) | unchanged + inFloorForTiles guard added |
| 1005 Ghost Town | dust patches 0x2a2018 @ 0.24α (warm spotlight) | wear shadows 0x050302 @ 0.11α (dark stain) |

**Cathedral choice worth verifying in smoke test:** kept milky white but reduced to near-invisibility. Thematically defensible (Cathedral's element is "milk"/white) but risks losing the season's white tonal identity at the floor level. Re-eyeball during smoke test.

**Fix 2 (wall continuity) — clever leverage of existing architecture:**
- Insight: the 36px `TILE_MARGIN` + `_drawPerimeterRing()` already create an implicit continuous dark band at the floor edge. Tiles never draw in the outer 36px zone.
- Wall segment gaps now reveal that band, not bright floor tiles.
- N: 14 → 22 (gap angle 26° → 16°, ~37% tighter)
- Result: continuous dark band around entire ellipse; segments visible as structural detail on top.

## Phase 9.3 — Left-mouse-button control scheme (~3-5 days) — NEW 2026-05-10

**Status:** 🟡 Implemented (2026-05-10) — tagged v0.9.3-partial; awaiting Matt smoke test

**What shipped (per CLI report):**
- LMB click → arena floor walks to click point (blue ring indicator, ~0.45s fade)
- LMB click → enemy in range fires lowest-cooldown ready skill (red pulsing ring on target)
- Hold-click → continuous attack at cooldown rate; no movement
- LMB click → out-of-range enemy chases + auto-fires when in range
- Click elsewhere during chase → chase aborts; new behavior takes over
- WASD interrupt → red ring clears; keyboard movement takes over
- isPaused gate → clicks blocked during inventory/character sheet/between-wave
- Hotkeys 1-6/Space → no regression, still fire as before
- Performance: O(6) per frame for skill selection; negligible

**Console-log spec:**
- `[click] world=(x,y) hit=floor` (floor click)
- `[click] world=(x,y) hit=opponent in-range` + `[click-attack] slot=N skill=...` (in-range)
- `[click-chase] world=(x,y) chasing opponent` (out-of-range)
- `[click-attack] slot=N skill=...` (skill fires during chase on approach)

**Three high-risk behaviors to verify** (per pre-playtest discipline):
1. Out-of-range chase + auto-fire on approach (complex state machine)
2. WASD interrupt during click-attack (state ownership transition)
3. Click elsewhere during chase aborts cleanly (chase-cancel logic)

**Smoke test result (Matt 2026-05-10):** click-to-move works; chase works; UI clicks preserved. BUG surfaced: click-on-enemy fired all ready skills simultaneously due to frame-by-frame race in skill selection.

**Hot fix landed (2026-05-10):** Root cause was subtler than naive iteration — the original algorithm's per-frame `isSkillReady` filter changed the "min cooldown_seconds" winner each frame as each fired and went on cooldown. Two-pass fix: (1) find preferred slot ignoring cooldown state (always same slot, usually primary); (2) gate firing on that specific slot's cooldown. Result: emergent ARPG-correct behavior — LMB effectively binds to primary attack.

**Architectural note:** if a class ever has a secondary skill with lower base_cooldown than primary, LMB will fire that secondary. Currently primary is always lowest in observed seasonal data; consistent in practice.

**Status:** ✅ Complete (2026-05-10) — Matt re-verified clean; promote v0.9.3-partial → v0.9.3 in flight; **family playtest #3 is the next moment**.

Triggered by Matt 2026-05-10: WASD-only + hotkey-only is missing the dominant ARPG input pattern. Adding Diablo-style left-click control with auto-skill-selection brings the demo into proper genre alignment.

**Control scheme:**
- Click on arena floor: player moves toward click point at range_profile speed
- Click on enemy: cast lowest-cooldown ready+affordable+in-range skill; player attacks in place
- Click on out-of-range enemy: Diablo-style move-and-attack (chase + auto-fire when in range)
- Hold-click on enemy: continuous auto-attack at cooldown rate
- WASD preserved as alternative; WASD takes precedence when active
- UI clicks unchanged (existing inventory/character sheet/between-wave behavior)

**Skill selection algorithm:** filter to skills with (cooldown_remaining ≤ 0) AND (player.can_afford) AND (target_in_range); pick the one with the shortest base_cooldown_seconds. Implements "use the most-available ability" pattern.

**Family playtest #3 MOVED:** previously specced at end of Phase 9; now happens AFTER 9.3 ships, evaluating the full visual (Phase 9) + control scheme (9.3) package. This is the demo1 ship gate.

## Phase 9.5b — Minimum-viable rooms (Step 2 of ARPG genre alignment)

**Status:** ✅ Complete (2026-05-10) — Matt smoke-test verified Goldilocks zone; faces forward, all combo skills castable, focus tuned 25→18 (final); **demo1 ships at v1.0**

**What shipped:**
- `arena.ts`: `ELLIPSE_RX/RY` → mutable `export let`; `setPlayableRoomDimensions(rx, ry)` updates dims + PLAYER_SPAWN/OPPONENT_SPAWN in-place
- `arenaFloor.ts`: same pattern for `FLOOR_RX/FLOOR_RY`; `setArenaFloorDimensions()` updates them; tile loops + wall segments auto-update via live bindings
- `main.ts`: `WAVE_ROOM_SPECS[7]` array (ellipse / hallway-h / hallway-v per wave); `PackActor.dormant` flag separate from `.spawned`; state machine extended with `breather | door_active | transitioning` states; `between_waves` overlay state removed entirely as refactor
- `loadWave()` flow: apply room shape → redraw floor/walls → refill HP/resource → spawn player at left → all pack `dormant=true spawned=true` at right → state=breather
- `_drawDoor(active)`: dim pulse during breather; bright green glow when activated post-wave-clear; at right edge of playable ellipse
- State transitions: `breather → fighting (cross aggro threshold) → pack_dying (all dead) → door_active (door turns green) → transitioning (cross door) → breather (next wave)`
- Console logs: `[room]`, `[door] activated`, `[door] crossed`, `[pack-aggro]`

**Design call worth verifying:** CLI chose **visible-dormant** packs (Hades/Diablo style — visible but frozen until aggro). Alternative is invisible-spawn-on-cross. Matt to eyeball which feels right.

**Smoke test priorities:**
- 🔴 Per-wave room shapes change correctly (ellipse / hallway-h / hallway-v)
- 🔴 Breather → aggro → fight → door → next room flow works
- 🔴 1v1 act-boss flow preserved (waves 6-7)
- 🟡 Per-season floors/walls adapt to room shape
- 🟡 Ambient particles work across all room shapes
- 🟡 Console logs fire correctly per spec
- 🟢 60 FPS at peak (wave 5)

**Note:** v0.9.5a.1 hot fix status in this build is unclear — CLI report doesn't mention sprite facing / focus / combo overrides. Verify with CLI before smoke test; if missing, apply alongside 9.5b verification.

## Phase 9.5 — ARPG genre alignment, incremental (was Option A/B/C from family playtest #3) — RESTRUCTURED 2026-05-10

**Status:** 🔄 Active — family playtest #3 confirmed demo1 doesn't yet feel ARPG-shaped. Matt's locked plan: incremental build toward full dungeon crawl with ship-or-continue gates after each step.

**Sequence:**

| Sub-phase | What lands | After landing |
|---|---|---|
| **9.5a** (Option C: packs only) | Packs in current single arenas + pack-grade monster nerfs (HP×0.18, damage×0.25 for trash adds) | Playtest gate: ship at v1.0, or continue to 9.5b |
| **9.5b** (Option B: rooms) | Minimum-viable rooms — walk-through-door transitions, hallway-shaped rooms for some waves | Playtest gate: ship at v1.0, or continue to 9.5c |
| **9.5c** (Option A: full dungeon) | Full dungeon crawl — forks, multi-room map graph, act-boss path divergence | Ship at v1.0 |

**Worst case:** 4-6 weeks total. **Best case:** ship after 9.5a (~3-5 days).

**Wave 1-5 pack composition (9.5a):**

| Wave | Composition |
|---|---|
| 1 | 4-5 weak trash simultaneous |
| 2 | 1 standard + 2-3 trash adds |
| 3 | 1 elite + 3 trash adds |
| 4 | 1 mini-boss + 3-4 trash adds |
| 5 | 1 boss + 2 elites + 4-5 trash adds |
| 6 | 1v1 act-boss (preserved) |
| 7 | 1v1 act-boss (preserved) |

Boss fights stay 1v1 per ARPG genre convention (Diablo/PoE/Last Epoch preserve this).

**Engine queue addition:** swarm-tier monster generation. For now, demo client-side stat override is acceptable; engine adopts swarm-tier as a generation rule when engine work resumes post-demo1-ship.

**Phase 9.5a prompt** delivered to Matt 2026-05-10; partial-tag protocol applies.

### Phase 9.5a implementation (2026-05-10)

**Status:** 🟡 Implemented; tagged v0.9.5a-partial; awaiting Matt smoke test

**What shipped:**
- `combatant.ts`: `_packHpMult`, `_packDmgMult` fields + `applyPackMultipliers(0.18, 0.25)` on trash adds at spawn; multiplied into `maxHp` getter and `attackerStats.damageModifier`
- `gauntlet.ts`: `WaveSpec.pack` replaces sequential `opponents[]`; `GauntletManager.advance()` returns `next_wave | complete`
- `main.ts`: `PackActor` struct; `loadWave()` builds simultaneous pack with arc spawn positions; per-actor spawn fade-in (alpha 0→1, ~70ms stagger between members); AI loop iterates pack members independently; wave clear when `pack.every(!isAlive)`; 30% potion drop on trash add death
- **AOE splash added:** `resolveSkillEffects()` runs on secondary targets within `AOE_RADIUS` — semantics need smoke-test verification

**Two deviations from spec to verify:**
1. AOE splash — if it applies only to true AOE geometries (cone/circle/ground_slam), ✅ correct. If it applies to single-target/projectile, ⚠️ regression that erodes class differentiation.
2. Wave 5 trimmed from "1 boss + 2 elites + 4-5 adds" → "1 boss + 1 elite + 4 adds". May be intentional perf/visual simplification; verify feels boss-y.

**Smoke test priorities (risk-weighted):**
- 🔴 High: single-target abilities stay single-target; AOE abilities hit multiple; AI runs independently per pack member; wave clear gated on ALL pack dead
- 🟡 Medium: 60 FPS at Wave 5 peak; pack stat overrides apply; Wave 5 trim acceptable
- 🟢 Low: spawn fade-in; 30% potion drop rate

**Matt smoke test result (2026-05-10):**
- ✅ All combatants spawn correctly
- ✅ AOE moves hit multiple targets within geometry (correct semantics)
- ❌ One combatant usually invisible (still casts abilities + takes damage)
- ❌ Clicks "away from all combatants" sometimes target most recently attacked enemy

**Root cause diagnosis (main.ts:587 — both bugs from one line):**
- The line `spawned: slot.spawnDelay === 0` marks the first pack member as `spawned:true` immediately, but line 562 still sets `sprite.container.alpha = 0`
- The fade-in code at line 1224 only runs `if (!m.spawned)` — member 0 is skipped, alpha stays at 0 → INVISIBLE
- The LMB hit-test at line 730 skips `!m.spawned` members but member 0 is `spawned:true` → remains hit-testable → clicks "on empty floor" near its invisible position trigger attacks
- One-line fix: `spawned: false` (let every member go through the fade-in flow normally)

**Hot fix delivered to Matt 2026-05-10** — CLI re-tags v0.9.5a-partial after fix; Matt re-verifies; promote to v0.9.5a.

**Hot fix partial result (2026-05-10):**
- ✅ Bug 2 (click-attack stickiness on last enemy) — resolved by `spawned: false` fix; clicks now correctly disambiguate enemy vs floor
- ❌ Bug 1 (invisible first enemy) — persists despite the same fix; code inspection confirms fade-in path SHOULD reach alpha=1, but observation shows it doesn't

**Diagnostic in flight:** added temporary instrumentation (debug-spawn / debug-fade logs) to capture what's actually happening per-frame for pack member 0. Will reveal whether (a) fade-in code isn't running, (b) alpha increments correctly but render doesn't reflect, or (c) cached build (fix not deployed to whichever build Matt is testing).

**Resolution (2026-05-10):** Stale Vite HMR. Code fix at line 587 (`spawned: false`) WAS correct; Vite just didn't pick up the change. Solution: stop + restart dev server. All 4 pack members fade in correctly after restart.

**Phase 9.5a playtest result (Matt 2026-05-10):**
- ✅ All combatants visible after dev restart
- ✅ Fire mage cleared full 7-wave gauntlet in ~2 minutes
- ✅ "A bit tougher than earlier battles" — pack stats (HP×0.18, dmg×0.25) land in target zone
- ✅ AOE classes work cleanly with pack format

**Process lesson:** second occurrence of "stale build, code looks right" (first was Phase 8 ticker fix). Rule going forward: when fix is in code but observation contradicts, restart dev server BEFORE diagnostic instrumentation. 30-second check rules out half the failure modes.

**Status:** ✅ Phase 9.5a Complete (2026-05-10) — promoted v0.9.5a, committed, prd-built; Phase 9.5b prompt delivered to Matt; two bugs surfaced during 9.5b wait worth fixing (bundle into 9.5b OR ship as v0.9.5a.1):
- **Bug: Sprites back-facing.** `archetypeRenderer.ts:108-110` uses wrong rows for standard N,W,S,E LPC layout. Fix: `LPC_WALK_S = Rectangle(0, 640, 64, 64)` + `WALK_ONLY_S = Rectangle(0, 128, 64, 64)`.
- **Issue: Focus restore can't sustain costs.** Matt diagnostic 2026-05-10: ranger casts deplete energy because +10 restore < typical skill cost (7.9-35.3 range, median ~19). Engine generator miscalibration — same shape as combo cost A1. **Added to engine queue as A1b in file 28.** Demo-side override: boost `FOCUS_RESTORE_PER_CAST` from 10 to 25 in combatant.ts:98.
- **Issue: Combo skills cost > pool max=5.** Same shape as focus. Engine queue A1. Demo-side override: clamp `min(energy_cost, 5)` for combo classes in combatant.ts `effectiveEnergyCost`. After clamp, all 24 combo skills castable; high-tier spenders all share cost=5 (loss of differentiation acceptable until engine fix).
- **Demo-override removal plan added to file 28** — canonical map between current demo overrides and engine queue items. After each engine queue category (A/B/C/D) ships, demo team runs cleanup pass to remove corresponding overrides. Section also includes verification rubric for each removal.

**Family playtest #3.5 follows v0.9.5a promotion** — decision question: does combat now feel ARPG-shaped? Outcomes: ship at v1.0, continue to 9.5b, or skip 9.5b and continue to 9.5c.

**Status:** ⬜ Conditional — ships if playtest #3 reveals genre-feel issue (combat reads as adventure-game vs ARPG due to 1v1 wave structure)

**Decision locked 2026-05-10:** Option B — keep 1v1 primary encounter as focal threat, add trash adjacent. Engine convergence stays mostly meaningful; class targeting still works; AOE classes feel rewarded but don't faceroll.

**Wave restructure spec (Option B):**

| Wave | Current | Proposed |
|---|---|---|
| 1 | 3 trash sequential | 4-5 weak trash simultaneous |
| 2 | 2 standard | 1 standard + 2-3 trash |
| 3 | 1 elite | 1 elite + 3 trash |
| 4 | 1 mini-boss | 1 mini-boss + 3-4 trash adds |
| 5 | 1 boss | 1 boss + 2 elites + 4-5 trash |
| 6-7 | 2 act-bosses | **Stay 1v1** — boss fights are climactic; preserve focus |

**Tuning targets for trash adds:**
- HP: 15-25% of current trash baseline
- Damage: 20-30% of current trash baseline
- AI: simple tier, slow cadence (atmosphere not threat)
- Drops: 30% chance for 1 potion; NO gear (gear stays on named tiers — preserves progression)
- Count: 3-5 per wave depending on tier

**Engine convergence implications (acceptable, not blockers):**
- Primary 1v1 encounter unchanged → class balance survives
- Status-effect saturation increases (4-5 sources rolling 35% chances → controllers feel impactful) — engine queue item already tracks per-skill ailment chance scaling
- AOE classes become more valuable (visible reward for group hits) — engine queue item could add AOE budget rebalancing later

**Family playtest #4 (final ARPG-feel validation) happens after Phase 9.5 if it ships.**

## Phase 9.7 — Ability VFX sprite atoms (~3-5 days, conditional on family playtest #3) — NEW 2026-05-10

**Status:** ⬜ Tentatively scheduled — fires if family playtest #3 reveals procedural ability VFX feels "prototype-y"; defers to Phase 10 if VFX feel acceptable to son

Triggered by Matt 2026-05-10: itch.io has many pixel-art magic/spell VFX packs in the $0-$20 range that could replace procedural Pixi Graphics for ability geometries. Visual delta from "procedural shapes with eased motion" → "real pixel-art animated VFX" is large.

**Decision-informing question at playtest #3:** ask son "do the abilities look cool, or do they look like prototype shapes?" Answer drives Phase 9.7 fire or Phase 10 defer.

**If 9.7 fires (before demo1 ship):**
- Asset pack survey + decision (stop-and-surface gate, same pattern as Phase 8.1)
- Acquisition + license documentation
- Per-geometry integration: melee_strike / melee_arc / projectile / ranged_physical / circle / ground_targeted_circle / ground_slam / cone / line / beam_channel / others
- Element tinting per element-flavor (so fire/water/earth/wind variants share geometry but read distinctly)
- Animation frame timing + state machine for play-once-on-cast
- Performance check at peak combatant + AOE density

**Pack candidates to survey** (CLI does the work; Matt approves):
- itch.io "magic spell effects" tag (sorted by popularity)
- OpenGameArt "magic" / "spell-fx" tags as CC0 backup
- Single-author packs preferred over mixing (aesthetic consistency)
- $5-$20 range often gets meaningful coverage over free

**If 9.7 defers to Phase 10:** demo1 ships with current procedural ability VFX; Phase 10 becomes "post-ship polish" covering VFX sprites + walk cycles for warrior/brute + Tier 2 source-replacements + etc.

## Phase 11 — Mobile support (~5-7 days) — NEW 2026-05-11

**Status:** ✅ Complete (2026-05-11) — tagged v1.1, pushed; Vercel auto-deploying mobile-supported build

Triggered by Matt 2026-05-11: extended audience beyond Matt + son is primarily mobile. Demo1 v1.0 was shipped + deployed to Vercel; v1.1 adds full mobile support as a single coherent phase. Engine queue (file 28) defers behind v1.1 mobile.

**Seven workstreams in one phase:**

1. Mobile detection (`Mobile.isActive` singleton) + orientation lock (Screen Orientation API + rotate-device overlay fallback) + responsive canvas (CSS `object-fit: contain` to scale Pixi viewport)
2. Virtual joystick (bottom-left, Pixi component, analog vector → existing player movement system)
3. Touch ability buttons (bottom-right arc, ~70px each, Diablo-Immortal-style layout)
4. Potion belt UI (bottom-center, health + mana icons with count badges, tap-to-use)
5. Top-right icons: inventory + character + combat log; tap-to-open existing panels
6. Tap-tooltip flow: short-tap = action (equip/unequip), long-press (400ms) = tooltip; replaces hover on mobile
7. Combat log default minimized on mobile; tap-to-expand panel

**Critical: desktop preservation 100%** — all mobile UI is additive behind `Mobile.isActive` gate; desktop v1.0 behavior unchanged.

**iOS Safari + Android Chrome both tested** before promotion. Audio context unlock confirmed on first touch.

Family playtest #5 on real mobile device after v1.1 ships.

### Phase 11.1 hot fixes from real-device mobile testing (2026-05-11)

**Matt's iOS Safari smoke test surfaced 3 bugs + 1 polish:**
- Bug: movement disabled after wave clear (state gate too restrictive — allowed only in 'fighting')
- Bug: mobile UI layout overlaps — potions covered by desktop hotbar (should be hidden on mobile); inventory/character icons covering combat log; icons have no visual
- Bug: iOS Safari shows URL bar — not a bug to fix programmatically; iOS doesn't allow web fullscreen; needs PWA "Add to Home Screen" path
- Polish: dead combatants stay rendered alive (just empty HP bar)

**Fixes bundled into hot-fix prompt:**
- Allow movement in all states except `transitioning`
- Hide desktop hotbar on mobile; move inventory+character to top-left; potions to curved arc below ability buttons; add procedural Pixi icons (backpack, bust, scroll)
- Add PWA manifest + `apple-mobile-web-app-capable` meta tag + Add-to-Home-Screen hint overlay
- Dead combatant: rotate 90° + fade alpha over 1.5s + hide bars/labels immediately

Tag v1.1.1 after fixes verified on real device.

## Phase 12 — Ability VFX sprite atoms (~3-5 days) — NEW 2026-05-11

**Status:** ✅ Complete (2026-05-11) — Matt verified ("plays 5x more enjoyable"); shipping v1.2; Vercel auto-deploys on push

**Two bugs caught during smoke test, both fixed before ship:**
1. Hardcoded 64×64 frame dimensions didn't match pack reality (some effects 96×96, 128×128, 140×50). Replaced hardcoding with auto-derivation from `spritesheet.txt` sidecar files — eliminates the entire bug class for future pack swaps.
2. ground_slam scale 3.5 → 2.0 after frame-size correction (was 448px after correction; appropriately scaled to 256px).

**Architecture wins from the fix:**
- `prewarmSpriteVfxCache()` at startGauntlet() — fetches 15 .txt files in parallel (~200ms); subsequent casts hit the dim cache instantly
- `try/catch` safety net in `spawnSpriteVfx()` — any future error triggers procedural fallback; game never crashes
- Removed `frameW`/`frameH` from EffectSpec entirely — that column can't drift wrong again

**Pack chosen:** Super Pixel Effects Gigapack ($4.99, unTied Games, 110 effects + per-element color variants)

CLI survey presented 3 finalists 2026-05-11. Matt chose Option B (gigapack) over Option A (Foozlecc CC0) for coverage — paid tier covers melee_strike/melee_arc/line/beam_channel that the CC0 pack lacked.

**License:** simple attribution (in-game credits OR ATTRIBUTION.md). Bake the attribution into `/public/sprites/abilities/ATTRIBUTION.md` matching Phase 8.1 LPC convention.

**Color variants in paid tier** may obviate Pixi `.tint` for element coloring — if the pack ships fire/water/earth/wind/physical variants per effect, picking the right file per element is cleaner than runtime tint multiplication. CLI to evaluate after `ls -R` of unzipped pack.

**Next step:** Matt purchases + downloads + drops folder; runs `ls -R` to surface folder structure; CLI maps geometries to sprites + integrates + verifies.

**Implementation summary (2026-05-11):**
- `src/visuals/spriteVfx.ts` (new): 16-geometry → pack-effect map; per-element color variant URL builder; Pixi base texture caching; 15 FPS frame state machine + fade-out; `!sv()` fallback pattern for procedural safety net
- `src/abilities/vfx.ts`: hybrid integration with three patterns:
  - Pure sprite replacement (melee, AOE circles, self_buff/cast, teleport, single_target)
  - Travel + sprite-at-landing (projectile, ranged_physical)
  - Sprite burst + procedural shape (cone, line, beam_channel — preserves area/direction read)
  - Sprite on activation + procedural duration marker (aura, totem — preserves persistent zone read)
- `main.ts`: spriteVfx pool + tick wiring
- `.gitignore` excludes 34,932 unused individual frames; 1,448 spritesheets committed
- ATTRIBUTION.md credits Will Tice / unTied Games per license

**Architecture wins:**
- Element color variants from pack > Pixi runtime tint (better color preservation)
- Hybrid procedural+sprite for informational geometries preserves combat legibility
- `!sv()` fallback ensures no crashes if asset loads fail

The cherry-on-top phase. Replaces procedural Pixi Graphics ability VFX with real pixel-art sprite frames per geometry type. Single CLI session covers: pack survey on itch.io/OpenGameArt/Kenney → stop-and-surface gate for Matt's pack choice → acquisition → integration → element-aware tinting → smoke test.

**Coverage target:** all 16 ability geometries map to a sprite effect (multiple geometries can share an effect type — e.g., melee_strike + melee_arc both use a "slash" sprite). Procedural fallback retained for any unmatched geometry.

**Element tinting:** 5 elements (fire/water/earth/wind/physical) visibly distinct on same geometry via Pixi `.tint` multiplicative blend.

**Tag v1.2 when verified on desktop + mobile.** Then demo1 is at "polished as it'll get for v1.x." Engine queue (file 28) is the only remaining major work item.

## Phase 10 — Stretch goals (optional, post-Phase-9.5) — RENUMBERED (was Phase 7)

Decide whether to pursue based on Phase 9 family playtest priorities. Either, both, or neither.

### Stretch A — Co-op multiplayer (~2 weeks if pursued)

- [ ] Server scaffolding (Node.js + WebSocket)
- [ ] Authoritative game loop (combat resolution moves server-side)
- [ ] Action message protocol (client → server actions; server → client state)
- [ ] Co-op gameplay rules (shared loot, revival at next wave)
- [ ] Co-op UI (partner HP/resources visible)
- [ ] Local network deployment + family co-op playtest

### Stretch B — Per-season themed music (~1 week if pursued)

- [ ] One unique ambient track per season (5 tracks, AI-generated via Suno/Udio)
- [ ] Per-season prompt structure ("ambient ARPG fantasy music, [anchor], [dominant element]-themed, looping")
- [ ] Track triggers on season selection
- [ ] Replaces single general soundtrack for that season

---

## Family playtest log

### Playtest #1 (after Phase 4) — 2026-05-10

**Matt played:** Trenchwind Pitch-Caster (fire mage, mana) — Gauntlet cleared in 4:07
**Son's session:** *(awaiting separate notes if applicable)*

**What worked:**
- Demo is genuinely playable; gauntlet structure is satisfying as a progression
- Fire mage felt powerful and fun (though see "OP" caveat below)
- Wave-to-wave transitions and HP refills work cleanly
- Combat log + potion HUD don't get in the way

**What felt off (4 findings):**
1. **AI passivity (CRITICAL):** monster + act-boss AI doesn't fire abilities aggressively on cooldown availability. Result: every wave, including the act-boss climax, was trivially easy. Wave 7 act-boss died in ~10 seconds because it didn't use its defensive ability or burn its resource pool. This isn't class-specific — it's structural across all 5 monster tiers + act-bosses.
2. **Heal-targets-enemy bug:** some classes' heal abilities point at and "heal" the enemy instead of self/ally. Non-debatable bug.
3. **Fire mage potentially OP:** no cooldown on core low-mana-cost ability + large mana pool + burn DoT damage = "felt like a god" against the AI. Partially conflated with the AI passivity (when AI fights back, fire mage's high damage feels more appropriate); but worth investigating whether the cooldown data is genuinely 0 or whether demo isn't respecting it.
4. **Some classes feel resource-constrained:** stamina/cooldown chokes mean some classes barely cast. Likely a regen formula issue (similar to the mana regen formula error caught in Phase 2).

**Top classes:** Fire mage felt fun (acknowledging it's currently OP).

**Decision:** Phase 5 paused. Insert Phase 4.5 polish pass (AI fix + heal bug + balance investigation) before Phase 5 ships gear drops onto fights that don't feel earned.

### Playtest #2 (after Phase 5) — 2026-05-10

**Wins (locked in):**
- ✅ Cooldown multiplier 1.4× = right pace
- ✅ Space bar as primary = feels right
- ✅ Cooldown visualization at-a-glance = working

**Issues for Phase 5.5 polish:**
1. **Wave-cleared overlay hides drops** — legendaries dropping on Wave 6 are obscured by the overlay popping up immediately
2. **Inventory may be capacity-constrained** — 4 items × 2 act-bosses + initial loadout might exceed slots
3. **Flavor text missing from tooltips** — gear has `flavor_text` in JSON; not surfaced
4. **No pause during inventory inspection** — AI continues attacking while player inspects gear
5. **Stat comparison invisibility** — player can't see what changes when equipping (no +/- deltas vs current)
6. **No Spirit Guide direction** — engine has marginal-value math (CP7); demo1 isn't surfacing it. Player has no signal whether an upgrade is "strong" or "marginal"

## Phase 5.5 — Post-playtest #2 polish pass (~3-5 days)

**Status:** ✅ Complete (2026-05-10) — tagged v0.5.5-phase5.5, pushed to GitHub

- [x] **Wave-cleared overlay delay** — `ACT_BOSS_GLORY_PAUSE = 4s` for act-boss waves; non-act-boss waves keep 1.6s
- [x] **Inventory stash capacity** — switched from single-column 4-item clip to 2-column grid fitting ~16 items
- [x] **Flavor text in tooltips** — both ground-drop hover and inventory stash hover show `flavor_text` for epic/legendary in italic below stats
- [x] **Pause during inventory** — `isPaused` flag freezes player/opponent ticks, DoT ticks, AI timer; VFX continue animating so drops stay visible
- [x] **Stat delta on hover** — per-stat color-coded delta table; green/red/gray; covers damage flat, damage %, crit, HP, armor, resource regen, CDR, cost reduction
- [x] **Spirit Guide marginal-value signal** — `fit_for_class()` ported from `gear_schema.py` (geometric mean × power_score); `computeMarginalValue()` handles 2H/1H displacement; categorical thresholds: Strong / Solid / Marginal / Sidegrade / Downgrade

## Phase 5.5b — Character sheet (~1-2 days)

**Status:** ✅ Complete (2026-05-10) — tagged v0.5.5b-character-sheet, pushed

- [x] C key toggle, integrates with `syncPause()` (no double-pause when inventory + character sheet both open)
- [x] Six sections: class identity, base attributes, derived combat stats, ability modifiers, element resistances, active state
- [x] Real-time updates on equip/unequip via `charSheet?.build()` re-render
- [x] Spec correction caught: crit cap is **0.75** (not 0.60 as I wrote in the prompt); dodge cap is 0.60. Both shown with correct values per `math_model.py:computeCritChance`
- [x] Element resistances show seasonal names (e.g., "pitch (fire)")

**Phase 5.5b report highlights:**
- Spec error caught (crit cap 0.75 vs 0.60) — another `damage_formula.md` discrepancy added to engine-team backlog
- Both panels (inventory + character sheet) can open simultaneously without bugs
- Energy-type-specific regen descriptions in the derived stats section

## Phase 5.5c — End-game screen polish (~half day)

**Status:** ✅ Complete (2026-05-10) — tagged + pushed

- [x] `ACT_BOSS_GLORY_PAUSE = 4s` confirmed already flowing through `onOpponentDefeated()` for Wave 7 (no new code needed; verified working)
- [x] Win overlay shows ⚔ Inspect Gear (I) + ◈ Character Sheet (C) buttons
- [x] Both panels open from `gState === 'done'` with gear drops still animating
- [x] R-to-restart blocked while a panel is open
- [x] **Browser-runnable milestone:** ✓

## Phase 5.5d — Heal scaling investigation + fix (~half day)

**Status:** ✅ Complete (2026-05-10) — tagged + pushed

- [x] Engine source identified:
  - `damage_resolver.py:104` — direct heals: `magnitude × (1.0 + wisdom × 0.002)`
  - `damage_resolver.py:122` — HoT: `tick_heal × attacker.damage_modifier`
- [x] Both demo bugs confirmed:
  - Direct heals had no wisdom scaling (formula entirely missing)
  - HoT used hardcoded 1.0 instead of `attacker.damage_modifier`
- [x] Both fixed in `resolver.ts`
- [x] Brings damage_formula.md doc-correction backlog to 10 documented errors
- [x] **Browser-runnable milestone:** healing scales meaningfully ✓

## Phase 5.5e — Character sheet enhancements (~1-2 days)

**Status:** ✅ Complete (2026-05-10) — tagged + pushed

Triggered by Matt 2026-05-10 — character sheet from Phase 5.5b is good, but two specific enhancements would make it land harder:

- [x] **Class flavor text in headline format** — class `flavor_text` rendered italic in the right column of the identity section, alongside name + class subtitle on the left
- [x] **Abilities section with full info** — full-width ABILITIES section: name + element-themed icon, geometry type, cost, effective cooldown (post-multiplier), damage/heal/status details, flavor text in tooltip on hover. Hotbar order: slot 0 (SPACE / Primary) first, then 2-6
- [x] **Browser-runnable milestone:** character sheet shows class flavor in headline + abilities section ✓

## Phase 5.5f — Lifesteal + Shield mechanics (~half day)

**Status:** ✅ Complete (2026-05-10) — tagged + pushed

Triggered by Phase 5.5e tooltips surfacing two more engine-vs-demo gaps:

- [x] **Lifesteal** — `resolveOneEffect` now receives running `totalDamage` from prior effects in the loop. On `lifesteal` effect: `stolen = min(totalDamage × percent, maxHp - hp)`. Combat log + green floating number fire on each proc. Matches engine `damage_resolver.py:150-160` exactly.
- [x] **Shield** — applied as ActiveEffect on cast; drained before HP in damage-receive path; expires on duration timeout OR magnitude depletion. Matches engine `damage_resolver.py:109-116` + `combatant.py:183-196`.
- [x] **Root cause caught** — `applyDamage` was double-subtracting shield from already-shield-reduced finalDamage, giving infinite effective absorption AND silently swallowing overflow damage. Fix: separated concerns into `drainShield(amount)` + `applyDamage(amount)`. New pipeline pattern: `remaining = drainShield(incoming); applyDamage(remaining)`.
- [x] Visualization: 5px cyan bar above HP bar, shows `shield / maxHp` fraction of bar width, disappears on depletion or expiry
- [x] **Bonus catches:**
  - DoT ticks now drain shield before HP (same pipeline pattern)
  - Character sheet active-state showed `magnitude × 100%` (latent 5.5b bug); now shows actual remaining shield HP
  - `logLifesteal` and `logShieldAbsorb` added to CombatLog
- [x] **Browser-runnable milestone:** ✓ — Abyssal Cantor / Trench Thrum Gale (12% lifesteal) visibly heals on damage; Trenchwind Pitch-Caster / Trench Pitch Shroud cyan bar absorbs hits and vanishes on depletion/expiry

**Phase 5.5f report highlights:**
- Double-counting was the load-bearing diagnostic — explains why shields felt weightless. The pipeline-vs-parallel framing now extends cleanly to all future damage paths (auto-attack 5.5g, Phase 6 AOE multi-hits, any future reflect/thorns).
- DoT-drain-before-HP fix fell out for free when shield path was made pipeline-clean. Good signal that the fix was structural, not patch-on-symptom.

**Out of scope (engine-side balance gap, NOT a demo bug):** shield magnitude does not scale with WIS or `damage_modifier`. Engine is flat at JSON `magnitude=1000`. Logged in `project_engine_state_findings.md`.

## Phase 5.5g — Auto-attack on Return / Left-mouse (~half day)

**Status:** ⏸ Deferred (2026-05-10, Matt's call) — lands when silence or resource-starvation becomes felt; until then, current demo classes don't expose the gap. Paste-ready prompt preserved in this conversation's transcript for retrieval.

Trigger conditions for un-deferring:
- Silence implementation lands (silence prevents skills; auto-attack should still fire)
- A class is observed standing still in playtest because all skills are gated by resource/cooldown
- Phase 6+ adds inputs that benefit from being able to attack-while-moving without committing to a primary cooldown

Engine ground truth memorialized in `project_engine_state_findings.md` so the spec can be reconstructed on demand.

### Playtest #3 (after Phase 6)
*Status: not yet conducted. Schedule when Phase 6 completes.*

---

## Open questions / blockers

*Update as new questions arise. Cleared questions move to "Resolved."*

### Resolved
- ✅ MANA_REGEN_SCALING constant — found in engine source as 0.002 in `math_model.py:16` (Phase 2). Engine formula is multiplicative: `base_regen * (1 + max(int, wis) * 0.002)`. `damage_formula.md` had this wrong as additive.
- ✅ Monster damage modifier — confirmed 1.0 for gauntlet monsters; act-bosses use class.balance_metadata.final_modifier (Phase 1)
- ✅ Dodge chance cap — corrected to 0.60 in Phase 2 (was wrong in `damage_formula.md`)

### Open / future
- 🔧 **`damage_formula.md` has errors** — at least mana regen formula and dodge cap are wrong. Demo works correctly via engine-source lookups, but doc-correction pass is needed in a future engine session. Non-blocking.
- *(no other open questions currently)*

---

## How to update this tracker

When the demo CLI reports phase completion:
1. Mark phase status (🔄 → ✅)
2. Check sub-goals that landed
3. Note any deviations from spec (e.g., "skipped X because Y")
4. Add observations to the phase notes section
5. Update the "Last updated" date at the top
