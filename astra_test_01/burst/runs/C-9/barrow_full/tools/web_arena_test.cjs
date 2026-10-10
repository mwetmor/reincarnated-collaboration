// Packaged browser smoke test: startup, integrity gates, rendering, and inputs.
// PLAYWRIGHT_CORE=<installed module> node web_arena_test.cjs <url> <outdir> [--touch|--fail-pack]
const fs = require('fs');
const path = require('path');
let playwright;
try { playwright = require(process.env.PLAYWRIGHT_CORE || 'playwright-core'); }
catch (error) {
  if (process.env.PLAYWRIGHT_CORE) throw error;
  playwright = require(path.join(process.env.HOME, '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright-core'));
}
const { chromium } = playwright;
const [url, outdir, mode = 'desktop'] = process.argv.slice(2);
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
fs.mkdirSync(outdir, { recursive: true });

(async () => {
  const browser = await chromium.launch({
    executablePath: process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: false,
    args: ['--use-angle=metal', '--ignore-gpu-blocklist', '--disable-background-timer-throttling', '--disable-renderer-backgrounding'],
  });
  const touch = mode === '--touch';
  const page = await browser.newPage({ viewport: touch ? { width: 844, height: 390 } : { width: 1280, height: 720 }, hasTouch: touch, deviceScaleFactor: 1 });
  if (process.env.VERCEL_OIDC_TOKEN) {
    const origin = new URL(url).origin;
    await page.route(u => u.origin === origin, route => route.continue({headers:{...route.request().headers(), 'x-vercel-trusted-oidc-idp-token':process.env.VERCEL_OIDC_TOKEN}}));
  }
  const started = Date.now();
  const logs = [], responses = [], failures = [], inputs = [];
  let launch = '', ready = false, packFailure = false;
  const persist = () => fs.writeFileSync(path.join(outdir, 'result.json'), JSON.stringify({ mode, elapsed_ms: Date.now() - started, launch, ready, packFailure, logs, responses, failures, inputs }, null, 2));
  page.on('console', msg => {
    const text = msg.text();
    logs.push({ ms: Date.now() - started, type: msg.type(), text });
    if (text.startsWith('[arena] launch:')) launch = text;
    if (/\[bv2f_arena\] site .*arena up/.test(text)) ready = true;
    if (/bv2f_arena: pack failed/.test(text)) packFailure = true;
    if (/ERROR|REFUSED|\[bv2f_arena\] pack:|\[arena\] launch:|\[bv2f_arena\] site|\[arena\] input:/.test(text)) console.log(text.slice(0,2000));
    persist();
  });
  page.on('pageerror', error => { failures.push(error.message); persist(); });
  page.on('response', r => { responses.push({ url: r.url(), status: r.status() }); });
  if (mode === '--fail-pack') await page.route('**/site_0.pck', r => r.fulfill({status:404,body:'missing test pack'}));
  try {
    const testUrl = new URL(url); testUrl.searchParams.set('probe', '1');
    await page.goto(testUrl.toString(), { waitUntil: 'domcontentloaded', timeout: 120000 });
    await page.bringToFront();
    while (!(ready && launch) && !packFailure && !logs.some(x => /REFUSED|SCRIPT ERROR/.test(x.text)) && Date.now() - started < 240000) await sleep(250);
    if (mode === '--fail-pack') {
      if (!packFailure || ready) throw new Error('Missing pack did not stop arena startup');
      await page.screenshot({path:path.join(outdir,'download-failure.png')});
      console.log('PASS: missing pack stops startup');
      return;
    }
    if (!ready || !/bundled true, web true/.test(launch) || !/G6C-LEECH-JOIN:PASS/.test(launch)) throw new Error('Arena did not open with verified web bundle');
    if (!logs.some(x => /^\[arena\] enemy vfx: \d+ sets, \d+ pages$/.test(x.text))) throw new Error('Enemy effect atlas did not load');
    if (/solver native/.test(launch)) throw new Error('Web unexpectedly selected native solver');
    await page.waitForFunction(() => !document.getElementById('warm-veil'), {timeout:120000});
    await page.locator('canvas').focus();
    await sleep(500);
    const observe = async label => {
      const state = await page.evaluate(() => window.__barrowProbe);
      if (!state) throw new Error('Input probe unavailable');
      inputs.push({label,...state});
      return state;
    };
    const before = await observe('before');
    if (before.exploration_touch) throw new Error('Exploration controls overlap arena controls');
    const cdp = await page.context().newCDPSession(page);
    if (touch) {
      await cdp.send('Input.dispatchTouchEvent', {type:'touchStart',touchPoints:[{x:320,y:210,id:1}]});
      await sleep(1500);
      await observe('moving');
      await cdp.send('Input.dispatchTouchEvent', {type:'touchEnd',touchPoints:[]});
      // Buttons use the 1920x1080 canvas, scaled/letterboxed into 844x390.
      const scale = 390 / 1080, padX = (844 - 1920 * scale) / 2;
      const at = (x,y) => ({x:padX + x*scale,y:y*scale,id:2});
      await cdp.send('Input.dispatchTouchEvent', {type:'touchStart',touchPoints:[at(1782,907.5)]});
      await sleep(2000);
      const held = await observe('channel-held');
      if (!held.channel || !held.touch || !held.fight_started) throw new Error('Touch did not start combat/channel');
      await cdp.send('Input.dispatchTouchEvent', {type:'touchEnd',touchPoints:[]});
      await cdp.send('Input.dispatchTouchEvent', {type:'touchStart',touchPoints:[at(1851,539.5)]});
      await sleep(100);
      await cdp.send('Input.dispatchTouchEvent', {type:'touchEnd',touchPoints:[]});
    } else {
      await page.keyboard.press('Space');
      await sleep(500);
      await page.mouse.move(740,370);
      await page.mouse.down(); await sleep(1500); await observe('moving'); await page.mouse.up();
      await page.mouse.down({button:'right'}); await sleep(2000);
      const held = await observe('channel-held');
      if (!held.channel || held.touch || !held.fight_started) throw new Error('Mouse did not start combat/channel');
      await page.mouse.up({button:'right'});
      await page.keyboard.press('z');
      await page.keyboard.press('3');
    }
    await sleep(2500);
    const after = await observe('after');
    if (after.channel || after.zoomed_out === before.zoomed_out) throw new Error('Channel release or zoom input failed');
    if (!inputs.some(x => x.label === 'moving' && JSON.stringify(x.position) !== JSON.stringify(before.position))) throw new Error('Player did not move');
    await page.screenshot({path:path.join(outdir,'playing.png')});
    // Same non-fatal decoder warning exists in the pinned native runtime's launch.log.
    // Keep it in result.json; do not change sealed runtime bytes to silence it.
    const knownWarning = 'Unicode parsing error, some characters were replaced with � (U+FFFD): Unexpected NUL character';
    const errors = logs.filter(x => (x.type === 'error' && x.text !== knownWarning) || /SCRIPT ERROR|REFUSED/.test(x.text));
    console.log('Known runtime NUL warnings: ' + logs.filter(x => x.text === knownWarning).length);
    if (errors.length || failures.length) throw new Error('Browser errors: ' + JSON.stringify({errors,failures}));
    console.log('PASS: verified bundle, arena rendered, ' + (touch ? 'touch' : 'mouse/keyboard') + ' inputs dispatched');
  } catch (error) {
    await page.screenshot({path:path.join(outdir,'failed.png')}).catch(() => {});
    throw error;
  } finally {
    persist();
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
