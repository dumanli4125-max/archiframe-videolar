import sys
import numpy as np
from audio_kit import Mix, SR

D = 59.5
m = Mix(D=D)
# anlatım (scene.html ile aynı başlangıçlar); tempo düzeltmesi yok
VO = [(0.3, 'l01'), (4.4, 'l02'), (8.9, 'l03'), (13.0, 'l04'), (17.0, 'l05'), (21.4, 'l06'),
      (25.9, 'l07'), (29.8, 'l08'), (34.4, 'l09'), (40.1, 'l10'), (44.8, 'l11'), (50.6, 'l12')]
for st, n in VO:
    m.vo(f'seslendirme/{n}.wav', st)

m.pad(gain=0.04, swell_from=44)
t = m.t
# banka uğultusu (4.2–29.6): yumuşak gürültü
n = m.rng.standard_normal(m.N); k = int(0.006 * SR); n = np.convolve(n, np.ones(k) / k, 'same')
amp = np.clip((t - 4.2) / 0.6, 0, 1) * (1 - np.clip((t - 29.3) / 0.4, 0, 1))
m.sfx += 0.18 * n * amp
# market floresan uğultusu (38.45–50.6)
amp2 = np.clip((t - 38.45) / 0.4, 0, 1) * (1 - np.clip((t - 50.4) / 1.0, 0, 1))
m.sfx += 0.012 * np.sin(2 * np.pi * 100 * t) * amp2
# kanca: soru notaları
m.note(0.4, 392, g=0.06, dur=2.0); m.note(1.6, 440, g=0.06, dur=2.0); m.note(3.3, 523.3, g=0.06, dur=2.0)
# sahne geçişleri
for k in [4.2, 21.4, 29.6, 34.2, 38.45]:
    m.whoosh(k - 0.15, 0.4, 0.09)
# sıra numaratörü
m.ding(7.9, gain=0.08); m.ding(24.0, gain=0.08)
# gün 1: takım elbiseli girer, sırayı keser, telefon
m.steps(9.0, 10.6, rate=0.36, gain=0.14)
m.steps(10.9, 12.2, rate=0.36, gain=0.14)
m.buzz(12.6, dur=0.5, gain=0.06)
m.note(17.4, 523.3, g=0.05, dur=2.0)      # gülümseme
m.ping(18.0, gain=0.08)                   # göz
m.thud(18.4, f=60, gain=0.18)             # MEŞGUL damgası
m.note(19.8, 659.3, g=0.05, dur=2.0)
# gün 2: eşofmanlı aynısını yapar
m.steps(23.0, 24.5, rate=0.36, gain=0.14)
m.steps(24.6, 25.6, rate=0.36, gain=0.14)
m.tension(26.0, 29.4, gain=0.05)
m.ping(26.3, gain=0.08)
m.thud(26.7, f=42, gain=0.34)             # KABA damgası
m.click(27.2, 0.12); m.click(28.3, 0.12)
# karşılaştırma
m.thud(29.9, f=50, gain=0.18); m.thud(30.4, f=50, gain=0.18)
m.note(32.8, 349.2, g=0.07, dur=2.0)
# koşu
m.steps(34.4, 38.4, rate=0.18, gain=0.12)
# market kapısı ding-dong
for k, f in [(38.5, 659.3), (38.8, 523.3)]:
    m.note(k, f, g=0.09, dur=1.0)
m.steps(38.5, 40.0, rate=0.4, gain=0.1)
m.click(41.3, 0.1)                        # şişe
m.steps(42.4, 45.0, rate=0.5, gain=0.12)  # görevli peşinde
m.tension(42.5, 50.2, gain=0.045)
m.ping(46.4, gain=0.08)
m.thud(47.1, f=42, gain=0.3)              # ŞÜPHELİ damgası
# final
for k, f in [(50.6, 392), (53.7, 523.3), (55.2, 659.3), (56.8, 784)]:
    m.note(k, f, g=0.07, dur=2.5)
m.write(sys.argv[1])
