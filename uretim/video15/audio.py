import sys
import numpy as np
from audio_kit import Mix, SR

# 15 — Balık mı, olta mı? VO başlangıçları scene.html ile AYNI.
D = 64.9
m = Mix(D=D)
VO = [(0.3,'l01',1.0),(4.3,'l02',1.07),(9.6,'l03',1.07),(14.6,'l04',1.07),(19.7,'l05',1.07),(25.9,'l06',1.07),
      (29.5,'l07',1.07),(34.8,'l08',1.07),(39.9,'l09',1.07),(45.8,'l10',1.07),(52.5,'l11',1.0),(56.6,'l12',1.0)]
for st, n, tp in VO: m.vo(f'seslendirme/{n}.wav', st, tempo=tp)
m.pad(gain=0.04, swell_from=45)

# deniz: yavaş dalgalanan yumuşatılmış gürültü (iskele sahneleri; oda sahnesinde kısık)
n = m.rng.standard_normal(m.N); k = int(0.004 * SR)
c = np.concatenate([[0], np.cumsum(n)]); waves = (c[k:] - c[:-k]) / k; waves = np.pad(waves, (0, m.N - len(waves)))
t = m.t
lfo = 0.55 + 0.45 * np.sin(2 * np.pi * 0.13 * t) * np.sin(2 * np.pi * 0.05 * t + 1)
room = ((t > 29.4) & (t < 34.7)).astype(float)
m.sfx += 0.10 * waves * lfo * (1 - 0.85 * room) * np.clip(t / 1.5, 0, 1)
# ateş çıtırtısı
for x in np.sort(m.rng.uniform(0, D - 3, 160)):
    if not (29.4 < x < 34.7) and x < 56.6: m.click(x, 0.035)

# kanca
m.note(2.2, 523.3, g=0.05, dur=1.4); m.ping(2.25, gain=0.05)   # "balık"
m.note(3.5, 659.3, g=0.05, dur=1.6)                              # "olta"
m.whoosh(4.0, 0.4, 0.06)
# her akşam aynı saat
m.note(5.23, 392.0, g=0.05, dur=1.6); m.tick(5.23, 0.08)
m.whoosh(7.6, 0.5, 0.08); m.thud(8.2, f=180, gain=0.07); m.whoosh(8.2, 0.3, 0.05)   # atış + suya düşüş
# genç gelir, aç
m.steps(9.7, 11.0, rate=0.36, gain=0.1, f=90)
m.thud(10.9, f=55, gain=0.12)
m.click(12.3, 0.12); m.click(12.45, 0.1)                         # kovada eşelenme
m.ding(12.78, gain=0.06); m.whoosh(13.75, 0.35, 0.05)
m.keyboard(15.0, 16.0, gain=0.025)                               # cızırtı
m.steps(17.05, 17.9, rate=0.34, gain=0.08, f=90)
m.note(17.78, 330.0, g=0.045, dur=1.6)
m.steps(18.55, 19.5, rate=0.34, gain=0.09, f=90)
# günler akar
for tt in [20.45, 21.29, 22.41]: m.ping(tt, gain=0.05); m.whoosh(tt + 0.15, 0.25, 0.04)
for kk in np.arange(23.75, 25.3, 0.25): m.tick(kk, gain=0.06)    # bekleyiş
m.ping(25.35, gain=0.04)
for t0, f in [(26.0, 293.7), (27.58, 246.9), (28.42, 220.0)]: m.note(t0, f, g=0.06, dur=2.2)
# sen de... (oda)
m.whoosh(29.35, 0.5, 0.07)
for tt in [30.43, 30.99, 31.56]: m.whoosh(tt - 0.05, 0.2, 0.05)  # takvim yaprağı
for tt in [30.71, 31.25, 31.8]: m.ping(tt + 0.3, gain=0.04)      # para
m.note(32.02, 196.0, g=0.06, dur=2.4); m.note(33.24, 174.6, g=0.06, dur=2.6)
m.whoosh(34.5, 0.5, 0.07)
# dönüm
m.steps(34.85, 35.8, rate=0.38, gain=0.09, f=90)
m.thud(36.15, f=120, gain=0.1); m.click(36.15, 0.15)            # kova kapağı
m.steps(37.3, 38.0, rate=0.33, gain=0.08, f=90); m.thud(38.3, f=60, gain=0.1)
m.whoosh(38.9, 0.4, 0.05)
for a, b in [(41.0, 41.5), (42.5, 42.9), (43.75, 44.1)]:
    m.whoosh(a, 0.45, 0.07); m.thud(b, f=200, gain=0.06)
for a, b in [(41.9, 42.3), (43.25, 43.6), (46.35, 47.15)]:
    for x in np.arange(a, b, 0.06): m.click(x, 0.05)
m.tension(44.0, 44.85, gain=0.035)
m.thud(44.85, f=70, gain=0.16); m.whoosh(44.85, 0.4, 0.07)
m.thud(46.35, f=200, gain=0.07); m.ding(47.2, gain=0.1)
for t0, f in [(47.55, 523.3), (47.8, 659.3), (48.05, 784.0), (48.3, 1046.5)]: m.note(t0, f, g=0.055, dur=1.4)
m.whoosh(48.75, 0.45, 0.06)
# ertesi gün
m.note(49.1, 392.0, g=0.05, dur=2.0)
m.thud(54.65, f=200, gain=0.06); m.ding(55.1, gain=0.07)
for t0, f in [(52.6, 329.6), (54.6, 392.0), (56.7, 261.6), (58.9, 329.6), (60.4, 392.0), (61.5, 523.3)]:
    m.note(t0, f, g=0.065, dur=2.6)
m.write(sys.argv[1])
