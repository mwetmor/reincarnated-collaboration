# EN-E3 (Run C-9 Phase 2, R-C9-132, the CRUCIBLE CREATURES lane: the NON-BIPED enemies) stage 1: model sheets.
#   python3 scripts/n01_briefs.py <name>   name = our own generic creature name (maw, ...); the roster type_id rides as data only, never in a filename or prompt
# Each creature is ORIGINAL to our world (crypt-born horrors under the Keepers of Hours' desecrated cathedral),
# described GENERICALLY. lane_guard() refuses the roster's record names and the source game's vocabulary on top of
# refs_guard's conductor-owned FORBID list. Sizes, gait and attack styles come from the roster packet's rows.
import json, pathlib, re, sys
BURST = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
A = str(BURST / 'runs/C-9/artifacts') + '/'
LANE_FORBID = re.compile(r'grim\s*dawn|\bcrate\b|crucible|chthon|devourer|hungerer|gorger|ugdenbog|crab\s*monstros|spikeshell|stoneshell|'
                         r'moltenclaw|sandclaw|riftclaw|sand\s*lizard|carnivorous|livingplant|narl|carraxus|basilisk|diablo|blizzard', re.I)
def lane_guard(t):
    m = LANE_FORBID.search(t)
    assert not m, 'lane guard: forbidden token %r' % m.group(0)

STYLE = dict(path=A + 'inputs/nb_style_ref_matt.png',
             role="IMAGE 1 -- STYLE reference ONLY (Matt-supplied): the HAND to copy; never its character, costume, staff, bag or pose")

WORLD = ("THE WORLD: the great cathedral of the Keepers of Hours, an order of timekeepers (their colours lapis blue, ivory and brass; their art is clocks, "
         "astrolabes and hour-rings). It has been desecrated, and under its floor the crypt has woken: things that were never alive in daylight climb up "
         "through the broken floor, out of the ossuary, into the nave. This sheet is one of them: a CREATURE, not a person, an animal-like horror of the crypt.\n")

CREATURES = {
 'maw': dict(type_id='devourer', tid='EN3-MW', marker='the brass gear sunk in its LEFT shoulder', text="""THE CREATURE, a CRYPT MAW: a low, four-legged crawling horror that is mostly MOUTH. It runs fast and low, bites, and retches a spray of bile.
- SIZE AND BUILD: four-legged, about the size of a large boar: roughly 1.8 m from snout to the root of the tail, the top of the shoulders about 0.8 m from the ground. The body is heavy at the front and slung LOW between the legs; the back slopes down from high shoulders to lower hips.
- THE HEAD is the creature: broad, blunt and heavy, as wide as the shoulders, carried level and forward on a thick short neck. It is nearly all JAW: a wide mouth that runs back almost to the neck. In this sheet the MOUTH IS CLOSED: the jaws are shut and a row of long, uneven, pale ivory-yellow TEETH interlock over the lips all along the closed jaw line, upper teeth pointing down over the lower lip and lower teeth pointing up over the upper lip. A thin line of dark madder-red shows only along the lip seam. NO nose. Two small deep-set pale cold-blue EYES set high on the head behind a heavy ridge of bony brow knobs.
- THE HIDE: hairless, tight, ashen grey-violet skin like an old bruise, paler and warmer (a dull ivory-grey) on the belly and the underside of the jaw; the ribs show under the skin along the flanks. A ridge of short, blunt BONE SPURS runs down the middle of the back from the back of the head to the hips, in one row.
- THE LEGS: four thick, strong, many-jointed legs, the FRONT legs heavier and a little longer than the hind legs. Each foot is broad and splayed, with THREE thick dark grey-brown CLAWS.
- THE TAIL: short, thick and tapering, about half a metre long, held straight out behind, level with the hips.
- ASYMMETRY MARKER: a broken, tarnished BRASS CLOCK-GEAR, palm-sized, sunk into the hide of its LEFT SHOULDER ONLY, the skin puckered around it. It shows in every view where the left shoulder is visible, and never on the right shoulder.
- Nothing else on it: no collar, no chain, no armour, no saddle, no cloth, no rider.
"""),
}

def sheet_text(tid, c):
    return ("GENERATE BURST %s -- Run C-9 Phase 2 (Matt, R-C9-132): a NEW ENEMY CREATURE for the same world as the barbarian, the sorceress and the "
     "dark knight already built: ITS MODEL SHEET for a 3D model. task_id \"%s\".\n\n"
     "WHY this sheet exists (so you can judge your own result): a 3D model will be BUILT from these four views, then given a skeleton and animated "
     "(walking, running, biting, being hit, dying). The four views must agree exactly, as four views of ONE animal. A dozen of these will fill an arena "
     "at once, seen from above at a small size, so its silhouette must read clearly.\n\n"
     "IMAGE 1 is a STYLE reference ONLY: copy its HAND (the varying dark ink line, the transparent watercolour washes that pool, granulate and bloom, "
     "the fine hatching in the shadows, the cream paper highlights, the moderate colour). Copy NOTHING else from it: not its character, costume, staff, "
     "bag or pose. It shows a person; this sheet shows a four-legged creature.\n\n"
     + WORLD + c['text'] +
     "\nSTYLE: the REGISTER CARD above governs line, washes, light and plate: no glow, no rim light, no large black areas; the shadows are hatching and "
     "layered washes, never a flat black fill. Brass is a warm ochre-brown wash with pale paper highlights, tarnished, never shiny. Horror comes from "
     "the drawing (the shape, the teeth, the bruised hide), never from darkness or gore.\n"
     "SHEET: ONE 1536x1024 LANDSCAPE sheet on flat pure #00ff00 in a 2x2 grid: the SAME creature in four views at the SAME scale, each view centred in "
     "its quarter, every foot on one ground line per row, the side views filling most of their quarter's WIDTH, and the front and back views drawn at "
     "exactly the same scale as the side views (so they are narrower). Top-left FRONT (head-on, facing the viewer); top-right its RIGHT SIDE (in "
     "profile, its head toward the viewer's right); bottom-left BACK (seen from behind, the tail toward the viewer); bottom-right its LEFT SIDE (in "
     "profile, its head toward the viewer's left). The views are flat orthographic elevations: no three-quarter turn, no perspective.\n"
     "POSE (for building and rigging a 3D model): standing SQUARE and still, in a neutral pose. All four legs STRAIGHT and VERTICAL under the body, "
     "the feet flat on the ground and a little apart, so that in the front and back views a clear gap of green shows between the left and right legs "
     "and under the belly, and in the side views a clear gap of green shows between the front and hind legs. The head level and pointing straight "
     "ahead; the MOUTH CLOSED; the tail straight out behind. Nothing overlaps anything.\n"
     "Soft even light; no cast shadows, no ground, no text, no labels, no cell borders, no other figures.\n"
     "BACKGROUND: flat pure #00ff00. If the image model returns a darker or gradient background anyway, still deliver the image.\n\n"
     "Two image_gen calls: variants a and b. ONE retry per variant only if the result DRIFTS between views (the body, head, teeth, spurs or %s "
     "change between views), a view is missing or faces the wrong way, the asymmetry marker is on the RIGHT side or missing, the mouth is open, a leg is "
     "bent or hidden, or the views are not at one scale -- name the reason. Copy the outputs to out/%s_a.png and out/%s_b.png (a retry to "
     "out/%s_a_r1.png / out/%s_b_r1.png) with sha256. No code. No other files. No web.\n"
     "RETURN: receipt task_id \"%s\"; images = the files with prompt, references (role + path) and elapsed_s; calls_used = the TRUE number of image_gen "
     "calls; status; concerns. Never PASS/FAIL.") % (tid, tid, c['marker'], tid, tid, tid, tid, tid)

def write(tid, text, refs, outs, cap):
    lane_guard(text); [lane_guard(r['role']) for r in refs]
    task = dict(text=text, references=refs, image_cap=cap, minutes_cap=15, tool_call_cap=20, outputs=outs, effort='high', add_dirs=[],
                experiment='R-C9-132-crucible-creatures')
    p = BURST / ('briefs/C-9/%s.task.json' % tid)
    assert not p.exists(), p
    p.write_text(json.dumps(task, indent=1, ensure_ascii=False) + '\n'); print('wrote', p)

if __name__ == '__main__':
    c = CREATURES[sys.argv[1]]; tid = c['tid']
    write(tid, sheet_text(tid, c), [STYLE], ['out/%s_a.png' % tid, 'out/%s_b.png' % tid], 4)
