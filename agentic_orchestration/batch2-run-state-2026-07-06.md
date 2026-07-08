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
