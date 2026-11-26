import sys, json
import numpy as np
from audio_kit import Mix

D = 59.5
m = Mix(D=D)
# anlatım: başlangıç/tempo zamanlama.json'dan (scene.html ile aynı)
Z = json.load(open('zamanlama.json'))
for n, z in Z.items(): m.vo(f'seslendirme/{n}.wav', z['baslangic'], tempo=z.get('tempo', 1.0))
m.pad(gain=0.045, swell_from=45)
# kanca: uçakta titreme, sonra arabada radyo
m.note(0.3, 196, g=0.05, dur=2.2); m.note(0.9, 185, g=0.04, dur=1.6)
m.whoosh(2.45, 0.4, 0.08)
for t0, f in [(2.7, 523.3), (3.0, 659.3), (3.3, 784), (3.7, 659.3)]: m.note(t0, f, g=0.03, dur=0.6)
m.tick(4.1, gain=0.07)
# havalimanı anonsu, kemer tıkı
m.ding(5.3, gain=0.07)
m.whoosh(6.3, 0.4, 0.06)
m.click(9.15, gain=0.25); m.ping(9.25, gain=0.06)
# kalkış: uğultu
m.whoosh(10.9, 2.5, 0.10); m.thud(11.25, f=40, gain=0.18)
m.note(12.6, 174.6, g=0.05, dur=2)
# hostes gülümser, sarsıntı, dua
m.steps(14.7, 15.4, rate=0.22, gain=0.06)
m.ping(15.4, gain=0.05); m.note(16.2, 523.3, g=0.04, dur=1.2)
for k in [18.0, 18.25, 18.55, 18.8]: m.thud(k, f=55, gain=0.14)
for k in np.arange(18.0, 19.0, 0.06): m.click(k + m.rng.uniform(-0.02, 0.02), gain=0.05)
m.note(19.3, 196, g=0.05, dur=1.6)
# iniş, oh be, araba kapısı
m.whoosh(20.55, 0.8, 0.07)
m.note(21.4, 659.3, g=0.04, dur=0.8)
m.thud(21.9, f=70, gain=0.12)
m.tick(22.85, gain=0.07); m.whoosh(23.65, 0.35, 0.05)
# radyo melodisi, gaz
for i, f in enumerate([523.3, 587.3, 659.3, 784, 659.3, 587.3, 523.3, 659.3, 784, 880]):
    m.note(26.7 + i * 0.32, f, g=0.03, dur=0.5)
m.whoosh(28.7, 1.0, 0.10); m.steps(28.7, 30.0, rate=0.08, gain=0.05, f=55)
# grafik
m.whoosh(30.15, 0.5, 0.06); m.tick(30.75, gain=0.06)
for t0, f in [(32.05, 261.6), (32.3, 329.6), (32.55, 392), (32.8, 523.3)]: m.note(t0, f, g=0.05, dur=1.0)
m.thud(32.9, f=60, gain=0.15)
# haber
for t0, f in [(33.95, 440), (34.15, 554.4), (34.35, 659.3)]: m.note(t0, f, g=0.04, dur=0.8)
m.ping(35.6, gain=0.05); m.ping(35.8, gain=0.05)
# her gün
for i in range(7): m.tick(37.05 + i * 0.17, gain=0.06)
m.thud(38.55, f=60, gain=0.15); m.ping(38.6, gain=0.05)
m.note(39.8, 392, g=0.04, dur=1.0)
# dönüm: bildirim, fren lambaları, sert fren
m.buzz(41.7, 0.6, 0.06); m.ping(41.75, gain=0.10)
m.note(44.3, 146.8, g=0.05, dur=1.5)
m.note(45.1, 138.6, g=0.07, dur=1.5); m.tick(45.1, gain=0.08)
m.whoosh(46.4, 1.5, 0.22); m.thud(46.45, f=45, gain=0.30)
m.thud(47.95, f=50, gain=0.20)
for k in np.arange(48.6, 51.2, 0.75): m.steps(k, k + 0.3, rate=0.18, gain=0.12, f=55)  # kalp atışı
# final
for t0, f in [(51.7, 261.6), (53.5, 329.6), (55.0, 392), (56.8, 523.3)]: m.note(t0, f, g=0.07, dur=2.5)
m.click(54.0, gain=0.25); m.ping(54.1, gain=0.06)
m.whoosh(55.8, 0.5, 0.06)
m.write(sys.argv[1])
