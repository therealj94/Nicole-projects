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
    d.text((W/2,1610),'Lempira, señor de la sierra · Parte 2',font=ImageFont.truetype(FX,50),fill=(255,255,255),anchor='mm',stroke_width=7,stroke_fill=(30,15,50)); return im
def place(text,y):
    im=cv(); d=ImageDraw.Draw(im); f=ImageFont.truetype(FM,58); w=d.textlength(text,font=f); x=(W-w)/2
    d.rounded_rectangle((x-30,y-50,x+w+30,y+46),10,fill=(246,236,214,235)); d.text((x,y-42),text,font=f,fill=(120,60,20)); return im.rotate(-2,resample=Image.BICUBIC,center=(540,y))
def endcard():
    im=Image.new('RGBA',(W,H),(10,18,30,215)); d=ImageDraw.Draw(im)
    lw=620; lg=LOGO.resize((lw,int(LOGO.height*lw/LOGO.width))); im.alpha_composite(lg,((W-lw)//2,520))
    d.text((W/2,880),'Gracias, Lempira',font=ImageFont.truetype(FM,80),fill=YEL,anchor='mm')
    d.text((W/2,965),'Ciudad colonial y tierra lenca · ¿Ya la conocés?',font=ImageFont.truetype(FB,40),fill=(255,255,255),anchor='mm')
    d.text((W/2,1020),'Colonial town and Lenca land · Have you been there?',font=ImageFont.truetype(FB,32),fill=(200,200,200),anchor='mm')
    d.text((W/2,1170),'Próximo episodio: LOS GARÍFUNAS',font=ImageFont.truetype(FX,56),fill=(255,255,255),anchor='mm')
    d.text((W/2,1240),'Next episode: The Garifuna',font=ImageFont.truetype(FB,38),fill=(46,190,186),anchor='mm'); return im
S=[(0.1,7.6,"Finally, visitors! I'm from La Campa, where Lenca women\nhave made clay pots like me for centuries."),
   (10.2,11.6,"And those drawings?"),(12.0,15.0,"Every line tells something about our people."),(15.1,19.0,"And I don't mean to brag…\nbut I look gorgeous."),
   (20.0,25.6,"This is the Guancasco: two villages visit each other\nto make peace and celebrate together."),
   (26.0,28.5,"Like when you make up with your best buddy!"),
   (29.5,35.9,"My name is on the money so you never forget:\nthe worth of a people is in its people."),
   (37.0,38.3,"Thank you, Lempira."),(40.1,42.9,"And how do you know so much about Lempira?"),(44.2,47.3,"Let's just say…\nhe told me himself.")]
OV=[(0.3,3.3,title()),(3.4,7.2,place('La Campa, Lempira',1720)),(19.7,23.3,place('El Guancasco',1720))]
OV+=[(a,b,sub(t)) for a,b,t in S]
OV.append((53.3,57.58,endcard()))
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
