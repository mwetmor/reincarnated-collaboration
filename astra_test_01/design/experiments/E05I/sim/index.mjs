// Pure fixture state. Rendering consumes these JSON values; it cannot commit heading.
const wrap = angle => ((angle % 360) + 360) % 360;
function finite(value) {
  if (typeof value === 'number' && !Number.isFinite(value)) throw Error('Nonfinite state');
  if (value === null || ['number','string','boolean'].includes(typeof value)) return;
  if (typeof value !== 'object' || (!Array.isArray(value) && Object.getPrototypeOf(value) !== Object.prototype)) throw Error('Not plain JSON');
  for (const v of Object.values(value)) finite(v);
}
export function validate(state) {
  finite(state);
  if (!state || !['idle', 'turn_left', 'turn_right'].includes(state.action)) throw Error('Bad action');
  if (!Array.isArray(state.root) || state.root.length !== 2 || !state.root.every(Number.isFinite)) throw Error('Bad root');
  for (const name of ['heading_deg', 'start_heading_deg', 'target_heading_deg']) {
    if (!Number.isInteger(state[name]) || state[name] < 0 || state[name] >= 360 || state[name] % 45) throw Error('Bad heading');
  }
  if (!Number.isFinite(state.elapsed_s) || state.elapsed_s < 0 || !Number.isFinite(state.duration_s) || state.duration_s <= 0) throw Error('Bad timing');
  if (!Number.isSafeInteger(state.turn_id) || state.turn_id < 0 || !Array.isArray(state.events)) throw Error('Bad identity/events');
  if (state.action === 'idle') {
    if (state.elapsed_s !== 0 || state.start_heading_deg !== state.heading_deg || state.target_heading_deg !== state.heading_deg) throw Error('Bad idle snapshot');
  } else {
    const delta = state.action === 'turn_left' ? 45 : -45;
    if (state.heading_deg !== state.start_heading_deg || state.target_heading_deg !== wrap(state.start_heading_deg + delta) || state.elapsed_s >= state.duration_s) throw Error('Bad active snapshot');
  }
  for (const event of state.events) {
    if (!event || event.type !== 'turn_complete' || !/^turn-\d+$/.test(event.id) || !Number.isFinite(event.at_s) || event.at_s <= 0 || !Number.isInteger(event.heading_deg) || event.heading_deg < 0 || event.heading_deg >= 360 || event.heading_deg % 45) throw Error('Bad event');
  }
  return state;
}
export function createState(root = [0, 0], heading = 0) {
  return validate({action:'idle', root:[...root], heading_deg:heading, start_heading_deg:heading, target_heading_deg:heading, elapsed_s:0, duration_s:0.6, turn_id:0, events:[]});
}
export function step(input, command, content) {
  validate(input);
  if (input.action !== 'idle' && content.clips[input.action]?.duration_s !== input.duration_s) throw Error('Content/state duration mismatch');
  const state = structuredClone(input);
  state.events = [];
  if (command.type === 'turn') {
    if (state.action !== 'idle') throw Error('Turn already active');
    if (!['left', 'right'].includes(command.direction)) throw Error('Bad turn direction');
    const action = 'turn_' + command.direction, clip = content.clips[action];
    const delta = command.direction === 'left' ? 45 : -45;
    if (!clip || clip.heading_delta_deg !== delta || !Number.isFinite(clip.duration_s) || clip.duration_s <= 0) throw Error('Incompatible turn content');
    state.action = action;
    state.start_heading_deg = state.heading_deg;
    state.target_heading_deg = wrap(state.heading_deg + delta);
    state.duration_s = clip.duration_s;
    state.elapsed_s = 0;
    state.turn_id++;
  } else if (command.type === 'advance') {
    if (!Number.isFinite(command.dt) || command.dt < 0 || command.dt > 10) throw Error('Bad dt');
    if (state.action !== 'idle') {
      state.elapsed_s += command.dt;
      if (state.elapsed_s >= state.duration_s) {
        state.heading_deg = state.target_heading_deg;
        state.events.push({type:'turn_complete', id:'turn-'+state.turn_id, at_s:state.duration_s, heading_deg:state.heading_deg});
        state.action = 'idle';
        state.start_heading_deg = state.heading_deg;
        state.elapsed_s = 0;
      }
    }
  } else throw Error('Bad command');
  return validate(state);
}
