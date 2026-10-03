# MX audition (R-C9-149): compose the per-side 1x play-scale films (film/<tag>_<side>.mp4, 960x540 each, identical step
# durations per state) into ONE side-by-side film with a label bar over each pane (PIL label PNG; this ffmpeg has no drawtext).
# 2 sides: 1x2; 3: 1x3; 4: 2x2; 5: 3+2 (2x3 grid, last cell blank). Pane 0 = the clip of record (or the idle fallback).
#   python3 scripts/mx08_sbs.py <tag> <out.mp4>
import sys, os, json, glob, subprocess
from PIL import Image, ImageDraw, ImageFont
tag, OUT = sys.argv[1], sys.argv[2]; S = json.load(open('specs/%s.json' % tag))
n = len(glob.glob('film/%s_[0-9].mp4' % tag)); F = ImageFont.load_default(size=22)
labels = []
for s in range(n):
    names = [st[1 + s] if s + 1 < len(st) and st[1 + s] else ('(no clip of record: idle)' if s == 0 else '(no candidate: idle)') for st in S['pairs']]
    lab = ('RECORD: ' if s == 0 else 'MIXAMO %d: ' % s) + ' / '.join(names)
    im = Image.new('RGB', (960, 40), (30, 30, 50) if s == 0 else (90, 30, 20)); ImageDraw.Draw(im).text((10, 8), lab[:80], fill=(255, 255, 255), font=F)
    p = 'work/_label_%s_%d.png' % (tag, s); im.save(p); labels.append(p)
args = ['ffmpeg', '-y', '-loglevel', 'error']
for s in range(n): args += ['-i', 'film/%s_%d.mp4' % (tag, s)]
for s in range(n): args += ['-i', labels[s]]
fc = ''.join('[%d:v][%d:v]vstack=inputs=2[p%d];' % (n + s, s, s) for s in range(n))
if n == 2: fc += '[p0][p1]hstack=inputs=2[o]'
elif n == 3: fc += '[p0][p1][p2]hstack=inputs=3[o]'
elif n == 4: fc += '[p0][p1][p2][p3]xstack=inputs=4:layout=0_0|w0_0|0_h0|w0_h0[o]'
else:
    fc += 'color=c=black:s=960x580:d=60[bk];[p0][p1][p2][p3][p4][bk]xstack=inputs=6:layout=0_0|w0_0|w0+w1_0|0_h0|w0_h0|w0+w1_h0:shortest=1[o]'
args += ['-filter_complex', fc, '-map', '[o]', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', OUT]
subprocess.run(args, check=True); print('wrote', OUT, n, 'panes')
