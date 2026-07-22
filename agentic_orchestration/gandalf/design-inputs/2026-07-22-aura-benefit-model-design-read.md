# Aura BENEFIT-model design read — Wave-B S6-cert unblock

**Author:** gandalf (SPEC-AUTHOR) · **Date:** 2026-07-22 · **Status:** DESIGN-INPUT for KR dispatch authoring
**Trigger:** Matt ruled fork **(B) BENEFIT-BEARING** on the Wave-B Reservation/Aura lane (KR run-state §"OPEN"). The build HALTed at S6 cert: `aura_effective_benefit()` (`spatial_engine.py:2650`) composes `full · radius_gate · ramp` but has **zero fight-loop call sites**; `full_benefit` defaults 1.0, never sourced from the kit; rocket's `aura_geometry` block emits only `aura_radius_m` + `aura_reattune_ramp_s`. Sweeping both bands → byte-identical outcome (math note §8.2). Only the reservation TAX is wired.
**Companion docs:** `2026-07-21-wave-b-reservation-aura-spec-draft.md` (§5–§10, §15-R) · KR run-state `wave-b-reservation-aura-run-state.md` · math note `waveb-reservation-aura-sim-2026-07-22.md` §8 · `rdr-d2-itemization-design-digest.md`.
**REMOTE-TRUTH (do not reopen):** `canonical/reap-die-rise-engine/wave-b-economy-engine-spec.md` (`b850800`). All §15-R rulings BINDING. FORBIDDEN fields (`aura_polarity`, `aura_target_cap`, `exclusive_aura_class`) stay absent.
**Engine facts grounded at HEAD `bcbe001`** (all cited symbols verified read).

> **Scope of this doc:** it fills the ONE hole fork (B) opened — *what magnitude flows into the already-built `full_benefit` slot, and where it is felt.* It does NOT re-spec radius/ramp/reservation (built + smoke-green) and does NOT re-open any §15-R ruling. NO code, NO dispatch authoring (KR's).

---

## §1 — Benefit families: WHAT auras grant

An aura's benefit is a **stat-mod on beneficiaries in radius** (spec §6/§10-C1 verbatim: the set within `aura_radius_m` "receives the stat-mod; outside get nothing"). The genre splits benefits into two mechanically distinct shapes, and only one is a stat-mod:

**Shape 1 — STAT-MOD auras** (persistent while-in-radius modifier on a beneficiary's resolved damage/defense/regen/speed). This is what the built `aura_effective_benefit()` composition already expresses — `full` is a stat-mod magnitude, gated by radius, ramped by C4. Genre by name:
- **Damage-amp** — D2 paladin *Might / Concentration / Fanaticism*; PoE *Hatred / Anger*. Beneficiary's damage-out ×(1+m).
- **Defense** — D2 *Defiance / Salvation*; PoE *Determination / Grace*. Beneficiary's damage-taken ×(1−m).
- **Sustain/regen** — D2 *Prayer / Meditation*; PoE *Vitality*. Beneficiary's resource/health regen ×(1+m).
- **Speed** — PoE *Haste*; D2 *Fanaticism* (attack-speed rider). Beneficiary's cast/attack/move rate ×(1+m).

**Shape 2 — PULSE-DAMAGE auras** (benefit = a periodic *damage EMISSION* to enemies in radius, NOT a stat-mod on anyone). D2 paladin *Holy Fire / Holy Freeze / Holy Shock*; PoE *heralds* are adjacent. This is a **different mechanical shape** — it is an AoE damage tick centered on the carrier, not a modifier multiplied into someone's resolution. It does **not** flow through the `full_benefit` slot; it needs its own per-tick damage-application path (closer to `_apply_skill_damage` than to `get_buff_percent`).

### The v1 family set (LEAN — LOCKED to shipped-family recommendation)

**Ship Shape-1 stat-mod families only in the v1 wiring: DAMAGE-AMP · DEFENSE · REGEN · SPEED.** Grounds — three:

1. **They are the shape `aura_effective_benefit()` already computes.** Wiring them is a *sink* problem (route the composed scalar into resolution), not a *new mechanism* problem. Rocket owes ONE magnitude field; gamora owes call-sites into paths that already exist (§4). This is the minimal true completion of fork (B).
2. **They map 1:1 onto the engine's EXISTING buff vocabulary.** `damage_resolver.py:1168` already recognizes the ActiveEffect family `("buff_damage", "buff_defense", "buff_dodge", "buff_mana_regen")`, summed by `combatant.get_buff_percent()` (:426, sums `params["percent"]`) and composed at `resolve_skill:814` (`buff_dmg_mult = (1+get_buff_percent("buff_damage")) · damage_modifier · (1+bonus_damage_percent)`). The four v1 families are the four canonical stat axes this hook already speaks. No new resolution arithmetic type.
3. **The corpus the reservation-aura family serves is stat-mod-dominant** (spec §5 ground 2: built RS roster is Grace/Determination/Discipline/Hatred-shaped — all Shape-1). Shipping Shape-1 first faithfully represents the dominant corpus, matching the built spec's own "match the attested shape" method.

**DEFER Shape-2 PULSE-DAMAGE as a named later family.** Do NOT wire it v1. **Re-open trigger (state it in the dispatch so it is not lost):** pulse-damage re-opens when (a) the corpus census surfaces a Holy-Fire-class kit that cannot be expressed as a stat-mod aura (a genuine *emission* aura), OR (b) an offensive-aura archetype is prioritized for a later slice. Its build cost is a separate per-tick AoE-damage path + a distinct emission field (`aura_pulse_damage` or equivalent) — explicitly NOT the `full_benefit` scalar. Deferring it costs zero v1 critical path (it is additive, like the capstone slice).

> **Discipline #41 respected:** no fantasy-archetype taxonomy is introduced. "Damage-amp / defense / regen / speed" are MECHANICAL stat axes (the same class of enum as the geometry enums and the existing `buff_*` names) — not "paladin / templar / warcaster" archetype labels. The families name *what stat moves*, never *who the character is*.

---

## §2 — Magnitude bands (per shipped family)

**Anchoring principle — the Σ-budget equilibrium.** At **band midpoint**, an aura's marginal combat value should ≈ the reservation price its carrier pays (`reservation_percent` on the carrier). Then toggling is a REAL choice (benefit ≈ cost at the margin) and stacking to Σ<0.90 is a **build identity**, not free power. Below-midpoint = the aura is a luxury you pay pool for; above-midpoint = it starts to be strictly-worth-it and the Σ<0.90 activation-block (built, live) is what stops runaway stacking.

**Engine stat-mod scale (grounded, HEAD `bcbe001`):**
- **Damage** = `damage_multiplier × 500 × attacker.damage_modifier` (`spatial_engine.py:2191,2213`), further ×`(1+get_buff_percent("buff_damage"))` at `resolve_skill:814`. So a benefit `m` on damage-amp = a **+m fractional damage-out multiplier**, linear. `m=0.10` ⇒ +10% damage.
- **Defense** — the engine's incoming-damage rail: sunder's `damage_taken_percent` calibration band is **[0.15, 0.25]** (`damage_resolver.py:75`, LOCKED). A defense aura is the *mirror* (reduce damage-taken), so its magnitude lives in the same order-of-magnitude rail.
- **Regen** — `mana_regen × (1.0 + get_buff_percent("buff_mana_regen"))` (`combatant.py:477`). Benefit `m` = +m fractional regen. This composes directly with the reservation pool-ceiling tax — a regen aura that pays reservation and grants regen is a *self-consistent economic loop*, which makes it the cleanest equilibrium demonstrator.
- **Substrate-resistance reference magnitude** — the engine's own "this is a meaningful combat swing" precedent is the 7×7 resistance matrix default **±25%** (1.25/0.75, `damage_resolver.py:9`). Aura magnitudes should sit *at or below* this — an aura is a sustained layer, not a one-shot elemental advantage, so it should not out-swing the matrix.

### Proposed scaffold bands (Discipline #40 scaffold-declaration; gamora S6 cert finalizes)

| Family | Sink axis (engine hook) | Band (scaffold) | Rationale |
|---|---|---|---|
| **Damage-amp** | `buff_damage` % → `resolve_skill:814` | **[0.08, 0.20]**, mid 0.14 | Below the ±25% matrix swing (an aura shouldn't beat an element matchup); mid 0.14 ≈ a mid `reservation_percent` carrier's price → equilibrium. Stacking two mid damage-auras ≈ +30% before Σ<0.90 bites. |
| **Defense** | damage-taken ×(1−m) | **[0.08, 0.20]**, mid 0.14 | Same rail as sunder's `[0.15,0.25]` (`damage_resolver.py:75`); kept slightly under so a defense aura is meaningful but not a wall. |
| **Regen** | `buff_mana_regen` % → `combatant.py:477` | **[0.10, 0.30]**, mid 0.20 | Regen is lower combat-value per point than damage (it buys sustained casting, not burst), so a wider/higher band buys equilibrium against the reservation tax it pays. |
| **Speed** | cast/attack/move rate ×(1+m) | **[0.05, 0.15]**, mid 0.10 | Speed compounds (more actions → more damage AND more sustain), so the tightest band — a small speed % is worth more than the same damage %. Genre echo: PoE Haste is deliberately low-magnitude. |

**Bands are SCAFFOLD, not LOCKED** — they mirror the existing `aura_reattune_ramp_s` [0.5,1.5] scaffold-declaration pattern (rocket emitted it with default+band; gamora tunes at cert). gamora finalizes each band at S6 between the **D2-dominance band** (an aura-stacker trivializes content — containment target) and the **evaporate band** (auras too weak to feel). The midpoints above are the equilibrium starting-line, not the answer.

**THE FALSIFICATION (this is the whole point of fork B).** A band sweep across `full_benefit ∈ band` MUST now produce **non-identical fight outcomes** — kills the byte-identical failure (math note §8.2, where `radius{2,7,12}×ramp{0.5,1,1.5}` → 50.000 energy, identical). The S6 cert's first assertion: sweep `full_benefit` low→high on a damage-amp aura kit, observe monotonic win-rate / TTK movement. If it is still byte-identical, the sink is not wired and the cert fails (not passes).

---

## §3 — The emission field (ONE new rocket field)

Fork (B) needs the kit to *source* a benefit magnitude into the `full_benefit` slot that already exists on the ActiveEffect (`spatial_engine.py:2639`). Two candidate shapes:

- **(a) SCALAR + family discriminator** — a `aura_benefit_mod` float (the magnitude, band-guarded per §2) **+** an `aura_benefit_kind` enum ∈ `{damage, defense, regen, speed}` (which sink axis). Two fields, both additive to the `aura_geometry` block.
- **(b) TYPED PAYLOAD** — a nested `{kind, magnitude}` dict per aura.

### LEAN: (a) SCALAR + family discriminator.

Grounds — three:

1. **It matches the additive-emission pattern rocket already ran twice this wave.** `aura_radius_m` and `aura_reattune_ramp_s` are both flat scalars in the frozen `AURA_GEOMETRY_KEYS` tuple with a default + band + 1-line MIGRATION (`generation/aura_geometry.py:42`). Two more flat keys (`aura_benefit_mod` float|None, `aura_benefit_kind` str|None) extend the SAME contract the same way — sibling fields, `_validate_aura_geometry` gains a band-guard on the scalar + an enum-guard on the kind, inert corner stays `None/None` = byte-identical. A typed payload (b) would break the flat-scalar shape the block established and complicate the extra-key drift guard.
2. **The discriminator is a MECHANICAL enum, Discipline #41-clean.** `{damage, defense, regen, speed}` is the same class of enum as the geometry constants — it names *which stat axis*, exactly the four axes `damage_resolver.py:1168` already dispatches (`buff_damage/buff_defense/buff_dodge/buff_mana_regen`). It is NOT a fantasy-archetype tag. (A forbidden enum would be `aura_class ∈ {paladin, templar}` — this is not that.)
3. **`None` is the correct inert sentinel** (same reasoning as the radius field, `aura_geometry.py:63`): `aura_benefit_mod=None` ⇒ `full_benefit` stays 1.0 ⇒ the aura is reservation-only (fork-A behavior preserved as the inert corner), and a kit with a real benefit sets both. This keeps the whole prior build byte-identical when the field is absent — the additive-identity theorem the wave has held throughout.

**Band-guard on emission** (per §2, Discipline #8 schema validation at the boundary): `_validate_aura_geometry` rejects `aura_benefit_mod` outside the per-kind scaffold band. Because the band is kind-dependent, the validator reads `aura_benefit_kind` to pick the band. Scaffold-declaration annotation (Disc #40): `SCAFFOLD — gamora S6 cert finalizes band`.

**MIGRATION:** 1-line addition to `generation/MIGRATION.md` (new cross-seam consumed fields, ADR-004), mirroring the existing `aura_geometry.py` MIGRATION entry.

---

## §4 — Wiring acceptance criteria (for gamora)

**Where the benefit ENTERS resolution (call-site CLASS, by symbol — not line numbers, which drift):**

The composed scalar `aura_effective_benefit(aura_effect, beneficiary, elapsed)` must be **read per-tick per-beneficiary and applied to that beneficiary's resolved output on the sink axis named by `aura_benefit_kind`:**

- **`damage`** → fold into the `buff_dmg_mult` composition in `damage_resolver.resolve_skill` (the `get_buff_percent("buff_damage")` term) — OR, equivalently, seed a `buff_damage` ActiveEffect whose `percent` is refreshed per-tick from the aura's effective benefit. The existing `("buff_damage",…)` dispatch at `resolve_skill` already consumes this; the aura becomes a *source* of that percent, radius-and-ramp-gated.
- **`defense`** → the incoming-damage mitigation path (the same rail sunder's `damage_taken_percent` uses, mirror-signed) — beneficiary's damage-taken ×(1 − effective_benefit).
- **`regen`** → `combatant.apply_mana_regen_buff` (`get_buff_percent("buff_mana_regen")`) — the aura sources this percent.
- **`speed`** → the cast/attack/move-rate scalar the beneficiary already carries.

The **radius gate and ramp are already inside `aura_effective_benefit()`** — gamora does not re-implement them; the sink reads the composed `full · radius_gate · ramp` and `full` is now the kit-sourced magnitude (not the 1.0 default). The establishment path (`_establish_aura_carriers` :2667, called from `run()` :3365) already stamps `full_benefit` onto the ActiveEffect params (:2639) — it must now read the emitted `aura_benefit_mod` instead of defaulting 1.0.

**AC-9 "aura-is-felt" — operationalized (the cert that was un-runnable, now runnable):**

- **AC-9a (non-identity — the falsification):** a band sweep of `aura_benefit_mod` low→high on a damage-amp aura kit produces **monotonically non-identical** fight outcomes (win-rate or TTK moves with magnitude). If byte-identical, the sink is unwired ⇒ FAIL. (This is the exact test math note §8.2 ran and got 50.000-identical; it must now vary.)
- **AC-9b (equilibrium):** aura-ON vs aura-OFF win-rate delta at **band-midpoint** sits in a *healthy window* — non-trivial (the aura is felt: delta above an evaporate floor, e.g. ≥ a few % win-rate) but NOT dominant at a single aura (delta below the D2-dominance ceiling). gamora sets the exact window at cert; the design constraint is "midpoint ≈ the reservation price at the margin" (§2).
- **AC-9c (stacking is identity, not free power):** two mid-band auras stacked (under Σ<0.90) play *recognizably* differently from one (more total benefit for more total pool paid) — the build-identity predicate — but do NOT breach the D2-dominance band. This is where the efficiency capstone (§7, deferred) will later be the containment dial.

**Interaction with the Σ activation-block guard (built, live — FLAG A / AC-7-SIM):** the benefit MUST NOT bypass the guard. The order is fixed by the built code: `_toggle_aura_on` (:2605) evaluates `aura_activation_would_breach` **before** appending the ActiveEffect (:2626-2631) — a blocked aura is never appended, so its `full_benefit` never enters any sink. Wiring the benefit changes nothing here: the benefit rides the ActiveEffect, and no ActiveEffect ⇒ no benefit. **AC:** a benefit-bearing aura that would breach Σ<0.90 grants ZERO benefit (blocked before establishment) — assert the win-rate contribution of a guard-blocked aura is exactly nil.

**Banner (8a) inherits the benefit path via origin-arg:** `plant_banner` (:2704) already threads `full_benefit` into `_toggle_aura_on` (:2726) and reuses `aura_effective_benefit` with a `_PosProbe` origin (:2660). So a banner sources `aura_benefit_mod` the same way a carried aura does — the benefit is gated from the *plant-point*, not the caster. No separate benefit wiring for the banner; the origin-arg design (built Slice-2) already generalized it. **AC:** a banner's beneficiaries in radius-from-plant-point receive the benefit; the roaming caster outside the plant radius does not (unless self-in-radius).

---

## §5 — Seam split

| Item | rocket | gamora | gandalf / Matt |
|---|---|---|---|
| §3 emission field `aura_benefit_mod` (float\|None) + `aura_benefit_kind` (enum\|None) on `aura_geometry` block | **OWNS** — additive keys, `_validate` band+enum guard, `None/None` inert corner, 1-line MIGRATION | consumes | ruling **(B)** already given; no further Matt gate |
| §2 magnitude bands (scaffold values) | emits with scaffold default+band (Disc #40) | **OWNS finalization** at S6 cert (D2-dominance/evaporate) | equilibrium *principle* (this doc); midpoints are the starting-line |
| §4 wire `aura_effective_benefit()` into resolution (4 sink axes) | — | **OWNS** — source the composed scalar into `buff_damage`/defense/regen/speed paths; benefit rides the ActiveEffect | — |
| §4 AC-9a/b/c + falsification (non-identity sweep) | — | **OWNS** — S6 cert as originally spec'd, now runnable | AC-9 *criterion shape* (this doc) |
| Σ-guard non-bypass (built, live) | — | **preserves** (benefit rides ActiveEffect; blocked ⇒ no benefit) | — |
| Banner benefit inheritance (origin-arg) | — | **OWNS** (reuses built `plant_banner` full_benefit thread) | — |
| Shape-2 PULSE-DAMAGE family | DEFERRED (separate field later) | DEFERRED (separate AoE path later) | re-open trigger stated §1 |
| Efficiency capstone as stacking-containment dial (§7 draft, Fork-4 4c) | DEFERRED behind MVP + Q35 | DEFERRED | Fork-5 vehicle PARKED → Q35 (soulbound-gear), Matt-present |

### Commitment-class residue back to Matt (kept minimal — Matt ruled (B) to UNBLOCK)

**One flag, and it is genuinely archetype-identity, not implementation:**

- **The four-family set is a scope commitment.** This doc LEANS "ship damage-amp / defense / regen / speed in v1; defer pulse-damage." That is a *taste/scope* judgment about what an aura archetype IS at v1, which per the authority envelope (KR run-state §"Authority envelope": scope changes → HALT to Matt) is Matt's to ratify, not gamora's to assume. **Recommended handling:** KR cites this §1 lean into the rocket dispatch as the *proposed* v1 set; if Matt concurs (or is silent under the (B)-ruling-implies-stat-mod-families reading), it proceeds. If Matt wants pulse-damage in v1, that is a *second* rocket field + a *second* gamora path (materially larger scope) and re-opens the slice sizing. **This is the only genuine fork; everything else in this doc is implementation of ruling (B).**

Bands, sink axes, emission shape, and AC-9 operationalization are all **reasoning-boundary** decisions inside the (B) ruling — no Matt gate. The four-family v1 *scope* is the one **commitment-boundary** residue.

---

## Appendix — the falsification, restated for the cert

Fork (A) world (current HEAD): `full_benefit ≡ 1.0`, `aura_effective_benefit` uncalled → band sweep byte-identical (math note §8.2). Fork (B) world (this doc's target): `full_benefit ← aura_benefit_mod` (kit-sourced, band-guarded), `aura_effective_benefit` read per-tick into the sink axis → **band sweep MUST vary monotonically.** The cert PASSES when the sweep varies and the midpoint sits in the equilibrium window; it FAILS if the sweep is still identical (sink unwired) OR if a single aura reaches the D2-dominance band (magnitude too high). That is the whole of what fork (B) asked for, made decidable.

---

## DRIFT-CRITIC review — 2026-07-22 (conductor pass on own sub-agent draft)

**▶ ROLE: DRIFT-CRITIC — reviewing gandalf sub-agent's draft against the §15-R ruled-fork set + KR run-state authority envelope before it becomes the input of record.**

Checklist (all pass):

1. **No §15-R re-opens** — all ruled forks (Σ-cap 0.90, banner origin-arg, D2-reservation register, S6 cert framing) consumed as constraints, none re-litigated ✓
2. **Forbidden fields absent** — no archetype/class enum, no per-class aura tables, no kit-side behavior branching ✓
3. **v1 scope shape** — stat-mod families only (damage/defense/regen/speed), pulse-damage DEFERRED with a *stated* re-open trigger, not silently dropped ✓
4. **Bands** — numeric, engine-grounded (damage_resolver.py:1168 buff vocabulary, combatant.py:477 regen), equilibrium-principled, Disc #40 scaffold with gamora finalization at S6 ✓
5. **Emission shape** — scalar `aura_benefit_mod` + `aura_benefit_kind`, None/None inert corner, Disc #41-clean (mechanical stat axes, not archetypes) ✓
6. **AC-9a/b/c falsifiable** — monotonic non-identity sweep kills the byte-identical failure mode; equilibrium window decidable; stacking identity under Σ<0.90 ✓
7. **Σ-guard non-bypass** — benefit rides ActiveEffect; blocked aura ⇒ zero benefit, no side channel ✓
8. **Banner inheritance** — reuses built `plant_banner` origin-arg thread, no new mechanism ✓
9. **Commitment-boundary residue** — exactly ONE Matt-flag (four-family v1 scope), correctly classified; everything else reasoning-boundary inside ruling (B) ✓

**VERDICT: PASS — this doc is the input of record for the R2=B unblock chain (KR cites §1 into the rocket field dispatch + §2/§4 into the gamora wiring dispatch; S6 cert as spec'd via AC-9).** The §5 four-family flag goes to Matt with the delivery.

— gandalf (DRIFT-CRITIC), 2026-07-22
