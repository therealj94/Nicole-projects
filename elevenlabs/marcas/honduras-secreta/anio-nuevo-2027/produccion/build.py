import subprocess, json, os
R = lambda *a: subprocess.run(a, check=True)
SEGS = [('01',0,None),('02a',0,None),('02b',0,None),('03',0,None),('04',0,None),('05a',0,None),('05b',0,None),('06',0,None),('07',0,None),('08',0,None),('09',0,None),('10',0,8.0),('11',0,None),('12',0,None)]
os.makedirs('seg', exist_ok=True); t=0; files=[]; aud=[]; starts={}
for k,(n,a,b) in enumerate(SEGS):
    f = f'sync/{n}.mp4' if os.path.exists(f'sync/{n}.mp4') else f'hd/{n}.mp4'
    o = f'seg/{k:02d}.mp4'
    R('ffmpeg','-loglevel','error','-y','-i',f,'-vf','fps=24,scale=1080:1920,setsar=1','-an','-c:v','libx264','-crf','14','-pix_fmt','yuv420p','-r','24',o)
    d = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',o]))
    starts[n]=t; aud.append((f'sync/{n}.wav' if os.path.exists(f'sync/{n}.wav') else None, t, d)); files.append(o); t+=d
open('seg/list.txt','w').write(''.join(f"file '{os.path.basename(x)}'\n" for x in files))
R('ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i','seg/list.txt','-c','copy','seg/base.mp4')
END=4.5; R('ffmpeg','-loglevel','error','-y','-i','seg/base.mp4','-vf',f'tpad=stop_mode=clone:stop_duration={END}','-c:v','libx264','-crf','14','-pix_fmt','yuv420p','seg/base2.mp4')
json.dump({'starts':starts,'total':t+END,'audio':aud},open('seg/tl.json','w')); print({k:round(v,2) for k,v in starts.items()}, round(t+END,2))
