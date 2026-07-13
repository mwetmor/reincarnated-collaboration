import { chromium } from 'playwright';
const URL='https://reincarnated-glance-i26spw3cp-matthew-wetmore-s-projects.vercel.app/#/atlas';
const OUT='/Users/admin/Games/reincarnated-collaboration/agentic_orchestration/galadriel/captures/2026-07-13-glance-atlas-perdot-v3';
function popScan(){const cards=[...document.querySelectorAll('*')].filter(el=>{const cs=getComputedStyle(el);const b=el.getBoundingClientRect();return (cs.position==='fixed'||cs.position==='absolute')&&b.width>70&&b.width<700&&b.height>20&&b.height<680&&(el.textContent||'').trim().length>6&&cs.visibility!=='hidden'&&cs.opacity!=='0';}).map(el=>{const b=el.getBoundingClientRect();const mono=[...el.querySelectorAll('*')].some(d=>/mono/i.test(getComputedStyle(d).fontFamily));return{text:(el.textContent||'').replace(/\s+/g,' ').trim().slice(0,80),x:Math.round(b.left),right:Math.round(b.right),w:Math.round(b.width),h:Math.round(b.height),y:Math.round(b.top),hasMono:mono};});return cards.filter(c=>c.hasMono).sort((a,b)=>(a.w*a.h)-(b.w*b.h));}
const browser=await chromium.launch();
const ctx=await browser.newContext({viewport:{width:375,height:812},deviceScaleFactor:2});
const page=await ctx.newPage();
await page.goto(URL.split('#')[0],{waitUntil:'domcontentloaded'});
await page.evaluate(()=>{window.location.hash='#/atlas';});
await page.waitForLoadState('networkidle').catch(()=>{});
await page.waitForTimeout(3000);
await page.evaluate(()=>document.querySelector('svg[viewBox]').scrollIntoView({block:'center'}));
await page.waitForTimeout(400);
// hover ROOTED-row right-edge dot: screenX 368 screenY 435 (Judgement Paladin) — same Y band as working left test
async function t(label,X,Y){await page.mouse.move(2,2);await page.waitForTimeout(200);await page.mouse.move(X,Y);await page.waitForTimeout(700);const p=(await page.evaluate(popScan))[0];const ring=await page.evaluate(()=>{const c=document.querySelector('svg[viewBox] circle');return c?{cx:+c.getAttribute('cx').toFixed?+c.getAttribute('cx'):+c.getAttribute('cx')}:null;});console.log(`[${label}] hover(${X},${Y}) ring=${ring?'yes':'NONE'} popover=${p?`x=${p.x} right=${p.right} w=${p.w} onScreen=${p.x>=-1&&p.right<=376} overflowR=${Math.max(0,p.right-375)} overflowL=${Math.max(0,-p.x)} "${p.text.slice(0,30)}"`:'NONE'}`);await page.screenshot({path:`${OUT}/mobile-final-${label}.png`});return p;}
await t('right-rooted',368,435);
await t('right-walk',370,363);
await t('mid-rooted',200,435);
await ctx.close();await browser.close();console.log('DONE');
