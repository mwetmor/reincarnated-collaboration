# Dispatch — 2026-07-13 — gamora — Wave-A re-summon loop + GX-19 clock + proxy-AI + C1a/C1b calibration

**From:** knight-rider
**To:** gamora (simulation / proxy-AI / calibration seam)
**Approved by:** Matt — Wave-A mandate ratified at PAUSE-2 (Q25, 2026-07-12: wave order **A summoner/proxy → B → C**; GX-19 RATIFIED as Wave-A nucleus; DL-03 streams-never-tax-movement adopted as design law). Sequencing + dispatch authoring by KR per gandalf Wave-A KR-handoff 2026-07-13.
**Pattern:** B (multi-day; own session memory)
**Estimated effort:** 3–4 days (Slice 1 loop + clock + AI + calibration); Slice 2 nav fix held behind an escalation.
**Companion dispatch:** `2026-07-13-rocket-wave-a-summon-economy-config.md` — rocket owns the economy config surface + the `_DEFERRED_PROXY_BINS` lift; **your calibration sign-off is rocket's go-signal for that lift.**

## Slice discipline (READ FIRST — the load-bearing sequencing call)

Wave A ships in **two slices**. Do **Slice 1 now** (fully authorized). Do **NOT** start the Slice 2 item — it is gated on a Matt build-shape ruling filed at `canonical/matt_decision_needed/2026-07-13-wave-a-slice2-build-shape-escalations.md`.

- **Slice 1 (build now):** B1 re-summon fight-loop · GX-19 proxy commitment clock · proxy-AI behavior-branch map + proximity trigger (melee + volatile_emitter; **ranged excluded — blocked by §8**) · C1a/C1b calibration bands with D3/D2 rails · **then sign off calibration readiness so rocket can lift the gate.**
- **Slice 2 (HELD — do not build until Matt rules the fix-shape):** ranged-proxy nav fix (§8). You SCOPE the fix-shape options for the escalation; you do NOT self-authorize the fix (Gate-1 fold D). Ranged-summon cert is blocked on this — melee ships without it.

## Context

The summon/proxy machinery exists but is gated. The one real fight-path gap is that `_build_positioned_allies()` spawns proxies only at fight start — there is no re-establish loop during the fight (evidence §3). GX-19 is the north-star seam: an absorption kit lets the **player's action-budget see an instant cast** while the **proxy entity models the channel/wind-up duration internally** — the interaction between the proxy's absorbed-channel clock and the player's cadence clock is currently undefined (`commitment_state_machine.py` covers the PLAYER axis only). The S6 matchup gate certifies the archetype **at the C1b endgame coordinate** (the FREE-MOVE × BEAM drop-and-forget payoff) with **D3-evaporate / D2-dominance as pass/fail rails** — so calibration is what makes the cell real-and-balanced rather than exploitative.

## Required reading before starting

- Full spec: `agentic_orchestration/gandalf/design-inputs/wave-a-engine-spec-2026-07-13.md` (§3 re-summon, §4 GX-19, §6 calibration, §7 proxy-AI, §8 nav defect — **file/line refs there**)
- Rulings: `agentic_orchestration/gandalf/design-inputs/wave-a-summon-proxy-RULINGS-2026-07-13.md` (Fork B1, Fork C1a/C1b, Fork C3 channel+wind-up)
- Evidence: `agentic_orchestration/gandalf/design-inputs/wave-a-summon-proxy-evidence-v1.md` (§2 absorption gap, §3 re-summon gap, §4 D2/D3 failure modes, §6 nav defect, §7 proxy-AI taxonomy)
- Matt escalation file: `canonical/matt_decision_needed/2026-07-13-wave-a-slice2-build-shape-escalations.md` (why the nav fix is HELD; your job is to scope its fix-shape options)
- The W3 failed-cell autopsy + gate semantics you authored: `canonical/matt_decision_needed/2026-07-03-w3-summoner-emission-structural-gap.md` (the `eligible_encounters_passed >= 9` tier_2 ship gate; `gauntlet_sim.py:640-692`) — the S6 cert reads this gate at the C1b coordinate
- Disciplines #1 (math-before-code), #1.1 (resource-bounds projection), #2.1 (smoke-test resource-scaling rehearsal), #12, #18.1 (substrate-voting-is-binding), #23 (framing-audit)

## Math-before-code

Before touching the calibration numbers, document (math-note under `simulation/notes/`):
- **C1a floor (permanent):** ramp-time + fragility, protected from buy-out. Ramp shortens with investment but never reaches literal-instant — illustrative floor **~0.5–0.8 s**; **you calibrate the actual number**. State the ramp-vs-investment curve and the asymptote gap that keeps the C1a floor felt at endgame.
- **The two failure-mode rails (evidence §4):** D3-evaporate = proxy HP too low → killed before dealing damage (floor proxy survivability); D2-dominance = proxy DPS too high → player has nothing to do (cap the drop-and-forget ceiling). State the proxy-HP floor and DPS ceiling you're certifying `proxy-light` and `proxy-heavy` against.
- **Proxy magnitude scaffold:** `proxy_commander.py` carries `PROXY_REFERENCE_HP=20_000`, `PROXY_TIER_HP_FACTOR`, `PROXY_TIER_MAX_ACTIVE` unset — set them here and justify against the two rails.
- Per Discipline #1.1: project peak memory / mob-count for any calibration batch and verify against host RAM before firing; per #2.1 the smoke gate must include resource scaling.

## Cross-seam contract change? (Principle 6 gate — KR completed at authoring time)

**LIKELY YES.** The GX-19 proxy commitment clock and the re-summon loop touch the fight_log / proxy-telemetry surface (gamora → star-lord boundary), and proxy-realized-damage attribution feeds S6. If you add/modify any `fight_log` dict key or proxy-telemetry field, the Acceptance below MUST carry a round-trip clause exercising the gamora→star-lord boundary. If you determine no cross-seam fixture-dict field changes (proxy state stays sim-internal), state `Round-trip: not applicable because <reason>` explicitly. Silence is a Gate-1 BLOCK (Principle 6).

## Slice 1 scope (build now)

- [ ] **B1 re-summon fight-loop** (§3): a fight-runtime re-summon path that, on the economy's native trigger (A1 cooldown / A2 resource / A3 slot-freed / A4 kill-token — rocket owns the config surface), re-invokes the positioned-ally spawn for the freed slot. **Manual = player-initiated action-slot, not a background tick.** The re-summon MUST respect the player's position at trigger time (**drop-at-player, not drop-at-dead-proxy**) — this is where the abandonment tax becomes real in sim.
- [ ] **GX-19 proxy commitment clock** (§4): a proxy-local commitment clock. When a kit has an absorption mode — player action resolves at instant cadence (no channel lock on the player entity); the proxy entity carries the channel/wind-up duration and ramps output over that window; the absorbed commitment is **NOT refundable to the player as free DPS** — the ramp IS the C1a floor made mechanical. Canonical exhibit: PoE Pizza Sticks (totem carries the channel; player cast instant + mobile). Ships **channel-absorption + wind-up-absorption** (Fork C3); life/mana cost-absorption rides the economy layer — no separate build.
- [ ] **Proxy-AI behavior-branch map** (§7): extend `PROXY_TYPE_TARGETING` from targeting-intent-only to a full behavior-branch assignment (`PROXY_TYPE_BEHAVIOR`) mapping each proxy type to its `preferred_behavior`: `totem_turret`→`stationary_caster`, `passive_fighter`→`melee_aggressive` (works today), `volatile_emitter`→ **NEW proximity-triggered branch** (add it). **`ranged_proxy`→ EXCLUDED this slice** (blocked by §8). See the cross-seam note below re: where the declaration lives.
- [ ] **C1a/C1b calibration bands** (§6): certify `proxy-light` and `proxy-heavy` BC cells pass the gauntlet at the correct band — D3-evaporate floor + D2-dominance ceiling. The S6 gate certifies at the **C1b endgame coordinate**, not against a flattened-away version.
- [ ] **Calibration-readiness sign-off (literal token — Gate-1 note):** append the EXACT string `CALIBRATION-READY: _DEFERRED_PROXY_BINS lift authorized` to your completion record ONLY when `proxy-light` + `proxy-heavy` certify within the D3/D2 rails at the C1b coordinate. rocket keys on this exact token (confirmed live through KR) as its go-signal for the §9 lift — do NOT emit the token on partial completion. This is the gate that keeps the lift from opening onto uncalibrated cells.
- [ ] MIGRATION.md if any cross-seam field changes (proxy telemetry / fight_log).
- [ ] `simulation/AGENT_STATE.md` updated at session end.
- [ ] Tag: `gamora/v1.7-wave-a-summon-simulation-1`.

## Slice 2 scope (HELD — do NOT build until Matt rules the fix-shape)

- [ ] **Ranged-proxy nav fix** (§8): a ranged proxy parks **38.9 m** from a boss it hits at 10 m — ally-nav chases nearest-enemy adds instead of holding boss-focus at range (`spatial_engine.py:~1996` nearest-enemy nav; `:2350` attack-phase boss-focus parity). **No magnitude lever moves `proxy_realized_damage_dealt` — this is a nav MECHANIC, not tuning.**
  - **Your Slice-1 deliverable on this item is to SCOPE the fix-shape options for the escalation, NOT to build.** Options gandalf surfaced: (a) boss-focus **inheritance** (ranged ally adopts the player's boss-focus target — cleaner for the drop-and-forget C1b fantasy); (b) a **hold-at-range** behavior variant (proxy maintains engagement distance vs its target — more general); (c) a nav_target priority override. gandalf lean: (a) or (b). Add your engineering read (cost/blast-radius/E4-nav-entanglement risk) to the escalation file so Matt/you can rule the fix-shape, then build.

## S6 interaction

The matchup gate certifies at the **C1b endgame coordinate** with D3-evaporate / D2-dominance as the pass/fail rails. **Wave A must land before its kits enter the S6 population.** Your calibration IS the S6 target — do not certify against a flattened C1b.

## Acceptance criteria

- [ ] Re-summon loop fires on the native per-economy trigger, drop-at-player; a proxy dying/expiring while the player has kited out of drop-range leaves a real gap (abandonment tax observable in sim).
- [ ] GX-19 clock: player action instant (no player-entity channel lock); proxy carries the channel/wind-up ramp; absorbed commitment not refundable as free player DPS.
- [ ] Proxy-AI: `totem_turret`/`passive_fighter`/`volatile_emitter` behavior branches assigned + proximity-trigger branch added; ranged excluded + reason recorded.
- [ ] `proxy-light` + `proxy-heavy` certify at the C1b coordinate within the D3/D2 rails; math-note states the proxy-HP floor + DPS ceiling + the ~0.5–0.8s-class C1a ramp floor (actual calibrated number).
- [ ] **Round-trip smoke** exercising the gamora→star-lord proxy-telemetry / fight_log boundary IF any cross-seam field changed — OR `Round-trip: not applicable because <reason>`.
- [ ] Calibration-readiness go-signal appended for rocket's §9 lift.
- [ ] Nav-fix fix-shape scoped in the escalation file (Slice 2 held — NOT built).
- [ ] gamora-owned tests green (no NEW failures vs HEAD; prove pre-existing on HEAD via git-stash).
- [ ] Auto-commit; **NO push** (KR owns the Wave-A push after Gate-2).

## Out of scope (explicit non-goals)

- **Building** the ranged-proxy nav fix (Slice 2 — scope only, held on Matt).
- The economy CONFIG surface (A1/A2/A4 params) + A3 reservation resource type + the `_DEFERRED_PROXY_BINS` lift — all rocket (companion dispatch).
- **fission mid-fight combat-spawn** (evidence §8) — DEFERRABLE, post-Wave-A.
- **B11 master-hides / zero-aggro taunt** (evidence §5) — DEFERRABLE; taunt-0.6 approximates, full model later.
- Any auto-refresh re-summon (Fork B1 is MANUAL — no background tick).

## Cross-seam coordination note (resolve via MIGRATION / escalate ambiguity to KR)

The §7 `PROXY_TYPE_BEHAVIOR` map extends `PROXY_TYPE_TARGETING`, which lives in **rocket's seam** (`generation/proxy_vocabulary_bridge.py`), while the behavior EXECUTION is yours (`spatial_engine._navigate_entity`). Coordinate with rocket: if the behavior-branch DECLARATION needs a gen-side field in the bridge, that's a rocket emit + a MIGRATION contract you consume; the nav-branch logic is yours. If the seam boundary is ambiguous on any specific edit, route to KR — do NOT reach into generation/ unilaterally.

**Discipline #12 (semantic shift):** `PROXY_TYPE_TARGETING → PROXY_TYPE_BEHAVIOR` is a **widening of an existing structure** (targeting-intent → full behavior branch), not a greenfield add. The MIGRATION note MUST state explicitly: *targeting-intent semantics preserved; behavior-branch is additive* — so any existing consumer of the old targeting-intent field does not break on the widened structure.

## Completion record
_(append: math-note path; C1a floor number + D3/D2 rails; re-summon loop behavior; GX-19 clock design; proxy-AI branch map; C1a/C1b calibration result at the C1b coordinate; the calibration-readiness go-signal for rocket's §9 lift; round-trip disposition; nav-fix fix-shape scoping added to the escalation file; MIGRATION path if any; tag; notes for jack-ryan Gate-2)_
