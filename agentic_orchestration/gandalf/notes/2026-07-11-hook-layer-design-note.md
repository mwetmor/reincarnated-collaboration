# The Hook Layer — design note (build ladder #2)

> **STATUS:** DESIGN AUTHORITY for the hook-layer build. Authored under Matt's (b) ruling
> (2026-07-11: hook-layer design note fires in parallel with the E3 dispatch) + explicit go
> (*"Agreed — proceed with the hook-layer design note"*). Build fires AFTER the E3 dispatch lands
> (mechanical-reality.md §9 ladder: E3 dispatch → **hook layer** → component accounting → phase
> axis → emission). KR sequences; math note FIRST per Discipline #1.
>
> **Author:** gandalf, 2026-07-11 · **Seams:** gamora (resolver/registry) + rocket (binder
> stamping) + star-lord (attribution spine — already riding the E3 dispatch)
> **Companions:** `canonical/current-to-end-state/mechanical-reality.md` §4 (binding resolver)
> §5 rows 4–5 (the gap this note closes) §7 (Layer-2 + hooks) ·
> `matt_notes_handoff_docs/reap-die-rise-element-application-addendum.md` (rider_on_hit +
> proc_trigger structures) · scaffolding audit
> `agentic_orchestration/gandalf/notes/2026-07-11-hybridity-mechanical-scaffolding-audit.md` §4–§5.

---

## §0 — What this is

ONE event-consumer registry over the damage resolver's existing event emissions, serving BOTH
element-application structures that are declared-not-resolved today: **`rider_on_hit`** (element-bound
rider effects — Matt's verbatim first customer: *"on physical hits, apply burn"*) and
**`proc_trigger`** (chance-gated triggered effects). First hook = the EXISTING ailment application
refactored onto the layer, proving non-regression before any new customer lands.

**The design's one sentence:** hooks are **named points inside `resolve_skill` where a
generation-stamped registry executes** — not post-hoc event replay — so RNG draw order is
preserved and the ailment refactor can prove per-seed identity.

---

## §1 — What EXISTS (engine-verified this session, all line-cited)

| # | Fact | Cite |
|---|---|---|
| 1 | `resolve_skill` emits **8 event types** into `events: list[str]`, returned at `:584`: `on_chaos_immune` :350 · `on_dodge` :445 · `on_block` :458/:488 · `on_hit` :476/:519 · `on_kill` :522 · `on_lifesteal` :582 · `on_crit` :668 (inside `_apply_crit`) · `on_vortex_pull` (vortex metadata, :646 comment) | `simulation/damage_resolver.py` |
| 2 | **ZERO consumers.** The ONLY live sim path routes through the spatial adapter, which unpacks `total_damage, _events = resolve_skill(...)` and drops events **by explicit math-note ruling** ("consume the damage float; events are dropped", §6) | `spatial_gauntlet/spatial_resolver_adapter.py:304`, ruling cited at `:19` |
| 3 | **A Phase-0 stub ancestor exists**: `trigger_handler.py` — docstring declares the intended surface (*"Handles trigger events fired during combat (on_hit, on_kill, on_threshold, etc.). Trigger chains are capped at depth 3"*); `handle_trigger()` body = `pass`; `MAX_TRIGGER_DEPTH = 3`; zero imports anywhere. The hook layer was architecturally anticipated and never built | `simulation/trigger_handler.py` |
| 4 | `layer2_trigger` declared enum: `{on_use, on_hit, on_kill, on_take_damage, periodic, threshold_stack, threshold_hp, sequence}`; only `threshold_stack` is consumed (charge-stack detection generation-side; per-stack passive bonus sim-side) | `generation/skill_schema.py:141` · `generation/charge_stack_generation.py:96` · `damage_resolver.py:327-334` |
| 5 | Ailment application is INLINE in the resolver's effects loop: `elif name in AILMENT_NAMES: _try_apply_ailment(...)` at `:562` (helper at `:977`); silence-style control uses `did_apply_ailment(BASE_AILMENT_CHANCE=0.35, status_resist, roll)` at `:567` | `damage_resolver.py` |
| 6 | **Vocabulary mismatch**: emitted events ∩ declared triggers = `{on_hit, on_kill}` only. Six emitted events have no trigger declaration; six declared triggers have no emission point | facts 1 + 4 |

---

## §2 — THE DESIGN

### 2.1 Hook points, not event replay

Registered entries execute **inline at the existing emission sites** inside `resolve_skill` (and at
the cast site for `on_use`). The `events` list return is UNCHANGED — it becomes the audit
trail/telemetry surface it already half-is. Rationale: post-return dispatch at the adapter would
move ailment RNG draws after all resolution draws → per-seed divergence → the non-regression proof
degrades to statistical. Inline dispatch at the same code position preserves draw order exactly.

### 2.2 HookEntry (generation-stamped, binder-resolved)

```
HookEntry:
  trigger: str             # reconciled vocabulary (§2.3)
  scope: str               # which resolutions fire it: "any" | "physical_chain" |
                           #   "chain:<element>" | "skill:<skill_id>"
  chance: float            # 1.0 for rider_on_hit; <1.0 for proc_trigger
  effect: str              # "apply_ailment" | "spawn_effect" | "grant_buff" | ...
  effect_params: dict      # ailment name, magnitude, duration, geometry ref...
  element: str             # BINDER-STAMPED from element_application (the WHAT — never decided sim-side)
  magnitude_share: float   # binder-derived from rate_band → feeds realized-share accounting
  source_structure: str    # "rider_on_hit" | "proc_trigger" | "ailment_core" (the refactor)
```

Stamped at generation time by `generation/element_application_binder.py` (the E3 binder — this is
its fourth walker family made concrete: `rider_on_hit` → hook entry; `proc_trigger` → trigger
entry, per mechanical-reality.md §4). **The generation-time law holds:** the binder resolves WHAT
(element, share, chance); the sim EXECUTES resolved entries; zero sim-time element decisions.

### 2.3 Vocabulary reconciliation (the fact-6 mismatch, resolved by emission-point class)

| Class | Triggers | Emission point | Stage |
|---|---|---|---|
| Hit-resolution | `on_hit`, `on_crit`, `on_kill`, `on_block`, `on_dodge` | existing resolver sites (§1 fact 1) | **v1** |
| Cast | `on_use` | skill-cast site (E4 cast-state machine adjacency) | **v1** (cheap; site exists) |
| Defender-side | `on_take_damage` | same resolution site, defender-registry lookup | schema v1, **build with first customer** (thorns-class archetype) |
| Tick | `periodic` | `effect_resolver` DoT-tick site | v1.1 (no v1 structure needs it) |
| State | `threshold_hp` | combatant HP transitions (trial-boss ancestor) | v1.1 |
| State | `threshold_stack` | charge-stack machinery — **stays on its own live path** (§1 fact 4); absorb-into-registry = v2 cleanup, not v1 churn | live as-is |
| Cross-skill | `sequence` | **OUT — the phase axis** (build ladder #4); explicitly not this layer | out |
| Audit-only | `on_chaos_immune`, `on_lifesteal`, `on_vortex_pull` | not hookable; telemetry/presentation metadata | out |

### 2.4 Depth guard

`MAX_TRIGGER_DEPTH = 3` carried forward from the Phase-0 stub (a hook whose effect spawns damage
can fire further hooks — on_kill proc → nova → on_hit rider — capped at depth 3; deeper
firings no-op). The stub's one design decision survives into the real build.

---

## §3 — Customer ladder (build order inside the hook-layer dispatch)

1. **`ailment_core` refactor — the non-regression proof.** The `:562` AILMENT_NAMES branch body
   becomes a registry execution at the same code position: each damage skill carrying an ailment
   effect implies exactly one `ailment_core` HookEntry; `_try_apply_ailment` is the execution
   target, unchanged. **Proof standard: per-seed identical fight outcomes on a pinned gauntlet
   population** (achievable because dispatch position + draw order are unchanged). If registry
   iteration introduces draws, fall back to pre-registered statistical tolerances — flagged, never
   silent. Smoke-test mode first (Discipline #2).
2. **`rider_on_hit` — burn-on-physical (Matt's example, the first NEW customer).** Kit: physical
   primary (STR), fire secondary, structure `rider_on_hit`, splash band. Binder emits
   `HookEntry(trigger=on_hit, scope=physical_chain, chance=1.0, effect=apply_ailment,
   effect_params={ailment: burn, …}, element=fire, source_structure=rider_on_hit)`. The physical
   hit lands at `:476` → registry match → burn applies through the SAME refactored machinery →
   burn ticks attribute to FIRE → realized-share lands inside the 10–25% splash band → cert.
3. **`proc_trigger`** — chance-gated entries (`chance < 1.0`) on any v1 trigger; depth guard
   exercised here (proc effects that spawn damage).

---

## §4 — Attribution spine coupling (v1-BLOCKING, star-lord)

Every hook execution stamps `(source element, damage)` into the attribution spine
(kill-attribution-by-element + realized-share columns — riding the E3 dispatch). **The rate-band
law is unenforceable for rider structures without this**: splash 10–25% / co_equal 40–60% are
*realized-output-share* bands, and rider/proc damage is precisely the output that flows through
hooks. The hook layer is the spine's first high-volume customer beyond chain_partition. DoT-tick
attribution (audit §5 open item) joins here: burn ticks credit fire, not the physical carrier.

---

## §5 — What the hook layer is NOT

- **Not the phase axis** — `sequence`/`prerequisite_skill` cross-skill state is build ladder #4.
- **Not presentation** — Godot reads the same resolved fields + events audit trail; no
  presentation-side hook registration (packet-contract discipline, E4 precedent).
- **Not a charge-stack rework** — that machinery stays live as-is (§2.3).
- **Not speculative defender machinery** — `on_take_damage` schema lands v1, build waits for its
  first customer.

---

## §6 — Build shape + acceptance criteria

**Seams:** gamora — hook points, registry, depth guard, `ailment_core` refactor, non-regression
harness (math note first: `simulation/math/hook-layer-<date>.md`, gamora-led, rocket co-signs the
binder contract). rocket — binder stamping (HookEntry emission from `element_application`), schema
fields. star-lord — attribution columns (E3 dispatch scope; this note adds the hook-source stamp).

| # | Acceptance criterion |
|---|---|
| 1 | Registry + hook points live at the five hit-resolution sites + cast site; `events` return unchanged (audit trail) |
| 2 | `ailment_core` refactor: per-seed identical outcomes on a pinned gauntlet population (or pre-registered statistical fallback, flagged) |
| 3 | Burn-on-physical kit emits, resolves, and certs with fire realized-share inside its band |
| 4 | `proc_trigger` entry executes chance-gated; a depth-3 chain terminates (no infinite loops) |
| 5 | Hook damage stamps source element; realized-share columns populate from hook output |
| 6 | Perf ≥30 fights/s preserved (E4 criterion carried) |
| 7 | Generation-time-law audit: zero sim-time element decisions (grep-provable — sim reads stamped fields only) |

**Leans flagged (gandalf decides, Matt may override):** MAX_TRIGGER_DEPTH=3 carried · charge-stack
not absorbed v1 · `on_take_damage` schema-only v1. None gates the build.

---

**Signed:** gandalf, 2026-07-11 — SPEC-AUTHOR. Anchors: mechanical-reality.md §4/§5/§7 ·
element-application addendum · scaffolding audit §4–§5 · `damage_resolver.py` /
`trigger_handler.py` / `spatial_resolver_adapter.py` / `skill_schema.py` (all read this session).
