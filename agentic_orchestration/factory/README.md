# factory — the spine

**Built by:** star-lord (ruling D4)
**Against:** `agentic_orchestration/gandalf/notes/2026-08-10-factory-spine-spec.md` (Spec A)
**Strategy of record:** `agentic_orchestration/operating-procedures/software-factory.md`
**Status:** v1 landed 2026-08-10. Spec A § 11 acceptance items 1–4 mechanically proven
(item 5, jack-ryan Gate-2, is queued — no compiled *agentic* workflow runs before it).

This is the SPINE layer of CHARTER / SPINE / LABOR. It does not decide what work is
worth doing (charter) and it does not do the work (labor). It runs phases, adjudicates
their claims against the disk, and writes receipts.

---

## The five compiled laws

Everything in this package exists to make one of these mechanical rather than
aspirational. Each has a test that reds when the law is broken.

| Law | Where it lives | Where it is proven |
|---|---|---|
| A phase is FAILED until exactly one `finish()` collapses it — **no override exists** | `phase.py` | `tests/test_phase.py` |
| Dataclass, JSON schema and prompt block are **one field table** | `envelope.py` | `tests/test_envelope_triad.py` |
| Gates adjudicate the world, never the envelope's word; **NOT_RUNNABLE is red**; **zero stubs** | `gates/` | `tests/test_gates.py`, `tests/test_no_stub_gates.py` |
| A write outside the allowlist is **quarantine + rollback + ABORT**, never a retry | `permissions.py` | `tests/test_permissions.py` |
| **Only failures travel**; reasoning tokens are a share of output, **never a fifth addend** | `gates/core.py`, `usage.py` | `tests/test_gates.py`, `tests/test_usage.py` |

## Layout

```
factory/
  phase.py         default-fail phase primitive
  envelope.py      the synced triad (one _FIELDS table -> dataclass + schema + prompt)
  gates/           base.py (registry, GateReport, RunContext)
                   core.py (the v1 six + command_succeeds)
                   digest.py (sha256_matches)  media.py (ffprobe_verifies)
  permissions.py   before/after tree fingerprinting, classify, quarantine, rollback
  harness/         claude_code.py (LIVE)   codex.py (HONEST STUB, blocked on T16)
  receipts.py      SQLite/WAL, 7 tables + schema_meta, SCHEMA_VERSION = 1
  runner.py        phases in order; fingerprint -> execute -> fingerprint -> permissions
                   -> gates -> fingerprint again -> phase verdict
  workflow.py      YAML/JSON loader; every refusal happens at LOAD
  report.py        renders from receipts only (one data path)
  cli.py           run · status · report · gates · determinism · probe-agent
  workflows/       kc2-baton-mechanical.yaml (the founding run's mechanical cells)
  tests/           247 tests, all green
```

## Use

```bash
cd agentic_orchestration/factory

./factory gates                                   # what can adjudicate a claim
./factory run workflows/kc2-baton-mechanical.yaml # run it
./factory status                                  # recent runs, from receipts
./factory report <run_id>                         # the full receipt, rendered
./factory determinism workflows/<wf>.yaml         # two laps, compare gate verdicts
./factory probe-agent <seam>                      # smoke the live harness lane
```

Nothing here writes to a remote, and nothing here runs `--dangerously-skip-permissions`.

## Why the runner fingerprints twice

Mechanical cells do their work *inside* a gate command (`tests_pass` /
`command_succeeds`), so a write made by the command itself lands after the
post-execution snapshot. A single check would let a gate's own writes escape
containment. The second pass aborts with `during="gate execution"` so the receipt
says which side of the boundary the breach came from.

## What "the tree was clean" is worth

Containment is a git change-set diff, so it is only as good as what git will
describe. Five rules keep the claim honest, each one added closing a Gate-2 finding
that had the *same shape*: a predicate answering a slightly different question than
the one asked, whose wrong answer is always `clean`.

1. **Gitignored is not exempt.** `git status --porcelain` never reports ignored
   paths, so the v1 build was blind to the engine's `seasons/` and `telemetry.db`
   — inside a tree the workflow declares read-only. Status is now read with
   `--ignored=traditional` and the collapsed entries are swept. The only exemption
   is `FACTORY_RUNTIME_PATHS`: six named paths, root repo only, recorded on the
   fingerprint whenever one is taken.
2. **Unmeasurable is not clean.** A declared repo that is not a git worktree used
   to produce an empty diff, and an empty diff reads like innocence. Such a repo
   now fails at LOAD; a snapshot that fails mid-run raises `ContainmentError`.
3. **Coarse is declared as coarse.** A region over 50,000 files (the godot tree's
   `.godot/` + `Assets/Synty/` = 259k) falls back to directory mtimes: catches
   creation, deletion, rename; **misses in-place content edits**. Every phase emits
   a `containment_coarse` receipt naming the regions and the caveat. A test asserts
   the blind spot exists, so the caveat can only be weakened on evidence.
4. **A fence is judged where the artifact IS.** `read_only_trees` is matched on the
   path's lexical *and* resolved form, breaching on either. `.resolve()` alone
   follows symlinks, so a link planted inside a fenced tree was judged by where it
   *pointed* — a link to `/tmp` walked straight out of the fence (H1).
5. **Unreadable is not clean.** `git status` reports a directory it cannot descend
   into on **stderr**, with exit code 0 and nothing on stdout, so a `chmod 000`
   subtree measured as untouched. Warned paths are folded into the fingerprint:
   unreadable at both ends is unchanged, unreadable at one end is a change.
6. **The status output is parsed with `-z`, and both ends of a rename are fenced.**
   Porcelain v1 C-quotes special paths and uses ` -> ` as its rename separator — a
   delimiter a filename can legally contain. Keeping only the last field dropped the
   rename SOURCE, so `git mv` out of a fenced tree named only a legal destination and
   passed; and a file named `junk -> src` parsed to `src`, a real path the rollback
   then deleted. `-z` is NUL-separated, never quoted, and emits the rename origin as
   its own record.
7. **Rollback never deletes tracked content.** A `created` path cannot contain
   anything git already tracks; if it does, the path identification is wrong and the
   deletion is refused with a reason. This does not depend on knowing which parse bug
   produced the bad path. Containment must never be the thing that destroys work.
8. **Empty directories are swept on the read-only trees.** git tracks content, so a
   wholly-empty directory tree is invisible at every porcelain setting. This was
   declared as a bounded blind spot and then closed: it is not inert (a bare directory
   is a PEP-420 namespace package; a new `res://` directory enters Godot's import
   scan) and a structure-only walk — no stats — costs 0.21 s for the engine and
   1.69 s for godot.

**The wall.** `tests/test_containment_wall.py` is the standing answer to that
repeated shape — thirteen artifact kinds (regular file, symlink out of the tree,
broken symlink, nested dir, collapsed untracked member, gitignored file, nested git
repo, unreadable subtree, a quoted path containing the rename delimiter, a path with
a newline, a hard link, a mode-only change, a directory replacing a file) each run
through four rounds: the change-set must **name** the artifact (not merely be
non-empty — the first draft asserted only non-emptiness, which is the module's own
disease in the one assertion meant to cure it), it must be **fenced** under
`writes: ["**"]`, the rollback must **report the undo honestly** (a `deleted` action's
path must be gone, a `restored` action's path must be present, a `NOT_ROLLED_BACK`
must carry a reason), and every **residue** left on disk afterwards must be named by
some action. Each round has a falsification partner requiring the same artifact to be
*allowed* where it is declared. The wall found rule 5 on its first run. A new
containment question of this shape should be a new row, not a new reviewer finding.

**Why the mechanical lane is easier than it looks.** Every path a mechanical workflow
touches is authored by a human in a YAML file under review, so the adversarial-filename
class (rule 6) is unreachable there. That is a property of its *inputs*, not of its
code — the moment a phase's paths come from a model's output the immunity is gone. It
is written down here so no one mistakes the mechanical lane's clean record for
evidence that the parser is safe.

**What the rollback promises.** Not that the artifact is always removed — nothing is
deleted unquarantined, so evidence that cannot be safely quarantined is deliberately
left in place and named. The promise is that the receipt and the disk agree: an
artifact never survives while the receipt says `deleted`.

Gate commands run with `PYTHONDONTWRITEBYTECODE=1` and
`PYTEST_ADDOPTS=-p no:cacheprovider`. Running pytest inside a read-only tree writes
`__pycache__` there, which is a real breach; the fix is to stop the write, not to
exempt the path.

## Session-local state (gitignored)

`sessions/` and `receipts.db` are runtime artifacts, not source. They are ignored
at the meta-repo root so that the factory's own writes never read as tree changes
during its own fingerprinting — `tests/test_permissions.py` pins that behavior.

## The open items, as resolved

Spec A § 13 asked four questions. All four were probed live before any code was
written (claude 2.1.119, Python 3.12.0, this host, 2026-08-10):

- **O1 — flag co-support:** CONFIRMED. `--agent` + `-p` + `--output-format stream-json`
  work together. **`--verbose` is mandatory** alongside stream-json in print mode; without
  it the CLI exits 1 *before any API call*. The adapter passes it unconditionally.
- **O2 — usage fields:** `input_tokens`, `output_tokens`, `cache_read_input_tokens`,
  `cache_creation_input_tokens`, `total_cost_usd`, `modelUsage{}`. No `reasoning_tokens`
  key was present → reasoning is NULL with a reason, never folded into output.
- **O3 — PyYAML:** present (6.0.3). `.json` workflows load through the same validator
  if it ever goes missing.
- **O4 — dollars: SPEC DELTA.** The spec expected `total_cost_usd` to be NULL on a
  subscription lane. It is **populated** ($0.0672 for a 4-output-token call). It is a
  harness-computed **list-price imputation**, not money billed — the Max subscription
  is flat. The schema therefore records the figure *and* `dollars_source`, so no
  downstream surface can report it as spend. Flagged to gandalf as DRIFT-CRITIC input.

## What is deliberately not here (Spec A § 12)

No dashboard, no scheduler, no queue, no sandbox, no model pinning in workflow files,
no cost optimizer, no auto-merge. Tier-0 is a terminal surface reading receipts.
UI does not advance a tier before receipts exist to render.

## Custody

Receipts schema custody is star-lord's (strategy § 8). A schema change gets a
MIGRATION note before it ships, because gate consumers and any future Tier-2 surface
read these tables. `schema_meta.schema_version` exists so a consumer can refuse an
unknown version rather than guess at it.
