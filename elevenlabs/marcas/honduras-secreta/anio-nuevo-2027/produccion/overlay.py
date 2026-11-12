import numpy as np, subprocess, json
from PIL import Image, ImageDraw, ImageFont
W, H, FPS = 1080, 1920, 24
FB='/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'; FX='/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf'; FM='../enc/fonts/PermanentMarker.ttf'
LOGO=Image.open('/home/user/Nicole-projects/elevenlabs/marcas/honduras-secreta/logo_honduras_secreta_reconstruido.png').convert('RGBA')
YEL=(255,214,64)
cv=lambda: Image.new('RGBA',(W,H),(0,0,0,0))
def sub(text, y, size=60, font=FB, fill=(255,255,255)):
    im=cv(); d=ImageDraw.Draw(im); lines=text.split('\n')
    while size>30 and max(d.textlength(l,font=ImageFont.truetype(font,size)) for l in lines)>960: size-=2
    f=ImageFont.truetype(font,size); hs=size*1.2; cy=y*H; yy=cy-hs*len(lines)/2
    for ln in lines:
        w=d.textlength(ln,font=f); d.text(((W-w)/2,yy),ln,font=f,fill=fill,stroke_width=7,stroke_fill=(0,0,0,230)); yy+=hs
    return im
def big(text, y, size, fill=YEL, font=FM):
    im=cv(); d=ImageDraw.Draw(im); d.text((W/2,y*H),text,font=ImageFont.truetype(font,size),fill=fill,anchor='mm',stroke_width=12,stroke_fill=(30,15,50)); return im
def endcard():
    im=Image.new('RGBA',(W,H),(14,10,36,205)); lw=820; lg=LOGO.resize((lw,int(LOGO.height*lw/LOGO.width))); im.alpha_composite(lg,((W-lw)//2,480)); d=ImageDraw.Draw(im)
    d.text((W/2,880),'¡Feliz Año Nuevo, catrachos!',font=ImageFont.truetype(FM,70),fill=YEL,anchor='mm')
    d.text((W/2,960),'Happy New Year, catrachos!',font=ImageFont.truetype(FB,40),fill=(235,235,235),anchor='mm')
    d.text((W/2,1110),'What would you leave',font=ImageFont.truetype(FX,58),fill=(255,255,255),anchor='mm')
    d.text((W/2,1180),'in the Año Viejo?',font=ImageFont.truetype(FX,58),fill=(255,255,255),anchor='mm')
    d.text((W/2,1270),'Tell us in the comments',font=ImageFont.truetype(FB,42),fill=(46,190,186),anchor='mm'); return im
S=[(3.0,5.1,"I brought the clothes\nfor the Año Viejo!",.42),
   (5.5,8.15,"This year we're making him\nreally big…",.24),(8.3,10.3,"…so he takes away\nall the bad stuff.",.24),
   (10.9,12.5,"Here go the power outages!",.25),
   (16.95,19.0,"Math homework!",.30),(19.9,21.8,"And the boulevard traffic!",.30),
   (22.6,23.6,"And this…",.25),(23.75,25.6,"…being flat broke!",.20),
   (25.95,28.0,"Where are you going,\nDoña Tencha?",.33),(28.1,30.6,"So I finally travel\nthis year, sweetie!",.42),
   (31.8,34.2,"Out with the bad…",.60),(34.8,37.2,"…in with the good!",.60),
   (38.85,42.1,"And careful with the fireworks,\nyou hear me, kids?",.30),(42.25,43.9,"Yes, Don Chepe!",.30),
   (61.9,65.6,"Happy New Year, little macaw.\nThank you for being with us.",.36),(65.55,67.5,"Happy New Year, Don Chepe!",.36),
   (71.9,75.0,"May we get to know\nour land better this year…",.45),(75.4,77.3,"…and may nobody\nbe broke.",.45)]
OV=[(0.3,2.9,big('EL AÑO VIEJO',.84,128))]
OV+=[(a,b,sub(t,y)) for a,b,t,y in S]
nums=[('10',45.87),('9',46.51),('8',47.33),('7',47.87),('6',48.45),('5',48.91),('4',49.47),('3',50.01),('2',50.45),('1',51.11)]
for i,(n,t) in enumerate(nums):
    e=nums[i+1][1] if i+1<len(nums) else 51.75; OV.append((t,e-.02,big(n,.16,230)))
OV.append((51.75,54.6,big('¡FELIZ AÑO!',.16,150))); OV.append((51.85,54.6,sub('HAPPY NEW YEAR!',.245,48)))
OV.append((77.1,81.54,endcard()))
OV=[(a,b,np.array(im).astype(np.float32)) for a,b,im in OV]
dec=subprocess.Popen(['ffmpeg','-loglevel','error','-i','seg/base2.mp4','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
enc=subprocess.Popen(['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','24','-i','-','-vf','format=yuv420p','-c:v','libx264','-crf','17','video_ov.mp4'],stdin=subprocess.PIPE)
i=0
while True:
    b=dec.stdout.read(W*H*3)
    if len(b)<W*H*3: break
    f=np.frombuffer(b,np.uint8).reshape(H,W,3).astype(np.float32); t=i/FPS
    for a0,a1,im in OV:
        if a0<=t<=a1:
            k=min(1,(t-a0)/.12,(a1-t)/.12); al=im[...,3:]/255*k; f=f*(1-al)+im[...,:3]*al
    enc.stdin.write(f.astype(np.uint8).tobytes()); i+=1
enc.stdin.close(); enc.wait(); print('frames',i)
