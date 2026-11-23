// 2B tefriş planı (SVG) — ölçüler room.js ile aynı
import fs from 'fs';
const k = 2.6, ox = 200, oy = 210; // px/cm, kenar boşluğu
const X = x => ox + x * k, Y = z => oy + z * k;
let o = [], arcs = [];
const rect = (x0, z0, x1, z1, st) => o.push(`<rect x="${X(x0)}" y="${Y(z0)}" width="${(x1 - x0) * k}" height="${(z1 - z0) * k}" ${st}/>`);
const txt = (x, z, t, st = '') => o.push(`<text x="${X(x)}" y="${Y(z)}" ${st}>${t}</text>`);
const line = (x0, z0, x1, z1, st) => o.push(`<line x1="${X(x0)}" y1="${Y(z0)}" x2="${X(x1)}" y2="${Y(z1)}" ${st}/>`);
const WALL = 'fill="#3d3a36"', FUR = 'fill="#f3ead9" stroke="#8a6a45" stroke-width="2"';
const dimH = (x0, x1, z, t) => { line(x0, z, x1, z, 'class="d"'); [x0, x1].forEach(x => line(x - 2, z + 2, x + 2, z - 2, 'class="dt"')); txt((x0 + x1) / 2, z - 3, t, 'class="dl" text-anchor="middle"'); };
const dimV = (z0, z1, x, t) => { line(x, z0, x, z1, 'class="d"'); [z0, z1].forEach(z => line(x - 2, z + 2, x + 2, z - 2, 'class="dt"')); o.push(`<text class="dl" text-anchor="middle" transform="translate(${X(x) - 8},${Y((z0 + z1) / 2)}) rotate(-90)">${t}</text>`); };

// döşeme
rect(0, 0, 277, 262, 'fill="#efe2cc"'); rect(0, 262, 90, 340, 'fill="#efe2cc"');
// kirişler (kesikli)
rect(0, 0, 266, 25, 'class="beam"'); rect(0, 237, 266, 262, 'class="beam"');
txt(170, 15, 'KİRİŞ — alt kotu 220', 'class="bl"'); txt(190, 252, 'KİRİŞ — alt kotu 220', 'class="bl"');
// duvarlar
rect(-20, -20, 286, 0, WALL); rect(-20, 0, 0, 340, WALL);
rect(266, -20, 286, 45, WALL); rect(266, 182, 286, 182, WALL); rect(277, 182, 286, 242, WALL); rect(266, 242, 286, 282, WALL);
rect(90, 262, 286, 282, WALL); rect(90, 282, 105, 340, WALL);
rect(0, 0, 14, 32, 'fill="url(#h)" stroke="#3d3a36" stroke-width="2"'); rect(246, 0, 266, 40, WALL);
// pencereler
rect(75, -20, 155, 0, 'fill="#fff" stroke="#3d3a36" stroke-width="1.5"'); line(75, -10, 155, -10, 'stroke="#5a8db3" stroke-width="3"');
rect(266, 45, 286, 100, 'fill="#fff" stroke="#3d3a36" stroke-width="1.5"'); line(276, 45, 276, 100, 'stroke="#5a8db3" stroke-width="3"');
rect(266, 100, 286, 182, 'fill="#fff" stroke="#3d3a36" stroke-width="1.5"');
// balkon kapısı yayı (menteşe 266,182)
line(266, 182, 186, 182, 'stroke="#3d3a36" stroke-width="3"');
arcs.push(`<path d="M${X(186)},${Y(182)} A${80 * k},${80 * k} 0 0 1 ${X(266)},${Y(102)}" class="arc"/>`);
// oda kapısı (menteşe 5,262 — içeri, sol duvara doğru)
line(5, 262, 5, 182, 'stroke="#3d3a36" stroke-width="3"');
arcs.push(`<path d="M${X(5)},${Y(182)} A${80 * k},${80 * k} 0 0 1 ${X(85)},${Y(262)}" class="arc"/>`);
// gardırop kapak yayları
[[206, 184, 1], [206, 262, -1]].forEach(([x, z, s]) => arcs.push(`<path d="M${X(x)},${Y(z + s * 39)} A${39 * k},${39 * k} 0 0 ${s > 0 ? 1 : 0} ${X(x - 39)},${Y(z)}" class="arc2"/>`));
// halı
rect(140, 36, 250, 176, 'fill="#e4d9c6" stroke="#b9a586" stroke-width="2" stroke-dasharray="2 4"');
// mobilyalar
rect(0, 32, 6, 176, 'fill="#b5ab9d" stroke="#6d6458" stroke-width="2"');
rect(6, 33, 198, 175, FUR); rect(12, 38, 30, 102, 'fill="#fff" stroke="#8a6a45"'); rect(12, 106, 30, 170, 'fill="#fff" stroke="#8a6a45"');
line(62, 33, 62, 175, 'stroke="#8a6a45" stroke-dasharray="5 4"'); rect(150, 33, 198, 175, 'fill="#c9d3c4" stroke="#8a6a45" stroke-width="2"');
txt(100, 100, 'YATAK', 'class="fl" text-anchor="middle"'); txt(100, 112, '140×190', 'class="fs" text-anchor="middle"');
rect(14, 0, 54, 30, FUR); txt(34, 18, 'KOMODİN', 'class="fs" text-anchor="middle"');
rect(206, 184, 266, 262, 'fill="#fbfaf7" stroke="#8a6a45" stroke-width="2"'); line(206, 223, 266, 223, 'stroke="#8a6a45"');
txt(236, 226, 'GARDIROP', 'class="fs" text-anchor="middle"'); txt(236, 236, '78×60 h215', 'class="fs" text-anchor="middle"');
rect(92, 222, 167, 262, FUR); txt(129.5, 243, 'ŞİFONYER', 'class="fs" text-anchor="middle"'); txt(129.5, 253, '75×40', 'class="fs" text-anchor="middle"');
rect(86, 3, 146, 10, 'fill="#fff" stroke="#888"'); txt(116, 31, 'radyatör', 'class="fs" text-anchor="middle"');
o.push(`<circle cx="${X(232)}" cy="${Y(72)}" r="${15 * k}" fill="#cfdcc6" stroke="#5f7a52" stroke-width="2"/>`);
o.push(`<circle cx="${X(133)}" cy="${Y(131)}" r="${22 * k}" fill="none" stroke="#c8a463" stroke-width="2" stroke-dasharray="3 3"/>`);
// etiketler
txt(226, 145, 'BALKON KAPISI 80', 'class="fs" text-anchor="end"'); txt(45, 230, 'ODA KAPISI 80', 'class="fs" text-anchor="middle"');
txt(45, 310, 'KORİDOR', 'class="fl" text-anchor="middle"'); txt(115, -26, 'PENCERE 80', 'class="fs" text-anchor="middle"');
o.push(`<text class="fs" text-anchor="middle" transform="translate(${X(296)},${Y(72)}) rotate(90)">PENCERE 55</text>`);
txt(290, 176, 'niş 60×11', 'class="fs"'); txt(-6, 50, '', '');
// ölçüler
dimH(0, 266, -42, '266'); dimV(0, 32, -36, '32'); dimV(32, 262, -36, '230'); dimV(182, 242, 318, '60');
dimV(0, 262, -52, '262');
const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${ox * 2 + 290 * k}" height="${oy + 380 * k}" viewBox="0 0 ${ox * 2 + 290 * k} ${oy + 380 * k}">
<defs><pattern id="h" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="8" height="8" fill="#fff"/><line x1="0" y1="0" x2="0" y2="8" stroke="#3d3a36" stroke-width="3"/></pattern></defs>
<style>text{font-family:Inter,Arial,sans-serif}.d{stroke:#7a3e1d;stroke-width:1.2}.dt{stroke:#7a3e1d;stroke-width:2}.dl{font-size:15px;fill:#7a3e1d;font-weight:600}
.fl{font-size:16px;font-weight:700;fill:#4a3a28}.fs{font-size:12px;fill:#4a3a28}.arc{fill:none;stroke:#3d3a36;stroke-width:1.3;stroke-dasharray:6 4}.arc2{fill:none;stroke:#8a6a45;stroke-width:1;stroke-dasharray:3 3}
.beam{fill:none;stroke:#9b8f80;stroke-width:1.5;stroke-dasharray:10 6}.bl{font-size:11px;fill:#8a7f70;font-style:italic}</style>
<rect width="100%" height="100%" fill="#fff"/>
<text x="${ox - 150}" y="44" style="font-size:24px;font-weight:700;fill:#2d2a26">YATAK ODASI — TEFRİŞ PLANI</text>
<text x="${ox - 150}" y="70" style="font-size:13px;fill:#6b645b">Ölçüler cm · Tavan 260 (varsayım) · Kiriş altı 220 · Kolon 14×32</text>
${o.join('\n')}
${arcs.join('\n')}
<text x="${ox - 150}" y="${oy + 380 * k - 30}" style="font-size:12px;fill:#6b645b">Balkon kapısı yatak ayakucunu teğet geçer (~85° açılır). Gardırop yüksekliği kiriş altına göre 215 cm.</text>
</svg>`;
fs.writeFileSync(process.argv[2], svg);
