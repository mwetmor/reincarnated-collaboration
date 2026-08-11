"""Line-execution collector for the reach audit (Gate-2 C2).

Loaded as a pytest plugin in a CHILD suite run (`-p tests._reach_tracer`) with
`FACTORY_REACH_OUT` naming the file to write. Records every line executed inside
`tests/` and writes them at session end.

Why a plugin and not a fixture: `sys.settrace` only affects frames entered AFTER it
is installed, so it has to go in before collection runs anything.

Frames outside `tests/` return None from the global hook, which switches off line
events for that frame entirely — the difference between a ~1.3x run and an
unusable one. This means the tracer cannot see product lines, which is correct:
the claim under audit is about the SUITE's assertions, not the product's.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

#: Which trees produce line events. Defaults to this directory; the sentinel probe
#: overrides it because the probe is written into a tmp_path, and a tracer whose
#: reach is hardcoded to the suite cannot be shown to have power over anything else.
#: (First version hardcoded `tests/` and the sentinel went red on its first run —
#: which is what a sentinel is for.)
TRACED_DIRS = tuple(
    d for d in os.environ.get(
        "FACTORY_REACH_DIRS", str(Path(__file__).resolve().parent)
    ).split(os.pathsep) if d
)
_reached: set[tuple[str, int]] = set()
#: Every file pytest actually COLLECTED. Gate-2 F2: the audit enumerated its subject
#: with a flat `glob`, while the child collects RECURSIVELY — so an assert in
#: `tests/sub/` was collected, never executed, and never asked about. The subject is
#: now reported by the collector itself, which cannot disagree with the collector.
_collected: set[str] = set()


def _line_hook(frame, event, arg):
    if event == "line":
        _reached.add((frame.f_code.co_filename, frame.f_lineno))
    return _line_hook


def _global_hook(frame, event, arg):
    if frame.f_code.co_filename.startswith(TRACED_DIRS):
        return _line_hook
    return None


def pytest_configure(config):
    sys.settrace(_global_hook)


def pytest_collection_modifyitems(session, config, items):
    for item in items:
        _collected.add(str(Path(str(item.path)).resolve()))


def pytest_unconfigure(config):
    sys.settrace(None)
    out = os.environ.get("FACTORY_REACH_OUT")
    if not out:
        return
    Path(out).write_text(
        json.dumps({
            "reached": sorted(f"{f}:{n}" for f, n in _reached),
            "collected": sorted(_collected),
        }),
        encoding="utf-8",
    )
