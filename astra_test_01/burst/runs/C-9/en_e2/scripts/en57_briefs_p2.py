# EN-E2 Phase 2 (conductor dispatch after R-C9-135, reordered for Matt's wave-order playtest w151-160): FIVE new model sheets, one
# variant each (image budget), the en44 round-7 form. Original to our world; generic descriptors only (en01 lane_guard + refs_guard);
# record names live in kit keys only.
#   EN2-L  the w152 quest boss on its own caster rig    -> a FLESH-SHAPER aether sorcerer            (lane letter l)
#   EN2-U  the w154 quest boss on its own caster rig    -> an ASCENDED fire zealot-priest           (lane letter u)
#   EN2-X  the w160 nemesis on the skeleton rig         -> a SKELETAL VIGIL-LORD caster (free transfer from the revenant rig; letter x)
#   EN2-D  the w159 hulking flesh brute boss            -> a FLESH HULK                              (lane letter d)
#   EN2-E  the w160 giant crystal-studded brute boss    -> a CRYSTAL COLOSSUS                         (lane letter e)
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
B = __import__('en01_briefs'); R3 = __import__('en23_briefs_r3'); R7 = __import__('en44_briefs_r7')
SHAPER = """THE CHARACTER, the FLESH-SHAPER, a BOSS: a sorcerer of the cold light that took the cathedral, who sculpts living flesh with it:
- a tall gaunt man, about one and a quarter times a man's height, upright, long-armed, long thin fingers;
- a long split robe of pale ivory and faded LAPIS, torn into points at the knee (the legs move free below), stitched all over with thick dark surgical sutures; a heavy leather apron over it hung with small brass hooks, clamps and scalpels on chains;
- the head: a bald, pale grey-green skull-like head with grafted patches of different flesh held by brass staples, thin lips, pale sickly GREEN-WHITE eyes (painted as pale colour, never a glow);
- thin crystalline seams of pale aether-GREEN running under the skin of the hands, forearms and neck like veins (pale colour, never a glow);
- ASYMMETRY MARKER: his LEFT forearm is a GRAFTED ARM, visibly larger and of mismatched grey-violet flesh, bound at the elbow with a brass ring; the right forearm is his own thin arm. It shows in every view where the left forearm is visible, never on the right;
- NOTHING held in the hands.
"""
ASCENDED = """THE CHARACTER, the ASCENDED ZEALOT, a BOSS: a priest of a fire cult who burned himself into something more than a man:
- a tall powerful man, about one and a quarter times a man's height, upright, broad chest, a commanding stance;
- his skin is cracked dark CHARCOAL-grey like cooled lava, with thin cracks of pale EMBER-ORANGE between the plates (painted as pale colour, never a glow), most on the chest, arms and face;
- the head: a heavy brow, a short burnt beard, pale ember-orange eyes, and a tall CROWN of three long curved dark horns rising behind the head like a fan;
- a long tattered priest's robe of deep oxblood RED and soot-black, open at the chest, torn into points at the knee (the legs move free below), a broad belt of tarnished brass plates; bound wrists in strips of burnt cloth; bare charcoal feet;
- a heavy brass censer-chain looped once across the chest;
- ASYMMETRY MARKER: a large BRASS SUN-DISC pauldron on his LEFT shoulder ONLY; the right shoulder is bare robe. It shows in every view where the left shoulder is visible, never on the right;
- NOTHING held in the hands.
"""
VIGIL = """THE CHARACTER, the VIGIL-LORD, a NEMESIS: an immortal skeleton lord who keeps a death-watch over the cathedral's crypts, a caster of death-bolts:
- a man-sized human SKELETON of old ivory-grey bone, a little taller than a man and upright, dark empty eye sockets each with a small pale blue-white point (painted as pale colour, never a glow);
- a tall high-collared COWL and long hooded MANTLE of faded LAPIS and black over the shoulders, falling to the knee front and back in ragged strips, edged in tarnished brass hour-marks;
- a ribbed breastplate of tarnished BRASS over the ribcage, engraved with an hour-ring; a belt of brass links; ragged dark cloth around the hips to the knee (the legs move free below); bare bone shins, hands and feet;
- a thin brass CIRCLET of small hour-hand spikes on the skull;
- ASYMMETRY MARKER: a small brass LANTERN with a cracked glass, hanging on a short chain from its LEFT wrist ONLY (part of the costume; nothing is held); the right wrist has none. It shows in every view where the left wrist is visible, never on the right;
- NOTHING held in the hands.
"""
HULK = """THE CHARACTER, the FLESH HULK, a BOSS: a towering brute built out of many bodies stitched into one by the cold light:
- HUGE: about one and two-thirds times a man's height, a massive hunched body, a small head sunk low between huge rounded shoulders, a vast barrel belly, very thick arms reaching past the knees with huge four-fingered hands, short thick legs, broad bare feet;
- the flesh is sickly pale grey-violet with darker purple-grey bruising, every part a different shade, all joined by thick dark STITCHED seams and brass staples; pale aether-GREEN crystal shards grow out of the seams on the shoulders and back (pale colour, never a glow);
- a great iron-and-brass collar around the neck with a broken chain; a torn leather loincloth on a heavy belt; brass bands around the forearms;
- the head: a small bald head with a heavy stitched jaw, small pale green-white eyes;
- ASYMMETRY MARKER: a large rusted brass CLOCK-GEAR riveted into its LEFT shoulder ONLY; the right shoulder is bare stitched flesh. It shows in every view where the left shoulder is visible, never on the right;
- NOTHING held in the hands.
"""
COLOSSUS = """THE CHARACTER, the CRYSTAL COLOSSUS, a BOSS: a giant of stone and crystal that the cold light grew out of the cathedral's foundations:
- GIANT: about one and three-quarter times a man's height, a massive broad upright body, a small head low between enormous shoulders, very long thick arms with huge blunt three-fingered stone hands reaching to the knees, thick legs, broad flat feet;
- its body is dark slate-grey STONE in great cracked slabs like armour, the cracks filled with pale aether-GREEN; large jagged clusters of pale green-white CRYSTAL grow out of its shoulders, back and forearms (pale colour and paper highlights, never a glow);
- old tarnished BRASS bands and broken hour-ring fragments are embedded in the stone of its chest and thighs, as if it had grown through the cathedral's clockwork;
- the head: a heavy stone brow, no mouth, two small pale green-white points for eyes;
- ASYMMETRY MARKER: the crystal cluster on its LEFT shoulder is HUGE (twice the size of the right one) and rises above its head; the right one is small. It shows in every view where the shoulders are visible, never swapped;
- NOTHING held in the hands.
"""
FEET = R7.FEET
JOBS = (('EN2-L', 'HIS', SHAPER, 'grafted left forearm', 'the grafted arm swaps to the right side, a staff or a book is drawn, the robe reaches below the knee,'),
        ('EN2-U', 'HIS', ASCENDED, 'sun-disc pauldron', 'the pauldron swaps to the right shoulder, a staff is drawn, the robe reaches below the knee,'),
        ('EN2-X', 'ITS', VIGIL, 'brass lantern at the wrist', 'a staff, sword or book is drawn, the mantle reaches below the knee, legs or feet are missing,'),
        ('EN2-D', 'ITS', HULK, 'clock-gear in the shoulder', 'the gear swaps to the right shoulder, legs or feet are missing, a weapon is drawn,'),
        ('EN2-E', 'ITS', COLOSSUS, 'huge left crystal cluster', 'the big cluster is on the right shoulder, legs or feet are missing, a weapon is drawn,'))
if __name__ == '__main__':
    only = sys.argv[1].split(',') if len(sys.argv) > 1 else None
    for tid, who, ch, mk, extra in JOBS:
        if only and tid not in only: continue
        B.write(tid, R7.one(R3.text(tid, who, ch, FEET, extra, mk), tid), [B.STYLE, B.LAYOUT], ['out/%s_a.png' % tid], 2)
