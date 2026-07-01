# B4 + B5 — Handoff to knight-rider (cross-seam capture-check + route)

**Type:** gandalf → knight-rider handoff-request (KR sequences into dispatches; gandalf does not author dispatches).
**Date:** 2026-06-30
**Author:** gandalf (CANON-STEWARD / story-and-design steward)
**Authority:** Matt 2026-06-30 — *"run B2+B3 solo now, and hand B4+B5 to knight-rider to sequence."* B2/B3 are gandalf-solo (in progress); **B4+B5 are yours to sequence.**
**Parent worklist:** `agentic_orchestration/gandalf/notes/2026-06-30-canonical-reorg-fold-map.md` §6.5 (the Tranche-3 execution log — read its **⚠ LOAD-BEARING FINDING** block; it is the load-bearing context below).
**Governing ruling:** the canonical reorg is strategy **(b) heavyweight-fold** (Matt 2026-06-30): distill load-bearing content into the tight spec folders, delete sources — never blind-delete a CURRENT doc.

---

## 0. One line

B4 and B5 are the **cross-seam** remainder of the canonical (b)-fold — the doc-clusters that are NOT gandalf's to fold solo because their content lives in other seams' authority (engine-mechanics → rocket/gamora/star-lord; substrate → elrond; disciplines → jack-ryan). Each is a **capture-check-then-fold-or-kill**, not a move-pass. **The v1→v2 supersession finding (§3) is the trap that makes this cross-seam and not mechanical — brief every specialist with it.**

## 1. B4 — story/ Cluster D (engine-mechanics docs) → `reap-die-rise-engine/`

**What it is:** ~30 `canonical/story/` docs that are *engine-mechanics specs wearing story-folder clothing* (attribute system, skill system, tier-4 architecture, gear substrate rules, proxy/commander specs, stat-derivation, convergence algorithms, cohesion-judge calibration, etc.). They belong in the engine spec, not the story spec — but they are **v1/seasonal-era** and several are superseded or landed-in-code.

**Why it is cross-seam (not gandalf-solo):** the content is engine-mechanics *authority* — the seam owners (rocket = generation/element/anchor/foundation; gamora = simulation; star-lord = telemetry/export/llm) are the ones who can verify whether a given doc's intent is (a) still-live spec, (b) superseded by the run-model, or (c) already landed in code. gandalf can fold *design-overview* framing; gandalf cannot certify that `tier-4-architecture-defaults` matches what `foundation/` actually does. That certification is the capture-check.

**The Cluster-D doc list** (from fold-map §4 Cluster D):
```
attribute-system-2026-05-24 (carries Matt 2026-06-24 VIT-DELETE amendment — load-bearing) ·
skill-system-2026-05-24 · off-hand-items-2026-05-24 · v1-bc-target-intent-2026-05-24 ·
qd-engine-bc-axes-lock-2026-05-20 · stat-derivation-from-bc-convergence-2026-05-22 ·
multi-dim-convergence-algorithm-2026-05-21 · tier-4-architecture-defaults-2026-05-22 ·
bdi-omega-tau-tables-v1-2026-05-22 · gear-heavy-promotion-2026-05-22 ·
gear-spec-element-flavor-manifest-design-half-2026-06-18 ·
gear-spec-generation-deferred-architecture-2026-06-16 (check "deferred" vs no-deferral discipline) ·
gear-substrate-rule-table-v1-2026-05-22 · proxy-add-design-spec-2026-06-16 ·
proxy-commander-set-6-capstone-spec-2026-06-16 (proxy = summoner pillar, FLIP-ratified) ·
six-profile-set-architecture-2026-06-16 · representative-loadout-measurement-contract-2026-06-16 ·
seasonal-hero-h-5-hybrid-spec-2026-05-27 · styleprofile-output-shape-ruling-2026-06-17 ·
thematic-registry-2026-05-27 · c-hybrid-cell-and-curation-architecture-2026-05-28 ·
phase-5-cohesion-judge-calibration-spec-2026-05-25 · phase-5-llm-prompts-cohesion-judge-2026-05-27 ·
phase-5-t4-narration-amendment-2026-05-26 · phase-7-2-layer-joint-gate-spec-2026-05-27 ·
weapon-as-identity-surface-recognition-2026-06-14 · telegraph-dodge-temporal-decoupling-2026-06-15 ·
battle-room-presentation-decoupling-2026-06-15 · 2026-06-09-arpg-physical-magical-ratio-baseline ·
2026-06-13-2d-spatial-golden-oracle-spec ·
2026-06-13-combat-fidelity-drift-proofing-and-2d-certification-wave ·
2026-06-01-flavor-pool-per-primary-element-lock
```

**Routing within B4 (per-doc capture-check verdict):**
- **(a) still-live engine spec** → fold into `reap-die-rise-engine/` (coordinate with B2 — see §4; the run-invariant math spine is authored *once*, both doc-sets fold into it).
- **(b) superseded-by-run-model** → verify-superseded → capture any orphan into the live spec → delete. **Do NOT forward-fold.**
- **(c) landed-in-code** → thin lineage pointer + delete (grep-verify the code citation; full re-read unnecessary).
- **Flagged specials:** `attribute-system` carries the Matt 2026-06-24 **VIT-DELETE** amendment (load-bearing — the survivor must land in the engine spec); `gear-spec-generation-deferred-architecture` — **check the "deferred" against build-to-spec/no-deferral discipline** (OP §3.7: a spec-conflicting "deferred" is a GAP-to-close, not a settled state — classify FLIP/FLAG/KEEP, do not pass through); `proxy-*` docs are the **summoner pillar (FLIP-ratified)** — live spec, not deferred.

## 2. B5 — routes (substrate → elrond; principles → jack-ryan; infra → per-doc kill)

- **Cluster E (substrate / catalogue / lineage) → elrond.** Mostly KILL (curation working-history → git). **EXCEPTION flagged — do NOT blind-kill:** `2026-06-06-atomic-substrate-registry` (STATUS: CANONICAL, load-bearing → ENGINE or elrond-owned). elrond capture-checks the exception, kills the rest.
- **Cluster F principle docs → jack-ryan disciplines** (these are *principles*, not kill): `2026-05-29-designer-writes-substrate-player-names-experience-principle`, `v1-1-plus-design-discipline-recognitions-2026-05-23`, `2026-05-31-hypothesis-flow-pattern-library-architecture` (STATUS: CANONICAL methodology). Route to jack-ryan as candidate engineering-discipline entries, not deletions.
- **Cluster F infra/genre records → per-doc capture-check then kill.** Flagged keepers (do NOT blind-kill): `2026-06-07-federated-pc-team-architecture-commit` (**re-check** — CLAUDE.md dropped it; sole remaining citer is the engine index → may now be killable or demote to build-architecture annex), `2026-06-10-engine-greenfield-verdict-wrap-and-extend`, `2026-06-11-forward-architecture-contract-wrap-and-extend` (referenced by the projection doc §7 — now folded into `story-expansion §12`; re-check the citer).

## 3. ⚠ The essential context — v1→v2 supersession (brief EVERY specialist with this)

**The trap:** Cluster D (and the flat `37–51` engine docs in B2) are **v1/seasonal-era.** The v2 run-model (`reap-die-rise-story/gameplay-loop-design.md` §7/§23) has **already superseded chunks** — most sharply **progression** (doc `41`'s seasonal-L50-cap → gameplay-loop §7's **descent/sawtooth**: floors-trail-power-by-2, old-floors-never-rescale). A specialist who folds a v1 doc as if it were live spec will **re-canonize a superseded model.**

**The discipline that prevents it — every Cluster-D doc is classified (a)/(b)/(c) against the run-model + engine code + engine tracker BEFORE any delete:**
- **(a) run-invariant** (the *math* doesn't care seasonal-vs-run — gear/stat/damage/scaling) → fold as reframe.
- **(b) superseded-by-run-model** (progression, seasonal-cadence assumptions) → verify + capture orphan + delete; **do not forward-fold.**
- **(c) landed-in-code** → thin pointer + delete.

**This is exactly why B4 is cross-seam and not a gandalf move-pass:** only the seam owner can certify (a) vs (b) vs (c) for their own mechanics.

## 4. Coordination flag — B4 ⇄ B2 (both feed `reap-die-rise-engine/`)

B2 (flat `37–51`, **gandalf-solo, in progress**) and B4 (Cluster-D story/ engine-mechanics, **yours**) **both fold into the same engine spec folder** and **both carry the same v1→v2 split.** They overlap on the run-invariant math spine (e.g., doc `40` gear-balance is the linchpin; `tier-4-architecture-defaults` and `gear-substrate-rule-table` in Cluster D are the same subject matter). **Recommend:** sequence B4 *after* or *interleaved-with* B2's spine authoring so the run-invariant math is authored **once** and both doc-sets fold into it — not two parallel authorings that diverge. gandalf owns the B2 spine; the B4 specialists fold their Cluster-D content **into** that spine, not alongside it. Flagging the coordination; the sequencing call is yours.

## 5. Discipline constraints (bind all B4/B5 folds — non-negotiable)

1. **verify-then-prune** — delete only after every load-bearing survivor is **reference-verifiably captured** (not author-asserted) in a live spec. git holds lineage; a "routes to" pointer is NOT a capture. (Precedent: the B3 anchor fold re-homed even a single presentation-seam survivor before deleting — commit `f9f763e`.)
2. **reconcile, do not amputate** — the *structure* is load-bearing; only the retired *labels* (isekai/season/spirit-guide/Earth-Self) die. Open v2-reconciliation forks route to the **trackers** (`current-to-end-state-{engine,story,game}.md` PART B), NOT silently re-designed mid-fold.
3. **build-to-spec / no-deferral** (OP §3.7) — a spec-conflicting "deferred" flag is a **GAP-to-close**, not a settled state; classify FLIP/FLAG/KEEP and surface it; do not pass it through. No "season-N" release framing reintroduced.
4. **no dangling refs** — re-point every inbound cross-ref before a source deletes (grep the corpus; the B3 fold re-pointed 4 refs before committing).
5. **survey-mode** — "what-IS" (a doc's current STATUS) and "what's-wrong" (spec-conflict) are separate outputs; a spec-conflicting deferral IS a what's-wrong.

## 6. What gandalf still owns in parallel (so you know the boundary)

- **B2** (flat `37–51` engine spine) — gandalf-solo, in progress; the run-invariant math spine authored 40-first. B4 folds *into* this (see §4).
- **B3 continuation** (remaining story/ Cluster-C docs) — gandalf-solo; several are split-sources (STORY+presentation or STORY+ENGINE) needing capture-check.
- **B6** (CLAUDE.md "Where to find things" table rewrite) — gandalf.

---

**Signed:** gandalf, 2026-06-30. B4/B5 are the cross-seam half of dissolving the pile. The clusters are enumerated, the v1→v2 trap is named, the disciplines are bound — the sequencing is yours. Brief the specialists with §3 or they will fold superseded v1 progression as if it were live.
