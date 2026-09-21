# C-8 attack turnaround, PASS 2 — the LEVEL SWEEP PLANE fix (Matt eye 2026-09-21).
# Pass 1 pinned the mace to "shoulder height". On a chibi the helm spans the top ~25 % of the figure and the
# shoulder line sits at ~0.71 of height, right under the chin — so "shoulder height" IS head height here, and
# because each still was generated independently there was no anchor at all: the measured mace band came out
# 0.181..0.962 of figure height (spread 0.78) against the reference's [0.551, 0.746] (spread 0.195).
# A whirlwind reads as a weapon tracing a LEVEL PLANE. So every frame now pins the mace head to the SAME
# mid-torso height, named by a body landmark instead of by an anatomy word that does not survive the proportions.
import subprocess, sys
B='/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'
REF=f'{B}/runs/C-8/artifacts/seeds/S_battle_p3.png'
LEVEL=("CRITICAL — THE HEIGHT OF THE MACE: the mace head must sit at the MIDDLE OF HIS CHEST, half way between his belt "
 "and his chin. It is NEVER up beside his helmet, NEVER above his head, and NEVER down by his knees or the ground. "
 "In every frame of this turnaround the mace head stays at that SAME height above the ground — he is sweeping it "
 "around himself in one flat level circle, like a hammer thrower, so its height never changes as he turns.")
HOLD=("He is otherwise IDENTICAL to the reference image: same pixel-art knight, same armour, helm, gold trim, colours, "
 "shield with its dark flame device, ONE spiked mace always GRIPPED FIRMLY IN HIS FIST at the very end of its haft "
 "(his hand is never empty and never pointing), same chunky proportions, same slightly elevated camera. "
 "He stays in the same DEEP BATTLE STANCE — knees bent, hips sunk, feet planted wide, weight low; his helmet stays the "
 "same height above the ground and he is the same size in the frame as the reference. His arm stays straight out from "
 "the shoulder at full reach, so the mace head is far out from his body. "
 "Flat solid pure green #00ff00 background, completely empty. Clean crisp pixel art — no blur, no motion lines, no "
 "swoosh arcs, no rings, no shadow. Wide green margins all round.")
VIEWS=[
 ('a0','facing the viewer, his visor toward us, his shield on the right of the picture. His straight mace arm reaches out to the LEFT of the picture, the mace head far out on the left'),
 ('a1','turned so we see him at three-quarters, his visor still toward us but angled, his shield swung toward the right-hand edge. His straight mace arm reaches out toward the LOWER-LEFT of the picture, the mace head low and far out on the left'),
 ('a2','turned further, his shoulders now nearly side-on with his visor pointing to the left edge of the picture and his shield swung round behind his body. His straight mace arm reaches toward the BOTTOM of the picture, the mace head low and centred just in front of his boots but still far out from his body'),
 ('a3','turned so we see him from the back three-quarter: the back of his helmet toward us, no visor visible, the edge of his shield showing past his left side. His straight mace arm reaches out toward the LOWER-RIGHT of the picture'),
 ('a4','with his BACK fully to us: we see the back of his helmet and the back of his armour, his shield edge-on past his left arm. His straight mace arm reaches straight out to the RIGHT of the picture, the mace head far out on the right'),
 ('a5','turned back toward us from behind, a back three-quarter from the other side: the back of his helmet still toward us but beginning to turn, the face of his shield swinging into view on the left of the picture. His straight mace arm reaches toward the UPPER-RIGHT of the picture'),
 ('a6','nearly side-on again with his visor pointing to the right edge of the picture and the face of his kite shield turned toward us on the left. His straight mace arm reaches toward the TOP of the picture, the mace head high behind his shoulder but still far out from his body'),
 ('a7','almost facing us again, turned slightly to his own right, his visor toward us and his shield on the left of the picture. His straight mace arm reaches out toward the UPPER-LEFT of the picture'),
]
which=sys.argv[1:] or [v[0] for v in VIEWS]
for tag,desc in VIEWS:
    if tag not in which: continue
    prompt=(f"This is one frame of an eight-frame TURNAROUND of the knight in the reference image, spinning on the spot. "
            f"Draw the same knight {desc}. {LEVEL} {HOLD}")
    r=subprocess.run(['zsh',f'{B}/runs/C-8/conductor_scripts/grok_image_ref.sh',f'S_battle_turn_{tag}',REF,prompt],capture_output=True,text=True)
    print(r.stdout.strip() or r.stderr.strip()[:200], flush=True)
