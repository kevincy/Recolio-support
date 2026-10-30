// Isolated headless browser QA against this local site; no user Chrome profile.
const path=require('node:path');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE || path.join(require('node:os').homedir(),'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright'));
const fs=require('node:fs');
const assert=require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.BROWSER_EXECUTABLE || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 const out='/tmp/recolio-support-review-20261030';fs.mkdirSync(out,{recursive:true});
 const results=[];const errors=[];
 for(const width of [390,1280]){
  const context=await browser.newContext({viewport:{width,height:900},locale:'en-US'});
  const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));
  for(const lang of ['en','zh-Hans','ja','ko','es','zh-Hant']){
   for(const name of ['index','guide','support','privacy','terms']){
    await page.goto(`http://127.0.0.1:8096/${name}.html?lang=${lang}`,{waitUntil:'networkidle'});
    assert.equal(await page.getAttribute('html','lang'),lang);
    assert.equal(await page.locator('main > [data-locale]:visible').count(),1);
    assert.equal(await page.locator('h1:visible').count(),1);
    assert.equal(await page.locator('#language').inputValue(),lang);
    assert.ok(!(await page.title()).includes('undefined'));
    const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);
    assert.equal(overflow,false,`${lang} ${name} at ${width}: horizontal overflow`);
    const internal=await page.locator('a[href*=".html"]:visible').evaluateAll(xs=>xs.map(x=>x.href));
    for(const url of internal)assert.equal(new URL(url).searchParams.get('lang'),lang);
    if(name==='index'){
     const images=page.locator(`main > [data-locale="${lang}"] img`);
     for(let i=0;i<await images.count();i++){
      await images.nth(i).scrollIntoViewIfNeeded();
      await images.nth(i).evaluate(img=>img.decode());
      assert.ok(await images.nth(i).evaluate(img=>img.naturalWidth>0));
     }
     await page.evaluate(()=>scrollTo(0,0));
     if((width===1280&&['en','ja'].includes(lang))||(width===390&&['es','zh-Hant'].includes(lang)))await page.screenshot({path:`${out}/${lang}-${width}-home.png`});
     if(width===390&&lang==='ko'){
      await page.locator('#search-ko').scrollIntoViewIfNeeded();await page.screenshot({path:`${out}/ko-390-search.png`});
     }
    }
    results.push({language:lang,page:name,width,status:'PASS'});
   }
  }
  await page.goto('http://127.0.0.1:8096/index.html?lang=en');
  await page.selectOption('#language','ja');await page.reload();assert.equal(await page.getAttribute('html','lang'),'ja');
  await page.locator('footer a[href*="guide.html"]').click();
  assert.equal(await page.getAttribute('html','lang'),'ja');
  await context.close();
 }
 assert.deepEqual(errors,[]);
 await browser.close();fs.writeFileSync(out+'/results.json',JSON.stringify({cases:results.length,results,consoleErrors:errors},null,2));
 console.log(`BROWSER_PASS: ${results.length} page/locale/viewport cases; no overflow, all active images loaded, labels/metadata/locale links valid; selection persists.`);
})().catch(e=>{console.error(e);process.exit(1)});
