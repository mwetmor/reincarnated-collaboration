# EN-E4 (Run C-9 Phase 2, R-C9-137, the w153/w158 ALTERNATES lane) stage 1: model sheets. Copied from en_e3/scripts/n01_briefs.py (sheet_text unchanged).
#   python3 scripts/n01_briefs.py <name>   name = our own generic creature name (maw, ...); the roster type_id rides as data only, never in a filename or prompt
# Each creature is ORIGINAL to our world (crypt-born horrors under the Keepers of Hours' desecrated cathedral),
# described GENERICALLY. lane_guard() refuses the roster's record names and the source game's vocabulary on top of
# refs_guard's conductor-owned FORBID list. Sizes, gait and attack styles come from the roster packet's rows.
import json, pathlib, re, sys
BURST = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
A = str(BURST / 'runs/C-9/artifacts') + '/'
LANE_FORBID = re.compile(r'grim\s*dawn|\bcrate\b|crucible|chthon|devourer|hungerer|gorger|ugdenbog|crab\s*monstros|spikeshell|stoneshell|'
                         r'moltenclaw|sandclaw|riftclaw|sand\s*lizard|carnivorous|livingplant|narl|carraxus|basilisk|diablo|blizzard|'
                         r'slith|slathra|wrallan|lunorius|balladra|hyppo|corv|corrot|covull|gryphon|griffin|naga|inashkor|corridius', re.I)
def lane_guard(t):
    m = LANE_FORBID.search(t)
    assert not m, 'lane guard: forbidden token %r' % m.group(0)

STYLE = dict(path=A + 'inputs/nb_style_ref_matt.png',
             role="IMAGE 1 -- STYLE reference ONLY (Matt-supplied): the HAND to copy; never its character, costume, staff, bag or pose")

WORLD = ("THE WORLD: the great cathedral of the Keepers of Hours, an order of timekeepers (their colours lapis blue, ivory and brass; their art is clocks, "
         "astrolabes and hour-rings). It has been desecrated, and under its floor the crypt has woken: things that were never alive in daylight climb up "
         "through the broken floor, out of the ossuary, into the nave. This sheet is one of them: a CREATURE, not a person, an animal-like horror of the crypt.\n")

CREATURES = {

 'coilseer': dict(type_id='slith01', tid='EN4-SL', marker='the brass armlet on its LEFT upper arm', body='a serpent-bodied creature with a human-like upper body and arms',
   pose=("POSE (for building and rigging a 3D model): the upper body UPRIGHT and still, rising straight up from the front end of the serpent body, "
         "facing forward; the serpent body lies on the ground in ONE STRAIGHT LINE running directly BACKWARD from under the upper body to the tail tip, "
         "no coils, no curves, the tail tip resting on the ground. BOTH ARMS held DOWN and OUT from the sides at about 30 degrees, elbows nearly straight, "
         "hands open with the fingers together, palms facing in, so a clear gap of green shows between each arm and the body in the front and back views. "
         "The head level and facing straight ahead, the MOUTH CLOSED, the hood folded flat against the neck. Nothing overlaps anything."),
   text="""THE CREATURE, a COILSEER: a serpent-bodied caster of the flooded lower crypt, a scaled thing with the upper body of a lean person and the long body of a great snake in place of legs. It glides on its belly, lashes with its tail so that a wave of black water rolls out across the floor, and calls frost, poison and lightning down out of the air.
- SIZE AND BUILD: the upper body stands about 2.2 m tall from the ground to the top of the head. From the hips down it is ONE thick serpent body, as thick as the waist where it joins, tapering to a thin pointed tail: about 2.4 m of serpent body lies on the ground behind it. Lean and long-armed, never bulky.
- THE HEAD: a long, narrow, flat-topped SNAKE'S HEAD on a human-like neck: small slit-pupilled pale yellow-green eyes set to the sides, two small nostril slits, a long closed lipless mouth, no ears, no hair; a low frill of thin spines folded flat down the back of the skull and neck.
- THE UPPER BODY: a lean, narrow-shouldered human-like torso and two long thin arms covered in small fine scales; each hand has FOUR long thin clawed fingers. A broad pale belly-plate of overlapping cream-ivory scutes runs from the throat down the front of the torso and on down the whole UNDERSIDE of the serpent body to the tail.
- THE SCALES: dull deep teal-green and slate along the back, the arms, the head and the top of the serpent body, broken by darker bands of mottled olive-black across the serpent body; fading to the pale ivory belly-plate. A few patches of ragged dead skin peel at the shoulders.
- CLOTHING: only a short ragged wrap of faded lapis-blue cloth around the hips where the serpent body begins, its frayed hem falling no lower than a hand's width, and a few strings of small bone beads across the chest. Nothing on the serpent body.
- ASYMMETRY MARKER: a corroded BRASS ARMLET engraved with hour-marks clamped around its LEFT upper arm ONLY, just below the shoulder. It shows in every view where the left arm is visible, never on the right.
- Nothing else on it: no weapon, no staff, no armour, no crown, no wings.
"""),

 'gloamwing': dict(type_id='gryphon01a', tid='EN4-GR', marker='the brass band on its LEFT foreleg', body='a winged four-legged beast with the head of a raven',
   pose=("POSE (for building and rigging a 3D model): standing SQUARE and still on its FOUR legs in a neutral pose, all four legs STRAIGHT and VERTICAL "
         "under the body, the feet flat and a little apart, so that in the front and back views a clear gap of green shows between the left and right legs "
         "and under the belly, and in the side views a clear gap of green shows between the front and hind legs. The two WINGS FOLDED tight along its back "
         "and flanks, their tips lying along the top of the hindquarters and NOT reaching the ground, clear of the legs. The neck raised, the head level and "
         "pointing straight ahead, the BEAK CLOSED. The tail straight out behind. Nothing overlaps anything."),
   text="""THE CREATURE, a GLOAMWING: a great winged beast of the crypt's black sky-shafts, built like a heavy horse with the head, neck, wings and forelegs of a giant raven. It stalks on four legs, rakes with its talons, and breathes out a gout of shadow that flies as a burst of dark, skull-faced sparks; a cold dark haze clings around it.
- SIZE AND BUILD: about 3.6 m from the tip of the beak to the rump (the tail more), its back about 1.8 m from the ground, the head carried higher, about 2.6 m up. A deep feathered chest and strong shoulders; the hindquarters lean and horse-like.
- THE HEAD AND NECK: a big RAVEN'S HEAD on a long, thick, feathered neck held up and forward: a heavy, curved, black-iron-grey BEAK as long as the skull, closed; small deep-set pale violet eyes; a ruff of ragged hackle feathers around the throat.
- THE WINGS: two great black feathered WINGS, folded along the back; folded, each wing reaches from the shoulder to the top of the hindquarters. The long flight feathers are blue-black with dull violet sheen painted as a pale wash, never shiny.
- THE FORELEGS: like a giant bird's legs, scaly and dark grey, each foot with FOUR long hooked TALONS (three forward, one back), gripping the ground.
- THE HINDQUARTERS AND HIND LEGS: short-coated, sooty black-brown hide like a horse's, the hind legs long and horse-like ending in broad, dark, cloven hooves.
- THE TAIL: a long sweep of black tail feathers, fanned slightly, held straight out behind.
- FEATHERS: black and slate-grey everywhere above, paler ash-grey on the breast and the underside of the neck, ragged at the edges; on the shoulders a few feathers are bone-pale and bare-quilled.
- ASYMMETRY MARKER: a corroded BRASS BAND engraved with hour-marks clamped around its LEFT foreleg ONLY, just above the talons. It shows in every view where the left foreleg is visible, never on any other leg.
- Nothing else on it: no rider, no saddle, no harness, no chains, no armour.
"""),
}

def sheet_text(tid, c):
    return ("GENERATE BURST %s -- Run C-9 Phase 2 (Matt, R-C9-135/137): a NEW ENEMY CREATURE for the same world as the barbarian, the sorceress and the "
     "dark knight already built: ITS MODEL SHEET for a 3D model. task_id \"%s\".\n\n"
     "WHY this sheet exists (so you can judge your own result): a 3D model will be BUILT from these four views, then given a skeleton and animated "
     "(walking, running, attacking, being hit, dying). The four views must agree exactly, as four views of ONE animal. A dozen of these will fill an arena "
     "at once, seen from above at a small size, so its silhouette must read clearly.\n\n"
     "IMAGE 1 is a STYLE reference ONLY: copy its HAND (the varying dark ink line, the transparent watercolour washes that pool, granulate and bloom, "
     "the fine hatching in the shadows, the cream paper highlights, the moderate colour). Copy NOTHING else from it: not its character, costume, staff, "
     "bag or pose. It shows a person; this sheet shows " + c.get('body', 'a four-legged creature') + ".\n\n"
     + WORLD + c['text'] +
     "\nSTYLE: the REGISTER CARD above governs line, washes, light and plate: no glow, no rim light, no large black areas; the shadows are hatching and "
     "layered washes, never a flat black fill. Brass is a warm ochre-brown wash with pale paper highlights, tarnished, never shiny. Horror comes from "
     "the drawing (the shape, the teeth, the bruised hide), never from darkness or gore.\n"
     "SHEET: ONE 1536x1024 LANDSCAPE sheet on flat pure #00ff00 in a 2x2 grid: the SAME creature in four views at the SAME scale, each view centred in "
     "its quarter, every foot on one ground line per row, the side views filling most of their quarter's WIDTH, and the front and back views drawn at "
     "exactly the same scale as the side views (so they are narrower). Top-left FRONT (head-on, facing the viewer); top-right its RIGHT SIDE (in "
     "profile, its head toward the viewer's right); bottom-left BACK (seen from behind, the tail toward the viewer); bottom-right its LEFT SIDE (in "
     "profile, its head toward the viewer's left). The views are flat orthographic elevations: no three-quarter turn, no perspective.\n"
     + c.get('pose', "POSE (for building and rigging a 3D model): standing SQUARE and still, in a neutral pose. All four legs STRAIGHT and VERTICAL under the body, "
     "the feet flat on the ground and a little apart, so that in the front and back views a clear gap of green shows between the left and right legs "
     "and under the belly, and in the side views a clear gap of green shows between the front and hind legs. The head level and pointing straight "
     "ahead; the MOUTH CLOSED; the tail straight out behind. Nothing overlaps anything.") + "\n"
     "Soft even light; no cast shadows, no ground, no text, no labels, no cell borders, no other figures.\n"
     "BACKGROUND: flat pure #00ff00. If the image model returns a darker or gradient background anyway, still deliver the image.\n\n"
     "Two image_gen calls: variants a and b. ONE retry per variant only if the result DRIFTS between views (the body, head, teeth, spurs or %s "
     "change between views), a view is missing or faces the wrong way, the asymmetry marker is on the RIGHT side or missing, the mouth is open, a leg is "
     "hidden or touches another, or the views are not at one scale -- name the reason. Copy the outputs to out/%s_a.png and out/%s_b.png (a retry to "
     "out/%s_a_r1.png / out/%s_b_r1.png) with sha256. No code. No other files. No web.\n"
     "RETURN: receipt task_id \"%s\"; images = the files with prompt, references (role + path) and elapsed_s; calls_used = the TRUE number of image_gen "
     "calls; status; concerns. Never PASS/FAIL.") % (tid, tid, c['marker'], tid, tid, tid, tid, tid)

def write(tid, text, refs, outs, cap):
    lane_guard(text); [lane_guard(r['role']) for r in refs]
    task = dict(text=text, references=refs, image_cap=cap, minutes_cap=15, tool_call_cap=20, outputs=outs, effort='high', add_dirs=[],
                experiment='R-C9-137-alternates')
    p = BURST / ('briefs/C-9/%s.task.json' % tid)
    assert not p.exists(), p
    p.write_text(json.dumps(task, indent=1, ensure_ascii=False) + '\n'); print('wrote', p)

if __name__ == '__main__':
    c = CREATURES[sys.argv[1]]; tid = c['tid']
    write(tid, sheet_text(tid, c), [STYLE], ['out/%s_a.png' % tid, 'out/%s_b.png' % tid], 4)
