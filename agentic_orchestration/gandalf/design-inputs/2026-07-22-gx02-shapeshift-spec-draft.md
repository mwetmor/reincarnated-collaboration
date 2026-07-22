# SHAPESHIFT (GX-02) — Engine Spec Draft

**Author:** gandalf (SPEC-AUTHOR, named sub-agent) · **Date:** 2026-07-22
**Run:** VDM-2 → Edition-next lap (`2026-07-22-vdm2-edition-next-lap`); conductor gandalf `RUN-CONDUCTOR`. This is the parallel gandalf-seam **GX-02 docket-to-spec SPEC-AUTHOR pass** (charter §4 lane b), riding after W0 returned the door-arg grammar. Its output is **engine-spec input, NOT Wave-B scope** — the shapeshift Wave-1 slice waits for it.
**Routes to (on ratification):** KR → **rocket** (generation / config / emission / T4-door surface) + **gamora** (simulation / form-state resolution / castability enforcement / calibration).
**Status:** **DRAFT for specialist build — NOT YET AUTHORIZED.** This spec awaits a **DRIFT-CRITIC pass (gandalf-prime)** + **jack-ryan Gate-1** before any build (Wave-C precedent, decisions-log 2026-07-17). It authorizes *what to build once gated*; it does not self-authorize the engine amendments flagged §7 (those escalate to KR/Matt per Gate-1 fold D, Wave-A §8 precedent).

---

## §0 — Governance header (what ruled it · what it extends · what it does NOT touch)

**What ruled it.** GX-02 forks A–F were **RULED 2026-07-22** — Matt adopted ALL PRIME-CONCURRED leans (verbatim: *"Ruling GAP-2: adopt all PRIME-CONCURRED leans A2/B3/C1+C2/D5/E5"*). Recorded at `canonical/matt_decision_needed/README.md` **Q32** row (2026-07-22) and stamped on the docket (`agentic_orchestration/gandalf/design-inputs/2026-07-16-shapeshift-gx02-docket.md`, commit `a7db4b8d`). The ruled surface:

| Fork | Ruling | Meaning for this spec |
|---|---|---|
| **A → A2** | TWO atlas families | `PERSISTENT-FORM` + `TEMPORAL-WINDOW-FORM` are distinct atlas citizens (AURA/TOTEM-SENTRY split logic). |
| **B → B3** | BOTH persistence models | Engine expresses persistent-loop AND temporal-window; each family owns one (A2 makes B3 definitional). |
| **C → C1 + C2 pair** | slot-semantics per family | `PERSISTENT-FORM` → C1 LOCKED-SUBSET; `TEMPORAL-WINDOW-FORM` → C2 REMAPPED (whole-kit swap). |
| **D → D5**, D3 Wave-1 slice | all-4 economies configurable | Cooldown-lockout (D3) ships Wave-1; spend/gauge (D1/D2) `BLOCKED: GX-19`. |
| **E → E5** | compositional commit-state | Form-ENTRY = existing WIND-UP bin; form-persistence = NEW player-state field; form-swap = WIND-UP; form-exit = `form_state_machine.py` tick (temporal only). |
| **F → F2** | auto-follows A2 | Two families = two atlas citizens (derivative of A). |
| **naming** | `shape` (2026-07-16, veto-open) | In-fight state noun is `shape`; **"form" stays EXCLUSIVELY** the ascended-lineage / Court-of-Forms concept. |

**What it extends.** The Wave-A summon/proxy spec's compositional discipline (`agentic_orchestration/gandalf/design-inputs/wave-a-engine-spec-2026-07-13.md`) — minimal-new-primitives + maximum-reuse; the §11 rocket/gamora routing template; the §9 gate-lift pattern; the S6 matchup-gate cert model. It reuses the E4 commitment machinery (`commitment_bin ∈ {snap, wind-up, channel}`, verified `skill_schema.py:222`) as the CAST layer without extending it.

**What it does NOT touch (governance boundaries — hard):**
- **`canonical/reap-die-rise-engine/wave-b-economy-engine-spec.md` is REMOTE TRUTH** (BUILT, Gate-2 PASS jack-ryan 2026-07-16, engine `b850800`). The GX-19 gauge/charge-stack economy family lives THERE. This spec's D1/D2 gauge-coupled entries **consume** that built machinery as a dependency; they do **not** re-open, re-litigate, or re-spec it.
- **The parallel Wave-B reservation/aura KR lane** (`agentic_orchestration/gandalf/design-inputs/2026-07-21-wave-b-reservation-aura-spec-draft.md`) is a **separate concurrent session's** work. This spec does **NOT** reference its namespace as a dependency, touch its file, or assume its rulings. Its RS/aura fork-space is orthogonal to shapeshift.
- **No `canonical/` writes. No `corpus.db` writes. No dispatches. No production code.** This is a design-input spec draft on disk. KR fires builds; rocket/gamora write code post-Gate.
- **Court-of-Forms / `foundation/court_persistence.py`** — the "form" noun there means an ascended-lineage record (persistent Earth-Self identity). This spec's `shape` naming (per the 2026-07-16 ruling) is precisely the disambiguation that leaves Court untouched. Zero churn on story canon.

**Framing-audit note (OP §4.1):** applied at §10 (end). This spec makes three load-bearing assumptions, each with a named refutation surface.

---

## §1 — Scope & the one-line intent

Shapeshift makes the **two form-shift families shippable in the dev-log catalogue** for veteran gamers who cognize "the shapeshifter" as a Diablo-audience class category (D2 Druid, D3 Wizard Archon, D4 Druid, LA Wildsoul, GD Berserker Wereforms). It lifts form-shift from "no incumbent engine answer" to "cooldown-slice certifiable through the S6 matchup gate," with the gauge-coupled economies staged behind GX-19.

**The design north star (Fork A → A2).** RDR ships TWO recognizable shapeshift fantasies as distinct atlas citizens, not one blurred config:
- **`PERSISTENT-FORM`** — *you ARE the beast, alternating faces.* Form is the resting state you cycle within; the rotation IS the identity (Ferality Fox↔Bear; D2 Druid). Slot-semantics = LOCKED SUBSET (half your bar is "wrong shape" at any moment — the partition is the game).
- **`TEMPORAL-WINDOW-FORM`** — *you become the beast briefly, then return.* Form is a burst super-mode you occasionally enter; downtime = base kit, uptime = burst kit (D3 Archon; GD Wereforms). Slot-semantics = REMAPPED (form entry replaces the action bar).

The engine work exists to make BOTH cells *real and balanced*. The Wave-1 slice ships the cooldown-lockout economy for both families; the gauge-coupled entry (build-to-spend, build-to-trigger) lands after GX-19 ratifies.

**Scope-comparability read (from docket §3.3):** shapeshift is Wave-A-comparable-to-larger, NOT a new order of magnitude. It adds ONE-to-TWO state machines (form-persistence field + optional `shape_state_machine.py` for temporal auto-expire) + THREE-to-FOUR economy axes (D5, cooldown shipping first) + ONE-to-TWO calibration axes (shape entry-cost band + shape uptime band). No new physics primitive — a shape is a persistent flag with skill-availability re-routing.

---

## §2 — What already EXISTS (do not rebuild)

Per the docket §3.1 read, re-verified against live engine this session. Specialists build *around* these:

| Engine surface | File (verified) | Reuse for shapeshift |
|---|---|---|
| Commitment machine — `commitment_bin ∈ {snap, wind-up, channel}` | `simulation/spatial_gauntlet/commitment_state_machine.py` + `generation/skill_schema.py:222,227` | Shape-ENTRY is a **WIND-UP** cast (existing bin); shape-SWAP is another WIND-UP cast. **Zero new commit_state work** (E5). |
| `move_policy` field (rooted / walk / full_move) on skills | `skill_schema.py` | Shape buffs re-multiply move_policy (Fox +20% MS = shape-scaled walk_pct); existing hook, DL-03-clean (§8). |
| `active_effects` list on combatant_state | `simulation/.../combatant.py` (`ActiveEffect`: name / params / duration_remaining / source_element / tick_accumulated — per wave-b Gate-1 note #9) | Shape-BUFFS (Fox +20% MS, Bear +10% DR) ride ActiveEffect; new sub-state lands in `params`, not a new `.category` field. |
| Ailment-layer refresh law (`_add_or_refresh`, DoT tick loop, hard-control enforcement) | `canonical/reap-die-rise-engine/ailment-layer-engine-spec.md` (Gate-1-passed) | Shape-BUFFS as ActiveEffect ride the SAME refresh law; shape synergy-debuffs route through the sunder-adjacent damage-amp machinery. |
| GX-19 gauge economy — `charge-stack` bin, RS reservation, cost-type map | **`canonical/reap-die-rise-engine/wave-b-economy-engine-spec.md` (REMOTE TRUTH, `b850800`)** — `bc_target_composer._ECON_BIN_COST_TYPE_MAP`, `resource_economy.py` | BUILD-TO-SPEND (D1) + BUILD-TO-TRIGGER (D2) entry economies **DEPEND ON** this built family. `BLOCKED: GX-19` until the shape-entry cost-coupling interface is specced against it (§4.D). |
| `kit_architecture.Architecture` enum — SINGLE_ELEMENT / HYBRID_2_ELEMENT / PHYSICAL_HYBRID | `generation/kit_architecture.py:49-52` (verified) | Open question (§7): a 4th enum value `shapeshift_multi_shape` OR shape is a compositional layer on top. rocket/Matt call — flagged, not pre-closed. |
| Ability grammar VERB surface | `generation/ability_grammar.py` (verified present) | Shape-entry / shape-swap / shape-exit land as 3–5 new grammar verbs (§5). |
| Wave-A proxy layer (positioned-ally spawn, proxy commit-clock) | `wave-a-engine-spec-2026-07-13.md` | Companion-summon flavor of temporal-window shapes (PBA companion spirits) can ride proxy adjacents — OPTIONAL, not Wave-1. |

---

## §3 — The two families (Fork A → A2; Fork F → F2)

Two atlas citizens. Each owns one persistence model (B3), one default slot-semantics (C1/C2), and the full D5 economy axis (cooldown shipping Wave-1).

### 3.1 `PERSISTENT-FORM`

- **Persistence (B3 / B1-shape):** shape is entered and remains until the player un-shifts or swaps to another shape. `shape_active: str | None` on the player entity; no auto-expire timer.
- **Slot-semantics (C1 LOCKED-SUBSET):** skills carry a `shape_gate` field; a skill is castable only when its gate matches `shape_active`. Neutrals (gate `None` or a shared token) cast in any shape; ultimates gate to matching shape.
- **Player-consequence:** every cast decision carries a shape-cost. The rotation IS the identity. Fantasy = *you ARE the beast, alternating faces.* **Genre anchor:** LA Wildsoul Ferality (Fox↔Bear ordered-pair rotation, "3-2-3 setup"); D2 Druid Werewolf/Werebear (persistent toggle, form-gated skills). LE Druid Werebear/Swarmblade/Spriggan is the genre's best modern realization — forms as their own skill bars with a rage/mana gauge — and is the target for the D1 gauge-coupled slice later.
- **Sub-shape the emission layer expresses as config, not a new citizen:** D4 Druid skill-driven-shift (form implicit from last cast). This is `PERSISTENT-FORM` with `entry_trigger = skill-implicit` rather than `explicit-shift-required` — a config parameter (Fork B4 folds here per the docket B-lean), NOT a third family (A3 was ruled out — over-fit on one exhibit).

### 3.2 `TEMPORAL-WINDOW-FORM`

- **Persistence (B3 / B2-shape):** shape is a timed super-mode with an entry trigger and auto-expiry. `shape_active: str | None` PLUS `shape_duration_remaining_s: float | None`; a `shape_state_machine.py` per-tick check auto-fires shape-exit at expiry (E5 / E4 sub-shape).
- **Slot-semantics (C2 REMAPPED whole-kit swap):** shape entry replaces the entire action bar with a shape-specific kit. `shape_kit_index: dict[str, list[Skill]]` on the player + kit-swap machinery in the sim's player-action-selection loop. Base skills unavailable during the window; window expiry restores the base bar.
- **Player-consequence:** the transformation is a burst window. Downtime = base kit; uptime = burst kit. Fantasy = *you become the beast briefly, then return.* **Genre anchor:** D3 Wizard Archon (20s ultimate, entire palette replaced, stat re-basing); GD Berserker Wereforms (Fangs of Asterkarn 2026-07 — cooldown-gated timed window, wereform-specific skills, **extendable-toward-permanent** per the docket ANNEX slider note); LA Shadowhunter Demonize (meter-fill → timed demon-form).
- **Sub-shape the emission layer expresses as config:** PBA COLLAPSED-SUBSET (Fork C4) — inside the window the base partition *dissolves* rather than being *replaced* (all base skills castable, no swap). This is `TEMPORAL-WINDOW-FORM` with `slot_mode = collapse` instead of `remap`. A config variant of C2, not a new citizen. (Only sensibly composes atop a kit that already partitions — i.e., a `PERSISTENT-FORM`-adjacent base; the emission layer gates it accordingly.)

### 3.3 Family-level naming (per 2026-07-16 `shape` ruling, veto-open)

The in-fight state noun is **`shape`** across the engine namespace: `shape_active`, `shape_gate`, `shape_duration_remaining_s`, `shape_kit_index`, `shape_state_machine.py`, `shape_entry` / `shape_swap` / `shape_exit` grammar verbs. Player surface reads "Bear shape" / "Fox shape." The **class fantasy may still say "shapeshift" freely** — only the STATE noun is `shape`. **"form" is reserved exclusively** for the ascended-lineage / Court-of-Forms / form-library meta-layer concept (`court_persistence.py` untouched). Working atlas-citizen labels `PERSISTENT-FORM` / `TEMPORAL-WINDOW-FORM` are the docket-3 review-sitting labels; if the citizen labels themselves should read `PERSISTENT-SHAPE` / `TEMPORAL-WINDOW-SHAPE` to hold the `shape`-noun discipline, that is a gandalf-prime + Matt call at the atlas ratification sitting (flagged §9, not closed here).

---

## §4 — Entry economy (Fork D → D5; D3 Wave-1, D1/D2 BLOCKED: GX-19)

D5 = all four economies emission-configurable, mirroring Wave-A's ALL-4 ruling. rocket owns the gen-side config surface; gamora owns the sim-side enforcement. **The axis ships now; only the D3 cooldown value-set ships now** (see §6 for the slice boundary).

| # | Economy | Engine representation | Wave-1? |
|---|---|---|---|
| **D3** | **COOLDOWN-LOCKOUT** — fixed re-entry timer | shape-entry is a skill on cooldown; reuses **existing cooldown machinery** (no new economy). shape-exit = auto-expire (temporal) or manual WIND-UP un-shift (persistent). | **✅ WAVE-1** |
| **D1** | BUILD-TO-SPEND — spend gauge to swap shapes | shape-entry/swap consumes a gauge that fills passively + accelerated by non-shape skills. **Consumes GX-19 charge-stack / resource-economy machinery** (REMOTE TRUTH). | **`BLOCKED: GX-19`** |
| **D2** | BUILD-TO-TRIGGER — fill gauge → free trigger to enter | gauge fills to full → zero-incremental-cost trigger enters shape → auto-expires (temporal-window pairing). GX-19 accumulator sub-shape. | **`BLOCKED: GX-19`** |
| **D4** | DURATION-DRAIN — shape drains a resource while active | time-in-shape consumes a bar that ticks down; pairs with D3 or D1 to add a "manage-to-extend" layer (GD extend-toward-permanent slider). | **`BLOCKED: GX-19`** (drain-bar coupling) |

**`BLOCKED: GX-19` discipline — spec the INTERFACE, not the values.** The D1/D2/D4 rows are architecturally present in the emission config surface from Wave-1 (the axis is configurable), but their **value-sets are un-authored** pending the GX-19 gauge economy's shape-entry cost-coupling interface. What Wave-1 pins is the *shape* of that interface so the config surface is forward-compatible:

- **Interface contract (rocket, forward-declared, un-valued):** a shape-entry config carries `entry_economy: str` ∈ {`cooldown`, `spend`, `trigger`, `drain`} and an `entry_economy_ref` pointer. For `cooldown` (Wave-1) the ref resolves to the existing cooldown field. For `spend`/`trigger`/`drain` the ref MUST resolve to a GX-19 economy binding — **which does not exist for shapes yet.** Wave-1 emits `entry_economy = cooldown` universally on shape kits and rejects (emission-gate) any kit that requests a non-cooldown economy, with a `BLOCKED: GX-19` deviation auto-opened (VDM-2 `kit_deviation` class `param_gap`, §5b).
- **What GX-19 must later supply (NOT specced here — a forward finding, §9):** the coupling law for "a shape-entry spends/triggers/drains a GX-19-family resource" — analogous to how Wave-A's A2 spend-economy ties re-summon to a combat-replenishing resource. This is the shape-side consumer of GX-19; it is a Wave-2 spec unit gated on GX-19's own atlas admission (ranked #2, ABOVE shapeshift at #3, on the family docket — so the ordering is natural).

**Player-consequence per economy:** D3 = "I use my transformation on cooldown"; D1 = "shape is a resource I manage"; D2 = "burst opens when the meter fills"; D4 = "shape has an internal timer I extend." Wave-1 ships the D3 feel; the gauge-tension feels (D1/D2) are the Wave-2 payoff.

---

## §5 — Commitment-grammar + T4 door expression (Fork E → E5)

### 5.a Commit-state composition (E5)

Form does NOT get its own `commit_state`. The composition (verified against `skill_schema.py:222` + docket §E engine-legibility read):

1. **Shape-ENTRY is a WIND-UP cast** — the transformation animation IS a wind-up (Ferality ordered-pair rotation is a wind-up macro; Archon's entry has a small cast_time; PBA's Z-press is a snap-shape with immediate entry — all three fit existing bins). Zero new commit_state work.
2. **Shape-PERSISTENCE is a new player-state field** — `shape_active` (both families) + `shape_duration_remaining_s` (temporal only). Genuinely new; SMALL (2 fields + serialization).
3. **Shape-SWAP is another WIND-UP cast** — Fox→Bear is a wind-up transition (persistent family).
4. **Shape-EXIT** — persistent: a WIND-UP un-shift cast OR an implicit-shift (D4 config). Temporal: an auto-fire from the `shape_state_machine.py` per-tick expiry check (E4 sub-shape).
5. **Castability check consults BOTH** `shape_active` AND `commit_state` — a targeted clause in the skill-selection loop (`spatial_engine.py` player commit_state resolution), NOT a rewrite. This mirrors Wave-A adding a proxy-side clock without polluting the player commit_state.

**Anti-leans (ruled out, do not build):** E2 (form as a 4th commit_state) semantically overloads a per-cast machine with persistent identity; E3 (form as a defender-side ActiveEffect) is a semantic mismatch (shape ≠ debuff, and `active_effects` is defender-debuff-shaped). E4-alone reinvents patterns Wave-A settled — hence E5 *composes* E4's auto-expire machine with the existing WIND-UP bin rather than rebuilding the cast layer.

### 5.b T4 door expression (W0 door-arg grammar)

The W0 wave (`agentic_orchestration/elrond/notes/2026-07-22-vdm2-ddl-v0.sql`) defines a typed T4 door grammar: a `door_registry` (door token + status + RFC ref), a `door_arg_schema` (per-arg type ∈ {enum, int, ref, bool, list, duration_s, pct} + enum_values + default_value), and a per-kit `kit_door_arg` binding (bound value + `mutation_surface` ∈ {locked, mutable} — the season lever). Shapeshift expresses as a **new T4 door** in that grammar. Proposed shape (door status `proposed`, requires a full RFC per W0 spec s2 before it becomes `active`):

**Proposed door `SHAPESHIFT_ENGINE`** — one door, two family-modes selected by an arg (mirrors how Wave-A's economies are one door-family with an economy arg):

| arg_name | arg_type | enum_values / range | default_value | mutation_surface (season default) | Notes |
|---|---|---|---|---|---|
| `family` | enum | `persistent`, `temporal_window` | `persistent` | `locked` | Fork A → A2: the two atlas citizens. Locked — a kit's family is its identity. |
| `slot_mode` | enum | `locked_subset`, `remap`, `collapse`, `skill_driven` | (derived: persistent→`locked_subset`, temporal→`remap`) | `locked` | Fork C. `collapse` = PBA C4; `skill_driven` = D4 config. |
| `entry_economy` | enum | `cooldown`, `spend`, `trigger`, `drain` | `cooldown` | `mutable` | Fork D → D5. **Only `cooldown` legal Wave-1**; the other three carry `BLOCKED: GX-19` at bind-time (emission-gate rejects + auto-dockets). `mutable` so a season can retune the economy later once GX-19 lands. |
| `entry_economy_ref` | ref | (pointer: cooldown-field id \| GX-19 economy binding id) | (cooldown-field ref) | `locked` | The resolved economy handle. Wave-1: always a cooldown-field ref. |
| `shape_count` | int | 1–3 (Wave-1 cap 2; 3 needs calibration evidence) | 2 | `locked` | Ferality Fox+Bear = 2; single-shape wereform = 1. |
| `window_duration_s` | duration_s | 0 = persistent \| >0 = temporal window length | 0 | `mutable` | 0 ⇒ persistent (no auto-expire); >0 ⇒ temporal (`shape_state_machine` auto-exit). Season-mutable (a season could shorten Archon-window). Grammar-expressible ✅. |
| `swap_cost_kind` | enum | `wind_up`, `instant`, `implicit` | `wind_up` | `locked` | Maps to the E5 commit layer: `wind_up` = WIND-UP swap cast; `implicit` = D4 skill-driven; `instant` = PBA snap. |
| `extendable` | bool | true / false | false | `mutable` | GD Fangs-of-Asterkarn slider (temporal → extendable-toward-permanent). Season-mutable — a season lever that pushes a temporal shape toward persistent. |

**Grammar-expressibility check (per brief — flag any arg the W0 grammar cannot express).** Six of eight args map cleanly onto the `door_arg_schema` type system (enum / int / duration_s / bool / ref). **Two inexpressibles + one grain-mismatch flagged to the conductor** (§9, findings — this spec does NOT edit the schema):

1. **`shape_kit_index` (the C2 whole-kit-swap payload) has NO door-arg representation.** The remap-mode's action-bar-replacement is a *per-shape skill-list structure* on the player, not a scalar/enum/ref door arg. The `door_arg_schema` types (enum/int/ref/bool/list/duration_s/pct) include `list`, but a `list` of skill-refs keyed by shape-name is a *nested map*, not a flat list. **Finding F-1:** either (a) the W0 grammar gains a `map` or `ref_list_keyed` arg_type, or (b) `shape_kit_index` lives OUTSIDE the door-arg surface as its own side-car table (`kit_shape_slot` keyed (kit_id, shape_name, skill_ordinal)) — analogous to how VDM-2 re-homed geometry as `skill_geometry_band` rather than a JSON blob. **SPEC-AUTHOR lean: (b)** — the whole-kit-swap payload is per-skill relational data, matching the VDM-2 normalized-relational correction; a door arg should stay scalar/enum/ref. This is a schema-shape decision for the conductor + elrond, not a door-grammar edit I make.
2. **`shape_gate` (the C1 per-skill castability tag) is a SKILL-schema field, not a door arg.** It rides on the Skill, not on the kit's door binding — parallel to how `commitment_bin` rides on the skill. **This is not an inexpressible so much as a placement note:** `shape_gate: str | list[str] | None` extends `skill_schema.py` (the same surface that carries `commitment_bin`), NOT `kit_door_arg`. Flagged so the conductor routes it to rocket's skill-schema surface, not the door registry.
3. **Grain note (not a blocker):** the W0 `kit_door_arg` PK is (kit_id, door_name, arg_name) — one binding per (kit, door, arg). A kit with 2 shapes that want *different* `window_duration_s` per shape (e.g., a kit where Bear-shape lasts 20s but Fox-shape is persistent) cannot express per-shape arg divergence at the kit-door grain. **Finding F-3:** most attested exhibits use a *uniform* economy/window across a kit's shapes (Ferality both-persistent; Archon single-shape), so the uniform-per-kit grain covers the corpus. If a per-shape-divergent kit is ever needed, it wants a (kit, door, shape, arg) grain — a schema extension, flagged not built. Wave-1 assumes uniform-per-kit and opens a `param_gap` deviation for any divergent kit.

**RFC gate (W0 spec s2):** `SHAPESHIFT_ENGINE` enters `door_registry` with `door_status = 'proposed'` and an `rfc_ref` pointing at THIS spec draft. It becomes `active` only after this spec clears DRIFT-CRITIC + Gate-1 (a new door requires a full RFC per W0 s2; a new arg-value later = a cheap mini-RFC). New arg-values on `entry_economy` (spend/trigger/drain) are the Wave-2 mini-RFCs gated on GX-19.

---

## §6 — Wave-1 build slice (the D3-cooldown slice ONLY — carved)

**The slice boundary, stated once, unambiguous.** Wave-1 ships **both families with the COOLDOWN economy only.** Everything gauge-coupled waits for GX-19.

### 6.1 What SHIPS in Wave-1

| Build unit | Owner | New work | Scope |
|---|---|---|---|
| `shape_active: str \| None` + `shape_duration_remaining_s: float \| None` on player entity + serialization | gamora (sim state) / rocket (emission of initial shape config) | YES | SMALL — 2 fields |
| `shape_gate: str \| list[str] \| None` on Skill schema + castability-check clause | rocket (schema field) / gamora (sim consult in skill-selection loop) | YES | SMALL — 1 field + 1 clause (mirrors `commitment_bin`) |
| `shape_state_machine.py` — temporal-window auto-expire per-tick check | gamora (sim) | YES | MEDIUM — ~100–200 LOC, parity with Wave-A's `commitment_state_machine.py` |
| `shape_kit_index` payload (C2 remap) as a side-car (`kit_shape_slot`, per F-1 lean b) | rocket (emission) / gamora (kit-swap on entry/exit) | YES | LARGE — new per-shape skill-list structure + kit-swap in player-action-selection + cooldown-carryover semantics on swap |
| `SHAPESHIFT_ENGINE` T4 door (status `proposed`) + arg schema (§5.b), **`entry_economy` restricted to `cooldown`** | rocket (emission / door binding) | YES | MEDIUM — door def + arg schema + emission binding + the non-cooldown-rejection emission-gate |
| shape-entry / shape-swap / shape-exit VERB entries in `ability_grammar.py` | rocket | YES | SMALL — 3–5 grammar verbs |
| Shape-eligibility at kit-generation (which kits carry shape-shift; element bias) | rocket (emission — `element_biases.py` + `substrate_templates.py`) | YES | MEDIUM — new emission surface |
| Shape-BUFF/DEBUFF riders as ActiveEffect (Fox +MS, Bear +DR) into `params` | gamora (reuse ailment refresh law) | NO (reuse) | SMALL — config into existing hook |
| **S6 calibration bands** — shape entry-cost band + shape uptime band | gamora | YES | MEDIUM — two bands, pass/fail rails (§6.3) |

### 6.2 What WAITS (explicitly out of Wave-1)

- **D1 BUILD-TO-SPEND, D2 BUILD-TO-TRIGGER, D4 DURATION-DRAIN economies** — `BLOCKED: GX-19`. The `entry_economy` arg exists in the config surface; only `cooldown` is a legal bound value in Wave-1; the others reject at emission with an auto-docketed `param_gap` deviation. Wave-2 spec unit (gated on GX-19 atlas admission) authors the coupling interface + values.
- **PBA collapse-mode (`slot_mode = collapse`)** and **D4 skill-driven (`slot_mode = skill_driven`)** — config variants deferrable to Wave-2; Wave-1 ships `locked_subset` (persistent) + `remap` (temporal) as the two default slot-modes. (The arg enum *includes* collapse/skill_driven from Wave-1 so the surface is forward-compatible; only the two defaults are certified.)
- **`extendable = true` slider** (GD temporal→permanent) — deferrable; Wave-1 ships `extendable = false` certified; the true-path is a Wave-2 calibration.
- **Companion-summon flavor of temporal shapes** (PBA spirit companions riding the Wave-A proxy layer) — OPTIONAL, post-Wave-1.
- **Progression composition** — does a shape carry across seasonal descent? UNRESOLVED (docket §3.2). The `shape`/`form` naming split de-collides it from Court-of-Forms, but the *mechanical* question (shape-persistence across descent boundaries) is a Wave-2+ progression question, NOT a Wave-1 blocker.

### 6.3 S6 cert expectations (the gate this slice certifies against)

Following Wave-A's C1a/C1b band model, Wave-1 certifies both families at their intended coordinates through the S6 matchup gate:

- **`PERSISTENT-FORM` cert:** the LOCKED-SUBSET rotation is *legible and balanced* — a kit with half its bar shape-gated at any moment must still clear the gauntlet at its BC cell (the partition is a design feature, not a DPS deficit to buy out). Calibration band: **shape-swap cost** (the WIND-UP cost of Fox→Bear) tuned so the rotation has felt cadence-tension without becoming a swap-tax that dominates the fight.
- **`TEMPORAL-WINDOW-FORM` cert:** the burst-window is *felt* — downtime (base kit) vs uptime (remap kit) must both clear at their band. Two documented failure modes to rail against (parallel to Wave-A's D3-evaporate / D2-dominance):
  - **window-starve:** cooldown too long / window too short → the shape never meaningfully contributes → the whole family collapses to "a cooldown skill I press occasionally." Floor the uptime.
  - **window-dominance:** window too long / cooldown too short → base kit is vestigial, the player lives in the burst form → the "return to base" fantasy evaporates. Cap the uptime ratio so the base kit stays load-bearing.
- **Certify the shape-BC cells pass the gauntlet at the correct band** before any emission-gate lift (§6.4).

### 6.4 Gate-lift sequencing (Wave-A §9 pattern)

If shape kits sit behind an emission-deferral bin (parallel to `_DEFERRED_PROXY_BINS`), lifting it is the switch that turns Wave-1 on — and it must fire AFTER the `shape_state_machine` + castability clause + S6 calibration land, else the gate opens onto uncalibrated shape cells (window-starve / window-dominance risk in live cert). rocket owns the lift; gamora signs off on calibration readiness first.

---

## §7 — Blocking vs deferrable triage + escalations

| Gap | Wave-1 status |
|---|---|
| `shape_active` / `shape_duration_remaining_s` player fields | **BLOCKING** (both families need them) |
| `shape_gate` skill field + castability clause | **BLOCKING** (C1 persistent family requires it) |
| `shape_state_machine.py` auto-expire | **BLOCKING for temporal family**; persistent family ships without it |
| `shape_kit_index` / `kit_shape_slot` side-car + kit-swap | **BLOCKING for temporal (C2 remap) family**; persistent (C1) family ships without whole-kit-swap |
| `SHAPESHIFT_ENGINE` door + arg schema (cooldown-only) | **BLOCKING** (the emission surface) |
| S6 calibration bands | **BLOCKING** (cert needs the target) |
| D1/D2/D4 gauge-coupled economies | **`BLOCKED: GX-19`** — Wave-2, gated on GX-19 admission |
| PBA collapse-mode / D4 skill-driven slot-modes | **DEFERRABLE** — config variants, Wave-2 |
| `extendable = true` slider | **DEFERRABLE** — Wave-2 calibration |
| Progression composition (shape across descent) | **DEFERRABLE** — Wave-2+ progression question |

**Escalations (DO NOT self-authorize — KR/Matt route, Wave-A §8 / Gate-1 fold D precedent):**

- **ESC-1 — `kit_architecture.Architecture` enum.** Does shape-shift need a 4th enum value (`shapeshift_multi_shape`) or does it compose as a layer on top of the existing 3 (SINGLE / HYBRID_2 / PHYSICAL_HYBRID)? The docket flagged this as a rocket/Matt call. **SPEC-AUTHOR lean: compose as a layer** (a shape kit is STILL one of the 3 architectures for its element identity; shape-shift is orthogonal to element-hybridity, exactly as the enum's own docstring says a proxy-dominant kit is still single/hybrid/physical). But rocket scopes it against the emission code; escalate before adding an enum value.
- **ESC-2 — the GX-19 shape-entry coupling interface (forward dependency).** The D1/D2/D4 value-sets need GX-19 to supply the "shape-entry spends/triggers/drains a gauge-family resource" coupling law. This is a Wave-2 spec unit; it is NOT this spec's to write, and it is NOT the parallel Wave-B reservation/aura lane's either (that lane is RS/aura, a different economy). Flag to the conductor for the GX-19 atlas-admission sequencing.

---

## §8 — DL-03 conformance check

DL-03 (streams never tax movement). Shape-BUFFS may ride `move_policy` scaling (Fox +20% MS = shape-scaled walk_pct). DL-03 is satisfied by the base engine's `move_policy` contract — shape scaling composes cleanly with the existing rooted/walk/full_move hooks and does NOT introduce a new "movement penalty while shaped" mechanic. Shape-ENTRY as a WIND-UP cast is a *cast-commitment* (the transformation animation), not a *movement stream tax* — it is exactly the kind of commitment the WIND-UP bin already models. Ailment-layer spec §2.12 pattern applied.

---

## §9 — Open items routed to the RUN-CONDUCTOR

1. **Door-grammar inexpressible F-1 — `shape_kit_index` (C2 whole-kit-swap payload).** The W0 `door_arg_schema` types cannot express a per-shape skill-list nested map as a door arg. **Lean: side-car table `kit_shape_slot` (kit_id, shape_name, skill_ordinal)** matching the VDM-2 normalized-relational correction — NOT a door-grammar edit. Conductor + elrond decide the schema home; I do not edit the DDL.
2. **Door-grammar placement note F-2 — `shape_gate`.** Rides on the Skill schema (`skill_schema.py`, alongside `commitment_bin`), NOT on `kit_door_arg`. Route to rocket's skill-schema surface. (Not an inexpressible; a placement finding.)
3. **Door-grammar grain-mismatch F-3 — per-shape arg divergence.** The (kit, door, arg) PK cannot express per-shape divergent `window_duration_s`/`entry_economy` within one kit. Corpus is uniform-per-kit so Wave-1 is covered; a divergent kit would want (kit, door, shape, arg) grain. Flagged, not built; Wave-1 auto-dockets any divergent kit as `param_gap`.
4. **ESC-1 — `Architecture` enum** (compose-as-layer lean; rocket scopes; escalate before adding an enum value).
5. **ESC-2 — GX-19 shape-entry coupling interface** (Wave-2 spec unit; forward dependency; NOT this spec, NOT the parallel Wave-B reservation/aura lane).
6. **Atlas-citizen naming** — whether `PERSISTENT-FORM`/`TEMPORAL-WINDOW-FORM` citizen labels should read `…-SHAPE` to hold the `shape`-noun discipline. gandalf-prime + Matt call at the docket-3 atlas ratification sitting; not closed here. (Consistent with the standing island-naming gate — name the atlas geography when its sitting convenes.)
7. **`shape` naming ruling is veto-open** (2026-07-16). This spec is built on it; if Matt vetoes, the namespace search-replaces `shape → <ruled noun>` — a mechanical churn, not a design change.

---

## §10 — Framing audit (OP §4.1 Q1–Q3)

**Q1 — What load-bearing assumptions does this spec make, and are they inspected?**
- (a) *The E4 commitment machine's WIND-UP bin genuinely fits shape-entry.* INSPECTED — verified `skill_schema.py:222,227` (`commitment_bin ∈ {snap, wind-up, channel}`, `str | None`); the docket §E engine-legibility read confirms all three exhibits (Ferality wind-up macro, Archon cast_time, PBA snap) fit existing bins. Refutation surface: gamora's build hits a shape-entry that fits NONE of the three bins → that is a finding, not a forced fit.
- (b) *GX-19 is a real, separable dependency for D1/D2/D4 — not already-built-for-shapes.* INSPECTED — the GX-19 economy family is BUILT (`wave-b-economy-engine-spec.md`, REMOTE TRUTH) but its *shape-entry coupling* is NOT (grep confirms no shape-side consumer). So `BLOCKED: GX-19` is honest: the primitive exists, the shape-side consumer does not. Refutation surface: if a shape-entry coupling ALREADY exists in the built economy code, ESC-2 dissolves and D1/D2 un-block — gamora/rocket confirm at build.
- (c) *`shape_kit_index` is per-skill relational data, not a scalar door arg.* INSPECTED against the VDM-2 normalized-relational correction (the whole point of the W0 diff was that flat JSON blocks re-home as side-car tables). Refutation surface: if the conductor + elrond rule the whole-kit-swap payload IS door-arg-expressible (e.g., the grammar gains a `map` type), F-1 lean (b) flips to (a).

**Q2 — Is refuting evidence surfaceable?** Yes — three designed refutation surfaces above (the WIND-UP-bin fit at build, the GX-19 shape-coupling grep at build, the door-grammar schema ruling). Plus S6 cert is the empirical gate: window-starve / window-dominance / swap-tax-dominance are the failure modes the band explicitly rails against; a shape family that cannot clear the gauntlet at its band is a finding that re-opens the economy or slot-mode ruling, not a spec to force through.

**Q3 — If a core assumption is wrong, is the move to reframe (not patch)?** Yes. If the WIND-UP bin does not fit shape-entry (Q1a fails), the move is E5-recomposition (a `shape_state_machine` entry-phase), not a commit_state overload (E2 was ruled out for exactly this reason). If GX-19 has no shape-coupling (Q1b — the expected state), the move is to STAGE (Wave-2 gated on GX-19), not to build a shadow gauge inside shapeshift. If `shape_kit_index` misfits the door grammar (Q1c), the move is a side-car table (matching VDM-2's own correction), not a JSON-blob-on-the-door hack.

---

## §11 — What this spec does NOT do

- Does NOT self-authorize any build. Awaits **DRIFT-CRITIC (gandalf-prime) + jack-ryan Gate-1** before KR fires (Wave-C precedent, decisions-log 2026-07-17).
- Does NOT write production code, `canonical/` docs, `corpus.db` rows, or dispatches.
- Does NOT edit the W0 DDL / door-arg grammar. The three door-grammar findings (F-1/F-2/F-3) are routed to the conductor as findings; the schema home is the conductor + elrond's call.
- Does NOT touch the parallel Wave-B reservation/aura lane's namespace or file.
- Does NOT re-open the BUILT `wave-b-economy-engine-spec.md` (REMOTE TRUTH) — it consumes GX-19 as a forward dependency only.
- Does NOT close the veto-open `shape` naming ruling or the atlas-citizen labels — both remain Matt's / the atlas sitting's.

---

## Signed

gandalf (SPEC-AUTHOR, named sub-agent) · 2026-07-22 · VDM-2 → Edition-next lap (`2026-07-22-vdm2-edition-next-lap`), gandalf `RUN-CONDUCTOR`. This draft awaits DRIFT-CRITIC + Gate-1 before build. Every ruling it operationalizes (A2/B3/C1+C2/D5+D3-slice/E5/F2 + `shape` naming) carries Matt's veto.
