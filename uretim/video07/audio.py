import sys
import numpy as np
from audio_kit import Mix, SR

D = 62.0
m = Mix(D=D)
# anlatım (scene.html ile aynı başlangıçlar); l03-l10 %6 hızlı
VO = [(0.3, 'l01', 1), (3.9, 'l02', 1), (11.1, 'l03', 1.06), (15.8, 'l04', 1.06), (19.85, 'l05', 1.06),
      (24.65, 'l06', 1.06), (30.7, 'l07', 1.06), (34.85, 'l08', 1.06), (40.1, 'l09', 1.06),
      (44.55, 'l10', 1.06), (49.7, 'l11', 1), (53.3, 'l12', 1)]
for st, n, tp in VO:
    m.vo(f'seslendirme/{n}.wav', st, tempo=tp)

m.pad(gain=0.045, swell_from=24)
t = m.t

# yatak lambası / mutfak lambası anahtarları
for k in [8.15, 12.2, 50.6, 52.75]:
    m.click(k, 0.25)
# yürüme
m.steps(9.3, 11.0, rate=0.37, gain=0.16)
m.steps(50.7, 52.4, rate=0.37, gain=0.16)
# musluktan su (filtrelenmiş gürültü)
n = m.rng.standard_normal(m.N); kk = int(0.0008 * SR); n = np.convolve(n, np.ones(kk) / kk, 'same')
e = np.clip((t - 13.75) / 0.1, 0, 1) * np.clip((15.25 - t) / 0.15, 0, 1)
m.sfx += 0.10 * n * e * (1 + 0.2 * np.sin(2 * np.pi * 9 * t))
# yudum
for k in [15.9, 16.35]:
    m.sfx += 0.18 * np.sin(2 * np.pi * 180 * (t - k)) * m.env(k, 0.07, 0.003, 0.05)
# damla (scene: 16 + n*1.7, düşüş ~0.4 sn)
for k in np.arange(16.0, 40.5, 1.7):
    h = k + 0.41
    f = 1500 * (1 + 0.6 * np.exp(-np.clip(t - h, 0, None) * 40))
    m.sfx += 0.07 * np.sin(2 * np.pi * f * (t - h)) * m.env(h, 0.06, 0.001, 0.05)
# düşünce balonları belirir
for k, f in [(19.94, 392), (21.55, 349.2), (24.84, 329.6), (26.82, 293.7), (28.99, 261.6)]:
    m.note(k, f, g=0.07, dur=1.8)
# kapı çalıyor: tak tak
for k in [23.5, 23.72]:
    m.sfx += 0.3 * np.sin(2 * np.pi * 95 * (t - k)) * m.env(k, 0.08, 0.002, 0.06)
# saat hızla ilerliyor, 03:40'ta vuruş
m.tension(32.8, 36.2, gain=0.05)
m.thud(36.27, f=45, gain=0.3)
# çekmece + kâğıt
m.whoosh(40.9, 0.4, 0.08); m.click(41.0, 0.15); m.whoosh(41.7, 0.35, 0.06)
# yazma (kalem cızırtısı)
m.keyboard(42.7, 47.0, gain=0.025)
# balonlar kâğıda akar
for k in [43.0, 43.7, 44.6, 45.3, 46.15]:
    m.whoosh(k, 0.45, 0.07)
# rahatlama: yükselen notalar
for k, f in [(46.98, 261.6), (47.6, 329.6), (49.75, 392), (53.3, 261.6), (54.95, 329.6), (57.15, 392), (59.3, 523.3)]:
    m.note(k, f, g=0.07, dur=2.5)
m.write(sys.argv[1])
