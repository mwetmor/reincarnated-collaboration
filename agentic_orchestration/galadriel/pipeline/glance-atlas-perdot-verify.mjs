// Galadriel PER-DOT verification harness — Glance /atlas v3.
// Verifies: (2) ring centered on a real dot in dense cell, (3) per-dot resolution, (4) popover title+public_label,
// (5) UNMAPPED strip stays a LIST, (6) mobile edge-clamp. Read-only. No target-file modification.
import { chromium } from 'playwright';
import { mkdirSync, readFileSync } from 'node:fs';

const URL = 'https://reincarnated-glance-i26spw3cp-matthew-wetmore-s-projects.vercel.app/#/atlas';
const OUT = '/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-13-glance-atlas-perdot-v3';
mkdirSync(OUT, { recursive: true });

const dotJson = JSON.parse(readFileSync('/tmp/pdp.json', 'utf8'));
const dots = dotJson.dots;
const VB = dotJson.viewBox; // {w,h}

// ---- read back injected ring + popover from live DOM ----
async function readOverlay(page) {
  return await page.evaluate(() => {
    const svg = document.querySelector('svg.absolute.inset-0, svg[viewBox]');
    const svgRect = svg?.getBoundingClientRect();
    // Find highlight ring: a <circle> injected on hover (sky-blue stroke). Take the last circle with a stroke.
    const circles = [...(svg?.querySelectorAll('circle') || [])].map(c => ({
      cx: parseFloat(c.getAttribute('cx')),
      cy: parseFloat(c.getAttribute('cy')),
      r: parseFloat(c.getAttribute('r')),
      stroke: c.getAttribute('stroke') || getComputedStyle(c).stroke,
    }));
    // Popover: a fixed/absolute card with a title + mono line. Grab the topmost small floating card.
    const cards = [...document.querySelectorAll('*')].filter(el => {
      const cs = getComputedStyle(el); const b = el.getBoundingClientRect();
      return (cs.position === 'fixed' || cs.position === 'absolute')
        && b.width > 80 && b.width < 600 && b.height > 20 && b.height < 500
        && (el.textContent || '').trim().length > 3
        && cs.visibility !== 'hidden' && cs.opacity !== '0' && b.top >= -5;
    }).map(el => {
      const b = el.getBoundingClientRect();
      // detect a mono descendant (public_label line)
      const monoEl = [...el.querySelectorAll('*')].find(d => /mono/i.test(getComputedStyle(d).fontFamily));
      return {
        text: (el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 240),
        x: Math.round(b.left), y: Math.round(b.top), w: Math.round(b.width), h: Math.round(b.height),
        right: Math.round(b.right), bottom: Math.round(b.bottom),
        hasMono: !!monoEl,
        monoText: monoEl ? (monoEl.textContent || '').trim().slice(0, 120) : null,
      };
    });
    // Prefer the smallest card that has a mono line (the single-kit popover); fallback to smallest.
    cards.sort((a, b) => (a.w * a.h) - (b.w * b.h));
    const withMono = cards.filter(c => c.hasMono);
    return {
      svg: svgRect ? { x: Math.round(svgRect.left), y: Math.round(svgRect.top), w: svgRect.width, h: svgRect.height } : null,
      circles,
      popover: (withMono[0] || cards.find(c => c.h < 260) || cards[0]) || null,
      cardCount: cards.length,
    };
  });
}

const browser = await chromium.launch();

// ============ DESKTOP: alignment + per-dot ============
{
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 1000 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  const base = URL.split('#')[0];
  await page.goto(base, { waitUntil: 'domcontentloaded' });
  await page.evaluate(() => { window.location.hash = '#/atlas'; });
  await page.waitForLoadState('networkidle').catch(() => {});
  await page.waitForTimeout(3000);

  // Plane img bbox (in page coords, scroll-adjusted to viewport).
  const plane = await page.evaluate(() => {
    const svg = document.querySelector('svg[viewBox]');
    const r = svg.getBoundingClientRect();
    return { x: r.left, y: r.top, w: r.width, h: r.height, scrollY: window.scrollY };
  });
  // scroll svg into view so hover coords are within viewport
  await page.evaluate(() => document.querySelector('svg[viewBox]').scrollIntoView({ block: 'center' }));
  await page.waitForTimeout(400);
  const svgBox = await page.evaluate(() => {
    const r = document.querySelector('svg[viewBox]').getBoundingClientRect();
    return { x: r.left, y: r.top, w: r.width, h: r.height };
  });
  console.log('svg on-screen bbox:', JSON.stringify(svgBox));
  const sx = svgBox.w / VB.w, sy = svgBox.h / VB.h;
  console.log(`scale vb->screen: sx=${sx.toFixed(4)} sy=${sy.toFixed(4)}`);
  const vbToScreen = (px, py) => ({ x: svgBox.x + px * sx, y: svgBox.y + py * sy });
  const screenToVb = (X, Y) => ({ px: (X - svgBox.x) / sx, py: (Y - svgBox.y) / sy });

  // Pick 3 dense top-left dots that are well-separated so per-dot resolution is testable.
  const tl = dots.filter(x => x.cell.movement === 'FREE-MOVE' && x.cell.delivery === 'PROJECTILE');
  // widely-spaced picks
  const picks = [
    tl.reduce((a, b) => (b.px < a.px ? b : a)),             // leftmost
    tl.reduce((a, b) => (Math.abs(b.px - 165) + Math.abs(b.py - 220) < Math.abs(a.px - 165) + Math.abs(a.py - 220) ? b : a)), // center
    tl.reduce((a, b) => (b.px > a.px ? b : a)),             // rightmost
  ];

  const results = [];
  for (let i = 0; i < picks.length; i++) {
    const d = picks[i];
    const scr = vbToScreen(d.px, d.py);
    await page.mouse.move(scr.x, scr.y);
    await page.waitForTimeout(500);
    const ov = await readOverlay(page);
    // find ring circle = the one whose stroke is blue-ish OR the largest-r hover circle
    let ring = null;
    const blue = ov.circles.filter(c => /(#|rgb|sky|blue|38bdf8|0ea5e9|7dd3fc|light)/i.test(c.stroke || ''));
    ring = (blue.sort((a, b) => b.r - a.r)[0]) || ov.circles.sort((a, b) => b.r - a.r)[0] || null;
    let ringVb = null, nearest = null, offPx = null;
    if (ring) {
      // ring cx/cy are already in viewBox units (svg uses viewBox coordinate space)
      ringVb = { px: ring.cx, py: ring.cy };
      // nearest actual JSON dot to ring center
      nearest = dots.reduce((a, b) => (Math.hypot(b.px - ring.cx, b.py - ring.cy) < Math.hypot(a.px - ring.cx, a.py - ring.cy) ? b : a));
      const dvb = Math.hypot(nearest.px - ring.cx, nearest.py - ring.cy);
      offPx = { vb: dvb, screen: dvb * ((sx + sy) / 2) };
    }
    results.push({
      target: { name: d.display_name, px: d.px, py: d.py, public_label: d.public_label },
      ringCircle: ring,
      ringVb,
      nearestJsonDot: nearest ? { name: nearest.display_name, px: nearest.px, py: nearest.py } : null,
      ringToNearestDotOffset: offPx,
      targetMatchesRingNearest: nearest ? (nearest.dot_id === d.dot_id) : null,
      popover: ov.popover,
      circleCount: ov.circles.length,
    });
    // Draw a crosshair overlay marking JSON-truth target for screenshot evidence (injected, non-persistent).
    await page.evaluate(({ x, y }) => {
      let m = document.getElementById('gal-mark'); if (m) m.remove();
      m = document.createElement('div'); m.id = 'gal-mark';
      m.style.cssText = `position:fixed;left:${x - 9}px;top:${y - 9}px;width:18px;height:18px;border:2px solid magenta;border-radius:50%;pointer-events:none;z-index:99999;`;
      document.body.appendChild(m);
    }, scr);
    await page.mouse.move(scr.x, scr.y); // re-assert hover after DOM inject
    await page.waitForTimeout(300);
    // Clip around the top-left cell for evidence
    const clip = { x: Math.max(0, svgBox.x - 20), y: Math.max(0, svgBox.y - 20), width: Math.min(560, svgBox.w * 0.5), height: Math.min(560, svgBox.h * 0.55) };
    await page.screenshot({ path: `${OUT}/desktop-hover-${i}-${d.dot_id.slice(0,20)}.png`, clip });
    // full shot too for popover placement
    await page.screenshot({ path: `${OUT}/desktop-hover-${i}-full.png` });
  }

  console.log('\n===== DESKTOP PER-DOT RESULTS =====');
  console.log(JSON.stringify(results, null, 2));

  // ---- UNMAPPED strip: hover the text band, expect a LIST popover ----
  const unmapped = await page.evaluate(() => {
    // find element containing UNMAPPED / movement=unknown text
    const els = [...document.querySelectorAll('*')].filter(el => el.children.length <= 3 && /UNMAPPED|movement=unknown|roster/i.test(el.textContent || ''));
    if (!els.length) return null;
    const el = els.sort((a, b) => (a.textContent.length - b.textContent.length))[0];
    const r = el.getBoundingClientRect();
    el.scrollIntoView({ block: 'center' });
    const r2 = el.getBoundingClientRect();
    return { x: Math.round(r2.left + r2.width / 2), y: Math.round(r2.top + r2.height / 2), text: (el.textContent || '').slice(0, 80) };
  });
  let unmappedResult = null;
  if (unmapped) {
    await page.waitForTimeout(300);
    await page.mouse.move(unmapped.x, unmapped.y);
    await page.waitForTimeout(600);
    const ov = await readOverlay(page);
    // A LIST popover = a card whose text contains multiple kit-ish lines / many bullets.
    unmappedResult = {
      hoverText: unmapped.text,
      popover: ov.popover,
      // heuristic: list if popover text has several separators or is tall
      looksLikeList: ov.popover ? (ov.popover.h > 120 || (ov.popover.text.match(/·|,|\n|poe2|pure-mobility/gi) || []).length >= 4) : false,
    };
    await page.screenshot({ path: `${OUT}/desktop-unmapped-hover.png` });
  }
  console.log('\n===== UNMAPPED STRIP =====');
  console.log(JSON.stringify(unmappedResult, null, 2));

  await ctx.close();
}

// ============ MOBILE: edge-clamp ============
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
  // pick a dot near the RIGHT edge (SUMMON column, e.g. free-move × summon) to force clamp
  const rightDots = dots.filter(d => d.cell.delivery === 'SUMMON' && d.cell.movement === 'FREE-MOVE');
  const pick = rightDots.reduce((a, b) => (b.px > a.px ? b : a), rightDots[0] || dots.reduce((a,b)=>b.px>a.px?b:a));
  const scr = { x: svgBox.x + pick.px * sx, y: svgBox.y + pick.py * sy };
  await page.mouse.move(scr.x, scr.y);
  await page.waitForTimeout(600);
  const ov = await readOverlay(page);
  const clamp = ov.popover ? {
    popover: ov.popover,
    viewportW: 375,
    onScreen: ov.popover.x >= 0 && ov.popover.right <= 375 + 1,
    overflowRightPx: Math.max(0, ov.popover.right - 375),
    overflowLeftPx: Math.max(0, -ov.popover.x),
  } : { popover: null };
  console.log('\n===== MOBILE 375px EDGE CLAMP =====');
  console.log('target dot:', pick.display_name, 'px=', pick.px.toFixed(1), '-> screenX', Math.round(scr.x), 'of 375');
  console.log(JSON.stringify(clamp, null, 2));
  await page.screenshot({ path: `${OUT}/mobile-375-edge-hover.png`, fullPage: true });
  await ctx.close();
}

await browser.close();
console.log('\nDONE. captures in', OUT);
