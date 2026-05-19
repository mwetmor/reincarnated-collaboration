# VS2b Coordination Matrix

**Authored:** 2026-05-19 by knight-rider per Matt directive (VS2A → VS2B pre-approval extension).
**Status:** Live; updated by knight-rider as items advance.
**Purpose:** Per-item seam mapping + cross-item DAG + concurrent-edit hot-spots + tag milestone plan.
**Companion:** `scope-of-work-vs2b.md`; inherited operating protocol from `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9.

---

## § 1 — Seam × item matrix

Legend per VS2a matrix.

| Item | Rocket | Gamora | Star-lord | Drax | Elrond | Legolas | Jack-ryan | Gandalf | Galadriel |
|---|---|---|---|---|---|---|---|---|---|
| **V1** `embodiment_narrative_beat` schema | **OWNS schema + generator hook** | — | consumer (export) | consumer (loadout) | — | — | observes (D14 + P7) | spec input (`embodiment-display-loadout.md`) | — |
| **V2** LLM beat-generation orchestration | reads (call hook) | — | **OWNS LLM orchestration + cost telemetry** | consumer (loadout) | — | — | observes | spec input (beat quality rubric) | — |
| **V3** Drax loadout embodiment display | reads | — | reads (export packet contract) | **OWNS surface** | — | — | observes | spec input (full spec) | — |
| **V4** Gandalf chierit element-reconciliation | — | — | — | reads (V3 + C3 consumer) | — | reads (chierit catalogue) | — | **OWNS reconciliation** | — |
| **V5** Drax + elrond full Pimen integration | — | — | reads | **OWNS demo VFX integration** | **OWNS Pimen curation completion** | — | — | spec input (catalogue review) | optional capture |
| **V6** VS2b ship gate (regen season_001005) | reads | **OWNS sim validation** | **OWNS regen orchestration** | consumer (visual ship) | reads | — | reviews (decisions-log) | spec input (cohesion sanity-check) | optional capture |

---

## § 2 — Cross-item dependency DAG

```
VS2a L1 SHIP ──► VS2b kickoff (vs2b/v0.0-vs2a-baseline)
                              │
              ┌───────────────┼───────────────┬─────────────┐
              ▼               ▼               ▼             ▼
             V1              V4              V5         (M1+M2 HELD)
       (rocket schema)  (gandalf chierit)  (drax+elrond
                                            Pimen full)
              │                              │
              ▼                              │
             V2                              │
        (star-lord LLM call)                 │
              │                              │
              ▼                              │
             V3                              │
       (drax loadout display)                │
              │                              │
              └──────────────┬───────────────┘
                             │
                             ▼
                            V6
                       (star-lord+gamora regen)
                             │
                             ▼
                    vs2b/v1.0-vs2b-ship
```

**Critical-path item:** V1 → V2 → V3 chain (4–6 days sequential — schema field + LLM call + drax surface)

**Independent items (no upstream gating, can fire at VS2b kickoff):** V1, V4, V5

**Ship-gate item:** V6 (gated on V1–V5 + VS2a L1)

---

## § 3 — Concurrent-edit hot-spots

| File | Edit-concerned seams | Coordination |
|---|---|---|
| `PlayerClass` schema (skill JSON / class manifest) | rocket (V1 schema) + star-lord (V2 export packet) | rocket-led; MIGRATION.md authored before generator hook lands |
| `reincarnated-engine/src/reincarnated/llm/` (beat-generation call) | star-lord (V2 orchestration) | star-lord-only; rocket consults on hook integration |
| `reincarnated-engine/src/reincarnated/generation/season_orchestrator.py` | rocket (V1 generator hook) | rocket-only |
| `reincarnated-loadout/src/` (class-header component) | drax (V3 surface) | drax-only |
| chierit asset paths | drax (V3 portrait + C3 character rendering consumer) | drax-only; gandalf V4 reconciliation defines slot assignments |
| Pimen asset catalogue + integration paths | drax (V5 demo VFX) + elrond (V5 curation completion) | sequential per AGENT_STATE; coordination via hive log |

**Producing seam declares intent in hive log before edit; consumer seam reads-and-reacts.**

---

## § 4 — Cross-seam contract documents (MIGRATION.md per ADR-004)

| Item | Producing seam | Consumer seams | MIGRATION.md path |
|---|---|---|---|
| V1 `embodiment_narrative_beat` schema | rocket | star-lord (V2), drax (V3) | `reincarnated-engine/src/reincarnated/generation/MIGRATION.md` (rocket appends) |
| V2 LLM beat-generation + export | star-lord | drax (V3 consumer) | `reincarnated-engine/src/reincarnated/llm/MIGRATION.md` + `export/MIGRATION.md` (star-lord appends) |
| V3 Loadout display surface | drax | (terminal consumer) | `reincarnated-loadout/MIGRATION.md` (drax appends if cross-loadout-internal contract surfaces) |
| V5 Pimen full integration | drax + elrond | (terminal consumer per VS2b ship) | `reincarnated-demo/MIGRATION.md` (drax appends if new VFX catalogue contract) |

---

## § 5 — Item activation gates

| Item | Activation gate | Status (2026-05-19 ~12:45Z) |
|---|---|---|
| V1 schema | VS2a L1 ships → VS2b kickoff | ⏸ QUEUED (post-VS2a) |
| V2 LLM call | V1 lands | ⏸ QUEUED |
| V3 loadout display | V1 + V2 + V4 land | ⏸ QUEUED |
| V4 chierit reconciliation | VS2a L1 ships → VS2b kickoff | ⏸ QUEUED (post-VS2a; fires immediately at kickoff) |
| V5 Pimen full integration | extends C2 + C4; can begin at VS2b kickoff in parallel | ⏸ QUEUED (~at VS2a L1 timeframe) |
| V6 ship gate | V1–V5 + VS2a L1 + VS2a validated | ⏸ FAR-QUEUED |

---

## § 6 — Tag milestone plan

Per protocol § 4.3 tag namespace: `vs2b/v0.<N>-<milestone>` (distinct from `vs2a/v0.<N>`).

| Tag | Trigger |
|---|---|
| `vs2b/v0.0-vs2a-baseline` | At VS2b kickoff (fires when VS2a L1 ships) |
| `vs2b/v0.1-embodiment-narrative-beat-schema` | V1 lands |
| `vs2b/v0.2-llm-beat-generation-operational` | V2 lands |
| `vs2b/v0.3-loadout-embodiment-display-shipped` | V3 lands |
| `vs2b/v0.4-chierit-element-reconciliation` | V4 lands |
| `vs2b/v0.5-pimen-full-integration` | V5 lands |
| `vs2b/v1.0-vs2b-ship` | V6 regen ships; VS2b CLOSED |

Notional `vs2b/v1.1-vs2b-validated` fires when post-VS2b playtest captures land.

---

## § 7 — Push authority (continues from VS2a)

Per launch dispatch § 6.6 + protocol § 4.0 autonomous-operation extension to ADR-006 amendment (continues unchanged):

**Knight-rider has commit + push authority upon major milestone achievement and hypothesis-test passage** without per-action authorization.

Hard constraints retained: no `--force` push; no hook bypass; explicit refspec; push to `main` only; summary generated from live git state (Discipline #11); no destructive operations without separate authorization.

---

## § 8 — Forward-looking risks + watchpoints

| Risk | Severity | Mitigation |
|---|---|---|
| `embodiment_narrative_beat` LLM quality regresses (cohesion gap) | 🟡 MEDIUM | gandalf beat-quality rubric per spec § 15 "For gandalf" item 2; re-prompt or accept-and-iterate |
| Drax bandwidth saturation (V3 + V5 + carryover from VS2a F4 + Track D) | 🔴 HIGH | sequence per drax AGENT_STATE; V3 + V5 may serialize rather than parallel |
| Pimen catalogue gap (some elements without coherent Pimen mapping) | 🟡 MEDIUM | elrond C4 curation surfaces gap; drax V5 falls back to placeholder; surface to gandalf if cross-cutting |
| chierit element gap (some elements without chierit character) | 🟡 MEDIUM | V4 reconciliation establishes physical/hybrid fallback per spec § 13 |
| VS2a slip cascades into VS2b timeline | 🟡 MEDIUM | V1 + V4 + V5 can begin at VS2b kickoff; only V6 ship gate requires VS2a L1 |
| Substrate-identity surface regression | 🟢 LOW | already empirically validated 2026-05-16 via Stage 3 cipher migration 22-test no-leak guard |
| Matt returns mid-VS2b with redirection | 🟢 LOW | wind-down trigger; pause; respect |

---

## § 9 — Cross-references

- VS2b scope-of-work: `scope-of-work-vs2b.md` (companion artifact)
- Predecessor: `coordination-matrix-vs2a.md`
- Roadmap: `canonical/16-project-roadmap.md` § VS2b
- Embodiment-narrative spec: `canonical/story/embodiment-display-loadout.md`
- Engineering disciplines: `reincarnated-engine/design/working-agreement/engineering-disciplines.md`
- Operating protocol: `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

*Filed 2026-05-19 by knight-rider at VS2b kickoff pre-approval. The matrix maps six dispatches; the DAG names what gates what; the road continues into substrate-realignment closure.*
