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

 'glutton': dict(type_id='aetherialbloater', tid='EN3-GL', marker='the brass manacle on its LEFT wrist', body='a hunched two-legged brute',
   pose=("POSE (for building and rigging a 3D model): standing still on its two legs in a neutral pose, hunched forward as it naturally stands, "
         "the legs straight-ish and apart under the hips, the feet flat and pointing forward, so a clear gap of green shows between the legs in the "
         "front and back views. Both long arms hang down and a little OUT from the body, clear of the belly and the legs, the claws open, so a gap of "
         "green shows between each arm and the body in the front and back views. The head level and facing forward, the MOUTH CLOSED. Nothing overlaps anything."),
   text="""THE CREATURE, a CRYPT GLUTTON: a hunched, two-legged brute that is mostly GUT. It lumbers, lunges to bite, retches a spray of bile, and coughs up gobbets of half-digested filth that crawl away as worms.
- SIZE AND BUILD: about 2.3 m tall as it stands hunched; enormously broad and heavy in the middle. Its body is a vast distended BELLY that sags forward and down almost to its knees, the skin stretched tight and veined; the shoulders hunch high and the head sits low and forward between them, below the line of the shoulders.
- THE HEAD: small for the body, bald and lumpy, mostly a wide lipless jaw with stubby broken yellow teeth, CLOSED in this sheet; small sunken pale eyes; no nose, two slits.
- THE SKIN: corpse grey going to livid bruise-purple at the joints and on the back; the belly paler, a sickly pale verdigris-grey, with dark veins and a few weeping sores; a few crude black stitches across the belly where it was once sewn shut.
- THE LEGS: short, thick and bowed, with broad flat three-toed feet.
- THE ARMS: surprisingly LONG and thin compared with the body, hanging nearly to the ground, each ending in a hand of three long hooked dark claws.
- ASYMMETRY MARKER: a corroded BRASS MANACLE with a short broken chain clamped around its LEFT wrist ONLY. It shows in every view where the left wrist is visible, never on the right.
- Nothing else on it: no clothing except a torn grey-brown loincloth rag at the hips, no weapon, no rider.
"""),

 'blightsac': dict(type_id='voidfiend', tid='EN3-BS', marker='the brass hour-ring on its LEFT side', body='a floating creature',
   pose=("POSE (for building and rigging a 3D model): floating still in a neutral pose, the body level, about a metre clear of the ground "
         "(draw NO ground), the mouth CLOSED, the six tendrils hanging straight down and evenly spaced around the underside, not touching each "
         "other, their tips well clear of the ground line. In every view a clear gap of green shows between the tendrils and under the tips. Nothing overlaps anything."),
   text="""THE CREATURE, a BLIGHT SAC: a floating, bloated horror that drifts up out of the crypt like a swollen bladder of plague. It retches a cone of acid, spits heavy orbs of poison, and leaks a choking caustic haze around itself; when it dies it bursts.
- SIZE AND BUILD: a single swollen, roughly egg-shaped body about 1.4 m long, 1.2 m wide and 1.1 m tall, its underside hanging about 0.9 m above the floor, so the top is at about 2 m. It HAS NO LEGS: it floats.
- THE BODY: tight, shiny-wet but painted matte, pallid grey-violet skin stretched over the swelling, mottled with sickly yellow-green blotches; dark veins; on its BACK a cluster of five or six open, crusted VENTS like small chimneys rimmed with yellow crust, where the haze leaks out (painted, no smoke drawn).
- THE FRONT: a wide round lamprey MOUTH at the front, ringed with rows of small inward-pointing pale teeth, CLOSED as a puckered ring in this sheet; above it a band of five small pale-yellow eyes in an arc.
- THE TENDRILS: SIX thick, tapering, fleshy tendrils hang from the underside in a ring, each about 0.8 m long, grey-violet with paler sucker rings.
- ASYMMETRY MARKER: a corroded BRASS HOUR-RING (a band engraved with hour-marks) sunk into the skin of its LEFT flank ONLY, like a buckle swallowed into the flesh. It shows in every view where the left flank is visible, never on the right.
- Nothing else on it: no rider, no chains, no wings, no cloth.
"""),

 'rimethorn': dict(type_id='thornedhorrora01', tid='EN3-RT', marker='the brass ring around its LEFT foreleg', body='a four-legged spiny beast',
   pose=("POSE (for building and rigging a 3D model): standing square and still on all four legs in a neutral pose, the legs straight and "
         "vertical under the body, the feet flat and apart, the head level and facing straight ahead, the MOUTH CLOSED, the short tail straight "
         "out behind. In the front and back views a clear gap of green shows between the left and right legs and under the belly; in the side "
         "views between the front and hind legs. Nothing overlaps anything."),
   text="""THE CREATURE, a RIMETHORN BRUTE: a hulking four-legged horror of frost, bone and thorn that has crawled up from the frozen lower crypt. It slashes with its long foreclaws, drives a wall of ice spikes out of the floor ahead of it, and bursts ice shards.
- SIZE AND BUILD: heavy and hunched, like a great bear or a bull: about 2.6 m from snout to rump, the top of its humped shoulders about 1.6 m from the ground, the back sloping down to lower hips. The FORELEGS are longer and much heavier than the hind legs.
- THE HEAD: low-slung and heavy, a long skull of bare pale bone like a horse's skull without skin, with a closed jaw of uneven teeth and two small pale ice-blue eyes deep in the sockets, painted pale, never glowing.
- THE BODY: dark slate and blue-grey hide, rough, matted; out of the hump, the spine and the shoulders grow DOZENS of long, sharp, crooked THORNS of pale bone and clear blue-white ice, pointing up and back like a broken crown -- the creature's silhouette is a spiky hump. Frost crusts the thorn roots.
- THE FORELIMBS: thick, end in long hooked claws of pale bone, three per hand, longer than the feet; the hind legs shorter with blunt claws.
- THE TAIL: short and thick, with a few thorns.
- ASYMMETRY MARKER: a corroded BRASS RING engraved with hour-marks clamped around its LEFT foreleg ONLY, above the claws. It shows in every view where the left foreleg is visible, never on any other leg.
- Nothing else on it: no rider, no chains, no cloth.
"""),

 'gazer': dict(type_id='basilisk', tid='EN3-GZ', marker='the brass band on its LEFT foreleg', body='a four-legged reptile',
   pose=("POSE (for building and rigging a 3D model): standing square and still on all four legs in a neutral pose, the legs straight and "
         "vertical under the body, the feet flat and a little apart, the long neck held up and forward in a gentle curve, the head level and "
         "facing straight ahead, the MOUTH CLOSED, the long tail held straight out behind, level. In the front and back views a clear gap of "
         "green shows between the left and right legs and under the belly; in the side views between the front and hind legs. Nothing overlaps anything."),
   text="""THE CREATURE, a CRYPT GAZER: a long, low, four-legged reptile of the ossuary with a long serpentine neck. Its stare turns flesh to stone; it also spits and retches acid and sweeps with its heavy tail.
- SIZE AND BUILD: about 4 m from snout to tail tip, a third of that the tail; the body low and long, the top of the back about 1.1 m from the ground; the neck rises from the shoulders in an S-curve so the head is carried at about 1.8 m.
- THE HEAD: wedge-shaped, with a closed lipless mouth and a crown of SIX short pale bone horns swept back from the brow like a broken diadem; two large round EYES, pale verdigris-white with a black slit pupil, painted pale, never glowing.
- THE HIDE: small dull scales, slate-grey and dark verdigris green, mottled; the belly and throat pale chalky ivory, banded; along the spine a row of low, flat, stone-grey scutes, as if part of it were already stone.
- THE LEGS: four short, thick, sprawling legs with five-clawed feet, the claws dark.
- THE TAIL: long and heavy, ending in a flattened club of stony scutes.
- ASYMMETRY MARKER: a corroded BRASS BAND engraved with hour-marks clamped around its LEFT foreleg ONLY, just above the foot. It shows in every view where the left foreleg is visible, never on the right.
- Nothing else on it: no rider, no collar, no chains, no cloth, no wings.
"""),

 'bloom': dict(type_id='carnivorousplant01a_p1', tid='EN3-BL', marker='the brass clock-hand in the LEFT side of its head', body='a rooted flesh-eating plant',
   pose=("POSE (for building and rigging a 3D model): standing still and upright, rooted in place, in a neutral pose: the stem straight up, the head level "
         "and facing straight ahead, the MOUTH CLOSED, the floor leaves spread flat and evenly around the base. In the side views a clear gap of green "
         "shows between the stem and the leaves above the floor, and between the head and the leaves. Nothing overlaps anything."),
   text="""THE CREATURE, an OSSUARY BLOOM: a great flesh-eating plant that has burst up through the cracked crypt floor. It never moves from its spot: it snaps at anything close and spits heavy venom seeds at anything far.
- SIZE AND BUILD: about 2.2 m tall. A ROSETTE of six broad, thick, leathery leaves lies spread flat on the floor around its base, about 2.4 m across, their tips curling up a little. From its middle rises one thick, ribbed, slightly twisting STEM, as thick as a man's thigh at the bottom, narrowing upward.
- THE HEAD at the top of the stem: a large swollen bulb, about 1 m long from front to back, like a great seed pod or a closed flower bud on its side, with a wide horizontal MOUTH running across its front and around both sides. The mouth is CLOSED: its two thick lips are fringed with long pale ivory thorn-teeth that interlock. Thin dark madder-red lines show at the lip seam. No eyes.
- COLOURS: the leaves and stem a dull verdigris green going to a bruised violet-grey at the edges; the head the same with pale ivory veins running back from the mouth like old bone; small vermilion-red flecks on the head; the underside of the leaves paler.
- ASYMMETRY MARKER: a bent, tarnished BRASS CLOCK-HAND, as long as a forearm, pierced through the LEFT side of the head and stuck there ONLY. It shows in every view where the left side of the head is visible, and never on the right.
- Nothing else on it: no flowers, no pot, no chains, no bones lying around it, no ground or floor drawn.
"""),

 'raptor': dict(type_id='sandlizard', tid='EN3-RP', marker='the brass ring on its LEFT forearm', body='a two-legged reptile',
   pose=("POSE (for building and rigging a 3D model): standing still on its two hind legs in a neutral pose, the body level and horizontal, "
         "the tail held straight out behind, level with the hips, the neck and head level and pointing straight ahead, the MOUTH CLOSED. Both hind legs "
         "straight under the hips, the feet flat and a little apart, so that in the front and back views a clear gap of green shows between the legs. "
         "Both forelimbs held a little forward and AWAY from the chest, the claws open and relaxed, so that a gap of green shows between each forelimb and "
         "the body in the front and back views. Nothing overlaps anything."),
   text="""THE CREATURE, a CINDER STALKER: a fast, lean, two-legged reptile hunter of the burning crypt. It runs down its prey, rakes with its forelimbs, kicks with a hooked claw, and LEAPS onto its target from far away.
- SIZE AND BUILD: a big lean predator that runs on its two hind legs like a giant bird, its body held level: about 5.5 m from snout to tail tip, about half of that the long tail; the top of the hips about 1.6 m from the ground, the head carried at about 2.2 m. Lean, long-legged, never bulky.
- THE HEAD: long and narrow, with a long closed jaw lined with small hooked teeth showing along the lip, a bony ridge over the eyes, two small amber eyes; a short crest of three backward-pointing horn spines at the back of the skull.
- THE HIDE: small tight scales, ash-grey and charcoal, with cracks of dull EMBER ORANGE and ochre running across the back, the flanks and the tail like cooling lava under the scales (painted as warm colour, never as glow); the throat and belly paler, a warm ash-ivory.
- THE HIND LEGS: long, powerful and bird-like, the shin long and the ankle high off the ground; each foot with three forward toes, and on the inner toe one large hooked SICKLE CLAW held up off the ground.
- THE FORELIMBS: two lean arms, shorter than the legs but strong, each hand with three long hooked claws for raking.
- THE TAIL: long, thick at the hips and tapering to a point, with a low ridge of small dark spines along its top.
- ASYMMETRY MARKER: a corroded BRASS RING engraved with hour-marks, clamped around its LEFT forearm ONLY. It shows in every view where the left forearm is visible, and never on the right.
- Nothing else on it: no rider, no saddle, no chains, no cloth, no feathers.
"""),

 'crab': dict(type_id='crabmonstrosity', tid='EN3-CR', marker='the brass band on its LEFT claw', body='a many-legged creature',
   pose=("POSE (for building and rigging a 3D model): standing still and level in a neutral pose, the shell level. The SIX walking legs spread "
         "evenly, three on each side, each rising to its knee and down to a point on the ground, with clear gaps of green between neighbouring legs in "
         "every view and under the shell. The two claws held forward, a little raised and CLEAR of the ground, the pincers CLOSED, a gap of green between "
         "each claw and the shell and between the two claws. The eye stalks upright; the mouth plates shut. Nothing overlaps anything."),
   text="""THE CREATURE, an OSSUARY CRAB: a huge crab-like horror of the drowned crypt, the size of a cart. It scuttles fast, slams its claws down, and breathes out a freezing mist.
- SIZE AND BUILD: a broad, low-domed CARAPACE about 1.6 m across and 1.3 m from front to back, its top about 1.2 m from the ground; with the legs spread, the whole creature is about 3 m across. Heavy and wide, never tall.
- THE CARAPACE: a dome of fused, pitted plates of old BONE, pale grey-ivory, with a cold slate-blue-grey wash in the hollows; along its front and side edges a fringe of short blunt bone points; a crust of pale white-blue frost along the rim. Seen from above it reads as one clear oval shell.
- THE FRONT: two short stalked EYES, small and pale cold-blue, on top of the front edge; below them a small closed cluster of mouth plates, shut.
- SIX WALKING LEGS, three on each side, long, jointed and spindly, each rising up and out from the shell to a high bent knee and then down to a sharp pointed tip on the ground; dark slate-grey, the joints paler bone.
- TWO GREAT CLAWS in front, each on a thick jointed arm, held forward and slightly raised, CLEAR OF THE GROUND, the pincers CLOSED. The claws are the same size as each other, heavy and serrated, bone-pale with slate-grey tips.
- ASYMMETRY MARKER: a corroded BRASS BAND engraved with hour-marks, clamped around the wrist of its LEFT claw ONLY. It shows in every view where the left claw is visible, and never on the right claw.
- Nothing else on it: no rider, no chains, no cloth, no weeds hanging.
"""),
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
                experiment='R-C9-132-crucible-creatures')
    p = BURST / ('briefs/C-9/%s.task.json' % tid)
    assert not p.exists(), p
    p.write_text(json.dumps(task, indent=1, ensure_ascii=False) + '\n'); print('wrote', p)

if __name__ == '__main__':
    c = CREATURES[sys.argv[1]]; tid = c['tid']
    write(tid, sheet_text(tid, c), [STYLE], ['out/%s_a.png' % tid, 'out/%s_b.png' % tid], 4)
