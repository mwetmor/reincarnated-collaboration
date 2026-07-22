# Dispatch — 2026-07-22 — gamora — SIM CAPACITY: multi-actor / horde (spec-frozen two-step wave)

**Status:** PENDING — FIREABLE. Open a gamora session; it picks this up at session start.
**Gates cleared:** jack-ryan Gate-1 (DESIGN-MODE, dispatch review) **PASS-WITH-AMENDMENTS** 2026-07-22 — all 5 amendments folded (W2-red-flag lifecycle timing · A3 formation-necessity boundary · #1.1 named host-bounds threshold · Disc #18 baseline-before-prereg · checkable band-refit provenance). NOTE: this cleared the *dispatch*; gamora's step-(a) *spec* gets its own separate jack-ryan Gate-1 (the internal gate below).
**From:** knight-rider (Lane-2 conductor; run-state `agentic_orchestration/knight-rider/sim-capacity-lane2-run-state.md`)
**To:** gamora (simulation / spatial gauntlet / calibration)
**Approved by:** Matt — fire-word on gandalf brief `agentic_orchestration/gandalf/briefs/2026-07-22-parallel-kr-lanes-emission-sim.md` §3 (2026-07-22)
**Estimated effort:** multi-day (Pattern B). Step (a) audit+spec ~0.5–1 day; step (b) build behind the checked spec ~2–4 days depending on the buildable envelope the spec certifies.
**Pattern:** B — spec-first, build-behind-checked-spec. **This is the desirable-run-pattern F4 "fork profile technical-not-design → spec-frozen build wave (KR-conducted)" case** (brief §1). The BUILD is engine production code (yours); the DESIGN decisions are NOT yours — they route to gandalf (Pattern-A) / Matt (see riders).

**Acceptance (wave-level):** a jack-ryan-Gate-1-checked capacity-extension spec exists on disk (step a), and the spec-certified buildable envelope is built + smoke-green + jack-ryan Gate-2-checked (step b). Design-gated extensions are surfaced with their gating ruling named, NOT built in this lane.

---

## THE TWO-STEP STRUCTURE (read this first — the internal gate is load-bearing)

This is **not** one build dispatch. It is an **audit → spec → GATE → build** sequence with an internal jack-ryan Gate-1 you must clear before any production code lands:

1. **STEP (a) AUDIT+SPEC.** You audit current-state sim capacity against the I.2 end-state extensions + formation topology, and author a **capacity-extension spec** that partitions every extension into **BUILDABLE-SPEC-FROZEN** (technical, no open design question) vs **DESIGN-GATED** (needs a gandalf temperature-definition ruling or a Matt persistence ruling before it can be specced-to-build). NO production code in step (a).
2. **INTERNAL GATE.** Route the spec to **jack-ryan (Gate-1, DESIGN-MODE)**. This is the "jack-ryan-checked" in the fire-word. Do not proceed to step (b) until PASS or PASS-WITH-AMENDMENTS (build to the amendments). A BLOCK is a terminal HALT → route to KR.
3. **STEP (b) BUILD** — only the spec's BUILDABLE-SPEC-FROZEN envelope, exactly as jack-ryan cleared it. Design-gated items do NOT get built here; they leave the lane as routed work (§ Coordination riders).
4. **Gate-2** on the build (per brief §3 twin: "Gate-2-checked").

**Why spec-frozen matters:** the point of this pattern is that KR conducts a build behind a *frozen* spec so no design drift enters through the build. If the audit finds an extension needs a design decision, that decision is elicited THROUGH the proper seam (gandalf/Matt) and folded into the spec BEFORE the build — never invented at the code face.

---

## Context

The v2 loop moved the sim's finish line (I.3). The sole fight entry `spatial_engine.py:2944` takes ONE player class vs a list of monster dicts — **no second-kit slot**, and all 6 arena shells cap **≤8 concurrent** (`arena.py`; `endgame_encounter_catalog.py` MobSpec max 8; `mean_mobs_killed` golden-master 8.0). The 2026-06-21 defensive-axis close + offensive bands are calibrated **at ≤8 concurrent only**. Meanwhile I.2 names three v2-driven instrument extensions the sim was never built to measure — **horde-density (≥50 concurrent)**, **matchup-temperature**, **per-kit level-scaling** — and the encounter grammar work needs **formation topology** (swarm / volley-fan / lane / emplacement). IV.2 #2 has already clocked `SCENARIO_OVERRUN` + horde KPM-bands as a gap with a lock-in clock on it (every band frozen at 8-concurrent is a band we may re-litigate).

Your job in step (a) is to tell us — **grounded in the actual sim source, not the spec's prose** — what each of those extensions actually requires, which are buildable spec-frozen right now, and which are blocked on a design ruling. Then build the cleared envelope.

## Required reading before starting

1. `canonical/current-to-end-state/current-to-end-state-engine.md` — **PART I §I.1/§I.2/§I.3** (current→end-state→gap for the battle sim), **PART III §III.1** (kit-vs-kit matchup-temperature — the gandalf lean is a temperature SIGNAL, not a kit-vs-kit fight), **§III.1b** (multi-actor player-side proxy path is BUILT — W1+W2; the second-kit slot for kit-vs-kit is a *separate* unbuilt item), **§III.2** (per-kit level model + the §12 checkpoint-validation method), **§III.3** (horde density 8→50-150, `SCENARIO_OVERRUN`, the M1 positioning primitive, the defensive-axis re-fit), **PART IV §IV.1/§IV.2** (owner map + forward queue; #1 multi-actor consult is gandalf-seam, #2 is this gap).
2. `agentic_orchestration/gandalf/briefs/2026-07-22-parallel-kr-lanes-emission-sim.md` — §3 (this lane's charter) + §4 (T3-V7 one-way coupling law).
3. `agentic_orchestration/gandalf/notes/2026-07-22-tier3-encounter-geometry-run-charter.md` — **W2 row** (line ~54: "fit layer + MESO/MICRO sim scenarios; **Harness-expressiveness risk surfaces HERE by design** — if the sim cannot express formation topology: red-flag ping + honorable fallback") + **Q1 framing audit** (line ~82: "gamora harness can express formation topology — **NOT VERIFIED**") + **T3-V7** (line ~76). **READ-ONLY.** This is a Tier-3 artifact; you do not write into it.
4. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — **#1** (math-before-code) + **#1.1** (pre-fire resource-bounds projection — LOAD-BEARING here; see below), **#2** (smoke-test) + **#2.1** (smoke-test resource-scaling rehearsal), **#12** (semantic-shifting), **#18** (baseline-before-prereg — the horde KPM-band re-fit is a fresh empirical fit at a new density; pin a neutral baseline before the bands are declared), **#20** (density-based row-duplication prohibition — relevant to any horde-weighting), **#62** (parallel-tree hygiene + stale-line-ref discipline).
5. Your own `simulation/AGENT_STATE.md` + the just-closed Wave-B dispatch (`dispatches/2026-07-22-wave-b-reservation-aura-gamora-sim.md`) for the current HEAD, the positioned-ally / ground-tether primitives, and the S6 cert HALT pattern (a clean precedent for surfacing a design fork rather than patching it).

**Line refs in the spec are anchors, not addresses** (Disc #62 — they go stale). Re-locate every cited site by symbol/grep at HEAD before you reason about it.

## Math-before-code (Disc #1 + #1.1 — mandatory in step (a), before any step (b) code)

- **#1.1 pre-fire resource-bounds projection is the single most load-bearing math item in this dispatch.** The horde regime is a **6–19× density jump** (8 → 50, up to 150). The audit MUST project: per-tick compute cost at ≥50 concurrent (entity-pair interactions, nav, AoE membership re-tests, formation maintenance), peak memory, and the full-gauntlet wall-clock at the target density — and **verify against host RAM before any ≥50-concurrent run fires.** A naive O(N²) pair loop that was invisible at N=8 is ~40× heavier at N=50 and ~350× at N=150. **The projection MUST state the actual host RAM + wall-clock ceiling it checks against and name the concurrency at which the current entity-interaction model breaks that ceiling — the ≥50-run fire/no-fire decision is a checkable number, not an assertion.** If the projection shows the harness cannot run ≥50 concurrent within host bounds, THAT is a first-class audit finding (it may itself be the W2 harness-expressiveness red-flag, arriving from this side first).
- **#1 math-before-code** for every primitive the spec authorizes to build: the M1 horde-positioning primitive (gather/funnel/kite geometry), each formation-topology construction (swarm / volley-fan / lane / emplacement), the `SCENARIO_OVERRUN` scenario shell, and the horde KPM-band re-fit method (the ≥50 bands are their OWN bands — measure them, do not scale the 8-concurrent bands).
- **Band re-fit is empirical, not assumed** (III.3): `SCENARIO_OVERRUN` floors at the **comfortable-band ≥50, not the ceiling** — "measure, don't assume" the peak. Expect a defensive-axis re-fit (50 swarm @ 0.20 ≈ 6× the incoming the 2026-06-21 bands were fit against). The 2026-06-21 close is valid *within its measured band*; the band moved.

## Cross-seam contract change? (Principle 6 gate — knight-rider completes this at authoring time)

**Likely YES, to be confirmed by the step-(a) audit.** A new `SCENARIO_OVERRUN` scenario and horde KPM-bands will probably add scenario-identity + band fields to the fight/telemetry surface (the gamora → star-lord boundary). Formation topology may add an encounter-composition field. **The step-(a) spec MUST make the determination explicit** and, if any inter-seam fixture field is added/renamed, the step-(b) build MUST include:
- `Round-trip smoke: <production-path fixture exercising the SCENARIO_OVERRUN telemetry emission through the star-lord consumer boundary + field-presence check>` **AND** a `MIGRATION.md` at the gamora→star-lord boundary (ADR-004).
- If the audit finds NO inter-seam field change (all additions sim-internal): `Round-trip: not applicable because <explicit reason>` — stated in the spec.

Silence on this is a Gate-1 BLOCK (REVIEW_PROCESS.md Principle 6). Resolve it in step (a).

---

## STEP (a) — AUDIT + SPEC (deliverable: `simulation/spec/sim-capacity-extension-spec-2026-07-22.md` or your seam's spec home)

Audit each extension against **live sim source** and partition it. For every extension, the spec states: (i) what the end-state asks, (ii) what the sim does today (cited by symbol), (iii) the gap, (iv) **BUILDABLE-SPEC-FROZEN or DESIGN-GATED**, (v) if design-gated, the exact ruling owed and its owner, (vi) if buildable, the primitive(s) + math-note + smoke + resource-bounds + band-refit plan.

**A1 — Multi-actor, disentangled into its two faces (the audit's central move).** "Multi-actor" is TWO different asks with different dispositions — do not conflate them:
- **A1-enemy (horde/formation side) — expected BUILDABLE-SPEC-FROZEN.** Many hostiles + formations on the enemy side. This is III.3 + the encounter-grammar formation need. No open design question at the *sim-capacity* level (the encounter-DESIGN grammar is Tier-3's, not yours — you build the capacity to *express* it).
- **A1-player (second-kit slot) — expected DESIGN-GATED.** `spatial_engine.py:2944` is a single fight-entry: one player class vs monster dicts, **no second player-KIT slot** (III.1b confirms this is a distinct unbuilt item; the built W1/W2 proxy path is allegiance-heterogeneous but is NOT a second *kit* slot). **BUT** per III.1 the gandalf lean is that **matchup-temperature is a SIGNAL (a measurement over already-emitted features / a QD-grouping matrix), NOT a kit-vs-kit fight** — so a second-kit fight slot may not be needed at all. **The audit characterizes the architectural cost of a second-kit fight slot IF one were required, but does NOT decide whether temperature needs it** — that is the gandalf temperature-definition ruling (III.1 owner: gamora+star-lord scoping, gandalf design-fit). Route it (see riders).

**A2 — Horde density (III.3) — the spec-frozen buildable core.** Audit: current ≤8 ceiling (6 shells; catalog max 8; `mean_mobs_killed` 8.0), the missing horde/gather primitive (`arena.py:298-365` player-AI closes on nearest mob; no "reposition to GATHER into the AoE" primitive). Spec: `SCENARIO_OVERRUN` (7th scenario, ≥50 floor), the **M1 horde-positioning primitive** (gather/funnel/kite — the prerequisite and likely the longer pole), horde-regime KPM bands (their own bands), defensive-axis re-fit. Include the #1.1 resource-bounds projection as a named section.

**A3 — Formation topology (swarm / volley-fan / lane / emplacement) — BUILDABLE, but this is the W2 named-risk probe.** Audit whether the sim can *express* each of the four formations (positional construction + maintenance under nav). **This is the Tier-3 Q1 unverified assumption ("gamora harness can express formation topology — NOT VERIFIED").** If the harness can express all four: the spec says so and this pre-hedges the W2 risk. If it cannot express one or more: that is a red-flag finding — the spec names the harness-extension needed as a requirement (it becomes buildable-in-this-lane work), NOT a new lane (T3-V7). **gamora builds expressive capacity for the four named formations (swarm / volley-fan / lane / emplacement); which formations the encounter grammar actually *requires* is Tier-3 W1's design call, not this lane's — do not prune the four based on a judgment about need.**

**A4 — Matchup-temperature (III.1) — expected DESIGN-GATED.** Audit: sim does global kit-vs-control only, no kit-vs-kit path; the ~24×24 QD-grouping matchup matrix is a MEASURE, and whether the BC axes align with matchup axes is [OPEN]. The spec characterizes what a temperature *measurement* would require sim-side (which queries produce the cells + inversion probability masses) but does NOT define temperature — that is the gandalf design-fit ruling. Name it as the gate.

**A5 — Per-kit level-scaling (III.2) — expected DESIGN-GATED on a Matt ruling.** Audit: sim validates at a single fixed L50 point, flat-skill assumption (`balance_loop.py:1935`). The §12 method is bounded checkpoint-validation (representative grouping-level sample in-band across ~4-6 milestones 1→50; skill-unlock is the lumpy non-monotonic axis — spend the sim budget there). **The +3-becoming band is gated on the flag #2 persistence-contract Matt ruling** ("what banks across the roguelite reset"). The spec characterizes the checkpoint-validation harness but flags that the acceptance criteria cannot be frozen until Matt rules. Likely DESIGN-GATED (or partial: the checkpoint harness scaffold may be buildable while the +3 band waits).

**A6 — `SCENARIO_OVERRUN` + horde KPM-bands (IV.2 #2 — already clocked).** Fold into A2/A3 as the concrete scenario + band deliverables. This is the item with a lock-in clock.

**Spec output requirements:** a clear BUILDABLE-SPEC-FROZEN vs DESIGN-GATED partition table; the Principle-6 cross-seam determination; the #1.1 resource-bounds projection; the math-note plan for each buildable primitive; and the harness-expressiveness verdict on formation topology (the W2 pre-hedge). **Then route to jack-ryan Gate-1.**

## INTERNAL GATE — jack-ryan Gate-1 (DESIGN-MODE) on your spec

Route the spec to jack-ryan. Do not fire step (b) until PASS / PASS-WITH-AMENDMENTS. Build to any amendments. A BLOCK → terminal HALT, route to KR (do not patch around it).

## STEP (b) — BUILD (only the jack-ryan-cleared BUILDABLE-SPEC-FROZEN envelope)

- Build exactly what the checked spec certifies buildable — no more. The design-gated extensions (A1-player second-kit slot, A4 temperature definition, A5 +3-becoming band) are NOT built in this lane; they leave as routed work.
- **math-note-first per primitive** (Disc #1), authored before code.
- **Smoke per primitive** (Disc #2) **+ resource-scaling rehearsal** (Disc #2.1 — the smoke gates MUST include a resource-scaling step: prove the primitive runs at the ≥50-concurrent target within host bounds before the full band-refit run fires).
- **Band re-fit empirically** at the `SCENARIO_OVERRUN` ≥50 floor (measure, don't assume). **Pin a neutral baseline before declaring the bands (Disc #18)**; the completion record cites the measurement run (seed + telemetry artifact) the bands were fit against, so the fit is provenance-verifiable.
- **MIGRATION.md** at the gamora→star-lord boundary if the audit found an inter-seam field change (ADR-004) + the round-trip smoke.
- Tag per slice (`gamora/v<next>-sim-capacity-...`); prove pre-existing HEAD failures via git-stash; append a completion record per slice.
- **Gate-2** on the build (per brief §3).

---

## Coordination riders (BINDING)

1. **T3-V7 one-way coupling (Tier-3 → this lane only).** Tier-3 W2 (fit-layer + MESO/MICRO scenario compute) surfaces harness-expressiveness findings. **Any W2 red-flag routes INTO this lane's spec as requirements — never a new lane.** Your A3 formation-topology probe is the *pre-hedge*: if this lane lands formation-topology capacity before W2 fires, the charter's named risk is retired; if W2 fires the red-flag first, its honorable-fallback harness-extension spec routes here. **Coupling is one-way — you read Tier-3's run-state for W2 findings (`gandalf/notes/2026-07-22-tier3-encounter-geometry-run-state.md`, READ-ONLY); you never write into any Tier-3 artifact.**
   - **Lifecycle timing (Gate-1 amendment):** if a W2 red-flag arrives **before** step-(a) Gate-1 clears, fold it into the spec under review. If it arrives **after** Gate-1 has cleared but before step (b) completes, the incoming requirement **re-enters step (a) as a spec amendment and requires a fresh jack-ryan Gate-1 on the delta before it is built** — it does not enter the build unreviewed. Surface the arrival to KR either way.
2. **The multi-actor DESIGN consult (IV.2 #1) stays gandalf-seam.** When the spec hits a point that needs a design decision — the matchup-temperature *definition* (A4), whether kit-vs-kit is a fight or a signal (A1-player), the horde-regime KPM-band *methodology* acceptance shape — **request Pattern-A input from gandalf** (surface it to KR; KR routes the Pattern-A consult). Do NOT invent the design decision at the sim seam. The technical *capacity* is yours; the design *definition* is gandalf's.
3. **The A5 +3-becoming band is gated on the Matt flag-#2 persistence ruling** — surface it to KR if the audit shows the per-kit-level checkpoint harness is otherwise buildable; KR decides whether to build the scaffold now or defer the whole A5 item behind Matt's ruling.
4. **Namespace discipline.** Own dispatch namespace (this file + your seam's spec/math/AGENT_STATE). **No writes into Tier-3 run files.** If KR lanes run parallel on the meta-repo, distinct namespaces + no cross-lane writes (Tier-3 charter §meta-repo-contention).

## Scope

- [ ] Step (a): capacity-extension spec authored with the BUILDABLE-SPEC-FROZEN vs DESIGN-GATED partition, #1.1 resource-bounds projection, Principle-6 cross-seam determination, formation-topology harness-expressiveness verdict (W2 pre-hedge)
- [ ] Internal gate: jack-ryan Gate-1 (DESIGN-MODE) PASS / PASS-WITH-AMENDMENTS on the spec
- [ ] Step (b): the cleared buildable envelope built — `SCENARIO_OVERRUN` (≥50 floor), M1 horde-positioning primitive, formation-topology construction (as the audit clears), horde KPM-band + defensive-axis empirical re-fit
- [ ] math-note-first per primitive (Disc #1)
- [ ] Smoke per primitive + resource-scaling rehearsal (Disc #2 + #2.1)
- [ ] MIGRATION.md + round-trip smoke IF the audit found a cross-seam field change (else not-applicable justification in the spec)
- [ ] AGENT_STATE.md updated at session end
- [ ] Design-gated extensions surfaced to KR with their gating ruling + owner named (routed, NOT built)
- [ ] Gate-2 on the build
- [ ] Tags per slice

## Acceptance criteria

- [ ] The spec exists on disk and partitions all five audited extensions (A1-enemy, A1-player, A2/A6 horde, A3 formation, A4 temperature, A5 per-kit-level) into buildable-spec-frozen vs design-gated, each with owner/gate named
- [ ] jack-ryan Gate-1 cleared the spec (record in `qa/pending/`)
- [ ] The buildable envelope is built, smoke-green with a resource-scaling rehearsal at ≥50 concurrent proving host-bounds compliance, and the horde bands are empirically re-fit — the spec/completion-record cites the `SCENARIO_OVERRUN` measurement run (seed + telemetry artifact) the bands were fit against, so the fit is provenance-verifiable and demonstrably not scaled from the 8-concurrent bands
- [ ] Formation-topology harness-expressiveness verdict is recorded (W2 pre-hedge satisfied or the red-flag named as a spec requirement)
- [ ] Round-trip smoke: `<SCENARIO_OVERRUN telemetry fixture through the star-lord consumer boundary + field-presence check>` OR Round-trip: not applicable because the audit found all additions sim-internal (stated in the spec)
- [ ] jack-ryan Gate-2 on the build

## Out of scope (explicit non-goals)

- **The A1-player second-kit fight slot** — do not build a kit-vs-kit fight path. Characterize its cost in the audit only; the temperature-definition ruling (III.1, gandalf) decides whether it is even needed.
- **The matchup-temperature measurement definition (A4)** — gandalf design-fit; not defined at the sim seam.
- **The +3-becoming acceptance band (A5)** — gated on the Matt flag-#2 persistence ruling.
- **Any encounter-DESIGN grammar** (deck archetypes, disposition parameters, verb sets) — that is Tier-3 W1's, not this lane's. You build the *capacity to express* formations; you do not author the encounter grammar.
- **Any write into Tier-3 run files.**
- **Emission-side wiring** — that is Lane-1 (star-lord), a separate dispatch.
- **Over-correcting the horde bands into the ceiling** — `SCENARIO_OVERRUN` floors at the comfortable-band ≥50, not the 150 peak (measure, don't assume).

## Open questions for the agent to resolve (in the audit, then route the design ones)

- Does the ≥50-concurrent regime clear the host-RAM / wall-clock bound with the current entity-interaction model, or does the audit surface a harness-compute red-flag (possibly the W2 risk arriving from this side)? — resolve empirically in the #1.1 projection.
- Is any `SCENARIO_OVERRUN` / KPM-band field a cross-seam fixture change (→ MIGRATION + round-trip), or all sim-internal? — resolve in the Principle-6 determination.
- Can the harness express all four formations (swarm / volley-fan / lane / emplacement), or is a harness-extension needed for one or more? — resolve in A3 (the W2 pre-hedge).
- Which design decisions must be routed to gandalf (Pattern-A) before the spec can freeze, and which to Matt (flag #2)? — enumerate and route through KR.

## References

- `current-to-end-state-engine.md` §I.1/I.2/I.3, §III.1, §III.1b, §III.2, §III.3, §IV.1, §IV.2 (esp. #1, #2)
- gandalf brief `2026-07-22-parallel-kr-lanes-emission-sim.md` §3 + §4 (T3-V7)
- Tier-3 charter `gandalf/notes/2026-07-22-tier3-encounter-geometry-run-charter.md` — W2 row, Q1 framing audit, T3-V7 (READ-ONLY)
- engineering-disciplines #1 / #1.1 / #2 / #2.1 / #12 / #18 / #20 / #62
- Prior calibration precedent: proxy-fight calibration (`gamora/v-proxy-fight-calibration-1` @ `abb010d`); 2026-06-21 G-C defensive-axis close (decisions-log 4562-4649, calibrated ≤8 concurrent — the band that moved)

## Commit / push

Auto-commit in-scope work-products (spec, math-notes, smoke scripts, code). **PUSH: ask KR/Matt** — no per-cycle push pattern is established for this lane yet (unlike Wave-B). Surface a push-request at each slice boundary unless KR relays a Matt push-pattern authorization.
