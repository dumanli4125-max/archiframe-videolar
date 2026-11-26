import sys
import numpy as np
from audio_kit import Mix

D = 60.5
m = Mix(D=D)
# anlatım (scene.html ile aynı başlangıçlar)
VO = [(0.3,'l01'),(3.9,'l02'),(8.8,'l03'),(13.9,'l04'),(17.6,'l05'),(21.8,'l06'),
      (26.6,'l07'),(32.3,'l08'),(38.9,'l09'),(42.9,'l10'),(47.4,'l11'),(54.3,'l12')]
for st, n in VO: m.vo(f'seslendirme/{n}.wav', st)
m.pad(gain=0.045, swell_from=42)
# kanca: beğeniler, sonra kadraj kararır
for k in [0.5, 0.8, 1.1, 1.4]: m.ping(k, gain=0.05)
m.note(0.4, 523.3, g=0.05, dur=1.5); m.note(2.8, 220, g=0.06, dur=1.8)
m.whoosh(2.65, 0.4, 0.07)
# eve giriş, eşyalar
m.click(3.95, gain=0.12)
m.steps(4.0, 6.3, rate=0.36, gain=0.12)
for t0 in [5.4, 7.5, 9.7]: m.thud(t0, f=70, gain=0.1)
for t0 in [10.9, 11.9, 12.6]: m.tick(t0, gain=0.08)
m.note(9.8, 246.9, g=0.05, dur=2); m.note(12.7, 220, g=0.05, dur=2)
# fotoğraf: zoom, odak, deklanşör
m.whoosh(15.0, 0.7, 0.08)
m.ping(16.1, gain=0.06)
m.tick(17.9, gain=0.06); m.tick(19.1, gain=0.06)
m.click(20.0, gain=0.4); m.click(20.07, gain=0.25); m.whoosh(19.95, 0.25, 0.06)
m.ding(20.7, gain=0.08)
# kalpler + yorumlar
for k in np.arange(21.9, 23.4, 0.13): m.ping(k, gain=0.035)
m.ping(24.0, gain=0.07); m.ping(24.8, gain=0.07)
for t0, f in [(22.0, 523.3), (22.6, 659.3), (23.2, 784)]: m.note(t0, f, g=0.045, dur=1.2)
# akış kayıyor
for t0 in [26.9, 29.4, 30.6]: m.whoosh(t0, 0.55, 0.08)
for t0, f in [(28.4, 587.3), (29.95, 659.3), (31.15, 784)]: m.note(t0, f, g=0.05, dur=1.3)
# kıyas: eşyalar, omuz düşer
for t0 in [34.4, 35.2, 36.0]: m.thud(t0, f=65, gain=0.1)
m.thud(37.3, f=45, gain=0.3)
for t0, f in [(32.5, 293.7), (35.0, 261.6), (37.3, 220)]: m.note(t0, f, g=0.06, dur=2.5)
# dönüm: duraklat, kadraj açılır
m.click(38.95, gain=0.2); m.thud(39.0, f=55, gain=0.2)
m.whoosh(41.2, 1.3, 0.12)
m.thud(43.7, f=60, gain=0.12); m.thud(45.1, f=60, gain=0.12)
for t0, f in [(42.6, 329.6), (44.0, 293.7), (46.1, 246.9)]: m.note(t0, f, g=0.065, dur=2.5)
# gerçek: taslak silinir, panel, VS
m.click(48.4, gain=0.15); m.whoosh(48.9, 0.6, 0.08)
m.whoosh(49.8, 0.4, 0.06)
m.thud(52.7, f=50, gain=0.2); m.ping(52.75, gain=0.06)
# final
for t0, f in [(54.4, 261.6), (56.2, 329.6), (57.2, 392), (58.0, 523.3)]: m.note(t0, f, g=0.07, dur=2.5)
m.whoosh(56.15, 0.9, 0.07)
m.write(sys.argv[1])
