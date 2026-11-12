import subprocess, json, os
R = lambda *a: subprocess.run(a, check=True)
# (video, desde, hasta, velocidad, audio de diálogo o None)
SEGS = [('hd/e01.mov', .6, 6.0, .75, None), ('v2/sync/A.mp4', 0, 7.92, 1, 'v2/sync/A.wav'), ('v2/sync/B1.mp4', 0, 6.5, 1, 'v2/sync/B1.wav'),
        ('v2/sync/B2.mp4', 1.8, 5.71, 1, 'v2/sync/B2.wav'), ('v2/sync/C.mp4', 0, 7.25, 1, 'v2/sync/C.wav'), ('v2/sync/D.mp4', 0, 7.3, 1, 'v2/sync/D.wav'),
        ('v2/sync/E.mp4', 0, 8.25, 1, 'v2/sync/E.wav'), ('v2/sync/F.mp4', 0, 6.04, 1, 'v2/sync/F.wav'), ('v2/sync/G.mp4', 0, 7.54, 1, 'v2/sync/G.wav'),
        ('v2/sync/H.mp4', 0, 6.0, 1, 'v2/sync/H.wav'), ('v2/sync/I.mp4', 0, 7.42, 1, 'v2/sync/I.wav'), ('hd/e11a.mov', 0, 8, .6, None),
        ('hd/e11b.mov', 0, .42, .09, None), ('v2/sync/J.mp4', 0, 6.21, 1, 'v2/sync/J.wav'), ('vfix/e13.mp4', 0, 8, 1, None)]
t = 0; starts = []; files = []; afiles = []
for k, (f, a, b, sp, au) in enumerate(SEGS):
    o = f'v2/seg/{k:02d}.mp4'; d = (b - a) / sp
    mi = ',minterpolate=fps=24:mi_mode=blend' if sp < 1 else ''
    R('ffmpeg','-loglevel','error','-y','-i',f,'-vf',f'trim={a}:{b},setpts=(PTS-STARTPTS)/{sp}{mi},fps=24,scale=1080:1920,setsar=1','-an','-t',f'{d:.3f}','-c:v','libx264','-crf','14','-pix_fmt','yuv420p','-r','24',o)
    d = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',o]))
    starts.append(t); files.append(o); afiles.append((au, a, t, d)); t += d
open('v2/seg/list.txt','w').write(''.join(f"file '{os.path.basename(x)}'\n" for x in files))
R('ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i','v2/seg/list.txt','-c','copy','v2/seg/base.mp4')
END = 5.9; total = t + END
R('ffmpeg','-loglevel','error','-y','-i','v2/seg/base.mp4','-vf',f'tpad=stop_mode=clone:stop_duration={END}','-c:v','libx264','-crf','14','-pix_fmt','yuv420p','v2/seg/base2.mp4')
json.dump({'starts': starts, 'total': total, 'audio': afiles}, open('v2/seg/tl.json','w'))
print([round(s, 2) for s in starts], round(total, 2))
