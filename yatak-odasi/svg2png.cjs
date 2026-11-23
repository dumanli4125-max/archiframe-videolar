const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ deviceScaleFactor: 2 });
 const svg = fs.readFileSync(process.argv[2], 'utf8'); const w = +svg.match(/width="([\d.]+)"/)[1], h = +svg.match(/height="([\d.]+)"/)[1];
 await p.setViewportSize({ width: Math.ceil(w), height: Math.ceil(h) }); await p.setContent(`<body style="margin:0">${svg}</body>`);
 await p.locator('svg').screenshot({ path: process.argv[3] }); await b.close(); })();
