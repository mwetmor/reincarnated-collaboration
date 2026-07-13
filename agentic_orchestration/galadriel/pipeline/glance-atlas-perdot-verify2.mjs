// Galadriel PER-DOT verify — round 2: clean 3rd desktop dot, UNMAPPED list (fixed coords), mobile edge-clamp.
import { chromium } from 'playwright';
import { mkdirSync, readFileSync } from 'node:fs';

const URL = 'https://reincarnated-glance-i26spw3cp-matthew-wetmore-s-projects.vercel.app/#/atlas';
const OUT = '/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-13-glance-atlas-perdot-v3';
mkdirSync(OUT, { recursive: true });
const dotJson = JSON.parse(readFileSync('/tmp/pdp.json', 'utf8'));
const dots = dotJson.dots; const VB = dotJson.viewBox;

async function readOverlay(page) {
  return await page.evaluate(() => {
    const svg = document.querySelector('svg[viewBox]');
    const circles = [...(svg?.querySelectorAll('circle') || [])].map(c => ({
      cx: parseFloat(c.getAttribute('cx')), cy: parseFloat(c.getAttribute('cy')),
      r: parseFloat(c.getAttribute('r')), stroke: c.getAttribute('stroke') || getComputedStyle(c).stroke,
    }));
    const cards = [...document.querySelectorAll('*')].filter(el => {
      const cs = getComputedStyle(el); const b = el.getBoundingClientRect();
      return (cs.position === 'fixed' || cs.position === 'absolute')
        && b.width > 80 && b.width < 600 && b.height > 20 && b.height < 560
        && (el.textContent || '').trim().length > 3 && cs.visibility !== 'hidden' && cs.opacity !== '0' && b.top >= -5;
    }).map(el => {
      const b = el.getBoundingClientRect();
      const monoEl = [...el.querySelectorAll('*')].find(d => /mono/i.test(getComputedStyle(d).fontFamily));
      // count list-ish child rows
      const rows = el.querySelectorAll('li, [class*="row"], div > div').length;
      return { text: (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 300),
        x: Math.round(b.left), y: Math.round(b.top), w: Math.round(b.width), h: Math.round(b.height),
        right: Math.round(b.right), bottom: Math.round(b.bottom), hasMono: !!monoEl, rows };
    });
    cards.sort((a, b) => (a.w * a.h) - (b.w * b.h));
    const withMono = cards.filter(c => c.hasMono);
    return { circles, popover: (withMono[0] || cards[0]) || null, allCards: cards.slice(0, 6) };
  });
}

const browser = await chromium.launch();

// ---------- DESKTOP: clean 3rd dot + UNMAPPED ----------
{
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 1000 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  const base = URL.split('#')[0];
  await page.goto(base, { waitUntil: 'domcontentloaded' });
  await page.evaluate(() => { window.location.hash = '#/atlas'; });
  await page.waitForLoadState('networkidle').catch(() => {});
  await page.waitForTimeout(3000);
  await page.evaluate(() => document.querySelector('svg[viewBox]').scrollIntoView({ block: 'center' }));
  await page.waitForTimeout(400);
  const svgBox = await page.evaluate(() => { const r = document.querySelector('svg[viewBox]').getBoundingClientRect(); return { x: r.left, y: r.top, w: r.width, h: r.height }; });
  const sx = svgBox.w / VB.w, sy = svgBox.h / VB.h;
  const vbToScreen = (px, py) => ({ x: svgBox.x + px * sx, y: svgBox.y + py * sy });

  // clean 3rd dot: an interior top-left dot far from the two already tested
  const tl = dots.filter(x => x.cell.movement === 'FREE-MOVE' && x.cell.delivery === 'PROJECTILE');
  const pick = tl.reduce((a,b)=> (Math.abs(b.px-150)+Math.abs(b.py-245) < Math.abs(a.px-150)+Math.abs(a.py-245) ? b : a));
  const scr = vbToScreen(pick.px, pick.py);
  await page.mouse.move(scr.x, scr.y); await page.waitForTimeout(500);
  const ov = await readOverlay(page);
  const ring = ov.circles.sort((a,b)=>b.r-a.r)[0] || null;
  const nearest = ring ? dots.reduce((a,b)=>Math.hypot(b.px-ring.cx,b.py-ring.cy)<Math.hypot(a.px-ring.cx,a.py-ring.cy)?b:a) : null;
  console.log('===== 3RD DESKTOP DOT =====');
  console.log('target:', pick.display_name, 'px', pick.px.toFixed(1), 'py', pick.py.toFixed(1));
  console.log('ring:', JSON.stringify(ring));
  console.log('nearest JSON dot to ring:', nearest?.display_name, 'offsetVb:', ring&&nearest?Math.hypot(nearest.px-ring.cx,nearest.py-ring.cy).toFixed(3):null);
  console.log('matches target:', nearest?.dot_id === pick.dot_id);
  console.log('popover:', JSON.stringify(ov.popover));

  // UNMAPPED strip — measure element center AFTER scrolling it into view, then hover in the same frame's coords
  const um = await page.evaluate(() => {
    const els = [...document.querySelectorAll('*')].filter(el => el.children.length <= 4 && /movement=unknown|pure-mobility residual|UNMAPPED/i.test(el.textContent || ''));
    if (!els.length) return null;
    const el = els.sort((a,b)=>a.textContent.length-b.textContent.length).find(e=>/poe2|B10|movement=unknown/i.test(e.textContent)) || els[0];
    el.scrollIntoView({ block: 'center' });
    return true;
  });
  await page.waitForTimeout(400);
  const umBox = await page.evaluate(() => {
    const els = [...document.querySelectorAll('*')].filter(el => el.children.length <= 4 && /movement=unknown|pure-mobility residual/i.test(el.textContent || ''));
    if (!els.length) return null;
    const el = els.sort((a,b)=>a.textContent.length-b.textContent.length)[0];
    const r = el.getBoundingClientRect();
    return { x: Math.round(r.left + Math.min(r.width/2, 120)), y: Math.round(r.top + r.height/2), text: (el.textContent||'').slice(0,70) };
  });
  let umResult = null;
  if (umBox) {
    await page.mouse.move(umBox.x, umBox.y); await page.waitForTimeout(700);
    const ov2 = await readOverlay(page);
    umResult = { hoverText: umBox.text, popover: ov2.popover,
      looksLikeList: ov2.popover ? (ov2.popover.h > 110 || (ov2.popover.text.match(/·|,|poe2|B1[0-9]|K[0-9]/gi)||[]).length >= 5) : false };
    await page.screenshot({ path: `${OUT}/desktop-unmapped-hover.png` });
  }
  console.log('\n===== UNMAPPED STRIP =====');
  console.log(JSON.stringify(umResult, null, 2));
  await ctx.close();
}

// ---------- MOBILE 375: right-edge clamp ----------
{
  const ctx = await browser.newContext({ viewport: { width: 375, height: 812 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  const page = await ctx.newPage();
  const base = URL.split('#')[0];
  await page.goto(base, { waitUntil: 'domcontentloaded' });
  await page.evaluate(() => { window.location.hash = '#/atlas'; });
  await page.waitForLoadState('networkidle').catch(() => {});
  await page.waitForTimeout(3000);
  await page.evaluate(() => document.querySelector('svg[viewBox]').scrollIntoView({ block: 'center' }));
  await page.waitForTimeout(400);
  const svgBox = await page.evaluate(() => { const r = document.querySelector('svg[viewBox]').getBoundingClientRect(); return { x: r.left, y: r.top, w: r.width, h: r.height }; });
  const sx = svgBox.w / VB.w, sy = svgBox.h / VB.h;
  console.log('\n===== MOBILE svg bbox =====', JSON.stringify(svgBox), 'sx', sx.toFixed(3));
  // Find a dot whose ON-SCREEN x is near the right edge of the 375 viewport (within visible plane).
  const scored = dots.map(d => ({ d, X: svgBox.x + d.px * sx, Y: svgBox.y + d.py * sy }))
    .filter(o => o.X > 0 && o.X < 375 && o.Y > 0 && o.Y < 812);
  scored.sort((a,b)=> b.X - a.X); // rightmost visible
  const target = scored[0];
  if (!target) { console.log('no visible dot found on mobile plane'); }
  else {
    console.log('rightmost-visible dot:', target.d.display_name, 'screenX', Math.round(target.X), 'of 375');
    await page.mouse.move(target.X, target.Y); await page.waitForTimeout(700);
    const ov = await readOverlay(page);
    const clamp = ov.popover ? {
      popover: ov.popover, viewportW: 375,
      onScreen: ov.popover.x >= -1 && ov.popover.right <= 376,
      overflowRightPx: Math.max(0, ov.popover.right - 375), overflowLeftPx: Math.max(0, -ov.popover.x),
    } : { popover: null, note: 'no popover captured' };
    console.log(JSON.stringify(clamp, null, 2));
    await page.screenshot({ path: `${OUT}/mobile-375-edge-hover.png` });
    // crop clip around popover for evidence
    if (ov.popover) {
      const c = { x: Math.max(0, ov.popover.x-10), y: Math.max(0, ov.popover.y-10), width: Math.min(375, ov.popover.w+40), height: Math.min(812, ov.popover.h+40) };
      await page.screenshot({ path: `${OUT}/mobile-375-popover-crop.png`, clip: c });
    }
  }
  await ctx.close();
}

await browser.close();
console.log('\nDONE round2');
