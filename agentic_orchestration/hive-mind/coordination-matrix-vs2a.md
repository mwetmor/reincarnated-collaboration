# VS2a Coordination Matrix

**Authored:** 2026-05-19 by knight-rider at VS2a kickoff (continuation per dispatch § 6.5).
**Status:** Live; updated by knight-rider as items advance.
**Purpose:** Per-item seam mapping + cross-item DAG + concurrent-edit hot-spots + tag milestone plan.
**Companion:** `scope-of-work-vs2a.md` (item definitions); inherited operating protocol from `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` (autonomous mode + § 4.0 + § 4.9).

---

## § 1 — Seam × item matrix

Legend: **OWNER** (executes work); **OWNS X** (owns specific facet); consumer (reads contract, must adapt code); reads (needs awareness); observes (jack-ryan watches); spec input (gandalf provides design spec); commission (knight-rider commissions; legolas executes).

| Item | Rocket | Gamora | Star-lord | Drax | Elrond | Legolas | Jack-ryan | Gandalf | Galadriel |
|---|---|---|---|---|---|---|---|---|---|
| **F1** geometry_type schema | **OWNS schema + catalogue** | consumer (R2 re-test) | **OWNS telemetry/export adaptation** | consumer (B11) | reads | — | observes (D13 + P7) | reads (post-R2 H1 disposition § 5.2) | — |
| **F2** kit-redesign approach decision | reads | reads | — | — | reads | — | reads | **OWNS decision** | — |
| **F3** Drift-14 + Drift-15 framework | reads | — | — | reads (Drift-15) | reads (Drift-14 pool) | reads (commission) | — | **OWNS framework** | — |
| **F4** B6 skill-tree UI decomposition | reads (B6 main) | reads | — | **OWNS design dispatch** | — | — | observes | spec input (telegraph art, naming) | — |
| **F5** Drift-14 audit | reads (pool cull) | — | — | reads | reads (pool data) | **OWNER** (Mode B) | — | spec input (criteria) | — |
| **F6** Drift-15 sweep Track A | — | — | — | reads (Track D) | — | **OWNER** (Mode B) | — | spec input (framework) | — |
| **S1** kit-redesign sprint | **OWNS catalogue redesign** | consumer (R1 re-run) | reads (telemetry) | — | reads | — | observes (D1, P7, D17) | **OWNS design criteria** | — |
| **S2** B6 main work | **OWNS pre-work** | **OWNS main work** | reads (telemetry for convergence) | consumer (skill-tree UI) | reads | — | observes | spec input | — |
| **S3** Gate-3b sim MS | reads (schema-default) | **OWNER** | OWNS export-DTO fix | consumer | — | — | observes | — | — |
| **C1** Movement-speed baseline | OWNS schema-default | OWNS sim consumption | OWNS export-DTO emission | OWNS demo MS impl | — | — | observes (Gate 3b) | — | — |
| **C2** B11 GREEN-list VFX | reads | — | reads | **OWNS demo VFX integration** | **OWNS Pimen curation** | — | — | spec input (catalogue) | optional capture |
| **C3** chierit character rendering | reads | — | — | **OWNER** | — | — | — | spec input (per-archetype mapping decision pending) | — |
| **C4** Pimen curation | reads | — | — | consumer | **OWNER** | — | — | spec input | — |
| **L1** Demo regen on single season | reads | OWNS sim validation | **OWNS regen orchestration** | consumer (visual ship) | reads | — | reviews (decisions-log entry) | spec input (cohesion check) | optional capture (ship pre-screen) |
| **M1** Drift-15 Matt-selection (HELD) | — | — | — | reads (Track D follow-on) | — | reads (presents Track A output) | — | spec input (presentation framework) | — |
| **M2** Engine-rebuild playtest tags (HELD) | — | — | — | reads | — | — | — | — | — |

---

## § 2 — Cross-item dependency DAG

```
ENGINE-REBUILD CLOSED (v1.0) ──► VS2a kickoff
                                  │
              ┌───────────────────┼───────────────────┬────────────────────┐
              │                   │                   │                    │
              ▼                   ▼                   ▼                    ▼
        F1 (rocket+SL)      F2 (gandalf)         F3 (gandalf)          F4 (drax)
        geometry_type       kit-redesign         Drift-14+15            B6 UI design
        schema field        approach             framework
              │                   │                   │
              │                   └─────┐             │
              │                         │             │
              │                         ▼             ▼
              │                    S1 (rocket+   F5+F6 (legolas)
              │                    gandalf)      Drift-14+15
              │                    kit-redesign  Mode B crawls
              │                    sprint
              │                         │
              │                         ▼
              │                    S2 (rocket+gamora)
              │                    B6 main work
              │                         │
              └─────────────────────────┤
                                        │
                                        ▼
                            S3 (gamora) + L1 (star-lord+gamora)
                            Gate-3b sim MS    VS2a SHIP GATE
                                        │
                                        ▼
                            (Matt-gated step: M1 Drift-15 Matt-selection;
                             notional v1.0-vs2a-ship can fire without M1)

C1, C2, C3, C4 in-flight throughout — independent timelines

At Matt wind-down:
  M1 + M2 fire → VS2b begins
```

**Critical-path item:** S1 (kit-redesign sprint) — gates S2 (B6 main work); both downstream of F2 + F1.

**Independent items (no upstream gating, can fire immediately):** F1, F2, F3, F4 (first-fire batch).

**Legolas commissions (F5, F6):** gated on F3 only.

**In-flight items (C1-C4):** continue per AGENT_STATE; do not require knight-rider dispatch to proceed.

---

## § 3 — Concurrent-edit hot-spots

Per protocol § 4.4 (inherited). Likely multi-seam edit-concerned files during VS2a:

| File | Edit-concerned seams | Coordination |
|---|---|---|
| Skill JSON schema (across `output/<season>/*/skills/*.json`) | rocket (F1 schema; S1 kit-redesign) + elrond (F1 backfill) + star-lord (F1 telemetry/export) | rocket-led; MIGRATION.md authored before catalogue regen |
| Monster JSON schema (per-archetype mapping changes) | rocket (S1 catalogue) + gandalf (S1 design consult) | rocket-led; gandalf review at criteria authorship |
| `reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/*` | gamora (R2 re-test under explicit geometry_type) | gamora-only; no conflict expected |
| `reincarnated-engine/src/reincarnated/simulation/balance_loop.py` | gamora (S2 B6 main + S3 sim MS) | gamora sequential per work item |
| `reincarnated-demo/src/world/movement.ts` + `src/world/aggro.ts` | drax (C1 MS impl + C3 character rendering) | sequential per drax AGENT_STATE |
| `reincarnated-demo/src/world/skill-tree-ui.tsx` (or equivalent, post-F4) | drax (F4 design + S2 main wiring) | drax-only; F4 design first |
| LLM call topology (`canonical/19-llm-call-map.md`) | gandalf (F2 if R8-inversion path) + rocket (S1 regen orchestration if applicable) | gandalf-led; rocket adapts at S1 |

**Producing seam declares intent in hive log before edit; consumer seam reads-and-reacts.** Knight-rider mediates if conflict surfaces.

---

## § 4 — Cross-seam contract documents (MIGRATION.md per ADR-004)

| Item | Producing seam | Consumer seams | MIGRATION.md path |
|---|---|---|---|
| F1 geometry_type schema | rocket | star-lord (telemetry/export), elrond (backfill), gamora (R2 re-test consumer) | `reincarnated-engine/src/reincarnated/generation/MIGRATION.md` (rocket appends) |
| S1 kit-redesign (catalogue regen) | rocket | gamora (R1 re-run consumer), star-lord (telemetry continuity) | `reincarnated-engine/src/reincarnated/generation/MIGRATION.md` (rocket appends per F2 path) |
| S2 B6 main (skill-tree data structure) | rocket + gamora (joint) | drax (F4 UI consumer) | `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` + `reincarnated-demo/MIGRATION.md` (drax appends) |
| S3 Gate-3b sim MS | gamora | none (terminal consumer) | `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` if telemetry changes |
| C1 MS engine-emitted JSON | rocket + star-lord (joint) | drax, gamora | `reincarnated-engine/src/reincarnated/export/MIGRATION.md` (star-lord appends) |

---

## § 5 — Item activation gates

| Item | Activation gate | Status (2026-05-19 ~07:05Z) |
|---|---|---|
| F1 geometry_type schema | none — fires immediately | 🚀 READY — dispatch authoring pending |
| F2 kit-redesign approach decision | none — gandalf decides under L2-equivalent | 🚀 READY — dispatch authoring pending |
| F3 Drift-14 + Drift-15 framework | none — gandalf decides | 🚀 READY — dispatch authoring pending |
| F4 B6 skill-tree UI decomposition | none — drax authors | 🚀 READY — dispatch authoring pending |
| F5 Drift-14 audit | F3 lands | ⏸ QUEUED |
| F6 Drift-15 sweep Track A | F3 lands | ⏸ QUEUED |
| S1 kit-redesign sprint | F2 + F1 land | ⏸ QUEUED |
| S2 B6 main work | rocket pre-work + F2 decision | ⏸ QUEUED |
| S3 Gate-3b sim MS | rocket schema-default + star-lord export-DTO | ⏸ QUEUED on C1 sub-tasks |
| C1 Movement-speed baseline | in-flight | 🟢 IN-FLIGHT |
| C2 B11 GREEN-list VFX | in-flight | 🟢 IN-FLIGHT |
| C3 chierit character rendering | in-flight (gandalf per-archetype decision pending; not blocking initial render) | 🟢 IN-FLIGHT |
| C4 Pimen curation | in-flight | 🟢 IN-FLIGHT |
| L1 Demo regen on single season | all above + post-pool-cull state | ⏸ FAR-QUEUED |
| M1 Drift-15 Matt-selection | F6 Track A complete + Matt wind-down | ⏸ MATT-GATED |
| M2 Engine-rebuild playtest tags | Matt wind-down | ⏸ MATT-GATED |

---

## § 6 — Tag milestone plan

Per protocol § 4.3 tag namespace: `vs2a/v0.<N>-<milestone>` (distinct from `hive-rebuild/v0.<N>` for engine-rebuild batch).

| Tag | Trigger |
|---|---|
| `vs2a/v0.0-engine-rebuild-baseline` | At VS2a kickoff (this commit) |
| `vs2a/v0.1-geometry-type-schema-shipped` | F1 lands |
| `vs2a/v0.2-r2-h1-revalidated` | R2 re-test passes under explicit field |
| `vs2a/v0.3-drift14-framework-decided` | F3 Drift-14 framework lands |
| `vs2a/v0.4-drift15-framework-decided` | F3 Drift-15 framework lands |
| `vs2a/v0.5-kit-redesign-approach-decided` | F2 decision lands |
| `vs2a/v0.6-b6-skilltree-ui-decomposition` | F4 drax dispatch lands |
| `vs2a/v0.7-kit-redesign-sprint-complete` | S1 ships |
| `vs2a/v0.8-b6-main-work-complete` | S2 ships |
| `vs2a/v0.9-sim-ms-gate3b-complete` | S3 ships |
| `vs2a/v0.10-drift14-audit-complete` | F5 ships |
| `vs2a/v0.11-drift15-track-a-complete` | F6 Track A ships |
| `vs2a/v0.12-b11-vfx-coverage-complete` | C2 ships 11/13 elements |
| `vs2a/v0.13-chierit-rendering-complete` | C3 ships |
| `vs2a/v0.14-pimen-curation-complete` | C4 ships |
| `vs2a/v1.0-vs2a-ship` | L1 demo regen ships; VS2a CLOSED |
| `vs2a/v0.15-drift15-matt-selected` (Matt-gated) | M1 |
| `vs2a/v0.16-drift15-drax-integration-complete` (post-Matt) | follow-on to M1 |

Notional `vs2a/v1.1-vs2a-validated` fires when post-VS2a playtest captures land.

Engine-rebuild carryover tags (held for Matt wind-down):
- `hive-rebuild/v0.12-r5-hypothesis-test-passed`
- `hive-rebuild/v0.16-r4-hypothesis-test-passed`
- `hive-rebuild/v1.1-engine-rebuild-final` (notional)

Specialist seams may tag intermediate `<seam>/<vs2a-item>-<sub-step>-<n>` tags (per existing convention; no Matt approval).

---

## § 7 — Push authority (continues from engine-rebuild)

Per launch dispatch § 6.6 + protocol § 4.0 autonomous-operation extension to ADR-006 amendment (continues unchanged):

**Knight-rider has commit + push authority upon major milestone achievement and hypothesis-test passage** without per-action authorization.

**Hard constraints retained:**
- No `--force` push
- No hook bypass (`--no-verify`, `--no-gpg-sign`)
- Explicit refspec
- Push to `main` only
- Summary generated from live git state (Discipline #11)
- No deletion / destructive operations without separate explicit authorization

Per-milestone push pattern unchanged (4 steps; documented in engine-rebuild coordination-matrix § 7).

---

## § 8 — Forward-looking risks + watchpoints

| Risk | Severity | Mitigation |
|---|---|---|
| F2 decision deferred → S1 + S2 stall | 🔴 HIGH | Knight-rider fires F2 dispatch as first-batch HIGH-priority; gandalf decides within 1 day |
| S1 R8-inversion path produces incoherent kits | 🟡 MEDIUM | gandalf cohesion-judging protocol re-applied; R8 disposition pattern (commit-what's-proven; defer-what-isn't) inherits |
| Drax bandwidth saturation (F4 + C1 + C2 + C3) | 🔴 HIGH | F4 design dispatch is small (1-2 days); C1 + C2 + C3 in-flight; sequenced per drax AGENT_STATE |
| Drift-14 audit surfaces additional VS2a-blocking work | 🟡 MEDIUM | gandalf authors disposition if surfaces; routes per protocol § 4 |
| Movement-speed baseline implementation slips → S3 + L1 stall | 🟡 MEDIUM | C1 status visible per AGENT_STATE; knight-rider tracks via state-of-hive cadence |
| R2 re-test (post-F1) still fails H1 | 🟢 LOW | per R2 H1 disposition § 3.2: gandalf re-disposition if needed; deeper finding worth surfacing |
| chierit per-archetype decision blocks render polish | 🟢 LOW | C3 ships initial render without decision; polish lands when decision arrives |
| Matt returns mid-VS2a with redirection | 🟢 LOW | wind-down trigger; pause; respect |

---

## § 9 — Cross-references

- VS2a scope-of-work: `scope-of-work-vs2a.md` (companion artifact)
- Predecessor: `coordination-matrix-engine-rebuild.md`
- v1.0 disposition (engine-rebuild closure): `canonical/story/v1.0-engine-rebuild-complete-disposition-2026-05-19.md`
- R2 H1 disposition: `canonical/story/r2-h1-disposition-2026-05-19.md`
- R1 kit-redesign queue: `canonical/story/r1-kit-redesign-queue-2026-05-19.md`
- R8 disposition: `canonical/story/r8-disposition-2026-05-19.md`
- Roadmap: `canonical/16-project-roadmap.md`
- Engineering disciplines: `reincarnated-engine/design/working-agreement/engineering-disciplines.md`
- Operating protocol (inherited): `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

*Filed 2026-05-19 by knight-rider at VS2a kickoff. The matrix maps the next batch. The DAG names what gates what. The road continues.*
