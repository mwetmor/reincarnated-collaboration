// Pure fixture state and authoritative event timing. No renderer/pose imports.
export function createState(){return{action:'idle',time:0,root:[0,0],events:[],cast_id:0,released:false};}
export function step(input,command,content){
 const s=structuredClone(input);s.events=[];
 if(command.type==='action'){
  if(!Object.hasOwn(content.motion,command.action))throw Error('Unknown action');
  s.action=command.action;s.time=0;s.released=false;if(s.action==='cast')s.cast_id++;
 }else if(command.type==='advance'){
  const dt=command.dt;if(!Number.isFinite(dt)||dt<0||dt>10)throw Error('Bad dt');const before=s.time;s.time+=dt;
  if(s.action==='walk')s.root[0]+=dt*content.motion.walk.speed_mps;
  if(s.action==='cast'){
   const clip=content.motion.cast;
   if(!s.released&&before<clip.release_s&&s.time>=clip.release_s){s.events.push({type:'cast_release',id:'cast-'+s.cast_id,at:clip.release_s,socket:'right_hand',root:[...s.root]});s.released=true;}
   if(s.time>=clip.duration_s){s.events.push({type:'action_complete',id:'cast-'+s.cast_id,at:clip.duration_s});s.time-=clip.duration_s;s.action='idle';s.released=false;}
  }
 }else throw Error('Unknown command');
 return s;
}
