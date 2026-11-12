import subprocess, os
os.makedirs('hd', exist_ok=True)
for n in ['01','02','03','04a','04b','05','06','07','08']:
    src = f'fix/{n}.mp4' if n in ('01','04a') else f'vid/{n}.mp4'
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',src,'-vf','scale=1080:1920:flags=lanczos','-c:v','libx264','-crf','12','-pix_fmt','yuv420p','-an',f'hd/{n}.mp4'],check=True)
print('ok')
