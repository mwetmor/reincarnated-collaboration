import {createState as baseState, step as baseStep, obstacles as baseObstacles} from '../../E07D/sim/index.mjs';
import {Chamber} from '../../E04/sim/chamber.mjs';
export const doorObject = content => content.layout.objects.find(o => o.id === 'door');
const model = (content, saved) => new Chamber(content.layout, saved ? JSON.stringify(saved) : null);
function finiteJSON(value) { if (typeof value === 'number' && !Number.isFinite(value)) throw Error('Nonfinite JSON'); if (value && typeof value === 'object') for (const v of Object.values(value)) finiteJSON(v); }
export function createState(content, saved = null) {
 const s = baseState(content, saved); finiteJSON(s);
 if (!s.chamber || s.chamber.schema !== 1 || !Number.isFinite(s.chamber.time) || s.chamber.time < 0) throw Error('Invalid time/schema');
 const c = s.chamber, d = c.state.door, p = c.pending; model(content, c);
 if (!['intact','broken'].includes(c.state.crate) || !['closed','open','looted'].includes(c.state.chest) || !['absent','ground','picked'].includes(c.state.loot) || !['rewards','picked','events'].every(k=>Array.isArray(c.state[k])) || !Array.isArray(s.outcomes)) throw Error('Invalid prop/event state');
 if (['opening','closing'].includes(d)) { if (!p || p.state !== (d === 'opening' ? 'open' : 'closed') || !Number.isFinite(p.at) || p.at <= c.time || p.at > c.time + .5 + 1e-8) throw Error('Invalid pending transition'); }
 else if (p !== null) throw Error('Unexpected pending transition');
 if (!Object.values(s.doors).every(x => ['open','closed'].includes(x)) || !['west','east'].every(k => k in s.doors)) throw Error('Invalid exit state');
 for (const a of content.layout.actors) { const v = s.actors[a.id]; if (!v || !Array.isArray(v.point) || v.point.length !== 2 || !v.point.every(Number.isFinite) || v.height !== a.height || v.radius !== a.radius) throw Error('Invalid actor'); }
 if (!Number.isInteger(c.state.navVersion) || c.state.navVersion < 0) throw Error('Invalid nav version');
 return s;
}
export function contentFor(state, content, forceClosed = false) {
 const c = structuredClone(content), o = doorObject(c);
 if (state.chamber.state.door !== 'open' || forceClosed) for (const [id,f] of Object.entries(c.factions)) f.objects.push({id:'internal-leaf',role:'door',bounds:[[o.rect[0],o.rect[1],0],[o.rect[2],o.rect[3],o.height]],material_id:id==='F01'?'timber':'iron'});
 return c;
}
export const obstacles = (state,content,faction,forceClosed=false) => baseObstacles(state,contentFor(state,content,forceClosed),faction);
export function step(input, cmd, content, faction, diagnosticOmitDoor = false) {
 finiteJSON(cmd); if(!content.factions[faction])throw Error('Unknown faction');const s = createState(content, input);
 if (cmd.type !== 'internal_door' && cmd.type !== 'tick') return baseStep(s, cmd, diagnosticOmitDoor ? content : contentFor(s, content), faction);
 const m = model(content, s.chamber); let accepted = false, reason = 'invalid-state';
 if (cmd.type === 'tick') { if (!Number.isFinite(cmd.dt) || cmd.dt < 0) throw Error('Invalid dt'); m.tick(cmd.dt); accepted = true; reason = 'advanced'; }
 else {
  if (!['unlock','open','close'].includes(cmd.action) || !s.actors[cmd.actor_id]) throw Error('Invalid door action');
  const a=s.actors[cmd.actor_id], r=doorObject(content).rect, q=[(r[0]+r[2])/2,(r[1]+r[3])/2];
  if (Math.hypot(a.point[0]-q[0],a.point[1]-q[1]) > 1.35) reason = 'out-of-range';
  else { accepted=m.action(cmd.action,Object.values(s.actors));reason=accepted?'changed':m.state.events.at(-1)?.type==='close-rejected-occupied'?'occupied':'invalid-state'; }
 }
 s.chamber=JSON.parse(m.save()); s.outcomes.push({command:structuredClone(cmd),accepted,reason});return s;
}
function navigationModel(state, content, faction) {
 const static_blocks=obstacles(state,content,faction).map(o=>({id:o.id,rect:[o.bounds[0][0],o.bounds[0][1],o.bounds[1][0],o.bounds[1][1]]}));
 for(const [i,r] of [[-8,-4,-5,-1.25],[-8,1.25,-5,4],[5,-4,8,-1.25],[5,1.25,8,4]].entries())static_blocks.push({id:'outside-region-'+i,rect:r});
 return new Chamber({bounds:[-8,-4,8,4],objects:[],static_blocks});
}
const signature=(state,content,faction)=>JSON.stringify(obstacles(state,content,faction).map(o=>[o.id,o.bounds]));
export function plan(state,content,faction,id,target) { const a=state.actors[id];return{navVersion:state.chamber.state.navVersion,signature:signature(state,content,faction),actor_id:id,target:[...target],points:navigationModel(state,content,faction).path(a.point,target,a.radius)}; }
export function routeValid(route,state,content,faction) {return route.points!==null && route.navVersion===state.chamber.state.navVersion && route.signature===signature(state,content,faction);}
