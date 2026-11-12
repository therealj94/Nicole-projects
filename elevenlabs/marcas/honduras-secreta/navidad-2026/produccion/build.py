import subprocess, json, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R = lambda *a: subprocess.run(a, check=True)
# (archivo, desde, hasta, velocidad)
SEGS = [('hd/e01.mov',0,6,1), ('hd/e02s.mp4',0,6.5,1), ('hd/e03.mov',0,5.2,1), ('hd/e04.mov',2.8,8,1), ('hd/e05.mov',0,6.5,1),
        ('hd/e06.mov',0,4.8,1), ('hd/e07.mov',0,5,1), ('hd/e08s.mp4',0,4.92,1), ('hd/e09.mov',0,5.5,1), ('hd/e10.mov',0,8,1),
        ('hd/e11a.mov',0,8,.75), ('hd/e11b.mov',0,0.42,.15), ('hd/e12.mov',0,.35,.15), ('hd/e12s.mp4',0,6.0,1), ('hd/e13.mov',0,8,1)]
starts = []; t = 0; files = []
for k, (f, a, b, sp) in enumerate(SEGS):
    o = f'seg/{k:02d}.mp4'; d = (b - a) / sp
    vf = f"trim={a}:{b},setpts=(PTS-STARTPTS)/{sp},fps=24,scale=1080:1920,setsar=1"
    if sp < 1: vf = f"trim={a}:{b},setpts=(PTS-STARTPTS)/{sp},minterpolate=fps=24:mi_mode=blend,scale=1080:1920,setsar=1"
    R('ffmpeg','-loglevel','error','-y','-i',f,'-vf',vf,'-an','-t',f'{d:.3f}','-c:v','libx264','-crf','14','-pix_fmt','yuv420p','-r','24',o)
    d = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',o]))
    starts.append(t); t += d; files.append(o)
open('seg/list.txt','w').write(''.join(f"file '{os.path.basename(x)}'\n" for x in files))
R('ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i','seg/list.txt','-c','copy','seg/base.mp4')
END = 4.5; total = t + END
# cierre: último cuadro congelado
R('ffmpeg','-loglevel','error','-y','-i','seg/base.mp4','-vf',f'tpad=stop_mode=clone:stop_duration={END}','-c:v','libx264','-crf','14','-pix_fmt','yuv420p','seg/base2.mp4')
json.dump({'starts': starts, 'total': total}, open('seg/tl.json','w'))
print([round(s,2) for s in starts], round(total,2))
