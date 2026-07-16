# Feasibility-Cuts Register — v1.3

> **STATUS:** CURRENT (load-bearing as of 2026-07-15). The enumerated feasible lattice
> (SPACE) that the atlas ghost field (charter §4) projects — **Edition-III**. v1.3 supersedes
> v1.2 for the CENSUS-POPULATION record; the **feasible-lattice denominators are byte-identical
> to v1.2** (the lattice did not move — the census did).
>
> **v1.3 supersedes v1.2** under Matt's Edition-III one-batch directive (2026-07-15: *"Edition 3:
> one batch"*). The Edition-III batch curated **+65 corpus rows** (Stage A pull-7 re-insertion +
> Stage B Lost Ark 58 at class-engraving grain). Those rows use **only existing coordinate
> values** — no new function level, no new delivery, no new geometry, nothing new in the
> enumeration base. `pull` already entered at v1.2 (Edition-II). Therefore the enumeration base,
> the cut ledger (L1′/L2/L3/L4″/RED-3′ + taste-KEEP), and the feasible-lattice denominators are
> **UNCHANGED**; v1.3 records the census population against the frozen lattice.

**Author:** elrond (data steward — enumeration + register) · **Date:** 2026-07-15 (v1.3)
**Tracker item:** IV.x-b (feasibility-cuts register → atlas ghost field) — Edition-III
**Charter:** `canonical/reap-die-rise-engine/atlas-derivation-charter-2026-07-14.md` §2 + §4 + §6 (Edition law: frozen frame, versioned occupancy)
**Commission:** `agentic_orchestration/gandalf/briefs/2026-07-15-elrond-edition3-one-batch-commission.md` §3
**Predecessor:** `feasibility-cuts-register-v1.2.md` (Edition-II — the `pull` vocabulary; retained as lineage)
**Machine-readable twin:** `feasibility-cuts-register-v1.3.csv` / `.json` (this dir) · **Generator:** `feasibility_cuts_register_v1_3_2026_07_15.py`
**Governance:** gandalf audit-grade verify (Edition-III commission §5).

---

## 0. What changed v1.2 → v1.3 (and what did NOT)

**The load-bearing property of v1.3:** the LATTICE is frozen; the CENSUS grew. This is exactly the
charter §6 "frozen frame, versioned occupancy" law, applied at Edition scale.

| | v1.2 (Edition-II) | v1.3 (Edition-III) | changed? |
|---|---|---|---|
| enumeration base (coordinate cardinalities) | 13 coords + `pull` (fn=11) | **identical** | **NO** |
| cut ledger (L1′/L2/L3/L4″/RED-3′ + taste-KEEP) | ratified | **identical** | **NO** |
| exact feasible lattice | 767,411,820 | **767,411,820** | **NO** (byte-identical) |
| meso feasible / sealed | 11,160 / 1,314 | **11,160 / 1,314** | **NO** |
| pull slice (meso) | 1,080 feasible + 54 sealed | **1,080 + 54** | **NO** |
| corpus census | 644 rows | **709 rows** (+65) | **YES** |
| occupied meso cells (lit) | 193 | **202** (+9) | **YES** |
| pull-lit meso cells | 2 | **4** (+2) | **YES** |
| new-law-needed / HALT | 0 / False | **0 / False** | (still false) |

**Why NO new law (and no HALT).** LA class-engraving rows are pure occupancy against the frozen
lattice — every row lands in a cell that already exists in the v1.2 enumeration. No coordinate
value was added, so no cut predicate changed, so no new law is possible. Had ANY row required a new
coordinate value or landed a lit cell on a sealed cell, this register would **HALT to Matt** (the
v1.2 discipline). It does not: `new_law_needed = 0`, `halt = False`, asserted in-generator.

**Denominator NON-supersession.** Because the lattice did not move, v1.2's denominators are NOT
superseded strings at v1.3 — they are the SAME numbers, re-asserted (independently re-derived from
first principles in the generator, matching the Edition-II acceptance criterion 22). This differs
from the v1.1→v1.2 bump, which grew function 10→11 and DID supersede 693,146,160 / 10,080. The
Edition-I strings 693,146,160 / 10,080 remain **labeled-lineage-only**; the anti-`422,445,240` law
carries forward unchanged.

---

## 1. The counts ladder (v1.3 — byte-identical to v1.2)

Both grains, independently re-derived from first principles (the enumeration base is UNCHANGED):

| stage | exact-lattice | meso-grain |
|---|---|---|
| raw naive product | **990,186,120** | **12,474** |
| → post-logical (L1′ + L2 + L3 + L4″) | **819,439,740** | **11,160** |
| → post-red-law (RED-3′) | **767,411,820** | 11,160 |

**Meso sealed decomposition:** L1′ 756 + L2 558 = **1,314** (identical to v1.2). The feasible
lattice is the denominator for every coverage claim (denominator law: the sample is never its own
denominator).

---

## 2. The pull slice (v1.3 — re-vet under the larger census)

The pull-slice LATTICE is frozen at v1.2's values (1,080 feasible + 54 sealed, all L2). v1.3 re-vets
it under the LARGER census:

| pull-slice (meso) | count | seal cause |
|---|---|---|
| feasible | **1,080** | — |
| sealed | **54** | L2 (SUMMON × solo × pull) |
| **lit pull cells (post-batch)** | **4** | census — see §3 |

**Re-vet result:** every one of the 4 lit pull cells is a FEASIBLE pull cell (none lands on a
sealed cell); `new_law_needed = 0`; `halt = False`. The 2 new pull-lit cells (vs Edition-II's 2)
are:
- `[ROOTED, ZONE, damage, pull, solo, active, build→spend]` — lit by the Destroyer engraving-grain
  pull carriers (`la-destroyer-rage-hammer`, `la-destroyer-gravity-training`; `at-target`→ZONE) +
  `la-destroyer-gravity-impact` (skill-grain rows that map ZONE).
- `[ROOTED, ZONE, damage, pull, solo, active, one-shot]` — lit by `d3-wizard-black-hole`
  (`rooted|at-target`→ZONE|…|one-shot).

The Edition-II pull-lit pair persists: `[FREE-MOVE, ZONE, damage, pull, …, one-shot]` (`d3-zbarb`)
+ `[WALK, NOVA, control, pull, …, one-shot]` (`di-cyclone-monk-pvp`).

---

## 3. Census population (the ONLY v1.3 delta)

| metric | pre-batch (644) | post-batch (709) | delta |
|---|---|---|---|
| corpus rows | 644 | **709** | +65 (7 pull-tranche + 58 LA) |
| active combat-kit (cell_key non-null) | 563 | **628** | +65 |
| occupied meso cells (lit) | 193 | **202** | +9 |
| pull-lit meso cells | 2 | **4** | +2 |
| unmapped-pending-curation | 108 | **114** | +6 |

**The +6 unmapped (documented, NOT keying errors):**
- **1 honest-NULL movement** — `d4-spiritborn-vortex`: source movement is undocumented (tranche:
  *"unknown (not documented in available sources)"*) → `mob=blank` (never-invent). Cell will not
  light on the movement gate until a movement value is sourced.
- **5 MELEE-collapse** — `delivery=melee` has NO meso ghost image (the `fit2reg_delivery` crosswalk
  has no `melee` image; documented in the pull-tranche insert script + the MCD re-run): the 4
  skill-grain Destroyer rows (`vortex-gravity`, `gravity-impact`, `gravity-force`,
  `gravity-compression`) + `di-cyclone-strike-monk-base`. This is the structural reality of pull's
  genre expression (melee gravity-hammers) — surfaced, not papered. Their ENGRAVING-grain siblings
  (`at-target`→ZONE) DO light, which is why pull-lit went 2→4.

**Isotope collapse (LA class-engraving grain).** The 58 LA rows occupy **~43 distinct cell_keys**
(34 singleton + 6 doubles + 1 triple + 1 quad + 1 quint). This is the expected element-free-key
collapse (register §2): LA class identities that share the same 14-coordinate abstract signature
(differing only in element/flavor/numbers, which the identity key excludes) legitimately co-inhabit
one atlas cell. **All 58 rows persist as distinct kit_ids with full provenance** (raw_json,
mech_note); the atlas cell carries the multiplicity as `kit_count`. Same-cell coexistence at atlas
grain is legitimate — the collapse is a truth about the genre's behavioral clustering, not a keying
loss (flag-c verdict, Stage-B log §3).

---

## 4. Re-keys forced on existing rows

**NONE.** The Edition-III batch is purely additive at the census level. The 469 frozen survivors +
the Stage-A 7 rows are byte-identical before and after Stage B (asserted in-generator). The LA
Destroyer engraving-grain rows CROSS-REFERENCE the skill-grain pull-tranche rows but do not
contradict them (tranche index: *"No contradiction; enrichment"*), so no existing row's evidence
changed. The Edition-II Stage-3 re-keys (`d3-zbarb`, `di-cyclone-monk-pvp` → `function=pull`) stand
unchanged. No C3-style re-key is owed by this batch.

---

## 5. Schema + provenance

- **Schema change: NONE.** The batch works inside the existing corpus schema. The v1.3 register
  adds one additive analysis table (`atlas_feasibility_ladder_v1_3_2026_07_15`) to corpus.db
  (elrond-owned, gitignored) — no schema change to any consumer table, no engine-side migration
  owed. Logged in `research/curated/MIGRATION.md` (Edition-III entry).
- **Source-anchored:** enumeration base = `coordinate-register-2026-07-13.md` §2 + `pull`
  (Edition-II, UNCHANGED); census = current corpus post-Edition-III batch (709 rows). Every
  denominator independently re-derived from first principles (acceptance-suite method).
- **Reversible / no silent transformation:** the lattice is frozen; the census is additive; every
  new row's raw JSONL is preserved in `raw_json`. v1 + v1.1 + v1.2 retained in git as lineage.

---

**Signed:** elrond (data steward) — for recording, at Edition-III, that the map's frame held while
its occupancy grew: 65 new class-kit rows lit 9 more meso cells and 2 more pull cells against a
lattice that did not move by a single cell. The space is the truth by construction; the census is
what the genre has been shown to build within it; v1.3 is the honest ledger of the second.
