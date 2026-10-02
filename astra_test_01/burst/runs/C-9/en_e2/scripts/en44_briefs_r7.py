# EN-E2 round 7 (conductor, 2026-10-02): the REFERENT build list (legolas BUILD_PRIORITY.md), sheets first in one batch.
#   EN2-S  `possessedstatue` (2.4 bodies, w156): an animated Keeper temple STATUE (the body; its two-handed spear is a separate prop)
#   EN2-SP the statue's two-handed SPEAR (a prop sheet: three views, one scale)
#   EN2-O  `golembone_phase01` (w158 hero, ~1.0): a towering BONE GOLEM (moved from the creature lane)
#   EN2-H1 hero01_unarmed boss mesh: the w159 FINAL BOSS -- an armoured warden of the order
#   EN2-H2 hero01_unarmed boss mesh: the w160 VANGUARD NEMESIS -- an arch-magister caster
#   EN2-W1 heroine01_unarmed boss mesh: the w156 WITCH (the betrayer)
#   EN2-W2 heroine01_unarmed boss mesh: the w155 MIND-TAKER
# Boss meshes: ONE variant each (image budget), rigged on their own Meshy rigs, the built rig's clip set re-grafted (same method).
# Original to our world; generic descriptors only, never a record or source name (en01's lane_guard + refs_guard).
import sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
B = __import__('en01_briefs'); R3 = __import__('en23_briefs_r3')
A = B.A
STATUE = """THE CHARACTER, an ANIMATED TEMPLE STATUE: one of the Keepers' guardian statues from the cathedral's nave, carved to stand watch for ever, now walking:
- a tall armoured warrior carved in pale weathered GREY STONE, about one and a quarter times a man's height, broad and upright, heavy-limbed, perfectly still in its carving;
- carved armour: a smooth domed helm with a blank stone face-plate (two shallow eye-slits, no eyes), a breastplate carved with a sunken HOUR-RING inlaid in tarnished BRASS, layered carved shoulder plates, a carved tabard of stone falling to the knee front and back, carved greaves and sandalled stone feet;
- the stone is cracked and chipped at the edges, darker grey in the cracks, with patches of pale green lichen and old dark water-stains running down from the shoulders;
- thin tarnished brass inlay along the edges of the helm, breastplate and tabard;
- ASYMMETRY MARKER: a carved stone SUNDIAL FIN (a triangular gnomon) rising from its LEFT shoulder plate ONLY; the right shoulder plate is plain. It shows in every view where the left shoulder is visible, and never on the right;
- NOTHING in its hands (its spear is drawn separately); the hands are open, carved stone.
"""
GOLEM = """THE CHARACTER, a BONE GOLEM: a towering construct the ossuary built out of its own dead:
- HUGE: about one and a half times a man's height, a massive hunched body, a small skull-head low between huge shoulders, very long thick arms reaching to the knees with huge hands of fused finger-bones, short thick legs, broad feet;
- its whole body is FUSED BONES: ribcages stacked into a barrel chest, long bones bundled into the limbs like cords of wood, dozens of skulls packed into the shoulders and back, vertebrae chained down the spine; the bone old ivory-grey to yellowed, darker brown-grey in the joints and gaps;
- bound together with bands of rusted BRASS and old iron chain wound around the limbs and torso; tattered strips of grey burial cloth caught between the bones;
- the head: a large horned skull (two short broken horns), dark empty eye sockets each with a small pale blue-white point (painted as pale colour, never a glow);
- ASYMMETRY MARKER: a cracked BRASS BELL hanging on a short chain from its LEFT wrist ONLY; the right wrist has none. It shows in every view where the left wrist is visible, and never on the right;
- NOTHING held in the hands.
"""
WARDEN = """THE CHARACTER, the WARDEN OF HOURS, a BOSS: the order's last armoured champion, hollowed out and filled with something cold, still guarding the dead cathedral:
- TALL and imposing: about one and a quarter times a man's height, broad-shouldered, upright, a commander's stance;
- full heavy PLATE ARMOUR of tarnished BRASS with deep LAPIS-blue enamel panels, engraved with hour-marks; a great helm whose visor is a CLOCK-FACE (a brass ring of numerals around a dark slit), two thin pale blue-white points of light behind it (painted as pale colour, never a glow);
- a long torn LAPIS tabard over the armour to the knee, front and back, embroidered with a brass hour-ring; a tattered ivory half-cape from the right shoulder only;
- a round brass CLOCK-FACE SHIELD strapped to its LEFT FOREARM as part of the armour (the left hand is empty below it) -- this is also the ASYMMETRY MARKER: it is on the LEFT forearm ONLY, in every view;
- armoured gauntlets with open hands, NOTHING held.
"""
MAGISTER = """THE CHARACTER, the HOLLOW ARCH-MAGISTER, a BOSS: the order's highest scholar-mage, risen from the archive vaults, a caster of terrible power:
- TALL and gaunt: about one and a fifth times a man's height, upright and severe, long-limbed;
- layered ceremonial ROBES: an ivory under-robe to the ankle (split to the knee at the sides so the legs move), a deep LAPIS over-robe with a tall stiff collar rising behind the head, broad brass-embroidered bands of star-charts and hour-marks along every hem;
- the face: a long pale grey-blue face with hollow cheeks, a long thin white beard, pale blue-white eyes (painted as pale colour, never a glow); on the head a CROWN of broken brass ASTROLABE RINGS standing up in a tall open lattice;
- a heavy brass chain of office across the shoulders with a large engraved disc on the chest;
- ASYMMETRY MARKER: a palm-sized brass ASTROLABE DISC bound into the palm of its LEFT HAND ONLY with brass straps around the wrist (part of the costume; nothing is held); the right hand is bare. It shows in every view where the left hand is visible, never on the right;
- NOTHING else held.
"""
WITCH = """THE CHARACTER, the BETRAYER WITCH, a BOSS: a seeress of the order who sold it to the dark, now its high priestess:
- a tall woman, about one and a tenth times a man's height, slender, upright, imperious;
- flowing ritual ROBES of deep MADDER-red and faded ivory, layered and torn, falling to the knee in ragged points (the legs move free below), a high open collar of stiff bone-ivory lace behind the head; a corset of dark leather laced with brass;
- the face: pale grey skin, a BONE-WHITE HALF-MASK over the upper face carved with an hour-ring, a cold mouth; long loose SILVER-GREY hair to the waist behind;
- strings of small brass HOURGLASSES and bone beads hanging from the belt and wrists;
- ASYMMETRY MARKER: a carved BONE HAND (an open skeletal hand) fixed as a pauldron on her LEFT shoulder ONLY; the right shoulder is bare robe. It shows in every view where the left shoulder is visible, never on the right;
- NOTHING held in the hands.
"""
MINDTAKER = """THE CHARACTER, the MIND-TAKER, a BOSS: a gaunt sorceress who eats the memories of the dead:
- a tall, very thin woman, about one and a tenth times a man's height, upright, still;
- a long close gown of pale VIOLET-grey silk, torn into points at the knee (the legs move free below), wound with strips of faded LAPIS cloth around the waist and arms;
- the head: shaved, pale grey-violet skin, her EYES BOUND with a band of lapis cloth, a thin cruel mouth; a brass CIRCLET of long thin brass NEEDLES standing out around the skull like a crown of spines;
- long thin fingers ending in brass-capped nails;
- ASYMMETRY MARKER: a ring of brass NEEDLES (a spiked bracelet) around her LEFT WRIST ONLY; the right wrist is bare. It shows in every view where the left wrist is visible, never on the right;
- NOTHING held in the hands.
"""
SPEAR = ("GENERATE BURST EN2-SP -- Run C-9 Phase 2 (Matt, R-C9-132/133): the animated temple statue's TWO-HANDED SPEAR as a MODEL SHEET for 3D. task_id \"EN2-SP\".\n\n"
 "IMAGE 1 is a STYLE reference ONLY (the hand: ink line, transparent washes, hatching); copy nothing else. IMAGE 2 is our own earlier weapon sheet: copy its LAYOUT only "
 "(three orthographic views side by side at one scale, the butt on one ground line); never its weapon's design.\n"
 "Deliver ONE 1536x1024 sheet on flat pure #00ff00 showing ONE object alone (no hands, no person), in THREE orthographic views side by side, all at ONE common scale, "
 "the butt on one ground line near the bottom edge, the top near the top edge, nothing overlapping. LEFT the spear FRONT-ON (the blade's flat face); MIDDLE turned 90 "
 "degrees (the blade edge-on); RIGHT turned 180 degrees.\n"
 "THE SPEAR, a Keeper temple guardian's ceremonial two-handed spear, carved and cast:\n"
 "- the BLADE: a long, narrow, leaf-shaped blade of tarnished BRASS shaped like the HOUR HAND of a great clock (a slim pointed hand with a small pierced ring near its base), "
 "about a sixth of the whole length; a brass collar ring where it meets the shaft;\n"
 "- the SHAFT: a long, straight, round shaft of pale weathered grey STONE (the same stone as the statue), about 30 pixels thick, banded with three thin brass rings "
 "along its length, a plain stone butt-cap at the bottom;\n"
 "- the whole spear about 990 pixels tall: the blade about 170 pixels, the shaft below it about 820 pixels.\n"
 "Paint in IMAGE 1's hand: pale stone and tarnished brass laid as transparent washes with pale paper highlights; soft even light, no glow, no cast shadows, no ground, "
 "no text, no labels.\nBACKGROUND: flat pure #00ff00. If the image model returns a darker or gradient background anyway, still deliver the image.\n\n"
 "ONE image_gen call. ONE RETRY ONLY if the proportions are off (the blade longer than a quarter of the whole) or the three views disagree -- name the reason and "
 "deliver BOTH images. Copy the output to out/EN2-SP.png (a retry to out/EN2-SP_r1.png) with sha256. No code. No other files. No web.\n"
 "RETURN: receipt task_id \"EN2-SP\"; images = the files with prompt, references (role + path) and elapsed_s; calls_used = the TRUE number of image_gen calls; status; concerns. Never PASS/FAIL.")
FEET = "Legs straight, feet a little apart and pointing forward, soles on one ground line per row; a clear gap of green between the legs. The arms hang AWAY from the body: a clear gap of green between each arm and the body."
def one(text, tid):
    """ONE variant (image budget): rewrite en23's two-variant clause to a single call with one retry."""
    t = text.replace("Two image_gen calls: variants a and b. ONE retry per variant only if", "ONE image_gen call (variant a). ONE retry only if")
    t = t.replace("Copy the outputs to out/%s_a.png and out/%s_b.png (a retry to out/%s_a_r1.png / out/%s_b_r1.png)" % (tid, tid, tid, tid),
                  "Copy the output to out/%s_a.png (a retry to out/%s_a_r1.png)" % (tid, tid))
    assert 'variants a and b' not in t, 'one(): rewrite failed'
    return t
if __name__ == '__main__':
    B.write('EN2-S', R3.text('EN2-S', 'ITS', STATUE, FEET, "the sundial fin swaps to the right shoulder or is missing, a weapon is drawn,", 'sundial fin'),
            [B.STYLE, B.LAYOUT], ['out/EN2-S_a.png', 'out/EN2-S_b.png'], 4)
    B.write('EN2-SP', SPEAR, [dict(B.STYLE, role="IMAGE 1 -- " + B.STYLE['role'].split(' -- ', 1)[-1]),
                              dict(path=A + 'GS-BMAUL2/GS-BMAUL2_a.png', role="IMAGE 2 -- LAYOUT reference (our own earlier weapon sheet): three views, one scale, one ground line; never its weapon's design")],
            ['out/EN2-SP.png'], 2)
    B.write('EN2-O', R3.text('EN2-O', 'ITS', GOLEM, FEET, "the bell swaps to the right wrist or is missing, legs or feet are missing,", 'brass bell'),
            [B.STYLE, B.LAYOUT], ['out/EN2-O_a.png', 'out/EN2-O_b.png'], 4)
    for tid, who, ch, mk, extra in (('EN2-H1', 'ITS', WARDEN, 'clock-face shield', 'a weapon is drawn, the shield swaps to the right arm,'),
                                    ('EN2-H2', 'ITS', MAGISTER, 'astrolabe disc in the hand', 'a staff or a book is drawn,'),
                                    ('EN2-W1', 'HER', WITCH, 'bone-hand pauldron', 'a staff is drawn, the robe reaches below the knee,'),
                                    ('EN2-W2', 'HER', MINDTAKER, 'needle bracelet', 'a staff is drawn, the gown reaches below the knee,')):
        B.write(tid, one(R3.text(tid, who, ch, FEET, extra, mk), tid), [B.STYLE, B.LAYOUT], ['out/%s_a.png' % tid], 2)
