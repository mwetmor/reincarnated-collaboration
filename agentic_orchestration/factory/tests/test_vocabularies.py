"""Gate-2 JR-20 — which module-level collections need a literal pin, derived over
ALL of them rather than over the four that happened to be under discussion.

Rule 47 asked ONE question — is a member *behaviour* or a *record*? — and got the
right answer for the dict it was written about. jack-ryan measured three survivors
it does not explain: deleting a member of `FACTORY_RUNTIME_PATHS` survives, and
ADDING to `FACTORY_RUNTIME_PATHS` or to `STRUCTURE_SKIP_DIRS` survives. All three
are behaviour collections, which rule 47 says need no pin.

The missing question is WHICH DIRECTION IS FAIL-OPEN.

  * A PROTECTION list fails open when a member is DELETED. Deleting it stops
    something being refused, and a scenario row exercising that member notices,
    because the row's expected verdict flips.
  * An EXEMPTION list fails open when a member is ADDED. Nothing notices, and
    nothing CAN: the row that would catch it has to exercise a path nobody has
    exempted yet, so it could not have been written in advance. Deletion from an
    exemption is fail-CLOSED — the run gets noisier, not blinder — which is why
    rule 44's "delete it" measured the safe direction here and the reading read
    as reassurance.

Crossed with rule 47's own axis:

                | protection (delete = fail-open) | exemption (add = fail-open)
    behaviour   | rows suffice                    | LITERAL REQUIRED
    record      | LITERAL REQUIRED                | LITERAL REQUIRED

One cell of four is covered by rows. Rule 47 generalised from that cell.

The direction is a property of the CALL SITE, not of the collection — JR-18's
lesson arriving again one layer up. `REFUSAL_GUARDS` and `GUARDS_OWING_FACTS` are
two frozensets of guard names declared eight lines apart in the same file, and
they fail open in OPPOSITE directions:

    REFUSAL_GUARDS      spent as `assert action.guard in REFUSAL_GUARDS` — the
                        vocabulary the wall will ACCEPT. Adding a name admits a
                        guard nobody adjudicated. Deleting one reds the wall.
    GUARDS_OWING_FACTS  spent as `if action.guard in GUARDS_OWING_FACTS:` — the
                        gate on an EXTRA assertion. Deleting a name skips that
                        assertion silently. Adding one demands more.

Nothing about their spelling, type, or neighbourhood says which is which. Only
the sentence they are spent in does.

There is a THIRD kind, and naming it is what keeps this from becoming "pin
everything", which would be noise. A LABELLING list changes the DIAGNOSIS and not
the VERDICT: `_CO_TENANCY_SUFFIXES` labels breaches that still breach and still
abort; `_FAILURE_MARKERS` selects which lines of a failing gate's output travel
into the next prompt, while the verdict is the exit code. Getting their
membership wrong costs an operator clarity, not containment. They are not pinned
here, on purpose, and this paragraph is the record of that decision.

THE PIN IS AN EQUALITY, NOT A MEMBERSHIP ASSERT. `==` fails on an addition, on a
deletion, on a reorder that changes a tuple, and on the type degeneration that
broke the round-20 mutator: `("worktrees/", "modules/")` with its first element
deleted textually is `("modules/")`, which is not a 1-tuple but the bare string
`"modules/"` — and `in` reports that string as containing `"modules/"` while `==`
does not. A membership test cannot tell a shorter tuple from a string. That is
the round-21 correction to rule 48, expressed as an instrument choice.
"""

import ast
from pathlib import Path

from factory import envelope as envelope_mod
from factory import permissions as perm
from factory import workflow as workflow_mod
from factory.harness import claude_code as cc

FACTORY_DIR = Path(__file__).resolve().parents[1]

#: The modules whose vocabularies this file adjudicates. Named rather than walked,
#: because a walk over every module would sweep in infrastructure dicts and the
#: resulting table would be long enough that nobody reads it.
ADJUDICATED_MODULES: dict[str, object] = {
    "permissions.py": perm,
    "workflow.py": workflow_mod,
    "envelope.py": envelope_mod,
    "harness/claude_code.py": cc,
}


# ---------------------------------------------------------------------------
# The pins.
# ---------------------------------------------------------------------------

#: Every entry says WHICH DIRECTION it is pinned against, because a pin whose
#: direction is not stated is the state rule 47 was in.
VOCABULARY_PINS: dict[str, object] = {
    # --- exemption: ADDITION is the fail-open direction --------------------
    #: Forgiven in the root repo. The consumer is `rel.startswith(p)`, so adding
    #: `"agentic_orchestration/"` forgives nine agents' trees and adding `""`
    #: forgives everything. Measured by jack-ryan at round 21: member deletion
    #: SURVIVES (no covering row at all) and addition SURVIVES.
    "FACTORY_RUNTIME_PATHS": (
        "agentic_orchestration/factory/sessions/",
        "agentic_orchestration/factory/receipts.db",
        "agentic_orchestration/factory/receipts.db-wal",
        "agentic_orchestration/factory/receipts.db-shm",
        "agentic_orchestration/factory/__pycache__/",
        "agentic_orchestration/factory/.pytest_cache/",
    ),
    #: Pruned from the structural walk. Adding `"src"` makes a whole tree
    #: invisible to the COARSE fingerprint — and the fingerprint still reports
    #: clean, which is a green proof over a tree nobody looked at. Measured by
    #: jack-ryan at round 21: addition SURVIVES.
    "STRUCTURE_SKIP_DIRS": frozenset({".git"}),
    #: The vocabulary the WALL accepts from a refusal; production never reads it.
    #: Adding a name is how a guard enters the closed vocabulary without anyone
    #: adjudicating it, which is rule 13 run backwards.
    "REFUSAL_GUARDS": frozenset({
        "whole_tree", "quarantine_failed", "committed", "dirty_before", "destroyer",
        "delete_failed", "nothing_at_path", "unknown_status", "staging",
        "checkout_failed", "git_internal",
    }),
    #: The grant vocabulary, read off ONE live init frame. Adding a name by hand
    #: admits a tool nobody probed while the module's own comment still says the
    #: set was probed. Extending it is legitimate — re-probe, then update this
    #: literal; that edit IS the act of re-probing, and it must not happen by
    #: accident.
    "BUILTIN_TOOLS": frozenset({
        "Task", "AskUserQuestion", "Bash", "CronCreate", "CronDelete", "CronList",
        "Edit", "EnterPlanMode", "EnterWorktree", "ExitPlanMode", "ExitWorktree",
        "Glob", "Grep", "Monitor", "NotebookEdit", "PushNotification", "Read",
        "RemoteTrigger", "ScheduleWakeup", "Skill", "TaskOutput", "TaskStop",
        "TodoWrite", "ToolSearch", "WebFetch", "WebSearch", "Write",
    }),
    # --- protection with no covering row: DELETION is the fail-open direction -
    #: Deleting a name here skips the `action.facts` assertion for that guard,
    #: silently, and the operator gets prose where they were promised numbers.
    "GUARDS_OWING_FACTS": frozenset({"destroyer", "staging"}),
    #: Spent as `for code in sorted(perm.UNMERGED_CODES)` — a parametrised loop
    #: over the collection under test. Deleting a code deletes the case that
    #: would have caught it, and the suite gets GREENER. Rule 44's exact subject,
    #: in a row that predates rule 44.
    "UNMERGED_CODES": frozenset({"DD", "AU", "UD", "UA", "DU", "AA", "UU"}),
    #: A record of a measurement. Its own comment says "this dict has exactly one
    #: entry until a frame says otherwise" — a claim nothing enforced. The pin is
    #: what makes "until a frame says otherwise" mean something.
    "INVOCATION_ONLY_TOOLS": ("Agent",),  # keys only; the reason is prose, pinned below
}

#: `INVOCATION_ONLY_TOOLS` is a dict; its keys are the record and its values are
#: an argument. Compared as keys above so that re-wording a reason is not a
#: failure here — `REASONED_ADMISSIONS`' digests in test_workflow.py are the
#: mechanism for reason text, and duplicating it would be two pins answering one
#: question badly.
_KEYS_ONLY: frozenset[str] = frozenset({"INVOCATION_ONLY_TOOLS"})

#: The other half of the derivation, stated rather than left to inference: the
#: collections whose members ARE visible to a row, or which already carry a pin,
#: each with the reason named. A claim that something is covered is a claim like
#: any other, and rule 45 says it has to name the thing it is about.
VOCABULARY_COVERED: dict[str, str] = {
    "PROTECTED_ALWAYS":
        "deny arm; deleting a member stops a path being refused and the wall's "
        "protected-path rows flip verdict. REASONED, NOT MEASURED",
    "PROTECTED_EVERY_REPO":
        "measured round 20: member deletion KILLED, 3 failed",
    "GIT_CONTROL_PATHS":
        "measured round 20: member deletion KILLED, 11 failed",
    "GIT_NESTED_GITDIRS":
        "measured round 21 by jack-ryan: `worktrees/` deleted, KILLED, 7 failed. My "
        "own round-20 figure for this row was an artifact — see rule 48",
    "UNFENCEABLE_TOOLS":
        "pinned by the `REFUSED_ROSTER` literal in test_workflow.py (rule 47)",
    "REASONED_ADMISSIONS":
        "pinned by `ADMISSION_REASON_DIGESTS` (rewrite) and by "
        "`set(ADMISSION_DEPENDS_ON) == set(REASONED_ADMISSIONS)` (addition and "
        "deletion) in test_workflow.py",
    "FORBIDDEN_PHASE_KEYS":
        "exercised by test_workflow.py's `{**MINIMAL_PHASE, 'model': ...}` row; "
        "deleting the only member makes that row pass a workflow it must refuse",
    "ENVELOPE_STATUSES":
        "carries an equality assert in test_envelope_triad.py",
}


def _module_vocabularies(relpath: str) -> set[str]:
    """Public UPPERCASE module-level containers, read off the SOURCE.

    By AST rather than by `dir()`, so a name imported into the module is not
    counted as one the module declares — the denominator has to be the set of
    things this file is responsible for, not the set of things visible from it
    (rule 49: establish the denominator before reasoning over the set).
    """
    tree = ast.parse((FACTORY_DIR / relpath).read_text())
    found: set[str] = set()
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = [node.target] if isinstance(node, ast.AnnAssign) else node.targets
        for target in targets:
            if not isinstance(target, ast.Name):
                continue
            if target.id.startswith("_") or not target.id.isupper():
                continue
            value = node.value
            is_container = isinstance(value, (ast.Tuple, ast.List, ast.Set, ast.Dict))
            is_setcall = (isinstance(value, ast.Call)
                          and getattr(value.func, "id", "") in ("frozenset", "set"))
            if is_container or is_setcall:
                found.add(target.id)
    return found


def test_JR20_every_vocabulary_is_either_PINNED_or_NAMES_the_row_that_covers_it():
    """The denominator, established rather than assumed.

    jack-ryan's verdict said "re-derive from all fifteen rather than from four".
    Fifteen is reproducible: it is the count of public UPPERCASE module-level
    containers across the four adjudicated modules, and this row recomputes it
    from source every time rather than trusting the number. A new vocabulary
    added to any of these modules fails here until somebody has said which of the
    two boxes it goes in — which is the structural half of the fix, and the half
    that survives the next collection nobody has written yet.
    """
    declared = set()
    per_module = {}
    for relpath in ADJUDICATED_MODULES:
        names = _module_vocabularies(relpath)
        per_module[relpath] = names
        declared |= names

    classified = set(VOCABULARY_PINS) | set(VOCABULARY_COVERED)

    assert declared == classified, (
        "a module-level vocabulary is not classified, or a classification names "
        "something that no longer exists.\n"
        f"  declared but unclassified: {sorted(declared - classified)}\n"
        f"  classified but not declared: {sorted(classified - declared)}\n"
        f"  by module: { {m: sorted(n) for m, n in per_module.items()} }\n"
        "Every collection is either PINNED to a literal or COVERED by a named row. "
        "The question to answer for a new one is not 'is it important' but 'which "
        "DIRECTION is fail-open' — adding to an exemption and deleting from a "
        "protection are the two that no scenario row catches by accident."
    )
    assert not (set(VOCABULARY_PINS) & set(VOCABULARY_COVERED)), (
        "a vocabulary is in both boxes: "
        f"{sorted(set(VOCABULARY_PINS) & set(VOCABULARY_COVERED))}. Being pinned and "
        "being covered are different claims and a collection cannot rest on both "
        "without one of them going unmaintained."
    )


def test_JR20_no_pinned_vocabulary_can_be_ADDED_TO_or_DELETED_FROM_silently():
    """Equality, not membership — the instrument choice IS the fix.

    A membership assert answers "is this member still there?", which is fail-open
    against addition and blind to a container that has changed type. `==` answers
    "is this collection what was adjudicated?", which is the question.
    """
    resolved = {}
    for module in ADJUDICATED_MODULES.values():
        for name in VOCABULARY_PINS:
            if hasattr(module, name):
                resolved[name] = getattr(module, name)

    missing = sorted(set(VOCABULARY_PINS) - set(resolved))
    assert not missing, (
        f"pinned vocabularies that no module declares: {missing}. A pin against a "
        "name that has moved is a pin against nothing, and it passes."
    )

    for name, expected in sorted(VOCABULARY_PINS.items()):
        raw = resolved[name]
        # Keys-only entries are compared as an ordered tuple of keys, so the type
        # assert below would be comparing tuple to tuple and certifying nothing.
        # State the underlying type here instead, where it is still a real check.
        assert (name not in _KEYS_ONLY) or isinstance(raw, dict), (
            f"`{name}` is pinned by KEYS, which assumes it is a mapping; it is now a "
            f"{type(raw).__name__}. The pin would have compared its keys and passed."
        )
        observed = tuple(raw) if name in _KEYS_ONLY else raw
        assert observed == expected, (
            f"`{name}` is not what was adjudicated.\n"
            f"  pinned:   {expected!r}\n"
            f"  observed: {observed!r}\n"
            f"  added:    {sorted(set(observed) - set(expected))}\n"
            f"  removed:  {sorted(set(expected) - set(observed))}\n"
            "If the change is intended, edit this literal — that edit IS the "
            "adjudication, and it is the thing that must not happen silently. Note "
            "which direction was moved: ADDING to an exemption list and DELETING "
            "from a protection list are the two directions no scenario row catches."
        )
        assert type(observed) is type(expected), (
            f"`{name}` changed TYPE: pinned {type(expected).__name__}, observed "
            f"{type(observed).__name__}. This is the round-20 mutator's own defect "
            "as a production possibility — a single-line tuple that loses an element "
            "textually becomes a `str`, and every membership test in the suite keeps "
            "passing because `in` on a `str` is a substring test."
        )
