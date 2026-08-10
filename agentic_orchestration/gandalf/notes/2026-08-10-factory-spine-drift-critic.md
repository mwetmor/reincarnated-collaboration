# Factory Spine v1 — DRIFT-CRITIC verdict

**Date:** 2026-08-10 · **Author:** gandalf
**Role:** ▶ ROLE: DRIFT-CRITIC — judging a build against a spec, and the spec is mine
**⚠ SWITCH: SPEC-AUTHOR → DRIFT-CRITIC** (I wrote Spec A; I am now judging its build. The seam is
declared because a spec's author is the worst-placed reader of its build and the best-placed
reader of its *departures*.)

**Under review:** `agentic_orchestration/factory/` @ `339c7216`
**Against:** `agentic_orchestration/gandalf/notes/2026-08-10-factory-spine-spec.md` (Spec A)
**Governing:** `agentic_orchestration/operating-procedures/software-factory.md` (D1–D5)
**Landing note:** `agentic_orchestration/star-lord/notes/2026-08-10-factory-spine-landing.md`
**Method:** read every module in the tree, ran the suite independently (136 passed, 1.69 s),
probed the CLI flag surface and the two sibling repos' ignore rules for the claims that depend
on them. Not a note-review.

---

## 0 · Verdict

**FAITHFUL WITH DRIFT.** The five laws are compiled — and three of them are compiled *harder*
than I specified. The build is not a plausible neighbor of Spec A; it is Spec A, plus judgment.

But two containment mechanisms are weaker than their prose, and one of them is weaker in the
exact place the founding run will put its whole weight. There is also an architectural inversion
the tree itself argues against in one file and authorizes in another.

Twelve findings below. **D-1 and D-2 are blocking for the founding run** (not for the landing —
the mechanical workflow is sound and its acceptance evidence stands). D-3 through D-9 are
sharpenings. D-10 through D-12 are what the founding run needs and the spine does not have.

Star-lord's own sentence is the standard I am holding this to: *"The line between them is now
enforced, not remembered."* Findings D-1, D-3 and D-6 are places where it is remembered.

---

## 1 · The O4 ruling — DROP the figure from the schema

**Ruling: remove `dollars` and `dollars_source` from the `phases` table, from `UsageBreakdown`,
and from `usage_totals()`. Keep the raw result frame on disk. This is a doctrine call and it is
mine to make; star-lord's labeling was the correct interim and is now superseded.**

The argument that decides it is not "labels are weak." Star-lord's label is good and the
plumbing is clean. The argument that decides it is **the figure carries no information the
ledger does not already hold.**

`total_cost_usd` is a deterministic function of (tokens × model × list price). We already store
all four token columns (`receipts.py:55-58`) and the model (`agent_sessions.model`,
`receipts.py:123`). Any dollar figure at any price table is therefore recomputable from receipts
at read time, forever, with the price table named at the point of computation. Storing the
harness's own imputation adds *zero* measurement and adds *one* misreadable claim. That is a
strictly negative trade in an evidentiary artifact.

Three supporting observations, each with a file:line, because the interim labeling already leaks
in three places:

1. **The label is hard-coded, not read.** `report.py:110-117` prints "harness-reported
   list-price imputation, NOT a billed amount on a subscription lane" as a **literal**, not from
   `dollars_source`. The per-phase renderer reads the source (`report.py:44-45`); the **totals**
   line does not. So the moment a genuinely metered lane exists, the totals line mislabels real
   money as imputed. The safeguard is already half-off.
2. **The total sums across sources.** `receipts.py:402` is `SUM(dollars)` with no `GROUP BY
   dollars_source` and no source in the returned dict. Imputed + real would silently become one
   number.
3. **`merge()` keeps only the first source.** `usage.py:118`:
   `dollars_source=self.dollars_source or other.dollars_source`. A retry that crossed lanes
   collapses two sources to one label.

None of these is a bug in star-lord's work; all three are the *shape* of the thing. A derived
number in a measurement table generates labeling obligations at every downstream surface, in
perpetuity, and each surface is a fresh chance to drop the label. The project's own law is
**reproduce the number from the artifact, not the report** (CL-3). $0.0672 has no artifact. No
money moved. It is the harness's model of a counterfactual.

**Forensics are preserved regardless.** The raw `result` frame is written verbatim to
`sessions/{run_id}/{phase}/raw_output.attemptN.jsonl` (`claude_code.py:103-105`) and the probe
sample ships as a fixture. What the harness *said* is retained; it just is not promoted into a
queryable column a dashboard can `SUM`.

**Re-entry path when the money is real.** A metered lane re-enters as `dollars_billed REAL` with
a `NOT NULL` companion `billing_source`, and the column is only creatable when an actual invoice
line exists behind it. The schema then asserts money only when money moved.

**Cost of the ruling:** one `SCHEMA_VERSION` bump (1 → 2) at the moment when the only consumer
in existence is `report.py`. This is the cheapest this removal will ever be. Every session that
passes makes it more expensive. That is the whole reason to rule now rather than "revisit at
schema v2."

**If Matt or star-lord veto the drop** (veto-open, as always), the minimum acceptable fallback is
all four of: rename the column `list_price_imputed_usd`; `dollars_source` NOT NULL whenever the
figure is present; `usage_totals()` refuses to sum across mixed sources and returns the source
set; `report.py` reads the label instead of asserting it. Partial adoption of that four is worse
than either endpoint.

---

## 2 · Where the compiled version is WEAKER than the prose

### D-1 · The permissions fingerprint is blind to gitignored writes — in every tree · **BLOCKING for the founding run**

`permissions.py:133-143` builds the change-set from `git status --porcelain`, which never lists
ignored paths, and `_signature()` (`permissions.py:58-85`) summarizes directories from
`git ls-files --others --exclude-standard` — deliberately excluding ignored files, with the
docstring naming the reason: to keep the factory's own gitignored `sessions/` and `receipts.db`
from reading as writes to a PROTECTED path.

That fix is correct and necessary. But it was applied **globally** to solve a **local** problem,
and the consequence is: *a write to any gitignored path in any repo is invisible to containment.*

This is not theoretical, and the tree contains its own proof. `kc2-baton-mechanical.yaml:93-95`:

> ``-p no:cacheprovider`` keeps pytest from writing .pytest_cache into a tree this run declares
> read-only. A read-only proof that writes is not a proof.

I checked: `.pytest_cache/` **is** gitignored in the engine repo. So had that flag been omitted,
pytest would have written into a declared read-only tree and the fingerprint would have reported
**nothing** — no breach, no abort, green run, and the YAML's own claim two lines earlier ("the
read-only claim is proved per phase, not asserted", lines 11-12) would have been false while
reading true. The mechanism did not catch it. The author caught it, by hand, in a comment.

That is the SSSF shape in our own tree: a law held by a person remembering rather than by
machinery refusing. Star-lord found the *first-order* containment hole in this same area (the
single-fingerprint gap, landing note § 5) and patched it well. The second-order hole opened by
the patch is unreported.

**Remedy (my recommendation; star-lord rules the implementation):** scope the exemption to its
actual subject. The blindness should apply to `agentic_orchestration/factory/` only — the
self-write carve-out — not universally. For trees declared in `read_only_trees`, fingerprint with
`git status --porcelain --ignored=matching`; the cost is bounded precisely because the expected
answer is "nothing moved," and a read-only tree that produces 2,800 ignored deltas has already
failed. For writable trees, keep the current cheap path but record in the receipt that ignored
paths were out of scope, so the run's forensic record does not overclaim.

### D-2 · The only way a mechanical phase can DO anything is through a gate · **BLOCKING for the founding run**

`runner.py:273-282`: a mechanical phase's `_execute()` synthesizes an envelope and returns. There
is no exec step at phase level. `PhaseSpec` (`workflow.py:44-56`) has no `command` field.
Therefore the only executable primitive available to a mechanical cell is
`command_succeeds` — a **gate** — whose own docstring invites the use
(`gates/core.py:335-341`): *"This is what a render/promote step runs under (R-BR-56's promotion
half), so that the write lands inside the phase window."*

And `gates/media.py:6-10` argues the opposite, in the same tree, about the same law:

> The promotion half is a separate phase in the workflow (`command_succeeds`), so that the
> promotion write passes through permissions fingerprinting like any other write — **a gate that
> mutated the tree would slip its own writes past the fingerprint.** The gate is PURE: it reads,
> it reports, it changes nothing.

The phase is separate; the mutating actor is still a gate. Spec A § 4 says gates run *post-hoc
against artifacts on disk*. A gate that produces the artifact it then adjudicates is not post-hoc,
and the containment hole star-lord found is the first symptom of the inversion, not an incident.
The double-fingerprint is the right patch and the wrong resting place: it makes the inversion
survivable rather than removing it.

The shipped workflow is clean — all three cells verify and nothing writes — so this is latent,
not live. It goes live the moment the founding run renders or promotes anything.

**Remedy:** add a phase-level `exec:` (or `steps:`) that runs between the before-fingerprint and
the gates, so the sequence becomes `fingerprint → exec → fingerprint → gates → verdict` with
execution and adjudication in different hands. Then withdraw the promotion invitation from
`command_succeeds`'s docstring and let it be what its name says.

### D-3 · `verdict_consistent` greens vacuously if it is not last

`gates/core.py:216-220`: with `run.prior_reports == []` and `status == "PASS"`, the gate returns
**PASS** — "all 0 prior gate(s) are green." Nothing in `workflow.py` enforces gate ordering, and
`runner.py:353` sets `prior_reports` incrementally, so a workflow listing `verdict_consistent`
first gets a green consistency verdict that consulted nothing.

The no-stub suite does not catch this: `test_no_stub_gates.py:166-189` proves a gate *mentions*
the world (`run.prior_reports` is in the `WORLD_TOUCHING` list) by source-text scan. It proves
syntax, not consultation. And `test_gates.py:148-151` explicitly *blesses* the empty-prior case
for a FAIL envelope — correct in itself, and it means the vacuous path is tested-in rather than
tested-out.

Every shipped phase happens to order it last. That is the author remembering again.

**Remedy:** the loader rejects a workflow where `verdict_consistent` is not the final gate of its
phase; or the gate returns NOT_RUNNABLE when `prior_reports` is empty *and* the phase declared
other gates (which requires the phase's gate list in `RunContext` — a two-line change at
`runner.py:342-350`).

### D-4 · The dollars label is asserted, not read

Covered in § 1. `report.py:110-117`, `receipts.py:402`, `usage.py:118`.

### D-5 · `changed_paths` discards repo identity — `diff_matches_claims` is repo-blind

`runner.py:347-348`: `changed_paths=[c.path for c in changes]`. `Change` carries `root`
(`permissions.py:100`) and even exposes a disambiguating `key` property
(`permissions.py:106-108`) — which nothing calls. So a change to `scenes/level.tscn` in the godot
tree and one in the meta-repo are the same string to `diff_matches_claims` (`core.py:163-167`).

The shipped run never exercised this: every phase declares `writes: []`, so the measured set was
empty and the gate passed on an empty subtraction. **`diff_matches_claims` has never adjudicated
a real write in a live run** — only synthetic single-repo paths in unit tests
(`test_gates.py:105-120`).

The founding run is multi-repo and writes. Fix before it fires: use `c.key` (or `repo/path`) and
normalize envelope claims the same way.

### D-6 · Harness names are unvalidated at load; `available()` is dead code

`workflow.py:180` accepts `raw.get("harness", "claude_code")` with no check against the harness
registry, while `workflow.py:1` declares the module's own doctrine: *"Fails at LOAD, not
mid-run."* A typo (`claude-code`) or a deliberate `codex` phase loads clean, runs the earlier
phases, and dies at the phase that names it — `get_harness` raises `KeyError`
(`harness/base.py:44-47`) or the stub raises `NotImplementedError` (`codex.py:27`), which
`Phase.__exit__` converts to a FAILED phase.

`CodexHarness.available()` exists (`codex.py:29-31`) and is called by exactly one thing: a test
(`test_harness.py:130`). The refusal is written and not wired.

### D-7 · A red phase's `notes_for_next_agent` travels unlabeled

`runner.py:118-119` carries the envelope's notes forward **before** the status check at line 120,
and `_build_prompt` (`runner.py:322-324`) renders them under "## Notes from the previous phase"
with no verdict stamp. Under `on_fail: continue`, the next worker receives a failed phase's
self-authored handoff as though it were a clean one. "Only failures travel" is enforced for gate
*output* and unenforced for envelope *notes*.

**Remedy:** stamp the verdict into the carried block, or refuse to carry notes from a non-PASS
phase.

### D-8 · `PROTECTED_ALWAYS` is root-repo-scoped, though the spec said "regardless of config"

`permissions.py:214`: the protected-path check applies only when
`change_root == Path(root).resolve()`. A workflow rooted in the engine tree with the meta-repo in
`repos:` gets no `canonical/` or `.claude/` protection from this clause — only the writes
allowlist, which is config, which is exactly what "regardless of config" was meant to survive.
Spec A § 8 named these unconditional. Low likelihood, high blast radius: make the check
root-agnostic by matching on repo-relative path in any repo whose name matches the meta-repo, or
by declaring protected paths per-repo.

### D-9 · Determinism is verdict-level, not evidence-level

`cli.py:81-85` compares `gate_verdict_tuples` = `(phase, gate, status)` (`receipts.py:421-429`).
Two laps agree if both greened, regardless of whether the digest, the frame count, the duration,
or the number of tests changed underneath. KC2's determinism claim was **digest-identical**; this
one is **verdict-identical**, and the printed banner ("DETERMINISM: EXACT") reads stronger than
what was compared.

The landing note's wording is accurate ("14 gate verdicts identical"). The banner is not, and the
banner is what gets quoted three sessions from now. Sharpen: hash the evidence dicts with
timing keys excluded, and report both — `VERDICTS: EXACT · EVIDENCE: EXACT/DIFFERS`.

Secondary: `factory determinism` runs the workflow twice **for real** with no idempotence guard.
Harmless for a read-only workflow; destructive for one that writes. Refuse (or require a flag)
when any phase declares a non-empty `writes`.

---

## 3 · What was quietly added

None of these is illegitimate — F0 authorized gate extensions and seam owners rule
implementation — but the spec did not author them and the ledger should say so:

| # | Addition | Where | Assessment |
|---|---|---|---|
| A-1 | `command_succeeds` — a seventh gate that **executes** | `core.py:327-342` | Legal as a gate addition; the execution semantics is D-2 |
| A-2 | `on_fail: continue` — a workflow-level continue-past-red | `workflow.py:72, 193-195` | Not in Spec A § 9's field list. Defensible (some runs want every phase's verdict) but it is the "keep going after red" switch and deserves an explicit ruling + the D-7 fix before it is used |
| A-3 | Mechanical phases never retry | `runner.py:247` | Correct and undocumented. A deterministic cell retried is a cell run twice for nothing. Fold into the spec |
| A-4 | `MAX_RETRIES = 3` | `workflow.py:29, 134-139` | star-lord's standing LLM-call-site rule, correctly imported. Keep |
| A-5 | `harness` · `artifacts` · `claim` · `notes` · `timeout_s` · `repos` · `read_only_trees` · `description` workflow fields | `workflow.py:44-56, 197-199` | All necessary, all benign. Ratified by use; name them in the spec's next revision so the New Run form has a closed field list to target |

---

## 4 · What is faithful — plainly, and in three places better than specified

- **Default-fail.** `phase.py` is stronger than § 2 asked. No override parameter exists; a second
  `finish()` is a protocol error (`phase.py:93-96`) on the grounds that a phase reporting twice
  does not know what it did; an unhandled exception is FAILED-with-traceback; gates can only
  downgrade (`phase.py:120-126`); exiting without `finish()` is FAILED with the reason recorded.
  I specified a floor and got a wall.
- **Synced triad.** Genuinely single-sourced from `_FIELDS` (`envelope.py:39-83`) — dataclass,
  JSON schema, and prompt block are all *generated*, not maintained in parallel. This is the
  strongest single piece of the build. Nine tests hold it.
- **NOT_RUNNABLE is red.** `gates/base.py:32-35` plus — and this is the better-than-specified
  part — `test_no_stub_gates.py:192-207` scans the whole tree for `status == FAIL` / `!= FAIL`
  comparisons and fails the suite if any exist, because that is the idiom through which
  NOT_RUNNABLE would silently become green. I did not think of that mechanism. It is the right
  one.
- **No stub gates.** Three independent proofs plus registry coverage
  (`test_gates.py:315-321`) so a new gate cannot land without a falsification pair. The
  string-blanking tokenizer that lets the modules *describe* the law without tripping the scanner
  that *enforces* it (`test_no_stub_gates.py:50-74`) is a small piece of craft with a real
  principle behind it: a law that cannot be written down is a law nobody reads.
- **Reasoning is not a fifth addend.** Enforced twice — `usage.py:81-96` and
  `receipts.py:414-418` — and asserted, not just commented.
- **Breach = abort, never retry.** `runner.py:186, 225-233`; permissions run **before** gates so a
  breaching phase can never be greened by its own gates (`runner.py:6-11`). The two rollback
  safety rules star-lord added — quarantine before delete, never restore over pre-existing dirt
  (`permissions.py:285-295`) — are additions I did not specify and would have. A containment
  mechanism that destroys uncommitted work is worse than the breach.
- **No `model` in workflows.** Enforced in two places, belt and braces:
  `workflow.py:127-132` at load and `claude_code.py:45-49` at argv build.
- **No `--dangerously-skip-permissions`, ever.** `claude_code.py:17`. Stated and honored.
- **O1's `--verbose` catch.** I verified the flag surface independently: `--agent`, `--tools`,
  `--allowedTools`, `--add-dir` all exist at the installed version, and passing both `--tools`
  and `--allowedTools` composes correctly. The `--verbose` finding was real and would have burned
  a phase before any API call. That is what VERIFY-AT-BUILD is for, and it worked.

---

## 5 · The honest stub — ruling

**It satisfies the law as I meant it, with one required addition.**

The law's content is not "no `NotImplementedError` in the tree." It is: **a verdict is never
green when nothing was checked.** SSSF's gap was `echo; exit 0` in a *verdict* position — a
checker asserting a pass it never earned. An adapter is a *labor* position. A labor position that
raises is a lane declaring itself closed, and a closed lane is a legible fact, not a laundered
one. `codex.py` declares `HONEST_STUB`, names T16, and raises; the raise lands as a FAILED phase
with a traceback in receipts. Nothing greens. The distinction is load-bearing and correctly drawn.

**The required addition:** the refusal arrives too late. It fires when the phase executes — after
every prior phase has already spent its wall time (and, in an agentic workflow, its tokens). The
adapter already knows the answer at load time: `available()` returns `False` (`codex.py:29-31`)
and nothing calls it. Wire it into `load_workflow`: a phase naming an unavailable or unregistered
harness is a **load error**, not a mid-run failure. That is D-6, and it converts the honest stub
from honest-eventually to honest-immediately, which is the entire point of default-fail.

With that wired, the stub is not an SSSF gap. Without it, it is a smaller cousin of one: a lane
that looks runnable right up until it isn't.

---

## 6 · UI tier ladder + the New Run form — ruling

**The gate does not move. Receipts existing is a floor, not a trigger.**

"No dashboard before receipts" is a *necessary* condition someone wrote down because it is the
condition most often skipped. It was never the *sufficient* one. The sufficient condition is in
the same § 7 row: **receipts schema stable across ≥2 compiled workflows.** We have one.

And the one we have is the wrong shape to authorize a dashboard, for a reason that matters more
than the count. Every phase in `kc2-baton-mechanical.yaml` is mechanical, so every usage column
in receipts is NULL-with-reason. Tier 2 is specified to answer four questions, and one of them is
***what did it cost?*** A cost panel built today would be built against a table that has never
carried a number. That is not a dashboard; that is a mockup with a database behind it — which is
the precise failure the doctrine names.

**Sharpened gate — Tier 2 unlocks when all three hold:**
1. ≥2 compiled workflows have landed with receipts;
2. **at least one is agentic**, so `input_tokens` / `output_tokens` / `cache_*` /
   `agent_sessions.model` are non-NULL and the four Tier-2 questions all have a column behind
   them;
3. `SCHEMA_VERSION` has not moved between them.

Note that the § 1 ruling deliberately moves `SCHEMA_VERSION` **now** — resetting condition 3 at
the only moment it is free, before any consumer exists. That is the argument for ruling on O4 in
this review rather than deferring it: the schema's stability clock should start *after* the
removal, not run through it.

**The proto-editor doctrine is unchanged and is in better shape than it was.** Two skins, one
spine; the New Run form emits a workflow file. What the build has quietly given the form is its
validation layer: `load_workflow` (`workflow.py:96-211`) fails at load with specific,
human-legible messages — the empty-gates refusal at `workflow.py:160-164` ("an unadjudicated
phase is a claim nobody checked") is a *form validation rule* already written in prose a person
can read. The form's job is to emit YAML this validator accepts, and the validator's error
strings are the form's field-level help text. That is a real gift to drax.

**The one prerequisite nobody has named yet:** the gate registry carries names only
(`gates/base.py:94-110`); gate *arguments* are `**kwargs` with no machine-readable schema. A form
cannot render the `expected` / `size_bytes` fields for `sha256_matches`, or the
`min_duration_s` / `expect_streams` fields for `ffprobe_verifies`, without introspecting each
signature. Add an args schema to the registry (derivable from `inspect.signature` + type hints)
and expose it as `factory gates --json`. That is a small star-lord task and it is on the
critical path for Tier 2 — worth landing well before drax starts, not during.

---

## 7 · What the founding run needs and the spine cannot yet do

The founding run is the KC2 baton scene build: a Godot scene authored from the baton alone. Five
gaps, ordered by how early they bite.

**D-10 · There is no HALT. This is the largest gap.**
`RunResult.status` is `PASS | FAIL | ABORTED` (`runner.py:51`). The charter layer's central verb
is *halt to Matt at commitment boundaries* (desirable-run-pattern), and the strategy's own § 6
refusal is *owner-eye is load-bearing and never automated* — BR-2's two gates that passed while
failing are the founding evidence. The spine has no expression for either. A run that reaches a
commitment boundary can only pass it, fail it, or abort — and "abort" throws away the run.

**Remedy that does not automate the eye:** a `HALT` session status plus a gate
`awaits_owner_eye(token_path)` that is NOT_RUNNABLE by construction until a human writes a
countersign file at a declared path. Red until a person acts, red forever if nobody does, and the
countersign is a human artifact the gate *reads* rather than a judgment the gate *makes*. This is
the NAMED-ABSENT-DECLARED pattern from KC2, compiled. It is the single highest-value addition
before the founding run charters.

**D-11 · No agentic phase has ever run end-to-end.**
`extract_envelope` has never met a real Claude Code final message. The likeliest first-contact
failure is `envelope.py:105-107`: **unknown fields are a hard rejection.** A worker that adds one
helpful key — `"gates_i_expect_to_pass"`, `"open_questions"` — gets `EnvelopeError`, no envelope,
and burns a retry. The strictness is right (it is the anti-drift mechanism) but it should meet
reality on a cheap call, not on the founding run's first phase.

`factory probe-agent` (`cli.py:97-120`) verifies the lane and prints the usage frame; it does not
assert an envelope round-trip. Extend it — or add `factory probe-envelope <seam>` — so one live
call proves prompt-block → worker → `extract_envelope` closes. One call, one afternoon of risk
removed.

**D-12 · The containment surface the founding run will actually lean on is the weakest one.**
The shipped workflow declares `~/Games/reincarnated-godot` **read-only**. The founding run must
write there. The moment it comes off the read-only list, containment is the writes allowlist plus
git visibility — and Godot writes `.godot/` and import caches constantly, all gitignored, all
invisible per **D-1**. The founding run is the first run where D-1 stops being theoretical. Fix
D-1 first; it is not optional for this run.

**D-5 again, concretely.** The founding run writes to a repo that is not the workflow root, so
`diff_matches_claims` compares repo-blind path strings. Fix before it fires.

**Timeouts.** `tests_pass` defaults to 1800 s (`core.py:321`) and phases to 3600 s
(`workflow.py:53`). A Godot import + headless render cell can exceed both. Configurable — just
needs to be set deliberately in the charter rather than discovered at minute 30.

**What the spine handles fine and should be trusted with:** the digest pin on the baton
(`sha256_matches` is exactly right and its size cross-check can red independently), ffprobe
verification of any render, the headless test wall, the session dir as forensic record, and
receipts as the run ledger's mechanical shadow. The mechanical fraction of the founding run is
genuinely compiled. It is the *boundaries* — write containment, owner-eye halt, the agentic
handoff — that are not.

---

## 8 · Recommended disposition

**The landing stands.** Spec A § 11 items 1–4 are proven and I verified the suite independently.
Nothing here retracts the acceptance. Item 5 (jack-ryan Gate-2) remains blocking for the first
compiled agentic workflow, correctly.

**Before Gate-2 sits** (cheap, and jack-ryan should see them resolved rather than queued):
D-6 (harness validation at load — wires the dead `available()`), D-3 (verdict_consistent
ordering), D-7 (verdict-stamped carried notes).

**Before the founding run charters:**
D-1 (gitignore blindness, scoped exemption), D-5 (repo-qualified change paths), D-10 (HALT +
`awaits_owner_eye`), D-11 (envelope round-trip probe). D-2 is the architectural one — an `exec:`
step at phase level — and it is the right time to do it, because the founding run is the first
workflow that needs it and retrofitting after two more workflows exist costs more.

**O4:** drop `dollars` / `dollars_source`, bump `SCHEMA_VERSION` to 2, keep the raw frames. Ruled.

**Ledger tail:** the § 3 additions table (A-1…A-5) should ride into Spec A's next revision so the
spec and the tree agree on the workflow field list — the New Run form needs a closed one.

---

**Signed:** gandalf — DRIFT-CRITIC, 2026-08-10.

*Three sharp objections were requested. There are twelve, and I would trade eleven of them for
D-1 alone: the containment mechanism has a blind spot that the workflow's own comment was written
to compensate for. Everything else in this tree is enforced. That one is remembered.*
