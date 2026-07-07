# Batch-2 run-state — the fresh 18-roster economy fire (staged, pilot-gated)

> **Governing spec:** `canonical/reap-die-rise-engine/batch2-build-spec-2026-07-06.md` (gandalf, ARCHITECT pass CLEAN).
> **Authorized:** Matt 2026-07-06 ("Fire per its §7"). **Orchestrator:** knight-rider.
> This file tracks leg-by-leg state; the spec is authoritative for intent.

---

## Sequence + live state

| Leg | What | Seam | State |
|---|---|---|---|
| A | economy-axes build (math-first) | rocket (+ gamora adjacency) | ✅ **DONE** — `legA-economy-axes-math-2026-07-06.md` (engine `ed6c349`) |
| A-gate | Gate-1 on the axis math (critique pair + sim consult) | jack-ryan + gandalf + gamora | ✅ **RATIFY-WITH-CONDITIONS** (all three) |
| B-build | wire the `resource_economy` loadout field (Route B) — cross-seam | rocket (emit) + gamora (consume) | ✅ **DONE** — emit `rocket/…-emit-1` (`9eca04c`) + consume `gamora/…-consume-1` (`7e1a5d1`); C3 round-trip GREEN, C4 default-corner 0.0-KPM CONFIRMED |
| B-gate | Gate-2 on the cross-seam field | jack-ryan | ✅ **PASS-WITH-FOLLOWUPS** (`77e634b`) — re-ran all suites, no BLOCK |
| B-sign-off | **ADR-002 cross-seam-schema sign-off on `resource_economy`** | **Matt** | ✅ **SIGNED 2026-07-06** |
| B-fire | economy pilot: 2 cells × 25 LHS-within-strata; pre-registered GO/HALT; PRODUCTION path | star-lord (fire) · gamora (read) | 🛑 **HALT** — 0/50 clear; verdict gamora (`6c5303b`) → escalated to Matt |
| C | full fresh 18-roster emission, all axes live, detached ~12–15h | star-lord (gamora shells) | ⛔ **HELD — does NOT auto-continue on HALT.** Awaiting Matt structural direction |
| close | batch-2 run report → elrond #18 consult | star-lord → elrond | pending C |

## Gate-1 disposition (2026-07-06) — RATIFY-WITH-CONDITIONS

- **Math / #1 / #1.2:** CLEAN — jack-ryan byte-checked every load-bearing citation.
- **Sweep-isolation #24:** AUDIT CLEAN — E1a⊥E1b (BETA fixed), `_CAST_TIME` excluded, not overloaded on the T4-keyed `gamora_combatant_fields` channel.
- **Structural-honesty:** PASS — default axis corner byte-reproduces the known 0.0-KPM chassis; ranges span outward from a failing center; HALT stays genuine.
- **Route decision: ROUTE B — LOCKED** (rocket + jack-ryan + gamora all concur). Single additive `resource_economy` loadout dict, init-consumed; sibling of the `t4_cost_resource` precedent.

**Frozen Route-B contract (the field that lands in B-build):**
`resource_economy = {cost_scale, cost_slope, regen_shape, regen_magnitude, on_kill_frac, ramp_per_s, cadence_scale}`

**Binding conditions (carried forward):**
- **C1 (jack-ryan) — 18-cell vocabulary fix → gandalf, BEFORE Leg C.** The engine BC space is **68,040 cells**; the "18" is a Matt-ruled demo-roster tiling target (1 kit/rostered cell), NOT a subset enumeration. Spec phrase "full 18-cell emission — every BC cell populated" conflates enumerable space with roster count. Leg A/B unaffected; must close before Leg C.
- **C2 (jack-ryan) — Route B ratified pending gamora concurrence** → gamora concurred → **firm.**
- **C3 (jack-ryan) — B-build carries MIGRATION.md + round-trip smoke; Gate-2 verifies** (ADR-004).
- **C4 (jack-ryan) — default-corner 0.0-KPM regression must be a HARD CHECKED ASSERTION in the pilot, not prose.**
- **gandalf G1 — Axis-5 coverage boundary (MATT-FACING RULING, before Leg C).** Resource economy is BC **Axis 5, a locked 7-bin substrate axis.** The mana-triple reaches the **4 statistical bins** (overflow/steady/generator-spender/starved) but CANNOT reach the **3 structural bins** (HP-economy / damage-taken-converts / charge-stack — keyed on cost-TYPE, not magnitude). Per spec §5, empty axis-bins make the clustering form factions around economy-*absence*. **Matt should rule the hole as a scoped decision, not inherit it after the faction cut.**
- **gandalf G2 — Leg-B report in Axis-5 identity terms** ("generator-spender cleared"), not lever-coordinates ("clear near c=0.7").
- **gandalf G3 — categorical-shape findings stamped pilot-confidence** (~4 LHS points/stratum is directional; densification is Leg C's job).
- **gamora carry-forwards:** (a) caster population is mana-default-only = the correct C2 instrument (build-spend economies deferred, separate rocket item); (b) **RUN PRECONDITION: `WIRE_RESOURCE_ECONOMY=True` must be asserted** — pilot fires inert if the flag is OFF (`spatial_engine.py:1221`); (c) Discipline #12 semantic-shift extends Phase-1; MIGRATION+round-trip with the B-build code.
- **gamora file-location correction (Discipline #11):** the binding fight loop is `spatial_gauntlet/spatial_engine.py` (regen tick `:2407`, energy gate `:1213/:1244`, cast decrement `:2136/:2319`, kill flip `:1506-1508/:1519-1521`), NOT `combatant.py` kernel. rocket's cites were correct as kernel cites; the wiring lands in spatial_engine.

## Gate-2 disposition (2026-07-06) — PASS-WITH-FOLLOWUPS (`77e634b`)

jack-ryan re-ran all suites (Disc #11, didn't trust GREEN): consume 7/7, emit 4/4, pathb-1a 35/35, generation 266 (superset of claimed 122), no Leg-1 regression. C4 confirmed a genuine hard assertion (exit≠0 on failure; re-ran → 0.0 KPM both shells + byte-identical to no-key path). Production-path instrument fact sound + documented. No contract drift; `_validate` rejects extra/missing keys. **Escalates to Matt for ADR-002 cross-seam-schema sign-off — engineering is PASS, this is a tiered-approval gate, not a defect.**

**Followups:**
- **FU-1 (jack-ryan):** decisions-log continuity entry for the Disc-#12 semantic shift (KPM now varies with per-kit economy identity) — jack-ryan authors.
- **FU-2 (star-lord pilot dispatch):** carry `assert WIRE_RESOURCE_ECONOMY is True` onto the PILOT run path (currently asserted in build smoke only) — **folded into the B-fire dispatch.**
- **FU-3 (rocket/gamora, cosmetic):** stale MIGRATION `file:line`s (read `:2694`→`:2780`; flips `:1506/:1519`→`:1536/:1550`) — code correct, citations drifted; batch on next touch.
- **FU-4 (optional):** add no-key==default byte-identity check to the smoke.

## B-fire VERDICT (2026-07-06) — 🛑 HALT (pre-registered, spec §3 — designed outcome, not a failure)

**gamora read `6c5303b`** (`simulation/notes/legB-economy-pilot-read-2026-07-06.md`). Run `617409b8…`, seed base `62_000_000`, 101.3s detached.

- **Formal call:** 0/25 plain-caster configs clear EITHER shell solo → 0/25 clear both → GO condition (i) fails. Sweep confirmed genuinely LIVE via all three anchors: C4 default-corner 0.0/0.0, production path (`from_player_class`→bounded pool, not un-starvable projection), FU-2 `WIRE_RESOURCE_ECONOMY` guard passed.
- **Landscape headline:** best open_arena config 1.0 vs 9.90 (**10.1% of floor, ~10× short**); best chokepoint 2.1 vs 11.65 (**18% of floor, ~5.5× short**). Gradient is **STEEP-but-SHORT** — economy levers HAVE grip (reorder configs), but the axis's ENTIRE dynamic range is worth ~1–2 KPM against a ~10–12 KPM requirement. **Economy tuning cannot close a 10× gap.**
- **Structural-honesty prediction CONFIRMED + sharpened:** the block is below the economy layer — not a bad-region-sampled miss. It's the whole economy layer that's insufficient (Leg-4 "band re-tune may be insufficient" confirmed).
- **Diagnostic seam (localizer):** caster is FINE on packs (3–4 KPM, economy-independent) and broken ONLY on single targets (1–2 KPM, economy-limited) → deficit localizes to **single-target damage-per-cast × cadence vs the 300k/500k HP wall** — a layer the economy cannot govern.
- **Economy-identity read (Axis-5, pilot-confidence):** warm-up/ramping got closest; builder-spender/on_kill dead-floor (chicken-and-egg: can't land the first kill to bootstrap the refund); cheap-sustained mid. Economy identity determines which caster feels LEAST-broken, not which is viable.
- **Summoner cell:** per-cohort measurement INTACT (Balanced/Hybrid scored separately across 25 econ_keys; the empty-`caster_proxy` miss did NOT recur). Certification machinery instrument-ready for when the structural block clears.

**Consequence:** Leg C is HELD (does not auto-continue on HALT). C1 vocab fix also parked — Leg C is not the next move regardless. **Escalated to Matt for structural direction** (analysis only; no fire recommended).

### Post-HALT structural diagnostic (2026-07-06) — gandalf finding → gamora ledger spike

- **gandalf finding** `gandalf/notes/2026-07-06-caster-single-target-structural-finding.md` — resolves the Leg-B HALT fork toward world (1) chassis-under-built with a NAMED mechanism: the weapon-era damage advantage fossilized into `BASE_PHYSICAL_DAMAGE_L50=48,012.6` vs `BASE_SPELL_DAMAGE_L50=20,532.2` (**2.3384×**); the AOE-pack channel (`damage_resolver.py:466-468`) compensated it at whole-encounter calibration; a lone wall zeroes the compensation and exposes the naked ratio. Arithmetic sanity: 9.90÷2.3384≈4.2 caster ceiling vs measured 1.0 → **~4× residual to decompose.** Fix forks: F-a REJECT (over-buffs trash-clear), **F-b geometry-keyed magical single-target premium (gandalf lean)**, F-c INT spell-crit channel (texture beside F-b), F-d REJECT (C2 floor stays).
- **gamora ledger spike** — dispatch `dispatches/2026-07-06-gamora-caster-single-target-ledger-spike.md` (Matt-approved 2026-07-06; committed `1b746e4`). ANALYSIS-ONLY: reproduce measured 1.0 KPM from named constants, decompose the ~4× residual, RANK the factors → sizes F-b/F-c as arithmetic. **COMPLETE** (engine `79796e2`, meta `fa6a065`; ledger `simulation/notes/caster-single-target-ledger-spike-2026-07-06.md`).

### Ledger spike RESULT (2026-07-06) — UNCLOSED; overturns gandalf §1–§4 arithmetic

- **Ledger does NOT close** — idealized per-cast throughput from named constants exceeds measured 1.0 KPM by **~3–6×**. The residual is **SPATIAL/geometry, not damage-arithmetic**, and **path-symmetric** (a martial single_target kit eats the same de-rating) → **NOT a caster-specific damage defect.**
- **The 2.3384× seed ratio is net-cancelled by pools.** INT scaffold weapon carries `spell_damage_modifier=90%` (1.90×, `substrate_weapon_binding.py:76`) vs martial `physical_damage_pct=5%` (1.05×); pool ratio 1.81× ≈ cancels the seed. **Net per-cast the caster is within ~1.07× of the martial** (even ahead after the martial's 15% dodge-gate tax). This directly contradicts gandalf §2 ("caster does 43% per cast, purely from the seed constant").
- **Ranked residuals:** (1) spatial single_target-vs-dispersed-8-mob-wall de-rating ~3–6× [path-symmetric]; (2) composition — pilot drew `support_specialist`, least-damage template, 5/9 attack slots — ~1.4–1.6×; (3) seed 2.34× raw / **~1.07× net of pools**; crit-EV ≤1.029× (negligible); resistance tax **0** (armor & resist symmetric, `combatant.py:1111`); investment NOT a residual (max-profile 1.0×).
- **Sized fix:** **F-b alone suffices; F-c recovers <3% (texture, not required).** CRITICAL: F-b must be sized to the **pool-adjusted** seed ratio (~1.3× with scaffold pools), **NOT the naked 2.34× or nominal 4×** — sizing to the naked ratio over-buffs. The rank-1 spatial/geometry residual is a **separate structural lever outside F-b/F-c scope.**
- **Two flags:** (a) the 9.90 martial bar EXCEEDS the 8-mob cap (`spatial_engine.py:2527`, no respawn) → NOT measured on the same wall as the caster's 1.0; part of the nominal "4×" is a **units mismatch**; F-b must calibrate on the identical wall. (b) The 90% spell pool is the **scaffold default** — the pilot's DB binding may differ; reading the exact value needs a re-emit (out of spike scope); the ledger brackets both.
- **CRITIQUE-PAIR CONTRADICTION:** gamora's ledger materially overturns gandalf's authored §1–§4 arithmetic + the F-b sizing basis. Steward (gandalf, finding author + F-b proposer) response pass warranted before Matt rules the fix fork. **Surfaced to Matt.**

### Critique-pair CONVERGED (gandalf §8 CORRECTION, commit `9fb3467`) — 2026-07-06

gandalf closed gamora's declared 0%→90% spell-pool bracket EMPIRICALLY (SC-6b enrichment LIVE: `weapon_sim_props` 2601/2601; INT avg 88.4% spell_damage_modifier, WIS 71.8, STR 7.3, DEX 5.2; the ~90% caster pool WAS live in the pilot via the un-nested gauntlet builder). **"43% per cast" RETRACTED**; true per-cast martial advantage ≈ **1.15–1.25×** (near-parity).

- **Inversion finding:** post-Path-α the substrate weapon does NOTHING for martials (physical pool fed only by `gear_set`={} in pilot) and +88% for casters. Today's near-parity is an ACCIDENT of two opposing legacy asymmetries (fossil 2.3384× seed × caster-only weapon pool). Fragile — moves when SC-6b shifts, loot lands, or WIS cells pilot (71.8 vs INT 88.4 → WIS ~9% behind from pool alone). Eventual fix should collapse both into ONE principled path×geometry surface with the weapon pool as an explicit term.
- **Reconciled defect stack (§8.3):** (1) bar/instrument mismatch [metrology]; (2) spatial/geometry single-target throughput, path-symmetric [design fork for Matt]; (3) composition (support_specialist draw) [sampling]; (4) residual damage asymmetry ~1.15–1.25× [F-b IF it survives re-measurement, sized to ~1.2× NOT 2.34×; F-c texture <3%]; (5) latent carried_gear nesting bug [wiring].

### 5-step sequencing (both stewards aligned; Matt-relayed 2026-07-06/07)

1. **Bar re-derivation** (gamora, metrology) — re-derive per-shell martial DISTRIBUTIONS on the instrument-matched Leg-B shells; pre-registered validity check (can martials reach 9.90 on the 8-mob dispersed wall?). NOT F-d. → dispatch `2026-07-07-gamora-caster-bar-re-derivation.md`. **Gate-1 RATIFY-WITH-CONDITIONS (jack-ryan, `70a6eab`); conditions folded (`c3444c4`). ✅ COMPLETE** (engine `8056f22`, tag `gamora/v-batch2-caster-bar-rederivation-1`; meta `b7e484f`; run `8e98a01d`).

   **RESULT — Q1 = NO on BOTH shells. The 9.90/11.65 bars were NEVER valid for this shell.** Batch-1 martials on the identical Leg-B instrument (8×300k open / 8×500k choke, dmod 0.3, 120s, production path) top out at **mean-mobs-killed = 8.0** — the metric is HARD-CAPPED at spawn count 8, no respawn (`spatial_engine.py:2527,3262`; `arena.py:366-378`). `8.0 < 9.90 < 11.65` → no martial at any power can reach the bars on an 8-mob wall. Metrology mismatch confirmed (NOT a caster-power defect, NOT a reason to move C2).
   - **Distribution:** ceiling-saturated + bimodal. **7 of 8 martial cells clear all 8** (mean 8.0, every template); ONE melee-DEX cell floors at ~1 (open)/~2–3 (choke) — a per-cell engagement stall on the dispersed high-HP wall. **This EMPIRICALLY CONFIRMS the path-symmetric single-target-throughput regime** the ledger named: a MARTIAL kit also stalls on the dispersed wall.
   - **Frozen clearing definition** (`frozen_clearing_definition` field, Gate-1 cond 1): ABSOLUTE mean-mobs-killed in fixed 120s, hard-capped at 8, no respawn, dmod 0.3, production path. `NOTE_FOR_STEP3` directs verbatim citation + no comparison against 9.90/11.65 as if reachable on 8 mobs.
   - **⚠️ LOAD-BEARING CONSEQUENCE for steps 3/4 (gamora flagged, not actioned):** because the martial mass SATURATES the 8.0 ceiling, this instrument CANNOT produce a martial distribution with headroom above the caster → cannot size a yield-rate-comparable F-b against it. **An INSTRUMENT-DESIGN decision precedes step 3/4:** more spawns / respawn / a kills-per-minute RATE metric (a different metric than absolute-kills-capped-at-8). → **surfaces the instrument-design fork below; converges with the step-5 geometry design session.**
2. **carried_gear shape fix** — RE-SCOPED rocket→star-lord after rocket STOP-and-flag (`b3e5658`/`802cf5e`). rocket inspected actual phase2 JSON: `gear_representative` (10-field slot, nested `substrate_binding` BY DESIGN) and `carried_gear` (flat binding) are CORRECTLY DIFFERENT shapes — the original "un-nest `:472`" premise was FALSE. KR verified every link (`:472` correct; `:1885-1890` bridge correct; `:2308-2322` validator correct; `cycle14_unified_bundle_emitters.py:538-576` reads `gear_representative` NOT `carried_gear` → unaffected). **REAL BUG:** `export/cycle13_normal_season_export.py:367-378` `_derive_carried_gear` returns `gear_representative` verbatim as `carried_gear` → persisted → read-back → combatant reads 0.0 spell pool. Fix = flatten in `_derive_carried_gear` to canonical pilot shape (`:1604`). → NEW dispatch `2026-07-07-star-lord-carried-gear-export-flatten.md` (`dd50f22`). **✅ FIX COMPLETE** (engine `64289f0`, tag `star-lord/v-batch2-carried-gear-export-flatten-1`). Open-Q1 RESOLVED = flatten SAFE (combatant is SOLE consumer of `carried_gear.main_weapon.spell_damage_modifier`; loadout uses separate `_derive_main_weapon` WeaponDescriptor + carried_gear null for all classes; demo CarriedGear is a different old-format contract; telemetry stores carried_gear opaque TEXT). `_derive_carried_gear` now returns `{"main_weapon": substrate_binding}` flat → combatant reads 0.72 (was 0.0). 5 round-trip smokes PASS (persisted read-back non-zero; pilot byte-equivalent no-regression; null-safety ×4; real static char None→None). cycle14 confirmed unaffected. MIGRATION lockstep ×3. **✅ Gate-2 PASS (jack-ryan, `f4431de`; qa/pending cleared).** Verdict PASS / severity INFO. jack-ryan verified against SOURCE (not smoke): single edit, byte-identical to pilot builder `:1604`, no scope creep; open-Q1 stress-tested (DB layer provably opaque TEXT; demo reads `carried_gear.weapon` never `.main_weapon` across all 11 live season `classes.json` → nothing starved); MIGRATION lockstep ×3 accurate. **One non-blocking INFO follow-up (star-lord discretion):** add a true end-to-end `recorder.persist → read-back → combatant.from_player_class` DB-row smoke to harden Principle 6 for the next persist-path touch. **STEP 2 FULLY CLOSED.** NOTE: refines gandalf §8.3 rank-5 mechanism LOCATION (export-path conflation, not decl `:472` nesting) — bug class unchanged; gandalf finding to reconcile on next engage.
   - _Superseded dispatch:_ `2026-07-07-rocket-gamora-carried-gear-nesting-unification.md` (Gate-1 `70a6eab`; STOP-flagged, closed no-code).
3. **Stratified re-pilot** (gamora) — role-split templates pinned/stratified; economy sweep re-run vs re-derived bars; GO = yield-rate comparability vs martial (finding §7.2), NOT bare floor-clearance. **⛔ BLOCKED — cannot proceed as specified.** Step 1 showed the 8-mob instrument saturates martials (no headroom) AND the bars are invalid on it → the re-pilot needs the redesigned instrument (fork below) FIRST.
4. **Residual assessment** — F-b sized to resolved ~1.2× ONLY if the gap survives re-measurement; F-c texture-only (<3%). **HELD — gates on step 3 + a valid instrument.**
5. **Leg C stays HELD.** The spatial/geometry fork (single-target rotation vs dispersed wall, path-symmetric) → Matt design session. **Empirical criterion now MET to convene it:** step 1 delivered the metrology finding (bars invalid on 8-mob wall) + empirical path-symmetry confirmation (melee-DEX martial also stalls). The instrument-design fork IS this design session's first decision.

### ⚑ INSTRUMENT-DESIGN FORK (Matt-facing; surfaced by step-1 saturation finding) — 2026-07-07

Step 1 proved the caster-viability measurement instrument is BROKEN in two ways: (a) the bars (9.90/11.65) exceed the 8-mob metric cap → invalid; (b) the 8-mob no-respawn wall saturates 7/8 martials at 8.0 → no headroom to distinguish caster-vs-martial or size a distribution-shaped F-b. **Steps 3–4 cannot fire on this instrument.** The decision that unblocks them:

- **What metric/shell measures single-target caster viability with martial headroom?** Candidates (gamora-flagged): more spawns; respawn; a **kills-per-minute RATE metric** (not absolute-kills-capped-at-8). Must preserve the two-shell C2 band structure (finding §7.1), never a whole-encounter median.
- **Convergence:** this is the SAME regime as the step-5 geometry fork (single-target-vs-dispersed-wall, path-symmetric). Recommend they be ONE Matt design session, informed by: gamora's ledger (`79796e2`), the step-1 report (`8056f22`), gandalf finding §7/§8.
- **Critique-pair candidates for the session:** gandalf (instrument/shell shape = C2-band design territory + the geometry fork = experiential); jack-ryan (metrology/measurement-validity). **Awaiting Matt: convene the design session, and who's in.**
- **Guard intact:** NO constants move; NO further compute fires until the instrument is ruled (firing a re-pilot on a saturating instrument = wasted compute, exactly what the pilot-gate discipline prevents).

**Guard intact:** NO constants move until step 3 empirical output + Matt fix ruling. recognition→validate→commit.

### ✅ INSTRUMENT FORK CLOSED — Q11 RATIFIED (Matt 2026-07-07) → four-family gauntlet instrument

Matt ruled the instrument-design fork: **"Ratify R1–R5 as drafted, assuming no issues on monster count for godot game's playable PC or mobile phone system specs."** Governing spec `canonical/reap-die-rise-engine/gauntlet-run-beat-families-spec.md` (RATIFIED). Fire order `gandalf/notes/2026-07-07-kr-relay-q11-fire-order.md`. The 9.90/11.65 bars are DEAD as certification targets (they presupposed throughput above the 8-mob supply cap); successors derive on the NEW instrument only.

**The new instrument = four run-beat families** (replaces the 6-room monster-tier ladder as the certification question; rooms largely survive as members/diagnostics):
- **F1 dense_cell** 16×22m / ~24 mobs (20 trash + 1 champion pack) — confined-space clear throughput.
- **F2 open_arena** 36×36m / re-populated 8→~40 (THE saturation repair) — spread-target throughput.
- **F3 boss_with_adds + mini_boss** ~30m + 1–2 timed add-waves — single-target boss viability (success-rate-judged, NOT KPM).
- **F4 escape_lane** 60×16m directional lane / continuous spawner, champion-elevated — the escape crescendo (NEW room; the purest spatial/geometry signal).
- **R4:** STR boss-shell carve-out RETIRES (pass ALL FOUR, no exemptions). Wall demotes to diagnostic; nothing deleted.
- **Two governing laws:** (a) fit-direction (bars answer to genre, kits are the subject); (b) one-spatial-contract (§3 dims ARE the Godot floor dims, authored once, both consumers read the spec).

**Three-lane fire order (dispatches authored 2026-07-07):**
| Lane | Owner | Task | State |
|---|---|---|---|
| 1 | gamora | feasibility pass + build the four family configs + R4 carve-out retire + wall→diagnostic + cost estimate | ✅ **BUILD DONE** (engine `8d45f95`, math note `657524a` before code, tag `gamora/v-batch2-gauntlet-four-family-instrument-1`; NOT pushed, Matt-gated). **→ Gate-2 FIRED (jack-ryan).** See result below |
| 2 | drax | perf-contingency spike (F2 ~40 + F4 continuous under Camera B vs 60-FPS floor, min-spec + mobile) — compose w/ pre-D7 horde spike + non-gating §7 camera-verify | ✅ **DONE — PASS** (godot `ba5547d`, tag intent `drax/v-godot-perf-contingency-spike-1`; NOT pushed, Matt-gated). See result below |
| 3 | jack-ryan | §6 metrology pass — derive bars on new instrument vs legolas genre bands + saturation guards + re-run martial/caster distributions + decisions-log registration | ⛔ **GATED on Lane 1** — `dispatches/2026-07-07-jack-ryan-gauntlet-metrology-pass.md`; triggers on Lane-1 Gate-2 PASS. ⚑ resolve the F2 camera-verify ±20% amendment (gandalf) in the window BEFORE this fires |

### Lane 1 RESULT (gamora, 2026-07-07) — BUILD DONE; Gate-2 in flight

- **Instrument built at spec §3 dims/populations.** F1 `dense_cell` NEW 16×22m/~24 (20 trash + champion pack of 4); `chokepoint_corridor` re-pop 8→24 (funnel kept); `magic_pack` re-roled champion-pack variant. **F2 `open_arena` re-dimensioned 50×50→36×36 + re-pop 8→40** (28 trash + 3 rare packs — the saturation repair). F3 `boss_with_adds` +2 timed add-waves (R5; injection verified 3→7 mobs at runtime). F4 `escape_lane` NEW 60×16m, continuous spawner (k=3/1s/cap50, seeded-deterministic), champion-elevation ×2.0, `escape_reached` win — population grows 12→50, the 8-mob no-respawn ceiling LIFTED by construction.
- **R4:** STR boss-shell carve-out RETIRED via new `family_certification_pass` (four-family gate). `gauntlet_pass` keeps the legacy floor until Lane-3 bars — the one-line flip is Lane 3's (confirm staging at Gate-2).
- **§4:** wall demoted to diagnostic `open_arena_wall_diag` (not deleted); six existing rooms survive.
- **Cross-seam (MIGRATION v1.84 → star-lord):** F4 fight-result fields `escape_reached` + `continuous_spawned_total` (claimed additive/brownfield-safe) + `mobs_killed` range semantic-shift. **Gate-2 verifies whether star-lord must consume before safe.**
- **Guardrails:** §3 dims read verbatim (no invented dims, no infeasibility→no spec-amendment flag); NO bar derivation; NO constant changes (byte-unchanged verified); build-smoke = "does-the-room-work" not certification. `mobs_killed=0` in smoke = fixture-DPS artifact (reproduces on known-good rooms) → Lane-3 concern, not a room defect (Gate-2 to assess). Compute (Disc #1.1): peak ~51 live entities on 8GB host, no bounds risk. Regression: 254 tests / 8 spatial suites pass, 2 updated.
- **Discipline #12 semantic-shifts** (R4 contract / open_arena re-base / mobs_killed range) routed to jack-ryan decisions-log.
- **→ Gate-2 FIRED (jack-ryan, scoped Gate-2 ONLY — Lane 3 held for the gandalf ±20% amendment).** Submission `qa/pending/2026-07-07-gamora-gauntlet-four-family-instrument-gate2-submission.md`.

### Lane 2 RESULT (drax, 2026-07-07) — PASS; Q11 re-open trigger NOT tripped

- **Perf spike PASS vs 60-FPS floor.** Rendered real Synty-class meshes (~6520-tri) under Camera B across F2 (40 concurrent, 36×36m: 45 draws / 111,876 tris), F4 (50 engaged, 16×60m: 75 draws / 190,136 tris), combo worst-case (72, 16×60m: 91 draws / 228,224 tris). Geometry load ~1–2% of a GTX-1650 budget; pessimistic 3× extrapolation clears 60 FPS >600 eq-FPS; mobile read ~380–510 eq-FPS before res/LOD lever. **→ §3 densities render-feasible AS-DRAFTED; NO population shrink; Lane 1 builds at ratified densities; Lane 3 bars derive on ratified populations.** Composed with the pre-D7 horde spike (one spike, two customers).
- **Honest limitation (carried):** Godot 4.6.3 Metal backend does NOT populate per-viewport GPU render time → verdict rests on geometry-load + render-CPU submit, NOT a GPU-ms figure. **Absolute GPU-ms certification remains Gate B on a real GTX-1650 (`matt_to_do` T2) before Next Fest.** The spike answered the CONTINGENCY (feasible? YES), not the CERT question.
- **Camera-verify finding → gandalf (spec-amendment flag, NON-BLOCKING):** measured legible width **~48.9m** (near-edge 40.6m, depth 36.5m) runs WIDER than the §7 estimate (~28–35m × 20–26m). F2's 36m fits with no clip. drax did NOT apply any dim change (one-spatial-contract law). Routed to gandalf open-thread `gandalf/open-threads/2026-07-07-F2-camera-verify-dim-amendment-flag.md` — options: (1) record measured anchor [hygiene, no churn] or (2) optionally widen F2 ±20% [re-points both consumers + shifts F2's travel-sensitive KPM bar]. **Recommended resolve window: after Lane 1 lands, before Lane 3 derives bars.**

**Then Steps 3–4 resume:** stratified re-pilot (vs the NEW bars) → F-b sizing ONLY if the gap survives re-measurement → Leg C. **Gate state until new-instrument numbers land: Leg C HELD, constants FROZEN, no F-fork adjudication.** Loot fairness campaign inherits the instrument as-built (one instrument, two customers).

**Guard intact:** NO constants move until Lane-1 build + Lane-3 metrology land + Step-3 re-pilot output + Matt fix ruling. recognition→validate→commit.

## Leg-C-entry gate (auto-continue is no longer blind)

Spec §8 D1 default = auto-continue Leg C on B-GO. Gate-1 added two Leg-C-gating findings that resolve **during the Leg-B window** (independent of the pilot fire):
1. **C1 — 18-cell vocab fix** (gandalf spec edit) — OPEN, gandalf before Leg C.
2. **gandalf G1 — Axis-5 structural-bin hole ruling** — ✅ **RULED by Matt 2026-07-06** (see below).

Leg C auto-continues on B-GO **AND** these two closed. HALT on B always escalates to Matt regardless.

### Axis-5 ruling (Matt 2026-07-06) — 3 structural bins INTENTIONALLY-EMPTY-FOR-NOW

The 3 structural-cost bins (**HP-economy / damage-taken-converts / charge-stack**) are ruled **intentionally-empty-for-now** in the batch-2 / faction derivation — the mana-default caster population by construction. NOT a gap; a scoped decision. Ships with **gandalf's three guards** (all binding):

- **Guard 1 — reserved, empty-by-ruling.** The 3 bins are recorded RESERVED / empty-by-ruling in the Axis-5 schema, and the **elrond #18 consult is told the coverage explicitly** (so the clustering does not silently form factions around economy-*absence*). → routing: gandalf annotates the axis schema; knight-rider briefs elrond at the derivation-step-3 consult.
- **Guard 2 — F5 re-derivation pre-registered as the arrival path.** When a structural-cost population ships, it enters as its **own build, own pilot, NEW-BRANCH entry**, and triggers **affected-cut re-ratification only** (not a full library re-derivation). → routing: pre-registered in decisions-log / spec (jack-ryan + gandalf).
- **Guard 3 — naming/flavor may not claim identity the population lacks.** The naming/flavor pass (derivation step 6) may NOT assign structural-cost identity (HP-cost, damage-converts, charge-stack flavor) to a population that is mana-default. → routing: constraint on the step-6 naming/flavor dispatch (gandalf).

## B-build result (2026-07-06) — Route B wired, binding CONFIRMED

- **Emit (rocket):** `resource_economy` on both loadout boundaries (`season_generation_pipeline.py:533`, `bc_target_player_class.py:428`), key always present, sibling of `proxies`. Sampler `generation/resource_economy.py` (LHS-within-6-strata, salt `1_800_000`). Emit smoke GREEN; regression clean.
- **Consume (gamora):** entity-init read `spatial_engine.py:2694` (`_econ = class_dict.get("resource_economy") or DEFAULT_RESOURCE_ECONOMY` — sim default IS the emit contract, no drift). Cost `:2745`, cadence `:2126`, regen `:2820`/ramp `:2440`. on_kill hook `_on_kill_energy_burst` at both flip sites (`:1536`/`:1549`).
- **C3 round-trip GREEN:** favorable corner moves a REAL season-001 caster off 0.0 KPM on both shells (open_arena 0.0→1.0/2.67 ramping; chokepoint 0.0→1.0).
- **C4 CONFIRMED (load-bearing):** default corner reproduces 0.0 KPM on BOTH shells + byte-identical to no-economy-key path → the binding is real.
- **Instrument fact (matters for the pilot fire):** economy bites ONLY on the PRODUCTION (bounded-pool) path — the projection/harness path pins `mana=1e9` and cannot starve (`spatial_resolver_adapter.py:192`). **The Leg-B pilot MUST fire through the production path.**
- **WIRE_RESOURCE_ECONOMY** precondition asserted on the run path.

## B-fire result (2026-07-06/07) — pilot FIRED, gamora reads GO/HALT

**Run ID:** `617409b8-3508-4a4f-a307-107c6f564246`
**Engine commits:** `bfb6097` (driver) + `3a09a4d` (artifacts)
**Wall time:** 101.3s — DETACHED nohup (PID 31410, exit 0)
**Seed base:** `62_000_000`

**Cells fired:**
- plain_caster: `endgame_bc_ranged_medium_variable_int_none` (proxy=none), 25 configs, calibrated mobs (300k/500k HP, dmod=0.3)
- summoner: `endgame_bc_ranged_medium_variable_int_none` (proxy=light), 25 configs, same calibration
- Third cell (D2): EXCLUDED — marginal cost not ~zero at config time; documented in run config

**Assertions confirmed on run path:**
- `WIRE_RESOURCE_ECONOMY is True` — PASS (FU-2 carried from Gate-2)
- Production path: `from_player_class` → bounded pool — CONFIRMED
- C4 default-corner: open_arena=0.0 KPM, chokepoint=0.0 KPM — PASS (HARD CHECKED ASSERTION)

**Measured landscape (gamora reads GO/HALT):**
- plain_caster open_arena: max KPM = 1.0 (bar lo 9.90); 0/25 configs clear
- plain_caster chokepoint: max KPM = 2.1 (bar lo 11.65); 0/25 configs clear
- n_configs_clearing_both: 0

**Measurement report:** `output/economy_pilot/economy_pilot_measurement_report.json` (schema `economy-pilot-v1`)
**Checkpoint:** `output/economy_pilot/economy_pilot_checkpoint.json`

Per-cohort bucket keys LIVE: `_econ_key()` encodes all 7 fields as stable string hash — no cohort collapse.

**GO/HALT verdict:** gamora reads and reports per spec §3 pre-registered criteria.

## QA / note trail
- jack-ryan Gate-1: `qa/pending/2026-07-06-legA-economy-axes-gate1-jackryan.md` (`bf2f571`)
- gandalf Gate-1: `gandalf/notes/2026-07-06-legA-economy-axes-gate1-gandalf.md` (`fdd9082`)
- gamora consult: `simulation/notes/2026-07-06-legA-economy-binding-consult.md` (`be6c7c6`)
- rocket axis math: `generation/notes/legA-economy-axes-math-2026-07-06.md` (`ed6c349`)
- star-lord B-fire driver: `export/economy_pilot_driver.py` (`bfb6097`)
- star-lord B-fire artifacts: `output/economy_pilot/` (`3a09a4d`)
