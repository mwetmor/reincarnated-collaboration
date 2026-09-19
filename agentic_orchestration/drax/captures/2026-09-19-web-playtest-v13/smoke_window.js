// web13: close the sampling gap in the A/B pass. The seven-verdict harness takes six
// back-to-back frames (~0-1.5 s) then jumps to +4 s, so a smoke pass that fires between
// 1.5 s and 4 s would be invisible to it. This casts arm B once and samples every ~300 ms
// for 9 s continuously. drax, 2026-09-19.
const { chromium } = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');
const fs=require('fs'), path=require('path');
const url=process.argv[2], outdir=process.argv[3], label=process.argv[4]||'smoke';
fs.mkdirSync(outdir,{recursive:true});
const sleep=(ms)=>new Promise(r=>setTimeout(r,ms));
(async()=>{
  const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,
    args:['--headless=new','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
  const context=await browser.newContext({viewport:{width:844,height:390},deviceScaleFactor:2,hasTouch:true,isMobile:true});
  const page=await context.newPage(); const logs=[];
  page.on('console',m=>logs.push(`[${m.type()}] ${m.text()}`));
  await page.goto(url,{waitUntil:'load',timeout:180000});
  let booted=false;
  for(let i=0;i<200;i++){const h=await page.evaluate(()=>{const s=document.getElementById('status');
    return s?getComputedStyle(s).display==='none'||s.style.visibility==='hidden':true;});
    if(h){booted=true;break;} await sleep(1000);}
  await sleep(6000);
  const cdp=await context.newCDPSession(page);
  const touch=(t,p)=>cdp.send('Input.dispatchTouchEvent',{type:t,touchPoints:p});
  let n=0; const shot=(tag)=>page.screenshot({path:path.join(outdir,`${label}_${String(++n).padStart(2,'0')}_${tag}.png`)});
  await page.keyboard.down('KeyD'); await sleep(60); await page.keyboard.up('KeyD'); await sleep(500);
  await shot('control_precast');
  for(let i=0;i<18;i++){await page.keyboard.press('Tab');await sleep(250);}   // -> index 18, arm B
  await shot('kit_label');
  await touch('touchStart',[{x:700,y:314,id:2}]);
  await sleep(120); await touch('touchEnd',[]);
  for(let i=0;i<30;i++){ await shot(`t${String(i*300).padStart(4,'0')}ms`); await sleep(300); }
  fs.writeFileSync(path.join(outdir,`${label}_console.txt`),[`booted=${booted}`,'--- console',...logs].join('\n'));
  console.log(`done booted=${booted}`);
  console.log(logs.filter(l=>/error/i.test(l)).slice(0,6).join('\n')||'(no error lines)');
  await browser.close();
})().catch(e=>{console.error(e);process.exit(1);});
