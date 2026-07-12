# Expansion census — findings (Unit A)

**Date:** 2026-07-12 · **Author:** gandalf (continuation, mechanical execution) · **Data:** `expansion-census-v1.csv` (deterministic; `expansion-census-gen.py`) · **Source:** `rdr-kit-atlas-v3.csv` canon rows only (515 rows; roster/bench excluded) joined to `roster-atlas-rebuilt-v1.csv` occupancy · **Governs:** Matt's selection principle — *"simple coverage of the count of genre kits, weighted by the longevity/lineage."* This DESCRIBES the surface; Matt selects.

> **Method note.** Buckets = 6-slot engine prefix (bc6). Negatives counted in a separate column, **never in coverage**. Occupancy joined at **bc5 (ex-commitment)** because roster commit is mostly unpinned (only K1/K7/K19 code-pinned); commit-exact matches reported in a second column. Ruled weight = `kit_count × distinct_era_count` (transparent first cut — Matt's eyeball governs; not a fancier weight). Cross-decade flag = release-year span ≥10yr across the cell's games.

---

## 1. The shape of the field

| Status (canon bc6 cells) | Cells | Reading |
|---|---|---|
| occupied-by-us | 21 | our founding roster sits on genre coverage here |
| **genre-attested, UNOCCUPIED** | **151** | **the expansion field — genre kits exist, we have none** |
| genre-negative (pure) | 10 | the genre tried and shipped duds; avoid or subvert |

**478 canon positive kits populate 182 bc6 cells.** Of those, **99 kits (21%) sit in the 21 cells we occupy**; the other **379 kits sit in 151 cells we don't touch.** That 151-cell field is the expansion target surface. 15 distinct founding kits (K1, K2, K5, K6, K7, K9c/f, K10, K11, K12, K13, K14, K15, K17, K23) do the occupying — the med/var block (K3/K16/K18/K19/K20/K21/K22/K24/K25) occupies **none of it** (see §3).

## 2. Top unoccupied genre-attested cells (by ruled weight)

Every one of these is cross-decade (17–24yr recurrence) — the genre's oldest, densest, most-lineaged coordinates, and we are absent from all of them:

| bc6 | weight | kits | eras | span | Archetype (folk-name read) |
|---|---|---|---|---|---|
| **IRMFHI** | 325 | 13 | 25 | 24yr | **Summoner / pet-master** (Hydra, Skeleton Mages, Spectre, Typhon) |
| **IRHFSI** | 322 | 14 | 23 | 23yr | **Ranged elemental nuker** (Lightning Blast, Frozen Orb, Ice Shards, Prismatic Bolt) |
| **SMMFSI** | 280 | 14 | 20 | 23yr | **Warcry / banner crusader** (Earthquake Barb, Shield Charge, Banner) †neg-shared |
| **IRMSSI** | 240 | 12 | 20 | 17yr | **Artillery caster** (Bombardment, Bladefall, Rocketeer, Devastation) †neg-shared |
| **SMMSSI** | 209 | 11 | 19 | 23yr | **STR slam** (Raekor, Leapquake, Tectonic Slam, HotA) †neg-shared |
| **IMMFHI** | 184 | 8 | 23 | 18yr | **Summoner** (Skeleton/minion necro, Pet Conjurer) |
| **WMHFSI** | 144 | 9 | 16 | 24yr | **Aura-paladin** (Auradin, Aurastacker, Roland's Sweep, Condemn) |

†neg-shared = the same bc6 also holds negative attempts (positives dominate; the cell is live but has a failure sub-region — a *tuning-risk* marker, not a veto).

**Headline:** the genre's center of mass is the **caster/summoner/slam/aura** high-tempo, flat/spike basins. Our founding roster's occupancy is strongest in the martial rows (DRHFSI archer w=520, DMHFSI dagger w=288, SMHFSI fighter w=221) and the one big caster cell we hold (IMHFSI spellsword w=198). **The expansion field is disproportionately caster-, summoner-, and aura-shaped.**

## 3. The med/var skew, now seen from the corpus side (carried from V4-r2 F2)

V4-r2 measured the roster: **10 of 25 CellDefs sit at tempo=med / amp=var.** The census confirms the genre ships that texture at **11/478 = 2.3%** — and reveals the structural consequence: **only 1 of our 21 occupied canon cells is med/var.** The med/var CellDefs don't occupy genre coverage at all — they land in the **9 roster-whitespace bc5 cells** (no canon at that bc5): `SMMVS`(K3) · `WDMVS`(K19) · `IRMVL`(K16) · `IDMVH`(K18) · `WMMVS`(K20) · `WRMVS`(K21/K22) · `WDMVH`(K24/K25) · plus `DRLSS`(K8) · `SRLSS`(K4).

So the roster splits cleanly: **genre-attested occupancy = the non-med/var kits; whitespace claims = the med/var block.** This is exactly F2's fork, now bilateral: (a) deliberate frontier signature the QD engine exists to explore, or (b) unexamined palette-flatness filler. *Census does not resolve the fork — it sharpens it. Batch-2 gauntlet fingerprints resolve it (Rule 1: uniqueness is behavioral).* Honesty flag: `DRLSS`(K8) and `SRLSS`(K4) were VOCAB (vocab-artifact zeros) in V4-r2, not true frontier — census bc5-whitespace = coordinate-absence, which V4-r2 further split into frontier (K3/K19) vs vocab-artifact (K4/K8). Do not conflate.

## 4. Mechanics cut (feeds V3 + Matt's "all mechanics if I can")

GX families attested in the corpus with **no founding-roster occupant** — candidate mechanics-adds, ordered by game-span (breadth of genre precedent):

| GX | cells | games | Reading |
|---|---|---|---|
| **GX-15** element-application hybrid | 7 | **18** | widest genre precedent of any unoccupied mechanic — every game ships it |
| **GX-05** reservation / aura toggles | 9 | 18 | *technically occupied (partial); the aura-paladin basin WMHFSI is unoccupied* |
| **GX-19** summon / turret / troop economy | 11 | **15** | pairs with the unoccupied IRMFHI/IMMFHI summoner basins — coherent gap |
| **GX-04** on-kill resource-spawn (corpse/soul) | 10 | 14 | necro economy; unoccupied |
| **GX-16** (mark/consume variant) | 4 | 11 | unoccupied |
| **GX-14** finite-ammo / consumable economy | 5 | 10 | unoccupied |
| **GX-12** stochastic ops | 2 | 12 | unoccupied |

Occupied-by-founding already: GX-01/02/03/06/07/09/10/11/17/20/21. **GX-13 (reap/possession) shows 1 cell / 2 games unoccupied — expected: it is RDR-native, so the corpus barely attests it; that "gap" is our keystone, not a hole.**

**The mechanics story aligns with the coordinate story:** the biggest unoccupied basins (summoner IRMFHI/IMMFHI, aura WMHFSI) are gated by the biggest unoccupied mechanics (GX-19 summon economy, GX-05 reservation/aura). A summoner-and-aura expansion wave would close coordinate AND mechanics coverage together — a natural pause-2 candidate cluster.

## 5. Name-lineage ≠ cell-lineage, at census scale

K17 (Necromancer Summoner) is an exact `IDLSHI` match to d2 Summonmancer — but that cell carries **1 kit, thinly**. The genre's summoner *mass* lives at `IRMFHI` (13 kits) and `IMMFHI` (8 kits), which we do not occupy. **We named a summoner and occupied a rare summoner coordinate, not the genre's dominant one.** Same divergence V4-r2 flagged per-kit (K1 slam-name vs spin-cell; K20 Hammerdin vs cross-era `WDHFSI`) — now visible as a coverage-level fact. Not a defect; a *decision surface*: do we want the iconic-name coordinate or the genre-mass coordinate? Matt rules per kit.

---

**Open items for Matt-session gandalf:** (1) the caster/summoner/aura tilt of the expansion field — is that the intended growth direction? (2) med/var fork (a vs b) still awaits batch-2 fingerprints. (3) GX-15/GX-19/GX-05 cluster as a coherent pause-2 mechanics-add. **All are ELICITOR forks — options surfaced, Matt rules. This census does not select.**
