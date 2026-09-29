"""Contact sheets for the stance/block pass: rows = before/after per scenario, six frames each,
chosen where the change lives (the fade-in for strikes; press, raise, peak, hold, lower for the
block; evenly through the loop for the idle). Frames are pulled from the MP4s -- no frame dumps."""
import subprocess, sys, os, tempfile
from PIL import Image, ImageDraw, ImageFont
DEST = sys.argv[1]
FONT = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 28)
W, H = 640, 360
def grab(p, idx, tmp):
    o = os.path.join(tmp, "g.png")
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", p, "-vf", "select=eq(n\\,%d),scale=%d:%d" % (idx, W, H), "-frames:v", "1", o])
    return Image.open(o).copy()
def nfr(p):
    return int(subprocess.check_output(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
        "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", p]).strip())
SHEETS = {
  "contact_task1_idle_and_strikes.jpg": [("idle", None), ("slash_from_idle", 48), ("bash_from_idle", 48)],
  "contact_task2_block.jpg": [("block_from_idle", 48), ("block_from_run", 96)],
}
for sheet, rows in SHEETS.items():
    task = "task1" if "task1" in sheet else "task2"
    items = []
    for name, lead in rows:
        for mode in ["before", "after"]:
            p = os.path.join(DEST, "%s_%s_%s.mp4" % (task, mode, name))
            if not os.path.exists(p): continue
            n = nfr(p)
            if lead is None:
                idx = [int(n * f) for f in (0.08, 0.25, 0.42, 0.58, 0.75, 0.92)]
            elif "block" in name:
                idx = [lead - 4, lead + 6, lead + 12, lead + 18, lead + 100, lead + 144 + 14]
            else:
                idx = [lead - 4, lead + 3, lead + 6, lead + 9, lead + 12, lead + 40]
            items.append(("%s  %s" % (mode.upper(), name.replace("_", " ")), p, [max(0, min(n - 1, i)) for i in idx]))
    img = Image.new("RGB", (W * 6, (H + 40) * len(items)), (18, 18, 20))
    d = ImageDraw.Draw(img)
    with tempfile.TemporaryDirectory() as tmp:
        for r, (lab, p, idx) in enumerate(items):
            y = r * (H + 40)
            d.text((10, y + 5), "%s   (frames %s of the quarter-speed film)" % (lab, idx), font=FONT,
                   fill=(255, 210, 120) if lab.startswith("BEFORE") else (140, 230, 160))
            for c, i in enumerate(idx):
                img.paste(grab(p, i, tmp), (c * W, y + 40))
    out = os.path.join(DEST, sheet); img.save(out, quality=88); print(out, img.size)
