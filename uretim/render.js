// Kullanım: node render.js <scene.html> <out.mp4> [fps]   |  node render.js <scene.html> --stills t1,t2,... <dir>
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
(async () => {
  const [scene, out, arg3, arg4] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  const [sFile, sQuery] = scene.split('?');
  await p.goto('file://' + path.resolve(sFile) + (sQuery ? '?' + sQuery : ''));
  await p.waitForFunction('window.ready === true');
  const shot = async (t, f) => { await p.evaluate(([t, f]) => window.render(t, f), [t, f]);
    const d = await p.evaluate(() => document.getElementById('c').toDataURL('image/png'));
    return Buffer.from(d.split(',')[1], 'base64'); };
  if (out === '--stills') {
    const fs = require('fs');
    for (const t of arg3.split(',').map(Number)) fs.writeFileSync(`${arg4}/s_${t}.png`, await shot(t, 0));
  } else {
    const fps = Number(arg3 || 30), dur = await p.evaluate('window.DURATION'), n = Math.round(dur * fps);
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-',
      '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', out], { stdio: ['pipe', 'inherit', 'inherit'] });
    for (let i = 0; i < n; i++) { const buf = await shot(i / fps, i); if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
  }
  await b.close();
})();
