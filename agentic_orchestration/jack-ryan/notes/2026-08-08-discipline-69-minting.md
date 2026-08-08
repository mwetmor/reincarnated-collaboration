# Working note — 2026-08-08 — Discipline minting: edition-pinned corpus carry-forward

**Author:** jack-ryan
**Status:** CLOSED — Disciplines #69 / #70 / #71 minted (see § 6)
**Filed:** 2026-08-08, before drafting (FILE-EARLY, mandatory per commission)
**Commission:** gandalf (RUN-CONDUCTOR), KC2-SIM autonomous run, fold L-61(d)
**Run ledger:** `agentic_orchestration/gandalf/notes/2026-08-07-kc2-sim-run-ledger.md` rows L-60 / L-61
**Authority:** ADR-002 process/documentation tier, Matt-veto-open (same basis as L-60 entry disposition)
**Seam:** `~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`

---

## 1. Why this note exists

At L-60 I QUEUED a discipline candidate rather than minting it, and named an explicit
landing trigger:

> "the legolas II→III record-diff verdict supplies the record-granularity founding instance"

Predecessor note: `agentic_orchestration/jack-ryan/notes/2026-08-08-manifest-pin-decision-candidate.md`
Decisions-log entry: engine `8256dca4`

The commission asserts the trigger has FIRED via
`agentic_orchestration/legolas/notes/2026-08-08-kc2-edition-III-intake-and-diff.md`
(meta `65cf3016`) plus instruments at
`agentic_orchestration/legolas/scratch/2026-08-08-kc2-ed3-diff/`.

## 2. Work plan (in order)

1. FILE-EARLY this note (done).
2. Re-read my own L-60 note — recover the exact queued candidate substance and the
   clause (iv) text the conductor's R-L61-1 ruling leans on.
3. **Verify the trigger myself** — Discipline #11 (empirical inspection over assumption).
   Do NOT take the commission summary at face value. Independently confirm:
   - the 84,663 / 83,605 / 1,058 / 166 / 0 record counts from the instruments;
   - the KC2-dependent-set 100%-identical claim;
   - the a.7 9-DIFFER / 7-IDENTICAL vs "8/8" header discrepancy (majority-of-independent-
     measurement question — does it touch the founding-instance chain?);
   - the template-layer 811/819 + 8-additive claim.
4. Number assignment: read the disciplines file, find the next ACTUALLY-FREE number,
   verify no collision (the #60 reconciliation precedent — number assigned at landing,
   not at queueing).
5. Draft + mint the discipline.
6. Decide the D-a / D-b TRUE-SOURCES ride-along question (flagged at my own L-60(g)).
7. Commit in touched repos. NO push (conductor centralizes per R-KC2-10).

## 3. Open questions at file time

- **Q1** — Is the a.7 header/table discrepancy material to the founding-instance chain,
  or is it an isolated reporting defect already routed to legolas at L-61(i)? If material,
  the mint may need to narrow its founding-instance citation.
- **Q2** — Next free discipline number. Commission says "#69" as the queued label but
  explicitly directs number-at-landing. Must verify against the actual file.
- **Q3** — D-a / D-b TRUE-SOURCES ride-along: same touch, or separate? My call.
- **Q4** — Does the asymmetric direction rule (CHANGED ⇒ descend before invalidating)
  need an explicit stop-condition, or does "descend one level" bottom out naturally at
  record grain?

## 4. Findings

### 4.1 Trigger verification — I re-measured every limb rather than taking the summary (#11)

| limb | commission claim | my independent result | verdict |
|---|---|---|---|
| record counts | 84,663 / 83,605 / 1,058 / 166 / 0 | re-read from `fulldiff_summary.json`; 83,605 + 1,058 = 84,663 ✓ | CONFIRMED |
| file-SHA diff | (mine, L-60) 9 DIFFER / 7 IDENTICAL | re-hashed all 16 shared files from the two trees | CONFIRMED — reproduces exactly |
| KC2 set | 100 % identical | re-read `kc2set_verdicts.json`: 607 IDENTICAL / 5 CHANGED / 15 ABSENT-BOTH | CONFIRMED with caveats — see 4.2 |
| proto bios | 808/808 | recomputed from the overlay index: 808 in III, 808 shared, 0 changed | CONFIRMED |
| tier-16 tables | 55/55 | 54 wave proxies + 1 spawn entity, all IDENTICAL | CONFIRMED |
| template layer | 811/819, 8 additive | `tpl_changed.json` lists exactly 8; note tabulates each as additive | CONFIRMED |
| manifest grain | T7 11/11 + T15 8/8 | read both records; T15's 8/8 is the *prediction* test, of which depot 897671 is the unchanged-manifest limb | CONFIRMED, with the distinction below |

**Sharpening on the manifest limb.** "T7 11/11 + T15 8/8" conflates two different tests. T7's
11/11 is *manifest-unchanged ⇒ bytes-identical* at 11 files. T15's 8/8 is *pre-registered manifest
prediction confirmed on disk* (a #1.3 pre-registration test), of which only depot 897671 was
predicted unchanged — contributing **2** files to the unchanged-manifest evidence. The correct
statement of the manifest-grain founding evidence is **13/13 (T7's 11 + survivalmode2's pair),
zero counterexamples**, which is what my L-60 note already said and what #69 now records.

### 4.2 Two divergences between the commission summary and the committed instrument

Both resolve in the note's favour; neither weakens the founding instance. Recorded because a
summary that is right for the wrong reason is still a #11 hazard.

1. **"15/15 summon bodies."** The committed `kc2set_verdicts.json` shows **13 IDENTICAL + 2
   `ABSENT-BOTH`** (`fleshshaper_spirit_01`, `krieg_aethertrap`). The note's path-resolution
   honesty note covers set (5), not set (2b). I re-resolved both by corpus search: they live at
   `records/skills/nonplayerskillsgdx1/bossskills/pets/` and are **both IDENTICAL**. **The note's
   15/15 is correct; the committed artifact is stale.** Logged as **#70 founding instance 4** —
   an artifact's declared coverage decays independently of the prose citing it. INFO, no substance
   moves, no re-run commissioned.
2. **"3/3 survivalmode scalar arrays."** The instrument's group (3) is **21 records, 19 IDENTICAL
   / 2 CHANGED** — the 2 changed (`mp+difficulty_enemies01`, `ultramode_enemies01`) are **not**
   survivalmode records. The note states this correctly at b.1/b.3; the commission's compression
   to "3/3" is accurate but drops the containing population. Not an error, but it is exactly the
   shape #70 governs, so it is named.

### 4.3 The a.7 count — settled by majority of independent measurement

legolas's a.7 **header** says "8 CHANGED / 8 IDENTICAL"; his **closing prose** says "It is 8 of 16."
Both are wrong against **his own table**, which resolves to 7 `.arz` + 2 `.arc` = **9 CHANGED** and
1 + 6 = **7 IDENTICAL**. The error appears **twice**, not once — worth noting for the corrigendum
scope, since fixing only the header leaves the prose wrong. Three independent measurements now
agree on 9/7: my L-60 diff, my re-hash today, and his own table. Propagation checked by grep across
`agentic_orchestration/`: the run ledger quotes the **table**, not the header, and L-61(i) already
carries the flag. **No downstream consumer read the header count — CONFIRMED.** Corrigendum stays
routed to legolas at L-61(i)/R-L61-3; I did not touch his note.

### 4.4 The cost number — the discipline's justification, measured

Of the 612 KC2-dependent records, **552 (90.2 %) are owned exclusively by archives that CHANGED at
file grain.** A manifest- or file-grain stop would have invalidated the whole KC2 fixture substrate.
Every one of those records is byte-identical at record grain. This is the number #69 exists to
prevent paying, and it is now measured rather than argued.

### 4.5 The equality predicate — a subtlety worth naming in the discipline

`lib2.diff_rec` returns `IDENTICAL` **and** `IDENTICAL-FIELDS` (owner-stack moved, merged fields
equal), and `fulldiff.py` folds both into the identical count via `startswith("IDENTICAL")`. I
measured the split: **83,604 IDENTICAL / 1 IDENTICAL-FIELDS**
(`records/sounds/items/weaponattacks/spak_crossbow1h_shot.dbr`). The fold is **correct for a
consumption claim** and would be **wrong for a provenance claim**. Magnitude is negligible; the
principle is not, so #69 requires the predicate be named at the verdict site (#64).

### 4.6 Number assignment

Max landed discipline is **#68**; **#58** is intentionally vacant (DECLINED as redundant with #53).
Grepped both repos for `Discipline #69` — the **only** hit was my own QUEUED note in the
decisions-log. **#69 / #70 / #71 all verified free.** Post-write duplicate check on `^### N.`
headings returns clean.

## 5. Answers to the open questions

- **Q1 (a.7 discrepancy material?)** — **No.** It is a roll-up slip in a summary line; the table,
  the two component statements, and three independent measurements all agree at 9/7. It does not
  touch the founding-instance chain. Already routed; I added only the observation that it recurs
  twice in the section.
- **Q2 (next free number)** — **#69**, verified. #70 / #71 taken by the ride-along.
- **Q3 (D-a / D-b ride-along)** — **THEY RIDE.** This is the substantive call of the touch, and it
  reversed on evidence: my file-time instinct was that ratifying a separate proposal would be scope
  creep. It is not. **Matt ruled REFRAME on 2026-07-24** (`AGENTS.md` § known/unknown split), the
  proposal's § 7 chain is *gandalf proposes → Matt rules scope → jack-ryan ratifies*, and
  `skill_handoff_2026-07-25.md` line 395 assigns the ratification to me **by name**. It is an owed
  obligation open 15 days — the same latency and the same discovery path as the T7 § 7 item 4 I
  discharged at L-60. Decisive secondary reason: **#69's own body cites D-a as its mirror hazard**,
  so minting #69 alone would leave a load-bearing cross-reference dangling at an unlanded
  discipline. **§ 5c (TSR-4 coverage tier) does NOT ride** — it is an architecture change the
  proposal itself assigns to elrond; I ratified the *requirement* into #70's statement block and
  ROUTED the design, recorded explicitly so the REFRAME ruling's third limb is not dropped.
- **Q4 (stop-condition on the descent)** — needed, and added. "Descend one level" without a floor
  invites descending past the claim. #69 states: **the descent bottoms out where the consumer
  reads** — record-level claims descend to records, single-field claims to that field, and
  descending further than the claim needs is waste, not rigor.

## 6. Disposition

**MINTED — three disciplines, one touch.** All in
`~/Games/reincarnated-engine/design/working-agreement/engineering-disciplines.md`:

- **#69** Edition-pinned corpus carry-forward (7 founding instances; the commissioned one)
- **#70** Coverage-boundary declaration — D-a (4 founding instances; discharges REFRAME § 5b)
- **#71** Join validation before contradiction — D-b (3 founding instances; discharges REFRAME § 5b)

Anatomy-of-this-document entry added per the file's own "How to extend" step 3. Decisions-log
updated per step 5: the L-60 entry **annotated** at its Status line (original text left standing —
no silent self-healing) plus a **new minting entry**. Authority: ADR-002 process/documentation
tier, **Matt-veto open on all three**; #70/#71 substance is gandalf's under Matt's ruling and is
attributed in each header.

**Not done, deliberately:** no push (R-KC2-10, conductor centralizes); no edit to legolas's note
(his corrigendum, routed at L-61(i)); no re-run of the stale `kc2set_verdicts.json` (logged as
evidence, not a defect to repair); TSR-4 design ROUTED to elrond, not designed here.

**Status: CLOSED.**
