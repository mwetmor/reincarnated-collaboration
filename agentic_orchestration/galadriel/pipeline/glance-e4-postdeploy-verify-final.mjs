// FINAL — captures both skins as separate fullpage shots AND re-tests tooltip.
// Key discovery: r3 saw pixelIdentical=false in theme viewport shot, so toggle IS working.
// Diagnostic revealed the toggle changes plate canvas, not body bg.
// Also: use the r1 confirmed kit-dot coordinates and hover via Playwright hover() on selector.
import { chromium } from 'playwright';
import { mkdirSync, writeFileSync, readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';

const URL = 'https://reincarnated-glance.vercel.app/';
const OUT = '/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-17-glance-e4-postdeploy';
mkdirSync(OUT, { recursive: true });
const md5 = (p) => createHash('md5').update(readFileSync(p)).digest('hex');

const record = { url: URL, captured_at: new Date().toISOString(), checks: {} };
const consoleErrors = [];
const reqfails = [];
const browser = await chromium.launch();
const vp = { width: 1680, height: 1050 };
const ctx = await browser.newContext({ viewport: vp, deviceScaleFactor: 1 });
const page = await ctx.newPage();
page.setDefaultTimeout(90000);
page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text()); });
page.on('requestfailed', r => reqfails.push(`${r.url()} ${(r.failure()?.errorText || '')}`));
page.on('response', r => { if (r.status() >= 400) reqfails.push(`HTTP ${r.status()} ${r.url()}`); });

await page.goto(URL, { waitUntil: 'domcontentloaded' });
await page.evaluate(() => { window.location.hash = '#/atlas'; });
await page.waitForLoadState('networkidle').catch(() => {});
await page.waitForTimeout(4000);

// -------- (a, c, f, d) — full-page shot in DEFAULT (dark archive) skin --------
try { await page.screenshot({ path: `${OUT}/final-fullpage-archive-1680.png`, fullPage: true, timeout: 120000 }); }
catch (e) { record.checks.archive_fp_err = String(e).slice(0, 200); }

// -------- (b) — targeted tooltip test on r1-confirmed kit id --------
// r1 log: chr-arrow-storm-warden at (850, 603). Use Playwright locator-based hover, longer wait.
const b_probe = {};

// discover current kit dots (id-space may have changed)
const kitScan = await page.evaluate(() => {
  const all = document.querySelectorAll('[id^="chr-"],[id^="tq"],[id^="tl"],[id^="tg"]');
  const first20 = [...all].slice(0, 20).map(el => {
    const b = el.getBoundingClientRect();
    return { id: el.id, tag: el.tagName, x: Math.round(b.left + b.width / 2), y: Math.round(b.top + b.height / 2), w: Math.round(b.width), h: Math.round(b.height), visible: b.width > 0 && b.height > 0 };
  });
  return { total: all.length, sample: first20 };
});
b_probe.kit_scan = kitScan;

// Direct hover via Playwright locator
const tryHover = async (id) => {
  const loc = page.locator(`#${id}`);
  const count = await loc.count();
  if (count === 0) return { id, status: 'NOT-IN-DOM' };
  await loc.first().scrollIntoViewIfNeeded().catch(() => {});
  await page.waitForTimeout(400);
  const beforeBody = await page.evaluate(() => (document.body.innerText || '').length);
  await loc.first().hover({ force: true, timeout: 30000 }).catch((e) => { b_probe['hover_err_' + id] = String(e).slice(0, 100); });
  await page.waitForTimeout(1400);
  const state = await page.evaluate(() => {
    // Enumerate visible positioned tooltip-like nodes
    const cards = [...document.querySelectorAll('div,section,aside,span')]
      .filter(el => {
        const cs = getComputedStyle(el);
        const b = el.getBoundingClientRect();
        return (cs.position === 'fixed' || cs.position === 'absolute')
          && cs.visibility !== 'hidden' && cs.opacity !== '0' && cs.display !== 'none'
          && b.width >= 60 && b.width <= 700 && b.height >= 20 && b.height <= 500
          && (el.textContent || '').trim().length > 3;
      })
      .map(el => { const b = el.getBoundingClientRect(); return { text: (el.textContent || '').trim().slice(0, 300), x: Math.round(b.left), y: Math.round(b.top), w: Math.round(b.width), h: Math.round(b.height), zIndex: getComputedStyle(el).zIndex }; });
    return { cards: cards.slice(0, 12), bodyLen: (document.body.innerText || '').length };
  });
  // Save close-up screenshot
  const box = await loc.first().boundingBox().catch(() => null);
  if (box) {
    const clip = { x: Math.max(0, box.x - 350), y: Math.max(0, box.y - 220), width: Math.min(vp.width - Math.max(0, box.x - 350), 780), height: Math.min(vp.height - Math.max(0, box.y - 220), 500) };
    try { await page.screenshot({ path: `${OUT}/final-hover-${id}.png`, clip, timeout: 60000 }); } catch {}
  }
  return { id, state, beforeBodyLen: beforeBody, deltaBodyLen: state.bodyLen - beforeBody };
};

b_probe.live = await tryHover('chr-arrow-storm-warden');
b_probe.grave = await tryHover('tq2-bastion-tank');
b_probe.positive = await tryHover('tl2-shadowling-outlander');

// Move away
await page.mouse.move(0, 0);
await page.waitForTimeout(500);

record.checks.b_final = b_probe;

// -------- (e) — click Light instrument button, capture fullpage --------
const clickLight = await page.evaluate(() => {
  const btns = [...document.querySelectorAll('button,[role="button"]')];
  const t = btns.find(el => /light.*instrument|lightinstrument/i.test((el.textContent || '').replace(/\s+/g, '')));
  if (!t) return { clicked: false };
  t.click();
  return { clicked: true };
});
await page.waitForTimeout(2500);
try { await page.screenshot({ path: `${OUT}/final-fullpage-instrument-1680.png`, fullPage: true, timeout: 120000 }); }
catch (e) { record.checks.instrument_fp_err = String(e).slice(0, 200); }

// Click back to Dark archive
await page.evaluate(() => {
  const btns = [...document.querySelectorAll('button,[role="button"]')];
  const t = btns.find(el => /dark.*archive|darkarchive/i.test((el.textContent || '').replace(/\s+/g, '')));
  if (t) t.click();
});
await page.waitForTimeout(1200);
try { await page.screenshot({ path: `${OUT}/final-viewport-archive-verify.png`, timeout: 60000 }); } catch {}

// Now MD5 verify
try {
  const archMd5 = md5(`${OUT}/final-fullpage-archive-1680.png`);
  const instMd5 = md5(`${OUT}/final-fullpage-instrument-1680.png`);
  record.checks.e_final = { archive_md5: archMd5, instrument_md5: instMd5, differ: archMd5 !== instMd5 };
} catch (e) { record.checks.e_final = { err: String(e).slice(0, 200) }; }

// -------- Final gather --------
record.checks.d_final_console = { errors: consoleErrors, reqfails, err_count: consoleErrors.length, reqfail_count: reqfails.length };

writeFileSync(`${OUT}/verify-record-final.json`, JSON.stringify(record, null, 2));
await browser.close();

console.log('FINAL DONE.');
console.log('  kit_scan total=' + kitScan.total);
console.log('  b_live cards=' + (b_probe.live.state?.cards?.length ?? 'ERR'));
console.log('  b_grave cards=' + (b_probe.grave.state?.cards?.length ?? 'ERR'));
console.log('  b_positive cards=' + (b_probe.positive.state?.cards?.length ?? 'ERR'));
console.log('  e_final differ=' + record.checks.e_final?.differ);
console.log('  console errors=' + consoleErrors.length, 'reqfails=' + reqfails.length);
