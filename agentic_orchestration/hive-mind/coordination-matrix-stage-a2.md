# Stage A2 Coordination Matrix

**Authored:** 2026-05-19 by knight-rider per Matt directive (VS2A → VS2B → Stage A2 pre-approval extension).
**Status:** Live; updated by knight-rider as items advance.
**Purpose:** Per-item seam mapping + cross-item DAG + concurrent-edit hot-spots + tag milestone plan.
**Companion:** `scope-of-work-stage-a2.md`; inherited operating protocol from `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9.

---

## § 1 — Seam × item matrix

| Item | Rocket | Gamora | Star-lord | Drax | Elrond | Legolas | Jack-ryan | Gandalf | Galadriel |
|---|---|---|---|---|---|---|---|---|---|
| **A1** B7 gear-variance gate | reads (catalogue context) | **OWNER** | reads (telemetry) | — | — | — | observes | spec input | — |
| **A2** B12 full audit | **OWNS schema + slots + affixes** | consumer (sim) | reads (telemetry) | **OWNS UI** | reads | — | observes (D17) | spec input (A6 framework) | — |
| **A3** B13 post-narrow-slice | **OWNS catalogue role-tagging** | **OWNS AI + observability** | reads | consumer (telegraph UI) | — | — | observes (D13) | spec input (A6 framework — telegraph-art) | — |
| **A4** B14 multi-band convergence | reads (catalogue context) | **OWNER** | reads (telemetry) | — | — | — | reviews math | — | — |
| **A5** B16 loot drop architecture | **OWNS drop rules** | reads (sim consumer if balance impl.) | reads (telemetry) | **OWNS visual presentation** | — | — | observes | spec input (A6 framework — loot visual) | — |
| **A6** Design watch-items framework | reads | reads | — | reads (A2 + A3 + A5 consumer) | — | — | — | **OWNER** | — |
| **A7** Playtest Cycle 1 | reads | reads | reads | reads | reads | — | reviews (decisions-log) | **OWNS rubric + framework + disposition** | optional capture |

---

## § 2 — Cross-item dependency DAG

```
VS2b ship ──► Stage A2 kickoff (stage-a2/v0.0-vs2b-baseline)
                              │
              ┌───────────────┼───────────────┬──────────────┐
              ▼               ▼               ▼              ▼
             A1              A6              A4         (M1+M2 HELD)
       (gamora B7)       (gandalf design   (gamora
                          framework)        B14)
                              │
              ┌───────────────┼────────────────┐
              ▼               ▼                ▼
             A2              A3               A5
       (rocket+gamora+   (rocket+gamora;  (rocket+drax;
        drax B12)         B13 narrow-slice  B16 loot)
                          remaining)
              │               │                │
              └───────────────┼────────────────┘
                              │
                              ▼
                            A7 prep
                       (gandalf rubric)
                              │
                              ▼
                    (Matt: A7 execution)
                              │
                              ▼
                            A7 disposition
                       (gandalf report)
                              │
                              ▼
                    stage-a2/v1.0-stage-a2-ship
```

**Critical-path:** A6 (gandalf framework) gates A2 + A3 + A5 visual/UX axes; A1 + A4 + A6 are first-fire (parallel)
**Convergence:** A7 prep gated on A1-A6 all landing
**Matt-gated step:** A7 execution (playtest session)

---

## § 3 — Concurrent-edit hot-spots

| File | Edit-concerned seams | Coordination |
|---|---|---|
| Gear JSON schema (boots/gloves/belt + +% MS affixes) | rocket (A2 schema) + gamora (A2 sim consumer) + drax (A2 UI) | rocket-led; MIGRATION.md before B12 ship |
| Skill JSON schema (mobility geometries; role-tagging) | rocket (A3 catalogue) + gamora (A3 AI consumer) | rocket-led; sequential with A2 to avoid concurrent schema-edit |
| `balance_loop.py` (B14 multi-band convergence) | gamora (A4) | gamora-only; extends B14.5 V1 architecture |
| `fight_engine.py` / AI behaviors (B13 escape AI) | gamora (A3 AI) | gamora-led |
| Loot drop rules + drop telemetry | rocket (A5) + star-lord (telemetry consumer) | rocket-led |
| `reincarnated-demo/src/ui/` (B12 + B16 visual surfaces) | drax (A2 + A5 UI) | drax sequential per AGENT_STATE |
| `reincarnated-demo/src/world/` (B13 telegraph-art) | drax (A3 telegraph) | drax-only |

---

## § 4 — Cross-seam contract documents (MIGRATION.md)

| Item | Producing seam | Consumer seams | MIGRATION.md path |
|---|---|---|---|
| A1 B7 telemetry | gamora | star-lord (if telemetry extends) | `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` |
| A2 B12 gear schema | rocket | gamora, drax, star-lord | `reincarnated-engine/src/reincarnated/generation/MIGRATION.md` |
| A3 B13 skill schema (mobility role-tagging) | rocket | gamora, drax | `reincarnated-engine/src/reincarnated/generation/MIGRATION.md` |
| A4 B14 telemetry | gamora | star-lord (if telemetry extends) | `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` |
| A5 B16 drop rules + telemetry | rocket | star-lord (telemetry), drax (visual) | `reincarnated-engine/src/reincarnated/generation/MIGRATION.md` + `reincarnated-demo/MIGRATION.md` (drax appends) |
| A6 (design framework; no contract change) | gandalf | (consumer dispatches consume framework) | N/A — canonical-story doc |
| A7 (playtest cycle; no contract change) | gandalf | (Matt + retrospective dispositions) | N/A |

---

## § 5 — Item activation gates

| Item | Activation gate | Status |
|---|---|---|
| A1 B7 | Stage A2 kickoff (VS2b ships) | ⏸ QUEUED |
| A2 B12 | Stage A2 kickoff + A6 framework lands | ⏸ QUEUED |
| A3 B13 | Stage A2 kickoff + A6 framework lands | ⏸ QUEUED |
| A4 B14 | Stage A2 kickoff | ⏸ QUEUED |
| A5 B16 | Stage A2 kickoff + A6 framework lands | ⏸ QUEUED |
| A6 design watch-items framework | Stage A2 kickoff (autonomous; fires immediately) | ⏸ QUEUED (post-VS2b) |
| A7 prep | A1 + A2 + A3 + A4 + A5 + A6 land | ⏸ FAR-QUEUED |
| A7 execution (Matt-gated) | A7 prep + Matt wind-down | ⏸ MATT-GATED |
| A7 disposition | A7 execution (Matt-playtest) | ⏸ POST-MATT |

---

## § 6 — Tag milestone plan

Per protocol § 4.3 tag namespace: `stage-a2/v0.<N>-<milestone>`.

| Tag | Trigger |
|---|---|
| `stage-a2/v0.0-vs2b-baseline` | At Stage A2 kickoff (fires when VS2b V6 ships) |
| `stage-a2/v0.1-b7-gear-variance-gate` | A1 lands |
| `stage-a2/v0.2-b12-full-audit-complete` | A2 lands |
| `stage-a2/v0.3-b13-post-narrow-slice-complete` | A3 lands |
| `stage-a2/v0.4-b14-multi-band-convergence` | A4 lands |
| `stage-a2/v0.5-b16-loot-drop-architecture` | A5 lands |
| `stage-a2/v0.6-design-watch-items-framework` | A6 lands |
| `stage-a2/v0.7-playtest-cycle-1-prep-complete` | A7 prep lands |
| `stage-a2/v1.0-stage-a2-ship` | A7 disposition lands; Stage A2 CLOSED |

Notional `stage-a2/v1.1-stage-a2-validated` fires post-playtest-cycle-1 validated.

---

## § 7 — Push authority (continues from VS2a/VS2b)

Per launch dispatch § 6.6 + protocol § 4.0 (unchanged): knight-rider has commit + push authority upon major milestone achievement and hypothesis-test passage without per-action authorization. Hard constraints retained.

---

## § 8 — Forward-looking risks + watchpoints

| Risk | Severity | Mitigation |
|---|---|---|
| B13 escape AI complexity beyond narrow-slice forecast | 🟡 MEDIUM | gandalf re-disposition per dodge-plus-telegraphed-combat-l3-briefing precedent |
| B14 multi-band convergence destabilizes B14.5 V1 architecture | 🔴 HIGH (per roadmap "riskiest piece") | B14.5 V1 canonical pattern preserved; B14 EXTENDS, doesn't replace; rollback tag `v1.3-b14-5-primary-loop` available |
| B16 loot visual surfaces complexity beyond A6 framework | 🟡 MEDIUM | gandalf amends framework; drax stays within seam |
| A6 framework delay cascades into A2 + A3 + A5 | 🟡 MEDIUM | A6 is ~1 day gandalf; fires at Stage A2 kickoff alongside A1 + A4 |
| Playtest Cycle 1 reveals regression in VS2a/VS2b ships | 🟢 LOW | gandalf re-disposition routes to Matt at wind-down |
| Drax bandwidth saturation (A2 UI + A3 telegraph + A5 visual + carryover from VS2a/VS2b) | 🔴 HIGH | sequence per drax AGENT_STATE; may serialize rather than parallel |
| Matt returns mid-Stage-A2 with redirection | 🟢 LOW | wind-down trigger; pause; respect |

---

## § 9 — Cross-references

- Stage A2 scope-of-work: `scope-of-work-stage-a2.md`
- VS2a + VS2b predecessors: `scope-of-work-vs2a.md` + `scope-of-work-vs2b.md`
- B-spec source: `canonical/28-engine-arpg-rebalance-design.md`
- B14.5 V1 canonical balance-loop architecture: `v1.3-b14-5-primary-loop` (2026-05-12)
- p6-forward-audit: `canonical/story/p6-forward-audit-2026-05-16.md`
- B13 narrow-slice: `canonical/story/dodge-plus-telegraphed-combat-l3-briefing-2026-05-17.md`
- Roadmap: `canonical/16-project-roadmap.md` § "What comes after VS2a + VS2b"
- Engineering disciplines: `reincarnated-engine/design/working-agreement/engineering-disciplines.md`
- Operating protocol: `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

*Filed 2026-05-19 by knight-rider at Stage A2 kickoff pre-approval. The matrix maps seven dispatches; the DAG names the gates; the playtest cycle closes the engine's arc.*
