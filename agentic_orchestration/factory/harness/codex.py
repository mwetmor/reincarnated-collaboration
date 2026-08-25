"""Codex CLI adapter — the second live lane.

Was an honest stub, blocked on Matt action T16. T16 is DONE (`codex login status`
-> `Logged in using ChatGPT`, verified on this host 2026-08-24), so the block the
stub named is gone and the stub is gone with it. `HONEST_STUB` and `BLOCKED_ON` are
DELETED rather than left lying beside working code: a stub marker next to a live
body is worse than either, because it tells its reader the lane is closed while the
lane runs.

FLAG SURFACE VERIFIED at codex-cli 0.147.0 on this host (star-lord probe,
2026-08-24). Every claim below was run, not read:

    codex exec --json --ephemeral --skip-git-repo-check -s read-only \\
        -m gpt-5.6-sol -c model_reasoning_effort="xhigh" -o <file> -

  * `--json` emits JSONL EVENTS to stdout: `thread.started`, `turn.started`,
    `item.started`, `item.completed`, `turn.completed`, and on failure
    `turn.failed` plus a top-level `error`.
  * `turn.completed` carries `usage` NATIVELY. That is the frame this adapter maps,
    and it is mapped through `UsageBreakdown` — the spine already has one usage
    vocabulary and does not get a second.
  * **THERE IS NO `turn.completed` ON FAILURE.** Measured with a deliberately bad
    `-m`: rc=1, a `turn.failed` frame, no `turn.completed`. Its ABSENCE is the
    failure signal, exactly as a missing `result` frame is on the Claude lane.
  * `-o/--output-last-message <FILE>` writes the final agent message to a file.
    The proven runner uses it; so does this.
  * The prompt goes on STDIN via the `-` argument, as the proven runner does. Not
    on argv: a 40 KB brief is a normal job on this lane and `ARG_MAX` is not a
    thing to discover in production.

  * WARNING - **STDERR IS NOT A FAILURE SIGNAL ON THIS LANE.** Measured: ALL 30 of
    the proven run's jobs returned rc=0 with NON-EMPTY stderr —
    `codex_models_manager` cache warnings and `rmcp::transport::worker` MCP auth
    failures, on every single job. A junk-detector keyed on stderr would have failed
    30 of 30 successes. Nothing here reads stderr for a verdict; it is CAPTURED
    (operators need it) and it is never adjudicated.

  * WARNING - **AMBIENT MCP SERVERS LOAD ON THIS LANE.** The same measurement shows
    a `vercel` MCP server being contacted (and failing auth) inside every
    `codex exec` of the proven run. That is the Claude lane's H2 finding — the
    ambient config is granted even under an explicit invocation — arriving on the
    second vendor. It is RECORDED here and NOT fixed here: `--ignore-user-config`
    would also drop the model pin (which lives in `~/.codex/config.toml`), so
    closing it properly means pinning the whole config surface on the argv, which is
    a separate decision with its own evidence. Naming it is not fixing it, and this
    comment does not claim otherwise.

THE MODEL PIN
-------------
The pin is `MODEL_PIN` / `MODEL_REASONING_EFFORT_PIN` below and it is passed ON THE
ARGV. It was previously only in `~/.codex/config.toml` — ambient host state that no
file in this repository controls and that any `codex` UI action can change. That is
the Claude lane's H1 finding on the second vendor, and the fix is the same: say it
on the command line.

What this adapter can and cannot prove about the pin, stated in both directions
because a check that only reports one is a check that reads as reassurance:

  * It CANNOT confirm the pin. `thread.started` carries only a `thread_id` and
    `turn.started` is empty — measured; no frame on this lane echoes the model. So
    unlike `check_grant` on the Claude lane, there is no init frame to re-read and
    assert equal. This adapter does not pretend otherwise.
  * It CAN disprove the pin. A model name the CLI does not know produces an
    `item.completed` whose item type is `error` and whose message begins
    "Model metadata for `X` not found" — measured. `adjudicate` treats that item as
    a FAILURE rather than as a warning, because a run that silently fell back to
    fallback metadata is not a run at the pinned config, and every banked lane
    statistic (34/34 clean, 93.2% cache-hit, the fabrication-check pass rate) was
    measured at the pinned config.
"""

from __future__ import annotations

import json
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..lane import SANDBOX_MODES, LaneBusy, SerialLaneLock, lane_is_free
from ..usage import UsageBreakdown
from .base import RawResult, register_harness

#: THE LANE CONFIG OF RECORD. Every banked lane statistic — 34/34 jobs rc=0, the
#: 93.2% cache-hit over 72,375,471 input tokens, the 22 oEmbed fabrication checks —
#: WAS MEASURED AT THIS CONFIG. A silent swap does not "try a different model": it
#: invalidates the entire baseline those numbers are the baseline FOR, silently, and
#: the next person to compare against them compares against nothing.
#:
#: Changing it requires the U-4 A/B evidence template — ~6 duplicate jobs at
#: candidate vs pinned, judged on curation WARN rate and URL-verification pass rate
#: — NEVER an edit to this line. `build_argv` enforces that mechanically: a config
#: naming a different model is refused unless it also names the A/B note that
#: authorises it, so drift is loud at the call site instead of invisible in a diff.
MODEL_PIN = "gpt-5.6-sol"
MODEL_REASONING_EFFORT_PIN = "xhigh"

#: The sandbox posture of record for RESEARCH jobs, and a DEFAULT rather than a
#: constant: a future job class may legitimately need `workspace-write`, and when it
#: does that must be a visible decision in the job record, not a code edit. Declared
#: per job class via `config["sandbox"]`, validated against the closed vocabulary.
DEFAULT_SANDBOX = "read-only"

DEFAULT_TIMEOUT_S = 3600

#: Substring of the CLI's own model-metadata-miss message. Matched, not parsed —
#: the sentence is the vendor's and may be reworded; what must not happen is that a
#: fallback-metadata run is counted as a run at the pin.
_MODEL_MISS_MARKER = "Model metadata for"

#: **CONSECUTIVE `auth_expired` READINGS REQUIRED BEFORE THIS LANE MAY MINT TERMINAL.**
#: Ported from the Grok lane on 2026-08-25, and the reason is recorded because the
#: reason is the only thing anyone should carry between vendors here.
#:
#: **THE PREMISE I ORIGINALLY SAID WAS MISSING WAS THE WRONG PREMISE.** I held this fix
#: on the ground that nobody has observed a ChatGPT-auth token refresh presenting as a
#: failed `codex login status` — true, still true, and NOT what the debounce is a remedy
#: for. The debounce is a remedy for minting an IRREVERSIBLE verdict from ONE sample of a
#: network-backed credential check. That is a reading-discipline argument and it is
#: vendor-independent; xAI's refresh timing is a vendor fact and does not travel. I
#: conflated the two, and knight-rider's dispatch was right to make me decide rather than
#: inherit.
#:
#: **AND ONE HALF OF THE HAZARD WAS LIVE AND NEEDED NO VENDOR PREMISE AT ALL.** MEASURED
#: against pre-fix source: with `terminal` defaulting `True`, an **`auth_unknown`** — the
#: 60 s `codex login status` timeout — handed the whole pending queue to the Claude
#: fallback through P-7's one-way door. *"The CLI did not answer in 60 seconds"* is not a
#: positive finding about anything, and it was spending the irreversible outcome. That is
#: a host hiccup emptying a queue, and no claim about OpenAI's token behaviour is
#: required to see it.
#:
#: ⚑ **A CLAIM I MADE HERE AND HAD TO WITHDRAW, KEPT because the withdrawal is the useful
#: part.** I first wrote that `busy` was terminal too and was handing queues away on lane
#: contention. **It was not.** `JobQueue.drain` guards with `if not state.ok and
#: state.state != "busy"`, so `busy` never reached `_stop_on_closed_lane`. My own test
#: went GREEN against pre-fix source and refuted me. What is true is narrower and still
#: worth recording: `busy` DID carry `terminal=True` — a field asserting it may move
#: ownership — and was saved only by a SEPARATE string comparison elsewhere. Two
#: mechanisms answered one question, by field and by name, and they disagreed. Latent,
#: not live. **The distinction is the whole discipline: an argument dressed as a
#: measurement is exactly what the honest-labelling of this constant exists to prevent.**
#:
#: **NOTHING HERE IS EVIDENCE THAT CODEX HAS THE REFRESH DEFECT.** It does not exist. The
#: `auth_expired` debounce is insurance chosen on cost asymmetry (~1-3 s and $0.00 against
#: the whole queue plus a false Matt escalation), exactly as on the Grok lane, and a later
#: reader must not mistake a ruling about reading discipline for a measurement.
AUTH_CONFIRM_READINGS = 3

#: `BASE * 2**(n-1)` -> 1 s, then 2 s. Same shape and same reasoning as the Grok lane's:
#: exponential so the two extra samples ask "did a fast refresh land" and "did a slow
#: one", rather than asking one question twice.
AUTH_CONFIRM_BACKOFF_BASE_S = 1.0


@dataclass(frozen=True)
class LaneAvailability:
    """`available()` in both directions, with the reason SURFACEABLE rather than swallowed.

    The stub returned a bare `False` and the reason lived in a module constant the
    loader had to reach in and read. A bare bool cannot distinguish "Matt must
    re-authenticate" (which no retry will fix) from "another job is running" (which
    the next drain will fix), and those are the two states an operator most needs
    told apart.
    """

    ok: bool
    state: str
    reason: str
    #: **CAN THIS STATE MOVE OWNERSHIP?** `False` means *stop the drain and change
    #: nothing*; `True` means *this lane is confirmed unable to take the work, so
    #: `jobqueue` may file the condition and hand pending jobs to the Claude fallback.*
    #:
    #: **DEFAULT FLIPPED `True` -> `False` ON 2026-08-25.** It shipped `True` as an
    #: honest declaration of an unfixed hazard, pinned by a green-on-purpose test. The
    #: hazard is now CLOSED, and the disposition is recorded at `AUTH_CONFIRM_READINGS`
    #: above rather than here because the reason is the interesting part.
    #:
    #: The short form: `True` made an **`auth_unknown` 60 s TIMEOUT terminal**, and that
    #: was measured against pre-fix source, not argued — a host hiccup handed the pending
    #: queue to Claude through a door that does not open again. No claim about OpenAI's
    #: token behaviour is needed to see it.
    #:
    #: Every construction site below now says `terminal=True` EXPLICITLY or means `False`
    #: when it stays silent, and `jobqueue` reads it by `getattr(state, "terminal",
    #: False)` so a harness with no opinion lands on the reversible outcome.
    terminal: bool = False
    #: What actually re-opens this lane, for the escalation artifact. Empty means the
    #: credential remedy (`codex login`), which is what every terminal state on this lane
    #: means today. Present for parity with the Grok lane so that `jobqueue` has ONE
    #: contract to read rather than a per-vendor special case; no Codex state sets it yet,
    #: and inventing a use for it here would be a field written to be exercised rather
    #: than a field written to be needed.
    remedy: str = ""
    #: Whether that remedy is a MATT-ONLY action. `True` for every current Codex terminal
    #: state: `cli_missing` and a confirmed `auth_expired` are both host-level.
    matt_only: bool = True


class CodexHarness:
    name = "codex"

    def __init__(
        self,
        executable: str = "codex",
        lock_path: Path | None = None,
        auth_probe: Any = None,
        sleep: Any = time.sleep,
    ):
        self.executable = executable
        self.lock_path = lock_path
        #: Injectable so the availability contract is TESTABLE without a network call
        #: and without a Matt-only logout. Gate-2 C3's lesson: a verdict that can only
        #: be checked by spending money is a verdict nobody checks.
        self._auth_probe = auth_probe
        #: Injected for the same reason, one level down: the DEBOUNCE is now the thing
        #: under test, and a test that had to spend 3 real seconds to exercise it is a
        #: test that gets deleted the first time the suite feels slow.
        self._sleep = sleep

    # -- availability -------------------------------------------------------
    def probe_auth_once(self) -> LaneAvailability:
        """ONE reading of `codex login status`. No re-probe, NEVER terminal-by-auth.

        The raw instrument. It answers *"what did the CLI say just now"* and deliberately
        nothing else; `check_auth` is what turns readings into a VERDICT. The split is
        the remedy itself — while one method answered both questions, a reading and a
        verdict were the same object, and a single bad reading was a terminal verdict by
        construction.

        MEASURED (2026-08-24, codex-cli 0.147.0): logged in -> **rc=0, STDOUT EMPTY,
        and `Logged in using ChatGPT\\n` on STDERR.**

        WARNING - **THE ANSWER IS ON STDERR, AND THIS METHOD SHIPPED READING STDOUT.**
        This is a defect I introduced and the LIVE round-trip caught; it is recorded
        here rather than quietly repaired, because the way it was made is worth more
        than the fix. I ran `codex login status` in a terminal, saw the sentence, and
        wrote `proc.stdout` — a terminal merges the two streams, so what I actually
        measured was "the sentence appears somewhere" and what I wrote down was "the
        sentence appears on stdout". `capture_output=True` does not merge them.

        Its consequence is worth stating precisely, because "fails closed" is not the
        same as "harmless": with stdout empty, the check returned `auth_expired`
        UNCONDITIONALLY. `available()` would never have returned True, the queue would
        never have drained a job, and every enqueued job would have been handed to the
        Claude lane with a `matt_to_do` row demanding re-authentication of a lane that
        was already authenticated. A permanently-closed lane fails safe and delivers
        zero uptime, which is this dispatch's whole subject. NO UNIT TEST COULD HAVE
        FOUND IT — the fake `codex` binaries in the suite were written by me, against
        the same wrong belief, and they agreed with the bug.

        Both streams are read now. The NEGATIVE branch remains REASONED, NOT MEASURED,
        and this sentence is the record of that: verifying the vendor's real
        not-logged-in text requires `codex logout`, a Matt-only action on a live lane.
        It fails CLOSED — a non-zero exit, an unrecognised answer, or a missing binary
        all read as "not authenticated". Given the above, treat that untested branch as
        genuinely untested rather than as covered by symmetry.

        **AND THE DOWNSTREAM OF THAT DISCLOSURE IS NOW FOLLOWED**, which it was not while
        this method was also the verdict: the untested negative branch went straight to
        `jobqueue._stop_on_closed_lane`, which is terminal by design. No caller gets the
        raw reading unless it asks for it by this name.
        """
        if self._auth_probe is not None:
            return self._auth_probe()
        try:
            proc = subprocess.run(
                [self.executable, "login", "status"],
                capture_output=True, text=True, timeout=60, stdin=subprocess.DEVNULL,
            )
        except FileNotFoundError:
            return LaneAvailability(
                False, "cli_missing",
                f"{self.executable!r} is not on PATH; the Codex lane cannot be reached "
                "from this process at all",
                # TERMINAL on a DIFFERENT footing from the credential readings: this is a
                # filesystem fact, deterministic, with no refresh window to race. One
                # reading IS the confirmation and re-probing would spend wall time
                # re-learning a constant.
                terminal=True,
            )
        except subprocess.TimeoutExpired:
            return LaneAvailability(
                False, "auth_unknown",
                "`codex login status` did not answer within 60s. Absence of an answer "
                "is not a pass — the lane is treated as closed for THIS DRAIN, and "
                "nothing more.",
                # **NEVER TERMINAL, AT ANY READING COUNT.** A timeout is the absence of an
                # answer, not an answer of "expired". Fire-unsafe, which stops the drain;
                # not ownership-transferring, which would need a positive finding.
                terminal=False,
            )
        # BOTH streams. The vendor puts the answer on stderr; reading one stream is
        # how this method spent a build reporting a healthy lane as expired.
        answer = "\n".join(
            part for part in ((proc.stdout or "").strip(), (proc.stderr or "").strip())
            if part
        )
        if proc.returncode == 0 and "logged in" in answer.lower():
            return LaneAvailability(True, "open", answer or "logged in")
        return LaneAvailability(
            False, "auth_expired",
            "Codex auth is not healthy (`codex login status` exited "
            f"{proc.returncode}: {answer[:300] or 'no output on either stream'}).",
            # UNCONFIRMED — one reading. The MATT-ONLY claim and the fallback are NOT made
            # here any more; `check_auth` adds them after the readings agree.
            terminal=False,
        )

    def check_auth(self) -> LaneAvailability:
        """THE VERDICT. Debounced, and the ONLY thing on this lane that may mint terminal.

        Mirrors the Grok lane's, and the placement is the same deliberate one: at the
        narrowest waist every consumer already goes through, so that `factory lane-status`
        — the surface a HUMAN reads a lane verdict off — cannot report a blip as a
        closure. Putting it at the drain boundary would have been the easier write.

        **`auth_unknown` DOES NOT ENTER THE LOOP.** No count of timeouts is a positive
        finding, so re-probing one buys only wall time on the way to the same verdict, and
        would push a `lane-status` worst case from 60 s to 180 s to answer a question it
        already answered.

        The raw single reading is still available, by the name `probe_auth_once`, so a
        caller that genuinely wants an undebounced instrument reading must say so and
        cannot get one by accident.
        """
        reading = self.probe_auth_once()
        if reading.ok or reading.state != "auth_expired":
            return reading

        readings = 1
        started = time.monotonic()
        while readings < AUTH_CONFIRM_READINGS:
            self._sleep(AUTH_CONFIRM_BACKOFF_BASE_S * (2 ** (readings - 1)))
            reading = self.probe_auth_once()
            readings += 1
            if reading.ok:
                # THE TRANSIENT, ABSORBED — and SAID rather than swallowed, so that "this
                # lane blipped and recovered" is a visible lane event and not a silence
                # identical to a lane that never blipped.
                return LaneAvailability(
                    True, "open",
                    f"{reading.reason}  [auth reading 1 said not-authenticated and "
                    f"reading {readings} said logged-in after "
                    f"{time.monotonic() - started:.1f}s — TRANSIENT, absorbed]",
                )
            if reading.state != "auth_expired":
                # The confirmation could not be COMPLETED. Not a confirmed expiry — a
                # different unresolved state, travelling on its own `terminal` value
                # rather than inheriting a verdict from reading 1.
                return reading

        return LaneAvailability(
            False, "auth_expired",
            f"{reading.reason} CONFIRMED by {readings} consecutive readings over "
            f"{time.monotonic() - started:.1f}s. THIS IS NOT A JOB FAILURE AND MUST NOT "
            "BE RETRIED: re-authentication is a MATT-ONLY action. The queue stops taking "
            "Codex jobs, files the condition, and hands pending work to the named Claude "
            "curator's lane — idle work is the failure, a filed row plus a fallback is "
            "the success.",
            # The ONE site on this lane that mints terminal from a credential reading.
            terminal=True,
        )

    def availability(self) -> LaneAvailability:
        """Auth first, then busy. Order matters: an expired lane is not a busy lane."""
        auth = self.check_auth()
        if not auth.ok:
            return auth
        if not lane_is_free(self.lock_path):
            return LaneAvailability(
                False, "busy",
                "another `codex exec` holds the serial lane. ONE `codex exec` at a "
                "time, one `auth.json`, one job stream — queue behind it or fire the "
                "Claude lane, NEVER parallel.",
                # **SAID EXPLICITLY, AND UNTIL 2026-08-25 THE FIELD SAID THE OPPOSITE.**
                # `busy` is OCCUPIED, not CLOSED — it clears by itself when the holder
                # finishes, and a drainer's answer to it is to queue behind, never to hand
                # work over.
                #
                # It carried `terminal=True` by default, and was saved only by a SEPARATE
                # guard in `JobQueue.drain` (`state.state != "busy"`, keyed on the state's
                # NAME). Two mechanisms answered one question — one by field, one by
                # string — and they DISAGREED; inert only because the string one runs
                # first. Renaming this state, or reaching `_stop_on_closed_lane` from any
                # other caller, would have let the field's answer win. **Latent, never
                # live** (a test written on the assumption it WAS live went green against
                # pre-fix source and refuted the assumption). Said here so the two
                # mechanisms now agree rather than merely not colliding.
                terminal=False,
            )
        return LaneAvailability(True, "open", auth.reason)

    def available(self) -> bool:
        """Duck-typed at `workflow.py`, and DELIBERATELY NOT ON THE `HarnessAdapter` PROTOCOL.

        Promoting it was considered and REFUSED, and this is the record of that
        decision rather than a thing left unsaid (it is also named in
        `factory/MIGRATION.md`, because it is the kind of choice a later reader will
        assume was an oversight).

        `base.HarnessAdapter` declares `name` and `run`. Adding `available` makes
        `ClaudeCodeHarness` a non-conforming implementation of the protocol it is
        the reference for — which leaves two exits, and both are worse than
        duck-typing:

          * give the Claude lane an `available()` that returns `True` — a green
            nobody measured, in a tree whose loudest rule is that a checker
            returning green because nobody wrote it is a stub wearing a gate's name;
          * or make it probe `claude` on every workflow load, which is a subprocess
            per load to answer a question the Claude lane has never needed asked.

        Duck-typing says the honest thing: a lane that CAN answer "am I open?"
        answers, and a lane that cannot is not asked. `workflow.py` already spells it
        exactly that way (`if callable(available) and not available()`).

        ADVISORY, in both directions. The `busy` half is a PROBE — it acquires the
        flock and releases it — so between this answer and any use of it the lane can
        change hands. The GUARANTEE is `SerialLaneLock` held across the
        `subprocess.run` call in `run()`, and that is the only place the lane is
        actually reserved. Nothing may substitute this for that.
        """
        return self.availability().ok

    def unavailable_reason(self) -> str:
        """Read by `workflow.py` when a phase's lane is closed at LOAD.

        Replaces the module-level `BLOCKED_ON` the stub published: a lane with three
        distinct closed states cannot say which one it is in through a constant
        string fixed at import time.
        """
        state = self.availability()
        return "" if state.ok else f"{state.state}: {state.reason}"

    # -- the fence ----------------------------------------------------------
    @staticmethod
    def validate_tools(tools: object, where: str) -> list[str]:
        """REFUSES. The Codex lane's pre-hoc fence is the SANDBOX, not a tool allowlist.

        `workflow.py` requires every harness carrying an agentic phase to publish
        this, so that the loader never has its own opinion about what a tool name is.
        This lane's honest answer is that it does not implement the mechanism at all:
        there is no `--tools` on `codex exec`, so a phase declaring `tools:` would be
        declaring a fence that this lane cannot hold — and ACCEPTING the list would
        be the fail-open, because the workflow would read as fenced and would not be.

        Refused with a pointer at the fence this lane DOES have (`sandbox:`, a closed
        vocabulary validated in `build_argv`) rather than with a bare no.
        """
        raise ValueError(
            f"{where}: the codex lane has no tool allowlist. `codex exec` exposes no "
            "`--tools` flag, so a `tools:` declaration here would name a fence this "
            "lane cannot hold — and a workflow would read as contained while not "
            "being. This lane's pre-hoc containment is its SANDBOX MODE: declare "
            f"`sandbox:` from {sorted(SANDBOX_MODES)} instead. The posture of record "
            f"for research jobs is {DEFAULT_SANDBOX!r}."
        )

    # -- argv ---------------------------------------------------------------
    @staticmethod
    def _image_argv(config: dict[str, Any]) -> list[str]:
        """`-i/--image` — the vendor's image door, which this harness never opened.

        **THE SITUATION THIS CLOSES.** Matt asked for Codex and Grok second opinions on
        VFX frames. `codex exec` publishes `-i, --image <FILE>...` (*"Optional image(s) to
        attach to the initial prompt"*, verified on this host at the CLI's own `--help`),
        and `build_argv` emitted no such flag at any call site — `grep image|vision|
        attach|png|base64` across `factory/harness/*.py` returned zero hits. The lane was
        capable at the vendor and blocked by us.

        **NO IMAGES MEANS NO ARGV, BYTE FOR BYTE.** Every existing Codex call must be
        unchanged, and the risk here was never that images break — it is that adding a
        parameter silently perturbs 34 banked jobs' invocation shape. `[]` in, `[]` out,
        pinned by a test that compares a no-images argv against the literal current one.

        **ONE `-i` PER FILE, NOT ONE `-i` WITH MANY VALUES.** `<FILE>...` is a greedy
        multi-value option, and this lane's argv ENDS in a bare `-` (the stdin marker for
        the prompt). `-i a.png b.png -` would let the greedy list reach for that `-` and
        eat the prompt door. Repeating the flag terminates each occurrence at the next
        flag-shaped token and never approaches the tail. It is also why the images are
        emitted HERE — before `-m`, mid-argv — rather than adjacent to the `-` where they
        read more naturally.

        **PATHS ARE VALIDATED AT THE BOUNDARY** (discipline #8). A named image that does
        not exist is refused at argv construction, where the caller learns which path and
        why, instead of at the vendor, where it costs a launched process to learn that a
        typo was a typo. It is refused rather than dropped: an image the caller asked for
        and did not get, on a job whose whole purpose is to LOOK AT the image, produces an
        answer about nothing that reads exactly like an answer about something.
        """
        raw = config.get("images") or []
        if isinstance(raw, (str, Path)):
            raise ValueError(
                f"codex harness: `images` is {raw!r}, a single path. It must be a LIST of "
                "paths — a bare string would iterate character by character and emit one "
                "`-i` per letter, which the CLI would reject in a way that names neither "
                "the config key nor the mistake."
            )
        argv: list[str] = []
        for entry in raw:
            path = Path(entry).expanduser()
            if not path.is_file():
                raise ValueError(
                    f"codex harness: image {str(path)!r} does not exist (or is not a "
                    "file). REFUSED rather than dropped: a vision job silently missing "
                    "its image still returns a confident answer, and that answer is "
                    "about nothing while reading exactly like an answer about something."
                )
            argv += ["-i", str(path)]
        return argv

    def build_argv(self, config: dict[str, Any]) -> list[str]:
        sandbox = str(config.get("sandbox", DEFAULT_SANDBOX))
        if sandbox not in SANDBOX_MODES:
            raise ValueError(
                f"codex harness: sandbox {sandbox!r} is not one of {sorted(SANDBOX_MODES)}. "
                "The sandbox is this lane's pre-hoc containment; a value nobody "
                "enumerated is not a posture, it is a typo that would be passed to the "
                "CLI and adjudicated by nothing."
            )

        model = str(config.get("model", MODEL_PIN))
        effort = str(config.get("reasoning_effort", MODEL_REASONING_EFFORT_PIN))
        if (model, effort) != (MODEL_PIN, MODEL_REASONING_EFFORT_PIN):
            if not str(config.get("model_ab_note", "")).strip():
                raise ValueError(
                    f"codex harness: config asks for model={model!r} "
                    f"effort={effort!r}, which is not the pin "
                    f"({MODEL_PIN!r} @ {MODEL_REASONING_EFFORT_PIN!r}). EVERY banked "
                    "lane statistic was measured at the pin, so an unannounced swap "
                    "does not produce a different result — it produces results that "
                    "cannot be compared to anything and look like they can. U-4 "
                    "requires A/B evidence (~6 duplicate jobs, candidate vs pinned; "
                    "criteria = curation WARN rate + URL-verification pass rate). Name "
                    "the note in `model_ab_note` and this refusal lifts."
                )

        argv = [self.executable, "exec", "--json"]
        if config.get("ephemeral", True):
            argv.append("--ephemeral")
        if config.get("skip_git_repo_check", True):
            argv.append("--skip-git-repo-check")
        argv += ["-s", sandbox]
        argv += self._image_argv(config)
        # H1 on the second vendor: the pin is said ON THE ARGV, not left to
        # `~/.codex/config.toml`, which is ambient host state no file here controls.
        argv += ["-m", model]
        argv += ["-c", f'model_reasoning_effort="{effort}"']
        if config.get("web_search"):
            argv += ["-c", "tools.web_search=true"]
        output_path = config.get("output_path")
        if output_path:
            argv += ["-o", str(output_path)]
        for extra in config.get("extra_config", []) or []:
            argv += ["-c", str(extra)]
        argv.append("-")  # prompt arrives on stdin
        return argv

    # -- run ----------------------------------------------------------------
    def run(self, prompt: str, cwd: Path, config: dict[str, Any]) -> RawResult:
        """One job. THE LOCK IS HELD ACROSS THE `codex exec` CALL AND NOWHERE ELSE.

        This is the invocation site Gate-1's tightening is about, and it is the only
        place in this package that spawns `codex`. A caller that already holds the
        lane will be REFUSED here (measured: `flock` conflicts across two `open()`
        calls in the same process, errno 35), which is why `JobQueue.drain` must not
        wrap its loop in the lock — and `tests/test_lane.py` proves that the refusal
        fires rather than deadlocking.

        NEVER raises for an operational condition. A closed lane, a missing binary, a
        busy lane and a failed turn all come back as `RawResult(ok=False)` with an
        `error` that says which — because the spine records a RawResult and cannot
        record an exception.
        """
        raw_path = config.get("raw_output_path")
        prompt_path = config.get("prompt_path")
        timeout_s = int(config.get("timeout_s", DEFAULT_TIMEOUT_S))
        output_path = config.get("output_path")

        try:
            argv = self.build_argv(config)
        except ValueError as exc:
            return RawResult(
                ok=False, harness=self.name, error=str(exc),
                usage=UsageBreakdown.absent("harness never launched: refused at argv"),
            )

        started = time.monotonic()
        try:
            lock = SerialLaneLock(self.lock_path).acquire()
        except LaneBusy as exc:
            return RawResult(
                ok=False, harness=self.name, error=str(exc),
                usage=UsageBreakdown.absent("harness never launched: lane busy"),
                extra={"lane_state": "busy"},
            )
        try:
            try:
                proc = subprocess.run(
                    argv,
                    cwd=str(cwd),
                    input=prompt,
                    capture_output=True,
                    text=True,
                    timeout=timeout_s,
                    # THE CRASH-SAFETY LINE. The child inherits the locked descriptor,
                    # so the lane stays held for as long as `codex exec` LIVES and not
                    # one instant past it — no stale lock if this process is killed, and
                    # no unlocked lane if this process is killed while the child runs.
                    pass_fds=(lock.fd,),
                )
            except FileNotFoundError:
                return RawResult(
                    ok=False, harness=self.name,
                    error=f"{self.executable} not found on PATH",
                    usage=UsageBreakdown.absent("harness never launched"),
                )
            except subprocess.TimeoutExpired:
                return RawResult(
                    ok=False, harness=self.name,
                    error=f"codex exec exceeded {timeout_s}s and was killed",
                    usage=UsageBreakdown.absent("harness killed on timeout; no turn.completed"),
                )
        finally:
            lock.release()
        elapsed_ms = int((time.monotonic() - started) * 1000)

        if raw_path:
            Path(raw_path).parent.mkdir(parents=True, exist_ok=True)
            Path(raw_path).write_text(proc.stdout, encoding="utf-8")
            # Captured because operators need it; ADJUDICATED BY NOTHING, because all
            # 30 jobs of the proven run wrote to it while returning rc=0.
            Path(str(raw_path) + ".stderr").write_text(proc.stderr or "", encoding="utf-8")
        if prompt_path:
            Path(prompt_path).parent.mkdir(parents=True, exist_ok=True)
            Path(prompt_path).write_text(prompt, encoding="utf-8")

        return self.adjudicate(
            parse_events(proc.stdout),
            returncode=proc.returncode,
            elapsed_ms=elapsed_ms,
            raw_path=raw_path,
            prompt_path=str(prompt_path) if prompt_path else None,
            output_path=str(output_path) if output_path else None,
            model=str(config.get("model", MODEL_PIN)),
            stderr=proc.stderr or "",
        )

    # -- adjudication -------------------------------------------------------
    def adjudicate(
        self,
        events: list[dict[str, Any]],
        *,
        returncode: int,
        elapsed_ms: int = 0,
        raw_path: str | None = None,
        prompt_path: str | None = None,
        output_path: str | None = None,
        model: str = MODEL_PIN,
        stderr: str = "",
    ) -> RawResult:
        """Turn a stream of events into a verdict. Separated from `run` so it is TESTABLE.

        The Claude lane learned this at Gate-2 C3: adjudication buried inside `run()`
        behind a live subprocess can only be exercised by invoking a model, which
        means nothing exercises it.
        """
        completed = next((e for e in reversed(events) if e.get("type") == "turn.completed"), None)
        failed = next((e for e in reversed(events) if e.get("type") == "turn.failed"), None)
        stream_error = next((e for e in reversed(events) if e.get("type") == "error"), None)
        thread = next((e for e in events if e.get("type") == "thread.started"), None)
        message = next(
            (str((e.get("item") or {}).get("text", "")) for e in reversed(events)
             if e.get("type") == "item.completed"
             and (e.get("item") or {}).get("type") == "agent_message"),
            "",
        )
        model_miss = next(
            (str((e.get("item") or {}).get("message", "")) for e in events
             if e.get("type") == "item.completed"
             and (e.get("item") or {}).get("type") == "error"
             and _MODEL_MISS_MARKER in str((e.get("item") or {}).get("message", ""))),
            None,
        )

        extra: dict[str, Any] = {
            "elapsed_ms": elapsed_ms,
            "event_count": len(events),
            "stderr_bytes": len(stderr),
            "reasoning_effort": MODEL_REASONING_EFFORT_PIN,
        }

        if completed is None:
            reason = (
                ((failed or {}).get("error") or {}).get("message")
                or (stream_error or {}).get("message")
                or (stderr.strip()[-300:] if stderr.strip() else "no stderr")
            )
            return RawResult(
                ok=False, harness=self.name,
                harness_session_id=(thread or {}).get("thread_id"),
                model=model, exit_code=returncode,
                raw_output_path=raw_path, prompt_path=prompt_path,
                error=(
                    f"no `turn.completed` in the stream (exit {returncode}). On this "
                    f"lane that absence IS the failure signal: {reason}"
                ),
                usage=UsageBreakdown.absent("stream carried no turn.completed frame"),
                extra=extra,
            )

        usage = UsageBreakdown.from_codex_turn_completed(completed)
        if model_miss:
            return RawResult(
                ok=False, text=message, usage=usage, harness=self.name,
                harness_session_id=(thread or {}).get("thread_id"),
                model=model, exit_code=returncode,
                raw_output_path=raw_path, prompt_path=prompt_path,
                error=(
                    f"the CLI did not recognise the pinned model and fell back to "
                    f"fallback metadata: {model_miss!r}. A run at fallback metadata is "
                    "not a run at the pin, and every banked lane statistic is a "
                    "statistic ABOUT the pin. Failed rather than warned."
                ),
                extra={**extra, "model_metadata_miss": model_miss},
            )
        ok = returncode == 0
        missing_output = bool(ok and output_path and not Path(output_path).exists())
        if missing_output:
            ok = False
        return RawResult(
            ok=ok,
            text=message,
            usage=usage,
            harness=self.name,
            harness_session_id=(thread or {}).get("thread_id"),
            model=model,
            exit_code=returncode,
            raw_output_path=raw_path,
            prompt_path=prompt_path,
            error=(
                None if ok
                else f"the turn completed but the declared output {output_path!r} was never written"
                if missing_output
                else f"codex exec exited {returncode}"
            ),
            extra={**extra, "output_path": output_path},
        )


def parse_events(stdout: str) -> list[dict[str, Any]]:
    """Parse `codex exec --json` JSONL. Unparseable lines are skipped, not guessed at."""
    events: list[dict[str, Any]] = []
    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            events.append(parsed)
    return events


HARNESS = register_harness(CodexHarness())
