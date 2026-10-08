# Finding — 2026-10-08 — JOIN-1 J3d WARN-1 fix (`pct-resist-only` immunity), narrow delta

**Reviewer:** jack-ryan
**Severity:** INFO (verdict **GO**; `3eefaa2e` is the J3c pin)
**Target:** engine `156f09ec` (fail-first), `3eefaa2e` (rulebook), `3ce3c40f` (grids), `b2885503` (MIGRATION), `7df3721b` (N-6); collab `fc597ac7b`
**Developer:** gamora · conductor gandalf (KP-404/405)
**Principles applied:** 1, 2, 5 · Discipline #10. Read-only; no heavy runs (disk HALT).

## Checks
- **The diff is exact.** `git diff a8e11af6 3eefaa2e -- src/join2_rulebook` is only the `pct-resist-only` lines: `dr = res + bonus`; `if dr >= 100.0: return 0.0`; `max(0.0, raw − raw*dr/100)` if `dr > 0`, else raw. `kc2/**` has no diff.
- **The residues are gone.** I re-ran my 200,000-sample sweep on the committed function, extracted from `3eefaa2e`. At dr ∈ {100, 120}: **0 non-zero**. At dr ∈ {99.99999999999999, 99.9999999999999, 50, 0.5}: **0 negative**. The two named raws (3968.871…, 3304.079…) now give 0.0. dr = −20 gives raw (no amplification).
- **Certification holds.**
  - P-J2-9 `pass: true`.
  - GM 7/7, provenance `3eefaa2e`.
  - § 4.7 v4 BYTE-IDENTICAL at HEAD `3ce3c40f` with start = end. That commit differs from `3eefaa2e` only in the grid script.
  - The grids show `all_pass` at `3eefaa2e`, with L-07/08 rows 384 → 399. Fail-first `156f09ec` precedes the fix.
- **The ratification condition (`88819d4d`, clause 5) is MET.** `pct-resist-only` is **Active**, no longer conditional.

**INFO:** `dr` is no longer `min`-capped. That is behaviour-neutral, because the `≥ 100` branch covers every value the cap used to clip.

## References
- collab `agentic_orchestration/gamora/analyses/2026-10-08-join1-j3d-fix/` (README, `rulebook_diff_a8e11af6_3eefaa2e.patch`, `pj29.json`, `golden-master/`, `s47v4.stdout.txt`, `grids.json`)
