import { chromium } from 'playwright';
const OUT='/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-08-24-u1-s7';
const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1500,height:1000}, deviceScaleFactor:2});
await p.goto('http://127.0.0.1:8787/',{waitUntil:'networkidle'});
const secs=await p.$$('section, header, .topstrip');
let i=0;
for (const s of secs){
  const t=(await s.innerText()).slice(0,50).replace(/\s+/g,' ');
  const box=await s.boundingBox();
  if(!box||box.height<10) continue;
  i++;
  await s.screenshot({path:`${OUT}/board-sec-${String(i).padStart(2,'0')}.png`});
  console.log(i, Math.round(box.width)+'x'+Math.round(box.height), '|', t);
}
await b.close();
