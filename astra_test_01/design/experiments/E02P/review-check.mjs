import {chromium} from '../E02/pixi/vendor/playwright-package/package/index.mjs';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url)),out=path.join(here,'evidence/batch-03-review');
if(fs.existsSync(out))throw new Error('Refusing to overwrite review batch');fs.mkdirSync(out);
const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--use-angle=metal']});
const page=await browser.newPage({viewport:{width:1540,height:1100},deviceScaleFactor:1});
const record={started_at:new Date().toISOString(),errors:[],checks:[]};page.on('pageerror',e=>record.errors.push(e.message));
try{
 await page.goto('file://'+path.join(here,'review.html'));
 for(const camera of['fixed','tracking'])for(const sample of['center','far','near','left','right','far-left','far-right','near-left','near-right']){
  await page.selectOption('#camera',camera);await page.selectOption('#sample',sample);
  await page.waitForFunction(()=>[...document.images].every(i=>i.complete&&i.naturalWidth>0));
  record.checks.push({camera,sample,images:await page.evaluate(()=>[...document.images].map(i=>({id:i.id,width:i.naturalWidth,height:i.naturalHeight,src:i.getAttribute('src')})))});
 }
 for(const sample of['center','right']){
  await page.selectOption('#camera','fixed');await page.selectOption('#sample',sample);await page.waitForFunction(()=>[...document.images].every(i=>i.complete&&i.naturalWidth>0));
  await page.screenshot({path:path.join(out,sample+'.png'),fullPage:true});
 }
 await page.click('#enlarge');record.hide_details=await page.locator('.detail:visible').count()===0;
 await page.click('#enlarge');record.show_details=await page.locator('.detail:visible').count()===3;
}catch(e){record.errors.push(e.stack);process.exitCode=1;}finally{record.finished_at=new Date().toISOString();fs.writeFileSync(path.join(out,'review-check.json'),JSON.stringify(record,null,2)+'\n');await browser.close();}
console.log(JSON.stringify({cases:record.checks.length,errors:record.errors,hide:record.hide_details,show:record.show_details}));
