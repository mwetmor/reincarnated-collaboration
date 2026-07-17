# Wave-C Engine Spec — Trigger + Mark-Consume · Ailment-Wave-C+ · Small-Adds (BT · Orbit · Walls · TH · LC/DR)

**STATUS:** **DRAFT-FOR-GATE-1** (SPEC-AUTHOR complete; DRIFT-CRITIC gate + jack-ryan Gate-1 pending).
**Date:** 2026-07-17
**Author:** gandalf (SPEC-AUTHOR work unit, autonomous atlas-parity run cycle 3)
**Authority:** Matt autonomous-run delegation 2026-07-16 (sub-agents iterate engine toward 100% atlas mechanical parity) + S2 census V9 THE SCOREBOARD ranking the residue tail after Wave-B economy landed. **The §11 escalation rulings this doc records are gandalf-prime rulings under Matt's autonomous-run authority — veto-open, Matt may overturn on read.**

**Companion docs:**
- `./wave-b-economy-engine-spec.md` — THE HOUSE MODEL (STATUS discipline · §10 escalation format · §12 seam-routing · byte-neutrality · commitment_bin extension precedent · §8 damage-taken-converts TH roster · §2.5 AC-2 bias-map STRIKE lineage)
- `./ailment-layer-engine-spec.md` — this spec's ailment §4 EXTENDS it (canonical-names discipline · SECONDARY_AILMENT_MAP · interaction matrix + `max_amp_cap` runaway-guard pattern · shatter-hook expiry-check precedent)
- `../../agentic_orchestration/research/curated/atlas/s2-readiness-census-v9-2026-07-16.md` — THE SCOREBOARD (ranked blocked tail; 509/565 = 90.1% expressible-now baseline)
- `../../agentic_orchestration/research/curated/corpus.db` — DB truth for every per-bucket roster in this spec (single-writer = elrond; this spec writes ZERO rows)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/spatial_engine.py` — per-tick loop + `ActiveEffect` params consumer + PC/RS/AM/RC extension precedent
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/effect_resolver.py` — ailment tick + shatter-hook expiry-check pattern
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/bc_target_composer.py` — the emission composer this spec extends (`_ECON_BIN_COST_TYPE_MAP` · `resolve_cost_type`)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/resource_economy.py` — per-kit config surface (22 keys post-Wave-B; Wave-C adds trigger + charge-conversion fields)
- `/Users/admin/Games/reincarnated-engine/config/ailments.yaml` — the ailment registry Wave-C extends (12 entries post-ailment-wave)
- `/Users/admin/Games/reincarnated-engine/config/roles.yaml` — the 9-role registry (§10 hygiene pass rides here)

---

## §0 — TL;DR

Wave-C closes the residue tail after Wave-B economy landed. **THE HEADLINER is the trigger + mark-consume family** — the chain-grammar bump that lifts Wave-B's single-trigger `proc-loop` primitive into a true trigger→consequence chain grammar (mark-apply then mark-consume, on-event triggers beyond single-armed). Around it: an ailment-wave-c+ closure (blind / curse-hex / fear / deflect / instant-kill / unknown-ailment = 20 kits), the block-trigger `econ:BT` mini-bin (8 kits), two small-add geometries (orbit 6, walls 3), the damage-taken-converts TH primitive (3 kits — the Wave-B §8 carve-out), an LC/DR placement ruling for the 5 remaining life-cost kits, an AC-2 bias-map DEFER, and a bounded roles.yaml `support` hygiene pass.

**Scope IN (seven items + one rider — DB-derived roster counts vs V9 tail):**

| # | Bucket | V9 tail | DB re-verify | Wave-C treatment | Kits |
|---|---|---|---|---|---|
| 1 | **Trigger + mark-consume family** | (headliner) | (grammar; not a bucket) | New primitive grammar | (governs proc-loop successors + PC-shape:proc-loop kits) |
| 2 | ailment-wave-c+ blind | 8 | 8 | New ailment | 7 pure-blind + 1 blind+stun overlap = 8 kits |
| 2 | ailment-wave-c+ curse-hex | 4 | 4 | New ailment | 4 kits |
| 2 | ailment-wave-c+ fear | 4 | 4 | New ailment | 4 kits |
| 2 | ailment-wave-c+ deflect | 2 | 2 | **NOT ailment — defense-side reflect/dodge** | 2 kits (routing ESCALATION) |
| 2 | ailment-wave-c+ instant-kill | 1 | 1 | New ailment (execute-threshold) | 1 kit (vs-gorgeous-moon) |
| 2 | ailment-wave-c+ unknown-ailment | 1 | 1 | **OUT — elrond re-crawl lane** | 1 kit (di-spiritform-druid-pvp) |
| 3 | **econ:BT (block-trigger)** | 8 | 8 | New sub-shape on trigger family (block-event → linked cast) | 8 kits |
| 4a | **geometry:orbit** | 6 | 6 | New geometry_value `orbit` (25th) | 6 kits |
| 4b | **geometry:walls-placed-lane** | 3 | 3 | New geometry_value `placed-lane` (26th) | 3 kits |
| 5 | **LC 3 / DR 2 placement** | 5 | 5 | Per-kit rulings: engine-mechanic vs pool-content | 5 kits |
| 6 | **damage-taken-converts (TH)** | 3 | 3 | New primitive; Wave-B §8 carve-out honored | 3 kits (chr-thorns-templar is PC-tagged, not TH-blocked) |
| 7 | **roles.yaml `support` hygiene** | (governance) | 4 config sites + `gear_generation.py` many | Bounded config sweep + strike-plan | (§10) |
| R | AC-2 bias-map disposition | (Wave-B post-mortem) | (STRICKEN Wave-B, no consumer) | **DEFER** with empirical criterion (§11.h) | (rider) |

**Scope OUT (non-goals — stated in §NG):**
- `mechanic:shapeshift` × 3 — gated by Matt fork rulings A–E (GX-02 docket OPEN).
- `econ:UNKNOWN` × 13 — data-classification work, elrond lane, not spec work.

**Wave-C kit-touch total (gate-lift math):** 8+4+4+2+1 (ailment-wave-c+ minus unknown-ailment × 1) + 8 (BT) + 6 (orbit) + 3 (walls) + 3 (TH) + 3 (LC engine-mech, per §7 lean) = **42 kits unblocked at gate-lift**. Deflect 2 routes defense-side (§4.5) but is unblocked in the same wave; DR 2 defers per §7 lean; unknown-ailment 1 sits in the OUT lane. Net expressible flip on the V9 denominator: **42/565 = +7.43pp**, headline projection **90.1% → ~97.5%** post-Wave-C-landed (barring Wave-C multi-blocker residue in future census).

**Design north star:** Wave-B lifted the econ family. Wave-C lifts **the trigger family + the residue tail**. Same house rules: canonical-names discipline (Ailment §1 precedent), enum-widen (Wave-B §2.6 commitment_bin precedent), byte-neutrality theorem (§9), `max_amp_cap`-style LOCKED runaway guards on any chain-depth (§2.5), math-before-code notes on all conversion formulas (Discipline #1).

**Byte-neutrality theorem:** Absent new fields, today's behavior is byte-identical. Wave-C introduces zero implicit-default changes; every new field's absence = today's semantics. See §9.

**Escalations this doc raises (8 items, count-check §11):**
- (a) Trigger + mark-consume — chain-depth cap **LOCKED at 1** (single-hop mark→consume) vs LOCKED at 2 (Poet's-Pen-of-Poet's-Pen edge cases) — the runaway-guard invariant.
- (b) Trigger vocabulary — `on-mark-apply` / `on-mark-consume` as distinct events vs single `on-mark` with an intent flag.
- (c) Blind — soft_control (accuracy-tax hit-chance modifier) vs mixed_control (accuracy + short movement pause).
- (d) Curse-hex vs sunder collision — is curse a THIRD debuff class (persistent-while-in-range) or a mode-tag on sunder (`persistent_range` sub-shape).
- (e) Fear — soft_control flee AI (target-flees-caster movement modifier) vs hard-control (target action-lockout mimicking stun); interaction with taunt.
- (f) Deflect routing — ailment (defender-side buff class) vs def-bin rider (`riders += "deflect"`) vs new defensive-mechanic-family (WARN: no engine-side def-mechanic-family exists today).
- (g) LC/DR — the 5-kit disposition: which are engine mechanics (spec here) vs pool-content (defer with rationale).
- (h) AC-2 bias-map disposition — DEFER with empirical criterion (SPEC-AUTHOR LEAN: DEFER; DRIFT-CRITIC concurs at draft time).

---

## §NG — Non-goals (Wave-C explicit exclusions)

- **`mechanic:shapeshift` × 3 kits** (la-ferality-wildsoul, la-phantom-beast-awakening-wildsoul, gd-berserker-wereforms) — gated by Matt fork rulings A–E (GX-02 docket OPEN). Wave-C does NOT touch shapeshift emission surface or sim consumer. **Reason:** shapeshift redefines the actor's kit-slot semantics (form-swap = different active-effect roster mid-fight), which is a `combatant_state` architecture question, not an econ or ailment extension.
- **`econ:UNKNOWN` × 13 kits** — data-classification, elrond re-crawl lane. Wave-C does NOT spec these; they carry `econ-audit-ambiguous-2026-07-16` for future substrate resolution. Post-Wave-C census may flip a subset once elrond re-crawl closes; Wave-C engine treatment = zero.
- **CWDT chain-of-triggers with depth > 1** — governed here (§2.5) but as a LOCKED runaway guard, not a spec-out. If Matt overrules the LOCKED cap to 2 at ESCALATION (a), spec extends within the same primitive.

---

## §1 — What already EXISTS (do not rebuild)

Per current engine survey (2026-07-17 pass on Wave-B post-landing state):

| Component | File | State — for Wave-C purposes |
|---|---|---|
| Wave-B `proc_trigger_condition` enum | `resource_economy.py` PC-block (post-Wave-B) | Single-trigger primitive — `{on-hit-threshold, on-crit, on-cast-linked, on-kill, on-damage-taken}`. Chain-grammar HOOK per Wave-B §2.4 note-#2 (Gate-1 CLEAN — no chain leakage). Wave-C adds mark-apply/consume as NEW events, keeping per-trigger-not-per-chain grammar. |
| `commitment_bin` enum | `skill_schema.py:222–223` (post-Wave-B enum-widen) | Existing values include `persistent_trigger` (Wave-B §2.6 addition — the deliberate extension hook). Wave-C EXTENDS `persistent_trigger` semantics; does NOT widen the enum further at the commitment layer (Discipline #12 — additive-in-fields, not additive-in-commitment-values). |
| `_ECON_BIN_COST_TYPE_MAP` | `bc_target_composer.py:~236` | 6 active bins post-Wave-B (`generator-spender`, `starved`, `overflow`, `steady`, `reservation`, `persistent-condition`, `charge-stack`). Wave-C adds `damage-taken-converts` (drops from `_DEFERRED_ECON_BINS` per §7). |
| `_DEFERRED_ECON_BINS` | `bc_target_composer.py:~95` | Post-Wave-B: `frozenset({"HP-economy", "damage-taken-converts"})`. Wave-C drops `damage-taken-converts` → `frozenset({"HP-economy"})`. LC/DR (§7) either DROP `HP-economy` at Wave-C or defer LC to pool-content (§11.g). |
| `resource_economy.py` fields | (22 fields post-Wave-B) | Wave-C extends with trigger-chain fields (§2.6) + `damage_taken_converts_shape`/`conversion_rate`/`conversion_source` (§7) + BT sub-shape fields (§3). No existing field's semantics change. |
| `ailments.yaml` | 12 canonical names post-ailment-wave | Wave-C adds 4 new: `blind`, `curse` (curse-hex canonical name), `fear`, `execute` (instant-kill canonical name — see §4.7 name choice). Deflect does NOT enter here (§4.5 ruling). |
| Ailment apply hook | `damage_resolver._try_apply_ailment` | Extends unchanged for new ailments; blind/curse/fear/execute plug into the same RNG gate + `_add_or_refresh` machinery per ailment §2.3 pattern. |
| Ailment tick loop | `effect_resolver.tick_effects` | Auto-includes new DoT ailments if any (curse-hex will if it inherits DoT semantics; §4.3). Consumer for `execute` runs at expiry-check (shatter-hook precedent per ailment §3.6.i). |
| Geometry composer | `geometry_derivation.py` | Post-ailment-wave includes 24 geometry values. Wave-C adds `orbit` (25th) + `placed-lane` (26th) via new emission-surface rules. |
| Substrate templates | `substrate_templates.py` | Post-Wave-B: `W1_4_CHARGE_STACK` exists (Gate-2 amendment 11 confirmed via REUSE via field). Wave-C templates: `mark_apply_verb`, `mark_consume_burst`, `blind_flash`, `curse_of_frailty`, `fear_wail`, `execute_slam`, `orbit_field`, `wall_of_X`, `thorns_reflect_pulse`. Composition is off FIELDS, not templates (Gate-2 AC-2 finding). |
| `roles.yaml` | 9 canonical roles; `sustain` role carries `"Solo-gated in Phase-1 P1 — support role requires multi-actor context"` (line 142) | This IS the retired-support intent. Wave-C §10 hygiene pass makes the retirement explicit and reconciles `gear_generation.py` role-orientation maps that still carry "support" as an active weight. |
| `bc_target_composer.resolve_cost_type` | `bc_target_composer.py:270+` | Existing behavior: returns `role_priority[0]` on empty map. Wave-C's `damage-taken-converts` bin (§7) MUST carry non-empty map (`["hp"]` per §7.4 — the sole active bin whose taxed pool IS the HP pool). |

**Existing extension points (no new subsystems required):**
- Trigger + mark-consume = new sub-shape fields on `resource_economy` (proc-loop successors) + new `ActiveEffect.params["mark_state"]` on defender + expiry-check consumer at effect_resolver (per ailment §3.6.i shatter-hook precedent).
- Blind/curse/fear/execute = ailment registry additions (per ailment §1 discipline — canonical-names, DoT tick auto-inclusion, `debuff` category reuse where applicable).
- BT = trigger-family sub-shape (`on-block-successful` in trigger vocabulary; §3.4).
- Orbit + walls = geometry_value additions + new emission rules in `geometry_derivation.py`; sim spatial behavior in `spatial_engine.py` (per Wave-A geometry precedent).
- TH = new bin `damage-taken-converts` lifted from `_DEFERRED_ECON_BINS`; sim consumer at `damage_resolver` incoming-hit post-mitigation branch (per Wave-B §3.7 regen-cap-tax precedent).

---

## §2 — TRIGGER + MARK-CONSUME (the headliner)

### 2.1 Delegated ruling recorded (Matt 2026-07-17 autonomous-run, veto-open)

Wave-B's `persistent-condition:proc-loop` sub-shape shipped the **single-trigger primitive** (one armed condition → one linked cast; CWDT / CoC / Poet's Pen each treated as ONE armed trigger). Wave-C ships the **chain grammar** — trigger→consequence sequences where a marker is APPLIED on one event and CONSUMED on a subsequent event. Genre precedent: PoE1 mark-consume grammar (Assassin's Mark → Culling Strike consumes; Warlord's Mark → power charge on kill consumes), D4 Vulnerable → Lucky Hit consume chains, GD Devouring Swarm → chthonian marks that feed Sigil-of-Consumption pulses. **Reincarnated's own SG spirit-guide mark identity** (spirit-marked target = enhanced hit windows) rides this same grammar.

**Distinction from Wave-B's proc-loop:** proc-loop is `EVENT → SPELL` (single hop, no marker). Chain is `EVENT₁ → MARK APPLIED → EVENT₂ → MARK CONSUMED → SPELL`. The state carrier is the marker itself, living on the defender's `active_effects` as a first-class `ActiveEffect` with `name="mark:<identity>"`, `params={applier, source_element, consume_condition, ...}`, and a fixed duration.

### 2.2 Mechanic definition

A **trigger + mark-consume chain** is a two-event skill payoff loop:

1. **Mark-apply event.** A qualifying player action (hit-lands, crit-lands, kill, cast-linked) stamps a marker on the defender via `ActiveEffect` with `name="mark:<identity>"`. The marker carries a duration and a `consume_condition` param naming the event that consumes it.
2. **Mark-consume event.** A qualifying subsequent event (next-hit, crit, kill, ailment-application, defender-death) reads the marker, fires the linked consequence (damage burst, resource fill, ailment overwrite, additional cast), and clears the marker from `active_effects`.

The grammar is **single-hop by LOCKED invariant** (ESCALATION a) — mark-consume events do NOT themselves count as mark-apply events for a chained marker. A consequence-cast that meets a proc-loop trigger (Wave-B PC:proc-loop) fires normally; that is chain-adjacent, not chain-nested. See §2.5 for the LOCKED depth-cap math.

**Genre precedent (chain-family census — evidence pulled to inform grammar):**
- **PoE1 mark curses** (Assassin's Mark / Warlord's Mark / Poacher's Mark) — canonical mark-consume; consume on kill or crit triggers linked payoff.
- **D4 Vulnerable + Lucky Hit chains** — mark-apply on control impact; consume on Lucky Hit rolls.
- **GD Devouring Swarm → Sigil of Consumption** — mark-apply as chthonian debuff; Sigil pulses feed on marked targets.
- **RDR's own SG spirit-mark identity** — spirit-guide's marked-target amp; already partly modeled at Wave-A's spirit-guide seam, this spec brings it under one grammar.
- **Wave-C corpus attestations** — kits carrying trigger-family gaps that need chain grammar: multiple curse-hex kits (§4.2) whose curse APPLICATION is the mark-apply and whose PAYOFF is the mark-consume; poe1-poison-bv's `damage-amp` gap can express as a mark-consume payoff on poison-stack-cap-reached; the 8 BT kits (§3) whose `block-event → linked cast` is a distinct trigger vocabulary entry.

### 2.3 Trigger vocabulary (event types) + Consequence vocabulary

**Trigger event types (rocket enum widening — additive to Wave-B `proc_trigger_condition`):**

```python
# Wave-B baseline (per Wave-B §2.4):
proc_trigger_condition ∈ {
    "on-hit-threshold",       # CWDT — hits above threshold arm trigger
    "on-crit",                # CoC — crits arm trigger
    "on-cast-linked",         # Poet's Pen — linked-spell casts arm trigger
    "on-kill",                # kill-triggered
    "on-damage-taken",        # damage-taken triggered
}
# Wave-C additions (mark-apply + mark-consume grammar):
proc_trigger_condition += {
    "on-mark-apply",          # NEW — event that stamps a marker; fires linked APPLY-cast
    "on-mark-consume",        # NEW — event that consumes a marker; fires linked PAYOFF-cast
    "on-block-successful",    # NEW — block-event trigger (BT bucket, §3)
    "on-ailment-application", # NEW — a fresh ailment stamped on defender (feeds curse-hex chain §4.2)
    "on-defender-death",      # NEW — defender death event (distinct from `on-kill` which fires on the KILLING skill)
}
```

**Consequence vocabulary (rocket enum — the new `consequence_type` field):**

```python
consequence_type ∈ {
    "apply-mark",         # marker stamp on defender
    "consume-mark",       # marker read + payoff + clear
    "linked-cast",        # existing Wave-B (proc-loop successor)
    "resource-fill",      # trigger fills the applier's resource pool (BT precedent)
    "ailment-overwrite",  # trigger overwrites an existing ailment class (mark→sunder promotion)
    "burst-damage",       # trigger fires a burst damage event (shatter-hook precedent, ailment §3.6.i)
}
```

**ESCALATION b — `on-mark-apply`/`on-mark-consume` as distinct events vs single `on-mark` with intent flag** — SPEC-AUTHOR LEAN: **distinct events.** Grounds: the sim consumer branches sharply — mark-apply writes to `active_effects`, mark-consume reads-then-clears. Collapsing them under a single event with intent flag reintroduces the "one event, two responsibilities" anti-pattern Wave-B specifically avoided in the `proc_trigger_condition` design. Distinct events keep the emission surface auditable and the sim consumer branchless-per-event.

### 2.4 Emission fields (rocket)

Extending `resource_economy.py` (currently 22 keys post-Wave-B; Wave-C adds 6 keys — count-verified against `_DEFAULT_ECON` dict inspection):

```yaml
# Wave-C additions to resource_economy per-kit fields:

trigger_chain_shape:               # NEW — required for kits participating in mark grammar
  min: null
  max: null
  default: null
  # one of: {"apply-only", "consume-only", "apply-consume-pair", null}
  # null = kit is not part of a mark chain (Wave-B PC:proc-loop kits stay null here — they're single-trigger).

mark_identity:                     # NEW — string identity of the marker this kit reads/writes
  min: null
  max: null
  default: null
  # one of: {"mark:frailty", "mark:vulnerability", "mark:consumption", "mark:spirit", null}
  # (finite closed set — enum-validated at emission)

mark_apply_event:                  # NEW — trigger event that stamps the mark (for apply-shape kits)
  min: null
  max: null
  default: null
  # one of the `proc_trigger_condition` values from §2.3

mark_consume_event:                # NEW — trigger event that reads+clears the mark (for consume-shape kits)
  min: null
  max: null
  default: null

mark_duration_seconds:             # NEW — how long the mark lives before natural expiry (applies to apply-shape kits)
  min: 0.5
  max: 10.0
  default: 4.0                     # PoE1 mark curse median

consequence_type:                  # NEW — what the mark-consume event fires
  min: null
  max: null
  default: null
  # one of the §2.3 consequence_type values
```

**No new `commitment_bin` values.** Chain participants ride the existing Wave-B `persistent_trigger` commitment_bin (added Wave-B §2.6). QD lattice stays 3; 972-assert intact (§2.8).

### 2.5 Chain-depth cap — LOCKED runaway guard (ESCALATION a)

**Options:**
- **(1) LOCKED at 1** — mark-consume events NEVER themselves count as mark-apply events for a chained marker. The chain is single-hop: EVENT → MARK APPLIED → EVENT → MARK CONSUMED → CONSEQUENCE. If the CONSEQUENCE fires a linked cast that lands a NEW mark, that's a NEW chain — but a chained cast can only apply ONE mark per fire, and only one mark of any given `mark_identity` can exist on a defender at once.
- **(2) LOCKED at 2** — allow ONE nested consume-then-apply cycle. Consequence-of-consume MAY carry `trigger_chain_shape="apply-only"` and stamp a new mark. Genre precedent: PoE1 mark curse + Culling Strike chains can compose Assassin's Mark → crit consumes → new mark applied by triggered spell.
- **(3) UNCAPPED** — as in PoE1 CWDT-of-CWDT loop exploits before patch. Never seriously proposed.

**SPEC-AUTHOR LEAN: (1) LOCKED at 1.** Grounds beyond the runaway argument:
- The RDR sim is single-actor combat (§NG cross-check via `combatant.py` single-actor state); chain-depth-2 does not gain the multi-caster interaction that makes it interesting in PoE1.
- LOCKED-at-1 keeps the sim consumer trivially bounded — mark-consume in tick N cannot fire another mark-apply in the same tick. No re-entrancy guard needed; the `active_effects` mutation is safe within `effect_resolver.tick_effects`'s single-pass iteration.
- Empirical evidence: the 20 ailment-wave-c+ kits + 8 BT kits + 6 orbit kits + 3 TH kits collectively imply single-hop chains. **NO Wave-C-scope kit needs depth-2** at DB-truth (verified via raw_json inspection of the 20 ailment kits — no `mark-of-a-mark` construct present).
- Genre precedent for uncapping is uniformly cautionary — PoE1 CWDT-loop exploits, Diablo IV Nightmare-mark-chain patches, D3 firebird's-finery infinite-mark iterations — all patched OUT because of runaway sim cost.

**LOCKED INVARIANT:** `MAX_CHAIN_DEPTH = 1` (state as Python constant in `spatial_engine.py` — like `max_amp_cap = 0.50` in ailment §2.4). Sim asserts on any consequence-cast attempting to write to `defender.active_effects` when a mark-consume just fired in the same tick.

**Math note (Discipline #1):** Chain grammar produces payoff-per-mark = `apply_probability × consume_probability × consequence_magnitude`. At depth-1, payoff is bounded by `p_apply × p_consume × magnitude`. At depth-2, payoff is `(p × magnitude)²` — quadratic runaway is only theoretical at depth-2, but the LOCKED-at-1 rule holds the invariant trivially. See §13.1.

### 2.6 Mark state model + emission-vs-consumer flow

**Mark as `ActiveEffect`:**

```python
# Sim-side representation of a live mark:
ActiveEffect(
    name="mark:frailty",          # or "mark:vulnerability", "mark:consumption", "mark:spirit"
    params={
        "applier": <combatant_id>,
        "source_element": <element>,
        "consume_condition": "on-crit" | "on-kill" | ...,   # matches an emission's mark_consume_event
        "consequence_type": "burst-damage" | "resource-fill" | ...,
        "consequence_magnitude": <float, tune-band 0.1–0.5 of defender max HP or applier max resource>,
    },
    duration_remaining=<mark_duration_seconds>,
    source_element=<element>,
    tick_accumulated=0.0,
)
```

**Flow (per-tick):**

1. Player kit with `trigger_chain_shape="apply-only"` fires, event matches `mark_apply_event` → stamp `ActiveEffect(name="mark:<identity>")` on defender (`_add_or_refresh` policy — see §2.7).
2. Any subsequent tick, engine checks per-event: is there a live mark on defender whose `params["consume_condition"]` matches the current event? If yes, fire the consequence, then remove the mark from `active_effects`.
3. Marks expire naturally at `duration_remaining <= 0` (no consequence; the mark simply ends).

**Consumer sites (gamora):**
- Mark-apply: `damage_resolver._add_or_refresh` extension — reuses the ailment refresh law (later application refreshes duration; magnitude unchanged since marks are boolean-per-identity).
- Mark-consume: NEW branch in the per-tick loop at `spatial_engine.py:~1804` (accumulator on-kill fill precedent) + at `damage_resolver.resolve_skill` (on-hit / on-crit consume branch).
- Mark-expiry: `effect_resolver.tick_effects` at `duration_remaining <= 0` (per ailment §3.6.i shatter-hook precedent — same expiry-vs-cull ordering: check BEFORE cull).

### 2.7 Interaction with Wave-B PC:proc-loop sub-shape (extension hook honored)

Wave-B §2.6 added `persistent_trigger` commitment_bin as the "deliberate extension hook" for chain grammar. Wave-C uses it exactly: a kit with `trigger_chain_shape != null` sets `commitment_bin = "persistent_trigger"` (already permitted per Wave-B enum). The Wave-B PC:proc-loop kits are NOT retroactively converted to chain — they remain single-trigger under `commitment_bin = "persistent_trigger"`, `trigger_chain_shape = null`. This is the two-state distinction:

| commitment_bin | trigger_chain_shape | Kit family |
|---|---|---|
| `persistent_toggle` | (null) | Wave-B PC aura-toggle / tick-cost |
| `persistent_trigger` | (null) | Wave-B PC proc-loop (CWDT / CoC / Poet's Pen) — SINGLE-HOP |
| `persistent_trigger` | `apply-only` | Wave-C chain — kit stamps a mark |
| `persistent_trigger` | `consume-only` | Wave-C chain — kit reads-and-clears a mark |
| `persistent_trigger` | `apply-consume-pair` | Wave-C chain — kit stamps AND consumes in the same skill definition (e.g., a two-verb curse: apply-on-cast, consume-on-target-death) |

**Wave-B `proc_trigger_condition` enum: additive-widened only.** No existing value's semantics change; Wave-C adds `on-mark-apply`, `on-mark-consume`, `on-block-successful`, `on-ailment-application`, `on-defender-death`. Wave-B kits do not need re-emission — their `proc_trigger_condition` values continue to resolve identically.

### 2.8 QD lattice invariant — 3 stays LOCKED; 972-assert intact

The QD lattice is (attribute × range × tempo × amp × proxy × commitment) = 3⁵ × 3 = 3⁶ = 972 with `COMMITMENT_BINS=3`. Wave-C **DOES NOT WIDEN `COMMITMENT_BINS`.** Chain participants use the existing `persistent_trigger` value added at Wave-B. `per_skill_emitter.py:400` already commented: `.COMMITMENT_BINS, 972-assert) is DELIBERATELY LEFT at 3 — toggle/trigger are PC-kit-ROUTED shapes` — Wave-C respects this. Chain grammar rides `resource_economy` fields (§2.4), not lattice dimensions.

**LOCKED INVARIANT (verify at Gate-1):** `assert CATALOG_LATTICE_WITH_COMMITMENT == 972` at `bc_target_cell_sampler.py:395` must continue to pass post-Wave-C build. If any Wave-C branch attempts to widen `COMMITMENT_BINS`, that branch is REJECTED at Gate-1 (BLOCK).

### 2.9 DL-03 conformance

- Mark-apply is a per-event stamp — does not tax caster movement.
- Mark-consume is a per-event read+payoff — does not tax caster movement.
- The chain grammar is **entirely defender-side state**; the caster's commitment_bin governs their own skill's animation, not the chain.

**DL-03 PASSES for all three trigger_chain_shape sub-shapes.**

### 2.10 Calibration guardrails (gamora tunes)

- **HARD guard: `MAX_CHAIN_DEPTH = 1`** — LOCKED per §2.5 ruling.
- **HARD guard: one mark per `mark_identity` per defender.** Re-application of the same identity refreshes duration; consume-then-fresh-apply within the same tick is allowed (mark cleared, then new mark stamped).
- **HARD guard: `mark_duration_seconds ≤ 10.0`** — no perpetual marks; PoE1 mark curses max out around 8s with duration investment.
- **SOFT guard: `consequence_magnitude` tune-band per consequence_type:**
  - `burst-damage`: 0.10–0.30 of defender max HP (shatter-hook analog).
  - `resource-fill`: 0.10–0.40 of applier max resource.
  - `linked-cast`: no direct magnitude (cast fires linked skill's own tuning).
  - `apply-mark`: no direct magnitude (marker is boolean-per-identity).
- **Runaway check at S6 gauntlet:** verify chain kits do not exceed baseline DPS by > 1.5× when both apply and consume chain-parts land within the same encounter (S6 mirror-match rule).
- **Trigger cadence:** consume-event checks fire at most once per tick per mark; a fast-cadence primary-attack kit landing 5 hits per tick still only fires the consume once. Enforced at `_add_or_refresh` (same-tick idempotence).

---

## §3 — econ:BT (block-trigger; 8 kits — the mini-bin folded into trigger family)

### 3.1 Delegated ruling recorded (Matt 2026-07-17 autonomous-run, veto-open)

**BT = block-trigger.** A block event (successful defensive block) arms a trigger that fires a linked cast, resource fill, or ailment application. Wave-B explicitly left BT out (Wave-B §4 sidebar: "block-trigger BT deferred — the block-event vocabulary needs proc-loop's chain grammar to land first"). Wave-C ships it as a **sub-shape of the trigger family (§2)**, not a standalone econ_bin. The mechanic is a specialized `on-block-successful` trigger vocabulary (§2.3 additive), with the taxed pool being either resource-fill (D2 Zealot rage-fill-on-block) or damage-conversion (chr-thorns-templar block→reflect-pulse).

### 3.2 Mechanic definition

Block-trigger = an event-triggered payoff loop where the arming event is a successful defensive block (`def.riders` carries `trigger:block` flag on existing kits — grep-confirmed on d2-charger, chr-thorns-templar). The trigger consequence is one of:
- **Resource-fill** — block success fills applier's resource pool by a fixed magnitude or % of max (D2 Zealot fanaticism-on-block, D2 Hammerdin holy-shield block-charge).
- **Linked-cast** — block fires a linked skill (di-crusader-banner-support banner-refresh-on-block).
- **Mark-apply** — block stamps a mark on the attacker (hades1-beowulf-cast cast-attempt-on-block-flourish).
- **Damage-reflect** — block converts absorbed damage into reflect payload (chr-thorns-templar barrier-pulse-on-block; overlaps with TH §6).

The chain grammar of §2 governs BT natively: `commitment_bin = "persistent_trigger"` + `proc_trigger_condition = "on-block-successful"` + `consequence_type` per sub-shape.

### 3.3 Roster (DB-verified, 8 kits, all `econ_gaps` ⊇ `BT`)

| kit_id | folk_name | game | econ_gaps | economy_model | BT sub-shape mapping |
|---|---|---|---|---|---|
| `d2-charger` | Charger | d2 | `["BT"]` | spend | linked-cast (charge arms shield-throw follow-up) |
| `d2-hammerdin` | Hammerdin | d2 | `["BT"]` | spend | resource-fill (holy shield block → mana on-block; classic D2 Hammerdin sustain) |
| `d2-smiter` | Smiter | d2 | `["UNKNOWN", "BT"]` | free | resource-fill (Smiter's Smite is the block-followup verb; block arms next smite) |
| `d2-zealot` | Zealot | d2 | `["UNKNOWN", "BT"]` | free | resource-fill (Fanaticism aura + block-cadence combo) |
| `di-crusader-banner-support` | Banner Support Crusader | di | `["BT"]` | cooldown | linked-cast (block-successful → banner refresh event) |
| `chr-thorns-templar` | Thorns Barrier Templar | chronicon | `["PC", "BT"]` | free | damage-reflect (dovetails with §6 TH primitive; PC gap resolved Wave-B) |
| `hot-shieldmaiden-block` | Block-Stack Shieldmaiden | hot | `["PC", "BT"]` | free | resource-fill (block-stack builds fury for follow-up strike) |
| `hades1-beowulf-cast` | Beowulf Cast Build | hades1 | `["AM", "BT"]` | finite | mark-apply (block-cast arms retrieve-bash mark on attacker; AM gap resolved Wave-B) |

**Roster verification vs V9 tail:** V9 tail lists `econ:BT` at 8 kits; DB re-verify confirms 8. **No disagreement.** Note that 3 kits (d2-smiter, d2-zealot, hades1-beowulf-cast, chr-thorns-templar, hot-shieldmaiden-block) are multi-blocked; the BT resolution unblocks them only when their other blockers also land (chr-thorns-templar's PC landed Wave-B; hot-shieldmaiden-block's PC landed Wave-B; hades1-beowulf-cast's AM landed Wave-B; d2-smiter/d2-zealot's UNKNOWN sits in the elrond re-crawl lane §NG).

### 3.4 Sub-shape choice — trigger-family fold vs own bin

**Options:**
- **(A) BT folds into trigger family (§2) as `on-block-successful` trigger vocabulary.** No new econ_bin; existing PC:proc-loop machinery + Wave-C chain grammar handles BT natively. Emission surface = kit sets `commitment_bin="persistent_trigger"`, `proc_trigger_condition="on-block-successful"`, `consequence_type=<sub-shape>`, plus consequence-specific fields.
- **(B) BT as own econ_bin `block-trigger`.** New composer entry + new cost_type map. Semantic clarity but code-cost.

**SPEC-AUTHOR LEAN: (A) fold into trigger family.** Grounds:
- BT is trigger-family behavior with a specialized arming event. The event is data (trigger vocabulary), not architecture (bin).
- Wave-B specifically extended `commitment_bin` to `persistent_trigger` as the "deliberate extension hook" for exactly this kind of vocabulary. Adding a new bin re-litigates Wave-B's ruling.
- The 8-kit roster maps cleanly onto §2's existing `consequence_type` enum (resource-fill, linked-cast, mark-apply, damage-reflect via TH §6). No BT-specific consequence type is required.

**No ESCALATION** here (SPEC-AUTHOR treats this as a routing call within §2's architecture, not a contested design call). Gate-1 may promote to ESCALATION if disagreement surfaces.

### 3.5 Emission fields

No NEW fields beyond §2.4. BT kits emit:

```yaml
# Per-kit resource_economy config for BT kits (all reuse Wave-C §2.4 fields):
commitment_bin: "persistent_trigger"
proc_trigger_condition: "on-block-successful"   # Wave-C §2.3 addition
trigger_chain_shape: null OR "apply-only"       # depends on whether block arms a mark
consequence_type: "resource-fill" | "linked-cast" | "apply-mark" | "burst-damage"

# For resource-fill BT sub-shape (D2 Hammerdin / D2 Zealot / hot-shieldmaiden-block):
accumulator_max: <block-cadence stack cap; 1-10>
accumulator_fill_trigger: "on-block-successful"   # NEW enum value added at Wave-C §2.3
accumulator_fill_amount: <resource units per block, 0.05-0.20 of max>
# (reuses Wave-B AM sub-shape machinery — accumulator was designed for this class of trigger)
```

### 3.6 Sim consumer site

**Consumer site:** `damage_resolver.resolve_skill` block-branch — extend the existing block-outcome handler (where `def.riders` contains `trigger:block` and the block roll succeeds) to fire a `proc_trigger_condition="on-block-successful"` event through the trigger-family machinery per §2.6.

**Placement:** AFTER block-mitigation resolves; BEFORE damage-dealt attribution stamps. The block-event fire is a distinct sim step from the damage-taken step.

**gamora scope:** wire block-outcome → trigger dispatch. Reuses §2.6 flow entirely. No BT-specific consumer.

### 3.7 Interaction with existing `def.riders += "trigger:block"` flag

The `def.riders` field carries `"trigger:block"` on d2-charger, chr-thorns-templar, hot-shieldmaiden-block, hades1-beowulf-cast (grep-confirmed via raw_json inspection §3.3 evidence). This flag was authored pre-Wave-B for the def-bin classification pass; it declares that the kit has a block-mechanic surface. **Wave-C reads this flag as a CANDIDATE-SIGNAL** for BT-eligible kits but does NOT rely on it as the sole entry point — the emission surface is `proc_trigger_condition="on-block-successful"`, and any kit whose raw_json declares a block-trigger relationship qualifies.

**No flag change owed.** `def.riders` semantics unchanged; Wave-C is a new READ of an existing signal.

### 3.8 Calibration guardrails

- **HARD guard: `accumulator_fill_amount ≤ 0.20 of max resource per block`** — prevents block-farming as primary sustain.
- **HARD guard: BT + PC:tick-cost composition** — chr-thorns-templar has both a PC:tick-cost aura AND a BT reflect. Verify total resource drain does not stall pool regen; smoke-gate mirror-match (see §12.5).
- **SOFT guard: `mark_duration_seconds` default 4.0** for BT-triggered marks (hades1-beowulf-cast retrieve-bash mark) — matches PoE1 mark-median.
- **CC-density check:** BT kits that also carry hard-CC ailments (d2-smiter's `GAP-AILMENT:stun` overlap — but stun already landed ailment-wave) risk block-CC-lock chains. Smoke-gate at S6.

---

## §4 — Ailment-Wave-C+ (20 kits; extends ailment-layer-engine-spec)

**Preamble.** Wave-C extends the ailment registry (currently 12 canonical names post-ailment-wave: `burn`, `chill`, `root`, `knockback`, `bleed`, `shock`, `consecrate`, `drain`, `sunder`, `freeze`, `stun`, `poison`) by adding **4 new ailments** (blind, curse, fear, execute) plus **2 routing rulings** (deflect → def-bin rider; unknown-ailment → elrond lane). All 4 new ailments follow ailment-layer-engine-spec's §1 discipline: canonical name locked at emission, DoT tick auto-inclusion via `_DOT_AILMENT_NAMES` registry refresh, `_add_or_refresh` reuse for stacking, `debuff` category reuse where applicable, interaction matrix rows added.

### 4.1 Blind — new ailment (accuracy-tax; 8 kits)

**Delegated ruling recorded (Matt 2026-07-17 autonomous-run, veto-open).**

**Blind = timed % attack-accuracy reduction on target.** Not a movement or action lockout; a hit-chance modifier that the target's next N attacks or a duration window suffers. Genre precedent: PoE1 blind (50% reduced chance to hit, boolean), D2 Blind Sight passive (reduced enemy defense/accuracy), D4 Rogue smoke-grenade blind (miss chance), Hades Athena Blur (deflect+blind adjacency).

**Roster (DB-verified, 8 kits):**

| kit_id | folk_name | game | ailment_gaps | element_signal |
|---|---|---|---|---|
| `d2-wl-blood-boil` | Blood Boil Warlock | d2 | `["GAP-AILMENT:blind"]` | shadow |
| `d2-wl-tainted-summoner` | Tainted Summoner Warlock | d2 | `["GAP-AILMENT:blind"]` | shadow |
| `d4-death-trap` | Death Trap Rogue | d4 | `["GAP-AILMENT:blind"]` | shadow/physical |
| `d4-dread-claws-warlock` | Dread Claws Warlock | d4 | `["GAP-AILMENT:blind"]` | shadow |
| `d4-infinimist` | Infinimist Necromancer | d4 | `["GAP-AILMENT:blind"]` | shadow |
| `d4-shadowblight` | Shadowblight Necromancer | d4 | `["GAP-AILMENT:blind"]` | shadow |
| `poe2-acolyte-darkness` | Darkness Acolyte | poe2 | `["GAP-AILMENT:damage-amp", "GAP-AILMENT:blind"]` | shadow (Darkness = shadow-primary) |
| `poe2-witchhunter-grenades` | Grenadier Witchhunter | poe2 | `["GAP-AILMENT:stun", "GAP-AILMENT:blind"]` | physical (flash-grenade) |

**Pattern reading:** 7/8 kits are shadow-primary (shadow's canonical ailment identity is `drain`; blind rides shadow as SECONDARY — like stun rides lightning). 1/8 is physical (flash-grenade concussive adjacency; blind rides physical as SECONDARY on `heavy_hit` or explosive tags — similar to how stun rides physical).

**Category classification (ESCALATION c — soft_control vs mixed_control):**

- **(a) soft_control (accuracy-tax only, no movement/action modifier).** Blind is a hit-chance debuff; the target continues acting but its attacks land at reduced chance. Genre-native model (PoE1, D2, D4 all model blind as pure accuracy-tax).
- **(b) mixed_control (accuracy-tax + brief pause / stagger).** Some genre models (Diablo IV smoke grenade has a "confused" pause micro-window). Adds an action-interrupt secondary effect.

**SPEC-AUTHOR LEAN: (a) soft_control (accuracy-tax only).** Grounds:
- Cleaner interaction matrix (blind + stun compose additively as soft+hard control; if blind carries a hard-CC micro-pause, stack semantics fight the existing hard-CC immunity-after-expiry law of ailment §4.5).
- Corpus dominant pattern is pure accuracy-tax (7/8 kits).
- The one arguable case (poe2-witchhunter-grenades flash-grenade) already carries `stun` in ailment_gaps for the pause portion — blind is the accuracy-tax rider layered on stun's pause. Separate concerns.

**Params + defaults:**

```yaml
- name: blind
  description: >
    Timed reduction in target's attack accuracy. Soft-control ailment;
    does not lock movement or action. Shadow's canonical secondary
    (per element_biases.py SECONDARY_AILMENT_MAP), riding physical
    when carried by explosive/flash-grenade substrates.
  is_control: soft
  category: soft_control
  param_ranges:
    accuracy_reduction_percent:
      min: 0.20        # PoE1-min-blind
      max: 0.60        # PoE1-cap-blind
      default: 0.40    # median band
    duration_seconds:
      min: 1.5
      max: 5.0
      default: 3.0
  ai_priority: 3       # soft-control fires after hard-CC, before DoT
```

**Application sources:** shadow-primary skills (SECONDARY_AILMENT_MAP: `shadow → [drain (primary), blind (secondary)]`); physical explosive-tag skills (grenade / flash / concussive-adjacent).

**Sim consumer:** `damage_resolver.resolve_skill` attacker-side attack-accuracy composition — the attacker's `active_effects` scanned for `name=="blind"`; if present, apply `attack_hit_chance *= (1 - accuracy_reduction_percent)` at the hit-roll composition. Placement: at hit-roll composition step, BEFORE damage calculation (misses skip damage entirely).

**Stacking / refresh:** single-instance-per-target; refresh takes max magnitude + max duration (mirrors ailment §2.6 sunder single-instance-refresh law).

**Interaction matrix rows** (extending ailment-layer-engine-spec §7 interaction matrix):

| Composition | Interaction |
|---|---|
| blind × stun | ADDITIVE (blind stays; stun locks action; stun expiry re-exposes blind's accuracy-tax) |
| blind × chill | ADDITIVE (blind on attack; chill on movement — different vectors, no collision) |
| blind × freeze | REDUNDANT during freeze (target cannot act; blind's accuracy-tax has no denominator) — but blind PERSISTS through freeze and re-applies on freeze-expiry |
| blind × sunder | ADDITIVE across defenders' attacks and incoming damage (blind reduces THEIR hits landing; sunder amplifies YOUR hits landing) — no collision |
| blind × poison | INDIRECT — blind on defender doesn't affect poison ticks (DoTs bypass hit-rolls); ADDITIVE |
| blind × execute | THRESHOLD-INTERACTION — blind reduces execute-hit's chance of landing; if execute hits, threshold applies normally |

**DL-03 conformance:** blind is defender-side accuracy debuff; does not tax caster movement. PASSES.

### 4.2 Curse-hex — new ailment class or sunder-mode-tag (4 kits; ESCALATION d)

**Delegated ruling recorded (Matt 2026-07-17 autonomous-run, veto-open).**

**Curse-hex** = a **persistent-while-in-range** debuff class — the debuff PERSISTS as long as the caster's aura or curse-effect is within range of the defender, and clears when caster or aura moves out of range or curse duration expires. Genre precedent: D2 Necromancer curses (Weaken, Amplify Damage, Decrepify, Lower Resist — persistent aura-radius model), PoE1 curse gems (Vulnerability, Enfeeble, Temporal Chains — apply-once-and-tick model with % modifier), LE curse-hex family (Ghostflame Warlock's `RS`-tagged curse-reservation), Chronicon Plague Curse Warlock (curse+DoT hybrid).

**Roster (DB-verified, 4 kits):**

| kit_id | folk_name | game | ailment_gaps | econ_gaps | Pattern reading |
|---|---|---|---|---|---|
| `hot-warlock` | Warlock (summon caster) | hot | `["GAP-AILMENT:curse/hex"]` | `[]` | pure curse — summon-adjacent curse aura |
| `le-ghostflame-warlock` | Ghostflame Warlock | le | `["GAP-AILMENT:curse/hex"]` | `["RS"]` (Wave-B) | curse + RS-reservation composite (Wave-B RS lifted) |
| `le-chthonic-fissure-warlock` | Chthonic Fissure Warlock | le | `["GAP-AILMENT:damage-amp", "GAP-AILMENT:curse/hex"]` | `[]` | curse + sunder overlap — the ESCALATION d cross-check exhibit |
| `chr-plague-curse-warlock` | Plague Mage / Desecrator Curse Warlock | chronicon | `["GAP-AILMENT:poison-dot", "GAP-AILMENT:curse/hex"]` | `["AM"]` (Wave-B) | curse + poison + AM composite |

**ESCALATION d — curse-hex vs sunder collision — new ailment vs sunder-mode-tag:**

- **(1) NEW AILMENT `curse` (persistent-while-in-range debuff class).** Distinct from sunder (which is per-target timed multiplier). Semantic axis: sunder = target-carried timer (target keeps sunder for N seconds regardless of caster position); curse = caster-radius-carried effect (target loses curse the moment they leave caster's aura or curse ends).
- **(2) SUNDER-MODE-TAG — curse is sunder with `persistent_range` sub-shape.** Same debuff-multiplier semantics, mode-flagged to persist while in range. Composer routes both under sunder bin.

**SPEC-AUTHOR LEAN: (1) new ailment `curse`.** Grounds:
- Sunder is per-defender-timed (the target CARRIES the debuff). Curse is per-caster-radius (the CASTER'S presence maintains the debuff). This is a fundamentally different consumer contract:
  - Sunder consumer reads `defender.active_effects` for `name=="sunder"` at damage composition.
  - Curse consumer reads `defender.active_effects` for `name=="curse:<variant>"` AND validates the applier's position vs curse aura radius.
- Curse variants in the corpus (`Amplify Damage` = amplification-curse; `Weaken` = damage-reduction-curse; `Decrepify` = slow-curse; `Temporal Chains` = speed-curse) span multiple effect types, NOT just damage-amp. Folding into sunder collapses this variant space to one debuff.
- Chr-plague-curse-warlock's DoT+curse composite argues for curse being architecturally a debuff-class-with-variants, not a sunder-mode.

**Params + defaults (assuming ruling 1):**

```yaml
- name: curse
  description: >
    Persistent-while-in-range debuff class. The debuff persists while the
    applier's curse aura (or curse spell duration) covers the defender;
    clears when applier moves out of range or duration expires.
    Variants: {amplify (damage-taken multiplier), weaken (damage-dealt reduction),
    decrepify (movement slow), sap (defense reduction)}.
  is_control: none  # curse is a debuff; not directly control (but slow-variant behaves control-adjacent)
  category: debuff  # reuses the debuff category (per ailment-layer §2.3 sunder ruling)
  param_ranges:
    curse_variant:
      min: null
      max: null
      default: "amplify"
      # one of: {"amplify", "weaken", "decrepify", "sap"}
    magnitude:
      min: 0.10
      max: 0.40
      default: 0.20   # median debuff magnitude
    duration_seconds:
      min: 5.0
      max: 15.0        # curse endures longer than sunder — genre precedent (PoE1 curse median 10s)
      default: 10.0
    range_radius:      # aura-radius mode; null for spell-duration mode
      min: null
      max: null
      default: null    # null = spell-duration; number = aura-radius (curse persists only while defender ≤ radius from applier)
  ai_priority: 3     # debuff fires after hard-CC
```

**Application sources:** shadow-primary skills (SECONDARY_AILMENT_MAP: `shadow → [drain (primary), curse (secondary)]`); necromancer / warlock templates natively; poison-primary skills carry `curse:decrepify` (slow-variant) as secondary rider on plague-templates (chr-plague-curse-warlock evidence).

**Sim consumer:** at damage composition + at defender movement tick, read `defender.active_effects` for `name=="curse:<variant>"`; apply the variant-specific modifier. For range-mode curses, ADDITIONALLY validate `dist(applier, defender) ≤ range_radius`; clear if out of range.

**Stacking / refresh:** one curse per `curse_variant` per defender (four variants can coexist). Re-application refreshes max magnitude + max duration.

**Interaction matrix rows:**

| Composition | Interaction |
|---|---|
| curse:amplify × sunder | ADDITIVE (curse's amplify-magnitude adds to sunder's damage_taken_percent, subject to `max_amp_cap=0.50` — the LOCKED runaway guard from ailment §2.4 applies to the total) |
| curse:weaken × blind | ADDITIVE (curse's damage-out reduction + blind's hit-chance reduction compose multiplicatively on attacker) |
| curse × freeze | curse PERSISTS through freeze (no action, but debuff remains) |
| curse:decrepify × chill | ADDITIVE (both slow multipliers compose; cap at 0.90 movement reduction per ailment §chill law) |

**DL-03 conformance:** curse is defender-side debuff; does not tax caster movement. Range-mode curses do tax the CASTER'S maintenance-of-range (the caster must stay near defender), which is a soft commitment on caster movement — but this is a design feature, not a violation. **PASSES with note:** range-mode curses (`range_radius != null`) are intentional caster-anchoring mechanics; their emission surface flags this to the AI scheduler.

### 4.3 Fear — new ailment (flee AI; 4 kits; ESCALATION e)

**Delegated ruling recorded (Matt 2026-07-17 autonomous-run, veto-open).**

**Fear** = a **flee-response AI modifier** applied to defender. The target flees the applier (attempts to increase distance) for a timed window; target's attack targeting on applier is disabled during window. Genre precedent: D2 Terror curse (Necromancer, causes fleeing), D3 Fear Effect (multiple sources — witch doctor, monk), D4 Necromancer Fear active, Chronicon fire-berserker Terror aura, Hades cast-Panic modifier.

**Roster (DB-verified, 4 kits):**

| kit_id | folk_name | game | ailment_gaps | econ_gaps | Pattern reading |
|---|---|---|---|---|---|
| `chr-fire-berserker` | Fire Avatar Berserker | chronicon | `["GAP-AILMENT:fear"]` | `["PC"]` (Wave-B) | fire aura + fear-radius (fire-signature secondary) |
| `di-blood-knight` | Blood Knight (vampiric hybrid) | di | `["GAP-AILMENT:fear"]` | `[]` | vampiric drain + fear composite |
| `tq-liche-king-conjurer` | Liche King Conjurer | tq | `["GAP-AILMENT:fear"]` | `[]` | necromancer summoner + fear rider |
| `chr-demon-legion-warlock` | Demon Legion Warlock | chronicon | `["GAP-AILMENT:taunt", "GAP-AILMENT:fear"]` | `["RS"]` (Wave-B) | fear + taunt composite — the ESCALATION e interaction exhibit |

**ESCALATION e — fear as soft_control flee AI vs hard-control action-lockout:**

- **(A) soft_control flee AI.** Target retains action + move but AI target-selection actively moves away from applier; hit-targeting on applier disabled or de-prioritized. Player-agency preserved (player still moves, still attacks other targets).
- **(B) hard-control action-lockout.** Fear locks target's actions entirely (mimicking stun's mechanic). Genre precedent narrower — D2 Terror is closer to (A) than (B).

**SPEC-AUTHOR LEAN: (A) soft_control flee AI + explicit fear/taunt exclusive-slot interaction.** Grounds:
- Genre-dominant pattern is fleeing behavior, not action-lockout (D2/D3/D4/Chronicon all model as flee-AI).
- Interaction with `taunt` (Wave-A landed ailment): fear and taunt are POLAR OPPOSITES (taunt = target-must-attack-applier; fear = target-must-flee-applier). Simultaneous fear+taunt on the same target creates AI contradiction. **Rule: fear and taunt are EXCLUSIVE — later application supersedes earlier; earlier is cleared.** This is chr-demon-legion-warlock's exact composition case (carries both taunt+fear in the same kit; the kit fires them on different targets — evidence dossier or the AI cannot coherently target-vs-flee same defender).
- Preserving player agency: (A) does not lock defender's ability to counter-attack OTHER players (moot in single-actor RDR, but semantically clean); (B) is a stun-clone with a different name.

**Params + defaults (assuming ruling A):**

```yaml
- name: fear
  description: >
    Timed flee-response AI modifier. Target attempts to move away from applier
    and cannot select applier as attack target during window. Soft-control ailment;
    action + non-applier-directed attacks remain available. EXCLUSIVE with taunt
    (applying fear clears any existing taunt on target; applying taunt clears fear).
  is_control: soft
  category: soft_control
  param_ranges:
    flee_speed_multiplier:
      min: 1.0   # normal speed away from applier
      max: 1.5   # panic-speed (fleeing faster than normal)
      default: 1.2
    duration_seconds:
      min: 1.5
      max: 5.0
      default: 3.0
    fear_range:                          # applier-distance beyond which fear naturally lifts (fleeing DID work)
      min: null
      max: null
      default: null                       # null = fear runs to duration; number = distance-triggered lift
  ai_priority: 2   # soft-control fires before DoT
```

**Application sources:** fire-primary skills carry fear as SECONDARY (chr-fire-berserker evidence — terror aura on fire-avatar template); shadow / necromancer templates carry fear as secondary (tq-liche-king-conjurer, di-blood-knight); NOT holy (thematic collision — holy inspires courage, not fear); NOT physical.

**Sim consumer:** at defender AI tick, if `active_effects` contains `name=="fear"`, override target-selection: (a) set movement vector AWAY from `applier`, (b) exclude `applier` from attack-target candidates. Fear does NOT block defender's other actions or attacks on non-applier targets.

**Stacking / refresh:** single-instance-per-target. Re-application refreshes duration to `max(existing, incoming)`.

**Interaction matrix rows:**

| Composition | Interaction |
|---|---|
| fear × taunt | EXCLUSIVE — later application clears earlier (see ESCALATION e lean) |
| fear × chill | ADDITIVE — chill slows movement (all vectors); fear directs movement — target flees SLOWER but still flees |
| fear × root | fear SUPPRESSED — root pins defender in place; fear's movement-vector-override has no denominator until root expires |
| fear × freeze | fear SUPPRESSED — same as root |
| fear × stun | fear SUPPRESSED during stun; fear's target-exclusion re-activates on stun-expiry |
| fear × blind | ADDITIVE — fear's target-exclusion + blind's accuracy-tax compose (though target-excluded attacker doesn't hit-roll on applier anyway) |
| fear × curse:decrepify | ADDITIVE — fear's away-vector + curse's speed-slow; net effect is slow-fleeing (thematic and mechanical fit) |

**DL-03 conformance:** fear is defender-side AI modifier; does not tax caster movement. PASSES.

### 4.4 Execute (instant-kill canonical name) — execute-threshold semantics (1 kit)

**Delegated ruling recorded (Matt 2026-07-17 autonomous-run, veto-open).**

**Execute** = a **damage event that fires as an insta-kill when defender's HP is below a threshold fraction, otherwise resolves as normal damage.** Genre precedent: WoW execute (< 20% HP → instant-kill), D3 Killing Spree monk (execute on trash below threshold), Vampire Survivors Gorgeous Moon pentagram-evo (target-in-range-instant-kill; the kit that triggered this bucket), Hades weapon-charge finishers.

**Canonical name choice:** the corpus tag is `GAP-AILMENT:instant-kill` but the engine's ailment vocabulary discipline (ailment-layer §2.7 name shortlist rule — no ARPG owns the term as ailment identity) argues for a launder-clean name. Options:
- **`execute`** — genre-generic English verb; multiple ARPGs use "execute" descriptively; no single ARPG owns it as an ailment name. Instantly legible (threshold + kill).
- **`sever`** — evocative but LE uses it in an ailment sense.
- **`slay`** — genre-generic; possibly evokes D2 Slay perhaps too RPG-generic.

**SPEC-AUTHOR LEAN: `execute`.** Grounds: genre-generic; instantly readable; no ailment-space collision at DB corpus grain; bridges the physical-heavy-finisher pattern to the caster-execute-threshold pattern in one word.

**Roster (DB-verified, 1 kit):**

| kit_id | folk_name | game | ailment_gaps | Pattern reading |
|---|---|---|---|---|
| `vs-gorgeous-moon` | Gorgeous Moon (Pentagram evo) | vs | `["GAP-AILMENT:instant-kill", "GAP-AILMENT:instant-kill"]` (duplicate token; 1 kit) | vortex-pull + execute — target-in-range-and-below-HP instant-kill |

**Params + defaults:**

```yaml
- name: execute
  description: >
    Damage event that resolves as instant-kill when defender's HP is below
    execute_threshold_fraction; otherwise resolves as normal damage.
    Cross-checks with freeze's shatter-payoff (ailment §3) — freeze-shatter
    fires on freeze-expiry-under-threshold; execute fires on hit-under-threshold.
    NICHE-SEPARATION LAW: execute and freeze-shatter must NOT compose on the
    same target within same tick (§4.8 interaction matrix).
  is_control: none
  category: debuff  # reuses debuff (execute is a damage-event modifier, not control)
  param_ranges:
    execute_threshold_fraction:
      min: 0.05    # 5% HP — narrow niche
      max: 0.20    # 20% HP — WoW-execute-median
      default: 0.15
    boss_threshold_multiplier:
      min: 0.30
      max: 1.00
      default: 0.50   # bosses get 50% of nominal threshold — execute triggers at 7.5% default on bosses
    fizzle_damage_on_above_threshold:
      min: 1.0
      max: 1.5
      default: 1.0    # when target above threshold, hit resolves as damage × multiplier
  ai_priority: 1     # AI prioritizes execute-hit on threshold-eligible targets
```

**Application sources:** rare — execute is a payoff-mechanic, not a widespread rider. Emission surface: kit-explicit only (no SECONDARY_AILMENT_MAP entry; kits must be explicit `execute`-tagged in substrate_templates). Vs-gorgeous-moon uses a `vortex_pull + execute-in-radius` composite pattern.

**Sim consumer:** at `damage_resolver.resolve_skill`, after damage-composition but BEFORE mitigation, check: defender is `execute`-eligible AND `defender.hp / defender.max_hp < execute_threshold_fraction`. If yes, resolve as instant-kill (defender.hp = 0; damage attribution stamps `source_execute=True`). Otherwise resolve as normal damage × `fizzle_damage_on_above_threshold`.

**Placement:** BEFORE mitigation formula — execute bypasses mitigation entirely (this is what makes it an execute rather than "big damage"). Bypass includes bypassing sunder amplification (execute is a boolean fire, not a multiplier).

**Boss guardrail:** bosses have `execute_threshold_fraction × boss_threshold_multiplier` = 7.5% default HP window. Prevents boss-execute trivialization.

**Stacking / refresh:** N/A — execute is a per-hit event, not a persistent effect. No `active_effects` entry.

**Interaction matrix rows (niche-separation with freeze-shatter):**

| Composition | Interaction |
|---|---|
| execute × freeze-shatter | **NICHE-SEPARATION LAW.** Both are payoff-under-threshold mechanics with target-death outcomes. Rule: within same tick, if freeze-shatter would fire AND execute would fire on the same defender, freeze-shatter takes priority; execute suppressed for that tick (freeze-shatter is the pre-existing ailment mechanic; execute defers). Post-shatter, target either dead (both mechanisms achieved outcome) or above threshold (both moot). |
| execute × sunder | REDUNDANT — execute bypasses mitigation and multiplier composition; sunder's amplify is IGNORED on execute-fire. Above-threshold hits carry sunder normally. |
| execute × poison | INDEPENDENT — poison DoT ticks toward the threshold; execute fires when threshold crossed by ANY damage source (including DoT). |
| execute × freeze (unshattered) | FROZEN target is action-locked; execute-hit can still land during freeze; if defender crosses threshold during freeze, execute fires normally (frozen enemies are eligible for execute — genre-consistent). |
| execute × stun | INDEPENDENT — stunned targets execute-eligible. |

**DL-03 conformance:** execute is defender-side event modifier; does not tax caster movement. PASSES.

### 4.5 Deflect — defender-side (NOT ailment); routing ruling (2 kits; ESCALATION f)

**Delegated ruling recorded (Matt 2026-07-17 autonomous-run, veto-open).**

**Deflect** = a **defender-side buff class** — the "target deflects incoming projectiles / attacks" mechanic. Genre precedent: Hades Athena Divine Dash (deflect-on-move core mechanic — the defining Athena identity), Hades merciful-end (Athena+Ares duo — deflect + retaliation combo), D2 Amazon dodge/avoid/evade (defensive skills), D3 Monk Deadly Reach — Foresight (deflect-adjacent), PoE1 Kaom's Roots dodge, LE dodge-riders on Rogue.

**Roster (DB-verified, 2 kits):**

| kit_id | folk_name | game | ailment_gaps | def.bin | def.riders | Pattern reading |
|---|---|---|---|---|---|---|
| `hades1-merciful-end` | Merciful End (Ares+Athena duo) | hades1 | `["GAP-AILMENT:deflect", "GAP-AILMENT:damage-amp"]` | (n/a — Ares primary) | (deflect+damage-amp composite) | Athena's deflect + Ares' damage-amp compose as boon-duo |
| `hades1-athena-dash` | Athena Divine Dash Core | hades1 | `["GAP-AILMENT:deflect", "GAP-AILMENT:stun"]` | evade | deflect-on-move (raw_json verbs: `["dash", "deflect-on-move"]`) | Athena's Dash is deflect while dashing |

**ESCALATION f — deflect routing:**

- **(1) NEW AILMENT `deflect`.** Loops into ailment registry; defender-side buff category. Registry authoring cost; sim consumer branch on `active_effects` with `name=="deflect"`.
- **(2) def-bin RIDER `riders += "deflect"`.** Extends existing `def.riders` list (currently carries `trigger:block`, `synonym:ward`). Zero new schema surface; def-bin classification catches deflect as a defensive-mechanic-family variant.
- **(3) NEW defensive-mechanic-family.** Distinct architectural class (parallel to ailments) — but WARN: no engine-side defensive-mechanic-family exists today. Green-fielding this to serve 2 kits is over-engineering.

**SPEC-AUTHOR LEAN: (2) def-bin rider extension (`riders += "deflect"`).** Grounds:
- Deflect IS a defender-side buff, NOT a debuff or control class. Ailments are defender-side effects APPLIED BY attacker; deflect is defender-side effects INHERENT to defender. Category mismatch.
- The `def.riders` schema already carries defensive-mechanic-family variants (`trigger:block` is a block-mechanic tag; `synonym:ward` is a defensive-type tag). Adding `deflect` as a rider is the smallest lift and most semantically accurate.
- The two kits' raw_json shows deflect as a defender-side mobility+block behavior (`verbs: ["dash", "deflect-on-move"]`), which is squarely def-bin territory.
- Wave-A `def.bin` values are `{tank, mitigate, evade, absorb, glass, post-cutoff-deferred, FLAGGED}`. Deflect kits are already `def.bin=evade` (Athena Dash) or Ares-dominant (Merciful End). No new def.bin value needed — deflect is a modifier flag on existing evade/mitigate kits.

**Routing action (per ruling 2):** the 2 kits are UNBLOCKED at Wave-C without a new ailment. Emission surface: rocket adds `deflect` to `def.riders` allowed-values enum (schema-level widening); no sim consumer change beyond honoring `deflect` as a projectile-reflection check at `damage_resolver.resolve_skill` attacker-side (if defender's `def.riders` contains `deflect` AND deflect-eligible condition met — e.g., defender moving, per Athena Dash — attack resolves as `deflected` outcome: damage nullified OR partial-reflect).

**Deflect-eligible condition sub-shape (rocket enum):**

```yaml
deflect_condition:
  min: null
  max: null
  default: null
  # one of: {"on-move", "on-dash", "on-block", "always", null}
```

`hades1-athena-dash` → `deflect_condition = "on-dash"` (deflect fires while dashing).

**No new ailment registry entry.** The V9 tail's `ailment-wave-c+:deflect=2` count is a corpus-classification artifact; Wave-C routes to def-bin, not ailment. **The V9 census should be updated at V10 to reflect deflect as def-bin-mechanic, NOT ailment-blocked** — LOUD-FLAG to elrond.

**DL-03 conformance:** deflect is defender-side buff; does not tax caster movement (or defender's — deflect fires within existing movement). PASSES.

### 4.6 Unknown-ailment — OUT to elrond lane (1 kit)

**Delegated ruling recorded (Matt 2026-07-17 autonomous-run, veto-open).**

**Unknown-ailment = data gap, not engine gap.** The `GAP-AILMENT:unknown-ailment` token indicates the corpus classifier could not resolve the source-material description to a known ailment identity. Resolution path = elrond re-crawl, NOT engine spec.

**Roster (DB-verified, 1 kit):**

| kit_id | folk_name | game | ailment_gaps | Provenance note |
|---|---|---|---|---|
| `di-spiritform-druid-pvp` | Spirit-Form Druid (complaint-tier) | di | `["GAP-AILMENT:unknown-ailment"]` | one of the two originally-scoped kits per V9 §6; the other (`di-warlock-launch`) was resolved by legolas re-crawl 4abe140f pre-V9. |

**Routing action:** LOUD-FLAG to elrond substrate lane for re-crawl. Wave-C engine spec = ZERO action. Post-V10 census may flip this kit or leave it in unknown-lane depending on re-crawl outcome.

**Note to elrond (RE-CRAWL BRIEF):** DI Spirit-Form Druid PVP variant — check DI datamining sources / community wikis for what ailment this kit's Spirit-Form transformation applies. Likely candidates: chill (druid + cold), root (druid + nature), fear (spirit-form + terror aura), OR a distinct DI-specific ailment currently missing from the corpus vocabulary. Provenance tag `pvp-complaint-tier` suggests player-forum descriptions may be the source.

### 4.7 Canonical names — final picks (LOCKED at gandalf-prime DRIFT-CRITIC gate)

Following ailment-layer-engine-spec §2.7 launder-clean discipline:

| Registry name | Corpus gap-code | Ownership check | LEAN status |
|---|---|---|---|
| `blind` | `GAP-AILMENT:blind` | Genre-generic; PoE1 has a Blind ailment (~equivalent semantics — direct genre-native fit, not a name-launder issue). RDR uses same word for same concept. | LOCKED |
| `curse` | `GAP-AILMENT:curse/hex` | Genre-generic; D2 has curses (Necromancer skill family); PoE1 has curses (skill category). RDR uses same word — the mechanic IS the curse family. Not a launder issue; the term IS the mechanic. | LOCKED |
| `fear` | `GAP-AILMENT:fear` | Genre-generic; D2 Terror is fear; D4 has Fear skill. RDR uses genre-standard "fear." | LOCKED |
| `execute` | `GAP-AILMENT:instant-kill` | Genre-generic; multiple ARPGs use "execute" descriptively; no signature ownership. Chosen over `sever` (LE ailment collision) and `slay` (too generic). | LOCKED |
| — | `GAP-AILMENT:deflect` | Routes to def-bin rider (§4.5), NOT ailment registry. No canonical ailment name owed. | ROUTED (not ailment) |
| — | `GAP-AILMENT:unknown-ailment` | Elrond re-crawl lane (§4.6). No engine name owed until resolved. | ROUTED (not ailment) |

**Post-Wave-C ailment registry:** 12 (pre-Wave-C) + 4 (blind, curse, fear, execute) = **16 canonical ailments.**

### 4.8 Interaction matrix (Wave-C additions to ailment-layer §7 matrix)

Wave-C adds 4 new ailments, producing new matrix rows. Full extension:

| A × B | Composition rule |
|---|---|
| blind × sunder | ADDITIVE (independent surfaces) |
| blind × fear | ADDITIVE (attack-hit-chance + target-selection compose) |
| blind × curse:weaken | ADDITIVE-CAPPED (both reduce attacker output; cap at `1 - min(blind + weaken_magnitude, 0.80)` to prevent 100% miss) |
| blind × execute | THRESHOLD-INTERACTION (blind reduces execute-hit landing chance; if landed, threshold applies) |
| curse × sunder | ADDITIVE UNDER `max_amp_cap=0.50` LOCKED CAP (curse:amplify + sunder both contribute to defender's damage_taken_percent; sum capped at 0.50 per ailment §2.4 runaway guard) |
| curse × fear | INDEPENDENT (debuff + flee AI; no interaction) |
| curse × freeze | curse PERSISTS through freeze |
| curse × poison | ADDITIVE (curse:amplify amps poison ticks; curse:decrepify slows target's movement post-poison-tick) |
| fear × taunt | **EXCLUSIVE** (§4.3 ruling; later application clears earlier) |
| fear × root/freeze | fear SUPPRESSED during pin (§4.3 matrix) |
| execute × freeze-shatter | **NICHE-SEPARATION LAW** (§4.4 — freeze-shatter takes priority; execute suppressed same-tick) |
| execute × sunder | REDUNDANT (execute bypasses multiplier composition) |
| execute × mark-consume | INDEPENDENT — execute is a per-hit event, mark-consume is a triggered payoff; if execute-hit consumes a mark, both fire (mark-consume's consequence resolves in the tick, execute may or may not kill target — sequential resolution: mark-consume first, execute second) |

### 4.9 DR classes + boss-encounter guards

- **Blind DR:** none (blind is an accuracy-tax; low-magnitude default). No boss guard needed beyond calibration cap.
- **Curse DR:** none per-instance; total-modifier cap via `max_amp_cap=0.50` on curse:amplify. Boss guard: curse:decrepify slow-magnitude capped at 0.40 on bosses (prevents boss immobilization via curse-slow stacking).
- **Fear boss guard:** bosses IMMUNE to fear (fear does not apply to boss-tier defenders; enforced via `defender.is_boss` check at `_try_apply_ailment`). Aligns with genre pattern (bosses in D2/D4/PoE1 uniformly immune to fear).
- **Execute boss guard:** `boss_threshold_multiplier=0.50` (§4.4 params) reduces execute-eligibility window on bosses; combined with `execute_threshold_fraction=0.15` default, boss execute-window is 7.5% HP. NO absolute boss-immunity — execute IS eligible against bosses at the reduced window, matching genre precedent.

### 4.10 SECONDARY_AILMENT_MAP extensions

Extending `element_biases.py` SECONDARY_AILMENT_MAP (ailment-layer §2.5 SECONDARY_AILMENT_MAP is the extension surface):

```python
SECONDARY_AILMENT_MAP_WAVEC_ADDITIONS = {
    "shadow":     ["drain (primary — existing)", "blind", "curse"],   # blind + curse ride shadow as secondary
    "fire":       ["burn (primary — existing)", "fear"],               # fear rides fire (chr-fire-berserker precedent)
    "physical":   ["bleed (primary — existing)", "stun (existing)", "blind (via heavy_hit / explosive tag)"],  # blind rides physical via explosive
    "poison":     ["poison-dot (primary — existing)", "curse:decrepify"],  # plague-templates carry curse:decrepify secondary (chr-plague-curse-warlock precedent)
    # `execute` and `deflect` do NOT enter SECONDARY_AILMENT_MAP — both are kit-explicit only:
    #   `execute` = payoff mechanic, kit-tagged in substrate_templates
    #   `deflect` = def-bin rider, not ailment
}
```

**Emission logic:** rocket authorship extends `element_biases.py` per Wave-B §2.5 discipline (`SECONDARY_AILMENT_BIAS` map — the rocket-tuned probability per element-signature pair). NOT via a bias-map with econ-keys (Wave-B AC-2 STRIKE finding; §8 rider).

---

## §5 — Geometry small-adds: `orbit` (6 kits, 25th geometry) + `placed-lane` (3 kits, 26th geometry)

### 5.1 Orbit — new geometry_value (25th)

**Mechanic definition.** An `orbit` skill emits N sub-projectiles that orbit the caster (or an anchor point) at a fixed radius, tick-colliding with any defender within the orbit-band. Contrast: `projectile` is a straight-line motion primitive; `channel_beam` is a continuous ray; `orbit` is a persistent radial motion with tick-collision. The orbit primitive completes the caster-radius geometry family: `self_buff` (self-centered stat), `self_circle` (self-centered AoE), `orbit` (self-centered radial-motion damage).

**Roster (DB-verified, 6 kits, all `geometry_rule_fired='R8-orbit'` or `mint-dossier-fold12-2026-07-13` with `flags=['gx-candidate:orbit']`):**

| kit_id | folk_name | game | geometry_rule_fired | orbit narrative |
|---|---|---|---|---|
| `d3-inarius-bonestorm` | Inarius Bone Storm | d3 | R8-orbit | 4 bone shards orbit caster (D3 Bone Storm iconic geometry) |
| `d4-ball-lightning` | Ball Lightning Sorcerer | d4 | R8-orbit | ball projectile orbits target/anchor (D4 Sorc iconic) |
| `d4-bouldercane` | Bouldercane Druid | d4 | R8-orbit | boulder orbit around druid (D4 endgame druid) |
| `le-ring-of-shields` | Ring of Shields / Sentinel Guard | le/poe1 | mint-dossier-fold12-2026-07-13 | shields orbit caster (defensive orbit) |
| `poe1-poison-bv` | Poison Blade Vortex | poe1 | R8-orbit | blade orbit around caster (canonical PoE1 orbit) |
| `poe1-vaal-blade-vortex` | Vaal Blade Vortex | poe1 | mint-dossier-fold12-2026-07-13 | Vaal variant of Blade Vortex |

**Roster verification vs V9 tail:** V9 tail lists `geometry:orbit` at 6 kits; DB re-verify confirms 6. **No disagreement.**

**Emission rule.** `geometry_derivation.py` already has `R8-orbit` as `geometry_rule_fired`, but `geometry_value` is null on these kits (the rule identified orbit shape at derivation but no value was authored). Wave-C authors `geometry_value="orbit"` as the value, and R8-orbit becomes the rule-firing surface. Emission proceeds: rule R8-orbit fires when skill has orbit-narrative substrate (blade-vortex tags, ball-projectile-radial tags, shield-orbit tags), producing `geometry_value="orbit"`.

**Sim spatial behavior.** Orbit is a rotating N-projectile pattern:
- N sub-projectiles at angular positions θ_i = i × (2π/N), for i in [0, N-1].
- Radius r (fixed per-skill; tuning band 1.5–5.0 grid units).
- Angular velocity ω rad/s (tuning band π/2 to 4π; poison-BV canonical PoE1 is ~3π = 1.5 rotations/sec).
- Anchor: caster position (default) OR target position (for target-orbit variants — d4-ball-lightning latches to target). Anchor-mode as a sub-shape field.
- Duration: skill-controlled (persistent-while-carried for poison-BV; timed for Vaal variants; skill's duration parameter).
- Collision: per-tick, each sub-projectile checks defender-overlap within collision radius r_sub; on hit, apply damage + ailments per skill's normal damage-composition path.

**Emission fields:**

```yaml
# Rocket authors on orbit-emitted skills:
geometry_value: "orbit"
orbit_projectile_count:         # NEW
  min: 1
  max: 8
  default: 4
orbit_radius:                   # NEW (grid units)
  min: 1.5
  max: 5.0
  default: 3.0
orbit_angular_velocity:         # NEW (rad/s)
  min: 1.57                     # π/2 = 1 rotation per 4 sec (slow orbit)
  max: 12.56                    # 4π = 2 rotations per sec (fast orbit)
  default: 6.28                 # 2π = 1 rotation per sec
orbit_anchor:                   # NEW
  min: null
  max: null
  default: "caster"
  # one of: {"caster", "target", "anchor-point"}
```

### 5.2 Placed-lane — new geometry_value (26th)

**Mechanic definition.** A `placed-lane` skill emits a static lane collider (wall, barrier, line-shaped placed obstacle) at a designated position. Distinct from `projectile` (moving line), `channel_beam` (caster-anchored ray), and `zone` (radial persistent area). Placed-lane is a **line-segment static collider with duration expiry**. Genre precedent: D2 Firewall (canonical placed-lane fire), PoE1/PoE2 Frost Wall (frost-lane collider), DI Bone Wall (necromancer wall barrier).

**Roster (DB-verified, 3 kits):**

| kit_id | folk_name | game | provenance.footprint | geometry_value pre-Wave-C | Pattern reading |
|---|---|---|---|---|---|
| `d2-firewall-sorc` | Firewall Sorceress | d2 | lane | null (`R8-orbit` gandalf-override lineage but flags: `["J-GEO:placed-lane"]`) | D2 iconic firewall — persistent burn lane |
| `di-bone-wall-necro-pvp` | Bone Wall Disruption Necro | di | lane | null (`R6-placed-lane` rule_fired, flags: `["J-GEO:placed-lane"]`) | DI necromancer wall — root-carrying placed-lane |
| `le-frost-wall-rm` | Frost Wall Runemaster | le | lane | `totem` (`R0b` rule_fired, flags: `["resolved:walls-demand"]`) | LE frost wall via runemaster totem seam |

**Roster verification vs V9 tail:** V9 tail lists `geometry:walls-placed-lane` at 3 kits; DB re-verify confirms 3. **No disagreement.** Note that `le-frost-wall-rm` is currently `geometry_value="totem"` — this is a legacy R0b rule-fire that pre-dated placed-lane availability; Wave-C REVISES this kit's `geometry_value` to `"placed-lane"` (elrond re-classify at Wave-C landing).

**Emission rule.** New rule R11-placed-lane in `geometry_derivation.py`:
- FIRES when substrate has `walls_demand=true` flag OR raw_json.provenance.footprint == "lane" OR substrate templates carry wall/barrier/fissure/firewall verb tags.
- PRODUCES `geometry_value="placed-lane"`.

**Sim spatial behavior:**
- Static line-segment at (start, end) coordinates authored at cast time (start = target position, end = target position + direction_vector × length).
- Length L (tuning band 3–10 grid units).
- Width w (thin collider; ~0.5 grid units default).
- Duration D (skill-controlled; 4–15 seconds default).
- Collision: per-tick, check any defender overlap with line-segment; on overlap apply per-tick damage + ailments (this is the burn-DoT tick for firewall, chill-DoT tick for frost-wall, root-application tick for bone-wall).
- Line-of-sight: placed-lane BLOCKS projectile line-of-sight during duration (walls block projectiles). Defender melee-attack can cross wall (walls are per-projectile blockers, not physical barriers in RDR sim).

**Emission fields:**

```yaml
# Rocket authors on placed-lane-emitted skills:
geometry_value: "placed-lane"
placed_lane_length:               # NEW (grid units)
  min: 3.0
  max: 10.0
  default: 6.0
placed_lane_width:                # NEW (grid units)
  min: 0.3
  max: 1.0
  default: 0.5
placed_lane_duration:             # NEW (seconds)
  min: 4.0
  max: 15.0
  default: 8.0
placed_lane_blocks_projectiles:   # NEW (bool)
  min: null
  max: null
  default: true
```

### 5.3 Calibration guardrails (both new geometries)

- **HARD guard: `orbit_projectile_count ≤ 8`** — prevents N-projectile sim cost blowup.
- **HARD guard: `placed_lane_duration ≤ 15s`** — prevents perma-wall sim cost blowup + player-agency-collapse (walls that never expire fight AI trivializes).
- **RNG-stream discipline:** orbit angular position is DETERMINISTIC (no RNG draw at position update — angles are analytic θ_i(t) = θ_i0 + ω×t). Placed-lane position is determined at cast time from target position + direction (existing target-selection RNG; no new streams). NO new RNG streams introduced.
- **Composition with existing geometries:** orbit + burn (DoT) via poison-BV precedent works out-of-box. Placed-lane + burn (firewall), chill (frost-wall), root (bone-wall) work out-of-box. **NO SPECIAL interaction with mark-consume grammar** (§2) — a mark-consume payoff that fires "cast linked spell" can fire an orbit or placed-lane spell as the consequence normally.
- **Byte-neutrality:** absent orbit_* or placed_lane_* fields, existing kits behave identically. Emitted geometry values `"orbit"` and `"placed-lane"` are new-only; no existing kit's `geometry_value` changes (except `le-frost-wall-rm` per the roster note — but that's a corpus re-classification, not an engine field default change).

---

## §6 — TH (damage-taken-converts; 3 kits — the Wave-B §8 carve-out)

### 6.1 Delegated ruling recorded (Matt 2026-07-17 autonomous-run, veto-open)

**TH = damage-taken-converts.** A defender-side primitive: incoming damage taken by the player converts into another value — reflected damage (thorns pattern), resource fill (life-leech-style), or accumulator stack (rage-generation-on-damage). Wave-B §8 EXPLICITLY carved this out as the "3-kit real passive-reflect roster sitting in `econ:UNKNOWN`" and left it to Wave-C. Wave-C ships TH as a new active econ_bin (dropping `damage-taken-converts` from `_DEFERRED_ECON_BINS`) with sub-shape field for reflect vs fill vs stack.

Genre precedent: D2 Iron Maiden curse (reflect damage), D3 Thorns Invoker (raw thorns damage; the entire D3 build identity), D4 Thorns Barbarian (thorns build), GD Retaliation Warlord (retaliation-passive damage), PoE1 reflect maps (rare-mod defensive scaling), LE Sentinel Sentinel Guard thorns-passive.

### 6.2 Mechanic definition

Damage-taken-converts = defender-side primitive triggered on incoming damage post-mitigation. The event is `on-damage-taken` (already a Wave-B `proc_trigger_condition` value); the consequence is one of three sub-shapes:

- **reflect-damage** — incoming damage is REFLECTED to attacker at a fraction (D3 thorns: 100% of thorns-scaling as reflect; PoE1 reflect maps: fraction of received damage back to attacker).
- **resource-fill** — incoming damage FILLS a resource pool at a fraction (life-leech-analog for HP-cost kits; PoE1 leech via reservation-refill).
- **stack-fill** — incoming damage adds to an accumulator stack (D2 rage-on-damage; GD retaliation stack builder).

Reincarnated corpus attestation: the 3 kits are all reflect-damage sub-shape (thorns pattern). Sub-shape enum permits future stack-fill and resource-fill kits if data surfaces.

### 6.3 Roster (DB re-verified — Wave-B §8 correction anchor)

**Prior-run cross-check anchor honored (from re-fire note): the damage-taken-converts TH roster is exactly the 3 kits — `d3-invoker-thorns`, `d4-thorns-barb`, `gd-retaliation-warlord` — plus `chr-thorns-templar` which is PC-tagged (i.e., not TH-blocked).**

**DB re-verify:**

| kit_id | folk_name | game | econ_gaps | negative | Included in TH primitive? |
|---|---|---|---|---|---|
| `d3-invoker-thorns` | Thorns Invoker | d3 | `["UNKNOWN"]` (aura-pulse; identity is thorns-scaling) | 0 | **YES** — TH primitive kit |
| `d4-thorns-barb` | Thorns Barbarian | d4 | `["UNKNOWN"]` | 0 | **YES** — TH primitive kit |
| `gd-retaliation-warlord` | Retaliation Warlord | gd | `["UNKNOWN"]` | 0 | **YES** — TH primitive kit |
| `chr-thorns-templar` | Thorns Barrier Templar | chronicon | `["PC", "BT"]` (Wave-B PC lifted; BT this-spec) | 0 | NO — PC-tagged not TH; but LOGICALLY a thorns kit — see §6.7 |
| `gd-eor-warlord` | Eye of Reckoning Warlord | gd | (not TH-tagged; Wave-B PC kit) | 0 | NO — EoR is a channeled AoE, not thorns |
| `gd-forcewave-warlord` | Forcewave Warlord | gd | (not TH-tagged) | 0 | NO — forcewave is a projectile skill, not thorns |

**Verification:** Wave-B §8 asserted the 3-kit roster as `d3-invoker-thorns`, `d4-thorns-barb`, `gd-retaliation-warlord`. **Confirmed.** V9 tail did NOT list TH as its own bucket (it sits under the `econ:UNKNOWN=13` bucket — the corpus never classified thorns as a distinct econ shape). Wave-C's TH ships as an engine-side primitive whose roster is DERIVED from the UNKNOWN bucket via evidence-inspection, NOT from a dedicated corpus bucket. **This is the Wave-B §8 carve-out honored exactly:** count is 3, roster names match, chr-thorns-templar is PC-tagged (Wave-B lift already covered its resource concern; its `def.riders` may add `thorns:passive` at rocket authoring if the kit's thorns identity warrants — see §6.7 — but it does NOT contribute to the TH 3-kit primitive count).

**Loud-flag:** The V9 census does NOT surface `TH` as a bucket-token; the 3 kits carry `econ:UNKNOWN`. Wave-C ships the TH primitive; POST-Wave-C, elrond should RE-CLASSIFY these 3 kits from `econ:UNKNOWN` to `econ:TH` (or add a `damage-taken-converts` bucket label) for V10 census accuracy. This is a substrate-tag-alignment task, elrond lane.

### 6.4 Sub-shape choice — `conversion_target` sub-shapes

**Options:**
- **(1) One `damage-taken-converts` bin, sub_shape ∈ {reflect-damage, resource-fill, stack-fill}.** Mirrors Wave-B `charge-stack` bin lift pattern (one bin + sub_shape field for accumulator vs cycle).
- **(2) Three separate bins.** Semantic clarity; higher composer cost.

**SPEC-AUTHOR LEAN: (1) one bin + sub_shape.** Grounds:
- The three sub-shapes share the same TRIGGER event (`on-damage-taken`) and the same SIM SITE (post-mitigation branch at `damage_resolver`). Only the CONSEQUENCE differs — which is exactly what sub-shape flags model (Wave-B's `charge_stack_sub_shape` precedent).
- Current corpus roster is entirely reflect-damage sub-shape; adding two more bins for zero kits today is over-engineering.

### 6.5 Emission fields + composer bin drop

**Composer change:**

```python
# bc_target_composer.py:
_DEFERRED_ECON_BINS = frozenset({"HP-economy"})   # Wave-C DROPS `damage-taken-converts` from deferred set

_ECON_BIN_COST_TYPE_MAP["damage-taken-converts"] = ["hp"]  # the taxed pool IS the HP pool
# `hp` is a new cost_type family: the TAXED pool for TH kits is the DEFENDER'S HP.
# This is distinct from `HP-economy` (which is life-cost payment for casting cost);
# TH kits do NOT PAY hp to cast — they RECEIVE hp damage and CONVERT it.
# The `hp` cost_type here is a routing signal, not a cost payment.
```

**New emission fields (extending `resource_economy.py`):**

```yaml
damage_taken_converts_shape:      # NEW — required for TH bin kits
  min: null
  max: null
  default: null
  # one of: {"reflect-damage", "resource-fill", "stack-fill"}
reflect_damage_fraction:          # NEW — for shape=reflect-damage only
  min: 0.05
  max: 1.00                       # RUNAWAY-GUARD (LOCKED): reflect fraction ≤ 100% (no >1x reflect)
  default: 0.30                   # D3 Thorns median (30% of incoming damage back to attacker)
reflect_scaling_stat:             # NEW — which stat scales the reflect
  min: null
  max: null
  default: "thorns"
  # one of: {"thorns", "defense", "vitality"} — thorns is the D3/D4 canonical stat
conversion_source_element:        # NEW — what element the reflected damage carries
  min: null
  max: null
  default: "physical"
  # one of: {"physical", "elemental-mirror", "shadow", "holy"} — "elemental-mirror" reflects same-element as incoming
```

### 6.6 Sim consumer site

**Consumer site:** `damage_resolver.resolve_skill` incoming-hit branch, POST-mitigation but PRE-hp-application. Placement is critical:
- BEFORE mitigation would mean thorns scales off pre-mitigation damage (broken; unarmored player takes 100 damage, thorns reflects 30 back; but at defender.mitigation=50%, thorns should scale off 50 dealt-damage, not 100 pre-mitigation).
- POST-mitigation but PRE-hp-application means thorns scales off actually-dealt damage (correct — d3 thorns and d4 thorns both compute this way).

**Flow:**
1. Attacker deals damage D to defender.
2. Mitigation reduces to D' = D × (1 - mitigation).
3. **TH branch:** if defender's `resource_economy.damage_taken_converts_shape == "reflect-damage"`, compute reflect = D' × `reflect_damage_fraction`. Reflect back to attacker with `source_element=conversion_source_element`.
4. HP-application: defender.hp -= D'.

**Attribution:** reflected damage carries `source_reflect=True` in attribution telemetry; the "attacker" of the reflected damage is the ORIGINAL defender (the thorns carrier), and the "defender" is the original attacker. Extends E3 attribution spine.

### 6.7 Interaction with Wave-B PC:tick-cost (thorns aura runs concurrently)

`chr-thorns-templar` carries `PC` gap (Wave-B lifted) AND was flagged as `thorns:barrier:templar` semantically. If chr-thorns-templar's PC:tick-cost aura ALSO includes a thorns-passive component, the kit has TWO defender-side mechanics: PC aura (tick_cost + mitigation buff) + TH thorns-reflect. This is not a spec bug — it's a composite kit design. The two mechanics compose independently:

- PC:tick-cost drains resource per tick + applies stat modifiers (mitigation buff).
- TH reflects incoming damage.

Both use the same defender's `active_effects` list (PC = `name="persistent_condition"`; TH is not an active_effect — TH reads directly off `resource_economy.damage_taken_converts_shape` per §6.5, no ActiveEffect needed since damage-taken-converts is a static kit property).

**gandalf note:** chr-thorns-templar's classification is currently `econ_gaps=["PC", "BT"]`, NOT TH. If rocket authoring at Wave-C time determines the kit's thorns-identity is TH-mechanic-load-bearing, elrond should add `damage_taken_converts_shape="reflect-damage"` and `reflect_damage_fraction`. Otherwise the kit stays PC+BT-only and thorns is descriptive-flavor, not mechanical. LOUD-FLAG for elrond re-classify decision.

### 6.8 Attribution

Reflected-damage attribution:
- The reflected damage tick carries a `source_reflect=True` flag (new E3 attribution field).
- The attribution telemetry stamps `original_attacker=<attacker_id>` and `reflect_carrier=<defender_id>`.
- Test in telemetry: verify that reflected damage sums track separately from "own-dealt damage" in D3 Thorns Invoker-analog kits (verify build-crafting analysis can attribute damage source correctly).

### 6.9 Calibration guardrails

- **HARD guard: `reflect_damage_fraction ≤ 1.00`** — no >1x reflect (would create infinite-damage-loop in mirror-thorns pathological case).
- **HARD guard: reflect chain-depth = 0** — reflected damage does NOT itself trigger a defender's TH branch when it hits the attacker. Rule: `source_reflect=True` damage bypasses defender-side TH branch. This is the runaway-guard for mirror-thorns.
- **SOFT guard: `reflect_damage_fraction.default=0.30`** — tune band 0.20–0.50 per gauntlet response.
- **CC-density check:** TH-reflect + Wave-B PC:tick-cost + BT reflect (chr-thorns-templar if TH-tagged) — composite reflected damage sums must not exceed 2× incoming damage (defensive-domination check). Smoke-gate at S6.

---

## §7 — LC 3 / DR 2 placement ruling (5 kits)

### 7.1 Delegated ruling recorded (Matt 2026-07-17 autonomous-run, veto-open)

**Ruling 9 (from prior wave) parked LC+DR to Wave C with the note "LC-030 is pool-content."** This spec must rule per-kit: which 5 kits are engine-mechanics (spec here, unblocks at Wave-C) vs pool-content (defer, unblocks post-Wave-C via itemization/pool authoring). SPEC-AUTHOR LEAN summarized in §7.6.

### 7.2 Per-kit disposition table (all 5 kits)

**Roster (DB-verified, 5 kits: LC 3 + DR 2 = 5):**

| kit_id | folk_name | game | econ_gaps | economy_model | LEAN disposition | Rationale |
|---|---|---|---|---|---|---|
| `hades1-aspect-guan-yu` | Aspect of Guan Yu Spear | hades1 | `["LC"]` (partial:LC) | self-cost | **engine-mechanic** | Guan Yu spear's canonical mechanic is HP-cost casting (Cast spends HP not mana; Guan-Yu-signature Hades weapon). Engine primitive: cost payment from HP pool. `HP-economy` bin lift is scoped here. |
| `le-reaper-form-lich` | Reaper Form Lich | le | `["LC"]` (partial:LC) | self-cost | **engine-mechanic** | Reaper Form Lich transforms + pays HP as cost. Same HP-cost primitive as Guan Yu. |
| `poe2-grim-feast` | Grim Feast Overleech | poe2 | `["RS", "LC"]` (Wave-B RS lifted) | reserve | **engine-mechanic (LC portion)** | Grim Feast is overleech mechanic: leech beyond max HP into overflow pool. LC portion is the leech-cost-during-reservation. Requires HP-economy bin lift + composition with Wave-B RS. |
| `hot-norseman-frost-avalanche` | Frost Avalanche Norseman | hot | `["DR"]` | unknown | **pool-content (defer)** | Avalanche's DR (drain) is life-drain-over-time from spending HP as maintenance cost; canonically pool-content territory (avalanche's DR is the HoT-game maintenance-mechanic implemented via itemization/pool authoring, not an engine primitive). |
| `vs-queen-sigma` | Queen Sigma | vs | `["DR"]` | unknown | **pool-content (defer)** | VS Queen Sigma is a passive auto-fire-while-moving kit; the DR (drain) tag is the VS auto-fire maintenance semantics (already flagged VS-family adjacency in Wave-B §7). Pool-content = VS weapon behaviors, not an engine-side econ primitive. |

### 7.3 LC engine-mechanic path (hades1-aspect-guan-yu + le-reaper-form-lich)

**LC = life-cost (HP as maintenance-resource for casting).** These two kits pay HP to cast their signature skill. `_DEFERRED_ECON_BINS = {"HP-economy"}` was the LC-030 gate; Wave-C DROPS `HP-economy` from `_DEFERRED_ECON_BINS` for these two kits' pattern. LC engine-mechanic path:

**Composer change:**

```python
# bc_target_composer.py:
_DEFERRED_ECON_BINS = frozenset({})   # POST-Wave-C: empty (HP-economy also drops for LC kits)
# NOTE: Wave-C's TH bin lift + LC/HP-economy lift together empty _DEFERRED_ECON_BINS —
# but ONLY the 3 LC kits qualify for HP-economy binding. Emission validator rejects non-LC kits from HP-economy.
_ECON_BIN_COST_TYPE_MAP["HP-economy"] = ["hp"]  # cost_type_map: HP is the taxed pool for LC casts
```

**Emission fields (extending `resource_economy.py`):**

```yaml
hp_cost_scale:                   # NEW — for HP-economy bin kits (LC only)
  min: 0.0
  max: 0.30                      # RUNAWAY-GUARD (LOCKED): HP-cost per cast ≤ 30% max HP
  default: 0.05                  # 5% max HP per cast (Guan Yu median)
hp_cost_slope:                   # NEW — cost-slope for HP-payments (parallel to cost_slope for mana)
  min: null
  max: null
  default: "flat"
  # one of: {"flat", "escalating"}
```

**Sim consumer:** `damage_resolver.resolve_skill` cost-payment branch — if `econ_bin == "HP-economy"`, deduct `hp_cost_scale × applier.max_hp` from applier.hp (instead of the mana/focus/rage cost pool). Applier's cost pool (mana etc.) is UNTOUCHED.

**Runaway guard:** LC kits cannot cast when `applier.hp ≤ hp_cost_scale × max_hp` — refuses cast (mirrors PoE1's "insufficient life to cast" behavior). Prevents infinite-cost-descent.

### 7.4 Composite kit — poe2-grim-feast (RS + LC)

`poe2-grim-feast` has Wave-B RS (lifted) + Wave-C LC (this spec). The LC portion is grim-feast's leech-cost during reservation — a fraction of dealt damage returns to HP overflow, but the reservation ALSO taxes HP-max via a secondary reservation slot. Emission:

```yaml
# poe2-grim-feast at Wave-C landing:
econ_bin: "reservation"           # Wave-B RS is primary econ_bin (grim-feast is fundamentally reservation)
reservation_percent: 0.20         # 20% HP reserved for overflow buffer
reservation_resource: "hp"        # NEW: `hp` value permitted for reservation_resource
                                  # (extends Wave-B §3.4 reservation_resource enum which post-Wave-B is
                                  # {mana, focus, stamina-as-resource, rage, spirit}; Wave-C adds "hp")
# LC portion (overleech-into-overflow):
hp_cost_scale: 0.02               # ambient tick-cost for overflow maintenance
hp_cost_slope: "flat"
```

**Enum extension of Wave-B `reservation_resource`:** Wave-C adds `"hp"` as a valid `reservation_resource` value. Additive; no existing kit's semantics change.

### 7.5 DR pool-content (defer 2 kits — hot-norseman-frost-avalanche + vs-queen-sigma)

`DR` = drain, a life-drain-over-time mechanic. Roster is thin (2 kits), and both kits' drain semantics are already covered by their game's pool-content authoring:
- **hot-norseman-frost-avalanche** — HoT's Norseman avalanche has a maintained-channel life-drain; canonically pool-content (HoT itemization / class-authoring is the resolution surface).
- **vs-queen-sigma** — VS auto-fire-while-moving pattern; the "drain" is the auto-fire's inherent maintenance cost of the character's HP-drain-per-second attribute. Pool-content = VS gameplay behaviors, engine-side implemented via existing `mob.verbs=["auto-fire-while-moving"]` semantics.

**Defer rationale:**
- Adding a `DR` engine bin for 2 kits is over-engineering (Wave-B's 4-bin cluster addition was justified by 118 kits; 2 kits do not warrant a bin).
- Both kits' drain semantics can be expressed via existing engine surfaces post-content-authoring (pool-content lane).
- No corpus evidence supports a distinct engine-side drain-tick primitive beyond what LC's `hp_cost_scale` already covers if we treat drain as continuous small-cost-per-tick.

**Alternative disposition (Gate-1 may prefer):** DR folds into LC's `hp_cost_slope` as `escalating` OR `hp_cost_scale × cadence` as a continuous drain. If Gate-1 promotes DR to engine-mechanic path, this is the collapse — DR = LC with continuous-drain semantics rather than per-cast semantics. SPEC-AUTHOR LEAN stays "defer to pool-content" but flags this collapse as viable if Gate-1 disagrees.

### 7.6 SPEC-AUTHOR LEAN summary + net kit count

**SPEC-AUTHOR LEAN (ESCALATION g):**
- **LC = engine mechanic (3 kits: hades1-aspect-guan-yu, le-reaper-form-lich, poe2-grim-feast LC-portion).** HP-economy bin lifted; `hp_cost_scale`/`hp_cost_slope`/`reservation_resource="hp"` added.
- **DR = pool-content (defer 2 kits: hot-norseman-frost-avalanche, vs-queen-sigma).** Not spec'd here; roster-thin argument.

**Net Wave-C unblock from LC/DR: 3 kits** (LC engine-mechanic path). DR 2 kits stay blocked with the same `econ:DR` gap token (post-Wave-C census reflects: LC drops 3→0; DR stays 2).

### 7.7 Emission fields — coordination with TH (§6)

TH's `damage_taken_converts_shape` and LC's `hp_cost_scale` are DISTINCT fields — TH is about damage RECEIVED (input event on defender); LC is about cost PAID (cast payment on caster). No field re-use. But both bins share the `hp` cost_type — the `hp` value in `_ECON_BIN_COST_TYPE_MAP` is now used by BOTH TH (as taxed pool routing signal) and LC (as actual cost payment source). This is a shared vocabulary, not a shared field.

---

## §8 — AC-2 bias-map disposition (rider — DEFER)

### 8.1 Wave-B post-mortem context

Wave-B §2.5 originally authored econ-keyed bias maps (`PERSISTENT_CONDITION_BIAS` / `RESERVATION_BIAS`) in `element_biases.py` to describe element-conditional PC and RS composition rates. Gate-2 amendment 11 STRUCK these as drafter speculation:
- `element_biases.py` is an ailment/scaling module; nothing in composer consumes econ-keyed bias maps.
- Grep-zero engine consumers of econ-keyed bias maps at Wave-B time.
- Rocket correctly deferred rather than land dead code.

The maps died precisely for lack of a consumer.

### 8.2 SPEC-AUTHOR LEAN: DEFER

Wave-C is an **expressiveness wave** — new mechanics land at the emission-surface + sim-consumer levels. Element-bias is TUNING, not expressiveness. Adding element-biased composition weights during a wave that adds architecture (trigger grammar, new ailments, new geometries, TH primitive, LC bin) risks re-introducing the same "code without consumer" gap.

**Empirical criterion that would REOPEN AC-2 respec:**

The bias-map respec reopens IFF **both** conditions hold:
1. **A live composer sampling-weight consumer path exists.** Someone (rocket or gamora) authors a `bc_target_composer` sampling-weight change that WOULD read from an econ-keyed bias map. Until such consumer exists, the map's values have no impact — writing them is dead code (Discipline #13 drift-check).
2. **Corpus evidence establishes element-conditional economy at kit grain.** DB query must show that (say) fire-primary skills roll PC substantively more often than shadow-primary skills at kit grain, OR that lightning-primary skills roll RS at a distinct rate from cold-primary — with statistical significance vs random assignment. Until such evidence is DB-attested, the bias-map values are drafter speculation (Wave-B's exact anti-pattern).

Absent BOTH conditions, DEFER.

### 8.3 DRIFT-CRITIC concurrence at draft time

The re-fire brief noted: "gandalf lean: DEFER — Wave-C is an expressiveness wave; element-bias is tuning, and the maps died precisely for lack of a consumer." SPEC-AUTHOR concurs and adopts as the LEAN.

**Note to future spec-authors:** if AC-2 reopens post-empirical-criterion, the respec surface is `bc_target_composer` sampling weights (NOT `element_biases.py` — which is ailment/scaling). Any future bias-map authoring MUST cite (1) the consumer function name and (2) the corpus query establishing element-conditional economy. Wave-B's Gate-2 amendment 11 precedent stands as the invariant.

---

## §9 — Byte-neutrality theorem

**Theorem.** Absent any new Wave-C emission field, Wave-C code changes produce byte-identical outputs vs pre-Wave-C engine state on all existing seeds and all existing kits. Equivalently: the "default corner" of Wave-C behavior IS today's behavior.

### 9.1 Per-section neutrality checks

| Wave-C section | New default value | Absence-behavior | Byte-neutral? |
|---|---|---|---|
| §2 Trigger + mark-consume | `trigger_chain_shape=null`, `mark_identity=null`, `mark_apply_event=null`, `mark_consume_event=null`, `mark_duration_seconds=4.0` (unused if shape=null), `consequence_type=null` | With `trigger_chain_shape=null`, sim path never enters mark-apply/consume branches; existing Wave-B PC:proc-loop kits stay single-hop. **YES** |
| §2.3 Trigger vocabulary additions | New `proc_trigger_condition` values (`on-mark-apply`, `on-mark-consume`, `on-block-successful`, `on-ailment-application`, `on-defender-death`) | Additive to enum; existing kits keep their existing values; no forced re-emission. **YES** |
| §3 BT | `commitment_bin="persistent_trigger" + proc_trigger_condition="on-block-successful"` per kit | New emission; no default assigned to existing kits. **YES** |
| §4.1 Blind | New ailment registry entry `blind`; `_add_or_refresh` extension | New ailment; existing kits don't roll blind unless SECONDARY_AILMENT_MAP-eligible via new rocket authoring. **YES** |
| §4.2 Curse | New ailment registry entry `curse`; new variant enum | Same — existing kits don't roll curse. **YES** |
| §4.3 Fear | New ailment registry entry `fear` | Same. **YES** |
| §4.4 Execute | New ailment registry entry `execute` | Kit-explicit only; no default assignment. **YES** |
| §4.5 Deflect | `def.riders += "deflect"` schema-widen | Existing kits' `def.riders` lists unchanged; only 2 new kits (Athena Dash, Merciful End) opt-in. **YES** |
| §5.1 Orbit | New geometry_value `orbit`; new `orbit_*` fields | 6 kits opt-in; existing kits' `geometry_value` unchanged. **YES** |
| §5.2 Placed-lane | New geometry_value `placed-lane`; new `placed_lane_*` fields | 3 kits opt-in. Note: `le-frost-wall-rm` moves from `totem` → `placed-lane` (corpus RE-CLASSIFY, not engine default change). Coordinate at Wave-C landing with elrond. **YES** for engine; corpus re-classify flagged. |
| §6 TH | `damage_taken_converts_shape=null` default; new `reflect_*` fields | 3 TH kits opt-in via non-null shape; existing kits' shape stays null → skip TH branch. **YES** |
| §7 LC | `hp_cost_scale=0.0` default; `_DEFERRED_ECON_BINS` drops HP-economy | Existing kits' `hp_cost_scale=0.0` means no HP-cost payment path fires; only 3 LC kits opt-in. `_DEFERRED_ECON_BINS` drop for HP-economy has no effect on non-HP-economy kits. **YES** |
| §10 Support retirement | Config sweep + strike-plan | Section is a CONFIG-CLEANUP, not new-behavior. Behavior changes only where explicitly stated. **YES** |

**Net theorem holds:** every Wave-C addition is opt-in via non-null non-zero fields; every default = pre-Wave-C behavior.

### 9.2 RNG-stream discipline

Wave-B established discipline: any new random draw must not shift existing streams; prefer zero-RNG-draw designs; hard-drops return BEFORE rng calls. Wave-C compliance:

| Wave-C mechanic | New RNG draws? | Placement |
|---|---|---|
| Mark-apply | Uses existing ailment `_try_apply_ailment` RNG gate; no new stream | Reuses existing draw |
| Mark-consume | ZERO new RNG (mark-consume fires deterministically when consume-condition met — no chance-gate) | N/A |
| Blind apply | Reuses existing `_try_apply_ailment` gate | Reuses existing draw |
| Curse apply | Reuses existing gate | Reuses existing draw |
| Fear apply | Reuses existing gate | Reuses existing draw |
| Execute check | ZERO new RNG (deterministic threshold check) | N/A |
| Deflect check | ZERO new RNG (deterministic condition check per `deflect_condition`) | N/A |
| Orbit angular position update | ZERO new RNG (analytic θ(t) update) | N/A |
| Placed-lane cast | Reuses existing target-selection RNG | Reuses existing draw |
| TH reflect | ZERO new RNG (deterministic reflect on post-mitigation damage) | N/A |
| LC HP cost | ZERO new RNG (deterministic cost payment) | N/A |
| BT block-trigger | Reuses existing block-outcome RNG | Reuses existing draw |

**RESULT:** Wave-C introduces ZERO new RNG streams. Existing streams unshifted; existing seeds produce byte-identical existing kits post-Wave-C build (subject to the RE-CLASSIFY on le-frost-wall-rm noted §5.2 which is corpus-level, not engine-RNG-level).

**Hard-drops before RNG:** the LOCKED runaway guards (§2.5 MAX_CHAIN_DEPTH, §4.9 boss fear immunity, §6.9 reflect chain-depth=0, §7.3 HP-cost hard-drop when hp ≤ cost) all fire BEFORE any RNG gate. This preserves the Wave-B discipline: refusals happen deterministically; only qualifying attempts hit the RNG.

### 9.3 MIGRATION owed at each gen→sim seam

Per Wave-B §12 MIGRATION doc precedent, each cross-seam boundary in Wave-C requires a MIGRATION note:

| Boundary | MIGRATION owed |
|---|---|
| rocket resource_economy.py + composer → gamora spatial_engine.py | `MIGRATION-wavec-trigger-mark.md` — mark grammar consumer wire-up |
| rocket ailments.yaml → gamora damage_resolver + effect_resolver | `MIGRATION-wavec-ailments.md` — 4 new ailment consumers |
| rocket geometry_derivation.py → gamora spatial_engine.py | `MIGRATION-wavec-geometries.md` — orbit + placed-lane spatial behavior |
| rocket composer → gamora resource-branch | `MIGRATION-wavec-th-lc.md` — TH + LC + HP-economy bin lifts + reservation_resource enum-widen |
| rocket def.riders schema → gamora damage_resolver defensive branch | `MIGRATION-wavec-deflect.md` — deflect rider read at attacker-damage |

Each MIGRATION states pre-condition (Wave-B state), post-condition (Wave-C landed), and the deterministic byte-diff on regression tests.

---

## §10 — Support-retirement hygiene

### 10.1 Retirement intent (per Matt directive + Phase-2 solo-only)

The roles.yaml `sustain` role definition (line 141-142) reads:
> "Primary identity of support_healer; secondary slot for tank and water_mage. **Solo-gated in Phase-1 P1 — support role requires multi-actor context.**"

The "support" role_orientation is a legacy taxonomy value from pre-solo-only design. Post-solo-only ratification, support is:
- **Retired as a first-class role_orientation.** No new content emits with `role="support"` or `role_orientation="support"`.
- **Retained in roles.yaml `sustain`'s description as historical note.** The description references support-context; the role itself is `sustain`, not `support`.
- **Not the same as `sustain`.** `sustain` = HP recovery (self-heal, HoT). `support` = off-damage-buffing-others (buff, silence, mana-regen-for-others). The two roles are distinct; `sustain` stays engine-live for self-heal, `support` is the retired concept.

**LOUD-FLAG:** The current status is ambiguous. Multiple engine surfaces still carry `role="support"` as active string (`gear_generation.py` role_orientation maps, `output/one_realm_demo_bundle.json` role assignments, `canonical/sidecars/emit_substrate_registry.py` chain_role names). This spec proposes a bounded hygiene sweep with a strike-plan.

**If Matt's retirement intent is stronger than "solo-gated" (i.e., "retire entirely"), the strike-plan is the answer. If retirement intent is "solo-gated only" (i.e., "keep the concept for post-Phase-1 multi-actor extensions"), the sweep is docs-only, no code strike.** SPEC-AUTHOR treats this as an **ESCALATION-OPEN item**, not a locked ruling — hygiene sweep IS scoped; the retirement DEPTH is Matt-ruled.

### 10.2 Touchpoint inventory

Grep-verified touchpoints:

| Site | Touchpoint | Nature |
|---|---|---|
| `config/roles.yaml:141-142` | `sustain` description references support | Docs |
| `config/roles.yaml:156` | `utility` role description references "support effects" | Docs |
| `src/reincarnated/generation/gear_generation.py` | ~15+ role_orientation maps with `"support"` as active weight (weights range 0.05–0.80) | Code (role-orientation gear affinity weights) |
| `src/reincarnated/canonical/sidecars/emit_substrate_registry.py:184` | `chain_role` semantic label `"supporting_T3_only_chain"` | Semantic-label (not role_orientation) |
| `src/reincarnated/output/one_realm_demo_bundle.json` | Multiple `"role": "support"` + `"effect_category": "support"` entries in generated demo bundle | Generated output (regenerated each run — not source-of-truth) |

**Actual load-bearing sites:** roles.yaml (docs), gear_generation.py (code — the actual `support` weight consumer), sidecars/emit_substrate_registry.py (semantic label; different taxonomy).

**Generated output (one_realm_demo_bundle.json) will refresh automatically** once source-of-truth changes. NOT a manual sweep target.

### 10.3 Bounded config sweep plan (rocket authors; no gamora change owed)

**Sweep scope:**
1. `config/roles.yaml` line 141: strike "support_healer" reference from sustain description; replace with "self-heal identity" or similar solo-only language.
2. `config/roles.yaml` line 156: strike "or other off-damage non-healing support effects"; utility's description keeps buffs + silence + mana-regen if those are still solo-relevant self-directed utility.
3. `gear_generation.py` role_orientation maps: replace `"support": <weight>` with either (a) STRIKE the key entirely (support no longer a valid role_orientation) OR (b) rename to `"hybrid_support_flavor"` if hybrid-role kits carry support-adjacent effects (SPEC-AUTHOR LEAN: STRIKE — support is retired, and existing `hybrid` role_orientation already captures the concept).
4. `sidecars/emit_substrate_registry.py:184`: LOUD-FLAG the `supporting_T3_only_chain` naming for rocket review. This is a semantic-label for chain-role positioning ("supporting" here = position in T3 chain, not role_orientation); likely SAFE-TO-KEEP as a distinct concept but should be re-named to avoid confusion (`t3_only_chain` or `secondary_t3_chain`).

**Non-scope:**
- `output/one_realm_demo_bundle.json` — regenerated automatically; do not touch by hand.
- Any downstream telemetry / analytics touching `role="support"` — check post-strike; if any exists, MIGRATION owed. LOUD-FLAG for post-strike verification.

### 10.4 Strike-plan vs re-cast plan — SPEC-AUTHOR LEAN

**SPEC-AUTHOR LEAN: STRIKE (not re-cast).** Grounds:
- Post-solo-only ratification (2026-05-11 Phase 1 P1), the concept "support role for others" has no denominator. Re-casting to keep the concept while gating it forever is dead-code-with-explanation — worse than a clean strike.
- `hybrid` role_orientation already captures the "damage+control" and "damage+utility" cross-flavor kits that would previously have carried `support` weight.
- `sustain` role captures self-heal. `utility` role captures self-buff / non-damage-non-heal. Between `sustain`, `utility`, and `hybrid`, the "support" concept has no unique niche.

**Alternative (Gate-1 may prefer):** re-cast as "support role reserved for post-Phase-1 multi-actor extensions." Keeps the row in roles.yaml with an explicit dormant marker. Docs-only; no code change. This is the milder option.

**ESCALATION-OPEN item ruled at DRIFT-CRITIC gate:** SPEC-AUTHOR LEAN is STRIKE. If Matt overrules to re-cast, sweep collapses to docs-only.

### 10.5 What is OUT of scope

- Any downstream tool that consumes `role="support"` telemetry — verify post-strike; MIGRATION only if downstream exists.
- Sidecars/emit_substrate_registry.py `chain_role` semantic label — this is a distinct taxonomy from role_orientation; separately reviewed by rocket, not part of Wave-C strike scope.
- Retro-active edit of historical decision-log entries — git-lineage retains the concept; do not rewrite history.

---

## §11 — ESCALATIONS (contested design calls — gandalf-prime rules at DRIFT-CRITIC gate)

**Eight items. SPEC-AUTHOR LEAN stated. gandalf-prime rules ELICIT-don't-IMPOSE; Matt veto-open.**

### (a) Chain-depth cap — LOCKED at 1 vs LOCKED at 2

- **Options:** (1) LOCKED at 1 (single-hop); (2) LOCKED at 2 (nested consume-then-apply); (3) UNCAPPED.
- **Tradeoffs:** LOCKED-at-1 keeps sim consumer trivially bounded and matches all DB-attested Wave-C kits (no Wave-C kit needs depth-2). LOCKED-at-2 enables PoE1 Assassin's-Mark-triggered-cast composition edge cases (not present in Wave-C corpus). UNCAPPED = PoE1 CWDT-loop exploit precedent (never seriously proposed).
- **Genre precedent:** PoE1 patched CWDT-loop for exactly this reason; Diablo IV has depth-1 rulings on mark chains; D3 firebird's-finery patched infinite-mark-iteration.
- **SPEC-AUTHOR LEAN: (1) LOCKED at 1.** Runaway-guard cleanness + corpus fit; §2.5 has full grounds.

### (b) Trigger vocabulary — `on-mark-apply`/`on-mark-consume` distinct events vs single `on-mark` with intent flag

- **Options:** (I) distinct events; (II) single `on-mark` with `intent ∈ {apply, consume}` flag.
- **Tradeoffs:** Distinct events keep sim consumer branchless-per-event and preserve emission-surface auditability; single-with-flag reduces enum surface by 1 but conflates two behaviorally-distinct events under one dispatcher — the exact anti-pattern Wave-B's `proc_trigger_condition` design specifically avoided.
- **Genre precedent:** PoE1 mark curse system distinguishes apply-event from consume-event trigger conditions (Assassin's Mark: `apply-on-curse-cast`; consume-on-crit); D2 Iron Maiden distinguishes curse-apply from reflected-damage-fire.
- **SPEC-AUTHOR LEAN: (I) distinct events.** Preserves emission-surface auditability; matches Wave-B `proc_trigger_condition` design language.

### (c) Blind — soft_control (accuracy-tax) vs mixed_control (accuracy + brief pause)

- **Options:** (a) soft_control (accuracy-tax only); (b) mixed_control (accuracy + brief action-pause).
- **Tradeoffs:** soft_control is cleaner interaction matrix; mixed_control captures Diablo IV smoke-grenade micro-pause but reintroduces hard-CC-immunity-after-expiry composition question.
- **Genre precedent:** Corpus dominant is pure accuracy-tax (7/8 kits). The one arguable case (poe2-witchhunter-grenades flash-grenade) ALREADY carries `stun` in ailment_gaps — the pause is handled by stun, blind is the accuracy-tax rider.
- **SPEC-AUTHOR LEAN: (a) soft_control (accuracy-tax only).** Corpus fit + interaction matrix cleanness; §4.1 has full grounds.

### (d) Curse-hex vs sunder collision — new ailment vs sunder-mode-tag

- **Options:** (1) NEW ailment `curse` with variant enum {amplify, weaken, decrepify, sap}; (2) sunder-mode-tag `persistent_range` sub-shape.
- **Tradeoffs:** New ailment is architecturally cleanest (curse's variant space spans multiple effect types, NOT just damage-amp; folding into sunder collapses variant space). Sunder-mode-tag is smaller emission surface but conflates per-target-timed (sunder) with per-caster-radius (curse) which is fundamentally different sim consumer contract.
- **Genre precedent:** D2 curses (Necromancer skill family) are a distinct concept from D2 lightning shock; PoE1 curse system is separate from PoE1 shock damage-amp.
- **SPEC-AUTHOR LEAN: (1) new ailment `curse`.** Corpus fit (4 kits spanning multiple curse variants) + sim consumer contract distinction; §4.2 has full grounds.

### (e) Fear — soft_control flee AI vs hard-control lockout

- **Options:** (A) soft_control flee AI + fear/taunt exclusive-slot; (B) hard-control action-lockout (stun-clone).
- **Tradeoffs:** (A) preserves player-agency semantics and clean taunt-fear polar-opposite interaction. (B) is a stun rename that doesn't add design value and re-litigates ailment §4.5 stun DR ruling.
- **Genre precedent:** D2/D3/D4/Chronicon all model fear as flee-AI, not action-lockout.
- **SPEC-AUTHOR LEAN: (A) soft_control flee AI + fear/taunt exclusive-slot.** Genre-native + interaction-matrix clean; §4.3 has full grounds.

### (f) Deflect routing — ailment vs def-bin rider vs new defensive-mechanic-family

- **Options:** (1) NEW ailment `deflect`; (2) def-bin RIDER `riders += "deflect"`; (3) NEW defensive-mechanic-family.
- **Tradeoffs:** (1) miscategorizes deflect (defender-side buff, not applied-by-attacker debuff); (3) green-fields new architecture for 2 kits (over-engineering); (2) extends existing `def.riders` (which carries `trigger:block`, `synonym:ward` — exactly the same variant-flag pattern) at minimum lift.
- **Genre precedent:** Hades treats Athena deflect as a boon-buff on defender (mechanically defensive), not an applied debuff. D3 Monk deflect-adjacent skills same. LE dodge-riders same.
- **SPEC-AUTHOR LEAN: (2) def-bin rider extension.** Correct category + smallest lift + existing schema; §4.5 has full grounds.

### (g) LC/DR — engine mechanic vs pool-content

- **Options:** (i) All 5 kits engine-mechanic; (ii) LC 3 engine-mechanic + DR 2 pool-content; (iii) All 5 pool-content.
- **Tradeoffs:** (ii) matches roster-thin argument for DR (2 kits) + genre-canonical HP-cost binding for LC (Guan Yu spear, Reaper Form Lich — canonical HP-cost casting). (i) over-engineers a DR bin for 2 kits. (iii) leaves 3 canonical HP-cost kits blocked with no engine-side path.
- **Genre precedent:** PoE1 has HP-cost gems (Blood Magic keystone); D2 has HP-cost spells (Bone Spirit); LE has LC casters. DR mechanics are more commonly pool-content (drain-over-time is a stat, not a bin).
- **SPEC-AUTHOR LEAN: (ii) LC engine-mechanic (3 kits) + DR pool-content (defer 2 kits).** Roster-thin argument on DR + genre-canonical for LC; §7 has full grounds.

### (h) AC-2 bias-map disposition — DEFER vs respec

- **Options:** (D) DEFER with empirical criterion; (R) respec now with a composer sampling-weight consumer path.
- **Tradeoffs:** (D) preserves the Wave-B Gate-2 learning (no consumer = drafter speculation = STRIKE). (R) requires (a) a live consumer authoring AND (b) DB-attested element-conditional composition evidence — neither present at draft time. Attempting (R) without both risks re-introducing the exact Wave-B AC-2 gap.
- **Genre precedent:** This is a project-internal design-discipline call (Wave-B §2.5 STRIKE precedent), not a genre call.
- **SPEC-AUTHOR LEAN: (D) DEFER.** §8 has full grounds + empirical criterion for reopening.

**Count-check: 8 escalation items (a–h). Matches §0 TL;DR.**

---

## §12 — SEAM ROUTING (rocket vs gamora slice split + sequencing)

### 12.1 rocket slice (emission / config / enum widen; no sim change)

| Wave-C section | rocket surface changes |
|---|---|
| §2 Trigger + mark-consume | `resource_economy.py` +6 keys (trigger_chain_shape, mark_identity, mark_apply_event, mark_consume_event, mark_duration_seconds, consequence_type); `proc_trigger_condition` enum-widen (5 additions per §2.3); `substrate_templates.py` +3 templates (mark_apply_verb, mark_consume_burst, mark_of_frailty) |
| §3 BT | Zero new fields (reuses §2 fields + Wave-B AM sub-shape fields); enum-touch only |
| §4.1 Blind | `ailments.yaml` +1 entry `blind` (with params); `element_biases.py` SECONDARY_AILMENT_MAP extension (shadow → blind; physical → blind via heavy_hit/explosive) |
| §4.2 Curse | `ailments.yaml` +1 entry `curse` + `curse_variant` enum; `element_biases.py` SECONDARY_AILMENT_MAP (shadow → curse) + poison-templates rider |
| §4.3 Fear | `ailments.yaml` +1 entry `fear`; `element_biases.py` (fire → fear via chr-fire-berserker template; shadow → fear) |
| §4.4 Execute | `ailments.yaml` +1 entry `execute`; kit-explicit `substrate_templates.py` `execute_slam` + VS-adjacent templates |
| §4.5 Deflect | `def.riders` schema enum-widen +`deflect`; `deflect_condition` field enum |
| §5.1 Orbit | `geometry_derivation.py` R8-orbit rule-value binding; `geometry_value` +`orbit`; 4 new orbit_* fields on `resource_economy.py` (or a `geometry_config.py` if separated) |
| §5.2 Placed-lane | `geometry_derivation.py` +R11-placed-lane rule; `geometry_value` +`placed-lane`; 4 new placed_lane_* fields |
| §6 TH | `bc_target_composer.py` `_DEFERRED_ECON_BINS` drop `damage-taken-converts` + map entry; `resource_economy.py` +4 keys (damage_taken_converts_shape, reflect_damage_fraction, reflect_scaling_stat, conversion_source_element) |
| §7 LC | `_DEFERRED_ECON_BINS` drop `HP-economy` + `_ECON_BIN_COST_TYPE_MAP["HP-economy"] = ["hp"]`; `resource_economy.py` +2 keys (hp_cost_scale, hp_cost_slope) + `reservation_resource` enum +`hp` |
| §10 Support hygiene | `roles.yaml` doc edits; `gear_generation.py` STRIKE role_orientation `"support"` weights (per LEAN) |

**Rocket net additions: ~16-18 new emission fields + 4 new ailment entries + 2 new geometry values + 1 def.riders enum widen + composer bin changes.** Larger than Wave-B (Wave-B added ~9 fields + 2 new bins).

### 12.2 gamora slice (sim resolution + consumer sites)

| Wave-C section | gamora surface changes |
|---|---|
| §2 Trigger + mark-consume | `spatial_engine.py` per-tick loop: mark-apply consumer + mark-consume consumer + expiry check (per ailment §3.6.i shatter-hook precedent); `damage_resolver._add_or_refresh` extension for mark refresh; `effect_resolver.tick_effects` mark expiry pre-cull check |
| §3 BT | `damage_resolver.resolve_skill` block-branch: block-outcome → trigger dispatch via §2 machinery |
| §4.1 Blind | `damage_resolver.resolve_skill` attacker-side accuracy composition |
| §4.2 Curse | `damage_resolver` (per variant): amplify → damage-composition; weaken → attacker damage-out modifier; decrepify → defender movement composition; sap → defender defense composition. Range-mode curse: applier-distance validation at composition + defender-tick clear |
| §4.3 Fear | Defender AI tick: target-selection override + movement-vector override |
| §4.4 Execute | `damage_resolver.resolve_skill` pre-mitigation branch: threshold check + insta-kill outcome. Interaction with freeze-shatter niche-separation (§4.8) |
| §4.5 Deflect | `damage_resolver.resolve_skill` attacker-side: read defender `def.riders` for `deflect`; validate `deflect_condition`; resolve as deflected (nullify OR reflect per condition) |
| §5.1 Orbit | `spatial_engine.py` new orbit-motion primitive: N sub-projectiles at analytic θ_i(t) positions; per-tick collision check |
| §5.2 Placed-lane | `spatial_engine.py` new placed-lane collider: static line-segment at cast; per-tick defender-overlap check; projectile line-of-sight blocking |
| §6 TH | `damage_resolver.resolve_skill` incoming-hit branch (POST-mitigation, PRE-hp-application): reflect-damage computation + attribution stamp |
| §7 LC | `damage_resolver.resolve_skill` cost-payment branch: HP-cost deduction with hard-drop guard (hp ≤ cost → refuse cast) |

**Gamora net additions: multiple consumer sites across `damage_resolver`, `spatial_engine`, `effect_resolver`. Comparable to Wave-B (which had 4 major consumer sites). ~5-6 major consumer sites here.**

### 12.3 Sequencing dependency graph

```
[rocket:  base] resource_economy.py + composer bin lifts
    ↓
[gamora: base] damage_resolver + spatial_engine consumer wire-ups (all Wave-C sections consume from resource_economy)
    ↓
[rocket:  ailments] ailments.yaml + element_biases SECONDARY_AILMENT_MAP for 4 new ailments (§4.1–4.4)
    ↓
[gamora: ailments] blind/curse/fear/execute consumers (all read from ailments.yaml registry)
    ↓
[rocket:  geometries] R8-orbit + R11-placed-lane rules + geometry_value bindings (§5)
    ↓
[gamora: geometries] orbit motion + placed-lane collider primitives (§5)
    ↓
[gate: post-slice smoke] rocket-side emit-verify + gamora-side sim-verify
    ↓
[gate: gauntlet cert] S6 cert on trigger + mark-consume + ailments + geometries + TH + LC
    ↓
[gate: cross-seam smoke] mark grammar × ailment interaction matrix (§4.8) × runaway-guard verify
```

### 12.4 Rendezvous points (per-slice acceptance tests)

Per §12.3 order:

| Rendezvous | Test |
|---|---|
| After rocket base | `resource_economy._validate` accepts all new keys with default = null / 0.0; emission-verify: existing kits regenerate byte-identically (§9 theorem verification) |
| After gamora base | Sim smoke: existing kits produce byte-identical fight outcomes vs pre-Wave-C on 100-seed regression |
| After rocket ailments | Ailment loader accepts 4 new registry entries; ailments.yaml validates |
| After gamora ailments | Blind + curse + fear + execute apply on kit-emitted seeds; interaction matrix rows (§4.8) fire correctly |
| After rocket geometries | Orbit + placed-lane emission on 6+3 kits; geometry_value assignments correct |
| After gamora geometries | Orbit sub-projectile collision + placed-lane collider working; le-frost-wall-rm re-classified (elrond touch owed) |
| S6 gauntlet | All 42 Wave-C-flipped kits fight-cert PASS; runaway-guard verify (chain-depth ≤ 1; execute-boss-guard; fear-boss-immunity; reflect chain-depth 0) |
| Cross-seam | Mark-consume × ailment-application × execute composition test: mark-consume payoff that includes an execute-hit on frozen target correctly resolves niche-separation law |

### 12.5 S6 gauntlet cert path

Follow Wave-A/Wave-B precedent: S6 gauntlet cert required pre-Wave-C-lift-ships. Specific gauntlet tests:

- **Trigger mark grammar:** mark-apply then mark-consume within window fires consequence; mark expires without consume, no consequence.
- **BT block-trigger:** block-outcome → resource-fill / linked-cast fires per emission's `consequence_type`.
- **4 new ailments:** each ailment applies via `_try_apply_ailment`; ticks/lifecycle in `effect_resolver.tick_effects`.
- **Interaction matrix:** all 15+ interaction matrix rows (§4.8) fire per rule.
- **Runaway guards:** MAX_CHAIN_DEPTH=1 enforced; execute vs freeze-shatter niche-separation; fear-taunt exclusive; reflect chain-depth=0.
- **Byte-neutrality:** absent Wave-C fields, existing kits produce byte-identical output.

### 12.6 MIGRATION docs owed (per §9.3)

5 MIGRATION docs owed at gen→sim seams:
- `MIGRATION-wavec-trigger-mark.md` — mark grammar consumer wire-up
- `MIGRATION-wavec-ailments.md` — 4 new ailment consumers
- `MIGRATION-wavec-geometries.md` — orbit + placed-lane spatial behavior
- `MIGRATION-wavec-th-lc.md` — TH + LC + HP-economy bin lifts + reservation_resource enum-widen
- `MIGRATION-wavec-deflect.md` — deflect rider read at attacker-damage

### 12.7 Post-build census V10 delta projection

Wave-C net expressible flip: 42 kits (per §0 TL;DR gate-lift math). On V9 denominator 565:
- V9: 509/565 = 90.1%
- Post-Wave-C projection: (509 + 42) / 565 = 551/565 = **97.5%**.
- Blocked residue post-Wave-C:
  - econ:UNKNOWN 13 (elrond re-crawl lane; unchanged)
  - econ:DR 2 (Wave-C DEFER per §7 lean)
  - mechanic:shapeshift 3 (GX-02 docket open)
  - ailment-wave-c+:unknown-ailment 1 (elrond re-crawl lane)
  - dossier_owed 4 held-out (unchanged from V9 §7)
  - **Total residue: ~14 non-held-out + 4 held-out = 18 blocked kits post-Wave-C.**

**Caveat:** projection assumes zero Wave-C-multi-blocker residue (kits carrying multiple Wave-C blockers). Verify at V10 execution: is any Wave-C-scoped kit multi-blocked such that its Wave-C-flip is gated on ANOTHER Wave-C blocker landing? (Cross-inspection at V10 required.)

---

## §13 — Math notes (in-spec sketches; LOCKED invariants named)

### 13.1 Chain-depth decay math (Discipline #1)

At `MAX_CHAIN_DEPTH = 1`:
- Payoff-per-mark = `p_apply × p_consume × magnitude` (bounded linear).
- Depth-2 would produce `(p × magnitude)² + p × magnitude` — first-term is quadratic runaway.
- LOCKED-at-1 keeps first-order dominance; sim cost per-tick per-mark is O(1).

Runaway-cost analysis: at LOCKED-at-1, MAX 1 mark per identity per defender; MAX 4 identities defined; MAX defender_count active in sim. Per-tick cost = 4 × defender_count × O(1) = O(defender_count). LOCKED-at-2 would be O(defender_count) × O(depth²) — quadratic per-defender.

### 13.2 Blind accuracy-tax formula

`effective_hit_chance = base_hit_chance × (1 - accuracy_reduction_percent)`

With `accuracy_reduction_percent ∈ [0.20, 0.60]`, at max blind (0.60), a base 90% hit-chance drops to 36%. LOCKED cap `max = 0.60` (matches PoE1 blind cap; stated as invariant).

Composition with blind × curse:weaken:
`effective_hit_chance = base_hit_chance × (1 - blind_reduction) × (1 - weaken_reduction)`
Multiplicative composition. Cap: `blind + weaken ≤ 0.80` (invariant to prevent 100% miss). Enforced at emission composition.

### 13.3 Execute-threshold formula (interaction with freeze-shatter niche)

Threshold check:
`is_execute_eligible = defender.hp / defender.max_hp < execute_threshold_fraction × (defender.is_boss ? boss_threshold_multiplier : 1.0)`

Niche-separation law:
```
if same_tick_freeze_shatter_fires(defender) and is_execute_eligible(defender):
    freeze_shatter_fires  # takes priority
    execute_suppressed_for_this_tick
```

Prevents double-payoff on threshold-crossed defender. Corpus verifies at S6 gauntlet.

### 13.4 TH conversion-rate math

`reflect_damage = post_mitigation_damage × reflect_damage_fraction`

LOCKED invariants:
- `reflect_damage_fraction ≤ 1.00` (single-reflect ≤ 1x incoming; runaway-guard).
- Reflect chain-depth = 0 (reflected-damage bypasses defender-side TH branch; runaway-guard).

Sanity check: at `reflect_damage_fraction=0.30`, incoming 100 damage → 30 reflect. Attacker takes 30 damage back. This is D3 Thorns Invoker canonical baseline.

### 13.5 Orbit angular-velocity / radius params

Orbit sub-projectile angular position:
`θ_i(t) = θ_i(0) + ω × t = (i × 2π / N) + ω × (t - t_cast)`
where i ∈ [0, N-1], N = `orbit_projectile_count`, ω = `orbit_angular_velocity`.

Position:
`pos_i(t) = anchor_pos(t) + orbit_radius × (cos(θ_i(t)), sin(θ_i(t)))`

At `orbit_anchor="caster"`, `anchor_pos(t)` = caster's current position (orbit-follows-caster). At `orbit_anchor="target"`, anchor_pos = pinned target position at cast time.

LOCKED invariant: `orbit_angular_velocity ≤ 4π` (2 rotations/sec cap; prevents visual/collision aliasing at high tick rates).

### 13.6 Placed-lane duration + collider params

Placed-lane collider is a static line-segment:
`start = cast_target_pos`
`end = cast_target_pos + direction_vector × placed_lane_length`
`width = placed_lane_width`

Duration expiry:
`lane_active = (t - t_cast) < placed_lane_duration`

Per-tick collision:
`for each defender: if dist_to_line_segment(defender.pos, start, end) < (defender.radius + width/2): apply damage + ailment`

Line-of-sight blocking (if `placed_lane_blocks_projectiles = true`): projectile spawn-to-target rays intersecting the line-segment are BLOCKED (projectile stops at intersection).

LOCKED invariant: `placed_lane_duration ≤ 15s` (prevents perma-wall sim cost + agency collapse).

---

## Tracker-delta

**Canonical current-to-end-state impact:**

- `canonical/current-to-end-state/current-to-end-state-engine.md`: Wave-C IN-FLIGHT once Gate-1 PASS; adds trigger + mark-consume family + 4 new ailments + 2 new geometries + TH primitive + LC HP-economy bin lift + support-retirement hygiene sweep.
- `canonical/current-to-end-state/current-to-end-state-serial-content-emission.md`: post-Wave-C-landed, S5 corpus→engine migration for the 42 Wave-C-flipped kits reopens; queue at S5.
- `canonical/reap-die-rise-engine/wave-b-economy-engine-spec.md`: Wave-C references Wave-B §2.4 proc-loop primitive (extension), §2.6 `persistent_trigger` commitment_bin (extension hook honored), §3 reservation_resource (enum-widen +`hp` via §7), §8 damage-taken-converts TH roster (3-kit anchor honored). No Wave-B doc edit owed.
- `canonical/reap-die-rise-engine/ailment-layer-engine-spec.md`: Wave-C references §1 canonical-names discipline, §2.5 SECONDARY_AILMENT_MAP, §7 interaction matrix, §3.6.i shatter-hook expiry-check pattern. Wave-C extends §7 interaction matrix with 15+ new rows; ailment-spec §7 update owed AT-Wave-C-LANDING (post-Gate-2), not now.

**Census V10 projection:** Post-Wave-C landed = **551/565 = 97.5% expressible-now** (per §12.7). Residue: 13 econ:UNKNOWN + 2 econ:DR + 3 shapeshift + 1 unknown-ailment + 4 dossier-owed = 14 non-held-out + 4 held-out.

**decisions-log delta owed:** jack-ryan drafts at Gate-1 pass — Wave-C ruling entries for the 8 escalations (a–h) + gandalf-prime DRIFT-CRITIC gate stamp.

**Corpus re-classify LOUD-FLAGS to elrond:**
- `le-frost-wall-rm`: `geometry_value` should move from `totem` → `placed-lane` at Wave-C landing (§5.2).
- The 3 TH kits (`d3-invoker-thorns`, `d4-thorns-barb`, `gd-retaliation-warlord`): `econ:UNKNOWN` should re-classify to `econ:TH` or add `damage-taken-converts` bucket label (§6.3).
- `chr-thorns-templar`: if TH-mechanic-load-bearing, add `damage_taken_converts_shape="reflect-damage"`; otherwise stay PC+BT only (§6.7).
- `di-spiritform-druid-pvp`: elrond re-crawl for unknown-ailment resolution (§4.6 brief).
- V9 census `ailment-wave-c+:deflect=2` count is a corpus-classification artifact; deflect routes to def-bin at Wave-C (§4.5). V10 census should NOT count deflect under ailment-wave-c+.
- V9 census does NOT surface `TH` as a bucket-token; post-Wave-C V10 should add TH as a bucket (§6.3).

---

