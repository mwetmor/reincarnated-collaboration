# Coordination Matrix — Recompose-Validation Hive (third hive)

**Author:** knight-rider, 2026-05-19
**Source:** `canonical/story/hive-mind-protocol-per-tier-recompose-validation-2026-05-19.md` § 4
**Status:** snapshot at activation; knight-rider updates continuously as phases progress

---

## § 1 — Per-phase seam assignment

| Phase | Rocket | Gamora | Star-lord | Drax | Jack-ryan | Gandalf |
|---|---|---|---|---|---|---|
| **P0** Option A floor widening | — | **OWNER** | telemetry consumer | — | smoke audit | spec input |
| **P1** Option B recompose-conditioning | — | **OWNS implementation** | telemetry consumer | — | **Gate-1 critique** | **design brief author** |
| **P2** Fresh diagnostic regen | **OWNS generation** | **OWNS convergence** | **OWNS telemetry + classification** | — | observes; spot-checks | watches; advises on substrate choice |
| **P3** Validation synthesis | reads | reads | reads | — | **Gate-2 critique** | **OWNS synthesis** |
| **P4** True season ship | **OWNS generation** | **OWNS convergence** | **OWNS telemetry + export** | **syncs loadout if needed** | observes ship-gate | watches cosmology cohesion |
| **P5** Canonical record | — | — | — | — | **OWNS decisions-log** | **OWNS canonical authorship** |

---

## § 2 — Sequencing dependencies

```
P0 (gamora, ~4h)
 └─► P0 acceptance gate (smoke A1/A2/A3 + stop-gap regen) → tag recompose-hive/v0.1
     └─► P1 design brief (gandalf, ~1-2h)
         └─► P1 Gate-1 (jack-ryan, ~1-2h)
             └─► P1 implementation (gamora, ~4-6h)
                 └─► P1 acceptance gate (smoke B1: recompose fires at modifier<0.05) → tag recompose-hive/v0.2
                     └─► P2 dispatch authoring (knight-rider, ~30min)
                         └─► P2 substrate choice (gandalf, ~30min)
                             └─► P2 regen + telemetry (rocket + star-lord + gamora, ~4-6h)
                                 └─► P2 acceptance gate (regen complete; classification reproducible) → tag recompose-hive/v0.3
                                     └─► P3 synthesis (gandalf, ~2-3h)
                                         └─► P3 Gate-2 (jack-ryan, ~1h)
                                             └─► P3 verdict (PASS/CANNOT REJECT NULL) → tag recompose-hive/v0.4
                                                 ├─► PASS → P4 (rocket + gamora + star-lord + drax, ~8-12h)
                                                 │    └─► P4 ship gate → tag recompose-hive/v1.0
                                                 │        └─► P5 (gandalf + jack-ryan + knight-rider, ~4-6h) → tag recompose-hive/v1.1
                                                 └─► CANNOT REJECT NULL → surface to Matt (wind-down trigger #3)
```

---

## § 3 — Cross-seam contract touchpoints

| Surface | Producing seam | Consuming seam(s) | MIGRATION.md required? |
|---|---|---|---|
| `MODIFIER_SEARCH_FLOOR` named constant (P0) | gamora | star-lord (telemetry filters), rocket (downstream consumers) | YES — gamora authors at P0 |
| `modifier_extreme_low` telemetry flag (P0) | gamora | star-lord (queries), gandalf (designer review surface) | YES — included in same MIGRATION.md entry |
| Recompose trigger re-condition (P1) | gamora | star-lord (recompose telemetry fire-count + delta) | YES — gamora authors at P1 (semantic shift per Discipline #12) |
| Per-class classification taxonomy (P2) | star-lord (writer) + rocket (generator) | gandalf (synthesis), jack-ryan (Gate-2) | NO — classification is downstream of telemetry, not a producer contract |
| True season export schema (P4) | star-lord | drax (loadout sync) | DEPENDS on schema changes; star-lord assesses at P4 kickoff |

---

## § 4 — Same-file conflict watch

| File | Phases touching it | Conflict risk | Mitigation |
|---|---|---|---|
| `reincarnated-engine/src/reincarnated/simulation/balance_loop.py` | P0 (gamora), P1 (gamora) | LOW — same seam, sequential | gamora ships P0 first; P1 reads P0 commit before starting |
| `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` | P0, P1 (gamora authors) | LOW — append-only | gamora appends entry per phase |
| `reincarnated-engine/design/decisions/decisions-log.md` | P0 (knight-rider files entry) + P5 (jack-ryan files entry) | LOW — append-only | knight-rider files P0 entry on landing; jack-ryan files P5 entry on completion |
| Hive log `agentic_orchestration/hive-mind/recompose-validation-log.md` | ALL phases | MEDIUM — multi-author concurrent | fetch-before-commit discipline per 2026-05-17 § 14.1.1 |

---

## § 5 — Galadriel + elrond + legolas roles

**Galadriel:** NOT in scope (no visual benchmark work this hive). Sub-agent restriction per her agent definition remains operative.

**Elrond:** NOT in scope unless P4 substrate roster requires catalogue work beyond current state. Default DEFER.

**Legolas:** NOT in scope (no research crawl this hive's mission requires). Default DEFER.

---

## § 6 — Knight-rider's continuous responsibilities

- Sequence phase transitions on acceptance-gate fulfillment
- Tag + push milestones per ADR-006 amendment authority
- Daily state-of-hive at `state-of-hive-YYYY-MM-DD-recompose-validation.md`
- Pattern-B signal triage (any signal → file in PARKED thread; do not let pull focus)
- CHANGELOG entries per Discipline #11
- Cross-seam MIGRATION.md verification at each producer-consumer handoff
- Watch for scope creep (defaults in scope-of-work § 5)

---

*Authored 2026-05-19 by knight-rider at activation. Updates continuously as phases progress.*
