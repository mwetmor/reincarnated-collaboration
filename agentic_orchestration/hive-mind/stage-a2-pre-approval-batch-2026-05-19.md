# Stage A2 Pre-Approval Batch — full dispatch set authored for Matt review

**Authored:** 2026-05-19 ~13:30Z by knight-rider per Matt directive 2026-05-19 ("approved, proceed all the way through Stage A2").
**Authority:** Matt directive 2026-05-19 (autonomous-operation + pre-approval-batch mode extended through Stage A2 closeout + Playtest Cycle 1).
**Status:** ALL Stage A2 dispatches authored + committed + pushed alongside VS2a + VS2b pre-approval batches. Combined sprint = **24 production dispatches + 2 Matt-gated** (+ 4 in-flight VS2a continuations).

---

## § 0 — TL;DR

Stage A2 closeout completes the engine's ARPG-rebalance design queue (`canonical/28-engine-arpg-rebalance-design.md`) — the B-series items deferred while VS2a + VS2b shipped. **7 dispatches** (A1–A7) covering B7 + B12 + B13 + B14 + B16 + design watch-items framework + Playtest Cycle 1.

After A7 ships, Stage A2 CLOSES. Stage A3 (B9 series; ~4-6 weeks) follows; pre-approval-batch decision for Stage A3+ DEFERRED to Matt at next wind-down session.

---

## § 1 — The seven Stage A2 dispatches

| # | Dispatch | Owner(s) | Effort | Activation gate | Acceptance tag |
|---|---|---|---|---|---|
| **A1** | B7 gear-percentile variance gate | gamora | 2-3 days | Stage A2 kickoff (VS2b ships) | `stage-a2/v0.1-b7-gear-variance-gate` |
| **A2** | B12 full audit (boots/gloves/belt + +%MS + cap) | rocket + gamora + drax | 1.5-2 wk | Stage A2 kickoff + A6 lands | `stage-a2/v0.2-b12-full-audit-complete` |
| **A3** | B13 post-narrow-slice (mobility geometries + AI + observability + trait-pool) | rocket + gamora + drax (telegraph UI) | 2.5-3 wk | Stage A2 kickoff + A6 lands | `stage-a2/v0.3-b13-post-narrow-slice-complete` |
| **A4** | B14 multi-band convergence sim | gamora | 2-3 wk | Stage A2 kickoff | `stage-a2/v0.4-b14-multi-band-convergence` |
| **A5** | B16 loot drop architecture (Drift-12 filing) | rocket + drax | 1.5-2 wk | Stage A2 kickoff + A6 lands | `stage-a2/v0.5-b16-loot-drop-architecture` |
| **A6** | Design watch-items framework (B12 visual/UX + B13 telegraph-art + B16 loot visual) | gandalf | 1 day | Stage A2 kickoff | `stage-a2/v0.6-design-watch-items-framework` |
| **A7** | Playtest Cycle 1 (prep + execution + disposition) | gandalf + knight-rider + Matt | prep 2d / exec 1d (HELD) / dispo 2-3d | A1-A6 land + Matt wind-down | `stage-a2/v1.0-stage-a2-ship` (Stage A2 CLOSED) |

---

## § 2 — Already-shipped (reference; no re-dispatch)

| Item | Status |
|---|---|
| B10.1 — Gauntlet density | ✅ Shipped |
| B10.2 — Composition | ✅ Shipped |
| B10.4 — Pack-scale | ✅ Shipped |
| B11 — Geometry palette expansion (16 → 25) | ✅ Shipped (VS2a) |
| B14.5 V1 — Primary loop architecture | ✅ Shipped (`v1.3-b14-5-primary-loop` 2026-05-12; canonical balance-loop pattern) |
| B6 — Class kit composition + Hierarchical Skill Tree | ✅ Shipping in VS2a (S2 + F4) |
| B13 narrow-slice (~25%) | ✅ Shipped Phase-1 P1 Deliverable 28 |

---

## § 3 — DAG of activation gates

```
VS2b ship ──► Stage A2 kickoff (stage-a2/v0.0-vs2b-baseline)
                              │
              ┌───────────────┼───────────────┬──────────────┐
              ▼               ▼               ▼              ▼
             A1              A6              A4         (M1+M2 HELD;
       (gamora B7)       (gandalf design   (gamora       carry-over from
                          framework)        B14)         VS2b)
                              │
              ┌───────────────┼────────────────┐
              ▼               ▼                ▼
             A2              A3               A5
       (B12 full audit)  (B13 post-       (B16 loot
                          narrow-slice)    architecture)
              │               │                │
              └───────────────┼────────────────┘
                              │
                              ▼
                            A7 prep
                       (gandalf rubric)
                              │
                              ▼
                    (Matt-gated: A7 execution)
                              │
                              ▼
                            A7 disposition
                       (gandalf playtest report)
                              │
                              ▼
                    stage-a2/v1.0-stage-a2-ship
                              │
                              ▼
                  (Stage A3 — B9 series; pre-approval
                   decision deferred to Matt)
```

---

## § 4 — Matt approval pattern (combined three batches)

Matt approves (extending VS2A → VS2B → Stage A2):

✅ Combined 24 production dispatches as full sprint scope:
  - VS2a: 12 dispatches (F1-F4, F5, F6, F6-D, R2-RT, S1, S2, S3, L1)
  - VS2b: 6 dispatches (V1-V6)
  - Stage A2: 7 dispatches (A1-A7) — but A7 has 3 phases with Matt-gated execution phase
  - Total **production** dispatches = **24** (one A7 dispatch carries 3 phases)
✅ Combined DAG (VS2a L1 → VS2b kickoff → VS2b V6 → Stage A2 kickoff → A7 prep → Matt-gated A7 execution → A7 disposition → Stage A2 ship)
✅ Knight-rider autonomous L1 sequencing across all three batches
✅ Specialist L1 + gandalf L2 + jack-ryan continuous observation through Stage A2 disposition
✅ Matt-gated steps remain HELD for wind-down:
  - M1 (VS2a Drift-15 environment-pack selection)
  - M2 (engine-rebuild playtest tag firings v0.12 + v0.16)
  - A7 execution (Stage A2 Playtest Cycle 1; the playtest session itself)
✅ Forward routing: Stage A3+ pre-approval-batch decision DEFERRED to Matt at next wind-down session

Matt may request amendments:
- Per-dispatch scope adjustments
- Activation gate clarifications
- Cross-batch coordination overrides
- Pre-approval extension to Stage A3+ (would add B9 series ~4-6 wk further out)

Matt does NOT need to approve (per protocol § 4.0 autonomous-mode):
- Per-task implementation details
- L1 within-seam decisions
- L2 cross-seam routing
- gandalf disposition decisions
- knight-rider tag-firing on milestones
- Mid-flight canonical-doc amendments

---

## § 5 — Wind-down sequence (post-Stage-A2 ship)

Per protocol § 4.9:

1. **A7 prep lands** → knight-rider tag-fires `stage-a2/v0.7-playtest-cycle-1-prep-complete`
2. **Matt wind-down session opens** — Matt reviews:
   - VS2a + VS2b + Stage A2 closeout state-of-hive docs
   - Pending Matt-gated items (M1 environment-pack; M2 engine-rebuild playtest tags; A7 execution = playtest)
   - Decisions-log entries for VS2a + VS2b + Stage A2 arcs
   - Playtest rubric (gandalf-authored A7 prep)
3. **Matt** picks environment pack (M1); knight-rider activates F6-D drax integration
4. **Matt** fires engine-rebuild playtest tags (M2)
5. **Matt** plays Playtest Cycle 1 per A7 rubric — VS2a regen (season_001003) + VS2b regen (season_001005) + Stage A2 additions
6. **Matt** routes observations to gandalf
7. **Gandalf** authors A7 disposition → `stage-a2/v1.0-stage-a2-ship` (Stage A2 CLOSED)
8. **Forward decision** — Stage A3 (B9 series) pre-approval-batch decision; Matt decides extension pattern OR autonomous continuation
9. **Optional retrospective** — engine-rebuild + VS2a + VS2b + Stage A2 retrospective authored by gandalf (per protocol § 14.3 pattern from 2026-05-17 invocation)

---

## § 6 — Combined sprint inventory (consolidated view)

For one view across the whole approved sprint:

| Stage | Dispatches | Total | Ship gate |
|---|---|---|---|
| Engine-rebuild | (closed) | (closed) | `hive-rebuild/v1.0-engine-rebuild-complete` ✓ |
| VS2a | F1-F4, F5, F6, F6-D, R2-RT, S1, S2, S3, L1 | 12 | `vs2a/v1.0-vs2a-ship` |
| VS2b | V1-V6 | 6 | `vs2b/v1.0-vs2b-ship` |
| Stage A2 | A1-A7 | 7 | `stage-a2/v1.0-stage-a2-ship` |
| **TOTAL production dispatches** | | **25** | — |
| In-flight VS2a continuations | C1, C2, C3, C4 | 4 | (continue per AGENT_STATE) |
| Matt-gated wind-down items | M1, M2, A7-exec | 3 | (Matt at wind-down) |
| **GRAND TOTAL** | | **32 items** | — |

(Note: 25 production dispatches; the F4 + V3 inter-relationship counts as separate items even though F4 + V3 are sibling drax dispatches in different stages.)

**Estimated duration:** ~10-16 weeks wall from VS2a L1 to Stage A2 v1.0 ship, depending on parallel execution efficiency and Matt's wind-down session cadence.

---

## § 7 — Pattern-B status (parked; unchanged across all three batches)

Pattern-B remains PARKED at `agentic_orchestration/gandalf/open-threads/2026-05-19-pattern-b-commercial-direction-PARKED.md`. R6 (Host-Calibration) enters dispatch cycle only when Pattern-B commercial-direction resolves.

VS2a + VS2b + Stage A2 pre-approval does NOT alter Pattern-B status.

---

## § 8 — Cross-references

- Stage A2 scope-of-work: `agentic_orchestration/hive-mind/scope-of-work-stage-a2.md`
- Stage A2 coordination matrix: `agentic_orchestration/hive-mind/coordination-matrix-stage-a2.md`
- Stage A2 dispatches: `agentic_orchestration/dispatches/2026-05-19-*-stage-a2-*.md` (7 total)
- Sibling pre-approval batches:
  - `agentic_orchestration/hive-mind/vs2a-pre-approval-batch-2026-05-19.md`
  - `agentic_orchestration/hive-mind/vs2b-pre-approval-batch-2026-05-19.md`
- B-spec source: `canonical/28-engine-arpg-rebalance-design.md`
- B14.5 V1 canonical balance-loop architecture: `v1.3-b14-5-primary-loop` (2026-05-12)
- p6-forward-audit (watch-items source): `canonical/story/p6-forward-audit-2026-05-16.md`
- B13 narrow-slice: `canonical/story/dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md` § 7 + `canonical/32-progression-design.md` § 12.5 Amendment
- Roadmap: `canonical/16-project-roadmap.md` § "What comes after VS2a + VS2b"
- Operating protocol: `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9 + § 6.5
- Engineering disciplines: `reincarnated-engine/design/working-agreement/engineering-disciplines.md`
- Decisions log: `reincarnated-engine/design/decisions/decisions-log.md`
- AGENTS topology: `agentic_orchestration/AGENTS.md`
- GOVERNANCE ADRs: `agentic_orchestration/GOVERNANCE.md`

---

*Filed 2026-05-19 by knight-rider per Matt directive (pre-approval-batch extended through Stage A2 + Playtest Cycle 1). The combined 25-dispatch sprint plan awaits your eye; the wind-down session will encompass three Matt-gated steps in one sitting; the road continues toward Stage A3 when you open the next gate.*
