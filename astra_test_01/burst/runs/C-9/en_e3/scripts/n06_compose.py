# Compose rendered cells into one labelled sheet (system python; called by n05_render.py).
import json, sys
from PIL import Image, ImageDraw
S = json.load(open(sys.argv[1])); cells = [Image.open(p).convert('RGBA') for p in S['cells']]
w, h = cells[0].size; cols = S['cols']; rows = (len(cells) + cols - 1) // cols; T = 28
out = Image.new('RGB', (cols * w, rows * (h + 18) + T), (236, 230, 218)); d = ImageDraw.Draw(out)
d.text((8, 8), S['title'], fill=(30, 30, 30))
for i, (c, lab) in enumerate(zip(cells, S['labels'])):
    x, y = (i % cols) * w, T + (i // cols) * (h + 18)
    out.paste(c, (x, y + 18), c); d.text((x + 4, y + 3), lab, fill=(60, 40, 30)); d.rectangle([x, y, x + w - 1, y + h + 17], outline=(190, 180, 165))
out.save(S['out']); print('sheet', S['out'], out.size)
