# Corpus curation log — Edition-III Stage C + D: register v1.3 + Edition-III emission

> **STATUS:** CURRENT (record of completed register re-derivation + atlas emission). Edition-III Stage C + D.
> **Author:** elrond (data steward) · **Date:** 2026-07-15
> **Store:** `agentic_orchestration/research/curated/corpus.db` + `atlas/` (elrond-owned; corpus.db gitignored, atlas artifacts committed)
> **Commission:** `agentic_orchestration/gandalf/briefs/2026-07-15-elrond-edition3-one-batch-commission.md` §3 + §4.
> **Charter:** `canonical/reap-die-rise-engine/atlas-derivation-charter-2026-07-14.md` §4 (ghost field) + §6 (Edition law: frozen frame, versioned occupancy).

---

## STAGE C — register re-derivation v1.2 → v1.3

**Generator:** `scripts/feasibility_cuts_register_v1_3_2026_07_15.py`
**Artifacts:** `atlas/feasibility-cuts-register-v1.3.{md,csv,json}` + `atlas_feasibility_ladder_v1_3_2026_07_15` table (corpus.db, gitignored).

### C.1 The load-bearing property: lattice FROZEN, census GREW

The Edition-III batch (+65 rows) uses ONLY existing coordinate values — no new function level, no
new delivery/geometry, nothing new in the enumeration base (`pull` already entered at v1.2).
Therefore:
- **Enumeration base UNCHANGED** vs v1.2.
- **Cut ledger UNCHANGED** (L1′/L2/L3/L4″/RED-3′ + taste-KEEP, all inherited).
- **Feasible-lattice denominators BYTE-IDENTICAL** vs v1.2 (independently re-derived from first
  principles — the acceptance-suite arithmetic): exact **767,411,820** / meso **11,160** / sealed
  **1,314** (L1′ 756 + L2 558) / pull slice **1,080 feasible + 54 sealed** (all L2).

This is the charter §6 "frozen frame, versioned occupancy" law at Edition scale. Denominators are
RE-ASSERTED, not superseded (differs from the v1.1→v1.2 bump which grew function 10→11).

### C.2 Full denominator re-derivation (raw → post-logical → post-red-law)

| stage | exact-lattice | meso-grain |
|---|---|---|
| raw naive product | 990,186,120 | 12,474 |
| → post-logical (L1′+L2+L3+L4″) | 819,439,740 | 11,160 |
| → post-red-law (RED-3′) | 767,411,820 | 11,160 |

Every figure reproduces exactly (asserted in-generator, fail-loud on drift).

### C.3 Census population (the ONLY v1.3 delta)

| metric | pre-batch (644) | post-batch (709) | Δ |
|---|---|---|---|
| corpus rows | 644 | **709** | +65 |
| active combat-kit (cell_key non-null) | 563 | **628** | +65 |
| occupied meso cells (lit) | 193 | **202** | +9 |
| pull-lit meso cells | 2 | **4** | +2 |
| unmapped-pending-curation | 108 | **114** | +6 |

**The 2 new pull-lit meso cells:** `[ROOTED, ZONE, damage, pull, solo, active, build→spend]`
(Destroyer engraving-grain carriers + Gravity Impact) + `[ROOTED, ZONE, damage, pull, solo, active,
one-shot]` (d3-wizard-black-hole). The Edition-II pair persists (`d3-zbarb` FREE-MOVE/ZONE +
`di-cyclone-monk-pvp` WALK/NOVA control-pull).

**The +6 unmapped (documented, NOT keying errors):**
- 1 honest-NULL movement — `d4-spiritborn-vortex` (source movement undocumented → `mob=blank`).
- 5 MELEE-collapse — `delivery=melee` has NO meso ghost image (`fit2reg_delivery` has no `melee`
  image; documented in the pull-tranche insert script + MCD re-run): the 4 skill-grain Destroyer
  rows + `di-cyclone-strike-monk-base`. Their ENGRAVING-grain siblings (`at-target`→ZONE) DO light —
  hence pull-lit 2→4.

### C.4 Pull-slice re-vet under the larger census — HALT=False

Every one of the 4 lit pull cells is a FEASIBLE pull cell (none lands on a sealed cell), asserted
in-generator. `new_law_needed = 0`, `halt = False`. **No new law was needed** (LA class-kits add no
coordinate value). Had any lit pull cell landed on a sealed cell OR any cell required a new law, the
generator would HALT and park to Matt (the v1.2 discipline). It did not.

### C.5 Re-keys forced on existing rows — NONE

The batch is purely additive at the census level. The 469 frozen survivors + the Stage-A 7 rows are
byte-identical before and after Stage B (asserted). The LA Destroyer engraving-grain rows
CROSS-REFERENCE the skill-grain pull-tranche rows but do NOT contradict them (tranche index: *"No
contradiction; enrichment"*), so no existing row's evidence changed. The Edition-II Stage-3 re-keys
(`d3-zbarb`, `di-cyclone-monk-pvp` → `function=pull`) stand unchanged. No C3-style re-key is owed.

### C.6 Schema change — NONE

The batch works inside the existing corpus schema. v1.3 adds one additive analysis table
(`atlas_feasibility_ladder_v1_3_2026_07_15`) to corpus.db (gitignored) — no schema change to any
consumer table, no engine-side migration owed. (MIGRATION.md Edition-III entry.)

### C.7 HALT branches — NONE

No new-law-needed. No ambiguous grain-of-record beyond the explicit flag-c adjudication (skill vs
engraving grain, both recorded). The one genuinely-ambiguous evidence call (Sorceress Reverse
Gravity) was resolved by the bounded search under the register boundary rule + intrinsic bar (Stage
B log §3), not improvised into a new law. Nothing parked.

---

## STAGE D — Edition-III ghost-field emission

**Emitters:** `scripts/ghost_field_edition3.py` + `scripts/build_atlas_json_edition3.py`
**Acceptance:** `scripts/edition3_acceptance_2026_07_15.py` (24/24 PASS).
**Artifact:** `atlas/atlas-edition3.json` (7.49 MB) — emitted ALONGSIDE `atlas-edition2.json` (never over).

### D.1 Frozen-basis gate (charter §6) — RESPECTED

New rows PROJECT into the frozen Edition-I basis via the SAME CA supplementary transition formula
(`pull`/silence/hybrid/MELEE/SUMMON masked-like — no fit column, cannot bend an axis). The basis is
NOT re-derived at an edition increment. The fit reconstructs from the durable pre-C3 snapshot
`atlas-frozen-fit-cellkeys-edition1.csv`; lighting uses the LIVE post-Edition-III corpus keys at
emission time. **The +65 census rows are NOT active fit points** — the fit set stays 469 active /
506 total, Edition-I-frozen forever; the new rows light ghosts only.

### D.2 FIT layer byte-frozen — ASSERTED in-script (receipts)

| assertion | result |
|---|---|
| basis block byte-identical to Edition-I (`atlas.json`) | **PASS** |
| all 506 point coords byte-identical to Edition-I | **PASS** |
| tombstone `death_class` strings byte-identical to Edition-I | **PASS** |
| active fit points == 469 (census rows light ghosts only) | **PASS** |
| total fit points == 506 | **PASS** |

### D.3 Edition-II preserved (never overwritten)

`atlas-edition2.json` is asserted present + still an Edition-II artifact (edition==2) before Edition-III
emits. Confirmed byte-untouched vs git HEAD (git status clean on `atlas-edition2.json` +
`feasibility-cuts-register-v1.2.*`). Edition-II stays the SERVED TRUTH until Matt's Edition-III freeze
ratification + re-vendor.

### D.4 Lattice-integrity + pull-slice-integrity receipts

| assertion | result |
|---|---|
| depth_sum == 767,411,820 (unchanged vs Edition-II) | **PASS** |
| lit census reproduces from corpus keys (202) | **PASS** |
| every pull kit (10) is intrinsic-evidence | **PASS** |
| ZERO mcd-lit pull cells | **PASS** |

The 10 pull-function kits (all intrinsic): `d3-zbarb`, `di-cyclone-monk-pvp` (Edition-II Stage-3
re-keys) + `la-destroyer-vortex-gravity`, `la-destroyer-gravity-impact`, `la-destroyer-gravity-force`,
`d4-spiritborn-vortex`, `d3-wizard-black-hole`, `di-cyclone-strike-monk-base` (pull-tranche) +
`la-destroyer-rage-hammer`, `la-destroyer-gravity-training` (Destroyer engraving-grain carriers).

### D.5 Emitted ghost field (Edition-III)

11,160 feasible + 1,314 sealed meso cells; **202 lit** (up from 193); **4 pull-lit** (up from 2);
drill-in 172,312 sub-feasible + 10,136 RED-3- sealed; off-plane N=94 (mcd gear-grain, unchanged);
**P-DF-1 PASS**.

---

## Numbers of record (post-Edition-III batch)

| metric | value | Δ vs pre-batch |
|---|---|---|
| corpus total | **709** | +65 |
| engine_key total | **683** | +65 |
| active combat-kit (cell_key non-null) | **628** | +65 |
| corpses (negative) | **38** | 0 |
| system-records | **18** | 0 |
| unresolved | **39** | 0 (all pre-existing mcd/undecember/etc.) |
| pull-function rows | **10** | +8 |
| hybrid rows | **0** | 0 (frontier honest) |
| occupied meso cells | **202** | +9 |
| pull-lit meso cells | **4** | +2 |
| feasible lattice (exact) | **767,411,820** | 0 (frozen) |
| feasible lattice (meso) | **11,160** | 0 |
| sealed (meso) | **1,314** | 0 |
| pull slice | **1,080 feasible + 54 sealed** | 0 |

---

**Signed:** elrond (data steward) — the register re-derived the census against a lattice that did
not move, the pull slice re-vet returned HALT=False with zero new laws, the FIT layer is proven
byte-frozen, and Edition-III sits alongside Edition-II as an un-ratified artifact awaiting Matt's
freeze. The frame held; the occupancy grew; every frozen thing is proven frozen.
