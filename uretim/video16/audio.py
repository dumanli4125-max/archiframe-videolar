import sys
import numpy as np
from audio_kit import Mix, SR

D = 61.3
m = Mix(D=D)
# anlatım (scene.html ile aynı başlangıçlar); tempo düzeltmesi yok
VO = [(0.3, 'l01'), (4.8, 'l02'), (9.85, 'l03'), (14.3, 'l04'), (18.75, 'l05'), (21.95, 'l06'),
      (26.1, 'l07'), (31.3, 'l08'), (36.5, 'l09'), (42.75, 'l10'), (48.0, 'l11'), (52.5, 'l12')]
for st, n in VO:
    m.vo(f'seslendirme/{n}.wav', st)

m.pad(gain=0.04, swell_from=36)
t = m.t
# meydan uğultusu: kalabalık mırıltısı (alçak geçiren gürültü), finalde söner
n = m.rng.standard_normal(m.N); k = int(0.006 * SR); n = np.convolve(n, np.ones(k) / k, 'same')
n = np.convolve(n, np.ones(k) / k, 'same')
amp = np.clip(t / 1.0, 0, 1) * (1 - np.clip((t - 52.3) / 1.5, 0, 1))
m.sfx += 0.35 * n * amp * (1 + 0.25 * np.sin(2 * np.pi * 0.3 * t))

def applause(t0, t1, density=40, gain=0.05):
    """Alkış: rastgele kısa gürültü patlamaları."""
    cnt = int((t1 - t0) * density)
    for c in m.rng.uniform(t0, t1, cnt):
        m.sfx += gain * m.rng.standard_normal(m.N) * m.env(c, 0.012, 0.0005, 0.01)

# sultan konuşur (anlaşılmaz) -> alkış
m.note(9.95, 220, g=0.04, dur=1.2)
applause(11.4, 13.1, 45, 0.05)
applause(13.1, 18.4, 25, 0.035)      # SEN de katılır, alkış sürer
# "Yağmur yağıyor!" vurgusu
m.thud(19.25, f=55, gain=0.18)
m.note(20.45, 523.3, g=0.06, dur=1.8)
# güneş
m.note(22.05, 659.3, g=0.06, dur=2.5)
# şemsiyeler açılır (pat pat)
for c in np.arange(23.9, 24.65, 0.06):
    m.whoosh(c, 0.12, 0.05)
m.whoosh(25.25, 0.25, 0.12)          # SEN açar
# sıcak: hafif gerilim
m.tension(26.3, 31.0, gain=0.03)
# yukarı bakış, gökyüzü
m.whoosh(32.3, 0.5, 0.08)
m.note(32.4, 392, g=0.06, dur=3)
m.note(33.5, 587.3, g=0.05, dur=3)
# şemsiyeler kapanır (tık)
for c, f in [(36.9, 440), (39.1, 493.9), (40.7, 523.3), (41.7, 587.3)]:
    m.click(c + 0.3, 0.25)
    m.note(c + 0.3, f, g=0.05, dur=1.8)
# sultan kaybolur, ekran belirir
m.whoosh(44.35, 0.6, 0.10)
m.thud(44.5, f=40, gain=0.15)
m.ping(46.85, gain=0.12)
# herkes telefonda: bildirim tıkları, "Aynen!" yankıları
for c in [48.1, 48.3, 48.5, 48.75]:
    m.tick(c, 0.08)
for c in [50.0, 50.5, 51.0]:
    m.ping(c, gain=0.06)
# final
for c, f in [(52.6, 392), (55.85, 523.3), (57.3, 659.3), (58.6, 784)]:
    m.note(c, f, g=0.07, dur=2.5)
m.write(sys.argv[1])
