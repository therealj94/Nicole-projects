# Prepara cada clip 4K en horizontal (1920x1080) y vertical (recorte 1215x2160 -> 1080x1920, con paneo opcional)
import subprocess, sys
CROP = {  # centro x del recorte vertical (fracción del ancho): inicio, fin
 'i0': (.5, .5), 'i1': (.5, .5), 'i2': (.5, .5), 'i3': (.5, .5), 'i4': (.5, .5), 'i5': (.5, .5), 'i6c': (.5, .5), 'i7': (.5, .5), 'i8': (.5, .5),
 's1': (.40, .40), 's2': (.47, .60), 's3': (.46, .46), 's4': (.36, .50), 's5': (.47, .47), 's6': (.5, .5), 's7': (.5, .5)}
k = sys.argv[1]; src = f'vid/{k}.mp4'
dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src]))
c0, c1 = CROP[k]; x0 = c0 * 3840 - 607.5; x1 = c1 * 3840 - 607.5
xexp = f"'max(0,min(3840-1215,{x0}+({x1}-{x0})*min(t/{dur},1)))'"
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', src, '-vf', 'scale=1920:1080:flags=lanczos', '-c:v', 'libx264', '-crf', '12', '-c:a', 'copy', f'prep/{k}_h.mp4'], check=True)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', src, '-vf', f"crop=1215:2160:x={xexp}:y=0,scale=1080:1920:flags=lanczos", '-c:v', 'libx264', '-crf', '12', '-c:a', 'copy', f'prep/{k}_v.mp4'], check=True)
print('ok', k)
