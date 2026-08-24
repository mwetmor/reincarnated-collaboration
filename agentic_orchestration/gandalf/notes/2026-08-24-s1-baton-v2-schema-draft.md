# S-1 — baton-v2 SCHEMA DESIGN DRAFT (two-layer playable model-pack)

> ▶ **ROLE: SPEC-AUTHOR** — S-1 baton-v2 schema draft.
>
> **STATUS:** DRAFT — Wave-1 deliverable of the KC2 MODEL-COMPLETION RUN. **Spec, not code.** Implementation is Wave 4 (star-lord / gamora).
> **Date:** 2026-08-24 · **Author:** gandalf (named sub-agent, `SPEC-AUTHOR`) · **Conductor:** gandalf `RUN-CONDUCTOR`
> **Authority:** charter `agentic_orchestration/gandalf/notes/2026-08-24-kc2-model-completion-run-charter.md` · rulings `…/2026-08-24-kc2-model-pack-reframe-and-gap-rulings.md` (RULING-NOTE)
> **Standing law binding on every line below:** **Law 3** (no fitted constants, no invented rules) · **D5** (`E-s09-cp150` immutable; siblings only) · **GL-6** (verify digest before load) · **GL-12** (absence is DECLARED, not filled) · wave-160 is a **GRADED ROW, never a gate**.

---

## 0 · Headline — what changes, in one paragraph

v1 is a **recording**: a wire the Godot side plays back under a zero-derivation law (`kc2_baton.gd`: *"this file computes no damage, resolves no hit, decides no death, and moves nothing the baton did not move"*). v2 is a **model-pack**: the rules of the fight, such that a Godot **runtime** derives damage, resolves hits, and decides deaths itself — plus a *separate* recorded fight that acts as the acceptance test proving it derived them the same way the sim does. This inverts the consumer's constitutional law, so **v2 is a breaking cut with a new consumer contract**, not an extension of v1.

Three schema-design rules carry the weight, and everything in §§ 1–4 is an application of them:

- **DR-1 — Every leaf carries a provenance id, or the pack does not validate.** No field may exist whose only possible source is a guessed value (Law 3, mechanised). The provenance registry is closed-enum and the validator fails on `null`.
- **DR-2 — Anything whose knowledge is expected to GROW is a keyed collection, never a set of named optional fields.** The D-1/D-2/D-3 decode laps land new AI states, new reuse gates, new field groups. Those are **rows with a provenance column**, so a lap adds data without a schema version bump. (Corollary: the 43-state controller taxonomy is the *key space*; the sim's current 9 are rows that exist, the other 34 are rows marked `DECLARED-ABSENT` or `UNREACHABLE` with reasons.)
- **DR-3 — A parameter is a `(value, scope, provenance)` triple with an explicit precedence chain, never a scalar.** Forced by the ⚑ ViewDistance contradiction: 15.0 m population-wide (WR3-W2) vs **80.0 m on 169/169 rolled tier-16 Crucible monsters** (Lap U). Both are measured; both are true in their scope. A scalar field would have to pick one and thereby lie.

And one architectural idea that is the whole point of the pack:

> **The guess, if any, is made by the CONSUMER and labelled as the consumer's — never laundered through the baton as model truth.** A live runtime must do *something* where the model is silent. The pack's job is to make every such site explicit, enumerable, and countable (`declared_absent[]` with `blocks_playability`), so "the Godot team guessed here" is a fact on the record rather than a rumour in the code.

---

## 1 · PACK SHAPE — a directory of files, not one JSON (recommended)

**Recommendation: a digest-pinned directory pack, with Layer 1 and Layer 2 as independently versioned artifacts.**

```
kc2-model-pack-v2-<source>-<stamp>/
  manifest.json                    ← pack root; per-member sha256 + pack digest + layer versions
  model/                                                    ← LAYER 1 (the rules)
    meta.json                      ← schema_version, pack_format, source pins, tick+RNG contract ref
    provenance.json                ← the provenance REGISTRY + declared_absent REGISTRY (§5)
    arena.json                     ← geometry, spawn points, containment model (§2.6)
    ai_states.json                 ← the controller state machine: states + transitions (§2.1)
    monsters.json                  ← N stat blocks, skills, specials + reuse gates, DoT riders (§2.2)
    player_kit.json                ← 9 bar skills, 8 devotion procs, Menhir's Will, potions (§2.3)
    summons.json                   ← 2 player summons as first-class actor templates (§2.3d)
    math_rules.json                ← damage / mitigation / leech as evaluable blocks + vectors (§2.4)
    waves.json                     ← per-wave spawn structure + (if decoded) the roll rules (§2.5)
    rng_contract.json              ← tick contract, draw-site registry, ordering law (§2.7)
  reference/                                                ← LAYER 2 (the acceptance test)
    meta.json                      ← the sibling checkpoint pin (sha, seed, sim version)
    tracks.json                    ← recorded player path / hp / energy / channel (columnar)
    actors.json                    ← recorded actor rows + paths + per-actor state tracks
    events.jsonl                   ← one event per line (streaming; see size note)
    rng_tape.jsonl                 ← ordered draw log for exact twin reproduction (see OQ-3)
    acceptance.json                ← the tolerance rows, incl. report-only rows (§3)
```

**Why a pack and not one file.**

1. **The product seam is Layer 1 only.** The charter's founding-precedent note says this baton prototypes *the engine→Godot contract the actual product ships*. The shipping product ships **models**, not recordings of a Grim Dawn session. Splitting now builds the seam in its true shape; keeping one file builds a seam the product must later break.
2. **Different lifecycles.** Layer 1 re-cuts when a decode lap or sim build lands. Layer 2 re-cuts when a checkpoint is re-run. Coupling them forces spurious re-cuts and makes `git diff` on the model unreadable.
3. **Size.** v1 at 1.0 MB carries 1,900 events. A completed model fires specials (45 gated slots), control states (286 rows), summons, procs, casts, and per-actor state transitions — a 10–50× event multiplier is the honest expectation; the pm4-i12 batons already reach **14 MB**. `events.jsonl` streams line-by-line; a 14 MB single JSON object does not.
4. **Load posture.** The runtime loads `model/` at boot and never touches `reference/`; only the twin-test harness loads both. A single file forces every consumer to parse the recording.

**Digest law.** `manifest.json` carries `sha256` per member. The **pack digest** = `sha256` of the newline-joined `"<relpath>  <sha256>"` lines, sorted by relpath. GL-6 then holds at both member and pack level: verify pack digest → verify each member digest → load. A member whose digest fails is a load abort, not a warning.

**Non-recommended alternatives, stated so the fork is visible:** single-file (simplest consumer, breaks the product seam, fails at size) · SQLite/binary (best size/query, worst diffability and worst provenance-auditability — and this artifact's whole value is that a human can read a rule and see where it came from).

---

## 2 · LAYER 1 — MODEL

### 2.0 · The universal parameter object (DR-3)

Every numeric or enumerated rule value in Layer 1 is:

```jsonc
{
  "value": 80.0,
  "unit": "m",
  "scope": {"kind": "context_override", "context": "crucible_tier16", "waves": [150, 160]},
  "precedence": 20,                      // higher wins; ties are a validator ERROR, never a silent pick
  "provenance": "PRV-LAPU-VIEWDIST-T16", // → provenance.json registry; NEVER null
  "envelope": null,                      // {"lo": …, "hi": …} when the measurement carries a band
  "supersedes": ["PRV-WR3W2-VIEWDIST-POP"] // named, so the contradiction is visible not erased
}
```

Scope kinds: `global` (precedence 0) · `population` (10) · `context_override` (20) · `per_record` (30) · `per_wave` (40). **Overlapping scopes at equal precedence are a hard validation failure** — the pack may never resolve a contradiction by array order.

### 2.1 · `ai_states.json` — the monster controller state machine

Key space = the **43 controller states enumerated from `Game.dll` strings**. Every one of the 43 is a row. The sim currently expresses ~9 (the 7-state engagement enum `PRESPAWN · PATROL_TO_NODE · PURSUE · HALT_AT_ENGAGE · PARK_AT_NODE · BLOCKED · DEAD` at `simulation/kc2/engagement.py:116`, plus the 11-code mech enum with 12/17/18 declared unreachable). The baton currently carries **3** (`PRESPAWN/LIVE/DEAD`, `engagement.py:177`).

```jsonc
"states": [{
  "state_id": "AlertBeforePursue",
  "state_group": "engagement",
  "status": "DECODED_PARTIAL",          // DECODED | DECODED_PARTIAL | DECLARED_ABSENT | UNREACHABLE
  "unreachable_reason": null,           // required non-null iff status == UNREACHABLE (codes 12/17/18)
  "expressed_in_sim": false,            // does the Python sim run this state? (coverage bookkeeping)
  "presentation": {"anim_id": "0x21", "provenance": "PRV-DECODE-ONBEGIN-0x109410"},
  "parameters": [ {"param_id": "duration_s", "…": "<parameter object §2.0, or absence row>"} ],
  "provenance": "PRV-DLL-STATE-ENUM"
}],
"transitions": [{
  "transition_id": "TR-IDLE-TO-ALERT",
  "from": "Idle", "to": "AlertBeforePursue",
  "condition": {                        // an EXPRESSION BLOCK (§2.4 grammar), or an absence row
    "expr": "ShouldPlayRallyOrAlert(self, player)",
    "status": "DECLARED_ABSENT",        // ← D-1's target; flips to DECODED with values on return
    "absent_ref": "ABS-D1-RALLYALERT"
  },
  "priority": 10,
  "provenance": "PRV-DECODE-STATE-PRESENT-COND-UNREAD"
}]
```

**Three status classes, and no fourth.** A transition is `DECODED` (condition + parameters from substrate), `VIDEO_MEASURED` (derived from reference footage with frame evidence), or `DECLARED_ABSENT` (an `absent_ref` into the absence registry). There is deliberately **no `ESTIMATED`** status at this layer. D-1/D-2/D-3 returns flip rows in place; **no schema change is required for a decode lap to land** (DR-2).

**Coverage view (free, from the rows):** `43 total / n DECODED / n VIDEO_MEASURED / n DECLARED_ABSENT / n UNREACHABLE` — this is the facet-(a)/(b) coverage gate, computable by the validator rather than asserted in prose. It also retires `AGENT_STATE.md:347`'s standing "17 unexpressed AI states" as a number a human maintains.

### 2.2 · `monsters.json` — stat blocks, skills, specials, DoT riders

One block per encoded body, keyed by `record_path` (the v1 actor row already resolves every statline this way — `record_path` is `AC-6.4`-grade). Block contents map the sim's `MonsterStat` (`simulation/kc2/monster_stats.py:108`) **plus everything a live runtime needs that a recording did not**:

```jsonc
{
  "record_path": "records/creatures/enemies/ghost_b01.dbr",
  "display_name": "Haunted Noble",
  "threat_tier": "trash",              // trash | hero | boss | nemesis
  "archetype_tag": "ghost_b01",
  "faction": "monster",
  "level": {"…": "parameter object, per_wave scope"},
  "life": {
    "ehp_anchors": {"w1": [lo, hi], "w93": [lo, hi]},
    "life_equation": "…", "reconstruction_rule": "RULE-EHP-AFFINE",   // → math_rules
    "grade": "MEASURED", "provenance": "PRV-LAPD-EHP"
  },
  "offense": {"damage_types": [...], "flat_total_mid": …, "mod_total_pct": …,
              "attack_speed_tag": "…", "swing_anchors": {...},
              "upper_bound_declaration": "G-2"},                       // ← v1 declaration, carried
  "defense": {"armour": …, "resists": {...}, "OA": …, "DA": …},        // ← NEW vs v1 (no monster mitigation existed)
  "ai": {"controller_profile": "…", "state_overrides": [ /* §2.0 objects, e.g. ViewDistance 80 m */ ]},
  "skills": [ {"skill_id": …, "damage_rows_ref": …, "cast_rule_ref": …} ],
  "specials": [ {
      "slot_id": "…", "skill_id": "…",
      "reuse_gate": {"…": "parameter object (delay_s / skill_cooldown_s), or an absence row"},
      "fires": true                       // ← FALSE means DECLARED-NOT-FIRING, with absent_ref
  } ],
  "dot_riders": [ {"rider_id": …, "damage_row": …, "stacking_rule_ref": "RULE-DOT-STACK"} ],
  "pets": [ {"record_path": …, "spawn_skill_id": …} ]   // monster-summoned pets, own blocks
}
```

**Precision the audit forces, and the brief's "188" needs disambiguating against (→ OQ-5).** The 45/58 silent special slots are **pet** special slots — `threat.py:607` `pet_special_slots_ungated`, whose comment records that `tg2_attack_slots.csv` covers the roster only (0 of 56 pet records appear in it; only 13 of 58 pet special *skills* declare `skill_cooldown_s`). So D-2's slot table lands on a **pet-record stat-block population that is distinct from the 188 roster eHP closure**, and the schema must carry pet blocks as first-class rows (it does, above: `pets[]` → their own `monsters.json` entries with `faction: "monster_pet"`). A schema that only carried "the 188" would have nowhere to put D-2's return.

**The GL-12 discipline made structural.** `fires: false` with an `absent_ref` is how a slot ships honest. Borrowing the roster's `delay_s` distribution for pets is exactly what `threat.py` refused to do and what the schema must remain incapable of expressing: there is no field in which a borrowed distribution could hide, because every gate value carries its own provenance id.

### 2.3 · `player_kit.json` + `summons.json`

Lap G decoded the full kit; the sim's 13-row `OUT_OF_MODEL` manifest (`fixture.py:234-248`) is the delta the Wave-2 builds close. Sections:

- **(a) Bar skills — 9.** Per skill: id, host binding, resource cost, cast/channel model, geometry (`hit_test_model`, `radius_m`, sweep semantics), damage row refs, cooldown. The EoR channel keeps its measured limbs (`drain_rate_per_s` 176.4 `PER_TICK`, `channel_tail_s` 0.25, `rotation_speed_multiplier` 0.35, `radius_m` 3.0) as parameter objects with the L-22 pins as their provenance.
- **(b) Devotion procs — 8, with host bindings.** Per proc: `host_skill_id`, trigger condition (expression block), proc chance, ICD, effect rows. **Turtle Shell / Fighting Spirit / Ascension are named rows** — v1 carried only the prose disclosure `devotion_envelope_disclosure` under `R-KC2-1(d)`; v2 replaces prose with rows.
- **(c) Sustain circuit-breakers.** **Menhir's Will** first-class (the audit's finding: it is *the build's actual circuit-breaker, not Ghoulish Hunger*) with its trigger/threshold/heal/cooldown as parameter objects; leech ladder; Resilience; retaliation; potions with their measured counterplay limbs; War Cry.
- **(d) Summons — 2, as first-class actor templates.** `Guardian of Empyrion` + `Deathstalker` use **the same actor-template schema as monsters** (§2.2) with `faction: "player_summon"` — stats, AI profile, skills, reuse gates, lifetime/resummon rules. This is the structural expression of facet (f)'s "first-class actors" ruling: not a special case, the same case. (Layer-2 note: `R-L53-2` — summons carry no *path* in the recording — is a **Layer-2 absence**, `informative_rows[OBJ-1-UNION-RELAW]`, and must not be mistaken for a Layer-1 one. v1's consumer had to read two registries to find it; v2's absence registry is single and unified — see §5.)

### 2.4 · `math_rules.json` — evaluable rule blocks, and the test-vector guardrail

v1 carries the damage semantic as a **prose string** (`config.model.damage_semantic`, `mitigation_model`, `crit_model: "NOT_MODELLED"`). Prose is where invention enters: two engineers read the same sentence and write two formulas. v2 carries rule blocks:

```jsonc
{
  "rule_id": "RULE-DMG-APPLIED",
  "output": "damage_applied",
  "inputs": ["damage_raw", "target.hp", "target.armour", "target.resist[type]"],
  "expr": "min(damage_raw * (1 - mitigation(target, type)), target.hp)",
  "expr_grammar_version": 1,
  "provenance": "PRV-…",
  "envelope": {"lo": -0.005, "hi": 0.039},        // the fixture identity envelope where it applies
  "test_vectors": [ {"in": {...}, "out": 1234.56, "source": "sim@<engine_sha>"} ]
}
```

**The load-bearing move: `test_vectors` are normative; `expr` is documentary.** The Godot runtime is **not** required to implement an expression evaluator. It is required to implement the rule in GDScript and **reproduce every test vector to the declared precision**. This gives the twin-test a *unit-level* tier below the fight-level tier (§3) — a mitigation formula misread is caught by a 40-vector table in milliseconds instead of by a 300-second fight divergence with fifteen candidate causes. Vectors are generated by the emitter from the sim, so they cost the spec nothing and cannot drift from the sim's actual behaviour.

Rule families required: damage composition + type resolution · mitigation (armour/resist, both directions — **monster-side mitigation does not exist in v1 at all**: `mitigation_model: "NONE-MODELLED on the monster side"`) · crit (v1: `NOT_MODELLED`; PM4 introduced crit limbs — carry the model with its limb selection as a parameter) · leech ladder · DoT application **and stacking** (`RULE-DOT-STACK`, the D-4 target, provenance class `video-measured`, evidence-bearing per §5) · energy drain/regen · movement + the 3 dash layers · eHP affine reconstruction (`RULE-EHP-AFFINE`, incl. the exact `G_BAND_A` array — the module's own note records that linearising `G` costs **17.49 pp max error ≈ 2.5% on eHP**, so the array ships verbatim, never a fitted shape).

### 2.5 · `waves.json` — per-wave spawn structure

Per wave: `content_tier`, `reward_tier`, `life_modifier_pct` (the `G(wave)` term), `nemesis_wave`, `spawn_points_active` (**by `point_id`, never by array slot** — v1's `[M-6]`, retained), and the roster. **The playability fork lives here (→ OQ-6):** a runtime whose player fights differently still needs waves to arrive. If the *roll rules and pools* are decoded, Layer 1 carries them and the runtime rolls (v1's declaration `G-5` asserts wave 160 is *"rolled honestly from the pools, NOT a scripted Zantarin reenactment"* — which presupposes pools exist as decoded objects). If they are not decoded, Layer 1 carries the **recorded** per-wave rosters, and the pack must say plainly that wave composition is fixed-from-the-recording — a playability limitation named, not hidden. Schema supports both: `roll_model: "DECODED_POOLS" | "FIXED_FROM_REFERENCE"` with the pools or the rosters attached accordingly.

### 2.6 · `arena.json` — geometry, spawn points, containment

Carries: axis convention (v1's `AxisConvention` block, unchanged and good), `width_m`/`height_m`, `spawn_points[]` with `heading_rad` + bearing grade, `player_spawn`, `placement_extents_m`, scatter model, `d_engage_m`, and the path/interpolation laws (`GL-7` linear interpolation between knots **is** the position function).

**Containment — a Law-3 catch the schema must not paper over (→ OQ-2).** The charter and RULING-NOTE facet (h) speak of *"the decoded 86.915 × 85.303 m rectangle (GL-13)"*. The A1b-1 landing record says something materially different: that rectangle is **the MEASURED OCCUPIED REGION** (5,085 recorded positions + one 3.0 m sweep radius), and the same cell records **"NO WALL — tested: 1,429 nodes, zero wall-class names"**, with the wire declaring `arena_bounds.shape: "UNBOUNDED"` / `collision_model: "OPEN-PLANE"`. An occupancy hull is a fact about *where bodies went*; it is not an extent claim. Placing a wall on it is a fitted constant. The schema therefore separates three things that the single word "bounds" fuses:

```jsonc
"containment": {
  "substrate_model": "UNBOUNDED-OPEN-PLANE",          // what substrate says: parameter object
  "measured_occupancy_hull": {"width_m": 86.915, "height_m": 85.303,
      "basis": "5085 recorded positions + 3.0 m sweep radius",
      "claim_class": "FACT-ABOUT-THE-RECORDING",      // explicitly NOT an extent claim
      "provenance": "PRV-GL13-OCCUPANCY"},
  "runtime_containment": {                             // CONSUMER POLICY, not model truth
      "policy": "SKIRT",                               // per R-CPA-3, Matt-ruled for SB-1
      "claim_class": "PRESENTATION-CHOICE-NOT-MODEL-TRUTH"}
}
```

C-1's return feeds `measured_occupancy_hull` and the run's facet-(h) decision; it cannot, by itself, license a wall in Layer 1.

### 2.7 · `rng_contract.json` — tick + RNG

- **Tick.** `tick_period_s: 0.0816326530612245` (= 1/12.25), `run_tick` as the one global integer clock (v1 `NOTE-4`: `fight_tick` is NULL on 1,900/1,900 rows — the wave-local clock is **absent by measurement**; v2 either emits it properly or keeps it out; a column that is always null is a lie about capability). `binding_class` declares whether the runtime **must** step at this rate (`MODEL-BINDING`) or may pick its own with the tick treated as a sim artifact (→ OQ-7). Recommended presentation posture either way: fixed-tick simulation with render interpolation between ticks — the same discipline `GL-7` already imposes on positions.
- **RNG.** v1 pins `python-random-Mersenne-Twister` + seed. A GDScript runtime cannot reproduce that stream, so **an exact twin-test is impossible on the seed alone** (→ OQ-3). The schema splits the contract in two:
  - **Draw-site registry (Layer 1):** an ordered, named list of every stochastic decision the model makes — `{draw_site_id, distribution, parameters, consumption_order, consumed_by_rule}`. A free-play runtime uses *its own* RNG at *these* sites in *this* order. This is what makes divergent play well-defined rather than improvised.
  - **RNG tape (Layer 2):** the recorded draw log, `{run_tick, draw_site_id, value}`, so the twin-test is exactly reproducible without the consumer implementing MT19937.

---

## 3 · LAYER 2 — REFERENCE (the acceptance test)

**Source pin:** the sibling checkpoint **`E-s09-cp150-mech`**, sha `20b05cb4ef3bd888b998cbc46c68b41a8051111c12fbcf2066d101b0a4b15f4b` (D5: parent `E-s09-cp150` immutable; siblings only). `reference/meta.json` carries checkpoint sha, seed pins, engine sha + tree state, sim module version, spec pin — v1's `sim_pin`/`spec_pin`/`provenance.seed_pins` blocks are good and carry over intact.

**Contents:** recorded player path (the drive input for the twin-test) · per-tick player HP / energy / channel tracks · **per-actor state tracks** (facet (a): the state id per tick from the §2.1 key space, replacing v1's 3-code `PRESPAWN/LIVE/DEAD`) · actor rows with paths and knots · the full event stream (`events.jsonl`, vocabulary extended per facet (g): casts, dashes, War Cry, potions, proc fires, control applications, special fires, summon actions) · the RNG tape.

**`acceptance.json` — the tolerance rows.** Four tiers, each row independently graded:

| Tier | What it asserts | Instrument |
|---|---|---|
| **T-0 unit** | every `math_rules.test_vectors` row reproduces | vector table, exact-to-precision |
| **T-1 trajectory** | driven along the recorded player path, the runtime's player HP / energy / channel tracks stay inside band | per-tick band + max-excursion |
| **T-2 fight state** | board occupancy (alive bodies per tick), cumulative damage dealt/taken, wave clear ticks | per-wave band |
| **T-3 outcome** | waves cleared, run duration, end reason, **terminal wave** | see report-only below |

```jsonc
{
  "row_id": "ACC-T3-TERMINAL-WAVE",
  "tier": "T-3",
  "metric": "terminal_wave",
  "reference_value": 160,
  "tolerance": null,
  "report_only": true,             // ← STRUCTURAL: rows with report_only:true carry NO tolerance
  "assertion": "NONE",             //   and the harness is INCAPABLE of failing on them
  "grade_note": "Matt-ruled 2026-08-24: wave-160 is a GRADED ROW, never a gate."
}
```

**The `report_only` flag is a structural guarantee, not a procedural promise.** A `report_only: true` row may not carry a `tolerance`, and the validator rejects the pack if it does; the harness has no code path that turns a report-only row into a FAIL. This is how the wave-160 ruling survives a future session that does not remember it — the same failure mode the charter-freshness discipline exists to catch. Terminal wave is *reported* prominently and *asserted* never.

**Also report-only by construction** (recommended, → OQ-8): any metric whose reference value depends on a Layer-1 rule currently marked `DECLARED_ABSENT`. Grading a runtime against behaviour the model refused to specify grades the consumer's guess, not the consumer's fidelity.

**The twin-test protocol in one sentence** (Wave-4 spec to drax expands it): *load `model/` only into the runtime; drive the player actor along `reference/tracks.json`'s recorded path (positions are authoritative, GL-7 interpolation); consume `reference/rng_tape.jsonl` at the declared draw sites; run to the recorded end; emit the same track + event shapes; diff against `acceptance.json` row by row.*

---

## 4 · VERSIONING + THE CONSUMER CONTRACT

**v2 is a breaking cut. Say so on the wire.** `_schema_version: 2` + `pack_format: "kc2-model-pack/v2"`. The existing loader checks `_schema_version` at `kc2_baton.gd:223` and errors on mismatch, so **v1 consumers fail closed on a v2 pack** — correct behaviour, no silent misread, nothing to fix. v1 batons remain readable by v1 consumers forever; there is no in-place migration and none should be attempted.

**`export/MIGRATION.md` entry rides the Wave-4 cut** (discharges jack-ryan WARN-A). It must state: v1 = trace/replay artifact, v2 = model-pack, **not a superset** — v2 intentionally drops fields whose only content was a prose disclosure, and adds the obligation to derive.

**The consumer contract inverts.** v1's law is *zero derivation* ("computes no damage, resolves no hit, decides no death"). A Layer-1 runtime derives all three. What survives from v1's posture, and must be written into the v2 consumer contract explicitly, is the **honesty half** of that law:

- **GL-6 stands and strengthens** — verify pack digest, then member digests, before load.
- **GL-12 stands** — absence is declared, not filled. What changes is *who* fills: the runtime may fill, but only by registering a **runtime choice** against an `absent_ref`, surfaced in a ledger the harness prints. Silent filling is the failure.
- **GL-10 stands** — use the wire's constant; never re-derive one it carries.
- **FG-13 generalises from an event census to a RULE census.** v1 derives its need-list from the artifact's own `event_type` column and goes RED on an uncovered need. v2's consumer declares a disposition for every **rule id, state id, and skill id** in Layer 1 — `IMPLEMENTED` / `BINNED` (+ why) / `UNCOVERED` — and any `UNCOVERED` reachable in play goes RED. This is what turns "we implemented your model" into a countable claim, and it is the coverage instrument the Godot session hands back.

**Two declared consumer roles**, so a partial consumer cannot masquerade as a whole one:

| Role | Reads | Obligation |
|---|---|---|
| `MODEL-RUNTIME` | `model/` only | full rule census; runtime-choice ledger for every `absent_ref` it touches |
| `TWIN-TEST-HARNESS` | `model/` + `reference/` | the above, plus every `acceptance.json` row graded and reported |

**Emitter/validator posture (Wave-4 implementation note).** The v1 pydantic surface (`export/baton_v1_schema.py`, `_Strict` with `extra="forbid"`) is the right foundation and should be reused, not rewritten: `extra="forbid"` is precisely the DR-1 posture at the field level. What is new is a **semantic validator pass** the v1 validator has no analogue for: (1) no leaf with `provenance: null`; (2) every `provenance` id resolves in the registry; (3) every `absent_ref` resolves in the absence registry; (4) no two same-precedence overlapping scopes; (5) no `report_only` row carrying a tolerance; (6) every `test_vectors` table non-empty for rules marked normative; (7) grade enum closed (§5).

---

## 5 · CROSS-CUTTING — provenance, absence, and the evidence classes

**`provenance.json` carries two registries.**

*(1) The provenance registry.* Each entry: `{provenance_id, grade, source, locator, lap, date, note}`. **Closed grade enum, and the closure is the Law-3 mechanism:**

| grade | means | example |
|---|---|---|
| `decoded-substrate` | read out of game files / binary | eHP anchors, the `G_BAND_A` array, state enum from `Game.dll` |
| `video-measured` | measured from reference footage with frame evidence | the D-4 DoT stacking function |
| `sim-emitted-measured` | produced by the pinned sim run under a pinned seed | Layer-2 tracks; `test_vectors` |
| `declared-absent` | not carried; points to an absence row | — |

There is **no `estimated`**. This collides with real v1 content and the collision is a genuine fork, not an oversight — see **OQ-1** (`bearings_provenance: "ESTIMATED-FOOTAGE ±15°"`, `scatter_model: "SIM-ROLLED BOX"`, and the `T8-P04` ±5% declared band all exist on the current wire and have nowhere to live under a three-grade enum).

*(2) The absence registry — one registry, unified.* v1 split declared absences across `provenance.out_of_model[]`, `provenance.declarations[]`, and `provenance.informative_rows[]`, which is exactly why the Godot loader's `NOTE-3` had to warn that *"a consumer enumerating `out_of_model` to build its declared-absence panel will not find summons there. This loader reads BOTH."* A consumer should never need a footnote to find an absence. One registry:

```jsonc
{
  "absent_id": "ABS-D1-RALLYALERT",
  "what": "AlertBeforePursue entry condition (ShouldPlayRallyOrAlert) + duration",
  "why": "UNREACHED-U3 / U-U-2 — present in binary, condition body unread",
  "searched": ["Game.dll string table", "OnBegin @0x109410", "…"],   // what was looked at, per the honorable-fallback law
  "class": "UNDECODABLE-FROM-SUBSTRATE",  // or NOT-YET-DECODED | UNDECODABLE | OUT-OF-CHARTER
  "observable_in_reference": true,        // is video-measurement a live route?
  "blocks_playability": true,             // ← THE FIELD THAT ANSWERS MATT'S QUESTION
  "affected_rules": ["TR-IDLE-TO-ALERT"],
  "runtime_choice_required": true
}
```

`blocks_playability` makes the intent sentence — *"a Godot team could build the playable fight from this artifact without guessing a rule"* — into a **count**: the pack is playability-complete iff `count(absent WHERE blocks_playability AND runtime_choice_required) == 0`, and where it is not zero, the exact list is on the wire and in the seal summary.

**Evidence-class labelling (charter §6 obs-3(3)).** `video-measured` rules carry `evidence: {media_sha256, media_path, frames[], method_note, measurement_envelope}` and a `weaker_evidence_class: true` marker. The DoT stacking function's grade is not the same grade as an eHP anchor's and the pack must not let them read alike.

**Decode-lap lineage.** Every provenance entry names its lap (`D-1`, `D-2`, `D-3`, `D-4`, `Lap D`, `Lap G`, `Lap U`, `WR3-W2`…). `model/meta.json` carries a `lap_manifest[]` — lap id, date, seat, output note path — so a rule's history is one hop from the rule, and a contradiction (ViewDistance) reads as two laps disagreeing rather than as one number being wrong.

---

## 6 · OPEN QUESTIONS BACK TO THE CONDUCTOR

*Decision-shaped; conductor- or Matt-level. Not resolved here.*

**OQ-1 — the provenance enum vs. content that is already estimate-grade.** The brief's three grades (decoded-substrate / video-measured / declared-absent) have nowhere to put existing wire content: `bearings_provenance: "ESTIMATED-FOOTAGE ±15°"`, `scatter_model: "SIM-ROLLED BOX"`, the `T8-P04` ±5% declared band.
(A) Add a fourth grade `declared-estimate` requiring a mandatory envelope + a named ruling id — narrow, auditable, but reopens the word "estimated".
(B) Demote all estimate-grade content to `declared-absent` + runtime choice — cleanest Law 3, costs the runtime real information that was honestly measured with a band.
(C) Keep it, but move it out of Layer 1 MODEL into a `presentation_defaults` section explicitly marked NOT-MODEL-TRUTH, alongside `runtime_containment`.
**Lean: (C)** — the model layer stays Law-3-pure; the runtime still gets spawn bearings; the label carries the honesty.

**OQ-2 — arena containment, and a charter wording correction.** The charter/RULING-NOTE call 86.915 × 85.303 m *"the decoded rectangle"*; the A1b-1 record calls it the **measured occupied region**, with **no wall found** in substrate (1,429 nodes, zero wall-class names) and the wire declaring `UNBOUNDED`/`OPEN-PLANE`.
(A) Layer 1 carries `UNBOUNDED-OPEN-PLANE` + occupancy hull as FACT-ABOUT-THE-RECORDING + SKIRT as presentation policy (R-CPA-3); no wall either side, whatever C-1 returns.
(B) If C-1 returns CROSSES/APPROACHES, put walls in-sim as a **declared divergence from substrate** — which is a Law-3 exception and therefore a Matt commitment boundary, not a seam call.
(C) Commission a substrate decode of real Crucible arena collision before any wall enters either side.
**Lean: (A) now, (C) queued.** Flagging that facet (h) as *written* ("walls IN-SIM non-negotiable") may presuppose a wall the substrate has not yielded — worth the conductor's eye before Wave 2 fires B-7.

**OQ-3 — RNG portability, and the size of the tape.** Python MT19937 is not reproducible in GDScript from a seed.
(A) Layer 2 carries an RNG **tape** (ordered draw log) + Layer 1 carries the draw-site registry — exact twin-test, consumer burden near zero, tape size unknown until the completed model's draw count is known (could be 10⁵–10⁶ rows).
(B) Runtime reimplements MT19937 + the draw-site consumption order — exact, no tape, meaningful consumer burden and a whole new class of subtle bug.
(C) No exact twin; statistical tolerance bands only.
**Lean: (A)**, with a fallback to per-wave tape segments if size bites. Conductor's call whether tape size is a Wave-4 measurement or a pre-decision.

**OQ-4 — one pack or two artifacts.** (A) one pack, two subdirs, handed together. (B) two independently versioned artifacts (`model-pack` / `reference-pack`), with the model-pack the product-shaped one and the reference-pack a dev-time acceptance artifact.
**Lean: (B)** on the founding-precedent argument (the shipping product ships models, not recordings). Cost: two manifests, two digest chains, a cross-pin between them.

**OQ-5 — stat-block population: which "188"?** The brief says 188 stat blocks. The audit gives: 188/188 eHP closure (Lap D) · 163 distinct names in the 344-actor recorded roster · 56 pet records (where D-2's 45/58 ungated slots actually live) · the full tier-16 Crucible pool the waves roll from.
(A) Reference-roster closure only — matches the recording, smallest pack.
(B) Full tier-16 pool — a live runtime whose player performs differently still rolls from the pool, so anything the pool can produce must have a block.
(C) (A) now, (B) as a later lap.
**Lean: (B) is what "playable" actually requires** and (A) risks a runtime that hits an unknown `record_path` mid-wave — but the pool's size and decode state are not known to me. **Possibly intent-critical; recommend an explicit conductor ruling rather than a default.**

**OQ-6 — wave composition: rolled or fixed?** (A) Layer 1 carries pools + roll rules; runtime rolls (v1's `G-5` declaration presupposes decoded pools exist). (B) Layer 1 carries the recorded per-wave rosters; composition is fixed-from-reference, named as a playability limitation. (C) (B) now, (A) when the roll rules are decoded. Couples tightly to OQ-5. **Lean: (A) if decoded, else (C) with the limitation stated on the wire.**

**OQ-7 — is `tick_period_s` model truth or a sim artifact?** 0.0816326530612245 s = 1/12.25. (A) `MODEL-BINDING`: the runtime steps at this rate — twin-test tractable, but a sim convenience becomes game truth for the product seam. (B) `SIM-ARTIFACT`: carry the underlying real rates per rule and let the runtime pick its tick — honest, makes exact twin-testing much harder. **Lean: (A) with the limitation recorded**, since the product-seam question is properly Matt's.

**OQ-8 — do PM5's report card and the twin-test's acceptance rows share a row schema?** (A) shared — one grading vocabulary, wave-160's `report_only` flag written once and honoured by both instruments. (B) separate — they grade different questions (model faithfulness vs implementation fidelity) and conflating them invites a category error. **Lean: (A) for the row schema, (B) for the row sets.** Touches the Wave-3 D4 prereg, so it needs settling before Wave 3, not at Wave 4.

**OQ-9 — does the pack carry `runtime_guidance` for declared-absent rules?** (A) No — carry only the absence + `blocks_playability`; the Godot team decides and logs its own choice. Cleanest Law 3; hardest handoff. (B) Yes, namespaced `NOT-MODEL-TRUTH`; kinder handoff, but guidance is a guess wearing a label and labels erode across sessions. **Lean: (A)** — with the runtime-choice ledger (§4) as the compensating instrument, so choices are visible even though the pack made none.

**OQ-10 — validator + emitter ownership and gating.** The semantic validator (§4, seven checks) is what makes DR-1 real; without it the provenance fields are decoration. Is it (A) star-lord's Wave-4 scope alongside the emitter, (B) a jack-ryan Gate-2 instrument, or (C) both — emitter-side enforcement plus an independent Gate-2 re-run? **Lean: (C).** Also: does a validator failure block the cut (recommended: yes, hard) or emit a warning?

---

*Filed 2026-08-24 by gandalf (`SPEC-AUTHOR`), Wave-1 piece S-1, KC2 MODEL-COMPLETION RUN. No production code; specialists implement at Wave 4. Committed, not pushed.*
