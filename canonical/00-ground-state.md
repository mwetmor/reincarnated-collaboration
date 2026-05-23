# 00 — Ground State Oracle

> **STATUS:** CURRENT (load-bearing as of 2026-05-23) — this doc IS the oracle; see Section 1 for the current-truth table

**Status:** LIVING. This is the **first read for every agent on every invocation.**
**Last updated:** 2026-05-23 (gandalf, post D1-D10 lock)
**Update protocol:** edited whenever epoch shifts. Authored / maintained by gandalf.
**Purpose:** name the current epoch, identify the load-bearing canon, demote historical artifacts, and give every agent a sub-60-second orientation.

---

## TL;DR (read this paragraph first)

We are in **Epoch 4 — Vast-Library + Variant C + D1-D10 Delivery-Strategy Lock.** The engine is a general serial-content product (Variant C); the game (Reincarnated) is one of its products, currently positioned as isekai but **provisionally** so (D10 — substrate-evidence gate). The 89,839-row weapon substrate landed 2026-05-22 (hive-mind Cycle 8). Engine P0 closed 2026-05-22 with tag `v0.0-constraint-removal-shipped`. Downstream-delivery strategy locked 2026-05-23 in `canonical/38-downstream-delivery-strategy-2026-05-23.md`. The active workstream is documentation cleanup + ground-state stamping (this doc is part of it).

**If you only read one other doc, read `canonical/38-downstream-delivery-strategy-2026-05-23.md`.** It captures D1-D10 and supersedes all prior delivery-framing discussion.

---

## 1. What is CURRENT TRUTH (load-bearing, top-of-stack)

Read these as authoritative for ongoing work.

| Doc | Owns | Status |
|---|---|---|
| `canonical/38-downstream-delivery-strategy-2026-05-23.md` | Delivery strategy lock (D1-D10): Unreal, PC-first, variable execution, seasonal cadence, humanoid-only, isekai-provisional, ~200-220 day timeline | **CURRENT — keystone** |
| `canonical/02-roadmap.md` | Current roadmap (workstream sequencing + dependencies + empirical-evidence-gated deferred commitments); supersedes A-series roadmap | **CURRENT — living doc** |
| `canonical/37-engine-and-game-two-products.md` | Variant C lock: engine vs game as two products | CURRENT |
| `canonical/story/engine-as-general-serial-content-product-2026-05-22.md` | Variant C strategic frame (story-side) | CURRENT |
| `canonical/story/gear-heavy-promotion-2026-05-22.md` | Vast-library substrate architecture | CURRENT |
| `canonical/story/hive-mind-protocol-weapon-library-import-2026-05-22.md` | Substrate-acquisition hive-mind protocol | CURRENT |
| `canonical/story/multi-dim-convergence-algorithm-2026-05-21.md` | Substrate-vector axes (BC convergence) | CURRENT |
| `canonical/story/gear-substrate-rule-table-v1-2026-05-22.md` | Gear substrate rule table | CURRENT |
| `canonical/story/tier-4-architecture-defaults-2026-05-22.md` | T4 architecture defaults | CURRENT |
| `canonical/story/stat-derivation-from-bc-convergence-2026-05-22.md` | Stat derivation from BC | CURRENT |
| `canonical/story/asset-pipeline-meshy-swap-2026-05-22.md` | Asset pipeline (Meshy / Control Rig / Unreal) | CURRENT |
| `canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md` | Patterns 4-5-6 retirements audit | CURRENT |
| `canonical/story/style-register.md` | Visual style register filter (used by D10 Path A) | CURRENT |
| `canonical/story/w1-13-rescope-disposition-2026-05-22.md` | W1.13 rescope (LC-011 disposition) | CURRENT |
| `canonical/story/fate-genre-recognition-and-mobile-alignment-trajectory-2026-05-23.md` | Fate-genre recognition trajectory; D10 Path C alignment; mythological-named-weapons substrate layer; Reincarnation War franchise banner; faction emergence; Rift as cross-cultural merge mechanic; mobile-platform alignment; D1 reconsideration paths (logged, not resolved) | **CURRENT — recognition record (architectural commitments deferred per § 9)** |
| `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` | 20 engineering disciplines (1-17, 18 methodology-before-execution adopted 2026-05-23, 19 Agent-tool-not-for-waiting; plus R-prescriptions and named patterns) | CURRENT |
| `agentic_orchestration/gandalf/notes/2026-05-23-mathematical-seam-naming.md` | Mathematical Layer cross-cutting declaration + math-hotspot living list + Discipline #18 rationale | CURRENT (integrated 2026-05-23) |
| `~/Games/reincarnated-engine/design/decisions/decisions-log.md` | Temporal decisions log | CURRENT |
| `agentic_orchestration/AGENTS.md` | Team topology + scope map | CURRENT |
| `agentic_orchestration/GOVERNANCE.md` | Founding ADRs | CURRENT |
| `agentic_orchestration/REVIEW_PROCESS.md` | Review process + 5 principles | CURRENT |
| `agentic_orchestration/weapon-library-import-wind-down-summary-2026-05-22.md` | 89,839-row substrate state | CURRENT (live state ref) |

## 2. What is HISTORICAL but informative (consult for lineage, not current truth)

These shaped current canon. They are NOT wrong. They are NOT current. Read them only when you need to understand *how we got here*.

| Doc | Why it's historical | Where its work landed |
|---|---|---|
| `canonical/29-design-overview.md` | 2026-05-12 strategic anchor; predates Variant C | Superseded by 37 + 38 |
| `canonical/16-project-roadmap.md` | A-series roadmap; predates QD-rebuild + vast-library pivot | Superseded by hive-mind protocol + doc 38 |
| `canonical/28-engine-arpg-rebalance-design.md` | B-series engine queue; predates P0 closure | Mostly landed; consult for B-item context |
| `canonical/30-engine-explainer-current.md` | demo1 v1.2 baseline | Demo1 still exists; engine has evolved past |
| `canonical/31-engine-explainer-future.md` | Pre-Variant-C future state | Variant C reframes this |
| `canonical/32-progression-design.md` | Progression-design 12 sections | LOCKED entries stand; framing is pre-substrate-as-cohesion |
| `canonical/33-progression-skeleton.md` | Locked-only summary of 32 | Same |
| `canonical/35-stage-a2-cli-prompt.md`, `canonical/36-b14-5-cli-prompt.md` | Stage-A2 + B14.5 CLI prompts | EXECUTED; outputs landed |
| `canonical/37-form-bias-diagnosis-and-recovery.md` | Form-bias work (2026-05-14–16) | Superseded by substrate-as-cohesion architecture |
| Most `canonical/story/*-2026-05-14.md` through `canonical/story/*-2026-05-18.md` | Form-bias + substrate-coupling epochs | Folded into current QD-rebuild + vast-library work |
| `canonical/story/*-2026-05-19.md` through `canonical/story/*-2026-05-21.md` | QD-engine rebuild epoch | Foundation for current vast-library work |
| `agentic_orchestration/skill_handoff_2026-05-13.md` through `skill_handoff_2026-05-22.md` (most) | Daily handoffs | Cumulatively folded into current state; read latest only |
| `canonical/README.md` (this folder's own README) | 2026-05-12 README; predates everything above | Historical; this `00-ground-state.md` supersedes its "read order — first time" section |

**Default rule:** if a `canonical/story/` doc is dated before 2026-05-22 and is not on the CURRENT list (Section 1), treat it as historical. It informed; it does not direct.

## 3. What is DEAD — do NOT consult as current truth

| Pattern | What's dead | Why |
|---|---|---|
| **Pre-imposed aesthetic-tuple dimensions** (Pattern 4) | RETIRED 2026-05-22 | Replaced by emergent aesthetic clusters from data |
| **15-entry gear catalogue** (Pattern 5) | RETIRED 2026-05-22 | Replaced by vast-library substrate (~89K rows + growing) |
| **Pre-imposed axes** (Pattern 6) | RETIRED 2026-05-22 | Replaced by discovered axes from PCA / factor analysis on substrate |
| **Form-bias diagnosis framing** | Superseded 2026-05-19 | Substrate-as-cohesion architecture absorbs the form-bias concerns |
| **Pure-auto-combat consideration** | REJECTED 2026-05-23 (D2) | Variable execution by build (substrate-axis-driven) is the lock |
| **Mobile-first framing** | REJECTED 2026-05-23 (D1) | PC/console-first + mobile-port at +6 months |
| **Non-humanoid playable forms** | REJECTED 2026-05-23 (D9) | Humanoid-only playable; non-humanoids as bosses/pets/fauna |
| **W0.7-framework ablation cycle** | CLOSED 2026-05-22 | LC-002, LC-009, LC-011 disposed of; no further W0.7 sweeps warranted |
| **"Monthly" as a cadence term** | REJECTED 2026-05-23 (D3) | We say "seasonal" consistently; weekly beats live inside seasons |

If you find yourself building on any of these, stop. You are in a dead branch.

## 4. First-reads by role (every invocation)

Replaces the per-agent multi-doc Phase-1 reading list with a focused short list. Every agent reads this `00-ground-state.md` doc first, then their role-specific reads.

| Role | First reads (after this doc) |
|---|---|
| **knight-rider** | doc 38; latest `agentic_orchestration/skill_handoff_*.md`; current hive-mind state file; engineering-disciplines |
| **jack-ryan** | doc 38; engineering-disciplines; decisions-log; latest critique-pair dispatch |
| **gandalf** | doc 38; own latest 3 notes (`agentic_orchestration/gandalf/notes/`); style-register; legacy-categorical-cleanup-audit |
| **rocket** | doc 38; substrate-vector axes; gear-substrate rule table; tier-4 architecture defaults; engineering-disciplines |
| **gamora** | doc 38; multi-dim-convergence-algorithm; w1-13-rescope-disposition; engineering-disciplines |
| **star-lord** | doc 38; asset-pipeline-meshy-swap; loadout-analytics-suite info-arch; engineering-disciplines |
| **elrond** | doc 38; gear-heavy-promotion; hive-mind protocol; weapon-library wind-down summary |
| **galadriel** | doc 38; style-register; visual-benchmark-vs2a; geometry-vfx-coverage-assessment |
| **drax** | doc 38; loadout repo's own README + recent commits; relevant `canonical/story/loadout-*` docs |
| **legolas** | doc 38; latest gandalf request; relevant hive-mind protocol section |

**Do NOT re-walk the full historical archive on every invocation.** It is searchable when needed. It is not pre-load material.

## 5. Active workstreams (what's actually in flight)

| Workstream | Status | Owner(s) |
|---|---|---|
| Documentation cleanup (this pass) | ACTIVE — `00-ground-state.md` just landed; epoch-stamping next; onboarding-list shrink after | gandalf (oracle); knight-rider (epoch-stamp dispatch); jack-ryan (onboarding-list review) |
| Skill packaging (Skill Creator + Skill Seekers) | QUEUED — post-cleanup, pre-architecture-validation | gandalf design; knight-rider orchestrate |
| Architecture-validation spike (Unreal pipeline) | QUEUED — ~2 weeks out | Matt + knight-rider scope; specialists per integration |
| Weapon-library substrate Phase 2 (axis discovery) | QUEUED — pending Matt direction on D1 (accept 89.8% or fire Wave-4) | knight-rider dispatch; rocket + legolas execute |
| Stage 1 cluster checkpoint (D10) | DEFERRED — fires after Phase 4 of hive-mind protocol | Matt + gandalf |
| MVP scope lock | DEFERRED — fires after Stage 1 | Matt + gandalf + jack-ryan |
| Engine P0 → P1 transition | OPEN — P0 closed 2026-05-22; P1 hypothesis tests (W1.20-W1.22) pending | gamora + jack-ryan |

## 6. Single-source-of-truth contracts

When two docs disagree, **the latter is canonical:**

1. `canonical/38-downstream-delivery-strategy-2026-05-23.md` overrides any earlier delivery / engine / cadence / execution framing.
2. `canonical/37-engine-and-game-two-products.md` + `canonical/story/engine-as-general-serial-content-product-2026-05-22.md` override any "single-product" framing in older docs.
3. `canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md` overrides any Pattern 4-5-6 references in older docs.
4. `engineering-disciplines.md` overrides any older discipline lists in older docs.
5. `decisions-log.md` is temporal ground truth for decisions; if it disagrees with a `canonical/story/` doc, decisions-log wins.
6. This doc (`00-ground-state.md`) overrides `canonical/README.md` for read-order and current-state questions.

## 7. Update protocol for this doc

This doc is **living.** Update it when:
- An epoch shift occurs (new top-of-stack architectural commitment)
- A canonical doc moves between CURRENT / HISTORICAL / DEAD categories
- A new active workstream opens or an active workstream closes
- A new first-read addition is needed for a role

**Do NOT update it for routine work product.** This is the oracle, not the changelog. The `CHANGELOG.md` and per-doc histories cover routine activity. This doc captures *structural state*.

Authored / maintained by **gandalf** (story-and-design steward).

---

**For agent onboarding flow:**

1. Read this doc (you are here).
2. Read doc 38 (`canonical/38-downstream-delivery-strategy-2026-05-23.md`).
3. Read your role's first-read short list (Section 4).
4. Begin work.

Total onboarding read budget: ~10-15 minutes. Not 1-2 hours.
