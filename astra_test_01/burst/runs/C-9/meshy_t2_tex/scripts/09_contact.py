# Contact sheet from a directory of v_NN.png, on paper, with labels.
#   python3 scripts/09_contact.py <dir> <out.png> <cols> <title>
import os, sys, glob
from PIL import Image, ImageDraw
D, OUT, COLS, TITLE = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
fs = sorted(glob.glob(os.path.join(D, "v_*.png")))
ims = [Image.open(f).convert("RGBA") for f in fs]
w, h = ims[0].size
rows = (len(ims) + COLS - 1) // COLS
TOP = 26
sheet = Image.new("RGB", (w * COLS, TOP + rows * (h + 16)), (250, 249, 247))
dr = ImageDraw.Draw(sheet)
dr.text((8, 8), TITLE, fill=(25, 25, 25))
for i, im in enumerate(ims):
    r, c = divmod(i, COLS)
    bg = Image.new("RGBA", im.size, (250, 249, 247, 255))
    bg.alpha_composite(im)
    y = TOP + r * (h + 16)
    sheet.paste(bg.convert("RGB"), (c * w, y + 14))
    dr.text((c * w + 5, y + 2), os.path.basename(fs[i])[2:-4], fill=(90, 90, 90))
sheet.save(OUT)
print("wrote %s  %s  (%d frames)" % (OUT, sheet.size, len(ims)))
