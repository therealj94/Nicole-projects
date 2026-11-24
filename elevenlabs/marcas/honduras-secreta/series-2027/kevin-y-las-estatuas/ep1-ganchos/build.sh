#!/bin/bash
# uso: build.sh N Y_texto  (N=1|2). Requiere c$N.mp4 (Kling), vo$N.mp3, sfx$N.mp3, t${N}a.png, t${N}b.png, hp$N.png
set -e; N=$1; K=/tmp/claude-0/-home-user-Nicole-projects/dd5b2fc2-184e-5514-b789-f8432119b327/scratchpad/kevin
[ $N = 1 ] && EV=$K/p1b/final/KevinCopan_Parte1_v2_vertical.mp4 || EV=$K/p2/final/KevinCopan_Parte2_vertical.mp4
[ $N = 1 ] && SW=1.2 || SW=2.0
D=4.3
# 1) gancho vertical con texto y audio
ffmpeg -v error -y -i c$N.mp4 -loop 1 -i t${N}a.png -loop 1 -i t${N}b.png -i vo$N.mp3 -i sfx$N.mp3 -filter_complex "\
[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=24,trim=0:$D,setpts=PTS-STARTPTS[v0];\
[1:v]format=rgba,fade=in:st=0.15:d=0.2:alpha=1,fade=out:st=$(echo "$SW-0.12"|bc):d=0.12:alpha=1[a];\
[2:v]format=rgba,fade=in:st=$SW:d=0.15:alpha=1[b];\
[v0][a]overlay=0:0:shortest=1:enable='lt(t,$SW)'[v1];[v1][b]overlay=0:0:shortest=1:enable='gte(t,$SW)',fade=out:st=$(echo "$D-0.25"|bc):d=0.25:color=white,format=yuv420p[v];\
[3:a]atempo=1.1,adelay=200|200,aresample=48000,volume=1.15[vo];[4:a]aresample=48000,volume=0.5,afade=out:st=3.6:d=0.7[sf];\
[vo][sf]amix=inputs=2:normalize=0,atrim=0:$D,apad=whole_dur=$D,aformat=channel_layouts=stereo[aud]" \
 -map "[v]" -map "[aud]" -t $D -c:v libx264 -crf 17 -preset medium -c:a aac -b:a 192k -ar 48000 hook${N}_v.mp4
# 2) gancho + episodio vertical
ffmpeg -v error -y -i hook${N}_v.mp4 -i $EV -filter_complex "[1:v]fade=in:st=0:d=0.25:color=white[e];[0:v][0:a][e][1:a]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" -c:v libx264 -crf 18 -preset medium -c:a aac -b:a 192k -movflags +faststart final${N}_v.mp4
# 3) horizontal: fondo difuminado + vertical al centro + paneles
ffmpeg -v error -y -i final${N}_v.mp4 -i hp$N.png -filter_complex "[0:v]split[a][b];[a]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=30:3,eq=brightness=-0.12[bg];[b]scale=-2:1080[fg];[bg][fg]overlay=(W-w)/2:0[c];[c][1:v]overlay=0:0,format=yuv420p[v]" -map "[v]" -map 0:a -c:v libx264 -crf 19 -preset medium -c:a copy -movflags +faststart final${N}_h.mp4
# 4) móvil
ffmpeg -v error -y -i final${N}_v.mp4 -vf scale=720:1280 -c:v libx264 -crf 25 -preset medium -c:a aac -b:a 128k -movflags +faststart final${N}_v_movil.mp4
ls -la final${N}*
