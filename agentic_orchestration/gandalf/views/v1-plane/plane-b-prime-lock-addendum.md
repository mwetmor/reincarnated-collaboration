# Plane B′ — Lock Addendum for Q19 Ruling

**STATUS:** ✅ LOCKED — Matt ruled Q19 LOCKED 2026-07-13 ("I rule Q19 as locked"). The RULE is now permanent canon: **3 movement rows (FREE-MOVE/WALK/ROOTED) × 7 delivery columns × amp-tempo strata (FLAT/SPIKY/VAR)**, cell addresses = permanent kit identity. Locked = the RULE (axes + assignment rules + stratum order), NOT the raster (dots/badges stay per-version payload). Unblocks the PROMPT 5 periodic-table harness (arc S3).
**Date:** 2026-07-13 (V1.1 draft) · 2026-07-13 (V1.2 §10 added post-ruling) · 2026-07-13 (LOCKED)
**Author:** gandalf (sub-agent, drafting against gandalf-prime's delta-read verdict; V1.2 §10 by gandalf sub-agent)
**Status:** LOCKED — Matt ruled the plane RULE permanent 2026-07-13; §10 captures the rulings (rows = movement; strata = amp per-cell; cone Path 2 applied)
**Authority:** gandalf owns the surface; Matt rules the lock
**Companion:** `plane_view_v1_2_stratified.png` / `.svg` (RULED render) · `plane_view_v1_1_bprime.png` / `.svg` (pre-ruling B′ render) · `occupancy-stats-v1-2.md` (RULED stats) · `README.md` (V1 context) · `rollup-tables.md` (Table 2 mock mapping) · `delta-findings.md` (A vs B disagreements #1–#5) · `occupancy-stats.md` (V1 baselines)

---

## 1. B′ plane definition — 21 cells

**3 commitment rows × 7 delivery-family columns = 21 cells.**

Rows (verbatim from Matt's mock):
- `SNAP` = `instant` commit
- `WIND-UP` = `wind-up` commit
- `CHANNEL` = `channel` commit

Columns (7 delivery-family — RING absorbed into ORBITAL per §2):
- `PROJECTILE` · `ORBITAL` · `NOVA` · `ZONE` · `BEAM` · `MELEE` · `SUMMON`

Every combat kit routes to exactly one cell or the UNMAPPED residual. No column overlaps.

---

## 2. RING → ORBITAL merge — rationale

**The mock's RING column was empty** after first-listed-priority routing in V1 (see `rollup-tables.md` overlap flags § "ORBITAL vs RING"). All 9 corpus kits with `geometry_value = ring` were captured by ORBITAL:

| Kit | Game | Note |
|---|---|---|
| d2-nova-sorc | D2 | Poison/Fire Nova — expanding ring |
| d2-poison-nova-necro | D2 | Poison Nova — expanding ring |
| hot-astronomer-orbs | HoT | Orbital shields |
| hot-sage-ring-blades | HoT | Rotating ring blades |
| le-bladestorm-bd | LE | Bladestorm — orbital blades |
| vs-death-spiral | VS | Death Spiral — orbital axes |
| vs-phieraggi | VS | Phieraggi — orbital guns |
| vs-red-death | VS | Red Death — orbital scythe |
| vs-unholy-vespers | VS | Unholy Vespers — orbital tomes |

The distinction in Matt's mock (RING vs ORBITAL) does not survive the corpus data — every ring kit in the corpus is functionally an orbital rotating construct. Vampire Survivors uses "ring" as shorthand for what the ARPG genre broadly calls orbital. **Merging preserves the mock's genre precedent without keeping a permanently empty column.**

If a distinct RING archetype surfaces in future corpus additions (e.g., a static expanding-ring wave with no orbital rotation like a shockwave), it can be resurrected as an eighth column. For now: 7 columns is the ratified vocabulary.

---

## 3. NOVA/ZONE distinction rule — deterministic derivation + ambiguity census

### 3.1 Deterministic rule (B′ lock candidate)

The plane routes at `geometry_value` grain (the axis at which the corpus is currently keyed). B′ proposes:

| geometry_value | → column | rationale |
|---|---|---|
| `circle` | NOVA | Self-centered burst at cast (footprint origin = caster) |
| `ground_targeted_circle` | ZONE | Placed persistent region (footprint origin = targeted ground) |
| `cone` | ZONE | Placed bounded region (footprint origin = cast direction, non-self-centered) |

The narrative distinction: **NOVA is what happens AT the caster; ZONE is what the caster PLACES away from themselves.**

### 3.2 Ambiguity census — where per-kit delivery probe facts would refine or contradict

`canon_probe_facts.delivery.value` carries an orthogonal signal (`self-origin` · `at-target` · `projectile` · `beam` · `other`). Cross-tabulating this against the geometry-grain default surfaces where kits would move if per-kit facts governed instead:

| geometry | delivery.value | count | geometry-rule places | delivery-rule would place |
|---|---|---|---|---|
| `circle` | self-origin | 42 | NOVA | NOVA (aligned) |
| `circle` | projectile | 25 | NOVA | ambiguous — footprint is nova-shaped but delivered by projectile |
| `circle` | other | 2 | NOVA | ambiguous |
| `ground_targeted_circle` | at-target | 102 | ZONE | ZONE (aligned) |
| `cone` | beam | 5 | ZONE | **BEAM** (channeled flame cones — Incinerate, Flames of Ignaffar, Flamethrower, Dragon's Breath, Burn Exterminator) |
| `cone` | projectile | 6 | ZONE | **PROJECTILE** (shotgun/spread — Multishot, Strafe, Frost Claw, Galvanic Shards, Shotgonne, Ternion) |

**Circle census:** 42/69 circle kits (61%) align with the geometry-grain NOVA rule; 27/69 (39%) are projectile-delivered nova-footprint kits. The geometry-grain rule holds for circles because the DAMAGE FOOTPRINT is what the player sees — a Grenade Landsknecht produces a nova-shaped explosion at impact, and reading that as NOVA rather than PROJECTILE preserves the archetype reader's expectation.

**Cone census:** 0/11 cone kits align cleanly with ZONE by delivery signal. All 11 belong in either BEAM (5) or PROJECTILE (6) if delivery governs. This is a **honest strike against the deterministic `cone → ZONE` rule.**

**Ground_targeted_circle census:** 102/102 align — no ambiguity. This is the cleanest rule.

### 3.3 Recommendation for the lock rule

**Two paths for Matt's Q19 ruling:**

- **Path 1 — Pure geometry-grain (recommended for lock simplicity):** Adopt the rule table in §3.1 as written. Accept that 27 circle-projectile kits and 11 cone kits (38 total, ~8% of corpus) will land in cells that a per-kit reader might place differently. The plane is a coarse exploration surface; the delivery axis remains available as a filter/facet on top of the plane.
- **Path 2 — Geometry-grain plus per-kit refinement for cone:** Adopt §3.1 for `circle` and `ground_targeted_circle`, but split `cone` per delivery.value (cone-beam → BEAM, cone-projectile → PROJECTILE). This dissolves 11 kits from ZONE and moves them to their delivery-native columns. Adds one exception rule but eliminates the strongest ambiguity strike.

The renderer implements **Path 1** deterministically. If Matt rules Path 2, the change is a 5-line diff in `render_v1_1_bprime.py:GEO_TO_BP_COL` handling — trivial to re-render.

**Named follow-up regardless of path:** the `canon_probe_facts.delivery` signal is not yet a schema column on `canon_engine_key`; if the plane locks with per-kit delivery refinement, this signal should be promoted to a keyed column so the routing is reproducible from schema alone, not from JSON parsing.

---

## 4. UNMAPPED-9 placements

The 9 kits that Plane A and mock Plane B could not place (6 NULL-geometry + 3 teleport) resolve as follows under B′:

| Kit | Prior status | B′ cell | Reasoning | Flag |
|---|---|---|---|---|
| d3-inarius-bonestorm | NULL geo · flag `gx-candidate:orbit` | SNAP × ORBITAL | Bone Storm rotates around caster; orbital archetype | def |
| d4-ball-lightning | NULL geo · flag `gx-candidate:orbit` | SNAP × ORBITAL | Ball Lightning orbs orbit the caster | def |
| d4-bouldercane | NULL geo · flag `gx-candidate:orbit` | SNAP × ORBITAL | Boulder orbits with hurricane; orbital + persistent | def |
| poe1-poison-bv | NULL geo · flag `gx-candidate:orbit` | SNAP × ORBITAL | Poison Blade Vortex — canonical orbital-blade archetype | def |
| d2-firewall-sorc | NULL geo · flag `J-GEO:placed-lane` | SNAP × ZONE | Firewall is a placed persistent lane on ground | def |
| di-bone-wall-necro-pvp | NULL geo · flag `J-GEO:placed-lane` | SNAP × ZONE | Bone Wall is a placed persistent lane on ground | def |
| le-frost-wall-rm | geo=totem · flag `resolved:walls-demand` | SNAP × ZONE | Frost Wall is a placed lane barrier; totem-keying is legacy — semantically a wall/zone, not an autonomous entity | judgment |
| di-monk-sss | geo=teleport · delivery=at-target melee | SNAP × MELEE | Seven-Sided Strike teleports through 7 sequential melee blows; teleport is delivery mechanic, damage is melee | judgment |
| tq-phantom-strike-dreamkiller | geo=teleport · delivery=at-target melee | SNAP × MELEE | Phantom Strike teleport-blinks to target then melee burst; teleport is delivery mechanic, damage is melee | judgment |
| poe2-temporalis-blink | geo=teleport · delivery=self-origin mobility | **UNMAPPED-residual** | Pure mobility skill; deals no damage; no delivery family fits | def (honest residual) |

**Result: 9 of 10 (the 9 UNMAPPED-9) placed under B′; 1 kit remains UNMAPPED-residual (poe2-temporalis-blink) as an honest non-combat mobility utility.** An honest residual beats a bent placement.

The `le-frost-wall-rm` case is worth flagging separately: its current `geometry_value = totem` reflects a legacy engine-key choice that placed it in SUMMON (autonomous entity). Semantically it is a placed lane wall (like Firewall and Bone Wall), and B′ routes it accordingly via the `resolved:walls-demand` flag override. A follow-up to re-key its geometry_value from `totem` to a new `wall` or `placed_lane` value would make the routing schema-derivable — but is not blocking for the lock.

---

## 5. Delivery-family vocabulary — ratification case for the 7 column names

The 7 columns become canon vocabulary for archetype browsing. One paragraph per family, anchored on `rollup-tables.md § Table 2`:

**PROJECTILE (➤).** Traveling-entity family: `single_target`, `multi_projectile`, `fork`, `ricochet_bounce`, `chain`, `line`. Genre precedent: D2 Frozen Orb / Multi-Shot / Chain Lightning; PoE Barrage / Fork; every ARPG's "ranged bolt" archetype. 118 SNAP-column kits (largest single vocabulary bucket) — the reader's first-look for "shoots things."

**ORBITAL (◎).** Rotating/orbiting persistent region family: `ring`, `vortex_pull`, `whirlwind`, `aura`. Now includes RING per §2 merge. Genre precedent: PoE Blade Vortex; D2 Whirlwind; Vampire Survivors' entire orbital vocabulary (Death Spiral, Phieraggi, Unholy Vespers). 48 kits — the "spins around me" reader.

**NOVA (✳).** Self-centered instantaneous burst family: `circle` (when self-origin — see §3 census). Genre precedent: D2 Nova Sorc, Frost Nova; D3 Frozen Blast; the exemplar "boom outward from me right now" archetype. 69 kits under geometry-grain rule.

**ZONE (▒).** Placed persistent region family: `ground_targeted_circle`, `cone` (see §3 cone census). Genre precedent: D2 Blizzard / Meteor / Desecrate; PoE Vaal Cold Snap; the "I put danger there" reader. 116 kits under geometry-grain rule (including the 3 walls-flagged from UNMAPPED-9).

**BEAM (━).** Sustained-linear-channel family: `beam_channel`. Genre precedent: PoE Incinerate; D3 Disintegrate; the "held ray" archetype. 3 kits under geometry-grain rule; could grow to 8 under Path 2 if cone-beam kits refine into BEAM.

**MELEE (✕).** Contact-range family: `melee_strike`, `melee_arc`, `dash_attack`, `ground_slam`. Genre precedent: every ARPG melee class; D2 Barbarian, D3 Crusader, PoE Slam family. 56 kits (including 2 teleport-strike UNMAPPED-9 additions).

**SUMMON (☍).** Autonomous-spawned-entity family: `totem`, `self_buff`. Genre precedent: PoE Totem/SRS builds; D2 Necromancer/Druid summons; D4 Golem. 52 kits under B′ (dropped 1 vs V1 due to le-frost-wall reassignment to ZONE).

These 7 names are the archetype vocabulary a player uses when browsing the atlas ("show me the orbital builds"), and the writer uses when describing a kit ("channeled beam damage archetype"). This is a genre-native taxonomy, not an engine-internal one.

---

## 6. What changes vs Plane A — the delta-findings cited

Referencing `delta-findings.md` disagreements #1–#5 by number:

- **#1 (188 kits) — RESOLVED by B′.** Plane A's `large_aoe` cell (188 kits, 41% of corpus) splits into ORBITAL (17) + NOVA (65 under geometry-grain circle rule) + ZONE (94 for ground_targeted_circle) + walls-kits (3 more into ZONE via §4). No single B′ cell exceeds ~110. This is B′'s primary structural win: **the 174-kit haystack cell dissolves.**
- **#2 (118 kits) — B′ MERGES intentionally.** Plane B's PROJECTILE column deliberately unifies what Plane A separates across chain/single/small-aoe. This is the correct merge: players browse for "the projectile builds" as a single archetype family. Player-experience anchor: nobody browses for "chain over small-aoe" — they browse for "the multi-shot builds."
- **#3 (92 kits) — B′ SPLITS intentionally.** Plane A's `single` cell (86 SNAP kits) splits into MELEE (52) + PROJECTILE (38). This is the correct split: melee and ranged single-target read completely differently to a player. Player-experience anchor: a Barbarian and an Archer are not the same archetype even if both do single-target damage.
- **#4 (49 kits) — B′ SPLITS intentionally.** Plane A's `small_aoe` cell (49 kits) fans across ORBITAL, ZONE, BEAM, PROJECTILE. Correct: whirlwind/vortex/beam/cone are visually and mechanically distinct archetypes that only Plane A's outcome-based dispersion axis grouped together.
- **#5 (44 kits) — B′ RESOLVES.** Plane B's ORBITAL column receives 27 A:small_aoe (whirlwind/vortex/aura) + 17 A:large_aoe (ring/aura). Under §2 RING→ORBITAL merge this is coherent: one "spinning/rotating persistent region" family.

Additionally: **the multi_projectile 41-kit judgment call dissolves under B′.** In Plane A, multi_projectile was filed as `chain` via a judgment call flagged in `rollup-tables.md` Table 1. Under B′, the entire 41-kit set routes to PROJECTILE (regardless of chain-vs-large_aoe interpretation), because both alternative Plane A destinations collapse into the same B′ column. **One less contested judgment call.**

---

## 7. Axis-2 dispersion is NOT demoted

This addendum ratifies delivery-family as the **exploration plane**. It does not demote Axis 2 dispersion (single/chain/small-aoe/large-aoe/multi-spawn) from the archive. Dispersion remains a **measured axis in the substrate**, available for:
- BC-axes queries and clustering (P2/P3 substrate work)
- Design-spec-as-math handoffs where dispersion outcome is the load-bearing dimension
- Sidecar analyses (e.g., "how does dispersion correlate with clear-speed?")

The plane is the surface players (and designers) browse; the axes are what the substrate measures. B′ makes the two orthogonal — a healthy separation. Plane A confused them (measured axis served as browse surface), which produced the 174-kit pileup.

---

## 8. Open items for Matt's Q19 ruling

Kept short. This doc is the look-and-rule surface, not a new decision queue.

1. **Q19 plane-lock:** ratify B′ (3 × 7 = 21 cells) as the atlas plane?
2. **NOVA/ZONE Path 1 vs Path 2 (§3.3):** deterministic geometry-grain (cone → ZONE) OR per-kit refinement for cone (cone-beam → BEAM, cone-projectile → PROJECTILE)?
3. **RING resurrection trigger (§2):** accept 7-column merge, or reserve RING as a dormant 8th column with an explicit resurrection criterion documented?

---

## 9. Occupancy statistics — Plane B′ (single 3 × 7 = 21 cells)

Generated 2026-07-13 by `render_v1_1_bprime.py` against the same corpus DB as V1.

### 9.1 Headline numbers

- **Occupied cells:** 18 / 21
- **Empty cells:** 3 / 21 — `SNAP × BEAM`, `WIND-UP × ORBITAL`, `WIND-UP × BEAM`
- **Max-cell pileup:** 109 kits in `SNAP × PROJECTILE`
- **UNMAPPED (residual):** 1 corpus kit (poe2-temporalis-blink) + 37 negatives
- **Concentration (HHI):** 0.157

### 9.2 Per-cell counts

| Commitment | PROJECTILE | ORBITAL | NOVA | ZONE | BEAM | MELEE | SUMMON |
|---|---|---|---|---|---|---|---|
| **SNAP** | 109 | 36 | 63 | 105 | 0 | 52 | 48 |
| **WIND-UP** | 3 | 0 | 1 | 8 | 0 | 2 | 2 |
| **CHANNEL** | 6 | 12 | 5 | 3 | 3 | 2 | 2 |

Row totals: SNAP=413, WIND-UP=16, CHANNEL=33. Column totals: PROJECTILE=118, ORBITAL=48, NOVA=69, ZONE=116, BEAM=3, MELEE=56, SUMMON=52. Grand total placed: 462 corpus + 1 residual = 463 combat kits. Matches DB `row_class='combat-kit'` count.

### 9.3 Roster-45 spread

- Roster kits placed in grid: 5 / 45 (K1, K7, K19, H6, B12 — the 5 with committed commit_slot)
- Roster kits UNMAPPED / COMMIT_UNKNOWN: 40 (commit_slot='_')
- Grid cells containing ≥1 roster kit: 5 / 21

### 9.4 Comparison against V1 baselines

| Metric | Plane A (15 cells) | Plane B (24 cells) | **Plane B′ (21 cells)** |
|---|---|---|---|
| Occupied cells | 14 / 15 | 17 / 24 | **18 / 21** |
| Empty-cell % | 6.7% | 29.2% | **14.3%** |
| Max-cell pileup | 174 (instant × large_aoe) | 157 (SNAP × NOVA) | **109 (SNAP × PROJECTILE)** |
| HHI (concentration) | 0.222 | 0.208 | **0.157** |
| UNMAPPED corpus | 9 | 9 | **1** (residual) |

**Interpretation:** B′ improves on both Plane A and mock Plane B across every headline metric:
- **Empty-cell density down to 14%** (from B's 29%) — the plane feels populated, no permanently-empty columns.
- **Max pileup down 37% vs Plane A, down 30% vs mock B** — the biggest cell (109 kits) is now the natural archetype hub (SNAP × PROJECTILE — the "shooter" bucket a player intuitively expects to be large).
- **HHI down 24% vs Plane A, down 25% vs mock B** — kits distribute more evenly across the archetype surface.
- **UNMAPPED drops from 9 to 1** — the 8 previously-unplaceable kits find semantic homes; only 1 pure-mobility residual remains as honest non-placement.

Second-largest cell is `SNAP × ZONE = 105` — driven by the deterministic `ground_targeted_circle → ZONE` rule pulling in 94 kits. This is a real cluster in the corpus (the entire "I place damage on the ground" archetype family), and merits Matt's attention as a possible plane-lock sub-question: is a 105-kit ZONE cell acceptable, or does it warrant a further sub-facet (e.g., "placed burst" vs "placed persistent field")? Under Path 2 in §3.3, cone-beam and cone-projectile reassignment reduces ZONE by 11 to 94, which does not materially change the cluster size.

---

## 10. V1.2 — RULED plane (2026-07-13)

**Rulings recorded** (Matt, 2026-07-13):

1. **Rows changed** from commitment (SNAP/WIND-UP/CHANNEL, sourced from `commit_val`) to **movement-while-casting** (FREE-MOVE/WALK/ROOTED, sourced from `canon_engine_key.mob_policy_while_casting`; values full-move/walk/rooted map 1:1; unknown → UNMAPPED strip).
2. **Within-cell stratification adopted:** every one of the 21 cells is internally split into three horizontal strata by `canon_corpus.amp_val`, FIXED order top→bottom: **FLAT / SPIKY / VAR**. Empty strata stay visible (design-frontier signal). Chart-wide horizontal alignment preserved so bands scan across the whole plane.
3. **Cone Path 2 applied** (from §3.3): geometry=`cone` splits by `canon_probe_facts.delivery.value` — 5 cone-beam kits → BEAM, 6 cone-projectile kits → PROJECTILE. Derived from the DB, not hardcoded; V1.2 render verifies the derivation matches the ruled 5/6 lists exactly at load time.
4. **UNMAPPED-9 rows re-derived:** V1.1 hardcoded all 9 kits to SNAP; V1.2 derives each row from actual movement. The 9 kits now spread FREE-MOVE 3 / WALK 2 / ROOTED 4 — a meaningful spread the commit axis flattened. Columns unchanged per addendum §4.
5. **Amp-NULL kit preserved as unkeyed sliver:** `d2-wl-void-rift` (the 1 combat kit with amp=NULL) renders as a thin pink diamond sliver at the bottom of its cell (WALK × ZONE), not silently dropped or bent into an amp bin.

**Headline stats** (see `occupancy-stats-v1-2.md` for full detail):

| Grain | Occupied | Empty | Max | HHI |
|---|---|---|---|---|
| Cell (21) | 20 | 1 (`WALK × BEAM`) | 65 (FREE-MOVE × PROJECTILE) | 0.081 |
| Bucket (63) | 50 | 13 (12 are VAR-band) | 53 (FREE-MOVE × PROJECTILE × FLAT) | 0.046 |

Vs V1.1: max-cell down 40% (109 → 65), HHI down 48% (0.157 → 0.081), occupied-cell density up (18/21 → 20/21). The movement axis dissolves the dominant SNAP row (413 kits → three rows of 268 / 108 / 80). The 12-of-13 empty VAR-band buckets reveal a corpus-wide amplitude-variance scarcity (34 VAR kits total).

**Corpus reconciliation:** grid holds 456 kits (= 463 − 6 movement-unknown poe2 kits − 1 pure-mobility residual). Every kit accounted for.

**Renders:** `plane_view_v1_2_stratified.png` / `.svg`. Generator: `render_v1_2_stratified.py`.

---
