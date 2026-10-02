# EN-E2 (Run C-9 Phase 2, R-C9-132/133, the CRUCIBLE ENEMIES lane) stage A: two model sheets, one per humanoid caster rig.
#   EN2-M  -> the male humanoid rig  (roster tier-1 #6, hero01_unarmed;  projectile 40 % / aoe 39 %)
#   EN2-F  -> the female humanoid rig (roster tier-1 #15, heroine01_unarmed; projectile 74 %)
# Both are trash casters ORIGINAL to our world: possessed acolytes of the Keepers of Hours' desecrated cathedral.
# Prompt hygiene: generic descriptors only (no franchise/game/character/creature-record name); lane_guard() adds the roster's
# record names and the source game's vocabulary on top of refs_guard's conductor-owned FORBID list.
import json, pathlib, re, sys
BURST = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
A = str(BURST / 'runs/C-9/artifacts') + '/'
LANE_FORBID = re.compile(r'grim\s*dawn|\bcrate\b|crucible|apparition|possessed\s*armou?r|sentinel|eldritch\s*armou?r|janaxia|larria|hexxer|'
                         r'mindthief|allostria|ishtal|witch\s*god|aetherial|chthon|ugdenbog|ghost_[mf]|hero01|heroine01|diablo|blizzard', re.I)
def lane_guard(t):
    m = LANE_FORBID.search(t)
    assert not m, 'lane guard: forbidden token %r' % m.group(0)

STYLE = dict(path=A + 'inputs/nb_style_ref_matt.png',
             role="IMAGE 1 -- STYLE reference ONLY (Matt-supplied, R-C9-69): the HAND to copy; never its character, costume, hood, robe, staff or pose")
LAYOUT = dict(path=A + 'CS9-guides/SO-1_b_harvest.png',
              role="IMAGE 2 -- SHEET reference (our own earlier sheet): the 2x2 grid, the four views, A-pose, one scale and ground lines; never her body, face, hair or clothing")

WORLD = ("THE WORLD: the great cathedral of the Keepers of Hours, an order of timekeepers (their colours lapis blue, ivory and brass; their art is clocks, "
         "astrolabes and hour-rings). It has been desecrated -- a place made for keeping time, where time has been butchered -- and its own acolytes "
         "have been emptied and filled by something cold. These are the enemies the player fights in it: dead servants of the order, still walking.\n")

MALE = """THE CHARACTER, a POSSESSED ACOLYTE (a man), a spellcaster who throws cold bolts and calls rings of cold light:
- an ordinary man's build, gaunt and stooped a little at the neck but standing; natural proportions, about seven and a half heads tall;
- a DEEP HOOD up over his head, its front edge bound in tarnished brass. The face inside the hood is HIDDEN: a dim cool-grey hatched shadow (never a black fill) in which only TWO small pale blue-white EYES show, the same in every view where the face is seen;
- a faded LAPIS-BLUE hooded ACOLYTE'S ROBE over an ivory under-robe, belted at the waist with a plain cord; the robe stops at the KNEE and is SPLIT up both sides to the hip, so the legs move free; ragged, burnt and torn at the hem and cuffs;
- below the hem: plain dark grey-brown leggings and soft wrapped shoes with clear toes;
- BROKEN BRASS CLOCK-GEAR ornaments: a cracked brass gear-wheel as a clasp at the throat of the hood, and two or three small broken brass gear-wheels and a bent clock hand hanging on short chains from the cord belt, close against the robe;
- HANDS bare, thin, the skin a pale grey-blue going to a pale blue-white at the fingertips, as if lit cold from within (painted as pale colour, never as a glow);
- ASYMMETRY MARKER: a broad BRASS BRACER engraved with an hour-ring around his LEFT forearm ONLY; his RIGHT forearm is bare. It shows in every view where his left forearm is visible, and never on the right;
- NOTHING in his hands: no staff, no wand, no book, no orb, no weapon; nothing held.
"""

FEMALE = """THE CHARACTER, a POSSESSED ACOLYTE (a woman), a spellcaster who looses volleys of cold bolts:
- a slender woman's build, upright and still; natural proportions, about seven and a half heads tall;
- her head bare: a pale grey-blue face, gaunt and calm, mouth closed, the eyes open and a pale blue-white with no pupils, looking straight ahead; long straight ash-grey HAIR, loose, hanging to the shoulder blades behind, clear of the arms;
- a thin tarnished BRASS CIRCLET across her brow, a small broken clock-face disc at its front;
- TATTERED CEREMONIAL VESTMENTS: an IVORY ALB (a long close-sleeved under-robe) to the KNEE, under a sleeveless LAPIS-BLUE CHASUBLE (a ceremonial over-vestment hanging front and back in two panels, open at the sides), its edges bordered with a band of faded brass embroidery of hour-marks; everything ragged, burnt and torn at the hems; the hems stop at the KNEE, so the legs move free;
- below the hem: plain dark grey leggings and soft wrapped shoes with clear toes;
- a narrow STOLE of faded lapis cloth hanging from her neck down the front to the knee, a broken brass gear-wheel stitched near each end;
- HANDS bare, thin, the skin a pale grey-blue going to a pale blue-white at the fingertips, as if lit cold from within (painted as pale colour, never as a glow);
- ASYMMETRY MARKER: a cracked brass CLOCK-FACE disc, palm-sized, hanging on a short chain at her LEFT hip ONLY; nothing hangs at her right hip. It shows in every view where her left hip is visible, and never on the right;
- NOTHING in her hands: no staff, no wand, no book, no orb, no weapon; nothing held.
"""

def sheet_text(tid, who, pron, char, retry_marker):
    P, p = pron
    return ("GENERATE BURST %s -- Run C-9 Phase 2 (Matt, R-C9-132/133): a NEW ENEMY for the same world as the barbarian, the sorceress and the dark "
     "knight already built: %s MODEL SHEET for a 3D model. task_id \"%s\".\n\n"
     "WHY this sheet exists (so you can judge your own result): a 3D model will be BUILT from these four views, then rigged and animated (walk, run, "
     "casting, being hit, dying). The four views must agree exactly, as four views of ONE figure. Many copies of this figure will fill an arena, so "
     "%s silhouette must read clearly from above at a small size.\n\n"
     "IMAGE 1 is a STYLE reference ONLY: copy its HAND (the varying dark ink line, the transparent watercolour washes that pool, granulate and bloom, "
     "the fine hatching in the shadows, the cream paper highlights, the moderate colour). Copy NOTHING else from it: not its character, face, hood, robe, "
     "staff, bag or pose. IMAGE 2 is our own earlier sheet: copy its LAYOUT only (grid, views, pose, scale); never its figure.\n\n"
     + WORLD + char +
     "\nSTYLE: the REGISTER CARD above governs line, washes, light and plate: no glow, no rim light, no large black areas; the hood shadow and the "
     "darks are hatching and layered washes, never a flat black fill. Brass is a warm ochre-brown wash with pale paper highlights, tarnished, never shiny.\n"
     "SHEET: ONE 1024x1536 PORTRAIT sheet on flat pure #00ff00 in a 2x2 grid: the SAME %s in four views at the SAME scale, each view centred in its quarter, "
     "soles on one ground line per row, each figure filling most of its quarter's height. Top-left FRONT (facing the viewer); top-right %s RIGHT SIDE "
     "(in profile, facing the viewer's right); bottom-left BACK (seen from behind); bottom-right %s LEFT SIDE (in profile, facing the viewer's left).\n"
     "POSE (for building and rigging a 3D model): a relaxed A-POSE. Both arms straight and held AWAY from the body at about 30 degrees, so that in the "
     "front and back views a clear gap of green shows between each arm and the torso, and the wide sleeves hang clear of the body. Hands OPEN: fingers "
     "together and straight, palms facing the thighs. Legs straight, feet a little apart and pointing forward, and a clear gap of green shows between the "
     "legs below the hem in the front and back views. Head level, facing the same way as the body. Nothing overlaps anything.\n"
     "Soft even light; no cast shadows, no ground, no text, no labels, no cell borders, no other figures.\n"
     "BACKGROUND: flat pure #00ff00. If the image model returns a darker or gradient background anyway, still deliver the image.\n\n"
     "Two image_gen calls: variants a and b. ONE retry per variant only if the result DRIFTS between views (the figure, robe, brass pieces or %s change "
     "between views), a view is missing or faces the wrong way, the asymmetry marker is on the RIGHT side or missing, an arm touches the torso in the front "
     "or back view, the robe reaches below the knee, or anything is held in the hands -- name the reason. Copy the outputs to out/%s_a.png and out/%s_b.png "
     "(a retry to out/%s_a_r1.png / out/%s_b_r1.png) with sha256. No code. No other files. No web.\n"
     "RETURN: receipt task_id \"%s\"; images = the files with prompt, references (role + path) and elapsed_s; calls_used = the TRUE number of image_gen "
     "calls; status; concerns. Never PASS/FAIL.") % (tid, who, tid, p, P, p, p, retry_marker, tid, tid, tid, tid, tid)

def write(tid, text, refs, outs, cap):
    lane_guard(text); [lane_guard(r['role']) for r in refs]
    task = dict(text=text, references=refs, image_cap=cap, minutes_cap=15, tool_call_cap=20, outputs=outs, effort='high', add_dirs=[],
                experiment='R-C9-132-crucible-enemies')
    p = BURST / ('briefs/C-9/%s.task.json' % tid)
    assert not p.exists(), p
    p.write_text(json.dumps(task, indent=1, ensure_ascii=False) + '\n'); print('wrote', p)

if __name__ == '__main__':
    write('EN2-M', sheet_text('EN2-M', 'HIS', ('acolyte', 'his'), MALE, 'his brass bracer'), [STYLE, LAYOUT],
          ['out/EN2-M_a.png', 'out/EN2-M_b.png'], 4)
    write('EN2-F', sheet_text('EN2-F', 'HER', ('acolyte', 'her'), FEMALE, 'her clock-face disc'), [STYLE, LAYOUT],
          ['out/EN2-F_a.png', 'out/EN2-F_b.png'], 4)
