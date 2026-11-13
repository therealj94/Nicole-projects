import json, subprocess, numpy as np
SR=48000; tl=json.load(open('seg/tl.json')); TOT=tl['total']; L=int(TOT*SR)
def load(f,a=0,d=None):
    cmd=['ffmpeg','-loglevel','error','-ss',f'{a:.3f}','-i',f]+(['-t',f'{d:.3f}'] if d else [])+['-ac','2','-ar',str(SR),'-f','f32le','-']
    return np.frombuffer(subprocess.run(cmd,stdout=subprocess.PIPE).stdout,np.float32).reshape(-1,2).copy()
def put(trk,x,t,g=1.0):
    p=int(t*SR); e=min(L,p+len(x))
    if e>p: trk[p:e]+=x[:e-p]*g
dlg=np.zeros((L,2),np.float32); fx=np.zeros((L,2),np.float32)
for au,t,d in tl['audio']:
    if au: put(dlg,load(au,0,d),t)
for f,t,g in [('au/noche.mp3',0,.25),('au/magia.mp3',6.5,.4),('au/twinkle.mp3',34.0,.6),('au/procesion.mp3',37.08,.4),('au/bronce.mp3',65.1,.5),('au/escuela.mp3',74.75,.3),('au/aves.mp3',89.13,.3),('au/twinkle.mp3',91.5,.6),('au/whoosh.mp3',95.2,.5)]:
    put(fx,load(f),t,g)
mus=np.zeros((L,2),np.float32); put(mus,load('au/musica.mp3'),0)
env=np.abs(dlg).max(1); k=int(.05*SR); env=np.convolve(env,np.ones(k)/k,'same')
act=(env>.01).astype(np.float32); sm=int(.35*SR); act=np.convolve(act,np.ones(sm)/sm,'same'); gain=1-.7*np.clip(act*1.6,0,1)
mix=dlg+fx+mus*.5*gain[:,None]
mix[-int(2*SR):]*=np.linspace(1,0,int(2*SR))[:,None]**.5
subprocess.run(['ffmpeg','-loglevel','error','-y','-f','f32le','-ar',str(SR),'-ac','2','-i','-','-af','loudnorm=I=-14:TP=-1.5','-ar',str(SR),'-c:a','pcm_s16le','mix.wav'],input=np.clip(mix,-1,1).astype(np.float32).tobytes(),check=True)
print('ok',TOT)
