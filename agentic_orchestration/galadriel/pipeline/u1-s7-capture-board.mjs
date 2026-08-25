import { chromium } from 'playwright';
const OUT='/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-08-24-u1-s7';
const b=await chromium.launch();
for (const [w,h,tag] of [[1600,1200,'1600'],[1280,1000,'1280'],[430,932,'430']]) {
  const p=await b.newPage({viewport:{width:w,height:h}, deviceScaleFactor:2});
  await p.goto('http://127.0.0.1:8787/',{waitUntil:'networkidle'});
  await p.screenshot({path:`${OUT}/board-live-${tag}-full.png`, fullPage:true});
  // overflow probe
  const of = await p.evaluate(()=>{
    const bad=[];
    for (const el of document.querySelectorAll('*')) {
      if (el.scrollWidth > el.clientWidth+2 && el.clientWidth>0) bad.push({tag:el.tagName, cls:el.className, sw:el.scrollWidth, cw:el.clientWidth, txt:(el.textContent||'').slice(0,60)});
    }
    return {docW:document.documentElement.scrollWidth, winW:window.innerWidth, overflowers:bad.slice(0,15), n:bad.length};
  });
  console.log(tag, JSON.stringify(of));
  await p.close();
}
// text dump for value comparison
const p=await b.newPage({viewport:{width:1600,height:1200}});
await p.goto('http://127.0.0.1:8787/',{waitUntil:'networkidle'});
const txt=await p.evaluate(()=>document.body.innerText);
await import('fs').then(fs=>fs.writeFileSync(`${OUT}/board-live-text.txt`, txt));
await b.close();
