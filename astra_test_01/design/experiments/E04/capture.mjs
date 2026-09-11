import {chromium} from '../E02/pixi/vendor/playwright-package/package/index.mjs';import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url)),batch=process.argv[2]??'batch-01',out=path.join(here,'evidence',batch);if(fs.existsSync(out))throw Error('Refusing overwrite');fs.mkdirSync(out,{recursive:true});
const r={started_at:new Date().toISOString(),checks:{},snapshots:[],errors:[],warnings:[]};const check=(k,v)=>r.checks[k]=Boolean(v);
const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--use-angle=metal']});
try{
 const context=await browser.newContext({viewport:{width:1360,height:900},deviceScaleFactor:1,recordVideo:{dir:path.join(out,'video'),size:{width:1360,height:900}}});const page=await context.newPage();page.on('pageerror',e=>r.errors.push(e.message));page.on('console',m=>{if(m.type()==='warning')r.warnings.push(m.text());});await page.goto('http://127.0.0.1:8770/E04/');await page.waitForSelector('body[data-ready=true]',{timeout:30000});await page.evaluate(()=>window.E04.pause(true));
 const snap=async id=>{const s=await page.evaluate(()=>window.E04.snapshot());r.snapshots.push({id,...s});const png=await page.evaluate(()=>document.querySelector('canvas').toDataURL('image/png'));fs.writeFileSync(path.join(out,id+'.png'),Buffer.from(png.split(',')[1],'base64'));check(id+':render-state-synchronized',JSON.stringify(s.state)===JSON.stringify(s.rendered_state));return s;};
 await snap('locked');await page.click('[data-action=open]');check('locked-open-rejected',(await page.evaluate(()=>window.E04.snapshot())).state.door==='locked');
 check('locked-route-rejected',!(await page.evaluate(()=>window.E04.moveTo([3.3,0]))));
 await page.click('[data-action=unlock]');check('unlock-only-closes',(await page.evaluate(()=>window.E04.snapshot())).state.door==='closed');await page.click('[data-action=open]');await page.evaluate(()=>window.E04.advance(.25));await snap('opening');await page.evaluate(()=>window.E04.advance(.25));check('open-event',(await snap('open')).state.door==='open');
 for(const id of['mage','monster']){
  await page.selectOption('#actor',id);await page.evaluate(id=>window.E04.setPoint(id,[0,0]),id);
  // Actual canvas click -> inverse projection -> path -> independent swept movement.
  const pt=await page.evaluate(()=>window.E04.project([3.3,0]));await page.locator('canvas').click({position:{x:pt[0],y:pt[1]}});
  for(let i=0;i<150;i++)await page.evaluate(()=>window.E04.advance(1/60));
  const s=await snap(id+'-traversed');check(id+':actual-traversal',Math.hypot(s.actors[id].point[0]-3.3,s.actors[id].point[1])<.03);
  await page.evaluate(id=>window.E04.setPoint(id,[2.15,0]),id);await page.click('[data-action=close]');check(id+':occupied-close-rejected',(await page.evaluate(()=>window.E04.snapshot())).state.door==='open');await page.evaluate(id=>window.E04.setPoint(id,[3.3,id==='mage'?-2:2]),id);
 }
 await page.click('[data-action=close]');await page.evaluate(()=>window.E04.advance(.5));check('close-event',(await snap('closed-again')).state.door==='closed');
 await page.click('[data-action=break]');check('crate-broken',(await snap('crate-broken')).state.crate==='broken');
 await page.click('[data-action=chest]');await page.click('[data-action=chest]');const chest=await snap('chest-open');check('reward-once',chest.state.rewards.length===1&&chest.state.events.filter(e=>e.type==='reward').length===1);
 await page.click('[data-action=pickup]');await page.click('[data-action=pickup]');const picked=await snap('loot-picked');check('pickup-once',picked.state.picked.length===1&&picked.state.events.filter(e=>e.type==='pickup').length===1);
 await page.click('#reload');const reloaded=await snap('reentered');check('reload-persists',JSON.stringify(picked.state)===JSON.stringify(reloaded.state));await page.click('[data-action=chest]');check('reload-no-duplicate',(await page.evaluate(()=>window.E04.snapshot())).state.rewards.length===1);
 const pts=[[-4,-3],[0,0],[4,3],[-3,2],[2,-2]];r.roundtrips=await page.evaluate(pts=>pts.map(p=>({point:p,result:window.E04.inverse(window.E04.project(p))})),pts);check('projection-roundtrip',r.roundtrips.every(x=>Math.hypot(x.point[0]-x.result[0],x.point[1]-x.result[1])<1e-8));
 await page.click('#debug');await snap('debug');await page.click('#debug');

 await page.evaluate(()=>{window.E04.reset();window.E04.select('mage');});await snap('effect-baseline');
 await page.evaluate(()=>window.E04.effect('mage',{kind:'flash',color:'#f0c060',ms:150}));await snap('effect-flash');
 await page.evaluate(()=>window.E04.advance(.149));check('flash-before-deadline',Boolean((await page.evaluate(()=>window.E04.snapshot())).actors.mage.effects.flash));await page.evaluate(()=>window.E04.advance(.001));check('flash-expired-at-deadline',!(await snap('effect-expired')).actors.mage.effects.flash);
 await page.evaluate(()=>window.E04.effect('mage',{kind:'tint',color:'#3090ff',ms:0}));await snap('effect-tint');
 await page.evaluate(()=>{window.E04.reset();window.E04.effect('mage',{kind:'flash',color:'#ffffff',ms:100});window.E04.pause(false);});await page.waitForTimeout(250);check('idle-effect-clock-expires',!(await page.evaluate(()=>window.E04.snapshot())).actors.mage.effects.flash);await page.evaluate(()=>window.E04.pause(true));
 const unsupported=await page.evaluate(()=>{try{window.E04.effect('mage',{kind:'glow',color:'#ffffff',ms:100});return false;}catch(e){return e.message==='Unqualified effect kind glow';}finally{window.E04.reset();}});check('unsupported-glow-reported',unsupported);
 for(const [id,p]of Object.entries({'behind-pillar':[-3,-2.5],'front-pillar':[-1,-.5]})){await page.evaluate(p=>window.E04.setPoint('mage',p),p);await snap(id);}
 await page.click('#demo');await page.evaluate(()=>window.E04.pause(false));await page.waitForTimeout(12500);const demo=await snap('demo-end');check('live-demo-single-reward',demo.state.rewards.length===1&&demo.state.picked.length===1);r.live_profile=demo;r.browser=browser.version();check('no-browser-errors',!r.errors.length);
 await context.close();
}catch(e){r.errors.push(e.stack);process.exitCode=1;}finally{r.finished_at=new Date().toISOString();r.passed=Object.values(r.checks).filter(Boolean).length;r.total=Object.keys(r.checks).length;fs.writeFileSync(path.join(out,'runtime.json'),JSON.stringify(r,null,2)+'\n');await browser.close();}
console.log(JSON.stringify({batch,passed:r.passed,total:r.total,errors:r.errors,failed:Object.entries(r.checks).filter(x=>!x[1]).map(x=>x[0])}));if(r.passed!==r.total)process.exitCode=1;
