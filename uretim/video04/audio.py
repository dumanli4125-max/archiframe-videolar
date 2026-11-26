import sys
import numpy as np
from audio_kit import Mix
m = Mix(D=57.5)
VO = [(0.3,'l01',1),(3.6,'l02',1),(8.6,'l03',1),(12.1,'l04',1),(18.0,'l05',1),(24.4,'l06',1),
      (29.4,'l07',1),(33.4,'l08',1),(37.5,'l09',1),(44.6,'l10',1),(51.0,'l11',1)]
for st, n, tp in VO: m.vo(f'seslendirme/{n}.wav', st, tempo=tp)
m.pad(gain=0.045, swell_from=46.5)
t = m.t
# telefon titreşimleri (SEN'in telefonu)
m.buzz(0.4, 2.6); m.buzz(5.9, 2.6); m.buzz(13.2, 2.8)
m.click(8.7); m.click(16.2)                        # reddet
m.ping(10.8, 0.10); m.ping(16.7, 0.10)             # "Sonra ararım." gönderildi
m.whoosh(3.3, 0.5); m.whoosh(12.0, 0.4); m.whoosh(24.3, 0.4); m.whoosh(37.2, 0.5)
# annenin arka planda çalan arama sesi (çevir sesi)
def ringback(t0, dur=1.0, g=0.035):
    e = ((t > t0) & (t < t0 + dur)).astype(float)
    m.sfx += g * np.sin(2*np.pi*450*t) * e
for r in [4.0, 6.2, 12.4, 14.6]: ringback(r)
m.steps(18.2, 21.2, rate=0.33, gain=0.10)          # annenin adımları
m.tick(19.9, 0.12)                                  # ikinci bardak masada
for k in [25.7, 26.6, 27.4, 28.3]: m.buzz(k, 0.35, 0.07)
m.ping(29.9, 0.12)                                  # "Yemek yaptım" mesajı
m.keyboard(24.4, 29.8, 0.025); m.keyboard(31.8, 36.8, 0.025)
m.steps(35.5, 37.6, rate=0.45, gain=0.08)
# SEN arıyor: uzun çalma
for r in [39.6, 41.4, 43.2, 45.0]: ringback(r, 1.0, 0.06)
m.buzz(40.4, 5.6, 0.05)                             # annenin masadaki telefonu
m.steps(40.9, 46.0, rate=0.55, gain=0.07)
m.click(46.3, 0.15)                                 # açtı
# sıcak final notaları
for o, f in [(47.4, 261.6), (48.4, 329.6), (49.4, 392), (51.0, 349.2), (52.6, 392), (53.6, 523.3)]:
    m.note(o, f, 0.07, 2.8)
m.write(sys.argv[1])
