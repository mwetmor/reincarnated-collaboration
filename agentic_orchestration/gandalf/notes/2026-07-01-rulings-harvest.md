# Matt-Rulings Harvest Audit — canonical/story/ purge support

**Date:** 2026-07-01 · **Purpose:** classify every Matt ruling carried in `canonical/story/*.md` as CAPTURED / SOLE-CARRIER / STALE before the purge. Docs delete by default; a doc that is the sole carrier of a Matt ruling must have that ruling harvested to a ledger first.

**Carriers checked (the four ledgers):** (a) `~/Games/reincarnated-engine/design/decisions/decisions-log.md` · (b) `canonical/current-to-end-state/current-to-end-state-story.md` PART A · (c) `canonical/reap-die-rise-story/` + `canonical/reap-die-rise-engine/` spec docs · (d) `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`. "Captured" = decision CONTENT present, exact wording not required.

**Method:** specified regex (`matt.{0,60}(ruled|ratifi|approv|directive|amend|confirmed|verbatim)`) → 225 hits across 53 of 71 docs; the 18 no-hit docs were swept with loose `\bmatt\b` grep, recovering **10 more docs with real Matt canonical calls the regex missed** (noun-forms like "Matt ruling", "canonical call", "pre-authorization"): attribute-system, v1-bc-target-intent, skill-system, off-hand-items, gear-heavy-promotion, representative-loadout-measurement-contract, stat-derivation-from-bc-convergence, legacy-categorical-cleanup-audit, gear-substrate-rule-table-v1, bdi-omega-tau-tables-v1 (+ engine-as-general-serial-content-product, captured elsewhere). Distinct-ruling dedupe applied (e.g., the 2026-05-22-evening "six vestigial retirements" span 3 docs = 1 ruling family; the 6b-reference ruling spans 3 docs = 1 ruling).

---

## Summary

**~67 distinct Matt rulings** across 63 docs carrying Matt content (8 docs carry none):

| Classification | Rulings | Meaning |
|---|---|---|
| CAPTURED-AT a ledger/KEEP-spine doc | ~26 | safe — content already in decisions-log / PART A / spec docs / disciplines |
| SOLE-CARRIER (needs harvest) | ~28 | ledger row proposed below; doc deletable AFTER row lands |
| STALE (retired system) | ~13 | superseded by retitle/v2 slate, Godot seam, cycle-frame retirement — no harvest |

Authorization-only Matt approvals (work-firing, push-grants, Matt-gates with no design content) are marked AUTH-ONLY and need no harvest.

### Doc-level split — 45 SAFE TO DELETE vs 26 NEEDS-HARVEST

**NEEDS-HARVEST first (26 docs; each carries ≥1 sole-carrier ruling — harvest the proposed row(s), then delete):**

1. `weapon-substrate-composition-policy-v1-2026-05-24.md`
2. `six-profile-set-architecture-2026-06-16.md`
3. `representative-loadout-measurement-contract-2026-06-16.md` (shares 6b row)
4. `proxy-add-design-spec-2026-06-16.md`
5. `telegraph-dodge-temporal-decoupling-2026-06-15.md`
6. `battle-room-presentation-decoupling-2026-06-15.md`
7. `gear-spec-generation-deferred-architecture-2026-06-16.md`
8. `attribute-system-2026-05-24.md` (VIT-DELETE — in engine tracker but not a listed ledger)
9. `v1-bc-target-intent-2026-05-24.md`
10. `skill-system-2026-05-24.md`
11. `off-hand-items-2026-05-24.md`
12. `gear-heavy-promotion-2026-05-22.md`
13. `multi-dim-convergence-algorithm-2026-05-21.md`
14. `phase-5-llm-prompts-cohesion-judge-2026-05-27.md`
15. `phase-7-2-layer-joint-gate-spec-2026-05-27.md`
16. `2026-06-13-2d-spatial-golden-oracle-spec.md`
17. `2026-06-02-season-archive-realm-expansion-pivot.md` (delete already HALTED 2026-07-01 — live engine spine)
18. `2026-06-06-atomic-substrate-registry.md` (fold-map says KEEP → ENGINE/elrond; do not delete)
19. `2026-05-29-designer-writes-substrate-player-names-experience-principle.md` (route → disciplines)
20. `2026-05-31-hypothesis-flow-pattern-library-architecture.md` (route → disciplines)
21. `v1-1-plus-design-discipline-recognitions-2026-05-23.md` (route → disciplines parking)
22. `stat-derivation-from-bc-convergence-2026-05-22.md`
23. `legacy-categorical-cleanup-audit-2026-05-22.md`
24. `gear-substrate-rule-table-v1-2026-05-22.md`
25. `bdi-omega-tau-tables-v1-2026-05-22.md`
26. `style-register.md` (weak/demo1-scoped — see row)

**SAFE TO DELETE on Matt-ruling grounds (45 docs).** Every Matt ruling inside is captured, stale, or authorization-only:

- **Captured:** 2026-06-01-flavor-pool-per-primary-element-lock · 2026-06-01-gauntlet-metrics-as-provisional-hypotheses-recognition · 2026-06-07-earth-avatar-cosmograph-creation-moment-architecture · 2026-06-07-cosmograph-cross-surface-LOD-architecture · substrate-design-supplement-2026-05-21 · weapon-as-identity-surface-recognition-2026-06-14 · c-hybrid-cell-and-curation-architecture-2026-05-28 · qd-engine-bc-axes-lock-2026-05-20 · 2026-06-10-engine-greenfield-verdict-wrap-and-extend · 2026-06-11-forward-architecture-contract-wrap-and-extend · 2026-06-13-combat-fidelity-drift-proofing-and-2d-certification-wave · 2026-06-09-arpg-physical-magical-ratio-baseline · marginal-lineage-tagging-pattern-2026-05-23 · 2026-06-13-companion-as-hall-of-heroes-ally-commitment · 2026-05-29-experiential-cascade-architecture-recognition · 2026-06-10-engine-architecture-canonical-synthesis · tier-4-architecture-defaults-2026-05-22 · engine-as-general-serial-content-product-2026-05-22 · 2026-06-05-cosmograph-pivot (captured-as-superseded)
- **Stale (retired systems):** w1-13-rescope-disposition · visual-benchmark-vs2a · asset-pipeline-meshy-swap (Unreal seam) · fate-genre-recognition-and-mobile-alignment-trajectory · geometry-vfx-coverage-assessment (pixi/B11) · ab-comparison-protocol-cycle-14-close (cycle frame retired) · 2026-06-09-tal-rasha-glyphic-primitive-anchor (cosmograph presentation PARKED per A11) · seasonal-hero-h-5-hybrid-spec (seasonal-RELEASE model) · 2026-05-23-weapon-substrate-conclusion-declaration (v1.1+ queue framing; the one live half is captured)
- **Auth-only / no distinct Matt ruling:** 5 marginal-lineage dispositions (arctic-circumpolar, mesoamerican, n-am-indigenous, oceanic, south-american — elrond route) · cleaning-policy-design · variant-cluster-policy-assignments · thematic-registry · phase-5-t4-narration-amendment · phase-5-cohesion-judge-calibration-spec · loadout-analytics-suite-information-architecture · proxy-commander-set-6-capstone-spec · 2026-06-06-autonomous-fire-prompt-template (fold-map B holds it back anyway) · 2026-06-17-autonomous-run-plan-v2 (6b ruling harvested via row 2 below) · substrate-generalization-track-c-synthesis · styleprofile-output-shape-ruling (gandalf ruling, not Matt) · gear-spec-element-flavor-manifest-design-half (zero Matt content)

**Caveat on "safe":** several SAFE docs are on the reap-die-rise-engine 00-index Cluster-D fold list ("authoritative until folded") — ruling-harvest safety ≠ content-fold completion. This report clears the RULING dimension only; the fold worklist governs spec content. Also `qd-engine-bc-axes-lock` §3 and `2026-06-11-forward-architecture-contract` are pointed at BY ≥6 decisions-log entries as locked vocabulary / the contract — deleting them orphans ledger pointers even though ruling content is captured.

---

## Classification table (grouped by source doc)

Classifications: **C** = CAPTURED-AT (carrier named) · **SC** = SOLE-CARRIER · **ST** = STALE · **AUTH** = authorization-only. Proposed ledger rows target the decisions-log unless noted.

### Gear / stat / damage math (live)

| Source doc | Ruling (one line) | Class | Proposed ledger row if SOLE-CARRIER |
|---|---|---|---|
| `attribute-system-2026-05-24.md` | Matt 2026-06-24: VIT attribute DELETED — permanent 4-attribute frame STR/INT/WIS/DEX; Matt 2026-06-23: build-to-spec discipline for the attribute system | SC (present in `current-to-end-state-engine.md` III.10 — NOT a listed carrier) | "2026-06-24 — VIT DELETED; attribute frame locked at 4 (STR/INT/WIS/DEX), permanent. 2026-06-23 — attribute system builds TO SPEC (doc-42 partition), not exploratory. Source: attribute-system-2026-05-24 banner; also engine tracker III.10." |
| `stat-derivation-from-bc-convergence-2026-05-22.md` | Matt 2026-05-22 evening (Pattern 3 of six retirements): stats DERIVE from BC convergence, never pre-imposed; traits are NOT a v1 load-bearing surface (v1.1+ at most) | SC | "2026-05-22 evening — Pattern-3 vestigial retirement: stat sheets derive from converged BC coordinates; pre-imposed stat blocks retired; traits excluded from v1 load-bearing surface." |
| `gear-substrate-rule-table-v1-2026-05-22.md` | Matt 2026-05-22, three canonical calls: rule-table v1 adopted; "gear-archetype" naming retired; role_orientation retired as generation input (role emerges from 8 BC axes post-convergence) | SC | "2026-05-22 — gear-substrate rule table v1 ADOPTED (three calls): rule-table canonical; gear-archetype naming retired; role_orientation retired as input — role is post-convergence emergent." |
| `bdi-omega-tau-tables-v1-2026-05-22.md` | Matt 2026-05-22 pre-authorization A: BDI ω/τ tables adopted as v1 starting values, gated on H3 archive-correlation calibration | SC (weak — later gear math may supersede values; adoption ruling still uncaptured) | "2026-05-22 — BDI ω/τ table v1 adopted as starting values (pre-auth A); empirical H3 calibration gate attached." |
| `legacy-categorical-cleanup-audit-2026-05-22.md` | Matt 2026-05-22 evening: SIX vestigial-pattern retirement calls in one pass — categorical pre-imposition retired at role/archetype/stat/axis levels; axes must be DERIVED from statistically significant sample | SC (elrond-route for content; ruling uncaptured) | "2026-05-22 evening — six vestigial-retirement canonical calls: all categorical pre-imposition retired (role_orientation, archetype templates, pre-imposed stats, axis-level aesthetic/mechanical categories); axes derived from sample, not declared." |
| `gear-heavy-promotion-2026-05-22.md` | Matt 2026-05-22, three calls: gear promoted LITE→HEAVY surface; vast-library pivot; 15-catalogue architecture retired | SC | "2026-05-22 — gear promoted LITE→HEAVY (load-bearing v1 surface); vast-library pivot adopted; 15-catalogue architecture RETIRED." |
| `2026-06-13-2d-spatial-golden-oracle-spec.md` | Matt certification dispositions: 2D-spatial golden-oracle is the authority for spatial kernel changes; cert scope locked | SC | "2026-06-13 — 2D-spatial golden-oracle cert dispositions ratified: oracle = binding reference for spatial kernel change verification (kernel-change protocol instrument)." |
| `2026-06-13-combat-fidelity-drift-proofing-and-2d-certification-wave.md` | Masking-methodology: drift detectors DETECT → FLAG-AND-DEFER (not auto-fix) | C — decisions-log | — |
| `qd-engine-bc-axes-lock-2026-05-20.md` | 8-axis BC lock + D1–D6 dispositions ("The 8-axis BC lock is sound") | C — decisions-log QD hive-activation entry; §3 cited by ≥6 later entries as locked vocabulary | — (do not delete until fold: ledger points INTO §3, e.g., Axis-2A "NOT re-derived") |
| `multi-dim-convergence-algorithm-2026-05-21.md` | Late Matt amendment: node-count target v1 10–15 → v2 24–30 parity | SC (amendment only; base algorithm captured) | "2026-05-21 (late amendment) — convergence skill-node target amended: v2 targets 24–30 node parity (v1 10–15 stands for v1)." |
| `c-hybrid-cell-and-curation-architecture-2026-05-28.md` | Bounded-viability directive (Path α ratification); D2 curation rule | C — decisions-log 2026-05-28 Path α + Discipline #48 | — |
| `2026-06-09-arpg-physical-magical-ratio-baseline.md` | Genre ratio 40–45% physical / 55–60% caster baseline | C — Discipline #57 | — |
| `tier-4-architecture-defaults-2026-05-22.md` | Pre-authorization C (T4-A/T4-B plan); defaults superseded by T4 Session-1 | C/AUTH — T4 rulings (Q1–Q10, 21→25 catalog, DEFENSIVE_TRADEOFF reinstatement) captured at decisions-log T4 entries | — |
| `gear-spec-element-flavor-manifest-design-half-2026-06-18.md` | (no Matt content) | — | — (Cluster-D fold for content) |

### Weapons / substrate policy (live)

| Source doc | Ruling (one line) | Class | Proposed ledger row if SOLE-CARRIER |
|---|---|---|---|
| `weapon-substrate-composition-policy-v1-2026-05-24.md` | D1–D7 composition policy LOCKED (genre filter fantasy/mythological/historical; tiered promotion → v1_scope 2,293; cell-matching α/β/C; register weights; bi-modal ~32% personage / ~68% engine-original, uniform presentation) + Matt 2026-05-25 personage lock: §5.4 probabilistic-NOT-enforced ("forcing personages may diminish the uniqueness across seasons") | SC (second carrier `2026-06-10-engine-architecture-canonical-synthesis.md` §119 is also on the purge slate) | "2026-05-24 — weapon-substrate composition policy v1 D1–D7 LOCKED: genre filter (fantasy/mythological/historical); tiered promotion, v1 scope 2,293; cell-matching Options α/β/C; register weights hist 50-55%/fantasy 30-35%/mil-modern 5-8%; bi-modal form library ~32% personage/~68% original with UNIFORM presentation. 2026-05-25 — personage anchors sample probabilistically, never enforced (Matt verbatim)." |
| `weapon-as-identity-surface-recognition-2026-06-14.md` | Weapon-as-identity L1 ruling + envelope; Decision 2 HELD | C — decisions-log | — |
| `2026-05-23-weapon-substrate-conclusion-declaration.md` | Declare weapon-substrate concluded; 9.11-C/D/E → v1.1+; 9.10-E dormant + D10 Path C deferred; 9.11-B subsumed into 9.10-E | ST/C — conclusion + v1.1+ queue framing stale (isekai-era D10); live residue captured (composition policy row above; Mode #25) | — |
| `substrate-design-supplement-2026-05-21.md` | Substrate-as-cohesion-only architectural commitment (re-ratification clause is process) | C — decisions-log ("substrate-as-cohesion-only is the cleanest architectural expression") | — |
| `2026-06-06-atomic-substrate-registry.md` | Registry ratifications (atomic substrate registry canonical) | SC/KEEP — fold-map marks CANONICAL KEEP (→ENGINE or elrond) | Do NOT delete; ruling rides with the kept doc. If doc ever folds, carry "atomic substrate registry = canonical substrate surface" to decisions-log. |
| `marginal-lineage-tagging-pattern-2026-05-23.md` | Mode A/B/C/D lineage handling | C — Discipline #25 (derives from §2.4) | — |
| 5 × `*-marginal-lineage-disposition-2026-05-23.md` + `variant-cluster-policy-assignments` + `cleaning-policy-design-2026-05-22.md` | Curation dispositions / Matt-locked process framework / pending-Matt flags | AUTH — no design ruling; elrond-route for content | — |
| `engine-as-general-serial-content-product-2026-05-22.md` | Variant C strategic lock: engine = general serial-content product; game = one consumer via flags/gates (Matt verbatim reframe) | C — `canonical/37-engine-and-game-two-products.md` (KEEP spine; carries Variant C + 2026-05-24 amendment), cross-ref'd by doc 38 | — |

### Progression / profiles / proxy (live)

| Source doc | Ruling (one line) | Class | Proposed ledger row if SOLE-CARRIER |
|---|---|---|---|
| `v1-bc-target-intent-2026-05-24.md` | Matt 2026-05-24 Stage-0 locks: 7 BC-target sketches ratified; factions EMERGE from post-convergence clustering, NOT a pre-imposed roster | SC | "2026-05-24 — Stage-0 v1 BC-target locks: 7 sketches ratified as generation targets; factions emerge from clustering post-convergence (no pre-imposed faction roster)." |
| `skill-system-2026-05-24.md` | Matt 2026-05-24 lock: 10–15 nodes per form skill tree (v1 scope) | SC (v2 parity amendment in multi-dim row) | "2026-05-24 — skill-tree v1 scope locked: 10–15 nodes per form tree." |
| `off-hand-items-2026-05-24.md` | Matt 2026-05-24: off-hand Architecture B LOCKED, supersedes Architecture A | SC | "2026-05-24 — off-hand items Architecture B locked (supersedes A)." |
| `six-profile-set-architecture-2026-06-16.md` | All 6 gear profiles ship v1 — proxy profile NOT skipped; 6-profile set architecture ratified | SC | "2026-06-16 — six-profile set architecture ratified; all 6 profiles ship v1 incl. proxy (proxy profile explicitly NOT skipped)." |
| `representative-loadout-measurement-contract-2026-06-16.md` | Measurement anchors at 6b fixed reference instrument, not generated-kit-aligned 6a (6a-vs-6b park → Matt ruled 6b) | SC (shared: six-profile doc + autonomous-run-plan-v2 also carry it — all on purge slate) | "2026-06-16/17 — representative-loadout + set-bonus measurement anchors at the 6b fixed reference instrument (Matt-ruled; 6a generated-kit alignment rejected)." |
| `proxy-add-design-spec-2026-06-16.md` | Proxy-add spec SHIPS, incl. Beast Taming lane | SC | "2026-06-16 — proxy-add design spec ratified to ship (incl. Beast Taming); composes with proxy-primary charter + 2026-06-24 proxy FLIP." |
| `proxy-commander-set-6-capstone-spec-2026-06-16.md` | (authorization to author capstone spec) | AUTH | — |
| `2026-06-13-companion-as-hall-of-heroes-ally-commitment.md` | Path Pure RULED (Matt 2026-06-16: run 1 alone — no companion season 1); Hall-sourcing of companions | C — PART A A9 carries Path-Pure survival; A11 supersedes Hall-sourcing (companion = grimoire-summoned claimed soul); fold landed in `story-expansion.md §12` | — (STORY index already marks it FOLDED; source file still on disk — safe to delete) |
| `phase-5-llm-prompts-cohesion-judge-2026-05-27.md` | Pre-ratification #2: relationship_type locked to 6-enum; cosine < 0.7 similarity gate; no default-all-enemies | SC | "2026-05-27 — Phase-5 cohesion-judge pre-ratification #2: relationship_type = 6-enum (locked); embedding gate cosine<0.7; default-all-enemies prohibited." |
| `phase-7-2-layer-joint-gate-spec-2026-05-27.md` | Pre-ratification #1: 2-layer joint-gate thresholds locked | SC | "2026-05-27 — Phase-7 two-layer joint gate pre-ratification #1: joint pass thresholds locked (both layers must pass; thresholds per spec §)." |
| `phase-5-t4-narration-amendment-2026-05-26.md` / `phase-5-cohesion-judge-calibration-spec-2026-05-25.md` | (authoring/regen authorizations) | AUTH | — |
| `2026-06-01-flavor-pool-per-primary-element-lock.md` | Architecture A flavor-pool-per-primary-element lock | C — decisions-log | — |

### Engine architecture / process (live)

| Source doc | Ruling (one line) | Class | Proposed ledger row if SOLE-CARRIER |
|---|---|---|---|
| `2026-06-10-engine-greenfield-verdict-wrap-and-extend.md` + `2026-06-11-forward-architecture-contract-wrap-and-extend.md` | WRAP-AND-EXTEND verdict + contract (kernel-freeze, golden-master, §8.1 audit dispositions, §8.2 spatial re-point / cost-model / T4-native recompose-lever) — Matt-authorized | C — decisions-log 2026-06-11 combined entry (verified: clause (c) T4-recompose captured verbatim) | — (ledger entry cites the contract doc as source; deleting orphans the pointer — flag to purge executor) |
| `2026-06-02-season-archive-realm-expansion-pivot.md` | §3.2 per-skill bounded flavor (kit identity = primary element ONLY; flavor = per-skill naming — Matt verbatim); §3.3/§3.4 kit-space emission spine | SC — LIVE engine surfaces (`data/kit_space/`, `CHRONICLE_SCHEMA.md`, `kit_space_emitter.py`, `kit_space_skill_naming.py`, `ws1a4_lite_flavor_judgment.py`); DELETE ALREADY HALTED (commit 5043890) | Fold §3.2–§3.4 into `reap-die-rise-engine/` spec (per halt banner) + decisions-log row: "2026-06-02 — kit identity = primary element only; flavor is per-skill naming from element-gated pools; kit-space emission = engine content spine (Matt verbatim §3.2)." |
| `2026-06-01-gauntlet-metrics-as-provisional-hypotheses-recognition.md` | Gauntlet metrics ratified PROVISIONAL (hypotheses, not truths) | C — decisions-log | — |
| `2026-05-29-experiential-cascade-architecture-recognition.md` | Class-eradication election ("erase class concept at all levels") extending no-classes recommitment to substrate-input layer | C — decisions-log (no-classes recommitment 2026-05-27) + executed in engine (class-free substrate landed) | — |
| `2026-06-10-engine-architecture-canonical-synthesis.md` | Mission authorization (Fable-5 test Phase 1); consolidates already-ruled content | C/AUTH — all cited rulings classified at their source docs; second carrier for composition-policy | — |
| `2026-06-06-autonomous-fire-prompt-template.md` / `2026-06-17-autonomous-run-plan-v2.md` | Process templates; three-tier pre-authorization envelope; F1 semantic-shift PARKED for Matt (pending, not ruled) | AUTH — fold-map B holds template back; 6b corroboration harvested via 6b row | — |
| `loadout-analytics-suite-information-architecture-2026-05-18.md` | (work authorization) | AUTH | — |
| `substrate-generalization-track-c-synthesis-2026-05-21.md` | (analysis; Matt recall reinterpreted — no ruling) | — | — |
| `styleprofile-output-shape-ruling-2026-06-17.md` | (gandalf output-shape ruling; Matt only gates a future tool) | — | — (Cluster-D fold for content) |

### Story frame / presentation

| Source doc | Ruling (one line) | Class | Proposed ledger row if SOLE-CARRIER |
|---|---|---|---|
| `2026-06-05-cosmograph-pivot.md` | Cosmograph = possibility space (pivot ruling) | C/ST — PART A A11: cosmograph DEAD-as-browse, presentation PARKED; pivot content in tracker | — |
| `2026-06-07-earth-avatar-cosmograph-creation-moment-architecture.md` | Creation-moment scene ruling | C/ST — decisions-log capture; A11 reskins it (dark sacrament) — scene specifics stale | — |
| `2026-06-07-cosmograph-cross-surface-LOD-architecture.md` | Cross-surface LOD ruling | C/ST — decisions-log; presentation PARKED per A11 | — |
| `2026-06-09-tal-rasha-glyphic-primitive-anchor-architecture-recognition.md` | Glyphic-primitive anchor for cosmograph surface | ST — cosmograph presentation PARKED (A11) | — |
| `seasonal-hero-h-5-hybrid-spec-2026-05-27.md` | H-5 hybrid seasonal-hero ruling | ST — seasonal-RELEASE model retired | — |
| `battle-room-presentation-decoupling-2026-06-15.md` | Columns-arches architectural grammar rule for battle-room presentation (decoupled from sim abstraction) | SC — survivor per STORY-index A′2 routing; grammar rule uncaptured | "2026-06-15 — battle-room presentation decoupled from sim room abstraction; columns/arches architectural grammar ratified as the presentation vocabulary." |
| `telegraph-dodge-temporal-decoupling-2026-06-15.md` | Telegraph→dodge decoupling ratified: telegraph JSON bridge contract (sim emits windows, presentation consumes); human-playtest calibration DEFERRED | SC — masking-methodology half captured; bridge specifics + DEFERRED status uncaptured | "2026-06-15 — telegraph/dodge temporal decoupling ratified: sim emits telegraph-window JSON (bridge contract); presentation-side dodge reads windows; human playtest calibration DEFERRED." |
| `gear-spec-generation-deferred-architecture-2026-06-16.md` | Gear-spec GENERATION held behind Synty asset-library adoption | SC | "2026-06-16 — gear-spec generation architecture DEFERRED behind Synty library adoption (spec-driven gen resumes when asset vocabulary is fixed)." |
| `style-register.md` | Path A-prime per-slug scale lookup confirmed; v2 table 2.5× SUPERSEDES 1.31× (drax MONSTER_SCALE_BY_SLUG anchor); 2026-06-14 Steam-wall: Pixi = prototype-only, never ship target | SC-weak (demo1-scoped; Godot seam owns ship presentation) | "2026-05-16 — per-slug scale lookup Path A-prime; v2 lookup 2.5× supersedes 1.31× (demo1 anchor). 2026-06-14 — Pixi confirmed prototype-only (Steam wall); ship presentation = Godot seam." |
| `visual-benchmark-vs2a-2026-05-18.md` | VS2a town-benchmark ruling | ST — pixi-era benchmark | — |
| `geometry-vfx-coverage-assessment.md` | pixi/B11 VFX coverage rulings | ST | — |
| `asset-pipeline-meshy-swap-2026-05-22.md` | Meshy asset-pipeline swap | ST — Unreal/PC seam retired 2026-06-30 | — |
| `fate-genre-recognition-and-mobile-alignment-trajectory-2026-05-23.md` | Fate-genre trajectory | ST | — |
| `w1-13-rescope-disposition-2026-05-22.md` / `ab-comparison-protocol-cycle-14-close-2026-05-27.md` | Wave/cycle process dispositions | ST — cycle frame retired (decisions-log 2026-06-11) | — |

### Methodology (route to disciplines, not decisions-log)

| Source doc | Ruling (one line) | Class | Proposed ledger row if SOLE-CARRIER |
|---|---|---|---|
| `2026-05-29-designer-writes-substrate-player-names-experience-principle.md` | Principle: designer writes SUBSTRATE; player names EXPERIENCE | SC — fold-map routes → jack-ryan disciplines (pending) | Disciplines entry: "Designer writes substrate; the player (and LLM-at-the-player-boundary) names experience — naming is downstream of engine substrate, never in it (Matt 2026-05-29)." |
| `2026-05-31-hypothesis-flow-pattern-library-architecture.md` | Hypothesis-flow pattern library CANONICAL (incl. §1.7 flavor-judgment locks cited by synthesis doc) | SC — fold-map routes → disciplines (pending) | Disciplines entry: "Hypothesis-flow pattern-library = canonical Mode-A research architecture; per-skill bounded flavor judgment locks (§1.7) ride with it." |
| `v1-1-plus-design-discipline-recognitions-2026-05-23.md` | Matt flag-for-later: v1.1+ parking (9.11-C/D/E lanes; output_purpose commercial-vs-solo metadata; D7 differentiation) | SC-weak | Disciplines/tracker parking row: "v1.1+ flags (Matt 2026-05-23): weapon lanes 9.11-C/D/E; output_purpose metadata (player-ship vs solo-dev vs validation); full-D7 only for player-ship outputs." |

---

## Execution notes for the purge

1. **Two docs must NOT be deleted regardless of harvest:** `2026-06-06-atomic-substrate-registry.md` (fold-map KEEP) and `2026-06-02-season-archive-realm-expansion-pivot.md` (delete HALTED 2026-07-01 — live engine spine; fold to reap-die-rise-engine first).
2. **Pointer-orphan risk (captured but referenced):** `qd-engine-bc-axes-lock` §3 and `2026-06-11-forward-architecture-contract` are cited as binding vocabulary/source by multiple decisions-log entries. Recommend these two delete only at Cluster-D fold time with the ledger citations repointed.
3. **VIT-DELETE double-capture:** present in `current-to-end-state-engine.md` III.10 (RATIFIED deferral-audit, Matt 2026-06-24: proxy/charge-stack/damage-converts/support FLIP, VIT DELETE, HP-economy BUILD, dodge KEEP) — but the engine tracker is a DELTA tracker, not a listed ledger; the proposed decisions-log row makes capture durable.
4. **The 2026-05-22-evening family** (six retirements / stat-derivation / gear-substrate-rule-table / gear-heavy / BDI / serial-content) is entirely absent from the decisions-log (only one 2026-05-22 entry exists: Discipline #19). One consolidated ledger entry covering the evening's calls would satisfy rows for docs 22–25 + 12 in the NEEDS-HARVEST list.
5. Ruling-harvest clearance ≠ content-fold clearance: Cluster-D docs on the reap-die-rise-engine 00-index remain "authoritative until folded" for spec CONTENT even where their rulings are captured.
