import sys
import numpy as np
from audio_kit import Mix

D = 60.5
m = Mix(D=D)
# İngilizce anlatım (Kyle, speed 1.0; scene.html ile aynı başlangıçlar). l02 %5, l04/l06 %8, l08 %2, l10 %7 hızlı
VO = [(0.3,'l01',1),(3.9,'l02',1.05),(8.8,'l03',1),(13.9,'l04',1.08),(17.6,'l05',1),(21.8,'l06',1.08),
      (26.6,'l07',1),(32.3,'l08',1.02),(38.9,'l09',1),(42.9,'l10',1.07),(47.4,'l11',1),(54.3,'l12',1)]
for st, n, tp in VO: m.vo(f'seslendirme_en/{n}.wav', st, tempo=tp)
m.pad(gain=0.045, swell_from=42)
# kanca: beğeniler, sonra kadraj kararır
for k in [0.5, 0.8, 1.1, 1.4]: m.ping(k, gain=0.05)
m.note(0.4, 523.3, g=0.05, dur=1.5); m.note(2.8, 220, g=0.06, dur=1.8)
m.whoosh(2.65, 0.4, 0.07)
# eve giriş, eşyalar
m.click(3.95, gain=0.12)
m.steps(4.0, 6.3, rate=0.36, gain=0.12)
for t0 in [5.6, 7.5, 9.7]: m.thud(t0, f=70, gain=0.1)
for t0 in [10.8, 11.6, 12.2]: m.tick(t0, gain=0.08)
m.note(9.8, 246.9, g=0.05, dur=2); m.note(12.3, 220, g=0.05, dur=2)
# fotoğraf: zoom, odak, deklanşör
m.whoosh(15.0, 0.7, 0.08)
m.ping(16.1, gain=0.06)
m.tick(17.9, gain=0.06); m.tick(19.1, gain=0.06)
m.click(19.75, gain=0.4); m.click(19.82, gain=0.25); m.whoosh(19.7, 0.25, 0.06)
m.ding(20.5, gain=0.08)
# kalpler + yorumlar
for k in np.arange(21.9, 23.4, 0.13): m.ping(k, gain=0.035)
m.ping(24.1, gain=0.07); m.ping(25.3, gain=0.07)
for t0, f in [(22.0, 523.3), (22.6, 659.3), (23.2, 784)]: m.note(t0, f, g=0.045, dur=1.2)
# akış kayıyor
for t0 in [27.0, 29.75, 30.85]: m.whoosh(t0, 0.55, 0.08)
for t0, f in [(28.2, 587.3), (30.3, 659.3), (31.4, 784)]: m.note(t0, f, g=0.05, dur=1.3)
# kıyas: eşyalar, omuz düşer
for t0 in [34.85, 35.8, 36.7]: m.thud(t0, f=65, gain=0.1)
m.thud(38.35, f=45, gain=0.3)
for t0, f in [(32.5, 293.7), (35.6, 261.6), (38.35, 220)]: m.note(t0, f, g=0.06, dur=2.5)
# dönüm: duraklat, kadraj açılır
m.click(38.95, gain=0.2); m.thud(39.0, f=55, gain=0.2)
m.whoosh(41.9, 1.3, 0.12)
m.thud(44.3, f=60, gain=0.12); m.thud(45.5, f=60, gain=0.12)
for t0, f in [(42.6, 329.6), (44.3, 293.7), (46.6, 246.9)]: m.note(t0, f, g=0.065, dur=2.5)
# gerçek: taslak silinir, panel, VS
m.click(48.4, gain=0.15); m.whoosh(48.9, 0.6, 0.08)
m.whoosh(49.8, 0.4, 0.06)
m.thud(52.35, f=50, gain=0.2); m.ping(52.4, gain=0.06)
# final
for t0, f in [(54.4, 261.6), (56.2, 329.6), (57.2, 392), (58.0, 523.3)]: m.note(t0, f, g=0.07, dur=2.5)
m.whoosh(56.15, 0.9, 0.07)
m.write(sys.argv[1])
