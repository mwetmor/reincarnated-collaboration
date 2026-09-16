// Drive the Keeper along a planned 8-direction route and screenshot each leg.
// The route is a clearance-aware Dijkstra + pure-pursuit plan over
// parallax/walkable.json minus the collide=true prop footprints, simulated at the
// scene's real run_speed (494 px/s, overridden in cliffside.tscn -- the script
// default of 250 is NOT what ships). drax, web11.
// usage: PLAN='[["NE",1.3],...]' node route_walk.js <url> <outdir> <label>
const { chromium } = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');
const fs = require('fs'); const path = require('path');
const url = process.argv[2], outdir = process.argv[3], label = process.argv[4] || 'live';
const plan = JSON.parse(process.env.PLAN || '[]');
const SHOTS = Number(process.env.SHOTS || 5);
fs.mkdirSync(outdir, { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const KEYS = { N: ['KeyW'], S: ['KeyS'], E: ['KeyD'], W: ['KeyA'],
  NE: ['KeyW', 'KeyD'], NW: ['KeyW', 'KeyA'], SE: ['KeyS', 'KeyD'], SW: ['KeyS', 'KeyA'] };
(async () => {
  const browser = await chromium.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: true,
    args: ['--headless=new', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'],
  });
  const context = await browser.newContext({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  const logs = [];
  page.on('console', (m) => logs.push(`[${m.type()}] ${m.text()}`));
  page.on('pageerror', (e) => logs.push(`[pageerror] ${e.message}`));
  console.error('goto...'); await page.goto(url, { waitUntil: 'load', timeout: 180000 }); console.error('loaded');
  let booted = false;
  for (let i = 0; i < 200; i++) {
    const hidden = await page.evaluate(() => { const s = document.getElementById('status');
      return s ? getComputedStyle(s).display === 'none' || s.style.visibility === 'hidden' : true; });
    if (hidden) { booted = true; break; } await sleep(1000);
    if (i % 10 === 9) console.error('boot poll ' + i);
  }
  await sleep(6000);
  let n = 0;
  const shot = (tag) => page.screenshot({ path: path.join(outdir, `${label}_${String(++n).padStart(2, '0')}_${tag}.png`) });
  console.error('booted=' + booted + ' shooting spawn');
  await shot('spawn');
  console.error('spawn shot');
  // Hold Shift for the whole route so run_modifier never toggles mid-leg.
  await page.keyboard.down('Shift');
  for (const [dir, secs] of plan) {
    const keys = KEYS[dir];
    for (const k of keys) await page.keyboard.down(k);
    await sleep(Math.round(secs * 1000));
    for (const k of keys) await page.keyboard.up(k);
    console.error('leg ' + dir + ' ' + secs);
  }
  await page.keyboard.up('Shift');
  await sleep(600);
  for (let i = 0; i < SHOTS; i++) { await shot(`arrive_${i + 1}`); await sleep(500); }
  fs.writeFileSync(path.join(outdir, `${label}_route_console.txt`),
    [`booted=${booted}`, `plan=${JSON.stringify(plan)}`, '--- console', ...logs].join('\n'));
  console.log(`done booted=${booted}`);
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
