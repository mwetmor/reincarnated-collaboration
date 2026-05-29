# DISPATCH — Rocket Cycle 14 A2-1 Step 2 (Concern #2 — FACTION_VISIBILITY Flip "invisible" → "visible" + Assert Lift)

**Authored:** 2026-05-29 (Mode A Phase A2 cascade RESUMPTION; resolution plan § 1 Step 2)
**Author:** knight-rider (Cycle 14 Mode A hive-mind orchestrator)
**Recipient:** rocket (content generation seam; orchestrator-side owner for wave5_season_orchestrator.py per cycle convention)
**Pattern:** Pattern A-deep single-file amendment + downstream-consumer audit + completion record; ~0.5-1h wall-clock per resolution plan § 1 Step 2
**Expected effort:** ~0.5-1h (5 line-level amendments + Disc #11 downstream-consumer audit + completion record)
**Status:** PENDING — fires on receipt
**Authority:** Matt 2026-05-29 in-session Path D ratification (resolution plan § 1 Step 2) + hive-mind decision-routing (in-scope cascade-resumption work; Matt-directed direction "removal of LLM runs from v1 is off the table") + R48.4 single-seam (gamora released post Step 1 PASS; rocket firing alone)

---

## 0. CONTEXT (read first — 3 min)

### 0.1 Cascade-resumption lineage

| # | Dispatch / event | Status |
|---|---|---|
| A2-1 (RE-FIRE) | `2026-05-29-rocket-cycle-14-a2-1-refire-post-phase7-bridge-fix.md` | ❌ MATERIAL FAIL (Concern #1 KPM gap + **Concern #2** Phase 5 placeholder mode) — collab `9f9ed28` + engine `c8586e4` |
| Resolution plan ratification | Matt in-session 2026-05-29 | Path A + Path D ratified |
| A2-1 Step 1 (gamora KPM recalibration) | `2026-05-29-gamora-cycle-14-a2-1-step-1-synthetic-kit-kpm-recalibration.md` | ✅ COMPLETE 2026-05-29 — 18/18 PASS per-bc_cell_id magnitude table; engine `8715f10` + `685b362` + tag `gamora/v2.13-a2-1-step-1-synthetic-kit-kpm-recalibration-1`; collab `c8766a9` + `5e7c989` |
| **A2-1 Step 2 (THIS DISPATCH)** | this dispatch | ⏳ PENDING — Concern #2 flag flip + assert lift |

### 0.2 Empirical observation from A2-1 RE-FIRE FAIL (KR-verified)

Rocket A2-1 RE-FIRE attestation (commit `9f9ed28` § 3):

> Phase 5: Wave A SKIPPED (faction_visibility="invisible" = placeholder mode). Zero real LLM calls fired. LLM cost: $0.0000. The dispatch framing said "cohesion judge LLM calls FOR REAL THIS TIME." This was incorrect — the wave5_season_orchestrator.py hardcodes `faction_visibility="invisible"` which short-circuits Wave A entirely. Phase 5 in this pipeline is placeholder mode by design (Reincarnated v1 default per phase5_orchestrator.py line 83). No LLM cohesion judge budget was consumed.

KR Concern #2 surface at commit `e99b000`:

> **Concern #2 — Phase 5 LLM cohesion judge HARDCODED to placeholder mode.** `wave5_season_orchestrator.py:89` `FACTION_VISIBILITY="invisible"` SKIPS Wave A (faction LLM) AND Wave B (per-kit identity LLM); hardcoded `assert` at lines 1264-1265 enforces. **LLM cohesion judge NEVER exercised in current v1 production configuration.** Matt directive: removal of LLM runs from v1 is off the table.

### 0.3 Locked direction (Matt 2026-05-29 — Path D; not Path C or Path E)

- **Path C** (FACTION_VISIBILITY=invisible is intentional v1 commitment; defer to v2; re-examine D9 criteria) — NOT taken
- **Path D** (this dispatch — FACTION_VISIBILITY should be **visible** for Wave 5 production; orchestrator amendment) — RATIFIED
- **Path E** (mixed model; Phase 5 placeholder bug investigation) — NOT taken

**Resolution semantic:** the `invisible` default + hardcoded `assert` was scaffold-survival into production-fire (Disc #40 candidate). The locked v1 production direction is Wave A + F-C + Wave B all fire under `visible` mode. The A/B comparison protocol (Wave 5 close, A2-5 scope) is **independent** of FACTION_VISIBILITY flag and untouched by this dispatch.

### 0.4 Substrate-vector context (KR pre-loaded for rocket session)

**File:** `~/Games/reincarnated-engine/src/reincarnated/simulation/wave5_season_orchestrator.py`

**Touch sites (KR-verified against engine HEAD post Step 1):**

| Line(s) | Current state | New state |
|---|---|---|
| 12 (module docstring) | `Phase 5 — Cohesion-judge LLM: Phase5Orchestrator Wave A + F-C + Wave B (faction_visibility=invisible)` | `Phase 5 — Cohesion-judge LLM: Phase5Orchestrator Wave A + F-C + Wave B (faction_visibility=visible)` |
| 89 (constant + inline comment) | `FACTION_VISIBILITY: str = "invisible"   # Reincarnated v1 default; Wave A skipped` | `FACTION_VISIBILITY: str = "visible"   # Reincarnated v1 default; Wave A + F-C + Wave B fire (Matt 2026-05-29 Path D)` |
| 802-806 (Phase 5 function docstring) | block describes invisible-mode behavior | block describes visible-mode behavior (Wave A fires; faction_label_canonical produced; F-C inter-faction relationships fired; Wave B per-kit identity fired) |
| 1264-1266 (module-load postscript assert) | `assert FACTION_VISIBILITY == "invisible", (...)` | UPDATE the assert to match new default: `assert FACTION_VISIBILITY == "visible", (...)` OR LIFT entirely per architectural call below |

**Architectural call for assert at lines 1264-1266 (rocket's seam-internal decision):**

The assert exists as Disc #11 module-load postscript ensuring the default does not silently drift. Two options:

- **Option α (UPDATE):** change the asserted value from `"invisible"` to `"visible"`. Preserves the Disc #11 module-load guarantee; the new locked default is enforced.
- **Option β (LIFT to broader invariant):** replace with `assert FACTION_VISIBILITY in {"invisible", "visible"}, (...)` so the assert guards SHAPE (valid value space) without locking VALUE. This is more flexible if v1.x explores per-season flag-changes; less brittle to future flag flips.

KR recommendation: **Option α** for v1 lock semantics (D9 ratified close-criterion uses visible-mode as the production configuration; locking the asserted value matches the Cycle 14 v1 commitment). Rocket's call if there's a compelling reason to prefer β.

### 0.5 Disc #42a framing-audit at dispatch consumption

KR's authoring applied Q1-Q6. Rocket should re-apply at consumption:

- **Q1 — load-bearing framing assumption:** "Flipping FACTION_VISIBILITY from `invisible` to `visible` (and updating the assert to match) is a single-file amendment that causes Phase 5 to exercise Wave A + F-C + Wave B real LLM calls under Step 4 A2-1 RE-FIRE consumption."
- **Q2 — refutation evidence in scope:** any OTHER pre-imposed assumption gating LLM exercise beyond FACTION_VISIBILITY (e.g., other module-load flags, conditional short-circuits, env-var dependencies)? Rocket runs Disc #11 downstream-consumer audit (per § 1.2 below) to verify NO additional gating exists. If additional gating surfaces → SURFACE TO KR before commit.
- **Q3 — refutation surface-able cheaply:** yes — grep + read `wave5_season_orchestrator.py` and the consumer `phase5_orchestrator.py` (already KR-pre-scanned; see § 0.6 below) to confirm no other LLM-gating flags
- **Q4 — measurement context match:** Step 4 A2-1 RE-FIRE consumption fires the full pipeline with the new flag value; the cohesion-judge LLM cost guard (star-lord) projects against $50 soft cap; measurement matches the Cycle 14 v1 production configuration
- **Q5 — calibration scope match:** D9 ratified close-criterion (≥12/18 emit) was authored under the (still-implicit) assumption that Phase 5 LLM cohesion judge IS exercised; the `invisible`-default was the scaffold-survival pre-imposed assumption refuted at A2-1 RE-FIRE. Path D restores measurement scope to the D9 ratification intent.
- **Q6 — semantic stability of "visible-mode LLM exercised" vs "Cycle 14 v1 production":** the flip from `invisible` to `visible` is the v1 production lock; player-facing faction-architecture commitments (per `canonical/story/fate-genre-recognition-and-mobile-alignment-trajectory-2026-05-23.md` deferred-commitments recognition record) are SEPARATE from this orchestrator flag (the flag controls **generation-side LLM exercise**; player-side faction surfacing is downstream surface seam, not gated by this flip). Rocket completion record MUST distinguish.

If any framing refutes, SURFACE TO KR before commit.

### 0.6 KR-pre-scan of downstream consumers (informational for rocket audit)

KR pre-scanned `phase5_orchestrator.py` for FACTION_VISIBILITY consumer semantics:

- `phase5_orchestrator.py:83` — module-level comment captures "invisible" = v1 default Wave A SKIPPED
- `phase5_orchestrator.py:88` — implementation: `if faction_visibility == "invisible" and not monster_contrast_enabled` short-circuit
- `phase5_orchestrator.py:191-193` — config dataclass field `faction_visibility: str = "invisible"` (the consumer-side default; orchestrator OVERRIDES with FACTION_VISIBILITY at line 835)
- `phase5_orchestrator.py:196-197` — `monster_contrast_enabled: bool` — second gating flag; when True, Wave A fires regardless of visibility
- `phase5_orchestrator.py:229-231` — `should_fire_wave_a()` returns `(visibility == "visible") OR monster_contrast_enabled`
- `phase5_orchestrator.py:286` — `short_circuited: bool` field on result tracks Wave A skip status
- `phase5_orchestrator.py:1698-1700` — log line reports both `faction_visibility` AND `monster_contrast` at config init
- `phase5_orchestrator.py:2012` — comment: `"placeholder"` when LLM layer short-circuited

**KR conclusion (informational):** the only gating flags are (a) `faction_visibility` and (b) `monster_contrast_enabled`. Flipping `FACTION_VISIBILITY` to `"visible"` at the orchestrator level causes `should_fire_wave_a() = True` regardless of `monster_contrast_enabled`. Rocket's audit (per § 1.2) verifies this empirically; if any OTHER gating flag surfaces, SURFACE TO KR.

---

## 1. THE TASK

**Flip `FACTION_VISIBILITY` from `"invisible"` to `"visible"` in `wave5_season_orchestrator.py`, update the module-load assert + module docstring + inline comment + Phase 5 function docstring to match, and verify (Disc #11 empirical inspection) that no OTHER gating flag short-circuits Wave A/F-C/Wave B beyond what KR pre-scanned.**

### 1.1 Pre-flight (REQUIRED before edit)

1. **Disc #48 R48.5 vm_stat check:** confirm > 1 GB free + reclaimable (KR pre-flight at Step 2 entry showed ~2.8 GB available; verify still holds)
2. **Disc #48 R48.4 single-seam confirm:** gamora sub-agent released post Step 1 PASS; only this dispatch's rocket is running
3. **Engine state confirm:** HEAD at `685b362` (gamora Step 1 AGENT_STATE checkpoint); Step 1 commits `8715f10` + tag `gamora/v2.13-a2-1-step-1-synthetic-kit-kpm-recalibration-1` intact
4. **Verify the touch sites have not drifted:** grep `FACTION_VISIBILITY` in `wave5_season_orchestrator.py` → exactly the 5 touch sites at § 0.4 above (no surprise additional sites)

### 1.2 Disc #11 downstream-consumer audit (REQUIRED before edit)

Run audit confirming NO additional LLM-gating flag short-circuits Wave A / F-C / Wave B beyond `FACTION_VISIBILITY` + `monster_contrast_enabled` (which are KR-pre-scanned at § 0.6):

1. `grep -n "skip\|short_circuit\|placeholder\|stub" ~/Games/reincarnated-engine/src/reincarnated/llm/phase5_orchestrator.py` — surface any conditional short-circuit logic
2. `grep -rn "faction_visibility\|FACTION_VISIBILITY" ~/Games/reincarnated-engine/src/reincarnated/` — confirm scope of references
3. Read `phase5_orchestrator.py` § around lines 1690-1710 + § around lines 2000-2020 (KR-pre-scanned log + placeholder semantics)
4. Read `phase5_orchestrator.py` `should_fire_wave_a()` definition (line 229-231) + verify there's no THIRD gating flag

If audit surfaces any pre-imposed assumption OTHER than `FACTION_VISIBILITY` gating LLM exercise → SURFACE TO KR before commit (this is Disc #42a Instance-5 risk; capture as case-type same as gandalf pushback memo Instance 4).

### 1.3 The 5 edits

**Edit 1 — Module docstring (line 12):**

```python
# BEFORE
  Phase 5 — Cohesion-judge LLM: Phase5Orchestrator Wave A + F-C + Wave B (faction_visibility=invisible)
# AFTER
  Phase 5 — Cohesion-judge LLM: Phase5Orchestrator Wave A + F-C + Wave B (faction_visibility=visible)
```

**Edit 2 — Constant + inline comment (line 89):**

```python
# BEFORE
FACTION_VISIBILITY: str = "invisible"   # Reincarnated v1 default; Wave A skipped
# AFTER
FACTION_VISIBILITY: str = "visible"   # Reincarnated v1 default; Wave A + F-C + Wave B fire (Matt 2026-05-29 Path D — A2-1 Step 2 cascade-resumption)
```

**Edit 3 — Phase 5 function docstring (lines 802-806):**

```python
# BEFORE
    With faction_visibility="invisible" (Reincarnated v1 default):
    - Wave A (faction-level LLM) SKIPPED — placeholder ExportFactionCluster produced
    - G-B primary-pair already in pm1_result (from Phase 3)
    - F-C (inter-faction relationships) fires if Wave A is enabled; SKIPPED here
    - Wave B (per-kit identity) also SKIPPED in invisible mode
# AFTER
    With faction_visibility="visible" (Reincarnated v1 default per Matt 2026-05-29 Path D):
    - Wave A (faction-level LLM) FIRES — real LLM-generated ExportFactionCluster with faction_label_canonical
    - G-B primary-pair already in pm1_result (from Phase 3)
    - F-C (inter-faction relationships) FIRES — Wave A enabled → F-C derives ExportFactionRelationship records
    - Wave B (per-kit identity LLM) FIRES — per-kit cohesion + ai-tell signals produced for Phase 7 consumption
```

**Edit 4 — Module-load postscript assert (lines 1264-1266):**

```python
# BEFORE
assert FACTION_VISIBILITY == "invisible", (
    f"FACTION_VISIBILITY: expected 'invisible' (Reincarnated v1 default), got {FACTION_VISIBILITY}"
)
# AFTER (Option α — KR recommendation)
assert FACTION_VISIBILITY == "visible", (
    f"FACTION_VISIBILITY: expected 'visible' (Reincarnated v1 default per Matt 2026-05-29 Path D), got {FACTION_VISIBILITY}"
)
```

(Option β if rocket prefers: `assert FACTION_VISIBILITY in {"invisible", "visible"}, ...` — see § 0.4 for the architectural argument.)

**Edit 5 — Inline commentary at the orchestrator log site (lines 825-827, KR-verified):**

```python
# BEFORE (current state)
    log.info("[Phase 5] Cohesion-judge LLM: faction_visibility=%s (Wave A=%s)...",
             FACTION_VISIBILITY,
             "ENABLED" if FACTION_VISIBILITY == "visible" else "SKIPPED (placeholder mode)")
```

This line is already correctly conditional — no edit needed (the conditional already covers both states; rocket should NOT touch this line). Confirm correct via re-read.

Additional inline-comment touch at line 847 — verify text reads correctly after flag flip:

```python
# CURRENT (line 847)
    # With faction_visibility=invisible, run_phase5_with_fc_sync returns placeholder clusters
```

This is now MISLEADING under visible default. Rocket should update to:

```python
# REPLACEMENT
    # With faction_visibility=visible (Reincarnated v1 default per Matt 2026-05-29 Path D),
    # run_phase5_with_fc_sync fires Wave A + F-C + Wave B; returns LLM-derived clusters + relationships
```

### 1.4 Acceptance criterion (resolution plan § 1 Step 2)

- ✅ All 5 edits landed in `wave5_season_orchestrator.py` per § 1.3 above
- ✅ Disc #11 downstream-consumer audit confirms NO additional LLM-gating flag beyond FACTION_VISIBILITY (+ KR-pre-scanned monster_contrast_enabled)
- ✅ Module-load assert updated (Option α recommended) OR lifted to broader invariant (Option β with rationale)
- ✅ `python -c "from reincarnated.simulation.wave5_season_orchestrator import FACTION_VISIBILITY; assert FACTION_VISIBILITY == 'visible'"` succeeds
- ✅ No new test failures (run engine test suite quick-smoke if practical — Disc #2)
- ✅ MIGRATION.md update IF rocket judges this qualifies as cross-seam contract change (KR judgement: this is engine-internal orchestrator flag; rocket's call whether MIGRATION.md applies)
- ✅ Tag: `rocket/v1.1-a2-1-step-2-faction-visibility-visible-1` (or seam convention)
- ✅ Auto-commit per CLAUDE.md addendum 2026-05-25
- ✅ Do NOT push — KR fires push after Step 4 A2-1 RE-FIRE PASS + Step 5 A2-2 Gate-2 PASS per per-workstream pattern

### 1.5 Completion-record format (append to this dispatch)

Append a `## Completion record` section with:

1. **VERDICT** — single line: "A2-1 Step 2 FACTION_VISIBILITY flip — PASS (all 5 edits landed; module-load assert updated; downstream-consumer audit clean; v1 production locked to visible mode)" OR "FAIL with diagnosis + framing-audit Q1/Q2/Q3 applied"
2. **5 edits applied** — file + line + before/after diff snippets
3. **Architectural call on assert** — Option α (update value) or Option β (lift to invariant); rationale
4. **Disc #11 downstream-consumer audit results** — grep output enumerated; any additional gating flag found (expected: NONE)
5. **Module-load smoke verification** — `from reincarnated.simulation.wave5_season_orchestrator import FACTION_VISIBILITY; assert FACTION_VISIBILITY == 'visible'` PASS
6. **Disc #2 quick-smoke test results** — if practical (else cite skipped + reason)
7. **Disc #42a Q1-Q6 framing-audit** — self-audit at completion (meta-observation 5; verify edits match dispatch intent)
8. **Disc #48 R48.4/R48.5 verification** — gamora released; rocket alone; vm_stat captured
9. **Player-facing-vs-generation-side separation attestation** — confirm dispatch consumer-side note that THIS dispatch does NOT commit player-facing faction surfacing (per deferred-commitments recognition record at `canonical/story/fate-genre-recognition-and-mobile-alignment-trajectory-2026-05-23.md`; player-side surfacing is separate downstream seam)
10. **MIGRATION.md disposition** — applied (cite § number) OR judged inapplicable (cite reason)
11. **Engine + collab commits + tag** — rocket commits + tag
12. **Telemetry output paths** — N/A (no new sweep telemetry; this is an orchestrator flag flip)
13. **Any anomalies surfaced** during edit / audit

---

## 2. CROSS-SEAM CONTRACT CHANGE? (Principle 6)

**Engine-internal orchestrator flag flip; no cross-seam contract change beyond the LLM exercise that the downstream phase5_orchestrator was already wired to consume.** The semantic shift is: from "Phase 5 emits placeholder clusters" to "Phase 5 emits LLM-derived clusters." Downstream consumers (Phase 7 cohesion-judge consumption + ExportFactionCluster / ExportFactionRelationship telemetry surface) were ALREADY DESIGNED to handle either mode (per `phase5_orchestrator.py:286` `short_circuited` field + `phase5_orchestrator.py:2012` `"placeholder"` semantics).

If rocket's Disc #11 audit surfaces a downstream consumer that ASSUMED placeholder-mode (e.g., asserts `short_circuited == True`), that's a Disc #42a Instance-5-style scaffold-survival finding → SURFACE TO KR.

---

## 3. QUALITY CRITERION (KR OP § 3.11)

**Game-quality goal:** restore Phase 5 cohesion-judge LLM exercise to the Cycle 14 v1 production configuration so the A2-1 RE-FIRE Step 4 consumption produces the empirical signal D9 ratified close-criterion intended to measure — kits emit at ≥12/18 AFTER real-LLM cohesion judge exclusions, not placeholder-mode pseudo-exclusions. Matt directive: "removal of LLM runs from v1 is off the table."

**Refutation conditions:**
- Disc #11 audit surfaces additional LLM-gating flag beyond FACTION_VISIBILITY + monster_contrast_enabled — refute = Disc #42a Instance-5 surface; SURFACE TO KR; KR escalates to Matt for second-instance scaffold pattern
- Module-load assert update breaks tests elsewhere — refute = Disc #11 empirical inspection at quick-smoke + cite breakage
- Downstream consumer asserts short_circuited==True somewhere — refute = SURFACE TO KR before commit (downstream consumer-side amendment may be required)
- Dispatch framing pre-commits to a decision Matt has not ratified — NO (Path D Matt-ratified per resolution plan § 1 Step 2)
- Dispatch introduces pre-authored taxonomy without justification (#41 candidate) — N/A
- Dispatch introduces scaffold value not flagged as pending-decision (#40) — partial: the `invisible`-default + hardcoded `assert` was scaffold-survival into production (Disc #40 candidate data point); the flip RESOLVES the scaffold rather than introducing a new one; capture in completion record as Disc #40 data point for deferred-batched capture at Matt re-engage per resolution plan § 4

If any refutation condition triggers, SURFACE TO KR before commit.

---

## 4. OUT OF SCOPE

- ❌ Concern #1 synthetic-kit KPM recalibration — Step 1 (gamora; ✅ CLOSED)
- ❌ Cohesion-threshold (`cohesion_judge_confidence >= 0.75`) recalibration — capture-and-watch only per resolution plan § 3
- ❌ A/B comparison protocol (`canonical/story/ab-comparison-protocol-cycle-14-close-2026-05-27.md`) — runs at Wave 5 close (A2-5 scope; gandalf); independent of FACTION_VISIBILITY flag; do NOT touch
- ❌ Player-facing faction-architecture commitments — deferred-commitments recognition record (`canonical/story/fate-genre-recognition-and-mobile-alignment-trajectory-2026-05-23.md`) stands; this flip does NOT commit player-side surfacing; that's separate downstream seam (Cycle 14+ design call)
- ❌ Phase5Orchestrator-side amendments (e.g., consumer-side default flip) — orchestrator passes `FACTION_VISIBILITY` explicitly at line 835; consumer-side default change is OUT-of-scope unless audit surfaces a downstream-consumer scaffold-survival issue
- ❌ Phase 7 cohesion-judge-threshold (`cohesion_judge_confidence >= 0.75`) recalibration — scaffold-flag; Pattern B design call deferred to Matt re-engage IF systematic under-0.75 pattern observed in Step 4 A2-1 RE-FIRE telemetry
- ❌ Disc #42a Instance-5 addendum to pushback memo — deferred to Matt re-engage per resolution plan § 4 (capture this dispatch as Instance-5 data point; canonical-write at Matt re-engage; rocket NOT writing canonical here)
- ❌ Disc #40 scaffold-discipline data point canonical capture — deferred to Matt re-engage per resolution plan § 4
- ❌ Decisions-log canonical writes — jack-ryan owns; deferred to Matt re-engage
- ❌ Pushing — per per-workstream pattern; push after Step 4 + Step 5 PASS
- ❌ Parallel sub-agent fan-out under R48.4

---

## 5. RISKS + COMPLICATIONS

- **Disc #42a Instance-5 risk:** if Disc #11 downstream-consumer audit surfaces an ADDITIONAL pre-imposed assumption beyond FACTION_VISIBILITY gating LLM exercise → this is the SAME case-type as Phase 7 import bug masking Concern #1 (scaffold-survival pattern). SURFACE TO KR immediately; KR routes to Matt election (potential cascade halt).
- **Assert lift / consumer-side default mismatch:** consumer-side default at `phase5_orchestrator.py:193` is still `"invisible"`. Orchestrator explicitly overrides at line 835 → no functional break. But the consumer-side default-mismatch is a Disc #11 hygiene observation; rocket's call whether to flag in completion record as captured INFO (not a blocker).
- **Downstream consumer test coverage:** existing tests may assume placeholder-mode short-circuit. Rocket's call whether to update test assertions OR add new tests covering visible-mode (do NOT delete existing tests; preserve as historical). Surface in completion record.
- **Real LLM cost impact at Step 4:** Step 4 A2-1 RE-FIRE will be the FIRST production fire that meaningfully spends LLM budget. Star-lord cost guard will project mid-cascade against $50 soft cap; this is expected behavior, not a Step 2 risk.
- **Player-facing-architecture conflation risk:** rocket completion record MUST clearly distinguish "generation-side LLM exercise" (this flip) from "player-facing faction surfacing" (deferred commitments). The flag flip controls the FORMER only; the LATTER remains Matt-election territory for v1.x+.

---

## 6. URGENCY + SEQUENCING

**Fires under R48.4 single-seam IMMEDIATELY (gamora released post Step 1 PASS).** Step 3 (jack-ryan Gate-2) fires AFTER this dispatch closes; Step 4 (A2-1 RE-FIRE) fires AFTER Step 3 PASS.

Per resolution plan § 2: this dispatch is ~0.5-1h. Cumulative through Step 2 close: ~1.5-3h. Cascade then proceeds to Step 3 (Gate-2 ~0.5h) → Step 4 (A2-1 RE-FIRE ~1d) → Step 5+.

A2-1 Step 2 PASS → KR fires Step 3 (jack-ryan Gate-2 Pattern E autonomous-pair on Step 1 + Step 2 outputs).

A2-1 Step 2 FAIL → KR surfaces to Matt with framing-audit Q1-Q6 applied (FAIL would surface either a Disc #42a Instance-5 finding or downstream-consumer mismatch; routes to Matt).

---

## 7. SURFACING-TO-KR PROTOCOL

Append completion record (interim OR final) at any of:

- ✅ All 5 edits landed; Disc #11 audit clean; assert updated → normal close (KR fires Step 3 jack-ryan Gate-2)
- ⚠️ Disc #11 audit surfaces additional LLM-gating flag → SURFACE IMMEDIATELY before commit (Disc #42a Instance-5 surface; routes to Matt)
- ⚠️ Downstream consumer asserts short_circuited==True somewhere → SURFACE IMMEDIATELY (downstream amendment may be required)
- ⚠️ Test failures from assert update → SURFACE for KR call (test-update scope decision)
- ⚠️ Disc #42a Q1-Q6 framing-audit refutes any other pre-imposed assumption → SURFACE IMMEDIATELY
- ⚠️ Disc #48 R48.5 RAM pressure → pause + SURFACE
- 🚨 Substantial unexpected failure mode → SURFACE IMMEDIATELY

---

## 8. REFERENCES

- `agentic_orchestration/gandalf/notes/2026-05-29-concern-1-and-2-resolution-plan.md` — authoritative resolution plan (Path D ratified for Concern #2; this dispatch IS § 1 Step 2)
- `agentic_orchestration/dispatches/2026-05-29-gamora-cycle-14-a2-1-step-1-synthetic-kit-kpm-recalibration.md` — Step 1 dispatch + completion record (PASS); precedes this dispatch in cascade
- `agentic_orchestration/dispatches/2026-05-29-rocket-cycle-14-a2-1-refire-post-phase7-bridge-fix.md` § Completion record § 3 — empirical placeholder-mode observation (Wave A SKIPPED; $0 LLM)
- `agentic_orchestration/cycle-14-path-alpha-v1-closure-record-2026-05-28.md` — Phase A1 closure record
- `agentic_orchestration/cycle-14-hive-mind-state.md` — Wave 5 state (cascade resumption in-flight)
- `agentic_orchestration/gandalf/pushback/2026-05-28-framing-audit-three-instance-case.md` — Disc #42a Q1-Q6 architectural argument (Instance 4 same case-type as this dispatch's risk if audit surfaces additional gating)
- `canonical/story/fate-genre-recognition-and-mobile-alignment-trajectory-2026-05-23.md` — deferred-commitments recognition record (player-facing faction surfacing remains v1.x+ Matt-election territory)
- `canonical/story/ab-comparison-protocol-cycle-14-close-2026-05-27.md` — A/B comparison protocol (independent of FACTION_VISIBILITY; runs at A2-5; DO NOT touch)
- `~/Games/reincarnated-engine/src/reincarnated/simulation/wave5_season_orchestrator.py` — target file (5 edit sites at lines 12 / 89 / 802-806 / 1264-1266 + 847)
- `~/Games/reincarnated-engine/src/reincarnated/llm/phase5_orchestrator.py` — downstream consumer (KR-pre-scanned at § 0.6; should_fire_wave_a() at line 229-231)
- `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disc #1/#2/#11/#21/#22/#40/#42a/#43/#48 active
- Engine HEAD: `685b362` (gamora Step 1 AGENT_STATE checkpoint); tag `gamora/v2.13-a2-1-step-1-synthetic-kit-kpm-recalibration-1`

---

**KR signature:** authored per Phase A2 cascade RESUMPTION authorization + R48.4 single-seam (gamora released post Step 1 PASS; rocket alone) + Disc #42a meta-observation 5 self-vigilance (Step 1 PASS artifact verified at engine HEAD `685b362` + PHASE7_SYNTHETIC_KIT_MAGNITUDE_TABLE 18-entry dict + assert + fallback + tag verified via grep + git log; sweep telemetry + math note artifacts on-disk verified) + auto-commit per CLAUDE.md addendum 2026-05-25 + Disc #42a Q2/Q5 vigilance forward (rocket Disc #11 downstream-consumer audit verifies NO additional LLM-gating flag beyond FACTION_VISIBILITY + monster_contrast_enabled).

This dispatch is the cheapest empirical refutation of "is `FACTION_VISIBILITY="visible"` the single architectural lever that activates Phase 5 LLM exercise in Wave 5 production, AND is there no other pre-imposed assumption gating the LLM call?" — single-file amendment + downstream-consumer audit at rocket's seam-internal cost (no LLM spend; ~0.5-1h wall-clock).

A2-1 Step 2 PASS = Concern #2 resolved + unblocks A2-1 Step 3 (jack-ryan Gate-2 Pattern E autonomous-pair on Step 1 + Step 2 outputs) → cascade resumes Step 4 (A2-1 RE-FIRE) → Step 5+ per resolution plan § 1 sequence toward Cycle 14 v1 MVP D9 close.

---

## Completion record

**Date:** 2026-05-29
**Rocket engine commits:** `5d69291` (flag flip) + `3b69dad` (AGENT_STATE checkpoint)
**Tag:** `rocket/v1.1-a2-1-step-2-faction-visibility-visible-1`

---

**1. VERDICT**

A2-1 Step 2 FACTION_VISIBILITY flip — PASS (all 5 edits landed; module-load assert updated Option α; downstream-consumer audit clean; v1 production locked to visible mode). Concern #2 resolved. A2-1 Step 3 (jack-ryan Gate-2) unblocked.

---

**2. 5 edits applied**

| # | Site | Before | After |
|---|---|---|---|
| 1 | Line 12 module docstring | `faction_visibility=invisible` | `faction_visibility=visible` |
| 2 | Line 89 constant + inline comment | `"invisible"   # Reincarnated v1 default; Wave A skipped` | `"visible"   # Reincarnated v1 default; Wave A + F-C + Wave B fire (Matt 2026-05-29 Path D — A2-1 Step 2 cascade-resumption)` |
| 3 | Lines 802-806 Phase 5 function docstring | "invisible" mode: Wave A SKIPPED / F-C SKIPPED / Wave B SKIPPED | "visible" mode: Wave A FIRES / F-C FIRES / Wave B FIRES (per dispatch § 1.3 Edit 3 exact text) |
| 4 | Line 847 inline comment | `# Run Phase 5 (Wave A skipped; placeholder mode active) / # With faction_visibility=invisible, run_phase5_with_fc_sync returns placeholder clusters / # and no F-C calls (Wave A is the prerequisite for F-C)` | `# Run Phase 5 (Wave A + F-C + Wave B active; visible mode) / # With faction_visibility=visible (Reincarnated v1 default per Matt 2026-05-29 Path D), / # run_phase5_with_fc_sync fires Wave A + F-C + Wave B; returns LLM-derived clusters + relationships` |
| 5 | Lines 1264-1265 assert | `assert FACTION_VISIBILITY == "invisible", (f"... expected 'invisible' ...")` | `assert FACTION_VISIBILITY == "visible", (f"... expected 'visible' (... per Matt 2026-05-29 Path D) ...")` |

Lines 825-827 (orchestrator log — already correctly conditional) and line 835 (pass-through to phase5_orchestrator) and line 897 (telemetry dict pass-through) — NOT touched per dispatch § 1.3 instruction.

---

**3. Architectural call on assert**

Option α applied (update asserted value from `"invisible"` to `"visible"`). Rationale: D9 ratified close-criterion uses visible-mode as the production configuration; locking the asserted value matches the Cycle 14 v1 commitment. Option β (lift to broader invariant `{invisible, visible}`) was considered but Option α is cleaner for v1 lock semantics — if the flag changes in v1.x, that constitutes a deliberate revision requiring a new assert update and attribution, which is the correct audit trail. KR recommendation confirmed.

---

**4. Disc #11 downstream-consumer audit results**

Audit commands run:
- `grep -n "skip|short_circuit|placeholder|stub" phase5_orchestrator.py` — returned 60+ lines; all are: (a) placeholder field names / data structures, (b) the `if short_circuited:` branch handling visible/invisible forking (2-flag gate only), and (c) comments documenting placeholder semantics. No functional third gating flag found.
- `grep -rn "faction_visibility|FACTION_VISIBILITY" src/reincarnated/` — returned 50+ hits across wave5_season_orchestrator.py, phase5_orchestrator.py, phase7_verdict.py, export/MIGRATION.md, export/schemas.py, and math docs. All references outside wave5_season_orchestrator.py are: (a) documentation/comments, (b) the `phase5_orchestrator.py:231` `should_fire_wave_a()` gate (2-flag: `faction_visibility == "visible" OR monster_contrast_enabled`), or (c) schema comments on nullable `faction_label_canonical`.
- `phase5_orchestrator.py:229-231 should_fire_wave_a()` confirmed: `return self.faction_visibility == "visible" or self.monster_contrast_enabled` — exactly 2 gating flags. No third.
- Lines 1691-1711: `short_circuited = not config.should_fire_wave_a` — derived from should_fire_wave_a; if faction_visibility="visible", short_circuited=False, Wave A fires. No downstream code asserts `short_circuited == True`.
- Lines 2012-2013: comment only — "placeholder when LLM layer short-circuited"; not a functional assertion.

**Verdict: CLEAN. No additional LLM-gating flag beyond FACTION_VISIBILITY + monster_contrast_enabled. No surface-to-KR condition triggered.**

INFO observation (not a blocker): `phase5_orchestrator.py:193` consumer-side dataclass default is still `faction_visibility: str = "invisible"`. This is benign — wave5_season_orchestrator.py:835 overrides with FACTION_VISIBILITY explicitly at Phase5OrchestratorConfig construction. Consumer-side default mismatch is a Disc #11 hygiene note: if a future caller instantiates Phase5OrchestratorConfig without overriding, it will default to invisible. Out of scope for this dispatch per § 4 (consumer-side default flip explicitly excluded).

---

**5. Module-load smoke verification**

```
python3 -c "from reincarnated.simulation.wave5_season_orchestrator import FACTION_VISIBILITY; assert FACTION_VISIBILITY == 'visible'; print(f'PASS: FACTION_VISIBILITY={FACTION_VISIBILITY}')"
```
Output: `PASS: FACTION_VISIBILITY=visible`

PASS.

---

**6. Disc #2 quick-smoke test results**

`python3 -m pytest tests/test_phase7_bridge.py --no-header -q` — 9 passed in 0.22s. PASS.

Broader pytest run filtered to `faction_visibility or wave5_season_orchestrator or phase5` surfaced 2 pre-existing collection errors in `test_b6_generator_wired.py` and `test_cosmological_vocabulary.py` (missing `grouping-layer-vocabulary.md` env var — star-lord seam environment issue, pre-existing, unrelated to this edit). No new test failures from FACTION_VISIBILITY assert update.

---

**7. Disc #42a Q1-Q6 framing-audit self-audit**

| Q | Question | Verdict |
|---|---|---|
| Q1 | Load-bearing assumption: flipping FACTION_VISIBILITY to `visible` causes Wave A + F-C + Wave B to fire | HOLDS — `should_fire_wave_a()` returns True when faction_visibility=="visible"; verified at phase5_orchestrator.py:231 |
| Q2 | Refutation evidence in scope: any OTHER pre-imposed gating assumption beyond FACTION_VISIBILITY? | HOLDS — Disc #11 audit found zero additional gating flag; 2 flags only confirmed |
| Q3 | Refutation surface-able cheaply | HOLDS — grep + read took minutes, no LLM spend |
| Q4 | Measurement context match: Step 4 A2-1 RE-FIRE will exercise visible-mode; cost guard active | HOLDS — no change to star-lord cost projection mechanism |
| Q5 | Calibration scope match: D9 close-criterion authored under implicit visible-mode assumption; invisible was scaffold-survival | HOLDS — Path D restores measurement scope to D9 ratification intent (per resolution plan § 1 Step 2 semantic) |
| Q6 | Semantic stability: generation-side LLM exercise vs player-facing faction surfacing are distinct | HOLDS — see § 9 attestation below |

All 6 HOLD. Edits match dispatch intent. No surface-to-KR condition from framing-audit.

---

**8. Disc #48 R48.4/R48.5 verification**

- R48.4: gamora released post Step 1 PASS (engine HEAD 685b362 = gamora AGENT_STATE checkpoint; no concurrent sub-agent). Rocket alone for Step 2. PASS.
- R48.5: vm_stat at dispatch entry showed Pages free=6791 × 16384 = ~108 MB free + Pages inactive=170476 × 16384 = ~2.7 GB reclaimable = ~2.8 GB free+reclaimable. Exceeds 1 GB threshold. PASS.

---

**9. Player-facing-vs-generation-side separation attestation**

ATTESTATION: This dispatch (A2-1 Step 2) flips `FACTION_VISIBILITY` from `"invisible"` to `"visible"` to activate the **generation-side LLM exercise** (Wave A faction-level LLM calls, F-C inter-faction relationship calls, Wave B per-kit identity calls). This controls whether the Phase 5 cohesion-judge LLM pipeline fires during season generation.

This dispatch does NOT commit to any **player-facing faction surfacing** decision. The deferred-commitments recognition record at `canonical/story/fate-genre-recognition-and-mobile-alignment-trajectory-2026-05-23.md` stands: player-side faction surfacing (whether players see faction labels, whether faction clusters surface in UI, whether faction relationships are rendered in loadout) remains Matt-election territory for v1.x+. The orchestrator flag controls the generation-side LLM exercise; downstream player-facing surface decisions are a separate seam (drax/loadout architecture) that KR explicitly excluded from this dispatch's scope per § 4.

These are semantically distinct: the flag being `"visible"` means "the cohesion-judge LLM exercises during generation to produce faction_label_canonical + ExportFactionCluster + ExportFactionRelationship records for telemetry + Phase 7 gate consumption." It does not mean "these records surface to the player in v1."

---

**10. MIGRATION.md disposition**

Judged INAPPLICABLE. This is an engine-internal orchestrator flag flip. No cross-seam contract change: downstream consumers (phase5_orchestrator.py, phase7_verdict.py, export/schemas.py) were already designed to handle both modes via the `short_circuited` field and nullable `faction_label_canonical`. The semantic shift (placeholder clusters → LLM-derived clusters) was the pre-designed Phase 5 production mode; no consumer requires amendment to handle visible-mode outputs. MIGRATION.md would apply if the flag change required consumers to update their handling logic — it does not.

---

**11. Engine + collab commits + tag**

- Engine commit 1: `5d69291` — `rocket: A2-1 Step 2 — FACTION_VISIBILITY flip invisible → visible (Path D, Matt 2026-05-29)`
- Engine commit 2: `3b69dad` — `rocket: AGENT_STATE checkpoint — A2-1 Step 2 COMPLETE (FACTION_VISIBILITY visible; Concern #2 resolved)`
- Tag: `rocket/v1.1-a2-1-step-2-faction-visibility-visible-1` (on `5d69291`)
- Collab commit: this completion record append (to follow)

---

**12. Telemetry output paths**

N/A — this dispatch produces no new sweep telemetry. It is an orchestrator flag flip only. Step 4 A2-1 RE-FIRE will produce the first real Phase 5 LLM telemetry (ExportFactionCluster + ExportFactionRelationship records with `faction_label_canonical` populated).

---

**13. Anomalies surfaced**

- **Consumer-side default mismatch (INFO, not blocker):** `phase5_orchestrator.py:193` default remains `faction_visibility: str = "invisible"`. Orchestrator always overrides explicitly at line 835; no functional impact. Noted as hygiene item for future consumer-side cleanup if desired.
- **Test collection errors (pre-existing, unrelated):** `test_b6_generator_wired.py` and `test_cosmological_vocabulary.py` fail collection due to missing `GROUPING_VOCAB_DOC_PATH` env var. Pre-existing star-lord seam environment gap; not introduced by this edit.
- **Disc #40 scaffold-discipline data point (INFO):** the `FACTION_VISIBILITY="invisible"` hardcoded default + `assert FACTION_VISIBILITY == "invisible"` at module-load constitutes a scaffold-survival-into-production pattern (Disc #40 candidate). This dispatch resolves the scaffold by locking the production value. Deferred canonical-write per resolution plan § 4 (Matt re-engage for batched Disc #40 + Disc #42a Instance-5 capture).

---

**Rocket signature:** A2-1 Step 2 PASS — Concern #2 resolved. FACTION_VISIBILITY="visible" locked as Reincarnated v1 production default. Step 3 (jack-ryan Gate-2 Pattern E autonomous-pair on Step 1 + Step 2 outputs) unblocked. No surface-to-KR condition triggered at any step.
