#!/usr/bin/env python3
"""C-9 BV2F ARENA (R-C9-391/394): BUNDLE the arena's outside inputs INTO a mirror project (web_arena/), verified.

Copied, never referenced (an export cannot follow a symlink or an absolute path):
  * the KC2 runtime -- reincarnated-godot/kc2_runtime, BY DIGEST: tree digest re-derived by MANIFEST.json's own law
    and = the pin a0e75469..., every member sha256 checked at the SOURCE, copied, every member checked again in the COPY
    (kc2_play/tools/vendor.py's law, its functions imported read-only; reincarnated-godot is not written)
  * the model pack of record -- reincarnated-engine output, the same law against MODEL_DIGEST (997117...)
  * the V1-JOIN-1 leech table (R-C9-394 path shim input), sha cb6a008b... at source and copy
  * the crucible geometry (sha 68d895d7...), the NUM-POP font, the eor3 matrix, the eor4x GLB, v1's snow tile -- as raw
    *.bin / json, their sha256 recorded
  * the JOIN-1 kits the ten waves draw (data/arena/wave_kits.json) + the hero kits: every strip at HALF size as lossy
    WebP (q82) named *.webp.bin, each kit's index.json rewritten for the half size (cell px, anchors, stage_scale), the
    join1_index.json copied; kits grouped into KIT PACKS of <= 40 MB (the 50 MB file fence) by the first wave they appear
Writes <mirror>/kc2/bundle/BUNDLE_STAMP.json (what the running arena verifies at launch: scripts/arena/arena_paths.gd).
usage: python3 tools/arena_bundle.py <mirror godot dir>"""
import hashlib, importlib.util, io, json, os, shutil, sys
from PIL import Image

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_GODOT = os.path.join(HERE, "godot")
DST = os.path.abspath(sys.argv[1])
RT_SRC = "/Users/admin/Games/reincarnated-godot/kc2_runtime"
RT_PIN = "a0e75469a78b3b81d979d9d525e0bbf1c5324459260c62110192878c33a53f1c"
PACK_SRC = "/Users/admin/Games/reincarnated-engine/src/reincarnated/output/kc2-model-pack-v3-E-s09-cp150-mech-v3p11-20261002_192143"
PACK_PIN = "997117278c1e28dac0da9a6cf64ddaf72111347094a7ac5e3b4c03590507d788"
LEECH_SRC = "/Users/admin/Games/reincarnated-engine/data/kc2/pm4p_leech_resistance.csv"
LEECH_PIN = "cb6a008bde1e102573181968ab7f60958cd28fee07ff8736078fa092a80dd62e"
GEOM_SRC = "/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/notes/crucible-arena-geometry-v1.json"
GEOM_PIN = "68d895d75702996473cfd654a9a834816d4be0421c4b5ad7a3d2a0cc5d40481f"
JOIN1 = "/Users/admin/Games/reincarnated-godot/kc2_play/art/join1"
ART_X = os.path.join(SRC_GODOT, "kc2", "art_x")
FILES = {   # bundle name -> source (raw bytes; their sha recorded)
    "Bangers-Regular.ttf.bin": "/Users/admin/Games/reincarnated-godot/Assets/fonts/bangers/Bangers-Regular.ttf",
    "gd-eor-warlord-eor3_matrix_index.json": "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/join1_pack/gd-eor-warlord-eor3/matrix_index.json",
    "eor4x_wl_body.glb.bin": "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/wl_e1/export/final_k_eor4x/wl_body.glb",
    "v1_snow.png.bin": "/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst/runs/C-9/cliffside3d/godot/textures/barrow/snow.png",
}
HALF = 0.5
Q = 82
PACK_MB = 40.0


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def die(msg):
    sys.exit("BUNDLE ABORT: " + msg)


def vendor_tree(src, dst, man_name, key, pin):
    """verify (tree, every member) -> copy -> verify the copy; returns the member count"""
    man = json.load(open(os.path.join(src, man_name)))
    lines = ["%s  %s" % (m["path"], m["sha256"]) for m in sorted(man["members"], key=lambda m: m["path"])]
    tree = hashlib.sha256("\n".join(lines).encode()).hexdigest()
    if tree != man[key] or tree != pin:
        die("%s tree %s != manifest %s / pin %s" % (src, tree, man[key], pin))
    for m in man["members"]:
        if sha(os.path.join(src, m["path"])) != m["sha256"]:
            die("%s member %s at source" % (src, m["path"]))
    if os.path.lexists(dst):
        if os.path.islink(dst):
            os.unlink(dst)
        else:
            shutil.rmtree(dst)
    os.makedirs(dst)
    shutil.copy2(os.path.join(src, man_name), os.path.join(dst, man_name))
    for m in man["members"]:
        d = os.path.join(dst, m["path"])
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(os.path.join(src, m["path"]), d)
    for m in man["members"]:
        if sha(os.path.join(dst, m["path"])) != m["sha256"]:
            die("%s member %s in the COPY" % (dst, m["path"]))
    return len(man["members"])


def stage_kit(src_dir, dst_dir):
    """half-size WebP strips + the rewritten index; returns bytes written"""
    idx = json.load(open(os.path.join(src_dir, "index.json")))
    os.makedirs(dst_dir, exist_ok=True)
    total = 0
    done = {}
    for cid, c in idx.get("cells", {}).items():
        f = c["file"]
        if f not in done:
            im = Image.open(os.path.join(src_dir, f)).convert("RGBA")
            w, h = max(1, round(im.width * HALF)), max(1, round(im.height * HALF))
            im = im.resize((w, h), Image.LANCZOS)
            b = io.BytesIO()
            im.save(b, "WEBP", quality=Q, method=4)
            nm = os.path.splitext(f)[0] + ".webp.bin"
            open(os.path.join(dst_dir, nm), "wb").write(b.getvalue())
            total += b.tell()
            done[f] = nm
        c["file"] = done[f]
        for k in ("fw", "fh"):
            if k in c:
                c[k] = float(c[k]) * HALF
        if "anchor_px" in c:
            c["anchor_px"] = [float(v) * HALF for v in c["anchor_px"]]
    idx["stage_scale"] = float(idx.get("stage_scale", 0.5)) * HALF
    idx["_bundle"] = "R-C9-391: strips at %.2f size as lossy WebP q%d (*.webp.bin); cell px and anchors scaled" % (HALF, Q)
    json.dump(idx, open(os.path.join(dst_dir, "index.json"), "w"), indent=1, sort_keys=True)
    return total + os.path.getsize(os.path.join(dst_dir, "index.json"))


def main():
    if not os.path.isfile(os.path.join(DST, "project.godot")):
        die("no project.godot in " + DST)
    kc2 = os.path.join(DST, "kc2")
    bdir = os.path.join(kc2, "bundle")
    os.makedirs(bdir, exist_ok=True)
    gi = os.path.join(kc2, ".gdignore")
    if os.path.exists(gi):
        os.remove(gi)                     # the mirror's kc2/ must be visible to the export
    stamp = {"_what": "R-C9-391 bundle stamp (tools/arena_bundle.py); verified at launch by scripts/arena/arena_paths.gd",
             "runtime_tree_digest": RT_PIN, "model_pack_digest": PACK_PIN, "files": {}}
    stamp["runtime_members"] = vendor_tree(RT_SRC, os.path.join(kc2, "kc2_runtime"), "MANIFEST.json", "tree_digest", RT_PIN)
    stamp["model_pack_members"] = vendor_tree(PACK_SRC, os.path.join(kc2, "model_pack"), "manifest.json", "pack_digest", PACK_PIN)
    for nm, src, pin in (("pm4p_leech_resistance.csv.bin", LEECH_SRC, LEECH_PIN),
                         ("crucible-arena-geometry-v1.json", GEOM_SRC, GEOM_PIN)):
        if sha(src) != pin:
            die("%s at source != pin" % src)
        shutil.copy2(src, os.path.join(bdir, nm))
        if sha(os.path.join(bdir, nm)) != pin:
            die("%s copy != pin" % nm)
        stamp["files"][nm] = pin
    for nm, src in FILES.items():
        shutil.copy2(src, os.path.join(bdir, nm))
        stamp["files"][nm] = sha(os.path.join(bdir, nm))
        if stamp["files"][nm] != sha(src):
            die(nm + " copy")
    # ---- the art ----
    wk = json.load(open(os.path.join(SRC_GODOT, "data", "arena", "wave_kits.json")))
    art = os.path.join(kc2, "art")
    if os.path.isdir(art):
        shutil.rmtree(art)
    os.makedirs(art)
    shutil.copy2(os.path.join(JOIN1, "join1_index.json"), os.path.join(art, "join1_index.json"))
    order, first = [], {}
    for w in sorted(wk["waves"], key=int):
        for k in wk["waves"][w]:
            if k not in first:
                first[k] = int(w)
                order.append(k)
    heroes = [wk["hero"], "gd-eor-warlord-eor4x"]
    sizes = {}
    for k in heroes + order:
        src = os.path.join(ART_X, k) if os.path.isdir(os.path.join(ART_X, k)) else os.path.join(JOIN1, k)
        if not os.path.isfile(os.path.join(src, "index.json")):
            die("kit %s has no index at %s" % (k, src))
        sizes[k] = stage_kit(src, os.path.join(art, k))
        print("   kit %-28s %6.1f MB" % (k, sizes[k] / 1e6))
    # the art_x variant copy is now in kc2/art; the mirror's own art_x would be imported PNGs -- drop it
    ax = os.path.join(kc2, "art_x")
    if os.path.isdir(ax):
        shutil.rmtree(ax)
    # kit packs, by first appearance, each <= PACK_MB (the heroes ride in the first)
    packs, cur, cur_b = [], [], 0
    for k in heroes + order:
        if cur and cur_b + sizes[k] > PACK_MB * 1e6:
            packs.append(cur)
            cur, cur_b = [], 0
        cur.append(k)
        cur_b += sizes[k]
    if cur:
        packs.append(cur)
    stamp["kit_packs"] = ["kits_%d.pck" % i for i in range(len(packs))]
    stamp["kit_pack_members"] = {"kits_%d.pck" % i: p for i, p in enumerate(packs)}
    stamp["kit_mb"] = {k: round(v / 1e6, 2) for k, v in sizes.items()}
    json.dump(stamp, open(os.path.join(bdir, "BUNDLE_STAMP.json"), "w"), indent=1)
    print("bundled: runtime %d members (tree %s), model pack %d members (%s), %d kits %.1f MB in %d packs" % (
        stamp["runtime_members"], RT_PIN[:12], stamp["model_pack_members"], PACK_PIN[:12], len(sizes),
        sum(sizes.values()) / 1e6, len(packs)))


main()
