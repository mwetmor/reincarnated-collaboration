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
| 2026-06-02-season-archive-realm-expansion-pivot **(⚠ PARTIAL — DELETE HELD)** | →TRACKER | ⚠ DELETE HALTED 2026-06-30 (verify caught 8+ live engine refs). Isekai content-model (Realm Expansion / ascension / economic-veteran §5 / genre-departure §4) DEAD by "all v1 isekai gone"; **engine-architecture spine §3.2/§3.3/§3.4/§6 LIVE + uncaptured → partial-supersession BANNER, NOT deleted.** Seasonal-retire conclusion → gameplay-loop §19/§23; engine gap (kit-space emission live-vs-cycle-14-bundle) → engine-tracker PART II; §9.1/§9.2 → git. Final `git-rm` gated on engine-spine fold. |
| 2026-06-18-companion-difficulty-inversion-and-spirit-guide-combat-bridge | ? | references RETIRED spirit guide + "Season-2" — reconcile or KILL |
| ~~2026-06-22-faction-descent-and-reward-loop-recognition~~ **✓ FOLDED + DELETED 2026-06-30** | →STORY | captured → gameplay-loop §5/§9/§11; anti-faction mega-boss ruled SUPERSEDED (v2 §8); source deleted |
| ~~2026-06-22-seasonal-descent-architecture-recognition~~ **✓ FOLDED + DELETED 2026-06-30** | →STORY | captured → gameplay-loop §6/§7/§8/§23 + engine-tracker III + game-tracker B2; source deleted |
| ~~2026-06-22-seasonal-descent-content-audit~~ **✓ FOLDED + DELETED 2026-06-30** | →TRACKER | findings → engine-tracker III.1/III.5/III.6/III.7; source deleted |

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

**Batch 2 — B3 ANCHOR fold (EXECUTED, commit `f9f763e`):** folded `2026-06-11-avatar-projection-and-hall-of-heroes-framing` → `story-expansion.md §12` (two-space possibility/possession + "conflating them is a design error"; molting=harvest; sparse-hub; D7 lookup-not-generation), v2-reconciled; unsettled surface-mapping routed [OPEN]→ tracker B1/B2; the source's §4.1 presentation survivor (recurring-transition principle) re-homed to game-tracker A′2 (BANKED) — it was a PC/UE-seam routing orphan; source deleted; 4 inbound refs re-pointed (00-index, companion doc ×2, this map). **story/ 75 → 74.** Chosen as the first B3 unit precisely because it was small (64 L), high-value (content in NO other spec — lossy if deleted unfolded), and fully my domain (I can make the v2-reconciliation calls solo).

**Batch 3 — Q5/Q6 ratification + companion MEDIUM fold (EXECUTED 2026-07-01):** Matt ratified the **fit-audit slate** (Q5 — all 7 verdicts, with the load-bearing **two-register refinement**: *"the grimoire is only a listing of who you've been, you can't use them like a hall"* → claimed souls = usable/summonable; own past lives = LISTING-FIRST — refinement-2 same-day: **rationed re-summon**, 1 free/playthrough + ~3–5h materials each, design-decisions §6 proposal → RULED; re-inhabit ≠ deploy, the Hall-verb stays dead) and the **(b′) default-delete purge process** (Q6 — consultant memo §5/§7 governs). Applied: `story-expansion.md §12` rewritten per tracker A11 (possession space = the Grimoire, no Hall; possibility = *encountered in the descent*, not shopped; molt feeds the listing, not the party); `gameplay-loop-design.md §11` two-registers block annotated with the Matt-verbatim ruling; **companion doc folded → §12** (claimed-soul companion, scarcity/proxies separation, D7, Path Pure run-1-alone → B3) and **deleted**; 9 live citers re-pointed (OP + SKILL format-example swapped to `season-archive-pivot` — the one doc guaranteed to stay bannered). **Rulings-harvest agent returned: 45 SAFE-TO-DELETE / 26 NEEDS-HARVEST** (`gandalf/notes/2026-07-01-rulings-harvest.md`; proposed ledger row per sole-carrier ruling) — gates Batch-1 deletions. **story/ 74 → 73.** Specialist silence-is-consent: `companion_generation.py:22` governing-design cite → re-point to `reap-die-rise-story/story-expansion.md §12` + tracker B3 (**rocket**, at next touch; kit math unaffected — only the story-sourcing re-registered).

**Batch 1 — (b′) default-delete EXECUTED (2026-07-01):** first mass-delete under the Q6-ratified process; rulings pre-harvested (`gandalf/notes/2026-07-01-rulings-harvest.md` — sole-carrier ledger rows proposed there for KR/jack-ryan decisions-log routing). **19 DELETED:** 5 marginal-lineage dispositions (arctic / mesoamerican / oceanic / south-american / n-am-no-cluster) · variant-cluster-policy-assignments · ab-comparison-protocol-cycle-14-close · autonomous-fire-prompt-template · weapon-substrate-conclusion-declaration · engine-architecture-canonical-synthesis · autonomous-run-plan-v2 *(11 engine-src citers all MIGRATION / AGENT_STATE / dated-math = lineage class)* · seasonal-hero-h-5-hybrid-spec + arpg-physical-magical-ratio-baseline *(Cluster-D members, stale/captured-at-#57 — engine 00-index rows struck so the B4 fold doesn't chase them)* · engine-greenfield-verdict · experiential-cascade-recognition · fate-genre-recognition *(38/39/41 citers are Batch-2 fold-pending; dangles accepted)* · tal-rasha-glyphic-primitive *(consumer died with the A11 cosmograph kill; the rune-as-keystone sliver already lives in story-expansion §12)* · substrate-generalization-track-c *(captured in multi-dim-convergence)* · engine-as-general-serial-content-product *(captured in CLAUDE.md orientation banner + doc 38)*. **6 E2-MOVED** (citer-class spot-check found live OP/SKILL/code cites → move-whole + re-point, NOT delete): visual-benchmark-vs2a + geometry-vfx-coverage-assessment → `agentic_orchestration/galadriel/notes/` · w1-13-rescope → `gamora/notes/` · loadout-analytics-IA → `drax/notes/` · cleaning-policy + marginal-lineage-tagging-pattern → `elrond/notes/` *(per the engine 00-index substrate-curation routing)*. 14 OP/SKILL citers re-pointed (galadriel/gamora/drax/star-lord/elrond/gandalf/hive-mind, OP+SKILL each); verified zero stale paths. **1 RECLASSIFIED HOLD→Batch-2:** asset-pipeline-meshy-swap — a RULED pipeline decision (Meshy pass-through) with 4 live OP/SKILL cites + doc-38 + style-register; folds into `reap-die-rise-engine/` WITH 38, then re-point. **Silence-is-consent flags:** **drax** (`reincarnated-demo/src/abilities/vfx.ts` cites moved geometry-vfx doc — re-point comment at next touch), **jack-ryan** (`engineering-disciplines.md` cites moved tagging-pattern — cross-repo textual ref, re-point at next touch), **elrond** (2 docs re-homed to his notes/), **galadriel/gamora/star-lord/KR** (mechanical OP path swaps). Decisions-log + MIGRATION/AGENT_STATE/math-note dangles = lineage, accepted per Q6 (git holds). **story/ → 45 .md** (19 deleted + 6 moved; prior ledger count "73" was over-stated by ~3 — empirical recount governs).

**Batch-1 addendum — NEEDS-HARVEST 26 resolved per Matt "do not defer the deletions to other agents" (2026-07-01):** the 26 split by disposition, not deferred: **19 Cluster-D/spec-content docs die inside the Batch-2 engine folds** (fold-first per harvest note 5 — ruling-clearance ≠ content-clearance); **season-archive** folds spine §3.2–3.4 → engine spec then deletes; **atomic-substrate-registry** (KEEP) moves INTO `reap-die-rise-engine/` as spec member; **style-register** folds in Batch 3. Immediate: **designer-writes + v1-1-plus DELETED** (proposed disciplines entries stand verbatim in the harvest doc §Methodology — jack-ryan registers at next disciplines touch, non-gating); **hypothesis-flow RECLASSIFIED disciplines-route → Cluster-D engine fold** (live engine sidecar `emit_experiential_axes.py` + `experiential_axes_v1.json` name it GOVERNING — §3.5 cell-schema + §1.7 flavor locks are spec content; the harvest's disciplines routing missed the code cite); **legacy-categorical-cleanup-audit E2-MOVED → `elrond/notes/`** (gandalf session-start read + elrond Pattern-R-3 example — 4 OP/SKILL citers re-pointed). **story/ → 42 .md.**

**Batch 4 — cosmograph trio HEAVY fold EXECUTED (2026-07-01, Matt: "begin the cosmograph fold. Approved."):** the two B3-remaining heavies + the LOD split-doc (471 + 920 + 263 L) folded per tracker **A11** (cosmograph-browse DEAD; creation moment KEEP-RESKIN as dark sacrament; night-sky = presentation-park). Distillation, four destinations: **(1) story** → `story-expansion.md §13a` **The Binding Rite** (conducted rite not menu; two paths one substrate; 7-anchor player-named-precedent elicitation cascade re-voiced to the jailer's tutorial voice-slot — the mentor who asks what you want so the crusade can use it is the cage being fitted; INPUT/OUTPUT partition; vessel-as-canvas; sign-the-pact 4-layer semantic) + §12 pointer fix (A′2→A′3); **(2) presentation** → game-tracker **A′3** (BANKED package: spherical-shell sky + centroid-first 3-level LOD + rune-glyph register + cycling-preview + text-carries-options; admitted uses = patron's night-sky of reaped souls + Binding-Rite staging; browse-use DEAD; /forge dev-surface anchor `cb2d60d`) + **B5** (rite build, someday-scope, drax-gated); **(3) engine** → `reap-die-rise-engine/00-index.md` creation-flow contract (pre-generate corpus; rite SELECTS+LOOKS-UP, nothing generated at the altar — D7; nearest-kit honoring player-named precedent; coverage-filtered display, no 0-match); **(4) engine-tracker III.9** cosmograph/earth-avatar reconciliation bullets ✓ DONE-BY-FOLD (IV.2 #6 narrowed to the design-decisions §1 device-orphans). Live citers re-pointed (both trackers + rdr-story 00-index); ~10 lineage citers (dispatches, QA findings, CHANGELOG, dated notes) left as dated records per citer-classification. Sources deleted. **story/ 42 → 39 .md.**

**B3-remaining classification (survey finding — the anchor was the ONE clean small unit; the other 8 are ~2,800 L, ALL load-bearing, several split-sources routing a presentation-half to the GAME tracker like the anchor's §4.1 did):**

| Doc | L | Shape | Disposition |
|---|---|---|---|
| ~~`2026-06-05-cosmograph-pivot`~~ **✓ DONE 2026-07-01** | 471 | **tri-seam split:** story + presentation + substrate-viz | FOLDED per Batch 4 — browse DEAD (A11); presentation banked → game-tracker **A′3**; engine lookup-contract → rdr-engine 00-index; deleted |
| ~~`2026-06-07-earth-avatar-cosmograph-creation-moment`~~ **✓ DONE 2026-07-01** | 920 | **split:** story + presentation | FOLDED per Batch 4 — reskinned → `story-expansion §13a` **The Binding Rite** (dark sacrament); staging → game-tracker **A′3**; elicitation-cascade engine contract → rdr-engine 00-index; deleted |
| ~~`2026-06-13-companion-as-hall-of-heroes`~~ **✓ DONE 2026-07-01** | 141 | story; **re-sourced by A11** (companion = claimed soul, NEVER past self; Path Pure run-1-alone survives; dyad/per-season premises DEAD) | FOLDED → `story-expansion §12`; residue → tracker B3; citers re-pointed (`companion_generation.py` → rocket silence-is-consent); deleted |
| ~~`2026-06-07-cosmograph-cross-surface-LOD`~~ **✓ DONE 2026-07-01** | 263 | **split:** story + ENGINE (LOD architecture) | FOLDED per Batch 4 — centroid-first 3-level LOD banked → game-tracker **A′3** (presentation vocabulary; ratifies if/when drax builds a night-sky surface); deleted |
| `2026-06-02-season-archive-realm-expansion-pivot` **(⚠ PARTIAL — DELETE HELD)** | 449 | mixed doc: isekai content-model DEAD, engine-architecture spine LIVE (the "KILL-CAPTURED clean-kill" guess was **verify-RED corrected** — §3.2/§3.3/§3.4 are the canonical commitment behind `data/kit_space/` + chronicle + emitter, 8+ inbound refs) | **PARTIAL-SUPERSESSION BANNER applied; NOT deleted.** Isekai model dead by ruling; seasonal-retire → gameplay-loop §19/§23; engine spine §3.2/§3.3/§3.4/§6 → engine-tracker PART-II gap (live-vs-cycle-14-bundle question); §9.1/§9.2 → git; OP/SKILL/A4 cites re-pointed. **Final `git-rm` gated on engine-spine fold to `reap-die-rise-engine/`.** |
| ~~`2026-06-22-faction-descent-and-reward-loop`~~ **✓ DONE 2026-06-30** | 262 | story (descent / faction-walled-from-combat) | FOLDED → gameplay-loop §5/§9/§11; anti-faction mega-boss SUPERSEDED (v2 §8); deleted |
| ~~`2026-06-22-seasonal-descent-architecture`~~ **✓ DONE 2026-06-30** | 278 | **split:** story (descent-arc) + presentation (floor-authoring/camera) | FOLDED → gameplay-loop §6/§7/§8/§23 + engine-tracker III + game-tracker B2/A1–A3/A′1; deleted |
| ~~`2026-06-22-seasonal-descent-content-audit`~~ **✓ DONE 2026-06-30** | 264 | audit deliverable | FOLDED → engine-tracker III.1/III.5/III.6/III.7; deleted |

*(`2026-06-18-companion-difficulty-inversion` already deleted in Tranche 1; its S2 investigation is preserved in `companion-as-Hall §7`.)*

**Shape:** the clean **KILL-CAPTURED** verify-and-deletes are `season-archive-pivot`, `faction-descent`, `content-audit`, and the presentation-already-promoted `seasonal-descent-architecture` story-half. The **HEAVY** folds are the two cosmograph docs (471 + 920 L, tri-seam — presentation halves → game-tracker like A′2). `companion` is a MEDIUM fold with opens already routed. **B3-remaining is genuinely multi-session and routes presentation-halves to the game tracker (drax) — mirroring the B4 cross-seam pattern; it is NOT a quick delete-pass.** Next B3 session: take the KILL-CAPTURED four first (cheapest, cleanest), then the companion medium, then the two cosmograph heavies last.

**⚠ LOAD-BEARING FINDING — v1→v2 supersession reshapes B2 AND B4 (the engine-mechanics folds are NOT a uniform reframe-and-move):** the flat `37–51` docs (B2) and the Cluster-D story/ engine-mechanics docs (B4) are **v1 / seasonal-era**. The v2 run-model (`reap-die-rise-story/gameplay-loop-design.md` §7/§23) has **already superseded chunks** — most sharply **progression**: doc `41`'s seasonal-L50-cap model is superseded by gameplay-loop §7's **descent/sawtooth** (floors-trail-power-by-2, old-floors-never-rescale). So the engine-mechanics fold **splits three ways, per-doc, and must be capture-checked — not blind-folded:**
- **(a) run-invariant mechanics** — `39/40/42/46/47/51` (gear/stat/damage/concentration/scaling/investment *math*): the math doesn't care seasonal-vs-run → **fold as reframe.** This is the heavy **connected multi-session spine** (docs `43/44/45/46/40/47/41/49` cross-reference each other; cherry-picking a subset creates stale refs). **Clean order = 40-first** (doc `40 §8.5` already carries `41`'s mechanical survivors — 5/15/1 caps, ~70-pt budget, 70%-chain T4-unlock, L1→L50 earn — and cross-refs `41`).
- **(b) superseded-by-run-model** — `41` progression (+ parts of `37/38/50`): **verify-superseded → capture any orphan → delete; do NOT forward-fold.** `41`'s survivors already live in `40 §8.5`, so `41` deletes **AFTER `40` folds** (not before — or `40`'s cross-ref dangles).
- **(c) landed-in-code** — `43/44/45` (Wave-N *intent* docs): **thin lineage pointer → delete** (code is the authority; full re-read unnecessary — grep-verify the code citation).

**This is the essential context for the B4+B5 handoff:** Cluster-D carries the *same* v1-seasonal-era issue, so B4 is a **capture-check, not a blind fold** — each doc classified (a)/(b)/(c) against the run-model + engine code + engine tracker before any delete. knight-rider must brief the specialists (rocket/gamora/star-lord) with this three-way split, or they will forward-fold superseded v1 progression as if it were live spec.

**Remaining Tranche-3 batch spine (ordered; each fold = distill→verify-capture→delete):**
- **B2 — flat `37–51` engine spine → `reap-die-rise-engine/`** (Matt's "stand-alone docs first"). **NOT a uniform gandalf-fold — the three-way split above applies:** (a) run-invariant math = the connected multi-session spine, **40-first**; (b) `41` progression superseded-by-run-model → delete after 40; (c) `43/44/45` intent-in-code → thin pointer + kill. Genuine multi-session; do not cherry-pick the cross-referenced spine.
- **B3 — story/ Cluster C (story-frame) → `reap-die-rise-story/`.** Gandalf-solo (story = my domain); v2-reconcile (retired labels die, structure survives).
- **B4 — story/ Cluster D (engine-mechanics) → `reap-die-rise-engine/`.** **Cross-seam** — capture-check vs engine tracker/build-docs/code; may route to rocket/gamora/star-lord rather than gandalf-fold. **→ HANDED TO knight-rider (Matt 2026-06-30):** full brief at `gandalf/notes/2026-06-30-b4-b5-knight-rider-handoff.md` (cluster lists + the v1→v2 split + discipline constraints + the B4⇄B2 coordination flag). Matt is the conduit to KR's session.
- **B5 — routes:** Cluster E substrate → **elrond** (EXCEPTION: `atomic-substrate-registry` keep); Cluster F principle docs (`designer-writes-substrate`, `v1-1-plus-disciplines`, `hypothesis-flow-pattern-library`) → **jack-ryan disciplines**; remaining Cluster F infra/genre records → per-doc capture-check then kill (incl. re-check `federated-pc-team` now that CLAUDE.md dropped it — sole citer is the engine index). **→ HANDED TO knight-rider** in the same brief (§2).
- **B6 — Tranche-5 remainder:** CLAUDE.md "Where to find things" table still points at stale `canonical/` numbered paths + `canonical/historical/16-project-roadmap.md` — rewrite to the folder structure.

## 7. The gate

**Resolved (Matt 2026-06-30):** (1) clusters ratified; (2) fork = **(b)**; (3) Tranche 1 = go → **FIRED**.

**Next open item:** the Tranche-2 sequencing fork (§6.2) — rename `reap-die-rise/` now vs. fold-into-new-folders-first-and-retire-last. My rec: the latter (fewer link churns). The `?` rows + 4 held docs never get killed on a guess — each gets a capture-check during the (b) consolidation.

**Author:** gandalf, 2026-06-30. The pile remembers every step of the road; the spec only needs to remember the destination. Git keeps the road.
