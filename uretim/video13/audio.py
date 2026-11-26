import sys
import numpy as np
from audio_kit import Mix

# 13 — Oyuncak yağmuru. VO başlangıçları scene.html ile AYNI.
D = 61.5
m = Mix(D=D)
VO = [(0.3,'l01'),(5.0,'l02'),(10.2,'l03'),(15.9,'l04'),(20.4,'l05'),(26.1,'l06'),
      (30.3,'l07'),(34.2,'l08'),(39.5,'l09'),(43.1,'l10'),(48.2,'l11'),(53.4,'l12')]
for st, n in VO: m.vo(f'seslendirme/{n}.wav', st)
m.pad(gain=0.045, swell_from=43)

# saat tıkırtısı (ilk akşam ve kanca: saniyede bir)
for k in np.arange(0.5, 26.0, 1.0): m.tick(k, gain=0.035)
m.note(6.7, 659.3, g=0.05, dur=1.6)            # "dokuz": 21:00
# kapı + adımlar + çocuk koşar
m.click(7.45, 0.18)
m.steps(7.7, 9.3, rate=0.4, gain=0.12)
m.steps(10.65, 11.75, rate=0.18, gain=0.08, f=110)
m.whoosh(11.85, 0.35, 0.07)
# "Bir araba!" — paket açılır, sevinç
m.ding(13.45, gain=0.12)
for t0, f in [(13.9,523.3),(14.2,659.3),(14.5,784.0)]: m.note(t0, f, g=0.06, dur=1.6)
# telefon, laptop
m.ping(17.0, gain=0.08)
m.keyboard(19.2, 25.9, gain=0.03)
m.note(25.0, 220.0, g=0.06, dur=2.2)           # "Şimdi değil."

# günler akar: yağan kutular + hızlanan saat
TOYS = [27.1, 28.3, 29.3]
PILE = [30.6,31.0,31.45,31.9,32.35,32.8,33.3,34.5,34.95,35.4,35.8,36.2]
for tf in TOYS:
    m.whoosh(tf - 0.5, 0.5, 0.07); m.thud(tf, f=70, gain=0.18); m.ding(tf + 0.25, gain=0.07)
for tf in PILE:
    m.whoosh(tf - 0.45, 0.4, 0.05); m.thud(tf, f=60, gain=0.13)
def rate(t):
    s = lambda a, b, x: (lambda u: u*u*(3-2*u))(min(1, max(0, (x-a)/(b-a))))
    return 0.5 + 189.5*s(26.1, 30.5, t)*(1 - s(37.5, 41.5, t))
k = 26.3
while k < 42.5:
    m.tick(k, gain=0.03)
    k += max(0.07, min(1.0, 25.0/rate(k)))
m.keyboard(26.1, 39.2, gain=0.02)
m.tension(37.6, 42.6, gain=0.035)
for t0, f in [(39.6,246.9),(41.4,196.0)]: m.note(t0, f, g=0.06, dur=2.6)

# dönüm: eli boş, yere oturur, top
m.click(43.05, 0.18)
m.steps(43.3, 44.8, rate=0.4, gain=0.12)
m.thud(45.8, f=55, gain=0.15)
for a, b in [(47.2,48.1),(50.0,50.85),(51.6,52.4),(53.2,54.0),(55.0,55.8),(56.6,57.4),(58.4,59.2)]:
    for x in np.arange(a, b, 0.11): m.click(x, 0.04)
    m.thud(b, f=90, gain=0.06)
for t0, f in [(48.6,523.3),(48.85,659.3),(49.1,784.0),(49.35,1046.5)]: m.note(t0, f, g=0.06, dur=1.4)
for k in np.arange(43.5, 52.0, 1.0): m.tick(k, gain=0.03)
for t0, f in [(50.5,392.0),(52.2,329.6),(53.6,261.6),(55.3,329.6),(56.8,392.0),(58.0,523.3)]:
    m.note(t0, f, g=0.07, dur=2.6)
m.write(sys.argv[1])
