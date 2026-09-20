# Conductor data: Run C-8 (EoR Warlord) Grok prompts — C-3/C-6 skeleton in the pixel-overworld regime; camera-never-changes clause (E1 result).
import json, hashlib, pathlib
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
FACING = {
 'S':  ('facing the viewer (down-screen) and he keeps facing the viewer for the whole clip', 'in place toward the viewer'),
 'SW': ("turned three-quarters toward the screen's LOWER-LEFT for the whole clip", "in place toward the screen's lower-left"),
 'W':  ('in full LEFT-facing side view for the whole clip', 'in place toward screen-left'),
 'NW': ("in a back three-quarter view facing the screen's UPPER-LEFT, away from the viewer, for the whole clip", "in place away from the viewer toward the screen's upper-left"),
 'N':  ('with his back to the viewer, facing directly up-screen, for the whole clip', 'in place directly away from the viewer'),
 'NE': ("in a back three-quarter view facing the screen's UPPER-RIGHT, away from the viewer, for the whole clip", "in place away from the viewer toward the screen's upper-right"),
 'E':  ('in full RIGHT-facing side view for the whole clip', 'in place toward screen-right'),
 'SE': ("turned three-quarters toward the screen's LOWER-RIGHT for the whole clip", "in place toward the screen's lower-right"),
}
PLATE = 'on a flat solid pure green (#00ff00) background that stays completely unchanged and empty (no scenery, no shadows, no particles, no glow). Camera locked, no zoom, no pan; the figure stays centred at the same size.'
STYLE = 'PIXEL ART animation in the style of a 16-bit top-down action-RPG overworld sprite: crisp hard-edged pixels, limited palette, no smoothing, no anti-aliasing, the same blocky pixel look in every frame. THE CAMERA ANGLE NEVER CHANGES: he is seen from HIGH ABOVE exactly as in the first frame for the entire clip — the round TOP of the helm stays the largest part of the head, the tops of the pauldrons stay visible, the torso and legs stay short and compressed; he is never redrawn taller, more upright, or from a lower angle. Same closed helm with the brass crest band, same dark steel and brass armour, same spiked flanged mace in his right hand, same tower shield with the dark horned emblem on his left arm, in every frame. One continuous shot, no cuts.'
ANIM = {
 'walk': ('The armoured knight walks {W}, {F}, {P} A steady, heavy, armoured walk cycle in place: the feet lift and plant clearly, the planted foot sliding back under the body like a treadmill; the whole body rides gently up and down with the stride; the mace and shield sway only a little. {S} Loop: the last frame matches the first.'),
 'run':  ('The armoured knight runs {W}, {F}, {P} A heavy charging run in place, longer stride than a walk, torso leaning slightly forward, feet clearly leaving the ground on every stride, the planted foot driving back under the body like a treadmill; the shield held up in front, the mace pumping with the stride. {S} Loop: the last frame matches the first.'),
 'idle': ('The armoured knight stands at ease and breathes, {F}, {P} From the first frame he lowers the mace so its spiked head rests on the ground beside his right boot, the shield lowered and relaxed on his left arm; then he stands STILL for the rest of the clip and breathes — a slow, calm, CLEARLY VISIBLE breath, drawn a third bigger than life the way hand-drawn game animation does it: the shoulders and cuirass rise on the inhale and settle on the exhale, once every two seconds; nothing else moves. THE FIGURE STAYS EXACTLY THE SAME SIZE AND POSITION from first frame to last. NO NEW OBJECTS APPEAR. {S} Loop: the last frame matches the first still frame after the mace is grounded.'),
 'attack': ('The armoured knight, {F}, {P} From a standing guard he SPINS in place in a continuous whirlwind — the Eye of Reckoning: he pivots around his own centre at a constant fast rate of {SPIN}, the spiked mace swung out at arm\'s length in a level horizontal arc and the tower shield sweeping round with him, boots shuffling on the spot; the spin is smooth and constant from the first frame to the last, never slowing, never stopping, no wind-up and no recovery in this clip. He stays exactly the same size and position; only he rotates. {S} Loop: the last frame matches the first.'),
 'cast': ('The armoured knight, {F}, {P} From a standing guard: he draws the shield back, then SLAMS it forward in the direction he faces with a short stamp of the front foot while thrusting the mace forward beside it — the mace head pointing straight at the target for a beat (a small brief pale glint on the mace head; no particles leave it, nothing touches the background) — then he recovers to the same standing guard and holds still for the rest of the clip. ONE slam only. {S} The clip ends on the standing guard it began with.'),
 'jump': ('The armoured knight, {F}, {P} From a standing guard: he crouches, launches straight up, reaches the apex with knees tucked, lands on the same spot into a crouch and stands back up to the same guard — ONE heavy armoured jump, then he stands still for the rest of the clip. Mace and shield stay in hand throughout. {S} The clip ends on the standing guard it began with.'),
}
SPIN = 'SPIN_RATE_PLACEHOLDER'
import sys
if len(sys.argv) > 1: SPIN = sys.argv[1]
out = {'provenance': 'Run C-8 charter (Matt rulings R-C8-0, W1–W6); C-3 § 6 / C-6 skeleton; E1 camera-never-changes clause; attack spin rate from the wwcr whirlwind VFX', 'duration_s': 6, 'resolution': '720p', 'spin_rate': SPIN, 'cells': {}}
for d, (F, W) in FACING.items():
    for a, tpl in ANIM.items():
        p = tpl.format(F=F, W=W, P=PLATE, S=STYLE, SPIN=SPIN)
        out['cells'][f'{d}_{a}'] = {'prompt': p, 'sha256': hashlib.sha256(p.encode()).hexdigest()}
json.dump(out, open(B/'runs/C-8/matrix_prompts.json', 'w'), indent=1, ensure_ascii=False)
print(len(out['cells']), 'prompts; spin', SPIN)
