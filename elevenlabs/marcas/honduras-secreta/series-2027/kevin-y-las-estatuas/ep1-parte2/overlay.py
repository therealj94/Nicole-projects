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
    d.text((W/2,1610),'El Reino de Copán · Parte 2',font=ImageFont.truetype(FX,50),fill=(255,255,255),anchor='mm',stroke_width=7,stroke_fill=(30,15,50)); return im
def place(text,y):
    im=cv(); d=ImageDraw.Draw(im); f=ImageFont.truetype(FM,58); w=d.textlength(text,font=f); x=(W-w)/2
    d.rounded_rectangle((x-30,y-50,x+w+30,y+46),10,fill=(246,236,214,235)); d.text((x,y-42),text,font=f,fill=(120,60,20)); return im.rotate(-2,resample=Image.BICUBIC,center=(540,y))
def endcard():
    im=Image.new('RGBA',(W,H),(10,18,30,215)); d=ImageDraw.Draw(im)
    lw=620; lg=LOGO.resize((lw,int(LOGO.height*lw/LOGO.width))); im.alpha_composite(lg,((W-lw)//2,520))
    d.text((W/2,880),'Copán Ruinas',font=ImageFont.truetype(FM,86),fill=YEL,anchor='mm')
    d.text((W/2,965),'Patrimonio de la Humanidad · ¿Ya lo conocés?',font=ImageFont.truetype(FB,40),fill=(255,255,255),anchor='mm')
    d.text((W/2,1020),'World Heritage Site · Have you been there?',font=ImageFont.truetype(FB,32),fill=(200,200,200),anchor='mm')
    d.text((W/2,1170),'Próximo episodio: LEMPIRA',font=ImageFont.truetype(FX,56),fill=(255,255,255),anchor='mm')
    d.text((W/2,1240),'Next episode: Lempira',font=ImageFont.truetype(FB,38),fill=(46,190,186),anchor='mm'); return im
S=[(0.3,8.4,"This stairway is the longest Maya text in existence:\nover two thousand glyphs tell the story of our kings."),
   (9.1,11.4,"And you can read all of it?"),(13.6,17.9,"Almost all of it…\nsome are still a secret."),
   (20.4,23.2,"This is how your name\nwould be written, Kevin."),(26.0,28.2,"It looks better than my signature!"),
   (28.8,31.6,"It's just that I'm bad at math…"),(32.8,38.1,"One dot is one, one bar is five…\nand this shell is zero."),
   (40.0,42.4,"Oh, now I get it!"),(42.7,51.3,"This is Rosalila, a temple hidden inside the pyramid.\nA Honduran archaeologist discovered it in 1989."),
   (51.7,55.5,"A catracho discovering secrets…\njust like us!"),(56.3,59.6,"The sun is coming.\nWe have to turn back into stone."),
   (61.3,62.9,"Will I ever see you again?"),(65.2,72.0,"Every time someone visits us and takes care of us,\nwe'll be alive. Copán belongs to everyone, Kevin."),
   (73.6,77.1,"Excellent, Kevin!\nHow did you learn all this?"),(78.5,81.8,"Let's just say…\nthey told me in person.")]
OV=[(0.3,4.0,title()),(42.8,46.5,place('Templo Rosalila',1720))]
OV+=[(a,b,sub(t)) for a,b,t in S]
OV.append((87.0,91.08,endcard()))
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
