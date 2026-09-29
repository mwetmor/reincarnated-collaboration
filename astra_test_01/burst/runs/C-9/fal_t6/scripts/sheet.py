# T6 contact-sheet builder. Rows = models (Meshy baseline first), columns =
# directions. Mid-grey ground behind the figures -- NOT green -- so a dark ink
# edge still reads against the background.
import os
from PIL import Image, ImageDraw, ImageFont

BG = (128, 128, 128)
PANEL = (108, 108, 112)
INK = (18, 18, 20)
LBL = (245, 245, 245)


def _font(sz):
    for p in ('/System/Library/Fonts/Supplemental/Arial Bold.ttf',
              '/System/Library/Fonts/Supplemental/Arial.ttf',
              '/System/Library/Fonts/Helvetica.ttc'):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, sz)
            except Exception:
                pass
    return ImageFont.load_default()


def sheet(rows, cols, cell_path, out, title='', cell=512, lblw=210, hdr=46):
    """rows: [(row_label, row_key)]  cols: [(col_label, col_key)]
    cell_path(row_key, col_key) -> png path or None"""
    W = lblw + cell * len(cols)
    H = hdr + cell * len(rows)
    im = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(im)
    f_h = _font(max(15, cell // 22))
    f_r = _font(max(14, cell // 26))
    f_t = _font(max(17, cell // 20))
    d.rectangle([0, 0, W, hdr], fill=(38, 38, 42))
    if title:
        d.text((10, 8), title, font=f_t, fill=LBL)
    for j, (cl, _) in enumerate(cols):
        x = lblw + j * cell
        d.text((x + 8, hdr - 22), cl, font=f_h, fill=LBL)
    for i, (rl, rk) in enumerate(rows):
        y = hdr + i * cell
        d.rectangle([0, y, lblw - 1, y + cell - 1], fill=(38, 38, 42))
        for k, line in enumerate(rl.split('\n')):
            d.text((8, y + 10 + k * (f_r.size + 4)), line, font=f_r, fill=LBL)
        for j, (_, ck) in enumerate(cols):
            x = lblw + j * cell
            d.rectangle([x, y, x + cell - 1, y + cell - 1], fill=PANEL)
            p = cell_path(rk, ck)
            if p and os.path.exists(p):
                c = Image.open(p).convert('RGBA')
                if c.size != (cell, cell):
                    c = c.resize((cell, cell), Image.LANCZOS)
                bgp = Image.new('RGBA', (cell, cell), PANEL + (255,))
                im.paste(Image.alpha_composite(bgp, c).convert('RGB'), (x, y))
            else:
                d.text((x + cell // 2 - 22, y + cell // 2), 'n/a', font=f_r, fill=(200, 90, 90))
            d.rectangle([x, y, x + cell - 1, y + cell - 1], outline=INK)
    im.save(out)
    return im.size
