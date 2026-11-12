from PIL import Image, ImageDraw, ImageFont, ImageFilter
FM='../enc/fonts/PermanentMarker.ttf'; FX='/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf'; FB='/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'
LOGO=Image.open('/home/user/Nicole-projects/elevenlabs/marcas/honduras-secreta/logo_honduras_secreta_reconstruido.png').convert('RGBA')
YEL=(255,214,64); WHITE=(255,255,255); DARK=(20,14,40)
def cover(src,W,H,fx=.5,fy=.5):
    im=Image.open(src).convert('RGB'); s=max(W/im.width,H/im.height); im=im.resize((int(im.width*s)+1,int(im.height*s)+1),Image.LANCZOS)
    x=int((im.width-W)*fx); y=int((im.height-H)*fy); return im.crop((x,y,x+W,y+H)).convert('RGBA')
def grad(im,top=True,h=.45,a=200):
    W,H=im.size; g=Image.new('L',(1,256)); 
    for i in range(256): g.putpixel((0,i),int(a*(1-i/255)**1.3) if top else int(a*(i/255)**1.3))
    g=g.resize((W,int(H*h))); ov=Image.new('RGBA',(W,int(H*h)),DARK+(0,)); ov.putalpha(g)
    im.alpha_composite(ov,(0,0 if top else H-int(H*h))); return im
def text(d,xy,t,font,size,fill,anchor='mm',stroke=10,sc=DARK):
    d.text(xy,t,font=ImageFont.truetype(font,size),fill=fill,anchor=anchor,stroke_width=stroke,stroke_fill=sc)
def logo(im,w,xy):
    l=LOGO.resize((w,int(LOGO.height*w/LOGO.width))); sh=Image.new('RGBA',im.size,(0,0,0,0)); m=l.split()[3].filter(ImageFilter.GaussianBlur(6))
    sh.paste((0,0,0,170),(xy[0]+4,xy[1]+5),m); im.alpha_composite(sh); im.alpha_composite(l,xy)
# 1 · Miniatura YouTube 1280x720
im=cover('promo/thumb_h_fix.png',1280,720,.62,.5); im=grad(im,True,.0+1.0,0)
ov=Image.new('RGBA',(640,720)); g=Image.new('L',(256,1))
for i in range(256): g.putpixel((i,0),int(190*(1-i/255)))
ov=Image.new('RGBA',(640,720),DARK+(0,)); ov.putalpha(g.resize((640,720))); im.alpha_composite(ov)
d=ImageDraw.Draw(im)
text(d,(300,250),'EL AÑO',FM,138,YEL,stroke=12); text(d,(300,395),'VIEJO',FM,168,YEL,stroke=12)
text(d,(300,520),'versión catracha',FX,52,WHITE,stroke=8)
logo(im,300,(40,600))
im.convert('RGB').save('promo/AnoViejo_miniatura_YouTube.jpg',quality=93)
# 2 · Portada Reel 1080x1920 (título dentro de la zona segura 4:5 del perfil)
im=cover('promo/story1_fix.png',1080,1920,.5,.5); im=grad(im,True,.42,215); im=grad(im,False,.22,170); d=ImageDraw.Draw(im)
text(d,(540,430),'EL AÑO VIEJO',FM,150,YEL,stroke=12)
text(d,(540,575),'¿Qué vas a dejar atrás?',FX,62,WHITE,stroke=9)
logo(im,420,(330,1700))
im.convert('RGB').save('promo/AnoViejo_portada_Reel.jpg',quality=93)
# 3 · Historia 1 (teaser 29 dic)
im=cover('sf/02.png',1080,1920,.5,.55); im=grad(im,True,.45,225); im=grad(im,False,.35,215); d=ImageDraw.Draw(im)
text(d,(540,330),'Algo se está armando',FX,72,WHITE,stroke=9); text(d,(540,420),'en el barrio…',FX,72,WHITE,stroke=9)
text(d,(540,1560),'EL AÑO VIEJO',FM,130,YEL,stroke=12); text(d,(540,1690),'Muy pronto en Honduras Secreta',FB,46,WHITE,stroke=7)
logo(im,300,(390,1770))
im.convert('RGB').save('promo/AnoViejo_historia_1_teaser.jpg',quality=93)
# 4 · Historia 2 (día del estreno, con espacio para sticker de pregunta)
im=cover('sf/03.png',1080,1920,.5,.6); im=grad(im,True,.5,230); im=grad(im,False,.3,200); d=ImageDraw.Draw(im)
text(d,(540,250),'HOY · 6:00 P. M.',FX,84,YEL,stroke=10)
text(d,(540,360),'EL AÑO VIEJO',FM,120,WHITE,stroke=12)
d.rounded_rectangle((140,470,940,700),36,outline=(255,255,255,200),width=4)
text(d,(540,540),'¿Qué querés dejar',FX,52,WHITE,stroke=6); text(d,(540,612),'en el Año Viejo?',FX,52,WHITE,stroke=6)
text(d,(540,672),'(poné aquí el sticker de pregunta)',FB,26,(255,255,255,170),stroke=0)
logo(im,300,(390,1780))
im.convert('RGB').save('promo/AnoViejo_historia_2_estreno.jpg',quality=93)
print('ok')
