import sys
import numpy as np
from audio_kit import Mix, SR
# 04 — Annenin aramaları. Başlangıçlar scene.html ile aynı.
m = Mix(D=57.5)
VO = [(0.3,'l01',1),(3.6,'l02',1),(8.6,'l03',1),(12.1,'l04',1),(18.0,'l05',1),(24.4,'l06',1),
      (29.4,'l07',1),(33.4,'l08',1),(37.5,'l09',1),(44.6,'l10',1),(51.0,'l11',1)]
for st, n, tp in VO: m.vo(f'seslendirme/{n}.wav', st, tempo=tp)
m.pad(gain=0.045, swell_from=46.5)
rng = np.random.default_rng(4)

# Hızlı efektler: sadece ilgili dilime yazar (kitteki tam uzunluklu dizilerden çok daha hızlı)
def add(t0, sig):
    i = int(t0 * SR); L = min(len(sig), m.N - i)
    if L > 0: m.sfx[i:i+L] += sig[:L]
def envs(n, a, r):
    x = np.arange(n) / SR; return np.where(x < a, x / max(a, 1e-6), np.exp(-(x - a) / r * 4))
def buzz(t0, dur=0.9, g=0.09):
    x = np.arange(int(dur*SR)) / SR; add(t0, g * np.sign(np.sin(2*np.pi*150*x)) * (((x*6) % 1) < 0.6))
def click(t0, g=0.2):
    n = int(0.03*SR); add(t0, g * rng.standard_normal(n) * envs(n, 0.0005, 0.008))
def ping(t0, g=0.12):
    n = int(0.75*SR); x = np.arange(n)/SR; e = envs(n, 0.003, 0.2)
    add(t0, g*(np.sin(2*np.pi*1318*x) + 0.5*np.sin(2*np.pi*1975*x))*e); add(t0+0.09, g*0.7*np.sin(2*np.pi*1760*x)*e)
def tick(t0, g=0.12):
    n = int(0.15*SR); x = np.arange(n)/SR; add(t0, g*np.sin(2*np.pi*1200*x)*envs(n, 0.001, 0.04))
def steps(t0, t1, rate=0.4, g=0.2, f=70):
    n = int(0.18*SR); x = np.arange(n)/SR; s = g*np.sin(2*np.pi*f*x)*envs(n, 0.002, 0.05)
    for k in np.arange(t0, t1, rate): add(k, s)
def keyboard(t0, t1, g=0.025):
    n = int(0.06*SR); e = envs(n, 0.001, 0.015)
    for k in np.arange(t0, t1, 0.11): add(k + rng.uniform(-0.03, 0.03), g*rng.standard_normal(n)*e)
def whoosh(t0, dur=0.5, g=0.1):
    n = int(dur*3*SR); w = rng.standard_normal(n); k = int(0.002*SR)
    add(t0, g*np.convolve(w, np.ones(k)/k, 'same')*envs(n, dur*0.6, dur))
def ringback(t0, dur=1.0, g=0.035):   # TR çevir sesi (450 Hz)
    x = np.arange(int(dur*SR))/SR; e = np.clip(np.minimum(x, dur-x)/0.02, 0, 1); add(t0, g*np.sin(2*np.pi*450*x)*e)

buzz(0.4, 2.6); buzz(5.9, 2.6); buzz(13.2, 2.8)          # SEN'in telefonu titriyor
click(8.7); click(16.2)                                   # reddet
ping(10.8, 0.10); ping(16.7, 0.10)                        # "Sonra ararım." / "Sonra."
whoosh(3.3, 0.5); whoosh(12.0, 0.4); whoosh(24.3, 0.4); whoosh(37.2, 0.5)
for r in [4.0, 6.2, 12.4, 14.6]: ringback(r)              # annenin tarafında çalıyor
steps(18.2, 21.2, rate=0.33, g=0.10)                      # anne bardağı getiriyor
tick(19.9)                                                # ikinci bardak masada
for k in [25.7, 26.6, 27.4, 28.3]: buzz(k, 0.35, 0.07)    # cevapsız arama sayacı
ping(29.9, 0.12)                                          # "Yemek yaptım" mesajı
keyboard(24.4, 29.8); keyboard(31.8, 36.8)
steps(35.5, 37.6, rate=0.45, g=0.08)
for r in [39.6, 41.4, 43.2, 45.0]: ringback(r, 1.0, 0.06) # SEN arıyor, uzun uzun çalıyor
buzz(40.4, 5.6, 0.05)
steps(40.9, 46.0, rate=0.55, g=0.07)                      # annenin yavaş adımları
click(46.3, 0.15)                                         # açtı
for o, f in [(47.4, 261.6), (48.4, 329.6), (49.4, 392), (51.0, 349.2), (52.6, 392), (53.6, 523.3)]:
    m.note(o, f, 0.07, 2.8)                               # sıcak final

# Kitteki write() ile aynı miks; yalnız ducking yumuşatması np.convolve yerine kümülatif toplamla (aynı sonuç, çok daha hızlı)
import wave
def write_fast(path):
    k = int(0.25 * SR); c = np.concatenate([[0.0], np.cumsum(m.act)]); h = k // 2
    i = np.arange(m.N); lo = np.clip(i - h, 0, m.N); hi = np.clip(i - h + k, 0, m.N)
    duck = 1 - 0.55 * (c[hi] - c[lo]) / k
    out = m.v + (m.music + m.sfx) * duck
    out *= np.clip((m.D - m.t) / 2, 0, 1)
    out /= np.max(np.abs(out)) * 1.12
    w = wave.open(path, 'w'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close()
write_fast(sys.argv[1])
