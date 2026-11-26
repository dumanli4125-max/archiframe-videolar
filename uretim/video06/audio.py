import sys
import numpy as np
from audio_kit import Mix
D = 57.5
m = Mix(D=D)
# anlatım (scene.html ile aynı başlangıçlar)
VO = [(0.3,'l01'),(3.6,'l02'),(7.9,'l03'),(11.9,'l04'),(17.2,'l05'),(22.4,'l06'),
      (26.9,'l07'),(30.6,'l08'),(36.2,'l09'),(40.2,'l10'),(44.9,'l11'),(50.3,'l12')]
for st, n in VO: m.vo(f'seslendirme/{n}.wav', st)
m.pad(gain=0.045, swell_from=40)
# gündüz: neşeli kısa notalar her gülümsemede
for t0, f in [(0.7,523.3),(1.5,659.3),(6.8,587.3),(10.9,659.3),(13.1,698.5),(15.7,784)]: m.note(t0, f, g=0.06, dur=1.2)
for t0 in [0.6, 1.4, 6.8, 10.9, 13.1, 15.7]: m.ping(t0, gain=0.1)
m.keyboard(3.7, 4.6, gain=0.03)
m.whoosh(8.2, 0.5, 0.1); m.thud(8.4, f=60, gain=0.15)            # müşteri bağırıyor
m.steps(11.9, 12.9, rate=0.35, gain=0.12); m.steps(14.6, 15.7, rate=0.35, gain=0.12)
for k in np.arange(17.5, 18.65, 0.072): m.tick(k, gain=0.07)       # sayaç 4 -> 20
m.ding(18.65, gain=0.12)
for t0 in [3.5, 7.85, 11.85, 14.6, 17.2]: m.whoosh(t0-0.15, 0.35, 0.06)
# akşam: yorgun adımlar, ev
m.steps(20.8, 22.4, rate=0.48, gain=0.12)
m.click(22.45, gain=0.12)                                           # ön kapı
m.steps(22.8, 34.2, rate=0.5, gain=0.08)
m.note(27.4, 392, g=0.05, dur=1.5); m.note(28.9, 440, g=0.05, dur=1.5)
m.thud(34.75, f=48, gain=0.45); m.click(34.75, gain=0.3)            # kapı çarpar
for k in np.arange(35.2, 50.0, 1.0): m.tick(k, gain=0.035)           # duvar saati
m.click(39.1, gain=0.12); m.tick(39.1, gain=0.06)                    # tabak masaya
for t0, f in [(36.4,329.6),(38.0,293.7),(40.4,261.6),(43.5,220),(46.8,246.9),(50.4,261.6),(52.4,329.6),(53.4,392)]:
    m.note(t0, f, g=0.07, dur=2.5)
m.write(sys.argv[1])
