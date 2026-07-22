# Aware-Fighter Ablation Gate — Execution Charter (named-gamora)

**Author:** gandalf `RUN-CONDUCTOR`, 2026-07-22. **Executor:** named gamora (simulation seam).
**Authority:** the **FROZEN** prereg sheet
`agentic_orchestration/gandalf/notes/2026-07-22-aware-fighter-ablation-prereg.md` (L-27 pins;
jack-ryan check `a9bb1886` + freeze-beat re-verify `57d18520`; ledger L-28). **The sheet GOVERNS.**
This charter is operational sequencing only — on ANY conflict or ambiguity between charter and
sheet: **HALT and report to conductor. Do not improvise.** Post-freeze sheet edits void the gate
(nobody edits it, including you).

## 0. Read first

1. The frozen sheet, §1–§8 — the spec. Nothing here overrides it.
2. jack-ryan finding `agentic_orchestration/qa/findings/2026-07-22-prereg-check-aware-fighter-ablation.md`
   — especially the C2 seal-artifact shape and the C3/C4 result-read riders.
3. Your own lineage: `agentic_orchestration/gamora/notes/2026-07-22-aware-fighter-bw1-equivalence-battery.py`
   (frame cell/seed/parity logic) + BW-1.1 slice report + math addendum.
4. W3′ seal precedent: `agentic_orchestration/gamora/notes/2026-07-22-tier3-w3prime-pregate-seal.json`.

## 1. Preconditions (attest both in your report)

- `git -C ~/Games/reincarnated-engine rev-parse --short HEAD` == **`2f43045`**, working tree CLEAN.
  Engine is FROZEN this run: **zero engine edits** (§7 pin 8: engine diff seal→verdict = ∅).
- **Site-coverage attestation** (§7 pin 5): restate that `_policy_choose_target` is the ONLY player
  target-choice source at this hash (primary site + both E4 sites; your BW-1.1 tests prove it).

## 2. Runner (instrument code in collab notes — NOT engine source)

New runner `agentic_orchestration/gamora/notes/2026-07-22-aware-fighter-ablation-runner.py`,
extending the battery harness's frame logic (same selection→formation→scenario machinery):

- **Frame:** W3′ 32 cells × seeds **{20260722, 20260723, 20260724, 20260725}** × BOTH compositions
  (encounter + matched_baseline) = 256 fights per policy arm; **512 total**.
- **Arms:** BLIND = `BLIND_CONFIG` · AWARE = `AWARE_CANDIDATE_CONFIG` **verbatim** (6 entries, all
  weights 1.0 — NO weight edits; §3 frozen).
- **Both arms:** `player_gather_primitive` OFF · decision traces ON · sequential fights (Disc #3).
- **Capture per fight:** `player_damage_taken` (PRIMARY intake) · duration ticks (SECONDARY time) ·
  all-mobs-killed boolean (clear guard) · the standard triple (continuity) · trace length.

## 3. Execution order — the C2 seal is LOAD-BEARING

1. **SMOKE** (§7 pin 2): 1 cell × both arms × 4 seeds. Sanity-check every captured field is live
   and plausible. HALT on anomaly.
2. **BLIND arm COMPLETE** — all 256 fights, both compositions.
3. **SEAL** (§2 as amended): write the seal-JSON = 256 blind per-fight records + encounter-arm
   aggregate-per-seed means + `SD_seed` (`statistics.stdev`, n−1, 3 df — the SAME estimator the
   check verified). **FLUSH TO DISK before ANY aware fight.** Record the file md5.
4. **AWARE arm COMPLETE** — 256 fights.
5. **Verdict-input JSON:** re-read the seal file; verify md5 unchanged (**mismatch ⇒ red-flag HALT,
   no verdict**); embed the seal md5; evaluate the frozen predicates mechanically:
   - `Ī_blind`, `Ī_aware` (encounter-arm mean per-fight intake) · `M_rel = (Ī_blind − Ī_aware)/Ī_blind`
   - **D2:** `M_rel ≥ 0.10` → bool
   - **D3:** `(Ī_blind − Ī_aware) ≥ 2 × SD_seed` → bool (+ degenerate-guard note if `SD_seed == 0`)
   - **Clear guard:** per (cell, seed, composition) clear-outcome match blind-vs-aware; list every
     mismatch (cell id + direction)
   - **Specificity:** matched-baseline `M_rel`; flag if baseline margin > ½ × encounter margin
   - **Time:** encounter-arm aggregate duration, both arms; flag if AWARE >5% slower
   - **C4 rider:** realized intake-determinism profile (per-cell intake seed-SD zero-counts, both
     arms × both compositions) + pooled per-cell seed-SD (reported diagnostic, §5)
   - Per-cell intake deltas + sign counts (§5 reporting shape)

## 4. Artifacts + report discipline

- **Commit** (stage by explicit path; `git -C /Users/admin/Games/reincarnated-collaboration`;
  **commit-never-push** — conductor pushes): runner + seal JSON + verdict-input JSON + slice report
  (as-built, Discipline #11 deviations disclosed). Full traces regenerable-not-committed (BW-1
  precedent).
- corpus.db READ-ONLY · no telemetry-schema changes · no seed additions · no engine edits.
- **Report back:** attestations · smoke result · headline numbers (`Ī_blind`, `Ī_aware`, `M_rel`,
  `SD_seed`, D2/D3 bools, clear-guard list, specificity read, time flag, determinism profile) ·
  deviations · artifact paths + commit hash. **Report predicate FACTS only — the VERDICT
  (PASS/FAIL/PARTIAL) is the conductor's DRIFT-CRITIC synthesis against the frozen sheet + Matt's
  ruling. Do not caption your report with a verdict word.**

**Signed:** gandalf (`RUN-CONDUCTOR`), 2026-07-22 — veto-open.
