from PIL import Image, ImageDraw, ImageFont, ImageFilter
FM='../hs/enc/fonts/PermanentMarker.ttf'; FX='/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf'; FB='/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'
LOGO=Image.open('/home/user/Nicole-projects/elevenlabs/marcas/honduras-secreta/logo_honduras_secreta_reconstruido.png').convert('RGBA')
YEL=(255,206,84); JADE=(110,220,160); NAVY=(10,16,30)
def cover(src,W,H,fx=.5,fy=.5):
    im=Image.open(src).convert('RGB'); s=max(W/im.width,H/im.height); im=im.resize((int(im.width*s)+1,int(im.height*s)+1),Image.LANCZOS)
    x=int((im.width-W)*fx); y=int((im.height-H)*fy); return im.crop((x,y,x+W,y+H)).convert('RGBA')
def vgrad(im,top,h,a):
    W,H=im.size; g=Image.new('L',(1,256))
    for i in range(256): g.putpixel((0,i),int(a*(1-i/255)**1.3) if top else int(a*(i/255)**1.3))
    hh=int(H*h); ov=Image.new('RGBA',(W,hh),NAVY+(0,)); ov.putalpha(g.resize((W,hh))); im.alpha_composite(ov,(0,0 if top else H-hh)); return im
def T(d,xy,s,f,size,fill,st=9,maxw=None):
    if maxw:
        while d.textlength(s,font=ImageFont.truetype(f,size))>maxw: size-=2
    d.text(xy,s,font=ImageFont.truetype(f,size),fill=fill,anchor='mm',stroke_width=st,stroke_fill=NAVY)
def logo(im,w,xy):
    l=LOGO.resize((w,int(LOGO.height*w/LOGO.width))); sh=Image.new('RGBA',im.size,(0,0,0,0)); sh.paste((0,0,0,170),(xy[0]+4,xy[1]+5),l.split()[3].filter(ImageFilter.GaussianBlur(6))); im.alpha_composite(sh); im.alpha_composite(l,xy)
# Miniatura YouTube 1280x720
im=cover('promo/thumb_base.png',1280,720,.5,.5)
g=Image.new('L',(256,1))
for i in range(256): g.putpixel((i,0),int(215*(1-i/255)**1.1))
ov=Image.new('RGBA',(640,720),NAVY+(0,)); ov.putalpha(g.resize((640,720))); im.alpha_composite(ov)
d=ImageDraw.Draw(im)
T(d,(280,165),'KEVIN Y LAS',FM,78,YEL,10,500); T(d,(280,265),'ESTATUAS',FM,108,YEL,11,500)
T(d,(280,375),'El Reino de Copán',FX,50,(255,255,255),8,500)
d.rounded_rectangle((150,430,410,490),28,fill=(110,220,160,240)); d.text((280,460),'PARTES 1 Y 2',font=ImageFont.truetype(FX,32),fill=NAVY,anchor='mm')
logo(im,250,(155,600))
im.convert('RGB').save('promo/Copan_miniatura_YouTube.jpg',quality=93)
# Historia 1 · avance
im=cover('p1b/sf/C2.png',1080,1920,.5,.4); im=vgrad(im,True,.4,225); im=vgrad(im,False,.36,225); d=ImageDraw.Draw(im)
T(d,(540,240),'¿Y si las estatuas',FX,74,(255,255,255)); T(d,(540,330),'de Copán despertaran?',FX,74,(255,255,255),9,980)
T(d,(540,1540),'KEVIN Y LAS ESTATUAS',FM,96,YEL,10,1000); T(d,(540,1650),'Nueva serie · Muy pronto',FB,48,(255,255,255),7)
logo(im,300,(390,1760)); im.convert('RGB').save('promo/Copan_historia_1_avance.jpg',quality=93)
# Historia 2 · estreno parte 1
im=cover('p1b/sf/E.png',1080,1920,.5,.45); im=vgrad(im,True,.45,230); im=vgrad(im,False,.33,215); d=ImageDraw.Draw(im)
T(d,(540,220),'HOY · 6:00 P. M.',FX,84,YEL,10); T(d,(540,335),'KEVIN Y LAS ESTATUAS',FM,90,(255,255,255),10,1000)
T(d,(540,435),'El Reino de Copán · Parte 1',FB,50,JADE,7)
logo(im,300,(390,1760)); im.convert('RGB').save('promo/Copan_historia_2_estreno_parte1.jpg',quality=93)
# Historia 3 · parte 2
im=cover('p2/mb/03.png',1080,1920,.5,.5); im=vgrad(im,True,.42,230); im=vgrad(im,False,.36,225); d=ImageDraw.Draw(im)
T(d,(540,230),'¿Querés ver',FX,84,(255,255,255)); T(d,(540,330),'un secreto?',FX,84,(255,255,255))
T(d,(540,1540),'PARTE 2',FM,120,YEL,11); T(d,(540,1650),'El secreto del escriba · Mañana',FB,46,JADE,7,1000)
logo(im,300,(390,1760)); im.convert('RGB').save('promo/Copan_historia_3_parte2.jpg',quality=93)
print('ok')
