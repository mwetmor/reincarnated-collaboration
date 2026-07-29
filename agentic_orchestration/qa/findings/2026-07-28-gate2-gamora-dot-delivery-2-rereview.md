# Finding — 2026-07-28 — gamora DoT tick-delivery, C-1..C-7 re-review (R-KC1-25 amendment lap)

**Reviewer:** jack-ryan (DEV-MODE, Gate 2, re-review)
**Severity:** **CONDITIONAL PASS** — the BLOCK is **LIFTED**. Two WARN residuals, three INFO.
**Target:** engine commits `67e7ccb` (kernel + tests + math-note §10-§11) and `2be600f`
(`_fix3` batteries), tag **`gamora/v-dot-delivery-2`**, `origin/main`
**Developer:** gamora (simulation seam)
**Run:** KIT-CAL-1 / KC1-2026-07-27, ratified repair R-KC1-25, ruling R-KC1-25
**Supersedes on verdict:** `2026-07-28-gate2-gamora-dot-tick-delivery-r-kc1-25.md` (BLOCK)
**Principles applied:** 1 (math-before-code), 2 (smoke-gate), 3 (cross-seam impact), 5 (severity)
**Disciplines cited:** #1, #2, #3, #9, #11, #12

---

## §0 — Verdict in one line

She **rejected the letter of my C-1 and was right to**; the substitute satisfies C-1's intent
strictly better, I reproduced both her rejection measurement and her repair grid on my own harness,
**all 33 headline cells and all 450 trace files are byte-identical `_fix2` → `_fix3` (0 moved,
Matt escalation does NOT fire)**, and my own §3.2 prose was transposed — her correction stands.
**BLOCK lifted. `gamora/v-dot-delivery-2` is the terminal battery stack for the amendment lap.**

---

## §1 — THE CENTRAL ADJUDICATION: was she right to reject C-1's letter?

**Yes. Independently reproduced, and the rejection is the stronger engineering call.**

I did not take her word for it. I built the literal C-1 repair myself — a detached worktree at
`3aa4a55`, patched so that `S' = round(D'/Δ)` (no `+ phase`), the carried phase held in a separate
field, and pulse *k* firing at `e ≥ ⌈k·S'/P'⌉ − phase`. That is exactly what my C-1 asked for:
first interval shortened by the full phase, inter-pulse spacing untouched. Measured on my own
sustained-refresh harness (production `_add_or_refresh` writer, 120 s, `tick_damage = 10.0/s`):

| kernel | D ∈ {2,3,4,5}, Δ=0.1 | D=6.37, Δ=0.1 | D=6.37, Δ=0.5 (smoke grain) |
|---|---|---|---|
| pre-fix `7483a21` | 0.9917 | 0.9917 | 1.0000 |
| v1 `3aa4a55` | 0.550–1.000, cadence-dependent | 0.814–0.885 | 0.7078 |
| **V2a — MY C-1, literal** | 1.0000 | **0.9643** | **0.7078** |
| **V2b — shipped `67e7ccb`** | **1.0000** | **0.99974** | **0.99974** |

**Her two numbers reproduce to four decimals on my independent implementation** (she reported
0.964347 / 0.707778; I read 0.9643 / 0.7078). Her mechanism is also correct: a refresh restarts the
grid at `k = 0`, so the effect only ever traverses interval #1 `= ⌈S/P⌉`, systematically the longest
of the `P` intervals, and the steady-state rate is short by the ceiling defect of `S/P` — which
depends on `Δ` as well as `D`.

**That Δ-dependence is dispositive.** V2a would have made the smoke arm (Δ=0.5) and the full arm
(Δ=0.1) measure sustained DoT totals 26 points apart — **the same Discipline-#2 structural blindness
my BLOCK was written to remove, relocated one order down.** My C-1 named the right defect and
prescribed a remedy that reproduced the defect class at smaller amplitude. She was right not to ship
it, and right to say "one order smaller is not the standard" — that is my own §7 reasoning turned
correctly back on me.

**Does V2b satisfy C-1's INTENT?** C-1's intent was uniform declared-rate delivery under sustained
refresh, predictable from the declaration alone. V2b satisfies it strictly:

- 48/48 cells `1.000000` on my harness except D=6.37 at `0.99974`;
- **every row constant across the cadence sweep and identical between tick sizes** — the property
  V2a fails and the property that actually matters;
- the `P=1` starvation cell (D=1.0, re-apply 0.3 s) reads `1.0000` where v1 read `0.0000`;
- INV-1 re-verified: D ∈ {3.0, 6.37 @Δ=0.1, 6.37 @Δ=0.5, 0.5 @Δ=1.0, 0.05 @Δ=0.1} all `1.000000`.

The design reason it works is the one she names: microseconds are re-bind-invariant, so the phase
needs no conversion and cannot be destroyed by a restart. `_add_or_refresh` collapsing to one line
is the tell that the abstraction is right — the repair *removed* code rather than adding a
correction term. **Ruling: rejection of C-1's letter UPHELD; V2b ACCEPTED as satisfying C-1.**

### §1.1 — The final-settlement clause: checked, not taken on faith

`_pulse_due`'s second arm (`subticks_elapsed >= sched_subticks`) is the load-bearing part and she
says so. Verified: it is capped by `pulses_delivered < sched_pulses`, so a binding pays exactly `P`
pulses and never more; and the `max(0, …)` floor on the carry debit prevents a settlement pulse from
pushing the ledger into debt across a subsequent re-bind. Her rejected alternative (period grid with
no settlement clause) would indeed have lost the last pulse wherever `round(D/Δ) < D/Δ` — i.e. it
would have broken INV-1 in precisely the cells the original defect broke. The clause is load-bearing
and correctly bounded.

---

## §2 — RULING ON MY OWN §3.2: she is right, my prose was transposed

**Conceded without qualification. Correction appended to the original finding, not silently edited.**

My §3.2 formula reads `time-to-next-pulse ≈ N/P' − phase·(P'−1)/P'`. An unrefreshed first pulse is at
`N/P'`. The refresh therefore *advances* the pulse by `phase·(P'−1)/P'` — **that quantity is the
credit**, and the forfeit (relative to a full `phase` credit) is `phase − phase·(P'−1)/P' = phase/P'`.
My prose asserted the reverse.

The decisive check is my own `P' = 1` conclusion. At `P' = 1`:
- credit `= phase·(P'−1)/P' = 0` — **matches** my stated "the credit is *exactly zero*" and matches
  the measured total starvation (0.0000 on my harness above);
- credit `= phase/P' = phase` — a *full* credit, which contradicts both.

So the formula, the `P'=1` conclusion, and every measured cell agree on **credit = `phase·(P'−1)/P'`**.
Her code comment at `damage_resolver.py` states it the same way and is correct.

**What the transposition did and did not affect.** It is a labelling error in one sentence of §3.2's
prose. It does not touch §3.1's measurements, the mechanism, the reachability argument, or the BLOCK
— all of which were independently measured and all of which stand. Its only substantive effect is
that the transposed reading *overstates* severity at large `P'` (it implies near-total forfeiture
where the truth is near-full credit) while *understating* it at `P' = 1`, the worst case. The finding
was directionally right for the wrong stated reason in that one sentence.

**Discipline #9 note on myself:** I wrote a derivation and a prose gloss of it that disagreed, and
shipped both in a BLOCK. The gloss should have been checked against the formula's own limiting case
before it went out. That is the same failure mode as her "named approximation with no error bound" —
a sentence asserted past the arithmetic that precedes it.

---

## §3 — C-2: the discriminating refresh test. Shape and discrimination both verified.

**Shape matches the prescription and exceeds it.** `test_INV4_sustained_reapplication_conserves_the_declared_RATE`
is parametrized `D ∈ {2.0, 3.0, 5.0, 6.37}` × `reapply ∈ {0.2, 0.5, 0.8, 1.0, 1.2, 1.5}` × `window =
120.0` — my grid verbatim — **plus a `tick_size ∈ {0.1, 0.5}` sweep I did not ask for**, which is the
arm that would have caught V2a. It applies through the production `_add_or_refresh` writer, not a
hand-built struct (Discipline #10). `test_refresh_does_not_starve_the_pulse_cadence` is **deleted**,
not patched — correct call; a 9 s guard that scores 8 on both kernels is not repairable.

**Discrimination measured myself, by stash, not read from her report.** HEAD's test file copied into
a clean `3aa4a55` worktree:

```
44 failed, 6 passed, 392 deselected
```

and the 6 survivors are **exactly** the `reapply = 1.0` column for `D ∈ {2.0, 3.0, 5.0}` at both tick
sizes — the cells where v1's phase-spread happened to land on the pulse boundary. Her claim is exact.
The battery discriminates (Discipline #11).

**One INFO on test robustness (§7, INFO-2).** The second assertion `delivered/ideal >= 0.99` is
window-specific, not invariant-derived. The first assertion (`ideal − one_pulse ≤ delivered ≤ ideal`)
is the INV-4 form and is the one that generalises. At the shipped grid the ratio assertion carries
about 0.1 pp of headroom (worst case `1 − 10.617/1200 = 0.9912`); a future sweep entry with a larger
`D` or a shorter window would fail it for a rate-correct kernel. Not wrong today; brittle tomorrow.

---

## §4 — Post-repair grid and the 0.999736 exception: her explanation is correct

Reproduced on my harness: 48/48 cells `1.000000` except D=6.37 at `0.999736`, constant across the
cadence sweep and identical between Δ=0.1 and Δ=0.5.

**I did not accept "settlement pulse in flight" on assertion — I falsified the alternative.** If
0.999736 were a *rate* error it would persist at every window length. Sweeping the window:

| W (s) | measured | `⌊W/period⌋ · per_pulse / (10·W)` | residual (s) |
|---|---|---|---|
| 120 | 0.999736 | 0.999736 | 0.032 |
| 121 | **0.991474** | 0.991474 | 1.032 |
| 125 | **0.993720** | 0.993720 | 0.785 |
| 200 | **0.997967** | 0.997967 | 0.407 |
| 1000 | **0.999028** | 0.999028 | 0.971 |

The ratio moves with `W` and the residual is **always < one period (1.0617 s)** — the exact signature
of a boundary term, not a rate term. The underlying rate is `per_pulse/period = 9.9999968603` against
a declared 10.0, a relative deficit of **3.14 × 10⁻⁷**, inside her stated µs-rounding bound of
5 × 10⁻⁷. **INV-4's residual table is honest and its bounds hold.** (The apparent constancy at
W ∈ {120, 240, 480, 960} that made me suspicious is an artefact of those windows all having the same
fractional part in periods.)

---

## §5 — C-3: THE ESCALATION TRIGGER. Zero moved. **Matt escalation does NOT fire.**

My original routing: *"escalate to Matt only if … the C-1 repair turns out to move the G-5 headline
numbers, which would make `_fix2` non-final in substance."* I rebuilt my §4 extractor from scratch
against the committed traces and pointed it at both directories.

```
33 cells compared, 0 MOVED
```

Every `_fix2` value reproduces my original §4 table, and every `_fix3` value equals it:

| instrument | `_fix2` | `_fix3` | verdict |
|---|---|---|---|
| W-c bleed rows / damage | 90 / 16,767.00 | 90 / 16,767.00 | identical |
| S-1 bleed rows / damage | 270 / 50,301.00 | 270 / 50,301.00 | identical |
| boss mean elapsed W-c / R3 | 28.4500 / 26.0600 | 28.4500 / 26.0600 | identical |
| R3/W-c kill-time ratio | 0.91599 | 0.91599 | identical |
| player DoT share W-c / R3 / S-1 | 1.295% / 6.215% / 3.887% | same | identical |
| total player `delivered` W-c / R3 | 1,295,220.00 | 1,295,220.00 | identical |
| kills | 720 / 720 / 716 | 720 / 720 / 716 | identical |
| S-1 boss win rate | 56/60 | 56/60 | identical |
| R3 poison alone (DoT − bleed) | 63,725.31 | 63,725.31 | identical |
| R3 dominant DoT magnitude bucket | 27.6 | 27.6 | identical |
| trace-file count per arm | 150 × 3 | 150 × 3 | identical |

**And the stronger check verified independently:** all **450 trace files** SHA-compared with the
header `engine_git_hash` normalised out — **0 differ, 0 missing.** `_fix3` is byte-identical to
`_fix2` at the event level on every fight of every arm.

**Consequence, endorsed:** `_fix2` is final **in substance**; `_fix3` supersedes it in **provenance
only**. `_fix3` is the calibrated set to read, because it is the one whose stamp resolves to the
kernel that produced it. **No escalation. This closes in-seam under ADR-002.**

*(One immaterial divergence: her R3 dominant-bucket count reads ×1,888 and my extractor reads ×1,892.
A filter difference between our two independent extractors; identical between `_fix2` and `_fix3` on
mine, so it cannot affect the zero-moved conclusion. Logged as INFO-3, not a condition.)*

---

## §6 — C-4 / C-5 / C-6 / C-7

**C-4 — CLOSED.** All `_fix3` reports and all 450 trace headers stamp `67e7ccb`, with no `-dirty`
suffix; `_fix` reads `9f6805a`, `_fix2` reads `7483a21`. The `-dirty` mechanism is live — my own
harness probe stamped `2be600f-dirty` from a dirty tree. The ordering discipline (code commit →
clean-tree battery → outputs commit) is the right general fix, not just this lap's patch. *(INFO-4:
`git status --porcelain --untracked-files=no` means a wholly **untracked** new source module would
not raise `-dirty`. Correct choice for battery outputs; a narrow blind spot for new code.)*

**C-5 — CLOSED on the letter, WARN-1 on the residual.** `git diff --quiet 7483a21 HEAD --
…/output/kitcal_g5/` returns clean: the directory is byte-identical to its pre-repair state, all 465
tracked files. Math-note §8 is **annotated, not edited** — the false sentence stands with a `⚠` block
naming exactly what was claimed and what was true. That is the honest form and I endorse it. The
overwrite guard is real: I live-tested it, and it **refuses with rc=2** and leaves the prior report
untouched.

**WARN-1 — the guard is partial.** It sits at the report-write site, which runs *after* the fights.
My live test confirmed that **5 trace files were written into the protected directory before the
report refused**. `kitcal_g5/smoke/traces/` holds 5 tracked trace files today, so the exact accident
class C-5 was chartered to make structurally impossible remains live one layer down, at the trace
layer. Not a BLOCK — C-5 asked for restore-or-amend and she delivered restore + annotate + a guard
beyond scope, and traces are git-recoverable — but the guard should move to (or be mirrored at) the
`trace_dir` open site.

**C-6 — CLOSED.** SS-1 extended with `leech_capacity_total` / `leech_healed_total` as non-poolable,
with the HP-pool-pin mechanism stated correctly (and a second extension I did not ask for: `_fix`/
`_fix2` are non-poolable with `_fix3` on any sustained-re-application DoT). SS-2 extended with the
HoT per-pulse **magnitude** change and its R-KC1-20 overheal-clamp interaction, correctly traced to
`hot_recovered` → `a_hot_recovered` (v2.17) → BC Axis-4. SS-5 added as the generalised per-tick
DoT trace-row distribution notice to **galadriel** and **drax**. All three are what I asked for.

**C-7 — CLOSED.** Banker's rounding recorded at §10.6 with the worked cases and an explicit
"recorded, not changed" disposition. Correct call — `round` is the form INV-3 is stated in.

**SS-6 — verified, with one precision note (WARN-2).** I measured the full 72-cell lattice on both
kernels: **8 cells shift a pulse index, 0 cells change ledger pulse count, 0 cells change total** —
her numbers exactly, and the shifted cell list matches hers item-for-item. Both shipped G-5
durations (`3.0` and `5.0` at Δ=0.1) are lattice-identical, which is the mechanical basis for the
C-3 result and it holds.

**WARN-2 — SS-6's wording understates 5 of the 8 cells.** In `{2.5, 3.33, 4.5, 6.37, 12.5} at Δ=1.0`
the change is not a phase shift; the final two pulses **coalesce onto the same sub-tick**, so the
emitted damaging-sub-tick count drops by one (e.g. `2.5|1.0`: rows 2 → 1, pulses 2 → 2). Ledger
pulse count, magnitude and total are all unchanged as she says, and **exposure is zero at both
shipped tick sizes (0.1 and 0.5)** — I confirmed no Δ=0.1 or Δ=0.5 cell changes row count. SS-5
already carries the general row-distribution notice, so this is a wording precision on SS-6, not a
missing disclosure.

---

## §7 — Tests, re-run by me

| suite | result |
|---|---|
| `tests/test_dot_tick_delivery.py` | **442 passed**, 0 failed |
| ailment slices (gamora/rocket) + registry + cp7b + O-d leech + G-5 wake + G-5 harness | **290 passed**, 0 failed |
| spatial gauntlet + WD BC measurement + cycle-13 gauntlet sim + aware-fighter policy seam | **133 passed**, 0 failed |
| non-vacuity by stash at `3aa4a55` (new refresh tests only) | **44 failed / 6 passed** — discriminates |

**865 tests re-run by me, 0 failures.** Her headline counts (442 / 263 / 904) are consistent with
these; suite-boundary naming differs, the zero does not.

---

## §8 — Residual conditions (all in-seam, none blocking the tag)

- **WARN-1 — extend the C-5 guard to the trace layer.** The report refuses; the traces do not. Move
  or mirror the hash check at the `trace_dir` open site so a default-`--out-dir` accident cannot
  write into banked evidence at all. Verified live: 5 traces landed inside a protected directory
  before the refusal fired.
- **WARN-2 — tighten SS-6's wording.** Name the 5 Δ=1.0 coalescence cells as coalescence, not as a
  one-sub-tick index shift, and state explicitly that shipped Δ ∈ {0.1, 0.5} have zero exposure
  (I measured it; the claim is true and should be in the note).
- **INFO-1 — `_pulse_due`'s settlement arm is now the only path that can pay >1 pulse in one
  sub-tick.** Correct and capped, but it is the subtle line in the kernel; worth a pin if a future
  change touches the cull ordering.
- **INFO-2 — the C-2 ratio assertion (`>= 0.99`) is window-specific.** The INV-4 bound assertion
  above it is the general one; the ratio line carries ~0.1 pp headroom on today's grid and would
  fail for a rate-correct kernel on a larger `D` or shorter window.
- **INFO-3 — extractor divergence on the R3 dominant-magnitude bucket** (her ×1,888 vs my ×1,892).
  Immaterial to C-3; worth one line if that bucket is ever cited as a headline.
- **INFO-4 — `-dirty` uses `--untracked-files=no`.** A wholly untracked new source module evades the
  flag. Right default for outputs; narrow blind spot for code.

### Approval routing (ADR-002)

All four conditions are within-seam, no consumer API change, no schema change, no `MIGRATION.md`
owed. **Gamora's to close at her discretion; no Matt decision needed.** The C-3 escalation trigger I
wrote into the original finding is **verified not to have fired** — 0 of 33 headlines moved and 0 of
450 traces differ — so `_fix2`/`_fix3` remain in-seam evidence and the milestone question does not
arise here.

---

## §9 — What I am endorsing, stated plainly

- **The rejection of my own C-1's letter, with measurement rather than argument.** She reproduced my
  grid cell-for-cell *before* deriving anything, then built and measured my prescription and showed
  it insufficient. That is the right order of operations and it is the reason the substitute is
  trustworthy. Discipline #10 executed properly against a reviewer, which is harder than executing
  it against a defect.
- **The abstraction change, not just the fix.** Absolute-time carry made `_add_or_refresh` one line
  and deleted the boundary arithmetic entirely. A repair that removes the code that produced the
  defect is a different quality of repair from one that adds a compensating term.
- **INV-4 as a named invariant with a stated residual table and bounds.** This is the direct answer
  to her own §10.0 lesson — "a named approximation with no error bound is an unverified claim wearing
  a parenthesis." She named the rule and then obeyed it in the same document.
- **C-3 verified rather than assumed, and then over-verified at the event level.** The 450-trace
  compare is more than I asked for and is the cleanest possible statement of blast radius.
- **§11.3 — the self-correction of her own SESSION-82 record.** She reports that the G-5 harness
  *does* write `leg3_pilot_section8a1_band_measurement.json`, contradicting her prior session's
  claim. **I reproduced this by accident**: my own smoke probe dirtied exactly that file. Her
  correction is right, and the disposition (restore, leave unstaged, it is star-lord's) is right.
  Recording a falsified prior claim you found yourself is the behaviour Discipline #9 exists for.

---

## References

**Reviewed:**
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/effect_resolver.py`
  (`_bind_tick_schedule`, `_pulse_due`, `_per_pulse`, `tick_effects`)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/damage_resolver.py`
  (`_add_or_refresh` — now one line)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/combatant.py`
  (`ActiveEffect.sched_period_us`, `sched_carry_us`)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/math/dot-tick-delivery-2026-07-28.md`
  (§8 annotation, §10.0–§10.7, §11.1–§11.3)
- `/Users/admin/Games/reincarnated-engine/tests/test_dot_tick_delivery.py`
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/spatial_gauntlet/kitcal_g5_harness.py`
  (`_git_hash`, `--overwrite` guard)
- `/Users/admin/Games/reincarnated-engine/src/reincarnated/simulation/output/kitcal_g5_fix3/**`,
  `…/kitcal_g5_fix2/**`, `…/kitcal_g5/**`

**Method note (Discipline #10).** Every number in this finding was produced by my own harnesses
against detached `git worktree`s at `7483a21` (pre) and `3aa4a55` (v1), plus a hand-implemented V2a
patch of the v1 tree representing my own C-1 letter, and HEAD for V2b. The §4/§5 battery numbers
come from an extractor I rebuilt from scratch against the committed traces, not from her reports.
No engine file was modified; the one file my probe dirtied
(`leg3_pilot_section8a1_band_measurement.json`) was restored and the tree left clean; both worktrees
were removed after measurement.

**Upstream:**
- `agentic_orchestration/qa/findings/2026-07-28-gate2-gamora-dot-tick-delivery-r-kc1-25.md` (the
  BLOCK this lifts; see its appended §3.2 correction note)
- `agentic_orchestration/qa/findings/2026-07-28-gate2-gamora-g5-dotfix-addendum.md`
- `agentic_orchestration/qa/findings/2026-07-28-gate2-gamora-g5-s1control.md`
