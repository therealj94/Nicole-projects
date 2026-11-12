from PIL import Image, ImageDraw, ImageFont, ImageFilter
FM='fonts/PermanentMarker.ttf'; FR='fonts/Fraunces.ttf'; FX='/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf'; FB='/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'
LOGO=Image.open('/home/user/Nicole-projects/elevenlabs/marcas/honduras-secreta/logo_honduras_secreta_reconstruido.png').convert('RGBA')
CREAM=(255,240,215); GOLD=(255,200,110); TEAL=(70,210,205); NAVY=(12,18,40)
W,H=1080,1920
def cover(src,fy=.5):
    im=Image.open(src).convert('RGB'); s=max(W/im.width,H/im.height); im=im.resize((int(im.width*s)+1,int(im.height*s)+1),Image.LANCZOS)
    y=int((im.height-H)*fy); x=(im.width-W)//2; return im.crop((x,y,x+W,y+H)).convert('RGBA')
def grad(im,top=True,h=.45,a=210):
    g=Image.new('L',(1,256))
    for i in range(256): g.putpixel((0,i),int(a*(1-i/255)**1.3) if top else int(a*(i/255)**1.3))
    hh=int(H*h); ov=Image.new('RGBA',(W,hh),NAVY+(0,)); ov.putalpha(g.resize((W,hh))); im.alpha_composite(ov,(0,0 if top else H-hh)); return im
def t(d,y,s,font,size,fill,stroke=8): d.text((W/2,y),s,font=ImageFont.truetype(font,size),fill=fill,anchor='mm',stroke_width=stroke,stroke_fill=NAVY)
def logo(im,w=300,y=1770):
    l=LOGO.resize((w,int(LOGO.height*w/LOGO.width))); sh=Image.new('RGBA',im.size,(0,0,0,0)); sh.paste((0,0,0,170),((W-w)//2+4,y+5),l.split()[3].filter(ImageFilter.GaussianBlur(6))); im.alpha_composite(sh); im.alpha_composite(l,((W-w)//2,y))
# 1 · Avance (10 dic)
im=cover('hist/e01_clean.png',.45); im=grad(im,True,.42,220); im=grad(im,False,.38,225); d=ImageDraw.Draw(im)
t(d,250,'Esta Navidad,',FR,74,CREAM); t(d,345,'alguien está muy lejos de casa…',FR,56,CREAM)
t(d,1530,'LA ENCOMIENDA',FM,118,GOLD,10); t(d,1650,'Estreno · 12 de diciembre',FB,48,(255,255,255),7)
logo(im); im.convert('RGB').save('hist/Encomienda_historia_1_avance.jpg',quality=93)
# 2 · Estreno (12 dic)
im=cover('sv_11.png',.55); im=grad(im,True,.5,230); im=grad(im,False,.3,210); d=ImageDraw.Draw(im)
t(d,230,'HOY · 6:00 P. M.',FX,84,GOLD,10); t(d,350,'LA ENCOMIENDA',FM,118,CREAM,10)
t(d,470,'Para los que se fueron a buscar un sueño…',FR,40,CREAM,6); t(d,525,'y para los que los esperan en casa.',FR,40,CREAM,6)
logo(im); im.convert('RGB').save('hist/Encomienda_historia_2_estreno.jpg',quality=93)
# 3 · Convocatoria #DesdeHondurasConAmor
im=cover('sv_10.png',.5); im=grad(im,True,.55,235); im=grad(im,False,.3,215); d=ImageDraw.Draw(im)
t(d,220,'¿Tenés a alguien lejos?',FX,70,(255,255,255),9)
t(d,320,'Mandale un mensaje de 30 segundos.',FB,44,CREAM,6); t(d,378,'Lo publicamos el 24 de diciembre.',FB,44,CREAM,6)
d.rounded_rectangle((150,450,930,640),36,outline=(255,255,255,210),width=4)
t(d,520,'Mandalo por mensaje directo',FX,46,(255,255,255),5); t(d,585,'hasta el 15 de diciembre',FB,36,GOLD,4)
t(d,1640,'#DesdeHondurasConAmor',FX,62,TEAL,8)
logo(im); im.convert('RGB').save('hist/Encomienda_historia_3_convocatoria.jpg',quality=93)
print('ok')
