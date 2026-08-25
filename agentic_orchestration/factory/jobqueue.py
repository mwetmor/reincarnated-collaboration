"""The durable vendor-lane queue — hand-fired scripts are the bridge, this is the uptime.

`research/vfx-p2-dossiers/run_p2_serial.sh` proved the mechanics: 34/34 jobs `rc=0`,
strict serialization, idempotent re-entry, per-job usage JSONL. It is also bespoke to
one job class, and every new job class meant a hand-cloned script — a fresh chance to
get the serial law wrong. This module keeps the proven SEMANTICS and drops the
per-job-class cloning.

WHAT SURVIVED FROM THE PROVEN RUNNER, DELIBERATELY UNCHANGED
------------------------------------------------------------
  * **Strict serialization.** Enforced one layer down, at the `codex exec`
    invocation site in `harness/codex.py`, not here. See `drain`'s note on why this
    module must NOT hold the lock.
  * **Idempotent re-entry.** A re-fired queue does not redo completed jobs. The
    runner tested `dossier exists and > 500 bytes`; this generalises it to a declared
    `min_output_bytes` per job class AND adds the stronger test the runner could not
    have — a terminal row in `_run-log.tsv` for that job id.
  * **Per-job usage JSONL, stdout and stderr captured to separate files.**
  * **`_run-log.tsv` as the liveness surface**, `tail -1` answerable, columns 1-4
    unmoved.

WHAT IS NEW, AND WHY EACH IS NOT OPTIONAL
-----------------------------------------
  * **A curator, at ENQUEUE time** (U-4 R-B). Every vendor-lane output must have a
    named Claude curator downstream — that is the governance line, and it is not
    machine-checkable while the curator's identity lives only in the dispatcher's
    head. A job whose curator field is empty is a REFUSAL TO FIRE, not a job to be
    reconciled later. **Enqueue-time, not close-time, is the whole point:** a curator
    recorded at close is a curator chosen after seeing the output, which is not a
    governance control, it is a signature on work already done.
  * **Durable state.** Jobs are files. The queue drains them serially and survives
    process death, so re-entry after a crash is safe rather than hopeful.
  * **Telemetry from birth** (U-1(a)), append-only JSONL, `schema_version` +
    `passthrough` on every record, and NO consumer built here.
  * **A declared failure posture.** Junk or an unmodelled condition hands the job to
    the named Claude curator's lane and moves on. It does not retry indefinitely and
    it does not improvise.

WHAT THIS QUEUE IS NOT
----------------------
It is a LANE, not a source of truth about work state. Nothing here reads a dispatch
`**Status:**` header, derives work state from one, or emits a work-state claim of its
own — that field is measured-defective (Discipline #73) and a queue republishing it
would launder a corpus-wide stale claim into a data path. `tests/test_lane.py` proves
that mechanically, over this module's source, rather than leaving it to this
paragraph.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .lane import (
    LANE_STATE_SEAM_HELD,
    SANDBOX_MODES,
    SKIPPED_PER_AGENT,
    RunLog,
    Telemetry,
    utcnow,
)
from .roster import validate_seam

#: Bumped when the on-disk job record changes shape. Present on every record so a
#: reader never has to infer the vintage of a file it did not write.
JOB_SCHEMA_VERSION = "reincarnated.lane.job/0.1"

#: The declared failure posture, as a number. ONE attempt is the default: the U-4
#: fault fallback is *hand it to the named Claude agent, no re-litigating*, not
#: *try harder*. A job class may ask for more and is capped here, because "retries
#: with backoff" degenerates into a spin-retry the moment the ceiling is a variable.
DEFAULT_MAX_ATTEMPTS = 1
MAX_ATTEMPTS_CEILING = 3
RETRY_BACKOFF_BASE_S = 5.0

#: Fields a job record MUST carry to be accepted. `curator` is here because U-4 R-B
#: makes it schema rather than convention; deleting it from this set is what would
#: turn the governance line back into an assertion in someone's head. Its deletion is
#: caught by `test_lane.py::test_RB_a_job_with_no_curator_does_not_enqueue`, which is
#: named as the covering row in `tests/test_vocabularies.py`.
REQUIRED_JOB_FIELDS = frozenset({"job_id", "curator", "prompt"})

#: **AMENDMENT M — `seam` is a REQUIRED field, and it is required PER LANE.**
#:
#: M's own words leave the shape open: *"`seam` joins `REQUIRED_JOB_FIELDS` for
#: vendor-lane jobs (**or a lane-specific required set**)"*. Taken the second way, and
#: the reason is the same one that made `_validate_fence` a per-lane dispatch rather
#: than an `if lane == "codex"`: **the field is only load-bearing where a mechanism
#: enforces it.**
#:
#:   * **grok** — the per-seam flock is keyed on this name. An unnamed seam is a job
#:     that cannot be excluded against, so it is a REFUSAL TO FIRE, raised before any
#:     file or row exists (the P-8 curator-law shape, and Amendment L's shape one axis
#:     over: a claim whose release condition cannot be stated is not written).
#:   * **codex** — hard serial by VENDOR LAW, N=1, no per-agent grain and none coming.
#:     Requiring the field there would add a mandatory declaration that refuses jobs
#:     while enforcing nothing — a governance line with no mechanism behind it, which
#:     is exactly the "label, not a vocabulary" state R-B's own first version was in
#:     and which this package spent a Gate-2 finding getting out of. It is ACCEPTED
#:     there (roster-validated when given, recorded on the row) and never demanded.
#:
#: Deleting a lane's row does not fail open loudly — it silently stops demanding a
#: field — so this mapping is pinned by equality in `tests/test_vocabularies.py`.
REQUIRED_JOB_FIELDS_BY_LANE: dict[str, frozenset[str]] = {
    "codex": REQUIRED_JOB_FIELDS,
    "grok": REQUIRED_JOB_FIELDS | frozenset({"seam"}),
}

#: **AMENDMENT P.2 — why a queue wait happened, as a CLOSED vocabulary.**
#:
#: § 9.5's banked countable was *"`ENQUEUED`-to-`START` gaps — does anything actually
#: queue behind the lock?"*. Under AM-3 that same gap now measures TWO different things
#: — ceiling exhaustion at N=3, and a per-agent refusal — and P is explicit that the
#: two distinct causes must never share one number. So the number carries its reason.
#:
#: `both` exists because a job can wait for both across successive drains, and the
#: honest answer to *which one* is then *both*; collapsing it to the most recent would
#: publish a clean attribution the rows do not support. ADDITION is the fail-open
#: direction (a reason nobody adjudicated entering the banking window's own
#: attribution), so this is pinned by equality.
WAIT_REASONS: frozenset[str] = frozenset({"none", "ceiling", "per-agent", "both"})


@dataclass
class Job:
    """One unit of vendor-lane work. Durable, self-describing, curator-owned."""

    job_id: str
    curator: str
    #: **AMENDMENT M.** The agent seam whose process makes the INVOCATION — the grain of
    #: § 11's `seam` column, and NOT the holder session. Beside `curator`, never on top
    #: of it: the curator owns the OUTPUT (R-B/P-8) and the two legitimately differ (a
    #: star-lord-run job curated by galadriel). Empty on lanes with no per-agent grain.
    seam: str = ""
    job_class: str = "research"
    prompt_path: str = ""
    output_path: str | None = None
    #: PER-JOB-CLASS, NOT A HARDCODED CONSTANT. `read-only` is the posture of record
    #: for research jobs; a future class may need something else and it must be a
    #: VISIBLE decision in this record when it does.
    sandbox: str = "read-only"
    skip_git_repo_check: bool = True
    web_search: bool = False
    ephemeral: bool = True
    #: The proven runner's idempotency threshold, generalised. 0 disables the
    #: size test and leaves only the run-log's terminal row.
    min_output_bytes: int = 0
    max_attempts: int = DEFAULT_MAX_ATTEMPTS
    timeout_s: int = 3600
    enqueued_at: str = ""
    enqueued_by: str = ""
    schema_version: str = JOB_SCHEMA_VERSION
    extra: dict[str, Any] = field(default_factory=dict)

    def harness_config(self, *, raw_output_path: str, prompt_path: str) -> dict[str, Any]:
        return {
            "seam": self.seam,
            "sandbox": self.sandbox,
            "skip_git_repo_check": self.skip_git_repo_check,
            "web_search": self.web_search,
            "ephemeral": self.ephemeral,
            "output_path": self.output_path,
            "raw_output_path": raw_output_path,
            "prompt_path": prompt_path,
            "timeout_s": self.timeout_s,
            **{k: v for k, v in self.extra.items() if k not in ("prompt",)},
        }


@dataclass
class JobOutcome:
    job_id: str
    curator: str
    marker: str
    ok: bool
    attempts: int
    error: str | None = None
    exit_code: int | None = None
    usage: dict[str, Any] | None = None
    #: **AMENDMENT R.3.** Why the drain passed over this job, when it did. Carried as
    #: its own field rather than folded into `marker`, because the run-log marker is a
    #: CLOSED vocabulary answering the LIVENESS question (*is anything executing?*) and
    #: a per-agent skip's honest marker there is `ENQUEUED` — the job is pending again,
    #: exactly as it was. What is new is not the job's state but the REASON the drain
    #: reordered, and a queue that silently reorders is folklore while one that says why
    #: is evidence. `None` means the drain did not skip this job.
    skipped_reason: str | None = None


@dataclass
class DrainReport:
    lane_state: str
    outcomes: list[JobOutcome] = field(default_factory=list)
    stopped_reason: str | None = None

    @property
    def fired(self) -> int:
        return sum(1 for o in self.outcomes if o.marker.startswith("rc="))

    @property
    def skipped(self) -> int:
        return sum(1 for o in self.outcomes if o.marker == "SKIP-EXISTS")

    @property
    def handed_to_claude(self) -> int:
        return sum(1 for o in self.outcomes if o.marker == "FALLBACK-CLAUDE")

    @property
    def deferred(self) -> int:
        """Jobs returned to the queue because the lane was busy. NOT failures.

        Kept distinct from `handed_to_claude` because conflating them is the bug this
        property was added to fix: a busy lane is transient and self-clearing, and
        spending Claude-lane tokens on it converts "wait ten seconds" into "do the work
        somewhere else."
        """
        return sum(1 for o in self.outcomes if o.marker == "ENQUEUED")

    @property
    def skipped_per_agent(self) -> int:
        """**AMENDMENT R.3** — per-agent skips, counted. NOT failures, NOT attempts.

        Distinct from `deferred` (the lane's ceiling was full, so the drain stopped) and
        from `handed_to_claude` (ownership moved, once, permanently). This one means:
        *this agent already had a job in flight, so the drain took the next one and will
        come back for this.* The banking window's job-10 verdict wants this number —
        P.2 names ENQUEUED-to-START gaps as evidence about whether N=3 is right, and
        under AM-3 a gap has two possible causes that must not share one column.
        """
        return sum(1 for o in self.outcomes if o.skipped_reason == SKIPPED_PER_AGENT)


#: **THE PER-LANE FENCE, dispatched by vendor.** The two lanes do not have the same
#: pre-hoc containment and the difference is not cosmetic:
#:
#:   * **codex** — the fence IS the sandbox mode (`-s read-only`), because `codex exec`
#:     exposes no tool allowlist at all. Validated against the closed `SANDBOX_MODES`.
#:   * **grok** — there is no sandbox triad on that CLI's headless surface that has
#:     been enumerated on this host; the declared fence is `permission_mode` plus
#:     `--disable-web-search`. A Grok job carrying a `sandbox:` value would be naming a
#:     fence its lane does not hold, so the field is REFUSED there rather than accepted
#:     and ignored — accepting it is the fail-open direction, where the job record
#:     reads as fenced and the invocation is not.
#:
#: Written as a dispatch rather than as an `if lane == "codex"` inside `enqueue`
#: because the next lane is a table row, not another branch in a governance check.
def _validate_fence(lane: str, sandbox: str, extra: dict[str, Any]) -> str:
    """Refuse a job whose declared fence its lane cannot hold. Returns the fence, for the row."""
    if lane == "codex":
        if sandbox not in SANDBOX_MODES:
            raise ValueError(
                f"lane job refused: sandbox {sandbox!r} is not one of "
                f"{sorted(SANDBOX_MODES)}. The sandbox is this lane's pre-hoc "
                "containment and is declared per job class, never guessed."
            )
        return f"sandbox={sandbox}"
    if lane == "grok":
        from .harness.grok import (
            DEFAULT_PERMISSION_MODE,
            FORBIDDEN_PERMISSION_MODES,
            PERMISSION_MODES,
        )

        if sandbox and sandbox != _NO_FENCE_FIELD:
            raise ValueError(
                f"lane job refused: the grok lane holds no sandbox fence, so "
                f"sandbox={sandbox!r} would name a containment this lane cannot enforce "
                "— and a job record that reads as fenced while the invocation is not is "
                f"the fail-open direction. Pass sandbox={_NO_FENCE_FIELD!r} and declare "
                f"`permission_mode` (one of {sorted(PERMISSION_MODES)}) instead."
            )
        mode = str(extra.get("permission_mode") or DEFAULT_PERMISSION_MODE)
        if mode in FORBIDDEN_PERMISSION_MODES:
            raise ValueError(
                f"lane job refused: permission mode {mode!r} is REFUSED BY NAME. "
                "`bypassPermissions` removes the fence and `dontAsk` auto-answers it."
            )
        if mode not in PERMISSION_MODES:
            raise ValueError(
                f"lane job refused: permission mode {mode!r} is not one of "
                f"{sorted(PERMISSION_MODES)}."
            )
        extra["permission_mode"] = mode
        web = "on" if extra.get("web_search") else "off"
        return f"permission_mode={mode} web_search={web}"
    raise ValueError(
        f"lane job refused: no fence is declared for lane {lane!r}. A lane with no "
        "declared pre-hoc containment does not take jobs — that is the whole of U-4's "
        "fence discipline, and defaulting one here would invent a posture nobody ruled."
    )


#: The value a job on a lane WITHOUT a sandbox fence carries in the `sandbox` field.
#: Spelled rather than left empty so that a reader of the job record sees a positive
#: statement — *this lane holds no sandbox fence* — instead of a blank they must
#: interpret.
_NO_FENCE_FIELD = "n/a"


#: **D-3 — the Q3-NO router token.** A convention, not a schema change: the enqueue
#: row's free-form `detail` column carries `router=<verdict>`, so lane contention
#: becomes countable for the first time::
#:
#:     grep -c "router=Q3-NO" _run-log.tsv
#:
#: `Q3-NO` means the four-question router cleared the job but answered NO to question
#: (3) *"lane open?"* — i.e. the job was enqueued BECAUSE the lane was occupied, which
#: is the default routing under § 10.3 step 4 and not a failure. R-D compliance without
#: touching the column count.
ROUTER_Q3_NO = "Q3-NO"


def _slot_line(harness: Any) -> str:
    """`"k/N"` for a counted lane, `""` for one without slots. DUCK-TYPED ON PURPOSE.

    Reached by `getattr` rather than by `if self.lane == "grok"`, for the reason
    `_validate_fence` is a dispatch table: the Codex lane has no slots and must not grow
    any (P-1 is a vendor law, N=1, and § 9.5 probed xAI — evidence does not travel
    across vendors), and the next counted lane should be a harness that answers this
    method, not another branch in a queue that knows vendors by name.

    Any failure reads as ABSENT, never as zero: a `slots_held=0/3` written because the
    probe raised would publish a solo row for a job whose concurrency nobody measured,
    and the banking window would attribute the difference to load.
    """
    probe = getattr(harness, "slot_occupancy", None)
    if probe is None:
        return ""
    try:
        slots = probe()
    except Exception:  # noqa: BLE001 — an unmeasurable lane is not a measured-empty one
        return ""
    return f"{slots.held}/{slots.total}"


def _atomic_write(path: Path, text: str) -> None:
    """Write-then-rename. A crash leaves the old file or the new one, never half of one."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + f".tmp.{os.getpid()}")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


class JobQueue:
    """A standing durable queue over one vendor lane.

    Layout under `root`::

        _run-log.tsv          the liveness surface (tail -1 answerable)
        telemetry.jsonl       append-only lifecycle events (U-1(a))
        jobs/<id>.job.json    the durable job record, written atomically at enqueue
        prompts/<id>.md       the exact prompt text that was sent
        usage/<id>.jsonl      the raw `codex exec --json` stream
        usage/<id>.jsonl.stderr
        fallback/<id>.json    a manifest for the named Claude curator to pick up
        AUTH-BLOCKED.md       a ready-to-file matt_to_do row, when auth is not healthy
    """

    def __init__(self, root: Path, lane: str = "codex"):
        self.root = Path(root)
        self.lane = lane
        self.runlog = RunLog(self.root / "_run-log.tsv")
        self.telemetry = Telemetry(self.root / "telemetry.jsonl")

    # -- paths ---------------------------------------------------------------
    def job_path(self, job_id: str) -> Path:
        return self.root / "jobs" / f"{job_id}.job.json"

    def prompt_path(self, job_id: str) -> Path:
        return self.root / "prompts" / f"{job_id}.md"

    def raw_path(self, job_id: str) -> Path:
        return self.root / "usage" / f"{job_id}.jsonl"

    def fallback_path(self, job_id: str) -> Path:
        return self.root / "fallback" / f"{job_id}.json"

    def curator_at_enqueue(self, job_id: str) -> str | None:
        """U-4 R-B's empirical criterion, answerable by query rather than by memory."""
        return self.runlog.curator_at_enqueue(job_id)

    # -- enqueue -------------------------------------------------------------
    def enqueue(
        self,
        *,
        job_id: str,
        prompt: str,
        curator: str,
        seam: str = "",
        job_class: str = "research",
        output_path: str | Path | None = None,
        sandbox: str = "read-only",
        web_search: bool = False,
        skip_git_repo_check: bool = True,
        ephemeral: bool = True,
        min_output_bytes: int = 0,
        max_attempts: int = DEFAULT_MAX_ATTEMPTS,
        timeout_s: int = 3600,
        enqueued_by: str = "",
        router: str = "",
        extra: dict[str, Any] | None = None,
    ) -> Job:
        """Accept a job, or REFUSE IT. Nothing is written when the refusal fires.

        **U-4 R-B, and it is the first thing checked:** a job that cannot name its
        curator does not enqueue. Not "enqueues and is reconciled later" — the whole
        force of the amendment is that the naming happens BEFORE the output exists,
        so it is a commitment rather than an endorsement. The refusal is raised
        before any file is created and before any row is appended, so a refused job
        leaves no trace to clean up and no half-state to interpret.
        """
        # The refusal is DERIVED from `REQUIRED_JOB_FIELDS`, not restated beside it.
        # Restating it was the first version, and it made the constant a LABEL: it
        # named the requirement in an error message while three hardcoded conditions
        # actually enforced it, so deleting `"curator"` from the set would have changed
        # what the message SAID and nothing about what the code DID.
        #
        # `str(value or "")`, NOT `str(value)`. Written the second way first, and
        # `test_RB_a_job_with_no_curator_does_not_enqueue` caught it: `str(None)` is
        # the four-character string `"None"`, which is truthy, so a `curator=None`
        # sailed straight through the refusal and enqueued a job whose curator column
        # would have read `curator=None` — a governance leak that a query counting
        # non-empty curator fields would have counted as compliant. The refusal that
        # can be passed by not passing anything is the exact shape R-B exists to close.
        supplied = {"job_id": job_id, "prompt": prompt, "curator": curator, "seam": seam}
        # PER-LANE required set (Amendment M). `.get(lane, REQUIRED_JOB_FIELDS)` would
        # be the fail-open spelling for a lane nobody declared — but a lane nobody
        # declared is already refused by `_validate_fence` below, loudly and by name,
        # so the base set here is the honest default rather than a silent forgiveness.
        required = REQUIRED_JOB_FIELDS_BY_LANE.get(self.lane, REQUIRED_JOB_FIELDS)
        missing = sorted(
            f for f in required if not str(supplied.get(f) or "").strip()
        )
        # `curator` is separated out and refused FIRST, with its own message, because
        # a governance refusal that reads like a validation error gets fixed like one.
        if "curator" in missing:
            raise ValueError(
                "U-4 R-B: REFUSAL TO FIRE — this job names no curator.\n"
                "Every vendor-lane output must have a named Claude curator downstream; "
                "that is the governance line and it has no exceptions. The curator is "
                "written at ENQUEUE time, not at close: a curator chosen after seeing "
                "the output is an endorsement, not a control. Naming one is free and "
                "there is no schedule-critical scenario in which it is the expensive "
                "step (U-4 R-A), so this refusal has no override.\n"
                f"Pass `curator=\"<agent>\"` for job {job_id!r}."
            )
        if "seam" in missing:
            # AMENDMENT M, refused FIRST among the remainder and with its own message,
            # for the reason the curator refusal is separated: an exclusivity refusal
            # that reads like a validation error gets fixed like one — by typing
            # something into the field — and the one thing that must not happen here is
            # a plausible name being invented to satisfy a validator.
            raise ValueError(
                f"AMENDMENT M: REFUSAL TO FIRE — job {job_id!r} on the {self.lane!r} "
                "lane names no seam.\n"
                "This lane's per-agent exclusivity is a flock keyed on the seam name, "
                "so a job with no seam is not a job with a missing label — it is a job "
                "nothing can exclude against. The seam is the agent whose PROCESS makes "
                "the invocation; the curator is the named Claude owner of the OUTPUT. "
                "They legitimately differ, and defaulting one to the other breaks "
                "exclusivity in BOTH directions: two agents running one curator's jobs "
                "would collide on one slot, and one agent running three curators' jobs "
                "would take three.\n"
                f"Pass `seam=\"<agent>\"` (see `factory.roster.AGENT_ROSTER`)."
            )
        if missing:
            raise ValueError(
                f"lane job refused: empty {', '.join(missing)}. Required fields on the "
                f"{self.lane!r} lane are {sorted(required)}."
            )
        # ROSTER-VALIDATED WHEREVER GIVEN (M.3), including on a lane that does not
        # demand it: a recorded seam that is a typo is worse than an absent one,
        # because it reads as an answer. Vocabulary borrowed from § 11 custody;
        # MECHANISM DECOUPLED (M.4) — nothing here reads `_custody.tsv`, so a missing or
        # stale CLAIM row can never block a legal vendor fire.
        seam_name = validate_seam(seam, where=f"lane job {job_id!r}") if str(seam or "").strip() else ""
        job_extra = dict(extra or {})
        if web_search:
            job_extra.setdefault("web_search", True)
        fence = _validate_fence(self.lane, sandbox, job_extra)
        attempts = max(1, min(int(max_attempts), MAX_ATTEMPTS_CEILING))

        job = Job(
            job_id=str(job_id).strip(),
            curator=str(curator).strip(),
            seam=seam_name,
            job_class=job_class,
            prompt_path=str(self.prompt_path(job_id)),
            output_path=str(output_path) if output_path else None,
            sandbox=sandbox,
            skip_git_repo_check=skip_git_repo_check,
            web_search=web_search,
            ephemeral=ephemeral,
            min_output_bytes=int(min_output_bytes),
            max_attempts=attempts,
            timeout_s=int(timeout_s),
            enqueued_at=utcnow(),
            enqueued_by=enqueued_by,
            extra=job_extra,
        )

        existing = self.load(job.job_id)
        if existing is not None:
            same = {k: v for k, v in asdict(existing).items() if k != "enqueued_at"}
            fresh = {k: v for k, v in asdict(job).items() if k != "enqueued_at"}
            if same == fresh and self.prompt_path(job.job_id).exists() \
                    and self.prompt_path(job.job_id).read_text(encoding="utf-8") == prompt:
                # Idempotent re-enqueue: a re-fired enqueue script must not produce a
                # second ENQUEUED row, or the liveness surface grows a duplicate for
                # every re-run and the terminal-row check starts lying.
                return existing
            raise ValueError(
                f"lane job refused: {job.job_id!r} is already enqueued with DIFFERENT "
                "terms. Re-enqueuing under the same id would leave two job records "
                "disagreeing about what was asked for, and the run log could not say "
                "which one the output belongs to. Use a new id, or delete the record "
                "deliberately."
            )

        _atomic_write(self.prompt_path(job.job_id), prompt)
        _atomic_write(self.job_path(job.job_id), json.dumps(asdict(job), indent=2) + "\n")
        detail = f"job_class={job.job_class} {fence}"
        if job.seam:
            # On the ENQUEUE row, beside the fence, for the same reason the curator is:
            # the surface the banking window and the job-10 verdict read is the RUN-LOG,
            # and a per-agent skip counted later is only attributable if the row that
            # opened the job says which agent it belongs to.
            detail += f" seam={job.seam}"
        if router:
            # D-3. The token rides the free-form column; no schema change, and
            # `grep -c "router=Q3-NO"` counts lane contention from the surface that
            # already exists.
            detail += f" router={router}"
        self.runlog.append(
            job_id=job.job_id,
            marker="ENQUEUED",
            detail=detail,
            curator=job.curator,
            event="enqueue",
        )
        self.telemetry.emit(
            "enqueue",
            lane=self.lane,
            job_id=job.job_id,
            curator=job.curator,
            seam=job.seam or None,
            job_class=job.job_class,
            fence=fence,
            router=router or None,
            enqueued_by=job.enqueued_by or None,
            job_schema_version=job.schema_version,
            passthrough={"output_path": job.output_path, "max_attempts": job.max_attempts},
        )
        return job

    # -- inspection ----------------------------------------------------------
    def load(self, job_id: str) -> Job | None:
        path = self.job_path(job_id)
        if not path.exists():
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
        known = {f for f in Job.__dataclass_fields__}
        return Job(**{k: v for k, v in data.items() if k in known})

    def all_jobs(self) -> list[Job]:
        directory = self.root / "jobs"
        if not directory.exists():
            return []
        jobs = []
        for path in sorted(directory.glob("*.job.json")):
            job = self.load(path.name[: -len(".job.json")])
            if job is not None:
                jobs.append(job)
        return jobs

    def is_done(self, job: Job) -> str | None:
        """Idempotency, in two independent directions. Returns the REASON or None.

        A job is done if the run log carries a terminal row for it OR if its declared
        output already exists at the declared size. Both, rather than either alone:

          * The run-log test is the stronger one and the proven runner could not have
            it (its log had no per-job terminal semantics). It survives a job class
            with no output file at all.
          * The output-size test is the proven runner's, kept because it survives a
            LOST run log — and because it is the one that makes a Claude-lane
            fallback safe: if the curator's agent does the work by hand and writes the
            output, a later drain after re-auth will SKIP rather than duplicate it.
        """
        if job.job_id in self.runlog.terminal_job_ids():
            return "terminal row in _run-log.tsv"
        if job.output_path and job.min_output_bytes > 0:
            out = Path(job.output_path)
            if out.exists() and out.stat().st_size >= job.min_output_bytes:
                return f"output exists at {out.stat().st_size} bytes"
        return None

    def pending(self) -> list[Job]:
        return [job for job in self.all_jobs() if self.is_done(job) is None]

    # -- drain ---------------------------------------------------------------
    def drain(
        self,
        harness: Any,
        limit: int | None = None,
        sleep: Callable[[float], None] = time.sleep,
    ) -> DrainReport:
        """Run pending jobs SERIALLY until they are gone.

        **THIS METHOD DOES NOT HOLD THE LANE LOCK, ON PURPOSE.** The lock is taken
        inside `harness.run()`, around the `codex exec` call and nothing else, because
        that is the invocation site the serial law is about. Holding it here as well
        would be worse than redundant: `flock` conflicts across two `open()` calls in
        the SAME process (measured, errno 35), so a drain loop holding the lock would
        make every job's own acquisition fail. The apparent belt-and-braces would be a
        deadlock, and finding that out in production is exactly the class of mistake
        this build exists to prevent.

        Two drainers running at once is therefore SAFE and not an error: they
        interleave whole jobs, and one `codex exec` runs at a time. Interleaving whole
        jobs is serial. Overlapping them is not, and cannot happen.
        """
        state = harness.availability()
        if not state.ok and state.state != "busy":
            return self._stop_on_closed_lane(state)

        report = DrainReport(lane_state="open")
        count = 0
        for job in self.all_jobs():
            if limit is not None and count >= limit:
                break
            reason = self.is_done(job)
            if reason is not None:
                if job.job_id not in self.runlog.terminal_job_ids():
                    self.runlog.append(
                        job_id=job.job_id, marker="SKIP-EXISTS", detail=reason,
                        curator=job.curator, event="finish",
                    )
                    self.telemetry.emit(
                        "finish", lane=self.lane, job_id=job.job_id,
                        curator=job.curator, outcome="skip_exists",
                        passthrough={"reason": reason},
                    )
                    report.outcomes.append(JobOutcome(
                        job.job_id, job.curator, "SKIP-EXISTS", True, 0,
                    ))
                continue
            # A BUSY lane is not a failure and must never reach the fallback path.
            # Written the other way first: `drain` proceeded on `busy`, `harness.run`
            # refused with `LaneBusy`, and `_run_one` counted that refusal as an
            # attempt and handed the job to the named Claude curator — permanently,
            # for a condition that clears by itself when the other drainer finishes.
            # The serial law's own words are "queue behind it or fire the Claude lane",
            # and a DRAINER's answer to a busy lane is unambiguously the first: the
            # other drainer is already doing this work.
            pre = harness.availability()
            if not pre.ok and pre.state == "busy":
                report.lane_state = "busy"
                report.stopped_reason = pre.reason
                break
            outcome = self._run_one(job, harness, sleep)
            report.outcomes.append(outcome)
            if outcome.skipped_reason == SKIPPED_PER_AGENT:
                # **AMENDMENT R.2 — SKIP AND CONTINUE.** The `continue` is the whole
                # ruling, and the two things it is NOT are what make it necessary:
                #
                #   * NOT a `break`. A per-agent refusal is JOB-specific, not
                #     lane-specific. Breaking here head-of-line-blocks the entire drain
                #     on one agent's in-flight job — the lane sitting at 1/3 with a full
                #     queue and two free slots, inverting the amendment's own purpose.
                #   * NOT a fault. `_run_one` returned before the fallback path and did
                #     not count an attempt, so this job is still pending and still
                #     owned by this lane. Counting it as an attempt would hand it
                #     PERMANENTLY to FALLBACK-CLAUDE (P-7: ownership moves once) for a
                #     condition that clears when the agent's other job finishes — the
                #     exact defect the comment above records being made once already,
                #     arriving through a new door.
                #
                # `count` is deliberately NOT incremented: `limit` bounds jobs RUN, and
                # spending the budget on a job that never launched would make a
                # `--limit 1` drain do nothing at all whenever the head job's seam is
                # busy.
                continue
            count += 1
            # Re-check auth between jobs: a token can expire mid-drain, and the next
            # job would otherwise fail as if the MODEL had failed, which routes a
            # Matt-only condition into the fallback path where it does not belong.
            state = harness.availability()
            if not state.ok and state.state != "busy":
                stop = self._stop_on_closed_lane(state)
                report.stopped_reason = stop.stopped_reason
                report.lane_state = stop.lane_state
                break
        return report

    def _run_one(self, job: Job, harness: Any, sleep: Callable[[float], None]) -> JobOutcome:
        raw = self.raw_path(job.job_id)
        if job.output_path:
            # The job DECLARED where its artifact goes; making that directory exist is
            # the queue's job, not the vendor CLI's. `codex exec -o` into a missing
            # directory fails on an errno that reads like a model failure and would be
            # routed to the Claude fallback as if the LANE had misbehaved.
            Path(job.output_path).parent.mkdir(parents=True, exist_ok=True)
        config = job.harness_config(raw_output_path=str(raw), prompt_path=job.prompt_path)
        prompt = self.prompt_path(job.job_id).read_text(encoding="utf-8")

        last_error: str | None = None
        last_exit: int | None = None
        usage: dict[str, Any] | None = None
        for attempt in range(1, job.max_attempts + 1):
            start_detail = f"attempt={attempt}/{job.max_attempts} pid={os.getpid()}"
            if job.seam:
                start_detail += f" seam={job.seam}"
            # AMENDMENT P.1 — `slots_held=` AT START. Probed here, before the claim, so
            # it is the AMBIENT concurrency this job started into. Its inclusivity is
            # pinned in MIGRATION § 11.4 and it differs from the finish sample's on
            # purpose: at START this job holds nothing, at finish it holds one, and both
            # rows state the literal truth about the lane at the instant they were
            # written. `slots_at_claim` (inclusive, measured at acquisition) rides the
            # telemetry stream, where there is no column pressure.
            ambient = _slot_line(harness)
            if ambient:
                start_detail += f" slots_held={ambient}"
            # AMENDMENT P.2 — the ENQUEUED->START gap, WITH ITS REASON. § 9.5's banked
            # countable measured one thing under the serial law and measures two under
            # AM-3, and the two causes must never share one number.
            waited_ms, waited_reason = self._waited(job)
            if waited_ms is not None:
                start_detail += f" waited_ms={waited_ms} waited_reason={waited_reason}"
            self.runlog.append(
                job_id=job.job_id, marker="START",
                detail=start_detail,
                curator=job.curator, event="start",
            )
            # No `model` on the START event. The queue does not know which model the
            # harness will pin, and inventing the answer here would put a guess in the
            # telemetry beside the FINISH event's measured one. Absent is absent.
            self.telemetry.emit(
                "start", lane=self.lane, job_id=job.job_id, curator=job.curator,
                seam=job.seam or None, attempt=attempt,
                slots_held_at_start=ambient, waited_ms=waited_ms,
                waited_reason=waited_reason if waited_ms is not None else None,
                passthrough={"pid": os.getpid(), "sandbox": job.sandbox},
            )
            started = time.time()
            result = harness.run(prompt, self.root, config)
            elapsed = time.time() - started

            if (result.extra or {}).get("lane_state") == LANE_STATE_SEAM_HELD:
                # **AMENDMENT R.1 — ITS OWN OUTCOME.** Not `LaneBusy` (the lane may have
                # two free slots and other seams may be firing into them right now) and
                # not a fault (it is never an attempt, and it must never reach
                # `_hand_to_claude`). The job goes back to pending exactly as it was:
                # `ENQUEUED` is non-terminal, `is_done` says no, and the next drain —
                # or this same drain, once the agent's other job finishes — picks it up.
                #
                # The START row above is ANSWERED rather than left dangling, which is
                # what keeps leg 3 honest: a job that began and never ended reads
                # `busy-out-of-band` to every session on this host.
                self.runlog.append(
                    job_id=job.job_id, marker="ENQUEUED",
                    detail=(
                        f"skipped={SKIPPED_PER_AGENT} seam={job.seam} "
                        f"attempts_counted=0"
                    ),
                    curator=job.curator, event="defer",
                )
                self.telemetry.emit(
                    "skipped", lane=self.lane, job_id=job.job_id, curator=job.curator,
                    seam=job.seam or None, outcome=SKIPPED_PER_AGENT, error=result.error,
                    passthrough={
                        "transient": True,
                        "handed_to_claude": False,
                        # Named in the record, not only in the code: R.1's two
                        # prohibitions are the whole reason this outcome exists.
                        "counted_as_attempt": False,
                        "lane_state": "not-busy — this is a JOB refusal, not a lane one",
                    },
                )
                return JobOutcome(
                    job.job_id, job.curator, "ENQUEUED", False, 0, result.error,
                    skipped_reason=SKIPPED_PER_AGENT,
                )

            if (result.extra or {}).get("lane_state") == "busy":
                # The race window `drain`'s pre-check cannot close: free when asked,
                # taken by the time we launched. The job goes BACK to pending — the
                # `ENQUEUED` marker is non-terminal, so `is_done` says no and the next
                # drain picks it up — and the START row above is answered rather than
                # left dangling as a job that began and never ended.
                self.runlog.append(
                    job_id=job.job_id, marker="ENQUEUED",
                    detail=f"deferred=lane-busy attempt={attempt}",
                    curator=job.curator, event="defer",
                )
                self.telemetry.emit(
                    "deferred", lane=self.lane, job_id=job.job_id, curator=job.curator,
                    attempt=attempt, outcome="lane_busy", error=result.error,
                    passthrough={"transient": True, "handed_to_claude": False},
                )
                return JobOutcome(
                    job.job_id, job.curator, "ENQUEUED", False, attempt, result.error,
                )
            usage = result.usage.to_dict() if result.usage else None
            last_exit = result.exit_code
            last_error = result.error

            ok = result.ok
            if ok and job.output_path and job.min_output_bytes > 0:
                out = Path(job.output_path)
                size = out.stat().st_size if out.exists() else 0
                if size < job.min_output_bytes:
                    ok = False
                    last_error = (
                        f"output {job.output_path!r} is {size} bytes, below the job "
                        f"class's declared floor of {job.min_output_bytes}. Judged JUNK "
                        "by the job class's own criterion, not by this module's opinion."
                    )

            self.telemetry.emit(
                "finish" if ok else "attempt_failed",
                lane=self.lane, job_id=job.job_id, curator=job.curator,
                attempt=attempt, exit_code=result.exit_code,
                model=result.model, reasoning_effort=(result.extra or {}).get("reasoning_effort"),
                harness_session_id=result.harness_session_id,
                usage=usage, outcome="ok" if ok else "failed",
                error=None if ok else last_error,
                elapsed_s=round(elapsed, 3),
                passthrough={"harness_extra": result.extra or {}},
            )
            if ok:
                detail = (
                    f"attempt={attempt} elapsed_s={elapsed:.1f} "
                    f"tokens={result.usage.billable_token_total() if result.usage else 'NULL'}"
                )
                # AMENDMENT C, on the row a human reads: the RESOLVED model id, not the
                # declared pin. A pin whose resolved target is chosen by a vendor-side
                # rule is a request; recording only the request would let a resolution
                # change under an unchanged pin pass silently, and every banked lane
                # statistic is a statistic ABOUT the resolved config.
                resolved = (result.extra or {}).get("resolved_model")
                if resolved:
                    detail += f" resolved_model={resolved}"
                # AMENDMENT D, on the row — GATE-2 FINDING G2-1, fixed here. The effort
                # pin was argv-said and telemetry-recorded but ABSENT from the run-log
                # row, while `MIGRATION.md` § 5 asserted *"every row carries curator +
                # resolved model id + declared effort + per-call cost_usd"*. A document
                # asserting a property the artifact does not carry is #73 arriving in
                # the doc that pins #73's own build constraint.
                #
                # Struck the claim, or carry the field? Carry it. The surface Amendment I
                # names for the banking window is the RUN-LOG, and effort is one of the
                # three things the window must attribute against — a cost column read
                # beside a resolved model but not beside its effort level attributes an
                # effort change to the model (#10). Read from `extra` rather than from
                # the module pin, so a job that overrides the pin records what it ASKED
                # FOR and not what the constant says; the vendor-refused case never
                # reaches this branch, because an unknown effort is refused at build_argv.
                effort = (result.extra or {}).get("reasoning_effort")
                if effort:
                    detail += f" effort={effort}"
                # AMENDMENT P.1 — `slot_index=` and `slots_held=` AT FINISH, read by the
                # harness while this job still held its slot (so the sample is inclusive
                # on the same terms as `slots_at_claim`). The pair start/finish is
                # CONTEXT; the verdict conditions on the DERIVED OVERLAP INTERVAL — a
                # join over this log's own START/finish timestamps — because a job that
                # starts alone and spends 90% of its life alongside two others would
                # otherwise be read as a solo row. That derivation is pinned by name in
                # `MIGRATION.md` § 11.4 so job 10 is not reconstructed from memory.
                slot_index = (result.extra or {}).get("slot_index")
                if slot_index is not None:
                    detail += f" slot_index={slot_index}"
                finish_slots = (result.extra or {}).get("slots_at_finish")
                if finish_slots:
                    detail += (
                        f" slots_held={finish_slots['held']}/{finish_slots['total']}"
                    )
                # AMENDMENT I's per-row cost. Only where the vendor reports one —
                # absent is absent, and a zero here would read as a free call.
                if result.usage is not None and result.usage.dollars is not None:
                    detail += f" cost_usd={result.usage.dollars:.5f}"
                self.runlog.append(
                    job_id=job.job_id, marker=f"rc={result.exit_code if result.exit_code is not None else 0}",
                    detail=detail,
                    curator=job.curator, event="finish",
                )
                return JobOutcome(
                    job.job_id, job.curator, f"rc={result.exit_code or 0}", True,
                    attempt, None, result.exit_code, usage,
                )
            if attempt < job.max_attempts:
                # Bounded exponential backoff, never a spin. The ceiling is
                # MAX_ATTEMPTS_CEILING and it is not a variable.
                sleep(RETRY_BACKOFF_BASE_S * (2 ** (attempt - 1)))

        return self._hand_to_claude(job, last_error or "unmodelled condition", last_exit, usage)

    # -- Amendment P's two derivations ---------------------------------------
    def _waited(self, job: Job) -> tuple[int | None, str]:
        """`(ENQUEUED->START milliseconds, reason)` — P.2, derived, never asserted.

        The REASON is read off this job's own prior rows rather than carried in memory,
        because a drain is a process: the drain that skipped this job for a per-agent
        refusal is usually not the drain that eventually runs it, and a number whose
        cause lives in a dead process's variables is a number nobody can attribute. The
        run-log already records both causes as tokens in the detail column
        (`skipped=per-agent-slot-held`, `deferred=lane-busy`, `router=Q3-NO`), so the
        attribution is a query over the surface that exists.

        `both` rather than most-recent-wins: a job that queued behind the ceiling AND
        was skipped for its seam waited for two reasons, and picking one would publish a
        clean attribution the rows do not support. `none` means the gap is the drain's
        own cadence — nobody was in the way — which is the answer § 9.5's countable was
        originally asking for.
        """
        if not job.enqueued_at:
            return None, "none"
        try:
            enqueued = datetime.strptime(job.enqueued_at, "%Y-%m-%dT%H:%M:%SZ").replace(
                tzinfo=timezone.utc)
        except ValueError:
            return None, "none"
        waited_ms = max(0, int(
            (datetime.now(timezone.utc) - enqueued).total_seconds() * 1000))
        ceiling = per_agent = False
        for row in self.runlog.rows():
            if len(row) < 4 or row[1] != job.job_id:
                continue
            detail = row[3]
            if f"skipped={SKIPPED_PER_AGENT}" in detail:
                per_agent = True
            if "deferred=lane-busy" in detail or f"router={ROUTER_Q3_NO}" in detail:
                ceiling = True
        reason = {
            (False, False): "none",
            (True, False): "ceiling",
            (False, True): "per-agent",
            (True, True): "both",
        }[(ceiling, per_agent)]
        return waited_ms, reason

    def _hand_to_claude(
        self, job: Job, error: str, exit_code: int | None, usage: dict[str, Any] | None
    ) -> JobOutcome:
        """The declared failure posture: the named curator's agent takes the lane.

        No re-litigating, no indefinite retry, no improvisation. The manifest names
        the curator who already owns this job's output, because the whole point of
        capturing the curator at enqueue is that there is somebody to hand it to when
        the lane cannot finish it.
        """
        manifest = {
            "schema_version": JOB_SCHEMA_VERSION,
            "handed_off_at": utcnow(),
            "lane": self.lane,
            "job": asdict(job),
            "reason": error,
            "exit_code": exit_code,
            "posture": (
                "U-4 fault fallback: junk output or an unmodelled condition means the "
                "NAMED CLAUDE AGENT takes this job, with no re-litigating. This file is "
                "the handoff, not a retry queue."
            ),
        }
        _atomic_write(self.fallback_path(job.job_id), json.dumps(manifest, indent=2) + "\n")
        self.runlog.append(
            job_id=job.job_id, marker="FALLBACK-CLAUDE",
            detail=f"reason={error[:160]}",
            curator=job.curator, event="finish",
        )
        self.telemetry.emit(
            "finish", lane=self.lane, job_id=job.job_id, curator=job.curator,
            outcome="fallback_claude", exit_code=exit_code, usage=usage,
            fallback="claude", error=error,
            passthrough={"manifest": str(self.fallback_path(job.job_id))},
        )
        return JobOutcome(
            job.job_id, job.curator, "FALLBACK-CLAUDE", False, job.max_attempts,
            error, exit_code, usage,
        )

    # -- the auth-expired path ------------------------------------------------
    def _stop_on_closed_lane(self, state: Any) -> DrainReport:
        """Auth health is a FIRST-CLASS QUEUE STATE, not an exception.

        Expired auth is not a job failure to retry: re-authentication is a MATT-ONLY
        action, and a queue that retried around it would burn the lane's whole backlog
        against a wall.

        **THE CHOICE I MADE, NAMED (the dispatch left it to me):** this queue does NOT
        write into `canonical/matt_to_do/`. It writes a fully-formed, ready-to-file row
        to `<root>/AUTH-BLOCKED.md` and surfaces the condition on both the run log and
        the telemetry stream; knight-rider files it. Two reasons, and the second is the
        one that decided it:

          1. `matt_to_do/` is a curated human queue in the meta-repo. An automated
             process appending to it produces rows with no author in the accountability
             graph — the dispatch's own words, *do not have it write there silently and
             unattributably*.
          2. THE LAW. A queue that writes into a governance surface has put itself in
             that surface's data path. The lane is the data path for LANE state; it is
             a reporter everywhere else. Emitting the condition keeps it a reporter.

        Pending work is NOT abandoned and is NOT left ambiguous: every pending job is
        handed to its named curator's Claude lane via a `fallback/` manifest and a
        terminal `FALLBACK-CLAUDE` row. Terminal is deliberate — once a job is handed
        over, a drain after re-auth must NOT pick it up again, or the same artifact
        gets produced twice and two agents both believe they own it. Ownership moves
        once, cleanly, and the run log says when. Idle work is the failure; a filed row
        plus a fallback is the success.

        **AND THAT LAST SENTENCE WAS BEING SPENT ON UNCONFIRMED STATES.** Everything
        above is right for a lane that is CONFIRMED unable to take the work, and it was
        firing for any `not state.ok` at all — a single transient auth reading, a 60 s
        CLI timeout, an unreadable lock file. Those close a drain; they do not establish
        that Grok cannot do the job. So the gate is now the state's own
        `terminal` flag, read defensively: **absent means NOT terminal**, because a
        harness with no opinion must land on the reversible outcome.
        """
        if not bool(getattr(state, "terminal", False)):
            return self._stop_without_moving_ownership(state)
        pending = self.pending()
        note = self.root / "AUTH-BLOCKED.md"
        # VENDOR-GENERIC. The filename is unchanged because knight-rider's filing habit
        # and the `lane-status` check both look for it by name; the CONTENT names which
        # lane and which state, so a Grok block never reads as a Codex one.
        #
        # **AND THE FILENAME IS NOW ALSO WIDER THAN ITS CONTENT, DELIBERATELY.** A
        # terminal state no longer has to be a CREDENTIAL state — a refuted `--no-leader`
        # preflight is terminal and is not an auth problem — so `AUTH-BLOCKED.md` is now
        # the name of a CHANNEL rather than a claim about the cause. Renaming it per cause
        # was considered and REFUSED: `cli.py`'s `lane-status` tail and knight-rider's
        # filing habit both watch this exact name, and a block that lands under a name
        # nobody watches is a worse defect than a name that reads slightly wide. The
        # HEADING and the row inside say what it actually is.
        relogin = {"codex": "codex login", "grok": "~/.grok/bin/grok login"}.get(
            self.lane, f"re-authenticate the {self.lane} CLI"
        )
        # **THE REMEDY IS THE HARNESS'S TO NAME**, read defensively so that every existing
        # site and every harness with no opinion produces byte-identical text to before.
        # An empty remedy means the credential one, which is what every terminal state
        # meant when re-authentication was the only way a lane could be terminal.
        remedy = str(getattr(state, "remedy", "") or "").strip()
        matt_only = bool(getattr(state, "matt_only", True))
        if remedy:
            headline = f"**{self.lane} lane BLOCKED — `{state.state}`**"
            action = remedy
        else:
            headline = f"**{self.lane} lane re-authentication**"
            action = f"`{relogin}` on the Mac."
        owner = (
            "**MATT-ONLY.** Nobody else can perform this."
            if matt_only else
            "**NOT MATT-ONLY — DO NOT FILE THIS AS A MATT ACTION.** The remedy above is "
            "an engineering change on the owning seam. It is surfaced here because the "
            "queue stopped and work moved, not because a human credential is missing."
        )
        _atomic_write(note, (
            f"# {self.lane} lane BLOCKED — {utcnow()}\n\n"
            f"**State:** `{state.state}`\n\n"
            f"**Detected by:** `factory.jobqueue.JobQueue({self.root}, lane={self.lane!r}).drain`\n\n"
            f"{state.reason}\n\n"
            "## Ready-to-file `canonical/matt_to_do/` row\n\n"
            f"> {headline} — {action} "
            f"Blocks: the serialized {self.lane} worker lane (U-4). "
            f"Currently blocking **{len(pending)}** enqueued job(s) in `{self.root}`. "
            f"{owner} "
            "Pending work has been handed to the named Claude curators via "
            "`fallback/` manifests, so nothing is idle — but every fallback job is "
            f"Claude-lane tokens spent where subscription-native {self.lane} capacity "
            "was meant to absorb them.\n\n"
            "**This file was written by the queue. It is NOT filed. "
            "knight-rider files it.** The queue deliberately does not write into "
            "`canonical/matt_to_do/`: an unattributable automated row in a curated "
            "human queue is a governance surface with no author.\n"
        ))
        self.runlog.append(
            job_id="_lane", marker="AUTH-BLOCKED",
            detail=f"state={state.state} pending={len(pending)} note={note.name}",
            curator="knight-rider", event="finish",
        )
        self.telemetry.emit(
            # `outcome` is DERIVED from whether the harness named its own remedy, so a
            # consumer counting auth blocks stops counting preflight refutations among
            # them. `event` stays `lane_blocked` — the event's meaning (confirmed closure,
            # ownership moved, note written) did not change and consumers bind to it.
            "lane_blocked", lane=self.lane,
            outcome="auth_blocked" if not remedy else "lane_blocked",
            lane_state=state.state, error=state.reason,
            pending_jobs=len(pending),
            passthrough={
                "matt_to_do_draft": str(note),
                "matt_only_action": matt_only,
                "remedy": remedy or relogin,
                "response": "file the row, fall back to the Claude lane, do not retry",
            },
        )
        for job in pending:
            self._hand_to_claude(job, f"lane closed: {state.state}", None, None)
        return DrainReport(
            lane_state=state.state,
            stopped_reason=state.reason,
        )

    def _stop_without_moving_ownership(self, state: Any) -> DrainReport:
        """The lane is UNSAFE TO FIRE but NOT CONFIRMED CLOSED. Stop. Change nothing.

        Reached when a harness reports a not-ok state it has NOT established is terminal:
        a Grok `auth_unknown` (the CLI did not answer inside 60 s), an unreadable
        semaphore, or — before `AUTH_CONFIRM_READINGS` agree — a single not-authenticated
        auth reading, which is MEASURED to be what a routine token auto-refresh looks
        like from the outside (jack-ryan, 2026-08-25: `lane-status` said `auth_expired`;
        six probes seconds later all said logged-in).

        **THE THREE THINGS THIS DELIBERATELY DOES NOT DO**, each of which the old shared
        path did unconditionally:

          1. **No `fallback/` manifest and no `FALLBACK-CLAUDE` row.** P-7 makes
             ownership a one-way door — a drain after recovery must NOT pick the job back
             up — so spending it requires a positive finding, not the absence of one. A
             stopped drain resumes for free on the next invocation; a handed-off job
             never comes back.
          2. **No `AUTH-BLOCKED.md`.** That file escalates a MATT-ONLY re-authentication.
             Raising it for a lane that refreshed its own token five seconds ago trains
             the escalation surface to be ignored, which is worse than not having one.
          3. **No run-log row.** `RunLog.append` accepts a CLOSED marker vocabulary split
             into `TERMINAL_MARKERS` and `BUSY_MARKERS`, and both halves are wrong here:
             a terminal marker would say ownership moved, and a busy marker would leave
             the liveness surface's *"last row terminal"* check reading NOT IDLE with
             nothing running — wedging the lane on a condition that self-clears. The
             right answer is that this is a LANE event with no JOB in it, so it goes to
             the reporter surface and not the per-job ledger.

        It is NOT silent. Telemetry carries the condition with the count of jobs it did
        NOT touch, and the `DrainReport` carries a reason the CLI prints as `STOPPED:`.
        """
        pending = self.pending()
        self.telemetry.emit(
            "lane_stopped_unconfirmed", lane=self.lane, outcome="lane_unconfirmed",
            lane_state=state.state, error=getattr(state, "reason", ""),
            pending_jobs=len(pending),
            passthrough={
                "jobs_handed_to_claude": 0,
                "ownership_moved": False,
                "matt_only_action": False,
                "auth_blocked_note_written": False,
                "response": (
                    "stop this drain, touch nothing, re-probe on the next one — the "
                    "state was never confirmed terminal, and handing work over is the "
                    "one decision here that cannot be taken back"
                ),
            },
        )
        return DrainReport(
            lane_state=state.state,
            stopped_reason=(
                f"DRAIN STOPPED, NOTHING HANDED OFF — lane state {state.state!r} is "
                f"UNCONFIRMED, so {len(pending)} pending job(s) stay on this lane and "
                f"nothing was escalated. {getattr(state, 'reason', '')}"
            ),
        )
