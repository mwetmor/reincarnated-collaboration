# Canonical Reorg — Fold-Map (reviewable triage)

**STATUS:** IN EXECUTION. Matt ratified 2026-06-30 — fork = **(b) heavyweight-fold**; companion-inversion = **kill** (S2-companion investigation preserved); Tranche 1 = **go**. **Tranche 1 FIRED** (commits a813cec + 5fc2890): 13 live clean-kills + 98 already-demoted swept. Remaining: structural skeleton + (b) consolidation (§6).
**Author:** gandalf, 2026-06-30
**Workstream:** canonical-folder reorg + cleanse (Matt-agreed 2026-06-30: *"Agreed with the above and the three dispositions. Please begin."*)
**Companion:** `canonical/reap-die-rise/00-index.md` (the existing v2 spec set — the model for the target form); `canonical/story/current-to-end-state.md` (the engine tracker that becomes `current-to-end-state-engine`).

---

## 1. The target — three folders under `canonical/`

| Folder | Holds | Role |
|---|---|---|
| `reap-die-rise-story/` | story-keystone, story-expansion, gameplay-loop, cosmograph/projection/Hall frame, descent/faction story | **END-STATE story SPEC** |
| `reap-die-rise-engine/` | build/networking/perf/godot/vfx + the load-bearing engine-mechanics specs (37–51 distilled) | **END-STATE engine SPEC** |
| `current-to-end-state/` | `…-engine.md` (today's tracker PARTs I–V) + `…-story.md` (NEW — open story flags/beats) | **DELTA: where the engine is vs the spec** |

Plus **one thin router stub** at `canonical/` root (`00-start-here.md`, ~1 screen: "story spec → here, engine spec → here, where-we-are → here, archive → git"). The heavy oracle `00-ground-state.md` registry **dies** — its per-doc registry is the thing the reorg dissolves.

**Spec-vs-progress grid:** `reap-die-rise-{story,engine}` = the END STATE (what we're building). `current-to-end-state/{story,engine}` = the DELTA (how far the engine is from it). Two different questions, two homes.

---

## 2. Disposition legend (keep/kill triage)

The call I need from you is **keep vs kill** per doc. *How* a keeper lands (move-whole vs fold-then-delete) is an execution detail in §6.

| Tag | Meaning |
|---|---|
| **→STORY** | Load-bearing; survives in `reap-die-rise-story` |
| **→ENGINE** | Load-bearing; survives in `reap-die-rise-engine` |
| **→TRACKER** | Its live fact belongs in the delta tracker, not the spec |
| **KILL** | Nothing here that isn't already downstream; delete, git holds the lineage |
| **? ** | VERIFY before kill — confirm content is captured in spec/tracker first (resolved during execution, not by guess) |

---

## 3. The existing v2 set + tracker — how they re-home (mechanical, no judgment)

`reap-die-rise/` (10 docs) splits by content:

| Doc | → |
|---|---|
| story-keystone, story-expansion, gameplay-loop-design | **→STORY** |
| build-architecture, backend-networking-stack, performance-target-specs, godot-agent-contract, vfx-pipeline, design-decisions-session | **→ENGINE** |
| 00-index | split: supersession-map + story rows →STORY index; engine rows →ENGINE index (or one shared router) |

`current-to-end-state.md` → renamed **`current-to-end-state/current-to-end-state-engine.md`** (PARTs I–V are already the engine delta). New sibling **`current-to-end-state-story.md`** born from the open story flags (#2/#4), undecided keystone beats, and the frame-reconciliation queue.

---

## 4. The 94 live `story/` docs — clustered triage

### Cluster A — self-declared dead (KILL, high confidence)
| Doc | Why |
|---|---|
| 2026-06-16-engine-state-and-autonomous-run-plan.md | STATUS: HISTORICAL-SUPERSEDED |
| 2026-06-18-current-to-end-state-battlesim-and-pipeline.md | STATUS: SUPERSEDED (predecessor of today's tracker) |

### Cluster B — process / wave-close / orchestration records (KILL — never were spec; operational history → git)
2026-06-01-cycle-14-wave-5-swift-closure-wave-close-record · 2026-06-01-ws1a-q18-flavor-pool-wave-close-record · 2026-06-02-cycle-18-drax-amend-full-wave-close-record · 2026-06-02-eaa-chain-wave-close-record · 2026-06-02-qdx-chain-wave-close-record · 2026-06-06-cosmograph-phase-a-creation-moment-wave-close · ab-comparison-protocol-cycle-14-close-2026-05-27 · hive-mind-protocol-qd-engine-rebuild-2026-05-21 · hive-mind-protocol-weapon-library-import-2026-05-22 · 2026-06-06-autonomous-fire-prompt-template · 2026-06-01-gauntlet-metrics-as-provisional-hypotheses-recognition · **?** 2026-06-17-autonomous-run-plan-v2 (kill once you confirm the run it planned is spent)

### Cluster C — story-frame (→STORY; ALL under v2 reconciliation, experiential structure survives)
| Doc | → | note |
|---|---|---|
| 2026-06-05-cosmograph-pivot | →STORY | cosmograph structure survives |
| 2026-06-07-earth-avatar-cosmograph-creation-moment-architecture | →STORY | the creation scene |
| ~~2026-06-11-avatar-projection-and-hall-of-heroes-framing~~ **✓ DONE 2026-06-30** | →STORY | folded → `story-expansion.md §12`; v2 forks → tracker B1/B2; presentation survivor → game-tracker A′2; source deleted; inbound refs re-pointed (00-index, companion doc) |
| 2026-06-13-companion-as-hall-of-heroes-ally-commitment | →STORY | Path-Pure (Matt-RULED; Flag #4 open) |
| 2026-06-07-cosmograph-cross-surface-LOD-architecture | ? →STORY/ENGINE | LOD spans story+engine — split-check |
| 2026-06-02-season-archive-realm-expansion-pivot | ? →TRACKER | seasonal-retire conclusion already in v2 loop doc; keep lineage one-liner |
| 2026-06-18-companion-difficulty-inversion-and-spirit-guide-combat-bridge | ? | references RETIRED spirit guide + "Season-2" — reconcile or KILL |
| 2026-06-22-faction-descent-and-reward-loop-recognition | ? →STORY | descent/faction — confirm captured in loop doc |
| 2026-06-22-seasonal-descent-architecture-recognition | ? →STORY | descent arch — confirm captured |
| 2026-06-22-seasonal-descent-content-audit | ? →TRACKER | audit deliverable — fold findings, kill |

### Cluster D — engine-mechanics specs (→ENGINE; VERIFY each is captured in the engine spec before kill-or-fold)
attribute-system-2026-05-24 *(carries Matt 2026-06-24 VIT-DELETE amendment — load-bearing)* · skill-system-2026-05-24 · off-hand-items-2026-05-24 · v1-bc-target-intent-2026-05-24 · qd-engine-bc-axes-lock-2026-05-20 · stat-derivation-from-bc-convergence-2026-05-22 · multi-dim-convergence-algorithm-2026-05-21 · tier-4-architecture-defaults-2026-05-22 · bdi-omega-tau-tables-v1-2026-05-22 · gear-heavy-promotion-2026-05-22 · gear-spec-element-flavor-manifest-design-half-2026-06-18 · gear-spec-generation-deferred-architecture-2026-06-16 *(check "deferred" vs no-deferral discipline)* · gear-substrate-rule-table-v1-2026-05-22 · proxy-add-design-spec-2026-06-16 · proxy-commander-set-6-capstone-spec-2026-06-16 *(proxy = summoner pillar, FLIP-ratified)* · six-profile-set-architecture-2026-06-16 · representative-loadout-measurement-contract-2026-06-16 · seasonal-hero-h-5-hybrid-spec-2026-05-27 · styleprofile-output-shape-ruling-2026-06-17 · thematic-registry-2026-05-27 · c-hybrid-cell-and-curation-architecture-2026-05-28 · phase-5-cohesion-judge-calibration-spec-2026-05-25 · phase-5-llm-prompts-cohesion-judge-2026-05-27 · phase-5-t4-narration-amendment-2026-05-26 · phase-7-2-layer-joint-gate-spec-2026-05-27 · weapon-as-identity-surface-recognition-2026-06-14 · telegraph-dodge-temporal-decoupling-2026-06-15 · battle-room-presentation-decoupling-2026-06-15 · 2026-06-09-arpg-physical-magical-ratio-baseline · 2026-06-13-2d-spatial-golden-oracle-spec · 2026-06-13-combat-fidelity-drift-proofing-and-2d-certification-wave · 2026-06-01-flavor-pool-per-primary-element-lock

### Cluster E — substrate / catalogue / lineage (elrond's domain — NOT story, NOT game-spec)
Mostly KILL (curation working-history → git). EXCEPTION flagged.
arctic-circumpolar… · mesoamerican… · n-am-indigenous… · oceanic… · south-american-indigenous-marginal-lineage-disposition (5 lineage dispositions) · marginal-lineage-tagging-pattern-2026-05-23 · variant-cluster-policy-assignments-2026-05-23 · legacy-categorical-cleanup-audit-2026-05-22 · cleaning-policy-design-2026-05-22 · asset-pipeline-meshy-swap-2026-05-22 · substrate-design-supplement-2026-05-21 · substrate-generalization-track-c-synthesis-2026-05-21 · 2026-05-23-weapon-substrate-conclusion-declaration · **?** 2026-06-06-atomic-substrate-registry *(STATUS: CANONICAL, load-bearing — →ENGINE or elrond-owned, NOT kill)*

### Cluster F — architecture / infra / team / genre recognition records (mostly KILL → git; flagged keepers)
2026-05-28-cycle-15-unreal-direction-recognition-record · 2026-05-29-experiential-cascade-architecture-recognition · 2026-05-30-pi-engine-control-dashboard-recognition · 2026-05-30-pi-llm-proxy-architecture-recognition · 2026-05-30-pi-middleware-mac-to-pc-architecture · 2026-05-31-ue-seam-agent-placement-decision · 2026-06-09-tal-rasha-glyphic-primitive-anchor-architecture-recognition · 2026-06-10-engine-architecture-canonical-synthesis · infrastructure-raspberry-pi-postgres-and-closed-loop-pipeline-2026-05-25 · fate-genre-recognition-and-mobile-alignment-trajectory-2026-05-23 · engine-as-general-serial-content-product-2026-05-22 · loadout-analytics-suite-information-architecture-2026-05-18 · visual-benchmark-vs2a-2026-05-18 · geometry-vfx-coverage-assessment

**Flagged keepers in F (? — do NOT blind-kill):**
| Doc | Why keep |
|---|---|
| 2026-06-07-federated-pc-team-architecture-commit | **CLAUDE.md first-read** — referenced by repo root. →ENGINE/build or keep as build-architecture annex |
| 2026-05-31-hypothesis-flow-pattern-library-architecture | STATUS: CANONICAL — methodology. →ENGINE or jack-ryan disciplines |
| 2026-06-10-engine-greenfield-verdict-wrap-and-extend | greenfield verdict — load-bearing decision record |
| 2026-06-11-forward-architecture-contract-wrap-and-extend | forward contract — referenced by projection doc §7 |
| 2026-05-29-designer-writes-substrate-player-names-experience-principle | a *principle* — candidate for jack-ryan disciplines, not kill |
| v1-1-plus-design-discipline-recognitions-2026-05-23 | design disciplines — same |

### Cluster G — specials
| Doc | → |
|---|---|
| current-to-end-state.md | becomes `current-to-end-state/current-to-end-state-engine.md` |
| style-register.md | →ENGINE (consumption-time filter spec; gandalf-owned) |

---

## 5. The 17 top-level numbered docs

| Doc | Disposition |
|---|---|
| 00-ground-state.md | **dies → thin `00-start-here.md` router** |
| 02-roadmap.md | **KILL** — STATUS already HISTORICAL (retired 2026-06-12) |
| 48-cycle-14-class-roster.md | **KILL** — STATUS already VESTIGIAL (class concept retired) |
| 43-t4-algorithm-wave-2-intent / 44-…wave-3 / 45-spec-driven-gear-gen-wave-4-intent | **? →TRACKER/KILL** — "Wave-N intent" docs; intent has landed in code — fold residual, kill |
| 37-engine-and-game-two-products | →ENGINE (the two-products framing root) |
| 38-downstream-delivery-strategy / 39-qd-workflow / 40-gear-balance-guide / 41-progression-framework / 42-stat-partition / 46-concentration / 47-damage-scaling / 49-loadout-surface / 50-bounded-viability / 51-investment-scaling | **→ENGINE** (load-bearing engine spec — the spine of `reap-die-rise-engine`) |

---

## 6. Execution sequence + the strategic fork

**The fork (needs your call):** keepers can land two ways —
- **(a) lightweight — move-whole:** relocate load-bearing docs into the 2 spec folders as-is. Fast, safe, reaches 3 folders in one pass. Cost: `reap-die-rise-engine` is then ~40 docs, not a tight consolidated spec.
- **(b) heavyweight — fold-then-delete:** distill the pertinent content into a *tight* spec set (mirroring how `reap-die-rise/` already is 10 clean docs), delete the sources. Cost: multi-session spec-authoring.

**RULED (Matt 2026-06-30): (b) heavyweight-fold.** Distill pertinent content into a *tight* consolidated spec set (mirroring how `reap-die-rise/` is already 10 clean docs), delete sources. Multi-session. The fold-map is the worklist.

**Tranches:**
1. ✅ **DONE — KILL (zero-judgment):** Cluster A + clean B + 02 + 48 (commit a813cec, 13 live) + the 98 already-demoted subdirs (commit 5fc2890). All git-recoverable. **Held back from B to the `?`-verify set (4):** `autonomous-fire-prompt-template`, `autonomous-run-plan-v2` (possible active operational use), `gauntlet-metrics-as-provisional-hypotheses-recognition`, `ab-comparison-protocol-cycle-14-close` (possible reusable-methodology value). Companion-inversion killed *with* the S2-companion investigation note preserved in companion-as-Hall §7.
2. ✅ **DONE (skeleton) — structural folders + new story-tracker** (Matt approved fold-into-new-first sequencing). Created `reap-die-rise-story/`, `reap-die-rise-engine/`, `current-to-end-state/`; seeded the two spec folders with `00-index.md` fold-worklists; **born `current-to-end-state/current-to-end-state-story.md`** (the story-side delta — PART A locked frame / PART B open queue / PART C reconciliation worklist). **Two physical relocations DEFERRED to the final verified rewire pass** (measured fan-out: `reap-die-rise/` = 9 files, tracker = 9 files; both touch the startup-loaded OP skill, so batched into one verified pass): (i) split the 10 `reap-die-rise/` docs into the two spec folders; (ii) move `story/current-to-end-state.md` → `current-to-end-state/current-to-end-state-engine.md`.
3. **(b) consolidation — the real lift:** fold Cluster D + top-level 37–51 engine specs into a tight `reap-die-rise-engine` spec; fold Cluster C story-frame into `reap-die-rise-story` (v2-reconciled); resolve `?` rows + the 4 held docs via capture-checks; route the *principle* docs (`designer-writes-substrate`, `v1-1-plus-disciplines`) to jack-ryan disciplines rather than kill.
4. **Birth `current-to-end-state-story.md`** from open flags #2/#4 + undecided beats + the frame-reconciliation queue.
5. **Thin router stub** replaces `00-ground-state.md`; update CLAUDE.md "Where to find things" table + first-read pointers. **First-read pointers DONE (2026-06-30):** all **9 agent OPs + 9 SKILLs** swung session-start read #3 from the retired `02-roadmap.md` → `current-to-end-state/current-to-end-state-engine.md`; the gandalf OP additionally rewired its reads #2/#4 + § 5 session-end protocol to the two-tracker / spec-folder homes. **Companion governance LANDED (2026-06-30):** the doc-lifecycle system at `canonical-doc-format § 6` (total/partial supersession + the 4-predicate prune-safe rule + the standing § 6.6 hygiene Routine) + its 14-scenario stress-test (`gandalf/notes/2026-06-30-doc-lifecycle-governance-stress-test.md`) + the standing-Routine spec (`operating-procedures/canonical-hygiene-audit-routine.md`, instantiation BLOCKED on a CCR environment) — this is the **cleanup engine** the reorg motivated (prune follows promotion, the lever for "tons of notes"). **First verify-then-prune RAN** (`gandalf/notes/2026-06-30-verify-then-prune-first-run-prune-list.md`): safe tier empty, 113/153 notes evidentiary, 33 surface for ratification, nothing deleted. **Still pending:** the router stub + the CLAUDE.md "Where to find things" table rewrite.

---

## 6.5 Tranche 3 execution log (the (b) consolidation, in progress)

Matt 2026-06-30: *"move into doc-pruning — stand-alone canonical/ docs, then canonical/story/, toward dissolving the story folder."* Authorizes Tranche-3 execution.

**Reframe surfaced at execution start (survey finding):** the ~80 surviving `story/` docs are **overwhelmingly `STATUS: CURRENT (load-bearing)`.** Tranche 1 already took the self-declared-dead + clean operational records. So dissolving `story/` is **NOT a prune — it is the heavyweight FOLD**: author load-bearing content into the two tight spec folders (+ route substrate→elrond, principles→jack-ryan) BEFORE deleting sources. Deleting a CURRENT doc without folding = spec loss (the verify-then-prune failure). This is genuine multi-session, cross-seam authoring — not a delete pass.

**Batch 1 — cancelled-infrastructure lineage KILL (EXECUTED):** the 2026-06-30 Unreal/PC/Pi retirements turned 6 ratified-KILL (Cluster F) recognition records into pure lineage. Verified: 0 live-*spec* inbound (only historical-lineage citers — CHANGELOG, decision-logs, retired `pc-setup/`, agent notes — acceptable); the 2 pi- records were "architectural commitments DEFERRED" (no landed commitment to lose). Deleted (git-recoverable): `2026-05-28-cycle-15-unreal-direction-recognition-record` · `2026-05-30-pi-engine-control-dashboard-recognition` · `2026-05-30-pi-llm-proxy-architecture-recognition` · `2026-05-30-pi-middleware-mac-to-pc-architecture` · `2026-05-31-ue-seam-agent-placement-decision` · `infrastructure-raspberry-pi-postgres-and-closed-loop-pipeline-2026-05-25`. **story/ 81 → 75.**

**Remaining Tranche-3 batch spine (ordered; each fold = distill→verify-capture→delete):**
- **B2 — flat `37–51` engine spine → `reap-die-rise-engine/`** (Matt's "stand-alone docs first"). Gandalf-foldable (design-overview lane). `?` capture-check first on the 3 Wave-N intent docs (43/44/45 — intent-in-code → fold residual rationale, kill).
- **B3 — story/ Cluster C (story-frame) → `reap-die-rise-story/`.** Gandalf-solo (story = my domain); v2-reconcile (retired labels die, structure survives).
- **B4 — story/ Cluster D (engine-mechanics) → `reap-die-rise-engine/`.** **Cross-seam** — capture-check vs engine tracker/build-docs/code; may route to rocket/gamora/star-lord rather than gandalf-fold.
- **B5 — routes:** Cluster E substrate → **elrond**; Cluster F principle docs (`designer-writes-substrate`, `v1-1-plus-disciplines`, `hypothesis-flow-pattern-library`) → **jack-ryan disciplines**; remaining Cluster F infra/genre records → per-doc capture-check then kill (incl. re-check `federated-pc-team` now that CLAUDE.md dropped it — sole citer is the engine index).
- **B6 — Tranche-5 remainder:** CLAUDE.md "Where to find things" table still points at stale `canonical/` numbered paths + `canonical/historical/16-project-roadmap.md` — rewrite to the folder structure.

## 7. The gate

**Resolved (Matt 2026-06-30):** (1) clusters ratified; (2) fork = **(b)**; (3) Tranche 1 = go → **FIRED**.

**Next open item:** the Tranche-2 sequencing fork (§6.2) — rename `reap-die-rise/` now vs. fold-into-new-folders-first-and-retire-last. My rec: the latter (fewer link churns). The `?` rows + 4 held docs never get killed on a guess — each gets a capture-check during the (b) consolidation.

**Author:** gandalf, 2026-06-30. The pile remembers every step of the road; the spec only needs to remember the destination. Git keeps the road.
