import sys
import numpy as np
from audio_kit import Mix

D = 60.5
m = Mix(D=D)
# anlatım (scene.html ile aynı başlangıçlar)
VO = [(0.3,'l01'),(5.9,'l02'),(10.2,'l03'),(14.1,'l04'),(18.9,'l05'),(24.9,'l06'),
      (29.4,'l07'),(33.9,'l08'),(39.4,'l09'),(44.3,'l10'),(48.7,'l11'),(52.0,'l12')]
for st, n in VO: m.vo(f'seslendirme/{n}.wav', st)
m.pad(gain=0.045, swell_from=44)
# kanca: çipler, yıldız + fiyatlar
m.click(0.45, 0.12); m.click(1.4, 0.12)
m.whoosh(2.6, 0.4, 0.06)
m.thud(5.15, f=60, gain=0.25); m.ding(5.2, gain=0.12); m.ping(5.35, gain=0.08)
m.whoosh(5.6, 0.4, 0.08)
# fabrika: makine tıkırtısı + bant
for k in np.arange(6.0, 18.6, 0.11): m.tick(k, gain=0.035)
m.tension(6.0, 18.6, gain=0.015)
m.ping(12.0, gain=0.05)
m.whoosh(14.9, 0.4, 0.06)
for ts in (15.9, 17.9): m.thud(ts, f=70, gain=0.3); m.click(ts, 0.2); m.ping(ts + 0.05, gain=0.06)
for i in range(6, 19): m.thud(i + 0.26, f=90, gain=0.05)  # sepete düşen tişörtler
m.whoosh(18.5, 0.4, 0.08)
# vitrin: fiyatlar
m.ding(21.3, gain=0.1)
m.ding(23.65, gain=0.13); m.note(23.7, 659.3, g=0.05, dur=1.5)
m.thud(25.4, f=55, gain=0.22); m.ping(25.45, gain=0.08)
m.steps(25.9, 26.9, rate=0.3, gain=0.1)
m.note(27.3, 523.3, g=0.06, dur=1.4); m.note(27.55, 659.3, g=0.06, dur=1.4)
m.buzz(28.3, 0.5); m.ping(28.4, gain=0.1)
m.whoosh(29.0, 0.4, 0.08)
# sokak
m.steps(29.4, 33.6, rate=0.27, gain=0.12)
m.ping(32.4, gain=0.07)
m.whoosh(33.55, 0.4, 0.08)
# ev: dolap, ekstre
m.steps(33.8, 34.6, rate=0.3, gain=0.1)
m.whoosh(34.9, 0.6, 0.07); m.click(34.9, 0.15)
for i in range(3): m.click(38.0 + i * 0.2, 0.1)
m.thud(38.4, f=45, gain=0.2)
m.note(38.2, 220, g=0.06, dur=2.5)
m.whoosh(39.05, 0.4, 0.07)
# işçinin payı
for k in np.arange(39.6, 43.0, 0.14): m.tick(k, gain=0.025)
m.click(42.0, 0.15); m.ping(42.95, gain=0.05)
for t0, f in [(40.0,329.6),(42.9,261.6),(44.4,293.7),(45.5,329.6),(46.4,293.7),(47.4,220)]: m.note(t0, f, g=0.06, dur=2.4)
m.whoosh(47.3, 0.5, 0.06); m.thud(47.45, f=50, gain=0.22)
m.whoosh(48.35, 0.4, 0.07)
m.ping(50.4, gain=0.08)
# final: etiket döner
m.whoosh(51.4, 0.6, 0.06)
m.whoosh(54.3, 0.5, 0.07); m.click(54.65, 0.15)
for t0, f in [(52.2,261.6),(53.9,329.6),(55.5,392),(56.5,523.3)]: m.note(t0, f, g=0.07, dur=2.6)
m.ding(56.6, gain=0.08)
m.write(sys.argv[1])
