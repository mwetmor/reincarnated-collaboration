# Dispatch — 2026-05-16 — gandalf — Drift-14 Track B: pool-cull + selector hard-floor design-side synthesis

**From:** knight-rider (authored per Matt directive Day-4 close: Drift-14 VS2a-gating cascade; legolas Track A returned 2026-05-17 with comprehensive empirical inputs)
**To:** gandalf
**Approved by:** Matt at 2026-05-17 (fire authorization granted post-legolas-Track-A-return)
**Status:** READY-TO-FIRE — legolas Track A inputs landed; cascade proceeds.
**Estimated effort:** ~2-3h (design-side synthesis; possibly authoring a small rocket dispatch as side-output)

**Gate-1 bypass rationale:** Matt-directed (Drift-14 VS2a-gating per gandalf commit 8a89d1b reclassification + Matt Day-4 close authorization); single-seam (gandalf-only canonical authorship); reversible (canonical doc + dispatch authoring; no production state modified); follows critique-pair pattern.

**Acceptance summary:** Track B design-side synthesis consuming legolas Track A empirical findings (`agentic_orchestration/research/knowledge/pool-vfx-coverage-audit-2026-05-16.md` — or the inline-delivered equivalent if doc was not filed at canonical path; see Required reading). Produces: (a) **pool-cull execution list** (which of the 27 candidates land in the cull; rationale per entry; any keeps with mitigations); (b) **selector hard-floor amendment spec** (D1 rubric changes — `canonical_pair_leak` property, `vfx_catalogue_mapping_clean` boolean gate, wind-storm cluster effective-selection-probability floor); (c) **vendor-acquisition prioritization** (which of the top-3 picks proceed, on what timeline); (d) **PATH-D1 sequencing call** (does the pool-cull need to ship BEFORE / WITH / AFTER any Stage 3 follow-on); (e) IF rocket-side amendment recommended, **author a rocket dispatch** at `agentic_orchestration/dispatches/2026-05-1x-rocket-selector-hardfloor-and-pool-cull-execution.md` ready for knight-rider routing.

---

## Why this dispatch exists — Drift-14 cascade resolution

Per gandalf commit `8a89d1b` § Drift-14 re-amendment:

> **D1 rubric pushes selector toward canonical-four conformity → form-bias instance the Stage 1 work was supposed to close at the player-facing surface.**

Per Matt Day-4 close directive: "We need the elements to map cleanly across 2D VFX and to halt LLM API confusion around canonical pair visibility."

Track A (legolas, RETURNED) gathered empirical data:
- 156 pool entries audited; 47.4% GREEN / 35.3% YELLOW / 17.3% RED
- 27 cull candidates including 7 critical allow-list (chitin/scale/horn/tooth/claw/throne/marrow at d1_total 9-11)
- 15 HIGH canonical-pair-leak entries (wind-storm cluster of 8: hurricane/gale/cyclone/tempest/gust/howl/typhoon/squall)
- Wind worst-affected slot (28.9% RED); fire cleanest (78% GREEN)
- Vendor coverage: Pimen 92.6% / Pixogen 90.6% / Fellor 68.5% / CraftPix 63.8%
- **Novel finding PATH-D1**: D1 rubric offline scoring path upstream of all 48 runtime sites in cipher-migration paths-audit — pool composition fix must precede/co-ship with Stage 3 for full Drift-14 closure

Track B (this dispatch) is the DESIGN-SIDE SYNTHESIS — empirical findings → canonical decisions → execution-ready specs for downstream seams.

## Cross-seam contract change?

**Round-trip: not applicable for Track B itself** — gandalf is authoring canonical-side specs; no production state modified during synthesis. However:

- **IF rocket-side amendment is recommended:** the rocket dispatch you author MUST flag the cross-seam contract implications. D1 rubric changes touch the pool-eligibility scoring (gamora simulation consumes via balance-loop selection; star-lord LLM-bound paths consume via prompt construction; drax consumes via VFX-mapping at render). MIGRATION.md likely required for that downstream dispatch.
- **IF pool entries are removed from allow-list:** flag for star-lord prompt-template audit (any hard-coded element names in LLM prompts that match removed entries?) — surface as side-routing item to knight-rider, do not author star-lord dispatch yourself.
- Per R11(b) Principle 6.

## What this dispatch produces

### Section 1 — Pool-cull execution list (canonical-side decision)

Land a canonical decision per legolas-flagged candidate. For each of the 27 cull candidates:

- **CULL** (entry leaves allow-list → demoted to eligible OR quarantine OR removed entirely)
- **KEEP** (entry stays; document mitigation that addresses leak/coverage concern)
- **DEFER** (entry needs further investigation before decision)

Cull decisions for the **7 critical allow-list entries** (chitin / scale / horn / tooth / claw / throne / marrow at d1_total 9-11) warrant explicit per-entry rationale — these scored well on the existing D1 rubric, so culling them implies the D1 rubric itself was undermeasuring leak risk (validates the rubric-amendment work below).

Wind-storm cluster (8 entries) warrants cluster-level reasoning — these are tightly thematically related; partial culls may concentrate selector pressure on the survivors, creating new bias patterns. Recommend cluster-level decision (cull-all, keep-1-as-representative, or rebalance with new non-leak alternates).

File the cull decisions in: `canonical/story/drift-14-pool-cull-decisions-2026-05-17.md` (or similar canonical-side filing per your discretion).

### Section 2 — Selector hard-floor amendment spec (rubric-side)

Per legolas top-3 selector hard-floor recommendations, author the D1 rubric amendment spec:

- **`canonical_pair_leak` property:** new D1 dimension scoring whether a name structurally implies canonical-four pair binding. Define: scoring criteria (lexical-pattern match? embedding-distance? hand-curated leak-set?); 0-N scale or boolean? interaction with existing d1_total composite?
- **`vfx_catalogue_mapping_clean` boolean gate:** required-true for allow-list status. Define: how is "mapping clean" measured at scoring time (does it require a live catalogue lookup, or a pre-computed catalogue-coverage manifest cached in source-of-truth)? what happens if catalogue coverage status changes (vendor acquired/dropped)?
- **Wind-storm cluster effective-selection-probability floor:** mechanism for capping aggregate selection-probability across a thematically-clustered set. Define: how is "cluster" defined (tag-based? embedding-based? hand-curated cluster manifest?); what's the floor value (e.g., max 20% combined selection-probability across cluster); does this generalize to other thematic clusters or is it wind-storm-specific?

Surface implementation trade-offs: which of these is cheapest to ship + delivers the most Drift-14 leverage; which is most expensive but architecturally cleanest; what's the minimum-viable cut.

### Section 3 — Vendor-acquisition prioritization

Per legolas top-3 vendor-acquisition recommendations:
- CraftPix premium (wood-nature substrate)
- Frostwindz Deathbringer (bone)
- Fellor Crystal pack (gem cluster)

Land decisions:
- **ACQUIRE** (proceed; assign to Matt for license/cost approval if applicable)
- **DEFER** (note conditions for revisit — e.g., "if quarterly asset budget allows")
- **DECLINE** (not aligned with VS2a/VS2b roster; document why)

Sequencing: do acquisitions need to land BEFORE pool-cull (replacing culled coverage)? AFTER (filling gaps surfaced by post-cull D1 re-scoring)? In-parallel (independent)?

### Section 4 — PATH-D1 sequencing call

Per legolas novel finding: D1 rubric is upstream of all 48 runtime sites in the cipher-migration paths-audit. Sequencing question:

- **Pool-cull BEFORE Stage 3 follow-on:** clean state before any further Stage-3-style work
- **Pool-cull WITH Stage 3 (combined):** ship both in same migration window; single coordinated cascade
- **Pool-cull AFTER Stage 3:** Stage 3 work proceeds; pool-cull is a follow-on hygiene pass

Make the call + document rationale. Note any dependency-graph implications for the combined post-cascade gamora regen (it's currently gated on this Track B return; sequencing call affects how/when the regen consumes the pool-cull state).

### Section 5 — Downstream rocket dispatch authoring (conditional)

**IF** Section 2 (rubric amendment) is recommended for execution, **author a rocket dispatch** at:
`agentic_orchestration/dispatches/2026-05-17-rocket-drift-14-pool-cull-and-selector-hardfloor-amendment.md` (or appropriately-dated)

Dispatch should specify:
- Pool-cull execution (apply Section 1 decisions to rocket-owned element source-of-truth)
- D1 rubric amendment implementation (per Section 2 spec)
- Re-scoring run + validation (does post-amendment D1 scoring match Section 1 cull decisions, or surface new candidates?)
- MIGRATION.md cross-reference (cross-seam impact on gamora + star-lord)
- Smoke + tag intent
- Co-author with knight-rider (Gate-1 friendly to fire post-Matt-approval)

**IF** Section 2 surfaces an architecturally-novel amendment that needs Matt-decision before rocket can execute, surface for routing instead of authoring the dispatch yourself.

### Section 6 — Hand-off summary for knight-rider

Single-paragraph summary capturing:
- Pool-cull count (cull / keep / defer breakdown)
- Selector hard-floor amendment cut shipped (minimum-viable vs full)
- Vendor acquisitions queued for Matt-approval
- PATH-D1 sequencing decision
- Rocket dispatch authored (yes/no + path if yes)
- Any side-routing items for star-lord prompt-template audit

## Out of scope (explicit)

- **NO execution of pool-cull on rocket-owned source-of-truth** (rocket's seam; via the dispatch you author or knight-rider routes)
- **NO D1 rubric code changes** (rocket's seam)
- **NO LLM prompt-template edits** (star-lord's seam; surface as side-routing if needed)
- **NO MIGRATION.md authoring beyond cross-reference** in the rocket dispatch
- **NO drax-side VFX-asset wiring work** (separate workstream; only surface vendor-acquisition prioritization as canonical decision)
- **NO new legolas crawls** (work from Track A inputs; if gaps surface, route via knight-rider for Mode A follow-on)
- **NO V2 calibration epoch declaration** (separate Matt-decision; Drift-14 closure is one input among many)
- **NO new ADRs** (canonical-doc updates are sufficient; ADRs are reserved for cross-seam process changes)
- **NO authoring of canonical story content beyond Drift-14 closure docs** (other gandalf workstreams — story arc, naming triad, court framing — are separate)

## Required reading

- **Legolas Track A return** — primary input. Located inline in agent return (per legolas persona rule deliver-inline-over-file); also potentially at `agentic_orchestration/research/knowledge/pool-vfx-coverage-audit-2026-05-16.md` IF Track A subsequently filed there. **If canonical-path file is missing, you may need to ask knight-rider to surface the inline-delivered content from the prior session.**
- **Your own commit 8a89d1b** § Drift-14 re-amendment + § Case 4 re-amendment (VS2a-gating reclassification; rationale for why pool composition is structural-canonical-bias source)
- **Form-bias cipher migration paths-audit:** `agentic_orchestration/research/cipher-migration-paths-audit-2026-05-16.md` (48 runtime sites; PATH-D1 is the novel upstream path)
- **Star-lord Stage 3 cipher migration MIGRATION.md** (the engine-side closure; understand what Drift-14 says was structurally-incomplete)
- **Rocket-owned element source-of-truth** (likely `~/Games/reincarnated-engine/src/reincarnated/foundation/` or `element/` or `generation/`) — verify the element-name pool schema before authoring rubric-amendment spec
- **Engineering disciplines** `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — especially R11(b) (cross-seam round-trip discipline) + #1 (math-before-code) + Drift-11 (sibling-cluster-sweep prescription — wind-storm cluster is a sibling-cluster instance)

## Acceptance criteria

- [ ] Pool-cull execution list complete (per-entry decision + rationale for 7 critical allow-list + cluster-level decision for 8-entry wind-storm cluster)
- [ ] Selector hard-floor amendment spec authored (minimum-viable vs full cut surfaced)
- [ ] Vendor-acquisition prioritization landed (3 picks with decisions)
- [ ] PATH-D1 sequencing call documented with rationale
- [ ] Rocket dispatch authored at canonical path IF rubric amendment recommended (or surface-for-routing if architecturally-novel)
- [ ] Canonical-side filing complete (`canonical/story/drift-14-pool-cull-decisions-2026-05-17.md` or similar)
- [ ] Cross-seam side-routing surfaced (star-lord prompt-template audit if applicable)
- [ ] Knight-rider notified with: cull count breakdown, amendment cut shipped, acquisition decisions, sequencing call, rocket dispatch status, side-routing items

## Tag policy

- **No git tag** (gandalf persona; canonical-doc commits + dispatch authoring are the artifacts)

---

## Completion record

**Completed:** _<date>_
**Pool-cull breakdown:** _<n cull / n keep / n defer>_
**Critical allow-list (7) disposition:** _<per-entry summary>_
**Wind-storm cluster decision:** _<cull-all / keep-1 / rebalance / other>_
**Selector hard-floor cut shipped:** _<minimum-viable / full / hybrid>_
**Vendor acquisitions queued for Matt:** _<list with rationale>_
**PATH-D1 sequencing:** _<before / with / after Stage 3>_
**Rocket dispatch:** _<authored at path / surfaced for routing / not needed>_
**Side-routing items:** _<list or "none">_
**Canonical doc filed:** _<path>_
**Notes for knight-rider:**
