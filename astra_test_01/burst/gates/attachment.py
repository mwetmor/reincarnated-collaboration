"""Bright flare attachment distance, measured in the supplied frame canvas."""
import math

import numpy as np
from scipy import ndimage

from gates.vfx_lifecycle import _frames, _result

BRIGHT_BLOB_FRACTION = .8


def flare_centroid(frame):
    """Alpha*HSV-value centroid of the strongest connected bright core.

    Core pixels have weight >= .8 of the frame maximum, 8-connectivity.
    Choose the component with greatest integrated weight (ties raster order).
    Invisible RGB is excluded; an empty frame has no measurable flare.
    """
    a = _frames([frame])[0]
    weights = a[..., :3].max(axis=2).astype(float)*a[..., 3].astype(float)/255
    maximum = float(weights.max())
    if maximum <= 0:
        return None
    labels, count = ndimage.label(weights >= BRIGHT_BLOB_FRACTION*maximum,
                                  structure=np.ones((3, 3)))
    sums = ndimage.sum(weights, labels, range(1, count+1))
    chosen = int(np.argmax(sums))+1
    y, x = ndimage.center_of_mass(weights, labels, chosen)
    return [float(x), float(y)]


def evaluate(vfx_frames, socket_xy_per_frame, tol_px=6):
    """Maximum active-frame centroid/socket distance; no alignment is applied.

    Fully dark/transparent frames have null distance and are excluded. Missing
    sockets on an active frame make the aggregate unevaluable unless another
    measured frame already exceeds the literal tolerance.
    """
    if isinstance(tol_px, bool) or not math.isfinite(float(tol_px)) or tol_px < 0:
        raise ValueError('tol_px must be finite and nonnegative')
    frames = _frames(vfx_frames)
    sockets = list(socket_xy_per_frame)
    if len(sockets) != len(frames):
        raise ValueError('Exactly one socket per VFX frame required')
    details, values, missing = [], [], []
    for i, (a, socket) in enumerate(zip(frames, sockets)):
        if socket is not None:
            socket = np.asarray(socket, dtype=float)
            if socket.shape != (2,) or not np.isfinite(socket).all():
                raise ValueError('Each socket must be a finite xy pair or None')
            socket = socket.tolist()
        center = flare_centroid(a)
        distance = None
        reason = 'no_emissive_flare' if center is None else None
        if center is not None and socket is None:
            missing.append(i); reason = 'missing_socket'
        elif center is not None:
            distance = float(np.linalg.norm(np.asarray(center)-socket))
            values.append(distance)
        details.append(dict(index=i, centroid_xy=center, socket_xy=socket,
                            distance_px=distance, reason=reason))
    row = _result('attachment', 'vfx', max(values) if values else None,
                  float(tol_px), unit='px', per_frame=details,
                  missing_active_sockets=missing, bright_blob_fraction=BRIGHT_BLOB_FRACTION,
                  definition='Maximum Euclidean distance in supplied canvas; no registration')
    if missing and row['passed'] is not False:
        row['passed'] = None
    return row
