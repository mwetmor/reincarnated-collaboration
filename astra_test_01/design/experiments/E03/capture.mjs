import {chromium} from '../E02/pixi/vendor/playwright-package/package/index.mjs';
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));const engine=process.argv[2],tag=process.argv[3]??engine;if(!['pixi','phaser'].includes(engine))throw Error('Engine required');
if(fs.existsSync(path.join(here,'evidence',tag+'-runtime.json')))throw Error('Refusing overwrite');
const r={engine,started_at:new Date().toISOString(),cases:[],errors:[],warnings:[]};
const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--use-angle=metal']});
try{const page=await browser.newPage({viewport:{width:1100,height:850},deviceScaleFactor:1});page.on('pageerror',e=>r.errors.push(e.message));page.on('console',m=>{if(m.type()==='warning')r.warnings.push(m.text());});await page.goto('http://127.0.0.1:8770/E03/browser/?engine='+engine);await page.waitForSelector('body[data-ready=true]',{timeout:20000});const scenes=await page.evaluate(()=>window.E03.scenes);
for(let i=0;i<scenes.length;i++){await page.evaluate(i=>window.E03.set(i),i);await page.waitForTimeout(100);const result=await page.evaluate(()=>window.E03.results());const png=await page.evaluate(()=>document.querySelector('canvas').toDataURL('image/png'));fs.writeFileSync(path.join(here,'evidence',tag+'-'+scenes[i].id+'.png'),Buffer.from(png.split(',')[1],'base64'));r.cases.push(result);}
await page.selectOption('#scene','0');await page.click('#next');r.ui_next=(await page.evaluate(()=>window.E03.results())).scene==='floor-overlay';r.browser=browser.version();
}catch(e){r.errors.push(e.stack);process.exitCode=1;}finally{r.finished_at=new Date().toISOString();fs.writeFileSync(path.join(here,'evidence',tag+'-runtime.json'),JSON.stringify(r,null,2)+'\n');await browser.close();}console.log(JSON.stringify({engine,cases:r.cases.length,errors:r.errors}));
