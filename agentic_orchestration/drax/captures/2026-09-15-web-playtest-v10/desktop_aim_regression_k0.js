// Regression guard on F-C5-5: desktop (non-touch) mouse aim must be UNCHANGED.
// Discriminator: face EAST, park the mouse WEST of the Keeper, cast.
// mouse aim intact -> burst lands WEST (at the cursor, behind the Keeper).
// forward-along-facing leaking to desktop -> burst would land EAST. drax, web10.
const { chromium } = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');
const fs = require('fs'); const path = require('path');
const url = process.argv[2], outdir = process.argv[3], label = process.argv[4] || 'desk';
fs.mkdirSync(outdir, { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
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
  await page.goto(url, { waitUntil: 'load', timeout: 180000 });
  for (let i = 0; i < 200; i++) {
    const hidden = await page.evaluate(() => { const s = document.getElementById('status');
      return s ? getComputedStyle(s).display === 'none' || s.style.visibility === 'hidden' : true; });
    if (hidden) break; await sleep(1000);
  }
  await sleep(6000);
  const touchFlags = await page.evaluate(() => ({ maxTouchPoints: navigator.maxTouchPoints, ontouchstart: 'ontouchstart' in window }));
  // kit 0 (frozen_orb): slow, and cyan is rare on this terrain -> clean signal
  // Face east briefly.
  await page.keyboard.down('KeyD'); await sleep(500); await page.keyboard.up('KeyD'); await sleep(400);
  // Park the real mouse WEST of the Keeper (Keeper sits at viewport centre 640,360).
  await page.mouse.move(200, 200); await sleep(500);
  await page.screenshot({ path: path.join(outdir, `${label}_20_pre.png`) });
  for (let shot = 0; shot < 8; shot++) {
    await page.keyboard.down('KeyE');
    for (let i = 0; i < 8; i++) await page.screenshot({ path: path.join(outdir, `${label}_21_cast_s${shot}f${i}.png`) });
    await page.keyboard.up('KeyE');
    await sleep(1200);
  }
  fs.writeFileSync(path.join(outdir, `${label}_console.txt`), [`touchflags=${JSON.stringify(touchFlags)}`, ...logs].join('\n'));
  console.log(`done touchflags=${JSON.stringify(touchFlags)}`);
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
