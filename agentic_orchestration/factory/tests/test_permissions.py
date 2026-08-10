"""Permissions fingerprinting — Spec A § 8 and § 11 acceptance item 4 (second half).

The centrepiece is `test_planted_write_outside_the_allowlist_aborts_and_rolls_back`:
a phase writes a file it never declared, and the run must ABORT (not retry), the
bytes must be quarantined, and the tree must come back clean.

The rest are the safety rules that keep the containment from becoming its own
accident: pre-existing dirt is never restored over, committed paths are never
unwound, protected paths cannot be opted into by config.
"""

import json
import subprocess
from pathlib import Path

import pytest

from factory import permissions as perm
from factory.runner import Runner
from factory.workflow import load_workflow


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _write_workflow(tmp_path: Path, repo: Path, phase: dict) -> Path:
    doc = {
        "name": "breachtest",
        "root": str(repo),
        "repos": [str(repo)],
        "phases": [phase],
    }
    path = tmp_path / "wf.json"
    path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    return path


def _run(tmp_path: Path, repo: Path, phase: dict):
    wf = load_workflow(_write_workflow(tmp_path, repo, phase))
    runner = Runner(wf, factory_dir=tmp_path / "factory_home", verbose=False)
    try:
        return runner.run()
    finally:
        runner.close()


def _sh(command: str) -> dict:
    return {"gate": "command_succeeds", "args": {"command": f"sh -c '{command}'"}}


# ---------------------------------------------------------------------------
# the acceptance test
# ---------------------------------------------------------------------------
def test_planted_write_outside_the_allowlist_aborts_and_rolls_back(tmp_path, git_repo):
    result = _run(
        tmp_path,
        git_repo,
        {
            "name": "sneaky",
            "writes": ["allowed/**"],
            "retries": 1,  # a breach must NOT consume this
            "artifacts": ["allowed/declared.txt"],
            "gates": [_sh("mkdir -p allowed && echo ok > allowed/declared.txt && "
                          "echo gotcha > not_declared.txt")],
        },
    )

    assert result.status == "ABORTED", f"expected ABORTED, got {result.status}"
    assert "permissions breach" in (result.abort_reason or "")

    # the undeclared write is gone from the tree
    assert not (git_repo / "not_declared.txt").exists(), (
        "the breaching file survived rollback"
    )
    # ...but its bytes were kept as evidence before deletion
    quarantined = list((result.session_dir / "breach").rglob("not_declared.txt"))
    assert quarantined, "breaching bytes were deleted without being quarantined"
    assert quarantined[0].read_text().strip() == "gotcha"

    breach_json = list((result.session_dir / "breach").rglob("BREACH.json"))
    assert breach_json, "no BREACH.json written"
    record = json.loads(breach_json[0].read_text())
    assert record["writes_allowlist"] == ["allowed/**"]
    assert any("not_declared.txt" in b for b in record["breaches"])


def test_a_breach_is_never_retried(tmp_path, git_repo):
    result = _run(
        tmp_path,
        git_repo,
        {
            "name": "sneaky",
            "writes": ["allowed/**"],
            "retries": 3,
            "gates": [_sh("echo gotcha > not_declared.txt")],
        },
    )
    assert result.status == "ABORTED"
    assert result.outcomes[0].attempts == 1, (
        "a permissions breach consumed a retry — a breach is evidence, not a retry"
    )


def test_a_declared_write_does_not_abort(tmp_path, git_repo):
    """The falsification partner: the same machinery must let a legal write through."""
    result = _run(
        tmp_path,
        git_repo,
        {
            "name": "tidy",
            "writes": ["allowed/**"],
            "artifacts": ["allowed/declared.txt"],
            "gates": [
                _sh("mkdir -p allowed && echo ok > allowed/declared.txt"),
                "artifacts_exist",
                "files_non_empty",
            ],
        },
    )
    assert result.status == "PASS", f"legal write was blocked: {result.abort_reason}"
    assert (git_repo / "allowed" / "declared.txt").exists()


# ---------------------------------------------------------------------------
# classify — the rules that cannot be configured away
# ---------------------------------------------------------------------------
def _change(root: Path, path: str, kind: str = "created") -> perm.Change:
    return perm.Change(root=root, path=path, kind=kind, before_status=None, after_status="??")


@pytest.mark.parametrize(
    "path",
    ["agentic_orchestration/factory/gates/core.py", "canonical/00-ground-state.md",
     ".claude/settings.json"],
)
def test_protected_paths_breach_even_when_the_allowlist_names_them(tmp_path, path):
    root = tmp_path
    allowed, breaches = perm.classify([_change(root, path)], writes=["**"], root=root)
    assert not allowed
    assert len(breaches) == 1
    assert "always-protected" in breaches[0].reason


def test_write_inside_a_read_only_tree_is_a_breach(tmp_path):
    root = tmp_path / "meta"
    engine = tmp_path / "engine"
    root.mkdir()
    engine.mkdir()
    allowed, breaches = perm.classify(
        [_change(engine, "src/whatever.py")],
        writes=["**"],
        root=root,
        read_only_trees=[engine],
    )
    assert not allowed
    assert "read-only tree" in breaches[0].reason


def test_allowlist_accepts_directory_prefixes_and_globs(tmp_path):
    root = tmp_path
    changes = [
        _change(root, "out/season/001.json"),
        _change(root, "notes/x.md"),
    ]
    allowed, breaches = perm.classify(changes, writes=["out/", "notes/*.md"], root=root)
    assert len(allowed) == 2
    assert not breaches


# ---------------------------------------------------------------------------
# rollback safety
# ---------------------------------------------------------------------------
def test_rollback_never_restores_over_pre_existing_dirt(tmp_path, git_repo):
    """A path already dirty at phase start is baseline, not the phase's doing."""
    (git_repo / "tracked.txt").write_text("edited by the human, before the phase\n")
    before = {str(git_repo): perm.fingerprint(git_repo)}
    assert "tracked.txt" in before[str(git_repo)].entries

    breach = perm.Breach(
        _change(git_repo, "tracked.txt", kind="modified"), "outside the allowlist"
    )
    actions = perm.rollback([breach], before, tmp_path / "q")

    assert actions[0].action == "NOT_ROLLED_BACK"
    assert "already dirty" in actions[0].reason
    assert (git_repo / "tracked.txt").read_text().startswith("edited by the human")
    assert actions[0].quarantined_to, "evidence should still have been quarantined"


def test_rollback_will_not_unwind_a_commit(tmp_path, git_repo):
    before = {str(git_repo): perm.fingerprint(git_repo)}
    breach = perm.Breach(_change(git_repo, "tracked.txt", kind="committed"), "committed")
    actions = perm.rollback([breach], before, tmp_path / "q")
    assert actions[0].action == "NOT_ROLLED_BACK"
    assert "human decision" in actions[0].reason


def test_rollback_deletes_only_what_the_phase_created(tmp_path, git_repo):
    before = {str(git_repo): perm.fingerprint(git_repo)}
    (git_repo / "new.txt").write_text("phase output\n")
    breach = perm.Breach(_change(git_repo, "new.txt", kind="created"), "outside the allowlist")
    actions = perm.rollback([breach], before, tmp_path / "q")
    assert actions[0].action == "deleted"
    assert not (git_repo / "new.txt").exists()
    assert Path(actions[0].quarantined_to).read_text() == "phase output\n"


# ---------------------------------------------------------------------------
# fingerprint mechanics
# ---------------------------------------------------------------------------
def test_fingerprint_sees_a_new_file_and_ignores_gitignored_ones(git_repo):
    before = perm.fingerprint(git_repo)
    (git_repo / "visible.txt").write_text("x\n")
    (git_repo / "ignored").mkdir()
    (git_repo / "ignored" / "noise.txt").write_text("y\n")
    after = perm.fingerprint(git_repo)

    paths = {c.path for c in perm.diff_fingerprints(before, after)}
    assert "visible.txt" in paths
    assert not any(p.startswith("ignored") for p in paths), (
        "gitignored writes must not read as tree changes — the factory's own "
        "sessions/ and receipts.db depend on this"
    )


def test_fingerprint_of_a_non_git_directory_is_inert(tmp_path):
    fp = perm.fingerprint(tmp_path)
    assert fp.is_git is False
    assert perm.diff_fingerprints(fp, fp) == []


def test_fingerprint_detects_content_change_in_a_tracked_file(git_repo):
    before = perm.fingerprint(git_repo)
    (git_repo / "tracked.txt").write_text("changed\n")
    after = perm.fingerprint(git_repo)
    changes = perm.diff_fingerprints(before, after)
    assert [c.path for c in changes] == ["tracked.txt"]


def test_fingerprint_detects_a_commit_made_during_the_window(git_repo):
    before = perm.fingerprint(git_repo)
    (git_repo / "sneaky.txt").write_text("committed behind our back\n")
    subprocess.run(["git", "add", "sneaky.txt"], cwd=git_repo, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-q", "-m", "sneak"], cwd=git_repo, check=True, capture_output=True
    )
    after = perm.fingerprint(git_repo)
    changes = perm.diff_fingerprints(before, after)
    assert any(c.kind == "committed" and c.path == "sneaky.txt" for c in changes)
