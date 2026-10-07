#!/usr/bin/env python3
"""BV2F frozen-tool runner (lane PT, 0.3). Runs a FROZEN v1 python tool against a chosen working root,
without editing the tool.

    python3 v1run.py --root <WORKROOT> <tierA|tierB>/<path/to/tool.py> [tool args...]
    blender -b --python v1run.py -- --root <WORKROOT> tierA/nb_t8/scripts/t5_06a_surface.py [-- tool args]

WHY: the v1 tools find their inputs from their OWN location (HERE = dirname(__file__);
BF/ROOT = dirname(HERE)). A frozen copy run in place would read fid/v1tools/<tier>/barrow_full,
which is not a level. This runner sets the tool's __file__ to <WORKROOT>/<tool's own dir name>/<name>
(e.g. <WORKROOT>/tools/heather_instances.py), so BF/ROOT = <WORKROOT>, and executes the frozen
bytes -- after checking them against SHA256SUMS (shipped sha). The tool file is never copied or edited.

Nothing is written by this runner; the tool writes where its own code writes, under <WORKROOT>.
"""
import hashlib
import os
import sys

V = os.path.dirname(os.path.abspath(__file__))


def shipped_shas():
    out = {}
    for line in open(os.path.join(V, "SHA256SUMS")):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        # format: <shipped_sha> <v1_git_sha> <pin> <path>
        out[parts[-1].lstrip("./")] = parts[0]
    return out


def main():
    try:
        import bpy  # noqa: F401  (inside Blender: our args follow Blender's own '--')
        in_blender = True
    except ImportError:
        in_blender = False
    a = sys.argv[sys.argv.index("--") + 1:] if in_blender else sys.argv[1:]
    if len(a) < 3 or a[0] != "--root":
        sys.exit("usage: v1run.py --root WORKROOT <tier>/<path/tool.py> [args]")
    root, rel, rest = os.path.abspath(a[1]), a[2], a[3:]
    if rest[:1] == ["--"]:
        rest = rest[1:]
    tool = os.path.join(V, rel)
    want = shipped_shas().get(rel)
    if want is None:
        sys.exit("[v1run] HALT: %s is not a frozen tool (not in SHA256SUMS)" % rel)
    src = open(tool, "rb").read()
    got = hashlib.sha256(src).hexdigest()
    if got != want:
        sys.exit("[v1run] HALT: %s sha %s != SHA256SUMS %s" % (rel, got[:12], want[:12]))
    fake = os.path.join(root, os.path.basename(os.path.dirname(tool)), os.path.basename(tool))
    # the tool's own argv shape: blender tools read argv after '--', the others argv[1:]
    sys.argv = [fake] + (["--"] + rest if in_blender else rest)
    sys.path.insert(0, os.path.dirname(tool))      # sibling imports resolve to the frozen dir
    print("[v1run] %s (sha %s) as %s" % (rel, got[:12], fake), file=sys.stderr)
    g = {"__name__": "__main__", "__file__": fake, "__builtins__": __builtins__}
    exec(compile(src, fake, "exec"), g)


main()
