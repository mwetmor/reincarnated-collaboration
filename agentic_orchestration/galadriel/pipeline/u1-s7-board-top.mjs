import { chromium } from 'playwright';
const OUT='/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-08-24-u1-s7';
const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1500,height:1050}, deviceScaleFactor:2});
await p.goto('http://127.0.0.1:8787/',{waitUntil:'networkidle'});
for (const [y,tag] of [[0,'top'],[900,'mid1'],[1800,'mid2']]) {
  await p.evaluate(yy=>window.scrollTo(0,yy), y);
  await p.waitForTimeout(200);
  await p.screenshot({path:`${OUT}/board-view-${tag}.png`});
}
await b.close();
