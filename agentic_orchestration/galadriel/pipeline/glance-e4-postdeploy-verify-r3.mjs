// Round-3 — targeted verification for (b) tooltip content + folk_name/game join, (e) skin toggle.
// Use r1-confirmed kit id `chr-arrow-storm-warden`. Wait harder for tooltip.
// Toggle: click Lightinstrument button by text; compare viewport pixels; also check body class/attr changes.
import { chromium } from 'playwright';
import { mkdirSync, writeFileSync, readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';

const URL = 'https://reincarnated-glance.vercel.app/';
const OUT = '/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-17-glance-e4-postdeploy';
mkdirSync(OUT, { recursive: true });
const md5 = (p) => createHash('md5').update(readFileSync(p)).digest('hex');

const record = { url: URL, captured_at: new Date().toISOString(), checks: {} };
const browser = await chromium.launch();
const vp = { width: 1680, height: 1050 };
const ctx = await browser.newContext({ viewport: vp, deviceScaleFactor: 1 });
const page = await ctx.newPage();
page.setDefaultTimeout(90000);

await page.goto(URL, { waitUntil: 'domcontentloaded' });
await page.evaluate(() => { window.location.hash = '#/atlas'; });
await page.waitForLoadState('networkidle').catch(() => {});
await page.waitForTimeout(3000);

// -------- (b) — targeted kit-dot hover via specific known id + generous wait --------
// Confirmed r1 ids: chr-arrow-storm-warden, tq2-bastion-tank, tl2-shadowling-outlander.
const targets = [
  { id: 'chr-arrow-storm-warden', label: 'live-chr' },
  { id: 'tq2-bastion-tank', label: 'graveyard-tq2' },
  { id: 'tl2-shadowling-outlander', label: 'positive-tl2' },
];

// Discover full id-space now (for later)
const idSpace = await page.evaluate(() => {
  const els = [...document.querySelectorAll('circle[id],line[id],rect[id],path[id]')];
  const prefixes = {};
  for (const el of els) {
    const id = el.id;
    const p = (id.match(/^([a-z0-9]+)-/i) || [null, 'none'])[1];
    prefixes[p] = (prefixes[p] || 0) + 1;
  }
  return { total: els.length, prefixes };
});
record.checks.id_space = idSpace;

const hoverRigorous = async (t) => {
  const found = await page.evaluate((id) => {
    const el = document.getElementById(id);
    if (!el) return null;
    const b = el.getBoundingClientRect();
    return { x: Math.round(b.left + b.width / 2), y: Math.round(b.top + b.height / 2), w: Math.round(b.width), h: Math.round(b.height), tag: el.tagName, hasTitle: !!el.querySelector('title'), titleText: el.querySelector('title')?.textContent || null };
  }, t.id);
  if (!found) return { ...t, status: 'DOM-NOT-FOUND' };
  // Move away, then scroll into view, then hover slowly
  await page.mouse.move(0, 0);
  await page.waitForTimeout(300);
  await page.evaluate((id) => {
    const el = document.getElementById(id);
    if (el && 'scrollIntoView' in el) el.scrollIntoView({ behavior: 'instant', block: 'center' });
  }, t.id);
  await page.waitForTimeout(400);
  // Re-fetch coords after scroll
  const found2 = await page.evaluate((id) => {
    const el = document.getElementById(id);
    if (!el) return null;
    const b = el.getBoundingClientRect();
    return { x: Math.round(b.left + b.width / 2), y: Math.round(b.top + b.height / 2) };
  }, t.id);
  await page.mouse.move(found2.x, found2.y);
  await page.waitForTimeout(1500);
  // Capture ALL text content that appeared: full body text, plus any hover-shown element
  const hoverState = await page.evaluate(() => {
    // Look for elements with high z-index or position:fixed/absolute recently mutated
    const layerTexts = [];
    const all = document.querySelectorAll('*');
    for (const el of all) {
      const cs = getComputedStyle(el);
      if (cs.pointerEvents === 'none' && (cs.position === 'fixed' || cs.position === 'absolute') && cs.visibility !== 'hidden' && cs.opacity !== '0' && cs.display !== 'none') {
        const b = el.getBoundingClientRect();
        if (b.width > 30 && b.width < 700 && b.height > 12 && b.height < 400) {
          const t = (el.textContent || '').trim();
          if (t.length > 3 && t.length < 500) layerTexts.push({ text: t.slice(0, 300), x: Math.round(b.left), y: Math.round(b.top), w: Math.round(b.width), h: Math.round(b.height), pos: cs.position, z: cs.zIndex });
        }
      }
    }
    // Also grab any SVG <title> tooltip visible via native browser mechanism (won't render but content exists)
    return { layerTexts: layerTexts.slice(0, 20) };
  });
  // Screenshot near the target
  const clip = { x: Math.max(0, found2.x - 350), y: Math.max(0, found2.y - 200), width: Math.min(vp.width - Math.max(0, found2.x - 350), 780), height: Math.min(vp.height - Math.max(0, found2.y - 200), 500) };
  const shot = `${OUT}/hover-r3-${t.label}.png`;
  await page.screenshot({ path: shot, clip, timeout: 60000 });
  return { ...t, found, found2, hoverState, screenshot: shot };
};

record.checks.b_r3_hover_live = await hoverRigorous(targets[0]);
record.checks.b_r3_hover_grave = await hoverRigorous(targets[1]);
record.checks.b_r3_hover_positive = await hoverRigorous(targets[2]);

// -------- (e) skin toggle rigorous — button pixel-verify --------
const bgBefore = await page.evaluate(() => ({
  body: getComputedStyle(document.body).backgroundColor,
  htmlBg: getComputedStyle(document.documentElement).backgroundColor,
  themeAttr: document.documentElement.getAttribute('data-theme') || document.body.getAttribute('data-theme') || null,
  bodyClasses: document.body.className || null,
  htmlClasses: document.documentElement.className || null,
}));
await page.screenshot({ path: `${OUT}/theme-preclick-r3.png`, clip: { x: 0, y: 0, width: 1680, height: 400 }, timeout: 60000 });

// Click "Lightinstrument"
const clickResult = await page.evaluate(() => {
  const btns = [...document.querySelectorAll('button,[role="button"]')];
  const target = btns.find(el => /light.*instrument|instrument.*light|lightinstrument/i.test((el.textContent || '').replace(/\s+/g, '')));
  if (!target) return { clicked: false, note: 'button-not-found' };
  target.click();
  return { clicked: true, text: (target.textContent || '').trim().slice(0, 40) };
});
await page.waitForTimeout(1500);
const bgAfter = await page.evaluate(() => ({
  body: getComputedStyle(document.body).backgroundColor,
  htmlBg: getComputedStyle(document.documentElement).backgroundColor,
  themeAttr: document.documentElement.getAttribute('data-theme') || document.body.getAttribute('data-theme') || null,
  bodyClasses: document.body.className || null,
  htmlClasses: document.documentElement.className || null,
}));
await page.screenshot({ path: `${OUT}/theme-postclick-instrument-r3.png`, clip: { x: 0, y: 0, width: 1680, height: 400 }, timeout: 60000 });

record.checks.e_theme_diagnostic = { clickResult, bgBefore, bgAfter, bgChanged: JSON.stringify(bgBefore) !== JSON.stringify(bgAfter) };

// Grab full-page for each skin
if (record.checks.e_theme_diagnostic.bgChanged) {
  try { await page.screenshot({ path: `${OUT}/atlas-fullpage-instrument-r3.png`, fullPage: true, timeout: 120000 }); }
  catch (e) { record.checks.instrument_fp_err = String(e).slice(0, 200); }
  // Click Darkarchive to switch back
  await page.evaluate(() => {
    const btns = [...document.querySelectorAll('button,[role="button"]')];
    const t = btns.find(el => /dark.*archive|archive.*dark|darkarchive/i.test((el.textContent || '').replace(/\s+/g, '')));
    if (t) t.click();
  });
  await page.waitForTimeout(1500);
  try { await page.screenshot({ path: `${OUT}/atlas-fullpage-archive-r3.png`, fullPage: true, timeout: 120000 }); }
  catch (e) { record.checks.archive_fp_err = String(e).slice(0, 200); }
}

// MD5 check of the two theme viewport shots
try {
  const md5Pre = md5(`${OUT}/theme-preclick-r3.png`);
  const md5Post = md5(`${OUT}/theme-postclick-instrument-r3.png`);
  record.checks.e_pixel_verify = { pre: md5Pre, post: md5Post, identical: md5Pre === md5Post };
} catch {}

writeFileSync(`${OUT}/verify-record-r3.json`, JSON.stringify(record, null, 2));
await browser.close();
console.log('R3 DONE.');
console.log('  id_space total=' + idSpace.total, JSON.stringify(idSpace.prefixes).slice(0, 200));
console.log('  hover live layerTexts:', record.checks.b_r3_hover_live.hoverState?.layerTexts?.length ?? 'NF');
console.log('  hover grave layerTexts:', record.checks.b_r3_hover_grave.hoverState?.layerTexts?.length ?? 'NF');
console.log('  hover positive layerTexts:', record.checks.b_r3_hover_positive.hoverState?.layerTexts?.length ?? 'NF');
console.log('  theme clicked=' + record.checks.e_theme_diagnostic.clickResult.clicked, 'bgChanged=' + record.checks.e_theme_diagnostic.bgChanged, 'pixelIdentical=' + record.checks.e_pixel_verify?.identical);
