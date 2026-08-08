# KC2-SIM Phase D — the three pre-registered star-lord items

**Author:** star-lord (export / output / telemetry / LLM seam)
**Commission:** gandalf `RUN-CONDUCTOR`, KC2-SIM Phase-D, commissioned at the L-41 close
**Binds:** BEFORE the Phase-E baton emit
**Source artifacts read:** jack-ryan Gate-2 `2026-08-08-kc2-gate2-phase-c.md` §§ 4–5 ·
run ledger `2026-08-07-kc2-sim-run-ledger.md` rows **L-31** / **L-34** (READ-ONLY, not edited) ·
own Phase-C report `2026-08-08-kc2-baton-emitter-report.md` · engine `export/` seam
**Engine commit:** `a53c97fc` (8 files, +858 / −54) on `main`
**Battle spec:** NOT edited (guard honoured). The § 11 schema row for CD-2 is transcribable
verbatim from § 2 below.
**Push:** NOT fired. Awaiting Matt.

---

## 0 — Verdict table

| item | status | evidence |
|---|---|---|
| **S-W2** — in-repo pin | **DONE** | 3 new always-running tests + checked-in golden + provenance sidecar |
| **S-I1** — AST-scan extension | **DONE** | scan covers 5/5 modules, asserts its own scope, and gained a positive control |
| **CD-2** — `tree_state_policy` provenance field | **DONE** | 2 additive `sim_pin` fields, `G-CD2-POLICY` check, 9 new tests incl. a real scratch git repo |

**Tests:** `tests/test_baton_v1.py` **35 → 51 green**. `tests/test_kc2_*.py` (gamora's) **128 green,
untouched**. No test deleted, none weakened, no `xfail` added.

**Coupling taken on gamora:** one read-only constant compare. `count_model_provenance()` is **NOT**
consumed — see § 5.

---

## 1 — CD-2: field semantics, VERBATIM for transcription into spec § 11

> The conductor lands the § 11 schema row. Everything below is the exact implemented shape; it is
> written so the row can be copied out of it without reading the code.

### 1.1 Location and names

Both fields are on **`sim_pin`**, adjacent to `engine_tree_state`. They live there and not in
`provenance` deliberately: the ruling's own phrasing is *"a `clean` without its policy is an
unrecorded claim"*, so if the grade and its policy sat in different blocks a consumer reading
`sim_pin` alone would still be holding the unrecorded claim.

| field | type | nullable | default |
|---|---|---|---|
| `tree_state_policy` | string enum (5 values, § 1.2) | yes | `null` |
| `tree_state_untracked_entries_outside_src` | integer ≥ 0 | yes | `null` |

Both are **ADDITIVE and optional-defaulting**. A baton emitted before this ruling still validates
against the model, and validates *honestly* — as **policy not recorded** — rather than being
back-filled with a policy it never ran under. (Back-filling would manufacture exactly the false
provenance claim CD-2 exists to prevent.) The **emitter always sets both** on the paths where they
apply; `G-CD2-POLICY` fails any baton where `tree_state_policy` is absent.

### 1.2 `tree_state_policy` — the complete value set, and when each is emitted

The vocabulary is **exhaustive by construction**: every code path in the emitter that can produce an
`engine_tree_state` produces exactly one of these names. There is no unnamed path.

| value | rule it names | emitted when |
|---|---|---|
| `code-surface-v1` | **THE RULED DEFAULT (CD-2, L-31).** dirty ⟺ (any tracked modification, anywhere) OR (any untracked path under the import surface `src/`). Untracked paths outside `src/` are non-dirtying and are COUNTED. | the tree was measured and the caller took the default (or passed it explicitly) |
| `any-change-v1` | dirty ⟺ `git status --porcelain` emits ANY line, tracked or untracked, anywhere. (The pre-ruling conservative default.) | the caller selected it |
| `tracked-only-v1` | dirty ⟺ any tracked modification anywhere; ALL untracked ignored, including under `src/`. (The pre-ruling `--allow-untracked` behaviour.) | the caller selected it, or passed the deprecated `--allow-untracked` |
| `declared-override` | the state was **DECLARED** by the caller via the `tree_state_override` fixture hook and **NOT measured**. | `build_baton(..., tree_state_override=...)` was used. Production callers leave the hook `None`; a `log.warning` fires when they do not. |
| `unavailable` | git could not be interrogated (not a repo / no git / non-zero exit / timeout). The state is **forced `"dirty"`** — clean cannot be PROVEN — and the reason ships instead of being swallowed. | `git status` was unreachable |

`code-surface-v1` / `any-change-v1` / `tracked-only-v1` are **selectable**. `declared-override` and
`unavailable` are **produced by code paths and are never selectable** — passing either to
`engine_tree_state_detail()` raises `BatonEmitError`, so a caller cannot hand-declare "git was
unavailable" on a tree where it was fine.

### 1.3 `tree_state_untracked_entries_outside_src` — when it is set, and what it counts

| policy | value |
|---|---|
| `code-surface-v1` | integer ≥ 0 — the ruling's "recorded count" limb |
| `any-change-v1` | `null` — this policy draws no inside/outside line, so a number would be a fiction |
| `tracked-only-v1` | `null` — same |
| `declared-override` | `null` — nothing was measured |
| `unavailable` | `null` — nothing could be measured |

**⚑ ENTRIES, not files — and the name says so on purpose.** `git status --porcelain` at its default
`--untracked-files=normal` **collapses a wholly-untracked directory into ONE line**, so a directory
holding 400 run artifacts counts **1**. This was measured, not assumed: the field's first draft was
named `tree_state_untracked_outside_src`, and a scratch-repo test (5 files in one untracked
directory) returned 1 rather than 5. The field was renamed **before anything shipped**. A reader who
took an entry count for a file count would under-report by whatever the directory holds — the quiet
kind of schema drift.

`-uall` would count files, but it is a known performance hazard on a tree carrying thousands of
artifacts **and it changes no clean/dirty verdict**: the collapsed entry keeps its directory path, so
the import-surface prefix test still sees it. The count is provenance colour; the grade is the claim.

### 1.4 The emitted block, from a real build at `a53c97fc`

```json
{
  "engine_tree_state": "dirty",
  "engine_version_full": "a53c97fcf920d5551c6cb9c43536f97f8277fe9f",
  "engine_version_sha": "a53c97f",
  "rng_algorithm": "python-random-Mersenne-Twister",
  "seed": 42,
  "sim_module_version": "kc2-sim-fixture-0.1 (SYNTHETIC — not a calibrated run)",
  "tree_state_policy": "code-surface-v1",
  "tree_state_untracked_entries_outside_src": 135
}
```

### 1.5 The new boundary check

**`G-CD2-POLICY`** — individually addressable like every other check (28 now, was 27). Fails when:

1. `tree_state_policy` is absent or `null` → *"engine_tree_state=… without the rule that produced it
   is an unrecorded claim (CD-2, L-31)"*
2. the policy is not one of the five named values
3. policy is `code-surface-v1` but no count was recorded → the non-dirtying half of the rule left no
   evidence
4. a count is present but is negative, non-integral, or a bool
5. policy is `declared-override` / `unavailable` **and** a count was recorded — a policy that
   measures nothing must not carry a measurement

**Carried as a `G-` id, not `AC-11.4i`, on purpose.** The `G-` namespace is this seam's own
discipline; the `AC-11.4x` namespace is the spec's, and **the conductor lands the § 11 row**.
Renaming it is one line in the `CHECKS` dict if he wants it in the AC namespace.

`AC-11.4e`'s refusal message now also names the policy, so a refusal says *which rule* produced the
`dirty` it is refusing on.

---

## 2 — ⚑ The finding the conductor needs before Phase E

**`code-surface-v1` is implemented LITERALLY.** The ruling names a PATH (`src/`) and glosses it *"the
import surface"*. The path is what I implemented, for two reasons: a path prefix is exactly
reproducible by anyone reading the ruling, whereas a judgement about what is "importable" is not; and
the literal reading errs toward `dirty`, which is the safe direction for a provenance claim. I did
not reinterpret the ruling.

**On this repo's layout, that makes the ruled rule ≈ `any-change-v1`.** Measured at this lap:

| measured on `reincarnated-engine` | count |
|---|---|
| untracked entries, total | 2,537 |
| untracked entries **under `src/`** ⇒ dirtying | 2,403 |
| … of those, under a `/output/` path segment | **2,393 (99.6 %)** |
| … of those, `.py` files | **2** |
| … of those, other (5 `.md` notes · 1 telemetry `.db` backup · 2 sqlite WAL/SHM sidecars) | 8 |
| untracked entries **outside `src/`** ⇒ counted, non-dirtying | 134 |

**Why:** the engine's runtime artifact directory is **`src/reincarnated/output/`** — it lives INSIDE
`src/`. So the ruling's stated intent (*"untracked artifacts elsewhere = recorded count,
non-dirtying"*) finds almost nothing to apply to here: the artifacts are not elsewhere, they are
inside the import surface. The non-dirtying limb catches 134 of 2,537.

**This is a conductor call, not a seam call.** I implemented as ruled and shipped it. If he wants the
rule to deliver its stated intent, the two obvious refinements are a `code-surface-v2` scoped to
`*.py` under `src/`, or `src/` minus `src/**/output/`. I am not proposing one; I am reporting the
measurement.

**Consequence for Phase E, stated plainly:** unless the engine tree is committed/cleaned before the
baton emit, or the rule is refined, the Phase-E baton grades **`dirty`**, and `AC-11.4e` then forbids
`calibration_grade: "FULL"`. The honorable fallback (charter § 7) is `PARTIAL`, truthfully declared.
Nothing about that is broken — but it should be a decision, not a surprise at emit time.

---

## 3 — S-W2: the verbatimness guard no longer skips into a no-op

**The finding:** `test_ac_11_4h_devotion_block_is_the_spec_text_verbatim` was the **sole** enforcement
of AC-11.4h / AC-9.2, and it `pytest.skip`ped when the collaboration repo was absent. On any other
host a MUST became a no-op with no signal.

**What landed — a chain, every link of which is asserted somewhere:**

```
spec § 9.5  →  goldens/*.value.txt  →  DEVOTION_ENVELOPE_DISCLOSURE  →  wire
  (cross-repo test,           (in-repo pins, ALWAYS run)        (AC-11.4h, validator)
   skips when absent)
```

- **`export/goldens/devotion_envelope_disclosure.value.txt`** — the § 9.5 block's VALUE,
  **extracted from the spec by script, never typed**. No trailing newline (the spec block has none;
  a byte-compare would otherwise fail). Loaded via `read_bytes().decode()`, not `read_text()`, so
  universal-newline handling cannot silently repair a CRLF-mangled golden into a false pass.
- **`export/goldens/devotion_envelope_disclosure.provenance.json`** — spec path · spec
  **sha256 `6aa777e192d1b3b1…`** · spec **git commit at extraction `135dfa8a3163…`** · the extraction
  pattern · the value's own sha256 / byte count (1,578) / line count (25) · the register key.
- **Three always-running tests:**
  1. constant ↔ golden (and `DEVOTION_ENVELOPE_DISCLOSURE_KEY` ↔ the recorded register key)
  2. golden ↔ **its own recorded digest** — a hand-edited golden is caught by its own sidecar, and
     the no-trailing-newline invariant is asserted
  3. the **cross-seam join**: `simulation.kc2.devotion.ENVELOPE_DISCLOSURE` /
     `ENVELOPE_DISCLOSURE_KEY` against the export constants
- **The cross-repo test is kept**, and now ALSO proves the golden has not gone stale against the
  spec — the one link the in-repo pins cannot check by themselves. Its skip message names what still
  covers the MUST, so a skip is no longer silent about its own consequences.

**Test 3 is the star-lord half of S-W1, landing early.** gamora's split has landed
(`ENVELOPE_DISCLOSURE_KEY` + value-only `ENVELOPE_DISCLOSURE`), and both seams now hold one scope,
asserted rather than assumed. jack-ryan's S-W1 action for me was *"at Phase-D wiring, assert the seam
join"*; this discharges it at the constant level. The manifest-routing assert (`sim_manifest[...] ==
schema.DEVOTION_ENVELOPE_DISCLOSURE`) still belongs at the actual Phase-D/E wiring call site and is
**not** yet written — it cannot be, because the wiring does not exist yet. Flagging it so it is not
lost.

---

## 4 — S-I1: the ADR-006 guard now covers the whole surface, and can fail

**The finding:** the AST guard scanned `emitter`, `schema`, `stub` — 3 of 5 — while MIGRATION claimed
*"writes NO row … and no row anywhere else."* The guard was narrower than the claim it was cited for.

**What landed:**

- Scans **all five** `baton_v1_*.py` modules (adds `baton_v1_validator`, `baton_v1_fixture`).
- **Asserts its own scope.** The scanned set is compared against `baton_v1_*.py` discovered on disk,
  so a sixth module joining the surface **fails the test** rather than silently re-narrowing the
  guard. This is the actual fix — adding two names to a tuple would have left the same failure mode
  in place for the next module.
- **`test_adr_006_guard_has_teeth`** — a positive control. The identical scan runs against
  `export/run_registry.py`, a real registry writer, and is **required to TRIP**. An absence-test that
  cannot fail proves nothing; this one is now demonstrably able to fail.

**Result:** no forbidden import (`sqlite3`, `run_registry`, `telemetry.db`, `telemetry.recorder`) and
no forbidden call (`register_run`, `execute`, `executemany`, `commit`, `connect`) in any of the five
modules. **ADR-006 posture unchanged; the evidence for it is now as wide as the claim.**

---

## 5 — Coupling taken on gamora's surface

**Seam boundary honoured: nothing under `src/reincarnated/simulation/kc2/` was edited.** Verified by
the commit's file list (8 files, all under `export/` or `tests/test_baton_v1.py`). Her in-flight
beat-3 files (`tests/test_kc2_micro_oracles.py`, `tests/test_kc2_opposition_wave_engine.py`,
`tests/test_kc2_s1_ramp.py`) were present as working-tree changes and were **deliberately left
unstaged**.

**`count_model_provenance()` is NOT consumed.** The brief flagged that its `p06_state` is moving to
RULED-OFF under her D-W1 rider this same window. It does not matter to this lap: CD-2 is *tree-state*
provenance and has no relationship to *count-model* provenance. The export seam imports nothing from
`wave_engine`. **Zero exposure to the `p06_state` change.**

**The one coupling taken, named:** `tests/test_baton_v1.py` imports
`reincarnated.simulation.kc2.devotion` **read-only**, to compare two string constants
(`ENVELOPE_DISCLOSURE`, `ENVELOPE_DISCLOSURE_KEY`). This is the coupling jack-ryan's S-W2 acceptance
shape explicitly sanctioned (*"or against `simulation.kc2.devotion`'s value once S-W1 aligns them"*)
and it is the S-W1 seam join. **Failure mode if gamora's lap moves that constant:** my test fails
with a message naming CD-5 and both seams — which is the correct signal, not a false alarm. The
export constant is independently pinned to the checked-in golden by a separate test, so a failure
localises to whichever side moved.

Directionally the other way: `tests/test_kc2_energy_devotion.py`, `test_kc2_micro_oracles.py` and
`test_kc2_run_surfaces.py` already import `export.baton_v1_*`. All **128 green** after my change.

---

## 6 — Evidence

| | |
|---|---|
| Engine commit | **`a53c97fc`** — *"star-lord: CD-2 tree-state provenance + S-W2 in-repo pin + S-I1 AST-scan extension (KC2-SIM Phase D)"* |
| Files | 8 changed, +858 / −54; 2 new (`export/goldens/*`) |
| `tests/test_baton_v1.py` | **51 passed** (was 35 at Phase C) — +9 CD-2, +3 S-W2, +1 S-I1 control, +3 supporting |
| `tests/test_kc2_*.py` (gamora's, 6 files) | **128 passed**, untouched |
| Validator checks | **28** addressable (was 27) |
| MIGRATION | `export/MIGRATION.md` — new dated entry above the Phase-C one, amending not replacing it |
| AGENT_STATE | `export/AGENT_STATE.md` — Phase-D session recorded |
| Spec note | **NOT edited** (guard honoured) |
| Run ledger | **NOT edited** (READ-ONLY, conductor-owned) |
| Push | **NOT fired** |

### Method notes worth keeping

- **The CD-2 rule is tested against a real `git` repo, not a mock.** A scratch repo is created,
  committed clean, then perturbed three ways (untracked outside `src/`, untracked under `src/`,
  tracked modification). CD-2 is a claim about what `git status` *means*; a mock would only re-assert
  my reading of it. That test is what caught the entry-vs-file collapse.
- **The three policies are asserted to disagree on one tree**, which is what makes the recorded name
  load-bearing rather than decorative.
- **The import-surface prefix is computed, not assumed** — re-expressed relative to
  `git rev-parse --show-toplevel`, because `git status --porcelain` prints repo-root-relative paths
  and a bare `src/` test inside a vendored checkout would silently match nothing and read every
  untracked module as non-dirtying.
- **`--allow-untracked` was retained**, not dropped, as a deprecated alias for `tracked-only-v1`
  (it prints a note; it errors on conflict with `--tree-state-policy`). Silently ignoring a flag a
  caller passed is the same class of failure as silently dropping a field.

---

## 7 — Open, flagged, not picked up

1. **The § 11 schema row for CD-2** — conductor's, per the guard. § 1 above is written for verbatim
   transcription.
2. **`code-surface-v1` vs this repo's `src/reincarnated/output/` layout** (§ 2) — conductor's call;
   bears on whether Phase E can grade `FULL`.
3. **The manifest-routing join assert** (`sim_manifest["devotion_envelope_disclosure"] ==
   schema.DEVOTION_ENVELOPE_DISCLOSURE`) — belongs at the wiring call site, which does not exist yet.
   Not lost; not written.
4. **S-I2** (spec § 11.6.1 `9–12 MB` → measured **17.4 MB**) — conductor-assigned in the Gate-2 table,
   not mine, not touched.
5. **S-I3** (no `Co-Authored-By` trailer on `68e2e372`) — noted; the Phase-D commit `a53c97fc`
   carries one. The Phase-C commit is not amended (history is not rewritten to fix a trailer).
6. **`tests/test_kit_space_emitter.py::TestMultiKitEmit`** 4 failures — pre-existing water→ice
   vocabulary residue, already routed to KR as a dispatch recommendation at the L-31 closeout. **Not
   picked up autonomously**, per the no-silent-pickup rule.
