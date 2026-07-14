# Cell-key dedup v1 — Stage 1 collapse-structure report

**Author:** gamora (simulation seam) · **Date:** 2026-07-13
**Dispatch:** `dispatches/2026-07-13-gamora-cell-key-dedup-v1-BLOCKED.md` (gate CLEARED)
**Spec:** `gandalf/design-inputs/dedup-stage1-gamora-handoff-2026-07-13.md`
**Canon:** `canonical/reap-die-rise-engine/coordinate-register-2026-07-13.md` §6/§6.1/§8
**Nature:** PURE DATA — read-only strict `GROUP BY cell_key` + Hamming-1 scan over 470 combat-kit rows. No sim, no gauntlet, no batch, no cert instrument. No coarsening, no deletion.

This is the evidence packet the Stage-2 cluster review (gandalf + gamora + Matt) rules against. It reports what EXISTS. It does not demote any coord. **Stage 1 STOPS here.**

---

## 0 — Run parameters (all consumed, none re-verified)

- Source: `agentic_orchestration/research/curated/corpus.db` (read-only).
- Filter: `row_class='combat-kit' AND cell_key IS NOT NULL` → **470 rows**, all 14-arity (`|`-delimited).
- `cell_key` materialized by elrond (commit `2a02ed0d`), gandalf-verified read-only.
- 14-slot layout confirmed against register §2 (see `generate_outputs.py` `POS`): #5 control contributes two slots (5a treatment + 5b function).
- Unknown/blank slots are literal values (guardrail #3 verified): **49 kit-rows** carry ≥1 literal `unknown`/`blank` slot → **45 cells**. Never merged on absence.

---

## 1 — Strict collapse: 470 → 457 cells

Strict exact-match `GROUP BY cell_key` (§6.1 Stage 1 — the maximally-split start; never wrong-merges):

| | count |
|---|---|
| combat-kit rows | 470 |
| distinct cells (strict-14) | **457** |
| representatives (1 per cell) | 457 |
| retained isotope losers (never deleted) | 13 |

The collapse is near-maximally-split: 470 kits differ from one another on the strict key almost everywhere. Only 25 kits (13 losers + their 12 representatives) share a cell with any other kit.

---

## 2 — Output #2: isotope-depth histogram (SUPPORT — trivial, as predicted)

`isotope_depth_hist.csv`:

| depth | num_cells | kits_covered |
|---|---|---|
| 1 (singleton) | 445 | 445 |
| 2 (pair) | 11 | 22 |
| 3 (triple) | 1 | 3 |

445 + 22 + 3 = 470 kits; 445 + 11 + 1 = 457 cells. **Confirmed trivial** — matches the reshuffle prediction exactly. The histogram tells the review almost nothing (the key is essentially flat). It is emitted to confirm the shape; it is NOT the decision object. **All Stage-2 signal lives in §4.**

The one triple is `poe1` ballista/fire-trap/pizza-sticks (a totem-delivery, cooldown, apply→detonate cell). The 11 pairs are cross-game or intra-game near-duplicate builds.

---

## 3 — Representative selection (§6 tiebreak, operationalized)

§6 rule: **longevity of lineage across games → recency → primary.** Column-math drafted (support columns `canon_corpus.{eras, era_year, canon_tier, kit_id}`; deprecated `mobile_*` fields NOT used):

- **longevity** = `era_span` = count of `;`-delimited era segments in `eras` (how many balance-eras the lineage survived). DESC.
- **recency** = `era_year` (the kit's era anchor year). DESC.
- **quality nudge** = `canon_tier` rank (deep=3 > moderate=2 > shallow=1 > blank=0). DESC.
- **primary (deterministic floor)** = `kit_id` ASC — fully-orders every partition so selection is reproducible.

Empirical constraints that shaped this:
- `skill_debut_year` is populated for only **7/470** rows → **unusable** as a longevity proxy. `era_span` is the faithful substitute.
- **"Across games" caveat (flagged to gandalf):** no cell's members share a single multi-GAME lineage in this corpus — each kit's `eras`/`lineage` is single-game. So "longevity across games" is not literally per-lineage computable; `era_span` measures era-persistence within the lineage, which is the closest faithful reading of the §6 intent. Confirmed with gandalf before finalizing (see completion record).

Behavior on the 12 multi-member cells is in `cell_table.csv`. Two illustrative outcomes confirming the rule works:
- The `poe1` **triple**: `poe1-fire-trap` wins (era_span=3) over ea-ballista (2) and pizza-sticks (1) — longevity FIRST, ahead of the deeper-tier ballista. Correct per §6.
- `poe1-cyclone` beats `d3-ww-wastes` (both era_span=4) on recency (2013 > 2012). Correct.

Isotopes are **retained, flagged not filtered** (`isotope_kit_ids` column). Breadth is the pitch; nothing deleted.

---

## 4 — ★ Output #3: near-twin adjacency aggregate (THE PRIMARY DELIVERABLE)

All cell-pairs whose `cell_key`s differ in **exactly one** of the 14 positions. **92 near-twin pairs** across the 457 cells (`near_twin_pairs.csv`, annotated with which coord + the two values). Aggregated per differing-coord (`near_twin_percoord.csv`):

| differing coord | near-twin pairs | distinct swaps | register class |
|---|---:|---:|---|
| **#4 geometry** | **17** | 11 | demotable-with-evidence |
| **#7 economy_model** | **17** | 10 | demotable-with-evidence (the contentious one) |
| **#5b ctrl_function** | 14 | 8 | never-demote core |
| **#6 defense** | 13 | 7 | demotable-with-evidence |
| #3 amp | 7 | 2 | demotable-with-evidence |
| #1 movement | 4 | 3 | never-demote core |
| #9 range | 4 | 2 | demotable-with-evidence |
| #10 tempo | 4 | 2 | demotable-with-evidence |
| #13 dependency | 4 | 2 | never-demote core |
| #11 commit | 3 | 2 | demotable-with-evidence |
| #12 activation | 3 | 1 | never-demote core |
| #8 proxy | 2 | 2 | never-demote core |
| #2 delivery | 0 | 0 | never-demote core |
| #5a ctrl_treatment | 0 | 0 | never-demote core |

**Read the shape, not gandalf's hypothetical.** The spec's illustration ("312 pairs differ only on #10 tempo") does NOT occur — there is no runaway texture coord. The distribution is flat-topped: a four-coord shoulder (#4, #7, #5b, #6 at 13–17 pairs each) then a long tail. This is a *more* informative outcome than a single dominant coord: it says the strict-14 key is near-orthogonal — most coords genuinely partition the population, and the collapse pressure is spread, not concentrated.

### Texture-vs-identity read (my empirical call — the object the review rules on)

**Strongest demotion candidates (behaving as texture within a shared archetype):**

- **#4 geometry (17 pairs).** The register already flags geometry as "refine *within* #2 delivery," and the swaps confirm it: `chain~circle`, `multi_projectile~single_target`, `ground_targeted_circle~melee_strike`, `circle~melee_strike`. These are same-delivery shape variants of one build (a chain-lightning vs a nova of the same caster; a multi-proj vs single-target of the same attacker). Geometry is reading as **texture** here — it splits cells that are the same build wearing a different shape. **Lead demotion candidate.**

- **#7 economy_model (17 pairs, tied-lead).** This is the register's flagged-contentious coord, and the data splits it *down the middle* — exactly as §6.1 warned. The swaps divide into two populations:
  - **Texture-like:** `spend~unknown` (3), `reserve~unknown` (1), `cooldown~finite` (1) — one side is an unknown/soft-fill, or a cost-flavor difference that doesn't change the build. These smell like texture.
  - **Identity-like:** `generator-spender~self-cost` (1), `generator-spender~spend` (1), `finite~spend` (3), `reserve~spend` (3) — generator-spender and self-cost (blood-magic) are *build-defining* economies; a WW-Fury barb is not the same build as a spend-pool version. §6.1's own note holds: "generator-spender is build-defining; mana-vs-cooldown often is not." My read: **#7 should NOT be wholesale demoted.** If the review coarsens it, coarsen it *conditionally* — collapse the soft/unknown-adjacent swaps, keep generator-spender / self-cost / reserve as cell-defining. This is the one coord where a blanket demote would wrong-merge.

- **#6 defense (13 pairs).** Swaps: `mitigate~tank` (3), `evade~tank` (3), `glass~mitigate` (2), `glass~tank` (2). These are defensive-posture variants of an otherwise-identical offensive build. Defense reads mostly as **texture** — the same delivery/control/geometry kit with a tankier vs glassier survival profile. Demotable, with one caution: `glass` vs `tank` is a large survivability gap that a player might read as build identity, not garnish. Demote with the review's eyes open.

- **#3 amp (7 pairs, only 2 swaps: `flat~var` ×4, `flat~spiky` ×3).** Small count, low swap-diversity — amp is a 3-value axis whose near-twins are all "same build, different damage-shape." Reads as **texture.** Clean demotion candidate, low blast radius.

**Behaving as identity (do NOT demote — the data agrees with the never-demote core):**

- **#5b ctrl_function (14 pairs)** is high, but it is **never-demote core**, and the swaps justify that: `hard-stop~none`, `none~stun`, `expose~none`, `knockback~none` — these are "has-a-control-function vs does-not," which is precisely a build-identity fork (a stun-lock controller vs a pure-damage kit of the same shape are *different builds*). High near-twin count here is NOT a demotion signal; it means control-function is doing exactly its identity job at the margin. **Keep.**
- **#2 delivery (0)** and **#5a ctrl_treatment (0)** produce *zero* near-twins — no two cells differ on delivery or treatment alone. They are perfectly identity-partitioning. Strongest evidence for their never-demote status.
- **#1 movement (4), #8 proxy (2), #12 activation (3), #13 dependency (4)** — all low, all never-demote core; the data supports keeping them (they rarely fork alone, and when they do it's a real build difference).

**Summary recommendation for the review (NOT enacted here):** the demotion-candidate ranking by texture-behavior is **#4 geometry ≈ #3 amp > #6 defense > (conditional) #7 economy_model**. #4 and #3 are the cleanest wholesale demotions; #6 demotable with the glass/tank caveat; #7 is the coord where the data says *split the coord's values*, not demote it whole. #9/#10/#11 (range/tempo/commit) each have only 3–4 near-twins — too few to drive a confident call either way; the review can fold them opportunistically if a specific pair is obviously the same build.

---

## 5 — Artifacts

- `cell_table.csv` — Output #1: 457 cells; `cell_key` · population · representative · isotope members.
- `isotope_depth_hist.csv` — Output #2: depth histogram (trivial).
- `near_twin_pairs.csv` — Output #3: 92 annotated Hamming-1 pairs.
- `near_twin_percoord.csv` — Output #3 aggregate: the per-coord Stage-2 driver (this report §4).
- `generate_outputs.py` — reproducible generator (read-only).

**STOP.** No coord demoted. No coarsening. The Stage-2 coarsening decision is the cluster review (gandalf + gamora + Matt), ruled against §4. Holding at the gate.
