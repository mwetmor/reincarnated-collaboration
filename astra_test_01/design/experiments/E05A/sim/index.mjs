export function createState(){return{outfit:'advanced-fitted-v2',head_visible:true};}
export function step(state,event){if(typeof event.visible!=='boolean'||event.type!=='head_visibility')throw Error('Unsupported state event');return{...JSON.parse(JSON.stringify(state)),head_visible:event.visible};}
