# EN-E2 round 6 (conductor, 2026-10-02): the LAST tier-1 rig, #17 `chthonianrylok` (3.5 bodies incl. BOSS records; melee 42 / projectile 28 /
# aoe 27 %; p05 1.0). A towering VOID-TOUCHED horned humanoid of the crypt depths, a boss-grade silhouette. Original; generic descriptors only.
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
B = __import__('en01_briefs'); R3 = __import__('en23_briefs_r3')
VOID = """THE CHARACTER, a VOID-TOUCHED HORNED LORD: a towering thing that climbed out of the deepest crypt under the cathedral, where the dark below the world leaks through:
- TOWERING: about one and a half times a man's height, a long powerful body, broad high shoulders, a narrow waist, long muscular arms that reach to mid-thigh ending in long four-fingered hands with long dark claws, long digitless-looking but HUMAN-JOINTED legs (knees bend forward) ending in broad clawed feet; it stands tall and upright, a lord, not a beast;
- its skin is a deep VIOLET-INDIGO, laid as layered transparent washes with pale violet-grey highlights on every ridge of muscle (never a flat black fill), cracked all over with thin pale VIOLET-WHITE seams like breaking stone (painted as pale colour, never a glow);
- the head: a long narrow armoured skull-face with no nose, deep-set small pale violet-white eyes, a lipless mouth of long thin teeth; two GREAT HORNS of dark bone sweep back from the brow and curl forward again beside the jaw, ridged and heavy, the same in every view;
- a row of short dark bone SPINES down the spine from the neck to the small of the back; ragged bone plates on the shoulders;
- the Keepers' relics on it: a broken brass HOUR-RING (a hand-span disc of engraved tarnished brass) driven into the centre of its chest, the flesh grown round it; a torn war-skirt of faded LAPIS Keeper banners hanging from a heavy belt of chain and brass to the knee, front and back, open at the sides;
- ASYMMETRY MARKER: a heavy BRASS RING clamped around its LEFT horn ONLY, near the base, a short length of broken chain hanging from it; the right horn is bare bone. It shows in every view where the left horn is visible, and never on the right;
- NO wings, NO tail; NOTHING held in the hands.
"""
FEET = ("Legs straight, feet a little apart and pointing forward, soles on one ground line per row; a clear gap of green between the legs. The horns fit "
        "inside the quarter (scale the figure down slightly if they would be cut off). The long arms hang AWAY from the body: a clear gap of green between each arm and the body.")
if __name__ == '__main__':
    B.write('EN2-V', R3.text('EN2-V', 'ITS', VOID, FEET, "the brass ring swaps to the right horn or is missing, wings or a tail appear, the horns are cut off,", 'brass horn-ring'),
            [B.STYLE, B.LAYOUT], ['out/EN2-V_a.png', 'out/EN2-V_b.png'], 4)
