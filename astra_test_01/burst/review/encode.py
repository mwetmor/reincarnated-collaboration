"""Deterministic Pillow review rasters and streaming H.264 encodes.

Frames may be paths, Pillow images, or uint8 RGB/RGBA arrays. Canvas is an
optional pre-scale (width, height), or square integer, centred without cropping.
Odd video dimensions are padded on the right/bottom for yuv420p. No source
frame is modified. Side-by-side uses a common clock at the higher input fps,
repeating each source independently until the longer source completes once.
"""
import math
from pathlib import Path
import subprocess
import threading

import numpy as np
from PIL import Image, ImageColor, ImageDraw

FFMPEG = '/opt/homebrew/bin/ffmpeg'
BACKGROUND = '#3a3f4a'


def _frames(frames):
    if isinstance(frames, (str, Path)):
        frames = sorted(Path(frames).glob('*.png'))
    result = []
    for frame in frames:
        if isinstance(frame, (str, Path)):
            with Image.open(frame) as image:
                result.append(image.convert('RGBA'))
        elif isinstance(frame, Image.Image):
            result.append(frame.convert('RGBA'))
        else:
            a = np.asarray(frame)
            if a.dtype != np.uint8 or a.ndim != 3 or a.shape[2] not in (3, 4):
                raise ValueError('Frames must be uint8 RGB/RGBA arrays')
            result.append(Image.fromarray(a).convert('RGBA'))
    if not result:
        raise ValueError('At least one frame required')
    if any(im.size != result[0].size for im in result):
        raise ValueError('All frames in a sequence must share a canvas')
    return result


def _positive(value, name):
    if isinstance(value, bool) or not math.isfinite(float(value)) or float(value) <= 0:
        raise ValueError(name + ' must be finite and positive')
    return float(value)


def _rgb(frame, bg=BACKGROUND, canvas=None):
    size = frame.size if canvas is None else ((canvas, canvas) if isinstance(canvas, int) else tuple(canvas))
    if len(size) != 2 or any(isinstance(v, bool) or not isinstance(v, int) or v <= 0 for v in size):
        raise ValueError('Canvas must contain two positive integers')
    if size[0] < frame.width or size[1] < frame.height:
        raise ValueError('Canvas would crop source frame')
    color = ImageColor.getrgb(bg) if isinstance(bg, str) else tuple(bg)
    base = Image.new('RGBA', size, (*color[:3], 255))
    base.alpha_composite(frame, ((size[0]-frame.width)//2, (size[1]-frame.height)//2))
    return base.convert('RGB')


def _encode(images, fps, out_mp4, size):
    """Stream RGB frames; drain stderr concurrently, creating no temp files."""
    out = Path(out_mp4)
    out.parent.mkdir(parents=True, exist_ok=True)
    w, h = size
    command = [FFMPEG, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
               '-s:v', f'{w}x{h}', '-r', str(fps), '-i', 'pipe:0', '-an',
               '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2:0:0:color=0x3a3f4a',
               '-c:v', 'libx264', '-preset', 'fast', '-crf', '16', '-threads', '2',
               '-pix_fmt', 'yuv420p', '-tag:v', 'avc1', '-movflags', '+faststart',
               '-f', 'mp4', str(out)]
    proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                            stderr=subprocess.PIPE)
    errors = []
    def drain():
        for chunk in iter(lambda: proc.stderr.read(8192), b''):
            errors.append(chunk)
    reader = threading.Thread(target=drain, daemon=True)
    reader.start()
    try:
        try:
            for im in images:
                proc.stdin.write(im.tobytes())
            proc.stdin.close()
        except BrokenPipeError:
            pass
        code = proc.wait(timeout=110)
        reader.join()
        if code:
            raise RuntimeError('ffmpeg encode: ' + b''.join(errors).decode(errors='replace'))
    except BaseException:
        proc.kill()
        proc.wait()
        reader.join()
        out.unlink(missing_ok=True)
        raise
    finally:
        try:
            proc.stdin.close()
        except BrokenPipeError:
            pass
        proc.stderr.close()
    return out


def encode_loop(frames, fps, out_mp4, scale=2, resample='lanczos', loops=5,
                bg='#3a3f4a', canvas=None):
    """Encode exactly len(frames)*loops frames at fps, composite then resize."""
    fps = _positive(fps, 'fps')
    scale = _positive(scale, 'scale')
    if isinstance(loops, bool) or not isinstance(loops, int) or loops < 1:
        raise ValueError('loops must be a positive integer')
    filters = {'lanczos': Image.Resampling.LANCZOS, 'nearest': Image.Resampling.NEAREST,
               'bilinear': Image.Resampling.BILINEAR, 'bicubic': Image.Resampling.BICUBIC}
    if resample not in filters:
        raise ValueError('Unknown resampling filter')
    source = [_rgb(im, bg, canvas) for im in _frames(frames)]
    size = (max(1, round(source[0].width*scale)), max(1, round(source[0].height*scale)))
    source = [im.resize(size, filters[resample]) for im in source]
    return _encode((im for _ in range(loops) for im in source), fps, out_mp4, size)


def encode_side_by_side(left_frames, right_frames, fps_left, fps_right, out_mp4, height):
    fps_left = _positive(fps_left, 'fps_left')
    fps_right = _positive(fps_right, 'fps_right')
    if isinstance(height, bool) or not isinstance(height, int) or height <= 0 or height % 2:
        raise ValueError('height must be a positive even integer for yuv420p')
    sides = []
    for frames in (left_frames, right_frames):
        source = [_rgb(im) for im in _frames(frames)]
        width = max(1, round(source[0].width*height/source[0].height))
        sides.append([im.resize((width, height), Image.Resampling.LANCZOS) for im in source])
    left, right = sides
    fps = max(fps_left, fps_right)
    count = math.ceil(max(len(left)/fps_left, len(right)/fps_right)*fps - 1e-9)
    size = (left[0].width + right[0].width, height)
    def images():
        for i in range(count):
            im = Image.new('RGB', size, BACKGROUND)
            im.paste(left[math.floor(i*fps_left/fps + 1e-9) % len(left)], (0, 0))
            im.paste(right[math.floor(i*fps_right/fps + 1e-9) % len(right)], (left[0].width, 0))
            yield im
    return _encode(images(), fps, out_mp4, size)


def seam_pairs_png(frames, out_png):
    """Last | first | absolute RGB difference amplified 4x (clipped at 255).

    RGB is composited on the review background, so invisible RGB contributes
    nothing. This diagnostic raster does not replace any numerical seam gate.
    """
    source = _frames(frames)
    last, first = _rgb(source[-1]), _rgb(source[0])
    difference = np.abs(np.asarray(last).astype(np.int16)-np.asarray(first).astype(np.int16))
    diff = Image.fromarray(np.minimum(difference*4, 255).astype(np.uint8))
    out = Image.new('RGB', (last.width*3, last.height))
    for i, im in enumerate((last, first, diff)):
        out.paste(im, (i*last.width, 0))
    path = Path(out_png); path.parent.mkdir(parents=True, exist_ok=True); out.save(path)
    return path


def strip_png(frames, out_png, numbered=True):
    source = [_rgb(im) for im in _frames(frames)]
    w, h = source[0].size
    header = 20 if numbered else 0
    out = Image.new('RGB', (w*len(source), h+header), BACKGROUND)
    draw = ImageDraw.Draw(out)
    for i, im in enumerate(source):
        out.paste(im, (i*w, header))
        if numbered:
            draw.text((i*w+4, 3), str(i), fill='white')
    path = Path(out_png); path.parent.mkdir(parents=True, exist_ok=True); out.save(path)
    return path
