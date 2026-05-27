# Finding — 2026-05-27 — Cycle 14 Wave 1.5 Stage 3 Gate-2 Closure

**Reviewer:** jack-ryan
**Severity:** PASS-with-WARN (2 WARN, 3 INFO; 0 BLOCK)
**Target:** commit `0a5a4f2`; tag `rocket/v1.5-wave-1-5-skill-tree-architecture`
**Developer:** rocket
**Principles applied:** 1 (math-before-code), 2 (smoke-gate before commit), 3 (cross-seam impact), 4 (decisions-log as SSOT), 6 (cross-seam round-trip discipline)

---

## Discipline #40 Canonical-Lock Compliance Verification

**VERIFIED. CLEAN.**

Rocket consumed doc 48 as CANONICAL LOCK input (option (a)). All 10 class names match doc
48 § 1 verbatim (case-sensitive). No scaffold-with-pending-decision flags anywhere in
`class_roster.py`. Module docstring explicitly cites `doc 48 (CANONICAL LOCK — Discipline #40
option (a))`. D83 enforcement fires at construction time (T4_count = chain_count − 1 asserted
in `ClassRosterEntry.__post_init__()`). Class roster is NOT a design output from rocket; it is
a consumption artifact. Discipline #40 intent fully honored.

---

## What I Found

### WARN-1 — Total-chains constant `_EXPECTED_TOTAL_CHAINS = 38` is wrong; narrative comment in code expresses the correct count (32) but the constant is never asserted

**Severity:** WARN
**File:** `class_roster.py` lines 561–578

`class_roster.py` declares `_EXPECTED_TOTAL_CHAINS = 38` and includes an extended comment
block (25 lines) where rocket works through the arithmetic and concludes the correct count is
**32** (8 × 3 + 2 × 4 = 32). Despite reaching the correct conclusion in the comment,
`_EXPECTED_TOTAL_CHAINS` is set to 38 and is **never used in any assertion**. The constant is
dead weight that disagrees with both the comment and the math.

The doc 48 § 2.1 aggregate line reads: "Total chains: 30 (3×8) + 4 (4-chain Gunslinger) + 4
(4-chain Crusader) = 38 chains." The "30 (3×8)" is a doc 48 typographic error — 3×8 = 24, not
30 — which rocket correctly identified. The math-note `wave-1-5-class-chain-architecture-math.md`
§ 1 correctly states 32 total chains (8×3=24 + 2×4=8 = 32) and the dispatch header also
correctly states 38 total chains. So there is a discrepancy between math-note (32), dispatch
header (38), doc 48 § 0 aggregate (38), and the implementation comment conclusion (32).

**Root cause:** doc 48 § 0 TL;DR states "8 × 3-chain + 2 × 4-chain = 16 T4 capstones + 10
supporting chains" and does NOT state total chains = 38 there; the 38 figure appears only in §
2.1 where it is arithmetically inconsistent with 3×8 + 4 + 4 = 32. Dispatch header reproduces
the doc 48 § 2.1 figure uncritically.

**The functionally correct values are all asserted:** 10 classes, 8 3-chain, 2 4-chain, 22 T4
capstones, 10 supporting chains. D83 per-class enforcement runs correctly. The missing assertion
on total chains is the gap — but the _EXPECTED_TOTAL_CHAINS variable itself being 38 and unused
is the concrete problem.

**Action:** Rocket should:
(a) Fix the constant: `_EXPECTED_TOTAL_CHAINS = 32` (correct per 8×3 + 2×4)
(b) Add an assertion: `assert sum(e.chain_count for e in CLASS_ROSTER.values()) == 32`
(c) Clean up the 25-line comment block; replace with a 2-line note citing the doc 48 § 2.1
    typographic error and the correct count
(d) Note in math-note `wave-1-5-class-chain-architecture-math.md` § 1 that doc 48 § 2.1
    aggregate "38" has a typographic error; correct count is 32

This does NOT block Wave 1.5 close — the load-bearing assertions (D83, D66, per-class counts,
T4 capstone count, supporting chain count) are all correct. The 38 vs 32 discrepancy is a
documentation-arithmetic inconsistency, not a behavioral error.

**Cite:** Discipline #1 (math-before-code; math note should be internally consistent) +
Discipline #1.2 (code citations must match claims; doc 48 § 2.1 aggregate cited in dispatch
header does not match code implementation math) + Discipline #11 (empirical inspection —
rocket DID inspect this correctly in code comment but didn't close it cleanly)

---

### WARN-2 — `_total_supporting` assertion counts classes, not supporting chains

**Severity:** WARN
**File:** `class_roster.py` line 599

```python
_total_supporting = sum(1 for e in CLASS_ROSTER.values())  # one per class
```

This iterates over all entries and counts 1 for each — it always equals `len(CLASS_ROSTER)` (10)
regardless of whether any class has a supporting chain. It does NOT count chains with
`is_t4_eligible=False`. A correct implementation would be:

```python
_total_supporting = sum(
    1 for e in CLASS_ROSTER.values()
    for c in e.chains
    if not c.is_t4_eligible
)
```

The D83 per-class assertion (`len(t4_chains) == chain_count - 1` + `len(supporting_chains) == 1`)
in `ClassRosterEntry.__post_init__()` does enforce that each class has exactly one supporting
chain at construction time. So the functional invariant IS enforced — but the module-level
assertion on line 599 is vacuously true and does not test what its comment claims to test.

**Action:** Rocket should fix line 599 to iterate `c in e.chains if not c.is_t4_eligible` per
the pattern above. The assertion will remain a no-op in terms of blocking a bad state (since
`__post_init__` already catches it) but it should be correct for future archaeology and for
Discipline #11 (module-level empirical assertions should assert what they say they assert).

**Cite:** Discipline #11 (empirical inspection over assumption; the assertion looks empirical but
is vacuous)

---

### INFO-1 — Synthetic `_SyntheticPlayerClass` in `season_generation_pipeline.py` carries comments referencing `synthetic_mode=True` behavior (historical)

**Severity:** INFO
**File:** `season_generation_pipeline.py` lines 898, 901

Two inline comment lines read "Variance disabled via synthetic_mode=True in gauntlet_sim.py
(§ 10.4)" and "Cohort expectations with synthetic_mode (variance disabled)". These are
historical calibration comments for the now-retired synthetic_mode behavior. The
`_SyntheticPlayerClass` itself is a scout/calibration scaffold — it is NOT functional
synthetic_mode behavior (which was retired at Wave 0.5 per Discipline #39). `gauntlet_sim.py`
L427 confirms: "Discipline #39 (Cycle 14 Wave 0.5): synthetic_mode detection retired."

These comments predate Wave 1.5 and are not a Wave 1.5 Stage 3 artifact. They are stale
documentation carried forward. No behavior is gated on synthetic_mode in the current codebase.
No Discipline #39 violation.

**Action (optional):** Rocket may update the two comment lines in a future cleanup wave to read
"calibration scaffold for gauntlet integration (not synthetic_mode — see Discipline #39)" to
prevent future confusion. Not required for Wave 1.5 close.

**Cite:** Discipline #39 (synthetic_mode RETIRED ABSOLUTELY — confirmed clean in functional
code; stale comments only)

---

### INFO-2 — `bc_target_subspace_generator.py` L190 docstring says `default 22 = one per cell base enumeration` (stale after n_kits=40 change)

**Severity:** INFO
**File:** `bc_target_subspace_generator.py` line 190

The `generate()` docstring's `Args:` block reads: `n_kits: total kits to generate (default 22 =
one per cell base enumeration)`. The default was changed to 40 per doc 41 § 4.6. The docstring
was not updated. Functionally correct (line 173 `def generate(self, n_kits: int = 40)` is the
ground truth); documentation inconsistency only.

**Action (optional):** Update L190 to `n_kits: total kits to generate (default 40 per doc 41
§ 4.6 + doc 48 § 6.3 season cardinality amendment; one-per-cell base enumeration = 22)`.

**Cite:** Discipline #7 (capture decision telemetry; docstrings are part of the decision trace)

---

### INFO-3 — Discipline #25 (semantic-layer rep-audit) carry-forward: doc 48 § 2.2 names this as a Wave 5 obligation; no current-wave gap

**Severity:** INFO

Doc 48 § 2.2 states: "Discipline #25 (semantic-layer rep-audit) applied at firing time: when
rocket Stage 3 implementation reaches T3 supporting-chain skill emission, rep-audit the
substrate rows feeding the chain." The dispatch scope explicitly defers rep-audit to Wave 5
cohesion-judge pass. No Wave 1.5 gap. Recording for archaeology and to ensure Wave 5 dispatch
explicitly includes this obligation.

**Action:** KR includes rep-audit obligation in Wave 5 dispatch acceptance criteria.
No Wave 1.5 action required.

**Cite:** Discipline #25 (semantic-layer rep-audit required before semantic inheritance at any
downstream design surface)

---

## Empirical Verification Summary

| Verification item | Result |
|---|---|
| 10-class roster matches doc 48 § 1 verbatim | PASS — all 10 names case-match |
| 8 × 3-chain + 2 × 4-chain (module-load assertion) | PASS — asserted at import |
| 22 T4 capstones (D83 per-class + aggregate assertion) | PASS |
| 10 supporting chains (aggregate assertion — with WARN-2 caveat) | FUNCTIONALLY PASS (D83 per-class catches violation; module assertion is vacuous) |
| Supporting chain T3-cap enforced in emitter | PASS — `chain.tiers` returns `[1,2,3]` for `is_t4_eligible=False` |
| Assassin Shadow-Strike T2 branch (branch_a + branch_b) | PASS — `branch_node=2, branch_enabled=True` in registry; emission loop verified |
| 4-chain classes no branching in v1 | PASS — module-load assertion fires; `branch_enabled=False` on all Gunslinger + Crusader chains |
| active_t4_chain=None default (Q-W15-S3-1) | PASS — `bc_target_player_class.py:332` |
| 3 new fields in to_dict() | PASS — lines 456-458 verified |
| D66 validate() enforces active_t4_chain ∈ t4_chain_ids | PASS — lines 390-403 verified |
| n_kits=40 default at L173 | PASS |
| Multi-fire extension cap 50 preserved | PASS — Stage 2B check at L218 preserved |
| emit_skills_for_kit() backward compat preserved | PASS — separate function not modified |
| MIGRATION.md § Wave 1.5 authored (ADR-004) | PASS — section at L4632 verified |
| gamora null-safe note present in MIGRATION.md | PASS — L4711 verified |
| AGENT_STATE.md current | PASS |
| 232/232 regression tests PASS | CLAIMED; not empirically re-run by jack-ryan (Discipline #4 — regression runs are developer's gate, not reviewer's re-execution burden when smoke evidence is present) |
| synthetic_mode RETIRED ABSOLUTELY (Discipline #39) | PASS — functional code clean; comments are stale text only |
| Discipline #40 canonical-lock compliance | VERIFIED CLEAN |

---

## Verdict

**PASS-with-WARN**

Wave 1.5 fully closes. WARN-1 and WARN-2 are documentation/assertion-correctness issues that
do not affect behavioral correctness — all load-bearing assertions (D83, D66, T4 capstone
count, per-class chain counts) are empirically correct. WARN items should be addressed in the
next rocket seam-cleanup opportunity (Wave 2 or standalone within-seam fix); they do NOT gate
Wave 2 or Wave 3 firing.

**Wave 2 and Wave 3 fire from a clean structural foundation.**

---

## Action Items

- [ ] **Rocket (WARN-1):** Fix `_EXPECTED_TOTAL_CHAINS = 32` + add total-chain assertion +
  clean comment block + note in math-note § 1 that doc 48 § 2.1 "38" is typographic; doc
  48 § 0 TL;DR is correct. Address in Wave 2 scope or standalone seam-cleanup.
- [ ] **Rocket (WARN-2):** Fix `_total_supporting` assertion at `class_roster.py:599` to
  iterate chain objects, not class entries. Address with WARN-1 fix.
- [ ] **Rocket (INFO-1, optional):** Update stale synthetic_mode comments in
  `season_generation_pipeline.py` L898/L901 during next cleanup pass.
- [ ] **Rocket (INFO-2, optional):** Update `bc_target_subspace_generator.py` L190 docstring
  to reflect n_kits=40 default.
- [ ] **KR:** Include Discipline #25 rep-audit obligation in Wave 5 dispatch acceptance
  criteria (INFO-3).
- [ ] **Matt (if BLOCK or ESCALATE):** N/A — no BLOCKs; no escalation required.

---

## References

- `agentic_orchestration/dispatches/2026-05-27-rocket-cycle-14-wave-1-5-stage-3-skill-tree-architecture-impl.md`
- `canonical/48-cycle-14-class-roster-2026-05-27.md` § 0 + § 1 + § 2.1 + § 2.2 + § 2.3 + § 7
- `canonical/41-progression-framework-2026-05-27.md` § 4.6
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/class_roster.py` (full)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/per_skill_emitter.py` (§ 2B; lines 260-480)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/bc_target_player_class.py` (fields 326-341, to_dict 456-458, validate 390-403)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/bc_target_subspace_generator.py` (L173; L190; L218)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/MIGRATION.md` (§ Wave 1.5; L4632-L4748)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/AGENT_STATE.md` (§ Wave 1.5 Stage 3)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/math/wave-1-5-class-chain-architecture-math.md`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/math/wave-1-5-branching-math.md`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/generation/math/wave-1-5-active-t4-runtime-math.md`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/gauntlet_sim.py` (L427 — Discipline #39 retirement confirmation)
