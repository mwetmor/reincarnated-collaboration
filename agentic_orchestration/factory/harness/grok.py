"""Grok CLI adapter — the THIRD lane, and the second vendor lane.

Build-authorized 2026-08-24 by jack-ryan's re-ratification addendum (D-6…D-8), after
Matt exercised the AM-1 § 13.3 release valve and widened Grok from the U-8-judge-door
to a general second vendor lane. Amendments C, D and E ride this file and are cited
inline where they are enforced rather than summarised at the top.

**THE SERIAL POLICY, AND WHY IT IS NOT THE CODEX LAW.** This lane takes a
`SerialLaneLock` exactly as the Codex lane does, and the two are NOT the same kind of
rule. Codex's serial law cites a VERIFIED VENDOR PRECONDITION (OpenAI CI/CD auth: one
machine or a serialized job stream). **No equivalent xAI statement has been
verified.** This lane is serialised BY CHOICE — G-2's false-busy ruling applied at the
policy level: serial costs delay, parallel-on-an-unknown-constraint risks an
account-level fault. Loosening it requires the evidence NAMED, by amendment to the
lane spec — but it is a policy, and a future reader who finds the same primitive on
both lanes must be able to tell which one is a law. That is what this paragraph is
for, and jack-ryan required it by name.

FLAG SURFACE VERIFIED at grok 1.0.5 (5115b46bc909) [stable] on this host (star-lord
probe, 2026-08-24). Every claim below was RUN, not read:

  * `grok -p "<prompt>" --output-format json` -> one JSON object on stdout with
    `text` / `stopReason` / `sessionId` / `requestId` / `num_turns` / `usage` /
    `modelUsage` / `total_cost_usd`. That envelope shape is the Claude lane's, not
    Codex's, and `usage.py` maps it accordingly (see `from_grok_envelope`).
  * `-m/--model` and `--reasoning-effort` both exist at the TOP LEVEL (verified in
    `grok --help`). The effort vocabulary is enumerated by the CLI's own error
    surface: `--reasoning-effort bogusvalue` -> *"unknown effort level 'bogusvalue';
    use one of: xhigh, high, medium, low"* — identical to Codex's.
  * `--disable-web-search` exists and is the posture of record: web access is granted
    only when a job class NAMES it.
  * `--permission-mode` is a CLOSED vocabulary printed by `--help`:
    default / acceptEdits / auto / dontAsk / bypassPermissions / plan. Two of those
    are REFUSED here by name (see `FORBIDDEN_PERMISSION_MODES`).
  * `grok models` -> rc=0 and *"You are logged in with grok.com."* — the auth check of
    record, cheap and exercising real credential state.

  * WARNING - **`--no-leader` IS ACCEPTED BUT UNDOCUMENTED AT THE TOP-LEVEL SURFACE.**
    Measured both directions this session: `grok --no-leader --version` exits **0**; a
    known-bogus flag exits **2** with *"error: unexpected argument"*. The flag is
    absent from `grok --help` and documented only under `grok agent --help`. Leader
    mode multiplexes multiple clients onto one backend through `~/.grok/leader.sock`,
    which is a concurrency door AROUND the serial lock — so the prohibition rests on a
    hidden flag, and a version bump could remove it with no help-diff to signal the
    change. The failure would be silent re-entry through the exact door the lock
    exists to close. **Amendment E, BINDING: the preflight ASSERTS the flag parses
    (rc check, no model call, no cost) and the lane REFUSES TO FIRE if the assertion
    fails.** Never assumed.

  * WARNING - **`--sandbox <PROFILE>` EXISTS ON THIS CLI AND IS DELIBERATELY NOT SAID.**
    Its profile vocabulary has not been probed on this host, and declaring a fence
    value nobody enumerated is how a workflow reads as contained while not being. This
    lane's declared fence is `--permission-mode` + `--allow`/`--deny` +
    `--disable-web-search` (lane spec § 9.3). Naming the gap is not closing it, and
    this comment does not claim otherwise.

THE MODEL PIN, AND WHAT IT IS HONESTLY WORTH
--------------------------------------------
`MODEL_PIN` @ `REASONING_EFFORT_PIN`, both said ON THE ARGV from the FIRST job
(Amendment D) — never left to `~/.grok/config.toml`, which is ambient host state that
no file in this repository controls.

**This pin is DECLARED, NOT BANKED.** Zero lane statistics exist at any Grok config.
The Codex pin's authority comes from 30/30 jobs measured at it; this one has nothing
behind it yet, and saying otherwise would launder a default into a baseline. The first
10 production jobs ARE the banking window (Amendment I), with a verdict point at job
10.

**Amendment C, BINDING: the DECLARED pin is not the RESOLVED model.** `grok-4.6`
resolves to `grok-4.6-build` in headless mode — a vendor-side rule chose that, not us.
A pin whose resolved target is chosen by the vendor is a REQUEST, not a pin, and P-5's
grounding fails silently if the resolution moves under a CLI update. So every call
captures the resolved identifier out of the envelope's `modelUsage` keys and records
it. A change in the resolved id at an unchanged declared pin is a LANE EVENT THAT MUST
BE VISIBLE, not a silent substitution.
"""

from __future__ import annotations

import json
import os
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..lane import LaneBusy, SerialLaneLock, default_lock_path, lane_is_free
from ..usage import UsageBreakdown
from .base import RawResult, register_harness

#: THE LANE CONFIG OF RECORD — declared, NOT banked. See the module docstring.
MODEL_PIN = "grok-4.6"
REASONING_EFFORT_PIN = "xhigh"

#: The CLI's own effort vocabulary, enumerated from its error surface rather than from
#: documentation (`--reasoning-effort bogusvalue` prints the list). CLOSED: a value
#: outside it is a typo the CLI would reject at a cost we already know how to avoid.
REASONING_EFFORTS = frozenset({"xhigh", "high", "medium", "low"})

#: `--permission-mode` values this lane REFUSES BY NAME. Both of them dissolve the
#: fence: `bypassPermissions` removes it and `dontAsk` auto-answers it. A research
#: lane that can be talked into either has no pre-hoc containment at all, and the
#: refusal is at the argv builder so it fires before a process exists.
FORBIDDEN_PERMISSION_MODES = frozenset({"bypassPermissions", "dontAsk"})

#: The permission modes a job class may declare. `default` is the posture of record
#: for single-turn research jobs.
PERMISSION_MODES = frozenset({"default", "acceptEdits", "auto", "plan"})
DEFAULT_PERMISSION_MODE = "default"

#: The prohibition of record. Said on EVERY argv, and preflight-asserted (Amendment E).
NO_LEADER_FLAG = "--no-leader"

#: `~/.grok/bin/grok`, and the environment variable that relocates it. The binary is
#: **NOT ON PATH** on this host — `shutil.which("grok")` returns None — so it is
#: resolved EXPLICITLY. A harness that shelled out to a bare `grok` would report
#: `cli-missing` on a lane that is installed and authenticated, which is the Codex
#: lane's own auth-stream defect arriving on the third lane by a different route.
GROK_BINARY_ENV = "REINCARNATED_GROK_BIN"
GROK_HOME_ENV = "GROK_HOME"
DEFAULT_GROK_HOME = "~/.grok"
DEFAULT_GROK_BINARY_RELATIVE = "bin/grok"

DEFAULT_TIMEOUT_S = 3600

#: The prompt travels on ARGV (`-p`), which is the invocation of record. `ARG_MAX` on
#: this host is ~1 MB, so a 40 KB brief is comfortable — but "comfortable" is not a
#: bound, so the bound is declared here and REFUSED at the argv builder rather than
#: discovered as an `E2BIG` in production. `grok --prompt-file <PATH>` exists and is
#: the door if a job class ever needs to go past this; taking that door is a job-class
#: decision with its own record, not a silent widening of this constant.
MAX_PROMPT_ARGV_BYTES = 256 * 1024


def resolve_grok_home() -> Path:
    """The credential home this lane is serialised against. `~/.grok` unless told otherwise."""
    return Path(os.environ.get(GROK_HOME_ENV) or DEFAULT_GROK_HOME).expanduser()


def resolve_grok_binary() -> Path | None:
    """Where the CLI actually is, or None. Explicit resolution; never a bare `grok`.

    Order: the env override, then `<grok home>/bin/grok`. PATH is deliberately NOT
    consulted first — the install of record is inside the credential home, and if a
    different `grok` ever appears on PATH it would be a different install pointing at
    a different home, which is a different LANE under P-3.
    """
    override = os.environ.get(GROK_BINARY_ENV)
    if override:
        path = Path(override).expanduser()
        return path if path.exists() else None
    candidate = resolve_grok_home() / DEFAULT_GROK_BINARY_RELATIVE
    return candidate if candidate.exists() else None


def grok_lock_path() -> Path:
    """This lane's lock, keyed to `~/.grok` — an INDEPENDENT lane from Codex's.

    Per-credential (P-3): `~/.grok/auth.json` is not `~/.codex/auth.json`, so a busy
    Codex lane does NOT close this one and running both at once is LEGAL and intended.
    The law was never "one vendor process per host"; it is "one job stream per
    credential."
    """
    return default_lock_path(resolve_grok_home(), vendor="grok")


@dataclass(frozen=True)
class LaneAvailability:
    """`available()` in both directions, with the reason SURFACEABLE rather than swallowed.

    Structurally identical to the Codex lane's, and duplicated rather than shared on
    purpose: the two lanes' availability vocabularies are allowed to diverge as their
    vendors diverge, and a shared type would make the next divergence look like a
    change to the other lane.
    """

    ok: bool
    state: str
    reason: str


class GrokPreflightFailed(RuntimeError):
    """Amendment E's refusal. Raised where it can be caught and turned into a RawResult."""


class GrokHarness:
    name = "grok"

    def __init__(
        self,
        executable: str | os.PathLike[str] | None = None,
        lock_path: Path | None = None,
        auth_probe: Any = None,
        preflight_probe: Any = None,
    ):
        #: `None` means "resolve at use", so that a test setting the env var after
        #: construction still gets the right binary and so a missing binary is a
        #: reported STATE rather than a constructor explosion.
        self._executable = str(executable) if executable else None
        self._lock_path = lock_path
        #: Injectable so both contracts are TESTABLE without a network call, without a
        #: Matt-only logout, and without a vendor binary present at all. Gate-2 C3's
        #: lesson: a verdict that can only be checked by spending money is a verdict
        #: nobody checks.
        self._auth_probe = auth_probe
        self._preflight_probe = preflight_probe
        self._preflight_result: tuple[bool, str] | None = None

    # -- resolution ---------------------------------------------------------
    @property
    def executable(self) -> str | None:
        if self._executable:
            return self._executable
        found = resolve_grok_binary()
        return str(found) if found else None

    @property
    def lock_path(self) -> Path:
        return self._lock_path if self._lock_path is not None else grok_lock_path()

    # -- Amendment E: the preflight assertion -------------------------------
    def assert_no_leader_parses(self, force: bool = False) -> tuple[bool, str]:
        """AMENDMENT E. Assert `--no-leader` is ACCEPTED. Refuse the lane if it is not.

        The test is the cheapest one that can distinguish acceptance from rejection:
        `grok --no-leader --version`. It makes NO model call and costs NOTHING. The
        two outcomes were both measured on this host, so the assertion has a known
        positive AND a known negative:

            grok --no-leader --version          -> rc 0, prints the version
            grok --definitely-not-a-flag ...    -> rc 2, "error: unexpected argument"

        Both conditions are checked — a zero exit AND the absence of the rejection
        sentence — because a future CLI could plausibly warn-and-continue on an
        unknown flag, which would pass an rc-only test while silently leaving leader
        mode reachable. That is precisely the silent failure this amendment exists to
        prevent, so the assertion does not rest on rc alone.

        Cached per instance after the first success: the fact does not change inside
        one process, and re-running it per job would spend a subprocess per job to
        re-learn a constant.
        """
        if self._preflight_result is not None and not force:
            return self._preflight_result
        if self._preflight_probe is not None:
            result = self._preflight_probe()
            self._preflight_result = result
            return result
        binary = self.executable
        if binary is None:
            result = (False, "the grok binary could not be resolved; nothing to assert against")
            self._preflight_result = result
            return result
        try:
            proc = subprocess.run(
                [binary, NO_LEADER_FLAG, "--version"],
                capture_output=True, text=True, timeout=30, stdin=subprocess.DEVNULL,
            )
        except FileNotFoundError:
            result = (False, f"{binary!r} vanished between resolution and invocation")
            self._preflight_result = result
            return result
        except subprocess.TimeoutExpired:
            result = (False, f"`{binary} {NO_LEADER_FLAG} --version` did not answer in 30s")
            self._preflight_result = result
            return result
        combined = f"{proc.stdout or ''}\n{proc.stderr or ''}"
        rejected = "unexpected argument" in combined
        ok = proc.returncode == 0 and not rejected
        result = (
            ok,
            f"`{NO_LEADER_FLAG}` accepted (rc=0, no rejection sentence): {(proc.stdout or '').strip()[:80]}"
            if ok else
            f"`{NO_LEADER_FLAG}` was NOT accepted (rc={proc.returncode}): "
            f"{combined.strip()[:200]}. Leader mode multiplexes clients onto ONE backend "
            "through `~/.grok/leader.sock` — a concurrency door AROUND the serial lock. "
            "The lane REFUSES TO FIRE rather than firing with an ignored flag.",
        )
        self._preflight_result = result
        return result

    # -- availability -------------------------------------------------------
    def check_auth(self) -> LaneAvailability:
        """`grok models` — the check of record.

        MEASURED (2026-08-24, grok 1.0.5): rc=0, and *"You are logged in with
        grok.com."* on STDOUT. Both streams are read anyway, because the Codex lane
        spent a build reporting a healthy lane as expired by reading only one — that
        defect is cheap to not repeat and expensive to repeat.

        The NEGATIVE branch is REASONED, NOT MEASURED, and this sentence is the record
        of that: producing a real not-logged-in answer requires `grok logout`, a
        Matt-only action on a live lane. It fails CLOSED — non-zero exit, an
        unrecognised answer, or a missing binary all read as "not authenticated".
        Treat it as genuinely untested rather than as covered by symmetry.
        """
        if self._auth_probe is not None:
            return self._auth_probe()
        binary = self.executable
        if binary is None:
            return LaneAvailability(
                False, "cli_missing",
                f"the grok CLI was not found (looked at ${GROK_BINARY_ENV}, then "
                f"{resolve_grok_home() / DEFAULT_GROK_BINARY_RELATIVE}). It is NOT on "
                "PATH by design; this lane resolves it explicitly.",
            )
        try:
            proc = subprocess.run(
                [binary, "models"],
                capture_output=True, text=True, timeout=60, stdin=subprocess.DEVNULL,
            )
        except FileNotFoundError:
            return LaneAvailability(
                False, "cli_missing", f"{binary!r} is not executable from this process",
            )
        except subprocess.TimeoutExpired:
            return LaneAvailability(
                False, "auth_unknown",
                "`grok models` did not answer within 60s. Absence of an answer is not a "
                "pass — the lane is treated as closed.",
            )
        answer = "\n".join(
            part for part in ((proc.stdout or "").strip(), (proc.stderr or "").strip()) if part
        )
        if proc.returncode == 0 and "logged in" in answer.lower():
            return LaneAvailability(True, "open", answer.splitlines()[0][:200])
        return LaneAvailability(
            False, "auth_expired",
            f"Grok auth is not healthy (`grok models` exited {proc.returncode}: "
            f"{answer[:300] or 'no output on either stream'}). THIS IS NOT A JOB FAILURE "
            "AND MUST NOT BE RETRIED: re-authentication is a MATT-ONLY action. The queue "
            "stops taking Grok jobs, files the condition, and hands pending work to the "
            "named Claude curator's lane — idle work is the failure, a filed row plus a "
            "fallback is the success.",
        )

    def availability(self) -> LaneAvailability:
        """Auth first, then the leader assertion, then busy.

        The ORDER is the ruling. An expired lane is not a busy lane, and a lane whose
        concurrency door cannot be proven shut is not an open lane no matter how free
        the lock reads — asserting the flag AFTER the busy probe would let a caller
        see `open` on a lane this harness will then refuse to fire.
        """
        auth = self.check_auth()
        if not auth.ok:
            return auth
        ok, why = self.assert_no_leader_parses()
        if not ok:
            return LaneAvailability(False, "preflight_failed", why)
        if not lane_is_free(self.lock_path):
            return LaneAvailability(
                False, "busy",
                "another `grok` job holds the serial lane. ONE job stream at a time per "
                "credential — SERIAL BY CHOICE on this lane, not by a verified vendor "
                "precondition — queue behind it, take the Codex lane, or fire the named "
                "Claude curator, NEVER parallel on this credential.",
            )
        return LaneAvailability(True, "open", auth.reason)

    def available(self) -> bool:
        """Duck-typed at `workflow.py`, exactly as `CodexHarness.available` is.

        ADVISORY in both directions. The busy half is a PROBE — it acquires the flock
        and releases it — so between this answer and any use of it the lane can change
        hands. The GUARANTEE is `SerialLaneLock` held across the `subprocess.run` call
        in `run()`, and that is the only place the lane is actually reserved.
        """
        return self.availability().ok

    def unavailable_reason(self) -> str:
        state = self.availability()
        return "" if state.ok else f"{state.state}: {state.reason}"

    # -- the fence ----------------------------------------------------------
    @staticmethod
    def validate_tools(tools: object, where: str) -> list[str]:
        """`--tools` EXISTS on this CLI, and this lane still refuses to hold that fence.

        Unlike `codex exec`, `grok` does publish a `--tools` allowlist. It is refused
        here anyway, and the reason is not symmetry with the Codex lane: the tool-name
        vocabulary this CLI accepts has NOT been enumerated on this host, so accepting
        a list would let a workflow declare a fence whose members nobody has verified
        the CLI recognises. A misspelled tool name in an allowlist is the fail-open
        direction — the workflow reads as fenced and the CLI silently ignores a name
        it does not know.

        The posture of record for this lane's job classes is single-turn `-p` with
        `--disable-web-search`, where the tool surface is not the fence in the first
        place. Opening `--tools` is a job-class decision that starts with probing the
        vocabulary, and it is not made by accepting a list today.
        """
        raise ValueError(
            f"{where}: the grok lane does not accept a `tools:` declaration. The CLI has "
            "a `--tools` flag, but its accepted vocabulary has not been enumerated on "
            "this host, so a list here would name a fence whose members nobody verified "
            "the CLI recognises — and an unrecognised member is silently dropped, which "
            "makes the workflow read as fenced while it is not. This lane's declared "
            f"fence is `permission_mode` (from {sorted(PERMISSION_MODES)}) plus "
            "`--disable-web-search`, which is on unless the job class names web access."
        )

    # -- argv ---------------------------------------------------------------
    def build_argv(self, prompt: str, config: dict[str, Any]) -> list[str]:
        """The invocation of record, assembled with every pin SAID rather than assumed."""
        binary = self.executable
        if binary is None:
            raise ValueError(
                f"grok harness: the CLI was not found (looked at ${GROK_BINARY_ENV}, then "
                f"{resolve_grok_home() / DEFAULT_GROK_BINARY_RELATIVE}). This binary is "
                "not on PATH by design."
            )

        model = str(config.get("model", MODEL_PIN))
        effort = str(config.get("reasoning_effort", REASONING_EFFORT_PIN))
        if effort not in REASONING_EFFORTS:
            raise ValueError(
                f"grok harness: reasoning_effort {effort!r} is not one of "
                f"{sorted(REASONING_EFFORTS)} — the vocabulary the CLI itself enumerates "
                "in its rejection message. A value outside it buys a refused invocation "
                "at the vendor instead of a refused one here."
            )
        if (model, effort) != (MODEL_PIN, REASONING_EFFORT_PIN):
            if not str(config.get("model_ab_note", "")).strip():
                raise ValueError(
                    f"grok harness: config asks for model={model!r} effort={effort!r}, "
                    f"which is not the pin ({MODEL_PIN!r} @ {REASONING_EFFORT_PIN!r}). "
                    "This pin is DECLARED, not banked — the first 10 jobs ARE the banking "
                    "window (Amendment I) — which makes an unannounced swap WORSE than it "
                    "would be on a banked lane, not better: it corrupts the baseline while "
                    "the baseline is being measured. Name the A/B note in `model_ab_note` "
                    "and this refusal lifts."
                )

        permission_mode = str(config.get("permission_mode", DEFAULT_PERMISSION_MODE))
        if permission_mode in FORBIDDEN_PERMISSION_MODES:
            raise ValueError(
                f"grok harness: permission mode {permission_mode!r} is REFUSED BY NAME on "
                "this lane. `bypassPermissions` removes the fence and `dontAsk` "
                "auto-answers it; either one leaves a research lane with no pre-hoc "
                f"containment at all. Declare one of {sorted(PERMISSION_MODES)}."
            )
        if permission_mode not in PERMISSION_MODES:
            raise ValueError(
                f"grok harness: permission mode {permission_mode!r} is not one of "
                f"{sorted(PERMISSION_MODES)}. The fence is declared per job class, never "
                "guessed — a typo here would be passed to the CLI and adjudicated by "
                "nothing."
            )

        encoded = len(prompt.encode("utf-8"))
        if encoded > MAX_PROMPT_ARGV_BYTES:
            raise ValueError(
                f"grok harness: the prompt is {encoded} bytes and the argv ceiling "
                f"declared for this lane is {MAX_PROMPT_ARGV_BYTES}. The invocation of "
                "record puts the prompt on argv (`-p`), and `ARG_MAX` is not a limit to "
                "discover as an E2BIG in production. `grok --prompt-file <PATH>` is the "
                "door past this, and taking it is a job-class decision with its own "
                "record."
            )

        argv = [binary, "-p", prompt, "--output-format", "json"]
        # AMENDMENT E: said on EVERY argv, and asserted at preflight. Leader mode is a
        # shared backend multiplexing clients — the concurrency door around the lock.
        argv.append(NO_LEADER_FLAG)
        # H1 on the third vendor: the pin is said ON THE ARGV, not left to
        # `~/.grok/config.toml`, which is ambient host state no file here controls.
        argv += ["-m", model]
        # AMENDMENT D: argv-said from the FIRST job, not merely from a pilot.
        argv += ["--reasoning-effort", effort]
        argv += ["--permission-mode", permission_mode]
        if not config.get("web_search"):
            # The posture of record. Web access is granted only when a job class NAMES
            # it, and the default direction is OFF rather than inherited.
            argv.append("--disable-web-search")
        for rule in config.get("allow", []) or []:
            argv += ["--allow", str(rule)]
        for rule in config.get("deny", []) or []:
            argv += ["--deny", str(rule)]
        if config.get("max_turns"):
            argv += ["--max-turns", str(int(config["max_turns"]))]
        return argv

    # -- run ----------------------------------------------------------------
    def run(self, prompt: str, cwd: Path, config: dict[str, Any]) -> RawResult:
        """One job. THE LOCK IS HELD ACROSS THE `grok` CALL AND NOWHERE ELSE.

        Same enforcement discipline as the Codex lane, for the same structural reason:
        this is the single invocation site, the lock fd is inheritable and passed to
        the child, so lock lifetime is `max(queue, grok)` — a killed queue cannot leave
        a running child on an unlocked lane, and a dead process cannot leave a stale
        lock. `JobQueue.drain` must therefore NOT wrap its loop in the lock.

        NEVER raises for an operational condition. A failed preflight, a closed lane, a
        missing binary, a busy lane and a failed turn all come back as
        `RawResult(ok=False)` with an `error` that says which.
        """
        raw_path = config.get("raw_output_path")
        prompt_path = config.get("prompt_path")
        timeout_s = int(config.get("timeout_s", DEFAULT_TIMEOUT_S))
        output_path = config.get("output_path")

        # AMENDMENT E, at the gate: refuse to fire rather than fire with an ignored
        # flag. Checked BEFORE the lock so a refused lane never takes it.
        preflight_ok, preflight_why = self.assert_no_leader_parses()
        if not preflight_ok:
            return RawResult(
                ok=False, harness=self.name,
                error=f"PREFLIGHT REFUSED (lane spec Amendment E): {preflight_why}",
                usage=UsageBreakdown.absent("harness never launched: preflight assertion failed"),
                extra={"lane_state": "preflight_failed"},
            )

        try:
            argv = self.build_argv(prompt, config)
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
                    input="",
                    capture_output=True,
                    text=True,
                    timeout=timeout_s,
                    # THE CRASH-SAFETY LINE, identical to the Codex lane's.
                    pass_fds=(lock.fd,),
                )
            except FileNotFoundError:
                return RawResult(
                    ok=False, harness=self.name,
                    error=f"{argv[0]} not found at invocation time",
                    usage=UsageBreakdown.absent("harness never launched"),
                )
            except subprocess.TimeoutExpired:
                return RawResult(
                    ok=False, harness=self.name,
                    error=f"grok exceeded {timeout_s}s and was killed",
                    usage=UsageBreakdown.absent("harness killed on timeout; no envelope"),
                )
        finally:
            lock.release()
        elapsed_ms = int((time.monotonic() - started) * 1000)

        if raw_path:
            Path(raw_path).parent.mkdir(parents=True, exist_ok=True)
            Path(raw_path).write_text(proc.stdout or "", encoding="utf-8")
            Path(str(raw_path) + ".stderr").write_text(proc.stderr or "", encoding="utf-8")
        if prompt_path:
            Path(prompt_path).parent.mkdir(parents=True, exist_ok=True)
            Path(prompt_path).write_text(prompt, encoding="utf-8")

        return self.adjudicate(
            proc.stdout or "",
            returncode=proc.returncode,
            elapsed_ms=elapsed_ms,
            raw_path=raw_path,
            prompt_path=str(prompt_path) if prompt_path else None,
            output_path=str(output_path) if output_path else None,
            model=str(config.get("model", MODEL_PIN)),
            effort=str(config.get("reasoning_effort", REASONING_EFFORT_PIN)),
            stderr=proc.stderr or "",
        )

    # -- adjudication -------------------------------------------------------
    def adjudicate(
        self,
        stdout: str,
        *,
        returncode: int,
        elapsed_ms: int = 0,
        raw_path: str | None = None,
        prompt_path: str | None = None,
        output_path: str | None = None,
        model: str = MODEL_PIN,
        effort: str = REASONING_EFFORT_PIN,
        stderr: str = "",
    ) -> RawResult:
        """Turn the JSON envelope into a verdict. Separated from `run` so it is TESTABLE.

        The absence of a parseable envelope IS the failure signal on this lane, exactly
        as a missing `turn.completed` is on the Codex lane and a missing `result` frame
        is on the Claude lane.
        """
        envelope = parse_envelope(stdout)
        extra: dict[str, Any] = {
            "elapsed_ms": elapsed_ms,
            "stderr_bytes": len(stderr),
            "reasoning_effort": effort,
            "declared_model": model,
        }

        if envelope is None:
            return RawResult(
                ok=False, harness=self.name, model=model, exit_code=returncode,
                raw_output_path=raw_path, prompt_path=prompt_path,
                error=(
                    f"no parseable JSON envelope on stdout (exit {returncode}). On this "
                    "lane that absence IS the failure signal: "
                    f"{(stderr.strip()[-300:] or 'no stderr')}"
                ),
                usage=UsageBreakdown.absent("grok emitted no parseable JSON envelope"),
                extra=extra,
            )

        # AMENDMENT C: the RESOLVED model id, captured per call from the envelope's own
        # `modelUsage` keys. `grok-4.6` is known to resolve to `grok-4.6-build`; if that
        # ever changes at an unchanged declared pin, this field is where it becomes
        # visible instead of silent.
        resolved = resolved_model_ids(envelope)
        extra["resolved_model_ids"] = resolved
        extra["resolved_model"] = resolved[0] if resolved else None
        extra["model_resolution_captured"] = bool(resolved)
        extra["stop_reason"] = envelope.get("stopReason")
        extra["num_turns"] = envelope.get("num_turns")
        extra["session_id"] = envelope.get("sessionId")
        extra["request_id"] = envelope.get("requestId")

        usage = UsageBreakdown.from_grok_envelope(envelope)
        text = str(envelope.get("text") or "")

        ok = returncode == 0 and envelope.get("stopReason") not in ("error", "refusal")
        missing_output = bool(ok and output_path and not Path(output_path).exists())
        if missing_output:
            ok = False
        return RawResult(
            ok=ok,
            text=text,
            usage=usage,
            harness=self.name,
            harness_session_id=envelope.get("sessionId"),
            model=model,
            exit_code=returncode,
            raw_output_path=raw_path,
            prompt_path=prompt_path,
            error=(
                None if ok
                else f"the turn completed but the declared output {output_path!r} was never written"
                if missing_output
                else f"grok exited {returncode} (stopReason={envelope.get('stopReason')!r})"
            ),
            extra={**extra, "output_path": output_path},
        )


def parse_envelope(stdout: str) -> dict[str, Any] | None:
    """Parse `grok -p --output-format json`. One JSON object; None if there is not one.

    Tolerant in ONE direction only: the object may be preceded or followed by noise
    (a progress line, a warning), so the parser looks for the outermost JSON object
    rather than demanding that stdout be exactly one document. It does NOT guess at a
    partial object — an unparseable stream returns None, and None is the failure
    signal the adjudicator acts on.
    """
    text = (stdout or "").strip()
    if not text:
        return None
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end <= start:
        return None
    try:
        parsed = json.loads(text[start:end + 1])
    except json.JSONDecodeError:
        return None
    return parsed if isinstance(parsed, dict) else None


def resolved_model_ids(envelope: dict[str, Any]) -> list[str]:
    """AMENDMENT C's field: the model ids the VENDOR actually billed, from `modelUsage`.

    Returns a LIST, not a string. A multi-model turn (a subagent, a router) would
    produce more than one key, and collapsing that to "the first one" would record a
    fact that is not the whole fact. The adjudicator publishes both the list and a
    convenience first element, and the list is the record.
    """
    usage = envelope.get("modelUsage")
    if not isinstance(usage, dict):
        return []
    return sorted(str(key) for key in usage)


HARNESS = register_harness(GrokHarness())
