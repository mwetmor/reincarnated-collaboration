"""Find item-tooltip frames by their rarity-coloured title text.
GD item tooltips title in rarity colour: magic=yellow-green, rare=green,
epic=blue, legendary=purple. The character window itself carries none of
these hues in text, so a count of rarity-hue text pixels separates
tooltip-bearing frames cleanly."""
import csv
from pathlib import Path
import numpy as np
from PIL import Image

SRC = Path("/Volumes/reincarnated/visual-artifacts/GD-matt-test/play-test-v1/screenshots")
OUT = Path("/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-28-gd-playtest-v1-g6")
REG = (480, 240, 1150, 820)

det = []
with open(OUT/"g6-window-detect.csv") as f:
    for r in csv.DictReader(f):
        if float(r["charpaper"]) > 0.80:
            det.append(int(r["id"]))

rows = []
for i in det:
    with Image.open(SRC/f"Screenshot ({i}).png") as im:
        a = np.asarray(im.convert("RGB").crop(REG)).astype(np.int16)
    r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]
    green = ((g > 140) & (g - r > 45) & (g - b > 45)).sum()
    blue  = ((b > 150) & (b - r > 60) & (b - g > 30)).sum()
    rows.append((i, int(green), int(blue)))

rows.sort(key=lambda t: -t[1])
print("top green-title frames (id, green_px, blue_px):")
for t in rows[:30]:
    print(f"  f{t[0]:4d}  {t[1]:6d}  {t[2]:5d}")
with open(OUT/"g6-itemtip-scan.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["id","green_px","blue_px"]); w.writerows(rows)
