import { chromium } from 'playwright';
const OUT='/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-08-24-u1-s7';
const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1500,height:1000}, deviceScaleFactor:2});
await p.goto('http://localhost:5199/#/fleet',{waitUntil:'networkidle'});
await p.waitForTimeout(1200);
// find headings and screenshot their nearest card ancestor
const n = await p.evaluate(()=>{
  const out=[];
  document.querySelectorAll('h1,h2,h3').forEach((h,i)=>{ h.setAttribute('data-gsec', String(i)); out.push(h.textContent.trim().slice(0,60)); });
  return out;
});
console.log(n.map((t,i)=>i+': '+t).join('\n'));
for (let i=0;i<n.length;i++){
  const h=await p.$(`[data-gsec="${i}"]`);
  if(!h) continue;
  const card=await h.evaluateHandle(el=>el.closest('section,article,div.card')||el.parentElement);
  const box=await card.asElement().boundingBox();
  if(!box||box.height<20||box.height>4000) continue;
  await card.asElement().screenshot({path:`${OUT}/glance-sec-${String(i).padStart(2,'0')}.png`});
  console.log('shot',i, Math.round(box.width)+'x'+Math.round(box.height));
}
await b.close();
