# Dispatch — Star-Lord — Cycle 14 Cascade-Resumption-3 Surface 1 Regex Amendment (W-B8/W-A10/F-C13 lookaround pattern)

**Date:** 2026-05-29
**From:** knight-rider (orchestrator)
**To:** star-lord (engine operational-pipeline seam — export/, output/, telemetry/, llm/)
**Authority:**
- Matt 2026-05-29 cascade-resumption-3 Amendment 4 — Surface 1 disposition (W-B8/W-A10/F-C13 regex underscore boundary bug; canonical doc § 4.4/§ 5.4/§ 6.5 AMENDED to lookaround pattern)
- gandalf canonical doc amendment commit `f8ebac4` — Phase 5 LLM prompts canonical doc § 4.4 (W-A10) + § 5.4 (W-B8) + § 6.5 (F-C13) amended regex from `\b(barbarian|...)\b` to `(?<![a-zA-Z])(barbarian|...)(?![a-zA-Z])` lookaround pattern (allows underscore/digit/punctuation as boundaries)
- Hive-mind decision-routing (Matt 2026-05-23 verbatim "seam-owners decide in-scope; Matt is last-resort escalation"); auto-routed per Matt 2026-05-29 hive-state clarification

**Pattern:** Pattern A-light follow-up patch (~30min implementation + tests)
**R48.4 / R48.5 RETIRED per Amendment 3**
**Parallel-firing companion this batch:** gamora S2 (gauntlet variant enumeration; ~1-2d)

---

## 0. TL;DR

**Star-lord S5 implementation (engine commit `a553950`) lands W-B8/W-A10/F-C13 runtime grep with the OLD canonical verbatim regex `\b(barbarian|...)\b`. Canonical doc § 4.4/§ 5.4/§ 6.5 was AMENDED post-S5 per Amendment 4 Surface 1 to lookaround pattern `(?<![a-zA-Z])(barbarian|...)(?![a-zA-Z])`. Update implementation to match amended canonical to close the canonical-vs-implementation gap.**

**Why amend:** the `\b` word-boundary pattern doesn't fire between two `\w` characters; `_` is `\w` in Python regex. So `warrior_001` is NOT caught by `\b(warrior)\b` (no `\b` between `r` and `_`). Lookaround `(?<![a-zA-Z])(?![a-zA-Z])` treats only alphabetic characters as boundary-blockers; underscore/digit/punctuation become boundaries. Tokens like `warrior_001`, `mage42`, `cleric.tag` now correctly match.

**Effort:** ~30min implementation + ~30min new positive tests for underscore-bounded tokens.

---

## 1. Required first reads (in order)

1. `agentic_orchestration/gandalf/notes/2026-05-29-cascade-resumption-3-class-eradication-authorization.md` Amendment 4 (header + Surface 1 disposition)
2. `canonical/story/phase-5-llm-prompts-cohesion-judge-2026-05-27.md` § 4.4 (W-A10 line 286 amended regex) + § 5.4 (W-B8 line 414 amended regex) + § 6.5 (F-C13 line 616 amended regex) — verbatim updated regex strings
3. Your S5 implementation at `reincarnated-engine/src/reincarnated/llm/phase5_orchestrator.py`:
   - Line 176 `# ── W-B8 / W-A10 / F-C13 substrate-input purity regex (canonical § 5.4 line 414 verbatim) ───` — current regex pattern
   - Line 449/453/467 — W-A10 implementation at Wave A
   - Line 1014 — F-C13 implementation at F-C
   - Wave B implementation references
4. `tests/test_cascade_r3_s5_wave_b_impl.py` — existing S5 W-B8/W-A10/F-C13 positive + negative tests
5. `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md` — Disc #11 + #42a (Instance 6 canonical-vs-implementation gap pattern — this patch IS closing the gap)

---

## 2. Scope

### 2.1 Regex pattern amendment

At `reincarnated-engine/src/reincarnated/llm/phase5_orchestrator.py` line ~176 (and any other co-located regex definitions):

**FROM (current; old canonical pre-Amendment 4):**
```python
re.compile(
    r'\b(barbarian|wizard|cleric|monk|knight|fighter|assassin|archer|sniper|'
    r'fencer|spellsword|mage|caller|warrior|rogue|hunter|paladin)\b',
    re.IGNORECASE
)
```

**TO (canonical § 4.4/§ 5.4/§ 6.5 amended verbatim per Amendment 4 Surface 1):**
```python
re.compile(
    r'(?<![a-zA-Z])(barbarian|wizard|cleric|monk|knight|fighter|assassin|archer|sniper|'
    r'fencer|spellsword|mage|caller|warrior|rogue|hunter|paladin)(?![a-zA-Z])',
    re.IGNORECASE
)
```

**Update comment to reference Amendment 4 disposition** (e.g., `# ── W-B8 / W-A10 / F-C13 substrate-input purity regex (canonical § 5.4 line 414 verbatim; AMENDED Amendment 4 2026-05-29 evening per canonical doc lookaround pattern; \b did not fire between warrior and _001 because _ is \w in Python regex) ───`).

### 2.2 New positive tests for underscore-bounded tokens

Add new test cases to `tests/test_cascade_r3_s5_wave_b_impl.py`:

| Test name (suggested) | Input | Expected |
|---|---|---|
| `test_w_b8_catches_underscore_bounded_class_token` | `kit_id="warrior_001"` | Match → CascadeBlockError raised |
| `test_w_a10_catches_underscore_bounded_class_token` | rep_kit_X with `"mage_caster"` substring | Match → CascadeBlockError |
| `test_f_c13_catches_digit_bounded_class_token` | faction_a_name with `"cleric42"` substring | Match → CascadeBlockError |
| `test_w_b8_catches_punctuation_bounded_class_token` | `kit_id="knight.alpha"` | Match → CascadeBlockError |

Verify EXISTING positive tests (clean class-name tokens like `barbarian`, `warrior`) still PASS — Amendment 4 is an EXTENSION of detection capability; no regression.

Verify EXISTING negative tests (substrate-vocabulary tokens like `melee_low_spiky_str_none`) still PASS — substrate vocabulary should not match.

### 2.3 W-A10 + W-B8 + F-C13 all updated atomically

All three sites use the same regex pattern (per canonical doc verbatim). Update all three together in one commit for semantic coherence.

---

## 3. Acceptance criteria

### 3.1 Regex pattern match canonical (Disc #11 grep)

```bash
grep -nE 'lookaround|\(\?\<!\[a-zA-Z\]\)' /Users/admin/Games/reincarnated-engine/src/reincarnated/llm/phase5_orchestrator.py
```

**Expected:** lookaround `(?<![a-zA-Z])` + `(?![a-zA-Z])` present at regex definition; matches canonical § 4.4/5.4/6.5 verbatim.

### 3.2 New test cases for underscore-boundary detection PASS

- Test suite includes new positive cases for `warrior_001` / `mage_caster` / `cleric42` / `knight.alpha` underscore/digit/punctuation-bounded patterns
- All new tests PASS

### 3.3 Existing tests still PASS

- All 92 S5 test cases at `tests/test_cascade_r3_s5_wave_b_impl.py` still PASS (positive + negative; no regression)

### 3.4 Tag

- Engine commit + tag (star-lord prefix per CLAUDE.md: e.g., `star-lord/v1.3-cascade-r3-surface-1-regex-amendment-1`)

---

## 4. Out-of-scope

- Wave B orchestrator integration (S5b rocket scope; post-S3)
- Wave B feature additions (S5 implementation already closed; this is regex-only patch)
- Phase 5 LLM prompt template modifications (gandalf seam; S4 closed; Amendment 4 amended canonical doc)
- Canonical doc edits (gandalf seam; Amendment 4 already amended)
- S2 gauntlet variant enumeration (gamora dispatch; parallel-firing)

---

## 5. Surface to knight-rider conditions

| Condition | Trigger | Action |
|---|---|---|
| **Amended regex breaks unrelated tests** | Existing test PASS regression at unrelated test files | Halt + surface to KR — may indicate broader regex usage we didn't account for |
| **Canonical verbatim copy-paste discrepancy** | Implementation regex doesn't match canonical character-for-character | Halt + surface to KR — Disc #42a Instance 6 vigilance |
| **Disc #42a framing-audit catch** | Q1-Q6 surfaces pre-imposed assumption mid-execution | Halt + surface to KR |

---

## 6. Engineering disciplines composition

| Discipline | Application |
|---|---|
| **Disc #11 empirical inspection** | § 3.1 grep verification + § 3.2/3.3 test PASS gates |
| **Disc #42a framing-audit Q1-Q6** | CRITICAL Instance 6 awareness — this patch IS closing the canonical-vs-implementation gap (canonical amended post-implementation; gap closure required) |
| **Disc #45 vocabulary lock** | Regex enforces vocabulary lock at LLM call construction surface |
| **Disc #48 RETIRED per Amendment 3** | No pre-flight vm_stat gate; no concurrent count limit |
| **Recognition → empirical validation → commit** | Recognition: canonical-vs-implementation gap from Amendment 4 Surface 1; Validation: § 3 acceptance gates + new test cases; Commit: star-lord auto-commits per CLAUDE.md addendum |

---

## 7. Deliverables

1. **Engine commit(s)** — phase5_orchestrator.py regex amendment + new tests + tag (star-lord prefix)
2. **Completion record appended to this dispatch file** — captures: (a) regex amendment evidence (code excerpt; before/after); (b) new test cases + PASS evidence; (c) existing tests PASS evidence (no regression); (d) Disc #11 grep verification PASS
3. **Auto-commit per CLAUDE.md team commit + push discipline addendum 2026-05-25** — work-products of authorized cascade-resumption-3 work; commit fires without re-asking; push REQUIRES Matt-explicit-auth (do NOT push)

---

## 8. Sign-off

**Authored:** knight-rider per Matt 2026-05-29 Amendment 4 Surface 1 disposition + hive-state-explicit observation (auto-route in-scope)

**Star-lord session-start protocol:**
1. Onboard via § 1 required first reads (especially Amendment 4 + canonical § 4.4/5.4/6.5 amended regex)
2. Apply Disc #42a framing-audit Q1-Q6 at dispatch consumption (canonical-vs-implementation closure; this patch IS the closure)
3. Execute § 2 scope (regex amendment at all 3 sites + new positive tests)
4. Apply § 3 acceptance gates
5. Surface per § 5 if triggered (auto-route in-scope per hive-mind decision-routing)
6. Author § 7 deliverables
7. Auto-commit per CLAUDE.md addendum

**KR next-step on close:** verify § 3 acceptance + tag. No further follow-on for star-lord at this point in cascade (S5b is rocket scope post-S3).

**Parallel-firing companion:** gamora S2 (gauntlet variant enumeration expansion per Option C; ~1-2d).

**Signed:** knight-rider (orchestrator)

---

## Completion record

**Date:** 2026-05-29
**Agent:** star-lord
**Engine commit:** `857d825` — `star-lord: cascade-r3 Surface 1 — SUBSTRATE_PURITY_VOCAB_REGEX lookaround amendment (Amendment 4 closure)`
**Tag:** `star-lord/v1.4-cascade-r3-surface-1-regex-amendment-1`

### § 3.1 Regex amendment evidence (before/after at SUBSTRATE_PURITY_VOCAB_REGEX line 192)

**BEFORE (commit a553950; S5 implementation; old canonical pre-Amendment 4):**
```python
SUBSTRATE_PURITY_VOCAB_REGEX: re.Pattern = re.compile(
    r"\b(barbarian|wizard|cleric|monk|knight|fighter|assassin|archer|sniper|"
    r"fencer|spellsword|mage|caller|warrior|rogue|hunter|paladin)\b",
    re.IGNORECASE,
)
```

**AFTER (commit 857d825; canonical § 4.4/5.4/6.5 amended verbatim; Amendment 4 disposition):**
```python
SUBSTRATE_PURITY_VOCAB_REGEX: re.Pattern = re.compile(
    r"(?<![a-zA-Z])(barbarian|wizard|cleric|monk|knight|fighter|assassin|archer|sniper|"
    r"fencer|spellsword|mage|caller|warrior|rogue|hunter|paladin)(?![a-zA-Z])",
    re.IGNORECASE,
)
```

W-B8 (line 1636), W-A10 (line 474), F-C13 (line 1063) all reference `SUBSTRATE_PURITY_VOCAB_REGEX` — all three updated atomically via the single constant change.

### § 3.2 New test cases PASS (underscore/digit/punctuation-bounded class tokens)

Group 15 `TestAmendment4LookaroundBoundary` — 16 tests, all PASS:

| Test | Input | Result |
|---|---|---|
| `test_w_b8_catches_underscore_bounded_class_token` | `kit_id="warrior_001"` | CascadeBlockError raised (W-B8) |
| `test_w_b8_catches_underscore_prefix_class_token` | `kit_id="_warrior_001"` | CascadeBlockError raised (W-B8) |
| `test_w_b8_catches_digit_suffix_class_token` | `kit_id="mage42"` | CascadeBlockError raised (W-B8) |
| `test_w_b8_catches_punctuation_bounded_class_token` | `kit_id="knight.alpha"` | CascadeBlockError raised (W-B8) |
| `test_w_b8_catches_class_token_in_kit_name_with_underscore` | `kit_name_placeholder="rogue_caster_001"` | CascadeBlockError raised (W-B8) |
| `test_w_a10_catches_underscore_bounded_class_token` | rep_kit `"mage_caster_bc1high_fire"` | CascadeBlockError raised (W-A10) |
| `test_w_a10_catches_digit_bounded_class_token` | rep_kit `"wizard42_bc_fire"` | CascadeBlockError raised (W-A10) |
| `test_w_a10_catches_underscore_in_faction_label` | `faction_label_placeholder="rogue_fire_european"` | CascadeBlockError raised (W-A10) |
| `test_f_c13_catches_digit_bounded_class_token` | `faction_a_name="The cleric42 Brotherhood"` | CascadeBlockError raised (F-C13) |
| `test_f_c13_catches_underscore_bounded_class_token_in_faction_b` | `faction_b_name="hunter_elite clan"` | CascadeBlockError raised (F-C13) |
| `test_magery_still_does_not_match_after_amendment` | `cultural_lineage="ancient-magery-tradition"` | PASS (no block — `r` after `mage` is alpha; lookahead blocks) |
| `test_spellcraft_still_does_not_match_after_amendment` | `weapon_type_family="spellcraft-blade"` | PASS (no block — `spellsword` not substring) |
| `test_warrior_standalone_still_blocks_after_amendment` | `kit_id="warrior"` | CascadeBlockError raised (no regression) |
| `test_clean_substrate_still_passes_after_amendment` | default clean inputs | PASS (no block; no regression) |
| `test_disc11_lookaround_pattern_present_in_source` | source grep at compile site | PASS — `(?<![a-zA-Z])` + `(?![a-zA-Z])` present at line 192 block |
| `test_disc11_amendment4_comment_present_in_source` | source grep | PASS — `Amendment 4` + `f8ebac4` present |

### § 3.3 Existing tests PASS (no regression)

92 prior S5 tests PASS (0 regressions). Final: **108/108 PASS**.

### § 3.4 Disc #11 grep verification PASS

`(?<![a-zA-Z])` and `(?![a-zA-Z])` present at `SUBSTRATE_PURITY_VOCAB_REGEX` compile site (line 192). Amendment 4 comment block present at lines 182-191 (commit reference `f8ebac4`, dispatch reference, root-cause rationale).

### Instance 6 canonical-vs-implementation gap status

**CLOSED.** S5 surface finding 1 surfaced that `\b` did not catch `warrior_001`-style tokens. Canonical doc § 4.4/5.4/6.5 amended by gandalf (commit `f8ebac4`). Implementation now matches amended canonical verbatim. Gap duration: S5 commit (`a553950`) → this patch (`857d825`), same session batch.

### § 5 surface conditions

None triggered. No unrelated test regressions. Canonical verbatim copy matches character-for-character. No Disc #42a framing-audit catch during execution.

**Signed:** star-lord (export seam)
