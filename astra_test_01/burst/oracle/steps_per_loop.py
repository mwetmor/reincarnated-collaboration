"""Report head bobs per registered loop; no gait or shipping verdict.

Confidence is the dominant bin's share of non-DC FFT power (squared magnitude,
one-sided rFFT). No smoothing, detrending beyond mean removal, or interpolation
is applied. A constant series has no measured step count: steps=None,
confidence=0. The instrument measures image motion, not anatomical footfalls.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image


def measure(frames_dir):
    """Measure sorted RGBA PNGs in a frame directory or one walk/run cell.

    Cell roots resolve only frames/{walk,run}/D/*.png, excluding rest frames
    and contact sheets. Multiple animation directories are rejected, as are
    empty alpha support, mismatched canvases and fewer than two frames.
    Alpha >= 128 defines the head-top row, at the delivered resolution.
    """
    root = Path(frames_dir)
    if not root.is_dir():
        raise ValueError('frames_dir must be an existing directory')
    paths = sorted(root.glob('*.png'))
    if not paths:
        if (root/'frames').is_dir():
            root = root/'frames'
        paths = sorted([*root.glob('walk/*/*.png'), *root.glob('run/*/*.png')])
    if len({p.parent for p in paths}) > 1:
        raise ValueError('frames_dir must contain exactly one animation loop')
    if len(paths) < 2:
        raise ValueError('at least two registered RGBA PNG frames are required')
    tops = []
    size = None
    for path in paths:
        with Image.open(path) as frame:
            if frame.mode != 'RGBA':
                raise ValueError('registered frames must be RGBA: '+str(path))
            if size is not None and frame.size != size:
                raise ValueError('registered frame canvas sizes differ')
            size = frame.size
            rows = np.flatnonzero(np.any(np.asarray(frame)[..., 3] >= 128, axis=1))
            if not len(rows):
                raise ValueError('frame has no alpha >= 128 support: '+str(path))
            tops.append(int(rows[0]))
    values = np.asarray(tops, dtype=float)
    values -= values.mean()
    spectrum = np.abs(np.fft.rfft(values))[1:]**2
    total = float(spectrum.sum())
    method = 'head_top_y_fft_power'
    if total == 0:
        return dict(steps=None, confidence=0.0, method=method+'; no non-DC energy')
    peak = int(np.argmax(spectrum))
    return dict(steps=peak+1, confidence=float(spectrum[peak]/total), method=method)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('frames_dir', type=Path)
    args = parser.parse_args(argv)
    print(json.dumps(measure(args.frames_dir), allow_nan=False))


if __name__ == '__main__':
    main()
