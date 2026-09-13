# Conductor data: Run C-3 matrix Grok prompts (charter § 6 skeleton + C-2 passed prompts + R-51 gaze line). Not lane code.
import json, hashlib, pathlib
B = pathlib.Path('/Users/admin/Games/reincarnated-collaboration/astra_test_01/burst')
FACING = {
 'S':  ('facing the camera (toward the viewer) and she keeps facing the camera for the whole clip', 'in place toward the viewer'),
 'SW': ("turned three-quarters toward the screen's LOWER-LEFT — body and head face the lower-left for the whole clip", "in place toward the screen's lower-left"),
 'W':  ('in full LEFT-facing profile — she faces screen-left and keeps facing screen-left for the whole clip', 'in place toward screen-left'),
 'NW': ("in a back three-quarter view facing the screen's UPPER-LEFT, away from the camera — she keeps that facing for the whole clip and never turns her face to the camera", "in place away from the camera toward the screen's upper-left"),
 'N':  ('with her back to the camera, facing directly away from the viewer — she keeps her back to the camera for the whole clip and never turns around', 'in place directly away from the camera'),
 'NE': ("in a back three-quarter view facing the screen's UPPER-RIGHT, away from the camera — she keeps that facing for the whole clip and never turns her face to the camera", "in place away from the camera toward the screen's upper-right"),
 'E':  ('in full RIGHT-facing profile — she faces screen-right and keeps facing screen-right for the whole clip', 'in place toward screen-right'),
 'SE': ("turned three-quarters toward the screen's LOWER-RIGHT — body and head face the lower-right for the whole clip", "in place toward the screen's lower-right"),
}
PLATE = 'on a flat solid pure green (#00ff00) background that stays completely unchanged and empty (no scenery, no shadows, no particles, no glow). Camera locked, no zoom, no pan; the figure stays centred at the same size.'
SAME = 'Same face, same hair, same costume, same colours, same staff (in her right hand) and satchel (on her left hip) in every frame. Hand-drawn 2D animation, one continuous shot, no cuts.'
GAZE = 'Her eyes are on the horizon from the FIRST frame, head level, looking ahead in the direction she faces — never looking down at the ground or at her feet.'
ANIM = {
 'idle': ('The character stands still and breathes, {F}, {P} A slow, calm, CLEARLY VISIBLE relaxed breath, drawn about a third bigger than life the way hand-drawn game animation does it: the torso and shoulders rise and broaden on the inhale and settle on the exhale, once every two seconds; the head rides gently with the breath and does not turn; {G} The staff stays planted in her right hand; both feet stay planted and never slide; the belt, satchel and legs barely move. {S} Loop: the last frame matches the first.'),
 'walk': ('The character walks {W}, {F}, {P} A natural, confident, weighty walk cycle in place: the feet lift and plant clearly, the planted foot sliding back under the body like a treadmill; the head bobs down into each footfall and rises through the passing position, twice per stride; the free left arm swings opposite the legs; the right arm holds the staff upright and swings only a little. {G} {S} Loop: the last frame matches the first.'),
 'run': ('The character runs {W}, {F}, {P} A brisk run in place, longer stride than a walk, arms pumping, torso leaning slightly forward, feet clearly leaving the ground on every stride, the planted foot driving back under the body like a treadmill; the right hand carries the staff angled forward as she runs. {G} {S} Loop: the last frame matches the first.'),
 'jump': ('The character, {F}, {P} From a standing rest: she crouches, launches straight up, reaches the apex with knees tucked, lands on the same spot into a crouch and stands back up to the same rest pose — ONE jump, then she stands still for the rest of the clip. The staff stays in her right hand throughout. {G} {S} The clip ends on the standing rest pose it began with.'),
 'cast': ('The character, {F}, {P} From a standing rest: she raises the staff two-handed, a small brief pale glint gathers at the staff tip (no particles leave the staff, nothing touches the background), she thrusts the staff forward in the direction she faces to release the spell, then returns to the same standing rest pose — ONE cast, then she stands still for the rest of the clip. {G} {S} The clip ends on the standing rest pose it began with.'),
}
out = {'provenance': 'Run C-3 charter § 6; C-2 grok_idle.sh / grok_walk.sh (R-48/R-50/R-55); gaze line R-51; cast surge reduced to a glint (R-C3-3: plate must stay empty for the matte; the frost bolt is composited in P5)', 'duration_s': 6, 'resolution': '720p', 'cells': {}}
for d, (F, W) in FACING.items():
    for a, tpl in ANIM.items():
        p = tpl.format(F=F, W=W, P=PLATE, G=GAZE, S=SAME)
        out['cells'][f'{d}_{a}'] = {'prompt': p, 'sha256': hashlib.sha256(p.encode()).hexdigest()}
json.dump(out, open(B/'runs/C-3/matrix_prompts.json', 'w'), indent=1, ensure_ascii=False)
print(len(out['cells'])); print(out['cells']['E_cast']['prompt'])
