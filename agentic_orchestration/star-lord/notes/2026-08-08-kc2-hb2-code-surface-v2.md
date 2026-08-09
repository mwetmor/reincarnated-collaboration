# KC2-SIM HB-2 — `code-surface-v2` plumbed across the baton emit surface

**Author:** star-lord (export seam)
**Date:** 2026-08-08
**Commission:** HB-2, conductor gandalf (RUN-CONDUCTOR), KC2-SIM run
**Authority:** Matt **R-KC2-11** (2026-08-08, option **(a+)**) · conductor **R-L71-1** (evidence
field, veto-open) · spec § 11.4 CD-2 field block (AMENDED L-71) + § 14 **F-11** · ADR-004 · ADR-006
**Engine commits:** `7e192537` (code + tests) · `3cb3bc2f` (MIGRATION.md + AGENT_STATE.md)
**Push:** NONE — R-KC2-10, commit-only; the conductor pushes and my commits ride as passengers.

---

## 1. What was owed, and what my own measurement said before this lap

The ruling was already made and gamora's disposition lap had already cleared the 10 residual
non-output entries. The tree therefore graded clean under v2 *by read-only census*. What did not
exist was the plumbing: my schema, emitter and validator only knew v1, and I had measured the
rejection myself —

```
BatonEmitError: unknown tree-state policy 'code-surface-v2'
G-CD2-POLICY  FAIL
```

This lap inverts exactly that measurement. Nothing about the ruling was re-litigated.

---

## 2. The semantics, stated where they cannot be missed

The exclusion is **`src/**/output/`** — a directory named `output` at **ANY DEPTH** under `src/`.
Not `src/reincarnated/output/`.

This is arithmetic, not pedantry. On this repo the **bulk** of the exhaust sits two levels down at
`src/reincarnated/simulation/output/`. A predicate anchored at depth 1 excludes almost none of it and
**reproduces v1's verdict while calling itself v2** — a policy field that lies about which policy
ran, which is the precise failure CD-2 exists to prevent. A first sweep read it the shallow way and
would have declared the ruling unexecutable; that misread was priced once already.

I carried the semantics in three places so a future reader cannot pick up only the shallow half:

- the constant `TREE_STATE_EXCLUSION_GLOB = "src/**/output/"` (the ruling verbatim), with the
  predicate's segment **DERIVED** from it — `…GLOB.rstrip("/").rsplit("/", 1)[-1]` — so the two
  cannot drift apart;
- the predicate `_is_code_surface_excluded()`, whose docstring names the misread and tabulates six
  worked path examples including the three near-misses;
- a test whose name is the claim: `test_cd2_v2_exclusion_matches_output_at_ANY_DEPTH`.

Matching is a **SEGMENT** test (`"/output/" in "/" + below`), never a substring test. `outputs/`,
`output_v2/` and a FILE named `output` all stay IN the code surface and all dirty the tree. All three
near-misses err toward `dirty`, which is the safe direction.

---

## 3. Line-cited diff summary — engine `7e192537`

### `src/reincarnated/export/baton_v1_schema.py` (+95 / −12)

| what | where |
|---|---|
| CD-2 header + per-policy doc block rewritten; v2 documented first as THE RULED DEFAULT, v1 re-labelled SUPERSEDED-but-SELECTABLE | `:485-532` |
| `TreeStatePolicy` Literal **5 → 6** members, `"code-surface-v2"` first | `:533-540` |
| `TREE_STATE_POLICIES_CODE_SURFACE` **NEW** — the two policies that owe an `..._outside_src` count, named once so emitter and validator cannot disagree | `:548` |
| `TREE_STATE_POLICY_DEFAULT` `"code-surface-v1"` → **`"code-surface-v2"`** | `:552` |
| `TREE_STATE_POLICIES_SELECTABLE` 3 → **4**, v2 first, v1 retained with the reason inline | `:559-561` |
| `TREE_STATE_EXCLUSION_GLOB` **NEW** (ruling verbatim) + `TREE_STATE_EXCLUSION_SEGMENT` **NEW** (derived) | `:565-581` |
| `SimPin.tree_state_untracked_entries_excluded: Optional[int] = None` **NEW FIELD** + the name-is-contract note added to `..._outside_src` | `:607-634` |

### `src/reincarnated/export/baton_v1_emitter.py` (+118 / −28)

| what | where |
|---|---|
| module docstring: the write-discipline bullet restated for v2 | `:31-38` |
| `TreeState` NamedTuple gains `untracked_entries_excluded: int \| None = None` — **appended WITH a default**, so every existing positional construction keeps working and keeps meaning what it meant | `:166-177` |
| `_is_code_surface_excluded()` **NEW** — the predicate, the misread, the six worked examples | `:218-252` |
| `engine_tree_state_detail()` docstring: v2 is the ruled rule; the old "MEASURED CAVEAT" paragraph promoted to "WHY v2 EXISTS" | `:255-298` |
| v1 branch split out explicitly (`excluded=None` — v1 draws no exclusion) and the **v2 branch added**: `in_src` splits again into `excluded` / `in_surface`; only `in_surface` can dirty | `:340-362` |
| `build_baton`: declared-override construction + `SimPin(...)` carry the new field | `:487-501` |
| CLI `--tree-state-policy` help re-cited to R-KC2-11; success line prints `untracked_entries_excluded` | `:935-939`, `:977` |

### `src/reincarnated/export/baton_v1_validator.py` (+45 / −6)

`_g_cd2_policy` at `:213-281`. Limb 1 (`..._outside_src`) widened from the hard-coded
`"code-surface-v1"` to `TREE_STATE_POLICIES_CODE_SURFACE` — v2 owes it too. Limb 2 **NEW**: under v2
`..._excluded` is MANDATORY and may be `0` but never `null`; under any other policy it must be
absent. `_not_a_count()` factored out and rejects `bool` explicitly (a `True` here would be schema
drift wearing a count's clothes). Check **ids** unchanged at 32 — the branch lands inside the
existing guard.

### `tests/test_baton_v1.py` (+357 / −37) — **86 → 98**

New: `git_run` fixture (hermetic git config, factored out of `scratch_repo`), `wire_v2` fixture
(self-asserts valid before any probe perturbs it), `_porcelain_untracked()` helper. Nine new tests;
four existing ones repaired for the default shift; the "unknown policy" probe re-pointed from
`code-surface-v2` (now real) to `code-surface-v3`.

---

## 4. Discriminating, not vacuous — written against Gate-2 **F-1**

F-1 caught a vacuous nullable test in another seam: a default that zeroed the code path for the whole
domain. The guard against repeating that here is not a claim, it is three artifacts:

**(a) The disagreement probe.** `test_cd2_v2_and_v1_grade_the_SAME_tree_differently` builds one
scratch tree with `src/pkg/output/run_001.json` and asserts **`v1.state != v2.state`** (v1 `dirty`,
v2 `clean`). If the exclusion did nothing, this test fails. The engine repo is itself such a tree —
that is the whole of F-11.

**(b) The pre-ruling probe.** `test_cd2_a_pre_ruling_v1_baton_loads_AND_VALIDATES_unchanged` **POPS**
the new key rather than setting it to `None`, because only the pop models an artifact written before
the field existed. It loads, round-trips, keeps its policy and count, and `G-CD2-POLICY` PASSES.

**(c) Two mutations injected, both caught, both reverted.**

| mutation | tests failed |
|---|---|
| depth-1 shallow misread — `below.split("/", 1)[0] == "output"` | **4** — `…SAME_tree_differently`, `…ANY_DEPTH`, `…partition_arithmetic…`, `…tracked_modification_still_dirties…` |
| substring not segment — `"output" in below` | **1** — `…is_a_SEGMENT_test_not_a_substring_test` |

`grep -rn MUTATION src/ tests/` returned only an unrelated pre-existing comment in gamora's seam
before I committed. A predicate wrong in either of the two ways this rule can be wrong does not
survive the suite.

---

## 5. MEASURED edge that decides verdicts — porcelain collapse vs the exclusion

`git status --porcelain -unormal` reports the **shallowest** wholly-untracked directory. A brand-new
`src/pkg/a/` containing nothing but `b/output/` is reported as `src/pkg/a/` — a path with **no
`output` segment** — so it is **NOT** excluded and the tree grades dirty.

Correct and safe: the ancestor is not an exhaust directory, it is a new subtree under the import
surface that happens to contain one. A predicate that looked *inside* a collapsed entry would let a
wholly-untracked package ship as `clean` because of what one of its children was named.

Found by a test failing (I had assumed the deep case would report at depth 4), confirmed against real
git, and now pinned twice: the ANY_DEPTH test commits its intermediate packages first — reproducing
the real engine layout, where `src/reincarnated/simulation/` is tracked and its `output/` is the
shallowest untracked entry — and `test_cd2_v2_a_collapsed_untracked_ANCESTOR_is_not_excluded` asserts
the collapse case on its own.

---

## 6. Acceptance — the measured rejection, INVERTED

Reproduction chain (R-KC2-7). Run at engine **`7e192537`**, **tracked modifications = 0**. All probe
output written to `/tmp` deliberately, so the probe could not dirty the tree it was measuring.

```bash
git -C ~/Games/reincarnated-engine rev-parse HEAD                          # 7e192537
git -C ~/Games/reincarnated-engine status --porcelain | grep -vc '^??'     # 0

# independent hand census — NOT via the emitter
git -C ~/Games/reincarnated-engine status --porcelain | grep '^??' \
  | sed 's/^?? //' > /tmp/sl_u.txt
wc -l < /tmp/sl_u.txt                                    # 2691   total untracked
grep -vc '^src/'          /tmp/sl_u.txt                  #  134   outside_src
grep '^src/' /tmp/sl_u.txt | grep -c  '/output/'         # 2557   excluded
grep '^src/' /tmp/sl_u.txt | grep -vc '/output/'         #    0   in-surface  ⇒ clean

# run-record: synthetic fixture + spec_pin resolved from the spec note
python3 -c "
import json; from pathlib import Path
from reincarnated.export import baton_v1_emitter as emitter
from reincarnated.export.baton_v1_fixture import make_synthetic_run_record
note = Path.home()/'Games'/'reincarnated-collaboration'/'agentic_orchestration'/'gandalf'/'notes'/'2026-08-08-kc2-sim-battle-spec.md'
rec = make_synthetic_run_record()
rec['spec_pin'] = json.loads(emitter.resolve_spec_pin(note).model_dump_json())
json.dump(rec, open('/tmp/sl_run_record.json','w'))"          # spec_pin COMMITTED, ebbc21f0b91a

python3 -m reincarnated.export.baton_v1_emitter \
  --run-record /tmp/sl_run_record.json --out /tmp/sl_baton_v2.json
python3 -m reincarnated.export.baton_v1_emitter \
  --run-record /tmp/sl_run_record.json --out /tmp/sl_baton_v1.json \
  --tree-state-policy code-surface-v1
```

**Output, verbatim:**

```
[baton_v1_emitter] OK — 428 events, 13 actors, 3 waves → /tmp/sl_baton_v2.json
  (grade=PARTIAL, tree=clean/code-surface-v2, untracked_entries_outside_src=134,
   untracked_entries_excluded=2558, player_id='player')

[baton_v1_emitter] OK — 428 events, 13 actors, 3 waves → /tmp/sl_baton_v1.json
  (grade=PARTIAL, tree=dirty/code-surface-v1, untracked_entries_outside_src=134,
   untracked_entries_excluded=None, player_id='player')

v2: state=clean policy=code-surface-v2  outside_src=134 excluded=2558
    G-CD2-POLICY = PASS | checks=32 | failures=[]
v1: state=dirty policy=code-surface-v1  outside_src=134 excluded=None
    G-CD2-POLICY = PASS | checks=32 | failures=[]

code-surface-v2: FULL grade ACCEPTED  (tree=clean) failures=[]
code-surface-v1: FULL grade REFUSED  -> AC-11.4e: engine_tree_state == 'dirty'
                 with calibration_grade == 'FULL' (tree_state_policy='code-surface-v1').
```

**Every acceptance criterion met:** emit under v2 succeeds · grades `clean` · both evidence fields
populated · `G-CD2-POLICY` PASS · **AC-11.4e FULL-capability discharged** (F-11's Phase-E
consequence). And the inversion is **isolated to the exclusion**: one tree, one minute, two rules,
two verdicts, with `outside_src=134` identical on both sides. AC-11.4e itself is **UNCHANGED** — it
keys off the grade, and only the grade moved.

### ⚑ Census invariance re-confirmed live

Hand census `excluded=2557`; the emit seconds later read **2558**, while `outside_src` (134) and
`in-surface` (0) **held**. That is the same live mechanism F-11's original +11 delta demonstrated —
the sim writes exhaust while you measure. It is the reason **no count is pinned** in the schema or in
any test against the live repo. The ARITHMETIC (`total = outside_src + excluded + in-surface`;
`clean ⟺ in-surface == 0 AND zero tracked modifications`) is invariant; the numerals are not, and a
test that pinned them would fail on whoever ran the sim next.

---

## 7. Smoke (Discipline #2)

| suite | result |
|---|---|
| `tests/test_baton_v1.py` | **98 passed** (was 86) |
| every module importing `reincarnated.export` (24 files) | **1,124 passed, 5 failed** in 17 m 35 s |

The 5 failures are **pre-existing and disjoint** — see hand-back (1).

---

## 8. Hand-backs — flagged, NOT self-assigned

Per my standing rule (2026-05-16): a flagged item in my seam without a knight-rider-authored dispatch
does not get picked up autonomously, however small. Both of these are one-liners. Neither is mine to
take today.

**(1) Five pre-existing export-adjacent test failures.** Surfaced by my own smoke run; untouched by
this change; zero baton imports; all fail in 0.3 s.

- `tests/test_kit_space_emitter.py::TestMultiKitEmit` ×4 — `AssertionError: 17 != 20` (kit count).
- `tests/test_cycle13_normal_season_export.py::TestRoundTrip::test_manifest_has_elements_block` —
  asserts `water` against a manifest carrying `ice`. That is drift from the **2026-07-12
  `water` → `ice` rekey recorded in my own MIGRATION log**: the export was rekeyed, this test was
  not. It is squarely in my seam and I would like a dispatch for it.

**(2) D2-6 remains OPEN, and this change makes it *asymmetric*.** D2-6 (Gate-2 Phase-D2, awaiting
dispatch) proposed widening the CD-2 count check to `policy != "code-surface-v1" and count is not
None`. I did not touch it. But the NEW field's guard is necessarily written the D2-6 way —
`policy != "code-surface-v2" and excluded is not None` ⇒ reject — because the commission rules the
field is set ONLY under v2. So `_g_cd2_policy` now holds both shapes side by side: the new field is
guarded tightly, `..._outside_src` still uses the narrow
`policy in ("declared-override", "unavailable")` check, and `any-change-v1` / `tracked-only-v1` can
still carry an `..._outside_src` count unchallenged. The inconsistency is now **visible in one
function** and is a one-line change whenever knight-rider dispatches it. Flagging, not closing.

**No hand-back owed on scope.** I touched only `export/` + `tests/test_baton_v1.py`. Gamora's
concurrent bundle (`simulation/`, `tests/kc2`, `scripts/`) never overlapped; his in-flight
`src/reincarnated/simulation/AGENT_STATE.md` modification was present in the tree at both my commits
and I did not stage it.

---

## 9. External-system posture (ADR-006)

No DB write. No LLM call. No push. The only writes were: two engine commits, one meta commit, and
three files under `/tmp`. The acceptance probe is read-only against git.
