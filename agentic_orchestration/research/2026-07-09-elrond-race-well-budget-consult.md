# Elrond Consult — Race-Well Budget Verification (Lane 4(b) empirical inputs)

> **STATUS:** CONSULT (read-only). Empirical inputs for rocket's Lane 4(b) math note.
> **Author:** elrond (data steward). **Date:** 2026-07-09. **Consumer:** rocket (authors the verification arithmetic per Disc #18 — I supply evidence, rocket derives).
> **Scope guard:** the race well is RULED + CLOSED at 5 (Human, Goblin, Orc, Elf, Dwarf) — `canonical/reap-die-rise-engine/bestiary-race-well-design-2026-07-09.md`, commit `908e858`. This note does NOT derive or propose races. It supplies P / cell-occupancy / M×F / over-under signal so rocket can VERIFY that the ruled 5 satisfy §3.1a `R ≤ P/(M×F)`.
> **Terms verified against canon:** `mob-affix-system-spec-2026-07-09.md` §3.1a (R = race count; P = season kit population; M = min viable faction mass; F = factions per race).

---

## 0. One-line read (for the memo's disposition)

**The cluster math HOLDS at 5 races — but the budget's own inputs are looser than the canon's ~700/40/2 sketch implies, and the load-bearing input (real per-cluster faction mass) is NOT YET MEASURABLE because the derivation population (batch-2, 18-cell fresh fire) has not emitted.** No empirical signal of FAILURE at 5. Verdict: **memo parks as FYI**, with one flagged caveat rocket should state explicitly (the M term is proxy-only until batch-2; this consult is pre-registered to re-fire on the real population at derivation-stack §10 step 3).

---

## 1. P — kit population size

**Empirical: P = 700, verified by direct byte-count.**

- `reincarnated-engine/src/reincarnated/output/w3_batch1_bundle.json` → `kits` array length = **exactly 700** (run_id `cbeb9471`, the W3 batch-1 martial bundle). The canon's "~700" is not an estimate — it is this run.
- **Load-bearing caveat rocket MUST carry:** these 700 are the **fixture/regression bank, NOT the faction-derivation population.** Per `batch2-build-spec-2026-07-06.md` §60: batch-1's 700 martial kits are "instruments, never derivation members" because "pre-axes kits are degenerate in every new dimension, and a mixed population forms clusters around axis-absence." The REAL derivation population is **batch-2: ≥100 gauntlet-passed kits/cell × 18 BC cells** (batch2 spec §L25) — a designed population well above 700 — which **has not emitted** (Leg C un-held but not fired). So P=700 is a valid *floor* for the budget verification, and the eventual P is larger, which only *loosens* the budget (more headroom for R). Using P=700 is conservative.

## 2. Populated-cell count (of the 20 race×register identity cells)

**NOT directly measurable — races are not yet a kit coordinate (E10 Leg 3 unbuilt; `mob-affix-system-spec` §10.1 confirms mob/kit records carry NO race/lineage/faction fields).** Two proxies, both mine:

- **Proxy A — my S4 faction-lookup cell space** (`reincarnated-engine/data/identity/faction_lookup_table.json`, which I maintain per §4.6): axis space = 13 lineages × 7 periods × 7 registers = **637 exact records** (complete cross-product by construction — "one record per non-void cell so nearest-match is never reached"). This is EXHAUSTIVE-fill, not sparse-occupancy — it tells you the cell *space* is fully mapped, not which cells the substrate votes to populate. It maps to **9 factions** (8 + Void override).
- **Proxy B — batch-1 PM-1 native occupancy** (`w3_batch1_bundle.json.factions.clusters`): the 700-kit population clustered into **4 PM-1 factions**, total **34 kits assigned** — i.e., the substrate natively populates only a handful of cells, ~5% of the population clusters. (Batch-1 is martial-uniform, so this UNDER-states real occupancy — see §4.)

**Read against 20 cells:** batch-1's native 4 clusters and my 637-cell exhaustive map bracket the answer. Neither over- nor under-populates 20 pathologically. E10 Leg 3 post-build must measure occupancy directly on a race×register coordinate (does not exist yet).

## 3. Faction mass M and factor F

**F (factions per race): canon indicative = 2; the live faction ceiling is F-C = 4 factions total** (`w3_batch1_bundle.json.factions.clusters` = 4; F-C ruling `faction-derivation-stack-spec` L72). At R=5 races and 4 total factions, effective F per race < 1 — factions are race-dominant-with-minority (canon §3.1a: "modal race + minority members; strict race-coherence NOT imposed"). This makes M×F SMALLER than the canon's M≈40 × F≈2 = 80, which **loosens** the budget.

**M (faction mass) — measurable, but only at proxy scale (batch-1):**
- batch-1 PM-1 cluster masses = **15, 8, 5, 6 kits** (mean ~8.5, min 5). NOT M≈40.
- PM-1 math floor (`phase-5-pm-1-multimodal-clustering-math` L427): "~5-6 kits per cluster = minimal viable cluster size for semantic identity"; 24-kit population threshold for a 4-cluster target.
- **So the empirically-observed M is ~5-15, and the design FLOOR is ~5-6 — an order of magnitude below the canon's M≈40 sketch.** The ~40 figure appears to fold in "per-floor faction/lieutenant/spawn-table needs" (canon §3.1a) beyond pure clustering mass; that operational M is not something I can measure from clustering substrate alone — flag for rocket.

**M×F for rocket's arithmetic (proxy, conservative):** clustering-observed M×F ≈ 8.5 × 4 ≈ 34 (matches batch-1 total assigned). Canon-sketch M×F = 80. Either way, with P=700: R ≤ 700/34 ≈ 20 (proxy) or R ≤ 700/80 ≈ 8.75 (canon-sketch). **5 sits inside both.**

## 4. Over/under-populate signal at 5 races

**No FAILURE signal. Both failure modes checked:**
- **Bland-collapse (too many kits/cell):** would require M ≫ 40 at 5 races. Observed clustering M is 5-15, well under. At P=700 / (5 races × 4 factions) = 35 kits per race×faction — right at the canon's ~35/cell target, and comfortably above the ~5-6 viability floor. No over-population.
- **Wasted-budget (too few populated cells):** batch-1 natively populated only 4 clusters, which could read as under-population — BUT this is a KNOWN ARTIFACT of batch-1's martial-uniformity (degenerate in the new axes, per §60), NOT a property of the 5-race well. The 18-cell batch-2 fire is explicitly designed to populate the axis space. So the low batch-1 occupancy does not falsify 5 races; it confirms batch-1 is the wrong population to measure on.

**The one thing that WOULD flip this to a decision item:** if batch-2 emits and its PM-1 clustering produces either (a) < ~4 viable clusters over the 18-cell population (well under-populates → 5 races is too many for the faction fabric) or (b) mean cluster mass ≫ 40 forcing bland race×register cells. Neither is measurable pre-batch-2. This consult is pre-registered to re-fire on batch-2's emitted population (batch2 spec §56 → derivation-stack §10 step 3, "elrond #18 consult").

---

## 5. Summary table (rocket's inputs)

| Term | Value | Basis | Confidence |
|---|---|---|---|
| **P** | 700 (floor; eventual larger) | byte-count `w3_batch1_bundle.json.kits` = 700; batch-2 ≥100×18 not yet emitted | HIGH (direct) |
| **populated cells / 20** | not directly measurable (no race coordinate yet); proxies: 4 native clusters (batch-1) / 637 exhaustive cells (S4 map) | `factions.clusters`; `faction_lookup_table.json` | proxy only |
| **M (faction mass)** | observed 5-15 (mean ~8.5); design floor ~5-6; canon operational sketch ~40 | batch-1 PM-1 cluster sizes; PM-1 math L427 | proxy scale (batch-1) |
| **F (factions/race)** | live total = 4 (F-C); per-race < 1 (race-dominant) | `factions.clusters`=4; F-C ruling | HIGH |
| **M×F** | ~34 (proxy) to ~80 (canon-sketch) | above | proxy/sketch |
| **over/under signal @ 5** | CLEAN — no failure; low batch-1 occupancy is a known martial-uniformity artifact, not a 5-race property | §4 | HIGH for "no failure signal" |

**Disposition:** cluster math holds at 5 → **memo is FYI**, with rocket stating the M-term caveat (proxy-only until batch-2 emits; consult re-fires then).

**What E10 Leg 3 must measure post-build:** direct race×register cell occupancy on a real race-coordinate; real per-cluster M on the batch-2 18-cell population (not batch-1); operational M inclusive of per-floor lieutenant/spawn-table needs.

**Signed:** elrond, 2026-07-09. *The numbers are supplied; the arithmetic is rocket's. I measured what exists, named the two proxies where the coordinate does not yet exist, and flagged — not fabricated — the term that batch-2 has yet to speak.*
