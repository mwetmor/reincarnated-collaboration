# VS2b Scope of Work — Substrate Realignment + Full Catalogue (continuation from VS2a closure)

**Authored:** 2026-05-19 by knight-rider per Matt directive 2026-05-19 ("approved, proceed with VS2A → VS2B").
**Authority:** Matt directive (autonomous-operation continues + pre-approval-batch mode extended to VS2b scope).
**Status:** **Pre-approved executable plan.** Specialists pick up dispatches at activation gates per coordination matrix DAG.
**Estimated duration:** ~2–4 weeks wall (per roadmap "VS2b ships within 2–4 weeks of VS2a"; most VS2b work already shipped 2026-05-16).
**Operating mode:** AUTONOMOUS per protocol § 4.0 + § 4.9 (inherited from engine-rebuild protocol into VS2a + VS2b).
**Companion artifacts:** `coordination-matrix-vs2b.md` + `vs2b-pre-approval-batch-2026-05-19.md`.
**Predecessor:** `scope-of-work-vs2a.md` (VS2a; CLOSES at L1 ship → VS2b activates).

---

## § 0 — TL;DR

VS2b's substrate-realignment foundation already shipped 2026-05-16 (Stage 1 embodiment-axis + Stage 2 cosmological-vocabulary + Stage 3 cipher migration engine + Stage 3 cipher migration drax). What remains:

1. **`embodiment_narrative_beat`** — generative schema field + LLM beat-generation call + drax loadout display surface per gandalf 2026-05-16 spec (`canonical/story/embodiment-display-loadout.md` § 15)
2. **chierit element-reconciliation** — small gandalf clarification on 10-character slot assignments + physical/hybrid fallback (~30 min)
3. **Full Pimen catalogue integration** — extends VS2a C2 (11/13 GREEN-list) to full catalogue coverage
4. **VS2b ship gate** — fresh regenerated season (regens season_001005) demonstrating cipher migration + embodiment-axis + embodiment-narrative display + Pimen full integration

**6 dispatches total** (V1–V6). Smaller than VS2a (12 dispatches) because the substrate-realignment heavy lift already shipped.

---

## § 1 — Already-shipped (reference only; no re-dispatch)

Per `canonical/16-project-roadmap.md` § VS2b + dispatch completion records:

| Item | Owner | Tag / commit | Status |
|---|---|---|---|
| S1 — embodiment-axis additive field on Loadout schema | rocket | `rocket/v1.3-form-bias-stage-1-embodiment-axis` | ✅ Shipped 2026-05-16 |
| S2 — abstract pair-structure (grouping layer) | rocket | (form-bias Stage 2 commit) | ✅ Shipped 2026-05-16 |
| Grouping-layer vocabulary v1.1 lock (gandalf spec) | gandalf | decisions-log locks 2026-05-16 | ✅ Locked |
| Form-bias Stage 1+2 fields wired into `_class_to_dict` | star-lord | (star-lord shipped) | ✅ Shipped 2026-05-16 |
| Cipher-migration paths-audit (48 sites; 26 LEAK-RISK) | star-lord | `agentic_orchestration/research/cipher-migration-paths-audit-2026-05-16.md` | ✅ Complete + R11(d) fail-loud shipped |
| Stage 2 cosmological-vocabulary (per-season vocabulary generator) | star-lord | `star-lord/v1.3-form-bias-stage-2-cosmological-vocabulary @ 5b0285b` | ✅ Shipped 2026-05-16 |
| **S3 — cipher migration (engine side)** | star-lord | `star-lord/v1.3-form-bias-stage-3-cipher-migration @ 19d8ba0` | ✅ Shipped 2026-05-16 (LLM filters + export additive fields + manifest parallel v1.5 + debug logging; 22-test no-leak guard PASSING) |
| **S3 — cipher migration (drax side)** | drax | (drax dispatch completion record 2026-05-16) | ✅ Shipped 2026-05-16 (6 LEAK-RISK sites + manifest v1.5 + fallback resolver hardening) |
| Embodiment-narrative display **loadout-side spec** | gandalf | `canonical/story/embodiment-display-loadout.md` | ✅ Authored 2026-05-16 (the design framework for V1–V3 below) |
| Cipher-migration paths-audit + R11(d) recorder fail-loud | star-lord | (commit) | ✅ Complete |

**Note:** the roadmap doc lists some of the above as "in-flight" or "dispatch not yet authored" — this is roadmap drift; the dispatch completion records are the ground truth. VS2b's structural substrate is operational. What remains is the embodiment-narrative SURFACE + Pimen FULL integration + ship-validation regen.

---

## § 2 — In-scope dispatches (V1–V6)

### § 2.1 — V1 — Rocket `embodiment_narrative_beat` schema field

- **Owner:** rocket (generation seam — schema + LLM call hook)
- **Origin:** `canonical/story/embodiment-display-loadout.md` § 15 "For rocket+star-lord" recommendation 1 + Discipline #14 (generative-side schema)
- **Deliverables:**
  - Additive `embodiment_narrative_beat` field on `PlayerClass` schema (string; ≤40 words; concrete; sensory; per spec § 1)
  - Generator hook: per-season-per-class LLM beat-generation call invocation
  - Validator: schema enforces field exists (additive nullable initially → non-null post-backfill, same two-stage pattern as F1 `geometry_type`)
  - MIGRATION.md authored at `reincarnated-engine/src/reincarnated/generation/MIGRATION.md`
- **Effort:** ~2–3 days rocket (schema + LLM call integration; spec is detailed)
- **Activation gate:** none — fires immediately under VS2b activation (VS2a L1 ship + VS2b kickoff)
- **Tag:** `vs2b/v0.1-embodiment-narrative-beat-schema`

### § 2.2 — V2 — Star-lord LLM beat-generation call orchestration

- **Owner:** star-lord (operational pipeline seam — LLM orchestration + cost telemetry)
- **Origin:** `canonical/story/embodiment-display-loadout.md` § 15 recommendation 3
- **Deliverables:**
  - LLM beat-generation call orchestrated per-season-per-class (folds into Stage 2 cosmological-vocabulary pipeline as follow-on per spec)
  - Cost telemetry per-season: incremental LLM cost captured ($ + call count)
  - Export packet emits `embodiment_narrative_beat` per class
  - MIGRATION.md appended at `reincarnated-engine/src/reincarnated/llm/MIGRATION.md` + `export/MIGRATION.md`
  - Round-trip smoke per Principle 6 (generator emits field → LLM call → export packet → loadout consumer)
- **Effort:** ~2–3 days star-lord
- **Activation gate:** V1 schema field operational (rocket adds field; star-lord orchestrates fill)
- **Tag:** `vs2b/v0.2-llm-beat-generation-operational`

### § 2.3 — V3 — Drax loadout embodiment-narrative-display surface

- **Owner:** drax (presentation seam — loadout-first surface)
- **Origin:** `canonical/story/embodiment-display-loadout.md` § 15 recommendation 1 + § 13 implementation cascade
- **Deliverables:**
  - Class-header component scaffold per spec § 4–§ 10 (portrait + spirit name + narrative beat + mobile responsive)
  - chierit portrait crop tooling (idle-frame extraction → 96×96 crop) per spec § 13 immediate
  - Beat content rendering: consumes `embodiment_narrative_beat` field from V1 + V2; canonical-four labels fully hidden per Stage 3 cipher
  - Typography exploration per HD-2D register
  - Mobile responsiveness implementation
  - AGENT_STATE.md updated
- **Effort:** ~1–1.5 weeks drax (per spec § 13 estimate — scaffolding 2-3 days + engine integration 1-2 days + polish 2 days + chierit tooling 1 day)
- **Activation gate:** V1 + V2 land (`embodiment_narrative_beat` field flowing); V4 chierit reconciliation lands (slot assignments locked)
- **Tag:** `vs2b/v0.3-loadout-embodiment-display-shipped`

### § 2.4 — V4 — Gandalf chierit element-reconciliation small dispatch

- **Owner:** gandalf (design-steward; small clarification)
- **Origin:** `canonical/story/embodiment-display-loadout.md` § 15 recommendation 4
- **Deliverables:**
  - Confirm 10-character chierit slot assignments per element
  - Physical/hybrid fallback strategy documented
  - Cross-reference to character-track ingest dispatch (in-flight per VS2a C3) — same call serves both VS2a + VS2b display surfaces per roadmap watch-items
- **Effort:** ~30 min gandalf
- **Activation gate:** none — fires immediately
- **Tag:** `vs2b/v0.4-chierit-element-reconciliation`

### § 2.5 — V5 — Drax + elrond full Pimen catalogue integration

- **Owner:** drax (demo VFX integration) + elrond (Pimen curation completion)
- **Origin:** VS2b roadmap ship trigger ("Pimen full integration") + extends VS2a C2 (11/13 GREEN-list elements) to full catalogue
- **Deliverables:**
  - All Pimen catalogue elements integrated (extends C2 11/13 to full coverage; the remaining 2 elements + non-GREEN-list extensions)
  - elrond completes Pimen curation pipeline + subset selection (extends C4)
  - Demo VFX integration end-to-end smoke
  - AGENT_STATE.md updated both seams
- **Effort:** ~1–1.5 weeks (extends C2 + C4 in-flight)
- **Activation gate:** VS2a C2 + C4 reach substantial maturity (typically L1 ship time-frame)
- **Tag:** `vs2b/v0.5-pimen-full-integration`

### § 2.6 — V6 — Star-lord + gamora VS2b ship gate (regen season_001005)

- **Owner:** star-lord (orchestration) + gamora (sim validation)
- **Origin:** `canonical/16-project-roadmap.md` § VS2b ship trigger
- **Deliverables:**
  - Fresh regen of season_001005 (per roadmap § "Regen budget" — VS2a regens season_001003; VS2b regens season_001005; preserves comparability)
  - Regenerated season demonstrates: cipher migration (LLM no longer sees canonical-four; per-season vocabulary fully drives surface) + embodiment-axis populated + embodiment-narrative display in loadout + Pimen full integration
  - Combined VS2a + VS2b playtest readiness: same player walks through both regen seasons
  - State-of-hive VS2b ship doc authored at `agentic_orchestration/hive-mind/state-of-hive-<YYYY-MM-DD>-vs2b-ship.md`
  - Decisions-log entry (jack-ryan routes) capturing VS2b arc + ship outcomes
- **Effort:** ~1 week
- **Activation gate:** all of V1, V2, V3, V4, V5 land + VS2a L1 shipped + VS2a validated
- **Tag:** `vs2b/v1.0-vs2b-ship` (VS2b CLOSED)

---

## § 3 — Matt-gated items (HELD for wind-down)

VS2b has no NEW Matt-gated items beyond what's already deferred from VS2a:

- **M1** (VS2a) — Drift-15 environment-pack Matt selection (HELD; F6-D drax integration fires post-M1)
- **M2** (engine-rebuild) — playtest tag firings (HELD)

VS2b ship (V6) does NOT require Matt-gate; ships autonomously per pre-approval.

After VS2b L1 ships → wind-down trigger remains exclusively Matt's discretion per protocol § 4.9.

---

## § 4 — Sequencing summary

```
VS2a L1 SHIP (vs2a/v1.0-vs2a-ship) → VS2b kickoff (vs2b/v0.0-vs2a-baseline)
                              │
              ┌───────────────┼──────────────┬──────────────┐
              ▼               ▼              ▼              ▼
             V1              V4             V5             (M1+M2 HELD)
        (rocket schema)  (gandalf chierit) (drax+elrond Pimen full)
              │                              │
              ▼                              │
             V2                              │
        (star-lord LLM call)                 │
              │                              │
              ▼                              │
             V3                              │
        (drax loadout display)               │
              │                              │
              └──────────────┬───────────────┘
                             │
                             ▼
                            V6
                       (star-lord+gamora regen)
                             │
                             ▼
                    vs2b/v1.0-vs2b-ship
                             │
                             ▼
                  (Stage A2 closeout → Playtest Cycle 1 → ...)
```

---

## § 5 — Roadmap continuation (post-VS2b)

Per `canonical/16-project-roadmap.md` § "What comes after VS2a + VS2b" + dispatch § 6.5 explicit ordering:

### § 5.1 — Stage A2 closeout (post-VS2b)

- Source: `canonical/16-project-roadmap.md` § Stage A2 closeout + `canonical/28-engine-arpg-rebalance-design.md` queue
- Items: B7 (gear-percentile variance gate), B12 full audit, B13 (post-narrow-slice; ~25% already shipped), B14, B16
- Timing: ~6–10 weeks after VS2a/VS2b close
- Pre-approval-batch decision deferred to VS2b completion checkpoint (knight-rider re-engages Matt or continues autonomous per his preference)

### § 5.2 — Playtest Cycle 1 (post-Stage-A2)

- Source: `canonical/16-project-roadmap.md` § Playtest Cycle 1
- Timing: ~1–2 weeks post Stage A2 closeout
- Combined VS2a + VS2b playtest

### § 5.3 — Stage A3 (B9 series)

- Source: `canonical/16-project-roadmap.md` § Stage A3 + `canonical/32-progression-design.md`
- Timing: ~4–6 weeks
- Design fully resolved 2026-05-12

### § 5.4 — Subsequent (per roadmap)

- Playtest Cycle 2 → Stage A4 → Playtest Cycle 3 → Stage A5/A6 → Stage A7 → Playtest Cycle 4 → Phase 0 ship-readiness assessment

---

## § 6 — Mission discipline

**Scope is fluid but bounded.** VS2b scope is **per roadmap doc + V1–V6 dispatches** as captured here. Scope-creep protocol:

| Pressure | Default |
|---|---|
| `embodiment_narrative_beat` LLM call quality regresses | gandalf judges per beat-quality rubric (forward-flagged spec § 15 "For gandalf" item 2); re-prompt or accept-and-iterate |
| chierit roster element gap surfaces (some elements unmapped) | V4 reconciliation handles; physical/hybrid fallback per spec |
| Pimen catalogue surfaces additional curation needs | elrond C4 in-flight; surface if blocking V5 |
| Stage A2 readiness signal during VS2b execution | DEFER; Stage A2 is post-VS2b territory |
| Pattern-B research arrives | FILE in PARKED thread; do NOT pull focus |
| Matt returns mid-VS2b with redirection | Wind-down trigger; pause; respect direction |

**Canonical-doc revisions** → gandalf authors; knight-rider broadcasts; jack-ryan reviews when affecting Disciplines or decisions-log.

---

## § 7 — Cross-references

- VS2a scope-of-work: `agentic_orchestration/hive-mind/scope-of-work-vs2a.md` (predecessor)
- VS2a pre-approval batch: `agentic_orchestration/hive-mind/vs2a-pre-approval-batch-2026-05-19.md`
- Roadmap: `canonical/16-project-roadmap.md` § VS2b
- Embodiment-narrative spec: `canonical/story/embodiment-display-loadout.md` (V1–V3 design framework)
- Embodiment-narrative layer: `canonical/story/embodiment-narrative-layer.md` (architectural framing)
- Form-bias cadence strategy: `canonical/story/form-bias-cadence-strategy.md`
- Cosmology / Court / naming triad: `canonical/story/cosmology-reincarnated.md` + `court-of-forms.md` + `naming-triad.md`
- Style register: `canonical/story/style-register.md`
- Substrate identity declarations: `canonical/story/substrate-identity-declarations-2026-05-17.md`
- Cipher-migration paths-audit: `agentic_orchestration/research/cipher-migration-paths-audit-2026-05-16.md`
- Engineering disciplines: `reincarnated-engine/design/working-agreement/engineering-disciplines.md` (#13a/#13b/#14 form-bias)
- Decisions log: `reincarnated-engine/design/decisions/decisions-log.md`
- Operating protocol: `canonical/story/hive-mind-protocol-engine-rebuild-2026-05-19.md` § 4.0 + § 4.9

---

## § 8 — Tag milestone plan (VS2b namespace)

| Tag | Trigger |
|---|---|
| `vs2b/v0.0-vs2a-baseline` | At VS2b kickoff (fires when VS2a L1 ships) |
| `vs2b/v0.1-embodiment-narrative-beat-schema` | V1 rocket schema field lands |
| `vs2b/v0.2-llm-beat-generation-operational` | V2 star-lord orchestration lands |
| `vs2b/v0.3-loadout-embodiment-display-shipped` | V3 drax loadout surface lands |
| `vs2b/v0.4-chierit-element-reconciliation` | V4 gandalf reconciliation lands |
| `vs2b/v0.5-pimen-full-integration` | V5 drax + elrond full Pimen integration lands |
| `vs2b/v1.0-vs2b-ship` | V6 regen season_001005 ships; VS2b CLOSED |

Notional `vs2b/v1.1-vs2b-validated` fires when post-VS2b playtest captures land.

Specialist seams may tag intermediate `<seam>/<vs2b-item>-<sub-step>-<n>` per convention.

---

*Filed 2026-05-19 by knight-rider per Matt directive (VS2A → VS2B pre-approval extension). VS2b's substrate is built; the surfaces remain; the regen will land six dispatches from here.*
