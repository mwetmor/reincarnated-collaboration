# Sequential Grok stills for the Warlord probe directions, driven from python (no shell quoting; prompts are data). usage: e1_turned_stills.py N,SE,NE
import subprocess, sys, pathlib
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst'); REF = B/'runs/C-6/artifacts/E1/e1_pixel_warlord_S_r1.png'
COMMON = ("The SAME pixel-art knight as the reference image - same dark steel armour with brass trim, same round-topped closed helm with the brass crest band, same spiked flanged mace, same large tower shield with the dark horned emblem and brass boss, same palette, same crisp 16-bit overworld-sprite pixel style, same size in the frame - "
          "SAME VIEW FROM ABOVE as the reference: bird's-eye three-quarter, the round TOP of the helm dominant, pauldron tops visible, torso and legs short and compressed, small boots. Standing at rest. Flat solid bright green background, no shadow, no ground, no text. Tall portrait image.")
TURN = {'N': "TURNED to face AWAY from the viewer (up-screen, a back view): we see the back of his helm and the back of his cuirass, the shield on his left arm on the screen-left side, the mace in his right hand on the screen-right side. ",
        'SE': "TURNED 45 degrees toward the viewer's lower-RIGHT (a front three-quarter view facing down-right): his right side nearer, the mace in his near right hand, the shield on his far left arm. ",
        'NE': "TURNED 45 degrees AWAY toward the screen's upper-RIGHT (a back three-quarter view facing up-right): we see his back and his right side, the mace in his right hand on the near side, the shield on his far left arm mostly hidden. "}
for d in sys.argv[1].split(','):
    r = subprocess.run([str(B/'runs/C-6/conductor_scripts/grok_image_ref.sh'), f'E1_pixel_warlord_{d}', str(REF), TURN[d] + COMMON], capture_output=True, text=True)
    print(r.stdout.strip()[-200:], r.stderr.strip()[-200:], flush=True)
