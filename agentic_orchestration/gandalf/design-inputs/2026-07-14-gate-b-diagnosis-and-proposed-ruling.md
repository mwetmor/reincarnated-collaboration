# Gate-B Diagnosis + Proposed Protocol Ruling — Atlas Derivation 2026-07-14

**Date:** 2026-07-14 · **Author:** gandalf (DRIFT-CRITIC verdict; SPEC-AUTHOR proposal)
**Status:** **RATIFIED-WITH-AMENDMENTS by jack-ryan** (post-results review, `qa/findings/2026-07-14-gate2-atlas-gate-b-ruling-review.md`, commit 036d0a8d) — RIDER-1 + CLARIFY-1 applied below; jack-ryan independently reproduced the § 3.2 neighbor table byte-for-byte and the Gate-B statistic within Monte-Carlo tolerance, and ran his own falsifiability probe (a co-located corpse set would have cleared 1.389; the corpses sit at 2.44 — the gate was falsifiable both ways, the FAIL is real). **The RULING is cleared; the Edition-I FREEZE decision is Matt's.** **→ ✓ RATIFIED 2026-07-14 (Matt: *"Ratify a"*) — Edition-I freeze LIVE on A/C/D + F-1; axis names dims 1–2 ratified (PERFORM↔DEPLOY / EMBODY↔LAUNCH); consequences fired (star-lord IV.x-c atlas.json basis block; KR + jack-ryan decisions-log rows).**
**Review object for:** jack-ryan · **Decision object for:** Matt (Edition-I freeze / fallback)
**Companion docs:**
- `agentic_orchestration/gandalf/design-inputs/2026-07-14-atlas-derivation-preregistration.md` (v1.1 PINNED — the contract)
- `agentic_orchestration/research/curated/atlas/2026-07-14-gate-report.md` (elrond, numbers only)
- `canonical/reap-die-rise-engine/atlas-derivation-charter-2026-07-14.md` (the adopted charter)

**⚠ CONFLICT DECLARED:** I authored Gate B in the pre-registration. I now diagnose my own gate as mis-specified. That is rule-maker-judging-own-rule; therefore this ruling does NOT proceed on my authority — jack-ryan reviews with BLOCK authority, and the freeze itself is Matt's ratification either way.

---

## 0. TL;DR

- **A / C / D pass with margins** (ARI 0.668 vs 0.6; R² 0.0757 vs 0.15 with PERMDISP interpretable; bootstrap 3.60% vs 10%, worst LOFO 0.968 vs 0.85). The 14-D retained MCA basis is a valid, franchise-agnostic, highly stable representation.
- **B fails REVERSED:** the five intrinsic-red corpses are significantly *dispersed* (p_dispersed = 0.0363), not clustered. The extrinsic-tuning secondary (non-gating) is also non-clustered (p_lower 0.814).
- **Diagnosis (the pinnable cause):** Gate B encoded a directional *territory hypothesis* ("intrinsic design failure concentrates in a danger zone") as a *map-validity criterion*. The data falsifies the hypothesis, not the map. Neighbor-identity evidence (§ 3.2) shows the projection places every corpse among its mechanical siblings — the map represents the negatives faithfully; they are dispersed because they died for different structural reasons in different regions, exactly as the 38-negative failure taxonomy (3 distinct red laws, 12 patterns) should have predicted at authoring time. The directional prior was mine and it was wrong.
- **Proposed ruling:** spend the prereg's one permitted protocol-amendment cycle as a *reclassification*, not a re-run — Gate B converts to **Finding F-1** ("kit death is not geography"), published verbatim; Edition-I freeze proceeds on A/C/D; zero recomputation; danger-zone overlay vocabulary retired in favor of per-corpse tombstones. If jack-ryan blocks: fallback clause fires as pinned.

---

## 1. DRIFT-CRITIC verdict on the pipeline execution

Execution fidelity: **clean.** elrond ran v1.1 with zero protocol amendments, pinned seed 20260714, snapshot verified, N=469 exact, frozen label table byte-verified (86/15/24/23/9/8/7), rollup 11 franchises no orphans, fusing map computed once and recorded. Leiden ran as true Leiden-CPM (leidenalg installed; A7 honored — no silent Louvain). The one Stage-0 reconciliation (37 projectable negatives vs "38 graveyard"; `vs-golden-egg-scaling` is a system-record outside the combat denominator) is correctly documented data-state, not a fault.

| Gate | Result | Margin |
|---|---|---|
| A group-recovery | **PASS** | ARI 0.668 (bar 0.6); 6/6 silhouettes clear, all four large groups clear (0.283–0.551); zero permitted-failure slots used |
| B negative-geography | **FAIL (reversed)** | p_clustered 0.9638; p_dispersed 0.0363 |
| C franchise-mixing | **PASS** | R² 0.0757 (bar ≤0.15); PERMDISP p 0.066 → interpretable |
| D stability | **PASS** | bootstrap median 3.60% of diameter (bar ≤10%); LOFO min 0.968 incl. holding out all 156 Diablo kits; reweight 0.985 |

## 2. Structural findings (non-gate; decision-shaping)

1. **The space is high-dimensional and diffuse.** Parallel analysis retains **14 MCA dims**, each 1.7–4.6% corrected inertia; dims 1–2 carry **8.36%** combined. There is no dominant plane. The charter's inertia badge must say this honestly on every render. (Gower-MDS view retains 5 dims at 38.5% of its own inertia — a candidate secondary view.)
2. **No discrete meso-families exist.** Leiden-CPM finds no non-degenerate plateau anywhere in the pinned sweep (132→469 communities); LCA selects k=3 by BIC; cross-family partition agreement is low (ARI 0.02–0.23). **The kit space is a continuum with archetype condensations, not a periodic table of boxes.** Gate A proves the condensations are real where genre history says they are; the space between them is connective tissue. This retroactively vindicates rejecting the Q19 fixed grid — even *derived* discrete partitions don't exist at meso-scale. Render consequence: density/terrain, not cell borders.
3. **Strongest coordinate association:** economy↔activation V=0.616 (triggered kits live on cooldown economies — mechanically real, not redundancy; no V>0.8 near-duplicates, so the 13-coord Class-A set stands for Edition I).

## 3. Gate-B diagnosis — the pinnable cause

### 3.1 What the gate actually tested vs what validity requires

Gate B's threshold (p<0.05 that intrinsic-red corpses are *tighter* than random draws) operationalized the charter's "the map must not misrepresent the negatives" as **"the negatives must form a danger zone."** Those are different claims. A valid map of a territory where failure is NOT geographically concentrated will — correctly — show dispersed corpses. The gate could only pass if a substantive hypothesis about the territory happened to be true. It was not:

- intrinsic-red k=5: mean pairwise 2.4404 vs null 1.8549 → **dispersed**, p_dispersed 0.0363
- extrinsic-tuning k=6 (secondary, non-gating): 2.0944 vs 1.8470 → non-clustered, same direction

The failure taxonomy already knew this: **three distinct red laws**, twelve patterns, amber ledger ~2/3 extrinsic. Five corpses spanning multiple distinct structural laws have no reason to co-locate. I wrote a directional prior the taxonomy didn't support; the prereg's example of a pinnable cause ("e.g., a fusing error") imagined execution-side causes, but the cause here is specification-side: **wrong operationalization of a correct intent.**

### 3.2 Neighbor-identity evidence — the map represents the corpses faithfully

Read-only check on the committed coordinate CSVs (5 nearest active neighbors per corpse, 14-D retained space):

| Corpse (intrinsic-red) | Nearest active neighbors | Reading |
|---|---|---|
| `poe1-charged-dash` | d4-ww-dust-devils, d3-poj-tempest-rush, **gd-eor-warlord [WHIRLWIND]**, d4-dance-of-knives, **d2-ww-sin [WHIRLWIND]** | a channel-dash melee corpse buried in whirlwind country, among *living* frozen-label whirlwind kits |
| `poe1-reaper` | poe1-generals-cry, poe1-golementalist, d3-helltooth-garg, d3-inna-allies, di-crusader-banner-support | a minion corpse among minion kits |
| `d2-leap-attack-barb` | poe2-titan-hotg, di-meteor-wizard, d3-lod-bazooka, hades2-hephaestus-blast, d3-tal-meteor | a jump-slam corpse among wind-up impact kits |
| `d2-blaze-sorc` | hot-swordsman, d4-flame-shield-immortal, gd-blade-arc-warder, **poe2-walking-calamity**, d2-singer | a walk-and-burn corpse next to a *living* near-identical archetype |
| `vs-gatti-amari` | d2-firewall-sorc, d3-lod-archetype, le-chthonic-fissure-warlock, hot-kugelblitz, d2-poison-nova-necro | an autonomous zone-chaos corpse among ground-effect kits |

Every corpse sits among its mechanical siblings. The projection machinery is the same machinery Gate A validated (places known-similar kits together) and Gate D validated (stable). **The corpses are dispersed because they are different kits that died for different reasons — not because the map mislocates them.**

Two of these neighborhoods carry the finding in a single image: **the same neighborhood holds both thriving citizens and a grave** (charged-dash beside living whirlwinds; blaze beside living walking-calamity). Death is not a place on this map.

### 3.3 The finding (F-1, proposed for publication in the Edition-I record)

> **F-1 — Kit death is not geography.** Neither intrinsic-structural corpses (k=5, p_dispersed 0.036) nor tuning-killed corpses (k=6, non-clustered) concentrate in mechanical-coordinate space. Kits do not die because of *where* they are in the space; they die for causes the coordinates do not encode (tuning, itemization, meta context) or for kit-specific structural violations that are local to the kit, not to a region. **Consequence: the unexplored ghost field contains no forbidden zones derived from corpse-geography** — any feasible cell can in principle host a living kit executed well. The graveyard is rendered as per-corpse tombstones with cause-of-death, never as shaded danger regions.
>
> *(RIDER-1 §2 applied — binding: this finding is **non-downgradable**. F-1 is a published NEGATIVE result about geography; no future Edition may quietly convert it into a soft danger-heuristic or claim "we always knew death was geographic." Revision requires a new powered test under a fresh prereg, not reinterpretation.)*

## 4. Proposed ruling (jack-ryan reviews → Matt ratifies)

Under the pinned decision rule ("One protocol-amendment cycle is permitted (§9) IF the failure diagnosis identifies a pinnable cause… otherwise fallback"):

- **R1 — Reclassify, don't re-run.** The one permitted amendment cycle is spent as a specification correction: Gate B is reclassified from validity-gate to substantive result, published verbatim as **FAIL → Finding F-1**. The Edition-I freeze criterion becomes A+C+D (all of which passed with margins). **Zero recomputation, zero tuning** — every number stands exactly as computed under v1.1. No new gate is invented post-hoc to replace it in this edition.
- **R2 — Overlay consequence.** Danger-zone overlay vocabulary is retired from the charter's ghost-field rendering; GRAVEYARD renders as individual tombstones with cause-of-death labels (feeds the devlog directly).
- **R3 — Edition-II criterion.** A replacement negative-validity criterion (per-law locality, powered) is designed *before* Edition-II derivation, in a fresh v2 prereg with jack-ryan review, once the graveyard census grows (Legolas re-crawl of the 211 source-capped rows + new corpses). Per the second-attempt clause. *(CLARIFY-1 applied — binding: the v2 prereg must state the **minimum per-law corpse count** that makes a per-law locality test powered, with the power calculation behind it, AND the **census-growth trigger** — which Legolas re-crawl deliverable and what count unlocks Edition-II Gate-B design. "Grows" is no longer unpinned.)*
- **If jack-ryan BLOCKS R1:** the fallback clause fires as pinned — exact lattice at meso-grain ships as the census dashboard + F-1 publishes as the negative finding. (Note: F-1 publishes on *either* branch; the branches differ only in whether the derived map freezes as Edition I.)

### What jack-ryan is asked to rule

a. Is the § 3 diagnosis a legitimate *pinnable cause* under the decision rule, or motivated reasoning by the gate's author? (The neighbor-identity table is the evidence to attack.)
b. Does reclassification-without-re-run fit within the "one protocol-amendment cycle" power, or is it gate-deletion-after-failure that the prereg's spirit forbids — forcing fallback?
c. Is freezing Edition I on A/C/D+F-1 sound, given the structural findings (§ 2) are disclosed on the badge?
d. R3's Edition-II criterion placement — correct per the second-attempt clause?

Return: **RATIFY / RATIFY-WITH-AMENDMENTS / BLOCK**, with reasoning. On RATIFY*, the package goes to Matt for the Edition-I freeze decision; on BLOCK, the fallback surface goes to Matt instead.

---

## 5. Cross-references

- Gate report: `agentic_orchestration/research/curated/atlas/2026-07-14-gate-report.md`
- Prereg v1.1: `agentic_orchestration/gandalf/design-inputs/2026-07-14-atlas-derivation-preregistration.md` (decision rule at "Decision rule (pinned)")
- Charter: `canonical/reap-die-rise-engine/atlas-derivation-charter-2026-07-14.md` (§ 5 pipeline, § 10 fallback clause)
- Failure taxonomy lineage: commit 1bf4c2c9 (38-negative taxonomy — 12 patterns, 3 red laws, amber ~2/3 extrinsic)
- Feel-layer tranche 1: `agentic_orchestration/research/knowledge/feel-layer/2026-07-14-feel-layer-tranche1-confirmed-groups.md` (naming lexicon; corroborates the two overlap border-cases)

Tracker-delta: see § 6.2 — consolidated by gandalf into `current-to-end-state-engine.md` SESSION-DELTA 2026-07-14 (pipeline executed; 3/4 gates; B-diagnosis pending jack-ryan review; Edition-I freeze BLOCKED on ruling).

---

**Signed:** gandalf (DRIFT-CRITIC verdict · SPEC-AUTHOR proposal · conflict declared § header)
**For:** converting a reversed gate into an honest ruling surface — review by the one agent with no stake in this map passing.
