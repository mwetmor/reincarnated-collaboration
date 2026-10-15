# Finding — 2026-10-15 — JOIN-1 J4b ADDENDUM-13 CORRIGENDUM-3 (delta on my CORR-2 delta `1a0b6ccc1`)

**Reviewer:** jack-ryan
**Severity:** WARN (verdict: GO-WITH-AMENDMENTS; 2 WARN / 2 INFO)
**Target:** engine `afadd23d` (CORR-3); forms `b537d81c` / `4a21b418` → laws `55ce3bec`, locks `28beb665`, grader `931ecf43`; tapes `6f300c60` → `4e6ed5b3`; contact table `a8cda203` / `d52dd775`
**Developer:** gamora (the mirror booking lines belong to drax, godot `8ce6036`)
**Principles applied:** REVIEW_PROCESS 1, 2, 3; Disciplines #8, #10; KP-312; KP-439 R-(a)

## What I found
- **My CORR-2 WARN-1 (i)–(vii) is folded in full in § 1:**
  - the operand is the guarded records, with killing blows included;
  - pre-cap `d` equals GO `offered` bit-for-bit (`applied` is the clamped value);
  - the state is mirror-side;
  - the HOOK row text is fixed;
  - GH carries `seq`.
- INFO-1 (L-02 and L-07 key to `eyeofreckoning1`) and INFO-2 (the gethit replay halt, now in the grader) are folded too.
- drax's rulings (a)–(d) are consistent with the law.
- I re-ran forms12 + locks + grade: **102/102**. The oracle tree is clean.

## Answer to the ⚑ question — (e) and KP-439
**It falls under KP-439's conditional consent, but the condition is NOT yet met.**
- **Why it is in scope:**
  - The booking is J4b booking code.
  - It adds **no sealed line**: it is in the out-of-tree mirror, `kc2_play/join/rulebook/kc2rb_d2lane.gd`, which has **8 `f._cons_add("dropped", …)` lines** (:1281, 1293, 1295, 1299, 1329, 1334, 1344, 1346; first at godot `8ce6036`).
  - It calls an **existing** member with an **existing** census key (`dropped`, census rows at :4067 and :4852).
  - It is inert under null (the mirror is not installed).
  - So no site ruling and no second Matt ruling is needed.
- **Why the condition is not met:** `kc2rt_census_grep.py` greps only `kc2_runtime/sim/kc2rt_fight.gd`, and only for `^\s*(_cons_add\("|_offer\()`. It **cannot see** an `f._cons_add(` call in the mirror. "census_grep MATCH 43/55" at `4e93fa7` therefore says nothing about these 8 lines. This is the same failure shape as the instrument-domain cases in CLAUDE.md: an instrument that returns cleanly about a domain it cannot see.
- This finding is the **named finding** for the 8 lines at `8ce6036`.

## WARN-1 — discharge the census condition (drax / gamora)
Three things are needed:
1. **A mirror census enumeration.** Extend `census_grep` or add a companion over `kc2_play/join/**`, matching `\b_cons_add\(|\b_offer\(` against a pinned list (8 lines). It must exit 1 on any difference and have a fail-first control: a planted call must be caught.
2. **Conservation closes with no double booking on her arm, per cell.** Σ the registered DoT totals (sealed `_dot_register`) must equal Σ landed via `_land` + Σ mirror `dropped`, within the Kahan tolerance. The mirror `dropped` subtotal is printed separately from a mirror counter, so **no new key** is added.
3. Both must be **at the pinned runtime digest, before the graded run depends on them.**

## WARN-2 — the dying-slot exclusion is sound in law and label-trusting in code
- **The law is sound.** A death-triggered skill fired at the kill is not an action of a living locked body, and D2 fires it regardless of mode. Gate (b) is unaffected, and the count is reported.
- **The code trusts the label.** `931ecf43` excludes any G1 row with `slot == "dying"` without checking when it fired. A mislabelled slot would therefore hide a real gate (a) violation.
- **Fix:** every excluded row's tick must equal its attacker's death or removal tick (GB `off_tick`, or a death grain), with a stated phase tolerance. Any mismatch is a HALT.
- **Counts:** CORR-3 § 3 quotes 14/40 (from `dcebb054`). At `fb49080f`, drax reports **11/42**. Cite the digest when quoting.

## INFO
- **INFO-1, replay completeness.** `gethit_replay` checks each GH row but not completeness. Add three checks:
  - per-body `seq` contiguous from 0 (a gap is a silent missing record);
  - per-stream `draw_index` contiguous and non-duplicated;
  - the record count reconciled against the decision count. KP-456 prints records 8,369 against decisions 8,368, so the remainder must be named, e.g. a terminal-tick record whose k+1 never runs.
- **INFO-2.** (a)–(d), the contact-table FORM (`DEFAULT_SKILL` → `(True,"swing")` after `apply_default`), the tape gate `n_no_tape == 0 AND n_mismatch == 0`, the crit tapes and the J4B-ROWS contract are consistent. I have no remarks on them.

## Action
- [ ] drax: the mirror census enumeration with its fail-first control (WARN-1 item 1).
- [ ] gamora: the conservation identity print (WARN-1 item 2); the death-tick check on dying rows (WARN-2); the completeness checks (INFO-1).
- [ ] Matt: none. This is inside KP-439 once WARN-1 is discharged.

## References
- `reincarnated-engine/src/reincarnated/simulation/math/join1-j4b-d2-adapter-fire-sorc-design-2026-10-14-ADDENDUM-13-CORRIGENDUM-3.md`
- `reincarnated-engine/src/reincarnated/simulation/scripts/gamora_join4b_grade.py` (`931ecf43`)
- `reincarnated-godot/kc2_play/join/rulebook/kc2rb_d2lane.gd`; `reincarnated-godot/kc2_runtime/tools/kc2rt_census_grep.py`
- `agentic_orchestration/gandalf/notes/2026-10-14-j4b-kp312-port-site-ruling-sheet.md` § (a); charter rows KP-439, KP-455, KP-456
