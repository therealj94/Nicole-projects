import subprocess
T = 91.17
ins = ['video_ov.mp4','au/musica.mp3','vo/guara_e02.mp3','vo/guara_e08.mp3','vid/e08.mp4','vo/marta.mp3','vo/carlos.mp3',
       'au/sfx_wind.mp3','au/sfx_coffee.mp3','au/sfx_flash.mp3','au/sfx_rope.mp3','au/sfx_plane.mp3','au/sfx_airport.mp3','au/sfx_wind.mp3','au/sfx_box.mp3','au/sfx_fireworks.mp3','au/sfx_flap.mp3','au/sfx_fireworks.mp3']
args = []
for f in ins: args += ['-i', f]
def dl(i, t, v=1.0, pre=''): ms = int(t * 1000); return f"[{i}:a]{pre}aformat=sample_rates=48000:channel_layouts=stereo,volume={v},adelay={ms}|{ms}[s{i}]"
fc = [dl(2, 6.42), dl(3, 40.83), dl(4, 39.57, 1.0, 'atrim=0.4:1.65,asetpts=PTS-STARTPTS,'), dl(5, 54.0), dl(6, 73.09),
      "[s2][s3][s4][s5][s6]amix=inputs=5:normalize=0[dlg]", "[dlg]asplit=2[dlg1][sc]",
      dl(7, 0, .45), dl(8, 14.0, .6), dl(9, 24.4, .7), dl(10, 33.0, .6), dl(11, 34.17, .45), dl(12, 39.17, .3), dl(13, 44.08, .4), dl(14, 49.9, .7),
      dl(15, 75.8, .45), dl(16, 76.0, .6), dl(17, 80.3, .4),
      "[s7][s8][s9][s10][s11][s12][s13][s14][s15][s16][s17]amix=inputs=11:normalize=0[fx]",
      f"[1:a]atrim=0:{T},afade=t=in:st=0:d=1,afade=t=out:st={T-2}:d=2,aformat=sample_rates=48000:channel_layouts=stereo,volume=0.5[mu]",
      "[mu][sc]sidechaincompress=threshold=0.025:ratio=8:attack=30:release=400[mud]",
      f"[dlg1][fx][mud]amix=inputs=3:normalize=0,atrim=0:{T},loudnorm=I=-14:TP=-1.5,aformat=sample_rates=48000:channel_layouts=stereo[a]"]
subprocess.run(['ffmpeg','-loglevel','error','-y',*args,'-filter_complex',';'.join(fc),'-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart','LaEncomienda_v1.mp4'], check=True)
