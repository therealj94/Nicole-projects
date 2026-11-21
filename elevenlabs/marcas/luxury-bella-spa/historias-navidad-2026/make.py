from st import *
import sys
os.makedirs('out',exist_ok=True)
def save(im,n): im.convert('RGB').save(f'out/Historia_{n:02d}.jpg',quality=94)
# 1 Portada calendario
im=paper(); brand(im)
text(im,(W/2,360),'ES LA ÉPOCA MÁS\nBONITA DEL AÑO…',F('pf',72,500),INK,spacing=14)
text(im,(W/2,530),'para consentirte.',F('pfi',84,500),BURG)
notif(im,640,'RECORDATORIO','Tu cita en Luxury Bella Spa')
box=(150,890,930,1520); card(im,box,40); d=ImageDraw.Draw(im)
d.text((W/2,975),'Diciembre',font=F('pfi',96,700),fill=INK,anchor='mm')
days=['LU','MA','MI','JU','VI','SA','DO']; cw=(box[2]-box[0]-80)/7
for i,t in enumerate(days): d.text((box[0]+40+cw*(i+.5),1075),t,font=F('ms',28,600),fill=(90,80,72),anchor='mm')
d.line([(box[0]+40,1105),(box[2]-40,1105)],fill=(225,218,210),width=2)
mark={5,12,19,23}; start=1
for dd in range(1,32):
    idx=start+dd-1; r,c=divmod(idx,7); x=box[0]+40+cw*(c+.5); y=1150+r*68
    if dd in mark: d.ellipse((x-27,y-27,x+27,y+27),fill=CHOC); col=IVORY
    else: col=INK
    d.text((x,y),str(dd),font=F('ms',30,500),fill=col,anchor='mm')
sticker(im,'hat',230,(800,800),rot=-18); sticker(im,'bow',330,(800,1390),rot=12)
text(im,(W/2,1600),'Reserva tu espacio antes de que se llene la agenda',F('cgi',40,500),INK)
cta(im,1690); save(im,1)
# 2 Gift card foto
im=photo('gift',fy=.55); brand(im,col=CHOC)
text(im,(W/2,380),'El regalo perfecto',F('gv',120),CHOC)
text(im,(W/2,520),'NO SE ENVUELVE,\nSE VIVE.',F('pf',66,600),INK,spacing=12)
tag(im,W/2,660,'TARJETAS DE REGALO DISPONIBLES',bg=CHOC)
gc=giftcard(380,-8); paste_shadow(im,gc,(340,1130))
cta(im,1640); save(im,2)
# 3 Lista de regalos
im=paper(); brand(im)
text(im,(W/2,330),'Mi lista de',F('pfi',70,500),INK); text(im,(W/2,430),'regalos navideños',F('gv',110),BURG)
torn(im,(130,540,950,1240))
d=ImageDraw.Draw(im); d.rounded_rectangle((470,505,610,575),14,fill=GOLD); d.rounded_rectangle((495,520,585,560),10,fill=(214,186,130))
items=[('Mamá','Mascarilla facial + LED',True),('Mi hermana','Dermaplaning',True),('Mi mejor amiga','Tarjeta de regalo',True),('Mi esposo','Depilación con cera',True),('Yo','…también me lo merezco',False)]
for i,(a,b,ok) in enumerate(items):
    y=650+i*112; d.rounded_rectangle((190,y-26,242,y+26),8,outline=CHOC,width=4)
    if ok: d.line([(200,y),(214,y+16),(236,y-18)],fill=BURG,width=7)
    d.text((275,y-18),a,font=F('ms',36,700),fill=INK,anchor='lm'); d.text((275,y+24),b,font=F('cgi',38,500),fill=(90,72,62),anchor='lm')
gc=giftcard(420,10); paste_shadow(im,gc,(560,1170)); sticker(im,'bow',260,(180,1210),rot=-14)
text(im,(W/2,1560),'Regala bienestar con una tarjeta de Luxury Bella Spa',F('cgi',38,500),INK)
cta(im,1660); save(im,3)
# 4 Dermaplaning búsqueda
im=photo('derma',fy=.6); vgrad(im,True,.5,120,(255,250,244)); brand(im,col=CHOC)
text(im,(W/2,330),'la búsqueda:',F('pfi',70,600),INK)
box=(110,400,970,500); card(im,box,50); d=ImageDraw.Draw(im)
d.text((160,450),'¿Cómo lucir piel suave en las fotos?',font=F('ms',33,500),fill=INK,anchor='lm')
d.ellipse((900,428,936,464),outline=INK,width=4); d.line([(930,460),(946,476)],fill=INK,width=5)
text(im,(W/2,610),'la solución:',F('pfi',70,600),INK); tag(im,W/2,700,'DERMAPLANING',F('ms',38,700),bg=CHOC)
torn(im,(150,1330,930,1520),(252,250,246))
text(im,(W/2,1425),'Retira el vello fino y las células muertas\npara una piel suave y un maquillaje impecable.',F('cg',36,600),INK,spacing=6)
cta(im,1620); save(im,4)
# 5 Dermaplaning polaroid
im=paper(); brand(im)
text(im,(W/2,320),'Piel de porcelana',F('gv',118),BURG)
text(im,(W/2,450),'PARA TODAS LAS FOTOS\nDE DICIEMBRE',F('pf',56,600),INK,spacing=10)
polaroid(im,'derma',560,(230,560),-4,fy=.62,cap='Dermaplaning')
sticker(im,'bow',240,(110,520),rot=-20)
for i,t in enumerate(['Textura más suave','Luminosidad al instante','El maquillaje se ve mejor']):
    y=1470+i*55; text(im,(W/2,y),'·  '+t+'  ·',F('ms',34,500),INK)
cta(im,1700); save(im,5)
# 6 Mascarillas
im=photo('mask',fy=.7); vgrad(im,True,.48,150,(255,250,244)); brand(im,col=CHOC)
text(im,(W/2,360),'Glow',F('gv',190),BURG); text(im,(W/2,520),'NAVIDEÑO',F('pf',84,600),INK)
text(im,(W/2,630),'Tu piel también merece un regalo.',F('cgi',52,500),INK)
tag(im,W/2,730,'MASCARILLAS FACIALES',bg=CHOC)
cta(im,1640); save(im,6)
# 7 LED
im=photo('led',fy=.75); vgrad(im,True,.5,170); brand(im,col=GOLD)
text(im,(W/2,370),'Este año las luces',F('pfi',74,500),IVORY,sh=(0,0,0,200))
text(im,(W/2,480),'también son',F('pfi',74,500),IVORY,sh=(0,0,0,200))
text(im,(W/2,610),'para tu piel',F('gv',140),(240,210,160),sh=(0,0,0,200))
tag(im,W/2,750,'TERAPIA DE LUZ LED',bg=GOLD)
cta(im,1640,dark=True); save(im,7)
# 8 LED notificaciones
im=paper(); brand(im)
text(im,(W/2,330),'Tu agenda de hoy',F('pfi',76,500),INK)
notif(im,430,'RECORDATORIO','Sesión de terapia de luz LED',when='4:00 pm')
notif(im,650,'TU PIEL','Lista para brillar estas fiestas',when='ahora')
notif(im,870,'LUXURY BELLA SPA','¡Te esperamos! Relájate y disfruta',when='ahora')
p=Image.open('img/led.png').convert('RGB'); s=520/p.width; p=p.resize((520,int(p.height*s))); p=p.crop((0,int(p.height*.55),520,int(p.height*.55)+400)).convert('RGBA')
m=Image.new('L',p.size,0); ImageDraw.Draw(m).rounded_rectangle((0,0,520,400),36,fill=255); p.putalpha(m)
paste_shadow(im,p,(280,1110)); sticker(im,'bow',220,(700,1060),rot=14)
cta(im,1630); save(im,8)
# 9 Láser
im=photo('laser',fy=.65); vgrad(im,True,.5,140,(255,250,244)); brand(im,col=CHOC)
text(im,(W/2,340),'Querido Santa:',F('gv',120),BURG)
text(im,(W/2,500),'este año quiero decirle\nadiós a la rasuradora.',F('pfi',62,500),INK,spacing=10)
tag(im,W/2,650,'DEPILACIÓN LÁSER',bg=CHOC)
cta(im,1640); save(im,9)
# 10 Láser plan
im=paper(); brand(im)
text(im,(W/2,330),'Empieza en diciembre…',F('pfi',70,500),INK)
text(im,(W/2,450),'y llega lista al verano',F('gv',104),BURG)
card(im,(110,560,970,1060),40); d=ImageDraw.Draw(im)
ms=['DIC','ENE','FEB','MAR','ABR','MAY','JUN']; x0,x1=180,900
d.line([(x0,800),(x1,800)],fill=(220,210,198),width=6)
for i,m_ in enumerate(ms):
    x=x0+(x1-x0)*i/6; on=i in (0,2,4)
    d.ellipse((x-26,800-26,x+26,800+26),fill=CHOC if on else (236,228,218))
    if on: d.text((x,800),'✦',font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',26),fill=GOLD,anchor='mm')
    d.text((x,870),m_,font=F('ms',28,700 if on else 500),fill=INK,anchor='mm')
d.text((W/2,660),'Tu plan de depilación láser',font=F('ms',36,700),fill=INK,anchor='mm')
d.text((W/2,960),'Se trabaja en varias sesiones espaciadas.',font=F('cgi',38,500),fill=(90,72,62),anchor='mm')
d.text((W/2,1010),'Pregunta por tu plan personalizado.',font=F('cgi',38,500),fill=(90,72,62),anchor='mm')
polaroid(im,'laser',380,(330,1090),3,fy=.6)
sticker(im,'hat',200,(640,1020),rot=16)
cta(im,1690); save(im,10)
# 11 Cera
im=photo('wax',fy=.6); vgrad(im,True,.45,90,(255,250,244)); brand(im,col=CHOC)
text(im,(W/2,370),'Suave',F('gv',190),BURG); text(im,(W/2,520),'COMO LA NIEVE',F('pf',76,600),INK)
text(im,(W/2,625),'Piel lista para lucir tu outfit de fiesta.',F('cgi',48,500),INK)
tag(im,W/2,720,'DEPILACIÓN CON CERA',bg=CHOC)
cta(im,1640); save(im,11)
# 12 Microderm
im=photo('micro',fy=.62); vgrad(im,True,.5,150,(255,250,244)); brand(im,col=CHOC)
text(im,(W/2,350),'Año nuevo,',F('pfi',86,500),INK); text(im,(W/2,480),'piel nueva',F('gv',140),BURG)
tag(im,W/2,620,'MICRODERMOABRASIÓN',bg=CHOC)
torn(im,(160,1330,920,1500),(252,250,246))
text(im,(W/2,1415),'Exfolia y renueva la textura de tu piel\npara empezar el año radiante.',F('cg',36,600),INK,spacing=6)
cta(im,1620); save(im,12)
# 13 Antes de despedir el año
im=paper(); brand(im)
text(im,(W/2,330),'Antes de despedir el año,',F('pfi',62,500),INK); text(im,(W/2,440),'despide también…',F('gv',100),BURG)
torn(im,(150,540,930,1010))
d=ImageDraw.Draw(im)
for i,t in enumerate(['la piel opaca','la textura áspera','las células muertas']):
    y=640+i*120; d.line([(222,y-18),(258,y+18)],fill=BURG,width=7); d.line([(258,y-18),(222,y+18)],fill=BURG,width=7); d.text((300,y),t,font=F('pf',50,500),fill=INK,anchor='lm')
    d.line([(300,y+4),(300+d.textlength(t,font=F('pf',50,500)),y+4)],fill=(150,60,70),width=3)
polaroid(im,'micro',400,(140,1050),-5,fy=.6)
text(im,(800,1230),'Hola,',F('gv',90),BURG); text(im,(800,1340),'MICRODERMO-\nABRASIÓN',F('ms',38,700),INK,spacing=6)
cta(im,1680); save(im,13)
# 14 Menú navideño
im=paper(); brand(im)
p=Image.open('img/room.png').convert('RGB'); s=800/p.width; p=p.resize((800,int(p.height*s))); p=p.crop((0,int(p.height*.35),800,int(p.height*.35)+360)).convert('RGBA')
m=Image.new('L',p.size,0); ImageDraw.Draw(m).rounded_rectangle((0,0,800,360),36,fill=255); p.putalpha(m); paste_shadow(im,p,(140,240))
text(im,(W/2,700),'Menú navideño',F('gv',120),BURG)
d=ImageDraw.Draw(im); d.line([(330,775),(750,775)],fill=GOLD,width=2)
sv=['Tarjetas de regalo','Dermaplaning','Mascarillas faciales','Terapia de luz LED','Depilación láser','Depilación con cera','Microdermoabrasión']
for i,t in enumerate(sv):
    y=850+i*86; text(im,(W/2,y),t,F('pf',50,500),INK)
    if i<len(sv)-1: d.text((W/2,y+43),'✦',font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',18),fill=GOLD,anchor='mm')
sticker(im,'bow',230,(60,1130),rot=-16)
cta(im,1500); save(im,14)
# 15 Cierre
im=photo('woman',fy=.5); vgrad(im,True,.42,200,(255,250,244)); vgrad(im,False,.40,230); brand(im,col=CHOC)
text(im,(W/2,370),'Feliz Navidad',F('gv',150),BURG)
text(im,(W/2,1390),'DE PARTE DE TODO EL EQUIPO DE',F('ms',30,600),IVORY,sh=(0,0,0,230))
text(im,(W/2,1450),'Luxury Bella Spa',F('pfi',58,600),(240,215,170),sh=(0,0,0,230))
text(im,(W/2,1530),'Cupos de diciembre limitados',F('cgi',44,600),IVORY,sh=(0,0,0,230))
cta(im,1630,dark=True); save(im,15)
print('ok')
