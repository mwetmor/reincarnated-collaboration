# T8 step 3: compose the eight facings of a rendered cycle into one contact
# sheet per frame and encode STRAIGHT TO MP4 through a pipe, then delete the
# frames. Nothing uncompressed is left behind -- the frames exist only while
# the video is being written, and the directory is removed at the end.
#
#   python3 scripts/16_encode_cycle.py <framedir> <out.mp4> <title>
import json, os, shutil, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw

SRC, OUT, TITLE = sys.argv[1], sys.argv[2], sys.argv[3]
info = json.load(open(os.path.join(SRC, "info.json")))
FAC, N = info["facings"], info["frames"]
R = info["res"]
COLS, TOP, LBL = 4, 22, 14
W, H = R * COLS, TOP + (R + LBL) * 2
proc = subprocess.Popen(
    ["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-vcodec", "png",
     "-r", str(info["fps"]), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p",
     "-crf", "18", "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2", OUT],
    stdin=subprocess.PIPE)
for i in range(N):
    sheet = Image.new("RGB", (W, H), (250, 249, 247))
    d = ImageDraw.Draw(sheet)
    d.text((8, 6), "%s   frame %02d/%02d" % (TITLE, i + 1, N), fill=(25, 25, 25))
    for k, f in enumerate(FAC):
        r, c = divmod(k, COLS)
        im = Image.open(os.path.join(SRC, "%s_%03d.png" % (f, i))).convert("RGBA")
        bg = Image.new("RGBA", im.size, (250, 249, 247, 255))
        bg.alpha_composite(im)
        y = TOP + r * (R + LBL)
        sheet.paste(bg.convert("RGB"), (c * R, y + LBL))
        d.text((c * R + 5, y + 1), f, fill=(90, 90, 90))
    sheet.save(proc.stdin, "PNG")
proc.stdin.close()
rc = proc.wait()
assert rc == 0, "ffmpeg exited %d" % rc
mb = os.path.getsize(OUT) / 1e6
shutil.rmtree(SRC)
print("wrote %s (%.2f MB, %d frames at %s fps); deleted %d frames from %s"
      % (OUT, mb, N, info["fps"], N * len(FAC), SRC))
