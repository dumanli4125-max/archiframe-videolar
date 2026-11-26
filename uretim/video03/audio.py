import sys
import numpy as np
from audio_kit import Mix
# 03 — Taksit. Başlangıçlar scene.html ile aynı.
m = Mix(D=62.5)
VO = [(0.3,'l01',1),(4.5,'l02',1),(9.3,'l03',1.06),(15.36,'l04',1.04),(20.38,'l05',1.06),(26.63,'l06',1.06),
      (32.6,'l07',1.06),(38.0,'l08',1.06),(43.68,'l09',1),(47.78,'l10',1),(51.48,'l11',1),(56.08,'l12',1)]
for st, n, tp in VO:
    m.vo(f'seslendirme/{n}.wav', st, tempo=tp)
m.pad(swell_from=40)
# A: MAĞAZA
m.steps(0.2, 3.0, rate=0.35)
m.ping(8.1); m.whoosh(7.8, 0.5)
m.note(10.6, 523.3, g=0.06, dur=1.2); m.note(10.8, 659.3, g=0.05, dur=1.2)
m.steps(11.7, 12.5, rate=0.35)
m.click(12.6)
m.ding(14.0, gain=0.12)
m.steps(14.4, 15.3, rate=0.35)
m.whoosh(15.1, 0.5, gain=0.08)
# B: SOKAK
m.steps(15.4, 17.4, rate=0.35)
m.tick(16.42)
m.steps(17.0, 18.4, rate=0.38, gain=0.12, f=85)
m.note(18.0, 659.3, g=0.05, dur=1.5)
for k in np.arange(20.0, 21.0, 0.2): m.tick(k, gain=0.12)
m.note(22.1, 110, g=0.07, dur=2.0)
m.tick(22.83, gain=0.10); m.tick(23.05, gain=0.10)
m.thud(24.78, f=60, gain=0.3); m.click(24.8, gain=0.25)
m.click(25.85, gain=0.35); m.click(25.9, gain=0.25)
m.note(26.0, 220, g=0.06, dur=2.0)
m.whoosh(26.4, 0.5, gain=0.08)
# C: MAĞAZA (yeni model)
m.steps(26.7, 28.5, rate=0.35)
m.ping(27.76)
m.tick(30.3, gain=0.1); m.tick(30.75, gain=0.1); m.tick(31.2, gain=0.1)
m.ding(31.85, gain=0.12)
m.whoosh(32.4, 0.5, gain=0.08)
# D: EV, sayaçlar
m.steps(32.7, 34.5, rate=0.35)
m.ping(34.86, gain=0.12); m.ping(36.0, gain=0.12)
m.thud(37.13, f=50, gain=0.3)
m.whoosh(37.8, 0.5, gain=0.08)
# E: MARKET
m.steps(38.05, 39.5, rate=0.35)
m.click(41.6, gain=0.2)
m.buzz(42.62, dur=0.8, gain=0.1); m.thud(42.7, f=42, gain=0.3)
m.note(43.1, 196, g=0.06, dur=2.5)
m.click(45.78, gain=0.15)
m.note(46.2, 174.6, g=0.06, dur=3.0)
# F: BANKA
for k in np.arange(48.1, 51.2, 0.27): m.tick(k, gain=0.05)
m.thud(50.68, f=45, gain=0.35)
# FİNAL
for t0, f in [(51.5, 220), (53.78, 185), (56.1, 261.6), (57.8, 329.6), (59.6, 392)]:
    m.note(t0, f)
m.write(sys.argv[1])
