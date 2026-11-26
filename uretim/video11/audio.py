import sys
import numpy as np
from audio_kit import Mix, SR
import wave

class FastMix(Mix):
    # kit'teki write() ile aynı sonuç; ducking için kümülatif toplam (hızlı)
    def write(self, path):
        k = int(0.25 * SR); h = (k - 1) // 2
        c = np.concatenate([[0.0], np.cumsum(self.act)])
        i = np.arange(self.N); lo = np.clip(i + h - k + 1, 0, self.N); hi = np.clip(i + h + 1, 0, self.N)
        duck = 1 - 0.55 * (c[hi] - c[lo]) / k
        out = self.v + (self.music + self.sfx) * duck
        out *= np.clip((self.D - self.t) / 2, 0, 1)
        out /= np.max(np.abs(out)) * 1.12
        w = wave.open(path, 'w'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close()

D = 59.0
m = FastMix(D=D)
# anlatım (scene.html ile aynı başlangıçlar)
VO = [(0.3,'l01'),(4.8,'l02'),(9.9,'l03'),(13.9,'l04'),(20.8,'l05'),(25.3,'l06'),
      (29.1,'l07'),(32.4,'l08'),(36.0,'l09'),(40.3,'l10'),(45.0,'l11'),(50.6,'l12')]
for st, n in VO: m.vo(f'seslendirme/{n}.wav', st)
m.pad(gain=0.045, swell_from=42)
# kanca + sabah
m.note(0.4, 329.6, g=0.05, dur=2.5); m.note(2.9, 293.7, g=0.05, dur=2.5)
m.click(4.95, gain=0.12)                                   # ayna lambası
m.ding(6.75, gain=0.08)                                    # 07:12
m.keyboard(10.4, 13.8, gain=0.018); m.keyboard(11.5, 13.8, gain=0.014)   # fırça sesi
m.buzz(13.0, dur=0.5, gain=0.04)
# telaş
for t0 in [13.85, 20.6, 25.2, 29.0, 32.3, 35.9, 40.2]: m.whoosh(t0-0.15, 0.35, 0.06)
m.steps(13.9, 19.8, rate=0.22, gain=0.12)
m.ping(16.0, gain=0.07); m.ping(16.8, gain=0.07)
m.click(17.75, gain=0.18)                                  # kapı açılır
m.thud(19.95, f=48, gain=0.45); m.click(19.95, gain=0.3)   # kapı çarpar
# akşam
m.note(21.0, 220, g=0.05, dur=3); m.note(23.3, 196, g=0.05, dur=3)
m.buzz(25.55, dur=0.6, gain=0.06); m.ping(25.6, gain=0.1)  # "İyi geceler"
m.click(28.05, gain=0.15)                                  # lamba söner
# ayna, sebepler
m.note(30.6, 261.6, g=0.05, dur=1.8); m.note(31.7, 329.6, g=0.05, dur=1.8)
m.note(32.6, 246.9, g=0.06, dur=3); m.note(34.4, 220, g=0.06, dur=3)
for t0 in [36.1, 37.0, 37.8]: m.tick(t0, gain=0.1); m.whoosh(t0-0.1, 0.3, 0.05)
for t0 in [38.65, 38.85, 39.05]: m.thud(t0, f=70, gain=0.18)
# dönüm: sarılma
m.ding(40.4, gain=0.06)
m.keyboard(40.3, 42.5, gain=0.016)
m.click(43.2, gain=0.12)                                   # fırça bardağa
m.steps(43.3, 44.2, rate=0.3, gain=0.1)
for t0, f in [(44.2,261.6),(45.8,293.7),(47.0,329.6),(48.4,392),(49.3,523.3),(50.8,392),(52.1,440),(53.8,523.3)]:
    m.note(t0, f, g=0.07, dur=2.8)
m.ping(48.6, gain=0.08); m.ping(49.4, gain=0.1)
m.write(sys.argv[1])
