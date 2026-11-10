# Mezcla de audio común para ambos formatos (mismos tiempos)
import json, subprocess
tl = json.load(open('timeline_h.json')); S = tl['start']; T = round(tl['total'], 3); Q0 = tl['q0']
segs = [('i0','sync/i0_h.mov',0),('i1','sync/i1_h.mov',0),('s1','sync/s1_h.mov',0),('s1b','prep/s1_h.mp4',3.77),('i2','sync/i2_h.mov',0),
        ('s2','prep/s2_h.mp4',0),('i3','sync/i3_h.mov',0),('s3','prep/s3_h.mp4',0),('i4','sync/i4_h.mov',0),('s4','prep/s4_h.mp4',0),
        ('i5','sync/i5_h.mov',0),('s5','prep/s5_h.mp4',0),('i6','sync/i6c_h.mov',0),('s6','prep/s6_h.mp4',0),('i7','sync/i7_h.mov',0),('i8','prep/i8_h.mp4',0),('s7','sync/s7_h.mov',0)]
order = list(S.keys()); nxt = {k: (S[order[i+1]] if i+1 < len(order) else T) for i, k in enumerate(order)}
ins, fc, labs = [], '', []
ms = lambda x: int(round(x * 1000))
for j, (k, f, ss) in enumerate(segs):
    d = nxt[k] - S[k]; ins += ['-i', f]
    vol = {'s2': 1.0, 's3': 1.1, 's4': 1.0, 's5': .8, 's6': .7, 'i8': .4}.get(k, 1.0)
    fc += f"[{j}:a]aresample=48000,atrim={ss}:{ss+d:.3f},asetpts=PTS-STARTPTS,volume={vol},afade=t=in:d=0.02,afade=t=out:st={max(d-0.03,0):.3f}:d=0.03,adelay={ms(S[k])}|{ms(S[k])},apad=whole_dur={T}[c{j}];"
    labs.append(f'[c{j}]')
extra = [('musica_catr.mp3', None), ('punta.mp3', S['s6']), ('vo/q_raymond_b.mp3', Q0), ('sfx_power.mp3', S['s3'] + 3.1), ('sfx_wh.mp3', S['m1'] - .25), ('sfx_scratch.mp3', S['s1'] - .05)]
base = len(segs)
for i, (f, t0) in enumerate(extra): ins += ['-i', f]
fc += ''.join(labs) + f"amix=inputs={len(labs)}:normalize=0,loudnorm=I=-15:TP=-2,aresample=48000,asplit=2[dia1][dia2];"
# música: baja durante la fiesta (entra la punta) y sube en el final emotivo
fc += (f"[{base}:a]aresample=48000,atrim=0:{T},volume='if(between(t,{S['s6']-.3:.2f},{S['i7']:.2f}),0.08,if(gt(t,{S['m1']-.3:.2f}),0.42,0.30))':eval=frame,"
       f"afade=t=out:st={T-2.5:.2f}:d=2.5,apad=whole_dur={T}[mus];[mus][dia2]sidechaincompress=threshold=0.03:ratio=5:attack=20:release=400[md];")
fc += f"[{base+1}:a]aresample=48000,atrim=0:{S['i7']-S['s6']:.3f},volume=0.45,afade=t=in:d=0.3,afade=t=out:st={S['i7']-S['s6']-.6:.3f}:d=0.6,adelay={ms(S['s6'])}|{ms(S['s6'])},apad=whole_dur={T}[pu];"
fc += f"[{base+2}:a]aresample=48000,highpass=f=80,loudnorm=I=-16:TP=-2,aresample=48000,adelay={ms(Q0)}|{ms(Q0)},apad=whole_dur={T}[q];"
fx = ''
for i, (f, t0) in enumerate(extra[3:]):
    fc += f"[{base+3+i}:a]aresample=48000,volume=0.5,adelay={ms(t0)}|{ms(t0)},apad=whole_dur={T}[x{i}];"; fx += f'[x{i}]'
fc += f"[dia1][md][pu][q]{fx}amix=inputs={4+len(extra)-3}:normalize=0:duration=longest,atrim=0:{T},loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]"
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y'] + ins + ['-filter_complex', fc, '-map', '[a]', '-c:a', 'pcm_s16le', 'mix_catr.wav'], check=True)
print('mezcla', T)
