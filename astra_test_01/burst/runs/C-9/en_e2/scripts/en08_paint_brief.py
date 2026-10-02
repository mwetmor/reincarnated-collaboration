# EN-E2 painted-texture briefs (D7's SOP-A / SOP-B via wl_e1's e07, re-worded for the acolytes). View words GENERATED from the
# layout rects (never typed by hand). The canvas is staged into CS9-guides + its manifest (the refs_guard rule, as e07 does).
#   python3 en08_paint_brief.py <m|f> A <canvas.png>            -> EN2-<G>PA
#   python3 en08_paint_brief.py <m|f> B <canvas.png> <A_paint>  -> EN2-<G>PB
import json, sys, os, hashlib, shutil, pathlib
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); import importlib; B = importlib.import_module('en01_briefs')
G, NAME, CANVAS = sys.argv[1], sys.argv[2], sys.argv[3]
L = json.load(open(os.path.join(ROOT, "work", "layout_%s%s.json" % (G, NAME))))
P = dict(m=("his", "him", "he", "man"), f=("her", "her", "she", "woman"), w=("its", "it", "it", "figure"), r=("its", "it", "it", "figure"), b=("its", "it", "it", "figure"), c=("his", "him", "he", "man"), i=("its", "it", "it", "figure"), g=("its", "it", "it", "figure"), n=("its", "it", "it", "figure"), y=("its", "it", "it", "figure"), v=("its", "it", "it", "figure"), s=("its", "it", "it", "figure"), o=("its", "it", "it", "figure"))[G]
WORD = dict(S="FACING THE VIEWER (south)", N="seen from BEHIND (north)", E="facing the viewer's RIGHT in profile (east)",
            W="facing the viewer's LEFT in profile (west)", SE="facing the lower right (south-east)", SW="facing the lower left (south-west)",
            NE="facing away to the upper right (north-east)", NW="facing away to the upper left (north-west)",
            face_S="a CLOSE-UP of %s HEAD from the front" % P[0], face_SE="a CLOSE-UP of %s head from the lower right, three-quarter" % P[0])
mid = L["canvas"][1] / 2; rows = {"Top": [], "Bottom": []}
for k, c in L["cells"].items():
    x, y, w, h = c["rect"]; rows["Top" if y + h / 2 < mid else "Bottom"].append((x, k))
desc = " ".join("%s row, left to right: %s." % (rn, "; ".join(WORD[k] for _, k in sorted(rows[rn]))) for rn in ("Top", "Bottom"))
GD = pathlib.Path(B.A) / "CS9-guides"; dst = GD / ("en2_%s_canvas_%s.png" % (G, NAME)); shutil.copy(CANVAS, dst)
man = json.load(open(GD / "manifest.json")); man[dst.name] = hashlib.sha256(dst.read_bytes()).hexdigest()
json.dump(man, open(GD / "manifest.json", "w"), indent=1)
TID = dict(m="EN2-M", f="EN2-F", w="EN2-W", r="EN2-R", b="EN2-B", c="EN2-C", i="EN2-I", g="EN2-G", n="EN2-N", y="EN2-Y", v="EN2-V", s="EN2-S", o="EN2-O")[G]
PICK = dict(m="a", f="a", w="b", r="a", b="b_r1", c="a", i="b", g="a", n="a", y="a", v="a", s="a", o="a")[G]   # round 3: the wraith's sheet of record is b
LOOK = dict(path=B.A + "%s/%s_%s.png" % (TID, TID, PICK), role="IMAGE %%d -- %s approved model sheet (%s_%s): the look" % (P[0], TID, PICK))
STY = dict(B.STYLE, role="IMAGE %d -- STYLE reference ONLY (Matt-supplied, R-C9-69): the HAND to copy; never its character, costume, hood, robe, staff or pose")
WHO = dict(
    m=("a possessed acolyte: a deep lapis-blue hood bound in tarnished brass, the face inside it a dim cool-grey hatched shadow with two small pale "
       "blue-white eyes; a faded lapis hooded robe over an ivory under-robe, split to the knee and ragged at the hem and cuffs, a plain cord belt; "
       "broken brass gear-wheels at the throat and hanging from the belt; dark grey-brown leggings and soft wrapped shoes; thin bare hands, pale "
       "grey-blue going to pale blue-white at the fingertips; and ONE broad BRASS BRACER engraved with an hour-ring on his LEFT forearm only"),
    f=("a possessed acolyte: an ashen grey-blue face, gaunt and calm, pale blue-white eyes with no pupils, long straight ash-grey hair, a thin tarnished "
       "brass circlet with a small broken clock-face at the brow; an ivory knee-length alb under a sleeveless lapis-blue chasuble bordered with faded "
       "brass hour-mark embroidery, ragged at the hems; a narrow lapis stole down the front with a broken brass gear near each end; dark grey "
       "leggings and soft wrapped shoes; thin bare hands, ashen grey-blue going to pale blue-white at the fingertips; and ONE cracked brass "
       "CLOCK-FACE disc hanging at her LEFT hip only"),
    w=("a wraith: a gaunt skull-like face of tight pale grey-blue skin with deep dark eye hollows and a small pale blue-white point in each, a thin dark mouth; "
       "a hooded burial SHROUD of torn ivory and pale lapis cloth over the head and shoulders, falling past the waist into a long ragged tail of strips "
       "(no legs, no feet); long thin pale grey-blue arms and long clawed hands with dark hooked nails; a rusted brass chain with a small cracked brass "
       "hour-medallion on the chest; and ONE torn strip of pale lapis cloth tied around its LEFT upper arm only"),
    r=("a revenant: a man-sized human SKELETON of old ivory-grey bone, dark empty eye sockets each with a small pale blue-white point, a ragged grey "
       "cowl around the neck and shoulders, a torn LAPIS tabard to mid-thigh with thin tarnished brass edging and a brass hour-ring disc on the chest, "
       "a cracked leather belt with a brass clock-face buckle, ragged grey cloth wrapped around the shins, bare bone hands and feet; and ONE BRASS "
       "BRACER ring around its LEFT forearm only"),
    b=("a flesh-warped brute: a hulking hunched body of swollen, stitched, sickly pale grey-violet flesh with darker violet-grey bruising and pale lapis veins; "
       "its RIGHT arm enormous (twice the left's thickness) ending in a huge three-fingered hand, its LEFT arm thin and sinewy; a large cracked brass gear-wheel "
       "fused into its LEFT shoulder, small brass gears and a bent clock hand along the spine, a broken brass hour-ring grown into the top of its head; "
       "torn lapis robe-tatters hanging from a cracked leather belt as a loincloth; bare feet with thick dark toenails; small pale blue-white eyes"),
    c=("a bog-wretch: a gaunt wiry hunched man, skin a sickly mud-grey-green streaked with dried mud and old blood, long matted dark hair and a ragged "
       "beard tangled with reeds; a ragged hide loincloth, a rope belt hung with small bones; filthy cloth wound round the shins; bare feet; a torn faded "
       "LAPIS sash across the chest from the right shoulder to the left hip with a cracked brass gear knotted into it; and ONE bracelet of knuckle-bones "
       "around his LEFT wrist only"),
    i=("a small corrupted imp: a wiry pot-bellied body of pale grey-violet skin with darker violet blotches, a large round head with two short curled "
       "dark horns and long pointed ears, small pale blue-white eyes and a wide mouth of needle teeth; a cracked brass gear-wheel embedded in its chest; "
       "a scrap of torn lapis cloth around its hips; long clawed fingers and toes; and ONE thin BRASS RING around its LEFT upper arm only"),
    g=("a crypt-mud golem: a hulking hunched body of packed wet dark grey-brown mud bound by twisted dark roots, old yellowed bones and skulls pressed "
       "into its chest, back and shoulders, thick green moss and pale lichen with small bone-white flowers over the shoulders and back, a rusted brass "
       "gear-wheel sunk in the chest, a bent clock hand and broken brass rods jutting from the back, huge blunt three-fingered hands, two small green "
       "points in the eye-pits; and ONE rusted BRASS CHAIN wrapped around its LEFT forearm only"),
    n=("a frost-gaunt: a tall emaciated horror, frost-pale grey-blue skin stretched over bone with every rib showing, long thin arms with long dark "
       "hooked claws, a long skull-like face with pale blue-white points in deep sockets, tatters of grey-brown fur hide over the shoulders and hips, two "
       "tall branching dark antlers crusted with frost; and its LEFT antler BROKEN OFF to a short jagged stump"),
    y=("an ice-brute: an enormous hunched shaggy beast, long thick dirty pale grey-white fur in heavy clumps, the bare skin of the face, chest, palms and "
       "soles a dark blue-grey, ice and hoarfrost matted into the shoulders and forearms, a small head with a heavy brow, small pale blue-white eyes, two "
       "short tusks and two short curved pale horns; and ONE broken rusted brass SHACKLE with dangling chain links on its LEFT wrist only"),
    v=("a towering void-touched horned lord: deep violet-indigo skin laid in layered washes with pale violet-grey highlights, cracked all over with "
       "thin pale violet-white seams, a long narrow bone skull-mask face with small pale violet-white eyes, two great ridged curling horns of dark bone, "
       "bone spines down the back and ragged bone plates on the shoulders, a broken brass hour-ring driven into the chest, a torn war-skirt of faded "
       "lapis Keeper banners on a heavy chain-and-brass belt, long clawed hands and clawed feet; and ONE heavy BRASS RING with a short broken chain "
       "clamped round its LEFT horn only"),
    s=("an animated temple statue: a tall armoured warrior carved in pale weathered grey stone, a domed helm with a blank face-plate and two shallow eye-slits, "
       "a breastplate with a sunken hour-ring inlaid in tarnished brass, layered carved shoulder plates, a carved stone tabard to the knee, carved greaves "
       "and sandalled feet, thin brass inlay along the edges, cracks and chips darker grey, pale green lichen and old water-stains; and ONE carved stone "
       "sundial fin rising from its LEFT shoulder plate only"),
    o=("a bone golem: a towering hunched construct of fused old ivory-grey bones, ribcages stacked into a barrel chest, long bones bundled into the limbs, "
       "skulls packed into the shoulders and back, bound with rusted brass bands and iron chain, tattered grey burial cloth, a horned skull head with "
       "pale blue-white points in the sockets; and ONE cracked brass bell on a short chain at its LEFT wrist only"))[G]
MARK = dict(m="THE BRASS BRACER is on his LEFT forearm ONLY", f="THE CLOCK-FACE DISC hangs at her LEFT hip ONLY",
            w="THE LAPIS CLOTH STRIP is tied around its LEFT upper arm ONLY", r="THE BRASS BRACER is on its LEFT forearm ONLY",
            b="THE SWOLLEN ARM is its RIGHT arm and THE BRASS GEAR is fused into its LEFT shoulder", c="THE BONE BRACELET is on his LEFT wrist ONLY",
            i="THE BRASS RING is on its LEFT upper arm ONLY", g="THE RUSTED CHAIN is wrapped around its LEFT forearm ONLY",
            n="THE BROKEN ANTLER STUMP is its LEFT antler ONLY", y="THE SHACKLE is on its LEFT wrist ONLY", v="THE BRASS RING is on its LEFT horn ONLY", s="THE SUNDIAL FIN is on its LEFT shoulder ONLY", o="THE BRASS BELL hangs at its LEFT wrist ONLY")[G]
SKIN = dict(m="", f="Her skin is ASHEN: a cold grey-blue, the colour of the dead, never warm or rosy (the conductor's note); ",
            w="Its skin is a cold pale grey-blue and the shroud is thin, pale and cold; ", r="The bone is old ivory-grey, cracked and stained darker in the joints; ",
            b="The flesh is sickly pale grey-violet, bruised and stitched, never a healthy pink; ",
            c="His skin is a bog-mud GREEN-GREY with algae and silt tones, darkest on the shins, feet and hands (the conductor's note), never a healthy tan; ",
            i="Its skin is a pale grey-violet with violet blotches, never pink; ", g="The mud is wet and dark, the moss a cool deep green; ",
            n="Its skin is a cold frost-blue-grey, never warm; ", y="The fur is a cool pale grey-white, never yellow; ",
            v="The violet skin is never a flat black: pale highlights on every ridge; ", s="The stone is pale and cool, never yellow; ", o="The bone is old ivory-grey, stained darker in the joints; ")[G]
RULES = ("Paint the SURFACE, not the lighting: soft even light; no cast shadows, no dark side, no rim light, no glow, no shading that belongs to one "
         "viewpoint. " + SKIN + "The darks are hatching and layered transparent washes with pale paper highlights, never a flat black fill. Brass is a "
         "tarnished ochre-brown wash with pale highlights. Stay inside every outline; change no outline, pose, hand or foot. Add NOTHING the look sheet "
         "does not show: no staff, no book, no weapon, nothing held.\n" + MARK + ", exactly where IMAGE 1 shows it; never on the right side.\n")
TAIL = ("BACKGROUND: keep the background flat pure #00ff00, as in IMAGE 1. If the image model returns a darker or gradient background anyway, DO NOT spend a retry "
        "on it and still deliver the image: the figures are cut out afterwards by their exact 3D outlines. Spend retries ONLY on the faults named below.\n\n"
        "Two image_gen EDIT calls: variants a and b. ONE retry per variant only if a view's outline, pose, facing or position changed, a view is missing, the "
        "figure differs between views, the brass marker is on the wrong side or missing, something is added that the look sheet does not show, or a head "
        "close-up is a different face -- name the reason. Never retry for the background colour. Copy outputs to out/{t}_a.png and out/{t}_b.png with sha256. "
        "No code. No other files. No web.\n"
        "RETURN: receipt task_id \"{t}\"; images = the files with prompt, references (role + path) and elapsed_s; calls_used = the TRUE number of image_gen calls; "
        "status; concerns. Never PASS/FAIL.")
if NAME == "A":
    T = TID + "PA"
    text = ("GENERATE BURST {t} -- Run C-9 Phase 2 (Matt, R-C9-132/133): the PAINTED TEXTURE of a 3D enemy for the cathedral arena, sheet 1 of 2. task_id \"{t}\".\n\n"
            "IMAGE 1 is a sheet of TEN renders of ONE 3D model standing in a relaxed A-pose, on flat pure #00ff00. " + desc +
            " They are renders of the model: every OUTLINE, POSE, POSITION and SIZE is correct and must not change; the surface is flat and too smooth.\n"
            "IMAGE 2 is the approved model sheet: " + WHO + ". IMAGE 3 is a STYLE reference ONLY: copy its HAND (the ink line that varies in weight, "
            "transparent watercolour washes that pool and granulate, fine hatching, cream paper highlights); copy nothing else from it.\n"
            "Use image_gen in EDIT mode on IMAGE 1 and deliver ONE 1536x1024 sheet in which EVERY figure is repainted as the figure of IMAGE 2 seen from that "
            "direction, in IMAGE 3's hand, inside exactly that view's outline, position and size.\n"
            "THIS PAINTING BECOMES THE MODEL'S TEXTURE: it is projected back onto the 3D model from these ten cameras and blended into one texture. So: ONE "
            "figure in ten views, not ten figures -- the same cloth, brass, hands and shoes in every view; any disagreement between views becomes a seam.\n"
            + RULES + "THE TWO HEAD CLOSE-UPS are the identity: the same head as IMAGE 2, larger. More detail is welcome; a different face or hood is not.\n"
            + TAIL).format(t=T)
    refs = [dict(path=str(dst), role="IMAGE 1 -- the sheet to EDIT (8 body views at 19.77 deg + 2 head close-ups of the rigged 3D model at rest; outlines correct, surface flat)"),
            dict(LOOK, role=LOOK['role'] % 2), dict(STY, role=STY['role'] % 3)]
else:
    T = TID + "PB"; APAINT = sys.argv[4]
    text = ("GENERATE BURST {t} -- Run C-9 Phase 2 (Matt, R-C9-132/133): the PAINTED TEXTURE of a 3D enemy for the cathedral arena, sheet 2 of 2, at the GAME "
            "CAMERA (looking down at 53 degrees). task_id \"{t}\".\n\n"
            "IMAGE 1 is the SAME FIGURE, ALREADY PAINTED, seen from the game's own camera looking steeply down: its painted surface (from IMAGE 2) projected onto "
            "the 3D model and re-rendered from above. " + desc + " Every OUTLINE, POSE, CROP and CAMERA in IMAGE 1 is fixed and must not change.\n"
            "IMAGE 2 is the painting IMAGE 1 was made from (sheet 1, the same figure from ten low angles). IMAGE 3 is the approved model sheet (the look): " + WHO +
            ". IMAGE 4 is a STYLE reference ONLY: copy its HAND, never its character, clothing or staff.\n"
            "Use image_gen in EDIT mode on IMAGE 1 and deliver ONE 1536x1024 sheet.\n"
            "REPAINT THIS SURFACE; DO NOT PAINT A NEW VIEW. Everything already drawn in IMAGE 1 stays exactly where it is, at the same size and shape: the "
            "brass pieces, the belt, the hems and borders, the hair or hood. A feature drawn in a different place becomes a double. What this pass is FOR: the "
            "surfaces a steep camera sees properly and a low one only grazed -- the tops of the shoulders, the crown of the head or hood, the upper back, the "
            "tops of the forearms and shoes. Give them the detail and the hand of IMAGE 2 and IMAGE 4; leave everything else as found, only cleaner.\n"
            + RULES + TAIL).format(t=T)
    refs = [dict(path=str(dst), role="IMAGE 1 -- the sheet to EDIT (sheet A paint projected onto the rigged 3D model, re-rendered at 52.95 deg; outlines, crops and cameras fixed)"),
            dict(path=APAINT, role="IMAGE 2 -- the painting IMAGE 1 was made from (sheet A, chosen by registration)"),
            dict(LOOK, role=LOOK['role'] % 3), dict(STY, role=STY['role'] % 4)]
B.lane_guard(text); [B.lane_guard(r['role']) for r in refs]
task = dict(text=text, references=refs, image_cap=4, minutes_cap=15, tool_call_cap=20, outputs=["out/%s_a.png" % T, "out/%s_b.png" % T],
            effort='high', add_dirs=[], experiment='R-C9-132-crucible-enemies')
p = B.BURST / ('briefs/C-9/%s.task.json' % T); assert not p.exists(), p
p.write_text(json.dumps(task, indent=1, ensure_ascii=False) + '\n'); print('wrote', p); print(desc)
