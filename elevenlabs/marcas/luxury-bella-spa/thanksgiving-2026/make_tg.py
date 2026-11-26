import sys,os; sys.path.insert(0,os.getcwd())
from st import *
src=Image.open(sys.argv[1]).convert('RGBA'); out=sys.argv[2]
for L in ['es','en']:
    E=L=='en'
    im=src.resize((W,int(src.height*W/src.width)),Image.LANCZOS).crop((0,0,W,H)) if src.width/src.height<W/H else src.resize((W,H))
    im=im.resize((W,H)); vgrad(im,True,.24,170); vgrad(im,False,.36,245)
    brand(im,y=95,col=IVORY)
    text(im,(W/2,215),'Happy Thanksgiving' if E else 'Feliz Día de',F('gv',118 if E else 96),IVORY,sh=(0,0,0,200))
    if not E: text(im,(W/2,320),'Acción de Gracias',F('gv',104),IVORY,sh=(0,0,0,200))
    text(im,(W/2,1485),'THANK YOU FOR TRUSTING US' if E else 'GRACIAS POR CONFIAR EN NOSOTRAS',F('ms',30,600),IVORY,sh=(0,0,0,230))
    text(im,(W/2,1555),'Wendy & the Luxury Bella Spa team' if E else 'Wendy y el equipo de Luxury Bella Spa',F('pfi',46,600),(240,215,170),sh=(0,0,0,230))
    text(im,(W/2,1625),'We are grateful for you' if E else 'Agradecidas de tenerte',F('cgi',42,600),IVORY,sh=(0,0,0,230))
    cta(im,1730,dark=True,t='Book now  ·  (631) 365-6004' if E else 'Agenda tu cita  ·  (631) 365-6004')
    im.convert('RGB').save(f'{out}_{L.upper()}.jpg',quality=94)
