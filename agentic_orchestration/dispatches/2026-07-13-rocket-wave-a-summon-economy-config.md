# Dispatch — 2026-07-13 — rocket — Wave-A summon/proxy economy config + C2a dual-address emission

**From:** knight-rider
**To:** rocket (generation / economy + absorption config seam)
**Approved by:** Matt — Wave-A mandate ratified at PAUSE-2 (Q25, 2026-07-12: wave order **A summoner/proxy → B → C**; GX-19 RATIFIED as Wave-A spec nucleus; DL-03 adopted as design law). Sequencing + dispatch authoring by KR per gandalf Wave-A KR-handoff 2026-07-13.
**Pattern:** B (multi-day, multi-seam; own session memory)
**Estimated effort:** 2–3 days (Slice 1 gen-config + emission); Slice 2 held behind an escalation
**Companion dispatch:** `2026-07-13-gamora-wave-a-summon-simulation.md` (sim / proxy-AI / calibration) — serializes the calibration sign-off that gates your §9 lift.

## Slice discipline (READ FIRST — the load-bearing sequencing call)

Wave A ships in **two slices**, sequenced melee-first. **Both Matt build-shape escalations RULED 2026-07-13** — Slice 2 is now build-authorized (`canonical/matt_decision_needed/2026-07-13-wave-a-slice2-build-shape-escalations.md`, RULING RECORD).

- **Slice 1 (build first):** melee economy config A1/A2/A4 · C2a dual-address + center-of-gravity emission · then HOLD for calibration.
- **Slice 2 (build after Slice 1 — NOW AUTHORIZED, no longer waits on Matt):** A3 reservation-ceiling resource type. **Q27 RULED build-true** — build the true `reserved` resource type per spec §2 option (a); do NOT approximate-as-spend.
- **The `_DEFERRED_PROXY_BINS` lift (§9) is the LAST action of the whole wave** — it fires only after gamora signs off calibration readiness (companion dispatch §6). Do not lift it at the end of Slice 1; lift it when gamora's calibration lands.

## Context

Wave A makes the summon/proxy family **shippable in the dev-log catalogue** (Matt: ship all 4 economies for veteran gamers). The design north star (Fork C, PAUSE-2 ratified): a summon kit can legitimately occupy **FREE-MOVE × BEAM** — the plane cell the genre barely ships — because the proxy absorbs the commitment the player would otherwise pay (GX-19), balanced by a permanent C1a floor with the C1b endgame drop-and-forget fantasy as the intended payoff. The gen→sim proxy bridge already exists and is wired (`generation/proxy_vocabulary_bridge.py`); it emits `[]` today only because the emission gate (`_DEFERRED_PROXY_BINS`) is down. Your job is the economy config surface + the C2a plane-address emission, then to open the gate last.

## Required reading before starting

- Full spec: `agentic_orchestration/gandalf/design-inputs/wave-a-engine-spec-2026-07-13.md` (§1 inventory, §2 economies, §5 C2a, §9 gate — **build-against detail; file/line refs there**)
- Rulings: `agentic_orchestration/gandalf/design-inputs/wave-a-summon-proxy-RULINGS-2026-07-13.md` (Fork A ALL-4, Fork C north star)
- Evidence: `agentic_orchestration/gandalf/design-inputs/wave-a-summon-proxy-evidence-v1.md` (engine inventory + the 9 gaps)
- Matt escalation file: `canonical/matt_decision_needed/2026-07-13-wave-a-slice2-build-shape-escalations.md` (why A3 is HELD)
- Q19 lock (atlas plane RULE) in `canonical/matt_decision_needed/` queue — the C2a plane addresses use the **locked** movement×delivery axes (3 movement rows × 7 delivery columns × amp strata); your CoG emission feeds that atlas render
- W3 summoner-emission ruling (Option 1) history: `canonical/matt_decision_needed/2026-07-03-w3-summoner-emission-structural-gap.md` — this Wave-A build is the continuation of that gen-path
- Discipline #12 (semantic shift / MIGRATION), #1 (math-before-code)

## Math-before-code

The A1/A2/A4 economies are **drop-rate governors** — each produces a distinct mobility-vs-uptime tax curve. Before coding the config surface, document (in `generation/MIGRATION.md` or a `generation/notes/` math-note):
- The trigger predicate for each economy (A1 cooldown elapsed / A2 resource ≥ cost / A4 kill-token ≥ cost) and which existing engine field carries it (`proxy_spawn_cadence_s`, the combat-replenishing `mana`/`focus`/`rage` economies, a NEW kill-token accumulator).
- The **CoG (center-of-gravity) function** for §5: CoG ∈ [0.0 = proxy-delivery cell / ROOTED×BEAM, 1.0 = player-movement cell / FREE-MOVE×BEAM] as a function of the kit's tuned config (ramp floor, leash, economy, count). State the functional form; gamora validates the sim cost against it. This is a design reading of record — write it down before emitting.

## Cross-seam contract change? (Principle 6 gate — KR completed at authoring time)

**YES.** §5 C2a adds a NEW emitted structure: an absorption kit emits **two plane addresses + a CoG weight**. This feeds (a) the atlas render (drax/Glance `/atlas`, consumes exported season JSON) and (b) the S6 matchup gate (gamora/sim). This is a cross-seam contract on the exported-kit / season-JSON shape.

**Therefore the Acceptance criteria below MUST include a round-trip smoke** exercising the dual-address emission through the export boundary that the atlas + S6 read. A MIGRATION.md documenting the new field is mandatory (ADR-004).

## Slice 1 scope (build now)

- [ ] **A1 cooldown-gated** config: re-summon cooldown governor on the existing `proxy_spawn_cadence_s`. (The re-summon LOOP itself is gamora §3 — you own the config surface that parameterizes it.)
- [ ] **A2 spend-to-summon** config: cost-on-summon hook tying re-summon to `mana`/`focus`/`rage` spend (combat-replenishing economies already exist).
- [ ] **A4 harvest/corpse** config: a **NEW kill-token accumulator** (accrues on mob death) + a spend-to-summon hook. Document the accumulator's persistence/reset semantics in the math-note — **explicitly state cross-fight vs within-fight reset** (this determines whether A4 is a within-fight economy or a meta-progression one; name it, don't leave it implicit).
- [ ] **C2a dual-address + CoG emission** (§5): emit two plane addresses + the CoG weight per absorption kit. **Corpus kits** (478 engine_key rows carrying `mob_policy_while_casting`) carry the player-cell half NOW — emit it for them. **The curated 45-kit roster player-cell half is S7-BLOCKED** (elrond S1 finding: roster movement is S7-emitted) — emit a **flagged UNMAPPED sentinel** for the roster player-cell half, do NOT fabricate it. Document this split; it is the render/mouseover Phase-2 gate, not yours to resolve.
- [ ] MIGRATION.md — new emitted structure (two plane addresses + CoG); the CoG function; the S7-blocked roster player-cell sentinel.
- [ ] Round-trip smoke (see Acceptance).
- [ ] `generation/AGENT_STATE.md` updated at session end.
- [ ] Tag: `rocket/v2.8-wave-a-summon-economy-config-1`.
- [ ] **HOLD** — do not lift `_DEFERRED_PROXY_BINS`; do not build A3. Append a completion record and hand off to gamora calibration.

## Slice 2 scope (BUILD AFTER SLICE 1 — Q27 RULED build-true 2026-07-13)

- [ ] **A3 reservation-ceiling resource type** (§2, spec option (a) — **RULED**): build the true `reserved` resource type where `regen_cap -= reservation_per_proxy × active_count` (a permanent regenerating-resource-cap tax, NOT a per-cast spend). This preserves A3 as the 4th distinct economy + its abandonment-tax inversion (weakest re-drop tax, hardest leash). **Do NOT approximate-as-spend** (that was option (b), ruled out — it collapses A3 into A2). Sequence behind Slice 1; it no longer waits on Matt. Tag with a Slice-2 suffix (e.g. `rocket/v2.8-wave-a-summon-economy-config-2`) or fold into the wave tag per your judgment — coordinate the tag intent through KR.

## The gate (§9) — the LAST action of the wave

- [ ] Lift `_DEFERRED_PROXY_BINS = {"proxy-light","proxy-heavy"}` (`bc_target_cell_sampler.py:466`) — the switch that turns Wave A on. **ONLY after gamora signs off calibration readiness** (companion §6). Lifting onto uncalibrated proxy cells risks live D3-evaporate / D2-dominance in cert.
  - **The go-signal is a literal token, not a vibe (Gate-1 note):** gamora appends `CALIBRATION-READY: _DEFERRED_PROXY_BINS lift authorized` to her completion record. **Lift ONLY on that exact token, confirmed live through KR.** Do NOT conflate "my Slice 1 config done" or a partial gamora completion with the lift authorization — a misread here opens the gate onto uncalibrated cells.

## Acceptance criteria

- [ ] A1/A2/A4 economy config surfaces present + parameterizable; math-note documents each trigger predicate + the CoG function.
- [ ] C2a dual-address + CoG emitted for corpus kits; roster player-cell half emits the flagged UNMAPPED sentinel (S7-blocked), not a fabricated value.
- [ ] **Round-trip smoke:** emit an absorption-kit fixture through the production export path (season JSON → the shape the atlas `/atlas` render + S6 read); assert both plane addresses + the CoG weight are present and well-formed, and that the roster S7-sentinel is distinguishable from a real player-cell address. **The atlas render is a HARD consumer — do NOT let the export boundary go unexercised.** If the emission lands only at the S6/sim boundary in Slice 1, you may state `Round-trip: export-boundary deferred to <dispatch/tag> — S6 boundary exercised now` and NAME where the export round-trip will be proven — but **Wave A does not close until the atlas-consumed export round-trip is proven somewhere** (Gate-1 jack-ryan note, 2026-07-13).
- [ ] MIGRATION.md written (new emitted structure + CoG function + S7 sentinel).
- [ ] rocket-owned tests green (count is an estimate — don't gate on a number; gate on no NEW failures vs HEAD; prove pre-existing failures on HEAD via git-stash per the water-to-ice precedent).
- [ ] Auto-commit; **NO push** (KR owns the Wave-A push after Gate-2).

## Out of scope (explicit non-goals)

- **A3 reservation mechanic** during Slice 1 (it's now Slice-2 authorized — build it AFTER the melee economies + C2a emission land, not before).
- **Lifting the gate** until gamora calibration signs off (sequence LAST).
- The re-summon fight-loop, GX-19 clock, proxy-AI behavior branches, calibration bands, ranged-proxy nav — all gamora (companion dispatch).
- **fission mid-fight combat-spawn** (evidence §8) — DEFERRABLE, post-Wave-A. Lifetime fission works; do not build combat-spawn.
- Any change to the Discipline #14 slot-routing layer or historical persisted kits (Law 2 immutability).
- Resolving the S7 roster player-cell mapping — flag it, don't fabricate it.

## Cross-seam coordination note (resolve via MIGRATION / escalate ambiguity to KR)

The proxy-AI behavior-branch map (spec §7) extends `PROXY_TYPE_TARGETING` / `PROXY_TYPE_TIER` — which live in **your seam** (`generation/proxy_vocabulary_bridge.py`) — into a `PROXY_TYPE_BEHAVIOR` map that **gamora consumes** in `spatial_engine._navigate_entity` (sim seam). The spec routes the §7 build to gamora, but the **declaration surface may be gen-side**. Coordinate with gamora: if `PROXY_TYPE_BEHAVIOR` needs a gen-side declaration in the bridge, that's your emit + a MIGRATION contract; the behavior execution is gamora's. If the seam boundary is ambiguous on any specific hit, route to KR — do NOT guess.

**Discipline #12 (semantic shift):** if the declaration lands in your bridge, `PROXY_TYPE_TARGETING → PROXY_TYPE_BEHAVIOR` is a **widening of an existing structure** (targeting-intent → full behavior branch), not a greenfield add — the MIGRATION note MUST state *targeting-intent semantics preserved; behavior-branch is additive* so existing consumers of the old field don't break.

## Completion record
_(append: math-note path; A1/A2/A4 config surfaces; CoG function form; C2a emission + S7-sentinel handling; round-trip smoke result; MIGRATION path; tag; the calibration-readiness go-signal you're waiting on from gamora before the §9 lift; notes for jack-ryan Gate-2)_

---

### Completion record — rocket — 2026-07-13 (Slice 1 COMPLETE; gate HELD)

**Math-note (Discipline #1, authored BEFORE code):** `reincarnated-engine/src/reincarnated/generation/notes/wave-a-summon-economy-config-math-2026-07-13.md`.

**A1/A2/A4 config surfaces:** NEW `generation/summon_economy.py` — `build_summon_economy(economy=...)` emits a per-decl `summon_economy` block. A1 cooldown (`cooldown_s`, defaults to decl `spawn_cadence_s` — backward-compat); A2 spend (`summon_cost` + `summon_cost_resource ∈ {mana,focus,rage,stamina,combo}`); A4 harvest (`summon_token_cost`, `token_per_kill`, `starting_tokens`). Trigger predicates code-cited in math-note §1. **A4 reset semantics EXPLICIT: WITHIN-FIGHT — accumulator resets to `starting_tokens` (default 0) each fight, no cross-fight persistence** (math-note §1.3.1; persistence would be a D2-dominance back-door + break S6-single-fight cert validity; the persistence-needed case is a flagged DESIGN escalation, not a silent flip). A3 `reserved` RAISES (Slice 2 held). Wired onto each decl via `proxy_vocabulary_bridge`.

**CoG function form:** `CoG = clamp(W_RAMP·(1−ramp_floor_norm) + W_LEASH·leash_norm + W_ECON·economy_slack + W_COUNT·count_norm, 0, COG_CEILING)` — convex combination (weights 0.40/0.25/0.20/0.15, sum 1.0), monotone in each lever, capped at `COG_CEILING=0.92` (the permanent C1a asymptote gap — never literal 1.0). `economy_slack` is a per-economy switch (A1 cooldown / A2 cost / A4 token / A3-Slice2 reservation). **gamora re-pins `COG_CEILING = 1 − (calibrated C1a floor share)` + the `*_REF` anchors at calibration.** Full form + monotonicity proof + refutation in math-note §2.

**C2a emission + S7-sentinel handling:** `absorption_plane_address = {proxy_cell, player_cell, center_of_gravity, cell_confident, roster_movement_source}` emitted on BOTH `to_dict()` paths (`bc_target_player_class.py` + `season_generation_pipeline.py`), `None` for non-absorption kits (additive-only). Each cell = `{movement, delivery, amp}` per the atlas contract. **Corpus (self_derived) player-cell carried NOW:** `movement=FREE-MOVE`, `cell_confident=True` (an absorption kit's player action resolves instant → free-moving, spec §4). **Roster (s7_pending) player-cell BLOCKED:** `movement=UNMAPPED` sentinel, `cell_confident=False` — NOT fabricated; the proxy_cell half stays derivable; distinguishable from a real address by the enum member + the flag. Render/mouseover Phase-2 gate flagged, NOT resolved (dispatch fence honored).

**Round-trip smoke:** `generation/notes/wave_a_summon_economy_roundtrip_smoke_2026_07_13.py` — **30/30 PASS**, exercised through the **EXPORT boundary** (`to_dict()`-shape → `json.dumps`/`loads` → read = the shape the atlas `/atlas` render + S6 read). Asserts both cells enum-valid, CoG monotone + capped, corpus vs roster distinguishable, non-absorption=None, A3 rejected, targeting preserved. **The export-boundary round-trip is proven HERE** (not deferred). Existing proxy smokes (demo_summoner 53✓, w2_pairing✓) green.

**MIGRATION:** `reincarnated-engine/src/reincarnated/generation/MIGRATION.md` [2026-07-13] entry — new emitted structure + CoG function + S7 sentinel + the `PROXY_TYPE_BEHAVIOR` §12 semantic-shift (widening) contract.

**Tag:** `rocket/v2.8-wave-a-summon-economy-config-1`. Auto-committed in-scope. **NOT pushed** (KR owns Wave-A push after Gate-2).

**Tests:** 240 passed on touched-module scope. 21 pre-existing errors in `test_cycle13_wave5_season_generation.py` (W5R.2 cell-grain fixture-setup violation) PROVEN identical on pristine HEAD via git-stash (pristine = 46 passed, 21 errors); NOT mine. 4 grouping-vocab doc-path collection errors also pre-existing + unrelated.

**§9 lift — HOLDING.** `_DEFERRED_PROXY_BINS` UNTOUCHED (`bc_target_composer.py:97` intact = `frozenset({"proxy-light","proxy-heavy"})`). The lift is the LAST action of the whole wave. **The go-signal I am waiting on: gamora's exact token `CALIBRATION-READY: _DEFERRED_PROXY_BINS lift authorized`, confirmed live through KR.** I will NOT conflate my Slice-1 done, or a partial gamora completion, with the lift authorization. A3 is untouched (Slice 2).

**`PROXY_TYPE_BEHAVIOR` (gamora consumes) — the §7 contract, seam-ownership RESOLVED (no ambiguity for KR):** the DECLARATION surface (the `PROXY_TYPE_BEHAVIOR` dict in `generation/summon_economy.py` + the `preferred_behavior` field on each decl) is gen-side — I built it. The EXECUTION (`spatial_engine._navigate_entity` branch dispatch + the NEW `proximity_trigger` branch for `volatile_emitter`) is gamora's. Discipline #12: targeting-intent semantics PRESERVED (`PROXY_TYPE_TARGETING` unchanged, `targeting_behavior` still emitted), behavior-branch ADDITIVE. Branch tokens ∈ existing `{stationary_caster, melee_aggressive, ranged_kite, cast_at_range, hit_and_run}` + NEW `proximity_trigger`; `ranged_kite` declared but its boss-focus execution is §8-nav-gated (Slice 2). No seam-ownership ambiguity to escalate.

**Notes for jack-ryan Gate-2:**
- Math-before-code honored (note authored + read BEFORE code; A4 reset semantics + CoG form stated first).
- Principle-6 round-trip through the EXPORT boundary proven (not deferred) — the atlas HARD consumer is exercised via the `to_dict()`-shape → JSON path.
- Additive-only invariant proven (non-absorption kit = `None`; decl targeting_behavior preserved; no existing key shape change).
- Pre-existing failures proven on HEAD via git-stash (water-to-ice precedent).
- Gate HELD; A3 untouched; §9 lift awaits gamora's literal token.
