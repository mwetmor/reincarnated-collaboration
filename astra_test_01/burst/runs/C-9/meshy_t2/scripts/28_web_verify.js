// C-9 T2 step 28: drive /playtest/cliffside/?c=keeper in a real browser and
// verify the manticore shipped, without assuming anything the pack can lie about.
//
//   node 28_web_verify.js <base_url> <outdir>
//   env PLAYWRIGHT_CORE=<path to playwright-core>   CHROME_BIN=<chromium binary>
//
// WHAT IT CHECKS
//   1. the route BOOTS   -- the shell's #status overlay is removed, 0 page errors
//   2. only keeper.pck is fetched (the pre-boot character select still works)
//   3. the Keeper is the DEFAULT skin and K still cycles -- read off the HUD's own
//      words, and asserted by pixel diff: three presses must change the strip each
//      time and RETURN it to the first state, which proves the count, not just motion
//   4. the manticore CIRCLES -- position measured frame by frame, against a
//      negative control, and its speed and loop period compared with the authored
//      numbers (64.7 px/s, 14.0 s)
//   5. an UNTOUCHED pack (?c=warlord) is loaded last, so anything odd in the scene
//      can be attributed to the scene rather than to this change
//
// TWO INSTRUMENT DEFECTS FOUND WRITING THIS. Both returned a number; neither
// answered the question. They are recorded because the failure shape recurs.
//
//   (a) The first tracker searched the WHOLE FRAME for "the most-changed 50x50 box"
//       and reported a 1040x872 px path for a 217x217 px loop. It was never on the
//       creature: the HUD's fps digits repaint four times a second, the player's
//       idle animation plays at screen centre, and a fly swarm drifts through the
//       grass, so the winning box hopped between movers and the "extent" was the
//       distance between them. Fixed by measuring inside the region the scene's own
//       numbers predict AND pairing it with a same-sized control region -- if the
//       control shows a comparable path, the instrument is tracking scenery.
//
//   (b) The strip was captured with a 1 s sleep and its samples were LABELLED
//       t = 0,1,2... seconds. They are 1.574 s apart: a 1920x1080 screenshot plus
//       PNG encode under software GL costs the other 0.57 s. Read as seconds, the
//       loop closed in 9 s against an authored 14, and the creature appeared to walk
//       at 100 px/s against an authored 64.7 -- a correct build looking 35% fast.
//       The sample interval is now MEASURED from the capture timestamps, not assumed
//       from the sleep. A time base is an instrument too.
//
// WHERE THE PREDICTION COMES FROM (scenes/cliffside.tscn, nothing fitted by eye):
//   Keeper at (2285.62, 2407.32); her Camera2D offset (-2,-55) -> centre
//   (2283.62, 2352.32). Canvas 1920x1080 at zoom 1, so screen = world - centre +
//   (960,540). The octagon's node origins are world x 2410..2627.28,
//   y 2246.36..2463.64 -> screen x 1086..1304, y 434..651. The sprite is 512 px at
//   scale 0.629167 with offset (-256,-398), so it draws 161 px either side of its
//   origin and 250 px above: the cell spans screen x 925..1465, y 184..723.
const { chromium } = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');
const fs = require('fs');
const path = require('path');

const base = (process.argv[2] || '').replace(/\/$/, '');
const outdir = process.argv[3];
if (!base || !outdir) { console.error('usage: 28_web_verify.js <base_url> <outdir>'); process.exit(2); }
fs.mkdirSync(outdir, { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const ROI = { name: 'manticore', x: 915, y: 170, width: 560, height: 565 };
const CTRL = { name: 'control  ', x: 300, y: 170, width: 560, height: 565 };
const WALK_PX_S = 64.7;        // 26_cliffside_npc.py: 0.933 m/s * 69.33 px/m
const LOOP_S = 14.0;           // measured in-engine by scripts/t2_probe.gd
const N = 15, SLEEP = 1000;

async function boot(page, url) {
  await page.goto(url, { waitUntil: 'load', timeout: 120000 });
  for (let i = 0; i < 180; i++) {
    if (await page.evaluate(() => !document.getElementById('status'))) return true;
    await sleep(1000);
  }
  return false;
}

// Fraction of pixels differing by more than a small threshold. Decoded by the
// browser itself, so the harness needs no image library.
function pngDiff(page, a, b) {
  return page.evaluate(async ([pa, pb]) => {
    const load = (d) => new Promise((res) => {
      const i = new Image(); i.onload = () => res(i); i.src = 'data:image/png;base64,' + d;
    });
    const [ia, ib] = await Promise.all([load(pa), load(pb)]);
    const c = document.createElement('canvas');
    c.width = ia.width; c.height = ia.height;
    const g = c.getContext('2d', { willReadFrequently: true });
    g.drawImage(ia, 0, 0); const A = g.getImageData(0, 0, c.width, c.height).data;
    g.clearRect(0, 0, c.width, c.height);
    g.drawImage(ib, 0, 0); const B = g.getImageData(0, 0, c.width, c.height).data;
    let n = 0;
    for (let i = 0; i < A.length; i += 4) if (Math.abs(A[i] - B[i]) > 24) n++;
    return n / (A.length / 4);
  }, [a, b]);
}

// Centroid of the LARGEST connected changed region, per frame, against the
// temporal median. Largest-connected rather than all-changed: the centroid of
// every changed pixel is pulled about by contrast (this octagon's north half is
// bright dirt and its south half dark grass), which inflates the span with the
// region size instead of tracking the body.
function trackRegion(page, set) {
  return page.evaluate(async ([frames, n]) => {
    const load = (d) => new Promise((res) => {
      const i = new Image(); i.onload = () => res(i); i.src = 'data:image/png;base64,' + d;
    });
    const imgs = await Promise.all(frames.map(load));
    const w = imgs[0].width, h = imgs[0].height;
    const c = document.createElement('canvas'); c.width = w; c.height = h;
    const g = c.getContext('2d', { willReadFrequently: true });
    const grey = [];
    for (const im of imgs) {
      g.clearRect(0, 0, w, h); g.drawImage(im, 0, 0);
      const d = g.getImageData(0, 0, w, h).data;
      const a = new Float32Array(w * h);
      for (let p = 0; p < w * h; p++)
        a[p] = d[p * 4] * 0.299 + d[p * 4 + 1] * 0.587 + d[p * 4 + 2] * 0.114;
      grey.push(a);
    }
    const med = new Float32Array(w * h), col = new Array(n);
    for (let p = 0; p < w * h; p++) {
      for (let i = 0; i < n; i++) col[i] = grey[i][p];
      col.sort((a, b) => a - b);
      med[p] = col[n >> 1];
    }
    const out = [];
    for (let i = 0; i < n; i++) {
      const on = new Uint8Array(w * h);
      for (let p = 0; p < w * h; p++) on[p] = Math.abs(grey[i][p] - med[p]) > 30 ? 1 : 0;
      // iterative flood fill (a recursive one blows the stack on a 560x565 blob)
      const seen = new Uint8Array(w * h);
      let best = 0, bx = -1, by = -1;
      const stack = new Int32Array(w * h);
      for (let p0 = 0; p0 < w * h; p0++) {
        if (!on[p0] || seen[p0]) continue;
        let top = 0, cnt = 0, sx = 0, sy = 0;
        stack[top++] = p0; seen[p0] = 1;
        while (top > 0) {
          const p = stack[--top];
          const x = p % w, y = (p - x) / w;
          cnt++; sx += x; sy += y;
          if (x > 0 && on[p - 1] && !seen[p - 1]) { seen[p - 1] = 1; stack[top++] = p - 1; }
          if (x < w - 1 && on[p + 1] && !seen[p + 1]) { seen[p + 1] = 1; stack[top++] = p + 1; }
          if (y > 0 && on[p - w] && !seen[p - w]) { seen[p - w] = 1; stack[top++] = p - w; }
          if (y < h - 1 && on[p + w] && !seen[p + w]) { seen[p + w] = 1; stack[top++] = p + w; }
        }
        if (cnt > best) { best = cnt; bx = Math.round(sx / cnt); by = Math.round(sy / cnt); }
      }
      out.push({ x: bx, y: by, n: best });
    }
    return out;
  }, [set, set.length]);
}

(async () => {
  // The cached playwright build and the cached browsers can be a few revisions
  // apart, so the binary is named explicitly. SwiftShader is required: Godot's
  // gl_compatibility renderer needs WebGL2, and a headless shell with no GPU
  // otherwise draws nothing -- which reads as "the build is broken".
  const browser = await chromium.launch({
    executablePath: process.env.CHROME_BIN || undefined,
    args: ['--no-sandbox', '--use-gl=angle', '--use-angle=swiftshader',
           '--enable-unsafe-swiftshader', '--disable-gpu-sandbox'],
  });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  const errors = [], lines = [], packs = new Set();
  page.on('pageerror', (e) => errors.push(e.message));
  page.on('console', (m) => lines.push(m.type() + ': ' + m.text()));
  page.on('request', (r) => { if (r.url().endsWith('.pck')) packs.add(path.basename(r.url())); });

  // --- 1 + 2 -------------------------------------------------------------
  console.log('BOOT keeper:', await boot(page, base + '/playtest/cliffside/?c=keeper'));
  console.log('PACKS FETCHED:', JSON.stringify([...packs]));
  console.log('CHIP:', await page.evaluate(() => {
    const a = document.querySelector('#char-chip a');
    return a ? a.getAttribute('href') : 'ABSENT';
  }));
  // The chip overlays the HUD's first 150 px, so the HUD cannot be READ with it up.
  await page.addStyleTag({ content: '#char-chip{display:none !important}' });
  await sleep(4000);
  // NB: do NOT click the canvas to focus it. A click at world position casts a
  // spell, and the VFX then looks like a rendering defect in the still.
  const HUD = { x: 0, y: 0, width: 900, height: 34 };
  await page.screenshot({ path: path.join(outdir, 'still_keeper_default.png') });
  await page.screenshot({ path: path.join(outdir, 'hud_0_keeper.png'), clip: HUD });

  // --- 3: K cycles three skins and returns -------------------------------
  const shot = async () => (await page.screenshot({ clip: HUD })).toString('base64');
  const hud = [await shot()];
  for (let k = 1; k <= 3; k++) {
    await page.keyboard.press('KeyK');
    await sleep(1200);
    await page.screenshot({ path: path.join(outdir, `hud_${k}_after_K.png`), clip: HUD });
    hud.push(await shot());
  }
  for (let k = 0; k < 3; k++)
    console.log(`HUD ${k}->${k + 1} changed frac ${(await pngDiff(page, hud[k], hud[k + 1])).toFixed(4)} (want > 0.02)`);
  console.log(`HUD 0 vs 3 after a full cycle ${(await pngDiff(page, hud[0], hud[3])).toFixed(4)} (want ~0)`);

  // --- 4: does it circle, at the authored pace? --------------------------
  const grabs = [[], []], stamps = [];
  for (let i = 0; i < N; i++) {
    for (let j = 0; j < 2; j++) {
      const r = j === 0 ? ROI : CTRL;
      grabs[j].push((await page.screenshot({
        path: j === 0 ? path.join(outdir, `loop_${String(i).padStart(2, '0')}.png`) : undefined,
        clip: { x: r.x, y: r.y, width: r.width, height: r.height },
      })).toString('base64'));
    }
    stamps.push(Date.now());          // MEASURED, not assumed from the sleep
    await sleep(SLEEP);
  }
  const gaps = stamps.slice(1).map((t, i) => (t - stamps[i]) / 1000);
  const mean = gaps.reduce((a, b) => a + b, 0) / gaps.length;
  console.log(`sample interval measured ${mean.toFixed(3)} s (the harness slept ${SLEEP / 1000} s)`);

  const A = await trackRegion(page, grabs[0]);
  const B = await trackRegion(page, grabs[1]);
  const rep = (name, t) => {
    const live = t.filter((p) => p.n > 400);
    const sp = (v) => (v.length ? Math.max(...v) - Math.min(...v) : 0);
    console.log(`${name}  blob in ${live.length}/${t.length} frames  median px ` +
      `${t.map((p) => p.n).sort((a, b) => a - b)[t.length >> 1]}  ` +
      `span x ${sp(live.map((p) => p.x))} y ${sp(live.map((p) => p.y))}`);
    return live;
  };
  const live = rep(ROI.name, A);
  rep(CTRL.name, B);
  console.log('  (predicted span for the octagon: 217 px in each axis; the control must be ~0)');

  // speed between consecutive live samples, and the period from a repeat position
  const sp = [];
  for (let i = 0; i + 1 < A.length; i++) {
    if (A[i].n < 400 || A[i + 1].n < 400) continue;
    const d = Math.hypot(A[i + 1].x - A[i].x, A[i + 1].y - A[i].y);
    sp.push({ i, px: +d.toFixed(0), v: +(d / gaps[i]).toFixed(1) });
  }
  console.log('consecutive-sample speeds px/s (authored %s):', WALK_PX_S,
    JSON.stringify(sp.map((s) => s.v)));
  let period = null;
  for (let lag = 3; lag < A.length; lag++) {
    if (A[0].n < 400 || A[lag].n < 400) continue;
    if (Math.hypot(A[lag].x - A[0].x, A[lag].y - A[0].y) < 25) {
      period = (stamps[lag] - stamps[0]) / 1000; break;
    }
  }
  console.log(`loop period measured ${period === null ? 'n/a' : period.toFixed(1) + ' s'}  (in-engine probe: ${LOOP_S} s)`);

  // --- 5: an untouched pack, for attribution ------------------------------
  console.log('BOOT warlord (untouched pack):', await boot(page, base + '/playtest/cliffside/?c=warlord'));
  await page.addStyleTag({ content: '#char-chip{display:none !important}' });
  await sleep(6000);
  await page.screenshot({ path: path.join(outdir, 'still_warlord_untouched.png') });

  console.log('PAGE ERRORS', errors.length, JSON.stringify(errors.slice(0, 5)));
  const bad = lines.filter((l) => /error|ERROR|Failed|SCRIPT/.test(l));
  console.log('CONSOLE ERROR LINES', bad.length, JSON.stringify(bad.slice(0, 5)));
  fs.writeFileSync(path.join(outdir, 'console.txt'), lines.join('\n'));
  fs.writeFileSync(path.join(outdir, 'motion.json'),
    JSON.stringify({ interval_s: mean, gaps, roi: ROI, ctrl: CTRL, A, B, speeds: sp, period }, null, 1));
  await browser.close();
})().catch((e) => { console.error('HARNESS FAILED', e); process.exit(1); });
