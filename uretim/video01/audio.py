import numpy as np, wave, sys
SR=44100; D=27; t=np.arange(int(SR*D))/SR; out=np.zeros_like(t)
rng=np.random.default_rng(1)
def env(t0,dur,a=0.005,r=None):
    r=r or dur; x=t-t0; e=np.where(x<0,0,np.where(x<a,x/a,np.exp(-(x-a)/r*4))); e[x>dur*3]=0; return e
# ambiyans: düşük drone, yavaş LFO; finalde koyulaşır
lfo=0.6+0.4*np.sin(2*np.pi*0.08*t)
pad=(np.sin(2*np.pi*55*t)+0.6*np.sin(2*np.pi*82.4*t)+0.35*np.sin(2*np.pi*110.3*t)+0.2*np.sin(2*np.pi*164.8*t))*lfo
out+=0.06*pad*np.clip(t/2,0,1)
# klavye 0.3-4.8
for k in np.arange(0.3,4.8,0.11):
    k+=rng.uniform(-0.03,0.03); n=rng.standard_normal(len(t))*env(k,0.02,0.001,0.015); out+=0.05*n
# adımlar 5.7-8.5
for k in np.arange(5.75,8.5,60/170):
    out+=0.25*np.sin(2*np.pi*70*(t-k))*env(k,0.06,0.002,0.05)
# saat 18:00 'tık' 4.5
out+=0.15*np.sin(2*np.pi*1200*t)*env(4.5,0.05,0.001,0.04)
# titreşim 11.0-11.9
m=(t>11)&(t<11.9)&((((t-11)*6)%1)<0.6); out+=0.18*np.sign(np.sin(2*np.pi*150*t))*m*0.5
# bildirim pingleri
for k in [11.2,15.6,16.6,17.6]:
    out+=0.18*(np.sin(2*np.pi*1318*t)+0.5*np.sin(2*np.pi*1975*t))*env(k,0.25,0.003,0.2)
    out+=0.12*np.sin(2*np.pi*1760*t)*env(k+0.09,0.25,0.003,0.2)
# final darbe 21.0 ve vurgu 22.9
for k,f in [(21.0,45),(22.9,40)]:
    out+=0.5*np.sin(2*np.pi*f*t*(1+0.3*np.exp(-(t-k).clip(0)*8)))*env(k,1.5,0.005,1.2)
fade=np.clip((D-t)/1.5,0,1); out*=fade
out/=np.max(np.abs(out))*1.15
w=wave.open(sys.argv[1],'w');w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((out*32767).astype(np.int16).tobytes());w.close()
