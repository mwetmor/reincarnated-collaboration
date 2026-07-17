// FINAL-2 — with correct data-el selectors + sample the data-kit values, hover each.
import { chromium } from 'playwright';
import { mkdirSync, writeFileSync } from 'node:fs';

const OUT = '/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-17-glance-e4-postdeploy';
mkdirSync(OUT, { recursive: true });

const record = { captured_at: new Date().toISOString(), checks: {} };
const browser = await chromium.launch();
const vp = { width: 1680, height: 1050 };
const ctx = await browser.newContext({ viewport: vp, deviceScaleFactor: 1 });
const page = await ctx.newPage();
page.setDefaultTimeout(90000);
await page.goto('https://reincarnated-glance.vercel.app/', { waitUntil: 'domcontentloaded' });
await page.evaluate(() => { window.location.hash = '#/atlas'; });
await page.waitForLoadState('networkidle').catch(() => {});
await page.waitForTimeout(3500);

const listByClass = await page.evaluate(() => {
  const collect = (sel) => {
    const els = [...document.querySelectorAll(sel)];
    return els.slice(0, 6).map(el => {
      const b = el.getBoundingClientRect();
      return { kit: el.getAttribute('data-kit'), tag: el.tagName.toLowerCase(), cx: el.getAttribute('cx'), cy: el.getAttribute('cy'), x: Math.round(b.left + b.width / 2), y: Math.round(b.top + b.height / 2), w: Math.round(b.width), h: Math.round(b.height) };
    });
  };
  return {
    live: collect('[data-el="live"]'),
    liveCount: document.querySelectorAll('[data-el="live"]').length,
    graveyard: collect('[data-el="graveyard"]'),
    graveCount: document.querySelectorAll('[data-el="graveyard"]').length,
    positive: collect('[data-el="positive"]'),
    positiveCount: document.querySelectorAll('[data-el="positive"]').length,
  };
});
record.checks.class_counts = { live: listByClass.liveCount, graveyard: listByClass.graveCount, positive: listByClass.positiveCount };
record.checks.samples = { live: listByClass.live, graveyard: listByClass.graveyard, positive: listByClass.positive };

const hoverKit = async (dot, label) => {
  if (!dot) return { label, status: 'no-dot' };
  // Move away first
  await page.mouse.move(100, 100);
  await page.waitForTimeout(300);
  // Scroll dot into view via layer-selector approach
  await page.evaluate((kit) => {
    const el = document.querySelector(`[data-kit="${kit}"]`);
    if (el && 'scrollIntoView' in el) el.scrollIntoView({ block: 'center' });
  }, dot.kit);
  await page.waitForTimeout(400);
  const pos = await page.evaluate((kit) => {
    const el = document.querySelector(`[data-kit="${kit}"]`);
    if (!el) return null;
    const b = el.getBoundingClientRect();
    return { x: Math.round(b.left + b.width / 2), y: Math.round(b.top + b.height / 2) };
  }, dot.kit);
  if (!pos) return { label, status: 'no-pos' };
  await page.mouse.move(pos.x, pos.y);
  await page.waitForTimeout(1600);
  const panels = await page.evaluate(() => {
    const cards = [...document.querySelectorAll('*')]
      .filter(el => {
        const cs = getComputedStyle(el);
        const b = el.getBoundingClientRect();
        return (cs.position === 'fixed' || cs.position === 'absolute')
          && cs.visibility !== 'hidden' && cs.opacity !== '0' && cs.display !== 'none'
          && b.width >= 40 && b.width <= 800 && b.height >= 14 && b.height <= 700
          && (el.textContent || '').trim().length > 3;
      })
      .map(el => { const b = el.getBoundingClientRect(); return { text: (el.textContent || '').trim().slice(0, 400), x: Math.round(b.left), y: Math.round(b.top), w: Math.round(b.width), h: Math.round(b.height), pos: getComputedStyle(el).position, z: getComputedStyle(el).zIndex }; });
    return cards.slice(0, 16);
  });
  const clip = { x: Math.max(0, pos.x - 400), y: Math.max(0, pos.y - 240), width: Math.min(vp.width - Math.max(0, pos.x - 400), 800), height: Math.min(vp.height - Math.max(0, pos.y - 240), 550) };
  const shot = `${OUT}/final2-hover-${label}-${dot.kit}.png`;
  await page.screenshot({ path: shot, clip, timeout: 60000 });
  return { label, kit: dot.kit, pos, panels, screenshot: shot };
};

if (listByClass.live[0]) record.checks.hover_live = await hoverKit(listByClass.live[0], 'live');
if (listByClass.graveyard[0]) record.checks.hover_graveyard = await hoverKit(listByClass.graveyard[0], 'graveyard');
if (listByClass.positive[0]) record.checks.hover_positive = await hoverKit(listByClass.positive[0], 'positive');

writeFileSync(`${OUT}/verify-record-final2.json`, JSON.stringify(record, null, 2));
await browser.close();
console.log('FINAL-2 DONE.');
console.log('  live/grave/positive counts:', record.checks.class_counts);
console.log('  live hover panels:', record.checks.hover_live?.panels?.length, 'kit:', record.checks.hover_live?.kit);
console.log('  grave hover panels:', record.checks.hover_graveyard?.panels?.length, 'kit:', record.checks.hover_graveyard?.kit);
console.log('  positive hover panels:', record.checks.hover_positive?.panels?.length, 'kit:', record.checks.hover_positive?.kit);
