# Mechanical Reality — the engine's full mechanical surface register (build-out reference)

> **STATUS:** MATT-FACING · LIVING — born 2026-07-11 per Matt directive: *"We need both a full
> substrate coordinate page for kit design search and we also need a full mechanical reality page
> for the build out when exploring each new kit."*
>
> **PURGE-EXEMPT:** Matt-consumption surface — never folded, retired, or purged without Matt's
> explicit ruling (form-precedent: the pipeline docs, 2026-07-10).
>
> **Maintenance law — SAME-COMMIT:** the commit that lands mechanics-changing work updates the
> touched surface row here in the SAME commit (rocket: generation/emitters/binder · gamora:
> sim/resolver/hooks · star-lord: attribution/telemetry · gandalf: doc owner + design-state stamps).
>
> **PAIR LAW:** this page = **WHAT the engine can express** (mechanical truth, per surface, with
> state). Its twin `substrate-coordinates.md` = **WHERE a kit sits in design space** (search).
> Exploring a new kit reads BOTH: sample the coordinate there → verify every mechanical surface the
> kit touches here. **Glance:** candidate page (contract amendment — KR sequences; drax builds).

**Siblings:** `pipeline-serial-content-emission.md` (E0–E8) · `pipeline-battle-sim.md` (S0–S8) ·
`substrate-coordinates.md` (the pair twin). **Register of record for gaps:**
`agentic_orchestration/gandalf/notes/2026-07-11-hybridity-mechanical-scaffolding-audit.md`.

---

## FLOW

> Glance `/mechanics` lead bar (contract §7.7, v1.9). **Navigation semantics, NOT
> state-progression** — mechanical-composition order (what a kit IS → how it resolves → what's owed
> → build order); stages carry no modeled queue rows and render quiet by design. Owner (gandalf)
> updates refs same-commit on any §-restructure.

1. **Kit anatomy (packet)** ← §1
2. **Geometry + motion** ← §2
3. **Elements + mitigation** ← §3
4. **THE BINDING RESOLVER** ← §4
5. **Surfaces register (truth vs owed)** ← §5
6. **Scaling + economy** ← §6
7. **Layer-2 + hooks** ← §7
8. **Proxies + summons** ← §8
9. **BUILD LADDER** ← §9

---

## §1 — Kit anatomy (the packet)

| Surface | State | Anchor |
|---|---|---|
| 5 skill slots under the **slot law** (attack slots carry the kit's commitment-bin identity · control takes real cast time but doesn't define the coordinate · support fires instant · T4 declares per-capstone) | LIVE (Q-E4-1b RULED) | composer; E4 design note §1 |
| Skill = ability composite: `composition_mode ∈ {single, layered, fused, triadic}`; **each Ability carries its own `canonical_element`** | LIVE generation-side; composition FLATTENS at emission (sim reads one element/skill) | `skill_schema.py:9` · `ability_schema.py:17` |
| T4 capstones with **transform declarations** `(commitment_bin, amplitude_delta)` — expressed-coordinate cert law | RULED (E4); build with pair | E4 design note §1 |
| **Scaling-unification T4** — "all elements scale off your primary stat"; overrides scaling STAT only; the slot = the price of co_equal | RULED (E3, 2026-07-10); build in E3 dispatch | tracker eighth entry |
| **`element_application` block** — declares WHAT, never HOW: `{primary, secondary, structures, rate_band}` | RULED (E3); build in E3 dispatch | element addendum §1–§10 |
| **`naming_flavor_element`** — naming-only field for the LLM proportional-rename judgment; Do-Not-Regress (flavor-nuke lineage) | RULED rename; split owed in E3 dispatch | tracker seventh/eighth entries |

## §2 — Geometry + motion

| Surface | State | Anchor |
|---|---|---|
| 24-type `geometry_type` + 6-type `spatial_geometry_type` + `geometry_params` | LIVE | `ability_schema.py:20-29` |
| Geometry ladder (damage-scaling by geometry class) | LIVE | `damage_resolver.py:287` |
| Motion-frame seven-axis family (F1–F6 ratified: named-bundle primitives, ONE ai_strategies kernel, nova/spin migration audit-gated) | RULED; staged consumers | `../reap-die-rise-engine/motion-frame-substrate-amendment-2026-07-09.md` |
| **Emission slot** (kernel primitive `{entity, origin, trigger, depth≤2}` — "circular skills spawn roaming damage entities" lives HERE, element-blind, reusable by mono kits) | SPECCED-NOT-BUILT | rotational addendum §3 |

## §3 — Elements + mitigation

| Surface | State | Anchor |
|---|---|---|
| 8 elements, **physical first-class** (`STAT_ELEMENT_POOLS`: STR → `["physical"]`) | LIVE | `season_generation_pipeline.py:210-248` |
| **Per-chain elements** (Amendment 7a): `chain_elements = {A: primary, B: secondary, C: primary}`; per-skill `canonical_element = chain_elem` | LIVE since 2026-05-29 | `per_skill_emitter.py:864/:1136/:1279` |
| Per-chain ailments: `ELEMENT_AILMENT[chain_elem]` on chain-A primary attacks (hardwired, pre-hook-layer) | LIVE | `per_skill_emitter.py:772` |
| Mitigation branch: physical → dodge gate + block + armor; magical → flat resist + 7×7 substrate matrix (physical deliberately non-substrate) | LIVE | `damage_resolver.py:439+` · `resistance_matrix.py:137-139` |
| Layer-2 hybrid roll `_roll_hybrid`, secondary from `_ALL_8_ELEMENTS − {primary}`, `HYBRID_RATE = 0.175` | LIVE; promotion to governed dial owed (E3 dispatch) | `season_generation_pipeline.py:654-664` |

## §4 — THE BINDING RESOLVER (element-application machinery, in full)

The rules that decide how a hybrid element is presented across a kit. **Four addresses:**

1. **Capability slots** (kernels / chain / hooks / emission) — **element-BLIND mechanics.** "Circular
   skills spawn roaming damage entities" is the kernel emission slot's line (rotational addendum §3),
   reusable by mono kits — D2 Whirlwind slot-empty vs D4 dust-devil slot-populated. Mechanics text
   never lives in the element home (a second spawn mechanism = §10 duplicate-representation violation).
2. **`element_application` block** (kit packet) — declares WHAT, never HOW:
   `{primary, secondary, structures, rate_band}`.
3. **THE BINDING RESOLVER** — the rulebook: **~7 one-line walkers + a data map**, one per structure:

   | Structure | Walker (the one line) | State |
   |---|---|---|
   | `chain_partition` | chain_B := secondary | **LIVE** (`per_skill_emitter.py:1136`) |
   | `geometry_partition` | geometry-class map, e.g. {flies → frost, pools → fire} | rule owed (E3 dispatch; runtime-free) |
   | `emission_carrier` | emitted entities := secondary (+ gen-2 inherit) | with emission primitive (ladder #5) |
   | `rider_on_hit` | hook entry on_hit(scope) → secondary rider/ailment — *"on physical hits, apply burn"* verbatim | with hook layer (ladder #2) |
   | `proc_trigger` | trigger entry on_event + chance → secondary effect | with hook layer (ladder #2) |
   | `flat_split` | output := component vector [(primary, 1−f), (secondary, f)] | with component accounting (ladder #3) |
   | `phase_partition` | phase-2 skills := secondary | with phase axis (ladder #4) |

   Each walker ships WITH its capability layer (§7 build ladder) — never ahead of it.
4. **Affinity masks** (per cell) — constraint at SAMPLING, before binding (e.g. carrier ⇒ emission
   slot present). Home: `substrate-coordinates.md` §3.

**Home:** NEW `generation/element_application_binder.py` (rocket seam), sited at the emitter stage
where Amendment 7a chain-element resolution already runs. **Generation-time law: resolution is
GENERATION-TIME, never runtime** — the binder stamps concrete fields (per-skill element, per-slot
entity element, hook/trigger entries, component vectors); the sim reads only resolved fields; the
gauntlet certifies the RESOLVED kit (realized-share measured on real output; deterministic per seed).
**Presentation (§8 legibility) rides the same resolved fields** — no separate rules engine: per-skill
element drives palette; emitted entities wear the secondary palette; `naming_flavor_element` +
Emberfrost pattern handle names.

## §5 — Binding surfaces register (mechanical truth vs owed)

| # | Surface | Engine state | Owed |
|---|---|---|---|
| 1 | Chain slots | ✓ LIVE (Amendment 7a) | per-chain `damage_scaling_type` + `scaling_attribute` derivation via `scales_with` (E3 dispatch — replaces kit-level stamping `per_skill_emitter.py:1115/:1589`) |
| 2 | Kernel geometry classes | ✓ vocabulary rich; elements per-chain only | pipeline assignment rule + mask `hard_constraint` (kit spans ≥2 geometry classes) |
| 3 | Damage-output split | ~ HALF-BUILT (per-ability elements exist; flattens at emission) | sim-side component-vector resolution; crit/block per-component math (gamora note) |
| 4 | On-hit hooks | ~ DECLARED-NOT-RESOLVED (resolver emits **8 event types** — on_chaos_immune/on_dodge/on_block/on_hit/on_kill/on_lifesteal/on_crit/on_vortex_pull, returned `:584`; the ONLY live caller drops them by math-note ruling `spatial_resolver_adapter.py:304`/`:19`; Phase-0 stub ancestor `trigger_handler.py` — `handle_trigger()`=pass, `MAX_TRIGGER_DEPTH=3`, zero imports) | **THE HOOK LAYER** — hook points inline at emission sites (NOT event replay — preserves RNG draw order); first hook = ailment application (`:562`) refactored on, per-seed non-regression proof. **Design note LANDED 2026-07-11:** `agentic_orchestration/gandalf/notes/2026-07-11-hook-layer-design-note.md` |
| 5 | Trigger table | ~ DECLARED-NOT-RESOLVED (`layer2_trigger` enum `skill_schema.py:139-141`; only charge-stack consumed `damage_resolver.py:327-334`; emitted∩declared = {on_hit, on_kill} only) | SAME hook layer — one architecture serves 4+5; vocabulary reconciled by emission-point class (design note §2.3: hit-resolution+cast v1 · tick/threshold v1.1 · `sequence` OUT→phase axis · charge-stack stays live as-is) |
| 6 | Combo phases | ✗ ABSENT cross-skill (`sequence` + `prerequisite_skill` declared-not-consumed) | mark/consume state design from scratch + placement hearing (gandalf) |
| 7 | Emission slots | ~ SPECCED-NOT-BUILT | build per rotational addendum §3; pairs with B12 re-cert; emitted-vs-proxy boundary ruling at integration |
| S | **Attribution spine** | damage events exist; NO per-element attribution columns | **v1-BLOCKING** — kill-attribution-by-element + realized-share columns (star-lord); covers DoT ticks, later components/emissions/proxy attacks |

## §6 — Scaling + economy

| Surface | State | Anchor |
|---|---|---|
| `damage_scaling_type` + `scaling_attribute` — today stamped KIT-LEVEL on all skills (`_BC_ATTRIBUTE_TO_SCALING_ATTR`) | LIVE; per-chain derivation owed (E3 dispatch, ONE site flips both fields) | `per_skill_emitter.py:1115/:1303/:1589` · `damage_resolver.py:318-320/:354-382` |
| Cost: mana live; **Axis-5 cost-TYPE bins reserved-empty** (the bench B1–B3 blockers) | RESERVED | tracker PART F.3 |
| Cooldowns + `cast_time_seconds` tier map | LIVE emitter-side; sim consumer = E4 pair build | `per_skill_emitter.py` · E4 design note §0 |
| E4 commitment machinery: cast-state machine · tick resolution · drain + pay-on-commit · move-while-channel enum (rooted/walk/full_move) · cumulative break threshold (F-1b) · ramp + break-reset (F-2b) · interrupt RULE v1 sim-side | RULED; pair landed emitter-side (`e4d682e`), gamora PHASE-2 queued | E4 design note + runtime addendum |
| 3 pricing guards as LAW (k-aware) + throughput-active bands | RULED | E4 design note §1 |

## §7 — Layer-2 + the hook layer (build ladder #2)

| Surface | State |
|---|---|
| `layer2_trigger` enum: `{on_use, on_hit, on_kill, on_take_damage, periodic, threshold_stack, threshold_hp, sequence}` + stackability vocab | DECLARED (`skill_schema.py:120-165`) |
| Charge stacks: `per_stack_passive_bonus` → resolver + combatant | LIVE (the one consumed path; E4/Q9 lineage) |
| `prerequisite_skill` (Layer 1.5 coupling) | DECLARED-NOT-CONSUMED |
| **Hook layer** (registry executing at inline hook points; serves rider_on_hit + proc_trigger; HookEntry binder-stamped — generation-time law) | **DESIGN NOTE LANDED 2026-07-11** (`gandalf/notes/2026-07-11-hook-layer-design-note.md`): customer ladder ailment_core→burn-on-physical→proc_trigger · 7 acceptance criteria · depth guard 3 · build fires post-E3-dispatch (gamora-led, math note first) |

## §8 — Proxies + summons

| Surface | State |
|---|---|
| ProxySpawn — generation-only today (`spatial_engine.py` zero proxy handling) | P0 parametric emitters ride motion-frame build; P1 +HP/aggro; P2 +nav/command |
| Proxy octet in the roster (K5/K10/K16 light · K11/K17/K18/K24/K25 heavy) | see `substrate-coordinates.md` |
| Emitted-entity vs proxy/summon attribution boundary | RULING OWED at emission integration (ladder #5) |
| Do proxy/summon attacks carry element today? | VERIFICATION OWED (rocket/gamora) — inheritance-law input |

## §9 — Build ladder (order of mechanical work)

1. **E3 dispatch (NOW):** per-chain scaling derivation · geometry-partition rule + mask constraint · `element_application` block + masks + pins + `HYBRID_RATE` → governed dial · Option C tuple DELETION · `naming_flavor_element` split · scaling-unification T4 · **attribution spine** (star-lord) · `element_application_binder.py` born. Ships `chain_partition` + `geometry_partition`, honestly certified.
2. **HOOK LAYER** (design note LANDED 2026-07-11 — build authority: `gandalf/notes/2026-07-11-hook-layer-design-note.md`): registry at inline hook points; ailment application refactored on as first hook (per-seed proof); rider_on_hit + proc_trigger become element-bound HookEntries; attribution spine = its measurement surface.
3. **COMPONENT ACCOUNTING** (pre-`flat_split`): sim-side component vectors; gamora crit/block math note.
4. **PHASE/STATE AXIS** (pre-`phase_partition`): mark-and-consume design note + placement hearing.
5. **EMISSION PRIMITIVE** (carrier): per rotational addendum §3; pairs with B12 re-cert; boundary ruling at integration.

---

**Signed:** gandalf, 2026-07-11. The coordinate says where a soul sits; this page says what the
forge can actually shape. A kit exploration that reads only one of the two builds either an
unplaceable thing or an unbuildable one.
