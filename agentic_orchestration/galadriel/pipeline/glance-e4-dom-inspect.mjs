// One-shot diagnostic — dump the actual SVG structure of the atlas plate.
import { chromium } from 'playwright';
import { writeFileSync } from 'node:fs';

const OUT = '/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-17-glance-e4-postdeploy';
const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 1680, height: 1050 } });
const page = await ctx.newPage();
page.setDefaultTimeout(90000);
await page.goto('https://reincarnated-glance.vercel.app/', { waitUntil: 'domcontentloaded' });
await page.evaluate(() => { window.location.hash = '#/atlas'; });
await page.waitForLoadState('networkidle').catch(() => {});
await page.waitForTimeout(4000);

const dump = await page.evaluate(() => {
  // Find every SVG and its structure at depth 1-2
  const svgs = [...document.querySelectorAll('svg')];
  const bigSvg = svgs.map(s => ({ el: s, r: s.getBoundingClientRect() })).filter(o => o.r.width > 500 && o.r.height > 500).sort((a, b) => b.r.width * b.r.height - a.r.width * a.r.height)[0];
  if (!bigSvg) return { note: 'no big svg found', svgCount: svgs.length };
  const s = bigSvg.el;
  // Enumerate child <g> layers
  const layers = [...s.children].map(c => ({
    tag: c.tagName.toLowerCase(),
    id: c.id || null,
    cls: c.getAttribute('class') || null,
    childCount: c.childElementCount,
    firstChildTag: c.firstElementChild?.tagName?.toLowerCase() || null,
    firstChildId: c.firstElementChild?.id || null,
    firstChildAria: c.firstElementChild?.getAttribute('aria-label') || null,
    firstChildDataAttrs: c.firstElementChild ? [...c.firstElementChild.attributes].filter(a => a.name.startsWith('data-')).map(a => a.name + '=' + a.value.slice(0, 40)) : [],
  }));
  // Sample dots: find small circles anywhere in this svg
  const dots = [...s.querySelectorAll('circle')].filter(c => {
    const r = c.getBoundingClientRect();
    return r.width > 0 && r.width < 12 && r.height > 0 && r.height < 12;
  });
  const dotSample = dots.slice(0, 12).map(d => {
    const r = d.getBoundingClientRect();
    return {
      cx: d.getAttribute('cx'), cy: d.getAttribute('cy'), r: d.getAttribute('r'),
      fill: d.getAttribute('fill') || getComputedStyle(d).fill,
      cls: d.getAttribute('class'),
      id: d.id,
      parentTag: d.parentElement?.tagName?.toLowerCase(),
      parentId: d.parentElement?.id,
      parentCls: d.parentElement?.getAttribute('class'),
      dataAttrs: [...d.attributes].filter(a => a.name.startsWith('data-')).map(a => a.name + '=' + a.value.slice(0, 40)),
      hasTitle: !!d.querySelector('title'),
      titleText: d.querySelector('title')?.textContent?.slice(0, 200),
      screenX: Math.round(r.left + r.width / 2), screenY: Math.round(r.top + r.height / 2),
    };
  });
  return { svgCount: svgs.length, bigSvgR: bigSvg.r, layers, totalDots: dots.length, dotSample };
});

writeFileSync(`${OUT}/dom-inspect.json`, JSON.stringify(dump, null, 2));

// Now do one hover test on the first dot found and record the popover state
if (dump.dotSample && dump.dotSample.length > 0) {
  const first = dump.dotSample[0];
  await page.mouse.move(0, 0);
  await page.waitForTimeout(300);
  await page.mouse.move(first.screenX, first.screenY);
  await page.waitForTimeout(1800);
  const state = await page.evaluate(() => {
    const cards = [...document.querySelectorAll('*')]
      .filter(el => {
        const cs = getComputedStyle(el);
        const b = el.getBoundingClientRect();
        return (cs.position === 'fixed' || cs.position === 'absolute')
          && cs.visibility !== 'hidden' && cs.opacity !== '0' && cs.display !== 'none'
          && b.width >= 40 && b.width <= 800 && b.height >= 14 && b.height <= 700
          && (el.textContent || '').trim().length > 2;
      })
      .map(el => { const b = el.getBoundingClientRect(); return { text: (el.textContent || '').trim().slice(0, 300), x: Math.round(b.left), y: Math.round(b.top), w: Math.round(b.width), h: Math.round(b.height) }; });
    return cards.slice(0, 20);
  });
  writeFileSync(`${OUT}/dom-hover-state.json`, JSON.stringify({ dot: first, cards: state }, null, 2));
  const clip = { x: Math.max(0, first.screenX - 400), y: Math.max(0, first.screenY - 250), width: Math.min(1680 - Math.max(0, first.screenX - 400), 800), height: Math.min(1050 - Math.max(0, first.screenY - 250), 600) };
  await page.screenshot({ path: `${OUT}/dom-hover-shot.png`, clip, timeout: 60000 });
}

await browser.close();
console.log('DOM inspect complete.');
console.log('layers:', dump.layers?.map(l => `${l.id || l.tag}(${l.childCount})`).join(' '));
console.log('total small circles:', dump.totalDots);
console.log('first dot sample:', JSON.stringify(dump.dotSample?.[0]));
