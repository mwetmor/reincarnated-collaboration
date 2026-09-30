# Finding — 2026-09-29 — Run KC2-PLAY · T-A prereg v1.7 pre-read (DESIGN-MODE, before any graded result)

**Reviewer:** jack-ryan
**Severity:** **PASS** — 0 BLOCK · 1 WARN · 2 INFO
**Target:** `agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.7.md` @ collab `845f55d43` — FILE sha256 `552d9faecd83d955c77f2be35991ec51e3908d9f586ab70b5a78b6c156b92896` (derived before reading; matches the brief)
**Predecessor:** v1.6, sha256 `db2c0ca3c6cdba022b83d0229439a3ad9e0709cd25732304ffc979a200be7b0e` (derived; matches), unedited
**Developer:** gamora
**Principles applied:** REVIEW_PROCESS #4 (committed record as truth) · #5 (severity matters); Discipline #12 (semantic shift framed); CLAUDE.md mooted-escalation corollary

## What I found

**The one-change claim holds mechanically.** `diff -U0 v1.6 v1.7` = **36 hunks**, every one classified:

| class | hunks | notes |
|---|---:|---|
| header / § 0 front matter (title, status, § 0–0.5 block, authority, sequencing, author, not-edited, occasioned-by) | 12 | § 0 table carries exactly ONE row (`TA-X-06`) |
| § PINS re-derivation (paragraph, column heading, v1.6 + pre-read rows added) | 3 | no digest value changed |
| `⚑ v1.7` sites listed in § 0.2 (counts line, § A italic line, § B.3, § F.2 heading + disposition line + `TA-X-06` row, § F.2e ×5, § G ×4, § G.1, § H `H-5`, § I `OQ-1`) | 19 | each marked in place |
| footer (incl. one blank line) | 2 | — |

**Zero hunks outside those classes.** Everything not in a hunk is byte-identical to v1.6 by construction of the diff, so "nothing else moved" is established, not asserted. Specifically confirmed unchanged: § F.2e's six-point reasoning (v1.6 L802–827 untouched), § F.3 CLASS V's `TA-B-14` sentence (L1129), `TA-X-09` at 9 / `C-h` / `OQ-9` (GM-OQ-1 not folded), all other 28 EXACT rows.

**Authority verified at source:** charter ledger KP-110 records *"Q83(b) YES: TA-X-06 → UNGRADEABLE-declared, via prereg v1.7 committed ALONE before attempt 1"*; `matt_decision_needed/README.md` row Q83 marked (b) RULED. Commit `845f55d43` touches the prereg alone (D4).

**Counts:** 28 EXACT + 1 UNGRADEABLE-declared; the 28 are **enumerated by id** at § 0.1; PASS label reads `28/28`; Q85 counter `0 of 2` attached to v1.7 (no graded run exists under v1.6 — consistent with KP-106/107 HOLD).

**My v1.6 pre-read is carried as it stood.** Source pinned at sha `5a5f45d7…` (re-derived: matches). All 4 WARN + 3 INFO + the three OQ answers appear at § 0.5; WARN-1 / WARN-4 / INFO-2 correctly remain **grader obligations at emission**, not silently discharged. My preferred option (route Q83(b) before attempt 1) is recorded as the path taken, and the KP-105 pre-ruling escalation is given a one-line disposition — the corollary satisfied.

## Is the declared class closed at `TA-X-06`?

**Yes, in effect — by enumeration, not by an explicit closure sentence.** § G's new clause names `TA-X-06` only; § 0.1 fixes Q87's set as 28 ids by name; the PASS label hardcodes `28/28` and `TA-X-06`; § G retains *"No post-hoc widening, by anyone."* A grader who "declared" any other row would still owe it inside the enumerated 28, so it lands `INDETERMINATE` or `STRUCTURAL`, never `PASS`. No path to declare another EXACT row away exists in the text.

## WARN-1 · The closure is implicit; two surfaces read as an open class

§ G's clause is headed generically (*"A DECLARED ROW IS NOT AN UNGRADEABLE EXACT ROW"*), and the verdict-file field `declared_ungradeable` is an **array**. Neither admits a second member, but neither forbids one in terms. **Grader obligation at emission (no v1.8 required):** a verdict file is conforming only if `declared_ungradeable` is exactly `[TA-X-06]` with authority `Q83(b) / KP-110`; any other id there makes the file non-conforming. The declared class is `{TA-X-06}`, closed; a new member requires Matt's word and a new dated prereg version.

## INFO-1 · § 0.2 lists the header as "new"; it was also edited

Three header deletions are not individually `⚑`-marked: v1.6's *"v1.5 became legal only because Matt ruled it (KP-49 F4)…"* sentence, *"seat W2"* in the Author line, and v1.6's KP-83…KP-103 occasion list. All front matter; no row, count or verdict effect.

## INFO-2 · The occasion-list lineage claim is slightly overstated

The header says v1.6's occasion list is *"carried in § A as lineage"*; § A (L232–445) lacks KP-84, KP-88, KP-89. Lineage is not lost — v1.6 is pinned and unedited — but the pointer is imprecise.

## Action
- [ ] Grader (gamora, W3) — at emission: enforce WARN-1's conformance check on `declared_ungradeable`; carry v1.6 pre-read WARN-1 / WARN-4 / INFO-2 obligations as § 0.5 states.
- [ ] None for Matt. **W3 / graded attempt 1 is clear to fire against v1.7.**

## References
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.7.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-ta-prereg-v1.6.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/qa/findings/2026-09-29-run-KC2-PLAY-w2-prereg-v1.6-preread.md`
- `/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/gandalf/notes/2026-09-20-kc2-play-run-charter.md` (KP-110)
- `/Users/admin/Games/reincarnated-collaboration/canonical/matt_decision_needed/README.md` (row Q83)
