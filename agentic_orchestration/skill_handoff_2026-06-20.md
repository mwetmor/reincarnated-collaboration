# Skill Handoff — 2026-06-20

**Author:** knight-rider
**Prior handoff:** `skill_handoff_2026-06-19.md`

## Instrument-validity workstream — DROVE Phases 1-4 to completion; HALTED at the Phase-R/Phase-5 wall (Matt decision)

Autonomous orchestration run driving the gandalf-authored instrument-validity workstream (`gandalf/requests/2026-06-20-instrument-validity-workstream-KR-brief.md`). Four instrument defects on the combat damage equation, each fixed and **measured in isolation against the standing (untouched) bands**; bands refit ONCE at Phase 5 against the composed instrument; then the first honest STR-lever read at Phase 6.

### Phases 1-4 — COMPLETE, all Gate-2 PASS-WITH-INFO (gamora implement, jack-ryan gate)

| Phase | Fix | Result | Tag | Gate-2 |
|---|---|---|---|---|
| **1** | Resource-economy wiring (gate + decrement + energy_type-branched pool, ported from kernel `_ENERGY_CONFIGS`) | G2 auto-resolve: KPM flat-not-rising (gate correct but inert until Phase 2 fires expensive tiers); flag `WIRE_RESOURCE_ECONOMY`, OFF=byte-identical | `gamora/v-resource-economy-phase1-1` (engine `c28d027`) | PASS-WITH-INFO |
| **2** | Rotation selector (energy_type-branched build-vs-spend; FULL branch set built) | G3a PASS: T1-collapse BROKEN (100% T1 → 53.9% T1 / 46.1% T4 burst→lull); G3b (rage falsifier) BUILT-but-UNMEASURED (false-PASS guard held) | `gamora/v-rotation-selector-phase2-1` (engine `e2f3929`) | PASS-WITH-INFO |
| **3** | DoT activation + physical-DoT scaling (F1/F2 pre-committed `e537b29`; + NEW F3-DEFECT fix) | G4 auto-resolve: STR bleed now >0 (`dot_dps=0.10`); per-tick symmetry holds (STR 1.24 / INT 1.27); realized gap is throttle-driven not magnitude | `gamora/v-dot-activation-phase3-1` (engine `9e1d25d`) | PASS-WITH-INFO |
| **4** | Armor/resist symmetry (Path-B `from_monster` off-element floored to armor curve) | G5 auto-resolve: caster boss-survive fell toward martial (int boss KPM 98.96→0.73); martial unchanged (str Δ=0.000 every shell); no over-correction; flag `MITIGATION_SYMMETRY` | `gamora/v-armor-resist-symmetry-phase4-1` (engine `d2d3dde`) | PASS-WITH-INFO |

**Disciplines held throughout:** math-note-first (#1), recompose-first (PORT not BUILD — no new mechanic in any phase), measure-ISOLATED (bands UNTOUCHED in 1-4; `bands_untouched:true` verified each gate), fresh disjoint seed bases per phase (820000 / 8.5M / 16M / 24M), semantic-shift declared at all four boundaries (#12 — jack-ryan confirms the four-boundary chain is assembled + coherent), no production-gate regression. All commits local on `main`; **NOT pushed** (Matt-gated, ADR-006).

**New mechanism bug found + fixed in-phase (Phase 3, recompose-first):** `_add_or_refresh` let the ~22×-more-frequent zero-tick T1 bleed clobber the live T4 bleed (tick=5) to zero — a second, independent zeroing mechanism distinct from the SESSION-31 selector collapse. Fix: DoT refresh keeps MAX tick_damage (faithful ARPG rule, scoped to DoT-only). jack-ryan ruled SOUND. Routed gamora→re-gate→proceed per the autonomy envelope; did NOT go to Matt.

### Phase R — COMPLETE (Matt-authorized + executed) | G3b PASS | Phase 5 → DIAGNOSTIC STOP at a Matt halt

**Matt authorized Phase R** (scope) with a gandalf design-constraint amendment (G1 table LOCKED; rocket's room is only the population→kit-type KEY; key-ambiguity → gandalf, round-trip → KR). The Phase R chain then ran end-to-end inside the autonomy envelope:

| Step | Owner | Result |
|---|---|---|
| Phase R implement | rocket | DONE — `_assign_doc48_economy` + `_DOC48_ECONOMY_BY_BC` on `season_generation_pipeline.py`. Both guards HELD (KEY = doc-48's own `(attr,range,tempo,amplitude)` signature, proven collision-free; bc_target round-trip untouched — harness path doesn't call it). Population now rage:12/combo:9/stamina:3/mana:30; all 9 STR-melee → rage. Tag `rocket/v-phaseR-reference-economy-hardening-1` (engine). |
| Phase R Gate-2 | jack-ryan | PASS-WITH-INFO (`qa/findings/2026-06-20-phaseR-rocket-reference-economy-gate2.md`, commit `81b39f9`). Both guards verified first-hand; contract verified (emitted vocab ⊂ kernel `_ENERGY_CONFIGS`); no gamora code change required. INFO: charge-stack absent from `bc_target_source._ENERGY_ECON` — inert for this workstream (no DEX-melee-spiky cell), MIGRATION-flagged for the production season_orchestrator owner only. |
| G3b re-arm | gamora | PASS — rage build-spend rhythm fires (T4 spender 45.7%→78.5% swarm→anchor, +32.8pp); economies distinguishable (rage-vs-mana TVD 0.386; 5/6 pairs). Tag `gamora/v-g3b-rearm-1`, seed base 32M. **Phase-6 carry:** the `anchor_present = max_hp>=600` predicate is INERT at live HP regime (swarm ~39,750 / boss ~231,000) — rhythm fires via the energy threshold, not the anchor gate. |
| G3b ruling | gandalf | CONCUR PASS (`gandalf/notes/2026-06-20-G3b-disposition-and-anchor-predicate-ruling.md`). Anchor predicate = Phase-6-INTERNAL tuning input (owner gamora; gates Read-2 mixed-pack focus-fire ONLY; criterion = anchor-targeted spender fraction ≥60% on mixed shells; does NOT gate Phase 5 / Phase-6 Read-1). **Phase 5 CLEARED.** |

**PHASE 5 (the ONE composed re-baseline) → DIAGNOSTIC STOP (gamora, engine `b70f173` / collab `fe4837f`).** gamora ran the refit math-note-first with the ported single-per-shell band method and STOPPED rather than wire a fake band. **Finding:** the composed (honest) instrument's KPM is strongly economy-dependent WITHIN each shell — cohort-invariance is broken. elite_pack: rage 8.3 vs stamina 600 = ~72× spread. Mechanism: all economies kill the same pack but DURATION differs ~70× — unthrottled casters one-shot small packs in 0.3-0.5s → a 600-KPM timing-floor artifact (magic/elite); casters read ~0.5 KPM on boss (long single-target grind). A single per-shell percentile band over an 8→600 mixture is a fake instrument (re-introduces the contamination the workstream removed, one layer down). Brief forbids gamora inventing band methodology or magnitude-retuning → correct STOP. Artifacts: math-note `simulation/math/composed-rebaseline-phase5-2026-06-20.md`; STOP JSON `cycle-14-wave-5-season-001/composed-rebaseline-phase5-DIAGNOSTIC-STOP-20260620.json`; harness `scripts/gamora_composed_rebaseline_phase5_2026_06_20.py` (ready to re-fire once the fork resolves). Bands UNTOUCHED, no band wired.

**GANDALF RULED the three forks** (`gandalf/notes/2026-06-20-composed-rebaseline-three-fork-ruling.md`) — headline: **gamora's STOP rediscovered, from the composed path, the encounter-measurement doctrine Matt ALREADY ADOPTED 2026-06-19** (boss shells → survive-and-kill, not KPM). NOT a new design question.
- **Fork 1 (economy-aware band?): NO + reframed.** Band becomes WIN-CONDITION-aware (already-ruled doctrine), NOT per-economy. Boss/mini_boss shells DELETE the KPM band → survive-and-kill (that's where the 72× spread + 0.25-0.58 craters live). Clear shells keep one KPM band per shell; per-economy-vs-single on clear shells DEFERRED behind fork 2. Do NOT have gamora re-fire `--full` per-economy — that builds the methodology gandalf ruled against.
- **Fork 2 (timing-floor): LEAVES the workstream** (magnitude — SPATIAL_DAMAGE_SCALE/mob-HP, composes with MOB_HP). Asymmetric boundary: blocks ONLY the clear-room re-band, NOT the boss-gate. Boss-gate lands NOW with zero magnitude work.
- **Fork 3 (design): both are IDENTITY, not defect.** Caster burst = legit fantasy (the 600 number is artifact, magnitude-tune it to a fast measurable clear). Caster "crater" = NO crater — clean-boss-run showed int/wis survive+kill ≈0.99, ~33-35s TTK; the 0.58 is the METRIC cratering on a single-target shell, not the caster. Phase-4 worked.

### THE ONE MATT DECISION NOW (Phase 5 halt — sequencing ratification, not a new design call)
**Wire the already-ruled boss-gate now** (boss/mini_boss shells leave the KPM band onto survive-and-kill-in-enrage-timer — resolves the boss-row spread with ZERO magnitude work; owner gamora), **and defer the clear-room re-band behind the scheduled SPATIAL_DAMAGE_SCALE/mob-HP magnitude pass** (caster clear cells are timing-floor artifacts no honest band can fit until magnitude is calibrated). Matt is ratifying a sequencing of principles he already ruled. Workstream is ON its spine (boss-gate = §6 of the doctrine spine, same work not new work); the single deliberate refit holds (it IS the boss-shell refit; the clear-shell refit is the one piece waiting on magnitude).

### BOSS-GATE BUILT (Matt-ratified the Phase-5 sequencing) → at a Matt disposition-approval halt
Matt RATIFIED the Phase-5 sequencing (boss-gate now / clear-band after magnitude) and authorized the boss-gate build (`gandalf/requests/2026-06-20-boss-gate-implementation-spec.md`). The chain ran end-to-end in the envelope:

| Step | Owner | Result |
|---|---|---|
| Boss-gate build | gamora | DONE — recompose-first REWIRE (sg2 was computed but gated nothing). (a) boss shells route to tier_2 unconditionally; (b) `eligible_encounters_passed` gates boss shells on survive-and-kill ≥ `SURVIVAL_FLOOR_BY_COHORT`, KPM band never consulted for boss shells; (c) DPS/TTK measure-only. Boss-shell-scoped via `_BOSS_SHELL_GATE_TYPES`. Tag `gamora/v-boss-gate-1` (engine `50caa12`), collab `2c75e0c`. |
| Structural Gate-2 (FIRST production-gate change, BLOCK authority) | jack-ryan | PASS-WITH-INFO (`qa/findings/2026-06-20-boss-gate-gate2.md`, `91aa98e`). Gate-only diff, fight path byte-unchanged; NO clear-shell regression (719/720 clear cells identical); substrate-drift claim adjudicated SOUND. |
| Design-fit on inverted disposition | gandalf | `gandalf/notes/2026-06-20-boss-gate-inverted-disposition-design-fit-ruling.md` (`6ab1d4c`). See below. |
| Decisions-log draft + review | KR draft + jack-ryan review | Draft `agentic_orchestration/2026-06-20-boss-gate-decisions-log-draft.md` (`da1ab99`); jack-ryan reviewed ACCURATE, zero changes, will canonical-write to decisions-log.md AFTER Matt approves. |

**THE LOAD-BEARING FINDING — the composed instrument honestly FALSIFIED the §5a prediction.** The spec §3 / doctrine §5a predicted STR FAILS boss shells (timeout 1.000). The WIRED gate on the full composed instrument measures the INVERTED disposition. Split by shell (gandalf caught the pooled numbers hid a cliff):

| attr | boss_with_adds | mini_boss | pooled |
|---|---|---|---|
| str | 1.000 | **1.000** | 1.000 |
| dex | 1.000 | 0.667 | 0.917 |
| int | 1.000 | **0.000** | 0.750 |
| wis | 0.955 | **0.000** | 0.716 |

- **STR now SHIPS boss shells (1.000) — HONEST, the workstream win.** Its real rage economy (Phase R) + full rotation (Phase 2) focus-and-kill the boss (~15s TTK; tier_2_kpm VARIES 8-12, all kill = real capability not flat artifact). Lever is active via rotation/economy, NOT DoT (STR bleed still unemitted). The instrument stopped lying about STR — that's the entire point of the workstream. gandalf + jack-ryan both proved gate-sound + substrate-honest (gate-only diff; §5 measured 2026-06-19 BEFORE the composed fixes).
- **The caster mini_boss 0.000 cliff = CANDIDATE DEFECT, flagged-NOT-ratified.** int/wis = 0.000 on EVERY mini_boss cell but ~1.0 on the harder boss_with_adds, and STR is the only class clearing mini_boss. Wrong shape (categorical not graded) / wrong selectivity (perfect on harder shell, zero on easier) / wrong winner (melee out-solos burst-casters single-target) = instrument-defect fingerprint pointing at the mini_boss scenario config / `mini_boss_killed` win-condition wiring, NOT caster damage. Cliffs are bugs until proven design.

### THE MATT DECISION NOW (Phase-5 boss-half halt — disposition approval, a production-gate change)
- **Approve the gate + the STR finding** (gate is Gate-2-sound; STR-ships-boss is the honest instrument-validity win). jack-ryan canonical-writes the decisions-log entry on approval.
- **Hold the caster mini_boss cliff as flagged, NOT approved** — authorize a cheap targeted diagnosis (pull 2-3 zero cells + 1 STR pass cell; check `mini_boss_killed` vs `boss_killed` win-condition wiring asymmetry, mini_boss HP/resist scaling, killing-but-failing-subcondition). Empirical close criterion: a first-hand explanation of why STR clears mini_boss and casters cannot.

### BOSS-GATE APPROVED-WITH-REFINEMENTS (Matt) → decisions-log WRITTEN; mini_boss DIAGNOSED both halves → AT A MATT IDENTITY-RATIFICATION HALT

Matt approved the gate mechanism (ships), scoped the decisions-log precisely, and authorized a two-halves diagnosis. Both returns are now IN HAND.

**Decisions-log — WRITTEN (canonical).** jack-ryan canonical-wrote the boss-gate entry to `~/Games/reincarnated-engine/design/decisions/decisions-log.md` (commit `d5b7ac2`, 74 insertions append-only). Scoped per Matt rev-2: **BANK boss_with_adds column ONLY** (str/dex/int 1.000; wis 0.944 = gate-pass rate 255/270 / 0.955 = mean survival fraction — both meanings written); **§5a "STR fails boss shells" OVERTURNED = workstream win** (STR ships via RAW THROUGHPUT ~15s kills, not focus-fire — anchor predicate max_hp≥600 inert at ~231k boss HP); **entire mini_boss column HELD in escrow** (incl STR 1.000) as "measured, held pending diagnosis" — NOT written as "STR ships all boss shells". KR draft `agentic_orchestration/2026-06-20-boss-gate-decisions-log-draft.md` rev-2 (`ce7c92f`).

**ENGINE-half diagnosis (gamora) — DONE.** `~/Games/reincarnated-engine/src/reincarnated/simulation/math/miniboss-caster-wipe-diagnosis-2026-06-20.md` (engine `60627e9`); data `cycle-14-wave-5-season-001/miniboss-caster-diagnosis-clean-boss-rerun-2026-06-20.{json,txt}` (collab `e3cd740`). **Decisive finding:** the caster mini_boss 0.000 cliff is **100% TIMEOUTS, not early deaths** — casters are ALIVE and WINNING the fight, the clock kills them. Two stacked mechanical causes: (1) **mini_boss `soft_timeout_s = 150s` guillotine** (boss_with_adds = None → 240s enrage timer) — caster single-target TTK is 125-175s, so they cross 150s mid-kill and force-loss at `spatial_engine.py:1684-1696`; (2) **mini_boss HP rolls ABOVE the full boss** (config inversion) so the "easier" shell is the longer grind. STR clears (~15s raw-throughput kill) under both. Inversion fingerprint = the easier-named shell is harder + the burst classes are the ones failing.

**DESIGN-half ruling (gandalf) — DONE.** `gandalf/notes/2026-06-20-miniboss-design-half-ruling-what-is-miniboss-for.md`. Per Matt's instruction I brought the engine diagnosis back to gandalf for the design call (did NOT resolve it myself):
1. **mini_boss = "a smaller boss," NOT a burst-window enrage check.** No canonical doc ratified a burst identity; the class-fantasy outcome is INVERTED (burst casters wipe, grind STR clears); the "mini" naming-contract is violated (easier-named shell is the harder grind).
2. **DEFECT — both sub-findings.** The 150s soft_timeout is the **same dead-absolute-constant / stale-calibration class** as the four instrument-validity targets (calibrated to a ~3s-TTK / KPM~60 regime, mis-applied to 125-175s caster kills). The mini_boss HP-above-boss roll is a config inversion from a Phase-3c "T4 achievability" reach. Neither is honest texture.
3. **Held mini_boss column does NOT bank.** Convert to confirmed defect → recompose-first re-scale soft_timeout + floor mini_boss HP ≤ boss HP → re-measure caster×shell grid → bank. Owner gamora. Criterion = **inversion gone** (STR no longer the only archetype clearing mini_boss). **Fix FLAGGED, NOT authorized — Matt's identity call picks the soft_timeout target.**
4. **Cross-cutting:** the banked STR-via-raw-throughput boss_with_adds result is UNAFFECTED (timer-insensitive ~15s kills); de-contaminating casters FIRMS the §5a-overturn reading. Add both stale constants (150s soft_timeout, mini_boss HP factor) to the post-workstream absolute-magnitude-constant sweep (task #11).

**PER-CELL DEEPENING (gamora, tag `gamora/v-miniboss-caster-diagnosis-1`, engine `a947053` / collab `5a7337f`, NOT pushed) — CONFIRMS the finding at every grain.** First-hand termination split from the 2026-06-19 clean-boss harness (`/tmp/miniboss-diag/clean-boss-numbers-harness-2026-06-19.json`): int|mini_boss **100.0% timeout / 0.0% death** (960 fights, bossHP_med 0.467); wis|mini_boss **100.0% timeout / 0.0% death** (2400 fights, bossHP_med 0.426); str|mini_boss 0% timeout / 100% win (DPS 48,161). Boss_with_adds: int 99.9% win, wis 95.1% win, str 100% win. **0 of 240 caster mini_boss cells have ANY early death; total caster a_dead across both shells = 0** — casters are never killed anywhere, they out-race nothing defensively and lose to the 150s clock. 80 of 240 wis|mini_boss cells remove ≥90% of the boss and still time out (the "hair short, clock kills them" pattern, by-cell). Diagnosis-only caveat flagged for V5 attribution (NOT a design finding): 14 wis|mini_boss cells report bossHP_removed >1.0 (uncapped damage-accumulation artifact at `clean_boss_numbers_harness_2026_06_19.py:163`; all 20/20 timeouts; disregard — honest signal is pooled ~0.43). Finding STRENGTHENED, design-half ruling UNCHANGED.

**THE ONE DECISION THAT IS MATT'S (gandalf-framed):** ratify the mini_boss IDENTITY. "Smaller boss" (gandalf-recommended) → authorize the gamora recompose-first fix (soft_timeout re-scale toward 240s/boss-align + HP floor ≤ boss) → re-measure → bank. OR a real burst-window enrage check → then design it loud + player-legible (HP inversion gets fixed either way). The fix is not authorized until Matt makes this call. **KR is halted here — this is Matt's, not KR's.**

### Phase 6 status (REFRAMED by the inverted disposition)
gandalf ruled the STR (A)-vs-(B) read is **substantially ANSWERED for the as-is lever** — STR boss-solos via the composed Phase-R economy (not the route-via-floor §5a premise, now obsolete). Read-1 (encounter-segregated) becomes confirmation. Read-2 (mixed-pack focus-fire) + the anchor-predicate rescale (task #8) DOWNGRADED from shipping-blocker to post-halt texture-tuning ("is the now-automatic focus-fire the player-agency version we want?"). Phase 6 Read-1 unblocks on Matt's boss-gate approval.

### TRACKED post-workstream follow-up (gandalf-flagged, do NOT action now) — task #11
The inert anchor predicate (`max_hp >= 600` vs ≥39,750-HP entities) is the same dead-absolute-constant class as the four instrument-validity defects. Open a sweep of absolute-magnitude constants in the spatial selector that should be regime-relative. Post-workstream.

### Phase 6 status (pre-boss-gate note, superseded by the REFRAMED section above)

### --- OBSOLETE BELOW (superseded by the above; retained for trail) ---
### THE SCOPE SURPRISE — Phase R (rocket reference-economy hardening) — AWAITING MATT SCOPE AUTHORIZATION

**What gamora found at Phase-1 G1 (verified first-hand by gamora + gandalf):** the *generated population* never carries the doc-48 economies. Generation infers resource type from BC-tempo (`_BC_TEMPO_TO_RESOURCE`) → `{cooldown, energy, mana}`, all collapsing to mana-default. The doc-48 per-class economies never reach the spatial layer. **The Barbarian-rage build-spend lever — the entire hinge of the Phase-6 STR read — is absent from the population.** Phase 2 corroborated empirically: STR throttles (2.2× vs casters 16-40×) purely because it borrows the wrong economy.

**gandalf ruled** (`gandalf/notes/2026-06-20-instrument-validity-G1-rocket-economy-prerequisite-RULING.md`): (a) the rocket change is REQUIRED — Phase 6 on mana-default is a null instrument; (b) new **Phase R**, parallel to 1-4, **hard-prerequisite to Phase 5** (doc-48 economies move KPM → refitting before they exist forces a second refit, violating the one-refit discipline); (c) Phases 2/3/4 proceed now (done); (d) recompose-first PORT-not-BUILD with one guard (bc_target round-trip must thread); (e) G1 mapping HOLDS (the finding revised an implicit assumption beneath the table, not the table). **If Matt declines Phase R → Phase 6 is HELD, not run** (no honest STR read without the economies in the population). G3 split: G3a gated now; G3b re-arms post-Phase-R.

**Ready-to-fire draft dispatch authored:** `dispatches/2026-06-20-rocket-phaseR-reference-economy-hardening-DRAFT.md` (marked DO-NOT-FIRE-until-Matt-authorizes).

### OPEN MATT DECISIONS (the halt wall — both land here)
1. **Phase R scope authorization** (halt-point 3, scope surprise): authorize rocket reference-economy hardening, OR accept Phase 6 STR read is HELD/deferred and Phase 5 refits as explicitly mana-default-only-scoped. No third path runs Phase 6 honestly.
2. **Phase 5 band approval** (halt-point 1): the composed re-baseline produces new bands → jack-ryan structural Gate-2 (G6, BLOCK authority) → Matt decisions-log decision. Gated on #1 (refit on the full-economy population requires Phase R first).

### Hand-back chain if Matt authorizes Phase R
rocket Phase R (doc-48 economies into population) → jack-ryan Gate-2 → gamora re-arms G3b (rage branch materializes on real rage entity) → Phase 5 composed re-baseline (gamora + jack-ryan G6) → Matt band approval → Phase 6 STR fires its rage economy + bleed lever → gandalf rules O1-O4 → feeds the (A)-vs-(B) skill investigation.

### Carryover / standing items
- **60 pre-existing test failures** (rocket-seam config drift: 5-element vs 7-substrate `season_emit`; + star-lord LLM auth; + cycle12 convergence shape) — verified identical on the clean baseline, NOT introduced by this workstream. Relevant if Phase R authorizes rocket work (rocket should be aware of the drift).
- Crypt-Vault Node PoC (2026-06-19 handoff): drax dispatch still awaiting drax session launch (Pattern B, needs open Godot editor) — untouched this session.

### Push gate
All instrument-validity commits (Phases 1-4 engine tags + collab results + qa findings + dispatches + this handoff) are local on `main`, NOT pushed. Awaiting Matt push authorization (ADR-006).
