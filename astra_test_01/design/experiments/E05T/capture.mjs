import{chromium}from '../E02/pixi/vendor/playwright-package/package/index.mjs';
import fs from 'node:fs';import path from 'node:path';import{fileURLToPath,pathToFileURL}from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url)),out=path.join(here,'evidence/batch-04');
const size=d=>fs.readdirSync(d,{withFileTypes:true}).reduce((n,e)=>n+(e.isDirectory()?size(path.join(d,e.name)):fs.statSync(path.join(d,e.name)).size),0);
if(fs.existsSync(out))throw Error('Refuse overwrite');if(size(here)+15000000>100000000)throw Error('Capacity');fs.mkdirSync(out);
const r={started_at:new Date().toISOString(),reserved_bytes:15000000,checks:{},errors:[]};
const b=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--use-angle=metal']});
try{
 const p=await b.newPage({viewport:{width:1200,height:900},deviceScaleFactor:1});p.on('pageerror',e=>r.errors.push(e.message));
 await p.goto('http://127.0.0.1:8770/E05T/');await p.waitForSelector('body[data-ready=true]');
 for(const bg of ['dark','light','blue']){await p.evaluate(bg=>E05T.set(.2,bg),bg);await p.locator('canvas').screenshot({path:path.join(out,bg+'.png')});}
 const a=await p.evaluate(()=>E05T.set(.1)),c=await p.evaluate(()=>E05T.set(.5));
 r.checks.time_selects_frame=a.index===6&&c.index===30;r.checks.root_from_json=Math.abs(c.state.root[0]-1)<1e-9;
 r.checks.neutral_manifest=await p.evaluate(()=>E05T.manifest.fps===60&&E05T.manifest.frames.length===48&&E05T.manifest.frames.every(f=>f.pivot.length===2&&f.atlas_coordinates.width===512));
 const video=await p.evaluate(async()=>{
  E05T.set(0);const stream=document.querySelector('canvas').captureStream(60),rec=new MediaRecorder(stream,{mimeType:'video/webm;codecs=vp9',videoBitsPerSecond:3000000}),chunks=[];
  rec.ondataavailable=e=>chunks.push(e.data);const done=new Promise(r=>rec.onstop=r);rec.start();E05T.play();
  await new Promise(r=>setTimeout(r,4000));rec.stop();await done;stream.getTracks().forEach(t=>t.stop());
  return await new Promise(r=>{const f=new FileReader();f.onload=()=>r(f.result);f.readAsDataURL(new Blob(chunks,{type:'video/webm'}));});
 });
 const bytes=Buffer.from(video.split(',')[1],'base64');if(size(here)+bytes.length>100000000)throw Error('Actual capacity');
 fs.writeFileSync(path.join(out,'normal-speed.webm'),bytes);
 await p.goto(pathToFileURL(path.join(here,'review.html')).href);await p.waitForFunction(()=>[...document.images].every(i=>i.complete));
 r.checks.review_images=await p.evaluate(()=>[...document.images].every(i=>i.naturalWidth>0));
 await p.locator('video').evaluate(v=>v.play());await p.waitForFunction(()=>document.querySelector('video').currentTime>.1);
 r.checks.review_video_decodes=true;await p.locator('video').evaluate(v=>v.pause());
 await p.screenshot({path:path.join(out,'review.jpg'),type:'jpeg',quality:70,fullPage:true});r.checks.no_browser_errors=!r.errors.length;
}catch(e){r.errors.push(e.stack);process.exitCode=1;}
finally{r.finished_at=new Date().toISOString();r.final_owned_bytes=size(here);fs.writeFileSync(path.join(out,'runtime.json'),JSON.stringify(r,null,2));await b.close();}
console.log(JSON.stringify(r));
