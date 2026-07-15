# Feasibility-Cuts Register — v1.1

> **STATUS:** CURRENT (load-bearing as of 2026-07-15). The enumerated feasible lattice
> (SPACE) that the atlas ghost field (charter §4) projects. **Ghosts land whenever THIS
> register lands** (decoupling law); **coverage claims use the enumerated feasible lattice,
> never the sample** (denominator law).
>
> **v1.1 supersedes v1** under the Matt-ratified Q30 amendments (2026-07-15: *"Great.
> Approved on all. Please proceed."*). v1's arithmetic was verified exact by gandalf's audit,
> but the **occupancy test** (real kits vs cut cells) falsified three predicates — v1.1 corrects
> them. The v1 artifact is retained in git as lineage.

**Author:** elrond (data steward — enumeration + register) · **Date:** 2026-07-15 (v1.1); 2026-07-14 (v1)
**Tracker item:** IV.x-b (feasibility-cuts register → atlas ghost field)
**Charter:** `canonical/reap-die-rise-engine/atlas-derivation-charter-2026-07-14.md` §2 (SPACE ≠ MAP; three ratified cut classes) + §4 (ghost field)
**Audit that drove v1.1:** `agentic_orchestration/gandalf/design-inputs/2026-07-15-feasibility-register-audit-and-taste-slate.md` (gandalf; Matt-ratified Q30a/Q30b)
**Enumeration base:** `canonical/reap-die-rise-engine/coordinate-register-2026-07-13.md` §2 — the 13-coordinate kit-identity key (element-free; 14 serialized `cell_key` slots)
**Red-law source (amended at source):** `agentic_orchestration/gandalf/design-inputs/2026-07-13-gaps-kpis-direction-analysis.md` §A.4 (RED-3′ tempo conjunct dropped)
**Machine-readable twin:** `feasibility-cuts-register-v1.1.csv` / `.json` (this dir) · **Generator:** `agentic_orchestration/research/scripts/feasibility_cuts_register_2026_07_14.py` (regenerates everything from one command)
**Governance:** gandalf audited; Matt ratified the amendments AND ruled the taste slate. Logical + red-law cuts are the ratified cut *classes*; the taste slate below is **RULED KEEP (zero cuts)**.

---

## 0. What this register is (and what it is NOT)

This register turns the raw 13-coordinate combinatorics into the **enumerated feasible lattice** — the SPACE. It is the denominator for every "we've explored X%" claim and the substrate the ghost field projects into the frozen Edition-I basis.

**A load-bearing distinction (do not conflate two lattices):**

| Lattice | Doc | Naive box | Number of record |
|---|---|---|---|
| **Kit-IDENTITY lattice** (THIS register) | `coordinate-register-2026-07-13.md` §2 — 13 coords, element-free | **900,169,200** (pre-cut naive; see caveat) | **feasible lattice = 693,146,160** (post logical L1′+L2+L3+L4″ + red-law RED-3′) |
| **Engine-native SUBSTRATE lattice** (separate object) | `substrate-coordinates.md` L0–L4 | banned bounding box **2.57×10⁹** | L4 ≈ **1.284×10⁹** |

> ⚠ **Renderer rule R2 spirit — naive-box caveat.** The 13-coord register's own raw naive
> product is **900,169,200** (≈9.0×10⁸). This is the **pre-cut naive box** — it treats all
> coordinate slots as free-independent, which fabricates incoherent cells (a control kit with
> no function; a summon with nothing summoned). **It is reported here inside the register with
> this explicit caveat; it is NEVER a coverage denominator and NEVER a surface headline.** The
> coverage denominator is the *feasible* lattice (693,146,160). — This is a **different** naive
> box from the substrate `2.57B`; the `2.57` ban in the renderer spec applies to the substrate
> object, not to this register.

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

**Raw naive product** = 3·7·3·21·3·10·5·7·3·4·3·3·2·3 = **900,169,200**. (See §0 caveat: pre-cut naive box, not a denominator.)

---

## 2. The counts ladder (v1.1)

Both grains. **Exact-lattice** = all 13 coordinates. **Meso-grain** (register rollup) = the never-demote core (`coordinate-register-2026-07-13.md` §6.1: #1 movement · #2 delivery · #5 control [treatment+function] · #8 proxy · #12 activation · #13 dependency) — the grain the charter §4 renders at.

| stage | exact-lattice | meso-grain |
|---|---|---|
| raw naive product | **900,169,200** | **11,340** |
| → post-logical (L1′ + L2 + L3 + L4″) | **740,139,120** | **10,080** |
| → post-red-law (RED-3′) | **693,146,160** | 10,080 |

**Reduction (v1.1):** logical cuts remove **~17.8%** of the naive box (160.0M cells); the one lattice-expressible red-law (RED-3′) removes a further **~5.2%** of the naive box (47.0M) — **which is ~6.4% of the post-logical survivors** (the honest framing; the v1 prose "~8.5% of the naive box" was a slip — RED-3′ is stated against post-logical survivors, not the naive box). The feasible lattice is **~77%** of the naive box.

> **What changed from v1 → v1.1 (the occupancy correction).** v1 reported feasible = 422,445,240
> (naive ≈47%). The three falsified predicates (§3, §4) were **over-cutting** — sealing inhabited
> ground. Correcting them GROWS the denominator to **693,146,160** (naive ≈77%). This is the honest
> direction: v1 was over-claiming exploration by shrinking the space. 469 active kits ≈ **6.8×10⁻⁵ %**
> of exact grain.

**Meso sealed decomposition** (the 1,260 sealed meso cells, charter §4 SEALED hatching):

| sealed by | meso cells | how |
|---|---|---|
| **L1′** (composed) | **756** | 2 incoherent tf pairs ({control,hybrid}×none) × movement 3 × delivery 7 × proxy 3 × activation 2 × dependency 3 |
| **L2** (composed, on L1′-survivors) | **504** | SUMMON × solo × 28-coherent-tf × movement 3 × activation 2 × dependency 3 |
| **total** | **1,260** | 11,340 raw − 10,080 feasible |

L3 / L4″ / RED-3′ seal **0 meso cells** — their antecedent coords (range, geometry) are demotable, not in the never-demote core. RED-3′ seals sub-regions *within* geometry-bearing cells; it renders at **geometry drill-in**, not on the meso plane (charter §4 note).

The **corpus lights 469 of these ghosts** (active combat-kit set). Coverage against the feasible lattice = 469 / 693,146,160 at exact grain; 469 distinct-key kits collapse toward far fewer occupied meso cells (the isotope collapse — occupied-meso count is the ghost-field lit measurement, §6).

---

## 3. Logical cuts — incoherent by definition (v1.1 amended)

Four cuts. Each is a predicate over coordinate values with the logical rule stated. Removed-counts are the **marginal footprint on the raw box** (cuts overlap; the ladder in §2 uses composed survivors). Meso-grain footprint given where the cut's coords are in the core.

| id | rule (predicate) | removed (exact, marginal) | removed (meso, marginal) |
|---|---|---|---|
| **L1′** treatment-function coherence | `{control,hybrid} ⟹ function≠none` (damage×function IS coherent) | 330,062,040 | 4,158 |
| **L2** summon ⟹ proxy | `delivery=SUMMON ⟹ proxy∈{light,heavy}` (SUMMON⊗solo forbidden) | 42,865,200 | 540 |
| **L3** melee-delivery range coherence | `delivery=MELEE ⟹ range≠ranged` (melee/mid/dual allowed) | 32,148,900 | 0 (range∉core) |
| **L4″** projectile-delivery range coherence | `delivery=PROJECTILE ⟹ range≠melee` (BEAM & ORBITAL spared) | 96,446,700 | 0 (range∉core) |

**L1′ — AMENDED (audit §2.A1).** The only incoherent treatment×function pairs are **`{control,hybrid}×none`** — a control/hybrid kit's function IS its identity, so `none` is incoherent for it. **`damage×(any control function)` is COHERENT** — the control-RIDER semantics: a damage primary carrying a kit-designed control rider (Frozen-Orb class) is bedrock genre. **130 living kits** prove it (damage×hard-stop 33, ×stun 26, ×hex 24, ×knockback 16, ×expose 11, ×taunt 10, ×blind 7, ×fear 3). v1's `damage⟺none` half over-formalized coord #5 and was falsified by 30% of the living corpus. **28 coherent pairs** (was 19): damage×10 + control×9 + hybrid×9.

**L2 — summon implies a proxy** (unchanged; zero referents in SUMMON⊗solo). ✅ STANDS.

**L3 — melee⊗ranged** (unchanged; zero referents). ✅ STANDS.

**L4″ — AMENDED (audit §2.A3).** Only **`PROJECTILE⊗melee`** is incoherent (a travelling payload cannot have pure-melee reach — zero referents). **BEAM and ORBITAL DROP OUT of the cut:** the occupancy test found both inhabited — `d3-arachyr-firebats` is ACTIVE at BEAM×melee (rooted point-blank channel-beam, the flamethrower archetype), and **8 active whirling-blades-class kits** sit at ORBIT×melee. Cells with living referents are not logically incoherent. `mid`/`ranged`/`dual` remain; NOVA/ZONE/MELEE/SUMMON unconstrained.

---

## 4. Red-law cuts — 3 intrinsic laws, applied WHERE HONESTLY EXPRESSIBLE (v1.1 amended)

The critical honesty rule (charter §2): **a red law that is about kit-internal design pattern and does NOT translate to a coordinate-combination predicate STAYS a generation/curation filter and is NOT applied to the lattice.** Honest disposition of all three:

| red law | lattice cut? | disposition |
|---|---|---|
| **RED-1 co-location** | **NO** | filter only — key-invisible (trail-vs-present geometry property; the 13-coord key encodes no positional coordinate) |
| **RED-2 no anti-synergy** | **NO** | filter only — key-invisible (within-kit relational property; two identical keys can differ on cannibalism) + future sim-KPI (K5/K6) |
| **RED-3′ movement-damage carve-out** | **YES** | lattice cut — coordinate-expressible |

**RED-3′ — AMENDED (audit §2.A2; law text amended at source, `gaps-kpis-direction-analysis.md` §A.4).** The tempo conjunct is **DROPPED**. The occupancy test found what separates dead from living movement kits is **COMMIT, not tempo**:

> `geometry ∈ {movement-verb geoms: dash_attack, teleport} ∧ commit ≠ instant ⟹ SEAL`

| id | rule | removed (exact, marginal) | removed (meso) |
|---|---|---|---|
| **RED-3′** movement-damage carve-out | as above | 76,204,800 | 0 (geometry∉core) |

- **All 19 living movement-verb kits are `commit=instant`** — across low/med/high tempo (d2-charger low; d3-leapquake, tq-shield-charge-conqueror med; poe1-flicker, hades1-athena-dash high). Leapquake & Shield Charge are `instant+high` and *alive* — v1's `instant∧high` consequent would have sealed 10 living kits.
- **Both intrinsic-red movement corpses are non-instant:** d2-leap-attack-barb (`commit=wind-up`) and poe1-charged-dash (`commit=channel`). Both were re-keyed `geometry` blank→`dash_attack` (corpus.db, Edition-II-bound) so the law's evidence lives inside its own predicate.
- **d4-blade-shift** (instant+high, dash) died **extrinsic-itemization** (legolas verdict — no Aspect written) — RED-3′ correctly **SPARES** it.
- **Three-way concordance:** RED-3′ seals exactly the two intrinsic-red corpses (wind-up, channel), spares the extrinsic corpse and all 19 living kits. The law text, corpus occupancy, and legolas's death-class re-crawl now agree perfectly.

**⚑ Binding caveat (RED-3′ cardinality).** The antecedent is keyed to the **movement-verb geometry class** = {`dash_attack`, `teleport`} = 2 of the ~21 abstract #4 slots (`g00`, `g01` placeholders). The cut is real and coordinate-expressible; its exact cardinality depends on which #4 slots are bound as movement-verbs — a curation ruling. If a third movement-verb geometry lands, RED-3′'s count moves (re-run trigger). RED-3′ is **not expressible at meso-grain** (geometry demotable, not in the never-demote core) — meso removes 0, correctly: the carve-out is a within-cell seal, visible only at geometry drill-in.

---

## 5. Taste slate — RULED 2026-07-15: ZERO CUTS (Matt Q30b) · kept as lineage

Per charter §2, Matt ratifies taste cuts one by one. **Matt ruled the slate 2026-07-15: ZERO taste cuts — all five candidates KEEP.** They are recorded here as **lineage** (the decision surface Matt ruled on); **nothing is sealed by taste.** Removed-counts below are the cells each candidate *would* have sealed on the post-red-law survivor lattice (693,146,160) — recorded for the devlog record of what was considered and kept, NOT applied.

| id | predicate | would-remove (post-red-law) | % survivors | ruling | why kept |
|---|---|---|---|---|---|
| **T5** hybrid-treatment plane | `treatment=hybrid` | 222,796,980 | 32.1% | **KEEP** | The engine's own ratified role taxonomy (damage/control/hybrid) makes hybrid first-class in OUR generator. The corpus is hybrid-empty → that makes it the flagship FRONTIER, not dead ground. Curation debt: define hybrid-assignment criteria before first engine-hybrid ingestion. |
| **T2** triggered + wind-up | `activation=triggered ∧ commit=wind-up` | 111,608,280 | 16.1% | **KEEP** | Double-latency parry-counter fantasy — unexplored, not dead. Genre-rare because genre engines are poor at telegraphs. |
| **T3** self-cost + heavy proxy | `economy=self-cost ∧ proxy=heavy` | 34,791,120 | 5.0% | **KEEP** | The blood-summoner — a proven signature archetype (Last Epoch Acolyte bleeds HP to sustain her army as class identity). |
| **T4** flat + low + channel | `amp=FLAT ∧ tempo=low ∧ commit=channel` | 24,801,840 | 3.6% | **KEEP** | The drain-life channel (WoW Warlock, V Rising) is iconic. "Inert as primary" is a tuning risk the balance loop prices, not an impossibility. |
| **T1** glass + rooted + channel | `defense=glass ∧ commit=channel ∧ movement=ROOTED` | 14,881,104 | 2.1% | **KEEP** | The maximal-risk contract (huge damage if you dare stand still) — a genre staple. d4-incinerate died here of D4's content mix; PoE1's rooted channels thrived. Content-mix-dependent, not intrinsically dead — the balance loop's showcase corner. |

**Meso footprint (T5 only — the sole meso-expressible candidate):** 3,240 cells (composed-on-survivors: 10,080 − 6,840). **NOT sealed** (ruled KEEP). *(The other four read non-core coords — not expressible at meso grain.)*

> **T5 slip fix (v1.1).** v1's meso T5 count was computed marginal-on-raw; v1.1 computes it
> composed-on-survivors (3,240), matching the exact-grain composition discipline.

**Consequence of ZERO taste cuts:** denominator stays **693,146,160** / meso **10,080**. SEALED ground on the ghost field = **logical (L1′+L2) + RED-3′ only**. No taste hatching.

---

## 6. Ghost-projection readiness → EMITTED (v1.1)

The surviving feasible lattice is projected into the frozen Edition-I basis via the pipeline's CA supplementary-projection transition formulas (charter §4 step 2). Each ghost is a coordinate tuple → indicator row → projected via the MCA column-standard coordinates in `atlas-loadings.csv`. Ghosts have zero mass; they cannot bend the axes (**decoupling law**).

**Rendered at MESO-GRAIN** (charter §4; exact grain 693.1M is unrenderable point-per-cell). The ghost field is:
1. **10,080 feasible meso cells** — each projected as one zero-mass ghost point.
2. **1,260 SEALED meso cells** — each tagged with its cut_id (L1′ or L2), rendered as SEALED hatching.
3. **Corpus kits light their meso-ghosts** — each of the 469 active kits mapped to its meso cell via the corpus-key → register-meso crosswalk (§6.1). Lit vs unlit = explored vs unexplored (figure-ground).
4. **Per-hex depth badge** = exact-lattice survivor count collapsing into that meso cell (the projection is lossy; the badge is honest). **Delivery-keyed:** cells with delivery ∈ {MELEE, PROJECTILE} → **55,755** each (the L3/L4″ range cut bites there); all other deliveries → **74,340**. Σ over all 10,080 = **693,146,160** exactly.
5. **RED-3′ sealed ground** renders at **geometry drill-in**, not the meso plane (charter §4 note).

Emitted into `atlas.json` `ghost_field` block (charter §4; register_ref = v1.1). See the emitter `build_atlas_json_edition1.py` and `MIGRATION.md` entry 2026-07-15.

### 6.1 Corpus-key → register-meso crosswalk (lit-mapping, documented + reversible)

The corpus `cell_key` uses the delivery-proxy vocabulary (charter §4 meso core); the register enumerates the abstract naive vocabulary. The lit-mapping applies this crosswalk (source-anchored, no silent transformation):

| register coord | corpus signal → register value |
|---|---|
| movement | `full-move`→FREE-MOVE · `walk`→WALK · `rooted`→ROOTED · `unknown`→unmapped |
| delivery | `geometry=totem`(proxy heavy/light)→**SUMMON** · `projectile`→PROJECTILE · `orbit`→ORBITAL · `beam`/`line`→BEAM · `self-origin`/`aura-pulse`→NOVA · `at-target`(non-totem)→ZONE · `other`/`blank`→unmapped |
| treatment+function | direct (damage/control/hybrid × 10). The 9 former `control×none` kits re-keyed control→damage (curation §C3) — DoT ailments are damage signatures, not control functions. |
| proxy | direct (solo/light/heavy) |
| activation | direct (active/triggered); `unknown`→unmapped |
| dependency | direct (one-shot/build→spend/apply→detonate); `unknown`→unmapped |

Kits whose meso-core carries any `unknown`/`blank`/`other` slot are **unmapped** (excluded from lighting, counted in `ghost_field.unmapped_pending_curation`) — never light a cell on ambiguous keys. After §C3, **0 kits remain function-unassignable** (the 9 control×none resolved to damage×none).

---

## 7. Regeneration + provenance

- **Everything regenerates** from `feasibility_cuts_register_2026_07_14.py` (one command). Counts, CSV, JSON, and the corpus.db analysis tables all derive from the pinned coordinate cardinalities.
- **Source-anchored:** enumeration base = `coordinate-register-2026-07-13.md` §2 (RATIFIED); red-law statements = `gaps-kpis-direction-analysis.md` §A.4 (RED-3′ amended); amendments = gandalf audit `2026-07-15-feasibility-register-audit-and-taste-slate.md` (Matt-ratified Q30a/Q30b); active-kit count (469) = `2026-07-14-gate-report.md` Stage 0.
- **Reversible / no silent transformation:** every cut is a stated predicate; no coordinate value is destructively transformed. The raw naive box is preserved in-register (with its caveat). v1 is retained in git as lineage.
- **MIGRATION note:** v1.1 refreshes the `atlas_feasibility_*` analysis tables in `corpus.db` (elrond-owned, gitignored). No schema change to any consumer table, no engine-side migration owed. Logged in `research/curated/MIGRATION.md` (2026-07-15 entry).

---

**Signed:** elrond (data steward) — for enumerating the feasible lattice so the atlas ghost field draws the unexplored space honestly, against a denominator that is the truth by construction, never the sample. v1.1 is the truth after the occupancy test: the space is larger than v1 claimed, because inhabited ground is not forbidden ground.
