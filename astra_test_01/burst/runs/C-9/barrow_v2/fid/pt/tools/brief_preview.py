#!/usr/bin/env python3
"""BV2F (lane PT, R-C9-190(3)): assemble a chunk's brief with a FROZEN guided_paint.py WITHOUT writing into the shared
briefs/ dir, and diff two assemblies.

    python3 brief_preview.py <tier>/conductor_scripts/guided_paint.py <cfg.json> <chunk> <out.json>

The frozen file is sha-checked against fid/v1tools/SHA256SUMS, then exec'd as-is with argv [cfg, 'brief', chunk];
the ONLY interception is `open(..., 'w')` on a path under burst/briefs/, which is redirected to <out.json>.
Every read (guide, neighbour artifacts) is the tool's own.
"""
import builtins, hashlib, os, sys

FID = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
V = os.path.join(FID, "v1tools")
rel, cfg, chunk, out = sys.argv[1:5]
tool = os.path.join(V, rel)
src = open(tool, "rb").read()
want = {l.split()[-1].lstrip("./"): l.split()[0] for l in open(os.path.join(V, "SHA256SUMS")) if l.strip() and not l.startswith("#")}
if hashlib.sha256(src).hexdigest() != want.get(rel):
    sys.exit("[brief_preview] HALT: %s is not the frozen file" % rel)
real_open = builtins.open


def guarded_open(p, mode="r", *a, **k):
    if "w" in mode and "/burst/briefs/" in str(p):
        return real_open(out, mode, *a, **k)
    if any(m in mode for m in "wa+"):
        raise PermissionError("brief_preview: unexpected write %s" % p)
    return real_open(p, mode, *a, **k)


sys.argv = [tool, cfg, "brief", chunk]
g = {"__name__": "__main__", "__file__": tool, "__builtins__": builtins, "open": guarded_open}
exec(compile(src, tool, "exec"), g)
