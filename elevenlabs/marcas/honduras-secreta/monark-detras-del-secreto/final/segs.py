import subprocess, json
M = '/tmp/claude-0/-home-user-Nicole-projects/dd5b2fc2-184e-5514-b789-f8432119b327/scratchpad/monark/'
def R(*a): subprocess.run(a, check=True)
V = "scale=1080:1920,setsar=1,fps=30"
A = "aformat=sample_rates=48000:channel_layouts=stereo"
segs = []
# 1 · gancho (video compuesto + audio limpio de la escena 1)
R('ffmpeg','-loglevel','error','-y','-i',M+'g1/Escena1_prueba_cel.mp4','-vf',V,'-af',A,'-c:v','libx264','-crf','16','-pix_fmt','yuv420p','-c:a','pcm_s16le','s1.mov')
# 2 · la idea (desde 2.6 s)
R('ffmpeg','-loglevel','error','-y','-ss','2.6','-i',M+'g2/Escena2_prueba_cel.mp4','-vf',V,'-af',A,'-c:v','libx264','-crf','16','-pix_fmt','yuv420p','-c:a','pcm_s16le','s2.mov')
# 3 · entra Claudio
R('ffmpeg','-loglevel','error','-y','-i',M+'g3/Escena3_prueba_cel.mp4','-vf',V,'-af',"volume='if(lt(t,0.8),0,1)':eval=frame,"+A,'-c:v','libx264','-crf','16','-pix_fmt','yuv420p','-c:a','pcm_s16le','s3.mov')
# 4 · el taller: Veo 0–1.1 + montaje 6 s + Veo 7.0–8.0
g = M + 'g5/'
R('ffmpeg','-loglevel','error','-y','-i',g+'v4.mp4','-i',g+'taller.mp4','-filter_complex',
  f"[0:v]trim=0:1.1,setpts=PTS-STARTPTS,{V}[a];[1:v]{V},setpts=PTS-STARTPTS[b];[0:v]trim=7.0:8.0,setpts=PTS-STARTPTS,{V}[c];[a][b][c]concat=n=3:v=1:a=0[v];"
  f"[0:a]atrim=0:1.1,asetpts=PTS-STARTPTS[x];anullsrc=r=48000:cl=stereo,atrim=0:6[y];[0:a]atrim=7.0:8.0,asetpts=PTS-STARTPTS[z];[x][y][z]concat=n=3:v=0:a=1,{A}[au]",
  '-map','[v]','-map','[au]','-c:v','libx264','-crf','16','-pix_fmt','yuv420p','-c:a','pcm_s16le','s4.mov')
# 5 · llamado a la estrella: audio de Veo (chasquido y aleteo) bajo, voz de José latam encima
R('ffmpeg','-loglevel','error','-y','-i',g+'v5.mp4','-i',g+'guara_v5.mp3','-filter_complex',
  f"[0:v]trim=0:7.3,setpts=PTS-STARTPTS,{V}[v];[0:a]atrim=0:7.3,volume='if(between(t,0.3,1.0)+gte(t,4.4),0,0.9)':eval=frame[x];[1:a]adelay=4680|4680[y];[x][y]amix=inputs=2:normalize=0,atrim=0:7.3,{A}[au]",
  '-map','[v]','-map','[au]','-c:v','libx264','-crf','16','-pix_fmt','yuv420p','-c:a','pcm_s16le','s5.mov')
# 6 · el rodaje
R('ffmpeg','-loglevel','error','-y','-i',M+'g4/Escena6_rodaje_prueba_cel.mp4','-vf',V,'-af',A,'-c:v','libx264','-crf','16','-pix_fmt','yuv420p','-c:a','pcm_s16le','s6.mov')
# 7 · la revisión (zoom leve para quitar la franja blanca de arriba)
R('ffmpeg','-loglevel','error','-y','-i',g+'v7.mp4','-vf',"crop=iw/1.05:ih/1.05:(iw-iw/1.05)/2:ih-ih/1.05," + V,'-af',A,'-c:v','libx264','-crf','16','-pix_fmt','yuv420p','-c:a','pcm_s16le','s7.mov')
# 8 · cierre: final real de la escena 1 + tarjeta final (último cuadro congelado y oscurecido)
R('ffmpeg','-loglevel','error','-y','-ss','4.4','-i',M+'g1/Escena1_prueba_cel.mp4','-filter_complex',
  f"[0:v]{V},tpad=stop_mode=clone:stop_duration=3.6[v];[0:a]{A},apad=pad_dur=3.6[au]",'-map','[v]','-map','[au]','-c:v','libx264','-crf','16','-pix_fmt','yuv420p','-c:a','pcm_s16le','s8.mov')
durs = []
for i in range(1, 9):
    d = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f's{i}.mov'])); durs.append(d)
open('list.txt','w').write(''.join(f"file 's{i}.mov'\n" for i in range(1, 9)))
R('ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i','list.txt','-c:v','libx264','-crf','16','-pix_fmt','yuv420p','-r','30','-c:a','pcm_s16le','base.mov')
st = [sum(durs[:i]) for i in range(8)]
json.dump({'durs': durs, 'starts': st}, open('tl.json','w')); print([round(x,2) for x in durs], [round(x,2) for x in st], round(sum(durs),2))
