// Galadriel perception check — Glance /atlas page (hash route) plane-image visibility
// One-off probe for drax Phase-1 SVG embed. Read-only; no file modification of target.
import { chromium } from 'playwright';
import { mkdirSync } from 'node:fs';

const URL = 'https://reincarnated-glance-2f3afx1xf-matthew-wetmore-s-projects.vercel.app/#/atlas';
const OUT = '/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-13-glance-atlas-abovefold';
mkdirSync(OUT, { recursive: true });

const viewports = [
  { name: 'desktop', width: 1280, height: 900 },
  { name: 'mobile', width: 375, height: 812 },
];

const browser = await chromium.launch();
for (const vp of viewports) {
  const ctx = await browser.newContext({
    viewport: { width: vp.width, height: vp.height },
    deviceScaleFactor: vp.name === 'mobile' ? 2 : 1,
  });
  const page = await ctx.newPage();
  const consoleErrors = [];
  page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text()); });
  page.on('requestfailed', r => consoleErrors.push('REQFAIL ' + r.url() + ' ' + (r.failure()?.errorText || '')));

  // Load base then set hash, to be robust to SPA hash-route hydration order.
  const base = URL.split('#')[0];
  await page.goto(base, { waitUntil: 'domcontentloaded' });
  await page.evaluate(() => { window.location.hash = '#/atlas'; });
  await page.waitForLoadState('networkidle').catch(() => {});
  await page.waitForTimeout(2500); // let SPA + fetch(state.json) resolve

  const fullH = await page.evaluate(() => document.body.scrollHeight);

  // Above-the-fold shot
  await page.screenshot({ path: `${OUT}/${vp.name}-fold.png` });
  // Full-page shot
  await page.screenshot({ path: `${OUT}/${vp.name}-full.png`, fullPage: true });

  // Probe DOM for the plane image / provenance / structural markers
  const probe = await page.evaluate(() => {
    const txt = document.body.innerText || '';
    const imgs = [...document.querySelectorAll('img,svg')].map(el => ({
      tag: el.tagName.toLowerCase(),
      src: el.getAttribute?.('src') || null,
      alt: el.getAttribute?.('alt') || null,
      w: el.getBoundingClientRect().width,
      h: el.getBoundingClientRect().height,
      top: Math.round(el.getBoundingClientRect().top + window.scrollY),
      role: el.getAttribute?.('role') || null,
    })).filter(i => i.w > 40 && i.h > 40);
    // Largest svg/img = the plane grid; find its doc-top and title/triplelaw tops
    const rectTop = (el) => Math.round(el.getBoundingClientRect().top + window.scrollY);
    const findTextTop = (needle) => {
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
      let best = null;
      while (walker.nextNode()) {
        const el = walker.currentNode;
        if (el.children.length === 0 && new RegExp(needle, 'i').test(el.textContent || '')) {
          const t = rectTop(el);
          if (best === null || t < best) best = t;
        }
      }
      return best;
    };
    const planeEls = [...document.querySelectorAll('img,svg')]
      .map(el => ({ el, r: el.getBoundingClientRect() }))
      .filter(o => o.r.width > 100 && o.r.height > 100)
      .sort((a, b) => (b.r.width * b.r.height) - (a.r.width * a.r.height));
    const plane = planeEls[0]?.el;
    const planeTop = plane ? rectTop(plane) : null;
    const planeBottom = plane ? planeTop + Math.round(plane.getBoundingClientRect().height) : null;
    const foldH = window.innerHeight;
    return {
      title: document.title,
      hash: window.location.hash,
      hasRuled: /RULED/i.test(txt),
      hasStratified: /Stratified Plane View/i.test(txt),
      hasQ19: /Q19 LOCKED/i.test(txt),
      hasQ19Date: /Q19 LOCKED 2026-07-13/i.test(txt),
      hasTripleLaw: /TRIPLE LAW/i.test(txt),
      foldH,
      planeTag: plane?.tagName?.toLowerCase() || null,
      planeTop, planeBottom,
      planeVisibleWithinFold: planeTop !== null ? Math.max(0, Math.min(planeBottom, foldH) - Math.max(planeTop, 0)) : null,
      planePctShownInFold: (planeTop !== null && planeBottom > planeTop) ? Math.round(100 * Math.max(0, Math.min(planeBottom, foldH) - Math.max(planeTop, 0)) / (planeBottom - planeTop)) : null,
      titleTop: findTextTop('Stratified Plane View|RULED'),
      tripleLawTop: findTextTop('TRIPLE LAW'),
      q19Top: findTextTop('Q19 LOCKED'),
      bodyTextLen: txt.length,
      textSnippet: txt.slice(0, 400),
      imgs,
    };
  });
  console.log(`\n===== ${vp.name} (${vp.width}px) =====`);
  console.log('scrollHeight:', fullH);
  console.log(JSON.stringify(probe, null, 2));
  if (consoleErrors.length) console.log('CONSOLE/NET ERRORS:', JSON.stringify(consoleErrors, null, 2));
  await ctx.close();
}
await browser.close();
console.log('\nDONE. Captures in', OUT);
