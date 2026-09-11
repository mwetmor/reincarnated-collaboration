# Work across sessions

Purpose: make progress independent of chat memory, while improving methods only
from evidence. This is a workflow for the new painted-world suite, not a daemon
or promise that an agent keeps running after a session ends.

## Resume

1. Read repository charter routes and check authentication. Remain in the open
   lane unless explicitly adopting a free named seam; internal subagents stay off.
2. Read the painted-character-vfx skill, START_HERE and PROGRESS.json. Load the
   current gate/experiment and its direct dependencies, not every historical note.
3. Check exact relevant paths, repo state and any recorded running jobs. Inspect
   output/receipts before relaunching; interrupted calls may have completed.
4. Verify named evidence exists and matches hashes before relying on it. Missing
   evidence becomes UNVERIFIED and an explicit recovery task; do not repeat an
   expensive generation automatically. Refresh only facts/tool versions that
   matter to the current decision.
5. Choose one bounded experiment with a reviewable deliverable and closeout time.
   Announce the outcome being pursued; continue independently where possible.

## Work unit and limits

One session should normally finish one decision packet or experiment, not all
eight gates. Suggested sequence: native exemplar packet; projection/capability
probe; floor/style anchors; pilot motion/gear; chamber interactions; VFX transfer;
ten-character cohesion; scale/budget qualification. Split any unit before it
becomes too large to review or record reliably.

Read-only research and document maintenance are already authorized. Before
generation, record a numeric call/retry/time/disk ceiling suited to the experiment
and current authorization. Existing task authority permits bounded work; it does
not invent paid-account access, spending authority or extra external writes.
Ask only for actual missing access/budget/visual choices, after doing independent
preparation. Tool masks/seeds are capabilities to verify, never promises.

Retain source art and rejected evidence. Store outputs in experiment-specific
directories; never overwrite a qualified asset in place. Cache by input/tool/
profile hash. Prefer local repair when supported by the available tool and
authorization. Reuse generation results across sessions instead of starting over.

Use available image-generation tooling for generated/edited art. Programmatic
layout, mask derivation, runtime rigs and diagnostic geometry are separate from
painting. Python artwork editing has not been explicitly requested in this
planning turn; do not reinterpret permission to plan a deterministic pipeline as
permission to bypass the image-editing tool rule. Resolve concrete tool limits
at G2 without blocking research now.

## Improve the skill without turning guesses into rules

Keep three kinds of records separate:

- User decisions and proposed architecture: design docs and dated decisions.
- Unvalidated methods: hypothesis/experiment records, including falsifiers.
- Demonstrated reusable lessons: skill references, with evidence and scope.

After a failure: preserve the artifact, identify whether the cause is art,
preparation, runtime, measurement or missing evidence, run a discriminating
control, then amend the narrowest relevant instruction. A successful pilot is
scoped to its tested body/view/material; promote a broad production rule only
after transfer evidence. Record counterexamples and retire invalid advice with
lineage. Do not lower a frozen bar without a separately versioned, justified
test redesign; old verdicts remain old verdicts.

Camera/style/layout/rig revisions invalidate dependant builds and assessments.
The receipt's dependency hashes determine what needs retesting. Keep unmodified
accepted assets cached; do not blanket-regenerate the roster after a local fix.

## Closeout and handoff

Before ending, even after a failed experiment:

1. Finish the smallest reviewable artifact; stop or record outstanding jobs,
   partial outputs and safe resume commands. Do not start a long generation to
   fill remaining context.
2. Write an experiment receipt with commands, raw results, inspection scope,
   verdicts, costs, limitations and exact next action. Only evidence-backed gates
   may move to PASS.
3. Update PROGRESS.json: stage, active experiment, dependencies, decisions,
   blockers, artifact paths and next task. Append a dated decision/lesson only
   if something changed; avoid competing copies of current state.
4. Validate links/JSON/schema and relevant code/runtime tests. Review only owned
   paths; auto-commit authorized work with explicit paths under repo discipline.
   Verify the commit contents. Push only under applicable authorization.
5. Tell Matt what changed, what passed/failed, what remains uncertain, and provide
   the START_HERE link. A fresh session can use its restart prompt verbatim.

Stop at a clean milestone or before a large new dependency chain. Do not claim
an exact remaining context percentage unless the runtime exposes one. Compaction
is survivable because durable state is authoritative; a planned handoff is useful
because the next session can focus on one experiment.
