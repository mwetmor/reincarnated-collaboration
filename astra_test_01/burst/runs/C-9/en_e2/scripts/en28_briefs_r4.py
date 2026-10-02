# EN-E2 round 4 (conductor, 2026-10-02): three more crucible enemies, model sheets first (one wave).
#   EN2-B -> #1  `aetherialcorruption` (17.8 bodies, the largest rig): a hulking flesh-warped BRUTE; melee 59 / projectile 31 %; p05 emergence
#   EN2-C -> #12 `cannibal` (5.7): a feral BOG-WRETCH; melee 44 / projectile 40 / buff 12 %
#   EN2-I -> #9  `aetherialimp` (6.0): a small corrupted IMP; melee 91 %
# Original to our world; generic descriptors only (en01's lane_guard + refs_guard). en23's sheet text, reused.
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
B = __import__('en01_briefs'); R3 = __import__('en23_briefs_r3')

BRUTE = """THE CHARACTER, a FLESH-WARPED BRUTE: a former Keeper of the order, twisted by the corruption into a hulking, ASYMMETRIC monster:
- HUGE and heavy: about one and a quarter times a man's height, a massive hunched torso and thick neck, the small head sunk low between the shoulders; short thick legs, feet planted wide;
- the flesh is swollen and lumpy, a sickly pale grey-violet with darker violet-grey bruising and a few pale lapis veins; patches of torn stitched skin;
- ASYMMETRY (the marker): its RIGHT arm is ENORMOUS -- swollen to twice the left arm's thickness, ending in a huge heavy three-fingered hand; its LEFT arm is long, thinner and sinewy with a normal clawed hand. The swollen arm is on the RIGHT in every view, never on the left;
- BRASS CLOCKWORK FUSED INTO THE FLESH: a large cracked brass gear-wheel half-sunk into its LEFT shoulder, smaller brass gears and a bent clock hand embedded along the spine, and a broken brass hour-ring pressed into the top of its head like a crown grown over by flesh;
- the shreds of a Keeper's lapis robe hanging from its waist as a torn loincloth, a cracked leather belt; bare feet with thick dark toenails;
- a heavy brow, small pale blue-white eyes (painted as pale colour, never a glow), a wide lipless mouth;
- NOTHING held in the hands.
"""
WRETCH = """THE CHARACTER, a BOG-WRETCH: a feral cannibal from the drowned marsh below the cathedral's crag, once human:
- a gaunt, wiry man of ordinary height, standing upright but with hunched shoulders and the head pushed forward; natural proportions;
- skin a sickly mud-grey-green, streaked with dried dark-brown mud and old blood; long matted dark hair and a ragged beard tangled with reeds;
- a ragged loincloth of hide and sacking, a crude rope belt hung with small bones and teeth; strips of filthy cloth wound around the shins; bare feet;
- a STOLEN torn sash of faded lapis Keeper cloth worn across the chest from the right shoulder to the left hip, a cracked brass gear-wheel knotted into it;
- yellowed eyes, a snarling mouth with broken teeth; long dirty fingernails;
- ASYMMETRY MARKER: a BONE BRACELET of small knuckle-bones around the LEFT wrist ONLY; the right wrist is bare. It shows in every view where the left wrist is visible, and never on the right;
- NOTHING held in the hands.
"""
IMP = """THE CHARACTER, a CORRUPTED IMP: a small, quick, malicious creature born of the corruption in the cathedral's ruins:
- SMALL: about two thirds of a man's height, a wiry thin body with a pot belly, a large round head, long thin arms that reach to its knees and short bowed legs; it stands upright;
- skin a pale grey-violet with darker violet blotches; two short curled horns of dark bone on its brow; long pointed ears; small pale blue-white eyes (painted as pale colour, never a glow) and a wide mouth of small needle teeth;
- a cracked BRASS gear-wheel embedded in the middle of its chest, the flesh grown around its rim; a scrap of torn lapis cloth tied around its hips as a ragged loincloth;
- long clawed fingers and clawed toes; NO tail, NO wings;
- ASYMMETRY MARKER: a thin BRASS RING around its LEFT upper arm ONLY; the right arm is bare. It shows in every view where the left upper arm is visible, and never on the right;
- NOTHING held in the hands.
"""
FEET = "Legs straight (as straight as the body allows), feet a little apart and pointing forward, soles on one ground line per row; a clear gap of green between the legs."
if __name__ == '__main__':
    B.write('EN2-B', R3.text('EN2-B', 'ITS', BRUTE, FEET + " The arms hang away from the body: the huge RIGHT arm clear of the belly and leg, a gap of green between them.",
                             "the swollen arm swaps sides or both arms are equal, legs or feet are missing,", 'swollen arm'),
            [B.STYLE, B.LAYOUT], ['out/EN2-B_a.png', 'out/EN2-B_b.png'], 4)
    B.write('EN2-C', R3.text('EN2-C', 'HIS', WRETCH, FEET, "a weapon appears, the sash is missing,", 'bone bracelet'),
            [B.STYLE, B.LAYOUT], ['out/EN2-C_a.png', 'out/EN2-C_b.png'], 4)
    B.write('EN2-I', R3.text('EN2-I', 'ITS', IMP, FEET + " It is SMALL: draw it filling most of its quarter's height anyway (the scale is set later).",
                             "a tail or wings appear,", 'brass ring on the upper arm'),
            [B.STYLE, B.LAYOUT], ['out/EN2-I_a.png', 'out/EN2-I_b.png'], 4)
