# elrond charge — GRAIN LAW ratification (Part A) + Archipelago Mock on E1-469 (Part B) — FIRED

**From:** gandalf (SPEC-AUTHOR) · **Date:** 2026-07-16 · **Status:** FIRED
**Authority:** Matt rulings 2026-07-16, verbatim: (1) *"Exclude the Minecraft Dungeons kits entirely."* (2) *"On Lost Ark, yes we CANNOT emit full classes… I would recommend deleting these entirely rather than decomposing."* (3) *"I do approve of the archipelago strategy."* All three logged in `canonical/matt_decision_needed/2026-07-16-edition3-vs-refit-candidate-1-adoption.md` § RULING.

## Part A — GRAIN LAW (corpus.db + atlas MIGRATION.md; do this FIRST — Part B consumes it)

1. **Add a `grain` column** to the corpus kits table (or the correct curation table — your schema call, disclosed in MIGRATION). Vocabulary: `kit` | `gear` | `class`. **Derive per-row from provenance, don't assume:** mcd rows (expect 120 incl. the 26 no-key) → `gear` · LA class-grain rows (expect 56) → `class` · LA Destroyer skill-grain rows (expect 6) → `kit` · everything else → `kit` unless the row's own provenance says otherwise. Any row you cannot confidently classify → leave NULL + flag list in your return. Do NOT guess.
2. **Record the GRAIN LAW in atlas `MIGRATION.md`** with Matt's verbatim rulings 1+2: *corpus grain = emission grain. The engine emits kits; the atlas plots what the engine can emit. Every future fit-stage predicate MUST include `grain = 'kit'`.* One law implements both rulings and closes the failure class that contaminated Refit-Candidate-1 (manual fit-stage holds do not survive predicate rewrites; a ratified column does). Note the grain-based-not-source-based reading (Destroyer 6 survive) as gandalf's flagged interpretation.
3. **Rows stay catalogued INERT** — catalogue philosophy: score/filter at consumption, never purge. NO deletion from corpus.db.
4. **Iron laws:** Edition III + every served artifact READ-ONLY · Refit-Candidate-1 artifacts READ-ONLY (permanent evidence exhibit — Matt's ruling 1 makes it never-adoptable) · no re-fit or re-emission of ANY existing atlas artifact in Part A.

## Part B — Archipelago mock (E1-469 · MOCK — NOT RATIFIED · nothing served, nothing vendored)

Purpose: Matt approved the strategy sight-unseen; the mock shows what the territory surface looks like and answers his membership-census question with real numbers. Throwaway-class exhibit: one JSON + one short report; galadriel renders AFTER gandalf's verify gate; serving untouched.

0. **Corpus assert (fail-loud, uses Part A's column):** mock corpus = Edition I's 469 active kits, exactly. Assert all 469 grain=`kit`; assert zero mcd-source rows; report LA composition (expected zero — the 62 LA rows are post-E1 growth). HALT if any `gear`/`class`-grain row is inside the 469; merely REPORT if kit-grain LA rows appear.
1. **Cluster in FULL mechanical space** — the retained-dims space or full standardized feature space, your call, disclosed. NOT the 2D plane. Method: Leiden on kNN graph (existing `leiden_cluster` machinery) or HDBSCAN — your call, disclosed; HDBSCAN's noise labels map natively to drifters.
2. **Family labels:** seed from the 86 gateA ratified family labels. Label propagation to unlabeled kits with confidence threshold τ **calibrated on a gateA holdout** (~20% of the 86 held out; τ maximizes holdout assignment accuracy with abstention allowed; disclose the τ curve + holdout accuracy in the report).
3. **Five-strata assignment** for all 469 + ghost cells: island CORES (τ-confident family members) · unnamed ISLETS (clusters carrying no gateA seed — label `U-1, U-2, …`) · STRAITS (split affinity between two families within margin m — disclose m) · DRIFTERS (noise / below-τ, no strong match) · GHOST shallows vs deep (feasible cells shaded by family affinity; deep = no family within affinity radius — the frontier).
4. **Seating (TERRITORY surface — memberships computed, seating designed-for-legibility, disclosed as such IN the JSON):** MDS on cluster centroids (full-space distances) → island positions · within-island local layout · water by fiat spacing · tombstones (graveyard kits) seated on their HOME island per Finding F-1 (kit death is not geography).
5. **Emit:** `agentic_orchestration/research/curated/atlas/atlas-archipelago-mock.json` (points + strata + island seats + ghost affinities + census block + a `mock: true, ratified: false` stamp) and `archipelago-mock-report.md` whose FIRST table is the **ashore/at-sea census**: islands (named six) / islets (U-n) / straits / drifters counts + per-family core sizes + ghost shallows-vs-deep cell counts.
6. **G1/G2/G3 ratification gates are NOT run in the mock** (charter-run, pre-registered). State this in the report so nobody reads the mock as ratified.

## Return contract

≤20 lines: Part A grain census (counts per grain value + flag list) · MIGRATION entry confirmed · Part B ashore/at-sea census headline numbers · τ + holdout accuracy · cluster method + count · paths · commit hash. Auto-commit. **NO push.** HALT conditions: grain-ambiguous rows > 20 (return the list, await ruling) · Part B step-0 corpus assert fails · degenerate clustering (one cluster > 60% of kits — report, don't force structure).

**Signed:** gandalf — the law makes the rulings permanent; the mock buys the census with real numbers.
