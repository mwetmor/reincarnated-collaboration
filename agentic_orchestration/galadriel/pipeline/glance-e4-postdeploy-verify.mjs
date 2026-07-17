// Galadriel POST-DEPLOY verification — Glance production (E4 cutover, HEAD 5bd368bd).
// URL: https://reincarnated-glance.vercel.app/#/atlas
// Verify:
//   a. E4 marker present ("Edition IV" / "Build Horizon — Edition IV")
//   b. Interactive tooltips: hover kit dots → panel shows folk_name + game; sample live / graveyard / positive
//   c. Candidate-islands layer VISIBLE (dashed islet outlines + "CANDIDATE FAMILIES" legend)
//   d. No console errors
//   e. Theme toggle both skins if present
//   f. Full-page screenshot at ≥1600 wide
import { chromium } from 'playwright';
import { mkdirSync, writeFileSync } from 'node:fs';

const URL = 'https://reincarnated-glance.vercel.app/';
const OUT = '/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-17-glance-e4-postdeploy';
mkdirSync(OUT, { recursive: true });

const record = {
  url: URL,
  captured_at: new Date().toISOString(),
  viewport: null,
  console: { errors: [], warnings: [], reqfails: [] },
  checks: {},
};

const browser = await chromium.launch();
const vp = { width: 1680, height: 1050 };
record.viewport = vp;
const ctx = await browser.newContext({ viewport: vp, deviceScaleFactor: 1 });
const page = await ctx.newPage();

page.on('console', m => {
  const t = m.type();
  if (t === 'error') record.console.errors.push(m.text());
  else if (t === 'warning') record.console.warnings.push(m.text());
});
page.on('requestfailed', r => record.console.reqfails.push(`${r.url()} ${(r.failure()?.errorText || '')}`));
page.on('response', r => {
  const st = r.status();
  if (st >= 400) record.console.reqfails.push(`HTTP ${st} ${r.url()}`);
});

// Route to /#/atlas
await page.goto(URL, { waitUntil: 'domcontentloaded' });
await page.evaluate(() => { window.location.hash = '#/atlas'; });
await page.waitForLoadState('networkidle').catch(() => {});
await page.waitForTimeout(2500);

// Auth-wall guard
const authWall = await page.evaluate(() => {
  const t = (document.body.innerText || '').toLowerCase();
  return /log in to vercel|authentication required|sign in to vercel|vercel authentication/.test(t);
});
if (authWall) {
  record.checks.auth_wall = 'FAIL';
  writeFileSync(`${OUT}/verify-record.json`, JSON.stringify(record, null, 2));
  await browser.close();
  process.exit(1);
}

// ---- (a) E4 marker ----
const editionProbe = await page.evaluate(() => {
  const t = document.body.innerText || '';
  const e4 = /edition\s*IV|Build Horizon\W*Edition\s*IV/i.test(t);
  const e3 = /edition\s*III(?![VvI])/i.test(t);
  // Find nearest heading node matching Build Horizon
  const heads = [...document.querySelectorAll('h1,h2,h3,[role="heading"]')]
    .map(h => (h.textContent || '').trim())
    .filter(s => /build\s+horizon/i.test(s));
  return { e4, e3, headlines: heads.slice(0, 6), textSample: t.slice(0, 400) };
});
record.checks.a_edition_marker = {
  status: editionProbe.e4 && !editionProbe.e3 ? 'PASS' : (editionProbe.e4 && editionProbe.e3 ? 'MIXED' : 'FAIL'),
  e4_found: editionProbe.e4,
  e3_found: editionProbe.e3,
  headlines: editionProbe.headlines,
};

// ---- (c) Candidate-islands layer ----
const islandsProbe = await page.evaluate(() => {
  // Look for dashed islet outlines and CANDIDATE FAMILIES legend.
  const dashedEls = [...document.querySelectorAll('path,ellipse,polygon,rect,circle')]
    .filter(el => {
      const sd = el.getAttribute('stroke-dasharray') || el.style.strokeDasharray || '';
      return sd && sd !== 'none' && sd.trim() !== '';
    });
  const dashedCount = dashedEls.length;
  const bodyText = document.body.innerText || '';
  const legend = /candidate\s+families/i.test(bodyText);
  // Try common class hooks
  const candidateIslets = document.querySelectorAll('[class*="candidate"],[class*="islet"],[class*="island"]').length;
  const svgs = [...document.querySelectorAll('svg')].map(s => ({
    id: s.id || null,
    cls: s.getAttribute('class') || null,
    childCount: s.childElementCount,
  })).slice(0, 8);
  return { dashedCount, legend, candidateIslets, svgs, legendSnippet: (bodyText.match(/candidate\s+families[^\n]{0,120}/i) || [null])[0] };
});
record.checks.c_candidate_islands = {
  status: (islandsProbe.dashedCount > 0 && islandsProbe.legend) ? 'PASS' : 'FAIL',
  dashed_element_count: islandsProbe.dashedCount,
  legend_present: islandsProbe.legend,
  legend_snippet: islandsProbe.legendSnippet,
  candidate_class_hits: islandsProbe.candidateIslets,
  svgs: islandsProbe.svgs,
};

// ---- Full-page screenshot (default skin) ----
page.setDefaultTimeout(90000);
let fullOK = false;
try {
  await page.screenshot({ path: `${OUT}/atlas-fullpage-default-1680.png`, fullPage: true, timeout: 90000 });
  fullOK = true;
} catch (e) {
  record.checks.fullpage_default_err = String(e).slice(0, 200);
}
await page.screenshot({ path: `${OUT}/atlas-viewport-default-1680.png`, timeout: 60000 });
record.checks.f_fullpage_shot = { status: fullOK ? 'PASS' : 'PARTIAL', path: fullOK ? 'atlas-fullpage-default-1680.png' : 'atlas-viewport-default-1680.png' };

// ---- (e) Theme/skin toggle detection ----
const themeProbe = await page.evaluate(() => {
  // Look for buttons with theme-ish labels or aria attrs
  const btns = [...document.querySelectorAll('button,[role="button"],a')];
  const cand = btns
    .filter(el => {
      const s = ((el.textContent || '') + ' ' + (el.getAttribute('aria-label') || '') + ' ' + (el.title || '')).toLowerCase();
      return /(theme|skin|dark|light|instrument|archive|toggle)/.test(s);
    })
    .map(el => {
      const b = el.getBoundingClientRect();
      return {
        text: (el.textContent || '').trim().slice(0, 40),
        aria: el.getAttribute('aria-label') || null,
        title: el.title || null,
        x: Math.round(b.left), y: Math.round(b.top), w: Math.round(b.width), h: Math.round(b.height),
      };
    })
    .slice(0, 6);
  return { candidates: cand };
});
record.checks.e_theme_toggle = { status: 'INFO', candidates: themeProbe.candidates };

if (themeProbe.candidates.length > 0) {
  try {
    const first = themeProbe.candidates[0];
    // Click the first plausible toggle
    await page.evaluate((sel) => {
      const btns = [...document.querySelectorAll('button,[role="button"],a')];
      const target = btns.find(el => {
        const s = ((el.textContent || '') + ' ' + (el.getAttribute('aria-label') || '') + ' ' + (el.title || '')).toLowerCase();
        return /(theme|skin|dark|light|instrument|archive|toggle)/.test(s);
      });
      if (target) target.click();
    }, first);
    await page.waitForTimeout(1200);
    try { await page.screenshot({ path: `${OUT}/atlas-fullpage-alt-1680.png`, fullPage: true, timeout: 90000 }); }
    catch (e) { record.checks.fullpage_alt_err = String(e).slice(0, 200); }
    await page.screenshot({ path: `${OUT}/atlas-viewport-alt-1680.png`, timeout: 60000 });
    record.checks.e_theme_toggle = {
      status: 'PASS',
      toggled: true,
      first_candidate: first,
      alt_screenshot: 'atlas-fullpage-alt-1680.png',
    };
    // Toggle back
    await page.evaluate(() => {
      const btns = [...document.querySelectorAll('button,[role="button"],a')];
      const target = btns.find(el => {
        const s = ((el.textContent || '') + ' ' + (el.getAttribute('aria-label') || '') + ' ' + (el.title || '')).toLowerCase();
        return /(theme|skin|dark|light|instrument|archive|toggle)/.test(s);
      });
      if (target) target.click();
    });
    await page.waitForTimeout(600);
  } catch (e) {
    record.checks.e_theme_toggle.error = String(e);
  }
} else {
  record.checks.e_theme_toggle = { status: 'NO-TOGGLE-FOUND', note: 'Captured default only.' };
}

// ---- (b) Interactive tooltips: hover kit dots ----
// Discover kit-dot candidates: elements with kit_id-ish attrs or data hooks
const kitDots = await page.evaluate(() => {
  // Search for elements with data-kit-id or class containing 'kit' or aria-labels that look like folk names
  const candidates = [];
  const all = document.querySelectorAll('circle,rect,g,path,[data-kit-id],[data-kit],[data-id]');
  for (const el of all) {
    const id = el.getAttribute('data-kit-id') || el.getAttribute('data-kit') || el.getAttribute('data-id');
    const aria = el.getAttribute('aria-label');
    const cls = el.getAttribute('class') || '';
    if (id || (aria && aria.length > 2 && aria.length < 120) || /kit|dot|glyph/i.test(cls)) {
      const b = el.getBoundingClientRect();
      if (b.width > 0 && b.width < 40 && b.height > 0 && b.height < 40) {
        candidates.push({
          tag: el.tagName.toLowerCase(),
          id: id || null,
          aria: aria || null,
          cls: cls.slice(0, 80),
          x: Math.round(b.left + b.width / 2),
          y: Math.round(b.top + b.height / 2),
          w: Math.round(b.width),
          h: Math.round(b.height),
          classHints: {
            live: /live/i.test(cls),
            graveyard: /graveyard|tomb|tombstone|dead/i.test(cls),
            positive: /positive|new|admit|path-a/i.test(cls),
          },
        });
      }
    }
  }
  return candidates.slice(0, 800);
});
record.checks.b_kit_dot_discovery = { total_candidates: kitDots.length, sample: kitDots.slice(0, 8) };

// Bucket by class hints; also fall back to first-N by DOM order
const liveCand = kitDots.find(k => k.classHints.live) || kitDots[0];
const graveCand = kitDots.find(k => k.classHints.graveyard) || kitDots[Math.floor(kitDots.length * 0.5)];
const posCand = kitDots.find(k => k.classHints.positive) || kitDots[kitDots.length - 1];

const hoverProbe = async (cand, label) => {
  if (!cand) return { status: 'NOT-FOUND', label };
  await page.mouse.move(cand.x, cand.y);
  await page.waitForTimeout(700);
  const panel = await page.evaluate(() => {
    // Detect visible tooltip/panel: fixed/absolute, sized card-like, with body text
    const all = [...document.querySelectorAll('*')];
    const cards = all.filter(el => {
      const cs = getComputedStyle(el);
      const b = el.getBoundingClientRect();
      return (cs.position === 'fixed' || cs.position === 'absolute')
        && b.width > 80 && b.width < 700
        && b.height > 24 && b.height < 600
        && (el.textContent || '').trim().length > 5
        && cs.visibility !== 'hidden' && cs.opacity !== '0' && cs.display !== 'none';
    }).map(el => ({
      text: (el.textContent || '').trim().slice(0, 400),
      x: Math.round(el.getBoundingClientRect().left),
      y: Math.round(el.getBoundingClientRect().top),
      w: Math.round(el.getBoundingClientRect().width),
      h: Math.round(el.getBoundingClientRect().height),
    }));
    return cards.slice(0, 6);
  });
  // Screenshot the hover state focused on the cand region
  const clip = {
    x: Math.max(0, cand.x - 300),
    y: Math.max(0, cand.y - 200),
    width: Math.min(vp.width - Math.max(0, cand.x - 300), 700),
    height: Math.min(vp.height - Math.max(0, cand.y - 200), 500),
  };
  const shot = `${OUT}/hover-${label}.png`;
  await page.screenshot({ path: shot, clip });
  // Heuristic: does the panel text look like folk_name + game (Title Case fragment + " / " or " — " or " • " with second fragment)?
  const looksJoined = panel.some(p => /[A-Z][a-z]+.{0,40}(\/|—|•|·|,)\s*[A-Z0-9]/.test(p.text));
  return {
    label,
    hovered_at: { x: cand.x, y: cand.y },
    candidate: cand,
    panels: panel,
    tooltip_visible: panel.length > 0,
    join_heuristic: looksJoined,
    screenshot: `hover-${label}.png`,
  };
};

record.checks.b_hover_live = await hoverProbe(liveCand, 'live');
record.checks.b_hover_graveyard = await hoverProbe(graveCand, 'graveyard');
record.checks.b_hover_positive = await hoverProbe(posCand, 'positive');

const bJoinPassCount =
  (record.checks.b_hover_live.tooltip_visible ? 1 : 0) +
  (record.checks.b_hover_graveyard.tooltip_visible ? 1 : 0) +
  (record.checks.b_hover_positive.tooltip_visible ? 1 : 0);
record.checks.b_hover_summary = {
  status: bJoinPassCount >= 2 ? 'PASS' : (bJoinPassCount === 1 ? 'PARTIAL' : 'FAIL'),
  tooltips_visible_count: bJoinPassCount,
};

// ---- (d) Console errors ----
record.checks.d_console_errors = {
  status: record.console.errors.length === 0 ? 'PASS' : 'FAIL',
  error_count: record.console.errors.length,
  errors: record.console.errors.slice(0, 20),
  reqfail_count: record.console.reqfails.length,
  reqfails: record.console.reqfails.slice(0, 20),
  warning_count: record.console.warnings.length,
};

writeFileSync(`${OUT}/verify-record.json`, JSON.stringify(record, null, 2));
await browser.close();
console.log('DONE. verify-record.json written.');
console.log('Edition marker:', record.checks.a_edition_marker.status);
console.log('Islands layer:', record.checks.c_candidate_islands.status);
console.log('Hover tooltips:', record.checks.b_hover_summary.status, `(${record.checks.b_hover_summary.tooltips_visible_count}/3)`);
console.log('Console errors:', record.checks.d_console_errors.status, `(${record.checks.d_console_errors.error_count} errors)`);
console.log('Theme toggle:', record.checks.e_theme_toggle.status);
