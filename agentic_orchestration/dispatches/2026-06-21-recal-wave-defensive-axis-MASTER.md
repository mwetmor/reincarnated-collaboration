> # ⛔ HELD — SUPERSEDED SPINE — DO NOT PUBLISH / DO NOT PICK UP
> **Matt LOCKED typed resistances 2026-06-21.** This MASTER is built on the SUPERSEDED flat/typeless spine and CANNOT publish as-is. The corrected design of record is `agentic_orchestration/gandalf/notes/2026-06-21-typed-resistance-meta-design-half.md` (commit `c85261e`).
> **No agent should pick up this dispatch or split it into per-seam files.** It re-drafts only after Stage-0a (gamora resolver spike) PASS + Stage-0b (typed-resistance design-half) jack-ryan Gate-1 PASS + Matt publish-go.
> **What survives (salvage):** threat SHAPE (heavy-slow boss / light-variance swarm), trash<boss, emission-held-until-joint-close, "skills into skill-less mobs" (sharpened to TYPED), star-lord additive telemetry (now richer: death-cause-with-element).
> **What is superseded:** the flat-constant spine, constraint-1 anchor knob-set (`MOB_DAMAGE_SCALE=4.0` / `armor 0.76` — INVALID under the resolver; re-derive from scratch), the "tune the flat armor_factor" framing throughout, the threat-spec typeless ruling.
> **GUARDS that carry verbatim into the re-draft:** ANTI-TAX (resistance is reward-for-matching, NEVER a mandatory cap — if the only survival path is match-capping the element, the knob-set FAILS); trash<boss always; content emission HELD until the two-axis joint close; flat anchor INVALID.

# Dispatch — 2026-06-21 — MULTI-SEAM — defensive-axis recalibration wave (MASTER) [HELD — SUPERSEDED]

**From:** knight-rider
**To:** rocket → gamora → star-lord (sequenced); jack-ryan (Gate-1 this dispatch, Gate-2 each build)
**Approved by:** Matt 2026-06-21 — ruled death a core pillar (disposition B); authorized the recal as its own wave; authorized close-disposition (b) (offensive bands banked PROVISIONAL, re-rate-pending this wave). This dispatch sequences the build against that ruled+gated target.
**Estimated effort:** ~4 waves across 3 seams (asymmetric). rocket content prereq (~1.5 waves) BLOCKS gamora calibration (~2 waves); star-lord additive telemetry (~0.5 wave) concurrent.
**Acceptance (wave-level):** glass-cannon kit lands in the HEART of ~0.6–0.8 survive+kill (~0.70) at FULL POPULATION; bruiser ~0.95+; homogenization guard re-passes at the production heavy-slow cadence; trash death-rate STRICTLY below boss for every kit profile; offensive bands re-rate ONCE jointly over both axes. **Nothing emits to content until the joint two-axis close.**

> **STATUS GATE:** This MASTER dispatch is the artifact jack-ryan Gate-1's. On Gate-1 PASS + Matt go, knight-rider spawns the per-seam pickup files (`2026-06-21-rocket-…`, `2026-06-21-gamora-…`, `2026-06-21-star-lord-…`) from the per-seam sections below. **Do NOT start the build before Gate-1 PASS + Matt go.** This is a future-authorized production wave; the design is ruled but the BUILD is not yet released.

---

## Context (why this wave, what it closes)

The combat instrument grades every kit on a boss gate that has been running in a **degenerate 1-D mode**: survival = 1.000 instrument-wide (gamora measured all six shells, tier_1-bypassed, elite_pack included — `defensive-axis-calibration-diagnose-2026-06-21.md`). The player never dies, so the only failure is the 240s enrage clock — the survive limb of the `survive AND kill` gate is vacuous. A defensively-fragile kit gets blessed (offensively in-band, kills in time) and is a lie the moment a real death channel exists.

Matt RULED (B): **death is a core pillar.** "There is no point in playing a game where you cannot die, and all game data is pushed into the battle sim." The glass-cannon diagnostic shifted from go/no-go to **calibration anchor**: the recal is proven REACHABLE (knob-set found) and the homogenization guard proven HOLDS — so restoring the defensive axis is a committed wave, not a question. This dispatch builds it.

**The missed layer that makes this partly a CONTENT wave (not a scalar re-fit):** the production endgame boss path builds synthetic mobs with `"skills": []` (`t4_sim_cycling.py:1082`) → zero damage **by construction**, independent of every knob. You cannot restore boss death by turning the armor knob — there is nothing to mitigate. rocket must give the boss/adds a damaging mechanism FIRST; only then does gamora's calibration have a death channel to tune. That dependency is the wave's spine.

This wave's design is fully ruled by two Stage-1 gandalf docs (both Gate-1'd ENDORSE-WITH-CONCERNS, pushed). **The design questions are RULED — this dispatch does NOT re-open them.** It sequences the build.

---

## Required reading before starting (ALL seams)

1. `agentic_orchestration/gandalf/notes/2026-06-21-defensive-axis-recal-encounter-model-ruling.md` — **PART 3 = the nine named constraints (entry conditions).** This is the binding ruling.
2. `agentic_orchestration/gandalf/notes/2026-06-21-monster-offense-threat-design-spec.md` — **§6 = the per-seam buildable handoff.** Build to §6. (§1 = the engine substrate, read first-hand by gandalf + jack-ryan; §2 boss-threat heavy-slow; §3 swarm-threat variance; §5 positional avoidance.)
3. `agentic_orchestration/qa/findings/2026-06-21-threat-design-spec-gate1-design.md` — jack-ryan Gate-1; **CONCERN B1 (heavy-slow guard re-run) is folded into the gamora line below as a RULED ACCEPTANCE TEST.**
4. `~/Games/reincarnated-engine/src/reincarnated/simulation/math/defensive-axis-calibration-diagnose-2026-06-21.md` — the calibration anchor (gamora's own measured substrate).
5. `agentic_orchestration/qa/findings/2026-06-21-defensive-axis-calibration-diagnose-gate2.md` — jack-ryan Gate-2 on the diagnostic (mechanism correction verified; coverage-weak + joint-re-derivation concerns).

---

## The NINE ruled constraints this wave carries (verbatim from encounter-model ruling PART 3)

Every seam honors these; jack-ryan Gate-1's the dispatch against them and Gate-2's each build against them.

1. **Anchor knob-set is the START, not the answer:** `MOB_DAMAGE_SCALE=4.0` (primary enabler), `PLAYER_ARMOR_FACTOR_VS_BOSS≈0.76` (fine dial), `PLAYER_ARMOR_FACTOR_VS_STANDARD=0.85` held for the boss path **but RE-DERIVED for clear shells** (constraint 3). Tune from here against full population.
2. **Calibration target (RULED):** glass cannon in the HEART of ~0.6–0.8 survive+kill (~0.70) at FULL POPULATION; bruiser ~0.95+. Authorized to add per-hit mob-damage variance and/or rely on population HP-spread to soften the cliff into a genuine grade — **the softening is design-intended, not an artifact to engineer around.**
3. **Clear-shell JOINT re-derivation (HARD CONSTRAINT):** `PLAYER_ARMOR_FACTOR_VS_STANDARD` + `MOB_DAMAGE_SCALE` re-derived JOINTLY for clear shells alongside boss knobs — **NO boss-only patch** (it inverts trash-vs-boss). Ordering target: boss = peak graded death-risk; trash death-rate STRICTLY below boss for every kit profile.
4. **Clear-shell death mechanism:** in scope but rare-by-design; **NOT coverage-pressure alone** (it cannot reach fast-AOE kits, by design). Evaluate per-hit variance (preferred) / not-fully-coverable threats (texture). Fallback if no guard-respecting mechanism: **BOSS-ONLY death, logged explicitly** as a scope decision.
5. **Endgame monster-offense DESIGN:** skill-less synthetic mobs (`"skills": []`) — restoring boss death is NOT a knob turn; it requires giving boss/adds a damaging spatial skill. This is monster-offense CONTENT design (rocket). The wave is partly a content wave.
6. **Homogenization guard = RULED ACCEPTANCE CRITERION:** the chosen production knob-set MUST pass gamora's guard sweep — fast kit survives-by-killing where slow kit of IDENTICAL HP/armor dies, AND bruiser survives-by-enduring at the same knob-set. **No mandatory defensive floor. Two viable paths or reject the knob-set.**
7. **Gate-semantics:** boss gate is now `survive AND kill`, both LIVE and GRADED; kit disposition is a 2-D point; offensive bands re-rate ONCE jointly over both axes (NOT two separate refits).
8. **Provisional-bands re-rate:** banked offensive bands are PROVISIONAL; they re-rate over the joint two-axis outcome when this wave lands; the wave's output FEEDS the joint band-finalization. **Content emission stays gated on the joint two-axis close.**
9. **Full-population validation:** the diagnose used a single-kit throwaway fixture; production validation is a FULL-population sweep across the ~0.60-armor headroom. Direction + magnitude robust (analytic TTD/TTK matched measured); width-at-population is the empirical burden.

## The THREE non-negotiable guards (carry into every seam)

- **G-A — Homogenization guard is an ACCEPTANCE CRITERION, not a hope** (constraint 6). Reject any knob-set that forces one armor number.
- **G-B — Trash < boss, always** (constraint 3). Boss = peak death-risk; clear shells strictly below for every kit profile. An inversion (fear the hallway, not the throne room) is a fail.
- **G-C — Content emission HELD until the two-axis joint close** (constraint 8). No offensively-blessed-but-defensively-fragile kit ships before death is real. `_DEFERRED_PROXY_BINS` lift and any 25% emission remain Matt-reserved and separate.

---

## Wave sequencing (the dependency spine)

```
  rocket G1/G2 (content prereq) ──BLOCKS──▶ gamora W1/W2/W3 (calibration)
        │                                          │
        │  (gen→sim bridge soldered)               │
        ▼                                          ▼
  star-lord (additive threat telemetry + MIGRATION) ── concurrent, lands before gamora's full-pop validation needs the field
                                                     │
                                                     ▼
                          jack-ryan Gate-2 each build ──▶ joint two-axis re-rate ──▶ Matt joint-close
```

**Why rocket first (hard block):** gamora cannot calibrate a death channel that does not exist. The boss/adds have no damaging skill today; the swarm has no per-hit variance field. gamora's W2/W3 calibration consumes what rocket emits. rocket G1/G2 land first-or-concurrent; gamora's *calibration* phase starts only once a fighting boss exists in the sim.

---

## PER-SEAM SECTIONS (each becomes a pickup file on Gate-1 PASS)

### ROCKET — content prereq (G1/G2) — BLOCKS gamora

**Build to threat-design-spec §6 (rocket bullet).** Give the endgame boss / elite / synthetic mobs **real skills** (replacing `"skills": []` at `t4_sim_cycling.py:1082`):

- [ ] **Boss-threat content (heavy-slow):** a damaging spatial skill with geometry + `damage_multiplier` + `cooldown_seconds`, on the **HEAVY per-hit × SLOW cadence** profile (few big readable hits — the D3 Rift-Guardian shape that discriminates by HP/armor and produces the spread). The telegraph-mint already shows the danger zone (`spatial_engine.py:744-812`, minted `:1975-1988`) — no new telegraph system.
- [ ] **Geometry constraint (HARD — Gate-1 INFO #2):** emit ONLY wired hit-geometries — `{point, circle, line, cone}`. `burst/ring/nova/wave/chain/arc` fall through to **no-hit / zero damage** (`_compute_aoe_hits` → `return []` at `spatial_engine.py:740-741`). Emitting an unwired geometry mints a **damage-less threat** (silent defect). Do NOT reach for an unwired shape — it would be net-new engine, contradicting recompose-first.
- [ ] **Swarm-threat content:** surface a **per-hit variance field** for swarm candidate (a) (the preferred clear-shell death mechanism — burst spikes a high-HP kit absorbs and a paper kit doesn't). Optionally a small fraction of `ranged_kite`/`cast_at_range` behavior for candidate (b) texture.
- [ ] **gen→sim vocabulary bridge:** the monster-offense vocabulary emitted into the pipes §1 confirmed exist (gen speaks the content; sim's mob-cast branch `:1933-2001` consumes `damage_multiplier`/`geometry`/`cooldown_seconds`). Verify the emitted dict keys match what the cast branch reads — this is the seam that was specified at both ends and must be soldered in the middle.

**Math-before-code:** document the per-archetype magnitude SHAPE you emit (heavy-slow vs light-variance ranges) as a math-note BEFORE wiring; gamora tunes the exact constants, but rocket's emitted ranges set the envelope. SHAPE is gandalf-ruled (§4): boss = HEAVY×SLOW, swarm = LIGHT+VARIANCE, same `MOB_DAMAGE_SCALE`, opposite ends of the per-hit×cadence plane.

**Out of scope for rocket:** setting exact production constants (gamora's lane); the calibration sweep; the emission schema lift (`_DEFERRED_PROXY_BINS` is a different, Matt-reserved decision — not this wave).

**Cross-seam:** emitting new mob-skill keys into the synthetic-mob dict IS a gen→sim contract surface. Write MIGRATION.md (rocket → gamora). Round-trip smoke: build a synthetic boss with the emitted skill, step it through `spatial_engine` one tick, assert the cast branch fires and applies damage (proves the seam is soldered, not just specified).

### GAMORA — calibration (W1/W2/W3) — depends on rocket

**Build to threat-design-spec §6 (gamora bullet) + the nine constraints.** Tune magnitudes against the ruled spread target. The five gamora deliverables:

- [ ] **Calibrate the spread:** per-archetype `damage_multiplier` × cadence against the target — glass cannon HEART of ~0.6–0.8 (~0.70) at FULL POPULATION, bruiser ~0.95+. Start from the validated anchor `MOB_DAMAGE_SCALE=4.0`, `PLAYER_ARMOR_FACTOR_VS_BOSS≈0.76`, `PLAYER_ARMOR_FACTOR_VS_STANDARD=0.85` (boss path). The anchor is the START, not the answer (constraint 1).
- [ ] **HEAVY-SLOW guard RE-RUN (RULED ACCEPTANCE TEST — jack-ryan CONCERN B1, folded verbatim):** the homogenization guard sweep that proved two-viable-paths was run at a **FAST chip-stream cadence** (`circle, dm=1.0, cooldown_seconds=2.0` — the throwaway fixture). That result **does NOT transfer** to the heavy-slow profile this wave rules. **RE-RUN the guard sweep at the chosen production heavy-slow per-hit × cadence:** a fast kit must survive-by-killing where a slow kit of IDENTICAL HP/armor dies, AND the bruiser must survive-by-enduring — at the heavy-slow profile, not inherited from the 2s sweep. **PLUS a one-shot check:** no single slam may one-shot a glass-pole kit at the band-center (the PoE-rip boundary §2 forbids). If heavy-slow tips into one-shot, soften cadence/per-hit toward the band until BOTH the guard and the one-shot check hold. **The heavy-slow→guard transfer is unproven; it is your empirical burden, not an assumption.**
- [ ] **Wire per-hit variance to the MOB death channel (cliff-softener):** the ±variance primitive exists on the **player-attacker** resolver path (`:1344`, `:1877`) but the **mob→player death channel** (`:1946-1952`) is a separate FLAT branch. Wiring variance to the mob path is a **small mob-path addition** (reuse the existing variance machinery, point it at the mob damage line) — NOT zero-new-code, but well-precedented. This is the §2.1 cliff-softener (turns the binary safe/dead into a graded slope) AND swarm candidate (a)'s mechanism.
- [ ] **JOINT clear-shell re-derivation (HARD CONSTRAINT 3):** re-derive `PLAYER_ARMOR_FACTOR_VS_STANDARD` + `MOB_DAMAGE_SCALE` JOINTLY for clear shells alongside the boss knobs. **NO boss-only patch** (it inverts trash-vs-boss — clear shells carry 3× the boss's per-hit damage; a global mob-scale crank makes trash lethal). Ordering target: boss peak, trash STRICTLY below for every kit profile. Per Gate-2 carried concern: coverage-pressure is a WEAK clear-shell death lever vs fast-AOE — do NOT crank coverage; deliver clear-shell death via per-hit variance per constraint 4. Boss-only death is the LOGGED fallback if no guard-respecting clear-shell mechanism lands.
- [ ] **Full-population validation (constraint 9):** the heavy-slow + variance profiles are BOTH unmeasured at population scale today — validate against a FULL-population sweep across the ~0.60-armor headroom, not the single-kit throwaway. Realized band WIDTH at production is the empirical burden.
- [ ] **Two-axis joint re-rate (constraint 7/8):** the boss gate is now `survive AND kill`, both graded. Re-rate the banked PROVISIONAL offensive bands ONCE, JOINTLY, over both axes — NOT offense-then-defense in two separate refits (prevents a double re-bank; preserves the single-tail-refit discipline). This output FEEDS the joint band-finalization. **Do NOT finalize/emit — finalization is the joint close gated on Matt.**

**Math-before-code (Discipline #1):** math-note the TTD/TTK-vs-cadence derivation for the heavy-slow profile BEFORE the calibration sweep — the diagnostic established direction+magnitude analytically and they matched measured; carry that forward to predict where heavy-slow tips into one-shot, so the sweep is targeted not blind. Cite the diagnostic's §4.5/§4.7.

**Single-parameter sweep isolation (Discipline #24):** when sweeping per-hit × cadence × armor, isolate the swept parameter per run; do not co-vary the spread-target levers and the guard levers in one sweep.

**Seed hygiene (Discipline #3):** prior runs consumed bases through 46M+. Use a DISJOINT base for this wave — **assign 47M+**; keep disjoint from the 700k–46M range.

**Out of scope for gamora:** monster-offense content emission (rocket's lane — gamora consumes it); the encounter-model SHAPE (gandalf-ruled — do NOT re-open); the band FINALIZATION/emission (Matt-gated joint close); any explicit dodge/reaction model (§5 ruled positional-only; explicit telegraph-reaction is a named FUTURE fork, not this wave).

**Cross-seam:** restoring the survive limb makes the fight_log's survive outcome a live, varying signal; new per-hit-variance + death-channel fields may surface. Coordinate MIGRATION.md with star-lord. Round-trip smoke: a full-population fight that produces a non-trivial death → assert the survive-rate + death-cause fields land in the export packet star-lord consumes.

### STAR-LORD — additive threat telemetry — concurrent

**Build to threat-design-spec §6 (telemetry) + proxy-packet §3 (telemetry row, same texture).**

- [ ] One **additive** telemetry field capturing the now-live death channel — candidate: `mob_damage_dealt_to_player` and/or `player_death_cause` / per-shell survive-rate — star-lord's call on exact shape at build, but it must make the restored survive axis OBSERVABLE in the export packet (today survival=1.000 is invisible because nothing dies).
- [ ] **Additive only** — no field renamed/removed; existing consumers byte-identical. This is the discipline that keeps the offensive instrument's banked artifacts intact.
- [ ] **MIGRATION.md** (star-lord ↔ gamora boundary, ADR-004) — the field is written by the sim's death channel and read by export; document the contract.

**Cross-seam (Principle 6 — round-trip REQUIRED):** this dispatch ADDS a fight_log/telemetry field. Round-trip smoke: production-path fight that kills the player → assert the new field is present and populated through the gamora→star-lord boundary into the season JSON. (This is a YES on the Principle 6 gate — silence would be a Gate-1 BLOCK.)

**Out of scope for star-lord:** the `_DEFERRED_PROXY_BINS` lift / 25% emission (Matt-reserved, separate); any schema change beyond the additive threat field.

### JACK-RYAN — Gate-1 (this dispatch) + Gate-2 (each build)

- [ ] **Gate-1 DESIGN-MODE on THIS MASTER dispatch** (before knight-rider publishes the per-seam pickup files): verify the sequencing respects all nine constraints, the three guards are carried verbatim, the B1 heavy-slow guard re-run is folded into the gamora line as an acceptance test (not inherited), the rocket geometry constraint is hard, no ruled design question is re-opened, and the cross-seam Principle-6 round-trip clauses are present on rocket/gamora/star-lord lines.
- [ ] **Gate-2 DEV-MODE on each seam build** in sequence: rocket content (is the seam soldered? does the cast branch fire?), gamora calibration (does the heavy-slow guard RE-PASS first-hand? is the clear-shell re-derivation JOINT, not boss-only? does trash stay strictly below boss? is the re-rate ONE joint refit?), star-lord telemetry (round-trip present?).

---

## Cross-seam contract change? (Principle 6 gate — knight-rider completed at authoring)

**YES.** This wave adds/modifies inter-seam fixture dicts on multiple boundaries:
- rocket → gamora: new mob-skill keys on the synthetic-mob dict (gen→sim bridge).
- gamora → star-lord: live survive-outcome + per-hit-variance + death-cause fields on the fight_log.
- star-lord export: additive threat telemetry field on the season JSON.

**Each per-seam section above carries its required round-trip smoke clause + MIGRATION.md requirement.** No seam may tag without its round-trip smoke (or an explicit not-applicable justification, which does not apply here — all three boundaries change).

## Out of scope (wave-level explicit non-goals)

- The `_DEFERRED_PROXY_BINS` lift and any 25% proxy emission — **separate Matt-reserved decision**, not unlocked by this wave.
- Proxy/summoner Wave-3 — it INHERITS this real death channel (encounter-model ruling §2.4), but is a separate downstream wave, not built here.
- An explicit dodge / telegraph-reaction model — §5 ruled positional-only; explicit reaction is a named FUTURE fork.
- Re-opening any ruled design question (targets, gate-semantics, clear-shell scope, threat vocabulary, avoidance model) — all RULED in the two Stage-1 docs.
- Band FINALIZATION / content emission — Matt-gated joint two-axis close, AFTER this wave's output feeds the re-rate.

## Open questions the build resolves (and documents)

- **gamora:** exact heavy-slow per-hit × cadence at which the guard re-passes AND no one-shot — the band-center tuning. Document in a math-note.
- **gamora:** whether clear-shell death is deliverable via per-hit variance inside the guard+ordering, OR the boss-only fallback fires (constraint 4) — log the decision either way.
- **rocket:** exact emitted magnitude envelope (gamora tunes within it) and which mob roles carry the heavy-slow boss skill vs the swarm variance.
- **star-lord:** exact additive field shape (survive-rate vs death-cause vs raw mob-damage).

## References

- Encounter-model ruling (nine constraints): `agentic_orchestration/gandalf/notes/2026-06-21-defensive-axis-recal-encounter-model-ruling.md`
- Threat-design spec (§6 handoff): `agentic_orchestration/gandalf/notes/2026-06-21-monster-offense-threat-design-spec.md`
- Threat-spec Gate-1 (B1 acceptance test): `agentic_orchestration/qa/findings/2026-06-21-threat-design-spec-gate1-design.md`
- Calibration anchor (diagnostic): `~/Games/reincarnated-engine/src/reincarnated/simulation/math/defensive-axis-calibration-diagnose-2026-06-21.md`
- Diagnostic Gate-2 (mechanism correction + carried concerns): `agentic_orchestration/qa/findings/2026-06-21-defensive-axis-calibration-diagnose-gate2.md`
- Proxy decision packet (Wave-3 inheritance + telemetry texture): `agentic_orchestration/2026-06-21-proxy-combat-decision-packet.md`
- Engine — mob-cast death channel: `spatial_gauntlet/spatial_engine.py:1933-2001` (formula `:1950-1952`; cadence `:1991-1993`); geometry dispatch `:716-741` (`{point,circle,line,cone}` only); player-path variance `:1344`/`:1877` (NOT on mob channel); coverage `:815-845`
- Engine — skill-less synthetic-mob gap: `t4_sim_cycling.py:1082`
- Disciplines: #1 math-before-code, #3 seed hygiene, #11 empirical inspection, #12 semantic-shift, #24 single-parameter sweep isolation
