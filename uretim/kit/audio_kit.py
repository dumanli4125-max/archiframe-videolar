"""syntetic.tr ses kiti. Kullanım: videoNN/audio.py içinde
    from audio_kit import Mix
    m = Mix(D=60)                                 # süre (sn)
    m.vo('seslendirme/l01.wav', 0.3)              # anlatım satırı (tempo=1.06 ile perde korunarak hızlanır)
    m.pad(); m.keyboard(0.3, 7); m.ping(24); ...  # efektler
    m.write(sys.argv[1])
Anlatım konuşurken müzik/efekt otomatik kısılır (ducking)."""
import numpy as np, wave, subprocess, os

SR = 44100

class Mix:
    def __init__(self, D, seed=1, base=None):
        self.D = D; self.N = int(SR * D); self.t = np.arange(self.N) / SR
        self.v = np.zeros(self.N); self.act = np.zeros(self.N)
        self.music = np.zeros(self.N); self.sfx = np.zeros(self.N)
        self.rng = np.random.default_rng(seed)
        self.base = base or os.getcwd()

    # ---- yardımcılar
    def env(self, t0, dur, a=0.005, r=None):
        r = r or dur; x = self.t - t0; e = np.zeros(self.N); m = (x >= 0) & (x < dur * 3)
        xm = x[m]; e[m] = np.where(xm < a, xm / a, np.exp(-(xm - a) / r * 4)); return e

    def load(self, path, tempo=1.0):
        path = path if os.path.isabs(path) else os.path.join(self.base, path)
        raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', path, '-af', f'atempo={tempo}', '-f', 's16le',
                              '-ac', '1', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
        return np.frombuffer(raw, np.int16).astype(float) / 32768

    # ---- anlatım
    def vo(self, path, start, tempo=1.0, gain=0.12):
        a = self.load(path, tempo).copy(); a /= np.sqrt(np.mean(a ** 2)) + 1e-9; a *= gain
        i = int(start * SR); L = min(len(a), self.N - i)
        self.v[i:i + L] += a[:L]; self.act[i:i + L] = 1
        return len(a) / SR  # satır süresi (sn)

    # ---- müzik
    def pad(self, gain=0.05, swell_from=None):
        t = self.t; lfo = 0.6 + 0.4 * np.sin(2 * np.pi * 0.07 * t)
        p = (np.sin(2*np.pi*55*t) + 0.6*np.sin(2*np.pi*82.4*t) + 0.35*np.sin(2*np.pi*110.3*t)
             + 0.25*np.sin(2*np.pi*164.8*t) + 0.12*np.sin(2*np.pi*246.9*t)) * lfo
        g = gain * np.clip(t / 2, 0, 1)
        if swell_from is not None: g = g * (1 + 0.6 * np.clip((t - swell_from) / 6, 0, 1))
        self.music += p * g

    def note(self, t0, f, g=0.08, dur=2.5):
        e = self.env(t0, dur, 0.01, dur); t = self.t
        self.music += g * e * (np.sin(2*np.pi*f*t) + 0.3*np.sin(2*np.pi*2*f*t) + 0.1*np.sin(2*np.pi*3*f*t))

    def tension(self, t0, t1, gain=0.05):
        """Test videoları için gerilim: yükselen nabız (tik-tak)."""
        for k in np.arange(t0, t1, 0.5):
            self.sfx += gain * 2 * np.sin(2*np.pi*900*self.t) * self.env(k, 0.04, 0.001, 0.03)

    # ---- efektler
    def keyboard(self, t0, t1, gain=0.04):
        for k in np.arange(t0, t1, 0.11):
            k += self.rng.uniform(-0.03, 0.03)
            self.sfx += gain * self.rng.standard_normal(self.N) * self.env(k, 0.02, 0.001, 0.015)
    def steps(self, t0, t1, rate=0.4, gain=0.22, f=70):
        for k in np.arange(t0, t1, rate): self.sfx += gain * np.sin(2*np.pi*f*(self.t-k)) * self.env(k, 0.06, 0.002, 0.05)
    def tick(self, t0, gain=0.15):
        self.sfx += gain * np.sin(2*np.pi*1200*self.t) * self.env(t0, 0.05, 0.001, 0.04)
    def buzz(self, t0, dur=0.9, gain=0.09):
        t = self.t; m = (t > t0) & (t < t0 + dur) & ((((t - t0) * 6) % 1) < 0.6)
        self.sfx += gain * np.sign(np.sin(2*np.pi*150*t)) * m
    def ping(self, t0, gain=0.14):
        t = self.t
        self.sfx += gain * (np.sin(2*np.pi*1318*t) + 0.5*np.sin(2*np.pi*1975*t)) * self.env(t0, 0.25, 0.003, 0.2)
        self.sfx += gain * 0.7 * np.sin(2*np.pi*1760*t) * self.env(t0 + 0.09, 0.25, 0.003, 0.2)
    def click(self, t0, gain=0.2):
        self.sfx += gain * self.rng.standard_normal(self.N) * self.env(t0, 0.01, 0.0005, 0.008)
    def thud(self, t0, f=45, gain=0.35):
        t = self.t; self.sfx += gain * np.sin(2*np.pi*f*t*(1+0.3*np.exp(-np.clip(t-t0, 0, None)*8))) * self.env(t0, 1.5, 0.005, 1.2)
    def whoosh(self, t0, dur=0.5, gain=0.12):
        n = self.rng.standard_normal(self.N); e = self.env(t0, dur, dur*0.6, dur)
        k = int(0.002*SR); c = np.concatenate([[0], np.cumsum(n)]); sm_ = (c[k:] - c[:-k]) / k
        self.sfx += gain * np.pad(sm_, (0, self.N - len(sm_))) * e
    def ding(self, t0, gain=0.15):  # doğru cevap
        for f, d in [(1046.5, 0), (1318.5, 0.12), (1568, 0.24)]:
            self.sfx += gain * np.sin(2*np.pi*f*self.t) * self.env(t0 + d, 0.4, 0.003, 0.35)

    def write(self, path):
        k = int(0.25 * SR); c = np.concatenate([[0], np.cumsum(self.act)])  # hızlı kayan ortalama
        lo = np.clip(np.arange(self.N) - k // 2, 0, self.N); hi = np.clip(np.arange(self.N) + k // 2, 0, self.N)
        duck = 1 - 0.55 * (c[hi] - c[lo]) / k
        out = self.v + (self.music + self.sfx) * duck
        out *= np.clip((self.D - self.t) / 2, 0, 1)
        out /= np.max(np.abs(out)) * 1.12
        w = wave.open(path, 'w'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close()
