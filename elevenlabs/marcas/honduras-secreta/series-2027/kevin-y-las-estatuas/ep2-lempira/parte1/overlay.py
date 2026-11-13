import numpy as np, subprocess, json
from PIL import Image, ImageDraw, ImageFont
W, H, FPS = 1080, 1920, 24
FB='/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'; FX='/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf'; FM='../../../hs/enc/fonts/PermanentMarker.ttf'
LOGO=Image.open('/home/user/Nicole-projects/elevenlabs/marcas/honduras-secreta/logo_honduras_secreta_reconstruido.png').convert('RGBA')
YEL=(255,214,64)
cv=lambda: Image.new('RGBA',(W,H),(0,0,0,0))
def sub(text, y=.075, size=44, font=FB, fill=(255,255,255)):
    im=cv(); d=ImageDraw.Draw(im); lines=text.split('\n')
    while size>30 and max(d.textlength(l,font=ImageFont.truetype(font,size)) for l in lines)>960: size-=2
    f=ImageFont.truetype(font,size); hs=size*1.2; cy=y*H; yy=cy-hs*len(lines)/2
    for ln in lines:
        w=d.textlength(ln,font=f); d.text(((W-w)/2,yy),ln,font=f,fill=fill,stroke_width=5,stroke_fill=(0,0,0,235)); yy+=hs
    return im
def big(text, y, size, fill=YEL, font=FM):
    im=cv(); d=ImageDraw.Draw(im); d.text((W/2,y*H),text,font=ImageFont.truetype(font,size),fill=fill,anchor='mm',stroke_width=12,stroke_fill=(30,15,50)); return im
def title():
    im=cv(); d=ImageDraw.Draw(im)
    d.text((W/2,1500),'KEVIN Y LAS ESTATUAS',font=ImageFont.truetype(FM,92),fill=YEL,anchor='mm',stroke_width=11,stroke_fill=(30,15,50))
    d.text((W/2,1610),'Lempira, señor de la sierra · Parte 1',font=ImageFont.truetype(FX,50),fill=(255,255,255),anchor='mm',stroke_width=7,stroke_fill=(30,15,50)); return im
def place(text,y):
    im=cv(); d=ImageDraw.Draw(im); f=ImageFont.truetype(FM,58); w=d.textlength(text,font=f); x=(W-w)/2
    d.rounded_rectangle((x-30,y-50,x+w+30,y+46),10,fill=(246,236,214,235)); d.text((x,y-42),text,font=f,fill=(120,60,20)); return im.rotate(-2,resample=Image.BICUBIC,center=(540,y))
def endcard():
    im=Image.new('RGBA',(W,H),(14,12,10,215)); d=ImageDraw.Draw(im)
    d.text((W/2,760),'CONTINUARÁ…',font=ImageFont.truetype(FM,120),fill=YEL,anchor='mm')
    d.text((W/2,860),'To be continued…',font=ImageFont.truetype(FB,44),fill=(230,230,230),anchor='mm')
    d.text((W/2,1010),'Parte 2: el secreto de la sierra',font=ImageFont.truetype(FX,54),fill=(255,255,255),anchor='mm')
    d.text((W/2,1080),'Part 2: the secret of the mountains',font=ImageFont.truetype(FB,40),fill=(46,190,186),anchor='mm')
    lw=420; lg=LOGO.resize((lw,int(LOGO.height*lw/LOGO.width))); im.alpha_composite(lg,((W-lw)//2,1280)); return im
S=[(0.4,3.0,"Why is our money called lempira?"),(3.71,7.61,"You don't know? Grab your backpack…\nwe're going to Gracias."),
   (8.31,12.71,"Welcome to Gracias, one of the\noldest cities in Honduras!"),(13.11,15.21,"Whoa! It's the guy on the bill!"),
   (16.81,21.71,"I am Lempira, lord of the mountains.\nAnd yes… also the guy on the bill."),
   (23.01,28.41,"Come. I'll show you why\nmy people never gave up."),(29.11,33.61,"From here I united many mountain villages\nto defend our land."),
   (35.31,36.91,"Weren't you scared?"),(39.11,43.41,"Of course we were. But together…\nfear becomes small."),(46.81,48.81,"And nobody's going to introduce me?")]
OV=[(0.3,3.3,title()),(8.21,11.81,place('Gracias, Lempira',1720)),(28.61,32.21,place('Peñol de Cerquín',1720))]
OV+=[(a,b,sub(t)) for a,b,t in S]
OV.append((49.51,53.04,endcard()))
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
