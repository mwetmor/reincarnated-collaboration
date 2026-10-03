# Does the manifest agree with the GLB, and with itself?
#
#   python3 scripts/48_manifest_lint.py <manifest.json> <x.glb>
#
# The scene now reads speeds from the manifest at load, so a stale number in it
# is a defect in the shipped product, not a documentation slip. And one got
# through: run_armed_trim said "0.667 s ... 4.74 m/s" while locomotion_in_place
# said 0.8333 s and 3.795 -- the same file answering one question two ways,
# because the correction was written in a new block and the old one was left.
#
# Three checks, and the third is the one that catches this class:
#   DURATION  any "<n> s" stated near a clip name, against the GLB's sampler
#             times. The GLB is authoritative: its inputs are seconds.
#   SPEED     any "<n> m/s" stated near a clip name, against the single
#             declared speed for that clip. Not against the GLB -- the clips
#             ship in place, so there is no travel left in the file to check a
#             speed against. This is an INTERNAL consistency check and saying so
#             matters: it cannot tell you the speed is right, only that the
#             manifest states one speed rather than several.
#   ARITHMETIC the declared speed against the declared travel and duration.
#
# Prose is scanned as well as fields, because the stale numbers were in prose.
#
# THE CLIP A NUMBER BELONGS TO COMES FROM THE PATH FIRST, then the text. The
# first version of this check looked only in the text and so missed the very
# defect it was written for: "ONE gait cycle: 20 frames, 0.667 s ... 4.74 m/s"
# never says "run_armed" -- the clip name is the KEY of the block containing it.
# Meanwhile it flagged two phantoms, matching the bare words "run" and "walk"
# inside "walk/run sync group" and attaching them to a neighbouring "2.0 s".
# So: longest clip name in the path wins; failing that, longest in the text;
# and a name shorter than 5 characters is not matched from text at all, because
# "run" and "walk" are words before they are clip names.
import json, re, sys
sys.path.insert(0, __file__.rsplit('/', 1)[0])
T = __import__('46_clip_timing')

NUM_S = re.compile(r'(\d+(?:\.\d+)?)\s*s(?:ec(?:onds?)?)?\b')
NUM_V = re.compile(r'(\d+(?:\.\d+)?)\s*m/s\b')
TOL = 0.02          # 2% -- rounding in the manifest, not a real disagreement


def walk(node, path=""):
    if isinstance(node, dict):
        for k, v in node.items():
            yield from walk(v, "%s.%s" % (path, k))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk(v, "%s[%d]" % (path, i))
    else:
        yield path, node


def main():
    mf, glb = sys.argv[1], sys.argv[2]
    m = json.load(open(mf))
    tim, _ = T.timing(glb)
    clips = set(tim)
    # the single declared speed per clip, from locomotion_in_place
    loco = m.get("locomotion_in_place", {})
    declared = {}
    for cn in clips:
        d = loco.get(cn)
        if isinstance(d, dict):
            for k in ("speed_m_s", "stepping_speed_m_s", "net_speed_m_s"):
                if isinstance(d.get(k), (int, float)):
                    declared.setdefault(cn, []).append((k, float(d[k])))
    bad = []
    def owner(path, val):
        inpath = sorted([c for c in clips if c in path], key=len)
        if inpath:
            return inpath[-1]
        intext = sorted([c for c in clips if len(c) >= 5 and c in val], key=len)
        return intext[-1] if intext else None

    for path, val in walk(m):
        if not isinstance(val, str):
            continue
        cn = owner(path, val)
        if cn:
            for s_ in NUM_S.findall(val):
                got, want = float(s_), tim[cn]["seconds"]
                if want > 0 and abs(got - want) / want > TOL:
                    bad.append("%s says '%s ... %s s' but the GLB says %.4f s"
                               % (path, cn, s_, want))
            for v_ in NUM_V.findall(val):
                got = float(v_)
                opts = [x[1] for x in declared.get(cn, [])]
                if opts and not any(abs(got - o) / max(o, 1e-9) <= TOL for o in opts):
                    bad.append("%s says '%s ... %s m/s' but the declared speed%s "
                               "for %s %s %s"
                               % (path, cn, v_, "s" if len(opts) > 1 else "", cn,
                                  "are" if len(opts) > 1 else "is",
                                  ", ".join("%.3f" % o for o in opts)))
    # structured duration fields
    for cn in clips:
        d = loco.get(cn)
        if isinstance(d, dict) and isinstance(d.get("seconds"), (int, float)):
            got, want = float(d["seconds"]), tim[cn]["seconds"]
            if want > 0 and abs(got - want) / want > TOL:
                bad.append("locomotion_in_place.%s.seconds = %s but the GLB says "
                           "%.4f" % (cn, got, want))
        if isinstance(d, dict):
            tr, se, sp = d.get("cycle_travel_m"), d.get("seconds"), d.get("speed_m_s")
            if all(isinstance(x, (int, float)) for x in (tr, se, sp)) and se > 0:
                if abs(tr / se - sp) / max(sp, 1e-9) > TOL:
                    bad.append("locomotion_in_place.%s: %.4f m / %.4f s = %.3f "
                               "m/s, not the stated %.3f"
                               % (cn, tr, se, tr / se, sp))
    # RELEASE_S (D7): every cast states the instant its spell leaves the hand.
    # The scene reads it at load to spawn the projectile, so it is a shipped
    # number and is linted like a speed. Three checks against the GLB:
    #   inside the clip        0 < release_s < duration
    #   on a real key          within half a frame of a sampler time, because a
    #                          release between keys is an interpolated pose the
    #                          animator never drew
    #   one answer             stated once, in casts.<clip>.release_s
    casts = m.get("casts", {})
    g_, bin_ = T.L.load_glb(glb)
    for cn, rec in casts.items():
        if not isinstance(rec, dict) or "release_s" not in rec:
            continue
        rs = float(rec["release_s"])
        if cn not in tim:
            bad.append("casts.%s: no clip of that name in the GLB" % cn)
            continue
        dur = tim[cn]["seconds"]
        if not (0.0 < rs < dur):
            bad.append("casts.%s.release_s = %.4f is outside the clip (0, %.4f)" % (cn, rs, dur))
        keys = set()
        for an in g_.get("animations", []):
            if an.get("name") != cn:
                continue
            for ch in an.get("channels", []):
                tt = T.L.read_accessor(g_, bin_, an["samplers"][ch["sampler"]]["input"])[:, 0]
                keys.update(round(float(x), 5) for x in tt)
        if keys:
            t0 = min(keys)
            step = min(b - a for a, b in zip(sorted(keys), sorted(keys)[1:])) if len(keys) > 1 else 1.0
            near = min(abs((rs + t0) - k) for k in keys)
            if near > step / 2 + 1e-4:
                bad.append("casts.%s.release_s = %.4f falls %.4f s from the nearest key "
                           "(frame step %.4f) -- a pose between keys" % (cn, rs, near, step))
    rel = [c for c, r in casts.items() if isinstance(r, dict) and "release_s" in r]
    if rel:
        print("  release_s checked on %d cast(s): %s" % (len(rel), ", ".join(rel)))
    for b in bad:
        print("  MANIFEST MISMATCH  %s" % b)
    print("  %d clip(s) checked, %d mismatch(es)" % (len(clips), len(bad)))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
