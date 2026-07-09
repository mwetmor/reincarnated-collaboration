# E2 Economy Axis — Design Note (bc_amplitude → mechanical economy)

**Author:** gandalf. **Ratified:** Matt, in-session 2026-07-09 — three rulings (Q-E2-1 = (a) mixed portfolio; Q-E2-2 = cycle-throughput invariance agreed; Q-E2-3 = modulation scope agreed).
**Feeds:** rocket E2 dispatch (KR sequences; the held-dispatch precondition is CLEARED by this note landing). Ledger row **E2** (`canonical/current-to-end-state/surface-ledger.md`).
**Discipline:** design-spec-as-math (Disc #18 — gandalf authors intent + acceptance; rocket derives exact values in a math note FIRST, Disc #1).

---

## 0. Scope and boundaries

**E2 is:** `bc_amplitude` gains mechanical meaning in the emitted kit's economy — per-hit size, cooldown cadence, energy-cost texture. Today amplitude is a coordinate that never cashes out (post-E1 it is v1-INERT: a tie-shaper secondary sort only, geometry math note §3); every kit in a cell has identical economy tables regardless of amplitude.

**E2 is NOT:**
- cast-time / wind-up / charge texture — that is **E4**'s axis (sim already consumes `cast_time`; uniformly instant today);
- resource-model / regen shapes — the **tempo** axis's seam (E2 must not annex it);
- hybrid dual-scaling — **E3** (own design pass, queued);
- geometry — **E1**, landed (`bfc94eb`).

**The spine is sacred.** `TIER_COEFFICIENTS` (1.00 / 1.50 / 2.17 / 4.00), `_DAMAGE_MULTIPLIER` per (tier, role), `BASE_SPELL_DAMAGE_L50`, and the base `_ENERGY_COST` / `_COOLDOWN` tables are **untouched**. Amplitude applies as a **separate scalar layer at emission** on top of the tables — the tier curve stays the balance spine exactly as the E2 ledger ruling requires.

## 1. Ruled semantics (Matt 2026-07-09)

### 1.1 Vocabulary pin (Q-E2-1)

Canonical amplitude vocabulary: **spiky / flat / variable** — the catalog's coordinate space governs (`endgame_encounter_catalog.py`). The `per_skill_emitter.py` docstring's "spiky/sustained/flat" is a stale artifact; **correcting it is part of the E2 change**.

**variable = mixed portfolio (ruling a):** the kit's primary-attack chain runs spiky while the rest of the modulated kit runs flat — a burst window AND a filler cadence in one kit. Genre anchors: PoE slam-plus-spam builds; D2 Hammerdin weave (big committed hit inside a smooth rotation). Explicitly rejected: mid-point blend (bland-by-construction — the palette-swap failure class) and per-sample coin-flip (a label for "undecided").

### 1.2 Conservation law (Q-E2-2)

**Cycle-throughput invariance.** For every modulated attack skill: per-hit damage × casts-per-cycle holds at the tier-spine value. Spiky trades per-hit UP for cooldown UP; flat the reverse. Cost obeys the same law: **cost-per-cycle preserved** — spiky casts cost more each, fire less often.

**The single-scalar construction (the elegant core).** One per-skill amplitude scalar `k` applied jointly to (per_hit, cooldown, energy_cost):

```
throughput  = per_hit / period     → (k·per_hit) / (k·period) = per_hit / period   ✓ invariant
cost_rate   = cost / period        → (k·cost)   / (k·period)  = cost / period      ✓ invariant
```

Both conservation laws hold **exactly, by construction** — no re-balancing pass, no band forking. Certification consequence: bands should NOT lurch when E2 lands; spiky-vs-flat deltas come only from real second-order play — overkill waste, burst against fight truncation, energy pooling, ailment-application cadence, B11 geometry interaction. **That is the intended texture, and it is also the empirical test: if the post-E2 band re-fit lurches, the conservation law leaked somewhere.**

### 1.3 Modulation scope (Q-E2-3)

| Role / tier | Modulation | Detail |
|---|---|---|
| primary_attack, secondary_attack (T1–T3) | **Full** | `k` on (per_hit, cooldown, energy_cost) |
| control (T1–T3) | **Cadence-only** | `k` on (cooldown, **duration**, energy_cost); per-hit damage UNSCALED — "the lock, not the nuke." Duration scales WITH cooldown so **lock uptime is invariant** (duration/period constant): spiky controller = longer-cycle, longer-hold locks; flat = rapid short locks. Named + accepted consequence: control *chip-damage* throughput varies ×1/k (flavor-tier — control's damage multiplier band 0.40→1.00 is minor beside attack chains). |
| support | **Exempt** | no `k` |
| T4 (all roles) | **Exempt entirely** | cooldown 0.0 passive-mode capstones — modulating a passive is meaningless |

**Per-cell assignment:**
- **spiky cell** → all modulated chains get `k_spiky` (control cadence at `k_spiky`);
- **flat cell** → all get `k_flat`;
- **variable cell** → the **primary_attack chain** gets `k_spiky`; all other modulated chains (secondary, control cadence) get `k_flat`. Role-based, not chain-letter-based — robust across the five role-split templates.

**E4 boundary held:** no `cast_time` changes under E2.

## 2. Magnitude (stated lean — rocket derives exact values in the math note)

`k_spiky ≈ 1.6`, `k_flat ≈ 0.7` (per-hit ratio spiky:flat ≈ 2.29). Genre anchor: PoE slam-vs-attack-speed archetypes sit ~2–3× per-hit at comparable DPS; D3 big-hit vs IAS-stacking similar. Derivation constraints for the math note:

1. **Felt-difference floor:** spiky T3 per-hit ≥ 2× flat T3 per-hit at the same (role, tier, delivery).
2. **Cadence sanity ceiling:** `k_spiky` × max modulated cooldown (T3 primary) must leave ≥ 2 casts of the skill inside a representative gauntlet fight duration — burst that never comes back is not texture, it is a dead slot. (D3's Archon-length cooldowns on trash-clear skills failure class.)
3. **Affordability guard:** `k_spiky` × max modulated per-cast cost (T3 = 30 base) must be affordable within the sim's energy pool — no skill permanently unaffordable, no energy-starvation lockout. Pooling *pressure* is intended; lockout is a defect.
4. **Flat floor:** `k_flat` cooldowns must not collapse below the sim's effective action cadence (a cooldown shorter than the actor can act is invisible — wasted differentiation).

## 3. Acceptance criteria (the dispatch's verdict instruments)

1. **Invariance check (exact):** per-skill computed cycle-throughput and cost-rate match pre-E2 spine values within float ε for all modulated attack skills; control lock-uptime (duration/period) invariant likewise.
2. **Felt-difference floor:** §2.1 holds on emitted kits.
3. **Round-trip smoke on real kits** (E1 #2-FF pattern): emit kits from spiky, flat, AND variable cells; print per-skill (per_hit, cooldown, cost, duration-where-control) before/after; verify variable kits show the mixed portfolio (primary spiky, rest flat); verify support + T4 byte-identical; verify sim consumes without contract change.
4. **Vocab pin lands:** docstring corrected to spiky/flat/variable.
5. **Provenance:** the applied `k` is recoverable from the emitted skill record (certification honesty — the scalar must be visible downstream, not folded invisibly into the numbers).
6. **Table integrity:** zero diffs to `TIER_COEFFICIENTS`, `_DAMAGE_MULTIPLIER`, `BASE_SPELL_DAMAGE_L50`, base `_ENERGY_COST` / `_COOLDOWN` — `k` is a layer, not an edit.
7. **Math note first** (Disc #1) at `generation/math/economy-axis-e2-<date>.md`, including the §2 derivations with the four constraints shown.
8. **Duration-field location:** if control lock duration does not live on the emitted skill (engine-side per-ailment), rocket locates the real home and the uptime-invariance criterion applies wherever it lives — flag, don't fake.

## 4. Sequencing (KR-visible)

E2 fires **after the in-flight C3 re-fit lands** (per-axis main-line rhythm: generate → sim → certify, one axis at a time). E2's landing then triggers the NEXT band re-fit cycle — expected band impact small by construction (§1.2), which doubles as the conservation-law audit. Sequencing lean unchanged: **E2 → E4 → E3.**

## 5. Player consequence (why this axis exists)

Spiky = commitment windows, punished whiffs, screen-shaking numbers — the D2 Smiter/PoE slammer fantasy. Flat = smooth rotation, reliable cadence — the wand-caster/attack-speed fantasy. Variable = a build with a *moment* in it: filler until the window opens, then the payoff cast. Today all three players pilot the same metronome; after E2 the same BC cell address produces three recognizably different hands on the same tier spine — mechanical identity ("which skills dominate throughput, and when") without touching certified power.

**Signed:** gandalf, 2026-07-09. Rulings: Matt, in-session.
