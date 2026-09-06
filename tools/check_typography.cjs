// Optional browser regression check. Requires Playwright with Chromium.
const {chromium} = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');

(async () => {
  const browser = await chromium.launch({headless: true, ...(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE ? {executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE} : {})});
  try {
    const page = await browser.newPage();
    const css = fs.readFileSync(path.join(__dirname, '../wp-content/themes/generatepress_child/style.css'), 'utf8');
    let checks = 0;
    for (const width of [1440, 768, 390]) {
      await page.setViewportSize({width, height: 900});
      await page.setContent(`<style>h1{font-size:100px}h2{font-size:90px}p{font-size:80px}.gb-text-early{font-size:23px}</style>
        <style>${css}</style><style>.gb-text-late{font-size:29px}</style>
        <h1 id="h1">H1</h1><h2 id="h2">H2</h2><p id="p">P</p>
        <h2 id="sized" class="fs-h1">H2 as H1</h2><p id="paragraph" class="fs-h1">P as H1</p>
        <h1 id="small" class="fs-p">H1 as P</h1><span id="span" class="fs-h1">Span</span>
        <h2 id="early" class="fs-h1 gb-text-early">Early override</h2>
        <h2 id="late" class="fs-h1 gb-text-late">Late override</h2>`);
      const values = await page.evaluate(() => Object.fromEntries([...document.querySelectorAll('[id]')].map(el => [el.id, getComputedStyle(el).fontSize])));
      for (const id of ['sized', 'paragraph', 'span']) { assert.equal(values[id], values.h1, `${width}: ${id}`); checks++; }
      assert.equal(values.small, values.p); checks++;
      assert.notEqual(values.h1, values.h2); checks++;
      assert.equal(values.early, '23px'); checks++;
      assert.equal(values.late, '29px'); checks++;
    }
    console.log(`${checks} Chromium typography assertions passed at 1440, 768 and 390px.`);
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
