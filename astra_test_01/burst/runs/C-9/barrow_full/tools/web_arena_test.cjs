// Packaged browser smoke test: startup, integrity gates, rendering, and inputs.
// node web_arena_test.cjs <url> <outdir> [desktop|--touch|--fail-pack|--perf|--perf-touch|--touch-long]
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
  const touch = ['--touch', '--perf-touch', '--touch-long'].includes(mode);
  const perf = mode === '--perf' || mode === '--perf-touch';
  const origin = new URL(url).origin;
  // Context headers also cover AudioWorklet module fetches, which page.route misses.
  // The authenticated context is restricted to this deployment's origin.
  const context = await browser.newContext({
    viewport: touch ? { width: 844, height: 390 } : { width: 1280, height: 720 },
    hasTouch: touch, deviceScaleFactor: Number(process.env.ARENA_DEVICE_SCALE || (['--perf-touch','--touch-long'].includes(mode) ? 3 : 1)),
    extraHTTPHeaders: process.env.VERCEL_OIDC_TOKEN ? {'x-vercel-trusted-oidc-idp-token':process.env.VERCEL_OIDC_TOKEN} : {},
  });
  if (process.env.VERCEL_OIDC_TOKEN) await context.route(u => u.origin !== origin, route => route.abort());
  // Observe actual WebAudio samples reaching the destination. Cue counters
  // alone can pass while browser autoplay or the output graph is silent.
  await context.addInitScript(() => {
    const contexts = [], analysers = [];
    window.__arenaAudioOutput = {contexts, analysers, peak:0, samples:0, nonzero:0};
    const connect = AudioNode.prototype.connect;
    AudioNode.prototype.connect = function(destination, output = 0, input = 0) {
      if (destination instanceof AudioDestinationNode) {
        const analyser = this.context.createAnalyser(); analyser.fftSize = 1024;
        connect.call(this, analyser, output, 0); connect.call(analyser, destination, 0, input);
        analysers.push(analyser); return destination;
      }
      return connect.apply(this, arguments);
    };
    for (const name of ['AudioContext', 'webkitAudioContext']) {
      const Original = window[name];
      if (Original) window[name] = new Proxy(Original, {construct(target, args) {
        const ctx = Reflect.construct(target, args); contexts.push(ctx); return ctx;
      }});
    }
    const buffer = new Float32Array(1024);
    setInterval(() => {
      const report = window.__arenaAudioOutput;
      for (const analyser of analysers) {
        analyser.getFloatTimeDomainData(buffer);
        let peak = 0; for (const value of buffer) peak = Math.max(peak, Math.abs(value));
        report.peak = Math.max(report.peak, peak); report.samples++;
        if (peak > 0.00001) report.nonzero++;
      }
    }, 50);
  });
  if (process.env.VERCEL_CLI_PATH && process.env.VERCEL_OIDC_TOKEN) {
    // AudioWorklet fetches do not inherit CDP custom headers. Obtain a normal
    // same-origin bypass session with the authenticated CLI; keep cookies in memory.
    const { spawnSync } = require('child_process');
    const session = spawnSync(process.env.VERCEL_CLI_PATH, [
      'curl', '/playtest/barrow-arena/?x-vercel-set-bypass-cookie=true',
      '--deployment', origin, '--', '--silent', '--dump-header', '-', '--output', '/dev/null',
    ], {encoding:'utf8', env:{...process.env,VERCEL_CLI_USE_NATIVE_BINARY:'0'}, maxBuffer:1024*1024});
    if (session.status !== 0) { await browser.close(); throw new Error('Vercel preview cookie bootstrap failed'); }
    const cookies = [...session.stdout.matchAll(/^set-cookie:\s*([^=;]+)=([^;\r\n]+)/gmi)]
      .map(m => ({name:m[1],value:m[2],url:origin,secure:true,httpOnly:true,sameSite:'Lax'}));
    if (!cookies.length) { await browser.close(); throw new Error('Vercel preview did not issue a bypass session cookie'); }
    await context.addCookies(cookies);
  }
  const page = await context.newPage();
  const started = Date.now();
  const logs = [], responses = [], failures = [], inputs = [];
  let launch = '', ready = false, packFailure = false, frameTimes = [];
  const persist = () => fs.writeFileSync(path.join(outdir, 'result.json'), JSON.stringify({ mode, elapsed_ms: Date.now() - started, launch, ready, packFailure, logs, responses, failures, inputs, frameTimes }, null, 2));
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
    if (perf) testUrl.searchParams.set('perf', '1');
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
    const audioOutput = () => page.evaluate(() => {
      const p = window.__arenaAudioOutput;
      return {peak:p.peak,samples:p.samples,nonzero:p.nonzero,contexts:p.contexts.map(c=>({state:c.state,sample_rate:c.sampleRate})),outputs:p.analysers.length};
    });
    await page.evaluate(() => { const p=window.__arenaAudioOutput; p.peak=0; p.samples=0; p.nonzero=0; });
    await page.screenshot({path:path.join(outdir,'ready.png')});
    if (before.exploration_touch) throw new Error('Exploration controls overlap arena controls');
    const manifest = fs.readFileSync(path.join(__dirname, '../godot/data/audio/arena_audio.json'));
    const expectedAudio = require('crypto').createHash('sha256').update(manifest).digest('hex');
    const sfxCount = new Set(Object.values(JSON.parse(manifest).cues).flat()).size;
    if (before.audio_manifest_sha256 !== expectedAudio || before.sfx_loaded !== sfxCount || before.audio_missing.length || before.ambience_db !== -20)
      throw new Error('Web audio differs from current local scene: ' + JSON.stringify(before));
    if (!before.hero_3d || before.walk_reachable_cells < 100) throw new Error('3D hero or traversal geometry missing');
    if (before.paint_files_bad?.length || before.paint_pieces?.bakes_missing?.length || !(before.paint_pieces?.baked_meshes > 0))
      throw new Error('World painting missing: ' + JSON.stringify(before.paint_pieces));
    // Measure wall-clock presentation intervals, independently of engine delta clamping.
    await page.evaluate(() => {
      window.__arenaFrames = []; let previous;
      const sample = now => { if (previous !== undefined) window.__arenaFrames.push(now - previous); previous = now; window.__arenaFrame = requestAnimationFrame(sample); };
      window.__arenaFrame = requestAnimationFrame(sample);
    });
    const cdp = await page.context().newCDPSession(page);
    if (perf) {
      await page.keyboard.press('m'); // Autopilot still needs a user gesture to resume browser audio.
      await page.keyboard.press('m');
      await sleep(35000);
      await observe('performance-combat');
    } else if (touch) {
      await cdp.send('Input.dispatchTouchEvent', {type:'touchStart',touchPoints:[{x:320,y:210,id:1}]});
      await sleep(1500);
      await observe('moving');
      await cdp.send('Input.dispatchTouchEvent', {type:'touchEnd',touchPoints:[]});
      // Buttons use the 1920x1080 canvas, scaled/letterboxed into 844x390.
      const scale = 390 / 1080, padX = (844 - 1920 * scale) / 2;
      const at = (x,y) => ({x:padX + x*scale,y:y*scale,id:2});
      // Exercise every skill button and verify accepted cues from the real adapter.
      for (const [skill,x,y,cue] of [['Potion',1586.5,988,'potion'], ['Might',1609.5,815.5,'vires_might'], ['Battle Cry',1713,700.5,'war_cry'], ['Haste',1851,700.5,'rune_of_rush']]) {
        const previous = await observe('before-' + skill);
        await cdp.send('Input.dispatchTouchEvent', {type:'touchStart',touchPoints:[at(x,y)]});
        await sleep(100);
        await cdp.send('Input.dispatchTouchEvent', {type:'touchEnd',touchPoints:[]});
        await sleep(400);
        const accepted = await observe('accepted-' + skill);
        if ((accepted.audio_played[cue] || 0) <= (previous.audio_played[cue] || 0)) throw new Error('Touch skill not accepted: ' + skill);
      }
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
    const audible = await audioOutput();
    fs.writeFileSync(path.join(outdir, 'audio-output.json'), JSON.stringify(audible,null,2));
    console.log('WebAudio output: ' + JSON.stringify(audible));
    if (!audible.contexts.some(c=>c.state==='running') || audible.peak <= 0.00001 || audible.nonzero === 0)
      throw new Error('Browser output is silent despite triggered cues: ' + JSON.stringify(audible));
    if (!perf && (after.channel || after.zoomed_out === before.zoomed_out)) throw new Error('Channel release or zoom input failed');
    if (!perf && !inputs.some(x => x.label === 'moving' && JSON.stringify(x.position) !== JSON.stringify(before.position))) throw new Error('Player did not move');
    let sustainedStart = null;
    if (mode === '--touch-long') {
      sustainedStart = await page.evaluate(() => window.__arenaFrames.length);
      const scale = 390 / 1080, padX = (844 - 1920 * scale) / 2;
      await cdp.send('Input.dispatchTouchEvent', {type:'touchStart',touchPoints:[{x:padX+1782*scale,y:907.5*scale,id:3}]});
      await sleep(1000);
      if (!(await observe('long-channel-held')).channel) throw new Error('Long touch channel did not start');
      await sleep(34000);
      const sustained = await observe('sustained-touch-combat');
      if (sustained.tick < after.tick + 350) throw new Error('Sustained combat did not advance for the test interval');
      await cdp.send('Input.dispatchTouchEvent', {type:'touchEnd',touchPoints:[]});
      await sleep(500);
      if ((await observe('sustained-channel-released')).channel) throw new Error('Long touch channel did not release');
    }
    frameTimes = await page.evaluate(() => { cancelAnimationFrame(window.__arenaFrame); return window.__arenaFrames; });
    const ordered = [...frameTimes].sort((a,b) => a-b);
    const average = frameTimes.reduce((a,b) => a+b,0) / frameTimes.length;
    const surface = await page.evaluate(() => { const c=document.querySelector('canvas'); return {width:c.width,height:c.height,dpr:devicePixelRatio}; });
    const timing = {frames:frameTimes.length, average_ms:average, fps:1000/average, p99_ms:ordered[Math.floor(ordered.length*.99)], max_ms:ordered.at(-1), over_33_ms:frameTimes.filter(x=>x>33.4).length, surface};
    if (sustainedStart !== null) {
      const frames = frameTimes.slice(sustainedStart), sorted = [...frames].sort((a,b)=>a-b);
      const mean = frames.reduce((a,b)=>a+b,0)/frames.length;
      timing.sustained_combat = {frames:frames.length, average_ms:mean, fps:1000/mean, p99_ms:sorted[Math.floor(sorted.length*.99)], max_ms:sorted.at(-1), over_33_ms:frames.filter(x=>x>33.4).length};
    }
    fs.writeFileSync(path.join(outdir, 'performance.json'), JSON.stringify(timing,null,2));
    console.log('Frame timings: ' + JSON.stringify(timing));
    if (!perf) {
      if (mode !== '--touch-long') {
        // Verify the real graph is silent with both buses muted, then prove
        // combat SFX reach it while music and environment remain muted.
        await page.keyboard.press('m'); await page.keyboard.press('k');
        await sleep(350);
        const resetOutput = () => page.evaluate(() => { const p=window.__arenaAudioOutput; p.peak=0; p.samples=0; p.nonzero=0; });
        await resetOutput(); await sleep(500);
        const mutedOutput = await audioOutput();
        if (mutedOutput.peak > 0.00001) throw new Error('Muted audio graph still emits sound: ' + JSON.stringify(mutedOutput));
        await page.keyboard.press('k');
        await resetOutput();
        if (touch) {
          const scale=390/1080,padX=(844-1920*scale)/2;
          await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:padX+1782*scale,y:907.5*scale,id:4}]});
          await sleep(1800);
          await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
        } else {
          await page.mouse.down({button:'right'}); await sleep(1800); await page.mouse.up({button:'right'});
        }
        const sfxOutput = await audioOutput();
        if (sfxOutput.peak <= 0.00001 || sfxOutput.nonzero===0) throw new Error('Combat SFX output is silent with background muted');
        await page.keyboard.press('m');
        fs.writeFileSync(path.join(outdir,'audio-output.json'),JSON.stringify({combined:audible,all_muted:mutedOutput,sfx_only:sfxOutput},null,2));
      }
      for (const [key, property] of [['m','music_muted'], ['k','sfx_muted']]) {
        await page.keyboard.press(key); await sleep(350);
        if (!(await observe('muted-' + property))[property]) throw new Error('Mute key failed: ' + key);
        await page.keyboard.press(key); await sleep(350);
        if ((await observe('unmuted-' + property))[property]) throw new Error('Unmute key failed: ' + key);
      }
      await page.keyboard.press('b');
      await page.waitForFunction(expected => window.__barrowProbe?.music_index === expected,
        (before.music_index + 1) % JSON.parse(manifest).music.length, {timeout:15000});
      if ((await observe('next-score')).music_index !== (before.music_index + 1) % JSON.parse(manifest).music.length) throw new Error('Score selection failed');
    }
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
