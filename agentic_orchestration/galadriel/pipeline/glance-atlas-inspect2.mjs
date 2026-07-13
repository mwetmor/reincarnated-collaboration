import { chromium } from 'playwright';
const URL = 'https://reincarnated-glance-i26spw3cp-matthew-wetmore-s-projects.vercel.app/#/atlas';
const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1280, height: 1000 } });
const page = await ctx.newPage();
const base = URL.split('#')[0];
await page.goto(base, { waitUntil: 'domcontentloaded' });
await page.evaluate(() => { window.location.hash = '#/atlas'; });
await page.waitForLoadState('networkidle').catch(()=>{});
await page.waitForTimeout(3000);

// Dump all elements whose text contains UNMAPPED or movement=unknown, with tag + full class + parent, no children<= filter.
const dump = await page.evaluate(() => {
  const out = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
  while (walker.nextNode()) {
    const el = walker.currentNode;
    const own = [...el.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent).join('');
    if (/UNMAPPED|movement=unknown|pure-mobility|roster \(movement/i.test(own)) {
      const b = el.getBoundingClientRect();
      out.push({ tag: el.tagName.toLowerCase(), ns: el.namespaceURI?.includes('svg')?'svg':'html', cls: (el.getAttribute('class')||'').slice(0,90), cursor: getComputedStyle(el).cursor, x:Math.round(b.left),y:Math.round(b.top),w:Math.round(b.width),h:Math.round(b.height), own: own.slice(0,70) });
    }
  }
  return out;
});
console.log('=== elements owning UNMAPPED-band text ===');
console.log(JSON.stringify(dump, null, 2));

// Also: is the band inside the svg (svg <text>) or html below it? And find any element with a hover/list handler = look for elements with cursor pointer near y of band.
const nearBand = await page.evaluate(() => {
  const anchor = [...document.querySelectorAll('*')].find(el => [...el.childNodes].some(n=>n.nodeType===3 && /movement=unknown/i.test(n.textContent)));
  if (!anchor) return null;
  const by = anchor.getBoundingClientRect().top;
  const pointers = [...document.querySelectorAll('*')].filter(el=>{const b=el.getBoundingClientRect();return getComputedStyle(el).cursor==='pointer' && Math.abs(b.top-by)<160 && b.width>20;}).map(el=>{const b=el.getBoundingClientRect();return{tag:el.tagName.toLowerCase(),cls:(el.getAttribute('class')||'').slice(0,70),x:Math.round(b.left),y:Math.round(b.top),w:Math.round(b.width),h:Math.round(b.height),t:(el.textContent||'').replace(/\s+/g,' ').trim().slice(0,50)};});
  return { bandTop: Math.round(by), pointerEls: pointers.slice(0,12) };
});
console.log('\n=== pointer-cursor elements near band ===');
console.log(JSON.stringify(nearBand, null, 2));
await ctx.close();
await browser.close();
console.log('DONE');
