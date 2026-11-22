"""Örnek videonun müziği ve ses efektleri (lisans gerektirmez, numpy ile üretilir).
Çıktı: audio.wav (35 sn, 44.1 kHz stereo). Efekt zamanları scene.html'deki sahnelerle eşleşir."""
import numpy as np, wave
sr=44100;D=47;N=sr*D;L=np.zeros(N);R=np.zeros(N)
rng=np.random.default_rng(7)
def add(sig,t,g=1.0,pan=0.0):
    i=int(t*sr);n=min(len(sig),N-i)
    if n<=0:return
    L[i:i+n]+=sig[:n]*g*(1-max(pan,0));R[i:i+n]+=sig[:n]*g*(1+min(pan,0))
def env(n,a,d):
    t=np.arange(n)/sr;return np.minimum(1,t/a)*np.exp(-t/d)
def lp(x,k):
    y=np.zeros_like(x);s=0
    for i in range(len(x)):s+=k*(x[i]-s);y[i]=s
    return y
# müzik: 100 bpm davul + bas + pad
bpm=100;beat=60/bpm
kick_n=int(.35*sr);tk=np.arange(kick_n)/sr
kick=np.sin(2*np.pi*(45+90*np.exp(-tk*30))*tk)*np.exp(-tk*9)
hat=rng.standard_normal(int(.05*sr));hat=np.diff(hat,prepend=0)*env(len(hat),.001,.012)
bass_notes=[41.2,41.2,49.0,36.7]
t=0;b=0
while t<D-1.2:
    add(kick,t,.55);add(hat,t+beat/2,.12,.3)
    if b%4==0:
        f=bass_notes[(b//4)%4];n=int(beat*4*sr);tt=np.arange(n)/sr
        saw=2*((tt*f)%1)-1;add(lp(saw*np.minimum(1,tt/.05)*np.exp(-tt/3),.05),t,.35)
    t+=beat;b+=1
tt=np.arange(N)/sr
pad=(np.sin(2*np.pi*110*tt)+.6*np.sin(2*np.pi*164.8*tt+.5)+.4*np.sin(2*np.pi*130.8*tt))*(.5+.5*np.sin(2*np.pi*tt/8))
L+=pad*.03;R+=np.roll(pad,800)*.03
fade=np.ones(N);fade[-int(1.5*sr):]=np.linspace(1,0,int(1.5*sr));L*=fade;R*=fade
# efektler
def slam():
    n=int(.8*sr);t=np.arange(n)/sr
    return np.sin(2*np.pi*(38+140*np.exp(-t*25))*t)*np.exp(-t*5)+lp(rng.standard_normal(n),.15)*np.exp(-t*14)*.8
def pop(f=900):
    n=int(.09*sr);t=np.arange(n)/sr;return np.sin(2*np.pi*(f*np.exp(-t*12))*t)*env(n,.002,.03)
def whoosh(d=.7):
    n=int(d*sr);t=np.arange(n)/sr;x=rng.standard_normal(n);e=np.sin(np.pi*t/d)**2;k=.02+.25*e
    y=np.zeros(n);s=0
    for i in range(n):s+=k[i]*(x[i]-s);y[i]=s
    return y*e*2.2
def tick():
    n=int(.03*sr);t=np.arange(n)/sr;return np.sin(2*np.pi*2400*t)*np.exp(-t*200)
def alarm():
    n=int(.25*sr);t=np.arange(n)/sr;return np.sin(2*np.pi*220*t)*np.sin(np.pi*t/.25)
for a in [0,2.6,7,15,19.5,24,29,37,43]: add(slam(),a,.9)      # başlık darbeleri
add(pop(600),2.95,.6)                                            # skor
for i in range(3): add(pop(900),3.6+i*.35,.5,(i-1)*.2)           # gol satırları
for i in range(8): add(pop(1100),7.6+i*.1+.08,.35,(i-3.5)*.1)    # rakip diskler
for i in range(10): add(pop(800),8.6+i*.1+.08,.4,(i-4.5)*.1)     # GS diskleri
for a,d in [(2.5,.6),(15.9,1.0),(20.3,1.0),(21.6,.8),(25.3,.9)]: add(whoosh(d),a,.5)
for a in [17.8,22.4]: add(slam(),a,.5); add(pop(1400),a,.4)      # GS golleri
add(slam(),26.7,.4)                                              # Bayo golü
for i in range(3): add(alarm(),24.3+i*.8,.22)
for a in [29.2,31.8,34.4,37.2]:
    for k in range(12): add(tick(),a+k*.075,.35)                  # sayaçlar
mix=np.stack([L,R],1);mix/=np.max(np.abs(mix))*1.12
w=wave.open('audio_gs.wav','wb');w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes((mix*32767).astype(np.int16).tobytes());w.close()
print('audio.wav hazır')
