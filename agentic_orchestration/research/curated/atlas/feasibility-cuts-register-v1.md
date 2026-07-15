# Feasibility-Cuts Register — v1

> **STATUS:** CURRENT (load-bearing as of 2026-07-14). The enumerated feasible lattice
> (SPACE) that the atlas ghost field (charter §4) projects. **Ghosts land whenever THIS
> register lands** (decoupling law); **coverage claims use the enumerated feasible lattice,
> never the sample** (denominator law).

**Author:** elrond (data steward — enumeration + register) · **Date:** 2026-07-14
**Tracker item:** IV.x-b (feasibility-cuts register → atlas ghost field)
**Charter:** `canonical/reap-die-rise-engine/atlas-derivation-charter-2026-07-14.md` §2 (SPACE ≠ MAP; three ratified cut classes) + §4 (ghost field)
**Enumeration base:** `canonical/reap-die-rise-engine/coordinate-register-2026-07-13.md` §2 — the 13-coordinate kit-identity key (element-free; 14 serialized `cell_key` slots)
**Red-law source:** `agentic_orchestration/gandalf/design-inputs/2026-07-13-gaps-kpis-direction-analysis.md` §A.4 (the 3 intrinsic RED laws)
**Machine-readable twin:** `feasibility-cuts-register-v1.csv` / `.json` (this dir) · **Generator:** `agentic_orchestration/research/scripts/feasibility_cuts_register_2026_07_14.py` (regenerates everything from one command)
**Governance:** gandalf audits; **Matt ratifies taste cuts one by one** (charter §2). Logical + red-law cuts are the ratified cut *classes*; the taste slate below is proposed, NEVER applied.

---

## 0. What this register is (and what it is NOT)

This register turns the raw 13-coordinate combinatorics into the **enumerated feasible lattice** — the SPACE. It is the denominator for every "we've explored X%" claim and the substrate the ghost field projects into the frozen Edition-I basis.

**A load-bearing distinction (do not conflate two lattices):**

| Lattice | Doc | Naive box | Number of record |
|---|---|---|---|
| **Kit-IDENTITY lattice** (THIS register) | `coordinate-register-2026-07-13.md` §2 — 13 coords, element-free | **900,169,200** (pre-cut naive; see caveat) | **feasible lattice = 422,445,240** (post logical + red-law) |
| **Engine-native SUBSTRATE lattice** (separate object) | `substrate-coordinates.md` L0–L4 | banned bounding box **2.57×10⁹** | L4 ≈ **1.284×10⁹** |

> ⚠ **Renderer rule R2 spirit — naive-box caveat.** The 13-coord register's own raw naive
> product is **900,169,200** (≈9.0×10⁸). This is the **pre-cut naive box** — it treats all
> coordinate slots as free-independent, which fabricates hundreds of millions of incoherent
> cells (a damage kit with a control function; a summon with nothing summoned). **It is
> reported here inside the register with this explicit caveat; it is NEVER a coverage
> denominator and NEVER a surface headline.** The coverage denominator is the *feasible*
> lattice (422,445,240). — This is a **different** naive box from the substrate `2.57B`
> (which is the engine-native 9-axis + element + hybridity all-independent bound); the `2.57`
> ban in the renderer spec applies to the substrate object, not to this register.

The feasible lattice is enumerated by **arithmetic on the register cardinalities minus cut predicates** — never estimated. Every cut states its predicate over coordinate values; no cut is silent.

---

## 1. The enumeration base — coordinate cardinalities (definitional)

Element-free identity key, `coordinate-register-2026-07-13.md` §2. Masks (`unknown`/`blank`) are **curation states, never definitional cells** — excluded from the SPACE. Coord #5 serializes as **two** `cell_key` slots (treatment + function); hence 14 positions for 13 coordinates.

| # | Coordinate | Definitional values | card |
|---|---|---|---|
| 1 | movement | FREE-MOVE · WALK · ROOTED | 3 |
| 2 | delivery | PROJECTILE · ORBITAL · NOVA · ZONE · BEAM · MELEE · SUMMON | 7 |
| 3 | amp | FLAT · SPIKY · VAR | 3 |
| 4 | geometry | ~21 abstract shapes rolling up into #2 | 21 |
| 5a | treatment | damage · control · hybrid | 3 |
| 5b | function | none · hard-stop · stun · taunt · fear · blind · knockback · expose · hex · silence | 10 |
| 6 | defense | tank · mitigate · evade · absorb · glass | 5 |
| 7 | economy | spend · cooldown · generator-spender · reserve · self-cost · finite · free | 7 |
| 8 | proxy | solo · light · heavy | 3 |
| 9 | range | melee · mid · ranged · dual | 4 |
| 10 | tempo | low · med · high | 3 |
| 11 | commit | instant · wind-up · channel | 3 |
| 12 | activation | active · triggered | 2 |
| 13 | dependency | one-shot · build→spend · apply→detonate | 3 |

**Raw naive product** = 3·7·3·21·3·10·5·7·3·4·3·3·2·3 = **900,169,200**. (See §0 caveat: this is the pre-cut naive box, not a denominator.)

---

## 2. The counts ladder

Both grains. **Exact-lattice** = all 13 coordinates. **Meso-grain** (register rollup) = the never-demote core (`coordinate-register-2026-07-13.md` §6.1: #1 movement · #2 delivery · #5 control [treatment+function] · #8 proxy · #12 activation · #13 dependency) — the grain the charter §4 falls back to if the exact lattice is too large to project point-per-cell.

| stage | exact-lattice | meso-grain |
|---|---|---|
| raw naive product | **900,169,200** | **11,340** |
| → post-logical (4 cuts) | **461,515,320** | **6,840** |
| → post-red-law (1 lattice cut) | **422,445,240** | 6,840 |
| (post-taste, if ALL 5 accepted) | ~130,000,000* | 3,060† |

\* Illustrative only — taste cuts overlap; the exact all-accepted figure is not additive and is not computed as a headline (Matt ratifies one by one, so a "post-all-taste" number is not a real state). See §5 for per-candidate post-red-law removal. † meso all-taste = only T5 is meso-expressible: 6,840 − 3,780 = 3,060.

**Reduction:** logical cuts remove **~49%** of the naive box (438.7M cells); the one lattice-expressible red-law removes a further **~8.5%** of the naive box (39.1M). The feasible lattice is **~47%** of the naive box — the naive box roughly doubles the truth, almost entirely on the incoherent damage⊗control-function product.

The **corpus lights 469 of these ghosts** (the active combat-kit set, `2026-07-14-gate-report.md` Stage 0). Coverage against the feasible lattice = 469 / 422,445,240 ≈ **1.1×10⁻⁴ %** at exact grain; 469 distinct-key kits collapse toward far fewer occupied meso cells (the isotope collapse — occupied-meso count is a render-time measurement, not enumerated here).

---

## 3. Logical cuts — incoherent by definition

Four cuts. Each is a predicate over coordinate values with the logical rule stated. Removed-counts are the **marginal footprint on the raw box** (cuts overlap; the ladder in §2 uses composed survivors). Meso-grain footprint given where the cut's coords are in the core.

| id | rule (predicate) | removed (exact) | removed (meso) |
|---|---|---|---|
| **L1** treatment-function coherence | `damage ⟺ function=none` ; `{control,hybrid} ⟺ function≠none` | 330,062,040 | 4,158 |
| **L2** summon ⟹ proxy | `delivery=SUMMON ⟹ proxy∈{light,heavy}` (SUMMON⊗solo forbidden) | 42,865,200 | 540 |
| **L3** melee-delivery range coherence | `delivery=MELEE ⟹ range≠ranged` (melee/mid/dual allowed) | 32,148,900 | 0 (range∉core) |
| **L4** ranged-delivery range coherence | `delivery∈{PROJECTILE,ORBITAL,BEAM} ⟹ range≠melee` (payload travels) | 96,446,700 | 0 (range∉core) |

**L1 — the big one.** Coord #5's two `cell_key` slots (treatment + function) are ONE concept (register §3): a pure-damage kit has no control function (`none`); a control/hybrid kit *is* its control function, so `none` is incoherent for it. Enumerating the slots freely fabricates 330M non-existent cells. Of the 30 (treatment × function) pairs, only **19 are coherent** (damage×none = 1; control×{9 non-none} = 9; hybrid×{9 non-none} = 9).

**L2 — summon implies a proxy.** Register §3B defines summon-economy as `model ∩ delivery=SUMMON ∩ proxy density`. A SUMMON kit's identity *is* its proxy; `proxy=solo` means nothing was summoned — the pairing has no referent.

**L3 / L4 — delivery↔range coherence.** Charge C.5 names melee⊗projectile-family as **definitional** (the range coord is partly derived from delivery). Operationalized on the identity key as two half-predicates: a MELEE-delivered strike cannot have pure-ranged reach (L3); a projectile/orbital/beam kit cannot have pure-melee reach because the payload travels (L4). `dual` (hybrid reach) and `mid` (lunge/extended) survive both. NOVA/ZONE/SUMMON are range-unconstrained (a point-blank nova is coherent).

---

## 4. Red-law cuts — 3 intrinsic laws, applied WHERE HONESTLY EXPRESSIBLE

The critical honesty rule (charter §2): **a red law that is about kit-internal design pattern and does NOT translate to a coordinate-combination predicate STAYS a generation/curation filter and is NOT applied to the lattice.** Force-fitting is forbidden. Here is the honest disposition of all three:

| red law | lattice cut? | disposition |
|---|---|---|
| **RED-1 co-location** | **NO** | filter only — key-invisible |
| **RED-2 no anti-synergy** | **NO** | filter only — key-invisible (+ future sim-KPI) |
| **RED-3 movement-damage carve-out** | **YES** | lattice cut — coordinate-expressible |

**RED-1 (co-location) does NOT cut the lattice.** "Damage must be co-located with the avatar's present position or an anchored proxy." This distinguishes damage painted *where the avatar was* from damage *at its present position* — a trail-vs-chase **geometry/positional** property. The 13-coord identity key encodes no trail/present positional coordinate. gandalf §B.5 states this verbatim: "structurally under-observable … the co-location law is carried by curation/generation filters instead. That is division of labor, not failure." **Stays a generation/curation filter.** Not force-fit into a predicate the key cannot honestly express.

**RED-2 (no anti-synergy) does NOT cut the lattice.** "Sustain must not cannibalize the build's own resources, army, or economy." The corpses (poe1-reaper — a minion that eats your other minions; vs-gatti-amari — cats that eat your pickups) are **within-kit relational** patterns: this kit's sustain consumes this kit's *own* scaling substrate. Two kits with **identical 13-coord keys** can differ on whether the sustain cannibalizes — the property lives in the mechanic, not the coordinate tuple. gandalf §A.2-6: observable only as a future sim-KPI (K5 self-inflicted proxy-death / K6 economy drain) on **emitted** kits, never as a lattice predicate. **Stays a generation/curation filter.**

**RED-3 (movement-damage carve-out) DOES cut the lattice.** "Movement verbs as damage loops only at instant-commit + high tempo." This is the one honestly coordinate-expressible red law. gandalf §A.2-4 states the register **already** separates the living from the dead by exactly two coordinates: flicker-survivors sit at `commit=instant + tempo=high`; leap-attack-corpses at `commit=wind-up + tempo=low`. The predicate:

> `geometry ∈ {movement-verb geoms} ∧ ¬(commit=instant ∧ tempo=high) ⟹ SEAL`

| id | rule | removed (exact) | removed (meso) |
|---|---|---|---|
| **RED-3** movement-damage carve-out | as above | 76,204,800 | 0 (geometry∉core) |

**⚑ Honesty caveat on RED-3's cardinality (curation binding flagged).** The antecedent is keyed to the **movement-verb geometry class** — the #4 geometry slots that *are* movement verbs. The corpus surfaces two: `dash_attack`, `teleport`. The register's coord #4 is `~21 abstract shapes`; this enumeration designates **2 of 21** as movement-verb slots (`g00`, `g01` placeholders standing for dash/teleport). The cut is real and coordinate-expressible; its **exact cardinality depends on which of the 21 geometry slots are bound as movement-verbs**, a curation ruling not yet locked. If that binding changes (e.g., a third movement-verb geometry lands), RED-3's count moves — flagged as a re-run trigger. Also note RED-3 is **not expressible at meso-grain** (geometry is a demotable coord, not in the never-demote core) — meso-grain removes 0 here, which is correct: the carve-out is a within-cell (geometry-level) seal, invisible at the rollup grain. This is a genuine finding: **the movement-damage carve-out cannot be drawn at meso-grain; it only appears when the ghost field renders at geometry resolution.**

---

## 5. Taste-candidate slate — PROPOSED, never applied

Per charter §2, **Matt ratifies taste cuts one by one.** These are a slate for consideration; none is applied. Removed-counts are the **additional cells sealed on the post-red-law survivor lattice** (422,445,240) if that candidate alone is accepted — the honest "this decision seals this many ghosts." Percentages are of the surviving lattice. (Exact, factored; MC-cross-checked.)

| id | predicate | removes (post-red-law) | % survivors | taste question |
|---|---|---|---|---|
| **T5** hybrid-treatment plane | `treatment=hybrid` | **200,105,640** | **47.4%** | Enumerate the full hybrid-treatment plane as frontier (Mendeleev), or treat `hybrid` as a curation interpolation, not a first-class ghost region? **HIGHEST-IMPACT decision in the slate** — hybrid is corpus-empty (active corpus: damage/control only, zero hybrid) yet definitionally present; it multiplies the entire function sub-plane. |
| **T2** triggered + wind-up | `activation=triggered ∧ commit=wind-up` | 69,593,580 | 16.5% | Double-latency (the condition fires, then you still charge). Genre-rare. Seal as feel-dead, or keep for telegraphed heavy procs? |
| **T3** self-cost + heavy proxy | `economy=self-cost ∧ proxy=heavy` | 21,299,760 | 5.0% | The blood-summoner corner (bleed your HP to sustain a heavy army). Coherent but a strong flavor commitment — reserve for a signature archetype, or seal as over-specific? |
| **T4** flat + low + channel | `amp=FLAT ∧ tempo=low ∧ commit=channel` | 15,465,240 | 3.7% | The flattest, slowest, most inert damage feel in the space. Seal as anti-fun, or keep (some sustained-drain fantasies live here)? |
| **T1** glass + rooted + channel | `defense=glass ∧ commit=channel ∧ movement=ROOTED` | 9,279,144 | 2.2% | The maximally-exposed sustained-cast corner (the CONTESTED rooted-channel cell's most fragile sub-region). Seal, or keep as the balance-loop's showcase? |

**Note on T5.** T5 is a genuine architectural fork, not a mere trim. The corpus has zero `hybrid`-treatment kits — every active kit is damage or control. If Matt rules hybrid a *curation interpolation* (a kit is fundamentally damage-primary or control-primary, hybrid being a blend annotation rather than a distinct identity), nearly half the enumerated ghost field vanishes and the coverage denominator halves. If Matt rules hybrid a *first-class frontier*, the atlas advertises a vast unexplored hybrid-treatment region. This decision should be taken deliberately and early because it dominates the denominator.

---

## 6. Ghost-projection readiness

**Confirmed (not yet emitted):** the surviving feasible lattice **can** be projected into the frozen Edition-I basis via the pipeline's CA supplementary-projection transition formulas. The frozen basis (`atlas.json` `basis` block: `frozen:true`, `edition:1`, 14 retained dims, `axis_names` dim1 PERFORM↔DEPLOY / dim2 EMBODY↔LAUNCH) accepts supplementary points as zero-mass ghosts by construction (charter §4 step 2; renderer spec §2 amendment). Each ghost is a coordinate tuple → indicator row → projected via the MCA column-standard coordinates already computed and stored in `atlas-loadings.csv`. Ghosts have zero mass; they cannot bend the axes (decoupling law satisfied).

**⚠ Point-per-cell is infeasible at exact grain.** The exact feasible lattice is **422,445,240 cells** — far too large to project or render point-per-cell. **Per charter §4, the ghost field renders at MESO-GRAIN**: the register-rollup lattice (never-demote core) is **6,840 feasible cells** (post-cut), each projectable as one ghost point with a **per-hex depth badge** = how many exact-lattice tuples collapse into it (charter §4 step 5 — the projection is lossy; the badge is honest). 6,840 ghost points is a tractable, renderable field. Exact-lattice tuples remain **clickable-to-drill** (charter §4 step 6 — the map links back to the lattice; it never replaces it).

**The meso-grain ghost plan (recommended):**
1. Enumerate the 6,840 post-cut meso cells (this register, §2).
2. Project each as a supplementary ghost into the frozen basis (CA transition formulas).
3. Corpus kits light their meso-ghosts (map each of the 469 active kits to its meso cell).
4. Lit vs unlit = explored vs unexplored (figure-ground).
5. Per-hex depth badge = exact-tuple collapse count; clickable to the exact tuples.
6. RED-3 sealed ground: **note** that the movement-damage carve-out seals sub-regions *within* geometry-bearing cells — it renders at geometry drill-down, not on the meso plane. SEALED hatching (charter §4 step 4) at meso-grain therefore shows only logical-cut and (Matt-ratified) taste-cut ground; RED-3 hatching appears on drill-in.

**Fires AFTER Matt rules the taste slate** (charter §4 decoupling: ghosts land whenever this register lands; the register lands now, but the taste ratifications shape which ground is SEALED vs FRONTIER). The register itself is complete and committed; the ghost layer emission is the next step, gated on the taste ruling.

---

## 7. Regeneration + provenance

- **Everything regenerates** from `agentic_orchestration/research/scripts/feasibility_cuts_register_2026_07_14.py` (one command). Counts, CSV, JSON, and the corpus.db analysis tables (`atlas_feasibility_cuts_2026_07_14`, `atlas_feasibility_ladder_2026_07_14` — gitignored) all derive from the pinned coordinate cardinalities.
- **Source-anchored:** enumeration base = `coordinate-register-2026-07-13.md` §2 (RATIFIED); red-law statements = `gaps-kpis-direction-analysis.md` §A.4 (ratified as feasibility-cut class per Q28 binding (c)); active-kit count (469) = `2026-07-14-gate-report.md` Stage 0.
- **Reversible / no silent transformation:** every cut is a stated predicate; no coordinate value is destructively transformed. The raw naive box is preserved in-register (with its caveat).
- **MIGRATION note:** this register introduces `atlas_feasibility_*` analysis tables in `corpus.db` (elrond-owned, gitignored) — no schema change to any consumer table, no engine-side migration owed. Logged in `research/curated/MIGRATION.md`.

---

**Signed:** elrond (data steward) — for enumerating the feasible lattice so the atlas ghost field draws the unexplored space honestly, against a denominator that is the truth by construction, never the sample.
