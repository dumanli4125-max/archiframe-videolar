import sys
import numpy as np
from audio_kit import Mix

D = 58.0
m = Mix(D=D)
# anlatım (scene.html ile aynı başlangıçlar)
VO = [(0.3,'l01'),(4.3,'l02'),(8.2,'l03'),(12.7,'l04'),(16.9,'l05'),(20.8,'l06'),
      (26.1,'l07'),(31.0,'l08'),(36.4,'l09'),(41.0,'l10'),(45.5,'l11'),(49.6,'l12')]
for st, n in VO: m.vo(f'seslendirme/{n}.wav', st)
m.pad(gain=0.045, swell_from=40)
# kanca: bakiye hızla eriyor
for k in np.arange(0.9, 2.7, 0.06): m.tick(k, gain=0.05)
m.thud(3.0, f=50, gain=0.25)
m.whoosh(3.75, 0.4, 0.08)
# maaş günü: bildirim, sayaç yukarı
m.buzz(6.1, 0.8); m.ping(6.2)
for k in np.arange(8.2, 9.5, 0.07): m.tick(k, gain=0.05)
m.ding(9.45, gain=0.13)
m.note(10.6, 523.3, g=0.07, dur=1.5); m.note(10.9, 659.3, g=0.07, dur=1.5); m.note(11.2, 784, g=0.06, dur=1.8)
# kapı
m.thud(14.0, f=90, gain=0.3); m.thud(14.35, f=90, gain=0.3); m.click(14.0, 0.25); m.click(14.35, 0.25)
# pay alanlar: adımlar + para akışı (tick düşüş)
TAKES = [(14.4,16.3,17.9),(21.0,23.2,23.1),(21.3,22.9,24.0),(21.6,23.2,24.7),(25.3,26.4,26.7),(26.4,27.6,27.9),(27.9,29.1,29.4)]
for a, b, tk in TAKES:
    m.steps(a, b, rate=0.36, gain=0.08)
    m.whoosh(tk - 0.1, 0.4, 0.07)
    for k in np.arange(tk, tk + 0.6, 0.05): m.tick(k, gain=0.045)
    m.thud(tk + 0.05, f=55, gain=0.12)
for t0, f in [(18.0,392),(23.2,349.2),(26.8,329.6),(28.0,293.7),(29.5,261.6)]: m.note(t0, f, g=0.05, dur=1.8)
m.whoosh(30.6, 0.5, 0.08)
# 3. gün: ekstre, bozukluk
for i in range(5): m.click(33.6 + i * 0.25, 0.1)
for i in range(9): m.ping(39.4 + i * 0.1 + 0.3, gain=0.025); m.click(39.4 + i * 0.1 + 0.33, 0.12)
m.note(37.9, 220, g=0.06, dur=2.5)
# kardeş araması
m.buzz(41.0, 0.9); m.buzz(41.0 + 1.0, 0.0)
m.ping(43.7, gain=0.06)
m.thud(46.1, f=45, gain=0.2)
for t0, f in [(42.6,329.6),(44.2,293.7),(46.3,261.6),(47.8,220),(50.2,261.6),(51.8,329.6),(53.4,392),(55.0,523.3)]:
    m.note(t0, f, g=0.07, dur=2.5)
# final: kumbaraya jeton
m.ping(53.6, gain=0.1); m.click(53.6, 0.15)
m.write(sys.argv[1])
