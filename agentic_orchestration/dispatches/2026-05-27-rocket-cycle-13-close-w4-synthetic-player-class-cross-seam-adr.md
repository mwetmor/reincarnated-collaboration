# Dispatch — rocket — Cycle 13 Close W4 — `_SyntheticPlayerClass` Cross-Seam ADR / MIGRATION Documentation

**Date authored:** 2026-05-27
**Authored by:** knight-rider (per jack-ryan PASS-with-WARN verdict `482801c`)
**Status:** PENDING
**Cycle:** 13 (post-close non-blocking remediation)
**Scope:** W4 — rocket-side acknowledgment + documentation of gamora's Cycle 13 remediation-exception touch on `_SyntheticPlayerClass` (which lives in rocket's seam at `generation/season_generation_pipeline.py`)

---

## 0. Context

During Cycle 13 Option A remediation Track A (sim execution fix), gamora identified that one of the 3 root causes lived inside `_SyntheticPlayerClass` (a helper class for synthetic-bucket gauntlet sweeps). That class lives in:

```
reincarnated-engine/src/reincarnated/generation/season_generation_pipeline.py
```

— which is **rocket's seam** (generation/), not gamora's. Gamora modified `cast_time_seconds` (0.0 → 0.7) and `magnitude` (1500 → 3000) on `_SyntheticPlayerClass` as part of the fix. Gamora flagged this as "Authorized as Cycle 13 remediation exception" + documented in gamora `simulation/MIGRATION.md` § v1.31.

Jack-ryan Gate-2 PASS-with-WARN verdict at `agentic_orchestration/qa/findings/2026-05-27-cycle-13-close-gate-2-re-verification.md` classified this as **W4 (non-blocking)**: gamora's MIGRATION § v1.31 adequately documents the touch; the remaining work is rocket-side ADR / MIGRATION documentation acknowledging the cross-seam-write + establishing whether the class should:

- (a) **Migrate** to gamora's seam (simulation/) since it's only used by sim sweeps, OR
- (b) **Remain** in rocket's seam with a documented cross-seam-write exception (Cycle 13 remediation precedent), OR
- (c) **Be refactored** into a shared seam (if one exists or should be created)

Rocket's call on the architectural disposition. This dispatch is the ADR / MIGRATION write to document the call.

---

## 1. Required reading

1. **`agentic_orchestration/qa/findings/2026-05-27-cycle-13-close-gate-2-re-verification.md`** § W4 — jack-ryan verdict on this WARN
2. **`reincarnated-engine/src/reincarnated/simulation/MIGRATION.md`** § v1.31 — gamora's prior documentation of the cross-seam touch (what was changed + why)
3. **`reincarnated-engine/src/reincarnated/simulation/math/cycle-13-option-a-remediation-root-cause-2026-05-27.md`** § 10 — gamora's math note + code-citation context
4. **`reincarnated-engine/src/reincarnated/generation/season_generation_pipeline.py`** — locate `_SyntheticPlayerClass`; understand its scope (who calls it, what it represents)
5. **`reincarnated-engine/src/reincarnated/generation/MIGRATION.md`** — rocket-side MIGRATION; add new § for this W4 amendment
6. **`reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md`** — rocket seam state
7. **`agentic_orchestration/GOVERNANCE.md`** — ADR-004 (cross-seam handoff) + ADR-002 (tiered approval); informs the disposition call

---

## 2. Scope — sequential steps

### Step 1 — Read `_SyntheticPlayerClass` in context

Empirically inspect the class definition + all call sites:

```
grep -n "_SyntheticPlayerClass\|class _SyntheticPlayer" reincarnated-engine/src/reincarnated/generation/season_generation_pipeline.py
grep -rn "_SyntheticPlayerClass" reincarnated-engine/src/
```

Establish:
- Is `_SyntheticPlayerClass` used ONLY by simulation (e.g., gamora sweeps)? Then disposition (a) migrate to gamora's seam may be cleanest.
- Is it used by BOTH generation AND simulation? Then disposition (b) remain-with-exception OR (c) refactor-to-shared may be cleanest.
- What does the class represent (a synthetic placeholder for sim testing? a real generation artifact?)?

### Step 2 — Disposition decision

Choose disposition (a) / (b) / (c) per rocket's architectural judgment. Document rationale.

**KR recommendation (non-binding):** if `_SyntheticPlayerClass` is purely a sim-side test artifact, disposition (a) migrate is cleanest — moves the class to where it's used + removes the cross-seam-write exception entirely. If it has broader generation responsibilities, disposition (b) remain-with-exception is fine + documents the Cycle 13 precedent.

**Do NOT implement migration in this dispatch.** Only document the decision. If disposition (a) is chosen, queue a separate migration dispatch post-close (KR routes).

### Step 3 — MIGRATION.md / ADR entry

Author a new § in `reincarnated-engine/src/reincarnated/generation/MIGRATION.md`:

```markdown
## [2026-05-27] §v<X.Y>-cycle-13-w4-synthetic-player-class-cross-seam-touch-acknowledgment

**Author:** rocket (this dispatch)
**Workstream:** Cycle 13 Close W4 remediation (post-PASS-with-WARN)
**Dispatch:** `agentic_orchestration/dispatches/2026-05-27-rocket-cycle-13-close-w4-synthetic-player-class-cross-seam-adr.md`
**Authority:** jack-ryan PASS-with-WARN verdict `482801c` + Matt Option A authorization

### What happened

During Cycle 13 Option A remediation Track A, gamora modified `_SyntheticPlayerClass` in `season_generation_pipeline.py` (rocket's seam) as part of fixing the synthetic-bucket gauntlet sweep KPM mis-classification. Specifically:
- `cast_time_seconds: 0.0 → 0.7`
- `magnitude: 1500 → 3000`

Cross-referenced: gamora `simulation/MIGRATION.md` § v1.31.

### Disposition

[(a) MIGRATE / (b) REMAIN with documented exception / (c) REFACTOR to shared seam]

**Rationale:** [rocket's architectural decision]

### Cycle 13 precedent established

Per ADR-004 (cross-seam handoff): when a cross-seam-write is necessitated by remediation, the writing seam (here: gamora) documents the touch + the touched seam (here: rocket) acknowledges + adopts the disposition decision in their MIGRATION.md. This dispatch is the canonical instance of that pattern for Cycle 13.

Future cross-seam-writes follow this precedent: writer's MIGRATION § + touched-seam's MIGRATION § acknowledgment within the same close cycle.
```

If you choose to author an ADR amendment instead of (or in addition to) MIGRATION § (e.g., extending ADR-004 with a "remediation-exception cross-seam-write pattern" subsection), flag for KR to route through jack-ryan (jack-ryan owns ADRs at the GOVERNANCE.md level).

### Step 4 — AGENT_STATE.md checkpoint

Update `reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` with brief note + commit-SHA pointer.

---

## 3. Acceptance criteria

- [x] Disposition decision (a/b/c) documented with rationale
- [x] `generation/MIGRATION.md` § for W4 acknowledgment landed
- [x] Cross-reference to gamora `simulation/MIGRATION.md` § v1.31
- [x] AGENT_STATE.md commit-SHA pointer updated
- [x] If disposition (a) MIGRATE chosen: flag for KR to route migration dispatch post-close (do NOT implement migration here)

---

## 4. Out-of-scope

- **Do NOT** implement the migration (if disposition (a) chosen) — separate dispatch
- **Do NOT** modify `_SyntheticPlayerClass` itself — gamora's changes stay; this dispatch only documents
- **Do NOT** modify gamora's `simulation/MIGRATION.md` § v1.31 — cross-reference only
- **Do NOT** modify ADR-004 directly without jack-ryan routing (jack-ryan owns GOVERNANCE.md)
- **Do NOT** re-run sim suites — verification-only dispatch is documentation work

---

## 5. Completion record protocol

Append a completion record to this dispatch file with:

- **Status:** COMPLETE
- **Disposition chosen:** (a) / (b) / (c)
- **Rationale (1-2 sentences)**
- **MIGRATION.md path + § version**
- **AGENT_STATE.md updated:** yes
- **Migration dispatch needed?** (if disposition (a) — yes; flag for KR)
- **Commit SHA(s)**

KR will pick up + close W4. After all 4 WARNs (W1-W4) are remediated, KR updates the wind-down summary for Matt's ratification surface.

---

**Authority:** knight-rider per jack-ryan PASS-with-WARN verdict `482801c` + Matt Option A authorization + ratified framing brief § 4.1 autonomous scope + Matt per-cycle-push authorization.
