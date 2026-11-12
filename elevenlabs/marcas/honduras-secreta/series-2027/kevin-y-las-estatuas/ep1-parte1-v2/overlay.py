import numpy as np, subprocess, json
from PIL import Image, ImageDraw, ImageFont
W, H, FPS = 1080, 1920, 24
FB='/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'; FX='/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf'; FM='../../hs/enc/fonts/PermanentMarker.ttf'
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
    d.text((W/2,1610),'El Reino de Copán · Parte 1',font=ImageFont.truetype(FX,50),fill=(255,255,255),anchor='mm',stroke_width=7,stroke_fill=(30,15,50)); return im
def place(text,y):
    im=cv(); d=ImageDraw.Draw(im); f=ImageFont.truetype(FM,58); w=d.textlength(text,font=f); x=(W-w)/2
    d.rounded_rectangle((x-30,y-50,x+w+30,y+46),10,fill=(246,236,214,235)); d.text((x,y-42),text,font=f,fill=(120,60,20)); return im.rotate(-2,resample=Image.BICUBIC,center=(540,y))
def endcard():
    im=Image.new('RGBA',(W,H),(10,18,30,215)); d=ImageDraw.Draw(im)
    d.text((W/2,760),'CONTINUARÁ…',font=ImageFont.truetype(FM,120),fill=YEL,anchor='mm')
    d.text((W/2,860),'To be continued…',font=ImageFont.truetype(FB,44),fill=(230,230,230),anchor='mm')
    d.text((W/2,1010),'Parte 2: el secreto del escriba',font=ImageFont.truetype(FX,54),fill=(255,255,255),anchor='mm')
    d.text((W/2,1080),'Part 2: the scribe\'s secret',font=ImageFont.truetype(FB,40),fill=(46,190,186),anchor='mm')
    lw=420; lg=LOGO.resize((lw,int(LOGO.height*lw/LOGO.width))); im.alpha_composite(lg,((W-lw)//2,1280)); return im
S=[(0.4,3.7,"What's so interesting about\na bunch of old rocks?"),(5.8,6.7,"Rocks?"),(6.75,9.95,"Grab your backpack, kid…\nwe're going to Copán."),
   (11.4,13.7,"Cousins! The family is here!"),(16.7,19.1,"Yeah… just rocks."),(19.7,20.6,"Rocks?"),(20.65,25.5,"I am Waxaklajuun Ub'aah K'awiil,\nthirteenth king of Copán!"),
   (26.3,30.2,"Waxa…? Waxa…? What?"),(30.6,35.2,"Wa… Waxa… Waxaklaju…\nugh, my beak got tangled!"),
   (35.6,40.2,"You can call me 18 Rabbit.\nCome, I'll show you my kingdom."),(41.1,44.3,"Here are the sixteen kings of Copán."),(44.35,48.0,"The first one founded the city\nin the year 426."),
   (48.8,51.3,"That's like 1,600 years ago!"),(53.5,55.3,"Welcome, cousin!"),(55.8,58.4,"Are you… my great-great-grandmothers?"),
   (59.2,63.7,"The macaw was sacred to us.\nThat's why they guard the court."),(64.5,67.1,"With your hip, not your hands!"),(67.4,70.4,"Goooal… I mean, point!"),
   (72.9,76.0,"And that's nothing…\nwant to see a secret?")]
OV=[(0.3,4.0,title()),(11.4,15.0,place('Copán Ruinas, Copán',1720))]
OV+=[(a,b,sub(t)) for a,b,t in S]
OV.append((76.3,79.83,endcard()))
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
