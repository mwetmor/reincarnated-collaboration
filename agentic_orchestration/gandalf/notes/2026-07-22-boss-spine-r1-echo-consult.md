# Boss Spine · R-1 `ss_phase_transform` · E4 ECHO — Widened Design Consult

**Role:** gandalf `SPEC-AUTHOR` · **Date:** 2026-07-22
**Authority:** WIDENED DESIGN CONSULT chartered L-26, fired L-32 (Matt *"(a) - close it out and fire the consult."*)
**Charter:** `2026-07-22-boss-spine-r1-echo-consult` (conductor: gandalf RUN-CONDUCTOR, Tier-3 ledger)
**Scope:** research + spec authoring ONLY — no code. corpus.db + engine READ-ONLY.
**Engine grounded at:** `2f43045` (the frozen ablation-gate hash) · **corpus.db:** `agentic_orchestration/research/curated/corpus.db`

> **This is a design-spec-as-math.** Every claim is grounded in the real seam (`simulation/spatial_gauntlet/`),
> the sim-capacity spec §A7 (`b34a14b`), the ratified proxy-pairing law (decisions-log 2026-07-02), and the
> kit substrate (`kit_delta_t4` / `kit_mapping.mapping_json` / `skill_geometry_band`). It is NOT a build
> authorization — it is the spec a specialist (gamora simulation / rocket generation) builds against, gated by
> a critique-pair Gate-1. Forks that are genuine commitment-boundary decisions are surfaced in §5 with options +
> tradeoffs + my lean; I do NOT rule them.

---

## 0. The design law this consult inherits (the ablation outcome, folded in)

The aware-fighter ablation gate CLOSED (L-30..L-32): equal-weight geometry-awareness on a **free fighter** was
measured and REJECTED. The mechanism (gamora `af0e56ce`, 144/144 byte-reproduced) is precise and it is the
spine's founding constraint:

- BLIND ≡ nearest-first EXACTLY (0.00 m/dec detour, 0% chosen-not-nearest).
- AWARE detours 0.16–0.61 m/dec, picks a **non-nearest** target 39–59% of decisions.
- For direct-damage ranged kits the mass-AOE burst (+25 kills in one tick after positioning) **never fires** —
  the detour de-centers the player from the pack; survivors sit at ≈100% HP (coverage loss, not chip-dilution).
- **The failure is loss of COMMITMENT, realized geometrically.** A free fighter with an equal-weight vote on
  *whom to fight* oscillates and closes on nobody.

**THE DESIGN LAW (encoded structurally throughout this spec):**

> **Commitment lives in the SPINE by construction. Awareness is garnish — a flavored choice *within*
> spine-designated bounds — and NEVER a free re-target mid-commitment.**

This is not a caveat bolted on; it is the load-bearing invariant that makes the boss stack safe where the free
fighter was not. The boss spine dictates *what* skill fires and *when* (the rotation); the Reader garnish gets a
vote only on *whom/where* *inside a spine-designated window*, and the window closes the vote the instant a
commitment (a wind-up, a channel, a locked cast) begins. The exact mechanism that broke the free fighter —
mid-flight re-targeting — is **unreachable by construction** in the spine architecture. That is the whole point
of L-26's three-layer stack, and it is why the geometry reads are *rescued as garnish* even though they were
*rejected as free choice* (L-32).

**Empirical garnish-candidate #1 (banked, L-31):** the DoT dwell-spread read. Awareness reduced dwell 4.9→2.3
runs for ranged-DoT kits (+1383 intake margin), spreading ailments wider. This is the first worked example in §3.

**Genre precedent for the whole architecture.** This is not novel — it is the ARPG/action-game consensus that
the industry re-derived the hard way. Diablo II's Act bosses (Duriel, Mephisto, Diablo) run fixed attack tables
with positional target selection layered on top — the *sequence* is authored, the *aim* tracks you. Path of
Exile's Sirus and the Shaper run scripted phase choreography (beam sweeps, meteor cascades, degen ground) with
live targeting inside each scripted beat. Elder-souls design (the acknowledged reference for "learnable boss")
is *entirely* fixed movesets with reactive spacing — the player learns the rotation, reads the tell, punishes
the recovery. Last Epoch's Emperor of Corpses and the Abomination are authored phase machines. **Not one of
these gives the boss a free equal-weight vote on its own move order.** The genre proved, across 25 years, that
readable = authored sequence + reactive aim. L-26 adopts exactly that; the ablation gate just measured, in our
own substrate, the cost of the alternative.

---

## PART 1 — R-1 `ss_phase_transform` spec (mid-fight entity mutation)

### 1.1 What R-1 is, and the two consumers it must serve

§A7 (`b34a14b`) files R-1 as **CANNOT — NET-NEW MECHANISM**: a trigger hook that mutates a live entity's
behavior + skill rotation mid-fight. The line-cited blocker is real and I spec against it:
`preferred_behavior` is read once at spawn (`spatial_engine.py:5387` player-side, `entity_from_monster_dict`
mob-side) and is **immutable per entity for the fight**. Skills, `skill_geometries`, `skill_cooldowns`,
`skill_energy_costs`, `skill_rotation_priority` are all built once at spawn (`:5325–5391`). Nothing swaps them
after fight-start. `proximity_trigger` is spawn-fixed, not a transform.

**Two consumers converge on this one mechanism:**

| Consumer | What it needs | Source |
|---|---|---|
| **SHAPESHIFT verb class** (player/monster-side) | 2 of 5 Tier-3 RDR-native templates: handler-form → beast-brawl form on trigger, swapping the MICRO verb + skill-set | §A7 R-1 |
| **Boss phase-changes** | HP-threshold phase transitions in the rotation spine (opener → phase-2 loop → enrage) | L-26 layer (1) |

**Ruling I make here (one mechanism, two callers — DO NOT diverge):** these are the *same* operation —
"replace a curated subset of a live SpatialEntity's combat definition at a triggered beat." The SHAPESHIFT verb
is a monster whose transform is authored into its kit; the boss phase is a rotation-spine beat whose transform
is compiled from the boss kit's structure. Both call **one primitive: `apply_phase_transform(entity, phase_delta)`.**
Divergence would give us two mid-fight-mutation code paths to keep coherent — exactly the kind of dual-path
drift the ablation battery discipline exists to forbid. The *trigger source* differs (kit-authored proximity/HP
for a SHAPESHIFT monster; rotation-spine beat for a boss); the *mutation apply* is identical. **This mirrors the
`boss_focus_entity` precedent** (`_get_player_primary_target:1539`): a single mechanical primitive (single-entity
install by object-identity reference) serves both the win-condition boss and any future focus caller. R-1 is the
mutation analogue of that install.

### 1.2 What MAY mutate — the `PhaseDelta` (the mutation surface, bounded by substrate)

Per Discipline #41 (substrate-led, no imposed taxonomy), the mutation surface is exactly the fight-relevant
subset of the SpatialEntity combat definition that the substrate already distinguishes. A `PhaseDelta` is a
**sparse override** — every field defaults to "no change"; a transform sets only what it changes. This keeps
byte-neutrality when no transform is installed (the L-26 "one architecture, three configs" discipline).

| Mutable field | May change? | Substrate source | Rationale / bound |
|---|---|---|---|
| **skills + geometries + cooldowns + energy_costs** | **YES (primary)** | `mapping_json.skills[]`, `skill_geometry_band` | This IS the SHAPESHIFT verb-swap and the boss phase-move-set. The headline mutation. |
| **`preferred_behavior`** (mob AI mode) | **YES** | mob-side spawn field | handler-form (ranged-kite) → beast-form (melee-rush) is a `preferred_behavior` swap. The named §A7 blocker. |
| **`skill_rotation_priority`** | **YES** | spine-compiled (Part 3) | The phase's rotation table. For a boss this is the whole point — phase-2 has a different loop. |
| **stat block: `damage_modifier`, `movement_speed`, `armor_factor`, `max_hp` policy** | **CONDITIONAL** (see fork F-R1-b) | spawn stat fields | Enrage = +damage/+speed. But mutating `max_hp` mid-fight is a HP-carryover hazard (§1.4). Damage/speed: yes. HP: fork. |
| **`geometry bands` (range/width/speed)** | **YES, as a consequence** of skill-set swap | `skill_geometry_band` | Bands travel WITH the skills — a ranged→melee form-swap changes `range_band` because the *skills* changed, not as an independent axis. Do NOT expose bands as an independent mutation axis (that would let a transform change reach without changing the skill = incoherent tell). |
| **element** | **CONDITIONAL** (see fork F-R1-c) | kit element coord | A form-swap that changes element (ice-handler → fire-beast) is genre-attested (D2 form-shifters) but has ailment/resist interaction. Fork. |
| **allegiance, entity_id, object identity** | **NEVER** | — | The entity IS the same combatant across the transform (carryover §1.4 depends on this). A transform mutates *definition*, never *identity*. This is the invariant that makes `boss_focus_entity`'s object-reference alive-check survive a phase change. |

**The bound that keeps this from becoming "arbitrary mid-fight entity rewrite":** a `PhaseDelta` may only set
fields the substrate *already carries as a per-kit combat property*. It cannot invent a field. This is the
Discipline #41 guardrail made mechanical — the mutation surface is the schema, not designer imagination.

### 1.3 Trigger model — `PhaseTrigger`

A transform installs a **`PhaseTrigger`** at fight-setup (like `boss_focus_entity` is installed at setup). The
trigger is evaluated once per tick against the entity's live state; when it fires, `apply_phase_transform` runs
and the trigger is consumed (or advances to the next phase's trigger). Three trigger kinds, ordered by §A7's
stated priority ("HP-threshold at minimum; phase/aggro desirable"):

| Trigger kind | Fires when | Determinism | Consumer |
|---|---|---|---|
| **`hp_threshold`** (MINIMUM — ship first) | entity HP-fraction crosses a declared threshold (e.g. ≤0.66, ≤0.33) | Fully deterministic (HP is deterministic under fixed seed) | Boss phase-changes (the D2/PoE/souls standard); SHAPESHIFT-on-wound |
| **`rotation_beat`** | the rotation spine reaches a declared beat index (openers done, loop N complete) | Deterministic (spine is a compiled sequence, §3) | Boss scripted phases not keyed to HP (timed enrage, "after the opener") |
| **`aggro` / `proximity`** | player enters/exits a declared range band, or first-aggro | Deterministic given deterministic positions | SHAPESHIFT monsters (handler→beast when the player closes) — the genre's "it lunges when you get near" |

**Order-of-evaluation ruling (determinism-critical):** triggers evaluate in a **fixed declared order** at a
**fixed point in the tick** (after damage resolution, before target selection — so a phase that just triggered
governs the same tick's targeting). Multiple thresholds crossed in one tick (a burst drops HP 0.70→0.20 past
two thresholds): fire them **in threshold order, applying each delta in sequence** (phase-2 delta then phase-3
delta) so the entity lands in the correct terminal phase — never skip a phase's `on_enter` (§1.6). This is the
souls-genre "you can't burst past the phase-2 mechanic" made deterministic; it also prevents a legibility hole
(a phase whose tell never played).

### 1.4 State carryover rules (what survives the transform)

The transform mutates *definition* while the entity *persists*. Carryover is where boss-fight feel is won or
lost — get this wrong and the phase change feels like a cheat (D3 Malthael's "teleport + full reset" was widely
disliked; D2 Duriel's honest continuity is the model).

| State | Carryover rule | Rationale |
|---|---|---|
| **HP (absolute) / HP-fraction** | **HP ABSOLUTE carries; do NOT re-fill.** If `max_hp` is unchanged, HP-fraction is trivially preserved. | The player's progress must not be erased — this is the D3-Malthael anti-pattern. A phase change is a *new pattern on the same healthbar*, not a fresh boss. |
| **position** | **Carries exactly.** No teleport on transform (unless a skill explicitly repositions — that's a skill, not the transform). | Continuity of space is continuity of fight. Teleport-on-phase is a legibility tax (the player loses their spacing read through no error). |
| **active ailments on the entity** (freeze, burn, shock stacks) | **Carry** — an ailment is on the *combatant*, which persists. UNLESS the transform changes element and fork F-R1-c rules a resist flip (then re-evaluate stacks against new resists at transform time, do not silently drop). | An ailment mid-application shouldn't vanish because the boss changed form; that would make control builds feel robbed at exactly the high-value moment. |
| **cooldowns** | **RESET to ready on transform** for the NEW skill-set (the new skills have not been cast); **the OLD skill-set's cooldowns are discarded** (those skills no longer exist on the entity). | A form-swap arriving with all-new-skills-on-cooldown would produce a dead beat (nothing to cast) — a legibility dead-zone. Fresh skills start ready. This is also the honest read: phase-2's mechanic is *available* when phase-2 begins. |
| **energy / resource pool** | **Carries** (fraction preserved); if the new skill-set has different `energy_type`, convert by fraction, do not refill. | Resource is a combatant property; refilling on phase = free burst the player can't play around. |
| **the `boss_focus_entity` reference** (if this entity is the focus) | **Survives** — object-identity is preserved (§1.2), so the win-condition boss-focus alive-check (`:1554`) keeps pointing at the same object across the transform. | This is exactly why "never mutate identity" is an invariant. The transform is transparent to the focus machinery. |

### 1.5 Telemetry fields (SpatialFightResult / trace extension)

The ablation investigation's core lesson (gamora §0): the gate dumps captured `trace_len` as an *integer* and
lost the decision bodies, blocking mechanism diagnosis until a re-run. R-1 must not repeat that — phase
transforms are *the* thing a boss-tuning pass will need to inspect. Emit, per fight:

- **`phase_transitions`**: ordered list of `{tick, entity_id, trigger_kind, from_phase, to_phase, hp_frac_at_transition, delta_summary}`. The `delta_summary` names which fields the `PhaseDelta` changed (skills / behavior / stats / element).
- **`phase_dwell_ticks`**: ticks spent in each phase (the boss-pacing read — "phase 2 is a 40-tick slog" is a tuning signal).
- **`transition_determinism_hash`**: a hash of the transition sequence (tick + trigger + delta-id per transition). Two runs at the same seed/hash MUST produce identical `transition_determinism_hash` — this is the R-1 determinism acceptance probe (§1.7).
- Extend the existing decision-trace (`raw["decision_traces"]`, engine `run_spatial_fight` builds it under `trace_decisions=True`) so each decision record carries the **active `phase_id`** — so a target-choice trace can be read *per phase* (garnish behaves differently across phases; §3).

### 1.6 `on_enter` phase hook (the legibility beat — where the telegraph lives)

Each phase declares an **`on_enter`** effect that fires once when the transform lands: the telegraph. This is
where the LEGIBILITY GOVERNOR (Part 3) attaches to R-1 specifically. Mechanically minimal for the sim (a
declared wind-up delay + a telemetry `telegraph_fired` marker); the *rendering* is Godot's (drax/REPLICA-1), but
the **sim must model the wind-up delay** so the phase's first dangerous action is gated behind a fair,
learnable tell. Without this, a phase change is an unreactable stat spike. With it, the player learns "when the
ground cracks, phase 2 is coming" — the D2 Baal / PoE Sirus contract.

### 1.7 Determinism requirements + acceptance criteria (builder-testable)

**Determinism (HARD — this is a frozen-hash-gate mechanism per the ablation precedent):**
1. `apply_phase_transform` consumes **NO RNG**. It is a pure state replacement from a declared `PhaseDelta`.
2. Given identical (seed, engine-hash, kit, formation), the `transition_determinism_hash` is identical across runs. **Byte-reproducibility is the standard, per L-31's 144/144 precedent.**
3. **The inert corner is byte-identical to HEAD:** an entity with NO `PhaseTrigger` installed runs the exact current code path — zero phase overhead, zero telemetry rows, byte-identical to `2f43045`. (This is the non-negotiable brownfield discipline the whole reader-stack build honored: `default None → BLIND` byte-equal. R-1's `default no-trigger → no-transform` is the same law.)

**Acceptance criteria a builder tests against:**
- **AC-R1-1 (mutation happens):** a `hp_threshold` transform at 0.5 on a test entity swaps its skill-set at the tick HP crosses 0.5; post-transform casts draw from the new skills only; telemetry logs the transition.
- **AC-R1-2 (carryover correct):** HP-fraction, position, and active ailments are preserved across the transform (assert exact values pre/post); new-skill cooldowns are ready; old-skill state is gone.
- **AC-R1-3 (multi-threshold ordering):** a single-tick burst crossing two thresholds applies both deltas in threshold order and fires both `on_enter` beats (neither phase skipped).
- **AC-R1-4 (determinism):** 8-fight replay at fixed seed/hash → identical `transition_determinism_hash` (Discipline #11 byte-repro).
- **AC-R1-5 (inert byte-equality):** the full existing sim battery (the 256-fight equivalence battery is the natural instrument) runs bit-equal with the R-1 machinery present but no trigger installed. **This is the gate.**
- **AC-R1-6 (both consumers):** the SAME `apply_phase_transform` primitive drives (a) a SHAPESHIFT monster (kit-authored proximity trigger) and (b) a boss phase (rotation-beat trigger) — one code path, proven by two test fixtures.

---

## PART 2 — E4 ECHO channel spec (the STRIKER×ECHO gap)

### 2.1 What the gap is (grounded in ratified law + substrate)

E4 STRIKER×ECHO is one of the six §6 exception rows of the **ratified** proxy-pairing spec
(`canonical/reap-die-rise-engine/proxy-pairing-q6-q7-2026-07-02.md`, decisions-log 2026-07-02, Matt-ratified).
The proxy-family partition is **reverse-engineered from ratified law** — it is not taste, and I do not reopen
it. Facts:

- **ECHO** = the sui-generis one-member "**Delayed Position Shadow**" family: *player-state replay* (spec §1, row 33). The one-member family is load-bearing — any 4-family collapse folding Shadow into BATTERY makes the ratified Emitter DUAL pool illegal (decisions-log 4731).
- **STRIKER×ECHO** = the 2 "**Mirror**" pairs (Fighter+Shadow → "Mirror Blade"): *an attacker that interleaves replayed player skills* (spec §6 row 5, VALID ⚑ sim-cost E4).
- **The blocker** (decisions-log 6218, residual #1): uncertified pending the **ECHO player-skill-replay ally-attack channel** — a NET-NEW sim mechanism absent from `_spawn_one_ally`. Certifying now = "a vacuous STRIKER-only merge." **Re-entry criterion, verbatim:** "the ECHO replay channel is built — co-sequence candidate with Tier-3 W2 R-1 SHAPESHIFT." That co-sequencing is exactly this consult.

**Genre + substrate attestation (this is not invented — the substrate already carries echo channels):**
- `poe2-snipe-mirage-deadeye`: *"Mirage Deadeye clone echo (triggered on ranged attack, repeats it at 50%)"* — a delayed replay of the player's own skill at reduced magnitude. This IS the ECHO channel, verbatim from a real kit's `trigger_grammar`.
- `d4-blood-lance`: `consequence_type: "echo re-hit"` — a marked target re-hit by a delayed echo.
- `le-umbral-blades`: *"Synchronized Strike shadows mirror-discharge the same throw"* — position-shadows replaying the player's throw.
- `d2-wl-echoing-strike`: the named exemplar.

The design is genre-canonical: **PoE's Mirage Archer / Mirage Deadeye, Last Epoch's Falconer/Synchronized
shadows, D4's Paingorger echo** — a summoned/positional entity that **replays the source's skills at a scalar
of their power, on a delay.** We are building the substrate primitive for a pattern the corpus already documents
in four independent franchises.

### 2.2 What an ECHO/replay channel IS, mechanically

An **echo channel** is a mechanism by which one entity (the ECHO source — a proxy, or a boss's shadow-add)
**records a source combatant's recent skill-casts and re-emits them from the ECHO's own position, on a delay, at
a magnitude scalar.** Formally, an `EchoChannel` carries:

- **`echo_source`**: the object reference whose casts are recorded (object-identity, mirroring the `boss_focus_entity` reference pattern §1.2 — NOT a string ID). For STRIKER×ECHO the source is the *player*; for a boss-shadow-add it is the *boss*.
- **`echo_delay_ticks`**: the lag between the source's cast and the echo's re-emit (the "delayed" in Delayed Position Shadow — this is the tell, the read).
- **`echo_magnitude_scalar`**: the power fraction (`poe2-snipe-mirage-deadeye`'s "50%" is the attested anchor). Bounds: (0, 1] — an echo never exceeds its source (that would invert the fantasy — the shadow is a *reflection*, not an amplifier).
- **`echo_skill_filter`**: which of the source's skills replay. Attested variety: Mirage Deadeye replays only *ranged attacks*; some echo only the *last cast*; some replay a *fixed skill*. Substrate anchor: `delivery_class` — a filter like "projectile + beam only" is a `delivery_class` predicate (Discipline #41 — derive the filter from the substrate field, do not invent a skill taxonomy).
- **`echo_origin`**: where the replay emits FROM — the ECHO entity's own position (`skill_geometry_band.origin` = `'self'` semantics for the echo entity). This is the "Position Shadow" — the replay comes from the *shadow's* location, creating a second angle of pressure. This is the tactical point of the family: **it multiplies the player's own geometry into a second origin.**

### 2.3 Interaction with the trigger grammar

The echo channel plugs into the existing `trigger_grammar` seam — it is a **`consequence_type`**, not a new
grammar. The substrate already models this: `d4-blood-lance` has `consequence_type: "echo re-hit"`;
`poe2-snipe-mirage-deadeye` has `consequence_type: "linked-cast"` with the echo described in `mark_identity`.
The mapping:

- **`proc_trigger_condition`** = when the echo fires. For player-replay STRIKER×ECHO: `on-cast-linked` (the source casts → the echo queues a replay). This is the *most common* attested condition (499 kits carry `proc`/`trigger`; `on-cast-linked` dominates the echo exemplars).
- **`trigger_chain_shape`** = `apply-only` (the source cast APPLIES a queued echo; the echo consumes itself on re-emit — matches `poe2-snipe-mirage-deadeye`'s `apply-only`).
- **`consequence_type`** = `linked-cast` (the echo re-emits the source's skill) — the value already in the substrate.
- **The echo does NOT re-trigger itself.** An echo of a cast does not enqueue a further echo (no infinite chain). This mirrors the chain-depth cap discipline (`spatial_engine.py:460`, chains capped depth-0/1) — the same anti-runaway law the sim already enforces for chains applies to echoes: **echo depth is capped at 1.**

### 2.4 Interaction with R-1 (why they co-sequence)

The re-entry criterion co-sequences E4 with R-1 because they are **the same class of mechanism gap: a live
entity gaining a combat capability it did not spawn with.** But they are DISTINCT primitives and I keep them so:

- **R-1** *replaces* an entity's own skill-set on a trigger (mutation of self).
- **E4** *adds a channel* that re-emits ANOTHER entity's skills (a relationship between two entities).

They share the **object-reference-held-at-setup** pattern (both hold a live reference — `PhaseTrigger`'s entity,
`EchoChannel`'s `echo_source`) and both must survive the OTHER's operation: **if the boss (echo source)
phase-transforms (R-1), its echo-add's replayed skills should track the boss's NEW skill-set** (the echo reads
the source's *current* skills at re-emit time, not a snapshot at channel-creation). This is the one genuine
coupling and I spec it explicitly: **`EchoChannel` reads `echo_source.skills` live at re-emit.** A phase-2 boss
casts phase-2 skills; its shadow echoes phase-2 skills. This is both correct and dramatic — the mirror learns
the new form. (For the player-source STRIKER×ECHO case the player does not phase-transform, so this coupling is
dormant but the live-read rule is uniform — no special case.)

### 2.5 Acceptance criteria (builder-testable)

- **AC-E4-1 (replay happens):** an ECHO entity with `echo_source=player`, `delay=D`, `scalar=0.5` re-emits the player's cast from the ECHO's position D ticks later at half magnitude.
- **AC-E4-2 (filter):** an `echo_skill_filter` of `delivery_class ∈ {projectile,beam}` replays only the source's ranged casts (a melee cast produces no echo) — the Mirage-Deadeye fixture.
- **AC-E4-3 (depth cap):** an echoed cast does NOT enqueue a further echo (depth capped at 1; assert no runaway).
- **AC-E4-4 (live-source-read under R-1):** an ECHO whose source phase-transforms replays the source's POST-transform skills after the transition tick (the §2.4 coupling).
- **AC-E4-5 (E4 certification unblocks):** with the channel built, the 2 STRIKER×ECHO "Mirror" pairs certify as non-vacuous merges (the proxy-pairing residual #1 re-entry is satisfied — an attacker that genuinely interleaves replayed player skills, not a STRIKER-only stub). **This closes the ratified-law residual.**
- **AC-E4-6 (inert byte-equality):** no `EchoChannel` installed → byte-identical to HEAD (the brownfield law again).

---

## PART 3 — Kit → rotation compilation spec (the spine compiler)

### 3.1 The compiler contract

**Input:** a kit = (`kit_delta_t4.shape` + `kit_delta_t4.asserts_json`) + (`kit_mapping.mapping_json`:
`skills[]`, `t4_doors`, `trigger_grammar`, `resource_economy`, `scaffold`) + (`skill_geometry_band` rows:
`delivery_class`, `cadence_class`, `range_band`, `width_band`, `speed_band`, `count_per_cast`, `pierce`,
`chain`, `motion_signature`).

**Output:** a deterministic **`RotationSpine`** = an ordered, phase-structured choreography:
`{opener[], loop[], phase_blocks[] (keyed to R-1 PhaseTriggers), cooldown_discipline}`.

**The compiler is DETERMINISTIC and runs at GENERATION time** (per L-26: "COMPILED into choreography at
generation time … DERIVED from the corpus row"). It is NOT an in-fight decision. This is the crucial separation:
the *sequence* is fixed before the fight starts; only the *aim within a beat* is live (garnish, §3.3). This is
the D2 attack-table model — the table is authored/derived; the aim tracks.

### 3.2 Compilation rules (substrate → spine, no imposed taxonomy)

Each rule derives a spine element from substrate fields. **No skill is invented; the spine sequences the kit's
OWN skills** (Discipline #41). The kit-class distinctions the compiler needs are read from `delivery_class` ×
`cadence_class` — the substrate carries these (distribution verified: zone 93, projectile 80, melee_arc 67,
aura 64, summon_delegate+cooldown 53, motion 26 …), so the compiler never needs a hand-authored archetype label.

| Spine element | Derived from | Rule |
|---|---|---|
| **Opener** | `cadence_class`, `t4_doors` | A kit with a `cooldown` signature skill or a `RETRIBUTION_ENGINE`/`DEFENSIVE_TRADEOFF` door opens by *establishing* that state (cast the setup / raise the aura / plant the totem) before the loop. Substrate: `cadence_class ∈ {cooldown, channel}` skills open; `spam`/`builder_spender` skills are loop-body. |
| **Loop body** | `cadence_class`, `resource_economy` | The `spam` and `builder_spender` skills form the sustain loop. A `builder_spender` economy compiles to a builder→spender cadence (build to threshold, dump) — the substrate's `resource_economy` gives the ratio. This is the PoE "generate charges → discharge" rhythm, derived not guessed. |
| **Phase blocks** | `kit_delta_t4.shape`, `t4_doors`, HP thresholds | A `step`-shaped kit (130 kits) has a **threshold-crossing experience target** (schema comment: "'step' = threshold-crossing") → compile a **phase transition at that step** (an R-1 `hp_threshold` PhaseTrigger). A `ramp`-shaped kit (137 kits) escalates continuously → compile a **rising-intensity single phase** (no hard phase break, or a soft cadence-scale ramp). **This is the direct substrate→R-1 bridge: `kit_delta_t4.shape=step` IS the signal that this boss wants a phase transform.** |
| **T4 door beats** | `t4_doors` (e.g. `["DEFENSIVE_TRADEOFF","RETRIBUTION_ENGINE"]`) | Each door is a spine "signature beat" — the moment the kit's T4 identity fires. `RETRIBUTION_ENGINE` → a beat that punishes after taking damage; `DEFENSIVE_TRADEOFF` → a beat that drops defense for offense. Doors are *when the boss does its special thing* — the punish window the player learns. |
| **Cooldown discipline** | `skill_cooldowns`, `cadence_class` | The spine respects each skill's cooldown — a `cooldown`-cadence signature skill fires on its cadence, not spammed. This is what makes a boss *readable*: the big attack has a rhythm. |
| **Geometry-tell pairing** | `skill_geometry_band` (`delivery_class`, `range_band`, `speed_band`) | Each spine beat carries its skill's geometry so the LEGIBILITY GOVERNOR (§3.4) can size the telegraph to the delivery (a `slow` `beam` gets a long tell; an `instant` `melee_arc` is a close-range punish that the player must *pre-read* from position). |

**Worked micro-example (substrate-grounded).** A `step`-shaped kit with skills [aura(cadence=cooldown,
setup), projectile-volley(cadence=spam, range=long), melee_arc(cadence=cooldown, range=melee)], `t4_doors =
[RETRIBUTION_ENGINE]`:
- **Opener:** raise the aura (establish the `RETRIBUTION_ENGINE` state).
- **Loop:** projectile-volley on cadence (the sustain pressure at range).
- **Phase block @ HP≤0.5** (from `shape=step`): R-1 `hp_threshold` PhaseTrigger → `PhaseDelta` swaps loop to melee_arc-forward (`preferred_behavior` ranged→aggressive), the boss commits to the close-range punish. The `on_enter` tell fires.
- **Door beat:** on taking a burst, `RETRIBUTION_ENGINE` fires a retaliation cast (the punish window).
- **Cooldown discipline:** the melee_arc respects its cadence — a rhythm the player dodges.

This is a **derived** D2-Duriel-class fight: authored competence, compiled from what the kit *is*.

### 3.3 The GARNISH plug-point (where the Reader gets a vote — and where it does NOT)

The Reader garnish (L-26 layer 2 = the BW-1 policy seam, `choose_target` at `policy/seam.py:44`) attaches to the
spine at **exactly one kind of location: a spine beat's TARGET-SELECTION slot, within that beat's bounds.** The
spine says "cast skill S at this beat"; garnish says "at WHOM/WHERE, among the legal targets for S."

**The plug-point contract (the design law, made mechanical):**

1. **The spine owns `what` + `when`.** Which skill fires, and at which beat, is compiled (§3.2) and immutable in-fight. Garnish CANNOT change the skill or the beat.
2. **Garnish owns `whom`/`where`, ONLY inside a beat's designated selection window, ONLY for beats the compiler marks `garnish_open`.** A beat is `garnish_open` iff the skill has a *meaningful target choice* (an AOE with a placement decision; a projectile with multiple valid targets). A single-target-locked or self-cast beat is `garnish_closed` (no vote — there is nothing to choose).
3. **The window CLOSES at commitment.** The instant a beat's cast/wind-up/channel *begins*, the target is LOCKED. Garnish gets its vote *before* the commitment, never during. **This is the structural fix for the ablation failure:** the free fighter re-voted every tick and oscillated (39–59% non-nearest, detour 0.16–0.61 m/dec, mass-burst never fired). The boss garnish votes ONCE per beat, at beat-open, then commits. **Mid-commitment re-targeting is unreachable — there is no code path for it.** The `movement_intent` seam (`seam.py:106`) already models this: `move_scale` from the E4 commitment policy (rooted=0.0 suspends movement during a locked cast). The garnish inherits that commitment gate.

**Encoding the ablation law explicitly (charter requirement):**

> **`garnish_choose_target` is called AT MOST ONCE per spine beat, at beat-open, and its result is LOCKED for
> the duration of that beat's commitment. There is NO per-tick re-evaluation. The spine's beat boundary IS the
> commitment boundary. Garnish never re-targets mid-commitment because the architecture provides no seam through
> which it could.**

The BW-1 seam is reused verbatim — `choose_target(entity, alive_mobs, config, boss_focus)` — but called with a
**boss-flavored `PolicyConfig`** and called **from the spine's beat-open, not from the per-tick engine loop.**
The five geometry considerations (`exposure_incoming_threat_density`, `cluster_density`, `crossfire_overlap`,
`lane_pressure`, `escape_gradient`) are the garnish vocabulary. The config is per-kit-flavored: a ranged-DoT
boss weights the dwell-spread read (below); a melee boss weights `cluster_density` (hit the pack).

**Worked garnish example #1 — the DoT dwell-spread read (empirical, banked L-31).** The ablation's one
*positive* signal: for ranged-DoT kits, awareness reduced dwell 4.9→2.3 runs and spread ailments wider (+1383
intake margin). As garnish this becomes: **for a `garnish_open` DoT-application beat, the consideration set
down-weights targets already carrying the DoT (a "dwell-spread" consideration = negative score for
already-marked targets) so the boss's DoT-apply beat prefers a FRESH target.** Substrate hook: the mark is in
`trigger_grammar.mark_identity` / the ailment stack; the consideration reads "does candidate already carry my
mark?" and scores fresh-target-higher. This is garnish-candidate #1 realized: it flavors *whom* the DoT-apply
beat hits, WITHIN the spine's decision to fire the DoT-apply beat. It cannot make the boss abandon a cast or
change the rotation — it only picks a better target for a beat the spine already chose. **The exact behavior
that HELPED in the ablation is precisely the behavior that is safe as garnish** (target-selection within a
committed beat), and the exact behavior that HARMED (free mid-flight re-targeting) is architecturally excluded.

**Why this is the whole thesis.** The ablation proved geometry-awareness is worth *negative* value when it can
break commitment, and *positive* value (the DoT case) when it only refines target choice. The spine architecture
*keeps the positive and forbids the negative by construction*. That is not a compromise — it is the correct
reading of the evidence.

### 3.4 The LEGIBILITY GOVERNOR (L-26 layer 3 — the boss is built to lose fairly)

The governor caps how much the boss "sees" and gates its actions behind fair tells, so bosses stay *learnable*
(the anti-D4-Torment-HP-multiplier design direction, L-26). Parameters:

| Governor parameter | What it caps | Default / lean | Rationale |
|---|---|---|---|
| **`read_rate_hz`** | how often garnish may re-evaluate an OPEN beat's target (NOT within a commitment — between beats) | tier-scaled: low tiers re-read slowly, pinnacle tiers re-read faster | This is the **awareness-as-difficulty-dial** (L-26): a harder boss *reads more often* → tracks the player better. The ablation instrument PRICES this dial (that was its surviving purpose). Low `read_rate_hz` = the boss's aim lags = the player can juke it. |
| **`telegraph_ticks`** (per beat, from geometry) | the wind-up delay before a beat's damage lands | sized from `skill_geometry_band.speed_band`: `slow`→long, `instant`→short-but-pre-readable | The tell. A `slow beam` telegraphs long (PoE Sirus die-beam); an `instant melee_arc` has a short tell but a *positional* pre-read (souls "it will lunge if I'm in range"). |
| **`recovery_ticks`** (per beat) | the punish window after a beat where the boss is committed/vulnerable | sized from `cadence_class` (`cooldown` beats have long recovery) | The player's reward for reading correctly. No recovery window = no counterplay = unfair. This is the souls-genre core. |
| **`max_concurrent_commitments`** | how many committed beats overlap | 1 for low tiers, up to a small cap for pinnacle | Prevents the "unreadable soup" failure (too many simultaneous tells). Legibility degrades with concurrency; the governor bounds it. |
| **`awareness_units`** (the dial's unit) | how many geometry considerations are active in the garnish config | tier-scaled: tier-1 boss reads 1–2, pinnacle reads all 5 | L-26's "boss tiers scale by reading MORE (information units)." A low boss reads only `cluster_density`; a pinnacle boss reads the full set → harder to position against. **This is the sponge alternative: difficulty from intelligence, not HP.** |

**The governor's job in one line:** the boss may be *smart* (read more, track better) but must always be *fair*
(every dangerous action has a sized tell + a recovery window + bounded concurrency). Smart-but-fair is the entire
promise of L-26's boss stack, and it is the difference between a boss the player *learns* (D2 Mephisto, PoE
Sirus, every good souls boss) and a boss the player *out-gears* (D3-vanilla-Inferno, D4-launch-Torment).

### 3.5 Spine determinism + acceptance

- **AC-SPINE-1 (deterministic compile):** the same kit compiles to a byte-identical `RotationSpine` across runs (the compiler is a pure function of the corpus row).
- **AC-SPINE-2 (uses only the kit's skills):** every beat's skill is a member of the kit's `skills[]` — the spine invents nothing (Discipline #41 assertion).
- **AC-SPINE-3 (step→phase bridge):** a `kit_delta_t4.shape=step` kit compiles a phase block with an R-1 `hp_threshold` trigger; a `ramp` kit compiles a single rising phase. (This is the R-1 dependency — see §4 sequencing.)
- **AC-SPINE-4 (garnish is bounded):** `garnish_choose_target` fires at most once per beat, at beat-open; a trace assertion confirms zero mid-commitment re-targets (the ablation-law probe — the SAME detour/switch instrument gamora built, now asserting detour is bounded by the beat structure).
- **AC-SPINE-5 (governor caps hold):** telegraph/recovery/concurrency caps are respected in a fight trace; a boss never fires a dangerous beat without its `telegraph_ticks` tell.
- **AC-SPINE-6 (inert byte-equality):** a kit run WITHOUT the spine (as a plain gauntlet mob, current path) is byte-identical to HEAD. The spine is opt-in per encounter.

---

## PART 4 — Build sequencing recommendation

The dependency spine is **R-1 first** (both the SHAPESHIFT verb-class AND the spine's phase-blocks converge on
it; §3.2's `step→phase` bridge is inert without it). E4 is independent of R-1 except the §2.4 live-read
coupling. The compiler is design-authorable in parallel but its phase-block output is gated on R-1.

| Slice | Seam | Depends on | Gate | Rationale |
|---|---|---|---|---|
| **S1 — R-1 `apply_phase_transform` + `PhaseTrigger` (hp_threshold only) + carryover + telemetry** | gamora (simulation) | — | Gate-1 (math-note-first) → Gate-2; AC-R1-1..5; **AC-R1-5 inert byte-equality is the hard gate** (the 256-battery instrument) | The foundation. Everything downstream needs mid-fight mutation. Ship `hp_threshold` first (§A7's "minimum"); `rotation_beat`/`aggro` triggers are S1.1 follow-ons. |
| **S2 — R-1 second consumer proof: SHAPESHIFT monster fixture** | gamora | S1 | AC-R1-6 (both callers, one primitive) | Proves the one-mechanism-two-callers ruling (§1.1) with a monster-side proximity/HP transform. Unblocks 2 of 5 RDR-native templates (§A7). Cheap once S1 lands. |
| **S3 — E4 `EchoChannel` (source-record + delayed re-emit + filter + depth-cap)** | gamora (sim) + rocket (the STRIKER×ECHO proxy generation) | — (parallel to S1) | Gate-1 → Gate-2; AC-E4-1..3,6; AC-E4-5 closes the ratified-law residual | Independent primitive; unblocks the 2 STRIKER×ECHO "Mirror" pairs (proxy-pairing residual #1). The player-source case needs no R-1. |
| **S4 — E4×R-1 coupling: live-source-read** | gamora | S1 + S3 | AC-E4-4 | The one genuine coupling (§2.4): a boss-shadow echoes the boss's post-transform skills. Small once both primitives exist. |
| **S5 — Rotation compiler (opener/loop/doors/cooldown; NO phase blocks yet)** | rocket (generation — it runs at gen time) | — (design-parallel; can spec against substrate now) | Gate-1 → Gate-2; AC-SPINE-1,2,6 | The `ramp`-kit path and the non-phase spine are fully expressible without R-1. Deliver this to prove the compile from substrate. |
| **S6 — Compiler phase-blocks (the `step→phase` R-1 bridge)** | rocket + gamora | S1 + S5 | AC-SPINE-3 | `kit_delta_t4.shape=step` → R-1 `hp_threshold` PhaseTrigger. GATED on R-1 (S1) landing — this is the join. |
| **S7 — Garnish plug-point (boss-flavored PolicyConfig at beat-open; dwell-spread consideration; the ablation-law lock)** | gamora | S5 (S6 for phase-conditioned garnish) | AC-SPINE-4 (the mid-commitment-re-target probe — reuse the ablation detour instrument) | Reuses the BW-1 seam verbatim. Adds the dwell-spread consideration (garnish-candidate #1). **The AC-SPINE-4 probe is the ablation-law acceptance test — it must show detour bounded by beat structure.** |
| **S8 — Legibility governor (telegraph/recovery/concurrency/read-rate/awareness-units)** | gamora | S5 | AC-SPINE-5 | The fairness layer + the difficulty dial. `read_rate_hz` + `awareness_units` are the tier-scaling knobs the ablation instrument prices. |

**Ordering summary:** S1 (R-1 core) and S3 (E4 core) and S5 (compiler-minus-phases) can proceed in parallel as
three independent foundations. S2/S4/S6/S7/S8 are joins/consumers gated as tabled. **The single most important
gate across all slices is inert byte-equality** (AC-R1-5, AC-E4-6, AC-SPINE-6) — every mechanism must be
byte-identical to `2f43045` when not installed. This is the discipline the entire reader-stack build honored and
it is non-negotiable: the boss stack is "one architecture, three configs," and the mob/free-fighter config must
not move a single bit.

**Slices gated on R-1 landing first:** S2, S6 (and S4 partly). S5, S7-base, S8 do not strictly need R-1 (they
operate on the non-phase spine), but S6/S7-phase-conditioned do. **Recommend: fire S1 + S3 + S5 as the first
wave** (three math-note-first Gate-1 dispatches), then the joins.

---

## PART 5 — Matt forks (genuine commitment-boundary decisions; options + lean; NOT ruled)

**F-R1-a — R-1 trigger scope for the first slice.** §A7 says "HP-threshold at minimum; phase/aggro desirable."
- **(i)** Ship `hp_threshold` ONLY in S1; `rotation_beat` + `aggro`/`proximity` as S1.1.
- **(ii)** Ship all three trigger kinds in S1.
- *Tradeoff:* (i) is the smaller, safer first landing and covers the genre-core boss-phase case (HP thresholds are how D2/PoE/souls do it); `aggro`-trigger is mostly a SHAPESHIFT-monster need (S2). (ii) front-loads the SHAPESHIFT monster but widens the first mutation surface.
- **My lean: (i).** HP-threshold is the boss-phase workhorse and the minimum §A7 names; get the mutation+carryover+determinism core proven on one trigger kind before widening. `aggro` rides naturally with S2's monster fixture.

**F-R1-b — may a `PhaseDelta` mutate `max_hp`?**
- **(i)** NO — `max_hp` is fixed for the fight; phases change *pattern*, not the healthbar.
- **(ii)** YES, with the rule "HP absolute carries, `max_hp` may rise (adds a shield/overheal segment) but never such that current HP-fraction resets upward."
- *Tradeoff:* (i) is the clean, D2-Duriel-honest model (one healthbar, new patterns) and forecloses the D3-Malthael "phase = fresh boss" anti-pattern entirely. (ii) enables multi-segment healthbars (PoE Sirus's storm/normal segments, some pinnacle designs) but adds a carryover hazard and a legibility cost (the player's "how close am I" read gets muddier).
- **My lean: (i) for now, revisit at pinnacle-boss design.** The One-Realm-MVP demo bosses don't need segmented healthbars; the honest single-bar model is the safer default and the stronger feel. Segmented bars are a pinnacle-act feature to spec deliberately later, not a foundation-slice decision.

**F-R1-c — may a `PhaseDelta` change ELEMENT?**
- **(i)** NO — element is fixed per entity; a form-swap keeps element.
- **(ii)** YES — a form-swap may change element (ice-handler → fire-beast), with the carryover rule "re-evaluate active ailment stacks against the new resists at transform time; do not silently drop."
- *Tradeoff:* (ii) is genre-attested (D2 form-shifters, elemental phase bosses) and dramatically strong (the mirror-reincarnator changing its element is a *story* beat, L-26's fallen-reincarnator resonance). But it interacts with the player's resist/ailment build — a boss that flips to your resisted element mid-fight can feel like a gear-check rug-pull if not telegraphed, and it complicates the ailment-carryover rule (§1.4).
- **My lean: (ii), gated on a clear `on_enter` element-shift tell.** The story resonance (the mirror changes its nature) is worth it and the substrate carries element as a kit coord, but ONLY if the legibility governor guarantees the element-shift is telegraphed (the player must be able to read "it's becoming fire now" and react). Without the tell it's a rug-pull; with it, it's a great phase.

**F-E4-a — echo magnitude scalar bounds + default.**
- **(i)** Fixed default `0.5` (the `poe2-snipe-mirage-deadeye` attested anchor), per-kit overridable in (0,1].
- **(ii)** Derive the scalar from the proxy's power budget (the STRIKER×ECHO merge math sets it).
- *Tradeoff:* (i) is simple, attested, and legible (the shadow does half your damage — a clean read). (ii) is more "balanced" but couples the echo channel to the proxy-pairing magnitude-cert loop (gamora's territory) and is harder to reason about.
- **My lean: (i) for the primitive, (ii) as the tuning pass.** Ship the channel with a `0.5` default so E4 certifies (AC-E4-5); let gamora's magnitude-cert loop tune the per-pair scalar afterward. Don't block the primitive on the balance loop.

**F-SPINE-a — how bosses source their kits (which kits become bosses).** Out of scope to *rule* here but I
surface it because the compiler needs an input contract: are boss kits (a) drawn from the SAME corpus as player
kits (a boss IS a kit, per L-26's "kit serving as a boss"), (b) a curated boss-only subset, or (c) player kits
with a boss-scalar applied?
- *Tradeoff:* (a) is the cleanest realization of L-26's "one architecture" thesis and the mirror-reincarnator story (the boss is literally a kit you could have been). (b) allows boss-specific tuning. (c) is the D3/D4 "elite = player-adjacent statline" model.
- **My lean: (a), with a boss-scalar (c-flavor) on top** — the boss IS a corpus kit (story + architecture coherence) but wears a tier-scaled stat/awareness envelope (the governor's `awareness_units` dial IS the boss-ification). This is a *design-direction* fork, not a foundation-slice blocker — the compiler spec (S5) works against any of the three. Flagging it so it's on the record for the boss-content-emission pass, not asking a ruling now.

---

## Provenance + attestation

- **Engine READ-ONLY**, grounded at `2f43045` (frozen gate hash; zero writes).
- **corpus.db READ-ONLY** (`agentic_orchestration/research/curated/corpus.db`): `kit_delta_t4` shape distribution (130 step / 137 ramp), `kit_mapping.mapping_json` trigger_grammar (499/574 kits; echo attested in `poe2-snipe-mirage-deadeye`, `d4-blood-lance`, `le-umbral-blades`, `d2-wl-echoing-strike`), `skill_geometry_band` delivery×cadence distribution — all read, none modified.
- **Real-seam grounding:** `simulation/spatial_gauntlet/policy/{considerations,seam,exposure_map}.py` (the BW-1 reader stack — the read-only selector I spec the garnish against); `spatial_engine.py:1539` (`_get_player_primary_target` boss-focus limb — the single-entity-install precedent), `:5387` (spawn-immutable `preferred_behavior` — the R-1 blocker), `:5325–5396` (the SpatialEntity combat-field set — the mutation surface).
- **Spec-of-record grounding:** sim-capacity §A7 (`src/reincarnated/simulation/spec/sim-capacity-extension-spec-2026-07-22.md`, `b34a14b`) R-1..R-4 rows; ratified proxy-pairing law (`canonical/reap-die-rise-engine/proxy-pairing-q6-q7-2026-07-02.md` + decisions-log 2026-07-02, 2026-07-22 residual #1).
- **Evidence folded:** ablation trace investigation (gamora `af0e56ce`, 144/144 byte-repro) — the commitment-loss mechanism is §0's design law.

**Signed:** gandalf `SPEC-AUTHOR`, 2026-07-22. Design-spec-as-math; NOT a build authorization. Forks in §5 are
for Matt; I do not rule them.
