# C-8 attack redesign, TURNAROUND-AS-SPIN technique (R-C8-5): a whirlwind and a turnaround are the same artifact.
# Instead of asking image_to_video for a 6 s spin (four passes each won one attribute and relaxed the others),
# draw the revolution as 8 deliberate stills at 45 deg, every one gated by the conductor eye, identity carried by
# a constant reference. 8 frames = one revolution; at 2.5 rev/s that is 20 fps. Phase-roll (R-C8-4) then yields all
# eight direction cells from this single revolution.
import json, subprocess, sys, pathlib
B='/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'
REF=f'{B}/runs/C-8/artifacts/seeds/S_battle_p3.png'
VIEWS=[
 ('01','has turned 45 degrees to his own left, so we see him from the front-right three-quarter: his chest angled toward the lower-left of the picture. His extended mace arm swings with him and now reaches out toward the LOWER-LEFT, the mace head nearer the bottom-left of the frame and slightly in front of him'),
 ('02','has turned 90 degrees to his own left, so his right side faces us in full profile, his chest pointing to the LEFT of the picture. His extended mace arm now points almost straight TOWARD the camera, so it is strongly foreshortened: we see the mace head large and low, close in front of his chest, with only a short length of haft visible'),
 ('03','has turned 135 degrees to his own left, so we see him from the back-right three-quarter: his shoulders angled away, the back of his helmet and the back edge of his shield visible. His extended mace arm reaches out toward the LOWER-RIGHT of the picture'),
 ('04','has turned 180 degrees and now has his BACK fully to us: we see the back of his helmet and the back of his armour, his shield edge-on behind his left arm. His extended mace arm reaches straight out to the RIGHT of the picture, the mace head far out on the right'),
 ('05','has turned 225 degrees, so we see him from the back-left three-quarter, still mostly from behind but turning back toward us. His extended mace arm reaches out toward the UPPER-RIGHT of the picture'),
 ('06','has turned 270 degrees, so his left side faces us in full profile, his chest pointing to the RIGHT of the picture, the face of his shield toward the camera. His extended mace arm points almost straight AWAY from the camera, so it is strongly foreshortened: only a short length of haft and a small mace head are visible just behind his shoulder'),
 ('07','has turned 315 degrees, so we see him from the front-left three-quarter, chest angled toward the lower-right, nearly facing us again. His extended mace arm reaches out toward the UPPER-LEFT of the picture'),
]
HOLD=("In every other respect he is IDENTICAL to the reference image and to the other frames of this turnaround: the same pixel-art knight, same armour, helm, gold trim, colours, shield with its dark flame device, one spiked mace, same chunky proportions, same slightly elevated camera height. "
 "He stays in the SAME DEEP BATTLE STANCE as the reference — knees bent, hips sunk, feet planted wide, weight low; his helmet stays at exactly the same height above the ground as in the reference, and he is exactly the same size in the frame. "
 "His fist stays closed around the VERY END of the haft at the pommel, and his arm stays LOCKED STRAIGHT out from the shoulder at shoulder height — never bent at the elbow, never raised beside or above his helmet. "
 "Flat solid pure green #00ff00 background, completely empty. Clean crisp pixel art, no blur, no motion lines, no swoosh arcs, no rings, no shadow. Draw him the same modest size with wide green margins all round.")
which=sys.argv[1:] or [v[0] for v in VIEWS]
for tag, desc in VIEWS:
    if tag not in which: continue
    prompt=(f"This is frame {tag} of an eight-frame TURNAROUND of the knight in the reference image, spinning on the spot. "
            f"Draw the same knight after he {desc}. {HOLD}")
    name=f'S_battle_turn_{tag}'
    r=subprocess.run(['zsh',f'{B}/runs/C-8/conductor_scripts/grok_image_ref.sh',name,REF,prompt],capture_output=True,text=True)
    print((r.stdout.strip() or r.stderr.strip()[:200]), flush=True)
