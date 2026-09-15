# C-5 conductor glue: BEFORE/AFTER crop diff -> object bboxes -> 2x tiles on #00ff00 sheets (1536x1024) + layout.json + objiso briefs.
# usage: mk_objsheet_c5.py <tag> <before.png> <after.png> <crop_origin_x> <crop_origin_y>
import sys, json, os, pathlib
import numpy as np
from PIL import Image
from scipy import ndimage
tag, before, after, ox, oy = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
O = B/f'runs/C-5/artifacts/CS-objsheets-{tag}'; O.mkdir(parents=True, exist_ok=True)
a = np.asarray(Image.open(before).convert('RGB')).astype(int); b = np.asarray(Image.open(after).convert('RGB')).astype(int)
d = np.abs(a-b).sum(axis=2) > 60
d = ndimage.binary_opening(d, iterations=2); d = ndimage.binary_dilation(d, iterations=6); d = ndimage.binary_fill_holes(d)
lab, n = ndimage.label(d); objs = []
for i in range(1, n+1):
    ys, xs = np.where(lab == i)
    if len(ys) < 900: continue
    x0, y0, x1, y1 = int(xs.min()), int(ys.min()), int(xs.max())+1, int(ys.max())+1
    m = 12; x0, y0 = max(0, x0-m), max(0, y0-m); x1, y1 = min(b.shape[1], x1+m), min(b.shape[0], y1+m)
    objs.append({'id': f'{tag}_{len(objs)+1:02d}', 'crop_box': [x0, y0, x1, y1], 'area_px': int(len(ys)), 'level_xy': [ox+x0, oy+y0]})
objs.sort(key=lambda o: (o['crop_box'][1]//256, o['crop_box'][0]))
# pack 2x tiles into 1536x1024 sheets, simple shelf packing
SW, SH, SC = 1536, 1024, 2; sheets = []; cur = None
def new_sheet():
    global cur; cur = {'img': Image.new('RGB', (SW, SH), (0, 255, 0)), 'x': 8, 'y': 8, 'row_h': 0, 'tiles': []}; sheets.append(cur)
new_sheet()
after_img = Image.open(after).convert('RGB')
for o in objs:
    x0, y0, x1, y1 = o['crop_box']; tw, th = (x1-x0)*SC, (y1-y0)*SC
    if tw > SW-16 or th > SH-16:
        SC2 = min((SW-16)/(x1-x0), (SH-16)/(y1-y0)); tw, th = int((x1-x0)*SC2), int((y1-y0)*SC2); o['scale'] = round(SC2, 3)
    else: o['scale'] = SC
    if cur['x'] + tw > SW-8: cur['x'] = 8; cur['y'] += cur['row_h'] + 8; cur['row_h'] = 0
    if cur['y'] + th > SH-8: new_sheet()
    tile = after_img.crop((x0, y0, x1, y1)).resize((tw, th), Image.LANCZOS)
    cur['img'].paste(tile, (cur['x'], cur['y'])); o['sheet'] = len(sheets); o['sheet_xy'] = [cur['x'], cur['y']]; o['sheet_size'] = [tw, th]
    cur['tiles'].append(o['id']); cur['x'] += tw + 8; cur['row_h'] = max(cur['row_h'], th)
for k, s in enumerate(sheets, 1): s['img'].save(O/f'objsheet_{tag}_{k}.png')
json.dump({'tag': tag, 'before': before, 'after': after, 'crop_origin': [ox, oy], 'objects': objs, 'sheets': len(sheets)}, open(O/f'objsheet_{tag}_layout.json', 'w'), indent=1)
print('objects', len(objs), 'sheets', len(sheets)); [print(' ', o['id'], o['crop_box'], o['area_px']) for o in objs]
# objiso briefs (GENERATE, edit mode), one per sheet
for k in range(1, len(sheets)+1):
    ids = [o['id'] for o in objs if o['sheet'] == k]
    text = (f'GENERATE BURST CS-objiso-{tag}-{k} — ISOLATE painted training dummies from their own scene crops (Run C-5 P0-a; the props method, Matt R-C3-61/64). task_id "CS-objiso-{tag}-{k}".\n\n'
            f'IMAGE 1 (1536×1024) is a sheet of {len(ids)} tiles on flat PURE GREEN #00ff00. Each tile is an enlargement of a crop from a hand-painted 2D ARPG level, showing a static straw-and-timber training dummy standing on sunlit dirt or grass (some tiles may hold two dummies or a dummy plus a stray stone).\n'
            'Use image_gen in EDIT mode on IMAGE 1 and deliver ONE 1536×1024 image in which EVERYTHING that is ground — dirt, path texture, pebbles lying on the ground, grass, and every cast/contact SHADOW on the ground — is replaced by flat PURE GREEN #00ff00, and every DUMMY stays EXACTLY as painted: same pixels, same position in the sheet, same size, same outline, same colours and lighting, including its post, base, ropes and any straw touching the ground. Where a base met the ground, finish its bottom edge cleanly (no ground strip, no shadow). Nothing new is added; nothing moves.\n'
            'The green must be one flat colour everywhere with a crisp edge against each dummy (no halo, no glow, no blur).\n\n'
            'One image_gen call. ONE retry only if a dummy moved, was resized or redrawn differently, ground/shadow remains attached to a dummy, or the green is not flat — name the reason. '
            f'Copy the output from $CODEX_HOME/generated_images/... to out/objiso_{tag}_{k}.png with sha256. No code. No other files. No web.\n'
            f'RETURN: the receipt (task_id "CS-objiso-{tag}-{k}"): files = [out/objiso_{tag}_{k}.png with sha256]; images = the INTEGER COUNT of image_gen calls made (1 or 2) — NOT a list, and NEVER a path under $CODEX_HOME/generated_images (a discarded attempt is not referenced anywhere in the receipt); calls_used; status DELIVERED / DELIVERED_WITH_CONCERNS with concerns listed honestly.')
    task = {'text': text, 'references': [{'path': str(O/f'objsheet_{tag}_{k}.png'), 'role': 'IMAGE 1 — sheet of dummy tiles to isolate (EDIT)'}], 'image_cap': 2, 'minutes_cap': 15, 'tool_call_cap': 20, 'outputs': [f'out/objiso_{tag}_{k}.png'], 'effort': 'high', 'add_dirs': [], 'experiment': 'C5-P0a'}
    json.dump(task, open(B/f'briefs/C-5/CS-objiso-{tag}-{k}.task.json', 'w'), indent=1, ensure_ascii=False); print('brief', f'CS-objiso-{tag}-{k}', ids)
