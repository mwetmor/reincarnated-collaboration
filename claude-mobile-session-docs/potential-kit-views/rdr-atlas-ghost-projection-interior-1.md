# Atlas memo — Ghost grain & placement: keep 7, fix the projection (INTERIOR-1)

> **STATUS:** ANALYSIS MEMO · RECOMMENDATION-FORWARD — authored 2026-07-15 from the Edition-I r3 ghost-field review. Scope: the ghost lattice's coordinate grain (7 of 14) and the placement of ghost cells on the frozen plane. Tags: **[ANALYSIS]** = assessment of what stands, **[RECOMMENDED]** = author's steer with reasoning, **[OPEN — RULING NEEDED]** = fork for the team.
>
> **The question, and the answer in one paragraph:** should ghosts carry 14 coordinates instead of 7? **No — 7 is the correct census grain, and 14 is not merely worse but category-incoherent for what a ghost is.** The real defect the question surfaced is elsewhere: ghosts at 7 coordinates are *positioned* by an average over present categories, which shrinks every ghost toward the origin and makes the field extremes-blind by construction. Keep the grain; fix the placement. The fix (**INTERIOR-1**) borrows the missing coordinates' information only where the law ledger already supplies it, at sampling-script cost, with the 192 lit cells available as free calibration ground truth.

---

## §1 — Why 7 is the correct census grain **[ANALYSIS — endorse current design]**

A ghost is a **neighborhood, not a kit** — a 7-coordinate equivalence class (movement × delivery × treatment × function × proxy × activation × dependency) holding 55,755–74,340 exact-grain kits. Promote it to 14 coordinates and it becomes one exact kit specification; the dark population goes from 10,080 cells to 693,146,160. Three things die at once:

- **The render dies.** ~693M dots is a uniform gray wash in which 469 lit points drown. The Mendeleev-visible property exists *because* the dark is enumerated coarsely enough to see.
- **The census claim dies.** At exact grain essentially every cell is unlit (469 vs 693M), so "unexplored" becomes trivially true of everything and therefore meaningless. Dark only carries information at a grain the genre's footprint could plausibly have covered: **192 of 10,080 is a real, checkable statistic; 469 of 693M is a tautology.**
- **The vetting dies.** The 1,260 sealed cells exist because feasibility curation was tractable at meso grain. Cuts cannot be ratified over 693M cells, and dark that hasn't been vetted is not honest dark.

The grain is not a compromise — it is chosen so that *"the genre never stood here"* is a non-trivial assertion. Too coarse and everything is lit; too fine and everything is dark; 7 is where the signal lives. **No change requested to the census layer.**

## §2 — The placement bias: co-location is half real, half artifact **[ANALYSIS]**

The observation that ghosts "occupy the same space as the kits" is correct in the settled center and false at both edges — and the two edges mean opposite things.

**Mechanism.** A supplementary point built from 7 of 14 variables is positioned at the **average of its present categories**; the seven masked variables (geometry, commit, range, tempo, …) contribute nothing. Every ghost is therefore pulled toward the origin regardless of where its full-grain interior actually lives. Kits cluster mid-plane because the genre's kits genuinely have mixed profiles; ghosts cluster mid-plane because *half their profile is masked*. Two mechanisms, one overlapping picture — and the plane cannot distinguish a genuinely-central ghost from a central-because-masked one.

**The three zones this produces:**
1. **Settled country** (center): co-location is real — those meso cells genuinely neighbor real kits.
2. **True frontier** (gray outruns color — e.g. the 49-cell wedge): real, vetted, unlit ground.
3. **Blind strip** (color outruns gray — the six kits beyond ghost reach at x = 1.258): pure lattice bias. Dark may exist out there; the lattice structurally cannot draw it.

**Why the naive fixes are both wrong.** Adding the 7 masked coordinates is §1's category error. Rescaling the average (e.g. ×14/7) pushes *all* ghosts outward uniformly — including genuinely-central ones — manufacturing fake frontier. Neither injects information; the second injects noise. The correct fix injects the information that already exists: **the constrained shape of each ghost's interior.**

## §3 — **INTERIOR-1**: feasibility-weighted interior projection **[RECOMMENDED]**

Position each ghost at the centroid of a sample of its **feasible interior**, rather than at the average of its stated categories.

**Spec:**
1. For ghost cell *g* (7 fixed categories), define its interior *I(g)*: all completions over the 7 masked coordinates that survive (a) the ratified feasibility cuts, (b) finer-grain sealed exclusions where applicable, and (c) RED laws that couple masked coordinates to present ones (e.g. **RED-3′** couples movement verbs to commit — for movement-verb ghosts, the commit marginal excludes the sealed combinations).
2. Sample K members uniformly from *I(g)* (K = 256–512 is ample for a stable centroid; exact enumeration if the constraint structure factorizes — it likely does, since cuts are largely per-coordinate/pairwise).
3. Project each sampled member as a **full 14-coordinate supplementary point** onto the frozen basis — zero-mass, axes untouched, same guarantee as today.
4. **Ghost position = centroid of the sampled projections.** Optionally retain the sample spread and render a faint log-scaled extent smear, so a ghost reads as the *region* it is rather than the point it isn't.
5. Emit per-ghost **constraint displacement** = |new − old| position. This scalar is itself ledger-worthy: it measures how strongly the law ledger binds that cell.

**Why this is the right shape of fix:**
- **Graceful degradation.** Where the interior is unconstrained, uniform imputation over centered category coordinates contributes ~0 in expectation → placement ≈ current behavior. The mixed middle does not move.
- **Moves exactly the right dots.** Cells whose interiors are law-bound toward extremes — the wedge's "one narrow core recipe" cells, movement×commit-coupled cells — migrate outward toward where their members actually live. The extremes-blindness is repaired *only* where evidence exists to repair it.
- **Cost.** A sampling script over existing cut/law tables plus a galadriel render pass. No new lattice. No combinatorial explosion.

**Pre-registered validation gates (freeze INTERIOR-1 only if these pass):**
- **G-i (calibration on lit ground):** the 192 lit cells have known truth — project each lit cell's feasible interior and compare its centroid to the mean position of its actual member kits. Report the displacement distribution; it should be small and unbiased. *This is free ground truth; use it before trusting any dark placement.*
- **G-ii (degradation):** unconstrained ghosts move < ε from current placement.
- **G-iii (direction sanity):** wedge ghosts migrate consistently with their named recipes (BEAM × taunt tuples toward PERFORM, etc.).

**Invariants preserved:** the census is untouched (still 7-coordinate cells; still 10,080 / 192 / 1,260); zero-mass is untouched (axes never move); the frame stays frozen (clip, don't rescale); **RIDER-1** still badges the plane — interior placement improves *where* a ghost renders, it does not upgrade plane proximity into kinship.

## §4 — Ghost horizon **[RECOMMENDED — cheap; do regardless of §3]**

Draw the **reach boundary of the ghost lattice** on the plane — a faint dashed envelope (convex hull or per-direction max-reach) labeled to the effect of: *"ghost coverage limit — dark beyond this line is unmapped at meso grain, not absent."* Today that boundary ends at x = 1.258 with six real kits beyond it; without the line, the render invites the exact misreading the wedge analysis had to correct in prose ("no dark here" ≠ "mined out"). If INTERIOR-1 lands, the horizon expands where laws bind — re-emit it per edition alongside the badge.

## §5 — Local drill-in lattices **[OPEN — Edition-II RULING NEEDED]**

The full fix for extremes-blindness is finer ghost grain, but globalizing geometry+commit multiplies the whole 10,080-cell lattice and re-triggers §1's vetting problem. **[RECOMMENDED shape]:** scoped **drill-in lattices** — promote to 9 coordinates only within selected regions (e.g. the 49-cell wedge × geometry × commit ≈ hundreds-to-low-thousands of cells, vettable). Rulings needed: (a) the region-selection rule (proposal: the k dark cells nearest each condensation's extreme, per basis distance); (b) the coordinate pair *per region* — the wedge analysis argues geometry+commit there, but the deepest-PERFORM beam column may want commit+tempo. Leave pair-choice per-region rather than fixing one pair globally.

## §6 — Adjacent items surfaced in the same review (logged, one line each)

- **Defended zero (pre-publication requirement for the wedge claim):** red-team the 29-cell hybrid-treatment finding against player-assembled near-misses (PoE CwC-Cyclone, curse-on-hit spins, LE Warpath ailment assemblies); write the **rider-proc ≠ treatment-hybrid** taxonomy line *before* any public surface, and annotate the wedge with the examined-and-excluded list. The strongest negative claim ships with its exclusion work attached.
- **Headline statistics:** lead with **192 / 10,080 ≈ 1.9% of feasible meso ground ever built** and the companion **469 / 192 ≈ 2.4 kits per lit cell** ("the genre didn't explore; it remade"). Keep 693M as flavor only — exact-grain denominators read as combinatorial inflation under scrutiny.
- **Iconicity-as-consensus** (from the wedge analysis's Truth 1): *maximal coordinate consensus = maximal fantasy legibility = far-corner position* is a testable hypothesis — icon status should correlate with basis-distance from centroid along consensus directions; checkable against external popularity data in a future edition.

---

**Division of labor suggestion:** INTERIOR-1 sampling + gates = atlas pipeline (build_atlas_json_edition*.py side); horizon + extent smears = galadriel render; §5 rulings = wherever Q30-class grain decisions are owned. Census layer: no change.

**One-line summary for the ledger:** *Grain stays 7 (census is honest); placement gains interior information (INTERIOR-1, gated on the 192 lit cells); the horizon gets drawn so absence of gray is never read as absence of ground; drill-ins go local, not global.*
