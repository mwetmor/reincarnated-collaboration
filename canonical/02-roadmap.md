# 02 — Current Roadmap

> **STATUS:** CURRENT (load-bearing, living doc) — see `canonical/00-ground-state.md`
>
> **Living-doc protocol:** updated whenever workstream state shifts (new workstream enters; existing closes; dependency landscape changes). Authored / maintained by gandalf. Supersedes `canonical/historical/16-project-roadmap.md` (A-series roadmap, HISTORICAL — predates QD-rebuild + vast-library pivot + D1-D10 lock).

**Date:** 2026-05-23 (initial authoring)
**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-23 — confirmed during cleanup-pass session
**Purpose:** name the active + queued + deferred workstreams with explicit dependencies + empirical-criterion gates. The companion to `canonical/00-ground-state.md` — the oracle says *what's true*; this doc says *what's sequenced*.
**Companion docs:**
- `canonical/00-ground-state.md` — current epoch + canon status
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` — D1-D10 delivery strategy keystone
- `canonical/37-engine-and-game-two-products.md` — Variant C lock (engine vs game)
- `canonical/story/fate-genre-recognition-and-mobile-alignment-trajectory-2026-05-23.md` — recognition record (commitments gated)
- `canonical/story/hive-mind-protocol-weapon-library-import-2026-05-22.md` — substrate-acquisition P-series
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` — engine-rebuild P-series

---

## 0. TL;DR

The roadmap has four layers:

1. **Active workstreams** (in flight RIGHT NOW): Phase D cleaning pipeline (elrond); canonical folder restructure (knight-rider); documentation cleanup continuation (gandalf).
2. **Queued workstreams** (immediate next, sequenced): per-agent operating-procedure skills; skill_handoff reframing; architecture-validation spike; substrate P2/P3/P4 sequence; engine P1 hypothesis tests.
3. **Deferred architectural commitments** (gated by empirical-evidence criteria, not time): D10 Path C lock as Fate-genre; D1 mobile-platform reconsideration; MVP scope lock; faction architecture; three-tier branding; Track M1 mythological-named-weapons fire.
4. **Out of scope** (not in current roadmap): items belonging to other canonical authorship or to specialist decisions outside the roadmap's reach.

Every deferred commitment lists the **specific empirical-evidence criterion** that gates re-engagement. Per the discipline: recognition → validate against substrate evidence → commit. No commitments fire on time-passage; all commitments fire on evidence.

---

## 1. Active workstreams (in flight)

### 1.1 Phase D cleaning pipeline (substrate normalization)

| Aspect | Spec |
|---|---|
| **Owner** | Elrond (executing under Pattern-B Gate-1 PASS-WITH-AMENDMENTS) |
| **State** | Mid-execution. Steps 1-6 complete per most recent reports; Steps 7+ in progress. |
| **Inputs** | 89,839-row weapon substrate (post-hive-mind-Cycle-8 wind-down). Phase A audit + Phase B policy + Phase C variant-cluster assignments completed earlier. |
| **Outputs** | Normalized substrate with `dedup_status` (canonical / merged / unprocessed); `weapon_kind` tagging; F1 RA TIERED collapse; F3 quarantines (pf2ools, souls-api); F4 cross-source canonical merge; updated v_category_sample view. |
| **Empirical criterion for completion** | All 7 cleaning steps committed; Discipline #11 empirical inspection at each gate passed; substrate ready for P2 axis discovery as feedstock. |
| **Unblocks** | P2 axis discovery (substrate Phase 2). |

### 1.2 Canonical folder structural restructure

| Aspect | Spec |
|---|---|
| **Owner** | Knight-rider (Pattern-B sub-agent dispatch authored 2026-05-23) |
| **State** | In flight (firing concurrently with this doc's authoring). |
| **Scope** | Move HISTORICAL-stamped docs to `canonical/historical/`; DEAD-stamped to `canonical/dead/`; same split for `canonical/story/`. Two outright deletes (CLI prompts 35 + 36). Cross-reference audit across all four sibling repos. Single end-of-pass commit. |
| **Empirical criterion for completion** | Commit lands; ~4 CURRENT docs visible at `canonical/` top-level; gandalf spot-check passes; cross-references resolved or flagged. |
| **Unblocks** | Cleaner browseable structure for next-session agents + Matt. |

### 1.3 Documentation cleanup pass continuation

| Aspect | Spec |
|---|---|
| **Owner** | Gandalf (story-and-design steward) |
| **State** | Near-complete. This roadmap doc closes the major-artifact authoring. Remaining: skill_handoff reframing as Matt-facing daily-state (queued, not yet executed). |
| **Empirical criterion for completion** | All cleanup-pass artifacts landed; agent-slowdown root cause (epoch-collision + per-invocation read budget growth) structurally resolved. |
| **Unblocks** | Team operates under disciplined documentation pattern; per-invocation read budget reduced 60-70%. |

---

## 2. Queued workstreams (sequenced, post-active)

### 2.1 Skill_handoff reframing as Matt-facing daily-state

| Aspect | Spec |
|---|---|
| **Owner** | Jack-ryan (working-agreement review) + knight-rider (integration) |
| **Trigger** | Cleanup pass continuation (1.3) closes |
| **Scope** | The next end-of-session handoff written by knight-rider treats Matt as primary audience (not next-session knight-rider). Sections: pending Matt-decisions queue; active workstreams + status; awaiting-Matt blockers; recent decisions Matt made; "next session pickup" guidance. |
| **Empirical criterion for completion** | Next handoff lands in new format; Matt confirms it's useful for session-start; pattern adopted as working-agreement. |
| **Effort** | Small (working-agreement edit + one handoff in new format). |

### 2.2 Per-agent operating-procedure skills + cross-cutting work-mode skills (Skill Creator packaging)

| Aspect | Spec |
|---|---|
| **Owner** | Multi-agent coordination via knight-rider; each agent authors their own per-agent OP skill; cross-cutting skills authored per ownership lineage |
| **Trigger** | Cleanup pass continuation (1.3) + Skill_handoff reframing (2.1) land |
| **Stream 2 — per-agent OP skills** | Thin operating-procedure skill (~500-800 words): session-start protocol; mode-selection (what kind of work is this session?); session-end protocol. Specialized work-mode skills compose on top |
| **Stream 2 landed (2026-05-23 morning)** | `operating-procedures/gandalf.md` (prototype); `operating-procedures/jack-ryan.md`; `operating-procedures/knight-rider.md` |
| **Stream 2 landed (2026-05-23 fan-out)** | `operating-procedures/rocket.md`; `operating-procedures/gamora.md`; `operating-procedures/star-lord.md`; `operating-procedures/elrond.md`; `operating-procedures/galadriel.md`; `operating-procedures/drax.md`; `operating-procedures/legolas.md` (Pattern C parallel fan-out per `gandalf/requests/2026-05-23-knight-rider-stream-2-per-agent-op-fan-out.md`; gandalf executed on Matt direct authorization 2026-05-23) |
| **Stream 2 status** | **COMPLETE.** All 10 agents now have per-agent OP skills. |
| **Stream 3 — cross-cutting work-mode skills** | Compose on top of per-agent OP skills when in specialized work modes |
| **Stream 3 landed (2026-05-23 keystone)** | `operating-procedures/hive-mind-protocol.md` — hive-mind work-mode skill (gandalf author; cross-cutting; covering state entry/exit + Wave cadence + decision routing per Matt 2026-05-23 directive + critique-pair structure + Discipline #19 + math hotspots + Discipline #18 + state-file + wind-down + sub-agent verdict pattern § 5.5) |
| **Stream 3 landed (2026-05-23 batch)** | `operating-procedures/engineering-disciplines.md`; `operating-procedures/decision-log-format.md`; `operating-procedures/canonical-doc-format.md`; `operating-procedures/substrate-vector-cheatsheet.md`; `operating-procedures/critique-pair-gate-protocol.md` (gandalf foreground authoring; cross-cutting reference skills wrapping canonical sources) |
| **Stream 3 status** | **COMPLETE.** All 6 cross-cutting skills landed (1 keystone + 5 reference wrappers). |
| **Streams 2 + 3 status** | **BOTH COMPLETE.** 10 per-agent OP skills + 6 cross-cutting skills = 16 skills total authored as Markdown sources. |
| **Skill Creator packaging pass (2026-05-23)** | **COMPLETE.** All 16 Markdown sources converted to installable Claude Code skills at `.claude/skills/<name>/SKILL.md` with YAML frontmatter (name + description with auto-load triggers + version). Project-local skill registration; Markdown sources at `operating-procedures/` remain authoritative for revisions. |
| **Stream 2 + 3 + packaging — final status** | **ALL COMPLETE.** Skills auto-load per description triggers; per-invocation read budget empirical verification queued for next session-start under skill-load discipline. |

### 2.3 Architecture-validation spike (Unreal pipeline)

| Aspect | Spec |
|---|---|
| **Owner** | Matt + knight-rider scope; specialists per integration |
| **Trigger** | Skill packaging (2.2) lands (per doc 38 § 4 step 3) |
| **Scope per doc 38 § 4.3** | JSON output → Meshy → Control Rig → Unreal → playable form with one skill. Specific acceptance criteria: clean Meshy import; Control Rig export importable into Unreal; **image-pass-through-to-Meshy validation** on 3-5 museum-tier weapons vs ChatGPT-gen comparison; Niagara consuming JSON ability-spec; PCG room generation; TAA/TSR fast-combat readability validation. |
| **Effort** | ~1-2 weeks |
| **Empirical criterion for completion** | All sub-criteria pass per § 4.3 acceptance; or specific blockers identified for follow-on resolution. |
| **Unblocks** | D1 mobile-platform reconsideration (3.2); MVP scope lock (3.3); Track M1 indirectly. |

### 2.4 Substrate P2 — axis discovery (statistical methodology)

| Aspect | Spec |
|---|---|
| **Owner** | Elrond (execution); gandalf (design intent + acceptance criterion) |
| **Trigger** | Phase D cleaning pipeline (1.1) completes |
| **Scope** | PCA / factor analysis / NMF / UMAP / t-SNE methodology selection on sparse multimodal feature matrix; variance-explained validation; axis-stability bootstrapping; interpretability scoring. **Math hotspot per Discipline #18 — legolas Mode A methodology consultation required before execution.** |
| **Empirical criterion for completion** | Axes discovered with stability metrics + interpretability scores; ready for P3 multimodal clustering as feedstock. |
| **Unblocks** | P3 multimodal clustering (2.5). |

### 2.5 Substrate P3 — multimodal clustering

| Aspect | Spec |
|---|---|
| **Owner** | Elrond (execution); gandalf (design intent + acceptance criterion) |
| **Trigger** | P2 axis discovery (2.4) completes |
| **Scope** | HDBSCAN / k-means / GMM / spectral clustering choice; silhouette + Davies-Bouldin + gap-statistic validation; multimodal-distance-metric design; cluster-count selection. **Math hotspot per Discipline #18 — legolas Mode A methodology consultation required.** |
| **Empirical criterion for completion** | Clusters produced with validation metrics; ready for P4 semantic labeling. |
| **Unblocks** | P4 cluster semantic labeling (2.6); faction architecture canonical authoring (3.4). |

### 2.6 Substrate P4 — cluster semantic labeling

| Aspect | Spec |
|---|---|
| **Owner** | Matt + gandalf (design call) |
| **Trigger** | P3 multimodal clustering (2.5) completes |
| **Scope** | Name the ~50-150 emergent clusters with design-meaningful identity. Acceptance gate: **≥80% of clusters receive a design-meaningful name within one design call**. If <80%, methodology rerun triggered (back to P2 or P3 with refined methodology). |
| **Empirical criterion for completion** | ≥80% cluster naming with confidence; cluster taxonomy ready for cohesion-judge consumption. |
| **Unblocks** | D10 Stage 1 checkpoint (3.1); cohesion-judge validation (P5); faction architecture (3.4). |

### 2.7 Engine P1 hypothesis tests (W1.20-W1.22)

| Aspect | Spec |
|---|---|
| **Owner** | Gamora + jack-ryan |
| **Trigger** | P0 closed 2026-05-22; W1.13 rescope landed; W1.20-22 are diagnostic tests against archive data |
| **Scope** | BDI H1-H5 hypothesis tests against historical telemetry. Diagnostic, not generative. |
| **Effort** | Per gamora + jack-ryan scoping |
| **Empirical criterion for completion** | All H1-H5 hypotheses resolved (confirmed / refuted / reframed); diagnostic findings inform subsequent engine work. |

### 2.8 Substrate P5 — cohesion-judge validation

| Aspect | Spec |
|---|---|
| **Owner** | Star-lord (statistics execution); gandalf (design intent); gamora (simulation-side integration) |
| **Trigger** | P4 cluster semantic labeling (2.6) lands |
| **Scope** | LLM-as-judge calibration with statistical rigor; inter-rater reliability; significance testing; probability calibration via isotonic regression. **Math hotspot per Discipline #18 — legolas Mode A methodology consultation required.** |
| **Empirical criterion for completion** | Judge calibrated to acceptance threshold; tail-behavior reported alongside accuracy point estimates. |
| **Unblocks** | Production-grade content generation gated on validated cohesion judge. |

---

## 3. Deferred architectural commitments (gated by empirical-evidence criteria)

### 3.1 D10 Stage 1 checkpoint (Fate-genre alignment evidence)

| Aspect | Spec |
|---|---|
| **Decision deferred** | D10 Path A (tighten to isekai) vs Path B (shift framing copy) vs Path C (Fate-genre positioning) lock |
| **Empirical-evidence criterion** | P4 cluster semantic labeling completes; ≥80% of clusters express cultural-mythological-tradition identity (≥8-10 of the 13 predicted natural factions clearly clustered); spirit-guide narrative output coheres with Fate-genre register |
| **Decision authority** | Matt + gandalf design call |
| **Downstream consequence (if Path C confirms)** | Track M1 fires; faction architecture authoring opens; D10 architectural lock; doc 38 amendment; commercial-pitch material updates |
| **Downstream consequence (if Path A or B confirms instead)** | Different engine-tightening or copy-shift work fires; recognition-record doc gets amendment noting refined recognition |

### 3.2 D1 mobile-platform reconsideration

| Aspect | Spec |
|---|---|
| **Decision deferred** | D1 unchanged (PC-first + mobile port at +6mo) vs amended (simultaneous mobile + PC + console launch) vs mobile-primary (FGO model) |
| **Empirical-evidence criterion** | Architecture-validation spike (2.3) completes; Unreal mobile feasibility for ARPG depth confirmed; schedule analysis quantifies timeline impact of simultaneous-launch path (~3-6 additional calendar months estimated) |
| **Decision authority** | Matt |
| **Downstream consequence (if Path 2 — simultaneous launch)** | D1 amendment; timeline floor revised (~260-320 effective days, ~13-18 calendar months); mobile UI architecture acceleration; cross-platform infrastructure work fires |
| **Downstream consequence (if Path 1 — unchanged)** | Original D1 holds; mobile work remains at +6mo |

### 3.3 MVP scope lock

| Aspect | Spec |
|---|---|
| **Decision deferred** | Specific roster size, season count for launch, feature inclusion list, monetization model |
| **Empirical-evidence criterion** | D10 Stage 1 (3.1) resolves + architecture-validation spike (2.3) completes |
| **Decision authority** | Matt + gandalf + jack-ryan |
| **Downstream consequence** | All scope-creep candidates gated against this lock; jack-ryan enforces lock at milestones; ship-discipline anchor |

### 3.4 Faction architecture canonical doc

| Aspect | Spec |
|---|---|
| **Decision deferred** | Faction model specifics (allegiance fluidity; faction-coherent kit pools; Rift Event PVE/PVP framework; cross-faction summoning rules) |
| **Empirical-evidence criterion** | P3 multimodal clustering (2.5) validates faction-equivalent clusters; P4 cluster semantic labeling (2.6) names them; ≥8-10 of the 13 predicted natural factions clearly expressed |
| **Decision authority** | Matt + gandalf design call |
| **Downstream consequence** | Faction architecture canonical doc authored; integration with seasonal cadence design; Rift Event design scoped |

### 3.5 Three-tier branding lock ("Reincarnation War" franchise banner)

| Aspect | Spec |
|---|---|
| **Decision deferred** | Franchise banner ("Reincarnation War" vs "Spirit War" vs other); season-instance title; event-level naming pattern |
| **Empirical-evidence criterion** | Title-IP search completes (no blocking trademarks/conflicts); marketing director re-validation; D10 Stage 1 (3.1) confirms Fate-genre alignment |
| **Decision authority** | Matt |
| **Downstream consequence** | Branding canonical doc authored; marketing positioning lock; commercial-pitch material updates |

### 3.6 Track M1 — mythological-named-weapons substrate import

| Aspect | Spec |
|---|---|
| **Decision deferred** | Whether to fire Track M1 (estimated 2-3 day hive-mind cycle; 200-500 named-mythological-weapons entries) |
| **Empirical-evidence criterion** | D10 Stage 1 (3.1) confirms Fate-genre alignment; Phase D cleaning (1.1) complete; substrate ready for layered enrichment |
| **Decision authority** | Matt + gandalf + knight-rider dispatch |
| **Downstream consequence (if fires)** | Named-mythological substrate joined to existing weapon_knowledge_entries; faction-anchor objects available to cohesion judge; spirit-guide narrative templates can surface named-mythological echoes per form |
| **Placeholder usage in meantime** | Ad-hoc named-mythological references in in-flight design work (form-library concept notes, season concept docs, spirit-guide narrative drafts) are fine. These get bound to actual substrate rows when M1 lands. Standard refactor pattern. |

### 3.7 Monetization model

| Aspect | Spec |
|---|---|
| **Decision deferred** | Premium vs F2P vs hybrid; expansion pricing; mobile-port monetization model |
| **Empirical-evidence criterion** | First playable vertical-slice demo lands; MVP scope lock (3.3) resolves; market-test feedback if applicable |
| **Decision authority** | Matt |
| **Downstream consequence** | Monetization integration architected into game systems before MVP scope freeze |

---

## 4. Roadmap sequence (dependency view)

```
[ACTIVE — RIGHT NOW]
    Phase D cleaning (elrond)  ←  hive-mind state Cycle 9
    Canonical restructure (knight-rider sub-agent, background)
    Documentation cleanup continuation (gandalf, foreground)

         ↓ Phase D cleaning completes

[QUEUED — SUBSTRATE TRACK]
    P2 axis discovery (elrond + gandalf + legolas Mode A)
         ↓ Discipline #18 methodology consult → execute
    P3 multimodal clustering (elrond + gandalf + legolas Mode A)
         ↓ Discipline #18 methodology consult → execute
    P4 cluster semantic labeling (Matt + gandalf design call)
         ↓ ≥80% nameable clusters acceptance
    P5 cohesion-judge validation (star-lord + gandalf + gamora + legolas Mode A)

         ↓ P4 cluster labeling completes

[GATED — D10 STAGE 1 CHECKPOINT]
    Fate-genre alignment evidence reviewed
         ↓ if confirmed: Path C lock + downstream amendments fire

[POST-CHECKPOINT — ARCHITECTURE TRACK]
    Track M1 mythological-named-weapons substrate import (legolas + elrond)
    Faction architecture canonical doc (gandalf + Matt)
    Three-tier branding lock (Matt)
    D10 architectural amendment (gandalf)
    Commercial-pitch material updates

[PARALLEL — OPERATIONAL TRACK]
    Skill_handoff reframing (jack-ryan + knight-rider)
    Per-agent operating-procedure skills (multi-agent coordination)
    Architecture-validation spike (Matt + specialists)
         ↓ schedule + Unreal mobile feasibility
    D1 mobile-platform decision

[PARALLEL — ENGINE TRACK]
    Engine P1 hypothesis tests W1.20-W1.22 (gamora + jack-ryan)
    Engine P1 substrate enrichment (rocket + gandalf design-spec-as-math)

[POST-ALL-ABOVE — SHIP TRACK]
    MVP scope lock (Matt + gandalf + jack-ryan)
    Trial-boss-gallery roster (gandalf + Matt)
    Monetization model (Matt)
    Player-facing copy for continuity architecture (gandalf)
    Vertical-slice playable demo
    ...
```

---

## 5. What this doc does NOT decide

Out of scope for the roadmap; lives in other canonical authorship or specialist decisions:

- **Specific Unreal engine implementation choices** (Blueprint vs C++ boundary, plugin selection, asset-import-automation specifics) — owned by architecture-validation-spike outcomes
- **Specific cluster naming language** at P4 — owned by Matt + gandalf design call when P4 fires
- **Specific weapon-substrate per-row decisions** (which weapons to feature; which forms get which signature weapons) — owned by post-P4 form-library design work
- **Specific mythology selection for M1** (which traditions to import deeply vs lightly) — owned by post-Stage-1 M1 dispatch authoring
- **Specific monetization tier structure** (price points, F2P balancing, mobile-store positioning) — owned by post-MVP-scope-lock monetization design
- **Specific MVP roster size** — owned by post-Stage-1 scope-lock work
- **Provisional patent application timing** — Matt's domain (independent of dev roadmap)
- **Engineering disciplines** — jack-ryan's territory; lives in `engineering-disciplines.md`
- **Per-agent operating-procedure specifics** — owned by each agent authoring their own when 2.2 fires

---

## 6. How this doc gets updated

This is a **living doc**. Update triggers:

- **A workstream enters Active or moves between phases** — update § 1
- **An empirical-evidence criterion resolves and unblocks a deferred decision** — move from § 3 to § 1 or § 2; mark the dependency landscape change
- **A new workstream surfaces (from Matt direction or discovered need)** — add to § 2 or § 3 with explicit empirical-evidence criterion
- **An architectural commitment fires** — update § 3 to reflect lock; cross-reference the downstream canonical doc; mark the dependency change
- **A workstream completes** — strike from § 1; cross-reference completion artifact in § 6

Authored / maintained by **gandalf** (story-and-design steward). Knight-rider can update when workstream state shifts during orchestration.

---

## 7. Cross-references

### Active project canon this roadmap depends on
- `canonical/00-ground-state.md` — ground-state oracle
- `canonical/37-engine-and-game-two-products.md` — Variant C lock
- `canonical/38-downstream-delivery-strategy-2026-05-23.md` — D1-D10 delivery strategy
- `canonical/story/fate-genre-recognition-and-mobile-alignment-trajectory-2026-05-23.md` — recognition record
- `canonical/story/legacy-categorical-cleanup-audit-2026-05-22.md` — Pattern 4-5-6 retirements
- `canonical/story/hive-mind-protocol-weapon-library-import-2026-05-22.md` — substrate P-series
- `canonical/story/hive-mind-protocol-qd-engine-rebuild-2026-05-21.md` — engine P-series
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — 20 disciplines (including #18 methodology-before-execution + #11 empirical inspection)
- `~/Games/reincarnated-engine/design/decisions/decisions-log.md` — temporal decisions log

### Live state references
- `agentic_orchestration/weapon-library-import-hive-mind-state.md` — current hive-mind state
- `agentic_orchestration/weapon-library-import-wind-down-summary-2026-05-22.md` — 89,839-row substrate baseline

### Predecessor (HISTORICAL)
- `canonical/historical/16-project-roadmap.md` (formerly `canonical/16-project-roadmap.md`) — A-series roadmap; predates QD-rebuild + vast-library pivot + D1-D10 lock; consulted for lineage only

### Downstream artifacts this roadmap anchors
- Future workstream-specific dispatches (knight-rider authors per active workstream entries)
- Future architectural amendments (gated by § 3 empirical-evidence criteria)
- Future MVP scope lock canonical doc (post-Stage-1)
- Future faction architecture canonical doc (post-P3 + P4)
- Future monetization model canonical doc (post-MVP-scope-lock)

---

## 8. Sign-off

**Author:** gandalf (story-and-design steward)
**Authority:** Matt 2026-05-23 — confirmed during cleanup-pass session
**Status:** CURRENT — living doc; updated as workstream state evolves
**Maintenance:** gandalf authors + maintains; knight-rider updates when workstream state shifts during orchestration

**For:** the canonical record of the workstream sequencing, empirical-evidence-gated commitments, and active/queued/deferred status of Reincarnated's downstream work as of 2026-05-23. Supersedes A-series roadmap framing per the QD-rebuild + vast-library + D1-D10 + Fate-genre-recognition trajectory.
