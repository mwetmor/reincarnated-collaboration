"""Socket review composites; no source rescale, registration, or frame mirroring.

Character and VFX share the explicit output clock. The character repeats if
shorter; the effect plays once and then stays transparent. Output count is the
longer input count. Source VFX anchor is fixed at its canvas centre, never a
per-frame centroid fit (which would hide attachment wobble).
"""
import json
from pathlib import Path

import numpy as np
from PIL import Image

from gates.attachment import evaluate as attachment_evaluate
from gates.vfx_lifecycle import _frames, _fps, sequence_pse
from oracle.video_cut import track
from review.encode import encode_loop


def estimate_sockets(character_frames, transform=None):
    """Track tip_xy; optionally map NATIVE inputs through a cell transform.

    With transform=None, inputs are already registered and the identity map is
    reported. With a transform, inputs MUST be the native frames, never the
    registered output again. Pixel-centre map matches Pillow's sampling box:
    registered_xy = (native_xy + .5)*scale - .5 + translation_xy.
    This mask landmark is a staff-tip proxy, not a labeled anatomical socket.
    """
    frames = _frames(character_frames)
    if not frames:
        raise ValueError('At least one character frame required')
    scale, translation = 1., np.zeros(2)
    if transform is not None:
        scale = float(transform['scale'])
        translation = np.asarray(transform['translation_xy'], dtype=float)
        if not np.isfinite(scale) or not 0 < scale <= 1 or translation.shape != (2,) or not np.isfinite(translation).all():
            raise ValueError('Expected one downscale and finite xy translation')
        if np.any(translation != np.rint(translation)):
            raise ValueError('Cell translation must be integer')
        if 'source_size' in transform and list(transform['source_size']) != [frames[0].shape[1], frames[0].shape[0]]:
            raise ValueError('Native input dimensions disagree with cell transform')
    series = track(frames)
    mapped = [((np.asarray(p)+.5)*scale-.5+translation).tolist() if p is not None else None
              for p in series['tip_xy']]
    return dict(xy_per_frame=mapped, source='oracle.video_cut.track.tip_xy',
                native_tip_xy=series['tip_xy'], working_scale=series['working_scale'],
                transform=dict(scale=scale, translation_xy=translation.tolist()),
                input_space='native' if transform is not None else 'registered',
                mapping='(xy + 0.5) * scale - 0.5 + translation_xy',
                notes='Mask-based staff-tip proxy; no anatomical guarantee or per-frame correction')


def premultiplied_over(character, overlay):
    """Straight uint8 RGBA in/out, Porter-Duff over in premultiplied byte RGB.

    No linear-light conversion: this matches the T3d/Pillow review convention.
    RGB under zero output alpha is set to zero; input arrays are never changed.
    """
    base, top = _frames([character, overlay])
    base, top = base.astype(float)/255, top.astype(float)/255
    ab, at = base[..., 3:4], top[..., 3:4]
    alpha = at+ab*(1-at)
    premult = top[..., :3]*at+base[..., :3]*ab*(1-at)
    rgb = np.divide(premult, alpha, out=np.zeros_like(premult), where=alpha > 0)
    return np.rint(np.concatenate([rgb, alpha], axis=2)*255).clip(0, 255).astype(np.uint8)


def composite(character_frames, vfx_frames, sockets, out_dir, fps):
    """Write RGBA frames, H.264 MP4, sockets.json and PSE/attachment reports.

    sockets accepts one fixed xy pair, an xy list of output length, or the
    estimate_sockets report. All placements round to integer pixels. Clips at
    canvas edges are recorded by alpha mass lost, never silently recentered.
    """
    fps = _fps(fps)
    characters, effects = _frames(character_frames), _frames(vfx_frames)
    if not characters or not effects:
        raise ValueError('Nonempty character and VFX sequences required')
    n = max(len(characters), len(effects))
    metadata = dict(sockets) if isinstance(sockets, dict) else {'source': 'supplied'}
    values = sockets['xy_per_frame'] if isinstance(sockets, dict) else sockets
    try:
        xy = np.asarray(values, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError('Sockets must be finite xy pairs') from exc
    if xy.shape == (2,):
        xy = np.repeat(xy[None, :], n, axis=0)
        metadata['source'] = 'fixed_socket'
    if xy.shape != (n, 2) or not np.isfinite(xy).all():
        raise ValueError('One finite socket per output frame required')
    height, width = characters[0].shape[:2]
    eh, ew = effects[0].shape[:2]
    anchor = np.array([ew//2, eh//2])
    output, overlays, placements = [], [], []
    for i in range(n):
        overlay = Image.new('RGBA', (width, height))
        offset = np.rint(xy[i]-anchor).astype(int)
        source_sum = 0.
        if i < len(effects):
            source_sum = float(effects[i][..., 3].sum())
            # Unmasked paste preserves straight RGB/alpha, without double alpha.
            overlay.paste(Image.fromarray(effects[i]), tuple(offset.tolist()))
        a = np.array(overlay)
        lost = max(0., source_sum-float(a[..., 3].sum()))
        placements.append(dict(index=i, character_index=i % len(characters),
                               vfx_index=i if i < len(effects) else None,
                               socket_xy=xy[i].tolist(), offset_xy=offset.tolist(),
                               clipped_alpha_fraction=lost/source_sum if source_sum else 0.))
        overlays.append(a)
        output.append(premultiplied_over(characters[i % len(characters)], a))
    attachment = attachment_evaluate(overlays, xy)
    pse = dict(character=sequence_pse(characters, fps, 'composite.character'),
               vfx=sequence_pse(effects, fps, 'composite.vfx'),
               composite=sequence_pse(output, fps, 'composite'))
    out = Path(out_dir)
    folder = out/'frames'; folder.mkdir(parents=True, exist_ok=True)
    paths = []
    for i, a in enumerate(output):
        path = folder/f'composite_{i:02d}.png'
        Image.fromarray(a).save(path); paths.append(str(path))
    mp4 = encode_loop(output, fps, out/'composite.mp4', scale=1, loops=1)
    report = dict(fps=fps, count=n, canvas=[width, height], vfx_anchor_xy=anchor.tolist(),
                  socket_source=metadata, xy_per_frame=xy.tolist(), placements=placements,
                  timing='One shared fps; character cycles, VFX once then transparent',
                  compositing='Premultiplied Porter-Duff over; straight RGBA outputs',
                  attachment=attachment, pse=pse, frames=paths, mp4=str(mp4))
    path = out/'sockets.json'
    path.write_text(json.dumps(report, indent=2, allow_nan=False)+'\n')
    return dict(report, sockets_json=str(path))
