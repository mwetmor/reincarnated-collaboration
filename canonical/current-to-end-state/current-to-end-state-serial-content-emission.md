# Current → End State — SERIAL CONTENT EMISSION PIPELINE (living tracker)

> **STATUS:** CANONICAL — CURRENT (load-bearing, LIVING). **Founded 2026-07-02** by Matt-ratified split from `current-to-end-state-engine.md` PART II (*"I do certainly agree with the separation/creation"*). Fourth ledger in the tracker family (engine / story / game / **serial-content-emission**).
>
> **What this tracks:** the **serial content emission pipeline** — the callable process that turns engine generation into LLM-named/flavored, sim-certified, disk-written content bundles (full seasons of kits / monsters / factions / gear / weapons / flavortext) consumable by player surfaces (loadout, Godot). It spans engine + LLM + export + consumption seams — a cross-seam *product*, not an engine-internal subsystem.
>
> **Protocol:** same as the sibling trackers — open at session start when emission work is in scope; prepend a SESSION-DELTA per state-changing session; **latest delta governs all body sections below it.**
>
> **Evidence substrate:** star-lord emission two-state inspection, `agentic_orchestration/star-lord/notes/2026-07-02-emission-two-state-inspection.md` (commit `9873c6b`) — every current-state claim below carries its verification.
>
> **Owners:** star-lord (export/LLM/telemetry seam lead) + rocket (generation-side) · gandalf (content-shape specs + this ledger) · drax (consumption surfaces) · gamora (sim-certification adjacency).

---

## SESSION-DELTA LOG (latest governs all below)

### 2026-07-02 — FOUNDING + four Matt rulings (split ratified · all-six-types demo bundle · zero hand-authored shipped content · dormant-T4 revival + proxy-T4 suite)

Founded from the engine tracker's PART II (now a pointer stub there) on the star-lord inspection substrate. **Four Matt rulings land at founding (rulings 1–3 at founding; ruling 4 same session, post-KR-run review):**

1. **Split RATIFIED** — this doc exists; PART II collapses to a stub. jack-ryan ratifies structure per `canonical-doc-format.md § 6.7` (rides the current KR team session).
2. **The demo bundle carries ALL SIX content types with FULL LLM flavor** — Matt overrules the one-realm §5.1 "weapon descriptors nice-not-critical / factions presentation-side-only" holds: *"I definitely don't agree with the demo not needing full LLM flavor, full weapons/gear and factions. Why hold them out?"* Post-inspection this is cheap: `emit_faction_block()` + `emit_weapon_descriptor()` are **built+validated, wiring-only**; gear writer works-when-called; flavor gaps are call-wiring. One-realm §4/§5 amended in place.
3. **Zero hand-authored shipped content** — *"They need to be balanced and pipeline emitted… we can pick from a seasonal emission of the serial content pipeline of battle-sim passed kits."* The demo roster = **curated selection from a REAL pipeline-emitted, gauntlet-passed seasonal run**. Consequences: (a) the summoner **content-emit un-gate moves DEMO-CRITICAL** (`_DEFERRED_PROXY_BINS` lift — already Matt-ratified as spec 2026-06-24 *"Thanks for flipping PROXY,"* now pulled onto the demo path); (b) D2's hand-authored proxy decls **re-purpose to calibration FIXTURES** (never shipped content); (c) a **demo emission run** (proxy bins live, post-D3-calibration) becomes the roster source — and run #1 in the registry (PART C).
4. **Dormant-T4 revival + PROXY-T4 SUITE, demo-critical** — *"Summon-focused kits MUST have a proxy-focused T4… we are expecting summon-kits to time out or die to boss if not for their proxy's DPS… will only one T4 work for all Proxies? I'm doubtful… We need to make all of the dormant T4 capstones alive in the engine (including proxyspawn) and we also need a full suite of proxy-T4's for the demo, so decent proxy kits can be emitted for selection."* Gap-queue row D.1 #9 carries it; #7 (demo emission run) now depends on it. **Timing note:** the bundle-v1 chain (D1 LOCKED-2 → D4 CLOSED) executed against pre-ruling scope — bundle-v1 is a **development bridge** (Godot D5/D6/D8 build against it); the **v2 demo emission run** (proxy bins + full T4 set live) is the shipping roster source.

**Direction registered (Matt, same session):** rebuild/assemble the pipeline as an **autonomously running, non-agentic, callable process** (triggered processes, results auto-written to disk), with **runs tracked in a database and eventually a website tracker**. Staged path adopted in PART C (callable → registered → triggered → surfaced). This gives the parked route-vs-replace choice (`P1_ARCHITECTURE_PARK`) a direction lean — formal un-park still Matt's, queued in PART E.

**Signed:** gandalf, 2026-07-02.

---

## PART A — What this pipeline IS

The serial content emission pipeline is the project's **content factory**: engine generation (BC discovery → gauntlet certification → mechanical archive) → LLM identity layer (names, flavor, faction narrative) → export (schema-validated bundles on disk) → consumption (loadout app today; Godot bundle loader per one-realm §6.1). §20d's honesty condition lives here: *the engine is the product* — every shipped kit is pipeline-emitted and sim-passed, never hand-built.

## PART B — Current state (inspection-verified 2026-07-02)

**Three tracks; the two main tracks never meet; no serial driver exists.**

| Track | Produces | Real / hollow |
|---|---|---|
| **NEW (cycle-14 wave5)** — `run_season_production.py` → `wave5_season_orchestrator.py` → phase-5 LLM → `cycle14_wave5_emitter.py` → `reincarnated-loadout/data/` | Named kits, 12 real skills, kit-level flavor, T4 fields, gear_representative (11 slots), season name | **LIVE LLM:** Wave A/F-C/Wave B/Wave S (~$0.85–1.00/season, `AsyncAnthropic`, anomaly guards). **Hollow:** skill `flavor_text` 100% NULL (60 sampled — `name_skill()` never called; phase-5 skill pass writes WS1A4 fields, not flavor); `proxies` key ABSENT; `main_weapon` NULL (explicit, WeaponSlot mismatch avoidance); no monsters, no gear pool; factions generated but never written to bundle |
| **OLD (season_exporter)** — `export_season()` → `exports/<id>/{metadata,classes,monsters,gear_pool}` | Sim-ready bundle *shape*: kits + 44 monsters/season + 200-item gear pool | **NEVER DRIVEN for a live season** (`exports/` = stale `v2_narrow` research artifacts only); stored seasons STUB-named (`class_0001`/`monster_00001`, flavor NULL — `name_class`/`name_monster`/`name_gear_item` paths exist, never run); CLI driver deleted at `4b089e3` (b6 — correct, legacy pre-spatial path); writes no factions/weapons |
| **THIRD (kit_space)** — `kit_space_emitter.py` (EAA-3/EAA-4) | Per-kit JSONs + chronicle | A kit-identity **store**, not a bundle. Live, independent. |

**Built-but-unwired assets (the cheap wins):** `emit_faction_block()` (`cycle14_unified_bundle_emitters.py:211`) · `emit_weapon_descriptor()` (`:522`, extracts `gear_representative.main_weapon.substrate_binding`) · `build_unified_season_content_blocks()` (`:620`, builds per-type blocks, assembles nothing) · full LLM naming layer (`llm/naming.py` + `TrackedLLMClient`).

**Summoner emission:** gated at composition — `_DEFERRED_PROXY_BINS = {proxy-light, proxy-heavy}` (`bc_target_composer.py:97,318`); the composer never deals a summon-verb kit, so zero summoners exist in any emitted season. The **fight mechanism is BUILT** (W1+W2 2026-06-22, engine tracker III.1b); the gate is generation-side only, plus scaffold magnitudes awaiting D3 calibration. Stale reason-string (`"sim is solo-only…"`) flagged for retirement.

**T4 capstones ARE in the pipeline:** alteration runs in `class_generator.generate()` pre-gauntlet; emitted ClassData carries `t4_alteration_output` / `t4_scope` / `t4_candidates` / `primary_t4`. Live strategy set is kit-universal (DirectDamageAmplification primary + TradeOffReversedFrenzy / ELEMENT_CONVERSION / GEOMETRY_COLLAPSE / RESOURCE_CONVERSION). η-floor (0.35) means not every kit draws one. **ProxySpawn** (the summon-*granting* capstone) is dependency-satisfied (W1/W2) + Matt-ratified to un-defer (2026-06-24) — rides the same un-gate + calibration as the bins.

## PART C — End state (the Matt vision, staged)

**End state:** an **autonomously running, non-agentic, callable pipeline** — a set of triggered processes that runs a full seasonal emission end-to-end (generation → gauntlet → LLM identity → six-type bundle → disk), **registers every run in a database** (run_id, git SHA, seed, config, counts, cost, verdicts, artifact paths), and surfaces run history on a **web tracker**. Agents BUILD and GATE the pipeline; the pipeline RUNS without them. (Industry pattern: the nightly content-bake / build-farm with dashboards; the discipline that matters is **reproducibility** — seed+SHA+config per run — and **dashboard-reads-registry, never artifacts**.)

The core is *already* non-agentic (callable scripts, programmatic LLM calls, pure-export emitters) — this is with the grain, not a rewrite. Stages:

1. **CALLABLE (demo window)** — one assembly driver produces the six-type bundle on invocation (D1 grows into this). No triggers yet — while the driver is still being reshaped, trigger-automation would constrict build speed; callable-first costs nothing.
2. **REGISTERED (demo window)** — the **run registry** table lands NOW (star-lord seam, telemetry-adjacent): every invocation writes a run record. Cheap, and history starts accumulating immediately — **the demo emission run is run #1.**
3. **TRIGGERED (post-demo)** — cron/CI layer fires scheduled emissions (nightly bakes); failure alerts; cost-anomaly guards already exist per-wave.
4. **SURFACED (post-demo)** — web run-tracker reading the registry (drax; loadout-adjacent surface already consumes emitted seasons).

## PART D — The gap queue

### D.1 DEMO-CRITICAL (the One Realm bundle — all six types, full flavor, zero authored content)

| # | Gap | Owner | Notes |
|---|---|---|---|
| 1 | **Assembly driver** (D1) — cycle-14 kits + old-track monsters + `_load_gear_pool()` + proxy decls → ONE bundle; **adds the missing `proxies` landing key**; writes a **stage-2 run record** | star-lord | Inspection-verified achievable; MIGRATION.md before tags (ADR-004) |
| 2 | **Flavor completion passes** — monster names/flavor (`name_monster()`, MUST — stubs unshippable) + skill flavor_text (`name_skill()`, fold-in) + gear names (`name_gear_item()`) over the demo season; **curated after generation** (D7 AI-tell line: LLM generates, we curate) | star-lord + gandalf curation | ~$1–3 order; infrastructure live |
| 3 | **Faction block wiring** — `emit_faction_block()` into the bundle | star-lord | Built+validated; Matt-ruled IN 2026-07-02 |
| 4 | **Weapon descriptor wiring** — `emit_weapon_descriptor()` into the bundle (substrate_binding path; avoids the WeaponSlot mismatch) | star-lord | Built+validated; Matt-ruled IN 2026-07-02 |
| 5 | **Gear pool for the demo season** — drive the 200-item writer against a live season + LLM naming | star-lord | Writer works-when-called |
| 6 | **Proxy calibration slice** (D3) — gamora derives the four scaffold magnitudes on D2 fixture decls; rocket applies | gamora → rocket | **✓ DONE 2026-07-02** — D3 cert (`gamora/v-proxy-fight-calibration-1` @ `abb010d`): four magnitudes **certified-HOLD** at scaffold values; 2 melee summoners PASS build-floor. #7's live dependency is #9 only |
| 7 | **Summoner un-gate + DEMO EMISSION RUN** — lift `_DEFERRED_PROXY_BINS`, retire the stale reason-string, run ONE real seasonal emission with proxy bins live **and the #9 T4 set live**; **demo roster curated from its gauntlet-passed output** (v2 supersedes the bundle-v1 bridge summoners) | rocket (un-gate) + star-lord (run) | Matt-ruled demo-critical 2026-07-02; run #1 in the registry; **depends on #6 + #9** |
| 8 | **Run registry (minimal)** — runs table + write-path in the driver | star-lord | Stage 2 of PART C |
| 9 | **Dormant-T4 revival + PROXY-T4 SUITE** — ALL five v1.1-dormant strategies go LIVE (ResourceBuffer, MechanicReplacement, ZoneControl, ConditionalModifier, ProxySpawn) **plus the RATIFIED catalog-v2 PROXY family** (PROXY_ASCENSION / PROXY_SOVEREIGNTY / PROXY_FISSION / PROXY_INVERSION / PROXY_CONVERGENCE / DUAL_PROXY — Session-1 rulings Q1–Q10, decisions-log 2026-06-12; `t4_catalog_v2.py:53-58`; generation-side wired, **execution-layer activation is the gap**), with η axis-match wired so summon-bearing kits score proxy-T4s high | rocket (strategies) + gamora (sim-eval extension + magnitudes) + gandalf (suite design spec + η integration intent) | **✓ Design spec AUTHORED 2026-07-02; REVISED IN PLACE same-day** (Matt prior-art catch: v1 drafted a parallel S1–S6 family missing the ratified catalog — v2 re-bases on the ratified six as the demo-activation + η/emission layer; two Matt rulings pending inside: §6 dormant-register binding, §7 demo-critical subset) — `canonical/reap-die-rise-engine/proxy-t4-suite-spec-2026-07-02.md` (**B1 fires against the REVISED spec**). **Matt-ruled 2026-07-02:** *"summon-focused kits MUST have a proxy-focused T4… we need a full suite of proxy-T4's for the demo, so decent proxy kits can be emitted for selection."* Evidence: W2 caster-alone WR 0.000 / D3 build-floor passes ride proxy DPS — a self-cast capstone amplifies the zero. Note: the v1.1 "sim-extension-required" labels predate the spatial sim — several dormant strategies may map to now-existing spatial mechanics (triggers/energy/AoE); rocket+gamora assess per-strategy |

### D.2 LAUNCH-SCOPE (unchanged unless re-ruled)

- **Unified serial driver** — route-vs-replace (`P1_ARCHITECTURE_PARK`, Tier-3 Matt PARK; direction lean registered, PART E) — star-lord/rocket
- **Monster generation wired into the cycle-14 track** (demo uses old-track monsters) — rocket/star-lord
- **Trigger layer** (scheduled emissions) + **web run-tracker** — star-lord + drax
- **Proxy emission share tuning** (~25% target) — rocket/gamora. ~~+ proxy-*amplifying* T4s at launch~~ **moved DEMO-CRITICAL 2026-07-02** (Matt proxy-T4 ruling → D.1 #9; launch keeps only share-tuning + suite *depth* beyond the demo family)
- **Faction/weapon content-shape specs** (gandalf) — demo wiring ships with inspection-shaped defaults; the full spec pass stays launch
- **Godot bundle loader** (consumption side) — drax, tracked in the game tracker (one-realm §6.1)

## PART E — Open Matt rulings

| Item | State |
|---|---|
| Route-vs-replace (`P1_ARCHITECTURE_PARK`) | PARKED Tier-3; **direction lean registered 2026-07-02** (autonomous-callable favors a unified driver with registry integration) — formal un-park when launch driver work starts |
| Run-registry schema | star-lord proposes; jack-ryan Gate-1; Matt ratifies |
| Web tracker placement (loadout-embedded vs standalone) | Open; drax proposes post-demo |
| Whether DirectDamageAmplification propagates to proxy damage | Calibration-adjacent question — D3 notes it; likely NO today (decl `damage_multiplier` is a separate surface) |
| **Ranged-proxy navigation gap** (D3 finding: `demo_gravecaller`'s archer proxy parks at 38.9 m, never closes — nav gap, not magnitude; defer-and-log at D3) | Blocks RANGED summoners from certifying in the v2 demo emission run. Matt rules: fix nav in the bundle-v2 engine wave, or **exclude ranged summoners from v2 curation** (melee summoners certify clean — D3 build-floor PASS ×2) |

---

**Signed:** gandalf, 2026-07-02 (founding). The factory is the product: every shipped soul is one the pipeline made and the sim passed.
