# Working note — 2026-08-08 — Vendor-corpus edition-pin discipline (decisions-log candidate)

**Agent:** jack-ryan
**Mode:** decisions-log entry authoring (per OP § mode selection)
**Commission:** gandalf (RUN-CONDUCTOR, KC2-SIM run, fold L-59), routing Matt directive
**Matt's arrow (verbatim):** "→ jack-ryan: decisions-log candidate."
**Status:** OPEN — filed at task start per FILE-EARLY mandate

---

## Task framing

Matt's T15 DepotDownloader sitting (2026-08-08) produced FINDING A (manifest-pin premise
validated bidirectionally) + FINDING B (edition-scoping consequence, ruled R-KC2-9), plus
context ruling R-T15-1 (pin drift ⇒ whole new edition tree, not a residual fetch).

Candidate shape handed to me (mine to sharpen or restructure):
1. vendor game-data corpora are EDITION-PINNED immutable trees — never updated in place
2. no-auth manifest diff (public PICS mirror) = standing drift tripwire pre-lap
3. changed manifests ⇒ new edition cut, never residual/hybrid (R-T15-1 precedent)
4. corpus-derived results are edition-scoped; carry forward only where record-granularity
   diff shows IDENTICAL

Evidence chain to cite:
- T7 cut record: `agentic_orchestration/gandalf/notes/2026-07-24-gd-edition-II-cut-record.md`
- KC2 ledger L-59 (+ L-55 consolidation lineage):
  `agentic_orchestration/gandalf/notes/2026-08-07-kc2-sim-run-ledger.md`
- matt_to_do DONE row: `canonical/matt_to_do/README.md`

Constraints: source-attribute substance to Matt; commit per auto-commit pattern; NO pushes.

---

## Log

### 14:2x — note filed, evidence read begins

Reading order: decisions-log (format + tail + any prior vendor-corpus entries) → T7 cut
record → KC2 ledger L-55/L-59 → matt_to_do DONE row → engineering-disciplines (which
disciplines this touches / whether a discipline amendment is also owed).

### Evidence read — what the chain actually says

- **T7 cut record § 3:** 11/11 IDENTICAL across unchanged manifests (base/gdx1/gdx2 +
  survivalmode/1/2). § 7 item 4 reads verbatim: *"Ratify the disposition ruling + the
  manifest-pin validation into decisions-log. — jack-ryan."* **That follow-up has been OPEN
  since 2026-07-24 (15 days).** This commission discharges it; the T15 sitting is what
  surfaced that it was never closed. Recorded as a self-observation.
- **T7 cut record § 5:** the Edition-I freeze claimed "All Text_EN.arc (5 files)" and it was
  5 of 6 — a case-sensitivity miss (`text_en.arc` lowercase). Named there as hazard D-a
  (coverage-boundary declaration). D-a / D-b are TRUE-SOURCES canon-change proposals; grep
  confirms **neither has landed in `engineering-disciplines.md`** — still proposals.
- **KC2 ledger L-59:** R-T15-1, R-KC2-9, R-L59-1 as briefed. L-55: G-STATS born (33rd gate).
- **`depot.pins.predicted.txt`** (inside the Edition-III tree) is the primary artifact: an
  8-row predicted manifest table, header declares *"REGISTERED BEFORE FETCH (prediction test,
  not description)"*, source = public PICS mirror `api.steamcmd.net/v1/info/219990`.
  Predicted drift: 7 of 8 CHANGED, 897671 (survivalmode2) alone unchanged.

### My own re-verification (Discipline #11 — do not take the claim, measure it)

**1. Pre-registration precedence is EVIDENCED, not merely asserted** (Discipline #68 § 1.3).
mtimes: `depot.pins.predicted.txt` 14:28:05 < earliest fetched archive `database.arz`
14:31:00. Corroborating, not proving (mtimes are mutable), but it is the check § 1.3 asks for
and it passes.

**2. Edition-II immutability — VERIFIED 5/5 by me, 15 days after the freeze.** Re-hashed the
five files the T7 cut record § 4 tabulated; all five SHA-256 match the record byte-for-byte
(`GDX3.arz` 1661be5e… · gdx3 `Text_EN.arc` d6e7f781… · `SurvivalMode3.arz` b4aa2d78… ·
survivalmode3 `Text_EN.arc` 6336cde2… · survivalmode2 `text_en.arc` 8269f89c…). The
never-update-in-place rule has held in practice, not just in policy.

**3. FINDING A is CORRECT — and its granularity needs naming.** I re-ran the full 16-file
shared-path hash diff II↔III myself:

| | files |
|---|---|
| DIFFER | 9 |
| IDENTICAL | 7 |
| absent in III | 0 |

At **`.arz` granularity** Matt's 7/7 and 1/1 reproduce exactly: the seven changed-manifest
depots each moved their `.arz`; survivalmode2's `.arz` is identical. **At FILE granularity the
mapping is not 1:1** — five files *inside changed-manifest depots* are byte-IDENTICAL across
editions: `gdx1/resources/Text_EN.arc`, `gdx2/resources/Text_EN.arc`,
`survivalmode1/resources/Text_EN.arc`, `mods/survivalmode/resources/Text_EN.arc`,
`survivalmode3/resources/Text_EN.arc`.

**The asymmetry this establishes (the load-bearing shape):**
- manifest **UNCHANGED** ⇒ *every* file in that depot identical — **13/13, zero
  counterexamples** (T7's 11 + T15's survivalmode2 pair). Safe to carry forward with no
  further checking.
- manifest **CHANGED** ⇒ at least one file in that depot moved, **but not necessarily the one
  you read** — 5 of 14 files in changed depots were identical. Must descend a granularity
  level before invalidating anything.

Consequence, immediate and free: the manifest diff alone would retire 14 of 16 Edition-II
files; the file-SHA diff retires 9. **Five Edition-II-derived rows carry forward MEASURED right
now**, no record-diff needed. A coarse-CHANGED verdict is *conservative* (never falsely says
"unchanged") but *costly* (discards good work). Over-invalidation is the mirror-image of the
D-a coverage hazard and it is the failure mode clause (iv) has to prevent.

### Catches to fold into the entry

- **C-1 (WARN, naming): "Edition-<N>" is now overloaded inside this same log.** The Atlas MCA
  basis uses Edition-I (frozen 2026-07-14, log line 5623) / Edition-II (candidate); the GD
  vendor corpus uses Edition-I/II/III. Both are Roman-numeral, both mean "frozen basis behind
  an evidence gate". A future grep for "Edition-II" returns both. → RIDER-1: qualify in prose
  (`GD-Edition-<N>` vs `Atlas Edition <N>`); **do NOT rename the on-disk directories** — a
  directory name IS the pin, and renaming a pin is precisely the Discipline #67 hazard.
- **C-2 (INFO, mirror trust is asymmetric).** The PICS mirror is a third-party read of Valve's
  PICS. 8/8 agreement was measured once, on 8 depots. → RIDER-2: mirror-says-DRIFT is
  actionable immediately (gate the lap); mirror-says-NO-DRIFT is good enough to continue a
  routine lap but NOT to cut or certify a frozen edition (that needs the credentialed read);
  mirror unreachable ⇒ the check is **NOT-RUN**, never "no drift" (Discipline #63,
  unmeasured-is-not-zero, applies verbatim).
- **C-3 (evidence, founding instance for "never in place").** Queue row T12 as written
  instructed a fetch of `Levels.arc` *into the Edition-II tree*. The pre-fetch gate is what
  stopped it; the matt_to_do DONE row now carries "NOTE the pin moved". A live queue row asked
  for the violation. That is the discipline's founding instance, not a hypothetical.

### Disposition

Land as a **full ACTIVE entry**, not a candidate. Rationale: R-T15-1 and R-KC2-9 are
Matt-made, Matt-tier, already ruled — I am recording, not ruling. The generalization into
standing discipline is process/documentation-tier ⇒ ADR-002 jack-ryan direct authority,
Matt-veto-open. RIDER-1 + RIDER-2 marked jack-ryan-tier, veto-open. Discipline **#69 QUEUED**
(not minted) with a named landing trigger — the legolas II→III record-diff verdict supplies
the record-granularity founding instance; per the #60 reconciliation precedent a queued
candidate holds **no number reservation**.

### Landed

Entry written to `~/Games/reincarnated-engine/design/decisions/decisions-log.md`, inserted
immediately before `## Decisions to revisit`. Committed in the engine repo. NO push (both
repos push on Matt's word only).
