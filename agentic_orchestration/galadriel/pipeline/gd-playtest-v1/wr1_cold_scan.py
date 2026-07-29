"""Coarse cold-VFX energy scan (downscaled play-area, 30 fps) to locate nova candidates."""
import subprocess, sys, numpy as np, json
video = "/Users/admin/gd-scratch/play_test_2026-07-26.mp4"
ss, dur, out = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
FPS = 30
# play area only: native 0..1350 x 0..940 -> scaled /4
cmd = ["ffmpeg","-nostdin","-hide_banner","-loglevel","error","-ss",str(ss),"-i",video,
       "-t",str(dur),"-vf",f"fps={FPS},crop=1350:940:0:0,scale=337:235","-pix_fmt","rgb24",
       "-f","rawvideo","-"]
W,H = 337,235; n = W*H*3
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=n*8)
rows, i = [], 0
while True:
    b = p.stdout.read(n)
    if len(b) < n: break
    a = np.frombuffer(b, dtype=np.uint8).reshape(H,W,3).astype(np.int16)
    R,G,B = a[:,:,0],a[:,:,1],a[:,:,2]
    m = (B>140)&(B-R>55)&(B>=G-10)
    c = int(m.sum())
    if c:
        ys,xs = np.nonzero(m); rows.append((round(ss+i/FPS,3), c, round(float(xs.mean()),1), round(float(ys.mean()),1)))
    else:
        rows.append((round(ss+i/FPS,3), 0, -1, -1))
    i += 1
    if i % 9000 == 0: print(f"  {ss+i/FPS:.0f}s", file=sys.stderr, flush=True)
p.stdout.close(); p.wait()
json.dump(rows, open(out,"w")); print(len(rows))
