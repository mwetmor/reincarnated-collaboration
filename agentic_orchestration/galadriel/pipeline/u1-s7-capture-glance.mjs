import { chromium } from 'playwright';
import fs from 'fs';
const OUT='/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-08-24-u1-s7';
const b=await chromium.launch();
const errs=[];
for (const [w,h,tag] of [[1500,1000,'1500'],[430,932,'430']]) {
  const p=await b.newPage({viewport:{width:w,height:h}, deviceScaleFactor:2});
  p.on('console', m=>{ if(m.type()==='error') errs.push(tag+': '+m.text().slice(0,200)); });
  p.on('pageerror', e=>errs.push(tag+' PAGEERROR: '+String(e).slice(0,200)));
  await p.goto('http://localhost:5199/#/fleet',{waitUntil:'networkidle'});
  await p.waitForTimeout(1500);
  await p.screenshot({path:`${OUT}/glance-fleet-${tag}-full.png`, fullPage:true});
  const of = await p.evaluate(()=>{
    const bad=[];
    for (const el of document.querySelectorAll('*')) {
      if (el.scrollWidth > el.clientWidth+2 && el.clientWidth>0) bad.push({tag:el.tagName, cls:String(el.className).slice(0,40), sw:el.scrollWidth, cw:el.clientWidth});
    }
    return {docW:document.documentElement.scrollWidth, winW:window.innerWidth, n:bad.length, sample:bad.slice(0,8)};
  });
  console.log('OVERFLOW',tag, JSON.stringify(of));
  if(tag==='1500'){
    const txt=await p.evaluate(()=>document.body.innerText);
    fs.writeFileSync(`${OUT}/glance-fleet-text.txt`, txt);
  }
  await p.close();
}
console.log('CONSOLE ERRORS:', errs.length); errs.forEach(e=>console.log('  ',e));
await b.close();
