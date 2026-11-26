import sys
import numpy as np
from audio_kit import Mix, SR

D = 59.5
m = Mix(D=D)
# İngilizce anlatım (Kyle). l01/l08/l09 uzun: hafif tempo + küçük başlangıç kaydırması
VO = [(0.15, 'l01', 1.08), (5.3, 'l02', 1.0), (9.9, 'l03', 1.0), (15.5, 'l04', 1.0), (20.8, 'l05', 1.0), (25.3, 'l06', 1.0),
      (30.4, 'l07', 1.0), (34.3, 'l08', 1.06), (38.65, 'l09', 1.08), (42.9, 'l10', 1.0), (46.6, 'l11', 1.0), (51.3, 'l12', 1.0)]
for st, n, tp in VO:
    m.vo(f'seslendirme_en/{n}.wav', st, tempo=tp)

m.pad(gain=0.04, swell_from=42)
t = m.t
# tren uğultusu: alçak geçiren gürültü, finalde söner
n = m.rng.standard_normal(m.N); k = int(0.004 * SR); n = np.convolve(n, np.ones(k) / k, 'same')
n2 = np.convolve(n, np.ones(k) / k, 'same')
amp = np.clip(t / 0.8, 0, 1) * (1 - np.clip((t - 51.0) / 1.5, 0, 1))
m.sfx += 0.55 * n2 * amp * (1 + 0.15 * np.sin(2 * np.pi * 0.7 * t))
# ray tıkırtısı (tak-tak)
for c in np.arange(0.6, 51.0, 1.15):
    for d in (0, 0.13):
        m.sfx += 0.10 * np.sin(2 * np.pi * 70 * (t - c - d)) * m.env(c + d, 0.05, 0.002, 0.04)
# 07:40 vuruşu
m.ping(7.0, gain=0.12)
for k in (3.0,):
    m.tick(k, 0.12)
# gün geçişleri
for k in [16.6, 17.3, 18.3, 19.0, 19.6, 20.15, 30.4, 38.7]:
    m.whoosh(k - 0.1, 0.35, 0.08)
# 3 yıl: hızlı dönen günler
for k in np.arange(25.4, 26.6, 1 / 9):
    m.tick(k, 0.07)
m.thud(26.6, f=50, gain=0.22)
# etiketler belirir
for k, f in [(10.7, 392), (12.3, 440), (13.4, 349.2)]:
    m.note(k, f, g=0.05, dur=1.5)
# "?" adı yok
m.note(28.5, 293.7, g=0.06, dur=2.0)
# dönüm: boş köşe
m.tension(30.6, 38.4, gain=0.05)
m.thud(32.95, f=40, gain=0.25)
# kapı zili + kapı
for k, f in [(39.1, 659.3), (39.4, 523.3)]:
    m.note(k, f, g=0.10, dur=1.0)
m.whoosh(39.5, 0.6, 0.12)
m.steps(40.3, 41.6, rate=0.37, gain=0.14)
m.whoosh(41.9, 0.6, 0.08)
# günaydın, gülümseme, isim
m.note(44.3, 392, g=0.07, dur=2.5)
m.note(47.1, 440, g=0.07, dur=2.5)
for k, f in [(50.4, 523.3), (50.8, 659.3), (51.3, 392), (52.4, 523.3), (54.8, 659.3), (56.8, 784)]:
    m.note(k, f, g=0.07, dur=2.5)
m.write(sys.argv[1])
