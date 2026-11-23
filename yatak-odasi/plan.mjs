// 2B tefriş planı (SVG) — ölçüler room.js ile aynı
import fs from 'fs';
const k = 2.4, ox = 190, oy = 250; // px/cm, kenar boşluğu
const X = x => ox + x * k, Y = z => oy + z * k;
let o = [], arcs = [];
const rect = (x0, z0, x1, z1, st) => o.push(`<rect x="${X(x0)}" y="${Y(z0)}" width="${(x1 - x0) * k}" height="${(z1 - z0) * k}" ${st}/>`);
const txt = (x, z, t, st = '') => o.push(`<text x="${X(x)}" y="${Y(z)}" ${st}>${t}</text>`);
const line = (x0, z0, x1, z1, st) => o.push(`<line x1="${X(x0)}" y1="${Y(z0)}" x2="${X(x1)}" y2="${Y(z1)}" ${st}/>`);
const WALL = 'fill="#3d3a36"', FUR = 'fill="#f3ead9" stroke="#8a6a45" stroke-width="2"';
const dimH = (x0, x1, z, t) => { line(x0, z, x1, z, 'class="d"'); [x0, x1].forEach(x => line(x - 2, z + 2, x + 2, z - 2, 'class="dt"')); txt((x0 + x1) / 2, z - 3, t, 'class="dl" text-anchor="middle"'); };
const dimV = (z0, z1, x, t) => { line(x, z0, x, z1, 'class="d"'); [z0, z1].forEach(z => line(x - 2, z + 2, x + 2, z - 2, 'class="dt"')); o.push(`<text class="dl" text-anchor="middle" transform="translate(${X(x) - 8},${Y((z0 + z1) / 2)}) rotate(-90)">${t}</text>`); };

// döşeme
rect(0, 0, 392, 262, 'fill="#efe2cc"'); rect(0, 262, 100, 340, 'fill="#efe2cc"');
rect(0, 0, 381, 25, 'class="beam"'); rect(0, 237, 381, 262, 'class="beam"');
txt(225, 63, 'KİRİŞ — alt kotu 220', 'class="bl"'); txt(120, 252, 'KİRİŞ — alt kotu 220', 'class="bl"');
// duvarlar
rect(-20, -20, 401, 0, WALL); rect(-20, 0, 0, 340, WALL);
rect(381, -20, 401, 45, WALL); rect(392, 182, 401, 242, WALL); rect(381, 242, 401, 282, WALL);
rect(100, 262, 401, 282, WALL); rect(100, 282, 115, 340, WALL);
rect(0, 0, 14, 32, 'fill="url(#h)" stroke="#3d3a36" stroke-width="2"'); rect(361, 0, 381, 40, WALL);
// pencereler
rect(110, -20, 210, 0, 'fill="#fff" stroke="#3d3a36" stroke-width="1.5"'); line(110, -10, 210, -10, 'stroke="#5a8db3" stroke-width="3"');
rect(381, 45, 401, 100, 'fill="#fff" stroke="#3d3a36" stroke-width="1.5"'); line(391, 45, 391, 100, 'stroke="#5a8db3" stroke-width="3"');
rect(381, 100, 401, 182, 'fill="#fff" stroke="#3d3a36" stroke-width="1.5"');
line(381, 182, 301, 182, 'stroke="#3d3a36" stroke-width="3"');
arcs.push(`<path d="M${X(301)},${Y(182)} A${80 * k},${80 * k} 0 0 1 ${X(381)},${Y(102)}" class="arc"/>`);
// halı
rect(130, 70, 300, 190, 'fill="#e4d9c6" stroke="#b9a586" stroke-width="2" stroke-dasharray="2 4"');
// yatak
rect(0, 32, 6, 190, 'fill="#b5ab9d" stroke="#6d6458" stroke-width="2"');
rect(6, 33, 214, 189, FUR); rect(12, 41, 30, 108, 'fill="#fff" stroke="#8a6a45"'); rect(12, 114, 30, 181, 'fill="#fff" stroke="#8a6a45"');
line(70, 33, 70, 189, 'stroke="#8a6a45" stroke-dasharray="5 4"'); rect(165, 33, 214, 189, 'fill="#c9d3c4" stroke="#8a6a45" stroke-width="2"');
txt(110, 108, 'YATAK', 'class="fl" text-anchor="middle"'); txt(110, 120, '150×200', 'class="fs" text-anchor="middle"');
rect(14, 0, 59, 30, FUR); txt(36.5, 18, 'KOMODİN', 'class="fs" text-anchor="middle"');
rect(125, 3, 195, 10, 'fill="#fff" stroke="#888"'); txt(160, 22, 'radyatör', 'class="fs" text-anchor="middle"');
// masa + tabure
rect(235, 0, 355, 50, FUR); txt(295, 22, 'MAKYAJ / ÇALIŞMA', 'class="fs" text-anchor="middle"'); txt(295, 34, 'MASASI 120×50', 'class="fs" text-anchor="middle"');
o.push(`<circle cx="${X(295)}" cy="${Y(78)}" r="${18 * k}" fill="#d9d2c6" stroke="#8a6a45" stroke-width="2"/>`);
// gardırop (sürgü)
rect(216, 202, 381, 262, 'fill="#fbfaf7" stroke="#8a6a45" stroke-width="2"');
line(216, 200, 271, 200, 'stroke="#8a6a45" stroke-width="3"'); line(271, 198, 326, 198, 'stroke="#8a6a45" stroke-width="3"'); line(326, 200, 381, 200, 'stroke="#8a6a45" stroke-width="3"');
txt(298.5, 228, 'SÜRGÜ KAPAKLI GARDIROP', 'class="fs" text-anchor="middle"'); txt(298.5, 240, '165×62 h215', 'class="fs" text-anchor="middle"');
o.push(`<circle cx="${X(350)}" cy="${Y(75)}" r="${15 * k}" fill="#cfdcc6" stroke="#5f7a52" stroke-width="2"/>`);
o.push(`<circle cx="${X(190)}" cy="${Y(131)}" r="${22 * k}" fill="none" stroke="#c8a463" stroke-width="2" stroke-dasharray="3 3"/>`);
// etiketler
txt(340, 150, 'BALKON KAPISI 80', 'class="fs" text-anchor="middle"');
txt(50, 310, 'KORİDOR', 'class="fl" text-anchor="middle"'); txt(160, -26, 'PENCERE 100', 'class="fs" text-anchor="middle"');
o.push(`<text class="fs" text-anchor="middle" transform="translate(${X(411)},${Y(72)}) rotate(90)">PENCERE 55</text>`);
txt(405, 176, 'niş 60×11', 'class="fs"');
// ölçüler
dimH(0, 381, -60, '381'); dimH(0, 100, -42, '100 (koridor)'); dimH(100, 115, -42, '15'); dimH(115, 381, -42, '266');
dimH(0, 100, 352, '100'); dimH(100, 115, 352, '15');
line(100, -20, 100, -42, 'stroke="#7a3e1d" stroke-width="0.8" stroke-dasharray="2 4"'); line(115, -20, 115, -42, 'stroke="#7a3e1d" stroke-width="0.8" stroke-dasharray="2 4"');
dimV(0, 32, -36, '32'); dimV(32, 262, -36, '230'); dimV(0, 262, -54, '262'); dimV(182, 242, 432, '60');
const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${ox * 2 + 440 * k}" height="${oy + 380 * k}" viewBox="0 0 ${ox * 2 + 440 * k} ${oy + 380 * k}">
<defs><pattern id="h" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="8" height="8" fill="#fff"/><line x1="0" y1="0" x2="0" y2="8" stroke="#3d3a36" stroke-width="3"/></pattern></defs>
<style>text{font-family:Inter,Arial,sans-serif}.d{stroke:#7a3e1d;stroke-width:1.2}.dt{stroke:#7a3e1d;stroke-width:2}.dl{font-size:15px;fill:#7a3e1d;font-weight:600}
.fl{font-size:16px;font-weight:700;fill:#4a3a28}.fs{font-size:12px;fill:#4a3a28}.arc{fill:none;stroke:#3d3a36;stroke-width:1.3;stroke-dasharray:6 4}.arc2{fill:none;stroke:#8a6a45;stroke-width:1;stroke-dasharray:3 3}
.beam{fill:none;stroke:#9b8f80;stroke-width:1.5;stroke-dasharray:10 6}.bl{font-size:11px;fill:#8a7f70;font-style:italic}</style>
<rect width="100%" height="100%" fill="#fff"/>
<text x="${ox - 150}" y="44" style="font-size:24px;font-weight:700;fill:#2d2a26">YATAK ODASI — TEFRİŞ PLANI</text>
<text x="${ox - 150}" y="70" style="font-size:13px;fill:#6b645b">Ölçüler cm · Tavan 260 (varsayım) · Kiriş altı 220 · Kolon 14×32</text>
${o.join('\n')}
${arcs.join('\n')}
<text x="${ox - 150}" y="${oy + 380 * k - 30}" style="font-size:12px;fill:#6b645b">Oda genişliği = koridor 100 + koridor duvarı 15 + 266 = 381 cm. Gardırop yüksekliği kiriş altına (220) göre 215 cm.</text>
</svg>`;
fs.writeFileSync(process.argv[2], svg);
