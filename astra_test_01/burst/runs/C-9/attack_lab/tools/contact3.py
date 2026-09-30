"""Foot-lock contact sheets: per start state, rows = OFF/ON per action, frames through the
fade-in and the step that follows it (fire at frame LEAD; 4 film frames = one game frame)."""
import subprocess, sys, os, tempfile
from PIL import Image, ImageDraw, ImageFont
DEST = sys.argv[1]
FONT = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 28)
W, H = 640, 360
def grab(p, idx, tmp):
    o = os.path.join(tmp, "g.png")
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", p, "-vf", "select=eq(n\\,%d),scale=%d:%d" % (idx, W, H), "-frames:v", "1", o])
    return Image.open(o).copy()
for frm, lead in (("idle", 48), ("run", 96)):
    items = []
    for act in ("slash", "chop", "bash", "block"):
        for tag in ("before", "after"):
            p = os.path.join(DEST, "footlock_%s_%s_from_%s.mp4" % (tag, act, frm))
            if os.path.exists(p):
                items.append(("LOCK %s  %s from %s" % ("OFF" if tag == "before" else "ON", act, frm), p,
                              [lead - 2, lead + 6, lead + 12, lead + 20, lead + 28, lead + 40]))
    img = Image.new("RGB", (W * 6, (H + 40) * len(items)), (18, 18, 20))
    d = ImageDraw.Draw(img)
    with tempfile.TemporaryDirectory() as tmp:
        for r, (lab, p, idx) in enumerate(items):
            y = r * (H + 40)
            d.text((10, y + 5), "%s   (film frames %s; fire at %d, 4 frames = 1 game frame)" % (lab, idx, lead), font=FONT,
                   fill=(255, 210, 120) if "OFF" in lab else (140, 230, 160))
            for c, i in enumerate(idx):
                img.paste(grab(p, i, tmp), (c * W, y + 40))
    out = os.path.join(DEST, "contact_footlock_from_%s.jpg" % frm); img.save(out, quality=86); print(out, img.size)
