from st import *
import sys
L=sys.argv[1]  # 'es' o 'en'
E=(L=='en')
os.makedirs(f'out2/{L}',exist_ok=True)
CTA='Book now  ·  (631) 365-6004' if E else 'Agenda tu cita  ·  (631) 365-6004'
def save(im,n,name): im.convert('RGB').save(f'out2/{L}/{n:02d}_{name}_{L.upper()}.jpg',quality=94)
def tx(es,en): return en if E else es
def wendy_bg():
    im=paper((236,228,218)); w=Image.open('img/wendy_cut.png').convert('RGBA'); y0=H-w.height
    m=Image.new('L',w.size,255); g=np.linspace(0,1,180)
    for i,v in enumerate(g): ImageDraw.Draw(m).line([(0,i),(w.width,i)],fill=int(255*v))
    w.putalpha(m); im.alpha_composite(w,(0,y0)); return im
# 1 Wendy: Feliz Navidad
im=wendy_bg(); vgrad(im,False,.36,215); brand(im,y=150,col=CHOC)
text(im,(W/2,330),tx('Feliz Navidad','Merry Christmas'),F('gv',150),BURG)
sticker(im,'hat',200,(800,520),rot=18,sh=True); sticker(im,'bow',300,(70,480),rot=-14)
text(im,(W/2,1430),tx('DE PARTE DE TODO EL EQUIPO DE','FROM THE WHOLE TEAM AT'),F('ms',30,600),IVORY,sh=(0,0,0,230))
text(im,(W/2,1495),'Luxury Bella Spa',F('pfi',60,600),(240,215,170),sh=(0,0,0,230))
text(im,(W/2,1575),tx('Cupos de diciembre limitados','Limited December availability'),F('cgi',44,600),IVORY,sh=(0,0,0,230))
cta(im,1680,dark=True,t=CTA); save(im,1,'Wendy_Navidad' if not E else 'Wendy_MerryChristmas')
# 2 Últimos cupos de diciembre (calendario tachado)
im=paper(); brand(im)
text(im,(W/2,330),tx('Diciembre se llena','December fills up'),F('pfi',74,500),INK)
text(im,(W/2,440),tx('más rápido que Santa','faster than Santa'),F('gv',104),BURG)
box=(150,560,930,1190); card(im,box,40); d=ImageDraw.Draw(im)
d.text((W/2,640),tx('Diciembre','December'),font=F('pfi',84,700),fill=INK,anchor='mm')
days=['LU','MA','MI','JU','VI','SA','DO'] if not E else ['MO','TU','WE','TH','FR','SA','SU']; cw=(box[2]-box[0]-80)/7
for i,t in enumerate(days): d.text((box[0]+40+cw*(i+.5),725),t,font=F('ms',26,600),fill=(90,80,72),anchor='mm')
taken={1,2,3,4,5,6,8,9,10,11,12,13,15,16,17,18,19,20,22,23}
for dd in range(1,32):
    idx=dd; r,c=divmod(idx,7); x=box[0]+40+cw*(c+.5); y=785+r*62
    col=(190,180,170) if dd in taken else INK
    d.text((x,y),str(dd),font=F('ms',28,500),fill=col,anchor='mm')
    if dd in taken: d.line([(x-18,y+14),(x+18,y-14)],fill=BURG,width=4)
sticker(im,'bow',260,(790,1080),rot=12)
tag(im,W/2,1290,tx('QUEDAN POCOS ESPACIOS','ONLY A FEW SPOTS LEFT'),bg=CHOC)
text(im,(W/2,1390),tx('Facial · Dermaplaning · LED · Láser · Cera','Facial · Dermaplaning · LED · Laser · Wax'),F('cgi',42,600),INK)
cta(im,1560,t=CTA); save(im,2,'Ultimos_cupos' if not E else 'Last_spots')
# 3 Gift card
im=photo('flat',fy=.6); vgrad(im,True,.5,200,(250,246,240)); brand(im,col=CHOC)
text(im,(W/2,340),tx('El único regalo','The only gift'),F('pfi',78,500),INK)
text(im,(W/2,460),tx('que nadie devuelve','no one returns'),F('gv',110),BURG)
tag(im,W/2,590,tx('TARJETAS DE REGALO','GIFT CARDS'),bg=CHOC)
gc=giftcard(560,-6); paste_shadow(im,gc,(250,1000))
cta(im,1640,t=CTA); save(im,3,'GiftCard')
# 4 Checklist antes de Navidad
im=paper(); brand(im)
text(im,(W/2,330),tx('Tu checklist','Your pre-holiday'),F('pfi',76,500),INK); text(im,(W/2,440),tx('antes de Navidad','glow checklist'),F('gv',104),BURG)
torn(im,(130,560,950,1290)); d=ImageDraw.Draw(im)
items=[(tx('Piel suave para las fotos','Smooth skin for photos'),'Dermaplaning'),(tx('Glow e hidratación','Glow & hydration'),tx('Mascarilla facial','Facial mask')),(tx('Luz para tu piel','Light for your skin'),tx('Terapia LED','LED therapy')),(tx('Piernas listas','Party-ready legs'),tx('Cera o láser','Wax or laser')),(tx('Textura renovada','Renewed texture'),tx('Microdermoabrasión','Microdermabrasion'))]
for i,(a,b) in enumerate(items):
    y=650+i*122; d.rounded_rectangle((190,y-26,242,y+26),8,outline=CHOC,width=4); d.line([(200,y),(214,y+16),(236,y-18)],fill=BURG,width=7)
    d.text((275,y-18),a,font=F('ms',34,700),fill=INK,anchor='lm'); d.text((275,y+24),b,font=F('cgi',38,500),fill=(90,72,62),anchor='lm')
sticker(im,'hat',210,(790,480),rot=16)
cta(im,1440,t=CTA); save(im,4,'Checklist')
# 5 Party ready Dec 31
im=photo('wax',fy=.6); vgrad(im,True,.45,110,(255,250,244)); brand(im,col=CHOC)
text(im,(W/2,350),tx('Lista para','Ready for'),F('pfi',80,500),INK)
text(im,(W/2,480),tx('la fiesta del 31','the NYE party'),F('gv',120),BURG)
tag(im,W/2,620,tx('DEPILACIÓN CON CERA  ·  LÁSER','WAXING  ·  LASER HAIR REMOVAL'),bg=CHOC)
cta(im,1640,t=CTA); save(im,5,'Fiesta31' if not E else 'NYE_ready')
# 6 Propósitos de año nuevo
im=paper(); brand(im)
text(im,(W/2,320),tx('Mis propósitos','My 2027'),F('pfi',78,500),INK); text(im,(W/2,440),tx('2027','resolutions'),F('gv',120),BURG)
card(im,(130,560,950,1300),40); d=ImageDraw.Draw(im)
res=[(tx('Cuidar más mi piel','Take better care of my skin'),tx('Mascarillas faciales','Facial masks')),(tx('Decirle adiós a la rasuradora','Say goodbye to my razor'),tx('Depilación láser','Laser hair removal')),(tx('Brillar todo el año','Glow all year long'),tx('Terapia LED','LED therapy')),(tx('Piel más suave','Softer skin'),tx('Dermaplaning · Microdermo','Dermaplaning · Microderm')),(tx('Darme un tiempo para mí','Make time for me'),'Luxury Bella Spa')]
for i,(a,b) in enumerate(res):
    y=650+i*125; d.text((200,y-16),f'{i+1}.',font=F('pf',44,600),fill=GOLD,anchor='lm')
    d.text((265,y-16),a,font=F('ms',34,700),fill=INK,anchor='lm'); d.text((265,y+26),b,font=F('cgi',38,500),fill=(90,72,62),anchor='lm')
cta(im,1440,t=CTA); save(im,6,'Propositos' if not E else 'Resolutions')
# 7 LED post fiestas
im=photo('led',fy=.75); vgrad(im,True,.5,170); brand(im,col=GOLD)
text(im,(W/2,360),tx('Después de las fiestas…','After the holidays…'),F('pfi',70,500),IVORY,sh=(0,0,0,200))
text(im,(W/2,500),tx('recarga tu glow','recharge your glow'),F('gv',130),(240,210,160),sh=(0,0,0,200))
tag(im,W/2,640,tx('TERAPIA DE LUZ LED','LED LIGHT THERAPY'),bg=GOLD)
cta(im,1640,dark=True,t=CTA); save(im,7,'LED_recarga' if not E else 'LED_recharge')
# 8 Wendy te espera
im=wendy_bg(); vgrad(im,False,.34,215); brand(im,y=150,col=CHOC)
text(im,(W/2,320),tx('Tu piel en','Your skin in'),F('pfi',72,500),INK)
text(im,(W/2,440),tx('buenas manos','good hands'),F('gv',118),BURG)
text(im,(W/2,1470),tx('Te espera Wendy','Wendy is waiting for you'),F('pfi',58,600),(240,215,170),sh=(0,0,0,230))
text(im,(W/2,1550),tx('Agenda tu tratamiento de fin de año','Book your end-of-year treatment'),F('cgi',44,600),IVORY,sh=(0,0,0,230))
cta(im,1660,dark=True,t=CTA); save(im,8,'Wendy_te_espera' if not E else 'Wendy_waiting')
# 9 Feliz Año Nuevo
im=photo('gift',fy=.55); vgrad(im,True,.5,215,(250,246,240)); brand(im,col=CHOC)
text(im,(W/2,330),tx('Feliz','Happy'),F('pfi',84,500),INK)
text(im,(W/2,470),tx('Año Nuevo','New Year'),F('gv',150),BURG)
text(im,(W/2,600),'2027',F('cz',80,600),GOLD)
text(im,(W/2,690),tx('Gracias por dejarnos cuidarte este año','Thank you for letting us care for you this year'),F('cgi',42,600),INK)
cta(im,1640,t=CTA); save(im,9,'Feliz_Ano_Nuevo' if not E else 'Happy_New_Year')
print('ok',L)
