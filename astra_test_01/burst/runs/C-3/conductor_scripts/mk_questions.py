# Conductor data: closed YES/NO motion-question sets per animation kind for P4 TRANSCRIBE (X0-M family; presence/absence only, never coordinates).
import json, pathlib
Q = {
 'common': [
  ('same_facing', 'Does the figure face the same direction in every frame (no turning toward or away from the camera)?', 'yes'),
  ('staff_same_hand', 'Is the staff held by the same hand in every frame?', 'yes'),
  ('identity_stable', 'Are the face (where visible), hair, costume and colours the same in every frame (no redrawn features, no changing items)?', 'yes'),
  ('head_down_frame0', 'In frame 0, is the head tilted down so the gaze points at the ground?', 'no'),
  ('plate_clean', 'Is every frame free of scenery, floor shadow, particles or glow outside the figure?', 'yes'),
  ('size_stable', 'Is the figure the same size in every frame?', 'yes'),
 ],
 'idle': [
  ('feet_move', 'Do either of the feet change position between any two frames?', 'no'),
  ('breath_visible', 'Do the shoulders/torso visibly rise and settle across the frames?', 'yes'),
  ('head_turns', 'Does the head turn to face a different direction in any frame?', 'no'),
  ('loop_continuous', 'Does the last frame lead naturally back into frame 0 (no jump in pose)?', 'yes'),
 ],
 'walk': [
  ('feet_alternate', 'Do the two legs take turns stepping forward across the frames?', 'yes'),
  ('head_bobs', 'Does the head move up and down across the frames?', 'yes'),
  ('free_arm_swings', 'Does the arm without the staff swing forward and back?', 'yes'),
  ('both_feet_air', 'Is there any frame where both feet are clearly off the ground?', 'no'),
  ('loop_continuous', 'Does the last frame lead naturally back into frame 0 (no jump in pose)?', 'yes'),
 ],
 'run': [
  ('feet_alternate', 'Do the two legs take turns driving forward across the frames?', 'yes'),
  ('both_feet_air', 'Is there any frame where both feet are clearly off the ground?', 'yes'),
  ('torso_lean', 'Does the torso lean forward in the direction of travel?', 'yes'),
  ('loop_continuous', 'Does the last frame lead naturally back into frame 0 (no jump in pose)?', 'yes'),
 ],
 'jump': [
  ('crouch_before', 'Is there a crouch before the figure leaves the ground?', 'yes'),
  ('airborne', 'Is there a frame where both feet are clearly off the ground?', 'yes'),
  ('lands_crouch', 'Is there a landing crouch after the airborne frames?', 'yes'),
  ('ends_rest', 'Does the last frame show the same standing rest pose as frame 0?', 'yes'),
 ],
 'cast': [
  ('staff_raised', 'Is the staff raised above its rest position in some frame?', 'yes'),
  ('two_handed', 'Are both hands on the staff in some frame?', 'yes'),
  ('thrust_forward', 'Is the staff pushed toward the direction the figure faces in some frame?', 'yes'),
  ('ends_rest', 'Does the last frame show the same standing rest pose as frame 0?', 'yes'),
 ],
 'control': [
  ('shield_present', 'Does the figure carry a shield in any frame?', 'no'),
  ('helmet_present', 'Does the figure wear a helmet in any frame?', 'no'),
 ],
}
out = {}
for k in ('idle', 'walk', 'run', 'jump', 'cast'):
    items = [{'id': i, 'question': q, 'expected': e, 'class': 'motion'} for i, q, e in Q['common'] + Q[k]]
    items += [{'id': i, 'question': q, 'expected': e, 'class': 'declared_absent_control'} for i, q, e in Q['control']]
    out[k] = {'answers': ['yes', 'no', 'cannot tell'], 'items': items}
json.dump({'provenance': 'Run C-3 P4 X0-M closed question sets (conductor data); expected answers are the INTENT, not a verdict; controls must answer no', 'sets': out}, open(S/'..'/'scratchpad'/'matrix_questions.json' if False else pathlib.Path(__file__).with_name('matrix_questions.json'), 'w'), indent=1)
print({k: len(v['items']) for k, v in out.items()})
