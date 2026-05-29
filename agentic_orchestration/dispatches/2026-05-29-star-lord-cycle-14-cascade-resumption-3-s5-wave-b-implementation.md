# Dispatch — Star-Lord — Cycle 14 Cascade-Resumption-3 Stream S5: Wave B FULL Implementation per Canonical § 5

**Date:** 2026-05-29
**From:** knight-rider (orchestrator)
**To:** star-lord (engine operational-pipeline seam — export/, output/, telemetry/, llm/)
**Authority:**
- Matt 2026-05-29 cascade-resumption-3 authorization + Amendment 1 + Amendment 2 (parallel sub-agent fan-out enabled)
- gandalf authorization at `agentic_orchestration/gandalf/notes/2026-05-29-cascade-resumption-3-class-eradication-authorization.md` § "Stream S5 — Wave B FULL implementation per canonical § 5" (line 248-272)
- gandalf S4 audit at canonical Phase 5 LLM prompts doc commit `13822ba` — Phase 5 LLM prompt audit class-free verification + § 2.5 substrate-input purity precondition + W-A10/W-B8/F-C13 runtime grep acceptance criteria added
- Disc #42a Instance 6 ROOT-CAUSE finding (Wave B phantom; zero `wave_b|WaveB|run_wave_b` matches engine-wide pre-S5) — S5 BUILDS the missing component
- Hive-mind decision-routing (seam-owner decides per audit evidence; Matt last-resort escalation)

**Pattern:** B sustained-execution (~4-6h per Amendment 2 split; S5b rocket integration deferred)
**R48.4 status:** RELAXED per Amendment 2 — fires in parallel with rocket S7 + gamora T4-strategy research
**Pre-flight (this dispatch authoring time):** vm_stat free + reclaimable ~2.8 GB combined > 1 GB threshold; PASS

---

## 0. TL;DR

**Build the Wave B per-kit identity LLM component that has been propagated as taxonomy across cascade-architecture artifacts since the recognition record but does not exist in production code.** Empirical refutation finding 2026-05-29 commit `fd48cab`: `grep -rE 'wave_b|WaveB|run_wave_b' reincarnated-engine/src/` returns ZERO matches engine-wide. This is Disc #42a Instance 6 ROOT-CAUSE — S5 closes the gap.

**Star-lord scope (Amendment 2 split — implementation only; S5b rocket integration deferred to post-S3):**

- Implement `run_wave_b_async()` per canonical § 5 spec at `canonical/story/phase-5-llm-prompts-cohesion-judge-2026-05-27.md` (mirrors Wave A pattern)
- Implement `Phase5WaveBResult` dataclass with required fields
- Per-kit prompt execution infrastructure with functional cost-tracker (already wired post Concern #3 resolution at A2-1 R2 Step 4 — `tracker` parameter functional at Phase 5 LLM call path)
- Implement W-B8 substrate-input purity precondition runtime grep at USER prompt assembly time (canonical § 5.4 acceptance criterion W-B8)

**Effort:** ~4-6h.

**S5b (rocket scope; SEPARATE DISPATCH POST-S3):** Wave B invocation in `wave5_season_orchestrator.py` Phase 5 hook (sequence: Wave A → F-C → Wave B per orchestrator docstring line 12); persist per-kit Wave B outputs to `kit_archive.cohesion_data` (unhardcode `{}` at `wave5_season_orchestrator.py:1169`); wire `cohesion_data` flow to Phase 7 cohesion-judge gate consumption; validate Phase 7 `cohesion_judge_confidence >= 0.75` gate becomes binding (not pass-through).

---

## 1. Required first reads (in order)

1. `agentic_orchestration/gandalf/notes/2026-05-29-cascade-resumption-3-class-eradication-authorization.md` § "Stream S5" (line 248-272) + Amendment 2 (line 7) parallel fan-out protocol
2. `canonical/story/phase-5-llm-prompts-cohesion-judge-2026-05-27.md` — AUTHORITATIVE Wave B spec:
   - § 0.1 Amendment 1 — S4 audit findings + substrate-input purity precondition framing
   - § 2.5 — Substrate-input purity precondition (NEW per S4 audit)
   - § 5 — Wave B per-kit identity LLM prompt template (§ 5.1 Registry consumption / § 5.2 SYSTEM prompt / § 5.3 USER prompt / § 5.4 Acceptance criteria including **W-B8 runtime grep** / § 5.5 Composition with D-Sharpened)
3. gandalf pushback memo Instance 6 at `agentic_orchestration/gandalf/pushback/2026-05-28-framing-audit-three-instance-case.md` § 4-quater — Wave B phantom-component empirical refutation history
4. `canonical/story/2026-05-29-experiential-cascade-architecture-recognition.md` § 0.1 Amendment 1 — Wave B finding amendment + cascade architecture Step C operational gap (S5 closes Step C)
5. Existing `reincarnated-engine/src/reincarnated/llm/phase5_orchestrator.py` — Wave A (`run_wave_a_async()`) is the pattern to mirror for Wave B; F-C (`run_fc_async()`) also implemented; star-lord's reincarnated-star-lord-operating-procedure
6. `agentic_orchestration/dispatches/2026-05-29-star-lord-cycle-14-a2-1-resumption-2-step-4-observability-wire-up.md` — Concern #3 cost-tracker wire-up (already landed; cost-tracker functional at Phase 5 LLM path)
7. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disc #11 + #18 + #41 + #42a + #45 + #48 LOAD-BEARING

---

## 2. Scope

### 2.1 `run_wave_b_async()` implementation

Implement async Wave B entry point at `reincarnated-engine/src/reincarnated/llm/phase5_orchestrator.py`:

- Mirror Wave A pattern (`run_wave_a_async()`) — same async LLM-call infrastructure; same tracker integration; same retry / error handling
- Consume per-kit input per canonical § 5.1 Registry consumption + § 5.3 USER prompt template
- Substitute variables per § 5.3 USER prompt template (`{kit_id}` / `{kit_name_placeholder}` / `{weapon_type_family}` / `{cultural_lineage}` / `{element}` / `{faction_name}` from Wave A / etc.)
- Produce `Phase5WaveBResult` per-kit
- Return `dict[kit_id, Phase5WaveBResult]` (mirrors Wave A return shape adapted for per-kit semantics)

### 2.2 `Phase5WaveBResult` dataclass

Implement per canonical § 5 spec at `reincarnated-engine/src/reincarnated/llm/phase5_orchestrator.py` (or appropriate dataclass module):

Required fields per gandalf authorization line 258:
- `kit_name_canonical: str`
- `kit_identity_narrative: str`
- `ai_tell_compliance_score: float`
- `cohesion_judge_confidence: float`

Additional fields per canonical § 5.4 acceptance criteria — verify which additional fields are spec'd at § 5.2 SYSTEM prompt output schema OR § 5.3 USER prompt output schema; include all spec'd fields.

### 2.3 Per-kit prompt execution infrastructure with functional cost-tracker

- Cost-tracker (`tracker=`) already wired functional at Phase 5 LLM call path per Concern #3 cost-tracker wire-up resolution (A2-1 R2 Step 4 star-lord work; commit `d388c49`)
- Verify Wave B per-call cost accumulates correctly in tracker (smoke test against synthetic prompt → verify tracker.delta > 0 after call)
- Per-call telemetry: per-kit Wave B call cost + latency + token count (mirror Wave A telemetry pattern)

### 2.4 W-B8 substrate-input purity precondition runtime grep

Implement per canonical § 5.4 line 414 acceptance criterion **W-B8**:

```python
import re
combined_substituted_text = (
    f"{kit_id} {kit_name_placeholder} {weapon_type_family} "
    f"{cultural_lineage} {element} {faction_name}"
)
if re.search(
    r'\b(barbarian|wizard|cleric|monk|knight|fighter|assassin|archer|sniper|'
    r'fencer|spellsword|mage|caller|warrior|rogue|hunter|paladin)\b',
    combined_substituted_text,
    re.IGNORECASE
):
    # Gate-2 BLOCK + halt cascade + surface to Matt queue
    # (substrate-input layer regression beyond cascade-resumption-3 S1 eradication)
    raise CascadeBlockError(
        f"W-B8 substrate-input purity precondition violated for kit_id={kit_id}: "
        f"class-vocabulary substring detected in substituted variables"
    )
```

Adapt per `phase5_orchestrator.py` existing error-handling conventions. The W-B8 grep is the LOAD-BEARING runtime defense at Wave B per-kit layer; kit_id substitution is the highest-risk surface in pre-S1 substrate state (or future regression). Per canonical § 5.4 line 414 spec.

Similarly, verify W-A10 (canonical § 4.4) is in place at Wave A USER prompt assembly OR add it if missing (Wave A pattern reference for W-B8 implementation).

F-C13 (canonical § 6.5) — lower-risk surface; consumes Wave A outputs; verify in place at F-C USER prompt assembly time.

---

## 3. Pre-ratified contingent decisions

| Decision point | Pre-ratified action |
|---|---|
| `run_wave_b_async()` signature shape | Mirror Wave A pattern; star-lord elects exact signature per implementation simplicity |
| Phase5WaveBResult additional fields beyond gandalf-spec'd 4 | Per canonical § 5.2/§ 5.3 output schema; star-lord includes all spec'd fields |
| W-B8 implementation error class | Star-lord elects per `phase5_orchestrator.py` existing error-handling conventions |
| W-B8 grep token list | Per canonical § 5.4 line 414 verbatim regex (16 tokens) |

---

## 4. Acceptance criteria (S5 close — star-lord side)

### 4.1 Implementation present (Disc #11 grep)

```bash
grep -rE 'run_wave_b_async|RunWaveB|Phase5WaveBResult|run_wave_b' \
  ~/Games/reincarnated-engine/src/reincarnated/ --include='*.py'
```

**Expected:** non-empty matches (vs ZERO pre-S5 per Instance 6 finding); `run_wave_b_async` function present in `phase5_orchestrator.py`; `Phase5WaveBResult` dataclass present.

### 4.2 W-B8 runtime grep present

```bash
grep -nE 'W-B8|substrate-input purity|barbarian.*wizard.*cleric' \
  ~/Games/reincarnated-engine/src/reincarnated/llm/phase5_orchestrator.py
```

**Expected:** W-B8 runtime grep implemented at Wave B USER prompt assembly point; matches present.

### 4.3 Smoke test

- `run_wave_b_async()` callable with synthetic Wave A output + synthetic kit input; returns valid `Phase5WaveBResult` with 4+ fields populated
- W-B8 grep blocks synthetic class-vocabulary input (raises expected error)
- W-B8 grep passes substrate-vocabulary input (no error)
- Cost-tracker accumulates per Wave B call (`tracker.delta > 0` after synthetic call)

### 4.4 Test suite

- All existing tests PASS (no regression)
- New tests authored for `run_wave_b_async()` + `Phase5WaveBResult` + W-B8 grep behavior (positive + negative cases for W-B8)

### 4.5 Tag

- Engine commit + tag (star-lord prefix per CLAUDE.md: e.g., `star-lord/v1.0-cascade-r3-s5-wave-b-impl-1`)

---

## 5. Out-of-scope for S5 (star-lord side; deferred to S5b rocket post-S3)

- Wave B invocation in `wave5_season_orchestrator.py` Phase 5 hook (S5b rocket)
- `kit_archive.cohesion_data` field wiring + unhardcode `{}` at `wave5_season_orchestrator.py:1169` (S5b rocket)
- Phase 7 cohesion-judge gate `cohesion_judge_confidence >= 0.75` binding integration (S5b rocket)
- Wave B prompt template modifications (canonical doc; gandalf seam; S4 audit already complete)
- Phase 5 LLM cost guard / $50 soft cap projection logic (existing per Concern #3 resolution)
- Wave A modifications (already firing)
- F-C modifications (already firing)
- Cascade-resumption-3 Stream S2 gauntlet variant enumeration (separate dispatch)
- Cascade-resumption-3 Stream S7 substrate multi-sample (parallel-firing rocket dispatch)

---

## 6. Surface to knight-rider conditions

| Condition | Trigger | Action |
|---|---|---|
| **Canonical § 5 spec gap** | Star-lord encounters spec ambiguity OR canonical prompt requires refinement during implementation | Halt + surface to knight-rider; gandalf S4 amendment may be required to canonical Phase 5 LLM prompts doc |
| **Phase5WaveBResult dataclass field surface beyond spec'd 4** | Implementation surfaces additional required fields not enumerated in spec | Author per simpler-implementation principle; document at completion record; surface to knight-rider if architectural |
| **W-B8 regex token list expansion** | Star-lord during testing identifies class-vocabulary tokens not in canonical regex list | Document at completion record; defer to gandalf S4 amendment OR jack-ryan Gate-2 review; do NOT modify canonical regex unilaterally |
| **Cost-tracker integration surfaces deeper gap** | Wave B call shows `tracker.delta = 0` despite functional cost path; OR tracker design issue surfaces | Halt + surface to knight-rider; may compose into Disc #40 scaffold-discipline cumulative finding |
| **Disc #42a framing-audit catch** | Q1-Q6 surfaces pre-imposed assumption mid-execution (e.g., Wave B canonical-vs-implementation gap propagation) | Halt + surface to knight-rider |
| **R48 RAM degradation** | Mid-execution vm_stat shows free + reclaimable < 1 GB combined OR free < 200 MB AND reclaimable < 1 GB | Pause + report; resume when RAM available |
| **S5 effort exceeds ~8h** | Implementation complexity surfaced significantly beyond ~4-6h estimate | Surface to knight-rider — scope reconsideration |

---

## 7. Engineering disciplines composition

| Discipline | Application |
|---|---|
| **Disc #11 empirical inspection** | § 4.1-4.4 acceptance gates; W-B8 grep IS the runtime empirical defense |
| **Disc #18 math hotspot consultation** | Wave B cohesion-confidence scoring math; if star-lord finds multiple methodology options, surface to knight-rider for gandalf Pattern B consultation |
| **Disc #41 substrate-led vocabulary lock** | W-B8 runtime grep IS the operational enforcement at Wave B layer; composes with S1 substrate-input layer eradication |
| **Disc #42a framing-audit Q1-Q6** | Applied at every implementation step; CRITICAL Instance 6 awareness — S5 IS the build that closes the phantom-component gap |
| **Disc #45 vocabulary lock** | W-B8 + W-A10 + F-C13 enforce vocabulary lock at LLM call construction surface |
| **Disc #48 R48.4 RELAXED per Amendment 2** | Parallel fan-out enabled; pre-flight vm_stat at dispatch fire load-bearing |
| **Pattern E autonomous-pair pre-authorization** | Applies at S6 Gate-2 (post-S7+S5+S2+S3+S5b); NOT at S5 fire |
| **Recognition → empirical validation → commit** | Recognition: Wave B phantom-component empirical refutation finding 2026-05-29; Validation: § 4 acceptance gates; Commit: star-lord auto-commits per CLAUDE.md addendum 2026-05-25 |

---

## 8. Deliverables

1. **Engine commit(s)** — phase5_orchestrator.py with `run_wave_b_async()` + `Phase5WaveBResult` + W-B8 grep + (verify W-A10 + F-C13 in place or add) + tag (star-lord prefix per CLAUDE.md)
2. **Tests** — new test cases for Wave B implementation + W-B8 positive/negative
3. **MIGRATION.md entry** if any cross-seam coordination is required (likely minimal — star-lord owns llm/ seam; S5b is rocket follow-on which will have its own MIGRATION)
4. **Completion record appended to this dispatch file** — captures: (a) Wave B implementation evidence (grep matches; function signatures; dataclass fields); (b) W-B8 runtime grep evidence + positive/negative test results; (c) smoke + tests PASS; (d) cost-tracker integration verification; (e) any surface-to-KR findings
5. **AGENT_STATE.md checkpoint** at appropriate star-lord checkpoint location
6. **Auto-commit per CLAUDE.md team commit + push discipline addendum 2026-05-25** — work-products of authorized cascade-resumption-3 work; commit fires without re-asking; push REQUIRES Matt-explicit-auth (do NOT push)

---

## 9. Sign-off

**Authored:** knight-rider per Matt 2026-05-29 Amendment 2 parallel fan-out authorization + gandalf authorization § Stream S5

**Star-lord session-start protocol:**
1. Onboard via § 1 required first reads (especially canonical Phase 5 LLM prompts doc § 5 + § 2.5 + § 5.4 W-B8)
2. Apply Disc #42a framing-audit Q1-Q6 at dispatch consumption (Instance 6 awareness LOAD-BEARING)
3. Execute § 2 scope sub-tasks 2.1 → 2.4
4. Apply § 4 acceptance gates
5. Surface conditions per § 6 if triggered
6. Author § 8 deliverables
7. Auto-commit per CLAUDE.md addendum

**KR next-step on S5 close:** verify § 4 acceptance criteria + § 8 deliverables; route S5b dispatch (rocket Wave B integration + cohesion_data wiring + Phase 7 binding) AFTER S3 close per Amendment 2 § 2 trajectory.

**Parallel-firing companions this batch (Amendment 2 parallel fan-out):**
- **S7 (rocket)** — Phase 2 multi-sample substrate consumption + lineage propagation; ~1-2d; fires in parallel
- **gamora T4-strategy-applicability research** — light analytical work; <300 MB RSS; informs S2 dispatch authoring; fires in parallel

**Signed:** knight-rider (orchestrator)
