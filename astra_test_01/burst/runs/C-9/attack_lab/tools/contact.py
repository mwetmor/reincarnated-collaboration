"""One contact sheet per action: rows BEFORE/AFTER x from idle/from run, six frames each,
two of them inside the fade-in -- which is where the lurch lives. Frames are pulled
straight from the MP4s (no frame dumps kept) and composed with a row label."""
import subprocess, sys, os, tempfile
from PIL import Image, ImageDraw, ImageFont
DEST = sys.argv[1]
FONT = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 30)
LEAD = {"idle": 48, "run": 96}
TAIL = 48
W, H = 640, 360

def nframes(p):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
                                   "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", p])
    return int(out.strip())

def grab(p, idx, tmp):
    o = os.path.join(tmp, "g.png")
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", p, "-vf",
                           "select=eq(n\\,%d),scale=%d:%d" % (idx, W, H), "-frames:v", "1", o])
    return Image.open(o).copy()

for act in ["slash", "chop", "bash", "block"]:
    rows = []
    for frm in ["idle", "run"]:
        for mode in ["before", "after"]:
            p = os.path.join(DEST, "%s_%s_from_%s.mp4" % (mode, act, frm))
            if not os.path.exists(p):
                continue
            n = nframes(p)
            L = LEAD[frm]
            a = n - L - TAIL
            idx = [L - 4, L + 5, L + 10, L + int(a * 0.45), n - TAIL - 14, n - TAIL + 22]
            idx = [max(0, min(n - 1, i)) for i in idx]
            rows.append(("%s  from %s" % (mode.upper(), frm), p, idx))
    if not rows:
        continue
    sheet = Image.new("RGB", (W * 6, (H + 44) * len(rows)), (18, 18, 20))
    d = ImageDraw.Draw(sheet)
    with tempfile.TemporaryDirectory() as tmp:
        for r, (lab, p, idx) in enumerate(rows):
            y = r * (H + 44)
            d.text((10, y + 6), "%s   (frames %s of the quarter-speed film)" % (lab, idx), font=FONT,
                   fill=(255, 210, 120) if lab.startswith("BEFORE") else (140, 230, 160))
            for c, i in enumerate(idx):
                sheet.paste(grab(p, i, tmp), (c * W, y + 44))
    out = os.path.join(DEST, "contact_%s.jpg" % act)
    sheet.save(out, quality=90)
    print(out, sheet.size)
