import { createRequire } from 'module'; const { chromium } = createRequire(import.meta.url)('playwright');
import fs from 'fs'; import path from 'path';
const NM = process.env.NM; const DIR = path.resolve('.'); const OUT = process.argv[2] || 'gorseller';
fs.mkdirSync(OUT, { recursive: true });
const jobs = JSON.parse(fs.readFileSync(process.argv[3] || 'jobs.json', 'utf8'));
const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
const p = await b.newPage({ viewport: { width: 1800, height: 1200 } });
p.on('console', m => console.log('[page]', m.text())); p.on('pageerror', e => console.log('[err]', e.message));
await p.route('http://local/**', async r => {
  const u = new URL(r.request().url()); let f = u.pathname.slice(1);
  f = f.startsWith('three/') ? path.join(NM, f) : path.join(DIR, f);
  const ct = f.endsWith('.js') ? 'text/javascript' : 'text/html';
  r.fulfill({ status: 200, contentType: ct, body: fs.readFileSync(f) });
});
for (const j of jobs) {
  const qs = new URLSearchParams(Object.fromEntries(Object.entries(j.q).map(([k, v]) => [k, typeof v === 'object' ? JSON.stringify(v) : String(v)])));
  await p.setViewportSize({ width: +(j.q.w || 1600), height: +(j.q.h || 1000) });
  await p.goto('http://local/render.html?' + qs, { waitUntil: 'load' });
  await p.waitForFunction(() => window.__done, null, { timeout: 120000 });
  if (j.glb) { const s = await p.evaluate(() => window.__api.exportGLB()); fs.writeFileSync(path.join(OUT, j.name), Buffer.from(s, 'base64')); }
  else await p.locator('canvas').screenshot({ path: path.join(OUT, j.name) });
  console.log('ok', j.name);
}
await b.close();
