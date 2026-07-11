# Reap. Die. Rise. — Substrate Addendum: Element Application & Hybridity

**Audience:** the Mac build team.
**Status:** addendum. Amends the layer contract (adds one layer row — patched in `reap-die-rise-engine-doctrine.md` Part II), **re-addresses the rotational addendum's axes per the placement test** (§4), extends the loot doc's naming law (§8). Retires the unpopulated hybrid placeholder cell currently tupled with the attribute system.
**Resolution in one line:** hybridity is a *structure* (a kind — how a second element attaches) plus a *rate* (a magnitude — how much), and the two live at different addresses; neither lives in BC space or the attribute tuple.

---

## 0. Placement Resolution (why the current placeholder is wrong)
- A hybrid **rate is a magnitude** → the placement test bars it from BC space (kinds only). A per-cell percentage would leak magnitude into the kind space — the §7 double-representation regression.
- Coupling to the **attribute tuple** (STR/DEX/INT/WIS) answers a question nobody asked (stat ratios don't determine element blend) and violates the agnostic philosophy. If attribute↔element interaction is ever wanted, that is an **operator's** job ("your INT also scales your secondary element"), not baseline plumbing.
- **Action: retire the placeholder cell.** The element-application block (§1) replaces it.

## 1. The Element-Application Block & the Binder Law
A small block on the **kit packet**, alongside kernels / chain / attributes:

```
element_application: {
  primary: <element>,
  secondary: <element | none>,        // HARD CAP: one
  structures: [<structure> x1..2],    // may co-occur, expressing the SAME secondary
  rate_band: splash | co_equal        // realized-share semantics, §5
}
```

**THE BINDER LAW:** *the element block is a binder over existing machinery, never new machinery.* Every structure attaches elements to something another layer already built (chain slots, kernel geometry, emission slots, hit/trigger hooks). Structure **creates capability** only in those layers; element application **binds to capability slots that already exist**. This is the rule that prevents every future representational collision.

## 2. The Structure Enum (7 structures, 3 families)

| Structure | Family | Binds to | Canonical anchor | Runtime cost |
|---|---|---|---|---|
| `flat_split` | blend | damage output | generic dual-damage weapons | split accounting |
| `rider_on_hit` | blend | on-hit hooks | chill-on-hit attacks | hook system |
| `proc_trigger` | blend | trigger table | "chance to ignite" | hook system |
| `chain_partition` | partition | **chain role slots** | **D2 Meteorb** (fire Meteor + cold Frozen Orb, co-equal) | **FREE** — every skill stays mono-element |
| `geometry_partition` | partition | **kernel geometry class** | "everything that flies is frost; everything that pools is fire" | **FREE** |
| `phase_partition` | partition | combo phases | cast fire → detonate lightning | free where phases exist |
| `emission_carrier` | carrier | **kernel emission slots** | **D4 dust-devil whirlwind** (spin emits wind entities) | emission system |

Notes: partitions keep every individual button pure while the *kit* is dual — arguably the most legible family. Full supersession (secondary owns 100%) is **not hybridity** — it's an ordinary element identity variation (a reskin), and the rate band ceiling (§5) enforces this.

## 3. One Emission Primitive (unification)
Every kernel geometry (nova, spin, orbital, beam, projectile, zone) carries the **same optional emission slot**:

```
emission: { entity: <ref>, origin: <point-in-geometry>, trigger: <cadence|event>, depth: ≤2 }
```

Nova-spawns-hammers, spin-spawns-devils, orbitals-spawn-orbitals — **one mechanic, many parent shapes.** The rotational addendum's `emission_hook` folds into this slot. `emission_carrier` (§2) binds elements to entities coming out of this slot — it never defines the slot.

## 4. Rotational-Axes Migration (re-addressing per the placement test)
The rotational addendum predates the factoring; run its seven sub-axes through the placement test today:
- **→ per-skill kernel vocabulary:** reference_frame, ω, dr/dt, orbiter count/phase, persistence, collision mode, and the emission slot are *trajectory vocabulary for skills* — same address as damage geometry, which already moved there.
- **→ BC cells persist only where the motion/emission IS the kit-defining kind:** the persistent-ring cell and the proxy/summon cell (both already in the canon set).
- All addendum *content* survives (identities, sim requirements, blacklist seeds); only the **addresses** redistribute. This is the addendum honoring its own §7.

**Worked example — the whirlwind cell (one cell, two anchors):**
- D2 Whirlwind: spin-to-win cell · spin kernel · **emission slot empty** · physical. Baselines the cell's envelope.
- D4 dust-devil: **same cell** · spin kernel · **emission slot populated** · element block binds secondary=wind via `emission_carrier` at a banded rate. Baselines the hybrid expression.
Rule 1 applies: these anchor separately because they **fingerprint** differently (entity spawning, AOE beyond the spin annulus, kill attribution to secondaries) — never because of coordinate proximity.

## 5. Rates & Knobs (three different numbers — do not conflate)

| Knob | Scope | Semantics |
|---|---|---|
| **Prevalence dial** | GLOBAL (pipeline/seasonal) | fraction of emitted kits that are hybrid at all. Genre feel lives here (D2 ≈ 0%, D4 ≈ majority). A seasonal lever — "hybridity arrives" is a season concept. |
| **Rate band** | PER-KIT (emission draw) | `splash` (10–25%) or `co_equal` (40–60%) of **realized elemental output share**. Banded enum — 37% is fake granularity. Ceiling < 100% by definition (§2 note). |
| **Inheritance rule** | RULE (not a rate) | generation-2 emitted entities **inherit the parent's element binding by default**; the affinity mask may override. |

**Realized-share semantics:** rate bands are defined and certified on *gauntlet-measured elemental output share*, regardless of structure — because a partition's realized share depends on which slots convert (slot count lies; a spender owns most output, a utility skill owns little). One semantic across all seven structures; kill-attribution-by-element joins the fingerprint columns.

## 6. Affinity Masks (selection vs. randomness: neither — masked sampling)
Per BC cell:

```
hybrid_affinity: {
  valid_structures: [...], weights: {...},
  hard_constraints: (carrier ⇒ emission slot present; rider/proc ⇒ hit/trigger-capable),
  pins: anchor kits may PIN a structure (the dust-devil anchor pins carrier; variations sample)
}
```

Pure per-cell selection over-authors (cells go monotone across seasons); pure randomness draws incoherent combos. **Mask-constrained sampling with pin-capable anchors** is the standing pipeline pattern applied here — authored guarantees where mechanics demand them, texture where they don't.

## 7. Certification & Blacklist Seeds
Hybrid kits run the standard gauntlet **plus** a realized-share check against the declared band. Pre-registered degenerates:
- **Blend:** dual-DoT rule-packages stacked on the same output at co-equal rate.
- **Carrier:** DoT-via-emission stacking; emission-recursion element stacking (the depth-2 cap holds).
- **Partition (the new class — partitions replace rather than add, so they're fairness-benign on damage but relocate *rule-packages* onto roles):** a control/chill package partitioned onto a high-frequency chain role = perma-slow engine; a DoT element geometry-partitioned onto a high-tick zone class = stacking exploit.
- **Exploiter hunting ground:** the chain-role × rule-package interaction matrix.

## 8. Legibility Law (extends loot doc §5.1)
Hybridity must be readable **in name and VFX before the button is pressed**: the *Emberfrost* naming pattern; VFX per family — partitions show per-button purity (each skill wears one palette), blends show mixed accents on shared outputs, carriers dress **emitted entities** in the secondary palette.

## 9. Build Order & Seasonal Hooks
1. **v1 — partitions** (`chain_partition`, `geometry_partition`): runtime-free, pure pipeline assignment. **The Meteorb ships before the dust devil** — the order the genre invented them in.
2. **v2 — blends** (split accounting + hit/trigger hooks).
3. **carrier** ships with the emission system.
Seasonally: new *pairings* at existing structures = identity-speed content; a new *structure* = a season's mechanical ingredient; the prevalence dial is a seasonal lever.

## 10. Do Not Regress
- The attribute-tuple hybrid placeholder is **retired** — no element data at the attribute address, ever.
- No rates in BC space, ever (magnitudes are barred by the placement test).
- The element block **binds; it never builds** — capability slots are created only in kernel/chain/emission layers.
- Emission has **one source of truth** (the kernel slot, §3). Any future "X spawns Y" feature routes through it or is rejected as a duplicate representation.
