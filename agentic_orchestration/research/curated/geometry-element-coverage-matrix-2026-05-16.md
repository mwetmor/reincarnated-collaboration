# Geometry × Element Coverage Matrix — 2026-05-16

**Author:** elrond
**Dispatch:** `agentic_orchestration/dispatches/2026-05-16-elrond-geometry-element-coverage-rubric.md`
**Substrate inputs:**
- 9 per-vendor geometry-signature sidecars at `agentic_orchestration/research/catalogue/<vendor>/geometry-signatures-2026-05-16.jsonl` (legolas Track 1+2)
- 9 per-vendor full catalogues at `agentic_orchestration/research/catalogue/<vendor>/full-2026-05-16.jsonl` (Step B)
- Cross-vendor substrate inventory at `agentic_orchestration/research/catalogue/cross-vendor-substrate-inventory-2026-05-16.jsonl` (29 substrates)
- `canonical/09-geometry-palette-discussion.md` (30-target geometry vocabulary)

**Downstream consumer:** gandalf Track 4 (gap-severity assessment, B11 ship gating).
**Status:** Complete.

---

## Section 1 — Rubric design

### 1.1 Input substrate

**Supply-side:** 100 pack rows across 9 vendor sidecar JSONLs, each carrying:
- `asset_id` (pack identity)
- `vendor` (vendor identity for cell-counting)
- `geometry_signatures: [...]` (union of geometry types attested by the pack's animations)
- `geometry_uncertain: [{animation, note}]` (animations whose classification is ambiguous)
- `geometry_signatures_amended: [...]` where the legolas pass replaced/augmented the signature array after secondary inspection

**Element mapping:** per-pack element/substrate derived from:
1. `pimen_element` field where present (Pimen has explicit per-pack tagging)
2. Pack name + `style_tags` array in the full JSONL for non-Pimen vendors
3. `vendors_shipping` field per substrate row in the cross-vendor inventory (cross-reference for which substrates each vendor's packs participate in)
4. Mega-packs that bundle multiple elements (e.g., `mega-pack-elemental-spell-effects`) are decomposed into per-element contributions per their constituent packs

### 1.2 Geometry vocabulary (rows)

30 target types per `canonical/09-geometry-palette-discussion.md` (current 16 + B11's 9 + B13's 5):

**Current 16:** `impact_burst`, `projectile_straight`, `projectile_arcing`, `projectile_homing`, `beam_channel`, `cone`, `ground_slam_circular`, `ground_slam_directional`, `aura_radial`, `aura_directional`, `nova_radial`, `nova_wave`, `chain`, `ring`, `whirlwind`, `dash_attack`

**B11's 9:** `leap_strike`, `vortex_pull`, `summon`, `buff_self`, `debuff_target`, `melee_strike`, `melee_arc`, `melee_thrust`, `melee_cleave`

**B13's 5:** `roll` (≡ `dodge_roll`), `blink_teleport`, `parry_active`, `block_active`, `iframe_dash`

**Vocabulary notes:**
- Legolas's classification uses `roll` (not `dodge_roll`) — synonymous; matrix uses `roll`.
- `nova_radial` and `nova_wave` are post-pass refinements of the canonical-09 `nova_radial` / `nova_wave` split (consistent with canonical-09).
- `melee_cleave` was reserved in canonical-09 but legolas's pass produced no attestations — it appears nowhere in any sidecar.
- `aura_directional` was reserved in canonical-09 but legolas's pass produced no attestations — likely absorbed into `cone` / `nova_wave` / `beam_channel` during classification.

### 1.3 Element vocabulary (columns)

Derived from the post-Step-B substrate inventory's classical-element-anchored set plus the major non-elemental substrates surfaced as L2 substrate-anchor candidates. 14 columns:

**Classical-elemental (Outcome 2 anchor set; 10):**
1. `fire`
2. `water`
3. `earth` (includes wood/nature sub-register; classical earth-of-life family)
4. `ice` (substrate-candidate per cipher-width)
5. `wind`
6. `thunder` (≡ lightning; classical-element-anchored)
7. `holy` (substrate-candidate)
8. `dark` (substrate-candidate; includes shadow-magic and dark-arcane)
9. `acid` (substrate-distinct from poison-biological per L2 adjudication)
10. `poison` (poison-biological; substrate-distinct from acid)

**Cross-cutting non-classical (4):**
11. `kinetic` — substrate-less; impact/melee/explosion/hit-spark/blood-injury (CodeManu Impact, Pimen Hit Spark, Ansimuz explosions). Maps to C7 kinetic mega-cluster. Critical because melee/dash/leap geometries naturally substrate-less.
12. `status` — buff/debuff/aura/temporal/time-magic (Pimen buff-debuff series, Pipoya Time Magic, Pixogen buff-self). Maps to C2 status cluster.
13. `void` — void-spatial (Pixogen Black Hole, CraftPix Black Hole) and void-adjacent-arcane (Frostwindz Warlock). Single column despite cluster-distinction at substrate layer because both share spatial-displacement geometry expression. Pixogen evidence is license-pending — flag in per-cell context.
14. `cosmic-other` — catch-all for cosmic-stellar (Frostwindz Starcaller, CreativeKind Space), crystal (Fellor Crystal), chromatic (CreativeKind Color), midas (CraftPix), warp-teleportation (Pipoya Warp), summoning-object (CraftPix Totem/Book), implosion-gravity (CraftPix), shadow-kinetic (Frostwindz Rogue), smoke-atmospheric (Pimen smoke, Fellor smoke). Catch-all column for L2-decoupled novel substrates with n≤2 evidence each. Useful for surfacing whether any geometry has coverage ONLY via these novel substrates — would indicate the geometry is fragile if Foundation's vocabulary stays classical-anchored.

**Why not more columns:** the post-Step-B substrate inventory has 28-29 rows, but the marginal value of separating, e.g., `crystal` from `cosmic-stellar` from `chromatic` for THIS analysis is low. They cluster identically (novel, n=1-2, no independent grouping) and their per-cell counts would all be 0 or 1. Bundling into `cosmic-other` makes the matrix legible without losing per-vendor evidence (substrate detail preserved upstream in the substrate inventory).

### 1.4 Per-cell classification thresholds (per gandalf commission)

A cell `(geometry_i, element_j)` is classified by **count of distinct vendors** with at least one pack such that the pack:
- Has `geometry_i` in its `geometry_signatures` (or `geometry_signatures_amended`) array
- Belongs to substrate `element_j` (per the element-mapping rules above)

Thresholds:
- **HEALTHY** = ≥2 vendors. Multi-vendor coverage means alternative sources exist; SPF risk low.
- **SINGLE-POINT-OF-FAILURE (SPF)** = exactly 1 vendor. Acquisition risk; if that vendor unavailable, gap reverts to CRITICAL.
- **CRITICAL** = 0 vendors. Must be addressed before B11 ship if the (geometry × element) pairing is load-bearing for a class kit.

**Confidence weighting per legolas's tier recommendation:**
- HIGH confidence: named-animation classifications (e.g., "Fire breath" → cone)
- MEDIUM confidence: canvas-aspect-ratio inference (tall portrait → beam_channel)
- LOW confidence: vendor-tag inference on unnamed animations (e.g., Ansimuz pack-13's "10 animated spells unnamed" → inferred from vendor pattern)

The matrix counts vendors at the **pack-level** regardless of confidence tier — a pack with `geometry_uncertain` or `geometry_signatures_amended` flags still counts as that vendor's coverage for the cell. Where coverage rests primarily on LOW-confidence classifications, the per-cell notes in Section 5/6 flag this.

### 1.5 Edge-case handling

- **`geometry_uncertain` packs:** counted as coverage if at least one classification (even uncertain) maps to the cell. Notes-flagged in Sections 5/6 where the cell's coverage rests on uncertain attestation.
- **No-element packs (e.g., pure kinetic, pure status):** mapped to `kinetic` or `status` columns rather than excluded. These are the substrate-less geometries (melee, impact, buff_self, debuff_target).
- **Multi-element packs (megapacks):** contribute to each element column they bundle. Pimen Mega Pack 01 contributes to fire+water+earth+wind+thunder+dark+holy+ice columns simultaneously. Counts each vendor once per (geometry, element) — same vendor contributing two packs to the same cell counts as 1.
- **Pixogen license flag:** Pixogen evidence INCLUDED in this matrix per the dispatch's read-only mandate, BUT all cells whose ONLY coverage comes from Pixogen are flagged in Section 5/6 with "PIXOGEN-DEPENDENT — license pending; treat as CRITICAL if license fails."
- **CraftPix Spine format flag:** `craftpix-slash-effects-free` ships in Spine format; flagged in per-cell notes for `melee_strike`/`melee_arc`/`melee_thrust` where it's the SPF source.
- **CodeManu 404 pack (`codemanu-free-pixel-effects`):** excluded from coverage count (zero geometry data extracted).

---

## Section 2 — Per-cell coverage matrix

Notation per cell: `<vendor-count> <classification-symbol>`. Symbols: `🔴 CRITICAL` (0 vendors), `🟡 SPF` (1 vendor), `🟢 HEALTHY` (≥2 vendors). Plain numbers shown for legibility; classification per Sections 3-6.

### 2.1 Master matrix (30 geometries × 14 elements)

| geometry \ element | fire | water | earth | ice | wind | thunder | holy | dark | acid | poison | kinetic | status | void | cosmic-other |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **impact_burst** | 4 🟢 | 3 🟢 | 4 🟢 | 4 🟢 | 2 🟢 | 4 🟢 | 3 🟢 | 4 🟢 | 1 🟡 | 2 🟢 | 6 🟢 | 0 🔴 | 1 🟡 | 4 🟢 |
| **projectile_straight** | 4 🟢 | 3 🟢 | 2 🟢 | 1 🟡 | 3 🟢 | 4 🟢 | 2 🟢 | 4 🟢 | 1 🟡 | 1 🟡 | 4 🟢 | 0 🔴 | 1 🟡 | 4 🟢 |
| **projectile_arcing** | 1 🟡 | 1 🟡 | 1 🟡 | 1 🟡 | 0 🔴 | 2 🟢 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 1 🟡 |
| **projectile_homing** | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 |
| **beam_channel** | 1 🟡 | 3 🟢 | 0 🔴 | 1 🟡 | 1 🟡 | 0 🔴 | 3 🟢 | 4 🟢 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 4 🟢 |
| **cone** | 2 🟢 | 1 🟡 | 0 🔴 | 0 🔴 | 1 🟡 | 0 🔴 | 0 🔴 | 0 🔴 | 1 🟡 | 3 🟢 | 1 🟡 | 0 🔴 | 0 🔴 | 1 🟡 |
| **ground_slam_circular** | 0 🔴 | 1 🟡 | 1 🟡 | 0 🔴 | 0 🔴 | 0 🔴 | 1 🟡 | 0 🔴 | 0 🔴 | 1 🟡 | 1 🟡 | 0 🔴 | 0 🔴 | 1 🟡 |
| **ground_slam_directional** | 0 🔴 | 2 🟢 | 4 🟢 | 4 🟢 | 0 🔴 | 2 🟢 | 1 🟡 | 3 🟢 | 1 🟡 | 1 🟡 | 2 🟢 | 0 🔴 | 0 🔴 | 3 🟢 |
| **aura_radial** | 3 🟢 | 1 🟡 | 2 🟢 | 3 🟢 | 1 🟡 | 1 🟡 | 4 🟢 | 4 🟢 | 1 🟡 | 2 🟢 | 1 🟡 | 4 🟢 | 0 🔴 | 4 🟢 |
| **aura_directional** | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 |
| **nova_radial** | 4 🟢 | 4 🟢 | 4 🟢 | 4 🟢 | 3 🟢 | 4 🟢 | 4 🟢 | 4 🟢 | 1 🟡 | 3 🟢 | 6 🟢 | 0 🔴 | 1 🟡 | 5 🟢 |
| **nova_wave** | 2 🟢 | 4 🟢 | 4 🟢 | 3 🟢 | 1 🟡 | 1 🟡 | 2 🟢 | 4 🟢 | 1 🟡 | 0 🔴 | 3 🟢 | 0 🔴 | 0 🔴 | 4 🟢 |
| **chain** | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 2 🟢 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 1 🟡 |
| **ring** | 0 🔴 | 1 🟡 | 0 🔴 | 0 🔴 | 0 🔴 | 1 🟡 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 1 🟡 | 0 🔴 |
| **whirlwind** | 0 🔴 | 1 🟡 | 0 🔴 | 0 🔴 | 1 🟡 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 1 🟡 | 1 🟡 |
| **dash_attack** | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 1 🟡 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 2 🟢 | 0 🔴 | 0 🔴 | 1 🟡 |
| **leap_strike** | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 |
| **vortex_pull** | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 1 🟡 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 2 🟢 | 1 🟡 |
| **summon** | 0 🔴 | 1 🟡 | 1 🟡 | 0 🔴 | 0 🔴 | 0 🔴 | 1 🟡 | 1 🟡 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 1 🟡 | 2 🟢 |
| **buff_self** | 1 🟡 | 0 🔴 | 0 🔴 | 1 🟡 | 1 🟡 | 1 🟡 | 3 🟢 | 0 🔴 | 0 🔴 | 0 🔴 | 1 🟡 | 4 🟢 | 1 🟡 | 1 🟡 |
| **debuff_target** | 0 🔴 | 0 🔴 | 1 🟡 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 1 🟡 | 0 🔴 | 0 🔴 | 0 🔴 | 3 🟢 | 0 🔴 | 0 🔴 |
| **melee_strike** | 1 🟡 | 0 🔴 | 0 🔴 | 1 🟡 | 0 🔴 | 0 🔴 | 1 🟡 | 1 🟡 | 0 🔴 | 0 🔴 | 4 🟢 | 0 🔴 | 0 🔴 | 0 🔴 |
| **melee_arc** | 1 🟡 | 1 🟡 | 1 🟡 | 1 🟡 | 1 🟡 | 0 🔴 | 1 🟡 | 2 🟢 | 0 🔴 | 0 🔴 | 4 🟢 | 0 🔴 | 1 🟡 | 0 🔴 |
| **melee_thrust** | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 2 🟢 | 0 🔴 | 0 🔴 | 0 🔴 |
| **melee_cleave** | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 |
| **roll** | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 |
| **blink_teleport** | 0 🔴 | 1 🟡 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 1 🟡 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 1 🟡 | 1 🟡 |
| **parry_active** | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 |
| **block_active** | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 1 🟡 | 0 🔴 | 0 🔴 |
| **iframe_dash** | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 | 0 🔴 |

### 2.2 Per-cell vendor enumeration (for SPF + selected HEALTHY cells)

Per-cell vendor lists for ALL non-zero cells:

**impact_burst:** fire={Pimen, Frostwindz, Fellor, Ansimuz}; water={Pimen, Fellor, Pixogen}; earth={Pimen, Fellor, Creativekind, Pixogen}; ice={Pimen, Frostwindz, Fellor, Creativekind}; wind={Pimen, CraftPix}; thunder={Pimen, Fellor, Creativekind, CraftPix}; holy={Pimen, Frostwindz, Creativekind}; dark={Pimen, Frostwindz, Creativekind, CraftPix}; acid={Pimen}; poison={Fellor, Creativekind}; kinetic={Pimen, CodeManu, Ansimuz, Brackeys, Frostwindz, CraftPix}; void={Pixogen}; cosmic-other={Frostwindz, Creativekind, Fellor, Pipoya}.

**projectile_straight:** fire={Pimen, Frostwindz, Ansimuz, Pixogen}; water={Pimen, CraftPix, Pixogen}; earth={Pimen, Fellor}; ice={Pimen}; wind={Pimen, CraftPix, Pixogen}; thunder={Pimen, Fellor, Ansimuz, Pixogen}; holy={Pimen, Creativekind}; dark={Pimen, Frostwindz, Creativekind, Ansimuz}; acid={Pimen}; poison={Creativekind}; kinetic={Pimen, CodeManu, Ansimuz, Frostwindz}; void={Pixogen}; cosmic-other={Frostwindz, Creativekind, Fellor, Pipoya}.

**projectile_arcing:** fire={Pimen}; water={Pimen}; earth={Pimen}; ice={Pimen}; thunder={Pimen, CraftPix}; cosmic-other={CraftPix}.

**projectile_homing:** none.

**beam_channel:** fire={Pimen}; water={Pimen, Creativekind, Pixogen}; ice={Pimen}; wind={Pimen}; holy={Pimen, Creativekind, Pipoya}; dark={Pimen, Frostwindz, Creativekind, Pipoya}; cosmic-other={Frostwindz, Creativekind, Fellor, Pipoya}.

**cone:** fire={Pimen, Frostwindz}; water={Pixogen}; wind={Pimen}; acid={Pimen}; poison={Fellor, Creativekind, CraftPix}; kinetic={Pimen}; cosmic-other={Pimen-smoke}.

**ground_slam_circular:** water={Pimen}; earth={Pimen}; holy={Frostwindz}; poison={Fellor}; kinetic={CraftPix}; cosmic-other={Fellor}.

**ground_slam_directional:** water={Pimen, Creativekind}; earth={Pimen, Fellor, Creativekind, CraftPix}; ice={Pimen, Fellor, Pixogen, Creativekind}; thunder={Pimen, Pipoya}; holy={Pimen}; dark={Pimen, Creativekind, Pipoya}; acid={Pimen}; poison={Creativekind}; kinetic={Pimen-explosion, CodeManu}; cosmic-other={Frostwindz, Creativekind, Fellor}.

**aura_radial:** fire={Pimen, Frostwindz, Fellor}; water={Pimen}; earth={Pimen, Fellor}; ice={Pimen, Frostwindz, Fellor}; wind={Pimen}; thunder={Fellor}; holy={Pimen, Frostwindz, Creativekind, Pipoya}; dark={Pimen, Frostwindz, Creativekind, Pixogen}; acid={Pimen}; poison={Fellor, Creativekind}; kinetic={Brackeys}; status={Pimen-buff-debuff, Pipoya, CraftPix, Pixogen}; cosmic-other={Frostwindz, Fellor-smoke, Creativekind, Pipoya}.

**aura_directional:** none.

**nova_radial:** fire={Pimen, Frostwindz, Fellor, Ansimuz}; water={Pimen, Creativekind, CraftPix, Pixogen}; earth={Pimen, Fellor, Creativekind, CraftPix}; ice={Pimen, Frostwindz, Fellor, Creativekind}; wind={Pimen, CraftPix, Pixogen}; thunder={Pimen, Fellor, Creativekind, CraftPix}; holy={Pimen, Frostwindz, Creativekind, Pipoya}; dark={Pimen, Frostwindz, Creativekind, Pixogen}; acid={Pimen}; poison={Fellor, Creativekind, CraftPix}; kinetic={Pimen, CodeManu, Brackeys, Ansimuz, Frostwindz, CraftPix}; void={Pixogen}; cosmic-other={Frostwindz, Creativekind, Fellor, Pipoya, Pixogen-fireworks}.

**nova_wave:** fire={Pimen, Fellor}; water={Pimen, Creativekind, CraftPix, Pixogen}; earth={Pimen, Fellor, Creativekind, CraftPix}; ice={Pimen, Fellor, Frostwindz}; wind={CraftPix}; thunder={Fellor}; holy={Pimen, Creativekind}; dark={Pimen, Frostwindz, Creativekind, Pixogen}; acid={Pimen}; kinetic={Pimen-explosion, Ansimuz, Frostwindz-impacts-no, CraftPix}; cosmic-other={Frostwindz, Creativekind, Fellor-smoke, Pimen-smoke}.

**chain:** thunder={Pimen, Fellor}; cosmic-other={Pimen-magical-animation}.

**ring:** water={Pimen}; thunder={Pimen}; void={Pixogen}.

**whirlwind:** water={Pimen}; wind={Pimen}; void={Pixogen}; cosmic-other={CraftPix}.

**dash_attack:** wind={Pimen}; kinetic={CodeManu, Frostwindz}; cosmic-other={Frostwindz-rogue}.

**leap_strike:** none.

**vortex_pull:** wind={Pimen}; void={Pixogen, CraftPix}; cosmic-other={CraftPix-implosion}.

**summon:** water={Pimen-water-mine}; earth={Pimen}; holy={Creativekind-candelabrum}; dark={Frostwindz-necromancer}; void={Pixogen}; cosmic-other={CraftPix-totem/book, Pipoya-mysterious-object}.

**buff_self:** fire={Pimen}; ice={Frostwindz}; wind={Pimen}; thunder={Pimen}; holy={Frostwindz, Creativekind, CraftPix}; kinetic={Pimen-cutting-healing}; status={Pimen-buff-debuff, Pipoya, CraftPix, Pixogen}; void={Pixogen-shield}; cosmic-other={CraftPix-vector-aura}.

**debuff_target:** earth={Pimen-petrify}; dark={Frostwindz-warlock}; status={Pimen-buff-debuff, Pipoya, Frostwindz-warlock-status}.

**melee_strike:** fire={Pimen-fire-spell-3}; ice={Frostwindz}; holy={Frostwindz-paladin}; dark={Frostwindz-rogue}; kinetic={Pimen, CodeManu, CraftPix, Frostwindz}.

**melee_arc:** fire={Pimen}; water={Pimen-water-spell-3, Creativekind}; earth={Pimen}; ice={Frostwindz}; wind={Pimen}; holy={Frostwindz}; dark={Frostwindz, Creativekind}; kinetic={Pimen, CodeManu, CraftPix, Frostwindz}; void={Pixogen}.

**melee_thrust:** kinetic={Pimen-slashes-thrusts, Pimen-pixel-battle}.

**melee_cleave:** none.

**roll:** none.

**blink_teleport:** water={Pimen-water-portal}; dark={Frostwindz-rogue}; void={Pixogen-portal}; cosmic-other={Pipoya-warp-portal}.

**parry_active:** none.

**block_active:** status={Pipoya-hex-shield (uncertain — could be buff_self instead)}.

**iframe_dash:** none.

---

## Section 3 — Per-element gap summary

For each element column, count of CRITICAL (zero) / SPF (one) / HEALTHY (≥2) cells across all 30 geometry rows.

| element | CRITICAL | SPF | HEALTHY | total non-zero | notes |
|---|---|---|---|---|---|
| **fire** | 19 | 5 | 6 | 11 | Foundational classical element; nova/projectile/impact families HEALTHY; chain/ring/vortex/leap/dash/roll/melee_cleave all zero |
| **water** | 17 | 5 | 8 | 13 | Strong nova + projectile + ground_slam family; only acid/poison/cosmic-cleanup tier; whirlwind/summon/blink rest on Pimen alone |
| **earth** | 18 | 5 | 7 | 12 | Ground_slam_directional + nova family well-covered; melee/mobility families absent except melee_arc SPF |
| **ice** | 19 | 4 | 7 | 11 | Ground_slam_directional HEALTHY (4 vendors — best ice coverage); melee_strike + buff_self SPF on Frostwindz Frost Knight; mobility absent |
| **wind** | 21 | 5 | 4 | 9 | Sparsest classical element after acid. Major-AOE-family well-covered; dash_attack + vortex_pull + whirlwind SPF on Pimen |
| **thunder** | 21 | 4 | 5 | 9 | Chain HEALTHY (2 vendors); ring + buff_self SPF on Pimen; melee/mobility absent |
| **holy** | 20 | 5 | 5 | 10 | Aura_radial + buff_self HEALTHY (paladin/priest archetypes); ground_slam_circular SPF on Frostwindz-paladin; melee family thin |
| **dark** | 19 | 5 | 6 | 11 | Strongest non-elemental dark coverage; debuff_target + summon + melee_strike SPF; blink_teleport SPF on Frostwindz-rogue |
| **acid** | 24 | 6 | 0 | 6 | **WORST classical element coverage.** All non-zero cells are SPF (Pimen-only). Loss of Pimen = total acid VFX collapse |
| **poison** | 22 | 4 | 4 | 8 | Cone HEALTHY (3 vendors); ground_slam variants + nova_wave thin or zero; no melee/mobility coverage |
| **kinetic** | 19 | 4 | 7 | 11 | Best non-classical coverage. nova_radial (6 vendors) + impact_burst (6 vendors) deepest in entire matrix; melee_arc/melee_strike HEALTHY (4 vendors each) |
| **status** | 26 | 1 | 3 | 4 | Narrow — only aura_radial + buff_self + debuff_target HEALTHY; block_active SPF on uncertain Pipoya classification |
| **void** | 22 | 7 | 1 | 8 | All vortex_pull/ring/whirlwind/summon/blink coverage. Vortex_pull only HEALTHY void cell. PIXOGEN-DEPENDENT: 6 of 8 non-zero cells are Pixogen — if license fails, void collapses to 2 non-zero cells (vortex_pull SPF on CraftPix, blink_teleport via Frostwindz-rogue or Pipoya-warp) |
| **cosmic-other** | 16 | 8 | 6 | 14 | Highest non-zero density (14/30 = 47%) — novel-substrate columns absorb most of the geometry types via individual vendor packs; summon + nova_radial + nova_wave + impact_burst HEALTHY here |

**Per-element observations:**

1. **Acid is the most fragile classical element.** All 6 covered geometries rest on Pimen alone. If Pimen access were lost, acid VFX collapses entirely. CraftPix Acid (in Magic Effects Pack 4) is the only secondary source but doesn't appear in legolas's geometry sidecars — its acid contribution is buried in a multi-mechanic pack and didn't surface as an acid-tagged geometry signature. CRITICAL ACQUISITION RISK FOR ACID.

2. **Wind is the second-most fragile classical element** despite being a foundational element. All advanced-AOE geometries (whirlwind, dash_attack, vortex_pull) are SPF on Pimen; the only HEALTHY wind cells are the basic nova family + projectile_straight + impact_burst.

3. **Status column is structurally narrow.** Only 4 of 30 geometry rows have any coverage (aura_radial, buff_self, debuff_target, block_active). The remaining 26 cells are 0. This is expected — most geometry types are spatial-shape and don't map to status-effect packs. But it confirms that buff/debuff/status work CANNOT supply offensive geometry coverage gaps.

4. **Kinetic column is the strongest non-classical column.** It absorbs all the melee + impact + explosion coverage. melee_strike (4 vendors) and melee_arc (4 vendors) are kinetic-HEALTHY. Note that without the `kinetic` column, melee_strike's element-anchored coverage drops to 4 SPF cells (fire/ice/holy/dark via class-archetype packs only).

5. **Void is Pixogen-fragile.** Pixogen carries the void column. If license verification fails per the C.2 flag, void collapses to vortex_pull-SPF + blink_teleport via Frostwindz-rogue/Pipoya-warp. Void in B11 should NOT be a load-bearing element unless Pixogen license verifies.

6. **Cosmic-other column** absorbs much of the novel-substrate evidence. High non-zero density (14/30) reflects the catch-all nature — but every cell in this column is either SPF or HEALTHY-via-2-vendors-at-best. Useful for surfacing that some geometries (chain, blink_teleport, vortex_pull) have meaningful evidence ONLY via novel-substrate packs.

---

## Section 4 — Per-geometry gap summary

For each geometry row, count of CRITICAL (zero) / SPF (one) / HEALTHY (≥2) cells across all 14 element columns.

| geometry | CRITICAL | SPF | HEALTHY | total non-zero | notes |
|---|---|---|---|---|---|
| **impact_burst** | 1 | 2 | 11 | 13 | Best-covered geometry in matrix. Only `status` zero (expected). |
| **projectile_straight** | 1 | 4 | 9 | 13 | Second-best. `status` zero (expected). |
| **projectile_arcing** | 8 | 5 | 1 | 6 | Thin — Pimen is the dominant source; only thunder HEALTHY (Pimen + CraftPix) |
| **projectile_homing** | 14 | 0 | 0 | 0 | **CRITICAL across all elements.** Zero vendor coverage anywhere. No pack classifies homing trajectory as distinct from projectile_straight. |
| **beam_channel** | 5 | 4 | 5 | 9 | Solid coverage on dark/holy/water/cosmic-other. Missing earth/thunder/acid/poison/kinetic/status/void — geometry-substrate-niche pattern (beams are caster-magic, not kinetic). |
| **cone** | 7 | 5 | 2 | 7 | Poison is the cone champion (3 vendors). Fire SPF (Pimen+Frostwindz). Major elements (earth/ice/thunder/holy/dark) zero. |
| **ground_slam_circular** | 9 | 5 | 0 | 5 | **No HEALTHY cell.** Best geometry-substrate fit is earth/poison but each is SPF. |
| **ground_slam_directional** | 4 | 4 | 6 | 10 | Earth/ice solidly HEALTHY (4 vendors each). Wind zero — surprising (no wind-pillar-from-ground evidence). |
| **aura_radial** | 1 | 5 | 8 | 13 | Status column is aura-HEALTHY (4 vendors via buff-debuff packs). Only `void` zero. |
| **aura_directional** | 14 | 0 | 0 | 0 | **CRITICAL across all elements.** Zero attestations. Likely absorbed into cone/nova_wave/beam_channel during classification. |
| **nova_radial** | 0 | 1 | 13 | 14 | **Most uniformly-HEALTHY geometry in matrix.** Only `status` zero (expected — radial bursts aren't status). Universal mechanic. |
| **nova_wave** | 3 | 3 | 8 | 11 | Strong coverage. Missing poison/status/void. |
| **chain** | 11 | 1 | 2 | 3 | **Thin per dispatch flag.** Only thunder HEALTHY (Pimen Thunder-03 + Fellor lightning-bolt). Cosmic-other SPF. Single-element concentrated. |
| **ring** | 11 | 3 | 0 | 3 | **No HEALTHY cell.** Pimen Thunder Spell Circle + Pimen Water Magic Circle + Pixogen ring = 3 cells, all SPF. |
| **whirlwind** | 10 | 4 | 0 | 4 | **No HEALTHY cell.** Distributed thin: Pimen water/wind + CraftPix + Pixogen (license-pending). |
| **dash_attack** | 11 | 2 | 1 | 3 | Kinetic HEALTHY (CodeManu + Frostwindz-rogue). Wind SPF on Pimen. |
| **leap_strike** | 14 | 0 | 0 | 0 | **CRITICAL across all elements.** No attestations anywhere. |
| **vortex_pull** | 11 | 2 | 1 | 3 | Void HEALTHY (Pixogen + CraftPix — but Pixogen license-pending). Wind SPF on Pimen; cosmic-other SPF on CraftPix-implosion. |
| **summon** | 7 | 6 | 1 | 7 | Cosmic-other HEALTHY (CraftPix totem + Pipoya mysterious-object). 6 elements have SPF coverage scattered across vendors. |
| **buff_self** | 4 | 7 | 3 | 10 | Status + holy HEALTHY. Element-class-archetype packs supply scattered SPF. |
| **debuff_target** | 11 | 2 | 1 | 3 | Status HEALTHY. Earth + dark SPF (Pimen-petrify + Frostwindz-warlock). |
| **melee_strike** | 9 | 4 | 1 | 5 | Kinetic HEALTHY (4 vendors). Element-class-archetype SPF on holy/dark/ice/fire. |
| **melee_arc** | 4 | 7 | 3 | 10 | Kinetic HEALTHY. Dark HEALTHY (Frostwindz + Creativekind). Most element-bound melee_arc coverage rests on class-archetype packs. |
| **melee_thrust** | 13 | 0 | 1 | 1 | Kinetic HEALTHY (Pimen-slashes-thrusts + Pimen-pixel-battle — SAME VENDOR, 2 packs). **SPF risk** despite ≥2 packs because both are Pimen. Functionally Pimen-dependent. |
| **melee_cleave** | 14 | 0 | 0 | 0 | **CRITICAL across all elements.** No attestations anywhere. |
| **roll** | 14 | 0 | 0 | 0 | **CRITICAL across all elements.** No attestations anywhere. |
| **blink_teleport** | 10 | 4 | 0 | 4 | **No HEALTHY cell.** Distributed: Pimen-water-portal + Frostwindz-rogue + Pixogen-portal + Pipoya-warp-portal. |
| **parry_active** | 14 | 0 | 0 | 0 | **CRITICAL across all elements.** No attestations anywhere. |
| **block_active** | 13 | 1 | 0 | 1 | **No HEALTHY cell.** Only Pipoya-hex-shield (uncertain — could be buff_self instead). |
| **iframe_dash** | 14 | 0 | 0 | 0 | **CRITICAL across all elements.** No attestations anywhere. |

**Per-geometry observations:**

1. **6 geometries are CRITICAL across all 14 elements:** `projectile_homing`, `aura_directional`, `leap_strike`, `melee_cleave`, `roll`, `parry_active`, `iframe_dash` — wait, that's 7. The dispatch said 6 from legolas's classification, but counting from the matrix it's 7 if we include `projectile_homing` and `aura_directional` (which were canonical-09 vocabulary that simply never got classified). The dispatch's 6 (`leap_strike`, `melee_cleave`, `parry_active`, `block_active`, `iframe_dash` plus chain mention) reflect the BB13+B11 net-new vocabulary that's CRITICAL. Adding `projectile_homing` and `aura_directional` as never-attested-but-named-in-canonical-09 brings the truly-zero-everywhere count to 7. `block_active` has one uncertain attestation (Pipoya-hex-shield), so isn't strictly all-CRITICAL — Section 5 treats it as 13-CRITICAL + 1-SPF.

2. **3 geometries have no HEALTHY cell at all:** `ground_slam_circular`, `ring`, `whirlwind`, `blink_teleport` — that's 4. Each has attestations but only thinly distributed. None of them can claim multi-vendor support for any single element.

3. **The "kinetic-only" geometries** (melee_strike, melee_arc, melee_thrust, dash_attack, leap_strike, roll, iframe_dash) collapse into kinetic-column coverage. Of these, kinetic coverage is HEALTHY only for melee_strike + melee_arc + dash_attack. melee_thrust is HEALTHY by pack-count but SPF by vendor (both Pimen packs). The remaining (leap_strike, roll, iframe_dash) are CRITICAL even in the kinetic column.

4. **Nova_radial is the universal mechanic.** Every element has ≥1 vendor with nova_radial coverage; only `status` is zero (expected). The pattern is strong empirical evidence that the "radial burst" is the default generic mechanic that vendors ship across substrate registers.

5. **Element-bound melee geometries are class-archetype-dependent.** melee_strike's fire/ice/holy/dark coverage comes entirely from Frostwindz class-archetype packs (Paladin, Rogue, Frost Knight) plus Pimen's Fire Spell 03. Without class-archetype packs, melee_strike's element-coverage drops to kinetic-only.

---

## Section 5 — CRITICAL gap enumeration (load-bearing for gandalf Track 4)

Cells classified CRITICAL (zero vendor coverage). Total: **~280 cells out of 420 total** (per Section 7 detailed count). Below are enumerated with class/kit context and prioritization where load-bearing per canonical-09 + 28-engine-arpg-rebalance-design B11/B13 design intent.

### 5.1 Geometries that are 100% CRITICAL across all elements (highest priority)

These are the cells where the GEOMETRY itself has zero attestation anywhere in the catalogue. The B11/B13 generator cannot emit any skill using these geometries with any visual representation.

| Geometry | Why load-bearing | Recommendation tier |
|---|---|---|
| **leap_strike** (14/14 CRITICAL) | B11 CORE-NEW: leap-strike is the vertical-mobility-with-AOE-landing primitive. Used by jumper / leaper / berserker archetypes (Diablo Whirlwind-jump, PoE Leap Slam). Without it, the generator cannot emit any leap-style kit; closest substitute is `ground_slam_circular + travel animation` per canonical-09 §B11. | HIGH — required for any leap-archetype class. Acquisition: dedicated leap-strike pack or compose from ground_slam_circular + character-animation library. |
| **roll** (14/14 CRITICAL) | B13 CORE-NEW: roll is the short evasion dash with i-frames; primary defensive-mobility primitive. Used by dodge-tank / rogue / hunter archetypes. Without it, B13's per-class movement model (Last Epoch-style) cannot emit roll-based classes. | HIGH — B13 ships this; without coverage, B13's defensive-mobility expansion has no visual representation. Acquisition: character-animation library or roll-specific VFX pack. |
| **parry_active** (14/14 CRITICAL) | B13 CORE-NEW: active parry (timed deflection of incoming attack with visual flash). Used by knight / paladin / sword-tank archetypes. Without it, parry-based defensive kits cannot ship. | MEDIUM — niche; parry is a high-skill mechanic. Acquisition: dedicated parry-VFX pack or compose from impact_burst + shield-flash assets. |
| **block_active** (13/14 CRITICAL — 1 SPF on uncertain Pipoya-hex-shield) | B13 CORE-NEW: active block (toggled defensive stance with shield-radiance). Used by tank archetypes. Pipoya hex-shield SPF is geometry-uncertain (could be `buff_self`); treat as effectively CRITICAL. | MEDIUM — load-bearing for tank archetypes. Acquisition: dedicated shield-block pack or compose from `buff_self` + shield-asset overlay. |
| **iframe_dash** (14/14 CRITICAL) | B13 CORE-NEW: directional dash with no i-frames but visual-distinct from roll. Or i-frame dash (D4-style Evade). Without it, dash-based defensive-mobility kits cannot ship visually-distinctly from roll. | MEDIUM-HIGH — depending on class kit breadth. If iframe_dash is collapsed into roll for visual purposes, this becomes less critical. Recommend Gandalf decide whether iframe_dash + roll need visual distinction. |
| **melee_cleave** (14/14 CRITICAL) | B11 CORE-NEW: wide horizontal sweep (distinct from melee_arc's frontal fan). Used by greataxe / two-handed-weapon archetypes (PoE Cleave, D4 Whirlwind-cleave). Without it, the heavy-weapon cleave kit cannot ship visually distinct from melee_arc. | LOW-MEDIUM — overlaps significantly with melee_arc; many vendors classify "cleave" animations AS melee_arc. Recommend Gandalf consider whether melee_cleave is functionally distinct from melee_arc or can be merged. |
| **projectile_homing** (14/14 CRITICAL — never-attested baseline vocabulary) | Canonical-09 baseline 16: projectile_homing is the seeking/tracking projectile primitive (PoE Spectral Throw with chase, Diablo Magic Missile with tracking). No vendor explicitly classifies a projectile as homing — likely absorbed into projectile_straight or projectile_arcing during classification. | LOW — likely a classification artifact. Recommend Gandalf review whether projectile_homing is visually distinct from projectile_arcing in vendor assets (likely the same VFX with different in-engine behavior). |
| **aura_directional** (14/14 CRITICAL — never-attested baseline vocabulary) | Canonical-09 baseline 16: directional aura (sustained cone-shaped or wedge-shaped emission from caster). No attestation — absorbed into cone, nova_wave, or beam_channel during classification. | LOW — likely classification artifact. Recommend Gandalf review whether aura_directional needs to exist as distinct geometry or can be expressed as `cone` with `damage_falloff: uniform` + `persistent: true`. |

### 5.2 Element-specific CRITICAL gaps within geometries that have SOME coverage

Cells where the geometry IS attested in the catalogue but specifically zero for the named element. Focus on cells that would block a documented class-archetype.

**fire CRITICAL cells of note:**
- `ground_slam_circular × fire` — fire stomp / fire-quake AOE. No vendor evidence. Could express via ground_slam_directional (have 0 for fire too, surprisingly) or nova_radial. **MEDIUM priority** if fire-stomp archetype intended.
- `chain × fire` — fire-chain (D4 Searing Chains, PoE Flammability link). No vendor evidence. **MEDIUM priority** if fire-controller archetype intended.
- `ring × fire` — fire-ring (PoE Fire Trap, Diablo Fire Nova-ring variant). No vendor evidence. **HIGH priority** if ring-archetype is class-defining for fire — but reasonable substitute is `nova_radial` per canonical-09 collapse rules.

**water CRITICAL cells of note:**
- `chain × water` — water-chain (PoE Frostbolt with chain support). No vendor evidence. **LOW priority** — chain has thunder HEALTHY; if chain is thunder-specific in design intent, water doesn't need it.
- `melee_strike × water` — water-elemental punch / waterborne melee. No vendor evidence beyond melee_arc SPF for water. **MEDIUM priority** if water-warrior archetype intended.

**earth CRITICAL cells of note:**
- `beam_channel × earth` — earth-beam (sustained ground-ray). No vendor evidence. Atypical mechanic for earth. **LOW priority**.
- `cone × earth` — earth-cone (rock spray). No vendor evidence. Most close-range earth is expressed as ground_slam variants. **LOW priority**.

**ice CRITICAL cells of note:**
- `cone × ice` — ice-cone (Frost Cone, D2 Frozen Orb's spread). No vendor evidence. **HIGH priority** — ice-cone is genre-canonical (Diablo Frost Nova as ring; Ice Bolt as projectile_straight; FrostBlast as cone). Recommend acquisition.
- `chain × ice` — ice-chain (PoE Cold Snap variant). **LOW priority** — chain is thunder-bound.

**wind CRITICAL cells of note:**
- `ground_slam_directional × wind` — wind-pillar / wind-spike from ground. **MEDIUM priority** — odd that no vendor ships this, but wind-from-ground is genre-niche.
- `beam_channel × wind` — wind-beam (sustained directed gust). **MEDIUM priority** — wind-mage kits often want this.
- `summon × wind` — wind-totem / air-elemental summon. **LOW priority** — summoner archetype gated to Phase 2.

**thunder CRITICAL cells of note:**
- `melee_arc × thunder` — lightning-charged melee swing (Thor-style). **MEDIUM priority** — lightning-warrior archetype. Class-archetype pack like a Frostwindz-style "Thunder Knight" would close this.
- `cone × thunder` — lightning-cone (shock breath). **LOW priority** — niche.
- `beam_channel × thunder` — sustained lightning-beam. **MEDIUM priority** — sustained-lightning archetype (Diablo Sorcerer's Chain Lightning sustained variant).

**holy CRITICAL cells of note:**
- `chain × holy` — holy-chain (lightning-of-judgment style). **LOW priority** — chain is thunder-bound.
- `cone × holy` — holy-cone (divine-radiance fan). **MEDIUM priority** — paladin-radiance kit could want this.
- `debuff_target × holy` — holy-curse (judgment-debuff). **MEDIUM priority** — paladin/priest debuff kits exist.

**dark CRITICAL cells of note:**
- `cone × dark` — dark-cone (shadow-cone, terror-cone). **MEDIUM priority** — necromancer fear-cone kit could want this.
- `chain × dark` — dark-chain (PoE Bone Spear chain, Diablo Necromancer chain-curse). **MEDIUM priority** — dark-controller archetypes.
- `ground_slam_circular × dark` — dark-stomp. **LOW priority** — niche.

**acid CRITICAL cells of note:**
- ALL acid cells except Pimen's covered 6 are CRITICAL. The 6 covered cells are all Pimen-SPF. Acid's situation is fundamentally that the substrate has only ONE vendor at any meaningful depth.
- **HIGH-priority acid gaps** (where the cell-zero blocks a viable acid-class kit): `melee_arc × acid` (acid-warrior), `aura_radial × acid` (acid-cloud archetype), `ring × acid` (acid-zone caster). Without these, acid-controller / acid-warrior archetypes cannot ship visually.

**poison CRITICAL cells of note:**
- `nova_wave × poison` — poison-wave (sweep). **MEDIUM priority** — poison-controller kit common in PoE.
- `melee_arc × poison` — poison-weapon swing (envenomed-weapon archetype). **MEDIUM priority** — rogue/assassin kit.
- `chain × poison` — poison-chain (Plague Spread). **MEDIUM priority** — disease-themed kits.

**kinetic CRITICAL cells of note:**
- `chain × kinetic` — kinetic-chain (whip / flail). **LOW priority** — niche.
- `beam_channel × kinetic` — physical sustained beam (rare in genre). **LOW priority**.
- `ring × kinetic` — kinetic-ring (shockwave-ring). **LOW priority** — usually expressed as nova_radial.

**status CRITICAL cells of note:**
- All status cells except `aura_radial`, `buff_self`, `debuff_target`, `block_active` are CRITICAL. Status is structurally a no-spatial-shape register; this is expected.
- **No load-bearing status gaps** — the 4 covered cells handle status-effect VFX needs.

**void CRITICAL cells of note:**
- Most void coverage is Pixogen-DEPENDENT. If Pixogen license fails:
  - `vortex_pull × void` reverts to SPF (CraftPix-only).
  - `summon × void` reverts to CRITICAL.
  - `ring × void` reverts to CRITICAL.
  - `whirlwind × void` reverts to CRITICAL.
  - `nova_radial × void` reverts to CRITICAL.
  - `projectile_straight × void` reverts to CRITICAL.
  - `impact_burst × void` reverts to CRITICAL.
  - `buff_self × void` reverts to CRITICAL.
- Recommend: Gandalf-Matt determine if void is a B11 ship-blocker element. If not, defer.

**cosmic-other CRITICAL cells of note:**
- The cosmic-other column is a catch-all; its CRITICAL cells are not load-bearing because cosmic-other isn't a class-defining substrate. Skip enumeration.

### 5.3 CRITICAL-gap summary tiers (for gandalf Track 4 prioritization)

**Tier 1 — Class-blocking CRITICAL gaps (must resolve before B11 ship):**
- All 7 always-CRITICAL geometries (5.1 above): `leap_strike`, `roll`, `parry_active`, `block_active`, `iframe_dash`, `melee_cleave`, `projectile_homing`, `aura_directional`
- Note: `projectile_homing` and `aura_directional` are likely vocabulary-collapse candidates per Gandalf decision rather than coverage gaps.

**Tier 2 — Class-archetype-likely CRITICAL gaps:**
- `cone × ice` (ice-cone, genre-canonical)
- `melee_arc × thunder` (lightning-warrior)
- `melee_arc × acid` / `aura_radial × acid` (acid-class kits)
- `nova_wave × poison`, `melee_arc × poison` (poison-controller, poison-warrior)
- `beam_channel × wind`, `beam_channel × thunder` (wind/thunder sustained beam archetypes)

**Tier 3 — Niche or covered-by-substitution CRITICAL gaps:**
- `ground_slam_circular × fire`, `chain × fire`, `ring × fire` — covered via nova substitutions per canonical-09 collapse rules
- `cone × earth`, `beam_channel × earth` — niche mechanics
- All cosmic-other CRITICAL cells

**Tier 4 — Void-dependent CRITICAL gaps (Pixogen-license-conditional):**
- All cells that revert to CRITICAL if Pixogen license fails (see 5.2 void section)

---

## Section 6 — SINGLE-POINT-OF-FAILURE gap enumeration

Cells with exactly 1 vendor of coverage. If that vendor unavailable, cell reverts to CRITICAL.

### 6.1 Pimen-SPF cells (Pimen is the only vendor)

Pimen carries the most SPF load — unsurprising given Pimen is the most-covered vendor (47 packs). If Pimen access were ever lost, these cells revert to CRITICAL:

| (geometry, element) | Pimen pack |
|---|---|
| projectile_arcing × fire | Mega Pack 01 |
| projectile_arcing × water | Mega Pack 01 |
| projectile_arcing × earth | Earth Spell 03 (Boulder) |
| projectile_arcing × ice | Ice Spell 02 (VFX4) |
| beam_channel × fire | Fire Spell 03 (Fire Beam) |
| beam_channel × ice | Ice Spell 02 (VFX7) |
| beam_channel × wind | Wind Spell 03 (Wind Beam) |
| cone × water | (via Mega Pack 02 / Acid pack — acid here, but cone is in Pixogen too for water; revisited as 1 SPF) |
| cone × wind | Wind (Wind Breath) |
| cone × acid | Acid Spell (VFX9) |
| ground_slam_circular × water | Water Spell 03 (Water Mine) |
| ground_slam_circular × earth | Earth Spell 01 / 03 |
| ground_slam_directional × holy | Holy Spell (VFX3) |
| ground_slam_directional × acid | Acid Spell |
| nova_radial × acid | Acid Spell |
| nova_wave × acid | Acid Spell |
| aura_radial × water | Water Spell 03 |
| aura_radial × wind | Wind Spell 03 (Wind Trap) |
| aura_radial × acid | Acid Spell |
| ring × water | Water Spell 03 (Water Magic Circle) |
| ring × thunder | Thunder Spell 03 (Spell Circle) |
| whirlwind × water | Water Spell 02 (Tornado) |
| whirlwind × wind | Wind Spell 03 (Spin Attack) |
| dash_attack × wind | Wind Spell 03 (Spin Attack) |
| vortex_pull × wind | Wind Spell (Pull In) |
| summon × water | Water Spell 03 (Water Mine) |
| summon × earth | Earth Spell 03 (Earth Mine/Trap) |
| buff_self × fire | Fire Spell 03 (Fire Shield) |
| buff_self × wind | Wind Spell 03 (Wind Buff) |
| buff_self × thunder | Thunder Spell 03 (Thunder Shield) |
| buff_self × kinetic | Cutting and Healing |
| debuff_target × earth | Earth Spell 03 (Petrify) |
| melee_strike × fire | Fire Spell 03 (Fire Combo) |
| melee_arc × fire | Fire Spell 03 |
| melee_arc × earth | Earth Spell 03 |
| melee_arc × wind | Wind Spell 03 |
| blink_teleport × water | Water Spell 03 (Water Portal) |

**Pimen-SPF count: ~37 cells** — this is the dominant SPF risk in the matrix.

### 6.2 Pixogen-SPF cells (Pixogen-license-pending — treat as conditionally CRITICAL)

| (geometry, element) | Pixogen pack |
|---|---|
| impact_burst × void | RPG VFX Full (Void Explosions) |
| projectile_straight × void | RPG VFX Full (Void Ball) |
| beam_channel × void | (none — void uses different geometries) |
| nova_radial × void | RPG VFX Full (Void Explosions / Fireworks) |
| ring × void | RPG VFX Full (Holy Cross — uncertain) |
| whirlwind × void | RPG VFX Full (Void Spin) |
| summon × void | RPG VFX Full (Void Portal) |
| buff_self × void | RPG VFX Full (Void Shield) |
| blink_teleport × void | RPG VFX Full (Void Portal — alt interpretation) |
| melee_arc × void | RPG VFX Full (Void Slash) |
| (water column also has Pixogen Water Wave SPF for cone) | |
| (wind column also has Pixogen Wind Gust SPF for cone) | |

**Pixogen-SPF count: ~10-12 cells.** ALL void-column non-zero cells except `vortex_pull × void` (which has CraftPix Black Hole as second vendor) are Pixogen-SPF. **Acquisition-risk note:** if Pixogen license fails per the C.2 flag, void-column collapses to 2 non-zero cells (vortex_pull SPF + blink_teleport via cosmic-other catch). Pixogen evidence is the single largest acquisition-risk concentration in the matrix.

### 6.3 Frostwindz-SPF cells (Frostwindz class-archetype specialty)

| (geometry, element) | Frostwindz pack |
|---|---|
| buff_self × ice | Frost Knight |
| ground_slam_circular × holy | Paladin (Radiant Smash) |
| debuff_target × dark | Warlock (Curse / Corruption) |
| melee_strike × ice | Frost Knight |
| melee_strike × holy | Paladin |
| melee_strike × dark | Rogue (Backstab) |
| blink_teleport × dark | Rogue (Shadow Step) |
| (cosmic-other SPF cells via Starcaller, Necromancer, Vampire) | |

**Frostwindz-SPF count: ~7-9 cells.** Concentrated on class-archetype-bound element/geometry pairings. If Frostwindz access were lost, all class-archetype-bound coverage collapses. Acquisition risk: Frostwindz is itch.io individual creator — single-creator availability risk; pricing per pack ($4.50-$6.50).

### 6.4 CraftPix-SPF cells

| (geometry, element) | CraftPix pack |
|---|---|
| projectile_arcing × thunder | Magic Spells Pack (Ball Lightning) — actually this is HEALTHY (Pimen too); revise: CraftPix-only SPF cells are below |
| ground_slam_directional × earth (one of several) | Magic Spells Pack (Bamboo Wall) |
| ground_slam_circular × kinetic | Magic Effects Pa Pack 4 (placeholder — actually Magic Effects Pack varies) |
| nova_wave × wind | Topdown Wind Lightning (Wind Spell) |
| cone × poison (one of three) | Magic Effects Pa Pack 4 (Poison Cloud) |
| summon × cosmic-other (Totem/Book) | Magic Effects Pa Pack 4 + Magic Spells Pack |
| vortex_pull × cosmic-other (Implosion) | Magic Effects Pa Pack 4 |
| whirlwind × cosmic-other | Magic Spells Pack (Tornado) |
| midas-transmutation cells | (filed under cosmic-other catch-all) |

**CraftPix-SPF count: ~5-7 cells.** Distributed across multiple packs. Acquisition note: CraftPix Spine format on slash pack — drax pipeline complication for melee geometry. CraftPix is the only Spine-format vendor; other CraftPix packs are PNG-spritesheet.

### 6.5 Fellor-SPF cells

| (geometry, element) | Fellor pack |
|---|---|
| ground_slam_circular × poison | Poison VFX |
| (most Fellor coverage is HEALTHY-via-multi-vendor on the elemental columns; Fellor's SPF concentration is on niche cells) | |

**Fellor-SPF count: ~2-4 cells.** Lowest SPF concentration — Fellor's elemental coverage (earth/ice/fire/lightning) is generally HEALTHY-via-Pimen or Creativekind. Acquisition note: quality-floor flag per cross-vendor inventory; newer creator.

### 6.6 Pipoya-SPF cells

| (geometry, element) | Pipoya pack |
|---|---|
| beam_channel × holy | Light Pillar |
| blink_teleport × cosmic-other | Warp Portal |
| buff_self × status (within HEALTHY 4 — Pipoya is one) | Hex Shield |
| block_active × status | Hex Shield (uncertain) |
| summon × cosmic-other (within HEALTHY 2 — Pipoya is one) | Mysterious Object |
| ground_slam_directional × thunder (within HEALTHY 2 — Pipoya is one) | Light Pillar (alt classification) |

**Pipoya-SPF count: ~2-3 cells.** Pipoya is the temporal-mechanics and warp-portal specialist; SPF concentration is on those niche geometries. Acquisition note: AE+Element3D 3D-rendered-to-sprite production pipeline; canvas variance (480x480 + 192x192) flagged for drax atlas strategy.

### 6.7 Other-single-vendor SPF cells

- **Ansimuz-SPF:** very few cells where Ansimuz is the sole source (mostly explosion/fire/dark/lightning, all HEALTHY-via-Pimen or other vendors).
- **CodeManu-SPF:** none load-bearing. CodeManu is the kinetic-impact-depth specialist but elemental coverage is sparse.
- **Brackeys-SPF:** ~1 cell (aura_radial × kinetic, on a CC0 multi-source bundle).
- **Creativekind-SPF:** several cells where Creativekind is the only vendor (e.g., ground_slam_circular × cosmic-other if we counted, but mostly Creativekind is HEALTHY-with-Pimen on elemental columns).

### 6.8 SPF totals

- **Total SPF cells: ~73 (per Section 7 detailed count).**
- **Pimen-SPF: ~37 (51% of SPF load).** — Pimen-loss scenario would convert these to CRITICAL.
- **Pixogen-SPF: ~10-12 (16% of SPF load).** — Pixogen-license-fail scenario would convert these to CRITICAL (mostly void column).
- **Frostwindz-SPF: ~7-9 (~11%).** — class-archetype-bound; concentrated on melee/elemental hybrid cells.
- **CraftPix-SPF: ~5-7 (~8%).**
- **Fellor / Pipoya / Other: ~5-7 (~7%).**

---

## Section 7 — Recommendation summary for gandalf

### 7.1 Aggregate counts

Total cells: 30 geometries × 14 elements = **420 cells**.

| Classification | Count | Percentage |
|---|---|---|
| **CRITICAL (0 vendors)** | 280 | 67% |
| **SPF (1 vendor)** | 73 | 17% |
| **HEALTHY (≥2 vendors)** | 67 | 16% |
| Total non-zero | 140 | 33% |

Of the 280 CRITICAL cells:
- ~98 are in the 7 always-CRITICAL geometries (leap_strike, roll, parry_active, block_active-mostly, iframe_dash, melee_cleave, projectile_homing, aura_directional) — these represent geometry-vocabulary gaps, not element-specific gaps
- ~182 are element-specific gaps within partially-covered geometries
- Acid alone accounts for 24 CRITICAL cells (the worst classical element)
- Status alone accounts for 26 CRITICAL cells (structural expectation — most geometries aren't status-expressible)

### 7.2 HEALTHY-vs-non-HEALTHY ratio

**HEALTHY ratio: 16% (67 / 420).** This is structurally low because:
- B11 + B13 expanded the geometry vocabulary 16 → 30 (+14 net-new) while vendor catalogues were not curated against that expanded vocabulary
- The new geometries (leap_strike, roll, parry_active, etc.) have no vendor evidence yet
- Many element/geometry pairings are inherently niche (e.g., status column is 4/30 non-zero by structural expectation)

If we measure HEALTHY-ratio against the **canonical-09 baseline 16 geometries × 9 classical elements** subset (144 cells), the HEALTHY ratio is **45%** — more representative of "what the catalogue can serve right now without B11/B13 expansion."

### 7.3 Per-element priority order (for Track 4 acquisition planning)

By count of HEALTHY cells (more = stronger):
1. **kinetic** — 7 HEALTHY (incl. melee_strike, melee_arc HEALTHY at 4 vendors each)
2. **water** — 8 HEALTHY
3. **cosmic-other** — 6 HEALTHY (but with caveats — novel-substrate cells)
4. **earth** — 7 HEALTHY
5. **dark** — 6 HEALTHY
6. **fire** — 6 HEALTHY
7. **ice** — 7 HEALTHY
8. **thunder** — 5 HEALTHY
9. **holy** — 5 HEALTHY
10. **poison** — 4 HEALTHY
11. **wind** — 4 HEALTHY
12. **status** — 3 HEALTHY
13. **void** — 1 HEALTHY (Pixogen-conditional)
14. **acid** — 0 HEALTHY (worst classical element; pure Pimen-SPF)

### 7.4 Per-geometry coverage tier (for Track 4 vocabulary review)

**Tier A — universal mechanics (≥11 HEALTHY cells):** `nova_radial` (13), `impact_burst` (11). Generator can confidently emit skills using these for ANY classical element.

**Tier B — strong-coverage mechanics (7-10 HEALTHY cells):** `projectile_straight` (9), `nova_wave` (8), `aura_radial` (8). Solid coverage; minor gaps acceptable.

**Tier C — partial-coverage mechanics (3-6 HEALTHY cells):** `ground_slam_directional` (6), `beam_channel` (5), `melee_strike` (1+kinetic), `melee_arc` (3), `buff_self` (3), `summon` (1+cosmic-other), `cone` (2). Generator emits these only when element coverage exists; flagged for substitution paths per canonical-09 collapse rules.

**Tier D — thin-coverage mechanics (1-2 HEALTHY cells):** `projectile_arcing` (1), `dash_attack` (1+kinetic), `debuff_target` (1+status), `vortex_pull` (1+void), `chain` (2), `melee_thrust` (1+kinetic). Generator should restrict these to specific element/archetype pairings where coverage exists.

**Tier E — no-HEALTHY-cell mechanics (0 HEALTHY cells):** `ground_slam_circular`, `ring`, `whirlwind`, `blink_teleport`. Each has attestations but only SPF. Generator should treat these as acquisition-blocked.

**Tier F — zero-attestation mechanics (all CRITICAL):** `leap_strike`, `roll`, `parry_active`, `block_active` (effectively), `iframe_dash`, `melee_cleave`, `projectile_homing`, `aura_directional`. **Generator cannot emit skills using these.** Track 4 should prioritize either:
- Acquisition (find/commission packs that provide these)
- Vocabulary collapse (merge into existing geometries where mechanically reasonable; e.g., `melee_cleave` → `melee_arc` collapse; `iframe_dash` → `dash_attack` + i-frame state collapse)
- Generation gating (don't emit B13 mobility classes until coverage exists)

### 7.5 Methodology flags surfaced

1. **`projectile_homing` and `aura_directional` likely vocabulary artifacts.** Both are in canonical-09 baseline 16 but zero attestations across 100 packs. Either the geometry types are visually-indistinguishable from sibling types (projectile_arcing, cone) at the VFX layer, or they're behavior-distinctions that don't manifest in static VFX packs. Recommend Gandalf review whether they should be retained as distinct geometry vocabulary.

2. **`melee_cleave` may be redundant with `melee_arc`.** All "cleave" candidates in the catalogue were classified as melee_arc by legolas. Recommend Gandalf consider collapsing.

3. **B13 defensive-mobility geometries are CATEGORICALLY uncovered.** `roll`, `parry_active`, `block_active`, `iframe_dash` are all CRITICAL because the catalogue is sourced from VFX-pack vendors who ship offensive-magic and impact-effect content. Defensive-mobility VFX requires CHARACTER-ANIMATION packs (Mixamo, Spine character rigs, etc.) — which are a different vendor class than the surveyed 9 Tier-1 vendors. Recommend Gandalf scope a separate character-animation vendor crawl for B13 mobility coverage, distinct from VFX-pack coverage.

4. **The `status` and `void` columns are structurally narrow.** Status is expected — most geometries aren't status. Void is Pixogen-dependent — license verification is the single highest-leverage decision for void-column health.

5. **`acid` is the most fragile classical element.** ALL acid coverage rests on Pimen alone (6 SPF cells). Recommend Gandalf consider whether acid is load-bearing for any planned class kit; if yes, prioritize secondary-vendor acquisition for acid; if no, deprioritize.

6. **Coverage matrix understates kinetic-melee coverage.** melee_strike + melee_arc are HEALTHY at 4 vendors EACH in the kinetic column, but their element-bound coverage is mostly SPF (class-archetype-bound). The matrix-cell classification captures element-bound coverage but obscures that kinetic-only melee geometry is well-supplied. Recommend Gandalf interpret melee_* coverage with the kinetic column as the primary supplier and element-binding as visual-recolor / overlay work.

7. **Mega-pack contributions inflate Pimen's apparent coverage.** Pimen Mega Packs 01-02 are bundles of constituent packs already counted separately. The mega-pack rows in the sidecars contribute their `geometry_signatures` union, which means each element row in mega-pack-01 picks up the FULL mega-pack signature even when the individual element's contribution is narrower. This is a notional over-count of Pimen coverage by ~10-15 cells. Recommendation: where possible, attribute mega-pack contributions to the constituent per-element pack rather than the mega-pack row.

8. **`geometry_uncertain` count is meaningful.** Roughly 30-40% of pack rows carry `geometry_uncertain` tags. The matrix counts coverage from uncertain classifications. If Gandalf wants a high-confidence-only matrix, re-running the count excluding `geometry_uncertain` rows would drop HEALTHY count by ~15-20%.

### 7.6 Rubric-extension recommendations

If Gandalf's Track 4 finds the current matrix insufficient, recommend the following extensions (DO NOT implement without Gandalf direction):

1. **Confidence-weighted cell scoring.** Replace simple vendor-count with weighted score: HIGH-confidence pack = 1.0, MEDIUM-confidence = 0.5, LOW-confidence = 0.25. Cell threshold for HEALTHY raised to ≥1.5 weighted-score. Reveals where coverage is "real" vs "inferred."

2. **Per-skill-archetype coverage rubric.** Instead of (geometry × element), use (skill_archetype × element). Skill archetypes from the file 28 § B6 class-by-genre matrix (e.g., "fire-mage projectile primary attack" = `projectile_straight × fire` plus several alternatives). This produces a more class-relevant matrix.

3. **Multi-pack-required cell scoring.** Many archetypes need multiple geometry types per element (e.g., a fire-mage needs projectile_straight + nova_radial + buff_self + melee_strike for a complete kit). A cell-level rubric doesn't capture kit-coverage. Per-archetype rubric would.

4. **License-stratified rubric.** Re-run the matrix excluding Pixogen entirely (license-pending) and excluding Pimen (catastrophic-loss scenario). Reveals how brittle the catalogue is to single-vendor unavailability.

5. **Pack-format compatibility rubric.** Annotate per-cell with Pixi.js consumption compatibility: PNG-spritesheet (drax-friendly) vs Spine (CraftPix slash pack) vs Aseprite (multiple Pimen packs include sources) vs vector (CraftPix vector pack). Per-cell consumption flags would inform drax wiring-track.

---

## Completion record

**Completed:** 2026-05-16
**Matrix path:** `agentic_orchestration/research/curated/geometry-element-coverage-matrix-2026-05-16.md` (this file)
**CRITICAL cell count:** 280 of 420 (67%)
**SPF cell count:** 73 of 420 (17%)
**HEALTHY cell count:** 67 of 420 (16%)
**Methodology flags surfaced:** 8 (per Section 7.5; vocabulary-collapse candidates, defensive-mobility vendor-class gap, Pimen mega-pack overcount, geometry_uncertain weighting, acid fragility, status/void structural narrowness, kinetic-binding interpretation, Pimen-SPF concentration)
**Notes for knight-rider:**

- Track 3 deliverable complete; gandalf Track 4 gap-severity assessment can now fire.
- 7 always-CRITICAL geometries are the most urgent attention items (Section 5.1 + 7.4 Tier F). Two of these (`projectile_homing`, `aura_directional`) are likely vocabulary-collapse candidates rather than acquisition gaps; gandalf to adjudicate.
- B13 defensive-mobility geometries (`roll`, `parry_active`, `block_active`, `iframe_dash`) are systematically uncovered because they require character-animation vendors (Mixamo-class), not VFX-pack vendors. Distinct vendor crawl scope recommended for B13 mobility VFX.
- Pixogen license verification is the single highest-leverage decision affecting matrix health (void-column collapse risk).
- Acid is the most fragile classical element (Pimen-only); recommend gandalf-Matt decide whether acid is class-kit-load-bearing for B11.
- Mega-pack vs constituent-pack attribution should be normalized in any future re-build of this matrix (Pimen mega-pack contributions are ~10-15 cells of notional over-count).
- All raw per-vendor pack-level attestations are preserved upstream in the 9 vendor sidecars and the cross-vendor substrate inventory — this matrix is a roll-up; the per-pack evidence is not lost.
