# Tier-3 W2 — `fit(kit, encounter | era)` math note (math-before-code, Discipline #1)

**Author:** named-gamora sub-agent (WAVE W2 of Tier-3 Encounter-Geometry Run)
**Conductor:** gandalf RUN-CONDUCTOR · charter `agentic_orchestration/gandalf/notes/2026-07-22-tier3-encounter-geometry-run-charter.md` §4 W2
**Reads-as-math:** W1 grammar spec §7 (fit's four reads) + schema draft + derived-templates instance (L-10)
**Substrate:** corpus.db md5 `d091881d` (`agentic_orchestration/research/curated/corpus.db`) — READ-ONLY
**Engine HEAD at author:** `a57ee1f`

---

## §0 — What `fit` is, and the determinate/underdetermined split

Per W1 §7, `fit(kit, encounter | era)` reads four things:
- (i) the **family address** (§1.1): `(era, family, provenance, tier)`.
- (ii) the **MICRO verb-set** per family (§3.3 verb column / §5 derived).
- (iii) the **MESO formation topology** (§3.3).
- (iv) the **era shelf** (§1.2 — `era` is already the shelf via `era_year`).

The W2 done-predicate (charter §4) is TOTALITY: `fit` computes over **267 kits × the 4 era decks** without error. That is the join layer. It is **fully determined by the spec** — every read above is a lookup against frozen data. I compute it totally.

What the spec **underdetermines** is the SCORING: how (verb-overlap, topology-match, shelf-match) combine into a single ordering. §7 names the four reads but not the combining function. Per the charter design-authority rule, I compute the determinate join totally and propose a v0 scoring formula **EXPLICITLY FLAGGED `PROPOSAL — conductor ruling required`**, built for W3's consumer (W3 needs an ordering to pick matched SHOWCASE / matched STRESS pairs per kit).

---

## §1 — The determinate join layer (no ruling needed)

### §1.1 — Kit → family resolution (the membership read)

**Finding (reported to conductor, not fabricated):** the frozen corpus.db resolves family membership ONLY via `atlas_gateA_labels_2026_07_14` (byte-identical to `_refit_candidate_1`) — the RATIFIED tier. It covers **6 of 13 families** {TOTEM-SENTRY, TRAP-MINE, WHIRLWIND, CHANNELED-BEAM, AURA, MINION-PET}, 86 kit_ids, of which **46 are in the record-267 spine**. The charter's τ-PROPAGATED 44 + DOCKET-5 tiers are **NOT materialized as tables** in this md5. `mechanic_gap_docket.docket_family` is a DIFFERENT taxonomy (mechanic-gap families: "summoner-deferral", "stat-as-damage-substrate", …). The `gx` column (58 distinct codes on the spine; GX-02=shapeshift per docket destination) is a THIRD taxonomy, partial-overlap, not a clean 13-family membership.

**Determinate resolution (no fabrication):** `family_of(kit)` returns the gateA `group` when present (46 record kits), else `UNRESOLVED`. The fit layer computes over ALL 267 kits regardless — an UNRESOLVED kit still joins the era shelf and the BC-axis reads; only its family-address-dependent terms degrade to the era-level (documented in §2). **No kit is dropped; no membership is invented.** The 221 UNRESOLVED kits carry `family_resolution: "UNRESOLVED"` in output.

### §1.2 — Kit → era-shelf resolution (the shelf read)

`era_year` → era shelf, total over 267 (267/267 have era_year):
- 2000 → I (60) · 2013 → II (93) · 2016 → III (41) · 2024 → IV (73).

One anomaly reported: `poe1-kinetic-fusillade` has `game=poe1` but `era_year=2024` (`eras_normalized "3.20+"`) — a genuine late-PoE1 skill. It shelves to IV by era_year (the shelf key is era_year, not game). Documented, not corrected (not W2's call; the era shelf is `era_year`-driven per §1.2).

### §1.3 — The BC-axis reads (the kit's shape, the Q38 vocabulary)

The kit side and encounter side share the Q38 address space so fit can compute. The kit's fit-relevant fields, all near-total on the spine:
- `range_val` (267/267) ∈ {melee, mid, ranged, dual}
- `court` (258/267) ∈ {fire, cold, lightning, physical, chaos-poison}
- `original_element` (267/267)
- `proxy_val` (267/267) ∈ {solo, light, heavy}
- `commit_val` (265/267) ∈ {instant, wind-up, channel}
- `tempo_val` (267/267) ∈ {low, med, high}

These are the join surfaces. The encounter side binds through the W1 §6.2 join fields (`aggro_radius_m`, `leash_distance_m`, `preferred_behavior`, `skill_rotation_priority`) — but at W1 those are grammar-level (formations/verbs), not per-monster numerics (RD-1 populates monsters). So at W2 the encounter side is read at the GRAMMAR level: each era deck's `present_families`, each family's MESO formations + MICRO verbs, from the frozen W1 artifacts.

### §1.4 — The determinate join, per (kit, era-deck)

For each kit `k` and each era deck `D` (one of I/II/III/IV):
- `shelf_match(k, D)` ∈ {native, off-shelf}: native iff `era_shelf(k) == D.era`. Determinate.
- `family_present(k, D)` ∈ {present, hole, unresolved}: if `family_of(k)` resolved, `present` iff `family_of(k) ∈ D.present_families`, else `hole`; if unresolved, `unresolved`. Determinate from the W1 deck tables.
- `formations(k, D)`: the MESO formation_ids catalogued for `(family_of(k), D.era)` in W1 §3.3. Determinate (empty if hole/unresolved).
- `verbs(k, D)`: the MICRO verb-set for `family_of(k)` (era-invariant per family; verbs inherit from kit-leader, R-b2). Determinate.
- `derived_flag(k, D)`: whether `(family_of(k), D.era)` is one of the 5 RDR-NATIVE-DERIVED cells (L-10). Determinate.

This 5-tuple per (kit, deck) is the **totally-computed join**. 267 × 4 = 1068 join rows, zero ruling needed.

---

## §2 — The v0 SCORING formula — `PROPOSAL — conductor ruling required`

> **⚠ PROPOSAL — conductor ruling required. These weights are NOT spec. The spec (§7) names the four reads but not their combination. This is gamora's v0 proposal, built for the W3 consumer (matched SHOWCASE/STRESS pair selection). Never present as spec. The join layer above (§1) is determinate and needs no ruling; ONLY this scoring is proposed.**

### §2.1 — Why a scoring is needed and what shape W3 needs

W3 picks, per kit, a **matched SHOWCASE** encounter (where the kit's shape is advantaged — expect ≥X over neutral) and a **matched STRESS** encounter (where it is disadvantaged — expect ≤−X). That requires an ORDERING of encounters per kit: a scalar `fit_score(k, encounter)` so W3 can take the argmax (showcase) and argmin (stress). The scoring must be a total order per kit over the era's dealable encounters (archetype × formation).

### §2.2 — The proposed decomposition (three additive terms, each in [0,1], then weighted)

`fit_score(k, enc) = w_v · verb_affinity + w_t · topology_affinity + w_s · shelf_affinity`

with the proposed weights **`w_v = 0.50, w_t = 0.30, w_s = 0.20`** (rationale below; these are the ruling-required knobs).

**Term 1 — `verb_affinity` (w_v = 0.50): does the kit's shape counter or feed the encounter's MICRO pressure?**
The MICRO verb is what the pack DOES to the player. A kit's fit is highest when its shape is the natural answer to that pressure and lowest when the pressure exploits the kit's shape. Proposed mapping (per encounter's dominant verb-class → kit BC-axis advantage):
- `stack-and-retreat` (DoT field) → favors `range=ranged/dual` + `commit=instant` (can damage from outside the field, no channel-lock in the field). Penalizes `range=melee` + `commit=channel`.
- `swarm-the-brawl` (melee surround) → favors `proxy=heavy/light` (bodies to absorb) + AoE geometry (`amp=var`/wide). Penalizes `proxy=solo` + single-target.
- `channel-lanes` (beam) → favors `range=melee/mid` mobility (close the caster) + `commit=instant`. Penalizes `commit=channel` (rooted in the beam).
- `fan` (volley) → favors `range=ranged` (out-range the fan) OR `proxy=heavy` (screen). Penalizes `range=melee` solo.
- `spin-and-close` (whirlwind) → favors `range=ranged/dual` (kite the spin) + `tempo=high`. Penalizes `range=melee` + `tempo=low`.
- `emplace-and-hold` (totem) → favors burst/`amp=spiky` (delete the anchor) + `range=ranged`. Penalizes sustained-only.
- `pre-seed` (trap) → favors `tempo=high` mobility + `proxy=heavy` (sacrificial bodies). Penalizes `commit=channel` (can't reposition off mines).
- `form-transition` (shapeshift) → neutral baseline (the transform is the pressure; no clean BC-axis counter). 0.5.
- `bounce-and-chain` → favors `proxy=solo` (fewer bounce targets) + `range=ranged`. Penalizes `proxy=heavy` (chain amplifiers).
- `aura-enable` → favors burst/`amp=spiky` (delete the carrier). Penalizes sustained.
- `dash-and-strike` → favors `range=melee` (trade) + `tempo=high`. Penalizes `range=ranged` solo (kited-back-onto).

Each maps to a `verb_affinity ∈ [0,1]` via a small favor/penalize table (favor = 1.0, neutral = 0.5, penalize = 0.0; multiple axes averaged). PROPOSAL — the specific favor/penalize assignments above are the design content requiring the ruling.

**Term 2 — `topology_affinity` (w_t = 0.30): does the kit's delivery geometry match the MESO formation's spatial demand?**
Formation geometry (from §3.3) has a spatial signature; the kit's `range_val` + geometry (from `geo_raw`/court) matches or mismatches:
- Corridor/lane formations (`cbn_corridor_arc`, `cb_lane_hold`, chokepoint) → favor `range=ranged` line-geometry (`beam`/`bolt`), penalize `range=melee` (funneled).
- Converge/swarm formations (`ww_converge_spin`, `ms_swarm_surround`) → favor AoE/`amp=var` wide geometry, penalize single-target line.
- Emplaced/anchor formations (`ts_anchor_screen`, `aura_matron_center`) → favor `range=ranged` burst (reach the anchor), penalize `range=melee` (screened off).
- Field/nest formations (`da_field_retreat`, `tm_ritual_minefield`, `ts_environmental_nest`) → favor `tempo=high` mobility + `range=ranged`, penalize `commit=channel`.
Mapped to `topology_affinity ∈ [0,1]` by the same favor/neutral/penalize table.

**Term 3 — `shelf_affinity` (w_s = 0.20): is the kit native to the encounter's era?**
- native (kit's era_shelf == deck era): **1.0**.
- off-shelf but family present (RDR-derived or traveling-kin-eligible): **0.5**.
- off-shelf and family is a hole: **0.0** (the kit's family does not live in this era's hostile deck).
This is the lightest term (w_s=0.20) because the anachronism is deliberately allowed for kin (T3-V4); shelf-nativity should nudge, not dominate.

### §2.3 — Degradation for UNRESOLVED-family kits (determinate, not proposed)

For the 221 UNRESOLVED kits, `verb_affinity` and `topology_affinity` have no family to key on. They degrade to the **era-level neutral 0.5** (the kit still gets a shelf_affinity from era_year). Output flags `scoring_basis: "era_only_unresolved_family"` so W3 knows these carry only the shelf term at full confidence. This is a DETERMINATE fallback (no invented family), reported as a coverage limit, not a design choice.

### §2.4 — Why these weights (the ruling-required rationale)

- `w_v = 0.50` dominant: the MICRO verb is the moment-to-moment pressure; the design's whole thesis (§0) is "what the pack DOES to you." The counter/feed relationship is the strongest fit signal.
- `w_t = 0.30`: formation geometry is real but secondary — it modulates the verb (a beam in a corridor is worse than a beam in the open) rather than defining the encounter.
- `w_s = 0.20`: era-nativity is a nudge; the traveling-kin exemption (T3-V4) deliberately breaks strict era-purity, so shelf cannot dominate.
- These sum to 1.0 so `fit_score ∈ [0,1]`, giving W3 a clean per-kit ordering. **The ruling the conductor owns: accept 0.50/0.30/0.20, or re-weight (e.g. if W3's showcase/stress separation is too weak, raise w_v; if era-personality should bind harder, raise w_s).**

### §2.5 — Confidence carry (§8 obligation)

Fit records SOURCED FROM MEDIUM-confidence W1 elements carry MEDIUM. Concretely: any (kit, deck) whose formation/verb read draws on an Age-II row 17–18 element or an Age-IV LE row (all 9) inherits `confidence: MEDIUM` + the staleness note. HIGH otherwise. The confidence is a per-join-row tag, propagated from the W1 formation_catalogue entry's `confidence`.

---

## §3 — Totality guarantee (the W2 predicate)

`fit` computes over 267 × 4 = **1068 join rows without error**. Every kit shelves (era_year total). Every kit either resolves a family (46) or degrades cleanly to era-level (221) — no exceptions thrown, no kit dropped. The scoring is defined on every row (UNRESOLVED → 0.5 neutral verb/topology + real shelf). **Totality is structural, not sampled.**

---

## §4 — Scenario-set math (Phase c)

The sim scenarios are the MESO/MICRO grammar rendered in the LIVE harness (HEAD `a57ee1f`). Per the PROBE-4 findings (separate report), the four strain formations split CAN-EXPRESS / PARTIAL / CANNOT. The scenario set covers: the probe-4 (where expressible) + representative coverage of the §3.3 catalogue's 11 families via the registered arena scenarios (`SCENARIO_OPEN_ARENA`, `SCENARIO_CHOKEPOINT`, `SCENARIO_MAGIC_PACK`, `SCENARIO_DENSE_CELL`, `SCENARIO_ESCAPE_LANE`, `SCENARIO_OVERRUN`, boss/add shells) mapped to formation classes. Holes stay holes: a formation the harness CANNOT express is recorded as could-not-run with the specific missing capability, routed to Lane-2 as a red-flag (T3-V7), never faked.

**Math-before-code satisfied. Implementation follows this note.**
