# Current State → End State (LIVING)

**STATUS:** LIVING CANONICAL — the single consolidated current-vs-end-state tracker. **Every gandalf session opens this at session-start (OP § 1) and updates it during work (OP § 5).** Not a dated snapshot; a continuously-maintained instrument carried forward until both completion targets close.
**Steward:** gandalf (story-and-design steward). Updates: any gandalf session; sub-agent gandalf proposes, steady-state gandalf commits.
**Purpose:** for the game we are building (the v2 ARPG-build-depth + roguelite-descent loop), hold in ONE place: (I) what the **battle sim** currently IS and where it must go, (II) what the **content-emission pipeline** currently IS and where it must go, (III) the **engine-fit gaps the v2 design opens** (the new material), and (IV) the **owner map + forward queue**. This is the artifact every subsequent session plans from.
**Method:** reconciled against disk with file:line evidence. Provenance tags distinguish `[gandalf-verified]` (looked myself this lineage) from `[fit-audit]` (Explore-pass file:line, 2026-06-23) from `[design-doc]` (claim from the v2 design doc, not yet code-verified).
**Supersedes:** `canonical/story/2026-06-18-current-to-end-state-battlesim-and-pipeline.md` (the dated spine) and `agentic_orchestration/gandalf/notes/2026-06-18-pipeline-completion-progression-memo.md` (the wind-down memo). Those remain as lineage; where they conflict with this doc, **this governs**. The B-series / P-series detail there is not re-reproduced in full — pointers below.
**End-state authority:** `matt_notes_handoff_docs/reincarnated-gameplay-loop-design.md` (v2 canonical gameplay loop) + `matt_notes_handoff_docs/reincarnated-performance-target-specs.md` (Godot density/perf targets). This doc tracks the engine's distance to THAT end state.
**Survey-mode discipline:** within each PART, *Current state* subsections are descriptive (what IS, cited). *End state* / *The gap* subsections are forward judgment (what should be / what's wrong). Kept structurally separate per the cross-cutting rule.

---

## HOW THIS DOC WORKS (living-doc protocol)

1. **Open at startup.** OP § 1 names this as a mandatory session-start read. Read the SESSION-DELTA LOG top-to-bottom first (latest governs), then the body PARTs relevant to the session's work.
2. **Prepend a SESSION-DELTA.** Each session that changes state adds a dated block at the TOP of the SESSION-DELTA LOG. **The latest delta governs all blocks and body sections below it** where they conflict (same pattern as the predecessor memo).
3. **Update the body in place.** When a state table row changes (a gap closes, a blocker clears, a new gap surfaces), edit the row AND note it in the session's delta. Never silently delete — strike with `~~...~~` + date, or move to a "closed" line, so lineage is legible.
4. **Mark completion.** When an item closes, mark it `✓ DONE (date, commit)`. When BOTH completion targets (battle-sim + emission) close AND the v2-fit gaps are dispositioned, this doc retires to historical.

---

## SESSION-DELTA LOG (latest governs all below)

### 2026-06-23 (later, same session) — Matt directive: BUILD-TO-SPEC, NO DEFERRALS; purge "season-N" + accepted-deferral framing

**Matt's ruling (GOVERNS all deferral language in this doc and forward in every gandalf artifact):** *"We are just building an engine to specs and we have no need to defer anything if it is needed in the engine… We will likely need to flip these out of deferred and remove the deferred verbiage across the board."* Plus: *"get rid of references to season 1 across the board."* The engine is built to its FULL spec; "deferred" is not a disposition for anything the v2 loop needs — it is a gap-to-close.

**What this corrects in the founding block below:**

1. **Summoner/proxy is NOT a deferral — it is a GAP-TO-CLOSE (high priority).** `_DEFERRED_PROXY_BINS = {proxy-light, proxy-heavy}` `[bc_target_composer.py:97,318]` zeros out every summoner kit (each emitted kit carries `"proxies": []` — `proxy_vocabulary_bridge.py:22-23`). That flag is a stale artifact of the retired Profile-A "sim is solo-only" era. It **conflicts with v2**, where summoning is a **pillar**: grimoire capture-and-summon (§11), temporal summoning (§13), summoner-as-revealed-identity (§12/§17) all need player-side proxy combatants. An engine "to spec" cannot ship summoner deferred. **Reframed → new PART III.1b, tied to the same multi-actor-sim root as the kit-vs-kit keystone (III.1).**

2. **Full deferral audit added → new PART III.10.** Answering "is anything else deferred?": yes — `charge-stack`, `damage-taken-converts`, `support-role` (`check_infeasibility` deferrals), the `VIT` attribute, the `T4` algorithm, `element-conversion` ailment, and the `HP-economy` substrate-gap. Each classified **flip (v2-build-depth needs it)** / **flag for Matt's ruling** / **keep (genuine layer-handoff)**. The ONE "deferred" that is correct and stays: `dodge_gated_deferred` — a balance-loop terminal outcome handing glass-close-ST viability to the *piloted Godot dodge layer* (a layer-handoff downstream, not a missing feature).

3. **"Season-N" content-release framing purged.** "season-1 kits / season-2 companion / six season content types / emit a season's content" were stale leaks of the **retired seasonal-release model** (archived 2026-06-02, `2026-06-02-season-archive-realm-expansion-pivot.md`). Reframed to "engine content types" / "future-product scope." **Code filenames containing "season" (`season_exporter.py`, `season_generation_pipeline.py`, `run_season_production.py`) are real on-disk artifacts → they stay as literal path cites; they are not the release-model framing.**

**Discipline note (gandalf, self-correcting):** survey-mode faithfully reports what-IS (the code says deferred), but when what-IS conflicts with the end-state this doc tracks against, the conflict is a GAP and must be surfaced as one — never passed through as an accepted disposition. Matt caught a pass-through; corrected here. Forward rule: **no "deferred" disposition for anything the v2 spec needs — it is a gap-to-close.**

---

### 2026-06-23 — TRAJECTORY SHIFT captured: ARPG-build-depth + roguelite descent; v2 frame; horde-gap verified; fit-audit consolidated

**This session founded this living doc** by consolidating the 06-18 spine + memo and absorbing two new inputs Matt handed over: the **v2 gameplay-loop design** (death-faith reframe + crystallized roguelite-descent-with-Goldilocks loop) and the **performance-target specs** (Godot 50-150 density). The trajectory is, in Matt's words, "slightly" changed — the *frame* re-registered (isekai → death-faith) and the *loop* sharpened (Goldilocks fork, grimoire economy, roguelite descent), while the engine direction (battle-sim + emission) is carried forward. The change's weight is in the **new engine demands the v2 loop opens** — captured in PART III.

**What this session established (load-bearing):**

1. **The v2 frame fits cleanly; the v2 loop-machinery has three foundational engine gaps.** The death-faith / patron / home-realm re-registration (design doc §2/§3/§14/§15) touches no engine seam and improves the story — no fit problem. The misfits are in the machinery the doc treats as "carried forward intact." Worst-first in PART III.
2. **KEYSTONE gap — there is no kit-vs-kit path in the sim** `[fit-audit: spatial_engine.py:2944 sole entry = one player-class vs list-of-monster-dicts; balance_loop.py:2051 mirror-duel deliberately retired 2026-06-16]`. Goldilocks (§9), scouting (§9), and the matchup-coverage reward all cash against a kit-vs-kit matchup-temperature the sim does not produce. **Resolution path (gandalf lean): a matchup-temperature SIGNAL — a type-chart/distance lookup over already-emitted features (element + archetype + BC-signature + resistances) — NOT a kit-vs-kit fight.** Net-new either way; gates the most → resolve first.
3. **Horde gap — VERIFIED `[gandalf-verified]`.** The balance kernel validates kits against a **maximum of 8 concurrent enemies**. All six arena shells cap at 8 (`arena.py`); all 18 endgame encounters bind to those shells (`endgame_encounter_catalog.py:33`) and never exceed 8 total (`MobSpec` count maxes at 8: catalog lines 222/352/393/524/692; densest mixed pack 6+1+1=8 lines 304-306); golden-master `mean_mobs_killed` tops out at 8.0. The performance doc's endgame target is **50-150 simultaneous** — a 6-19× gap. The just-closed defensive axis (2026-06-21, dm=5.0 boss @ 4.5s / swarm 0.20) was calibrated only at ≤8 concurrent. **BOTH the prior closing-session summary AND my own first state-of-the-build answer missed this.** Matt's instinct ("add a test/encounter/area") is correct → PART III item 3 recommends `SCENARIO_OVERRUN`.
4. **The "400" the marketing hook rests on is ~54 in the live pipeline** `[fit-audit: season_generation_pipeline.py:169 = 18 BC cells × 3 samples; :41 substrate-led no-pre-imposed-N]`. Not necessarily an architecture wall (substrate-led can scale; ~2,293 active rows), but the hook number is ~7× current output. **I refute treating 400 as a hard spec** — the design doc itself says "effectively endless"; 400 is illustrative. The real gap is *validation throughput for hundreds*, not a literal count.
5. **Per-kit level model absent — the descent is unvalidated** `[fit-audit: balance_loop.py:1935 flat-skill assumption, class stats unchanged across bands]`. The 1→50 leveling (§6), the sawtooth (§7), the +3-becoming (§8), and the §21 spacing-inequality are all unmeasurable; the sim validates at a single fixed L50 endgame point. This is doc-33 progression territory the sim has not absorbed.

**Corrections to prior records this session makes (reconcile, do not act on stale):**
- "Evicted kits become the bestiary" (prior recognition record) — **REFUTED.** Monsters are a separate generated bestiary with a closed archetype enum, not derived from kits `[fit-audit]`.
- Mega-boss = "anti-faction contrast-inversion lead" (prior record) — **SUPERSEDED.** v2 §8 sets mega-boss = "holdout champion beyond the base 400 / curated experimental kit"; v2 drops the anti-faction concept entirely (contrast moves to per-lieutenant Goldilocks temperature).
- Doc-38 Unreal platform layer — **decided-superseded but not formally restamped** (style-register retired Unreal; ground-state:52 still lists doc 38 CURRENT). KR restamp, flagged.

**What did NOT move this session:** the content-emission plumbing (two-tracks-don't-meet) — zero movement; still rocket/star-lord seam work. No code authored; this is a consolidation + capture session.

**Empirical criterion gating the next architectural commit:** the kit-vs-kit-temperature scoping (full-sim vs signal-heuristic) is the single highest-leverage resolution — recommend a joint gamora/star-lord scoping consult as the first forward move (PART IV). Until that scoping lands, Goldilocks/scouting/coverage-reward stay design-locked, not built.

**Signed:** gandalf, 2026-06-23.

---

## PART 0 — The frame: three targets, one game

### 0.1 The end state is the v2 gameplay loop

The game we are building is defined by `matt_notes_handoff_docs/reincarnated-gameplay-loop-design.md` (v2, canonical). One-line: **an ARPG where one spirit, bound to a dark patron, descends procedural dungeons, bests individuated champion-kits, and — by choice — *becomes* them ("you keep what you kill"), accumulating an endless roster that is the record of who it became.** Roguelite-shaped descent (L1→50 per run, resets), sawtooth power curve, Goldilocks matchup-fork at boss floors, grimoire capture-and-summon economy, atmospheric-dark (Synty-under-Godot-lighting), single home-realm creation with face propagation.

This doc does **not** re-litigate the design doc. It tracks the **engine's distance to it.**

### 0.2 The trajectory shift (what "slightly changed" means for the engine)

| Layer | v1 (prior) | v2 (now) | Engine impact |
|---|---|---|---|
| **Frame** | warm isekai / reborn traveler / spirit guide / earth realm | death-faith / ascending conqueror / **patron deity** / time-agnostic **home realm** | **None at the seam** — re-registration only; improves story. Prior cosmograph/earth-avatar canon needs reconciliation (PART III.9). |
| **Loop** | journey-as-descent (v1 release model) | **roguelite procedural descent** + Goldilocks fork + grimoire economy | **New demands**: kit-vs-kit temperature, per-kit level model, horde density (PART III). |
| **Build depth** | implicit | **explicit ARPG build-depth pillar** ("no meta," 400 unique, parametric abilities) | Parametric-ability realization (data-layer mostly present; Godot verbs unbuilt); scale-throughput. |
| **Combat density** | unspecified | **50-150 simultaneous** (perf doc) | Horde gap — sim caps at 8 (PART III.3). |

**The honest read:** the engine *direction* (validate kits in a battle sim → emit the engine's content for Godot) is unchanged. The v2 loop adds **new measurement demands** the current sim was never built to satisfy. The work is not a pivot; it is an extension whose long poles are now visible.

### 0.3 The two engine completion targets (unchanged definitions, now serving the v2 loop)

- **(A) Battle-sim complete** = the measurement instrument is *honest* AND the bands are *ruled + wired* AND the open balance calls are *dispositioned* — **and now additionally** measures what the v2 loop demands (matchup temperature, per-level scaling, horde density). PART I.
- **(B) Content-emission complete** = one driver emits all **six** engine content types (kits / monsters / factions / gear / weapons / flavortext) into a single Godot-consumable sim-ready bundle. PART II.

---

## PART I — Battle sim: current state → end state

### I.1 Current state (what exists, cited)

- **Sole substrate = the 2D spatial gauntlet** (1D sim deleted 2026-06-16, `gamora/v1.1-1d-sim-b6-deletion`). Tick-based (0.1s), physical/magical/hybrid routing, 7×7 resistance matrix, recompose-first balance loop (4 levers before modifier search).
- **Genuinely spatial** `[fit-audit]`: real arenas, entity radii, cone/line/circle AoE, chokepoints, flanking — the *ambition* of spatial encounter design is supported at the sim level.
- **Sole fight entry** `[fit-audit: spatial_engine.py:2944]`: one player class vs a list of monster dicts. **No second-kit slot. No kit-vs-kit path.**
- **6 arena shells, all cap ≤8 concurrent** `[gandalf-verified: arena.py]`: open_arena 8 swarm, chokepoint 8 swarm, boss_with_adds 3, magic_pack 4, elite_pack 3, mini_boss 3.
- **18 endgame encounters bind to those 6 shells** `[gandalf-verified: endgame_encounter_catalog.py:33]`; max composition = 8 (catalog lines 222/352/393/524/692); `mean_mobs_killed` golden-master = 8.0.
- **Validation at fixed L50 endgame** `[fit-audit: balance_loop.py:1935]`: flat-skill assumption, class stats unchanged across bands. L17/L33/L50 labels are *monster difficulty bands*, not kit levels.
- **Pass criterion**: kit ships iff ≥9/18 eligible encounters in-band (tier_2_kpm) for ≥1 of 4 cohorts.
- **Win-condition split (boss shells)**: survive-and-kill within 240s enrage, binary; DPS/TTK measured-never-gating `[d5b7ac2]`.
- **Defensive axis CLOSED + offensive bands FINAL** (2026-06-21 G-C close): dm=5.0 boss @ cadence 4.5s, swarm 0.20 LOCKED as calibration anchors; 0.926 unmatched-resist survive+kill a watch-item `[decisions-log 4562-4649]`. **Calibrated at ≤8 concurrent only.**
- **DPS is derived, not a gate** `[fit-audit: bounded_viability_validation.py:431]`: only a ≤1.5× cross-path variance check.
- **Summoner/proxy archetype is GATED OUT today — a GAP-TO-CLOSE, not a settled disposition** `[bc_target_composer.py:97,318 _DEFERRED_PROXY_BINS={proxy-light, proxy-heavy}]`: the sim is solo-only (legacy Profile-A), so proxy-creating kits cannot be evaluated and **every emitted kit carries `"proxies": []`** `[proxy_vocabulary_bridge.py:22-23]`. v2 makes summoning a **pillar** (grimoire §11/§13, summoner-identity §12/§17) → the engine is not to-spec until this is BUILT. See PART III.1b.

### I.2 End state (where the sim must go)

The honest-instrument + ruled-bands criterion (above) **plus** three v2-driven instrument extensions:
1. A **matchup-temperature** measurement (kit-relative "too hot / just right / too cold") for Goldilocks/scouting/coverage-reward.
2. A **per-kit level-scaling** model so the 1→50 descent, the sawtooth, and the +3-becoming are validated, not assumed.
3. A **horde-density regime** (≥50 concurrent) so KPM/defensive bands certify at play-density, not at 8.

### I.3 The gap (battle sim)

Carried B-series blockers (detail: predecessor spine doc): keystone-ceiling open_arena 1.000 WR zero-variance; caster coverage-bound (3.3× HP move = ΔWR ~0.02); trial-gallery NotImplementedError; summoner spatial-combat unbuilt. **PLUS the three v2-driven extensions** — these are the new long poles, detailed in PART III (items 1, 2, 3). The sim's *direction* is sound; its *finish line moved out* the moment the v2 loop named demands it was never built to measure.

---

## PART II — Content-emission pipeline: current state → end state

### II.1 Current state — two emit tracks that do not meet

```
TRACK NEW (cycle-14 wave5) → reincarnated-loadout app JSON
  run_season_production.py → kit-candidates → gauntlet+PM1 → mechanical-archive
    → cohesion-judge LLM (faction identity / names) → joint-gate → cycle14_wave5_emitter
  KIT+FACTION-RICH, but: no monsters; skill flavor_text NULL; main_weapon NULL.

TRACK OLD (season_exporter) → exports/<id>/{metadata,classes,monsters,gear_pool,...}.json
  SIM-READY bundle, but: kit/monster/gear-only (factions ABSENT, weapon=null);
  one-shot generate-season CLI driver DELETED (b6 deletion).

THE GAP: the two tracks never meet. No single driver emits all content into one
  Godot-consumable bundle. cycle-14 content never reaches season_exporter;
  season_exporter never gets factions / weapon-descriptors / cycle-14 kits.
```

**The six-content-type honest state** (NPC struck 2026-06-18 — "npc" = a companion/mercenary ally or future Engine-2 townsfolk, which is **future-product scope**, NOT one of the engine's six current content types):

| Type | State | Evidence |
|---|---|---|
| **kits** | WORKING (solo) / **summoner GATED-OUT (gap → III.1b)** | `classes.json` full stat_distribution + skills + LLM names; every kit emits `proxies:[]` — summoner archetype unbuilt, not "deferred" |
| **monsters** | WORKING (old track) / MISSING (cycle-14) | `monsters.json` 44 w/ stats+flavor; cycle-14 is kit-only |
| **factions** | PARTIAL — generated, never written to bundle | schema `schemas.py:1174`; `_export_season_inner()` never writes it |
| **gear** | WORKING | `gear_pool.json` 200 items + rolled_effects + LLM names |
| **weapons** | PARTIAL — identity in substrate, not emitted | `main_weapon=None` everywhere; lives in `substrate_weapon_binding` |
| **flavortext** | WORKING (class/monster/gear) / GAP (cycle-14 skill NULL) | `naming.py` live Anthropic calls |

### II.2 End state

One driver emitting all six types into one sim-ready Godot bundle, with the cycle-14 kit/faction richness and the old-track monster/gear completeness joined.

### II.3 The gap (emission) — mostly rocket/star-lord plumbing; gandalf surface = content-shape specs

- (a) single driver routing cycle-14 content through (or replacing) `season_exporter` — *star-lord/rocket*
- (b) monster generation wired into the cycle-14 track — *rocket/star-lord*
- (c) `faction_clusters` actually written — *star-lord, gated on the faction content-shape spec (gandalf)*
- (d) weapon descriptor wired `substrate_weapon_binding → main_weapon` — *star-lord, gated on the weapon content-shape spec (gandalf)*
- **NEW v2 emission demands** (PART III.6): encounter-geometry-per-floor (seam-ownership unresolved); faction as presentation-restyle only (the hard invariant — III.7).
- **Emission HELD / Matt-gated** `[export/MIGRATION.md v1.81-1.82]`: telemetry supports validation; it does NOT unlock emission.

**The bridge to Godot (Track B) does not exist** — content-consumption loader + GDScript combat-parity re-implementation are greenfield and the longest pole overall. This is downstream of both A and B.

---

## PART III — The v2-design engine-fit gaps (the new material, worst-first)

Each item: what the v2 design asks · what the engine currently does · the gap · resolution path · owner. Provenance-tagged.

### III.1 — KEYSTONE: kit-vs-kit matchup-temperature (Goldilocks) [HIGHEST LEVERAGE]

- **v2 asks** (§9): each boss floor offers 3-4 lieutenants at different **matchup temperatures relative to the current kit** (too hot / just right / too cold), regenerated on every reincarnation; scouting glyphs preview temperature; the matchup-coverage reward cashes against it.
- **Engine does**: only **global** kit-vs-control validation. **No kit-vs-kit path** `[fit-audit: spatial_engine.py:2944; mirror-duel retired balance_loop.py:2051]`.
- **Gap**: three mechanics (Goldilocks, scouting, coverage-reward) rest on a measurement the sim does not produce and that was deliberately removed.
- **Resolution path (gandalf lean):** Goldilocks needs a matchup-**temperature signal**, not a kit-vs-kit **fight**. Compute temperature as a lookup over already-emitted features — archetype + dominant_element + BC-signature distance + resistance profile (the Pokémon type-chart path). Cheap, reuses the emission surface, no second-kit sim slot. **Unvalidated (heuristic, not sim result); net-new either way.** The alternative — a true kit-vs-kit sim slot — is heavier net-new spatial-combat architecture.
- **Owner**: joint **gamora + star-lord scoping** (signal-heuristic vs full kit-vs-kit sim) — the first forward consult; **gandalf** design-fit on the temperature definition. **Resolve first; it gates the most.**

### III.1b — Summoner / player-side proxies (the grimoire-summon pillar) [HIGH — same multi-actor root as III.1]

- **v2 asks**: summoning is a **pillar**, not flavor — the grimoire capture-and-summon economy (§11), temporal summoning of coveted champions into your next dungeon at your level (§13), and **summoner-as-revealed-identity** ("a player who chooses summoner every time *is* a summoner," §12/§17). Player-side proxy combatants are core to the loop.
- **Engine does**: gates the entire proxy archetype OUT. `_DEFERRED_PROXY_BINS = {proxy-light, proxy-heavy}` `[bc_target_composer.py:97,318]`; `check_infeasibility` returns `is_deferred=True, reason="sim is solo-only (Profile A); proxy-creation mechanics absent"`. Every emitted kit carries `"proxies": []` `[proxy_vocabulary_bridge.py:22-23; schemas.py:1305 "production proxy_decls always [] → reads 0.0 on all real rows"]`.
- **Gap**: a **stale Profile-A artifact**, not a design disposition — and per Matt 2026-06-23 it does NOT survive as a deferral, because the v2 spec needs it. The sim cannot create, position, or resolve a player-summoned proxy that deals spatial damage / takes aggro.
- **Resolution path**: build the **player-side multi-actor path** — proxies as spatially-real combatants the player's kit creates (occupy position, deal/take damage, draw aggro). This is the **same root** as the III.1 kit-vs-kit keystone (the sim is single-actor-per-side); BUT it forces the harder branch — summoner viability genuinely needs the proxies *simulated*, so the III.1 type-chart heuristic does NOT discharge it. Un-gate `_DEFERRED_PROXY_BINS` only once the sim can evaluate proxy kits.
- **Owner**: **gamora** (multi-actor sim + proxy combat) + **rocket** (proxy-decl generation un-gate); **gandalf** design-fit on summoner viability bands + the grimoire-summon combat contract. **Scope jointly with III.1 — shared multi-actor-sim foundation.**

### III.2 — Per-kit level model (the descent is unvalidated)

- **v2 asks** (§6/§7/§8/§21): L1→50 per descent; sawtooth tuned to "power from ~2 levels prior"; +3-becoming reward; the spacing inequality (levels-per-champion ≤ levels-caught-up-between).
- **Engine does**: validates at a single fixed L50 endgame point; flat-skill assumption `[fit-audit: balance_loop.py:1935]`.
- **Gap**: "in-band" means in-band *at endgame against the control* — it says nothing about balance at L13 partway down a descent. The sawtooth, the +3-becoming, and the §21 inequality have **no validating instrument today**, and the §21 inequality is literally unfalsifiable without a per-level kit model.
- **Resolution path**: doc-33 progression absorbed into the sim — a per-level kit-scaling curve + a descent-band measurement. Substantial net-new.
- **Owner**: **gamora** (sim extension) + doc-33 progression lineage; **gandalf** scenario-design + the sawtooth-inequality stress-test spec.

### III.3 — Horde density (8 → 50-150) [gandalf-verified]

- **v2/perf asks**: 50-150 simultaneous hostiles (perf doc §3/§5; comfortable band, anti-target the PoE-juiced few-hundred); horde count is gameplay-critical and fixed across hardware tiers (a balance variable, not a render-only knob).
- **Engine does**: max **8** concurrent, ever `[gandalf-verified: arena.py 6 shells; endgame_encounter_catalog.py MobSpec max 8; mean_mobs_killed 8.0]`. The defensive axis (2026-06-21) was calibrated at ≤8.
- **Gap**: a 6-19× density gap. AoE-vs-single-target balance **inverts** with density (D3 vanilla→RoS; PoE Breach/Legion "AoE-or-die") — the same KPM band cannot judge both regimes. The engine has **no horde/gather primitive** `[arena.py:298-365: player-AI closes on nearest mob; no "reposition to GATHER into the AoE" primitive — and that was a struggle over eight mobs]`, so it cannot even *measure* AoE value at density.
- **Resolution path (gandalf recommendation):** a 7th gauntlet scenario **`SCENARIO_OVERRUN`** at the **comfortable-band floor (≥50, not the ceiling)** — "measure, don't assume" the peak. Re-fit KPM bands for the horde regime (its own bands). Build the **M1 horde-positioning primitive** (gather/funnel/kite) — the prerequisite and likely the longer pole. Expect a **defensive-axis re-fit** (50 swarm @ 0.20 ≈ 6× the incoming the bands were fit against). The 2026-06-21 close is valid *within its measured band*; the band moved.
- **Owner**: **gamora** (scenario + M1 primitive + band re-fit); **gandalf** (scenario-design spec + horde-regime KPM-band methodology).

### III.4 — The "hundreds" scale (54 today)

- **v2 asks** (§4/§20): ~400 in-band kits; the hook is the *scale that defeats netdecking* ("seven classes is the genre standard; here are four hundred").
- **Engine does**: ~54 candidates per run `[fit-audit: season_generation_pipeline.py:169 = 18 BC × 3]`; no "400" target; substrate-led, no pre-imposed N `[:41]`; ~2,293 active substrate rows could support more.
- **Gap**: the hook number is ~7× current output. **Not necessarily an architecture wall** — but the pipeline must *demonstrably* produce hundreds, and validation throughput at that scale is unproven.
- **gandalf refutation**: 400 is **illustrative, not a spec** — the design doc itself says "effectively endless." Treating it as a hard count fights the substrate-led discipline (Discipline #41, no pre-imposed N). The honest hook is "hundreds, generatively endless"; the real gap is **validation throughput for hundreds**, not a literal count.
- **Owner**: **rocket/gamora** scale-config + throughput; **gandalf** hook-honesty framing.

### III.5 — Monsters: "one pipeline, two roles" is aspiration, not build

- **v2 asks** (§4/§5): one pipeline, two roles (monsters = fixed control, kits = treatment); named champions (lieutenants/mega-boss) ARE kits, becomable; fodder monsters are not.
- **Engine does**: a **separate** generated bestiary — `ExportMonster`, closed archetype enum (brute/caster/swarmer/sniper/controller/tank), threat-tier, built via `build_reference_gauntlet`. **Monsters are not derived from kits** `[fit-audit]`.
- **Gap**: both the prior "evicted kits → bestiary" record and the doc's "one pipeline" framing describe a unification that does not exist. **The fodder/champion split the doc relies on is sound** (and matches the engine — fodder monsters vs becomable champion-kits); what's absent is monsters-as-role-partitioned-kits.
- **Resolution path**: design call — keep the separate fixed-control bestiary (cleanest for the sim's control-variable role) and source *named champions* from the kit pipeline (which the doc already wants), OR unify. **Lean: keep fodder-monsters as the fixed control (write-once, §4); source lieutenants/mega-boss from kits.** That satisfies the doc's becomable-champions ask without forcing monsters-from-kits.
- **Owner**: **gandalf** design call; **rocket/gamora** if any unification.

### III.6 — Encounter-geometry emission + a seam-ownership conflict

- **v2 asks** (§9): the engine emits per-floor encounter JSON "including room dimensions and structure … constructed around the lieutenant's strengths and the player's weaknesses."
- **Engine does**: season export carries **zero geometry** (kit/balance/stat only); the one geometry artifact is `arena_scenarios.json` — a Godot-only sidecar, 6 fixed shells (open_arena 50×50, chokepoint 10×50), not per-matchup-tuned `[fit-audit]`.
- **Conflict**: this collides with the prior seasonal-descent decision — "**engine emits content, Godot owns geometry.**" §9 says geometry comes from the engine. **Pick one.** (Good news: the sim *is* genuinely 2D-spatial, so spatial encounter design is supported; it's the *procedural-per-matchup generation* + *emission* that don't exist.)
- **Resolution path**: a seam-ownership ruling. **Lean: engine emits an encounter *intent* (composition + spatial-parameter hints derived from the matchup), Godot realizes geometry** — preserves "Godot owns geometry" while letting the matchup shape the fight. Avoids the engine owning room-mesh layout.
- **Owner**: **gandalf + drax + knight-rider** seam-ownership call.

### III.7 — Faction is walled out of combat (CORRECT discipline — endorse)

- **v2 asks** (§6): "each floor changes the faction and element of its enemies."
- **Engine does**: hard invariant — **zero faction fields enter the fight model; any faction field in a class/monster export raises a hard error** `[fit-audit: cycle14_unified_bundle_emitters.py:330]`.
- **Split**: **element** is mechanical and fully supported (first-class dominant_element + resistances; per-floor element rotation is real and validated). **faction can only be presentation-restyle** — it cannot make a fight harder or different.
- **gandalf endorsement**: this is **healthy discipline, not a gap** — it keeps the fight model clean (D2's act-bosses differ by *abilities*, not by a "faction" tag). **The design-doc language is loose, not the engine.** Any "this lieutenant is built against your weakness" difficulty must come from **element + archetype matchup**, never from faction. Re-seat the §6 contrast at the element/archetype layer.
- **Owner**: **gandalf** design-language correction; **no engine change.**

### III.8 — Corrections & narrower-than-feared items (briefer)

- **DPS is not a validated band** `[fit-audit: bounded_viability_validation.py:431]`. §4's "WR, KPM, and DPS all within ranges" overstates — WR + KPM gate; DPS is a ≤1.5× variance check. Minor.
- **Parametric abilities — partly already here.** The 16-type geometry palette (24 in production: chain_lightning, beam_channel, ground_slam, vortex_pull, whirlwind…) **is** the §20d "bounded library of ability primitives" — *at the data level*. Unbuilt: the Godot-side realization of each primitive as a distinct playable verb. The cash-condition is narrower than §20d fears — "realize the existing 16/24 primitives as verbs," not "invent a library."
- **Scouting glyphs — feasible, vocabulary mismatch.** `archetype_tag` + `role_orientation` are already emitted + surfaced in the demo UI. But engine labels (fire_mage, hunter…) ≠ the doc's "glass cannon / bruiser / controller" vocabulary. Needs a **label→glyph mapping** (respecting Discipline #41 — the presentation vocabulary maps to emergent clusters, does not pre-impose a taxonomy), not new generation.
- **Patron runtime banter (§15) — net-new online infra.** The engine's LLM layer is offline-batch (faction labels, kit identities, once per season). Runtime contextual banter is a different latency profile — not reusable existing plumbing. The doc's instinct to flag it as a real scope decision is correct.
- **Mega-boss source diverged** — reconcile (see SESSION-DELTA): prior "anti-faction" record superseded by v2 §8 "holdout champion beyond 400 / curated experimental kit."

### III.9 — Story-canon reconciliation (v2 supersedes a chunk of prior canon)

v2 re-registers the frame. The following prior canon needs reconciliation (a **named forward work item**, not resolved here):
- **isekai → death-faith** (§2): reincarnation *mechanic* + world-rotation survive, re-registered as conquest.
- **spirit guide → patron deity** (§2c/§14/§15): the guidance/companion role is now the antagonistic-helpful patron-voice. Reconcile against the **companion/mercenary ally** (future-product scope; `2026-06-13-companion-as-hall-of-heroes-ally-commitment.md`) — patron (guidance) and companion (ally) appear to be distinct entities; confirm.
- **earth realm → time-agnostic home realm** (§3): same structural function (one creation, face propagation, cultural-diversity-as-world-diversity); contemporary-Earth baggage shed. Reconcile against the earth-avatar/cosmograph creation-moment canon (`2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md`).
- **cosmograph re-anchored** (§2b): "the cosmograph is the patron's domain" — the night-sky-of-kits gains a native mythology. The cosmograph SURVIVES; reconcile the pivot docs (`2026-06-05-cosmograph-pivot.md`) to the patron framing.
- **Owner**: **gandalf** — a dedicated story-canon reconciliation pass (forward queue, PART IV). Do not silently let v2 and prior records contradict.

### III.10 — Deferral audit: what else is gated, and whether v2 needs it [Matt directive 2026-06-23]

Per Matt's build-to-spec ruling, every engine deferral is re-classified: **FLIP** (v2 needs it → gap-to-close), **FLAG** (needs Matt's ruling), or **KEEP** (genuine layer-handoff, not a scope-cut). Audited against engine source this session.

| Deferral | Code site | v2 read | Disposition |
|---|---|---|---|
| **proxy/summon bins** (proxy-light/heavy) | `bc_target_composer.py:97,318` | grimoire-summon pillar (§11/§13), summoner identity (§12/§17) | **FLIP → III.1b (high)** |
| **charge-stack** mechanic bin | `bc_target_composer.py:311` | stacking-resource build mechanic — the v2 thesis IS combat-build-depth | **FLIP (recommend) — build-depth** |
| **damage-taken-converts** mechanic bin | `bc_target_composer.py:312` | defensive→offensive conversion (PoE-class build mechanic) | **FLIP (recommend) — build-depth** |
| **support role** | `bc_target_composer.py:313` (Profile-A solo) | solo descent, BUT player-side proxies + companion ally (§14) create ally contexts | **FLAG — Matt: any ally/party context in v2?** |
| **HP-economy** | `bc_target_composer.py:326` (HARD-INFEASIBLE, LC-030) | Blood-Magic-class build mechanic; pool has ZERO HP-cost mechanics — a *substrate* gap, not a toggle | **FLAG — substrate acquisition, distinct from a flag-flip** |
| **VIT attribute** | `attribute-system-2026-05-24`; `emit_substrate_registry.py:116` | defensive/health-scaling attribute; deferred to "v1.1" | **FLAG — Matt: does v2 build-depth want VIT in?** |
| **T4 modifier algorithm** | `bounded_viability_validation.py:1477`; `sc7_calibration_loop.py:1058` | 4th-tier affix algorithm; "measured-for-record, Cycle 16+" | **FLAG — likely a real refinement-defer; confirm vs build-depth** |
| **element-conversion Variant-C ailment** | `damage_resolver.py:248` | ailment-on-conversion build-depth flavor; "Cycle 15 candidate" | **FLAG — build-depth flavor** |
| **`dodge_gated_deferred`** | `balance_loop.py` (terminal outcome) | NOT a scope-cut — hands glass-close-ST viability to the *piloted Godot dodge LAYER* | **KEEP — correct layer-handoff; done downstream, not omitted** |

**The pattern Matt named:** the engine accreted "deferred" dispositions under the old phased/Profile-A/Cycle-N staging. The v2 trajectory — *ARPG combat build-depth* — turns several of those into **direct removals of the thing the game is about** (summoner, charge-stack, damage-conversion, HP-cost are exactly the build-mechanic depth the hook promises). **gandalf recommendation:** flip proxy/summon (III.1b) + the two mechanic bins now; bring support-role / VIT / HP-economy / T4 / element-ailment to Matt as a single **build-depth-scope ruling**. Keep only `dodge_gated_deferred`.

- **Owner**: **gandalf** (the build-depth-scope ruling brief for Matt) + **gamora/rocket** (the un-gates). Forward-queue item (PART IV).

---

## PART IV — Owner map + forward queue

### IV.1 What's a gandalf chokepoint vs another seam's

| Work | Owner | gandalf surface |
|---|---|---|
| kit-vs-kit-temperature scoping | gamora + star-lord | design-fit on temperature definition (III.1) |
| summoner / player-side proxies (un-gate) | gamora + rocket | summoner viability bands + grimoire-summon combat contract (III.1b) |
| deferral audit → build-depth-scope ruling | gandalf → Matt | the flip/flag/keep brief (III.10) |
| per-kit level model | gamora + doc-33 | scenario-design + sawtooth-inequality spec (III.2) |
| `SCENARIO_OVERRUN` + M1 primitive + band re-fit | gamora | scenario-design spec + horde KPM-band methodology (III.3) |
| scale throughput (hundreds) | rocket/gamora | hook-honesty framing (III.4) |
| monster/champion sourcing | rocket/gamora | the design call (III.5) |
| encounter-geometry seam | drax + KR | the seam-ownership ruling (III.6) |
| emission plumbing (a)(b)(c)(d) | star-lord/rocket | faction + weapon **content-shape specs** (gandalf) |
| Godot bridge (loader + GDScript parity) | drax + engine | content-shape fidelity review |
| doc-38 Unreal restamp | knight-rider | flag (done) |

### IV.2 gandalf forward queue (priority order)

1. **Convene the multi-actor-sim scoping consult** (gamora + star-lord) — the keystone, with TWO faces sharing one root (the sim is single-actor-per-side): (a) **kit-vs-kit matchup-temperature** (III.1 — gates Goldilocks/scouting/coverage-reward; likely a signal-heuristic) and (b) **summoner / player-side proxies** (III.1b — the grimoire-summon pillar; needs proxies genuinely simulated). Author the design-fit brief framing heuristic-vs-full-sim for (a) and the proxy-combat contract for (b).
2. **Author the `SCENARIO_OVERRUN` design spec + horde-regime KPM-band methodology** — the verified, clock-on-it gap; every band locked at 8-concurrent is a band we may re-litigate.
3. **Author the deferral / build-depth-scope ruling brief for Matt** (III.10) — flip proxy/summon + charge-stack + damage-taken-converts now; bring support-role / VIT / HP-economy / T4 / element-ailment as one build-depth decision. Unblocks the un-gates; fast to author.
4. **Author the faction + weapon content-shape specs** — unblocks emission plumbing (c)(d); needed regardless of trajectory.
5. **Author the per-kit-level / sawtooth-inequality stress-test spec** — converts §7/§8/§21 from unfalsifiable to measurable.
6. **The story-canon reconciliation pass** (III.9) — v2 vs prior cosmograph/earth-avatar/companion records.
7. **The encounter-geometry seam-ownership ruling** (with drax + KR).

**Recommended first move:** #1 (multi-actor keystone — kit-vs-kit + summoner) and #2 (horde) carry the most leverage; #2 has a clock on it (8-concurrent band lock-in); #3 is a fast brief that unblocks the build-depth un-gates. #4 unblocks the spine regardless. Sequence per knight-rider; Matt approves.

---

## PART V — What genuinely fits (the honest picture)

So the survey is not all gaps:
- **The v2 frame fits cleanly** — death-faith / patron / home-realm touch no seam and improve the story; the theology-rhymes-with-mechanics is stronger than the isekai bridge.
- **The enemy-ontology split** (fodder monsters = MultiMesh; champions = CharacterBody3D) maps cleanly onto the Jolt+MultiMesh hybrid — a correct architecture call.
- **Elements are first-class and mechanical**; per-floor element rotation is real and validated.
- **The faction infrastructure** (clusters, relationships, 6-enum) is built — it just stays presentation-side (correctly).
- **The sim is more spatially capable** than the design doc assumes (real arenas, AoE shapes, flanking) — the *ambition* of spatial encounter design is supported.
- **The parametric-ability data layer** (16/24 primitives) already exists — the work is Godot-verb realization, not invention.
- **The faction-walled-from-combat invariant** is the engine being *right* — protect it.

**One operational note for drax:** the Godot prototype runs on Mac/Metal, which the perf doc names as the *flattering* machine. Looks-fine-on-Mac will not certify the GTX-1650 floor. Burn the density target into the drax workflow now.

---

**Signed:** gandalf, 2026-06-23 (founding entry). This doc is LIVING — the next gandalf session opens it at startup and updates it. The two completion targets (battle-sim, emission) and the v2-fit gaps (PART III) are the agenda until closed.
