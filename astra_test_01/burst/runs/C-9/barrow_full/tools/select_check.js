// C-9 R-C9-117 -- THE SELECT PAGE, checked in Chrome at phone size: it renders (a screenshot), every card's toggles
// build the URL they claim (the navigation is caught, not followed), an old ?c= link goes straight to play.html.
//   PLAYWRIGHT_CORE=<playwright-core> node select_check.js <base url ending /playtest/barrow-painted/> <outdir>
const { chromium } = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');
const fs = require('fs'); const path = require('path');
const base = process.argv[2]; const out = process.argv[3]; fs.mkdirSync(out, { recursive: true });
(async () => {
  const browser = await chromium.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: true });
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3, hasTouch: true, isMobile: true });
  const page = await ctx.newPage();
  const errors = []; page.on('pageerror', (e) => errors.push(e.message));
  await page.route('**/play.html*', (r) => r.fulfill({ status: 200, contentType: 'text/html', body: '<p>play</p>' }));
  const cases = [
    ['barbarian', {}, 'c=barbarian&hold=t1211'],
    ['barbarian', { b_hold: 'f25l' }, 'c=barbarian&hold=f25l'],
    ['barbarian', { b_hold: 'f40l' }, 'c=barbarian&hold=f40l'],
    ['barbarian', { b_armor: 'gladc' }, 'c=barbarian&armor=gladc'],
    ['barbarian', { b_armor: 'gladb' }, 'c=barbarian&armor=gladb'],
    ['sorceress', {}, 'c=sorceress'],
    ['sorceress', { s_armor: 'bmc', s_meteor: 'mix3' }, 'c=sorceress&armor=bmc&meteor=mix3'],
    ['sorceress', { s_armor: 'bmd', s_fb: 'full', s_fall: '2.4' }, 'c=sorceress&armor=bmd&fb=full&fall=2.4'],
    ['sorceress', { s_v5: 'ab' }, 'c=sorceress&v5=ab'],
    ['sorceress', { s_v5: 'b' }, 'c=sorceress&v5=b'],
    ['warlord', {}, 'c=warlord'],
    ['warlord', { w_eye: 'ice' }, 'c=warlord&eye=ice'],
  ];
  const rows = [];
  let first = true;
  for (const [c, picks, want] of cases) {
    await page.goto(base, { waitUntil: 'load' });
    if (first) { await page.screenshot({ path: path.join(out, 'select_phone.png'), fullPage: true }); first = false; }
    for (const [name, v] of Object.entries(picks)) {
      for (const one of (name === 's_v5' ? v.split('') : [v])) await page.check(`input[name="${name}"][value="${one}"]`);
    }
    await Promise.all([page.waitForURL('**/play.html*'), page.click(`[data-c="${c}"] .go`)]);
    const got = new URL(page.url()).search.slice(1);
    rows.push({ card: c, picks, want, got, ok: got === want });
  }
  await page.goto(base + '?c=sorceress&fb=c75', { waitUntil: 'load' });
  await page.waitForURL('**/play.html*');
  rows.push({ old_link: '?c=sorceress&fb=c75', got: page.url(), ok: page.url().endsWith('play.html?c=sorceress&fb=c75') });
  fs.writeFileSync(path.join(out, 'select_check.json'), JSON.stringify({ rows, errors }, null, 1));
  console.log(JSON.stringify({ ok: rows.every((r) => r.ok) && errors.length === 0, n: rows.length, errors }));
  await browser.close();
})();
