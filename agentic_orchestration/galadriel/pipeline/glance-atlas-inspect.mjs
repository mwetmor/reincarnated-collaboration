// Inspect UNMAPPED band DOM + mobile plane layout + hover mechanism.
import { chromium } from 'playwright';
import { readFileSync } from 'node:fs';
const URL = 'https://reincarnated-glance-i26spw3cp-matthew-wetmore-s-projects.vercel.app/#/atlas';
const dotJson = JSON.parse(readFileSync('/tmp/pdp.json', 'utf8')); const VB = dotJson.viewBox; const dots = dotJson.dots;

const browser = await chromium.launch();

// DESKTOP: find what element carries the unmapped-list hover handler.
{
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 1000 } });
  const page = await ctx.newPage();
  const base = URL.split('#')[0];
  await page.goto(base, { waitUntil: 'domcontentloaded' });
  await page.evaluate(() => { window.location.hash = '#/atlas'; });
  await page.waitForLoadState('networkidle').catch(()=>{});
  await page.waitForTimeout(3000);

  const info = await page.evaluate(() => {
    // Locate the UNMAPPED band text nodes and describe their ancestor structure + whether ancestors have pointer cursor / title tokens
    const hits = [...document.querySelectorAll('*')].filter(el => /movement=unknown|pure-mobility residual|roster \(movement column/i.test(el.textContent||'') && el.children.length <= 6);
    return hits.slice(0,6).map(el => {
      const chain = [];
      let n = el;
      for (let i=0;i<4 && n;i++){ const cs=getComputedStyle(n); const b=n.getBoundingClientRect();
        chain.push({ tag:n.tagName.toLowerCase(), cls:(n.getAttribute('class')||'').slice(0,80), cursor:cs.cursor, w:Math.round(b.width), h:Math.round(b.height), x:Math.round(b.left), y:Math.round(b.top) });
        n = n.parentElement; }
      return { text:(el.textContent||'').slice(0,60), chain };
    });
  });
  console.log('===== UNMAPPED band DOM chains =====');
  console.log(JSON.stringify(info, null, 2));

  // Try hovering the innermost token that has a pointer cursor (or its parent), directly via element handle.
  const res = await page.evaluate(async () => {
    // find a candidate token: a small element in the unmapped band whose text looks like a kit id (poe2-..., B10 etc)
    const cands = [...document.querySelectorAll('span,a,li,div,em,strong')].filter(el => {
      const t=(el.textContent||'').trim();
      return el.children.length===0 && /^(poe2-|B1[0-9]|K[0-9]|H[0-9]|pure-mobility|movement=unknown)/i.test(t) && t.length<60;
    });
    return cands.slice(0,10).map(el=>{ const b=el.getBoundingClientRect(); return {t:el.textContent.trim().slice(0,40), x:Math.round(b.left+b.width/2), y:Math.round(b.top+b.height/2), cursor:getComputedStyle(el).cursor}; });
  });
  console.log('\ncandidate hover tokens in band:');
  console.log(JSON.stringify(res, null, 2));

  // Hover the first token that has pointer cursor; else first token.
  const tok = res.find(t=>t.cursor==='pointer') || res[0];
  if (tok) {
    tok && console.log('\nhovering token:', tok.t, 'cursor', tok.cursor, 'at', tok.x, tok.y);
    // scroll into view first
    await page.evaluate(({y})=>window.scrollBy(0, y-500), tok);
    await page.waitForTimeout(300);
    // re-find same token position after scroll
    const tok2 = await page.evaluate((txt)=>{ const el=[...document.querySelectorAll('span,a,li,div,em,strong')].find(e=>e.children.length===0 && e.textContent.trim().startsWith(txt.slice(0,12))); if(!el)return null; const b=el.getBoundingClientRect(); return {x:Math.round(b.left+b.width/2),y:Math.round(b.top+b.height/2)}; }, tok.t);
    if (tok2) {
      await page.mouse.move(tok2.x, tok2.y); await page.waitForTimeout(700);
      const pop = await page.evaluate(()=>{
        const cards=[...document.querySelectorAll('*')].filter(el=>{const cs=getComputedStyle(el);const b=el.getBoundingClientRect();return (cs.position==='fixed'||cs.position==='absolute')&&b.width>80&&b.width<640&&b.height>20&&b.height<600&&(el.textContent||'').trim().length>8&&cs.visibility!=='hidden'&&cs.opacity!=='0'&&b.top>=-5;}).map(el=>{const b=el.getBoundingClientRect();return{text:(el.textContent||'').replace(/\s+/g,' ').trim().slice(0,260),h:Math.round(b.height),w:Math.round(b.width),y:Math.round(b.top),rows:el.querySelectorAll('li,div').length};});
        cards.sort((a,b)=>b.h-a.h); return cards.slice(0,4);
      });
      console.log('\npopover(s) after token hover (tallest first):');
      console.log(JSON.stringify(pop, null, 2));
      await page.screenshot({ path: '/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-13-glance-atlas-perdot-v3/desktop-unmapped-hover.png' });
    }
  }
  await ctx.close();
}
await browser.close();
console.log('DONE inspect');
