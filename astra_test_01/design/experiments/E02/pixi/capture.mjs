// Fresh local browser for the isolated test. Never reads an existing user profile.
import {chromium} from './vendor/playwright-package/package/index.mjs';
import {writeFile} from 'node:fs/promises';
const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--use-angle=metal']});
const page=await browser.newPage({viewport:{width:1460,height:1120},deviceScaleFactor:1});
const errors=[];page.on('pageerror',e=>errors.push(String(e)));
await page.goto('http://127.0.0.1:8768/pixi/',{waitUntil:'networkidle'});
await page.waitForSelector('body[data-ready="true"]');
const records=[];
for(const tracking of [false,true])for(let sample=0;sample<9;sample++){
  const record=await page.evaluate(v=>window.E02.set(v),{sample,tracking,bad:false,point:null});records.push(record);
  const data=await page.evaluate(()=>window.E02.frame());
  await writeFile(new URL(`../evidence/pixi-v2-${tracking?'tracking':'fixed'}-${record.sample}.png`,import.meta.url),Buffer.from(data.split(',')[1],'base64'));
}
await page.evaluate(()=>window.E02.set({sample:0,tracking:false,bad:false,point:null}));
const controls=await page.evaluate(()=>window.E02.negativeControls());
await page.locator('#tracking').click();
const toggled=await page.evaluate(()=>window.E02.results());
await page.locator('#position').selectOption('4');
const selected=await page.evaluate(()=>window.E02.results());
controls.tracking_button=toggled.tracking===true;controls.position_select=selected.sample==='right';
await page.locator('#bad').click();
const bad=await page.evaluate(()=>window.E02.results());
controls.bad_scale_button=bad.source_scale>records.find(r=>r.tracking&&r.sample==='right').source_scale*1.24;
await page.locator('#motion').click();await page.waitForTimeout(150);
await page.locator('#motion').click();
controls.motion_button=(await page.locator('#motion').textContent())==='Play translation probe';
const data=await page.evaluate(()=>window.E02.frame());
await writeFile(new URL('../evidence/pixi-v2-bad-control.png',import.meta.url),Buffer.from(data.split(',')[1],'base64'));
await writeFile(new URL('../evidence/runtime-pixi-v2.json',import.meta.url),JSON.stringify({browser:browser.version(),errors,controls,records},null,2)+'\n');
await browser.close();
if(errors.length||Object.values(controls).some(v=>!v))throw Error('Browser controls failed; inspect runtime-pixi.json');
console.log(JSON.stringify({samples:records.length,controls,errors}));
