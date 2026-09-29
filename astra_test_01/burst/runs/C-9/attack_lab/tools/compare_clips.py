"""Source clip vs shipped clip, on the data. For each rotation track: key count, key
spacing, interpolation, peak angular speed, and SPIKES -- a key-to-key step far above
the track's own local rate, which is what a one-frame pop is in the data."""
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from gltf_anim import clips, qangle

def track_stats(t, v):
    steps, flips = [], 0
    for i in range(1, len(t)):
        a, f = qangle(v[i - 1], v[i])
        dt = max(t[i] - t[i - 1], 1e-9)
        steps.append((a / dt / 24.0, a, dt, i))       # deg per 1/24 s, deg, dt, key
        flips += int(f)
    return steps, flips

def spikes(steps, k=4.0, floor=8.0):
    """a step more than k x the median of its 6 neighbours AND above `floor` deg per
    1/24 s -- local, because a fast swing is fast everywhere and is not a pop."""
    out = []
    r = [s[0] for s in steps]
    for i, s in enumerate(steps):
        nb = r[max(0, i - 3):i] + r[i + 1:i + 4]
        med = float(np.median(nb)) if nb else 0.0
        if s[0] > floor and s[0] > k * max(med, 1e-6):
            out.append((s[3], s[0], med))
    return out

def report(path, clip, label):
    C = clips(path)
    if clip not in C:
        clip = list(C.keys())[0] if len(C) == 1 else clip
    c = C[clip]
    rot = {b: ch['rotation'] for b, ch in c.items() if 'rotation' in ch}
    anyt = next(iter(rot.values()))[0]
    dts = np.diff(anyt)
    print("\n%s  [%s]  '%s'" % (label, path.rsplit('/', 1)[-1], clip))
    print("  keys %d, duration %.4f s, key spacing %.5f s (%.2f fps), interp %s" % (
        len(anyt), anyt[-1] - anyt[0], float(np.median(dts)), 1.0 / float(np.median(dts)),
        sorted({ch[2] for ch in rot.values()})))
    worst = []
    tot_flips = 0
    all_spk = []
    for b, (t, v, it) in rot.items():
        st, fl = track_stats(t, v)
        tot_flips += fl
        pk = max(st, key=lambda s: s[0]) if st else (0, 0, 0, 0)
        worst.append((pk[0], b, pk[3], t[pk[3]] if st else 0))
        for sp in spikes(st):
            all_spk.append((sp[1], b, sp[0], t[sp[0]], sp[2]))
    worst.sort(reverse=True)
    print("  quaternion sign flips between consecutive keys: %d" % tot_flips)
    print("  fastest tracks (deg per 1/24 s):")
    for w in worst[:5]:
        print("     %-16s %7.1f  at key %d (t=%.3f s)" % (w[1], w[0], w[2], w[3]))
    all_spk.sort(reverse=True)
    print("  SPIKES (step > 4x its neighbours and > 8 deg/frame): %d" % len(all_spk))
    for s in all_spk[:8]:
        print("     %-16s %7.1f deg/frame at key %d (t=%.3f s), neighbours %.1f" % (s[1], s[0], s[2], s[3], s[4]))
    # the root
    hips = c.get('Hips', {}).get('translation')
    if hips is not None:
        t, v, it = hips
        d = np.linalg.norm(np.diff(v, axis=0), axis=1)
        i = int(np.argmax(d))
        print("  Hips translation: %d keys, largest key-to-key step %.4f (units) at key %d (t=%.3f), median %.4f"
              % (len(t), d[i], i + 1, t[i + 1], float(np.median(d))))
    return c

if __name__ == '__main__':
    for path, clip, label in [a.split('::') for a in sys.argv[1:]]:
        report(path, clip, label)
