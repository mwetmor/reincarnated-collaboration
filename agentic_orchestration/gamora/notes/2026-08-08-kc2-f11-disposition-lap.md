# KC2 F-11 disposition lap — tree-state fork, ruling R-KC2-11 option (a+)

**Author:** gamora (simulation seam)
**Date:** 2026-08-08
**Status:** COMPLETE — 10/10 disposed · acceptance MET (`clean` under v2, FULL-capable) · commissioned smoke **244/0 EXACT** · **8 hand-backs raised, 2 of them BLOCKING** (the v2 policy name is not emittable today — § 5)
**Commissioned by:** gandalf as RUN-CONDUCTOR (KC2-SIM run charter `agentic_orchestration/gandalf/notes/2026-08-07-kc2-sim-run-charter.md`; commission row L-69(a))
**Ruling executed:** R-KC2-11 option (a+) — Matt, 2026-08-08
**Engine commits:** `396aa4ad` (1/3 .gitignore) · `d525fd05` (2/3 the 2 .py) · `97fb8f65` (3/3 the 5 notes) — all UNPUSHED per R-KC2-10
**Concurrency:** jack-ryan Gate-2 on `08b87085`+`f573f171` ran in parallel. Zero overlap — see § 9.

---

## 0. Mandate (verbatim ruling text)

> "(a+) code-surface-v2 = src/ minus src/\*\*/output/, PLUS dispose the 10 residual entries → target
> `engine_tree_state: clean`, FULL-capable. Disposition by class: 2 .py under src/ ADJUDICATED (commit
> if they touched results, relocate out of src/ if dead scratch — do NOT widen v2 to hide them);
> WAL/shm + telemetry backup → .gitignore; 5 notes → commit or relocate."

Anti-pattern pin, binding throughout: **do NOT widen v2 to hide them.** Honoured literally — the code
surface stayed `src/` minus `src/**/output/` at every step, and every residual was disposed on its
merits. § 8 records the compliance check.

---

## 1. Census — MECHANICAL, per Discipline #72 (tool output pasted, not eye-curated)

### 1.1 Set declaration (clause 6(a) — the set is declared BEFORE the sweep, and names what it excludes)

| | |
|---|---|
| **Repo** | `/Users/admin/Games/reincarnated-engine` |
| **Instrument** | `git status --porcelain -unormal`, `??` rows |
| **Population** | every untracked ENTRY (porcelain `-unormal` collapses wholly-untracked directories to one line — entries, not files) |
| **code-surface-v2** | paths matching `^src/` **MINUS** paths matching `^src/(.*/)?output/` |
| **EXCLUDED by declaration** | (a) all untracked entries under `src/**/output/` — the sim's own exhaust, which is the whole point of v2; (b) all untracked entries outside `src/` — never in the code-surface predicate under v1 or v2, counted separately in § 6.3 |
| **Also swept** | tracked modifications / staged rows (`git status --porcelain -unormal \| grep -v '^?? '`) — v2 is dirty on those too, and a census of untracked entries alone would have missed them |

### 1.2 ⚑ A SET-DECLARATION MISS I MADE AND CAUGHT — Discipline #72 clause 6 in the act

My **first** sweep declared the exclusion as `src/reincarnated/output/`. The ruling says
`src/**/output/`. The two are not the same set: the bulk of this repo's exhaust sits at
`src/reincarnated/**simulation**/output/`, one level deeper. Pasted, because a mechanical
instrument run over an under-declared set misses **with an instrument's authority**:

```
=== untracked under src/reincarnated/output/ ===          <-- MY UNDER-DECLARED SET
6
=== untracked under src/ but NOT under src/reincarnated/output/ ===
2524
```

The grouping that caught it:

```
2518 src/reincarnated/simulation      <-- 2,514 of these are .../simulation/output/
  22 output/standard-demo-regen-2026-05-17/season_002012
   6 src/reincarnated/output
   3 src/reincarnated/telemetry
   2 src/reincarnated/generation
```

Had I closed on the first sweep I would have reported **2,524 residuals** instead of 10 and declared
the ruling unexecutable. **#72 clause 6(b) note:** this is not a declined row folded into a verdict —
it is the failure clause 6 exists to name, committed by an agent who had read clause 6 twenty minutes
earlier, which is the same structural point #72's own founding instances 6 and 7 make. Recorded, not
buried.

### 1.3 The census, as executed (corrected set)

```
### SET DECLARATION
population = git status --porcelain -unormal (untracked '??' rows), repo /Users/admin/Games/reincarnated-engine
code-surface-v2 = paths matching ^src/ MINUS paths matching ^src/(.*/)?output/

=== [A] ALL entries (?? rows) ===
2664
=== [B] entries under src/ ===
2530
=== [C] entries under src/**/output/ (the v2 exclusion) ===
2520
=== [D] CODE-SURFACE-V2 RESIDUALS = B minus C ===
     1	src/reincarnated/export/drax-SIGNED-encounters-delta-2026-07-22.md
     2	src/reincarnated/generation/notes/2026-06-15-dodge-intrinsic-glass-close-st-math-note.md
     3	src/reincarnated/generation/notes/2026-06-20-str-bleed-emission-regression-diagnosis.md
     4	src/reincarnated/simulation/math/auto-amp-delete-flag-defer-2026-06-15.md
     5	src/reincarnated/simulation/math/glass-cannon-boss-death-diagnose-2026-06-21.md
     6	src/reincarnated/simulation/notes/step3_f3_boss_scale_smoke_2026_07_07.py
     7	src/reincarnated/simulation/scripts/gamora_step3_f3_boss_scale_sweep_2026_07_07.py
     8	src/reincarnated/telemetry/telemetry.db.pre-v2.21-backup-20260711T000000Z
     9	src/reincarnated/telemetry/telemetry_seed.db-shm
    10	src/reincarnated/telemetry/telemetry_seed.db-wal
=== [D] count ===
      10
=== [E] entries OUTSIDE src/ (not in v2 scope; informational) ===
134
=== [F] tracked modifications / staged (v2 dirty also if any) ===
                                                    <-- EMPTY
```

### 1.4 Census vs Matt's count — ZERO DELTA

| | Matt / L-42 conductor enumeration | My mechanical sweep | Δ |
|---|---|---|---|
| residuals in code-surface-v2 | **10** | **10** | **0** |
| export delta note | 1 | 1 | 0 |
| generation notes | 2 | 2 | 0 |
| simulation math notes | 2 | 2 | 0 |
| simulation scripts (.py) | 2 | 2 | 0 |
| telemetry backup | 1 | 1 | 0 |
| telemetry-seed WAL/shm | 2 | 2 | 0 |
| tracked modifications | (not enumerated) | **0** | — |

**Grade: MEASURED.** Count and per-class composition both reproduce exactly. Checked, not assumed —
per the commission brief.

**One thing the sweep found that the L-42 enumeration did not carry:** `[F]` is EMPTY, i.e. there
were **zero tracked modifications** at census time. That matters, because v2's predicate is a
disjunction — untracked-in-code-surface OR tracked-modification — and disposing only the 10 would not
have produced `clean` if the second limb were non-empty. It was empty. Now recorded.

**Population drift since L-42, informational — compared at the SAME grain.** L-42's triple
`2,414 / 2,404 / 10` is *under `src/`* / *under `src/**/output/`* / *residual*, not a repo total
(the emitter docstring's companion figure "134 of 2,537" supplies the outside-`src/` half). Lined up
against the same three quantities from my sweep:

| quantity | L-42 | this sweep | Δ |
|---|---|---|---|
| untracked entries under `src/` | 2,414 | **2,530** | **+116** |
| untracked entries under `src/**/output/` | 2,404 | **2,520** | **+116** |
| residuals in code-surface-v2 | 10 | **10** | **0** |
| untracked entries outside `src/` | 134 | **134** | **0** |

**Every one of the 116 new entries landed in `src/**/output/`.** The exhaust grew by the intervening
laps (stat fold, C-1 closure, ARR re-pass) and the code surface did not move at all — **F-11's
mechanism confirming itself a third time**, and precisely the reason v2 excludes that directory.

*(An earlier draft of this paragraph compared my repo TOTAL of 2,664 against L-42's under-`src/`
2,414 and reported a "+250" that does not exist at any single grain. Corrected here before commit;
recorded rather than silently fixed, because the whole subject of this lap is counts taken at a
declared grain.)*

---

## 2. Per-file disposition table

| # | Path (relative to engine root) | Class | Per-class rule (Matt's text) | Action | Evidence |
|---|---|---|---|---|---|
| 1 | `src/reincarnated/export/drax-SIGNED-encounters-delta-2026-07-22.md` | note (cross-seam: star-lord's dir, drax-authored) | "5 notes → commit or relocate" | **COMMIT in place** `97fb8f65` | drax SIGN-WITH-CONDITIONS verdict; the artifact it signs, `export/math/2026-07-22-one-realm-bundle-schema-delta.md`, is TRACKED (verified `git ls-files --error-unmatch`) |
| 2 | `src/reincarnated/generation/notes/2026-06-15-dodge-intrinsic-glass-close-st-math-note.md` | note (cross-seam: rocket's) | same | **COMMIT in place** `97fb8f65` | rocket Discipline-#1 math note, status "PRODUCED — HALT for MANDATORY jack-ryan Gate-1"; cites dispatch `2026-06-15-rocket-dodge-intrinsic-glass-close-st.md` (verified present + tracked); 46 tracked siblings in that dir at census time (48 after this commit) |
| 3 | `src/reincarnated/generation/notes/2026-06-20-str-bleed-emission-regression-diagnosis.md` | note (cross-seam: rocket's) | same | **COMMIT in place** `97fb8f65` | rocket READ-ONLY diagnosis, KR-dispatched + Matt-authorized per its own header; root cause PINNED (BC-target emitter path vs `ability_grammar.py`) |
| 4 | `src/reincarnated/simulation/math/auto-amp-delete-flag-defer-2026-06-15.md` | note (**my seam**) | same | **COMMIT in place** `97fb8f65` | gamora Discipline-#1 math note; cites dispatch `2026-06-15-gamora-auto-amp-delete-flag-defer.md` (verified present + tracked); 214 tracked siblings in `simulation/math/` at census time (216 after this commit) |
| 5 | `src/reincarnated/simulation/math/glass-cannon-boss-death-diagnose-2026-06-21.md` | note (**my seam**) | same | **COMMIT in place** `97fb8f65` | gamora math note + post-run findings; converges with `gandalf/notes/2026-06-21-monster-to-player-calibration-design-half.md` (verified present + tracked); DIAGNOSE-ONLY, zero production change |
| 6 | `src/reincarnated/simulation/notes/step3_f3_boss_scale_smoke_2026_07_07.py` | py — **ADJUDICATED** | "commit if they touched results" | **COMMIT** `d525fd05` | § 3.1 — touched results |
| 7 | `src/reincarnated/simulation/scripts/gamora_step3_f3_boss_scale_sweep_2026_07_07.py` | py — **ADJUDICATED** | "relocate out of src/ if dead scratch" | **RELOCATE** → `scripts/gamora_step3_f3_boss_scale_sweep_2026_07_07.py` (byte-identical) | § 3.2 — dead scratch on four measured negatives |
| 8 | `src/reincarnated/telemetry/telemetry.db.pre-v2.21-backup-20260711T000000Z` | telemetry backup (472 MB) | "telemetry backup → .gitignore" | **GITIGNORE** `396aa4ad` | § 4 |
| 9 | `src/reincarnated/telemetry/telemetry_seed.db-shm` | WAL/shm (32 KB) | "WAL/shm → .gitignore" | **GITIGNORE** `396aa4ad` | § 4 |
| 10 | `src/reincarnated/telemetry/telemetry_seed.db-wal` | WAL/shm (0 B) | "WAL/shm → .gitignore" | **GITIGNORE** `396aa4ad` | § 4 |

**Class totals vs the ruling:** notes 5/5 disposed · .py 2/2 adjudicated (1 commit, 1 relocate) ·
gitignore 3/3. **10/10, no residual, no deferral.**

---

## 3. The 2 .py — adjudications, SHOWN

Both were adjudicated on **content + git history + a mechanical citation sweep**, not on intuition,
and they split. Common ground first:

- **Neither was ever tracked.** `git log --all --full-history --oneline -- <path>` returns EMPTY for
  both. Their content exists in no commit anywhere in the repo.
- **Zero importers, both.** `grep -rn --include='*.py' 'step3_f3_boss_scale' src/ tests/ scripts/`
  returns nothing but the files themselves.
- **Basename citation sweep** across both repos (`*.md`/`*.py`/`*.json`, vendor + captures excluded):
  3 hits for the smoke (2 self-references + jack-ryan's F-11 census listing), 2 for the sweep (1 self
  + the same census listing). **No third-party names either file.**

⚑ **A signal I deliberately did NOT use — and it turned into the lap's incidental finding.**
Both `.py` carry mtime `2026-07-29 03:48:43/44`, three weeks after the commit their docstrings
reference. I checked whether that was authorship evidence. It is not, and the reason is § 3.0.

### 3.0 ⚑ INCIDENTAL FINDING — all ten residuals share ONE five-second mtime window

Measured across all 10 (post-disposition paths):

```
2026-07-29 03:48:40  src/reincarnated/export/drax-SIGNED-encounters-delta-2026-07-22.md
2026-07-29 03:48:40  src/reincarnated/generation/notes/2026-06-15-dodge-intrinsic-glass-close-st-math-note.md
2026-07-29 03:48:40  src/reincarnated/generation/notes/2026-06-20-str-bleed-emission-regression-diagnosis.md
2026-07-29 03:48:43  src/reincarnated/simulation/math/auto-amp-delete-flag-defer-2026-06-15.md
2026-07-29 03:48:43  src/reincarnated/simulation/math/glass-cannon-boss-death-diagnose-2026-06-21.md
2026-07-29 03:48:43  src/reincarnated/simulation/notes/step3_f3_boss_scale_smoke_2026_07_07.py
2026-07-29 03:48:44  scripts/gamora_step3_f3_boss_scale_sweep_2026_07_07.py
2026-07-29 03:48:44  src/reincarnated/telemetry/telemetry_seed.db-shm
2026-07-29 03:48:44  src/reincarnated/telemetry/telemetry_seed.db-wal
2026-07-29 03:48:44  src/reincarnated/telemetry/telemetry.db.pre-v2.21-backup-20260711T000000Z
```

Ten files whose **content** dates span five weeks (2026-06-15 → 2026-07-22), across four different
seams, in file classes as unlike as a 472 MB SQLite snapshot and a 4 KB markdown verdict, all
touched inside **five seconds**. The sweep's output artifact
(`output/step3_f3_boss_scale_sweep_beat.json`) sits in the same window at `03:48:40`.

**What this changes.** The F-11 residual set is not ten independent hygiene lapses accumulated over
five weeks. It is the survivor set of **one filesystem event** at `2026-07-29 03:48`. That is why the
set is exactly these ten and why it did not grow between L-42's census and mine — both read **10**
while the exhaust under `src/**/output/` grew by **+116** (§ 1.4). The code surface accumulates
nothing on its own; it acquired these ten in one stroke and then stayed put.

**Mechanism: UNRESOLVED-NAMED.** Candidates I can see but did not test: a git-worktree operation
(this repo carries `.claude/worktrees/agent-ad557ae39574ea548/`), an archive/backup restore, a
stash-adjacent operation. The nearest engine commit is `ddf51a86` at `2026-07-29 03:49`, one minute
later. **I am not guessing which** — the mechanism is outside the ruling's scope and outside what I
measured, so it is named rather than asserted, and routed as HB-6.

**Consequence for § 3.1 and § 3.2: mtime is excluded from both adjudications** (#72 clause 6(b) — a
row the instrument cannot resolve is emitted as unresolved, never folded into a verdict). Both
verdicts rest only on git history, the seed-base chain, the citation sweep, the importer sweep, and a
live run. Neither depends on when these files were written.

### 3.1 `simulation/notes/step3_f3_boss_scale_smoke_2026_07_07.py` → **COMMIT** (touched results)

**It is the falsification instrument for a landed production behaviour, and the tree has no other.**

1. **It runs GREEN today, against live production code.** Executed
   `python3 -m reincarnated.simulation.notes.step3_f3_boss_scale_smoke_2026_07_07`:

   ```
   A. strictly-positive guard: PASS (0.0 and -1.0 raise)
   B. identity (bds=1.0, mds=1.0 == native dm): PASS
   C. tier-scoped no-leakage: boss=1.2 (mds*bds) elite=0.0675 swarm=0.0255 mini-boss=1.2 (only mds on swarm/elite): PASS
   D. genre-sane boss HP: 9000.0 = 60x trash: PASS
   E. F2 room no-leakage (tiers=['elite', 'swarm']; no boss tier): dm invariant to bds: PASS

   7/7 assertions GREEN — tier-scoped boss_damage_scale knob proven; no leakage; genre-sane HP.
   ```

2. **Its assertions map 1:1 onto behaviour commit `61a7faf8` shipped** into tracked production code:
   the strictly-positive guard at `gauntlet_four_family_metrology_driver.py:235`, the
   boss/mini-boss-only tier gate at `:256`, the 9000 boss HP in `_build_standard_mob_dicts`.
3. **⚑ It is the ONLY coverage of that knob in the repo — MEASURED.**
   `grep -rln 'boss_damage_scale' tests/` returns **EMPTY**. The strictly-positive guard, whose own
   error message explains that `0.0` silently aliases the native damage multiplier through the
   `or 1.0` coercion at `spatial_resolver_adapter.py:118`, has no pytest coverage at all. Relocating
   this file out of `src/` would have left a live fail-fast guard with zero falsifiers.
4. **Directory convention agrees:** **13** sibling `.py` in `simulation/notes/` were tracked before
   this commit (14 including it) — that dir's convention is that these smoke/probe modules ARE
   committed.

   ⚑ **CORRIGENDUM, self-filed.** I first wrote **20** here and in commit `d525fd05`'s message. That
   number was eye-read off a `git ls-files` listing truncated at `head -20` which contained `.md`
   files as well as `.py`. Re-measured mechanically: `git ls-files 'src/reincarnated/simulation/notes/*.py'`
   → 14 post-commit, so **13** before. The verdict does not move — the argument is that tracked
   `.py` siblings exist in numbers in that directory, and 13 carries it exactly as 20 would — but the
   number in `d525fd05`'s message is **wrong and is corrected here** (corrigenda-forward; the commit
   stands as record). It is the same defect class as § 1.2: a count taken by eye off a truncated tool
   output, inside a lap whose whole subject is #72. Third instance in this lap's own scope.

**Verdict: touched results → COMMIT.** Grade **MEASURED** (chain: run output → live source lines →
empty test-grep → landed commit).

### 3.2 `simulation/scripts/gamora_step3_f3_boss_scale_sweep_2026_07_07.py` → **RELOCATE** (dead scratch)

The tempting reading is that this script produced production's `LOCKED_BOSS_DAMAGE_SCALE = 48.0`.
**It did not, and the seed base proves it.**

**The discriminator.** The untracked script declares `SWEEP_SEED_BASE = 69_000_000` and writes to
`output/step3_f3_boss_scale`. Its tracked sibling `gamora_step3_lived_calibration_sweep_2026_07_07.py`
declares `SWEEP_SEED_BASE = 67_000_000` and writes to `output/step3_calibration`. Every sweep result
stamps its own `seed_base`. So the question "which instrument produced the number production uses"
has a mechanical answer.

**The chain, closed:**

| Link | Measurement |
|---|---|
| Production constant | `gauntlet_lived_channel_repilot_driver.py:61` → `LOCKED_BOSS_DAMAGE_SCALE = 48.0`, comment "Full-pop sweep step2 lock: bds=48.0, WR_IN_BAND, F3 pop WR 0.7018" |
| Landed by | `git log -S 'LOCKED_BOSS_DAMAGE_SCALE = 48.0'` → **`61a7faf8`** (2026-07-07, "Step-3 completion") |
| Result artifact in that commit | `src/reincarnated/output/step3_calibration/step3_lived_sweep.json` → `"seed_base": 67000000`, `"locked_boss_damage_scale": 48.0`, `"locked_mob_damage_scale": 0.03`; `0.7018` ×2 and `0.9446` ×4 present — the exact figures `61a7faf8`'s own message reports |
| ⇒ producer | **`seed_base 67000000` = the TRACKED sibling**, which `61a7faf8` also modified (+189 lines). The commit's 7-file list does not contain either untracked file. |
| The untracked script's ONLY output | `src/reincarnated/output/step3_f3_boss_scale/step3_f3_boss_scale_sweep_beat.json` → `"seed_base": 69000000`, **`"beat": true`, `"n_fights_per_element": 1`**, `"locked_boss_damage_scale": 36.0` |
| Is `36.0` consumed anywhere? | Mechanical grep for a boss-scale-adjacent `36.0`, both repos, `*.md`/`*.py`/`*.json` — **EMPTY** |

**Four independent negatives:** never tracked · zero importers · its one output is a low-fidelity
BEAT run (`n_fights_per_element: 1`) · the value that run produced is cited by nothing, while the
value production uses provably came from a different instrument at a different seed base.

**It is not a copy of the tracked sibling either** — 255 lines vs 327, 392 diff lines, different step
ordering, different output dir. It is a second independent implementation of the same sweep whose
full-population mode was never run.

**Why relocate rather than commit.** Committing it into `simulation/scripts/` would place a
never-full-pop-run instrument beside the constant it appears to authorise, where a later reader would
reasonably treat it as the provenance of `48.0`. It is not. That is a **#67 name-is-a-pin hazard**
created by a filing decision, and the cheapest way not to create it is not to file it there.

**Why relocate rather than delete.** Deletion is destructive and the evidence for "disposable" is
weaker than the evidence for "not the producer of record". Relocated **byte-identical** —
`sha256 c6c605d8f527b497f1ac1c74c648285ad203414cd48ec5dd45f725328eb2f11b` verified before and after
the move.

**Verdict: dead scratch → RELOCATE to `scripts/`.** Grade **MEASURED**.

**Destination rationale:** engine-root `scripts/` is this repo's established home for one-off
harnesses — it already carries 18 untracked one-off `.py`, including
`gamora_glass_cannon_boss_death_diagnose_2026_06_21_DIAGNOSE_THROWAWAY_.py`, the harness belonging to
residual #5. It is outside `src/`, so it is outside the v2 code surface by construction.

**⚑ One durability caveat, named not hidden.** The relocated file remains **untracked**, so its only
durable records are this note (with its sha256) and commit `d525fd05`'s message. A `git clean -fdx`
would remove it. Matt's ruling said *relocate*, and relocation is what was executed; if the conductor
would rather it were banked, committing it at the new path is a one-line follow-up that does not
disturb anything decided here.

---

## 4. `.gitignore` — WAL/shm + telemetry backup (commit `396aa4ad`)

Two insertions, both placed beside the pattern block they extend.

**Beside the existing production-telemetry block:**

```
src/reincarnated/telemetry/telemetry_seed.db-shm
src/reincarnated/telemetry/telemetry_seed.db-wal
```

**Beside the existing `data/telemetry.db.pre-*` backup line:**

```
src/reincarnated/telemetry/telemetry.db.pre-*
```

**Why these shapes.** `telemetry_seed.db` **itself is TRACKED** (verified `git ls-files`) — it is a
fixture. Only its two SQLite journal sidecars, which any reader of the fixture creates, are ignored,
and they are ignored by **exact path with zero glob**. The backup pattern is anchored to one
directory plus one filename stem and globs only the snapshot timestamp; it mirrors the pre-existing
`data/telemetry.db.pre-*` line, which predates the production DB's move into
`src/reincarnated/telemetry/`.

**Narrowness verified by control probe, not asserted** (`git check-ignore -v`):

```
=== the 3 targets ===
telemetry.db.pre-v2.21-backup-20260711T000000Z -> .gitignore:63:src/reincarnated/telemetry/telemetry.db.pre-*
telemetry_seed.db-shm                          -> .gitignore:44:src/reincarnated/telemetry/telemetry_seed.db-shm
telemetry_seed.db-wal                          -> .gitignore:45:src/reincarnated/telemetry/telemetry_seed.db-wal

=== NARROWNESS CONTROL: these must stay visible ===
telemetry_seed.db (tracked fixture) -> correctly NOT ignored
telemetry/db.py (tracked code)      -> correctly NOT ignored
telemetry/new_mod.py (hypothetical) -> correctly NOT ignored
```

The third control is the load-bearing one: a future real `.py` added to the telemetry package is
**not** hidden by anything landed here.

---

## 5. Policy transition v1 → code-surface-v2 — ⛔ **HAND-BACK, both limbs**

**Not executed. Handed back, per the commission brief's own instruction.** The emitted value cannot
legally become `code-surface-v2` today, for two independent reasons, each measured.

### 5.1 Limb A — the spec's enum has no legal value (conductor-owned)

CD-2 § 11.4 of `agentic_orchestration/gandalf/notes/2026-08-08-kc2-sim-battle-spec.md`, verbatim:

> five values, exhaustive by construction: `"code-surface-v1"` (ruled default …) | `"any-change-v1"` |
> `"tracked-only-v1"` | `"declared-override"` … | `"unavailable"` …

**`code-surface-v2` is not among them.** The brief is explicit that the spec is conductor-owned and
that I edit emitted values, never the spec. **Handed back to gandalf.**

### 5.2 Limb B — the emit site is star-lord's seam, and it rejects v2 (measured)

The whole emit path lives in `src/reincarnated/export/` — outside my scope by AGENTS.md:

| Surface | File | What it is |
|---|---|---|
| enum | `export/baton_v1_schema.py:512–518` | `TreeStatePolicy` Literal — five members, no v2 |
| selectable set | `export/baton_v1_schema.py:528–530` | `TREE_STATE_POLICIES_SELECTABLE` — three members, no v2 |
| default | `export/baton_v1_schema.py:524` | `TREE_STATE_POLICY_DEFAULT = "code-surface-v1"` |
| surface constant | `export/baton_v1_schema.py:534` | `TREE_STATE_IMPORT_SURFACE = "src/"` — v2 needs the `src/**/output/` exclusion here |
| grader | `export/baton_v1_emitter.py:210–290` | `engine_tree_state_detail()` — the v1 branch is `:278–290` |
| guard | `export/baton_v1_validator.py:212–240` | `G-CD2-POLICY` |

Measured rejection, both layers:

```
code-surface-v2 in enum? -> False
code-surface-v2 -> RAISES: BatonEmitError unknown tree-state policy 'code-surface-v2';
                   known: ['any-change-v1', 'code-surface-v1', 'declared-override', 'tracked-only-v1', 'unavailable']

G-CD2-POLICY under a hypothetical v2 emission:
  policy='code-surface-v2' count=0    -> FAIL: tree_state_policy='code-surface-v2' is not a named policy
  policy='code-surface-v2' count=None -> FAIL: tree_state_policy='code-surface-v2' is not a named policy
  policy='code-surface-v1' count=134  -> pass
```

**A baton emitted with `tree_state_policy: "code-surface-v2"` today would fail `G-CD2-POLICY`** —
i.e. the honest emission is currently blocked at the guard, not merely unimplemented. **Handed back
to star-lord** (schema + emitter + validator), gated on limb A.

### 5.3 ⚑ A design question the transition creates — for the conductor, priced

`tree_state_untracked_entries_outside_src` is documented (`baton_v1_schema.py:548–561`) as the
**evidence for the non-dirtying half of the rule**, and `G-CD2-POLICY` enforces exactly that: under
`code-surface-v1` the field MUST be present, or *"the non-dirtying half of the rule left no
evidence"*. v2 **enlarges the non-dirtying set** — from "outside `src/`" (135 entries) to "outside
`src/`, plus everything under `src/**/output/`" (135 + 2,521 = **2,656**). So v2 forces a choice:

- **(a) keep the field literal.** It keeps counting outside-`src/` only (135). v2's *largest*
  non-dirtying class — the 2,521 exhaust entries, the entire reason v2 exists — then leaves **no
  evidence at all**, which is precisely the defect `G-CD2-POLICY`'s v1 branch was written to prevent.
- **(b) re-semantic the field to "outside the code surface"** (2,656). Honest, but the field NAME
  then misdescribes its contents — a **#67 name-is-a-pin** hazard — and a rename is a baton schema
  change with an ADR-004 MIGRATION obligation.

Not mine to rule. Priced here so the hand-back is not scoped as "add one enum member" when it is
enum + surface constant + grader branch + guard branch + a field-semantics decision + possibly a
schema migration. **(#72 clause 8 — grade the work class before pricing the discharge.)**

---

## 6. Acceptance check

### 6.1 Post-disposition census — **`engine_tree_state: clean` under code-surface-v2**

Same declared set, same instrument:

```
=== [A] ALL untracked entries ===
2656
=== [B] entries under src/ ===
2521
=== [C] entries under src/**/output/ (the v2 exclusion) ===
2521
=== [D] CODE-SURFACE-V2 RESIDUALS = B minus C  (target: 0) ===
--- count: 0 ---                                    <-- EMPTY
=== [F] tracked modifications / staged (must be empty) ===
--- count: 0 ---                                    <-- EMPTY

=== v2 PREDICATE: dirty iff (tracked modification) OR (untracked under src/ minus src/**/output/) ===
tracked_modifications=0  v2_untracked_in_code_surface=0
==> engine_tree_state under code-surface-v2: CLEAN
```

`B == C` exactly: **every** remaining untracked entry under `src/` is exhaust. Grade **MEASURED**.

### 6.2 AC-11.4e FULL-capability predicate — **PASSES**

AC-11.4e is `engine_tree_state == "dirty" ⇒ calibration_grade != FULL`, implemented at
`baton_v1_emitter.py:499` and `baton_v1_validator.py:204–209`. Evaluated read-only, no seam edit:

```
  engine_tree_state='dirty'  + calibration_grade=FULL -> BLOCKED: dirty tree claims FULL grade — a clean SHA on an edited tree is a false claim
  engine_tree_state='clean'  + calibration_grade=FULL -> PASSES (FULL permitted)
```

Measured v2 grade of this tree post-disposition = `clean` ⇒ **the AC-11.4e guard does not fire ⇒
FULL-CAPABLE**, which is the target Matt's ruling named.

**Scope of the claim, stated precisely:** the tree now *satisfies* the FULL-capability precondition
under v2. The baton cannot yet *emit* `code-surface-v2` as its policy name (§ 5), so until the
hand-backs land, an honest emission still reads `code-surface-v1` → `dirty` → non-FULL. **The
disposition is done; the plumbing is owed by two other seams.**

### 6.2b ⚑ The v2 grade is INVARIANT under sim activity — measured, not argued

A one-shot `clean` would be a weak result on a repo that dirties its own tree by running. So I
re-measured the predicate **while the pytest suite of § 7 was mid-flight**, writing fresh artifacts
into `src/reincarnated/output/`:

```
=== ACCEPTANCE PREDICATE RE-MEASURED *DURING* THE PYTEST RUN ===
[B] under src/                 : 2526      <- +5 vs the § 6.1 census, minutes earlier
[C] under src/**/output/       : 2526      <- +5, the SAME +5
[D] code-surface-v2 residuals  : 0         <- UNMOVED
[F] tracked modifications      : 0         <- UNMOVED

  code-surface-v1 (implemented): state=dirty   <- dirty, and re-dirties every run
  code-surface-v2 (ruled)      : state=clean   <- [D]=0 and [F]=0
```

`[B]` and `[C]` moved by exactly the same +5; `[D]` and `[F]` did not move at all. A third reading
minutes later, still mid-suite, read `[B] 2530 / [C] 2530 / [D] 0`. **The writer is named, not
inferred** — the growing entries are the suite's own results artifacts, one per ~80 seconds:

```
2026-08-08 19:07:21  src/reincarnated/simulation/output/cycle-13-gauntlet-sim-results-20260808_230721.json
2026-08-08 19:06:02  src/reincarnated/simulation/output/cycle-13-gauntlet-sim-results-20260808_230602.json
2026-08-08 19:04:42  src/reincarnated/simulation/output/cycle-13-gauntlet-sim-results-20260808_230442.json
2026-08-08 19:03:23  src/reincarnated/simulation/output/cycle-13-gauntlet-sim-results-20260808_230323.json
2026-08-08 19:02:04  src/reincarnated/simulation/output/cycle-13-gauntlet-sim-results-20260808_230204.json
2026-08-08 19:00:45  src/reincarnated/simulation/output/cycle-13-gauntlet-sim-results-20260808_230045.json
2026-08-08 18:57:26  src/reincarnated/simulation/output/cycle-13-gauntlet-sim-results-20260808_225726.json
2026-08-08 18:56:38  src/reincarnated/simulation/output/cycle-13-gauntlet-sim-results-20260808_225638.json
```

That is `test_cycle13_wave5_gauntlet_sim` — the same test `61a7faf8`'s own smoke line named. Across
`[B]`/`[C]` 2521 → 2526 → 2530, **`[D]` and `[F]` never moved.** **Every byte the
engine wrote while grading itself landed in the excluded set.** So v2's grade is not merely `clean`
at one instant — it is *stable under the workload that makes v1 dirty*, which is the property option
(c) (demand a clean tree at emit) could never have delivered and the reason the conductor's lean
toward (a) was right. Emitted grade under v2 is a fact about the code, not about whether a run
happened to be in flight.

### 6.3 `tree_state_untracked_entries_outside_src` — reads **135**, not 0. This is a FINDING.

The commission brief asked me to confirm this field "reads 0". **It cannot, and 0 is not what the
field means.** Measured post-disposition:

```
  code-surface-v1    state=dirty  untracked_entries_outside_src=135
  any-change-v1      state=dirty  untracked_entries_outside_src=None
  tracked-only-v1    state=clean  untracked_entries_outside_src=None
```

The field counts untracked entries **outside `src/`** — a set the ruling never touched and neither v1
nor v2 treats as dirtying:

```
 110 output/          (repo-root run artifacts)
  19 scripts/         (one-off harnesses; +1 is my relocation)
   3 data/
   1 telemetry.db/
   1 simulation/
   1 .claude/
```

Pre-disposition it read **134**; post it reads **135**, and the +1 is exactly the relocated sweep
crossing out of `src/` — the field behaving correctly, and a small independent confirmation that the
relocation landed where intended.

**What the brief most likely meant** — *"zero untracked entries inside the v2 code surface"* — is
§ 6.1's `[D] count: 0`, and that is **MET**. The field with this name measures something else. Flagged
because § 5.3 shows the name is about to become load-bearing in the v2 transition.

---

## 7. Smoke suite

### 7.1 The commissioned smoke — **244 passed / 0 failed, 33.60 s. EXACT baseline, zero regressions.**

The run's smoke is a **named six-module selection**, not the whole tree (stat-fold note § header:
*"`test_kc2_opposition_wave_engine` + `test_kc2_locomotion` + `test_kc2_s1_ramp` +
`test_kc2_micro_oracles` + `test_baton_v1` + `test_kc2_monster_stats` → 244 passed / 0 failed,
33.84 s"*). Re-run on the post-disposition tree, no `-x` per #65:

```
........................................................................ [ 29%]
........................................................................ [ 59%]
........................................................................ [ 88%]
............................                                             [100%]
244 passed in 33.60s
```

**244 / 244, identical to the baseline count, zero failures.** Grade **MEASURED**.

### 7.2 ⚑ I FIRST RAN THE WRONG SUITE, AND IT IS NOT CLEAN — declared, not buried

My first run was `pytest tests/ -q` — **the entire tree, 10,436 tests, 21 min 48 s** — which I
launched believing it was the "244" the brief named. It is not. Its result:

```
63 failed, 10373 passed, 3 warnings, 21 errors in 1308.86s (0:21:48)
```

I am reporting this rather than quietly substituting the run that passed, because a 63-failure tree
is a fact about the substrate the conductor may not have, and discovering it by accident does not
make it less true.

**Is any of it mine? NO — three structural reasons and one empirical control.**

1. **The relocated file was never importable.** Neither `src/reincarnated/simulation/scripts/` nor
   repo-root `scripts/` contains `__init__.py`. Neither is a package; the file could never be reached
   by an `import` from either location.
2. **Neither location is collected.** `pyproject.toml:25` → `testpaths = ["tests"]`.
3. **The six committed files changed no working-tree byte.** `git add` writes `.git/index`; pytest
   reads the working tree. The three `.gitignore` lines are read by git alone.
4. **A/B CONTROL, run explicitly.** I copied the relocated `.py` back to its original path under
   `src/` and re-ran the three named failing files. **Byte-identical outcome** — same three test IDs,
   `3 failed, 107 passed` both times. Then I removed the control copy and re-verified
   `[D] code-surface-v2 residuals = 0`. The relocation is not the cause of anything.

**Independent corroboration for the 21 errors:** `simulation/AGENT_STATE.md:7414` already records the
`test_cycle13_wave5_season_generation.py` errors as **pre-existing on HEAD, git-stash-proven**, living
in rocket's `season_generation_pipeline.py` cell-grain contract — not this seam, and not new today.

**⚑ COVERAGE BOUNDARY, DECLARED (#70).** My full-tree command ended in `| tail -25`, so **I captured
only the last 25 lines**: 21 named `ERROR` rows (all `test_cycle13_wave5_season_generation.py`) and 3
named `FAILED` rows (`test_wr2_d_nova_telegraph.py` ×2, `test_wr1_m12_gd_mitigation_nova.py` ×1). The
remaining **~60 failures are UNNAMED — I do not know what they are**, and nothing above should be read
as characterising them. What I *can* say about all 84 is reason (1)–(4): none can be caused by this
lap, whatever they are. Routed as HB-8.

---

## 8. Anti-pattern compliance — "do NOT widen v2 to hide them"

| Check | Result |
|---|---|
| Was the v2 exclusion ever broadened beyond `src/**/output/`? | **NO** — the same predicate `^src/` minus `^src/(.*/)?output/` was used in the pre-census, every intermediate check, and the post-census |
| Was any residual disposed by redefining the surface rather than acting on the file? | **NO** — 10/10 disposed by act: 6 committed, 1 relocated, 3 gitignored |
| Do the `.gitignore` patterns hide anything beyond their 3 named targets? | **NO** — control probe, § 4; two are exact paths with zero glob, the third globs only a timestamp |
| Was either `.py` filed somewhere convenient to avoid adjudicating it? | **NO** — both adjudicated on measured evidence and they *split*, which is the outcome a hiding move would have avoided |

A `.gitignore` entry *is* a hiding instrument in general, which is why the three patterns are exact
paths / one-stem anchors and why the narrowness control probe is in the commit message, not just here.

### 8.1 Per-file self-audit — each disposition verified INDEPENDENTLY of the census

The § 6.1 census proves the *aggregate* is 0. It does not prove each file went where the § 2 table
says — a file could vanish from the census for the wrong reason. Each row re-checked against the
disposition it claims (`git ls-files --error-unmatch` for COMMIT, presence/absence for RELOCATE,
`git check-ignore -q` for IGNORE):

```
drax-SIGNED-encounters-delta-2026-07-22.md                  COMMIT   -> TRACKED ✓
2026-06-15-dodge-intrinsic-glass-close-st-math-note.md      COMMIT   -> TRACKED ✓
2026-06-20-str-bleed-emission-regression-diagnosis.md       COMMIT   -> TRACKED ✓
auto-amp-delete-flag-defer-2026-06-15.md                    COMMIT   -> TRACKED ✓
glass-cannon-boss-death-diagnose-2026-06-21.md              COMMIT   -> TRACKED ✓
step3_f3_boss_scale_smoke_2026_07_07.py                     COMMIT   -> TRACKED ✓
gamora_step3_f3_boss_scale_sweep_2026_07_07.py              RELOCATE -> gone from src/, present at scripts/ ✓
telemetry.db.pre-v2.21-backup-20260711T000000Z              IGNORE   -> IGNORED ✓
telemetry_seed.db-shm                                       IGNORE   -> IGNORED ✓
telemetry_seed.db-wal                                       IGNORE   -> IGNORED ✓
```

**10/10.** Two independent instruments now agree: the aggregate is empty *and* every individual
disposition is the one claimed.

---

## 9. Concurrency — jack-ryan Gate-2, disjointness verified

jack-ryan's Gate-2 on `08b87085` + `f573f171` ran in parallel. Discharged by hit table over a
mechanical file list, not by assertion (#72 clause 4).

**The complete set of files my three commits touch** — `git show --name-only --format='' 396aa4ad
d525fd05 97fb8f65 | sort -u`:

```
     1	.gitignore
     2	src/reincarnated/export/drax-SIGNED-encounters-delta-2026-07-22.md
     3	src/reincarnated/generation/notes/2026-06-15-dodge-intrinsic-glass-close-st-math-note.md
     4	src/reincarnated/generation/notes/2026-06-20-str-bleed-emission-regression-diagnosis.md
     5	src/reincarnated/simulation/math/auto-amp-delete-flag-defer-2026-06-15.md
     6	src/reincarnated/simulation/math/glass-cannon-boss-death-diagnose-2026-06-21.md
     7	src/reincarnated/simulation/notes/step3_f3_boss_scale_smoke_2026_07_07.py
```

**Intersection with the four named no-touch surfaces:**

| jack-ryan's surface | in my commit set? |
|---|---|
| `monster_stats.py` | absent |
| `data/kc2/t22_band_a_monster_stats.csv` | absent |
| `tests/test_kc2_monster_stats.py` | absent |
| `tests/test_kc2_locomotion.py` (incl. the `:716` region) | absent |

Plus the one file this lap **moved** — `scripts/gamora_step3_f3_boss_scale_sweep_2026_07_07.py` —
which is in none of those four either. **Intersection EMPTY. Disjoint. No hand-back on this axis.**

One shared surface does exist and is benign: `pytest tests/` (§ 7) *reads* the whole test tree
including jack-ryan's files. Reading is not touching, and the run writes only into
`src/reincarnated/output/` (§ 6.2b measured that growth).

---

## 10. Hand-backs

| # | To | Item | Blocking? |
|---|---|---|---|
| **HB-1** | **gandalf** (conductor; spec-owned) | CD-2 § 11.4's `tree_state_policy` 5-enum contains no legal value for `code-surface-v2`. Spec amendment owed. § 5.1. | Yes — blocks HB-2, blocks an honest v2 emission |
| **HB-2** | **star-lord** (export seam) | Implement v2 across `baton_v1_schema.py` (enum + selectable set + default + `TREE_STATE_IMPORT_SURFACE` exclusion), `baton_v1_emitter.py` (`engine_tree_state_detail` branch), `baton_v1_validator.py` (`G-CD2-POLICY` branch). § 5.2. | Yes — gated on HB-1 |
| **HB-3** | **gandalf** (conductor; design call) | `tree_state_untracked_entries_outside_src` semantics under v2 — keep literal (135, leaves v2's largest non-dirtying class unevidenced) or re-semantic to outside-code-surface (2,656, name/#67 + schema-migration cost). § 5.3. | Rides HB-1 |
| **HB-4** | **conductor, informational** | Three of the five committed notes sit in other seams (`export/` ×1 drax-authored, `generation/` ×2 rocket-authored). Committed unmodified, in place, and declared in `97fb8f65`'s message so the owning seams can re-home by `git mv` if they prefer. | No |
| **HB-5** | **conductor, informational** | The relocated sweep stays untracked at `scripts/` (Matt said *relocate*, not *commit*), so its only durable records are this note's sha256 and `d525fd05`. Banking it is a one-line follow-up if wanted. § 3.2. | No |
| **HB-6** | **conductor, informational** | All ten residuals share a five-second mtime window at `2026-07-29 03:48:40–44` despite content dates spanning five weeks and four seams — the residual set is the survivor set of ONE filesystem event, not accumulated drift. Mechanism UNRESOLVED-NAMED. Bears on whether the set can regrow. § 3.0. | No |
| **HB-7** | **conductor, informational** | Disk hygiene, noticed in passing, **NO disposition owed** (it sits in v2's excluded set): `src/reincarnated/output/w3_batch1_run_log.txt` is **4.09 GB** untracked, and carries the same `2026-07-29 03:48` mtime as the ten residuals — so it is probably from the same event as HB-6. Not touched here; v2 is clean with it present. Flagged only because 4 GB of untracked log is the kind of thing nobody discovers on purpose. | No |
| **HB-8** | **conductor — SUBSTRATE FACT, worth a look** | The **full** `tests/` tree is **63 failed / 10,373 passed / 21 errors** (21 min 48 s). The run's smoke is a six-module 244-test slice and is green; the tree behind it is not. Proven NOT caused by this lap (3 structural reasons + an A/B control, § 7.2), and the 21 errors are AGENT_STATE-documented pre-existing rocket-seam. **~60 of the 63 failures are UNNAMED** — my command truncated at `tail -25`. Whether a red full tree matters before the baton emits is the conductor's call, not mine. § 7.2. | Not for this lap |

---

## 11. Grades (R-KC2-7 vocabulary)

| Claim | Grade | Chain |
|---|---|---|
| Census = 10 residuals, zero delta vs Matt's count | **MEASURED** | § 1.3 tool output; per-class table § 1.4 |
| Zero tracked modifications at census | **MEASURED** | § 1.3 `[F]` empty |
| Smoke `.py` touched results | **MEASURED** | 7/7 GREEN run + live source lines + empty `tests/` grep, § 3.1 |
| Sweep `.py` is dead scratch | **MEASURED** | seed-base chain 67M↔69M + uncited 36.0 + zero importers + never tracked, § 3.2 |
| `.gitignore` patterns are narrow | **MEASURED** | `git check-ignore -v` positive + negative controls, § 4 |
| Each of the 10 landed as its table row claims | **MEASURED** | § 8.1 per-file self-audit, independent of the census |
| My commits are disjoint from jack-ryan's Gate-2 surfaces | **MEASURED** | § 9 hit table over the mechanical `git show --name-only` file list |
| `engine_tree_state: clean` under code-surface-v2 | **MEASURED** | § 6.1 post-census, both predicate limbs empty |
| v2 grade is invariant under sim activity | **MEASURED** | § 6.2b — re-measured mid-pytest; `[B]`/`[C]` +5, `[D]`/`[F]` unmoved |
| AC-11.4e FULL-capability passes | **MEASURED** | § 6.2 read-only predicate evaluation |
| `code-surface-v2` is unemittable today | **MEASURED** | § 5.2 — enum introspection + `BatonEmitError` + `G-CD2-POLICY` FAIL |
| All 10 residuals share one 5-second mtime window | **MEASURED** | § 3.0 `stat` output, all ten pasted |
| The mechanism that produced that window | **UNRESOLVED-NAMED** | § 3.0 — candidates named, none tested; outside the ruling's scope |
| Commissioned smoke 244/0, zero regressions | **MEASURED** | § 7.1 pytest output, six named modules |
| The full-tree 63 failures are not caused by this lap | **MEASURED** | § 7.2 — A/B control (identical failures with the file restored) + 3 structural reasons |
| What the ~60 unnamed full-tree failures ARE | **NOT-MEASURED** | § 7.2 — `tail -25` truncated the list; declared, not characterised (#70) |
| Authorship / run-date of the 2 `.py` | **UNRESOLVED-NAMED** | § 3.0; excluded from both verdicts by construction |
