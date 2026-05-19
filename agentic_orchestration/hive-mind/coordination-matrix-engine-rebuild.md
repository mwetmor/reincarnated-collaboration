# Engine-Rebuild Coordination Matrix

**Authored:** 2026-05-19 by knight-rider at engine-rebuild hive activation.
**Status:** Live; updated by knight-rider as workstreams advance.
**Purpose:** Per-workstream seam mapping + cross-workstream dependency DAG + concurrent-edit hot-spots.
**Companion:** `scope-of-work-engine-rebuild.md` (workstream definitions); `engine-rebuild-log.md` (hive log); `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 3.

---

## § 1 — Seam × workstream matrix

Legend: **OWNER** (executes work); **OWNS X** (owns specific facet); consumer (reads contract, must adapt code); reads (needs awareness); observes (jack-ryan watches); reviews (jack-ryan or gandalf actively reviews); spec input (gandalf provides design spec).

| Workstream | Rocket | Gamora | Star-lord | Drax | Elrond | Jack-ryan | Gandalf | Galadriel |
|---|---|---|---|---|---|---|---|---|
| **R1 — Per-tier balance targets** | reads | **OWNER** | reads (telemetry) | — | — | observes (math-first; P7) | spec input (per-tier targets confirmed) | — |
| **R2 — 2D spatial sub-gauntlet** | reads | **OWNS combat model** | **OWNS telemetry emission** | — | — | reviews math (Discipline #1) | spec input (scenario design consult) | optional capture if scenarios visualized |
| **R3 — Per-skill range + AI schema** | **OWNS schema + catalogue** | consumer | **OWNS export + telemetry** | consumer | **OWNS backfill tooling** | observes (Discipline #13 drift) | spec input | — |
| **R4 — Demo collision + leash + range** | — | — | — | **OWNER** | — | observes | spec input if visual register at stake | optional capture for validation |
| **R5 — Demo AI parity audit** | — | — | — | **OWNER** | — | observes | — | optional capture for validation |
| **R7 — AI catalogue source of truth** | **OWNS schema + sim consumption** | consumer | **OWNS catalogue + parity-test infrastructure** | consumer | reads | reviews coherence (P7 watch) | — | — |
| **R8 — Season-as-emergent-output** | **OWNS generation pipeline + CLI flags** | reads | **OWNS LLM orchestration + cost telemetry** | reads (cosmology consumers if any) | reads | reviews methodology | **OWNS theme-coalescence prompt + cohesion judging + final disposition** | — |

---

## § 2 — Cross-workstream dependency DAG

```
R1 (gamora) ──────────────────────────────────────────► ship
R8 (rocket+star-lord+gandalf) ────────────────────────► ship (gandalf disposition)

R3 (rocket+star-lord+elrond) ──┬─► R7 (rocket+star-lord) ──► ship
                                ├─► R5 (drax) ──► ship
                                ├─► R2 (gamora+star-lord) ──► ship
                                └─► R4 (drax) ──► ship
```

**Critical-path workstream:** R3. Foundation for R2/R4/R5/R7. Slip in R3 slips four downstream.

**Independent workstreams (no upstream gating):** R1, R8.

**R7 parity-test infrastructure** is partial-parallel with R3 schema work (shares schema; star-lord builds the test scaffolding while rocket authors the schema).

---

## § 3 — Concurrent-edit hot-spots (per protocol § 4.4 inheritance)

Per protocol § 4.4 (inherited from 2026-05-17 § 6.3 same-file-conflict protocol). The following files are likely to have multi-seam edit concern during the rebuild:

| File | Edit-concerned seams | Coordination |
|---|---|---|
| `reincarnated-engine/src/reincarnated/simulation/balance_loop.py` | gamora (R1 per-tier convergence) + future R3 consumer (range checks in sim) | gamora first; R3 consumer follows after R3 schema ships |
| `reincarnated-engine/src/reincarnated/simulation/fight_engine.py` | gamora (R1 + future R2 spatial sub-gauntlet) + rocket (R3 schema consumer) | sequential per workstream cadence |
| Monster JSON schema (across `output/<season>/monsters/*.json`) | rocket (R3 author) + elrond (R3 backfill) + star-lord (R3 telemetry + R7 catalogue) | MIGRATION.md authored by rocket; elrond + star-lord read concurrently |
| `reincarnated-demo/src/world/movement.ts` + `src/world/aggro.ts` | drax (R4 collision/leash + R5 parity) | sequential R5 → R4 per protocol § 5.5–§ 5.7 activation gates |
| `reincarnated-engine/src/reincarnated/llm/*` (R8 modifications) | rocket (R8 pipeline) + star-lord (R8 LLM call orchestration) | concurrent within R8; coordinate via MIGRATION.md |
| `reincarnated-engine/cli.py` | rocket (R8 CLI flag surface: `--theme-input`, `--no-coalesce`) | rocket-only within R8 |

**Producing seam declares intent in hive log before edit; consumer seam reads-and-reacts.** If genuine conflict, knight-rider mediates.

---

## § 4 — Cross-seam contract documents (MIGRATION.md per ADR-004)

| Workstream | Producing seam | Consumer seams | MIGRATION.md path |
|---|---|---|---|
| R3 (schema migration) | rocket | star-lord (telemetry), elrond (backfill), gamora (sim consumer), drax (demo R4 + R5 consumer) | `reincarnated-engine/src/reincarnated/generation/MIGRATION.md` (rocket authors concurrently) |
| R7 (catalogue source of truth) | rocket + star-lord (joint) | gamora (sim AI consumer), drax (demo AI consumer) | shared MIGRATION.md with R3 (single coherent migration) |
| R8 (CLI flag surface + theme-coalescence) | rocket + star-lord (joint) | gandalf (theme prompt design); future tooling consumers | `reincarnated-engine/src/reincarnated/generation/MIGRATION.md` + `src/reincarnated/llm/MIGRATION.md` (rocket + star-lord author concurrently) |
| R1 (per-tier convergence) | gamora | star-lord (telemetry per-tier field) | `reincarnated-engine/src/reincarnated/simulation/MIGRATION.md` (gamora authors if telemetry surface changes) |

---

## § 5 — Workstream activation gates (per protocol § 5)

| Workstream | Activation gate | Status (2026-05-19 04:26Z) |
|---|---|---|
| R1 | gamora reads protocol + solutions doc § 2; per-tier targets confirmed (gandalf, pre-confirmed) | ✅ READY — dispatch fired |
| R3 | rocket + star-lord + elrond read protocol + solutions doc § 4; schema draft authored by rocket; backfill strategy decided | ✅ READY — dispatch fired |
| R7 | rocket + star-lord read protocol + solutions doc § 7; Option A pre-confirmed (gandalf); parity-test infrastructure design | ✅ READY — dispatch fired |
| R8 | rocket + star-lord + gandalf read protocol + solutions doc § 8; CLI flag design + theme-coalescence prompt + cohesion-judging + 3+3 A/B run protocol | ✅ READY — dispatch fired (gandalf drafts prompt + protocol as in-dispatch work) |
| R5 | R3 schema migration shipped (at least AI behavior fields); drax reads solutions doc § 6 | ⏸ QUEUED (gated on R3 partial) |
| R2 | R3 shipped (per-skill range data); sub-gauntlet scenario design (3–5 per class); gamora + star-lord read solutions doc § 3 | ⏸ QUEUED (gated on R3) |
| R4 | R3 shipped (per-skill range + aggro/leash); soft-vs-hard collision decision; drax reads solutions doc § 5 | ⏸ QUEUED (gated on R3) |

---

## § 6 — Tag milestone plan

Per protocol § 4.3 (inherited 2026-05-17 § 5.2) tag namespace: `hive-rebuild/v0.<N>-<milestone>` (distinct from `hive/v0.<N>` for Phase-1 P1).

| Tag | Trigger |
|---|---|
| `hive-rebuild/v0.0-pre-engine-rebuild` | ✅ Activation baseline (2026-05-19) — all 4 repos |
| `hive-rebuild/v0.1-r1-baseline-measurement-captured` | gamora ships baseline WR-distribution measurement before R1 implementation |
| `hive-rebuild/v0.2-r1-per-tier-convergence-operational` | gamora ships R1 modified balance loop |
| `hive-rebuild/v0.3-r1-hypothesis-test-passed` | R1 Test 2 passes (post-retune pass-rate ≥ 70%) |
| `hive-rebuild/v0.4-r3-schema-draft-committed` | rocket commits schema draft (MIGRATION.md authored) |
| `hive-rebuild/v0.5-r3-backfill-complete` | elrond completes 5-shipped-season backfill |
| `hive-rebuild/v0.6-r3-hypothesis-test-passed` | R3 Tests 1+2+3 pass |
| `hive-rebuild/v0.7-r7-parity-test-operational` | star-lord ships parity-test infrastructure |
| `hive-rebuild/v0.8-r7-hypothesis-test-passed` | R7 Tests 1+2+3 pass |
| `hive-rebuild/v0.9-r8-prototype-operational` | rocket ships inverted-pipeline + CLI flags + star-lord LLM orchestration |
| `hive-rebuild/v0.10-r8-ab-run-complete` | 6-season A/B run shipped; cohesion + variety + cost measured |
| `hive-rebuild/v0.11-r8-disposition-decided` | gandalf authors disposition (commit/revert/partial) |
| `hive-rebuild/v0.12-r5-hypothesis-test-passed` | drax ships R5 (after R3 partial); R5 Test 2 passes |
| `hive-rebuild/v0.13-r2-sub-gauntlet-operational` | gamora + star-lord ship sub-gauntlet (after R3) |
| `hive-rebuild/v0.14-r2-hypothesis-test-passed` | R2 Tests 1+2+3 pass |
| `hive-rebuild/v0.15-r4-collision-leash-range-operational` | drax ships R4 (after R3) |
| `hive-rebuild/v0.16-r4-hypothesis-test-passed` | R4 Tests 1+2+3+4 pass |
| `hive-rebuild/v1.0-engine-rebuild-complete` | All seven workstreams' hypothesis tests pass → tag all 4 repos → continue forward to VS2a |

Specialist seams may tag intermediate `<seam>/<workstream>-<sub-step>-<n>` tags within their seam (per existing convention; no Matt approval needed for intermediate tags).

---

## § 7 — Push authority

Per launch dispatch § 6.6 + protocol § 10 commit-push extension to ADR-006 amendment:

**Knight-rider has commit + push authority upon major milestone achievement and hypothesis-test passage** without per-action authorization.

**Per-milestone push pattern:**
1. Generate push-readiness summary from live `git status` + `git log` per-repo
2. Include summary in milestone's state-of-hive entry
3. Name any Vercel deploy triggers (loadout, demo)
4. Push per explicit `git push origin <branch>` refspec (ADR-006 hard constraints)
5. Record push in hive log STATE entry

**Hard constraints retained (ADR-006 amendment):**
- No `--force` push
- No hook bypass (`--no-verify`, `--no-gpg-sign`)
- Explicit refspec
- Push to `main` only
- Summary generated from live git state (Discipline #11)
- No deletion / destructive operations without separate explicit authorization
