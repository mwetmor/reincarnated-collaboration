# Wave-B Engine Spec — Reservation / Persistent-Cost / Attunement-Meter / Recharge (+ Life-Cost / Drain triage)

**STATUS:** GATE-1 PASS-WITH-AMENDMENTS (jack-ryan 2026-07-16 — verdict stamp below the DRIFT-CRITIC stamp). GATED by gandalf-prime DRIFT-CRITIC 2026-07-16 (PASS-WITH-NOTES); five §10 escalations RULED-veto-open under Matt's autonomous-run authority — Gate-1 audited all five for internal consistency + code-grounding: **all five stand as ruled** (no reversal, no flag). Amendments (10, enumerated in verdict stamp) ride into the rocket/gamora implementation charges. Ready for build-slice dispatch per §12.2 sequencing.
**Date:** 2026-07-16
**Author:** gandalf (SPEC-AUTHOR work unit, autonomous atlas-parity run cycle 2)
**Authority:** Matt autonomous-run delegation 2026-07-16 (sub-agents iterate engine toward 100% atlas mechanical parity) + S2 census V7 THE SCOREBOARD ranking Wave B the #2 parity lever after in-flight ailment layer. **The five §10 escalation rulings this doc records are gandalf-prime rulings under Matt's autonomous-run authority — veto-open, Matt may overturn on read.** (The four §X.1 bin-family definitions are governed by those rulings, not separately ruled.)

> **⚖ DRIFT-CRITIC GATE STAMP (gandalf-prime, 2026-07-16) — PASS-WITH-NOTES.** The §10 ruling block was drafted-for-ratification; it is now RATIFIED as written — all five leans concurred on the drafted grounds (D2 aura-slot dominance for a; corpus-shape fidelity + Wave-A A3 backward-compat for b; smallest-lift + consumer-level split for c; LC-030-is-pool-content + thin-roster for d; player-agency-vs-game-plays-itself AI distinction for e). Numbers verified against THE SCOREBOARD (44/42/16/16/3/2; 118 gate number). Three notes for jack-ryan Gate-1:
>
> 1. **§4.3 ↔ §4.8 cost_type contradiction — EMISSION SURFACE WINS.** §4.3's lean parenthetical ("both need same cost_type_map = `[]` — the meter IS the resource") contradicts §4.8/§12.1 (`charge-stack: ["mana", "focus", "stamina-as-resource"]`). Ruling: the §4.8 non-empty map is correct — `resolve_cost_type` must return a resolvable family for an ACTIVE bin; zero-marginal-cost kits (D2 Throw Barb, VS auto-fire) express via near-zero `cost_scale` in `resource_economy`, not via an empty map (an empty map is DEFERRED semantics). Gate-1: verify against `resolve_cost_type` code path + strike the §4.3 parenthetical.
> 2. **Wave-C trigger-boundary** — PC proc-loop sub-shape builds the single-trigger PRIMITIVE (CWDT/CoC/Poet's Pen as one armed trigger, no chains); Wave-C's trigger + mark-consume family owns chain-of-triggers grammar. The e=(B) `persistent_trigger` commitment-state is the deliberate extension hook. Gate-1: stress-test that nothing in §2.4's `proc_trigger_condition` enum forecloses chain-grammar (it must stay per-trigger, never per-chain).
> 3. **Minor:** Authority-line "six rulings" normalized to five (fixed in this stamp's commit); §8 table HP-economy kit-touch "3 (LC + 2 overlap)" is loose (DR's 2 kits are not HP-economy-mapped — drain's Wave-C home is an open §7.3 question, not pre-assigned). Gate-1 tidies.
>
> **⚖ GATE-1 VERDICT STAMP (jack-ryan, 2026-07-16) — PASS-WITH-AMENDMENTS.** Stress-tested against live engine code (read-only) + corpus rosters. **Escalation audit: all five §10 rulings (a–e) are internally consistent AND code-grounded; NONE reversed, NONE flagged.** Roster spot-check: 14/14 named exemplar kits verified present in corpus; PC/RS/AM/RC/LC/DR any-occurrence counts (45/42/18/18/3/2) reproduce, scoreboard primary buckets (44/42/16/16/3/2) are the authority and match §0. Ten amendments (all corrections/reconciliations/path-fixes — NO BLOCK, NO ruling reversal, NO code defect):
> 1. **[note #1 — cost_type CONTRADICTION resolved, EMISSION-SURFACE-WINS, code-confirmed]** `resolve_cost_type` (`bc_target_composer.py:274`) returns `role_priority[0]` (=mana) on an empty `[]` map — empty ≠ "no cost." §4.3 parenthetical STRUCK; §4.8/§12.1 `["mana","focus","stamina-as-resource"]` is correct. Zero-marginal-cost via `cost_scale`, not empty map.
> 2. **[note #2 — trigger-boundary CONFIRMED clean]** `proc_trigger_condition` enum is all single-trigger primitives; no chain leakage; boundary sound as written (no edit).
> 3. **[note #3 — §8 table tidied]** `HP-economy` = LC×3 exact; DR not HP-mapped.
> 4. **[ruling-10 TH rider — §8 `damage-taken-converts` corrected 0→3]** Retaliation Warlord (gd) / Thorns Barbarian (d4) / Thorns Invoker (d3) are a REAL passive-reflect roster sitting in `econ:UNKNOWN`; Wave-C park stands, count is 3 not 0.
> 5. **[ruling-10 NR rider — RULED steady-absorbs, no new bin]** NR carries 0 corpus tokens; routes to `steady` via `cost_scale≈0` (§5.3).
> 6. **[WARN — `combatant.py:tick` consumer-site is WRONG]** `combatant.py` is state-only (no `tick` method); the per-tick loop is `spatial_gauntlet/spatial_engine.py` (:2326/:2189) + `effect_resolver.tick_effects` (:55). §1 table + §12.1 corrected; §2.8/§3.7/§4.7 inherit the §1 correction.
> 7. **[WARN — `commitment_state_machine.py` PATH wrong + extension mis-modeled]** module is under `spatial_gauntlet/`, NOT bare `simulation/`; it is a stateless `commitment_bin ∈ {snap,wind-up,channel}` parser (`skill_schema.py:222`), NOT a state registry. Ruling (e)=(B) stands; extension = enum-widen by 2 (Discipline #12), corrected at §2.6 + companion-docs path.
> 8. **[INFO — `substrate_templates.py` under-claimed]** `W1_4_CHARGE_STACK` (~25 templates) ALREADY exists (Cycle-12 L3); rocket EXTENDS/REUSES, does not greenfield. §4.8 annotated.
> 9. **[INFO — `ActiveEffect.category` is a PROPOSED field, not existing]** `ActiveEffect` (`combatant.py:109`) has `name/params/duration_remaining/source_element/tick_accumulated` only; new sub-shape state lands in `params`. §1 table annotated (§2.3/§4.3 `.category` reads as a proposed add).
> 10. **[INFO — primary-vs-any-occurrence count discipline]** §0 "42 primary / 44 primary" are SCOREBOARD bucket-attributions (authority), which differ from naive single-token `econ_gaps` exact counts (PC `["PC"]`=43, AM `["AM"]`=17, RC `["RC"]`=18) by the scoreboard's overlap primary-attribution logic. Not an error — flagged so implementers read counts from the scoreboard, not raw token grep.
>
> Disciplines/Principles applied: #1 (math-before-code — build charges must cite pre-code math notes, as ailment/Wave-A did), #8 (schema-at-boundary — new fields into frozen `resource_economy`/`summon_economy` key tuples via their `_validate` gates), #11 (E4 nav/commitment-spine VERIFY — pure-read confirmation of the commitment machine), #12 (semantic-shift = additive widening — commitment_bin enum + charge-stack templates), #13 (drift-check — escalation rulings held, no scope creep). Review Principles #2 (smoke-gate — S6 gauntlet cert required pre-lift, §12.2), #3 (cross-seam impact — MIGRATION owed at each gen→sim boundary), #4 (decisions-log as truth — companion DL entry logged). ADR-002 (jack-ryan-tier: Gate-1 findings + spec-doc edits + decisions-log write). **Finding:** `agentic_orchestration/jack-ryan/reviews/2026-07-16-wave-b-economy-gate1.md`.
**Companion docs:**
- `../../agentic_orchestration/research/curated/atlas/s2-readiness-census-v7-2026-07-16.md` — THE SCOREBOARD (bin counts, ranking, denominator)
- `../../agentic_orchestration/gandalf/design-inputs/wave-a-engine-spec-2026-07-13.md` — Wave-A form model (§9 gate-lift pattern, §2 A3 reservation precedent, §11 routing template)
- `./ailment-layer-engine-spec.md` — sibling Gate-1-PASS spec (§10 escalation pattern, DL-03 conformance section, rocket/gamora split)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/bc_target_composer.py` — the composer this spec extends (`_DEFERRED_ECON_BINS`, `_ECON_BIN_COST_TYPE_MAP`, `resolve_cost_type`)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/summon_economy.py` — the Wave-A A3 reservation precedent (`ECONOMY_RESERVED`, `reservation_per_proxy`, `reservation_resource`) — RS builds on this
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/resource_economy.py` — the per-kit cost-shaping config surface Wave B extends
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/commitment_state_machine.py` — player commitment axis (E4; extension point for PC toggle-state). **[Gate-1 path-fix: module is under `spatial_gauntlet/`, NOT bare `simulation/`; it is the E4 stateless `commitment_bin ∈ {snap, wind-up, channel}` parser, not a state registry — see §2.6 amendment.]**

---

## §0 — TL;DR

Six intake bins (from S2 census V7) collapse to **four new engine mechanics** + two Wave-C-deferred bins. This spec authorizes `RS` and `PC` as **first-class new econ_bin values** in `bc_target_composer._ECON_BIN_COST_TYPE_MAP`; `AM` and `RC` fold into the existing engine-deferred `charge-stack` bin as **two sim-side sub-shapes** (accumulator vs cycle); `LC` and `DR` triage TO Wave C on evidence of thin roster + HP-cost gate collision with `_DEFERRED_ECON_BINS = {"HP-economy"}` which the Wave-A LC-030 finding already declared "pool has zero HP-cost mechanics — hard infeasible."

**Bin count reconciliation (S2 census V7 primary + spec cross-check):**

| Bin | Scoreboard primary | Any-occurrence | 2-way overlaps | Spec ruling |
|---|---|---|---|---|
| econ:PC (persistent-condition) | 44 | 45 | +BT×2 | **Ships Wave B — new econ_bin `persistent-condition`** |
| econ:RS (reservation) | 42 | 42 | +SU×4, +LC×1 | **Ships Wave B — new econ_bin `reservation`** (extends Wave-A A3 to non-summoner auras) |
| econ:AM (attunement-meter) | 16 | 18 | +BT×1 | **Ships Wave B — lifts `charge-stack` sub-shape `accumulator`** |
| econ:RC (recharge) | 16 | 18 | (all clean) | **Ships Wave B — lifts `charge-stack` sub-shape `cycle`** |
| econ:LC (life-cost) | 3 | 3 | +RS×1 | **Defers to Wave C — see §7** (thin roster + `HP-economy` remains hard-infeasible per LC-030) |
| econ:DR (drain) | 2 | 2 | (clean) | **Defers to Wave C — see §7** (thin roster + auto-fire-while-moving pattern is a VS-family adjacency, not a first-class RDR economy) |

**Wave-B kit-touch total:** 44 + 42 + 16 + 16 = **118 kits unblocked at gate-lift** (scoreboard exclusive counts). Adding LC (3) + DR (2) would push to 123; ruling defers those to Wave C, so **118 is the load-bearing gate number.**

**Design north star:** Wave A's contribution was the proxy-family gate lift (`_DEFERRED_PROXY_BINS = {}` + summon_economy A1–A4 build). Wave B is the **econ-family gate lift** — dropping `charge-stack` from `_DEFERRED_ECON_BINS` + adding two new econ_bin values (`reservation`, `persistent-condition`). Same gate pattern; same rocket/gamora split; same S6 cert requirement.

**Interaction with in-flight ailment layer:** four of six Wave-B bins compose with sunder / freeze / stun / poison at consumer time. Composition contracts §5. **DL-03 CRITICAL:** aura and persistent-condition mechanics that emit ticks are `tags=["placed"]` per zone-template precedent — they **do not tax caster movement**. Ailment-spec §11 poison-cloud DL-03 resolution is the exact template.

**Escalations this doc raises (5 items, count-check §10):**
- (a) `persistent-condition` = one-active-only OR multi-active-stacking law (aura-slot semantics);
- (b) `reservation` = %-of-max-cap OR flat-cap-subtraction representation;
- (c) AM/RC = one shared `charge-stack` bin with sub-shape tag OR two separate econ_bin values;
- (d) LC/DR triage confirmation (defer to Wave C is the LEAN — Matt ratifies);
- (e) PC bin scope split — pure toggles (auras/charges) vs proc-loops (CoC/CWDT/Poet's-Pen) as ONE bin or TWO. These are ARCHITECTURAL, not tuning — Matt/KR ruling owed before build.

---

## §1 — What already EXISTS (do not rebuild)

Per current engine survey (2026-07-16 pass on `bc_target_composer.py`, `summon_economy.py`, `resource_economy.py`, `commitment_state_machine.py`):

| Component | File | State — for Wave-B purposes |
|---|---|---|
| Econ-bin registry | `bc_target_composer._ECON_BIN_COST_TYPE_MAP` (:236) | 7 bins keyed: 3 DEFERRED (`HP-economy`, `charge-stack`, `damage-taken-converts`), 4 ACTIVE (`generator-spender`, `starved`, `overflow`, `steady`). Wave B adds `reservation` + `persistent-condition`; lifts `charge-stack` |
| Deferred set | `bc_target_composer._DEFERRED_ECON_BINS` (:95) | `frozenset({"HP-economy", "charge-stack", "damage-taken-converts"})` — the gate. Wave-B **drops `charge-stack`** (analogous to Wave-A's `_DEFERRED_PROXY_BINS` drain to `frozenset()`) |
| Infeasibility gate | `bc_target_composer.check_infeasibility` (:304) | Reads `_DEFERRED_ECON_BINS`; `HP-economy` is HARD-INFEASIBLE per LC-030 ("pool has zero HP-cost mechanics"). Wave-B change: `charge-stack` drops to feasible; new bins added to `_ECON_BIN_COST_TYPE_MAP` |
| Cost-type resolver | `bc_target_composer.resolve_cost_type` (:247) | `(econ_bin, role, rng) → cost_type ∈ {mana, rage, combo, focus, stamina-as-resource}`. Wave-B adds new cost_types OR new mappings (see §2, §3, §4) |
| A3 reservation precedent | `summon_economy.py:39,59-60,73,120-137` | `ECONOMY_RESERVED = "reserved"` + `reservation_per_proxy` (regen-cap tax) + `reservation_resource` (which pool taxed). **RS extends this pattern to non-summoner auras** — same regen-cap-tax mechanic, different consumer (§3.4) |
| Per-kit resource_economy | `resource_economy.py:15-25` | Kit-declared `{cost_scale, cost_slope, regen_magnitude, on_kill_frac, ramp_per_s, cadence_scale}`. Wave-B PC extends this with `persistent_tick_cost` / `activation_cost` fields (§2.5); AM extends with `accumulator_state` (§4.5) |
| Commitment state | `commitment_state_machine.py` | Player-only commitment (instant/wind-up/channel). Wave-B extension: **PC is a fourth commitment shape** — the "persistent-toggle" — where the player is neither casting nor idle but paying a slow tick while an aura ticks (§2.6, ESCALATION e) |
| Active-effects consumer | `damage_resolver._add_or_refresh` (:1156) / `effect_resolver.tick_effects` (:55) | VERIFIED — the Wave-A ailment substrate; new PC and AM state-carriers plug in as `ActiveEffect` entries (`combatant.py:109`; fields `name`/`params`/`duration_remaining`/`source_element`/`tick_accumulated`). NOTE any new sub-shape field lands in the `params` dict — `ActiveEffect` has no `.category` attr today (§2.3/§4.3's `.category` is a proposed add, not an existing field) |
| Per-tick loop (consumer SITE) | `spatial_gauntlet/spatial_engine.py` (channel tick loop :2326; `_step_proxy_population` :2189) | **[Gate-1 correction]** the per-tick fight loop lives HERE, NOT at `combatant.py:tick` — `combatant.py` is a state dataclass (`CombatantState`) with NO `tick` method. Every "combatant.py:tick" consumer-site citation below (§2.8, §3.7, §4.7, §12.1) should read "`spatial_engine` per-tick loop + `effect_resolver.tick_effects`." gamora wires PC/AM/RC consumers into the spatial-engine tick + `effect_resolver.tick_effects`, mirroring the E4 channel-tick and D4 proxy-population precedents |
| Gauntlet cert path | S6 matchup gate | Wave-A precedent: `proxy-light` + `proxy-heavy` certified at gauntlet. Wave-B parallel: `charge-stack` (lifted), `reservation`, `persistent-condition` all pass S6 gauntlet before gate-lift ships |

**Existing extension points these mechanics plug into (no new subsystems required for 3 of 4):**
- **RS** = extends Wave-A A3 reservation-ceiling machinery (`summon_economy.reservation_per_proxy` generalized to non-proxy carriers)
- **PC** = new econ_bin + new commitment-state extension (`persistent_toggle`) + new per-kit `resource_economy` field
- **AM** = `charge-stack` sub-shape `accumulator` — lifts existing deferred bin
- **RC** = `charge-stack` sub-shape `cycle` — same lift, different sub-tag

---

## §2 — Econ-bin: `persistent-condition` (PC — the #1 Wave-B gap: 44–45 kits / 8.4% of combat corpus)

### 2.1 Delegated ruling recorded (Matt 2026-07-16 autonomous-run, veto-open)

**PC is the "always-on" family: D2 auras (Auradin), D2 stackable stances (Frenzy charges), PoE1 proc-loops (CoC Ice Nova, CWDT self-hit loop, Poet's Pen VD), PoE1 summoner-adjacent buffs (SRS raging-spirit charges, Summonmancer commander buffs), Diablo werewolf/werebear form states.** Genre precedent: D2 aura model (paladin auras that pulse while active); PoE1 permanent-buff loops (CWDT / Cast-on-Crit trigger meta); D4 ultimate-charge buff states.

**Distinction from RS (reservation):** RS TAXES a resource pool's regen-cap; PC TAXES a per-tick cost OR provides an always-on effect that itself costs to activate. RS is a permanent-tax model; PC is either a persistent-tick model or a toggle-with-activation-cost model. A single kit MAY carry both (D2 Auradin: RS = holy aura reservation + PC = frenzy-charge state — evidence §2b poe1-aurastacker with `["RS", "SU"]` overlap and d2-auradin with `["PC"]`).

### 2.2 Mechanic definition

Persistent-condition = a **stateful engine flag** on the player that persists while the kit is "active" and costs to maintain via one of three mechanisms:
- **(i) Tick cost** — a small mana/energy drain per tick (PoE1 aura maintenance model, if we treat it as tick-cost rather than reservation);
- **(ii) Activation cost + toggle** — a one-shot activation cost, then free maintenance until the player deactivates OR is knocked out (D2 aura model);
- **(iii) Proc-trigger loop** — the state IS the trigger condition (CWDT: on-hit-of-N-damage fires linked skill; CoC: on-crit fires linked skill; Poet's Pen: on-cast-of-linked-spell fires bonded spell). This last form is a **passive-driver** rather than an active-cost.

**Genre precedent** (bin roster attestation):
- **D2 Auradin, Summonmancer, Frenzy Barb, Horker, Maul Werebear** — persistent stance/aura/charge state (13/44 = ~30% of PC bin is D2)
- **PoE1 CoC Ice Nova, Poet's Pen VD, CWDT Self-Hit Loop, Autobomber, SRS, Minion-Pact BV** — proc-loop / linked-trigger meta (11/44 = ~25%)
- **D2 Tainted Summoner Warlock** — necromancer commander state
- **PoE1 Summon Raging Spirits** — active-buff state on summons

### 2.3 Category classification (ARCHITECTURAL ESCALATION a)

**Options:**
- **(a) One `persistent-condition` bin, one active at a time** — the D2 aura-slot model (one aura from paladin's list active); simplest sim consumer; matches D2 precedent verbatim (13/44 kits).
- **(b) One `persistent-condition` bin, multi-active with cost stacking** — PoE1 aurastacker precedent (multiple reservation-auras compose; total reservation < 100%); requires new stacking-cap invariant.
- **(c) Two bins split — `aura-toggle` (D2 slot-model) + `proc-loop` (PoE1 trigger-meta)** — semantic clarity; two consumer sites; higher build cost.
- **gandalf lean: (a) one-active-at-a-time.** Rationale beyond simplicity: the D2 aura-slot model is the **corpus's dominant PC shape by count** (13/44 direct + PoE1 aurastacker's multi-aura is scored under RS `["RS", "SU"]` overlaps in the corpus, not PC — so the multi-aura case is already RS-family, not PC-family). Proc-loops (CWDT/CoC/Poet's Pen) are ALSO one-active-at-a-time (you carry ONE CWDT setup; ONE Poet's Pen wand). One-active keeps the sim consumer clean; ESCALATION e (§10) can later split proc-loops if their AI-priority behavior diverges.

**ESCALATION a — Matt/KR ruling owed:** ratify (a) or (b) or (c) before rocket writes the composer bin extension. Impact: `_ECON_BIN_COST_TYPE_MAP` gains one bin (a/b) or two bins (c); consumer complexity in `combatant.py` differs by factor.

### 2.4 Sub-shape tag on ActiveEffect (rocket emits; gamora consumes)

Even under one-bin ruling (a), the three sub-shapes (tick-cost, toggle, proc-loop) need distinguishing on the ActiveEffect entry so gamora's sim consumer branches correctly:

```yaml
# resource_economy per-kit fields (rocket emits; gamora reads)
persistent_condition_shape:  # NEW field for PC-bin kits
  min: null
  max: null
  default: null
  # one of: {"tick-cost", "activation-toggle", "proc-loop"}
persistent_tick_cost:        # NEW — for shape="tick-cost" only
  min: 0.0
  max: 5.0
  default: 1.0              # units of primary resource per second while active
activation_cost:             # NEW — for shape="activation-toggle" only
  min: 5.0
  max: 50.0
  default: 20.0             # one-shot cost on toggle-on
proc_trigger_condition:      # NEW — for shape="proc-loop" only
  min: null
  max: null
  default: null
  # one of: {"on-hit-threshold", "on-crit", "on-cast-linked", "on-kill", "on-damage-taken"}
```

**Calibration ranges (gamora tunes within rails):** `persistent_tick_cost` default 1.0/s is a conservative floor; adjust to 0.5–2.0/s based on S6 gauntlet response. `activation_cost` default 20 is D2-Auradin-analog (~10% max mana at low levels).

> **⚑ Gate-1 TRIGGER-BOUNDARY CONFIRMATION (jack-ryan 2026-07-16, note #2 — PASS, no chain leakage):** stress-tested `proc_trigger_condition`'s enum `{on-hit-threshold, on-crit, on-cast-linked, on-kill, on-damage-taken}` for chain-grammar leakage. **CLEAN.** Every value is a SINGLE-trigger primitive (one armed condition → one linked cast). None encodes a trigger-of-a-trigger, a chain depth, a mark-consume, or a "on-linked-cast-fire re-trigger" back-door. `on-cast-linked` is the closest risk (Poet's-Pen "on cast of a linked spell") but it is the ARMING condition read from the player's own cast, not a chain link — it fires ONE bonded spell, terminal. §2.2(iii), §9 ("CWDT trigger-chain semantics DEFERRABLE — proc-loop covers primitive; chain-of-triggers is Wave-C"), and the e=(B) `persistent_trigger` commitment-state (the deliberate extension HOOK) all hold the boundary correctly. Chain-of-triggers grammar remains Wave-C's `trigger + mark-consume` family. **No spec edit needed — boundary is sound as written.**

### 2.5 Element/element-neutral bias (which skills roll it)

- **Holy / Consecrate skills** — aura-toggle sub-shape natively; consecrate's existing ampification-zone already implies this. `element_biases.py` NEW map: holy-primary skills roll PC as secondary rider at rate 0.35.
- **Physical / Barbarian-family** — Frenzy-charge / berserk state (D2 Frenzy Barb precedent). PC as activation-toggle sub-shape.
- **Fire / Lightning proc-loops** — CoC Ice Nova, Poet's Pen VD, CWDT (all attested in PC roster). PC as proc-loop sub-shape. **Rocket routes via `proc_trigger_condition` field.**
- **Shadow / Necromancer commander** — Summonmancer, Tainted Summoner Warlock. PC as activation-toggle (commander presence buff).
- **NOT poison** (poison's stack model §5 conflicts semantically with a single-active PC state).
- **NOT wind / cold** (chill/root already own the soft/hard-control identity for those elements).

Rocket authorship touchpoint: `element_biases.py` gets a NEW `PERSISTENT_CONDITION_BIAS` map; `substrate_templates.py` gets new templates `paladin_aura_of_X`, `barbarian_frenzy_state`, `proc_loop_trigger`.

### 2.6 Commitment-state extension (ESCALATION e — proc-loop split question)

**Options:**
- **(A) One commitment_state `persistent_toggle`** covering all three sub-shapes — sim consumer branches on `persistent_condition_shape` field; commitment_state is unified.
- **(B) Two commitment_states — `persistent_toggle` (tick-cost + activation-toggle) + `persistent_trigger` (proc-loop)** — semantic clarity; proc-loop is passive-driven (player never "activates" it — it fires when trigger condition met) whereas toggle-model is player-driven.
- **gandalf lean: (B).** Grounds: proc-loops have a **fundamentally different player-input profile** — the player builds the trigger meta, then the game plays itself (CWDT / CoC / Poet's Pen are notorious afk-friendly builds in PoE1). Toggle-auras and charge-states require **active player choice per encounter** (which aura to have on, when to Frenzy up). If commitment_state_machine.py collapses these, the sim's per-tick AI cannot distinguish "player is deciding aura choice" from "trigger meta is firing autonomously." Split the commitment_state; keep the econ_bin unified.

**Impact:** commitment_state_machine.py gains two new values; gamora's AI logic branches on `commitment_state`; rocket sets it per kit at emission.

> **⚑ Gate-1 CODE-SHAPE NOTE (jack-ryan 2026-07-16, note #2-adjacent — WARN, non-blocking):** the extension point is viable but the spec's mental model of it is imprecise against actual code. There is NO `commitment_state` enum-registry to "add two values to." The E4 machine (`spatial_gauntlet/commitment_state_machine.py`) is a **stateless `.get`-based parser**: `commitment_bin` is a per-SKILL field on `skill_schema.py:222–223` with enum `{snap, wind-up, channel}` (None = exempt). "Add `persistent_toggle` + `persistent_trigger`" means **extending that `commitment_bin` enum by two values** and teaching the parser + `spatial_engine` player-action phase to honor them — a real change, but shaped as (enum-widen + new branch in the E4 consumer at `spatial_engine.py:~2220+`), NOT "new states in a machine." rocket owns the `skill_schema.py` enum widen; gamora owns the `spatial_engine`/`commitment_state_machine` branch. **The ruling (B) stands; only the extension-point description is corrected.** Discipline #12 (semantic-shift = additive widening) governs — same pattern as Wave-A's `PROXY_TYPE_TARGETING → PROXY_TYPE_BEHAVIOR` widen.

**ESCALATION e — Matt/KR ruling owed:** ratify (A) or (B) before gamora writes the commitment-state consumer. Impact: 1 vs 2 new commitment_state values; sim AI complexity.

### 2.7 Stacking / refresh law

- **One-active-per-slot** — under ruling (a). Player switches PC states = old state ends, new state begins. Frenzy stacks (D2) are NOT PC-stacking; they are a within-PC internal counter (`stack_count` on the ActiveEffect).
- **Refresh rule** — activation-toggle sub-shape does NOT refresh (deactivate + reactivate = pay activation_cost twice; no auto-refresh). Tick-cost sub-shape auto-continues until pool depleted (D2 Auradin model: aura ends when mana hits zero; PoE1 aurastacker model: reservation is via RS, not tick-cost).
- **Proc-loop persistence** — trigger-condition state is permanent while carried (CWDT gem socketed = trigger armed; no expiry).

### 2.8 Sim-side resolution point

**Consumer site:** `combatant.py:tick` — the per-tick loop where movement_factor + resource regen resolve. PC entries in `active_effects` with `name="persistent_condition"` consume tick_cost (if sub-shape="tick-cost") OR fire trigger check (if sub-shape="proc-loop"). Activation-toggle sub-shape is stateless-in-tick — it just carries the aura's stat modifiers on `active_effects`.

**Placement:** BEFORE damage resolution — PC state modifiers (aura's +damage buff, frenzy stack's +attack speed) apply to the tick's damage calculations. Proc-loop trigger check fires AFTER damage resolution (if incoming damage triggered CWDT, resolve the linked spell in the next micro-tick).

**gamora scope:** add PC-effect lookup + tick_cost drain + trigger_check at `combatant.py:tick`; wire into damage-tick path in `damage_resolver.resolve_skill` for stat-modifier composition.

**Attribution:** PC state modifier contributions to total damage are telemetrable via extending E3 attribution spine — stamp `source_persistent_condition` on the ActiveEffect and propagate through damage attribution.

### 2.9 Gen-side emission surface

- **`bc_target_composer._ECON_BIN_COST_TYPE_MAP`** — add entry: `"persistent-condition": ["mana", "focus", "rage"]` (all three primary maintenance-resource families).
- **`bc_target_composer._DEFERRED_ECON_BINS`** — NO CHANGE for PC (PC is a NEW active bin; drop only applies to `charge-stack` per §4).
- **`resource_economy.py`** — add 4 new fields per §2.4 (persistent_condition_shape, persistent_tick_cost, activation_cost, proc_trigger_condition).
- **`substrate_templates.py`** — new templates: `paladin_aura_of_X`, `barbarian_frenzy_state`, `proc_loop_trigger`.
- **`commitment_state_machine.py`** — 1 or 2 new commitment states per ESCALATION e.

### 2.10 DL-03 conformance

**DL-03 (streams never tax movement):** aura-toggle and tick-cost sub-shapes emit auras which are `tags=["placed"]` (self-centered zone) — do NOT tax player movement. Player Auradin walks around while aura ticks. Proc-loop sub-shape triggers ARE cast events but the player is not "casting" them — the game fires them; player continues moving. **DL-03 conformance passes for all three sub-shapes.**

### 2.11 Calibration guardrails (gamora tunes)

- **HARD guard: `persistent_tick_cost.max = 5.0/s`** — prevents runaway drain; D2 Auradin at endgame consumes ~2/s.
- **SOFT guard: `activation_cost.default = 20`** — tune band 10–40 based on gauntlet response.
- **Proc-loop interaction with cooldowns:** proc-loop trigger firing should respect linked-skill cooldowns (CWDT semantic — trigger fires but skill on cooldown = no cast). gamora smoke-gate: verify proc-loop does not exceed linked-skill's cadence limit.
- **PC × sunder × poison worst-case:** aura amp'ing damage that ticks a poison on a sundered target. Verify S6 gauntlet DPS ceiling.

---

## §3 — Econ-bin: `reservation` (RS — 42 kits, the aura/reservation family)

### 3.1 Delegated ruling recorded (Matt 2026-07-16 autonomous-run, veto-open)

**RS = the reservation model:** a permanent regen-cap tax on the maintenance-resource pool while the aura/reservation is active. **PoE1 native semantics** (percent-reservation auras: Grace, Determination, Discipline, Herald-of-X). **D4 Auradin paladin** (holy aura reserving fury). **LE Ghostflame Warlock** (ward reservation). **D3 Helltooth Gargantuan / Inna Mystic Ally** (summoner-slot-reservation). **D2 Summon Druid** (spirit-slot reservation).

**Distinction from PC:** RS is a permanent-tax (regen_cap -= X while active); PC is a per-tick tax OR an activation-cost + free-maintenance. Wave-A already built RS-for-summoners (`summon_economy.reservation_per_proxy`). Wave B generalizes to non-summoner auras.

### 3.2 Mechanic definition

Reservation = **a percentage OR flat magnitude subtracted from a resource pool's regen ceiling while the reservation is active**. Multiple reservations may compose (subject to a per-pool total-reservation cap); regen continues on the un-reserved fraction.

**Genre precedent** (RS roster attestation, 42 kits):
- **PoE1 Aurabot, Solo Aurastacker, Low-Life Shavronne's, Death's Oath, Skeleton Mages, Golementalist** — %-reservation aura model (canonical PoE1)
- **D2 Summon Druid** — summon-slot reservation
- **D3 Helltooth Gargantuan, Inna Mystic Ally** — summoner-slot reservation
- **D4 Auradin Paladin, Minion Necromancer** — modern-Diablo reservation
- **LE Ghostflame Warlock** — LE ward-reservation

### 3.3 Representation choice (ARCHITECTURAL ESCALATION b)

**Options:**
- **(i) %-of-max-cap reservation** — regen_cap = max_pool × (1 − Σ reservation_percent). PoE1-native; per-pool total cap invariant enforceable (Σ < 1.0). Composition semantics identical to PoE1 aurastacker.
- **(ii) Flat-magnitude reservation** — regen_cap = max_pool − Σ reservation_flat. Wave-A A3 `reservation_per_proxy` uses this shape (a flat number of regen-cap units per active proxy).
- **(iii) Hybrid — flat for summoner-slot RS, %-of-max for aura RS** — matches how the genre actually models it (PoE reservations are %; D2 summoner-slots are integer counts).
- **gandalf lean: (iii) hybrid.** Grounds: forcing summoner-slot into %-model is fine mathematically but semantically wrong (D2 has "3 skeleton warriors + 2 skeleton mages" — that's 5 flat slots, not "50% of body-space"). PoE aura %-model is the corpus's dominant non-summoner RS shape. Hybrid matches evidence AND lets Wave-A A3's flat model live unchanged (backward compat). Impact: `resource_economy` gains TWO reservation fields (`reservation_percent` + `reservation_flat`), one or both non-zero per kit.

**ESCALATION b — Matt/KR ruling owed:** ratify (i) or (ii) or (iii) before rocket extends composer. Impact: one vs two new resource_economy fields; invariant enforcement shape (Σ percent ≤ some cap vs Σ flat ≤ max_pool).

### 3.4 Params + defaults + ranges (extending resource_economy.py)

Assuming ruling (iii) hybrid:

```yaml
# resource_economy per-kit fields (rocket emits; gamora reads)
reservation_percent:         # NEW — for %-of-max aura RS (i-shape)
  min: 0.00
  max: 0.75                  # RUNAWAY-GUARD (LOCKED): no single reservation exceeds 75%
  default: 0.30              # PoE1 aura default (~35% for Grace/Determination)
reservation_flat:            # NEW — for flat-count summoner-slot RS (ii-shape) [Wave-A shared]
  min: 0.0
  max: 25.0                  # RUNAWAY-GUARD (LOCKED): no single reservation exceeds 25 flat units
  default: 5.0
reservation_resource:        # WHICH pool is taxed
  min: null
  max: null
  default: "mana"
  # one of: {"mana", "focus", "stamina-as-resource", "rage"}
# INVARIANT: Σ reservation_percent per pool < 0.90 (LOCKED — never allow >90% reservation total)
# INVARIANT: Σ reservation_flat per pool ≤ 0.75 × max_pool (LOCKED — same 75% ceiling in flat units)
```

**Calibration ranges (gamora tunes):** `reservation_percent.default` 0.30 is PoE1-aura median; band 0.20–0.50. `reservation_flat.default` 5.0 matches Wave-A A3 slice-2 defaults.

### 3.5 Application sources

- **Holy/Auradin family** — % reservation for auras.
- **Necromancer/Summoner family** — flat reservation for slot-count (extends Wave-A A3 machinery to Golementalist / Skeleton Mages / Helltooth Gargantuan).
- **Warlock/Ghostflame** — flat reservation for ward-magnitude (LE Ghostflame Warlock precedent).
- **NOT ailment DoT skills** (poison, burn own their space; reservation would be economy-double-dipping).
- **NOT physical melee combo** (rage/combo already handle spend-model).

Rocket authorship: `element_biases.py` gains a `RESERVATION_BIAS` map keyed by element + role_orientation.

### 3.6 Stacking + composition law

- **Per-pool total-cap invariant** — the LOCKED runaway guard. Σ reservation_percent per pool < 0.90; Σ reservation_flat per pool ≤ 0.75 × max_pool. Attempting to activate an aura that would breach the cap = activation blocked (no partial reservation; matches PoE1 "insufficient un-reserved" behavior).
- **Composition with existing pool regen** — regen_rate multiplied by (1 − Σ reservation_percent). Un-reserved fraction regenerates normally.
- **Cross-pool** — a mana-reservation aura does not touch focus pool. Reservation is per-resource-pool.

### 3.7 Sim-side resolution point

**Consumer site:** `combatant.py` at pool-regen tick — subtract Σ active reservations from max_pool before regen_rate applies. Existing Wave-A A3 code at `summon_economy.py` regen_cap = max(0, max_pool − reservation_per_proxy × active_count) is the direct precedent; generalize to sum over active reservation-carriers (not just proxies).

**Placement:** at pool-regen tick, BEFORE regen_rate applies.

**gamora scope:** extend Wave-A A3 regen-cap enforcement to non-proxy carriers. NO NEW ALGORITHM — same code path, wider input set.

### 3.8 Gen-side emission surface

- **`bc_target_composer._ECON_BIN_COST_TYPE_MAP`** — add entry: `"reservation": ["mana", "focus"]` (rage/combo/stamina lack the regen-cap semantics needed).
- **`resource_economy.py`** — add 2 fields per §3.4.
- **`substrate_templates.py`** — new templates: `holy_aura_reservation`, `necromancer_slot_reservation`, `ward_reservation`.

### 3.9 DL-03 conformance

**DL-03 (streams never tax movement):** reservation is a stat-tax, not a stream. Non-collision. Aura auras themselves emit stat effects while player moves freely. DL-03 **PASSES.**

### 3.10 Calibration guardrails (gamora tunes)

- **HARD guard: `reservation_percent.max = 0.75`** — single reservation ≤ 75%.
- **HARD guard: `Σ reservation_percent per pool < 0.90`** — total reservation < 90% per pool.
- **HARD guard: `reservation_flat.max ≤ 25`** — single flat-reservation ≤ 25 units.
- **Cross-check with Wave-A A3:** verify summoner-slot reservations (existing A3 kits) do not double-count under new generalized consumer.
- **Composition with PC (aura-toggle sub-shape):** an Auradin with both a %-reservation holy aura AND a Frenzy-charge PC state must not stack-tax the same pool beyond safe regen threshold. gamora smoke-gate: verify D2-Auradin-analog kit under both PC + RS load.

---

## §4 — Econ-bin: `charge-stack` (existing bin lift) — sub-shape `accumulator` (AM, 16 kits) + sub-shape `cycle` (RC, 16 kits)

### 4.1 Delegated ruling recorded (Matt 2026-07-16 autonomous-run, veto-open)

**AM and RC are two sub-shapes of ONE engine bin — the existing `charge-stack` bin** (already in composer's `_ECON_BIN_COST_TYPE_MAP` at `[]` = DEFERRED; already in `_DEFERRED_ECON_BINS`). Wave-B action = **DROP `charge-stack` from `_DEFERRED_ECON_BINS`** + populate its cost_type mapping + add a `charge_stack_sub_shape` field to distinguish AM (accumulator) from RC (cycle).

**Distinction:**
- **AM (accumulator)** = the meter FILLS from external events (kills, damage-dealt, corpses, evolution-conditions) and DISCHARGES on trigger. VS evolutions (Holy Wand, Thousand Edge — evo-condition-met), Wormblaster (worm-charge builds), Corpse Explosion (corpse-count consumed), grenadier ammo, Trap Magician (trap-charge). The player does NOT set the fill rate — it's world-driven.
- **RC (cycle)** = the meter DEPLETES from use and REFILLS on time-cooldown. VS weapon auto-fire (Holy Wand as RC = auto-projectile cycle), D2 Throw Barb (throwing-weapon ammo), Cadence Witchblade (charge-up cycle), Krieg Death Knight (weapon-swing cycle), Runic Invocation Runemaster (rune-slot cycle). Time-refilled or use-refilled.

### 4.2 Mechanic definition

**Accumulator (AM):**
- State variable `accumulator_current` accumulates on trigger events (kill, damage-taken, damage-dealt, kill-count, evolution-condition-met).
- Player consumes accumulator on activation (spends threshold to fire linked skill).
- Overflow behavior: caps at `accumulator_max`.

**Cycle (RC):**
- State variable `cycle_charges` starts at `charge_max`, depletes on use.
- Refills on time-cooldown (`recharge_seconds`) OR on external event (kill, reload action).
- No overflow; caps at `charge_max`.

**Genre precedent** (roster):
- AM: VS evolutions, PoE1 Wormblaster (worm-count), PoE2 Witchhunter Grenades (grenade-ammo), DI Corpse Explosion (corpses), TQ Trap Magician (traps), TQ2 Forge Turrets (turret-count), TL2 Shotgonne Outlander (ammo), TLi Carino2 Lethal Flash (charge), TLi Sage Elixir Kit (potion-uses)
- RC: D2 Throw Barb (throwing-weapons deplete + reload), VS weapon evos (cooldown-cycle), GD Cadence Witchblade (cadence-cycle), GD Krieg Death Knight (swing-cycle), LE Runic Invocation Runemaster (rune-slot-cycle)

### 4.3 Category classification (ARCHITECTURAL ESCALATION c)

**Options:**
- **(A) ONE bin `charge-stack`, sub_shape ∈ {"accumulator", "cycle"}** — matches existing engine reality (`charge-stack` already exists as deferred bin); minimal composer change; sim consumer branches on sub_shape.
- **(B) TWO bins — `accumulator` + `cycle`** — semantic clarity; two composer entries; two consumer sites.
- **gandalf lean: (A) one bin.** Grounds: the composer already carries `charge-stack` as a deferred bin — lifting it and adding a sub_shape field is a SMALLER engine change than adding two brand-new bins. The mechanical difference (fill-from-world vs cycle-with-cooldown) is significant for sim consumer but not for composer routing (both route through the SAME `charge-stack` cost_type map). ESCALATION c can revisit if S6 gauntlet reveals divergent balance needs.

> **⚑ Gate-1 STRIKE (jack-ryan 2026-07-16, note #1 resolved — EMISSION SURFACE WINS):** the original lean-parenthetical here read "both need same cost_type_map = `[]` — the meter IS the resource." **STRUCK — code-refuted.** `resolve_cost_type` (`bc_target_composer.py:247`) returns `role_priority[0]` (a valid family, e.g. `mana`) when the feasible map is `[]` (:274) — an empty map does NOT express "no cost," it silently resolves to mana. An empty map is DEFERRED semantics (the bin never reaches the resolver at all while it sits in `_DEFERRED_ECON_BINS`). A LIFTED active bin MUST carry a resolvable non-empty map. §4.8/§12.1's `["mana", "focus", "stamina-as-resource"]` is therefore the correct emission surface; zero-marginal-cost kits (D2 Throw Barb auto-fire, VS evo auto-cast) express near-zero cost via `cost_scale` in `resource_economy.py`, NOT via an empty cost_type map.

**ESCALATION c — Matt/KR ruling owed:** ratify (A) or (B) before rocket extends composer. Impact: 1 bin lift + 1 sub_shape field vs 2 new bins + 2 composer entries.

### 4.4 Params + defaults + ranges (extending resource_economy.py)

Assuming ruling (A):

```yaml
# resource_economy per-kit fields (rocket emits; gamora reads)
charge_stack_sub_shape:      # NEW — required for kits in charge-stack bin
  min: null
  max: null
  default: null
  # one of: {"accumulator", "cycle"}
# Accumulator (sub_shape=accumulator) fields:
accumulator_max:             # NEW
  min: 1
  max: 100
  default: 10
accumulator_fill_trigger:    # NEW
  min: null
  max: null
  default: "on-kill"
  # one of: {"on-kill", "on-hit-taken", "on-hit-dealt", "on-evolution-condition-met", "on-corpse-consume"}
accumulator_fill_amount:     # NEW
  min: 1
  max: 25
  default: 3
accumulator_discharge_threshold:  # NEW
  min: 1
  max: 50
  default: 5
# Cycle (sub_shape=cycle) fields:
charge_max:                  # NEW
  min: 1
  max: 20
  default: 6                 # D2-Throw-Barb-analog default
recharge_seconds:            # NEW
  min: 0.5
  max: 30.0
  default: 5.0
recharge_source:             # NEW
  min: null
  max: null
  default: "time"
  # one of: {"time", "on-kill", "on-reload-action"}
```

**Calibration ranges (gamora):** all ranges S6-tuned; primary invariant is that per-encounter charge-throughput does not exceed the mana-analog-per-encounter throughput of comparable spend-model kits.

### 4.5 Application sources

- **AM (accumulator):** VS-family evolutions (thematic fit — kills/actions build meter), necromancer corpse-consumption, physical-projectile ammo-count, trap/turret-count. Rocket routes via kit-tag `substrate_templates` `evolution_meter`, `corpse_meter`, `ammo_meter`, `trap_meter`.
- **RC (cycle):** Physical throwing / ranged weapons with reload semantic, VS auto-fire weapon cycles, GD cadence-tag kits, rune-slot systems. Rocket routes via `substrate_templates` `throwing_reload`, `auto_fire_cycle`, `cadence_cycle`, `rune_slot_cycle`.

### 4.6 Stacking + composition

- **One-active-per-kit** — a kit is either AM OR RC, not both (attested in corpus: no kit tags both).
- **Multi-kit-per-player** — a player build MAY have a charge-stack (AM) primary + a spend-model secondary. Composition orthogonal.

### 4.7 Sim-side resolution point

**Consumer site:** `combatant.py:tick` per-tick loop reads `accumulator_state` OR `cycle_charges` from active_effects; increments/decrements per event.

**Placement:** at per-tick event resolution — AM fill fires on kill/hit event; RC decrement fires on skill cast; RC recharge fires on timer tick.

**gamora scope:** new state carrier per-sub-shape; wire event listeners for AM fill triggers; timer-based recharge for RC.

### 4.8 Gen-side emission surface

- **`bc_target_composer._ECON_BIN_COST_TYPE_MAP`** — change entry `"charge-stack": []` → `"charge-stack": ["mana", "focus", "stamina-as-resource"]` (kits still pay marginal costs for skill activation; the CHARGE is the constraint but skill cost still consumes small amount).
- **`bc_target_composer._DEFERRED_ECON_BINS`** — DROP `"charge-stack"` from the frozenset (mirroring Wave-A `_DEFERRED_PROXY_BINS` drain to `frozenset()`).
- **`bc_target_composer.check_infeasibility`** — remove the `charge-stack → DEFERRED` branch (already implicit once bin is dropped from `_DEFERRED_ECON_BINS`).
- **`resource_economy.py`** — add 7 new fields per §4.4.
- **`substrate_templates.py`** — new templates listed in §4.5. **[Gate-1 note: `substrate_templates.py` ALREADY carries a `W1_4_CHARGE_STACK` family of ~25 templates (`charge_up_*`, `stack_builder_*`, `charge_decay_*`, `multi_charge_*`, `charge_on_hit_*`, `overdrive_*`) from Cycle-12 Layer-3. rocket EXTENDS/REUSES that family (add the AM/RC sub-shape routing + any missing `evolution_meter`/`ammo_meter`/`throwing_reload` templates), NOT greenfield-authors — the charge-stack substrate scaffold predates this lift. Verify overlap before authoring to avoid duplicate template_ids.]**

### 4.9 DL-03 conformance

**DL-03 (streams never tax movement):** AM fill happens on world-events (kills, hits) — player moves freely. RC cycle depletes on cast; the CAST itself may be a stream (VS auto-fire is a stream-projectile) — DL-03 binds per-skill authoring: any RC-carried stream must be `tags=["placed"]` or free-fire, not caster-held-channel. **RC RESOLVED at Gate-1: rocket authors RC-carried streams as auto-fire-while-moving pattern per VS precedent.** DL-03 **PASSES.**

### 4.10 Calibration guardrails

- **HARD guard: `accumulator_max ≤ 100`** — prevents unbounded meter accumulation.
- **HARD guard: `charge_max ≤ 20`** — prevents machine-gun ammo abuse.
- **HARD guard: `recharge_seconds.min = 0.5`** — prevents zero-cooldown charge cycling.
- **AM × sunder × ailment worst-case:** high-accumulator VS-evo firing amp'ed damage on sundered targets with ailment ticks — verify S6 DPS ceiling. VS-family is a known DPS outlier; verify it doesn't blow past intended power tier.

---

## §5 — Cross-bin interaction contracts (with Wave-A + ailment layer)

### 5.1 Wave-B × Wave-A (summon/proxy)

| A × B | Interaction | Notes |
|---|---|---|
| RS × Wave-A A3 (proxy-reservation) | **SAME BIN, DIFFERENT CARRIERS** — Wave-A A3's `reservation_per_proxy` = the flat-shape RS §3.3 (ii); Wave-B RS extends the same machinery to non-proxy carriers | No new algorithm; gamora widens consumer input set |
| PC × summon-slot | Some PC kits ALSO summon (D2 Summonmancer, Tainted Summoner Warlock — attested `["PC"]` in econ_gaps but summoner in mechanic) | Sim consumer reads BOTH active_effect PC entry AND summon economy proxy count |
| AM × summon-count | AM meter as summon fuel (D3 Helltooth Garg-adjacent) | Rocket's `substrate_templates` allows AM `accumulator_fill_trigger="on-kill"` + linked-skill = summon spawn |
| RC × summon-cadence | Wave-A A1 (cooldown-gated summon economy) is essentially an RC-cycle with `recharge_source="time"` | Ratify these as ONE bin at consumer level; Wave-A A1 semantics preserved |

### 5.2 Wave-B × ailment layer (in flight; Gate-2 pending)

| A × B | Interaction | Notes |
|---|---|---|
| PC × sunder | Persistent-condition state modifiers (e.g., aura-of-fury adds +20% damage) compose with sunder amp at damage_resolver composition | Multiplicative; verified in ailment spec §7 |
| PC (proc-loop) × any ailment | Proc-loop fires linked skill; linked skill applies its own ailments per emission | No special-case; proc-loop is a trigger, not a cost-model change to the linked cast |
| RS × any ailment | Reservation is stat-tax only; no interaction with ailment resolution | Non-collision |
| AM (kill-fill) × poison-stack | Killing poisoned targets fills AM meter; ordering matters at kill-event resolution | gamora smoke-gate: verify kill-fires-before-death-triggers-attribution |
| RC × ailment auto-fire | RC-carried stream (VS Holy Wand) applies ailments on hit; ailment application is per-projectile | Standard ailment auto-apply; no special-case |
| RC × freeze-shatter | RC-carried skill freezing target then shattering: RC cycles continue normally through shatter event | Non-collision |
| PC (Auradin aura) × ailment (consecrate) | Aura-based holy amp state × existing consecrate amplification-zone: both apply to allies in range | Composition rules per ailment spec §7 (consecrate × sunder) |

### 5.3 Wave-B × existing econ bins (generator-spender, starved, overflow, steady)

- **Cross-bin exclusivity**: a kit is emitted with ONE econ_bin per composer contract. Wave-B introduces NO new cross-bin composition rules. A player build may have multiple kits with different econ_bin values (mana-spender + reservation-aura + charge-stack), but each kit's own emission is single-bin.
- **Composer route preservation**: existing `generator-spender`, `starved`, `overflow`, `steady` behavior UNCHANGED. Wave B is additive.

> **⚑ Gate-1 RULING (jack-ryan 2026-07-16, ruling-10 NR rider — `steady`-absorbs, NO new bin):** the "NR no-resource ×4" question is ruled: **NR kits route to the existing `steady` bin with near-zero cost expressed via `resource_economy.cost_scale ≈ 0`, NOT a new econ_bin.** Grounds: (1) NR is NOT a scoreboard bucket and carries ZERO `econ_gaps` tokens in the corpus (`SELECT COUNT WHERE econ_gaps LIKE '%NR%'` = 0) — there is no ranked NR roster to amortize a bin against, unlike PC/RS/AM/RC. (2) `steady` (`["mana","focus","stamina-as-resource"]`) already resolves a valid cost_type; `resource_economy`'s DEFAULT-corner + `cost_scale` range `(0.60, 1.60)` already spans near-zero-effective-cost when scaled down, and the sim treats a near-zero per-cast cost as a no-op on the pool (the byte-reproduction default-corner logic, `resource_economy.py:50`). (3) A dedicated "no-resource" bin would carry the SAME empty-map hazard §4.3 was struck for — the resolver returns mana on `[]` anyway, so "no cost" is a `cost_scale` concern, not a bin concern. **Disposition: no Wave-B action. If a future census surfaces a ranked NR roster (>~10 kits), reopen as a Wave-C `cost_scale`-floor calibration item, not a new bin.**

### 5.4 DL-03 CRITICAL cross-check (whole spec)

DL-03 (Matt 2026-07-12 design law: streams never tax movement) binds specifically:
- **PC**: aura-toggle/tick-cost = `tags=["placed"]`; proc-loop = trigger-passive, player never streams. PASS.
- **RS**: stat-tax; no stream. PASS.
- **AM**: meter is state; discharge fires a skill (skill-level DL-03 authored). PASS at bin level.
- **RC**: cycle-carried streams (VS auto-fire) explicitly `tags=["placed"]` per §4.9 amendment. **RESOLVED at Gate-1.** PASS.

DL-03 explicitly satisfied for Wave B.

---

## §6 — Post-Wave-B registry (before-and-after)

**Before Wave B** (`_ECON_BIN_COST_TYPE_MAP` current state):
- 7 keys: HP-economy (DEFERRED), charge-stack (DEFERRED), damage-taken-converts (DEFERRED), generator-spender, starved, overflow, steady
- 3 in `_DEFERRED_ECON_BINS`
- 1 hard-infeasible (HP-economy per LC-030)

**After Wave B** (post gate-lift):
- 9 keys: 2 DEFERRED (HP-economy [WAVE-C], damage-taken-converts [WAVE-C — 3 TH thorns-reflect kits currently in `econ:UNKNOWN`, re-tag owed]), 7 ACTIVE (generator-spender, starved, overflow, steady, **charge-stack** [lifted], **reservation** [NEW], **persistent-condition** [NEW])
- 2 in `_DEFERRED_ECON_BINS`
- 1 hard-infeasible (HP-economy — LC would-be-here per §7 deferral; DR's home is the open §7.3 question)

**Delta:** +2 new bins; −1 lifted bin; +1 new sub-shape tag on charge-stack. Kit-touch: +118 (44 PC + 42 RS + 16 AM + 16 RC).

---

## §7 — LC + DR triage — Wave-C deferral (ESCALATION d)

### 7.1 Delegated ruling recorded (Matt 2026-07-16 autonomous-run, veto-open)

**LC (life-cost, 3 kits) + DR (drain, 2 kits) DEFER TO WAVE C.**

### 7.2 Grounds

**LC roster (3 kits):**
- `le-reaper-form-lich` — LE Reaper Form Lich (necrotic self-life-cost)
- `poe2-grim-feast` — PoE2 Grim Feast Overleech (life-cost with overleech gain) [`["RS", "LC"]` overlap]
- `hades1-aspect-guan-yu` — Hades Aspect of Guan Yu Spear (life-cost per swing)

**DR roster (2 kits):**
- `vs-queen-sigma` — Vampiric Survivors Queen Sigma (drain-adjacent)
- `hot-norseman-frost-avalanche` — Heroes of the Titan Frost Avalanche (drain pattern)

**Why defer:**
1. **`HP-economy` bin is HARD-INFEASIBLE per LC-030** (composer :313: "pool has zero HP-cost skill mechanics — LC-030 confirmed"). Ratifying LC/DR into Wave B requires FIRST reversing LC-030 — a pool-content decision, not a spec-lift.
2. **Thin roster** — 5 kits total across both bins; the gate-open cost (`HP-economy` mechanic set + `damage-taken-converts` mechanic set + new sim consumers) does not amortize over 5 kits the way Wave B amortizes over 118.
3. **Wave-A A3 already carries a partial-LC pattern** — the `["RS", "LC"]` overlap on `poe2-grim-feast` suggests LC ends up cross-cutting with reservation; better to spec LC when the fuller cross-cut is understood.
4. **DR is a VS-family adjacency signal** — auto-fire-while-moving with drain-feel is VS-specific; may not survive V3 mechanics-leverage weighting.

### 7.3 What Wave C picks up

Wave-C econ-family scope (post Wave B):
- Revisit LC-030 finding: is HP-economy still zero-mechanics after Wave-B economy adds? IF yes, deprecate `HP-economy` bin from composer permanently. IF no (Wave B introduces LC-adjacent mechanics via cross-cuts like PoE2 Grim Feast), promote LC to a Wave-C bin.
- DR as a `charge-stack` sub-shape variant (drain = cycle-with-negative-refill) OR as standalone Wave-C bin.
- `damage-taken-converts` (CWDT-adjacent) — Wave-B PC proc-loop sub-shape may cover this; verify at Wave-B S6 cert.

**ESCALATION d — Matt/KR ruling owed:** ratify Wave-C deferral for LC + DR. Impact: 5 kits stay blocked until Wave C; Wave-B ships with 118-kit unblock instead of 123-kit unblock.

---

## §8 — Post-spec registry (after Wave B lands)

Full econ_bin registry becomes 9 bins:

| Bin | Status | Kit-touch | Composer entry | Sim consumer |
|---|---|---|---|---|
| `mana` / `focus` / `stamina-as-resource` families (existing) | ACTIVE | (existing base) | existing 4 bins | existing |
| `persistent-condition` | ACTIVE (NEW) | 44 | `["mana", "focus", "rage"]` | spatial_engine per-tick loop + `effect_resolver.tick_effects` + `damage_resolver.resolve_skill` stat-mod composition |
| `reservation` | ACTIVE (NEW) | 42 | `["mana", "focus"]` | spatial_engine pool-regen tick (extends Wave-A A3 `reservation_per_proxy`) |
| `charge-stack` | ACTIVE (LIFTED) | 32 (16 AM + 16 RC) | `["mana", "focus", "stamina-as-resource"]` | spatial_engine per-tick loop + `effect_resolver.tick_effects` per sub-shape |
| `HP-economy` | DEFERRED (Wave C) | 3 (LC×3: 2 `["LC"]` + 1 `["RS","LC"]` overlap) | `[]` | (Wave-C build) |
| `damage-taken-converts` | DEFERRED (Wave C) | 3 (TH thorns-retaliation, econ_gaps=`["UNKNOWN"]`, NOT yet bin-tagged) | `[]` | (Wave-C build) |

Total Wave-B unblock: **118 kits**.

> **⚑ Gate-1 CORRECTION (jack-ryan 2026-07-16, note #3 + ruling-10 TH rider):** two prior-row errors fixed. **(1) `HP-economy` kit-touch** was loosely "3 (LC + 2 overlap)" — corrected to LC×3 exactly (corpus: `["LC"]`×2 + `["RS","LC"]`×1). DR's 2 kits are NOT HP-economy-mapped (drain's Wave-C home is the open §7.3 question, not pre-assigned to HP-economy). **(2) `damage-taken-converts` kit-touch** was "0" — corrected to **3**. The "0" was the count of the `damage-taken-converts` *econ_gaps token*, which is genuinely 0, but a real thorns-retaliation roster EXISTS mechanically: corpus folk_names *Retaliation Warlord* (gd), *Thorns Barbarian* (d4), *Thorns Invoker* (d3) all carry econ_gaps=`["UNKNOWN"]` (they sit in the scoreboard's `econ:UNKNOWN=38` bucket, §3 row 5) and are damage-taken-converts-family (retaliation = passive reflect keyed off damage-taken, NOT a trigger-cast — so PC proc-loop does NOT cover them). A 4th thorns kit (*Thorns Barrier Templar*, chronicon) is already tagged `["PC","BT"]` and rides PC. **Wave-C park stands** — the 3 stay deferred to Wave C — but the count is 3, not 0, and the park rationale is "unclassified thorns-reflect roster needs a `damage-taken-converts` re-tag pass + a passive-reflect sim consumer, neither in Wave-B scope."

---

## §9 — Blocking vs deferrable triage

| Item | Status | Reason |
|---|---|---|
| §2 PC (all sections) | **BLOCKING** on ESCALATION a (one-active/multi-active/split) + ESCALATION e (commitment-state split) | affects composer bin count + commitment_state_machine.py structure |
| §3 RS (all sections) | **BLOCKING** on ESCALATION b (percent/flat/hybrid) | affects resource_economy.py field count + invariant enforcement shape |
| §4 charge-stack lift (AM+RC) | **BLOCKING** on ESCALATION c (one bin + sub_shape vs two bins) | affects composer entry count |
| §7 LC + DR deferral | **BLOCKING** on ESCALATION d (Wave-C defer confirmation) | affects Wave-B kit-count claim (118 vs 123) |
| PC proc-loop split (ESCALATION e) | **BLOCKING** on gamora build if e=(B); DEFERRABLE if e=(A) | affects commitment_state count |
| `damage-taken-converts` fate | **DEFERRABLE** — verify at S6 cert whether PC proc-loop covers it | Wave-C decision if orphaned |
| CWDT trigger-chain semantics | **DEFERRABLE** — PC proc-loop sub-shape covers primitive; chain-of-triggers is Wave-C | proc-grammar work per pause-2 |
| VS-family AM tuning (Holy Wand DPS ceiling) | **DEFERRABLE via S6 cert** — calibration band, not spec |
| Reservation × Wave-A A3 shared consumer refactor | **DEFERRABLE** — Wave A code stays; Wave B code extends; refactor when both stable |

---

## §10 — ESCALATIONS (5 total — RULED at gandalf verify-gate 2026-07-16; veto-open; Gate-1 stress-tests)

> **RULINGS (gandalf-prime, 2026-07-16 verify-gate, under Matt's autonomous-run delegated authority — all five ratify the drafter's leans, each on named grounds; one word from Matt reverses any):**
>
> - **a → one-active-at-a-time.** The D2 aura-slot model is the corpus's dominant PC shape by count (13/44 direct D2 kits + PoE1 multi-aura kits scored under RS `["RS", "SU"]` overlaps, not PC). Proc-loops are also one-active-per-slot at the mechanical level (one CWDT setup, one Poet's Pen wand). Splitting into (c) creates two consumer sites for a semantic distinction that resolves cleanly via sub-shape field. Player consequence: aura-swap decisions carry weight (Auradin picks Concentration OR Fanaticism, not both), matching D2's iconic build-craft.
> - **b → hybrid (iii).** Grounds beyond mechanical: PoE1 aura % model is universally understood by ARPG veterans (35% mana reserve = one aura); D2 summoner slots are integer counts (5 skeletons, not "50% of the summoner"). Forcing D2 under % misrepresents the corpus. Wave-A A3 already ships flat-shape; forcing % breaks backward compat. Hybrid respects both attested shapes. Extra invariant (Σ ≤ 90%) enforced consistently.
> - **c → one bin + sub_shape.** `charge-stack` already exists in the composer's registry (deferred). Lifting an existing bin with a sub_shape tag is SMALLER than adding two new bins. AM vs RC have DIFFERENT sim consumers (event-fill vs timer-refill) but SAME composer routing (`[]` cost_type = meter IS the resource). Consumer-level split via sub_shape field is the correct architectural boundary.
> - **d → defer LC + DR to Wave C.** LC-030 finding (`HP-economy` = pool has zero HP-cost mechanics) is a POOL-CONTENT decision; changing it requires generation-side pool expansion, which is NOT Wave-B scope. Thin roster (5 kits) does not amortize. VS-family DR is possibly a survives-V3-mechanics-leverage risk. Wave-C revisits with a wider frame.
> - **e → split commitment_state (B).** Proc-loops are FUNDAMENTALLY different from player-driven toggles — the game plays itself in CWDT/CoC/Poet's-Pen builds (afk-friendly in PoE1). Collapsing commitment_state hides the AI-agency distinction the sim needs. Aura-toggle vs proc-trigger split at commitment_state layer; unified econ_bin at composer layer.

1. **ESCALATION a (PC §2.3)** — one-active-at-a-time OR multi-active-stacking OR two-bin-split (aura + proc-loop). **RULED: one-active-at-a-time (a).**
2. **ESCALATION b (RS §3.3)** — %-of-max OR flat-magnitude OR hybrid. **RULED: hybrid (iii).**
3. **ESCALATION c (AM+RC §4.3)** — one bin `charge-stack` + sub_shape field OR two bins `accumulator` + `cycle`. **RULED: one bin + sub_shape (A).**
4. **ESCALATION d (LC+DR §7)** — ship in Wave B OR defer to Wave C. **RULED: defer (Wave C).**
5. **ESCALATION e (PC §2.6)** — one commitment_state `persistent_toggle` OR split (`persistent_toggle` + `persistent_trigger`). **RULED: split (B).**

Count check: 5, all RULED veto-open. Matches §0 TL;DR.

---

## §11 — DL-03 conformance note (whole spec)

DL-03 (Matt 2026-07-12 design law: streams never tax movement) binds specifically:
- **PC**: aura-toggle sub-shape emits `tags=["placed"]` self-centered zones (non-taxing to caster movement); proc-loop sub-shape is passive-triggered (player never streams); tick-cost sub-shape emits `tags=["placed"]` per-tick zones. PASS.
- **RS**: reservation is a stat-tax on regen_cap; no stream; no caster-movement collision. PASS.
- **AM**: accumulator is a state variable; discharge fires a linked skill whose own DL-03 conformance is authored at skill-level. Bin-level PASS.
- **RC**: cycle-carried streams (VS Holy Wand auto-fire, D2 Throw Barb) resolved at Gate-1: rocket authors as `auto-fire-while-moving` per §4.9 (VS precedent), not caster-held-channel. PASS.

DL-03 explicitly satisfied for the whole spec.

---

## §12 — Routing & sequencing (→ KR)

### 12.1 Routing (by seam owner)

**rocket (generation / config / emission):**
- `bc_target_composer._ECON_BIN_COST_TYPE_MAP` — add 2 entries (persistent-condition, reservation); modify 1 entry (charge-stack `[]` → `["mana", "focus", "stamina-as-resource"]`).
- `bc_target_composer._DEFERRED_ECON_BINS` — DROP `"charge-stack"`.
- `bc_target_composer.check_infeasibility` — remove `charge-stack → DEFERRED` branch (implicit once bin dropped).
- `resource_economy.py` — add 13 new fields (§2.4: 4 for PC; §3.4: 3 for RS; §4.4: 7 for charge-stack sub-shapes − 1 shared = ~13 total).
- `element_biases.py` — add `PERSISTENT_CONDITION_BIAS`, `RESERVATION_BIAS`, sub-shape routing for charge-stack.
- `substrate_templates.py` — new templates per §2.9, §3.8, §4.8 (~9 new templates total).
- `commitment_state_machine.py` — add 2 new commitment_states (`persistent_toggle`, `persistent_trigger`) per ESCALATION e ruling (B).

**gamora (sim / resolution / calibration):** *(Gate-1 path-fix: consumer SITE is `spatial_gauntlet/spatial_engine.py`'s per-tick loop + `effect_resolver.tick_effects`; `combatant.py` is state-only, no `tick` method — see §1 EXISTS table.)*
- `spatial_engine.py` per-tick loop (near the E4 channel-tick service :2326 / D4 `_step_proxy_population` :2189) — PC state consumer (per-sub-shape branching); AM/RC state consumers (per-sub-shape branching).
- `spatial_engine.py` pool-regen tick — extend Wave-A A3 regen-cap enforcement to non-proxy reservations (generalize `summon_economy.reservation_per_proxy × active_count` to sum-over-all-active-reservation-carriers). NO NEW ALGORITHM.
- `damage_resolver.resolve_skill` (:345) — PC stat-modifier composition step (aura's +damage buff, frenzy stack's +attack speed apply pre-mitigation).
- `effect_resolver.tick_effects` (:55) — PC tick_cost drain; AM accumulator fill on events; RC recharge timer. New per-sub-shape state carried in `ActiveEffect.params`.
- Calibration bands for all 4 new mechanisms — S6 gauntlet pass required post-emission (parallels Wave-A `proxy-light`/`proxy-heavy` cert).

### 12.2 Sequencing (LEAN — KR sequences)

1. **First slice — RS (extends Wave-A A3; smallest new-code delta; 42-kit unblock)** — rocket adds composer entry + resource_economy fields; gamora generalizes A3 regen-cap consumer.
2. **Second slice — PC (biggest new bin, 44-kit unblock)** — rocket adds composer entry + commitment_state extensions + 4 new resource_economy fields + templates; gamora builds three-sub-shape consumer (tick-cost, activation-toggle, proc-loop).
3. **Third slice — `charge-stack` lift (AM + RC parallel, 32-kit unblock)** — rocket lifts bin + adds sub_shape field + resource_economy fields; gamora builds two-sub-shape consumer (accumulator, cycle).
4. **S6 gauntlet cert pass** — all 3 new bins certify through S6 matchup gate; calibration bands validate; DL-03 conformance validates; runaway-guard invariants hold; no cross-bin composition breaks.
5. **Gate lift ships** — `_DEFERRED_ECON_BINS.discard("charge-stack")` + composer entries active. Wave-B expressible-now = 118 kits added to census (V8 delta expected).
6. **Post-Wave-B S2 census V8 rerun** — verify 118-kit shift from blocked to expressible; delta report.

**Cross-slice sequencing observations (KR):**
- RS + Wave-A A3 code proximity: RS ships first because it REUSES existing code; PC ships second because it introduces new commitment_state; charge-stack ships last because two-sub-shape consumer is largest new build.
- Ailment-layer Gate-2 (in flight) does NOT block Wave B; interaction contracts (§5.2) hold across both. Wave-B and ailment-layer teams may parallel-execute.
- LC + DR (Wave C) deferral does NOT block Wave B ship; escalation d ruling holds.

---

## §13 — Cross-references

- Scoreboard: `agentic_orchestration/research/curated/atlas/s2-readiness-census-v7-2026-07-16.md` (§2 bucket ranking, §3 bucket detail rows 2/4/8/9 = PC/RS/AM/RC; row 16 = LC; row 21 = DR)
- Form model: `agentic_orchestration/gandalf/design-inputs/wave-a-engine-spec-2026-07-13.md` (§2 A3 reservation precedent, §9 `_DEFERRED_PROXY_BINS` gate pattern, §11 routing template)
- Sibling Gate-1-PASS spec: `canonical/reap-die-rise-engine/ailment-layer-engine-spec.md` (§0 TL;DR shape, §1 EXISTS table shape, §10 ESCALATIONS + verify-gate ruling shape, §11 DL-03 conformance section)
- Composer + deferred set: `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/bc_target_composer.py` (`_ECON_BIN_COST_TYPE_MAP` :236, `_DEFERRED_ECON_BINS` :95, `resolve_cost_type` :247, `check_infeasibility` :304)
- Wave-A A3 precedent: `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/summon_economy.py` (`ECONOMY_RESERVED` :39, `reservation_per_proxy` :59, `reservation_resource` :60, math note `notes/wave-a-slice2-a3-reservation-math-2026-07-13.md`)
- Per-kit resource_economy: `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/resource_economy.py`
- Commitment-state: `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/commitment_state_machine.py`
- Ailment-layer LC-030 finding: `bc_target_composer.py:313` ("pool has zero HP-cost skill mechanics — LC-030 confirmed")
- Corpus evidence: `agentic_orchestration/research/curated/corpus.db` (READ-ONLY; queries derived §2, §3, §4, §7 rosters per bin from `canon_engine_key.econ_gaps` + `canon_corpus.game/folk_name` join; primary + any-occurrence + 2-way overlap counts §0 table)

Tracker-delta: NEW SPEC `canonical/reap-die-rise-engine/wave-b-economy-engine-spec.md` — 2 new econ_bin values (persistent-condition, reservation) + 1 lifted deferred bin (charge-stack) + 2 sub-shapes (accumulator, cycle) + LC/DR Wave-C deferral triage; draft-for-Gate-1; 5 escalations flagged; gandalf-prime consolidates into engine tracker.
