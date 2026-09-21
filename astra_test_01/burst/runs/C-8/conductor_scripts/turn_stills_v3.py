# C-8 attack turnaround, PASS 3 — the plane made a CONSEQUENCE OF ANATOMY, not an absolute height.
# Pass 2 asked for 'the same height in every frame'. Each still is generated independently with no memory of its
# siblings, so a cross-frame absolute is not a constraint the generator can even represent: spread stayed 0.786, and
# the extra wording cost weapon ORIENTATION (fist at the spiked head in b0/b2), weapon COUNT (two maces in b4) and
# brought back the empty pointing hand. Pass 3 instead fixes a per-frame, locally checkable relationship — straight
# arm, locked elbow, angled ~20 deg below level from the shoulder — from which a level sweep plane FOLLOWS, and which
# also answers Matt's actual complaint (the weapon sat at head height because 'shoulder height' on this chibi IS head
# height: crown 1.00, chin 0.753, shoulder ~0.71).
# Pass 1 pinned the mace to "shoulder height". On a chibi the helm spans the top ~25 % of the figure and the
# shoulder line sits at ~0.71 of height, right under the chin — so "shoulder height" IS head height here, and
# because each still was generated independently there was no anchor at all: the measured mace band came out
# 0.181..0.962 of figure height (spread 0.78) against the reference's [0.551, 0.746] (spread 0.195).
# A whirlwind reads as a weapon tracing a LEVEL PLANE. So every frame now pins the mace head to the SAME
# mid-torso height, named by a body landmark instead of by an anatomy word that does not survive the proportions.
import subprocess, sys
B='/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'
REF=f'{B}/runs/C-8/artifacts/seeds/S_battle_p3.png'
LEVEL=("HOW HE HOLDS THE MACE — the same in every frame: his fist is closed around the POMMEL, the plain knob at the BOTTOM END of the haft. "
 "The heavy SPIKED BALL is at the FAR end of the haft, out away from his body — never near his fist, never next to his chest. "
 "His arm is held STRAIGHT, elbow locked, reaching out from the shoulder and angled SLIGHTLY DOWNWARD, about twenty degrees below level, "
 "so that his fist rides a little below his shoulder and the spiked ball ends up LEVEL WITH HIS BELT. The ball is never up beside his helmet, "
 "never above his head, and never down at his knees or dragging on the ground. "
 "There is EXACTLY ONE mace in the picture. Both of his hands are busy: one grips the mace, the other carries the shield. Neither hand is ever "
 "empty, open or pointing, and there is never a second weapon anywhere in the frame.")
HOLD=("He is otherwise IDENTICAL to the reference image: same pixel-art knight, same armour, helm, gold trim, colours, "
 "shield with its dark flame device, ONE spiked mace always GRIPPED FIRMLY IN HIS FIST at the very end of its haft "
 "(his hand is never empty and never pointing), same chunky proportions, same slightly elevated camera. "
 "He stays in the same DEEP BATTLE STANCE — knees bent, hips sunk, feet planted wide, weight low; his helmet stays the "
 "same height above the ground and he is the same size in the frame as the reference. His arm stays straight out from "
 "the shoulder at full reach, so the mace head is far out from his body. "
 "Flat solid pure green #00ff00 background, completely empty. Clean crisp pixel art — no blur, no motion lines, no "
 "swoosh arcs, no rings, no shadow. Wide green margins all round.")
VIEWS=[
 ('b0','facing the viewer, his visor toward us, his shield on the right of the picture. His straight mace arm reaches out to the LEFT of the picture, the mace head far out on the left'),
 ('b1','turned so we see him at three-quarters, his visor still toward us but angled, his shield swung toward the right-hand edge. His straight mace arm reaches out toward the LOWER-LEFT of the picture, the mace head low and far out on the left'),
 ('b2','turned further, his shoulders now nearly side-on with his visor pointing to the left edge of the picture and his shield swung round behind his body. His straight mace arm reaches toward the BOTTOM of the picture, the mace head low and centred just in front of his boots but still far out from his body'),
 ('b3','turned so we see him from the back three-quarter: the back of his helmet toward us, no visor visible, the edge of his shield showing past his left side. His straight mace arm reaches out toward the LOWER-RIGHT of the picture'),
 ('b4','with his BACK fully to us: we see the back of his helmet and the back of his armour, his shield edge-on past his left arm. His straight mace arm reaches straight out to the RIGHT of the picture, the mace head far out on the right'),
 ('b5','turned back toward us from behind, a back three-quarter from the other side: the back of his helmet still toward us but beginning to turn, the face of his shield swinging into view on the left of the picture. His straight mace arm reaches toward the UPPER-RIGHT of the picture'),
 ('b6','nearly side-on again with his visor pointing to the right edge of the picture and the face of his kite shield turned toward us on the left. His straight mace arm reaches toward the TOP of the picture, the mace head high behind his shoulder but still far out from his body'),
 ('b7','almost facing us again, turned slightly to his own right, his visor toward us and his shield on the left of the picture. His straight mace arm reaches out toward the UPPER-LEFT of the picture'),
]
which=sys.argv[1:] or [v[0] for v in VIEWS]
for tag,desc in VIEWS:
    if tag not in which: continue
    prompt=(f"This is one frame of an eight-frame TURNAROUND of the knight in the reference image, spinning on the spot. "
            f"Draw the same knight {desc}. {LEVEL} {HOLD}")
    r=subprocess.run(['zsh',f'{B}/runs/C-8/conductor_scripts/grok_image_ref.sh',f'S_battle_turn_{tag}',REF,prompt],capture_output=True,text=True)
    print(r.stdout.strip() or r.stderr.strip()[:200], flush=True)
