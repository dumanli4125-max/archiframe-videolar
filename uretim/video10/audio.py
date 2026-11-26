import sys, json
import numpy as np
from audio_kit import Mix

D = 61
m = Mix(D=D)
# anlatım: başlangıç/tempo zamanlama.json'dan (scene.html ile aynı)
Z = json.load(open('zamanlama.json'))
for n, z in Z.items(): m.vo(f'seslendirme/{n}.wav', z['baslangic'], tempo=z.get('tempo', 1.0))
m.pad(gain=0.045, swell_from=48)
# kanca: NORMAL damgası, böcek kartı, İĞRENÇ damgası
m.ping(1.35, gain=0.07); m.note(1.35, 523.3, g=0.05, dur=1.5)
m.whoosh(2.5, 0.45, 0.07)
m.thud(3.1, f=60, gain=0.2); m.note(3.1, 233.1, g=0.06, dur=1.6)
m.tick(3.95, gain=0.07)
# kahvaltı: çay bardağı şıngırtısı, batırma, NORMAL
m.ping(5.7, gain=0.03)
m.click(8.25, gain=0.12)
for k in np.arange(9.05, 9.9, 0.18): m.click(k, gain=0.05)
m.ping(10.0, gain=0.07); m.note(10.0, 587.3, g=0.05, dur=1.4)
# soru: zoom
m.whoosh(10.75, 0.8, 0.08)
for t0, f in [(11.1, 392), (11.7, 440), (12.5, 493.9)]: m.note(t0, f, g=0.04, dur=1.0)
# arı: vızıltı, nektar, kovan, bal
m.buzz(13.4, 1.5, 0.025); m.buzz(15.1, 1.4, 0.025); m.buzz(17.6, 1.2, 0.02)
for k in [14.2, 14.4, 14.6, 14.8]: m.tick(k, gain=0.04)
m.ping(16.9, gain=0.05)
m.ding(17.95, gain=0.08)
for t0, f in [(17.95, 523.3), (18.25, 659.3), (18.55, 784)]: m.note(t0, f, g=0.045, dur=1.2)
# geri dönüş: şaşırma, yine NORMAL
m.note(20.7, 220, g=0.06, dur=1.4); m.whoosh(20.6, 0.3, 0.05)
for k in np.arange(22.6, 23.0, 0.15): m.click(k, gain=0.05)
m.ping(22.5, gain=0.07)
# dünya turu: küre, kart, kalabalık yürür, İĞRENÇ
m.whoosh(23.25, 0.6, 0.07); m.whoosh(24.85, 0.5, 0.08)
m.steps(26.2, 27.2, rate=0.14, gain=0.08)
m.thud(28.3, f=60, gain=0.2); m.note(28.3, 233.1, g=0.06, dur=1.4)
# çocuk: kıtır kıtır, damga NORMAL'e döner
m.steps(29.0, 30.0, rate=0.2, gain=0.06)
for t0 in [31.2, 31.45]:
    for k in np.arange(t0, t0 + 0.12, 0.025): m.click(k, gain=0.12)
m.whoosh(32.75, 0.35, 0.06); m.ping(32.95, gain=0.08); m.note(32.95, 659.3, g=0.05, dur=1.3)
# salyangoz, peynir, iki tepki
m.whoosh(33.65, 0.45, 0.07); m.whoosh(35.3, 0.45, 0.07)
m.note(37.05, 207.7, g=0.05, dur=1.2)
m.ping(38.6, gain=0.05); m.note(38.6, 523.3, g=0.045, dur=1.2)
# kokoreç: cızırtı, lezzet, turist İĞRENÇ
for k in np.arange(39.8, 48.4, 0.07):
    m.click(k + m.rng.uniform(-0.02, 0.02), gain=0.018)
m.ping(40.6, gain=0.07)
m.steps(41.0, 41.9, rate=0.22, gain=0.07)
m.thud(42.6, f=60, gain=0.18)
# dönüm: yan masa, buruşturma, gülme
m.note(43.4, 293.7, g=0.05, dur=2)
m.note(46.75, 233.1, g=0.06, dur=1.4)
for t0, f in [(47.85, 523.3), (48.0, 659.3)]: m.note(t0, f, g=0.04, dur=0.6)
# durdu, aynı yüz, sofralar
m.thud(48.9, f=50, gain=0.22)
m.whoosh(49.75, 0.4, 0.06)
m.thud(50.65, f=55, gain=0.2); m.ping(50.7, gain=0.06)
for i in range(4): m.whoosh(52.0 + i * 0.25, 0.3, 0.04)
for i in range(4): m.ping(53.0 + i * 0.15, gain=0.04)
# final
for t0, f in [(54.2, 261.6), (56.6, 329.6), (57.4, 392), (58.2, 523.3)]: m.note(t0, f, g=0.07, dur=2.5)
m.whoosh(57.3, 0.6, 0.06)
m.write(sys.argv[1])
