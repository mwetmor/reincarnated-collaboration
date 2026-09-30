# Count white speckles at the play camera from beauty + ID stills.
#   python3 scripts/s11_count.py <dir> <tag>
#
# HOLE pixel     the ID pass shows BODY (red) and at least 6 of its 8 neighbours are GARMENT
#                (blue): the body seen through a hole in a garment. Geometric; texture and
#                lighting cannot change it.
# SPECKLE        a hole pixel that is PALE in the beauty pass (min channel > 170): the dot you see.
# OWN WHITES     pale pixels inside her silhouette that are NOT hole pixels -- the linen seen
#                through the robe's real front opening, the cream border runes. These are the
#                texture's own whites and are reported, never counted as defects.
import glob, json, os, re, sys
import numpy as np
from PIL import Image
from scipy import ndimage
D, TAG = sys.argv[1], sys.argv[2]
rows = {}
for idp in sorted(glob.glob(os.path.join(D, "%s_*_id.png" % TAG))):
    bp = idp.replace("_id.png", "_beauty.png")
    I = np.asarray(Image.open(idp).convert('RGB')).astype(int)
    B = np.asarray(Image.open(bp).convert('RGB')).astype(int)
    body = (I[..., 0] > 200) & (I[..., 1] < 60) & (I[..., 2] < 60)
    garm = (I[..., 2] > 200) & (I[..., 0] < 60) & (I[..., 1] < 60)
    sil = I.sum(-1) > 90
    k = np.ones((3, 3)); k[1, 1] = 0
    enclosed = ndimage.convolve(garm.astype(int), k, mode='constant') >= 6
    hole = body & enclosed
    pale = B.min(-1) > 170
    m = re.search(r"%s_(.+?)_h(\d+)_s(\d+)_id\.png$" % re.escape(TAG), idp)
    # KEYED BY CLIP TOO. The first version keyed "h25 s1" etc., so with two clips in a run the
    # second clip's stills OVERWROTE the first's and the printed totals were one clip's only.
    key = "%s h%s s%s" % (m.group(1), m.group(2), m.group(3))
    # ISOLATED components (the speckle as a DOT). The per-pixel 6-of-8 rule also fires on the APEX
    # of a real V-shaped opening -- the robe's front split narrows to a one-pixel point, and every
    # rasterised apex is enclosed -- and on one-pixel notches of a real opening's edge. A dot is a
    # SMALL patch of visible body with garment on (nearly) every side and NOT connected to an
    # opening: 8-connected body component <= MAXC px at this scale, and >= 75% of the pixels
    # bordering it are garment.
    sc = int(m.group(3)); MAXC = 6 * sc * sc
    lab, n = ndimage.label(body, np.ones((3, 3)))
    iso = np.zeros_like(body)
    if n:
        sizes = ndimage.sum(body, lab, range(1, n + 1))
        for ci in np.nonzero(sizes <= MAXC)[0] + 1:
            cm = lab == ci
            ring = ndimage.binary_dilation(cm, np.ones((3, 3))) & ~cm
            if ring.sum() and (garm & ring).sum() / ring.sum() >= 0.75:
                iso |= cm
    # A dot within 2 px (x scale) of a DESIGNED OPENING -- a body region larger than the dot limit,
    # e.g. the robe's front split -- is that opening's rasterised edge or apex: a V tip breaks into
    # disconnected pixels at any resolution. It is the texture's own white seen through the design,
    # and is reported apart from the defect count, never dropped silently.
    big = np.isin(lab, (np.nonzero(sizes > MAXC)[0] + 1)) if n else np.zeros_like(body)
    near_open = ndimage.binary_dilation(big, np.ones((3, 3)), iterations=2 * sc)
    edge_frag = iso & near_open
    iso = iso & ~near_open
    # SLIT FRAGMENTS (pass 2, at the true play scale). A split robe seen edge-on shows its underdress
    # as a LINE, and a one-pixel-wide line rasterises into a chain of 1-3 px pieces, each of which
    # passes the dot test above. Pieces within 2*sc px of each other are chained; a chain whose body
    # pixels together exceed the dot limit is a slit -- the costume's opening -- not a speckle. It
    # is reported apart, never dropped, and s11_dots.py gives each remaining piece its 3D evidence.
    chain, nch = ndimage.label(ndimage.binary_dilation(body & ~big, np.ones((3, 3)), iterations=sc), np.ones((3, 3)))
    slit = np.zeros_like(iso)
    if nch:
        csz = ndimage.sum(body & ~big, chain, range(1, nch + 1))
        slit = iso & np.isin(chain, np.nonzero(csz > MAXC)[0] + 1)
    iso = iso & ~slit
    rows[key] = dict(silhouette_px=int(sil.sum()), hole_px=int(hole.sum()),
                     speckle_px=int((hole & pale).sum()),
                     isolated_hole_px=int(iso.sum()), isolated_speckle_px=int((iso & pale).sum()),
                     opening_edge_fragments_pale_px=int((edge_frag & pale).sum()),
                     slit_fragments_pale_px=int((slit & pale).sum()),
                     own_whites_px=int((sil & pale & ~iso).sum()))
tot = {k: sum(r[k] for r in rows.values()) for k in ("hole_px", "speckle_px", "isolated_hole_px", "isolated_speckle_px", "opening_edge_fragments_pale_px", "slit_fragments_pale_px", "own_whites_px")}
for s_ in ("1", "2"):
    ss = {k: sum(r[k] for kk, r in rows.items() if kk.endswith("s" + s_)) for k in tot}
    print("  %sx  per-pixel: holes %4d, pale %3d  |  ISOLATED DOTS: holes %4d, PALE %3d  |  opening-edge pale %2d, slit pale %2d  |  own whites %5d"
          % (s_, ss["hole_px"], ss["speckle_px"], ss["isolated_hole_px"], ss["isolated_speckle_px"],
             ss["opening_edge_fragments_pale_px"], ss["slit_fragments_pale_px"], ss["own_whites_px"]))
json.dump(dict(per_still=rows, totals=tot), open(os.path.join(D, "%s_counts.json" % TAG), "w"), indent=1)
