# DISPATCH — gamora: GD 40-state coverage audit (G1-A)

**From:** gandalf (SPEC-AUTHOR), Matt-directed 2026-07-25 (*"Draft and fire the gamora audit"*)
**To:** gamora
**Type:** ANALYSIS / AUDIT — findings only. **No production code. No sim changes.**
**Gate:** none triggered (read-only audit); output feeds future Gate-1 design work.

---

## 1. Why

Matt's three-goal frame (`agentic_orchestration/skill_handoff_2026-07-25.md` § 0): goal 1 is
*"ensure all of GD's combat mechanisms exist in our battle sim."* The 40-entry
`ControllerMonster` state table is now the **exhaustive** vocabulary of what a GD monster can
do (verified in `Game.dll`, count exact). What does NOT exist is the comparison against our
sim — every "we don't model this" claim in circulation is **provisional and hand-triaged by
gandalf, who did not read your seam's code to make it**. The hand-off § 4.1 states plainly:
*"no number in it should be quoted until she has run it."* This dispatch is that run.

Downstream consumers: the G1-A coverage matrix gates the constraint-ladder rungs (§ 2.3), the
per-family design specs (gandalf), and the eventual L0-CLOSE run charter
(`agentic_orchestration/gandalf/notes/2026-07-25-gd-three-goal-end-state-and-twin-analysis.md` § 5).

## 2. Substrate (read these)

| Input | Path |
|---|---|
| The 40-state table (authoritative; includes RTTI evidence) | `research/knowledge/gd/2026-07-25-gd-ai-state-tables-complete.md` |
| gandalf's provisional triage — **audit target, NOT ground truth** | `agentic_orchestration/skill_handoff_2026-07-25.md` § 4.1 |
| The 7 mechanism families clustering | same, § 4.1 table |
| Existing 5-KPI gap register (to be expanded) | `agentic_orchestration/gamora/notes/2026-07-24-tsf6-track-a-run.md` § 3 |
| Your seam's code | `~/Games/reincarnated-engine/src/reincarnated/simulation/` (+ `spirit_guide/` where adjacent) |

## 3. The task

**For each of the 40 states**, classify against our battle sim:

- **`MODELLED`** — our sim has an equivalent construct. **NAME IT: file + symbol + line.**
  Equivalence means the *transition semantics* exist (entry trigger, exit trigger, parameter
  binding), not that a similarly-named string appears.
- **`PARTIAL`** — some semantics exist; state exactly which half is missing.
- **`ABSENT`** — no construct. **Evidence of absence required:** name what you searched
  (modules, symbols, grep terms) so the claim is checkable.
- **`PROPOSED-OUT`** — non-combat (quest/cosmetic) candidates. **Do not rule scope** — G1-B
  scope is Matt's ruling, queued to ride the next grill session. Mark and move on.

Then: **expand the gap register from 5 KPIs to the 7 mechanism families** (+ the two loose
items: `NavigateObstacle`, `UseSkillOnPoint`/`UseSkillOnAlly`), preserving the existing KPI
numbering as cross-references.

## 4. Disciplines in force

- **Empirical inspection over assumption** — read the code, cite file:line. gandalf's triage
  guessed ~12 modelled / ~18 absent; if your audit agrees exactly, be suspicious of anchoring.
- **Bank vs route** (§ 8.2 of the hand-off) — anything you infer rather than verify is
  LABELLED as inference. Five banked-inference failures this week; do not add a sixth.
- **Findings only** — no code changes, no TODO edits in engine files, no fixes-while-here.
- Auto-commit your report per team commit discipline (this dispatch is your authorization).

## 5. Output

`agentic_orchestration/gamora/notes/2026-07-25-gd-40-state-coverage-audit.md`:

1. The 40-row matrix (state · classification · sim construct file:line or absence evidence · notes)
2. Per-family rollup (7 families + 2 loose items) with the corrected modelled/partial/absent counts
3. Expanded gap register section (5 KPIs → 7 families, cross-referenced)
4. Anything the audit surfaces that the triage missed entirely (states misassigned to families, etc.)
5. A ≤10-line summary block at top: the corrected headline counts + the single most
   consequential divergence from the provisional triage

**Signed:** gandalf, 2026-07-25
