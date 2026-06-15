import sharp from 'sharp';
import { join } from 'path';
const TARGET_W = 960;
const DIR = '/Users/admin/Games/reincarnated-godot/harness_logs/iter2fix_fullcap';
const VIEWS = ['zone0_threshold','zone1_arcane','zone2_warhall','zone3_oubliette','zone4_antechamber','zone5_sanctum','establish_primary'];
function rgb2hsv(r,g,b){r/=255;g/=255;b/=255;const max=Math.max(r,g,b),min=Math.min(r,g,b),d=max-min;let h=0;if(d!==0){if(max===r)h=((g-b)/d)%6;else if(max===g)h=(b-r)/d+2;else h=(r-g)/d+4;h*=60;if(h<0)h+=360;}const s=max===0?0:d/max;return[h,s,max];}
async function hb(path){const{data:rgb,info}=await sharp(path).resize(TARGET_W,null,{fit:'inside'}).removeAlpha().raw().toBuffer({resolveWithObject:true});let warm=0,green=0,tot=0;for(let i=0;i<rgb.length;i+=3){const[hue,s,v]=rgb2hsv(rgb[i],rgb[i+1],rgb[i+2]);const m=s*v;tot+=m;if(hue<70||hue>=330)warm+=m;if(hue>=70&&hue<170)green+=m;}return{w:100*warm/tot,g:100*green/tot,r:warm/Math.max(1e-9,green)};}
console.log('view              warmMass%  greenMass%  warm:green');
let sw=0,sg=0,sr=0,c=0;
for(const v of VIEWS){const f=join(DIR,'gal_descent_'+v+'_04.png');const x=await hb(f);console.log(v.padEnd(18)+x.w.toFixed(2).padEnd(11)+x.g.toFixed(2).padEnd(12)+x.r.toFixed(3));sw+=x.w;sg+=x.g;sr+=x.r;c++;}
console.log('-'.repeat(50));
console.log('SCENE MEAN'.padEnd(18)+(sw/c).toFixed(2).padEnd(11)+(sg/c).toFixed(2).padEnd(12)+(sr/c).toFixed(3));
