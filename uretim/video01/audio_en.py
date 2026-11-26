# İngilizce sürüm ses miksi (audio.py kopyası). build.sh uretim/video01 en
import numpy as np, wave, sys, subprocess, os
SR=44100; D=64.5; N=int(SR*D); t=np.arange(N)/SR; sfx=np.zeros(N)
rng=np.random.default_rng(1); HERE=os.path.dirname(os.path.abspath(__file__))
# sahne zaman eğrisi (scene.html WARP ile aynı): yeni zaman <-> eski zaman
WARP=[(0,0),(14.4,14.4),(15.6,15.35),(22.2,21.4),(28.4,27.4),(35.1,34.0),(39.9,39.0),(46.5,44.3),(52.4,50.6),(58.6,56.6),(64.5,62.5)]
def W(old): return float(np.interp(old,[o for n,o in WARP],[n for n,o in WARP]))
def env(t0,dur,a=0.005,r=None):
    r=r or dur; x=t-t0; e=np.zeros(N); m=(x>=0)&(x<dur*3)
    xm=x[m]; e[m]=np.where(xm<a,xm/a,np.exp(-(xm-a)/r*4)); return e
def load(path,tempo=1.0):
    raw=subprocess.run(['ffmpeg','-loglevel','error','-i',path,'-af',f'atempo={tempo}','-f','s16le','-ac','1','-ar',str(SR),'-'],capture_output=True).stdout
    return np.frombuffer(raw,np.int16).astype(float)/32768
# --- anlatım (yeni zaman) — İNGİLİZCE: Cartesia 'Kyle', uzun duraklamalar 0.3-0.45 sn'ye kısaltıldı; l01 %5, l05/l07/l09 %3 hızlandırılır
VO=[(0.3,'l01',1.05),(4.0,'l02',1),(10.3,'l03',1),(15.6,'l04',1),(22.2,'l05',1.03),(28.4,'l06',1),(35.1,'l07',1.03),(39.9,'l08',1),(46.5,'l09',1.03),(52.4,'l10',1),(58.6,'l11',1)]
vo=np.zeros(N); act=np.zeros(N)
for st,n,tp in VO:
    a=load(f'{HERE}/seslendirme_en/{n}.wav',tp).copy(); a/=np.sqrt(np.mean(a**2))+1e-9; a*=0.12
    i=int(st*SR); L=min(len(a),N-i); vo[i:i+L]+=a[:L]; act[i:i+L]=1
k=int(0.25*SR)
# np.convolve(act,np.ones(k)/k,'same') ile aynı sonuç, kayan toplamla (dakikalar yerine milisaniye)
cs=np.concatenate([[0],np.cumsum(act)]); o=(k-1)//2; ii=np.arange(N)
duck=(cs[np.clip(ii+k-o,0,N)]-cs[np.clip(ii-o,0,N)])/k; duck=1-0.55*duck
# --- ambiyans
lfo=0.6+0.4*np.sin(2*np.pi*0.07*t)
pad=(np.sin(2*np.pi*55*t)+0.6*np.sin(2*np.pi*82.4*t)+0.35*np.sin(2*np.pi*110.3*t)+0.25*np.sin(2*np.pi*164.8*t)+0.12*np.sin(2*np.pi*246.9*t))*lfo
music=pad*0.05*np.clip(t/2,0,1)*(1+0.6*np.clip((t-W(44))/6,0,1))
def note(t0,f,g=0.08,dur=2.5):
    e=env(t0,dur,0.01,dur); return g*e*(np.sin(2*np.pi*f*t)+0.3*np.sin(2*np.pi*2*f*t)+0.1*np.sin(2*np.pi*3*f*t))
for o,f in [(34.2,440),(35.4,392),(36.6,349.2),(39.2,329.6),(40.6,293.7),(42.4,261.6),(50.6,220),(53.0,196),(56.6,261.6),(58.3,329.6),(59.3,392)]:
    music+=note(W(o),f)
# --- efektler (ofis: zaman aynı)
for kk in np.arange(0.3,7.6,0.11):
    kk+=rng.uniform(-0.03,0.03); sfx+=0.04*rng.standard_normal(N)*env(kk,0.02,0.001,0.015)
for kk in np.arange(8.6,12.1,60/150): sfx+=0.22*np.sin(2*np.pi*70*(t-kk))*env(kk,0.06,0.002,0.05)
sfx+=0.15*np.sin(2*np.pi*1200*t)*env(6.9,0.05,0.001,0.04)
b=W(21.4); m=(t>b)&(t<b+0.9)&((((t-b)*6)%1)<0.6); sfx+=0.09*np.sign(np.sin(2*np.pi*150*t))*m
for o in [25.3,30.2,31.4,32.6]:
    kk=W(o); sfx+=0.14*(np.sin(2*np.pi*1318*t)+0.5*np.sin(2*np.pi*1975*t))*env(kk,0.25,0.003,0.2)
    sfx+=0.10*np.sin(2*np.pi*1760*t)*env(kk+0.09,0.25,0.003,0.2)
for o in list(np.arange(33.7,35.5,0.32))+list(np.arange(40.0,41.6,0.32)):
    kk=W(o); sfx+=0.08*np.sin(2*np.pi*95*(t-kk))*env(kk,0.05,0.002,0.04)
sfx+=0.2*rng.standard_normal(N)*env(W(42.55),0.01,0.0005,0.008)  # EN: ışık 'the light goes out' ile ~0.4 sn geç söner
for o,f in [(50.6,45),(53.0,40)]:
    kk=W(o); sfx+=0.35*np.sin(2*np.pi*f*t*(1+0.3*np.exp(-np.clip(t-kk,0,None)*8)))*env(kk,1.5,0.005,1.2)
out=vo+(music+sfx)*duck
out*=np.clip((D-t)/2,0,1)
out/=np.max(np.abs(out))*1.12
w=wave.open(sys.argv[1],'w');w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((out*32767).astype(np.int16).tobytes());w.close()
