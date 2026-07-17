// Round-2 — tighten (b) hover-tooltip detection via before/after DOM delta,
// and (e) skin toggle: capture initial theme, click both plausible toggles, compare pixel diffs.
import { chromium } from 'playwright';
import { mkdirSync, writeFileSync, readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';

const URL = 'https://reincarnated-glance.vercel.app/';
const OUT = '/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-17-glance-e4-postdeploy';
mkdirSync(OUT, { recursive: true });

const md5 = (p) => createHash('md5').update(readFileSync(p)).digest('hex');

const record = { url: URL, captured_at: new Date().toISOString(), viewport: null, checks: {} };
const browser = await chromium.launch();
const vp = { width: 1680, height: 1050 };
record.viewport = vp;
const ctx = await browser.newContext({ viewport: vp, deviceScaleFactor: 1 });
const page = await ctx.newPage();
page.setDefaultTimeout(90000);

await page.goto(URL, { waitUntil: 'domcontentloaded' });
await page.evaluate(() => { window.location.hash = '#/atlas'; });
await page.waitForLoadState('networkidle').catch(() => {});
await page.waitForTimeout(2500);

// -------- (b) rigorous hover-tooltip detection via DOM delta --------
const baseline = await page.evaluate(() => {
  return [...document.querySelectorAll('*')].map(el => el.tagName + '#' + (el.id || '') + '.' + (el.className && el.className.baseVal !== undefined ? el.className.baseVal : el.className || '')).join('|').length;
});

const bucketByPrefix = await page.evaluate(() => {
  // Kit dots use id prefix chr- (live), tq2- / etc, tl2-, tg- ; scan set
  const els = [...document.querySelectorAll('circle[id],rect[id],path[id],line[id],g[id]')];
  const buckets = {};
  for (const el of els) {
    const id = el.getAttribute('id') || '';
    const b = el.getBoundingClientRect();
    if (b.width <= 0 || b.height <= 0) continue;
    const prefix = (id.match(/^([a-z0-9]+)-/i) || [null, 'none'])[1];
    if (!buckets[prefix]) buckets[prefix] = { count: 0, samples: [] };
    buckets[prefix].count += 1;
    if (buckets[prefix].samples.length < 5) {
      buckets[prefix].samples.push({ id, tag: el.tagName.toLowerCase(), x: Math.round(b.left + b.width / 2), y: Math.round(b.top + b.height / 2) });
    }
  }
  const summary = Object.entries(buckets).map(([k, v]) => ({ prefix: k, count: v.count, first: v.samples[0] }));
  summary.sort((a, b) => b.count - a.count);
  return summary;
});
record.checks.b_id_buckets = bucketByPrefix.slice(0, 20);

// Pick specific candidates per class: chr- (live), tomb- or tq-/tl-/tg- (graveyard candidates),
// and any "positive" — the invocation says path-A admissions (50 members). Try id-prefix pos- or similar.
const pickBy = (prefix) => {
  const bkt = bucketByPrefix.find(b => b.prefix === prefix);
  return bkt ? bkt.first : null;
};

// Diagnostic: log discovered id prefixes for manual review
const chrDot = pickBy('chr');       // live (Path-A confirmed builds)
const graveDot = pickBy('tq2') || pickBy('tomb') || pickBy('tq') || pickBy('gv');
// positive: try pos-, path-, adm-, then fall back to distinctive later-alphabet prefix
const posDot = pickBy('pos') || pickBy('path') || pickBy('adm') || pickBy('new') || pickBy('cand');

const doHoverProbe = async (dot, label) => {
  if (!dot) return { label, status: 'CANDIDATE-NOT-FOUND' };
  // Snapshot panels present before hover
  const before = await page.evaluate(() => {
    return [...document.querySelectorAll('div,span,section,aside')]
      .filter(el => { const cs = getComputedStyle(el); const b = el.getBoundingClientRect();
        return (cs.position === 'fixed' || cs.position === 'absolute')
          && cs.visibility !== 'hidden' && cs.opacity !== '0' && cs.display !== 'none'
          && b.width > 40 && b.height > 12; })
      .map(el => { const b = el.getBoundingClientRect(); return {
        text: (el.textContent || '').trim().slice(0, 200),
        x: Math.round(b.left), y: Math.round(b.top),
        w: Math.round(b.width), h: Math.round(b.height),
      }; });
  });
  await page.mouse.move(0, 0);
  await page.waitForTimeout(200);
  await page.mouse.move(dot.x, dot.y);
  await page.waitForTimeout(900);
  const after = await page.evaluate(() => {
    return [...document.querySelectorAll('div,span,section,aside')]
      .filter(el => { const cs = getComputedStyle(el); const b = el.getBoundingClientRect();
        return (cs.position === 'fixed' || cs.position === 'absolute')
          && cs.visibility !== 'hidden' && cs.opacity !== '0' && cs.display !== 'none'
          && b.width > 40 && b.height > 12; })
      .map(el => { const b = el.getBoundingClientRect(); return {
        text: (el.textContent || '').trim().slice(0, 400),
        x: Math.round(b.left), y: Math.round(b.top),
        w: Math.round(b.width), h: Math.round(b.height),
      }; });
  });
  // Find "new" panels: appear in after but not before, by (x,y) coord ~equal
  const key = (p) => `${p.x},${p.y},${p.w}x${p.h}`;
  const beforeKeys = new Set(before.map(key));
  const newPanels = after.filter(p => !beforeKeys.has(key(p)));
  // Screenshot the hover region
  const clip = {
    x: Math.max(0, dot.x - 300),
    y: Math.max(0, dot.y - 220),
    width: Math.min(vp.width - Math.max(0, dot.x - 300), 720),
    height: Math.min(vp.height - Math.max(0, dot.y - 220), 500),
  };
  const shot = `${OUT}/hover-r2-${label}.png`;
  await page.screenshot({ path: shot, clip, timeout: 60000 });
  // Body-text delta as another signal
  const bodyDelta = await page.evaluate((prev) => {
    const t = (document.body.innerText || '');
    return { length: t.length, delta_vs_prev: t.length - prev };
  }, baseline);
  return { label, dot, before_count: before.length, after_count: after.length, new_panel_count: newPanels.length, new_panels: newPanels.slice(0, 4), bodyDelta, screenshot: shot };
};

record.checks.b_hover_r2_live = await doHoverProbe(chrDot, 'live');
record.checks.b_hover_r2_grave = await doHoverProbe(graveDot, 'graveyard');
record.checks.b_hover_r2_positive = await doHoverProbe(posDot, 'positive');

// Also: hover a chr- dot but move a click event / verify tooltip
// The E3→E4 change may show tooltip as SVG <title> or via data-tippy — capture SVG <title> content too
const svgTitleProbe = await page.evaluate(() => {
  const dots = [...document.querySelectorAll('circle[id^="chr-"]')].slice(0, 6);
  const titles = dots.map(d => {
    const t = d.querySelector('title');
    return { id: d.id, hasTitle: !!t, titleText: t ? (t.textContent || '').trim().slice(0, 200) : null };
  });
  return titles;
});
record.checks.b_svg_title_probe = svgTitleProbe;

// -------- (e) skin toggle: identify both variants, click each with pixel-verify --------
const toggles = await page.evaluate(() => {
  const btns = [...document.querySelectorAll('button,[role="button"],a,input[type="button"]')];
  const t = btns.filter(el => {
    const label = ((el.textContent || '') + ' ' + (el.getAttribute('aria-label') || '') + ' ' + (el.title || '')).toLowerCase();
    return /skin|theme|instrument|archive/.test(label);
  }).map(el => {
    const b = el.getBoundingClientRect();
    return { text: (el.textContent || '').trim().slice(0, 60), title: el.title || null, aria: el.getAttribute('aria-label') || null, x: Math.round(b.left + b.width / 2), y: Math.round(b.top + b.height / 2), w: Math.round(b.width), h: Math.round(b.height) };
  });
  return t;
});
record.checks.e_toggle_candidates = toggles;

// Snapshot the default theme background color for pixel-verify
const bg = async () => await page.evaluate(() => {
  return {
    body: getComputedStyle(document.body).backgroundColor,
    docEl: getComputedStyle(document.documentElement).backgroundColor,
  };
});
const bgBefore = await bg();
record.checks.e_bg_before = bgBefore;

// Take a viewport shot to verify pre-toggle state (guard: keep header visible so light/dark shows)
await page.screenshot({ path: `${OUT}/atlas-viewport-preTogg.png`, timeout: 60000 });

// Try each candidate that CONTAINS the word "instrument" or is not the currently-active one
let toggledOK = false;
for (const cand of toggles) {
  const label = ((cand.text || '') + ' ' + (cand.title || '') + ' ' + (cand.aria || '')).toLowerCase();
  // Skip if likely current (title says "current" or looks selected)
  await page.mouse.move(cand.x, cand.y);
  await page.waitForTimeout(150);
  await page.mouse.click(cand.x, cand.y);
  await page.waitForTimeout(900);
  const bgNow = await bg();
  const changed = JSON.stringify(bgNow) !== JSON.stringify(bgBefore);
  if (changed) {
    await page.screenshot({ path: `${OUT}/atlas-viewport-postTogg.png`, timeout: 60000 });
    record.checks.e_toggle_success = { clicked: cand, bg_before: bgBefore, bg_after: bgNow };
    toggledOK = true;
    // Toggle back
    await page.mouse.click(cand.x, cand.y);
    await page.waitForTimeout(600);
    break;
  }
}
if (!toggledOK) record.checks.e_toggle_success = { note: 'Clicked all candidates, background did not change — theme may auto-persist or single-skin build.' };

// Full-page with delay for candidate-island lazy paint
await page.evaluate(() => window.scrollTo(0, 0));
await page.waitForTimeout(500);
try { await page.screenshot({ path: `${OUT}/atlas-fullpage-r2-1680.png`, fullPage: true, timeout: 120000 }); }
catch (e) { record.checks.fullpage_err = String(e).slice(0, 200); }

writeFileSync(`${OUT}/verify-record-r2.json`, JSON.stringify(record, null, 2));

// MD5 of the two "toggle" fullpage shots from r1
try {
  const a = md5(`${OUT}/atlas-fullpage-default-1680.png`);
  const b = md5(`${OUT}/atlas-fullpage-alt-1680.png`);
  record.checks.e_r1_md5_check = { default: a, alt: b, identical: a === b };
  writeFileSync(`${OUT}/verify-record-r2.json`, JSON.stringify(record, null, 2));
} catch {}

await browser.close();
console.log('R2 DONE.');
console.log('  b_id_buckets top:', bucketByPrefix.slice(0, 6).map(x => `${x.prefix}=${x.count}`).join(' '));
console.log('  hover new panels: live=' + (record.checks.b_hover_r2_live.new_panel_count ?? 'NF') +
  ' grave=' + (record.checks.b_hover_r2_grave.new_panel_count ?? 'NF') +
  ' positive=' + (record.checks.b_hover_r2_positive.new_panel_count ?? 'NF'));
console.log('  svg <title> present:', record.checks.b_svg_title_probe.slice(0, 3).map(t => t.hasTitle));
console.log('  toggle candidates:', toggles.length, 'toggle-changed-bg:', !!record.checks.e_toggle_success.bg_after);
console.log('  r1 default/alt MD5 identical:', record.checks.e_r1_md5_check?.identical);
