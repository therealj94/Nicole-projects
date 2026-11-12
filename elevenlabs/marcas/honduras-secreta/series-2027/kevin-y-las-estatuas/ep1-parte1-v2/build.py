import subprocess, json, os
R = lambda *a: subprocess.run(a, check=True)
SEGS = [('A1',0,None),('A2',0,None),('B',0,None),('C1',0,None),('C2',0,None),('D1',0,None),('D2',0,None),('E',0,None),('F1',0,None),('F2',0,None),('G1',0,3.3),('G2',0,None),('G3',0,None),('H1',0,2.9),('H2',0,None),('I',0,None)]
os.makedirs('seg', exist_ok=True); t=0; files=[]; aud=[]; starts={}
for k,(n,a,b) in enumerate(SEGS):
    f = f'sync/{n}.mp4' if os.path.exists(f'sync/{n}.mp4') else f'hd/{n}.mp4'
    o = f'seg/{k:02d}.mp4'
    R('ffmpeg','-loglevel','error','-y','-i',f,'-vf',f'trim=0:{b},setpts=PTS-STARTPTS,fps=24,scale=1080:1920,setsar=1' if b else 'fps=24,scale=1080:1920,setsar=1','-an','-c:v','libx264','-crf','14','-pix_fmt','yuv420p','-r','24',o)
    d = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',o]))
    starts[n]=t; aud.append((f'sync/{n}.wav' if os.path.exists(f'sync/{n}.wav') else None, t, d)); files.append(o); t+=d
open('seg/list.txt','w').write(''.join(f"file '{os.path.basename(x)}'\n" for x in files))
R('ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i','seg/list.txt','-c','copy','seg/base.mp4')
END=3.5; R('ffmpeg','-loglevel','error','-y','-i','seg/base.mp4','-vf',f'tpad=stop_mode=clone:stop_duration={END}','-c:v','libx264','-crf','14','-pix_fmt','yuv420p','seg/base2.mp4')
json.dump({'starts':starts,'total':t+END,'audio':aud},open('seg/tl.json','w')); print({k:round(v,2) for k,v in starts.items()}, round(t+END,2))
