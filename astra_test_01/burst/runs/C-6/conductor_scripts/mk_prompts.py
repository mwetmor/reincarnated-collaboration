# Conductor data: Run C-6 matrix Grok prompts — C-3 § 6 skeleton (mk_prompts.py lineage: C-2 R-48/R-50/R-55 prompts, gaze line R-51,
# cast surge reduced to a glint R-C3-3) with the Necromancer identity line and the scythe held two-handed, blade up (charter § 4 P3).
import json, hashlib, pathlib
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
FACING = {
 'S':  ('facing the camera (toward the viewer) and he keeps facing the camera for the whole clip', 'in place toward the viewer'),
 'SW': ("turned three-quarters toward the screen's LOWER-LEFT — body and head face the lower-left for the whole clip", "in place toward the screen's lower-left"),
 'W':  ('in full LEFT-facing profile — he faces screen-left and keeps facing screen-left for the whole clip', 'in place toward screen-left'),
 'NW': ("in a back three-quarter view facing the screen's UPPER-LEFT, away from the camera — he keeps that facing for the whole clip and never turns his face to the camera", "in place away from the camera toward the screen's upper-left"),
 'N':  ('with his back to the camera, facing directly away from the viewer — he keeps his back to the camera for the whole clip and never turns around', 'in place directly away from the camera'),
 'NE': ("in a back three-quarter view facing the screen's UPPER-RIGHT, away from the camera — he keeps that facing for the whole clip and never turns his face to the camera", "in place away from the camera toward the screen's upper-right"),
 'E':  ('in full RIGHT-facing profile — he faces screen-right and keeps facing screen-right for the whole clip', 'in place toward screen-right'),
 'SE': ("turned three-quarters toward the screen's LOWER-RIGHT — body and head face the lower-right for the whole clip", "in place toward the screen's lower-right"),
}
PLATE = 'on a flat solid pure green (#00ff00) background that stays completely unchanged and empty (no scenery, no shadows, no particles, no glow). Camera locked, no zoom, no pan; the figure stays centred at the same size.'
SAME = 'Same face, same long white hair, same black bone-plate armour, same horn on his left shoulder, same tome at his left hip, same great scythe in every frame — the scythe stays in BOTH hands with the blade up, exactly as in the first frame. Hand-drawn 2D animation, one continuous shot, no cuts.'
GAZE = 'His eyes are on the horizon from the FIRST frame, head level, looking ahead in the direction he faces — never looking down at the ground or at his feet.'
ANIM = {
 'idle': ('The character stands still and breathes, {F}, {P} A slow, calm, CLEARLY VISIBLE relaxed breath, drawn about a third bigger than life the way hand-drawn game animation does it: the torso and shoulders rise and broaden on the inhale and settle on the exhale, once every two seconds; the head rides gently with the breath and does not turn; the scythe rides with the shoulders, both hands on the haft, the blade up. {G} {S} Loop: the last frame matches the first.'),
 'walk': ('The character walks {W}, {F}, {P} A natural, heavy, deliberate walk cycle in place: the feet lift and plant clearly, the planted foot sliding back under the body like a treadmill; the head bobs down into each footfall and rises through the passing position, twice per stride; both hands keep the scythe across the body, the blade up, swaying only a little with the shoulders. {G} {S} Loop: the last frame matches the first.'),
 'run': ('The character runs {W}, {F}, {P} A brisk run in place, longer stride than a walk, torso leaning slightly forward, feet clearly leaving the ground on every stride, the planted foot driving back under the body like a treadmill; both hands carry the scythe across the body angled forward as he runs, the blade up. {G} {S} Loop: the last frame matches the first.'),
 'jump': ('The character, {F}, {P} From a standing rest: he crouches, launches straight up, reaches the apex with knees tucked, lands on the same spot into a crouch and stands back up to the same rest pose — ONE jump, then he stands still for the rest of the clip. The scythe stays in both hands, blade up, throughout. {G} {S} The clip ends on the standing rest pose it began with.'),
 'cast': ('The character, {F}, {P} From a standing rest: he raises the scythe two-handed so the blade rises higher, a small brief pale glint gathers on the blade (no particles leave the blade, nothing touches the background), he sweeps the blade forward in the direction he faces to release the spell, then returns to the same standing rest pose — ONE cast, then he stands still for the rest of the clip. Both hands stay on the haft. {G} {S} The clip ends on the standing rest pose it began with.'),
}
out = {'provenance': 'Run C-6 charter § 4 P3 (C-3 § 6 skeleton + necro identity line + "the scythe stays in both hands, blade up"); cast glint on the blade (R-C3-3: plate stays empty for the matte; C-5 kits erupt at the blade socket in P5)', 'duration_s': 6, 'resolution': '720p', 'cells': {}}
for d, (F, W) in FACING.items():
    for a, tpl in ANIM.items():
        p = tpl.format(F=F, W=W, P=PLATE, G=GAZE, S=SAME)
        out['cells'][f'{d}_{a}'] = {'prompt': p, 'sha256': hashlib.sha256(p.encode()).hexdigest()}
json.dump(out, open(B/'runs/C-6/matrix_prompts.json', 'w'), indent=1, ensure_ascii=False)
print(len(out['cells']), 'prompts;', 'E_cast:', out['cells']['E_cast']['prompt'][:160])
