// syntetic.tr kurgu paketi — ortak motor. Sahne dosyası bu dosyayı yükler, sonra scene(t) tanımlayıp K.run(DURATION, scene) çağırır.
// Koordinat: 1080x1920, zemin çizgisi FLOOR=1400. Zaman t saniye.
const C = {
  bgTop:'#0f1d33', bgBot:'#070e1a', wall:'#13233c', floor:'#0b1628',
  line:'#2a4166', amber:'#ffb547', coral:'#ff6b5b', cream:'#efe4cf',
  teal:'#5fd3c6', ink:'#081120'
};
// Dil: sahne URL'sinde ?lang=en varsa İngilizce sürüm. Metinlerde L('Türkçe','English') kullan.
const LANG = new URLSearchParams(location.search).get('lang') || 'tr';
const HANDLES = {tr:'@syntetic.tr', en:'@syntetic.en'};
let HANDLE = HANDLES[LANG] || HANDLES.tr;
const L = (tr, en) => (LANG === 'en' && en !== undefined) ? en : tr;
const W = 1080, H = 1920, FLOOR = 1400;
const cv = document.getElementById('c'), ctx = cv.getContext('2d');

// ---------- yardımcılar ----------
const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
const sm=(a,b,t)=>{const x=clamp((t-a)/(b-a));return x*x*(3-2*x);};
const lerp=(a,b,k)=>a+(b-a)*k;
const rad=d=>d*Math.PI/180;
const V=(a,l)=>[Math.sin(rad(a))*l, Math.cos(rad(a))*l]; // 0=aşağı, 90=ileri, 180=yukarı
function rr(x,y,w,h,r){ctx.beginPath();ctx.moveTo(x+r,y);ctx.arcTo(x+w,y,x+w,y+h,r);ctx.arcTo(x+w,y+h,x,y+h,r);ctx.arcTo(x,y+h,x,y,r);ctx.arcTo(x,y,x+w,y,r);ctx.closePath();}
function glow(color,b){ctx.shadowColor=color;ctx.shadowBlur=b;}
function noGlow(){ctx.shadowBlur=0;ctx.shadowColor='transparent';}

// grain dokusu
const grain=document.createElement('canvas');grain.width=grain.height=512;
(function(){const g=grain.getContext('2d'),d=g.createImageData(512,512);let s=7;
 for(let i=0;i<d.data.length;i+=4){s=(s*16807)%2147483647;const v=s%255;d.data[i]=d.data[i+1]=d.data[i+2]=v;d.data[i+3]=255;}g.putImageData(d,0,0);})();

// ---------- KARAKTER: "fasulye" gövde + yuvarlak kafa + göz ----------
function figure(o){
  const s=o.s||1, f=o.facing||1, col=o.color||C.cream;
  const L={torso:118*s,r:40*s,ua:62*s,fa:58*s,th:72*s,sh:70*s,w:19*s,body:60*s};
  const P=(p,a,l)=>{const v=V(a,l);return [p[0]+v[0]*f,p[1]+v[1]];};
  const hip=[o.x,o.y];
  const br=Math.sin((window.__t||0)*2.4+(o.x||0)*0.01)*1.5;
  const sh=P(hip,180-(o.lean||0)-br,L.torso+br);
  const limbCol=o.limb||shade(col,-0.18);
  ctx.save();ctx.globalAlpha=o.alpha??1;ctx.lineCap='round';ctx.lineJoin='round';
  const limb=(root,a1,a2,l1,l2,c)=>{const j=P(root,a1,l1),e=P(j,a2,l2);
    ctx.strokeStyle=c;ctx.lineWidth=L.w;ctx.beginPath();ctx.moveTo(...root);ctx.lineTo(...j);ctx.lineTo(...e);ctx.stroke();return e;};
  if(o.glow!==false) glow(col,30*s);
  // arka uzuvlar
  limb(hip,o.th2??o.th??0,o.sh2??o.sh??0,L.th,L.sh,shade(limbCol,-0.25));
  const handB=limb(P(sh,0,10*s),o.ua2??o.ua??0,o.fa2??o.fa??0,L.ua,L.fa,shade(limbCol,-0.25));
  // gövde (kapsül)
  ctx.strokeStyle=col;ctx.lineWidth=L.body;ctx.beginPath();ctx.moveTo(...P(hip,180-(o.lean||0),8*s));ctx.lineTo(...P(sh,0,14*s));ctx.stroke();
  // ön uzuvlar
  limb(hip,o.th??0,o.sh??0,L.th,L.sh,limbCol);
  const hand=limb(P(sh,0,10*s),o.ua??0,o.fa??0,L.ua,L.fa,limbCol);
  // kafa
  const hc=P(P(sh,180-(o.lean||0),L.r+20*s),90,(o.nod||0)*s);
  hc[1]+= (o.nodY||0)*s;
  ctx.fillStyle=col;ctx.beginPath();ctx.arc(hc[0],hc[1],L.r,0,7);ctx.fill();
  noGlow();
  // gözler
  ctx.fillStyle=C.ink;ctx.strokeStyle=C.ink;ctx.lineWidth=5*s;
  const ey=hc[1]-4*s+(o.look||0)*s;
  const bt=((window.__t||0)+(o.x||0)*0.003)%3.1; const blink=bt<0.12&&o.eyes!=='tired';
  for(const dx of [10,27]){const ex=hc[0]+dx*f*s;
    if(o.eyes==='tired'||blink){ctx.beginPath();ctx.moveTo(ex-6*s,ey);ctx.lineTo(ex+6*s,ey);ctx.stroke();}
    else if(o.eyes==='wide'){ctx.beginPath();ctx.arc(ex,ey,6.5*s,0,7);ctx.fill();}
    else{ctx.beginPath();ctx.arc(ex,ey,5*s,0,7);ctx.fill();}}
  ctx.restore();
  return {hand,handB,head:hc,sh};
}
function shade(hex,k){const n=parseInt(hex.slice(1),16);let r=n>>16,g=(n>>8)&255,b=n&255;
  const f=v=>Math.round(k<0?v*(1+k):v+(255-v)*k);return '#'+[f(r),f(g),f(b)].map(v=>v.toString(16).padStart(2,'0')).join('');}

// ---------- UI parçaları ----------
// İngilizce sürümde sık etiketler otomatik çevrilir; listede olmayanlar için tag(L('TR','EN'),...) kullan.
const TAG_EN={'SEN':'YOU','OFİS':'OFFICE','EV':'HOME','MESAİ':'OVERTIME','ÇOCUĞUN':'YOUR KID','ÇOCUK':'KID','ANNE':'MOM','ANNEN':'YOUR MOM','ANNEM':'MOM',
  'BABA':'DAD','KARDEŞ':'SIBLING','PATRON':'BOSS','MÜŞTERİ':'CUSTOMER','KASİYER':'CASHIER','MUTFAK':'KITCHEN','SATICI':'SELLER','BANKA':'BANK',
  'MAAŞ':'SALARY','KİRA':'RENT','FATURA':'BILLS','TAKSİT':'INSTALLMENT','MARKET':'GROCERIES','HERKES':'EVERYONE','KOMŞU':'NEIGHBOR','ARKADAŞ':'FRIEND'};
function tag(text,x,y,color,alpha=1,strike=0){
  if(LANG==='en'&&TAG_EN[text])text=TAG_EN[text];
  ctx.save();ctx.globalAlpha=alpha;ctx.font='700 26px Inter';ctx.letterSpacing='5px';
  const w=ctx.measureText(text).width+34;ctx.textAlign='center';ctx.textBaseline='middle';
  rr(x-w/2,y-22,w,44,22);ctx.fillStyle=hexA(color,0.13);ctx.fill();ctx.lineWidth=2;ctx.strokeStyle=hexA(color,0.8);ctx.stroke();
  ctx.fillStyle=color;ctx.fillText(text,x+2.5,y+1);
  if(strike>0){ctx.strokeStyle=C.coral;ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(x-w/2-6,y);ctx.lineTo(x-w/2-6+(w+12)*strike,y);ctx.stroke();}
  ctx.restore();
}
function hexA(hex,a){const n=parseInt(hex.slice(1),16);return `rgba(${n>>16},${(n>>8)&255},${n&255},${a})`;}

function caption(lines,t0,t1,t,size=62,y=240){
  const a=sm(t0,t0+0.35,t)*(1-sm(t1-0.3,t1,t)); if(a<=0)return;
  ctx.save();ctx.globalAlpha=a;ctx.textAlign='center';ctx.textBaseline='middle';ctx.letterSpacing='0px';
  const dy=(1-sm(t0,t0+0.4,t))*20;
  lines.forEach((ln,i)=>{ // ln: [[metin,renk],...]
    ctx.font=`800 ${size}px Inter`;
    const total=ln.reduce((s,p)=>s+ctx.measureText(p[0]).width,0);let x=W/2-total/2;
    ln.forEach(p=>{ctx.textAlign='left';ctx.fillStyle=p[1]||'#fff';glow('rgba(0,0,0,.6)',18);ctx.fillText(p[0],x,y+dy+i*size*1.22);x+=ctx.measureText(p[0]).width;});
  });ctx.restore();
}

function clockPanel(x,y,str,pulse=0,alpha=1){
  ctx.save();ctx.globalAlpha=alpha;rr(x-130,y-58,260,116,18);ctx.fillStyle='#0a1426';ctx.fill();
  ctx.lineWidth=3;ctx.strokeStyle=hexA(C.amber,0.35+pulse*0.6);ctx.stroke();
  ctx.font='700 70px "DejaVu Sans Mono"';ctx.textAlign='center';ctx.textBaseline='middle';
  glow(C.amber,20+pulse*30);ctx.fillStyle=C.amber;ctx.fillText(str,x,y+3);ctx.restore();
}
function fmt(min){min=Math.floor(min);const h=Math.floor(min/60)%24,m=min%60;return String(h).padStart(2,'0')+':'+String(m).padStart(2,'0');}

function lampCone(x,y,w,len,a=1){
  ctx.save();ctx.globalAlpha=a;const g=ctx.createLinearGradient(0,y,0,y+len);
  g.addColorStop(0,hexA(C.amber,0.28));g.addColorStop(1,hexA(C.amber,0));
  ctx.fillStyle=g;ctx.beginPath();ctx.moveTo(x-30,y);ctx.lineTo(x+30,y);ctx.lineTo(x+w/2,y+len);ctx.lineTo(x-w/2,y+len);ctx.closePath();ctx.fill();
  const r=ctx.createRadialGradient(x,y+len,10,x,y+len,w*0.6);r.addColorStop(0,hexA(C.amber,0.18));r.addColorStop(1,hexA(C.amber,0));
  ctx.fillStyle=r;ctx.fillRect(x-w,y+len-w*0.3,w*2,w*0.6);ctx.restore();
}

function room(){
  const g=ctx.createLinearGradient(0,0,0,H);g.addColorStop(0,C.bgTop);g.addColorStop(1,C.bgBot);
  ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
  // zemin + perspektif ızgara
  ctx.fillStyle=C.floor;ctx.fillRect(0,FLOOR,W,H-FLOOR);
  ctx.strokeStyle=hexA(C.line,0.55);ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(0,FLOOR);ctx.lineTo(W,FLOOR);ctx.stroke();
  ctx.strokeStyle=hexA(C.line,0.22);ctx.lineWidth=1.5;
  for(let i=-8;i<=8;i++){ctx.beginPath();ctx.moveTo(W/2+i*70,FLOOR);ctx.lineTo(W/2+i*260,H);ctx.stroke();}
  for(let k=1;k<7;k++){const y=FLOOR+Math.pow(k/7,1.8)*(H-FLOOR);ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke();}
}

function notif(x,y,title,msg,a,scale=1){
  if(a<=0)return;ctx.save();ctx.globalAlpha=a;ctx.translate(x,y);ctx.scale(scale,scale);
  rr(-400,-62,800,124,26);ctx.fillStyle='rgba(16,30,54,0.96)';glow('rgba(0,0,0,.6)',30);ctx.fill();noGlow();
  ctx.lineWidth=2;ctx.strokeStyle=hexA(C.amber,0.5);ctx.stroke();
  rr(-370,-34,68,68,16);ctx.fillStyle=C.amber;ctx.fill();
  ctx.fillStyle=C.ink;ctx.font='800 34px Inter';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText((title||'P').trim().charAt(0),-336,2);
  ctx.textAlign='left';ctx.fillStyle=C.amber;ctx.font='800 28px Inter';ctx.letterSpacing='3px';ctx.fillText(title,-280,-20);
  ctx.letterSpacing='0px';ctx.fillStyle='#e9eef7';ctx.font='500 32px Inter';ctx.fillText(msg,-280,22);
  ctx.fillStyle='rgba(233,238,247,.45)';ctx.font='500 24px Inter';ctx.textAlign='right';ctx.fillText(L('şimdi','now'),370,-20);
  ctx.restore();
}

// ================== ZAMAN ==================
function keyed(t,kf){if(t<=kf[0][0])return kf[0][1];for(let i=1;i<kf.length;i++){if(t<=kf[i][0]){const a=kf[i-1],b=kf[i];return lerp(a[1],b[1],(t-a[0])/(b[0]-a[0]));}}return kf[kf.length-1][1];}
function fade(alpha,color='0,0,0'){if(alpha<=0)return;ctx.fillStyle=`rgba(${color},${alpha})`;ctx.fillRect(0,0,W,H);}

// ================== POZLAR (figure() için hazır açı setleri) ==================
// Açılar: 0=aşağı, 90=ileri (bakış yönü), 180=yukarı. th/sh: ön bacak uyluk/baldır, th2/sh2 arka bacak; ua/fa ön kol, ua2/fa2 arka kol.
const POSE={
  stand:{lean:3,th:0,sh:0,th2:0,sh2:0,ua:8,fa:14,ua2:8,fa2:14},
  sit:{lean:2,th:90,sh:0,th2:86,sh2:-4,ua:20,fa:60,ua2:18,fa2:56},          // kalça y = oturak yüksekliği
  sitPhone:{lean:-4,th:90,sh:0,th2:86,sh2:-4,ua:28,fa:140,ua2:22,fa2:146},   // telefon ele: el yüze yakın
  sitType:{lean:9,th:90,sh:0,th2:88,sh2:-2,ua:36,fa:95,ua2:34,fa2:93},       // masada klavye
  think:{lean:2,th:0,sh:0,th2:0,sh2:0,ua:20,fa:160,ua2:8,fa2:14},             // el çenede
  shrug:{lean:0,th:0,sh:0,th2:0,sh2:0,ua:60,fa:130,ua2:60,fa2:130},
  point:{lean:4,th:0,sh:0,th2:0,sh2:0,ua:95,fa:95,ua2:8,fa2:14},
  sad:{lean:12,th:0,sh:0,th2:0,sh2:0,ua:4,fa:6,ua2:4,fa2:6,eyes:'tired',nodY:8},
};
// Yürüme: p = faz (zamanla artar). Kullanım: figure({x,y:STAND_Y-walkBob(p),...walk(p)})
function walk(p,amp=24){const th=amp*Math.sin(p),th2=-amp*Math.sin(p);
  return {lean:4,th,sh:th-22*Math.max(0,-Math.cos(p)),th2,sh2:th2-22*Math.max(0,Math.cos(p)),ua:-22*Math.sin(p),fa:-22*Math.sin(p)+18,ua2:22*Math.sin(p),fa2:22*Math.sin(p)+18};}
function walkBob(p){return 5*Math.abs(Math.sin(p));}
// İki poz arası geçiş (sayısal alanlar)
function blend(a,b,k){const o={...a};for(const key in b){if(typeof b[key]==='number'&&typeof a[key]==='number')o[key]=lerp(a[key],b[key],k);else if(k>0.5)o[key]=b[key];}return o;}
const STAND_Y=FLOOR-142;            // s=1 ayakta kalça yüksekliği
const standY=s=>FLOOR-142*s;        // ölçekli karakter için

// ================== SAHNE OBJELERİ ==================
function desk(x=520,w=280,top=1268){ctx.fillStyle='#1d3254';ctx.fillRect(x,top,w,14);ctx.fillRect(x+20,top+14,12,FLOOR-top-14);ctx.fillRect(x+w-30,top+14,12,FLOOR-top-14);}
function monitor(x=600,y=1110,on=1){rr(x,y,170,118,10);ctx.fillStyle='#0b1426';ctx.fill();ctx.lineWidth=5;ctx.strokeStyle='#2c4772';ctx.stroke();
  ctx.save();glow(C.teal,40*on);rr(x+10,y+10,150,98,6);ctx.fillStyle=hexA(C.teal,0.15+0.35*on);ctx.fill();ctx.restore();ctx.fillStyle='#2c4772';ctx.fillRect(x+77,y+118,16,40);}
function chair(x=370){ctx.fillStyle='#22385c';ctx.fillRect(x,1328,120,14);ctx.fillRect(x+55,1342,10,58);rr(x-18,1180,22,160,10);ctx.fill();}  // oturan kalça: (x+60, 1322)
function sofa(x=270,w=370){ctx.fillStyle='#24406b';rr(x+20,1180,w-40,60,26);ctx.fill();rr(x,1240,w,95,22);ctx.fill();
  ctx.fillStyle='#1b3156';rr(x-15,1220,50,140,20);ctx.fill();rr(x+w-15,1220,50,140,20);ctx.fill();
  ctx.fillStyle='#16294a';ctx.fillRect(x+15,1360,14,40);ctx.fillRect(x+w-30,1360,14,40);}       // oturan kalça y=1300
function bed(x=200,w=560){ctx.fillStyle='#1b3156';rr(x,1260,w,80,14);ctx.fill();ctx.fillStyle='#2b4a7a';rr(x+10,1230,w-20,50,20);ctx.fill();
  ctx.fillStyle='#e9e2cf';rr(x+20,1205,140,40,18);ctx.fill();ctx.fillStyle='#16294a';rr(x-20,1140,30,260,10);ctx.fill();ctx.fillRect(x+w-14,1330,14,70);}
function floorLamp(x=190,a=1){ctx.strokeStyle='#2c4772';ctx.lineWidth=6;ctx.beginPath();ctx.moveTo(x,1400);ctx.lineTo(x,980);ctx.stroke();ctx.fillStyle='#2c4772';ctx.fillRect(x-40,1394,80,8);
  ctx.save();ctx.globalAlpha=a;ctx.fillStyle=C.amber;glow(C.amber,40);ctx.beginPath();ctx.moveTo(x-40,980);ctx.lineTo(x+40,980);ctx.lineTo(x+24,930);ctx.lineTo(x-24,930);ctx.closePath();ctx.fill();ctx.restore();noGlow();
  lampCone(x,980,460,420,a);}
function ceilingLamp(x=470,a=1,len=1130){ctx.strokeStyle=C.line;ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,230);ctx.stroke();
  ctx.fillStyle='#22385c';ctx.beginPath();ctx.moveTo(x-50,270);ctx.lineTo(x+50,270);ctx.lineTo(x+25,230);ctx.lineTo(x-25,230);ctx.closePath();ctx.fill();lampCone(x,270,560,len,a);}
function windowNight(x=600,y=560,w=380,h=440,{moon=true,city=false}={}){ctx.save();rr(x,y,w,h,10);ctx.fillStyle='#132a52';ctx.fill();ctx.clip();
  if(city){[[0,260,90],[100,200,70],[180,320,110],[300,160,80],[390,240,100],[500,130,90],[600,280,80],[690,200,110],[810,260,80]].forEach(([dx,dy,bw],i)=>{const bx=x+dx*(w/900),by=y+dy*(h/520),bww=bw*(w/900);
      ctx.fillStyle='#0d1a33';ctx.fillRect(bx,by,bww,h);for(let yy=by+20;yy<y+h;yy+=34)for(let xx=bx+12;xx<bx+bww-12;xx+=24){if(((xx*7+yy*13+i)%5)<2){ctx.fillStyle=hexA(C.amber,0.55);ctx.fillRect(xx,yy,10,14);}}});}
  if(moon){ctx.fillStyle='#e9e2cf';glow('#e9e2cf',40);ctx.beginPath();ctx.arc(x+w*0.68,y+110,46,0,7);ctx.fill();noGlow();ctx.fillStyle='#132a52';ctx.beginPath();ctx.arc(x+w*0.68+20,y+95,40,0,7);ctx.fill();}
  for(let i=0;i<14;i++){ctx.fillStyle='rgba(255,255,255,.5)';ctx.fillRect(x+10+((i*97)%(w-20)),y+10+((i*53)%(h*0.6)),3,3);}
  ctx.restore();ctx.strokeStyle=C.line;ctx.lineWidth=6;rr(x,y,w,h,10);ctx.stroke();ctx.beginPath();ctx.moveTo(x+w/2,y);ctx.lineTo(x+w/2,y+h);ctx.lineWidth=4;ctx.stroke();}
function door(x=975,light=1){ctx.save();rr(x,1030,120,370,6);ctx.fillStyle='#091222';ctx.fill();
  if(light>0){const g=ctx.createLinearGradient(x,0,x+105,0);g.addColorStop(0,hexA(C.amber,0.55*light));g.addColorStop(1,hexA(C.amber,0.25*light));ctx.fillStyle=g;ctx.fill();}
  ctx.restore();ctx.strokeStyle=C.line;ctx.lineWidth=6;ctx.strokeRect(x,1030,140,370);}
function plant(x=75){ctx.fillStyle='#1d3254';ctx.fillRect(x-35,1320,70,80);ctx.fillStyle='#2f6b62';for(let i=0;i<5;i++){ctx.beginPath();ctx.ellipse(x+(i-2)*14,1290-i%2*20,14,44,(i-2)*0.35,0,7);ctx.fill();}}
function frame(x=120,y=640){ctx.strokeStyle=C.line;ctx.lineWidth=4;rr(x,y,200,150,6);ctx.stroke();ctx.beginPath();ctx.moveTo(x+20,y+130);ctx.lineTo(x+70,y+60);ctx.lineTo(x+110,y+100);ctx.lineTo(x+180,y+40);ctx.stroke();}
// Telefon: (x,y) merkez, lit=true ise kehribar parlar, buzz>0 titreşir
function phone(x,y,{lit=false,color=null,buzz=0,rot=-0.35,t=0}={}){const bx=buzz>0?Math.sin(t*90)*4*buzz:0;ctx.save();ctx.translate(x+bx,y);ctx.rotate(rot);rr(-20,-36,40,72,8);ctx.fillStyle='#0a1222';ctx.fill();
  const c=color||(lit?C.amber:C.teal);glow(c,40);rr(-15,-30,30,60,5);ctx.fillStyle=hexA(c,lit?0.8:0.55);ctx.fill();ctx.restore();
  const g=ctx.createRadialGradient(x,y,5,x,y,170);g.addColorStop(0,hexA(c,lit?0.28:0.12));g.addColorStop(1,'rgba(0,0,0,0)');ctx.fillStyle=g;ctx.fillRect(x-170,y-170,340,340);
  if(buzz>0){for(let i=0;i<3;i++){const r_=((t*120)+i*30)%90;ctx.strokeStyle=hexA(C.amber,(1-r_/90)*buzz);ctx.lineWidth=3;ctx.beginPath();ctx.arc(x,y,30+r_,-1.2,-0.2);ctx.stroke();ctx.beginPath();ctx.arc(x,y,30+r_,Math.PI+0.2,Math.PI+1.2);ctx.stroke();}}}
// Konuşma balonu
function bubble(x,y,text,a,color){if(a<=0)return;ctx.save();ctx.globalAlpha=a;ctx.font='700 34px Inter';ctx.letterSpacing='0px';
  const w=ctx.measureText(text).width+48;const dy=(1-a)*12;
  rr(x-w/2,y-36+dy,w,72,36);ctx.fillStyle=C.cream;glow('rgba(0,0,0,.5)',20);ctx.fill();noGlow();
  ctx.beginPath();ctx.moveTo(x-12,y+34+dy);ctx.lineTo(x+12,y+34+dy);ctx.lineTo(x,y+56+dy);ctx.closePath();ctx.fill();
  ctx.fillStyle=color||C.ink;ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(text,x,y+2+dy);ctx.restore();}
// Büyük kart (test videoları için: soru kartı, sayaç, seçenek kutuları)
function card(x,y,w,h,{fill='rgba(16,30,54,0.96)',stroke=C.amber,alpha=1,r=26}={}){ctx.save();ctx.globalAlpha=alpha;rr(x-w/2,y-h/2,w,h,r);ctx.fillStyle=fill;glow('rgba(0,0,0,.5)',30);ctx.fill();noGlow();ctx.lineWidth=3;ctx.strokeStyle=hexA(stroke,0.7);ctx.stroke();ctx.restore();}
function bigText(text,x,y,size=72,color='#fff',alpha=1,weight=800){if(alpha<=0)return;ctx.save();ctx.globalAlpha=alpha;ctx.font=`${weight} ${size}px Inter`;ctx.textAlign='center';ctx.textBaseline='middle';ctx.letterSpacing='0px';ctx.fillStyle=color;glow('rgba(0,0,0,.6)',18);ctx.fillText(text,x,y);ctx.restore();}
// Geri sayım halkası (testler)
function countdown(x,y,r,remaining,total,alpha=1){ctx.save();ctx.globalAlpha=alpha;ctx.lineWidth=12;ctx.strokeStyle=hexA(C.line,0.8);ctx.beginPath();ctx.arc(x,y,r,0,7);ctx.stroke();
  ctx.strokeStyle=remaining/total<0.3?C.coral:C.amber;glow(ctx.strokeStyle,20);ctx.beginPath();ctx.arc(x,y,r,-Math.PI/2,-Math.PI/2+Math.PI*2*clamp(remaining/total));ctx.stroke();noGlow();
  ctx.font='800 64px Inter';ctx.fillStyle='#fff';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(String(Math.ceil(remaining)),x,y+2);ctx.restore();}
// Kapanış kartı (son 2-3 sn)
function endCard(t,t0){const a=sm(t0,t0+0.6,t);if(a<=0)return;ctx.save();ctx.globalAlpha=a;ctx.textAlign='center';ctx.font='700 40px Inter';ctx.letterSpacing='6px';ctx.fillStyle=C.amber;ctx.fillText(HANDLE.toUpperCase(),W/2,1380);
  ctx.font='500 32px Inter';ctx.letterSpacing='1px';ctx.fillStyle='rgba(239,228,207,.7)';ctx.fillText(L('Takip et, sorgulamaya devam et.','Follow for more. Keep questioning.'),W/2,1440);ctx.restore();}

// ================== SON İŞLEM + ÇALIŞTIRICI ==================
function post(t,frameNo){
  const v=ctx.createRadialGradient(W/2,H*0.55,W*0.35,W/2,H*0.55,H*0.75);v.addColorStop(0,'rgba(0,0,0,0)');v.addColorStop(1,'rgba(0,0,0,.6)');
  ctx.fillStyle=v;ctx.fillRect(0,0,W,H);
  ctx.save();ctx.globalAlpha=0.05;ctx.globalCompositeOperation='overlay';const ox=(frameNo*137)%512,oy=(frameNo*271)%512;
  for(let x=-ox;x<W;x+=512)for(let y=-oy;y<H;y+=512)ctx.drawImage(grain,x,y);ctx.restore();
  ctx.save();ctx.globalAlpha=0.55;ctx.font='600 26px Inter';ctx.letterSpacing='3px';ctx.fillStyle=C.cream;ctx.textAlign='center';ctx.fillText(HANDLE,W/2,1780);ctx.restore();
}
const K={run(duration,sceneFn){window.DURATION=duration;
  window.render=(t,frameNo=0)=>{window.__t=t;ctx.save();ctx.letterSpacing='0px';sceneFn(t);ctx.restore();post(t,frameNo);};
  document.fonts.load('800 40px Inter').then(()=>{window.ready=true;window.render(0);});}};
