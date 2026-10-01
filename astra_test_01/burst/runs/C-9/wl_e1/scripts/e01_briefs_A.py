# E1 (third character, R-C9-112/113) stage A: two armoured model sheets (A1 long cape, A2 shoulder cape) + one weapon sheet.
# Prompt hygiene: generic descriptors only (no franchise/game/character/item/artist name); lane_guard() adds names
# refs_guard's FORBID list does not carry (it is conductor-owned; we do not edit it).
import json, pathlib, re, sys
BURST = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
A = str(BURST / 'runs/C-9/artifacts') + '/'
LANE_FORBID = re.compile(r'golbez|final\s*fantasy|square|grim\s*dawn|crate|gutsmasher|warborn|eye\s*of\s*reckoning|\beor\b|'
                         r'sandreaver|solael|windshear|vire|empyrion|oleron|kaisan|deathstalker|amano|yoshitaka|warlord', re.I)
def lane_guard(t):
    m = LANE_FORBID.search(t)
    assert not m, 'lane guard: forbidden token %r' % m.group(0)

STYLE = dict(path=A + 'inputs/nb_style_ref_matt.png',
             role="STYLE reference ONLY (Matt-supplied, R-C9-69): the HAND to copy; never its character, costume, staff or pose")
LAYOUT = dict(path=A + 'CS9-guides/SO-1_b_harvest.png',
              role="SHEET reference (our own earlier sheet): the 2x2 grid, the four views, A-pose, one scale and ground lines; never her body, face, hair or clothing")
PLATE = dict(path=A + 'GS-SBM/GS-SBM_a.png',
             role="PLATE-ARMOUR reference (our own earlier sheet): how steel plate is painted in this hand (ink line, hatching, washes); never its design, colours, helmet or wearer")

KNIGHT = """THE CHARACTER, a towering sorcerous DARK KNIGHT (a man):
- TALL, ELONGATED and ELEGANT: about eight and a half heads tall, long legs, a narrow waist, a lean commanding silhouette rather than a bulky one; he stands straight and still;
- FULL PLATE ARMOUR from head to foot, NEAR-BLACK steel with a deep VIOLET-INDIGO sheen in the washes, edged and traced with FINE GOLD FILIGREE (thin scrolling lines along the plate edges, never large gold areas);
- a closed HELM with a full face-concealing VISOR: no face, skin or hair shows anywhere; a narrow horizontal EYE SLIT with a FAINT violet glow inside it; two long dark HORNS sweep back and up from the helm's sides, the same in every view;
- TALL, FLARING, LAYERED PAULDRONS: three overlapping lames on each shoulder rising to a point above the shoulder line and flaring outward, the same on both shoulders;
- a sculpted breastplate with a narrow waist, a plated fauld over the hips, segmented arm plates, articulated gauntlets, plated legs and pointed sabatons;
- ASYMMETRY MARKER: a broad GOLD filigree band around his LEFT forearm plate ONLY; his RIGHT forearm plate is plain dark steel. The band shows in every view where his left forearm is visible, and never on the right;
- NOTHING in his hands and nothing at his belt: no weapon, no mace, no sword, no shield, no scabbard.
"""

def sheet_text(tid, cape):
    return ("GENERATE BURST %s -- Run C-9 Phase 2 (Matt R-C9-112/113): a NEW character for the same world as the barbarian and the sorceress "
     "already built: his MODEL SHEET for a 3D model. task_id \"%s\".\n\n"
     "WHY this sheet exists (so you can judge your own result): a 3D model will be BUILT from these four views, then rigged and animated. "
     "The four views must agree exactly, as four views of ONE figure.\n\n"
     "IMAGE 1 is a STYLE reference ONLY: copy its HAND (the varying ink line, the transparent watercolour washes that pool, granulate and bloom, "
     "the fine hatching in the shadows, the cream paper highlights). Copy nothing else from it. IMAGE 2 is our own earlier sheet: copy its LAYOUT "
     "only (grid, views, pose, scale). IMAGE 3 is our own earlier sheet: it shows how PLATE ARMOUR is painted in this hand; copy nothing of its design.\n\n"
     + KNIGHT + cape +
     "\nSTYLE: delicate dark ink line with SOFT, BLEEDING WATERCOLOUR WASHES, as IMAGE 1. The register card's palette clause (no large black areas, gold only "
     "on sacred objects, no glow) is SET ASIDE for this figure's armour by Matt's ruling R-C9-113: the plate IS near-black with a violet-indigo sheen, the gold is "
     "fine filigree, and the eye slit has a faint glow. Keep the paper highlights: the dark plate is laid as layered transparent washes with pale highlights "
     "on its edges, never a flat black fill or a glossy render.\n"
     "SHEET: ONE 1024x1536 PORTRAIT sheet on flat pure #00ff00 in a 2x2 grid: the SAME knight in four views at the SAME scale, each view centred in its quarter, "
     "soles on one ground line per row, each figure (horns included) filling most of its quarter's height. Top-left FRONT (facing the viewer); top-right his RIGHT "
     "SIDE (in profile, facing the viewer's right); bottom-left BACK (seen from behind); bottom-right his LEFT SIDE (in profile, facing the viewer's left).\n"
     "POSE (for building and rigging a 3D model): a relaxed A-POSE. Both arms straight and held AWAY from the body at about 30 degrees, so that in the front and "
     "back views a clear gap of green shows between each arm and the torso AND between each arm and the cape. Hands OPEN: fingers together and straight, palms "
     "facing the thighs. Legs straight, feet a little apart and pointing forward. Head level, facing the same way as the body. Nothing overlaps anything.\n"
     "Soft even light; no cast shadows, no ground, no text, no labels, no cell borders, no other figures.\n"
     "BACKGROUND: flat pure #00ff00. If the image model returns a darker or gradient background anyway, still deliver the image.\n\n"
     "ONE image_gen call. ONE RETRY ONLY if the result DRIFTS between views (the knight differs between views: helm, horns, pauldrons, cape or the gold band "
     "change), a view is missing or faces the wrong way, the gold band is on the RIGHT forearm or missing, an arm touches the torso in the front or back view, "
     "a face or skin shows, or a weapon or shield appears -- name the reason and deliver BOTH images. Copy the output to out/%s.png (a retry to out/%s_r1.png) "
     "with sha256. No code. No other files. No web.\n"
     "RETURN: receipt task_id \"%s\"; images = the files with prompt, references (role + path) and elapsed_s; calls_used = the TRUE number of image_gen calls; "
     "status; concerns. Never PASS/FAIL.") % (tid, tid, tid, tid, tid)

CAPE_A1 = """- a LONG DARK CAPE (deep indigo-black cloth, a thin gold border), fastened under the pauldrons, falling to just above the ANKLES. It is designed to be CUT INTO PANELS for 3D: ONE broad BACK PANEL hanging straight down behind him, plus a LEFT and a RIGHT side panel hanging behind each arm; the panels are separated by two clear vertical SLITS running from the hem up to the hips. The cape hangs FREE of the legs: in both side views a clear gap of green shows between the back of his legs and the cape, all the way down; in the front view only its edges show behind him, outside the legs.
"""
CAPE_A2 = """- a SHORT DARK CAPE (deep indigo-black cloth, a thin gold border) fastened under the pauldrons, hanging only to the SHOULDER BLADES (no lower than the bottom of the shoulder blades), stiff and close to the back; it never reaches the waist.
"""

MACE = ("GENERATE BURST DK-MACE -- Run C-9 Phase 2 (Matt R-C9-112/113): the dark knight's TWO-HANDED SPIKED MACE as a MODEL SHEET for 3D. task_id \"DK-MACE\".\n\n"
 "IMAGE 1 is a STYLE reference ONLY (the hand: ink line, transparent washes, hatching); copy nothing else. IMAGE 2 is our own earlier weapon sheet: copy its LAYOUT only "
 "(three orthographic views side by side at one scale, butt on one ground line); never its weapon's design.\n"
 "Deliver ONE 1536x1024 sheet on flat pure #00ff00 showing ONE object alone (no hands, no person, no strap), in THREE orthographic views side by side, all at ONE common "
 "scale, the butt on one ground line near the bottom edge, the top near the top edge, nothing overlapping. LEFT the mace FRONT-ON; MIDDLE turned 90 degrees; RIGHT turned 180 degrees.\n"
 "THE MACE, a towering knight's two-handed weapon, ornate:\n"
 "- the HEAD: a heavy DARK IRON flanged-and-spiked mace head, an elongated bulb about 230 pixels tall and 150 pixels wide (spikes included), ringed by eight flanges, "
 "each ending in a short sharp spike, one longer spike on top; FINE GOLD FILIGREE traced along every flange edge; a gilded collar where the head meets the haft;\n"
 "- the HAFT: a slim, straight, round two-handed haft of the same dark iron, about 34 pixels thick (NEVER thicker than a fifth of the head's width), long enough for TWO hands "
 "with room between them: from the underside of the head down to the butt about 3.2 head-heights (about 740 pixels); a DARK LEATHER-wrapped grip section at the butt "
 "(about 170 pixels long) and a second at mid-haft (about 150 pixels long), each bounded by thin gold rings; a small spiked iron pommel at the butt;\n"
 "- the whole mace about 990 pixels tall. Proportion check before you deliver: the head is about a QUARTER of the whole length; the haft below the head is about THREE head-heights.\n"
 "Paint in IMAGE 1's hand: near-black iron laid as layered transparent washes with a deep violet sheen and pale paper highlights on the edges, never a flat black fill; "
 "soft even light, no glow, no cast shadows, no ground, no text, no labels.\n"
 "BACKGROUND: flat pure #00ff00. If the image model returns a darker or gradient background anyway, still deliver the image.\n\n"
 "ONE image_gen call. ONE RETRY ONLY if the PROPORTIONS are off (the head larger than a third of the whole length, the haft below the head shorter than 2.5 head-heights, "
 "or the haft thicker than a fifth of the head) or the three views disagree -- name the reason and deliver BOTH images. Copy the output to out/DK-MACE.png (a retry to "
 "out/DK-MACE_r1.png) with sha256. No code. No other files. No web.\n"
 "RETURN: receipt task_id \"DK-MACE\"; images = the files with prompt, references (role + path) and elapsed_s; calls_used = the TRUE number of image_gen calls; status; concerns. Never PASS/FAIL.")

def write(tid, text, refs, outs):
    lane_guard(text); [lane_guard(r['role']) for r in refs]
    task = dict(text=text, references=refs, image_cap=2, minutes_cap=15, tool_call_cap=12, outputs=outs, effort='high', add_dirs=[],
                experiment='R-C9-112-third-character')
    p = BURST / ('briefs/C-9/%s.task.json' % tid)
    assert not p.exists(), p
    p.write_text(json.dumps(task, indent=1, ensure_ascii=False) + '\n'); print('wrote', p)

if __name__ == '__main__':
    write('DK-A1', sheet_text('DK-A1', CAPE_A1), [STYLE, LAYOUT, PLATE], ['out/DK-A1.png'])
    write('DK-A2', sheet_text('DK-A2', CAPE_A2), [STYLE, LAYOUT, PLATE], ['out/DK-A2.png'])
    write('DK-MACE', MACE, [dict(STYLE, role="IMAGE 1 -- " + STYLE['role']),
                            dict(path=A + 'GS-BMAUL2/GS-BMAUL2_a.png', role="IMAGE 2 -- LAYOUT reference (our own earlier weapon sheet): three views, one scale, one ground line; never its weapon's design")],
          ['out/DK-MACE.png'])
