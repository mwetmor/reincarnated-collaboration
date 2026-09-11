import {chromium} from '../E02/pixi/vendor/playwright-package/package/index.mjs';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const batch=process.argv[2]??'batch-01',out=path.join(here,'evidence',batch);
if(fs.existsSync(out))throw new Error('Refusing to overwrite a capture batch');
fs.mkdirSync(out,{recursive:true});
const record={started_at:new Date().toISOString(),cases:[],ui:{},errors:[]};
const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--use-angle=metal']});
try{
 const page=await browser.newPage({viewport:{width:1100,height:800},deviceScaleFactor:1});
 page.on('pageerror',e=>record.errors.push(e.message));
 await page.goto('http://127.0.0.1:8769/E02P/');
 await page.waitForSelector('body[data-ready=true]',{timeout:20000});
 const samples=await page.evaluate(()=>window.E02P.samples);
 for(const tracking of[false,true])for(let sample=0;sample<samples.length;sample++){
  const result=await page.evaluate(v=>window.E02P.set(v),{sample,tracking,bad:false,point:null});
  const controls=await page.evaluate(()=>window.E02P.negativeControls());
  await page.waitForTimeout(80);
  const name=(tracking?'tracking':'fixed')+'-'+samples[sample].id+'.png';
  const png=await page.evaluate(()=>document.querySelector('canvas').toDataURL('image/png'));
  fs.writeFileSync(path.join(out,name),Buffer.from(png.split(',')[1],'base64'));
  const bad=await page.evaluate(()=>window.E02P.set({bad:true}));
  record.cases.push({...result,controls,bad_scale:bad.source_scale,capture:name});
 }
 await page.evaluate(()=>window.E02P.set({sample:0,tracking:false,bad:false,point:null}));
 await page.selectOption('#position','4');
 record.ui.position=await page.evaluate(()=>window.E02P.results());
 await page.click('#tracking');record.ui.following=await page.evaluate(()=>window.E02P.results());
 await page.click('#bad');record.ui.bad=await page.evaluate(()=>window.E02P.results());
 await page.click('#bad');await page.click('#tracking');
 await page.click('#motion');await page.waitForTimeout(250);
 record.ui.motion_start=await page.evaluate(()=>window.E02P.results());
 await page.waitForTimeout(500);record.ui.motion_end=await page.evaluate(()=>window.E02P.results());
 await page.click('#motion');record.ui.pause_start=await page.evaluate(()=>window.E02P.results());
 await page.waitForTimeout(150);record.ui.pause_end=await page.evaluate(()=>window.E02P.results());
 await page.evaluate(()=>window.E02P.set({sample:0,tracking:false,bad:false,point:null}));
 await page.screenshot({path:path.join(out,'browser.png')});
 record.browser=browser.version();
}catch(e){record.errors.push(e.stack);process.exitCode=1;}finally{
 record.finished_at=new Date().toISOString();fs.writeFileSync(path.join(out,'runtime.json'),JSON.stringify(record,null,2)+'\n');await browser.close();
}
console.log(JSON.stringify({batch,cases:record.cases.length,errors:record.errors}));
