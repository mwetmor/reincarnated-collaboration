import {chromium}from '/Users/admin/Games/reincarnated-collaboration/astra_test_01/design/experiments/E02/pixi/vendor/playwright-package/package/index.mjs';
import fs from'node:fs';
const base='/Users/admin/Games/reincarnated-collaboration/astra_test_01/design/experiments/';
const b=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
try{for(const[id,batch,cap]of[['E07V','batch-01-review',45000000],['E08A','batch-02-review',20000000]]){
 const dir=base+id+'/evidence/'+batch;if(fs.existsSync(dir))throw Error('No overwrite');fs.mkdirSync(dir,{recursive:true});
 const p=await b.newPage({viewport:{width:1280,height:900}}),errors=[];p.on('pageerror',e=>errors.push(e.message));await p.goto('file://'+base+id+'/review.html');await p.waitForFunction(()=>[...document.images].every(i=>i.complete&&i.naturalWidth>0));
 const images=await p.locator('img').evaluateAll(xs=>xs.map(x=>({src:x.getAttribute('src'),width:x.naturalWidth,height:x.naturalHeight})));
 if(id==='E08A'){await p.getByRole('button',{name:'Packed atlas',exact:true}).click();await p.waitForFunction(()=>document.querySelector('#frame').src.endsWith('atlas-12.png'));await p.waitForFunction(()=>document.querySelector('#frame').complete);}
 const png=await p.screenshot();const size=d=>fs.readdirSync(d,{withFileTypes:true}).reduce((n,e)=>n+(e.isDirectory()?size(d+'/'+e.name):fs.statSync(d+'/'+e.name).size),0);if(size(base+id)+png.length+50000>cap)throw Error('Capacity');fs.writeFileSync(dir+'/review.png',png);fs.writeFileSync(dir+'/review.json',JSON.stringify({at:new Date().toISOString(),images,errors,pass:errors.length===0,delivery:'file:// Chrome'},null,2));console.log(id,images.length,errors);await p.close();
}}finally{await b.close();}
