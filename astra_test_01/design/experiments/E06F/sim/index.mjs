import{createViewState,consume}from'../../E06D/instances.mjs';
export function createState(content){return{time:0,caster_root:[...content.actor.root],views:createViewState(),release:false,contact:false,hit_response_ids:[]};}
export function advance(input,dt,content,catalog){if(!Number.isFinite(dt)||dt<0||dt>10)throw Error('Invalid dt');const s=structuredClone(input),end=s.time+dt;
if(!s.release&&end>=content.release_s){const origin=content.release_socket.map((x,i)=>x+s.caster_root[i]);s.views=consume(catalog,s.views,{id:'release-1',type:'spawn',at:content.release_s,instance_id:'projectile-1',binding:content.binding,presentation:{lifecycle:'burst',anchor_mode:'frozen',origin,duration_s:content.end_s-content.release_s,fade_s:0}});s.release=true;}
if(!s.contact&&end>=content.contact_s){s.views=consume(catalog,s.views,{id:'contact-1',type:'contact',at:content.contact_s,instance_id:'projectile-1',target_id:content.target.id,point:content.target.contact});s.contact=true;s.hit_response_ids.push('contact-1');}
s.time=end;return s;}
