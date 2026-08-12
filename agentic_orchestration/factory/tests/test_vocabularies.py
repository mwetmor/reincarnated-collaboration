"""Gate-2 JR-20 — which module-level collections need a literal pin, derived over
ALL of them rather than over the four that happened to be under discussion.

Rule 47 asked ONE question — is a member *behaviour* or a *record*? — and got the
right answer for the dict it was written about. jack-ryan measured three survivors
it does not explain: deleting a member of `FACTORY_RUNTIME_PATHS` survives, and
ADDING to `FACTORY_RUNTIME_PATHS` or to `STRUCTURE_SKIP_DIRS` survives. (That
collection was split into `FACTORY_RUNTIME_FILES` and `FACTORY_RUNTIME_DIRS` at
JR-22; the finding above is about both halves and is left in its original words.)
All three
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
import importlib
from pathlib import Path

from factory import permissions as perm

FACTORY_DIR = Path(__file__).resolve().parents[1]
_PACKAGE_PREFIX = "agentic_orchestration/factory/"

#: Runtime subtrees, taken FROM THE PRODUCT rather than restated here (JR-24).
#:
#: This is not tidiness. `sessions/` holds QUARANTINED PHASE ARTIFACTS — real `.py`
#: files whose contents a phase chose — so a naive `rglob` puts this file's
#: denominator under the control of the thing it is measuring. Measured in the live
#: worktree, the naive walk returns 18 names, two of them
#: (`ARTIFACT_KINDS`, `MIGRATIONS`) written by earlier runs into `sessions/`; the
#: filtered walk below returns 16. The hazard is invisible in a `git archive HEAD`
#: copy, where `sessions/` is gitignored and therefore ABSENT, and live in the tree
#: that ships — a review environment can be CLEANER than the runtime one.
#:
#: CORRECTED (round 25). This comment used to continue "that is also why jack-ryan
#: measured 'the walk returns the same fifteen' and I do not". Wrong, and wrong at
#: their expense. Their fifteen is CORRECT at their target `7bbba6fb` — reproduced
#: from `git archive`: 21 modules, 15 names. The 15→16 delta is JR-22 splitting
#: `FACTORY_RUNTIME_PATHS`; the 16→18 delta is `sessions/`. Two causes, and the
#: sentence charged both to the second. Comparing counts taken over different
#: denominators and reading the difference as someone's error is this series' own
#: defect shape (rule 49), committed inside the note explaining the fix.
_RUNTIME_SUBTREES: tuple[str, ...] = tuple(
    p[len(_PACKAGE_PREFIX):] for p in perm.FACTORY_RUNTIME_DIRS
)


def _adjudicated_modules() -> tuple[str, ...]:
    """Every SOURCE module in the package. Walked, not named (JR-24).

    The named-four version could not see a new vocabulary in `runner.py`, `gates.py`,
    `receipts.py`, `phase.py`, `host.py`, `usage.py`, `report.py` or `cli.py` — eight
    modules outside a denominator whose whole purpose is to be complete. Its comment
    said a walk "would sweep in infrastructure dicts and the resulting table would be
    long enough that nobody reads it"; measured, the walk returns exactly the same
    names, because the classifier below already ignores private and non-container
    assignments. The objection was reasoned and the reasoning was wrong.
    """
    out = []
    for path in sorted(FACTORY_DIR.rglob("*.py")):
        rel = path.relative_to(FACTORY_DIR).as_posix()
        if rel.startswith("tests/"):
            continue
        if any(rel.startswith(sub) for sub in _RUNTIME_SUBTREES):
            continue
        out.append(rel)
    return tuple(out)


ADJUDICATED_MODULES: tuple[str, ...] = _adjudicated_modules()

#: Public UPPERCASE module-level names that are NOT vocabularies, each with its
#: reason. The classifier does not get to silently DROP what it cannot understand:
#: anything that is neither a container nor a scalar must be named here or it reds
#: the row by existing. That is the JR-20 direction question turned on the classifier
#: itself — an unrecognised spelling used to be an exemption nobody had to ask for.
NOT_A_VOCABULARY: dict[str, str] = {
    "cli.py:FACTORY_DIR": "a Path expression, not a collection",
    "harness/claude_code.py:HARNESS": "the object returned by `register_harness(...)`",
    "harness/codex.py:HARNESS": "the object returned by `register_harness(...)`",
}


# ---------------------------------------------------------------------------
# The pins.
# ---------------------------------------------------------------------------

#: Every entry says WHICH DIRECTION it is pinned against, because a pin whose
#: direction is not stated is the state rule 47 was in.
VOCABULARY_PINS: dict[str, object] = {
    # --- exemption: ADDITION is the fail-open direction --------------------
    #: Forgiven in the root repo, EXACT match only. Split from the directories at
    #: JR-22, where one collection spent as `rel.startswith(p)` forgave
    #: `receipts.dbEVIL` and a whole collapsed subtree. Adding
    #: `"agentic_orchestration"` here forgives one path; adding it to the DIRS
    #: tuple below forgives nine agents' trees, and `""` there forgives
    #: everything — which is why the two are pinned separately rather than as one
    #: list whose members mean different things. Measured by jack-ryan at round 21:
    #: member deletion SURVIVES (no covering row at all) and addition SURVIVES.
    #: `test_JR22_every_exemption_MEMBER_states_its_own_matching_direction` now
    #: covers the DIRECTION of every member; this pin covers WHICH members exist,
    #: which that row cannot — it passes just as happily over a wider list.
    "FACTORY_RUNTIME_FILES": (
        "agentic_orchestration/factory/receipts.db",
        "agentic_orchestration/factory/receipts.db-wal",
        "agentic_orchestration/factory/receipts.db-shm",
    ),
    #: Forgiven as a PREFIX, which is the fail-open half. See above.
    "FACTORY_RUNTIME_DIRS": (
        "agentic_orchestration/factory/sessions/",
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
        #: ADDED at Gate-2 JR-23, and this line IS the adjudication. `unreadable_marker`
        #: refuses any change whose key carries a `MARKER_SEP` note: the path could not
        #: be read when the tree was fingerprinted, so the string is a measurement's own
        #: note and not a name the rollback may act on. This is an ADDITION to an accept
        #: vocabulary — the direction this pin exists to catch — so it is spelled out
        #: rather than absorbed. What it admits is a REFUSAL and never an action, and it
        #: replaced a path on which the rollback ACTED on a guessed name: measured, an
        #: ignored untracked `build/` was deleted under the reason "created by the
        #: phase" because the phase had created `build\tx` beside it.
        "unreadable_marker",
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
    # Every figure below names the MEMBER it is about (rule 50). JR-25: the
    # `11 failed` that stood against GIT_CONTROL_PATHS was a measurement of a
    # DIFFERENT collection, and nothing in the sentence could have said so.
    "PROTECTED_ALWAYS":
        "deny arm; deleting a member stops a path being refused and the wall's "
        "protected-path rows flip verdict. MEASURED round 23: `canonical/` deleted, "
        "KILLED, 2 failed (R23-I); `agentic_orchestration/factory/` deleted, KILLED, "
        "2 failed (R23-J)",
    "PROTECTED_EVERY_REPO":
        "measured round 23: `.claude/` deleted, KILLED, 3 failed (R23-K)",
    "GIT_CONTROL_PATHS":
        "measured round 23: `config.worktree` deleted, KILLED, 3 failed (R23-F); "
        "`hooks/` deleted, KILLED, 21 failed (R23-G). The `11 failed` printed here "
        "until round 23 belonged to `GIT_NESTED_GITDIRS`' `modules/`; no member of "
        "THIS collection gives 11, and until R23-F it had never been measured",
    "GIT_NESTED_GITDIRS":
        "measured round 21 by jack-ryan: `worktrees/` deleted, KILLED, 7 failed; "
        "measured round 23: `modules/` deleted, KILLED, 11 failed (R23-H). My own "
        "round-20 figure for this row was an artifact — see rule 48",
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
    return _classify_module(relpath)[0]


#: Container CONSTRUCTORS, not only container LITERALS (JR-24). The v1 filter
#: recognised `frozenset(...)` and `set(...)` and nothing else, so a vocabulary
#: spelled `tuple([...])` left the denominator without anyone choosing that — an
#: exemption granted by SPELLING, in the addition direction, which is the direction
#: this whole file exists to close.
_CONTAINER_CALLS = frozenset({"frozenset", "set", "tuple", "list", "dict"})
_CONTAINER_LITERALS = (ast.Tuple, ast.List, ast.Set, ast.Dict)


def _classify_module(relpath: str) -> tuple[set[str], set[str]]:
    """(vocabularies, UNCLASSIFIABLE) for one module's public UPPERCASE names.

    By AST rather than by `dir()`, so a name imported into the module is not
    counted as one the module declares — the denominator has to be the set of
    things this file is responsible for, not the set of things visible from it
    (rule 49: establish the denominator before reasoning over the set).

    THREE outcomes, not two. A name whose value is a container is a vocabulary; a
    name whose value is a scalar constant is not; and a name that is NEITHER is
    returned as unclassifiable rather than dropped. Dropping was the v1 behaviour
    and it is an exemption the classifier granted itself, silently, in the direction
    where nothing can notice.
    """
    tree = ast.parse((FACTORY_DIR / relpath).read_text())
    found: set[str] = set()
    unknown: set[str] = set()
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
            if isinstance(value, _CONTAINER_LITERALS):
                found.add(target.id)
            elif (isinstance(value, ast.Call)
                    and getattr(value.func, "id", "") in _CONTAINER_CALLS):
                found.add(target.id)
            elif isinstance(value, ast.Constant):
                continue                      # a scalar; not a vocabulary
            else:
                unknown.add(target.id)
    return found, unknown


def test_JR24_the_classifier_ADJUDICATES_what_it_cannot_CLASSIFY():
    """An unrecognised spelling is a question, not an answer.

    The v1 classifier had two exits: "container" and "everything else, dropped". The
    second is an exemption in the ADDITION direction — write a vocabulary in a shape
    the filter does not know and it leaves the denominator, with no row anywhere able
    to see that it did, because the row that would catch it has to name a spelling
    nobody has used yet. That is JR-20's own finding, standing inside the file that
    made it.

    So the third exit reds this row, and clearing it means writing the name into
    `NOT_A_VOCABULARY` with a reason — which is the adjudication, performed by a
    human, exactly once.
    """
    unclassifiable: dict[str, str] = {}
    for relpath in ADJUDICATED_MODULES:
        for name in _classify_module(relpath)[1]:
            unclassifiable[f"{relpath}:{name}"] = relpath

    unadjudicated = sorted(set(unclassifiable) - set(NOT_A_VOCABULARY))
    assert not unadjudicated, (
        f"public UPPERCASE names the classifier cannot place: {unadjudicated}. Each "
        "is either a vocabulary spelled in a shape `_classify_module` does not know "
        "— add the shape — or it is not a vocabulary, in which case name it in "
        "`NOT_A_VOCABULARY` with the reason. What must not happen is the v1 "
        "behaviour: dropped, silently, by a filter that had no opinion."
    )
    stale = sorted(set(NOT_A_VOCABULARY) - set(unclassifiable))
    assert not stale, (
        f"adjudicated as 'not a vocabulary' but no longer unclassifiable: {stale}. "
        "Either the name is gone or it now classifies cleanly; an exemption for a "
        "condition that has passed is an exemption nobody is maintaining."
    )


def test_JR24_the_denominator_covers_the_PACKAGE_and_excludes_only_RUNTIME():
    """What the walk includes, asserted rather than left to the walk.

    Two claims, and the second is the one with teeth. The named-four version could
    not see a vocabulary in `runner.py`; the walk can. And the walk must NOT see
    `sessions/`, because `sessions/` holds quarantined phase artifacts — `.py` files
    a phase wrote — so an unfiltered walk hands the denominator of the containment
    tests to the thing being contained.
    """
    assert _RUNTIME_SUBTREES, "the exclusion list is empty; the filter does nothing"
    for member in perm.FACTORY_RUNTIME_DIRS:
        assert member.startswith(_PACKAGE_PREFIX), (
            f"{member!r} is not under {_PACKAGE_PREFIX!r}, so the slice that derives "
            "the exclusion prefixes silently produced a wrong string"
        )
    for expected in ("runner.py", "gates/base.py", "receipts.py", "cli.py"):
        assert expected in ADJUDICATED_MODULES, (
            f"{expected} is outside the denominator — the named-four state JR-24 found"
        )
    assert not [m for m in ADJUDICATED_MODULES if m.startswith("sessions/")], (
        "a quarantined phase artifact entered the denominator. A phase could then "
        "add or remove names from the set this file adjudicates, which inverts what "
        "the file is for"
    )


def test_JR20_every_vocabulary_is_either_PINNED_or_NAMES_the_row_that_covers_it():
    """The denominator, established rather than assumed.

    jack-ryan's verdict said "re-derive from all fifteen rather than from four".
    The count is reproducible: it is the number of public UPPERCASE module-level
    containers across the package's SOURCE modules, and this row recomputes it
    from source every time rather than trusting the number. A new vocabulary
    added to any of them fails here until somebody has said which of the
    two boxes it goes in — which is the structural half of the fix, and the half
    that survives the next collection nobody has written yet.

    *Round 23 (JR-24): the denominator is now the WALK, not four named modules.*
    Fifteen became sixteen at JR-22 (`FACTORY_RUNTIME_PATHS` split in two), and no
    number is written down here, because a hardcoded total is a claim that goes
    stale in exactly the direction — growth — that this row exists to catch.
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
    for relpath in ADJUDICATED_MODULES:
        # Imported from the same relpath the AST walk read, so the two halves of this
        # file cannot disagree about which module they are talking about.
        module = importlib.import_module(
            "factory." + relpath[: -len(".py")].replace("/", ".")
        )
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
