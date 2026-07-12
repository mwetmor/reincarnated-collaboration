# V2 — Convergence Ledger (resolution ladder), first computation

**Date:** 2026-07-12 · **Author:** gandalf · **Source:** `final-docs-v3/rdr-kit-atlas-v3.csv` (506 placed corpus rows, 494 unique cells; positives only unless noted) · **Threshold ruling:** ≥2 distinct games (Matt 2026-07-12)

---

## 1. The resolution ladder

Convergence is scale-dependent. One number lies; the ladder tells the truth:

| Resolution | What's masked | Cells ≥2 games | Cells ≥4 games | What it measures |
|---|---|---|---|---|
| **full key** | nothing | **7** | 0 | exact identity twins — the rarest, strongest recurrence |
| **elem-masked** | identity element | **20** | 1 | **FLAVOR families** (same kit, different element skin) |
| **bc10** | element + econ | **39** | 3 | behavior-coordinate recurrence |
| **bc6** (sampled prefix) | all measured slots | **74** | **25** | **attractor basins** — anchor-candidate territory |

## 2. Full-key cross-game twins (all 7 — each one is signal)

| Address | Games | Kits |
|---|---|---|
| `DRHFSI-HMDD-SP-PH` | **d4 + poe1 + undecember** (3g/4k) | Quill Volley · Tornado Shot · Wander · Spread/Rapid baseline — **the archer identity cell** |
| `IDHFSC-RSDG-SP-FI` | poe1 + undecember | Incinerate · Flamethrower Channel (+1 negative twin) — contested channel cell (GX-21) |
| `DDHFSI-HMDD-SP-PH` | le + poe2 | Spiral Volley · Umbral Blades |
| `DRHFSI-HCDD-SP-LI` | poe1 + poe2 | Lightning Arrow · Lightning Arrow Deadeye (cross-era self-recurrence) |
| `IMMFHI-MNDM-SU-PH` | gd + le | Skeleton Necromancer · Skeleton Ritualist — the minion identity cell |
| `IRMVSI-_LDG-SP-FI` | d2 + d4 | Fire Warlock · Blazing Abyss — fire-caster recurrence across 24 years |
| `SMHFSI-MSMT-SP-PH` | d4 + poe1 | Bash · Boneshatter — STR-melee-instant cell |

## 3. Deepest bc6 attractor basins (≥4 games = 25 cells; top two)

- **`IRMFHI`** — 11 games / 13 kits: the standard-caster basin (K12's address).
- **`DRHFSI`** — 10 games / 20 kits: the fast-archer basin (K7's address).

These basins + era persistence + tier weight = the seed list for the ANCHOR ROSTER PROPOSAL (Stage 2).

## 4. Within-game multiplicity at full key (the redundancy check)

**Only 3 game-cells worldwide hold ≥2 kits at the same exact address** (poe1 Tornado Shot+Wander; hot Arcane Splinters+Archer-multishot; vs Holy Wand+Thousand Edge — the latter two at abstain-degraded keys). True same-address redundancy in the corpus is nearly nonexistent.

## 5. Case study — Matt's whirlwind hypothesis, measured

Hypothesis: *"maybe a portion of the 9 whirlwind barbs are so similar that they are redundant."* Measured: **12 spin-verb kits across 9 games occupy 10 DISTINCT full addresses.** They differentiate by attribute (DEX-spin: d2 WW Assassin, poe2 Whirling Assault, tq2 WW Rogue · STR-spin: d3 Wastes, poe1 Cyclone, undecember WW, di WW Barb, d4 Dust Devils), tempo, **commit (instant vs channel!)**, mobility semantics, econ. Closest pair: DI Whirlwind Barbarian vs Undecember WW baseline — identical except econ slot (`CD` vs `SP`).

**Verdict:** in DESIGN space the whirlwinds are not redundant — the genre kept re-shipping spin because the coordinate neighborhood is rich. Whether the sim FEELS the slot-differences (does `SMHFSC-_SDT` fingerprint apart from `SMHFSC-KSDT`?) is exactly the behavior map's job — *uniqueness is sim behavioral fingerprint, never coordinate distance* (mobile Rule 1 = our gauntlet doctrine). REDUNDANT is a **phenotype verdict**; design space can only nominate candidates.

Roster note: our Spin-to-Win sits inside the STR-spin basin (validated lineage); **K1 Heavy Barbarian (low-tempo/spiky spin) is a spin variant NO genre game shipped** — now crisply visible as deliberate whitespace or drift (Mac-fill rules).

## 6. Era-depth decoration (V6 folded in — next computation)

Corpus rows carry version-era strings (e.g., poe1 `1.x;3.0-3.6;3.7-3.13;3.20+`). Next V2 iteration: era-span column per convergence cell; attractors that persist across eras outrank one-era fads for anchor selection.

## 7. Reproduction

All numbers from Python computations over the CSV (session transcript 2026-07-12): group by `atlas_key` at 5 masking levels, positives only, distinct-game counting, within-game grouping by (address, game).
