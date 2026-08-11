"""The runner — phases in order, gates after each, receipts throughout.

Spec A § 2/4/7/8 stitched together. The order inside one attempt is fixed and
load-bearing:

    fingerprint(before) -> execute -> fingerprint(after) -> permissions verdict
    -> gates -> phase verdict

Permissions come BEFORE gates so that a phase which wrote outside its allowlist
aborts the run without its gates ever having a chance to green it. Gates come
before the phase verdict because gates can only downgrade.
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import permissions as perm
from .envelope import EnvelopeBase, EnvelopeError, envelope_prompt_block, extract_envelope
from .gates import GateReport, RunContext, run_gate
from .harness import get_harness
from .phase import FAILED, PASS, Phase
from .receipts import Receipts
from .usage import UsageBreakdown
from .workflow import PhaseSpec, Workflow

DEFAULT_DB = "receipts.db"
DEFAULT_SESSIONS = "sessions"


@dataclass
class PhaseOutcome:
    name: str
    status: str
    gate_reports: list[GateReport] = field(default_factory=list)
    envelope: EnvelopeBase | None = None
    attempts: int = 1
    usage: UsageBreakdown = field(default_factory=lambda: UsageBreakdown.absent("not run"))
    error: str | None = None


@dataclass
class RunResult:
    run_id: str
    status: str                     # PASS | FAIL | ABORTED
    session_dir: Path
    outcomes: list[PhaseOutcome] = field(default_factory=list)
    abort_reason: str | None = None

    @property
    def is_green(self) -> bool:
        return self.status == PASS


CO_TENANCY_NOTE = (
    "These paths are side effects other processes on this host produce merely by "
    "READING. A SQLite reader creates -wal/-shm sidecars that outlive it; an editor "
    "or language server writes caches. The factory measures the TREE, not its own "
    "actions, so another agent's read of an engine DB is indistinguishable from this "
    "phase writing there — and it aborts the run either way. That is fail-closed and "
    "correct, but the diagnosis matters: check whether anything else on this host "
    "touched the read-only tree during the run before treating this as a phase defect."
)

_CO_TENANCY_SUFFIXES = ("-wal", "-shm", "-journal", ".lock", "~")
_CO_TENANCY_NAMES = (".DS_Store",)


def _co_tenancy_suspects(breaches: list) -> list[str]:
    """Breaching paths that another process's mere READ could have created.

    Not an exemption — every one of these still breaches and still aborts. This
    only labels them, because the failure mode found in Gate-2 re-review (G3) is an
    abort that reads as a containment defect when it is a co-tenancy problem, and a
    misdiagnosis on a 10-agent host costs more than the abort does.
    """
    suspects = []
    for breach in breaches:
        name = Path(breach.change.path).name
        if name in _CO_TENANCY_NAMES or any(name.endswith(s) for s in _CO_TENANCY_SUFFIXES):
            suspects.append(f"{breach.change.root.name}:{breach.change.path}")
    return suspects


def new_run_id(workflow_name: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{workflow_name}-{stamp}-{uuid.uuid4().hex[:6]}"


class Runner:
    def __init__(
        self,
        workflow: Workflow,
        factory_dir: Path | None = None,
        run_id: str | None = None,
        verbose: bool = True,
    ):
        self.wf = workflow
        self.factory_dir = Path(factory_dir or Path(__file__).parent)
        self.run_id = run_id or new_run_id(workflow.name)
        self.session_dir = self.factory_dir / DEFAULT_SESSIONS / self.run_id
        self.db_path = self.factory_dir / DEFAULT_DB
        self.verbose = verbose
        self.receipts = Receipts(self.db_path)
        # phase_id -> caveats already emitted, so the same region is not re-declared
        # at every snapshot within one phase
        self._coarse_said: dict[int | None, set[str]] = {}

    # -- logging -----------------------------------------------------------
    def _say(self, line: str) -> None:
        if self.verbose:
            print(line, flush=True)

    # -- entry point -------------------------------------------------------
    def run(self) -> RunResult:
        self.session_dir.mkdir(parents=True, exist_ok=True)
        for sub in ("context_handoff", "prompts"):
            (self.session_dir / sub).mkdir(exist_ok=True)
        self.receipts.start_session(
            self.run_id,
            self.wf.name,
            self.wf.root,
            self.session_dir,
            workflow_path=str(self.wf.path),
            workflow_sha256=self.wf.sha256,
        )
        (self.session_dir / "workflow.snapshot").write_text(
            self.wf.path.read_text(encoding="utf-8"), encoding="utf-8"
        )
        self._say(f"run {self.run_id}  ({self.wf.name}, {len(self.wf.phases)} phases)")

        result = RunResult(run_id=self.run_id, status=PASS, session_dir=self.session_dir)
        carried_notes = ""

        for idx, spec in enumerate(self.wf.phases):
            outcome, abort_reason = self._run_phase(idx, spec, carried_notes)
            result.outcomes.append(outcome)
            if abort_reason:
                result.status = "ABORTED"
                result.abort_reason = abort_reason
                self.receipts.finish_session(self.run_id, "ABORTED", abort_reason)
                self._say(f"ABORTED: {abort_reason}")
                self._write_run_summary(result)
                return result
            if outcome.envelope is not None:
                carried_notes = self._label_notes(outcome)
            if outcome.status != PASS:
                result.status = "FAIL"
                if self.wf.on_fail == "stop":
                    self._say(f"stopping: phase {spec.name} is {outcome.status}")
                    break

        self.receipts.finish_session(self.run_id, result.status)
        self._write_run_summary(result)
        self._say(f"run {self.run_id} -> {result.status}")
        return result

    @staticmethod
    def _label_notes(outcome: PhaseOutcome) -> str:
        """Notes travel forward. Their VERDICT must travel with them (D-7).

        `notes_for_next_agent` from a phase that went red reads identically to notes
        from a phase that passed — same field, same prose, same confident tone. The
        next agent would inherit a failed phase's conclusions as though they were
        established. Only-failures-travel governs OUTPUT; this governs the handoff
        prose, which travels either way.
        """
        notes = outcome.envelope.notes_for_next_agent if outcome.envelope else ""
        if not notes.strip() or outcome.status == PASS:
            return notes
        return (
            f"[carried from phase `{outcome.name}`, which ended {outcome.status} — "
            "these notes were written by an agent whose own work did not pass its "
            "gates. Treat them as a lead, not as an established result.]\n"
            f"{notes}"
        )

    # -- fingerprinting ----------------------------------------------------
    def _fingerprint_all(self) -> dict[str, perm.TreeFingerprint]:
        """Snapshot every declared tree. The root repo alone gets the factory exemptions."""
        root = self.wf.root.resolve()
        return {
            str(r): perm.fingerprint(r, is_root_repo=Path(r).resolve() == root)
            for r in self.wf.repos
        }

    def _diff_all(
        self, before: dict[str, perm.TreeFingerprint], after: dict[str, perm.TreeFingerprint]
    ) -> list[perm.Change]:
        """Diff every tree. An unmeasurable tree raises rather than reading as clean."""
        changes: list[perm.Change] = []
        for key, fp_before in before.items():
            changes += perm.diff_fingerprints(fp_before, after[key])
        return changes

    def _note_coarse(
        self, fingerprints: dict[str, perm.TreeFingerprint], phase_id: int | None, when: str
    ) -> None:
        """A region measured coarsely is DECLARED as coarse, never reported as exact.

        Coarse means directory mtimes: creation, deletion and rename are caught; an
        in-place rewrite of an existing file is not. The receipt says so on every
        phase, so a later reading of "the read-only tree was clean" carries the
        strength of the claim with it.

        Called on EVERY snapshot, not just the phase-start one. A region can cross the
        cap during the phase — the very case where a phase wrote enough to change how
        well it can be measured — and emitting only from `before` would have described
        a diff by half its inputs (Gate-2 re-review G4). Identical caveats within a
        phase are emitted once; a NEW region appearing later is its own line.
        """
        for key, fp in fingerprints.items():
            if not fp.coarse:
                continue
            detail = (
                f"{Path(key).name} measured COARSELY (directory mtimes; in-place "
                f"content edits not detected) in region(s): {fp.coarse}"
            )
            if detail in self._coarse_said.get(phase_id, set()):
                continue
            self._coarse_said.setdefault(phase_id, set()).add(detail)
            self.receipts.event(self.run_id, "containment_coarse", f"{when}: {detail}", phase_id)
            self._say(f"   containment: coarse — {detail}")

    # -- one phase ---------------------------------------------------------
    def _run_phase(
        self, idx: int, spec: PhaseSpec, carried_notes: str
    ) -> tuple[PhaseOutcome, str | None]:
        phase_dir = self.session_dir / spec.name
        phase_dir.mkdir(parents=True, exist_ok=True)
        self._say(f"\n-- phase {idx + 1}/{len(self.wf.phases)}: {spec.name}"
                  f" [{spec.agent or 'mechanical'}]")

        abort_reason: str | None = None
        total_usage = UsageBreakdown.absent(
            "mechanical phase — no model invoked" if spec.is_mechanical else "no attempt recorded"
        )
        outcome = PhaseOutcome(name=spec.name, status=FAILED)
        failures_context = ""

        with Phase(
            name=spec.name,
            agent=spec.agent,
            harness=spec.harness if not spec.is_mechanical else None,
            receipts=self.receipts,
            run_id=self.run_id,
            idx=idx,
        ) as phase:
            for attempt in range(1, spec.retries + 2):
                phase.attempts = attempt
                if attempt > 1:
                    backoff = 2 ** (attempt - 1)
                    self._say(f"   retry {attempt - 1}/{spec.retries} after {backoff}s backoff")
                    self.receipts.event(
                        self.run_id, "retry", f"{spec.name} attempt {attempt}", phase.phase_id
                    )
                    time.sleep(backoff)

                try:
                    before = self._fingerprint_all()
                except perm.ContainmentError as exc:
                    abort_reason = self._handle_containment_failure(phase, exc, "phase start")
                    break
                self._note_coarse(before, phase.phase_id, "phase start")

                envelope, attempt_usage, exec_error = self._execute(
                    spec, phase, attempt, phase_dir, carried_notes, failures_context
                )
                total_usage = (
                    attempt_usage if attempt == 1 else total_usage.merge(attempt_usage)
                )
                phase.usage = total_usage

                try:
                    after = self._fingerprint_all()
                    self._note_coarse(after, phase.phase_id, "post-execution")
                    changes = self._diff_all(before, after)
                except perm.ContainmentError as exc:
                    abort_reason = self._handle_containment_failure(
                        phase, exc, "post-execution"
                    )
                    break
                allowed, breaches = perm.classify(
                    changes,
                    spec.writes,
                    self.wf.root,
                    read_only_trees=self.wf.read_only_trees,
                )
                if breaches:
                    abort_reason = self._handle_breach(spec, phase, breaches, before)
                    break

                if envelope is None:
                    self.receipts.record_envelope(
                        self.run_id, phase.phase_id, None, attempt,
                        parse_error=exec_error or "no envelope produced",
                    )
                    failures_context = exec_error or "no envelope produced"
                    self._say(f"   no usable envelope: {failures_context}")
                    if attempt <= spec.retries:
                        continue
                    break

                (phase_dir / "envelope.json").write_text(envelope.to_json(), encoding="utf-8")
                (self.session_dir / "context_handoff" / f"{idx:02d}-{spec.name}.json").write_text(
                    envelope.to_json(), encoding="utf-8"
                )
                self.receipts.record_envelope(
                    self.run_id, phase.phase_id, envelope, attempt,
                    raw_path=str(phase_dir / "envelope.json"),
                )

                reports = self._run_gates(spec, envelope, allowed + [b.change for b in breaches])

                # Second fingerprint pass. Mechanical cells do their work INSIDE a
                # gate command (tests_pass / command_succeeds), so a write made by
                # the command itself lands after the post-execution snapshot. One
                # check would let a gate's own writes escape containment.
                try:
                    post_gate = self._fingerprint_all()
                    self._note_coarse(post_gate, phase.phase_id, "post-gate")
                    gate_changes = self._diff_all(before, post_gate)
                except perm.ContainmentError as exc:
                    for report in reports:
                        self.receipts.record_gate(self.run_id, phase.phase_id, report, attempt)
                    outcome.gate_reports = reports
                    outcome.envelope = envelope
                    abort_reason = self._handle_containment_failure(
                        phase, exc, "gate execution"
                    )
                    break
                _, gate_breaches = perm.classify(
                    gate_changes,
                    spec.writes,
                    self.wf.root,
                    read_only_trees=self.wf.read_only_trees,
                )
                if gate_breaches:
                    for report in reports:
                        self.receipts.record_gate(self.run_id, phase.phase_id, report, attempt)
                    outcome.gate_reports = reports
                    outcome.envelope = envelope
                    abort_reason = self._handle_breach(
                        spec, phase, gate_breaches, before, during="gate execution"
                    )
                    break

                for report in reports:
                    self.receipts.record_gate(self.run_id, phase.phase_id, report, attempt)
                    self._say("   " + report.one_line())
                outcome.gate_reports = reports
                outcome.envelope = envelope

                if all(r.is_green for r in reports):
                    if not phase.finished:
                        phase.finish_with_envelope(envelope)
                    break

                failures_context = _failures_digest(reports)
                if attempt <= spec.retries and not spec.is_mechanical:
                    continue
                if not phase.finished:
                    phase.finish_with_envelope(envelope)
                break

            if outcome.gate_reports:
                phase.apply_gate_verdicts(outcome.gate_reports)

        outcome.status = phase.status
        outcome.attempts = phase.attempts
        outcome.usage = phase.usage
        outcome.error = phase.error
        self._say(f"   phase {spec.name} -> {phase.status}   {phase.usage.one_line()}")
        return outcome, abort_reason

    # -- execution ---------------------------------------------------------
    def _execute(
        self,
        spec: PhaseSpec,
        phase: Phase,
        attempt: int,
        phase_dir: Path,
        carried_notes: str,
        failures_context: str,
    ) -> tuple[EnvelopeBase | None, UsageBreakdown, str | None]:
        if spec.is_mechanical:
            # The mechanical cell's claim, stated so the gates have something to
            # adjudicate. The claim is never self-verifying: gates read the disk.
            envelope = EnvelopeBase(
                status="PASS",
                summary=spec.claim or f"mechanical cell {spec.name}: claim under gate adjudication",
                artifacts=list(spec.artifacts),
                notes_for_next_agent=spec.notes,
            )
            return envelope, UsageBreakdown.absent("mechanical phase — no model invoked"), None

        prompt = self._build_prompt(spec, carried_notes, failures_context)
        prompt_path = self.session_dir / "prompts" / f"{spec.name}.attempt{attempt}.txt"
        prompt_path.write_text(prompt, encoding="utf-8")
        raw_path = phase_dir / f"raw_output.attempt{attempt}.jsonl"

        started = _now()
        harness = get_harness(spec.harness)
        result = harness.run(
            prompt,
            self.wf.root,
            {
                "agent": spec.agent,
                "tools": spec.tools,
                "timeout_s": spec.timeout_s,
                "raw_output_path": str(raw_path),
            },
        )
        self.receipts.record_agent_session(
            self.run_id,
            phase.phase_id,
            spec.agent or "",
            spec.harness,
            attempt,
            result.harness_session_id,
            result.model,
            str(prompt_path),
            result.raw_output_path,
            started,
        )
        if not result.ok:
            return None, result.usage, result.error or "harness reported failure"
        try:
            return extract_envelope(result.text), result.usage, None
        except EnvelopeError as exc:
            return None, result.usage, str(exc)

    def _build_prompt(self, spec: PhaseSpec, carried_notes: str, failures_context: str) -> str:
        parts = [spec.prompt or ""]
        if carried_notes:
            parts.append(f"\n## Notes from the previous phase\n\n{carried_notes}\n")
        if failures_context:
            # Only failures travel. A passing suite never enters a prompt.
            parts.append(
                "\n## What went red last attempt (failures only)\n\n" + failures_context + "\n"
            )
        if spec.writes:
            parts.append(
                "\n## Write allowlist (enforced by fingerprint, not by trust)\n\n"
                + "\n".join(f"- {w}" for w in spec.writes)
                + "\n\nA write outside this list aborts the run.\n"
            )
        parts.append("\n" + envelope_prompt_block())
        return "\n".join(p for p in parts if p)

    # -- gates -------------------------------------------------------------
    def _run_gates(
        self, spec: PhaseSpec, envelope: EnvelopeBase, changes: list[perm.Change]
    ) -> list[GateReport]:
        ctx = RunContext(
            run_id=self.run_id,
            root=self.wf.root,
            session_dir=self.session_dir,
            phase_name=spec.name,
            repos=list(self.wf.repos),
            changed_paths=[c.path for c in changes],
            extra={"search_trees": list(self.wf.read_only_trees)},
        )
        reports: list[GateReport] = []
        for gspec in spec.gates:
            ctx.prior_reports = list(reports)
            reports.append(run_gate(gspec.gate, envelope, ctx, **gspec.args))
        return reports

    # -- containment failure -----------------------------------------------
    def _handle_containment_failure(
        self, phase: Phase, exc: perm.ContainmentError, during: str
    ) -> str:
        """A tree we cannot measure stops the run. Unknown is not clean (Gate-2 F2)."""
        reason = f"containment failure during {during}: {exc}"
        self._say(f"   CONTAINMENT FAILURE during {during} — {exc}")
        self.receipts.event(self.run_id, "containment_failure", reason, phase.phase_id)
        phase.error = reason
        phase.status = FAILED
        return reason

    # -- breach ------------------------------------------------------------
    def _handle_breach(
        self,
        spec: PhaseSpec,
        phase: Phase,
        breaches: list[perm.Breach],
        before: dict[str, perm.TreeFingerprint],
        during: str = "phase execution",
    ) -> str:
        quarantine = self.session_dir / "breach" / spec.name
        listing = [f"{b.change.path} ({b.change.kind}) — {b.reason}" for b in breaches]
        self._say(f"   PERMISSIONS BREACH during {during}"
                  " — aborting the run (a breach is evidence, not a retry)")
        for line in listing:
            self._say("     " + line)
        self.receipts.event(
            self.run_id, "permissions_breach", json.dumps(listing), phase.phase_id
        )
        actions = perm.rollback(breaches, before, quarantine)
        for action in actions:
            self.receipts.event(
                self.run_id,
                "rollback",
                f"{action.path}: {action.action} — {action.reason}",
                phase.phase_id,
            )
            self._say(f"     rollback: {action.path} -> {action.action}")
        co_tenancy = _co_tenancy_suspects(breaches)
        if co_tenancy:
            self.receipts.event(
                self.run_id, "co_tenancy_suspected", json.dumps(co_tenancy), phase.phase_id
            )
            self._say(f"     NOTE: {len(co_tenancy)} breaching path(s) look like another "
                      "process on this host, not this phase — see BREACH.json")
        (quarantine / "BREACH.json").parent.mkdir(parents=True, exist_ok=True)
        (quarantine / "BREACH.json").write_text(
            json.dumps(
                {
                    "phase": spec.name,
                    "detected_during": during,
                    "writes_allowlist": spec.writes,
                    "breaches": listing,
                    "rollback": [a.__dict__ for a in actions],
                    "co_tenancy_suspects": co_tenancy,
                    "co_tenancy_note": CO_TENANCY_NOTE if co_tenancy else None,
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        phase.error = (
            f"permissions breach during {during}: "
            f"{len(breaches)} path(s) outside the allowlist"
            + (f" — {len(co_tenancy)} of them look like host co-tenancy, not this phase"
               if co_tenancy else "")
        )
        phase.status = FAILED
        return phase.error

    # -- summary -----------------------------------------------------------
    def _write_run_summary(self, result: RunResult) -> None:
        from .report import render_run_report  # local import: report reads receipts

        text = render_run_report(self.receipts, self.run_id)
        (self.session_dir / "run_report.md").write_text(text, encoding="utf-8")

    def close(self) -> None:
        self.receipts.close()


def _failures_digest(reports: list[GateReport]) -> str:
    lines: list[str] = []
    for r in reports:
        if r.is_green:
            continue
        lines.append(f"- {r.gate}: {r.status} — {r.detail}")
        failures = r.evidence.get("failures")
        if isinstance(failures, list):
            lines += [f"    {ln}" for ln in failures[:20]]
        for key in ("missing", "empty", "absent", "broken", "unclaimed", "problems"):
            if r.evidence.get(key):
                lines.append(f"    {key}: {r.evidence[key]}")
    return "\n".join(lines)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
