# Mezcla v2: voces limpias (sin audio de Veo salvo diálogos útiles), ambientes y efectos de comedia
import json, subprocess
tl = json.load(open('timeline_h.json')); S = tl['start']; T = round(tl['total'], 3); Q0 = tl['q0']
STK = json.load(open('stickers_h.json'))
ms = lambda x: int(round(max(0, x) * 1000))
ins, fc, L = [], '', []
def inp(f): ins.extend(['-i', f]); return len(ins) // 2 - 1
def place(f, t0, vol=1.0, trim=None, extra=''):
    j = inp(f); tr = f'atrim={trim[0]}:{trim[1]},asetpts=PTS-STARTPTS,' if trim else ''
    global fc; lab = f'x{len(L)}'
    fc += f"[{j}:a]aresample=48000,{tr}volume={vol}{extra},adelay={ms(t0)}|{ms(t0)},apad=whole_dur={T}[{lab}];"; L.append(lab); return lab
off = lambda k: json.load(open(f'sync/{k}_h.mov.json'))['off']
# --- diálogo (voces originales, sin tocar)
dlg = []
for seg, k, vk in [('i0','i0','i0_c'),('i1','i1','i1_b'),('s1','s1','s1_c'),('i2','i2','i2_b'),('i3','i3','i3_c'),('i4','i4','i4_b'),('i5','i5','i5_a'),('i6','i6c','i6_c'),('i7','i7','i7_c'),('s7','s7','s7_c')]:
    dlg.append(place(f'vo/{vk}.mp3', S[seg] + off(k)))
dlg.append(place('vo/q_raymond_b.mp3', Q0, .9))
dlg.append(place('prep/s2_h.mp4', S['s2'], 1.0, (0, 4.4)))                                 # cobrador
dlg.append(place('prep/s3_h.mp4', S['s3'], 1.0, (0.9, 6.9), ",volume='if(between(t,1.95,4.85),0,1)':eval=frame"))   # narración + ¡Nooo!
dlg.append(place('prep/s4_h.mp4', S['s4'], 1.0, (0, 2.5), ',afade=t=out:st=2.3:d=0.2'))  # señora de las baleadas
L.clear(); fc_d = fc; fc = ''
fc_d += ''.join(f'[{l}]' for l in dlg) + f"amix=inputs={len(dlg)}:normalize=0,highpass=f=70,acompressor=threshold=-18dB:ratio=3:attack=8:release=120,loudnorm=I=-15:TP=-2,aresample=48000,asplit=2[dia][dsc];"
# --- música
m1 = inp('musica2.mp3'); m2 = inp('musica_final.mp3')
fc += (f"[{m1}:a]aresample=48000,atrim=0:{S['i8']+.4:.3f},volume='if(between(t,{S['s6']-.2:.2f},{S['i7']:.2f}),0.10,0.42)':eval=frame,"
       f"afade=t=out:st={S['i8']-.1:.2f}:d=0.5,apad=whole_dur={T}[mA];"
       f"[{m2}:a]aresample=48000,volume=0.5,afade=t=in:d=1.0,afade=t=out:st={T-S['i8']-2.5:.2f}:d=2.5,adelay={ms(S['i8'])}|{ms(S['i8'])},apad=whole_dur={T}[mB];"
       f"[mA][mB]amix=inputs=2:normalize=0[mus];[mus][dsc]sidechaincompress=threshold=0.03:ratio=5:attack=20:release=400[md];")
# --- ambientes y efectos
fx = []
fx.append(place('punta.mp3', S['s6'], .5, (0, S['i7'] - S['s6']), f",afade=t=in:d=0.2,afade=t=out:st={S['i7']-S['s6']-.4:.2f}:d=0.4"))
fx.append(place('sfx2/hamaca.mp3', S['s1'], .35)); fx.append(place('sfx2/bus.mp3', S['s2'], .30))
fx.append(place('sfx2/fan.mp3', S['s5'], .35)); fx.append(place('sfx2/fiesta.mp3', S['s6'], .35))
fx.append(place('sfx2/olas.mp3', S['s7'], .35)); fx.append(place('sfx2/tvoff.mp3', S['s3'] + 1.9, .6)); fx.append(place('sfx2/shake.mp3', S['s3'] + 2.0, .5))
for k in ['s1', 's2', 's3', 's4', 's5', 's6']: fx.append(place('sfx2/crash.mp3', S[k] - .12, .45))
for a, b in STK: fx.append(place('sfx2/pop.mp3', a, .55))
fx.append(place('sfx2/sting.mp3', S['s2'] + 2.4, .45))
fx.append(place('sfx_scratch.mp3', S['m1'] - .3, .45))
fc += ''.join(f'[{l}]' for l in fx) + f"amix=inputs={len(fx)}:normalize=0[fxm];"
fc = fc_d + fc + f"[dia][md][fxm]amix=inputs=3:normalize=0:duration=longest,atrim=0:{T},loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]"
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y'] + ins + ['-filter_complex', fc, '-map', '[a]', '-c:a', 'pcm_s16le', 'mix2.wav'], check=True)
print('mezcla', T)
