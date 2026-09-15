// Cast-landing burst capture for the cliffside web playtest.
// usage: node cast_capture.js <url> <outdir> <label>
const { chromium } = require(process.env.PLAYWRIGHT_CORE);
const fs = require('fs');
const path = require('path');
const [url, outdir, label] = process.argv.slice(2);
fs.mkdirSync(outdir, { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

(async () => {
  const browser = await chromium.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: true,
    args: ['--headless=new', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'],
  });
  const context = await browser.newContext({ viewport: { width: 844, height: 390 }, deviceScaleFactor: 2, hasTouch: true, isMobile: true });
  const page = await context.newPage();
  const logs = [];
  page.on('console', (m) => logs.push(`[${m.type()}] ${m.text()}`));
  page.on('pageerror', (e) => logs.push(`[pageerror] ${e.message}`));
  const t0 = Date.now();
  await page.goto(url, { waitUntil: 'load', timeout: 120000 });
  let booted = false;
  for (let i = 0; i < 180; i++) {
    const hidden = await page.evaluate(() => {
      const s = document.getElementById('status');
      return s ? getComputedStyle(s).display === 'none' || s.style.visibility === 'hidden' : true;
    });
    if (hidden) { booted = true; break; }
    await sleep(1000);
  }
  const bootMs = Date.now() - t0;
  await sleep(5000);
  const cdp = await context.newCDPSession(page);
  const dir = process.env.DIR || 'W';
  const dx = dir === 'W' ? -1 : 1;
  // Short joystick nudge (walk, not run) to set facing.
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: 250, y: 280, id: 1 }] });
  for (let k = 1; k <= 5; k++) { await cdp.send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: 250 + dx * k * 8, y: 280, id: 1 }] }); await sleep(30); }
  await sleep(Number(process.env.WALK_MS || 600));
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
  await sleep(400);
  await page.screenshot({ path: path.join(outdir, `${label}_00_before_cast.png`) });
  // Stream every rendered frame (screencast) so the 0.1 s flash / 0.35 s floor light is not missed.
  const frames = [];
  if (process.env.RAF) {
    // Per-animation-frame copy of a device-px region of the Godot canvas (RAF="sx,sy,w,h"), registered after
    // Godot's own rAF loop so the drawing buffer is still intact when copied.
    const [sx, sy, w, h] = process.env.RAF.split(',').map(Number);
    await page.evaluate(([sx, sy, w, h]) => {
      const gl = document.getElementById('canvas');
      window.__cap = { on: false, frames: [], size: [gl.width, gl.height] };
      const loop = (t) => {
        if (window.__cap.on && window.__cap.frames.length < 90) {
          const c = document.createElement('canvas'); c.width = w; c.height = h;
          c.getContext('2d').drawImage(gl, sx, sy, w, h, 0, 0, w, h);
          window.__cap.frames.push([t, c]);
        }
        requestAnimationFrame(loop);
      };
      requestAnimationFrame(loop);
    }, [sx, sy, w, h]);
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: 700, y: 314, id: 2 }] });
    await sleep(120);
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
    await sleep(Number(process.env.CLIP_DELAY || 600));
    await page.evaluate(() => { window.__cap.on = true; });
    await sleep(Number(process.env.CAPTURE_MS || 1200));
    const out = await page.evaluate(() => {
      window.__cap.on = false;
      const f = window.__cap.frames;
      return { size: window.__cap.size, frames: f.map(([t, c]) => [Math.round(t - f[0][0]), c.toDataURL('image/png')]) };
    });
    const st = [`canvas=${out.size.join('x')} region=${process.env.RAF}`];
    out.frames.forEach(([t, d], i) => {
      const f = path.join(outdir, `${label}_raf_${String(i).padStart(2, '0')}.png`);
      fs.writeFileSync(f, Buffer.from(d.split(',')[1], 'base64'));
      st.push(`${path.basename(f)} +${t}ms`);
    });
    await page.screenshot({ path: path.join(outdir, `${label}_after_full.png`) });
    fs.writeFileSync(path.join(outdir, `${label}_raf_console.txt`), [`url=${url}`, `booted=${booted} boot_ms=${bootMs}`, ...st, '--- console', ...logs].join('\n'));
    console.log(`booted=${booted} boot_ms=${bootMs}`); console.log(st.join('\n'));
    await browser.close();
    return;
  }
  if (process.env.CLIP) {
    // Hi-res clip burst around the landing point (CLIP="x,y,w,h" in CSS px), starting CLIP_DELAY ms after the tap.
    const [cx, cy, cw, ch] = process.env.CLIP.split(',').map(Number);
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: 700, y: 314, id: 2 }] });
    await sleep(120);
    await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
    const t1 = Date.now();
    await sleep(Number(process.env.CLIP_DELAY || 700));
    const st = [];
    for (let i = 0; Date.now() - t1 < Number(process.env.CAPTURE_MS || 1600); i++) {
      const f = path.join(outdir, `${label}_clip_${String(i).padStart(2, '0')}.png`);
      const ts = Date.now() - t1;
      await page.screenshot({ path: f, clip: { x: cx, y: cy, width: cw, height: ch } });
      st.push(`${path.basename(f)} +${ts}ms`);
    }
    await page.screenshot({ path: path.join(outdir, `${label}_after_full.png`) });
    fs.writeFileSync(path.join(outdir, `${label}_clip_console.txt`), [`url=${url}`, `booted=${booted} boot_ms=${bootMs}`, `clip=${process.env.CLIP}`, ...st, '--- console', ...logs].join('\n'));
    console.log(`booted=${booted} boot_ms=${bootMs}`); console.log(st.join('\n'));
    await browser.close();
    return;
  }
  cdp.on('Page.screencastFrame', async (ev) => {
    frames.push({ t: Date.now(), data: ev.data });
    try { await cdp.send('Page.screencastFrameAck', { sessionId: ev.sessionId }); } catch (e) {}
  });
  await cdp.send('Page.startScreencast', { format: 'png', everyNthFrame: 1, maxWidth: 1688, maxHeight: 780 });
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: 700, y: 314, id: 2 }] });
  await sleep(120);
  await cdp.send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
  const tc = Date.now();
  await sleep(Number(process.env.CAPTURE_MS || 3000));
  await cdp.send('Page.stopScreencast');
  const stamps = [];
  frames.forEach((fr, i) => {
    const f = path.join(outdir, `${label}_frame_${String(i).padStart(3, '0')}.png`);
    fs.writeFileSync(f, Buffer.from(fr.data, 'base64'));
    stamps.push(`${path.basename(f)} +${fr.t - tc}ms`);
  });
  fs.writeFileSync(path.join(outdir, `${label}_console.txt`), [`url=${url}`, `booted=${booted} boot_ms=${bootMs}`, ...stamps, '--- console', ...logs].join('\n'));
  console.log(`booted=${booted} boot_ms=${bootMs}`);
  console.log(stamps.join('\n'));
  console.log(logs.filter((l) => /error|fail/i.test(l)).slice(0, 20).join('\n'));
  await browser.close();
})().catch((e) => { console.error('TEST_FAILED', e); process.exit(1); });
