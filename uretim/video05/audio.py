import sys
import numpy as np
from audio_kit import Mix, SR
# 05 — Annen elde yıkardı. VO başlangıçları scene.html ile AYNI.
D = 58.5
m = Mix(D=D)
VO = [(0.3, 'l01'), (4.6, 'l02'), (10.3, 'l03'), (16.3, 'l04'), (20.5, 'l05'), (23.9, 'l06'),
      (29.2, 'l07'), (35.3, 'l08'), (39.0, 'l09'), (42.8, 'l10'), (47.8, 'l11'), (52.2, 'l12')]
for st, n in VO:
    m.vo(f'seslendirme/{n}.wav', st)
t = m.t; rng = m.rng
def smooth(x, k):
    c = np.cumsum(np.concatenate([[0.0], x])); y = (c[k:] - c[:-k]) / k
    return np.concatenate([y, np.zeros(len(x) - len(y))])

# --- müzik: alçak pad, geçmişte sıcak melodi, finalde yükselir
m.pad(gain=0.045, swell_from=38)
for t0, f in [(23.2, 261.6), (25.6, 329.6), (28.0, 293.7), (30.4, 261.6), (33.0, 246.9), (35.4, 220.0),
              (38.0, 261.6), (40.4, 329.6), (42.9, 392.0), (45.4, 349.2), (52.2, 261.6), (54.3, 329.6), (55.6, 392.0)]:
    m.note(t0, f, g=0.07, dur=2.6)

# --- çamaşır makinesi: titreyen gürültü 0 → 6.5, sonra hata bipleri
mask = (t < 6.5) * np.clip(t / 0.4, 0, 1)
hum = np.sin(2*np.pi*48*t) * (0.6 + 0.4*np.sin(2*np.pi*7*t))
k = int(0.004*SR); noise = smooth(rng.standard_normal(m.N), k)
m.sfx += (0.10*hum + 0.10*noise*(0.5 + 0.5*np.sin(2*np.pi*11*t))) * mask
m.thud(6.5, f=55, gain=0.28)
for b in (6.8, 7.15, 7.5):
    m.sfx += 0.10*np.sin(2*np.pi*1046*t) * m.env(b, 0.18, 0.003, 0.15)
# telefon: yazma, cevap, "2 SAAT"
for kk in np.arange(11.0, 12.9, 0.13):
    m.click(kk + rng.uniform(-0.02, 0.02), gain=0.06)
m.buzz(13.9, dur=0.8, gain=0.06); m.ping(13.95)
m.tick(14.9, gain=0.18)
# volta
m.steps(16.4, 20.2, rate=0.37, gain=0.18)
# geçişler
m.whoosh(21.2, dur=1.2, gain=0.10); m.note(22.2, 196.0, g=0.06, dur=3)
m.whoosh(47.0, dur=0.9, gain=0.10)
# geçmiş: su şapırtısı (ovma ritmi), rüzgâr, üfleme
scrub = ((t > 22.4) & (t < 47.0)) & ~((t > 35.4) & (t < 38.0))
k2 = int(0.0008*SR); wn = smooth(rng.standard_normal(m.N), k2)
m.sfx += 0.035*wn*(0.5 + 0.5*np.sin(2*np.pi*(9/(2*np.pi))*t))**4 * scrub
k3 = int(0.02*SR); wind = smooth(rng.standard_normal(m.N), k3)
m.sfx += 0.25*wind*(0.6 + 0.4*np.sin(2*np.pi*0.2*t)) * ((t > 22.4) & (t < 47.0)) * np.clip((t - 22.4)/2, 0, 1) * (1 + np.clip((t - 29.2)/1.5, 0, 1))
for b in (35.7, 36.5, 37.3):
    m.whoosh(b, dur=0.45, gain=0.07)
m.tick(37.9, gain=0.08)
m.thud(42.9, f=42, gain=0.30)        # 20 YIL
for kk in np.arange(43.4, 46.4, 3.0/11):
    m.click(kk, gain=0.05)            # mandal
# bugün + final
m.thud(48.6, f=40, gain=0.22)
m.thud(52.0, f=38, gain=0.25)
for b in (53.0, 54.6):                # arama sesi
    m.sfx += 0.05*(np.sin(2*np.pi*425*t)) * ((t > b) & (t < b + 1.0))
# Kit'teki write() ile aynı miks; ducking yumuşatması np.convolve yerine kümülatif toplamla (aynı sonuç, çok daha hızlı).
def write_fast(m, path):
    import wave
    k = int(0.25 * SR); c = np.cumsum(np.concatenate([np.zeros(k // 2 + 1), m.act, np.zeros(k)]))
    avg = (c[k:k + m.N] - c[:m.N]) / k
    duck = 1 - 0.55 * avg
    out = m.v + (m.music + m.sfx) * duck
    out *= np.clip((m.D - m.t) / 2, 0, 1)
    out /= np.max(np.abs(out)) * 1.12
    w = wave.open(path, 'w'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close()
write_fast(m, sys.argv[1])
