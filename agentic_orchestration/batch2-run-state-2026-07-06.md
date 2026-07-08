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
| 3 | jack-ryan | §6 metrology pass — derive bars on new instrument vs legolas genre bands + saturation guards + re-run martial/caster distributions + decisions-log registration | ✅ **DONE** (engine `e1f12b8`, main). Bars derived + guards PASS + re-run + decisions-log registered. See result below. **INSTRUMENT REBUILD COMPLETE.** |

### gandalf F2 dim-amendment RULING (2026-07-07) — OPTION 1 RECORD-ONLY (`02ca347`)

F2 stays **36×36m** (no widen). Measured anchor (~48.9m legible × 36.5m deep) recorded to spec §7 as the strongest absolute anchor, superseding the camera-geometry estimate. **Why not widen:** (1) 36×36 already fits the ~48.9m band with legible margin — reads full, no experiential defect; (2) widening raises repositioning cost + shifts F2's travel-sensitive KPM bar BEFORE Lane-3 derives it = fit-direction inversion one layer down; (3) legolas warning #2 (rooms >~50m read empty on a fixed camera) — widening walks toward the empty-room failure. **No gamora re-point; Lane 3 fires directly.** Secondary: §8.3 rank-5 nesting-bug location note reconciled (decl `:472` → export-path `_derive_carried_gear`; bug class unchanged).

### Lane 3 RESULT (jack-ryan, 2026-07-07) — bars derived; INSTRUMENT REBUILD COMPLETE; ⚑ MATT DECISION POINT

**Derived per-family bars (ALL provisional-hypotheses-pending-playtest; from legolas genre bands as external reference, NEVER fitted to kits):**
| Family | Metric | Bar |
|---|---|---|
| F1 | KPM | floor 30 / ceiling 60; WR ≥0.95 |
| F2 | KPM | floor 20 / ceiling 40; WR ∈[0.85, 0.95] |
| F3 | **success-rate + TTK (NOT KPM)** | WR/attempt ∈[0.60, 0.80]; boss-TTK rail 15–90s (<15s = overpowered flag); KPM wide sanity rail only |
| F4 | KPM + progress + exit | KPM floor 60 / ceiling 150; exit-within-window ≥0.80 |

**Saturation guards (§5 headroom law) — all four PASS, registered not just applied:** F1 24≥20, F2 40≥13.3, F4 by-construction (~180 stream > 150 ceiling), F3 exempt (success-judged). **The KPM RATE metric (declared distinct from Step-1's absolute-count) removes the supply-ceiling pin that killed the dead 9.90/11.65 bars.**

**Re-run on the NEW instrument (80.9s, seed 64M, native threat-tier HP — NO dead 300k/500k wall):**
- **F1** — HEALTHY, non-saturated: martial KPM median 45.3 in-band, 25/40 pass; **casters 2/2.**
- **F2** — KPM fine (median 42.3) but WR saturates 1.0 (above 0.85–0.95) → 0/40 pass.
- **F3** — WR=1.0 (above 0.60–0.80) + TTK median 6.0s (below 15–90s rail) → overpowered-flag → 0/40 pass.
- **F4** — exit median 1.0 (escape resolves); martial KPM median 23.9 BELOW the 60 floor → 5/40 KPM-half; **casters 2/2.**

**⭐ REFRAMING (the load-bearing takeaway):** on the properly-populated instrument with native HP, **casters PASS the cells they ran (F1 2/2, F4 2/2)** — the original ~10× caster shortfall was substantially a DEAD-WALL + saturation-cap ARTIFACT, not a caster damage defect. The remaining misses (F2/F3 WR saturation, F3 sub-rail TTK, F4 martial-KPM-below-floor) are **native-HP / mob-LETHALITY calibration signals — NOT bar moves (fit-direction) and NOT caster-vs-martial asymmetry.** jack-ryan flags: Step-3 re-pilot tunes mob lethality to exercise the WR-competency bands. **This puts the F-b caster-damage-premium fork increasingly in question — Step 3 confirms empirically.** (Caster n is small — 2 cells — so Step 3 stratification is the real test.)

**Decisions-log registered (jack-ryan owns it):** Q11 ratification + both governing laws (fit-direction, one-spatial-contract) + all three Disc-#12 semantic shifts (R4 cert-contract, open_arena re-base, mobs_killed range).

**Two downstream flags to route — BOTH queued for Step-3/4 resume, NOT fired (gated on Matt ruling):**
1. **R4 ship-gate one-line flip** — gamora added `family_certification_pass()` (`gauntlet_sim.py:771`) but `gauntlet_pass()` (`:812`) still reads the legacy ≥9-of-18 W-α6 floor. Wiring one into the other IS the R4 flip. **gamora's seam** — dispatch when Step 3/4 resumes.
2. **star-lord telemetry MIGRATION** — `escape_reached` + `continuous_spawned_total` (`spatial_engine.py:2868-2869`) + `mobs_killed` range shift (F4 unbounded by initial spawn). Telemetry-boundary; star-lord consumes `mean_mobs_killed`. **star-lord's seam** — fire when export/persistence needs F4 telemetry on-disk.

**Work-products (`e1f12b8`, main):** `simulation/math/gauntlet-four-family-metrology-2026-07-07.md` (bands→bars + guards + re-run §7) · `simulation/gauntlet_four_family_metrology_driver.py` · `output/gauntlet_four_family_metrology/metrology_report.json` · `design/decisions/decisions-log.md`.

**⚑ MATT DECISION POINT — ✅ RULED 2026-07-07: GO on reshaped Step 3** (mob-lethality calibration + stratified caster+martial re-pilot vs the new bars). F-b held confirm-unneeded — the re-pilot IS its closing criterion (parity beyond the 2-cell caster sample ⇒ F-b retires to git). Three riders + two precisions folded verbatim into the gamora dispatch.

### Step 3 GO (Matt 2026-07-07) — riders + precisions + 3-dispatch fan-out

**Riders (binding):** (1) pre-registered calibration split by knob — (a) mob damage UP → F2 WR 0.85–0.95 + F3 WR 0.60–0.80; (b) F3 boss HP → boss TTK 15–90s (6000 was placeholder); reference pop = stratified pilot pop (both paths, template-stratified per seventh-entry finding), never curated subset; bands/bars do NOT move (fit-direction one layer down). (2) F4-martial stays OUT of room-calibration bucket = the KIT finding; MEASURED in re-pilot, disposition kit-side (AOE/cleave), NOT fired in Step 3. (3) miss-taxonomy split under-floor/over-ceiling/WR-side; floor = hard cert line; **ceiling = OVERPOWERED flag → balance review, NOT auto-fail** (matches F3 overpowered-flag + doc-50 bounded-viability).
**Precisions (binding):** (1) **FREEZE SPLITS** — kit-side chassis constants (BASE_PHYSICAL/SPELL_DAMAGE_L50 + kin, 2.3384× fossil) remain FROZEN (Matt rules after re-pilot numbers land); room-side mob constants (damage scalars, boss HP, MOB_HP_DIFFICULTY_MULTIPLIER-class) explicitly UNFROZEN for the calibration (the unfreeze IS the point of Step 3). (2) the two queued flags fire with this go.

**3 dispatches FIRED in parallel 2026-07-07:**
| Dispatch | Owner | Scope | State |
|---|---|---|---|
| `2026-07-07-gamora-step3-mob-lethality-calibration-stratified-repilot.md` | gamora | 2-lever calibration + stratified re-pilot + miss-taxonomy report + F4-martial measure-only + **R4 ship-gate flip** + F-b parity read | ✅ DONE (`08972d0`, tag `gamora/v-batch2-step3-mob-lethality-calibration-1`) — **STOP-and-flagged the calibration (#24 guard fired = DEAD MOB-DAMAGE CHANNEL finding); R4 flip executed.** **jack-ryan Gate-2 (`38b5a30`): R4 = PASS-WITH-FOLLOWUPS; dead-channel = DIAGNOSIS CONFIRMED + fix ENDORSED; §7 bars+KPM+caster-PASS-verdict SURVIVE (only F2/F3 WR=1.0 re-attributed, margins re-confirm post-fix).** ⚑ Instrument-fix ruling (A/B/C) at Matt |
| `2026-07-07-star-lord-f4-telemetry-migration-consume.md` | star-lord | MIGRATION v1.84 CONSUME — persist `escape_reached`+`continuous_spawned_total`, scope-relax `mobs_killed` invariant (F4 continuous), round-trip smoke | ✅ DONE (`7d999db`) — **Gate-2 PASS (jack-ryan, `984981b`, no BLOCK)**; finding `qa/findings/2026-07-07-star-lord-f4-telemetry-consume-gate2.md`; prod-DB apply PENDING Matt (ADR-006) |
| jack-ryan (Pattern-A, no dispatch file) | jack-ryan | Rider-3 semantics registration (decisions-log) + **Disc-#24 methodology check** on the F3 two-knob coupling (report FAST if confounded so KR relays to gamora before she tunes) | ✅ DONE (`2bfa599`) — semantics registered + #24 verdict CONFOUNDED-but-resolvable |

**#24 hotspot:** lever (a) mob damage + lever (b) F3 boss HP BOTH touch F3 (damage→WR, HP→TTK, HP secondary WR). gamora math-note pre-registers sweep isolation w/ STOP-and-flag; jack-ryan parallel-checks; gamora's math-note is the checkpoint before tuning.

**#24 RESOLUTION (jack-ryan, `2bfa599`) — CONFOUNDED (on F3 WR), but resolvable.** Isolation protocol jack-ryan authored:
1. **Fix mob damage FIRST on F2** (the clean single-knob family) — lock the mob-damage scalar on F2 WR ∈ 0.85–0.95.
2. **Carry the locked mob-damage into F3, then sweep boss HP ALONE against F3 TTK** — lock boss HP on TTK ∈ 15–90s.
3. **Read F3 WR LAST, as an OUTPUT — do NOT tune to it.** If F3 WR misses 0.60–0.80 after (1)+(2), that is a *finding* (rooms not lethal enough at the F2-locked scalar) → **STOP and flag to KR**, do not add a third knob.
jack-ryan's note: this **composes with — does not override — gamora's math-note checkpoint.** If her pre-registered isolation plan already sequences F2-first / boss-HP-on-TTK / WR-as-readout, it is clean as-written and the protocol is a *confirm*.

**⚠ RELAY CONSTRAINT (KR, honest):** no live-messaging channel to the in-flight gamora agent exists in this session (SendMessage not surfaced; TaskStop would be destructive). The relay could NOT be injected mid-run. The protocol's intent is nonetheless **structurally guarded** by gamora's dispatch: (i) math-note committed BEFORE any tuning + (ii) explicit STOP-and-flag on the F3 coupling. **Enforcement point that IS still open: jack-ryan Gate-2 on the Step-3 tag becomes a HARD verification criterion — gamora's math-note MUST show F2-first / boss-HP-on-TTK / WR-as-readout sequencing, or a coupling flag.** If gamora's math-note derives a less-clean isolation and she tuned before flagging, that surfaces at Gate-2 as a re-tune, not a silent pass.

### gamora Step-3 RESULT (2026-07-07) — STOP-and-flag: DEAD MOB-DAMAGE CHANNEL; R4 flip executed (`08972d0`)

**⭐ THE FINDING (the #24 guard did its job — no blind tuning):** the pre-registered calibration **cannot execute on the instrument as-built**, so **NO knob was moved, NO constant touched.** gamora's mandatory pre-tuning probe (`simulation/scripts/gamora_step3_calibration_probe_2026_07_07.py`, results `simulation/output/step3_calibration/step3_probe.json`) found:
- **Lever (a) "mob damage UP" has ZERO grip.** Mob damage-per-hit = **0.0**, unchanged across `damage_multiplier` 1×→32× (direct `resolve_spatial_hit` measurement + F3 sweep). **Root cause:** the metrology driver's `_build_standard_mob_dicts` AND the Lane-1 build smoke hand-roll a **damage-less** mob dict (`effect_category` string, not an `effects` list). Typed death channel is selected but `resolve_skill` accumulates only effects named `"damage"` → zero effects → zero mob damage → `MOB_DAMAGE_SCALE` inert. **The rooms don't kill functional kits because the mob-damage channel is structurally DEAD — not "too easy" in a tunable sense.** This REFINES jack-ryan's §7 WR=1.0 reading.
- **Lever (b) boss HP** moves TTK a little (9.5→13.4s at 400k) but never reaches the 15s floor nor moves WR off 1.0.
- **Canonical fix gamora proved:** `spatial_engine.py:3122` `emit_skills_for_threat_tier` is the intended mob-skill source — emits live `"damage"` effects (swarm dm 0.85, boss dm 5.0, mag 1000). Both instrument builders BYPASS it. Sourcing from it restores full linear lever-(a) grip and opens a genuine two-sided tunable surface (dead channel → WR 1.0; canonical-full → WR 0.0 at dm=1.0; tunable middle between). Because living the channel **changes what jack-ryan derived bars against**, she STOPPED and flagged per dispatch.
- **Miss-taxonomy re-pilot:** on the dead-channel instrument all misses are over-ceiling/WR-side (WR=1.0) for F1/F2/F3 + F4-martial under-floor (KPM); the meaningful split needs the lived-channel re-pilot (post-ruling).
- **F4-martial KPM:** median **23.9** (below 60 floor), measured-only (Rider 2), NOT re-measured under mob-HP rise (calibration STOP precedes any tune). Kit-side, deferred.
- **F-b parity read:** on dead channel both martial+caster saturate WR=1.0; on canonical-full both collapse ~0.0 — **no caster-vs-martial asymmetry in either regime (consistent with F-b confirm-unneeded)**, but the definitive closing read needs the calibrated lived-channel stratified re-pilot. Parity holds on evidence so far; closing read PENDING calibrated re-pilot.

**R4 ship-gate flip (Precision 2 — executed independently of the STOP):** `gauntlet_pass()` (`gauntlet_sim.py:854`) now routes to `family_certification_pass()` — four-family conjunction, STR carve-out retires. Disc-#12 framed in-code + MIGRATION v1.85. **Cross-seam (no schema change):** R4 tightening contracts `season_emit` → rocket's `season_generation_pipeline.py` season-content set drops to zero until Lane-3 registers the F4 band + calibration lands (correct not-yet-certifiable state). Regression: `test_cycle13_wave5_gauntlet_sim` 50/50 (5 legacy-floor tests rewritten to four-family contract), 151/151 across four `gauntlet_pass`-referencing suites, 868 PASS broader slice (1 pre-existing P5-LLM-seam fail, stash-verified not gamora's). star-lord F4-telemetry already landed (`7d999db`) — no in-memory gap.

**⚑ ESCALATION (gamora → KR → Matt) — instrument-fix ruling needed (math-note §5, three sub-questions):**
- **(A)** confirm sourcing metrology + build-smoke mob dicts from `emit_skills_for_threat_tier`, then sweep a mob-damage scalar.
- **(B)** `signature_element` per tier for the emitter.
- **(C)** whether F4 continuous-spawn fodder shares the dead-effect defect (probe covered F2/F3 only).
Constants FROZEN; no further compute fires until the instrument is ruled.

**→ jack-ryan Gate-2 ✅ (both parts, `38b5a30`; pending cleared). Finding `qa/findings/2026-07-07-gamora-step3-mob-lethality-calibration-r4-flip-gate2.md`:**
- **PART 1 — R4 flip: PASS-WITH-FOLLOWUPS.** Flip correct at source; legacy ≥9-of-18 floor fully retired as ship gate (kept as diagnostic lineage, not half-wired); STR carve-out retires. Independently re-ran: **50/50** rewritten suite + **151/151** four named suites + a **6th API-referencing suite 49/49 (not broken)**; the 5 rewritten tests were **TIGHTENED not loosened** (boss-only kit that passed old 18/18 now returns False; each cross-checks `gauntlet_pass == family_certification_pass`). P5 cohesion-judge fail reproduced in isolation, structurally not gamora's. `season_emit→zero` = TRUE GATE not regression (F4 band unregistered → cert universally False today), correctly doc'd MIGRATION v1.85. **WARN (non-blocking, jack-ryan pre-approved doc-only fix under ADR-002):** three docstring spans (`gauntlet_sim.py:781-783`, `:833-835`, `:897-898`) still narrate pre-flip state → Disc-#12 hygiene; **queued gamora doc-fix.** **rocket INFO owed (via KR):** a zero-emit season-gen run is EXPECTED, not a regression — no rocket schema/code action, no consumer MIGRATION entry.
- **PART 2 — dead-channel: DIAGNOSIS CONFIRMED (reproduced at mechanism: 0.0 dmg/hit at dm=1× AND 32×; a live-`damage`-effect dict yields 1522.9 dmg/hit scaling linearly). FIX ENDORSED.**
- **§7-SURVIVAL DETERMINATION (the crux):** **bars survive WHOLE** (genre-anchored, fit-direction — a room defect never moves a bar); **all KPM dispositions survive** (dead-channel-independent); **the caster-PASS reframe survives as a VERDICT** — both caster passes are gated on a KPM component (F1 39.5∈[30,60]; F4 71.8≥60) + one-sided floors (WR≥0.95, exit≥0.80) that WR/exit=1.0 satisfy regardless of mob damage; a lived channel can only LOWER those, never manufacture a pass → dead channel did NOT fabricate the caster passes. **PRECISION correcting "fully unaffected":** the WR=1.0/exit=1.0 *margins* on those passes ARE dead-channel-inflated + unmeasured → margins (not the verdict) must be re-confirmed post-fix. **The one re-attributed signal:** F2/F3 WR=1.0 saturation was a dead-channel artifact (not "rooms too easy" tunably) → re-read on the lived instrument. Nothing in §7 invalidated; ~one signal re-attributed.
- **Fix concerns that VALIDATE gamora's ruling-asks:** **(B)** `emit_skills_for_threat_tier("boss",...)` **REJECTS `physical`** — signature_element must be one of the 7 rotating elements → the genre-neutral choice is a genuine per-run parameter needing a ruling. **(C)** the F4 continuous-spawn fodder path was NOT probed, may share the dead-effect defect → must be checked before the full re-pilot (ties to the F4 caster-margin caveat).
- **jack-ryan is HOLDING the decisions-log Q11-Step3 entry pending Matt's ruling** (so it records the DECISION, not just the flag).

### ⚑ Matt instrument-fix ruling + canon directives (2026-07-07) — Step-3 redux FIRED

**Instrument-fix ruling (VERBATIM):** "Authorize A and C. B: deterministic within-kit rotation across the full 7-element wheel — every kit faces the identical seeded element schedule; certification judged on the wheel average; worst-element recorded as a diagnostic flag, not a gate. Pre-register the lever-(b) TTK-saturation anomaly for a mechanism check post-fix."
- **(A) authorized** — source both mob-dict builders from `emit_skills_for_threat_tier` + sweep. **(C) authorized** — F4-fodder dead-effect check. **(B) ruled** — 7-element wheel, kit-invariant seeded schedule, cert on WHEEL AVERAGE, worst-element = diagnostic-flag-not-gate. **TTK-saturation anomaly** pre-registered for a falsifiable post-fix mechanism check.

**Canon directives (VERBATIM):** "ratify the one-pilot-policy contract (gandalf's 2026-07-07 recognition note) as canon — jack-ryan adds it to the decisions-log beside the two laws; stamp all derived bands/certs with pilot_policy version; GOAP is cut; utility-scorer direction approved for when the Godot combat layer scopes. F4-martial: pilot-attribution probe gates any kit-side design response post-re-pilot."
- **One-pilot-policy contract RATIFIED as the THIRD governing law** (beside fit-direction + one-spatial-contract): pilot policy authored ONCE, deterministic+seeded, consumed by BOTH sim gauntlet + Godot combat layer; human-feel diffs are registered degradations of the same policy, never a second policy; planned-re-derivation corollary on ship-pilot upgrade. Source note `gandalf/notes/2026-07-07-pilot-policy-contract-recognition.md`.
- **`pilot_policy` version stamp** on all derived bands + certs (traceability; policy upgrade → registered re-derivation). jack-ryan canonicalizes the version string; gamora stamps certs with it.
- **GOAP CUT entirely** (not reserved for bosses). **Utility-scorer-over-kit-axes APPROVED** for when the Godot combat layer scopes (future spec-work, un-parks then; scripted rotation adequate now). Pack-spacing = balance parameter.
- **F4-martial pilot-attribution-probe GATE:** no kit-side martial (AOE/cleave) response fires until a pilot-attribution probe rules artifact-vs-defect. Pre-registered, deferred post-re-pilot.

**Two parallel fires (2026-07-07):**
| Agent | Task | State |
|---|---|---|
| gamora | Step-3 redux: (A)+(C) channel fix + (B) 7-element wheel + lever sweeps (#24 F2-first protocol) + TTK-anomaly mechanism check + lived-channel stratified re-pilot + miss-taxonomy + caster-margin re-confirm + F4-martial measure-only + F-b closing read + docstring WARN fix + pilot_policy cert stamp. Dispatch `97dc802`. | ✅ DONE (`6468b57`, tag `gamora/v-batch2-step3-lived-channel-repilot-1`) — channel fixed; F2 locked; **F3 = 2nd #24 STOP (needs tier-independent boss_damage_scale)**; TTK DPS-bound (not artifact); **F-b PARITY HOLDS → retire**; **Gate-2 ✅ PASS-WITH-FOLLOWUPS (jack-ryan `9ecccff`)**; 4 Matt decision points validated |
| jack-ryan | decisions-log: (1) release Q11-Step3 instrument-fix decision; (2) ratify one-pilot-policy contract as 3rd law; (3) canonicalize `pilot_policy` version string + stamp bands; (4) record F4-martial pilot-attribution-probe gate + GOAP-cut + utility-scorer-approved. Pattern-A (no dispatch file) | ✅ DONE (`8607840`) — 4 entries in `design/decisions/decisions-log.md` (repo-root path); metrology note stamped |

**⚑ rocket INFO owed (via KR, from jack-ryan Gate-2):** a zero-emit season-gen run is EXPECTED right now (R4 gate tightened; F4 band unregistered until the lived-channel re-pilot lands) — NOT a regression, no rocket schema/code action. Flag to rocket before any season-gen run.

### gamora Step-3 REDUX RESULT (2026-07-07) — channel LIVE; F3 2nd #24 STOP; F-b PARITY HOLDS (`6468b57`)

**Tag `gamora/v-batch2-step3-lived-channel-repilot-1`; Gate-2 FILED `cf4c81e` → `qa/pending/2026-07-07-gamora-step3-lived-channel-repilot-gate2.md`. jack-ryan Gate-2 running. Push HELD (Matt-gated).**

- **Channel fix (A)+(C) DONE:** both builders (`_build_standard_mob_dicts` + `_build_smoke_four_family._mob`) source `skills` from `emit_skills_for_threat_tier`; mobs deal real typed damage. **F4 fodder (C) resolved by inspection** — reinforcements clone `mob_dicts[-1]` (`spatial_engine.py:3269`), same fix repairs it, no separate F4 code. **Disc-#11 finding:** `mob_damage_scale=0.0` is NOT off — coerced 0.0→1.0 (`or 1.0`, `spatial_resolver_adapter.py:120`); sweep uses strictly-positive scales, dead-dict = true-off.
- **Calibration:** lever (a) **`mob_damage_scale=0.03`** locked on F2 (wheel-avg WR 0.881 beat / 0.945 full-pop mean ∈ [0.85,0.95]); steep cliff (0.025→0.98 / 0.03→0.88 / 0.035→0.31). lever (b) boss HP moves TTK 9.7→18s across 6k→9.6M, reaches 15s floor only at ~9.6M HP.
- **TTK-anomaly mechanism finding:** all 4 pre-registered hypotheses discriminated — H2 timeout-censoring REJECTED, H3 heal-race REJECTED, H4 DPS-cap REJECTED; **H1-refined CONFIRMED: TTK dominated by a fixed ~11–13s engage/ramp floor; the martial kit's ~90k+ effective DPS is the binding term, not boss HP. The saturation is REAL (DPS-bound), NOT a dead-channel artifact — it persists.**
- **⚑ F3 = 2nd #24 STOP-AND-FLAG (no third knob added, correct discipline):** F3 WR stuck at 1.0 across boss HP 150k→9.6M. Root: `mob_damage_scale` is **MONOLITHIC** (multiplies boss dm 5.0 AND swarm dm 0.85 together); the F2-lock 0.03 defangs the F3 boss (5.0→0.15) → never threatens the kit → WR 1.0. **Landing F3 WR ∈ [0.60,0.80] needs a THIRD knob = tier-independent `boss_damage_scale`.** Per dispatch: STOP, flag. **→ Matt ruling needed.**
- **Miss-taxonomy** (martial; under-floor / over-ceiling-flag / WR-side): F1 15/15/0 · F2 0/20/32 · F3 40/40 (STOP) · F4 35/10/0.
- **Caster-margin re-confirm** (verdicts stand per §7; real numbers): F1 both casters WR 1.0 (+0.05 above 0.95 floor); F4 both exit 1.0 (+0.20 above 0.80). **Caveat:** measured at the F2-locked scale 0.03 — at native scale 1.0 the same caster dies 5/5 on F4, so a per-family higher mob-damage could still lower caster margins.
- **F4-martial KPM (measure-only):** median **23.7** < 60 floor (reproduces §7's 23.9). Kit response gated on pilot-attribution probe (Matt) — not fired.
- **⭐ F-b CLOSING READ: PARITY HOLDS** on F1/F2/F4 (F3 excluded as STOP). No systematic caster-vs-martial WR asymmetry beyond the 2-cell sample → **F-b confirm-unneeded criterion MET; F-b retires to git (Matt rules).** The caster-HALT investigation resolves: casters NOT underpowered; the shortfall was instrument artifacts (dead wall + saturation cap + dead mob-damage channel).
- **7-element wheel verified kit-invariant** (element@w=`ROTATING_ELEMENTS[w]` every kit; cert=wheel-avg; worst-element=diagnostic flag). Report stamped **`pilot_policy=scripted-rotation-v1`**. Docstring WARN fixed. `test_cycle13_wave5_gauntlet_sim` 50/50; smokes PASS. No bar/band moved; kit-side chassis FROZEN; no MIGRATION (sim-internal sidecar JSON).
- **Calibration-precision note (§12.3):** beat-locked 0.03 gives full 40-kit pop F2 mean WR 0.945 (band-ceiling edge, median saturated 1.0); recommends re-lock on full pop (~0.032–0.035) for the milestone — a precision refinement, NOT a bar/kit change; candidate to fold into the F3 third-knob re-run.
- **Work-products:** math note `simulation/math/step3-lived-channel-calibration-repilot-2026-07-07.md` · driver `simulation/gauntlet_lived_channel_repilot_driver.py` · report `simulation/output/gauntlet_lived_channel_repilot/lived_channel_repilot_report.json`.

**→ jack-ryan Gate-2 ✅ PASS-WITH-FOLLOWUPS (`9ecccff`; pending cleared; push held).** Certified against source + independent re-runs (sweep beat 45.7s reproduced exactly; `test_cycle13_wave5_gauntlet_sim` 50/50). Channel fix verified at source (`emit_skills_for_threat_tier` @ `:203`,`:54-59`); F4-by-inheritance SOUND (reinforcements clone a fixed-builder dict); **coercion finding real + load-bearing** (`spatial_resolver_adapter.py:118` `or 1.0` maps dm 0.0→1.0 → scale-0.0 aliases native, sweep correctly uses strictly-positive). **One INFO defect:** `_miss_taxonomy` mislabels F2 over-band saturation as `wr_under_band` (disp dict lacks `wr` key for kpm_band families) — cosmetic, zero cert/verdict/parity impact, folds into re-run.
**jack-ryan's three Matt-facing determinations:**
- **(4) F3 STOP correct; tier-independent `boss_damage_scale` is the CLEAN MINIMAL resolution — no two-knob path exists** (rank-deficiency: one scalar can't serve both a low-competency F2 swarm chip AND a threatening F3 boss; boss dm 5.0×0.03=0.15 verified). Stays inside fit-direction (room knob, not bar/kit). **Recommend AUTHORIZE.**
- **(5) F-b retirement LEGITIMATE + ROBUST.** F3 exclusion doesn't undercut parity (F3 could only re-confirm delta-0, never refute); the caster-margin caveat is class-agnostic (a lethality knob lowers BOTH classes) → bounds absolute survivability, not parity. **Recommend RETIRE.**
- **(3) TTK-DPS-bound SOUND** — 4 hypotheses pre-registered pre-tuning w/ real discriminating measurements; saturation persists on lived channel = genuine DPS-vs-HP mismatch, not artifact.
- **Sequencing:** fold the §12.3 full-pop F2 re-lock (~0.032–0.035) INTO the F3 third-knob re-run under one seed stream. Finding `qa/findings/2026-07-07-gamora-step3-lived-channel-repilot-gate2.md`.

**⚑ MATT DECISION POINTS (all now Gate-2-validated):** (1) **F3 third knob** — authorize tier-independent `boss_damage_scale` [jack-ryan: clean minimal, recommend authorize]. (2) **TTK reality** — F3 boss TTK DPS-bound (~11–13s floor + ~90k kit DPS), 15s band only at ~9.6M HP [Matt reads sizing implication; possible kit-chassis signal]. (3) **F-b retirement** — parity holds [jack-ryan: legitimate+robust, recommend retire]. (4) **Calibration precision** — re-lock F2 on full pop ~0.032–0.035, folded into the F3 re-run.

**jack-ryan decisions-log canon DONE (`8607840`) — 4 entries (all 2026-07-07, in `design/decisions/decisions-log.md` at repo root):**
1. Q11-Step3 instrument-fix ruling (A mob-dict unification + sweep, C F4 dead-effect probe, B wheel-average cert, lever-b pre-registered mechanism check; §7-survival recorded; Gate-2 HOLD released).
2. Third governing law: the one-pilot-policy contract (+ planned-re-derivation corollary; GOAP CUT, utility-scorer APPROVED, pack-spacing=balance-param — ratified-but-not-now).
3. Canonical `pilot_policy` version stamp — **string = `pilot_policy=scripted-rotation-v1`** (fully-qualified: player=`_select_player_skill_v2` `spatial_engine.py:1335` + monster=`skill_rotation_priority` `spatial_engine.py:1190`, deterministic+seeded). **Bands stamped now** in the metrology note (header + §7). **gamora stamps certs with the short string `pilot_policy=scripted-rotation-v1`** (consumes it via the metrology note, her required reading — no dependency stall).
4. F4-martial pilot-attribution-probe gate (pre-registered, deferred post-re-pilot).

**Work-products:** math note `simulation/math/step3-mob-lethality-calibration-2026-07-07.md` · probe + `step3_probe.json` · R4 flip `gauntlet_sim.py:854` · MIGRATION v1.85 · Gate-2 submission `qa/pending/2026-07-07-gamora-step3-mob-lethality-calibration-r4-flip-gate2.md`.

### ⚑ Matt 4-decision ruling (2026-07-07) — F3 boss-scale completion + F-b retire + chassis-evidence FIRED

**Ruling (VERBATIM):** "Authorize (1) — boss_damage_scale, boss/mini-boss tier only. Retire (2) — F-b to git with the parity statement; jack-ryan logs the arc. On (3): register as chassis-evidence #1 for the loot-campaign rebalance alongside the F2-cliff defense finding; boss HP set at genre-sane ratio; the TTK overpowered flag stands population-wide; nothing unfreezes. Accept (4) with the fold, and confirm F2 WR-over-band disposes as flag-pass per Rider 3, not fail."

| # | Decision | Lane | Fire |
|---|---|---|---|
| (1) | Authorize tier-independent `boss_damage_scale` — **boss + mini-boss tier ONLY** (decoupled from swarm `mob_damage_scale`); tune F3 WR ∈ [0.60,0.80]. | gamora | ✅ dispatched (`b38de08`, tag-target `gamora/v-batch2-step3-f3-boss-scale-1`) |
| (2) | **Retire F-b** (caster-damage-premium fork) to git with the parity statement; log the full caster-HALT arc (resolved as instrument artifact — dead wall + saturation cap + dead mob-damage channel; casters never underpowered). | jack-ryan (decisions-log) | ✅ dispatched |
| (3) | Register **TTK-DPS-bound = chassis-evidence #1** for the FUTURE loot-campaign rebalance, alongside the F2-cliff defense finding; boss HP at **genre-sane ratio** (NOT swept to force TTK); TTK-under-15s = **standing population-wide overpowered flag**; **nothing kit-side unfreezes** (2.3384× fossil stays frozen). | jack-ryan (decisions-log) + gamora (HP sizing) | ✅ dispatched |
| (4) | **Accept F2 full-pop re-lock** (~0.032–0.035) **folded into the F3 re-run under one seed stream**; **F2 WR-over-band = flag-pass per Rider 3, NOT fail** (confirmed). | gamora | ✅ dispatched |

**Fires (2026-07-07, both background):**
- **gamora** → dispatch `2026-07-07-gamora-step3-f3-boss-scale-completion.md` (`b38de08`): decisions (1)+(4) — tier-scoped `boss_damage_scale`, F2 full-pop re-lock, genre-sane boss HP, full four-family re-pilot, Rider-3 dispositions, cosmetic `_miss_taxonomy` label fix. Math-note-before-tuning + no-leakage proof + #24 orthogonality guard built in. Tag `gamora/v-batch2-step3-f3-boss-scale-1` → Gate-2. **⚠ FIRST run KILLED by infra API-overload mid-execution (NOT a logic failure); resumed by a 2nd gamora session.** Prior session had already: committed the math-before-code note (`59dc832` — complete plan of record: genre-sane HP=9000=60× trash in ARPG 40–100× band, #24 sweep order, no-leakage proof, Rider-3 schema) + implemented the tier-scoped knob in `gauntlet_four_family_metrology_driver.py` (`_mob_skills_for_tier`, boss/mini-boss gated, strictly-positive guard — UNCOMMITTED). Not-yet-done at kill: the F2 re-lock run, the `boss_damage_scale` sweep, the full re-pilot, dispositions, caster margins, cosmetic fix, tag, Gate-2. **Resume session picks up from execution.**

### gamora Step-3 F3 BOSS-SCALE COMPLETION RESULT (2026-07-07) — 2nd #24 STOP CLOSED (`61a7faf`, tag `gamora/v-batch2-step3-f3-boss-scale-1`)

**Tag `gamora/v-batch2-step3-f3-boss-scale-1` (HEAD `61a7faf`); Gate-2 FILED `qa/pending/2026-07-07-gamora-step3-f3-boss-scale-gate2.md`. jack-ryan Gate-2 running. Push HELD (Matt-gated).**

- **F2 re-lock:** `mob_damage_scale = 0.03` IN-BAND on full 40-kit pop (wheel-avg WR **0.9446** ∈ [0.85,0.95], band-ceiling edge). Beat lock held on full pop; cliff 0.025→0.998 / 0.03→0.945 / 0.035→0.707<floor → 0.03 is the sole near-midpoint in-band member.
- **`boss_damage_scale = 48.0`** (tier-scoped boss/mini-boss ONLY) → **F3 pop WR 0.7018** ∈ [0.60,0.80]. Boss dm = 5.0·0.03·48.0 = 7.2. Monotone single-param grip (bds 40→0.818 / 46→0.761 / 48→0.702 / 50→0.639).
- **⭐ No-leakage witness MEASURED (the #24 orthogonality crux):** F2 pop WR **0.9446 IDENTICAL at `bds=1.0` and `bds=5.0`** — the boss knob is a proven no-op on the F2/swarm/trash/champion lock (F2 has no boss tier). Measured, not asserted.
- **Genre-sane boss HP = 9000 = 60× trash** (ARPG 40–100× band; NOT swept). **F3 TTK = 5.036s → STANDING population-wide overpowered flag** (38 kits; kit-DPS-bound = chassis-evidence #1; recorded, NOT auto-fail, NOT HP-inflated). Nothing kit-side unfroze.
- **Rider-3 dispositions (full four-family re-pilot, ONE seed stream):** F3 **certifies 28/40** (WR med 0.8214 — was the STOP; 12 genuine under-floor FAILs). F2 **36/40** (8 PASS + 28 FLAG_PASS_OVERPOWERED [over-band WR>0.95 = flag-pass per Matt (4), NOT fail] + 4 FAIL). F1 25 cert; F4 5 cert + 35 FAIL (KPM floor — kit-side, deferred, measure-only).
- **Caster margins:** F1 +0.05 · **F3 +0.40** (real numbers now — boss threatens) · F4 +0.20; all pass.
- **Cosmetic INFO fix landed:** over-band F2 labels `wr_over_band` (was `wr_under_band`), `disp["wr"]` written, disposition FLAG_PASS_OVERPOWERED.
- **Disc #12 semantic shifts framed** (for jack-ryan decisions-log assessment): (a) mob-damage calibration decoupled (tier-independent boss knob); (b) over-ceiling now FLAG_PASS_OVERPOWERED not auto-fail (`passes_bar` unchanged; `n_certified` = new Rider-3 count).
- **Regression** `test_cycle13_wave5_gauntlet_sim` 50/50. **NO MIGRATION.md** (sim-internal room constants + sidecar JSON, no persisted-field boundary).
- **Work-products:** knob + Rider-3 disposition + `wr` fix in `gauntlet_four_family_metrology_driver.py`; re-pilot driver `gauntlet_lived_channel_repilot_driver.py`; sweep script `gamora_step3_lived_calibration_sweep_2026_07_07.py`; sweep result `output/step3_calibration/step3_lived_sweep.json`; re-pilot report `output/gauntlet_lived_channel_repilot/lived_channel_repilot_report.json`; math note `simulation/math/step3-f3-boss-damage-scale-2026-07-07.md`.

**→ jack-ryan Gate-2 ✅ PASS-WITH-FOLLOWUPS (`7401953` finding+archive; engine `a908ced` decisions-log; NOT pushed). No BLOCK; pending cleared to `qa/archive/`.** Verified the whole tag as one unit (both authorship sessions). **No-leakage witness REAL + MEASURED** — sidecar `no_leakage_witness` carries both 40-kit per-kit WR vectors at bds∈{1.0,5.0}, byte-identical (0.9446==0.9446); jack-ryan independently re-ran: swarm/magic/elite dm identical across bds∈{1.0,5.0,48.0}, elite explicitly excluded from the boss knob, bds=1.0 a strict byte-reproducing no-op → **two knobs cleanly decoupled, rank-deficiency genuinely resolved.** **All hard-guards HOLD:** chassis constants byte-frozen (only in AGENT_STATE prose, never in any code diff); bars/bands only READ never reassigned; boss HP 9000 constant across every sweep row (not swept for TTK); boss knob scoped {boss,mini-boss} only; `pilot_policy` stamped; strictly-positive guard raises on ≤0.0; regression 50/50 reproduced; NO MIGRATION verified structurally (no telemetry/export/schema in diff; `schema_version` is the sidecar's internal field). **Decisions-log (jack-ryan lane):** SHIFT 2 (FLAG_PASS_OVERPOWERED) already logged; **SHIFT 1 (third-knob AUTHORIZATION / calibration decoupling) was forward-referenced by 3 entries but the entry itself was missing — jack-ryan authored it (`a908ced`) rather than BLOCK** (code/math/orthogonality all sound). **Two INFO follow-ups (non-blocking, gamora next-touch):** (1) `_caster_margins` F3 row reports floor-pass but caster F3 WR=1.0 is itself over-ceiling (a flag-pass) — future report iteration could surface the caster over-band flag for symmetry; (2) bds sweep shoulder past ~55 goes one-shot/non-monotone — locked 48.0 sits well inside the clean monotone region, grid-shoulder note only. **Matt action: none required** (within jack-ryan ADR-002 authority — within-seam sim, no cross-seam schema, no milestone-tag drop). **Milestone tagging of the four-family certification remains Matt's call.**

### ⭐ CASTER-DIAGNOSTIC ARC — CLOSED (2026-07-07)

The caster HALT is fully resolved as an INSTRUMENT ARTIFACT (dead 300k/500k HP wall + 8-mob saturation cap + dead mob-damage channel). Casters were never underpowered — final proof: with a threatening F3 boss, caster F3 margin is **+0.40**. The four-family gauntlet instrument is now fully calibrated + Gate-2-passed across all four families (F1 dense_cell, F2 open_arena, F3 boss_with_adds, F4 escape_lane), with Rider-3 dispositions and the one-pilot-policy stamp. **F-b retired; #24 STOP ×2 both closed via disciplined tier-independent knob (never a hacky third-knob-in-place).**

**Still open / gated (post-arc):** — ALL RESOLVED by Matt's arc-close authorization batch below.

## ⭐⭐ MATT ARC-CLOSE AUTHORIZATION BATCH (2026-07-07) — two-front demo assembly FIRED

Matt's transmission IS the ruling for items 1–6; item 7 pre-folded by gandalf (meta-repo `e64a59d`, `93f231c`).

**RULINGS:**
1. **ARC NUMBERS RATIFIED** — F2 mds full-pop re-lock, boss_damage_scale=48.0, boss HP 9000 (genre-sane, never TTK-inflated), Rider-3 semantics (over-ceiling=FLAG_PASS_OVERPOWERED→certify+review; floor=hard fail). **→ LEG C UN-HELD; batch-2 population completion proceeds.**
2. **MILESTONE TAG AUTHORIZED** — four-family certification is a true milestone; gamora drops the Matt-approved milestone tag (v<X.Y>-<feature>).
3. **Q8 CAMERA B APPROVED** (G3 sign-off): **FOV 40 / pitch −55° / yaw 47° fixed / dist 34m.** Every floor inherits it.
4. **RANGED-PROXY NAV:** EXCLUDE ranged summoners from v2 demo curation — melee summoners certify clean + satisfy the necromancer mandate. Nav fix → LAUNCH-track (PART E stays open there).
5. **PUSHES AUTHORIZED:** engine 79796e2→a908ced (incl. decisions-log), godot ba5547d, production DB v2.20 APPLY (satisfies ADR-006). **[KR DONE: engine pushed `6468b57..a908ced` + intermediate tag; godot ba5547d confirmed already at remote. DB v2.20 apply → star-lord lane.]**
6. **Q7 NOT RULED YET** — drax fires the BoneMap vs GeneralSkeleton two-option brief as FIRST BEAT; Matt rules same-session on return; drax executes immediately after. Not queued behind anything.
7. **Q9 + Q10 SWEPT** (pre-folded; decisions-log only): Q9 all five as recommended; Q10 = transform cap 2 at v1 (3 gated on §7a audit live) / band-widths = band-sheet at campaign time / ω-penalty RETIRED-by-construction (Track-D tripwire) / defensive vocab per spec §2. Sole loot remainder = resist-cap VALUES riding the band-sheet. Loot build fully unblocked behind Leg C close.

**LANES FIRED (2026-07-07, all background; KR sequences within seam):**
| Lane | Fire | Status |
|---|---|---|
| **drax** | Beat 1 Q7 brief (BoneMap vs GeneralSkeleton) → Matt ruling → [gated: D6 three-beat floors under Camera B + D5 verb VFX + D8 grimoire UI] | 🔵 Q7 brief running; demo body HELD behind Q7 ruling |
| **rocket** | gen-path legs 2–3 (summoner emission) · B1-REBASE Phase 1 vs `proxy-t4-suite-spec-2026-07-02.md` **v3 ONLY** | ✅ **Item 2 DONE — gamora UNBLOCKED.** B1-REBASE Ph1 CONFIRMED v3-conformant at HEAD (already LANDED `40e351e`, ancestor; 169 tests green — Disc #11+#3, NOT rebuilt). **Anchor tag `rocket/v-proxy-t4-rebase-phase1-v3-confirmed-1` @ `0e9fc91`** (gamora ext §7 rides it — cert sweeps can now fire). Two DoFs gamora routes to my seam PRE-REGISTERED for Gate-1 (DoF-A A3-energy: `charge_stack` invalid + INT-cell→mana closes SOVEREIGNTY→A3 fail; R-A1 `focus` re-designate recommend / R-A2 count-axis; **design call, not self-authored** · DoF-B F-f: consumer exists, live-wiring is B4-scoped, inert-guard now). Math note `generation/math/proxy-t4-b1-rebase-phase1-v3-refire-2026-07-07.md` (engine `a5adcf1`). ⚑ **Item 1 gen-path legs 2-3 = SCOPED + FLAGGED, NOT fired blind:** leg-1 LANDED+live (smoke GREEN); **leg 2 = route summoner kits through `select_proxy_t4` so `primary_t4` carries a proxy-family member** (`select_primary_t4:1831` today = hard-coded ALWAYS-DDA = the v1 bug spec v3 §1 names); **leg 3 = emission run**. Leg 2 is CROSS-SEAM cert path (star-lord DDA-lock validator widen owed per sim `MIGRATION:8371`) → needs math-note+Gate-1+**a co-dispatch (rocket emit-route ∥ star-lord validator-widen)**. **KR: leg-2/3 scoping dispatch owed before leg 3 can unblock star-lord Leg C.** |
| **gamora** | milestone tag drop (item 2) · proxy-T4 sim-eval extension + magnitudes (rides B1-REBASE) | ✅ tag DONE: **`v2.2-batch2-four-family-certification`** (annotated, on `a908ced`, seam-prefix dropped per milestone convention; local-only, NOT pushed — Matt-gated). proxy-T4 extension math-note LANDED (`eb7c9b1`); **cert sweeps ⛔ GATE-BLOCKED on rocket B1-REBASE Ph1** (pre-registered so completion is deterministic on the tag: A2 magnitude sweeps + A3 energy re-confirm + F-f test-promotion + extension tag `gamora/v-proxy-t4-rebase-eval-extension-1`→Gate-2). |
| **star-lord** | II.3 hand-join scaffold (MVP-CRIT, now) · gear-pool writer (live season) · **DB v2.20 APPLY** (item 5) · Leg C re-fire w/ rocket [GATED on rocket leg 3] | ✅ **Items 1+2+3 DONE** (engine `e57b796`, tag `star-lord/v-batch2-arc-close-scaffold-1`). DB v2.20 APPLIED (v2.15→v2.20; 7,841 rows intact; ADR-006 satisfied). II.3 scaffold bundle emitted (`one_realm_batch1_scaffold_bundle.json`; 14 kits / 40 monsters / 200 gear; round-trip smoke PASS). Gear-pool writer advanced to season_001005 (200 items w/ off_hand; resist-cap deferred to band-sheet). Gate-2 filed `qa/pending/2026-07-07-star-lord-arc-close-scaffold-gate2.md`. **Leg C held — gated on rocket leg-2/3 dispatch (KR owed)** |
| **jack-ryan** | decisions-log: arc ratification (item 1) + Q9/Q10 sweep (item 7) · Gate-2 per return | ✅ decisions-log DONE (`0e9fc91`, NOT pushed — beyond a908ced, gated). 2 entries: arc-ratification (4 canonical numbers + Leg C un-held + arc-closed-as-artifact + chassis-evidence #1/#2) & Q9/Q10 sweep (Q9 source LOCATED `agnostic-loot-engine-spec.md` §2, no gap; Q10 cap-2-at-v1 / band-widths=band-sheet / ω-penalty retired / resist-cap VALUES sole remainder). Gate-2s fire per-return. |
| **galadriel** | G2 register-CV as D6 floors land | ⏸ HELD — gates on drax D6 floors landing (not yet fired) |

**GUARDS (standing, Matt-restated):** kit-side chassis constants FROZEN (2.3384× fossil); bars/bands FIXED (fit-direction); chassis-evidence #1/#2 accumulate for loot-campaign rebalance — nothing unfreezes this run. Kits vote BARE (provenance law); pilot_policy stamps on new bands. **LAUNCH-track, deliberately NOT this run:** counter-breadth scoping consult, F4-martial pilot-attribution probe, ranged-nav fix. Auto-commit per meta-repo addendum; pushes beyond the item-5 set remain Matt-gated.

**KR sequencing watch-points:** (a) **rocket leg 3 BLOCKED on a leg-2/3 SCOPING DISPATCH** — rocket scoped legs 2-3 (leg 2 = `select_proxy_t4`→`primary_t4` routing, cross-seam; leg 3 = emission run) but did NOT fire the multi-hour cross-seam build off a one-line authorization (no dispatch, Gate-1 owed, star-lord DDA-lock validator-widen must co-dispatch per sim `MIGRATION:8371`). **KR owes: author the leg-2/3 dispatch (rocket emit-route ∥ star-lord validator-widen) → Gate-1 → leg 2 → leg 3 → unblocks star-lord Leg C re-fire + gamora summoner proxy-T4;** (b) ✅ **DONE — rocket B1-REBASE Ph1 LANDED** (`rocket/v-proxy-t4-rebase-phase1-v3-confirmed-1` @ `0e9fc91`) → gamora proxy-T4 sim-eval cert sweeps UNBLOCKED (her ext §7 4 items key on this tag; extension tag → Gate-2); the two DoFs gamora routed back (A3-energy R-A1/R-A2, F-f) are pre-registered for Gate-1 in rocket's math note `a5adcf1`; (c) drax D6 floors land → fire galadriel G2 register-CV; (d) **drax Q7 brief RETURNED (`5cd36f6`, recommends Option A authored per-variant BoneMaps) → surfaced to Matt, AWAITING RULING → re-fire drax demo body on ruling**; (e) Gate-2 per tagged return.

**Delta-propagation flag (routing to jack-ryan, collab-side canonical owner — non-gating):** the `v2.2-batch2-four-family-certification` milestone closes the four-family gauntlet certification gap in `canonical/current-to-end-state/current-to-end-state-engine.md` (the balance/sim cert question). gamora surfaced it; KR does not own that doc → route to jack-ryan on a future fire or fold into handoff.
- **jack-ryan** → decisions-log for (2)+(3): retire F-b with parity statement + log the arc; register chassis-evidence #1 (TTK-DPS-bound) alongside the F2-cliff defense finding; record genre-sane-HP + population-wide-TTK-flag + nothing-unfreezes; confirm F2-WR-over-band = flag-pass per Rider 3. **✅ DONE (`1ca3d79`, not pushed) — 3 entries:** (1) F-b RETIRED, caster-HALT arc closed (~10× shortfall = artifact of 3 dead channels: 300k/500k wall + 8-mob saturation cap + dead mob-damage channel; casters never underpowered; freeze discipline prevented 3 phantom buffs; carried bound: re-read caster margins if a future per-family lethality knob lands). (2) Chassis-evidence #1 REGISTERED (F3 TTK real DPS-vs-HP mismatch, H1-refined confirmed) alongside chassis-evidence #2 (F2-cliff, ±17% flips pop); boss HP genre-sane (gamora sets value); TTK flag population-wide; fossil FROZEN; loot economy is the eventual lever. (3) Rider-3 flag-pass confirmation (F2 WR-over-band certifies; floor exclusionary / ceiling diagnostic); notes the cosmetic `_miss_taxonomy` mislabel (gamora's within-seam fix). Decision (1) `boss_damage_scale` left to its own ruling (not logged here — room-side knob).

**Rider-3 confirmation (Matt-requested):** F2 mean WR at/over the band ceiling after best-effort full-pop re-lock disposes as an **OVERPOWERED FLAG → balance review (flag-pass), NOT a certification fail.** Encoded in the gamora dispatch; recorded by jack-ryan in the decisions-log.

**Still frozen / gated:** kit-side chassis constants FROZEN (chassis-evidence accumulates for the future loot-campaign rebalance, not a now-fix); production DB apply of v2.20 (`telemetry.db`) still Matt-gated (ADR-006 — "push" ≠ "apply"); Leg C HELD until Step-3 completes + Matt rules; F4-martial kit response gated on the pilot-attribution probe.

### star-lord F4-telemetry consume RESULT (2026-07-07) — DONE; Gate-2 FILED

- **Schema delta v2.20:** two nullable `ALTER TABLE` columns on `spatial_fight_results` — `escape_reached` (INT NULL: NULL=pre-v2.20 / 0=no-escape / 1=escape-win) + `continuous_spawned_total` (INT NULL: NULL=pre / 0=non-F4 / N=reinforcements). No DDL change to `mobs_killed`.
- **Scoped invariant:** `mobs_killed ≤ total_mob_count` is a semantic contract (not `validate()`-enforced); relaxation scopes to F4 ONLY via discriminant `continuous_spawned_total > 0` (or `scenario_id == 'escape_lane'`). Six existing rooms emit `escape_reached=0` + `continuous_spawned_total=0` byte-identically; tight invariant preserved + asserted (`test_non_f4_room_tight_invariant_preserved`).
- **Round-trip smoke (Principle 6) GREEN — both cases:** CASE 1 (F4 escape) `mobs_killed=35 > total=8`, `escape_reached=1`, `spawned=27` persists+reads intact; CASE 2 (non-F4) `mobs_killed=8 ≤ 8`, tight invariant holds.
- **Regression:** 78 round_trip_spatial_telemetry (70 pre + 8 new `TestF4EscapeLaneTelemetrySchema220`) + 174 additional round-trip/spatial PASS; zero regressions.
- **MIGRATION lockstep:** telemetry `MIGRATION.md` v2.20 + export `MIGRATION.md` v2.20-telemetry entries; AGENT_STATE updated.
- **⚑ Production DB apply (`telemetry.db`) PENDING Matt explicit authorization (ADR-006) — NO DB write executed.** Schema/migration code shipped; the on-disk apply is a separate Matt-gated external-systems action.
- **→ Gate-2 ✅ PASS (jack-ryan, `984981b`; no BLOCK; pending cleared).** Finding `qa/findings/2026-07-07-star-lord-f4-telemetry-consume-gate2.md`. Verified vs SOURCE + re-ran suite: nullable ADD-COLUMN **no-DEFAULT** = correct pre-v2.20→NULL backfill (`test_pre_v220_rows_have_null_f4_fields`); positional-INSERT 24-col/24-`?`/value-tuple alignment correct (the real hazard, checked); invariant relaxation is a discriminant-gated semantic contract (NOT a blanket removal — six rooms keep + assert the tight bound); round-trip CASE 1/2 are real assertions; **78 tests pass re-run, zero regressions**; MIGRATION lockstep both sides (export declares NONE drax impact); scope held byte-for-byte (producer untouched); ADR-006 apply correctly gated. **Two INFO notes (non-blocking):** (1) if F4 metrology ever enters the exported season bundle, drax becomes a consumer → fresh export/MIGRATION entry owed (not now); (2) `getattr(...,default)` reads redundant-but-defensive, fine as-is.

**Guard now (freeze re-scoped kit-side):** kit-side constants FROZEN; room-side UNFROZEN for calibration; bars/bands fixed (fit-direction); Leg C HELD until re-pilot returns + Matt rules its numbers; F-b held confirm-unneeded; F4-martial deferred kit-side.

### Lane 1 RESULT (gamora, 2026-07-07) — BUILD DONE; Gate-2 PASS

- **Instrument built at spec §3 dims/populations.** F1 `dense_cell` NEW 16×22m/~24 (20 trash + champion pack of 4); `chokepoint_corridor` re-pop 8→24 (funnel kept); `magic_pack` re-roled champion-pack variant. **F2 `open_arena` re-dimensioned 50×50→36×36 + re-pop 8→40** (28 trash + 3 rare packs — the saturation repair). F3 `boss_with_adds` +2 timed add-waves (R5; injection verified 3→7 mobs at runtime). F4 `escape_lane` NEW 60×16m, continuous spawner (k=3/1s/cap50, seeded-deterministic), champion-elevation ×2.0, `escape_reached` win — population grows 12→50, the 8-mob no-respawn ceiling LIFTED by construction.
- **R4:** STR boss-shell carve-out RETIRED via new `family_certification_pass` (four-family gate). `gauntlet_pass` keeps the legacy floor until Lane-3 bars — the one-line flip is Lane 3's (confirm staging at Gate-2).
- **§4:** wall demoted to diagnostic `open_arena_wall_diag` (not deleted); six existing rooms survive.
- **Cross-seam (MIGRATION v1.84 → star-lord):** F4 fight-result fields `escape_reached` + `continuous_spawned_total` (claimed additive/brownfield-safe) + `mobs_killed` range semantic-shift. **Gate-2 verifies whether star-lord must consume before safe.**
- **Guardrails:** §3 dims read verbatim (no invented dims, no infeasibility→no spec-amendment flag); NO bar derivation; NO constant changes (byte-unchanged verified); build-smoke = "does-the-room-work" not certification. `mobs_killed=0` in smoke = fixture-DPS artifact (reproduces on known-good rooms) → Lane-3 concern, not a room defect (Gate-2 to assess). Compute (Disc #1.1): peak ~51 live entities on 8GB host, no bounds risk. Regression: 254 tests / 8 spatial suites pass, 2 updated.
- **Discipline #12 semantic-shifts** (R4 contract / open_arena re-base / mobs_killed range) routed to jack-ryan decisions-log.
- **→ Gate-2 ✅ PASS-WITH-FOLLOWUPS (jack-ryan, `ab35694`; no BLOCK; pending archived).** Finding `qa/findings/2026-07-07-gamora-gauntlet-four-family-instrument-gate2.md`. Verified vs SOURCE: Disc #1 note-before-code substantive; 3 frozen constants zero delta; §3 dims verbatim (60×16 mapped to y-axis run-length, not invented); R4 sequencing correct (`gauntlet_pass()` legacy floor UNCHANGED, `family_certification_pass()` export-only — one-line flip cleanly deferred to Lane 3, does NOT break the paused Step-3 sequence); champion-elevation inert-by-default 1.0 post-multiply on existing `spatial_dm` seam (no threshold smuggling); `mobs_killed=0` a SOUND fixture-DPS artifact (reproduces on known-good F1/F2/F3), room mechanics proven via `aoe_hits>0` + escape resolution + spawner firing; re-ran regression 233 (7 suites) + 70 (round_trip_spatial_telemetry) = zero regressions.
  - **⭐ STAR-LORD CROSS-SEAM DETERMINATION: no action required before safe — a note suffices.** The two new `SpatialFightResult` fields are additive/defaulted, NOT `validate()`-enforced, NOT persisted by SQLite `_INSERT_SQL`, consumed by nothing today; `mobs_killed` range shift scoped to continuous-spawn only (six existing rooms hold `mobs_killed ≤ total_mob_count` byte-identically). star-lord obligations (widen schema; relax invariant) go live only when Lane-3/export needs F4 telemetry on-disk — future event in MIGRATION v1.84. **KR did NOT dispatch star-lord.**
  - **jack-ryan followups (non-blocking, DEFERRED to land with Lane-3):** 3 Disc-#12 decisions-log entries (R4 cert-contract shift; open_arena re-base; mobs_killed range) + the R4 one-line ship-gate flip + star-lord MIGRATION work — all future-Lane-3 events so the log reflects the certifiable end-state.
- **→ Gate-2 PASS ⇒ gandalf F2 ±20% dim-amendment ruling FIRED (`gandalf/open-threads/2026-07-07-F2-camera-verify-dim-amendment-flag.md`).** LANE 1 FULLY CLOSED. **Lane 3 gated on this ruling:** record-only ⇒ fire Lane 3 directly; widen F2 ⇒ small gamora re-point of `arena.py` F2 dims first (bar is travel-sensitive), then Lane 3.

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

---

## ⭐ KR PROGRESS-DELTA (2026-07-07, post-arc-close-batch execution)

**Two background agents returned; two new fires; two items now on Matt.**

1. **star-lord Gate-2 → PASS-WITH-FOLLOWUPS** (jack-ryan, finding `qa/findings/2026-07-07-star-lord-arc-close-scaffold-gate2.md`, `3534749`; pending archived). Tag `star-lord/v-batch2-arc-close-scaffold-1` (`e57b796`) CLEARS. **Production DB integrity CONFIRMED independently:** `integrity_check=ok`, 22 tables, `fight_events` 2.3M rows untouched, **7,841** `spatial_fight_results` rows, **both new cols 100% NULL-backfilled (0 invented values)**, schema→2.20, applied shape matches Gate-2-passed v2.20 code (no drift). Items 2+3 verified (round-trip smoke reproduced; 171 tests; 50 off_hand; 0/200 resist-cap invented). Hard-guards all HELD.
   - ⚑ **FOLLOWUP → MATT (WARN, non-blocking, does NOT gate the tag):** the DB apply migration committed a **450MB `telemetry.db` binary blob into engine git history** (2.1MB→450MB, permanent; SQLite compresses poorly). Matt's call per ADR-002: **gitignore telemetry.db + keep a small seed fixture (jack-ryan's recommendation)** / accept the blob / history-rewrite (high-touch). Parked for Matt.
   - Record note: invocation cited v2.20 baseline `984981b`; actual v2.20 migration-code commit is `7d999db` (tag `star-lord/v-batch2-f4-telemetry-consume-1`). jack-ryan verified vs the correct one; reference cleaned.

2. **gandalf DoF-A → RESOLVED = `focus`** (R-A1). **Design-steward call, NOT a Matt escalation** (designates `energy_type` of ONE hand-authored demo fixture inside frozen guardrails; doc-48 population economy table UNTOUCHED; analogous to the ratified `shadow:soul` designer-overlay precedent). Load-bearing finding beyond rocket's framing: `focus` **passively decays + refills-by-acting** at the kernel (`combatant.py:418`) → correct death-economy on mechanical grounds, not just a non-mana gate-opener. R-A2 rejected (would drop the marquee SOVEREIGNTY capstone from the A3 pair). Determination: `gandalf/notes/2026-07-07-dof-a-summoner-energy-designation-determination.md`.
   - **gandalf §7 forward fork registered, deliberately NOT answered:** whether *emitted-population* summoner kits carry `focus` (a doc-48 G1 population-canon change) is Matt-gated + deferred, gated on B4 surfacing real summoner kits. This demo-fixture ruling does not prejudge it.

3. **leg-2/3 co-dispatch AUTHORED** (KR-owed obligation discharged): `dispatches/2026-07-07-rocket-starlord-leg-2-3-summoner-emission-route.md` — rocket route side (`select_primary_t4:1831` ALWAYS-DDA → route proxy-bearing kits through `select_proxy_t4` so `primary_t4` carries the highest-η ratified proxy member) ∥ star-lord DDA-lock validator-widen (per sim `MIGRATION:8371`); coordinated MIGRATION lockstep; math-note + Gate-1 BEFORE routing code; leg-3 emission run = the unblocking event for star-lord Leg C re-fire + gamora summoner proxy-T4. DoF-A/DoF-B explicitly out of leg-2 blocking scope.

4. **rocket FIRED** (bg `a389f472`): Deliverable 1 = land DoF-A `focus` field on `DemoSummonerSpec` (gandalf-ratified) + MIGRATION line, DISCRETE commit (unblocks gamora A3); Deliverable 2 = author leg-2 math note per co-dispatch → submit Gate-1 (NO routing code this session). jack-ryan now FREE for that Gate-1.

**KR sequencing (updated):**
- **gamora proxy-T4 A2+A3** — HELD for ONE clean pass, fires AFTER rocket's Deliverable-1 `focus` commit lands (A3 reads the landed field; A2 already unblocked by the Phase-1 tag). Avoids re-fire churn.
- **jack-ryan Gate-1** on rocket's leg-2 math note — fires when it lands in `qa/pending/` (jack-ryan free post-Gate-2).
- **leg-2 routing code + star-lord validator-widen** — fire AFTER Gate-1 passes (co-dispatch, MIGRATION lockstep) → leg-3 emission → unblocks star-lord Leg C + gamora summoner proxy-T4.

**ON MATT (2 items):** (i) **Q7** BoneMap-vs-GeneralSkeleton (drax recommends Option A; drax demo body D6/D5/D8 HELD behind this — his same-session ruling); (ii) **450MB telemetry.db blob** disposition (gitignore+seed recommended).

---

## ⭐ KR DELTA (2026-07-07, cont.) — rocket returned; gamora + jack-ryan-Gate-1 returned

**rocket (`a389f472`) DONE — both deliverables:**
1. **DoF-A `focus` field LANDED** `1af6889` (tag `rocket/v-batch2-dof-a-focus-field-1`): additive `energy_type="focus"` on all 3 `DemoSummonerSpec` necromancer fixtures + exported read accessors `demo_summoner_energy_type(kit_id)` / `all_demo_summoner_energy_types()` (gamora reads → retires `_A3_ENERGY="charge_stack"`). doc-48 pop table UNTOUCHED; MIGRATION line written; 262 tests PASS. **= gamora A3 unblocking event.**
2. **leg-2 math note** `cbac6ed` (`generation/math/leg2-summoner-primary-t4-routing-math-2026-07-07.md`) + Gate-1 request filed. NO routing code (Gate-1-gated).

**jack-ryan Gate-1 on leg-2 note → PASS-WITH-CONDITIONS** (finding `a5ebd17`; pending archived). All 5 dims clear vs SOURCE (predicate-P empty-decl no-op is an EXISTING passing test `w0_prereqs_smoke:207`; FROZEN 5-member value-set structural; band framing faithful to spec §4.5). **⚑ Verdict UPGRADED leg-2 to a THREE-SEAM lockstep — 4 conditions folded into the co-dispatch:**
- **C1 (load-bearing):** gamora sites 2/3 (`gauntlet_sim.py:2267`, `unified_calibration_loop.py:3577`) re-derive `primary_t4` via old always-DDA `select_primary_t4` → summoner would EMIT proxy but SIMULATE DDA (divergence). gamora added as consume-side seam; MIGRATION must cross-ref her patch OR document a known-transient divergence window.
- **C2:** freeze `ACCEPTED_PROXY_PRIMARY_T4` = {ASCENSION, SOVEREIGNTY, FISSION, CONVERGENCE, DUAL_PROXY} as ONE shared MIGRATION constant all 3 seams build against.
- **C3:** $0 S2 byte-diff GREEN + CITED at Gate-2. **C4 (INFO):** S1 route-correctness unit case (bone→FISSION, crypt→SOVEREIGNTY under `focus`) cited at Gate-2.
- Confirmed: F-f stays structurally unreachable through the summoner route (ZONE_CONTROL isolated) — B4-scoped disposition correct; no decisions-log conflict.

Co-dispatch AMENDED (`2026-07-07-rocket-starlord-leg-2-3-...`): added gamora consume-side leg + Gate-1 conditions section + gamora scope block + tag `gamora/v-batch2-primary-t4-consume-widen-1`.

**KR sequencing (updated):**
- **gamora proxy-T4 A2+A3** (`aa5862005af8111bd`) — RUNNING; independent of leg-2. Fold its return first.
- **leg-2 implementation = THREE-seam coordinated build** (rocket route + star-lord validator-widen + gamora consume-side) with C1–C3 folded — fires AFTER gamora's proxy-T4 pass returns (avoids double-booking gamora on the sim seam). → leg-3 emission → unblocks star-lord Leg C + gamora summoner proxy-T4.
- **ON MATT unchanged:** Q7 (drax body held) + 450MB telemetry.db blob.

---

## ⭐ KR DELTA (2026-07-07, cont.) — gamora proxy-T4 DONE; leg-2 producer + gamora-ext Gate-2 fired

**gamora proxy-T4 sim-eval EXTENSION → DONE** (tag `gamora/v-proxy-t4-rebase-eval-extension-1` @ `8a29009`, 20/20 pins). Both §7 gates cleared in one pass:
- **A2** = HOLD, no band re-opened; all scaffold bands CERTIFIED-HOLD (N=24/cell; axis-directional; R1-by-construction; D3 byte-unchanged; peak 59.8MB).
- **A3** = UNCONDITIONAL PASS; retired eval-side `_A3_ENERGY="charge_stack"` in harness+tests, now reads landed `focus` via `demo_summoner_energy_type()` → SOVEREIGNTY gate opens → bone→FISSION / crypt→SOVEREIGNTY. Hidden eval-side coupling removed.
- **F-f** = HELD at eval-side invariant (probe False; live-wiring B4-scoped; NOT promoted — no inert guard on frozen surface, Disc #12).
- MIGRATION: consumer-read note (consumes rocket's `energy_type`; cross-ref rocket DoF-A line); NO producer/schema change → star-lord owes nothing. Gate-2 filed `qa/pending/2026-07-07-gamora-proxy-t4-rebase-eval-extension-gate2.md`.

**Fired (parallel):**
- **jack-ryan Gate-2** (`a5ada10355e1ae157`) on gamora's proxy-T4 extension.
- **rocket leg-2 PRODUCER half** (`ac088b7121feeea0c`): define shared C2 constant `ACCEPTED_PROXY_PRIMARY_T4` (T4-catalog home) + emit route (predicate P) + S1 route-correctness case (bone→FISSION/crypt→SOVEREIGNTY under `focus`) + S2 byte-diff + generation MIGRATION cross-ref'ing gamora sites 2/3 + star-lord validator. **NO leg-3 yet** (gates on consume/validate halves). Tag `rocket/v-batch2-leg2-summoner-emission-route-1` → Gate-2.

**KR sequencing (updated):**
- After rocket's C2 constant + emit route lands → fire **star-lord validator-widen** + **gamora consume-side (sites 2/3)** in parallel, both importing rocket's C2 constant.
- After those land → **rocket leg-3 emission run** → coordinated three-seam Gate-2 → unblocks **star-lord Leg C** + **gamora summoner proxy-T4**.
- **ON MATT unchanged:** Q7 (drax body held) + 450MB telemetry.db blob.

---

## ⭐ KR DELTA (2026-07-07, cont.) — gamora proxy-T4 extension Gate-2 → PASS (lane CLOSED)

**jack-ryan Gate-2 on `gamora/v-proxy-t4-rebase-eval-extension-1` @ `8a29009` → PASS** (finding `qa/findings/2026-07-07-gamora-proxy-t4-rebase-eval-extension-gate2.md`, `dce4ae4`; pending archived). Independently reproduced: 20/20 pins + full harness (EXIT=0, all A2/A3 numbers exact); diffstat touches ZERO gen/production code; own AST F-f probe = False (honest eval-side HOLD, no inert guard, Disc #12); D3 baseline byte-unchanged; `energy_type` consumer-side only (star-lord owes nothing; Principle 3/6/ADR-004 OK). Within ADR-002 tier — no Matt escalation. **⇒ proxy-T4 sim-eval lane CLOSED + certified.**
- **Two B4-scoped follow-ups re-surfaced to KR (NOT blockers, NOT gamora-owed):** (1) rocket owes `enforce_family_max_one` live-wiring before B4 wires the emission pipeline; (2) when it lands, the F-f probe flips True → F-f test promotes to live-consumer assertion (gamora §3 sub-case-1). Parked for the B4 dispatch.

**Still in flight:** rocket leg-2 PRODUCER (`ac088b7121feeea0c`). On landing → fire star-lord validator-widen ∥ gamora consume-side (sites 2/3) against rocket's C2 constant → rocket leg-3 → three-seam Gate-2 → unblocks star-lord Leg C + gamora summoner proxy-T4.

---

## ⭐ KR DELTA (2026-07-07, cont.) — leg-2 producer LANDED; consume/validate halves fired

**rocket leg-2 PRODUCER → DONE** (commit `996f77d`, tag `rocket/v-batch2-leg2-summoner-emission-route-1` = engine HEAD; Gate-2 filed `0f973b6`):
- **C2 shared constant** `ACCEPTED_PROXY_PRIMARY_T4: frozenset` @ `t4_catalog_v2.py:128-171` (derived from named PROXY constants, import-time guards: exactly-5 / subset-of-family / INVERSION excl / ZONE_CONTROL excl). star-lord + gamora IMPORT it.
- **Route** `route_primary_t4()` @ `mechanic_alteration.py:1962` — `select_proxy_t4` first (non-None ⇒ proxy member is `primary_t4`), else DDA fallback; self-cast stays `t4_candidates`. DDA displaced, not removed.
- **S1/S2 14/14 GREEN** (`generation/notes/leg2_primary_t4_route_smoke_2026_07_07.py`): S1 route-correctness (bone→FISSION / crypt→SOVEREIGNTY under `focus`; routed == ranker argmax = faithful pass-through); S2 `$0` byte-diff (8-kit non-summoner × {[],None} byte-identical off route). 263 regression PASS.
- **C1** captured in `generation/MIGRATION.md [2026-07-07] LEG-2` (three-seam lockstep; interim divergence window documented). Leg-3 HELD (confirmed).

**⚑ KR-TRIAGE FLAG (pre-existing, NOT leg-2):** `tests/test_w3_emission_driver.py::TestW3EmissionDriverSmokeRun::test_smoke_dry_run_completes` FAILS on the CLEAN baseline too (verified by stashing rocket's leg-2 files: 1 failed / 13 passed) — a pre-existing ENVIRONMENTAL emission-driver smoke failure with documented history, independent of the additive landing. **Watch-point for leg-3:** leg-3 IS an emission run; confirm whether this smoke failure touches the leg-3 emission driver path BEFORE the leg-3 run relies on it (rocket to assess in the leg-3 fire; captured in rocket AGENT_STATE + Gate-2 submission).

**Fired (parallel — both build against rocket's C2 constant @ HEAD):**
- **star-lord validator-widen** (`ad49a55a92efb5630`): widen DDA-lock to admit `ACCEPTED_PROXY_PRIMARY_T4` for proxy-bearing kits; preserve lock for empty-decl; round-trip both cases; export MIGRATION lockstep. Tag `star-lord/v-batch2-dda-lock-validator-widen-1` → Gate-2.
- **gamora consume-side** (`af9955be987c9ea90`): route sim sites 2/3 (`gauntlet_sim.py:2267`, `unified_calibration_loop.py:3577`) through rocket's `route_primary_t4()` (same fn as emit ⇒ provably no divergence) OR consume emitted `primary_t4`; cert-baseline byte-intact; sim MIGRATION lockstep. Tag `gamora/v-batch2-primary-t4-consume-widen-1` → Gate-2.

**Next:** both halves land → **coordinated three-seam Gate-2** (rocket+star-lord+gamora; cite S1/S2 GREEN per C3/C4) → **rocket leg-3 emission run** (owes its own Disc #1.1 resource/LLM-cost projection + the W3-smoke check) → unblocks **star-lord Leg C** + **gamora summoner proxy-T4**.
**ON MATT unchanged:** Q7 (drax body held) + 450MB telemetry.db blob.

---

## ⭐ KR DELTA (2026-07-07, cont.) — leg-2 CONSUME-side (gamora) DONE; awaiting star-lord validator half

**gamora leg-2 CONSUME-side (C1) → DONE** (tag `gamora/v-batch2-primary-t4-consume-widen-1` @ `8d8e76b`, on rocket's `996f77d`; Gate-2 filed `qa/pending/2026-07-07-gamora-leg2-primary-t4-consume-gate2.md`):
- Both sim sites route through rocket's SHARED `route_primary_t4()` (not a re-impl, not a persisted-field consume): `gauntlet_sim.py:2279` + `unified_calibration_loop.py:3592`, with `proxy_decls = build_proxies_surface(kit.skills)` = the emit source verbatim (`season_generation_pipeline.py:528`) ⇒ sim decls == emit decls byte-for-byte. Divergence closed by construction, not mirrored.
- **⭐ Structural clarification (load-bearing for leg-3 scoping):** rocket's leg-2 added the route FUNCTION but has NOT wired the emit assignment — `season_generation_pipeline.py:404-412` still holds the old DDA slot. **Wiring the emit assignment to call `route_primary_t4()` + running the emission IS leg-3** (rocket's separate fire). ⇒ leg-2 (route fn + validator + consume) is INERT on the current all-non-summoner population; the proxy-bearing behavior change reaches the population only at leg-3.
- Cert-baseline byte-intact (all-non-summoner pop → DDA fallback byte-identical; Disc #12 no live-behavior shift). Non-summoner no-regression 8/8 byte-identical. C1 summoner route verified: bone→FISSION / crypt→SOVEREIGNTY / gravecaller→SOVEREIGNTY, all ∈ `ACCEPTED_PROXY_PRIMARY_T4` (imported from C2). MIGRATION lockstep CLOSES the v1.83/`:8371` producer divergence window.

**Awaiting:** star-lord validator-widen (`ad49a55a92efb5630`, in flight). On landing → **coordinated three-seam Gate-2** (rocket `996f77d` + star-lord + gamora `8d8e76b`; S1/S2 GREEN cited per C3/C4) → **leg-3** (rocket: wire emit assignment + emission run; owes Disc #1.1 projection + W3-smoke check) → unblocks star-lord Leg C + gamora summoner proxy-T4.

---

## ⭐ KR DELTA (2026-07-07, cont.) — leg-2 VALIDATOR (star-lord) DONE; all 3 halves landed; coordinated Gate-2 FIRED

**star-lord leg-2 VALIDATOR-widen → DONE** (tag `star-lord/v-batch2-dda-lock-validator-widen-1` @ `0f7de25` = engine HEAD; Gate-2 filed `qa/pending/2026-07-07-star-lord-dda-lock-validator-widen-gate2.md`):
- Site `export/cycle14_wave5_emitter.py::validate_class_data()` (~L745). Conditional widen: `is_proxy_bearing = bool(proxy_decls)`; proxy-family branch rejects if `not is_proxy_bearing` ⇒ empty-decl DDA lock preserved. **Imports `ACCEPTED_PROXY_PRIMARY_T4` from `t4_catalog_v2` (C2 single-source); RETIRED the W0 local `_PROXY_FAMILY_PRIMARY_T4_STRATEGIES`; ZONE_CONTROL now correctly excluded** (it was wrongly in the W0 local set).
- Round-trip 3 cases GREEN (summoner+FISSION admit / empty-decl+stray reject / ZONE_CONTROL-on-summoner reject). 115/115 validator suite + 303/303 broad regression PASS.

**⇒ ALL THREE leg-2 halves landed, linear on HEAD:** rocket `996f77d` (producer) → gamora `8d8e76b` (consume) → star-lord `0f7de25` (validator). C2 constant single-sourced in `t4_catalog_v2`; C1 divergence closed by construction (gamora routes via rocket's exact `route_primary_t4()`).

**Coordinated three-seam Gate-2 FIRED** (jack-ryan `a9c8804f2a218600e`): verifies the three AS A UNIT (C2 single-source no divergent copies / C1 sim==emit / C3 S2 byte-diff + C4 S1 route-correctness / validator both directions / cert-baseline byte-intact + leg-2-inert-pre-leg-3 / regression). Also disposing the lingering `qa/pending/2026-07-07-rocket-proxy-t4-b1-rebase-phase1-v3-refire-gate1.md` (decisions already ratified piecemeal: gandalf DoF-A + jack-ryan F-f-B4-scoped at `a5ebd17` + gamora ext Gate-2 `dce4ae4`).

**Next (on Gate-2 PASS):** **leg-3** — rocket wires the emit assignment (`season_generation_pipeline.py:404-412`, still DDA slot) to call `route_primary_t4()` + runs the emission; owes Disc #1.1 resource/LLM-cost projection + the pre-existing `test_w3_emission_driver` smoke check. Leg-3 = the unblocking event for **star-lord Leg C re-fire** + **gamora summoner proxy-T4**.
**ON MATT unchanged:** Q7 (drax body held) + 450MB telemetry.db blob.

---

## ⭐ KR DELTA (2026-07-07, cont.) — leg-2 coordinated Gate-2 PASS (leg-2 CERTIFIED); leg-3 STEP-1 prep fired

**Coordinated three-seam leg-2 Gate-2 → PASS-WITH-FOLLOWUPS** (jack-ryan, finding `qa/findings/2026-07-07-leg2-summoner-emission-route-coordinated-gate2.md`, `3bae44a`; 4 pending items archived incl. Phase-1 disposal; 2026-07-07 pending queue CLEAR). All 6 points verified vs SOURCE as a UNIT: (1) C2 single-source, no divergent copies (star-lord W0 local = bare alias; gamora/star-lord import); (2) C1 divergence CLOSED by construction (both sim sites call rocket's exact `route_primary_t4` w/ same `build_proxies_surface`; sim==emit, 3 MIGRATIONs cross-ref); (3) C3/C4 re-run GREEN (rocket 14/14, gamora S2 8/8); (4) validator both directions (115/115: admit-on-summoner / reject-on-empty-decl / ZONE_CONTROL reject); (5) cert-baseline byte-intact, emit path NOT wired (`season_generation_pipeline:404-412` still DDA) ⇒ leg-2 INERT pre-leg-3 (Disc #12); (6) 378 tests green across all three seams together. **NO BLOCK.** ⇒ **leg-2 three-seam machinery CERTIFIED.** Leg-3 readiness call: **GREEN.**

**Leg-3 = a distinct Matt-gated phase.** jack-ryan explicit: leg-3 needs "its own dispatch + Gate-1 + **Matt authorization for the run**" (emission run = ADR-006 external/compute action + LLM-cost). **KR authored leg-3 dispatch** (`dispatches/2026-07-07-rocket-leg3-summoner-emission-wire-and-run.md`) STAGED:
- **STEP 1 (prep, NO code/run — fires now):** emit-wiring design note (`season_generation_pipeline:404-412` DDA slot → `route_primary_t4()`) + **Disc #1.1 resource/LLM-cost projection (the artifact Matt authorizes the run against)** + `test_w3_emission_driver` root-cause (gating vs orthogonal) → Gate-1.
- **STEP 2 (wire + run — fires ONLY on Matt run-auth + Gate-1 PASS):** land emit-wiring, run pilot emission (within projected envelope), measure §8-A1 bands, → Gate-2. **= unblocking event for star-lord Leg C + gamora summoner proxy-T4.**

**rocket leg-3 STEP-1 FIRED** (`afca173ebc7fb5326`): design + projection + W3-root-cause → Gate-1. Reports the cost envelope to KR → KR relays to Matt for run-auth.

**Two B4-scoped leg-2 followups (parked, NOT leg-3):** rocket `enforce_family_max_one` live-wiring before B4; then F-f test promotion.

**ON MATT (now 3 items):** (i) **Q7** BoneMap-vs-GeneralSkeleton (drax body held); (ii) **450MB telemetry.db blob** disposition; (iii) **leg-3 emission-run authorization** — pending rocket's STEP-1 resource/LLM-cost projection (KR will relay it).

---

## ⭐ KR DELTA (2026-07-07, cont.) — leg-3 STEP-1 RETURNED (design+projection+W3 root-cause); Gate-1 FIRED

**rocket leg-3 STEP-1 → DELIVERED** (math note engine `0384dbb` `generation/math/leg3-summoner-emission-wire-and-projection-2026-07-07.md`, collab `297220a`; Gate-1 pending `qa/pending/2026-07-07-rocket-leg3-summoner-emission-wire-projection-gate1.md`). Three findings:

1. **⚠️ LOAD-BEARING ROUTING CORRECTION (re-scopes STEP-2):** the leg-3 dispatch's cited wire site `season_generation_pipeline.py:404-412` is only a **dataclass field def** — `KitCandidate.primary_t4` is NEVER assigned in the pipeline. The **REAL DDA emission stamp is `cycle14_wave5_emitter.py:546`** — **star-lord's export seam.** ⇒ **STEP-2 is a rocket+star-lord CO-DISPATCH, NOT a solo rocket landing.** 4 touch-points: **3 in star-lord export/** (emit-wire + adapter, driver-drive, glyph-assertion-fix) + **1 in rocket** (`bc_target_composer.py` proxy-bin un-gate). *(This is the staged-dispatch discipline paying off — STEP-1-first caught the seam error before a blind cross-seam build fired.)*

2. **Disc #1.1 resource/LLM-cost projection (THE run-auth artifact):** ≤200-candidate deterministic pilot, **seed 56M**, ~23 min expected / ≤36 min worst-case, **50–80 MB RSS**, ≤7 concurrent entities. LLM cost: **$0 dry-run** (no LLM calls) / **≤$10 flavor ceiling** (~$6.50 expected) if named pilot kits wanted. **rocket recommended run-auth framing (verbatim):** *"authorize the $0 dry-run unconditionally + a ≤ $10 flavor ceiling if named pilot kits are wanted."*

3. **W3-smoke root-cause:** `test_w3_emission_driver` fails on clean baseline via a hard-coded `BRUISER==300 / GLASS_CANNON==400` glyph-split assertion (no smoke guard) — **orthogonal to the emit path (zero proxy refs) but WILL halt a proxy-inclusive pilot run.** Fix = population-aware assertion in **star-lord's export seam** → folds into STEP-2.

**jack-ryan Gate-1 FIRED** (`afbe3d240a44f97f1`, RUNNING): verify routing correction vs source (real stamp @ `cycle14_wave5_emitter.py:546`), confirm STEP-2 co-dispatch touch-point inventory + seam attribution, sanity-check projection/call-count math, verify W3 orthogonality.

**Next (on Gate-1 PASS + Matt run-auth):** KR authors leg-3 **STEP-2 rocket+star-lord co-dispatch** (4 touch-points above). Emission RUN itself stays Matt-gated (ADR-006).
**ON MATT (3 items):** (i) Q7 (drax body held); (ii) 450MB telemetry.db blob; (iii) **leg-3 run-auth — envelope now in hand: $0 dry-run unconditional + ≤$10 flavor ceiling (~$6.50 exp).**

---

## ⭐ KR DELTA (2026-07-07, cont.) — leg-3 STEP-1 Gate-1 PASS-WITH-CONDITIONS; STEP-2 co-dispatch AUTHORED (run Matt-gated)

**jack-ryan Gate-1 on leg-3 STEP-1 → PASS-WITH-CONDITIONS** (finding `qa/findings/2026-07-07-rocket-leg3-summoner-emission-wire-projection-gate1.md`, `bdca4a7`; pending archived). All 5 load-bearing claims verified vs SOURCE at `0384dbb` (not trusted from note):
- **Routing correction RATIFIED** — `season_generation_pipeline.py:404-412` is field-def only (never assigned, grep 0 hits); real DDA stamp `cycle14_wave5_emitter.py:546` (star-lord export). Emit-wire design SOUND (adapter Clause D `dict(PRIMARY_T4)` byte-identical for solo per validator `:795-841` DDA-match; `route_primary_t4` returns `AlterationOutput` dataclass ⇒ adapter net-new). §8-A1 bands correctly MEASURED-not-threshold. Cost projection honestly bounded ($0 dry-run levers real @ `:703`/`:792`). W3-smoke orthogonal-but-gates CONFIRMED.
- **STEP-2 touch-point inventory CONFIRMED + seam-attributed:** 4 touch-points — 3 star-lord export (emit-wire+adapter `cycle14_wave5_emitter.py:546`, driver-drive + glyph-assertion-fix `w3_emission_driver.py:688`) + 1 rocket (`bc_target_composer.py:97` proxy-bin un-gate). ⇒ **STEP-2 = rocket+star-lord CO-DISPATCH.**
- **4 fold conditions (none block):** C1 rocket doc-only line-ref (`chain_wide_own` vocab @ `:67-68` not `:451`); C2 carry ≤7-entity peak as STEP-2 rehearsal-measure; C3 carry §2.5 `t4_candidates` A1-coverage as STEP-2 measure; C4 star-lord §4.4 fix option (b) — non-empty + all-glyphs-valid, no exact split pinned.

**KR authored STEP-2 co-dispatch** `dispatches/2026-07-07-rocket-starlord-leg3-STEP2-emission-wire-and-run.md` (design Gate-1-cleared; folds C1-C4). Structure: **STEP-2A WIRE** (lands on dispatch: star-lord emit-wire+adapter+driver+assertion-fix, rocket composer un-gate; round-trip smoke; MIGRATION lockstep) → **STEP-2B RUN two-tier, Matt-gated:** Tier-1 **$0 dry-run** (unconditional on Matt go; 0 LLM calls, ~23-36min, wire-proof + §8-A1 band measure + C2 peak + C3 A1-coverage) → Tier-2 **≤$10 flavor** (SEPARATE Matt rule, deferred until Tier-1 bands seen).

**ON MATT (3 items) — run-auth now framed two-tier:** (i) Q7 (drax body held); (ii) 450MB telemetry.db blob; (iii) **leg-3 run-auth = (a) $0 dry-run unconditional now + (b) ≤$10 flavor ceiling deferred/optional** (jack-ryan's de-risking posture). STEP-2A wire may land on the co-dispatch immediately once Matt says go on the dispatch; STEP-2B run holds for the two-tier auth.

---

## ⭐ KR DELTA (2026-07-07, cont.) — MATT RULINGS BATCH (Q7 / 450MB / leg-3 STEP-2 GO + Tier-1 run-auth)

**Matt 2026-07-07 ruled 4 items + fire order.** Standing guards unchanged (chassis FROZEN, bars/bands FIXED, kits vote BARE, no magnitude touch, no leg-2 machinery changes; Gate-2 on STEP-2 artifacts).

1. **Q7 → OPTION A** (authored per-variant BoneMaps → GeneralSkeleton). `apply_hero_retarget.py` + per-family `.tres` (`sidekick_bone_map` + `goblin_bone_map`) = v2 demo canonical retarget contract; superset eye-check-skip nuance adopted. **drax UNBLOCKED → D6 (three-beat floor + capture) + D5 (verb VFX + summon meshes) + D8 (grimoire portraits)**, all under FIXED Camera B (FOV40/pitch−55°/yaw47°/dist34m, not re-litigated). Dispatch `dispatches/2026-07-07-drax-q7-optionA-rig-gated-D6-D5-D8.md`. jack-ryan files decisions-log.

2. **450MB telemetry.db → gitignore + seed fixture. DONE (star-lord).** Engine push was HARD-BLOCKED by GH 100MB hook (`e57b796` v2.20 APPLY bloated the tracked DB to 450MB). star-lord: gitignored `telemetry.db` (kept on disk), rewrote unpushed history `e57b796`→`1c00a06` stripping ONLY the blob (all scaffold/gear-pool work preserved), added `telemetry_seed.db` (376KB, empty v2.20 schema — fresh checkout reconstructs via `initialize_telemetry_db()`; registry = durable record), re-pointed 6 seam tags + confirmed milestone tag. **PUSHED: `a908ced..44fc92d` engine main + 15 tags incl. milestone `v2.2-batch2-four-family-certification`.** KR-verified: HEAD==origin/main, .db untracked+ignored+on-disk, seed tracked, .db absent from HEAD tree. **Engine push blocker CLEARED; four-family cert milestone now on remote.**

**Also pushed this batch (Matt "yes please"):** collaboration main + 8 tags, demo main, loadout main + 2 tags. godot clean. (engine was the only reject; now resolved.)

3. **Leg-3 STEP-2 co-dispatch → GO.** STEP-2A wire lands now (star-lord TP1-3 + rocket TP4, C1-C4 folded) on clean engine HEAD.

4. **Run-auth two-tier (ADR-006):** **TIER-1 AUTHORIZED** = $0 dry-run (`dry_run_flavor=True`, ≤200 cand, seed 56M, 0 LLM). Report to Matt: §8-A1 bands + C2 peak-concurrent-proxy + C3 A1-coverage. **TIER-2 NOT YET** — ≤$10 flavor is a SEPARATE ruling Matt takes AFTER the Tier-1 band report; NO LLM spend on this lane until then.

**Fire order:** blob-fix DONE+pushed → jack-ryan decisions-log (Q7+450MB) FIRING → STEP-2A co-dispatch GO (rocket+star-lord, clean HEAD) → Tier-1 $0 dry-run → band report to Matt. drax runs parallel (godot/demo, no engine conflict).

---

## ⭐ KR DELTA (2026-07-07, cont.) — leg-3 STEP-2A: rocket STOP-FLAG (composer un-gate INERT); §8-A1 heavy-band coverage routed to Matt

**rocket STEP-2A TP4 → STOP-and-FLAG (correct; NO inert edit made).** Verifying vs source (Disc #11) before editing, rocket found the composer un-gate @ `bc_target_composer.py:97/:318` is **INERT for the leg-3 pilot path** — the pilot runs `w3_emission_driver → w5r1_generate_kit_candidates → ENDGAME_ENCOUNTER_CATALOG`, which never imports `bc_target_composer`. Lifting `_DEFERRED_PROXY_BINS` = 0 proxy cells added (n_proxy_cells 1→1) + silent change to an orphan path = duct-tape faking an un-gate signal. **rocket did NOT tag** (`rocket/v-batch2-leg3-composer-ungate-1` NOT applied — inert), NO MIGRATION. **Self-corrected its own STEP-1 §3.1 causal claim** (composer-gate→0-proxy-kits was WRONG; trusted sim-side spec prose vs tracing the driver path — Disc #19.1). C1 doc line-ref folded (`:451`→`:67-68`, verified). Commits: `db1bbe1` (engine math-note C1 + AGENT_STATE), `f9ec4e6` (collab STOP-flag note `rocket/notes/2026-07-07-leg3-composer-ungate-inert-STOP-flag.md`), `14ed369` (dispatch completion). Pushed. Smoke `test_w02_bc_target_composer` 45 pass (untouched).

**REAL pilot proxy gate = `ENDGAME_ENCOUNTER_CATALOG` curation: 17 none / 1 light / 0 heavy.** The 1 proxy-LIGHT cell composes with a real proxy decl (n_skills=13, n_proxies=1) via live leg-1 summon path ⇒ Tier-1 dry-run CAN prove wire+emit end-to-end at $0 + measure the LIGHT band. **Zero proxy-HEAVY coverage ⇒ §8-A1 heavy-share band NOT measurable this pilot.**

**Sequencing correction:** star-lord TP1-3 + Tier-1 run do NOT wait on any composer un-gate (there is none). BUT the heavy-band gap is a scope-of-run decision on the §8-A1 acceptance line ⇒ **routed to Matt (KR held star-lord's wire+run pending ruling; Option 3 would change star-lord's driver work).**

**DECISION ROUTED TO MATT — §8-A1 band coverage:** (1) run pilot as-is = wire-proof + LIGHT band + C2 + C3, report HEAVY NOT-EXERCISED [$0, no new scope — rocket + KR rec]; (2) author deferred proxy-heavy cells [content wave, own math-note+Gate-1]; (3) re-point driver at `bc_target_cell_sampler.CELL_DEFINITIONS` [star-lord driver-source swap, cross-seam]. **KR rec: Option 1 now + Option 2 as named follow-up** (alongside the held Tier-2 flavor decision). On Matt Option-1 nod → fire star-lord TP1-3 + Tier-1 $0 dry-run → band report.

**Process note:** staged-dispatch discipline caught the inert-edit + STEP-1 causal error at STEP-2A execution BEFORE any run fired (STEP-1-first + Disc #11 inspect-source). Gate-1 verified routing/touch-points vs source but did not re-derive the composer→0-proxy causal claim (it lived in rocket §3.1, trusted by both). No harm — caught pre-run.

---

## ⭐ KR DELTA (2026-07-07, cont.) — Matt RULED §8-A1 STOP-flag = OPTION 1 (run pilot as-is) + 3 binding riders; star-lord TP1-3 + Tier-1 FIRED

**Matt ruling: OPTION 1 — run the leg-3 pilot as-is.** Three BINDING riders:
1. **Composer un-gate (TP4) = DEFERRED-NOT-DROPPED** → re-home to **batch-2 Leg C** (summoner leg). **rocket verifies Leg C actually consumes `bc_target_composer` BEFORE landing it there; if nothing downstream consumes it either, flag as DEAD CODE rather than carry forward.** [PARKED — rocket, Leg C.]
2. **§8-A1 proxy-heavy band + C2 worst-case peak-entity read = re-home to batch-2 Leg C** (population-level) and/or **gamora sim-side concurrency measurement.** Option 2 stays PARKED unless something gates on a heavy read before Leg C. **Option 3 REJECTED** — a cross-seam driver re-point mid-authorization invalidates the Gate-1-reviewed run projection. [PARKED — Leg C / gamora.]
3. **Report honesty (batch-2 R1 registry-honesty discipline):** Tier-1/Tier-2 reports carry an explicit **NOT-EXERCISED** line for the proxy-heavy band; C2 peak-entity read is **light-band-only** (1 light cell, n_proxies=1); the **≤7 worst-case bound stays UNPROVEN** this pilot. No coverage claims beyond the catalog's 17 none / 1 light / 0 heavy. [BINDING on star-lord's run.]

**star-lord FIRED:** TP1 emit-wire+adapter @ `cycle14_wave5_emitter.py:546`, TP2 driver drive @ `w3_emission_driver.py` (NO driver-source re-point — Option 3 rejected; drive catalog as-is), TP3 glyph-assertion→population-aware @ `:688` (option b). Round-trip smoke + export MIGRATION lockstep + tag `star-lord/v-batch2-leg3-emission-wire-1`. Then **Tier-1 $0 dry-run** (`dry_run_flavor=True`, seed 56M, ≤200 cand) → measure LIGHT §8-A1 band + C2 (light-only) + C3 A1-coverage, honesty riders binding → Gate-2 submit. → band report to Matt.

**Parked follow-ups (post-run):** rider-1 (rocket composer→LegC-consumer-verify-or-deadcode), rider-2 (heavy-band + C2 worst-case → LegC/gamora), Tier-2 flavor decision (Matt, after Tier-1 bands). **drax Q7 dispatch launched-parallel (godot).**

---

## ⭐ KR DELTA (2026-07-07, cont.) — Tier-1 $0 dry-run FAILED (hung in STEP 3/4 live gauntlet); NO bands, $0 spent; re-fire routed to Matt

**OUTCOME: Tier-1 dry-run did NOT complete. No bundle, no §8-A1 bands, no measurements. $0 spent (never reached flavor).** Process launched 23:11:04, hung, sat silent 29 min, vanished 23:44:04. No OOM, no crash trace, no partial output.

**Forensic timeline (verified against `/tmp/leg3_pilot_n1_run.log`, 18163 lines):**
- Header confirms authorized Tier-1 params: `n_samples_per_cell=1  seed=56000000  smoke=False  dry_run_flavor=True`. ✓
- [STEP 0] Setup ✓ → [STEP 2] generated **18 candidates** ($0, no LLM) ✓ (23:11:04).
- **[STEP 3/4] "Running gauntlet on 18 candidates via w5r2_gauntlet_sim_integration…"** ← fired a **LIVE gauntlet sim**.
- Live gauntlet entered R2 spatial-gauntlet calibration; **last-logged locus = non-converging class `S1_endgame_bc_melee_medium_variable_str_none_s0`** (bimodal geometry — open_arena WR=0.000 floor-saturating / chokepoint_corridor WR=1.000 ceiling-saturating; calibrator not resolving). Log froze **23:15:15** mid-calibration.
- Process persisted **29 min silent** (23:15→23:44), then disappeared. **STEP 5+ (§8-A1 band measure / bundle write) NEVER reached.**

**Root locus (honest framing per registry-honesty rider):** the run hung in the STEP 3/4 **live gauntlet**, last logging the non-converging melee-class calibration. The 29-min silent gap (23:15→23:44) is UNOBSERVED — the *proven* fact is the hang was in STEP 3/4; the *exact* hang mechanism (infinite calibration retry vs deadlock vs post-calibration stall) is UNPROVEN from the frozen log.

**Why recovery-mode didn't save it:** `w3_emission_driver.py` has a `--recover-from-canonical` fast-path (`_recover_gauntlet_from_canonical_json`, skips re-running the 6h gauntlet) — but it's **hard-coded to the batch-1 shape** (`_RECOVERY_EXPECTED_SURVIVOR_COUNT=700` = 7 cells × 100 samples; `_RECOVERY_EXPECTED_ENTRY_COUNT=2200`). This 18×1 pilot is a different population ⇒ recovery would halt-loud on its asserts ⇒ the **live gauntlet was the only available path**, and it hung.

**Disc #1.1 / #2.1 miss:** the Gate-1-reviewed resource projection (~23–36 min) modeled the emission/band phase but **under-modeled STEP 3/4** — that a live gauntlet on 18 endgame candidates (incl. a non-converging bimodal-geometry class) can hang unbounded. No resource-scaling rehearsal of STEP 3/4 preceded the run.

**Cost posture: CLEAN.** $0 LLM (dry_run_flavor + never reached flavor). Only cost = ~33 min wasted local compute. No ADR-006 spend harm. Engine HEAD `2779b62` unchanged by the failed run (1 unpushed = star-lord's pre-run in-progress commit; no new commits).

**ROUTED TO MATT — re-fire disposition.** KR will NOT reschedule (process dead) and will NOT re-fire blind (ADR-006; it'll hang again). Recommended: **star-lord + gamora diagnosis dispatch** before any Tier-1 re-fire — (a) star-lord: does STEP 3/4 need a live gauntlet at all for a $0 band-measurement dry-run, or can the driver gate/skip the gauntlet (or generalize recovery-mode) for the leg-3 pilot config? (b) gamora: the `medium_variable` spatial-calibration non-convergence (bimodal floor/ceiling) — is it a calibration bug or a genuine geometry-partition problem, and does it need a convergence-timeout guard? **Held for Matt's routing nod.**

---

## ⭐ KR DELTA (2026-07-07, cont.) — Tier-1 RE-FIRE (v3): gauntlet COMPLETED but 0/18 survivors → TP3 HALT-LOUD; spatial-calibration floor-saturation is the locus; still no bands, $0

**v3 (`/tmp/leg3_n1_v3.log`, launched 23:17, driver params identical: `seed=56000000 dry_run_flavor=True n_samples=1`) COMPLETED the gauntlet** — no hang this time (25,530 fights, 1588.3s ≈ 26.5 min). Different, more informative failure than the earlier hang.

**Outcome: 0 in-band survivors → HALT-LOUD, no bundle, nothing to extract, $0 spent.**
- `[W5R.2] WR-bracket filter (Q10 substrate-led season_emit gate): **0 passing / 18 failing / 18 total**`.
- `[W5G.2] GAUNTLET_SIM_PASS=False | kits_season_emit=0 | round_trip_smoke_pass=True | 25530 fights | 1588.3s`. (Round-trip smoke PASSED — telemetry path intact.)
- `[STEP 4] In-band survivors: 0 / 18 (0.0% yield)`; identity_glyph split BRUISER=0 GLASS_CANNON=0 SUMMONER=0 other=0.
- **`HALT-LOUD (leg-3 TP3): identity_glyph assertion — survivor_kit_records is EMPTY.`** ← star-lord's population-aware TP3 guard (option b) **fired correctly** — refused to emit a degenerate empty bundle. **The leg-3 wire behaved exactly as designed; it simply had zero kits to carry.**

**LOCUS (strong-inference, causal link is the diagnosis question): spatial-gauntlet calibration floor-saturation.** ~11 of 12 endgame BC classes floor-saturate (WR=0.000, ≤0.05 floor) in ≥1 scenario (323 floor events vs 278 ceiling). The log's own R2-calibration warning names the trigger + remedy verbatim: *"If ≥80% of classes floor-saturate: reduce MOB_HP 1.5→1.25 per L1 authority"* (`MOB_HP_DIFFICULTY_MULTIPLIER=1.5`, `LEASH_DISTANCE_OVERRIDE_M_SWARM=35.0`). With nearly every class pinned at WR=0.000, the Q10 WR-bracket season_emit gate rejects all 18 candidates ⇒ 0 survivors ⇒ leg-3 emit path never exercised.

**Honest framing (registry-honesty rider):** PROVEN — v3 completed; 0/18 WR-bracket passes; ≥11/12 classes floor-saturate; TP3 guard fired correctly; no bundle; $0. INFERRED (not proven by KR) — that the 0-yield is *caused* by the spatial floor-saturation vs some other WR-bracket rejection; the causal link is the gamora diagnosis question (strongly supported by the log's own ≥80%-floor remedy note).

**No Gate-2 submission written** — there is no passing artifact; a Tier-1 "measurements" Gate-2 for an empty HALT-LOUD run would be dishonest. This is a FAILURE/forensics record.

**ROUTED TO MATT — same diagnosis dispatch, sharper signal.** Not the earlier hang; a 0-yield calibration floor. Recommended **gamora + star-lord co-diagnosis before any Tier-1 re-fire:** (a) **gamora (sim, primary):** the R2 spatial-gauntlet is broadly floor-saturated at `MOB_HP=1.5` for endgame BC classes — is the L1-authority `MOB_HP 1.5→1.25` reduction the right move, and is this a KNOWN uncalibrated state (gamora Step-3 / R2 work) that leg-3's pilot inherited, orthogonal to the wire? (b) **star-lord (driver):** should an 18×1 $0 band-measurement dry-run even gate season_emit on the full spatial gauntlet, or is the WR-bracket threshold wrong at n_samples=1? **Held for Matt's routing nod.** Engine HEAD `2779b62` unchanged (0 survivors ⇒ no new artifacts committed).

---

## ⭐ KR DELTA (2026-07-08) — gandalf Lane-C GO: co-diagnosis dispatch AUTHORED (gamora PRIMARY + star-lord); both deltas pushed

**gandalf Lane-C v3-aware verdict (Matt) = GO on both.** Deltas `3d2b8aa` + `6d11556` confirmed on remote (push up-to-date). Co-diagnosis dispatch authored: `dispatches/2026-07-08-gamora-starlord-spatial-floor-diagnosis.md` (Pattern B co-fire, gamora PRIMARY / star-lord secondary). All 8 riders folded:
1. **MEASURE-THEN-FILTER (star-lord):** decouple §8-A1 band REPORT from WR-bracket GATE — measure all 18, report bands+gate side by side; next re-fire yields §8-A1 bands even if 0 pass bracket (coin-flip → guaranteed diagnostic yield).
2. **Convergence/fail-loud guard (gamora):** REQUIRED unconditional deliverable — R2 loop must HALT-LOUD on non-convergence, not wedge silent (v2 29-min wedge = Disc-#24 violation; v3 same-params completion ⇒ INTERMITTENT).
3. **Diagnosis GATES LEG C** (critical path; nothing Tier-1+ re-fires until dispositioned).
4. **Don't fix CONTENT to satisfy INSTRUMENT:** 11/12 floor-saturating ⇒ instrument suspect; `melee_medium_variable` bimodality (open 0.000 / choke 1.000) = positional identity, live hypothesis not defect.
5. **Goodhart guard (gamora G1, load-bearing fork):** MOB_HP 1.5→1.25 legit ONLY if 1.5 known-uncalibrated-inherited; if 1.5 RULED ⇒ WR=0.000 is a DESIGN FINDING, softening = drift.
6. **Recovery-mode batch-1 fossil (700/2200)** = NAMED follow-up, out of scope.
7. **Kill-verify before re-fire** (v2/v3 parallel-same-seed window).
8. **Credit:** failure infra WORKED — TP3, round-trip smoke, registry-honesty, $0; wire PROVEN, breakage is upstream.

**Gate posture:** code deliverables (gamora guard + conditional MOB_HP; star-lord decoupling) → jack-ryan Gate-2 on submission. G1 disposition (ruled vs inherited) routes back to Matt/gandalf. ~~Re-fire = SEPARATE Matt run-auth (ADR-006) AFTER this lands.~~ *(Superseded 2026-07-08 — the run-auth is PRE-GRANTED by the ratified chain table below, R2.)* **Launch:** `cd ~/Games/reincarnated-engine && claude --agent gamora` (+ a star-lord session); both read `dispatches/` at start.

---

## ⭐ PRE-RATIFIED AUTONOMOUS CHAIN (gandalf-authored, Matt-ratified "Agreed" 2026-07-08) — the diagnosis-return execution contract

> **Authority:** Matt ratified R1–R6 (gandalf ELICITOR grill, 2026-07-08 session). This table IS the run-authorization for the chain below — **it pre-satisfies the dispatch's "re-fire = SEPARATE Matt run-auth (ADR-006)" clause** (ADR-006 honored by THIS pre-authorization; the clause above is struck accordingly). KR executes against this table without fresh Matt asks.

**The chain:** diagnosis returns → [R1] → guards + decoupling land + Gate-2 → [R2] Tier-1 re-fire ($0) → §8-A1 bands + gate report → [R4] Leg-C full fire (ruled arc numbers) → batch-2 closes → [R5] band-sheet draft → **Matt ratifies VALUES** → §7 loot campaign (already zero-round-trip per the 2026-07-07 Q9/Q10 rulings).

| # | Ruling (Matt-ratified 2026-07-08) |
|---|---|
| **R1** | **MOB_HP disposition conditional.** G1 = inherited-uncalibrated → the L1 remedy (`1.5→1.25` or gamora's calibrated value) auto-applies (+ MIGRATION + Gate-2); chain proceeds. G1 = 1.5 IS the ruled difficulty → **HALT-LOUD for Matt** (design finding: endgame BC can't clear ruled difficulty — content/difficulty ruling is his). |
| **R2** | **Tier-1 auto-re-fire.** Fires with NO fresh Matt ask once ALL empirical criteria are green: (a) G3 convergence guard landed + tested · (b) star-lord measure-then-filter landed + 0/18-pass round-trip smoke green · (c) R1 dispositioned green (branch a, or branch b subsequently ruled) · (d) kill-verify — no prior driver PID alive, never two same-seed emissions · (e) **jack-ryan Gate-2 green on the dispatch deliverables**. Run posture: $0 (dry_run_flavor), bounded (guard), guaranteed yield (measure-then-filter). |
| **R3** | **Bimodality containment.** If G2 finds genuine positional identity, the scalar-vs-vector certification-semantics fork is a **Leg-C gate item** (flagged on the Leg-C run report), never a Tier-1 blocker. Tier-1 measures regardless — measurement is fork-independent by construction. |
| **R4** | **Leg-C hold-clear.** The rider-3 hold clears AUTOMATICALLY when Tier-1 bands land + R1/R3 green. Leg C fires at the ruled arc numbers with the §8-A1 re-homes (heavy-band coverage + C2 worst-case peak) as REQUIRED report items. No fresh authorization round-trip — Leg C was already authorized (ARC NUMBERS ruling + Option-1 riders, 2026-07-07). |
| **R5** | **Band-sheet pre-draft.** When Leg-C bands land, the band-sheet proposal drafts automatically (gamora numbers → gandalf design-spec → jack-ryan review). **Matt ratifies VALUES** (resist/mitigation caps, band widths — the Q10 remainder) — the designed human gate, unchanged. |
| **R6** | **Chain guardrails.** $0 LLM throughout — any step that would spend LLM halts loud (ADR-006 posture) · any HALT-LOUD anywhere STOPS the chain, no auto-resume past a halt · **push-as-you-go granted for chain commits** (per-workstream push pattern, CLAUDE.md). |

> **R1 CONSUMED + R3a AUTHORIZED (2026-07-08, post-ratification amendment):** the R1 touchpoint fired in design-finding form and **Matt ruled A/yes/yes** — see the ⭐ MATT RULING delta at the file tail (latest-governs). The recalibration work unit (R3a) is now pre-authorized chain work between R2's bands and R4. Matt touchpoints outstanding: **R5 VALUES** + a *conditional* Lever-4 certification-criterion ruling (fires only if structural fails persist on a working gradient).

**Execution protocol (seam discipline, structural):** KR fires all sub-agent sessions/dispatches HIMSELF — coordinated sub-agent firing is KR's seam (hive-mind decision-routing, Matt 2026-05-23; CLAUDE.md team addendum 2026-05-25). Matt's transmission of this table = the authorization act; per-step "should I fire X?" asks are the retired anti-pattern. **Matt touchpoints in this chain are EXACTLY TWO: (1) the R1-(b) halt, if it fires; (2) R5 band-sheet VALUES.** Everything else: execute, commit, push, log deltas here. **ONE LIVE KR SHELL per this workstream** (the orchestration twin of kill-verify): a takeover session derives state from THIS file + the dispatch's completion record before acting — fire only what has not fired; NEVER re-fire a fired dispatch or run a step a prior shell holds in flight.

**Signed:** gandalf (ELICITOR → ARCHITECT), 2026-07-08.

---

## ⭐ KR DELTA (2026-07-08) — gamora PRIMARY diagnosis COMPLETE + KR-verified: DESIGN-FINDING path (no constant moves); G3 guard SHIPPED

**gamora done, KR-verified against source (trust-but-verify):**
- **G1 = DESIGN-FINDING path. NO CONSTANT MOVES.** `MOB_HP_DIFFICULTY_MULTIPLIER=1.5` is a **known-parked-uncalibrated state Matt-scheduling-pending**, NOT the ruled endgame difficulty. 4 verified sources: `arena.py:49` git-blame (one commit ever, `24cdc7e` 2026-05-19, calibrated vs old ~2019-HP swarm); `endgame_mob_stat_profile.py:8-16` explicitly declares itself "distinct from MOB_HP_DIFFICULTY_MULTIPLIER=1.5 … DOES NOT modify arena.py"; decisions-log 4240+5223 ("separate, Matt-scheduling-pending"). **KR spot-verified:** arena.py:49 still `1.5` (untouched by commit `03076c0`); the citation reads verbatim as claimed.
- **The `1.5→1.25` remedy is STRUCTURALLY INCAPABLE, not just uncalibrated:** `MOB_HP_DIFFICULTY_SCENARIOS = frozenset({open_arena, chokepoint_corridor})` — 1.5 does NOT apply to `magic_pack`, yet magic_pack = 111 of 323 floor events. Softening it to green the pilot = Goodhart drift. (Rider-5 Goodhart guard held.)
- **G2 = 10 of 12 bimodal-by-design; 0 uniformly-floored.** All 12 wall chokepoint at WR=1.000; floor is SCENARIO-specific (open_arena 212 + magic_pack 111), not class-brokenness. Dispatch exemplar `melee_medium_variable` is the population pattern, not an outlier. Instrument's difficulty state is the suspect, not the kits (rider-4 confirmed). Content untouched.
- **G3 = fail-loud convergence guard SHIPPED.** 3 layers in `SpatialFightEngine.run()` (tick-budget / continuous-spawn catch-up cap / wall-clock watchdog) + `SpatialFightConvergenceError` + log-ERROR-and-re-raise. Math-note-first. 312 spatial tests pass, byte-neutral on nominal fights. Tag `gamora/v-spatial-fail-loud-convergence-guard-1` (`03076c0`). **KR-verified guard present in spatial_engine.py.**
- **Artifacts:** Gate-2 `qa/pending/2026-07-08-gamora-g3-fail-loud-convergence-guard-gate2.md`; design-finding `gamora/notes/2026-07-08-spatial-floor-saturation-g1-g2-design-finding.md`; math note `simulation/math/r2-calibration-fail-loud-convergence-guard-2026-07-08.md`. Auto-committed both repos, NOT pushed (Matt-gated).

**CONSEQUENCE FOR MATT/gandalf (routed):** the parked `MOB_HP_DIFFICULTY_MULTIPLIER` recalibration is now on **Leg-C's critical path**. Correct levers = open_arena leash/positional geometry + the magic_pack HP-scope question — NOT a `1.5→1.25` tweak. That scheduling decision is Matt's. **star-lord (measure-then-filter) still running.**

---

## ⭐ KR DELTA (2026-07-08) — star-lord measure-then-filter COMPLETE + KR-verified; both halves Gate-2-ready; jack-ryan Gate-2 firing

**star-lord done, KR-verified against source:**
- **Ordering correct (the load-bearing check):** `_build_section8a1_band_report()` call @ `w3_emission_driver.py:666`, persist @ `:674`; TP3 HALT-LOUD assert @ `:901`. **674 < 901** — the §8-A1 band report persists BEFORE the emission gate can halt. A 0/18-pass re-fire now yields bands regardless. KR-verified line numbers.
- Report reads `bc_proxy_density`/`character_id` from ALL 18 KitCandidates (not just survivors); records per-candidate WR-bracket pass/fail + gate_outcome + band_summary + embedded `registry_honesty` (proxy-heavy NOT-EXERCISED, ≤7 UNPROVEN, C2 light-only, 17/1/0). Artifact: `output/leg3_pilot_section8a1_band_measurement.json` (analysis JSON only — bundle + run_registry schema unchanged; run_registry additively references path @ `:1290`).
- TP3 unchanged (still HALT-LOUDs empty survivor set — correct as emission gate).
- Round-trip smoke `test_zero_passing_round_trip_read_back`: 18 all-failing stubs → report persisted → read back → gate=0/18 truthful, bands intact, honesty riders present. 32/32 driver tests pass. Commit `061176c` touched ONLY export/ (KR-verified — no sim/drax/gamora consumer changes). Tag `star-lord/v-batch2-measure-then-filter-1`. MIGRATION § MEASURE-THEN-FILTER (additive). Gate-2 `qa/pending/2026-07-08-star-lord-measure-then-filter-gate2.md`.

**LANE STATE:** both code halves DONE + KR-verified. Two Gate-2 submissions pending → **jack-ryan Gate-2 firing on both.** G1 design-finding (MOB_HP recalibration on Leg-C critical path) routed to Matt as a scheduling decision. **Re-fire (ADR-006, Matt-gated) is NO LONGER a coin-flip:** with measure-then-filter, a re-fire yields §8-A1 bands even at 0/18 pass — so a diagnostic re-fire is now decoupled from the difficulty disposition. Matt owns: (a) re-fire-now-for-bands vs hold-for-recalibration, (b) MOB_HP recalibration scheduling.

---

## ⭐ KR DELTA (2026-07-08) — R6 push-as-you-go executed; R2 ARMED (4/5 green, waiting on jack-ryan Gate-2); R1→R4 nuance FLAGGED

**R6 push executed:** collab `2d7b51e..2e0fa5f`, engine `4aad1f1..061176c` + chain tags (`gamora/v-spatial-fail-loud-convergence-guard-1`, `star-lord/v-batch2-measure-then-filter-1`). Chain commits on remote.

**R2 (Tier-1 auto-re-fire) criteria status — ARMED, one gate remaining:**
- (a) G3 convergence guard landed + tested — ✅ GREEN (gamora, 312 tests, byte-neutral; KR-verified)
- (b) measure-then-filter landed + 0/18-pass round-trip smoke green — ✅ GREEN (star-lord, 32/32; KR-verified :674<:901)
- (c) R1 dispositioned green — ✅ branch-(a) [inherited-uncalibrated, NOT the ruled difficulty]; R1-(b) Matt-halt did NOT fire
- (d) kill-verify (no prior driver PID alive) — ⏳ KR checks at fire-time
- (e) **jack-ryan Gate-2 green on both deliverables — ⏳ IN FLIGHT** (the only remaining gate)

**On jack-ryan Gate-2 GREEN, KR auto-executes (no Matt ask, per R2 + Matt reaffirmation 2026-07-08):** fold verdict → push (R6) → kill-verify → fire Tier-1 $0 re-fire (dry_run_flavor, seed 56M, bounded by G3 guard, guaranteed yield via measure-then-filter) → push §8-A1 band artifact → log session-close.

**⚠️ R1→R4 NUANCE FLAGGED (KR one-step-ahead catch — for the R4 evaluation point, NOT a Tier-1 blocker):** R1 branch-(a) presumed "inherited-uncalibrated → scalar remedy auto-applies → instrument fixed." gamora's diagnosis broke that presumption: the `1.5→1.25` remedy is **structurally incapable** (1.5 doesn't touch magic_pack = 111/323 floor events), so gamora applied **NO constant** and routed the real fix (open_arena leash/positional geometry + magic_pack HP-scope) as **scheduling-pending recalibration work on Leg-C's critical path.** Consequence: **the instrument stays floor-saturated.** This is FORK-INDEPENDENT for R2/Tier-1 (measurement yields §8-A1 bands regardless — R3 confirms). BUT **R4 (Leg-C emission at ruled arc numbers) would emit ~0 surviving kits against the still-floor-saturated gauntlet** — so R4's "hold clears automatically when Tier-1 bands land + R1/R3 green" is NOT cleanly satisfied. **Likely a THIRD Matt touchpoint the pre-ratification didn't anticipate: schedule the recalibration BEFORE R4.** Surfaced now; adjudicate at the R4 point (post-Tier-1-bands). Tier-1 proceeds unaffected.

---

## ⭐ KR DELTA (2026-07-08) — jack-ryan Gate-2 PASS/PASS → R2 FIRED; gandalf R1-read formalizes the R1→R4 nuance as the R1 Matt touchpoint

**jack-ryan Gate-2 = BOTH PASS, no BLOCK, no conditions** (commit `3f525c5`). Both BLOCK-triggers I flagged came back CLEAR — jack-ryan re-verified against source AND re-ran 225 spatial regression + 32 driver tests + re-fired the guard smoke. Findings: `qa/findings/2026-07-08-spatial-floor-diagnosis-gate2.md` + two `-CLEARED.md`. Both submissions cleared from `qa/pending/`. **R2 criterion (e) GREEN.**

**R2 criteria — ALL 5 GREEN:** (a) G3 guard ✅ · (b) measure-then-filter ✅ · (c) R1 branch-(a) ✅ · (d) **kill-verify PASSED — no driver/emission PID alive** (KR-checked at fire-time) ✅ · (e) jack-ryan Gate-2 ✅. **R2 auto-fires (no fresh Matt ask, per the pre-ratified table).**

**gandalf R1-read landed (`1cb2f62`, `gandalf/notes/2026-07-08-spatial-difficulty-levers-design-read.md`) — CONFIRMS my R1→R4 flag and formalizes it:**
- **R2 is NOT blocked** (gandalf verbatim §5.1: "R2 re-fire proceeds as ratified once Gate-2 greens — it measures the CURRENT state and becomes the **before-side of the before/after diff**"). My guaranteed-yield framing now has a design purpose: the $0 re-fire is the *before* snapshot of the recalibration diff.
- **The instrument lost its gradient** (§1): 323 floor + 278 ceiling events, ALL exactly 0.000/1.000, no mid-band mass — a step function, not a gradient. Same degeneracy the ×1.5 was invented to repair on 2026-05-19, recurred in two-rail form because **3 difficulty dials moved independently and the joint state was never re-ruled** (HP regime ~13× · legacy ×1.5 still stacking in 2/3 rooms · density+geometry 8→40 mobs). HP is NOT the discriminant (magic_pack floors 7 kits at the LOWEST HP budget while everyone walls chokepoint at the HIGHEST) — engagement geometry is.
- **G2 refined:** PATTERN (differential WR by scenario) = design intent; AMPLITUDE (0.000/1.000 binary) = instrument artifact. Design wants melee at corridor-0.85 / open-0.35, not open-0.000 (a lockout no ARPG ships). Rider-4 stands: don't fix content to satisfy the instrument.
- **§6 asks = the R1 Matt touchpoint, in design-finding form (this IS the third touchpoint I flagged):** (1) HP-difficulty governance fork — **A** un-stack legacy ×1.5 from endgame path [gandalf lean; resolves the parked recalibration as SCOPE-RETIREMENT, no constant moves] / B extend+re-rule / C per-scenario spec block; (2) authorize serial-engagement (pack-local activation) design pass for open_arena + magic_pack [gandalf lean YES — restores genre open-field grammar the room certifies against]; (3) schedule steps 2-4 as the pre-R4 work unit on Leg-C's critical path [gandalf lean YES]. Anti-Goodhart acceptance criterion (§4): NOT "N/18 pass" — "WR surface regains a gradient: mass in (0.05,0.95), differentials persist as spread not rails."
- **Sequencing (§5):** R2 fires now ($0, before-side) → gamora $0 termination-split of the 323 floor events (death vs timeout, weights Lever 1 vs Lever 2) → Matt rules the §6 fork → gamora executes ruled levers + $0 re-run → before/after gradient check → R4/Leg-C hold-clears against a coherent difficulty state.

**KR execution (R6 push-as-you-go done; R2 fire HANDED OFF):** pushed chain commits (`3f525c5` + `1cb2f62` + `efdb84d`) to remote. **The §6 fork goes to Matt as the R1 touchpoint (surfaced, non-blocking); R4 stays held until Matt rules it + recalibration lands.**

> ⚠️ **CORRECTION (this delta's header said "R2 FIRED" — it did NOT fire).** Matt directive (2026-07-08): **do NOT fire R2 from this shell.** R2 is **ARMED 5/5** and **handed to a fresh autonomous session** which fires it as its FIRST chain act. See the SESSION-CLOSE + R2-HANDOFF delta below for the exact fire spec. This shell closes without firing.

---

## ⭐ SESSION-CLOSE + R2 HANDOFF (2026-07-08) — R2 ARMED 5/5, handed to the next (fresh autonomous) shell

**Matt directive (2026-07-08):** append the Gate-2-fold delta + push (DONE, `efdb84d` on remote), then **do NOT fire R2 from this shell** — log the arming state and hand off. **The fresh autonomous session fires R2 as its first chain act.**

**R2 (Tier-1 auto-re-fire) — ARMED, ALL 5 CRITERIA GREEN:**
- (a) G3 convergence guard landed + tested — ✅ (gamora, `03076c0`, 312 tests, byte-neutral; KR-verified)
- (b) measure-then-filter landed + 0/18-pass round-trip smoke green — ✅ (star-lord, `061176c`, 32/32; KR-verified `:674`<`:901`)
- (c) R1 dispositioned green — ✅ branch-(a) [inherited-uncalibrated, NOT the ruled difficulty]; gandalf R1-read `1cb2f62` ratifies R2 proceeds ("before-side of the diff")
- (d) kill-verify — ✅ no driver/emission PID alive as of this session-close (**the next shell MUST re-run kill-verify at its own fire-time** — this is a point-in-time check, not a durable one)
- (e) jack-ryan Gate-2 green — ✅ PASS/PASS, `3f525c5`, no BLOCK, no conditions

**FIRE SPEC for the next shell (R2 first chain act — the exact intended invocation):**
- Fire via a **star-lord sub-agent** (running `w3_emission_driver.py` is star-lord's export/driver seam; coordinated sub-agent firing is KR's seam).
- Params: `dry_run_flavor=True` (**$0 — hard requirement**; HALT-LOUD if the path would spend LLM), seed `56000000`, `n_samples_per_cell=1`, bounded by the G3 guard.
- **Re-run kill-verify at fire-time** (`ps aux | grep w3_emission_driver`) before firing — NEVER two same-seed emissions.
- measure-then-filter yields the §8-A1 band artifact at `output/leg3_pilot_section8a1_band_measurement.json` **regardless of the gate outcome** — this is the CURRENT-state "before-side" snapshot of the recalibration diff (gandalf §5.1). Expect ~0/18 gate pass (floor-saturated instrument); the TP3 HALT-LOUD at `:901` firing on empty survivors is CORRECT, and the artifact at `:674` persists BEFORE it.
- On completion: verify the artifact contents (read the file, don't narrate), push the band artifact (R6), report bands + gate outcome, append completion record to `dispatches/2026-07-08-gamora-starlord-spatial-floor-diagnosis.md`.

**AFTER R2 bands land — the sequenced continuation (gandalf §5, do NOT skip ahead):**
1. gamora $0 termination-split of the 323 floor events (death vs timeout, per scenario) — weights Lever 1 (HP) vs Lever 2 (engagement) empirically.
2. **Matt rules the §6 fork** (the R1 touchpoint, design-finding form): (1) HP-difficulty governance A/B/C [gandalf lean **A** un-stack legacy ×1.5 from endgame path]; (2) authorize serial-engagement design pass for open_arena+magic_pack [gandalf lean **YES**]; (3) schedule steps 2-4 as pre-R4 work on Leg-C critical path [gandalf lean **YES**]. Ref `gandalf/notes/2026-07-08-spatial-difficulty-levers-design-read.md`.
3. gamora executes ruled levers + $0 gauntlet re-run → before/after band diff → §4 gradient check (acceptance = "WR surface regains a gradient: mass in (0.05,0.95), differentials persist as spread not rails" — NOT "N/18 pass").
4. Lever-4 certification-criterion ruling if structural fails persist on a working gradient (with data).
5. **R4 / Leg-C hold-clears** against a coherent difficulty state. R5 band-sheet VALUES = the remaining designed Matt touchpoint.

**Matt touchpoints outstanding:** (1) the §6 spatial-difficulty fork (R1, now live — surfaced above; adjudicate after R2 bands + gamora's termination-split); (2) R5 band-sheet VALUES (later, post-Leg-C).

**ONE-LIVE-KR-SHELL discipline (per the pre-ratified execution protocol):** this shell is CLOSING and holds NOTHING in flight. R2 has NOT fired. The fresh autonomous session derives state from THIS file + the dispatch completion records, re-runs kill-verify, and fires R2 as its first act. No dispatch was double-fired; no run is in flight.

---

## ⭐ MATT RULING (2026-07-08) — §6 fork RULED **A / YES / YES**; R1 touchpoint CONSUMED; R3a recalibration work unit AUTHORIZED

**Matt ruled the §6 fork (Pattern-B session with gandalf, 2026-07-08 — verbatim "I agree with the 1-2 asks (A/yes/yes)").** Ref: `gandalf/notes/2026-07-08-spatial-difficulty-levers-design-read.md` §6. This consumes the R1 Matt touchpoint. **The SESSION-CLOSE block's "AFTER R2" step 2 ("Matt rules the §6 fork") is PRE-RULED — the fresh shell does NOT stop there.**

**The three rulings:**

1. **Ask 1 = OPTION A (un-stack).** The endgame-BC gauntlet path **stops applying `MOB_HP_DIFFICULTY_MULTIPLIER`**. The constant itself stays 1.5, untouched, for the legacy convergence instrument it was ruled for (2026-05-19). The parked Matt-scheduling-pending recalibration workstream (decisions-log 4240 + 5223) **resolves as SCOPE-RETIREMENT — no constant moves.** Single application-site change (`spatial_engine.py:3441` region); gamora seam; math-note-first; Gate-2.
2. **Ask 2 = YES (serial-engagement design pass).** Pack-local activation for open_arena + magic_pack so open rooms engage in proximity waves (~3-4 bites), restoring both the rooms' stated certification intent ("repositioning cost") and genre open-field grammar. gamora maths the activation radii. **The termination-split (death vs timeout) WEIGHTS the lever magnitudes; it is NOT a go/no-go gate — both levers are authorized regardless of the split's outcome.**
3. **Ask 3 = YES (scheduling).** The recalibration work unit is **R3a**, the pre-R4 unit on Leg-C's critical path.

**R3a — the authorized work unit (fresh shell sequences via gamora dispatch(es), KR fires per seam discipline):**

1. R2 bands land (before-side snapshot) →
2. gamora **$0 termination-split** of the 323 floor events from the v3 log (death vs timeout, per scenario) →
3. gamora executes **Option-A un-stack** + **serial-engagement pass** (math-note-first; Gate-2 each; gamora determines MIGRATION need) →
4. **$0 gauntlet re-run** → before/after band diff →
5. **§4 gradient acceptance check** — the anti-Goodhart gate: "WR surface regains a gradient: mass in (0.05, 0.95); differentials persist as spread, not rails." **NOT "N/18 pass."** Rider-4 stands: no content re-tuning; kits still floored on a calibrated gradient = TRUE content findings — REPORT them, do not fix them.
6. If structural certification fails persist on a working gradient → **conditional Lever-4 Matt touchpoint** (certification-criterion ruling, with data). Otherwise →
7. **R4 hold-clears** → Leg-C at ruled arc numbers → batch-2 closes → R5 band-sheet VALUES (Matt).

**Capture obligation:** KR drafts the decisions-log entry for this ruling during chain execution (scope-retirement of the parked multiplier workstream + serial-engagement authorization; cites gandalf's design read + gamora's design-finding note; jack-ryan reviews per governance).

**Matt touchpoints outstanding: R5 VALUES + conditional Lever-4 only.**

**Signed:** gandalf (ELICITOR — fork resolved upstream, queue stays drained), 2026-07-08.

---

## ⭐ KR DELTA (2026-07-08) — R3a step 3 CODE COMPLETE (gamora, KR-spot-verified); firing jack-ryan Gate-2

**gamora R3a-step-3 DONE** (tag `gamora/v-r3a-step3-unstack-serial-engagement-1`, engine `e649659` pushed w/ tag; Gate-2 submission collab `5ded435`; completion record collab `6e78cad`). 4 math-notes (Disc #1), smokes PASS×3, **77+87 regression tests GREEN**, no HALT, no design ambiguity, no boundary crossing.

- **D1 un-stack:** endgame-BC swarm eff-HP **39,750→26,500 (÷1.5, −33%)** on open_arena+chokepoint; magic_pack unchanged (never in `MOB_HP_DIFFICULTY_SCENARIOS` — the very reason the log's `1.5→1.25` was structurally incapable). Mechanism = caller-flag `apply_mob_hp_difficulty_multiplier: bool = True` (existing callers byte-identical) with only `_w4g_run_fight_batch` (`t4_sim_cycling.py:1236`) passing `False`; gate at `spatial_engine.py:3457` = flag AND scenario-membership. **`arena.py:49 = 1.5` UNTOUCHED — scope-retirement, not a constant move (Goodhart guard intact).** Legacy convergence path verified unaffected.
- **D2 serial-engagement:** activation radii **open_arena 12m** (~4 peak concurrent, ~3-4 bites) / **magic_pack 9m** (14m-deep room, ~3 bites), derived from spawn-table geometry (framing-audit Disc #23). Shared `LEASH_DISTANCE_OVERRIDE_M_SWARM=35.0` **NOT re-based** (shared across 3 incompatible-geometry rooms incl. out-of-scope chokepoint; activation gate subsumes the concern in-scope) — chokepoint-scoped re-base **REPORTED, not fixed** (rider-4 honest finding).
- **D3 winner-tally:** `{player,monster,timeout}` 3 ints/(class,scenario) row from `FightSummary.termination_reason`, surfaced in `GauntletEncounterResult.to_dict`. **WITHIN-SEAM, NO MIGRATION** (in-JSON aggregate — confirms gandalf §5.2-AMEND lean; no star-lord coordination needed).
- **Resource projection (Disc #1.1):** step-4 re-run **~25-35 min, <5MB peak** (same class as R2; D1-down/D2-up partly offset; 120s cap unchanged).

**KR spot-verified (trust-but-verify):** `arena.py:49`=1.5 untouched ✅; caller-flag default True, only endgame path passes False ✅; tag present ✅; kill-verify clean ✅. Load-bearing Goodhart-guard + scoping claims hold at spot-check.

**NOW FIRING jack-ryan Gate-2** on the coordinated submission (`qa/pending/2026-07-08-gamora-r3a-step3-unstack-serial-winner-gate2-submission.md`) — balance/difficulty-affecting engine change; the ratified plan's "Gate-2 each" gate. **On Gate-2 GREEN → R3a step 4: KR fires the $0 gauntlet re-run** (seed 56M, kill-verify first) → after-side §8-A1 bands + native termination split → **§4 anti-Goodhart gradient acceptance check** (mass in 0.05-0.95, differentials as spread not rails — NOT "N/18 pass"). If Gate-2 BLOCKs → chain STOPS, route to Matt.

**Matt touchpoints outstanding: R5 VALUES + conditional Lever-4 only.**

---

## ⭐ KR DELTA (2026-07-08) — fresh autonomous shell: R2 FIRED (detached, in flight); one prior attempt failed on sub-agent lifecycle, not engine

**Fresh shell state-derivation (one-live-KR-shell discipline):** derived from THIS file + dispatch completion records. Diagnosis dispatch = COMPLETE (both halves, KR-verified). jack-ryan Gate-2 = PASS/PASS. §6 fork = Matt-RULED A/YES/YES (R1 CONSUMED). R2 = ARMED 5/5, NOT fired by prior shell (Matt-directed handoff). **This shell's first chain act = fire R2.** Kill-verify at derivation: clean.

**R2 attempt #1 — FAILED (sub-agent lifecycle, NOT engine).** First star-lord sub-agent launched the driver as a normal background job + returned before completion; the process was reaped when the sub-agent session ended (~01:27), killed mid-gauntlet on candidate `melee_high_flat_dex` (~6 min in, `/tmp/leg3_r2_run.log` ends 01:26:33, no completion marker, no HALT-LOUD, no traceback). **G3 guard did NOT fire; fights ran clean; $0 held — engine is fine.** The on-disk §8-A1 artifact was STALE (seed 55M / 5-cand smoke, not our seed 56M / 18-cand). No fresh bands produced. Lesson: a ~4.3hr detached run must NOT depend on sub-agent lifetime.

**R2 attempt #2 — LAUNCHED DETACHED, IN FLIGHT.** star-lord relaunched via `subprocess.Popen(start_new_session=True)` (macOS has no `setsid`; this is the native equivalent) → **PID 12819, PPID=1, own session — survives session exit.** Params: `--dry-run-flavor --seed 56000000 --n-samples 1`, 18 endgame-BC candidates, G3-guard-bounded, **$0**. Clean start verified (seed 56000000 · 18 candidates enumerated · into STEP 3/4 gauntlet · no traceback). Driver's own budget projection (Disc #1.1): **~45,360 fights | ~4.3 hrs wall-clock | <5MB peak.** KR-verified exactly ONE driver alive (no same-seed duplicate — rider-7 satisfied). Log: `/tmp/leg3_r2_run2.log`.

**Wait posture:** KR (persistent shell) owns the wait via a completion-triggered notifier (bg poll on PID 12819 exit → dumps log tail + artifact seed/cand/pass check). No context-burning poll. measure-then-filter guarantees the §8-A1 artifact at `output/leg3_pilot_section8a1_band_measurement.json` lands regardless of gate (expect ~0/18 pass — floor-saturated instrument; this is the before-side snapshot, gandalf §5.1).

**On R2 completion, this shell auto-continues (NO Matt ask — §6 pre-ruled) into R3a per line 827–835:** (1) verify fresh artifact (seed 56M/18-cand) + push (R6) + append dispatch completion record → (2) gamora $0 termination-split of the 323 v3 floor events → (3) gamora Option-A un-stack + serial-engagement pass (math-note-first, Gate-2 each) → (4) $0 gauntlet re-run → before/after diff → (5) §4 gradient acceptance check → conditional Lever-4 / R4 hold-clear. **KR capture obligation (line 837): draft the decisions-log entry for the §6 A/YES/YES ruling during chain execution.**

**Matt touchpoints outstanding: R5 VALUES + conditional Lever-4 only** (unchanged). No dispatch double-fired; one run (PID 12819) in flight; this shell is the sole live KR shell.

---

## ⭐ KR DELTA (2026-07-08) — R2 COMPLETE: §8-A1 before-side bands landed (0/18, floor-saturated); measure-then-filter PROVEN live; R3a step 2 (gamora termination-split) firing

**R2 ran to completion** (detached PID 12819, 25,530 fights, **1507.6s** — the 4.3hr projection was conservative; ~25 min actual). Result EXACTLY as the measure-then-filter design intended:
- `GAUNTLET_SIM_PASS=False` · `round_trip_smoke_pass=True` · WR-bracket **0 passing / 18 failing**.
- **§8-A1 band report persisted at STEP 4 (log line 22) BEFORE the TP3 HALT-LOUD (line 26)** — the decoupling fix proven in-flight. TP3 halt on empty survivors is CORRECT (emission gate); the before-side snapshot is on disk regardless.
- G3 convergence guard **did NOT fire** (calibration completed clean, no wedge). $0 (dry_run_flavor). Exactly one driver alive throughout (rider-7 satisfied).

**Fresh artifact (KR-read, not narrated):** `engine:src/reincarnated/output/leg3_pilot_section8a1_band_measurement.json` — seed 56000000 · 18 candidates · gauntlet 1507.7s · gate 0/18 `emission_certified=false` · bands **none=17 (all fail) / light=1 (fail) / heavy=0 NOT-EXERCISED** · registry-honesty riders all present (proxy-heavy NOT-EXERCISED, C2 light-only, ≤7 UNPROVEN, catalog 17/1/0) · all 18 per-candidate records truthful. **This is the before-side snapshot for R3a's before/after gradient diff (gandalf §5.1).**

**star-lord close-out (Pattern-A, KR-orchestrated):** engine artifact + AGENT_STATE committed+pushed (`75637f5`, `ae46047`); dispatch R2-fire completion record appended+pushed (`3a4c082`). Kill-verify clean. (star-lord's sign-off said "R3a gated on Matt run-auth" — that reflects the ORIGINAL dispatch's struck re-fire clause, which star-lord sees but the full chain does not carry: **R2's re-fire clause was pre-satisfied by the ratified table AND §6 is already Matt-ruled A/YES/YES — R3a is authorized, no fresh Matt disposition.** KR carries the chain context; star-lord's narrow close-out was correct.)

**NOW FIRING R3a step 2 (gandalf §5.2 / run-state line 830): gamora $0 termination-reason split** of the ~323 floor events (death vs timeout-with-mobs-alive, per scenario). This EMPIRICALLY WEIGHTS Lever 1 (HP budget — timeout-dominant floors) vs Lever 2 (engagement model — death-dominant floors) before either moves. It is NOT a go/no-go gate (both levers authorized regardless — ruling line 824); it sizes the magnitudes. Pattern-A ($0, minutes). Then R3a step 3: gamora Option-A un-stack + serial-engagement pass (math-note-first, Gate-2 each).

**Matt touchpoints outstanding: R5 VALUES + conditional Lever-4 only.** Sole live KR shell; no run in flight (PID 12819 exited clean).

---

## ⭐ KR DELTA (2026-07-08) — R3a step 2 result: termination-split UN-MEASURABLE (fail-loud telemetry gap); routing sequencing implication to gandalf

**gamora R3a-step-2 = honest FAIL-LOUD (commit `18dbba5`, pushed) — the split cannot be produced from current data:**
- The per-fight termination reason IS a first-class engine field: `SpatialFightResult.winner ∈ {player, monster, timeout}` (`spatial_telemetry.py:233`) → `monster`=death→Lever 2, `timeout`=timeout→Lever 1. Clean mapping exists.
- BUT the R2 run (`star_lord_integration_mode: stub_write`) used the **Null stub writer**, which only DEBUG-logs winner; driver ran at INFO → `grep winner=` on the 35MB log = 0 hits. No DB rows either (only stale VS2a 2026-05-20 `class_00xx` data; zero 56M-seed / zero endgame_bc). Aggregate results JSON collapses to `tier_2_survival_rate` — not decomposable post-hoc.
- gamora **did NOT fabricate** a split from proxies (Discipline honesty). One labeled proxy only: 30/252 open_arena floors have partial clears (`tier_2_kpm>0`); all 180 magic_pack floors 0-KPM (directionally alpha-strike but 0-KPM is the ambiguous death/timeout case — non-weighting). gandalf §1 mechanism read (HP not the discriminant → Lever 2 primary) stands on its own; this note adds no new empirical weight.
- gamora recommendation: a **winner-tally recording flip** (winner already computed + passed to `write_fight_result` — no fight-loop code) so the step-4 $0 re-run yields the split natively. Schema/export field → MIGRATION + star-lord; in-JSON aggregate gamora-side → within-seam; gamora rules that at step 3/4.

**SEQUENCING IMPLICATION (why this goes to gandalf, not silently onward — avoiding drift on gandalf's authored §5 plan):** gandalf §5.2 wanted the split "before either lever moves" AND assumed it came free from the existing v3 log — it does NOT (no winner recording). Compounding: Option A makes **Lever 1 a binary scope-retirement (no magnitude to weight)**, so the split's original weight-Lever-1-vs-2 purpose is largely dissolved; the only magnitude is Lever 2's activation radii, which gamora maths from room geometry (bite size), not from the death/timeout ratio. So the before-side split is now **confirmatory/diagnostic, not load-bearing weighting input.** **Question routed to gandalf (design steward, §5 author):** does the before-side termination split warrant a dedicated instrumented $0 re-run BEFORE step 3, or do we fold the recording flip into step 3 (closing the telemetry gap) and read the split natively from the step-4 after-side re-run + proceed to lever execution now? Both levers authorized regardless (non-gating, ruling line 824). Firing gandalf for the ruling.

**Matt touchpoints outstanding: R5 VALUES + conditional Lever-4 only** (unchanged — this is an in-scope R3a sequencing detail, gandalf's seam, NOT a Matt touchpoint).

---

## ⭐ KR DELTA (2026-07-08) — gandalf ruled sequencing (a); R3a step-3 dispatch AUTHORED + firing gamora

**gandalf sequencing ruling = (a)** (`1906598`, §5.2-AMEND appended to the design read, pushed): fold the winner-tally recording flip INTO R3a step 3; **NO dedicated before-side split re-run.** Reason: the before-side termination split is now confirmatory not load-bearing — §4 acceptance judges the WR SURFACE (mass 0.05-0.95, differentials as spread not rails), NOT termination reasons; §1's magic_pack smoking gun already over-determines HP-is-not-the-discriminant; a $0/~25-min run to re-confirm a ruled mechanism is exactly the rider-4 "bend the schedule to feed the instrument" move. We keep the load-bearing before-side BANDS (already in hand from R2) and gain the after-side split natively on the step-4 re-run at zero marginal run cost. **Recording flip = within-seam gamora** (in-JSON aggregate, no schema field crosses star-lord; MIGRATION only if it lands as a persisted DB column — gamora's final call).

**R3a step-3 dispatch AUTHORED:** `dispatches/2026-07-08-gamora-r3a-step3-unstack-serial-engagement.md`. Three deliverables, math-note-first each (Disc #1), coordinated Gate-2:
- **D1 — Option-A un-stack:** endgame-BC gauntlet path stops applying `MOB_HP_DIFFICULTY_MULTIPLIER`; `arena.py:49` stays `1.5` untouched for the legacy instrument (scope-retirement, NOT a constant move — Goodhart guard intact). Budget effect ~33% drop (gandalf §3).
- **D2 — Lever-2 serial-engagement:** pack-local activation (~3-4 waves) for open_arena + magic_pack; gamora maths the activation radii from room geometry; also addresses the inherited-uncalibrated `LEASH_DISTANCE_OVERRIDE_M_SWARM=35.0` (never re-based to the 36×36 geometry). magic_pack does NOT join `MOB_HP_DIFFICULTY_SCENARIOS` (wrong direction).
- **D3 — winner-tally recording flip:** in-JSON per-(class,scenario) `winner` tally so step-4 re-run yields the split natively; within-seam (gamora's boundary call; MIGRATION+star-lord only on the DB-column path).

Acceptance = gandalf §4 anti-Goodhart gradient gate (validated at step 4, NOT this dispatch). Out-of-scope: no constant move, no content re-tuning, no Lever-4 change, no step-4 re-run in this dispatch. Principle-6 gate assessed at authoring (D1/D2 no boundary; D3 conditional). **Gate-1 not separately fired: the design gate already happened upstream (gandalf design-read + Matt A/YES/YES ruling); the ratified plan specifies Gate-2 for step 3.** Firing gamora on the dispatch now (Pattern-B, KR-fired per chain execution protocol).

**Matt touchpoints outstanding: R5 VALUES + conditional Lever-4 only.**

---

## ⭐ KR DELTA (2026-07-08) — R3a step-3 Gate-2 PASS (all 3 deliverables); firing R3a step-4 $0 after-side re-run

**jack-ryan Gate-2 = PASS on all three deliverables** (finding `qa/findings/2026-07-08-gamora-r3a-step3-unstack-serial-winner.md`, submission cleared, commit `30b410e` pushed). No BLOCKs, no conditions. Verified independently (trust-but-verify, not narrated-trust):
- **Smokes re-run PASS×3** — reproduced un-stack factor (39,750→26,500 = ÷1.5), serial-engagement wave counts (open 4/40, magic 10/24), winner-tally sums.
- **164 regression tests green** (77+87).
- **Goodhart guard confirmed** — `arena.py:49 = 1.5` genuinely untouched (last change `24cdc7e`, 2026-05-19 R2 recalibration; not this commit). Constant did NOT move; only the endgame gauntlet call-path stopped applying it. Rider-5 intact.
- **Scoping confirmed** — only `t4_sim_cycling.py:1236` passes `apply_mob_hp_difficulty_multiplier=False`; every other caller byte-identical (default True); legacy convergence instrument keeps ×1.5. Un-stack is surgical to endgame-BC.
- **Rider-4 confirmed** — 10-file commit, zero kit/content/bar/band touches (no bending content to green the instrument).
- **D3 within-seam confirmed** — in-JSON aggregate only, no DB column, no star-lord telemetry boundary crossed → no MIGRATION needed (gamora's boundary call correct). ADR-004 / Principle-6 satisfied.

**NOW FIRING R3a step 4 (the after-side re-run):** $0 gauntlet re-run, seed 56000000, n=1, `dry_run_flavor` (no LLM — R6 $0 guard), kill-verify clean (no prior driver PID; rider-7 satisfied — never two same-seed emissions concurrent). The endgame-BC gauntlet now carries un-stack + serial-engagement + winner-tally. Expected artifacts: after-side §8-A1 bands + native termination split (D3 flip). star-lord sub-agent launches DETACHED (`subprocess.Popen(start_new_session=True)`) so the run survives the sub-agent lifecycle (the R2 attempt-1 reaping lesson). Projected ~25-35 min / <5 MB (gamora resource note).

**On completion → §4 anti-Goodhart gradient acceptance check:** the gate is "WR surface regains a gradient — mass in (0.05, 0.95), differentials persist as spread not rails" — **NOT "N/18 pass."** If the surface gradients AND structural fails persist → conditional Lever-4 certification-criterion ruling (a Matt touchpoint, WITH data). If it still rails → diagnose before any further lever move (no schedule-bending).

**Matt touchpoints outstanding: R5 VALUES + conditional Lever-4 only.** Sole live KR shell; kill-verify clean; firing step-4 now.

---

## ⭐ KR DELTA (2026-07-08) — R3a step-4 after-side re-run COMPLETE: §4 gradient acceptance FAILS (still rails); two coherence anomalies → gamora diagnosis before any Matt report

**Step-4 $0 re-run complete** (PID 16764, seed 56000000, `dry_run_flavor`, 879.8s / <1MB — kill-verify clean pre-launch, detached survived, $0 confirmed). Same TP3 HALT-LOUD on empty survivors (0/18 emit — CORRECT gate behavior; not the §4 criterion). Artifacts fresh: `leg3_pilot_section8a1_band_measurement.json` (seed 56M, mtime 02:53) + `cycle-13-gauntlet-sim-results-20260708_065352.json` carrying `tier_2_winner_tally` (D3 flip landed).

**§4 ANTI-GOODHART GRADIENT ACCEPTANCE = FAIL (robust under both surface readings):**
- **Final per-cell WR surface (authoritative, post-calibration `tier_2_survival_rate` over 1197 cells): mid-fraction = 0.001 — ONE cell in (0.05, 0.95).** Still a step function. floor=714 / MID=1 / ceil=482.
- Per-scenario final cells: `chokepoint_corridor` 189 floor / 0 mid / 0 ceil · `open_arena` 252 / 0 / 0 floor · `magic_pack` 153 / 0 / 36 · `boss_with_adds` 117 / 0 / 72 · `elite_pack` 0 / 0 / 315 (all ceiling) · `mini_boss` 3 / 1 / 59.
- Calibration-warning surface (secondary): floor 323→127, ceiling 278→414. Levers REDISTRIBUTED cells across rails (some floor→ceil) but produced NO mid-band mass.
- **Verdict holds under either reading: no gradient. The two authorized R3a levers (un-stack + serial-engagement) are SPENT and §4 is not met.**

**TWO COHERENCE ANOMALIES (routed to gamora — sim seam — NOT resolved by KR inference):**
1. **winner-tally ⟂ survival_rate:** `magic_pack` = WR-floor 153/189 yet `tier_2_winner_tally` player=1.00 / monster=0 / timeout=0. `monster=0` across ALL scenarios. A floored survival surface with zero monster-wins is contradictory. Bears on (a) is the surface trustworthy for §4, (b) does D3 have a latent defect (Gate-2 verified tally SUMS on a smoke, NOT surface-coherence on the real run).
2. **calibration-warning ⟂ final-cell surface:** warnings logged `open_arena` ceiling-heavy (225); final cells show `open_arena` 252/252 floor. Opposite. Likely a `scenario_shell_id` mapping vs calibration-loop-scenario distinction — but gamora confirms.

**BRANCH TAKEN:** per my stated step-4 branch — "still rails → diagnose before any further lever moves; no schedule-bending." Firing gamora Pattern-A ($0 read-only) on the two anomalies + which surface is the authoritative §4 input. The authorized R3a lever budget is exhausted, so the NEXT move (Option-C per-scenario difficulty spec / re-open lever magnitudes / Lever-4 criterion) is a genuine design+authority fork the ratified table did NOT pre-rule — that goes to Matt/gandalf as a consolidated picture AFTER gamora clears the surface-trust question. This is NOT re-asking run-auth (pre-satisfied); it is surfacing an un-pre-ruled fork.

**Matt touchpoints outstanding: R5 VALUES + the now-LIVE next-lever fork (levers spent, §4 unmet).** Conditional Lever-4 as originally framed ("gradient returns + structural fails persist") did NOT trigger — gradient did not return. Sole live KR shell; no run in flight (16764 exited).

---

## ⭐ KR DELTA (2026-07-08) — gamora forensics CLEAR the surface-trust question (§4 FAIL confirmed, not confounded); firing gandalf for the design verdict + next-move read

**gamora $0 read-only forensics** (note `agentic_orchestration/gamora/notes/2026-07-08-r3a-step4-coherence-forensics.md`, commit `b87d394`) resolved BOTH anomalies:
- **Anomaly 1 = SEMANTIC, not a D3 defect.** Over all 603 tally-bearing cells `survival_rate ≈ winner_tally.player/n` to <1e-6 (0 mismatches). The contradiction is an aggregation artifact: `tier_2_survival_rate` dataclass-defaults to **0.0** (`gauntlet_sim.py:609`) while `tier_2_winner_tally` defaults to **None** (`:616`); on a tier-1 CLEAR-shell reject the loop `continue`s (`t4_sim_cycling.py:1278-1288`) without running tier-2, so **594 of 1197 cells never ran tier-2** and read as FLOOR by 0.0-default. D3 flip is clean; jack-ryan Gate-2 stands. **Caveat for any writeup: do NOT read the winner-tally aggregates as a death/timeout split — they only cover the ceiling cells that reached tier-2.**
- **Anomaly 2 = different namespaces.** `[R2 calibration]` WARNINGs = raw `spatial_engine` instrument-health probe (separate loop); the final gate surface is the tier-1/tier-2 gate. open_arena's apparent ceiling→floor inversion is the unrun 0.0-default, not a math flip.
- **CORRECTED AUTHORITATIVE SURFACE = the 603 genuinely-simulated cells: 482 ceiling / 120 floor / 1 mid = 0.0017 mid-fraction.** **§4 read is TRUE and not confounded in the rescuing direction. Still a step function. §4 FAILS.**

**STRUCTURAL BYPRODUCT (new input the §5 lever taxonomy didn't have):** open_arena (252) + chokepoint_corridor (189) are **100% unrun at tier-2 — they reject at tier-1.** Serial-engagement is a tier-2 engagement fix; it could not have moved scenarios dying at tier-1. The next-move question is therefore NOT purely tier-2 engagement geometry — it implicates the tier-1 gate structure.

**FIRING gandalf (Pattern-A, $0 read-only design verdict):** §4 is gandalf's authored criterion; the next-lever call is his §5 taxonomy. Routing (a) the official §4 verdict on the corrected 603-cell surface, (b) a next-move design read given levers-spent + §4-unmet + the tier-1-reject finding. Output → a Matt-ready design-informed fork, NOT a raw options menu. Then I consolidate step-4 + gamora forensics + gandalf verdict for Matt.

**Matt touchpoints outstanding: R5 VALUES + the now-LIVE next-lever fork.** Sole live KR shell; no run in flight.

---

## ⭐ KR DELTA (2026-07-08) — gandalf §4 verdict = FAIL (uncontested); tier-1 gate identified as 4th inherited-uncalibrated constant; firing gamora $0 tier-1-gate read to sharpen Matt's fork

**gandalf design verdict** (note `agentic_orchestration/gandalf/notes/2026-07-08-r3a-step4-s4-verdict-and-next-move.md`, commit `988663e`):
1. **§4 = uncontested FAIL.** 603-cell authoritative surface 482 ceil / 120 floor / 1 mid = 0.0017; correction moved it the non-rescuing direction. Still a step function.
2. **Levers right-but-INSUFFICIENT.** §1 (HP-not-discriminant) over-determined → un-stack predictably moved nothing. Serial-engagement (a TIER-2 fix) was aimed at open_arena+chokepoint, which REJECT AT TIER-1 (`_route_tier_1` band_override → tier-1 KPM outside calibrated band → TIER_1_REJECT → continue, tier-2 never simulated). A tier-2 lever cannot move a tier-1-death scenario. Root: **the tier-1 KPM band is a FOURTH inherited-uncalibrated gate** (calibrated pre the 2026-07-07 re-population) — Discipline #13 drift one layer down, same shape as the three §1 constants. The band report masked it by collapsing "died in arena" and "never entered arena" into one WR=0.000 floor.
3. **Conditional Lever-4 is MOOT** — its trigger was "gradient returns + structural fails persist"; gradient did NOT return. Do not spend a Matt touchpoint ruling a criterion that judges a still-broken surface.
4. **Recommended ONE next thing ($0):** read-only tier-1-gate structural investigation — is the tier-1 KPM band for open_arena+chokepoint a cheap re-band (one field, 4th inherited constant) or genuine kit non-viability (→ Option-C)? Converts Matt's fork from raw menu to a sharp **re-band vs Option-C** binary. re-opening lever magnitudes = rejected by mechanism (no dial reaches a tier-1-rejected room).

**FIRING gamora (Pattern-A, $0 read-only) on the tier-1-gate investigation** — scoped to the ~441 tier-1-rejected open_arena+chokepoint cells. This is the direct continuation of the already-taken "diagnose before any further lever move" branch: no lever moves, no spend, no scope-amendment → in-scope autonomous (firing a $0 read is not a Matt touchpoint). AFTER this read I STOP and consolidate the full picture (step-4 §4-FAIL + gamora forensics + gandalf verdict + tier-1 read) for Matt as a decision-ready **re-band vs Option-C** fork — because THAT choice is a lever decision that exceeds autonomous scope and is Matt's.

**Matt touchpoints outstanding: R5 VALUES + the next-lever fork (re-band vs Option-C, to be sharpened by the tier-1 read).** Sole live KR shell; no run in flight.

---

## ⭐ KR DELTA (2026-07-08) — tier-1 gate diagnosis CLOSED: (a) mis-calibrated band, cheap re-band [NOT Option-C]; DIAGNOSIS CHAIN COMPLETE → chain HALTED at Matt fork (new-lever authorization)

**gamora $0 tier-1-gate read** (note `agentic_orchestration/gamora/notes/2026-07-08-r3a-tier1-gate-band-vs-viability-diagnosis.md`, commit `b469351`) = **BINARY RESOLVED to (a): mis-calibrated tier-1 KPM band, cheap re-band, both scenarios, NOT kit non-viability, NOT Option-C.**
- **Polarity flip:** the rejected open_arena+chokepoint cells reject by being ~2× ABOVE the band CEILING (clear too FAST), not below the floor. open_arena band ceiling 15.53 vs observed median 31.9 (2.05× hi), 0/252 in-band; chokepoint ceiling 15.88 vs median 35.2 (2.22× hi), 0/189 in-band. Non-viability would read KPM-below-floor; this is the inverse. Their "WR=0.000 floor" = "never entered the arena," not "died in it."
- **Provenance:** both band tuples last written 2026-06-16 (`92c040f`, Stage-2d); room pop changed underneath (F2 re-pop `59dc832` 2026-07-07, un-stack `e649659` 2026-07-08), no re-base. Fourth inherited-uncalibrated gate, exact Discipline #13 shape one layer below the §1 constants.
- **Re-band signature confirmed:** a plain p10/p90 re-fit (same estimator that made the current band) in-bands 81% of cells on both scenarios — distribution shifted up as one coherent ~2× mode, no can't-clear fracture. Fields: two tuples at `gauntlet_sim.py:434-435`; `_route_tier_1` predicate untouched — same one-constant class as the un-stack.

**DIAGNOSIS CHAIN COMPLETE (all $0, no levers moved):** step-4 §4 FAIL → gamora surface-trust forensics (surface real) → gandalf §4 verdict + design read (levers right-but-insufficient, tier-1 gate is the bottleneck) → gamora tier-1 binary (re-band, not Option-C). The "diagnose before any further lever move" branch is fully discharged.

**CHAIN HALTED at Matt fork — NEW-LEVER AUTHORIZATION (not re-asking run-auth; a genuine scope point):** the tier-1 band re-fit is a THIRD R3a-class lever, NOT part of the §6 A/YES/YES ruling (which named exactly two: un-stack + serial-engagement). Authorizing a new constant move exceeds the ratified R3a budget and is Matt's call per the §6-fork-is-Matt's precedent + scope-amendment rule. The chain cannot proceed to R4/R5 until the surface can be measured (R4 Leg-C + R5 band-sheet are downstream of batch-2 closing on a gradiented surface). **KR recommendation to Matt: authorize the re-band as a one-constant R3a follow-on (math-note-first + Gate-2, identical discipline to the un-stack) → re-run step-4 → judge §4 on a surface where all 6 scenarios actually run tier-2.** Honesty caveat surfaced to Matt: even the 603 already-MEASURED cells are still railed (elite_pack all-ceiling, magic_pack partial-floor, etc.), so the re-band unblocks MEASUREMENT of the two worst scenarios but does not guarantee the whole surface gradients — there may be further work after. Conditional Lever-4 is MOOT (gandalf).

**Matt touchpoints outstanding: (NEW, LIVE) tier-1 re-band authorization + R5 VALUES.** Sole live KR shell; no run in flight; diagnosis chain closed.

---

## ⭐ KR DELTA (2026-07-08) — R3a step-5 tier-1 band re-derivation COMPLETE (gamora); firing jack-ryan Gate-2

**Matt AUTHORIZED the re-band as R3a step-5** (verbatim: scoped to the two stale tuples `gauntlet_sim.py:434-435`; riders per gandalf — density-anchored re-derivation with percentile cross-check math-note-first, §4 unchanged, Gate-2, cohort-invariance preserved, residual-reject breakout in after-report; then re-run step-4 for the §4 verdict on the full surface). KR authored the dispatch (`2026-07-08-gamora-r3a-step5-tier1-band-rederive.md`, committed), fired gamora.

**gamora COMPLETE** (engine `649ff6a`, collab `750ada4`, tag `gamora/v-r3a-step5-tier1-band-rederive-1`, all pushed):
- **Band values (old→new):** open_arena (9.90, 15.53)→**(20.87, 53.33)** [45s,115s @ 40 mobs]; chokepoint (11.65, 15.88)→**(12.52, 60.00)** [24s,115s @ 24 mobs]. Model `KPM = mob_count×60/clear_s` (exact for all_mobs_killed / KILLS_ONLY full-clear). `_route_tier_1` byte-identical; other 4 shells byte-identical.
- **Density-anchor vs percentile — AGREE, with one finding surfaced (rider-4 held):** open_arena agrees cleanly (density ≈ percentile within ~1.5 KPM). chokepoint first-pass DISAGREED (naive model gave open_arena's fast-clear ceiling → 38% in-band); gamora surfaced it as a FINDING and **corrected the DENSITY MODEL** (24s funnel sweep grounded in the room's cone/line-AOE geometry, NOT the observed distribution) → 90% in-band. She corrected the model against the room's geometry, never the band against the kits. **← THE crux for Gate-2 to stress: is the corrected funnel model genuinely geometry-grounded, or a reverse-engineered justification to reach the percentile?**
- **Cohort-invariance PRESERVED** — single per-shell tuple replicated across all 4 cohort columns, no branching; per-cohort mean KPM agrees <0.16. Verified structurally + empirically (math note §4).
- **Residual-reject breakout — WITHIN-SEAM (no MIGRATION, no star-lord):** `tier_1_reject_breakout` top-level aggregate in results JSON (re-aggregation of already-serialized `tier_1_outcome`+`tier_1_kpm` vs band; D3 precedent). Simulated split admits ~375 of 441 previously-unrun cells into tier-2 (open 204 in/36 above/12 below; choke 171 in/18 above/0 below).
- **Smoke ALL PASS**; regression 50+27 green; **step-4 re-run projection ~25-30 min / <5MB / $0** (up from 879.8s — ~375 cells added to tier-2).

**FIRING jack-ryan Gate-2** (`qa/pending/2026-07-08-gamora-r3a-step5-tier1-band-rederive-gate2.md`). On PASS → KR fires the $0 step-4 RE-RUN (kill-verify first, seed 56M, dry_run_flavor, budget ~25-30 min) → §4 verdict on the FULL surface (all 6 scenarios running tier-2) → to Matt. Sole live KR shell; no run in flight.

**Matt touchpoints outstanding: R5 VALUES + the §4-verdict-on-full-surface report (next).**

---

## ⭐ KR DELTA (2026-07-08) — R3a step-5 Gate-2 PASS (no conditions); firing step-4 RE-RUN ($0, full surface)

**jack-ryan Gate-2 = PASS, no conditions, no BLOCK** (finding `qa/findings/2026-07-08-gamora-r3a-step5-tier1-band-rederive.md`, submission cleared, commit `82f71bb`). The crux (chokepoint density-model = geometry-grounded vs curve-fit-in-disguise) VERIFIED geometry-grounded on three independent tests:
- The room-structure difference the correction rests on is REAL in `arena.py`, predating the dispatch: open_arena `serial_activation_radius_m=12.0` (serial gating → slower clear) vs chokepoint `None` (funnel geometry, no serial gate). gamora's first-pass error (applying open_arena's serial 45s shape to a non-serial room) has a verifiable cause; the correction follows the room definition, not the target.
- The AOE-concentration term is the room's OWN documented cert intent (source comments at definition time).
- **Anti-curve-fit signature:** the corrected 60.0 ceiling sits ABOVE observed p90 (57.14) by ~2.9 KPM — a curve-fit lands ON the percentile; an independent geometry anchor with headroom lands PAST it. A band fitted to kits could not produce that.
- All else reproduced exactly: scope (predicate + 4 shells byte-identical, only 2 tuples), cohort-invariance preserved, within-seam breakout (no MIGRATION correct), percentiles/in-band/split, regression 77 green, §4 gate untouched. Three INFO notes (non-blocking): floors timeout-anchored not density-anchored; 24s choke ceiling is a coarse brisk-sweep estimate (revisit if choke rails at ceiling); breakout `else`-branch buckets completion-gate-fails into below_floor (doesn't affect open/choke).

**NOW FIRING R3a step-4 RE-RUN:** $0 gauntlet re-run, seed 56000000, n=1, `dry_run_flavor` (R6 $0 guard), kill-verify clean (rider-7 — no concurrent same-seed emission). Detached (`start_new_session=True`). Budget ~25-30 min / <5MB (gamora Disc #1.1 projection; up from 879.8s — ~375 previously-unrun cells now admitted to tier-2). **On completion: read `tier_1_reject_breakout` FIRST (proves the ~375 cells entered tier-2 — jack-ryan's instruction), THEN judge the §4 gradient on the FULL 6-scenario surface → verdict to Matt.**

**Matt touchpoints outstanding: R5 VALUES + the §4-verdict-on-full-surface report (imminent).** Sole live KR shell; firing re-run now.

---

## ⭐ KR DELTA (2026-07-08) — R3a step-4 RE-RUN COMPLETE: §4 FAILS but failure mode INVERTED (ceiling-saturation); re-band worked; selection lives at tier-1 → strategic fork to Matt

**Step-4 re-run complete** (PID 32539, seed 56M, `dry_run_flavor`, 1469.5s / <5MB — kill-verify clean, detached, $0). Fights 24,030→31,530 (~7,500 more = the ~375 admitted cells). Same TP3 HALT-LOUD on 0/18 emit (emission gate, not §4).

**BREAKOUT (read first, per jack-ryan) — re-band WORKED exactly as projected:** open_arena 0→**204 entered_tier2** (36 above/12 below), chokepoint 0→**171 entered** (18 above/0 below). breakout `entered_tier2` matched measured counts cell-for-cell across all 6 scenarios. The ~375 previously-unrun cells now run tier-2.

**§4 FULL-SURFACE VERDICT = FAIL, but failure mode INVERTED (ceiling-saturation, not floor).** Clean surface = `tier_1_outcome==PROVISIONAL_PASS` cells (genuinely ran tier-2; NOT `winner_tally present` — that filter was contaminated by tier-1-REJECT rows carrying placeholder `{0,0,timeout:20}` tallies on boss/mini_boss; KR caught + corrected before verdict):
- **769 entered tier-2: 765 ceiling / 4 MID / 0 floor. mid-fraction 0.0052, ceil-fraction 0.995.** Per-scenario: boss_with_adds 7/0/0/7ceil · chokepoint 171 all-ceil · elite_pack 315 all-ceil · magic_pack 36 all-ceil · mini_boss 36 (1 mid @0.90) · open_arena 204 (3 mid @0.85-0.95, 201 ceil).
- **The original "everything floors" was an ARTIFACT** — unrun tier-1-rejected cells defaulting to survival=0.0. With four inherited-uncalibrated gates cleared (HP un-stack, serial-engagement, tier-1 re-band ×open_arena+chokepoint), the TRUE tier-2 surface is CEILING-saturated: kits win everything they're measured on. A §4 gradient cannot exist on a layer where everyone wins.

**STRUCTURAL FINDING (new, load-bearing for the fork):** all real kit-vs-content SELECTION happens at TIER-1 (the KPM gate), NOT tier-2 (survival). tier-2 survival is a near-constant 1.0 for anyone who enters. boss_with_adds rejects 182/189 at tier-1 — **117 killed ZERO mobs** (`tier_1_kpm=0.0` = genuine content non-viability, can't fight the room), the 7 that enter faceroll. magic_pack rejects 153/189 (117 below-floor + 36 above). So §4 (a tier-2-WR-gradient criterion) is measuring a layer where the variance has already been spent at tier-1.

**STRATEGIC FORK → MATT (not autonomous levers — this questions the instrument frame, not a stale constant):** the campaign has cleared the inherited-uncalibrated gates; what's revealed is (a) tier-2 encounters undertuned relative to kit power (universal ceiling — possible content re-tune), (b) §4/tier-2 may be the wrong acceptance layer given selection lives at tier-1, (c) genuine content non-viability on boss_with_adds (0-KPM kits — bimodal, not a band). This is a design-steward (gandalf, §4 author) + Matt decision, NOT more autonomous re-banding. KR recommendation: fire gandalf for the §4 design read on the inverted surface (his authored criterion) → Matt steers. KR did NOT autonomously fire gandalf or another lever — surfacing the inflection to Matt first because it questions the campaign frame.

**Matt touchpoints outstanding: this §4-verdict fork (LIVE) + R5 VALUES.** Sole live KR shell; no run in flight.

---

## ⭐ KR DELTA (2026-07-08) — Matt rules A on gandalf §4 acceptance-layer REFRAME; KR sequencing jack-ryan review → gamora re-point → step-4-bis → R4

**Matt RULING: A** on `gandalf/notes/2026-07-08-s4-inverted-surface-acceptance-reframe.md` (gandalf's verdict on his OWN §4 criterion; DRIFT-CRITIC on SPEC-AUTHOR self). The reframe:
- **tier-1 KPM = THE MEASUREMENT** (per-scenario clear-speed envelope = the discrimination surface; ~2.4× spread empirically live in the SAME run that failed §4-as-authored — open p10/p90 22.3/53.8, choke 23.3/57.1).
- **tier-2 WR = VALIDITY SCREEN** (clears on-tier ⇒ viable; cannot engage ⇒ flagged non-viable; the WR number beyond that bit is NOT the discriminant).
- **WR-gradient's true home = the difficulty LADDER** (per-build wall depth = descent depth-scaling run-model; POST-DEMO instrument).
- **§4-as-authored = uncontested FAIL, but the CRITERION was mis-pointed, not the engine** — a single-rung WR gradient is the one shape the genre (D3 GR-farm, PoE mapping) never produces; discrimination is CLEAR SPEED. The un-stack removed the lockout that made rails=broken; WR≈1.000 now = competent pop clearing on-tier content.
- **Goodhart self-test PASSED + shown (§4):** stands on falsifiable genre + in-run-data claims independent of the gate outcome; preserves §4's spirit (spread-not-rails, relocated to KPM space where it's live + still demandable); deletes NO finding. Key reassurance: **the certification architecture ALREADY runs on KPM bands** (`season_emit`/`family_certification_pass` consume band verdicts) — the amendment is SMALL (rule tier-2 WR → validity bit, not gradient).
- **Findings preserved:** boss_with_adds genuine non-viability (117/189 kits kill ZERO mobs — content, parallel lane, possible boss-KPM-mis-instrumentation fork); magic_pack band (18.61,100.00) never got step-5 density re-derivation (audit it); lethality-floor = Godot game-feel/playtest workstream, explicitly NOT a certification gate.

**MATT SEQUENCE (serial, each gates the next):**
1. **jack-ryan review of the note** — independent review of a self-amended criterion (mandatory per note §6.1). FIRING NOW (Pattern-A). Scrutiny: the Goodhart self-test, the genre claims' defensibility, the "certification already runs on KPM bands" architectural claim (VERIFIABLE in code), whether any finding is silently deleted. Also: the reframe is decisions-log-worthy (architectural acceptance-criterion change) + the earlier §6 proposal still pends at `qa/pending/` — jack-ryan's authoring authority to batch.
2. **gamora certification re-point per note §6.2** — tier-2 WR → validity bit + non-viability flags; KPM bands stay discrimination surface; magic_pack band gets the step-5 density-anchored audit; Gate-2 per ADR-004. Small diff (architecture already points this way). GATED ON jack-ryan clearing the note.
3. **step-4-bis verdict on EXISTING run data** (no re-run — KPM spread live, validity screen 765/769 viable, flags emitted) → expected PASS under amended criterion → chain unblocks.
4. **chain proceeds to R4 / Leg-C** (summoner campaign), boss_with_adds carried as a FLAGGED scenario (KR sequences whether content fix lands pre/post-R4 on gamora's data pull).

**Matt touchpoints outstanding: R5 VALUES** (+ any that surface from jack-ryan review / the boss_with_adds content lane). Sole live KR shell; no run in flight.

---

## ⭐ KR DELTA (2026-07-08) — jack-ryan CLEARS §4 reframe WITH-CONDITIONS; firing gamora certification re-point (step 2)

**jack-ryan verdict: CLEAR-WITH-CONDITIONS** (`qa/findings/2026-07-08-jackryan-s4-reframe-review.md`). No load-bearing defect; the reframe is sound engineering, not moving goalposts. All four scrutiny points cleared:
- **Goodhart self-test passes genuinely** — relocates spread-not-rails to the KPM axis where it's empirically live (~2.4×) AND carries the falsifier forward (if KPM spread ever collapses to point-mass, amended criterion FAILS). A quiet deletion removes the falsifier; this one keeps it.
- **Architectural claim VERIFIED IN CODE** — `gauntlet_sim.py`: `season_emit`(:966)→`gauntlet_pass`(:963)→`family_certification_pass`(:864)→`_shell_result_passed`(:810). Clear shells gate on `ENCOUNTER_COHORT_KPM_BAND`(:778,:815); boss shells gate on `tier_2_survival_rate >= SURVIVAL_FLOOR` — survive-and-kill viability bit, KPM band never consulted (:783,:824-829). Win-condition split codified :192-204. **Certification already keys off KPM bands + a survival-viability bit → the reframe is a small overlay-correction, materially lower risk; "step-4-bis re-verdicts on existing data, no re-run" is credible.**
- **Genre claims defensible** (D3 farm-tier/rifts-hr, PoE maps-hr, single-rung WR near-binary — standard ARPG endgame grammar).
- **No silent deletion** — boss_with_adds flagged, lethality-floor routed, 4-mid on record, magic_pack queued, G2 bimodality honestly partial-retracted (amplitude=artifact, direction survives).

**CONDITIONS (carry into gamora re-point):**
1. **magic_pack stale-band audit must LAND before step-4-bis is scored clean on that shell** (band (18.61,100.00) never got step-5 density re-derivation).
2. **boss observable-fork stays OPEN** — KPM-primacy applies to CLEAR shells only; boss shells already gate on the survival-viability bit, not KPM.

**decisions-log advice (jack-ryan, authoring authority):** the reframe warrants a SEPARATE entry (difficulty-instrument ruling), NOT folded into the pending §6 un-stack proposal (distinct architectural rulings). Both authorable same batch, cross-linked, residual falsifier captured. jack-ryan to draft both next pass. No re-litigation of Matt's A-ruling.

**→ Step 2 FIRING: gamora certification re-point per note §6.2** (Pattern A, autonomous chain). Scope: (a) tier-2 WR → validity bit + non-viability flags (small overlay — arch already points this way per code-verify); (b) magic_pack band density-anchored audit per step-5 method (math-note-first, Discipline #1) — CONDITION 1; (c) boss-shell KPM-primacy NOT applied (CONDITION 2 — boss stays on survival-viability bit); (d) Gate-2. Then step-4-bis verdict on EXISTING data.

---

## ⭐ KR DELTA (2026-07-08) — gamora step-6 cert re-point Gate-2 PASS-WITH-FOLLOWUP; step-4-bis CLEARED; firing gandalf verdict (step 3)

**gamora step-6 executed** (tag `gamora/v-r3a-step6-cert-repoint-magicpack-audit-1`, pushed). Report:
- **Part (a) code delta = ZERO** — the §4 "WR gradient" was NEVER coded; it was only ever an overlay acceptance criterion in gandalf's note. The gating spine already gates clear-shells on KPM band + boss-shells on `survival_rate >= SURVIVAL_FLOOR`, no gradient/mid_mass demand anywhere. The reframe aligns the CRITERION to what the code already does. Non-viability flags already served by the step-5 breakout.
- **magic_pack band re-derived `(18.61,100.00) → (12.52,102.86)`** (CONDITION 1). Density-anchored, same method as step-5. Anti-curve-fit PASS: geometry ceiling 102.86 lands ~1.4 KPM ABOVE observed p90 (101.5) = honest anchor (stale 100.0 sat on/below p90). Re-band admits +18 fast-clears (in-band 36→54).
- **NEW content finding: magic_pack genuinely TRIMODAL** — LOW 117/MID 54/HIGH 18 (jack-ryan confirmed exact counts). The 117 = timeout non-clears = genuine below-floor CONTENT finding (parallel to boss_with_adds non-viability; floor-insensitive — reject below whether floor is 18.61 or 12.52). Correctly left FLAGGED, not curve-fit down to admit them.
- **Boss shells UNTOUCHED** (CONDITION 2) — smoke proves boss fails on survival<floor even with KPM=999.
- **No MIGRATION** (internal to simulation/). Smoke PASS + 77 regression green.

**jack-ryan Gate-2: PASS-WITH-FOLLOWUP** (`qa/findings/2026-07-08-jackryan-r3a-step6-gate2.md`). All 5 points verified AT SOURCE (grep confirms no gradient gate; re-ran p90≈101.5; re-ran boss smoke = KPM ignored; confirmed 117/54/18; re-ran smoke+77 green). **step-4-bis CLEARED to fire.**
- **Follow-up (non-blocking):** thin ceiling margin (~1.4 KPM) = coarse brisk-sweep estimate; revisit ONLY if magic_pack rails at 102.86. Not a blocker — floor (not ceiling) governs the load-bearing 117 rejects, floor-insensitive.
- **Content-lane action:** magic_pack 117 trimodal-LOW carried into R4 content lane PARALLEL to boss_with_adds.
- Cosmetic note: stray `.claude/worktrees/` test copy causes conftest glob collision; ran clean from `tests/`.

**→ Step 3 FIRING: gandalf step-4-bis verdict** on EXISTING run data under the AMENDED criterion (Pattern A). Expected PASS. Then step 4 = chain proceeds to R4/Leg-C.

---

## ⭐ KR DELTA (2026-07-08) — gandalf step-4-bis VERDICT = PASS; R3a arc CLOSED; R4 readiness under investigation (season_emit yield + LLM posture)

**gandalf step-4-bis: PASS** (`gandalf/notes/2026-07-08-r3a-step4-bis-verdict.md`, `8bce543`). Scored the endgame-BC surface against the AMENDED §3 criterion (not the retired single-rung WR gradient), on EXISTING run data, no re-run. All three pass-conditions met:
1. **tier-1 KPM discrimination LIVE** — falsifier (point-mass ⇒ FAIL) checked, does NOT fire. ~2.4× spread (open 22.3/31.9/53.8, choke 23.3/35.2/57.1), median off both tails. Wide, not a reach.
2. **tier-2 WR validity screen** — 765/769 viable (0.995 ceil-fraction); non-engagement FLAGGED via `tier_1_reject_breakout`, not silently gating.
3. **Non-viability preserved, not deleted** — boss_with_adds (117/189 zero-kill) + magic_pack trimodal-LOW (117 timeout non-clears) both carried FLAGGED.
- **Goodhart self-audit held explicit:** four FAIL-conditions named (KPM point-mass, silent gating, floor curve-fit, deleted finding); none fired. magic_pack re-band (in-band 36→54) STRENGTHENS the verdict in the reframe's own direction (+18 admitted = HIGH-mode fast-clears = the live discrimination signal).

**→ The 4-step Matt sequence (jack-ryan review → gamora re-point → step-4-bis → R4) is COMPLETE through step 3. R3a recalibration arc (steps 1-6 + step-4-bis) CLOSED and PASSED.**

**R4 carry-forward (from gandalf verdict):** (a) boss_with_adds + (b) magic_pack trimodal-LOW as FLAGGED content-lane items — NOT emission gates on Leg-C; (c) KPM-primacy is a CLEAR-shell statement only — boss rooms gate on the survival-viability bit.

**KR one-step-ahead check BEFORE firing R4 (misalignment-prevention, not a stall):**
- **"WR-bracket filter" in `season_generation_pipeline.py:1816` is a LEGACY MISNOMER, not a residual WR-gradient gate** — line 1772 relays each kit's `season_emit` bool from the gauntlet JSON (`kit_result.get("season_emit", False)`), downstream of `family_certification_pass`. No separate gradient gate in generation. (Disc-#12 label-hygiene item, functionally correct — queue with gamora's docstring fixes.)
- **OPEN: season_emit yield.** Last empirical data point (step-4 re-run bs2ptidcr, under step-5 bands, PRE-step-6 magic_pack re-band) = `kits_season_emit=0`, 0/18 in-band survivors. R4/Leg-C exists to produce bands for R5; 0-emit ⇒ chain cannot reach R5. Must confirm current HEAD (step-5+step-6 bands) produces >0 emit before/at R4.
- **OPEN: R6 LLM-spend guardrail.** R4/Leg-C posture (summoner campaign) must be $0 or it HALT-LOUDs per R6. Verifying scope + cost posture before firing.

---

## ⭐ KR DELTA (2026-07-08) — R4 NOT READY: F4 escape_lane band unregistered → season_emit=0 by construction. CHAIN STOPS at R4 for Matt routing (the anticipated "third touchpoint")

**KR pre-fire readiness check (did NOT fire R4 blind) → gamora $0 read-only diagnosis → DEFINITIVE:**

**R4/Leg-C would emit ZERO kits by construction. The blocker is NOT the R3a recalibration (that closed PASS) — it is the un-done half of the Q11 four-family lane: the F4 `escape_lane` band was never wired into `_shell_result_passed`.**

- `season_emit` (`gauntlet_sim.py:989`) = `any(gauntlet_pass(c) ...)`; `gauntlet_pass` (`:979`, R4-flip `08972d0`) → `family_certification_pass` (`:893`) = conjunction over ALL FOUR families. **F4 = frozenset({"escape_lane"})** (`:245`), sole member, no substitute.
- **F4 is dead code:** `escape_lane` appears ONLY at `:245` (the set) + `:966` (a docstring narrating its own absence). The F4 branch (`:847-851`) is **comment-only** — sets no band, falls through to the clear-shell KPM lookup where escape_lane has no entry → `:856 return False`. `family_passed(cohort,"F4")` is **False for every cohort** → `family_certification_pass` universally False → **season_emit=0 unconditionally.** This is the KNOWN "zero emit until Lane-3 registers F4" state (MIGRATION.md:21; run-state :229).

**Why R3a couldn't move it (two decoupled instruments):**
- R3a recalibrated the **T1 6-shell pilot gauntlet** (open_arena/chokepoint/magic_pack/boss_with_adds) — NO escape_lane, NO dense_cell.
- `season_emit` rides the **four-family cert instrument** (`gauntlet_four_family_metrology_driver.py` + `arena.py:1037` escape_lane) — a DIFFERENT code path. R3a's spatial bands cannot move season_emit. Both hypotheses A + B true; A is the root cause.

**The blocker = F4 escape_lane criterion wiring into `_shell_result_passed` (`:847-851`).** The VALUES EXIST (run-state :143, Lane-3-derived: F4 KPM floor 60 / ceiling 150 / exit-within-window ≥0.80) but were never wired. **Seam split:** wiring = gamora's (`_shell_result_passed` is her code; math-note-before-code per Disc #1); band-VALUES cert-criterion ratification = jack-ryan Lane-3 (`:832` design-note handoff). **Scope:** distinct dispatch, un-done half of the Q11 four-family lane; in-scope for batch-2 but NOT enumerated in the ratified R1-R6 table → a scope-extension.

**LLM-spend ambiguity (R6 guardrail):** "Leg-C" is OVERLOADED in run-state. Pure-sim four-family cert sweep = $0/autonomous but emits 0 (blocked above). star-lord's **Leg-C season-emission is gated behind rocket's gen-path leg-3 = an LLM-EMISSION run** (run-state :318) → if R4/Leg-C means THAT, it is a **Matt HALT-LOUD per R6 regardless of the F4 fix.**

**KR ROUTING DECISION: CHAIN STOPS at R4. Surfaced to Matt** (my line-763 flag realized: "likely a THIRD Matt touchpoint the pre-ratification didn't anticipate"). NOT auto-firing the F4-registration dispatch — it's a scope-extension (needs fresh Matt-auth per CLAUDE.md) AND requires a cert-criterion ratification AND the downstream emission-run LLM posture is unresolved. Decision-ready fork presented to Matt. **No run in flight. Matt touchpoints now live: (1) this R4-blocker routing; (2) R5 VALUES (still parked downstream).**

---

## ⭐ KR DELTA (2026-07-08) — Matt rules F4-registration AUTHORIZED as chain-extension; R4/Leg-C = pure-sim $0 cert sweep; sequence F4 → R4 → R5. Firing gamora F4 wiring.

**MATT RULING (2026-07-08):**
1. **YES — F4-registration authorized as chain-extension.** gamora wiring (math-note-first, $0); jack-ryan Lane-3 ratification WITH **gandalf's rider: verify the 60/150/≥0.80 values against escape_lane's spawn arithmetic via the step-5 density-anchored method, NOT rubber-stamp**; Gate-2.
2. **R4/Leg-C = the pure-sim four-family cert sweep** — $0, autonomous, fires on F4 green. The season-EMISSION run is **post-R5 by design** (bands → Matt VALUES → emit once) and stays a Matt touchpoint per R6 HALT-LOUD.
- **Sequence:** F4 work unit → R4 cert sweep → R5 VALUES touchpoint.
- gandalf's §6 chain (`gandalf/notes/2026-07-08-s4-inverted-surface-acceptance-reframe.md`) HOLDS, with **F4 inserted before R4.**

**KR execution structure (autonomous, $0 throughout):**
- **Step F4-a (gamora, FIRING NOW, Pattern A):** math-note-FIRST = the density-anchored verification of F4 escape_lane values (KPM floor 60 / ceiling 150 / exit-within-window ≥0.80) against escape_lane spawn arithmetic via the step-5 density-anchored method (gandalf's rider; may ADJUST values if arithmetic disagrees). THEN wire the (verified) criterion into `_shell_result_passed` (`gauntlet_sim.py:847-851`, currently comment-only). Smoke-test (four-family cert now reachable), tag, commit+push, completion note for jack-ryan.
- **Step F4-b (jack-ryan, GATED on F4-a):** Lane-3 ratification of the F4 band criterion + Gate-2 on gamora's wiring, enforcing gandalf's anti-rubber-stamp rider (confirm the verification was density-anchored, not an inherited-value rubber-stamp). ALSO lands the deferred Lane-3 decisions-log entries (run-state :357: R4 cert-contract shift + open_arena re-base + mobs_killed range + the F4 registration).
- **Step R4 (KR, GATED on F4-b green):** fire the pure-sim four-family cert sweep ($0, `gauntlet_four_family_metrology_driver.py`); judge yield — expected >0 season_emit now that F4 can pass. Carry boss_with_adds + magic_pack trimodal-LOW as FLAGGED content-lane items (not emission gates).
- **Step R5 (Matt touchpoint):** band-sheet VALUES — parked, the designed human gate.

Matt touchpoints live: **R5 VALUES** (+ the post-R5 season-emission run). No run in flight.

---

## ⭐ KR DELTA (2026-07-08) — gamora F4-a COMPLETE (values CONFIRMED density-anchored); firing jack-ryan F4-b (Lane-3 ratification + Gate-2 + decisions-log)

**gamora F4-a** (tag `gamora/v-batch2-f4-escape-lane-registration-1`, engine+collab pushed; note `gamora/notes/2026-07-08-f4-escape-lane-band-registration.md`):
- **Density-anchored verdict: 60/150/≥0.80 ALL THREE CONFIRMED** (not rubber-stamped per gandalf's rider). Derived escape_lane's honest demand from spawn arithmetic (55m lane / ~3-per-s stream / ~192 supply / 60s window / ×2.0 champion elevation); the inherited Lane-3 bars CONFIRM because escape_lane was BUILT to the §3-F4 genre spec → genre-anchored bars + geometry-anchored demand consistent by construction (contrast step-5/step-6 which ADJUSTED).
- **Anti-curve-fit cross-check: HONESTLY UNAVAILABLE** — no observed escape_lane distribution on disk (F4 branch was dead → no cert run ever produced one). Derived geometry-only, named the falsifier, did NOT invent a distribution.
- **Observable: exit-within-window ≥0.80 PRIMARY + KPM [60,150] SECONDARY** (escape_reached = success/exit metric, like F3 success-judged not KPM-primary). **Field-identity (no new schema):** exit fraction IS `tier_2_survival_rate` for escape_reached rooms — `winner=="player"` IFF `escape_reached` (`spatial_engine.py:2874-2888`).
- **Wiring:** new branch in `_shell_result_passed` + 3 constants (`_F4_ESCAPE_SHELL_GATE_TYPES`, `_F4_EXIT_WITHIN_WINDOW_FLOOR=0.80`, `_F4_KPM_BAND=(60,150)`) + docstring updates. **`family_certification_pass` now reachable-True** (smoke proves a walled/under-KPM kit still fails F4 = no manufactured passes); **F1/F2/F3 byte-identical.** MIGRATION v1.86 (within-seam discharge of the v1.85 zero-emit contract; no star-lord schema change).
- Pre-existing P5-cohesion-judge LLM-seam test failure, git-stash-verified NOT this seam (Disc #11).

**→ Firing jack-ryan F4-b (Pattern A):** Lane-3 ratification + Gate-2, with two KR-flagged pressure points: (1) **is "CONFIRMED by construction" a legitimate verification or a circular rubber-stamp?** — the room was built to the spec that set the bars, so agreement may be tautological, not corroborative; gandalf's rider exists precisely to catch this. (2) **The band is being registered with the anti-curve-fit cross-check UNAVAILABLE** — the R4 cert sweep will be the FIRST live escape_lane result; is registering a never-observed band acceptable, or does the band get a re-check after R4 produces the first distribution? Plus: the deferred Lane-3 decisions-log entries (R4 cert-contract shift + open_arena re-base + mobs_killed range + F4 registration) AND the §4-reframe entry jack-ryan advised earlier + the still-pending §6 proposal at `qa/pending/`.

---

## ⭐ KR DELTA (2026-07-08) — jack-ryan F4-b PASS-WITH-CONDITIONS; R4 cert sweep CLEARED + FIRING (gamora launches detached)

**jack-ryan F4-b: PASS-WITH-CONDITIONS** (`qa/findings/2026-07-08-jackryan-f4-registration-gate2-lane3.md`; engine `2fd05c4` + collab `732d011` pushed per R6 chain grant). R4 cert sweep CLEARED.
- **Pressure 1 (circular rubber-stamp?): NO — derivation INDEPENDENT.** Every math-note premise re-verified as an actual spawner/geometry param at `arena.py:1058-1097` (55m lane, ~3 fodder/s, ~192 supply, cap 50, ×2.0 elevation, 60s window) — NOT back-read from spec bars. gamora derives demand and *compares*; doesn't back-read the bar she checks. CONFIRM stands (with recorded caveat: a CONFIRM is weaker corroboration than an ADJUST is informative — room was tuned to spec — which is why Pressure-2 matters).
- **Pressure 2 (never-observed band): acceptable geometry-only, BUT MANDATORY RE-CHECK CONDITION** → after R4 produces the FIRST escape_lane distribution, run geometry-vs-p90 cross-check + re-validate 0.80/[60,150] **before R5 band-sheet VALUES are trusted.** Decisions-log entry stamped PROVISIONAL-pending-first-observation.
- Standard Gate-2 all PASS: field-identity exact (`spatial_engine.py:2874-2888`), wiring fail-safe, smoke re-run PASS (genuine gate, no manufactured passes), 52/52 regression, F1/F2/F3/T1-pilot byte-identical, P5 fail not-this-seam, MIGRATION v1.86.
- **Decisions-log (4 entries, batched/cross-linked, Status:Active):** F4 registration [PROVISIONAL] · R4 cert-contract shift + open_arena re-base + mobs_killed range · §4 acceptance-layer reframe [falsifier captured] · §6 MOB_HP un-stack Option A [pending §6 proposal folded]. + 2 SCOPE-RETIRED status edits.

**→ R4 STEP FIRING (KR autonomous, $0 pure-sim four-family cert sweep):** gamora launches the four-family metrology driver DETACHED (kill-verify first: no prior driver PID; never two same-seed emissions). Run MUST capture: (a) `season_emit` count — expected >0 now F4 can pass; (b) the **first-ever escape_lane distribution** (feeds jack-ryan's mandatory re-check condition); (c) per-family pass breakdown. $0 dry_run_flavor, no LLM (R6). KR monitors output, judges yield, then routes: >0 emit → bands land → R5 VALUES touchpoint (+ jack-ryan F4 band re-check on the fresh escape_lane distribution). 0 emit → HALT-LOUD diagnosis.

---

## ⭐ KR DELTA (2026-07-08) — R4 cert sweep EXITED: 0 season_emit (REAL this time, F4 live) + anomaly → HALT-LOUD, diagnosing before routing to Matt

**R4 four-family metrology sweep** (PID 42455, seed 64M, 17.0s, $0 confirmed, report `output/gauntlet_four_family_metrology/metrology_report_20260708_125938.json`). Per-family medians:
| Family | martial | caster |
|---|---|---|
| F1 dense_cell | kpm 13.64 / wr 0.0 / **pass 0/40** | kpm 100.0 / wr 0.0 / **pass 0/2** |
| F2 open_arena | kpm 21.51 / wr 0.0 / **pass 0/40** | kpm 87.69 / wr 0.0 / **pass 0/2** |
| F3 boss_with_adds | kpm 31.23 / wr 0.6 / **pass 0/40** | kpm 100.0 / **wr 1.0** / **pass 0/2** |
| F4 escape_lane | kpm 22.31 / wr 0.0 / **pass 0/40** | kpm 88.66 / wr 0.0 / **pass 0/2** |

**season_emit = 0 AGAIN — but NOT the prior dead-code blocker.** F4 is now LIVE (real kpm/wr numbers, not comment-only). This is a genuine certification result: 0/40 martial + 0/2 caster pass, all four families.

**Two signals I will NOT interpret raw (firing gamora $0 read-only diagnosis first):**
1. **Pattern INVERTS R3a.** Four-family instrument shows WR med=0.0 (kits DYING) across F1/F2/F4 — OPPOSITE of the T1 pilot's 765/769 CEILING (WR≈1.0). BUT different populations (sweep = econ-pilot casters + martial-template cells @ seed 64M, NOT the 18 endgame-BC candidates) AND a harder genre-density instrument (F1 ~24, F2 ~40). Need: is this a real floor-saturation, wrong-kits-for-cert, or band-mismatch?
2. **ANOMALY: F3 caster wr med=1.0 but pass=0/2** — a 100%-survival kit failing the boss family. Possible gate-logic issue OR a metric I'm misreading. Must resolve before trusting ANY of the pass counts.

**Open questions for gamora diagnosis ($0, read-only):** (a) is 0/40+0/2 EXPECTED for metrology PROBE cells (untuned templates) vs a real cert failure? (b) does THIS run even answer "does season_emit go >0" — or is season_emit measured via the GENERATION pipeline's real candidates (a different run)? (c) the F3 caster wr=1.0/pass=0 anomaly. (d) confirm escape_lane distribution captured for jack-ryan's mandatory re-check. (e) bottom line: chain-proceeds-to-R5 or HALT-LOUD-to-Matt, and the crisp finding either way.

**CHAIN POSTURE: HALTED at R4 pending diagnosis.** No auto-resume. escape_lane distribution IS captured (jack-ryan re-check has data regardless). Matt touchpoints live: this R4 result (routing after diagnosis) + R5 VALUES.
