# EN-E2 round 5 (conductor, 2026-10-02): the remaining tier-1 BIPEDS, model sheets first (one wave).
#   EN2-G -> #5  `golemswamp_phase01` (9.0): a crypt-mud GOLEM; aoe 66 / melee 17 / projectile 17 %; p05 emergence; summons the ossuary bloom
#   EN2-N -> #8  `wendigo` (6.0): a FROST-GAUNT; melee 55 / projectile 26 / aura 17 %
#   EN2-Y -> #19 `yeti` (3.0): a shaggy ICE-BRUTE; projectile 39 / aoe 37 / aura 14 %
# Original to our world; generic descriptors only (en01's lane_guard + refs_guard). en23's sheet text.
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
B = __import__('en01_briefs'); R3 = __import__('en23_briefs_r3')

GOLEM = """THE CHARACTER, a CRYPT-MUD GOLEM: a hulking thing that rose from the flooded ossuary under the cathedral, built of what it found there:
- HUGE and heavy: about one and a quarter times a man's height, a broad hunched mass of a body, a small head sunk forward between massive shoulders, very thick arms that hang to the knees with huge blunt three-fingered hands, short thick legs, feet planted wide;
- its body is packed dark grey-brown CRYPT MUD, wet and glistening dully, bound together by twisted dark ROOTS that wrap the limbs and chest; old yellowed BONES (ribs, a few skulls, long bones) are pressed into the mud of its chest, back and shoulders;
- thick green MOSS and pale lichen grow over its shoulders, back and the tops of its arms; a few small pale bone-white flowers among the moss;
- rusted BRASS CLOCKWORK caught in it: a large rusted brass gear-wheel half-sunk in its chest, a bent clock hand and broken brass rods jutting from its back;
- the head: a rough mud mass with two small hollow eye-pits holding a dull green point of light each (painted as pale colour, never a glow), no mouth;
- ASYMMETRY MARKER: a broken length of rusted BRASS CHAIN wrapped around its LEFT forearm ONLY, its loose end hanging; the right forearm is bare mud and root. It shows in every view where the left forearm is visible, and never on the right;
- NOTHING held in the hands.
"""
GAUNT = """THE CHARACTER, a FROST-GAUNT: a starved horror of the frozen heights above the cathedral, once a man, now something else:
- TALL and ELONGATED: about one and a third times a man's height, emaciated to skin and bone, a narrow chest with every rib showing, a hunched long neck, very long thin arms ending in long hands with long dark hooked claws, long thin legs with knobbed knees, long narrow feet with clawed toes;
- skin a frost-pale grey-blue, stretched tight over the bones, darker blue-grey in the hollows, rimed with pale frost on the shoulders, elbows and knees;
- the head: a long narrow skull-like face with deep dark eye sockets holding small pale blue-white points (painted as pale colour, never a glow), a lipless mouth of long thin teeth; from the top of the skull grow two tall branching dark ANTLERS, crusted with frost;
- tatters of an old grey-brown fur hide hanging from the shoulders down the back to the waist, and a ragged strip of the same hide around the hips;
- ASYMMETRY MARKER: its LEFT ANTLER is BROKEN OFF short (a jagged stump), its RIGHT antler is whole and tall. The broken stump is on the LEFT in every view, never on the right;
- NOTHING held in the hands.
"""
YETI = """THE CHARACTER, an ICE-BRUTE: a huge shaggy beast of the snowfields above the cathedral's crag:
- ENORMOUS and heavy: about one and a half times a man's height, a massive barrel chest and great sloping shoulders, very long thick arms that reach past the knees with huge hands, short thick legs, broad flat feet; it stands upright but hunched forward;
- covered in long, thick, SHAGGY fur, a dirty pale grey-white streaked with darker grey, hanging in heavy clumps; the bare skin of the face, chest, palms and soles a dark blue-grey; patches of ICE and hoarfrost matted into the fur of the shoulders and forearms;
- the head: small for the body, a heavy brow, small pale blue-white eyes (painted as pale colour, never a glow), a wide mouth with two short tusks; two short thick curved horns of pale bone sweeping back from the brow;
- ASYMMETRY MARKER: a broken rusted BRASS SHACKLE (an iron-and-brass cuff with three dangling chain links) on its LEFT wrist ONLY; the right wrist is bare fur. It shows in every view where the left wrist is visible, and never on the right;
- NOTHING held in the hands.
"""
FEET = "Legs straight (as straight as the body allows), feet a little apart and pointing forward, soles on one ground line per row; a clear gap of green between the legs."
if __name__ == '__main__':
    B.write('EN2-G', R3.text('EN2-G', 'ITS', GOLEM, FEET + " The huge arms hang AWAY from the body: a clear gap of green between each arm and the belly and legs.",
                             "the chain swaps to the right arm or is missing, legs or feet are missing,", 'brass chain on the forearm'),
            [B.STYLE, B.LAYOUT], ['out/EN2-G_a.png', 'out/EN2-G_b.png'], 4)
    B.write('EN2-N', R3.text('EN2-N', 'ITS', GAUNT, FEET + " The antlers fit inside the quarter (scale the figure down slightly if they would be cut off).",
                             "the broken antler swaps sides, the antlers are cut off by the quarter's edge,", 'broken antler'),
            [B.STYLE, B.LAYOUT], ['out/EN2-N_a.png', 'out/EN2-N_b.png'], 4)
    B.write('EN2-Y', R3.text('EN2-Y', 'ITS', YETI, FEET + " The long arms hang AWAY from the body: a clear gap of green between each arm and the body and legs.",
                             "the shackle swaps to the right wrist or is missing,", 'brass shackle'),
            [B.STYLE, B.LAYOUT], ['out/EN2-Y_a.png', 'out/EN2-Y_b.png'], 4)
