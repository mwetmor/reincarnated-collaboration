# EN-E2 round 3 (conductor, 2026-10-02): two more crucible enemies, model sheets first.
#   EN2-W  -> roster tier-1 #2 `wraith` (15.5 bodies): a FLOATING undead spirit; melee 49 / aura 19 / aoe 14 / projectile 12 %
#   EN2-R  -> roster tier-1 #14 `skeleton_01a` (revenants, 5.0 bodies): an elemental revenant skeleton; projectile 63 / aoe 22 / aura 14 %
# Original to our world (the Keepers of Hours' desecrated cathedral). Generic descriptors only; en01's lane_guard + refs_guard.
import json, sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
B = __import__('en01_briefs')

WRAITH = """THE CHARACTER, a WRAITH of the cathedral: the spirit of a dead servant of the order, HOVERING above the floor (it never touches it):
- a gaunt, hunched, elongated upper body about as tall as a man from the crown down to the waist; a long narrow skull-like face, the skin stretched tight and a pale grey-blue, deep dark eye hollows with a small cold blue-white point of light in each, the mouth a thin dark slit;
- a tattered grey-and-pale-lapis HOODED SHROUD (thin, torn burial cloth) over the head and shoulders, falling past the waist and narrowing below it into a long RAGGED TAIL of torn strips and wisps that ends in thin points about a hand's width ABOVE the ground line; NO legs and NO feet anywhere: the body simply ends in the trailing shroud;
- the shroud's tail hangs STRAIGHT DOWN and SYMMETRIC, as a narrow column below the waist (a little wider than the hips at most), so the figure's outline is a man's torso and arms above a tapering column;
- long thin bare ARMS with long CLAWED hands: four long fingers ending in dark hooked nails; the skin of the arms and hands the same pale grey-blue;
- a few rusted BRASS links of a broken chain around the neck, one small cracked brass hour-medallion hanging from it on the chest;
- ASYMMETRY MARKER: a long torn STRIP of pale lapis cloth tied around the LEFT upper arm ONLY, its loose end hanging to the elbow; the right arm is bare. It shows in every view where the left upper arm is visible, and never on the right;
- the cold light is painted as PALE COLOUR (pale blue-white) in the eye points only, never as a glow.
"""
REVENANT = """THE CHARACTER, a REVENANT: the SKELETON of a dead Keeper of the order, risen and walking:
- a man-sized human SKELETON standing upright, natural proportions, about seven and a half heads tall; old bone, ivory-grey with darker brown-grey in the joints and cracks; a skull with dark empty eye sockets, each with a small pale blue-white point of light (painted as pale colour, never a glow); the jaw closed;
- the remains of his ceremonial dress: a short torn tabard of faded LAPIS cloth over the ribcage, falling to mid-thigh front and back in two ragged panels, belted at the waist with a cracked leather belt and a BRASS buckle shaped as a small clock-face; tattered strips of grey cloth wrapped around both shins; a short ragged grey cowl around the neck and shoulders (the skull is bare);
- BRASS TRIM: thin tarnished brass edging along the tabard's hems and a brass hour-ring disc on the tabard's chest;
- the bones of the arms, hands, legs and feet clearly visible and separate (open spaces between the forearm bones, between the ribs only in shadow, the legs two clear bony columns): ONE solid skeleton, no missing parts, no broken-off limbs;
- ASYMMETRY MARKER: a BRASS BRACER ring around the LEFT forearm ONLY; the right forearm is bare bone. It shows in every view where the left forearm is visible, and never on the right;
- NOTHING in the hands: no staff, no weapon, no book; nothing held. No fire, no glow, no lightning drawn anywhere: the elemental light is added later.
"""

def text(tid, who, char, pose_extra, retry_extra, marker_name):
    return ("GENERATE BURST %s -- Run C-9 Phase 2 (Matt, R-C9-132/133): a NEW ENEMY for the same world as the acolytes already built: %s MODEL "
            "SHEET for a 3D model. task_id \"%s\".\n\n"
            "WHY this sheet exists (so you can judge your own result): a 3D model will be BUILT from these four views, then rigged and animated. The four "
            "views must agree exactly, as four views of ONE figure. Many copies will fill an arena, so the silhouette must read clearly from above at a small size.\n\n"
            "IMAGE 1 is a STYLE reference ONLY: copy its HAND (the varying dark ink line, the transparent watercolour washes that pool, granulate and bloom, the "
            "fine hatching, the cream paper highlights, the moderate colour). Copy NOTHING else from it. IMAGE 2 is our own earlier sheet: copy its LAYOUT only "
            "(grid, views, pose, scale); never its figure.\n\n" + B.WORLD + char +
            "\nSTYLE: the REGISTER CARD above governs line, washes, light and plate: no glow, no rim light, no large black areas; the darks are hatching and "
            "layered washes, never a flat black fill. Brass is a tarnished ochre-brown wash with pale highlights.\n"
            "SHEET: ONE 1024x1536 PORTRAIT sheet on flat pure #00ff00 in a 2x2 grid: the SAME figure in four views at the SAME scale, each view centred in its "
            "quarter, each figure filling most of its quarter's height. Top-left FRONT (facing the viewer); top-right its RIGHT SIDE (in profile, facing the "
            "viewer's right); bottom-left BACK (seen from behind); bottom-right its LEFT SIDE (in profile, facing the viewer's left).\n"
            "POSE (for building and rigging a 3D model): a relaxed A-POSE. Both arms straight and held AWAY from the body at about 30 degrees, so that in the "
            "front and back views a clear gap of green shows between each arm and the torso. Hands OPEN: fingers together and straight, palms facing inward. "
            "Head level, facing the same way as the body. Nothing overlaps anything. " + pose_extra + "\n"
            "Soft even light; no cast shadows, no ground, no text, no labels, no cell borders, no other figures.\n"
            "BACKGROUND: flat pure #00ff00. If the image model returns a darker or gradient background anyway, still deliver the image.\n\n"
            "Two image_gen calls: variants a and b. ONE retry per variant only if the figure DRIFTS between views, a view is missing or faces the wrong way, the "
            "%s is on the RIGHT side or missing, an arm touches the body in the front or back view, " + retry_extra + " or anything is held in the hands -- "
            "name the reason. Copy the outputs to out/%s_a.png and out/%s_b.png (a retry to out/%s_a_r1.png / out/%s_b_r1.png) with sha256. No code. No "
            "other files. No web.\n"
            "RETURN: receipt task_id \"%s\"; images = the files with prompt, references (role + path) and elapsed_s; calls_used = the TRUE number of image_gen "
            "calls; status; concerns. Never PASS/FAIL.") % (tid, who, tid, marker_name, tid, tid, tid, tid, tid)

if __name__ == '__main__':
    B.write('EN2-W', text('EN2-W', 'ITS', WRAITH,
                          "The figure FLOATS: the tips of its shroud-tail hang about a hand's width above an imagined ground line, the same height in all four views. "
                          "The tail hangs straight down, never blown sideways.",
                          "legs or feet appear, the tail touches the ground or flows to one side,", 'cloth strip on the upper arm'),
            [B.STYLE, B.LAYOUT], ['out/EN2-W_a.png', 'out/EN2-W_b.png'], 4)
    B.write('EN2-R', text('EN2-R', 'ITS', REVENANT,
                          "Legs straight, feet a little apart and pointing forward, soles on one ground line per row; a clear gap of green between the legs.",
                          "a bone or limb is missing, fire or lightning is drawn,", 'brass bracer'),
            [B.STYLE, B.LAYOUT], ['out/EN2-R_a.png', 'out/EN2-R_b.png'], 4)
