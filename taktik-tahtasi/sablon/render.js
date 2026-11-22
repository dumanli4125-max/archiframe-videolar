const {chromium}=require('playwright');const fs=require('fs');const {spawn}=require('child_process');
const http=require('http'),path=require('path');
const MIME={'.html':'text/html','.js':'text/javascript','.ttf':'font/ttf','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.webp':'image/webp'};
const srv=http.createServer((q,s)=>{const f=path.join(__dirname,decodeURIComponent(q.url.split('?')[0]));fs.readFile(f,(e,d)=>{if(e){s.writeHead(404);s.end();return;}s.writeHead(200,{'Content-Type':MIME[path.extname(f).toLowerCase()]||'application/octet-stream'});s.end(d);});});
(async()=>{await new Promise(r=>srv.listen(0,'127.0.0.1',r));const PORT=srv.address().port;
 const mode=process.argv[2];const LAND=process.env.LAND==='1';const b=await chromium.launch();const pg=await b.newPage({viewport:LAND?{width:1920,height:1080}:{width:1080,height:1920}});
 pg.on('console',m=>console.log('PAGE',m.text()));pg.on('pageerror',e=>console.log('ERR',e.message));
 await pg.goto('http://127.0.0.1:'+PORT+'/'+(process.env.SCENE||'scene.html')+(LAND?'?h=1':''));await pg.evaluate(()=>Promise.all(['800 40px BC','700 40px BC','600 40px BC','500 20px PM'].map(f=>document.fonts.load(f))).then(()=>document.fonts.ready).then(()=>window.ready||null));
 const grab=async t=>Buffer.from((await pg.evaluate(t=>{render(t);return document.getElementById('c').toDataURL('image/jpeg',.93)},t)).split(',')[1],'base64');
 if(mode==='stills'){for(const t of process.argv.slice(3)){fs.writeFileSync(`${process.env.OUT||''}${LAND?'h':''}still_${t}.jpg`,await grab(+t));}}
 else{const fps=30,dur=await pg.evaluate(()=>DUR);const ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate',''+fps,'-c:v','mjpeg','-i','-','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-preset','medium',(process.env.OUT||'')+(LAND?'video_h_noaudio.mp4':'video_noaudio.mp4')],{stdio:['pipe','inherit','inherit']});
  for(let f=0;f<dur*fps;f++){const buf=await grab(f/fps);if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));}
  ff.stdin.end();await new Promise(r=>ff.on('close',r));}
 await b.close();srv.close();})();
