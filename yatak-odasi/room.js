// Yatak odası 3B modeli — birim: cm. Plan koordinatı: x sağa, z aşağı (çizimdeki gibi), y yukarı.
import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';

// ---------- ÖLÇÜLER (taslaktan) ----------
export const R = {
  W: 266,          // oda genişliği (x)
  L: 262,          // oda derinliği (z) = kolon 32 + 230
  H: 260,          // tavan (varsayım)
  BEAM: 220,       // kiriş altı
  T: 20,           // duvar kalınlığı
  col: { x0: 0, x1: 14, z0: 0, z1: 32 },          // kolon 14x32
  pier: { x0: 246, x1: 266, z0: 0, z1: 40 },      // sağ üst duvar çıkıntısı
  winTop: { x0: 75, x1: 155, sill: 90, head: 210 },
  winRight: { z0: 45, z1: 100, sill: 90, head: 210 },
  balcony: { z0: 100, z1: 182, head: 210 },       // balkon kapısı, menteşe z=182
  niche: { z0: 182, z1: 242, d: 11 },             // 60 x 11 niş
  entry: { x0: 0, x1: 90, head: 210 },            // koridor ağzı / oda kapısı
};

const M = {};
function mats() {
  if (M.wall) return M;
  M.wall = new THREE.MeshStandardMaterial({ color: 0xe9e3da, roughness: 0.95 });
  M.accent = new THREE.MeshStandardMaterial({ color: 0xcdbfae, roughness: 0.95 });
  M.ceil = new THREE.MeshStandardMaterial({ color: 0xf6f4f0, roughness: 1 });
  M.floor = new THREE.MeshStandardMaterial({ map: floorTex(), roughness: 0.6 });
  M.pvc = new THREE.MeshStandardMaterial({ color: 0xf7f7f5, roughness: 0.4 });
  M.glass = new THREE.MeshPhysicalMaterial({ color: 0xcfe3ee, roughness: 0.05, transmission: 0.9, transparent: true, opacity: 0.25, metalness: 0 });
  M.oak = new THREE.MeshStandardMaterial({ map: woodTex('#c79c6c', '#b3875a'), roughness: 0.55 });
  M.oakDark = new THREE.MeshStandardMaterial({ color: 0x6b4a2f, roughness: 0.6 });
  M.white = new THREE.MeshStandardMaterial({ color: 0xf1eee8, roughness: 0.45 });
  M.greige = new THREE.MeshStandardMaterial({ color: 0xb5ab9d, roughness: 0.95 });
  M.linen = new THREE.MeshStandardMaterial({ color: 0xf4f1ec, roughness: 1 });
  M.sage = new THREE.MeshStandardMaterial({ color: 0x7d8f79, roughness: 1 });
  M.terra = new THREE.MeshStandardMaterial({ color: 0xc07a55, roughness: 1 });
  M.brass = new THREE.MeshStandardMaterial({ color: 0xc8a463, metalness: 0.9, roughness: 0.3 });
  M.black = new THREE.MeshStandardMaterial({ color: 0x2a2a2a, roughness: 0.5 });
  M.mirror = new THREE.MeshStandardMaterial({ color: 0xc4d0d6, metalness: 0.55, roughness: 0.08 });
  M.curtain = new THREE.MeshStandardMaterial({ color: 0xe9dfcf, roughness: 1, transparent: true, opacity: 0.88, side: THREE.DoubleSide });
  M.rug = new THREE.MeshStandardMaterial({ map: rugTex(), roughness: 1 });
  M.door = new THREE.MeshStandardMaterial({ color: 0xe9e4dc, roughness: 0.5 });
  M.leaf = new THREE.MeshStandardMaterial({ color: 0x5f7a52, roughness: 0.9 });
  M.pot = new THREE.MeshStandardMaterial({ color: 0xd8d0c4, roughness: 0.8 });
  M.radiator = new THREE.MeshStandardMaterial({ color: 0xfafafa, roughness: 0.35 });
  M.lampGlow = new THREE.MeshStandardMaterial({ color: 0xfff1d6, emissive: 0xffe2b0, emissiveIntensity: 1.2 });
  return M;
}

function canvas(w, h, draw) {
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  draw(c.getContext('2d'), w, h);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  t.wrapS = t.wrapT = THREE.RepeatWrapping; t.anisotropy = 8; return t;
}
function floorTex() {
  // 20 cm x 120 cm meşe laminat, doku 1 tekrar = 120 x 120 cm
  const t = canvas(1024, 1024, (g, w, h) => {
    const pw = w / 6, ph = h;
    for (let i = 0; i < 6; i++) {
      const off = (i % 3) * ph / 3;
      for (let k = -1; k < 2; k++) {
        const y = off + k * ph;
        const hue = 30 + Math.random() * 6, l = 62 + Math.random() * 8;
        g.fillStyle = `hsl(${hue},38%,${l}%)`; g.fillRect(i * pw, y, pw, ph);
        for (let s = 0; s < 40; s++) {
          g.strokeStyle = `hsla(${hue},35%,${l - 12}%,0.25)`; g.lineWidth = 1 + Math.random() * 2;
          const xx = i * pw + Math.random() * pw; g.beginPath(); g.moveTo(xx, y); g.bezierCurveTo(xx + 6, y + ph / 3, xx - 6, y + ph * 2 / 3, xx + 3, y + ph); g.stroke();
        }
        g.fillStyle = 'rgba(60,40,20,0.5)'; g.fillRect(i * pw, y, pw, 3);
      }
      g.fillStyle = 'rgba(60,40,20,0.5)'; g.fillRect(i * pw, 0, 3, h);
    }
  });
  return t;
}
function woodTex(a, b) {
  return canvas(256, 256, (g, w, h) => {
    g.fillStyle = a; g.fillRect(0, 0, w, h);
    for (let i = 0; i < 70; i++) {
      g.strokeStyle = b; g.globalAlpha = 0.25 + Math.random() * 0.3; g.lineWidth = 1 + Math.random() * 2;
      const y = Math.random() * h; g.beginPath(); g.moveTo(0, y); g.bezierCurveTo(w / 3, y + 8, 2 * w / 3, y - 8, w, y + 3); g.stroke();
    }
  });
}
function rugTex() {
  return canvas(512, 512, (g, w, h) => {
    g.fillStyle = '#e8e0d2'; g.fillRect(0, 0, w, h);
    g.strokeStyle = '#c9b89e'; g.lineWidth = 10; g.strokeRect(24, 24, w - 48, h - 48);
    g.strokeStyle = '#a88f6e'; g.lineWidth = 3; g.strokeRect(46, 46, w - 92, h - 92);
    g.globalAlpha = 0.07; for (let i = 0; i < 4000; i++) { g.fillStyle = Math.random() > .5 ? '#000' : '#fff'; g.fillRect(Math.random() * w, Math.random() * h, 2, 2); }
  });
}

// plan kutusu: x0..x1, z0..z1, y0..y1
function floorPlane(w, d, mat) {
  const geo = new THREE.PlaneGeometry(w, d); const uv = geo.attributes.uv;
  for (let i = 0; i < uv.count; i++) uv.setXY(i, uv.getX(i) * w / 120, uv.getY(i) * d / 120);
  return new THREE.Mesh(geo, mat);
}
function box(x0, x1, y0, y1, z0, z1, mat, round = 0) {
  const w = x1 - x0, h = y1 - y0, d = z1 - z0;
  const geo = round > 0 ? new RoundedBoxGeometry(w, h, d, 3, Math.min(round, w / 2, h / 2, d / 2)) : new THREE.BoxGeometry(w, h, d);
  const m = new THREE.Mesh(geo, mat);
  m.position.set((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2);
  m.castShadow = true; m.receiveShadow = true; return m;
}
function cyl(x, z, y0, y1, r, mat, seg = 24, r2) {
  const m = new THREE.Mesh(new THREE.CylinderGeometry(r2 ?? r, r, y1 - y0, seg), mat);
  m.position.set(x, (y0 + y1) / 2, z); m.castShadow = m.receiveShadow = true; return m;
}

// ---------- KABUK ----------
export function buildShell() {
  mats();
  const g = new THREE.Group(); g.name = 'kabuk';
  const { W, L, H, T, BEAM } = R;
  const tag = (o, t) => { o.userData.tag = t; g.add(o); return o; };

  // döşeme + koridor döşemesi
  const fl = floorPlane(W + 11, L, M.floor);
  fl.rotation.x = -Math.PI / 2; fl.position.set((W + 11) / 2, 0, L / 2); fl.receiveShadow = true; tag(fl, 'floor');
  const fl2 = floorPlane(90, 120, M.floor);
  fl2.rotation.x = -Math.PI / 2; fl2.position.set(45, 0, L + 60); fl2.receiveShadow = true; tag(fl2, 'floor');
  // tavan
  const cl = new THREE.Mesh(new THREE.PlaneGeometry(W + 11, L), M.ceil);
  cl.rotation.x = Math.PI / 2; cl.position.set((W + 11) / 2, H, L / 2); tag(cl, 'ceiling');

  // üst duvar (pencere boşluklu)
  const wt = R.winTop;
  tag(box(-T, wt.x0, 0, H, -T, 0, M.wall), 'wallTop');
  tag(box(wt.x1, W + T, 0, H, -T, 0, M.wall), 'wallTop');
  tag(box(wt.x0, wt.x1, 0, wt.sill, -T, 0, M.wall), 'wallTop');
  tag(box(wt.x0, wt.x1, wt.head, H, -T, 0, M.wall), 'wallTop');
  // sol duvar (koridora devam)
  tag(box(-T, 0, 0, H, 0, L + 120, M.wall), 'wallLeft');
  // sağ duvar
  const wr = R.winRight, bd = R.balcony, n = R.niche;
  tag(box(W, W + T, 0, H, -T, wr.z0, M.wall), 'wallRight');
  tag(box(W, W + T, 0, wr.sill, wr.z0, wr.z1, M.wall), 'wallRight');
  tag(box(W, W + T, wr.head, H, wr.z0, wr.z1, M.wall), 'wallRight');
  tag(box(W, W + T, bd.head, H, bd.z0, bd.z1, M.wall), 'wallRight');
  tag(box(W + n.d, W + n.d + T, 0, H, n.z0, n.z1, M.wall), 'wallRight');
  tag(box(W, W + T, 0, H, n.z1, L + T, M.wall), 'wallRight');
  // alt duvar + koridor ağzı
  const e = R.entry;
  tag(box(e.x1, W + T, 0, H, L, L + T, M.wall), 'wallBottom');
  tag(box(e.x0, e.x1, e.head, H, L, L + T, M.wall), 'wallBottom');
  tag(box(e.x1, e.x1 + 15, 0, H, L + T, L + 120, M.wall), 'wallBottom');
  tag(box(0, 0.6, 0, BEAM, R.col.z1, L, M.accent), 'accent');
  // kolon, çıkıntı
  tag(box(R.col.x0, R.col.x1, 0, H, R.col.z0, R.col.z1, M.wall), 'column');
  tag(box(R.pier.x0, R.pier.x1, 0, H, R.pier.z0, R.pier.z1, M.wall), 'pier');
  // kirişler (alt kotu 220)
  tag(box(0, W, BEAM, H, 0, 25, M.wall), 'beam');
  tag(box(0, W, BEAM, H, L - 25, L, M.wall), 'beamBottom');
  // süpürgelik
  const sk = new THREE.MeshStandardMaterial({ color: 0xf3f1ec, roughness: 0.5 });
  [[R.col.x1, R.pier.x0, 0, 1.2], [e.x1, W, L - 1.2, L]].forEach(([a, b, z0, z1]) => tag(box(a, b, 0, 8, z0, z1, sk), 'skirting'));
  tag(box(0, 1.2, 0, 8, R.col.z1, L, sk), 'skirting');

  // pencereler + balkon kapısı
  tag(windowX(wt.x0, wt.x1, wt.sill, wt.head, -T / 2), 'window');
  tag(windowZ(wr.z0, wr.z1, wr.sill, wr.head, W + T / 2), 'window');
  tag(balconyDoor(), 'window');
  tag(entryDoor(), 'door');
  return g;
}

function frameRing(w, h, p, mat) {
  const s = new THREE.Shape(); s.moveTo(0, 0); s.lineTo(w, 0); s.lineTo(w, h); s.lineTo(0, h); s.lineTo(0, 0);
  const hole = new THREE.Path(); hole.moveTo(p, p); hole.lineTo(p, h - p); hole.lineTo(w - p, h - p); hole.lineTo(w - p, p); hole.lineTo(p, p);
  s.holes.push(hole);
  const geo = new THREE.ExtrudeGeometry(s, { depth: 7, bevelEnabled: false }); geo.translate(-w / 2, 0, -3.5);
  const m = new THREE.Mesh(geo, mat); m.castShadow = true; return m;
}
function sash(w, h) { // tek kanat: çerçeve + cam (x-y düzleminde, merkez alt)
  const g = new THREE.Group();
  g.add(frameRing(w, h, 7, M.pvc));
  const gl = new THREE.Mesh(new THREE.PlaneGeometry(w - 14, h - 14), M.glass); gl.position.y = h / 2; g.add(gl);
  return g;
}
function windowX(x0, x1, y0, y1, z) {
  const g = new THREE.Group(); const w = x1 - x0, h = y1 - y0;
  const a = sash(w / 2, h); a.position.set(x0 + w / 4, y0, z); g.add(a);
  const b = sash(w / 2, h); b.position.set(x0 + 3 * w / 4, y0, z); g.add(b);
  g.add(box(x0 - 2, x1 + 2, y0 - 3, y0, z - 2, z + 16, M.white)); // mermer denizlik
  return g;
}
function windowZ(z0, z1, y0, y1, x) {
  const g = new THREE.Group(); const w = z1 - z0, h = y1 - y0;
  const a = sash(w, h); a.rotation.y = Math.PI / 2; a.position.set(x, y0, (z0 + z1) / 2); g.add(a);
  g.add(box(x - 16, x + 2, y0 - 3, y0, z0 - 2, z1 + 2, M.white));
  return g;
}
function balconyDoor() {
  const { z0, z1, head } = R.balcony; const g = new THREE.Group(); const x = R.W + R.T / 2;
  const s = sash(z1 - z0, head); s.rotation.y = Math.PI / 2; s.position.set(x, 0, (z0 + z1) / 2); g.add(s);
  g.add(box(x - 4, x + 4, 0, 85, z0 + 7, z1 - 7, M.pvc)); // alt panel
  g.add(box(x - 7, x - 3.5, 100, 103, z0 + 4, z0 + 16, M.brass)); // kol
  return g;
}
function entryDoor() {
  const { x0, x1, head } = R.entry; const g = new THREE.Group(); const z = R.L + R.T / 2;
  g.add(box(x0, x0 + 5, 0, head, z - 11, z + 11, M.door));
  g.add(box(x1 - 5, x1, 0, head, z - 11, z + 11, M.door));
  g.add(box(x0, x1, head - 5, head, z - 11, z + 11, M.door));
  // kanat kapalı — kasaya menteşeli (x=5)
  const leaf = box(0, 80, 0, head - 6, -2, 2, M.door); leaf.position.set(40, (head - 6) / 2, 0);
  const piv = new THREE.Group(); piv.position.set(x0 + 5, 0, z - 9); piv.rotation.y = 0; piv.add(leaf);
  const h = box(70, 78, 98, 101, -5, -2, M.brass); piv.add(h);
  g.add(piv);
  return g;
}

// ---------- MOBİLYALAR ----------
export const FURN = {
  yatak: { ad: 'Yatak (baza + başlık)', olcu: '146 × 198 cm, başlık h:105 — şilte 140×190', fn: bed },
  komodin: { ad: 'Dar komodin', olcu: '40 × 30 × 52 cm', fn: nightstand },
  gardirop: { ad: 'Gardırop (2 kapaklı)', olcu: '78 × 60 × 215 cm (kiriş altı 220\'ye göre)', fn: wardrobe },
  sifonyer: { ad: 'Şifonyer + ayna', olcu: '75 × 40 × 78 cm, ayna 55 × 80', fn: dresser },
  hali: { ad: 'Halı', olcu: '110 × 140 cm', fn: rug },
  aydinlatma: { ad: 'Aydınlatma', olcu: 'Ø45 sarkıt + 2 aplik', fn: lights },
  perde: { ad: 'Tül perdeler', olcu: '2 pencere', fn: curtains },
  radyator: { ad: 'Panel radyatör', olcu: '60 × 60 cm', fn: radiator },
  bitki: { ad: 'Saksı bitki', olcu: 'Ø30, h:110', fn: plant },
};

function bed() {
  const g = new THREE.Group(); g.name = 'yatak';
  // başlık: x 0-6, z 32-176
  g.add(box(0, 6, 25, 105, 32, 176, M.greige, 3));
  for (let i = 0; i < 6; i++) { const z = 34 + i * 23.3; g.add(box(5, 9, 30, 102, z, z + 22, M.greige, 2)); }
  // baza
  g.add(box(9, 198, 10, 34, 33, 175, M.greige, 3));
  [[14, 38], [14, 170], [193, 38], [193, 170]].forEach(([x, z]) => g.add(cyl(x, z, 0, 10, 2.2, M.oakDark)));
  // şilte
  g.add(box(10, 197, 34, 56, 34, 174, M.linen, 5));
  // nevresim + yatak örtüsü
  g.add(box(62, 198.5, 54, 60, 33, 175, M.linen, 3));
  g.add(box(150, 199, 56.5, 61, 32.5, 175.5, M.sage, 2));
  // yastıklar
  g.add(box(12, 30, 56, 74, 38, 102, M.linen, 7)); g.add(box(12, 30, 56, 74, 106, 170, M.linen, 7));
  g.add(box(28, 40, 56, 70, 50, 90, M.terra, 5)); g.add(box(28, 40, 56, 70, 118, 158, M.sage, 5));
  return g;
}
function nightstand() {
  const g = new THREE.Group(); g.name = 'komodin';
  g.add(box(14.5, 53.5, 10, 52, 0.5, 30, M.oak, 1));
  g.add(box(16, 52, 32, 48, 29.5, 31, M.oak, 0.5));
  g.add(box(30, 38, 39, 41, 31, 32.5, M.brass));
  [[17, 4], [51, 4], [17, 27], [51, 27]].forEach(([x, z]) => g.add(cyl(x, z, 0, 10, 1.2, M.black)));
  // masa lambası
  g.add(cyl(26, 14, 52, 54, 6, M.brass)); g.add(cyl(26, 14, 54, 72, 0.8, M.brass));
  const sh = cyl(26, 14, 70, 84, 9, M.linen, 24, 6); sh.material = M.lampGlow; g.add(sh);
  return g;
}
function wardrobe() {
  const g = new THREE.Group(); g.name = 'gardirop';
  // gövde x 206-266, z 184-262, h 215 (ön yüz x=206)
  g.add(box(208, 266, 0, 215, 184, 262, M.white));
  g.add(box(206, 208, 8, 214, 184.5, 222.8, M.white, 0.6));
  g.add(box(206, 208, 8, 214, 223.2, 261.5, M.white, 0.6));
  g.add(box(206, 208, 0, 8, 186, 260, M.oakDark)); // baza
  g.add(box(203.5, 206, 90, 150, 220, 221.5, M.oak)); g.add(box(203.5, 206, 90, 150, 224.5, 226, M.oak));
  // kapak üstünde ayna
  g.add(box(205.6, 206, 40, 190, 230, 255, M.mirror));
  return g;
}
function dresser() {
  const g = new THREE.Group(); g.name = 'sifonyer';
  g.add(box(92, 167, 10, 78, 222, 262, M.oak, 1));
  for (let i = 0; i < 3; i++) {
    const y0 = 13 + i * 21.5;
    g.add(box(93.5, 165.5, y0, y0 + 20.5, 221.2, 222.2, M.oak, 0.4));
    g.add(box(118, 141, y0 + 15, y0 + 16.5, 220, 221.2, M.brass));
  }
  [[96, 258], [163, 258], [96, 226], [163, 226]].forEach(([x, z]) => g.add(cyl(x, z, 0, 10, 1.4, M.black)));
  // ayna (yuvarlatılmış)
  const mg = new RoundedBoxGeometry(55, 80, 1.5, 4, 12);
  const mi = new THREE.Mesh(mg, M.mirror); mi.position.set(129.5, 135, 261); g.add(mi);
  const mf = new THREE.Mesh(new RoundedBoxGeometry(58, 83, 1.2, 4, 13), M.oak); mf.position.set(129.5, 135, 261.6); g.add(mf);
  // üst aksesuar
  g.add(cyl(105, 245, 78, 96, 5, M.pot)); g.add(cyl(155, 242, 78, 81, 7, M.brass));
  return g;
}
function rug() {
  const g = new THREE.Group(); g.name = 'hali';
  const m = new THREE.Mesh(new THREE.BoxGeometry(110, 1, 140), M.rug); m.position.set(195, 0.5, 106);
  m.material.map.repeat.set(1, 1); m.receiveShadow = true; g.add(m); return g;
}
function lights() {
  const g = new THREE.Group(); g.name = 'aydinlatma';
  // sarkıt (kirişler arası, oda ortası)
  g.add(cyl(133, 131, R.H - 0.5, R.H, 6, M.white));
  g.add(cyl(133, 131, 225, R.H, 0.3, M.black));
  const shade = new THREE.Mesh(new THREE.SphereGeometry(22, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2), new THREE.MeshStandardMaterial({ color: 0xe3d6c0, roughness: 0.9, side: THREE.DoubleSide }));
  shade.position.set(133, 205, 131); shade.scale.y = 0.9; g.add(shade);
  const bulb = new THREE.Mesh(new THREE.SphereGeometry(4, 16, 8), M.lampGlow); bulb.position.set(133, 205, 131); g.add(bulb);
  // başlık üstü aplikler
  [60, 148].forEach(z => {
    g.add(box(0, 3, 128, 140, z - 4, z + 4, M.brass));
    g.add(box(3, 18, 135, 137, z - 1, z + 1, M.brass));
    const s = cyl(20, z, 120, 136, 7, M.lampGlow, 20, 4); g.add(s);
  });
  return g;
}
function curtains() {
  const g = new THREE.Group(); g.name = 'perde';
  const pleat = (len, h) => {
    const geo = new THREE.PlaneGeometry(len, h, 48, 1); const p = geo.attributes.position;
    for (let i = 0; i < p.count; i++) p.setZ(i, Math.sin(p.getX(i) * 0.9) * 2.2);
    geo.computeVertexNormals(); const m = new THREE.Mesh(geo, M.curtain); m.castShadow = true; return m;
  };
  // üst pencere: iki yanda toplanmış tül
  [[50, 30], [180, 30]].forEach(([cx, w]) => { const c = pleat(w, 205); c.position.set(cx, 113, 5); g.add(c); });
  const rod = new THREE.Mesh(new THREE.CylinderGeometry(1, 1, 180, 12), M.brass); rod.rotation.z = Math.PI / 2; rod.position.set(115, 216, 5); g.add(rod);
  // sağ pencere + balkon kapısı: tek yanda toplanmış
  const c2 = pleat(36, 205); c2.rotation.y = -Math.PI / 2; c2.position.set(R.W - 5, 113, 58); g.add(c2);
  const rod2 = new THREE.Mesh(new THREE.CylinderGeometry(1, 1, 150, 12), M.brass); rod2.rotation.x = Math.PI / 2; rod2.position.set(R.W - 5, 216, 115); g.add(rod2);
  return g;
}
function radiator() {
  const g = new THREE.Group(); g.name = 'radyator';
  for (let i = 0; i < 15; i++) g.add(box(86 + i * 4, 89 + i * 4, 15, 75, 3, 10, M.radiator));
  return g;
}
function plant() {
  const g = new THREE.Group(); g.name = 'bitki';
  const x = 232, z = 72;
  g.add(cyl(x, z, 0, 32, 15, M.pot, 28, 17));
  const leafMat = M.leaf;
  for (let i = 0; i < 14; i++) {
    const l = new THREE.Mesh(new THREE.SphereGeometry(10, 12, 8), leafMat);
    const a = i * 2.4, r = 6 + (i % 4) * 3;
    l.scale.set(0.5, 1.6, 0.18); l.position.set(x + Math.cos(a) * r, 55 + (i % 5) * 11, z + Math.sin(a) * r);
    l.rotation.set(Math.sin(a) * 0.6, a, Math.cos(a) * 0.6); l.castShadow = true; g.add(l);
  }
  g.add(cyl(x, z, 30, 75, 0.8, M.oakDark));
  return g;
}

export function buildFurniture(only) {
  mats();
  const g = new THREE.Group(); g.name = 'mobilya';
  for (const [k, v] of Object.entries(FURN)) { if (only && only !== k) continue; const o = v.fn(); o.userData.key = k; g.add(o); }
  g.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } });
  return g;
}

export function addLights(scene, { interior = true } = {}) {
  scene.add(new THREE.HemisphereLight(0xfff8ee, 0xb8a58c, 0.55));
  const sun = new THREE.DirectionalLight(0xfff0d8, 3.2);
  sun.position.set(R.W + 380, 330, -260); sun.target.position.set(120, 0, 120);
  sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
  Object.assign(sun.shadow.camera, { left: -350, right: 350, top: 350, bottom: -350, near: 10, far: 1400 });
  sun.shadow.bias = -0.0005; sun.shadow.normalBias = 0.6;
  scene.add(sun, sun.target);
  if (interior) {
    const p = new THREE.PointLight(0xffd9a8, 9000, 0, 1.6); p.position.set(133, 195, 131); scene.add(p);
    const p2 = new THREE.PointLight(0xffd9a8, 1500, 0, 1.8); p2.position.set(30, 120, 104); scene.add(p2);
  }
}
