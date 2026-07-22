# elrond probe brief — Faction-coalescence census on the 270-kit corpus-of-record

**Commissioned:** gandalf (STORYWRIGHT / conductor), 2026-07-21 — **Matt-authorized empirical test**, verbatim: *"we would need to test to see how many factions accrue from our 270 kits, and if they have the specific relationship available where each adversary is also naturally a direct enemy of two factions."*
**Mode:** READ-ONLY analytical probe. No schema changes, no DB writes, no crawls.
**Deliverable:** `agentic_orchestration/elrond/notes/2026-07-21-faction-coalescence-probe.md` — ≤2 pages of findings + appendix tables. Auto-commit (no push).

---

## Context (self-contained)

Matt ruled the Archive-Frame motive fork **RESCUE** (2026-07-21) and added a faction layer: the archive's contents war among themselves (Night-at-the-Museum grammar — factions fight each other AND see the player as an adversary; a third devourer force sits outside the faction graph, hostile to all). Design intent: **kit element + stats stay exact-original** (corpus-of-record fidelity); **race + faction coalesce in the serial content engine** as an emitted social layer OVER preserved mechanics. As the player saves each kit they *become* that faction's member (faction rides the body — serial identity §23.3).

Before any faction design fires, the substrate votes: **how many factions accrue naturally from the 270 record kits, along which axis, and does the axis admit the war-graph topology Matt requires?**

**Known priors you should honor, not re-derive:**
- Edition I (frozen 2026-07-14): kit-space is a *continuum with condensations* — Leiden shatters, LCA k=3. Mechanical geometry does NOT yield discrete families.
- Gate C: franchise R² = 0.076 — mechanics do not follow game-of-origin. (Consequence: lineage/era-coalesced factions would each SPAN the atlas — mechanically diverse factions. That is the desired property, worth quantifying.)
- Q21 ruling: NO element mapping ever in the corpus schema — element is a free axis assigned at emission. This probe does NOT build a mapping; it *censuses evidence* (see Q3).

**Record subset:** `kit_master WHERE game IN ('d2','gd','poe1','poe2','le')` — verified 60/41/37/94/38 = 270. DB: `agentic_orchestration/research/curated/corpus.db` (your SSOT; the atlas/ copy is derived). Atlas coords: `agentic_orchestration/research/curated/atlas/atlas.json` (Edition I, dims PERFORM↔DEPLOY / EMBODY↔LAUNCH).

---

## The questions

### Q1 — Coalescence census per candidate axis (the core)
For each candidate faction-coalescing axis available in schema (map to real columns yourself — you own the schema):

1. **source-game** (`game`)
2. **class/mastery lineage** (whatever encodes source class — `lineage`, dossier fields, kit_id prefixes)
3. **era** (`eras` field; else release-era per source game)
4. **delivery family** (the 7-column: PROJECTILE/ORBITAL/NOVA/ZONE/BEAM/MELEE/SUMMON)
5. **movement row** (FREE-MOVE/WALK/ROOTED)
6. **role-orientation** (damage/control/hybrid)
7. **elements_attested** (as a categorical — primary attested element per kit where recoverable)
8. **mechanical clustering** (k-sweep k=3..12 on frozen Edition-I coords, record subset only; report silhouettes — expected weak per the prior, but this IS Matt's "how many factions accrue" under the mechanical reading, so report it honestly)

Per axis report: **k** (distinct groups on the record subset) · **size distribution** (min/median/max + the full counts) · **within-group atlas spread** (per-group dispersion on dims 1–2 vs. global — are groups mechanically diverse or mechanically narrow?) · **orphan/NULL coverage** (% of the 270 unkeyed on that axis).

### Q2 — War-graph feasibility per axis
Matt's topology requirement formalized: enemy-graph **minimum degree ≥ 2** per faction ("each adversary is also naturally a direct enemy of two factions"). Cycles satisfy it minimally (C_n = exactly 2 each); odd cycles give triangles → natural three-way fights. Per axis, brief analytical judgment: does the axis admit a NATURAL enmity relation (wheel/cycle/adjacency/opposition) reaching min-degree ≥2 **without arbitrary forced edges**? (Element wheels and era-adjacency are the obvious natural candidates; game-of-origin has no natural enmity; say so where true.) The devourer force sits OUTSIDE this graph (hostile-to-all is trivially assignable) — exclude it.

### Q3 — Element-evidence coverage (descriptor feasibility, NOT a mapping)
What fraction of the 270 carry recoverable original-element signal in `elements_attested` (+ any auxiliary evidence: names, dossier text)? Report coverage % per game and overall, and multi-element ambiguity rate. This feeds a possible future `original_element` *descriptive* field for record-kit fidelity presentation (engine's free element axis untouched — Q21 stands).

### Q4 — OM-7 rider: era-coordinate feasibility
Per-kit era tag: is release-era-per-source-game sufficient (coarse, free — 5 games ≈ 5-6 era buckets 2000–2025), or does per-kit expansion-level dating exist in the data (`eras`, citations)? Rough cost estimate for the finer grain. (This answers the Archive-Frame's era-descent gating question routed to you.)

### Q5 — Top-line synthesis (one paragraph)
"How many factions accrue naturally, per axis" — a single ranked read: which 1–2 axes best satisfy (a) sensible k (roughly 4–10 factions), (b) tolerable size balance, (c) high atlas-diversity within factions, (d) natural ≥2-degree enmity. **Do not pick the faction design** — rank the empirical fitness; the design ruling is Matt's, downstream.

---

## Guardrails
- READ-ONLY. No new tables, no writes, no schema edits (`corpus_class` enum still rides the next KR wave — untouched here).
- Report what IS; keep "should" out of Q1–Q4 (Q5 is the one synthesis paragraph).
- If a candidate axis is unrecoverable from schema, say so in one line and move on — absence is a finding.

**Sign-off target:** elrond, findings doc committed with prefix `elrond: faction-coalescence probe — 270-kit census`.
